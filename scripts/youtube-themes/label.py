"""Deterministic theme labels from the tags/concepts of a community's members."""
from __future__ import annotations

import re
import unicodedata
from collections import Counter

from corpus import ExtractMeta


def _counter(members: list[str], extracts: dict[str, ExtractMeta], attr: str) -> Counter:
    c: Counter[str] = Counter()
    for vid in members:
        m = extracts.get(vid)
        if m:
            c.update(getattr(m, attr))
    return c


def auto_label(members: list[str], extracts: dict[str, ExtractMeta],
               *, n_tags: int = 3, n_concepts: int = 2) -> dict:
    """Return {'top_tags': [...], 'top_concepts': [...], 'label_auto': str}."""
    tags = [t for t, _ in _counter(members, extracts, "tags").most_common(n_tags)]
    concepts = [c for c, _ in _counter(members, extracts, "concepts").most_common(n_concepts)]
    label = ", ".join(tags) if tags else "tema"
    return {"top_tags": tags, "top_concepts": concepts, "label_auto": label}


def slug(text: str, max_len: int = 60) -> str:
    folded = unicodedata.normalize("NFKD", text or "").encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"[^a-zA-Z0-9]+", "-", folded).lower().strip("-")
    return s[:max_len].rstrip("-") or "tema"
