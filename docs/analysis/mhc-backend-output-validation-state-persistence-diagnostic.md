# Diagnóstico: Output Validation & State Persistence no mhc-backend

**Data:** 2026-05-28
**Escopo:** Análise cruzada dos padrões de Output Validation e State Persistence — como o agente valida outputs do LLM antes de persistir estado entre turnos.

---

## Objetivo

Mapear toda a cadeia de validação de outputs do LLM e sua relação com a persistência de estado, identificando:
- Onde e como outputs são validados
- O que acontece quando a validação falha
- A ordem: validação → persistência (ou persistência → validação?)
- Gaps em relação ao padrão ideal

---

## Arquitetura de Validação em 4 Camadas

O mhc-backend **não** tem um único subsistema de "output validation". Em vez disso, implementa 4 camadas distintas, cada uma validando em um ponto diferente do pipeline, e todas operando **antes** da persistência de estado.

```
LLM output → [Camada 1: LangChain Zod] → [Camada 2: Business Validation] → [Camada 3: Structured Output Parsing] → [Camada 4: Contradiction Detection] → State Persistence
```

---

## Camada 1: LangChain Zod Schema Validation (Tool Boundary)

**Arquivos:** Todas as 20+ tools em `src/agents/graph/tools/**`

Cada `DynamicStructuredTool` declara um schema Zod que o LangChain usa para **forçar o LLM a produzir argumentos tipados**. Se o LLM produz algo inválido, o framework rejeita e força retry. Isso é **input validation** para tool calls, mas age como **output validation indireta** — o LLM precisa estruturar sua "decisão" (qual tool chamar + com quais args) em formato validado.

**Exemplo — AddToCartTool** (`src/agents/graph/tools/ecommerce/AddToCartTool.ts`):
```typescript
schema: z.object({
  productId: z.string(),       // LLM DEVE passar string
  productName: z.string(),     // LLM DEVE passar string
  quantity: z.number().int(),  // LLM DEVE passar número inteiro
})
```

**Exemplo — SaveMemoryTool** (`src/agents/graph/tools/memory/SaveMemoryTool.ts`):
```typescript
schema: z.object({
  category: z.enum(["preferences", "dietary", "medical", "goals", "history", "routine"]),
  key: z.string(),
  value: z.string(),
})
```

O `z.enum()` força o LLM a escolher uma das 6 categorias. Qualquer outra string é rejeitada.

---

## Camada 2: Business Validation nos Tool Handlers (Pre-Persistence Gate)

Esta é a camada mais relevante para a relação com **State Persistence**. Os handlers validam regras de negócio e **só persistem estado se todos os gates passarem**.

### SearchProductsTool — Filtro antes de persistir `shownProducts`

`src/agents/graph/tools/ecommerce/SearchProductsTool.ts:166-208`

```typescript
// GATE 1: Só aplica filtro se onboarding completo
if (agentState.onboardingData?.isComplete) {
  const filtered = productRecommendationFilter.filterProducts(
    products, agentState.onboardingData,
  );
  products = filtered.allowed;
  // Se TODOS bloqueados → NÃO persiste, retorna erro
  if (products.length === 0) {
    return { success: false, message: "Todos produtos foram filtrados..." };
  }
}
// GATE 2: Só persiste após filtro passar
await conversationStateBuilder.updateShownProducts(userId, products);
```

**Relação com State Persistence:** O estado persistido (`onboardingData`) é usado como **input** da validação. O resultado validado (`shownProducts`) só é persistido se passar nos filtros.

### AddToCartTool — 4 gates antes de persistir carrinho

`src/agents/graph/tools/ecommerce/AddToCartTool.ts:31-95`

| Gate | Validação | Se falhar |
|---|---|---|
| 1 | `quantity > 0` | Retorna erro, NÃO persiste |
| 2 | `productId` é numérico (`/^\d+$/`) | Retorna erro, NÃO persiste |
| 3 | Produto existe no catálogo (`ecommerceClient.getProduct()`) | Retorna erro, NÃO persiste |
| 4 | **Estoque suficiente** (`newTotalQty <= product.stock`) | Retorna erro com `availableStock` e `currentInCart` |

