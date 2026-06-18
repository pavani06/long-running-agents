---
title: "Prompt: Análise Comparativa Completa — Arquitetura de Agentes de E-commerce"
type: prompt
date: 2026-06-05
tags:
  - agentes-orquestracao
  - curriculo-conteudo
aliases:
  - analise comparativa koda
  - ecommerce agent architecture
  - comparacao mhc curriculo
relates-to:
  - "[[prompts/PROMPTS-00-INDEX|Prompt Index]]"
  - "[[docs/analysis/mhc-backend/|MHC Backend Analyses]]"
  - "[[curriculum/README|Curriculum README]]"
---

# PROMPT: Análise Comparativa Completa — Arquitetura de Agentes de E-commerce entre `mhc-backend` (Produção) e Currículo KODA (Referência)

**Tipo:** Prompt de exploração, análise e geração de repositório completo  
**Tempo estimado de execução:** 4–8 horas com LLM  
**Repositório-alvo de análise:** `chatshop-io/mhc-backend`  
**Repositório de saída:** Novo repositório (a ser criado) para uso do time  
**Foco:** Agente KODA como agente conversacional de e-commerce via WhatsApp

---

## Como Usar Este Prompt

1. Clone o `mhc-backend` localmente (ou aponte para o repositório GitHub)
2. Cole este prompt completo em um LLM com capacidade de contexto longo (Claude Opus recomendado)
3. O LLM irá explorar o código, gerar a análise comparativa e estruturar um novo repositório
4. Revise os outputs, ajuste o que for necessário e publique o repositório para o time

---

## PROMPT COMPLETO

```
You are a senior software architect specializing in AI agent systems, e-commerce platforms, and conversational commerce. Your task is to perform a deep comparative analysis between two architectures for the same domain — a conversational e-commerce agent called KODA that sells sports supplements via WhatsApp.

**Your Mission:**

Explore the production codebase `chatshop-io/mhc-backend` (the real KODA agent running in production) and compare it against the KODA reference architecture described below (the idealized multi-agent e-commerce system). Generate a complete new repository containing the full comparative analysis, structured for team consumption and actionability.

---

## PART 1: CONTEXT — The Reference Architecture You Are Comparing Against

### KODA Reference Architecture (Target / Idealized)

KODA is a conversational WhatsApp sales agent for sports supplements. The reference architecture defines 8 specialized agents orchestrated through file-based coordination:

```
WhatsApp (Meta Cloud API)
    │
    ▼
ORCHESTRATOR LAYER
├── Planner Agent      — divides customer journey into stages
├── Router Agent       — classifies intent → routes to specialist
├── Scheduler Agent    — orders agent execution
└── Recovery Agent     — reloads from checkpoints on failure
    │
    ▼
BUSINESS AGENTS
├── Discovery Agent    — extracts intent, restrictions, budget, preferences → discovery.json
├── Catalog Agent      — queries inventory, prices, promotions → catalog_results.json
├── Generator Agent    — creates product recommendations, responses → recommendations.json
├── Evaluator Agent    — scores recommendations against rubric → evaluation.json
├── Order Agent        — validates, prices, processes payment → order_state.json
└── Fulfillment Agent  — coordinates warehouse, driver, delivery → fulfillment_plan.json

PERSISTENCE LAYER
├── SQLite checkpoints (one per critical stage)
├── JSON state files (customer_profile.json, cart.json, order_state.json, agent_plan.json)
├── Audit manifest per decision (manifest.json linking inputs → outputs)
└── File-based locks (order.lock.json with TTL)

