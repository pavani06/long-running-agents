---
title: "Plano de Execução Atualizado: Implementação do Currículo"
type: source
date: 2026-05-26
tags:
  - curriculo-conteudo
  - governanca
aliases:
  - execution plan updated
  - plano de execucao atualizado
  - implementacao curriculo v2
relates-to:
  - "[[rawfiles/EXECUTION_PLAN|Execution Plan]]"
  - "[[rawfiles/DELIVERY-COMPLETE|Delivery Complete]]"
---

# 🗓️ PLANO DE EXECUÇÃO: Implementação do Currículo

**Data:** Maio 2026  
**Duração Total:** 12 semanas  
**Equipe:** FutanBear Technical Team  
**Objetivo:** Transformar equipe em especialistas de long-running agents  

---

## 📍 Status Atual

### Pré-Implementação (Semana 0) - ATUALIZADO MAIO 2026
- [x] Documento Mestre criado
- [x] QUICK START pronto
- [x] Glossário compilado
- [x] Estrutura de diretórios estabelecida
- [x] Equipe informada e alinhada
- [x] **NOVO:** Conteúdo Nível 1 expandido com profundidade 2.5x
- [x] **NOVO:** 2 exercícios práticos hands-on com código completo
- [x] **NOVO:** Exemplos progressivos (iniciante → mid-level dev)
- [x] **NOVO:** Métricas, trade-offs e gotchas adicionados

**Status:** ✅ Pré-implementação COMPLETADA com upgrade de qualidade
**Próximo:** Semana 1 começa segunda-feira (com conteúdo expandido)

---

## 🎯 Fases de Execução

```
FASE 1: FUNDAÇÃO (Semanas 1-2)
├─ Nível 1 para toda equipe
├─ Entendimento comum dos 3 problemas
└─ Preparação para Nível 2

FASE 2: PADRÕES (Semanas 3-4)
├─ Nível 2 para toda equipe
├─ Implementar 1 padrão em KODA
└─ Preparação para Nível 3

FASE 3: ARQUITETURA (Semanas 5-6)
├─ Nível 3 para membros avançados
├─ Desenhar arquitetura melhorada para KODA
└─ Preparação para Nível 4

FASE 4: APLICAÇÃO (Semanas 7-12)
├─ Nível 4 contínuo
├─ Implementar mudanças em KODA
├─ Mentoring e consolidação
└─ Documentação de aprendizados
```

---

## 📅 Calendário Semanal Detalhado

### SEMANA 1: O Problema (Nível 1 - Parte 1) - EXPANDIDA

**Tema:** Por que agentes falham? (com profundidade expandida em 2.5x)

**Mudanças Principais:**
- ✨ Conteúdo de `03-basic-harness-patterns.md` agora é 2.5x mais profundo
- ✨ 2 novos exercícios práticos com código completo
- ✨ Exemplos progressivos (iniciante → mid-level developer)
- ✨ Seções novas: Métricas, Trade-offs, Gotchas, Referências

| Dia | Atividade | Duração | Responsável | Status |
|-----|-----------|---------|------------|--------|
| **SEG** | Kickoff + QUICK START | 30 min | Líder | ⏳ |
| **SEG** | Ler `01-why-agents-lose-plot.md` | 45 min | Todos | ⏳ |
| **TER** | Ler `02-token-budgeting.md` | 45 min | Todos | ⏳ |
| **TER** | Síncronização de entendimento (call) | 30 min | Líder | ⏳ |
| **QUA** | Ler `03-basic-harness-patterns.md` (EXPANDIDO) | **90 min** | Todos | ⏳ |
| **QUA** | Q&A: Padrões + Narrativa Fernando | 30 min | Líder Tech | ⏳ |
| **QUI** | **Exercício 1: History Windowing** (NOVO) | **90 min** | Todos | ⏳ |
| **SEX** | **Exercício 2: Structured Output** (NOVO) | **90 min** | Todos | ⏳ |
| **SEX** | Review + Discussão | 45 min | Todos | ⏳ |

