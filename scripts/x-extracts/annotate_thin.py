#!/usr/bin/env python3
"""One-time backfill: stamp `thin: true|false` on existing extract frontmatter.

Future extracts get `thin` natively from render.build_note; this annotates the
extracts written before that change. Pure frontmatter surgery — no GLM, no
network, no secrets. Idempotent (re-running rewrites the same value).

Usage: python scripts/x-extracts/annotate_thin.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from thin import is_thin  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]
EXTRACTS_DIR = REPO_ROOT / "extracts" / "x" / "bookmarks"


def _fm_value(block: str, key: str):
    for line in block.splitlines():
        k, sep, v = line.partition(": ")
        if sep and k.strip() == key:
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return v.strip()
    return None


def set_thin(text: str, value: bool) -> str:
    """Set a single `thin:` line in the frontmatter (insert or replace)."""
    if not text.startswith("---\n"):
        return text
    end = text.find("\n---", 3)
    if end == -1:
        return text
    head, rest = text[: end + 1], text[end + 1:]
    lines = [ln for ln in head.split("\n") if not ln.startswith("thin:")]
    while lines and lines[-1] == "":
        lines.pop()
    lines.append(f"thin: {json.dumps(value)}")
    return "\n".join(lines) + "\n" + rest


def main() -> int:
    if not EXTRACTS_DIR.exists():
        print("no extracts dir")
        return 0
    changed = thin_n = 0
    total = 0
    for path in sorted(EXTRACTS_DIR.glob("*.md")):
        if path.name == "README.md":
            continue
        total += 1
        text = path.read_text(encoding="utf-8")
        block = text.split("---", 2)[1] if text.startswith("---") else ""
        value = is_thin(_fm_value(block, "key_points"), _fm_value(block, "grounded_in"))
        thin_n += int(value)
        updated = set_thin(text, value)
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            changed += 1
    print(f"annotated {total} extracts: {thin_n} thin, {total - thin_n} not; {changed} files changed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
