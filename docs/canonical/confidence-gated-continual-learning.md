---
title: "Confidence-Gated Continual Learning"
type: canonical
status: draft
source: "LangChain Max Agency — Zack Reno Wedeen (Sierra)"
date: 2026-06-26
tags: ["agentes-orquestracao", "evals", "governanca"]
aliases: ["confidence-gated deployment", "ghostwriter agent", "auto-deploy with confidence threshold", "FYI-vs-approval deployment"]
relates-to: ["[[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent Operating System]]", "[[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]]", "[[docs/canonical/garbage-collection-day-meta-loop|Garbage Collection Day Meta-Loop]]", "[[docs/canonical/failure-pattern-classification-loop|Failure Pattern Classification Loop]]", "[[docs/canonical/on-policy-rollout-feedback-loop|On-Policy Rollout Feedback Loop]]"]
---

# Confidence-Gated Continual Learning

**Type:** canonical
**Status:** draft
**Source:** LangChain Max Agency — Zack Reno Wedeen (Sierra)
**Classification:** Missing (P0)
**Precedence:** document-level 2 (canonical) per [[docs/system-of-record|System of Record]]

---

## Problem

Agent improvement cycles face a tension between velocity and safety. Full automation of agent improvements risks deploying incorrect fixes to production. Full manual review of every change bottlenecks deployment velocity — every fix must pass through a human gate regardless of complexity or risk. Neither extreme is sustainable at scale.

Sierra's Ghostwriter agent (an agent that builds agents, operating on declarative agent specifications) surfaces hundreds of improvement opportunities per day from production conversation data. Manually reviewing all of them would require a team whose sole job is reviewing Ghostwriter output — defeating the purpose of automation. But blindly deploying all suggestions would risk incorrect fixes reaching customers.

The insight: not all improvements carry equal risk. A fix for contradictory knowledge articles where the correct answer is unambiguous ("the return policy is 30 days, not 14") is trivially verifiable. A suggestion to change how the agent handles payment disputes is high-stakes and requires human judgment. The missing pattern is a confidence-gated deployment pipeline that routes improvements to auto-deployment or human review based on verifiability and risk.

## Solution

A four-stage detect→suggest→review→deploy loop where the review stage is confidence-gated: high-confidence, trivially verifiable fixes skip human review and deploy with an FYI notification; lower-confidence or ambiguous fixes queue for human approval before deployment.

**Key components:**

1. **Production issue detection**: The flywheel ([[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]]) and explorer agent continuously analyze production conversations, surfacing patterns where the agent underperforms. Issues are categorized by type: contradictory knowledge, missing knowledge, incorrect reasoning, poor phrasing, etc.

2. **Ghostwriter improvement generation**: An agent that operates on declarative agent specifications (similar to coding agents operating on file systems — see [[docs/canonical/file-system-materialization|File-System Materialization for Agent Tooling]]) generates concrete fixes. The Ghostwriter doesn't suggest vague improvements; it modifies the agent specification directly, producing a diff that can be reviewed and deployed.

3. **Confidence scoring per suggestion**: Each Ghostwriter-generated improvement receives a confidence score based on fix verifiability. A knowledge base contradiction where one article is unambiguously correct (e.g., "return policy is 30 days" vs. "return policy is 14 days" — and the policy document clearly states 30) scores high. A suggestion to rephrase how the agent handles frustrated customers scores low — there's no objective correct answer.

4. **Confidence-gated routing**:
   - **High confidence, trivially verifiable** → FYI notification to the team, auto-deployed. The team can rollback if the fix was wrong, but the confidence threshold makes this rare.
   - **Low confidence or ambiguous** → Human review queue. A domain expert reviews the suggested change, approves or rejects with rationale.

**Sierra's operational posture:** Wedeen explicitly says "we don't want to pull the future forward too quickly." The primitives are built; the constraint is customer comfort, not technical capability. In e-commerce, auto-correcting a return policy date is tolerable; auto-correcting payment handling is not. The confidence gate makes this gradient explicit and operational.

**The four-stage loop in practice:**

1. **Detect**: Explorer agent or always-on monitor flags a quality issue from production conversation data.
2. **Suggest**: Ghostwriter generates a concrete fix — modifying the agent's declarative specification (Journey/DSL).
3. **Review**: Confidence scorer evaluates verifiability. High → auto-deploy path. Low → human review queue.
4. **Deploy**: Fix is applied to the agent specification, and the updated agent is released through governance gates.

