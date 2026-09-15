"""Fase 4 — creation of ONE proposed canonical doc for a Missing pattern.

First-Useful-Governed-Loop slice (#263, minimal). Generates exactly ONE artifact
type: **canonical documentation**. Hard invariant, boundary redefined:

  * **creation != promotion** — creation writes the canonical artifact at its real
    destination `docs/canonical/<slug>.md` **on the isolated proposal branch**, with
    complete canonical frontmatter/conventions. Promotion happens ONLY when a human
    merges that PR into `main`. **The PR is the quarantine.** F4 never writes to `main`
    directly (the workflow commits to a proposal branch and opens a PR with auto-merge
    OFF); merging is a human act.
  * No ranking, no skills/exercises, no manifest framework — those are out of this slice.

The doc carries the canonical convention (title/type/aliases/tags/last_updated/relates-to/
sources) so it passes the docs/canonical/ CI checks; full provenance for review lives in
the body's Source/Classification block and in the PR description. `build_messages`,
`parse_creation`, `slugify`, `intended_destination`, `proposed_artifact`, `render_markdown`
and `destination_path` are pure and unit-tested; `create` makes the single GLM call and
`write_proposed` is the only disk write (guarded to the canonical target).
"""
from __future__ import annotations

import re
from datetime import date
from pathlib import Path

import serialize
from glm import GLMError, chat_json

CANONICAL_DIR = "docs/canonical"

_SYSTEM = (
    "Você redige uma PROPOSTA de documentação canônica para ESTE repositório a partir de "
    "um padrão reutilizável que a análise classificou como AUSENTE (Missing) no repo. É uma "
    "PROPOSTA para revisão humana via PR — não afirme que já existe, não invente "
    "arquivos/símbolos do repo, não cite caminhos inexistentes. Baseie-se no padrão "
    "(problema/mecanismo/trade-offs) e explique como ele se aplicaria aqui. Escreva conciso e "
    "mecanicista, no estilo de um doc canônico. O documento vai direto para docs/canonical/ e "
    "o CI valida links, então NÃO use links markdown ([texto](arquivo.md)) nem wikilinks "
    "([[...]]) — apenas prosa. Responda APENAS um objeto JSON válido:\n"
    '{"title": string, "body": string}\n'
    "`body` é markdown (sem frontmatter, sem cercas de código externas) com seções: "
    "Problema, Mecanismo, Trade-offs, Como se aplicaria aqui."
)


def slugify(name: str) -> str:
    """A filesystem-safe slug for a pattern name. Pure."""
    s = re.sub(r"[^a-z0-9]+", "-", (name or "").strip().lower()).strip("-")
    return s or "proposta"


def build_messages(pattern: dict, source_context: str) -> list[dict]:
    """System (task) + user (the Missing pattern + its source context). Pure."""
    user = (
        "PADRÃO AUSENTE (Fase 2, veredito Fase 3 = Missing):\n"
        f"- nome: {pattern.get('name','')}\n"
        f"- problema: {pattern.get('problem','')}\n"
        f"- mecanismo: {pattern.get('mechanism','')}\n"
        f"- trade-offs: {pattern.get('tradeoffs','')}\n\n"
        "CONTEXTO DA FONTE (para fidelidade, não para citar como evidência do repo):\n"
        + (source_context or "")[:2000]
    )
    return [{"role": "system", "content": _SYSTEM},
            {"role": "user", "content": user}]


def parse_creation(reply: dict) -> dict:
    """Validate the generated {title, body}. Pure."""
    title = reply.get("title")
    body = reply.get("body")
    if not isinstance(title, str) or not title.strip():
        raise GLMError("creation: 'title' must be a non-empty string")
    if not isinstance(body, str) or not body.strip():
        raise GLMError("creation: 'body' must be a non-empty string")
    return {"title": title.strip(), "body": body.strip()}


def intended_destination(pattern: dict) -> str:
    """The canonical destination this artifact is WRITTEN to on the proposal branch:
    `docs/canonical/<slug>.md`. Promotion to main is the human PR merge. Pure."""
    return f"{CANONICAL_DIR}/{slugify(pattern.get('name',''))}.md"


