"""AAI_METRICS — Stage-A rollout observability for docs+code indexing (#288).

Pure telemetry, ZERO behavior change: every function here only *reads* pipeline
state and *emits* one greppable line; nothing it does alters a verdict, an index,
or a landing decision. Two event lines are emitted on real runs:

  AAI_METRICS index    scope + chunk breakdown by source_type + churn + embed cost/latency
  AAI_METRICS classify scope + verdict distribution + the guard signals (uncovered
                       existence, code_only_grounded frequency, documentation gaps)

The `index` line establishes the churn/latency/cost baseline; the `classify` line
establishes the verdict-drift + guard baseline. Both are consumed off the job log /
step summary — no external sink, no new dependency. `scope_label`, `chunk_breakdown`,
`embed_cost_usd`, `classify_fields` and `format_line` are pure + unit-tested; `emit`
is the only side-effecting call (print + optional GITHUB_STEP_SUMMARY append).
"""
from __future__ import annotations

import json
import os
from pathlib import Path

from retrieval import source_type   # the canonical code/doc/other classifier the guard uses

# text-embedding-3-large list price, 2026-01. tokens≈chars/4 is a documented ESTIMATE
# (we do not call a tokenizer in-band); `embed_cost_usd` is a cost *proxy*, not a bill.
EMBED_USD_PER_1M_TOKENS = 0.13
CHARS_PER_TOKEN = 4


def scope_label() -> str:
    """`docs+code` iff the active index scope includes `.py` (via INDEX_EXTS env),
    else `docs`. Read-only — mirrors pipeline._index_scope's env, does not set it."""
    exts = os.environ.get("INDEX_EXTS", "")
    return "docs+code" if ".py" in exts else "docs"


def chunk_breakdown(records: dict) -> dict:
    """Count index records by evidence domain. Pure."""
    out = {"chunks_total": 0, "chunks_doc": 0, "chunks_code": 0, "chunks_other": 0}
    for rec in (records or {}).values():
        out["chunks_total"] += 1
        out[f"chunks_{source_type(rec.get('path', ''))}"] += 1
    return out


def embed_cost_usd(chars: int) -> float:
    """Estimated embedding cost for `chars` characters embedded this run. Pure proxy."""
    return round((chars / CHARS_PER_TOKEN) / 1_000_000 * EMBED_USD_PER_1M_TOKENS, 6)


def classify_fields(classifications: list[dict]) -> dict:
    """Verdict-drift + guard signals for one classify run. Pure — reuses the merged
    guard (`landing.is_documentation_covered` / `documentation_gaps`)."""
    import landing
    from landing import COVERAGE_VERDICTS
    counts: dict[str, int] = {}
    for c in classifications or []:
        counts[c.get("verdict", "?")] = counts.get(c.get("verdict", "?"), 0) + 1
    coverage = [c for c in classifications or [] if c.get("verdict") in COVERAGE_VERDICTS]
    covered = [c for c in coverage if landing.is_documentation_covered(c)]
    code_only = sum(1 for c in classifications or [] if c.get("code_only_grounded"))
    return {
        "patterns": len(classifications or []),
        "verdicts": json.dumps(counts, ensure_ascii=False, separators=(",", ":")),
        "exists_total": len(coverage),
        "exists_covered": len(covered),
        "exists_uncovered": len(coverage) - len(covered),
        "code_only_grounded": code_only,
        "doc_gaps": len(landing.documentation_gaps(classifications or [])),
    }


def format_line(event: str, fields: dict) -> str:
    """`AAI_METRICS <event> k=v k=v ...` — stable, greppable, one line. Pure."""
    kv = " ".join(f"{k}={v}" for k, v in fields.items())
    return f"AAI_METRICS {event} {kv}".rstrip()


def emit(event: str, fields: dict) -> str:
    """Print the metrics line and append to GITHUB_STEP_SUMMARY when present. The ONLY
    side effect in this module; returns the line (for tests)."""
    line = format_line(event, fields)
    print(line, flush=True)
    path = os.environ.get("GITHUB_STEP_SUMMARY")
    if path:
        try:
            with open(path, "a", encoding="utf-8") as fh:
                fh.write(line + "\n")
        except OSError:
            pass   # telemetry must never break a run
    return line
