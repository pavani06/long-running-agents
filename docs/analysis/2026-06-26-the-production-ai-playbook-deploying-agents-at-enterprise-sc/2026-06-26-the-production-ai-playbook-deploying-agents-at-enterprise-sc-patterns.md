---
title: "The Production AI Playbook — Reusable Patterns"
type: analysis
date: 2026-06-26
aliases: ["production AI playbook patterns", "Bhaumik production patterns", "enterprise agent patterns", "5-pillar patterns"]
tags: ["evals", "agentes-orquestracao", "production", "governanca", "monitoramento"]
relates-to: ["[[docs/analysis/2026-06-26-the-production-ai-playbook-deploying-agents-at-enterprise-sc/2026-06-26-the-production-ai-playbook-deploying-agents-at-enterprise-sc-analysis|Production AI Playbook Analysis]]", "[[docs/canonical/eval-tier-stratification|Eval Tier Stratification]]", "[[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]]", "[[docs/canonical/production-grounded-eval-sampling|Production-Grounded Eval Sampling]]", "[[docs/canonical/deterministic-tool-dispatch|Deterministic Tool Dispatch]]", "[[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]]", "[[docs/canonical/pain-signal-eval-progression-gate|Pain-Signal Eval Progression Gate]]"]
---

# The Production AI Playbook — Reusable Patterns

Padrões extraídos da talk "The Production AI Playbook: Deploying Agents at Enterprise Scale" por Sandipan Bhaumik (Databricks), aplicáveis a sistemas agenticos em produção.

---

## 1. 3-Layer Evaluation Architecture

**problem_solved:** Agents can produce correct outputs via incorrect or wasteful execution paths; evaluating only the final answer (semantic quality) hides expensive behavioral failures (redundant tool calls, loops, unnecessary API consumption) that surface only under production scale.

**inputs:**
- Agent execution traces (tool calls, API invocations, intermediate decisions)
- Agent response outputs (text, structured data)
- Schema definitions for expected output formats
- PII taxonomy from the data catalog
- Golden answers from the living eval dataset

**outputs:**
- Layer 1 (Deterministic) verdict: regex/pattern match on output format, PII presence, schema validity — zero LLM cost
- Layer 2 (Semantic/LLM-as-Judge) verdict: groundedness, safety, relevance, faithfulness scores via LLM evaluation
- Layer 3 (Behavioral) verdict: tool call redundancy count, loop detection flag, duplicate API detection, path efficiency score
- Stratified pass/fail gating at each layer with independent frequency controls per layer

**benefits:**
- Catches the "right answer, wrong path" failure mode invisible to semantic-only evaluation
- Layer 1 blocks known failure modes (PII leaks, malformed outputs) at near-zero cost in CI
- Layer 2 catches quality regressions before they reach production with moderate LLM cost
- Layer 3 reveals the per-query cost profile of the agent, enabling cost optimization before scale
- Stratification allows each layer to run at its own frequency (every PR vs. merge-only), controlling eval cost

**limitations:**
- Layer 3 requires full execution traces from all tool calls and API invocations — adds engineering complexity to the tracing pipeline
- LLM-as-Judge (Layer 2) introduces its own evaluation error rate; it can endorse bad responses or flag good ones
- Behavioral eval is expensive to run on every commit; requires cost governance (stratified subset in CI, full suite on merge)
- The three layers must be designed together — adding Layer 3 post-hoc to an existing system requires retrofitting trace collection

---

## 2. Eval-Driven Development Timeline (Model-Selection-Last)

**problem_solved:** Model selection decisions made before evaluation infrastructure exists are based on intuition and public benchmarks (MMLU, HumanEval), not on domain-specific performance — resulting in weeks of subjective debate and suboptimal model choices for the actual production domain.

**inputs:**
- ~200 real production queries with golden answers (human agent responses)
- Candidate models to evaluate (any number, any provider)
- Centralized eval infrastructure (Layers 1-3) built in weeks 1-6
- Tracing and data foundation pipelines

**outputs:**
- Week 7: data-driven model comparison report ranking all candidates by performance against the enterprise eval dataset
- Selected model with domain-specific performance evidence (not intuition or public benchmarks)
- Model-switching infrastructure that can re-run the comparison whenever a provider updates their model

