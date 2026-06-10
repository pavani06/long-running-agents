---
title: "Diagnóstico: Arquitetura KODA no mhc-backend vs. Nível 3 de Referência"
type: analysis
date: 2026-05-26
domain: mhc-backend
aliases: []
tags: [analise, mhc-backend, diagnostico, nivel-3, arquitetura-avancada]
last_updated: 2026-06-10
---

# Diagnóstico: Arquitetura KODA no mhc-backend vs. Nível 3 de Referência

**Repositório analisado:** https://github.com/chatshop-io/mhc-backend.git
**Documento de referência:** `curriculum/03-nivel-3-advanced-architecture/koda-applications/nivel-3-koda.md`
**Data da análise:** Maio 2026

---

## Diagnóstico de Maturidade

O KODA no mhc-backend está entre **Nível 1 e Nível 2** da taxonomia de referência. Ele possui _foundation_ (prompts, tools, logging) e parcialmente _visibility_ (timings, traces), mas **nenhum dos 5 padrões de Nível 3 foi implementado**. A arquitetura atual opera essencialmente como um **agente único com prompt engineering avançado**, e não como um sistema multi-agente coordenado.

---

## Padrão 1: Sistemas Multi-Agente

| Requisito Nível 3 | mhc-backend (real) | Gap |
|---|---|---|
| **Planner Agent** — decide a etapa da jornada | **Inexistente.** A decisão de etapa (`navegando`, `adicionando_carrinho`, `checkout`, `pagamento`, `finalizado`) existe como campo no `ConversationContext`, mas sempre retorna `"navegando"` no `ConversationStateBuilder:519`. O planejamento é implícito no prompt. | Não há separação de responsabilidade. O prompt de ecommerce (~1800 linhas) contém todas as regras de discovery, recomendação, checkout e recompra. |
| **Discovery Agent** — extrai intenção e restrições | **Inexistente como agente separado.** O onboarding (4 perguntas sobre esporte, frequência, suplementos, restrições) é feito inline pelo mesmo prompt. Restrições são registradas via `saveMemoryTool` para a tabela `ConversationMemory`. | O prompt decide se faz onboarding ou vai direto para produto. Não há artefato `discovery.json` auditável. |
| **Catalog Agent** — consulta produtos e estoque | **Implementado como tool, não como agente.** As tools `searchProductsTool`, `getCatalogMetadataTool`, `getProductDetailsTool` fazem a busca. Mas são chamadas pelo mesmo agente monolítico, sem orquestração externa. | Tool ≠ agente. Sem separação de responsabilidade. |
| **Generator Agent** — cria respostas e artefatos comerciais | **Inexistente como agente separado.** A geração de resposta é output direto do LLM no `ecommerceAgenteNode`. | Toda resposta é gerada em uma única chamada LLM. |
| **Evaluator Agent** — avalia segurança, tom, contrato | **Inexistente como agente separado.** A "avaliação" existe como regras de prompt: `FAIL-SAFE`, `RESTRICAO_VALIDADA`, `GATE DE SEGURANÇA`. Não há um segundo LLM verificando output. | Segurança é prompt-level, não um agente independente com rubrics. |
| **Order Agent** — monta carrinho e pedido | **Implementado como tool, não como agente.** `createOrderTool`, `addToCartTool`, `updateCartItemTool`, etc. | Sem coordenação multi-agent. As tools são chamadas inline pelo mesmo prompt. |
| **Fulfillment Agent** — reserva estoque e prepara entrega | **Implementado como tool, não como agente.** `sendDeliveryFlowTool`, `calculateShippingTool`. | Mesmo gap. |
| **Recovery Agent** — retoma fluxo após falha | **Parcial, via prompt.** Existe detecção de "carrinho de sessão anterior" (`detectStaleCart`) no `ecommerceAgenteNode`. Mas não há checkpoint recovery. | Recuperação depende de estado em memória + DB. Sem checkpoints explícitos. |

### Topologia real do grafo LangGraph

```
START → [ecommerceAgenteNode] → END
         (único nó ativo em produção)
```

Em modo multi-agente (não usado em produção), seria:

```
START → routerNode → (coach | ecommerce | voturuna) → END
```

