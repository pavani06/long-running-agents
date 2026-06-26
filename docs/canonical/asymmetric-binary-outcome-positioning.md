---
title: "Asymmetric Binary-Outcome Positioning"
type: canonical
aliases: ["posicionamento binario assimetrico", "binary outcome betting", "negative convexity bet", "aposta de convexidade negativa", "probabilidade implícita vs real", "short opção de pré-pagamento"]
tags: ["agentes-orquestracao", "analise-estrutural"]
last_updated: 2026-06-25
relates-to: ["[[docs/analysis/2026-06-25-futuro-ia-juros-brasil-visao-daniel-goldberg/patterns|Extracted Patterns]]", "[[docs/analysis/2026-06-25-futuro-ia-juros-brasil-visao-daniel-goldberg/analysis|Knowledge Extraction]]", "[[docs/canonical/inelastic-market-flow-dominance-model|Inelastic Market Flow Dominance]]"]
sources: ["[[docs/analysis/2026-06-25-futuro-ia-juros-brasil-visao-daniel-goldberg/analysis|Knowledge Extraction]]"]
---

# Asymmetric Binary-Outcome Positioning

**Type:** Canonical Pattern
**Status:** Active
**Source:** raw-knowledge/sources/2026-06-25-futuro-ia-juros-brasil-visao-daniel-goldberg.md
**Classification:** Missing
**Precedence:** Level 2 (docs/system-of-record.md)

---

## Problem

Standard portfolio theory assumes normal payoff distributions, but binary-outcome events — default/recovery, judicial decisions, regulatory approvals, restructuring votes — have discontinuous payoffs that violate this assumption. Mean-variance optimization is blind to negative convexity: a position that wins 70% of the time but loses everything 30% of the time looks identical in expected value to a diversified portfolio, yet the risk-of-ruin dynamics are fundamentally different.

The key failure mode is that markets price binary events via **flow, not fundamentals**. When institutional holders are forced to sell on binary event triggers (downgrades, index exclusions, regulatory reclassifications), the market-implied probability of a favorable outcome collapses below the real probability — not because fundamentals deteriorated, but because the selling is involuntary and the buyer base is structurally limited. An investor who buys the mispriced binary option discovers too late that the flow doesn't reverse before the option expires, and the real probability converges to the implied probability through price, not through event outcome.

The pattern applies beyond finance. Any binary decision under uncertainty — deploying a breaking change, accepting a regulatory risk, choosing between two architectural paths where one is catastrophic if wrong — shares the same structure: estimate real probability, derive implied probability from observable behavior, compute the required premium to compensate for negative convexity, and assess whether flow-based mispricing exists.

## Solution

A structured four-step mechanism for evaluating binary-outcome positions: estimate real probability independently, extract market-implied probability from prices, compute the required premium for negative convexity, and assess whether flow-driven mispricing justifies the position.

### Payoff structure (negative convexity bet)

```
                     PAYOFF
                       │
    Win case (70%) ────┤████████████████  +R (finite, pre-paid upside)
                       │
                       │
                       │
                       │
    Loss case (30%) ───┤────────────────  -100% (total, carried downside)
                       │
                       ▼

    Key asymmetry: "namora vitórias, casa com derrotas"
    ─────────────────────────────────────────────────
    Wins are small and frequent. Losses are total and rare.
    Over a sequence of N independent bets, risk of ruin grows
    with N even when the edge is positive.
    
    P(ruin in N bets) = 1 - (1 - p_loss)^N
    For p_loss = 0.30, N = 5 → P(ruin) ≈ 83%
```

### Core mechanism

