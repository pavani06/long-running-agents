---
name: tiered-context-storage
description: "Implementa armazenamento de contexto em tres tiers (hot/warm/cold) com promocao e democao baseadas em relevancia. Mantem o conjunto de trabalho ativo deliberadamente pequeno na hot tier (cache in-memory), move contexto recentemente relevante para warm tier (NVMe, baixa latencia), e arquiva historico completo na cold tier (object storage, alta latencia). O Tier Orchestrator executa transicoes baseadas em scores de relevancia e prefetch preditivo antes de cada passo de raciocinio. Previne context rot (cada token acumulado degrada qualidade do passo seguinte) e separa preocupacao de armazenamento de preocupacao de selecao. Dispara com: 'tiered context', 'tier storage', 'context tiers', 'hot warm cold', 'tiered storage', 'context promotion', 'context demotion', 'tier orchestrator', 'promocao de contexto', 'democao de contexto', 'armazenamento em tiers', 'tiered context storage', 'context tier management'."
license: MIT
compatibility: opencode
metadata:
  audience: agent-implementers
  workflow: implementation
  priority: medium
  source: "Memory Selection Problem — Pattern 3: Tiered Context Storage with Promotion/Demotion"
---

## What I Do

Eu implemento um sistema de armazenamento de contexto em tres tiers com transicoes dinamicas baseadas em relevancia. Em vez de manter todo o contexto na memoria ativa (insustentavel) ou todo em cold storage (inutil quando o modelo precisa raciocinar), eu movimento contexto entre tiers conforme a necessidade de cada passo.

1. **Hot Tier (in-memory cache)** — contem APENAS o conjunto de trabalho ativo atual. Sub-millisecond latency. O que o modelo esta raciocinando agora. Deliberadamente pequeno.
2. **Warm Tier (NVMe-backed store)** — contexto recentemente relevante, acessivel com baixa latencia (~1ms). Buffer entre hot e cold: itens que acabaram de sair do foco mas podem voltar.
3. **Cold Tier (object storage)** — historico completo, acessivel com alta latencia (~100ms). Tudo que o agente ja gerou. Recuperacao sob demanda quando necessario.

A camada de decisao (Tier Orchestrator) e o gate entre o modelo e tudo que ele poderia saber: decide o que promover (cold→warm→hot), o que demover (hot→warm→cold), e o que prefetch antes do proximo passo.

## When to Use Me

Carregue esta skill quando:

- O agente opera em sessoes longas e o contexto ativo cresce ate degradar a qualidade dos passos (context rot)
- Voce precisa de uma separacao explicita entre "onde os dados vivem" (tiers de armazenamento) e "o que o modelo atende" (conjunto de trabalho ativo)
- O sistema precisa escalar linearmente com volume de historico, sem que o custo de armazenamento domine
- Ha padroes de acesso previsiveis: contexto acessado em rajadas (passo atual) e depois raramente referenciado
- Voce ja tem infraestrutura de token budget ([[docs/canonical/explicit-token-budget-ledger|Explicit Token Budget Ledger]]) e quer adicionar gerenciamento de tiers
- O repositorio implementa [[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation]] e voce quer evoluir para um modelo de tres tiers com transicoes dinamicas
- Voce precisa que contexto descartado seja recuperavel sem reexecutar passos anteriores

Nao use quando:

- As sessoes do agente sao curtas (poucos passos) e o contexto ativo nunca excede o orcamento — o overhead de gerenciamento de tiers nao se justifica
- O contexto e estritamente linear e recency-based (sempre o mais recente importa, nunca o antigo) — use apenas truncation simples
- Nao ha infraestrutura para storage com diferentes caracteristicas de latencia (NVMe, object storage) — o modelo de tres tiers pressupoe essas capacidades
- A latencia de cold→hot promotion (obrigatoria se o modelo precisar de contexto arquivado) e proibitiva para o dominio — considere prefetch mais agressivo ou warm tier maior

## The Anti-Pattern

