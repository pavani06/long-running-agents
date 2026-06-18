---
title: "Plano Mestre: Curso de Long-Running Agents para KODA"
type: source
date: 2026-05-26
tags:
  - curriculo-conteudo
  - index
aliases:
  - master plan
  - plano mestre
  - curso KODA
relates-to:
  - "[[rawfiles/README|README]]"
  - "[[rawfiles/INDEX|Index]]"
  - "[[curriculum/MASTER_PLAN|Curriculum Master Plan]]"
---

# 📚 PLANO MESTRE: Curso de Long-Running Agents para KODA

**Data de Criação:** Maio 2026  
**Versão:** 1.0  
**Status:** 🟢 Ativo  
**Proprietário:** FutanBear Technical Team  

---

## 📋 Índice Executivo

Este documento serve como **mapa mestre** para o curso completo sobre construção de agentes que rodham por horas. Ele organiza:

- ✅ Estrutura curricular completa (Nível 1-4)
- ✅ 8 conceitos fundamentais com Knowledge Graphs
- ✅ Exercícios práticos e casos de estudo KODA
- ✅ Roadmap de implementação
- ✅ Rastreamento de progresso da equipe
- ✅ Integração com arquitetura do KODA

---

## 🎯 Objetivos do Programa

### Curto Prazo (4 semanas)
- [ ] Equipe completa entende "3 razões por que agentes perdem o foco"
- [ ] Todos completam Nível 1 (Conceitos Fundamentais)
- [ ] Identifica 2-3 melhorias imediatas para KODA

### Médio Prazo (8 semanas)
- [ ] Equipe completa em Nível 2 (Padrões Práticos)
- [ ] Implementa generator/evaluator para 1 feature do KODA
- [ ] Cria rubrics de avaliação para recomendações de produtos

### Longo Prazo (12 semanas)
- [ ] Equipe avançada em Nível 3 (Arquitetura Avançada)
- [ ] Redesenha harness do KODA com base em padrões
- [ ] Implementa multi-agent system para customer journey completo

---

## 📁 Estrutura de Diretórios

```
koda-long-running-agents/
│
├── 00-master-documents/
│   ├── MASTER_PLAN.md (este arquivo)
│   ├── QUICK_START.md
│   ├── GLOSSARY.md
│   └── FAQ.md
│
├── 01-nivel-1-fundamentals/
│   ├── 01-why-agents-lose-plot.md
│   ├── 02-token-budgeting.md
│   ├── 03-basic-harness-patterns.md
│   ├── exercises/
│   │   ├── exercise-01.md
│   │   ├── exercise-02.md
│   │   └── solutions/
│   └── koda-applications/
│       └── nivel-1-koda.md
│
├── 02-nivel-2-practical-patterns/
│   ├── 01-generator-evaluator-pattern.md
│   ├── 02-sprint-contracts.md
│   ├── 03-rubric-design.md
│   ├── 04-trace-reading.md
│   ├── exercises/
│   │   ├── exercise-01.md
│   │   ├── exercise-02.md
│   │   ├── exercise-03.md
│   │   └── solutions/
│   └── koda-applications/
│       └── nivel-2-koda.md
│
├── 03-nivel-3-advanced-architecture/
│   ├── 01-multi-agent-systems.md
│   ├── 02-state-persistence.md
│   ├── 03-file-based-coordination.md
│   ├── 04-server-side-compaction.md
│   ├── 05-harness-evolution.md
│   ├── exercises/
│   │   ├── exercise-01.md
│   │   ├── exercise-02.md
│   │   ├── exercise-03.md
│   │   └── solutions/
│   └── koda-applications/
│       └── nivel-3-koda.md
│
├── 04-nivel-4-koda-specific/
│   ├── 01-koda-architecture.md
│   ├── 02-customer-journey-flows.md
│   ├── 03-feature-design-patterns.md
│   ├── 04-evaluation-rubrics-koda.md
│   ├── 05-harness-improvements.md
│   ├── real-world-exercises/
│   │   ├── exercise-01.md
│   │   ├── exercise-02.md
│   │   └── solutions/
│   └── case-studies/
│       ├── case-study-01.md
│       ├── case-study-02.md
│       └── case-study-03.md
│
├── 05-core-concepts/
│   ├── 01-context-management.md
│   ├── 02-planning-execution-separation.md
│   ├── 03-generator-evaluator-pattern.md
│   ├── 04-sprint-contracts.md
│   ├── 05-state-persistence.md
│   ├── 06-harness-evolution.md
│   ├── 07-multi-agent-coordination.md
│   └── 08-evaluation-rubrics.md
│
├── 06-knowledge-graphs/
│   ├── 01-concept-ecosystem.md
│   ├── 02-koda-feature-dependencies.md
│   ├── 03-learning-progression.md
│   ├── 04-problem-solution-mapping.md
│   └── detailed-graphs/
│       ├── context-management-graphs.md
│       ├── generator-evaluator-graphs.md
│       └── [6 outros arquivos de conceitos]
│
├── 07-implementation-guides/
│   ├── 01-setup-guide.md
│   ├── 02-team-progression-guide.md
│   ├── 03-harness-design-checklist.md
│   ├── 04-evaluation-rubric-template.md
│   ├── 05-trace-analysis-guide.md
│   └── 06-harness-evolution-playbook.md
│
├── 08-tools-templates/
│   ├── team-progress-tracker.md
│   ├── learning-assessment-rubric.md
│   ├── knowledge-graph-template.md
│   ├── sprint-contract-template.md
│   ├── evaluation-rubric-template.md
│   └── architecture-decision-record-template.md
│
├── 09-case-studies/
│   ├── retro-game-maker.md
│   ├── browser-daw-app.md
│   ├── koda-product-discovery.md
│   ├── koda-order-processing.md
│   └── koda-fulfillment-workflow.md
│
└── 10-references/
    ├── anthropic-presentation.md
    ├── model-capability-timeline.md
    └── additional-resources.md
```