**Novo Conteúdo Adicionado:**
- 📊 Seção "Por Que Agora? O Contexto Histórico de 2026"
- 🔗 Conexões explícitas com jornada de Fernando
- 📈 Exemplos progressivos para cada padrão (Nível 1 simples → Nível 2 código Python real)
- ⚠️ Seção "Gotchas & Armadilhas Comuns" (top 10 erros)
- ⚖️ Seção "Trade-offs Comparativos" (decisão entre padrões)
- 📊 Seção "Métricas de Sucesso" (antes/depois com números reais)
- 📚 Seção "Referências & Recursos" (papers, ferramentas, comunidades)

**Exercícios Práticos Novos:**
1. ✅ `exercise-01_-_01-nivel-1-fundamentals-WINDOWING.md` (History Windowing)
   - Implementar ConversationManager
   - 5 testes práticos
   - Simular conversa de 4 horas
   
2. ✅ `exercise-02_-_01-nivel-1-fundamentals-STRUCTURED-OUTPUT.md` (Structured Output)
   - Usar Pydantic para validação
   - Implementar RecommendationValidator
   - 6 testes com validações de negócio

**Deliverable:** Todos entendem os 3 problemas + 5 padrões de harness + conseguem implementar 2 padrões
**Checkpoint Expandido:** 
- [ ] Leitura completa com compreensão
- [ ] Ambos exercícios completados com código funcional
- [ ] Todos entendem "quando usar qual padrão"
- [ ] Compreensão de métricas e trade-offs

**Tempo Total Semana:** 13-14 horas (vs 3 horas antes) - Upgrade 4-5x em conteúdo  

---

### SEMANA 2: Aplicação KODA (Nível 1 - Parte 2) - EXPANDIDA

**Tema:** Como os 3 problemas + 5 padrões afetam KODA? (Aplicação Prática)

**Mudanças Principais:**
- ✨ Agora inclui análise dos 5 padrões (não apenas 3 problemas)
- ✨ Comparação de métricas antes/depois
- ✨ Desenho de como KODA implementa todos os padrões juntos

| Dia | Atividade | Duração | Responsável | Status |
|-----|-----------|---------|------------|--------|
| **SEG** | Ler `nivel-1-koda.md` (aplicação dos padrões) | 45 min | Todos | ⏳ |
| **TER** | Exercício prático: Analisar conversa KODA real | 60 min | Pequeno grupo | ⏳ |
| **TER** | Mapear 5 padrões em KODA atual | 90 min | Pequeno grupo | ⏳ |
| **QUA** | Síncronização findings | 60 min | Todos | ⏳ |
| **QUI** | Documento: "Como KODA implementa os 5 padrões?" | 120 min | Líder + 1 tech | ⏳ |
| **QUI** | Palestra: "Métricas do harness KODA (antes/depois)" | 45 min | Líder Tech | ⏳ |
| **SEX** | Celebração Nível 1 COMPLETO! | 45 min | Todos | ⏳ |

**Novo Conteúdo:**
- 📊 Análise de como KODA usa os 5 padrões em combinação
- 📈 Métricas reais de melhoria (latência, custo, taxa de erro)
- 🔄 Fluxo end-to-end de um request em KODA
- 🎯 Trade-offs que KODA fez (por que padrão em qual situação)

**Deliverable:** 
- ✅ Todos completaram Nível 1 (ambos Semana 1 e 2)
- ✅ Documento: "Como KODA implementa os 5 padrões"
- ✅ Equipe consegue identificar padrões em código real

**Checkpoint Expandido:**
- [ ] Todos entendem os 5 padrões em teoria
- [ ] Todos conseguem reconhecer padrões em KODA real
- [ ] Todos compreendem a importância do "harness" vs "modelo"
- [ ] Preparado para Nível 2 (padrões mais avançados)

**Tempo Total Semana:** 8-9 horas (vs 4 horas antes)

---

### SEMANA 3: Padrões Práticos (Nível 2 - Parte 1)

**Tema:** Generator/Evaluator + Sprint Contracts

| Dia | Atividade | Duração | Responsável | Status |
|-----|-----------|---------|------------|--------|
| **SEG** | Revisão rápida Nível 1 | 15 min | Todos | ⏳ |
| **SEG** | Ler `01-generator-evaluator-pattern.md` | 90 min | Todos | ⏳ |
| **TER** | Ler `02-sprint-contracts.md` | 90 min | Todos | ⏳ |
| **TER** | Síncronização + Q&A | 30 min | Líder | ⏳ |
| **QUA** | Exercício `exercise-01.md` (generator/evaluator) | 60 min | Todos | ⏳ |
| **QUI** | Exercício `exercise-02.md` (contracts) | 60 min | Todos | ⏳ |
| **SEX** | Discussão: Aplicar em KODA? | 45 min | Todos | ⏳ |