**benefits:**
- Eliminates subjective model debates: "weeks of debate replaced by hours of data-driven comparison"
- Model is chosen based on how it performs on your data, your domain, your failure patterns — not on MMLU scores
- The same eval dataset that selected the model also serves as the regression suite for every subsequent change
- Model switching becomes mechanical: run new model against eval dataset, compare scores, decide

**limitations:**
- Requires organizational discipline to invest 6 weeks in evaluation infrastructure before any model experimentation
- The initial ~200 golden answers must come from human agents, creating a bootstrapping dependency on operational staff
- If the domain evolves rapidly, an eval dataset built on historical queries may not represent emerging query patterns
- The timeline assumes a greenfield project; retrofitting into an existing agent system may require different phasing

---

## 3. Living Eval Dataset

**problem_solved:** Static test suites do not catch regressions from new failure modes discovered in production — each incident teaches a lesson that is lost unless codified as a permanent test case that prevents reoccurrence.

**inputs:**
- Initial ~200 golden answer pairs (human agent query + correct response)
- Every production incident's failure trace and root cause analysis
- Every new feature specification
- Dataset categorization taxonomy (security, login, tool calls, knowledge retrieval, math/reasoning)
- Ownership assignment per category

**outputs:**
- Monotonically growing eval dataset (never shrinks; obsolete cases archived, not deleted)
- Per-category test suites with independent ownership and maintenance cycles
- Partitioned execution plans: fast subset for CI (stratified sample across categories), full suite for merge to main
- Traceable lineage from every test case back to the incident or feature that created it

**benefits:**
- "Every incident leaves a permanent scar in the test suite — that scar prevents the same failure from happening twice"
- Monotonic growth means the system gets strictly safer over time; each failure invests in future quality
- Categorization and ownership prevent the dataset from becoming an unmanageable monolith
- Cost-controlled execution (stratified CI subset vs. full suite on merge) keeps eval economically sustainable

**limitations:**
- Unchecked growth without maintenance leads to an uncategorized monolith that is expensive to run and hard to govern
- Requires a human or automated process to convert each production incident into a well-formed test case — raw incident logs are not test cases
- Golden answers must be authored or reviewed by humans to avoid training the eval against model-generated hallucinations
- The dataset must be actively groomed; test cases for deprecated features must be archived (not deleted, for traceability)

---

## 4. Production Incident → Eval Flywheel

**problem_solved:** Production failures in agentic systems are treated as one-off incidents to be fixed and forgotten, instead of treated as the highest-signal input to the evaluation system — missing the opportunity to convert failure cost into future quality.

**inputs:**
- Production incident signal (CSAT drop, anomaly alert, PII breach flag)
- Centralized trace collection spanning all agent frameworks
- LLM judge reports from recent evaluation runs
- Living eval dataset as the target for new test cases
- ITSM integration for incident tracking

**outputs:**
- Step 1 (Detect): incident identified via eval dashboard (primary detection surface, not logs/APM)
- Step 2 (Diagnose): root cause isolated from traces (stale embeddings, prompt drift, tool loop, PII leak)
- Step 3 (Contain): immediate mitigation via prompt rollback, human deflection routing, or circuit breaker activation
- Step 4 (Fix): root cause corrected — e.g., vector DB updated with new policy document, prompt bug fixed
- Step 5 (Add to Dataset): new test case covering the exact failure scenario added to the living eval dataset

**benefits:**
- Closes the learning loop: every incident is an investment in future quality, not just a cost
- Eval dashboard as primary detection surface means quality regressions are caught before CSAT surveys, not after
- Trace-based diagnosis enables precise root cause identification — no more "the agent is broken" with no explanation
- ITSM integration fits into existing enterprise incident management workflows

**limitations:**
- Step 5 (Add to Dataset) requires the failed query and its expected correct output — if the incident was a generic degradation (not a specific query), creating a precise test case is harder
- Containment actions (prompt rollback, circuit breaker) require versioned prompts and a routing layer — not present in ad-hoc agent deployments
- The flywheel assumes tracing coverage exists for the incident — if the failure occurred in an uninstrumented code path, diagnosis is blind
- Eval dashboard as primary detection surface requires eval alerts to be configured and monitored with the same rigor as production SLO alerts

