---
title: "Guia de Progressão da Equipe"
type: curriculum-guide
aliases: []
tags: [curriculo-conteudo, guia-implementacao]
last_updated: 2026-06-10
---
# 🧭 Guia de Progressão da Equipe
## Como Escalar o Aprendizado de Long-Running Agents na Sua Organização

**Tempo Estimado:** 60 minutos (leitura) + aplicação contínua  
**Nível:** Guia para Líderes Técnicos  
**Pré-requisitos:** Ter lido o `README.md` e `MASTER_PLAN.md` do currículo  
**Status:** 🟢 ESSENCIAL — Guia operacional para líderes que gerenciam times aprendendo Long-Running Agents  
**Data de Criação:** Maio 2026

---

## 📖 Prólogo: O Desafio que Ninguém te Conta Sobre Liderar Aprendizado de IA

**Segunda-feira, 9h15. Sala de reunião do time KODA.**

Fernando olhou para o whiteboard coberto de post-its. Cada um representava uma pessoa do time e seu progresso no programa de Long-Running Agents.

O programa tinha começado havia 6 semanas. O entusiasmo inicial foi elétrico — todo mundo animado para aprender sobre agentes que rodam por horas, padrões Generator/Evaluator, arquiteturas multi-agente. Era o futuro.

Mas agora, na semana 6, o whiteboard contava uma história diferente:

```
Time KODA — Progresso em Long-Running Agents (Semana 6/12)

Nível 1 (Fundamentals) — Completaram:
  ✅ Ana (Senior)      — 2 semanas (ritmo rápido)
  ✅ Carlos (Pleno)    — 4 semanas (ritmo médio)
  ⚠️ Pedro (Junior)    — 6 semanas e ainda não completou
  ⚠️ Julia (Junior)    — 5 semanas, travada no exercício 3

Nível 2 (Practical Patterns) — Completaram:
  ✅ Ana (Senior)      — 4 semanas, já quer avançar
  ⏳ Carlos (Pleno)    — Na metade, ritmo bom

Nível 3 (Advanced) — Ninguém chegou ainda

Nível 4 (KODA-Specific) — Ninguém
```

Fernando respirou fundo. O problema não era o conteúdo. O conteúdo era excelente — rico em exemplos, baseado em problemas reais, com exercícios práticos.

O problema era **progressão**.

Algumas pessoas voavam. Outras estavam travadas. Algumas terminavam um nível mas não sabiam se realmente aprenderam. Outras se sentiam sobrecarregadas com a quantidade de material. E, pior de tudo, Fernando não tinha **métricas** para saber se o programa estava funcionando.

> *"Eu sei que o conteúdo é bom. Mas como eu sei que o time está aprendendo DE VERDADE? Como eu sei se alguém está pronto para avançar? Como eu ajudo quem está travado sem microgerenciar? Como eu meço progresso sem criar ansiedade de performance?"*

**Este guia é a resposta para essas perguntas.**

### O Que Este Guia Resolve

Se você é um líder técnico gerenciando um time que está aprendendo Long-Running Agents, você enfrenta 5 desafios específicos:

1. **Velocidades Diferentes:** Cada pessoa aprende em ritmo diferente. Como manter coesão do time sem segurar os rápidos nem perder os lentos?

2. **Ilusão de Aprendizado:** Alguém lê o material, faz os exercícios, mas será que realmente ENTENDEU ou apenas completou?

3. **Falta de Métricas:** Como medir progresso sem criar uma cultura de "passar em teste"? Como equilibrar rigor com segurança psicológica?

4. **Mentoring Eficiente:** Sêniores querem ajudar, mas como estruturar mentoring para que seja produtivo e não vire "faz pra mim"?

5. **Aplicação Prática:** A pessoa entendeu Generator/Evaluator na teoria. Mas consegue aplicar no código real do KODA? Como fazer a ponte?

Este guia oferece ferramentas práticas para cada um desses desafios.

### Conexão com o Programa

Você já leu o `MASTER_PLAN.md` e conhece a estrutura do programa:

```
Nível 1: Fundamentos (Semanas 1-2)
  → Por que agentes falham, token budgeting, harness patterns básicos

Nível 2: Padrões Práticos (Semanas 3-4)
  → Generator/Evaluator, Sprint Contracts, Rubric Design, Trace Reading

Nível 3: Arquitetura Avançada (Semanas 5-6)
  → Multi-agent systems, state persistence, file-based coordination

Nível 4: KODA-Específico (Semanas 7-12)
  → Arquitetura KODA, customer journey, feature design, implementação real
```

Mas o `MASTER_PLAN.md` diz **o quê** ensinar. Este guia diz **como liderar** o aprendizado.

### Para Quem É Este Guia

- **Tech Leads & Engineering Managers:** Você é responsável pelo crescimento técnico do time
- **Mentores & Sêniores:** Você vai mentorar pessoas durante o programa
- **Pessoas participantes:** Você quer entender como será avaliado e como progredir
- **Diretores & Heads:** Você quer métricas para justificar o investimento no programa

### O Que Você Vai Encontrar Aqui

✅ **Roadmap de progressão** — timeline visual com marcos claros  
✅ **Checkpoints por nível** — critérios objetivos de "está pronto para avançar"  
✅ **Métricas de equipe** — KPIs que medem aprendizado real, não apenas completação  
✅ **Estratégias de mentoring** — templates para sessões produtivas de pair programming  
✅ **Templates de avaliação** — rubricas, feedback, auto-avaliação  
✅ **Aplicação KODA** — como tudo isso se aplica ao nosso contexto real  
✅ **Plano de ação** — próximos passos para implementar hoje

---

## 🗺️ Roadmap de Progressão por Nível

### Visão Geral: A Jornada de 12 Semanas

O programa foi desenhado para 12 semanas, mas a realidade é que pessoas diferentes progridem em velocidades diferentes. O roadmap abaixo mostra **expectativas realistas**, não ideais teóricos.

```
SEMANA 1-2          SEMANA 3-4          SEMANA 5-6          SEMANA 7-12
┌──────────┐       ┌──────────┐       ┌──────────┐       ┌──────────────────┐
│ NÍVEL 1  │  ──▶  │ NÍVEL 2  │  ──▶  │ NÍVEL 3  │  ──▶  │ NÍVEL 4          │
│          │       │          │       │          │       │ (KODA-Specific)   │
│ 3 horas  │       │ 8 horas  │       │ 10 horas │       │ Contínuo          │
└──────────┘       └──────────┘       └──────────┘       └──────────────────┘
     │                   │                   │                    │
     ▼                   ▼                   ▼                    ▼
 Entender           Aplicar             Projetar             Liderar
 os problemas       os padrões          arquiteturas         e mentorar
```

### Progressão Esperada por Perfil

| Perfil | Nível 1 | Nível 2 | Nível 3 | Nível 4 | Ritmo |
|--------|---------|---------|---------|---------|-------|
| **Junior** (0-2 anos exp.) | 3-4 semanas | 4-6 semanas | 6-8 semanas | Contínuo | Lento, focar fundamentos |
| **Pleno** (2-5 anos exp.) | 2-3 semanas | 3-4 semanas | 3-5 semanas | Contínuo | Médio, aplicar patterns |
| **Senior** (5+ anos exp.) | 1-2 semanas | 2-3 semanas | 2-3 semanas | Contínuo | Rápido, mentorar outros |
| **Staff/Principal** | 1 semana | 1-2 semanas | 1-2 semanas | Imediato | Referência, revisar material |

**Nota importante:** Essas são estimativas. O programa valoriza **compreensão profunda**, não velocidade. Alguém que leva 6 semanas no Nível 1 mas entende cada conceito profundamente está melhor que alguém que "completou" em 1 semana sem entender.

### O Que Significa "Completar" um Nível

Completar um nível **não é** apenas ler os arquivos. É demonstrar compreensão através de 3 pilares:

```
┌──────────────────────────────────────────────────────────┐
│            CRITÉRIOS DE COMPLETUDE POR NÍVEL              │
├───────────────┬──────────────────────────────────────────┤
│ Pilar 1:      │ Consegue explicar os conceitos-chave     │
│ CONHECIMENTO  │ do nível em suas próprias palavras,      │
│               │ com exemplos próprios (não do material)  │
├───────────────┼──────────────────────────────────────────┤
│ Pilar 2:      │ Completa TODOS os exercícios do nível    │
│ PRÁTICA       │ com 80%+ de acurácia. Se errar, entende │
│               │ por que errou e consegue corrigir        │
├───────────────┼──────────────────────────────────────────┤
│ Pilar 3:      │ Consegue aplicar pelo menos 1 conceito   │
│ APLICAÇÃO     │ do nível em código real (KODA ou projeto │
│               │ paralelo) com resultado demonstrável     │
└───────────────┴──────────────────────────────────────────┘
```

### Timeline Detalhada por Nível

#### 🟢 Nível 1: Fundamentos (Semanas 1-2, ~3-4 horas de conteúdo)

**Objetivo:** Entender POR QUE agentes falham em tarefas longas

| Semana | Atividade | Entregável | Tempo Estimado |
|--------|-----------|------------|----------------|
| 1 | Ler `01-why-agents-lose-plot.md` | Resumo de 1 página | 45 min |
| 1 | Ler `02-token-budgeting.md` | Cálculo de budget para caso real | 45 min |
| 1 | Ler `03-basic-harness-patterns.md` | Identificar padrões no KODA | 45 min |
| 1 | Fazer `exercises/exercise-01.md` | Respostas + auto-correção | 30 min |
| 2 | Ler `nivel-1-koda.md` | Relacionar teoria ↔ KODA | 30 min |
| 2 | **Checkpoint Nível 1** | Prova de conhecimento + code review | 45 min |

**Sinais de que a pessoa ENTENDEU Nível 1:**
- Consegue explicar os 3 problemas (Context Amnesia, Planning Collapse, Self-Evaluation Collapse) sem olhar o material
- Consegue dar exemplos REAIS (do KODA ou de outro sistema) de cada problema
- Consegue calcular: "Nesta conversa de 2 horas, quantos tokens sobram para raciocínio?"
- Sabe identificar qual padrão de harness aplicar em qual situação

**Sinais de que a pessoa NÃO entendeu (preso no Nível 1):**
- Decora as definições mas não consegue aplicá-las a um caso novo
- Confunde "token budgeting" com "reduzir tamanho do prompt"
- Não consegue identificar os 3 problemas em um trace real
- Acha que "é só usar um modelo maior que resolve"

---

#### 🟡 Nível 2: Padrões Práticos (Semanas 3-4, ~6-8 horas de conteúdo)

**Objetivo:** APLICAR padrões que tornam agentes confiáveis

| Semana | Atividade | Entregável | Tempo Estimado |
|--------|-----------|------------|----------------|
| 3 | Ler `01-generator-evaluator-pattern.md` | Diagrama de fluxo G/E para feature KODA | 90 min |
| 3 | Ler `02-sprint-contracts.md` | Escrever 2 contratos para módulos KODA | 60 min |
| 3 | Ler `03-rubric-design.md` | Criar rubrica para 1 feature KODA | 60 min |
| 4 | Ler `04-trace-reading.md` | Analisar 1 trace real e diagnosticar | 60 min |
| 4 | Ler `nivel-2-koda.md` | Mapa de integração dos 4 padrões | 90 min |
| 4 | Fazer todos os exercícios do nível | Respostas + code review | 120 min |
| 4 | **Checkpoint Nível 2** | Prova + implementação de G/E funcional | 90 min |

**Sinais de que a pessoa ENTENDEU Nível 2:**
- Consegue desenhar um fluxo Generator/Evaluator do zero para um problema novo
- Sabe escrever um Sprint Contract que outro desenvolvedor consegue implementar sem ambiguidade
- Consegue criar uma rubrica com múltiplas dimensões e justificar os pesos
- Lê um trace de 50 linhas e identifica exatamente onde e por que algo falhou

**Sinais de que a pessoa NÃO entendeu (preso no Nível 2):**
- Implementa Generator/Evaluator mas o Evaluator é uma cópia do Generator com prompt diferente
- Contratos são vagos ("retorna produtos bons") em vez de específicos
- Rubricas têm pesos arbitrários sem justificativa
- Na leitura de trace, aponta sintomas em vez de causas raiz

---

#### 🔵 Nível 3: Arquitetura Avançada (Semanas 5-6, ~8-10 horas de conteúdo)

**Objetivo:** PROJETAR sistemas multi-agente sofisticados

| Semana | Atividade | Entregável | Tempo Estimado |
|--------|-----------|------------|----------------|
| 5 | Ler `01-multi-agent-systems.md` | Proposta de arquitetura multi-agente | 90 min |
| 5 | Ler `02-state-persistence.md` | Implementar state persistence funcional | 90 min |
| 5 | Ler `03-file-based-coordination.md` | Sistema de coordenação com arquivos | 90 min |
| 6 | Ler `04-server-side-compaction.md` | Plano de compaction para KODA | 60 min |
| 6 | Ler `05-harness-evolution.md` | Documento de evolução de harness | 60 min |
| 6 | Fazer exercícios + `nivel-3-koda.md` | Todos exercícios + aplicação KODA | 150 min |
| 6 | **Checkpoint Nível 3** | Prova + sistema multi-agente funcional | 120 min |

**Sinais de que a pessoa ENTENDEU Nível 3:**
- Consegue desenhar uma arquitetura com 3+ agentes coordenados, justificando boundaries
- Implementa state persistence que sobrevive a reinicializações do sistema
- Sabe quando usar file-based coordination vs message queues vs shared memory
- Consegue evoluir um harness existente sem quebrar compatibilidade

**Sinais de que a pessoa NÃO entendeu (preso no Nível 3):**
- Multi-agente system é essencialmente o mesmo agente chamado 3 vezes
- State persistence é um dump JSON sem estratégia de evolução
- File-based coordination sem locking strategy (condições de corrida)
- Harness evolution quebrando todos os contratos existentes

---

#### 🟣 Nível 4: KODA-Específico (Semanas 7-12, contínuo)

**Objetivo:** LIDERAR aplicação de todos os conceitos no KODA real

Este nível é fundamentalmente diferente. Não é sobre "completar leituras" — é sobre **produzir impacto real** no KODA.

