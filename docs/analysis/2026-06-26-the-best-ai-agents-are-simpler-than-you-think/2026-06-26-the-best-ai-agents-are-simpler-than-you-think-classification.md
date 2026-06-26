# Classification: The best AI agents are simpler than you think

**Source**: LangChain Max Agency — Zack Reno Wedeen (Sierra)
**Date**: 2026-06-26
**Repository**: long-running-agents (ecossistema-pavan)
**Type**: classification

---

## Summary

| # | Pattern | Classification |
|---|---------|---------------|
| 1 | Task-Routed Model Tiering | Partial Coverage |
| 2 | Multi-Provider Model Routing with Capacity Resilience | Missing |
| 3 | Structured Data + LLM Hybrid Reasoning | Already Exists |
| 4 | Dual-Loop Harness Architecture | Partial Coverage |
| 5 | Cognitive Process Parallelization | Missing |
| 6 | Speculative Execution for Latency Reduction | Partial Coverage |
| 7 | Monolith-First Agent Architecture | Missing |
| 8 | Temporal Context Injection | Partial Coverage |
| 9 | File-System Materialization for Agent Tooling | Partial Coverage |
| 10 | Closed-Loop Agent Improvement Flywheel | Already Exists |
| 11 | Always-On Production Monitoring with Human Triage | Partial Coverage |
| 12 | Model-Switch-Driven Eval Hardening | Partial Coverage |
| 13 | Recursive AI Verification Chains | Partial Coverage |
| 14 | Confidence-Gated Continual Learning | Missing |
| 15 | Three-Tier Memory Persistence | Partial Coverage |
| 16 | Regulated Data Boundary | Missing |
| 17 | Auth-Coupled Memory Architecture | Missing |
| 18 | Model-First Interface Design (80/20 Rule) | Partial Coverage |

**Totals**: Already Exists: 2 | Partial Coverage: 10 | Missing: 6 | Better Implementation: 0

---

## Detailed Classification

### 1. Task-Routed Model Tiering

**Classification**: Partial Coverage

**What exists**:
- `~/.opencode/skills/analyze-and-improve/SKILL.md:67` — `model_tier.py` routes pipeline phases (3, 4, 6) to lighter model via `export AI_LIGHT_CATEGORY=quick`. Phase-level tiering, not task-level routing.
- `long-running-agents/curriculum/04-nivel-4-koda-specific/01-koda-architecture.md:845-858` — KODA assigns Opus to Generator and Sonnet to Evaluator. Agent-level model assignment, not within-turn routing.
- `long-running-agents/curriculum/10-references/model-capability-timeline.md:2312` — Industry reference: "Haiku/Flash for 80%, Opus for 15%". Documented as FAQ, not formalized pattern.

**What is missing**: No canonical doc for task-routed model tiering. No parallel dispatch mechanism for subtasks to different model tiers within the same turn. No decoupling of model selection from orchestration logic.

---

### 2. Multi-Provider Model Routing with Capacity Resilience

**Classification**: Missing

**What exists (foundational only)**:
- `long-running-agents/docs/canonical/model-switching-architecture-enterprise-eval-gate.md:22-25,62-70` — Batch migration pattern for model switching based on eval data. Not task-level multi-provider routing.
- `long-running-agents/docs/canonical/neutral-selection-layer.md:28-48` — Model-agnostic context format with vendor adapter. Foundational abstraction but no routing.

**What is missing**: No multi-provider redundancy at task level. No provider fallback mechanism. No load simulation across providers. No per-customer cloud constraint routing.

---

### 3. Structured Data + LLM Hybrid Reasoning

**Classification**: Already Exists

**Evidence** (3 layers):
- **Canonical**: `deterministic-tool-dispatch.md:33` — "Tools are not magical. Tools are JSON + deterministic code."
- **Curriculum**: `05-core-concepts/07-multi-agent-coordination.md:130-148` — "Agentes LLM vs. Serviços Determinísticos" distinction; KODA pipeline: `customer.json` + `catalog.json` → Generator LLM → WhatsApp.
- **KODA**: `01-koda-architecture.md` — Complete pipeline with deterministic services (`customer.json`, `catalog.json`) feeding LLM generators.

