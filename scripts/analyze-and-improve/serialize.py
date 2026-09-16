"""Render the Fase 0/1/2 outputs to the package's `.yaml` (typed mirror) and
`.md` (human-readable) forms. Pure and deterministic.

YAML uses PyYAML (the analyze-and-improve packages are real YAML, unlike the
json-value extract frontmatter); the workflow that runs this must install it.
"""
from __future__ import annotations

import yaml


def to_yaml(obj) -> str:
    """Deterministic YAML dump (block style, keys unsorted, unicode preserved)."""
    return yaml.safe_dump(obj, sort_keys=False, allow_unicode=True, default_flow_style=False)


def split_frontmatter(text: str) -> tuple[dict | None, str]:
    """Split a markdown document into (parsed frontmatter, body). Pure.

    Returns `(None, text)` when the document has no `---` block opening line 1 —
    the same shape the obsidian validator treats as "missing frontmatter"."""
    lines = (text or "").split("\n")
    if not lines or lines[0].strip() != "---":
        return None, text or ""
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            try:
                loaded = yaml.safe_load("\n".join(lines[1:i]))
            except yaml.YAMLError:
                return None, "\n".join(lines[i + 1:])
            return (loaded if isinstance(loaded, dict) else {}), "\n".join(lines[i + 1:])
    return None, text


def _bullets(items) -> str:
    return "\n".join(f"- {it}" for it in items) if items else "_(nenhum)_"


def mental_model_md(model: dict) -> str:
    meta = model.get("meta", {})
    lines = [f"# Mental Model: {meta.get('title', model.get('title', 'repo'))}", ""]
    if meta:
        lines += [f"> repo: {meta.get('repo', '')} · base_commit: {meta.get('base_commit', '')}"
                  + (f" · based_on: {meta['based_on']}" if meta.get("based_on") else ""), ""]
    lines += ["## Goals", _bullets(model.get("goals", [])), ""]
    arch = model.get("architecture", {}) or {}
    lines += ["## Architecture — abstractions",
              _bullets(f"**{a.get('name','')}** — {a.get('role','')}"
                       for a in arch.get("abstractions", [])), ""]
    lines += ["## Patterns",
              _bullets(f"**{p.get('name','')}** ({p.get('maturity','?')}) — {p.get('where_defined','')}"
                       for p in model.get("patterns", [])), ""]
    lines += ["## Gaps",
              _bullets(f"{g.get('what','')} — {g.get('where_documented','')}"
                       for g in model.get("gaps", [])), ""]
    return "\n".join(lines)


def extraction_md(extraction: dict) -> str:
    lines = ["# Analysis (Fase 1 — extração)", "",
             "## Tese", extraction.get("thesis", ""), "",
             "## Conceitos",
             _bullets(f"**{c.get('name','')}** — {c.get('summary','')}"
                      for c in extraction.get("concepts", [])), "",
             "## Claims",
             _bullets(f"{c.get('claim','')} — _evidência:_ {c.get('evidence','')}"
                      for c in extraction.get("claims", [])), ""]
    if extraction.get("tools"):
        lines += ["## Ferramentas", _bullets(extraction["tools"]), ""]
    if extraction.get("people"):
        lines += ["## Pessoas/Orgs", _bullets(extraction["people"]), ""]
    return "\n".join(lines)


def patterns_md(patterns: list[dict]) -> str:
    lines = ["# Patterns (Fase 2)", ""]
    if not patterns:
        lines += ["_(nenhum padrão reutilizável extraído)_", ""]
    for p in patterns:
        lines += [f"## {p.get('name','')}",
                  f"- **Problema:** {p.get('problem','')}",
                  f"- **Mecanismo:** {p.get('mechanism','')}",
                  f"- **Trade-offs:** {p.get('tradeoffs','')}", ""]
    return "\n".join(lines)


def _evidence(ev) -> str:
    if not ev:
        return "_(sem evidência)_"
    return "; ".join(f"{e.get('file','')}:{e.get('line','')}"
                     + (f" — “{e.get('quote')}”" if e.get("quote") else "")
                     for e in ev)


def classification_md(classifications: list[dict]) -> str:
    lines = ["# Classification (Fase 3)", ""]
    if not classifications:
        lines += ["_(nenhuma classificação)_", ""]
    for c in classifications:
        verified = c.get("verified")
        badge = "" if verified is None else ("  ✅ citações verificadas" if verified else "  ⚠️ citação não verificada")
        lines += [f"## {c.get('pattern','')} — **{c.get('verdict','')}**{badge}",
                  f"- **Evidência:** {_evidence(c.get('evidence', []))}",
                  f"- **Racional:** {c.get('rationale','')}", ""]
    return "\n".join(lines)
