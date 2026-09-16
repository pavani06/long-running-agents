"""Fase 4 — creation of proposed canonical docs, skills and exercises (#263).

The canonical-doc path is the First-Useful-Governed-Loop slice, proven live (five
promotions merged): it generates ONE canonical doc targeted at its real
destination `docs/canonical/<slug>.md` — creation is the branch write; promotion
is the human PR merge (**the PR is the quarantine**).

The #263 remainder extends generation to **skills** (`.opencode/skills/<slug>/SKILL.md`)
and **exercises** (`curriculum/<level>/exercises/exercise-<NN>-<slug>.md`), with
verdict-aware canonical creation (P1/P2 = Partial → reframe/naming). Those artifacts
are written by `phase4_flow` into the quarantine dir (`docs/analysis/<slug>/proposed/`,
never the authoritative layers) and promoted only when the Etapa-3 gates pass.

`build_messages*`, `parse_*`, `slugify`, `next_exercise_number`, the `*_destination`
helpers, `proposed_*artifact` and `render_*markdown` are pure and unit-tested;
`create*` make one GLM call each. This module never touches disk: since #264 there
is one production write path and `phase4_flow` owns it.
"""
from __future__ import annotations

import re
from datetime import date

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


def build_messages(pattern: dict, source_context: str, repo_context: str = "",
                   verdict: str = "Missing") -> list[dict]:
    """System (task) + user (the pattern + source context + retrieved repo context).

    `repo_context` is a small top-k of repo sections (from the First-Loop retriever) used to
    ground the "Como se aplicaria aqui" section in real artifacts. Pure. When empty, the
    model is told to say so explicitly rather than invent a repo anchor. `verdict`
    ("Missing" keeps the proven-live prompt byte-identical; "Partial" reframes the
    header for P1/P2 reframe/naming docs) only varies the user-message header."""
    repo_block = (repo_context or "").strip() or "(nenhum contexto de repo recuperado)"
    label = "AUSENTE" if verdict == "Missing" else "PARCIALMENTE COBERTO"
    user = (
        f"PADRÃO {label} (Fase 2, veredito Fase 3 = {verdict}):\n"
        f"- nome: {pattern.get('name','')}\n"
        f"- problema: {pattern.get('problem','')}\n"
        f"- mecanismo: {pattern.get('mechanism','')}\n"
        f"- trade-offs: {pattern.get('tradeoffs','')}\n\n"
        "CONTEXTO DA FONTE (para fidelidade, não para citar como evidência do repo):\n"
        + (source_context or "")[:2000]
        + "\n\nCONTEXTO DO REPO (seções recuperadas — use para fundamentar a seção "
        "'Como se aplicaria aqui'):\n" + repo_block[:4000]
        + "\n\nNa seção 'Como se aplicaria aqui', ancore em arquivos/mecanismos REAIS do repo "
        "acima, nomeando os arquivos concretos quando houver suporte. Se NENHUMA âncora relevante "
        "do repo for encontrada, diga isso explicitamente — não invente arquivos nem mecanismos."
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
    verdict = artifact.get("phase3_verdict", "Missing")
    classification = (f"{verdict} — ausente no repo; originado da análise da fonte"
                      if verdict == "Missing" else
                      f"{verdict} — cobertura parcial no repo; proposta de reframe/naming")
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
             f"**Classification:** {classification} (padrão: {artifact['pattern']}).", "",
             "---", "", artifact["content"], ""]
    return "\n".join(lines)


def create(pattern: dict, *, slug: str, source_file: str, video_id: str,
           evidence: list[dict], source_context: str, zai_key: str,
           repo_context: str = "", client=chat_json, today: str | None = None,
           verdict: str = "Missing") -> dict:
    """Generate the canonical-target artifact (one GLM call). `repo_context` (a small top-k of
    retrieved repo sections) grounds the application section; `client`/`today` injectable.
    `verdict` defaults to the proven-live Missing framing; "Partial" reframes P1/P2 docs."""
    reply = client(build_messages(pattern, source_context, repo_context, verdict), zai_key)
    creation = parse_creation(reply)
    return proposed_artifact(slug=slug, source_file=source_file, video_id=video_id,
                             pattern=pattern, verdict=verdict, evidence=evidence,
                             creation=creation, last_updated=today or date.today().isoformat())


SKILLS_DIR = ".opencode/skills"