COMPACTION LAYER
├── Sliding window (15-20 messages) + structured summary of old history
├── Critical metadata that never expires (allergies, preferences, budget, decisions)
└── Critically classification before summarization (not all facts are equal)
```

### Core E-commerce Patterns in the Reference Architecture

**Pattern 1: Generator/Evaluator Separation**
- Generator creates product recommendations at high temperature (creative, explores options)
- Evaluator scores each recommendation against a 4-dimension rubric at low temperature (rigorous)
- Rubric dimensions: Profile Fit (30%), Cost-Benefit (25%), Expected Satisfaction (25%), Operational Viability (20%)
- Only recommendations scoring ≥75/100 are shown to customer
- Top-3 are presented with score breakdowns visible for debugging

**Pattern 2: Sprint Contracts for Multi-Step Order Processing**
- Each e-commerce step has an explicit input/output contract:
  1. Validate Customer → {valid: bool, customer_data}
  2. Verify Inventory → [{sku, qty_available, reserved}]
  3. Calculate Price → {subtotal, discounts, total} (zero double-discount)
  4. Process Payment → {success, transaction_id} (idempotent)
  5. Schedule Fulfillment → {tracking_id, eta}
- Each contract is testable in isolation with clear acceptance criteria
- Contracts are validated at runtime, not just at compile time

**Pattern 3: State Persistence via Checkpoints**
- Each order has an explicit checkpoint file (order_state.json)
- Cart state survives process restart (durable, not in-memory)
- Customer profile is a unified artifact, not scattered across 6+ tables
- Every decision is auditable via manifest (which inputs produced which outputs)

**Pattern 4: Server-Side Compaction**
- When conversation exceeds window limit, old messages are summarized (not discarded)
- Facts are classified by criticality before summarization
- Critical metadata (allergies, budget, restrictions) never expires regardless of window
- Conversation summary is injected into agent prompt alongside semantic memories

**Pattern 5: Harness Evolution Governance**
- Each harness component has documented: cost, failure it prevents, value it provides
- Governance cycle: BUILD → STABILIZE → SIMPLIFY → REMOVE
- Metrics tracked: cost per agent, tokens per component, ROI per protection
- Components are removed when model capability makes them redundant

### E-commerce Journey States

```
AWARENESS → CONSIDERATION → DECISION → RETENTION
    │            │              │            │
    ▼            ▼              ▼            ▼
