---
title: "📑 ÍNDICE EXECUTIVO: Navegação Rápida"
type: curriculum-index
aliases: ["índice currículo", "navegação", "mapa currículo"]
tags: [curriculo-conteudo]
relates-to: ["[[docs/system-of-record|System of Record]]", "[[curriculum/MASTER_PLAN|Master Plan]]", "[[curriculum/QUICK_START|Quick Start]]", "[[curriculum/GLOSSARY|Glossary]]"]
last_updated: 2026-06-11
---
# 📑 ÍNDICE EXECUTIVO: Navegação Rápida

**Para quando você precisa achar algo rapidinho.**

---

## 🎯 Comece Pelo Seu Caso

### ❓ "Sou novo, não entendo nada"
```
[[curriculum/QUICK_START|QUICK_START.md]] (15 min)
    ↓
[[curriculum/01-nivel-1-fundamentals/01-why-agents-lose-plot|01-nivel-1-fundamentals/01-why-agents-lose-plot.md]]
    ↓
[[curriculum/01-nivel-1-fundamentals/exercises|01-nivel-1-fundamentals/exercises/]]
```

**Tempo estimado:** 4-5 horas, semana 1-2

---

### 💼 "Conheço LLMs, quero padrões práticos"
```
[[curriculum/02-nivel-2-practical-patterns/01-generator-evaluator-pattern|02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md]]
    ↓
[[curriculum/02-nivel-2-practical-patterns/02-sprint-contracts|02-nivel-2-practical-patterns/02-sprint-contracts.md]]
    ↓
[[curriculum/02-nivel-2-practical-patterns/exercises|02-nivel-2-practical-patterns/exercises/]]
```

**Tempo estimado:** 8-10 horas, semanas 2-3

---

### 🏗️ "Sou architect, preciso de sistema completo"
```
[[curriculum/03-nivel-3-advanced-architecture/01-multi-agent-systems|03-nivel-3-advanced-architecture/01-multi-agent-systems.md]]
    ↓
[[curriculum/03-nivel-3-advanced-architecture/02-state-persistence|03-nivel-3-advanced-architecture/02-state-persistence.md]]
    ↓
[[curriculum/03-nivel-3-advanced-architecture/exercises|03-nivel-3-advanced-architecture/exercises/]]
```

**Tempo estimado:** 10-12 horas, semanas 3-4

---

### 🎯 "Trabalho em KODA, preciso aplicar tudo"
```
[[curriculum/04-nivel-4-koda-specific/01-koda-architecture|04-nivel-4-koda-specific/01-koda-architecture.md]]
    ↓
[[curriculum/04-nivel-4-koda-specific/case-studies|04-nivel-4-koda-specific/case-studies/]]
    ↓
[[curriculum/04-nivel-4-koda-specific/real-world-exercises|04-nivel-4-koda-specific/real-world-exercises/]]
```

**Tempo estimado:** Contínuo, semanas 5-12

---

### 🔍 "Preciso de resposta rápida"
```
[[curriculum/GLOSSARY|GLOSSARY.md]]  (definições)
    ↓
[[curriculum/FAQ|FAQ.md]]       (perguntas comuns)
    ↓
[[curriculum/06-knowledge-graphs|06-knowledge-graphs/]] (diagramas)
```

**Tempo estimado:** Lookup instantâneo

---

## 📚 Estrutura por Tipo de Conteúdo

### 🎓 Quer Aprender um Conceito?

| Conceito | Arquivo Conceito | Arquivo Nível | Case Study | KG |
|----------|-----------------|---------------|-----------|-----|
| Context Management | `05-core-concepts/01-*.md` | Nível 1 | Ver KODA app | Sim |
| Planning vs. Exec | `05-core-concepts/02-*.md` | Nível 2 | Ver KODA app | Sim |
| Generator/Evaluator | `05-core-concepts/03-*.md` | Nível 2 | Retro Game | Sim |
| Sprint Contracts | `05-core-concepts/04-*.md` | Nível 2 | Retro Game | Sim |
| State Persistence | `05-core-concepts/05-*.md` | Nível 3 | Browser DAW | Sim |
| Harness Evolution | `05-core-concepts/06-*.md` | Nível 3 | Timeline | Sim |
| Multi-Agent | `05-core-concepts/07-*.md` | Nível 3 | Architecture | Sim |
| Evaluation Rubrics | `05-core-concepts/08-*.md` | Nível 2 | Retro Game | Sim |

