---
title: "Quarto Publishing Architecture"
type: canonical
tags: ["arquitetura", "stack-tooling", "spec-driven-development", "curriculo-conteudo"]
aliases: ["publishing architecture", "quarto architecture patterns", "publishing contract", "source bridge", "multi-format fan-out", "arquitetura de publicacao"]
last_updated: 2026-06-14
relates-to: ["[[AGENTS|AGENTS.md]]", "[[docs/canonical/persona-based-documentation|Persona-Based Documentation]]", "[[docs/canonical/application-owned-agent-control-plane|Application-Owned Agent Control Plane]]", "[[docs/canonical/llm-as-fuzzy-compiler|LLM as Fuzzy Compiler]]", "[[docs/canonical/skill-resolver-skillify-capability-pipeline|Skill Resolver Pipeline]]", "[[docs/canonical/quarto-authoring-workflow|Quarto Authoring Workflow]]", "[[docs/canonical/quarto-content-structure|Quarto Content Structure]]", "[[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-classification|Quarto Classification]]"]
sources: ["[[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-analysis|Quarto Analysis]]", "[[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-patterns|Quarto Patterns]]", "[[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-classification|Quarto Classification]]"]
---
# Quarto Publishing Architecture

**Type:** canonical
**Status:** active
**Source:** analysis/2026-06-14-quarto-book-publishing/
**Classification:** Missing (consolidated: Config-Driven Publishing Contract, Notebook/Markdown Source Bridge, Multi-Format Source Fan-Out)
**Precedence:** Level 2 ([[docs/system-of-record|System of Record]])

---

## Problem

Documentation and book publishing systems fragment when configuration, source formats, and output targets are handled by separate toolchains with no unifying contract. Three structural failures emerge:

1. **Configuration drift.** Metadata, table of contents, format choices, theme, and output behavior scatter across `setup.py`, `conf.py`, `_toc.yml`, Makefile, and manual publishing steps. No single file defines what the book is, so structural changes are invisible in version control and reviewers cannot audit the publishing contract from a diff ([[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-analysis|analysis]]:50-52, 187-193).

2. **The handoff gap.** Authors produce exploratory work in notebooks or Markdown, then face a costly translation step: export, convert, rewrite, or reformat for the publishing toolchain. The work artifact and the publishable artifact are different files, maintained separately. Changes in the exploratory source must be manually propagated to the publishing source, creating staleness and duplication ([[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-analysis|analysis]]:32-39, 159-169).

3. **Format fragmentation.** When different audiences need different output formats (HTML for web readers, PDF for offline consumption, ePub for e-readers), maintaining separate sources for each format fragments content and creates inconsistent documentation. Without a single-source multi-output rendering pipeline, format support becomes a manual conversion task ([[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-patterns|patterns]]:227-242).

The Quarto publishing model solves all three through three architectural patterns: a config-driven publishing contract, a notebook/Markdown source bridge, and a multi-format source fan-out.

## Solution

### Pattern 1: Config-Driven Publishing Contract

A single manifest file (`_quarto.yml`) serves as the executable definition of the book. It declares metadata (title, author, date), structure (parts, chapters, navigation), format (HTML theme, TOC, numbering), and output directory in one versioned artifact. No configuration lives outside this file.

```
_quarto.yml
     |
     | defines:
     |  - book metadata (title, author, date)
     |  - structure (parts > chapters)
     |  - format matrix (HTML, PDF, ePub, Word)
     |  - visual options (theme, TOC, numbering)
     |  - output directory
     |
     v
Build system reads config → renders book
```

The key insight is that the book's structure becomes code: reorganizing parts, adding chapters, or changing the theme is a git commit, not a design-tool session. The diff on `_quarto.yml` is the complete audit trail of structural evolution ([[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-analysis|analysis]]:50-52, 219-222).

### Pattern 2: Notebook/Markdown Source Bridge

