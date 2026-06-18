---
title: "Prompt: Creating a Comprehensive Course on Long-Running Agents"
type: prompt
date: 2026-05-26
tags:
  - curriculo-conteudo
aliases:
  - curso completo prompt
  - comprehensive course
  - geracao de curriculo
relates-to:
  - "[[prompts/PROMPTS-00-INDEX|Prompt Index]]"
  - "[[curriculum/MASTER_PLAN|Curriculum Master Plan]]"
  - "[[curriculum/README|Curriculum README]]"
---

# 📝 PROMPT: Creating a Comprehensive Course on Long-Running Agents

## Como Usar Este Prompt

Cole este prompt completo em um LLM (Claude, GPT-4, etc) junto com o PDF da apresentação Anthropic para gerar o currículo completo dos 4 níveis.

---

## PROMPT COMPLETO

```
You are an experienced technical trainer, course architect, and knowledge management specialist. Your task is to create a structured, comprehensive course based on the provided PDF about building agents that run for extended periods (Anthropic's "Build Agents That Run for Hours" presentation).

**Course Context:**
- Audience: Technical team at FutanBear working on multi-agent systems
- Primary Use Case: KODA (conversational AI agent for sports supplement sales via WhatsApp with catalog access, fulfillment integration, and same-day delivery)
- Level: Intermediate to Advanced (team has experience with system architecture and strategic implementation)
- Delivery Format: Modular, with hands-on examples tied to KODA's architecture
- Language: Portuguese (course materials) / Code examples in English

**CORE REQUIREMENTS:**

1. **Course Structure** (provide a detailed outline):
   - Define 6-8 modules with clear learning objectives
   - Include prerequisite knowledge for each module
   - Estimate time for each section
   - Specify which concepts apply directly to KODA
   - Map each module to the Progressão de Complexidade levels (see below)

2. **For Each Module, Provide:**
   - **Core Concepts**: Break down technical concepts with visual metaphors
   - **Why It Matters**: Connect to KODA's specific challenges (handling long conversations, maintaining context through multi-step order processes, managing fulfillment workflows)
   - **Key Takeaways**: 3-5 actionable insights
   - **KODA Example**: Concrete scenario showing how this module applies (e.g., how KODA maintains conversation coherence while processing a customer's order, checking inventory, applying promotions, and scheduling same-day delivery)
   - **Complexity Level**: Indicate which level(s) this concept belongs to (see Progressão de Complexidade)

3. **Deep Dives** (for critical sections):
   - "Three Reasons Agents Lose the Plot": Expand with KODA-specific failure modes
   - Generator/Evaluator Pattern: Show how KODA could use this for verifying customer orders before fulfillment
   - Sprint Contracts: How KODA's fulfillment workflow could define testable contracts
   - Harness Design Evolution: How KODA's harness should evolve as capabilities improve

4. **Knowledge Management System Design** (with Knowledge Graph):
   - Structure for capturing lessons learned
   - Documentation artifacts to track as KODA evolves
   - Pattern library for common agent challenges
   - Decision log template for architectural choices
   - **Knowledge Graph Format** (see requirements below)

5. **Lab Exercises** (hands-on, KODA-focused):
   - Create a simple evaluator for KODA's product recommendation quality
   - Design a sprint contract for KODA's order fulfillment feature
   - Implement context management for a 4-hour customer conversation
   - Debug an agent trace from a hypothetical KODA failure
   - Each exercise should be tagged with the Complexity Level it addresses

6. **Practical Implementation Guide**:
   - Step-by-step: How to apply generator/evaluator to KODA's next feature
   - Rubric design for evaluating KODA's design quality and originality
   - Tracing strategy for KODA's agent loops
   - Harness simplification checklist as Claude models improve
   - Implementation roadmap showing progression through complexity levels

7. **Common Pitfalls & Solutions**:
   - Map each of the three "reasons agents lose the plot" to KODA scenarios
   - Self-evaluation trap: Why KODA can't grade its own order accuracy
   - Context anxiety: How it manifests in multi-turn customer conversations
   - Solutions specific to KODA's architecture
   - Include which complexity level addresses each pitfall

8. **Building a KODA-Specific Harness** (synthesis):
   - Reference architecture: 3-agent model for KODA (Planner, Generator, Evaluator)
   - How these agents coordinate for product discovery, order management, and fulfillment
   - File-based state management for persistence
   - Rubrics for evaluating KODA's outputs (product recommendations, order accuracy, user experience)

---

## ADVANCED REQUIREMENT 1: KNOWLEDGE GRAPH FORMAT

For each critical concept, provide a representation in graph format showing:

**Format for each concept:**
```
CONCEPT: [Name]
├── DEFINITION: [Clear, concise explanation]
├── CONNECTS TO:
│   ├── [Related Concept 1] (how it relates)
│   ├── [Related Concept 2] (how it relates)
│   └── [Related Concept 3] (how it relates)
├── DEPENDENCIES:
│   ├── Must understand: [Prerequisite 1]
│   └── Must understand: [Prerequisite 2]
├── KODA APPLICATION:
│   ├── Feature/Workflow: [Which KODA feature uses this]
│   ├── Challenge it solves: [Specific KODA problem]
│   └── Implementation priority: [High/Medium/Low based on KODA roadmap]
├── IMPLEMENTATION CHECKLIST:
│   ├── [ ] Understand concept
│   ├── [ ] Review KODA-specific scenario
│   ├── [ ] Complete lab exercise
│   └── [ ] Document in team knowledge base
└── NEXT STEPS: [What to learn next to build on this concept]
```

**Create Knowledge Graphs for:**
- Context Management & Token Budgeting
- Planning vs. Execution separation
- Generator/Evaluator Pattern
- Sprint Contracts & Negotiation
- State Persistence & File-Based Coordination
- Harness Evolution (as models improve)
- Multi-Agent Coordination
- Evaluation Rubrics & Subjective Quality Measurement

---

## ADVANCED REQUIREMENT 2: PROGRESSÃO DE COMPLEXIDADE (Learning Progression)

Structure all course content across **4 levels**, with clear advancement criteria:

### **NÍVEL 1: Conceitos Fundamentais (Foundation)**
**Goals:** Understand why long-running agents fail and the basic building blocks

**Topics:**
- Why agents lose the plot (Context, Planning, Verification)
- Token budgeting and context windows
- Basic harness patterns
- Introduction to generator/evaluator concept

**KODA Application:**
- Maintaining conversation context in customer chats
- Preventing context anxiety in multi-turn interactions
- Basics of order processing workflows

**Completion Criteria:**
- [ ] Understand the three failure modes
- [ ] Can explain context window management
- [ ] Can identify a harness pattern in existing code
- [ ] Can write basic evaluation criteria

**Time:** 3-4 hours
**Prerequisite:** Basic understanding of LLMs and prompt engineering

---

### **NÍVEL 2: Padrões Práticos (Practical Patterns)**
**Goals:** Learn patterns that immediately improve agent reliability; apply to KODA

**Topics:**
- Generator/Evaluator pattern in depth
- Sprint contracts and negotiation between agents
- Rubric design for grading subjective outputs
- Context reset strategies vs. continuous context
- Debugging traces and identifying agent divergence

**KODA Application:**
- Generator/Evaluator for product recommendations vs. inventory checks
- Sprint contracts for order fulfillment steps
- Rubrics for evaluating KODA's response quality and originality
- Managing conversation state across multiple fulfillment stages

**Completion Criteria:**
- [ ] Can design a generator/evaluator pair for a feature
- [ ] Can write sprint contracts with specific, testable criteria
- [ ] Can create a rubric for evaluating outputs
- [ ] Can read and interpret agent traces
- [ ] Can complete all Nível 2 lab exercises

**Time:** 6-8 hours
**Prerequisite:** Completion of Nível 1

**Lab Exercises:**
- Design an evaluator rubric for KODA's product recommendations
- Create a sprint contract for the "check inventory & apply promotions" feature
- Debug a simulated KODA trace to identify where judgment diverged from expected behavior

---

### **NÍVEL 3: Arquitetura Avançada (Advanced Architecture)**
**Goals:** Design sophisticated multi-agent systems; understand state management and coordination

**Topics:**
- Multi-agent coordination patterns (Planner, Generator, Evaluator)
- File-based state management for long-running workflows
- Server-side compaction and context preservation
- Selective context disclosure (skills, progressive loading)
- Programmatic tool calling and structured outputs
- Agent teams and sub-agent delegation
- Harness evolution as models improve (knowing what to remove)

**KODA Application:**
- KODA's 3-agent architecture for customer journeys
- Persisting order state across hours-long conversations
- Coordinating between product discovery, order processing, and fulfillment agents
- Progressive disclosure of catalog information based on context
- How to simplify KODA's harness as Claude models improve

**Completion Criteria:**
- [ ] Can design a 3+ agent system from scratch
- [ ] Can implement file-based state coordination
- [ ] Understand when to use server-side compaction vs. context reset
- [ ] Can design agent teams with proper delegation
- [ ] Can identify harness components that can be removed as models improve
- [ ] Can complete all Nível 3 lab exercises

**Time:** 8-10 hours
**Prerequisite:** Completion of Nível 2

**Lab Exercises:**
- Design KODA's full 3-agent harness from a simple prompt
- Implement a state persistence layer for a customer order journey
- Create an agent team for product discovery, order management, and fulfillment
- Simulate harness evolution: remove components as model capabilities increase

---

### **NÍVEL 4: KODA-Específico (Production Application)**
**Goals:** Apply all concepts to KODA's actual architecture and roadmap; become expert in KODA's system

**Topics:**
- KODA's current harness design and rationale
- Identifying next improvements based on presentation patterns
- Building new features using generator/evaluator methodology
- Handling KODA-specific challenges:
  - Multi-turn order conversations (product discovery → selection → checkout → fulfillment)
  - Same-day delivery workflow coordination
  - Club pricing evaluation and recommendation
  - Inventory real-time updates during conversations
  - Payment and fulfillment confirmations
- Evaluating KODA's design quality (UI coherence, originality, user experience)
- Reading and interpreting KODA's actual traces
- Roadmap planning: what to build, when to simplify, how to evolve harness

**KODA Application:**
- This entire level is KODA-specific

**Completion Criteria:**
- [ ] Can diagnose issues in KODA's agent traces
- [ ] Can propose harness improvements with supporting data
- [ ] Can implement a new feature using appropriate patterns
- [ ] Can create and refine evaluator rubrics for KODA's outputs
- [ ] Can participate in architectural decision-making for KODA
- [ ] Can mentor others on KODA's harness design

**Time:** Ongoing (10+ hours, applies to real work)
**Prerequisite:** Completion of Nível 3

**Real-World Exercises:**
- Analyze a real KODA trace and identify optimization opportunities
- Design the harness for KODA's next major feature (e.g., inventory sync)
- Create comprehensive evaluation rubrics for a KODA feature rollout
- Lead a harness review and propose simplifications for the next Claude model release

---

**Progression Rules:**
- Each level builds on previous understanding
- Team members should progress at their own pace
- Nível 3 & 4 work can happen in parallel (advanced members move to Nível 4 while others complete Nível 2)
- Re-assessment when new Claude models release (may enable earlier progression)

---

## Tone & Style:
- Empathetic and practical (acknowledge implementation challenges)
- Blend of theoretical depth and pragmatic guidance
- Emphasize how mastering these patterns enables KODA's evolution
- Highlight the journey: from simple agents to sophisticated multi-agent systems
- Use analogies to development practices they know (Git workflows, CI/CD, sprint planning)

## Deliverables:

1. **Complete course curriculum** (outline + module summaries mapped to all 4 complexity levels)
2. **Full module content** (3-5 of the most critical modules, with depth)
3. **Knowledge Graph representations** for 8+ core concepts (showing connections, dependencies, and KODA applications)
4. **Learning Progression Roadmap** showing:
   - Timeline for completing each level
   - Prerequisites clearly marked
   - Branching paths for different team roles
   - How progression relates to KODA's roadmap
5. **3-5 KODA-specific case studies** with complexity level tagging
6. **Lab Exercise Suite** (all 4 levels, with solutions)
7. **Glossary of key terms** (with Knowledge Graph integration)
8. **Quick reference guide** for harness design decisions
9. **Implementation checklist** for each major concept
10. **Team Progression Tracker Template** (for monitoring who's at which level)

**Start with:**
1. Course structure and outline (mapping to all 4 complexity levels)
2. Full Knowledge Graphs for the 3 most critical concepts
3. Nível 1 complete content + Nível 2 intro
4. Then develop higher levels based on feedback

Prioritize content that directly informs KODA's next architectural evolution while ensuring foundational understanding is solid before advancing to complex patterns.
```

---

## 📌 Notas de Uso

1. **Cole o prompt inteiro** em um LLM (Claude, GPT-4, etc)
2. **Inclua o PDF** da apresentação Anthropic como contexto
3. **Solicitações sequenciais:**
   - Primeira: Estrutura curricular completa
   - Depois: Cada módulo em detalhes
   - Depois: Knowledge Graphs
   - Depois: Exercícios

4. **Tempo estimado:**
   - Estrutura: 5-10 minutos
   - Conteúdo Nível 1: 15-20 minutos
   - Conteúdo Nível 2: 20-30 minutos
   - Todos os níveis: 1-2 horas total

5. **Salve outputs** em sua pasta `04-nivel-X-*/` correspondente

---

*Prompt | Curso Completo | v1.0*
