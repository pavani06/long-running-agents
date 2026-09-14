"""E/R/V dataset capture for Gate-C failure characterization (#288 follow-up).

The metamorphic PoC's Gate C (every existence verdict must cite grep-verifiable
evidence) sat at 43% docs-only and 10% docs+code. `grep_verify` is an aggregate
pass/fail; we cannot yet say WHY it fails. This module runs the classifier over
the canon and persists a durable, reusable dataset with the automatable signals
needed to separate the failure axes:

  V (verifier outcome)   — did grep_verify (quote within ±2 lines) accept?  automatable.
  R (reference correctness) — is the cited file real, and does the quote appear
      ANYWHERE in it (right file, maybe wrong line) vs nowhere?             automatable.
  E (evidence correctness)  — does the cited evidence actually support the concept?
      NOT automatable here — left for offline human/Claude judgment over the dataset.

Per the evidence-provenance ADR, this only CHARACTERIZES the instrument; it fixes
nothing. It emits the dataset (as an Actions artifact) and a compact summary, and
stops. `source_type`, `quote_anywhere` and `citation_signals` are pure and
unit-tested; `run` makes the live calls.
"""
from __future__ import annotations

import json
import os
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import grep_verify  # noqa: E402
import metamorphic_canon as mc  # noqa: E402
import phase3_classify  # noqa: E402
import retrieval  # noqa: E402
from embed import embed_texts  # noqa: E402
from glm import GLMError, RateLimited  # noqa: E402
from retrieval import rank_sections  # noqa: E402


def _summary(line: str) -> None:
    print(line)
    path = os.environ.get("GITHUB_STEP_SUMMARY")
    if path:
        with open(path, "a", encoding="utf-8") as fh:
            fh.write(line + "\n")


def source_type(path: str) -> str:
    """Classify a cited path by evidence domain. Pure."""
    if path.endswith(".py"):
        return "code"
    if path.endswith(".md"):
        return "doc"
    return "other"


def quote_anywhere(quote: str, file_text: str) -> bool:
    """Does the (whitespace-collapsed) quote appear ANYWHERE in the file? Pure.

    Separates 'right file, wrong location' (True but grep_verify's ±2-line window
    rejected) from 'quote not in file at all'."""
    if not quote or not quote.strip():
        return False
    norm = lambda s: re.sub(r"\s+", " ", s).strip()
    return norm(quote) in norm(file_text)


def citation_signals(cit: dict, file_text: str | None, verify_result: dict) -> dict:
    """Automatable R/V signals for one citation. Pure.

    `auto_axis` is a FIRST-CUT label from automatable signals only — the E axis
    (is the evidence actually correct/relevant) is deliberately left None for
    offline judgment."""
    file_exists = file_text is not None
    passed = bool(verify_result.get("ok"))
    anywhere = quote_anywhere(cit.get("quote", ""), file_text) if file_exists else False
    if not file_exists:
        auto = "R0_file_missing"
    elif passed:
        auto = "V1_verified"
    elif anywhere:
        auto = "R1_wrong_location"      # right file, quote present, ±2-window missed it
    else:
        auto = "R0E_quote_absent"       # quote nowhere in file → bad ref or bad/hallucinated evidence
    return {
        "file": cit.get("file"), "source_type": source_type(cit.get("file", "")),
        "line": cit.get("line"), "quote": cit.get("quote", ""),
        "file_exists": file_exists, "quote_at_line": passed,
        "quote_anywhere": anywhere, "verify_reason": verify_result.get("reason"),
        "auto_axis": auto, "E_evidence_correct": None,  # offline
    }


def _classify(variant: str, index: dict, openai_key: str, zai_key: str, repo_root: Path):
    """Classify one variant; return (verdict, citations, verified_list). Tolerant."""
    pattern = {"name": variant[:80], "problem": variant, "mechanism": ""}
    retriever = retrieval.make_pattern_retriever([pattern], index, openai_key, repo_root)
    try:
        cls = phase3_classify.run([pattern], zai_key, retriever=retriever)
    except (GLMError, RateLimited) as e:
        return None, [], [], str(e)
    citations = phase3_classify.citations_of(cls)
    verified = grep_verify.verify_all(citations, repo_root)
    return cls[0].get("verdict"), cls[0].get("evidence", []), verified, None


