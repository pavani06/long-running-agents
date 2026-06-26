---
title: "Spread Capture as Analytical Primitive"
type: canonical
aliases: ["captura de spread como primitiva analitica", "spread capture primitive", "quem captura o spread", "where is the spread"]
tags: ["agentes-orquestracao", "analise-estrutural"]
last_updated: 2026-06-25
relates-to: ["[[docs/analysis/2026-06-25-futuro-ia-juros-brasil-visao-daniel-goldberg/patterns|Extracted Patterns]]", "[[docs/canonical/energy-value-chain-spread-analysis|Energy Value Chain Spread Analysis]]"]
sources: ["[[docs/analysis/2026-06-25-futuro-ia-juros-brasil-visao-daniel-goldberg/analysis|Knowledge Extraction]]"]
---

# Spread Capture as Analytical Primitive

**Type:** Canonical Pattern
**Status:** Active
**Source:** `docs/analysis/2026-06-25-futuro-ia-juros-brasil-visao-daniel-goldberg/analysis.md` (Daniel Goldberg, Market Makers #378)
**Classification:** Missing — no equivalent meta-pattern exists in the repo
**Precedence:** Level 2 (`docs/system-of-record.md`)

---

## Problem

The standard analytical question in any investment or allocation decision is "what is this worth?" (intrinsic value). But in structurally advantaged markets — where monopoly power, regulatory moats, network effects, or information asymmetry concentrate value capture — intrinsic value is the wrong primitive. The more informative question is "where is the spread, who captures it, and is the capture sustainable?"

This is not a niche insight for one industry. The same reframing applies across domains that appear unrelated:

| Domain | Spread | Capture Agent | Standard (Wrong) Question |
|--------|--------|---------------|---------------------------|
| Technology (AI, 2022-2025) | Cost of MWh per GPU chip ($3/M tokens) → sale price of compute ($15-50/M tokens) = 50-170% spread | NVIDIA (chip layer), not hyperscalers | "What are these AI companies worth?" → models valuation on the wrong layer |
| Government (Brazil) | Tax revenue as % of GDP: Brazil 38% vs. regional peers 25% → 13pp spread | Estado brasileiro, independentemente de crescimento | "Is GDP growth accelerating?" → misses the structural capture that persists regardless of growth rate |
| Platforms (marketplaces) | Seller cost of goods per transaction → platform take-rate (15-30%) → end-buyer price | Platform operator (take-rate is a structural spread, not a service fee) | "What multiple should I pay for this marketplace?" → models revenue growth without modeling spread persistence |
| Finance (credit markets) | Cost of funding (Selic 15.25%) → lending rate spread (8-10pp over Selic) → borrower rate | Brazilian banks (structural spread protected by institutional barriers to entry) | "Are banks cheap on P/B?" → misses that the spread exists because of institutional design, not operational efficiency |
| Logistics | Diesel cost per liter → fleet operator markup → dispatcher scheduling premium → last-mile delivery charge | The entity that controls the bottleneck layer (dispatcher or last-mile, depending on market structure) | "What is this logistics company worth at 8× EBITDA?" → models aggregate margins, not layer-by-layer spread |

In every case, the failure mode is identical: the analyst starts with a valuation model (DCF, multiples, comparative analysis) before identifying where the structural spread lives and whether it can persist. The answer to "is this cheap?" changes completely when you first answer "where is the spread?"

## Solution

Replace the analytical primitive "what → intrinsic value?" with "where → spread → who captures → sustainable?" as the first question in any domain analysis.

```
Standard analytical flow (valuation-first):
  Observe asset → "What is this worth?" → Build model → Compare to price → Decide

Reframed analytical flow (spread-first):
  Map value chain → Identify all cost-to-price gaps → Attribute each gap to capture agent
       → Rank by magnitude × persistence → Test sustainability → THEN ask "what is this worth?"
       ↘ If no structural spread exists, intrinsic value analysis may apply
```

### Core Mechanism

| Step | Question | Output |
|------|----------|--------|
| 1. Map the chain | What are the transformation steps from input to final service in this domain? | Ordered layer sequence with participants at each layer |
| 2. Find the spreads | What is the gap between cost to produce and price paid at each layer? | Spread map (dollar and percentage) across all layers |
| 3. Attribute capture | Which entity or layer captures each spread? Is the capture competitive (many players) or structural (one player or coordinated few)? | Capture attribution with concentration index per spread |
| 4. Rank by persistence | How durable is each spread? What competitive, regulatory, or technological force could compress it? | Ranked list: magnitude × persistence |
| 5. Identify the dominant agent | Which entity captures the widest AND most persistent spread? | Dominant capture agent(s) |
| 6. Scan for disruption | What is the most likely vector that could compress the dominant spread? | Disruption vector with estimated timeline |
| 7. Now value | Given the spread-and-capture map, what is the appropriate valuation framework? | May be intrinsic value, may be spread-capture multiple, may be "structural disadvantage — avoid" |

### Before/after: how the analysis changes

| Before (valuation primitive) | After (spread-capture primitive) |
|---|---|
| "What is this AI company worth?" | "Where is the spread between MWh cost and inference price, who captures it at each layer, and is that capture sustainable?" |
| "Is GDP growth accelerating in Brazil?" | "The government captures 38% of GDP regardless of growth rate. Where does that spread go — services, transfers, debt service? Who benefits from each allocation?" |
| "What multiple should I pay for this marketplace?" | "The platform's 15-30% take-rate is a structural spread, not a service fee. Does this spread persist if sellers coordinate, if regulation caps fees, or if a new platform subsidizes entry?" |
| "Are Brazilian banks cheap on P/B?" | "The credit spread (8-10pp over Selic) exists because institutional design — barriers to entry, Selic floor, judicial unpredictability — prevents competition from compressing it. The P/B multiple is a symptom; the spread persistence is the cause." |
| "Is this logistics company undervalued?" | "Does this company own the layer with the widest spread between diesel cost and last-mile delivery price? If the fleet layer is a commodity (thin spread) but the dispatcher layer captures a scheduling premium (thick spread), owning trucks is the wrong asset." |

### Design Principle

This is a META-PATTERN: it does not specify *how* to compute the spread at each layer — that is the job of domain-specific implementations like [[docs/canonical/energy-value-chain-spread-analysis|Energy Value Chain Spread Analysis]]. This pattern specifies *which question to ask first*. In any analytical domain, before you compute, you reframe.

The meta-pattern is validated by cross-domain application: if the same question ("where is the spread, who captures it, and is it sustainable?") produces non-obvious insight in technology (NVIDIA), government (Brazil's 38% tax/GDP), platforms (marketplace take-rates), and finance (Brazilian bank spreads), then the question itself — not the domain-specific mechanism — is the reusable primitive.

## Implementation in this repo

### What already exists

No existing coverage. The repo's analytical framework (spread analysis, structural power, institutional incentives) is a natural host for this meta-pattern, but no canonical doc formalizes the reframing from valuation to spread capture as the organizing analytical question.

### What is missing

1. **No explicit articulation of the meta-pattern** — the repo has domain-specific mechanisms ([[docs/canonical/energy-value-chain-spread-analysis|Energy Value Chain Spread Analysis]] for layered industries, [[docs/canonical/capex-revenue-credit-mispricing|Capex-Revenue Credit Mispricing]] for credit analysis) but no canonical doc that names "spread capture" as the primitive question that should precede all of them. Without this meta-pattern, each domain-specific pattern appears as an isolated technique rather than instances of a single analytical reframing.

2. **No cross-domain validation table** — the source analysis applies the spread-capture question to technology (GPU layer), government (tax/GDP), platforms (take-rates), and finance (credit spreads), demonstrating that the same question produces non-obvious insight across domains. The repo has no artifact that collects these applications as evidence that the meta-pattern is domain-agnostic. This gap makes it harder to teach the pattern as a general analytical framework.

3. **No integration with the decision-making stack** — once the dominant capture agent is identified, the agent or capital allocator needs a framework for converting that insight into an action: position, allocation, or risk budget. The repo does not connect the spread-capture primitive to downstream decision patterns (e.g., [[docs/canonical/asymmetric-binary-outcome-positioning|Asymmetric Binary-Outcome Positioning]], which may be the appropriate position structure when the spread persistence is a binary event like regulatory approval).

4. **No agentic application** — the meta-pattern is described for human analysts (capital allocators, investors), but the repo's core concern is agentic systems. A canonical specification of how an autonomous agent should apply the spread-capture primitive — which data sources to query, how to structure the output, what confidence thresholds to apply before proceeding to domain-specific analysis — would make the pattern operational within the agent architecture. Currently, an agent tasked with "analyze this industry" has no structured guidance to ask "where is the spread?" before computing.

## Tradeoffs

| Benefit | Cost |
|---------|------|
| Reframes analysis from valuation (model-dependent, sensitive to assumptions) to structural power (observable from market structure, regulatory design, competitive dynamics) | Spread data may be proprietary or estimated with wide error bands — the reframing does not eliminate measurement uncertainty, it changes what is being measured |
| Works across domains: technology layers, financial markets, government taxation, platforms, logistics, energy — the same question produces non-obvious insight in all of them | Sustainability assessment is speculative when disruption comes from unknown entrants or technological shifts the analyst cannot foresee |
| Identifies investment opportunities where spread capture is mispriced because the market is asking the wrong question (valuation) instead of the right one (spread persistence) | Does not directly produce a valuation — the meta-pattern tells you where to look for value, but does not tell you what price to pay. Requires complementary frameworks for position sizing |
| Unifies analysis of seemingly disparate domains through a single lens — prevents domain-specific overfitting where each industry gets its own analytical framework | Spread capture can shift abruptly on regulatory or technological shocks — the structural insight is durable until it isn't, and the transition is usually nonlinear |

## Relationship to Other Patterns

- **Implemented by:** [[docs/canonical/energy-value-chain-spread-analysis|Energy Value Chain Spread Analysis]] — this pattern provides the layered mechanism for computing where the spread accumulates in multi-step value chains. Spread Capture as Analytical Primitive provides the meta-question; Energy Value Chain Spread Analysis provides the computational method for one domain class (multi-layer industries).
- **Complements:** [[docs/canonical/inelastic-market-flow-dominance-model|Inelastic Market Flow Dominance Model]] — when markets are inelastic (price-demand elasticity ~0.2), spread persistence is amplified because competitive forces that would normally compress spreads operate with multi-year lags. The spread-capture question identifies *who* captures the spread; the inelastic-market model explains *why* the spread persists longer than efficient-market theory predicts.
- **Complements:** [[docs/canonical/social-archetype-classification|Social Archetype Classification]] — the archetype (Creation, Abundance, Predation) determines whether spread capture is a feature of value creation or a symptom of extraction. In a Creation society, wide spreads signal innovation premium and should attract capital. In a Predation society, wide spreads signal rent extraction and should trigger avoidance or regulatory positioning.
- **Feeds into:** [[docs/canonical/capex-revenue-credit-mispricing|Capex-Revenue Credit Mispricing]] — when the spread at a capital-intensive layer depends on technological assumptions (e.g., GPU depreciation rates), credit analysis that uses accounting schedules instead of the spread-capture framework will systematically misprice the debt.
- **Applies to:** [[docs/canonical/credibility-cascade-in-regulated-assets|Credibility Cascade in Regulated Assets]] — when credibility failures compress market pricing below intrinsic value, the spread-capture question reframes the opportunity: is this a forced-selling event creating a temporary spread between price and value that a patient allocator can capture?
- **Depends on:** None — this is the foundational analytical reframing that domain-specific patterns implement.

## References

- [[docs/analysis/2026-06-25-futuro-ia-juros-brasil-visao-daniel-goldberg/analysis|Knowledge Extraction]] — §6.4 (Onde está o spread e quem o captura?, explicit articulation of the meta-pattern), §6.5 (Síntese, cross-domain application of the question)
- [[docs/analysis/2026-06-25-futuro-ia-juros-brasil-visao-daniel-goldberg/patterns|Extracted Patterns]] — Pattern #6: full specification with inputs (domain, cost structure, pricing, competitive dynamics), outputs (spread map, dominant capture agent, sustainability score, disruption vector), 4 components, 6-step flow
