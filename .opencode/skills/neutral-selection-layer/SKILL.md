---
name: neutral-selection-layer
description: "Implementa uma camada de selecao de contexto model-agnostic e vendor-independent. Define um formato padronizado de contexto que qualquer modelo pode consumir, um Context Router que resolve queries de qualquer agente contra o grafo relacional e storage em tiers, e Vendor Adapters que traduzem o formato agnostico para o formato nativo de cada modelo. Transforma contexto no ativo mais duravel da organizacao — portavel entre modelos, sessoes, e provedores. Dispara com: 'neutral selection', 'model-agnostic context', 'vendor-independent context', 'context format standard', 'context router', 'multi-model context', 'portable context', 'cross-model context', 'camada neutra', 'contexto agnostico', 'formato de contexto', 'vendor adapter', 'neutral context layer', 'context portability', 'model migration context'."
license: MIT
compatibility: opencode
metadata:
  audience: agent-architects
  workflow: architecture
  priority: medium
  source: "Memory Selection Problem — Pattern 5: Neutral Selection Layer"
---

## What I Do

Eu implemento uma camada de selecao de contexto que desacopla o ativo mais duravel da organizacao — o contexto acumulado pelos agentes — de qualquer modelo, provedor, ou framework especifico. Em vez de soldar a estrategia de contexto a features de memoria de um vendor, eu forneco:

1. **Model-Agnostic Context Format** — schema padronizado para context units que qualquer modelo pode consumir. O contexto e armazenado nesse formato, nao no formato nativo de nenhum modelo.
2. **Context Router** — camada de resolucao que recebe queries de qualquer agente (independente do modelo que ele usa) e roteia para a estrategia de selecao apropriada (graph traversal, tier promotion, budgeted retrieval).
3. **Multi-Tenant Registry** — tracking de ownership: qual contexto pertence a qual agente, sessao, e modelo. Politicas de isolamento e compartilhamento.
4. **Vendor Adapters** — traduzem o formato agnostico para o formato nativo de cada modelo destino. Um adapter por modelo; o contexto de origem e sempre o mesmo.

O resultado: contexto como ativo organizacional portavel. Migrar de modelo A para B nao requer reindexacao de contexto. Multiplos agentes com modelos diferentes compartilham a mesma visao de contexto. O system-of-record que nenhum framework, app, ou lab consegue sustentar sozinho.

## When to Use Me

Carregue esta skill quando:

- A organizacao usa multiplos modelos (GPT, Claude, Gemini, DeepSeek) em diferentes agentes e precisa de coerencia cross-model
- Ha risco de vendor lock-in: a estrategia de contexto esta soldada a APIs especificas de um provedor (ex: Assistant API threads, Claude Projects)
- Voce preve migracao de modelo no futuro proximo e quer que o contexto sobreviva a transicao sem reindexacao
- Multiplos agentes, sessoes, ou times precisam compartilhar uma visao unificada de contexto organizacional
- O repositorio ja implementa [[docs/canonical/epistemic-memory-graph|Epistemic Memory Graph]] e [[docs/canonical/hybrid-context-stack|Hybrid Context Stack]] e voce quer adicionar vendor independence
- Voce esta projetando a arquitetura de contexto como um ativo de longo prazo (5+ anos), nao como um componente transiente da sessao atual
- O custo de reindexacao de contexto em uma migracao de modelo e proibitivo (meses de historico, terabytes de contexto)

Nao use quando:

- A organizacao usa um unico modelo e nao preve mudanca — o overhead da camada de abstracao nao se justifica
- O volume de contexto e pequeno e reindexacao em caso de migracao seria trivial (horas, nao semanas)
- A latencia adicional de atravessar a camada de selecao antes de chegar ao modelo e inaceitavel para o dominio (ex: trading de alta frequencia, roteamento de chamadas em tempo real)
- Voce esta em fase de prototipacao e a prioridade e velocidade, nao portabilidade — adie a camada neutra para quando houver contexto suficiente que justifique protege-lo
- O provedor oferece garantias contratuais de portabilidade e compatibilidade que tornam o vendor lock-in um risco aceitavel

## The Anti-Pattern

