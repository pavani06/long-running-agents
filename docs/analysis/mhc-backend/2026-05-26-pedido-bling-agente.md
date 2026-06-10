---
title: "Diagnóstico: Pedido Pago Não Encontrado no Bling e Agente Não Notificado"
type: analysis
date: 2026-05-26
domain: mhc-backend
aliases: ["falha webhook", "notificacao Bling", "pedido pago ERP", "Bling KODA"]
tags: [analise, mhc-backend, diagnostico, bling, pedido, erro]
relates-to: ["[[docs/canonical/error-context-hygiene|Error Context Hygiene]]", "[[docs/canonical/serializable-pause-resume-state|Serializable Pause/Resume State]]"]
last_updated: 2026-06-10
---

# Diagnóstico: Pedido Pago Não Encontrado no Bling e Agente Não Notificado

**Data:** 26 Maio 2026
**Contexto:** KODA / MHC Backend (chatshop-io/mhc-backend)
**Base teórica:** Currículo Long-Running Agents (Níveis 2, 3, 4)

---

## 1. Problema Reportado

Três sintomas ocorreram simultaneamente:

1. **"não achou o pedido no Bling"** — o pedido não foi encontrado no ERP
2. **"agent aparentemente não recebeu o pedido"** — o agente KODA não foi notificado
3. **"pagamento foi feito"** — o dinheiro saiu, o gateway confirmou

---

## 2. Diagnóstico: Causa Raiz

Após análise completa do código do `mhc-backend` e cruzamento com os padrões do currículo, a causa converge para **falha na fronteira de evento externo → sistema interno**.

### O fluxo esperado (o que deveria acontecer)

```
Cliente paga no checkout NuvemShop
  → NuvemShop dispara webhook POST /api/payment-webhook
    → webhook-payment.ts valida assinatura, processa pagamento
      → Order.paymentStatus = 'paid'
      → Envia WhatsApp de confirmação
        → Agente só descobre quando cliente pergunta (pull)
```

### O que quebrou (hipóteses por probabilidade)

| # | Hipótese | Probabilidade | Evidência no código |
|---|----------|:---:|---|
| **H1** | Webhook NuvemShop → MHC não chegou ou foi perdido | **Alta** | `webhook-payment.ts` não tem retry. Se o handler falha ou a rede falha, o evento se perde para sempre |
| **H2** | Webhook chegou mas o `order_id` não bateu com registro local | **Média** | Race condition: webhook chega antes do `ECommerceClient.createOrder()` retornar, `order` é `null`, retorna 200 com "order not found" e NÃO agenda retry |
| **H3** | NuvemShop criou pedido mas a sync com Bling falhou internamente | **Média** | O MHC depende da NuvemShop para sincronizar com Bling. Se essa sync falha no lado da NuvemShop, o MHC nunca sabe |
| **H4** | Agente não foi notificado (comportamento esperado, não bug) | **Alta** | O agente ecommerce só consulta status via `GetLastOrderStatusTool` quando o cliente pergunta. O webhook NÃO notifica o agente — é uma lacuna de design, não um bug |
| **H5** | `PaymentWebhookEvent` ficou preso em `PROCESSING` | **Baixa** | Se o processamento crasha após criar o evento mas antes de marcar `PROCESSED`, não há timeout/stale detection para limpar |

### A fronteira frágil

A transição `Payment Event → payment_approved` é o único ponto do fluxo que depende de um evento que o MHC **não gera** — ele apenas reage. O currículo Nível 3 (`02-state-persistence.md`) alerta: _"a fronteira entre sistema externo e interno exige polling de fallback, porque eventos podem ser perdidos"_ .

---

## 3. Arquitetura Atual do MHC Backend

### Visão Macro

