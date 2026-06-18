---
title: "Prompt: Generate Practical Exercises and Solutions"
type: prompt
date: 2026-05-26
tags:
  - curriculo-conteudo
aliases:
  - exercises prompt
  - exercicios praticos
  - geracao de exercicios
relates-to:
  - "[[prompts/PROMPTS-00-INDEX|Prompt Index]]"
  - "[[curriculum/README|Curriculum README]]"
---

# 📝 PROMPT: Generate Practical Exercises and Solutions

## Como Usar Este Prompt

Cole este prompt em um LLM para gerar todos os exercícios com soluções.

---

## PROMPT COMPLETO

```
You are an experienced course designer and technical educator. Your task is to create practical, hands-on exercises for a long-running agents curriculum.

**Context:**
- Program: Long-Running Agents for KODA
- Audience: FutanBear technical team
- Primary Application: KODA (conversational AI for sports supplement sales)
- Exercise Levels: 4 (Nível 1-4)
- Format: Markdown with clear problem statements, hints, and solutions

**REQUIREMENTS:**

## 1. **NÍVEL 1 EXERCISES (2 total, ~1 hour)**

### Exercise 1-1: Identify the Three Problems
**Duration:** 30 minutes
**Level:** Beginner
**Objective:** Recognize why agents lose the plot

**Problem Statement:**
You're observing KODA failing in a customer conversation. After 45 minutes of discussing products, KODA suddenly starts recommending completely wrong items. By hour 2, KODA seems "tired" and gives short, rushed responses. In hour 3, KODA approves a customer order that's clearly wrong (ordered 5000 units of one product).

**Your Tasks:**
1. Identify which of the 3 "reasons agents lose the plot" each failure represents
2. For each problem, explain WHY it happens (technical mechanism)
3. Propose a ONE-SENTENCE fix for each

**Hints:**
- Problem 1 happens first (time-based)
- Problem 2 happens when agent tries too much at once
- Problem 3 is about judgment, not capability

**Success Criteria:**
- [ ] Correctly mapped all 3 failures to the 3 problems
- [ ] Explained technical mechanisms (context windows, planning, sycophancy)
- [ ] Proposed reasonable fixes

---

### Exercise 1-2: Token Budgeting for KODA
**Duration:** 30 minutes
**Level:** Beginner
**Objective:** Understand token management

**Problem Statement:**
You're allocating tokens for KODA's conversation:
- Total available: 1,000,000 tokens (Opus 4.6)
- Conversation with customer so far: 45,000 tokens
- System prompt + instructions: 5,000 tokens
- KODA's internal state (JSON): 2,000 tokens

**Your Tasks:**
1. Calculate remaining tokens for KODA to operate
2. If KODA needs 10,000 tokens per response, how many more responses can it give?
3. How should KODA prepare for running out of tokens?

**Hints:**
- Budget = Total - History - System - State
- Be conservative in your calculations
- Token limits aren't hard walls, they're guardrails

**Success Criteria:**
- [ ] Correct token calculations
- [ ] Realistic response estimate
- [ ] Viable preparation strategy

---

## 2. **NÍVEL 2 EXERCISES (3 total, ~3 hours)**

### Exercise 2-1: Design Generator/Evaluator for Feature X
**Duration:** 60 minutes
**Level:** Intermediate
**Objective:** Apply generator/evaluator pattern

**Problem Statement:**
Design a generator/evaluator pair for KODA's "Apply Promotions" feature.

Customer says: "I have a club membership. Do I get a discount?"
Expected: KODA checks if customer is club member, applies 20% discount if yes

**Your Tasks:**
1. **Define Generator Role:**
   - What is the generator's job? (be specific)
   - What tools/data does it need?
   - What should it output?

2. **Define Evaluator Role:**
   - What is the evaluator's job?
   - How will it verify the generator's work?
   - What criteria will it grade against?

3. **Design the Handoff:**
   - How will they communicate?
   - What does "done" mean?
   - How many iterations before completion?

**Hints:**
- Generator: handles business logic
- Evaluator: verifies correctness
- Use files or structured messages for handoff
- Consider edge cases (invalid membership, expired, etc.)

**Success Criteria:**
- [ ] Clear generator responsibilities
- [ ] Specific evaluator criteria
- [ ] Defined communication protocol
- [ ] Handles edge cases

---

### Exercise 2-2: Write Sprint Contracts
**Duration:** 60 minutes
**Level:** Intermediate
**Objective:** Define testable acceptance criteria

**Problem Statement:**
KODA's "Check Inventory" feature needs a contract between generator and evaluator.

Feature: Check if product is in stock for customer's request
Generator proposes: "I'll query the inventory API and return stock level"

**Your Tasks:**
1. **As Generator**, write what you'll build:
   - What input will you accept?
   - What output will you produce?
   - What are you responsible for?

2. **As Evaluator**, write what you'll test:
   - What does "correct" mean?
   - What edge cases matter?
   - What could go wrong?

3. **Negotiate the Contract:**
   - Find a middle ground
   - Define 5-7 specific, testable criteria
   - Both sides agree

**Example Criteria:**
- [ ] Returns JSON with format: {sku, quantity_in_stock, last_updated}
- [ ] Handles out-of-stock by returning quantity_in_stock = 0 (not null/error)
- [ ] Queries API within 2 seconds
- [ ] Works for all 50,000+ products in catalog
- [ ] Returns "error" gracefully if API is down (no crashes)

**Your Task:** Write 5-7 criteria for inventory checking

**Success Criteria:**
- [ ] Criteria are specific (not vague)
- [ ] Criteria are testable (can verify yes/no)
- [ ] Both sides agreed (no unrealistic demands)
- [ ] Edge cases covered

---

### Exercise 2-3: Create Evaluation Rubric
**Duration:** 60 minutes
**Level:** Intermediate
**Objective:** Define criteria for subjective quality

**Problem Statement:**
KODA's product recommendations need grading. But "good recommendation" is subjective. Create a rubric.

Example KODA response: "Based on your interest in strength training, I recommend Whey Protein 5kg - it has excellent reviews and is on sale this week at $45 (normally $60)."

**Your Tasks:**
1. Define 4 evaluation criteria for KODA's recommendations
2. For each criterion, create a 1-10 scale with what 1, 5, 10 mean
3. Assign weights (importance)
4. Grade the example response

**Suggested Criteria:**
- Relevance to customer (does recommendation match their needs?)
- Accuracy of information (are price/product details correct?)
- Clarity of explanation (can customer understand why?)
- Value proposition (is the deal actually good?)

**Your Rubric Format:**
```
Criterion: [Name]
Weight: [%]
1 point: [What bad looks like]
5 points: [What ok looks like]
10 points: [What excellent looks like]
```

**Grade the Example:**
- Relevance: __ / 10
- Accuracy: __ / 10
- Clarity: __ / 10
- Value: __ / 10
- **Final Score:** (sum / 4) = __ / 10

**Success Criteria:**
- [ ] 4 relevant criteria defined
- [ ] Clear 1-5-10 point definitions
- [ ] Weights assigned
- [ ] Example graded with justification

---

## 3. **NÍVEL 3 EXERCISES (3 total, ~4 hours)**

### Exercise 3-1: Design 3-Agent KODA System
**Duration:** 90 minutes
**Level:** Advanced
**Objective:** Design multi-agent architecture

**Problem Statement:**
KODA currently runs as a single agent. Design a 3-agent system (Planner, Generator, Evaluator) for handling this customer journey:
1. Customer enters chat
2. Customer asks about protein powders
3. KODA recommends products
4. Customer adds items to cart
5. Customer pays
6. KODA arranges delivery

**Your Tasks:**

1. **Design the Planner:**
   - Input: Customer's initial message
   - Output: Workflow plan
   - Example: "First discover needs → then recommend → then checkout"

2. **Design the Generator:**
   - What does it build?
   - What tools does it use?
   - How long can it run?

3. **Design the Evaluator:**
   - How does it verify?
   - What are success criteria?
   - When does it stop/restart?

4. **Design Coordination:**
   - How do the 3 talk to each other?
   - What state gets passed?
   - How long can the whole system run?

**Success Criteria:**
- [ ] Clear role definitions
- [ ] Specified tool access
- [ ] Defined communication protocol
- [ ] State persistence strategy
- [ ] Can handle 2+ hour conversations

---

### Exercise 3-2: Implement State Persistence
**Duration:** 90 minutes
**Level:** Advanced
**Objective:** Design file-based state management

**Problem Statement:**
KODA's 3-agent system needs to persist state across sessions. Design the persistence layer.

**Your Tasks:**

1. **Define State Structure:**
   ```json
   {
     "conversation_id": "...",
     "timestamp": "...",
     "customer": {...},
     "cart": [...],
     "workflow_stage": "...",
     "...more state...": "..."
   }
   ```

2. **Design File Organization:**
   - Where does state live? (folder structure)
   - How is it named? (naming convention)
   - How often is it updated?

3. **Design State Transitions:**
   - When planner writes, what changes?
   - When generator writes, what changes?
   - When evaluator writes, what changes?
   - Can they overwrite each other? How prevent conflicts?

4. **Design Recovery:**
   - If one agent crashes, can we recover?
   - How do we know if state is corrupt?
   - Can we rollback?

**Example File Structure:**
```
conversations/
├── conv_12345/
│   ├── state.json (main state)
│   ├── conversation_history.json
│   ├── workflow_plan.md
│   ├── evaluator_findings.md
│   └── audit_log.json
```

**Your Task:** Design complete persistence strategy

**Success Criteria:**
- [ ] Clear state structure defined
- [ ] File organization logical
- [ ] Conflict prevention strategy
- [ ] Recovery mechanism
- [ ] Audit capability

---

### Exercise 3-3: Simulate Harness Evolution
**Duration:** 90 minutes
**Level:** Advanced
**Objective:** Understand how to simplify as models improve

**Problem Statement:**
Compare KODA's harness on Opus 4.5 vs 4.6:

**Opus 4.5 Setup:**
```
- Resets context between sessions (required)
- Decomposes into 1 feature per sprint (required)
- Runs evaluator per sprint (required)
- Planner specifies 200+ features upfront (required)
- Total harness complexity: HIGH
```

**Opus 4.6 Improvement:**
```
- Server-side compaction (handles own context)
- Can run 2+ hours continuously
- Better planning capability
- Can handle flexible scope
```

**Your Tasks:**

1. **What can be removed?**
   - [ ] Context resets? (Maybe, if model is good at compaction)
   - [ ] Sprint decomposition? (Maybe, if model can handle 2+ hrs)
   - [ ] Per-sprint evaluation? (Maybe, if can do single pass)
   - [ ] Detailed planning? (Maybe, if model is more agentic)

2. **For each, explain:**
   - What problem did it solve on 4.5?
   - Why does 4.6 not need it?
   - What's the risk of removing it?
   - How would you test removal?

3. **Design the Simplified Harness:**
   - Draw it (text or ASCII art)
   - Show data flow
   - Explain what's left and why

**Success Criteria:**
- [ ] Identified all removable components
- [ ] Explained why each can be removed
- [ ] Assessed risks
- [ ] Designed simplified version
- [ ] Clear reasoning

---

## 4. **NÍVEL 4 EXERCISES (2 real-world, ~4 hours)**

### Exercise 4-1: Analyze Real KODA Trace
**Duration:** 120 minutes
**Level:** Expert
**Objective:** Diagnose issues from actual agent behavior

**Problem Statement:**
You're given a KODA trace where the agent failed to properly apply a customer's club discount. 

[Sample Trace:]
```
Input: "I have a club membership"
Agent thought: "Customer mentioned club, I should apply discount"
Action 1: Query customer profile
Result 1: {club_member: true, membership_level: "gold", expires: "2026-06-30"}
Action 2: Query current promotions
Result 2: {club_discount: 0.20, non_member_promos: [...]}
Agent thought: "Got 20% discount, should apply"
Output: "Great! I found your club membership. You get 20% off."
---
PROBLEM: Customer's order was processed WITHOUT the discount
```

**Your Tasks:**

1. **Identify What Went Wrong:**
   - Generator said it would apply discount (it didn't)
   - Where is the gap between intention and action?
   - Is it a generator issue or integration issue?

2. **Root Cause Analysis:**
   - What's the actual failure?
   - Is it a logic error? Data error? Integration error?
   - Why didn't tests catch this?

3. **Design Evaluator Test:**
   - What should evaluator check?
   - How would evaluator have caught this?
   - Write specific test criteria

4. **Propose Fix:**
   - How would you prevent this?
   - Code change? Harness change? Process change?
   - How verify fix works?

**Success Criteria:**
- [ ] Root cause identified
- [ ] Evaluator test designed
- [ ] Fix proposed with rationale
- [ ] Prevents regression

---

### Exercise 4-2: Propose KODA Improvement
**Duration:** 120 minutes
**Level:** Expert
**Objective:** Apply all patterns to real improvement

**Problem Statement:**
KODA sometimes recommends products that have been discontinued. Customers get excited, then disappointed when they can't buy.

**Your Tasks:**

1. **Define the Problem:**
   - Why does this happen? (root cause)
   - How often? (frequency)
   - Impact on customer? (severity)

2. **Design Solution Using Patterns:**
   - Use generator/evaluator? Why/why not?
   - Use sprint contracts? For what?
   - Use rubrics? For what criteria?
   - Use state persistence? For what state?

3. **Design the Implementation:**
   - Which agent handles this?
   - What state needs persistence?
   - What's the evaluator testing?
   - Timeline to implement?

4. **Design the Evaluation:**
   - How measure success?
   - What metrics?
   - What edge cases to test?
   - How validate fix?

**Success Criteria:**
- [ ] Problem clearly defined
- [ ] Solution designed using course patterns
- [ ] Implementation plan detailed
- [ ] Evaluation criteria specific
- [ ] Considers edge cases

---

## 5. **OUTPUT SPECIFICATIONS**

### Format for Each Exercise:
```markdown
# Exercise N-X: [Title]