---

### 💻 Quer Fazer um Exercício?

**Nível 1 (Fundamentos)**
- `01-nivel-1-fundamentals/exercises/exercise-01.md`
- `01-nivel-1-fundamentals/exercises/exercise-02.md`

**Nível 2 (Padrões)**
- `02-nivel-2-practical-patterns/exercises/exercise-01.md` (Generator/Evaluator)
- `02-nivel-2-practical-patterns/exercises/exercise-02.md` (Sprint Contracts)
- `02-nivel-2-practical-patterns/exercises/exercise-03.md` (Rubric Design)
- `02-nivel-2-practical-patterns/exercises/exercise-04-error-context-hygiene.md` (Error Context Hygiene)

**Nível 3 (Arquitetura)**
- `03-nivel-3-advanced-architecture/exercises/exercise-01.md` (Multi-Agent Design)
- `03-nivel-3-advanced-architecture/exercises/exercise-02.md` (State Persistence)
- `03-nivel-3-advanced-architecture/exercises/exercise-03.md` (Harness Evolution)
- `03-nivel-3-advanced-architecture/exercises/exercise-04-llm-as-fuzzy-compiler.md` (LLM as Fuzzy Compiler)
- `03-nivel-3-advanced-architecture/exercises/exercise-05-persona-based-documentation.md` (Persona-Based Documentation)
- `03-nivel-arquiteto/exercises/exercise-04-owner-of-no-role.md` (Owner of No Role)

**Nível 4 (KODA)**
- `04-nivel-4-koda-specific/real-world-exercises/exercise-01.md`
- `04-nivel-4-koda-specific/real-world-exercises/exercise-02.md`
- `04-nivel-4-koda-specific/real-world-exercises/exercise-05-manual-brake-question-gate.md` (Manual Brake Question Gate)
- `04-nivel-4-koda-specific/real-world-exercises/exercise-06-deferred-ledger-agentic-work.md` (Deferred Ledger Agentic Work)

**Soluções:** Em `exercises/solutions/` em cada nível

---

### 🎬 Quer um Caso de Estudo?

| Caso | Arquivo | Nível | Foco |
|------|---------|-------|------|
| Retro Game Maker | `09-case-studies/retro-game-maker.md` | 2-3 | Generator/Evaluator |
| Browser DAW | `09-case-studies/browser-daw-app.md` | 3-4 | Multi-agent + State |
| KODA - Discovery | `09-case-studies/koda-product-discovery.md` | 4 | Product Finding |
| KODA - Orders | `09-case-studies/koda-order-processing.md` | 4 | Order Processing |
| KODA - Fulfillment | `09-case-studies/koda-fulfillment-workflow.md` | 4 | Delivery Workflow |

---

### 📊 Quer um Knowledge Graph?

| Tipo | Arquivo |
|------|---------|
| Ecosystem completo | `06-knowledge-graphs/01-concept-ecosystem.md` |
| Features vs Conceitos | `06-knowledge-graphs/02-koda-feature-dependencies.md` |
| Progressão de aprendizado | `06-knowledge-graphs/03-learning-progression.md` |
| Problem → Solution | `06-knowledge-graphs/04-problem-solution-mapping.md` |
| Conceito específico | `06-knowledge-graphs/detailed-graphs/XX-*.md` |

---

### 🛠️ Quer um Template ou Checklist?

