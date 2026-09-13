"""Disk-backed diff between the bookmark raw corpus and the extract corpus.

Stateless: the repo is the source of truth. "What still needs an extract?" is
`raw/x/bookmarks/items/` minus `extracts/x/bookmarks/`, keyed by status id.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from naming import extract_name_for, status_id_from


@dataclass
class ExtractStore:
    repo_root: Path

    @property
    def items_dir(self) -> Path:
        return self.repo_root / "raw" / "x" / "bookmarks" / "items"

    @property
    def extracts_dir(self) -> Path:
        return self.repo_root / "extracts" / "x" / "bookmarks"

    @property
    def ingest_dir(self) -> Path:
        return self.repo_root / "ingest" / "x"

    def ingest_index(self) -> dict[str, dict]:
        """Map url -> ingest entry ({file, status, ...}); empty if no ingest layer."""
        p = self.ingest_dir / "index.json"
        if not p.exists():
            return {}
        data = json.loads(p.read_text(encoding="utf-8"))
        return {it["url"]: it for it in data.get("items", []) if it.get("url")}

    def source_for(self, item: dict, index: dict[str, dict] | None = None) -> tuple[str, str]:
        """(grounded_in, source_text) for a bookmark, from the ingest layer.

        Returns ("article", <cleaned body>) using the first of the item's links
        whose ingested content is usable (status ok/paywall); else ("tweet", "").
        """
        index = self.ingest_index() if index is None else index
        for u in item.get("links", []) or []:
            entry = index.get(u.strip())
            if entry and entry.get("status") in ("ok", "paywall"):
                body = self._ingest_body(entry.get("file", ""))
                if body.strip():
                    return "article", body
        return "tweet", ""

    def _ingest_body(self, filename: str) -> str:
        path = self.ingest_dir / filename
        if not filename or not path.exists():
            return ""
        parts = path.read_text(encoding="utf-8").split("---", 2)
        return parts[2] if len(parts) >= 3 else ""

    def _scan(self, directory: Path, suffix: str) -> dict[str, str]:
        out: dict[str, str] = {}
        if not directory.exists():
            return out
        for path in directory.glob(f"*{suffix}"):
            sid = status_id_from(path.name)
            if sid:
                out[sid] = path.name
        return out

    def scan_items(self) -> dict[str, str]:
        return self._scan(self.items_dir, ".json")

    def scan_extracts(self) -> dict[str, str]:
        return self._scan(self.extracts_dir, ".md")

    def pending(self, *, rebuild: bool = False) -> list[tuple[str, str]]:
        """(status_id, item_filename) still needing an extract, sorted by name."""
        items = self.scan_items()
        done = set() if rebuild else set(self.scan_extracts())
        return sorted([(sid, fn) for sid, fn in items.items() if sid not in done],
                      key=lambda t: t[1])

    def read_item(self, filename: str) -> dict:
        return json.loads((self.items_dir / filename).read_text(encoding="utf-8"))

    def write_extract(self, item_filename: str, content: str) -> str:
        self.extracts_dir.mkdir(parents=True, exist_ok=True)
        name = extract_name_for(item_filename)
        (self.extracts_dir / name).write_text(content, encoding="utf-8")
        return name
