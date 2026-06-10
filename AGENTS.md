# AGENTS.md

These rules are mandatory for AI agents working in this repository. Violations should be surfaced before merge.

## Project Context

long-running-agents is a project for building and managing long-running AI agent workflows.

- Agent system: `.opencode/` (skills + agent definitions)
- Stack: Node >= 20.18.0, ESLint
- Runtime state: `.runtime/` and `artifacts/`
- Decisions: accepted ADRs in `docs/decisions/`

## Rule 0: One Task Per Session

Each work session should handle one concrete task. If a second unrelated task appears, finish or hand off the current task before starting another.

## Rule 1: Do Not Assume

Do not hide confusion. Surface tradeoffs, missing context, and conflicts before acting.

## Rule 2: Minimum Viable Change

Write the minimum code or documentation that solves the current task. No speculative abstractions, future-proofing, or unrelated cleanup.

## Rule 3: Touch Only What You Must

Modify only files required for the task. Clean up only your own mess. Never revert user or tool changes you did not make unless explicitly asked.

## Rule 4: Define Success and Verify It

Before implementation, define what done means in concrete, checkable terms. After implementation, verify against that condition with the narrowest relevant checks first, then wider checks when appropriate.

## Rule 5: GitHub Issues and Branches

Non-trivial work should be tied to a GitHub issue.

- Branch from `main`, not any historical integration branch.
- Prefer branch names like `issue/<N>-<slug>`.
- Use worktrees for parallel issue work when multiple agents or sessions are active.
- Use `agent:working` to mark an issue currently owned by an agent session.

## Rule 6: Commit and PR Style

Follow the repository's observed commit style:

- `type(scope): short description`
- `[FUP-N] type(scope): short description` for follow-ups
- PR titles and merge subjects should retain issue/PR traceability when possible.

Do not commit unless the user explicitly asks.

## Rule 7: Validation Gates

Use real npm scripts from `package.json`; do not invent validation commands.

Common gates:

- `npm run lint`
- `npm run test:unit`

Select the gates that match the changed surface.

## Rule 8: Documentation Precedence

Resolve documentation conflicts using `docs/system-of-record.md`:

1. Accepted ADRs in `docs/decisions/`
2. Active canonical docs in `docs/canonical/`
3. Validated evidence in `docs/evidence/`
4. Analysis docs in `docs/analysis/`
5. Archive docs in `docs/archive/`
6. READMEs and operational summaries

Do not contradict accepted ADRs without explicitly raising the conflict.

## Rule 9: Security Constraints

- No secrets in code, logs, tests, fixtures, docs, or artifacts.
- No force push unless explicitly requested and safe.
- No type suppressions: no `as any`, `@ts-ignore`, or `@ts-expect-error`.
- No empty catch blocks.
- No `eslint-disable` without a narrow explanation and linked issue when possible.
- External side effects, live sends, production mutations, and publishing require explicit approval.

## Rule 10: Code Standards

- Follow existing module patterns before introducing new ones.
- Keep scripts and library functions small, explicit, and testable.
- Use central config/client/logger helpers instead of scattering direct environment or logging behavior.

## Rule 11: Dependency Management

Use already-installed dependencies when possible. Adding or upgrading dependencies requires clear justification, relevant lockfile updates, and focused validation.

## Rule 12: Search Before You Code

Before editing, read the relevant docs and search for existing patterns.

Start with:

- `AGENTS.md`
- `docs/system-of-record.md`
- `README.md`
- Relevant `docs/canonical/`, `docs/decisions/`, `docs/guides/`, and `docs/evidence/`
- Existing code and tests near the target surface

## Rule 13: Review Protocol

Significant implementation should receive a second-pass review before merge. The review should check correctness, scope, tests, security, and any domain-specific compliance when relevant.

## Rule 14: Error Escalation

After three materially different failed attempts, stop changing files, document what was tried, consult a specialist, and mark or report the work as blocked if unresolved. Do not shotgun debug.

## Rule 15: Do Not Modify Runtime Artifacts Casually

Do not alter paths or contents under `.runtime/` or `artifacts/` unless the task is explicitly about runtime state, evidence, migration, or artifacts.

## Rule 16: Obsidian Document Conventions

All documentation intended for human consumption through Obsidian MUST follow these
conventions. The validation script `scripts/check-obsidian-conventions.sh` enforces them.

### 16.1 Frontmatter is mandatory

Every markdown file under `docs/canonical/`, `docs/analysis/`, and `curriculum/` index
files MUST have YAML frontmatter with at minimum `type:` and `tags:`. The frontmatter
block is delimited by `---` on its own lines at the very start of the file (line 1).

### 16.2 Document types and their required fields