```
ANTI-PATTERN: Modelo binario de dois tiers sem transicoes dinamicas.
Contexto e "ativo" (na janela) ou "morto" (descartado para sempre).

Cenario:
  1. O sistema implementa head-tail-context-truncation: head (prompt
     estavel + passos recentes), tail (ultimos resultados), middle
     (resto do historico) movido para external storage.
  2. Quando o middle e movido, ele vai para um bucket unico e indiferenciado.
     Nao ha distincao entre "isso foi relevante ha 3 passos" e "isso
     nunca foi relevante". Tudo no mesmo bucket.
  3. Quando o modelo precisa de contexto do middle, o sistema faz
     retrieval do bucket unico. Sem priorizacao, sem prefetch, sem
     latencia diferenciada.
  4. Contexto que era relevante ha 2 passos (e provavelmente ainda e)
     tem a mesma latencia de acesso que contexto de 200 passos atras.
  5. O sistema trata armazenamento como problema binario (dentro/fora)
     em vez de um espectro de relevancia com gradiente de acesso.

Consequencia:
  - Sem warm tier, contexto recentemente relevante sofre a mesma
    penalidade de latencia que contexto obsoleto
  - Sem promocao/democao, o sistema nao aprende padroes de acesso:
    itens frequentemente acessados nunca sao promovidos para tiers
    mais rapidos
  - Sem prefetch, o modelo espera ~100ms por contexto que poderia
    estar disponivel em ~1ms se tivesse sido antecipado
  - O modelo binario forc(a o trade-off falso: ou tudo na memoria
    (custo de tokens) ou tudo em cold storage (custo de latencia)
```

## The Pattern

```
PATTERN: Tres tiers de armazenamento com orquestrador de transicoes
baseadas em relevancia e prefetch preditivo.

Arquitetura:

  ┌─────────────────────────────────────────────────────────────┐
  │                    TIER ORCHESTRATOR                          │
  │                                                              │
  │  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐   │
  │  │   HOT TIER   │◄──►│  WARM TIER   │◄──►│  COLD TIER   │   │
  │  │              │    │              │    │              │   │
  │  │ In-Memory    │    │ NVMe-backed  │    │ Object Store │   │
  │  │ <1ms latency │    │ ~1ms latency │    │ ~100ms lat.  │   │
  │  │              │    │              │    │              │   │
  │  │ Active       │    │ Recently     │    │ Complete     │   │
  │  │ working set  │    │ relevant     │    │ history      │   │
  │  │ (small)      │    │ context      │    │ archive      │   │
  │  └──────────────┘    └──────────────┘    └──────────────┘   │
  │       ▲                    ▲                    ▲            │
  │       │    PROMOTE         │    PROMOTE         │            │
  │       │    (prefetch)      │    (on-demand)     │            │
  │       │                    │                    │            │
  │       ▼    DEMOTE          ▼    DEMOTE          │            │
  │       │    (step end)      │    (aging)         │            │
  │                                                              │
  │  Decision Signals:                                           │
  │  ├─ Relevance score (from Relational Context Graph)          │
  │  ├─ Recency (time since last access)                        │
  │  ├─ Access pattern (frequency, burstiness)                   │
  │  ├─ Prefetch prediction (graph traversal for next step)      │
  │  └─ Token budget remaining                                  │
  └─────────────────────────────────────────────────────────────┘

Fluxo de operacao por passo:

  STEP N EXECUTING (modelo raciocina com hot tier)
       │
       ▼
  ┌─────────────────────────────────────────────────────────────┐
  │ 1. DEMOTION (pos-step)                                       │
  │                                                              │
  │ Para cada context unit no hot tier apos o passo:             │
  │   - Calcule continued_relevance_score (graph distance do     │
  │     proximo passo previsto)                                  │
  │   - Se score < HOT_THRESHOLD:                                │
  │       - Se foi acessado nos ultimos K passos → hot → warm   │
  │       - Se nao foi acessado nos ultimos K passos → hot→cold │
  │   - Se score >= HOT_THRESHOLD: permanece no hot tier        │
  └─────────────────────────────────────────────────────────────┘
       │
       ▼
  ┌─────────────────────────────────────────────────────────────┐
  │ 2. AGING (warm tier maintenance)                             │
  │                                                              │
  │ Periodicamente (ex: a cada N passos ou quando warm tier      │
  │ atinge capacity threshold):                                  │
  │   - Para cada context unit no warm tier:                     │
  │       - Se time_since_last_access > WARM_TTL:                │
  │           warm → cold                                        │
  │       - Se access_count == 0 desde que entrou no warm:       │
  │           warm → cold (nunca foi usado, nao merece NVMe)    │
  └─────────────────────────────────────────────────────────────┘
       │
       ▼
  ┌─────────────────────────────────────────────────────────────┐
  │ 3. PREFETCH (pre-step N+1)                                   │
  │                                                              │
  │ Antes do proximo passo:                                      │
  │   - Traverse [[docs/canonical/epistemic-memory-graph|        │
  │     Epistemic Memory Graph]] a partir do task node           │
  │     para prever quais context units serao necessarias        │
  │   - Para cada predicted unit em warm ou cold:                │
  │       - Se relevance_score > PREFETCH_THRESHOLD:             │
  │           cold → warm (se em cold)                           │
  │           warm → hot (se em warm)                            │
  │       - Se relevance_score marginal:                         │
  │           cold → warm (prefetch conservador, sem hot)        │
  │   - Verifique tamanho do hot tier contra token budget        │
  │   - Se hot tier excede budget, demova lowest-score units    │
  └─────────────────────────────────────────────────────────────┘
       │
       ▼
  STEP N+1 EXECUTING (modelo raciocina com hot tier atualizado)
```

