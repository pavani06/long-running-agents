---
title: "Case Study 3: KODA Continuous Improvement — 6 Meses de Evolução"
type: curriculum-case-study
nivel: 4
aliases: []
tags: [curriculo-conteudo, nivel-4, caso-de-estudo]
last_updated: 2026-06-10
---
# 🔄 Case Study 3: KODA Continuous Improvement — 6 Meses de Evolução
## Como Ciclos de Feedback, Simplificação de Harness e Rubrics Adaptativas Transformaram um Sistema Frágil em uma Plataforma que se Auto-Melhora

**Tempo Estimado:** 120-150 minutos
**Nível:** 4 — KODA-Específico
**Pré-requisitos:** Ter completado Nível 1 (Fundamentos), Nível 2 (Padrões Práticos), Nível 3 (Arquitetura Avançada) e os módulos 01-05 do Nível 4
**Status:** 🟢 COMPLETO — Estudo de caso de melhoria contínua e evolução de harness
**Data de Criação:** Maio 2026
**Dependências:** `05-harness-improvements.md`, `01-koda-architecture.md`, `04-evaluation-rubrics-koda.md`

---

## 📖 Prólogo: A Reunião que Mudou a Filosofia do KODA

**Janeiro 2026. Primeira segunda-feira do ano. Sala de guerra do KODA.**

Fernando olhou para as 14 pessoas ao redor da mesa. Engenheiros, product managers, o time de operações. Todos com café na mão e olheiras de fim de ano.

Na tela, um gráfico que ninguém queria ver:

```
Métrica de Qualidade do KODA — Janeiro 2026
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Precisão de Recomendações:     ████████░░  75%
Taxa de Resolução no Primeiro 
  Contato (FCR):               ██████░░░░  62%
Satisfação do Cliente (CSAT):  ███████░░░  70%
Tempo Médio de Conversa:       ██████████  2.4 horas
Custo por Conversa (tokens):   ██████████  $0.47
Falsos Positivos (promessas 
  quebradas):                  ████░░░░░░  38%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Fernando apontou para o número de falsos positivos.

> *"38%. Trinta e oito por cento das vezes que o KODA promete algo — entrega no mesmo dia, produto em estoque, preço válido — essa promessa é quebrada. Nós não estamos apenas perdendo dinheiro. Estamos treinando nossos clientes a não confiar no KODA."*

A sala ficou em silêncio.

O Tech Lead foi o primeiro a falar:
> *"Fernando, nós já tentamos de tudo. MVPs, refatorações, novos modelos. O que mais podemos fazer?"*

Fernando respirou fundo e disse a frase que redefiniria os próximos 6 meses:

> *"Nós não precisamos de mais features. Não precisamos de um modelo melhor. Nós precisamos de um **processo de melhoria contínua**. Um sistema que aprende com cada erro, que simplifica em vez de complicar, que evolui conforme os modelos evoluem. O KODA não pode ser um projeto que termina. Precisa ser uma plataforma que **se auto-melhora**."*

E assim começou a jornada de 6 meses de melhoria contínua do KODA.

Este case study documenta essa jornada completa: o diagnóstico inicial, os ciclos de feedback, a evolução das rubrics, a simplificação do harness, e as lições que transformaram o KODA de um sistema que "quebrava menos" para um sistema que "melhora sozinho".

---

## 🎯 Objetivos Deste Case Study

Ao final deste case study, você será capaz de:

- ✅ **Desenhar um sistema de melhoria contínua** para agentes de IA, com ciclos de feedback, métricas e processos de ajuste
- ✅ **Implementar rubrics adaptativas** que evoluem conforme os modelos melhoram e os padrões de qualidade sobem
- ✅ **Identificar quando simplificar o harness** — removendo componentes que se tornaram desnecessários conforme os modelos evoluíram
- ✅ **Construir um dashboard de métricas trimestrais** que mostre progresso real, não métricas de vaidade
- ✅ **Criar ciclos de feedback que realmente funcionam** — do cliente ao código, sem gaps de informação
- ✅ **Aplicar o padrão de Harness Evolution** (Nível 3) em um sistema de produção com usuários reais
- ✅ **Tomar decisões de arquitetura baseadas em dados**, não em intuição ou hype de novos modelos
- ✅ **Liderar uma cultura de melhoria contínua** em times de AI engineering

---

## 📊 Contexto Inicial: O KODA em Janeiro de 2026

### Baseline de Métricas

Antes de começar qualquer iniciativa de melhoria, o time estabeleceu uma baseline precisa. Sem baseline, melhoria é opinião.

| Métrica | Janeiro 2026 | Alvo (Junho 2026) | Significado |
|---------|-------------|-------------------|-------------|
| **Precisão de Recomendações** | 75% | 95% | % de recomendações corretas (estoque, preço, adequação ao perfil) |
| **First Contact Resolution (FCR)** | 62% | 85% | % de conversas resolvidas sem escalar para humano |
| **CSAT (Customer Satisfaction)** | 70% | 90% | Nota média de satisfação pós-compra |
| **Tempo Médio de Conversa** | 2.4h | 1.2h | Duração média até conclusão da compra |
| **Custo por Conversa (tokens)** | $0.47 | $0.22 | Custo médio em tokens por conversa completa |
| **Falsos Positivos** | 38% | 5% | % de promessas quebradas (estoque, entrega, preço) |
| **Taxa de Devolução** | 15% | 5% | % de produtos devolvidos por insatisfação |
| **Churn Mensal** | 8% | 2% | Clientes que abandonam KODA |
| **Tempo de Debug (MTTD)** | 4.2h | 30min | Tempo médio para diagnosticar raiz de um incidente |
| **Cobertura de Testes de Harness** | 12% | 80% | % de cenários cobertos por validação automatizada |

### Estado do Harness — Janeiro 2026

O harness do KODA em janeiro era o que o time chamava de "frankenharness" — um conjunto de componentes acumulados ao longo de 8 meses, sem design coeso:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                 KODA HARNESS — JANEIRO 2026 (DIAGNÓSTICO INICIAL)           │
└─────────────────────────────────────────────────────────────────────────────┘

                              ┌──────────────────────┐
                              │    CLIENTE (WhatsApp) │
                              └──────────┬───────────┘
                                         │
                              ┌──────────▼───────────┐
                              │    KODA CORE          │
                              │  (Single Agent +      │
                              │   20+ tools Zod)      │
                              └──────────┬───────────┘
                                         │
          ┌──────────────────────────────┼──────────────────────────────┐
          │                              │                              │
┌─────────▼─────────┐        ┌──────────▼──────────┐       ┌───────────▼─────────┐
│  PROMPT ÚNICO     │        │  CACHE MANAGER      │       │  PROMPT TEMPLATES   │
│  + TOOLS          │        │  (MVP2 legado)      │       │  (15 versões        │
│                   │        │                     │       │   diferentes!)      │
│  Planner,         │        │  Worker 15min       │       │                     │
│  Generator,       │        │  promessas.json     │       │  Nunca limpas       │
│  Evaluator         │        │  Ineficaz           │       │  Inconsistentes     │
│  TUDO no mesmo    │        │                     │       │                     │
│  agente           │        │                     │       │                     │
└─────────┬─────────┘        └──────────┬──────────┘       └───────────┬─────────┘
          │                              │                              │
          └──────────────────────────────┼──────────────────────────────┘
                                         │
                         ┌───────────────┼───────────────┐
                         │               │               │
               ┌─────────▼─────────┐ ┌───▼──────────┐ ┌─▼──────────────┐
               │   PERSISTÊNCIA    │ │  COORDENAÇÃO │ │  TELEMETRIA    │
               │   (EXISTENTE!)    │ │  (PARCIAL)   │ │  (BÁSICA)      │
               │                   │ │              │ │                │
               │ PostgreSQL+Redis  │ │ Redis locks  │ │ StageTimings   │
               │ Prisma            │ │ em alguns    │ │ mas sem        │
               │ User/Cart/Order/  │ │ fluxos       │ │ audit trail    │
               │ Memories/Context   │ │              │ │ completo       │
               │                   │ │ Race cond    │ │                │
               │ + MemoryExtractor │ │ em carrinho  │ │ Custo invisível│
               │ + Cache Redis     │ │ documentada  │ │                │
               └───────────────────┘ └──────────────┘ └────────────────┘

PROBLEMAS IDENTIFICADOS:
━━━━━━━━━━━━━━━━━━━━━
1. KODA opera como single agent + tools, não como equipe coordenada
   (Planner, Generator, Evaluator colapsados no mesmo prompt)
2. Avaliador ausente como agente independente — sem sycophancy protection
3. Truncamento de histórico sem compactação crítica
   (60 msg WhatsApp + 20 API, mas sem resumo curado)
4. Coordenação frágil em carrinho (race condition documentada)
5. Audit manifest ausente — traces com timings mas sem cadeia completa
   de decisão (input → tools → output → decisão)
6. Custo invisível — sem tracking de tokens por componente, ROI por camada
7. 15 versões de prompt templates diferentes (cada dev usava o seu)
8. Componentes legados de MVPs ainda ativos (Cache Manager do MVP2)
9. Timings existem (StageTimings) mas sem replay completo da decisão
```

### A Decisão que Mudou Tudo

Naquela reunião de janeiro, Fernando propôs algo radical:

> *"Pelos próximos 6 meses, nós não vamos adicionar NENHUMA feature nova ao KODA. Zero. Nosso único objetivo é melhorar o que já existe. Vamos tratar o KODA como um paciente que precisa de fisioterapia, não de mais cirurgias."*

A proposta foi recebida com desconforto. O time de produto tinha 12 features no backlog. O CEO queria expansão para novas categorias. Mas Fernando insistiu:

> *"Se o KODA quebra 38% das promessas, adicionar features é como construir um segundo andar em cima de uma fundação rachada. Primeiro consertamos a fundação. Depois construímos."*

O CEO aprovou. E assim nasceu o programa **KODA Continuous Improvement (KCI)** — 6 meses, 2 trimestres (Q1 e Q2 de 2026), 1 objetivo: transformar o KODA em uma plataforma que se auto-melhora.

---

## 📅 A Jornada de 6 Meses: Timeline Completa

### Visão Geral dos Trimestres

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                     KCI — KODA CONTINUOUS IMPROVEMENT                        │
│                        Timeline de 6 Meses                                   │
└──────────────────────────────────────────────────────────────────────────────┘

JANEIRO 2026                    ABRIL 2026                    JUNHO 2026
    │                               │                            │
    ├───────────────┬───────────────┼───────────────┬────────────┤
    │               │               │               │            │
    ▼               ▼               ▼               ▼            ▼

┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│  MÊS 1-2 │   │  MÊS 3   │   │  MÊS 4   │   │  MÊS 5   │   │  MÊS 6   │
│          │   │          │   │          │   │          │   │          │
│ DIAGNÓS-│──▶│ CICLOS DE│──▶│ RUBRICS  │──▶│ SIMPLIFI-│──▶│ CULTURA  │
│ TICO &  │   │ FEEDBACK │   │ ADAPTA-  │   │ CAÇÃO DO │   │ DE ME-   │
│ BASELINE│   │          │   │ TIVAS    │   │ HARNESS  │   │ LHORIA   │
└──────────┘   └──────────┘   └──────────┘   └──────────┘   └──────────┘
     │               │               │               │            │
     ▼               ▼               ▼               ▼            ▼
  Medir tudo     Feedbacks      Rubrics que     Remover o     Processo
  que existe     do cliente     aprendem       que não        que roda
  sem mudar      → código      sozinhas       serve mais     sozinho
```

### Mês 1-2 (Janeiro-Fevereiro 2026): Diagnóstico & Baseline

**Objetivo:** Entender exatamente o que estava quebrado, com dados, não com opiniões.

#### Semana 1-2: Auditoria Completa do Sistema

O time realizou uma auditoria de cada componente do KODA:

| Componente | Status | Problema Principal | Ação Recomendada |
|------------|--------|-------------------|-----------------|
| **Validator V1** | 🟡 Legado | 3 chamadas API sequenciais, latência 5.8s, dados de cache desatualizados | Substituir por Evaluator dedicado |
| **Cache Manager (MVP2)** | 🔴 Obsoleto | Worker de 15min ineficaz, não previne problemas reais | Remover |
| **Prompt Templates** | 🔴 Caótico | 15 versões diferentes, ninguém sabe qual é a correta | Padronizar em 4 templates versionados |
| **Estado (RAM)** | 🔴 Crítico | Perda total em restart, sem persistência | Migrar para SQLite + JSON fallback |
| **Auto-Avaliação** | 🔴 Crítico | KODA avalia o próprio output, viés de sycophancy | Implementar Generator/Evaluator |
| **Rerouter (MVP3)** | 🟡 Legado | Funciona, mas cria race conditions e latência em cascata | Substituir por Planner com locks |
| **Trace/Logs** | 🔴 Inexistente | Impossível debugar decisões do agente | Implementar audit trail JSONL |
| **Métricas** | 🟡 Básico | Métricas de vaidade (uptime, mensagens/dia), zero qualidade | Implementar métricas de qualidade real |

#### Semana 3-4: Implementação da Telemetria

Antes de mudar qualquer coisa, o time precisava **ver** o que estava acontecendo. Implementaram:

```
SISTEMA DE TELEMETRIA — FEVEREIRO 2026
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

┌─────────────────────────────────────────────────────────────────────────────┐
│                         TELEMETRY PIPELINE                                   │
└─────────────────────────────────────────────────────────────────────────────┘

  AGENTE KODA
       │
       ├──▶ event: "message_received"      { ts, customer_id, intent }
       ├──▶ event: "recommendation_start"  { ts, context_size_tokens }
       ├──▶ event: "api_call"              { ts, endpoint, latency_ms, cached }
       ├──▶ event: "recommendation_done"   { ts, products_recommended, confidence }
       ├──▶ event: "promise_made"          { ts, promise_type, eta, conditions }
       ├──▶ event: "customer_action"       { ts, action: purchase|cancel|complaint }
       └──▶ event: "promise_broken"        { ts, promise_id, reason }

       │
       ▼
  ┌─────────────────────────────────────────────────────────────────┐
  │                     TELEMETRY STORE (SQLite)                     │
  │                                                                 │
  │  events table:                                                  │
  │  ┌──────────┬──────────┬──────────┬──────────┬──────────┐      │
  │  │ ts       │ event    │ data     │ session  │ cost_usd │      │
  │  ├──────────┼──────────┼──────────┼──────────┼──────────┤      │
  │  │ 14:32:01 │ msg_rcv  │ {...}    │ sess_901 │ $0.002   │      │
  │  │ 14:32:03 │ rec_start│ {...}    │ sess_901 │ $0.001   │      │
  │  │ 14:32:05 │ api_call │ {...}    │ sess_901 │ $0.005   │      │
  │  │ 14:32:08 │ rec_done │ {...}    │ sess_901 │ $0.008   │      │
  │  │ 14:32:09 │ prom_made│ {...}    │ sess_901 │ $0.001   │      │
  │  └──────────┴──────────┴──────────┴──────────┴──────────┘      │
  └─────────────────────────────────────────────────────────────────┘
       │
       ▼
  ┌─────────────────────────────────────────────────────────────────┐
  │                     METRICS DASHBOARD                            │
  │                                                                 │
  │  REAL-TIME:                                                     │
  │  • Latência p95 por endpoint                                    │
  │  • Taxa de cache hit/miss                                       │
  │  • Tokens consumidos por conversa                               │
  │  • Custo acumulado (USD) por hora                               │
  │                                                                 │
  │  DIÁRIO:                                                        │
  │  • Precisão de recomendações                                    │
  │  • FCR (First Contact Resolution)                               │
  │  • Promessas quebradas / total de promessas                     │
  │  • Tempo médio até debug (MTTD)                                 │
  │                                                                 │
  │  SEMANAL:                                                       │
  │  • CSAT (Customer Satisfaction)                                 │
  │  • Taxa de devolução                                            │
  │  • Churn semanal                                                │
  │  • Custo operacional total                                      │
  └─────────────────────────────────────────────────────────────────┘
