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


# CANDIDATE (#288 Track D — NOT the merged production behaviour; staged for the RED gate).
# The ±2-line matcher rejected ~68% of legitimate existence citations (E/R/V run): the
# quote is real and in the right file, but the model's line number is approximate or the
# quote spans/reflows across lines. Fix = a whole-file fallback, GUARDED by a minimum
# normalized length so short/common strings can't false-accept (offline: cross-file
# false-accept 0%, short-common 0/7 at ≥40; recall 32%→85%). The presence check still
# does NOT judge semantic support — that is the verdict/E-axis's job, by design.
MIN_WHOLEFILE_QUOTE_CHARS = 40


def verify_citation(file_text: str, line: int, quote: str = "", *, window: int = 2,
                    min_wholefile_chars: int = MIN_WHOLEFILE_QUOTE_CHARS) -> dict:
    """Check the cited `quote` is real evidence in `file_text`. Pure. Returns {ok, reason}.

    Order: (1) precise — quote within ±window of the cited line (strongest signal);
    (2) guarded whole-file — quote present anywhere, but only if it is at least
    `min_wholefile_chars` normalized chars (blocks short/common-string false-accepts).
    An empty quote just asserts the line exists."""
    lines = file_text.splitlines()
    line_in_range = 1 <= line <= len(lines)
    nquote = _norm(quote)
    if not nquote:
        return ({"ok": True, "reason": "line exists (no quote to match)"} if line_in_range
                else {"ok": False, "reason": f"line {line} out of range (file has {len(lines)})"})
    if line_in_range:
        lo = max(0, line - 1 - window)
        hi = min(len(lines), line - 1 + window + 1)
        if nquote in _norm(" ".join(lines[lo:hi])):
            return {"ok": True, "reason": "quote found near cited line"}
    present = nquote in _norm(file_text)
    if present and len(nquote) >= min_wholefile_chars:
        return {"ok": True, "reason": f"quote found in file (whole-file, ≥{min_wholefile_chars} chars)"}
    if present:
        return {"ok": False, "reason": f"quote present but < {min_wholefile_chars} chars and not near cited line"}
    return {"ok": False, "reason": "quote not found near cited line or in file"}


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