| Step | Action | Output |
|------|--------|--------|
| 1. Frame the event | Define the binary outcome and its trigger conditions precisely. What observable event resolves the bet? When? | Event specification with resolution timeline |
| 2. Estimate real probability | Derive probability of favorable outcome from fundamentals (legal analysis, default modeling, regulatory timeline), independent of market price | `P_real` (0–1) |
| 3. Extract implied probability | Back out the probability the market is pricing from observed asset prices (bond spread, option premium, equity discount) | `P_implied` (0–1) |
| 4. Compute probability gap | `P_real - P_implied`. A positive gap indicates the market is underpricing the favorable outcome — the opportunity zone | `Delta_P` (signed scalar) |
| 5. Calculate required premium | The minimum payoff in the favorable case needed to compensate for negative convexity, given `P_real` and the loss magnitude in the unfavorable case | `Premium_min = (1/P_real - 1) × Loss` |
| 6. Assess flow dominance | Is the gap driven by flow (forced selling, rating constraints, index mechanics) rather than fundamentals? If yes, the gap is structural — it persists until the flow reverses. If no, the gap may be information asymmetry (someone knows something you don't). | Flow attribution (yes/no) |
| 7. Structure the position | Size for ruin tolerance: if `P(ruin over N bets) > threshold`, reduce size. Collect upside upfront where possible (pre-paid structure). Never size for "conviction" — size for probability of survival. | Position specification with sizing rule |

### Decision rules

| Condition | Action |
|---|---|
| `Delta_P > 0` AND flow dominance confirmed AND `Premium_offered ≥ Premium_min` | Deploy position — the market is pricing a flow distortion, not an information gap. Structure with pre-paid upside and bounded size |
| `Delta_P > 0` AND flow dominance NOT confirmed | Caution — the gap may reflect information you lack. Reduce size, seek additional verification |
| `Delta_P > 0` AND `Premium_offered < Premium_min` | Insufficient compensation for negative convexity. Pass — the edge exists but isn't priced |
| `Delta_P < 0` | Market is pricing a worse outcome than fundamentals suggest. Do not deploy — either you're wrong about `P_real` or the market has information you don't |
| Sequence of losses approaching ruin threshold | Kill switch — stop deploying new binary bets regardless of edge. Survive to play the next sequence |
| `P_real` confidence interval is wide (>±15%) | Probability estimate is unreliable. Reduce position size proportionally to interval width |

### Sizing constraints

| Constraint | Rule |
|---|---|
| Maximum position size | `1 / max_loss_sequence` of portfolio (so you survive the worst-case run) |
| Kill criterion | Cumulative loss exceeds 20% of capital allocated to binary-outcome strategy |
| Premium threshold | Offered payoff must be ≥ 3× `Premium_min` when `P_real` is estimated with wide error bands |
| Concentration limit | Maximum 5 concurrent binary bets; no single event domain >40% of binary-outcome book |

## Implementation in this repo

### What already exists

No existing coverage. The repository focuses on agentic orchestration and harness engineering, not financial or decision-theoretic frameworks. The 85+ canonical docs cover agent evaluation, context management, harness design, and multi-agent coordination — none address binary-outcome positioning, probability gap analysis, or negative convexity modeling.

### What is missing

1. **No `BinaryEventFramer` abstraction** — the repo has no data model for defining binary events with observable trigger conditions, resolution timelines, and outcome spaces. This is a standalone analytical primitive that could be adapted to agentic decision contexts (e.g., "deploy feature flag vs. don't" as a binary outcome with real/implicit probability modeling).

2. **No `ProbabilityGap` computation** — the four-step mechanism (real probability → implied probability → gap → flow attribution) is not encoded in any canonical doc. The meta-structure (structured 4-step pipeline) is familiar to this repo's patterns (`plan-execute-verify`, `generator-evaluator`), but the specific probability-gap mechanic is absent.

3. **No `ruinModel` for agentic decisions** — agents that face binary decisions (retry vs. escalate, feature gate vs. rollback, accept vs. reject a constraint violation) have no risk-of-ruin framework. The `tested-degradation-ladder` handles failure recovery but does not model probability-weighted survival over N sequential binary decisions.

4. **No cross-domain bridge** — the pattern explicitly claims applicability beyond finance ("any binary decision under uncertainty"), but the repo has no documentation connecting this probability-gap structure to agent evaluation (confidence calibration), constraint enforcement (binary accept/reject with real vs. perceived risk), or deployment decisions (canary vs. full rollout as a binary bet). The structural homology is present (both domains involve estimating `P_real` from data and comparing to `P_implied` from behavior) but is unexploited.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Surfaces mispricing where market-implied probabilities diverge from real probabilities — identifies opportunities invisible to mean-variance analysis | Real probability estimates are subjective and may be systematically biased; overconfidence in `P_real` is the most common failure mode |
| Explicitly models negative convexity that standard portfolio theory ignores — prevents hidden risk-of-ruin from sequential binary bets | A string of unfavorable outcomes can be catastrophic regardless of edge; sizing rules mitigate but do not eliminate this risk |
| Applicable beyond finance: any binary decision under uncertainty (deploy/revert, feature gate, architectural fork) with asymmetric payoffs | Requires discipline to avoid overconfidence in probability estimates — the psychological bias toward "I'm right about this one" is stronger in binary bets than continuous bets |
| Connects to inelastic market theory via the flow-attribution step — explains *why* mispricing persists (forced selling, not information) | Flow direction can reverse abruptly on macro shocks, invalidating the flow-dominance assumption mid-position |
| Structured sizing rules (kill criteria, premium thresholds, concentration limits) prevent the "one bad year wipes out five good years" trap | Position sizing is non-trivial and the rules require calibration per domain; the framework provides structure, not plug-and-play parameters |

## Relationship to Other Patterns

- **Depends on:** [[docs/canonical/inelastic-market-flow-dominance-model|Inelastic Market Flow Dominance]] — the flow-attribution step (Step 6) requires identifying whether the probability gap is driven by flow or information. Without the elasticity estimate and flow-tracker from Flow Dominance, the binary-outcome analysis cannot distinguish structural mispricing from information asymmetry.
- **Complements:** Spread Capture as Analytical Primitive (Pattern #6 in [[docs/analysis/2026-06-25-futuro-ia-juros-brasil-visao-daniel-goldberg/patterns|Extracted Patterns]]) — Spread Capture identifies where structural economic value accumulates; Binary-Outcome Positioning provides the mechanism for betting on that accumulation when the market prices the outcome as a binary event.
- **Validated by:** [[docs/analysis/2026-06-25-futuro-ia-juros-brasil-visao-daniel-goldberg/analysis|Goldberg AI Analysis]] — applied by Lumina Capital Management in their Soluções de Capital book, pricing binary events (judicial decisions, restructurings, bankruptcies) with implied probabilities of 20% when real probabilities were 70%. The strategy operates on "short prepayment option" structures: pre-paid upside, carried downside.
- **Structurally related to:** [[docs/canonical/generator-evaluator|Generator/Evaluator]] — the separation between estimating `P_real` (generator, subjective, model-driven) and extracting `P_implied` (evaluator, observable, market-driven) mirrors the generator/evaluator split. Both patterns protect against self-deception by anchoring one estimate in observable behavior.

## References

- analysis §2.1 (Convexidade Negativa em Mercados Inelásticos — mechanism, pre-paid upside structure, "namora vitórias, casa com derrotas")
- patterns #7 (Asymmetric Binary-Outcome Positioning — full component model with event_framer, probability_estimator, premium_calculator, position_structurer; 7-step flow)