```
┌──────────────────────────────────────────────────────────────────────┐
│                         ENTRYPOINTS                                  │
│                                                                     │
│  Meta WhatsApp    Admin Dashboard    Webhooks Externos               │
│  POST /webhook    POST /admin/*      payment-webhook, Strava, etc.   │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────────┐
│                    EXPRESS ROUTES + MIDDLEWARE                       │
│  /webhook-unified  /chat  /ecommerce  /auth  /admin/*  /dayuse      │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────────┐
│                MessageProcessingQueue (Map em memória)               │
│             Garante 1 msg/userId por vez (previne race)             │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────────┐
│              AGENT ORCHESTRATION (LangGraph StateGraph)              │
│                                                                     │
│  RouterNode ──▶ Coach Agent    (wearables, treinos, saúde)          │
│             ├─▶ Ecommerce Agent (18 tools: busca, carrinho, pedido)  │
│             └─▶ Voturuna Agent  (day use)                           │
│                                                                     │
│  ConversationStateBuilder: monta estado (cart, user, shipping,      │
│                             memories, history) a cada mensagem       │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────────┐
│                          CLIENTS                                     │
│                                                                     │
│  ECommerceClient ──▶ NuvemShop/Commerce (produtos, pedidos, frete)  │
│  ExternalPaymentClient ──▶ Gateway pagamento (link de checkout)     │
│  WhatsAppService ──▶ Meta Cloud API (mensagens, templates, CTA)    │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────────┐
│                        DATA LAYER                                    │
│                                                                     │
│  PostgreSQL (Prisma): User, Order, PaymentWebhookEvent,             │
│    EcommerceCart, CartItem, EcommerceMessage, DayUsePurchase,       │
│    Conversation, Message, ConversationMemory, ProviderConnection,   │
│    RawProviderData, DailySummary, SubscriptionPayment, etc.         │
│                                                                     │
│  Redis: Cache, rate limiting, checkout session, cron locks          │
│  Pinecone: Vector DB para busca semântica de produtos               │
└─────────────────────────────────────────────────────────────────────┘
```

### Fluxo de Compra (Caminho do Pedido)

```
1. Cliente WhatsApp → Webhook Meta → MessageProcessingQueue
2. ConversationStateBuilder monta estado
3. RouterNode classifica → "ecommerce"
4. EcommerceAgent processa: SearchProducts → AddToCart → CalculateShipping → CreateOrder
5. CreateOrderTool:
   ├─ Valida carrinho, endereço, CPF, email, nome, estoque
   ├─ ECommerceClient.createOrder(payload) → NuvemShop
   ├─ NuvemShop cria pedido, gera externalOrderId + checkoutUrl
   ├─ Envia CTA URL (WhatsApp) com link de pagamento
   └─ postOrderCleanup: limpa carrinho em memória, fecha conversa
6. Cliente paga (fora do WhatsApp)
7. NuvemShop dispara webhook → webhook-payment.ts
8. processPaymentNotification():
   ├─ Valida HMAC, verifica idempotência (PaymentWebhookEvent)
   ├─ Busca Order por externalOrderId
   ├─ Atualiza paymentStatus → 'paid'
   ├─ Limpa carrinho DB + endereço
   ├─ Envia WhatsApp confirmação
   ├─ Envia email confirmação
   └─ Se DayUse: ativa
9. Agente NÃO é notificado — só descobre quando cliente pergunta
```

---

## 4. Diagrama de Estados Atual do Pedido