def run(canon_path: str) -> int:
    openai_key = os.environ.get("OPENAI_API_KEY")
    zai_key = os.environ.get("ZAI_API_KEY")
    if not openai_key or not zai_key:
        _summary("evrv: OPENAI_API_KEY and ZAI_API_KEY both required")
        return 1
    repo_root = Path(__file__).resolve().parents[2]
    state_path = repo_root / ".runtime" / "analyze-and-improve" / "index.json"
    if not state_path.exists():
        _summary("evrv: index not built — run `pipeline.py index --full` first")
        return 1
    index = json.loads(state_path.read_text(encoding="utf-8"))
    canon = mc.load_canon(Path(canon_path))
    variants = mc.all_variants(canon)

    records, file_cache = [], {}
    for v in variants:
        vvec = embed_texts([v["variant"]], openai_key)[0]
        retrieved = [{"path": r["path"], "source_type": source_type(r["path"]),
                      "score": round(r["score"], 3)} for r in rank_sections(vvec, index, k=8)]
        verdict, evidence, verified, err = _classify(
            v["variant"], index, openai_key, zai_key, repo_root)
        by_key = {(c.get("file"), c.get("line"), c.get("quote")): c for c in verified}
        cits = []
        for e in evidence:
            f = e.get("file", "")
            if f not in file_cache:
                fp = repo_root / f
                file_cache[f] = fp.read_text(encoding="utf-8") if fp.is_file() else None
            vr = by_key.get((e.get("file"), e.get("line"), e.get("quote")), {})
            cits.append(citation_signals(e, file_cache[f], vr))
        records.append({
            "concept_id": v["concept_id"], "expected_verdict": v["expected_verdict"],
            "exists": v["exists"], "variant": v["variant"], "verdict": verdict,
            "error": err, "retrieved_topk": retrieved, "citations": cits,
        })

    out_path = os.environ.get("EVRV_OUT", "evrv-dataset.json")
    Path(out_path).write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    _summary(_report(records, out_path))
    return 0


def _report(records: list[dict], out_path: str) -> str:
    existence = {"Exists", "Partial", "Better"}
    cits = [c for r in records for c in r["citations"] if r["verdict"] in existence]
    axis = Counter(c["auto_axis"] for c in cits)
    by_src = Counter((c["source_type"], c["auto_axis"]) for c in cits)
    verdicts = Counter(r["verdict"] for r in records)
    errored = sum(1 for r in records if r["error"])
    lines = [
        "# E/R/V dataset — Gate-C failure characterization (#288)", "",
        f"Dataset persistido: `{out_path}` (artifact). {len(records)} variantes"
        + (f" · ⚠️ {errored} com erro de LLM" if errored else "") + ".", "",
        f"Vereditos: {dict(verdicts)}", "",
        f"Citações de vereditos de existência: **{len(cits)}**", "",
        "## Distribuição auto (só sinais automatizáveis — eixo E fica p/ análise offline)",
        f"- `V1_verified` (verificou): **{axis.get('V1_verified', 0)}**",
        f"- `R1_wrong_location` (arquivo certo, quote existe, janela ±2 errou): **{axis.get('R1_wrong_location', 0)}**",
        f"- `R0E_quote_absent` (quote não está no arquivo → ref ruim ou evidência ruim/alucinada): **{axis.get('R0E_quote_absent', 0)}**",
        f"- `R0_file_missing` (arquivo citado não existe): **{axis.get('R0_file_missing', 0)}**", "",
        "## Por domínio (code vs doc)",
    ]
    for (src, ax), n in sorted(by_src.items()):
        lines.append(f"- {src} / {ax}: {n}")
    lines += [
        "", "## Leitura (o que cada célula implicaria — NÃO corrigir agora)",
        "- `R1_wrong_location` dominante em `code` → gargalo é o **verificador** (quote±2 hostil a código); não o modelo.",
        "- `R0E_quote_absent` dominante → problema de **attribution/grounding** (o modelo cita o que não está lá).",
        "- `R0_file_missing` relevante → o modelo inventa caminhos.",
        "",
        "**STOP obrigatório (ADR, Princípio 3):** este passo caracteriza o instrumento e para. "
        "Nenhuma correção nesta execução — a próxima intervenção passa por gate humano.",
    ]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    import argparse
    default = str(Path(__file__).resolve().parent / "metamorphic_canon.yaml")
    ap = argparse.ArgumentParser(description="E/R/V dataset capture (#288)")
    ap.add_argument("canon", nargs="?", default=default)
    return run(ap.parse_args(argv).canon)


if __name__ == "__main__":
    raise SystemExit(main())
