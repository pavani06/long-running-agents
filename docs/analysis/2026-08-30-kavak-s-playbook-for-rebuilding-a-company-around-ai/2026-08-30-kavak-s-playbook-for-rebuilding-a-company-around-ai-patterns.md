---
title: "Reusable Agentic Patterns from Kavak's Playbook for Rebuilding a Company Around AI"
type: patterns
tags: [agentes-orquestracao, evals, harness-engineering]
date: 2026-08-30
aliases: ["kavak playbook patterns", "kavak agentic patterns"]
relates-to:
  - "[[docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-analysis|Knowledge Extraction]]"
  - "[[docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-mental-model|Mental Model]]"
sources:
  - "docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-analysis.md"
---

# Reusable Agentic Patterns from Kavak's Playbook for Rebuilding a Company Around AI

Scope: extracted from the knowledge extraction of the a16z interview "Kavak's Playbook for Rebuilding a Company Around AI". Only patterns applicable to agentic system builders (harness design, evals, agent lifecycle, human-in-the-loop, org adoption) are included; generic business strategy is excluded.

## 1. Model-Agnostic Agent-VM Harness

- **name:** Model-Agnostic Agent-VM Harness
- **problem_solved:** Harnesses tuned to the current model generation become the ceiling when a step-change model lands; organizational value from agents only compounds if each monthly model improvement converts into production value without rewrites.
- **inputs:**
  - One virtual machine per agent.
  - Memory subsystem and eval suite attached to each agent.
  - A CLI exposing every company tool and API.
  - A long-term goal per agent (e.g., maximize lifetime value).
  - A stream of new model releases arriving roughly monthly.
- **outputs:**
  - A running fleet of agents (hundreds of thousands instantiated daily).
  - Model upgrades absorbed by swapping the model behind the same harness.
  - Model capability improvements converted into company value without rewrites.
- **benefits:**
  - Model-agnostic by construction: the harness is deliberately "dumb" so it never caps smarter models.
  - Compounding: each model improvement accrues to the whole fleet at once.
  - Eliminates per-model-generation rewrite cost.
- **limitations:**
  - Prerequisite: every internal API must be rebuilt/exposed through the CLI before agents can operate the company.
  - A minimal harness provides less task-specific guidance than tuned orchestration.
  - Requires the discipline to delete profitable scaffolding that would cap future models (see pattern 5).
- **components:**
  - Per-agent virtual machine.
  - Memory subsystem.
  - Eval suite per agent.
  - Universal tool CLI over company APIs.
  - Long-term goal slot.
  - Model-swap interface.
- **flow:**
  - Provision a VM per agent instance.
  - Load memory, eval suite, and long-term goal.
  - Expose company tools and APIs through the CLI.
  - Run the agent against its goal.
  - On each new model release, swap the model without harness changes.
  - Verify behavior via evals; the improvement flows to the fleet.

## 2. Alarm-Clock Agent Lifecycle

- **name:** Alarm-Clock Agent Lifecycle
- **problem_solved:** A fleet of 100,000-200,000 long-running agents cannot run continuously; long-horizon work (tasks lasting from 3 minutes to 3 days) needs a scheduling primitive that persists agents across idle periods.
- **inputs:**
  - An agent with pending work and durable state.
  - Task durations ranging from minutes to days.
  - A next-task schedule per agent.
- **outputs:**
  - A wake-work-sleep cycle: agent wakes, works for 3 minutes to 3 days, sets an alarm for its next task, and sleeps.
  - The scheduling primitive governing the whole fleet.
- **benefits:**
  - Scales to hundreds of thousands of concurrent agent instances.
  - Agents persist toward long-horizon goals without burning continuous compute.
  - Matches multi-month customer decision cycles with intermittent effort.
- **limitations:**
  - Requires durable memory so the agent survives sleep cycles.
  - Coordinated wake times across a 200k-instance fleet add operational overhead.
- **components:**
  - Alarm scheduler.
  - Wake trigger.
  - Durable state store.
  - Work executor.
- **flow:**
  - Agent wakes on its alarm.
  - Loads context from durable memory.
  - Executes the current task (minutes to days).
  - Sets an alarm for its next task.
  - Sleeps until the next wake.

## 3. Agent-Per-Customer with Persistent Cross-Channel Memory

