"""Render a GLM extract + video metadata into a Markdown note.

Frontmatter carries the machine-readable structure (JSON is valid YAML flow, so
each value is serialized with json.dumps — correct quoting/escaping for free);
the body is the human-readable rendering for Obsidian. Both come from one call.
"""
from __future__ import annotations

import json
from dataclasses import dataclass


@dataclass(frozen=True)
class VideoMeta:
    title: str
    video_id: str
    url: str
    channel: str
    transcript_file: str  # basename under raw/.../transcripts/
    extracted: str        # YYYY-MM-DD


def _as_str_list(value) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(x).strip() for x in value if str(x).strip()]


def normalize_extract(extract: dict, allowed_tags: list[str]) -> dict:
    """Coerce list fields to clean string lists and drop off-vocabulary tags."""
    allowed = set(allowed_tags)
    tags = [t for t in _as_str_list(extract.get("tags")) if t in allowed]
    return {
        "thesis": str(extract.get("thesis", "")).strip(),
        "concepts": _as_str_list(extract.get("concepts")),
        "tools": _as_str_list(extract.get("tools")),
        "people": _as_str_list(extract.get("people")),
        "claims": _as_str_list(extract.get("claims")),
        "tags": tags,
        "deep_dive": extract.get("deep_dive", "low"),
        "deep_dive_reason": str(extract.get("deep_dive_reason", "")).strip(),
    }


def _fm(key: str, value) -> str:
    return f"{key}: {json.dumps(value, ensure_ascii=False)}"


def build_note(meta: VideoMeta, extract: dict, allowed_tags: list[str], version: int, model: str) -> str:
    e = normalize_extract(extract, allowed_tags)
    transcript_link = f"raw/youtube/ai-learning/transcripts/{meta.transcript_file}"

    lines = ["---"]
    lines += [
        _fm("title", meta.title),
        _fm("type", "extract"),
        _fm("source", "youtube"),
        _fm("video_id", meta.video_id),
        _fm("url", meta.url),
        _fm("channel", meta.channel),
        _fm("extracted", meta.extracted),
        _fm("model", model),
        _fm("extract_version", version),
        f'transcript: "[[{transcript_link}]]"',
        _fm("tags", e["tags"]),
        _fm("thesis", e["thesis"]),
        _fm("concepts", e["concepts"]),
        _fm("tools", e["tools"]),
        _fm("people", e["people"]),
        _fm("claims", e["claims"]),
        _fm("deep_dive", e["deep_dive"]),
        _fm("deep_dive_reason", e["deep_dive_reason"]),
    ]
    lines.append("---")
    lines.append("")
    lines.append(f"# {meta.title}")
    lines.append("")
    lines.append("## Tese")
    lines.append(e["thesis"] or "_(sem tese extraída)_")
    lines.append("")
    lines.append("## Conceitos-chave")
    lines += ([f"- {c}" for c in e["concepts"]] or ["_(nenhum)_"])
    lines.append("")
    lines.append("## Ferramentas & pessoas")
    lines.append(f"**Ferramentas:** {', '.join(e['tools']) if e['tools'] else '—'}")
    lines.append("")
    lines.append(f"**Pessoas/orgs:** {', '.join(e['people']) if e['people'] else '—'}")
    lines.append("")
    lines.append("## Claims acionáveis")
    lines += ([f"- {c}" for c in e["claims"]] or ["_(nenhum)_"])
    lines.append("")
    lines.append(f"> **Deep dive:** `{e['deep_dive']}` — {e['deep_dive_reason'] or '—'}")
    lines.append("")
    return "\n".join(lines)