---

## 🎓 Estrutura Curricular

### Nível 1: Conceitos Fundamentais ⏱️ 3-4 horas
**Foco:** Por que agentes falham  
**Resultado:** Compreensão dos 3 problemas principais

| Tópico | Arquivo | Tempo | Status |
|--------|---------|-------|--------|
| Por que agentes perdem o foco | `01-why-agents-lose-plot.md` | 45 min | ⏳ |
| Token Budgeting | `02-token-budgeting.md` | 45 min | ⏳ |
| Padrões básicos de harness | `03-basic-harness-patterns.md` | 45 min | ⏳ |
| Exercícios Nível 1 | `exercises/` | 45 min | ⏳ |
| KODA Applications | `koda-applications/nivel-1-koda.md` | 30 min | ⏳ |

**Critérios de Conclusão:**
- [ ] Entendo os 3 motivos pelos quais agentes perdem o foco
- [ ] Posso explicar context windows e token budgeting
- [ ] Consigo identificar um padrão de harness em código existente
- [ ] Completei os 2 exercícios do Nível 1
- [ ] Consigo mapear conceitos para KODA

---

### Nível 2: Padrões Práticos ⏱️ 6-8 horas
**Foco:** Padrões que melhoram confiabilidade  
**Resultado:** Pode aplicar padrões ao KODA

| Tópico | Arquivo | Tempo | Status |
|--------|---------|-------|--------|
| Padrão Generator/Evaluator | `01-generator-evaluator-pattern.md` | 90 min | ⏳ |
| Sprint Contracts | `02-sprint-contracts.md` | 90 min | ⏳ |
| Rubric Design | `03-rubric-design.md` | 90 min | ⏳ |
| Trace Reading | `04-trace-reading.md` | 90 min | ⏳ |
| Exercícios Nível 2 | `exercises/` | 120 min | ⏳ |
| KODA Applications | `koda-applications/nivel-2-koda.md` | 60 min | ⏳ |

**Critérios de Conclusão:**
- [ ] Posso desenhar um pair generator/evaluator para uma feature
- [ ] Consigo escrever sprint contracts com critérios testáveis
- [ ] Posso criar uma rubric para avaliar outputs
- [ ] Consigo ler e interpretar agent traces
- [ ] Completei os 3 exercícios do Nível 2
- [ ] Consigo aplicar padrões ao KODA

---

### Nível 3: Arquitetura Avançada ⏱️ 8-10 horas
**Foco:** Sistemas multi-agentes sofisticados  
**Resultado:** Pode desenhar arquitetura avançada

