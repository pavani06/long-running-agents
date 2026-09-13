"""Hybrid retrieval for Fase 3: dense top-k over the Etapa-0 index + grep.

The classifier's worst failure is calling Missing something that already exists
under another name → duplication. Dense retrieval covers the conceptual axis
where grep fails; grep pins exact identifiers (filenames, ADR numbers, symbols).

Pure parts (unit-tested): `rank_sections` (cosine ranking over the stored
vectors) and `build_context` (prompt assembly from dense hits + grep hits). The
query embedding (network) and file/grep reads (I/O) live in thin wrappers.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

from floor import cosine
from index_store import records_for


def rank_sections(query_vec: list[float], index: dict, *, k: int = 8,
                  floor: float | None = None) -> list[dict]:
    """Top-k index sections by cosine to `query_vec`. Pure.

    Records without a stored vector are skipped; `floor` drops weak matches.
    Returns [{id, path, heading, score}] sorted by score desc.
    """
    scored: list[dict] = []
    for rid, rec in index.get("records", {}).items():
        vec = rec.get("vector")
        if not isinstance(vec, list) or not vec:
            continue
        s = cosine(query_vec, vec)
        if floor is not None and s < floor:
            continue
        scored.append({"id": rid, "path": rec.get("path"),
                       "heading": rec.get("heading"), "score": s})
    scored.sort(key=lambda d: d["score"], reverse=True)
    return scored[:k]


def fetch_texts(ranked: list[dict], repo_root: Path) -> list[dict]:
    """Attach each ranked section's text by re-chunking its file (I/O)."""
    by_path: dict[str, list[dict]] = {}
    for r in ranked:
        by_path.setdefault(r["path"], []).append(r)
    for path, items in by_path.items():
        fp = repo_root / path
        if not fp.exists():
            continue
        texts = {rec.id: rec.text for rec in records_for(path, fp.read_text(encoding="utf-8"))}
        for it in items:
            it["text"] = texts.get(it["id"], "")
    return ranked


def grep_identifiers(identifiers: list[str], repo_root: Path, *, max_hits: int = 5) -> list[dict]:
    """`git grep -Fn` each identifier (I/O). Returns [{identifier, path, line, content}]."""
    hits: list[dict] = []
    for ident in identifiers:
        if not ident.strip():
            continue
        out = subprocess.run(
            ["git", "-C", str(repo_root), "grep", "-n", "--no-color", "-F", ident],
            capture_output=True, text=True,
        ).stdout
        for line in out.splitlines()[:max_hits]:
            path, sep, rest = line.partition(":")
            lineno, sep2, content = rest.partition(":")
            if sep and sep2 and lineno.isdigit():
                hits.append({"identifier": ident, "path": path,
                             "line": int(lineno), "content": content})
    return hits


def build_context(dense_sections: list[dict], grep_hits: list[dict]) -> str:
    """Format retrieved evidence for the classifier prompt. Pure."""
    parts = ["## Seções relevantes (dense retrieval)"]
    if dense_sections:
        for s in dense_sections:
            head = s.get("heading") or "(preamble)"
            parts.append(f"### {s.get('path')} :: {head}  (score {s.get('score', 0):.3f})\n"
                         + (s.get("text", "") or "").strip())
    else:
        parts.append("_(nenhuma)_")
    parts.append("\n## Ocorrências exatas (grep)")
    if grep_hits:
        for h in grep_hits:
            parts.append(f"- {h['path']}:{h['line']} — `{h['identifier']}` — {h['content'].strip()}")
    else:
        parts.append("_(nenhuma)_")
    return "\n\n".join(parts)


def make_pattern_retriever(patterns: list[dict], index: dict, openai_key: str,
                           repo_root: Path, *, k: int = 8, embed_fn=None):
    """A `retriever(need_more)->context` closure for Fase 3, shared by the CLI and
    the spine runner. need_more=None → dense top-k for the patterns' text + grep of
    the pattern names; otherwise grep the model-named identifiers + append the named
    files. `embed_fn` is injectable (defaults to the OpenAI embeddings client)."""
    if embed_fn is None:
        from embed import embed_texts as embed_fn

    def _dense(query_text: str) -> list[dict]:
        qvec = embed_fn([query_text], openai_key)[0]
        return fetch_texts(rank_sections(qvec, index, k=k), repo_root)

    def retriever(need_more):
        if need_more is None:
            query = "\n".join(f"{p.get('name','')} {p.get('problem','')} {p.get('mechanism','')}"
                              for p in patterns)
            grep = grep_identifiers([p.get("name", "") for p in patterns], repo_root)
            return build_context(_dense(query), grep)
        grep = grep_identifiers(need_more.get("greps", []), repo_root)
        extra = []
        for rel in need_more.get("files", []):
            fp = repo_root / rel
            if fp.exists():
                extra.append({"path": rel, "heading": "(arquivo pedido)", "score": 0.0,
                              "text": fp.read_text(encoding="utf-8")[:4000]})
        return build_context(extra, grep)

    return retriever
