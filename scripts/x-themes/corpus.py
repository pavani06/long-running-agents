"""Read inputs for the themes layer: connections.json + extract frontmatter.

Derives everything from committed artifacts — never re-embeds. Extract
frontmatter is our own controlled format (each `key: <json>` line), so
line-based parsing with json.loads is exact.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

EXTRACTS_DIR_REL = "extracts/x/bookmarks"


@dataclass
class ExtractMeta:
    status_id: str
    title: str
    file: str
    tags: list[str] = field(default_factory=list)
    key_points: list[str] = field(default_factory=list)
    summary: str = ""
    thin: bool = False


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
    """status_id -> ExtractMeta for every extract note."""
    out: dict[str, ExtractMeta] = {}
    for path in sorted(extracts_dir.glob("*.md")):
        if path.name == "README.md":
            continue
        fm = parse_frontmatter(path.read_text(encoding="utf-8"))
        sid = fm.get("status_id")
        if not sid:
            continue
        out[str(sid)] = ExtractMeta(
            status_id=str(sid),
            title=fm.get("title", ""),
            file=path.name,
            tags=[str(t) for t in fm.get("tags", []) if str(t).strip()],
            key_points=[str(c) for c in fm.get("key_points", []) if str(c).strip()],
            summary=fm.get("summary", ""),
            thin=bool(fm.get("thin", False)),
        )
    return out


def load_edges(connections_path: Path) -> list[tuple[str, str, float]]:
    """(a, b, weight) tuples from connections.json."""
    data = json.loads(connections_path.read_text(encoding="utf-8"))
    return [(e["a"], e["b"], float(e.get("weight", 1.0))) for e in data.get("edges", [])]
