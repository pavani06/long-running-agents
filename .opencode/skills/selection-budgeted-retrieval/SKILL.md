---
name: selection-budgeted-retrieval
description: "Torna o retrieval de contexto budget-aware: cada candidato a retrieval e ranqueado por razao valor/custo antes de ser injetado no contexto. Implementa um Information Value Predictor que estima reducao de incerteza por candidato, um Token Cost Estimator que computa custo em tokens, e um Utility Feedback Loop que aprende com uso real — quais itens recuperados foram efetivamente referenciados pelo modelo. Previne o memory feedback loop onde o sistema construido para resolver o problema de memoria se torna o motor da degradacao. Contrapoe diretamente o Link 4 (inert memory feedback) do Agent Degradation Loop. Dispara com: 'selection-budgeted retrieval', 'budgeted retrieval', 'retrieval budget', 'cost-benefit retrieval', 'information value predictor', 'utility feedback retrieval', 'retrieval ranking', 'orcamento de retrieval', 'busca budgetada', 'recuperacao com orcamento', 'value-cost retrieval', 'retrieval utility feedback'."
license: MIT
compatibility: opencode
metadata:
  audience: agent-implementers
  workflow: implementation
  priority: high
  source: "Memory Selection Problem — Pattern 7: Selection-Budgeted Retrieval"
---

## What I Do

Eu previno que o sistema de retrieval — construido para resolver o problema de memoria — se torne o motor da degradacao. Todo retrieval adiciona tokens; todo token adicionado encolhe o contexto efetivo. Eu garanto que cada retrieval e justificado por sua contribuicao prevista para a tarefa.

1. **Token Cost Estimator** — computa o custo em tokens de cada candidato a retrieval antes da decisao de recuperar.
2. **Information Value Predictor** — estima a reducao esperada de incerteza sobre a tarefa atual se um dado candidato for recuperado. Usa dados historicos de utilidade: quais itens recuperados no passado foram efetivamente referenciados pelo modelo.
3. **Cost-Benefit Ranking** — ranqueia candidatos por razao value/cost. Aloca o budget de retrieval dos candidatos mais valiosos para os menos valiosos ate o budget acabar.
4. **Utility Feedback Loop** — apos o modelo produzir output, compara quais itens recuperados foram referenciados vs. ignorados. Atualiza o predictor para melhorar estimativas futuras.

O resultado: tokens sao conservados para raciocinio em vez de gastos em contexto near-miss que o modelo vai ignorar. O retrieval para de ser uma bomba de tokens e se torna um investimento calibrado.

## When to Use Me

Carregue esta skill quando:

- O agente experimenta o memory feedback loop: cada retrieval adiciona tokens → contexto efetivo encolhe → qualidade degrada → mais retrieval e disparado → mais tokens → colapso
- Voce observa que o modelo consistentemente ignora uma fracao significativa do contexto recuperado (near-miss rate alto)
- O sistema ja tem retrieval infraestructure ([[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]], [[docs/canonical/semantic-topic-bucketing|Semantic Topic Bucketing]]) mas o retrieval nao e budget-aware
- Voce quer implementar o Link 4 Interceptor do [[docs/analysis/2026-06-18-memory-selection-problem/2026-06-18-memory-selection-problem-patterns|Agent Degradation Loop Prevention]]: Budgeted Retrieval como contramedida ao inert memory feedback
- O [[docs/canonical/explicit-token-budget-ledger|Explicit Token Budget Ledger]] tem a acao 'retrieve' mas sem mecanica de decisao sobre O QUE recuperar sob constraints de orcamento
- Ha muitas candidatas a retrieval (>50) e o modelo so consegue processar efetivamente uma fracao delas
- Voce quer um ciclo de aprendizado: o sistema deve melhorar suas decisoes de retrieval ao longo do tempo com base no que o modelo realmente usa

Nao use quando:

- O numero de candidatos a retrieval e consistentemente pequeno (<10) e o custo de todos cabe no budget — o overhead de ranking nao se justifica
- Nao ha como rastrear quais itens recuperados o modelo referenciou (sem Utility Feedback Loop, o predictor nao aprende e o sistema e apenas um cost-based truncation)
- A tarefa e de exploracao pura (open-ended research) onde o modelo precisa de contexto amplo e imprevisivel — o predictor pode subestimar o valor de itens inesperados
- O custo de estimar information value (graph traversal, consulta ao predictor) e maior que o custo de simplesmente recuperar e deixar o modelo decidir

## The Anti-Pattern

```
ANTI-PATTERN: Retrieval sem budget que alimenta o loop de degradacao.
O sistema que deveria ajudar se torna o motor da falha.

Cenario:
  1. Um agente opera em uma sessao longa. O contexto ativo esta
     chegando ao limite do orcamento de tokens.
  2. O agente precisa de informacao sobre uma decisao passada.
     Dispara retrieval: "busque tudo relacionado ao topico X."
  3. O retrieval retorna 47 context units. Similarity-based:
     todas tem similaridade > 0.7 com a query. O agente injeta
     todas no contexto ativo.
  4. Das 47 units, 38 sao near-misses: similares na superficie
     (mesmas palavras, mesmo dominio) mas irrelevantes para a
     decisao especifica. O modelo ignora 38 e usa 9.
  5. As 38 units near-miss consomem tokens, encolhem o contexto
     efetivo, e pior: atuam como distractors que reduzem a
     qualidade do raciocinio sobre as 9 units relevantes.
  6. A qualidade do passo degrada. O sistema detecta degradacao
     e dispara MAIS retrieval ("o modelo precisa de mais contexto!").
  7. Mais retrieval → mais tokens → mais near-misses → mais
     degradacao. O loop se fecha.

Cenario alternativo (retrieval sem feedback):
  1. O sistema implementa budget-aware retrieval: ranqueia
     candidatos por information value previsto e seleciona os
     top-K que cabem no orcamento.
  2. Mas o information value predictor e estatico: usa uma
     heuristica fixa (ex: recency × similarity) que nunca aprende.
  3. O predictor consistentemente superestima o valor de itens
     de um certo tipo (ex: tool results longos) e subestima
     outro tipo (ex: progress notes curtas).
  4. O budget e consistentemente alocado para o tipo errado de
     contexto. O modelo ignora a maioria do que e recuperado.
  5. Sem feedback loop, o sistema nunca descobre que esta
     desperdicando budget. O erro e sistematico e permanente.

Consequencia:
  - Memory feedback loop: retrieval → tokens → degradacao → mais
    retrieval → colapso
  - Custo de oportunidade: tokens gastos em near-misses poderiam
    ser usados para raciocinio
  - Sem feedback, o sistema nao melhora com o tempo: os mesmos
    erros de retrieval se repetem indefinidamente
```

## The Pattern