```
                    ┌──────────────────────────┐
                    │     PENDING               │
                    │  status: 'pending'        │
                    │  paymentStatus: 'pending' │
                    │  Carrinho DB: INTACTO     │
                    │  Carrinho memória: VAZIO  │
                    │  Conversa: CLOSED         │
                    └──────┬───────┬───────────┘
                           │       │
              ═════════════╪═══════╪═══════════════
              ║ WEBHOOK   ║       ║  CRON (24h / 12h inativo)
              ║           ║       ║
              ▼           ║       ▼
      ┌──────────┐        ║  ┌───────────┐
      │   PAID   │        ║  │  EXPIRED  │
      │ (webhook │        ║  │ payment   │
      │ payment. │        ║  │ Status=   │
      │ success) │        ║  │ 'expired' │
      └────┬─────┘        ║  └───────────┘
           │              ║
           │              ║  ═══ WEBHOOK FAILED ═══
           │              ║       ▼
           │              ║  ┌──────────┐
           │              ║  │  FAILED  │
           │              ║  │ payment  │
           │              ║  │ Status=  │
           │              ║  │'failed'  │
           │              ║  └──────────┘
           │              ║
           ▼              ║
    ┌──────────────────────╜──────────────────────┐
    │         APÓS PAID: FORA DO CONTROLE MHC      │
    │                                              │
    │  NuvemShop/Bling (externo):                  │
    │  processing → invoiced → shipped → delivered │
    │                                              │
    │  Agente: SÓ CONSULTA SOB DEMANDA (pull)      │
    │  Sem push notification                       │
    │  Sem verificação de consistência             │
    │  Sem retry para falhas de webhook            │
    └──────────────────────────────────────────────┘

ESTADOS TOTAIS: 4 (pending, paid, failed, expired)
```

**Gaps identificados:**
- ❌ Sem estado "processing" / "syncing" / "evaluated"
- ❌ Sem retry automático para webhook
- ❌ Sem polling de fallback se webhook não chega
- ❌ Sem push notification ao agente
- ❌ Sem verificação de consistência pós-pagamento (amount, itens)
- ❌ Sem visibilidade da sync com Bling
- ❌ Sem alerta para pedido pago não encontrado
- ❌ Sem audit trail unificado

---

## 5. Arquitetura Proposta: Payment-to-Order Bridge com Supervisor

Baseada nos padrões do currículo (Generator/Evaluator, Sprint Contracts, State Persistence, Multi-Agent, Event-Driven), a solução introduz 4 novos componentes:

```
                    ┌─────────────────────────────────────────┐
                    │         GATEWAY DE PAGAMENTO              │
                    │         (NuvemShop)                       │
                    └────────────────┬────────────────────────┘
                                     │
                          ┌──────────▼──────────┐
                          │  WEBHOOK HANDLER     │  ← idempotente,
                          │  (Ingestion Agent)   │     retry-safe
                          │                      │
                          │  SÓ persiste evento  │
                          │  Responde 200        │
                          │                      │
                          │  Cria:               │
                          │  PaymentEvent        │
                          └──────────┬──────────┘
                                     │
                    ┌────────────────▼────────────────────┐
                    │        SUPERVISOR AGENT              │  ← Planner + Evaluator
                    │                                      │
                    │  Polling a cada 60s OU               │
                    │  reage a PaymentEvent                │
                    │                                      │
                    │  ┌─────────────────────────────┐    │
                    │  │  1. Valida contrato         │    │
                    │  │  2. Orquestra BlingSync     │    │
                    │  │  3. Avalia com rubrica      │    │
                    │  │  4. Decide: retry/alert/    │    │
                    │  │     push                    │    │
                    │  └─────────────────────────────┘    │
                    └──────┬──────────────┬────────────────┘
                           │              │
              ┌────────────▼──┐   ┌───────▼──────────────┐
              │ BLING SYNC    │   │  EVALUATOR + RUBRICA │
              │ AGENT         │   │                      │
              │               │   │  4 dimensões:        │
              │ Tenta sync    │   │  • Completude (30%)  │
              │ com Bling     │   │  • Bling sync (40%)  │
              │ via NuvemShop │   │  • Consistência (20%)│
              │               │   │  • Idempotência (10%)│
              │ Retry 5x      │   │                      │
              │ Backoff exp.  │   │  Gate: score ≥ 14/20 │
              └───────────────┘   └───────┬──────────────┘
                                          │
                              ┌───────────▼───────────┐
                              │  AGENT NOTIFIER       │
                              │                       │
                              │  Push notification    │
                              │  ao agente:           │
                              │  "pedido pago e       │
                              │   sincronizado"       │
                              │                       │
                              │  Reabre conversa      │
                              │  se necessário        │
                              └───────────────────────┘
```

---

## 6. Diagrama de Estados Após Mudanças

