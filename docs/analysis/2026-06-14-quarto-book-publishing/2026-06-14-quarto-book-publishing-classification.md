---
title: "Comparative Classification: Quarto Book Publishing Patterns vs. long-running-agents Repo"
type: analysis
tags: ["governanca", "agentes-orquestracao", "curriculo-conteudo", "documentation-publishing", "classification"]
date: 2026-06-14
aliases: ["classificacao quarto", "quarto classification", "gap analysis quarto", "quarto book publishing classification", "mapeamento padroes quarto"]
last_updated: 2026-06-14
relates-to: ["[[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-analysis|Quarto Book Publishing Analysis]]", "[[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-patterns|Quarto Book Publishing Patterns]]", "[[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-mental-model|Quarto Book Publishing Mental Model]]", "[[docs/system-of-record|System of Record]]", "[[docs/canonical/persona-based-documentation|Persona-Based Documentation]]", "[[docs/canonical/plan-execute-verify|Plan-Execute-Verify]]", "[[docs/canonical/skill-resolver-skillify-capability-pipeline|Skill-Resolver-Skillify Capability Pipeline]]"]
sources: ["[[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-patterns|Patterns YAML]]", "[[docs/system-of-record|System of Record]]", "[[AGENTS|AGENTS.md]]"]
---

# Comparative Classification: Quarto Book Publishing Patterns vs. long-running-agents Repo

**Date:** 2026-06-14
**Repo analyzed:** `long-running-agents`
**Patterns source:** Quarto Book Publishing knowledge extraction (9 patterns)
**Evidence basis:** `docs/canonical/`, `curriculum/`, `.opencode/skills/`, `docs/analysis/`, `AGENTS.md`, `.github/workflows/`

---

## Classification Legend

| Class | Meaning |
|---|---|
| Already Exists | Pattern is documented, implemented, or taught at equivalent depth |
| Partial Coverage | Elements exist but key mechanics, reframe, or formalization are missing |
| Missing | Not present in any form (doc, code, or curriculum) |
| Better Implementation | Repo has a superior or more mature version of the same idea |

---

## Domain Context

The long-running-agents repository is an agentic AI engineering codebase — its primary domain is building and teaching long-running AI agent systems. The 9 Quarto Book Publishing patterns describe documentation publishing workflows: config-driven book manifests, parts-based chapter organization, notebook-to-published-content bridges, live preview authoring, dependency-gated builds, single-command deploys, CI/CD publishing pipelines, and multi-format fan-out.

These are fundamentally different domains. The repo has no Quarto, no Jupyter, no book publishing infrastructure, no gh-pages deployment, and no multi-format rendering pipeline. Expect most patterns to be classified as Missing — that is correct, not a failure of analysis.

Where Partial Coverage exists, it is through analogous concepts: the curriculum's level-based structure resembles parts-based organization, the repo's CI workflow and validation gates resemble dependency-gated builds, and the repo's orientation surfaces (INDEX.md, README.md) resemble landing pages.

---

## 1. Config-Driven Publishing Contract

**Classification:** Missing

**Why:**
The Quarto pattern centers on a single publishing manifest (`_quarto.yml`) that encodes book metadata, table of contents, formats, theme, and output behavior as a versioned, auditable artifact. The long-running-agents repo has no publishing manifest, no book configuration file, and no config-driven documentation build system.

Searches for `_quarto.yml`, `publishing manifest`, `declarative config`, `config-driven` returned matches only within the Quarto analysis directory itself — no results in canonical docs, curriculum, skills, or READMEs.

The closest analogous concept is `docs/canonical/application-owned-agent-control-plane.md` which defines a versioned prompt contract, structured action schema, and deterministic dispatch for agent control planes — but this targets agent execution, not documentation publishing. The repo's `AGENTS.md` defines operational rules and `docs/system-of-record.md` defines document precedence, but neither is a publishing manifest for a documentation book.

**Evidence:**
- NOT_FOUND: `_quarto.yml`, `publishing manifest`, `declarative config`, `config-driven` — searched across `docs/canonical/`, `curriculum/`, `.opencode/skills/`, `README.md`, `AGENTS.md`
- `docs/canonical/application-owned-agent-control-plane.md:31-60` — versioned prompt contract and control plane, analogous concept but unrelated domain
- `AGENTS.md:136-160` — Obsidian document conventions define document structure rules, not publishing manifests
- `docs/system-of-record.md:140-223` — 62 canonical patterns, none about publishing configuration