| Recurso | Arquivo | Uso |
|---------|---------|-----|
| Sprint Contract | `08-tools-templates/sprint-contract-template.md` | Definir contratos |
| Evaluation Rubric | `08-tools-templates/evaluation-rubric-template.md` | Grading criteria |
| Knowledge Graph | `08-tools-templates/knowledge-graph-template.md` | Criar novo KG |
| Architecture Decision | `08-tools-templates/architecture-decision-record-template.md` | Documentar decisões |
| Progress Tracker | `08-tools-templates/team-progress-tracker.md` | Rastrear equipe |
| Learning Rubric | `08-tools-templates/learning-assessment-rubric.md` | Avaliar aprendizado |

---

### 📋 Quer um Guia de Implementação?

| Guia | Arquivo | Para Quem |
|------|---------|----------|
| Setup inicial | `07-implementation-guides/01-setup-guide.md` | Líderes |
| Progressão da equipe | `07-implementation-guides/02-team-progression-guide.md` | Líderes |
| Design de Harness | `07-implementation-guides/03-harness-design-checklist.md` | Arquitetos |
| Rubrics para KODA | `07-implementation-guides/04-evaluation-rubric-template.md` | Todos |
| Análise de Traces | `07-implementation-guides/05-trace-analysis-guide.md` | Debuggers |
| Harness Evolution | `07-implementation-guides/06-harness-evolution-playbook.md` | Líderes |

---

## 🗺️ Navegação por Pergunta

### "Por que agentes falham?"
→ `01-nivel-1-fundamentals/01-why-agents-lose-plot.md`

### "Como mantenho contexto?"
→ `01-nivel-1-fundamentals/02-token-budgeting.md`
→ `05-core-concepts/01-context-management.md`

### "Como separo geração de avaliação?"
→ `02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md`
→ `05-core-concepts/03-generator-evaluator-pattern.md`

### "Como defino 'pronto'?"
→ `02-nivel-2-practical-patterns/02-sprint-contracts.md`
→ `05-core-concepts/04-sprint-contracts.md`

### "Como avalio qualidade?"
→ `02-nivel-2-practical-patterns/03-rubric-design.md`
→ `05-core-concepts/08-evaluation-rubrics.md`
→ `../docs/canonical/pain-signal-eval-progression-gate.md`
→ `../docs/canonical/eval-tier-stratification.md`
→ `../docs/canonical/pr-gated-eval-enforcement.md`
→ `../docs/canonical/production-grounded-eval-sampling.md`
→ `../docs/canonical/production-failure-regression-flywheel.md`
→ `../docs/canonical/eval-to-production-correlation-tracking.md`

### "Como evoluo a maturidade dos meus evals?"
→ `../docs/canonical/pain-signal-eval-progression-gate.md`
→ `../docs/canonical/repeatable-agent-spot-check-set.md`
→ `../docs/canonical/eval-tier-stratification.md`
→ `../docs/canonical/pr-gated-eval-enforcement.md`
→ `../docs/canonical/production-grounded-eval-sampling.md`
→ `../docs/canonical/production-failure-regression-flywheel.md`
→ `../docs/canonical/eval-to-production-correlation-tracking.md`

### "Como debugo agent behavior?"
→ `02-nivel-2-practical-patterns/04-trace-reading.md`
→ `07-implementation-guides/05-trace-analysis-guide.md`

### "Como coordeno múltiplos agentes?"
→ `03-nivel-3-advanced-architecture/01-multi-agent-systems.md`
→ `05-core-concepts/07-multi-agent-coordination.md`

### "Como persisto estado?"
→ `03-nivel-3-advanced-architecture/02-state-persistence.md`
→ `05-core-concepts/05-state-persistence.md`

### "Como removo scaffolding?"
→ `03-nivel-3-advanced-architecture/05-harness-evolution.md`
→ `05-core-concepts/06-harness-evolution.md`

### "Como isso se aplica ao KODA?"
→ `04-nivel-4-koda-specific/XX-*.md`
→ `09-case-studies/koda-*.md`

---

## 📱 Para Diferentes Tipos de Pessoas

### Developer
1. `02-nivel-2-practical-patterns/` (padrões)
2. `08-tools-templates/` (templates)
3. `09-case-studies/` (exemplos)

### Architect
1. `03-nivel-3-advanced-architecture/` (design)
2. `05-core-concepts/` (profundidade)
3. `06-knowledge-graphs/` (visualização)

