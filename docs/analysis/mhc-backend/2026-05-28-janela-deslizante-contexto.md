---
title: "Análise: Janela Deslizante + Resumo + Metadados no Contexto do Agente"
type: analysis
date: 2026-05-28
domain: mhc-backend
aliases: []
tags: [analise, mhc-backend, diagnostico, context-engineering, context-window]
last_updated: 2026-06-10
---

# Análise: Janela Deslizante + Resumo + Metadados no Contexto do Agente

**Data:** 2026-05-28
**Escopo:** Como o mhc-backend gerencia o contexto de conversa para os agentes LangGraph (Coach, Ecommerce/KODA, Voturuna)

---

## Objetivo

Avaliar a implementação atual de três mecanismos de compressão de contexto para LLMs:

1. **Janela deslizante** das últimas K mensagens (tipicamente 15-20)
2. **Resumo comprimido estruturado** do histórico antigo que saiu da janela
3. **Metadados críticos que nunca expiram** (decisões, compromissos, restrições)

---

## 1. Janela deslizante: últimas K mensagens

O sistema implementa truncagem simples ("pegar as últimas N"), sem sliding window com sumarização do que cai fora.

### Tamanhos de janela por contexto

| Contexto | Tamanho | Arquivo |
|---|---|---|
| Ecommerce (WhatsApp) | 60 mensagens | `src/agents/orchastrator/ConversationStateBuilder.ts:60` |
| Ecommerce (API) | 20 mensagens | `src/agents/orchastrator/ConversationStateBuilder.ts:59` |
| Coach | 5 mensagens | `src/services/coach/state-builder.ts:473` |
| Chat API (paginado) | 20 (default) | `src/controllers/ChatController.ts` |

### Fluxo de montagem (Ecommerce)

```
ConversationStateBuilder.buildState()
  │
  └─ getConversationHistory(userId, historyLimit, conversationId)
       │
       └─ ecommerceMessageService.getConversationHistory(userId, limit)
            │
            └─ prisma.message.findMany({ where: { userId }, take: limit })
                 │
                 └─ .reverse() para ordem cronológica
```

Depois, `OrchestratorAgent.buildHistoryMessages()` converte cada entrada em `HumanMessage` (com timestamp em metadados) ou `AIMessage` do LangChain e injeta no grafo como `state.messages`.

### Fluxo de montagem (Coach)

```
buildState(userId)
  │
  └─ prisma.message.findMany({ where: { userId }, take: 5 })
       │
       └─ state.context.conversation_history
```

**Observação:** O agente Coach monta o `conversation_history` no estado mas **não** o injeta no system prompt. O prompt do coach é composto apenas de: persona, regras globais, memórias, onboarding, daily summaries e providers.

### Problema identificado

Mensagens que caem fora da janela são **perdidas para sempre** do ponto de vista do agente. Não há sumarização incremental do que ficou para trás.

---

## 2. Resumo comprimido do histórico antigo

**Status: NÃO IMPLEMENTADO**

Não existe pipeline que gere um resumo do histórico quando mensagens saem da janela deslizante. O que existe são aproximações parciais que não substituem esse mecanismo:

### Aproximações existentes

| Mecanismo | Arquivo | O que faz |
|---|---|---|
| MemoryExtractionService | `src/services/memory/MemoryExtractionService.ts` | Extrai fatos atômicos das mensagens (alergias, metas, preferências) via `gpt-4.1-mini`. Captura entidades, não o fluxo narrativo da conversa. |
| ConversationContext.askedQuestions | `prisma/schema.prisma` (model `ConversationContext`) | Persiste flags de progresso do funil (ex: `delivery_flow_sent`, `athletic_profile_asked`). Funciona como mini-FSM. |
| PurchaseJourneyService | `src/services/ecommerce/PurchaseJourneyService.ts` | Agrupa e sumariza sessões de mensagens, mas é usado apenas para **analytics**, não para contexto do prompt do agente. |
| EcommerceMessageService.cleanupOldMessages | `src/services/ecommerce/EcommerceMessageService.ts:239` | Deleta mensagens antigas do banco (mantém 50). É limpeza de storage, não sumarização. |

### O que falta

Um pipeline que, quando uma conversa ultrapassa o limite da janela:

1. Detecta mensagens que saíram da janela
2. Passa essas mensagens por um LLM com prompt de sumarização estruturada
3. Armazena o resumo incremental como `ConversationMemory` (categoria `conversation_summary`) ou em campo dedicado no `ConversationContext`
4. Injeta o resumo no system prompt junto com as memórias semânticas

---

## 3. Metadados críticos que nunca expiram

**Status: IMPLEMENTADO** em duas camadas complementares.

### Camada A: Memória semântica (`ConversationMemory`)

```prisma
model ConversationMemory {
  id        String    @id
  userId    String
  category  String    // preferences | dietary | medical | goals | history | routine
  key       String    // ex: "lactose_intolerant"
  value     String    // ex: "intolerante à lactose"
  notes     String?
  expiresAt DateTime? // null = nunca expira
  isActive  Boolean   // soft-delete
  source    String    // "ai_tool" | "auto_extraction"
}
```

**Operações principais:**

| Operação | Arquivo:linha | Comportamento |
|---|---|---|
| `save()` | `MemoryService.ts:43` | Aceita `expires_in_days`; sem ele, `expiresAt = null` (nunca expira) |
| `recall()` | `MemoryService.ts:114` | Filtra `isActive: true` + não expiradas. Padrão: últimos 90 dias, take 50 |
| `formatForContext()` | `MemoryService.ts:201` | Agrupa por categoria, formata como `## MEMÓRIAS DO USUÁRIO:\n### CATEGORY:\n- [ID] key: value (N dias atrás)` |
| `forget()` | `MemoryService.ts:186` | Soft-delete: `isActive = false` |
| `deactivateContradictions()` | `MemoryService.ts:74` | Se usuário informa restrição, desativa automaticamente memórias de "sem restrições" |

