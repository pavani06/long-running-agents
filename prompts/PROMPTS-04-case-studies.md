---
title: "Prompt: Generate Comprehensive Case Studies"
type: prompt
date: 2026-05-26
tags:
  - curriculo-conteudo
aliases:
  - case studies prompt
  - casos de estudo
  - geracao de casos
relates-to:
  - "[[prompts/PROMPTS-00-INDEX|Prompt Index]]"
  - "[[curriculum/09-case-studies/|Case Studies]]"
---

# 📝 PROMPT: Generate Comprehensive Case Studies

## Como Usar Este Prompt

Cole este prompt em um LLM para gerar 5 casos de estudo detalhados.

---

## PROMPT COMPLETO

```
You are a technical case study writer and systems architect. Your task is to create comprehensive, detailed case studies demonstrating how patterns from long-running agents are applied in real scenarios.

**Context:**
- Purpose: Show real-world application of course concepts
- Scenarios: 2 generic + 3 KODA-specific
- Audience: FutanBear technical team
- Format: Detailed markdown with architecture diagrams, code examples, and lessons learned

**CASE STUDIES TO CREATE:**

## 1. **GENERIC CASE STUDY: Retro Game Maker**

**Source:** Anthropic's presentation example
**Complexity Level:** Nível 2-3
**Duration:** 6+ hours of agent runtime

### Problem Statement
Build a retro-style game maker web application. User gives one-line prompt: "Build a retro game maker with sprite editor and level designer."

### Initial Approach (Failed)
```
Single agent:
├─ Received prompt
├─ Tried to build everything at once
├─ Ran out of context at 2 hours
├─ Output: Broken, incomplete app
└─ Cost: $200, 6 hours wasted
```

### Solution: Multi-Agent Harness
```
Phase 1: Planner (5 min)
├─ Input: "Build a retro game maker"
├─ Output: spec.md with 10 sprints
├─ Features: Sprite editor, level designer, play mode, etc.

Phase 2: Generator (2 hrs for Sprint 1)
├─ Builds: Sprite editor UI
├─ Uses: React + Canvas
├─ Output: Working feature + code

Phase 3: Evaluator (10 min for Sprint 1)
├─ Tests: Can user create sprite?
├─ Grades: Against rubric
├─ Feedback: What's wrong/missing

Repeat for Sprints 2-10 (5-6 hours total)
```

### Results
```
Generator/Evaluator Approach:
├─ Completed: 6 hours runtime
├─ Output: Fully working game maker
├─ Features: Sprite editor, level designer, play mode, AI assist
├─ Quality: Coherent, polished, extra features
├─ Cost: $200, but 6 hours well-spent
```

### Key Patterns Used
1. **Planner:** Decompose into 10 sprints
2. **Sprint Contracts:** Define what "done" means per sprint
3. **Generator/Evaluator:** Separate build from quality check
4. **Trace Reading:** Debug when things go wrong
5. **Context Management:** Each sprint resets context

### Lessons Learned
1. **Planning Works:** Decomposition prevented context collapse
2. **Separation of Concerns:** Evaluator caught issues generator missed
3. **Contracts Matter:** Clear acceptance criteria = better output
4. **Iteration: ** Multi-pass is better than single attempt
5. **Token Budgeting:** Sprints prevent context waste

### KODA Application
This pattern applies to KODA's feature development:
- **Planner:** Routes customer journey into sprints
- **Generator:** Executes each step
- **Evaluator:** Verifies order accuracy before fulfillment

---

## 2. **GENERIC CASE STUDY: Browser DAW (Digital Audio Workstation)**

**Complexity Level:** Nível 3-4
**Duration:** 3.5+ hours of agent runtime
**Special Focus:** State persistence + file-based coordination

### Problem Statement
Build a browser-based music production tool. Features: timeline, synth controls, recording, playback.

### Architecture

```
Browser DAW: 3-Agent System
├─ Planner Agent (strategist)
│  ├─ Input: User's music project
│  ├─ Output: Build plan (4 sprints)
│  └─ Time: 5 min
│
├─ Generator Agent (builder)
│  ├─ Builds one sprint at a time
│  ├─ Reads/writes to state files
│  ├─ No context resets
│  └─ Time: 90 min per sprint
│
└─ Evaluator Agent (critic)
   ├─ Plays the audio
   ├─ Tests user interactions
   ├─ Grades against rubric
   └─ Time: 5-10 min per sprint