### Manager/Leader
1. `EXECUTION_PLAN.md` (cronograma)
2. `08-tools-templates/team-progress-tracker.md` (rastreamento)
3. `07-implementation-guides/` (guias)

### QA/Tester
1. `02-nivel-2-practical-patterns/04-trace-reading.md` (debugging)
2. `05-core-concepts/08-evaluation-rubrics.md` (avaliação)
3. `07-implementation-guides/05-trace-analysis-guide.md` (análise)

### Product Manager
1. `04-nivel-4-koda-specific/02-customer-journey-flows.md` (flows)
2. `04-nivel-4-koda-specific/03-feature-design-patterns.md` (patterns)
3. `09-case-studies/` (exemplos)

---

## 🔄 Fluxo de Aprendizado Recomendado

### Primeira Vez?
```
[[curriculum/README|README.md]] (5 min)
    ↓
[[curriculum/QUICK_START|QUICK_START.md]] (15 min)
    ↓
[[curriculum/MASTER_PLAN|MASTER_PLAN.md]] (30 min)
    ↓
Começar Nível apropriado
```

### Quer aprender um conceito específico?
```
Procura em [[curriculum/05-core-concepts|05-core-concepts/]]
    ↓
Leia explicação profunda
    ↓
Veja Knowledge Graphs em [[curriculum/06-knowledge-graphs|06-knowledge-graphs/]]
    ↓
Faça exercício relacionado
    ↓
Veja case study
```

### Quer implementar algo?
```
Procura padrão em [[curriculum/02-3-nivel-X|02-3-nivel-X/]]
    ↓
Leia seção "Como aplicar"
    ↓
Use template em [[curriculum/08-tools-templates|08-tools-templates/]]
    ↓
Veja exemplo em [[curriculum/09-case-studies|09-case-studies/]]
    ↓
Implementa em seu código
    ↓
Use guia em [[curriculum/07-implementation-guides|07-implementation-guides/]]
```

---

## 📊 Por Tempo Disponível

### Tenho 30 minutos
- [ ] Leia este índice
- [ ] Abra QUICK_START.md
- [ ] Escolha seu caminho

---

### Tenho 1-2 horas
- [ ] QUICK_START.md (15 min)
- [ ] Primeira leitura do seu nível (45 min)
- [ ] Discussão/Q&A (15 min)

---

### Tenho 4-5 horas
- [ ] Toda Nível 1 (Semana 1)
- [ ] Exercícios
- [ ] Aplicação KODA

---

### Tenho 6-8 horas
- [ ] Toda Nível 2 (Semana 2)
- [ ] Exercícios
- [ ] Aplicação KODA

---

### Tenho 10+ horas
- [ ] Toda Nível 3 (Semana 3-4)
- [ ] Exercícios
- [ ] Começar Nível 4

---

## 🔗 Índice por Arquivo

### 📄 Documentos Mestres
- `README.md` - Este arquivo principal
- `MASTER_PLAN.md` - Índice geral e estrutura
- `QUICK_START.md` - Começar em 45 minutos
- `GLOSSARY.md` - Referência de termos
- `EXECUTION_PLAN.md` - Cronograma 12 semanas
- `FAQ.md` - Perguntas frequentes (em construção)

### 📚 Conteúdo Nível 1
- `01-nivel-1-fundamentals/01-why-agents-lose-plot.md`
- `01-nivel-1-fundamentals/02-token-budgeting.md`
- `01-nivel-1-fundamentals/03-basic-harness-patterns.md`
- `01-nivel-1-fundamentals/exercises/`
- `01-nivel-1-fundamentals/koda-applications/nivel-1-koda.md`

### 📚 Conteúdo Nível 2
- `02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md`
- `02-nivel-2-practical-patterns/02-sprint-contracts.md`
- `02-nivel-2-practical-patterns/03-rubric-design.md`
- `02-nivel-2-practical-patterns/04-trace-reading.md`
- `02-nivel-2-practical-patterns/exercises/`
- `02-nivel-2-practical-patterns/koda-applications/nivel-2-koda.md`