**Deliverable:** Todos compreendem os 2 padrões  

---

### SEMANA 4: Rubrics e Aplicação (Nível 2 - Parte 2)

**Tema:** Rubric Design + Trace Reading

| Dia | Atividade | Duração | Responsável | Status |
|-----|-----------|---------|------------|--------|
| **SEG** | Ler `03-rubric-design.md` | 90 min | Todos | ⏳ |
| **TER** | Ler `04-trace-reading.md` | 90 min | Todos | ⏳ |
| **TER** | Case study: Retro Game Maker traces | 45 min | Pequeno grupo | ⏳ |
| **QUA** | Exercício `exercise-03.md` (rubric design) | 60 min | Todos | ⏳ |
| **QUI** | Micro-projeto: Rubric para feature KODA | 90 min | Pequeno grupo | ⏳ |
| **SEX** | Apresentação: "Como aplicar Nível 2 ao KODA" | 60 min | Pequeno grupo | ⏳ |

**Deliverable:**
- Todos completaram Nível 2
- 1+ rubrics para features do KODA
- Plano para implementar generator/evaluator em 1 feature

---

### SEMANA 5: Multi-Agent Systems (Nível 3 - Parte 1)

**Tema:** Arquitetura de múltiplos agentes

**Quem:** Membros em Nível 2+ (pode ser subconjunto)

| Dia | Atividade | Duração | Responsável | Status |
|-----|-----------|---------|------------|--------|
| **SEG** | Ler `01-multi-agent-systems.md` | 90 min | Avançados | ⏳ |
| **TER** | Ler `02-state-persistence.md` | 90 min | Avançados | ⏳ |
| **TER** | Síncronização + Q&A | 30 min | Líder tech | ⏳ |
| **QUA** | Ler `03-file-based-coordination.md` | 90 min | Avançados | ⏳ |
| **QUI** | Exercício `exercise-01.md` (3-agent design) | 90 min | Avançados | ⏳ |
| **SEX** | Brainstorm: Como aplicar 3-agent em KODA? | 60 min | Avançados | ⏳ |

**Paralelo (Resto da equipe):** Consolidar Nível 2, começar mentoring

**Deliverable:** Avançados compreendem multi-agent systems  

---

### SEMANA 6: State e Harness Evolution (Nível 3 - Parte 2)

**Tema:** State Persistence + Harness Evolution

| Dia | Atividade | Duração | Responsável | Status |
|-----|-----------|---------|------------|--------|
| **SEG** | Ler `04-server-side-compaction.md` | 60 min | Avançados | ⏳ |
| **TER** | Ler `05-harness-evolution.md` | 90 min | Avançados | ⏳ |
| **TER** | Case study: Retro Game Maker (arq completa) | 45 min | Avançados | ⏳ |
| **QUA** | Exercício `exercise-02.md` (state persistence) | 90 min | Avançados | ⏳ |
| **QUI** | Exercício `exercise-03.md` (harness evolution) | 90 min | Avançados | ⏳ |
| **SEX** | Síncronização: Estado do design KODA | 60 min | Todos | ⏳ |

**Paralelo (Resto):** Mentoring, implementar 1 padrão Nível 2 em KODA

**Deliverable:**
- Avançados completaram Nível 3
- Proposta: "Arquitetura melhorada para KODA"

---

### SEMANA 7-8: KODA-Específico Fase 1 (Nível 4)

**Tema:** Arquitetura e padrões atuais do KODA