```typescript
if (newTotalQty > product.stock) {
  return {
    success: false,
    error: `Estoque insuficiente. Disponível: ${product.stock}. Você já tem ${currentQty} no carrinho.`,
    availableStock: product.stock,
    currentInCart: currentQty,
  };
}
// PERSISTÊNCIA: Só se TODOS os gates passarem
await conversationStateBuilder.addToCart(userId, productId, newTotalQty, product);
```

### CreateOrderTool — Pipeline de 8 gates com retomada

`src/agents/graph/tools/ecommerce/CreateOrderTool.ts:52-137`

Esta é a tool com a validação mais extensa do sistema:

| Gate | O que valida | Se falhar |
|---|---|---|
| 1 | Carrinho vazio (`cart.items.length === 0`) | Bloqueia com `isEmpty: true` |
| 2 | Endereço (`!shippingAddress`) | **Salva `checkoutSession`** para retomar |
| 3 | Email real (`isMissingEmail(user)`) | **Salva `checkoutSession`** |
| 4 | CPF (`!user?.cpf`) | **Salva `checkoutSession`** |
| 5 | Nome completo (`isMissingFullName(user)`) | **Salva `checkoutSession`** |
| 6 | Autorização (`!agentState.authorization?.customerId`) | Bloqueia |
| 7 | Estoque por item (`product.stock < item.quantity`) | Bloqueia com detalhes do produto |
| 8 | Frete (`!shipping`) | Instrui LLM a chamar `calculate_shipping` |

**Relação crítica com State Persistence:** Quando um gate falha (2-5), o estado é salvo como `checkoutSession` (TTL 1h) para que o usuário **não precise recomeçar**. Isso é output validation que produz **estado de fallback** — uma proteção contra perda de contexto.

---

## Camada 3: Structured Output Parsing (LLM JSON → Zod → Persist)

### RouterNode — Único uso de `withStructuredOutput`

`src/agents/graph/nodes/routerNode.ts:11-13`

```typescript
const routerSchema = z.object({
  route: z.enum(["coach", "ecommerce", "voturuna"]),
});

const routerModel = new ChatOpenAI({
  model: "gpt-4.1-mini",
}).withStructuredOutput(routerSchema, {
  name: "route_classifier",
  strict: true,
});
```

**Bug encontrado:** O prompt (linhas 93-95 e 118-122) instrui o LLM a retornar `{"route": "clarification"}` para certos cenários, mas o schema Zod **só aceita** `coach | ecommerce | voturuna`. O `strict: true` faz com que `clarification` seja rejeitado pelo framework, forçando o LLM a escolher uma das 3 rotas válidas. O fluxo `clarification` é **inalcançável**.

### MemoryExtractionService — Único true output validator

`src/services/memory/MemoryExtractionService.ts`

Este é o caso mais próximo do padrão ideal: o LLM gera JSON com fatos extraídos da conversa, o serviço faz `safeParse()` com Zod, e **só persiste se válido**:

```
Conversa do usuário → LLM extrai fatos → JSON text → ExtractedMemorySchema.safeParse() → MemoryService.save()
```

Executado em **background** após cada resposta do agente (non-blocking). Se falhar, o erro é logado e descartado — não interrompe o fluxo principal.

### FlowResponseProcessor — Validação de formulários WhatsApp

`src/services/whatsapp/FlowResponseProcessor.ts`

Normaliza e valida JSON de respostas de WhatsApp Flow (onboarding, delivery) antes de persistir no banco. A validação é feita no entrypoint `webhook-unified.ts`, que recebe `response_json`, parseia e repassa ao processor.

---

## Camada 4: Contradiction Detection (Consistência do Estado)

### MemoryService.deactivateContradictions()

`src/services/memory/MemoryService.ts:43-80`

Validação que opera **sobre o estado já persistido** antes de adicionar nova informação:

```typescript
async save(userId: string, data: SaveMemoryInput): Promise<Memory> {
  // VALIDAÇÃO: Soft-delete de memórias contraditórias ANTES de salvar
  await this.deactivateContradictions(userId, data);

  // PERSISTÊNCIA: Só após limpar contradições
  const memory = await prisma.conversationMemory.create({ ... });
  return memory;
}
```

Regras:
- Se salva "intolerante a lactose" → soft-delete de `no_restrictions`, `no_allergies`
- Se salva "sem restrições" → soft-delete de todas as restrições alimentares existentes

Isso garante que o estado persistido é **internamente consistente** — output validation no nível do banco.

---