| type | Directories | Required fields | Optional fields |
|---|---|---|---|
| `canonical` | `docs/canonical/` | `title`, `type`, `tags` | `aliases`, `last_updated`, `relates-to`, `sources` |
| `analysis` | `docs/analysis/` | `title`, `type`, `tags`, `date` | `aliases`, `last_updated`, `relates-to`, `sources` |
| `system-of-record` | `docs/` | `title`, `type`, `tags`, `last_updated` | `aliases` |
| `plan` | `docs/plans/` | `title`, `type`, `tags`, `date` | `aliases`, `last_updated` |
| `curriculum-index` | `curriculum/` (top-level only) | `title`, `type`, `tags`, `last_updated` | `aliases` |
| `lesson` | `curriculum/0*-*/` | `title`, `type`, `tags`, `level` | `duration`, `aliases` |
| `exercise` | `curriculum/0*-*/exercises/` | `title`, `type`, `tags`, `level` | `duration`, `aliases` |
| `case-study` | `curriculum/0*-*/case-studies/` | `title`, `type`, `tags` | `aliases` |
| `index` | root | `title`, `type`, `tags` | `aliases`, `last_updated` |

All YAML list fields use `[]` for empty, `["single"]` for one value, `["a", "b"]` for
multiple. Fields not applicable to a document type MUST NOT be present.

### 16.3 Wikilinks for all cross-references

Use `[[path/relative/to/repo/root|Display Text]]` for every reference to another
markdown file in this repository. Never use `[text](path.md)`. Leave external URLs
(`https://...`) as standard markdown links. Do not convert links inside fenced code
blocks or inline code.

### 16.4 Tags — derivadas dos dominios do projeto

As tags de um documento DEVEM corresponder a um dominio documentado em
[[docs/system-of-record|system-of-record.md]], na secao "Dominios do projeto".

Use o nome do dominio em lowercase com hifens. Exemplos:
- "Agentes e orquestracao" → `agentes-orquestracao`
- "Curriculo e conteudo" → `curriculo-conteudo`
- "Stack e tooling" → `stack-tooling`
- "Governanca de repositorio" → `governanca`

Tags mais especificas que um dominio sao permitidas desde que ancoradas em um topico
existente no system-of-record ou em um canonical doc. Exemplos validos:
`context-engineering`, `evals`, `error-handling`, `harness`, `12-factor-agents`,
`production` — todos referenciam topicos tratados nos canonicos ou analises listados
no system-of-record.

Se um documento introduz um topico novo que nao esta no system-of-record, adicione-o
primeiro ao system-of-record (na secao do dominio correspondente) e depois use a tag
correspondente. Nao crie tags para topicos nao documentados.

Para garantir que as tags reflitam o conteudo real do documento sendo
commitado:
- Antes de definir as tags, leia o documento e identifique quais dominios
  e topicos do system-of-record se aplicam ao assunto tratado.
- As tags devem corresponder ao conteudo do documento, nao apenas ao
  diretorio onde ele se encontra.
- Prefira tags de dominio (mapeamento direto) e complemente com tags de
  topico mais especificas quando o documento aprofunda um subtopico
  documentado.

Tags estruturais (independentes de dominio):
- `index` — catalogos, navegacao, mapas
- `reference` — glossarios, FAQs, referencias

### 16.5 Slug naming

Filenames use lowercase with hyphens: `error-context-hygiene.md`. No spaces, no
underscores (except `_moc-` prefix for Maps of Content), no special characters.
The filename is the canonical identifier — renaming breaks wikilinks.

### 16.6 Validation

Run `bash scripts/check-obsidian-conventions.sh` before committing documentation
changes. The script checks:
- Files in `docs/canonical/` and `docs/analysis/` have YAML frontmatter with `type`
- No raw `[text](path.md)` links remain in monitored directories
- No broken `[[wikilinks]]` point to nonexistent files
- Cross-reference tag gaps between linked documents (warning only, nao bloqueia o commit)

### 16.7 Cross-reference tag consistency

Ao definir as tags de um documento, leia os documentos que ele referencia
via `[[wikilinks]]` para garantir consistencia semantica:

- Documentos interligados que tratam do mesmo topico devem compartilhar ao
  menos uma tag em comum. Divergencias devem ser intencionais e
  justificaveis.
- Se um documento referencia [[docs/canonical/error-context-hygiene]],
  por exemplo, considere incluir `error-handling` ou `context-engineering`
  entre suas tags, se o assunto for relacionado.
- Tags herdadas por transitividade: se A referencia B, e B tem a tag
  `evals`, A tambem deve considerar `evals` caso o assunto de A envolva
  o topico tratado em B.
- Esta verificacao e um passo manual no momento do commit — o script de
  validacao emite warnings sobre gaps de interseccao entre documentos
  linkados, mas a decisao final e do autor.
