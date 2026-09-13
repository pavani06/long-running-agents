"""Surgically set the `theme` line in an extract's frontmatter.

Touches only that one line — preserves relates-to, all other keys, and the body.
"""
from __future__ import annotations

import json
from pathlib import Path


def set_theme(text: str, theme: str) -> str:
    if not text.startswith("---\n"):
        return text
    end = text.find("\n---", 3)
    if end == -1:
        return text
    head = text[: end + 1]
    rest = text[end + 1:]
    lines = [ln for ln in head.split("\n") if not ln.startswith("theme:")]
    while lines and lines[-1] == "":
        lines.pop()
    lines.append("theme: " + json.dumps(theme, ensure_ascii=False))
    return "\n".join(lines) + "\n" + rest


def update_theme(path: Path, theme: str) -> bool:
    original = path.read_text(encoding="utf-8")
    updated = set_theme(original, theme)
    if updated != original:
        path.write_text(updated, encoding="utf-8")
    return updated != original
