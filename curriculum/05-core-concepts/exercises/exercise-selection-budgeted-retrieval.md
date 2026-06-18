---
title: "Exercicio: Implementar Selection-Budgeted Retrieval com Cost-Benefit Ranking"
type: exercise
level: "N3"
aliases: ["selection-budgeted retrieval", "budget-aware retrieval", "cost-benefit ranking", "information value predictor", "utility feedback loop", "retrieval budget", "token-cost retrieval"]
tags: [curriculo-conteudo, context-engineering, agentes-orquestracao, token-budgeting, harness-engineering]
duration: "2-3h"
relates-to: ["[[docs/analysis/2026-06-18-memory-selection-problem/2026-06-18-memory-selection-problem-patterns|Memory Selection Patterns]]", "[[docs/analysis/2026-06-18-memory-selection-problem/2026-06-18-memory-selection-problem-classification|Memory Selection Classification]]", "[[docs/canonical/explicit-token-budget-ledger|Explicit Token Budget Ledger]]", "[[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]", "[[docs/canonical/semantic-topic-bucketing|Semantic Topic Bucketing]]", "[[docs/canonical/burn-rate-runtime-forecast|Burn Rate Runtime Forecast]]"]
last_updated: 2026-06-18
---
# Exercicio: Implementar Selection-Budgeted Retrieval com Cost-Benefit Ranking
## Nivel 3 - Arquitetura Avancada

## Objetivo

Implementar um sistema de recuperacao de contexto que ranqueia candidatos por custo-beneficio, opera sob um orcamento de tokens explicito, e aprende com feedback de utilidade para melhorar predicoes futuras.

**Tempo Estimado:** 2-3 horas
**Dificuldade:** Avancado
**Pre-requisito:** Ter lido `[[docs/canonical/explicit-token-budget-ledger|Explicit Token Budget Ledger]]`, `[[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]` e `[[docs/canonical/burn-rate-runtime-forecast|Burn Rate Runtime Forecast]]`
**Objetivo:** Implementar um `SelectionBudgetedRetriever` que ranqueia candidatos de recuperacao por custo-beneficio, opera sob orcamento de tokens, e mantem um loop de feedback que aprende quais recuperacoes sao realmente uteis.

---

## Prologo: O Motor de Busca Que Afogava o Modelo

### Quarta-feira, 10h. Review de qualidade do agente.

```
ENGENHEIRO: "O agente de suporte esta piorando nas sessoes longas.
           A gente adicionou o retrieval de contexto porque o modelo
           esquecia decisoes anteriores. Mas agora parece que ele
           esta PIOR do que antes."
```

O agente `SupportAgent` da **MercuryPay** atendia tickets de suporte tecnico. Sessoes curtas (5-10 minutos) funcionavam bem. Mas tickets complexos duravam 45 minutos, e o agente comecava a repetir diagnosticos, ignorar contexto relevante, e contradizer decisoes anteriores.

O time implementou um sistema de retrieval: a cada passo, o agente consultava o addressable memory catalog, recuperava contexto relacionado ao ticket atual, e injetava no prompt. O resultado foi o oposto do esperado:

```
═══════════════════════════════════════════════════════════════
        ANALISE DE REGRESSAO — RETRIEVAL DE CONTEXTO
═══════════════════════════════════════════════════════════════

ANTES DO RETRIEVAL:
  Tickets resolvidos:      72%
  Tempo medio:             18 min
  Contexto ativo medio:    8,000 tokens

DEPOIS DO RETRIEVAL:
  Tickets resolvidos:      58%  ← PIOR
  Tempo medio:             31 min  ← MAIS LENTO
  Contexto ativo medio:   42,000 tokens  ← 5.25x MAIS TOKENS

ANALISE DAS RECUPERACOES:
  Total de itens recuperados:   1,847
  Itens efetivamente usados:     312  (17%)
  Itens ignorados pelo modelo: 1,535  (83%)
  Near-misses (similar mas irrelevante): 892 (48%)

  Cada recuperacao custou tokens. A maioria das recuperacoes
  injetou contexto que o modelo IGNOROU — mas que ocupou
  espaco na janela e diluiu a atencao do modelo.
  
  O retrieval, que deveria RESOLVER o problema de memoria,
  virou o MOTOR da degradacao.
═══════════════════════════════════════════════════════════════
```

```
ARQUITETA (post-mortem): "O retrieval nao e gratuito. Cada item
                          recuperado custa tokens — tokens que
                          competem com o raciocinio do modelo.
                          
                          Nosso retrieval era guloso: recuperava
                          tudo que parecia relevante, sem nunca
                          perguntar 'vale a pena?'. O que faltava
                          era um sistema que ranqueia candidatos
                          por custo-beneficio, respeita um orcamento
                          de tokens, e aprende com feedback quais
                          recuperacoes realmente ajudam."
```

**O que teria evitado tudo:**

> Selection-Budgeted Retrieval: um sistema de recuperacao que trata cada candidato como um investimento de tokens. Cada candidato tem um custo (tokens), um valor estimado (reducao esperada de incerteza), e um historico de utilidade (foi usado ou ignorado?). O recuperador ranqueia por value/cost ratio, aloca tokens do mais valioso ao menos, e para quando o orcamento acaba. O loop de feedback aprende: se um tipo de contexto e consistentemente ignorado, seu valor estimado cai.

**Sua missao:** Construir um `SelectionBudgetedRetriever` que implementa exatamente essa recuperacao budget-aware.

---

## Cenario: Retrieval Budget-Aware no Agente de Suporte

### Contexto

Voce e o engenheiro de qualidade do time de plataforma da **MercuryPay**. O `SupportAgent` processa tickets de suporte. A cada passo, o agente consulta o catalogo de memoria enderecavel, que retorna candidatos de recuperacao. Cada candidato tem:

| Campo | Descricao | Exemplo |
|---|---|---|
| `candidate_id` | ID unico | `mem-0042` |
| `kind` | Tipo de contexto | `past_decision`, `error_log`, `runbook`, `customer_history` |
| `token_cost` | Custo em tokens se recuperado | 350 |
| `similarity_score` | Score de similaridade (embedding) | 0.87 |
| `topic_tags` | Tags de topico | `["payment", "timeout"]` |
| `recency_hours` | Ha quanto tempo foi gerado | 0.5 |

O problema: o sistema atual recupera todo candidato com `similarity_score > 0.70`. Isso resulta em 83% de recuperacoes inuteis.

### Orcamento e Valor

O agente tem um **token budget** de 8,000 tokens por passo para recuperacao. Desses, 2,000 sao reservados para o prompt do harness (fixo) e 1,000 para o tail anchor (contexto recente). Sobram 5,000 tokens para recuperacao.

Cada candidato recuperado ocupa `token_cost` tokens desse orcamento. O desafio: escolher o subconjunto de candidatos que maximiza o valor informacional esperado sem exceder 5,000 tokens.

O **valor informacional** de um candidato e estimado como:

```
predicted_value = base_relevance * topic_match_bonus * utility_factor

Onde:
  base_relevance = similarity_score (ja calculado pelo catalog)
  topic_match_bonus = 1.5 se o ticket atual compartilha >= 2 topic_tags com o candidato
                      1.0 caso contrario
  utility_factor = historico de quantas vezes este tipo de contexto (kind)
                   foi efetivamente referenciado pelo modelo em sessoes anteriores
                   (inicia em 0.50, atualizado pelo feedback loop)
```

### Dados de Entrada

Voce recebe um batch de 25 candidatos de recuperacao para um ticket de suporte sobre falha de pagamento:

```python
# Ticket atual: "payment_timeout_error"
# Topic tags do ticket: ["payment", "timeout", "gateway", "production"]
# Budget de recuperacao: 5000 tokens

RETRIEVAL_CANDIDATES = [
    # (candidate_id, kind, token_cost, similarity_score, topic_tags, recency_hours)
    ("mem-001", "error_log",         350, 0.92, ["payment", "timeout"],              0.2),
    ("mem-002", "past_decision",     180, 0.88, ["payment", "gateway", "rollback"],  0.5),
    ("mem-003", "runbook",          1200, 0.95, ["payment", "timeout", "gateway"],   0.1),
    ("mem-004", "customer_history",  600, 0.45, ["account", "premium"],             48.0),
    ("mem-005", "error_log",         280, 0.78, ["timeout", "database"],             0.3),
    ("mem-006", "past_decision",     220, 0.72, ["gateway", "circuit_breaker"],     24.0),
    ("mem-007", "error_log",         400, 0.91, ["payment", "timeout", "gateway"],   0.1),
    ("mem-008", "runbook",           900, 0.68, ["database", "restart"],            72.0),
    ("mem-009", "customer_history",  500, 0.55, ["payment", "dispute"],             12.0),
    ("mem-010", "past_decision",     150, 0.85, ["payment", "timeout"],              0.4),
    ("mem-011", "error_log",         320, 0.94, ["payment", "gateway", "timeout"],   0.2),
    ("mem-012", "runbook",          1500, 0.60, ["network", "dns"],                 48.0),
    ("mem-013", "customer_history",  450, 0.40, ["account", "basic"],              120.0),
    ("mem-014", "past_decision",     200, 0.82, ["timeout", "retry"],                0.3),
    ("mem-015", "error_log",         380, 0.87, ["payment", "gateway"],              0.4),
    ("mem-016", "error_log",         290, 0.76, ["timeout", "load_balancer"],        0.3),
    ("mem-017", "past_decision",     170, 0.90, ["payment", "timeout", "gateway"],   0.2),
    ("mem-018", "runbook",           800, 0.55, ["monitoring", "alerts"],           24.0),
    ("mem-019", "customer_history",  550, 0.35, ["onboarding", "new_user"],        200.0),
    ("mem-020", "error_log",         310, 0.83, ["payment", "timeout"],              0.5),
    ("mem-021", "past_decision",     190, 0.79, ["gateway", "failover"],            18.0),
    ("mem-022", "error_log",         360, 0.89, ["payment", "timeout", "gateway"],   0.2),
    ("mem-023", "runbook",          1100, 0.71, ["payment", "gateway"],              0.3),
    ("mem-024", "customer_history",  480, 0.42, ["payment", "history"],             36.0),
    ("mem-025", "past_decision",     160, 0.86, ["payment", "timeout", "gateway"],   0.1),
]
```

---

## Requisitos

### Requisitos Funcionais

1. **RF1 - Token Cost Estimator:** Cada candidato tem um `token_cost` conhecido. O recuperador calcula o custo acumulado de qualquer subconjunto de candidatos.
2. **RF2 - Information Value Predictor:** Para cada candidato, calcula `predicted_value` usando similaridade, topic match bonus, e utility factor historico.
3. **RF3 - Cost-Benefit Ranking:** Ranqueia candidatos por `predicted_value / token_cost` (valor por token gasto). Aloca orcamento dos melhores aos piores ate o budget acabar.
4. **RF4 - Budget Gate:** Recuperacao so ocorre se `token_cost <= remaining_budget`. Candidatos que nao cabem no orcamento restante sao `DEFERRED` (nao descartados — podem ser recuperados no futuro).
5. **RF5 - Retrieval Decision:** Para cada candidato, decide: `RETRIEVE` (recuperar e injetar no prompt), `DEFER` (cabe no orcamento mas value/cost ratio baixo — so recuperar se sobrar budget), ou `SKIP` (nao recuperar — value/cost abaixo do threshold).
6. **RF6 - Utility Feedback Loop:** Apos o modelo produzir output, o recuperador verifica quais itens recuperados foram referenciados. Atualiza `utility_factor` do `kind` correspondente. Utility factors sobem quando o tipo e usado, caem lentamente (decay de 5%) quando nao e.

### Requisitos Tecnicos