## ProductRecommendationFilter — A Ponte Entre Output Validation e State Persistence

`src/services/ecommerce/ProductRecommendationFilter.ts`

Este serviço é o ponto onde as duas preocupações se encontram de forma mais explícita:

```
filterProduct(product, onboardingData)
  │
  ├─ [1] checkHealthRestrictions()    ← usa estado PERSISTIDO (onboardingData)
  │     ├─ Alergias (SEVERO → BLOQUEIA)
  │     │   └─ Verifica nome, descrição, tags do produto
  │     │   └─ Respeita exceções "sem X", "X-free", "free de X"
  │     ├─ Restrições alimentares severas (BLOQUEIA)
  │     ├─ Restrições não-severas (AVISO)
  │     └─ Condições diagnosticadas (AVISO contextual)
  │         ├─ Diabetes + açúcar → warning
  │         └─ Hipertensão + cafeína → warning
  │
  └─ [2] checkBudget()                ← usa estado PERSISTIDO (budget)
        ├─ Mapeia categoria do produto → budget
        ├─ Preço > budget → BLOQUEIA
        └─ Preço >= 80% do budget → AVISO
```

O estado que foi **persistido** em turnos anteriores (onboarding via WhatsApp Flow → `UserRestriction`, `UserHealthCondition`, `UserExpenseBudget`) é usado como **input para validar** os outputs do agente (produtos recomendados). Se o produto falha, ele é removido da lista **antes** de ser mostrado ao usuário e **antes** de ser persistido como `shownProducts`.

### Tipos de resultado

```typescript
interface ProductFilterResult {
  allowed: boolean;   // Se produto passa em TODOS os filtros
  reason?: string;    // Razão de bloqueio (se allowed = false)
  warnings?: string[]; // Avisos contextuais (mesmo se allowed = true)
}
```

---

## Fluxo Completo: Validação + Persistência em 1 Turno

```
Usuário: "quero um whey sem lactose até R$100"
  │
  ▼
OrchestratorAgent.processMessage()
  │
  ├─ ConversationStateBuilder.buildState()
  │   └─ CARREGA estado PERSISTIDO: onboardingData, memories, cart, context, etc.
  │
  ▼
LangGraph Agent (ecommerceAgenteNode)
  │
  ▼
LLM → search_products(query="whey", attributes="sem-lactose")
  │
  ├─ [CAMADA 1] LangChain valida args contra Zod schema ✓
  │
  ▼
SearchProductsTool handler
  │
  ├─ [1] Pinecone search → retorna N produtos
  ├─ [2] productRecommendationFilter.filterProducts(onboardingData)
  │     ├─ checkHealthRestrictions() → bloqueia produtos COM lactose
  │     └─ checkBudget() → bloqueia produtos > R$100
  ├─ [3] Se todos bloqueados → retorna erro (NÃO persiste)
  └─ [4] updateShownProducts() → persiste mapeamento ID→Nome
  │
  ▼
LLM apresenta produtos ao usuário (texto livre — NÃO validado estruturalmente)
  │
  ▼
Usuário: "quero o primeiro"
  │
  ▼
LLM → add_to_cart(productId="123", productName="Whey Isolado", quantity=1)
  │
  ├─ [CAMADA 1] LangChain valida args contra Zod schema ✓
  │
  ▼
AddToCartTool handler
  │
  ├─ quantity > 0 ✓
  ├─ productId numérico ✓
  ├─ Produto existe no catálogo ✓
  ├─ Estoque suficiente ✓
  └─ conversationStateBuilder.addToCart() → CartService → PostgreSQL
  │
  ▼
Background: MemoryExtractionService
  │
  ├─ [CAMADA 3] LLM extrai fatos → JSON → ExtractedMemorySchema.safeParse()
  ├─ [CAMADA 4] MemoryService.deactivateContradictions()
  └─ prisma.conversationMemory.create()
```

---

## As 4 Camadas de Estado Persistido