**Extração automática:**

`MemoryExtractionService.extractAndSave()` roda em background após cada resposta do agente. Usa `gpt-4.1-mini` com prompt estruturado para extrair fatos das mensagens do usuário. Detecta duplicatas e contradições antes de salvar.

**Categorias de memória:**

| Categoria | Exemplos de chave | Exemplo de valor |
|---|---|---|
| `preferences` | `horario_treino`, `estilo_comunicacao` | "prefere treinar de manhã" |
| `dietary` | `lactose_intolerant`, `dieta_vegana` | "intolerante à lactose" |
| `medical` | `lesao_joelho`, `arritmia` | "lesão no joelho esquerdo - jan/2026" |
| `goals` | `prova_10km`, `meta_peso` | "prova de 10km em março/2026" |
| `history` | `suplemento_creatina`, `bicicleta` | "toma creatina diariamente" |
| `routine` | `dias_treino`, `horario_trabalho` | "treina seg-qua-sex" |

### Camada B: Contexto de conversa (`ConversationContext`)

```prisma
model ConversationContext {
  id               String    @id
  userId           String    @unique
  askedQuestions   Json      // ["delivery_flow_sent", "athletic_profile_asked", ...]
  status           String    // "active" | "paused"
  discoveryContext Json?     // dados extraídos durante onboarding
}
```

- **`askedQuestions`**: flags que marcam progresso em fluxos multi-etapa (ex: `SendDeliveryFlowTool` → `delivery_flow_sent`, `delivery_flow_completed`)
- **`discoveryContext`**: dados que o LLM extraiu durante o fluxo de discovery/onboarding
- **`status`**: controle de pausa/reativação da conversa

### Injeção no prompt do agente

Tanto o Coach quanto o Ecommerce injetam memórias no system prompt:

```
===== CONTEXTO DO USUÁRIO =====
(onboarding data formatado)
## MEMÓRIAS DO USUÁRIO:
### DIETARY:
- [abc123] lactose_intolerant: intolerante à lactose (7 dias atrás)
### GOALS:
- [def456] prova_10km: prova de 10km em março/2026 (30 dias atrás)
```

---

## Diagrama do fluxo completo

```
Mensagem WhatsApp
  │
  ▼
webhook-unified.ts
  │
  ├─ Debounce (MessageDebounceService)
  ├─ Anti-spam gate
  └─ AgentRouter / FastPathRouter
       │
       ▼
OrchestratorAgent.processMessage()
  │
  ├─ [1] ConversationStateBuilder.buildState()
  │     ├─ getUserInfo()                    → perfil do usuário
  │     ├─ getConversationHistory(60)        → últimas 60 mensagens (RAW)
  │     ├─ getConversationContext()          → askedQuestions, status
  │     ├─ getActiveCart()                   → carrinho atual
  │     ├─ memoryService.recall(days_ago=90) → memórias semânticas
  │     ├─ getOnboardingData()               → lifestyle, budget, health
  │     ├─ getRecentOrders()                 → últimos 5 pedidos
  │     ├─ getShownProducts()                → mapeamento ID→Nome
  │     ├─ getLastWeekDailySummaries()       → dados de saúde/wearables
  │     └─ getProvadersOn()                 → Strava/Oura/Garmin status
  │
  ├─ [2] buildHistoryMessages(state)
  │     └─ conversation_history → [HumanMessage|AIMessage] LangChain
  │
  ├─ [3] graph.invoke({ messages: [history + userMsg], agentState })
  │     │
  │     ├─ routerNode ──→ coachAgenteNode
  │     │                   ├─ SystemPrompt: persona + rules + memory
  │     │                   │   + onboarding + providers + daily summaries
  │     │                   └─ tools: memory, reminders, workouts, products
  │     │
  │     ├─ routerNode ──→ ecommerceAgenteNode
  │     │                   ├─ SystemPrompt: persona + rules + memory
  │     │                   │   + checkout context + shown products
  │     │                   └─ tools: search, cart, order, shipping, memory
  │     │
  │     └─ routerNode ──→ voturunaAgenteNode
  │
  └─ [4] memoryExtractionService.extractAndSave() [BACKGROUND]
        └─ Extrai fatos das mensagens do usuário → ConversationMemory
```

---

## Resumo dos gaps

| Componente | Status | Detalhe |
|---|---|---|
| Janela das últimas K mensagens | ✅ Implementado | 20 (API) / 60 (WhatsApp) / 5 (Coach). Truncagem simples, sem sliding window. |
| Resumo comprimido do histórico antigo | ❌ Ausente | Mensagens fora da janela são descartadas. Não há sumarização incremental. |
| Metadados que nunca expiram | ✅ Implementado | `ConversationMemory` (fatos semânticos) + `ConversationContext` (estado do funil). Com extração automática e regras de contradição. |

---

## Recomendação

Para implementar o resumo comprimido do histórico antigo:

1. **Detecção**: quando `getConversationHistory` retorna mais mensagens do que o limite da janela, as excedentes devem ser sumarizadas
2. **Sumarização**: LLM com prompt estruturado gerando resumo incremental (tópicos discutidos, decisões tomadas, produtos mencionados, objeções levantadas)
3. **Persistência**: armazenar como `ConversationMemory` com categoria `conversation_summary` e `expiresAt` compatível com a janela (ex: 7 dias)
4. **Injeção**: adicionar o resumo ao system prompt na seção de contexto do usuário, antes ou depois das memórias semânticas
5. **Atualização incremental**: a cada novo resumo, atualizar (não duplicar) o resumo existente via `updateMemory`
