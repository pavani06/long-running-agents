---
title: "Análise: Output Validation (Structured Generation) no mhc-backend"
type: analysis
date: 2026-05-28
domain: mhc-backend
aliases: []
tags: [analise, mhc-backend, diagnostico, validacao, structured-output, zod]
relates-to: ["[[docs/canonical/deterministic-tool-dispatch|Deterministic Tool Dispatch]]", "[[docs/analysis/mhc-backend/2026-05-28-output-validation-state-persistence|Output Validation Diagnostic]]"]
last_updated: 2026-06-10
---

# Análise: Output Validation (Structured Generation) no mhc-backend

**Data:** 2026-05-28
**Escopo:** Como o mhc-backend força respostas estruturadas do LLM e valida contra regras de negócio antes de agir

---

## Objetivo

Avaliar se o projeto implementa o padrão de "Output Validation" — forçar o modelo a responder em formato estruturado (JSON/Zod) com validação pós-geração contra constraints de negócio (orçamento, restrições alimentares, estoque, etc.).

---

## Arquitetura de validação: DynamicStructuredTool (LangChain)

O mhc-backend **não** usa geração de JSON raw + parsing manual. Em vez disso, usa o padrão `DynamicStructuredTool` do LangChain, onde cada tool declara um **schema Zod** que o framework usa para:

1. **Forçar o LLM a produzir argumentos tipados** — o modelo é obrigado a gerar um objeto que satisfaz o schema
2. **Validar na fronteira** — se o LLM produzir argumentos inválidos, o LangChain rejeita e força retry
3. **Garantir type-safety no handler** — o handler recebe objetos já validados pelo Zod

### Exemplo: AddToCartTool

```typescript
// Schema Zod — validado PELO FRAMEWORK antes do handler executar
schema: z.object({
  productId: z.string(),       // LLM DEVE passar string
  productName: z.string(),     // LLM DEVE passar string
  quantity: z.number().int(),  // LLM DEVE passar número inteiro
})
```

O LangChain intercepta chamadas onde o LLM produz `productId: 123` (número em vez de string) e força correção **antes** do handler rodar.

---

## Camadas de validação por ferramenta

### 1. SearchProductsTool — validação na busca + filtro pós-busca

**Arquivo:** `src/agents/graph/tools/ecommerce/SearchProductsTool.ts`

| Etapa | O que valida | Tipo |
|---|---|---|
| Zod schema | `query: string`, `brand?`, `category?`, `attributes?`, `userId: string` | Input |
| Handler: busca Pinecone | Produtos existem no catálogo | Runtime |
| Handler: `productRecommendationFilter.filterProducts()` | Restrições de saúde, alergias, orçamento | **Business** |
| Handler: diversificação por marca | `pickProductsPerBrand()` — até 2 por marca em busca category-only | Regra de UX |
| Handler: `updateShownProducts()` | Persiste mapeamento ID→Nome para referências ordinais | Estado |

**Ponto crítico de validação:**

```typescript
// Linha ~172 — filtro de onboarding APÓS busca
if (agentState.onboardingData?.isComplete) {
  const filtered = productRecommendationFilter.filterProducts(
    products,
    agentState.onboardingData,
  );
  products = filtered.allowed;
  // Se todos foram bloqueados → retorna erro
  if (products.length === 0) {
    return { success: false, message: "Todos produtos foram filtrados devido ao seu perfil..." };
  }
}
```

### 2. AddToCartTool — validação de estoque + idempotência

**Arquivo:** `src/agents/graph/tools/ecommerce/AddToCartTool.ts`

| Etapa | O que valida | Tipo |
|---|---|---|
| Zod schema | `productId: string`, `productName: string`, `quantity: number` | Input |
| Handler: `performAddToCart()` | `quantity <= 0` → erro | Input |
| Handler: `performAddToCart()` | `productId` é numérico (`/^\d+$/`) | Input |
| Handler: `ecommerceClient.getProduct()` | Produto existe no catálogo externo | Runtime |
| Handler: `newTotalQty > product.stock` | **Validação de estoque** → bloqueia com `availableStock` e `currentInCart` | **Business** |

```typescript
// Validação de estoque COM feedback detalhado
if (newTotalQty > product.stock) {
  return {
    success: false,
    error: `Estoque insuficiente. Disponível: ${product.stock}. Você já tem ${currentQty} no carrinho.`,
    availableStock: product.stock,
    currentInCart: currentQty,
  };
}
```

### 3. CreateOrderTool — validação completa de checkout

**Arquivo:** `src/agents/graph/tools/ecommerce/CreateOrderTool.ts`

Esta é a ferramenta com a validação mais extensa do sistema. Implementa um **pipeline sequencial de 8 gates**:

