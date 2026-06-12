---
title: "Token Economics of Gap-Filling"
type: canonical
tags: ["context-engineering", "agentes-orquestracao", "harness-engineering", "governanca", "decision-discipline"]
aliases: ["gap-filling token burn", "gap-cost attribution", "ICE gap cost", "token burn gap filling", "gap fill economics", "missing field cost", "token efficiency gap filling"]
last_updated: 2026-06-12
relates-to: ["[[docs/canonical/ice-craft-separation|ICE Craft Separation]]", "[[docs/canonical/intent-five-part-primitive|Intent as Five-Part Primitive]]", "[[docs/canonical/human-owned-expectations-boundary|Human-Owned Expectations Boundary]]", "[[docs/canonical/explicit-token-budget-ledger|Explicit Token Budget Ledger]]", "[[docs/canonical/burn-rate-runtime-forecast|Burn Rate Runtime Forecast]]", "[[docs/canonical/phase-gated-token-health-monitor|Phase-Gated Token Health Monitor]]", "[[docs/canonical/deferred-ledger-agentic-work|Deferred Ledger for Agentic Work]]", "[[docs/canonical/budget-aware-session-handoff|Budget-Aware Session Handoff]]", "[[docs/canonical/manual-brake-question-gate|Manual Brake Question Gate]]", "[[docs/canonical/generator-evaluator|Generator-Evaluator]]", "[[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis|IDSD Method Analysis]]", "[[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-patterns|IDSD Method Patterns]]", "[[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-classification|IDSD Method Classification]]", "[[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-mental-model|IDSD Method Mental Model]]"]
sources: ["[[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis|IDSD Method Analysis]]", "[[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-patterns|IDSD Method Patterns]]", "[[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-classification|IDSD Method Classification]]"]
---

# Token Economics of Gap-Filling

**Type:** canonical
**Status:** active
**Source:** analysis/2026-06-12-idsd-method/
**Classification:** Partial Coverage, High integration value
**Precedence:** document-level 2 (canonical) per [[docs/system-of-record|System of Record]]

---

## Problem

Token prices continue to drop, but the total cost per finished outcome continues to rise. The paradox is not that tokens are expensive -- it is that an agent left to fill gaps in intent, context, or expectations burns exponentially more tokens per completed outcome. A significant portion of those tokens are spent being confidently wrong before anyone notices.

The source names this as the economic paradox: "O preco por token continua caindo, mas o custo total por outcome terminado sobe. Nao porque tokens ficaram caros -- porque um agente deixado para preencher gaps queima muito mais tokens por resultado. Um numero surpreendente desses tokens vai para estar confiantemente errado antes que alguem perceba" ([[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis|analysis]]:126).

The concrete cost: three days of rework, ~$985 in tokens (150-200M tokens/day at Opus prices), real money spent creating a problem and then paying again to undo it -- all because gaps in the intent were filled silently by the agent ([[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis|analysis]]:118).

The repo has extensive token economics infrastructure: per-call ledgers, burn-rate forecasting, health monitoring, and strategic debt tracking. But none of these mechanisms can attribute token costs to specific information gaps or measure the exponential penalty of filling ICE gaps during execution. The repo tracks how much you spend and at what rate, but cannot explain why ([[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-classification|classification]]:228-248).

## Solution

Build a gap-cost attribution layer on top of the existing token instrumentation. Instead of just measuring raw token consumption, measure which tokens were spent filling gaps that should have been closed by the human before execution. This shifts optimization from "cheaper tokens" to "fewer wrong turns per completed outcome."

**Gap-cost attribution model:**

Every retry, every exploratory token burn, and every validation failure is tagged with the ICE gap that caused it. The attribution maps token cost to missing fields:

| Gap Source | What it looks like in execution | Attribution |
|---|---|---|
| Missing intent field | Agent explores multiple interpretations of what the human wanted | Tagged to the specific missing intent field (description, constraints, failure scenarios, success scenarios, connections) |
| Missing expectations field | Agent produces output that passes technical checks but fails the outcome owner's definition of done | Tagged to the specific missing expectations field (done scenarios, failed scenarios, limits, non-goals) |
| Missing context | Agent requests information that the harness should have provided, or makes incorrect assumptions about the technical environment | Tagged to the specific context gap |
| Ambiguous constraint | Multiple retries on the same expectation because the constraint is not specific enough to verify | Tagged to the ambiguous constraint |