**Integration value:** Low — different domain. No reasonable integration path for a publishing manifest into an agentic AI engineering curriculum.

---

## 2. Parts-Based Chapter Organization

**Classification:** Partial Coverage

**Why:**
The pattern describes grouping chapters into semantic parts (e.g., "Fundamentals", "Practical Patterns", "Advanced Architecture") to create hierarchical navigation and narrative coherence. The repo's curriculum already uses a 4-level structure with parts:

- Nivel 1 — Fundamentos (`curriculum/01-nivel-1-fundamentals/`)
- Nivel 2 — Padroes Praticos (`curriculum/02-nivel-2-practical-patterns/`)
- Nivel 3 — Arquitetura Avancada (`curriculum/03-nivel-3-advanced-architecture/`)
- Nivel 4 — KODA-Especifico (`curriculum/04-nivel-4-koda-specific/`)

Each level groups related lessons, exercises, and case studies under a semantic label. This mirrors the parts-based organization concept: independent chapters grouped by reader progression.

However, this is Partial Coverage, not Already Exists, because:
1. The curriculum structure serves teaching progression (scaffolded learning), not book publishing navigation.
2. The repo does not formalize "parts-based chapter organization" as a named pattern — it is emergent from the curriculum design, not a documented reusable pattern.
3. No canonical doc covers hierarchical content organization for publishing; no skill or tool implements parts-based navigation generation.
4. The Quarto pattern includes specific mechanics (manifest-driven navigation rendering, link validation after reorganization) that the repo does not have.

**Evidence:**
- `curriculum/README.md:190-248` — 4-level curriculum structure with parts
- `curriculum/MASTER_PLAN.md:184-270` — level definitions with hierarchical grouping
- `curriculum/INDEX.md` — executive index with navigation by level and profile
- NOT_FOUND: "parts-based", "chapter organization", "navigation sections" as named patterns — searched across `docs/canonical/`, `curriculum/`, `.opencode/skills/`
- NOT_FOUND: manifest-driven navigation rendering or link validation after reorganization in any skill or canonical doc

**Integration value:** Low — the curriculum already has a parts-based structure for its own domain. The publishing-specific mechanics (manifest-driven navigation, reorganization validation) are irrelevant to agentic AI engineering.

---

## 3. Landing Page as Reader Orientation

**Classification:** Partial Coverage

**Why:**
The pattern describes a dedicated entry page that orients readers with purpose, audience, prerequisites, and start-here routes before deep technical content begins. The repo has orientation surfaces that serve analogous purposes:

- `README.md:19-30` — defines project purpose and target audiences (business builders learning agentic systems, production operators)
- `curriculum/INDEX.md` — executive index with navigation by reader profile
- `curriculum/QUICK_START.md` — 45-minute onboarding path
- `curriculum/README.md:190-248` — level descriptions with duration and focus

These surfaces orient readers before they dive into specific lessons. The repo's `README.md` functions as the primary landing page for the repository, and the curriculum index provides persona-aware navigation.

However, this is Partial Coverage because:
1. The repo's orientation surfaces are curriculum indices and READMEs, not a formalized "Landing Page as Reader Orientation" pattern.
2. The Quarto pattern's specific mechanics — routing different audiences to different starting paths from a single landing page, keeping onboarding concerns out of ordinary chapters, staleness review triggers — are not present.
3. No canonical doc, skill, or curriculum lesson formalizes landing page design as a reusable pattern.
4. No tool or skill generates or validates landing pages from content structure.

**Evidence:**
- `README.md:19-30` — purpose and audience definition
- `curriculum/INDEX.md` — executive index with per-profile navigation
- `curriculum/QUICK_START.md` — onboarding path
- `curriculum/README.md:190-248` — level orientation with duration and focus
- NOT_FOUND: "landing page", "reader orientation", "entry page" as named patterns — searched across `docs/canonical/`, `curriculum/`, `.opencode/skills/`

