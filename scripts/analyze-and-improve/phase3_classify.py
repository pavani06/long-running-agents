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
            + json.dumps(patterns, ensure_ascii=False, indent=2)
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
    """Flatten every classification's evidence into grep_verify citations."""
    out: list[dict] = []
    for c in classifications:
        for e in c.get("evidence", []):
            if isinstance(e, dict) and e.get("file"):
                out.append({"file": e["file"], "line": e.get("line", 0),
                            "quote": e.get("quote", ""), "pattern": c.get("pattern")})
    return out


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