```
PATTERN: Budget-aware retrieval com cost-benefit ranking e
utility feedback loop que aprende com o uso real.

Arquitetura:

  ┌─────────────────────────────────────────────────────────────┐
  │              SELECTION-BUDGETED RETRIEVAL                     │
  │                                                              │
  │  STEP N: Modelo precisa de contexto                          │
  │       │                                                      │
  │       ▼                                                      │
  │  ┌──────────────────────────────────────────────────────┐   │
  │  │ 1. CANDIDATE IDENTIFICATION                           │   │
  │  │                                                      │   │
  │  │ Sources:                                              │   │
  │  │ ├─ [[Epistemic Memory Graph]]: graph traversal        │   │
  │  │ │  from task node along typed edges                   │   │
  │  │ ├─ [[Addressable Memory Catalog]]: handle-based       │   │
  │  │ │  lookup by topic, session, task                     │   │
  │  │ ├─ [[Semantic Topic Bucketing]]: topic-based          │   │
  │  │ │  retrieval for broad context                        │   │
  │  │ └─ [[Tiered Context Storage]]: promotion candidates   │   │
  │  │    from warm/cold tiers                               │   │
  │  │                                                      │   │
  │  │ Output: candidate_list = [c1, c2, ..., cN]            │   │
  │  └────────────────────┬─────────────────────────────────┘   │
  │                       │                                      │
  │                       ▼                                      │
  │  ┌──────────────────────────────────────────────────────┐   │
  │  │ 2. TOKEN COST ESTIMATION (per candidate)              │   │
  │  │                                                      │   │
  │  │ For each candidate c_i:                               │   │
  │  │   token_cost_i = estimate_tokens(c_i.content)         │   │
  │  │                  + retrieval_overhead                 │   │
  │  │                  + formatting_overhead                │   │
  │  │                                                      │   │
  │  │ Retrieval overhead: tokens to represent the retrieval │   │
  │  │ in the prompt (ex: "Retrieved context [id]: ...")     │   │
  │  │                                                      │   │
  │  │ Formatting overhead: adapter-specific formatting      │   │
  │  │ (ex: XML tags, JSON structure)                        │   │
  │  └────────────────────┬─────────────────────────────────┘   │
  │                       │                                      │
  │                       ▼                                      │
  │  ┌──────────────────────────────────────────────────────┐   │
  │  │ 3. INFORMATION VALUE PREDICTION (per candidate)       │   │
  │  │                                                      │   │
  │  │ For each candidate c_i:                               │   │
  │  │                                                      │   │
  │  │   info_value_i = predict_value(                       │   │
  │  │     candidate = c_i,                                  │   │
  │  │     task_state = current_task,                        │   │
  │  │     history = utility_feedback_db,                    │   │
  │  │     features = [                                      │   │
  │  │       graph_distance(c_i, task_node),                 │   │
  │  │       edge_type_match(c_i, task_query_type),          │   │
  │  │       historical_reference_rate(c_i.kind),            │   │
  │  │       recency(c_i.timestamp),                         │   │
  │  │       content_freshness(c_i, prior_retrievals),       │   │
  │  │       model_attention_profile(current_model)          │   │
  │  │     ]                                                 │   │
  │  │   )                                                   │   │
  │  │                                                      │   │
  │  │ info_value ∈ [0, 1]: 0 = certainly ignored,          │   │
  │  │                       1 = certainly referenced        │   │
  │  └────────────────────┬─────────────────────────────────┘   │
  │                       │                                      │
  │                       ▼                                      │
  │  ┌──────────────────────────────────────────────────────┐   │
  │  │ 4. COST-BENEFIT RANKING                               │   │
  │  │                                                      │   │
  │  │ For each candidate:                                   │   │
  │  │   value_cost_ratio_i = info_value_i / token_cost_i    │   │
  │  │                                                      │   │
  │  │ Sort candidates by value_cost_ratio descending        │   │
  │  │                                                      │   │
  │  │ Allocate retrieval_budget:                            │   │
  │  │   retrieval_budget = total_step_budget               │   │
  │  │                     - reasoning_reserve              │   │
  │  │                     - harness_overhead                │   │
  │  │                                                      │   │
  │  │ Select top-K where sum(token_cost_1..K) ≤ budget     │   │
  │  │                                                      │   │
  │  │ Remaining candidates: deferred (not retrieved)        │   │
  │  └────────────────────┬─────────────────────────────────┘   │
  │                       │                                      │
  │                       ▼                                      │
  │  ┌──────────────────────────────────────────────────────┐   │
  │  │ 5. RETRIEVE & INJECT                                  │   │
  │  │                                                      │   │
  │  │ Retrieve selected K candidates from storage           │   │
  │  │ Inject into context with metadata:                    │   │
  │  │   [retrieved id=C1] content                           │   │
  │  │   [retrieved id=C2] content                           │   │
  │  │ Log budget consumption:                               │   │
  │  │   tokens_spent = sum(token_cost_1..K)                 │   │
  │  │   candidates_deferred = N - K                         │   │
  │  │   budget_remaining = retrieval_budget - tokens_spent  │   │
  │  └────────────────────┬─────────────────────────────────┘   │
  │                       │                                      │
  │                       ▼                                      │
  │  STEP N EXECUTING (modelo raciocina com contexto recuperado) │
  │       │                                                      │
  │       ▼                                                      │
  │  ┌──────────────────────────────────────────────────────┐   │
  │  │ 6. UTILITY FEEDBACK (post-step)                       │   │
  │  │                                                      │   │
  │  │ For each retrieved candidate c_i:                     │   │
  │  │                                                      │   │
  │  │   was_referenced_i = detect_reference(                │   │
  │  │     model_output,                                     │   │
  │  │     c_i.content                                       │   │
  │  │   )                                                   │   │
  │  │                                                      │   │
  │  │   Detection methods:                                  │   │
  │  │   ├─ Citation match: does output cite c_i.id?         │   │
  │  │   ├─ Content overlap: does output paraphrase c_i?     │   │
  │  │   ├─ Decision impact: did c_i change the decision?    │   │
  │  │   └─ Attention proxy: was c_i in high-attention       │   │
  │  │      position? (if attention available)               │   │
  │  │                                                      │   │
  │  │ Update utility_feedback_db:                           │   │
  │  │   record(c_i.kind, c_i.features, was_referenced_i)    │   │
  │  │                                                      │   │
  │  │ Retrain/recalibrate predictor periodically            │   │
  │  │ (ex: every 100 retrievals or daily)                   │   │
  │  └──────────────────────────────────────────────────────┘   │
  └─────────────────────────────────────────────────────────────┘
```

