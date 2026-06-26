---
title: "Prompt-as-Code with Causal Change Management"
type: canonical
aliases: ["prompt as code", "causal change management", "prompt versioning", "prompt rollback", "prompt commit discipline"]
tags: ["harness", "governanca", "production", "context-engineering"]
last_updated: 2026-06-26
relates-to: ["[[docs/canonical/stable-harness-prompt|Stable Harness Prompt]]", "[[docs/canonical/application-owned-agent-control-plane|Application-Owned Agent Control Plane]]", "[[docs/canonical/llm-as-fuzzy-compiler|LLM as Fuzzy Compiler]]", "[[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]", "[[docs/canonical/3-layer-evaluation-architecture|3-Layer Evaluation Architecture]]", "[[docs/canonical/eval-driven-development-timeline|Eval-Driven Development Timeline]]", "[[docs/canonical/living-eval-dataset|Living Eval Dataset]]", "[[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]]"]
sources: []
---
# Prompt-as-Code with Causal Change Management

**Type:** canonical
**Status:** active
**Source:** The Production AI Playbook (Bhaumik, Databricks)
**Classification:** Partial Coverage
**Precedence:** document-level 2 (canonical) per `docs/system-of-record.md`

---

## Problem

Prompts are the most frequently changed and least version-controlled component of agentic systems. Generic commit messages ("updated prompt", "improved response", "fixed edge case") make rollback and debugging impossible because no one knows why a prompt changed, what failure triggered the change, or what failure the change was supposed to prevent. When a prompt change degrades quality in production, the team cannot roll back with confidence because the previous version's rationale is lost.

This is the same problem that source control and disciplined commit messages solved for code. Prompts are code — they determine the agent's behavior just as much as application logic does. They deserve the same version control discipline: every change must be traceable to its trigger, its diagnostic context, and its intended effect.

## Solution

Treat prompts as first-class versioned artifacts in a git repository, with a mandatory causal commit discipline that links every prompt change to its evidence and its intent.

### The Three Mandatory Commit Questions

Every prompt commit message must answer three questions. A prompt change that cannot answer all three is not ready to commit:

**Question 1 — WHY did it change? (Causal Trigger)**

What external event or evidence triggered this change? Must reference a specific incident, eval regression, user complaint, CSAT drop, or feature requirement — not a vague "improvement."

Examples:
- ✅ `Trigger: incident #47 — 3% CSAT drop on refund queries after model v3 update`
- ✅ `Trigger: eval regression E-12 — Layer 2 groundedness score dropped from 0.87 to 0.64`
- ❌ `Trigger: improving response quality` (no specific trigger)

**Question 2 — WHAT failure caused the change? (Diagnostic Context)**

What diagnostic evidence identified the prompt as the root cause? Must reference trace analysis, eval results, or A/B test data showing that the prompt (not the model, not the context, not the tool) is the component responsible for the failure.

Examples:
- ✅ `Diagnosis: trace analysis shows agent ignores refund_policy_2026 tool in 40% of queries; prompt instructs "be concise" which overrides tool-use instruction`
- ✅ `Diagnosis: Layer 2 eval shows "be helpful and friendly" prompt instruction causes model to add unsolicited suggestions in checkout flow`
- ❌ `Diagnosis: prompt needed improvement` (no diagnostic evidence)

**Question 3 — WHAT failure does this change address? (Predictive Intent)**

What specific failure mode is this change designed to prevent or correct? Must name the failure class and the expected behavioral change — not "makes it better."

Examples:
- ✅ `Intent: prevent tool-ignore pattern on refund queries by removing conflicting "be concise" instruction from system prompt`
- ✅ `Intent: eliminate unsolicited cross-sell suggestions in checkout by scoping "be helpful" to post-purchase only`
- ❌ `Intent: improve prompt quality` (no specific failure target)

### Causal Commit Template