O `OrchestratorAgent` (`ecommerce-agent`) é o único registrado em `src/config/agents.ts:43`. O `AgentRouter.routeMessage()` está em modo "always ecommerce" com um comentário `TODO: Para voltar a alternar entre agentes, descomentar a lógica abaixo`.

**Conclusão:** A arquitetura atual é **Single Agent com tools** — o equivalente ao "Protótipo / Nível 1" da referência. Não há Planner, Evaluator, ou qualquer decomposição real de responsabilidades entre agentes.

---

## Padrão 2: Persistência de Estado

| Requisito Nível 3 | mhc-backend (real) | Gap |
|---|---|---|
| **SQLite checkpoints** | **Inexistente.** Nenhum SQLite é usado. O banco é **PostgreSQL** via Prisma. | PostgreSQL é mais robusto que SQLite, então isso não é um gap negativo — mas não há tabela de checkpoints. |
| **`customer_profile.json`** (restrições, objetivos, preferências) | **Parcial.** Dados existem em várias tabelas: `User` (dietaryRestriction, ecommerceBudgetMax, athleticGoal), `UserLifestyleBaseline`, `UserExpenseBudget`, `UserHealthCondition`, `UserRestriction`, `ConversationMemory`. | Fragmentado em 6+ tabelas. Não há um artefato unificado de perfil. |
| **`cart.json`** (itens, preço travado, cupom, frete) | **Híbrido e frágil.** `CartService` usa `Map<string, CartItem[]>` em memória com 24h de expiração. Existe tabela `EcommerceCart` + `CartItem` no PostgreSQL, mas o `ConversationStateBuilder.getActiveCart()` prioriza o `cartService.getCart()` que opera em memória. | **Carrinho NÃO sobrevive a restart do processo.** A tabela DB existe mas o código usa o cache em memória como fonte primária. |
| **`order_state.json`** (status do pedido, pagamento) | **Parcial.** Tabela `Order` com `status`, `paymentStatus`, `paidAt`, `expiresAt`. Pagamento via Stripe com webhook `PaymentWebhookEvent`. | Sem checkpoint explícito de estado de order. O estado está no DB, mas não há mecanismo de snapshot no ponto crítico (antes de gerar link de pagamento). |
| **`agent_plan.json`** (etapa atual, próxima ação) | **Inexistente.** O campo `ConversationContext.status` existe mas sempre retorna `"navegando"`. | Não há planejamento explícito serializado. |
| **`audit_manifest.json`** (artefatos que sustentam a decisão) | **Inexistente.** Não há registro de quais ferramentas/artefatos foram usados para produzir uma resposta. Existe `MessageLog` e `AuditLog`, mas não um manifest linking outputs to inputs. | Sem rastreabilidade de decisão. |

**O incidente do Pedro (carrinho perdido após restart) ACONTECERIA neste sistema.** O `CartService` usa `Map` em memória. Embora exista tabela `EcommerceCart` no PostgreSQL, o `ConversationStateBuilder` chama `cartService.getCart()` que opera no cache em memória. Se o processo reiniciar, o cache se perde e o carrinho some.

**Código crítico em `CartService.ts:12`:**
```typescript
private carts: Map<string, CartItem[]> = new Map();
```

---

## Padrão 3: Coordenação por Arquivos

| Requisito Nível 3 | mhc-backend (real) | Gap |
|---|---|---|
| **`order.lock.json`** com TTL | **Inexistente como arquivo.** Existe lock em memória no `CartService` (`acquireLock/release` com `Map<string, Promise<void>>`) e lock distribuído via Redis no `MessageDebounceService`. | Lock em memória não sobrevive a restart. Lock em Redis existe mas não é usado no fluxo de order. |
| **`status.json`** visível para todos os agentes | **Inexistente como arquivo.** O status está no campo `ConversationContext.status` do PostgreSQL, mas sempre retorna `"navegando"` no builder (linha 521). | O status não é usado ativamente para coordenação. |
| **`manifest.json`** (audit trail da decisão) | **Inexistente.** | Sem rastreabilidade. |
| **Atomic writes** | **Parcial.** Redis locks implementam exclusão mútua para debounce. Cron jobs usam `prisma.cronLock.upsert`. Mas o fluxo de order não tem atomicidade cross-service. | O `MessageProcessingQueue` tem um race condition documentado (`FIXME-RACE-CONDITIONS` em AGENTS.md:160). |
| **Prevenção de duplicados** | **Forte.** Webhook dedup por `whatsappMessageId`. Outbound por `idempotencyKey` no `MessageLog`. Pagamentos por `externalId` único no `PaymentWebhookEvent`. Reminders por `(userId, scheduledTime)` único. | Este ponto está bem implementado — mas opera em nível de mensagem, não de coordenação entre agentes. |