| Fase | Atividade | Entregável | Duração |
|------|-----------|------------|---------|
| **Imersão** (Sem 7-8) | Estudar arquitetura KODA real | Mapa de componentes + flows | 2 semanas |
| **Diagnóstico** (Sem 9) | Identificar oportunidades de melhoria | Documento de findings com prioridades | 1 semana |
| **Implementação** (Sem 10-11) | Implementar 1-2 melhorias reais | PR merged no KODA | 2 semanas |
| **Mentoring** (Sem 12+) | Mentorar novos participantes | Sessões documentadas + feedback | Contínuo |

**Sinais de que a pessoa está PRONTA para Nível 4:**
- Já implementou pelo menos 1 padrão de Nível 2-3 em produção
- Consegue explicar a arquitetura KODA para um novo membro do time
- Já participou de pelo menos 2 code reviews de features KODA
- Tem confiança para propor mudanças arquiteturais com análise de trade-offs

---

### Visual Roadmap: A Trilha Completa

```
INÍCIO
  │
  ├─ SEMANA 1-2 ─────────────────────────────────────────────┐
  │  NÍVEL 1: FUNDAMENTOS                                     │
  │  ┌──────────────────────────────────────────────────┐    │
  │  │ 📖 Ler 3 módulos + 1 KODA application             │    │
  │  │ ✏️ Fazer exercícios                               │    │
  │  │ 🏁 Passar Checkpoint N1                          │    │
  │  └──────────────────────────────────────────────────┘    │
  │                          │                                │
  │                    ⬇️ Se aprovado                         │
  │                          │                                │
  ├─ SEMANA 3-4 ─────────────────────────────────────────────┤
  │  NÍVEL 2: PADRÕES PRÁTICOS                                │
  │  ┌──────────────────────────────────────────────────┐    │
  │  │ 📖 Ler 4 módulos + 1 KODA application             │    │
  │  │ 🔧 Implementar G/E + Contracts + Rubric + Trace   │    │
  │  │ 🏁 Passar Checkpoint N2                          │    │
  │  └──────────────────────────────────────────────────┘    │
  │                          │                                │
  │                    ⬇️ Se aprovado                         │
  │                          │                                │
  ├─ SEMANA 5-6 ─────────────────────────────────────────────┤
  │  NÍVEL 3: ARQUITETURA AVANÇADA                            │
  │  ┌──────────────────────────────────────────────────┐    │
  │  │ 📖 Ler 5 módulos + 1 KODA application             │    │
  │  │ 🏗️ Projetar sistema multi-agente                  │    │
  │  │ 🏁 Passar Checkpoint N3                          │    │
  │  └──────────────────────────────────────────────────┘    │
  │                          │                                │
  │                    ⬇️ Se aprovado                         │
  │                          │                                │
  └─ SEMANA 7-12 ────────────────────────────────────────────┘
     NÍVEL 4: KODA ESPECÍFICO
     ┌──────────────────────────────────────────────────┐
     │ 🔬 Diagnosticar KODA                              │
     │ 🚀 Implementar melhorias reais                    │
     │ 👥 Mentorar novos participantes                   │
     │ ♻️ Ciclo contínuo de melhoria                     │
     └──────────────────────────────────────────────────┘
```

---

## 🏁 Checkpoints e Critérios de Avanço

Checkpoints são momentos formais de verificação. Não são "provas" punitivas — são **conversas estruturadas** para confirmar que a pessoa está pronta para o próximo nível.

### Estrutura de um Checkpoint

Todo checkpoint segue este formato de 45 minutos:

```
MINUTO 0-5:   Aquecimento
              "Como foi sua experiência neste nível?"
              "O que foi mais difícil? O que foi mais interessante?"

MINUTO 5-15:  Verificação de Conceitos (oral)
              3-5 perguntas-chave sobre os conceitos do nível
              Pessoa explica em suas próprias palavras

MINUTO 15-30: Verificação Prática (code review ou whiteboard)
              Pessoa mostra implementação ou resolve problema novo
              Avaliador observa raciocínio, não apenas resultado

MINUTO 30-40: Feedback e Ajustes
              O que está sólido? O que precisa reforçar?
              Plano de ação para gaps identificados

MINUTO 40-45: Decisão
              ✅ Avançar para próximo nível
              ⚠️ Avançar com recomendações específicas
              🔄 Reforçar conceitos X, Y, Z antes de avançar
```

### Checkpoint Nível 1: Fundamentos

**Quando aplicar:** Após completar leituras + exercícios do Nível 1

**O que avaliar:**

| Critério | Como Verificar | Peso |
|----------|---------------|------|
| **Explica os 3 problemas** | Oral: "Me explica cada problema como se eu fosse um novo dev no time" | 30% |
| **Context Amnesia na prática** | Whiteboard: "Aqui está uma conversa de 3 horas. Em que minuto o contexto começa a degradar? Por quê?" | 25% |
| **Token Budgeting** | Cálculo: "Esta conversa tem X mensagens de Y tokens cada. Quanto contexto sobra para raciocínio no modelo Z?" | 25% |
| **Harness Patterns** | Oral: "Qual padrão você usaria para resolver [problema específico]? Por quê?" | 20% |

**Exemplo de perguntas do Checkpoint N1:**

1. "Um cliente reclama que KODA recomendou um produto com lactose mesmo ele tendo dito que é intolerante. Qual dos 3 problemas explica isso? Como você resolveria?"
2. "Desenhe no quadro como o contexto de uma conversa evolui ao longo de 4 horas. Em que ponto começa a ter 'context rot'?"
3. "Se cada mensagem do cliente tem ~200 tokens e cada resposta do KODA tem ~300 tokens, quantas mensagens cabem em Claude Sonnet (200K tokens) antes de começar a perder as primeiras?"
4. "Qual a diferença entre um harness pattern de validação e um de persistência? Dê exemplos de quando usar cada um."

**Rubrica de Avaliação — Checkpoint N1:**

```
EXCELENTE (9-10): Explica conceitos com exemplos próprios, faz cálculos 
                  corretos, identifica problemas em cenários novos.
                  
BOM (7-8):       Explica conceitos corretamente mas depende de exemplos 
                  do material. Cálculos OK com ajuda.
                  
SUFICIENTE (5-6): Entende os conceitos mas tem dificuldade em aplicá-los 
                   a cenários novos. Precisa reforçar 1-2 áreas.
                   
INSUFICIENTE (<5): Não consegue explicar os conceitos ou confunde 
                   problemas diferentes. Precisa refazer o nível.
```

---

### Checkpoint Nível 2: Padrões Práticos

**Quando aplicar:** Após completar leituras + exercícios + implementação prática do Nível 2

**O que avaliar:**

| Critério | Como Verificar | Peso |
|----------|---------------|------|
| **Generator/Evaluator funcional** | Code review: Implementação real de G/E para um problema | 30% |
| **Sprint Contracts** | Escrever contrato para módulo novo + validar contrato existente | 25% |
| **Rubric Design** | Criar rubrica com 4+ dimensões para feature KODA | 25% |
| **Trace Reading** | Analisar trace real, identificar root cause, propor fix | 20% |

**Exemplo de perguntas do Checkpoint N2:**

1. "Aqui está o código de um Generator que recomenda produtos. Ele funciona, mas a taxa de erro é 15%. Como você adicionaria um Evaluator para reduzir para <2%? Me mostre o código ou pseudocódigo."
2. "Este Sprint Contract está ambíguo: 'retorna lista de produtos relevantes'. Reescreva para que outro desenvolvedor consiga implementar sem fazer perguntas."
3. "Crie uma rubrica para avaliar recomendações de suplementos. Inclua pelo menos 4 dimensões. Justifique os pesos."
4. "Aqui está um trace de 2 minutos de uma recomendação que deu errado. O cliente recebeu um produto fora de estoque. Identifique exatamente em qual etapa o erro aconteceu e como prevenir."

**Rubrica de Avaliação — Checkpoint N2:**

```
EXCELENTE (9-10): G/E funcional com feedback loop, contratos sem 
                  ambiguidade, rubrica com pesos justificados, 
                  diagnóstico preciso de trace.
                  
BOM (7-8):       G/E funcional mas simples, contratos OK com pequenas 
                  ambiguidades, rubrica funcional, trace reading correto 
                  mas superficial.
                  
SUFICIENTE (5-6): G/E implementado mas sem feedback loop, contratos 
                   básicos, rubrica com 2-3 dimensões, trace reading 
                   identifica sintoma mas não causa.
                   
INSUFICIENTE (<5): G/E não funcional ou conceitualmente errado. 
                   Precisa refazer módulos específicos.
```

---

### Checkpoint Nível 3: Arquitetura Avançada

**Quando aplicar:** Após completar leituras + exercícios + projeto de arquitetura do Nível 3

**O que avaliar:**

| Critério | Como Verificar | Peso |
|----------|---------------|------|
| **Design multi-agente** | Whiteboard: Desenhar sistema com 3+ agentes para problema novo | 30% |
| **State Persistence** | Code review: Implementação com evolução de schema | 25% |
| **File-based Coordination** | Demonstrar: Sistema que coordena agentes via arquivos | 25% |
| **Harness Evolution** | Propor: Evoluir harness existente sem breaking changes | 20% |

**Exemplo de perguntas do Checkpoint N3:**

1. "Desenhe uma arquitetura para processar pedidos no KODA usando 4 agentes especializados. Como eles se comunicam? Como você lida com falhas parciais?"
2. "O state persistence do KODA hoje é um JSON simples. Proponha uma evolução que suporte versionamento de schema. Como você faz migration dos dados antigos?"
3. "Você tem 3 agentes que precisam coordenar acesso a um catálogo de produtos compartilhado. Desenhe a estratégia de locking usando arquivos."
4. "O harness atual do KODA valida 5 coisas. Você quer adicionar 3 novas validações sem quebrar os clientes existentes. Como?"

**Rubrica de Avaliação — Checkpoint N3:**

```
EXCELENTE (9-10): Arquitetura com boundaries claras, estratégia de 
                  coordenação robusta, schema versioning, evolução 
                  sem breaking changes.
                  
BOM (7-8):       Arquitetura funcional com pequenas fragilidades, 
                  coordenação OK, schema versioning básico.
                  
SUFICIENTE (5-6): Arquitetura conceitualmente correta mas com gaps 
                   de implementação. Precisa aprofundar 1-2 áreas.
                   
INSUFICIENTE (<5): Não consegue projetar sistema multi-agente. 
                   Precisa revisar conceitos fundamentais.
```

---

### Checkpoint Nível 4: Impact Review (Revisão de Impacto)

**Quando aplicar:** Após pelo menos 4 semanas no Nível 4, com evidências de aplicação prática

**Diferente dos checkpoints N1-N3:** O N4 não tem "completude". É um processo contínuo. O Impact Review avalia **maturidade e impacto**, não conhecimento teórico.

**O que avaliar:**

| Critério | Como Verificar | Peso |
|----------|---------------|------|
| **Produção: PRs com padrões** | Code review de PRs merged no KODA usando padrões do programa | 30% |
| **Diagnóstico: Trace Reading aplicado** | Demonstrar diagnóstico de bug real usando trace reading | 20% |
| **Arquitetura: Proposta de melhoria** | Documento de proposta arquitetural para o KODA com análise de trade-offs | 20% |
| **Mentoring: Contribuição para o time** | Evidência de mentoring efetivo (sessões documentadas, feedback positivo) | 20% |
| **Métricas: Impacto mensurável** | Melhoria demonstrável em métricas do KODA (erros, latência, satisfação) | 10% |

**Exemplo de perguntas do Impact Review:**

1. "Me mostra o PR mais significativo que você fez usando padrões do programa. Explique suas decisões de design."
2. "Pegue este bug real do KODA desta semana. Me mostre como você diagnosticaria usando trace reading."
3. "Se você pudesse mudar uma coisa na arquitetura do KODA hoje, o que seria? Justifique com trade-offs."
4. "Quem você mentorou? Me mostra uma sessão de mentoring que você conduziu. O que o participante aprendeu?"
5. "Qual métrica do KODA melhorou por causa do seu trabalho? Me mostre os dados."

**Rubrica de Avaliação — Impact Review:**

```
EXCELENTE (9-10): Múltiplos PRs em produção com impacto mensurável, 
                  mentoring ativo e eficaz, propostas arquiteturais 
                  sólidas, métricas KODA melhoraram.

BOM (7-8):       PRs em produção sólidos, mentoring ocasional, 
                  boas análises de trace, começa a propor melhorias.

SUFICIENTE (5-6): Pelo menos 1 PR em produção, participou de 
                   mentoring, consegue diagnosticar bugs, mas ainda 
                   não propõe arquitetura.

INSUFICIENTE (<5): Não aplicou padrões em produção, não mentorou, 
                   não consegue diagnosticar bugs complexos. 
                   Precisa focar em aplicação prática.
```

**Frequência:** O Impact Review é feito a cada 4-6 semanas no N4. Não é um "passa/não passa" — é uma conversa de calibração para manter o crescimento contínuo.

---

### Como Conduzir um Checkpoint Eficaz

#### Antes do Checkpoint

```
LÍDER:
□ Revisar exercícios da pessoa (já corrigidos)
□ Preparar 3-5 perguntas específicas baseadas nos gaps observados
□ Reservar 45 minutos ininterruptos
□ Ter material de referência à mão (mas não deixar a pessoa consultar 
  durante a parte de verificação de conceitos)

PARTICIPANTE:
□ Completar todas as leituras e exercícios
□ Fazer auto-avaliação (template na Seção 6)
□ Preparar 1 exemplo de aplicação prática
□ Trazer dúvidas específicas (não genéricas como "não entendi nada")
```

#### Durante o Checkpoint

**O que FAZER:**
- Criar ambiente de conversa, não de interrogatório
- Fazer perguntas abertas ("Me explica como se eu fosse novo no time")
- Pedir exemplos concretos ("Me mostra no código onde isso acontece")
- Investigar o raciocínio ("Por que você escolheu essa abordagem e não aquela?")
- Dar espaço para a pessoa pensar (silêncio é OK)

**O que NÃO FAZER:**
- Interromper com a resposta "correta" antes da pessoa terminar
- Fazer perguntas capciosas ou "pegadinhas"
- Comparar com outras pessoas ("A Ana entendeu isso em 2 dias")
- Apressar a decisão de avançar/reprovar

#### Após o Checkpoint

**Se AVANÇAR (✅):**
```
1. Registrar decisão no tracker da equipe
2. Compartilhar feedback positivo específico ("Seu entendimento de 
   token budgeting está excelente, especialmente o cálculo de overhead")
3. Recomendar materiais complementares opcionais
4. Agendar checkpoint do próximo nível (4-6 semanas depois)
```