| Gate | O que valida | Consequência |
|---|---|---|
| 1. Carrinho vazio | `cart.items.length === 0` | Bloqueia com `isEmpty: true` |
| 2. Endereço | `!shippingAddress` | Bloqueia + salva `checkoutSession` para retomar |
| 3. Email real | `!user.emailReal` ou email do WhatsApp | Bloqueia + salva `checkoutSession` |
| 4. CPF | `!user.cpf` | Bloqueia + salva `checkoutSession` |
| 5. Nome completo | firstName/lastName ausentes ou "desconhecido" | Bloqueia + salva `checkoutSession` |
| 6. Autorização | `!agentState.authorization?.customerId` | Bloqueia |
| 7. Estoque por item | Cada item: `product.stock < item.quantity` | Bloqueia com detalhes do produto |
| 8. Frete | `!shipping` (cheapest/fastest) | Bloqueia, instrui LLM a chamar `calculate_shipping` |

**Mecanismo de retomada (`checkoutSession`):**

Quando um gate bloqueia, o estado é salvo para que o usuário não precise recomeçar:

```typescript
saveCheckoutSession(state, {
  missingCpf: !user?.cpf,
  missingEmail: isMissingEmail(user),
  missingName: isMissingFullName(user),
  missingAddress: !shippingAddress,
});
```

### 4. GetProductDetailsTool — validação de ID + estoque

**Arquivo:** `src/agents/graph/tools/ecommerce/GetProductDetailsTool.ts`

| Etapa | O que valida |
|---|---|
| ID inválido | `productId.includes("prod_12345")` — placeholder do LLM |
| Produto não encontrado | `ecommerceClient.getProduct()` retorna null |
| Estoque zerado | `product.stock <= 0` → bloqueia com `isInactive: true` |

### 5. CollectUserDataTool — normalização + persistência com validação

**Arquivo:** `src/agents/graph/tools/CollectUserDataTool.ts`

| Etapa | O que valida |
|---|---|
| Zod schema | Objeto parcial com 20+ campos tipados (`z.enum`, `z.literal(true)`, `z.email()`) |
| Handler: `mergeUserProfile()` | Normaliza campos (snake_case → camelCase, CPF → 11 dígitos) |
| Handler: `persistToDatabase()` | Valida CPF (11 dígitos), faz upsert seguro |

### 6. SaveMemoryTool — validação de categoria

**Arquivo:** `src/agents/graph/tools/memory/SaveMemoryTool.ts`

```typescript
schema: z.object({
  category: z.enum(["preferences", "dietary", "medical", "goals", "history", "routine"]),
  key: z.string(),
  value: z.string(),
  notes: z.string().optional(),
  expires_in_days: z.number().optional(),
})
```

O `z.enum` força o LLM a escolher uma das 6 categorias válidas. Qualquer outra string é rejeitada pelo framework.

---

## Camada central de business validation: ProductRecommendationFilter

**Arquivo:** `src/services/ecommerce/ProductRecommendationFilter.ts`

Este é o componente que mais se aproxima do padrão ideal de Output Validation com business rules. Ele é chamado **após** a busca de produtos, não após a recomendação.

### Pipeline de validação

```
filterProduct(product, onboardingData)
  │
  ├─ [1] checkHealthRestrictions()
  │     ├─ Alergias (SEVERO → BLOQUEIA)
  │     │   └─ Verifica nome, descrição, tags do produto
  │     │   └─ Respeita exceções "sem X", "X-free", "free de X"
  │     ├─ Restrições alimentares severas (BLOQUEIA)
  │     ├─ Restrições não-severas (AVISO apenas)
  │     └─ Condições diagnosticadas (AVISO contextual)
  │         ├─ Diabetes + açúcar → warning
  │         └─ Hipertensão + cafeína → warning
  │
  └─ [2] checkBudget()
        ├─ Mapeia categoria do produto → budget
        ├─ Preço > budget → BLOQUEIA
        └─ Preço >= 80% do budget → AVISO
```

### Tipos de resultado

```typescript
interface ProductFilterResult {
  allowed: boolean;   // Se produto passa em TODOS os filtros
  reason?: string;    // Razão de bloqueio (se allowed = false)
  warnings?: string[]; // Avisos contextuais (mesmo se allowed = true)
}
```

### Exemplo de bloqueio por alergia

```typescript
// Verifica nome, descrição E tags do produto
if (name.includes("lactose")) {
  const isFree = ["sem lactose", "lactose-free"].some(t => name.includes(t));
  if (!isFree) {
    return { allowed: false, reason: "Produto contém lactose, ao qual você é alérgico(a)" };
  }
}
```

### Validação adicional: dietary terms de memórias

```typescript
// Extrai termos de restrição das ConversationMemories
filterProductsByRestrictionTerms(products, ["lactose", "glúten", "vegano"])
```

Este método é usado para aplicar restrições extraídas das memórias semânticas (`ConversationMemory` com categoria `dietary`) como filtro adicional.

---

## Validação de entrada: restrictionValidators

**Arquivo:** `src/utils/restrictionValidators.ts`

Filtra respostas negativas que o usuário pode dar durante onboarding:

```typescript
isValidRestriction("lactose")   // true
isValidRestriction("não")       // false
isValidRestriction("nenhuma")   // false
isValidRestriction("sem")       // false
```