```

### State Persistence Example

```
project-files/
├── state.json
│   {
│     "project_name": "Summer Song",
│     "bpm": 120,
│     "tracks": [
│       {"id": "synth1", "notes": [...]},
│       {"id": "drums", "notes": [...]}
│     ],
│     "timeline_length": 8
│   }
│
├── generator_progress.md
│   "Currently building: Synth controls"
│   "Completed: Timeline UI, Note entry"
│   "Next: Audio playback"
│
├── evaluator_findings.md
│   "Sprint 1 Results:"
│   "✓ Timeline renders 8 bars"
│   "✗ Notes don't sync to playback"
│   "→ Recommend: Implement audio clock"
│
└── audit_log.json
   [timestamp changes]
```

### Results

```
Runtime: 3 hours 50 minutes
Cost: $124.70

Phase Breakdown:
├─ Planner: 5 min ($0.46)
├─ Generator Sprint 1: 2h 7min ($71.08)
├─ Evaluator Sprint 1: 8.8min ($3.24)
├─ Generator+Evaluator Sprints 2-3: 1h 30min ($50.00)

Final Output:
✓ Full timeline editor
✓ Synth controls with knobs
✓ Recording functionality
✓ Playback with sync
✓ UI is polished
✓ Handles real music workflows
```

### Key Patterns Used
1. **Multi-Agent Coordination:** Planner → Generator → Evaluator
2. **File-Based State:** JSON files persist across sessions
3. **Continuous Build:** No context resets (using Opus 4.6)
4. **Progressive Evaluation:** Each sprint graded before next
5. **Harness Simplification:** Opus 4.6 enables single-pass eval

### Lessons Learned
1. **State Files are Powerful:** JSON serialization prevents context bloat
2. **Continuous Build:** 4.6 model can handle 2+ hour builds
3. **Quality Improves:** Iteration through sprints = coherent system
4. **Emergent Features:** Generator added features not in original spec
5. **Naming Helps:** Good file names prevent state confusion

### KODA Application
DAW patterns → KODA patterns:
- **Timeline = Conversation:** Both are sequential
- **Synth controls = Product catalog:** Both are config options
- **Recording = Order history:** Both track what happened
- **Playback = Replay conversation:** Both verify accuracy

---

## 3. **KODA CASE STUDY: Product Discovery**

**Complexity Level:** Nível 2-3
**Focus:** Generator/Evaluator for recommendation quality

### Problem
KODA needs to recommend products that:
1. Match customer's needs
2. Are in stock
3. Offer good value
4. Are currently promoted

Customer: "I'm training for a marathon and need nutrition"

### Solution: Generator/Evaluator

```
Generator (Product Recommender):
├─ Input: Customer context (marathon training)
├─ Process:
│  ├─ Query product database
│  ├─ Filter by category (nutrition)
│  ├─ Match to customer level
│  ├─ Check stock
│  └─ Apply promotions
├─ Output: 3 recommendations with details
└─ Example: "Carbo-loading mix - 5kg - $35 (was $50)"

Evaluator (QA):
├─ Checks generator's work:
│  ├─ Is product real? (verify SKU)
│  ├─ Is price correct? (check promotions)
│  ├─ Is it in stock? (verify inventory)
│  ├─ Is recommendation relevant? (check rubric)
│  └─ Would customer be happy? (assess value)
├─ Rubric grades:
│  ├─ Relevance to goal: 8/10 (marathon nutrition)
│  ├─ Price value: 9/10 (40% off current)
│  ├─ Clarity: 7/10 (could explain why better)
│  └─ Overall: 8/10 → Approved
└─ If issue found: Send back to generator

Contract:
"Generator will recommend products that:
1. Directly support stated goal (marathon training)
2. Are in stock right now
3. Have price within +/- 5% of current promotions
4. Include clear explanation of why recommended
Evaluator will verify all 4 before approving"
```

### Results

```
Before (Single Agent):
├─ Recommendation time: 2-5 minutes
├─ Accuracy: 75% (sometimes wrong stock)
├─ Quality: Mixed (some recommendations mediocre)
└─ Customer satisfaction: 70%

