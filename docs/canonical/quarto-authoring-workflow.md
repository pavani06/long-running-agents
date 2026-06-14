---
title: "Quarto Authoring Workflow"
type: canonical
tags: ["stack-tooling", "governanca", "curriculo-conteudo", "decision-discipline", "harness"]
aliases: ["authoring workflow", "quarto workflow patterns", "publishing CI/CD", "live preview loop", "dependency-gated build", "single-command deploy", "fluxo de publicacao"]
last_updated: 2026-06-14
relates-to: ["[[AGENTS|AGENTS.md]]", "[[docs/canonical/plan-execute-verify|Plan-Execute-Verify]]", "[[docs/canonical/skill-resolver-skillify-capability-pipeline|Skill Resolver Pipeline]]", "[[docs/canonical/domain-embedded-workflow-automation-wedge|Domain-Embedded Workflow Automation Wedge]]", "[[docs/canonical/quarto-publishing-architecture|Quarto Publishing Architecture]]", "[[docs/canonical/quarto-content-structure|Quarto Content Structure]]", "[[docs/canonical/persona-based-documentation|Persona-Based Documentation]]", "[[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-classification|Quarto Classification]]"]
sources: ["[[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-analysis|Quarto Analysis]]", "[[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-patterns|Quarto Patterns]]", "[[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-classification|Quarto Classification]]"]
---
# Quarto Authoring Workflow

**Type:** canonical
**Status:** active
**Source:** analysis/2026-06-14-quarto-book-publishing/
**Classification:** Missing (Live Preview Authoring Loop, Single-Command Deploy) + Partial Coverage (Dependency-Gated Atomic Build, Push-to-Publish CI/CD Pipeline)
**Precedence:** Level 2 ([[docs/system-of-record|System of Record]])

---

## Problem

Documentation authoring and publishing suffer from four structural workflow failures:

1. **Slow edit-verify cycles.** When authors must run a full build to see formatting and rendering results, verification is deferred until the documentation has accumulated many possible breakpoints. The cycle of edit, build, check, and fix takes minutes, not seconds — breaking the writing flow ([[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-analysis|analysis]]:105-109).

2. **Hidden dependency failures.** A documentation site can appear publishable locally while hidden notebook errors, missing dependencies, or broken kernel setups make the full book fail in CI. Without a dependency diagnostic gate before build, authors discover failures only after pushing ([[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-analysis|analysis]]:159-177, 201-211).

3. **Manual deploy friction.** Publishing to static hosting typically involves multiple manual steps: render, create branch, copy artifacts, configure GitHub Pages, push. Each step is a potential failure point. Even when the deploy is scripted, the need to remember to run it after every change creates friction ([[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-analysis|analysis]]:111-115, 225-226).

4. **Stale published artifacts.** When documentation changes accumulate in the repository but the published site is not updated automatically, the live documentation diverges from the source of truth. Manual deploy becomes a bottleneck that authors circumvent or forget, and the gap between repository and published content widens over time ([[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-analysis|analysis]]:117-141).

The Quarto authoring workflow solves these through four patterns: a live preview authoring loop, a dependency-gated atomic build, a single-command deploy, and a push-to-publish CI/CD pipeline. Together they form an end-to-end authoring-to-deploy workflow.

## Solution

### Pattern 1: Live Preview Authoring Loop (Missing)

A local preview server (`quarto preview`) provides hot-reloaded rendering at `http://localhost:4200`. Saving any file (notebook, Markdown, or `_quarto.yml`) triggers automatic re-rendering in the browser. This transforms book authoring into an inner development loop comparable to frontend web development: edit, save, see result immediately.

```
Author edits chapter → save → local preview server detects change
    → re-renders affected pages → browser refreshes automatically
    → author sees rendered output in seconds
```

The non-obvious implication: errors in formatting, notebook execution, and navigation are caught before CI or deploy. The live preview reduces the cost of verification to near zero, which encourages smaller, more frequent documentation changes — authors can verify each edit immediately ([[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-analysis|analysis]]:105-109, 167-177).