1. **RT1 - Python puro:** Implementacao em Python com stdlib + dataclasses.
2. **RT2 - Ranking deterministico:** Dado o mesmo batch de candidatos e historico de utilidade, o ranking e deterministico.
3. **RT3 - Budget enforcement estrito:** O total de tokens dos candidatos `RETRIEVE` nunca excede o `retrieval_budget`.
4. **RT4 - Feedback loop com decay:** Utility factors sao atualizados apos cada sessao e sofrem decay de 5% ao fim da sessao se o kind nao foi usado.

---

## Sua Tarefa

Voce vai implementar o `SelectionBudgetedRetriever` em 3 partes.

---

### Parte 1: Diagnosticar o Retrieval Guloso (15 min)

Analise os 25 candidatos de recuperacao. Responda:

1. Se o sistema atual (guloso: `similarity_score > 0.70`) recuperar todos os candidatos, quantos tokens seriam consumidos? Quantos excedem o orcamento de 5,000?
2. Quais candidatos tem alta similaridade (>0.85) mas topic_match_bonus = 1.0 (pouca sobreposicao de topicos)? Esses sao os near-misses — contextualmente similares mas topicamente irrelevantes.
3. Quais candidatos seriam selecionados pelo cost-benefit ranking com budget de 5,000 tokens e utility_factor inicial de 0.50 para todos os kinds?

```python
# TAREFA: Responda no seu codigo como comentario:
#
# 1. Quantos candidatos tem similarity_score > 0.70?
#    Qual o token_cost total desses candidatos?
#    Quantos excedem o orcamento de 5,000 tokens?
#
# 2. Near-miss analysis:
#    - Liste candidatos com similarity > 0.70 mas < 2 topic_tags
#      em comum com o ticket atual.
#    - Esses candidatos seriam recuperados pelo sistema guloso?
#    - Eles tem alta probabilidade de serem ignorados pelo modelo?
#
# 3. Com budget de 5,000 tokens:
#    a. Calcule predicted_value para cada candidato com utility=0.50
#    b. Calcule value/cost ratio = predicted_value / token_cost
#    c. Ordene por value/cost ratio decrescente
#    d. Aloque orcamento do topo ate o budget acabar
#    e. Liste os candidatos RETRIEVE, DEFER, SKIP
#
# 4. Compare o numero de tokens recuperados entre:
#    a. Sistema guloso (similarity > 0.70)
#    b. Selection-Budgeted Retrieval (value/cost ranking + budget)
#    Qual a reducao percentual em tokens recuperados?
#    Quantos near-misses o sistema guloso teria injetado?
```

---

### Parte 2: Implementar o SelectionBudgetedRetriever (70 min)

Implemente o sistema de recuperacao budget-aware. Use este esqueleto:

```python
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Optional


# ============================================================
# DATA MODELS
# ============================================================

class RetrievalDecision(Enum):
    RETRIEVE = "retrieve"  # recuperar e injetar
    DEFER = "defer"        # valor ok, mas sem orcamento agora
    SKIP = "skip"          # valor/custo muito baixo


class ContextKind(Enum):
    ERROR_LOG = "error_log"
    PAST_DECISION = "past_decision"
    RUNBOOK = "runbook"
    CUSTOMER_HISTORY = "customer_history"


@dataclass
class RetrievalCandidate:
    """Um candidato de recuperacao do catalogo de memoria."""
    candidate_id: str
    kind: ContextKind
    token_cost: int
    similarity_score: float  # [0, 1]
    topic_tags: list[str]
    recency_hours: float

    # Calculados pelo predictor
    predicted_value: float = 0.0
    value_cost_ratio: float = 0.0

    # Decisao do recuperador
    decision: RetrievalDecision = RetrievalDecision.DEFER

    # Feedback (preenchido apos output do modelo)
    was_referenced: bool = False


@dataclass
class RetrievalBudget:
    """Orcamento de tokens para recuperacao em um passo."""
    total_budget: int         # orcamento total (ex: 5000)
    harness_reserved: int     # reserva para prompt fixo (ex: 2000)
    tail_anchor_reserved: int # reserva para tail anchor (ex: 1000)

    @property
    def retrieval_budget(self) -> int:
        """Orcamento disponivel para recuperacao."""
        return self.total_budget - self.harness_reserved - self.tail_anchor_reserved

    @property
    def remaining(self) -> int:
        """Orcamento restante (gerenciado pelo BudgetTracker)."""
        return self._remaining

    def __post_init__(self):
        self._remaining = self.retrieval_budget

    def consume(self, tokens: int) -> bool:
        """
        Consome tokens do orcamento.

        Returns:
            True se havia orcamento suficiente, False caso contrario.
        """
        if tokens <= self._remaining:
            self._remaining -= tokens
            return True
        return False


@dataclass
class UtilityTracker:
    """
    Rastreia a utilidade historica de cada tipo de contexto (kind).

    utility_factor para cada kind ∈ [0.1, 1.0].
    Inicia em 0.50. Sobe quando o tipo e referenciado.
    Cai 5% (decay) quando nao e referenciado em uma sessao.
    """
    factors: dict[str, float] = field(default_factory=lambda: {
        "error_log": 0.50,
        "past_decision": 0.50,
        "runbook": 0.50,
        "customer_history": 0.50,
    })

    DECAY_RATE = 0.05
    BOOST_RATE = 0.10
    MIN_FACTOR = 0.10
    MAX_FACTOR = 1.00

    def get(self, kind: ContextKind) -> float:
        """Retorna o utility factor atual para um kind."""
        return self.factors.get(kind.value, 0.50)

    def record_usage(self, kind: ContextKind) -> None:
        """
        Registra que um tipo de contexto foi referenciado pelo modelo.
        Aumenta o utility factor.
        """
        # SEU CODIGO AQUI
        # self.factors[kind.value] = min(MAX_FACTOR, current + BOOST_RATE)
        pass

    def apply_decay(self, used_kinds: set[ContextKind]) -> None:
        """
        Aplica decay (reducao) aos kinds que NAO foram usados na sessao.

        Args:
            used_kinds: Conjunto de kinds que foram referenciados nesta sessao.
        """
        # SEU CODIGO AQUI
        # Para cada kind em factors:
        #   se kind nao esta em used_kinds:
        #       factors[kind] = max(MIN_FACTOR, factors[kind] * (1 - DECAY_RATE))
        pass


# ============================================================
# INFORMATION VALUE PREDICTOR
# ============================================================

@dataclass
class InformationValuePredictor:
    """
    Prediz o valor informacional de cada candidato de recuperacao.

    Formula:
      predicted_value = similarity_score * topic_match_bonus * utility_factor

    Onde:
      - similarity_score: score de similaridade (embedding) do catalogo
      - topic_match_bonus: 1.5 se >= 2 topic_tags em comum com o ticket,
                           1.0 caso contrario
      - utility_factor: historico de utilidade do kind (do UtilityTracker)
    """

    utility_tracker: UtilityTracker
    ticket_topic_tags: list[str] = field(default_factory=list)
    MIN_TOPIC_MATCH_FOR_BONUS: int = 2
    TOPIC_MATCH_BONUS_MULTIPLIER: float = 1.5

    def compute_topic_match_count(self, candidate_tags: list[str]) -> int:
        """Conta quantos topic_tags o candidato compartilha com o ticket."""
        # SEU CODIGO AQUI
        pass

    def predict_value(self, candidate: RetrievalCandidate) -> float:
        """
        Calcula o predicted_value de um candidato.

        Args:
            candidate: Candidato de recuperacao.

        Returns:
            Valor predito em [0, 1.5] (pode exceder 1.0 com topic_match_bonus).
        """
        # SEU CODIGO AQUI
        #
        # 1. similarity = candidate.similarity_score
        # 2. topic_match = compute_topic_match_count(candidate.topic_tags)
        # 3. bonus = TOPIC_MATCH_BONUS_MULTIPLIER if topic_match >= MIN_TOPIC_MATCH_FOR_BONUS else 1.0
        # 4. utility = utility_tracker.get(candidate.kind)
        # 5. return similarity * bonus * utility
        pass

    def rank_candidates(self, candidates: list[RetrievalCandidate]) -> list[RetrievalCandidate]:
        """
        Ranqueia candidatos por value/cost ratio decrescente.

        Calcula predicted_value e value_cost_ratio para cada candidato,
        depois ordena por value_cost_ratio descendente.
        """
        # SEU CODIGO AQUI
        #
        # 1. Para cada candidato:
        #    a. candidate.predicted_value = predict_value(candidate)
        #    b. candidate.value_cost_ratio = predicted_value / token_cost
        # 2. Ordenar candidates por value_cost_ratio descendente
        # 3. Retornar lista ordenada
        pass


# ============================================================
# SELECTION-BUDGETED RETRIEVER — nucleo do exercicio
# ============================================================

# Threshold de value/cost ratio abaixo do qual candidatos sao SKIP
MIN_VALUE_COST_RATIO = 0.0005  # abaixo disso: valor negligivel por token


@dataclass
class SelectionBudgetedRetriever:
    """
    Recuperador de contexto budget-aware.

    Fluxo:
    1. Receber candidatos do catalogo de memoria
    2. Ranquear por value/cost ratio (via InformationValuePredictor)
    3. Alocar orcamento dos melhores aos piores
    4. Decidir RETRIEVE / DEFER / SKIP para cada candidato
    5. Apos output do modelo, coletar feedback de utilidade
    """

    predictor: InformationValuePredictor
    budget: RetrievalBudget
    utility_tracker: UtilityTracker

    def retrieve(self, candidates: list[RetrievalCandidate]) -> list[RetrievalCandidate]:
        """
        Executa a recuperacao budget-aware.

        Args:
            candidates: Lista de candidatos do catalogo de memoria.

        Returns:
            Lista de candidatos com decision field preenchido.
            Apenas candidatos com decision=RETRIEVE serao injetados no prompt.
        """
        # SEU CODIGO AQUI
        #
        # Algoritmo:
        # 1. Resetar orcamento (budget._remaining = budget.retrieval_budget)
        # 2. Ranquear candidatos via predictor.rank_candidates()
        # 3. Para cada candidato no ranking:
        #    a. Se value_cost_ratio < MIN_VALUE_COST_RATIO: decision = SKIP
        #    b. Senao, se budget.consume(token_cost): decision = RETRIEVE
        #    c. Senao: decision = DEFER (caberia, mas sem orcamento)
        # 4. Retornar lista de candidatos
        pass

    def collect_feedback(self, retrieved_candidates: list[RetrievalCandidate]) -> dict:
        """
        Coleta feedback de utilidade apos o modelo produzir output.

        Para cada candidato RETRIEVE, verifica se was_referenced=True.
        Agrega por kind e atualiza utility_tracker.

        Args:
            retrieved_candidates: Lista de candidatos (alguns com was_referenced=True).

        Returns:
            {
                "total_retrieved": N,
                "total_referenced": N,
                "reference_rate": float,
                "tokens_spent": N,
                "tokens_wasted": N (tokens de itens nao referenciados),
                "utility_updates": {kind: (old_factor, new_factor)},
            }
        """
        # SEU CODIGO AQUI
        pass

    def get_retrieval_summary(self, candidates: list[RetrievalCandidate]) -> dict:
        """
        Sumario da decisao de recuperacao.

        Returns:
            {
                "total_candidates": N,
                "retrieved": N,
                "deferred": N,
                "skipped": N,
                "tokens_used": N,
                "tokens_remaining": N,
                "budget_utilization_pct": float,
                "avg_value_cost_ratio_retrieved": float,
            }
        """
        # SEU CODIGO AQUI
        pass


# ============================================================
# TESTES RAPIDOS: SelectionBudgetedRetriever
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("TESTE DO SELECTION-BUDGETED RETRIEVER")
    print("=" * 60)

    # Configurar sistema
    ticket_tags = ["payment", "timeout", "gateway", "production"]
    utility = UtilityTracker()
    predictor = InformationValuePredictor(
        utility_tracker=utility,
        ticket_topic_tags=ticket_tags,
    )
    budget = RetrievalBudget(
        total_budget=8000,
        harness_reserved=2000,
        tail_anchor_reserved=1000,
    )
    retriever = SelectionBudgetedRetriever(
        predictor=predictor,
        budget=budget,
        utility_tracker=utility,
    )

    # Construir candidatos
    candidates = []
    for cid, kind_str, cost, sim, tags, recency in RETRIEVAL_CANDIDATES:
        candidates.append(RetrievalCandidate(
            candidate_id=cid,
            kind=ContextKind(kind_str),
            token_cost=cost,
            similarity_score=sim,
            topic_tags=tags,
            recency_hours=recency,
        ))

    # Teste 1: InformationValuePredictor — topic match bonus
    print(f"\nTeste 1: Topic match bonus")
    cand = RetrievalCandidate(
        candidate_id="test", kind=ContextKind.ERROR_LOG,
        token_cost=100, similarity_score=0.90,
        topic_tags=["payment", "timeout", "gateway"], recency_hours=0.1,
    )
    value = predictor.predict_value(cand)
    print(f"  Candidato com 3 topic matches: similarity=0.90, bonus=1.5, utility=0.50")
    print(f"  Predicted value: {value:.3f} (esperado ~0.675)")
    assert abs(value - 0.675) < 0.01, f"Valor esperado 0.675, obtido {value:.3f}"
    print("  OK: topic match bonus aplicado")

    # Teste 2: InformationValuePredictor — sem topic match bonus
    cand_no_match = RetrievalCandidate(
        candidate_id="test2", kind=ContextKind.CUSTOMER_HISTORY,
        token_cost=100, similarity_score=0.90,
        topic_tags=["account", "premium"], recency_hours=48.0,
    )
    value_no_bonus = predictor.predict_value(cand_no_match)
    print(f"\nTeste 2: Sem topic match bonus (0 tags em comum)")
    print(f"  Predicted value: {value_no_bonus:.3f} (esperado ~0.450)")
    assert abs(value_no_bonus - 0.450) < 0.01, f"Valor esperado 0.450, obtido {value_no_bonus:.3f}"
    print("  OK: sem bonus, apenas similarity * utility")

    # Teste 3: Ranking por value/cost ratio
    print(f"\nTeste 3: Ranking de candidatos por value/cost ratio")
    ranked = predictor.rank_candidates(candidates)
    print(f"  Top 5 candidatos por value/cost ratio:")
    for c in ranked[:5]:
        print(f"    {c.candidate_id}: kind={c.kind.value}, v/c={c.value_cost_ratio:.4f}, "
              f"tokens={c.token_cost}, value={c.predicted_value:.3f}")
    # Verificar que esta ordenado
    for i in range(len(ranked) - 1):
        assert ranked[i].value_cost_ratio >= ranked[i+1].value_cost_ratio, (
            f"Ranking deve ser decrescente: {ranked[i].value_cost_ratio:.5f} < {ranked[i+1].value_cost_ratio:.5f}"
        )
    print("  OK: ranking ordenado decrescentemente")

    # Teste 4: Retrieval budget-aware
    print(f"\nTeste 4: Recuperacao budget-aware (budget={budget.retrieval_budget} tokens)")
    result = retriever.retrieve(candidates)
    summary = retriever.get_retrieval_summary(result)
    print(f"  Total candidates: {summary['total_candidates']}")
    print(f"  Retrieved: {summary['retrieved']}")
    print(f"  Deferred: {summary['deferred']}")
    print(f"  Skipped: {summary['skipped']}")
    print(f"  Tokens used: {summary['tokens_used']}")
    print(f"  Tokens remaining: {summary['tokens_remaining']}")
    print(f"  Budget utilization: {summary['budget_utilization_pct']:.1f}%")
    assert summary['tokens_used'] <= budget.retrieval_budget, (
        f"Tokens usados ({summary['tokens_used']}) nao devem exceder orcamento ({budget.retrieval_budget})"
    )
    print("  OK: orcamento respeitado")

    # Teste 5: Utility feedback loop
    print(f"\nTeste 5: Utility feedback loop")
    # Simular que alguns itens foram referenciados
    for c in result:
        if c.decision == RetrievalDecision.RETRIEVE and c.kind in (ContextKind.ERROR_LOG, ContextKind.PAST_DECISION):
            # Metade dos error_logs e past_decisions foram uteis
            if hash(c.candidate_id) % 2 == 0:
                c.was_referenced = True

    feedback = retriever.collect_feedback(result)
    print(f"  Retrieved: {feedback['total_retrieved']}")
    print(f"  Referenced: {feedback['total_referenced']}")
    print(f"  Reference rate: {feedback['reference_rate']:.1%}")
    print(f"  Tokens spent: {feedback['tokens_spent']}")
    print(f"  Tokens wasted: {feedback['tokens_wasted']}")
    print(f"  Utility updates:")
    for kind, (old, new) in feedback['utility_updates'].items():
        direction = "↑" if new > old else "↓" if new < old else "→"
        print(f"    {kind}: {old:.2f} {direction} {new:.2f}")

    # Verificar que utility factors foram atualizados
    assert feedback['total_referenced'] > 0, "Alguns itens deveriam ser referenciados"
    assert len(feedback['utility_updates']) > 0, "Deve haver atualizacoes de utility"
    print("  OK: feedback loop funcionando")

    # Teste 6: Sistema guloso vs. budget-aware
    print(f"\nTeste 6: Comparacao — Guloso vs. Budget-Aware")
    greedy_retrieved = [c for c in candidates if c.similarity_score > 0.70]
    greedy_tokens = sum(c.token_cost for c in greedy_retrieved)
    print(f"  Guloso (similarity > 0.70):")
    print(f"    Candidatos: {len(greedy_retrieved)}")
    print(f"    Tokens: {greedy_tokens}")
    print(f"    Excede orcamento: {'SIM' if greedy_tokens > budget.retrieval_budget else 'NAO'}")
    print(f"  Budget-Aware (value/cost ranking):")
    print(f"    Candidatos: {summary['retrieved']}")
    print(f"    Tokens: {summary['tokens_used']}")
    print(f"    Excede orcamento: {'SIM' if summary['tokens_used'] > budget.retrieval_budget else 'NAO'}")

    assert summary['tokens_used'] <= budget.retrieval_budget, "Budget-aware nunca excede orcamento"
    assert greedy_tokens > summary['tokens_used'], (
        "Guloso deveria consumir mais tokens que budget-aware"
    )
    print("  OK: budget-aware consome menos tokens e respeita orcamento")

    # Teste 7: Utility decay apos sessao
    print(f"\nTeste 7: Utility decay para kinds nao usados")
    old_runbook = utility.get(ContextKind.RUNBOOK)
    old_customer = utility.get(ContextKind.CUSTOMER_HISTORY)
    used_kinds = {ContextKind.ERROR_LOG, ContextKind.PAST_DECISION}
    utility.apply_decay(used_kinds)
    new_runbook = utility.get(ContextKind.RUNBOOK)
    new_customer = utility.get(ContextKind.CUSTOMER_HISTORY)
    print(f"  RUNBOOK: {old_runbook:.2f} → {new_runbook:.2f}")
    print(f"  CUSTOMER_HISTORY: {old_customer:.2f} → {new_customer:.2f}")
    assert new_runbook < old_runbook, "Kind nao usado deve sofrer decay"
    assert new_customer < old_customer, "Kind nao usado deve sofrer decay"
    print("  OK: decay aplicado a kinds nao usados")

    print("\n" + "=" * 60)
    print("TODOS OS TESTES DO SELECTION-BUDGETED RETRIEVER PASSARAM")
    print("=" * 60)
```