```

**Resultado do Mês 1-2:**
- Telemetria implementada em 100% dos componentes
- Baseline de métricas estabelecida com precisão
- 847 problemas documentados e categorizados
- Dívida técnica quantificada: 3 MVPs legados, 15 templates, zero persistência

---

### Mês 3 (Março 2026): Ciclos de Feedback

**Objetivo:** Criar canais de feedback que alimentassem o sistema com dados reais de qualidade, em tempo hábil para agir.

#### O Problema dos Feedbacks Quebrados

O time descobriu que o KODA tinha **4 gaps de feedback** que impediam qualquer melhoria:

```
OS 4 GAPS DE FEEDBACK DO KODA (MARÇO 2026)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

GAP 1: CLIENTE → KODA
┌─────────────────────────────────────────────────────────────────┐
│ Cliente reclama: "Esse produto chegou errado!"                  │
│                    │                                             │
│                    ▼                                             │
│ KODA: "Desculpe! Vou verificar..."                              │
│                    │                                             │
│                    ▼                                             │
│ Nada acontece. Ninguém investiga. Próximo cliente sofre igual.  │
│                                                                 │
│ TEMPO PERDIDO: Infinito (nunca fecha o loop)                    │
└─────────────────────────────────────────────────────────────────┘

GAP 2: OPERAÇÃO → ENGENHARIA
┌─────────────────────────────────────────────────────────────────┐
│ Time de operações detecta: "12 pedidos cancelados hoje"         │
│                    │                                             │
│                    ▼                                             │
│ Reporta no Slack #koda-ops                                      │
│                    │                                             │
│                    ▼                                             │
│ Mensagem se perde no scroll. Ninguém da engenharia vê.          │
│                                                                 │
│ TEMPO PERDIDO: 3-5 dias (até alguém perceber o padrão)          │
└─────────────────────────────────────────────────────────────────┘

GAP 3: MÉTRICAS → AÇÃO
┌─────────────────────────────────────────────────────────────────┐
│ Dashboard mostra: "Falsos positivos subiram para 42%"           │
│                    │                                             │
│                    ▼                                             │
│ Ninguém é alertado. Dashboard é passivo.                        │
│                                                                 │
│ TEMPO PERDIDO: 1-2 semanas (até a reunião mensal)               │
└─────────────────────────────────────────────────────────────────┘

GAP 4: CORREÇÃO → VALIDAÇÃO
┌─────────────────────────────────────────────────────────────────┐
│ Engenharia corrige: "Ajustei o prompt de recomendação"          │
│                    │                                             │
│                    ▼                                             │
│ Ninguém valida se a correção realmente funcionou.               │
│                                                                 │
│ TEMPO PERDIDO: Nunca fecha o loop de verificação                │
└─────────────────────────────────────────────────────────────────┘
```

#### A Solução: Sistema de Feedback em 3 Camadas

O time implementou um sistema de feedback com três camadas de velocidade:

```
SISTEMA DE FEEDBACK KODA — 3 CAMADAS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

┌─────────────────────────────────────────────────────────────────────────────┐
│                         CAMADA 1: FEEDBACK IMEDIATO (segundos)               │
│                                                                             │
│  Gatilho: Cliente reporta erro na conversa                                  │
│  Ação: KODA registra automaticamente em feedback_events.json               │
│  Exemplo:                                                                    │
│  {                                                                           │
│    "ts": "2026-03-15T14:32:09Z",                                            │
│    "type": "recommendation_error",                                           │
│    "severity": "high",                                                       │
│    "context": {                                                              │
│      "product_recommended": "WHEY-042",                                      │
│      "customer_allergy": "gluten",                                           │
│      "product_contains": "gluten",                                           │
│      "detected_by": "customer"                                               │
│    }                                                                         │
│  }                                                                           │
└─────────────────────────────────────────────────────────────────────────────┘
                                         │
                                         ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         CAMADA 2: FEEDBACK DIÁRIO (horas)                    │
│                                                                             │
│  Gatilho: Agregação diária de eventos                                       │
│  Ação: Relatório automático para #koda-feedback no Slack                    │
│  Conteúdo:                                                                   │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │ 📊 KODA Daily Feedback — 15 Mar 2026                                  │  │
│  │                                                                       │  │
│  │ 🔴 CRÍTICO (3 eventos):                                               │  │
│  │  • 2x recomendação com alérgeno (WHEY-042, CASEIN-018)               │  │
│  │  • 1x promessa de entrega quebrada (PEDIDO-8941)                     │  │
│  │                                                                       │  │
│  │ 🟡 ATENÇÃO (12 eventos):                                              │  │
│  │  • 7x lentidão em consulta de estoque (> 3s)                         │  │
│  │  • 5x cliente precisou repetir informação                             │  │
│  │                                                                       │  │
│  │ 🟢 POSITIVO (47 eventos):                                             │  │
│  │  • 47x recomendação aceita sem questionamento                         │  │
│  │                                                                       │  │
│  │ 📈 Tendência: Recomendações com alérgeno subiram 15% esta semana      │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
                                         │
                                         ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         CAMADA 3: FEEDBACK ESTRUTURAL (semanas)              │
│                                                                             │
│  Gatilho: Análise semanal de padrões                                        │
│  Ação: Reunião de retrospectiva + ajuste de rubrics/harness                │
│  Conteúdo:                                                                   │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │ 📋 KODA Structural Feedback — Semana 11 (Mar 2026)                    │  │
│  │                                                                       │  │
│  │ PADRÃO IDENTIFICADO: "Alérgenos escapam da validação"                 │  │
│  │ Ocorrências: 8 na semana                                              │  │
│  │ Causa Raiz: Rubric de recomendação não tinha dimensão de alergia      │  │
│  │ Ação: Adicionar dimensão "Alergia" na rubric com peso 40%             │  │
│  │ Dono: @maria (engenharia)                                             │  │
│  │ Prazo: 18 Mar                                                         │  │
│  │                                                                       │  │
│  │ PADRÃO IDENTIFICADO: "Cache de estoque mente sobre disponibilidade"   │  │
│  │ Ocorrências: 15 na semana                                             │  │
│  │ Causa Raiz: TTL de cache de 15min, invalidação manual                 │  │
│  │ Ação: Migrar para consulta em tempo real com TTL máximo de 60s        │  │
│  │ Dono: @carlos (infra)                                                 │  │
│  │ Prazo: 20 Mar                                                         │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### Como os Feedbacks Foram Fechados

O time implementou um processo simples mas rigoroso: **todo feedback aberto precisa ser fechado**. Não basta reportar — é preciso agir, verificar e documentar.

```
CICLO DE VIDA DE UM FEEDBACK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ABERTO ──────▶ EM ANÁLISE ──────▶ CORRIGIDO ──────▶ VALIDADO ──────▶ FECHADO
    │                │                  │                 │               │
    │                │                  │                 │               │
  Cliente         Time            Engenharia         Time de QA     Documentado
  reporta         investiga       implementa         verifica se    lição
  problema        causa raiz      correção           resolveu       aprendida

  SLA: 1h          SLA: 24h        SLA: 48h          SLA: 24h       SLA: 72h
                  (crítico)       (crítico)         (crítico)      (total)
```

**Resultado do Mês 3:**
- 847 problemas documentados → 312 corrigidos (37%)
- Tempo médio de fechamento de feedback: 4.2 dias → 1.8 dias (melhora de 57%)
- Feedbacks "órfãos" (sem dono): 0 (todos tinham responsável)
- Primeiros sinais de melhoria: FCR subiu de 62% para 68%

---

### Mês 4 (Abril 2026): Rubrics Adaptativas

**Objetivo:** Criar rubrics de avaliação que evoluíssem sozinhas conforme o sistema melhorava.

#### O Problema das Rubrics Estáticas

O time tinha rubrics desde o MVP. Mas elas eram estáticas — definidas em janeiro, nunca atualizadas. O resultado:

```
PROBLEMA: RUBRICS ESTÁTICAS EM UM SISTEMA QUE EVOLUI
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

JANEIRO: Rubric definida
  Dimensão "Preço": peso 30%, threshold: erro < R$ 5.00
  → OK, modelo errava preços com frequência

MARÇO: Modelo melhorou. Preços raramente erram.
  Dimensão "Preço": peso 30%, threshold: erro < R$ 5.00
  → 30% do peso em algo que quase nunca falha. Desperdício!

  Enquanto isso...
  Dimensão "Alergia": peso 5%, threshold: mencionar alergias
  → 5% do peso no problema #1 de falsos positivos. Insuficiente!

RESULTADO: Rubric mal calibrada premia o que já funciona
           e ignora o que está quebrado.
```

#### A Solução: Rubrics com Calibragem Automática

O time implementou um sistema onde as rubrics se recalibram automaticamente baseadas em dados reais de falha:

```
SISTEMA DE RUBRICS ADAPTATIVAS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

┌─────────────────────────────────────────────────────────────────────────────┐
│                    CALIBRAGEM AUTOMÁTICA DE RUBRICS                          │
│                                                                             │
│  A cada 2 semanas, o sistema analisa:                                       │
│                                                                             │
│  1. TAXA DE FALHA POR DIMENSÃO:                                             │
│     ┌─────────────────────────────────────────────────────────────────┐    │
│     │ Dimensão     │ Falhas (2 sem) │ Peso Atual │ Peso Sugerido      │    │
│     ├──────────────┼────────────────┼────────────┼────────────────────┤    │
│     │ Preço        │ 3 (2%)         │ 30%        │ 10% ⬇ (reduzir)   │    │
│     │ Estoque      │ 12 (8%)        │ 20%        │ 20% ➡ (manter)    │    │
│     │ Alergia      │ 45 (30%)       │ 5%         │ 35% ⬆ (aumentar)  │    │
│     │ Adequação    │ 18 (12%)       │ 25%        │ 25% ➡ (manter)    │    │
│     │ Entrega      │ 22 (15%)       │ 20%        │ 10% ⬇ (reduzir)   │    │
│     └─────────────────────────────────────────────────────────────────┘    │
│                                                                             │
│  2. THRESHOLD DE APROVAÇÃO:                                                 │
│     Score mínimo atual: 75/100                                              │
│     Taxa de falsos positivos com threshold 75: 38%                          │
│     Sugestão: elevar threshold para 85/100                                  │
│     Impacto estimado: falsos positivos caem para 18%,                       │
│                        mas 12% mais recomendações serão rejeitadas          │
│                                                                             │
│  3. CORRELAÇÃO RUBRIC × OUTCOME:                                            │
│     "Recomendações com score 80-85 têm 12% de devolução"                    │
│     "Recomendações com score 85-90 têm 4% de devolução"                     │
│     "Recomendações com score 90+ têm 1% de devolução"                       │
│     → Threshold ideal parece ser 87, não 75                                 │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### A Evolução da Rubric de Recomendação

Veja como a rubric evoluiu ao longo de 3 meses:

```
EVOLUÇÃO DA RUBRIC DE RECOMENDAÇÃO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RUBRIC v1.0 (Janeiro 2026) — "A Básica"
─────────────────────────────────────────
DIMENSÕES:
  1. Preço Correto (30%)       — threshold: ±R$ 5.00
  2. Estoque Disponível (25%)   — threshold: em estoque = sim
  3. Entrega Viável (20%)       — threshold: ETA < 72h
  4. Adequação ao Perfil (15%)  — threshold: score > 3/5
  5. Descrição Clara (10%)      — threshold: sem erros gramaticais

Score mínimo: 70/100
Problema: Não considera alergias, dietas, ou restrições do cliente.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RUBRIC v2.0 (Fevereiro 2026) — "A Consciente"
────────────────────────────────────────────
DIMENSÕES:
  1. Alergia & Restrições (30%) — threshold: zero alérgenos nos recomendados
  2. Preço Correto (20%)        — threshold: ±R$ 2.00 (mais rigoroso)
  3. Estoque Disponível (20%)   — threshold: confirmação em tempo real
  4. Entrega Viável (15%)       — threshold: ETA < 48h
  5. Adequação ao Perfil (15%)  — threshold: score > 4/5

Score mínimo: 75/100
Adicionado: Dimensão de alergia como prioridade máxima.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RUBRIC v3.0 (Abril 2026) — "A Inteligente"
─────────────────────────────────────────
DIMENSÕES (com pesos dinâmicos):
  1. Alergia & Restrições    — peso automático baseado em taxa de falha
  2. Preço Correto           — peso automático
  3. Estoque Real-Time       — peso automático
  4. Entrega Viável          — peso automático
  5. Adequação ao Perfil     — peso automático
  6. Satisfação Projetada    — NOVA: prediz CSAT baseado em histórico
  7. Consistência Cross-Sell — NOVA: recomendações complementares não se contradizem

Score mínimo: 85/100 (elevado automaticamente)
Recalibragem: automática a cada 2 semanas
```

#### Impacto das Rubrics Adaptativas

| Métrica | Rubric v1.0 (Jan) | Rubric v2.0 (Fev) | Rubric v3.0 (Mai) | Melhoria |
|---------|-------------------|-------------------|-------------------|----------|
| **Precisão de Recomendações** | 75% | 82% | 91% | +16pp |
| **Falsos Positivos** | 38% | 23% | 9% | -29pp |
| **Recomendações Rejeitadas** | 8% | 14% | 22% | +14pp (bom: filtro mais rigoroso) |
| **CSAT pós-recomendação** | 70% | 78% | 88% | +18pp |
| **Devoluções por insatisfação** | 15% | 10% | 5% | -10pp |

**Lição crítica:** Rejeitar mais recomendações (22% vs 8%) foi positivo. O KODA aprendeu a dizer "não sei" ou "prefiro não recomendar" em vez de recomendar com baixa confiança. Clientes preferem honestidade a confiança falsa.

---

### Mês 5 (Maio 2026): Simplificação do Harness

**Objetivo:** Remover componentes que se tornaram desnecessários conforme os modelos evoluíram.

#### O Princípio da Simplificação

Fernando estabeleceu uma regra que o time passou a chamar de **"Lei de Fernando"**:

> *"Para cada componente do harness, pergunte: 'Se eu removesse isso hoje, qual métrica pioraria?' Se a resposta for 'nenhuma' ou 'não sei', remova."*

Este princípio é contraintuitivo. A maior parte dos times de engenharia **adiciona** complexidade ao longo do tempo. O time KODA decidiu fazer o oposto: **remover** complexidade sempre que possível.

#### O Processo de Simplificação

```
PROCESSO DE SIMPLIFICAÇÃO DO HARNESS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Para cada componente do harness:

  1. MEDIR: Quanto custa? (tokens, latência, complexidade)
     ↓
  2. REMOVER (em staging): Desligar o componente por 48h
     ↓
  3. COMPARAR: Métricas com componente vs sem componente
     ↓
  4. DECIDIR:
     ├─ Se métricas NÃO pioraram → REMOVER permanentemente
     ├─ Se métricas pioraram pouco → SIMPLIFICAR o componente
     └─ Se métricas pioraram muito → MANTER (é realmente necessário)
