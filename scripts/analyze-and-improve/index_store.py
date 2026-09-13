"""The repo's semantic index: section records + incremental update logic.

A record is one embeddable section (from `chunking.split_sections`) plus a
content hash. The index is a plain dict, JSON-serialisable, cached under
`.runtime/` (derived state — the repo is the source of truth, so it is rebuilt,
never committed).

Incremental update has two layers, both here and both pure:
  1. the delta scan (deltascan.py) says which *files* changed;
  2. `select_to_embed` compares hashes so only the *chunks* that actually
     changed get re-embedded — "só nos chunks que o delta scan aponta".
Vectors are supplied by the caller (from embed.py), keeping this module free of
network I/O and fully unit-testable.
"""
from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass

from chunking import split_sections

INDEX_VERSION = 1


@dataclass(frozen=True)
class Record:
    id: str
    path: str
    heading: str
    level: int
    text: str
    hash: str


def _slug(heading: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", heading.lower()).strip("-") or "section"


def text_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def records_for(path: str, text: str) -> list[Record]:
    """Section records for one file. Ids are stable and unique within the file
    (a repeated heading gets an ordinal suffix)."""
    out: list[Record] = []
    seen: dict[tuple[int, str], int] = {}
    for section in split_sections(text):
        slug = _slug(section.heading) if section.heading else "preamble"
        key = (section.level, slug)
        n = seen.get(key, 0)
        seen[key] = n + 1
        rid = f"{path}#{section.level}-{slug}" + (f"-{n}" if n else "")
        out.append(Record(rid, path, section.heading, section.level,
                           section.text, text_hash(section.text)))
    return out


def select_to_embed(index: dict, records: list[Record]) -> list[Record]:
    """Records whose content hash is new or changed vs the current index."""
    stored = index.get("records", {})
    return [r for r in records if stored.get(r.id, {}).get("hash") != r.hash]


def merge_index(index: dict, changed_records_by_path: dict[str, list[Record]],
                deleted_paths, new_vectors: dict[str, list[float]]) -> dict:
    """Fold a delta into the index.

    - `changed_records_by_path`: current records for the files the scan flagged.
    - `deleted_paths`: files removed from the repo.
    - `new_vectors`: id -> vector, only for records that were re-embedded; a
      record kept from a previous run reuses its stored vector.
    Records of untouched files pass through unchanged.
    """
    touched = set(changed_records_by_path) | set(deleted_paths)
    stored = index.get("records", {})
    records = {rid: v for rid, v in stored.items() if v.get("path") not in touched}

    for path, recs in changed_records_by_path.items():
        for r in recs:
            prev = stored.get(r.id, {})
            vector = new_vectors.get(r.id, prev.get("vector"))
            records[r.id] = {
                "path": r.path, "heading": r.heading, "level": r.level,
                "hash": r.hash, "vector": vector,
            }
    return {**index, "version": INDEX_VERSION, "records": records}


def index_vectors(index: dict) -> list[list[float]]:
    """The stored vectors, for feeding floor.distribution."""
    return [v["vector"] for v in index.get("records", {}).values()
            if isinstance(v.get("vector"), list)]