**Gap-cost report:**

After a session or outcome completion, a gap-cost report attributes token consumption to gap categories:

- Total tokens consumed for the outcome.
- Tokens spent on first-attempt generation (baseline).
- Tokens spent on retries, tagged by the gap that caused each retry.
- Tokens spent on exploration/assumption-making that was not present in the original intent.
- Gap-cost ratio: (gap-filling tokens / total tokens) * 100.

A high gap-cost ratio (>30-40%) signals that the intent, expectations, or context were under-specified, and the human should close the gaps before the next attempt, not just re-run the agent.

**Gap-cost triggers:**

The gap-cost report feeds stop/clarify/retry/continue decisions during execution:

1. **Continue**: gap-cost ratio below threshold, retries are convergent.
2. **Monitor**: gap-cost ratio rising but still below threshold; observe and flag.
3. **Clarify**: gap-cost ratio exceeds threshold, or retries are non-convergent. Pause execution, generate specific questions for the outcome owner, and wait for responses before continuing.
4. **Stop**: gap-cost ratio is extreme (>>50%) or the same gap causes repeated retries with no convergence. Stop execution and escalate to the outcome owner with the gap-cost report.

**Integration with the ICE framework:**

Gap-filling cost is the economic feedback loop for ICE craft separation. When ICE crafts are well-separated and complete, the gap-cost ratio stays low. When ICE crafts are blurred or incomplete, the gap-cost ratio spikes. The gap-cost report makes the cost of poor ICE discipline visible in token terms, converting an architectural principle into a measurable economic signal.

The Manual Brake Question Gate asks: "Would we still build it if it cost a week of engineering time instead of an afternoon of tokens?" ([[docs/canonical/manual-brake-question-gate|Manual Brake Question Gate]]:34). The gap-cost report answers: "Here is how many tokens this actually cost, and here is how many of those were spent filling gaps that should have been closed before execution." The cost-proxy question becomes measurable rather than intuitive.

**Prevention over detection:**

The gap-cost attribution model is a diagnostic tool. The preventive tools are:
- [[docs/canonical/intent-five-part-primitive|Intent as Five-Part Primitive]]: completeness gate catches missing fields before execution.
- [[docs/canonical/human-owned-expectations-boundary|Human-Owned Expectations Boundary]]: expectations artifact defines done before execution.
- [[docs/canonical/ice-craft-separation|ICE Craft Separation]]: craft separation prevents gaps from forming in the first place.

Gap-cost attribution proves that these preventive tools are worth the upfront cost by measuring what happens without them.

## Implementation in this repo

### What already exists