**Integration value:** Low — the repo already has effective orientation surfaces. The publishing-specific mechanics (staleness review triggers, audience routing from manifest) are outside the repo's domain.

---

## 4. Notebook/Markdown Source Bridge

**Classification:** Missing

**Why:**
The pattern describes publishing directly from authoring artifacts (notebooks, Markdown, Quarto documents) without rewriting into a separate publishing format. The long-running-agents repo has no notebook infrastructure, no Jupyter integration, no Quarto rendering, and no pipeline that converts exploratory authoring artifacts into published content.

Searches for `notebook`, `jupyter`, `.ipynb`, `executable notebook`, `source bridge` returned matches only within the Quarto analysis directory and one unrelated reference in a Stanford CS153 analysis file. No canonical doc, curriculum lesson, skill, or README mentions notebooks as authoring sources.

The repo uses Markdown extensively for documentation but treats it as the final format — there is no "bridge" from exploratory authoring to publishable content because the authoring format IS the content format. The `llm-as-fuzzy-compiler.md` canonical doc treats code as a build artifact, but that's about agent-generated code, not notebook publishing.

**Evidence:**
- NOT_FOUND: `notebook`, `jupyter`, `.ipynb`, `executable notebook` — searched across `docs/canonical/`, `curriculum/`, `.opencode/skills/`, `README.md`
- `docs/canonical/llm-as-fuzzy-compiler.md:65` — treats code as build artifact from agent generation, unrelated to notebook publishing
- `docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-analysis.md` — single mention of "notebook" in Stanford analysis, unrelated to publishing bridge
- NOT_FOUND: any Jupyter kernel, `requirements.txt` for notebook dependencies, or `quarto` tooling

**Integration value:** Low — the repo has no notebook authoring workflow to bridge. Adding notebook infrastructure would be a major domain expansion with no clear connection to agentic AI engineering.

---

## 5. Live Preview Authoring Loop

**Classification:** Missing

**Why:**
The pattern describes a hot-reloaded local preview (`quarto preview`) that gives authors fast feedback on formatting, navigation, and layout during editing. The long-running-agents repo has no preview server, no hot reload infrastructure, and no live authoring loop for documentation.

Searches for `live preview`, `hot reload`, `preview server`, `quarto preview` returned matches only within the Quarto analysis directory.

The closest analogous concept is the `plan-execute-verify.md` canonical doc, which describes an agent control loop with Plan → Execute → Verify phases, including checkpoints and verification gates. But this is an agent execution pattern, not a documentation authoring pattern. The `AGENTS.md` Rule 16 validation script (`scripts/check-obsidian-conventions.sh`) provides a check-after-edit cycle, but that's a batch validation gate, not a live preview.

**Evidence:**
- NOT_FOUND: `live preview`, `hot reload`, `preview server`, `quarto preview` — searched across `docs/canonical/`, `curriculum/`, `.opencode/skills/`, `AGENTS.md`
- `docs/canonical/plan-execute-verify.md:31-76` — Plan-Execute-Verify loop for agent execution, analogous loop concept but different domain
- `AGENTS.md:136-160` — Obsidian document conventions with validation script, batch check not live preview
- `scripts/check-obsidian-conventions.sh` — post-edit validation, not live preview server

**Integration value:** Low — the repo does not have a rendered documentation surface that would benefit from live preview. The validation script provides adequate post-edit checking.

---

## 6. Dependency-Gated Atomic Build

**Classification:** Partial Coverage

**Why:**
The pattern describes a CI build gate that checks dependencies, executes notebooks, and renders the full book as an atomic unit before allowing deployment. The long-running-agents repo has CI gating infrastructure:

- `.github/workflows/check-obsidian-conventions.yml` — GitHub Actions workflow that runs on push/PR to validate Obsidian conventions
- `AGENTS.md:69-78` — Rule 7 defines validation gates (`npm run lint`, `npm run test:unit`)
- `package.json` — scripts for lint and test execution
- `.opencode/skills/issue-review/SKILL.md:44-85` — references CI gates

The repo's CI infrastructure gates changes before merge — analogous to the dependency-gated build concept. The Obsidian conventions check acts as a pre-merge validation gate for documentation quality.