After (Generator/Evaluator):
├─ Recommendation time: 3-5 minutes (small overhead)
├─ Accuracy: 98% (evaluator catches issues)
├─ Quality: 92% (rubric grades high)
└─ Customer satisfaction: 88%
```

### Metrics

```
Improved Metrics:
├─ Stock accuracy: 75% → 98%
├─ Wrong recommendations: 20% → 2%
├─ Customer satisfaction: 70% → 88%
├─ Repeat purchase rate: 35% → 52%
└─ Return rate: 15% → 6%

Cost Impact:
├─ Added latency: +1-2 seconds
├─ Model cost: +15% (2 calls instead of 1)
├─ Revenue impact: +52% repeat purchases = +30% revenue
└─ ROI: 2x cost → 30x benefit
```

### Key Patterns Used
1. **Generator/Evaluator:** Separate recommendation from verification
2. **Rubric Design:** Grades both objective & subjective criteria
3. **Sprint Contracts:** Define what "good recommendation" means
4. **Trace Reading:** Debug why recommendations go wrong

### Lessons Learned
1. **Separation Works:** Evaluator catches errors generator misses
2. **Rubrics Enable Scale:** Clear criteria = consistent quality
3. **Small Cost, Big Benefit:** +15% cost → +30% revenue
4. **Trust Through Verification:** Customers trust verified recommendations
5. **Patterns are Universal:** Same pattern works for many features

---

## 4. **KODA CASE STUDY: Order Processing**

**Complexity Level:** Nível 3
**Focus:** Sprint contracts for multi-step workflows

### Problem
KODA's order processing is complex:
1. Validate customer
2. Check inventory
3. Calculate price (with club discounts)
4. Apply promotions
5. Process payment
6. Schedule fulfillment

Single agent fails ~5% of orders (wrong prices, double charges, etc.)

### Solution: Multi-Step Sprint Contracts

```
Sprint 1: Validate Customer
Contract: "Accept customer_id, return {valid: bool, customer_data: {...}}"
Generator: Queries customer database
Evaluator: Verifies customer exists, not blocked, payment on file
Test: 10 real & fake customer IDs

Sprint 2: Check Inventory
Contract: "Accept [sku], return [{sku, quantity_available, reserve: bool}]"
Generator: Queries real-time inventory
Evaluator: Verifies quantities, holds items, handles race conditions
Test: Concurrent orders, low stock scenarios

Sprint 3: Calculate Price
Contract: "Accept {customer, items}, return {subtotal, discounts, total}"
Generator: Applies club pricing, bulk discounts, promotions
Evaluator: Verifies math, checks promotion terms, prevents double-discount
Test: Edge cases (expired promos, conflicting discounts)

Sprint 4: Process Payment
Contract: "Accept {customer, total}, return {success: bool, transaction_id: str}"
Generator: Calls payment API
Evaluator: Verifies transaction, checks for duplicates, logs receipt
Test: Real payment flows, error handling

Sprint 5: Schedule Fulfillment
Contract: "Accept {order_id, customer_address}, return {tracking_id, eta}"
Generator: Contacts fulfillment system, schedules delivery
Evaluator: Verifies address valid, ETA reasonable, everything confirmed
Test: Same-day delivery, international shipping, edge locations
```

### Results

```
Before (Single Agent):
├─ Order accuracy: 95% (5% errors)
├─ Errors breakdown:
│  ├─ Wrong price: 2%
│  ├─ Double charges: 1%
│  ├─ Wrong address: 1%
│  └─ Unfulfilled: 1%
├─ Customer complaints: High
└─ Manual review rate: 10%

