# 🗓️ PLANO DE EXECUÇÃO: Implementação do Currículo

**Data:** Maio 2026  
**Duração Total:** 12 semanas  
**Equipe:** FutanBear Technical Team  
**Objetivo:** Transformar equipe em especialistas de long-running agents  

---

## 📍 Status Atual

### Pré-Implementação (Semana 0)
- [ ] Documento Mestre criado
- [ ] QUICK START pronto
- [ ] Glossário compilado
- [ ] Estrutura de diretórios estabelecida
- [ ] Equipe informada e alinhada

**Próximo:** Semana 1 começa segunda-feira

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

### SEMANA 1: O Problema (Nível 1 - Parte 1)

**Tema:** Por que agentes falham?

| Dia | Atividade | Duração | Responsável | Status |
|-----|-----------|---------|------------|--------|
| **SEG** | Kickoff + QUICK START | 30 min | Líder | ⏳ |
| **SEG** | Ler `01-why-agents-lose-plot.md` | 45 min | Todos | ⏳ |
| **TER** | Ler `02-token-budgeting.md` | 45 min | Todos | ⏳ |
| **TER** | Síncronização de entendimento (call) | 30 min | Líder | ⏳ |
| **QUA** | Ler `03-basic-harness-patterns.md` | 45 min | Todos | ⏳ |
| **QUI** | Exercício `exercise-01.md` | 45 min | Todos | ⏳ |
| **SEX** | Review + Discussão | 45 min | Todos | ⏳ |

**Deliverable:** Todos entendem os 3 problemas  
**Checkpoint:** Todos respondem "sim" ao checklist Nível 1  

---

### SEMANA 2: Aplicação KODA (Nível 1 - Parte 2)

**Tema:** Como os 3 problemas afetam KODA?

| Dia | Atividade | Duração | Responsável | Status |
|-----|-----------|---------|------------|--------|
| **SEG** | Ler `koda-applications/nivel-1-koda.md` | 45 min | Todos | ⏳ |
| **TER** | Exercício `exercise-02.md` | 45 min | Todos | ⏳ |
| **TER** | Mapear 3 problemas em KODA atual | 60 min | Pequeno grupo | ⏳ |
| **QUA** | Síncronização findings | 45 min | Todos | ⏳ |
| **QUI** | Documento: "Como KODA enfrenta 3 problemas hoje?" | 90 min | Líder + 1 tech | ⏳ |
| **SEX** | Celebração Nível 1 completo! | 30 min | Todos | ⏳ |

**Deliverable:** 
- Todos completaram Nível 1
- Documento identificando 3 problemas em KODA

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

## 👥 Alocação de Tempo por Pessoa

### Para Cada Membro da Equipe

```
Semana 1-2:  4-5 horas/semana (Nível 1 para todos)
Semana 3-4:  5-6 horas/semana (Nível 2 para todos)
Semana 5-6:  
  - Avançados: 8-10 horas/semana (Nível 3)
  - Outros: 2-3 horas/semana (consolidação + mentoring)
Semana 7-12: 10-15 horas/semana (implementação ativa)
```

### Total Estimado por Pessoa
- **Participante Padrão:** 30-40 horas
- **Membro Avançado:** 50-60 horas
- **Líder/Mentor:** 60-80 horas

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

## 📊 Métricas de Progresso

### Semanal

| Semana | Métrica | Meta | Real |
|--------|---------|------|------|
| 1-2 | % completando Nível 1 | 100% | ⏳ |
| 3-4 | % completando Nível 2 | 100% | ⏳ |
| 5-6 | % avançados em Nível 3 | 80% | ⏳ |
| 7-8 | Padrões implementados no KODA | 1+ | ⏳ |
| 9-10 | Melhorias em produção | 1-2 | ⏳ |
| 11-12 | Equipe expert | 80% | ⏳ |

### Global

- **Conclusão de Nível 1:** 100% da equipe até semana 2
- **Conclusão de Nível 2:** 100% da equipe até semana 4
- **Conclusão de Nível 3:** 60-80% da equipe até semana 6
- **Conclusão de Nível 4:** 50%+ da equipe até semana 12
- **Aplicação em KODA:** 1-3 features melhoradas até semana 12

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

## 🎯 Success Criteria

### Semana 2 (Nível 1)
✅ Todos entendem os 3 problemas  
✅ Nenhum gaps na compreensão  
✅ Identificados 3+ problemas em KODA

### Semana 4 (Nível 2)
✅ Padrões compreendidos  
✅ Rubrics criadas para KODA  
✅ Plano para implementar 1 padrão

### Semana 6 (Nível 3)
✅ Avançados compreendem arquitetura  
✅ Proposta de re-design KODA  
✅ Começado implementação de Nível 2

### Semana 8
✅ 1+ padrão implementado em KODA  
✅ Case study do processo documentado  
✅ Equipe alinhada em direção

### Semana 12 (Final)
✅ Equipe é expert em long-running agents  
✅ KODA significativamente melhorado  
✅ Novas features usando padrões  
✅ Processo contínuo de melhoria estabelecido  
✅ Mentoring de novos membros iniciado

---

## 🚀 Como Começar AGORA

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