---

### Parte 3: Simular Multiplas Sessoes com Feedback Loop (35 min)

Agora execute o recuperador sobre multiplas sessoes e observe como o feedback loop melhora a qualidade das recuperacoes:

```python
# ============================================================
# SIMULACAO: 5 sessoes de suporte com feedback loop
# ============================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("SIMULACAO: 5 SESSOES COM FEEDBACK LOOP")
    print("=" * 60)

    # Utility tracker compartilhado entre sessoes
    utility = UtilityTracker()
    ticket_tags = ["payment", "timeout", "gateway", "production"]

    # Simular 5 sessoes com o mesmo batch de candidatos
    # Em cada sessao, o modelo referencia apenas error_logs e past_decisions
    # (runbooks e customer_history sao consistentemente ignorados)
    session_results = []

    for session in range(1, 6):
        predictor = InformationValuePredictor(
            utility_tracker=utility,
            ticket_topic_tags=ticket_tags,
        )
        budget = RetrievalBudget(8000, 2000, 1000)
        retriever = SelectionBudgetedRetriever(predictor, budget, utility)

        # Construir candidatos frescos a cada sessao
        candidates = []
        for cid, kind_str, cost, sim, tags, recency in RETRIEVAL_CANDIDATES:
            candidates.append(RetrievalCandidate(
                candidate_id=cid,
                kind=ContextKind(kind_str),
                token_cost=cost,
                similarity_score=sim,
                topic_tags=tags,
                recency_hours=recency,
            ))

        # Recuperar
        result = retriever.retrieve(candidates)

        # Simular feedback: apenas error_logs e past_decisions sao uteis
        for c in result:
            if c.decision == RetrievalDecision.RETRIEVE:
                if c.kind in (ContextKind.ERROR_LOG, ContextKind.PAST_DECISION):
                    c.was_referenced = True
                # runbooks e customer_history nunca sao referenciados

        feedback = retriever.collect_feedback(result)

        # Aplicar decay aos kinds nao usados
        utility.apply_decay({ContextKind.ERROR_LOG, ContextKind.PAST_DECISION})

        session_results.append({
            "session": session,
            "retrieved": feedback['total_retrieved'],
            "referenced": feedback['total_referenced'],
            "reference_rate": feedback['reference_rate'],
            "tokens_wasted": feedback['tokens_wasted'],
            "utility_error_log": utility.get(ContextKind.ERROR_LOG),
            "utility_past_decision": utility.get(ContextKind.PAST_DECISION),
            "utility_runbook": utility.get(ContextKind.RUNBOOK),
            "utility_customer_history": utility.get(ContextKind.CUSTOMER_HISTORY),
        })

    # Relatorio de evolucao
    print(f"\nEVOLUCAO DOS UTILITY FACTORS AO LONGO DAS SESSOES:")
    print(f"{'Session':<10} {'ErrLog':<10} {'PastDec':<10} {'Runbook':<10} {'CustHist':<10} {'RefRate':<10}")
    print("-" * 60)
    for r in session_results:
        print(f"{r['session']:<10} "
              f"{r['utility_error_log']:<10.2f} "
              f"{r['utility_past_decision']:<10.2f} "
              f"{r['utility_runbook']:<10.2f} "
              f"{r['utility_customer_history']:<10.2f} "
              f"{r['reference_rate']:<10.1%}")

    # Verificar que utility factors convergiram
    first = session_results[0]
    last = session_results[-1]

    print(f"\nCONVERGENCIA DOS UTILITY FACTORS:")
    print(f"  ERROR_LOG:        {first['utility_error_log']:.2f} → {last['utility_error_log']:.2f} "
          f"({'↑' if last['utility_error_log'] > first['utility_error_log'] else '↓'})")
    print(f"  PAST_DECISION:    {first['utility_past_decision']:.2f} → {last['utility_past_decision']:.2f} "
          f"({'↑' if last['utility_past_decision'] > first['utility_past_decision'] else '↓'})")
    print(f"  RUNBOOK:          {first['utility_runbook']:.2f} → {last['utility_runbook']:.2f} "
          f"({'↓'})")
    print(f"  CUSTOMER_HISTORY: {first['utility_customer_history']:.2f} → {last['utility_customer_history']:.2f} "
          f"({'↓'})")

    assert last['utility_error_log'] > first['utility_error_log'], (
        "ERROR_LOG utility deve subir (e consistentemente referenciado)"
    )
    assert last['utility_runbook'] < first['utility_runbook'], (
        "RUNBOOK utility deve cair (nunca referenciado)"
    )
    assert last['utility_customer_history'] < first['utility_customer_history'], (
        "CUSTOMER_HISTORY utility deve cair (nunca referenciado)"
    )

    print(f"\nCOMPARACAO FINAL:")
    print(f"  Sessao 1 — Todos os kinds com utility=0.50 (neutro)")
    print(f"    Reference rate: {first['reference_rate']:.1%}")
    print(f"    Tokens wasted: {first['tokens_wasted']}")
    print(f"  Sessao 5 — Utility factors calibrados pelo feedback")
    print(f"    Reference rate: {last['reference_rate']:.1%}")
    print(f"    Tokens wasted: {last['tokens_wasted']}")

    if last['reference_rate'] > first['reference_rate']:
        print(f"\n  O feedback loop MELHOROU a taxa de referencia em "
              f"{(last['reference_rate'] - first['reference_rate']) * 100:.0f}pp.")
        print(f"  Runbooks e customer_history — consistentemente ignorados —")
        print(f"  tiveram seus utility factors reduzidos, fazendo com que")
        print(f"  o recuperador priorizasse error_logs e past_decisions.")
    else:
        print(f"\n  NOTA: A taxa de referencia pode nao melhorar monotonicamente")
        print(f"  se os candidatos disponiveis nao mudam entre sessoes. O ponto")
        print(f"  e que tokens estao sendo gastos onde ha EVIDENCIA de utilidade.")

    print(f"\nCONCLUSÃO:")
    print(f"  O Selection-Budgeted Retrieval transformou o retrieval de um")
    print(f"  processo guloso (recuperar tudo que parece similar) em um")
    print(f"  processo budget-aware (recuperar o que maximiza valor/token).")
    print(f"  O feedback loop aprendeu quais tipos de contexto o modelo")
    print(f"  realmente usa, reduzindo o desperdicio de tokens em near-misses.")
    print(f"  O orcamento de tokens — o recurso mais escasso do agente —")
    print(f"  foi alocado onde gera mais valor.")
```