**O incidente da Marina (dois pedidos com SKUs diferentes) PODERIA ACONTECER neste sistema** em condições de corrida, pois o lock do `CartService` é apenas em memória e o `MessageProcessingQueue` tem race conditions documentadas.

---

## Padrão 4: Compactação Server-Side

| Requisito Nível 3 | mhc-backend (real) | Gap |
|---|---|---|
| **Compactação que preserva alergias, orçamento, preferências** | **Inexistente como pipeline de compactação.** Existe `MemoryExtractionService` que extrai fatos (dietary, medical, preferences) das mensagens do usuário e salva em `ConversationMemory`. Existe `MemoryService.recall()` que recupera memórias por categoria. Existe `SummaryService` para daily summaries de health data. | Extrai fatos, mas não compacta a conversa. O histórico é truncado a 60 mensagens (WhatsApp) ou 20 (API), sem sumarização do que foi cortado. |
| **Classificação de criticidade antes de sumarizar** | **Inexistente.** Não há classificação de criticidade. O `MemoryExtractionService` extrai tudo que parece relevante, sem ranking. | Fatos como "evito cafeína" e "gosto de chocolate" têm o mesmo tratamento. |
| **Remoção de ruído social e repetição** | **Inexistente.** O histórico de conversa é carregado integralmente (60 mensagens), sem filtragem de ruído. | Conversas longas (4h+) terão seu contexto truncado, e o que for cortado some sem sumarização. |

**O incidente do Rafael (cafeína sugerida após 4h de conversa) ACONTECERIA neste sistema.** Após 60 mensagens, o histórico mais antigo é truncado sem compactação. Se a restrição de cafeína foi mencionada nas primeiras mensagens e a conversa já passou de 60 turnos, essa informação some. O `MemoryExtractionService` pode ter extraído a restrição para `ConversationMemory`, mas o recall depende de o agente chamar `recallMemoriesTool` — o que só acontece se o prompt instruir.

**Código crítico em `ConversationStateBuilder.ts:59`:**
```typescript
const historyLimit = isApiChannel ? 20 : 60;
```

---

## Padrão 5: Evolução do Harness

| Requisito Nível 3 | mhc-backend (real) | Gap |
|---|---|---|
| **Métricas de custo** | **Inexistente.** Há `StageTimings` com `measureAsyncStage` medindo latência de cada etapa (build_state_ms, graph_invoke_ms, etc.), mas sem tracking de custo por chamada LLM (tokens, $). | Sem visibilidade de custo. |
| **Decision records** | **Inexistente.** Não há ADRs ou decision records no código. | Sem registro de por que decisões arquiteturais foram tomadas. |
| **Remoção segura de componentes** | **Parcial.** O código tem `TODO` e `DEPRECATED` markers. Existe `// TODO ANALISAR ESSA CLASSE TBM` em `ConversationStateBuilder`. Mas não há métricas para justificar remoção. | Sem medição de custo/valor por componente. |
| **Métricas do sistema** | **Parcial.** Winston structured logging com trace JSON por turno. Endpoint `GET /admin/analytics` existe mas não foi inspecionado em detalhe. | Logging existe, mas não há dashboard de evolução arquitetural. |

---

## Resumo Visual: Mapa de Gaps

