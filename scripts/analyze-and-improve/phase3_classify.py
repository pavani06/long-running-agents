"""Fase 3 — classificação de cada padrão contra o repo, com evidência real.

Classifica Missing/Partial/Exists/Better usando contexto montado por busca
híbrida (retrieval.py). Suporta **1 rodada 'pedir mais'**: se o modelo declara
que falta contexto, ele nomeia greps/arquivos exatos num campo estruturado, o
código busca e faz a 2ª chamada. As citações são verificadas depois por
grep_verify (determinístico).

`build_messages`, `parse_classification` e `parse_ask_for_more` são puros e
testados; `run` injeta o cliente GLM e o retriever.
"""
from __future__ import annotations

import json

from glm import GLMError, chat_json

VERDICTS = {"Missing", "Partial", "Exists", "Better"}

_SYSTEM = (
    "Você classifica cada padrão candidato contra o repositório-alvo, usando "
    "SOMENTE o contexto fornecido (seções recuperadas + ocorrências de grep). "
    "Para cada padrão, decida um veredito: 'Missing' (não existe no repo), "
    "'Partial' (existe parcialmente), 'Exists' (já coberto), 'Better' (a fonte "
    "melhora o que existe). Cite evidência real como file:line do contexto — "
    "nunca invente caminhos. Se o contexto for insuficiente para classificar com "
    "segurança, NÃO adivinhe: nomeie no campo 'need_more' os greps/arquivos exatos "
    "que faltam. Responda APENAS um objeto JSON válido (sem markdown):\n"
    '{"classifications": [{"pattern": string, "verdict": '
    '"Missing|Partial|Exists|Better", "evidence": [{"file": string, "line": '
    'number, "quote": string}], "rationale": string}], '
    '"need_more": {"greps": [string], "files": [string]}}\n'
    "Deixe need_more com listas vazias quando o contexto bastar."
)


def build_messages(patterns: list[dict], context: str) -> list[dict]:
    """System + user for Fase 3: the candidate patterns and the retrieved context."""
    user = ("PADRÕES CANDIDATOS (da Fase 2):\n"
            + json.dumps(patterns, ensure_ascii=False)   # compact — keep the prompt small
            + "\n\nCONTEXTO DO REPO (busca híbrida):\n" + context)
    return [{"role": "system", "content": _SYSTEM},
            {"role": "user", "content": user}]


def parse_ask_for_more(reply: dict) -> dict | None:
    """Return the model's need_more spec iff it names any grep or file; else None."""
    nm = reply.get("need_more") or {}
    greps = [g for g in (nm.get("greps") or []) if isinstance(g, str) and g.strip()]
    files = [f for f in (nm.get("files") or []) if isinstance(f, str) and f.strip()]
    if greps or files:
        return {"greps": greps, "files": files}
    return None


def parse_classification(reply: dict) -> list[dict]:
    """Validate the classifications array and each item's shape/verdict. Pure."""
    items = reply.get("classifications")
    if not isinstance(items, list):
        raise GLMError("classification: 'classifications' must be an array")
    for i, c in enumerate(items):
        if not isinstance(c, dict):
            raise GLMError(f"classifications[{i}] not an object")
        if c.get("verdict") not in VERDICTS:
            raise GLMError(f"classifications[{i}] invalid verdict: {c.get('verdict')!r}")
        if not c.get("pattern"):
            raise GLMError(f"classifications[{i}] missing 'pattern'")
        if not isinstance(c.get("evidence"), list):
            raise GLMError(f"classifications[{i}] 'evidence' must be an array")
    return items


def citations_of(classifications: list[dict]) -> list[dict]:
    """Flatten every classification's evidence into grep_verify citations.

    Each citation carries a `source_type` provenance tag (G1, #288). NON-COUPLING:
    the tag is metadata only — `mark_verified` keys on pattern/ok/quote and ignores
    it, so a code-sourced citation is verified by exactly the same rule as a doc one."""
    from retrieval import source_type
    out: list[dict] = []
    for c in classifications:
        for e in c.get("evidence", []):
            if isinstance(e, dict) and e.get("file"):
                out.append({"file": e["file"], "line": e.get("line", 0),
                            "quote": e.get("quote", ""), "pattern": c.get("pattern"),
                            "source_type": source_type(e["file"])})
    return out


