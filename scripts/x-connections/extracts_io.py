"""Read the bookmark extract corpus and build the text that gets embedded.

Extract frontmatter is our own controlled format: a block between the first two
`---` lines, each entry `key: <json-value>` (build_note serialized values with
json.dumps, so each value parses back with json.loads). Line-based parsing is
therefore exact for these files — no YAML dependency.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Extract:
    status_id: str
    title: str
    file: str  # basename under extracts/x/bookmarks/
    topic: str = ""
    summary: str = ""
    key_points: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)


def parse_frontmatter(text: str) -> dict:
    """Parse the `---` frontmatter block into a dict (values via json.loads)."""
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


def load_extract(path: Path) -> Extract | None:
    fm = parse_frontmatter(path.read_text(encoding="utf-8"))
    sid = fm.get("status_id")
    if not sid:
        return None
    return Extract(
        status_id=str(sid),
        title=fm.get("title", ""),
        file=path.name,
        topic=fm.get("topic", ""),
        summary=fm.get("summary", ""),
        key_points=[str(c) for c in fm.get("key_points", []) if str(c).strip()],
        tags=[str(t) for t in fm.get("tags", []) if str(t).strip()],
    )


def load_all(extracts_dir: Path) -> list[Extract]:
    out = []
    for path in sorted(extracts_dir.glob("*.md")):
        if path.name == "README.md":
            continue
        e = load_extract(path)
        if e:
            out.append(e)
    return out


def embed_text(e: Extract) -> str:
    """Meaning-dense text for embedding: topic + summary + key_points + tags."""
    parts = [e.topic or e.title, e.summary]
    if e.key_points:
        parts.append("Pontos: " + " ".join(e.key_points))
    if e.tags:
        parts.append("Tags: " + ", ".join(e.tags))
    return "\n\n".join(p for p in parts if p).strip()
