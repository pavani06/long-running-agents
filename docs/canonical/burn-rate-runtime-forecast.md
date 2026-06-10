---
title: 'Burn-Rate Runtime Forecast'
type: canonical
aliases: ["previsao de consumo de tokens", "runtime forecast", "burn rate prediction", "consumption velocity"]
tags: ["context-engineering", "agentes-orquestracao"]
last_updated: 2026-06-10
relates-to: ["[[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation]]", "[[docs/canonical/stable-harness-prompt|Stable Harness Prompt]]", "[[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]]", "[[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]"]
sources: ["[[docs/analysis/2026-06-10-token-budgeting/analysis|Knowledge Extraction]]"]
---

# Burn-Rate Runtime Forecast

**Type:** Canonical Pattern
**Status:** Active
**Source:** curriculum/01-nivel-1-fundamentals/02-token-budgeting.md
**Classification:** Missing
**Precedence:** Level 2 (docs/system-of-record.md)

---

## Problem

Static remaining-context checks miss the runtime risk that matters in long-running sessions: the same token balance can be safe when consumption is slow and unsafe when the session is accelerating. The source lesson defines token budgeting as planning, allocating, and controlling token use over a conversation, then separates total context, already spent history, and future room for new messages plus responses [[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]:34-48.

The concrete failure is late intervention. A session can still show available context while output size, user message frequency, or tool-result volume increases enough to consume the remaining budget faster than the operator expects. The source lesson defines burn rate as `(Input + Output) / Minutos de Conversa` and says its operational value is knowing how many minutes remain, planning compaction, and changing strategy in time [[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]:143-165.

Without a runtime forecast, agents discover token pressure after behavior degrades. The analysis names token exhaustion as an early quality-degradation condition, not only a hard crash, and specifically lists short answers, rushed assumptions, reduced empathy, and weaker reasoning as warning signs [[docs/analysis/2026-06-10-token-budgeting/analysis|Knowledge Extraction]]:121-127. The curriculum shows the same user-visible degradation as "comportamento ansioso" near the limit and prescribes immediate compaction or a new session [[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]:510-519.

## Solution

Track token usage as a timestamped time series and forecast session runway from current consumption velocity, acceleration, reserved output capacity, and configured safety buffer. The static budget equation remains the base: available space equals total context minus processed history minus response buffer [[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]:49-62. The forecast layer adds time: the analysis states that budget health is temporal, not only spatial, because a large remaining context can still be unsafe when burn rate is accelerating [[docs/analysis/2026-06-10-token-budgeting/analysis|Knowledge Extraction]]:28-38.

```
+--------------------+     +----------------------+     +--------------------+
| timestamped usage  | --> | burn-rate calculator | --> | runway forecast    |
| input/output/used  |     | tokens/min + accel   |     | msgs + minutes     |
+---------+----------+     +----------+-----------+     +---------+----------+
          |                           |                           |
          v                           v                           v
+--------------------+     +----------------------+     +--------------------+
| reserve buffers    | --> | phase decision       | --> | intervention       |
| response + safety  |     | green/yellow/orange  |     | continue/compress  |
+--------------------+     | red                  |     | new session        |
                           +----------------------+     +--------------------+
```

| Component | Rule |
|---|---|
| Timestamped samples | Record enough input, output, elapsed time, and remaining-budget samples to compare recent velocity against earlier velocity. |
| Response reserve | Subtract response and safety buffers before treating remaining tokens as usable runway [[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]:445-459. |
| Velocity | Compute `tokens_per_minute = (input_tokens + output_tokens) / elapsed_minutes`, matching the lesson formula [[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]:143-159. |
| Acceleration | Compare burn-rate windows; the lesson marks 500 to 750 to 1200 tokens/min as repeated acceleration that should trigger action [[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]:486-499. |
| Runway | Convert available tokens into remaining messages and minutes, as the calculator does after subtracting reserves [[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]:428-460. |
| Intervention | Map runway and acceleration to continue, monitor, compress, or new-session actions, following the phase model in the analysis [[docs/analysis/2026-06-10-token-budgeting/analysis|Knowledge Extraction]]:39-48. |

Before this pattern, a monitor says: "150,000 tokens remain, so the session is healthy." The source dashboard already shows that token count alongside burn rate and time remaining, which is the missing signal [[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]:462-482. After this pattern, the monitor says: "150,000 tokens remain, current burn is 1,500 tokens/min, acceleration is positive, and estimated runway is about 100 minutes before reserves; stay green only while the acceleration window remains stable." The analysis explicitly frames the conversation calculator as a way to estimate remaining messages, convert them into minutes, and make exhaustion predictable enough for proactive intervention [[docs/analysis/2026-06-10-token-budgeting/analysis|Knowledge Extraction]]:50-62.

## Implementation in this repo

### What already exists

- [[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]] defines token budgeting as a control practice across an agent conversation and decomposes the budget into total context, spent history, and future room for new messages and responses [[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]:34-48.
- [[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]] gives the static budget equation and a worked example that subtracts processed history and response buffer from total context [[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]:49-62.
- [[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]] defines burn rate as token consumption per minute and gives a 60-minute example producing 1,500 tokens/min [[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]:143-159.
- [[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]] contains a conversation-viability calculator that reserves response and safety buffers, computes available tokens, estimates remaining messages, and converts messages into minutes [[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]:428-460.
- [[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]] shows a simplified token dashboard with total context, already used tokens, reserved tokens, available tokens, burn rate, and time remaining [[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]:462-482.
- [[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]] identifies accelerating burn rate as a red flag and prescribes compression, old-history removal, and context summary preparation [[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]:486-499.
- [[docs/analysis/2026-06-10-token-budgeting/analysis|Knowledge Extraction]] extracts the four-component budget model and states that budget health is temporal because a large remaining context can be unsafe when burn rate accelerates [[docs/analysis/2026-06-10-token-budgeting/analysis|Knowledge Extraction]]:28-38.
- [[docs/analysis/2026-06-10-token-budgeting/analysis|Knowledge Extraction]] extracts a conversation viability calculator that computes remaining budget, estimates remaining messages, and converts message budget into minutes [[docs/analysis/2026-06-10-token-budgeting/analysis|Knowledge Extraction]]:50-62.
- [[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation]] already covers bounded active context with head, tail, latest result, and recoverable middle [[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation]]:26-39.
- [[docs/canonical/stable-harness-prompt|Stable Harness Prompt]] already preserves the harness prompt as a non-reducible block while history, tool bulk, and context payload are reduced [[docs/canonical/stable-harness-prompt|Stable Harness Prompt]]:26-41.
- [[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]] already treats latency, token cost, false positives, infrastructure cost, maintenance hours, and user outcomes as measured lifecycle costs for harness components [[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]]:52-60.
- [[docs/canonical/eval-tier-stratification|Eval Tier Stratification]] already defines eval runtime budgets and expected runtime by fast, medium, and deep tiers, but for eval-suite scheduling rather than live session runway [[docs/canonical/eval-tier-stratification|Eval Tier Stratification]]:26-49.
- [[docs/system-of-record|System of Record]] lists active canonical docs under `docs/canonical/` and includes head-tail truncation, stable harness prompt, measured harness evolution lifecycle, and eval-tier stratification, but does not list a burn-rate runtime forecast canonical pattern [[docs/system-of-record|System of Record]]:124-166.

### What is missing

1. A canonical contract for timestamped token-usage samples that can distinguish current burn rate from earlier burn rate; the active canonical list does not include a burn-rate runtime forecast entry [[docs/system-of-record|System of Record]]:124-166.
2. A formal `tokens_per_minute` metric tied to both input and output tokens rather than remaining-context percentage alone; the metric exists in the curriculum but not as an active canonical contract [[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]:143-159 [[docs/system-of-record|System of Record]]:124-166.
3. A formal acceleration check that compares burn-rate windows before the session reaches low remaining-context thresholds; the red flag exists in the curriculum but not as an active canonical contract [[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]:486-499 [[docs/system-of-record|System of Record]]:124-166.
4. A runway estimate that outputs both remaining messages and remaining minutes after subtracting response and safety buffers; the calculator exists in the curriculum and analysis but not as an active canonical contract [[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]:428-460 [[docs/analysis/2026-06-10-token-budgeting/analysis|Knowledge Extraction]]:50-62 [[docs/system-of-record|System of Record]]:124-166.
5. A decision table that combines remaining percentage, burn-rate velocity, acceleration, and expected next-step intensity into continue, monitor, compress, or new-session actions; the analysis extracts phase actions, but the active canonical list has no runtime-forecast pattern [[docs/analysis/2026-06-10-token-budgeting/analysis|Knowledge Extraction]]:39-48 [[docs/system-of-record|System of Record]]:124-166.
6. Integration guidance for using runtime forecasts as the trigger for [[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation]] or [[docs/canonical/stable-harness-prompt|Stable Harness Prompt]] instead of waiting for visible behavior degradation; those canons define reduction mechanics and prompt preservation, not the burn-rate trigger itself [[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation]]:26-39 [[docs/canonical/stable-harness-prompt|Stable Harness Prompt]]:26-41.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Turns context health from a static percentage into an operational runway estimate grounded in burn rate [[docs/analysis/2026-06-10-token-budgeting/analysis|Knowledge Extraction]]:28-38 | Requires timestamped token accounting instead of a single remaining-context calculation |
| Triggers compaction while there is still room to summarize safely [[docs/analysis/2026-06-10-token-budgeting/analysis|Knowledge Extraction]]:219-223 | Can intervene too early if short bursts are mistaken for sustained acceleration |
| Makes remaining messages and minutes visible to operators before quality degrades [[docs/analysis/2026-06-10-token-budgeting/analysis|Knowledge Extraction]]:50-62 | Estimates depend on representative message size and message-rate assumptions |
| Connects token pressure to concrete actions such as compress, summarize, remove old history, or start a new session [[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]:486-508 | Adds monitoring state that must stay aligned with the context builder and model-specific context window |

## Relationship to Other Patterns

- **Depends on:** [[docs/canonical/stable-harness-prompt|Stable Harness Prompt]], because forecast-triggered reduction must not treat the harness prompt as reducible context [[docs/canonical/stable-harness-prompt|Stable Harness Prompt]]:26-41.
- **Depends on:** [[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation]], because the forecast needs a safe intervention path once acceleration or low runway appears [[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation]]:26-39.
- **Validated by:** [[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]], because forecast monitors should be judged by measured token cost, latency, operating cost, and user outcomes rather than intuition [[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]]:52-60.
- **Complements:** [[docs/canonical/eval-tier-stratification|Eval Tier Stratification]], because eval tiers govern validation runtime while this pattern governs live session runtime [[docs/canonical/eval-tier-stratification|Eval Tier Stratification]]:26-49.
- **Complements:** [[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]], because the curriculum teaches the calculator, dashboard, red flags, and KODA phase scenarios that this canonical pattern formalizes [[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]:428-566.

## References

- [[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]:34-62 - source definition of token budgeting and the static budget equation.
- [[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]:143-165 - source burn-rate definition, formula, and operational purpose.
- [[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]:428-482 - conversation viability calculator and dashboard with burn rate and time remaining.
- [[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]:486-566 - acceleration red flag and KODA green/yellow/orange/red phase scenarios.
- [[docs/analysis/2026-06-10-token-budgeting/analysis|Knowledge Extraction]]:28-38 - extracted four-component budget model and temporal burn-rate insight.
- [[docs/analysis/2026-06-10-token-budgeting/analysis|Knowledge Extraction]]:50-62 - extracted runtime calculator for remaining budget, messages, and minutes.
- [[docs/analysis/2026-06-10-token-budgeting/analysis|Knowledge Extraction]]:111-117 - extracted Token Health Monitor pattern.
- [[docs/analysis/2026-06-10-token-budgeting/analysis|Knowledge Extraction]]:195-199 - extracted accelerating burn-rate failure pattern and mitigation.
- [[docs/analysis/2026-06-10-token-budgeting/analysis|Knowledge Extraction]]:219-223 - extracted late-intervention failure pattern.
- [[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation]]:26-39 - existing bounded-context and recoverable-middle mechanism.
- [[docs/canonical/stable-harness-prompt|Stable Harness Prompt]]:26-41 - existing stable prompt preservation during context reduction.
- [[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]]:52-60 - existing measured token, latency, and operating-cost governance.
- [[docs/canonical/eval-tier-stratification|Eval Tier Stratification]]:26-49 - existing runtime-budget taxonomy for eval tiers.
- [[docs/system-of-record|System of Record]]:23-45 - domain grounding for `agentes-orquestracao`.
- [[docs/system-of-record|System of Record]]:124-166 - active canonical docs list and absence of a burn-rate runtime forecast canonical.