_SKILL_SYSTEM = (
    "Você redige uma PROPOSTA de skill de implementação (SKILL.md) para ESTE repositório "
    "a partir de um padrão reutilizável da análise. É uma PROPOSTA para revisão humana — "
    "não afirme que já existe, não invente arquivos/símbolos/caminhos do repo. A skill é "
    "acionável: regras de implementação que um agente carrega e aplica. Sem links markdown "
    "nem wikilinks — apenas prosa e cercas de código. Responda APENAS um objeto JSON válido:\n"
    '{"name": string, "description": string, "body": string}\n'
    "`name` é o nome curto da skill (sem o sufixo Skill). `description` é rica em triggers "
    "(quando carregar, 2-4 frases, termos de disparo). `body` é markdown SEM frontmatter e "
    "sem título H1, com as seções: ## What I Do, ## When to Use Me, ## The Anti-Pattern, "
    "## The Pattern, ## Implementation Rules, ## Quality Gates."
)


def build_skill_messages(pattern: dict, source_context: str,
                         repo_context: str = "", verdict: str = "Missing") -> list[dict]:
    """System + user for skill generation (same shape as the canonical builder). Pure.

    `verdict` is the Fase-3 classification verdict for this pattern; it is a
    classification field, never a key of the Fase-2 pattern dict."""
    repo_block = (repo_context or "").strip() or "(nenhum contexto de repo recuperado)"
    user = (
        f"PADRÃO (Fase 2, veredito Fase 3 = {verdict}):\n"
        f"- nome: {pattern.get('name','')}\n"
        f"- problema: {pattern.get('problem','')}\n"
        f"- mecanismo: {pattern.get('mechanism','')}\n"
        f"- trade-offs: {pattern.get('tradeoffs','')}\n\n"
        "CONTEXTO DA FONTE (para fidelidade, não para citar como evidência do repo):\n"
        + (source_context or "")[:2000]
        + "\n\nCONTEXTO DO REPO (seções recuperadas — use para fundamentar as regras de "
        "implementação):\n" + repo_block[:4000]
        + "\n\nAncore as Implementation Rules em arquivos/mecanismos REAIS do repo acima. "
        "Se NENHUMA âncora relevante for encontrada, escreva regras genéricas e diga isso "
        "explicitamente — não invente arquivos nem mecanismos."
    )
    return [{"role": "system", "content": _SKILL_SYSTEM},
            {"role": "user", "content": user}]


def parse_skill(reply: dict) -> dict:
    """Validate the generated {name, description, body}. Pure."""
    name = reply.get("name")
    description = reply.get("description")
    body = reply.get("body")
    if not isinstance(name, str) or not name.strip():
        raise GLMError("skill: 'name' must be a non-empty string")
    if not isinstance(description, str) or not description.strip():
        raise GLMError("skill: 'description' must be a non-empty string")
    if not isinstance(body, str) or not body.strip():
        raise GLMError("skill: 'body' must be a non-empty string")
    return {"name": name.strip(), "description": description.strip(), "body": body.strip()}


def skill_destination(pattern: dict) -> str:
    """The skill's authoritative destination `.opencode/skills/<slug>/SKILL.md`. Pure."""
    return f"{SKILLS_DIR}/{slugify(pattern.get('name',''))}/SKILL.md"


def proposed_skill_artifact(*, slug: str, source_file: str, video_id: str, pattern: dict,
                            verdict: str, evidence: list[dict], creation: dict,
                            last_updated: str) -> dict:
    """Assemble the skill artifact + provenance. Pure (mirrors proposed_artifact)."""
    return {
        "type": "skill",
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
        "intended_destination": skill_destination(pattern),
        "name": creation["name"],
        "title": creation["name"],   # uniform key for eval/manifest/PR surfaces
        "description": creation["description"],
        "content": creation["body"],
    }


