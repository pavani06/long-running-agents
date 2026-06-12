---
title: "Reusable Agentic Patterns from The Trap Spec-Driven Development Is Setting"
type: analysis
date: 2026-06-11
aliases: ["SDD trap patterns", "manual brake patterns", "IDSD patterns", "agentic value gate patterns"]
tags: ["agentes-orquestracao", "agentic-coding", "spec-driven-development", "decision-discipline", "harness-engineering", "governanca"]
relates-to: ["[[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis|The Trap SDD Analysis]]", "[[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent Operating System]]", "[[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]]", "[[docs/canonical/failure-pattern-classification-loop|Failure Pattern Classification Loop]]", "[[docs/canonical/grill-me-alignment-interview|Grill-Me Alignment Interview]]", "[[docs/canonical/generator-evaluator|Generator-Evaluator]]"]
sources: ["[[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis|The Trap SDD Analysis]]"]
---

# Reusable Agentic Patterns from The Trap Spec-Driven Development Is Setting

Scope: extracted from `docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis.md`. Only patterns that can be reused in agentic systems, long-running agent workflows, or agent harness governance are included; broad economic commentary and generic management observations are excluded unless they translate into an operational agent workflow.

## 1. Value-Gated Agent Control Loop

- **name:** Value-Gated Agent Control Loop
- **problem_solved:** Agent harnesses often govern how an agent builds, tests, and repairs, but not whether the agent should build the requested artifact at all.
- **inputs:**
  - Candidate task, feature, or agent run request.
  - Stated user or business intent.
  - Expected user consequence if the artifact never exists.
  - Cost, debt, and maintenance assumptions for the build.
  - Named decision owner for approval or refusal.
- **outputs:**
  - Build, experiment, defer, or stop decision before execution.
  - Intent statement attached to the agent task.
  - Scope constraints for the execution agent when the build is approved.
  - Refusal or deferral rationale when the build is not approved.
- **benefits:**
  - Separates the agentic coding engine from the value brake that governs it.
  - Prevents build requests from self-approving just because generation is cheap.
  - Gives long-running workflows an auditable answer to why the agent is working.
- **limitations:**
  - Requires human or business judgment that the harness cannot infer alone.
  - Adds friction to trivial changes if applied without a bypass policy.
  - Low-quality intents can still approve low-value work.
- **source_reference:**
  - /mnt/c/Users/pavan/long-running-agents/docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis.md:41
  - /mnt/c/Users/pavan/long-running-agents/docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis.md:48
  - /mnt/c/Users/pavan/long-running-agents/docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis.md:175

## 2. Manual Brake Question Gate

- **name:** Manual Brake Question Gate
- **problem_solved:** Cheap token-driven builds remove the economic brake and collapsed SDD removes the methodological brake, so the workflow no longer forces the value question.
- **inputs:**
  - Proposed agent build or continuation request.
  - Answer to who needs the artifact and what breaks if it never exists.
  - Answer to whether the team would still build it if it cost a week of engineering time.
  - Person or role who owns saying no.
- **outputs:**
  - Recorded answers to the three brake questions.
  - Classification as experiment, committed build, defer, or stop.
  - Named owner accountable for refusal or continuation.
- **benefits:**
  - Reintroduces a value and cost gate when real token prices do not force one.
  - Filters feature inflation before an agent spends cycles implementing it.
  - Makes ownerless decisions visible instead of letting them drift forward.
- **limitations:**
  - Can become a checklist if the answers are not challenged.
  - Relies on authority to enforce a no decision under delivery pressure.
  - The cost proxy is approximate and should not replace real cost telemetry.
- **source_reference:**
  - /mnt/c/Users/pavan/long-running-agents/docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis.md:62
  - /mnt/c/Users/pavan/long-running-agents/docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis.md:68
  - /mnt/c/Users/pavan/long-running-agents/docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis.md:69
  - /mnt/c/Users/pavan/long-running-agents/docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis.md:70

## 3. Intent-First Spec Loop

- **name:** Intent-First Spec Loop
- **problem_solved:** Specs can become detailed instructions for what the agent can build instead of a testable expression of what should be valuable.
- **inputs:**
  - Value intents from the person or role accountable for the outcome.
  - Constraints and non-goals that shape acceptable solutions.
  - Specs derived after the intent is known.
  - Verification criteria for whether the intent was satisfied.
- **outputs:**
  - Intent-backed specs.
  - Agent task contracts derived from value before implementation detail.
  - Evaluation criteria that test whether the built artifact served the intent.
- **benefits:**
  - Preserves the value decision before the agent begins execution.
  - Gives implementation agents a clearer target than a raw feature request.
  - Makes specs instruments for testing intent rather than justifying construction.
- **limitations:**
  - Requires someone to articulate intent before the spec is written.
  - The source describes IDSD at a high level, so implementation details need local design.
  - Exploratory work still needs explicit experiment framing when intent is uncertain.