---

## Entregaveis

- Implementacao de `InformationValuePredictor` com topic match bonus e utility factor.
- `SelectionBudgetedRetriever` com cost-benefit ranking e budget enforcement.
- `UtilityTracker` com feedback loop e decay.
- Simulacao de 5 sessoes demonstrando convergencia dos utility factors.
- Comparacao: sistema guloso vs. budget-aware.

## Validacao: Criterios de Aceitacao

Seu codigo sera considerado **APROVADO** quando:

### Criterio 1: Diagnostico (Parte 1)

- [ ] Voce calculou o token cost total do sistema guloso e a violacao do orcamento
- [ ] Voce identificou os near-misses (alta similaridade, baixo topic match)
- [ ] Voce simulou o cost-benefit ranking manualmente e listou RETRIEVE/DEFER/SKIP
- [ ] Voce comparou a reducao de tokens entre guloso e budget-aware

### Criterio 2: Information Value Predictor

- [ ] `predict_value()` aplica topic_match_bonus (1.5x) quando >= 2 tags em comum
- [ ] `predict_value()` usa utility_factor do kind correto
- [ ] `rank_candidates()` ordena por value/cost ratio decrescente
- [ ] Candidatos com mesmo value/cost ratio tem ordem estavel

### Criterio 3: Budget Enforcement