| Tópico | Arquivo | Tempo | Status |
|--------|---------|-------|--------|
| Multi-Agent Systems | `01-multi-agent-systems.md` | 90 min | ⏳ |
| State Persistence | `02-state-persistence.md` | 90 min | ⏳ |
| File-Based Coordination | `03-file-based-coordination.md` | 90 min | ⏳ |
| Server-Side Compaction | `04-server-side-compaction.md` | 60 min | ⏳ |
| Harness Evolution | `05-harness-evolution.md` | 90 min | ⏳ |
| Exercícios Nível 3 | `exercises/` | 150 min | ⏳ |
| KODA Applications | `koda-applications/nivel-3-koda.md` | 60 min | ⏳ |

**Critérios de Conclusão:**
- [ ] Posso desenhar um sistema 3+ agentes do zero
- [ ] Implementei coordenação baseada em arquivo
- [ ] Entendo quando remover componentes de harness
- [ ] Completei os 3 exercícios do Nível 3
- [ ] Posso apoiar decisões arquiteturais do KODA

---

### Nível 4: KODA-Específico ⏱️ Contínuo (10+ horas)
**Foco:** Aplicação prática no KODA  
**Resultado:** Expert em harness do KODA

| Tópico | Arquivo | Tempo | Status |
|--------|---------|-------|--------|
| Arquitetura KODA | `01-koda-architecture.md` | 90 min | ⏳ |
| Customer Journey Flows | `02-customer-journey-flows.md` | 90 min | ⏳ |
| Feature Design Patterns | `03-feature-design-patterns.md` | 90 min | ⏳ |
| Rubrics para KODA | `04-evaluation-rubrics-koda.md` | 90 min | ⏳ |
| Melhorias de Harness | `05-harness-improvements.md` | 90 min | ⏳ |
| Exercícios Real-World | `real-world-exercises/` | 180 min | ⏳ |
| Case Studies | `case-studies/` | 120 min | ⏳ |

**Critérios de Conclusão:**
- [ ] Posso diagnosticar problemas em traces do KODA
- [ ] Propus melhorias com dados de suporte
- [ ] Implementei uma feature novo no KODA
- [ ] Criei rubrics completes para outputs do KODA
- [ ] Participo de decisões arquiteturais

---

## 📊 Roadmap de Execução

### Semana 1-2: Fundação (Nível 1)
```
MON   TUE   WED   THU   FRI
[ 1 ][ 1 ][ 1 ][ 1 ][ EX1]  <- Semana 1
[ 1 ][ 1 ][ 1 ][ EX2][ REV]  <- Semana 2
```

**Deliverables:**
- ✅ Todos entendem problema
- ✅ Todos fizeram exercícios Nível 1
- ✅ Documento de síntese criado

---

### Semana 3-4: Padrões Práticos (Nível 2)
```
MON   TUE   WED   THU   FRI
[ 2 ][ 2 ][ 2 ][ 2 ][ 2 ]  <- Semana 3
[ EX3][ EX4][ EX5][ PROJ][ REV]  <- Semana 4
```

**Deliverables:**
- ✅ Generator/Evaluator para 1 feature KODA
- ✅ Sprint contracts escritos
- ✅ Rubrics iniciais criadas

---

### Semana 5-6: Padrões Avançados (Nível 3)
```
MON   TUE   WED   THU   FRI
[ 3 ][ 3 ][ 3 ][ 3 ][ 3 ]  <- Semana 5
[ EX6][ EX7][ EX8][ PROJ][ REV]  <- Semana 6
```

**Deliverables:**
- ✅ Multi-agent design para KODA
- ✅ State persistence implementada
- ✅ Harness evolution plan

---

### Semana 7-12: KODA-Específico (Nível 4)
```
Trabalho contínuo em:
- Melhorias no KODA
- Case studies reais
- Mentoring de novos membros
- Implementação de features
```

**Deliverables:**
- ✅ Nível 4 completion
- ✅ Team expertise solidificada
- ✅ KODA harness evolved

---

## 👥 Rastreamento de Progresso da Equipe

### Template de Rastreamento Individual

