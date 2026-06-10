---
title: "Diagnóstico: Arquitetura KODA no `mhc-backend` vs. Padrões Nível 2"
type: analysis
date: 2026-05-26
domain: mhc-backend
aliases: []
tags: [analise, mhc-backend, diagnostico, nivel-2, padroes-praticos]
last_updated: 2026-06-10
---

# Diagnóstico: Arquitetura KODA no `mhc-backend` vs. Padrões Nível 2

**Data:** 2026-05-26
**Repositório analisado:** [`chatshop-io/mhc-backend`](https://github.com/chatshop-io/mhc-backend)
**Referência curricular:** [`nivel-2-koda.md`](https://github.com/pavani06/long-running-agents/blob/main/curriculum/02-nivel-2-practical-patterns/koda-applications/nivel-2-koda.md)
**Stack:** Express.js 4.18, TypeScript 5.3, Prisma 5.7 (PostgreSQL 16), LangGraph, LangChain + OpenAI (gpt-4o-mini / gpt-5-mini), Pinecone, Redis 7, Trigger.dev 4.3

---

## Visão Geral

O `mhc-backend` é o motor conversacional da MHC — uma plataforma WhatsApp de coaching de saúde + e-commerce de suplementos. O agente de e-commerce é chamado **KODA** no próprio código (`OrchestratorAgent.ts:234`: _"Aqui é o KODA agente da MHC"_). A arquitetura usa **LangGraph** (StateGraph) para orquestrar 3 agentes especializados (`coach`, `ecommerce`, `voturuna`), com PostgreSQL + Redis como infraestrutura de estado.

O Nível 1 (fundamentos) já está implementado de forma madura. Este diagnóstico avalia a presença e maturidade dos **4 padrões do Nível 2** (Generator/Evaluator, Sprint Contracts, Rubric Design, Trace Reading) na implementação real.

### Diagrama de Arquitetura (Fluxo de Mensagem)

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
        │     └── 15+ queries paralelas com StageTimings
        │
        ▼
  buildAgentsGraph() — LangGraph StateGraph
        │
        ├── [1 agente ativo] → salta router, conecta direto (~800ms saving)
        │
        └── [2+ agentes ativos]
              ├── START → routerNode (gpt-4.1-mini)
              │     └── classifica: "ecommerce" | "coach" | "voturuna"
              │
              ├── ecommerceAgenteNode (KODA)
              │     ├── createAgent() com 20+ DynamicStructuredTools
              │     ├── systemPrompt: persona + global rules + ecommercePrompt (1800+ linhas)
              │     ├── contexto dinâmico: onboarding, memories, checkout, shownProducts
              │     ├── detecção de carrinho stale (sessão anterior)
              │     ├── detecção de resposta em inglês → rewrite PT-BR
              │     └── AIMessage final
              │
              ├── coachAgenteNode
              └── voturunaAgenteNode
        │
        ▼
  orquestrator_turn_trace (JSON log com StageTimings)
  memoryExtractionService.extractAndSave() (background, async)
```

---

## Arquivos-Chave da Arquitetura KODA

| Arquivo | Função |
|---------|--------|
| `src/agents/orchastrator/OrchestratorAgent.ts` | Entry point — monta estado, invoca grafo, extrai resposta |
| `src/agents/orchastrator/ConversationStateBuilder.ts` | Constrói AgentState com 15+ queries paralelas + cache Redis |
| `src/agents/agentsGraph.ts` | Monta StateGraph LangGraph com router condicional |
| `src/agents/graph/state.ts` | Define GraphState (Annotation.Root) — messages, route, agentState |
| `src/agents/graph/nodes/ecommerceAgenteNode.ts` | Nó KODA — 20+ tools, system prompt, detecção de carrinho/idioma |
| `src/agents/graph/nodes/routerNode.ts` | Classificador gpt-4.1-mini com structured output estrito |
| `src/agents/prompts/ecommerce/index.ts` | Prompt de e-commerce — 1800+ linhas de regras de negócio |
| `src/agents/prompts/persona/ecommerce.ts` | Persona "Votu" — tom, escopo, regras de comportamento |
| `src/agents/prompts/global/` | Regras globais: personality, rules, memory, onboarding |
| `src/agents/graph/tools/ecommerce/` | 20 tools: search, cart, order, shipping, tracking, reorder |
| `src/services/ecommerce/ProductRecommendationFilter.ts` | Filtro de produtos baseado em onboarding data |
| `src/utils/timing.ts` | `StageTimings` + `measureAsyncStage` para trace de performance |
| `src/services/memory/MemoryService.ts` | Memória semântica do usuário (save, recall, forget, extract) |
| `src/config/agents.ts` | Registro de agentes + configuração de roteamento |

---

## Padrão 1: Generator/Evaluator

### Status: PARCIALMENTE PRESENTE (25% de maturidade)

### O que existe

**Diversificação de opções no SearchProductsTool:**
O `SearchProductsTool` (`src/agents/graph/tools/ecommerce/SearchProductsTool.ts`) implementa `pickProductsPerBrand()`: em buscas por categoria sem marca especificada, pega até 2 produtos de cada marca distinta, intercalando rounds para garantir diversidade nas primeiras posições. Isso é uma forma primitiva de "gerar opções diversas".

```typescript
// SearchProductsTool.ts — diversificação por marca
function pickProductsPerBrand(products: Product[], perBrand: number): Product[] {
  const groups = new Map<string, Product[]>();
  for (const product of products) {
    const key = getBrandKey(product);
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key)!.push(product);
  }
  // Intercala rounds: 1º produto de cada marca, depois 2º, etc.
  for (let round = 0; round < perBrand; round++) {
    for (const brandKey of brandOrder) {
      if (productsForBrand.length > round) result.push(productsForBrand[round]);
    }
  }
  return result;
}
```

**Filtro como "Evaluator" binário:**
O `ProductRecommendationFilter` (`src/services/ecommerce/ProductRecommendationFilter.ts`) filtra produtos com base em onboarding data (budget, restrições alimentares, condições de saúde). Resultado: `allowed` ou `blocked`.

**Seleção implícita pelo LLM:**
O prompt instrui o modelo a _"destacar 1 opção principal, explicar brevemente por que ela se encaixa, fazer pergunta de decisão simples"_. A escolha é feita pelo próprio LLM, sem scoring intermediário.

### O que falta

| Elemento Nível 2 | Estado atual | Gap |
|------------------|-------------|-----|
| Gerar 5+ opções distintas | Diversificação por marca (até 2/marca) | Não gera opções com trade-offs explícitos (premium vs budget vs vegan) |
| Evaluator com scoring 0-100 | Filtro binário (allowed/blocked) | Sem scoring multi-dimensional ponderado |
| Temperature diferenciada (gen=1.0, eval=0.2) | Mesma chamada gera e seleciona | Sem separação de fases criativa/rigorosa |
| Top-3 com scores para o cliente | Apenas 1 opção principal | Cliente não vê alternativas com trade-offs |
| Breakdown de critérios por opção | Inexistente | Não se sabe qual dimensão elevou/baixou cada opção |

### Recomendação

Separar o fluxo em duas chamadas LLM: uma de **geração** (temperature alta, pedindo 5 opções distintas com justificativa) e uma de **avaliação** (temperature baixa, aplicando rubrica de 4 dimensões com scores 0-100). Apresentar top-3 ao usuário com scores e justificativas curtas.

---

## Padrão 2: Sprint Contracts

### Status: PRESENTE (65% de maturidade)

### O que existe

**Contratos de input/output via Zod:**
Cada uma das 20+ tools define schema Zod rigoroso para input e retorna estrutura tipada. Exemplo do `search_products`:

```typescript
// Input contract
schema: z.object({
  query: z.string(),
  brand: z.string().optional(),
  category: z.string().optional(),
  attributes: z.string().optional(),
  userId: z.string(),
})

// Output contract (implícito no return type)
{ success: boolean, products_found: number, products: Array<{...}>, message: string }
```

**Contrato de roteamento estrito:**
O `routerNode` (`src/agents/graph/nodes/routerNode.ts`) usa `withStructuredOutput` com `strict: true` — a saída é garantidamente `{route: "coach"|"ecommerce"|"voturuna"}`.

**Contrato de estado via LangGraph:**
`GraphState` (`src/agents/graph/state.ts`) define o schema que trafega entre nós do grafo:

```typescript
export const GraphState = Annotation.Root({
  messages: Annotation<BaseMessage[], BaseMessageLike[]>({ reducer: messagesStateReducer }),
  userId: Annotation<string>(),
  route: Annotation<"coach" | "ecommerce" | "voturuna">(),
  agentState: Annotation<AgentState>(),
  conversationStateBuilder: Annotation<ConversationStateBuilder>(),
  channelContext: Annotation<ChannelContext>(),
});
```

**Separação tool ↔ business logic:**
Tools contêm apenas a definição `DynamicStructuredTool`; toda lógica de negócio reside em `src/services/` — conforme AGENTS.md: _"Tool files contain only the tool definition; business logic goes in src/services/"_.

### O que falta

| Elemento Nível 2 | Estado atual | Gap |
|------------------|-------------|-----|
| Promessa explícita documentada | Schema Zod (implícito no código) | Sem documentação de "o que este módulo promete entregar" |
| Validação pós-execução | Tipagem TypeScript em compile-time | Sem runtime check de que o output corresponde ao prometido |
| Alerta de contrato quebrado | Falhas silenciosas (ex: getAthleteProfile → null) | Se uma query falha, o agente segue com dados parciais |
| Contratos entre módulos do StateBuilder | 15+ queries paralelas sem orquestração de falhas | Não há garantia de consistência cross-query |

### Recomendação

Adicionar validação de runtime pós-execução nas tools usando `schema.parse()` no output. Para o StateBuilder, implementar um `StateContract` que verifica integridade mínima antes de invocar o grafo (ex: "se cart não está vazio, user deve ter shippingAddress ou estar em modo coleta de dados"). Documentar contratos em comentários JSDoc no topo de cada tool e módulo.

---

## Padrão 3: Rubric Design

### Status: AUSENTE (10% de maturidade)

### O que existe

**Filtro binário de onboarding:**
O `ProductRecommendationFilter` aplica regras booleanas: produto está dentro do budget? Não contém ingredientes restritos? Resultado: `allowed` ou `blocked`.

**Regras de qualidade no prompt:**
O prompt de e-commerce (1800+ linhas) define regras como "não inventar dados nutricionais", "não usar preço de referência", "destacar 1 opção principal". Mas são regras de conformidade, não de avaliação de qualidade.

### O que falta

| Elemento Nível 2 | Estado atual | Gap |
|------------------|-------------|-----|
| Rubrica multi-dimensional (4+ dims) | Filtro binário (1 dimensão: passa/não passa) | Sem dimensões como adequação, custo-benefício, satisfação, viabilidade |
| Pesos por dimensão | Inexistente | Sem ponderação da importância relativa |
| Score 0-100 por recomendação | Inexistente | Sem métrica contínua de qualidade |
| Threshold configurável para rejeição | Inexistente | Não é possível rejeitar recomendações "válidas mas medíocres" |
| Breakdown de score visível | Inexistente | Debugging de qualidade é impossível |

### Proposta de Rubrica para KODA

```
RUBRIC PARA RECOMENDAÇÃO DE SUPLEMENTO:

DIMENSÃO 1: Adequação ao Perfil (peso 30%)
  5 pontos: Perfil atlético + onboarding batem perfeitamente
  3 pontos: Atende parcialmente (ex: esporte OK, mas preferência de sabor não)
  1 ponto:  Marginalmente compatível

DIMENSÃO 2: Custo-Benefício (peso 25%)
  5 pontos: Menor preço por dose na categoria, dentro do budget
  3 pontos: Preço médio, custo-benefício aceitável
  1 ponto:  Caro para o que entrega ou próximo do limite do budget

DIMENSÃO 3: Satisfação Esperada (peso 25%)
  5 pontos: Produto com alta recorrência de compra e zero reclamações
  3 pontos: Boa aceitação, algumas ressalvas
  1 ponto:  Histórico de insatisfação ou reclamações frequentes

DIMENSÃO 4: Viabilidade Operacional (peso 20%)
  5 pontos: Em estoque, frete disponível, entrega rápida
  3 pontos: Em estoque, mas frete longo ou dados de checkout incompletos
  1 ponto:  Estoque baixo, frete indisponível ou dados críticos faltando

SCORE TOTAL = Σ (score_dimensão × peso) × 20  →  escala 0-100
THRESHOLD: recomendar se ≥ 75; sugerir alternativas se < 75
```

### Recomendação

Implementar rubrica como uma tool separada (`evaluate_recommendation`) que o agente chama ANTES de apresentar ao usuário. A tool recebe o produto candidato + perfil do usuário, retorna score com breakdown. O prompt instrui o modelo a só recomendar se score ≥ 75 e a mostrar alternativas quando abaixo.

---

## Padrão 4: Trace Reading

### Status: PRESENTE (50% de maturidade)

### O que existe

**Trace operacional por turno:**
O `OrchestratorAgent.processMessage()` emite `orchestrator_turn_trace` com:

```json
{
  "userId": "...",
  "channel": "whatsapp",
  "route": "ecommerce",
  "history_message_count": 45,
  "initial_message_count": 47,
  "side_effect_count": 0,
  "turn_total_ms": 2340,
  "timings": {
    "build_state_ms": 412,
    "build_history_messages_ms": 3,
    "graph_build_ms": 1,
    "graph_invoke_ms": 1890,
    "extract_response_ms": 5
  }
}
```

**Trace de construção de estado:**
O `ConversationStateBuilder.buildState()` emite `state_build_trace` com:

```json
{
  "userId": "...",
  "cart_item_count": 2,
  "conversation_history_count": 60,
  "shown_products_count": 5,
  "profile_cache_hit": true,
  "turn_total_ms": 412,
  "timings": {
    "active_cart_ms": 45,
    "conversation_history_ms": 120,
    "memories_ms": 89,
    "recent_orders_ms": 34,
    "product_context_ms": 67
  }
}
```

**Tracking de buscas para analytics:**
O `SearchProductsTool` persiste mensagens de tracking no banco com query, resultados, success/failure — permitindo análise de qualidade de busca.

**StageTimings reutilizável:**
O utilitário `src/utils/timing.ts` fornece `measureAsyncStage()` que mede qualquer etapa assíncrona e popula `StageTimings`.

**Logger estruturado:**
Winston com output JSON, permitindo parsing e agregação em ferramentas de observabilidade.

### O que falta

| Elemento Nível 2 | Estado atual | Gap |
|------------------|-------------|-----|
| Trace de raciocínio do LLM | Inexistente | Não se sabe qual chain-of-thought levou à decisão |
| Log de tool calls com argumentos | Parcial (logs de info, não estruturado) | Não é possível reconstruir quais tools foram chamadas e com quais parâmetros |
| Replay de decisão | Inexistente | Impossível reproduzir exatamente o que ocorreu em um turno específico |
| Diagnóstico de "por que X e não Y" | Inexistente | Sabe-se o resultado, não a causa |
| Trace de rewrite PT-BR | Inexistente | Se `ensurePortuguese` reescreveu, o conteúdo original se perde |

### Recomendação

1. Adicionar `tool_call_trace`: log estruturado de cada tool invocation com `{toolName, args, result, durationMs}`
2. Persistir `messages` completos do LangGraph (incluindo tool calls e tool results) por turno em storage dedicado (Redis ou MongoDB) com TTL de 7 dias
3. Instrumentar o `ensurePortuguese` para logar `{originalLanguage, originalContent, rewrittenContent}` quando reescrever
4. Criar endpoint de debug `/admin/traces/:userId/:turnId` que retorna o trace completo de um turno para diagnóstico

---

## Padrões Adicionais (Além do Nível 2)

O time do mhc-backend implementou otimizações de produção que o currículo Nível 2 não cobre, mas que representam práticas avançadas:

| Padrão | Arquivo | Descrição | Impacto |
|--------|---------|-----------|---------|
| **Profile Cache** | `ConversationStateBuilder.ts:65-68` | Redis TTL 3min para dados estáticos de perfil | Reduz ~8 queries DB por turno |
| **Single-Agent Fast Path** | `agentsGraph.ts:39-47` | Quando 1 agente ativo, pula routerNode | Economiza ~800ms + 1 LLM call |
| **Debounced Message Batching** | `OrchestratorAgent.ts:175-361` | `processMessageBatch` agrupa mensagens rápidas | Evita N chamadas ao grafo |
| **Stale Cart Detection** | `ecommerceAgenteNode.ts:45-79` | Detecta carrinho de sessão anterior (gap > 1h) | Evita compras acidentais |
| **Language Guard** | `ecommerceAgenteNode.ts:94-165` | Detecta resposta em inglês, reescreve em PT-BR | Consistência de idioma |
| **Background Memory Extraction** | `OrchestratorAgent.ts:107-111` | Extrai memórias async pós-turno (non-blocking) | Zero latência adicional |
| **Channel Abstraction** | `OrchestratorAgent.ts:83-86` | SideEffects abstraem WhatsApp CTA vs API JSON | Mesmo agente serve 2 canais |
| **Anti-Spam Gate** | `src/services/proactive/anti-spam.ts` | Filtro de mensagens proativas | Segurança de UX |
| **Fast-Path Intent Router** | `src/services/chat/FastPathRouter.ts` | Classificador determinístico para intenções triviais | Respostas < 50ms sem LLM |
| **Error Trace** | `OrchestratorAgent.ts:152` | `orchestrator_turn_trace_error` com timings parciais | Diagnóstico de falhas |

---

## Matriz de Maturidade: Nível 1 → Nível 2

```
Nível 1 (Fundação)       ████████████████████ 100%
  ├─ Context Management      ████████████████████  Conversação multi-turn com 60 msgs
  ├─ Token Budgeting         ████████████████████  Compressão de histórico, historyLimit
  ├─ State Persistence       ████████████████████  PostgreSQL + Redis + Prisma
  └─ Basic Harness           ████████████████████  Zod validation, error middleware

Nível 2 (Visibilidade)    ████████░░░░░░░░░░░░  45%
  ├─ Generator/Evaluator     ████░░░░░░  25%  Diversificação + filtro, sem scoring
  ├─ Sprint Contracts        ████████░░  65%  Zod schemas + LangGraph, sem validação
  ├─ Rubric Design           ██░░░░░░░░  10%  Filtro binário apenas
  └─ Trace Reading           ██████░░░░  50%  Operacional (timing), não diagnóstico

Maturidade Geral Nível 2: ████████░░░░░░░░░░░░  45%
```

---

## Caminho para Nível 2 Completo

### Ordem recomendada de implementação

1. **Rubric Design** (menor esforço, maior impacto)
   - Criar `evaluate_recommendation` tool com scoring 4 dimensões
   - Menos de 200 linhas de código novo
   - Impacto imediato na qualidade percebida das recomendações

2. **Generator/Evaluator** (médio esforço, alto impacto)
   - Separar fluxo em duas chamadas LLM com temperatures distintas
   - Reusar a rubrica do passo 1 como critério de avaliação
   - Apresentar top-3 ao usuário

3. **Trace Reading diagnóstico** (médio esforço, habilita melhoria contínua)
   - Adicionar `tool_call_trace` estruturado
   - Persistir mensagens completas por turno
   - Criar endpoint de debug para replay

4. **Sprint Contracts com validação** (médio esforço, reduz bugs silenciosos)
   - Adicionar runtime validation no output das tools
   - Implementar `StateContract` para integridade mínima antes do grafo
   - Documentar contratos em JSDoc

### Estimativa de impacto

| Fase | Acurácia esperada | Custo adicional |
|------|-------------------|-----------------|
| Atual (N1 + 45% N2) | ~70% | Baseline |
| + Rubric Design | ~78% | +1 LLM call leve (eval tool) |
| + Generator/Evaluator | ~85% | +1 LLM call pesada (gen) |
| + Trace Reading | ~87% (*) | Custo de storage |
| + Sprint Validation | ~87% | Overhead desprezível |

_(*) Trace Reading não melhora acurácia diretamente, mas acelera debugging, permitindo iterações mais rápidas de melhoria._

---

## Observações

- O time já opera com disciplina de engenharia elevada: Zod validation, logging estruturado, cache multi-camada, separação de concerns, métricas de performance. A fundação para os padrões do Nível 2 está pronta.
- O prompt de e-commerce com 1800+ linhas sugere que regras de qualidade estão sendo codificadas em linguagem natural no prompt em vez de em ferramentas estruturadas (rubrics). Migrar gradualmente do prompt para tools de avaliação reduziria o tamanho do prompt e aumentaria a previsibilidade.
- A presença de `console.log` no `routerNode.ts:223` viola o próprio AGENTS.md ("No console.log — use logger"). São 43 ocorrências conhecidas no código.
- O `OrchestratorAgent` tem um bug de nomenclatura: a classe se chama `OrchestratorAgent` (sem 's' depois do 'r'), o arquivo `OrchestratorAgent.ts` (com 's') e o diretório `orchastrator/` (com 's' mas faltando 'e'). A inconsistência não causa erro de runtime mas dificulta navegação.