The limitation: local preview can still differ from CI if dependencies or environment setup drift. Heavy notebooks reduce the speed advantage. Preview is not a replacement for full build, link validation, or multi-format QA ([[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-patterns|patterns]]:131-139).

### Pattern 2: Dependency-Gated Atomic Build (Partial Coverage)

A pre-build diagnostic gate verifies that all publishing toolchain dependencies are present and functional before attempting a full build. The gate runs `quarto check jupyter` (or equivalent) to confirm that Python, Jupyter, and kernels are installed and accessible. If the gate fails, the build is aborted before any notebook execution begins.

```
Dependency check gate → pass? → full book build (all notebooks executed)
                              → deploy gate → static artifact
                       → fail? → abort with diagnostic (missing dependency, version, kernel)
```

The build itself is atomic: the entire book is rendered as a single pass/fail unit. There is no partial output — if any notebook has an execution error, the entire build fails. This guarantees that the published artifact is internally consistent, but it also means a single broken notebook blocks the entire pipeline ([[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-analysis|analysis]]:159-177, 201-211).

The operational lesson: notebooks intended for publication must be maintained like production code — executable, with declared dependencies, and without broken cells. Before each publish, authors should run all notebooks locally through the preview server to catch errors early ([[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-analysis|analysis]]:175-177).

### Pattern 3: Single-Command Deploy (Missing)

A single command (`quarto publish gh-pages`) executes the entire deployment pipeline: render the book, create or select the `gh-pages` branch, push the rendered HTML, and output the live URL. No manual branch handling, no artifact copying, no GitHub Pages configuration through the UI.

```
quarto publish gh-pages
    |
    +---> render book from source + _quarto.yml
    +---> create/select gh-pages branch
    +---> push rendered HTML artifacts
    +---> print live URL
    +---> done
```

The philosophy behind this pattern: when deploying is one command, publishing stops being a decision and becomes a reflex. The friction is low enough that documentation releases can happen as part of normal work, not as a scheduled event ([[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-analysis|analysis]]:111-115, 225-226).

The limitations: the command abstracts deployment mechanics, making failures harder to debug when it breaks. Concurrent manual deploys can conflict on the publishing branch. And publishing still requires explicit approval when external side effects are restricted by repository policy ([[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-patterns|patterns]]:186-190).

### Pattern 4: Push-to-Publish CI/CD Pipeline (Partial Coverage)

A GitHub Actions workflow triggers on push to the main branch: checkout, install Python and Jupyter, set up Quarto, run the dependency gate, build the book, and deploy to GitHub Pages — all in an ephemeral, reproducible CI environment.

```
Push to main
    |
    v
GitHub Actions workflow
    |
    +---> checkout repository
    +---> setup-python + pip install jupyter
    +---> quarto-actions/setup
    +---> quarto check jupyter (dependency gate)
    +---> quarto publish gh-pages --no-browser --no-prompt
    +---> live site updated
```

The result: the published documentation is always synchronized with the main branch. There are zero manual steps between merging a change and the live site reflecting it. The CI environment is ephemeral and reproducible, which exposes local/CI environment drift immediately — if the build works locally but fails in CI, the dependency manifest is incomplete ([[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-analysis|analysis]]:117-141).

The critical limitation: bad content reaches the published site automatically if validation gates are weak. Publishing from CI has external side effects and must respect repository approval rules. Automated deploy contradicts policies that require explicit human approval for publishing ([[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-patterns|patterns]]:214-218).

## Implementation in this repo

### What already exists

The long-running-agents repository has CI/CD infrastructure that serves as the substrate for Parts 2 and 4. Parts 1 and 3 (live preview and single-command deploy) have no equivalent because the repo has no rendered documentation surface:

- [[.github/workflows/check-obsidian-conventions.yml|CI workflow]] triggers on push/PR to validate Obsidian conventions (frontmatter, wikilinks, tags). This is a validation gate analogous to the dependency-gated build concept, but it checks documentation conventions, not notebook execution or full-book rendering. The workflow stops at validation — no deploy step exists ([[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-classification|classification]]:136-159).

- [[AGENTS|AGENTS.md]] Rule 7 (lines 69-78) defines validation gates: `npm run lint` and `npm run test:unit`. These gates are the CI entry point for code quality, analogous to the pre-build diagnostic gate. However, they target code quality and documentation conventions, not publishing toolchain diagnostics.

- [[AGENTS|AGENTS.md]] Rule 9 (lines 93-100) explicitly states that publishing requires explicit human approval. This contradicts the push-to-publish philosophy — the repo treats publishing as a gated, human-approved action, not an automated reflex. This is correct for an agentic AI codebase where external side effects must be controlled.

- [[docs/canonical/plan-execute-verify|Plan-Execute-Verify]] lines 28-74 defines a three-phase separation of planning, execution, and verification with checkpoints. The authoring workflow's edit-preview-build-deploy cycle maps loosely to this structure, but Plan-Execute-Verify is an agent execution pattern, not a documentation workflow.

- [[docs/canonical/domain-embedded-workflow-automation-wedge|Domain-Embedded Workflow Automation Wedge]] describes embedding automation in existing workflows guided by evidence. The CI/CD pipeline concept is structurally similar, but the wedge pattern targets agentic workflow embedding, not documentation deployment.

- [[docs/canonical/quarto-publishing-architecture|Quarto Publishing Architecture]] defines the config-driven source contract and format fan-out that this authoring workflow consumes. The build pipeline renders the source declared in the publishing contract.

- [[docs/canonical/quarto-content-structure|Quarto Content Structure]] defines the parts-based organization and landing page that the authoring workflow renders and deploys.

### What is missing

The classification assesses all four patterns against the repo:

1. **Live Preview Authoring Loop — Missing.** No preview server, hot reload, or live authoring loop exists. Searches for live preview, hot reload, preview server, and `quarto preview` returned no matches outside the analysis directory. The closest analogous concept is the Obsidian conventions validation script (`scripts/check-obsidian-conventions.sh`), which provides post-edit batch validation, not live preview ([[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-classification|classification]]:117-134).

2. **Dependency-Gated Atomic Build — Partial Coverage.** The CI workflow and validation gates in AGENTS.md provide gating infrastructure, but the gates target code quality and documentation conventions, not notebook execution, dependency diagnostics for publishing toolchains, or full-book rendering. No canonical doc formalizes the dependency gating pattern ([[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-classification|classification]]:136-159).

3. **Single-Command Deploy — Missing.** No deploy command, `gh-pages` branch, or static site publishing mechanism exists. AGENTS.md Rule 9 explicitly gates publishing behind human approval, directly contradicting the single-command deploy philosophy. This is correct — the repo has no static site to deploy ([[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-classification|classification]]:160-176).

4. **Push-to-Publish CI/CD Pipeline — Partial Coverage.** The GitHub Actions infrastructure exists and validates on push/PR, but no deploy step exists in any workflow. The pipeline stops at validation. The repo's explicit publishing approval requirement (AGENTS.md Rule 9) contradicts automated push-to-publish. The CI substrate is present, but the deploy action is intentionally absent ([[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-classification|classification]]:177-197).

All four gaps are expected and intentional. The repo is an agentic AI engineering codebase with Markdown documentation consumed through Obsidian — there is no rendered documentation surface that would benefit from preview, build gating, or automated deploy. The patterns exist as canonical references for documentation publishing workflow design, not as integration targets.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Live preview catches rendering and formatting errors seconds after editing | Local preview can drift from CI environment; heavy notebooks reduce speed |
| Dependency gate prevents broken notebooks from reaching the published artifact | One broken notebook blocks the entire pipeline; debugging is indirect |
| Single-command deploy reduces publishing friction to near zero | Abstracts mechanics, making failures harder to debug; concurrent deploys can conflict |
| Push-to-publish keeps documentation synchronized with the source of truth automatically | Bad content can reach production automatically if validation gates are weak |
| CI/CD exposes environment drift in an ephemeral, reproducible runner | External side effects require explicit approval — automated deploy contradicts gated publishing policies |
| Atomic build guarantees the published artifact is internally consistent | No partial output — a single failure blocks everything |