## Implementation Rules

### Tier Capacity Rules

| Tier | Capacidade Tipica | Politica de Eviccao |
|---|---|---|
| Hot | ~10-20% do token budget do passo | Democao por relevance score (menos relevante sai primeiro) |
| Warm | 5-10x hot tier (NVMe e barato) | Aging por TTL + access count (nunca acessado → cold) |
| Cold | Ilimitado (object storage) | Nenhuma — cold tier e o arquivo permanente |

### Relevance Scoring para Transicoes

```
relevance_score(unit, next_step) =
    graph_distance(unit, next_step_node)  // inversamente proporcional
  × recency_factor(time_since_last_access)
  × access_frequency_factor(times_accessed / total_steps)

Onde:
  - graph_distance: passos no grafo relacional entre a unit e o task node
  - recency_factor: e^(-λ × time_since_access), decaimento exponencial
  - access_frequency_factor: min(1.0, times_accessed / min_steps_for_confidence)
```

### Thresholds de Transicao

| Transicao | Condicao |
|---|---|
| cold → warm (prefetch) | relevance_score > PREFETCH_THRESHOLD (0.3) |
| warm → hot (prefetch) | relevance_score > PROMOTE_THRESHOLD (0.6) |
| hot → warm (demotion) | relevance_score < HOT_THRESHOLD (0.4) E foi acessado nos ultimos K passos |
| hot → cold (demotion) | relevance_score < HOT_THRESHOLD (0.4) E nao foi acessado nos ultimos K passos |
| warm → cold (aging) | time_since_last_access > WARM_TTL (ex: 50 passos) OU access_count == 0 |

### Prefetch Prediction Rules

1. **Graph traversal como sinal primario.** O [[docs/canonical/epistemic-memory-graph|Epistemic Memory Graph]] deve ser a fonte principal de predicao: nos conectados ao task node por edges de dependency, provenance, ou causation tem alta probabilidade de serem necessarios.

2. **Prefetch conservador para cold.** Promover cold→hot diretamente e arriscado (latencia + possivel irrelevancia). Prefira cold→warm primeiro; apenas promova warm→hot se o score justificar.

3. **Janela de prefetch limitada por budget.** O prefetch nao deve consumir mais que PREFETCH_BUDGET_PCT (ex: 15%) do token budget do passo. Se os candidatos excederem, priorize por relevance_score decrescente.

4. **Feedback loop de acuracia.** Registre quais unidades prefetched foram efetivamente referenciadas pelo modelo. Use essa taxa de acerto para calibrar PREFETCH_THRESHOLD: acerto < 50% → aumente threshold (mais seletivo); acerto > 90% → reduza threshold (mais agressivo).

## Integration with Existing Repo Infrastructure

O Tiered Context Storage adiciona gerenciamento dinamico de tiers sobre a infraestrutura de contexto que o repositorio ja possui:

