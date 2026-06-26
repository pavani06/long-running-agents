---
title: "Governance Context Injection for PII Prevention"
type: canonical
aliases: ["PII prevention", "governance injection", "data catalog PII", "compliance audit for agents"]
tags: ["governanca", "production", "evals", "error-handling"]
last_updated: 2026-06-26
relates-to: ["[[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]", "[[docs/canonical/compartmented-evaluation-architecture|Compartmented Evaluation Architecture]]", "[[docs/canonical/eval-tier-stratification|Eval Tier Stratification]]", "[[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]]", "[[docs/canonical/structured-generation-constraint-validation-circuit|Structured Generation Constraint Validation Circuit]]"]
---

# Governance Context Injection for PII Prevention

**Type:** canonical
**Status:** active
**Source:** analysis/2026-06-26-the-production-ai-playbook-deploying-agents-at-enterprise-sc/
**Classification:** Missing (P0, Low)
**Precedence:** document-level 2 (canonical) per `docs/system-of-record.md`

---

## Problem

Agents access enterprise data catalogs containing PII (SSN, phone, address, credit card numbers, customer names) but the model has no awareness of which fields are sensitive. The model treats all data as safe to include in responses, causing PII breaches that would be compliance incidents in production.

Traditional approaches — post-generation PII scanning — catch breaches after the response is generated, which is a safety net, not a prevention mechanism. The model already exposed the data; the scan can only flag and block delivery.

The repo has zero PII-related infrastructure. No data catalog PII tagging, no governance context injection into prompts, no deterministic PII detection, no audit records for sensitive data queries. The constraint-anchored evaluation and compartmented evaluation patterns provide general-purpose evaluation guards, but neither addresses domain-specific governance injection for PII prevention.

## Solution

Inject governance context — the list of PII-tagged fields accessed by the current query — into the prompt **before** the model generates its response. This makes the model aware of which fields are sensitive and must not be exposed, enabling the model to compose safe references (e.g., "your account ending in XXXX") instead of exposing raw PII.

### Mechanism

The system operates in three layers, executed in sequence for every query:

#### Layer 1: Before-Generation Injection (Prevention)

1. **Query arrives** — the orchestration layer identifies which data catalog tables/fields the query will access.
2. **PII lookup** — the data catalog returns the PII tags for every field in the query scope.
3. **Governance context injection** — a structured block is injected into the prompt before model generation:

```
[GOVERNANCE CONTEXT]
The following fields accessed by this query contain PII and MUST NOT be exposed in the response:
- customer.ssn: Personally Identifiable Information (Social Security Number)
- customer.phone: Personally Identifiable Information (Phone Number)
- customer.email: Personally Identifiable Information (Email)

When referencing these fields, use safe partial formats:
- SSN: "XXX-XX-1234" → "ending in 1234"
- Phone: "(555) 123-4567" → "on file"
- Email: "j***@domain.com" → masked display
[/GOVERNANCE CONTEXT]
```

4. **Model generates response** with awareness of which fields are sensitive.

#### Layer 2: Post-Generation Deterministic Scan (Safety Net)

After generation, a deterministic scanner checks the response against PII regex patterns (SSN, phone, email, credit card). If PII is detected, the response is blocked and the incident is logged. This is a safety net for cases where the model ignores governance context.

#### Layer 3: Audit Record

Every query's governance context and PII scan result is logged for compliance auditors. The audit record includes:
- Query ID and timestamp
- Fields accessed (with PII tags)
- Governance context injected into prompt
- PII scan result (pass/fail)
- If fail: the detected pattern and the blocked response

### Data Catalog Dependency

This pattern requires a data catalog with PII tagging (Unity Catalog or equivalent). PII tags in the catalog propagate through queries into prompts — no manual annotation of prompts per use case. The governance context travels with the data.

**If the organization lacks a PII-tagged data catalog**, a minimum viable catalog can be bootstrapped by tagging the most sensitive fields (SSN, credit card, phone) manually and expanding coverage over time.

