"""Parse digests/x/projects.md → the operator's projects with tiers.

Used to anchor the digest's actions in real projects, prioritizing by tier.
Format (see projects.md): `## Tier N` headings + `- **name** — line` entries,
plus a `## Teses / temas não-repo` section (no tier). Pure — no network/disk.
"""
from __future__ import annotations

import re

_TIER = re.compile(r"^##\s+Tier\s+(\d+)", re.I)
_THESES = re.compile(r"^##\s+Teses", re.I)
_ENTRY = re.compile(r"^-\s+\*\*(.+?)\*\*\s+—\s*(.*)$")


def parse_projects(text: str) -> list[dict]:
    """Return [{'name', 'tier' (int|None), 'desc'}], in file order."""
    out: list[dict] = []
    tier: int | None = None
    for line in text.splitlines():
        mt = _TIER.match(line)
        if mt:
            tier = int(mt.group(1))
            continue
        if _THESES.match(line):
            tier = None  # theses carry no tier
            continue
        me = _ENTRY.match(line.strip())
        if me:
            desc = re.sub(r"_\[refinar[^\]]*\]_", "", me.group(2)).strip()
            out.append({"name": me.group(1).strip(), "tier": tier, "desc": desc})
    return out


def projects_brief(projects: list[dict], *, max_items: int = 20) -> str:
    """Compact text of the projects (tier-ordered) for the GLM actions prompt."""
    ordered = sorted(projects, key=lambda p: (p["tier"] if p["tier"] is not None else 99))
    lines = []
    for p in ordered[:max_items]:
        t = f"tier {p['tier']}" if p["tier"] is not None else "tese"
        lines.append(f"- {p['name']} ({t}): {p['desc']}" if p["desc"] else f"- {p['name']} ({t})")
    return "\n".join(lines)
