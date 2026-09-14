"""Fase 4 — creation of ONE proposed canonical doc for a Missing pattern.

First-Useful-Governed-Loop slice (#263, minimal). Generates exactly ONE artifact
type: **proposed canonical documentation**. Hard invariants:

  * **creation != promotion** — F4 writes ONLY under `docs/analysis/<slug>/proposed/`;
    it MUST NEVER write to `docs/canonical/` (or any authoritative layer). The
    `intended_destination` is recorded as provenance for the human reviewer, not acted on.
  * No ranking, no skills/exercises, no manifest framework — those are out of this slice.

The proposed artifact keeps enough provenance for human review: source/slug, selected
pattern, the Phase-3 verdict (Missing), the evidence/citations that grounded it, the
intended destination, and the proposed content. `build_messages`, `parse_creation`,
`slugify`, `intended_destination`, `proposed_artifact`, `render_markdown` and
`quarantine_path` are pure and unit-tested; `create` makes the single GLM call and
`write_proposed` is the only disk write (guarded by the never-canonical invariant).
"""
from __future__ import annotations

import re
from pathlib import Path

import serialize
from glm import GLMError, chat_json

CANONICAL_DIR = "docs/canonical"
QUARANTINE_SUBDIR = "proposed"

_SYSTEM = (
    "Você redige uma PROPOSTA de documentação canônica para ESTE repositório a partir de "
    "um padrão reutilizável que a análise classificou como AUSENTE (Missing) no repo. É uma "
    "PROPOSTA em quarentena para revisão humana — não afirme que já existe, não invente "
    "arquivos/símbolos do repo, não cite caminhos inexistentes. Baseie-se no padrão "
    "(problema/mecanismo/trade-offs) e explique como ele se aplicaria aqui. Escreva conciso e "
    "mecanicista, no estilo de um doc canônico. Responda APENAS um objeto JSON válido:\n"
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
    """Where this WOULD live if a human promotes it. Recorded, never written. Pure."""
    return f"{CANONICAL_DIR}/{slugify(pattern.get('name',''))}.md"


def proposed_artifact(*, slug: str, source_file: str, video_id: str, pattern: dict,
                      verdict: str, evidence: list[dict], creation: dict) -> dict:
    """Assemble the full proposed artifact with human-review provenance. Pure."""
    return {
        "type": "proposed-canonical-doc",
        "status": "proposed",
        "created_by": "analyze-and-improve F4 (creation != promotion)",
        "source": source_file,
        "slug": slug,
        "video_id": video_id,
        "pattern": pattern.get("name", ""),
        "phase3_verdict": verdict,
        "problem": pattern.get("problem", ""),
        "mechanism": pattern.get("mechanism", ""),
        "evidence": evidence or [],
        "intended_destination": intended_destination(pattern),
        "title": creation["title"],
        "content": creation["body"],
    }


def render_markdown(artifact: dict) -> str:
    """Serialize the proposed artifact to a quarantine markdown file. Pure.

    A provenance frontmatter block (deliberately `type: proposed-canonical-doc`, NOT
    `analysis`/canonical — it is a proposal, not an authoritative doc) + the proposed
    content. The block carries everything the human needs to review the proposal."""
    fm = {
        "type": artifact["type"], "status": artifact["status"],
        "created_by": artifact["created_by"], "source": artifact["source"],
        "slug": artifact["slug"], "video_id": artifact["video_id"],
        "pattern": artifact["pattern"], "phase3_verdict": artifact["phase3_verdict"],
        "intended_destination": artifact["intended_destination"],
        "evidence": artifact["evidence"],
    }
    lines = ["---", serialize.to_yaml(fm).rstrip(), "---", "",
             f"# (PROPOSTA) {artifact['title']}", "",
             "> ⚠️ Proposta em quarentena — criada por análise, **não promovida**. "
             f"Destino pretendido (se aprovada): `{artifact['intended_destination']}`.", "",
             f"**Fonte:** `{artifact['source']}` · **padrão:** {artifact['pattern']} · "
             f"**Fase-3:** {artifact['phase3_verdict']}", "",
             "---", "", artifact["content"], ""]
    return "\n".join(lines)


def quarantine_path(repo_root: Path, slug: str, pattern: dict) -> Path:
    """The quarantine path for the proposal. Guarded: NEVER under docs/canonical/. Pure."""
    path = repo_root / "docs" / "analysis" / slug / QUARANTINE_SUBDIR / f"{slugify(pattern.get('name',''))}.md"
    _assert_never_canonical(path, repo_root)
    return path


def _assert_never_canonical(path: Path, repo_root: Path) -> None:
    """Enforce creation != promotion: refuse any path under an authoritative layer."""
    rel = path.resolve().relative_to(repo_root.resolve()).as_posix()
    if rel.startswith(f"{CANONICAL_DIR}/") or rel.startswith("curriculum/"):
        raise ValueError(f"F4 must never write to an authoritative layer: {rel}")
    if f"/{QUARANTINE_SUBDIR}/" not in f"/{rel}":
        raise ValueError(f"F4 must write under {QUARANTINE_SUBDIR}/: {rel}")


def create(pattern: dict, *, slug: str, source_file: str, video_id: str,
           evidence: list[dict], source_context: str, zai_key: str,
           client=chat_json) -> dict:
    """Generate the proposed artifact (one GLM call). `client` is injectable."""
    reply = client(build_messages(pattern, source_context), zai_key)
    creation = parse_creation(reply)
    return proposed_artifact(slug=slug, source_file=source_file, video_id=video_id,
                             pattern=pattern, verdict="Missing", evidence=evidence,
                             creation=creation)


def write_proposed(repo_root: Path, artifact: dict, slug: str, pattern: dict) -> str:
    """Write the proposal to quarantine; return the repo-relative path. Only disk write."""
    path = quarantine_path(repo_root, slug, pattern)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(artifact), encoding="utf-8")
    return path.resolve().relative_to(repo_root.resolve()).as_posix()
