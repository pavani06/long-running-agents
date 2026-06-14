---
title: "Quarto Content Structure"
type: canonical
tags: ["curriculo-conteudo", "arquitetura", "governanca"]
aliases: ["content structure", "quarto content patterns", "parts-based organization", "landing page orientation", "reader orientation", "estrutura de conteudo"]
last_updated: 2026-06-14
relates-to: ["[[docs/canonical/persona-based-documentation|Persona-Based Documentation]]", "[[docs/canonical/quarto-publishing-architecture|Quarto Publishing Architecture]]", "[[docs/canonical/quarto-authoring-workflow|Quarto Authoring Workflow]]", "[[curriculum/README|Curriculum README]]", "[[curriculum/INDEX|Curriculum Index]]", "[[AGENTS|AGENTS.md]]", "[[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-classification|Quarto Classification]]"]
sources: ["[[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-analysis|Quarto Analysis]]", "[[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-patterns|Quarto Patterns]]", "[[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-classification|Quarto Classification]]"]
---
# Quarto Content Structure

**Type:** canonical
**Status:** active
**Source:** analysis/2026-06-14-quarto-book-publishing/
**Classification:** Partial Coverage (consolidated: Parts-Based Chapter Organization, Landing Page as Reader Orientation)
**Precedence:** Level 2 ([[docs/system-of-record|System of Record]])

---

## Problem

Long-form technical content and documentation face two structural failures:

1. **Flat chapter lists lose narrative coherence.** When chapters are only a flat list of files, readers cannot see the learning path before opening individual chapters. Authors lose the ability to group related content under semantic labels, and reorganization requires touching every chapter file rather than a single structural declaration. The table of contents becomes a file listing, not a navigation design ([[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-analysis|analysis]]:58-75, 77-98).

2. **Readers arrive without orientation.** When a reader encounters a book or documentation package, they need immediate answers to three questions: what is this, who is it for, and where do I start? Without a dedicated landing page, readers must scan chapters and infer answers — or worse, dive into the first chapter without understanding the scope, prerequisites, or recommended paths. Orientation concerns bleed into chapter content, where they distract from the material ([[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-analysis|analysis]]:99-103).

The Quarto content structure addresses both through two patterns: parts-based chapter organization and landing page as reader orientation.

## Solution

### Pattern 1: Parts-Based Chapter Organization (Partial Coverage)

Chapters are grouped into semantic parts declared in the publishing manifest. Each part has a label that communicates its theme, and the part groups chapters into a navigation section. The structure is declared in YAML within the publishing contract, not hardcoded in file naming or directory layout.

```yaml
book:
  chapters:
    - index.qmd
    - part: "Fundamentals"
      chapters:
        - chapters/01_intro.ipynb
        - chapters/02_core_concepts.ipynb
    - part: "Advanced Topics"
      chapters:
        - chapters/03_patterns.ipynb
        - chapters/04_case_studies.ipynb
```

The non-obvious implication: the book's organization is code, not a design artifact. Reorganizing parts — moving a chapter between parts, renaming a part, splitting one part into two — is a git commit on the manifest file, not a drag-and-drop session in a CMS. The diff on the manifest shows exactly what changed structurally, and reviewers can audit the navigation impact before merge ([[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-analysis|analysis]]:77-98).

**Components:**

1. **Independent chapter files.** Each chapter is its own file (`.ipynb`, `.qmd`, or `.md` — mixing freely). This enables parallel authorship: two authors can work on different chapters without merge conflicts. Chapters are organized by naming convention (`01_`, `02_`) but their structural position is defined by the manifest, not the filename.

2. **Semantic part labels.** Parts are more than TOC labels — they are grouping declarations the publishing system renders as distinct visual sections in the navigation sidebar. A part communicates the theme before the reader opens a chapter. Part names should form a coherent taxonomy; weak labels create a false sense of structure.

3. **Manifest-driven navigation rendering.** The navigation sidebar, table of contents, and chapter ordering are all generated from the YAML structure. Changing navigation is a manifest edit, not a template or CSS change.

4. **Organization as versioned content decision.** Because the structure lives in version control, the decision to split "Fundamentals" into "Foundations" and "First Steps" is tracked, reviewable, and reversible. This turns content organization from a one-time design decision into an evolving structural choice ([[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-patterns|patterns]]:41-61).

**Limitations:** The taxonomy must be stable — renaming parts after publication breaks reader expectations. Too many parts can make navigation noisier than a flat chapter list. Link validation and reader-path review are still required after reorganization, even though the structural declaration is clean ([[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-patterns|patterns]]:59-62).