---

### 4. Dual-Loop Harness Architecture

**Classification**: Partial Coverage

**What exists**:
- `long-running-agents/docs/canonical/multi-level-agent-orchestration.md` — Hierarchical agent orchestration (orchestrator delegates to sub-agents). Parallel agent execution exists.
- `~/.opencode/agents/sisyphus-junior.md` — Orchestrator with background task system (`run_in_background=true`).

**What is missing**: No explicit dual-loop architecture with a fast conversational loop and a slow background processing loop. The repo has parallelism but not the loop-of-loops pattern Sierra describes.

---

### 5. Cognitive Process Parallelization

**Classification**: Missing

**Evidence**: Zero relevant results across `docs/canonical/`, `curriculum/`, `system-of-record.md`, and `.opencode/skills/`. The concept of parallelizing thinking/listening/speaking for voice agents is outside the repo's scope (coding agent harness, not voice agent harness). The repo's parallelism is task-decomposition parallelism, not cognitive-process parallelism.

---

### 6. Speculative Execution for Latency Reduction

**Classification**: Partial Coverage

**What exists**:
- `long-running-agents/docs/canonical/tiered-context-storage.md` — Prefetch pattern in context storage tiers (hot/warm/cold). Related but not the general pattern.
- `long-running-agents/docs/canonical/pre-verification-gate.md` — Validate prerequisites before expensive computation. Related concept but different domain.

**What is missing**: No general speculative execution pattern documented. The concept of computing answers before knowing if they're needed is not formalized. The voice-specific latency constraint (1-2s) that motivates this pattern is absent.

---

### 7. Monolith-First Agent Architecture

**Classification**: Missing

**Evidence**: The repo's architecture and curriculum are explicitly pro-multi-agent decomposition. Key canonical patterns (`generator-evaluator.md`, `multi-agent-fault-tolerance.md`, `multi-level-agent-orchestration.md`) all assume splitting as the default. Wedeen's "monolith loyalist" position — that better context engineering in a single agent outperforms multi-agent decomposition — contradicts the repo's generator-evaluator split philosophy.

---

### 8. Temporal Context Injection

**Classification**: Partial Coverage

**What exists** (distributed across 5+ docs):
- `long-running-agents/docs/canonical/context-engineering.md` — Context window management principles.
- `long-running-agents/docs/canonical/progressive-disclosure-agent-tool-context.md` — Progressive disclosure pattern.
- `long-running-agents/docs/canonical/tiered-context-storage.md` — Storage tiers with retrieval timing.
- `long-running-agents/curriculum/05-core-concepts/03-context-management.md` — Curriculum coverage of context management.

**What is missing**: No unified "Temporal Context Injection" pattern. The specific insight that *when* you inject context matters as much as *what* you inject is distributed across docs without explicit temporal framing. No coverage of prompt compaction incoherence risk.

---

### 9. File-System Materialization for Agent Tooling

**Classification**: Partial Coverage

**What exists**:
- `long-running-agents/curriculum/03-nivel-2-practical-patterns/08-file-based-coordination.md` — File-based coordination lesson covering the principle of materializing domain logic into file system structures. Strong curriculum coverage.
- `long-running-agents/docs/canonical/llm-as-fuzzy-compiler.md` — Code as disposable build artifact, generated code as compiler output.

**What is missing**: The term "File-System Materialization" is not used. The 80/20 framing ("meet models on their turf 80% of the time") is absent. The explicit connection to coding agents' strengths (git, grep, file systems) as the motivation for this pattern is not articulated.

---

### 10. Closed-Loop Agent Improvement Flywheel

**Classification**: Already Exists (with Ghostwriter automation gap)