```

#### O Que Foi Removido

```
COMPONENTES REMOVIDOS DO HARNESS (MAIO 2026)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

┌─────────────────────────────────────────────────────────────────────────────┐
│  ❌ REMOVIDO: Validator V1 (legado do MVP1)                                 │
│                                                                             │
│  O que fazia: 3 chamadas API sequenciais antes de cada recomendação        │
│  Custo: $0.09 por recomendação, 5.8s de latência                           │
│  Por que foi removido: O Evaluator (Generator/Evaluator) faz verificação   │
│                        mais precisa, mais rápida (0.6s) e mais barata      │
│  Métricas após remoção: Precisão = 91% (igual), Latência = -5.2s (ganho)   │
│  Economia: $27/dia em chamadas API                                         │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│  ❌ REMOVIDO: Cache Manager (legado do MVP2)                                │
│                                                                             │
│  O que fazia: Worker a cada 15min verificando promessas.json              │
│  Custo: $0.03 por verificação, 1 worker sempre rodando                     │
│  Por que foi removido: Consultas em tempo real com TTL de 60s eliminam     │
│                        a necessidade de verificação post-hoc                │
│  Métricas após remoção: Promessas quebradas = 9% (igual)                   │
│  Economia: $12/dia em worker + $0.03/verificação                           │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│  ❌ REMOVIDO: Rerouter (legado do MVP3)                                     │
│                                                                             │
│  O que fazia: Re-roteamento automático quando promessa quebrava            │
│  Custo: 38s de latência, race conditions, $1,200/mês em infra              │
│  Por que foi removido: Planner + Locks resolvem o problema na origem,     │
│                        evitando a necessidade de re-roteamento              │
│  Métricas após remoção: Race conditions = 0/dia (eram 5-8/dia)             │
│  Economia: $1,200/mês em infra                                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│  ❌ REMOVIDO: 11 dos 15 Prompt Templates                                    │
│                                                                             │
│  O que eram: 15 versões diferentes de prompts, criadas por devs diferentes │
│  Custo: Inconsistência, debugging difícil, ninguém sabia qual usar         │
│  Por que foram removidos: Padronização em 4 templates versionados          │
│                           com controle de versão (Git)                      │
│  Métricas após remoção: Consistência de respostas +40%, debug time -60%    │
│  Economia: Tempo de engenharia (impossível quantificar, mas enorme)        │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### O Novo Harness (Maio 2026)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                 KODA HARNESS — MAIO 2026 (VERSÃO SIMPLIFICADA)              │
└─────────────────────────────────────────────────────────────────────────────┘

                              ┌──────────────────────┐
                              │    CLIENTE (WhatsApp) │
                              └──────────┬───────────┘
                                         │
                              ┌──────────▼───────────┐
                              │    KODA INTERFACE     │
                              │    (Conversa)         │
                              └──────────┬───────────┘
                                         │
                         ┌───────────────┼───────────────┐
                         │               │               │
               ┌─────────▼─────────┐ ┌───▼──────────┐ ┌─▼──────────────┐
               │   GENERATOR       │ │  EVALUATOR   │ │  PLANNER       │
               │   (Recomenda)     │ │  (Verifica)  │ │  (Coordena)    │
               │                   │ │              │ │                │
               │   Prompt v4.2     │ │  Rubric v3.0 │ │  Locks + TTL   │
               │   0.3s            │ │  0.6s        │ │  0.4s          │
               └─────────┬─────────┘ └───┬──────────┘ └─┬──────────────┘
                         │               │               │
                         └───────────────┼───────────────┘
                                         │
                         ┌───────────────┼───────────────┐
                         │               │               │
               ┌─────────▼─────────┐ ┌───▼──────────┐ ┌─▼──────────────┐
               │   STATE STORE     │ │  AUDIT TRAIL │ │  TELEMETRY     │
               │   (SQLite)        │ │  (JSONL)     │ │  (SQLite)      │
               └───────────────────┘ └──────────────┘ └────────────────┘

COMPARAÇÃO COM JANEIRO 2026:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Componentes: 8 → 6 (-25%)
Latência total: 5.8s → 1.3s (-78%)
Custo por recomendação: $0.09 → $0.02 (-78%)
Custo mensal de infra: $5,400 → $3,100 (-43%)
Race conditions: 5-8/dia → 0/dia
Templates de prompt: 15 → 4 (versionados)
MTTD (debug): 4.2h → 35min (-86%)
```

---

### Mês 6 (Junho 2026): Cultura de Melhoria Contínua

**Objetivo:** Transformar a melhoria contínua de um "projeto" para um "processo que roda sozinho".

#### Os 4 Pilares da Cultura de Melhoria Contínua

Fernando sabia que o verdadeiro teste não era chegar a junho com métricas boas. Era garantir que em dezembro as métricas seriam **ainda melhores** — sem ele precisar liderar cada iniciativa.

```
OS 4 PILARES DA CULTURA DE MELHORIA CONTÍNUA DO KODA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PILAR 1: MÉTRICAS COMO LINGUAGEM COMUM
──────────────────────────────────────
• Toda reunião começa com o dashboard de métricas
• Métricas são visíveis para TODOS (não só engenharia)
• "O que os números dizem?" substituiu "Eu acho que..."
• Nenhuma decisão de arquitetura sem dados que a suportem

PILAR 2: FEEDBACK COMO RITUAL
──────────────────────────────
• Daily: 10min revisando feedbacks críticos das últimas 24h
• Semanal: 30min identificando padrões nos feedbacks
• Mensal: 1h de retrospectiva com ações concretas
• Trimestral: Recalibragem completa de rubrics e thresholds

PILAR 3: SIMPLIFICAÇÃO COMO VALOR
──────────────────────────────────
• "O que podemos remover este mês?" é pergunta obrigatória em toda planning
• Cada componente do harness tem um "dono" responsável por justificar sua existência
• Componentes sem dono há 30 dias são automaticamente candidatos à remoção
• Meta: reduzir número de componentes em 10% a cada trimestre

PILAR 4: APRENDIZADO COMO OUTPUT
─────────────────────────────────
• Todo incidente gera um "learning card" (documento de 1 página)
• Learning cards são revisados em onboarding de novos engenheiros
• Lições aprendidas alimentam as rubrics (fechando o ciclo)
• Métrica: "learning cards gerados por trimestre" (target: > 20)
```

#### O Ritmo Semanal de Melhoria Contínua

```
CALENDÁRIO SEMANAL DO TIME KODA (JUNHO 2026)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SEGUNDA-FEIRA
  09:00 — Daily Review: feedbacks críticos do fim de semana
  10:00 — Planning semanal: quais melhorias esta semana?
  11:00 — Alocação: cada melhoria tem um dono

TERÇA-FEIRA
  14:00 — "Simplify Hour": 1h dedicada a remover coisas
          (componentes, código, processos que não servem mais)

QUARTA-FEIRA
  10:00 — Code Review de melhorias implementadas
  16:00 — "Rubric Calibration Check": as rubrics ainda fazem sentido?

QUINTA-FEIRA
  09:00 — Demo interna: melhorias da semana em staging
  14:00 — Validação cruzada: time de QA testa melhorias

SEXTA-FEIRA
  10:00 — Retrospectiva semanal: o que aprendemos?
  11:00 — "Learning Cards": documentar lições da semana
  15:00 — Deploy controlado (se aplicável)
  16:00 — Celebrar wins da semana 🎉
```

---

## 🏗️ Diagrama: Evolução do Harness (Janeiro → Junho 2026)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│              EVOLUÇÃO DO HARNESS DO KODA — 6 MESES                           │
│                   De Frankenstein a Sistema Simplificado                     │
└─────────────────────────────────────────────────────────────────────────────┘

JANEIRO 2026 — "FRANKENHARNESS"              JUNHO 2026 — "HARNESS SIMPLIFICADO"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━            ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

┌──────────────────────────┐                ┌──────────────────────────┐
│      KODA (Monólito)     │                │      KODA INTERFACE      │
│                          │                │                          │
│  Faz TUDO sozinho:       │                │  Só conversa com cliente │
│  • Recomenda             │                │  Delega tudo abaixo      │
│  • Avalia                │                └────────────┬─────────────┘
│  • Coordena              │                             │
│  • Gerencia estado       │              ┌──────────────┼──────────────┐
└────────────┬─────────────┘              │              │              │
             │                   ┌────────▼──────┐ ┌─────▼──────┐ ┌────▼──────┐
  ┌──────────┼──────────┐        │   GENERATOR   │ │ EVALUATOR  │ │  PLANNER  │
  │          │          │        │               │ │            │ │           │
  ▼          ▼          ▼        │ Cria opções   │ │ Verifica   │ │ Coordena  │
┌────┐   ┌────┐     ┌────┐      │               │ │            │ │           │
│ V1 │   │ V2 │     │ V3 │      └──────┬────────┘ └─────┬──────┘ └────┬──────┘
│MVP1│   │MVP2│     │MVP3│             │                │             │
└────┘   └────┘     └────┘             └────────────────┼─────────────┘
                                                         │
Componentes: 8                                  ┌────────┼────────┐
Latência: 5.8s                                  │        │        │
Custo/rec: $0.09                         ┌──────▼──┐ ┌──▼────┐ ┌─▼───────┐
Falsos +: 38%                            │  STATE  │ │AUDIT  │ │TELEMETRY│
CSAT: 70%                                │  STORE  │ │TRAIL  │ │         │
MTTD: 4.2h                               └─────────┘ └───────┘ └─────────┘
Templates: 15
Race cond: 5-8/dia                       Componentes: 6 (-25%)
                                         Latência: 1.3s (-78%)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━    Custo/rec: $0.02 (-78%)
           TRANSIÇÃO (6 meses)           Falsos +: 5% (-33pp)
                                         CSAT: 91% (+21pp)
  JAN: Diagnóstico e baseline            MTTD: 35min (-86%)
  FEV: Telemetria e métricas             Templates: 4
  MAR: Ciclos de feedback                Race cond: 0/dia
  ABR: Rubrics adaptativas               ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  MAI: Simplificação do harness
  JUN: Cultura de melhoria contínua

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
              REDUÇÃO DE COMPLEXIDADE ENQUANTO MÉTRICAS MELHORAM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 📊 Métricas Comparativas por Trimestre

### Q1 2026 (Janeiro-Março): Diagnóstico, Telemetria & Feedback

| Métrica | Janeiro (Baseline) | Fevereiro | Março | Delta Q1 |
|---------|-------------------|-----------|-------|----------|
| **Precisão de Recomendações** | 75% | 78% | 82% | +7pp |
| **FCR (First Contact Resolution)** | 62% | 65% | 68% | +6pp |
| **CSAT** | 70% | 73% | 78% | +8pp |
| **Tempo Médio de Conversa** | 2.4h | 2.2h | 2.0h | -0.4h |
| **Custo por Conversa (tokens)** | $0.47 | $0.44 | $0.41 | -$0.06 |
| **Falsos Positivos** | 38% | 31% | 23% | -15pp |
| **Taxa de Devolução** | 15% | 13% | 10% | -5pp |
| **Churn Mensal** | 8% | 7% | 6% | -2pp |
| **MTTD (Debug)** | 4.2h | 2.5h | 1.5h | -2.7h |
| **Cobertura de Testes** | 12% | 25% | 40% | +28pp |

**Análise Q1:** Melhorias graduais mas consistentes. O foco em telemetria e feedback começou a mostrar resultados. Falsos positivos caíram 15pp — a maior melhoria do trimestre.

### Q2 2026 (Abril-Junho): Rubrics, Simplificação & Cultura

| Métrica | Abril | Maio | Junho | Delta Q2 | Delta Total (Jan→Jun) |
|---------|-------|------|-------|----------|----------------------|
| **Precisão de Recomendações** | 87% | 91% | 95% | +8pp | +20pp |
| **FCR (First Contact Resolution)** | 74% | 80% | 87% | +13pp | +25pp |
| **CSAT** | 83% | 88% | 91% | +8pp | +21pp |
| **Tempo Médio de Conversa** | 1.7h | 1.4h | 1.1h | -0.6h | -1.3h |
| **Custo por Conversa (tokens)** | $0.35 | $0.27 | $0.21 | -$0.14 | -$0.26 |
| **Falsos Positivos** | 14% | 9% | 5% | -9pp | -33pp |
| **Taxa de Devolução** | 8% | 6% | 4% | -4pp | -11pp |
| **Churn Mensal** | 5% | 3% | 2% | -3pp | -6pp |
| **MTTD (Debug)** | 55min | 40min | 30min | -25min | -3.7h |
| **Cobertura de Testes** | 55% | 70% | 82% | +27pp | +70pp |

**Análise Q2:** Aceleração significativa. A combinação de rubrics adaptativas + simplificação do harness criou um efeito multiplicador. Precisão saltou de 82% para 95%. Custo por conversa caiu mais 55%.

### Gráfico de Tendências: As 4 Métricas-Chave

```
EVOLUÇÃO DAS 4 MÉTRICAS-CHAVE (JANEIRO → JUNHO 2026)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PRECISÃO DE RECOMENDAÇÕES                    FALSOS POSITIVOS
100% ┤                                   40% ┤
 95% ┤                          ████████ 35% ┤ ██
 90% ┤                    ██████          30% ┤ ███
 85% ┤              ██████                25% ┤ ████
 80% ┤        ██████                      20% ┤ █████
 75% ┤  ██████                            15% ┤ ██████
 70% ┤                                    10% ┤ ███████
     └──┬──┬──┬──┬──┬──┬──                    └──┬──┬──┬──┬──┬──┬──
       J  F  M  A  M  J                          J  F  M  A  M  J

CSAT (SATISFAÇÃO)                           CUSTO POR CONVERSA
100% ┤                                   $0.50 ┤ ██
 95% ┤                          ██       $0.45 ┤ ███
 90% ┤                    ██████         $0.40 ┤ ████
 85% ┤              ██████               $0.35 ┤ █████
 80% ┤        ██████                     $0.30 ┤ ██████
 75% ┤  ██████                           $0.25 ┤ ███████
 70% ┤                                   $0.20 ┤ ████████
     └──┬──┬──┬──┬──┬──┬──                    └──┬──┬──┬──┬──┬──┬──
       J  F  M  A  M  J                          J  F  M  A  M  J