**Se AVANÇAR COM RECOMENDAÇÕES (⚠️):**
```
1. Documentar exatamente quais áreas precisam de reforço
2. Criar mini-plano de ação (1-2 semanas)
3. Agendar follow-up rápido (15 min) para verificar melhorias
4. Pessoa pode começar próximo nível EM PARALELO com reforço
```

**Se REFORÇAR (🔄):**
```
1. Explicar com empatia: "Você está perto, mas [área X] precisa 
   de mais profundidade antes de avançar. Vamos focar nisso."
2. Criar plano de reforço específico:
   - Reler módulo Y
   - Fazer exercício adicional Z
   - Pair programming session sobre o tema
3. Reagendar checkpoint em 1-2 semanas
4. Oferecer suporte extra (mentoring, office hours)
```

---

### Sinais de Alerta: Quando Alguém Está "Preso"

Fique atento a estes indicadores de que alguém está tendo dificuldades:

| Sinal | O Que Pode Significar | Ação Recomendada |
|-------|----------------------|-----------------|
| **Evita fazer exercícios** | Medo de errar ou síndrome do impostor | Conversa 1:1, reforçar segurança psicológica, oferecer pair programming |
| **Faz exercícios mecanicamente** | Copiando soluções sem entender | Code review mais profundo, pedir para explicar cada linha |
| **Fica preso nos mesmos conceitos** | Gap de fundamento ou estilo de aprendizado | Mudar abordagem: se leu, tentar vídeo; se praticou, tentar explicar para outro |
| **Desiste fácil de exercícios difíceis** | Frustração ou sobrecarga | Quebrar exercício em partes menores, celebrar pequenas vitórias |
| **Pula para níveis avançados sem base** | Ansiedade ou pressão de performance | Reforçar que fundamentos são críticos, mostrar exemplos de falhas por pular etapas |
| **Isolamento (não pede ajuda)** | Orgulho ou medo de parecer incompetente | Criar cultura de "pedir ajuda é sinal de senioridade", normalizar dúvidas |

---

## 📊 Métricas de Progresso da Equipe

Métricas sem contexto são perigosas. Mas sem métricas, você não sabe se o programa está funcionando. Esta seção apresenta **métricas balanceadas** que medem aprendizado real sem criar ansiedade de performance.

### Os 4 Pilares de Métricas

```
┌──────────────────────────────────────────────────────────────────┐
│                    MÉTRICAS DE PROGRESSO                          │
├─────────────────┬────────────────────────────────────────────────┤
│ Pilar 1:        │ Mede completude. É a métrica mais visível      │
│ VELOCIDADE      │ mas também a mais perigosa se usada sozinha.   │
├─────────────────┼────────────────────────────────────────────────┤
│ Pilar 2:        │ Mede qualidade do aprendizado. É a métrica     │
│ COMPREENSÃO     │ mais importante para resultado de longo prazo. │
├─────────────────┼────────────────────────────────────────────────┤
│ Pilar 3:        │ Mede aplicação no mundo real. É a métrica      │
│ APLICAÇÃO       │ que conecta aprendizado a impacto no negócio.  │
├─────────────────┼────────────────────────────────────────────────┤
│ Pilar 4:        │ Mede colaboração. Time que aprende junto       │
│ ENGAJAMENTO     │ performa melhor que indivíduos isolados.       │
└─────────────────┴────────────────────────────────────────────────┘
```

---

### Pilar 1: Velocidade de Progressão

**O que medir:**

| Métrica | Definição | Meta | Alerta |
|---------|-----------|------|--------|
| **Tempo médio por nível** | Dias entre início e checkpoint aprovado | N1: 14d, N2: 21d, N3: 21d | >200% da meta |
| **% do time no prazo** | Pessoas dentro da estimativa de tempo | 70%+ | <50% |
| **Taxa de aprovação em 1ª tentativa** | % que passa checkpoint na primeira | 60%+ | <30% |
| **Dias desde última atividade** | Tempo sem ler/exercitar/praticar | <7 dias | >14 dias (abandono) |

**Como coletar:**
```
Team Progress Tracker (planilha ou dashboard):

| Pessoa  | Nível Atual | Início Nível | Checkpoint | Status    | Dias |
|---------|-------------|-------------|------------|-----------|------|
| Ana     | N3          | 2026-05-20  | 2026-06-10 | ⏳ cursando| 21   |
| Carlos  | N2          | 2026-05-15  | 2026-05-30 | ✅ aprovado| 15   |
| Pedro   | N1          | 2026-04-20  | --         | 🔄 reforço| 38   |
| Julia   | N1          | 2026-04-25  | 2026-05-25 | ✅ aprovado| 30   |
```

**Interpretação:**
- Ana está no prazo (21 dias para N3, dentro da meta de 21d)
- Carlos foi rápido (15 dias vs meta de 21d) — candidato a mentor
- Pedro está em reforço há 38 dias — **alerta vermelho**, precisa de intervenção
- Julia completou em 30 dias (vs meta de 14d) — um pouco lento, mas aprovado

---

### Pilar 2: Compreensão (Qualidade do Aprendizado)

**O que medir:**

| Métrica | Definição | Meta | Alerta |
|---------|-----------|------|--------|
| **Score médio em checkpoints** | Média dos scores nas rubricas de avaliação | 7.5+/10 | <5.0/10 |
| **% de respostas "excelente"** | Checkpoints com score 9+ | 30%+ | <10% |
| **Auto-avaliação vs avaliação real** | Gap entre o que a pessoa acha que sabe e o que demonstra | Gap < 1.5pts | Gap > 3pts |
| **Retenção em follow-up** | Score em quiz surpresa 4 semanas após checkpoint | 80%+ do score original | <60% |

**Como coletar — Rubrica de Compreensão por Nível:**

```
NÍVEL 1 — Rubrica de Compreensão:

DIMENSÃO 1: Explicação dos 3 problemas (peso 35%)
  10: Explica cada problema com exemplos próprios, conecta os 3
   7: Explica corretamente, mas usa exemplos do material
   4: Explica com imprecisões, confunde causas
   1: Não consegue explicar

DIMENSÃO 2: Token Budgeting prático (peso 25%)
  10: Calcula orçamento para qualquer cenário, explica trade-offs
   7: Calcula corretamente com ajuda
   4: Entende o conceito mas erra cálculos
   1: Não entende a relação tokens ↔ qualidade

DIMENSÃO 3: Identificação de problemas em cenários (peso 25%)
  10: Diagnostica corretamente em cenários novos e complexos
   7: Diagnostica em cenários similares aos do material
   4: Identifica sintomas mas não causas
   1: Não consegue diagnosticar

DIMENSÃO 4: Aplicação de harness patterns (peso 15%)
  10: Escolhe padrão correto e justifica com clareza
   7: Escolhe correto mas justificativa fraca
   4: Escolhe padrão por intuição, sem critério
   1: Não sabe qual padrão usar
```

**Interpretação:**
- Score 8.5/10 = compreensão sólida, pronto para avançar
- Score 6.0/10 = compreensão básica, avançar com recomendações
- Score 4.0/10 = gaps significativos, precisa reforçar
- Gap auto-avaliação vs real > 2pts = pessoa não tem clareza sobre o próprio aprendizado (treinar metacognição)

---

### Pilar 3: Aplicação Prática

**O que medir:**

| Métrica | Definição | Meta | Alerta |
|---------|-----------|------|--------|
| **Features implementadas** | PRs merged no KODA aplicando conceitos do programa | 1+/pessoa a partir N2 | 0 após 4 semanas no nível |
| **Qualidade das implementações** | Code review score das PRs (1-10) | 7.0+ | <5.0 |
| **Redução de erros** | Comparação de métricas KODA antes/depois da aplicação | Tendência positiva | Tendência negativa |
| **Iniciativa** | Propostas de melhoria originadas dos participantes | 1+/mês | 0 por 2 meses |

**Como coletar:**

```
Registro de Aplicações Práticas:

| Pessoa  | Data       | Feature/Tarefa               | Padrão Aplicado     | Impacto          |
|---------|------------|------------------------------|---------------------|------------------|
| Ana     | 2026-05-15 | Refatorar recomendacao       | Generator/Evaluator | Precisão +23%    |
| Carlos  | 2026-05-22 | Adicionar validacao pedido   | Rubric Design       | Erros -85%       |
| Carlos  | 2026-06-01 | Contratos entre modulos      | Sprint Contracts    | Bugs -70%        |
| Pedro   | --         | --                           | --                  | --               |
```

---

### Pilar 4: Engajamento e Colaboração

**O que medir:**

| Métrica | Definição | Meta | Alerta |
|---------|-----------|------|--------|
| **Sessões de mentoring realizadas** | Pair programming ou code review focado em aprendizado | 1/semana por pessoa | 0 em 2 semanas |
| **Contribuições em discussões** | Perguntas, respostas, insights compartilhados no canal | 2+/semana por pessoa | 0 em 1 semana |
| **Ajuda entre pares** | Vezes que alguém ajudou outro participante | Cultura de reciprocidade | Só sêniores ajudam |
| **Satisfação com o programa** | NPS do programa (survey mensal) | NPS > 50 | NPS < 0 |

---

### Dashboard de Progresso da Equipe (Template)

Use este template para acompanhar o time semanalmente:

```markdown
# Dashboard de Progresso — Semana X

## Visão Geral
- Total participantes: 8
- No prazo: 6 (75%)
- Em reforço: 2 (25%)
- Em risco de abandono: 0

## Progresso por Nível
| Nível | Pessoas | Completaram | Cursando | Não Iniciaram |
|-------|---------|-------------|----------|---------------|
| N1    | 8       | 7 (88%)     | 1 (12%)  | 0 (0%)        |
| N2    | 7       | 4 (57%)     | 3 (43%)  | 1 (--)*       |
| N3    | 4       | 1 (25%)     | 3 (75%)  | 4 (--)*       |
| N4    | 1       | 0 (0%)      | 1 (100%) | 7 (--)*       |

*Pessoas que ainda não chegaram neste nível

## Destaques da Semana
✅ Julia passou no Checkpoint N1 (score 8.5)
⚠️ Pedro em reforço N1 há 5 semanas — agendar intervenção
🔵 Carlos implementou Sprint Contracts em produção

## Ações Esta Semana
□ Checkpoint N2 com Carlos (quarta)
□ Sessão de mentoring: Pedro + Ana (terça)
□ Workshop: Trace Reading ao vivo (sexta)
```

---

### Métricas que NÃO devem ser usadas

Evite estas métricas — elas criam comportamentos disfuncionais:

| Métrica Tóxica | Por que Evitar |
|----------------|---------------|
| **"Linhas de código escritas"** | Incentiva quantidade sobre qualidade. Uma refatoração de 10 linhas pode valer mais que 500 linhas novas |
| **"Horas estudando"** | Não mede aprendizado. 30min focado > 3h disperso |
| **"Velocidade para completar"** (ranking) | Cria competição prejudicial. O objetivo é compreensão, não velocidade |
| **"% de exercícios corretos na 1ª tentativa"** | Desincentiva experimentação. Errar faz parte do aprendizado |
| **Comparação entre pessoas** | Destrói segurança psicológica. Cada pessoa tem sua jornada |

---

## 👥 Estratégias de Mentoring e Pair Programming

Mentoring eficaz não é sobre "fazer para a pessoa". É sobre **criar as condições para que ela aprenda sozinha**, com suporte.

### Os 4 Modos de Mentoring

```
┌─────────────────────────────────────────────────────────────────┐
│                    MODOS DE MENTORING                            │
├───────────────┬─────────────────────────────────────────────────┤
│ MODO 1:       │ A pessoa assiste você fazendo. Você narra seu   │
│ SHADOWING     │ raciocínio em voz alta. Ideal para expor a      │
│ (Sombreamento)│ padrões de pensamento que não estão no material. │
├───────────────┼─────────────────────────────────────────────────┤
│ MODO 2:       │ Você e a pessoa trabalham juntos no mesmo       │
│ PAIR          │ problema. Alternam entre "piloto" (quem escreve)│
│ PROGRAMMING   │ e "copiloto" (quem observa e questiona).        │
├───────────────┼─────────────────────────────────────────────────┤
│ MODO 3:       │ Você observa a pessoa trabalhando, faz perguntas│
│ GUIDED        │ para direcionar o raciocínio, mas não dá        │
│ PRACTICE      │ respostas prontas. Ideal para desenvolver        │
│               │ autonomia.                                      │
├───────────────┼─────────────────────────────────────────────────┤
│ MODO 4:       │ A pessoa trabalha sozinha e depois vocês revisam│
│ CODE REVIEW   │ juntos. Você foca em "por que" das decisões,    │
│               │ não apenas "o que" está certo/errado.           │
└───────────────┴─────────────────────────────────────────────────┘
```

### Quando Usar Cada Modo

| Situação | Modo Recomendado | Por Quê |
|----------|-----------------|---------|
| Pessoa é nova no conceito (nunca viu antes) | Shadowing | Precisa ver o processo mental completo antes de tentar |
| Pessoa leu o material mas não consegue aplicar | Pair Programming | Precisa de apoio lado a lado na primeira aplicação |
| Pessoa já aplicou mas comete erros | Guided Practice | Precisa desenvolver autonomia de diagnóstico |
| Pessoa já implementou e quer validação | Code Review | Precisa de feedback sobre decisões de design |
| Pessoa está travada em um bug específico | Pair Programming (focado) | Precisa de outro par de olhos e raciocínio |
| Pessoa completou nível e quer aprofundar | Code Review + Discussão | Precisa de desafios de nível superior |

---

### Estrutura de uma Sessão de Mentoring Eficaz (45 min)

```
MINUTO 0-5:   Alinhamento
              "O que você quer resolver hoje?"
              "O que você já tentou?"
              Definir objetivo específico da sessão

MINUTO 5-30:  Trabalho Focado (escolher modo)
              Shadowing / Pair / Guided Practice
              Regra de ouro: mentor NUNCA toca no teclado 
              durante Guided Practice

MINUTO 30-40: Reflexão
              "O que você aprendeu que não sabia antes?"
              "O que faria diferente na próxima vez?"
              "Qual foi o momento de 'aha!'?"

MINUTO 40-45: Próximos Passos
              "O que você vai fazer antes da próxima sessão?"
              Definir 1-3 ações concretas
              Agendar próxima sessão se necessário
```

---

### Técnicas de Perguntas para Mentoring

O segredo do mentoring eficaz está nas **perguntas**, não nas respostas.