- **name:** Agent-Per-Customer with Persistent Cross-Channel Memory
- **problem_solved:** Task-scoped agents lose context between interactions and own no outcome; transactional optimization leaves dormant customer value unactivated.
- **inputs:**
  - Customer identity at millions-of-customers scale.
  - Every interaction stream across channels (web visits, calls, including years-old events).
  - Access to every company API and skill; humans building skills for the agents.
  - A long-term goal per customer (maximize LTV, convert across products over time).
- **outputs:**
  - One persistent agent per customer, "obsessed" with that customer, running on its own VM.
  - A long-term strategy and goal per customer informed by complete history.
  - 100,000-200,000 agents instantiated per day.
- **benefits:**
  - Complete customer history and infinite patience across multi-month decision cycles.
  - The relationship window becomes the moat instead of the transaction.
  - Activating even 1% of a dormant base via agent-driven relationship management is worth hundreds of millions.
- **limitations:**
  - Requires per-agent VM, memory, and evals: costlier than task agents.
  - Per-customer optimization must be bounded by portfolio-level constraints (risk, competing offers, portfolio health).
  - Humans shift role to skill-builders for the agents.
- **components:**
  - Per-customer agent instance on its own VM.
  - Cross-channel memory store spanning years of interactions.
  - Long-term goal (LTV maximization).
  - Skill library built by humans.
  - Full API access.
  - Portfolio constraint layer for personalized pricing/risk.
- **flow:**
  - Instantiate one agent per customer.
  - Ingest all historical cross-channel interactions into memory.
  - Set the long-term goal.
  - Act across channels and products over time.
  - Record every new interaction into memory.
  - Adjust the long-term strategy under portfolio constraints.

## 4. Goal-Driven Agents over Scripted Workflows

- **name:** Goal-Driven Agents over Scripted Workflows
- **problem_solved:** The prevailing multi-agent "expert/workflow" pattern scripts agent behavior, producing deflection bots and no outcome ownership; agents never persist toward anything.
- **inputs:**
  - A hard, measurable goal (e.g., 2x profits, maximize LTV).
  - Full tool/API access.
  - Persistence across the task horizon.
- **outputs:**
  - Agents that decompose the goal into their own plans and persist toward it, rather than executing a workflow DAG.
  - Explicit outcome ownership by the agent.
- **benefits:**
  - Exploits agent structural advantages in complex sales: infinite patience, complete history, long-horizon planning, no fatigue.
  - Changes what architecture you build (mega-expert vs. deflection bot).
  - Targets superhuman performance on the hardest problems (2.1x conversion vs. human team; tripled NPS/CSAT).
- **limitations:**
  - Goal compliance is harder to verify than workflow compliance; requires outcome-level evals (pattern 11).
  - Task-scoped agents remain simpler for narrowly scoped work.
  - Presupposes the superhuman bar; incremental "good enough" targets pull back toward workflows.
- **components:**
  - Hard goal specification.
  - Agent-owned planner.
  - Persistence layer.
  - Outcome evaluation.
- **flow:**
  - Assign a hard, measurable goal to the agent.
  - Agent decomposes the goal into its own plan.
  - Agent persists across the horizon toward the goal.
  - Measure the agent on outcome attainment, not step compliance.

## 5. Scaffold Deletion on Model Step-Change

- **name:** Scaffold Deletion on Model Step-Change
- **problem_solved:** Orchestration graphs and lattices tuned to current model capability become a ceiling when a frontier step-change lands (observed trigger: Opus 4.5); the smarter the model, the less scaffolding it wants.
- **inputs:**
  - Model release events, especially capability step-changes.
  - Existing working (even profitable) orchestration infrastructure.
  - An eval suite covering current fleet behavior.
- **outputs:**
  - Deleted scaffolding: two years of working, profitable multi-agent infrastructure removed rather than left capping future models.
  - A rebuilt minimal harness (VM + memory + evals + full API access).
  - Verified behavior preservation via evals.
- **benefits:**
  - Removes the harness ceiling ahead of each model step-change.
  - Converts model jumps into fleet-wide gains instead of lock-in.
  - Keeps the harness the compounding asset rather than the depreciating one.
- **limitations:**
  - Deleting working, profitable infrastructure requires unusual organizational willpower.
  - Only safe when evals already cover behavior (pattern 9/10 are prerequisites).
  - Sacrifices task-specific optimizations the scaffolding encoded.
