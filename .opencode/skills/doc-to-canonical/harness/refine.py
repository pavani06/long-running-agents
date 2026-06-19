"""Refinement session for doc-to-canonical pipeline.

Canonical docs follow a fixed template: Problem, Solution, Implementation,
Tradeoffs, Relationships, References. Refinement adjusts specific sections
without re-running knowledge extraction and pattern classification.
"""

from dataclasses import dataclass, field, asdict
import json
from pathlib import Path
from typing import Optional

CANONICAL_TYPES = frozenset({"canonical", "principle", "analysis", "evidence"})


@dataclass
class CanonicalEntry:
    entry_id: str
    canonical_type: str
    grounding_prompt: str
    current_text: str
    refinement_history: list[str] = field(default_factory=list)

    def __post_init__(self):
        if self.canonical_type not in CANONICAL_TYPES:
            raise ValueError(f"Invalid canonical_type: {self.canonical_type!r}")

    def add_refinement(self, instruction: str) -> None:
        self.refinement_history.append(instruction)

    def to_dict(self) -> dict:
        return {
            "entry_id": self.entry_id, "canonical_type": self.canonical_type,
            "grounding_prompt": self.grounding_prompt, "current_text": self.current_text,
            "refinement_history": self.refinement_history,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "CanonicalEntry":
        return cls(
            entry_id=d["entry_id"], canonical_type=d["canonical_type"],
            grounding_prompt=d["grounding_prompt"], current_text=d["current_text"],
            refinement_history=d.get("refinement_history", []),
        )


@dataclass
class CanonicalRefinementSession:
    source_slug: str
    entries: dict[str, CanonicalEntry] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {"source_slug": self.source_slug, "entries": {k: v.to_dict() for k, v in self.entries.items()}}

    @classmethod
    def from_dict(cls, d: dict) -> "CanonicalRefinementSession":
        entries = {k: CanonicalEntry.from_dict(v) for k, v in d.get("entries", {}).items()}
        return cls(source_slug=d["source_slug"], entries=entries)


def _safe_dir(output_dir: str) -> Path:
    out = Path(output_dir)
    if ".." in str(out):
        raise ValueError(f"Invalid output_dir: {output_dir!r}")
    return out


def save_session(session: CanonicalRefinementSession, output_dir: str) -> str:
    out = _safe_dir(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    fpath = out / "refine_session.json"
    fpath.write_text(json.dumps(session.to_dict(), indent=2, default=str))
    return str(fpath)


def load_session(output_dir: str) -> Optional[CanonicalRefinementSession]:
    sp = _safe_dir(output_dir) / "refine_session.json"
    if not sp.exists():
        return None
    return CanonicalRefinementSession.from_dict(json.loads(sp.read_text()))