```
┌──────────────────────────────────────────────────────────┐
│ CAMADA 1: Memória Semântica (ConversationMemory)         │
│ Storage: PostgreSQL    Ciclo: permanente ou expiresAt    │
│ Validação: deactivateContradictions() antes de INSERT    │
│ Conteúdo: preferências, restrições, metas, histórico     │
│ Categorias: preferences | dietary | medical | goals      │
│             history | routine                            │
├──────────────────────────────────────────────────────────┤
│ CAMADA 2: Contexto de Conversa (ConversationContext)     │
│ Storage: PostgreSQL    Ciclo: permanente                 │
│ Validação: normalizeAskedQuestions() no load             │
│ Conteúdo: askedQuestions, status, discoveryContext       │
├──────────────────────────────────────────────────────────┤
│ CAMADA 3: Estado Transacional (Cart + Address + Profile) │
│ Storage: Map (memória) + PostgreSQL                      │
│ Validação: 4-8 gates por tool ANTES de persistir         │
│ TTL: 24h inatividade (cart), 12h (address)               │
│ Conteúdo: cart, shipping, athlete profile, shownProducts │
├──────────────────────────────────────────────────────────┤
│ CAMADA 4: Cache de Performance (Redis + In-Memory)       │
│ Storage: Redis (3min TTL) + Map (30min TTL)              │
│ Validação: Nenhuma (dados regeneráveis)                  │
│ Conteúdo: profile_state, coaching state                  │
└──────────────────────────────────────────────────────────┘
```

### Ciclo de vida e limpeza

| Estado | TTL | Limpeza |
|---|---|---|
| ConversationMemory | Configurável (null = ∞) | Cron horário (`memory-cleanup`) |
| Cart (in-memory) | Até invalidação | Escrita no DB |
| Cart (DB) | 24h inatividade / 24h sem pagamento | Cron ecommerce (`inactive_conversation_cleanup`, `unpaid_order_cart_cleanup`) |
| ShippingAddress | 12h inatividade | Cron ecommerce |
| CheckoutSession | 1 hora | Limpeza em memória |
| Coach State Cache | 30 minutos | Limpeza em memória (5min) |
| Profile Cache (Redis) | 3 minutos | Redis TTL automático |
| shownProducts / lastViewedProduct | Duração da sessão | Perdido no restart do processo |

---

## Gaps vs Padrão Ideal

| Mecanismo | Status | Detalhe |
|---|---|---|
| Forçar formato estruturado | ✅ Forte | Zod schemas em 20+ tools; LangChain valida na fronteira |
| `recommendation` (qual produto) | ✅ Forte | LLM escolhe tool + args → tool executa e retorna resultado estruturado |
| `reasoning` (por que) | ⚠️ Parcial | LLM gera em linguagem natural na resposta; sem campo estruturado dedicado |
| `alternatives` | ⚠️ Parcial | `SearchProductsTool` retorna múltiplos produtos; LLM decide quais apresentar. Sem campo dedicado |
| `confidence` (0-100%) | ❌ Ausente | Nenhuma tool produz scoring de confiança |
| `risk_flags` | ⚠️ Parcial | `ProductRecommendationFilter` gera `warnings[]` internamente, mas **não expõe ao LLM** como campo estruturado |
| `contradicts_previous_preferences` | ⚠️ Parcial | `MemoryService.deactivateContradictions()` detecta entre memórias, mas não entre recomendação e preferências |
| Retry loop em falha de parsing | ✅ Forte | LangChain gerencia automaticamente em falha de schema Zod |
| Business validation pós-geração | ✅ Forte | `ProductRecommendationFilter`, validação de estoque, pipeline de 8 gates no checkout |
| Fallback seguro em falha total | ⚠️ Parcial | Erros retornam `success: false` com mensagem; `CheckoutSession` salva estado para retomar. Sem "produto seguro default" |
| Validação pré-persistência | ✅ Consistente | Todos os handlers validam antes de chamar `conversationStateBuilder` |
| Auditoria de decisões | ❌ Ausente | Sem log de "quem recomendou X e por quê" |
| `confidence_score` / `last_confirmed_date` | ❌ Ausente | Memórias têm `createdAt`/`updatedAt` mas não campo de confiança |
| `clarification` no router | ❌ Bug | Prompt instrui retornar `"clarification"` mas Zod schema rejeita (`strict: true`) |

---

## Bugs e Inconsistências Identificados

### 1. Router: `clarification` inalcançável

**Arquivo:** `src/agents/graph/nodes/routerNode.ts`

O prompt do router (linhas 93-95 e 118-122) instrui o LLM a retornar `{"route": "clarification"}` para perguntas sobre o parque Voturuna. Porém, o schema Zod (linha 12) define `z.enum(["coach", "ecommerce", "voturuna"])` com `strict: true` (linha 209). O LangChain rejeita `clarification` e força o LLM a escolher uma das 3 rotas válidas.