```
ANTI-PATTERN: Contexto soldado a APIs especificas de vendor.
O ativo mais duravel da organizacao e refem do roadmap de outro.

Cenario:
  1. O time constroi um sistema agentico usando exclusivamente a
     API de um provedor (ex: OpenAI Assistants API com threads,
     vector stores, e file search).
  2. Todo o contexto — 18 meses de sessoes de agente, decisoes,
     correcoes, aprendizados — reside no formato nativo do provedor.
     As queries de contexto usam a API proprietaria de retrieval.
  3. O provedor anuncia:
     a) Deprecacao da API atual em 12 meses.
     b) Nova API com formato de contexto incompativel.
     c) Aumento de preco de 3x para o tier de armazenamento.
  4. O time enfrenta um projeto de migracao de 6 meses: extrair
     contexto do formato proprietario, normalizar, reindexar no
     novo formato, validar que queries produzem resultados equivalentes.
  5. Durante a migracao, o sistema opera com contexto parcial —
     agentes tomam decisoes sem historico completo. A qualidade
     degrada. O time corre contra o clock da deprecacao.

Cenario alternativo (fragmentacao cross-model):
  1. O time adota um segundo modelo para tarefas especializadas
     (ex: Claude para raciocinio longo, GPT para acao rapida).
  2. Cada modelo usa seu proprio formato de contexto e storage.
     O agente Claude nao ve o contexto que o agente GPT acumulou.
  3. Decisoes tomadas por um agente sao invisiveis para o outro.
     O contexto organizacional se fragmenta em silos por modelo.
  4. Nao ha system-of-record unificado — cada modelo tem sua
     propria "verdade" sobre o estado do sistema.

Consequencia:
  - Contexto como passivo, nao como ativo: em vez de acumular valor
    ao longo do tempo, acumula custo de migracao
  - Vendor lock-in nao e so financeiro — e arquitetonico: a
    organizacao nao consegue trocar de modelo sem perder contexto
  - Fragmentacao cross-model impede aprendizado cross-agente:
    licoes aprendidas por um agente nunca beneficiam outros
```

## The Pattern

