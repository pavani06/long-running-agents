---
title: "Knowledge Extraction: Kavak's Playbook for Rebuilding a Company Around AI"
type: analysis
tags: [agentes-orquestracao, evals, harness-engineering]
date: 2026-08-30
aliases: ["extracao kavak playbook", "kavak playbook knowledge extraction"]
relates-to:
  - "[[docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-mental-model|Mental Model]]"
sources:
  - "Raw-Knowledge/sources/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai.md"
---

# Knowledge Extraction: Kavak's Playbook for Rebuilding a Company Around AI

Source: a16z interview 'Kavak's Playbook for Rebuilding a Company Around AI' (2026-08-10, 36:31, video_id n34CIw3gk1k)

Synthesized from 4 chunk analyses (header/beginning/middle/end of interview). Chunk 0 contained only frontmatter metadata; all extractable content comes from chunks 1-3.

## 1. Frameworks & Models

### 1.1 The 2035 design question
- Anchor question: "how would we build this company in 2035 with GPT-10-level intelligence?" — not incremental improvement of the current company.
- The answer looks structurally different from the existing company; that gap defines the transformation scope.

### 1.2 Three-decision framework for becoming agent-run
1. **Redesign the whole company around agents** — not layering AI onto the existing structure. Requires rebuilding most APIs and internal systems so agents can operate them, plus generating the data/feedback loops to teach agents.
2. **Bet on superhuman agents** — the bar is outperforming the best human ever hired on every dimension that matters (conversion, LTV, customer experience), deployed against the hardest problems, not the easiest.
3. **Change how success is measured** — shift from transactional metrics (cars bought/sold, brake pads purchased) to relational metrics (agents assigned to the customer database with the task of maximizing lifetime value).

### 1.3 Greenfield org-design axiom
- Design the organization from scratch assuming abundant, cheap superintelligence; never retrofit AI onto the legacy org. (The org-design corollary of the 2035 design question; stated independently in the interview.)

### 1.4 Evals-as-brakes model
- Maximum speed is a function of eval quality: "You only hit the gas if you have the right brakes."
- The correct response to AI risk is building better brakes (evals), not going slower.

### 1.5 Economic reframing: tokens as the unit of labor
- Kavak invests more in tokens than in knowledge workers; tokens are treated as the primary unit of labor investment. The human role shrinks to physical-presence and leadership interfaces.

### 1.6 Relational economics
- With a large customer base and high-ticket products, activating even 1% of the dormant base via agent-driven relationship management is worth hundreds of millions. This is why agent-per-customer beats transactional optimization for their industry.

### 1.7 Token-value tiering (AI cost accounting)
- **Tier 3**: tokens burned by production agents doing the company's actual work — per-token ROI directly measurable.
- **Tier 2**: value measurable indirectly (dev copilot tokens → value read through the codebase).
- **Tier 1**: generic chat/IDE usage, value unknown — where most companies sit while calling it "adoption."

### 1.8 Carve-out city pilot ("AI CEO")
- Isolate one city as a contained experiment; install an agent in the standard harness as its CEO, with a hard P&L target (goal: 2x profits in month one; got 1.5x in six weeks).
- Value mechanism: perfect forecasting over every number and customer plus daily micromanagement of execution — daily plans pushed to every physical worker, voice notes returned as progress telemetry. All KPIs moved (CSAT, inventory quality, rotation, financing penetration).

### 1.9 Self-improving organization (RSI reframe)
- 4,000 years of economic value came from organizations, not individuals — so aim the recursive self-improvement loop at the organization (harness + evals + agents absorbing each new model), yielding an exponential in company value, not just in intelligence.

### 1.10 Schumpeterian creative destruction applied to AI
- Innovation reaches the economy via new AI-native companies destroying incumbents, not via incumbent adoption, because deep adoption requires a CEO to destroy decades of prior building. Incumbent refusal is exactly the startup wedge.

### 1.11 General-purpose technology adoption curve (electricity/dynamo analogy)
- When electricity arrived, factories kept their old architecture (four floors, shafts, belts) and merely swapped the coal engine for an electric one → ~6% efficiency gain.
- The full gain (~3x productivity, which powered 20th-century US growth) only came from destroying the factory and rebuilding around the technology: flat single-floor layout, relocation out of dense city centers (NYC → Connecticut/New Jersey), redesigned around small distributed dynamos.
- Ford's production-line technology existed by ~1879–1881 (Edison's dynamo); the factory could have been built 40 years earlier. Technology existing ≠ adoption; the gap is organizational redesign, and that gap is the moat/opportunity.
- The same pattern repeated with computers and is repeating with AI: value capture is gated by complementary redesign of the surrounding structure, not by the technology itself. Framed as "the innovator's dilemma at an industrial scale."