```

---

## 🔄 Tabela Comparativa: Estratégias de Coordenação

Durante os 6 meses, o time experimentou diferentes estratégias de coordenação entre os componentes do KODA. Esta tabela documenta as 5 estratégias avaliadas e o que funcionou para cada contexto.

### Visão Geral das Estratégias

| Estratégia | Descrição | Quando Usar | Quando NÃO Usar | Usada no KODA? |
|------------|-----------|-------------|-----------------|----------------|
| **Monolítica** | Um agente faz tudo: recomenda, valida, coordena, persiste | MVPs rápidos, protótipos, features simples | Produção, features complexas, concorrência | ❌ Janeiro (substituída) |
| **Generator/Evaluator** | Separa criação (Generator) de verificação (Evaluator) | Qualquer sistema onde qualidade importa mais que latência | Features triviais onde o custo da verificação > custo do erro | ✅ Fevereiro+ |
| **Planner-Centralizado** | Um Planner coordena agentes especializados, que são passivos | Coordenação com estado compartilhado, recursos limitados | Sistemas onde agentes precisam de alta autonomia | ✅ Março-Maio |
| **Híbrida (Planner + Autonomia Local)** | Planner coordena macro, agentes otimizam micro | Sistemas complexos com múltiplos domínios | Sistemas simples (overhead desnecessário) | ✅ Maio-Junho |
| **Descentralizada (Event-Driven)** | Agentes se coordenam por eventos, sem orquestrador central | Escala massiva, domínios independentes | Coordenação com estado compartilhado, race conditions | 🔮 Futuro (pós-10K conversas/dia) |

### Análise Detalhada por Estratégia

#### 1. Estratégia Monolítica

```
┌─────────────────────────────────────────────────────────────────┐
│                        MONOLÍTICA                                │
│                                                                 │
│                    ┌──────────────────┐                         │
│                    │   KODA (Único)   │                         │
│                    │                  │                         │
│                    │ • Recomenda      │                         │
│                    │ • Valida         │                         │
│                    │ • Coordena       │                         │
│                    │ • Persiste       │                         │
│                    └──────────────────┘                         │
│                                                                 │
│  Prós:                                                          │
│  • Simples de implementar                                       │
│  • Baixa latência (tudo em memória)                             │
│  • Fácil de debugar (um único trace)                            │
│                                                                 │
│  Contras:                                                       │
│  • Sycophancy: agente aprova o próprio trabalho                 │
│  • Sem separação de responsabilidades                           │
│  • Impossível escalar (um agente = um gargalo)                  │
│  • Estado volátil (RAM apenas)                                  │
│                                                                 │
│  KODA: Usada em Janeiro 2026. Funcionava para MVP,              │
│         mas não para produção. Substituída em Fevereiro.        │
└─────────────────────────────────────────────────────────────────┘
```

#### 2. Generator/Evaluator

```
┌─────────────────────────────────────────────────────────────────┐
│                    GENERATOR / EVALUATOR                         │
│                                                                 │
│         ┌──────────────┐        ┌──────────────┐               │
│         │  GENERATOR   │───────▶│  EVALUATOR   │               │
│         │  (Cria)      │        │  (Verifica)  │               │
│         └──────────────┘        └──────┬───────┘               │
│                                        │                        │
│                                   ┌────▼────┐                   │
│                                   │ APROVA? │                   │
│                                   └────┬────┘                   │
│                                  ┌─────┴─────┐                  │
│                               ✅ SIM      ❌ NÃO               │
│                                  │            │                 │
│                                  ▼            ▼                 │
│                              Publica      Devolve ao            │
│                              resposta     Generator             │
│                                                                 │
│  Prós:                                                          │
│  • Elimina sycophancy (avaliador independente)                  │
│  • Feedback específico melhora o Generator ao longo do tempo    │
│  • Simples de entender e implementar                            │
│                                                                 │
│  Contras:                                                       │
│  • Latência adicional (2 chamadas LLM em vez de 1)              │
│  • Custo adicional (2x tokens para avaliação)                   │
│  • Não resolve coordenação entre múltiplos agentes              │
│                                                                 │
│  KODA: Implementado em Fevereiro. Reduziu falsos positivos      │
│         de 38% para 23%. Custo adicional compensado pela        │
│         redução em devoluções e suporte.                        │
└─────────────────────────────────────────────────────────────────┘
```

#### 3. Planner Centralizado

```
┌─────────────────────────────────────────────────────────────────┐
│                    PLANNER CENTRALIZADO                          │
│                                                                 │
│                    ┌──────────────┐                             │
│                    │   PLANNER    │                             │
│                    │ (Orquestra)  │                             │
│                    └──┬──┬──┬────┘                             │
│                       │  │  │                                    │
│              ┌────────┘  │  └────────┐                          │
│              ▼           ▼           ▼                          │
│        ┌─────────┐ ┌─────────┐ ┌─────────┐                     │
│        │ Agent A │ │ Agent B │ │ Agent C │                     │
│        │(passivo)│ │(passivo)│ │(passivo)│                     │
│        └─────────┘ └─────────┘ └─────────┘                     │
│                                                                 │
│  Prós:                                                          │
│  • Visão global: Planner vê o sistema inteiro                   │
│  • Decisões coerentes (sem conflitos entre agentes)             │
│  • Fácil de auditar (decisões centralizadas)                    │
│                                                                 │
│  Contras:                                                       │
│  • Planner é single-point-of-failure                            │
│  • Gargalo de escalabilidade (Planner processa tudo)            │
│  • Agentes especializados são subutilizados                     │
│                                                                 │
│  KODA: Usada de Março a Maio. Excelente para coordenação        │
│         de recursos compartilhados (estoque, entregadores).     │
│         Funcionou bem para volume atual (~500 conversas/dia).   │
└─────────────────────────────────────────────────────────────────┘
```

#### 4. Híbrida (Planner + Autonomia Local)

```
┌─────────────────────────────────────────────────────────────────┐
│                    HÍBRIDA                                       │
│                                                                 │
│              ┌──────────────────────────┐                       │
│              │        PLANNER           │                       │
│              │   (Coordenação Macro)    │                       │
│              │                          │                       │
│              │ • Define objetivos       │                       │
│              │ • Aloca recursos         │                       │
│              │ • Resolve conflitos      │                       │
│              └────┬──────┬──────┬──────┘                       │
│                   │      │      │                               │
│         ┌─────────┘      │      └─────────┐                    │
│         ▼                ▼                ▼                    │
│   ┌──────────┐    ┌──────────┐     ┌──────────┐               │
│   │ AGENT A  │    │ AGENT B  │     │ AGENT C  │               │
│   │(autônomo)│    │(autônomo)│     │(autônomo)│               │
│   │          │    │          │     │          │               │
│   │ Otimiza  │    │ Otimiza  │     │ Otimiza  │               │
│   │ domínio  │    │ domínio  │     │ domínio  │               │
│   │ local    │    │ local    │     │ local    │               │
│   └──────────┘    └──────────┘     └──────────┘               │
│                                                                 │
│  Prós:                                                          │
│  • Melhor dos dois mundos: coordenação + autonomia              │
│  • Planejador não é gargalo (agentes tomam decisões locais)     │
│  • Escala melhor que centralizado puro                          │
│  • Agentes especializados são valorizados                       │
│                                                                 │
│  Contras:                                                       │
│  • Mais complexo de implementar e debugar                       │
│  • Risco de decisões conflitantes (mitigado por locks)          │
│  • Overhead de coordenação                                      │
│                                                                 │
│  KODA: Adotada em Maio 2026. Melhor balanço para o volume       │
│         atual. Permite escalar para 5K conversas/dia sem        │
│         grandes mudanças.                                       │
└─────────────────────────────────────────────────────────────────┘
```

#### 5. Descentralizada (Event-Driven)

```
┌─────────────────────────────────────────────────────────────────┐
│                    DESCENTRALIZADA                               │
│                                                                 │
│   ┌──────────┐   evento   ┌──────────┐   evento   ┌──────────┐ │
│   │ AGENT A  │───────────▶│ AGENT B  │───────────▶│ AGENT C  │ │
│   │          │            │          │            │          │ │
│   └──────────┘            └──────────┘            └──────────┘ │
│         ▲                                               │       │
│         └─────────────── evento ───────────────────────┘       │
│                                                                 │
│  Prós:                                                          │
│  • Escala massivamente (sem gargalo central)                    │
│  • Robusto (sem single-point-of-failure)                        │
│  • Agentes totalmente autônomos                                 │
│                                                                 │
│  Contras:                                                       │
│  • Complexidade de debug (eventos assíncronos)                  │
│  • Estado eventualmente consistente (não imediato)              │
│  • Risco de loops infinitos de eventos                          │
│  • Difícil garantir atomicidade em operações críticas           │
│                                                                 │
│  KODA: Não implementada (ainda). Considerada para o futuro      │
│         se o volume ultrapassar 10K conversas/dia.              │
│         Híbrida atual é suficiente para a escala atual.         │
└─────────────────────────────────────────────────────────────────┘
```

### Matriz de Decisão: Qual Estratégia Usar?

| Critério | Monolítica | Gen/Eval | Planner | Híbrida | Descentralizada |
|----------|-----------|----------|---------|---------|-----------------|
| **Volume < 100/dia** | ✅ | ✅ | ❌ overkill | ❌ overkill | ❌ overkill |
| **Volume 100-1K/dia** | ❌ | ✅ | ✅ | ⚠️ opcional | ❌ overkill |
| **Volume 1K-10K/dia** | ❌ | ⚠️ | ⚠️ | ✅ | ⚠️ opcional |
| **Volume 10K+/dia** | ❌ | ❌ | ❌ | ⚠️ | ✅ |
| **Qualidade crítica** | ❌ | ✅ | ✅ | ✅ | ⚠️ |
| **Baixa latência** | ✅ | ⚠️ | ⚠️ | ⚠️ | ❌ |
| **Debug simples** | ✅ | ✅ | ⚠️ | ❌ | ❌ |
| **Recursos compartilhados** | ❌ | ❌ | ✅ | ✅ | ❌ |
| **Time pequeno (<5)** | ✅ | ✅ | ❌ | ❌ | ❌ |
| **Time médio (5-15)** | ❌ | ✅ | ✅ | ✅ | ❌ |
| **Time grande (15+)** | ❌ | ✅ | ✅ | ✅ | ✅ |

---

## 🛠️ KODA Application: Como Aplicar Melhoria Contínua no Seu Contexto

Esta seção traduz os aprendizados do case study em ações práticas para qualquer feature do KODA.

### Framework de Melhoria Contínua em 5 Passos

```
FRAMEWORK KCI (KODA CONTINUOUS IMPROVEMENT)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PASSO 1: MEDIR TUDO (Semana 1-2)
├── Implementar telemetria em TODOS os componentes
├── Estabelecer baseline de métricas com dados reais
├── Criar dashboard visível para todo o time
└── Identificar as 3 métricas que mais importam para o negócio

PASSO 2: FECHAR OS GAPS DE FEEDBACK (Semana 3-4)
├── Mapear todos os gaps de feedback (cliente → código)
├── Implementar sistema de feedback em 3 camadas
├── Definir SLAs para cada tipo de feedback
└── Criar ritual diário de revisão de feedbacks

PASSO 3: CALIBRAR RUBRICS (Semana 5-8)
├── Auditar rubrics existentes: pesos fazem sentido?
├── Implementar calibragem automática baseada em taxa de falha
├── Adicionar dimensões que faltam (alergias, restrições, preferências)
├── Elevar threshold de aprovação gradualmente
└── Criar correlação rubric score × outcome real

PASSO 4: SIMPLIFICAR (Semana 9-12)
├── Listar TODOS os componentes do harness
├── Para cada um: "Se eu remover, qual métrica piora?"
├── Remover em staging por 48h e medir
├── Se métricas não pioraram → remover permanentemente
└── Meta: reduzir componentes em 10% por trimestre

PASSO 5: CULTURA (Semana 13+)
├── Estabelecer rituais: daily feedback, weekly retro, monthly calibration
├── Criar "learning cards" para todo incidente
├── Tornar métricas a linguagem comum do time
├── Celebrar remoções tanto quanto adições
└── Fazer melhoria contínua ser automática, não dependente de líderes
```

### Template de Learning Card

Todo incidente ou aprendizado significativo no KODA gera um **Learning Card** — um documento de 1 página que captura a lição para sempre.

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
LEARNING CARD #042 — "Alérgenos escapam da validação quando mencionados no meio
                      de conversas longas"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DATA: 15 Março 2026
SEVERIDADE: 🔴 Alta
AUTOR: @maria (engenharia)
TAGS: #recomendação #alergia #context-amnesia #rubric

O QUE ACONTECEU:
Cliente mencionou alergia a glúten no minuto 5 da conversa. No minuto 45,
KODA recomendou WHEY-042 (contém glúten). Cliente detectou o erro e reportou.

CAUSA RAIZ:
A informação da alergia estava no histórico da conversa, mas a rubric de
recomendação (v1.0) não tinha dimensão de alergia. O Generator focou em
preço e estoque, ignorando restrições alimentares.

AÇÃO TOMADA:
1. Adicionada dimensão "Alergia & Restrições" na rubric v2.0 (peso 30%)
2. Implementada verificação automática: antes de recomendar, checar
   se o produto contém alérgenos conhecidos do cliente
3. Adicionado teste de regressão: "cliente com alergia a X" nunca recebe
   produto contendo X

VALIDAÇÃO:
48h após a correção, zero ocorrências de recomendação com alérgeno.
Monitorado por 2 semanas: 0 recorrências.

LIÇÃO:
Rubrics precisam evoluir com os padrões de falha. Uma dimensão que não
existia na v1.0 (alergia) era a causa de 40% dos falsos positivos.
Calibragem automática teria detectado isso mais cedo.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Exemplo Concreto: Aplicando o Framework KCI na Feature "Cupom de Desconto"

Vamos ver como o framework KCI foi aplicado em uma feature real do KODA, implementada após o programa KCI: o sistema de cupons de desconto.

**Contexto:** Em julho de 2026, após o sucesso do programa KCI, o time de marketing pediu uma feature de cupons. O KODA deveria sugerir cupons relevantes durante a conversa ("Você sabia que tem 15% de desconto em whey protein hoje?").

Em vez de simplesmente implementar, o time aplicou o framework KCI:

```
APLICAÇÃO DO FRAMEWORK KCI — FEATURE "CUPOM DE DESCONTO"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PASSO 1: MEDIR (Semana 1)
─────────────────────────
Antes de escrever uma linha de código:
  • Definiram métricas de sucesso:
    - Taxa de conversão de cupom (cliente vê → usa): target > 15%
    - Relevância do cupom (cupom certo para o cliente certo): target > 80%
    - Impacto no ticket médio (cupom não canibaliza venda cheia): target > 0%
    - Custo da feature (tokens, latência): target < $0.03 por sugestão
  • Criaram dashboard específico para a feature
  • Estabeleceram baseline: "hoje, 0 cupons são sugeridos = baseline zero"

PASSO 2: FEEDBACK (Semana 2)
────────────────────────────
  • Implementaram eventos de telemetria específicos:
    - "coupon_suggested" (quando KODA sugere um cupom)
    - "coupon_viewed" (cliente clicou/leu o cupom)
    - "coupon_applied" (cliente usou o cupom)
    - "coupon_ignored" (cliente ignorou a sugestão)
    - "coupon_irrelevant" (cliente reclamou: "não quero isso")
  • Feedbacks automáticos para o Slack:
    - Diário: taxa de conversão, cupons mais/menos usados
    - Semanal: padrões de rejeição, ajustes de targeting

PASSO 3: CALIBRAR RUBRICS (Semanas 3-4)
───────────────────────────────────────
  • Criaram rubric específica para sugestão de cupom:
    Dimensão 1: Relevância (40%) — o cupom é relevante para este cliente?
    Dimensão 2: Timing (25%) — é o momento certo na conversa?
    Dimensão 3: Não-canibalização (20%) — o cliente compraria mesmo sem cupom?
    Dimensão 4: Clareza (15%) — os termos do cupom são claros?
  • Threshold inicial: score > 75 para sugerir
  • Recalibragem após 2 semanas baseado em taxa de conversão real

PASSO 4: SIMPLIFICAR (Semana 5)
───────────────────────────────
  • Versão inicial tinha 3 etapas de validação
  • Testaram remover a etapa 2 (validação de estoque para cupom)
    → Conversão não mudou, latência caiu 0.3s
  • Removeram permanentemente

