"""Load the digest inputs from committed artifacts: extracts + themes + connections.

Never re-embeds/re-extracts — reads extract frontmatter, themes.json and
connections.json. Extract frontmatter is our controlled `key: <json>` format.
YouTube variant: keyed by video_id, ranked by deep_dive tier.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

EXTRACTS_REL = "extracts/youtube/ai-learning"


@dataclass
class Extract:
    video_id: str
    title: str
    file: str
    channel: str = ""
    url: str = ""
    topic: str = ""
    summary: str = ""
    key_points: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    entities: list[str] = field(default_factory=list)
    revisit: str = "low"          # deep_dive tier (high|medium|low)
    grounded_in: str = "video"
    thin: bool = False            # kept for parity; youtube extracts are never thin
    theme: str = ""
    links: list[str] = field(default_factory=list)
    created_at: str = ""          # video publish date if present (recency ranking)
    extracted: str = ""           # date the extract was written (daily scope)

    def stem(self) -> str:
        return self.file[:-3] if self.file.endswith(".md") else self.file


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


def load_extracts(extracts_dir: Path) -> dict[str, Extract]:
    out: dict[str, Extract] = {}
    for path in sorted(extracts_dir.glob("*.md")):
        if path.name == "README.md":
            continue
        fm = parse_frontmatter(path.read_text(encoding="utf-8"))
        vid = fm.get("video_id")
        if not vid:
            continue
        out[str(vid)] = Extract(
            video_id=str(vid), title=fm.get("title", ""), file=path.name,
            channel=fm.get("channel", ""), url=fm.get("url", ""),
            topic=fm.get("topic", ""), summary=fm.get("thesis", ""),
            key_points=[str(c) for c in fm.get("claims", []) if str(c).strip()],
            tags=[str(t) for t in fm.get("tags", []) if str(t).strip()],
            entities=[str(e) for e in fm.get("concepts", []) if str(e).strip()],
            revisit=fm.get("deep_dive", "low"),
            thin=bool(fm.get("thin", False)), theme=fm.get("theme", ""),
            links=[str(u) for u in fm.get("links", []) if str(u).strip()],
            created_at=fm.get("published_at", ""), extracted=fm.get("extracted", ""),
        )
    return out


def load_themes(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8")).get("themes", [])


def load_connection_neighbors(path: Path) -> dict[str, list[str]]:
    """video_id -> [neighbor video_id], from connections.json edges."""
    if not path.exists():
        return {}
    out: dict[str, list[str]] = {}
    for e in json.loads(path.read_text(encoding="utf-8")).get("edges", []):
        out.setdefault(e["a"], []).append(e["b"])
        out.setdefault(e["b"], []).append(e["a"])
    return out
