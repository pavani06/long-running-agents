"""Surgically set the `relates-to` line in an extract's frontmatter.

Touches only that one line — inserts it (or replaces an existing one) just
before the closing `---`, leaving every other byte of the file unchanged.
"""
from __future__ import annotations

import json
from pathlib import Path

EXTRACTS_REL = "extracts/youtube/ai-learning"


def wikilink(file: str, title: str) -> str:
    """`[[extracts/youtube/ai-learning/<file-without-.md>|<title>]]`."""
    target = f"{EXTRACTS_REL}/{file[:-3] if file.endswith('.md') else file}"
    return f"[[{target}|{title}]]"


def set_relates_to(text: str, wikilinks: list[str]) -> str:
    """Return `text` with a single `relates-to:` line set in the frontmatter."""
    if not text.startswith("---\n"):
        return text
    end = text.find("\n---", 3)
    if end == -1:
        return text
    head = text[: end + 1]  # includes up to the newline before closing ---
    rest = text[end + 1:]   # the closing '---' and body

    lines = [ln for ln in head.split("\n") if not ln.startswith("relates-to:")]
    # Drop a possible trailing empty element from the split, keep structure tidy.
    while lines and lines[-1] == "":
        lines.pop()
    lines.append("relates-to: " + json.dumps(wikilinks, ensure_ascii=False))
    return "\n".join(lines) + "\n" + rest


def update_file(path: Path, wikilinks: list[str]) -> bool:
    """Rewrite the file's relates-to; return True if the content changed."""
    original = path.read_text(encoding="utf-8")
    updated = set_relates_to(original, wikilinks)
    if updated != original:
        path.write_text(updated, encoding="utf-8")
    return updated != original