**Evidence**:
- `long-running-agents/docs/canonical/closed-loop-agent-operating-system.md:26-48` — Four-surface closed loop (State Intake → Priority Synthesis → Execution Routing → Feedback Writeback) with 5-rule minimum operating contract.
- `long-running-agents/docs/canonical/production-failure-regression-flywheel.md:30-41` — 9-step flywheel: intake → capture → privacy → label → deduplicate → tier → backfill → link → prune.
- `long-running-agents/docs/canonical/failure-pattern-classification-loop.md:35-53` — 4-stage Observe→Classify→Build→Verify with 6-class root cause taxonomy.
- `long-running-agents/docs/canonical/on-policy-rollout-feedback-loop.md:40-50` — Closing exposure-bias gap with production trajectories.
- `long-running-agents/docs/canonical/garbage-collection-day-meta-loop.md` — Weekly GC Day cadence.
- **Runtime**: `~/scripts/telemetry/flywheel-daemon.service` (60s loop), `FLYWHEEL_ALERT` gate in `AGENTS.md:343`.

**Gap**: No Ghostwriter-equivalent (agent that autonomously builds agent improvements from production data). Repo's flywheel improves harness guardrails; Sierra's improves agent specifications.

**Note**: The repo's flywheel has arguably *more* operational depth than Sierra's — 6-class root cause taxonomy, 7-surface guardrail mapping, GC Day meta-loop, operational daemon, FLYWHEEL_ALERT injection gate. Sierra's is simpler (3 phases) but the repo's has richer operational infrastructure.

---

### 11. Always-On Production Monitoring with Human Triage

**Classification**: Partial Coverage

**What exists**:
- `long-running-agents/docs/canonical/eval-dashboard-primary-detection-surface.md:20-44` — Always-on quality dashboard as primary detection surface. Detection-vs-diagnosis distinction.
- Flywheel daemon (systemd, 60s loop) — operational monitoring via `flywheel-health.sh`.
- SLO checker (`budget-slo-check.sh`) — burn rate alerts every 6h.
- `production-failure-regression-flywheel.md:28-40` — Converts production incidents into regression cases (batch/post-hoc).

**What is missing**: No human triage mechanism — no monitor definitions for quality dimensions, no flagged conversation subset, no compression ratio (10,000→5). The flywheel is fully automated without the Sierra pattern's human-in-the-loop triage step.

---

### 12. Model-Switch-Driven Eval Hardening

**Classification**: Partial Coverage

**What exists**:
- `long-running-agents/docs/canonical/model-switching-architecture-enterprise-eval-gate.md` — Full design for model-switching eval gate (Switch/Hold/Hybrid decision). Lines 48-52, 98.
- `long-running-agents/docs/canonical/neutral-selection-layer.md` — Provider-agnostic eval format.
- `long-running-agents/docs/canonical/multi-model-evaluation-council.md` — Model-diverse evaluation.

**What is missing**: The specific insight that "switching models is the best way to expose gaps in your eval suite" is not articulated. The repo's approach is a formal gate process, not the iterative, discovery-driven hardening Wedeen describes. No documented process of "switch → discover eval gap → harden eval → try again."

---

### 13. Recursive AI Verification Chains

**Classification**: Partial Coverage

**What exists**:
- `long-running-agents/docs/canonical/3-layer-evaluation-architecture.md` — Three evaluation layers (Deterministic, Semantic, Behavioral).
- `long-running-agents/docs/canonical/compartmented-evaluation-architecture.md` — Evaluation compartments for independent verification.
- `long-running-agents/docs/canonical/multi-model-evaluation-council.md` — Model-diverse evaluation council.

**What is missing**: No recursive AI-on-AI verification pattern ("verify the verifier"). The repo's layers are mechanism-based (deterministic regex, semantic similarity, behavioral LLM), not recursive LLM chains. The Sierra insight — chain 90% solutions to achieve multi-nine reliability — is not formalized.

---

### 14. Confidence-Gated Continual Learning

**Classification**: Missing

**Evidence**: NOT_FOUND across `docs/canonical/`, `curriculum/`, `system-of-record.md`, and `.opencode/skills/`. No confidence-gated deployment mechanism. No Ghostwriter-equivalent agent. No four-stage detect→suggest→review→deploy loop. No FYI-vs-approval confidence threshold.

