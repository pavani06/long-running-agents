"""Disk-backed diff between the transcript corpus and the extract corpus.

Stateless: the repo is the source of truth. "What still needs an extract?" is
`transcripts/` minus `extracts/`, keyed by video id parsed from filenames.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from naming import extract_name_for, video_id_from


@dataclass
class ExtractStore:
    repo_root: Path

    @property
    def transcripts_dir(self) -> Path:
        return self.repo_root / "raw" / "youtube" / "ai-learning" / "transcripts"

    @property
    def extracts_dir(self) -> Path:
        return self.repo_root / "extracts" / "youtube" / "ai-learning"

    def _scan(self, directory: Path, suffix: str) -> dict[str, str]:
        out: dict[str, str] = {}
        if not directory.exists():
            return out
        for path in directory.glob(f"*{suffix}"):
            vid = video_id_from(path.name)
            if vid:
                out[vid] = path.name
        return out

    def scan_transcripts(self) -> dict[str, str]:
        return self._scan(self.transcripts_dir, ".txt")

    def scan_extracts(self) -> dict[str, str]:
        return self._scan(self.extracts_dir, ".md")

    def pending(self, *, rebuild: bool = False) -> list[tuple[str, str]]:
        """(video_id, transcript_filename) still needing an extract.

        rebuild=True returns every transcript (re-extract all); otherwise only
        those without a corresponding extract on disk. Sorted by filename for
        stable, resumable ordering.
        """
        transcripts = self.scan_transcripts()
        done = set() if rebuild else set(self.scan_extracts())
        items = [(vid, fn) for vid, fn in transcripts.items() if vid not in done]
        return sorted(items, key=lambda t: t[1])

    def read_transcript(self, filename: str) -> str:
        return (self.transcripts_dir / filename).read_text(encoding="utf-8")

    def write_extract(self, transcript_filename: str, content: str) -> str:
        self.extracts_dir.mkdir(parents=True, exist_ok=True)
        name = extract_name_for(transcript_filename)
        (self.extracts_dir / name).write_text(content, encoding="utf-8")
        return name