def render_skill_markdown(artifact: dict) -> str:
    """Serialize the skill artifact to a SKILL.md file. Pure.

    Frontmatter follows the layer's dominant schema (name/description/license/
    compatibility/metadata — carried by 34 of the 38 hand-written skills) plus the
    quarantine-compliance fields (`type`/`aliases`/`relates-to` — the quarantined
    copy lives under docs/analysis/, where the obsidian validator requires them;
    extra keys are inert at the .opencode/skills/ destination). `name` is the
    slug of the pattern, byte-equal to the skill's own directory as every
    existing skill has it; the model's short name stays the human title. Body is
    link-free."""
    alias = (artifact.get("pattern") or artifact.get("slug") or "skill").strip().lower()
    fm = {
        "name": slugify(artifact.get("pattern") or artifact.get("name", "")),
        "description": artifact["description"],
        "license": "MIT",
        "compatibility": "opencode",
        "type": "skill",
        "aliases": [alias],
        "relates-to": [],
        "metadata": {"title": artifact["name"], "source": artifact["source"],
                     "created_by": "analyze-and-improve F4"},
    }
    return "\n".join(["---", serialize.to_yaml(fm).rstrip(), "---", "",
                      artifact["content"], ""])


def create_skill(pattern: dict, *, slug: str, source_file: str, video_id: str,
                 evidence: list[dict], source_context: str, zai_key: str,
                 repo_context: str = "", client=chat_json,
                 today: str | None = None, verdict: str = "Missing") -> dict:
    """Generate the skill artifact (one GLM call). `client`/`today` injectable.
    `verdict` is the Fase-3 classification verdict carried into prompt and manifest."""
    reply = client(build_skill_messages(pattern, source_context, repo_context, verdict), zai_key)
    creation = parse_skill(reply)
    return proposed_skill_artifact(slug=slug, source_file=source_file, video_id=video_id,
                                   pattern=pattern, verdict=verdict, evidence=evidence,
                                   creation=creation,
                                   last_updated=today or date.today().isoformat())


# ── Exercises (#263 remainder) ─────────────────────────────────────────────────

EXERCISES_SUBDIR = "exercises"
# INTERIM default placement for generated exercises — caller-overridable, and the
# resolved level is recorded per exercise in the artifact manifest. There is no
# level routing yet: Etapa 7 (#265, curriculum integration) must decide whether
# and how to own it, using the manifest's per-exercise `level` field as the
# re-routing input. Until then every generated exercise lands at level 3.
DEFAULT_LEVEL_DIR = "03-nivel-3-advanced-architecture"

_EXERCISE_SYSTEM = (
    "Você redige uma PROPOSTA de exercício hands-on de currículo para ESTE repositório "
    "a partir de um padrão reutilizável da análise. É uma PROPOSTA para revisão humana — "
    "não afirme que já existe, não invente arquivos/símbolos/caminhos do repo. Siga o "
    "formato de exercício do currículo: prólogo narrativo realista (cenário que deu "
    "errado), cenário com dados de entrada, requisitos funcionais/técnicos, tarefa em "
    "partes (diagnóstico → implementação → verificação), código esqueleto em Python, "
    "critérios de aceite com asserts e rubrica de avaliação. Sem links markdown nem "
    "wikilinks. Responda APENAS um objeto JSON válido:\n"
    '{"title": string, "body": string}\n'
    "`title` é o título do exercício. `body` é markdown SEM frontmatter e SEM título H1 "
    "(o título é renderizado fora), com as seções do formato acima."
)


def build_exercise_messages(pattern: dict, source_context: str,
                            repo_context: str = "", verdict: str = "Missing") -> list[dict]:
    """System + user for exercise generation (same shape as the canonical builder). Pure.

    `verdict` is the Fase-3 classification verdict for this pattern; it is a
    classification field, never a key of the Fase-2 pattern dict."""
    repo_block = (repo_context or "").strip() or "(nenhum contexto de repo recuperado)"
    user = (
        f"PADRÃO (Fase 2, veredito Fase 3 = {verdict}):\n"
        f"- nome: {pattern.get('name','')}\n"
        f"- problema: {pattern.get('problem','')}\n"
        f"- mecanismo: {pattern.get('mechanism','')}\n"
        f"- trade-offs: {pattern.get('tradeoffs','')}\n\n"
        "CONTEXTO DA FONTE (para fidelidade, não para citar como evidência do repo):\n"
        + (source_context or "")[:2000]
        + "\n\nCONTEXTO DO REPO (seções recuperadas — use para ancorar o cenário do "
        "exercício no que o repo já faz):\n" + repo_block[:4000]
        + "\n\nO código esqueleto deve ser executável e autocontido (importável sem "
        "recursos externos), e os asserts dos critérios de aceite devem poder falhar "
        "antes da implementação. Ancore o cenário em mecânicas REAIS do repo acima; "
        "se NENHUMA âncora relevante for encontrada, use um cenário genérico e diga "
        "isso explicitamente — não invente arquivos nem mecanismos."
    )
    return [{"role": "system", "content": _EXERCISE_SYSTEM},
            {"role": "user", "content": user}]