The closest concept is `garbage-collection-day-meta-loop.md` (weekly manual review), which is the opposite of confidence-gated automation.

---

### 15. Three-Tier Memory Persistence

**Classification**: Partial Coverage

**What exists** (storage latency tiers):
- `long-running-agents/docs/canonical/tiered-context-storage.md` — Hot/warm/cold storage tiers.
- `long-running-agents/docs/canonical/external-state-persistence.md` — External state persistence.
- `long-running-agents/docs/canonical/addressable-memory-catalog.md` — Addressable memory.
- `long-running-agents/docs/canonical/epistemic-memory-graph.md` — Epistemic memory graph.

**What is missing**: The three-tier user/builder/agent schema gradient: Tier 1 (user-initiated "remember this"), Tier 2 (builder-defined "birthdays matter"), Tier 3 (agent-decided implicit memory). The repo has storage tiers but not the authority gradient that maps to who decides what to persist.

---

### 16. Regulated Data Boundary

**Classification**: Missing

**Evidence**: The closest match is `long-running-agents/docs/canonical/governance-context-injection-pii-prevention.md` — policy-based PII prevention via context injection rules. This is a *policy* control (filter PII from context), not an *architectural* isolation pattern (separate infrastructure cluster for regulated data). The Sierra pattern — PCI DSS Level 1 isolated payment infrastructure where payment data never touches an LLM — has no equivalent.

---

### 17. Auth-Coupled Memory Architecture

**Classification**: Missing

**Evidence**: NOT_FOUND. No auth-to-memory coupling mechanism. No authentication confidence score. No memory sensitivity gating by authentication level (greeting by name = low auth bar, SSN-level memory = high auth bar). The repo's memory patterns (`addressable-memory-catalog.md`, `epistemic-memory-graph.md`, `canonical-context/SKILL.md`) treat memory as a purely technical problem without the identity/trust dimension.

---

### 18. Model-First Interface Design (80/20 Rule)

**Classification**: Partial Coverage

**What exists**:
- `long-running-agents/docs/canonical/llm-as-fuzzy-compiler.md` — Code as compiler output, models as fuzzy compilers.
- `long-running-agents/docs/canonical/resolver-disclosure-skill-discovery.md` — Skill discovery via resolver pattern (the 20%: "teach models your way").
- `long-running-agents/docs/canonical/context-engineering.md` — Context engineering principles.

**What is missing**: No explicit 80/20 rule framing ("meet models on their turf 80% of the time, teach them your way 20%"). No file-system materialization framing. The repo has the individual ideas but not the unified decision framework Wedeen describes: "reframe the problem into something models understand vs. build a skill and inject context."

---

## Key Insights

1. **Strongest match**: Structured Data + LLM Hybrid Reasoning and Closed-Loop Flywheel are the only two patterns with full coverage — the repo has canonical docs, curriculum lessons, and operational implementations for both.

2. **Biggest gaps (6 Missing)**: Multi-Provider Routing, Cognitive Parallelization, Monolith-First, Confidence-Gated Learning, Regulated Data Boundary, Auth-Coupled Memory. These represent areas where Sierra's production experience has discovered patterns not yet relevant to a coding-agent harness ecosystem.

3. **Partial Coverage patterns (10)**: The repo has foundational concepts for most patterns but lacks the specific framing, naming, or operational depth Sierra has developed through production deployment at Fortune 20 scale.

4. **Voice divergence**: Cognitive Process Parallelization and Speculative Execution (voice-motivated) are weakly represented because the repo focuses on coding-agent harnesses, not voice-agent harnesses. This confirms Wedeen's insight that voice and coding harnesses genuinely diverge architecturally.

5. **Implementation depth**: Where the repo covers a pattern (flywheel, eval architecture, structured data), it often has *more* operational depth than Sierra — the repo has systemd daemons, SLO checkers, GC Day meta-loops, and FLYWHEEL_ALERT injection gates that Sierra's simpler platform doesn't need at its scale.