PASSO 5: CULTURA (Semana 6+)
────────────────────────────
  • Learning card documentado após 1 mês de operação
  • Lição principal: "Cupons genéricos (10% em tudo) convertem 3x menos
    que cupons específicos (15% na sua categoria favorita)"
  • Rubric ajustada para penalizar genericidade

RESULTADO APÓS 6 SEMANAS:
  • Taxa de conversão: 18% (target era 15%) ✅
  • Relevância: 84% (target era 80%) ✅
  • Impacto no ticket médio: +8% (clientes compram mais com cupom) ✅
  • Custo: $0.02 por sugestão (target era $0.03) ✅
  • Zero incidentes relacionados a cupons ✅
```

### Anti-Padrões: O Que NÃO Fazer em Melhoria Contínua

Baseado nos erros que o time KODA cometeu (e viu outros times cometerem):

```
5 ANTI-PADRÕES DE MELHORIA CONTÍNUA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ANTI-PADRÃO 1: "MÉTRICAS DE VAIDADE"
────────────────────────────────────
❌ ERRADO: "Temos 99.9% de uptime!" (mas 38% das promessas são quebradas)
✅ CERTO:  Métricas que refletem a experiência real do cliente
          (precisão, CSAT, falsos positivos, FCR)

ANTI-PADRÃO 2: "FEEDBACK FANTASMA"
──────────────────────────────────
❌ ERRADO: "Coletamos feedback dos clientes!" (mas ninguém age sobre ele)
✅ CERTO:  Todo feedback tem dono, prazo, ação e verificação
          (ciclo fechado: aberto → em análise → corrigido → validado → fechado)

ANTI-PADRÃO 3: "RUBRIC CONGELADA"
─────────────────────────────────
❌ ERRADO: "Nossa rubric foi definida há 6 meses e funciona bem"
✅ CERTO:  Rubrics são recalibradas a cada 2 semanas baseado em dados reais
          (o que funcionava há 6 meses pode ser irrelevante hoje)

ANTI-PADRÃO 4: "ACUMULADOR DE COMPONENTES"
──────────────────────────────────────────
❌ ERRADO: "Vamos adicionar mais uma validação, só por segurança"
✅ CERTO:  "O que podemos remover este mês?" é pergunta obrigatória
          (cada componente tem custo de manutenção, debug, onboarding)

ANTI-PADRÃO 5: "MELHORIA CONTÍNUA É PROJETO DO LÍDER"
─────────────────────────────────────────────────────
❌ ERRADO: Só o Tech Lead puxa iniciativas de melhoria
✅ CERTO:  Qualquer pessoa do time pode (e deve) propor melhorias
          (cultura > projeto)
```

### Checklist de Implementação para Novas Features

Antes de implementar qualquer feature nova no KODA, use este checklist:

```
CHECKLIST PRÉ-IMPLEMENTAÇÃO DE FEATURE KODA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

□ TELEMETRIA: Todos os componentes da feature emitem eventos de telemetria?
□ MÉTRICAS: As métricas de sucesso da feature estão definidas e mensuráveis?
□ FEEDBACK: Existe um canal de feedback do cliente para a engenharia?
□ RUBRIC: A feature tem uma rubric de avaliação com pesos calibrados?
□ HARNESS: A feature adiciona novos componentes ao harness? Se sim, justifique.
□ SIMPLIFICAÇÃO: Algum componente existente pode ser removido com esta feature?
□ TESTES: Cobertura de testes > 80% para a nova feature?
□ LEARNING CARD: O design da feature foi documentado como learning card?
□ OWNERSHIP: Todo componente tem um dono claro?
□ REVISÃO TRIMESTRAL: A feature será reavaliada em 3 meses para possível simplificação?
```

---

## 💡 Lições Aprendidas

### As 10 Lições que Transformaram o KODA

#### Lição 1: Você Não Pode Melhorar o Que Não Mede

> *"Em janeiro, tínhamos 'métricas de vaidade': uptime, número de mensagens. Em março, tínhamos métricas de verdade: precisão, falsos positivos, CSAT por segmento. A diferença? Com métricas de verdade, você sabe o que melhorar. Com métricas de vaidade, você só sabe que algo está ligado."*

**Ação prática:** Antes de qualquer iniciativa de melhoria, invista 2 semanas em telemetria. Sem dados, melhoria é opinião.

#### Lição 2: Feedbacks Precisam de Dono e Prazo

> *"Tínhamos 847 problemas documentados em janeiro. Mas zero tinham dono. Zero tinham prazo. Eram uma lista de desejos, não um plano de ação. Quando cada feedback ganhou um responsável e um SLA, 37% foram resolvidos em 2 meses."*

**Ação prática:** Todo feedback aberto precisa de: (1) responsável nomeado, (2) data de conclusão, (3) verificação de que a correção funcionou.

#### Lição 3: Rubrics Estáticas São Inimigas da Melhoria

> *"Em janeiro, nossa rubric de recomendação dedicava 30% do peso a 'preço correto' — algo que o modelo acertava 98% das vezes. Enquanto isso, 'alergia do cliente' tinha peso zero. A rubric estava calibrada para o KODA de 8 meses atrás, não para o KODA de hoje."*

**Ação prática:** Recalibre rubrics a cada 2 semanas. Peso de cada dimensão deve ser proporcional à taxa de falha naquela dimensão.

#### Lição 4: Simplificar é Mais Difícil que Adicionar — e Mais Valioso

> *"Remover o Validator V1 (legado do MVP1) levou 3 semanas de convencimento. 'E se precisarmos?' 'Foi difícil construir'. 'Dá medo remover'. Mas quando removemos, nada quebrou. Ganhamos 5 segundos de latência e economizamos $27/dia. A lição: o medo de remover é maior que o risco real."*

**Ação prática:** Para cada componente, pergunte: "Se eu remover hoje, qual métrica piora?" Se a resposta for "não sei", teste em staging por 48h.

#### Lição 5: Modelos Melhoram, Seu Harness Deve Acompanhar

> *"Em janeiro, o modelo base errava preços com frequência. Precisávamos de 3 verificações. Em maio, o modelo acertava preços 98% das vezes. Mas ainda tínhamos as 3 verificações. O harness não evoluiu junto com o modelo."*

**Ação prática:** A cada novo modelo (ou melhoria significativa do modelo existente), reavalie TODOS os componentes do harness. O que era necessário com o modelo antigo pode ser desperdício com o novo.

#### Lição 6: Sycophancy é o Inimigo Silencioso

> *"O KODA aprovava o próprio trabalho com confiança inabalável. 'Claro que está certo, fui eu que fiz'. O Generator/Evaluator resolveu isso: quando você separa quem cria de quem avalia, a qualidade sobe naturalmente. Não porque o Generator melhorou, mas porque o viés de auto-confirmação foi eliminado."*

**Ação prática:** Nunca deixe o mesmo agente gerar e avaliar. A separação de responsabilidades é o padrão mais subestimado em AI engineering.

#### Lição 7: Custo e Qualidade Não São Trade-offs

> *"A intuição diz: 'para melhorar qualidade, preciso gastar mais'. Nossa experiência mostrou o oposto. Removemos componentes desnecessários, simplificamos o harness, e tanto a qualidade subiu (precisão +20pp) quanto o custo caiu (custo por conversa -55%). Qualidade e eficiência andam juntas quando você remove o que não serve."*

**Ação prática:** Desconfie de qualquer "melhoria" que aumente a complexidade do sistema. As melhores melhorias simplificam.

#### Lição 8: A Melhoria Não é Linear

> *"Janeiro e fevereiro foram lentos. Melhorias de 2-3 pontos percentuais. Março acelerou. Abril e maio explodiram. Isso é normal. Melhoria contínua tem um efeito composto: as primeiras melhorias criam a base para as próximas. Não desanime nos meses lentos."*

**Ação prática:** Espere 2-3 meses de melhorias graduais antes de ver aceleração. O efeito composto é real, mas leva tempo para aparecer.

#### Lição 9: Cultura Começa com Rituais

> *"No começo, 'melhoria contínua' era um projeto do Fernando. Em junho, era um ritual do time. A diferença? Rituais. Daily de feedback, weekly retro, monthly calibration. Quando a melhoria contínua tem um slot fixo no calendário, ela acontece. Quando depende de alguém lembrar, não acontece."*

**Ação prática:** Coloque a melhoria contínua no calendário. Slots fixos semanais. Se não está na agenda, não é prioridade.

#### Lição 10: O Objetivo Não é um KODA Perfeito. É um KODA Que Melhora Sozinho.

> *"Em janeiro, queríamos 'consertar o KODA'. Em junho, entendemos que o KODA nunca vai estar 'pronto'. Modelos evoluem, clientes mudam, o mercado se transforma. O objetivo não é um sistema perfeito. É um sistema que se auto-melhora — que detecta seus próprios erros, aprende com eles, e fica melhor a cada semana sem depender de um Fernando para liderar cada iniciativa."*

**Ação prática:** A métrica final de sucesso não é "precisão = 99%". É "quantas melhorias o time implementou este mês sem que ninguém precisasse mandar?"

---

## 📋 "O Que Você Aprendeu" — Resumo do Case Study

Este case study percorreu 6 meses de evolução do KODA. Aqui está o que você deve levar consigo:

### Conceitos Fundamentais

1. **Melhoria contínua não é um projeto — é um processo.** Tem começo mas não tem fim. O KODA de junho é melhor que o de janeiro, mas o de dezembro será melhor que o de junho.

2. **Medir antes de mudar.** A baseline de janeiro permitiu quantificar cada melhoria. Sem baseline, você não sabe se melhorou ou piorou.

3. **Feedbacks são o combustível da melhoria.** Sem canais de feedback do cliente para o código, você está voando cego. Os 4 gaps de feedback do KODA (cliente→KODA, operação→engenharia, métricas→ação, correção→validação) são universais — todo sistema de IA os tem.

4. **Rubrics precisam aprender.** Uma rubric estática é uma fotografia do passado. Uma rubric adaptativa é um sistema vivo que evolui com os padrões de falha.

5. **Simplificar é tão importante quanto construir.** O harness de maio tinha menos componentes que o de janeiro, mas era mais eficaz. A "Lei de Fernando" — "se eu remover, qual métrica piora?" — deve guiar toda decisão de arquitetura.

6. **Modelos evoluem, harness deve acompanhar.** O que era necessário com o modelo de janeiro (3 verificações de preço) era desperdício com o modelo de maio. A evolução do harness é tão importante quanto a evolução do modelo.

7. **Sycophancy se resolve com separação de responsabilidades.** Generator/Evaluator não é um padrão opcional — é a fundação para qualquer sistema de IA que precise de qualidade consistente.

8. **Cultura se constrói com rituais, não com decretos.** Daily feedback, weekly retro, monthly calibration. Quando está na agenda, acontece. Quando depende de inspiração, não acontece.

### Habilidades Práticas

Você agora é capaz de:

- ✅ Desenhar um sistema de telemetria completo para agentes de IA
- ✅ Implementar ciclos de feedback em 3 camadas (imediato, diário, estrutural)
- ✅ Criar rubrics adaptativas com calibragem automática
- ✅ Aplicar a "Lei de Fernando" para decidir o que remover do harness
- ✅ Construir dashboards de métricas que mostram progresso real
- ✅ Escolher a estratégia de coordenação correta para cada escala
- ✅ Liderar uma cultura de melhoria contínua em times de AI engineering

---

## 📋 Architecture Decision Records (ADRs)

Durante os 6 meses do programa KCI, o time documentou decisões arquiteturais críticas no formato ADR. Esta seção reproduz as 5 ADRs mais importantes.

### ADR-001: Programa KCI — 6 Meses sem Novas Features

```
Status: ACCEPTED
Data: 2026-01-10
Deciders: Fernando (CTO), CEO, VP de Produto

CONTEXT:
O KODA tem 38% de falsos positivos (promessas quebradas) e métricas
de qualidade estagnadas há 3 meses. O backlog de produto tem 12
features novas. A engenharia está sobrecarregada mantendo componentes
legados de 3 MVPs. Precisamos decidir: continuar adicionando features
ou parar para melhorar a fundação.

Opções consideradas:
1. CONTINUAR NORMAL: Features novas + correções pontuais (status quo)
2. PAUSA PARCIAL: 50% do time em features, 50% em melhorias
3. PAUSA TOTAL: 100% do time em melhorias por 6 meses

DECISION:
Pausa total por 6 meses. Zero features novas. Programa KODA
Continuous Improvement (KCI).

RATIONALE:
- 38% de falsos positivos significa que qualquer feature nova herda
  esse problema de qualidade
- Componentes legados consomem 40% do tempo de engenharia em
  manutenção
- Métricas de negócio (churn 8%, CSAT 70%) mostram que a fundação
  está rachada
- O custo de NÃO parar é maior que o custo de parar
- 6 meses é suficiente para ver resultados mensuráveis
- Revisão trimestral permite ajustar curso se necessário

CONSEQUENCES:
✅ Foco total em qualidade, telemetria e simplificação
✅ Redução de dívida técnica documentada e mensurável
⚠️ 12 features no backlog congeladas por 6 meses
⚠️ Pressão do time de produto e marketing
⚠️ Risco de concorrentes lançarem features que não temos
⚠️ Requer disciplina para não "só essa featurezinha rápida"
```

### ADR-002: Telemetria Antes de Qualquer Mudança

```
Status: ACCEPTED
Data: 2026-01-17
Deciders: Tech Lead, 2 Senior Engineers

CONTEXT:
Precisamos melhorar o KODA, mas não sabemos exatamente o que está
quebrado. Temos opiniões, não dados. A primeira decisão do KCI é:
começamos melhorando coisas baseados em intuição, ou investimos em
telemetria primeiro?

Opções:
1. MELHORAR JÁ: Começar pelas melhorias "óbvias" (prompts, cache)
2. TELEMETRIA PRIMEIRO: 2 semanas só implementando medição
3. HÍBRIDO: Telemetria + melhorias em paralelo

DECISION:
Telemetria primeiro. 2 semanas dedicadas a instrumentação.
Nenhuma mudança de comportamento até ter baseline.

RATIONALE:
- "O óbvio" frequentemente está errado (ex: todo mundo achava que
  o problema era o modelo, mas era o harness)
- Sem baseline, não sabemos se uma mudança melhorou ou piorou
- Telemetria implementada corretamente se paga em 2 meses
  (ex: descobrimos que Cache Manager custava $360/mês sem melhorar
  nenhuma métrica)
- Dados criam alinhamento: "os números dizem X" substitui "eu acho X"

CONSEQUENCES:
✅ Baseline de métricas estabelecida com precisão
✅ Decisões baseadas em dados, não em intuição
✅ Descoberta de componentes desnecessários (Cache Manager)
⚠️ 2 semanas sem melhorias visíveis (pressão da liderança)
⚠️ Custo de implementação: ~$8.000 em salário
⚠️ Telemetria adiciona 2-3% de overhead de latência
```

### ADR-003: Calibragem Automática de Rubrics com Supervisão Humana

```
Status: ACCEPTED
Data: 2026-03-28
Deciders: Tech Lead, ML Engineer, QA Lead

CONTEXT:
As rubrics do KODA foram definidas em janeiro e nunca atualizadas.
O sistema evoluiu (modelos melhores, novos padrões de falha), mas
as rubrics continuam as mesmas. Precisamos de um mecanismo para
manter rubrics atualizadas sem sobrecarregar o time.

Opções:
1. MANUAL: Revisão humana mensal das rubrics
2. AUTOMÁTICO: Sistema recalibra pesos automaticamente
3. HÍBRIDO: Sistema sugere, humanos aprovam