### 📚 Conteúdo Nível 3
- `03-nivel-3-advanced-architecture/01-multi-agent-systems.md`
- `03-nivel-3-advanced-architecture/02-state-persistence.md`
- `03-nivel-3-advanced-architecture/03-file-based-coordination.md`
- `03-nivel-3-advanced-architecture/04-server-side-compaction.md`
- `03-nivel-3-advanced-architecture/05-harness-evolution.md`
- `03-nivel-3-advanced-architecture/exercises/`
- `03-nivel-3-advanced-architecture/koda-applications/nivel-3-koda.md`

### 📚 Conteúdo Nível 4
- `04-nivel-4-koda-specific/01-koda-architecture.md`
- `04-nivel-4-koda-specific/02-customer-journey-flows.md`
- `04-nivel-4-koda-specific/03-feature-design-patterns.md`
- `04-nivel-4-koda-specific/04-evaluation-rubrics-koda.md`
- `04-nivel-4-koda-specific/05-harness-improvements.md`
- `04-nivel-4-koda-specific/real-world-exercises/`
- `04-nivel-4-koda-specific/case-studies/`

### 🧠 Conceitos Core
- `05-core-concepts/01-context-management.md`
- `05-core-concepts/02-planning-execution-separation.md`
- `05-core-concepts/03-generator-evaluator-pattern.md`
- `05-core-concepts/04-sprint-contracts.md`
- `05-core-concepts/05-state-persistence.md`
- `05-core-concepts/06-harness-evolution.md`
- `05-core-concepts/07-multi-agent-coordination.md`
- `05-core-concepts/08-evaluation-rubrics.md`

### 📊 Knowledge Graphs
- `06-knowledge-graphs/01-concept-ecosystem.md`
- `06-knowledge-graphs/02-koda-feature-dependencies.md`
- `06-knowledge-graphs/03-learning-progression.md`
- `06-knowledge-graphs/04-problem-solution-mapping.md`
- `06-knowledge-graphs/detailed-graphs/` (8 arquivos de conceitos)

### 🛠️ Guias e Templates
- `07-implementation-guides/` (6 arquivos)
- `08-tools-templates/` (6 templates)

### 📖 Casos de Estudo
- `09-case-studies/retro-game-maker.md`
- `09-case-studies/browser-daw-app.md`
- `09-case-studies/koda-product-discovery.md`
- `09-case-studies/koda-order-processing.md`
- `09-case-studies/koda-fulfillment-workflow.md`

### 📚 Referências
- `10-references/anthropic-presentation-summary.md`
- `10-references/model-capability-timeline.md`
- `10-references/additional-resources.md`

---

## 🎯 TL;DR (Muito Longo; Não Li)

**Para começar em 5 minutos:**
1. Você é novo? → `QUICK_START.md`
2. Quer cronograma? → `EXECUTION_PLAN.md`
3. Precisa de termo? → `GLOSSARY.md`
4. Quer overview? → `MASTER_PLAN.md`

**Depois:**
→ Escolha seu nível em `01-nivel-X-*/`

**Sempre que tiver dúvida:**
→ Procure em `GLOSSARY.md` ou `FAQ.md`

---

## ✨ Dicas de Ouro para Navegação

1. **Use Ctrl+F (Cmd+F) em seus documentos** para procurar palavras-chave
2. **Leia os "Ver também" links** em GLOSSARY.md para contexto relacionado
3. **Comece pelos Knowledge Graphs** se é aprendiz visual
4. **Faça os exercícios** mesmo que pareça óbvio
5. **Revise case studies** para ver conceitos em ação real

---

## 🚀 Próximo Passo

**Qual é seu caso?** Clique em um acima:
- ❓ "Sou novo" → QUICK_START.md
- 💼 "Conheço padrões" → Nível 2
- 🏗️ "Sou architect" → Nível 3
- 🎯 "Trabalho em KODA" → Nível 4
- 🔍 "Preciso de referência" → GLOSSARY.md

---

*Índice Executivo | Navegação Rápida | v1.0*