```
PATTERN: Camada de selecao neutra entre agentes/modelos e o
contexto armazenado. Formato agnostico como system-of-record;
adapters como boundary de traducao para cada modelo.

Arquitetura:

  ┌─────────────────────────────────────────────────────────────┐
  │                   NEUTRAL SELECTION LAYER                     │
  │                                                              │
  │  Agent A        Agent B        Agent C        Agent D       │
  │  (GPT-5)       (Claude 4)     (Gemini 3)    (DeepSeek V4)   │
  │     │              │              │              │           │
  │     ▼              ▼              ▼              ▼           │
  │  ┌──────────────────────────────────────────────────────┐   │
  │  │              CONTEXT ROUTER                           │   │
  │  │                                                      │   │
  │  │  Query: "context relevant to task X, step Y"          │   │
  │  │  Resolve: agent identity → permissions → strategy     │   │
  │  │                                                      │   │
  │  │  Strategies:                                          │   │
  │  │  ├─ Graph traversal (Relational Context Graph)        │   │
  │  │  ├─ Tier promotion (Tiered Context Storage)           │   │
  │  │  ├─ Budgeted retrieval (Selection-Budgeted Retrieval) │   │
  │  │  └─ Hybrid (combine above based on query type)        │   │
  │  └────────────────────┬─────────────────────────────────┘   │
  │                       │                                      │
  │                       ▼                                      │
  │  ┌──────────────────────────────────────────────────────┐   │
  │  │        MODEL-AGNOSTIC CONTEXT FORMAT                  │   │
  │  │                                                      │   │
  │  │  Schema:                                              │   │
  │  │  {                                                    │   │
  │  │    id: string            // stable identifier         │   │
  │  │    kind: ContextUnitKind // tool_result, decision,    │   │
  │  │                          // state_snapshot, note      │   │
  │  │    content: string       // plain text or markdown    │   │
  │  │    metadata: {                                       │   │
  │  │      timestamp: ISO8601                               │   │
  │  │      agent_id: string                                 │   │
  │  │      session_id: string                               │   │
  │  │      task_step: number                                │   │
  │  │      epistemic_status: "confirmed"|"tentative"|...   │   │
  │  │      provenance: string[]  // source trace            │   │
  │  │      relevance_score: number                          │   │
  │  │      tier: "hot"|"warm"|"cold"                        │   │
  │  │    }                                                  │   │
  │  │    relations: [{                                      │   │
  │  │      target_id: string                                │   │
  │  │      edge_type: "dependency"|"provenance"|            │   │
  │  │                  "supersession"|"causation"           │   │
  │  │    }]                                                 │   │
  │  │  }                                                    │   │
  │  └────────────────────┬─────────────────────────────────┘   │
  │                       │                                      │
  │                       ▼                                      │
  │  ┌──────────────────────────────────────────────────────┐   │
  │  │        MULTI-TENANT REGISTRY                          │   │
  │  │                                                      │   │
  │  │  Tracks:                                              │   │
  │  │  ├─ Context ownership (agent_id, session_id, model)   │   │
  │  │  ├─ Isolation policies (which agents share context)   │   │
  │  │  ├─ Access patterns (reads, writes per tenant)        │   │
  │  │  └─ Quota enforcement (storage, bandwidth per tenant) │   │
  │  └──────────────────────────────────────────────────────┘   │
  │                                                              │
  └─────────────────────────────────────────────────────────────┘
       │
       ▼
  ┌─────────────────────────────────────────────────────────────┐
  │                   VENDOR ADAPTERS                            │
  │                                                              │
  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
  │  │ GPT Adapter  │  │Claude Adapter│  │Gemini Adapter│  ...  │
  │  │              │  │              │  │              │       │
  │  │ Agnostic →   │  │ Agnostic →   │  │ Agnostic →   │       │
  │  │ Chat Complet.│  │ Messages API │  │ Generate API │       │
  │  └──────────────┘  └──────────────┘  └──────────────┘       │
  │                                                              │
  │  Each adapter:                                               │
  │  1. Recebe context units in model-agnostic format            │
  │  2. Mapeia para o formato nativo do modelo:                  │
  │     - System prompt vs. user message vs. tool result         │
  │     - Role mapping (system, user, assistant, tool)           │
  │     - Content format (text, multimodal, structured)          │
  │     - Tool definitions e function calling                    │
  │  3. Aplica ordenacao otimizada para o modelo (head/tail      │
  │     bias, capacity profile)                                  │
  │  4. Retorna contexto formatado + metadados de consumo        │
  └─────────────────────────────────────────────────────────────┘

Fluxo de uma query de contexto:

  1. Agent (qualquer modelo) emite query: "contexto relevante
     para a task X no passo Y, budget maximo Z tokens"

  2. Context Router resolve:
     a) Identity: qual agente/sessao/modelo esta query?
     b) Permissions: o que este agente pode acessar? (Registry)
     c) Strategy: qual estrategia de selecao?

  3. Strategy executa:
     - Graph traversal no [[docs/canonical/epistemic-memory-graph|
       Epistemic Memory Graph]] a partir do task node X
     - Tier promotion via [[docs/canonical/head-tail-context-truncation|
       Tiered Context Storage]] para candidatos em warm/cold
     - Budgeted retrieval se necessario (ranking cost/benefit)

  4. Context units selecionadas sao retornadas no formato agnostico

  5. Vendor Adapter do modelo destino traduz para formato nativo
     e otimiza ordenacao (head/tail bias do modelo)

  6. Contexto formatado e injetado no prompt do modelo
```

## Implementation Rules

### Model-Agnostic Context Format

O formato agnostico deve ser o system-of-record. NUNCA armazene contexto no formato nativo de um modelo como fonte primaria.

`ContextUnitKind` deve ser um enum fechado:
- `tool_result` — output de uma tool call
- `decision` — decisao tomada pelo agente
- `state_snapshot` — snapshot do estado do sistema em um ponto
- `progress_note` — nota de progresso, sumario, ou observacao
- `constraint` — restricao, preferencia, ou regra de negocio
- `correction` — correcao aplicada a um output anterior
- `observation` — observacao externa (feedback de usuario, metrica)