---

## 5. Behavioral Eval Path Analysis (Layer 3)

**problem_solved:** An agent can return the correct answer ("your balance is R$ 1.234,56") while executing a wasteful path (3 redundant database calls, 2 unnecessary external API calls) — invisible to semantic evaluation but financially unsustainable at 20,000 calls/month.

**inputs:**
- Full execution trace from each agent query (ordered tool calls with timestamps and parameters)
- Expected execution path template (the correct sequence and count of tool calls for the query type)
- Cost model per tool call (DB query cost, external API cost, LLM call cost)
- Query categorization (simple lookup vs. multi-step reasoning vs. transactional)

**outputs:**
- Redundancy score: count of unnecessary repeated calls to the same tool with equivalent parameters
- Loop detection flag: tool call sequences that form semantic cycles (call A → call B → call A with same intent)
- Path efficiency score: ratio of necessary calls to total calls for the query category
- Duplicate API detection: multiple calls to different external APIs retrieving overlapping or equivalent data
- Per-query cost attribution in dollars: sum of all tool call costs for each query

**benefits:**
- Reveals the "wrong path, right answer" failure mode that demo evaluations never expose
- Quantifies the per-query cost profile, enabling cost prediction at scale (20,000 queries/month)
- Path efficiency scores provide a leading indicator of production cost before CSAT drops
- Loop detection catches infinite or near-infinite tool call cycles before they consume budgets or crash the system

**limitations:**
- Requires full trace instrumentation of every tool call — adding tracing to existing agents retroactively is high effort
- Defining the "correct" path template per query category requires expert knowledge of the agent's design intent
- Cost model accuracy depends on real pricing data from DB/API providers; stale cost models mislead decisions
- Path analysis is expensive to run on every query; requires sampling or cost-tiered execution (subset in CI, full on merge)

---

## 6. Centralized Cross-Framework Tracing

**problem_solved:** Enterprises deploy multiple agent frameworks (CrewAI, LangChain, custom) across multiple clouds, creating fragmented observability where each framework has its own tracing, no unified view exists, and debugging requires context-switching between disconnected tools.

**inputs:**
- Execution traces from all agent frameworks (collected via framework-specific adapters or OpenTelemetry)
- Agent identity metadata (framework type, agent version, model version, deployment region)
- Query context (user input, session ID, timestamp)
- Tool call records (tool name, parameters, duration, success/failure)

**outputs:**
- Centralized trace layer with unified schema across all frameworks
- Dashboards: single-pane view of all agent activity regardless of framework
- Text-to-SQL interface: ad-hoc queries over trace data ("show me all queries that took >5 tool calls last week")
- LLM judge reports: automated quality evaluation consuming the unified trace stream
- Auditor reports: compliance evidence that every query is traceable end-to-end
- Online monitoring: real-time anomaly detection over the unified trace stream

**benefits:**
- Single debugging surface: trace any query from any agent in any framework from one tool
- Regulatory compliance: "you cannot even onboard AI into production without tracing" — centralized trace layer satisfies audit requirements
- Framework-independent evaluation: LLM judges and dashboards consume the same trace format regardless of which framework produced it
- Enables cross-framework comparisons: measure relative performance of CrewAI vs. LangChain vs. custom agents on identical queries

**limitations:**
- Requires per-framework adapter development; each framework's trace format is different
- Trace volume at enterprise scale (thousands of agents, millions of queries) demands significant storage and processing infrastructure
- Schema evolution management: if a framework adds new trace fields, the centralized layer must accommodate without breaking consumers
- Adds latency: trace collection and forwarding is an additional network hop per tool call; trace sampling may be required at extreme scale

---

## 7. Prompt-as-Code with Causal Change Management

**problem_solved:** Prompts are the most frequently changed and least version-controlled component of agentic systems — generic commit messages ("updated prompt", "improved response") make rollback and debugging impossible because no one knows why a prompt changed or what failure it was addressing.