### Budget Allocation

```
total_step_budget = from [[Explicit Token Budget Ledger]]

allocation:
  harness_overhead    = fixed (prompt, tool definitions, safety buffer)
  reasoning_reserve   = total_step_budget × 0.40  // 40% para raciocinio
  retrieval_budget    = total_step_budget - harness_overhead - reasoning_reserve

Se retrieval_budget < MIN_RETRIEVAL_BUDGET (ex: 200 tokens):
  → skip retrieval entirely (budget muito apertado, priorize raciocinio)
  → log: "retrieval skipped: insufficient budget"

Se nenhum candidato tem value_cost_ratio > MIN_VALUE_THRESHOLD:
  → skip retrieval (custo de recuperar > valor esperado)
  → log: "retrieval skipped: no candidates above value threshold"
```

### Information Value Predictor Features

| Feature | Peso | Justificativa |
|---|---|---|
| `graph_distance(c_i, task_node)` | Alto | Unidades diretamente conectadas ao task node tem maior probabilidade de serem referenciadas |
| `edge_type_match(c_i, task_query_type)` | Alto | Se a query e sobre dependencias, candidatos com edge `dependency` tem valor maior |
| `historical_reference_rate(c_i.kind)` | Medio | Certos tipos de context unit (ex: `decision`) sao historicamente mais referenciados que outros (ex: `progress_note`) |
| `recency(c_i.timestamp)` | Medio | Unidades mais recentes tem maior probabilidade de relevancia, mas com peso menor que graph distance |
| `content_freshness(c_i, prior_retrievals)` | Baixo | Se o conteudo ja foi recuperado e NAO referenciado em passos anteriores, valor diminui |
| `model_attention_profile(current_model)` | Baixo | Modelos diferentes tem perfis de atencao diferentes; ajusta expectativa de referencia |

### Utility Feedback: Reference Detection

```
detect_reference(output, candidate_content):
  
  // Method 1: Explicit citation (highest confidence)
  if output contains candidate.id:
    return true  // "According to [C17], the answer is..."
  
  // Method 2: Content fingerprint (medium confidence)
  key_phrases = extract_key_phrases(candidate_content, max=3)
  if ≥2 key_phrases appear in output:
    return true  // likely paraphrased or used
  
  // Method 3: Semantic entailment (lower confidence, mais caro)
  if entailment_score(output, candidate_content) > 0.7:
    return true
  
  return false  // no evidence of reference
```