```
                    ┌──────────────────────────────────────────────────────┐
                    │                   PENDING (mantido)                   │
                    │  status: 'pending'  │  paymentStatus: 'pending'       │
                    │  PaymentEvent: NÃO EXISTE                             │
                    └──────────────────────┬───────────────────────────────┘
                                           │
                                      ═════╪═════ Webhook NuvemShop
                                           │
                                           ▼
                    ┌──────────────────────────────────────────────────────┐
                    │             payment_received ◀── NOVO                │
                    │  PaymentEvent criado: { status: "pending" }          │
                    │  Ação: só persistir + responder 200                  │
                    └──────────────────────┬───────────────────────────────┘
                                           │
                              ─────────────┼───────────── PaymentProcessorService
                                           │
                                           ▼
                    ┌──────────────────────────────────────────────────────┐
                    │            payment_validated ◀── NOVO                │
                    │  PaymentEvent.status = "processing"                  │
                    │  Verifica: idempotência, user existe, order existe   │
                    └──────────────────────┬───────────────────────────────┘
                                           │
                              ┌────────────┴────────────┐
                              │                         │
                     Order ENCONTRADA            Order NÃO ENCONTRADA
                              │                         │
                              ▼                         ▼
                    ┌──────────────────┐    ┌──────────────────────────────┐
                    │   order_found    │    │    order_not_found ◀── NOVO  │
                    │   ◀── NOVO       │    │                              │
                    └────────┬─────────┘    │ Retry 5x (30s→1m→2m→5m→10m) │
                             │              │ Se esgotado: AlertEvent      │
                             │              │ (critical) + interv. manual  │
                             │              └──────────────────────────────┘
                             ▼
                    ┌──────────────────────────────────────────────────────┐
                    │            payment_matched ◀── NOVO                  │
                    │  Verifica: order.totalAmount === paymentEvent.amount │
                    │  Se OK: Order.paymentStatus = 'paid', paidAt = now() │
                    │  Se divergência: AlertEvent (critical) + bloqueia    │
                    └──────────────────────┬───────────────────────────────┘
                                           │
                              ─────────────┼───────────── Supervisor → BlingSyncAgent
                                           │
                                           ▼
                    ┌──────────────────────────────────────────────────────┐
                    │             bling_syncing ◀── NOVO                   │
                    │  BlingSyncLog: { status: "syncing", attempts: 1 }    │
                    │  Chama NuvemShop para verificar sync com Bling       │
                    └──────────────────────┬───────────────────────────────┘
                                           │
                              ┌────────────┴────────────┐
                              │                         │
                        Sync OK                   Sync FALHA
                              │                         │
                              ▼                         ▼
                    ┌──────────────────┐    ┌──────────────────────────────┐
                    │  bling_synced    │    │    bling_failed ◀── NOVO     │
                    │  ◀── NOVO        │    │                              │
                    └────────┬─────────┘    │ Retry 5x (10s→30s→1m→5m→10m)│
                             │              │ Se esgotado: AlertEvent      │
                             │              │ (critical) + interv. manual  │
                             │              └──────────────────────────────┘
                             ▼
                    ┌──────────────────────────────────────────────────────┐
                    │             evaluation ◀── NOVO                      │
                    │  OrderEvaluator aplica rubrica 4 dimensões:          │
                    │  D1: Completude (30%)    D3: Consistência (20%)      │
                    │  D2: Bling sync (40%)    D4: Idempotência (10%)      │
                    │  SCORE: N/20                                          │
                    └──────────────────────┬───────────────────────────────┘
                                           │
                              ┌────────────┴────────────┐
                              │                         │
                        score ≥ 14                  score < 14
                        (aprovado)                  (reprovado)
                              │                         │
                              ▼                         ▼
                    ┌──────────────────┐    ┌──────────────────────────────┐
                    │fulfillment_ready │    │  REPROVADO                   │
                    │◀── NOVO          │    │  AlertEvent + retry ou       │
                    │                  │    │  compensação                 │
                    │ AgentNotifier    │    └──────────────────────────────┘
                    │ PUSH ao agente   │
                    │ "pedido pago e   │
                    │  sincronizado"   │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────────────────────────────────────────┐
                    │              fulfillment (mantido, externo)           │
                    │  NuvemShop/Bling: processing → invoiced → shipped    │
                    │  Agente AGORA tem contexto de pagamento confirmado   │
                    └──────────────────────────────────────────────────────┘


ESTADOS TOTAIS: 10 (pending, payment_received, payment_validated,
order_found, order_not_found, payment_matched, bling_syncing,
bling_synced, bling_failed, evaluation, fulfillment_ready, fulfillment)

NOVOS MECANISMOS:
✅ Retry com exponential backoff (max 5 tentativas)
✅ Polling de fallback no gateway (cron every 60s)
✅ Rubrica de 4 dimensões com score gate (14/20)
✅ AlertEvent com severidade (critical/high/medium/low)
✅ Push notification ao agente (AgentNotifier)
✅ OrderAuditLog em TODA transição de estado
✅ BlingSyncLog com rastreamento de tentativas
✅ PaymentEvent como fonte de verdade (separado da Order)
```