**Perguntas para EXPOR RACIOCÍNIO:**
- "Me explica o que você está pensando agora?"
- "Por que você escolheu essa abordagem?"
- "Que alternativas você considerou e descartou?"
- "O que te fez descartar a alternativa X?"
- "Se você tivesse que explicar isso para alguém que nunca viu, como faria?"

**Perguntas para DESBLOQUEAR:**
- "O que você já tentou?"
- "Qual é a menor parte desse problema que você consegue resolver?"
- "Se não tivesse essa restrição, como faria?"
- "O que você sabe com certeza sobre este problema?"
- "Qual é a pergunta que você ainda não fez?"

**Perguntas para APROFUNDAR:**
- "O que aconteceria se [condição] fosse diferente?"
- "Como isso escala para 10x mais dados/tráfego/usuários?"
- "Qual edge case você não está considerando?"
- "Se isso falhasse em produção, qual seria o impacto?"
- "Como você testaria isso?"

**Perguntas para CONECTAR CONCEITOS:**
- "Isso te lembra algum padrão que você já viu?"
- "Como isso se relaciona com [conceito de nível anterior]?"
- "Se você aplicasse [padrão X] aqui, o que mudaria?"
- "Qual problema fundamental isso resolve (ou não resolve)?"

**O que EVITAR:**
- "Por que você não fez [solução correta]?" (julgamento)
- "Isso é fácil, olha..." (minimiza a dificuldade)
- "Deixa eu fazer pra você" (cria dependência)
- "Na minha época..." (desconecta da realidade atual)

---

### Pair Programming Focado em Aprendizado

Pair programming tradicional foca em **produtividade**. Pair programming para aprendizado foca em **transferência de conhecimento**.

**Protocolo para Pair Programming de Aprendizado:**

```
CONFIGURAÇÃO:
- Duração: 60-90 minutos (mais que isso = fadiga)
- Papéis: PILOTO (quem está aprendendo) e NAVEGADOR (mentor)
- Trocar papéis a cada 20-25 minutos
- PILOTO sempre começa (para não ficar só assistindo)

FASE 1: PILOTO = Participante, NAVEGADOR = Mentor (20-25 min)
  - Participante escreve código
  - Mentor faz perguntas, sugere caminhos, NÃO dita código
  - Mentor observa: onde a pessoa hesita? Onde comete erros?
  
FASE 2: PILOTO = Mentor, NAVEGADOR = Participante (20-25 min)
  - Mentor escreve código narrando raciocínio
  - Participante faz perguntas, questiona escolhas
  - Participante observa: como o mentor aborda o problema?
  
FASE 3: PILOTO = Participante, NAVEGADOR = Mentor (20-25 min)
  - Participante aplica o que aprendeu na Fase 2
  - Mentor observa se houve transferência de conhecimento
  - Foco: autonomia progressiva

DEBRIEF (10-15 min após a sessão):
  - O que aprendeu?
  - O que foi mais difícil?
  - O que vai praticar sozinho?
```

**Sinais de que o Pair Programming está funcionando:**
- Participante faz perguntas cada vez mais específicas
- Participante começa a antecipar problemas ("isso vai quebrar se...")
- Participante sugere abordagens alternativas
- Participante corrige o mentor ("não seria melhor...?")

**Sinais de que NÃO está funcionando:**
- Participante só copia o que o mentor faz
- Mentor dita código linha por linha
- Sessões são sempre no Modo Shadowing, nunca evoluem
- Participante não consegue reproduzir sozinho depois

---

### Plano de Mentoring por Nível

#### Mentoring para Nível 1 (Fundamentos)

**Foco:** Construir intuição sobre OS PROBLEMAS, não sobre soluções

**Atividades de mentoring típicas:**

1. **Shadowing de diagnóstico (45 min)**
   - Mentor pega um trace real do KODA
   - Narra o processo de identificar qual dos 3 problemas está ocorrendo
   - Mostra como diferenciar sintomas de causas

2. **Cálculo de token budget ao vivo (30 min)**
   - Mentor pega uma conversa real de WhatsApp
   - Mostra passo a passo: contar tokens, calcular overhead do system prompt, determinar espaço restante
   - Depois participante faz com outra conversa

3. **Quiz reverso (20 min)**
   - Participante cria perguntas sobre os 3 problemas para o mentor responder
   - Ensinar é a melhor forma de aprender
   - Mentor faz perguntas que expõem gaps

#### Mentoring para Nível 2 (Padrões Práticos)

**Foco:** Primeira implementação real dos padrões

**Atividades de mentoring típicas:**

1. **Pair programming: primeiro Generator/Evaluator (90 min)**
   - Escolher uma feature simples do KODA (ex: validar cupom)
   - Implementar juntos usando o protocolo de 3 fases
   - Foco: separação real de responsabilidades (não apenas 2 chamadas)

2. **Code review de contratos (45 min)**
   - Participante escreve 3 Sprint Contracts
   - Mentor revisa apontando ambiguidades
   - Refatorar juntos até ficarem "à prova de interpretação errada"

3. **Trace reading guiado (30 min)**
   - Mentor entrega um trace com um bug injetado
   - Participante diagnostica sozinho (Guided Practice)
   - Depois discutem: o que poderia ter sido feito diferente?

#### Mentoring para Nível 3 (Arquitetura Avançada)

**Foco:** Design de sistemas e decisões de arquitetura

**Atividades de mentoring típicas:**

1. **Whiteboard session: arquitetura multi-agente (60 min)**
   - Mentor propõe: "Como você faria um sistema de recomendação com 3 agentes?"
   - Participante desenha no quadro
   - Mentor faz perguntas que expõem trade-offs

2. **Code review arquitetural (45 min)**
   - Participante implementa state persistence
   - Mentor revisa com lente de "isso sobrevive a 6 meses de evolução?"
   - Discutir: schema versioning, migration, backward compatibility

3. **Simulação de falha (30 min)**
   - Mentor injeta falha no sistema de coordenação
   - Participante diagnostica e propõe solução
   - Discutir: o que mais poderia falhar?

---

### Cultura de Mentoring: Como Escalar

Não depende só de você (líder) mentorar todo mundo. Crie uma **cultura de mentoring**:

**Estratégia 1: Mentoring em Cadeia**
```
N4 (KODA Experts) mentoram N3
    N3 mentoram N2
        N2 mentoram N1
            N1 ajudam novos entrantes com onboarding

Cada pessoa tem 1 mentor e 1-2 mentorados
```

**Estratégia 2: Office Hours**
```
2x por semana, 1 hora
Qualquer pessoa pode aparecer com dúvidas
Formato: 15 min por pessoa, primeiro a chegar
Garantir que não vire "faz pra mim"
```

**Estratégia 3: Learning Logs Compartilhados**
```
Cada pessoa mantém um log de aprendizado (documento simples)
Compartilha semanalmente no canal:
  - O que aprendi esta semana
  - Onde travei
  - 1 insight que tive
  
Outros podem comentar, oferecer ajuda, compartilhar recursos
```

**Estratégia 4: Demo Fridays**
```
Sexta-feira, 30 min
1-2 pessoas mostram algo que implementaram
Foco: aprendizado, não perfeição
Plateia faz perguntas, sugere melhorias
```

---

## 📝 Templates de Avaliação

Esta seção contém templates prontos para usar. Copie, adapte e use no seu time.

### Template 1: Auto-Avaliação de Nível

Use este template ANTES do checkpoint. A pessoa preenche sozinha e envia para o avaliador.

```markdown
# Auto-Avaliação — [Nome] — Nível [X]

Data: ____/____/________

## Parte 1: Completude
- [ ] Li todos os módulos do nível? (Sim / Não — se não, quais faltam?)
- [ ] Fiz todos os exercícios? (Sim / Não — se não, quais faltam?)
- [ ] Fiz a aplicação KODA? (Sim / Não)

## Parte 2: Auto-Avaliação de Compreensão (1-10)

Para cada conceito-chave do nível, avalie sua compreensão:

| Conceito | Minha nota (1-10) | Evidência (o que eu sei fazer) |
|----------|-------------------|-------------------------------|
| [Conceito 1] | _/10 | |
| [Conceito 2] | _/10 | |
| [Conceito 3] | _/10 | |
| [Conceito 4] | _/10 | |

## Parte 3: Aplicação Prática

Descreva UMA aplicação prática que você fez:
- O que implementou?
- Qual conceito usou?
- Qual foi o resultado?
- O que faria diferente?

## Parte 4: Dificuldades

- O que foi mais difícil neste nível?
- Onde você travou?
- O que ajudou a destravar?

## Parte 5: Preparação para Próximo Nível

- Você se sente pronto para avançar? (Sim / Não / Talvez)
- Se não, o que falta?
- Que suporte você gostaria de ter no próximo nível?

## Parte 6: Feedback sobre o Programa

- O que está funcionando bem?
- O que pode melhorar?
- Sugestões para o material ou para o processo?
```

---

### Template 2: Rubrica de Avaliação por Nível

Use este template durante o checkpoint. Preencha durante ou imediatamente após.

```markdown
# Rubrica de Avaliação — Checkpoint Nível [X]

**Participante:** _________________  
**Avaliador:** _________________  
**Data:** ____/____/________  
**Decisão:** [ ] ✅ Avançar [ ] ⚠️ Avançar com recomendações [ ] 🔄 Reforçar

## Dimensões Avaliadas

| Dimensão | Peso | Score (1-10) | Ponderado | Evidência |
|----------|------|-------------|-----------|-----------|
| [Dimensão 1] | __% | _/10 | __ | |
| [Dimensão 2] | __% | _/10 | __ | |
| [Dimensão 3] | __% | _/10 | __ | |
| [Dimensão 4] | __% | _/10 | __ | |

**Score Total:** ___ / 10

## Pontos Fortes
1. 
2. 
3. 

## Oportunidades de Melhoria
1. 
2. 
3. 

## Recomendações Específicas
- [Ação 1]
- [Ação 2]
- [Ação 3]

## Plano de Ação (se ⚠️ ou 🔄)
| Ação | Responsável | Prazo | Status |
|------|------------|-------|--------|
| | | | |
| | | | |
| | | | |

## Follow-up Agendado?
Data: ____/____/________
```

---

### Template 3: Sessão de Mentoring

Use este template para preparar e documentar sessões de mentoring.

```markdown
# Sessão de Mentoring

**Mentor:** _________________  
**Participante:** _________________  
**Data:** ____/____/________  
**Duração:** ___ minutos  
**Modo:** [ ] Shadowing [ ] Pair Programming [ ] Guided Practice [ ] Code Review

## Antes da Sessão (preenchido pelo participante)

**O que quero resolver hoje:**
(Descreva o problema ou objetivo específico. Seja concreto.)

**O que já tentei:**
(Liste abordagens que já tentou e resultados)

**Onde estou travado:**
(Descreva exatamente o ponto de bloqueio)

**O que espero aprender:**
(Qual conhecimento ou habilidade quero desenvolver)

## Durante a Sessão (anotações)

**Insights / Momentos "Aha!":**
- 
- 

**Perguntas que surgiram:**
- 
- 

**Decisões tomadas:**
- 
- 

## Após a Sessão

**O que aprendi:**
(Em 2-3 frases, o principal aprendizado)

**O que farei diferente na próxima vez:**
(1-2 mudanças de abordagem)

**Próximos passos (ações concretas):**
1. [Ação 1] — Prazo: ___
2. [Ação 2] — Prazo: ___
3. [Ação 3] — Prazo: ___

**Próxima sessão:** ____/____/________ 

## Feedback do Mentor (preenchido pelo mentor)

**Progresso observado:**
- 

**Padrões de pensamento que precisam desenvolvimento:**
- 

**Sugestões para o participante:**
- 
```

---

### Template 4: Feedback de Code Review (Foco em Aprendizado)

Use este template para code reviews que têm objetivo primário de aprendizado.

````markdown
# Code Review — Foco em Aprendizado

**Autor:** _________________  
**Revisor:** _________________  
**Data:** ____/____/________  
**Contexto:** [Qual feature/tarefa? Qual conceito do programa está aplicando?]

## O que está bom (reforçar)
- [Ponto positivo 1 — seja específico: "A separação entre Generator e Evaluator está clara, especialmente..."]
- [Ponto positivo 2]
- [Ponto positivo 3]

## O que pode melhorar (desenvolver)

### Sugestão 1: [Título]
**Onde:** [Arquivo/linha ou conceito]  
**O que:** [Descrição específica do que pode melhorar]  
**Por quê:** [Explicação do princípio ou padrão por trás]  
**Exemplo:** [Se aplicável, mostre como ficaria]

    // Ao invés de:
    const resultado = await processarTudoDeUmaVez(pedido);

    // Considere:
    const plano = await gerarPlano(pedido);
    const resultado = await executarPlano(plano);
    const validacao = await validarResultado(resultado);

**Conceito relacionado:** [Qual conceito do programa isso ilustra?]

### Sugestão 2: [Título]
...

## Perguntas para Reflexão (não precisam ser respondidas agora)
1. [Pergunta que faz pensar sobre design]
2. [Pergunta que faz pensar sobre edge cases]
3. [Pergunta que conecta com outros conceitos]

## Conexões com o Programa
- Este código aplica: [Conceito X do Nível Y]
- Poderia também aplicar: [Conceito Z] — considere para versão futura
- Padrão similar visto em: [Módulo W, caso KODA]

## Próximos Passos
- [ ] [Ação concreta 1]
- [ ] [Ação concreta 2]
```

---

### Template 5: Learning Log Semanal

Use este template para o registro semanal de aprendizado.

```markdown
# Learning Log — [Nome] — Semana [X]

**Período:** ____/____ a ____/____  
**Nível Atual:** [N1/N2/N3/N4]  
**Tempo dedicado esta semana:** ___ horas

## O que aprendi esta semana
(2-3 bullet points com insights concretos)
- 
- 
- 

## O que apliquei na prática
(Se aplicou algo no KODA ou projeto paralelo)
- Feature/Problema: 
- Conceito aplicado: 
- Resultado: 

## Onde travei
(Se teve dificuldades)
- 
- 

## 1 Insight da Semana
(Uma frase — algo que "clicou" ou uma nova perspectiva)
> 

## Dúvidas para Office Hours
(Perguntas para levar para sessão de dúvidas)
- 
- 