def mark_verified(classifications: list[dict], verified_citations: list[dict]) -> list[dict]:
    """Set each classification's `verified` flag with verdict-aware policy.

    A `Missing` verdict claims nothing exists, so it needs no citation → verified.
    Any existence verdict (Exists/Better/Partial) is only `verified` when it has
    at least one citation whose **content** was checked (a non-empty quote that
    grep-verified) and none of its citations failed. This closes two gaps: an
    empty-quote citation (line exists but content unchecked) and a bare verdict
    with no evidence at all no longer count as verified.
    """
    by_pat: dict[str, list[dict]] = {}
    for v in verified_citations:
        by_pat.setdefault(v.get("pattern"), []).append(v)
    for c in classifications:
        cits = by_pat.get(c.get("pattern"), [])
        if c.get("verdict") == "Missing":
            c["verified"] = True
        else:
            has_content = any(x.get("ok") and (x.get("quote") or "").strip() for x in cits)
            no_failures = all(x.get("ok") for x in cits)
            c["verified"] = bool(cits) and has_content and no_failures
    return classifications


EXISTENCE_VERDICTS = VERDICTS - {"Missing"}   # Exists/Partial/Better assert the concept is present


def _grounds(cit: dict) -> bool:
    """A citation counts as grounding iff its content was actually checked: it
    grep-verified (`ok`) AND carried a non-empty quote. Same bar as `mark_verified`
    — a line that exists but was never content-checked is not grounding."""
    return bool(cit.get("ok")) and bool((cit.get("quote") or "").strip())


def mark_grounding(classifications: list[dict], verified_citations: list[dict]) -> list[dict]:
    """Annotate each classification with the provenance of its VERIFIED grounding.

    Adds two DERIVED-ONLY fields (the `verdict` is never touched, so the field is
    byte-compatible for every existing consumer of `verdict`):

    * `grounding`: {"code": nc, "doc": nd, "other": no} — counts of this verdict's
      grep-verified, content-checked citations by `source_type`.
    * `code_only_grounded`: True iff this is an **existence** verdict whose verified
      grounding is **exclusively** code (≥1 verified code citation, 0 verified doc
      citations). This is a statement about THIS RUN's evidence only — "this
      existence verdict was grounded solely in verified code citations here." It does
      NOT assert that the concept is implemented, nor that it is undocumented; it makes
      no ontology claim beyond what was cited.

    NON-COUPLING (extends the G1 invariant): these fields are read FROM provenance,
    never fed back into `verdict` or `verified`. `source_type == "code"` still cannot,
    by itself, set any verdict.
    """
    by_pat: dict[str, list[dict]] = {}
    for v in verified_citations:
        by_pat.setdefault(v.get("pattern"), []).append(v)
    for c in classifications:
        cits = [x for x in by_pat.get(c.get("pattern"), []) if _grounds(x)]
        counts = {"code": 0, "doc": 0, "other": 0}
        for x in cits:
            st = x.get("source_type")
            counts[st if st in counts else "other"] += 1
        c["grounding"] = counts
        c["code_only_grounded"] = (
            c.get("verdict") in EXISTENCE_VERDICTS
            and counts["code"] >= 1 and counts["doc"] == 0
        )
    return classifications


def run(patterns: list[dict], api_key: str, *, retriever, client=chat_json) -> list[dict]:
    """Fase 3 with one 'ask for more' round. `retriever(need_more)->context` and
    `client` are injectable. need_more=None asks for the initial context."""
    context = retriever(None)
    reply = client(build_messages(patterns, context), api_key)
    need_more = parse_ask_for_more(reply)
    if need_more:
        context = context + "\n\n" + retriever(need_more)
        reply = client(build_messages(patterns, context), api_key)
    return parse_classification(reply)