### Pattern 2: Landing Page as Reader Orientation (Partial Coverage)

A dedicated entry page (`index.qmd` or equivalent) serves as the structural front matter of the book. It is distinct from chapter content: chapters teach material, the landing page orients readers. It answers purpose, audience, prerequisites, and start-here guidance before any deep content begins.

```
Landing Page (index.qmd)
    |
    +---> What is this? (title, purpose, scope)
    +---> Who is it for? (audience, prerequisites)
    +---> Where to start? (recommended paths by persona/level)
    +---> How to navigate? (links to chapters, indices, setup)
    |
    v
Reader enters with context → navigates to the right starting point
```

**Components:**

1. **Purpose and audience definition.** The landing page declares what the material is, who it serves, and what prerequisites are expected. This prevents readers from starting content they are not prepared for or spending time on material that does not match their needs.

2. **Recommended paths by persona or experience level.** Different readers need different starting points. A beginner needs fundamentals first; an experienced practitioner needs the advanced patterns. The landing page provides persona-specific navigation: "If you are X, start at chapter A. If you are Y, start at chapter B."

3. **Separation of orientation from content.** Orientation concerns (what this is, who it is for, where to start) live on the landing page, not in chapter bodies. Chapters focus on teaching content; the landing page handles onboarding. This prevents the first chapter from becoming a dumping ground for introduction, prerequisites, and navigation advice that should live in a distinct structural surface.

4. **Staleness review trigger.** When the content structure changes (chapters added, parts reorganized, scope shifts), the landing page must be reviewed for staleness. Its recommended paths, audience description, and scope boundaries can drift from the actual content if not kept in sync. The landing page should be part of the structural review process, not a set-and-forget artifact ([[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-analysis|analysis]]:99-103).

**Limitations:** The landing page becomes stale if curriculum structure changes without updating entry routes. It cannot compensate for unclear chapter titles or weak part taxonomy — good orientation depends on good underlying structure. Multiple audiences may need persona-specific landing pages rather than a single generic introduction, which leads toward the pattern described in [[docs/canonical/persona-based-documentation|Persona-Based Documentation]] ([[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-patterns|patterns]]:84-88).

## Implementation in this repo

### What already exists

The long-running-agents repository has both patterns in analogous form through its curriculum structure and orientation surfaces, earning Partial Coverage for both:

**Parts-Based Chapter Organization — Partial Coverage:**

- The curriculum's 4-level structure (Nivel 1 Fundamentos, Nivel 2 Padroes Praticos, Nivel 3 Arquitetura Avancada, Nivel 4 KODA-Especifico) is a hierarchical content grouping that mirrors the parts-based organization pattern. Each level groups related lessons, exercises, and case studies under a semantic label with duration and focus declared in [[curriculum/README|Curriculum README]] lines 190-248 ([[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-classification|classification]]:54-71).

- [[curriculum/MASTER_PLAN|Curriculum Master Plan]] lines 184-270 defines level definitions with hierarchical grouping, listing concepts, learning objectives, and artifacts per level. This is structurally analogous to a manifest-driven TOC.

- [[curriculum/INDEX|Curriculum Index]] provides executive navigation by level, functioning as the rendered navigation output of the hierarchical structure.

However, the curriculum's grouping serves teaching progression (what should be learned in what order), not book publishing navigation. It is not formalized as a named reusable pattern. It lacks manifest-driven navigation rendering from a single content structure declaration — the structure is implicit in the directory layout and README descriptions, not a single YAML manifest that drives navigation generation. Link validation after reorganization is manual ([[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-classification|classification]]:66-71).

**Landing Page as Reader Orientation — Partial Coverage:**

- [[README|Repository README]] lines 19-30 defines purpose and audience: building long-running AI agent systems, for business builders and system builders, using KODA as the case domain. This answers "what is this" and "who is it for."

- [[curriculum/INDEX|Curriculum Index]] provides per-profile navigation with start-here paths: "Se voce e X, comece por Y." This is the persona-specific routing that a landing page provides.

- [[curriculum/QUICK_START|Quick Start]] provides an onboarding path in 45 minutes, answering "where to start" for new readers.

- [[curriculum/README|Curriculum README]] lines 190-248 provides level orientation with duration, focus, and artifact descriptions per level.

However, these are curriculum indices, not a formalized landing page pattern. They lack the publishing-specific mechanics: audience routing from a manifest, staleness review triggers when curriculum structure changes, and separation of orientation concerns from chapter content. The README, INDEX, and QUICK_START are orientation surfaces but not a named, reusable pattern with documented mechanics ([[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-classification|classification]]:83-95).

### What is missing

