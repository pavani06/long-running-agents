"""Assemble the digest Markdown from ranked items, per-theme synthesis, and the
thin bucket. Pure — takes already-computed data (incl. GLM synthesis) and emits
Obsidian-friendly Markdown with UTF-8 accents.
"""
from __future__ import annotations

from corpus import EXTRACTS_REL, Extract


def _est(e: Extract) -> str:
    return "~vídeo longo" if e.grounded_in == "video" else "~1 min"


def _first_sentence(text: str) -> str:
    text = (text or "").strip()
    for sep in (". ", "! ", "? "):
        i = text.find(sep)
        if 0 < i < 180:
            return text[: i + 1]
    return text[:180]


def _chip(e: Extract) -> str:
    return f"[[{EXTRACTS_REL}/{e.stem()}|{e.title}]]"


def material_for(members: list[Extract]) -> str:
    """Meaning-dense text of a theme's members for the GLM synthesis prompt."""
    blocks = []
    for e in members:
        pts = (" | claims: " + " ; ".join(e.key_points[:4])) if e.key_points else ""
        blocks.append(f"- {e.title} ({e.channel}): {e.summary}{pts}")
    return "\n".join(blocks)


def render_read_order(order: list[Extract]) -> list[str]:
    if not order:
        return []
    out = ["## Assista nesta ordem", ""]
    for i, e in enumerate(order, 1):
        why = _first_sentence(e.summary) or e.topic or e.title
        out.append(f"{i}. [{e.title}]({e.url}) — {e.channel} · `{e.revisit}` · {_est(e)}")
        out.append(f"   {why}")
    out.append("")
    return out


def render_theme(name: str, synth: dict | None, members: list[Extract],
                 chips: list[Extract]) -> list[str]:
    out = [f"## {name}  ({len(members)})", ""]
    if synth and synth.get("synthesis"):
        out += [synth["synthesis"], ""]
    else:  # deterministic fallback
        out += ["**Itens:**", ""] + [f"- {e.summary or e.title}" for e in members[:5]] + [""]
    if synth and synth.get("non_obvious"):
        out += [f"> **Não-óbvio:** {synth['non_obvious']}", ""]
    out.append("**Vídeos:**")
    for e in sorted(members, key=lambda x: x.title.lower()):
        out.append(f"- [{e.title}]({e.url}) — {e.channel}")
    out.append("")
    if chips:
        out.append("**Conecta com:** " + " · ".join(_chip(c) for c in chips))
        out.append("")
    if synth and synth.get("actions"):
        out.append("**Ações:**")
        out += [f"- {a}" for a in synth["actions"]]
        out.append("")
    return out


def render_thin(thin: list[Extract]) -> list[str]:
    if not thin:
        return []
    out = [f"## A investigar ({len(thin)})", ""]
    for e in sorted(thin, key=lambda x: x.channel.lower()):
        out.append(f"- [{e.topic or e.title}]({e.url}) — {e.channel}")
    out.append("")
    return out


def build_digest(*, date: str, mode: str, order: list[Extract],
                 theme_blocks: list[dict], thin: list[Extract], total: int) -> str:
    """theme_blocks: [{'name', 'synth'(dict|None), 'members'[Extract], 'chips'[Extract]}]."""
    header = "Digest de vídeos do YouTube" + (" — bootstrap do acervo" if mode == "bootstrap" else f" — {date}")
    lines = ["---", f'title: "{header}"', 'type: "digest"', "source: youtube",
             f"date: {date}", f"mode: {mode}", f"items: {total}", "---", "",
             f"# {header}", ""]

    themed = sum(len(b["members"]) for b in theme_blocks)
    lines.append(f"**{total} vídeos** · {len(theme_blocks)} temas · "
                 f"{themed} em temas · {len(thin)} a investigar")
    lines.append("")

    if total == 0:
        lines += ["_Nenhum vídeo novo neste período._", ""]
        return "\n".join(lines)

    lines += render_read_order(order)
    for b in theme_blocks:
        lines += render_theme(b["name"], b.get("synth"), b["members"], b.get("chips", []))
    lines += render_thin(thin)
    return "\n".join(lines).rstrip() + "\n"