def proposed_artifact(*, slug: str, source_file: str, video_id: str, pattern: dict,
                      verdict: str, evidence: list[dict], creation: dict,
                      last_updated: str) -> dict:
    """Assemble the canonical-target artifact + human-review provenance. Pure.

    `type` is `canonical` — the file IS the canonical artifact, created on the proposal
    branch and promoted only by human merge (the PR is the quarantine). Provenance fields
    (source/slug/pattern/phase3_verdict/evidence) are carried for the PR description and the
    body's Source/Classification block, not the canonical frontmatter."""
    return {
        "type": "canonical",
        "created_by": "analyze-and-improve F4 (creation != promotion)",
        "source": source_file,
        "slug": slug,
        "video_id": video_id,
        "pattern": pattern.get("name", ""),
        "phase3_verdict": verdict,
        "problem": pattern.get("problem", ""),
        "mechanism": pattern.get("mechanism", ""),
        "evidence": evidence or [],
        "last_updated": last_updated,
        "intended_destination": intended_destination(pattern),
        "title": creation["title"],
        "content": creation["body"],
    }


def render_markdown(artifact: dict) -> str:
    """Serialize the canonical-target artifact to a docs/canonical/ markdown file. Pure.

    Complete canonical frontmatter (title/type/aliases/tags/last_updated/relates-to/sources)
    so it passes the docs/canonical/ CI checks, then a canonical body: a Type/Source/
    Classification block + the content. NO transient lifecycle Status is persisted — proposal
    vs promotion is represented structurally by Git (open proposal PR = proposed; merged into
    main = promoted). Body is link-free (no `[text](x.md)` — Check 5; no `[[wikilink]]` —
    Check 6); `relates-to` is empty (real cross-links are a review/curation act, not fabricated
    by F4)."""
    alias = (artifact.get("pattern") or artifact.get("slug") or "proposta").strip().lower()
    fm = {
        "title": artifact["title"],
        "type": "canonical",
        "aliases": [alias],
        "tags": ["context-engineering"],
        "last_updated": artifact["last_updated"],
        "relates-to": [],
        "sources": [artifact["source"]],
    }
    lines = ["---", serialize.to_yaml(fm).rstrip(), "---", "",
             f"# {artifact['title']}", "",
             "**Type:** Canonical Pattern",
             f"**Source:** `{artifact['source']}` — adaptado para long-running-agents",
             f"**Classification:** Missing — ausente no repo; originado da análise da fonte "
             f"(padrão: {artifact['pattern']}).", "",
             "---", "", artifact["content"], ""]
    return "\n".join(lines)


def destination_path(repo_root: Path, pattern: dict) -> Path:
    """The canonical-target path `docs/canonical/<slug>.md`, written ON THE PROPOSAL BRANCH.
    creation != promotion: writing here is creation; promotion is the human PR merge to main.
    Guarded to exactly the canonical destination. Pure."""
    rel = intended_destination(pattern)
    path = repo_root / rel
    _assert_canonical_target(path, repo_root, rel)
    return path


def _assert_canonical_target(path: Path, repo_root: Path, rel: str) -> None:
    """F4 writes exactly its canonical destination and nowhere else (branch-local creation)."""
    actual = path.resolve().relative_to(repo_root.resolve()).as_posix()
    if actual != rel or not actual.startswith(f"{CANONICAL_DIR}/"):
        raise ValueError(f"F4 must write its canonical target ({rel}); got {actual}")


def create(pattern: dict, *, slug: str, source_file: str, video_id: str,
           evidence: list[dict], source_context: str, zai_key: str,
           client=chat_json, today: str | None = None) -> dict:
    """Generate the canonical-target artifact (one GLM call). `client`/`today` injectable."""
    reply = client(build_messages(pattern, source_context), zai_key)
    creation = parse_creation(reply)
    return proposed_artifact(slug=slug, source_file=source_file, video_id=video_id,
                             pattern=pattern, verdict="Missing", evidence=evidence,
                             creation=creation, last_updated=today or date.today().isoformat())


def write_proposed(repo_root: Path, artifact: dict, slug: str, pattern: dict) -> str:
    """Write the canonical artifact to its destination on the proposal branch; return the
    repo-relative path. Only disk write. (Promotion to main = human PR merge, not this.)"""
    path = destination_path(repo_root, pattern)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(artifact), encoding="utf-8")
    return path.resolve().relative_to(repo_root.resolve()).as_posix()