**inputs:**
- Prompt version history in a version-controlled repository (git)
- Production incident records that triggered prompt changes
- CSAT metrics or eval scores that degraded before the change
- Diagnostic evidence from trace analysis identifying which prompt component failed

**outputs:**
- Versioned prompt with commit message answering three mandatory questions: (1) why it changed (causal trigger), (2) what failure caused the change (diagnostic context), (3) what failure this change addresses (predictive intent)
- Prompt rollback capability: any previous prompt version can be restored with full context of why it was replaced
- Audit trail linking every prompt change to a specific incident, eval regression, or feature requirement
- Change impact prediction: when a prompt changes, the eval dataset runs to quantify the effect on quality before deploy

**benefits:**
- Debuggable prompt history: you know not just what changed but why, triggered by what, and targeting what failure mode
- Safe rollbacks: if a prompt change degrades quality, rollback to the previous version with full context — not guesswork
- Compliance: regulated industries can demonstrate that every prompt change was justified by evidence, not experimentation
- Change impact quantification: running the eval dataset before deploy catches prompt regressions before production exposure

**limitations:**
- Requires discipline from every engineer touching prompts — cultural adoption of commit message standards is hard
- The three-question format works for reactive changes (incident-driven) but is less natural for proactive improvements (refinement)
- Prompt version history grows unboundedly; outdated prompts should be archived but traceable, adding maintenance overhead
- Does not capture implicit prompt changes from model provider updates — the same prompt text may produce different behavior after a model update

---

## 8. Eval Dashboard as Primary Detection Surface

**problem_solved:** Traditional production monitoring (logs, APM, infrastructure dashboards) surfaces latency, error rates, and resource consumption — but does not surface agent quality regressions (increasing hallucination rate, response degradation, drift in answer accuracy), which only become visible days later through CSAT surveys.

**inputs:**
- Streaming eval results from all three layers (deterministic, semantic, behavioral) across all agents and queries
- CSAT scores as a lagging validation signal
- Historical quality baselines (expected pass rates per layer, per category, per agent)
- Anomaly detection thresholds calibrated per evaluation layer

**outputs:**
- Real-time quality dashboard: pass/fail rates per eval layer, per category, per agent — updated continuously
- Anomaly alerts: when pass rates drop below baseline thresholds for any category
- Trend visualization: quality trajectory over time, enabling detection of slow degradation before it becomes catastrophic
- Drill-down capability: from aggregate quality score → specific failing eval category → individual failing queries → full trace

**benefits:**
- Quality regressions are detected in minutes (via eval), not in weeks (via CSAT surveys)
- The eval dashboard is the first place the team looks during an incident — not logs, not APM
- Trend visibility catches slow degradation (e.g., embeddings gradually going stale) that binary alerts miss
- Drill-down from dashboard to individual trace enables rapid diagnosis without context-switching tools

**limitations:**
- Eval dashboard is only as good as the eval dataset feeding it — gaps in test coverage are gaps in visibility
- High false-positive rate from Layer 2 (LLM-as-Judge) can create alert fatigue if thresholds are not calibrated
- Requires eval infrastructure to be always-on, not batch; streaming eval results in real time adds infrastructure cost
- Dashboard is a detection surface, not a diagnosis surface — it tells you quality dropped, but you still need traces to find why

---

## 9. Multi-Agent Fault Tolerance (Saga + Circuit Breaker + Human Escalation)

**problem_solved:** Multi-agent workflows fail partially — one agent succeeds, another times out, a third returns stale data. Without fault tolerance, partial failures either go undetected (producing incorrect final results) or crash the entire workflow (losing the progress of successful agents).