- [[docs/canonical/explicit-token-budget-ledger|Explicit Token Budget Ledger]]:29-62 maintains a per-call ledger with fixed cost, reducible cost, output reservation, safety buffer, remaining budget, and budget percentage. This is the instrumentation foundation that gap-filling measurement would consume.
- [[docs/canonical/burn-rate-runtime-forecast|Burn Rate Runtime Forecast]]:28-60 tracks consumption velocity, acceleration, and remaining runway in messages and minutes. Forecasts when token pressure will hit, but does not explain why it is hitting.
- [[docs/canonical/phase-gated-token-health-monitor|Phase-Gated Token Health Monitor]]:32-55 converts budget and burn rate to green/yellow/orange/red health phases with corresponding actions (continue, monitor, compress, new session). Phase transitions are triggered by raw consumption, not by gap-cost ratio.
- [[docs/canonical/deferred-ledger-agentic-work|Deferred Ledger for Agentic Work]]:29-56 tracks three categories of strategic debt (skill, dependence, carry). The dependence debt category captures "workflows built on assumption of free, correct generation" -- closest concept to gap-filling cost, but framed as structural risk rather than token-efficiency optimization.
- [[docs/canonical/budget-aware-session-handoff|Budget-Aware Session Handoff]]:28-53 implements session handoff with explicit budget consideration and context reset. Handles the symptom (budget exhaustion) but not the cause (gap-filling burn).
- [[docs/canonical/manual-brake-question-gate|Manual Brake Question Gate]]:33-34 asks the cost-proxy question: "Would we still build it if it cost a week of engineering time instead of an afternoon of tokens?" This is a gap-filling cost proxy -- it estimates the true cost. But it is a human judgment question, not an automated gap-cost measurement.
- [[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]:34-566 teaches token budgeting as a full curriculum lesson with calculator, dashboard, burn rate, and phase scenarios.

### What is missing from the pattern

The classification marks Token Economics of Gap-Filling as Partial Coverage because the repo has the cost instrumentation layer but cannot attribute token costs to specific information gaps ([[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-classification|classification]]:227-248).

Missing items:

1. A gap-cost attribution model that tags token consumption to specific ICE gaps (missing intent fields, ambiguous expectations, context gaps).
2. A gap-cost report tied to finished outcomes that attributes what percentage of tokens went to filling which gaps.
3. Gap-cost triggers: stop, clarify, retry, continue thresholds based on gap-cost ratio, not just raw burn rate.
4. Integration with the existing token ledger: add a gap-source field to each ledger entry.
5. Retry-cause tagging: when the Evaluator rejects output, tag the rejection reason to the ICE gap that caused it (e.g., "ambiguous constraint on price ceiling").
6. The cost-proxy question in Manual Brake made measurable: the gap-cost report converts "would we still build this?" from intuition to data.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Shifts optimization from cheaper tokens to fewer wrong turns per completed outcome | Requires instrumentation across token use, validation failures, retries, and outcomes |
| Makes hidden cost from gap-filling visible before it becomes multi-day rework | Token cost is a proxy and cannot replace quality or value measurement |
| Encourages intent and expectations hygiene because missing fields become measurable cost drivers | Strict burn gates can interrupt legitimate exploration unless the work is explicitly framed as an experiment |
| Provides the economic feedback loop for ICE craft separation -- proves that upfront precision saves tokens | Attribution accuracy depends on correctly identifying which gap caused each retry |
| Converts the Manual Brake cost-proxy question from intuition to data | Adds instrumentation complexity to every agent session |

## Relationship to Other Patterns

- **[[docs/canonical/ice-craft-separation|ICE Craft Separation]]** -- ICE craft separation prevents gaps. Gap-filling cost attribution measures the cost when gaps are not prevented. Together they form the economic feedback loop for ICE discipline.
- **[[docs/canonical/intent-five-part-primitive|Intent as Five-Part Primitive]]** -- missing intent fields are the primary source of gap-filling token burn. The five-part completeness gate prevents gaps; gap-cost attribution measures the cost of missing fields.
- **[[docs/canonical/human-owned-expectations-boundary|Human-Owned Expectations Boundary]]** -- ambiguous expectations cause retries. Gap-cost attribution tags retries to the specific expectations field that was ambiguous.
- **[[docs/canonical/explicit-token-budget-ledger|Explicit Token Budget Ledger]]** -- the ledger is the instrumentation foundation. Gap-cost attribution adds a gap-source field to each ledger entry.
- **[[docs/canonical/burn-rate-runtime-forecast|Burn Rate Runtime Forecast]]** -- burn-rate forecasting detects when token pressure is rising. Gap-cost attribution explains why: which gaps are causing the burn.
- **[[docs/canonical/phase-gated-token-health-monitor|Phase-Gated Token Health Monitor]]** -- phase transitions based on gap-cost ratio (not just raw consumption) would produce different and potentially earlier warnings.
- **[[docs/canonical/manual-brake-question-gate|Manual Brake Question Gate]]** -- the cost-proxy question becomes measurable. The gap-cost report provides the data to answer "would we still build this?" with evidence instead of intuition.
- **[[docs/canonical/deferred-ledger-agentic-work|Deferred Ledger for Agentic Work]]** -- dependence debt is structurally similar to gap-filling cost. Gap-cost attribution makes dependence debt measurable in token terms.
- **[[docs/canonical/generator-evaluator|Generator-Evaluator]]** -- retry-cause tagging connects Evaluator rejections to ICE gaps, closing the loop between evaluation and cost attribution.

## References

- [[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis|IDSD Method Analysis]]:124-126 -- paradoxo economico dos tokens: preco cai, custo por outcome sobe
- [[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis|analysis]]:118-119 -- caso concreto: $985 em tokens, tres dias de retrabalho
- [[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis|analysis]]:173 -- monolithic context fed to fill gaps como failure pattern
- [[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-patterns|IDSD Method Patterns]]:219-247 -- extracted pattern: Gap-Filling Token Burn Control
- [[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-classification|IDSD Method Classification]]:219-248 -- classification evidence: Partial Coverage, High integration value
- [[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis|analysis]]:126 -- SDD quebrado infla o custo de construir software, e essa inflacao desce a linha ate o cliente