Discovery    Catalog         Order        Reorder
Onboarding   Comparison      Payment      Follow-up
Questions    Generator       Checkout     Loyalty
Memory       Evaluator       Fulfillment  Feedback
```

---

## PART 2: YOUR TASK — Explore, Compare, Generate

### Phase A: Deep Exploration of `mhc-backend`

Explore the `chatshop-io/mhc-backend` repository thoroughly. You MUST read (not guess) the following critical files:

**Core Agent Architecture:**
- `src/agents/agentsGraph.ts` — LangGraph wiring, agent graph topology
- `src/agents/orchastrator/OrchestratorAgent.ts` — Main orchestrator, state building, graph invocation
- `src/agents/orchastrator/ConversationStateBuilder.ts` — History windowing, cache, 15+ parallel queries
- `src/agents/graph/state.ts` — GraphState definition (Annotation.Root)
- `src/agents/graph/nodes/ecommerceAgenteNode.ts` — KODA e-commerce node, 20 tools, system prompt
- `src/agents/graph/nodes/routerNode.ts` — Intent classifier with structured output
- `src/config/agents.ts` — Agent registration and routing configuration

**E-commerce Tools (20+ tools):**
- `src/agents/graph/tools/ecommerce/SearchProductsTool.ts` — Product search + brand diversification
- `src/agents/graph/tools/ecommerce/AddToCartTool.ts` — Cart management
- `src/agents/graph/tools/ecommerce/CreateOrderTool.ts` — Order creation
- `src/agents/graph/tools/ecommerce/SendDeliveryFlowTool.ts` — Delivery flow initiation
- `src/agents/graph/tools/ecommerce/CalculateShippingTool.ts` — Shipping calculation
- All other e-commerce tools in `src/agents/graph/tools/ecommerce/`

**Prompts and Persona:**
- `src/agents/prompts/ecommerce/index.ts` — Main e-commerce prompt (~1800+ lines)
- `src/agents/prompts/persona/ecommerce.ts` — KODA persona ("Votu")
- `src/agents/prompts/global/` — Global rules, personality, memory, onboarding

**State and Persistence:**
- `prisma/schema.prisma` — All 50+ models including ConversationMemory, ConversationContext, EcommerceCart, CartItem, Order
- `src/services/ecommerce/CartService.ts` — Cart implementation (in-memory + DB hybrid)
- `src/services/ecommerce/OrderService.ts` — Order management
- `src/services/memory/MemoryService.ts` — Semantic memory CRUD with contradiction detection
- `src/services/memory/MemoryExtractionService.ts` — Background memory extraction via gpt-4.1-mini
- `src/services/ecommerce/ProductRecommendationFilter.ts` — Product filter based on onboarding

**Infrastructure:**
- `src/services/queue/MessageProcessingQueue.ts` — Sequential per-user processing
- `src/services/queue/MessageDebounceService.ts` — Message batching with Redis locks
- `src/services/proactive/` — Proactive triggers, anti-spam, cron locks
- `src/routes/webhook-unified.ts` — WhatsApp entry point (95KB, FSM, debounce, routing)
- `src/routes/webhook-payment.ts` — Payment webhook with HMAC + idempotency

**Existing Project Docs:**
- `AGENTS.md`
- `README.md`
- Any `docs/` directory
- `.github/PULL_REQUEST_TEMPLATE.md`

For EACH file you read, capture:
1. What e-commerce capability it implements
2. Which reference architecture pattern it maps to (or doesn't)
3. Its maturity level (N1-foundation, N2-visibility, N3-advanced, N4-optimized)
4. Specific code evidence (line numbers, function names, type signatures)
5. Gaps vs. the reference architecture

---

### Phase B: Structured Comparison Across 5 Dimensions

For each dimension below, produce a detailed comparison table with:
- **Concept**: What the reference architecture prescribes
- **mhc-backend (Production)**: What actually exists in code (with file:line references)
- **Gap**: What's missing or different
- **Severity**: CRITICAL / HIGH / MEDIUM / LOW
- **Incident Risk**: What real-world failure this gap could cause
- **Recommendation**: Concrete, actionable improvement (with estimated effort: lines of code)

**Dimension 1: Agent Decomposition (Multi-Agent vs Single-Agent)**

Compare how e-commerce responsibilities are decomposed:

| Check | Reference Expectation |
|-------|----------------------|
| Separate Planner agent that decides journey stage | Agent decides WHAT to do before doing it |
| Separate Discovery agent for intent extraction | Structured discovery.json artifact |
| Separate Catalog agent for inventory queries | Inventory queries are isolated and auditable |
| Separate Generator agent (high temp, creative) | Creative generation is separate from evaluation |
| Separate Evaluator agent (low temp, rigorous) | Quality scoring with rubric dimensions |
| Separate Order agent for the 6-step order pipeline | Each step has contract, validation, and audit |
| Separate Fulfillment agent for delivery coordination | Warehouse, driver, route, tracking coordination |
| Separate Recovery agent for failure handling | Checkpoint reload, retry with modified prompt |

**Dimension 2: Generator/Evaluator Pattern**

| Check | Reference Expectation |
|-------|----------------------|
| Generator and Evaluator are separate LLM calls | Different temperatures, different prompts |
| Evaluator uses a multi-dimension rubric (4+ dims) | Weighted scoring, not binary pass/fail |
| Score threshold for recommendation (≥75/100) | Below-threshold products are suppressed |
| Top-3 recommendations with breakdown | Customer sees alternatives with trade-offs |
| Evaluator can reject and request regeneration | Feedback loop between Generator and Evaluator |
| Scoring dimensions visible for debugging | You can explain WHY a product scored 8 vs 3 |

**Dimension 3: State Persistence and Checkpoints**

| Check | Reference Expectation |
|-------|----------------------|
| Cart survives process restart | Cart state is durable, not in-memory |
| Explicit checkpoints at critical stages | Before payment, after order creation, etc. |
| Unified customer profile artifact | Not scattered across 6+ tables |
| Audit manifest per decision | Traceable: input → tools → output |
| Order state is a single source of truth | order_state.json with versioned snapshots |
| Lock mechanism for concurrent operations | Order-level locks with TTL, not just message dedup |

**Dimension 4: Context and Memory Management**

| Check | Reference Expectation |
|-------|----------------------|
| Sliding window + structured summary | Old messages are summarized, not discarded |
| Critical metadata never expires | Allergies, budget, preferences survive any window size |
| Criticality classification before summarization | Medical restrictions > flavor preferences |
| Compaction pipeline for long conversations (4h+) | System handles conversations beyond window limit |
| Memory contradiction detection | System detects and resolves conflicting facts |
| Conversation summary injected into agent prompt | Agent sees both current window + historical summary |

**Dimension 5: Harness Governance and Observability**

| Check | Reference Expectation |
|-------|----------------------|
| Cost tracking per agent/component | Tokens and $ per LLM call, per agent |
| Harness component inventory | Each protection has documented: cost, value, failure mode |
| BUILD → STABILIZE → SIMPLIFY → REMOVE cycle | Formal process for harness evolution |
| Decision records (ADRs) | Why architectural choices were made |
| End-to-end trace replay | Reproduce exactly what happened in any turn |
| Tool call tracing with arguments | Structured log of every tool invocation |

---

### Phase C: Generate the Comparative Analysis Repository

Create a new repository directory structure. The output should be a complete, standalone project that the team can browse, reference, and use to drive KODA improvements.

#### Repository Structure

```
koda-ecommerce-comparison/
│
├── README.md                           # Landing page: what this is, how to use, quick nav
├── AGENTS.md                           # Rules for AI agents working in this repo
│
├── 00-executive-summary/
│   ├── 01-visao-geral.md               # 1-page executive summary: where KODA stands vs reference
│   ├── 02-matriz-maturidade.md          # Maturity matrix: N1-N4 across all dimensions  
│   └── 03-roadmap-priorizado.md         # Prioritized improvement roadmap with effort estimates
│
├── 01-exploracao-codigo/
│   ├── 01-arquitetura-agentes.md        # Agent graph topology, routing, node structure
│   ├── 02-pipeline-ecommerce.md         # Discovery → Order → Fulfillment tool chain
│   ├── 03-prompts-e-persona.md          # E-commerce prompt analysis (1800+ lines)
│   ├── 04-estado-e-persistencia.md      # PostgreSQL schema, CartService, MemoryService
│   ├── 05-contexto-e-memoria.md         # Sliding window, memory extraction, context building
│   ├── 06-infra-estrutura.md            # Queues, debounce, webhooks, anti-spam, cron
│   └── 07-inventario-tecnico.md         # Complete technical inventory (files, tools, models, stack)
│
├── 02-comparacao-dimensoes/
│   ├── 01-decomposicao-agentes.md       # Single-agent vs 8-agent comparison
│   ├── 02-generator-evaluator.md        # Scoring, rubric, separation analysis
│   ├── 03-estado-e-checkpoints.md       # Persistence maturity: in-memory → durable → auditable
│   ├── 04-contexto-e-compactacao.md     # Sliding window vs compaction pipeline
│   └── 05-governanca-e-observabilidade.md # Cost tracking, ADRs, harness evolution
│
├── 03-gaps-e-riscos/
│   ├── 01-gaps-criticos.md              # CRITICAL gaps with incident scenarios
│   ├── 02-gaps-altos.md                 # HIGH severity gaps
│   ├── 03-gaps-medios.md                # MEDIUM severity gaps
│   ├── 04-casos-de-incidente.md         # Realistic failure scenarios (Pedro, Marina, Rafael)
│   └── 05-matriz-risco.md               # Risk matrix: likelihood × impact per gap
│
├── 04-recomendacoes/
│   ├── 01-curto-prazo.md                # 2-4 weeks: quick wins, high impact
│   ├── 02-medio-prazo.md                # 4-8 weeks: structural improvements
│   ├── 03-longo-prazo.md                # 8-16 weeks: architectural transformation
│   └── 04-criterios-aceitacao.md        # Acceptance criteria per recommendation
│
├── 05-métricas-e-kpis/
│   ├── 01-metricas-atuais.md            # What's measured today (timings, traces, counts)
│   ├── 02-metricas-desejadas.md         # What should be measured (cost, quality, reliability)
│   └── 03-dashboard-proposto.md         # Proposed observability dashboard structure
│
├── 06-templates-e-ferramentas/
│   ├── 01-template-rubrica.md            # 4-dimension evaluation rubric template
│   ├── 02-template-sprint-contract.md    # Sprint contract template for order pipeline
│   ├── 03-template-checkpoint.md         # Order state checkpoint template
│   ├── 04-template-adr.md                # Architecture Decision Record template
│   ├── 05-template-harness-component.md  # Harness component inventory template
│   └── 06-checklist-implementacao.md     # Per-pattern implementation checklist
│
├── 07-aprendizados/
│   ├── 01-padroes-que-funcionam.md       # What mhc-backend does well (keep these)
│   ├── 02-padroes-que-faltam.md          # What's missing from reference (build these)
│   ├── 03-surpresas-arquiteturais.md     # Unexpected findings during exploration
│   └── 04-licoes-para-novos-projetos.md  # If starting fresh, what would you do differently
│
└── 08-referencias/
    ├── 01-curriculo-koda.md              # Mapping to curriculum levels N1-N4
    ├── 02-arquivos-criticos-mhc.md       # Index of critical files in mhc-backend
    ├── 03-glossario.md                   # Terminology glossary
    └── 04-bibliografia.md                # Related papers, talks, references