---

## 7. Plano de Implementação

### 7.1 Novos Arquivos

| Arquivo | Responsabilidade |
|---------|-----------------|
| `src/services/payment/PaymentEventService.ts` | Persistência de eventos de pagamento (`PaymentEvent`) |
| `src/services/payment/PaymentProcessorService.ts` | Processamento isolado com retry |
| `src/agents/graph/nodes/supervisorNode.ts` | Nó LangGraph: orquestrador pós-pagamento |
| `src/agents/graph/nodes/blingSyncAgentNode.ts` | Nó LangGraph: sincronia com Bling via NuvemShop |
| `src/services/evaluation/OrderEvaluator.ts` | Rubrica de 4 dimensões |
| `src/services/evaluation/AlertService.ts` | Criação e gerenciamento de alertas |
| `src/services/audit/OrderAuditService.ts` | Audit trail append-only |
| `src/jobs/payment-reconciliation-job.ts` | Cron job: polling de fallback (60s) + retry de eventos |
| `src/services/proactive/AgentNotifier.ts` | Push notification ao agente pós-pagamento |
| `src/services/queue/PaymentQueueService.ts` | Fila dedicada para eventos de pagamento (desacopla do chat) |

### 7.2 Arquivos a Modificar

| Arquivo | Mudança |
|---------|---------|
| `src/routes/webhook-payment.ts` | **Refatorar:** extrair lógica de processamento. Handler só valida + persiste + responde 200 |
| `src/agents/graph/state.ts` | **Expandir:** adicionar `paymentEvent`, `blingSyncStatus`, `supervisorVerdict` ao `GraphState` |
| `src/agents/graph/agentsGraph.ts` | **Expandir:** adicionar `supervisorNode` e `blingSyncAgentNode` ao `StateGraph` |
| `src/services/queue/MessageProcessingQueue.ts` | **Substituir:** Map em memória → Redis/BullMQ para durabilidade |
| `src/agents/orchastrator/ConversationStateBuilder.ts` | **Expandir:** carregar `PaymentEvent` e `BlingSyncLog` no estado da conversa |
| `prisma/schema.prisma` | **Expandir:** adicionar `PaymentEvent`, `AlertEvent`, `BlingSyncLog`, `OrderAuditLog` |

### 7.3 Novos Modelos Prisma

