---
title: "Prompt: Obsidian Adaptation — Frentes 1-3"
type: prompt
date: 2026-06-10
tags:
  - stack-tooling
  - governanca
  - curriculo-conteudo
aliases:
  - obsidian adaptation prompt
  - adaptacao obsidian
  - frentes 1 a 3
relates-to:
  - "[[prompts/PROMPTS-00-INDEX|Prompt Index]]"
  - "[[prompts/PROMPTS-08-obsidian-governance|Obsidian Governance]]"
  - "[[AGENTS|AGENTS.md]]"
  - "[[docs/system-of-record|System of Record]]"
---

# PROMPTS-07: Obsidian Adaptation — Frentes 1-3

> Entrega este prompt para um agente executor. Ele adiciona frontmatter YAML e converte links
> markdown para `[[wikilinks]]` nos arquivos existentes do repositorio, sem mexer nas licoes
> individuais do curriculo.

```
TASK:
Adapt the `long-running-agents` repository for Obsidian compatibility by adding YAML frontmatter and converting standard markdown links to `[[wikilinks]]` across three targeted surfaces: (1) a new root index catalog, (2) the 15 canonical docs plus `docs/system-of-record.md`, and (3) the 7 curriculum navigation/index files. Do NOT touch individual curriculum lessons, rawfiles, prompts, or infrastructure files.

EXPECTED OUTCOME:
- 1 new file created: `index.md` at repo root
- ~23 existing files modified with YAML frontmatter added and links converted
- After completion, opening the repo as an Obsidian vault shows: functional graph view with interconnected nodes, working backlinks between canonical docs, tag-based search returning canonical and curriculum index pages, and a navigable index.md hub linking to all key surfaces
- Zero broken wikilinks (every `[[target]]` resolves to an existing file in the repo)
- All existing content preserved exactly — only frontmatter is prepended and link syntax is changed

REQUIRED TOOLS:
- Read (to inspect each file before editing)
- Edit (for precise string replacements — add frontmatter at file start, replace link patterns)
- Write (only for the new index.md)
- Bash: `find` to verify all wikilinks resolve, `rg` to confirm no remaining `[text](path.md)` in modified files

MUST DO:

### FRONT 1 — Create root `index.md` (1 new file)

Create `/mnt/c/Users/pavan/long-running-agents/index.md` with this exact structure:

```yaml
---
title: "Long-Running Agents — Knowledge Index"
type: index
aliases: ["index", "home", "mapa"]
tags: [index]
last_updated: 2026-06-10
---
```

Body: A catalog of ALL important pages in the repo, organized in sections matching the repo's structure. Every entry uses `[[wikilinks]]` with display aliases. Sections:

1. **Canonical Patterns** — all 15 files from `docs/canonical/`, each with a one-line summary extracted from the doc's `## Problem` or first paragraph
2. **System of Record** — link to `docs/system-of-record`
3. **Analyses** — top-level analysis directories with their key files
4. **Curriculum** — links to the 7 curriculum index files (INDEX, MASTER_PLAN, README, QUICK_START, EXECUTION_PLAN, GLOSSARY, FAQ) plus level directories
5. **Architecture Decisions** — note that `docs/decisions/` is currently empty
6. **Plans** — link to existing plan files
7. **Project Docs** — README, AGENTS.md

Format example for each entry:
```markdown
- [[docs/canonical/error-context-hygiene|Error Context Hygiene]] — curates what the model sees about failures; never blind-append errors to context
```

Read each target file's title/heading and first meaningful paragraph to write accurate one-line summaries.

### FRONT 2 — Add frontmatter and convert links in canonical docs (16 files)

For each of the 15 files in `docs/canonical/` plus `docs/system-of-record.md`:

**Step A: Add YAML frontmatter at the very start of the file.**

For `docs/canonical/*.md` files, the frontmatter template is:
```yaml
---
title: "<EXTRACT FROM THE FILE'S # HEADING>"
type: canonical
aliases: []
tags: []
last_updated: 2026-06-10
relates-to: []
sources: []
---
```

For `docs/system-of-record.md`, use `type: system-of-record` and `tags: [index, arquitetura, governanca]`.

**Determining tags and aliases per file:**

Read each file's content and assign tags based on its domain. The tag vocabulary comes from the domains documented in `docs/system-of-record.md`, section "Dominios do projeto". Use the domain name in lowercase with hyphens. Tags mais especificas sao permitidas desde que ancoradas em um topico tratado nos canonicos ou analises listados no system-of-record.

Specific tag assignments for each file (derive aliases from the heading and key terms in the doc):