| Dia | Atividade | Duração | Responsável | Status |
|-----|-----------|---------|------------|--------|
| **Semana 7** | | | | |
| SEG | Ler `01-koda-architecture.md` | 90 min | Avançados | ⏳ |
| TER | Ler `02-customer-journey-flows.md` | 90 min | Avançados | ⏳ |
| TER | Review arquitetura real do KODA | 60 min | Avançados + PM | ⏳ |
| QUA | Ler `04-evaluation-rubrics-koda.md` | 90 min | Avançados | ⏳ |
| QUI | Desenhar rubrics para features KODA | 120 min | Avançados | ⏳ |
| SEX | Síncronização: Achados | 45 min | Todos | ⏳ |
| | | | | |
| **Semana 8** | | | | |
| SEG | Ler `03-feature-design-patterns.md` | 90 min | Avançados | ⏳ |
| TER | Real-world exercise: Analisar trace KODA | 120 min | Avançados | ⏳ |
| QUA | Ler `05-harness-improvements.md` | 90 min | Avançados | ⏳ |
| QUI | Micro-projeto: Propor 1 melhoria KODA | 120 min | Pequeno grupo | ⏳ |
| SEX | Review: Propostas de melhoria | 60 min | Todos | ⏳ |

**Paralelo:** Resto da equipe implementa primeiro padrão em KODA, documenta

**Deliverable:**
- 3+ rubrics para features KODA
- 2-3 melhorias propostas com análise
- Primeira feature com generator/evaluator funcionando

---

### SEMANA 9-10: KODA-Específico Fase 2 (Implementação)

**Tema:** Implementação de melhorias

| Dia | Atividade | Duração | Responsável | Status |
|-----|-----------|---------|------------|--------|
| **Semana 9** | | | | |
| SEG-QUI | Trabalhar em PRs para melhorias propostas | 240 min | Todos | ⏳ |
| QUI | Code review + feedback | 60 min | Todos | ⏳ |
| SEX | Sincronização do progresso | 45 min | Todos | ⏳ |
| | | | | |
| **Semana 10** | | | | |
| SEG-QUI | Continuar implementação | 240 min | Todos | ⏳ |
| QUI | Testing de melhorias | 120 min | Todos | ⏳ |
| SEX | Prepare para deployin | 60 min | Todos | ⏳ |

**Goal:** 1-2 melhorias implementadas e testadas

---

### SEMANA 11-12: Consolidação e Documentação

**Tema:** Consolidar aprendizado, documentar, ensinar

| Dia | Atividade | Duração | Responsável | Status |
|-----|-----------|---------|------------|--------|
| **Semana 11** | | | | |
| SEG | Deploy melhorias em KODA | Variável | Devops | ⏳ |
| TER | Monitorar e ajustar | Variável | Todos | ⏳ |
| QUA | Case study: "Como KODA evoluiu" | 90 min | Líder | ⏳ |
| QUI | Documentar lessons learned | 120 min | Todos | ⏳ |
| SEX | Prepare mentoring materials | 90 min | Avançados | ⏳ |
| | | | | |
| **Semana 12** | | | | |
| SEG | Workshop final: Mentoring novos membros | 120 min | Avançados | ⏳ |
| TER | Celebrate! | 60 min | Todos | ⏳ |
| QUA | Retrospectiva: O que aprendemos? | 120 min | Todos | ⏳ |
| QUI | Planejar próximo ciclo (Claude 5.0?) | 90 min | Líderes | ⏳ |
| SEX | Encerramento + Documentação final | 90 min | Todos | ⏳ |

**Deliverable:**
- Curso rodou completamente
- Equipe é expert em long-running agents
- Novo ciclo de aprendizado planejado

---

## 👥 Alocação de Tempo por Pessoa (ATUALIZADO)

### Para Cada Membro da Equipe

```
Semana 1-2:  13-16 horas/semana (Nível 1 EXPANDIDO - 2.5x profundo + exercícios)
             ├─ Leitura + compreensão: 3-4 h
             ├─ 2 exercícios práticos completos: 8-10 h
             └─ Síncronizações + discussões: 2-3 h

Semana 3-4:  6-7 horas/semana (Nível 2 para todos)
Semana 5-6:  
  - Avançados: 10-12 horas/semana (Nível 3)
  - Outros: 3-4 horas/semana (consolidação + mentoring)
Semana 7-12: 12-18 horas/semana (implementação ativa)
```

### Total Estimado por Pessoa

- **Participante Padrão:** 40-50 horas (vs 30-40 antes) - +25%
- **Membro Avançado:** 60-70 horas (vs 50-60 antes) - +20%
- **Líder/Mentor:** 70-90 horas (vs 60-80 antes) - +15%