```prisma
model PaymentEvent {
  id              String    @id @default(cuid())
  externalId      String    @unique
  provider        String
  eventType       String
  payload         Json
  status          String    @default("pending")  // pending | processing | processed | failed
  retryCount      Int       @default(0)
  maxRetries      Int       @default(5)
  lastError       String?
  nextRetryAt     DateTime?
  orderId         String?
  createdAt       DateTime  @default(now())
  processedAt     DateTime?

  @@index([status, nextRetryAt])
}

model AlertEvent {
  id          String    @id @default(cuid())
  orderId     String?
  userId      String?
  type        String    // payment_mismatch | bling_sync_failed | order_not_found | evaluation_failed
  severity    String    // critical | high | medium | low
  message     String
  resolved    Boolean   @default(false)
  resolvedAt  DateTime?
  createdAt   DateTime  @default(now())

  @@index([resolved, severity])
}

model BlingSyncLog {
  id            String    @id @default(cuid())
  orderId       String
  blingOrderId  String?
  status        String    // syncing | success | failed
  attempts      Int       @default(1)
  lastError     String?
  createdAt     DateTime  @default(now())

  @@index([orderId])
}

model OrderAuditLog {
  id         String    @id @default(cuid())
  orderId    String
  fromState  String
  toState    String
  agent      String    // webhook | supervisor | bling_sync | evaluator | cron
  metadata   Json?
  createdAt  DateTime  @default(now())

  @@index([orderId, createdAt])
}
```

### 7.4 Sequência de Implementação

A ordem respeita dependências entre componentes:

```
Fase 1 — Schema (1-2 dias)
  ├── 1.1 Criar migration com novos modelos Prisma
  └── 1.2 Rodar prisma generate + prisma migrate

Fase 2 — Services base (2-3 dias)
  ├── 2.1 PaymentEventService
  ├── 2.2 OrderAuditService
  └── 2.3 AlertService

Fase 3 — Lógica de negócio (3-4 dias)
  ├── 3.1 PaymentProcessorService
  ├── 3.2 OrderEvaluator (rubrica)
  └── 3.3 AgentNotifier

Fase 4 — Agent nodes LangGraph (2-3 dias)
  ├── 4.1 BlingSyncAgentNode
  ├── 4.2 SupervisorNode
  └── 4.3 Integrar no agentsGraph.ts + state.ts

Fase 5 — Jobs + Refactor (2-3 dias)
  ├── 5.1 PaymentReconciliationJob (cron every 60s)
  ├── 5.2 Refatorar webhook-payment.ts
  └── 5.3 Substituir MessageProcessingQueue por Redis/BullMQ

Fase 6 — Testes e integração (2-3 dias)
  ├── 6.1 Testes unitários dos novos services
  ├── 6.2 Testes de integração do pipeline completo
  ├── 6.3 Smoke test com pedido real em staging
  └── 6.4 Monitoramento: dashboards para AlertEvent + BlingSyncLog

Tempo total estimado: 12-18 dias (1 dev dedicado)
```

---

## 8. Padrões do Currículo Aplicados

| Padrão | Nível | Onde se aplica |
|--------|:-----:|----------------|
| **Generator/Evaluator** | 2 | Supervisor (planner) → BlingSync (generator) → Evaluator (verificador) |
| **Sprint Contracts** | 2 | Cada agente tem input/output explícito; Supervisor tem contrato documentado |
| **Rubric Design** | 2 | OrderEvaluator usa 4 dimensões com gates de segurança |
| **Trace Reading** | 2 | `OrderAuditLog` append-only permite reconstruir qualquer falha |
| **Multi-Agent (Planner/Generator/Evaluator)** | 3 | SupervisorNode → BlingSyncAgentNode → OrderEvaluator |
| **State Persistence** | 3 | JSON/DB como fonte de verdade; estados imutáveis; replay possível |
| **File-Based Coordination** | 3 | Evoluído para DB-based: `PaymentEvent`, `BlingSyncLog`, `OrderAuditLog` |
| **Event-Driven** | 3 | `PaymentEvent` dispara pipeline; `AgentNotifier` notifica após aprovação |
| **Harness Evolution** | 3 | Polling ativo como fallback; exponential backoff; compensação |
| **Continuous Operation** | 3 | Cron jobs com distributed locks para 24/7 |

---

## 9. Como Cada Sintoma é Resolvido