## Implementation in this repo

### What already exists

NOT_FOUND across `docs/canonical/`, `curriculum/`, `system-of-record.md`, and `.opencode/skills/`.

- [[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent Operating System]] lines 28-45: Four-surface closed loop (State Intake → Priority Synthesis → Execution Routing → Feedback Writeback). Covers the outer loop but not confidence-gated deployment within the loop.
- [[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]] lines 30-41: 9-step flywheel from intake through prune. Converts failures into regression cases but does not auto-generate or auto-deploy fixes.
- [[docs/canonical/failure-pattern-classification-loop|Failure Pattern Classification Loop]] lines 35-53: 4-stage Observe→Classify→Build→Verify with 6-class root cause taxonomy. Classifies failures but does not auto-correct them.
- The flywheel daemon (`systemd`, 60s loop) processes triggers but deploys nothing — it surfaces findings for human review.

### What is missing

1. **Ghostwriter-equivalent agent**: No agent that autonomously builds agent improvements from production data. The repo's flywheel improves harness guardrails; Sierra's Ghostwriter improves agent specifications — these are fundamentally different targets.
2. **Confidence-gated deployment mechanism**: No confidence scoring, no FYI-vs-approval routing, no auto-deployment pipeline for trivially verifiable fixes.
3. **Four-stage detect→suggest→review→deploy loop**: The repo has detect (production flywheel) and review ([[docs/canonical/garbage-collection-day-meta-loop|GC Day meta-loop]]) but not suggest and deploy.

The closest concept is [[docs/canonical/garbage-collection-day-meta-loop|Garbage Collection Day Meta-Loop]] — a weekly manual review cadence that is the *opposite* of confidence-gated automation. Where Sierra automates the easy cases and escalates the hard ones, the repo's GC Day requires manual review of everything.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Accelerates deployment for unambiguous fixes that waste human time in review | Confidence scoring accuracy is the safety bottleneck — overconfident scoring risks deploying incorrect fixes silently |
| Preserves human oversight for ambiguous or high-stakes changes | Customer comfort threshold varies by domain — healthcare tolerates less automation than e-commerce; the gate must be domain-calibrated |
| Gradual adoption path: start with non-critical fixes, expand confidence threshold as scoring improves | Requires clear verifiability criteria per fix type; ambiguous criteria produce ambiguous confidence scores |
| Ghostwriter creates inspectable diffs, not black-box model updates — rollback is a git revert | Auto-deployed fixes need observability: was the fix correct? Did it cause regressions? Without monitoring, confidence-gating is blind |

## Relationship to Other Patterns

- **Requires:** [[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent Operating System]] — the outer loop that detects issues and routes work.
- **Extends:** [[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]] — adds automated suggestion and confidence-gated deployment to the regression pipeline.
- **Uses:** [[docs/canonical/failure-pattern-classification-loop|Failure Pattern Classification Loop]] — root cause classification informs confidence scoring (e.g., "contradictory knowledge" has higher confidence potential than "incorrect reasoning").
- **Complements:** [[docs/canonical/garbage-collection-day-meta-loop|Garbage Collection Day Meta-Loop]] — GC Day reviews the harness guardrails; confidence-gated learning deploys agent specification fixes. They operate on different surfaces.
- **Builds on:** [[docs/canonical/on-policy-rollout-feedback-loop|On-Policy Rollout Feedback Loop]] — the teacher-student correction loop is a supervised precursor to unsupervised Ghostwriter improvement.
- **Requires:** [[docs/canonical/file-system-materialization|File-System Materialization for Agent Tooling]] — Ghostwriter operates on declarative agent specifications materialized as file-system artifacts.

## References

-  lines 342-368 — extracted pattern with four-stage loop, confidence scoring, FYI-vs-approval routing.
-  lines 199-207 — Missing classification with NOT_FOUND evidence across all surfaces.
- Sierra transcript: "The Ghostwriter agent is an agent that builds agents. It writes agent specifications that are deployed to production." — Wedeen describing the core mechanism.
- Sierra transcript: "We don't want to pull the future forward too quickly. The primitives are built; the constraint is customer comfort, not technical capability." — Wedeen on the confidence gate philosophy.

---

*Created: 2026-06-26 | From: Sierra pattern classification | Precedence: canonical*
