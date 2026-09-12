"""Render a Map-of-Content (MOC) note for a theme."""
from __future__ import annotations

from corpus import ExtractMeta

EXTRACTS_REL = "extracts/youtube/ai-learning"


def build_moc(theme: dict, members: list[str], extracts: dict[str, ExtractMeta]) -> str:
    """A theme note: frontmatter + a wikilinked list of the theme's videos."""
    name = theme.get("label_llm") or theme["label_auto"]
    desc = theme.get("description", "")
    tags = theme.get("top_tags", [])

    lines = ["---"]
    lines.append(f'title: "Tema: {name}"')
    lines.append('type: "theme"')
    lines.append("source: youtube")
    lines.append(f"tags: {_json(tags)}")
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
    lines.append(f"## Vídeos ({len(members)})")
    # members sorted by title for a stable, readable list
    ordered = sorted((m for m in members if m in extracts), key=lambda m: extracts[m].title.lower())
    for vid in ordered:
        e = extracts[vid]
        stem = e.file[:-3] if e.file.endswith(".md") else e.file
        lines.append(f"- [[{EXTRACTS_REL}/{stem}|{e.title}]]")
    lines.append("")
    return "\n".join(lines)


def _json(value) -> str:
    import json
    return json.dumps(value, ensure_ascii=False)