- [ ] `RetrievalBudget.consume()` so permite consumo se houver orcamento
- [ ] Tokens usados em `RETRIEVE` nunca excedem `retrieval_budget`
- [ ] Candidatos que nao cabem no orcamento sao marcados como `DEFER`
- [ ] Candidatos abaixo de `MIN_VALUE_COST_RATIO` sao marcados como `SKIP`

### Criterio 4: Retrieval Decisions

- [ ] `RETRIEVE`: value/cost ratio alto + cabe no orcamento
- [ ] `DEFER`: value/cost ratio aceitavel mas sem orcamento
- [ ] `SKIP`: value/cost ratio abaixo do threshold ou valor negligivel
- [ ] `get_retrieval_summary()` reporta contagens e utilizacao corretamente

### Criterio 5: Utility Feedback Loop

- [ ] `UtilityTracker.record_usage()` aumenta utility factor do kind referenciado
- [ ] `UtilityTracker.apply_decay()` reduz utility factors dos kinds nao usados
- [ ] Utility factors nunca saem do intervalo [0.10, 1.00]
- [ ] `collect_feedback()` agrega por kind e reporta tokens desperdicados

### Criterio 6: Simulacao

- [ ] 5 sessoes produzem convergencia dos utility factors
- [ ] ERROR_LOG e PAST_DECISION (consistentemente uteis) tem utility factors crescentes
- [ ] RUNBOOK e CUSTOMER_HISTORY (nunca uteis) tem utility factors decrescentes
- [ ] Tokens wasted reportados corretamente a cada sessao

---

## Rubrica de Avaliacao

| Criterio | Peso | Insuficiente (0-3) | Basico (4-6) | Proficiente (7-8) | Excelente (9-10) |
|---|---|---|---|---|---|
| **Diagnostico (Parte 1)** | 15% | Nao identificou o problema do retrieval guloso | Identificou parcialmente sem calcular tokens | Diagnostico completo com near-miss analysis | Diagnostico + analise de sensibilidade do budget |
| **Predictor + Retriever (Parte 2)** | 40% | Funcoes core nao implementadas | Implementa mas erra em edge cases (budget, ranking) | Predictor e retriever funcionais com budget enforcement | Sistema completo + utility tracker + feedback loop |
| **Simulacao (Parte 3)** | 30% | Nao executou a simulacao | Simulacao parcial sem convergencia | 5 sessoes com convergencia visivel dos utility factors | Simulacao + analise da trajetoria de convergencia + calibracao de thresholds |
| **Testes e verificacao** | 15% | Nenhum cenario passa | 3 criterios passam | 5 criterios passam | Todos os 6 criterios passam |