For **Parts-Based Chapter Organization:**

1. Formalization as a named reusable pattern with documented mechanics for manifest-driven navigation rendering.
2. A single content structure declaration (YAML or equivalent) that drives navigation generation, rather than implicit structure through directory layout.
3. Automated link validation after chapter reorganization.
4. Part taxonomy driven by content purpose rather than teaching progression (the curriculum's levels are pedagogical, not structural).

For **Landing Page as Reader Orientation:**

1. Formalized landing page pattern with documented audience routing mechanics.
2. Staleness review trigger when curriculum structure changes — no mechanism ensures the landing page stays synchronized with content reorganization.
3. Separation of orientation concerns from chapter content as an explicit design principle.

Both gaps are low-priority for the agentic AI engineering codebase. The curriculum already has effective orientation surfaces and hierarchical organization. Formalizing these as named patterns would add canonical documentation value but would not change day-to-day content operations. The patterns exist as domain knowledge references, not as integration targets.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Parts-based grouping communicates the learning path before readers open chapters | Requires stable taxonomy; weak part names create false structure |
| Structure is code — reorganization is a git commit, not a CMS session | Too many parts make navigation noisier than a flat list |
| Independent chapter files enable parallel authorship without merge conflicts | Reorganization still requires link validation and reader-path review |
| Landing page answers purpose, audience, and start-here before deep content begins | Becomes stale if content structure changes without updating entry routes |
| Orientation stays out of chapter bodies — chapters focus on teaching | Cannot compensate for unclear chapter titles or weak part taxonomy |
| Persona-specific paths guide different readers to different starting points | Multiple audiences may need separate landing pages, not one generic intro |

## Relationship to Other Patterns

- **Declared by:** [[docs/canonical/quarto-publishing-architecture|Quarto Publishing Architecture]] because the parts-based structure and landing page are declared in the publishing manifest (`_quarto.yml`), which is the config-driven contract.
- **Rendered by:** [[docs/canonical/quarto-authoring-workflow|Quarto Authoring Workflow]] because the live preview and build pipeline render the parts structure and landing page for visual verification.
- **Extends toward:** [[docs/canonical/persona-based-documentation|Persona-Based Documentation]] because multiple audiences on a landing page may need persona-specific paths, which leads to persona-specific documentation surfaces — one source, multiple views for different reader profiles.
- **Implemented as:** [[curriculum/README|Curriculum README]] lines 190-248 because the curriculum's 4-level structure with parts, levels, and orientation mirrors the parts-based and landing page patterns.
- **Navigated via:** [[curriculum/INDEX|Curriculum Index]] because the index provides per-profile navigation analogous to the rendered output of parts-based organization.
- **Onboarded via:** [[curriculum/QUICK_START|Quick Start]] because the quick start provides the start-here path that a landing page would route to.
- **Governed by:** [[AGENTS|AGENTS.md]] Rule 16 because any content structure in this repo must follow Obsidian conventions (frontmatter, wikilinks, tags) regardless of the organizational pattern.

## References

- [[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-analysis|analysis]]:58-75 — modular chapter organization with independent files.
- [[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-analysis|analysis]]:77-98 — config-driven table of contents with parts as semantic grouping.
- [[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-analysis|analysis]]:99-103 — landing page as structural front matter.
- [[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-patterns|patterns]]:41-65 — Parts-Based Chapter Organization pattern definition.
- [[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-patterns|patterns]]:67-91 — Landing Page as Reader Orientation pattern definition.
- [[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-classification|classification]]:50-71 — Parts-Based Chapter Organization: Partial Coverage classification with evidence.
- [[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-classification|classification]]:73-95 — Landing Page as Reader Orientation: Partial Coverage classification with evidence.
- [[curriculum/README|Curriculum README]]:190-248 — 4-level curriculum structure with parts, duration, and focus.
- [[curriculum/MASTER_PLAN|Curriculum Master Plan]]:184-270 — level definitions with hierarchical grouping.
- [[curriculum/INDEX|Curriculum Index]] — executive index with navigation by level and profile.
- [[curriculum/QUICK_START|Quick Start]] — onboarding path in 45 minutes.
- [[README|Repository README]]:19-30 — purpose and audience definition.
- [[docs/canonical/persona-based-documentation|Persona-Based Documentation]]:28-44 — persona-specific documentation surfaces as extension of landing page orientation.
- [[AGENTS|AGENTS.md]]:136-154 — Obsidian document conventions governing content structure in this repo.

---

*Created: 2026-06-14 | From: Quarto Book Publishing pattern classification (Partial Coverage: patterns 2, 3) | Precedence: canonical*