### 1.12 Conservative extrapolation heuristic
- When imagining the future to build for, don't assume exponential AI progress. Map the conservative case: "if AI keeps getting better at a linear scale, build for that."
- Even the linear-trend baseline yields valuable ideas — de-risks forecasts against hype curves and makes the business case robust to slower-than-hyped capability growth.
- Resolution with the 2035/GPT-10 question: the future-state design is the aspirational target that defines scope; the linear baseline is the planning floor that guarantees the case survives.

## 2. Patterns & Architectures

### 2.1 Agent-per-customer, not agent-per-task
- Each customer gets one persistent agent "obsessed" with them (at millions-of-customers scale), running on its own virtual machine, with access to every company API and skill; humans build skills for these agents.
- Scale: 100,000–200,000 agents instantiated per day.

### 2.2 Persistent cross-channel memory + long-term goal
- The agent remembers years of interactions (web visits, a call from two years ago) and uses this to set a long-term strategy and goal (maximize LTV, convert across products over time).

### 2.3 Long-running goal-driven agents, not workflow agents
- Explicit architectural bet against the prevailing multi-agent "expert/workflow" pattern. Agents hold hard goals (not scripted workflows) and persist toward them.

### 2.4 Alarm-clock lifecycle
- Agents wake, work for durations ranging from 3 minutes to 3 days, set an alarm for their next task, and sleep. This is the scheduling primitive for the fleet.

### 2.5 Agent-VM harness (post-Opus-4.5 rebuild)
- Each agent runs in a virtual machine with memory, evals, and a CLI exposing every tool/API in the company; hundreds of thousands instantiated daily, each with a long-term goal (e.g., maximize lifetime value).
- Design constraint: the harness must absorb smarter models arriving monthly without rewrites (model-agnostic by construction).

### 2.6 Mega-expert consolidation
- The old org required ~15 specialists in 15 teams (financing, car advisory, buying, insurance, trade-in quoting). Pattern: first build an agent that beats each individual expert, then fuse them into a single "mega expert" that faces the customer.

### 2.7 Shared fleet learning
- When one agent makes a mistake, the entire fleet (~200k agents) learns from it by the next day — feedback propagates across instances, not per-agent.

### 2.8 Closed-loop human-in-the-loop ("I need help" API)
- The standard pattern (agent stuck → escalate to tier-2 human queue → case forgotten) fails because the loop never closes and no training data is generated.
- Correct inversion: the stuck agent calls a help API; a human answers on the other side; resolution flows back into the agent. In org-chart terms: human teams that serve an agent outperform the reverse.

### 2.9 Sidekick pattern for physical work ("Ratatouille" / El Mike)
- Same scaling harness, agent rides along guiding a human mechanic (inspection procedure, tips). Used where dexterity/senses are irreplaceable (~800 mechanics).
- Results: inspection quality up, faster/cheaper repairs, warranty costs down ~20–26%, CSAT up.

### 2.10 Three-role team topology
- Flat, senior, empowered pods mixing engineering + AI + operations; every person either builds agents, works for agents, or is physical-world/customer-facing.

### 2.11 Human-in-the-loop only at physical boundaries
- 96% of interactions and 95% of transactions fully agent-handled; humans remain only where physical presence is required (handing over car keys).

### 2.12 Eval-investment parity rule
- Roughly equal engineering time, tokens, and money spent building evals as building the agents themselves. Evals are a first-class artifact, not an afterthought.

### 2.13 Outcome-level eval hierarchy
- First-order eval is business results — did the customer convert, are they happy to re-engage — then optimize the agentic architecture and add skills. Explicitly rejects superficial KPIs (call counts, call minutes).

### 2.14 Deep personalization under portfolio constraints
- Interest rate, risk, and max loan amount are personalized per customer, but optimized against the risk level, competing offers the customer is seeing, and the health of the portfolio as a whole.

### 2.15 Structure-determines-yield
- The same technology injected into two different organizational architectures produces categorically different returns (6% vs 3x). The architecture — physical layout then, company/process design now — is the binding constraint on value capture, not the tool.

### 2.16 Distributed-unit design
- The winning factory redesign moved from centralized power source (one coal engine driving all shafts) to small dynamos distributed across a flat layout — the architectural analogue being distributed, small-scale compute/agents throughout the company rather than a bolted-on central AI layer.