After (Sprint Contracts):
├─ Order accuracy: 99.8% (0.2% errors)
├─ Errors breakdown:
│  ├─ Wrong price: 0.05%
│  ├─ Double charges: 0%
│  ├─ Wrong address: 0.1%
│  └─ Unfulfilled: 0.05%
├─ Customer complaints: 80% reduction
└─ Manual review rate: 1%
```

### State Persistence

```
order-state/
├── order_12345.json
│   {
│     "customer_id": "cust_999",
│     "items": [{sku, qty, price}],
│     "validations": {
│       "customer_valid": true,
│       "inventory_reserved": true,
│       "price_final": true,
│       "payment_processed": true,
│       "fulfillment_scheduled": true
│     },
│     "status": "confirmed",
│     "created": "2026-05-23T10:30:00Z"
│   }
│
└── order_audit.log
   "2026-05-23T10:30:00Z - Order created"
   "2026-05-23T10:30:15Z - Customer validated"
   "2026-05-23T10:30:45Z - Inventory reserved"
   "2026-05-23T10:31:00Z - Price calculated ($159.99)"
   "2026-05-23T10:31:30Z - Payment processed (txn_abc123)"
   "2026-05-23T10:32:00Z - Fulfillment scheduled (tracking_123)"
```

### Key Patterns Used
1. **Sprint Contracts:** Clear acceptance criteria per step
2. **State Persistence:** Track order through 5 steps
3. **Multi-Agent:** Each sprint is separate agent or subprocess
4. **Evaluation:** Verify each step before proceeding
5. **Error Handling:** Know exactly where failures happen

### Lessons Learned
1. **Contracts Prevent Errors:** Clear definitions = fewer mistakes
2. **State Tracking is Critical:** Can always see where order is
3. **Step-by-Step is Safer:** Better to fail early than process bad data
4. **Validation Layers Work:** Each step verifies previous
5. **Audit Trail Required:** Recovery needs to know what happened

---

## 5. **KODA CASE STUDY: Fulfillment & Same-Day Delivery**

**Complexity Level:** Nível 4
**Focus:** Complex state persistence + multi-agent coordination

### Problem
KODA promises same-day delivery. This requires:
1. Inventory from warehouse
2. Packing verification
3. Driver assignment
4. Route optimization
5. Real-time customer updates
6. Delivery confirmation

All must happen within hours, with high reliability.

### Solution: 3-Agent System with Persistent State

```
Agent 1: Logistics Planner
├─ Input: Orders to fulfill today
├─ Job: Route optimization, driver assignments
├─ Output: fulfillment_plan.json
└─ Time: Runs every 30 minutes

Agent 2: Fulfillment Executor
├─ Reads: fulfillment_plan.json
├─ Job: Coordinate with warehouse, packing, driver dispatch
├─ Writes: fulfillment_status.json (updated every 5 min)
└─ Time: Continuous all day

Agent 3: Quality Verifier
├─ Reads: fulfillment_status.json
├─ Job: Verify accuracy, driver compliance, customer feedback
├─ Writes: verification_report.json
└─ Time: Spot checks + end-of-day report
```

### State Files

```
fulfillment-state/
├── fulfillment_plan.json
│   {
│     "timestamp": "2026-05-23T08:00:00Z",
│     "orders_to_fulfill": 47,
│     "drivers_available": 8,
│     "routes": [
│       {
│         "driver_id": "drv_001",
│         "orders": ["ord_123", "ord_124", "ord_125"],
│         "estimated_time": 90,
│         "stops": 3
│       },
│       ...
│     ]
│   }
│
├── fulfillment_status.json (LIVE, updated every 5 min)
│   {
│     "timestamp": "2026-05-23T10:45:00Z",
│     "orders_progress": {
│       "ord_123": {
│         "status": "in_transit",
│         "driver": "drv_001",
│         "eta": "2026-05-23T11:15:00Z",
│         "customer_notified": true,
│         "last_update": "2026-05-23T10:40:00Z"
│       },
│       "ord_124": {
│         "status": "delivered",
│         "delivered_at": "2026-05-23T10:30:00Z",
│         "signature": "verified"
│       }
│     }
│   }
│
├── verification_report.json (EOD)
│   {
│     "date": "2026-05-23",
│     "orders_fulfilled": 47,
│     "on_time": 46,
│     "late": 1,
│     "issues": [
│       {
│         "order_id": "ord_999",
│         "issue": "Wrong address initially",
│         "resolved": "Corrected via agent, re-routed"
│       }
│     ],
│     "quality_score": 98
│   }
```

### Real-Time Coordination Flow

```
Morning (6 AM):
- Planner reads: Orders from previous day + new orders
- Planner outputs: fulfillment_plan.json (47 orders, 8 drivers)
- Cost: $0.15, 2 minutes