**Duration:** X minutes
**Level:** Beginner/Intermediate/Advanced/Expert
**Objective:** [What student learns]

## Problem Statement
[Clear description of problem/scenario]

## Your Tasks
1. Task 1
2. Task 2
3. Task 3

## Hints
- Hint 1
- Hint 2

## Success Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

---

## SOLUTION

[Complete solution with explanation]

### Answer to Task 1
[Detailed answer]

### Answer to Task 2
[Detailed answer]

### Answer to Task 3
[Detailed answer]

### Key Insights
[What student should have learned]
```

---

## 6. **DELIVERABLES**

### Nível 1:
- [ ] 2 exercises (1 hour total)
- [ ] Full solutions with explanations
- [ ] Difficulty: Beginner

### Nível 2:
- [ ] 3 exercises (3 hours total)
- [ ] Full solutions with explanations
- [ ] Difficulty: Intermediate
- [ ] Can be done independently or in groups

### Nível 3:
- [ ] 3 exercises (4 hours total)
- [ ] Full solutions with explanations
- [ ] Difficulty: Advanced
- [ ] Recommended in small groups

### Nível 4:
- [ ] 2 real-world exercises (4 hours total)
- [ ] Full solutions with detailed analysis
- [ ] Difficulty: Expert
- [ ] Based on real KODA scenarios

**Total: 12 exercises with solutions**

---

## Tone & Style:
- Practical and grounded (based on real KODA problems)
- Clear problem statements (no ambiguity)
- Progressive difficulty within each level
- Solutions are thorough (teach through examples)
- Include "Key Insights" section in each solution

**File Organization:**
```
01-nivel-1-fundamentals/exercises/
├── exercise-01.md
├── exercise-02.md
└── solutions/
    ├── exercise-01-solution.md
    └── exercise-02-solution.md

02-nivel-2-practical-patterns/exercises/
├── exercise-01.md
├── exercise-02.md
├── exercise-03.md
└── solutions/
    ├── exercise-01-solution.md
    ├── exercise-02-solution.md
    └── exercise-03-solution.md

[And so on for Nível 3-4...]
```

Generate all exercises with complete solutions.
```

---

## 📌 Notas de Uso

1. **Gere em etapas:**
   - Nível 1: 2 exercícios (20-30 min)
   - Nível 2: 3 exercícios (30-40 min)
   - Nível 3: 3 exercícios (40-50 min)
   - Nível 4: 2 exercícios (30-40 min)
   - Total: ~2 horas

2. **Inclua:**
   - Problem statement claro
   - Tarefas específicas
   - Hints úteis
   - Soluções detalhadas
   - Key insights

3. **Teste:** 
   - Cada exercício leva tempo estimado?
   - Solução é completa?
   - Insights são valiosos?

4. **Salve em:** `{nivel}-exercises/` e `{nivel}-exercises/solutions/`

---

*Prompt | Exercícios | v1.0*