## Relationship to Other Patterns

- **Depends on:** [[docs/canonical/quarto-publishing-architecture|Quarto Publishing Architecture]] because the build pipeline, preview, and deploy all read the publishing contract and render the declared source files.
- **Depends on:** [[docs/canonical/quarto-content-structure|Quarto Content Structure]] because the live preview renders the parts-based organization and landing page for visual verification.
- **Analogous to:** [[docs/canonical/plan-execute-verify|Plan-Execute-Verify]] because the authoring workflow's edit → verify loop is structurally similar to the execute → verify phase with checkpoints, but one targets documentation and the other targets agent execution.
- **Analogous to:** [[docs/canonical/domain-embedded-workflow-automation-wedge|Domain-Embedded Workflow Automation Wedge]] because the CI/CD pipeline embeds automation in the existing push workflow, guided by validation gate evidence.
- **Analogous to:** [[docs/canonical/skill-resolver-skillify-capability-pipeline|Skill Resolver Pipeline]] because both define a pipeline from source (workflow/capability) through structured processing (skillify/build) to deployable output (skill/static site).
- **Contradicted by:** [[AGENTS|AGENTS.md]] Rule 9 because the repo's explicit human-approval requirement for publishing contradicts the automated push-to-publish pattern. This is intentional — the repo has no static site to deploy.
- **Governed by:** [[AGENTS|AGENTS.md]] Rule 7 because validation gates are the entry point for the CI pipeline. Any future publishing workflow would need to integrate with existing lint and test gates.

## References

- [[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-analysis|analysis]]:105-109, 167-177 — live preview development loop and operational lessons.
- [[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-analysis|analysis]]:159-177, 201-211 — dependency-gated atomic build and failure patterns.
- [[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-analysis|analysis]]:111-115, 225-226 — single-command deploy and one-command-as-philosophy.
- [[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-analysis|analysis]]:117-141 — push-to-publish CI/CD workflow and auto-deploy.
- [[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-patterns|patterns]]:119-142 — Live Preview Authoring Loop pattern definition.
- [[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-patterns|patterns]]:144-168 — Dependency-Gated Atomic Build pattern definition.
- [[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-patterns|patterns]]:170-195 — Single-Command Deploy pattern definition.
- [[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-patterns|patterns]]:197-223 — Push-to-Publish CI/CD Pipeline pattern definition.
- [[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-classification|classification]]:117-134 — Live Preview Authoring Loop: Missing classification with NOT_FOUND evidence.
- [[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-classification|classification]]:136-159 — Dependency-Gated Atomic Build: Partial Coverage classification.
- [[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-classification|classification]]:160-176 — Single-Command Deploy: Missing classification.
- [[docs/analysis/2026-06-14-quarto-book-publishing/2026-06-14-quarto-book-publishing-classification|classification]]:177-197 — Push-to-Publish CI/CD Pipeline: Partial Coverage classification.
- [[.github/workflows/check-obsidian-conventions.yml|CI workflow]]:1-22 — existing CI substrate for validation gates.
- [[AGENTS|AGENTS.md]]:69-78 — Rule 7 validation gates.
- [[AGENTS|AGENTS.md]]:93-100 — Rule 9 explicit human approval for publishing.
- [[docs/canonical/plan-execute-verify|Plan-Execute-Verify]]:28-74 — analogous three-phase execution pattern.

---

*Created: 2026-06-14 | From: Quarto Book Publishing pattern classification (Missing: 5, 7 | Partial: 6, 8) | Precedence: canonical*
