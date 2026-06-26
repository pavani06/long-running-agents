---
title: "Social Archetype Classification"
type: canonical
aliases: ["classificacao de arquetipos sociais", "criacao abundancia predacao", "taxonomia de sociedades", "creation abundance predation taxonomy"]
tags: ["agentes-orquestracao", "analise-estrutural"]
last_updated: 2026-06-25
relates-to: ["[[docs/analysis/2026-06-25-futuro-ia-juros-brasil-visao-daniel-goldberg/patterns|Extracted Patterns]]"]
sources: ["[[docs/analysis/2026-06-25-futuro-ia-juros-brasil-visao-daniel-goldberg/analysis|Knowledge Extraction]]"]
---

# Social Archetype Classification

**Type:** Canonical Pattern
**Status:** Active
**Source:** raw-knowledge/sources/2026-06-25-futuro-ia-juros-brasil-visao-daniel-goldberg.md
**Classification:** Missing
**Precedence:** Level 2 (docs/system-of-record.md)

---

## Problem

Political interventions, macroeconomic policies, and investment strategies fail systematically when analysts apply the wrong archetype's solutions to a different archetype's problems. Three failures recur across domains:

1. **Categorical strategy error** — applying Creation-society strategies (deregulation, innovation incentives) to Predation-society problems where the dominant incentive is extraction, not creation. Opening markets to competition fails when predation incentives dominate because entrants shift from innovating to extracting the same rents the incumbents already capture.

2. **Identical reforms, divergent outcomes** — why the same financial liberalization produces growth in the USA (Creation/Abundance hybrid) but capital flight and concentration in Brazil (Predation dominant). The reform interacts with the underlying incentive structure: in Creation, liberalization funds new entrants; in Predation, it funds incumbents buying competitors to consolidate extraction.

3. **Mispriced investment theses** — why some markets reward innovation (Silicon Valley) and others reward rent-seeking (regulated oligopolies, political access). An investor who analyzes "what is this company worth?" without asking "does this economy reward creating value or extracting it?" systematically overpays for growth in predation environments and underpays for moats in creation environments.

## Solution

Classify any economic unit — country, industry, company, or team — by its fundamental incentive structure: how individual actors are rewarded. Three ideal archetypes form a spectrum:

```
CREATION ─────────── ABUNDANCE ─────────── PREDATION
(positive-sum)    (capital management)    (zero-sum)

Innovation → new    Accumulated capital     Extraction via
value generated;    depreciated over        rents, barriers,
creative destruction time; stewarded        or political access;
is the norm         rather than created     "you have because
                                            you took"
```

### Archetype definitions

| Archetype | Dominant incentive | Value generation | Effective interventions | Interventions known to fail | Investment implication |
|---|---|---|---|---|---|
| **Creation** | Reward innovation; new entrants can destroy incumbents | Positive-sum: new value enters the system | Deregulation, IP protection, R&D incentives, open competition | Protectionism, state-directed industrial policy, incumbent bailouts | Bet on disruption; short incumbents with no moat beyond regulation |
| **Abundance** | Manage accumulated capital; preserve what exists | Neutral: value is stewarded, not grown or extracted | Incremental efficiency, capital recycling, intergenerational institutions | Creative-destruction shocks, rapid deregulation | Steady-state returns; infrastructure, regulated assets, capital-light compounders |
| **Predation** | Extract from others; barriers to entry are the moat | Zero-sum: one actor's gain is another's loss | **External competitive shock** (trade liberalization, foreign entry), antitrust enforcement, institutional transparency | Awareness campaigns, voluntary codes of conduct, subsidies to incumbents, incremental reform without external pressure | Bet on the moat, not the growth; the extraction margin is the alpha |

### Core mechanism

The archetype is determined by the answer to one diagnostic question: **"If an individual actor creates new value, do they capture it, or is it extracted by someone else?"**

- **Creation**: creator captures most of the value they create. Others can replicate or compete.
- **Abundance**: creator captures some, but institutional stewards (trustees, regulators, legacy owners) capture the rest through structured mechanisms.
- **Predation**: creator captures little. Value flows to the actor with the strongest extraction position (regulatory capture, political access, monopoly enforcement, legal asymmetry).