| File | Tags |
|---|---|
| `error-context-hygiene.md` | `[context-engineering, error-handling, 12-factor-agents]` |
| `deterministic-tool-dispatch.md` | `[agent-loop, 12-factor-agents]` |
| `owned-agent-control-loop.md` | `[agent-loop, harness, 12-factor-agents]` |
| `serializable-pause-resume-state.md` | `[agent-loop, 12-factor-agents]` |
| `head-tail-context-truncation.md` | `[context-engineering]` |
| `addressable-memory-catalog.md` | `[context-engineering]` |
| `n-plus-one-long-session-evals.md` | `[evals, context-engineering]` |
| `stable-harness-prompt.md` | `[harness, context-engineering]` |
| `late-failure-regression-suite.md` | `[evals, error-handling]` |
| `eval-tier-stratification.md` | `[evals]` |
| `pain-signal-eval-progression-gate.md` | `[evals, production]` |
| `pr-gated-eval-enforcement.md` | `[evals]` |
| `production-failure-regression-flywheel.md` | `[evals, production, error-handling]` |
| `production-grounded-eval-sampling.md` | `[evals, production]` |
| `repeatable-agent-spot-check-set.md` | `[evals]` |
| `system-of-record.md` | `[index, arquitetura, governanca]` |

For `aliases`, extract key alternative names from the doc (e.g., "error hygiene" for Error Context Hygiene, "head-tail truncation" for Head-Tail Context Truncation). Use 1-3 aliases per file. Keep them lowercase, no special chars.

For `relates-to`, add wikilinks to other canonical docs that are semantically connected. Read each file to determine natural connections (e.g., `error-context-hygiene` relates to `head-tail-context-truncation` and `stable-harness-prompt`). Use the format `"[[docs/canonical/filename|Display Name]]"`.

For `sources`, if the file references a specific analysis or external source, add a wikilink to it. Most canonical docs in this repo reference analysis files under `docs/analysis/`. Extract these from the existing `**Source:**` metadata line in the doc body.

**Step B: Convert all markdown links to wikilinks.**