However, this is Partial Coverage because:
1. The repo's gates target code quality (lint, unit tests) and documentation conventions (wikilinks, frontmatter), not notebook execution, dependency diagnostics for publishing toolchains, or book rendering.
2. No gate checks that "all notebooks execute" or "all dependencies for Quarto/Jupyter are installed" — the repo has no such dependencies.
3. The build is not "atomic" in the publishing sense — it's a collection of independent validation steps, not a full-book render.
4. No canonical doc formalizes the dependency-gated build pattern for documentation.

**Evidence:**
- `.github/workflows/check-obsidian-conventions.yml:1-22` — CI workflow with push/PR triggers
- `AGENTS.md:69-78` — validation gates (lint, test:unit)
- `package.json:8-13` — lint and test scripts
- `.opencode/skills/issue-review/SKILL.md:44-85` — CI gates reference
- NOT_FOUND: `quarto check`, `jupyter`, `notebook execution`, `atomic build`, `dependency-gated` — searched across `docs/canonical/`, `curriculum/`, `AGENTS.md`

**Integration value:** Low — the repo's existing CI gates are adequate for its domain. The publishing-specific mechanics (notebook execution gate, Quarto dependency check) are irrelevant.

---

## 7. Single-Command Deploy

**Classification:** Missing

**Why:**
The pattern describes a one-command publish operation (`quarto publish gh-pages`) that renders, branches, and pushes static artifacts to a publishing branch. The long-running-agents repo has no deploy command, no gh-pages configuration, and no static site publishing mechanism.

Searches for `quarto publish`, `gh-pages`, `single-command deploy`, `publish branch` returned matches only within the Quarto analysis directory.

`AGENTS.md:93-100` (Rule 9) explicitly states "External side effects, live sends, production mutations, and publishing require explicit approval" — the repo treats publishing as a gated, human-approved action, not an automated single command.

**Evidence:**
- NOT_FOUND: `quarto publish`, `gh-pages`, `single-command deploy`, `publish branch` — searched across `docs/canonical/`, `curriculum/`, `.opencode/skills/`, `AGENTS.md`, `.github/`
- `AGENTS.md:93-100` — Rule 9: publishing requires explicit approval
- NOT_FOUND: any deploy script, gh-pages branch, or static site hosting configuration

**Integration value:** Low — the repo does not publish a static documentation site and has no need for a single-command deploy. Adding one would require infrastructure the repo does not maintain.

---

## 8. Push-to-Publish CI/CD Pipeline

**Classification:** Partial Coverage

**Why:**
The pattern describes automated CI/CD that builds and deploys documentation on every accepted branch change. The long-running-agents repo has CI/CD infrastructure:

- `.github/workflows/check-obsidian-conventions.yml` — GitHub Actions workflow triggered on push/PR
- `AGENTS.md:69-78` — Rule 7 validation gates as CI checkpoints
- `AGENTS.md:93-100` — Rule 9: publishing requires explicit approval

The repo has the CI/CD substrate (GitHub Actions, push/PR triggers, validation gates) but does not use it for documentation publishing. The Obsidian conventions workflow validates documentation quality but does not render or deploy it.

This is Partial Coverage because:
1. The CI mechanism exists but targets validation, not publishing.
2. The repo explicitly gates publishing behind human approval (`AGENTS.md:100`), which contradicts the automated push-to-publish philosophy.
3. No deploy step exists in any workflow — the pipeline stops at validation.
4. No canonical doc or skill formalizes a CI/CD publishing pipeline.

**Evidence:**
- `.github/workflows/check-obsidian-conventions.yml:1-22` — CI workflow with push/PR triggers, validation only
- `AGENTS.md:69-78` — Rule 7 validation gates
- `AGENTS.md:93-100` — Rule 9: publishing requires explicit approval
- NOT_FOUND: deploy step, gh-pages push, `quarto publish` in any CI workflow or script
- NOT_FOUND: "push-to-publish", "automated deploy", "CI/CD pipeline" for documentation — searched across `docs/canonical/`, `curriculum/`, `.github/`

**Integration value:** Low — the repo's CI infrastructure serves its current needs (code quality, documentation conventions). Extending it to publish a documentation site would be a domain expansion with no connection to agentic AI engineering.