```text
prompt(refund-agent): fix tool-ignore pattern on refund queries

Trigger: incident #47 — 3% CSAT drop on refund queries after model v3 update
Diagnosis: trace analysis shows agent ignores refund_policy_2026 tool in 40%
  of queries; "be concise" instruction overrides tool-use instruction
Intent: prevent tool-ignore pattern by removing conflicting "be concise"
  from system prompt; preserve conciseness in user-facing tone instruction only

Eval impact (expected): Layer 2 faithfulness should recover from 0.64 to ≥0.85
Eval impact (verified): [filled after eval suite runs on this change]
Affected categories: refund, policy-lookup
Rollback: git revert <commit-hash> — restores previous prompt with full context
```

### Prompt Rollback Infrastructure

Every prompt version must be independently deployable. The rollback mechanism:

1. **Git-based versioning:** Every prompt change is a git commit. Rollback is `git revert <commit-hash>`.
2. **Prompt repository structure:** Prompts live in a version-controlled directory (e.g., `prompts/refund-agent/system.md`, `prompts/checkout-agent/context-builder.md`) with one file per prompt component.
3. **Deploy pipeline:** Prompt deployment reads from the git repository at a specific commit. Rolling back means deploying from the previous commit.
4. **Rollback audit trail:** Every rollback is also a commit — documenting why the rollback occurred, what evidence justified it, and linking to the incident.

### Change Impact Quantification

Before a prompt change deploys to production, the eval dataset must quantify its impact:

1. **Run the full eval suite** (all three layers: deterministic, semantic, behavioral) against both the current prompt and the proposed change.
2. **Produce a diff report:** which eval cases improved, which regressed, which were unaffected.
3. **Gate on regression:** if any eval category regresses beyond its threshold, block the deploy.
4. **Record the eval baseline:** the eval report becomes part of the commit evidence — the commit message references the eval run ID.

This is the same discipline applied to code changes (run tests before merge), applied to prompt changes (run evals before deploy).

### Audit Trail

The cumulative effect of causal commits creates an audit trail that answers:

- **For any point in time:** What was the exact prompt text deployed?
- **For any prompt change:** Why was it made? What failure triggered it? What evidence justified it?
- **For any incident:** Which prompt version was active? Had it recently changed? What was the change's intent?
- **For compliance:** Regulated industries can demonstrate that every prompt change was justified by evidence, not experimentation.

## Implementation in this repo

### What already exists

The repo has strong philosophical alignment with prompt-as-code, versioned prompt contracts, and treating prompts as durable first-class assets:

- **stable-harness-prompt** (`docs/canonical/stable-harness-prompt.md:28`) defines the separation of harness prompt from reducible context payload. The harness prompt must be preserved as a first-class input with its own budget and version. Prompt changes must be deliberate, versioned, and evaluated separately from context compaction (`docs/canonical/stable-harness-prompt.md:41`).
- **application-owned-agent-control-plane** (`docs/canonical/application-owned-agent-control-plane.md:29`) defines versioned prompt contracts as part of the owned control plane, alongside structured action schema, deterministic dispatch, loop policy, persistent execution state, and intervention gates.
- **llm-as-fuzzy-compiler** (`docs/canonical/llm-as-fuzzy-compiler.md:27`) treats code as a disposable build artifact and what matters is preserving the prompts, guardrails, and documentation that produced the code — elevating prompts to durable first-class assets.
- **Owned Agent Control Loop** (`docs/canonical/owned-agent-control-loop.md:102`) explicitly identifies prompt versioning as a current gap: "system prompt is hand-authored (1800+ lines). Not versioned or eval'd as a separate component." This acknowledgment is its own evidence that the repo recognizes the need.

### What is missing

The specific 3-question causal commit discipline with mandatory trigger/diagnosis/intent is not formalized:

1. **The 3 mandatory commit questions are NOT_FOUND as a formal requirement.** The repo prescribes versioning (stable-harness-prompt, application-owned-agent-control-plane) and acknowledges the gap (owned-agent-control-loop:102) but does not define the causal commit message format that links every prompt change to its trigger, diagnostic context, and intended effect.

2. **No explicit prompt rollback infrastructure.** The concept exists implicitly (stable-harness-prompt implies rollback should be possible; versioned contracts imply previous versions can be restored) but no operational procedure documents how to roll back a prompt, what evidence is needed, or how the audit trail works.

3. **No audit trail linking prompt changes to specific incidents or eval regressions.** The flywheel daemon detects anomalies and triggers QI loops, but when a QI loop results in a prompt change, there is no formal link between the incident that triggered the loop and the prompt commit that fixed it.