```
Padrão Nível 3          │ mhc-backend KODA           │ Gap
─────────────────────────┼────────────────────────────┼──────────────────────────
Multi-Agent (Planner,    │ Single Agent + tools       │ CRÍTICO: sem decomposição
Generator, Evaluator,    │ (1 prompt de 1800 linhas)  │ real de responsabilidades
Discovery, Catalog,      │                             │
Order, Fulfillment,      │                             │
Recovery)                │                             │
─────────────────────────┼────────────────────────────┼──────────────────────────
State Persistence        │ PostgreSQL (bom) + Redis    │ ALTO: carrinho em memória
(SQLite checkpoints,     │ + CartService em memória    │ não sobrevive restart;
JSON snapshots)          │ (frágil)                    │ sem checkpoints explícitos
─────────────────────────┼────────────────────────────┼──────────────────────────
File-based Coordination  │ Redis locks + in-memory     │ ALTO: sem lock files,
(lock.json, status.json, │ locks; sem manifest         │ manifest, ou audit trail
manifest.json, atomic    │                             │ por decisão
writes)                  │                             │
─────────────────────────┼────────────────────────────┼──────────────────────────
Server-side Compaction   │ MemoryExtraction +          │ ALTO: sem compactação de
(classificação de        │ truncamento a 60 msgs       │ conversa; fatos críticos
criticidade)             │                             │ podem ser perdidos
─────────────────────────┼────────────────────────────┼──────────────────────────
Harness Evolution        │ Timings + logging           │ MÉDIO: sem tracking de
(métricas de custo, ADRs,│ estruturado; sem custo ou   │ custo ou decision records
remoção segura)          │ ADRs                        │
```

---

## Arquivos-Chave Referenciados

| Arquivo | Função no KODA |
|---|---|
| `src/agents/orchastrator/OrchestratorAgent.ts` | Agente principal — único ponto de entrada para mensagens WhatsApp |
| `src/agents/graph/nodes/ecommerceAgenteNode.ts` | Nó LangGraph que executa o LLM com ~20 tools |
| `src/agents/graph/agentsGraph.ts` | Topologia do grafo — atualmente single-node (ecommerce) |
| `src/agents/orchastrator/ConversationStateBuilder.ts` | Monta o estado do agente (user, cart, history, context) a cada turno |
| `src/agents/prompts/ecommerce/index.ts` | Prompt monolítico de ~1800 linhas com todas as regras de negócio |
| `src/agents/prompts/persona/ecommerce.ts` | Persona "Votu" — tom e escopo de atuação |
| `src/agents/prompts/global/rules.ts` | Regras globais: idioma, segurança, handoff, anti-alucinação |
| `src/services/ecommerce/CartService.ts` | Carrinho híbrido (memória + DB) com lock em memória |
| `src/services/memory/MemoryService.ts` | Persistência de fatos do usuário (dietary, medical, preferences) |
| `src/services/memory/MemoryExtractionService.ts` | Extração assíncrona de memórias das mensagens do usuário |
| `src/services/queue/MessageProcessingQueue.ts` | Fila em memória com race condition documentada |
| `src/services/queue/MessageDebounceService.ts` | Debounce com Redis lock distribuído |
| `src/config/agents.ts` | Registro de agentes — apenas `ecommerce-agent` ativo |
| `prisma/schema.prisma` | 50+ modelos — inclui `EcommerceCart`, `CartItem`, `Order`, `ConversationContext`, `ConversationMemory` |

---

## Conclusão

O KODA no mhc-backend é um sistema funcional e bem instrumentado (logging, traces, dedup forte, memory extraction), mas sua arquitetura é fundamentalmente **monolítica em termos de agente**: um único prompt de 1800 linhas orquestrando ~20 tools em uma chamada LLM, sem decomposição de responsabilidades entre Planner/Generator/Evaluator/Discovery/Order/Fulfillment, sem checkpoints explícitos de estado, sem coordenação por arquivos, sem compactação de conversa, e sem métricas de evolução arquitetural.

Os incidentes descritos no documento de referência (Pedro: carrinho perdido, Marina: pedido duplicado, Rafael: contexto degradado) **poderiam ocorrer neste sistema** devido à dependência de estado em memória para o carrinho, race conditions documentadas na fila de mensagens, e truncamento de histórico sem compactação.

O caminho para Nível 3 exigiria decompor o prompt monolítico em agentes especializados com artefatos JSON auditáveis, migrar o carrinho para armazenamento durável com checkpoints explícitos, implementar lock files e manifestos por decisão, e adicionar compactação server-side com classificação de criticidade.
