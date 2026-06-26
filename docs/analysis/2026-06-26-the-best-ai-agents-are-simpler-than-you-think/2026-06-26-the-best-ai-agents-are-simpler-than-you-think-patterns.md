---
title: "Patterns: The best AI agents are simpler than you think"
type: analysis
tags: ["agentes-orquestracao", "harness-engineering", "context-engineering", "evals", "model-selection", "memory-architecture", "agent-tooling"]
date: "2026-06-26"
aliases: ["sierra-patterns", "wedeen-patterns", "agentes-simples-patterns"]
last_updated: 2026-06-26
relates-to: ["[[docs/analysis/2026-06-26-the-best-ai-agents-are-simpler-than-you-think/2026-06-26-the-best-ai-agents-are-simpler-than-you-think-analysis|Knowledge Extraction]]", "[[docs/system-of-record|System of Record]]"]
---

# Patterns: The best AI agents are simpler than you think

**Source**: LangChain Max Agency — Zack Reno Wedeen (Sierra)
**Date**: 2026-06-26
**Total Patterns**: 18

## Model Selection & Routing

### Pattern: Task-Routed Model Tiering

**Problem Solved**: Using a single frontier model for every subtask within an agent turn wastes cost and latency on tasks that don't need frontier-level reasoning.

**Inputs**:
- Conversation turn with multiple subtasks (classification, retrieval, reasoning, response generation)
- Per-task latency budgets and quality requirements
- Model capability profiles across frontier, in-house, and lightweight classifiers

**Outputs**:
- Task-to-model routing decisions per turn
- Parallel dispatch of subtasks to different model tiers
- Aggregated response from independently computed subtasks

**Benefits**:
- Reduces per-turn cost by routing simple classification/retrieval to lightweight models
- Decreases end-to-end latency through parallel execution across model tiers
- Maintains quality on reasoning-critical subtasks via frontier model dispatch
- Decouples model selection from orchestration logic — switch models without rewriting agent code
- Enables roughly one-third frontier, one-third in-house, one-third third-party composition

**Limitations**:
- Adds routing complexity — incorrect task classification sends simple tasks to expensive models or complex tasks to weak models
- Requires per-task eligible model sets that must be maintained as model capabilities evolve
- Parallel dispatch coordination introduces failure modes if one model times out
- Not beneficial when all subtasks genuinely require frontier reasoning

### Pattern: Multi-Provider Model Routing with Capacity Resilience

**Problem Solved**: Single-provider model dependencies create catastrophic failure risk during traffic spikes (Black Friday, Cyber Monday) or provider outages.

**Inputs**:
- Per-task eligible model sets across multiple providers
- Provisioned capacity and historical load patterns per provider
- Enterprise constraints (cloud regions, approved vendor lists)
- Evals that validate model-agnostic correctness across providers

**Outputs**:
- Provider-agnostic task routing (model switching at task granularity)
- Load simulation results (billions of conversations/year)
- Provider fallback decisions during capacity degradation

**Benefits**:
- Capacity resilience for extreme traffic spikes — multi-provider redundancy at the task level
- Enterprise compliance: supports per-customer cloud region and vendor constraints
- Model-agnostic harness — evals work across providers, making switching "pretty simple"
- Avoids single-provider lock-in for business continuity

**Limitations**:
- Eval coverage must be comprehensive enough to catch provider-specific regressions
- Adds operational overhead: model-specific prompt tuning, rate limit management, quota tracking
- Benefits diminish if all providers share common infrastructure (single cloud backend)
- Not justified for low-traffic systems without capacity risk

### Pattern: Structured Data + LLM Hybrid Reasoning

**Problem Solved**: LLMs excel at conversational empathy but lack deep knowledge of individual customer preferences, purchase history, and structured recommendation logic — producing charming but context-poor interactions.

**Inputs**:
- Structured customer data (preferences, purchase history, loyalty status)
- Recommendation engine outputs (cross-sell, upsell, retention offers)
- LLM conversational context (current turn, sentiment, conversation goals)

**Outputs**:
- Hybrid interaction blending structured "what to recommend" with LLM "how to present it naturally"
- Context-aware offer selection (choosing between competing recommendations)
- Empathetic framing of recommendation logic

**Benefits**:
- Combines deterministic recommendation quality with LLM conversational fluency
- Particularly effective in sales, loyalty, and retention conversations
- Previous-gen recommender systems hold data LLMs cannot replicate — leverage both
- Counter-intuitive: the most natural-seeming conversations require both data systems