Search each file for the pattern `[text](path/to/file.md)` and convert to `[[path/to/file|text]]`. Rules:
- Paths may be relative (e.g., `../analysis/...`) — resolve them to vault-relative paths (from repo root)
- Paths may be absolute from root (e.g., `docs/canonical/other-file.md`) — strip leading `/` if present, keep as vault-relative
- If the link text matches the target filename, use bare `[[path/to/file]]` (no alias needed)
- If the link text is different from the filename, use `[[path/to/file|link text]]`
- Links to external URLs (https://...) — leave as-is, do not convert
- Links to non-markdown files (`.json`, `.yaml`, `.sh`, directories) — leave as-is
- Links in code blocks (``` fenced or ` inline) — do NOT convert

For `docs/system-of-record.md` specifically: this file contains a large table of links. Convert every `[filename](relative/path.md)` in its tables to `[[relative/path|filename]]`. Verify the paths resolve correctly since this file is in `docs/` and some links go to `../` parent paths.

**Step C: Preserve existing content exactly.**
- The original `# Heading` and all body content stays unchanged below the frontmatter
- Do not remove, reorder, or modify any existing body content
- The only change to the body is link syntax conversion

### FRONT 3 — Convert curriculum index files to wikilinks + add frontmatter (7 files)

These files in `curriculum/`:
1. `INDEX.md`
2. `MASTER_PLAN.md`
3. `README.md`
4. `QUICK_START.md`
5. `EXECUTION_PLAN.md`
6. `GLOSSARY.md`
7. `FAQ.md`

**Step A: Add YAML frontmatter.**

```yaml
---
title: "<EXTRACT FROM FILE'S # HEADING>"
type: curriculum-index
aliases: []
tags: [curriculo-conteudo]
last_updated: 2026-06-10
---
```

For `GLOSSARY.md`, add `tags: [curriculo-conteudo, reference]`.
For `FAQ.md`, add `tags: [curriculo-conteudo, reference]`.

For aliases on `INDEX.md`, add `["indice", "navegacao"]`.

**Step B: Convert markdown links to wikilinks.**

These files contain many links to individual curriculum lessons. Convert ALL `[text](relative/path.md)` to `[[vault-relative/path|text]]`. Key patterns to handle:
- `[text](01-nivel-1-fundamentals/01-why-agents-lose-plot.md)` → `[[curriculum/01-nivel-1-fundamentals/01-why-agents-lose-plot|text]]`
- `[text](../05-core-concepts/01-context-management.md)` → resolve the relative path to vault-relative

**Step C: For INDEX.md specifically**, the file uses ASCII-art flow diagrams with paths like:
```
01-nivel-1-fundamentals/01-why-agents-lose-plot.md
    ↓
01-nivel-1-fundamentals/exercises/
```
Convert each path reference in these diagrams to a wikilink. Directory references (ending in `/`) should link to the directory's index or main file if one exists, or be left as text if no single target file exists.

### VERIFICATION (after all edits)

1. Run `find /mnt/c/Users/pavan/long-running-agents -name '*.md' -not -path '*/.git/*' | wc -l` — should show 191 files (190 original + 1 new index.md)
2. Run a search for remaining unconverted markdown links in the modified files: for each file in the 3 fronts, check that no `[text](*.md)` pattern remains (except in code blocks)
3. Run `rg '^---$' /mnt/c/Users/pavan/long-running-agents/index.md` — should find exactly 2 matches (opening and closing frontmatter delimiters)
4. For each canonical doc, verify the frontmatter has: `title`, `type`, `aliases`, `tags`, `last_updated`, `relates-to`, `sources` — all present, even if empty `[]`
5. Spot-check 3 wikilinks in the new index.md by reading the target files to confirm they exist at those paths
6. Run `rg -l '\[\[.*\]\]' /mnt/c/Users/pavan/long-running-agents/docs/canonical/` — should list all 15 canonical files

MUST NOT DO:
- Do NOT touch any file under `curriculum/01-nivel-1-fundamentals/`, `02-nivel-2-practical-patterns/`, `03-nivel-3-advanced-architecture/`, `04-nivel-4-koda-specific/`, `05-core-concepts/`, `06-knowledge-graphs/`, `07-implementation-guides/`, `08-tools-templates/`, `09-case-studies/`, `10-references/` — only the 7 top-level curriculum index files
- Do NOT touch files in `rawfiles/`, `prompts/`, `.opencode/`, `.github/`, `web/`, `webpage/`, `scripts/`, `eslint-rules/`
- Do NOT touch `AGENTS.md`, `README.md`, `package.json`, `Makefile`, or any non-markdown file
- Do NOT modify any existing body content beyond link syntax conversion
- Do NOT add frontmatter to files that already have it (the 3 `docs/analysis/*/\*-patterns.md` files)
- Do NOT change file names or directory structure
- Do NOT convert external URLs (`https://...`) to wikilinks
- Do NOT convert links inside fenced code blocks (```) or inline code (`)
- Do NOT delete any existing content, headings, or metadata lines

CONTEXT:

Repository root: `/mnt/c/Users/pavan/long-running-agents`

This is a software project with documentation, not a pure knowledge base like `raw-knowledge`. The goal is to make the authoritative documentation surfaces navigable in Obsidian without disrupting the project's existing structure.

The repo has 190 markdown files. Only 3 have YAML frontmatter (all `docs/analysis/*/\*-patterns.md`). Zero files use `[[wikilinks]]` — all cross-references are standard `[text](path.md)`.

Key files you must read before editing to extract titles, summaries, and link targets:
- All 15 files in `docs/canonical/`
- `docs/system-of-record.md`
- All 7 curriculum index files listed above
- `docs/analysis/2026-06-09-12-factor-agents/2026-06-09-12-factor-agents-analysis.md` (source for several canonical docs)
- `docs/analysis/2026-06-09-how-we-solved-context-management-in-agents/2026-06-09-how-we-solved-context-management-in-agents-analysis.md` (source for context-engineering canonical docs)
- `docs/analysis/2026-06-10-eval-maturity-phases/2026-06-10-eval-maturity-phases-analysis.md` (source for eval canonical docs)

The reference pattern for Obsidian-ready frontmatter comes from `raw-knowledge` at `/mnt/c/Users/pavan/Raw-Knowledge`. Key conventions:
- All YAML list values use `[]` for empty, `["value"]` for single, `["value1", "value2"]` for multiple
- `aliases` are lowercase, comma-separated alternatives to the title
- `tags` are lowercase, hyphenated domain terms
- `[[wikilinks]]` use vault-relative paths (from repo root), with optional `|Display Text` after the path
- Frontmatter is delimited by `---` on its own lines, at the very start of the file (line 1)

Existing metadata pattern in canonical docs: they use bold labels like `**Type:** canonical`, `**Status:** active`, `**Source:** ...`, `**Classification:** ...`. These stay in the body — the new YAML frontmatter supplements them, it does not replace them.
```