Eliminates the handoff gap by making exploratory authoring artifacts the publishing source directly. Notebooks (`.ipynb`) and Markdown (`.qmd`, `.md`) are first-class chapters in the book structure. There is no conversion, export, or rewrite step between the author's working environment and the published output.

The architecture treats notebooks as production code: they must be executable, with declared dependencies and no broken cells. The publishing build executes notebooks through the Jupyter kernel, embedding outputs (code results, figures, tables) directly in the rendered HTML. This preserves the link between explanation, code, and observed output in the published artifact ([[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-analysis|analysis]]:32-39, 179-181).

The tradeoff is fragility: one notebook with a broken cell or missing dependency kills the entire build. This enforces discipline — notebooks intended for publication must be maintained like production code, not exploratory scratchpads ([[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-analysis|analysis]]:159-161).

### Pattern 3: Multi-Format Source Fan-Out

A single canonical source generates multiple reader-facing artifacts through a format matrix declared in the publishing contract. Formats (HTML, PDF, Word, ePub) are configuration parameters, not separate codebases.

```
Single canonical source (notebooks + markdown + _quarto.yml)
     |
     +---> HTML  (web readers, theme: cosmo, TOC: sidebar)
     +---> PDF   (offline, template: LaTeX, numbering: yes)
     +---> Word  (editors, stakeholders)
     +---> ePub  (e-readers, mobile)
```

Each format can have independent options (theme for HTML, template for PDF, style for Word) while sharing the same content source. Format support becomes a versioned configuration choice, not a manual conversion task. The editorial source of truth remains single; format-specific concerns are configuration, not duplication ([[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-analysis|analysis]]:143-147).

The risk is least-common-denominator content: a shared source may compromise quality for any single format because content must work across all targets. Additionally, each format requires separate QA — a valid HTML build does not prove PDF or ePub quality ([[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-patterns|patterns]]:242-245).

## Implementation in this repo

### What already exists

The long-running-agents repository has no Quarto publishing infrastructure, and there is no intention to add one. The repo is an agentic AI engineering codebase — its content is Markdown consumed through Obsidian, not HTML rendered through Quarto. The following analogous concepts exist:

- [[AGENTS|AGENTS.md]] lines 136-154 defines Obsidian document conventions as a kind of documentation contract: mandatory frontmatter with `type` and `tags`, wikilinks for cross-references, and tag taxonomy derived from system-of-record domains. This is a config-driven documentation standard, but it governs document structure and metadata, not book publishing.
- [[docs/canonical/application-owned-agent-control-plane|Application-Owned Agent Control Plane]] lines 27-64 defines a versioned prompt contract for agent control planes. The concept of a single versioned contract that governs behavior is analogous to a publishing manifest, but its domain is agent orchestration, not documentation rendering.
- [[docs/canonical/llm-as-fuzzy-compiler|LLM as Fuzzy Compiler]] frames code as a build artifact from agent generation. The concept of "source in, rendered artifact out" is structurally similar to the publishing pipeline, but the pipeline produces rendered documentation, not executable code.
- [[docs/canonical/persona-based-documentation|Persona-Based Documentation]] lines 28-44 creates different documentation surfaces for different persona audiences — one source, multiple views. This shares the multi-format philosophy but targets persona-specific NFR documents, not format-specific rendering ([[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-classification|classification]]:199-216).
- [[docs/canonical/quarto-authoring-workflow|Quarto Authoring Workflow]] covers the build, preview, and deploy patterns that consume the publishing architecture defined here.
- [[docs/canonical/quarto-content-structure|Quarto Content Structure]] covers the parts-based and landing page patterns that the publishing manifest would declare.

### What is missing

The classification marks all three patterns as Missing with Low integration value for the repo ([[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-classification|classification]]:31-48, 97-115, 199-210):

1. No publishing manifest, book configuration file, or config-driven documentation build system exists. Searches for `_quarto.yml`, publishing manifest, and declarative config returned matches only within the Quarto analysis directory.
2. No notebook infrastructure, Jupyter integration, or Quarto rendering exists. Markdown is the final format — the authoring format IS the content format, so there is no bridge between exploratory and published artifacts.
3. No multi-format publishing infrastructure exists — no HTML/PDF/ePub/Word generation from a canonical source. The repo's static HTML artifacts (portal, knowledge graphs) are hand-built single-format outputs.