- **source_reference:**
  - /mnt/c/Users/pavan/long-running-agents/docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis.md:50
  - /mnt/c/Users/pavan/long-running-agents/docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis.md:52
  - /mnt/c/Users/pavan/long-running-agents/docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis.md:141

## 4. Continue Decision Checkpoint

- **name:** Continue Decision Checkpoint
- **problem_solved:** Long-running agent work can keep moving from one build to the next after prototyping has stopped discovering value and become the work itself.
- **inputs:**
  - Current iteration output and verification evidence.
  - Evidence that something reached a user or produced a return signal.
  - Stop criteria defined before the experiment continues.
  - Current debt, cost, and maintenance snapshot.
- **outputs:**
  - Continue, pivot, stop, or archive decision at the iteration boundary.
  - Updated intent and scope if continuation is approved.
  - Archived experiment or cleanup work if continuation is denied.
- **benefits:**
  - Encourages fast prototypes without allowing indefinite build loops.
  - Places the hard decision at the dangerous verb, continue, not at the first build.
  - Limits carry debt from agent-created artifacts that never reach users.
- **limitations:**
  - Needs a regular cadence in the orchestrator or project workflow.
  - Premature stop decisions can kill discovery whose value signal is delayed.
  - Weak return metrics can make the checkpoint subjective.
- **source_reference:**
  - /mnt/c/Users/pavan/long-running-agents/docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis.md:72
  - /mnt/c/Users/pavan/long-running-agents/docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis.md:76
  - /mnt/c/Users/pavan/long-running-agents/docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis.md:108
  - /mnt/c/Users/pavan/long-running-agents/docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis.md:151
  - /mnt/c/Users/pavan/long-running-agents/docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis.md:161

## 5. Owner-of-No Role

- **name:** Owner-of-No Role
- **problem_solved:** Builder-heavy agent teams naturally drift toward construction when no person or agent role is explicitly responsible for refusing low-value work.
- **inputs:**
  - Initiative or agent run proposal.
  - Named owner with authority to refuse, defer, or demand intent.
  - Refusal criteria and escalation path.
  - Alternative intents or narrower experiments the owner can provide.
- **outputs:**
  - Explicit approve, refuse, defer, or experiment decision.
  - Rationale attached to the task record.
  - Intent alternatives when the original request is rejected.
- **benefits:**
  - Turns saying no into a designed role instead of an accidental act of courage.
  - Gives the harness a concrete decision point before autonomous execution.
  - Makes refusal constructive by pairing no with better intents.
- **limitations:**
  - Can be bypassed if senior builders keep private token workflows outside the gate.
  - Creates cultural tension when the team identifies speed with value.
  - Becomes a bottleneck if ownership is not distributed across domains.
- **source_reference:**
  - /mnt/c/Users/pavan/long-running-agents/docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis.md:90
  - /mnt/c/Users/pavan/long-running-agents/docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis.md:94
  - /mnt/c/Users/pavan/long-running-agents/docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis.md:159

## 6. Deferred Ledger for Agentic Work

- **name:** Deferred Ledger for Agentic Work
- **problem_solved:** Agentic workflows can accumulate skill debt, dependence debt, and carry debt while token prices and generation costs look artificially cheap.
- **inputs:**
  - Agent run history and generated artifact inventory.
  - Token price assumptions and repricing scenarios.
  - Human build-or-dont-build decision records.
  - Tool dependency surface and quality monitoring data.
  - Maintenance, security, and ownership burden for shipped or retained artifacts.
- **outputs:**
  - Ledger entries for skill, dependence, and carry debt.
  - Exposure view for what breaks when generation becomes expensive or degraded.
  - Mitigation decisions such as stop, simplify, retire, evaluate, or rehearse judgment.
- **benefits:**
  - Makes hidden agentic risk visible before repricing or degradation exposes it.
  - Treats the future burden as a current workflow decision, not only a budget surprise.
  - Connects cost, quality, dependency, and maintenance risk in one operating artifact.
- **limitations:**
  - Debt estimates are approximate and need review rather than blind automation.
  - Can become bookkeeping if not tied to stop or mitigation decisions.
  - Requires instrumentation across costs, outputs, owners, and evals.
- **source_reference:**
  - /mnt/c/Users/pavan/long-running-agents/docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis.md:31
  - /mnt/c/Users/pavan/long-running-agents/docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis.md:35
  - /mnt/c/Users/pavan/long-running-agents/docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis.md:36
  - /mnt/c/Users/pavan/long-running-agents/docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis.md:37
  - /mnt/c/Users/pavan/long-running-agents/docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis.md:39

## 7. Silent Degradation Sentinel Evals

- **name:** Silent Degradation Sentinel Evals
- **problem_solved:** AI coding tools can degrade subtly for weeks, causing agent teams to ship against a broken instrument without recognizing the tool as the failure source.
- **inputs:**
  - Representative golden tasks for the agentic workflow.
  - Baseline outputs or expected quality thresholds.
  - Independent evaluator, rubric, or regression suite.
  - Current model and tool outputs sampled on a cadence.
