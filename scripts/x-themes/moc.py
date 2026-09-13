"""Render a Map-of-Content (MOC) note for a theme."""
from __future__ import annotations

import json

from corpus import ExtractMeta

EXTRACTS_REL = "extracts/x/bookmarks"


def build_moc(theme: dict, members: list[str], extracts: dict[str, ExtractMeta]) -> str:
    """A theme note: frontmatter + a wikilinked list of the theme's bookmarks."""
    name = theme.get("label_llm") or theme["label_auto"]
    desc = theme.get("description", "")
    tags = theme.get("top_tags", [])

    lines = ["---"]
    lines.append(f'title: "Tema: {name}"')
    lines.append('type: "theme"')
    lines.append("source: x")
    lines.append(f"tags: {json.dumps(tags, ensure_ascii=False)}")
    lines.append(f"size: {len(members)}")
    lines.append("---")
    lines.append("")
    lines.append(f"# Tema: {name}")
    lines.append("")
    if desc:
        lines.append(f"_{desc}_")
        lines.append("")
    if tags:
        lines.append(f"**Tags dominantes:** {', '.join(tags)}")
        lines.append("")
    lines.append(f"## Bookmarks ({len(members)})")
    ordered = sorted((m for m in members if m in extracts), key=lambda m: extracts[m].title.lower())
    for sid in ordered:
        e = extracts[sid]
        stem = e.file[:-3] if e.file.endswith(".md") else e.file
        lines.append(f"- [[{EXTRACTS_REL}/{stem}|{e.title}]]")
    lines.append("")
    return "\n".join(lines)