DECISION:
Híbrido. Sistema analisa taxas de falha a cada 2 semanas e sugere
novos pesos. Time revisa e aprova/rejeita em 30 minutos.

RATIONALE:
- Revisão 100% manual não escala (17 rubrics × 5-8 dimensões cada)
- Revisão 100% automática corre risco de overfitting e viés
- 2 semanas é frequente o suficiente para capturar mudanças e
  espaçado o suficiente para ter dados significativos
- Supervisão humana é safety net contra decisões automáticas ruins
- Tempo de revisão: 30min a cada 2 semanas (sustentável)

CONSEQUENCES:
✅ Rubrics sempre atualizadas com padrões reais de falha
✅ Overfitting mitigado por revisão humana
✅ Custo de manutenção baixo (1h/mês do time)
⚠️ Se o time pular a revisão, rubrics podem divergir
⚠️ Requer disciplina no ritual quinzenal
⚠️ Threshold de "dados significativos" precisa de ajuste inicial
```

### ADR-004: Remoção Agressiva de Componentes — "Lei de Fernando"

```
Status: ACCEPTED
Data: 2026-04-10
Deciders: Fernando (CTO), Tech Lead, todos os engenheiros

CONTEXT:
O harness do KODA acumulou 8 componentes ao longo de 8 meses.
Alguns são legados de MVPs, outros foram adicionados "por via das
dúvidas". O time gasta 40% do tempo mantendo componentes cuja
utilidade nunca foi validada. Precisamos de um processo para
decidir o que remover.

Opções:
1. GRADUAL: Remover 1 componente por mês, com análise profunda
2. AGRESSIVO: Testar remoção de todos os componentes candidatos
3. CONSERVADOR: Não remover nada "que está funcionando"

DECISION:
Agressivo. Para cada componente, teste de remoção em staging por
48h. Se métricas não piorarem, remove permanentemente.

RATIONALE:
- Abordagem gradual (1 por mês) levaria 8 meses para limpar o
  harness atual — tempo demais
- "Está funcionando" não é justificativa para manter — tudo tem
  custo de manutenção, debugging, onboarding
- Teste de 48h em staging é seguro (zero impacto em produção)
- Rollback é trivial (reverter commit)
- 4 componentes removidos = $1.500/mês de economia + tempo de
  engenharia liberado

CONSEQUENCES:
✅ Harness simplificado: 8 → 6 componentes
✅ Economia: $1.500/mês em infra + ~60h/mês de engenharia
✅ Sistema mais simples de entender, debugar e onboard
⚠️ Risco de remover algo necessário (mitigado por teste de 48h)
⚠️ Desconforto inicial do time ("medo de remover")
⚠️ Requer documentação do que foi removido e por quê
```

### ADR-005: Métricas de Qualidade como OKRs do Time

```
Status: ACCEPTED
Data: 2026-05-05
Deciders: Fernando (CTO), VP de Produto, Tech Lead

CONTEXT:
O programa KCI está no mês 5. As métricas melhoraram
significativamente, mas o time ainda trata "qualidade" como
responsabilidade do QA, não de todos. Precisamos internalizar
métricas de qualidade nos objetivos do time.

Opções:
1. SEPARADO: Time de engenharia foca em features, QA foca em
   qualidade (modelo tradicional)
2. COMPARTILHADO: Métricas de qualidade são OKRs de todos
3. RODÍZIO: Cada sprint, um engenheiro é "dono da qualidade"

DECISION:
Compartilhado. Métricas de qualidade (precisão, falsos positivos,
CSAT, MTTD) são OKRs do time inteiro, com peso igual a métricas
de entrega (velocity, throughput).

RATIONALE:
- Qualidade não é responsabilidade de um papel — é propriedade
  do sistema
- Quando QA é dono da qualidade, engenharia otimiza para
  velocidade e QA vira gargalo
- OKRs compartilhados alinham incentivos: código rápido mas
  quebrado prejudica todo mundo
- Métricas de qualidade são leading indicators de métricas de
  negócio (churn, receita)