## Plano para Próxima Semana
- [ ] 
- [ ] 
- [ ] 
```

---

## 🔄 Estratégias de Coordenação: Tabela Comparativa

Quando você está gerenciando um time aprendendo em velocidades diferentes, precisa de estratégias de **coordenação**. Esta tabela compara as principais abordagens.

### As 5 Estratégias de Coordenação de Aprendizado

```
┌──────────────────────────────────────────────────────────────────────────────┐
│               ESTRATÉGIAS DE COORDENAÇÃO DE APRENDIZADO                       │
├─────────────────┬──────────────────┬──────────────────┬──────────────────────┤
│ Estratégia      │ Como Funciona    │ Melhor Para       │ Cuidados             │
├─────────────────┼──────────────────┼──────────────────┼──────────────────────┤
│ COORTE FIXA     │ Todo mundo       │ Times pequenos   │ Os rápidos ficam     │
│ (Lockstep)      │ avança junto     │ (3-5 pessoas)    │ entediados. Os       │
│                 │ no mesmo ritmo   │ Conteúdo muito   │ lentos se sentem     │
│                 │                  │ novo para todos  │ pressionados.        │
├─────────────────┼──────────────────┼──────────────────┼──────────────────────┤
│ RITMO LIVRE     │ Cada pessoa      │ Times com        │ Pode criar ilhas de  │
│ (Self-Paced)    │ avança no seu    │ dispersão alta   │ conhecimento. Os     │
│                 │ próprio ritmo    │ de experiência   │ rápidos podem não    │
│                 │                  │                  │ ajudar os lentos.    │
├─────────────────┼──────────────────┼──────────────────┼──────────────────────┤
│ ONDAS           │ Todo mundo       │ Times médios     │ Requer coordenação   │
│ (Waves)         │ começa junto,    │ (5-10 pessoas)   │ para formar pares    │
│                 │ depois ritmo     │ Bom equilíbrio   │ de mentoria.         │
│                 │ livre com        │                  │                      │
│                 │ checkpoints      │                  │                      │
├─────────────────┼──────────────────┼──────────────────┼──────────────────────┤
│ TRILHAS         │ Caminhos         │ Times grandes    │ Complexidade de      │
│ (Tracks)        │ diferentes por   │ (10+) com        │ gestão. Pessoas em   │
│                 │ perfil (junior,  │ diversidade      │ trilhas diferentes   │
│                 │ pleno, senior)   │ de backgrounds   │ não interagem.       │
├─────────────────┼──────────────────┼──────────────────┼──────────────────────┤
│ EMBAIXADORES    │ Alguns fazem     │ Times que não    │ Embaixadores podem   │
│ (Ambassadors)   │ programa         │ podem parar      │ ficar sobrecarrega-  │
│                 │ completo, outros │ completamente    │ dos. Conhecimento    │
│                 │ aprendem via     │                  │ pode diluir.         │
│                 │ embaixadores     │                  │                      │
└─────────────────┴──────────────────┴──────────────────┴──────────────────────┘
```

### Análise Detalhada de Cada Estratégia

#### 1. COORTE FIXA (Lockstep)

**Mecanismo:** Todos começam o mesmo conteúdo na mesma semana. Avançam juntos. Ninguém vai para o próximo nível até todos completarem.

**Vantagens:**
- Máxima coesão de time — todos falam a mesma língua
- Discussões em grupo são muito ricas (todos no mesmo contexto)
- Fácil de gerenciar (um cronograma para todos)
- Pressão positiva dos pares (ninguém quer atrasar o grupo)

**Desvantagens:**
- Pessoas rápidas ficam frustradas (esperando)
- Pessoas lentas ficam ansiosas (segurando o grupo)
- Risco de nivelar por baixo (ritmo do mais lento)
- Não respeita diferenças individuais de aprendizado

**Quando usar:**
- Times pequenos (3-5 pessoas) com nível similar de experiência
- Conteúdo completamente novo para todos (ninguém tem vantagem)
- Primeira iteração do programa (para calibrar)

**Métricas para monitorar:**
- Variância de tempo de completude (se >50%, lockstep está prejudicando)
- Satisfação dos mais rápidos e dos mais lentos

---

#### 2. RITMO LIVRE (Self-Paced)

**Mecanismo:** Cada pessoa acessa o material e avança no seu próprio ritmo. Checkpoints são individuais.

**Vantagens:**
- Respeita diferenças individuais de aprendizado
- Pessoas rápidas não são seguradas
- Pessoas lentas não se sentem pressionadas
- Flexibilidade de horário (cada um estuda quando pode)

**Desvantagens:**
- Perda de coesão — pessoas em níveis diferentes não conseguem discutir
- Isolamento — pessoa pode passar semanas sem interagir com outros
- Difícil criar cultura de time (cada um por si)
- Sêniores podem "sumir na frente" e não ajudar

**Quando usar:**
- Times com grande dispersão de experiência (junior a staff)
- Pessoas com cargas horárias muito diferentes (part-time, fusos)
- Conteúdo que as pessoas já conhecem parcialmente

**Métricas para monitorar:**
- Tempo desde última atividade (abandono)
- Interações entre pessoas de níveis diferentes (colaboração)
- % de pessoas que chegam a N4 em 12 semanas

---

#### 3. ONDAS (Waves) ⭐ RECOMENDADO PARA KODA

**Mecanismo:** Todo mundo começa junto (Semana 1). As primeiras 2-3 semanas são em coorte. Depois o ritmo é livre, mas com checkpoints obrigatórios e sessões de integração semanais.

**Como funciona na prática:**

```
SEMANA 1-2 (Coorte):
  Todos no Nível 1 juntos
  Workshops coletivos, discussões em grupo
  Primeiro checkpoint em grupo (aprendizado coletivo)
  
SEMANA 3+ (Ritmo Livre com Sessões de Integração):
  Cada um avança no seu ritmo
  Toda sexta-feira: "Integration Hour" (1h)
    - 15 min: Alguém apresenta o que aprendeu
    - 15 min: Discussão de um problema real do KODA
    - 30 min: Pair programming cruzado (níveis diferentes)
    
  Checkpoints: individuais, mas compartilham-se aprendizados
```

**Vantagens:**
- Melhor dos dois mundos: coesão inicial + flexibilidade depois
- Integration Hour mantém cultura de time
- Pair programming cruzado acelera aprendizado (explica para outro = aprende mais)
- Sêniores naturalmente viram mentores nas sessões de integração

**Desvantagens:**
- Requer disciplina para manter Integration Hour (se pular 2 semanas, perde-se coesão)
- Pair programming cruzado precisa de facilitação (níveis muito diferentes podem frustrar)

**Quando usar:**
- Times de 5-10 pessoas (nosso caso no KODA)
- Quando há dispersão de experiência mas queremos manter cultura
- **Esta é a estratégia recomendada para o time KODA**

**Métricas para monitorar:**
- Presença nas Integration Hours (>80% = saudável)
- Qualidade das sessões de pair programming
- Progresso individual vs. coletivo

---

#### 4. TRILHAS (Tracks)

**Mecanismo:** Cria-se caminhos diferentes por perfil. Juniores têm uma trilha com mais exercícios e exemplos. Sêniores têm trilha acelerada.

**Exemplo:**
```
TRILHA JUNIOR:
  N1 (4 sem) → N2 (6 sem) → N3 (8 sem) → N4 básico
  + workshops extras de fundamentos
  + exercícios adicionais de reforço

TRILHA PLENO:
  N1 (3 sem) → N2 (4 sem) → N3 (5 sem) → N4 intermediário
  + exercícios padrão

TRILHA SENIOR:
  N1 (1 sem) → N2 (2 sem) → N3 (2 sem) → N4 avançado + mentoring
  + desafios de arquitetura
  + responsabilidade de mentorar
```

**Vantagens:**
- Conteúdo adaptado ao nível de cada pessoa
- Não frustra ninguém (nem muito fácil, nem muito difícil)
- Escala bem para times grandes

**Desvantagens:**
- Complexidade de gestão (3+ trilhas para manter)
- Pessoas em trilhas diferentes não interagem naturalmente
- Risco de criar "castas" (juniors se sentem inferiores)
- Manutenção do material é maior

**Quando usar:**
- Times grandes (10+ pessoas) com backgrounds muito diferentes
- Quando há orçamento para manter múltiplas trilhas

---

#### 5. EMBAIXADORES (Ambassadors)

**Mecanismo:** 2-3 pessoas fazem o programa completo. Elas se tornam "embaixadoras" e disseminam conhecimento para o resto do time através de workshops, code reviews e documentação.

**Vantagens:**
- Baixo custo (poucas pessoas fazem programa completo)
- Escala bem (embaixadores multiplicam conhecimento)
- Time não precisa parar completamente

**Desvantagens:**
- Conhecimento pode diluir na transmissão
- Embaixadores podem ficar sobrecarregados
- Time que não fez o programa pode não ter profundidade
- Dependência dos embaixadores (se saírem, conhecimento some)

**Quando usar:**
- Times que não podem dedicar 12 semanas ao programa
- Primeira iteração piloto do programa

---

### Matriz de Decisão: Qual Estratégia Usar?

| Critério | Coorte Fixa | Ritmo Livre | Ondas ⭐ | Trilhas | Embaixadores |
|----------|------------|-------------|---------|---------|-------------|
| **Tamanho do time** | 3-5 | 3-15 | 5-15 | 10+ | Qualquer |
| **Dispersão de experiência** | Baixa | Alta | Média-Alta | Muito Alta | Média |
| **Tempo disponível** | Dedicado | Variável | Misto | Misto | Mínimo |
| **Necessidade de coesão** | Alta | Baixa | Média-Alta | Baixa | Média |
| **Custo de gestão** | Baixo | Baixo | Médio | Alto | Médio |
| **Velocidade de aprendizado** | Média | Alta (rápidos) | Alta | Alta | Média |
| **Risco de isolamento** | Baixo | Alto | Baixo | Médio | Baixo |
| **Sustentabilidade** | Média | Alta | Alta | Média | Alta |
| **NOSSA RECOMENDAÇÃO** | — | — | ✅ KODA | — | Piloto inicial |

---

## 🏗️ Arquitetura de Aprendizado: O Sistema por Trás da Progressão

Um programa de aprendizado não é só conteúdo — é um **sistema**. Esta seção apresenta a arquitetura completa.

### Diagrama: O Sistema de Aprendizado

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SISTEMA DE APRENDIZADO — VISÃO ARQUITETURAL              │
│                                                                             │
│  ┌───────────────────────┐          ┌───────────────────────┐              │
│  │   INPUTS              │          │   PROCESSO CENTRAL    │              │
│  │                       │          │                       │              │
│  │ 👤 Participante       │          │  ┌─────────────────┐  │              │
│  │ ├─ Perfil (jr/pl/sr) │─────────▶│  │ CICLO DE        │  │              │
│  │ ├─ Disponibilidade   │          │  │ APRENDIZADO     │  │              │
│  │ └─ Background        │          │  │                 │  │              │
│  │                       │          │  │ 1. ESTUDAR     │  │              │
│  │ 📚 Conteúdo           │          │  │ (ler módulos)  │  │              │
│  │ ├─ Módulos por nível │─────────▶│  │      │         │  │              │
│  │ ├─ Exercícios        │          │  │      ▼         │  │              │
│  │ └─ Casos KODA        │          │  │ 2. PRATICAR    │  │              │
│  │                       │          │  │ (exercícios)   │  │              │
│  │ 🧠 Mentor             │          │  │      │         │  │              │
│  │ ├─ Sessões           │─────────▶│  │      ▼         │  │              │
│  │ ├─ Code reviews      │          │  │ 3. APLICAR     │  │              │
│  │ └─ Feedback          │          │  │ (código real)  │  │              │
│  │                       │          │  │      │         │  │              │
│  └───────────────────────┘          │  │      ▼         │  │              │
│                                     │  │ 4. VERIFICAR   │  │              │
│                                     │  │ (checkpoint)   │  │              │
│                                     │  └────────┬────────┘  │              │
│                                     │           │            │              │
│                                     │    ┌──────▼────────┐  │              │
│                                     │    │ LOOP DE       │  │              │
│                                     │    │ MELHORIA      │  │              │
│                                     │    │               │  │              │
│                                     │    │ AVANÇA? ──────┼──┼──▶ próximo   │
│                                     │    │ (sim)         │  │     nível    │
│                                     │    │               │  │              │
│                                     │    │ REFORÇA? ─────┼──┼──▶ revisitar │
│                                     │    │ (não)         │  │     módulos  │
│                                     │    └───────────────┘  │              │
│                                     └───────────────────────┘              │
│                                                                             │
│  ┌───────────────────────┐          ┌───────────────────────┐              │
│  │   MÉTRICAS &          │          │   OUTPUTS             │              │
│  │   MONITORAMENTO       │          │                       │              │
│  │                       │          │ ✅ Progressão         │              │
│  │ 📊 Dashboard time     │─────────▶│ ✅ Features no KODA   │              │
│  │ 📈 Métricas individuais│         │ ✅ Mentoria interna   │              │
│  │ 🚨 Alertas (travados) │          │ ✅ Cultura de aprend. │              │
│  └───────────────────────┘          └───────────────────────┘              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Componentes do Sistema

#### Componente 1: Ciclo de Aprendizado (Estudar → Praticar → Aplicar → Verificar)

Este é o motor do sistema. Inspirado no padrão Generator/Evaluator:

```
┌──────────────────────────────────────────────────────────────────┐
│               CICLO DE APRENDIZADO POR MÓDULO                     │
├────────────┬─────────────────────────────────────────────────────┤
│ 1. ESTUDAR │ Ler o módulo. Não é leitura passiva — fazer notas,  │
│            │ destacar conceitos, escrever perguntas.              │
│            │ Meta: Conseguir explicar o conceito para alguém.     │
├────────────┼─────────────────────────────────────────────────────┤
│ 2. PRATICAR│ Fazer exercícios do módulo. Tentar PRIMEIRO sem     │
│            │ consultar solução. Se errar, entender por quê.       │
│            │ Meta: 80%+ de acertos nos exercícios.               │
├────────────┼─────────────────────────────────────────────────────┤
│ 3. APLICAR │ Aplicar o conceito em código real (KODA ou projeto  │
│            │ paralelo). Não é exercício — é feature de verdade.   │
│            │ Meta: 1 PR merged aplicando o conceito.              │
├────────────┼─────────────────────────────────────────────────────┤
│ 4. VERIFICAR│ Checkpoint formal. Não é "prova" — é conversa para │
│            │ validar que o ciclo anterior foi eficaz.             │
│            │ Meta: Demonstrar compreensão + aplicação.            │
└────────────┴─────────────────────────────────────────────────────┘
```

#### Componente 2: Sistema de Suporte (Mentoring + Office Hours + Canal)

```
SUPORTE EM 3 CAMADAS:

CAMADA 1 — AUTO-SUFICIÊNCIA
  ├─ Material didático (módulos, exercícios, soluções comentadas)
  ├─ GLOSSARY.md (referência rápida de termos)
  └─ FAQ.md (perguntas comuns já respondidas)

CAMADA 2 — SUPORTE ENTRE PARES
  ├─ Canal #long-running-agents (perguntas, discussões)
  ├─ Learning Logs compartilhados
  └─ Pair programming entre participantes

CAMADA 3 — SUPORTE DE MENTORES
  ├─ Office Hours 2x/semana
  ├─ Sessões de mentoring 1:1
  └─ Code reviews focados em aprendizado
```

#### Componente 3: Sistema de Verificação (Checkpoints + Métricas)

```
VERIFICAÇÃO EM 3 NÍVEIS:

NÍVEL 1 — CONTÍNUA (diária/semanal)
  ├─ Exercícios auto-corrigidos
  ├─ Learning Logs semanais
  └─ Métricas de atividade (dias desde última ação)

NÍVEL 2 — POR MÓDULO (ao final de cada módulo)
  ├─ Quiz de compreensão (opcional, auto-aplicado)
  └─ Aplicação prática (mini-projeto)

NÍVEL 3 — POR NÍVEL (ao final do nível)
  ├─ Checkpoint formal (45 min)
  ├─ Rubrica de avaliação
  └─ Decisão de avanço
```

#### Componente 4: Sistema de Melhoria Contínua

```
FEEDBACK LOOPS:

LOOP 1 — INDIVIDUAL (semanal)
  Participante → Learning Log → Auto-reflexão → Ajuste de estratégia

LOOP 2 — MENTORIA (quinzenal)
  Mentor → Observação → Feedback → Participante ajusta abordagem

LOOP 3 — PROGRAMA (mensal)
  Time → Survey de satisfação → Análise de métricas → Ajustes no programa

LOOP 4 — CONTEÚDO (contínuo)
  Dúvidas recorrentes → Melhorias no material → Novos exemplos/exercícios
```

---

## 📋 Exercícios para Líderes

Antes de implementar este guia, pratique com estes exercícios. Eles simulam situações reais que você enfrentará liderando o programa.

### Exercício 1: Diagnóstico de Time

**Cenário:** Você recebeu o seguinte dashboard de progresso na Semana 6:

```
Time — Semana 6/12

Ana (Senior):     N3 — cursando — 14 dias no nível
Carlos (Pleno):   N2 — checkpoint ✅ aprovado (score 8.5)
Pedro (Junior):   N1 — 🔄 reforço — 42 dias no nível
Julia (Junior):   N1 — ✅ aprovado (score 7.0) — pronto para N2
Rafael (Senior):  N3 — cursando — 12 dias no nível
Mariana (Pleno):  N2 — ⚠️ avançou com recomendações — 28 dias
Bruno (Junior):   N1 — ✅ aprovado (score 8.0) — pronto para N2
```

**Perguntas:**

1. Quem está em situação crítica e precisa de intervenção imediata? Por quê?

2. Pedro está há 42 dias no Nível 1. Liste 3 possíveis causas e uma ação para cada uma.

3. Mariana avançou com recomendações. O que isso significa e como você faria o follow-up?

4. Julia (score 7.0) e Bruno (score 8.0) vão começar Nível 2. Como você estruturaria o suporte para eles, considerando que ambos são juniors?

5. Ana e Rafael estão no N3 em ritmo similar. Como você aproveitaria isso?

**Respostas esperadas:**

```
1. Pedro — 42 dias em reforço no N1. Já deveria ter completado em 14 dias.
   Está 3x acima da meta. Risco de abandono.

2. Possíveis causas para Pedro:
   a) Gap de fundamento (não tem base de LLMs) → Criar trilha de nivelamento
   b) Sobrecarga de outras tarefas → Negociar tempo dedicado com o manager
   c) Não está pedindo ajuda → Pair programming com Carlos (N2)

3. Mariana: avançou mas com gaps identificados. Follow-up:
   - Agendar check-in em 1 semana
   - Revisar áreas específicas apontadas no checkpoint
   - Ela pode começar N3 em paralelo enquanto reforça

4. Julia e Bruno no N2:
   - Começar com workshop conjunto de G/E
   - Pareá-los para exercícios iniciais
   - Designar Ana como mentora (N3, pode revisar código)
   - Checkpoints individuais para não criar comparação

5. Ana e Rafael no N3:
   - Podem fazer pair programming de arquitetura
   - Discutir designs juntos (debate melhora qualidade)
   - Um pode mentorar N2 enquanto outro foca em N3
   - Checkpoints separados mas discussões conjuntas
```

---

### Exercício 2: Preparação de Checkpoint

**Cenário:** Você vai conduzir um Checkpoint N2 para Carlos amanhã. Ele completou todos os módulos e exercícios. O auto-assessment dele mostra:

```
Auto-avaliação Carlos — Nível 2

Generator/Evaluator: 7/10 — "Entendo o conceito mas travei na implementação do feedback loop"
Sprint Contracts:    9/10 — "Fiz 3 contratos, todos funcionais"
Rubric Design:       8/10 — "Criei rubrica com 4 dimensões"
Trace Reading:       6/10 — "Consigo ler traces simples, complexos me confundem"
```

**Perguntas:**

1. Com base na auto-avaliação, quais áreas você deve focar mais durante o checkpoint?

2. Escreva 3 perguntas específicas que você faria para avaliar Trace Reading.

3. Escreva 3 perguntas para avaliar Generator/Evaluator focando no feedback loop (o ponto fraco dele).

4. Quanto tempo você alocaria para cada seção do checkpoint? Por quê?

5. Como você calibraria se o auto-assessment dele (6-9) corresponde à realidade?

**Respostas esperadas:**

```
1. Focar mais tempo em:
   - Trace Reading (auto-score 6, mais baixo)
   - Feedback loop do G/E (auto-score 7, mencionou dificuldade)
   - Sprint Contracts precisa de menos tempo (auto-score 9)

2. Perguntas para Trace Reading:
   a) "Aqui está um trace com 5 agentes interagindo. Em qual etapa 
      o erro foi introduzido? Como você sabe?"
   b) "Este trace mostra uma recomendação que foi rejeitada 2 vezes 
      e aprovada na 3ª. O que mudou entre as tentativas?"
   c) "Se você só tivesse o audit_log.jsonl e não os arquivos de 
      draft/verdict, o que você conseguiria diagnosticar? O que faltaria?"

3. Perguntas para G/E feedback loop:
   a) "No seu código, quando o Evaluator rejeita, como o Generator 
      recebe o feedback? Me mostra o fluxo completo."
   b) "O que acontece se o Generator ignorar o feedback e gerar 
      a mesma recomendação errada de novo?"
   c) "Como você evita loop infinito? Qual é o critério de parada?"

4. Alocação de tempo (45 min total):
   - Aquecimento: 5 min
   - Sprint Contracts: 5 min (área forte, validar rápido)
   - Rubric Design: 10 min (área média)
   - Generator/Evaluator: 15 min (área fraca, precisa de mais tempo)
   - Trace Reading: 10 min (área fraca, precisa de diagnóstico)

5. Calibração auto-assessment vs real:
   - Pedir para ele explicar conceitos em voz alta (não apenas definir)
   - Apresentar cenário novo (não do material) e ver performance
   - Sprint Contracts (9): se ele realmente domina, deve resolver 
     cenário novo em 2-3 minutos
   - Trace Reading (6): se ele está certo, vai hesitar em cenários 
     complexos — isso é esperado e OK
```

---

### Exercício 3: Planejamento de Mentoring

**Cenário:** Você é mentor de Julia (Junior, recém-chegada ao N2). Ela completou N1 com score 7.0 — entendeu os conceitos mas teve dificuldade em aplicá-los. Agora no N2, ela está lendo `01-generator-evaluator-pattern.md` e te mandou esta mensagem:

> "Li o módulo de Generator/Evaluator. Entendi a ideia: separar quem cria de quem avalia. Mas não consigo imaginar como implementar isso no KODA. Tentei começar o exercício e travei na primeira pergunta."

**Perguntas:**

1. Qual modo de mentoring você usaria para a primeira sessão com Julia? Justifique.

2. Estruture uma sessão de 60 minutos para ajudar Julia a destravar.

3. Que pergunta(s) você faria para diagnosticar ONDE exatamente ela travou?

4. Como você conectaria G/E com algo que ela já viu no N1 (Context Amnesia, Planning Collapse)?

5. Se após 3 sessões Julia continuar travada no mesmo ponto, qual seria seu próximo passo?

**Respostas esperadas:**

```
1. Modo: Guided Practice focado em G/E.
   Justificativa: Ela já leu (tem conceito), mas não consegue aplicar.
   Shadowing seria muito passivo. Pair Programming poderia virar 
   "faz pra mim". Guided Practice força ela a pensar.

2. Sessão de 60 min para Julia:

   MINUTO 0-5: Diagnóstico
   "Me explica com suas palavras o que é Generator/Evaluator."
   "O que especificamente te travou no exercício?"
   
   MINUTO 5-15: Conexão com N1
   "Lembra do Problema 3 (Self-Evaluation Collapse) do N1?"
   "G/E resolve exatamente isso. Vamos ver como..."
   Desenhar no quadro: agente único tenta se avaliar vs G/E
   
   MINUTO 15-35: Mini-implementação guiada
   "Vamos implementar um G/E para uma feature SIMPLES do KODA."
   Escolher: "Validar se um cupom de desconto é válido"
   Ela pilota. Você navega.
   Passo 1: Ela escreve o Generator (gera validação)
   Passo 2: Ela escreve o Evaluator (verifica validação)
   Passo 3: Ela conecta os dois
   
   MINUTO 35-45: Ela tenta sozinha
   "Agora tenta a primeira pergunta do exercício."
   Você observa em silêncio. Só intervém se 3+ min parada.
   
   MINUTO 45-55: Debrief
   "O que era difícil e ficou mais claro?"
   "O que você faria diferente?"
   
   MINUTO 55-60: Próximos passos
   "Termina o exercício 1 até quinta."
   "Me manda sua implementação para eu revisar."

3. Perguntas para diagnosticar:
   a) "Você consegue desenhar no quadro o fluxo: cliente pergunta → 
      KODA responde → onde entra Generator e onde entra Evaluator?"
      (Se não consegue: o conceito não está claro)
   b) "Sem escrever código, me explica: qual é a DIFERENÇA entre o que 
      o Generator faz e o que o Evaluator faz?"
      (Se confunde: não entendeu a separação de responsabilidades)
   c) "Se você tivesse que explicar G/E para o Pedro (que ainda está 
      no N1), como explicaria?"
      (Se não consegue simplificar: compreensão é superficial)

4. Conexão G/E com N1:
   "No N1, você aprendeu que agente não consegue se auto-avaliar 
   (Self-Evaluation Collapse). G/E é a SOLUÇÃO para esse problema.
   Pensa: em vez de KODA recomendar E verificar, a gente divide:
   um recomenda (Generator), outro verifica (Evaluator)."
   
   "Outra conexão: Planning Collapse (N1) acontece quando o agente 
   tenta planejar e executar ao mesmo tempo. G/E ajuda porque 
   separa as fases: Generator foca em uma coisa, Evaluator em outra."

5. Se após 3 sessões ainda travada:
   - Mudar de abordagem (ela pode aprender melhor com vídeos/exemplos)
   - Pedir para outro mentor tentar (estilos diferentes)
   - Verificar se o bloqueio é técnico OU emocional (síndrome do impostor?)
   - Criar exercício ainda mais simples (ex: G/E para "decidir se 
     um número é par ou ímpar" — remove complexidade do domínio KODA)
   - Se nada funcionar: conversa honesta sobre timing do programa
```

---

### Exercício 4: Métricas e Tomada de Decisão

**Cenário:** Você é Fernando, Tech Lead do KODA. O programa está na Semana 8. As métricas mostram:

```
MÉTRICAS — SEMANA 8

Progresso:
  Completaram N1: 8/8 (100%)
  Completaram N2: 5/8 (63%) — meta era 100%
  Completaram N3: 2/8 (25%) — meta era 60%
  Iniciaram N4:  1/8 (13%)

Compreensão (score médio em checkpoints):
  N1: 8.2/10
  N2: 7.1/10
  N3: 7.8/10

Aplicação prática:
  Features implementadas com padrões: 3
  Meta: 8 (1 por pessoa)

Engajamento:
  Presença em Integration Hours: 55% (meta: 80%)
  Sessões de mentoring/semana: 4 (meta: 8)

Satisfação (NPS do programa): +25 (mês 1: +45)

Custo:
  Horas dedicadas/semana (média por pessoa): 4.2h (meta: 5-7h)
```

**Perguntas:**

1. Esta semana, você tem 30 minutos na reunião de liderança. Que 3 pontos você apresentaria? Priorize.

2. O NPS caiu de +45 para +25. Liste 3 possíveis causas e investigações.

3. Apenas 55% de presença nas Integration Hours. O que você faria?

4. As pessoas estão dedicando 4.2h/semana em vez das 5-7h planejadas. Isso é um problema? Como abordar?

5. Você precisa decidir: estender o programa para 16 semanas ou manter 12 semanas com ajustes. Qual escolheria? Justifique com dados.

**Respostas esperadas:**

```
1. 3 pontos para liderança (30 min):

   PONTO 1 (10 min): Progresso abaixo da meta
   "N2 está em 63% vs meta de 100%. N3 em 25% vs 60%. 
   Causa raiz: tempo dedicado caiu de 6h para 4.2h/semana.
   Precisamos proteger o tempo do time."

   PONTO 2 (10 min): Impacto já visível no KODA
   "Apesar do atraso, 3 features já foram implementadas com 
   padrões do programa. Redução de 70% em erros nessas features.
   ROI é positivo — cada hora investida voltou em 3h de debug evitado."

   PONTO 3 (10 min): Plano de ação
   "Proponho: (1) reforçar proteção de horário, (2) ajustar 
   cronograma para 14 semanas, (3) celebrar as 3 features para 
   motivar o time. Peço apoio para blindar as manhãs de estudo."

2. Causas da queda de NPS (+45 → +25):

   a) Fadiga do programa (semana 8, cansados)
      → Investigar: survey qualitativo "o que está te cansando?"
   
   b) Frustração com ritmo (lentos se sentem pressionados, 
      rápidos se sentem segurados)
      → Investigar: NPS por perfil (junior vs senior)
   
   c) Desconexão com trabalho real ("não estou aplicando o que aprendo")
      → Investigar: quantas pessoas ainda não implementaram nada?