```

#### Content Requirements for Each File

**00-executive-summary/01-visao-geral.md:**
- 1-page summary: where production KODA is vs where reference says it should be
- Maturity score across 5 dimensions (% complete)
- Top 3 critical gaps with estimated business impact
- Quick-start: which section to read based on your role (developer, architect, PM, QA)

**00-executive-summary/02-matriz-maturidade.md:**
- Visual matrix: 5 dimensions × 4 maturity levels
- Color-coded: red (missing), yellow (partial), green (complete)
- Per-dimension breakdown with evidence from code
- Trend arrows: what's improving, what's static, what's degrading

**00-executive-summary/03-roadmap-priorizado.md:**
- Short-term (2-4 weeks): 3-5 items, estimated effort, expected impact
- Medium-term (4-8 weeks): 3-5 items, dependencies, risks
- Long-term (8-16 weeks): 2-3 architectural transformations
- Effort estimates in lines of code and engineer-weeks

**01-exploracao-codigo/*.md (7 files):**
- Each file documents ONE aspect of the production system
- Every claim backed by file:line references
- Include relevant code snippets (not whole files — just the evidence)
- End each file with "Key Observations" and "Open Questions"

**02-comparacao-dimensoes/*.md (5 files):**
- Each file compares ONE dimension
- Use the comparison table format from Phase B
- Include current maturity score and target maturity score
- Highlight "what would need to change" for each gap

**03-gaps-e-riscos/*.md (5 files):**
- Each gap includes: description, file evidence, severity, incident scenario, affected user journeys
- Incident cases (Pedro/cart, Marina/order, Rafael/context) in narrative format with root cause analysis
- Risk matrix visual (can be ASCII table)

**04-recomendacoes/*.md (4 files):**
- Each recommendation includes: gap it addresses, implementation approach, files to modify, acceptance criteria, estimated effort, dependencies on other recommendations
- Prioritized by: (business impact × implementation ease) / risk of not doing it

**05-metricas-e-kpis/*.md (3 files):**
- Current metrics inventory extracted from code (StageTimings, traces, logs)
- Proposed additional metrics with collection mechanism
- Dashboard structure recommendation

**06-templates-e-ferramentas/*.md (6 files):**
- Ready-to-use templates that the team can copy into their workflow
- Each template includes: when to use, fields to fill, example filled out

**07-aprendizados/*.md (4 files):**
- Patterns that work well in mhc-backend and should be preserved
- Patterns from reference that are missing
- Surprises: things you expected to find but didn't, or vice versa
- Lessons for greenfield projects

**08-referencias/*.md (4 files):**
- Curriculum mapping: which analysis files map to which curriculum modules
- Critical files index: every file referenced in the analysis with its role
- Glossary: all domain terms defined
- Bibliography: papers, talks, external references

---

### Phase D: Acceptance Criteria for the Generated Repository

The repository is COMPLETE when:

1. **All files exist** — 30+ markdown files across 8 directories
2. **Every comparison claim has code evidence** — file:line references, not opinions
3. **Every gap has a severity + incident scenario + recommendation**
4. **Executive summary is readable in 5 minutes** — anyone can understand where KODA stands
5. **Developers can act on recommendations** — clear what to change, where, and why
6. **PMs can prioritize** — effort estimates and business impact per recommendation
7. **QA can verify** — acceptance criteria per recommendation
8. **The repo AGENTS.md defines rules for future contributions** — the repo is maintainable
9. **Cross-references work** — you can navigate from summary → dimension → gap → recommendation
10. **Language is Portuguese** — all explanatory content in PT-BR (code identifiers remain English)

---

### Phase E: Specific E-commerce Patterns to Analyze Deeply

These are the highest-value patterns for the comparison. Give them extra depth:

**1. Product Discovery Flow (end-to-end)**
- How does the production system go from "Quero comprar whey" → product recommendation?
- What tools are called? What state is built? What validation happens?
- Compare against the reference: Discovery → Catalog → Generator → Evaluator pipeline
- Map the exact sequence of tool calls in a real discovery flow

**2. Cart and Order State Machine**
- Trace the exact state transitions: empty cart → item added → checkout → payment → confirmed
- What state is in memory? What's in Redis? What's in PostgreSQL?
- What survives a process restart? What doesn't?
- Compare against reference: unified order_state.json with checkpoint snapshots

**3. Payment and Fulfillment Integration**
- How does the webhook-payment.ts handle Stripe events?
- How does the delivery flow coordinate with external systems?
- What idempotency guarantees exist? Where are the gaps?
- Compare against reference: explicit order.lock.json + fulfillment_plan.json

**4. Memory and Personalization**
- How does the system remember that a customer is lactose-intolerant 3 months later?
- What's the recall mechanism? When does it fire? What's the fallback?
- How are contradictions handled (customer says "no restrictions" then later "lactose intolerant")?
- Compare against reference: critical metadata never expires + contradiction detection

**5. Conversation Longevity**
- What happens after message #61 on WhatsApp? (the window limit is 60)
- Is there a summary? Does the agent still know about allergies mentioned in message #10?
- How does Coach (5-message window) vs Ecommerce (60-message window) handle context loss differently?
- Compare against reference: compaction pipeline with criticality classification

---

### Phase F: Formatting and Quality Standards

**Every file must follow these rules:**

1. **Header**: Title, date, status (DRAFT / REVIEW / FINAL), author
2. **TL;DR**: 2-3 sentence summary at the top
3. **Evidence**: Every claim backed by file:line reference or code snippet
4. **Navigation**: Link to related files within the repo (use relative markdown links)
5. **Tables**: Use markdown tables for comparison data
6. **No speculation**: If you couldn't find something in the code, say "NOT FOUND" and where you looked
7. **Portuguese prose**: All explanations in PT-BR
8. **English code**: Code identifiers, file paths, function names in English

**Repository-level quality:**
- `README.md` has quick-nav by role (Developer, Architect, PM, QA)
- `AGENTS.md` defines contribution rules (similar to long-running-agents AGENTS.md)
- All cross-file links are relative and functional
- No broken references
- Glossary covers all domain terms

---

### Phase G: What NOT To Do

- Do NOT rewrite the mhc-backend code — this is analysis, not implementation
- Do NOT propose changes without first understanding what's there
- Do NOT skip reading files — every claim needs code evidence
- Do NOT speculate about what code "probably" does — read it
- Do NOT produce generic advice — every recommendation must be specific to KODA's codebase
- Do NOT ignore what works well — the analysis must acknowledge strengths, not just gaps
- Do NOT create the analysis without exploring the actual codebase first

---

## OUTPUT: The Complete Repository

Generate all files in the structure defined in Phase C. The repository should be self-contained, immediately useful to the team, and structured for ongoing maintenance as KODA evolves.

Begin with Phase A (exploration), document findings in Phase B (comparison), then generate the full repository structure in Phase C.
```