## 3. Operational Lessons

- **Agents are taught by exposure**: the only way to make agents work is putting them in front of real customers, harvesting the interaction data and evals, and training on that loop. Lab-only agents don't converge.
- **Build sales agents, not support agents**: Kavak never built customer service agents; they targeted the highest-leverage task (selling high-ticket items) directly. Counter-intuitively, this is where agents delivered tripled NPS/CSAT and 2.1x conversion vs. the human team (initially 1.5x).
- **Structural advantage of agents in complex sales**: infinite patience, complete customer history, long-horizon planning, no fatigue — properties humans cannot match in multi-month purchase cycles (customers take 3–4 months to decide on car + loan).
- **Long decision cycles are an asset**: knowing the customer throughout a multi-month decision process drives conversion and retention "through the roof" — the relationship window is the moat, not the transaction.
- **Regulated fintech end-to-end is tractable**: underwriting thin/no-file customers, pricing, and servicing all run through agents; loan approval went from ~2 months (Mexico/emerging-market baseline) to under 3 minutes, enabled by aggregated data on both customer and car.
- **Vertical integration as credit-risk mitigant**: if a customer can't pay, they return the car and receive a cheaper one with smaller payments — the asset backs the loan and keeps the customer "out of the water."
- **Company-wide agent literacy (Jedi Academy)**: 6-week program for everyone from CEO to mechanics; graduates ship state-of-the-art agents to production. Continuously redesigned in-house (content too new for Stanford et al.), led personally by leadership.
- **AI-CEO value comes from depth, not altitude**: enumerate every number and customer, forecast perfectly, micromanage daily execution against plan.
- **Retraining as explicit forced choice**: tell each function exactly what will change; offer training or exit. Delivered this way it strengthened culture rather than causing attrition.
- **Don't outsource agentic upskilling**: the curriculum doesn't exist externally; design and iterate it internally.
- **Transformation must be top-down**: bottom-up cannot generate the taste/strategy for what to build. Hackathons + sponsored use cases don't work. Fix the 3–5-year target state and drive vertically (army metaphor: soldiers don't each choose strategy).
- **Account for token quality, not token volume**: attribute spend by tier and push usage up the tier ladder; iterate.
- **Realistic reskilling outcome**: most graduates won't become AI engineers; the actual requirement is fluency collaborating with agentic systems.
- **Superficial adoption measurably caps out**: tooling swapped into unchanged processes yields single-digit improvements (6–10%); expect 10x-class gains only from redesigning workflows, org structure, and processes around agents.
- **Frontier intelligence is effectively free ($20/month)**: access is not the differentiator — depth of adoption and imagination of the rebuilt process is.
- **Timing lesson from prior venture** (Oppy Analytics, 2013, pre-transformers ML for Fortune 500 risk/logistics/forecasting): being 10 years early meant the vision was right but the substrate (transformers/LLMs) was missing — the current bet is sized to the technology actually being available.

## 4. Tradeoffs

- **Retrofit vs. rebuild**: adopting AI while leaving org structure intact yields no efficiencies and the same customer problems. Cost side: rebuilding most APIs and systems so agents can operate them — a prerequisite, not an option.
- **Speed vs. safety, resolved via evals**: companies that go slow do so because they lack brakes (evals). The alternative is investing in eval quality to unlock speed, accepting that eval parity halves effective builder capacity.
- **Tokens vs. knowledge workers**: capital allocation shifted toward tokens; the human role shrinks to physical-presence and leadership interfaces.
- **Individual personalization vs. portfolio integrity**: per-customer optimization must be bounded by portfolio-level risk constraints — agent autonomy in pricing is constrained by systemic objectives.
- **Superhuman bar vs. incremental automation**: targeting "better than the best human ever hired" on hard problems, rather than "good enough" on easy problems, changes what architectures you build (mega-expert vs. deflection bot).
- **Orchestration graph vs. minimal harness**: multi-agent graphs/lattices constrain frontier intelligence — the smarter the model, the less scaffolding it wants. Kavak deleted two years of working, profitable multi-agent infrastructure rather than let the harness cap future models.
- **Task-scoped vs. customer-scoped agents**: task agents are simpler; customer agents require per-agent VM/memory/evals but persist context and own outcomes (LTV).
- **Escalation-to-humans vs. humans-serving-agents**: tier-2 escalation loses the learning signal; the help-API inversion generates closed-loop data but restructures human work around agents.
- **Incumbent adoption vs. AI-native rebuild**: deep adoption means destroying legacy structure; most CEOs refuse — which is exactly the startup wedge.
- **Superficial adoption vs. deep redesign**: superficial = low disruption, preserves existing structure → bounded ~6–10% gain. Deep = "destroying the factory" (restructuring processes, changing where and how work happens) → 3x–10x gain at the cost of near-total organizational rebuild.