| Sintoma | Causa | Solução |
|---------|-------|---------|
| "não achou o pedido no Bling" | Sync com Bling falhou silenciosamente na NuvemShop | `BlingSyncAgent` verifica ativamente após pagamento. `BlingSyncLog` rastreia cada tentativa. Se falhar 5x, `AlertEvent` escala para humano |
| "agent não recebeu o pedido" | Agente só consulta status sob demanda (pull) | `AgentNotifier` faz push notification pós-pagamento. Cria `Message` de sistema na conversa. `ConversationStateBuilder` carrega contexto na próxima interação |
| "pagamento foi feito" | Dinheiro saiu mas sistema não reagiu | `PaymentEvent` persiste antes de processar. Se webhook não chega, cron job faz polling no gateway a cada 60s e cria `PaymentEvent` retroativo. Garantia: TODO pagamento vira `PaymentEvent` |

---

## 10. Riscos e Mitigações

| Risco | Impacto | Mitigação |
|-------|:-------:|-----------|
| Aumento de latência no webhook | Médio | Handler responde 200 imediatamente (só persiste). Processamento é assíncrono |
| Complexidade adicional (mais agentes, mais estados) | Médio | Cada agente tem ownership claro. `OrderAuditLog` garante rastreabilidade. Currículo Nível 3: _"cada agente precisa de um contrato verificável"_ |
| NuvemShop não expõe endpoint de sync status com Bling | Alto | Verificar com fornecedor antes da Fase 4. Alternativa: polling no endpoint de detalhes do pedido |
| Migração de schema em produção | Médio | Novas tabelas são aditivas (não alteram schema existente). Rollback é remover as tabelas |
| Custo adicional de LLM (Supervisor é um nó LangGraph) | Baixo | Supervisor usa `temperature=0.1`, prompt curto, cache de rota. Custo estimado: $0.02 por pedido |

---

## Apêndice A: Evidências do Código Atual

Trechos relevantes do código atual que fundamentam o diagnóstico:

**Webhook handler (sem retry):**
`src/routes/webhook-payment.ts` — recebe webhook, processa sincronamente. Se `order` é `null`, retorna 200 com "order not found" e não agenda retry.

**Agente sem push notification:**
`src/agents/graph/nodes/ecommerceAgenteNode.ts` — as tools `GetLastOrderStatusTool` e `GetOrderTrackingTool` só são chamadas quando o cliente pergunta. Não há trigger proativo pós-pagamento.

**Carrinho sobrevive no DB até pagamento:**
`src/agents/graph/tools/ecommerce/CreateOrderTool.ts` — `postOrderCleanup()` só limpa carrinho em **memória**. O DB (`EcommerceCart` + `CartItem`) permanece intacto. A limpeza do DB só ocorre no webhook de pagamento (`cartService.clearCart()`) ou no cron de expiração (24h).

**Message queue em memória:**
`src/services/queue/MessageProcessingQueue.ts` — `Map<string, Promise<void>>`. Crash = perda da fila.

**Schema atual sem PaymentEvent dedicado:**
`prisma/schema.prisma` — `PaymentWebhookEvent` existe mas é usado apenas para idempotência. Não tem `retryCount`, `nextRetryAt`, nem `status` com máquina de estados.

---

## Apêndice B: Referências do Currículo

- `curriculum/03-nivel-3-advanced-architecture/01-multi-agent-systems.md` — decomposição em Planner/Generator/Evaluator, handoffs entre agentes
- `curriculum/03-nivel-3-advanced-architecture/02-state-persistence.md` — estados imutáveis, retry do último evento confirmado
- `curriculum/03-nivel-3-advanced-architecture/03-file-based-coordination.md` — locks, status files, `retryable`, `error.json`
- `curriculum/03-nivel-3-advanced-architecture/05-harness-evolution.md` — fallback, exponential backoff, compensação
- `curriculum/02-nivel-2-practical-patterns/03-rubric-design.md` — rubricas multi-dimensão com gates
- `curriculum/09-case-studies/04-koda-order-processing.md` — case study de processamento de pedidos multi-step

---

*Documento gerado para o time técnico | 26 Maio 2026*
