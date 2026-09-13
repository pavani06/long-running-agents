"""Stateless queue: which `deep_dive: high` sources still need an analysis package.

The diff is `extracts with deep_dive == "high"` minus `extracts already carrying
an analyzed: marker`. Stateless: the extract frontmatter is the source of truth,
so re-running is idempotent and resumable (mirrors the transcripts−extracts diff
in `scripts/youtube-extracts/store.py`). Seeding the historical packages onto
existing extracts is a later step (Etapa 8), not this one.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from frontmatter import parse_frontmatter


@dataclass(frozen=True)
class Pending:
    file: str       # basename under the extracts dir
    video_id: str
    title: str


def is_pending(fm: dict) -> bool:
    """A source is pending when it is high-tier triage and not yet analyzed."""
    return fm.get("deep_dive") == "high" and not fm.get("analyzed")


def pending_from_texts(items: list[tuple[str, str]]) -> list[Pending]:
    """(filename, text) -> the pending subset, sorted by filename for stable order."""
    out: list[Pending] = []
    for filename, text in items:
        fm = parse_frontmatter(text)
        if is_pending(fm):
            out.append(Pending(
                file=filename,
                video_id=str(fm.get("video_id", "")),
                title=str(fm.get("title", "")),
            ))
    return sorted(out, key=lambda p: p.file)


def scan_pending(extracts_dir: Path) -> list[Pending]:
    """Scan an extracts directory on disk for pending sources."""
    items: list[tuple[str, str]] = []
    if not extracts_dir.exists():
        return []
    for path in sorted(extracts_dir.glob("*.md")):
        if path.name == "README.md":
            continue
        items.append((path.name, path.read_text(encoding="utf-8")))
    return pending_from_texts(items)