4. **No pre-deploy eval gate for prompt changes.** The repo has eval infrastructure (tier stratification, eval sampling, flywheel) but no explicit rule that prompt changes must pass the eval suite before deployment with a quantified impact report.

Add:

1. A causal commit discipline (this doc) defining the 3 mandatory questions and the commit template.
2. Rollback operational procedure: how to revert a prompt, what evidence justifies rollback, how to document it.
3. An audit trail convention: every prompt commit references the incident/regression/feature that triggered it.
4. A pre-deploy eval gate for prompt changes: run the eval dataset before deploy, produce diff report, block on regression.
5. Integration with the flywheel: when a QI loop produces a prompt change, the commit must link to the flywheel finding that triggered the loop.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Debuggable prompt history: you know not just what changed but why, triggered by what, and targeting what failure mode | Requires discipline from every engineer touching prompts — cultural adoption of commit message standards is hard |
| Safe rollbacks: if a prompt change degrades quality, rollback to the previous version with full context — not guesswork | The three-question format works for reactive changes (incident-driven) but is less natural for proactive improvements (refinement) |
| Compliance: regulated industries can demonstrate that every prompt change was justified by evidence, not experimentation | Prompt version history grows unboundedly; outdated prompts should be archived but traceable, adding maintenance overhead |
| Change impact quantification: running the eval dataset before deploy catches prompt regressions before production exposure | Does not capture implicit prompt changes from model provider updates — the same prompt text may produce different behavior after a model update |
| Audit trail linking every prompt change to its trigger and intent | Adds process friction to prompt iteration; fast experimentation cycles may resist the overhead |

## Relationship to Other Patterns

- **Implements:** [[docs/canonical/stable-harness-prompt|Stable Harness Prompt]] — the causal commit discipline makes prompt versioning operational.
- **Versioned within:** [[docs/canonical/application-owned-agent-control-plane|Application-Owned Agent Control Plane]] — the control plane's versioned prompt contracts are the artifacts that causal commits govern.
- **Aligned with:** [[docs/canonical/llm-as-fuzzy-compiler|LLM as Fuzzy Compiler]] — treating prompts as durable assets alongside guardrails and docs.
- **Noted as gap by:** [[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]] — explicitly identifies prompt versioning as missing.
- **Validated by:** [[docs/canonical/3-layer-evaluation-architecture|3-Layer Evaluation Architecture]] — the eval suite that gates prompt changes before deployment.
- **Data source for:** [[docs/canonical/eval-driven-development-timeline|Eval-Driven Development Timeline]] — the eval dataset built in weeks 1-6 is the same dataset that gates prompt changes.
- **Fuels:** [[docs/canonical/living-eval-dataset|Living Eval Dataset]] — prompt regressions caught by the eval dataset become new permanent test cases.
- **Triggers:** [[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]] — when a flywheel finding triggers a prompt change, the causal commit links back to the finding.

## References

- `docs/analysis/2026-06-26-the-production-ai-playbook-deploying-agents-at-enterprise-sc/2026-06-26-the-production-ai-playbook-deploying-agents-at-enterprise-sc-patterns.md:203` — original pattern definition (Bhaumik).
- `docs/analysis/2026-06-26-the-production-ai-playbook-deploying-agents-at-enterprise-sc/2026-06-26-the-production-ai-playbook-deploying-agents-at-enterprise-sc-classification.yaml:225` — Partial Coverage classification with evidence.
- `docs/canonical/stable-harness-prompt.md:28` — separation of harness prompt from reducible context.
- `docs/canonical/stable-harness-prompt.md:41` — deliberate, versioned prompt changes evaluated separately.
- `docs/canonical/application-owned-agent-control-plane.md:29` — versioned prompt contracts in the control plane.
- `docs/canonical/owned-agent-control-loop.md:102` — explicit gap: "prompt not versioned or eval'd as separate component."
- `docs/canonical/llm-as-fuzzy-compiler.md:27` — prompts as durable first-class assets.

---

*Created: 2026-06-26 | From: Production AI Playbook classification | Precedence: canonical*