CONSEQUENCES:
✅ Alinhamento de incentivos: todo mundo quer qualidade
✅ QA deixa de ser gargalo e vira parceiro estratégico
✅ Melhorias de qualidade são proativas, não reativas
⚠️ Requer mudança cultural (engenheiros acostumados a "jogar por
   cima do muro" para QA)
⚠️ Métricas de qualidade podem conflitar com prazos (requer
   negociação consciente)
⚠️ Medir qualidade de forma justa é difícil (evitar "gaming"
   das métricas)
```

---

## 💰 Business Impact: O Retorno do Investimento em Melhoria Contínua

### Análise de Custo-Benefício do Programa KCI

Muitas vezes, iniciativas de melhoria contínua são vistas como "custo" pela liderança. O time KODA quantificou o retorno financeiro para justificar o investimento.

#### Investimento Total (6 meses)

| Categoria | Custo | Detalhe |
|-----------|-------|---------|
| **Salários (2 engenheiros dedicados)** | $96.000 | 2 FTE × 6 meses × $8.000/mês |
| **Infraestrutura adicional (telemetria)** | $1.200 | SQLite + storage para eventos |
| **Ferramentas (dashboard, monitoring)** | $800 | Configuração inicial |
| **Custo de oportunidade (12 features)** | $0* | *Valor não realizado, não custo real |
| **TOTAL** | **$98.000** | Investimento total em 6 meses |

#### Economias Geradas (recorrentes, por mês)

| Categoria | Economia/mês | Detalhe |
|-----------|-------------|---------|
| **Infraestrutura removida** | $1.510 | Componentes legados (Validator, Cache, Rerouter) |
| **Tempo de engenharia liberado** | $4.800 | 60h/mês não gastas mantendo componentes obsoletos |
| **Redução de cancelamentos** | $5.400 | Churn caiu de 8% para 2% (180 clientes × $30/mês) |
| **Redução de suporte** | $3.240 | FCR subiu de 62% para 87% (menos tickets) |
| **Redução de devoluções** | $2.800 | Taxa de devolução caiu de 15% para 4% |
| **Tokens economizados** | $1.900 | Custo/conversa caiu de $0.47 para $0.21 |
| **TOTAL** | **$19.650/mês** | Economia recorrente mensal |

#### Payback e ROI

```
RETORNO SOBRE INVESTIMENTO (ROI) DO PROGRAMA KCI
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Investimento total:     $98.000
Economia mensal:        $19.650
Payback:                5.0 meses (após o fim do programa)
Economia em 12 meses:   $235.800
Economia em 24 meses:   $471.600
ROI em 12 meses:        141%
ROI em 24 meses:        381%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Além do financeiro (difícil de quantificar, mas real):

• Confiança do cliente: CSAT de 70% → 91% (+21pp)
  → Clientes satisfeitos compram mais, indicam amigos, voltam

• Velocidade de engenharia: MTTD de 4.2h → 30min (-86%)
  → Bugs são resolvidos em minutos, não dias

• Moral do time: Engenheiros passaram de "apagadores de incêndio"
  para "construtores de plataforma"
  → Retenção de talentos, menos burnout

• Vantagem competitiva: KODA entrega 95% de precisão vs 75% da
  concorrência (estimado)
  → Diferencial de mercado difícil de copiar
```

### O Custo de NÃO Fazer Melhoria Contínua

Para convencer stakeholders céticos, o time KODA projetou o cenário alternativo: o que teria acontecido se tivessem continuado adicionando features sem melhorar a fundação.

```
CENÁRIO ALTERNATIVO: "CONTINUAR NORMAL" (SEM KCI)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Mês 1-2: 3 novas features lançadas
  → Falsos positivos: 38% → 42% (features novas = mais promessas quebradas)
  → CSAT: 70% → 65% (clientes mais frustrados)

Mês 3-4: +3 features, total de 18 features no backlog "entregues"
  → Churn: 8% → 12% (clientes abandonando)
  → Custo de suporte: +40% (mais reclamações)

Mês 5-6: +3 features, pressão por crescimento
  → Tempo de engenharia: 70% em manutenção de legado, 30% em features
  → MTTD: 4.2h → 8h (sistema mais complexo = debug mais lento)

PROJEÇÃO FINANCEIRA (6 meses):
  Receita adicional (features novas):    +$40.000 (estimado)
  Perda por churn aumentado:            -$72.000
  Custo de suporte adicional:           -$28.000
  Custo de manutenção de legado:        -$35.000
  ─────────────────────────────────────────────
  RESULTADO LÍQUIDO:                    -$95.000

CONCLUSÃO: "Continuar normal" teria custado $95.000 em 6 meses.
           O KCI custou $98.000 e gerou $19.650/mês de economia recorrente.
           A escolha foi clara.
```

---

## 🔄 Estratégia de Transição: Do Modo "Apagar Incêndio" para "Melhoria Contínua"

### Como o Time Mudou sua Forma de Trabalhar

A transição de um time que "apaga incêndios" para um time que pratica melhoria contínua não acontece da noite para o dia. O KODA passou por 3 fases de transição:

#### Fase 1: Choque Cultural (Janeiro 2026)

```
SINTOMAS DA FASE 1:
━━━━━━━━━━━━━━━━━
• "Mas como assim não vamos lançar features?"
• "Isso é contraproducente, o concorrente vai nos ultrapassar"
• "O CEO aprovou mesmo isso?"
• "2 semanas só fazendo telemetria? Não era mais fácil arrumar o prompt?"

AÇÕES DO FERNANDO:
• Mostrou os números: 38% de falsos positivos, 8% de churn
• "Não estou pedindo opinião. Estou pedindo 6 meses."
• Celebrou cada pequena vitória (primeiro dashboard, primeira métrica)
• Protegeu o time da pressão externa (produto, marketing, CEO)

DURAÇÃO: 3-4 semanas
```

#### Fase 2: Evidência (Fevereiro-Abril 2026)

```
SINTOMAS DA FASE 2:
━━━━━━━━━━━━━━━━━
• "Olha só, o Cache Manager realmente não servia pra nada"
• "Removi o Validator V1 e nada quebrou!"
• "Nossa, o dashboard mostra exatamente onde está o problema"
• "O feedback do cliente virou ação em 48 horas!"

MUDANÇA DE COMPORTAMENTO:
• Time começa a perguntar: "Dá pra remover isso?" em vez de "Dá pra adicionar?"
• Métricas são citadas em conversas de corredor
• "O que os números dizem?" vira frase comum

DURAÇÃO: 8-10 semanas
```

#### Fase 3: Internalização (Maio-Junho 2026)

```
SINTOMAS DA FASE 3:
━━━━━━━━━━━━━━━━━
• Time agenda os rituais de melhoria contínua sozinho
• Novos engenheiros recebem learning cards no onboarding
• "Isso vai contra a Lei de Fernando" vira argumento em code review
• Alguém sugere remover um componente e ninguém questiona "mas e se precisar?"

MUDANÇA DE COMPORTAMENTO:
• Melhoria contínua não é mais "o projeto do Fernando" — é "como trabalhamos"
• Time se auto-organiza para identificar e corrigir problemas
• Métricas de qualidade competem com métricas de velocidade

DURAÇÃO: Indefinida (processo contínuo)
```

### Sinais de Que a Cultura de Melhoria Contínua Está Funcionando

| Sinal | Janeiro (antes) | Junho (depois) |
|-------|-----------------|----------------|
| **Quem sugere melhorias?** | Só o Fernando | Qualquer pessoa do time |
| **Decisões baseadas em?** | Intuição, experiência, "eu acho" | Dados, métricas, telemetria |
| **Componentes do harness** | Acumulando (ninguém remove) | Diminuindo (remoção é celebrada) |
| **Reação a incidentes** | "Corrige rápido e segue" | "Learning card, causa raiz, previne" |
| **Templates de prompt** | 15 versões, cada um usa a sua | 4 versionadas, controle no Git |
| **Métricas de qualidade** | Não existem | Visíveis no dashboard, OKRs do time |
| **Feedbacks de cliente** | Se perdem no Slack | Sistema de 3 camadas com SLA |
| **Rituais de melhoria** | Nenhum | Daily feedback, weekly retro, monthly cal |

### O Que Fazer Quando a Melhoria Contínua Encontra Resistência

Durante os 6 meses, o time encontrou resistência em vários momentos. Aqui está como lidaram:

```
CENÁRIO 1: LIDERANÇA QUER VOLTAR A LANÇAR FEATURES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Situação: No mês 3, o VP de Produto pressionou: "Já melhoramos bastante,
          podemos voltar a lançar features?"

Resposta do time:
• Mostraram o dashboard: falsos positivos ainda em 23% (alvo: 5%)
• "Se lançarmos features agora, o ganho de qualidade dos últimos 3 meses
   será diluído. A fundação ainda não está pronta."
• Negociaram: liberar 1 feature pequena (não crítica) como prova de que
   o processo funciona

Resultado: VP concordou em esperar até o mês 5. Feature liberada no mês 5
          foi lançada com 95% de cobertura de testes e zero incidentes.

CENÁRIO 2: ENGENHEIRO QUER ADICIONAR COMPONENTE "POR SEGURANÇA"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Situação: Engenheiro sugeriu adicionar um "DoubleValidator" que verificaria
          as recomendações duas vezes, "só por segurança".

Resposta do time:
• "Qual métrica vai melhorar com esse componente?"
• "Qual o custo? (latência, tokens, complexidade)"
• "Vamos testar em staging: adiciona o componente e mede por 48h"

Resultado: O DoubleValidator adicionou 1.2s de latência e melhorou a
          precisão em apenas 0.3%. Foi rejeitado. Engenheiro aprendeu
          a pensar em custo-benefício antes de propor adições.

CENÁRIO 3: TIME RESISTE A REMOVER COMPONENTE "QUE DEU TRABALHO"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Situação: O Validator V1 foi construído pelo engenheiro mais sênior do time.
          Ele levou 3 semanas para implementar. O time tinha apego emocional.

Resposta do Fernando:
• "Eu sei que deu trabalho. Eu sei que foi bem feito. Mas o sistema evoluiu.
   O Validator V1 foi essencial em janeiro. Em maio, é peso morto."
• "Honramos o trabalho removendo-o com respeito, documentando o que aprendemos,
   e aplicando esse aprendizado no que construímos depois."

Resultado: Time removeu o Validator V1 e documentou o aprendizado em um
          learning card. O engenheiro que o construiu liderou a remoção.
```

---

## 🧪 Exercícios

### Exercício 1: Diagnóstico de Baseline

**Objetivo:** Aplicar o processo de diagnóstico inicial em um sistema hipotético.

**Contexto:** Você é o novo Tech Lead de um agente de IA chamado "BOT-VENDAS", similar ao KODA. O sistema atual tem:
- Precisão de recomendações: 68%
- Tempo médio de conversa: 3.1 horas
- Custo por conversa: $0.62
- Sem telemetria implementada
- Sem separação Generator/Evaluator
- 3 MVPs legados ainda ativos

**Tarefa:**
1. Liste as 5 primeiras ações que você tomaria na Semana 1
2. Defina as 3 métricas principais que você estabeleceria como baseline
3. Desenhe um plano de 4 semanas para implementar telemetria
4. Identifique quais componentes legados provavelmente podem ser removidos

**Tempo estimado:** 30-45 minutos

---

### Exercício 2: Calibragem de Rubric

**Objetivo:** Recalibrar uma rubric baseado em dados de falha.

**Contexto:** A rubric atual do BOT-VENDAS tem estas dimensões:

| Dimensão | Peso | Falhas (últimas 2 semanas) |
|----------|------|---------------------------|
| Preço | 35% | 2 falhas |
| Estoque | 25% | 8 falhas |
| Entrega | 20% | 12 falhas |
| Descrição | 15% | 1 falha |
| Upsell | 5% | 18 falhas |

**Tarefa:**
1. Recalibre os pesos baseado na taxa de falha
2. Qual threshold de aprovação você sugeriria se a taxa atual de falsos positivos é 28%?
3. Que dimensão nova você adicionaria baseado nos dados?
4. Justifique cada mudança em 1-2 frases

**Tempo estimado:** 20-30 minutos

---

### Exercício 3: Simplificação de Harness

**Objetivo:** Aplicar a "Lei de Fernando" para decidir o que remover.

**Contexto:** O BOT-VENDAS tem 12 componentes no harness:

| Componente | Função | Custo/mês | Latência | Dono |
|------------|--------|-----------|----------|------|
| PriceChecker | Validar preços | $120 | 0.8s | @joao |
| StockChecker | Validar estoque | $95 | 1.2s | @maria |
| DeliveryCalc | Calcular frete | $80 | 2.1s | @carlos |
| SpellCheck | Corrigir ortografia | $15 | 0.2s | ninguém |
| DuplicateDetector | Evitar recomendar 2x | $45 | 0.5s | @joao |
| SentimentAnalyzer | Analisar tom do cliente | $200 | 1.8s | ninguém |
| HistoryCompressor | Comprimir histórico | $60 | 0.4s | @maria |
| CacheManager | Cache de respostas | $30 | 0.1s | ninguém |
| PromptFormatter | Formatar prompts | $10 | 0.05s | @carlos |
| ResponseValidator | Validar resposta final | $150 | 1.5s | @joao |
| LogAggregator | Agregar logs | $40 | 0.3s | ninguém |
| MetricsCollector | Coletar métricas | $50 | 0.2s | @maria |

**Tarefa:**
1. Identifique 4 componentes candidatos à remoção
2. Para cada um, explique: "Se eu remover, qual métrica piora?"
3. Priorize: quais removeria primeiro?
4. Estime a economia total se todas as remoções forem aprovadas

**Tempo estimado:** 25-35 minutos

---

### Exercício 4: Design de Ciclo de Feedback

**Objetivo:** Desenhar um sistema de feedback para uma feature específica.

**Contexto:** O BOT-VENDAS vai lançar uma feature de "recomendação personalizada por humor do cliente" (detecta se o cliente está feliz, neutro ou irritado pelo tom das mensagens).

**Tarefa:**
1. Desenhe o sistema de feedback em 3 camadas para esta feature
2. Defina os eventos de telemetria que precisam ser emitidos
3. Crie um template de relatório diário de feedback
4. Estabeleça SLAs para cada tipo de feedback
5. Descreva como os feedbacks desta feature alimentariam a recalibragem da rubric

**Tempo estimado:** 40-50 minutos

---

### Exercício 5: Learning Card

**Objetivo:** Documentar um aprendizado no formato de Learning Card.

**Contexto:** Durante o lançamento da feature de recomendação por humor, o time descobriu que clientes "irritados" recebiam recomendações 40% mais caras que clientes "felizes" — o modelo associava irritação com "cliente exigente que quer produtos premium".

**Tarefa:**
1. Crie um Learning Card completo para este incidente
2. Inclua: data, severidade, causa raiz, ação tomada, validação, lição
3. Adicione tags relevantes
4. Escreva a "lição" em uma frase que capture o aprendizado para sempre

**Tempo estimado:** 15-20 minutos

---

## 💡 Dicas e Gabaritos dos Exercícios

Estas dicas ajudam a verificar seu raciocínio. Não existe "resposta certa" única — o importante é o processo de pensamento.

### Dicas — Exercício 1 (Diagnóstico de Baseline)

1. **5 primeiras ações na Semana 1:**
   - Implementar telemetria em TODOS os componentes (sem exceção)
   - Estabelecer baseline de métricas de qualidade (não só uptime)
   - Mapear todos os componentes do harness e seus donos
   - Identificar os 4 gaps de feedback (cliente, operação, métricas, correção)
   - Criar dashboard visível para todo o time

2. **3 métricas principais de baseline:**
   - Precisão de recomendações (ou equivalente para o domínio)
   - Falsos positivos (promessas quebradas)
   - CSAT ou NPS (satisfação do cliente)

3. **Plano de 4 semanas para telemetria:**
   - Semana 1: Instrumentar core do agente (decisões principais)
   - Semana 2: Instrumentar componentes periféricos (cache, validação, APIs)
   - Semana 3: Criar dashboard e alertas
   - Semana 4: Validar dados (comparar com observação manual)

4. **Componentes legados candidatos à remoção:**
   - Cache Manager (se não melhora métrica nenhuma)
   - Validator antigo (se substituído por Generator/Evaluator)
   - Qualquer componente sem dono documentado
   - Componentes com custo > $50/mês sem melhoria mensurável

### Dicas — Exercício 2 (Calibragem de Rubric)

1. **Pesos recalibrados:**
   - Upsell: ~43% (18 falhas de 41 totais) — era 5%, claramente subvalorizado
   - Entrega: ~29% (12 falhas)
   - Estoque: ~20% (8 falhas)
   - Preço: ~5% (2 falhas) — era 35%, claramente supervalorizado
   - Descrição: ~3% (1 falha)
   - **Lógica:** Peso proporcional à taxa de falha. Dimensões que mais falham precisam de mais peso.

2. **Threshold sugerido:** 82-85. Com falsos positivos em 28%, o threshold atual está muito baixo. Elevar para 85 deve reduzir falsos positivos para ~12-15%. Monitorar approval rate após mudança.

3. **Nova dimensão:** "Consistência cross-sell" — upsells com 18 falhas em 2 semanas sugere que recomendações complementares estão se contradizendo. Uma dimensão que verifica se os produtos recomendados juntos fazem sentido.

### Dicas — Exercício 3 (Simplificação de Harness)

1. **4 componentes candidatos à remoção (em ordem de prioridade):**

   **#1: SentimentAnalyzer ($200/mês, 1.8s, sem dono)**
   - "Se eu remover, qual métrica piora?" → Provavelmente nenhuma. Análise de sentimento raramente afeta qualidade de recomendação. Custo alto, sem dono = remover primeiro.

   **#2: SpellCheck ($15/mês, 0.2s, sem dono)**
   - "Se eu remover, qual métrica piora?" → Modelos modernos raramente erram ortografia. Baixo custo, mas baixo valor também. Provavelmente desnecessário.

   **#3: CacheManager ($30/mês, 0.1s, sem dono)**
   - "Se eu remover, qual métrica piora?" → Cache pode ser útil, mas sem dono e sem métricas de efetividade documentadas, é suspeito. Latência pode subir um pouco, mas provavelmente insignificante.

   **#4: DuplicateDetector ($45/mês, 0.5s)**
   - "Se eu remover, qual métrica piora?" → Tem dono (@joao), mas se o Generator for bem construído, não deve recomendar duplicatas. Testar em staging.

2. **Economia total:** $200 + $15 + $30 + $45 = $290/mês em custo direto, mais latência reduzida em 2.6s e tempo de manutenção liberado.

### Dicas — Exercício 4 (Design de Ciclo de Feedback)

1. **Sistema de 3 camadas para feature de humor:**

   **Camada 1 (Imediata):** Eventos de telemetria
   - `mood_detected` (qual humor foi detectado?)
   - `recommendation_generated_for_mood` (o que foi recomendado?)
   - `mood_mismatch` (cliente reagiu negativamente à recomendação?)

   **Camada 2 (Diária):** Relatório automático
   - Distribuição de humores detectados (feliz/neutro/irritado)
   - Preço médio de recomendação por humor
   - Taxa de aceitação por humor
   - Alertas se algum humor tem taxa de aceitação anormal

   **Camada 3 (Estrutural):** Análise semanal
   - Correlação humor × preço recomendado (evitar viés)
   - Segmentos onde a feature funciona bem vs mal
   - Ajustes na rubric de recomendação baseado em padrões

2. **Eventos de telemetria:**
   - `mood_detection_start` / `mood_detection_complete` (latência, confiança)
   - `recommendation_context` (humor detectado, histórico do cliente)
   - `recommendation_result` (produtos, preços, scores)
   - `customer_reaction` (aceitou, rejeitou, questionou, reclamou)

3. **SLAs:**
   - Mood mismatch detectado pelo cliente: análise em 1h, correção em 24h
   - Viés de preço por humor: análise em 24h, correção em 72h
   - Queda na taxa de aceitação: alerta imediato, análise em 4h

### Dicas — Exercício 5 (Learning Card)

Modelo de resposta:

```
LEARNING CARD #XXX — "Modelo associa cliente irritado com cliente premium"

DATA: [data do incidente]
SEVERIDADE: 🔴 Alta
AUTOR: @[seu nome]
TAGS: #recomendação #viés #mood-detection #rubric

O QUE ACONTECEU:
O sistema de recomendação por humor detectava clientes irritados e
os tratava como "clientes exigentes que querem produtos premium",
resultando em recomendações 40% mais caras.

CAUSA RAIZ:
O modelo aprendeu uma correlação espúria nos dados de treinamento:
clientes que compram produtos premium tendem a ser mais detalhistas
nas perguntas, o que o detector de humor interpretava como "irritação".
Viés de confirmação: o modelo não foi treinado para separar "cliente
detalhista" de "cliente irritado".

AÇÃO TOMADA:
1. Adicionada dimensão "Equidade de Preço por Humor" na rubric (peso 15%)
2. Implementado monitoramento: diferença de preço médio entre humores
   não pode exceder 10%
3. Retreinado o detector de humor com exemplos de "cliente detalhista
   mas não irritado"
4. Adicionado teste de regressão: para o mesmo perfil de cliente,
   mudar o humor não deve mudar o preço médio recomendado em > 10%

VALIDAÇÃO:
48h após correção: diferença de preço entre humores caiu de 40% para 7%.
Monitorado por 2 semanas: zero recorrências.

LIÇÃO:
"Modelos aprendem correlações, não causalidades. Toda feature que usa
detecção de atributos humanos (humor, sentimento, urgência) precisa
de uma dimensão de equidade na rubric para evitar que o modelo
reforce vieses dos dados de treinamento."
```

---

## 📋 Templates Práticos para o Dia a Dia

### Template: Relatório Diário de Feedback

Use este template no Slack ou ferramenta de comunicação do time:

```
📊 KODA Daily Feedback — [DATA]

🔴 CRÍTICO ([N] eventos — requer ação em < 24h):
  • [evento 1] — [breve descrição] — dono: @[nome] — prazo: [data]
  • [evento 2] — [breve descrição] — dono: @[nome] — prazo: [data]

🟡 ATENÇÃO ([N] eventos — monitorar):
  • [evento 1] — [breve descrição]
  • [evento 2] — [breve descrição]

🟢 POSITIVO ([N] eventos):
  • [evento 1] — [breve descrição]

📈 TENDÊNCIA:
  • [métrica] subiu/caiu [X]% em relação à semana anterior
  • [observação relevante]

🎯 AÇÕES DE ONTEM:
  • [ação 1]: ✅ concluída / ⏳ em andamento / ❌ bloqueada
  • [ação 2]: ✅ concluída / ⏳ em andamento / ❌ bloqueada
```

### Template: Retrospectiva Semanal de Melhoria Contínua

```
🔄 KODA Weekly Retro — Semana [N]

1. O QUE MELHOROU ESTA SEMANA?
   (3-5 itens, com dados)
   • [métrica] passou de [X] para [Y] → delta: [+Z%]
   • [componente] foi otimizado → impacto: [descrição]

2. O QUE PIOROU ESTA SEMANA?
   (3-5 itens, com dados)
   • [métrica] caiu de [X] para [Y] → investigar causa
   • [incidente] ocorreu [N] vezes → learning card criado

3. O QUE APRENDEMOS ESTA SEMANA?
   (2-3 aprendizados)
   • [aprendizado 1]
   • [aprendizado 2]

4. O QUE VAMOS REMOVER NA PRÓXIMA SEMANA?
   (1-2 candidatos)
   • [componente] — testar remoção em staging
   • [processo] — simplificar ou eliminar

5. LEARNING CARDS CRIADOS:
   • LC #[N]: [título] — @[autor]
   • LC #[N]: [título] — @[autor]

6. MÉTRICAS DA SEMANA:
   | Métrica | Esta Semana | Semana Anterior | Delta |
   |---------|-------------|-----------------|-------|
   | Precisão | [X]% | [Y]% | [±Z]pp |
   | Falsos + | [X]% | [Y]% | [±Z]pp |
   | CSAT | [X]% | [Y]% | [±Z]pp |
   | Custo/conv | $[X] | $[Y] | $[±Z] |
   | MTTD | [X]min | [Y]min | [±Z]min |
```

### Template: Proposta de Remoção de Componente

Use este template antes de remover qualquer componente do harness:

```
🗑️ PROPOSTA DE REMOÇÃO — [NOME DO COMPONENTE]

COMPONENTE:
  Nome: [nome]
  Função: [o que faz]
  Criado em: [data]
  Dono atual: @[nome] (ou "ninguém" — 🚨 risco)

CUSTO ATUAL:
  Financeiro: $[X]/mês
  Latência: [X]s por operação
  Manutenção: ~[X]h/mês da engenharia
  Complexidade: [número de arquivos/LoC]

JUSTIFICATIVA PARA REMOÇÃO:
  (responda obrigatoriamente)
  "Se eu remover este componente, qual métrica piora?"
  Resposta: [métrica específica ou "nenhuma — testado em staging"]

TESTE DE REMOÇÃO (staging, 48h):
  Período: [data início] a [data fim]
  Métricas comparadas:
  | Métrica | Com componente | Sem componente | Delta |
  |---------|---------------|----------------|-------|
  | [nome]  | [valor]       | [valor]        | [±X%] |

DECISÃO:
  [ ] REMOVER permanentemente (métricas não pioraram)
  [ ] SIMPLIFICAR (métricas pioraram pouco — manter versão reduzida)
  [ ] MANTER (métricas pioraram significativamente — componente é necessário)

APROVAÇÕES:
  @[tech lead]: [aprovar/rejeitar]
  @[dono do componente]: [aprovar/rejeitar]
  @[QA lead]: [aprovar/rejeitar]
```

---

## ❓ Perguntas Frequentes

### P: "Quanto tempo leva para ver resultados de melhoria contínua?"

**R:** Os primeiros 2 meses são lentos — melhorias de 2-5 pontos percentuais. Do mês 3 em diante, o efeito composto acelera. O KODA levou 6 meses para ir de 75% para 95% de precisão. Mas se você parar no mês 2 achando que "não está funcionando", nunca verá a aceleração.

### P: "Como convencer a liderança a investir em melhoria contínua em vez de novas features?"

**R:** O argumento do KODA foi simples: "Se 38% das nossas promessas são quebradas, cada feature nova que adicionarmos vai herdar esse problema. Estamos construindo em cima de uma fundação rachada." Apresente dados de falsos positivos, custo de suporte, e churn. Melhoria contínua não é "não fazer features" — é "fazer features em cima de uma base sólida".

### P: "Rubrics adaptativas não correm o risco de overfitting?"

**R:** Sim, é um risco real. Por isso o KODA usa calibragem automática apenas como **sugestão**. O time revisa as sugestões e aprova ou rejeita. Além disso, a métrica de "approval rate" (quantas recomendações são aprovadas) é monitorada: se cair abaixo de 50%, a rubric está muito rigorosa.

### P: "Qual o custo de implementar telemetria em todos os componentes?"

**R:** O KODA gastou 2 semanas de 2 engenheiros (≈ $8.000 em salário) para implementar telemetria completa. O retorno: a telemetria permitiu identificar que o Cache Manager (legado do MVP2) custava $360/mês sem melhorar nenhuma métrica. Só essa descoberta pagou o investimento em 2 meses.

### P: "Como saber se um componente do harness é realmente necessário?"

**R:** Teste em staging por 48h. Remova o componente. Compare as métricas com e sem ele. Se nenhuma métrica piorou, remova permanentemente. O KODA removeu 4 componentes assim e economizou $1.500/mês. Se uma métrica piorar, o componente é necessário — mas pergunte se ele pode ser simplificado.

### P: "Isso funciona para times pequenos?"

**R:** Sim, e é ainda mais importante. Times pequenos não têm banda para manter componentes desnecessários. A "Lei de Fernando" (remover o que não serve) é mais crítica para times de 3-5 pessoas do que para times de 20+. Cada componente removido é um componente que você não precisa manter, debugar, documentar e ensinar para novos membros.

### P: "Com que frequência devo recalibrar as rubrics?"

**R:** O KODA recalibra a cada 2 semanas. Esse intervalo foi escolhido porque: (1) é frequente o suficiente para capturar mudanças nos padrões de falha, (2) é espaçado o suficiente para ter dados estatisticamente significativos, (3) coincide com o ciclo de sprint do time. Se seu volume é menor, recalibre mensalmente.

### P: "E se a simplificação do harness quebrar algo em produção?"

**R:** O KODA nunca remove direto em produção. O processo é: (1) remover em staging por 48h, (2) comparar métricas, (3) se OK, deploy em canary (10% do tráfego), (4) monitorar 24h, (5) rollout gradual até 100%. Em 4 remoções, zero incidentes em produção.

### P: "Como lidar com a frustração do time quando melhorias são lentas?"

**R:** Nos meses 1-2, o time KODA ficou frustrado. "Estamos há 2 meses nisso e a precisão só subiu 7 pontos percentuais!" Fernando mostrou o gráfico de tendência: melhoria não é linear. O efeito composto leva tempo. Ele também celebrou vitórias intermediárias: "Reduzimos MTTD de 4.2h para 1.5h — isso é enorme!" Pequenas vitórias mantêm o momentum.

### P: "Como evitar que a calibragem automática das rubrics crie viés?"

**R:** Três salvaguardas: (1) supervisão humana — o time sempre revisa e aprova as sugestões, (2) diversidade nas dimensões — a rubric cobre múltiplos aspectos para não otimizar cegamente uma métrica, (3) monitoramento de distribuição — se a rubric começar a rejeitar desproporcionalmente um segmento de clientes, um alerta é disparado.

### P: "O que fazer quando um componente removido se prova necessário depois?"

**R:** Reverter é trivial (git revert). O KODA nunca precisou reverter nenhuma remoção, mas o processo está documentado. Se um componente removido se provar necessário, a lição é: "O teste de 48h em staging não capturou o problema. Precisamos de testes melhores." Isso vira um learning card e melhora o processo de simplificação.

### P: "Melhoria contínua funciona se o time tem alta rotatividade?"

**R:** Funciona, mas requer onboarding estruturado. O KODA resolveu isso com: (1) learning cards — novos engenheiros leem os 20 learning cards mais recentes como parte do onboarding, (2) rituais fixos — daily/weekly/monthly que não dependem de pessoas específicas, (3) documentação viva — cada componente tem um README que explica por que existe e qual métrica impacta. A cultura sobrevive a pessoas.

### P: "Qual o papel do QA em um time de melhoria contínua?"

**R:** No KODA, QA evoluiu de "validador final" para "parceiro estratégico". Em vez de testar features no final do ciclo, QA: (1) ajuda a definir métricas de qualidade antes da implementação, (2) desenha os testes de regressão que a telemetria vai monitorar, (3) lidera as retrospectivas de feedback, (4) é o guardião dos thresholds das rubrics. QA não é mais gargalo — é acelerador.

### P: "Como medir o sucesso da cultura de melhoria contínua em si?"

**R:** O KODA definiu 4 "meta-métricas" para medir se a cultura está funcionando:
1. **Taxa de participação:** % do time que propôs pelo menos 1 melhoria no mês (target: > 80%)
2. **Tempo de ciclo de feedback:** tempo médio entre reportar um problema e fechá-lo (target: < 72h)
3. **Taxa de simplificação:** quantos componentes foram removidos no trimestre (target: > 10% de redução)
4. **Autonomia:** % de melhorias iniciadas sem envolvimento da liderança (target: > 60%)

Se essas 4 meta-métricas estão saudáveis, a cultura está funcionando — independentemente das métricas de feature.

---

## 🗺️ Roadmap Futuro: O Que Vem Depois dos 6 Meses

O programa KCI de 6 meses foi o começo, não o fim. O time KODA definiu um roadmap para os próximos 12 meses:

### Curto Prazo (Julho-Setembro 2026): Consolidação

```
OBJETIVOS:
━━━━━━━━━
• Todas as 12 features congeladas passam pelo framework KCI
  antes de serem implementadas
• Cobertura de testes de harness: 82% → 95%
• MTTD (debug): 30min → 15min
• Zero componentes sem dono documentado
• Learning cards: 30+ acumulados, usados em todo onboarding

META PRINCIPAL: "KCI deixa de ser um programa e vira o
                jeito padrão de trabalhar"
```

### Médio Prazo (Outubro-Dezembro 2026): Escala

```
OBJETIVOS:
━━━━━━━━━
• Framework KCI aplicado a TODAS as features do KODA (não só novas)
• Sistema de "auto-simplificação": detector automático de componentes
  ociosos ou redundantes
• Rubrics com calibragem 100% automática (supervisão humana apenas
  para exceções)
• Dashboard preditivo: "Se continuarmos nesta tendência, falsos
  positivos serão 2% em março de 2027"

META PRINCIPAL: "O KODA se auto-melhora sem intervenção humana
                na maioria dos casos"
```

### Longo Prazo (2027+): Autonomia

```
OBJETIVOS:
━━━━━━━━━
• KODA detecta e corrige próprios erros sem intervenção humana
• Sistema de "self-healing": quando uma métrica degrada, o KODA
  automaticamente testa hipóteses de correção em staging
• Harness auto-evolutivo: componentes são adicionados e removidos
  automaticamente baseado em eficácia medida
• Cultura de melhoria contínua exportada para outros times e produtos

META PRINCIPAL: "Melhoria contínua não é mais um processo —
                é uma propriedade emergente do sistema"
```

### Os Riscos do Futuro

Com todo progresso, o time identificou riscos que precisam ser monitorados:

```
RISCOS IDENTIFICADOS PARA O FUTURO DO KCI
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RISCO 1: "COMPLACÊNCIA PÓS-SUCESSO"
───────────────────────────────────
Sintoma: "Já chegamos em 95% de precisão, podemos relaxar"
Mitigação: Meta contínua de melhoria (target do trimestre seguinte)
           Cultura de "nunca está bom o suficiente"

RISCO 2: "OVER-ENGINEERING DA MELHORIA"
───────────────────────────────────────
Sintoma: Adicionar complexidade ao processo de melhoria contínua
         (mais métricas, mais rituais, mais dashboards)
Mitigação: Aplicar a Lei de Fernando ao próprio KCI:
           "Se eu remover esta métrica/ritual, algo piora?"

RISCO 3: "FERNANDO-DEPENDENCY"
──────────────────────────────
Sintoma: Melhoria contínua depende do Fernando para acontecer
Mitigação: Rotação de liderança dos rituais, documentação dos
           processos, onboarding que ensina "como melhoramos"

RISCO 4: "MÉTRICAS GAMING"
──────────────────────────
Sintoma: Time otimiza para as métricas, não para a qualidade real
         (ex: rejeitar recomendações demais para "melhorar" precisão)
Mitigação: Métricas pareadas (precisão + approval rate),
           revisão humana de outliers, auditoria trimestral

RISCO 5: "NOVO MODELO, NOVAS REGRAS"
────────────────────────────────────
Sintoma: Um novo modelo (ex: Claude 5) muda completamente o
         comportamento do KODA, invalidando rubrics e harness
Mitigação: Processo de "re-baseline" documentado para quando
           um novo modelo é introduzido
```

---

## 📚 Leituras Relacionadas

- `curriculum/04-nivel-4-koda-specific/05-harness-improvements.md` — Diagnóstico e propostas de melhoria do harness KODA
- `curriculum/04-nivel-4-koda-specific/04-evaluation-rubrics-koda.md` — Design e calibragem de rubrics para features KODA
- `curriculum/03-nivel-3-advanced-architecture/05-harness-evolution.md` — O padrão de Harness Evolution em detalhes (Nível 3)
- `curriculum/02-nivel-2-practical-patterns/04-trace-reading.md` — Como ler traces para diagnosticar problemas (Nível 2)
- `curriculum/02-nivel-2-practical-patterns/03-rubric-design.md` — Fundamentos de rubric design (Nível 2)
- `curriculum/04-nivel-4-koda-specific/case-studies/case-study-01.md` — Case Study 1: Same-Day Delivery (refatoração arquitetural)
- `curriculum/04-nivel-4-koda-specific/case-studies/case-study-02.md` — Case Study 2: KODA Scale-Up (de 100 para 10.000 conversas/dia)
- `docs/analysis/mhc-backend-koda-harness-diagnostic.md` — Diagnóstico técnico do harness KODA
- `docs/decisions/` — Todas as ADRs do KODA (incluindo as 5 deste case study)

---

## 🔗 Cross-Reference: Padrões do Programa Aplicados no KCI

Este case study aplica virtualmente todos os padrões do programa. Esta tabela mostra onde cada padrão aparece:

| Padrão | Nível | Onde no KCI | Impacto |
|--------|-------|-------------|---------|
| **Context Management** | N1 | Métricas de baseline, telemetria de contexto | Permitiu medir o que estava quebrado |
| **Token Budgeting** | N1 | Custo por conversa como métrica-chave | Reduziu custo de $0.47 para $0.21 (-55%) |
| **Basic Harness Patterns** | N1 | Fundação do harness simplificado | Estrutura mínima que funciona |
| **Generator/Evaluator** | N2 | Avaliador independente para recomendações | Eliminou sycophancy, precisão +20pp |
| **Sprint Contracts** | N2 | Contratos entre componentes do harness | Reduziu inconsistências entre módulos |
| **Rubric Design** | N2 | Rubrics adaptativas com calibragem automática | Rubrics sempre atualizadas com padrões reais |
| **Trace Reading** | N2 | Telemetria e audit trail JSONL | MTTD caiu de 4.2h para 30min (-86%) |
| **Multi-Agent Coordination** | N3 | Planner + locks para recursos compartilhados | Race conditions: de 5-8/dia para zero |
| **State Persistence** | N3 | SQLite como state store | Estado sobrevive a restarts |
| **File-Based Coordination** | N3 | Lock files com TTL para exclusão mútua | Coordenação sem dependências externas |
| **Harness Evolution** | N3 | Simplificação agressiva do harness | 8 componentes → 6, economia de $1.500/mês |
| **Evaluation Rubrics** | N2 | Sistema de feedback em 3 camadas | 847 problemas → 312 corrigidos em 2 meses |

### Por Que Tantos Padrões?

O KCI não é sobre um padrão específico — é sobre como **todos os padrões trabalham juntos** para criar um sistema que se auto-melhora. Cada padrão resolve uma dimensão diferente do problema:

```
DIMENSÕES DO PROBLEMA E PADRÕES CORRESPONDENTES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DIMENSÃO: VISIBILIDADE ("o que está acontecendo?")
  → Telemetria (N1) + Trace Reading (N2) + Métricas (N2)
  → Sem visibilidade, melhoria é impossível

DIMENSÃO: QUALIDADE ("está bom o suficiente?")
  → Generator/Evaluator (N2) + Rubric Design (N2) + Evaluation Rubrics (N2)
  → Sem qualidade, confiança é impossível

DIMENSÃO: COORDENAÇÃO ("como as partes trabalham juntas?")
  → Multi-Agent Coordination (N3) + File-Based Coordination (N3) + Sprint Contracts (N2)
  → Sem coordenação, escala é impossível

DIMENSÃO: RESILIÊNCIA ("o sistema sobrevive a falhas?")
  → State Persistence (N3) + Harness Evolution (N3) + Context Management (N1)
  → Sem resiliência, operação contínua é impossível

DIMENSÃO: EVOLUÇÃO ("o sistema melhora com o tempo?")
  → TODOS OS PADRÕES JUNTOS + Cultura de Melhoria Contínua
  → Sem evolução, relevância de longo prazo é impossível
```

---

## 📖 Glossário de Termos do KCI

| Termo | Definição |
|-------|-----------|
| **KCI** | KODA Continuous Improvement — programa de 6 meses de melhoria contínua |
| **Lei de Fernando** | "Se eu remover este componente, qual métrica piora?" — princípio de simplificação |
| **Learning Card** | Documento de 1 página que captura um aprendizado de incidente ou melhoria |
| **Frankenharness** | Apelido do harness de janeiro 2026 — componentes acumulados sem design coeso |
| **Métrica de Vaidade** | Métrica que parece boa mas não reflete qualidade real (ex: uptime, mensagens/dia) |
| **Feedback Órfão** | Feedback registrado sem dono, prazo ou plano de ação |
| **Rubric Adaptativa** | Rubric cujos pesos e thresholds se recalibram automaticamente baseado em dados |
| **MTTD** | Mean Time To Debug — tempo médio para diagnosticar a causa raiz de um incidente |
| **FCR** | First Contact Resolution — % de conversas resolvidas sem escalar para humano |
| **CSAT** | Customer Satisfaction — nota de satisfação do cliente pós-interação |
| **Approval Rate** | % de recomendações aprovadas pelo Evaluator (muito baixo = rubric muito rigorosa) |
| **Sycophancy** | Tendência de um LLM concordar consigo mesmo e aprovar o próprio trabalho |
| **Shadow Mode** | Rodar novo sistema em paralelo sem afetar usuários reais, apenas para comparação |
| **Canary Release** | Liberar mudança para % pequena do tráfego antes do rollout completo |

---

## 📊 Metadata

| Campo | Valor |
|-------|-------|
| **Arquivo** | case-study-03.md |
| **Nível** | 4 — KODA-Específico |
| **Tipo** | Case Study |
| **Tempo** | 120-150 minutos |
| **Status** | ✅ Completo |
| **Pré-requisitos** | Níveis 1, 2 e 3 completos + Módulos 01-05 do Nível 4 |
| **Feature KODA** | Melhoria Contínua (KCI Program) |
| **Padrões aplicados** | Generator/Evaluator, Sprint Contracts, Rubric Design, Trace Reading, Harness Evolution, State Persistence, Multi-Agent Coordination |
| **Período coberto** | Janeiro 2026 — Junho 2026 (6 meses) |
| **Data** | Maio 2026 |
| **Próximo** | Consulte o curriculum para novos módulos |

---

*Escrito com base na experiência real do time KODA implementando o programa KODA Continuous Improvement (KCI) ao longo de 6 meses.*
*Este case study é o documento de referência para qualquer iniciativa de melhoria contínua em sistemas de IA no KODA.*