| Membro | Nível Atual | Exercícios | Case Studies | Status Geral |
|--------|-----------|-----------|-------------|------------|
| Membro A | 1 | 0/2 | - | 🔴 Iniciando |
| Membro B | 2 | 3/5 | 1/2 | 🟡 Em Progresso |
| Membro C | 3 | 8/8 | 1/3 | 🟢 Avançado |
| Membro D | 4 | 8/8 | 3/5 | 🟢 Expert |

Veja `tools-templates/team-progress-tracker.md` para versão interativa.

---

## 🔗 8 Conceitos Fundamentais

Cada conceito tem:
- 📖 Explicação em profundidade
- 🎨 3 Knowledge Graphs (Mermaid)
- 🔧 Aplicação prática KODA
- ✅ Checklist de implementação

| # | Conceito | Arquivo | Complexidade | Prioridade |
|---|----------|---------|-------------|-----------|
| 1 | Context Management | `05-core-concepts/01-context-management.md` | Nível 1 | 🔴 Alta |
| 2 | Planning vs. Execution | `05-core-concepts/02-planning-execution-separation.md` | Nível 2 | 🔴 Alta |
| 3 | Generator/Evaluator | `05-core-concepts/03-generator-evaluator-pattern.md` | Nível 2 | 🔴 Alta |
| 4 | Sprint Contracts | `05-core-concepts/04-sprint-contracts.md` | Nível 2 | 🟡 Média |
| 5 | State Persistence | `05-core-concepts/05-state-persistence.md` | Nível 3 | 🟡 Média |
| 6 | Harness Evolution | `05-core-concepts/06-harness-evolution.md` | Nível 3 | 🟡 Média |
| 7 | Multi-Agent Coord. | `05-core-concepts/07-multi-agent-coordination.md` | Nível 3 | 🟡 Média |
| 8 | Evaluation Rubrics | `05-core-concepts/08-evaluation-rubrics.md` | Nível 2 | 🟢 Média |

---

## 📈 Knowledge Graphs Disponíveis

Acesse em `06-knowledge-graphs/`:

- **Ecosystem Graph:** Mostra como todos os conceitos se conectam
- **KODA Feature Dependencies:** Qual conceito sustenta qual feature
- **Learning Progression:** Ordem correta de aprendizado
- **Problem-Solution Mapping:** Como conceitos resolvem problemas

Cada conceito tem 3 diagramas Mermaid detalhados.

---

## 🛠️ Guias de Implementação

Localizados em `07-implementation-guides/`:

1. **Setup Guide:** Como estruturar seu repositório e workflow
2. **Team Progression Guide:** Como escalar aprendizado da equipe
3. **Harness Design Checklist:** Lista de verificação para bom harness
4. **Evaluation Rubric Template:** Como criar rubrics de qualidade
5. **Trace Analysis Guide:** Como ler e interpretar traces
6. **Harness Evolution Playbook:** Como evoluir harness com novas modelos

---

## 📋 Templates Disponíveis

Localizados em `08-tools-templates/`:

```markdown
├── team-progress-tracker.md
│   └── Rastreia progresso individual e da equipe
│
├── learning-assessment-rubric.md
│   └── Avalia compreensão de conceitos
│
├── knowledge-graph-template.md
│   └── Template para criar novos Knowledge Graphs
│
├── sprint-contract-template.md
│   └── Template para definir contracts generator/evaluator
│
├── evaluation-rubric-template.md
│   └── Template para rubrics de qualidade
│
└── architecture-decision-record-template.md
    └── ADR template para decisões arquiteturais
```

---

## 📚 Casos de Estudo

Localizados em `09-case-studies/`:

### Casos de Estudo Gerais
1. **Retro Game Maker** - Case study da apresentação Anthropic
2. **Browser DAW App** - Digital Audio Workstation na web

### Casos de Estudo KODA
1. **Product Discovery** - Como KODA encontra produtos certos
2. **Order Processing** - Processamento completo de pedidos
3. **Fulfillment Workflow** - Coordenação de entrega

Cada caso inclui:
- 🎯 Objetivo
- 🏗️ Arquitetura
- 💾 Persistência de estado
- ✅ Testes/Verificação
- 🎓 Lições aprendidas

---

## 🚀 Como Começar

### Para Novos Membros da Equipe:
1. Leia `QUICK_START.md`
2. Complete Nível 1 (3-4 horas)
3. Faça exercícios do Nível 1
4. Revise `glossary.md` conforme necessário