**inputs:**
- Multi-agent workflow definition with ordered steps and dependencies
- Per-step compensating action (the reverse operation that undoes the step's effect)
- Failure threshold configuration per agent (error rate, latency percentile)
- Human escalation policy (which failure classes require human judgment vs. automated fallback)
- Orchestrator state tracking which steps have completed, which are in-progress, which have failed

**outputs:**
- Saga rollback: if step N fails, compensating actions for steps 1..N-1 are executed in reverse order, returning the system to its pre-workflow state
- Circuit breaker activation: if an agent's failure rate exceeds threshold, the circuit opens, subsequent calls are redirected to a fallback (default response or human queue)
- Human escalation: when confidence is below threshold or the circuit is open, the query is routed to a human operator with full context (what the agent attempted, why it failed, what it needs)
- Partial completion log: if the workflow cannot complete, record which steps succeeded and what compensating actions were applied

**benefits:**
- Prevents cascading failures: a slow external API does not degrade the entire multi-agent system
- Maintains consistency: Saga pattern ensures distributed transactions across agents are atomic — all succeed or all are compensated
- Graceful degradation: circuit breaker routes failing agents to fallback responses instead of returning errors to users
- Audit trail: every failure, rollback, and escalation is logged, enabling post-incident analysis and eval dataset enrichment

**limitations:**
- Compensating actions must be designed and tested for every step — not every operation has a clean undo (e.g., sending an email)
- Saga adds latency: each step must await confirmation before the next begins, and rollback multiplies the number of operations
- Circuit breaker thresholds require tuning; too sensitive (false opens) degrades user experience, too lenient (late opens) allows cascading failures
- Human escalation introduces variable latency and requires operational staffing to handle escalation queues

---

## 10. Agent-Specific Data Freshness Pipeline

**problem_solved:** Data pipelines built for human consumption (dashboards, reports) tolerate staleness, ambiguity, and inconsistency because humans infer context and apply judgment. Agents treat every data point literally — stale embeddings, outdated policy documents, and contradictory records produce confident wrong answers that directly damage user trust.

**inputs:**
- Source documents (policy documents, product catalogs, FAQs, knowledge bases) from organizational systems
- Update timestamps and change logs for each source document
- Vector database or knowledge base consuming embeddings derived from source documents
- Agent query patterns and their data dependencies (which documents does each query type reference?)

**outputs:**
- Freshness guarantee: every source document change triggers automatic re-ingestion and re-embedding within a defined SLA
- Consistency checks: contradictory records across documents are flagged before ingestion (e.g., two policy docs with conflicting interest rates)
- Staleness monitoring: the tracing layer detects when agent responses reference outdated document versions and triggers CSAT alerts
- Update triggers: event-driven pipeline that reacts to source document changes (not periodic batch — documents can change between batches)

**benefits:**
- Prevents the "stale RAG" failure mode: bank changed interest rates, sent customer emails, but the agent kept quoting old rates because the vector DB wasn't updated
- Data quality becomes a first-class engineering concern, not an afterthought — 60% of project time allocated to data foundation
- Event-driven freshness eliminates the gap between "document changed" and "agent knows about the change"
- Consistency checks prevent contradictory information from entering the agent's knowledge base

**limitations:**
- Requires integration with every source document system to detect changes — organizational data is often scattered across legacy systems without webhooks or change events
- Embedding regeneration latency is non-trivial; large knowledge bases may take minutes to re-embed after a change, creating a freshness gap
- Consistency checks require semantic comparison between documents, which itself may use LLM calls — adding cost
- The 60% time investment in data foundation must be justified against the business value of the agent; for low-stakes use cases, it may be overinvestment

---

## 11. Governance Context Injection for PII Prevention

**problem_solved:** Agents access enterprise data catalogs containing PII (SSN, phone, address) but the model has no awareness of which fields are sensitive — it treats all data as safe to include in responses, causing PII breaches that would be compliance incidents in production.

**inputs:**
- Data catalog with PII tagging per field (Unity Catalog or equivalent)
- Agent prompt template with injection points for governance context
- Deterministic PII detection patterns (regex for SSN, phone, email, credit card)
- Query context (which tables/fields the agent accessed during this query)

**outputs:**
- Before-generation injection: governance context (list of PII-tagged fields accessed by this query) is injected into the prompt before the model generates its response
- Model awareness: the prompt tells the model which fields it accessed contain PII and must not be exposed in the response
- Post-generation verification: Layer 1 deterministic eval scans the output for PII patterns as a safety net
- Audit record: every query's governance context and PII scan result is logged for compliance auditors

**benefits:**
- Prevents PII breaches before generation — the model knows which fields are sensitive and can compose responses that reference them safely (e.g., "your account ending in XXXX")
- 47 PII breaches caught in testing phase; without this pattern, each would have been a compliance incident in production
- Governance context travels with the data: PII tags in the catalog propagate through queries into prompts — no manual annotation of prompts per use case
- Deterministic PII scan (Layer 1) provides a safety net even if the model ignores governance context

**limitations:**
- Requires a data catalog with PII tagging — organizations without mature data governance must build this first
- PII tagging coverage gaps: a field that is not tagged as PII in the catalog will not be injected into the prompt
- Model may still expose PII despite governance context — the injection is a prompt instruction, not a hard constraint
- Post-generation PII scan catches breaches but does not prevent them; the response has already been generated

---

## 12. Business-Outcome-First Eval Pipeline

**problem_solved:** Engineering teams build evaluation pipelines starting with technical metrics (latency, throughput, accuracy) instead of business outcomes (deflection rate, CSAT, revenue impact), creating misalignment where the technical eval passes but the business outcome fails.

**inputs:**
- Business success definition (e.g., "60% of customer queries deflected without human intervention")
- Manual golden answers created by domain experts (not by models) for the initial ~200 queries
- Real production queries from human agent logs (not synthetic queries)
- Business metrics that the agent is intended to improve (deflection rate, resolution time, customer satisfaction)

**outputs:**
- Business-aligned eval rubric: each test case is scored against the golden answer by a metric that correlates with the business outcome
- Python evaluation pipeline that compares agent responses against golden answers — built after, not before, the golden dataset exists
- Deflection rate prediction: eval pass rate predicts production deflection rate, enabling go/no-go decisions before deployment
- Iteration loop: eval metrics drive improvements until the business outcome threshold is met

**benefits:**
- Prevents the "technically correct, business irrelevant" trap: the eval measures what matters to the business, not what is easy to measure
- Golden answers authored by domain experts, not models, ensure the eval represents real customer expectations
- Starting with business outcomes and manual golden answers is faster than starting with engineering — "define success → create golden answers → build pipeline"
- Deflection rate prediction from eval scores enables evidence-based deployment decisions

**limitations:**
- Requires access to real production queries and domain experts to author golden answers — not feasible for pre-product agents
- Manual golden answer authoring does not scale; beyond ~200 cases, automation (LLM-assisted) is required, introducing quality risk
- Business metric correlation with eval scores must be validated empirically; initial correlation may not hold as the domain evolves
- The pipeline requires maintenance as business outcomes change; a deflection-rate-optimized eval may not measure quality for a new business goal

---

## 13. Model-Switching Architecture with Enterprise Eval Gate

**problem_solved:** Committing to a single model provider creates vendor lock-in — when the provider updates their model, performance may degrade silently because the organization has no way to test the new model against their specific domain before customers are affected.

**inputs:**
- Enterprise eval dataset (domain-specific, not public benchmarks)
- Current model performance baseline (pass rates on all three eval layers)
- Candidate model (new model version, new provider, or fine-tuned variant)
- Model-switching infrastructure: architecture that accepts any model implementing a standard interface

**outputs:**
- Side-by-side comparison: candidate model run against the enterprise eval dataset, results compared to current model baseline
- Switching decision: data-driven recommendation (switch, hold, or hybrid — use new model for certain query categories, old for others)
- Regression report: specific test cases where the candidate model performs worse than current, enabling targeted investigation
- Deployment plan: if switching, the eval dataset serves as the canary — deploy to a subset of traffic, compare eval scores, expand or rollback

**benefits:**
- Vendor independence: model selection is governed by domain-specific performance data, not by provider relationships
- Provider updates become testable: when a model provider releases a new version, run the eval dataset to decide if the update is safe
- No single point of model failure: if one model degrades, switch to another that has already been tested against the eval dataset
- The eval dataset that selected the model also serves as the continuous validation suite for every subsequent model change

**limitations:**
- Multi-model architecture adds complexity: prompting strategies, tool call formats, and output parsing may differ between models
- Running the full eval suite against multiple models adds cost (LLM calls for Layer 2-3 multiplied by number of candidates)
- Model behavior can change without provider announcement — continuous eval monitoring is required, not just point-in-time comparison
- The eval dataset itself may have model-specific biases if golden answers were authored with one model's typical output style in mind
