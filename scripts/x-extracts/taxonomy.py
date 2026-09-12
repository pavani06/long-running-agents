"""Controlled tag vocabulary for bookmark extracts (option B).

Built dynamically from the tags already used across the repo's curated content
(docs/canonical, docs/analysis, system-of-record) — so tech/finance bookmarks
connect to the existing Obsidian graph — unioned with a bookmarks-specific seed
for the operator's reading interests that are not repo domains on their own.

The seed themes are registered in the system-of-record (Rule 16.4) so they are
documented topics, not free-floating tags.
"""
from __future__ import annotations

import re
from pathlib import Path

# Reading-interest themes of the bookmarks corpus + a few tech themes so tech
# bookmarks link to the existing agent/eval notes. The dynamic part below brings
# in finance/econ tags (investimentos, macroeconomia, ...) already in the repo.
THEME_EXTENSION = [
    "performance",
    "ciclismo",
    "startups",
    "mercado-brasileiro",
    "agentic-coding",
    "agentes-orquestracao",
    "harness-engineering",
    "context-engineering",
    "evals",
    "production",
]

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
    """Union of curated tags + bookmarks theme extension, sorted and de-duplicated."""
    vocab: set[str] = set(THEME_EXTENSION)
    sources = [repo_root / "docs" / "system-of-record.md"]
    for sub in ("docs/canonical", "docs/analysis"):
        base = repo_root / sub
        if base.exists():
            sources.extend(base.rglob("*.md"))
    for path in sources:
        vocab |= _tags_in_file(path)
    return sorted(vocab)