### Para Líderes de Projeto:
1. Revise este documento (30 min)
2. Configure `team-progress-tracker.md`
3. Atribua membros a Níveis baseado em habilidades
4. Agende 1o workshop para Nível 1 (4 horas)

### Para Desenvolvedores Avançados:
1. Comece no Nível 3 se souber Nível 1-2
2. Foque em `04-nivel-4-koda-specific/`
3. Trabalhe em real-world exercises
4. Mentore novos membros

---

## 🔄 Como Usar Este Programa

### Leitura Sequencial (Recomendado)
```
Start
  ↓
QUICK_START.md (10 min)
  ↓
Nível 1: Fundamentals (4h)
  ↓
Nível 2: Practical (8h)
  ↓
Nível 3: Advanced (10h)
  ↓
Nível 4: KODA-Specific (ongoing)
```

### Leitura Modular
Pode pular diretamente para tópico de interesse:
- Quer aprender generator/evaluator? → Nível 2, Tópico 1
- Quer entender KODA? → Nível 4
- Quer entender Knowledge Graphs? → `06-knowledge-graphs/`

### Referência Rápida
- **Precisa de definição?** → `GLOSSARY.md`
- **Precisa de exemplo?** → `09-case-studies/`
- **Precisa de checklist?** → `07-implementation-guides/`

---

## 📞 Suporte e Perguntas

### FAQ
Veja `FAQ.md` para perguntas frequentes

### Termos Específicos
Veja `GLOSSARY.md` para definições

### Recursos Adicionais
Veja `10-references/` para:
- Resumo da apresentação Anthropic
- Timeline de capacidades dos modelos
- Links para recursos adicionais

---

## 📊 Métricas de Sucesso

### Nível 1
- ✅ 100% da equipe completa em 2 semanas
- ✅ 90%+ de acerto nos exercícios

### Nível 2
- ✅ 80%+ completa em 4 semanas
- ✅ Generator/Evaluator implementado em 1 feature KODA
- ✅ Rubrics documentadas para 2+ features

### Nível 3
- ✅ 50%+ completa em 6 semanas
- ✅ Multi-agent design proposto para KODA
- ✅ State persistence implementada

### Nível 4
- ✅ Membros avançados mentorando outros
- ✅ KODA harness evoluído baseado em padrões
- ✅ Novos features usando padrões ensinados

---

## 🔄 Versioning & Updates

**Versão Atual:** 1.0  
**Última Atualização:** Maio 2026  
**Próxima Revisão:** Quando nova release Claude (est. Julho 2026)

### Changelog
```
v1.0 (Maio 2026)
- Estrutura inicial completa
- Todos os 4 níveis documentados
- 8 conceitos core com Knowledge Graphs
- 5 casos de estudo (2 gerais + 3 KODA)
- Templates e checklists completos
```

---

## 📝 Como Contribuir

Encontrou erro ou tem sugestão?

1. Crie um PR com mudanças
2. Adicione seu nome ao fim do documento afetado
3. Atualize a data de última modificação

---

## 📬 Próximos Passos

1. **Hoje:** Compartilhe este documento com a equipe
2. **Amanhã:** Agende workshop de Nível 1 (4 horas)
3. **Próxima Semana:** Configure rastreamento de progresso
4. **Semana 2:** Comece Nível 1 com toda a equipe
5. **Semanas 3-4:** Implemente generator/evaluator no KODA
6. **Semanas 5-6:** Comece Nível 3 com membros avançados
7. **Semana 7+:** Contínuo aprimoramento de KODA

---

## ✨ Notas Finais

> "A jornada de 1000 milhas começa com um único passo." - Lao Tzu

Este programa foi desenhado para evoluir:
- 📚 Do conceitual ao prático
- 👥 Do individual à colaborativo  
- 🔧 Do aprender à aplicar
- 🏢 Do KODA para além do KODA

**Você não precisa completar tudo sozinho. Trabalhe com sua equipe, compartilhe aprendizados, e cresça junto.**

---

**Pronto para começar? Abra `QUICK_START.md` agora!** 🚀

---

*Documento Mestre | FutanBear Long-Running Agents Program | v1.0*
