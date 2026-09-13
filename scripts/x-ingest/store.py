"""Disk-backed ingested-content corpus: the repository is the source of truth.

Keyed by URL (via url_key), so an article linked from two bookmarks is fetched
once. EVERY processed URL gets a file — including `failed`/`unsupported` (empty
body, status in frontmatter) — so the index is fully regenerable from disk and a
failure stays visible and retriable (never silence).
"""
from __future__ import annotations

import json
from pathlib import Path

from naming import content_name, key_from_name, url_key

SOURCE = "Jina Reader (r.jina.ai) + trafilatura fallback"


class IngestStore:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root

    @property
    def items_dir(self) -> Path:
        return self.repo_root / "raw" / "x" / "bookmarks" / "items"

    @property
    def ingest_dir(self) -> Path:
        return self.repo_root / "ingest" / "x"

    @property
    def index_path(self) -> Path:
        return self.ingest_dir / "index.json"

    # ── reads ────────────────────────────────────────────────────────────
    def collect_links(self) -> list[str]:
        """Unique external links across all raw bookmark items, stable order."""
        seen: set[str] = set()
        out: list[str] = []
        if not self.items_dir.exists():
            return out
        for path in sorted(self.items_dir.glob("*.json")):
            data = json.loads(path.read_text(encoding="utf-8"))
            for u in data.get("links", []) or []:
                if u not in seen:
                    seen.add(u)
                    out.append(u)
        return out

    def scan_disk(self) -> dict[str, str]:
        """Map url_key -> filename for every ingested content file."""
        out: dict[str, str] = {}
        if not self.ingest_dir.exists():
            return out
        for path in self.ingest_dir.glob("*.md"):
            k = key_from_name(path.name)
            if k:
                out[k] = path.name
        return out

    def _frontmatter(self, filename: str) -> dict:
        text = (self.ingest_dir / filename).read_text(encoding="utf-8")
        block = text.split("---", 2)
        if len(block) < 3:
            return {}
        fm: dict = {}
        for line in block[1].strip().splitlines():
            key, _, val = line.partition(": ")
            try:
                fm[key.strip()] = json.loads(val)
            except json.JSONDecodeError:
                fm[key.strip()] = val
        return fm

    def pending(self, links: list[str], *, mode: str) -> list[str]:
        """URLs to (re)fetch. incremental=missing; retry=missing+failed; full=all."""
        if mode == "full":
            return list(links)
        present = self.scan_disk()
        missing = [u for u in links if url_key(u) not in present]
        if mode == "retry":
            failed = [u for u in links
                      if url_key(u) in present
                      and self._frontmatter(present[url_key(u)]).get("status") == "failed"]
            return missing + failed
        return missing  # incremental

    # ── writes ───────────────────────────────────────────────────────────
    def write_entry(self, url: str, result: dict, fetched: str) -> str:
        """Write one ingested URL (content + provenance frontmatter). Returns filename."""
        self.ingest_dir.mkdir(parents=True, exist_ok=True)
        fname = content_name(url)
        fm = {
            "url": url,
            "key": url_key(url),
            "status": result.get("status", "failed"),
            "final_url": result.get("final_url", url),
            "method": result.get("method", ""),
            "content_hash": result.get("content_hash", ""),
            "text_len": result.get("text_len", 0),
            "fetched": fetched,
        }
        lines = ["---"]
        lines += [f"{k}: {json.dumps(v, ensure_ascii=False)}" for k, v in fm.items()]
        lines += ["---", "", result.get("text", "")]
        (self.ingest_dir / fname).write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
        return fname

    def regenerate_index(self) -> dict[str, int]:
        """Rewrite index.json from disk. Returns status counts."""
        entries = []
        counts: dict[str, int] = {}
        for k, fname in sorted(self.scan_disk().items(), key=lambda kv: kv[1]):
            fm = self._frontmatter(fname)
            counts[fm.get("status", "?")] = counts.get(fm.get("status", "?"), 0) + 1
            entries.append({"key": k, "file": fname, **{
                f: fm.get(f) for f in ("url", "status", "final_url", "method", "text_len")}})
        self.ingest_dir.mkdir(parents=True, exist_ok=True)
        self.index_path.write_text(
            json.dumps({"source": SOURCE, "count": len(entries), "status_counts": counts,
                        "items": entries}, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8")
        return counts
