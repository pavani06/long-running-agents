"""Deterministic grep-verify of the classifier's citations.

Every `file:line` the model cites must exist and actually contain what it claims.
This is the safety net against fabricated evidence: a classification whose
citation fails verification is not trustworthy. The verification logic is pure
(`verify_citation`); reading the cited files is the only I/O (`verify_all`).
"""
from __future__ import annotations

import re
from pathlib import Path


def _norm(s: str) -> str:
    """Collapse whitespace so a quote survives reflowing/indentation differences."""
    return re.sub(r"\s+", " ", s).strip()


def verify_citation(file_text: str, line: int, quote: str = "", *, window: int = 2) -> dict:
    """Check `line` exists in `file_text` and (if given) `quote` appears within
    ±window lines of it. Pure. Returns {ok, reason}."""
    lines = file_text.splitlines()
    if line < 1 or line > len(lines):
        return {"ok": False, "reason": f"line {line} out of range (file has {len(lines)})"}
    if not quote or not quote.strip():
        return {"ok": True, "reason": "line exists (no quote to match)"}
    lo = max(0, line - 1 - window)
    hi = min(len(lines), line - 1 + window + 1)
    hay = _norm(" ".join(lines[lo:hi]))
    if _norm(quote) in hay:
        return {"ok": True, "reason": "quote found near cited line"}
    return {"ok": False, "reason": "quote not found near cited line"}


def verify_all(citations: list[dict], repo_root: Path) -> list[dict]:
    """Verify each {file, line, quote?} citation against disk (I/O).

    Returns each citation augmented with `ok`/`reason`. A missing file fails
    (never raises), so one bad citation cannot abort the batch."""
    out: list[dict] = []
    cache: dict[str, str | None] = {}
    for c in citations:
        file = c.get("file", "")
        if file not in cache:
            fp = repo_root / file
            cache[file] = fp.read_text(encoding="utf-8") if fp.exists() else None
        text = cache[file]
        if text is None:
            out.append({**c, "ok": False, "reason": f"file not found: {file}"})
            continue
        res = verify_citation(text, int(c.get("line", 0) or 0), c.get("quote", ""))
        out.append({**c, **res})
    return out


def all_ok(verified: list[dict]) -> bool:
    """True when every citation verified (empty list counts as ok)."""
    return all(v.get("ok") for v in verified)