| Componente Existente | Como o Tiered Context Storage complementa |
|---|---|
| [[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation]] | O head-tail truncation implementa um modelo binario (ativo vs. externo). O tiered storage evolui para tres tiers com transicoes dinamicas: o middle nao e mais um bucket unico — e estratificado em warm (recente/relevante) e cold (arquivo). |
| [[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]] | O catalog fornece os handles de recuperacao (id, location, preview, scope, fetch). O tiered storage adiciona metadata de tier (hot/warm/cold) e relevance_score a cada entrada do catalog, permitindo que o Tier Orchestrator decida promocoes e democoes. |
| [[docs/canonical/hybrid-context-stack|Hybrid Context Stack]] | O context stack define camadas ordenadas de contexto. O tiered storage gerencia ONDE cada camada reside: harness prompt e estado duraveis no hot tier; historico recente no warm tier; historico completo no cold tier. |
| [[docs/canonical/epistemic-memory-graph|Epistemic Memory Graph]] | O grafo fornece as distancias e edges que alimentam o relevance_score. Sem o grafo, o tiered storage colapsa para recency-based puro. O grafo e o sinal de relevancia; o tiered storage e a acao baseada nesse sinal. |
| [[docs/canonical/explicit-token-budget-ledger|Explicit Token Budget Ledger]] | O budget ledger define o tamanho maximo do hot tier por passo. O tiered storage respeita esse limite: se o prefetch excederia o budget, unidades de menor score sao demovidas antes da montagem do contexto. |
| [[docs/canonical/durable-fact-selective-history|Durable Fact Selective History]] | Fatos duraveis (constraints, preferencias, decisoes) residem permanentemente no hot tier (ou warm com promocao garantida). O tiered storage trata fatos duraveis como pinned — nunca demovidos para cold. |
| [[docs/canonical/semantic-topic-bucketing|Semantic Topic Bucketing]] | Os topic buckets mapeiam para tiers: topicos ativos no hot tier, topicos recentes no warm tier, topicos arquivados no cold tier. O tiered storage adiciona a dimensao de latencia e politica de acesso. |

## Quality Gates

Antes de declarar o tiered context storage como operacional, verifique:

- [ ] Tres tiers estao implementados com caracteristicas de latencia distintas: hot (<1ms, in-memory), warm (~1ms, NVMe), cold (~100ms, object storage)
- [ ] Cada context unit possui metadata de tier (hot/warm/cold) e relevance_score atualizado
- [ ] O Tier Orchestrator executa demotion apos cada passo (hot→warm, hot→cold) baseado em relevance_score
- [ ] O Tier Orchestrator executa prefetch antes de cada passo (cold→warm, warm→hot) baseado em graph traversal
- [ ] Warm tier tem politica de aging: TTL e access_count determinam warm→cold
- [ ] Fatos duraveis (do [[docs/canonical/durable-fact-selective-history|Durable Fact Selective History]]) sao pinned e nunca demovidos para cold
- [ ] O tamanho do hot tier e verificado contra o token budget apos cada prefetch; unidades de menor score sao demovidas se necessario
- [ ] A taxa de acerto do prefetch e monitorada: % de unidades prefetched que foram efetivamente referenciadas pelo modelo
- [ ] PREFETCH_THRESHOLD, PROMOTE_THRESHOLD, HOT_THRESHOLD e WARM_TTL estao documentados com justificativa
- [ ] O custo de operacao do orquestrador (scoring + graph traversal) nao excede 5% do token budget do passo
- [ ] A integracao com [[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]] esta completa: cada entrada do catalog tem campo `tier` e `relevance_score`

## References

- [[docs/analysis/2026-06-18-memory-selection-problem/2026-06-18-memory-selection-problem-classification|Memory Selection Problem Classification]]:79-98 — classificado como Missing, 4 missing mechanics
- [[docs/analysis/2026-06-18-memory-selection-problem/2026-06-18-memory-selection-problem-patterns|Memory Selection Problem Patterns]]:107-151 — Pattern 3: Tiered Context Storage (inputs, outputs, benefits, limitations, components, flow)
- [[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation]] — modelo binario que o tiered storage evolui para tres tiers
- [[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]] — catalog de memoria que o tiered storage estende com metadata de tier
- [[docs/canonical/hybrid-context-stack|Hybrid Context Stack]] — camadas de contexto que o tiered storage posiciona nos tiers
- [[docs/canonical/epistemic-memory-graph|Epistemic Memory Graph]] — grafo que alimenta o relevance_score para transicoes de tier
- [[docs/canonical/explicit-token-budget-ledger|Explicit Token Budget Ledger]] — budget que limita o tamanho do hot tier
- [[docs/canonical/durable-fact-selective-history|Durable Fact Selective History]] — fatos pinned que nunca sao demovidos
- [[docs/canonical/semantic-topic-bucketing|Semantic Topic Bucketing]] — topicos que mapeiam para tiers
- [[docs/analysis/2026-06-18-memory-selection-problem/2026-06-18-memory-selection-problem-classification|cross_pattern_dependencies]]:252-256 — Tiered Context Storage enables Deliberate Forgetting and Selection-Budgeted Retrieval

---

*Created: 2026-06-18 | Source: Memory Selection Problem — Pattern 3 (Missing, Medium integration value)*
