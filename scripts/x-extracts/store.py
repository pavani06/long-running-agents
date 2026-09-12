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