## Implementation Rules

1. **Retrieval budget e hard, nao soft.** Se os top-K candidatos excedem o retrieval_budget, os candidatos K+1..N SAO descartados — nao recuperados, nao injetados. Nao ha "so mais um". O budget existe para proteger o raciocinio.

2. **MIN_RETRIEVAL_BUDGET existe para proteger sessoes curtas.** Se o passo tem budget muito apertado, e melhor pular retrieval completamente do que injetar contexto insuficiente que so vai distrair. O modelo raciocina melhor com contexto zero do que com contexto parcial e enganoso.

3. **O predictor deve ser conservador no inicio.** Quando o utility_feedback_db tem poucos dados (cold start), o predictor deve usar peso maior em features estruturais (graph distance, edge type) e peso menor em features historicas (reference rate). Conforme o DB acumula dados, o peso das features historicas aumenta gradualmente.

4. **Reference detection nao e perfeito — e nao precisa ser.** O objetivo nao e auditoria forense de citacao. E detectar o sinal grosseiro: "o modelo usou isso ou ignorou completamente?" Falsos negativos (modelo usou mas nao detectamos) sao aceitaveis; falsos positivos (modelo nao usou mas marcamos como usado) sao mais danosos porque ensinam o predictor errado.

5. **Recalibracao periodica, nao online.** O predictor nao deve ser atualizado a cada retrieval (online learning) porque isso introduz oscilacao. Recalibre em batch: a cada 100 retrievals, ou diariamente, re-treine o predictor com todos os dados acumulados.

6. **O custo do ranking e contabilizado no budget.** Estimar token_cost, predict_value, e ordenar N candidatos consome tokens de computacao (nao de prompt, mas de latencia e CPU). Se N > 100, considere pre-filtrar com heuristica barata (ex: graph_distance < 3) antes do ranking completo.

7. **Candidatos deferred nao sao descartados permanentemente.** Eles permanecem disponiveis para passos futuros. Se um candidato e deferred repetidamente (ex: 5 passos seguidos), seu info_value deve ser decrementado permanentemente — ele provavelmente nao e relevante para esta sessao.

## Integration with Existing Repo Infrastructure

O Selection-Budgeted Retrieval conecta a infraestrutura de token budget com a infraestrutura de retrieval, adicionando a camada de decisao custo-beneficio que falta:

| Componente Existente | Como o Selection-Budgeted Retrieval complementa |
|---|---|
| [[docs/canonical/explicit-token-budget-ledger|Explicit Token Budget Ledger]] | O budget ledger tem a acao 'retrieve' (line 63) mas sem mecanica de decisao. O budgeted retrieval implementa essa mecanica: decide O QUE recuperar sob constraints de orcamento, com cost-benefit ranking. |
| [[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]] | O catalog fornece os handles de recuperacao. O budgeted retrieval adiciona a camada de decisao: entre todos os handles disponiveis, quais recuperar dado o budget? |
| [[docs/canonical/epistemic-memory-graph|Epistemic Memory Graph]] | O grafo fornece graph_distance e edge_type — os features estruturais mais importantes do information value predictor. Sem o grafo, o predictor depende apenas de features fracas (recency, kind). |
| [[docs/canonical/semantic-topic-bucketing|Semantic Topic Bucketing]] | Os topic buckets sao uma fonte de candidatos. O budgeted retrieval ranqueia candidatos de multiplos buckets por value/cost ratio, em vez de recuperar tudo de um bucket. |
| [[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation]] | O middle storage e a fonte de candidatos para retrieval. O budgeted retrieval decide quais partes do middle recuperar e quais deixar em storage. |
| [[docs/canonical/burn-rate-runtime-forecast|Burn Rate Runtime Forecast]] | O burn rate forecast projeta quantos passos restam na sessao. O budgeted retrieval usa essa projecao para ajustar a agressividade: se a sessao esta acabando, priorize candidates com maior value/cost. |
| [[docs/canonical/eval-to-production-correlation-tracking|Eval-to-Production Correlation Tracking]] | O correlation tracking pode validar o predictor: se retrievals com alto info_value previsto consistentemente resultam em melhores outcomes, o predictor e util. Se nao ha correlacao, o predictor precisa ser recalibrado. |
| [[docs/analysis/2026-06-18-memory-selection-problem/2026-06-18-memory-selection-problem-patterns|Agent Degradation Loop Prevention]]:373 — O budgeted retrieval e o Link 4 Interceptor: previne que memory retrieval alimente o loop de degradacao. |

