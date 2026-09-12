"""Read inputs for the themes layer: connections.json + extract frontmatter.

The themes layer derives everything from committed artifacts — it never
re-embeds. Extract frontmatter is our own controlled format (each `key: <json>`
line), so line-based parsing with json.loads is exact.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

EXTRACTS_DIR_REL = "extracts/youtube/ai-learning"


@dataclass
class ExtractMeta:
    video_id: str
    title: str
    file: str
    tags: list[str] = field(default_factory=list)
    concepts: list[str] = field(default_factory=list)
    thesis: str = ""


def parse_frontmatter(text: str) -> dict:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    out: dict = {}
    for line in text[3:end].strip("\n").splitlines():
        key, sep, value = line.partition(": ")
        if not sep:
            continue
        try:
            out[key.strip()] = json.loads(value)
        except json.JSONDecodeError:
            out[key.strip()] = value.strip()
    return out


def load_extracts(extracts_dir: Path) -> dict[str, ExtractMeta]:
    """video_id -> ExtractMeta for every extract note."""
    out: dict[str, ExtractMeta] = {}
    for path in sorted(extracts_dir.glob("*.md")):
        if path.name == "README.md":
            continue
        fm = parse_frontmatter(path.read_text(encoding="utf-8"))
        vid = fm.get("video_id")
        if not vid:
            continue
        out[vid] = ExtractMeta(
            video_id=vid,
            title=fm.get("title", ""),
            file=path.name,
            tags=[str(t) for t in fm.get("tags", []) if str(t).strip()],
            concepts=[str(c) for c in fm.get("concepts", []) if str(c).strip()],
            thesis=fm.get("thesis", ""),
        )
    return out


def load_edges(connections_path: Path) -> list[tuple[str, str, float]]:
    """(a, b, weight) tuples from connections.json."""
    data = json.loads(connections_path.read_text(encoding="utf-8"))
    return [(e["a"], e["b"], float(e.get("weight", 1.0))) for e in data.get("edges", [])]