3. Plano para Integration Hours (55% → 80%):

   - Perguntar POR QUE as pessoas estão faltando (não presumir)
   - Se é horário: mover para horário melhor (votação)
   - Se é valor: tornar mais relevante (ex: debugging ao vivo de 
     um bug real do KODA que aconteceu naquela semana)
   - Se é sobrecarga: encurtar para 45 min
   - Não tornar obrigatório (nunca funciona)
   - Celebrar quem vai consistentemente

4. 4.2h vs 5-7h planejadas:

   É um problema SE:
   - Está abaixo do mínimo para progresso (parece que sim, dado 
     que N2 está 63% vs 100%)
   - Pessoas querem dedicar mais mas não conseguem
   
   Como abordar:
   - Identificar quem está sendo interrompido e por quê
   - Negociar com managers: "terça e quinta de manhã são sagrados"
   - Oferecer flexibilidade: se manhã não funciona, que seja 
     outro horário, mas que seja protegido
   - Não microgerenciar horas — focar em output (checkpoints), 
     não em input (horas)

5. Decisão: 16 semanas com ajustes

   Dados que suportam:
   - 4.2h/semana vs 5-7h planejadas (déficit de 30-40%)
   - N2 em 63% vs 100%, N3 em 25% vs 60%
   - NPS caindo (sinal de que pressão do prazo está piorando 
     qualidade da experiência)
   
   Ajustes:
   - Semanas 9-12: foco em N2-N3 (recuperar atraso)
   - Semanas 13-16: N4 inicial (priorizar quem chegar)
   - Reforçar proteção de horário
   - Celebrar progresso, não velocidade
   
   Por que não manter 12 semanas:
   - Completar no prazo com qualidade baixa é pior que completar 
     com qualidade alta em 16 semanas
   - O objetivo é aprendizado profundo, não velocidade
```

---

### Exercício 5: Conversa Difícil

**Cenário:** Bruno (Junior, N1 completo com score 8.0) começou N2 há 4 semanas. Ele não completou nenhum módulo. Não aparece nas Office Hours. O último Learning Log foi há 3 semanas. Você precisa ter uma conversa com ele.

**Perguntas:**

1. Como você abriria essa conversa? Escreva exatamente as primeiras 3 frases.

2. Liste 3 hipóteses sobre por que Bruno não está engajado. Para cada uma, como você investigaria?

3. Se Bruno disser "não estou conseguindo acompanhar, é muita coisa", qual seria sua resposta?

4. Se Bruno disser "não vejo valor nisso para o meu trabalho", como você responderia?

5. Em que momento você consideraria tirar Bruno do programa? Quais seriam os sinais?

**Respostas esperadas:**

```
1. Abertura da conversa:

   "Bruno, obrigado por reservar esse tempo. Queria conversar sobre 
   como está sendo o programa para você. Notei que você não postou 
   learning log nas últimas semanas e queria entender como posso 
   ajudar. Como você está se sentindo em relação ao N2?"

   Por que essa abertura:
   - Não acusatória ("notei" vs "você não fez")
   - Foco em ajudar, não cobrar
   - Pergunta aberta (ele pode responder qualquer coisa)
   - Tom de parceria, não de chefe

2. Hipóteses:
   
   a) Sobrecarga de trabalho
      → Perguntar: "Como está sua carga de tasks do KODA?"
      → Se confirmado: negociar com manager para proteger horário
   
   b) Não entendeu N2 e tem vergonha de pedir ajuda
      → Perguntar: "O que você achou do primeiro módulo de N2? 
         Me explica o que entendeu?"
      → Se confirmado: oferecer pair programming, normalizar dúvidas
   
   c) Perdeu motivação (não vê conexão com trabalho)
      → Perguntar: "Você consegue ver como G/E se aplica no que 
         você faz no dia a dia?"
      → Se confirmado: mostrar exemplos concretos no código que 
         ele mesmo trabalha

3. Resposta para "não estou conseguindo acompanhar":

   "Entendo. N2 é realmente mais denso que N1. Não é só você — 
   é normal levar mais tempo. Que tal a gente ajustar o plano?
   
   Opção A: Você foca em 2 módulos primeiro (G/E e Trace Reading), 
   deixando Contracts e Rubrics para depois. Assim o volume 
   diminui pela metade.
   
   Opção B: A gente faz pair programming nos módulos. Em vez de 
   você ler sozinho, a gente lê e implementa junto.
   
   Opção C: Você dá um pause de 1 semana, respira, e volta com 
   mais energia. Sem culpa.
   
   Qual dessas faz mais sentido para você?"

4. Resposta para "não vejo valor":

   "Justo. Me ajuda a entender melhor: quando você está debugando 
   um bug no KODA, quanto tempo você leva para encontrar a causa?
   
   [Ouve a resposta]
   
   O Trace Reading que a gente ensina em N2 foi feito exatamente 
   para reduzir esse tempo. A Ana, por exemplo, reduziu de 3 horas 
   para 30 minutos o diagnóstico de bugs na feature de recomendação.
   
   E o Generator/Evaluator? Lembra daquele bug de double discount 
   que deu problema em produção mês passado? G/E teria evitado 
   porque o Evaluator pegaria antes de ir para o cliente.
   
   Não quero te convencer. Mas quero que você experimente aplicar 
   UM padrão em UMA feature que você já conhece bem. Se não fizer 
   diferença, a gente conversa de novo. Topa tentar?"

5. Considerar tirar Bruno do programa quando:

   Sinais para considerar remoção:
   - 3+ conversas sem melhora de engajamento
   - Ele explicitamente diz que não quer continuar
   - Presença negativa está afetando outros (cinismo, desmotivação)
   - Já tentou 3 abordagens diferentes (pair programming, projeto 
     prático, redução de escopo) sem resultado
   
   Como abordar:
   "Bruno, parece que esse formato de programa não está funcionando 
   para você agora. Não tem problema nenhum. Que tal a gente pausar 
   sua participação e você voltar quando fizer mais sentido? 
   O material fica disponível. A porta está aberta."
   
   Importante: não é punição. É respeitar o momento da pessoa.
   Melhor pausar e voltar motivado do que continuar frustrado.
```

---

## 🔬 Casos Reais: Padrões que Emergiram em Times Reais

Esta seção documenta padrões observados em times que implementaram programas similares de aprendizado em IA. Os nomes são fictícios, mas as situações são baseadas em experiências reais.

### Caso 1: O Efeito "Sênior Acelerador"

**Time:** 12 pessoas, 3 sêniores, 5 plenos, 4 juniores
**Programa:** Similar ao nosso, 12 semanas

**O que aconteceu:**
Na semana 3, dois sêniores completaram N1 e N2 em tempo recorde (2 semanas cada). Eles entraram no N3 enquanto o resto do time ainda estava no N1.

**Problema:** Os juniores começaram a se sentir "lentos" e "burros". "Se o João fez em 2 semanas e eu estou há 4, devo ser incompetente." A ansiedade aumentou. Dois juniores consideraram desistir.

**Solução aplicada:**
1. Os sêniores foram redesignados como "mentores oficiais" em vez de "alunos avançados"
2. Eles pararam de reportar progresso público (para não criar comparação)
3. Criou-se um canal separado para os sêniores discutirem N3-N4
4. O discurso mudou: "João não é 'mais rápido', ele tem 8 anos de contexto que vocês estão construindo agora"

**Resultado:** Ansiedade caiu. Juniores voltaram a engajar. Sêniores desenvolveram habilidades de mentoria. O time ficou mais coeso.

**Lição para KODA:** Cuidado com visibilidade de progresso. O que motiva um sênior (velocidade) pode desmotivar um junior. Use trilhas ou pelo menos comunicação separada.

---

### Caso 2: O Programa Que Virou "Teatro"

**Time:** 8 pessoas, todos plenos/sêniores
**Programa:** 8 semanas, obrigatório

**O que aconteceu:**
A empresa determinou que o programa era obrigatório. Todo mundo "participava". Completavam leituras. Faziam exercícios. Passavam nos checkpoints.

Mas 6 meses depois, zero aplicação prática. Nenhuma feature nova usava os padrões. Nenhum código tinha sido refatorado.

**Diagnóstico:** O programa virou "teatro". As pessoas aprenderam a passar nos checkpoints sem aprender de verdade. Obrigatoriedade matou a motivação intrínseca.

**O que descobriram na retrospectiva:**
- "Eu lia o material na véspera do checkpoint"
- "Decorava as respostas dos exercícios"
- "Nunca tentei aplicar porque ninguém mais estava aplicando"
- "Era só mais uma tarefa para riscar da lista"

**Lição para KODA:** Não torne obrigatório. Foque em aplicação real. Se ninguém está aplicando, o programa falhou — mesmo que todos "passem" nos checkpoints.

---

### Caso 3: O Mentor Que Virou Gargalo

**Time:** 10 pessoas, 1 mentor (Tech Lead)
**Programa:** 12 semanas

**O que aconteceu:**
O Tech Lead era o ÚNICO mentor. Ele fazia todos os checkpoints, todas as sessões de pair programming, todos os code reviews.

Na semana 6, ele estava fazendo 25 horas/semana de mentoring — além das 40h de trabalho normal. Começou a ter burnout. A qualidade do mentoring caiu. Checkpoints passaram a ser superficiais. O time sentiu.

**Solução aplicada:**
1. Os primeiros 2 participantes que completaram N3 viraram mentores também
2. Criou-se um sistema de "mentoring em cadeia": N4 mentora N3, N3 mentora N2, N2 mentora N1
3. O Tech Lead passou a mentorar apenas os mentores (meta-mentoring)
4. Checkpoints passaram a ser feitos por qualquer pessoa 1 nível acima

**Resultado:** Carga do Tech Lead caiu de 25h para 5h/semana. Qualidade dos checkpoints melhorou (mais pessoas avaliando). Mentores ganharam experiência de liderança.

**Lição para KODA:** Você (Fernando) não pode ser o único mentor. Invista em formar mentores desde o início. A primeira pessoa a chegar em N3 já deve começar a mentorar.

---

### Caso 4: O Programa Que Morreu na Semana 8

**Time:** 6 pessoas, todos juniores/plenos
**Programa:** 12 semanas

**O que aconteceu:**
Tudo estava indo bem até a semana 7. Na semana 8, um projeto urgente surgiu. O time precisou dedicar 100% do tempo por 3 semanas. O programa foi pausado.

Depois das 3 semanas, ninguém voltou. O ímpeto se perdeu. "A gente volta na semana que vem" virou "mês que vem" virou "ano que vem".

**O que poderia ter sido diferente:**
1. **Mínimo viável:** Mesmo durante o projeto urgente, manter 1h/semana de Integration Hour
2. **Checkpoint de retorno:** Agendar data específica de retorno ("voltamos dia 15")
3. **Mini-metas:** Em vez de "pausar tudo", reduzir para 1 módulo a cada 2 semanas
4. **Accountability:** Cada pessoa declarar publicamente "quando voltar, vou terminar X"

**Lição para KODA:** O programa é frágil a interrupções. Se precisar pausar, tenha um plano de retorno. Manter 1h/semana é melhor que pausar completamente e perder o hábito.

---

## 🚀 Aplicação KODA: Como Este Guia se Aplica ao Nosso Contexto

Tudo que foi apresentado até agora é genérico — funciona para qualquer time aprendendo Long-Running Agents. Mas como aplicar **especificamente no time KODA**?

### Contexto do Time KODA

```
TIME KODA (exemplo representativo):

👤 Fernando (Tech Lead) — 8 anos exp, visão arquitetural
👤 Ana (Senior) — 5 anos exp, especialista em backend
👤 Carlos (Pleno) — 3 anos exp, fullstack
👤 Pedro (Junior) — 1 ano exp, foco em frontend/suporte
👤 Julia (Junior) — 6 meses exp, primeira experiência com IA
👤 Rafael (Senior) — 7 anos exp, especialista em infra/DevOps
👤 Mariana (Pleno) — 4 anos exp, dados e analytics
👤 Bruno (Junior) — 1.5 ano exp, backend

Total: 8 pessoas
Dispersão: Alta (de 6 meses a 8 anos de exp)
Tempo disponível: ~20% da semana (1 dia) dedicado ao programa
```

### Estratégia Recomendada para KODA: ONDAS (Waves)

Baseado no perfil do time, recomendamos a estratégia de **Ondas**:

**Fase 1: Coorte Inicial (Semanas 1-2)**
```
SEMANA 1:
  Segunda: Kickoff — todos juntos, 2h
    - Fernando apresenta visão do programa
    - Todos leem Nível 1 (01-why-agents-lose-plot.md) juntos
    - Discussão: "Onde vemos esses problemas no KODA hoje?"
  
  Quarta: Workshop — 1.5h
    - Cálculo de token budget ao vivo
    - Usar conversas REAIS do KODA como exemplo
  
  Sexta: Integration Hour — 1h
    - Cada pessoa compartilha 1 insight da semana
    - Quiz rápido em grupo (gamificado)

SEMANA 2:
  Segunda: Leitura coletiva Nível 1 (módulos 2 e 3)
  Quarta: Exercícios em duplas (pair programming)
    - Duplas: (Ana + Pedro), (Rafael + Julia), (Carlos + Bruno)
    - Sêniores não resolvem — guiam com perguntas
  Sexta: Checkpoint N1 em grupo
    - Não é individual ainda — é coletivo
    - Cada dupla apresenta 1 problema que resolveu
```

**Fase 2: Ritmo Livre com Integração (Semanas 3-12)**
```
ESTRUTURA SEMANAL:

Segunda-Quinta: Ritmo livre
  - Cada pessoa avança no seu ritmo
  - Sessões de mentoring agendadas individualmente
  - Office Hours: Terça 14h e Quinta 10h

Sexta-feira: Integration Hour (1h, obrigatório)
  14:00-14:10 — Check-in rápido (1 frase cada: "meu estado esta semana")
  14:10-14:25 — Showcase (1 pessoa apresenta algo que implementou)
  14:25-14:40 — Problem Solving (1 problema real do KODA em grupo)
  14:40-15:00 — Pair Programming Cruzado
    - Duplas rotativas a cada semana
    - Sênior com junior, pleno com pleno, etc.
```

### Plano de Mentoring para o Time KODA

```
ATRIBUIÇÕES INICIAIS DE MENTORING:

Fernando (N4) → mentora Rafael (N3) e Mariana (N2-N3)
  Foco: Visão arquitetural, decisões de design
  
Ana (N3-N4) → mentora Carlos (N2-N3) e Julia (N1-N2)
  Foco: Padrões práticos, implementação
  
Rafael (N3) → mentora Bruno (N1-N2)
  Foco: Infraestrutura, state persistence, coordenação

Carlos (N2) → mentora Pedro (N1)
  Foco: Fundamentos, primeiros exercícios
  (Carlos ganha experiência de mentoring; Pedro tem par mais próximo)

ROTAÇÃO:
  A cada 4 semanas, reavaliar atribuições
  Mentorar também é aprendizado — sêniores desenvolvem 
  habilidades de comunicação e liderança
```

### Calendário Típico para KODA

```
SEGUNDA:
  09:00-10:00 — Bloco de estudo (leitura)
  14:00-15:00 — Sessão de mentoring (agendada)

TERÇA:
  09:00-10:00 — Bloco de prática (exercícios)
  14:00-15:00 — Office Hours (aberto a todos)

QUARTA:
  09:00-10:00 — Bloco de aplicação (código KODA)
  14:00-15:00 — Sessão de mentoring (agendada)

QUINTA:
  09:00-10:00 — Bloco de estudo (leitura)
  10:00-11:00 — Office Hours (aberto a todos)

SEXTA:
  09:00-10:00 — Bloco de prática (exercícios)
  14:00-15:00 — Integration Hour (todos)
```

**Total: 5-7 horas/semana dedicadas ao programa (~20% da semana)**

### Exemplo Real: Semana Típica do Carlos (Pleno, Nível 2)

```
CARLOS — NÍVEL 2 — SEMANA 4

Segunda:
  09:00-10:00 — Leu módulo 03-rubric-design.md (45 min) + notas (15 min)
  14:00-15:00 — Mentoring com Ana: revisão da rubrica que ele criou
               para feature de recomendação. Ana apontou que a dimensão
               "preço" precisava considerar desconto de clube.

Terça:
  09:00-10:00 — Fez exercício 3 (Rubric Design). Respondeu 6/7 perguntas.
               Errou a Q4 (confundiu peso com threshold).
  14:00-14:30 — Office Hours: tirou dúvida sobre diferença peso vs threshold
               com Rafael, que explicou com um exemplo do KODA.

Quarta:
  09:00-10:30 — Aplicação prática: implementou rubrica na feature de
               recomendação do KODA. Submeteu PR.
  14:00-15:00 — Mentoring com Ana: pair programming na feature de
               Sprint Contracts para o módulo de busca.

Quinta:
  09:00-10:00 — Leu módulo 04-trace-reading.md.
  10:00-10:30 — Office Hours: discussão sobre trace reading com Julia
               (que está no N1) — Carlos explicou o básico, reforçando
               seu próprio aprendizado.

Sexta:
  09:00-10:00 — Fez atividade prática de Trace Reading. Acertou 5/5!
  14:00-15:00 — Integration Hour:
               - Showcase: Ana mostrou sistema multi-agente (N3)
               - Problem Solving: discutiram bug real do KODA
               - Pair Programming: Carlos (N2) + Pedro (N1) — Carlos
                 ajudou Pedro com exercício de token budgeting

Resultado da semana:
  ✅ 2 módulos completos
  ✅ 2 exercícios feitos
  ✅ 1 PR aberto (rubrica)
  ✅ 2 mentorings recebidos
  ✅ 1 mentoring dado (Pedro)
  ✅ 1 Integration Hour
  
  Progresso: N2 está 75% completo. Ritmo: dentro do esperado.
```

### Métricas KODA-Específicas

Além das métricas genéricas, monitore estas métricas específicas do KODA:

| Métrica KODA | O Que Mede | Meta |
|-------------|------------|------|
| **Novas features com padrões do programa** | Features implementadas usando G/E, Contracts, Rubrics | 2+/mês |
| **Redução de erros em features refatoradas** | Antes/depois de aplicar padrões | -70% erros |
| **Cobertura de rubricas** | % de features KODA com rubrica documentada | 80%+ |
| **Tempo de diagnóstico de bugs** | Tempo médio para identificar root cause | -50% vs antes |
| **Satisfação do cliente KODA** | NPS do cliente final (impacto indireto) | +10 pts |

### Plano de Implementação para Líderes KODA

```
ANTES DO PROGRAMA (1-2 semanas antes):
□ Definir estratégia de coordenação (recomendado: Ondas)
□ Atribuir pares iniciais de mentoring
□ Configurar canal #long-running-agents
□ Criar dashboard de progresso
□ Agendar Integration Hours (sextas, 14h)
□ Alinhar expectativas com cada pessoa (1:1 de 15 min)

DURANTE O PROGRAMA (semanalmente):
□ Atualizar dashboard de progresso (segunda)
□ Facilitar Integration Hour (sexta)
□ Verificar alertas (pessoas sem atividade >7 dias)
□ Rotacionar pares de pair programming

MENSALMENTE:
□ Survey de satisfação (NPS do programa)
□ Revisão de métricas: velocidade, compreensão, aplicação
□ Ajustes no programa baseado em feedback
□ Celebrar marcos (checkpoints aprovados, PRs merged)
```

---

## 🎯 O Que Você Aprendeu (Resumo)

Este guia cobriu 5 domínios essenciais para liderar o aprendizado de Long-Running Agents no seu time:

### 1. Roadmap de Progressão
Você tem um mapa claro de como cada pessoa deve progredir pelos 4 níveis, com expectativas realistas por perfil (junior/pleno/senior) e uma timeline de 12 semanas.

### 2. Checkpoints e Critérios de Avanço
Você sabe exatamente como avaliar se alguém está pronto para avançar — não por tempo, mas por **compreensão demonstrada**. Cada nível tem critérios específicos, perguntas de exemplo e rubricas de avaliação.

### 3. Métricas de Progresso
Você tem um sistema de métricas balanceado em 4 pilares: velocidade, compreensão, aplicação e engajamento. Sabe quais métricas coletar, como interpretá-las e — crucialmente — quais métricas **evitar** porque criam comportamentos disfuncionais.

### 4. Estratégias de Mentoring
Você domina os 4 modos de mentoring (Shadowing, Pair Programming, Guided Practice, Code Review), sabe quando usar cada um, e tem templates prontos para estruturar sessões produtivas.

### 5. Templates de Avaliação
Você tem 5 templates prontos para usar: auto-avaliação, rubrica de checkpoint, sessão de mentoring, code review focado em aprendizado e learning log semanal.

### Bônus: Estratégia KODA
Você tem uma recomendação concreta (Ondas/Waves) para o time KODA, com plano de implementação semana a semana, atribuições de mentoring e métricas específicas.

---

### A Mudança de Mindset

Mas além das ferramentas, este guia propõe uma **mudança de mindset** sobre liderar aprendizado técnico:

**De:** "Preciso garantir que todo mundo complete o programa no prazo."
**Para:** "Preciso criar as condições para que cada pessoa aprenda profundamente, no seu ritmo, com suporte."

**De:** "Checkpoint é uma prova para ver quem sabe e quem não sabe."
**Para:** "Checkpoint é uma conversa para entender onde a pessoa está e como ajudá-la a avançar."

**De:** "Mentoring é sobre transferir conhecimento."
**Para:** "Mentoring é sobre desenvolver autonomia — a pessoa aprende a aprender."

**De:** "Métricas são para cobrar resultados."
**Para:** "Métricas são para diagnosticar onde o sistema de aprendizado precisa melhorar."

---

## 🚀 Checkpoint: Você Está Pronto para Liderar?

Antes de implementar este guia, verifique:

- [ ] Consigo explicar as 5 estratégias de coordenação e justificar por que Ondas é recomendada para KODA
- [ ] Sei conduzir um checkpoint de 45 minutos sem que a pessoa se sinta "avaliada" negativamente
- [ ] Consigo identificar sinais de que alguém está "preso" e sei qual intervenção fazer
- [ ] Tenho clareza sobre quais métricas coletar e quais evitar
- [ ] Consigo estruturar uma sessão de mentoring no modo Guided Practice (o mais difícil)
- [ ] Sei usar os 5 templates deste guia
- [ ] Tenho um plano concreto para a primeira semana de implementação

Se respondeu "não" para qualquer item, revise a seção correspondente.

---

## ❓ Perguntas Frequentes (FAQ)

### P: "E se alguém simplesmente não consegue avançar — fica preso no mesmo nível por meses?"

**R:** Primeiro, investigue a causa raiz:
1. **Gap de fundamento?** A pessoa pode não ter os pré-requisitos. Considere uma trilha de nivelamento antes de continuar.
2. **Estilo de aprendizado?** Se leitura não funciona, tente vídeos, pair programming, projetos práticos.
3. **Sobrecarga?** A pessoa pode estar com outras demandas. Negocie tempo dedicado.
4. **Desmotivação?** O conteúdo pode não fazer sentido para o trabalho dela. Conecte com impacto real.
5. **Problema pessoal?** Às vezes o bloqueio não é técnico.

Se após 3 intervenções diferentes a pessoa não avança, tenha uma conversa honesta: "Este programa pode não ser o melhor formato para você agora. Que tal uma abordagem diferente?"

### P: "Como eu convenço a liderança a investir 20% do tempo do time nisso?"

**R:** Fale a língua deles — impacto no negócio:
- "Meta: features KODA implementadas com 70% menos erros (baseline: métricas atuais de erro)"
- "Meta: tempo de diagnóstico de bugs 50% menor que o baseline atual"
- "Estimativa: cada R$ 1 investido em aprendizado pode retornar R$ 3-5 em produtividade (baseado em programas similares)"
- "Meta: satisfação do cliente KODA subir 10 pontos NPS em 6 meses"

Use as métricas deste guia para construir seu caso de ROI com dados reais do time.

### P: "E se os sêniores não quiserem mentorar?"

**R:** Mentorar é uma habilidade que também se desenvolve. Argumentos:
1. **Crescimento de carreira:** Mentorar é competência de senior+ e staff
2. **Aprende-se mentorando:** Explicar conceitos solidifica seu próprio conhecimento
3. **Escala:** Se só você mentorar, o programa não escala
4. **Reconhecimento:** Destaque público para quem mentora bem

Se mesmo assim alguém resiste, não force. Comece com os voluntários e deixe o exemplo contagiar.

### P: "Como lidar com a pessoa que 'já sabe tudo' e quer pular níveis?"

**R:** Ofereça um **desafio de proficiência**: "Se você já domina Nível 1, responda estas 5 perguntas e implemente este mini-projeto em 2 horas."

Se a pessoa demonstrar domínio real, ótimo — ela avança rápido. Isso é saudável. O problema é quando a pessoa **acha** que sabe mas tem gaps.

O checkpoint existe exatamente para isso: validar compreensão real, não autopercepção.

### P: "O programa é obrigatório? E se alguém não quiser participar?"

**R:** Depende da cultura. Recomendamos:
- **Não tornar obrigatório** — aprendizado forçado não funciona
- **Tornar altamente recomendado** — conecte com crescimento de carreira
- **Mostrar valor** — as primeiras pessoas que fizerem vão naturalmente contagiar

Se alguém optar por não participar, respeite. Mas deixe a porta aberta para entrar depois.

### P: "12 semanas é muito tempo. Dá para acelerar?"

**R:** Dá, mas tem custos:
- **Programa intensivo de 6 semanas:** 40-50% do tempo dedicado. Funciona se o time pode parar outras atividades.
- **Programa mínimo de 4 semanas:** Apenas Níveis 1 e 2. Perde-se profundidade arquitetural.
- **Bootcamp de 1 semana:** Imersão total. Cansaço mental reduz retenção.

A recomendação é manter 12 semanas com 20% de dedicação. É sustentável e a retenção é maior.

### P: "Como sei se o programa como um todo está funcionando?"

**R:** Olhe para o conjunto de métricas, não para uma só:

**Sinais verdes (programa saudável):**
- 70%+ do time completa Nível 2 em 6 semanas
- Métricas de qualidade KODA melhoram (menos erros, diagnósticos mais rápidos)
- Pessoas naturalmente começam a mentorar outras
- Canal de discussão é ativo com perguntas de qualidade
- Participantes aplicam conceitos sem serem solicitados

**Sinais amarelos (precisa de ajustes):**
- 30-50% do time está com mais de 2 semanas de atraso
- Só sêniores estão engajados, juniors desapareceram
- Pessoas "completam" níveis mas não aplicam nada
- Feedback menciona "conteúdo bom, mas não tenho tempo"

**Sinais vermelhos (programa em risco):**
- 50%+ do time abandonou ou está inativo há >3 semanas
- Nenhuma aplicação prática foi feita
- Checkpoints viram "teatro" (todo mundo passa sem demonstrar)
- Liderança questiona o valor do programa

### P: "E depois que o time completa o programa? O que vem depois?"

**R:** O programa não termina — ele evolui:

1. **Nível 4 é contínuo:** Sempre há melhorias para fazer no KODA
2. **Novos entrantes:** Quando novas pessoas entram no time, as que já completaram mentoram
3. **Novos modelos:** Quando Claude 5, GPT-5 ou outros modelos surgirem, revisite o material
4. **Novos padrões:** A comunidade de AI engineering evolui rápido. Mantenha-se atualizado
5. **Cultura de aprendizado:** O objetivo final não é "completar o programa" — é criar uma cultura onde aprendizado contínuo é natural

---

## 📋 Metadata

| Campo | Valor |
|-------|-------|
| **Arquivo** | 02-team-progression-guide.md |
| **Nível** | Guia para Líderes (07 - Implementation Guides) |
| **Tempo** | 60 minutos (leitura) + aplicação contínua |
| **Status** | ✅ Completo |
| **Pré-requisitos** | README.md, MASTER_PLAN.md |
| **Público-alvo** | Tech Leads, Engineering Managers, Mentores |
| **Estratégia recomendada** | Ondas (Waves) para time KODA |
| **Atualizado** | Maio 2026 |

---

*Escrito com foco em aplicabilidade prática, empatia com a realidade de times de engenharia e respeito pelos diferentes ritmos de aprendizado.*  
*Memória: Este guia transforma o programa de "conteúdo estático" em "sistema vivo de aprendizado".*

---

**Próximo passo: Retorne ao `MASTER_PLAN.md` para visão geral do programa ou veja os templates em `templates/` para ferramentas complementares.**