- **components:**
  - Model-capability watch (step-change detection).
  - Scaffold inventory.
  - Eval regression suite.
  - Deletion/rebuild policy.
- **flow:**
  - Observe a model capability step-change.
  - Identify scaffolding tuned to the prior capability level.
  - Confirm evals cover current behavior.
  - Delete or replace the scaffolding with a minimal harness.
  - Re-run evals to confirm behavior is retained or improved.

## 6. Shared Fleet Learning

- **name:** Shared Fleet Learning
- **problem_solved:** Per-agent learning means the same mistake is repeated across ~200,000 instances; individual agents cannot benefit from each other's errors.
- **inputs:**
  - A mistake/error signal from any single agent.
  - A feedback aggregation and distribution channel.
  - A shared harness/skill substrate across the fleet.
- **outputs:**
  - The entire fleet (~200k agents) learns from one agent's mistake by the next day.
  - Fleet-level behavior change, not per-agent improvement.
- **benefits:**
  - Each mistake costs the fleet only once.
  - Improvement compounds at fleet scale with every error.
  - Turns production failures into a training asset.
- **limitations:**
  - Requires a centralized feedback pipeline shared by all instances.
  - Propagation lag up to one day.
  - Depends on all agents running a common substrate so updates apply uniformly.
- **components:**
  - Error capture at the agent level.
  - Feedback aggregation layer.
  - Fleet-wide update distribution.
  - Next-day propagation mechanism.
- **flow:**
  - One agent makes a mistake.
  - Capture the error signal.
  - Aggregate it into a fleet-level update (skill/memory/policy).
  - Distribute the update to all instances.
  - Fleet behaves differently by the next day.

## 7. Closed-Loop Help API (Humans Serve Agents)

- **name:** Closed-Loop Help API (Humans Serve Agents)
- **problem_solved:** The standard escalation pattern (agent stuck, hand off to a tier-2 human queue, case forgotten) never closes the loop and generates no training data, so the system plateaus.
- **inputs:**
  - A stuck agent.
  - A help API the agent can call.
  - A human answering on the other side.
- **outputs:**
  - The resolution flowing back into the agent that asked.
  - Training data generated from every escalation.
  - Human teams organized to serve agents (org-chart inversion).
- **benefits:**
  - Closes the loop that open-loop escalation leaves open.
  - Every stuck moment becomes a learning signal.
  - Human teams serving agents outperform the reverse arrangement.
- **limitations:**
  - Restructures human work around agent demand.
  - Requires humans available on the agent's schedule, not a batch queue.
  - Only worth it where the returned resolution can actually be captured as data.
- **components:**
  - Help API endpoint.
  - Human responder pool.
  - Resolution-return channel into the agent.
  - Training-data capture on each resolution.
- **flow:**
  - Agent gets stuck.
  - Agent calls the help API.
  - A human answers.
  - Resolution flows back into the agent.
  - The interaction is recorded as training data.
  - Agent continues; fleet learning may propagate the fix (pattern 6).

## 8. Sidekick Pattern at Physical Boundaries

- **name:** Sidekick Pattern at Physical Boundaries
- **problem_solved:** Dexterity and physical senses are irreplaceable for some work (~800 mechanics); full automation is impossible at physical handoff points (handing over car keys).
- **inputs:**
  - The same scaling harness used for autonomous agents.
  - A human performing physical work.
  - Procedure knowledge and tips (e.g., inspection procedure).
  - Progress telemetry returned by the human.
- **outputs:**
  - An agent riding along, guiding the human through procedures.
  - Outcome telemetry feeding back into the agent/evals.
  - Humans retained only where physical presence is required (96% of interactions and 95% of transactions fully agent-handled).
- **benefits:**
  - Inspection quality up; faster and cheaper repairs; warranty costs down ~20-26%; CSAT up.
  - Reuses the identical harness as the autonomous fleet; no parallel stack.
  - Extends agent leverage into physical work without robotics.
- **limitations:**
  - Applies only where physical presence is genuinely required.
  - Quality depends on the depth of procedure knowledge encoded.
  - Requires humans to accept agent guidance in their craft.
- **components:**
  - Agent instance in the standard harness.
  - Guidance interface for the human ("Ratatouille"/El Mike arrangement).
  - Procedure/skill library.
  - Telemetry return channel (voice notes as progress signal).