**Limitations**:
- Requires integration with customer data platforms and recommender systems
- Structured data freshness affects recommendation relevance — stale data undermines LLM framing
- Added latency from structured data fetch before LLM turn
- Not applicable when structured data is unavailable or unreliable

## Harness Architecture

### Pattern: Dual-Loop Harness Architecture

**Problem Solved**: A single execution loop optimized for low-latency interaction cannot handle deep analysis tasks requiring extended processing (minutes or hours).

**Inputs**:
- Conversational turn classification (fast response vs. deep analysis)
- Latency budgets per task type (sub-2-second for conversation, minutes+ for analysis)
- Background task description and callback context

**Outputs**:
- Fast conversational loop handling real-time interaction
- Background loop spawning for extended processing with callback notification ("let me figure this out in 20 minutes")
- Convergent harness architecture — background loop converges toward tool-platform mastery

**Benefits**:
- Users experience sub-2-second responses for simple interactions while complex tasks run asynchronously
- Background loop can use more expensive reasoning models with higher latency tolerance
- Convergent architecture: coding agent harness and deep analysis harness share tool-platform patterns
- Elegant cost-latency trade-off per task type

**Limitations**:
- Callback UX complexity — user trust requires reliable follow-through on background tasks
- State synchronization between loops adds architectural complexity
- Background task failures need explicit error recovery and re-engagement flows
- Not beneficial when all agent tasks are uniformly fast or uniformly slow

### Pattern: Cognitive Process Parallelization

**Problem Solved**: Voice and conversational agents waste latency by pipelining cognitive processes (listen → think → speak) when human cognition parallelizes them.

**Inputs**:
- Audio input stream (real-time)
- Intent classification and response generation models
- Tool call and data retrieval infrastructure

**Outputs**:
- Concurrent listening, thinking, and speaking
- Interrupt-aware response generation (agent yields when user speaks)
- Progress indicators generated while background work completes

**Benefits**:
- Dramatically reduces perceived latency in voice interaction
- Mirrors human conversation patterns — ~50% of brain power in timing, not content
- Prevents the flawed architecture of "50 lines of Python deciding when to speak and a trillion parameters deciding what to say"
- Enables natural turn-taking with interruption handling

**Limitations**:
- Adds implementation complexity — coordinating parallel cognitive streams
- Requires speculative work that may be discarded when user interrupts
- Voice-specific benefits — less relevant for text-only chat agents
- Model coordination overhead can introduce bugs in transition logic

### Pattern: Speculative Execution for Latency Reduction

