"""Read/write extract frontmatter for the analyze-and-improve control plane.

Extract frontmatter is the repo's controlled `key: <json-value>` block — the
same line-based format the youtube-connections layer parses (see
`scripts/youtube-connections/extracts_io.py`). Values are `json.loads`-able, so
parsing needs no YAML dependency and runs under the pipeline's minimal
(requests-only) environment.

The `analyzed:` marker is the pipeline's stateless cursor: once a `deep_dive`
source has produced an analysis package, its extract carries
`analyzed: "docs/analysis/<slug>/"`. It is written back surgically — touching
only that one line, leaving every other byte unchanged (mirrors
`frontmatter_io.set_relates_to`).
"""
from __future__ import annotations

import json
from pathlib import Path


def parse_frontmatter(text: str) -> dict:
    """Parse the leading `---` block into a dict (each value via json.loads)."""
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    block = text[3:end].strip("\n")
    out: dict = {}
    for line in block.splitlines():
        key, sep, value = line.partition(": ")
        if not sep:
            continue
        try:
            out[key.strip()] = json.loads(value)
        except json.JSONDecodeError:
            out[key.strip()] = value.strip()
    return out


def read_analyzed(text: str) -> str | None:
    """The `analyzed:` marker's value, or None when the source is still pending."""
    value = parse_frontmatter(text).get("analyzed")
    return value if isinstance(value, str) and value else None


def set_analyzed(text: str, target: str) -> str:
    """Return `text` with a single `analyzed:` line set in the frontmatter.

    Inserts it (or replaces an existing one) just before the closing `---`.
    Text without a frontmatter block is returned unchanged.
    """
    if not text.startswith("---\n"):
        return text
    end = text.find("\n---", 3)
    if end == -1:
        return text
    head = text[: end + 1]   # up to the newline before the closing ---
    rest = text[end + 1:]    # the closing '---' and body

    lines = [ln for ln in head.split("\n") if not ln.startswith("analyzed:")]
    while lines and lines[-1] == "":
        lines.pop()
    lines.append("analyzed: " + json.dumps(target, ensure_ascii=False))
    return "\n".join(lines) + "\n" + rest


def mark_analyzed(path: Path, target: str) -> bool:
    """Write the `analyzed:` marker back to the extract; True if it changed."""
    original = path.read_text(encoding="utf-8")
    updated = set_analyzed(original, target)
    if updated != original:
        path.write_text(updated, encoding="utf-8")
    return updated != original