O campo `content` e sempre plain text ou markdown. NUNCA HTML, JSON aninhado, ou formatos binarios. Se o contexto original e binario (imagem, audio), armazene uma referencia + descricao textual no `content`.

### Context Router Rules

1. **Identity resolution e o primeiro passo.** Toda query de contexto deve ser autenticada (qual agente/sessao/modelo) antes de qualquer resolucao. O Multi-Tenant Registry responde: este agente pode acessar este contexto?

2. **Strategy selection por tipo de query.** O router deve selecionar a estrategia com base no tipo de query, nao em hardcoded paths:
   - "context around task X" → graph traversal
   - "recent context for session S" → tier promotion (warm→hot)
   - "find anything about topic T" → budgeted retrieval
   - "full context for step N" → hybrid (graph + tier + retrieval)

3. **Timeout e fallback por estrategia.** Se uma estrategia excede timeout (ex: graph traversal muito profundo), o router deve fazer fallback para uma estrategia mais simples (ex: tier promotion por recency) em vez de falhar a query inteira.

4. **Cache de queries frequentes.** Queries identicas (mesmo agente, task, step, budget) devem ser cacheadas por TTL curto (ex: 5 segundos) para evitar recomputacao quando multiplos componentes consultam o mesmo contexto.

### Vendor Adapter Rules

1. **Um adapter por modelo, nao por provider.** GPT-4 e GPT-5 podem compartilhar adapter se a API for compativel. Claude 3 e Claude 4 podem precisar de adapters diferentes se a API mudar.

2. **Ordenacao otimizada por modelo.** Cada adapter deve conhecer o perfil de atencao do modelo destino ([[docs/canonical/head-tail-context-truncation|head/tail bias]]) e posicionar os tokens mais importantes nas posicoes de maior atencao.

3. **Tool definitions sao parte do adapter.** O formato de tool definitions varia entre provedores. O adapter traduz tool definitions do formato agnostico para o formato nativo do modelo.

4. **Metadata de consumo.** Cada adapter deve reportar: quantos tokens o contexto formatado consumiu, quantos context units foram incluidas, e qual a taxa de compressao (tokens agnosticos vs. tokens nativos). Isso alimenta o [[docs/canonical/explicit-token-budget-ledger|Explicit Token Budget Ledger]].

5. **Adapter validation.** Todo adapter deve passar por um test suite que verifica: (a) todas as context units do formato agnostico estao representadas no formato nativo, (b) a ordenacao preserva a prioridade do relevance_score, (c) o token count reportado e acurado (±5%).

### Multi-Tenant Registry Rules

1. **Isolation por default.** Contexto de um agente/sessao e privado por default. Compartilhamento requer explicit opt-in (policy no registry).

2. **Cross-session sharing policies.** Defina quais tipos de contexto sao compartilhaveis entre sessoes: `decision` e `constraint` tipicamente sim; `tool_result` e `progress_note` tipicamente nao.

3. **Quota enforcement.** Cada tenant (agente, sessao, time) tem quota de storage e bandwidth. O registry rejeita writes que excederiam a quota.

## Integration with Existing Repo Infrastructure

A Neutral Selection Layer envolve a infraestrutura de contexto existente com uma camada de abstracao vendor-independent:

| Componente Existente | Como a Neutral Selection Layer complementa |
|---|---|
| [[docs/canonical/epistemic-memory-graph|Epistemic Memory Graph]] | O grafo opera no formato agnostico. A neutral layer garante que o grafo e populado e consultado independentemente do modelo que gerou o contexto. Nodes e edges sao agnosticos. |
| [[docs/canonical/hybrid-context-stack|Hybrid Context Stack]] | O context stack define camadas de contexto. A neutral layer garante que qualquer modelo pode consumir essas camadas — o stack e montado no formato agnostico e traduzido pelo adapter do modelo destino. |
| [[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation]] | O middle armazenado no catalog usa o formato agnostico. A neutral layer garante que o middle pode ser recuperado e injetado em qualquer modelo, nao apenas no modelo que o gerou. |
| [[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]] | Cada entrada do catalog referencia context units no formato agnostico. O catalog e o index; o formato agnostico e o conteudo indexado. |
| [[docs/canonical/explicit-token-budget-ledger|Explicit Token Budget Ledger]] | O budget ledger opera em tokens do formato agnostico. A neutral layer adiciona a traducao: tokens agnosticos → tokens nativos (via adapter metadata de consumo). |
| [[docs/canonical/llm-as-fuzzy-compiler|LLM as Fuzzy Compiler]] | O principio de "codigo como artefato de build descartavel" se estende ao contexto: contexto armazenado em formato agnostico e o source-of-truth; contexto formatado para um modelo especifico e o artefato de build descartavel. |
| [[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent OS]] | O OS escreve feedback no formato agnostico. A neutral layer garante que o feedback escrito por um modelo pode ser lido por qualquer outro modelo no loop. |
| [[docs/canonical/budget-aware-session-handoff|Budget-Aware Session Handoff]] | O handoff de sessao transfere contexto entre sessoes. A neutral layer garante que o contexto transferido e portavel: a proxima sessao pode usar um modelo diferente e ainda ler o contexto da sessao anterior. |

## Quality Gates

Antes de declarar a neutral selection layer como operacional, verifique:

- [ ] O Model-Agnostic Context Format esta definido com schema documentado (todos os campos de ContextUnit)
- [ ] `ContextUnitKind` e um enum fechado com os 7 tipos documentados e justificados
- [ ] NENHUM contexto e armazenado em formato nativo de vendor como fonte primaria
- [ ] O Context Router resolve queries com identity → permissions → strategy selection
- [ ] Pelo menos 2 estrategias de selecao estao implementadas e o router seleciona corretamente por tipo de query
- [ ] O Multi-Tenant Registry rastreia ownership (agent_id, session_id, model) para todas as context units
- [ ] Politicas de isolamento e compartilhamento estao documentadas e enforced pelo registry
- [ ] Pelo menos 2 Vendor Adapters estao implementados (para 2 modelos diferentes)
- [ ] Cada Vendor Adapter passa no test suite de validacao: todas as units representadas, ordenacao correta, token count acurado
- [ ] Metadata de consumo (tokens agnosticos → tokens nativos) e reportada por cada adapter
- [ ] O cache de queries frequentes esta implementado com TTL e invalidation
- [ ] Timeout e fallback por estrategia estao configurados: nenhuma query de contexto pode exceder 500ms sem fallback

## References

- [[docs/analysis/2026-06-18-memory-selection-problem/2026-06-18-memory-selection-problem-classification|Memory Selection Problem Classification]]:129-151 — classificado como Missing, 4 missing mechanics
- [[docs/analysis/2026-06-18-memory-selection-problem/2026-06-18-memory-selection-problem-patterns|Memory Selection Problem Patterns]]:199-245 — Pattern 5: Neutral Selection Layer (inputs, outputs, benefits, limitations, components, flow)
- [[docs/canonical/llm-as-fuzzy-compiler|LLM as Fuzzy Compiler]] — alinhamento filosofico: codigo descartavel, constraints duraveis
- [[docs/canonical/epistemic-memory-graph|Epistemic Memory Graph]] — grafo que a neutral layer consulta no formato agnostico
- [[docs/canonical/hybrid-context-stack|Hybrid Context Stack]] — stack de contexto que a neutral layer traduz para cada modelo
- [[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation]] — middle storage que a neutral layer torna portavel
- [[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]] — catalog que referencia unidades no formato agnostico
- [[docs/canonical/explicit-token-budget-ledger|Explicit Token Budget Ledger]] — budget ledger que a neutral layer estende com traducao de tokens
- [[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent OS]] — OS cujo feedback a neutral layer torna cross-model
- [[docs/canonical/budget-aware-session-handoff|Budget-Aware Session Handoff]] — handoff cujo contexto a neutral layer torna portavel entre modelos
- [[docs/analysis/2026-06-18-memory-selection-problem/2026-06-18-memory-selection-problem-classification|cross_pattern_dependencies]]:257-261 — Neutral Selection Layer wraps Relational Context Graph and Tiered Context Storage

---

*Created: 2026-06-18 | Source: Memory Selection Problem — Pattern 5 (Missing, Medium integration value)*
