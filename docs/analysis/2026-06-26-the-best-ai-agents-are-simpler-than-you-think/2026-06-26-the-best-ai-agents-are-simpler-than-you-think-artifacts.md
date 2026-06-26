# Artifacts Manifest: The best AI agents are simpler than you think

**Source**: LangChain Max Agency — Zack Reno Wedeen (Sierra)
**Date**: 2026-06-26
**Type**: artifact-manifest

---

## Summary

| Category | Count | Priority |
|---|---|---|
| Canonical Docs | 10 | P0: 4, P1: 6 |
| Skills | 4 | P0: 4 |
| Exercises | 4 | P0: 4 |
| **Total Created** | **18** | |
| Skipped | 6 | See below |

---

## Artifacts Created

### Canonical Docs (10)

| # | Pattern | File | Priority | Lines |
|---|---------|------|----------|-------|
| 1 | Multi-Provider Model Routing | `docs/canonical/multi-provider-model-routing.md` | P0 | ~96 |
| 2 | Confidence-Gated Continual Learning | `docs/canonical/confidence-gated-continual-learning.md` | P0 | ~101 |
| 3 | Regulated Data Boundary | `docs/canonical/regulated-data-boundary.md` | P0 | ~98 |
| 4 | Auth-Coupled Memory Architecture | `docs/canonical/auth-coupled-memory-architecture.md` | P0 | ~101 |
| 5 | Task-Routed Model Tiering | `docs/canonical/task-routed-model-tiering.md` | P1 | ~99 |
| 6 | Temporal Context Injection | `docs/canonical/temporal-context-injection.md` | P1 | ~103 |
| 7 | File-System Materialization | `docs/canonical/file-system-materialization.md` | P1 | ~104 |
| 8 | Always-On Monitoring with Human Triage | `docs/canonical/always-on-monitoring-human-triage.md` | P1 | ~108 |
| 9 | Model-Switch-Driven Eval Hardening | `docs/canonical/model-switch-driven-eval-hardening.md` | P1 | ~112 |
| 10 | Three-Tier Memory Persistence | `docs/canonical/three-tier-memory-persistence.md` | P1 | ~106 |

### Skills (4)

| # | Pattern | File | Lines |
|---|---------|------|-------|
| 1 | Multi-Provider Model Routing | `.opencode/skills/multi-provider-routing/SKILL.md` | ~193 |
| 2 | Confidence-Gated Continual Learning | `.opencode/skills/confidence-gated-learning/SKILL.md` | ~194 |
| 3 | Regulated Data Boundary | `.opencode/skills/regulated-data-boundary/SKILL.md` | ~193 |
| 4 | Auth-Coupled Memory Architecture | `.opencode/skills/auth-coupled-memory/SKILL.md` | ~212 |

### Exercises (4)

| # | Pattern | File | Level | Lines |
|---|---------|------|-------|-------|
| 1 | Multi-Provider Model Routing | `curriculum/02-nivel-2-practical-patterns/exercises/exercise-multi-provider-routing.md` | N2 | ~627 |
| 2 | Confidence-Gated Continual Learning | `curriculum/02-nivel-2-practical-patterns/exercises/exercise-confidence-gated-learning.md` | N2 | ~587 |
| 3 | Regulated Data Boundary | `curriculum/04-nivel-4-koda-specific/exercises/exercise-regulated-data-boundary.md` | N4 | ~660 |
| 4 | Auth-Coupled Memory Architecture | `curriculum/02-nivel-2-practical-patterns/exercises/exercise-auth-coupled-memory.md` | N2 | ~509 |

---

## Integration Map

| Artifact | Phase 5 Surface to Update |
|---|---|
| `docs/canonical/multi-provider-model-routing.md` | `system-of-record.md`: add to "Agentes e orquestração" section |
| `docs/canonical/confidence-gated-continual-learning.md` | `system-of-record.md`: add to "Agentes e orquestração" section |
| `docs/canonical/regulated-data-boundary.md` | `system-of-record.md`: add to "Agentes e orquestração" + "Governança" sections |
| `docs/canonical/auth-coupled-memory-architecture.md` | `system-of-record.md`: add to "Agentes e orquestração" section |
| `docs/canonical/task-routed-model-tiering.md` | `system-of-record.md`: add to "Agentes e orquestração" section |
| `docs/canonical/temporal-context-injection.md` | `system-of-record.md`: add to "Context Engineering" section |
| `docs/canonical/file-system-materialization.md` | `system-of-record.md`: add to "Harness Engineering" section |
| `docs/canonical/always-on-monitoring-human-triage.md` | `system-of-record.md`: add to "Evals" + "Production" sections |
| `docs/canonical/model-switch-driven-eval-hardening.md` | `system-of-record.md`: add to "Evals" section |
| `docs/canonical/three-tier-memory-persistence.md` | `system-of-record.md`: add to "Context Engineering" section |
| `.opencode/skills/multi-provider-routing/` | `system-of-record.md`: add to skills catalog |
| `.opencode/skills/confidence-gated-learning/` | `system-of-record.md`: add to skills catalog |
| `.opencode/skills/regulated-data-boundary/` | `system-of-record.md`: add to skills catalog |
| `.opencode/skills/auth-coupled-memory/` | `system-of-record.md`: add to skills catalog |
| `curriculum/02-nivel-2-practical-patterns/exercises/exercise-multi-provider-routing.md` | `curriculum/INDEX.md` + `curriculum/README.md` + `curriculum/MASTER_PLAN.md` |
| `curriculum/02-nivel-2-practical-patterns/exercises/exercise-confidence-gated-learning.md` | `curriculum/INDEX.md` + `curriculum/README.md` + `curriculum/MASTER_PLAN.md` |
| `curriculum/04-nivel-4-koda-specific/exercises/exercise-regulated-data-boundary.md` | `curriculum/INDEX.md` + `curriculum/README.md` + `curriculum/MASTER_PLAN.md` |
| `curriculum/02-nivel-2-practical-patterns/exercises/exercise-auth-coupled-memory.md` | `curriculum/INDEX.md` + `curriculum/README.md` + `curriculum/MASTER_PLAN.md` |

---

## Skipped Patterns

| Pattern | Reason | Classification |
|---|---|---|
| Cognitive Process Parallelization | Voice-specific — outside coding-agent harness scope | Missing |
| Monolith-First Agent Architecture | Contradicts repo's generator-evaluator split philosophy | Missing |
| Dual-Loop Harness Architecture | Partial Coverage Medium — deferred | Partial Coverage |
| Speculative Execution for Latency Reduction | Partial Coverage Medium — prefetch exists, not generalized | Partial Coverage |
| Recursive AI Verification Chains | Partial Coverage Medium — 3-layer eval exists, recursive not needed | Partial Coverage |
| Model-First Interface Design (80/20) | Partial Coverage Medium — pieces exist, unified framework deferred | Partial Coverage |

---

## Phase 4 Gate

- [x] 4 Missing patterns (P0) have canonical doc + skill + exercise
- [x] 6 Partial Coverage High (P1) have canonical docs
- [x] No artifacts created for Already Exists patterns (2)
- [x] Skipped patterns documented with justification
- [x] Artifacts manifest generated (YAML + MD)
- [x] Integration Map connects each artifact to Phase 5 surfaces