Midday (10 AM):
- Executor reads: fulfillment_plan.json
- Executor coordinates: Warehouse packing, driver dispatch
- Executor writes: fulfillment_status.json (46 delivered, 1 in transit)
- Continuous operation, updates every 5 min
- Cost: $1.20/hour

Verification (throughout):
- Verifier spot-checks: Sample 10% of deliveries
- Verifier checks: Address correct, package condition, customer happy
- Verifier updates: verification_report.json with findings

Evening (7 PM):
- Final report shows: 47/47 orders fulfilled, 46/47 on-time, 98% quality
- Issues: 1 wrong address (caught and fixed), 1 late (traffic)
- Next day: Planner adjusts routes based on learnings
```

### Results

```
Before (Manual + Single Agent):
├─ Orders fulfilled: 85% same-day
├─ Late deliveries: 12%
├─ Wrong address: 3%
├─ Customer satisfaction: 72%
├─ Manual work: 30 hours/day

After (Multi-Agent + State):
├─ Orders fulfilled: 99.5% same-day
├─ Late deliveries: 1%
├─ Wrong address: 0.1%
├─ Customer satisfaction: 94%
├─ Manual work: 2 hours/day (exceptions only)
```

### Key Patterns Used
1. **Planner/Executor/Verifier:** Separation of concerns
2. **Persistent State:** JSON files are source of truth
3. **Real-Time Updates:** fulfillment_status updated every 5 min
4. **Continuous Operation:** 12+ hour runtime for fulfillment agent
5. **Verification Loop:** Spot checks catch issues early
6. **Audit Trail:** Know exactly what happened when

### Lessons Learned
1. **Persistent State is Critical:** Can't lose track of orders
2. **Real-Time Updates Matter:** Customers need live tracking
3. **Continuous Operation:** Agents can run 12+ hours with compaction
4. **Spot Verification Works:** Don't need to verify everything, just enough
5. **Learning Loop:** Each day improves based on previous learnings
6. **Scale:** System handles 47+ orders/day without increasing cost proportionally

---

## FORMAT FOR EACH CASE STUDY

```markdown
# Case Study: [Name]

**Complexity Level:** [Nível X]
**Duration:** [Runtime hours]
**Focus:** [Key patterns]

## Problem Statement
[Clear description of challenge]

## Initial Approach (Before)
[What didn't work]

## Solution (After)
[What worked]

## Architecture
[Diagram or ASCII representation]

## State Management
[How data is persisted]

## Results
[Metrics improvement]

## Key Patterns Used
[Which course concepts apply]

## Lessons Learned
[Takeaways for team]

## KODA Application
[How this applies to KODA]
```

---

## DELIVERABLES

1. **Generic Case Study 1:** Retro Game Maker (fully detailed)
2. **Generic Case Study 2:** Browser DAW (fully detailed)
3. **KODA Case Study 1:** Product Discovery (fully detailed)
4. **KODA Case Study 2:** Order Processing (fully detailed)
5. **KODA Case Study 3:** Fulfillment & Same-Day Delivery (fully detailed)

**Total:** 5 comprehensive case studies with:
- Problem statements
- Architecture diagrams
- State management examples
- Results/metrics
- Key lessons
- KODA application guidance

Each case study should be 1,000-1,500 words with real examples.
```

---

## 📌 Notas de Uso

1. **Gere em fases:**
   - Fase 1: Retro Game Maker (20 min)
   - Fase 2: Browser DAW (20 min)
   - Fase 3: KODA Product Discovery (15 min)
   - Fase 4: KODA Order Processing (15 min)
   - Fase 5: KODA Fulfillment (15 min)
   - Total: ~1.5 horas

2. **Inclua:**
   - Problema claro
   - Solução com patterns
   - Arquitetura visual
   - Métricas antes/depois
   - Lições aprendidas

3. **Tamanho:** 1,000-1,500 palavras por caso

4. **Salve em:**
   - Casos genéricos: `09-case-studies/`
   - Casos KODA: `09-case-studies/` (com prefixo koda-)

---

*Prompt | Casos de Estudo | v1.0*