- **flow:**
  - Human starts a physical task.
  - Agent rides along in the same harness.
  - Agent guides the procedure and supplies tips.
  - Human returns progress telemetry (voice notes).
  - Outcomes feed evals and fleet learning.

## 9. Evals-as-Brakes

- **name:** Evals-as-Brakes
- **problem_solved:** The default response to AI risk is slowing down; companies that go slow do so because they lack brakes, so velocity stays capped by fear instead of governed by measurement.
- **inputs:**
  - Investment in eval quality (engineering time, tokens, money).
  - A velocity ambition for shipping agents.
- **outputs:**
  - A gas/brake coupling rule: "You only hit the gas if you have the right brakes."
  - Permitted shipping speed as a function of eval quality.
- **benefits:**
  - Maximum speed becomes a function of eval quality rather than risk appetite.
  - Risk is governed by measurement, not throttling.
  - The correct response to risk becomes building better brakes (evals), not going slower.
- **limitations:**
  - Eval parity halves effective builder capacity (see pattern 10).
  - Evals must be designed with the agent, not bolted on post-deployment; deferring them caps achievable speed anyway.
  - Bad evals give signal without truth and unlock false speed.
- **components:**
  - Eval suite (the brakes).
  - Deployment velocity policy (the gas).
  - Coupling rule tying permitted velocity to eval coverage.
- **flow:**
  - Invest in eval quality before accelerating.
  - Measure eval coverage of failure modes.
  - Set permitted velocity as a function of that coverage.
  - Hit the gas only when the brakes hold.
  - On failure, improve the brakes rather than permanently slowing down.

## 10. Eval-Investment Parity

- **name:** Eval-Investment Parity
- **problem_solved:** Evals treated as an afterthought cap the scale and speed an agent fleet can safely reach.
- **inputs:**
  - The engineering time, tokens, and money budget for building agents.
  - A parity rule: roughly equal allocation to evals.
- **outputs:**
  - Evals as first-class artifacts co-designed with the agents.
  - A ~50/50 split of time/tokens/money between agents and their evals.
- **benefits:**
  - Unlocks scale: getting to hundreds of thousands of agents requires evals designed with the agent.
  - Makes speed safe (feeds pattern 9).
  - Halves effective builder capacity by explicit, accepted decision rather than silent neglect.
- **limitations:**
  - Halves effective builder capacity; leadership must accept "50% non-product" spend.
  - Requires sustained discipline, not a one-time allocation.
- **components:**
  - Agent build track.
  - Eval build track.
  - Parity budget rule (time, tokens, money).
  - Deployment gate keyed on evals.
- **flow:**
  - Plan the agent build.
  - Allocate equal time, tokens, and money to eval construction.
  - Build agent and evals in parallel.
  - Gate deployment on eval results.

## 11. Outcome-Level Eval Hierarchy

- **name:** Outcome-Level Eval Hierarchy
- **problem_solved:** Superficial KPIs (number of calls, minutes on call) give signal without truth; most things break at the conversion level, which those metrics never surface.
- **inputs:**
  - Business-result data: did the customer convert, are they happy to re-engage.
  - The agentic architecture and its skill set as optimization variables.
- **outputs:**
  - First-order eval anchored on business results.
  - Architecture optimizations and skill additions ordered by outcome impact.
- **benefits:**
  - Truth-anchored optimization: rejects vanity metrics explicitly.
  - Directly links agent changes to business value.
  - Provides the measurement foundation for goal-driven agents (pattern 4).
- **limitations:**
  - Requires instrumentation of conversion/CSAT-type outcomes end to end.
  - Outcome attribution can lag behind the agent change that caused it.
  - Proxy KPIs remain tempting because they are cheaper to collect.
- **components:**
  - Business-result metrics (conversion, willingness to re-engage).
  - Agentic architecture metrics.
  - Skill-addition loop driven by outcome gaps.
- **flow:**
  - Define the business outcome metric for the agent's goal.
  - Measure the agent on that outcome.
  - If below bar, optimize the agentic architecture.
  - Add skills where outcomes reveal gaps.
  - Re-measure the outcome; never substitute proxy KPIs.

## 12. Mega-Expert Consolidation