- **outputs:**
  - Degradation signal when quality drifts from baseline.
  - Tool-health trend for critical agent dependencies.
  - Fallback, escalation, or freeze trigger when sentinel checks fail.
- **benefits:**
  - Detects dependence debt before it appears as user-visible defects.
  - Helps separate model/tool degradation from local implementation mistakes.
  - Gives long-running agents a recurring health check for their generator substrate.
- **limitations:**
  - Sentinel evals only cover the sampled task distribution.
  - Baselines can become stale as models, tasks, and expectations evolve.
  - False positives can interrupt legitimate model behavior changes.
- **source_reference:**
  - /mnt/c/Users/pavan/long-running-agents/docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis.md:124
  - /mnt/c/Users/pavan/long-running-agents/docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis.md:126
  - /mnt/c/Users/pavan/long-running-agents/docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis.md:155

## 8. Accidental Brake Replacement

- **name:** Accidental Brake Replacement
- **problem_solved:** Useful discipline may survive only inside slow bureaucracy such as procurement, security, or rollout review, which was not designed as the agentic value brake and can be removed accidentally.
- **inputs:**
  - Inventory of existing approval, procurement, security, and rollout gates.
  - Map of agent access paths that can bypass those gates.
  - Value, risk, and release criteria the organization actually wants to preserve.
  - Authority model for approving exceptions.
- **outputs:**
  - Explicit harness or workflow gates that replace accidental bureaucracy.
  - Policy for when agents can prototype, continue, ship, or require human approval.
  - Audit trail showing which intentional gate replaced each accidental one.
- **benefits:**
  - Preserves the useful brake while removing unnecessary accidental slowness.
  - Makes governance robust against an executive mandate to simply move faster.
  - Reduces hidden risk from private builder pockets outside enterprise gates.
- **limitations:**
  - Can overformalize exploration if every gate is copied directly from bureaucracy.
  - Needs executive support because it changes who may say yes or no.
  - Informal autonomous workflows can still evade the replacement gate.
- **source_reference:**
  - /mnt/c/Users/pavan/long-running-agents/docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis.md:54
  - /mnt/c/Users/pavan/long-running-agents/docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis.md:56
  - /mnt/c/Users/pavan/long-running-agents/docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis.md:88
  - /mnt/c/Users/pavan/long-running-agents/docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis.md:157

## 9. Judgment Exercise Cadence

- **name:** Judgment Exercise Cadence
- **problem_solved:** Human build-or-dont-build judgment atrophies when agentic systems make most builds feel too cheap to question.
- **inputs:**
  - Backlog of cheap-build candidates.
  - Historical approve, reject, continue, and stop decisions.
  - Outcome evidence from completed or stopped work.
  - Review ritual that forces explicit tradeoff discussion.
- **outputs:**
  - Recorded build, dont-build, continue, and stop rationales.
  - Calibration examples for future owners and agents.
  - Rejected or narrowed work that preserves judgment muscle.
- **benefits:**
  - Keeps the human value-decision skill active even when generation is abundant.
  - Produces examples that can train owners, reviewers, and agent prompts.
  - Reduces skill debt by making refusal a practiced behavior.
- **limitations:**
  - Consumes scarce leadership attention even when no immediate cost is visible.
  - Decision quality is hard to measure without delayed outcome tracking.
  - Rituals can be gamed if teams pre-justify everything they want to build.
- **source_reference:**
  - /mnt/c/Users/pavan/long-running-agents/docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis.md:35
  - /mnt/c/Users/pavan/long-running-agents/docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis.md:120
  - /mnt/c/Users/pavan/long-running-agents/docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis.md:122
  - /mnt/c/Users/pavan/long-running-agents/docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis.md:153

## 10. Carry Debt Sunset Gate

- **name:** Carry Debt Sunset Gate
- **problem_solved:** Software that was cheap for an agent to create becomes inventory that must be maintained, secured, understood, and eventually re-priced over its lifetime.
- **inputs:**
  - Agent-created artifact or feature inventory.
  - Expected user, owner, and value hypothesis for each artifact.
  - Security, maintenance, and operational burden estimate.
  - Expiration date or review trigger.
- **outputs:**
  - Keep, retire, archive, or promote decision for each artifact.
  - Named maintenance owner for retained artifacts.
  - Cleanup tasks for artifacts that did not justify their carry cost.
- **benefits:**
  - Prevents cheap prototypes from quietly becoming permanent production burden.
  - Keeps long-running agent output aligned with owned, maintained assets.
  - Makes deletion and archival normal parts of the agentic workflow.
- **limitations:**
  - Requires an accurate inventory of what agents created or changed.
  - Retirement can be politically difficult after stakeholders become attached.
  - Some artifacts reveal value only after a longer observation window.
- **source_reference:**
  - /mnt/c/Users/pavan/long-running-agents/docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis.md:37
  - /mnt/c/Users/pavan/long-running-agents/docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis.md:106
  - /mnt/c/Users/pavan/long-running-agents/docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis.md:149