The self-perpetuation loop in predation environments is the key structural insight: if everyone predates, not predating is losing. Individual rationality converges to predation even when collective welfare would improve under creation. This is why awareness campaigns fail — the incentive structure, not ignorance, drives behavior. Only an external competitive shock (foreign competition, technology that bypasses incumbents, institutional reform with external enforcement) can break the equilibrium.

### Diagnostic signals

| Signal | Creation | Abundance | Predation |
|---|---|---|---|
| **Innovation rate** (new firms/patents per capita) | High and sustained | Moderate, incremental | Low; innovation in regulatory arbitrage, not product |
| **Barriers to entry** | Low; new entrants challenge incumbents | Medium; legacy advantages but addressable | High; regulatory, legal, or capital barriers are the primary moat |
| **Competitive intensity** | High churn; incumbents regularly displaced | Low churn; incumbents stable but face margin pressure | Near-zero churn; incumbents entrenched via non-market mechanisms |
| **Capital allocation** | To new ventures, R&D | To maintenance, efficiency, yield | To political access, regulatory moats, consolidation |
| **External openness** | High; foreign competition welcome | Moderate; selective openness | Low; foreign entry restricted or captured |
| **Narrative about wealth** | "Build something new" | "Manage what we have" | "You have because you took" |

## Implementation in this repo

### What already exists

No existing coverage — this repository covers agentic patterns (context engineering, harness design, eval stratification, multi-agent coordination), not socio-economic classification. The pattern was extracted from a macroeconomic analysis source and is applicable to domains beyond this repository's primary scope, including economic policy, investment strategy, and institutional design.

### What is missing

1. **Integration with institutional patterns** — the `Institutional Layer Amplification` pattern describes how gaps compound across legal layers, but does not incorporate archetype classification as a pre-condition for predicting gap magnitude. Predation economies amplify gaps more than Creation economies because extraction incentives widen the gap between formal law and enforcement practice.

2. **Agent-scale application** — the archetype framework operates at macro scale (countries, industries) but could be adapted to micro scale: classifying teams, departments, or organizational units by their incentive structure. A "predation" team (zero-sum internal competition, credit-hoarding) requires different management interventions than a "creation" team (collaborative innovation).

3. **Classification automation** — the diagnostic signals are qualitative. A quantitative classifier using observable metrics (innovation rate, competitive churn, capital allocation patterns) would enable automated archetype assignment for any economic unit with sufficient data.

4. **Dynamic transition modeling** — archetypes are not fixed. Japan transitioned from Creation (post-war) to Abundance (1980s-2000s). South Korea transitioned from Predation (pre-1997) to Creation-hybrid (post-crisis reform). The framework lacks a model for what triggers archetype transitions and how long they take.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Prevents categorical error in strategy design — no more Creation solutions for Predation problems | Archetypes are ideal types — real economies are hybrids with dominant tendencies; classification requires judgment |
| Applicable at multiple scales (country, industry, company, team) | Classification is qualitative and may lag structural changes by years |
| Simple enough to communicate to non-specialists, structural enough to guide capital allocation and policy design | "Predation" label can be value-laden; requires evidence-based application to avoid weaponization |
| Explains persistent anomalies that standard models ignore (why identical reforms produce different outcomes) | Does not prescribe precise magnitude of intervention; identifies *what* works, not *how much* |
| Connects to established theory (institutional economics, public choice, Gabaix inelastic markets) | Requires multi-disciplinary fluency (economics, political science, organizational behavior) to apply correctly |

## Relationship to Other Patterns

- **Complements:** [[docs/canonical/institutional-layer-amplification|Institutional Layer Amplification]] — archetype classification predicts how much amplification to expect; predation economies amplify legal gaps more than creation economies because extraction incentives widen the enforcement gap at every layer
- **Depends on:** None — the archetype taxonomy is self-contained

## References

- analysis §1.2 — Taxonomia de Sociedades: Criação, Abundância, Predação
- patterns #3 — Social Archetype Classification (full component model)