## 5. Failure Patterns

- **The ChatGPT bolt-on trap**: first-instinct failure mode — keep the structure as-is, hand chat tools to the team, expect efficiency. Result: nothing happens, same customer problems, no measurable change. This is where "many companies are stuck."
- **Drop-in substitution**: adopting the new engine while keeping shafts-and-belts processes (old factory layout as proxy for pre-AI org design) — the default incumbent behavior that locks in marginal gains.
- **Unwillingness to redesign**: wanting the benefits while refusing the structural change; the innovator's-dilemma trap where the old structure's sunk cost prevents capturing the new technology's real multiplier.
- **Superficial KPI measurement**: measuring number of calls or minutes on call gives signal without truth; most things break at the conversion level, which those metrics never surface.
- **Slowing down as risk response**: treating AI risk by throttling velocity instead of building eval capacity — the wrong inversion of the speed/brakes relationship.
- **Evals as afterthought**: getting to scale requires evals designed with the agent, not bolted on post-deployment; deferring them caps achievable speed.
- **Right idea, wrong substrate**: a correct 2013 thesis about ML solving complex problems failed on timing because the model class (pre-transformer ML) wasn't sufficient — betting ahead of capability curves is a distinct failure mode from betting wrong.
- **Open-loop escalation**: agent hands off to a human queue and forgets → no improvement data → system plateaus.
- **Equating adoption with value**: heavy token spend at tier 1 with zero ROI attribution.
- **Hackathon/use-case-sponsorship transformation**: diffuse bottom-up effort with no target org design.
- **Harness lock-in**: orchestration graphs tuned to current model capability become the ceiling when a step-change model lands (trigger observed: Opus 4.5).
- **Assuming external institutions can teach agentic engineering**: the curvature of the field outruns academia.

## 6. Synthesis

Cross-cutting insights the author may not have named:

1. **The harness is simultaneously the depreciating asset and the compounding asset.** Two years of profitable multi-agent infrastructure was deleted because scaffolding tuned to current models becomes a ceiling (Opus 4.5 as the observed trigger); the rebuilt VM + memory + evals + full-API-access harness is valuable precisely because it is dumb — model-agnostic, it converts each monthly model improvement into company value without rewrites. This is the mechanical link between the RSI-organization reframe and the adoption-curve analogy: the organization, not the model, is the thing that must compound.
2. **Evals are the currency that converts model capability into organizational velocity.** Evals appear in three independent roles — brakes (govern speed), parity rule (allocate capacity), outcome hierarchy (define truth) — and every failure mode involving measurement (superficial KPIs, tier-1 "adoption," slowing-down-as-risk-response) is a variant of missing or mis-anchored evals.
3. **The inversion pattern: humans serve agents.** The help API, the three-role topology, the sidekick/Ratatouille pattern, and skill-building humans all reverse the default direction of service. Escalation-to-human and agent-as-assistant are the same structural error viewed from two sides: both open the loop and lose the learning signal.
4. **Structure-determines-yield is the master key.** The electricity analogy (6% vs 3x), the ChatGPT bolt-on trap, the hackathon failure, the incumbent-refusal wedge, and the Schumpeterian prediction are all one theorem restated: the binding constraint on GPT value capture is complementary organizational redesign, never the technology. The 40-year electricity-to-Ford lag is the proof that this constraint is historical, not hypothetical.
5. **All learning requires production contact.** Lab-only agents don't converge; closed-loop escalation is the data-generation mechanism; fleet learning propagates per-mistake across ~200k instances. The architecture is inseparable from its data feedback loops — the three-decision framework's "rebuild APIs and generate feedback loops" is not groundwork for the agents, it is the agents.
6. **Design aspirationally, plan conservatively.** The apparent contradiction between the 2035/GPT-10 superhuman bet and the conservative linear-extrapolation heuristic resolves as two different instruments: the future-state design defines scope of rebuild; the linear baseline guarantees the business case survives even if capability growth disappoints. Exponential upside becomes bonus, not dependency.
7. **The moat is organizational, not technological.** Frontier intelligence is a $20/month commodity; what incumbents cannot replicate is a CEO willing to destroy decades of prior building — which is why the wedge for AI-native startups is the incumbents' own sunk cost.