**Nota final:** Media ponderada. **Aprovacao:** >= 7.0

---

## Dicas para Implementacao

### Para o Information Value Predictor

1. **Value/Cost ratio, nao value absoluto.** Um runbook de 1,200 tokens com predicted_value=0.95 pode parecer valioso, mas seu ratio e 0.0008/token. Uma decision de 150 tokens com predicted_value=0.85 tem ratio de 0.0057/token — 7x melhor. O ratio captura a eficiencia do investimento.

2. **O topic match bonus e o antidoto contra near-misses.** Similaridade semantica (embedding) retorna "o que e parecido". Topic match verifica "o que e relevante para este ticket". Um customer_history com similarity=0.85 e zero topic matches e provavelmente um near-miss — o embedding achou similar, mas os topicos revelam que e irrelevante.

3. **Utility factor e a memoria do sistema.** No inicio (utility=0.50), o sistema e neutro — confia igualmente em todos os kinds. Conforme o feedback chega, kinds uteis sobem e kinds inuteis caem. Isso e aprendizado por reforco simples: a recompensa e "foi referenciado".

### Para o Budget Enforcement

1. **O orcamento e um hard constraint, nao um soft target.** Se o budget e 5,000 tokens, o recuperador nunca recupera 5,001. Isso e diferente de "tente ficar abaixo de 5,000" — e um limite rigido porque cada token recuperado compete com tokens de raciocinio.

2. **DEFER nao e SKIP.** DEFER significa "esse candidato tem valor, mas nao coube no orcamento deste passo — tente de novo no proximo". SKIP significa "esse candidato tem valor/custo tao baixo que nao vale a pena revisitar". A distincao importa para o loop de controle do agente.

3. **O harness e tail anchors sao reservas inegociaveis.** O harness prompt (2,000 tokens) e o tail anchor (1,000 tokens) sao essenciais para o funcionamento do agente. O orcamento de recuperacao e o que sobra depois dessas reservas — nunca invada as reservas.

### Para o Utility Feedback Loop

1. **Feedback e observavel, nao estimado.** `was_referenced` nao e uma predicao — e uma observacao. Depois que o modelo produz output, o sistema verifica quais `context_id`s aparecem no raciocinio do modelo (citacoes, referencias explicitas). Isso e ground truth.

2. **O decay e necessario para evitar overfitting.** Se um kind foi util na sessao 1 mas nunca mais, seu utility factor deve cair. Sem decay, o sistema acumularia vieses de sessoes antigas que nao refletem o comportamento atual do modelo.

3. **O decay de 5% e conservador.** Um kind precisa de ~14 sessoes sem uso para cair de 1.0 para 0.5. Isso evita que o sistema abandone um kind util por falta de uso em 2-3 sessoes. Ajuste o decay rate conforme a volatilidade do dominio.

---

## Duvidas Comuns

**P: Isso nao vai fazer o sistema parar de recuperar runbooks completamente?**
R: Nao. O utility factor tem piso de 0.10. Mesmo que runbooks nunca sejam referenciados, eles ainda tem 20% do valor inicial. Alem disso, o decay so se aplica a sessoes onde o kind nao foi usado — se um runbook voltar a ser util, o utility factor sobe rapidamente (boost de 0.10 por sessao).

**P: Como isso se relaciona com o Explicit Token Budget Ledger?**
R: O Explicit Token Budget Ledger define o orcamento total e as fases (green/yellow/orange/red). O Selection-Budgeted Retrieval e o componente que opera DENTRO do orcamento definido pelo ledger. O ledger diz "voce tem 5,000 tokens para recuperacao neste passo". O retriever decide COMO gastar esses 5,000 tokens.

**P: O que acontece se o modelo referencia um item que foi SKIP?**
R: Isso e um sinal de que o MIN_VALUE_COST_RATIO ou o topic_match_bonus precisa de calibracao. O sistema pode registrar esse evento como "false negative" e ajustar os thresholds. Em producao, voce pode adicionar um mecanismo de "recuperacao de emergencia": se o modelo explicitamente pede um contexto que foi skipped, recupera-lo sob demanda.

**P: Como medir `was_referenced` em um sistema real?**
R: Depende da implementacao. Opcoes: (a) o modelo cita o `context_id` no output (ex: "conforme [mem-042]..."), (b) o modelo referencia o conteudo textualmente (ex: "o log de erro mostrava timeout..."), (c) heuristica de overlap entre o output e o conteudo recuperado. A opcao (a) e a mais confiavel se o modelo for instruido a citar fontes.

**P: Isso nao adiciona latencia? Ranquear 25 candidatos toda vez.**
R: O ranking de 25 candidatos e O(N log N) com N=25 — microssegundos. O custo real e a inferencia do modelo (segundos). O overhead do ranking e negligenciavel comparado ao beneficio de evitar injetar 30,000 tokens de contexto que o modelo vai ignorar.

---

## Proximo Passo

Depois de completar este exercicio:
1. Leia `[[docs/canonical/explicit-token-budget-ledger|Explicit Token Budget Ledger]]` e entenda como o orcamento de recuperacao se integra com o ledger de orcamento mais amplo do agente.
2. Leia `[[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]` — o catalogo de memoria enderecavel e a fonte dos candidatos que o Selection-Budgeted Retriever ranqueia.
3. (Opcional) Estenda o sistema com `ContextualBudgetAllocator`: um modulo que ajusta o `retrieval_budget` dinamicamente baseado na fase do agente (fase de exploracao → mais budget para retrieval; fase de execucao → menos).

---

*Exercicio Selection-Budgeted Retrieval | Nivel 3 - Arquitetura Avancada*

**Recuperacao nao e gratuita. Cada token recuperado compete com o raciocinio do modelo. Gaste tokens onde ha evidencia de valor.**
