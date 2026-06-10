---
title: "Diagnóstico: Arquitetura KODA no `mhc-backend` vs. Padrões de Harness"
type: analysis
date: 2026-05-26
domain: mhc-backend
aliases: ["diagnostico harness", "arquitetura KODA", "harness KODA", "mhc harness"]
tags: [analise, mhc-backend, diagnostico, harness]
relates-to: ["[[curriculum/01-nivel-1-fundamentals/03-basic-harness-patterns|Basic Harness Patterns]]", "[[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]", "[[docs/canonical/stable-harness-prompt|Stable Harness Prompt]]"]
last_updated: 2026-06-10
---

# Diagnóstico: Arquitetura KODA no `mhc-backend` vs. Padrões de Harness

**Data:** 2026-05-26
**Repositório analisado:** [`chatshop-io/mhc-backend`](https://github.com/chatshop-io/mhc-backend)
**Referência curricular:** [[curriculum/01-nivel-1-fundamentals/03-basic-harness-patterns|03-basic-harness-patterns.md]]
**Stack:** Express.js 4.18, TypeScript 5.3, Prisma 5.7 (PostgreSQL 16), LangGraph, LangChain + OpenAI (gpt-4o-mini), Pinecone, Redis 7, Trigger.dev 4.3

---

## Visão Geral

O `mhc-backend` é o backend de produção do ecossistema MHC — uma plataforma conversacional de saúde, performance e e-commerce via WhatsApp. O agente de e-commerce é chamado **KODA** no próprio código (referência explícita em `OrchestratorAgent.ts:234`: _"Aqui é o KODA agente da MHC"_). A arquitetura usa **LangGraph** (StateGraph) para orquestrar 3 agentes especializados (`coach`, `ecommerce`, `voturuna`), com PostgreSQL + Redis como infraestrutura de estado.

O sistema implementa **todos os 5 padrões de harness do Nível 1** do currículo, com níveis de sofisticação que alcançam Nível 2 (Generator/Evaluator implícito via multi-agent, classificador determinístico) e Nível 3 (pipeline de memória com LLM secundário, cache multi-camada, coordenação multi-agente).

### Diagrama de Arquitetura

```
WhatsApp (Meta API)
        │
        ▼
  webhook-unified.ts  (95KB — FSM state, debounce, agent routing)
        │
        ▼
  OrchestratorAgent.processMessage()
        │
        ├── ConversationStateBuilder.buildState()
        │     ├── Redis cache (profile: 3min TTL)
        │     ├── PostgreSQL: user, cart, history (60 msgs), orders, memories
        │     ├── Pinecone: product context
        │     └── CartService (in-memory + DB persistence)
        │
        ├── buildHistoryMessages() → LangChain messages
        │
        ▼
  LangGraph StateGraph
        │
        ├── routerNode (classifica intent → coach | ecommerce | voturuna)
        │
        ├── coachAgenteNode (13 tools: reminders, summaries, Strava/Oura)
        ├── ecommerceAgenteNode (KODA) (20 tools: search, cart, order)
        └── voturunaAgenteNode (day-use purchases)
        │
        ▼
  MemoryExtractionService (background: extract facts → PostgreSQL)
```

---

## Padrão 1: History Windowing

### O que o currículo prescreve

Janela deslizante de 15-20 mensagens + resumo comprimido do histórico antigo + metadados críticos que nunca expiram (decisões, preferências, alergias).

### Como o `mhc-backend` implementa

**Janela deslizante adaptativa** — `ConversationStateBuilder.getConversationHistory()`:

| Canal | Limite | Arquivo |
|-------|--------|---------|
| WhatsApp | 60 mensagens | `src/agents/orchastrator/ConversationStateBuilder.ts:60` |
| API (web) | 20 mensagens | `src/agents/orchastrator/ConversationStateBuilder.ts:60-61` |

O histórico é convertido em mensagens LangChain (`HumanMessage` / `AIMessage`) com um detalhe arquitetural relevante: **mensagens do usuário recebem timestamp** (`"conteúdo | dd/MM/yyyy HH:mm:ss"`) enquanto **mensagens do assistant não** — para evitar que o LLM aprenda o padrão e passe a ecoar timestamps nas respostas (`OrchestratorAgent.ts:428-432`).

**Metadados críticos que nunca expiram** — implementados em 4 camadas separadas:

1. **`onboardingData`**: lifestyle, budget, healthConditions, restrictions — carregados em query única que junta 4 tabelas relacionadas (`ConversationStateBuilder.ts:1052-1183`)
2. **`athleteProfile`**: goal, sport, level — persistido via `CartService` (Redis + DB)
3. **`memoriesContext`**: memórias semânticas extraídas pelo `MemoryExtractionService` com recall de 90 dias (`ConversationStateBuilder.ts:137-141`)
4. **`conversationContext`**: askedQuestions, status da conversa (navegando, checkout, etc.) — persistido na tabela `conversationContext` (`ConversationStateBuilder.ts:500-534`)

**Cache de perfil no Redis** — os dados estáticos (user, shipping, athlete, onboarding) são cacheados com TTL de 3 minutos; dados dinâmicos (cart, history, product context) são sempre frescos (`ConversationStateBuilder.ts:67-93`).

### Métricas e trade-offs

- O currículo alerta sobre "perder decisões anteriores ao descartar histórico". O sistema resolve mantendo metadados críticos em tabelas separadas enquanto o histórico bruto (`Message`) serve apenas como janela de contexto.
- O currículo alerta sobre "resumir com 1000 tokens". O sistema resolve com o `MemoryExtractionService` usando modelo menor (`gpt-4.1-mini`) para extrair apenas fatos concretos, não resumos genéricos.

---

## Padrão 2: Output Validation (Structured Generation)

### O que o currículo prescreve

Forçar JSON estruturado + validação de schema (Pydantic/JSON Schema) + validação de business constraints pós-parsing + confidence score.

### Como o `mhc-backend` implementa

**Ferramentas com schema Zod** — as 40+ ferramentas do agente são definidas como `DynamicStructuredTool` com schema Zod. Exemplos:

- `SearchProductsTool`: busca no Pinecone → array de produtos com `{id, name, price, score}`
- `CreateOrderTool`: cria pedido → `{orderId, status, totalAmount}`
- `AddToCartTool`: valida produto existe antes de adicionar
- `GetDailySummariesTool`: dados formatados de sono/recuperação

**Memory Service com detecção de contradições** — `MemoryService.deactivateContradictions()` (`src/services/memory/MemoryService.ts:74-109`): quando o agente salva uma restrição (ex: `lactose_intolerant`), o sistema automaticamente desativa memórias contraditórias (ex: `no_dietary_restrictions`). Isso implementa exatamente o GOTCHA que o currículo alerta: "recomendar produto com ingrediente que cliente é alérgico".

**Classificador determinístico** — `src/services/coach/classifier.ts`: o Coach usa um classificador baseado em regras (não-LLM) para decidir EMPURRAR | MANTER | REDUZIR baseado em métricas objetivas:

| Condição | Threshold | Classificação |
|----------|-----------|---------------|
| Sleep Score | ≤ 72 | REDUZIR |
| HRV delta 7d | ≤ -10% | REDUZIR |
| RHR delta 7d | ≥ +3 bpm | REDUZIR |
| Temp delta | ≥ 0.3°C | REDUZIR |
| Carga aguda/crônica | ≥ 1.5x | REDUZIR |
| Sleep Score | ≥ 80 **E** HRV ≥ -5% **E** RHR ≤ +1 **E** temp ≤ 0.1°C **E** carga ≤ 1.2x | EMPURRAR |
| Default | — | MANTER |

Isso é output validation **pré-LLM**: o modelo recebe a classificação pronta e apenas gera a mensagem apropriada.

**Validação de input** — middleware Joi (`src/middleware/validation.ts`) + Zod schemas (`src/schemas/`) + HMAC em webhooks de pagamento (`src/routes/webhook-payment.ts`) + idempotency check por WhatsApp message ID.

### Métricas e trade-offs

- "Confiar que o modelo vai fazer a coisa certa" → resolvido com classificador determinístico + detecção de contradições
- "Output validation sem business validation" → resolvido com `deactivateContradictions()` que valida restrições de negócio após salvar memória
- "Não deixar model corrigir a si mesmo" → parcialmente resolvido: o sistema não tem retry loop com feedback, mas o classificador determinístico elimina a necessidade de auto-correção para decisões de risco

---

## Padrão 3: State Persistence (Memory Between Turns)

### O que o currículo prescreve

Persistir preferências, decisões e compromissos em estrutura recuperável (arquivo ou banco).

### Como o `mhc-backend` implementa

Este é o padrão mais desenvolvido no sistema. O estado é distribuído em múltiplas tabelas PostgreSQL com cache Redis.

**Tabelas de estado persistente:**

| Tabela | Propósito | Atualização | Arquivo relevante |
|--------|-----------|-------------|-------------------|
| `conversationMemory` | Memórias semânticas (preferences, dietary, medical, goals, history, routine) | Background após cada turno | `src/services/memory/MemoryService.ts` |
| `conversationContext` | Estado da conversa (status, askedQuestions) | Síncrono durante o turno | `prisma/schema.prisma` |
| `EcommerceCart` | Carrinho ativo + Redis cache | Síncrono via CartService | `src/services/ecommerce/CartService.ts` |
| `Order` | Pedidos realizados com status e tracking | Síncrono via CreateOrderTool | `src/services/ecommerce/OrderService.ts` |
| `shippingAddress` | Endereço de entrega persistido | Via CartService | `ConversationStateBuilder.ts:704-718` |
| `athleteProfile` | Goal, sport, level | Via CartService | `ConversationStateBuilder.ts:912-943` |
| `onboardingData` | Lifestyle, budget, health, restrictions | Via WhatsApp Flow | `ConversationStateBuilder.ts:1052-1183` |

**Memory Extraction Pipeline** — `src/services/memory/MemoryExtractionService.ts`:

1. Após cada mensagem processada, um modelo `gpt-4.1-mini` (mais barato que o principal) extrai fatos em background
2. Extração usa prompt estruturado que força 6 categorias: `preferences`, `dietary`, `medical`, `goals`, `history`, `routine`
3. Output validado com Zod: `ExtractedMemorySchema`
4. Detecta duplicatas antes de salvar (compara `category + key + value`)
5. Execução não bloqueante: `.catch()` no `OrchestratorAgent.ts:107-111` garante que falha na extração não afeta a resposta

**Coach State Cache** — `src/services/coach/state-builder.ts:47-93`:

- Cache in-memory de 30 minutos para `CoachingState` (agrega dados de Strava, Oura, perfil)
- Chave do cache: `userId:date` no timezone `America/Sao_Paulo`
- Limpeza automática de entradas expiradas a cada 5 minutos

### Métricas e trade-offs

- "Persistir estado bruto sem estrutura" → resolvido com 6 categorias tipadas e schema Zod
- "Não gerenciar expiração de estado" → resolvido com `expiresAt` nativo no modelo + `cleanupExpired()` em cron job
- "Nunca auditar o que foi persistido" → parcialmente: memórias têm `createdAt`, `updatedAt`, `source: 'ai_tool'`, mas não há log completo de auditoria por decisão

### Comparação com níveis do currículo

O currículo de Nível 1 descreve um sistema simples de `conversation_state.json`. O `mhc-backend` implementa o equivalente ao **Nível 3** (state persistence avançada com pipeline temporal): múltiplas tabelas PostgreSQL, extração assíncrona via LLM secundário, cache em dois níveis (Redis + in-memory), e expiração automática de memórias.

---

## Padrão 4: Fallback & Retry

### O que o currículo prescreve

Retry com novo prompt → fallback para recomendação segura → escalação para humano.

### Como o `mhc-backend` implementa

**Matriz de fallbacks:**

| Mecanismo | Local | Comportamento |
|-----------|-------|---------------|
| Try/catch no OrchestratorAgent | `OrchestratorAgent.ts:151-163` | Fallback: mensagem genérica de erro ao usuário |
| Message Debounce | `MessageDebounceService.ts` | Agrupa mensagens em rajada, processa em batch |
| Message Processing Queue | `MessageProcessingQueue.ts` | Processamento sequencial por usuário (documentado race condition: `FIXME-RACE-CONDITIONS`) |
| Redis cache fallback | `ConversationStateBuilder.ts:90` | Se Redis falha, query direta ao PostgreSQL |
| Memory extraction fallback | `OrchestratorAgent.ts:107-111` | `.catch()` não bloqueante: resposta enviada mesmo se extração falhar |
| Conversation history fallback | `ConversationStateBuilder.ts:492-494` | Se query falhar: "agent will run without context" |
| Memory recall fallback | `MemoryService.ts:158` | Se recall falhar: "agent will run without memory context" |
| Cron lock fail-open | `cron-lock.ts` | Se lock não pode ser adquirido (timeout/Redis down), job executa mesmo assim |
| Payment webhook idempotency | `webhook-payment.ts` | Verifica `paymentIntentId` antes de processar |
| Stale cart detection | `OrderExpiryService.ts` | Alerta usuário sobre itens antigos no carrinho |

**Single-agent bypass** — `src/agents/agentsGraph.ts:41-48`: se apenas 1 agente está ativo, o nó `routerNode` (que custa ~800ms de LLM call) é pulado e a mensagem vai direto para o agente. Isso é um fallback de performance e custo.

**Batch processing** — `OrchestratorAgent.processMessageBatch()` (`OrchestratorAgent.ts:175-362`): quando o debounce agrupa múltiplas mensagens, cada uma vira uma `HumanMessage` separada no array de mensagens, preservando o contexto natural da conversa.

### Métricas e trade-offs

- O sistema prioriza **fail-open** (continuar operando mesmo com degradação) sobre **fail-closed** (recusar operação)
- O `MessageProcessingQueue` tem race condition documentada — risco conhecido
- Falta um mecanismo explícito de "retry com novo prompt" como o currículo sugere; o retry atual é apenas re-processamento na fila

---

## Padrão 5: Guardrails & Constraints

### O que o currículo prescreve

Constraints explícitos injetados no prompt antes da geração (budget máximo, produtos disponíveis, prazo de entrega).

### Como o `mhc-backend` implementa

**Constraints injetados no estado do agente (pré-geração):**

O `ConversationStateBuilder.buildState()` monta um `AgentState` completo que inclui:

- `onboardingData.restrictions[]` — restrições alimentares e médicas (`UserRestriction[]`)
- `onboardingData.healthConditions[]` — condições de saúde com severidade (`HealthCondition[]`)
- `onboardingData.budget` — orçamento por categoria: supplements, meals, physiotherapy, coach, total (`ExpenseBudget`)
- `athleteProfile` — goal, sport, level do atleta
- `lastWeekDailySummaries` — dados dos últimos 5 dias de sono/recuperação
- `conversationContext.status` — estado atual: navegando → adicionando_carrinho → checkout → pagamento → finalizado
- `memoriesContext` — memórias semânticas formatadas como contexto para o LLM

Todo esse contexto é injetado no nó do agente via `GraphState`, que o repassa ao prompt do LLM.

**Anti-spam gate** — `src/services/proactive/anti-spam.ts`:

| Regra | Valor |
|-------|-------|
| Máximo de mensagens por dia | 4 (`MAX_MESSAGES_PER_DAY`) |
| Máximo de mensagens por hora | 2 (`MAX_MESSAGES_PER_HOUR`) |
| Máximo do mesmo tipo por dia | 2 (`MAX_SAME_TYPE_PER_DAY`) |
| Intervalo mínimo entre mensagens | 300 segundos (`MIN_INTERVAL_SECONDS`) |

**Cron locks** — `src/services/proactive/cron-lock.ts`: jobs agendados usam `acquireCronLock` para evitar execução concorrente. Fail-open: se Redis está down, job executa mesmo assim.

**Rate limiting** — middleware por endpoint e por usuário.

**Zod validation** — todo input externo é validado com Zod schemas antes de chegar ao agente.

**Product recommendation filter** — `src/services/ecommerce/ProductRecommendationFilter.ts`: remove produtos com preço zero, filtra fora de catálogo.

**Domain-specific validators** — `src/utils/restrictionValidators.ts`: validadores específicos de domínio para restrições do usuário.

### Métricas e trade-offs

- Constraints são injetados como **estado**, não como texto no prompt — o agente recebe objetos estruturados e decide como usar
- O anti-spam é a única barreira entre mensagens proativas e o usuário — se falhar, o usuário recebe spam
- O sistema tem 4 métodos deprecated no `anti-spam.ts` ainda não removidos (documentado no `AGENTS.md:163`)

---

## O Que o `mhc-backend` Faz Além dos 5 Padrões

### 1. Multi-Agent Routing com LangGraph

Em vez de um agente monolítico, o sistema usa 3 agentes especializados orquestrados por um nó `routerNode` que classifica a intent do usuário:

| Agente | Propósito | Tools | Status |
|--------|-----------|-------|--------|
| `coach` | Coaching de saúde e performance | 13 ferramentas | Parcialmente ativo |
| `ecommerce` (KODA) | Vendas de suplementos | 20 ferramentas | **Ativo (default)** |
| `voturuna` | Day-use purchases | Scaffolding | Incompleto |

Controle via variáveis de ambiente: `ENABLED_AGENTS=coach,ecommerce` ou `USE_ALL_AGENTS=true`. Single-agent mode pula o router economizando ~800ms.

### 2. Pipeline de Memória com LLM Secundário

O `MemoryExtractionService` usa `gpt-4.1-mini` (modelo menor/mais barato que o principal `gpt-4o-mini`) em background para extrair fatos e salvá-los na tabela `conversationMemory` com:

- Detecção automática de contradições (`deactivateContradictions`)
- Deduplicação por `category + key + value`
- Categorização em 6 tipos
- Expiração configurável por memória

### 3. Classificador Determinístico (Coach)

O `classifier.ts` implementa regras determinísticas baseadas em métricas objetivas de wearables para classificar o dia do atleta. Isso é um guardrail **pré-LLM**: o modelo não decide se o atleta deve treinar forte ou descansar — ele recebe a classificação pronta e apenas gera a mensagem apropriada.

### 4. Proactive Trigger System

O sistema detecta eventos e dispara mensagens proativas:

- `wake_detected` — bom dia com dados de sono
- `sleep_data_ready` — quando Oura/Garmin entregam dados
- `strava_activity_uploaded` — pós-treino
- `morning_no_show` — follow-up se usuário não respondeu
- `weekly_review` — resumo semanal
- `evening_summary` — resumo do dia

Todos passam obrigatoriamente pelo anti-spam gate antes do envio.

### 5. Cache Multi-Nível

| Camada | Tecnologia | TTL | Dados |
|--------|-----------|-----|-------|
| Redis | `redisClient` | 3 minutos | Perfil estático (user, shipping, athlete, onboarding) |
| In-memory | `Map<string, CacheEntry>` | 30 minutos | Coaching state (Strava + Oura + perfil agregado) |
| CartService | Memória + DB | Persistente | Carrinho, lastViewedProduct, shownProducts |

---

## Resumo Comparativo

| Padrão | Currículo Nível 1 | `mhc-backend` | Nível equivalente |
|--------|-------------------|---------------|-------------------|
| **History Windowing** | Janela 15-20 msgs + resumo simples | Janela adaptativa (20-60 msgs) + 4 camadas de metadados em tabelas separadas + Redis cache | Nível 2 |
| **Output Validation** | JSON Schema + business constraints manuais | Zod `DynamicStructuredTool` + MemoryService com detecção de contradições + classificador determinístico + Joi middleware | Nível 2-3 |
| **State Persistence** | Arquivo JSON simples | PostgreSQL multi-tabela + Redis cache + extração assíncrona via LLM secundário + expiração automática + in-memory cache | Nível 3 |
| **Fallback & Retry** | Retry + fallback seguro | 10 mecanismos de fallback em cascata (Redis→DB, memory→skip, history→skip) + fail-open + debounce/batch | Nível 2 |
| **Guardrails** | Constraints textuais no prompt | Estado completo do usuário injetado como objetos + anti-spam (4/dia, 2/hora) + cron locks + Zod validation + filtro de produtos | Nível 2 |

---

## Lacunas Identificadas

1. **Sem retry loop com feedback** — o currículo sugere "retry com novo prompt mais específico"; o sistema atual apenas re-processa na fila sem modificar o prompt
2. **MessageProcessingQueue com race condition** — documentado como `FIXME-RACE-CONDITIONS` no código fonte
3. **Coach e Voturuna parcialmente ativos** — o scaffolding multi-agente existe, mas a produção é majoritariamente single-agent (ecommerce)
4. **43 `console.log` calls** — documentado no `AGENTS.md:164`, deveriam usar o logger Winston
5. **4 métodos deprecated no anti-spam** — `AGENTS.md:163`, risco de comportamento inesperado
6. **Sem log de auditoria por decisão** — memórias têm timestamp e source, mas não há rastreabilidade completa de "quem decidiu o quê e por quê"
7. **Hardcoded JWT_SECRET fallback** — `AGENTS.md:161`, viola regra de segurança do próprio projeto

---

## Arquivos-Chave Referenciados

| Arquivo | Propósito |
|---------|-----------|
| `src/agents/agentsGraph.ts` | LangGraph multi-agent wiring e env-based agent activation |
| `src/agents/orchastrator/OrchestratorAgent.ts` | Orquestração principal, build de estado, graph invoke, memory extraction |
| `src/agents/orchastrator/ConversationStateBuilder.ts` | History windowing, cache, contexto de carrinho/perfil/pedidos, memory pull |
| `src/services/memory/MemoryService.ts` | CRUD de memórias com detecção de contradições e expiração |
| `src/services/memory/MemoryExtractionService.ts` | Pipeline de extração de memórias via gpt-4.1-mini em background |
| `src/services/coach/classifier.ts` | Classificador determinístico EMPURRAR/MANTER/REDUZIR |
| `src/services/coach/state-builder.ts` | Cache in-memory de 30min para coaching state |
| `src/services/proactive/triggers.ts` | Detecção de eventos para mensagens proativas |
| `src/services/proactive/anti-spam.ts` | Gate de frequência de envio (4/dia, 2/hora) |
| `src/services/proactive/cron-lock.ts` | Locks distribuídos para jobs agendados |
| `src/routes/webhook-unified.ts` | Entry point WhatsApp (95KB) com FSM, debounce, routing |
| `src/routes/webhook-payment.ts` | HMAC validation, idempotency, order updates |
| `src/services/queue/MessageDebounceService.ts` | Agrupamento de mensagens em rajada |
| `src/services/queue/MessageProcessingQueue.ts` | Fila de processamento sequencial por usuário |
| `prisma/schema.prisma` | 50+ modelos incluindo ConversationMemory, ConversationContext, EcommerceCart, Order |