Usado em:
- `ProductRecommendationFilter.checkHealthRestrictions()` — filtra alergias inválidas
- `ProductRecommendationFilter.filterProductsByRestrictionTerms()` — filtra termos vazios

---

## O que NÃO existe (gaps vs padrão ideal)

Comparando com o padrão descrito (campos `recommendation`, `reasoning`, `alternatives`, `confidence`, `risk_flags`, `contradicts_previous_preferences`):

| Mecanismo | Existe? | Como é feito |
|---|---|---|
| Forçar formato estruturado | ✅ Sim | Zod schemas nos `DynamicStructuredTool` — validado pelo LangChain na fronteira |
| `recommendation` (qual produto) | ✅ Sim | O LLM escolhe qual tool chamar e com quais args → a tool executa |
| `reasoning` (por que) | ⚠️ Parcial | O LLM produz reasoning em linguagem natural na resposta ao usuário, mas não há campo estruturado para isso |
| `alternatives` | ⚠️ Parcial | `SearchProductsTool` retorna múltiplos produtos; o LLM decide quais apresentar. Não há campo dedicado |
| `confidence` (0-100%) | ❌ Ausente | Não há scoring de confiança em nenhuma tool ou resposta |
| `risk_flags` | ⚠️ Parcial | `ProductRecommendationFilter` gera `warnings[]` no backend, mas não expõe ao LLM como campo estruturado. As warnings são usadas apenas para filtrar/bloquear, não para o LLM contextualizar a resposta |
| `contradicts_previous_preferences` | ⚠️ Parcial | `MemoryService.deactivateContradictions()` detecta contradições entre memórias, mas não entre uma recomendação e preferências |
| Retry loop em falha de parsing | ✅ Sim | LangChain gerencia automaticamente — se o LLM produz args inválidos para o schema Zod, o framework força retry |
| Business validation pós-geração | ✅ Sim | `ProductRecommendationFilter`, validação de estoque no `AddToCartTool`, pipeline de 8 gates no `CreateOrderTool` |
| Fallback seguro em falha total | ⚠️ Parcial | `SearchProductsTool` retorna `success: false` com mensagem amigável. `CreateOrderTool` salva estado para retomar. Mas não há fallback automático para "recomendar produto seguro default" |

---

## Diagrama do fluxo de validação

```
Usuário: "quero um whey sem lactose até R$100"
  │
  ▼
LLM decide chamar search_products
  │
  ├─ LangChain valida args contra Zod schema ✓
  │   └─ query: "whey sem lactose"
  │   └─ category: "proteinas"
  │   └─ attributes: "sem-lactose"
  │
  ▼
SearchProductsTool handler
  │
  ├─ [1] Pinecone search → retorna N produtos
  │
  ├─ [2] productRecommendationFilter.filterProducts()
  │     ├─ checkHealthRestrictions() → bloqueia produtos COM lactose
  │     └─ checkBudget() → bloqueia produtos > R$100
  │
  ├─ [3] Se onboarding incompleto → pula filtro
  │
  ├─ [4] Se todos bloqueados → retorna erro
  │
  └─ [5] Retorna produtos allowed + mensagem guia para o LLM
  │
  ▼
LLM apresenta produtos ao usuário (texto livre)
  │
  ▼
Usuário: "quero o primeiro"
  │
  ▼
LLM decide chamar add_to_cart
  │
  ├─ LangChain valida args contra Zod schema ✓
  │
  ▼
AddToCartTool handler
  │
  ├─ Valida productId numérico
  ├─ Valida quantity > 0
  ├─ Valida estoque (newTotalQty <= product.stock)
  └─ Se OK → adiciona ao carrinho
```

---

## Resumo

| Aspecto | Avaliação |
|---|---|
| Structured input (Zod) | **Forte** — todas as 20+ tools têm schema Zod. LangChain valida na fronteira automaticamente |
| Business validation | **Forte** — `ProductRecommendationFilter` com alergias, budget, restrições. Pipeline de 8 gates no checkout |
| Confidence scoring | **Ausente** — não implementado |
| Risk flags para o LLM | **Parcial** — warnings existem no backend mas não são passadas como campo estruturado para o LLM contextualizar |
| Fallback seguro | **Adequado** — erros são comunicados ao LLM via `success: false` com mensagem, permitindo recuperação |
| Retry automático | **Forte** — LangChain gerencia retry em falha de schema Zod |

### Principal diferença do padrão ideal

O mhc-backend não gera uma "recomendação JSON completa" com confidence, reasoning e risk_flags. Em vez disso, ele:

1. **Delega a geração para tools tipadas** — cada tool tem input Zod e output estruturado
2. **Valida na execução, não na geração** — as business rules rodam no handler da tool, não num parser pós-LLM
3. **Confia no LLM para a narrativa** — o texto da recomendação é gerado livremente; apenas as ações (add_to_cart, create_order) são validadas

Isso é uma arquitetura válida e funcional para o domínio, mas não captura métricas de confiança nem expõe risk_flags ao LLM para que ele mesmo ajuste sua resposta.