**Problem Solved**: Sequential processing (fetch data → decide it's needed → use it) adds avoidable latency when some preparation work can run before decisions are finalized.

**Inputs**:
- Incoming user query
- Knowledge bases, account data, and tool APIs
- Intent classifier (running in parallel, not as a gate)

**Outputs**:
- Pre-fetched data that may or may not be used
- Interim response generation ("Hold on, I'm pulling up your account")
- Reduced perceived latency through overlapping computation and wait time

**Benefits**:
- Knowledge retrieval runs in parallel with and often ahead of the decision about whether the answer is needed
- Progress indicators bridge the gap between user expectation and actual processing time
- Trading compute cost (discarded speculative work) for latency — acceptable trade-off in voice contexts

**Limitations**:
- Wastes compute on speculative work that gets discarded when decisions change
- Increases total compute cost per turn — acceptable for voice latency but wasteful for async chat
- Requires accurate interim response generation to avoid user confusion
- Less beneficial when most tasks complete within latency budget without speculation

## Context Engineering

### Pattern: Monolith-First Agent Architecture

**Problem Solved**: Prematurely splitting agents into triage + task sub-agents deprives each of the other's context, degrading overall quality compared to a single agent with disciplined context engineering.

**Inputs**:
- Full task context (user intent, procedural knowledge, system constraints)
- Context engineering strategies: relevance filtering, temporal timing, progressive disclosure
- Organizational boundaries (team ownership, if applicable)

**Outputs**:
- Single-agent conversation handling with selective context injection
- Rejection of multi-agent decomposition unless organizational separation is the sole motivation
- Better context retention than split-agent architectures

**Benefits**:
- Avoids the anti-pattern where triage agent loses procedural context and task agent loses triage context
- Simpler architecture with fewer failure modes (fewer agent handoffs)
- Converges with framing that sub-agents are for context control, not anthropomorphized roles
- Truly separable jobs (where context from the first has no purpose in the second) remain the only exception

**Limitations**:
- Requires sophisticated context engineering (progressive disclosure, temporal timing) to avoid context overload
- Single agent may hit context limits on very long multi-turn interactions without compaction
- Does not apply when organizational boundaries genuinely require separate agent ownership
- May not scale to extremely diverse task domains in a single agent

### Pattern: Temporal Context Injection

**Problem Solved**: Injecting all relevant context at turn start overloads the prompt, while removing previously-present context during compaction creates incoherence — timing matters as much as content selection.

**Inputs**:
- Conversation history with turn-level state
- Domain knowledge to inject (articles, SOPs, customer data)
- Current task phase and expected upcoming phases
- Prompt compaction events and their timing

**Outputs**:
- Context injected only when relevant to the current conversation phase
- Guarded compaction that avoids yanking context that contradicts updated system prompts
- Coherent prompt state across multi-turn interactions

**Benefits**:
- Shows agents "everything they need to do the right thing, but nothing more" at each moment
- Reduces prompt bloat and token waste on irrelevant context
- Preserves coherence across prompt compaction events
- Enables a single agent to handle complex multi-turn interactions without sub-agent decomposition

**Limitations**:
- Requires accurate prediction of when context will become relevant
- Context removal timing must avoid leaving contradictory signals between earlier and current claims
- Adds implementation complexity: context injection must be phase-aware
- Over-aggressive compaction can degrade understanding of earlier conversation turns

## Eval & Quality Infrastructure

### Pattern: Closed-Loop Agent Improvement Flywheel

**Problem Solved**: Agent improvement cycles that stop at deployment miss the opportunity to learn from production interactions and feed insights back into the build phase.

**Inputs**:
- Production conversation data from all customer interactions
- Explorer agent (long-running deep research over conversations)
- Reports and always-on monitors evaluating production quality
- Ghostwriter agent (agent that builds agents)
- Declarative agent specifications (Journeys/DSL)

**Outputs**:
- Analyze phase: insights from explorer, reports, and monitors
- Build phase: agent improvements generated by Ghostwriter
- Release phase: governance-gated deployment of improvements
- Daily closed-loop flow: Analyze → Build → Release

**Benefits**:
- Proactive improvement: Ghostwriter suggests optimizations based on explorer insights
- Continuous quality uplift from production data, not just pre-release testing
- Structured three-phase workflow aligns with governance requirements
- Each phase produces distinct, inspectable artifacts

**Limitations**:
- Requires production volume to generate statistically meaningful insights
- Ghostwriter-generated improvements need human review for correctness
- Release governance adds friction — must be balanced against improvement velocity
- Infrastructure complexity: three phases with distinct computational profiles

### Pattern: Always-On Production Monitoring with Human Triage

**Problem Solved**: Exhaustive human review of every agent conversation is impossible at scale; random sampling misses rare but critical failure modes.

**Inputs**:
- Every production conversation (real-time stream)
- Monitor definitions: evaluator specifications for quality dimensions
- Human review capacity (limited, expensive)

**Outputs**:
- Flagged subset of conversations requiring human attention
- Compression ratio: 10,000 conversations → ~5 human reviews
- Continuous quality signal without exhaustive manual effort

**Benefits**:
- Shifts human attention from defensive (review everything) to offensive (improve resolution rate and satisfaction)
- Catches rare failure modes that random sampling would miss
- Treats evaluation as ongoing operational concern, not just a pre-release gate
- Monitors are separate infrastructure from eval pipelines — both coexist

**Limitations**:
- Monitor quality determines triage accuracy — poorly designed monitors miss failures or flood humans
- Requires investment in monitor development and maintenance
- Human reviewers may develop alert fatigue if false positive rate is high
- Does not replace pre-release evals — production monitoring is complementary, not substitutive

### Pattern: Model-Switch-Driven Eval Hardening

**Problem Solved**: Eval suites designed against a single model provider develop blind spots — they test what the current model gets right but not what a different model might get wrong.

**Inputs**:
- Current eval suite (task-specific correctness tests)
- Task routing definition with eligible model sets
- Results from switching a task to a different model provider

**Outputs**:
- Gaps exposed in the eval suite (regressions the old eval missed)
- Hardened eval suite covering provider-specific failure modes
- Model-agnostic confidence: ability to switch providers with eval-based safety net

**Benefits**:
- Turns model switching from a migration risk into an eval hardening mechanism
- First switch "invariably reveals the eval wasn't as good as you thought"
- Continuous strengthening: each switch improves evals, making future switches safer
- Makes the harness genuinely model-agnostic — evals, not model affinity, are the stable interface

**Limitations**:
- Initial switches will surface more gaps than expected — requires investment to close them
- Eval hardening is iterative: each new provider exposes new gaps
- Not beneficial if you never intend to switch models
- Requires eval infrastructure that works across providers (same inputs/outputs semantics)

### Pattern: Recursive AI Verification Chains

**Problem Solved**: Non-deterministic AI components cannot be made 99.9% reliable through single-pass verification; compounding failure rates require layered checking.

**Inputs**:
- Primary AI output (e.g., generated conversation, classification decision)
- Verification AI models (second-pass checkers)
- Meta-verification AI models (validating the verifiers)

**Outputs**:
- Three-layer verification chain: primary output → AI verification → AI meta-verification
- Each layer filters additional errors, asymptotically approaching production-grade reliability
- Composability: each verification layer follows the same architectural pattern

**Benefits**:
- Achieves multi-nine reliability with non-deterministic systems through composable verification
- 90% accurate primary + 90% accurate verifier + 90% accurate meta-verifier = high aggregate reliability
- Architectural principle behind Sierra's monitors: AI-generated → AI-checked → meta-monitored
- Trades compute cost for reliability in a layerable, predictable way

**Limitations**:
- Compute cost multiplies with each verification layer
- Correlated errors: if all AI components share the same blind spot, layering doesn't help
- Diminishing returns after 2-3 layers — each additional layer filters fewer errors
- Requires diverse verification models to avoid correlated failure modes

### Pattern: Confidence-Gated Continual Learning

**Problem Solved**: Full automation of agent improvement risks deploying incorrect fixes; full manual review bottlenecks deployment velocity.

**Inputs**:
- Issues detected from production agent interactions
- Automated improvement suggestions (Ghostwriter)
- Confidence score per suggestion (based on fix verifiability)
- Customer comfort threshold for automation

**Outputs**:
- High-confidence, trivially verifiable fixes → FYI notification + auto-deployment
- Lower-confidence fixes → human review required before deployment
- Four-stage loop: detect → suggest → review → deploy

**Benefits**:
- Accelerates deployment for unambiguous fixes (e.g., contradictory knowledge articles with clear correct answer)
- Preserves human oversight for ambiguous or high-stakes changes
- Gradual: primitives are built; constraint is customer comfort, not technical capability
- "We don't want to pull the future forward too quickly"

**Limitations**:
- Confidence scoring accuracy determines safety — overconfident scoring risks deploying incorrect fixes
- Customer comfort threshold varies by domain — healthcare tolerates less automation than e-commerce
- Requires clear verifiability criteria per fix type
- May under-automate if confidence thresholds are set conservatively

## Memory & Security Architecture

### Pattern: Three-Tier Memory Persistence

**Problem Solved**: Memory is either fully manual (user must say "remember this") or fully implicit (agent guesses what matters), with no gradient between these extremes.

**Inputs**:
- Conversation turns with explicit save instructions
- Builder-defined memory schemas (declared upfront by agent designers)
- Implicit memory signals (agent-observed relevance patterns)

**Outputs**:
- Tier 1 (explicit per-turn): user says "save this to memory"
- Tier 2 (builder-defined): agent builders declare what matters upfront (e.g., "remember birthdays")
- Tier 3 (implicit/agent-decided): agent autonomously determines what to remember
- Increasing automation across tiers with corresponding increase in memory quality risk

**Benefits**:
- Measurably improved resolution rate through greeting by name, recalling previous call topics, recognizing frustrating past interactions
- Incremental adoption path: start with Tier 1 → add Tier 2 declarations → enable Tier 3 as confidence grows
- Treats memory as first-class platform primitive, not an afterthought

**Limitations**:
- Implicit memory (Tier 3) can capture incorrect or sensitive information without user awareness
- Memory quality degrades as automation increases — Tier 3 requires more verification than Tier 1
- Platform-level memory requires integration with identity resolution
- Memory bloat: without pruning, accumulated memories degrade retrieval relevance

### Pattern: Regulated Data Boundary

**Problem Solved**: LLM providers are not certified for regulated data (PCI, HIPAA, auth tokens), yet agents increasingly handle payments and sensitive information — routing all data through the LLM creates compliance and security risk.

**Inputs**:
- Regulated data streams (payment information, authentication tokens, PII)
- LLM context window (untrusted for regulated data)
- Parallel non-AI infrastructure for regulated operations

**Outputs**:
- Isolated infrastructure tier handling regulated data entirely outside LLM context
- Security boundary enforcement: sensitive data never enters a model prompt
- Compliance certification per boundary (PCI DSS Level 1 for payment tier)

**Benefits**:
- Enables agent-mediated commerce where no LLM provider is PCI-certified
- Same pattern applies to authentication-gated memory — data that must never enter an LLM context window gets isolated infrastructure, not just policy controls
- Built "before it made sense" as strategic bet on agent-mediated commerce exceeding e-commerce volume
- Policy controls alone are insufficient — architectural isolation is the enforcement mechanism

**Limitations**:
- Adds infrastructure complexity: separate payment/regulated data tier with independent certification
- Some agent interactions genuinely require regulated data in context — architectural isolation may limit functionality
- Certification processes (PCI, HIPAA) are long and expensive — upfront investment before demand materializes
- Not needed for agents that never touch regulated data

### Pattern: Auth-Coupled Memory Architecture

**Problem Solved**: Memory products treat storage and retrieval as independent of identity, but extracting the right memories requires knowing who the caller is — authentication and memory are coupled architectural concerns.

**Inputs**:
- Identity resolution signal (phone number, account ID, session token)
- Authentication confidence score
- Memory store keyed by identity

**Outputs**:
- Authenticated memory retrieval (only memoreies belonging to the identified caller)
- Tiered access per memory sensitivity level (low-sensitivity vs. high-sensitivity)
- Rejection of standalone memory products that lack identity coupling

**Benefits**:
- Explains why memory startups haven't broken out: "If I want to buy memory from you, I also need to buy authentication from you"
- Consumer products (ChatGPT, Claude) can offer memory freely because users already trust them with identity
- B2B vendors face higher bar: must couple memory with identity verification
- Memory sensitivity gating: "thanks for calling again, Harrison" requires less auth confidence than SSN-related memory

**Limitations**:
- Authentication is imperfect — phone numbers can be shared (office networks, family lines)
- Requires explicit sensitivity policy gradient per business domain
- Coupling increases integration cost: adopting memory means adopting identity infrastructure
- Not applicable to anonymous agents that don't persist per-user state

## Agent Tooling Design

### Pattern: File-System Materialization for Agent Tooling

**Problem Solved**: Coding agents struggle with custom abstractions and DSLs because they don't map to the primitives models were trained to manipulate (files, diffs, git, grep).

**Inputs**:
- Domain logic and agent specifications
- Coding agent capabilities (file system manipulation, git operations, text search)
- Model training corpus familiarity (common packages, file formats)

**Outputs**:
- Domain concepts materialized as file-system artifacts (files, directories, structured text)
- Tool interfaces that coding agents already understand without custom training
- Agent-manipulable representations of declarative specifications

**Benefits**:
- "Coding agents are really good at file systems, they're really good at Git, they're really good at grep. Let's materialize everything into those structures so that coding agents can just cook."
- Applies to Ghostwriter building agents by manipulating declarative DSL representations as if they were file systems
- Reduces the gap between what models know and what tasks demand
- No custom training or skill injection needed for tool usage

**Limitations**:
- Some domain concepts resist materialization into file-system primitives
- Over-materialization creates file bloat and maintenance overhead
- File-system representation may not capture semantic relationships that a database or graph would
- Requires the coding agent to be competent at file operations (generally true for frontier models)

### Pattern: Model-First Interface Design (80/20 Rule)

**Problem Solved**: Tooling interfaces designed for human engineers or pure correctness create a mismatch with coding agent capabilities — the model must learn your abstraction before it can be productive.

**Inputs**:
- Task requirements and domain logic
- Coding agent capability profile (what models are genuinely good at)
- Available primitives (file systems, git, grep, common packages)

**Outputs**:
- 80% of interfaces reframed into model-familiar primitives
- 20% of interfaces where domain abstractions are genuinely necessary — taught via skills and context injection

**Benefits**:
- Reduces the "middle ground" anti-pattern: abstractions that are almost what models are good at but not quite, causing overconfidence errors
- Default posture: meet the models on their turf; building custom model capabilities is the exception
- Reduces skill injection overhead — only the genuinely novel 20% needs custom teaching
- Aligns with the insight that halfway abstractions are worse than either extreme

**Limitations**:
- Some domain concepts genuinely cannot be reframed into model-familiar primitives — the 20% exists for a reason
- Determining which 20% justifies custom abstraction requires judgment — over-relying on model-familiar primitives may sacrifice domain correctness
- Model capabilities evolve — today's model-familiar primitives may change with new model generations
- Does not address the case where no good mapping to model-familiar primitives exists
