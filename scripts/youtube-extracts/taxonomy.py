"""Controlled tag vocabulary for extracts.

Built dynamically from the tags already used across the repo's curated content
(docs/canonical, docs/analysis, system-of-record) plus a small theme extension
for the "AI - Learning" corpus. Keeping extract tags inside this set is what
lets the implicit Obsidian graph connect extracts to existing canonical notes.
"""
from __future__ import annotations

import re
from pathlib import Path

# Themes the corpus centers on (from the pipeline handoff) — seeded so the
# vocabulary is useful even before much curated content references them.
THEME_EXTENSION = [
    "harness-engineering",
    "context-engineering",
    "evals",
    "agent-fleets",
    "governanca",
    "ontologia",
    "agentes-orquestracao",
    "agentic-coding",
    "observability",
    "production",
]

# Inline YAML array: tags: ["a", "b"]  (the repo's frontmatter style).
_TAGS_LINE = re.compile(r'^tags:\s*\[(.*?)\]', re.MULTILINE)
_QUOTED = re.compile(r'"([^"]+)"|\'([^\']+)\'')


def _tags_in_file(path: Path) -> set[str]:
    try:
        head = path.read_text(encoding="utf-8")[:4000]
    except OSError:
        return set()
    out: set[str] = set()
    for m in _TAGS_LINE.finditer(head):
        for q in _QUOTED.finditer(m.group(1)):
            tag = (q.group(1) or q.group(2)).strip()
            if tag:
                out.add(tag)
    return out


def build_vocabulary(repo_root: Path) -> list[str]:
    """Union of curated tags + theme extension, sorted and de-duplicated."""
    vocab: set[str] = set(THEME_EXTENSION)
    sources = [repo_root / "docs" / "system-of-record.md"]
    for sub in ("docs/canonical", "docs/analysis"):
        base = repo_root / sub
        if base.exists():
            sources.extend(base.rglob("*.md"))
    for path in sources:
        vocab |= _tags_in_file(path)
    return sorted(vocab)