### 2. `shownProducts` e `lastViewedProduct` são voláteis

**Arquivo:** `src/services/ecommerce/CartService.ts`

Estes dados são armazenados apenas em Map (memória) e são perdidos no restart do processo. Não há fallback para banco de dados.

### 3. `ConversationStateBuilder.updateConversationStatus()` é no-op

**Arquivo:** `src/agents/orchastrator/ConversationStateBuilder.ts:607-628`

O método apenas loga o status, sem persistir. O comentário no código diz "Implementar persistência se necessário".

### 4. Sem checkpointer no LangGraph

**Arquivo:** `src/agents/agentsGraph.ts`

O grafo é compilado sem checkpointer (`workflow.compile()` sem argumentos). O `thread_id` é passado na invocação mas não há persistência de estado do grafo entre execuções. O estado é reconstruído do zero a cada turno pelo `ConversationStateBuilder`.

---

## Recomendações

### Curto prazo (quick wins)

1. **Corrigir o bug do router:** Remover menções a `clarification` do prompt ou adicionar `"clarification"` ao `z.enum()` e tratar o caso no `conditionalMap` do `agentsGraph.ts`
2. **Persistir `shownProducts` no banco** para sobreviver a restarts — criar tabela `ShownProduct` ou usar Redis com TTL maior
3. **Implementar `updateConversationStatus()`** para persistir o status real no `ConversationContext`

### Médio prazo (melhorias estruturais)

4. **Adicionar `confidence_score` nas memórias** — campo `confidence` (0-100) no model `ConversationMemory`, atualizado a cada confirmação do usuário
5. **Expor `risk_flags` ao LLM** — passar `ProductRecommendationFilter.warnings[]` como campo estruturado no contexto para o LLM contextualizar a resposta
6. **Adicionar audit trail de recomendações** — log de qual produto foi recomendado, por qual tool, com qual reasoning, e se o usuário aceitou

### Longo prazo (arquitetura)

7. **Adicionar LangGraph checkpointer** para checkpointing nativo do grafo entre turnos (reduziria a dependência do `ConversationStateBuilder` para reconstrução completa)
8. **Unificar validação de estado** — um schema Zod único para o `AgentState` completo, validado antes de cada persistência
9. **Adicionar `last_confirmed_date`** em preferências e restrições para detectar dados desatualizados

---

## Resumo

O mhc-backend implementa output validation como **gates distribuídos** que bloqueiam ações inválidas **antes** da persistência de estado. A arquitetura é:

1. **LangChain Zod** — barreira de tipo na fronteira LLM↔tool; retry automático em falha
2. **Business validation** — handlers validam regras de negócio (saúde, orçamento, estoque, dados cadastrais); estado só é persistido se todos os gates passarem
3. **Structured output parsing** — `MemoryExtractionService` faz `safeParse()` do JSON do LLM antes de salvar memórias; `FlowResponseProcessor` valida formulários WhatsApp
4. **Contradiction detection** — `MemoryService` mantém consistência interna do estado antes de cada INSERT

A principal diferença do padrão ideal é que o mhc-backend **valida na execução das tools, não na geração de um JSON de recomendação completo**. Não existe um objeto `recommendation` com `confidence`, `reasoning` e `risk_flags`. Em vez disso, a validação é granular e distribuída: cada tool valida seu domínio específico antes de persistir. O texto narrativo da recomendação é gerado livremente pelo LLM e **não é validado estruturalmente**.

### Pontos fortes

- Zod em todas as 20+ tools garante type-safety na fronteira LLM↔código
- Pipeline de 8 gates no checkout com retomada (`checkoutSession`)
- Filtro de recomendações (`ProductRecommendationFilter`) usando estado persistido
- Detecção de contradições em memórias antes de salvar
- Extração automática de memórias com validação Zod (`MemoryExtractionService`)

### Pontos a melhorar

- Sem `confidence_score` — estado é binário (passou/não passou)
- `risk_flags` existem internamente mas não chegam ao LLM
- Sem audit trail de decisões
- `shownProducts` volátil (perde-se no restart)
- Router com branch `clarification` inalcançável
- `updateConversationStatus()` é no-op