These gaps are expected and correct. The repo has no documentation publishing surface, so all three patterns are inapplicable. They exist as canonical references for the conceptual architecture of documentation-as-code publishing systems, not as integration targets for the agentic AI codebase.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Single manifest makes the book structure auditable and versionable in git | Declarative config is weaker when conditional logic or dynamic TOC generation is needed |
| Notebooks as source eliminates the handoff gap between exploration and publication | Notebooks must be maintained like production code — no broken cells, declared dependencies |
| Multi-format fan-out serves different reader needs from one editorial source | Shared source risks least-common-denominator quality; each format needs separate QA |
| Configuration as single source of truth reduces drift and makes structural changes reviewable | A single manifest becomes high-blast-radius if reviewers do not understand its contract |
| Source bridge preserves the link between explanation, code, and observed output | Heavy exploratory notebooks degrade build performance and published page size |

## Relationship to Other Patterns

- **Depends on:** [[docs/canonical/quarto-content-structure|Quarto Content Structure]] because the publishing manifest declares parts and chapters, and the landing page is the structural entry point.
- **Consumed by:** [[docs/canonical/quarto-authoring-workflow|Quarto Authoring Workflow]] because the build pipeline, preview loop, and deploy mechanism all read the publishing contract and render the declared source files.
- **Analogous to:** [[docs/canonical/application-owned-agent-control-plane|Application-Owned Agent Control Plane]] because both patterns define a single versioned contract that governs behavior — one for agent orchestration, one for publishing.
- **Analogous to:** [[docs/canonical/persona-based-documentation|Persona-Based Documentation]] because both produce multiple outputs from one canonical source — one via persona-specific NFR documents, one via format-specific rendering.
- **Analogous to:** [[docs/canonical/llm-as-fuzzy-compiler|LLM as Fuzzy Compiler]] because both treat output as a build artifact from source input — one produces rendered documentation, one produces executable code.
- **Governed by:** [[AGENTS|AGENTS.md]] Rule 16 because any documentation publishing surface in this repo must follow Obsidian conventions (frontmatter, wikilinks, tags).

## References

- [[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-analysis|analysis]]:50-52, 187-193 — _quarto.yml as config-driven single source of truth for book structure.
- [[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-analysis|analysis]]:32-39, 159-169, 179-181 — notebook/Markdown source bridge and operational lessons.
- [[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-analysis|analysis]]:143-147, 219-226 — multi-format rendering and synthesis.
- [[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-patterns|patterns]]:15-36 — Config-Driven Publishing Contract pattern definition.
- [[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-patterns|patterns]]:93-117 — Notebook/Markdown Source Bridge pattern definition.
- [[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-patterns|patterns]]:225-248 — Multi-Format Source Fan-Out pattern definition.
- [[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-classification|classification]]:31-48 — Config-Driven Publishing Contract: Missing classification with NOT_FOUND evidence.
- [[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-classification|classification]]:97-115 — Notebook/Markdown Source Bridge: Missing classification with NOT_FOUND evidence.
- [[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-classification|classification]]:199-216 — Multi-Format Source Fan-Out: Missing classification with NOT_FOUND evidence.
- [[AGENTS|AGENTS.md]]:136-154 — Obsidian document conventions as documentation contract.
- [[docs/canonical/application-owned-agent-control-plane|Application-Owned Agent Control Plane]]:27-64 — versioned prompt contract as analogous single-source-of-truth pattern.
- [[docs/canonical/persona-based-documentation|Persona-Based Documentation]]:28-44 — persona-specific documentation as analogous multi-output pattern.

---

*Created: 2026-06-14 | From: Quarto Book Publishing pattern classification (Missing: patterns 1, 4, 9) | Precedence: canonical*