**Justificativa:** Semana 1-2 é mais intensa devido ao conteúdo profundo + 2 exercícios práticos com código Python/Pydantic completo.

---

## 🎯 Responsabilidades por Papel

### Líder do Programa
- [ ] Criar estrutura semanal
- [ ] Facilitar sincronizações
- [ ] Desbloquear obstáculos
- [ ] Rastrear progresso
- [ ] Garantir qualidade de mentoring

**Tempo:** 5-8 horas/semana

### Líder Técnico
- [ ] Responder perguntas técnicas
- [ ] Revisar exercícios
- [ ] Mentorear Nível 3+
- [ ] Guiar implementação em KODA
- [ ] Documentar decisões arquiteturais

**Tempo:** 5-10 horas/semana

### Membros Regulares
- [ ] Completar leituras semanais
- [ ] Fazer exercícios
- [ ] Participar de síncronizações
- [ ] Implementar padrões em KODA

**Tempo:** 4-6 horas/semana

### Membros Avançados (a partir de semana 5)
- [ ] Completar Nível 3-4
- [ ] Mentorear membros regulares
- [ ] Liderar implementações
- [ ] Documentar aprendizados

**Tempo:** 8-15 horas/semana

---

## 📊 Métricas de Progresso (ATUALIZADO)

### Semanal

| Semana | Métrica | Meta | Real | Observação |
|--------|---------|------|------|-----------|
| 1-2 | % completando Nível 1 (EXPANDIDO) | 100% | ⏳ | Inclui 2 exercícios com código |
| 1-2 | % com exercícios funcionando | 100% | ⏳ | ConversationManager + Validator |
| 1-2 | Compreensão de 5 padrões | 100% | ⏳ | Não apenas 3 problemas |
| 3-4 | % completando Nível 2 | 100% | ⏳ | Generator/Evaluator + Sprint Contracts |
| 5-6 | % avançados em Nível 3 | 80% | ⏳ | Multi-agent systems |
| 7-8 | Padrões implementados no KODA | 1+ | ⏳ | Pode começar com History Windowing |
| 9-10 | Melhorias em produção | 1-2 | ⏳ | Com métricas antes/depois |
| 11-12 | Equipe expert | 80% | ⏳ | Consegue mentorear novatos |

### Global

- **Conclusão de Nível 1:** 100% da equipe até semana 2 ✅ (com profundidade 2.5x)
  - Inclui compreensão dos 5 padrões (não apenas 3 problemas)
  - Inclui 2 exercícios práticos completos
  - Inclui análise de KODA real com métricas
  
- **Conclusão de Nível 2:** 100% da equipe até semana 4
- **Conclusão de Nível 3:** 60-80% da equipe até semana 6
- **Conclusão de Nível 4:** 50%+ da equipe até semana 12
- **Aplicação em KODA:** 1-3 features melhoradas até semana 12

**Novo Checkpoint - Qualidade de Aprendizado:**
- [ ] Equipe consegue explicar "por que" cada padrão importa (não apenas "o quê")
- [ ] Equipe consegue reconhecer padrões em código real (KODA)
- [ ] Equipe consegue implementar 2+ padrões (History Windowing + Structured Output)
- [ ] Equipe entende trade-offs entre padrões (quando usar qual)

---

## 🚨 Possíveis Desafios e Planos de Contingência

### Desafio 1: "Não temos tempo"
**Solução:**
- Comprima Nível 1-2 para 2 semanas se necessário
- Pule exercícios e vá direto para aplicação KODA
- Máx eficiência nas sincronizações

---

### Desafio 2: "Não entendo X"
**Solução:**
- Volte e releia
- Converse com mentor
- Faça exercício novamente
- Veja case studies (casos de estudo)

---

### Desafio 3: "Implementação é mais difícil do que esperado"
**Solução:**
- Comece com feature menor
- Use templates fornecidos
- Code review agressivo
- Ajuste escopo conforme necessário

---

### Desafio 4: "Nova release Claude durante o programa"
**Solução:**
- Atualize MASTER_PLAN se necessário
- Foco em conceitos (válidos sempre)
- Implementação muda, conceitos não

---

## ✅ Checklist de Pré-Lançamento

Antes de semana 1 começar:

- [ ] Repositório configurado
- [ ] Todos têm acesso aos documentos
- [ ] Calendário bloqueado
- [ ] Primeiro workshop agendado (Seg semana 1)
- [ ] Roles/responsabilidades claras
- [ ] Comunicado enviado à equipe
- [ ] Recursos (exemplos, ferramentas) prontos
- [ ] Template de rastreamento criado
- [ ] Slack channel #long-running-agents criado
- [ ] Retrospectiva semanal agendada

---

## 📝 Templates para Documentar Progresso

### Relatório Semanal (Sexta-feira)

```markdown
# Semana X - Relatório de Progresso

## Nível 1-4: Status de Progresso
- [ ] Nível 1: X de Y completo
- [ ] Nível 2: X de Y completo
- [ ] Nível 3: X de Y completo
- [ ] Nível 4: X de Y completo

## Exercícios Completos
- [x] Exercício A
- [ ] Exercício B

## Implementações KODA
- Feature X: Em progresso (PR #123)
- Feature Y: Completada

## Bloqueadores
- Problema 1: [Descrição]
  Solução: [Plano]

## Próxima Semana
- [ ] Tarefa 1
- [ ] Tarefa 2

## Observações
[Notas gerais]
```

---

## 🔗 Links Importantes para Referência Rápida

| Recurso | Localização |
|---------|------------|
| Master Plan | MASTER_PLAN.md |
| Quick Start | QUICK_START.md |
| Glossário | GLOSSARY.md |
| Nível 1 | `01-nivel-1-fundamentals/` |
| Nível 2 | `02-nivel-2-practical-patterns/` |
| Nível 3 | `03-nivel-3-advanced-architecture/` |
| Nível 4 | `04-nivel-4-koda-specific/` |
| Knowledge Graphs | `06-knowledge-graphs/` |
| Templates | `08-tools-templates/` |
| Case Studies | `09-case-studies/` |

---

## 🎯 Success Criteria (ATUALIZADO - MAIS PROFUNDO)

### Semana 2 (Nível 1 EXPANDIDO)
✅ Todos entendem os 3 problemas + 5 padrões (não apenas 3 problemas)  
✅ Todos conseguem implementar History Windowing (código funcionando)  
✅ Todos conseguem implementar Structured Output com Pydantic  
✅ Compreensão de métricas antes/depois e trade-offs  
✅ Identificados 5+ padrões em KODA real  
✅ Nenhum gap na compreensão de "por que" cada padrão importa

### Semana 4 (Nível 2)
✅ Padrões compreendidos (Generator/Evaluator + Sprint Contracts)  
✅ Rubrics criadas para KODA  
✅ Plano para implementar 1 padrão  
✅ Código de exercício funcional

### Semana 6 (Nível 3)
✅ Avançados compreendem arquitetura (multi-agent systems)  
✅ Proposta de re-design KODA  
✅ Começado implementação de Nível 2  
✅ Capaz de mentorear outros em Nível 1-2

### Semana 8
✅ 1+ padrão implementado em KODA em produção  
✅ Case study do processo documentado  
✅ Equipe alinhada em direção  
✅ Métricas de melhoria visíveis

### Semana 12 (Final)
✅ Equipe é expert em long-running agents  
✅ KODA significativamente melhorado com 2-3 padrões  
✅ Novas features usando padrões  
✅ Processo contínuo de melhoria estabelecido  
✅ Mentoring de novos membros iniciado  
✅ **NOVO:** Documentação de "como implementar harnesses" criada

---

## 🚀 Upgrade de Qualidade: Nível 1 Expandido (Maio 2026)

### O Que Mudou

**Antes (Versão Original):**
- 3 documentos (3 problemas apenas)
- Conteúdo: ~560 linhas
- Sem exemplos de código
- 1 exercício vago

**Depois (Versão Expandida - MAIO 2026):**
- 5 padrões descritos em profundidade
- Conteúdo: ~1.400 linhas (+156%)
- 2 exercícios práticos com código completo Python/Pydantic
- Exemplos progressivos (iniciante → mid-level dev)
- Seções novas: Métricas, Trade-offs, Gotchas, Referências
- Conectado narrativa Fernando (inovação, arquitetura, escala)

### Arquivos Novos Criados

