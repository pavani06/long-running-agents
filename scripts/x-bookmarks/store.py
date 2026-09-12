"""Disk-backed corpus state for X bookmarks: the repository is the source of truth.

Stateless — "what do we already have?" comes from the files on disk, never from
a separate seen-list. `new_ids()` is the bookmarks the API returned minus what is
already under items/, keyed by status id parsed from filenames.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path

from naming import build_filename, parse_status_id

SOURCE = "X API v2 GET /2/users/:id/bookmarks (OAuth2 user-context)"


@dataclass(frozen=True)
class Bookmark:
    status_id: str
    handle: str
    text: str
    created_at: str          # tweet creation time (ISO), from the API
    url: str                 # https://x.com/<handle>/status/<status_id>


@dataclass
class BookmarkStore:
    repo_root: Path

    @property
    def data_dir(self) -> Path:
        return self.repo_root / "raw" / "x" / "bookmarks"

    @property
    def items_dir(self) -> Path:
        return self.data_dir / "items"

    @property
    def index_path(self) -> Path:
        return self.data_dir / "index.json"

    # ── reads ────────────────────────────────────────────────────────────
    def scan_disk(self) -> dict[str, str]:
        """Map status_id -> filename for every bookmark item on disk."""
        out: dict[str, str] = {}
        if not self.items_dir.exists():
            return out
        for path in self.items_dir.glob("*.json"):
            sid = parse_status_id(path.name)
            if sid:
                out[sid] = path.name
        return out

    def new_bookmarks(self, fetched: list[Bookmark]) -> list[Bookmark]:
        """The fetched bookmarks whose status id is not yet on disk, dedup'd."""
        known = set(self.scan_disk())
        seen: set[str] = set()
        out: list[Bookmark] = []
        for b in fetched:
            if b.status_id in known or b.status_id in seen:
                continue
            seen.add(b.status_id)
            out.append(b)
        return out

    # ── writes ───────────────────────────────────────────────────────────
    def write_item(self, collection_date: str, bookmark: Bookmark) -> str:
        """Write one bookmark as JSON under the naming scheme; return filename."""
        self.items_dir.mkdir(parents=True, exist_ok=True)
        fname = build_filename(collection_date, bookmark.handle, bookmark.text, bookmark.status_id)
        payload = {"collected": collection_date, **asdict(bookmark)}
        (self.items_dir / fname).write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return fname

    def regenerate_index(self) -> int:
        """Rewrite index.json from disk. Returns the number of items indexed."""
        items = []
        for sid, fname in sorted(self.scan_disk().items(), key=lambda kv: kv[1]):
            data = json.loads((self.items_dir / fname).read_text(encoding="utf-8"))
            items.append({
                "status_id": sid,
                "handle": data.get("handle", ""),
                "url": data.get("url", ""),
                "file": fname,
            })
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.index_path.write_text(
            json.dumps({"source": SOURCE, "count": len(items), "items": items},
                       ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8")
        return len(items)