## Implementation in this repo

### What already exists

**NOT_FOUND across all evidence sources.** Zero PII-related canonical docs, curriculum materials, analysis documents, ADRs, or skill implementations. The closest general-purpose patterns are:

- **Constraint-Anchored Evaluation** (`constraint-anchored-evaluation.md`) — anchors evaluation to explicit constraint lists. Could theoretically include PII constraints, but no PII-specific constraint taxonomy exists.
- **Compartmented Evaluation Architecture** (`compartmented-evaluation-architecture.md`) — seals builder from validator surfaces. The compartmentation principle could be applied to PII governance, but no PII-specific compartmentation is defined.
- **Structured Generation Constraint Validation Circuit** (`structured-generation-constraint-validation-circuit.md`) — circuit of generation + constraint validation with repair, rejection, and audit. The circuit pattern is applicable but no PII constraints are wired in.

### What is missing

1. **No PII tagging** in any data catalog — the repo has no data catalog infrastructure at all.
2. **No governance metadata injection** into agent prompts — zero mechanism to inform the model which fields are sensitive.
3. **No pre-generation deterministic PII detection** via NER or regex — no Layer 1 scanning infrastructure.
4. **No post-generation PII scan** as safety net.
5. **No audit record** of governance context per query for compliance auditors.
6. **No data catalog PII taxonomy** — no classification of fields as PII, SPI (Sensitive Personal Information), or public.
7. **No skill implementing PII detection**, governance context injection, or compliance audit.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Prevents PII breaches before generation — the model knows which fields are sensitive and can compose safe responses | Requires a data catalog with PII tagging — organizations without mature data governance must build this first |
| 47 PII breaches caught in testing phase at Databricks; without this pattern, each would have been a compliance incident | PII tagging coverage gaps: a field not tagged as PII in the catalog will not be injected into the prompt |
| Governance context travels with the data: PII tags in the catalog propagate automatically — no per-use-case manual annotation | Model may still expose PII despite governance context — the injection is a prompt instruction, not a hard constraint |
| Deterministic PII scan (Layer 2) provides a safety net even if the model ignores governance context | Post-generation PII scan catches breaches but does not prevent them — the response has already been generated |

## Relationship to Other Patterns

- **Extends:** Constraint-Anchored Evaluation — PII governance is a domain-specific constraint category that the evaluation framework can verify.
- **Complements:** Compartmented Evaluation Architecture — governance context injection is a compartmentation mechanism: the builder (model) receives PII awareness, the validator (deterministic scan) verifies compliance without sharing the model's internal state.
- **Integrates with:** Structured Generation Constraint Validation Circuit — the circuit's repair/rejection/audit mechanics handle PII scan failures deterministically.
- **Feeds into:** Production Failure Regression Flywheel — PII scan failures become regression cases in the eval dataset, preventing recurrence.
- **Uses:** Eval Tier Stratification — PII scanning is a fast tier (Layer 1 deterministic) eval that should run on every query.

## References

- `docs/analysis/2026-06-26-the-production-ai-playbook-deploying-agents-at-enterprise-sc/2026-06-26-the-production-ai-playbook-deploying-agents-at-enterprise-sc-patterns.md:324` — extracted pattern definition.
- `docs/analysis/2026-06-26-the-production-ai-playbook-deploying-agents-at-enterprise-sc/2026-06-26-the-production-ai-playbook-deploying-agents-at-enterprise-sc-classification.yaml:385` — Missing classification (P0, Low).
- `docs/canonical/constraint-anchored-evaluation.md` — general-purpose constraint-based evaluation.
- `docs/canonical/compartmented-evaluation-architecture.md` — compartmentation between builder and validator.
- `docs/canonical/structured-generation-constraint-validation-circuit.md` — circuit with repair, rejection, and audit.

---

*Created: 2026-06-26 | From: Production AI Playbook classification (Batch B) | Precedence: canonical*