---

## 9. Multi-Format Source Fan-Out

**Classification:** Missing

**Why:**
The pattern describes generating multiple reader-facing formats (HTML, PDF, Word, ePub) from a single canonical content source, with format-specific configuration and per-format QA. The long-running-agents repo has no multi-format publishing infrastructure.

Searches for `multi-format`, `ePub`, `PDF`, `Word`, `format fan-out`, `format matrix` returned matches only within the Quarto analysis directory and one unrelated reference in `docs/canonical/constraint-anchored-evaluation.md` (about constraint formats, not publishing formats).

The closest analogous concept is `docs/canonical/persona-based-documentation.md`, which describes creating different documentation surfaces for different persona audiences (front-end architect, reliability engineer, security specialist). This shares the "one source, multiple outputs" philosophy but targets persona-specific NFR documents, not format-specific rendering (HTML/PDF/ePub).

The repo has static HTML artifacts (`web/koda_course_portal.html`, `web/koda_knowledge_graphs_35_diagrams.html`) but these are hand-built single-format outputs, not generated from a canonical source.

**Evidence:**
- NOT_FOUND: `multi-format`, `ePub`, `PDF output`, `Word output`, `format fan-out`, `format matrix` — searched across `docs/canonical/`, `curriculum/`, `.opencode/skills/`, `README.md`
- `docs/canonical/persona-based-documentation.md:30-69` — persona-specific documentation surfaces, analogous "different outputs for different audiences" concept
- `web/koda_course_portal.html` — single-format HTML, hand-built not generated
- NOT_FOUND: any Quarto, Pandoc, LaTeX, or other multi-format rendering tooling

**Integration value:** Low — the repo does not publish in multiple formats and has no need for format fan-out. The persona-based documentation pattern provides a related but orthogonal concept (audience-specific content, not format-specific rendering).

---

## Summary

| # | Pattern | Classification | Integration Value |
|---|---|---|---|
| 1 | Config-Driven Publishing Contract | Missing | Low — different domain |
| 2 | Parts-Based Chapter Organization | Partial Coverage | Low — curriculum already structured |
| 3 | Landing Page as Reader Orientation | Partial Coverage | Low — existing orientation surfaces |
| 4 | Notebook/Markdown Source Bridge | Missing | Low — no notebook infrastructure |
| 5 | Live Preview Authoring Loop | Missing | Low — no rendered doc surface |
| 6 | Dependency-Gated Atomic Build | Partial Coverage | Low — existing CI gates adequate |
| 7 | Single-Command Deploy | Missing | Low — no static site to deploy |
| 8 | Push-to-Publish CI/CD Pipeline | Partial Coverage | Low — validation CI already exists |
| 9 | Multi-Format Source Fan-Out | Missing | Low — no multi-format publishing need |

**Key insight:** All 9 Quarto Book Publishing patterns fall into Missing (5) or Partial Coverage (4). This is expected and correct — the long-running-agents repo is an agentic AI engineering codebase, and documentation publishing patterns from Quarto describe a fundamentally different domain. The Partial Coverage classifications are through analogous concepts (curriculum structure, CI gates, orientation surfaces) that serve different purposes than their Quarto counterparts. None of the patterns have High integration value because the repo has no documentation publishing surface to which they could be applied.

**Patterns with Partial Coverage detail:**
- **Parts-Based Chapter Organization** — curriculum's 4-level structure with parts (`curriculum/README.md:190-248`) mirrors hierarchical content grouping, but serves teaching progression, not book publishing navigation.
- **Landing Page as Reader Orientation** — `README.md`, `INDEX.md`, `QUICK_START.md` orient readers before deep content, but are curriculum indices, not a formalized landing page pattern.
- **Dependency-Gated Atomic Build** — `.github/workflows/check-obsidian-conventions.yml` gates documentation quality in CI, but targets conventions (wikilinks, frontmatter), not notebook execution or full-book rendering.
- **Push-to-Publish CI/CD Pipeline** — GitHub Actions infrastructure exists for validation, but `AGENTS.md:100` gates publishing behind human approval, and no deploy step exists.

---

*Created: 2026-06-14 | From: Quarto Book Publishing pattern classification | Precedence: analysis*