## Quality Gates

Antes de declarar o selection-budgeted retrieval como operacional, verifique:

- [ ] Token Cost Estimator computa custo de cada candidato incluindo retrieval_overhead e formatting_overhead
- [ ] Information Value Predictor usa pelo menos 3 features (graph_distance, edge_type_match, historical_reference_rate)
- [ ] Cost-benefit ranking ranqueia candidatos por value_cost_ratio decrescente
- [ ] Retrieval budget e derivado do total_step_budget com reserva para raciocinio (minimo 40%)
- [ ] MIN_RETRIEVAL_BUDGET esta definido e o sistema pula retrieval quando o budget e insuficiente
- [ ] MIN_VALUE_THRESHOLD esta definido e o sistema pula retrieval quando nenhum candidato supera o threshold
- [ ] Utility Feedback Loop detecta quais itens recuperados foram referenciados pelo modelo (pelo menos 2 metodos de deteccao)
- [ ] Cold start do predictor usa peso maior em features estruturais (graph) e menor em historicas
- [ ] Recalibracao periodica do predictor esta agendada (batch, nao online)
- [ ] Candidatos deferred repetidamente (5+ passos) tem seu info_value decrementado
- [ ] O custo do ranking (N candidatos) e contabilizado e nao excede 5% do retrieval_budget
- [ ] Budget consumption log registra tokens_spent, candidates_deferred, e budget_remaining por retrieval

## References

- [[docs/analysis/2026-06-18-memory-selection-problem/2026-06-18-memory-selection-problem-classification|Memory Selection Problem Classification]]:185-209 — classificado como Missing (High integration value), 4 missing mechanics
- [[docs/analysis/2026-06-18-memory-selection-problem/2026-06-18-memory-selection-problem-patterns|Memory Selection Problem Patterns]]:294-340 — Pattern 7: Selection-Budgeted Retrieval (inputs, outputs, benefits, limitations, components, flow)
- [[docs/canonical/explicit-token-budget-ledger|Explicit Token Budget Ledger]] — budget ledger com acao 'retrieve' que o budgeted retrieval operacionaliza
- [[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]] — catalog de handles que o budgeted retrieval ranqueia
- [[docs/canonical/epistemic-memory-graph|Epistemic Memory Graph]] — grafo que alimenta os features estruturais do predictor
- [[docs/canonical/semantic-topic-bucketing|Semantic Topic Bucketing]] — buckets que fornecem candidatos ao retrieval
- [[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation]] — middle storage como fonte de candidatos
- [[docs/canonical/burn-rate-runtime-forecast|Burn Rate Runtime Forecast]] — projecao de passos restantes que ajusta agressividade do retrieval
- [[docs/canonical/eval-to-production-correlation-tracking|Eval-to-Production Correlation Tracking]] — validacao do predictor contra outcomes reais
- [[docs/analysis/2026-06-18-memory-selection-problem/2026-06-18-memory-selection-problem-patterns|Agent Degradation Loop Prevention]]:373 — "Link 4 Interceptor: Budgeted Retrieval"
- [[docs/analysis/2026-06-18-memory-selection-problem/2026-06-18-memory-selection-problem-classification|cross_pattern_dependencies]]:262-264 — Selection-Budgeted Retrieval directly counters Link 4 of Agent Degradation Loop

---

*Created: 2026-06-18 | Source: Memory Selection Problem — Pattern 7 (Missing, High integration value)*