def parse_exercise(reply: dict) -> dict:
    """Validate the generated {title, body}. Pure."""
    title = reply.get("title")
    body = reply.get("body")
    if not isinstance(title, str) or not title.strip():
        raise GLMError("exercise: 'title' must be a non-empty string")
    if not isinstance(body, str) or not body.strip():
        raise GLMError("exercise: 'body' must be a non-empty string")
    return {"title": title.strip(), "body": body.strip()}


def next_exercise_number(existing_filenames: list[str]) -> int:
    """The next exercise number after the max `exercise-<NN>` in a level's dir. Pure.

    Deterministic numbering is the orchestrator's job (the model never picks it):
    max existing NN + 1, or 1 when the dir has no numbered exercises."""
    import re as _re
    numbers = [int(m.group(1)) for f in existing_filenames
               if (m := _re.match(r"exercise-(\d+)", f))]
    return max(numbers) + 1 if numbers else 1


def exercise_destination(pattern: dict, level_dir: str, number: int) -> str:
    """The exercise's authoritative destination
    `curriculum/<level>/exercises/exercise-<NN>-<slug>.md`. Pure."""
    return (f"curriculum/{level_dir}/{EXERCISES_SUBDIR}/"
            f"exercise-{number:02d}-{slugify(pattern.get('name',''))}.md")


def proposed_exercise_artifact(*, slug: str, source_file: str, video_id: str, pattern: dict,
                               verdict: str, evidence: list[dict], creation: dict,
                               last_updated: str, level: int, level_dir: str,
                               number: int) -> dict:
    """Assemble the exercise artifact + provenance. Pure (mirrors proposed_artifact)."""
    return {
        "type": "exercise",
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
        "intended_destination": exercise_destination(pattern, level_dir, number),
        "level": level,
        "level_dir": level_dir,
        "number": number,
        "title": creation["title"],
        "content": creation["body"],
    }


def render_exercise_markdown(artifact: dict) -> str:
    """Serialize the exercise artifact to a curriculum exercise file. Pure.

    Frontmatter carries the curriculum convention (title/type/level/tags/aliases/
    relates-to) so both the quarantined copy (docs/analysis/) and the promoted file
    (curriculum/) pass the obsidian validator. Body is link-free."""
    alias = (artifact.get("pattern") or artifact.get("slug") or "exercicio").strip().lower()
    fm = {
        "title": artifact["title"],
        "type": "exercise",
        "level": artifact["level"],
        "aliases": [alias],
        "tags": ["curriculo-conteudo", "context-engineering"],
        "relates-to": [],
        "duration": "60-90 min",
    }
    return "\n".join(["---", serialize.to_yaml(fm).rstrip(), "---", "",
                      f"# {artifact['title']}", "",
                      f"**Nível {artifact['level']}** · padrão: {artifact['pattern']} · "
                      f"fonte: `{artifact['source']}`", "",
                      artifact["content"], ""])


def create_exercise(pattern: dict, *, slug: str, source_file: str, video_id: str,
                    evidence: list[dict], source_context: str, zai_key: str,
                    level: int, level_dir: str, number: int,
                    repo_context: str = "", client=chat_json,
                    today: str | None = None, verdict: str = "Missing") -> dict:
    """Generate the exercise artifact (one GLM call). `client`/`today` injectable.
    Level/number/filename are orchestrator-decided (v3 rule): the model never picks them.
    `verdict` is the Fase-3 classification verdict carried into prompt and manifest."""
    reply = client(build_exercise_messages(pattern, source_context, repo_context, verdict), zai_key)
    creation = parse_exercise(reply)
    return proposed_exercise_artifact(slug=slug, source_file=source_file, video_id=video_id,
                                      pattern=pattern, verdict=verdict, evidence=evidence,
                                      creation=creation,
                                      last_updated=today or date.today().isoformat(),
                                      level=level, level_dir=level_dir, number=number)


_RENDERERS = {
    "canonical": render_markdown,
    "skill": render_skill_markdown,
    "exercise": render_exercise_markdown,
}


def render(artifact: dict) -> str:
    """Serialize an artifact to its destination markdown, by artifact `type`. Pure."""
    return _RENDERERS[artifact["type"]](artifact)
