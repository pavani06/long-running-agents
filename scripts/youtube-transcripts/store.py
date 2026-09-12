"""Disk-backed corpus state: the repository is the source of truth.

The pipeline is stateless — it derives "what do we already have?" from the files
on disk plus missing.json, never from a separate seen-list. These helpers scan,
regenerate index.json/missing.json, and migrate legacy `<id>.txt` filenames to
the `<date>-<slug>--<id>.txt` scheme.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from naming import build_filename, parse_video_id

PLAYLIST_URL = "https://www.youtube.com/playlist?list=PLdJYvRCSB6rO2Mm_0wGnHgFfoy34OaC0S"
SOURCE = "enumeration: YouTube Data API v3; transcript: SerpApi youtube_video_transcript"


def watch_url(video_id: str) -> str:
    return f"https://www.youtube.com/watch?v={video_id}"


@dataclass
class Corpus:
    data_dir: Path

    @property
    def transcripts_dir(self) -> Path:
        return self.data_dir / "transcripts"

    @property
    def index_path(self) -> Path:
        return self.data_dir / "index.json"

    @property
    def missing_path(self) -> Path:
        return self.data_dir / "missing.json"

    # ── reads ────────────────────────────────────────────────────────────
    def scan_disk(self) -> dict[str, str]:
        """Map video_id -> filename for every transcript on disk."""
        out: dict[str, str] = {}
        if not self.transcripts_dir.exists():
            return out
        for path in self.transcripts_dir.glob("*.txt"):
            vid = parse_video_id(path.name)
            if vid:
                out[vid] = path.name
        return out

    def load_missing(self) -> dict[str, str]:
        """Map video_id -> reason for videos previously found to have no captions."""
        if not self.missing_path.exists():
            return {}
        data = json.loads(self.missing_path.read_text(encoding="utf-8"))
        return {v["id"]: v.get("reason", "sem transcript") for v in data.get("videos", [])}

    def known_ids(self) -> set[str]:
        """Everything the daily diff should NOT refetch: on-disk + known-missing."""
        return set(self.scan_disk()) | set(self.load_missing())

    # ── writes ───────────────────────────────────────────────────────────
    def add_transcript(self, extraction_date: str, video_id: str, title: str, text: str) -> str:
        """Write a transcript file under the naming scheme; return its filename."""
        self.transcripts_dir.mkdir(parents=True, exist_ok=True)
        fname = build_filename(extraction_date, title, video_id)
        (self.transcripts_dir / fname).write_text(text, encoding="utf-8")
        return fname

    def rename_legacy(self, id_to_title: dict[str, str], extraction_date: str) -> list[tuple[str, str]]:
        """Rename `<id>.txt` files to `<date>-<slug>--<id>.txt`. Returns [(old,new)]."""
        renamed: list[tuple[str, str]] = []
        for vid, fname in self.scan_disk().items():
            if "--" in fname:
                continue  # already migrated
            title = id_to_title.get(vid, "")
            new_name = build_filename(extraction_date, title, vid)
            if new_name == fname:
                continue
            (self.transcripts_dir / fname).rename(self.transcripts_dir / new_name)
            renamed.append((fname, new_name))
        return renamed

    def regenerate_index(self, prior_meta: dict[str, dict] | None = None) -> int:
        """Rewrite index.json from disk, preserving prior lang/segments where known.

        `prior_meta` maps video_id -> extra fields (lang, segments) to carry over.
        Returns the number of transcripts indexed.
        """
        prior_meta = prior_meta or self._load_prior_meta()
        videos = []
        for vid, fname in sorted(self.scan_disk().items(), key=lambda kv: kv[1]):
            text = (self.transcripts_dir / fname).read_text(encoding="utf-8")
            entry = {"id": vid, "url": watch_url(vid), "file": fname, "chars": len(text)}
            extra = prior_meta.get(vid, {})
            for k in ("lang", "segments"):
                if k in extra:
                    entry[k] = extra[k]
            videos.append(entry)
        self.index_path.write_text(
            json.dumps(
                {"playlist_url": PLAYLIST_URL, "source": SOURCE, "count": len(videos), "videos": videos},
                ensure_ascii=False, indent=2,
            ) + "\n",
            encoding="utf-8",
        )
        return len(videos)

    def write_missing(self, missing: dict[str, str]) -> None:
        videos = [
            {"id": vid, "reason": reason, "url": watch_url(vid)}
            for vid, reason in sorted(missing.items())
        ]
        self.missing_path.write_text(
            json.dumps({"count": len(videos), "videos": videos}, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    def _load_prior_meta(self) -> dict[str, dict]:
        if not self.index_path.exists():
            return {}
        data = json.loads(self.index_path.read_text(encoding="utf-8"))
        return {
            v["id"]: {k: v[k] for k in ("lang", "segments") if k in v}
            for v in data.get("videos", [])
        }