- **name:** Mega-Expert Consolidation
- **problem_solved:** A specialist organization (~15 specialists across 15 teams: financing, car advisory, buying, insurance, trade-in quoting) fragments the customer experience across handoffs.
- **inputs:**
  - The enumeration of specialist domains.
  - Per-domain agent candidates.
  - A benchmark against the best individual human expert per domain.
- **outputs:**
  - One agent per specialty that beats the best individual expert.
  - A single fused "mega expert" facing the customer.
- **benefits:**
  - One coherent customer-facing interface with complete cross-domain knowledge.
  - Each component proven superhuman before fusion, de-risking the consolidation.
  - The superhuman bar changes the architecture built (mega-expert instead of deflection bot).
- **limitations:**
  - Prerequisite cost: each specialty agent must first outperform the best human ever hired in that domain.
  - Fusion is harder than the sum of its parts; evaluation must remain at the outcome level (pattern 11).
  - Not applicable where shallow task coverage is sufficient.
- **components:**
  - Per-specialty agents.
  - Best-human benchmark per specialty.
  - Fusion layer into a single agent.
  - Unified customer interface.
- **flow:**
  - Enumerate the specialist domains the org employs.
  - Build one agent per domain.
  - Verify each beats the best individual human expert.
  - Fuse the specialists into a single mega expert.
  - Face the customer with the unified agent.

## 13. Production-Contact Training Loop

- **name:** Production-Contact Training Loop
- **problem_solved:** Lab-only agents do not converge; synthetic or historical data cannot substitute for real interaction distributions.
- **inputs:**
  - Agents placed in front of real customers.
  - Interaction-data harvesting infrastructure.
  - Evals over the harvested interactions.
- **outputs:**
  - Agents trained on the real customer distribution.
  - Harvested data and feedback loops (which are the agents, not merely groundwork for them).
- **benefits:**
  - The only mechanism observed to make agents work at all.
  - Convergence to real customer behavior instead of lab assumptions.
  - Every production interaction becomes training material.
- **limitations:**
  - Real-customer exposure carries risk; requires evals as brakes first (pattern 9).
  - Requires data harvesting and eval infrastructure before scale.
  - Failure modes encountered in production become the curriculum.
- **components:**
  - Production exposure channel.
  - Interaction-data harvester.
  - Eval loop over interactions.
  - Training/update pipeline back into the fleet.
- **flow:**
  - Put the agent in front of real customers.
  - Harvest interaction data and eval signals.
  - Train/update the agent on that loop.
  - Redeploy to production.
  - Repeat; the loop is the training mechanism.

## 14. Carve-Out Pilot with Hard P&L Target

- **name:** Carve-Out Pilot with Hard P&L Target
- **problem_solved:** Proving that an agent can run operations is unsafe and unmeasurable if attempted company-wide at once; diffuse bottom-up pilots (hackathons, sponsored use cases) produce no target org design.
- **inputs:**
  - One isolated city as a contained experiment.
  - An agent installed in the standard harness as CEO.
  - A hard P&L target (goal: 2x profits in month one).
  - Every physical worker in the unit as plan executor and telemetry source.
- **outputs:**
  - 1.5x profits in six weeks (against a 2x month-one goal).
  - All KPIs moved: CSAT, inventory quality, rotation, financing penetration.
  - Daily plans pushed to every physical worker; voice notes returned as progress telemetry.
- **benefits:**
  - Contained blast radius with real P&L truth as the readout.
  - Value mechanism made visible: perfect forecasting over every number and customer plus daily micromanagement of execution.
  - Reuses the standard harness, proving it at management altitude.
- **limitations:**
  - Value comes from depth (enumerate every number and customer), not altitude; the pattern is demanding to replicate.
  - Requires a genuinely isolatable operating unit.
  - Missed the headline target (1.5x vs 2x); results take weeks, not days.
- **components:**
  - Isolated scope (one city).
  - Agent CEO running in the standard harness.
  - Hard P&L target.
  - Daily plan push channel to workers.
  - Voice-note telemetry return.
  - KPI dashboard.
- **flow:**
  - Pick one contained operating unit (a city).
  - Install an agent as its CEO in the standard harness.
  - Set a hard P&L target with a deadline.
  - Agent enumerates every number and customer, then forecasts.
  - Agent pushes daily plans to every physical worker.
  - Workers return voice notes as progress telemetry.
  - Agent micromanages execution daily against plan.
  - Read results on P&L and KPIs.