1. **03-basic-harness-patterns-IMPROVED.md** (1.436 linhas)
   - Versão expandida com profundidade 2.5x
   - 5 padrões + contexto histórico + métricas

2. **exercise-01_-_01-nivel-1-fundamentals-WINDOWING.md** (400+ linhas)
   - Implementar History Windowing
   - ConversationManager com DB simulation
   - 5 testes práticos

3. **exercise-02_-_01-nivel-1-fundamentals-STRUCTURED-OUTPUT.md** (450+ linhas)
   - Implementar Structured Output com Pydantic
   - RecommendationValidator com business rules
   - 6 testes com validações

### Impacto para a Equipe

| Dimensão | Antes | Depois | Melhoria |
|----------|-------|--------|----------|
| **Profundidade** | 3 problemas | 5 padrões + contexto | +250% |
| **Exemplos Prático** | Nenhum | 2 exercícios completos | ∞ |
| **Código Real** | Não | Python/Pydantic funcional | ∞ |
| **Tempo Semana 1-2** | 8 horas | 16 horas | +100% |
| **Compreensão Esperada** | Conceitual | Prática + Conceptual | +200% |
| **Preparação para Nível 2** | Básica | Avançada | +150% |

### Quem Se Beneficia Mais

1. **Mid-level Developers:** Vão aprender implementação real (Python, Pydantic, gerenciamento de DB)
2. **Iniciantes:** Vão ter exemplos progressivos para acompanhar
3. **Líderes Técnicos:** Vão ter métricas e trade-offs para tomar decisões
4. **Equipe KODA:** Vai entender exatamente como cada padrão funciona em produção

### Recomendação para Execução

Considere **adicionar 1-2 dias extras** na Semana 1-2 para que a equipe possa:
- Absorver a profundidade maior
- Completar os exercícios com qualidade
- Discutir aplicações reais em KODA

---

## 📞 Como Começar AGORA (ATUALIZADO)

1. **Segunda-feira, 9h:** Workshop Kickoff (30 min)
   - Apresente MASTER_PLAN
   - Distribua QUICK_START
   - Anuncie upgrade de qualidade do Nível 1
   - Explique novo cronograma (16h vs 8h por semana)

2. **Segunda-feira, 10h:** Primeira leitura (45 min)
   - Todos leiam `01-why-agents-lose-plot.md`
   - Live reading + discussão

3. **Quarta-feira, 14h:** Leitura de Padrões (90 min)
   - Todos leiam `03-basic-harness-patterns.md` (EXPANDIDO)
   - Foco em entender cada padrão
   - Q&A: "Por que cada padrão?"

4. **Quinta-feira, 10h:** Exercício 1 (90 min)
   - **Todos** implementam History Windowing
   - ConversationManager pronto para rodar
   - 5 testes devem passar ✅

5. **Sexta-feira, 14h:** Exercício 2 (90 min)
   - **Todos** implementam Structured Output
   - RecommendationValidator com Pydantic
   - 6 testes devem passar ✅

6. **Sexta-feira, 17h:** Celebração (45 min)
   - Showcase dos exercícios
   - Discussão: "O que aprendemos?"
   - Prepare para Semana 2

---

1. **Segunda-feira, 9h:** Workshop Kickoff
   - Apresente MASTER_PLAN
   - Distribua QUICK_START
   - Responda perguntas

2. **Segunda-feira, 10h:** Primeira leitura
   - Todos leiam `01-why-agents-lose-plot.md`
   - Live reading + discussão
   - 45 minutos

3. **Terça-feira:** Segunda leitura
   - Todos leiam `02-token-budgeting.md`
   - Discussão assíncrona no Slack

4. **Quinta-feira:** Primeira sincronização
   - Q&A
   - Clarificações
   - Próximos passos

5. **Sexta-feira:** Primeiro exercício
   - Todos fazem `exercise-01.md`
   - Submeter respostas
   - Review e feedback

---

## 📞 Suporte During Program

### Perguntas Técnicas
→ Líder Técnico (Slack #long-running-agents)

### Perguntas Administrativas  
→ Líder do Programa

### Obstáculos
→ Escalate imediatamente

### Feedback
→ Formulário anônimo (link em construção)

---

*Plano de Execução | 12 semanas para expertise | v1.0*

**Pronto para começar? Vá para QUICK_START.md!**
