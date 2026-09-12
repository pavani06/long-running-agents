"""Render a GLM extract + bookmark metadata into a Markdown note.

Frontmatter carries the machine-readable structure (JSON is valid YAML flow, so
each value is json.dumps'd for correct quoting); the body is the human-readable
Obsidian rendering. Judgment fields come from the model; links/media are the
factual values carried from the raw item.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field

from glm import CONTENT_TYPES


@dataclass(frozen=True)
class BookmarkMeta:
    status_id: str
    handle: str
    url: str
    created_at: str
    item_file: str            # basename under raw/x/bookmarks/items/
    extracted: str            # YYYY-MM-DD
    links: list[str] = field(default_factory=list)
    media: list[str] = field(default_factory=list)


def _as_str_list(value) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(x).strip() for x in value if str(x).strip()]


def normalize_extract(extract: dict, allowed_tags: list[str]) -> dict:
    """Coerce fields; drop off-vocabulary tags; validate content_type/revisit."""
    allowed = set(allowed_tags)
    tags = [t for t in _as_str_list(extract.get("tags")) if t in allowed]
    ctype = extract.get("content_type")
    if ctype not in CONTENT_TYPES:
        ctype = "other"
    revisit = extract.get("revisit")
    if revisit not in ("high", "medium", "low"):
        revisit = "low"
    return {
        "topic": str(extract.get("topic", "")).strip(),
        "summary": str(extract.get("summary", "")).strip(),
        "tags": tags,
        "entities": _as_str_list(extract.get("entities")),
        "content_type": ctype,
        "revisit": revisit,
    }


def _fm(key: str, value) -> str:
    return f"{key}: {json.dumps(value, ensure_ascii=False)}"


def build_note(meta: BookmarkMeta, extract: dict, allowed_tags: list[str],
               version: int, model: str) -> str:
    e = normalize_extract(extract, allowed_tags)
    item_link = f"raw/x/bookmarks/items/{meta.item_file}"
    title = e["topic"] or f"@{meta.handle} bookmark {meta.status_id}"

    lines = ["---"]
    lines += [
        _fm("title", title),
        _fm("type", "extract"),
        _fm("source", "x"),
        _fm("status_id", meta.status_id),
        _fm("handle", meta.handle),
        _fm("url", meta.url),
        _fm("created_at", meta.created_at),
        _fm("extracted", meta.extracted),
        _fm("model", model),
        _fm("extract_version", version),
        f'item: "[[{item_link}]]"',
        _fm("tags", e["tags"]),
        _fm("topic", e["topic"]),
        _fm("summary", e["summary"]),
        _fm("entities", e["entities"]),
        _fm("content_type", e["content_type"]),
        _fm("revisit", e["revisit"]),
        _fm("links", meta.links),
        _fm("media", meta.media),
    ]
    lines.append("---")
    lines.append("")
    lines.append(f"# {title}")
    lines.append("")
    lines.append(f"**@{meta.handle}** · [{meta.status_id}]({meta.url}) · `{e['content_type']}`")
    lines.append("")
    lines.append("## Resumo")
    lines.append(e["summary"] or "_(sem resumo extraído)_")
    lines.append("")
    if meta.links:
        lines.append("## Links")
        lines += [f"- {u}" for u in meta.links]
        lines.append("")
    lines.append("## Entidades")
    lines.append(", ".join(e["entities"]) if e["entities"] else "—")
    lines.append("")
    lines.append(f"> **Revisit:** `{e['revisit']}`")
    lines.append("")
    return "\n".join(lines)
