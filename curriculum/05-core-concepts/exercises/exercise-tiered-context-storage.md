---
title: "Exercicio: Implementar Tiered Context Storage com Promocao e Democao"
type: exercise
level: "N3"
aliases: ["tiered context storage", "three-tier storage", "hot warm cold", "promotion demotion engine", "context tier orchestration", "tiered memory architecture"]
tags: [curriculo-conteudo, context-engineering, agentes-orquestracao, harness-engineering]
duration: "2-3h"
relates-to: ["[[docs/analysis/2026-06-18-memory-selection-problem/2026-06-18-memory-selection-problem-patterns|Memory Selection Patterns]]", "[[docs/analysis/2026-06-18-memory-selection-problem/2026-06-18-memory-selection-problem-classification|Memory Selection Classification]]", "[[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation]]", "[[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]", "[[docs/canonical/external-state-persistence|External State Persistence]]"]
last_updated: 2026-06-18
---
# Exercicio: Implementar Tiered Context Storage com Promocao e Democao
## Nivel 3 - Arquitetura Avancada

## Objetivo

Implementar um sistema de armazenamento de contexto em tres tiers (hot/warm/cold) com promocao e democao baseadas em relevancia, prefetch preditivo e politicas de latencia por tier.

**Tempo Estimado:** 2-3 horas
**Dificuldade:** Avancado
**Pre-requisito:** Ter lido `[[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation]]`, `[[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]` e `[[docs/canonical/external-state-persistence|External State Persistence]]`
**Objetivo:** Implementar um `TieredContextStore` com tres tiers de armazenamento, um `TierOrchestrator` que promove/demote unidades de contexto por relevancia, e um `PrefetchPredictor` que antecipa necessidades futuras de contexto.

---

## Prologo: O Agente Que Afogava em Contexto

### Segunda-feira, 9h15. Sala de operacao.

```
SRE LEAD: "O agente de diagnostico de incidentes esta esgotando
          o context window em 40 minutos. A gente bota tudo no
          prompt — logs, traces, runbooks, historico do incidente.
          No comeco funciona bem, mas conforme o incidente cresce,
          ele perde o fio."
```

O agente `IncidentResponder` tinha um design simples: todo contexto era mantido na janela ativa. Quando um incidente abria, o agente carregava logs recentes, traces de dependencias e o runbook. Conforme novas evidencias chegavam — mais logs, mais traces, outputs de ferramentas — tudo era concatenado no prompt.

Funcionava para incidentes de 15 minutos. Mas incidentes complexos duravam horas. Em 40 minutos, a janela estava 85% ocupada por evidencias de 2 horas atras que o modelo ja nao conseguia atender. O agente comecava a repetir diagnoticos, ignorar novas evidencias, e sugerir acoes ja tentadas.

```
═══════════════════════════════════════════════════════════════
        POSTMORTEM — INCIDENTE #1247 (4h12m de duracao)
═══════════════════════════════════════════════════════════════

JANELA ATIVA AO FINAL:
  Tokens totais:          127,000 / 128,000 (99.2%)
  Tokens uteis (atendidos): ~18,000 / 128,000 (14%)
  Tokens obsoletos:        ~85,000 (66%)

  Evidencias das primeiras 2h ainda ocupavam 66% da janela.
  O modelo so conseguia atender aos ~18k tokens mais recentes.
  Diagnoticos repetidos: 7 ciclos identicos nas ultimas 2h.

CAUSA RAIZ:
  O agente tratava a janela de contexto como um deposito infinito.
  Nao havia distincao entre o que o modelo precisa AGORA (hot),
  o que pode ser util em breve (warm), e o que e historico (cold).
  Sem tiers, todo contexto compete pelo mesmo espaco finito.
═══════════════════════════════════════════════════════════════
```

```
ARQUITETA (post-mortem): "O problema e estrutural. A janela de contexto
                          tem tamanho fixo, mas o agente age como se
                          fosse infinita. O que faltava: tres tiers de
                          armazenamento com politicas claras de promocao
                          e democao. Hot: o que o modelo esta raciocinando
                          agora. Warm: contexto recente, acessivel com
                          baixa latencia. Cold: historico completo,
                          acessivel sob demanda. O orquestrador move
                          contexto entre tiers conforme a relevancia muda."
```

**O que teria evitado tudo:**

> Tiered Context Storage with Promotion/Demotion: tres tiers (hot/warm/cold) com politicas de movimento baseadas em relevancia. O hot tier mantem apenas o que o modelo precisa para o passo atual. Contexto que perde relevancia e demovido para warm; contexto que volta a ser relevante e promovido de cold para hot. O resultado: a janela ativa permanece deliberadamente pequena, independente da duracao da sessao.

**Sua missao:** Construir um `TieredContextStore` que implementa exatamente essa arquitetura de tres tiers.

---

## Cenario: Agente de Diagnostico com Contexto em Tres Tiers

### Contexto

Voce e o engenheiro de plataforma responsavel pelo agente `IncidentResponder` da **MercuryPay**. Durante um incidente, o agente gera unidades de contexto continuamente:

| Tipo de Contexto | Exemplo | Tamanho tipico |
|---|---|---|
| `log_entry` | Linha de log de erro | 200 tokens |
| `trace_span` | Span de tracing distribuido | 500 tokens |
| `tool_output` | Resultado de query no banco | 800 tokens |
| `agent_decision` | "Reiniciar instancia us-east-1" | 150 tokens |
| `runbook_step` | Passo do runbook executado | 300 tokens |
| `evidence_snapshot` | Estado do sistema em t0 | 2000 tokens |

Cada unidade de contexto tem um ciclo de vida: nasce no hot tier (janela ativa), perde relevancia com o tempo e e demovida para warm, e eventualmente migra para cold storage (historico completo). Quando uma evidencia antiga volta a ser relevante — por exemplo, um log da primeira hora que explica um erro que reapareceu na quarta hora — o sistema promove de cold para hot.

### Arquitetura de Tres Tiers

```
┌─────────────────────────────────────────────────────────────┐
│ HOT TIER (in-memory cache)                                   │
│ Latencia: < 1ms                                              │
│ Capacidade: 16,000 tokens (12.5% de janela de 128K)         │
│ Conteudo: contexto do passo atual + head/tail anchors        │
│ Politica: LRU com protecao de head/tail anchors              │
└────────────────────────────┬────────────────────────────────┘
                             │ democao (relevancia cai)
                             ▼
┌─────────────────────────────────────────────────────────────┐
│ WARM TIER (NVMe-backed store)                                │
│ Latencia: ~1ms                                               │
│ Capacidade: 64,000 tokens (50% da janela)                   │
│ Conteudo: contexto das ultimas N decisoes, acessivel rapido  │
│ Politica: LRU; promove para hot sob demanda                  │
└────────────────────────────┬────────────────────────────────┘
                             │ democao (relevancia minima)
                             ▼
┌─────────────────────────────────────────────────────────────┐
│ COLD TIER (object storage)                                   │
│ Latencia: ~100ms                                             │
│ Capacidade: ilimitada (historico completo da sessao)         │
│ Conteudo: todas as unidades de contexto desde t0             │
│ Politica: promove para warm via prefetch preditivo           │
└─────────────────────────────────────────────────────────────┘
```

### Dados de Entrada

Voce recebe uma sessao de incidente com 40 unidades de contexto geradas ao longo de 3 horas. Cada unidade tem:

```json
{
  "unit_id": "CTX-0042",
  "kind": "log_entry",
  "content": "ERROR: Connection timeout to payments-db (attempt 3/3)",
  "token_count": 85,
  "timestamp": "2026-06-18T09:23:15Z",
  "relevance_tags": ["database", "timeout", "payment-processing"],
  "task_step": 3,
  "referenced_by": ["CTX-0051", "CTX-0078"]
}
```

O campo `referenced_by` indica quais outras unidades de contexto referenciaram esta — uma medida observavel de relevancia. O campo `task_step` indica em qual passo do diagnostico a unidade foi gerada. O passo atual do agente e `task_step=12`.

---

## Requisitos

### Requisitos Funcionais

1. **RF1 - Tres tiers com politicas de capacidade:** Hot tier limitado a 16,000 tokens com protecao de head/tail anchors. Warm tier limitado a 64,000 tokens com LRU. Cold tier ilimitado.
2. **RF2 - Democao por relevancia:** Quando o hot tier excede a capacidade, o orquestrador demove as unidades de menor relevancia para warm. Quando warm excede, demove as menos relevantes para cold.
3. **RF3 - Promocao sob demanda:** Quando o agente referencia uma unidade que esta em warm ou cold, o orquestrador promove essa unidade para hot (e possivelmente unidades relacionadas).
4. **RF4 - Prefetch preditivo:** Antes de cada passo do agente, o `PrefetchPredictor` analisa o grafo de referencias e antecipa quais unidades em cold/warm serao necessarias, promovendo-as proativamente.
5. **RF5 - Score de relevancia:** Cada unidade de contexto tem um score de relevancia calculado como: `relevancy = recency_weight * recency_factor + reference_weight * reference_count + step_proximity_weight * (1 / (1 + |current_step - unit_step|))`. Pesos configuraveis.
6. **RF6 - Head/tail anchor protection:** As 3 unidades mais recentes (tail) e o runbook do passo atual (head) nunca sao demovidos do hot tier, independente do score de relevancia.

### Requisitos Tecnicos

1. **RT1 - Python puro:** Implementacao em Python com stdlib + dataclasses.
2. **RT2 - Simulacao de latencia:** Operacoes em cold tier reportam latencia de ~100ms; warm tier ~1ms; hot tier < 1ms. Use constantes, nao precisa de threads reais.
3. **RT3 - Operacoes atomicas:** Promocao e democao sao operacoes atomicas — nunca deixam uma unidade em estado inconsistente entre dois tiers.
4. **RT4 - Determinismo:** Dado o mesmo estado inicial e mesma sequencia de operacoes, o orquestrador produz o mesmo estado final.

---

## Sua Tarefa

Voce vai implementar o `TieredContextStore` em 3 partes.

---

### Parte 1: Diagnosticar o Colapso da Janela Unica (15 min)

Analise o log de 40 unidades de contexto da sessao de incidente abaixo. Identifique:

1. Quais unidades ocupavam o hot tier no momento do colapso (task_step=12) se o sistema tivesse usado janela unica (todas as 40 unidades na ativa)?
2. Quantas dessas unidades seriam demovidas para warm/cold se o sistema tivesse usado tiered storage com hot tier de 16,000 tokens?
3. Quais unidades em cold storage deveriam ser promovidas para hot no task_step=12 baseado no grafo de referencias?

```python
# Log simulado de 40 unidades de contexto durante incidente #1247
# Formato: (unit_id, kind, token_count, task_step, referenced_by_list)
# referenced_by_list: IDs de outras unidades que referenciaram esta

INCIDENT_CONTEXT_LOG = [
    # Hora 0-1: Fase de descoberta (task_steps 1-4)
    ("CTX-001", "runbook_step",   300, 1, ["CTX-005", "CTX-012"]),
    ("CTX-002", "log_entry",      200, 1, ["CTX-005"]),
    ("CTX-003", "trace_span",     500, 1, ["CTX-008", "CTX-015"]),
    ("CTX-004", "log_entry",       85, 1, ["CTX-005", "CTX-007"]),
    ("CTX-005", "agent_decision", 150, 2, ["CTX-010", "CTX-012", "CTX-025"]),
    ("CTX-006", "tool_output",    800, 2, ["CTX-010"]),
    ("CTX-007", "log_entry",      120, 2, ["CTX-010"]),
    ("CTX-008", "trace_span",     500, 2, ["CTX-015"]),
    ("CTX-009", "evidence_snapshot", 2000, 3, ["CTX-012", "CTX-020", "CTX-035"]),
    ("CTX-010", "agent_decision", 200, 3, ["CTX-012", "CTX-018"]),
    ("CTX-011", "log_entry",      180, 3, ["CTX-012"]),
    ("CTX-012", "agent_decision", 150, 4, ["CTX-018", "CTX-025"]),
    ("CTX-013", "tool_output",    700, 4, ["CTX-018"]),
    ("CTX-014", "log_entry",       90, 4, []),
    # Hora 1-2: Fase de investigacao (task_steps 5-8)
    ("CTX-015", "trace_span",     500, 5, ["CTX-020", "CTX-025"]),
    ("CTX-016", "log_entry",      200, 5, ["CTX-020"]),
    ("CTX-017", "tool_output",    800, 5, ["CTX-025"]),
    ("CTX-018", "agent_decision", 180, 6, ["CTX-020", "CTX-030"]),
    ("CTX-019", "log_entry",      150, 6, ["CTX-020"]),
    ("CTX-020", "agent_decision", 160, 7, ["CTX-025", "CTX-030"]),
    ("CTX-021", "trace_span",     400, 7, ["CTX-030"]),
    ("CTX-022", "evidence_snapshot", 1800, 7, ["CTX-025", "CTX-035"]),
    ("CTX-023", "log_entry",      110, 8, []),
    ("CTX-024", "tool_output",    600, 8, ["CTX-030"]),
    ("CTX-025", "agent_decision", 150, 8, ["CTX-030", "CTX-035", "CTX-040"]),
    # Hora 2-3: Fase de resolucao (task_steps 9-12)
    ("CTX-026", "log_entry",      200, 9, ["CTX-035"]),
    ("CTX-027", "trace_span",     450, 9, ["CTX-035"]),
    ("CTX-028", "tool_output",    750, 9, ["CTX-035"]),
    ("CTX-029", "log_entry",       95, 10, []),
    ("CTX-030", "agent_decision", 200, 10, ["CTX-035", "CTX-040"]),
    ("CTX-031", "trace_span",     500, 10, ["CTX-040"]),
    ("CTX-032", "log_entry",      180, 11, ["CTX-035", "CTX-040"]),
    ("CTX-033", "tool_output",    700, 11, ["CTX-040"]),
    ("CTX-034", "evidence_snapshot", 2000, 11, ["CTX-040"]),
    ("CTX-035", "agent_decision", 150, 11, ["CTX-040"]),
    ("CTX-036", "log_entry",      200, 12, ["CTX-040"]),
    ("CTX-037", "trace_span",     400, 12, ["CTX-040"]),
    ("CTX-038", "tool_output",    800, 12, ["CTX-040"]),
    ("CTX-039", "log_entry",      130, 12, []),
    ("CTX-040", "agent_decision", 250, 12, []),
]

# TAREFA: Responda no seu codigo como comentario:
#
# 1. Qual o total de tokens das 40 unidades?
#    Se a janela ativa tivesse 128,000 tokens, qual a ocupacao?
#
# 2. Se o hot tier e limitado a 16,000 tokens, quais unidades
#    estariam no hot tier no task_step=12?
#    (Dica: ordene por score de relevancia e preencha ate o limite)
#
# 3. Quais unidades em cold (task_steps 1-4) sao referenciadas
#    por unidades no task_step=12 direta ou indiretamente?
#    Estas deveriam ser promovidas via prefetch.
#
# 4. Compare o "working set" (unidades no hot tier) entre:
#    a. Janela unica: todas as 40 unidades competindo por atencao
#    b. Tiered storage: ~16,000 tokens das unidades mais relevantes
#    Qual a reducao percentual no volume de contexto?
```

---

### Parte 2: Implementar o TieredContextStore (70 min)

Implemente o sistema de tres tiers. Use este esqueleto:

```python
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Optional


# ============================================================
# DATA MODELS
# ============================================================

class StorageTier(Enum):
    HOT = "hot"     # in-memory, < 1ms
    WARM = "warm"   # NVMe, ~1ms
    COLD = "cold"   # object storage, ~100ms


class ContextKind(Enum):
    LOG_ENTRY = "log_entry"
    TRACE_SPAN = "trace_span"
    TOOL_OUTPUT = "tool_output"
    AGENT_DECISION = "agent_decision"
    RUNBOOK_STEP = "runbook_step"
    EVIDENCE_SNAPSHOT = "evidence_snapshot"


@dataclass
class ContextUnit:
    """Uma unidade de contexto gerada pelo agente."""
    unit_id: str
    kind: ContextKind
    content: str
    token_count: int
    timestamp: str
    relevance_tags: list[str] = field(default_factory=list)
    task_step: int = 0
    referenced_by: list[str] = field(default_factory=list)
    tier: StorageTier = StorageTier.HOT  # tier atual

    @property
    def reference_count(self) -> int:
        """Quantas outras unidades referenciaram esta."""
        return len(self.referenced_by)


# ============================================================
# TIER CAPACITY CONSTANTS
# ============================================================

HOT_TIER_TOKEN_CAPACITY = 16000
WARM_TIER_TOKEN_CAPACITY = 64000
# COLD tier: ilimitado

HEAD_TAIL_ANCHOR_COUNT = 3  # ultimas N unidades sao head/tail anchors

# Latencia simulada por tier (ms)
TIER_LATENCY_MS = {
    StorageTier.HOT: 0.5,
    StorageTier.WARM: 1.0,
    StorageTier.COLD: 100.0,
}

# Pesos do score de relevancia
DEFAULT_RELEVANCY_WEIGHTS = {
    "recency": 0.35,
    "reference_count": 0.40,
    "step_proximity": 0.25,
}


# ============================================================
# RELEVANCY SCORING
# ============================================================

def compute_relevancy_score(
    unit: ContextUnit,
    current_step: int,
    total_units: int,
    weights: dict[str, float] | None = None,
) -> float:
    """
    Calcula o score de relevancia de uma unidade de contexto.

    Formula:
      recency_factor = (unit.task_step / current_step)  # 1.0 se mais recente
      reference_factor = min(1.0, unit.reference_count / max_references)
      step_proximity = 1.0 / (1.0 + abs(current_step - unit.task_step))

      score = w_recency * recency_factor
            + w_reference * reference_factor
            + w_proximity * step_proximity

    Args:
        unit: Unidade de contexto.
        current_step: Passo atual do agente.
        total_units: Total de unidades no sistema (para normalizar reference_count).
        weights: Pesos configuraraveis.

    Returns:
        Score de relevancia em [0, 1].
    """
    # SEU CODIGO AQUI
    pass


# ============================================================
# TIERED CONTEXT STORE — nucleo do exercicio
# ============================================================

@dataclass
class TieredContextStore:
    """Armazenamento de contexto em tres tiers."""

    hot_units: dict[str, ContextUnit] = field(default_factory=dict)
    warm_units: dict[str, ContextUnit] = field(default_factory=dict)
    cold_units: dict[str, ContextUnit] = field(default_factory=dict)

    # Head/tail anchors: IDs das unidades que nunca sao demovidas do hot
    head_anchors: list[str] = field(default_factory=list)
    tail_anchors: list[str] = field(default_factory=list)

    # Contadores de tokens por tier
    hot_tokens: int = 0
    warm_tokens: int = 0

    def total_units(self) -> int:
        """Total de unidades em todos os tiers."""
        return len(self.hot_units) + len(self.warm_units) + len(self.cold_units)

    def all_unit_ids(self) -> set[str]:
        """Todos os IDs de unidades no sistema."""
        return set(self.hot_units) | set(self.warm_units) | set(self.cold_units)

    def get_unit(self, unit_id: str) -> ContextUnit | None:
        """
        Recupera uma unidade de qualquer tier.

        Retorna a unidade e o tier onde foi encontrada.
        """
        # SEU CODIGO AQUI
        pass

    def max_references(self) -> int:
        """Maior reference_count entre todas as unidades (para normalizacao)."""
        all_refs = [
            u.reference_count
            for u in list(self.hot_units.values())
            + list(self.warm_units.values())
            + list(self.cold_units.values())
        ]
        return max(all_refs) if all_refs else 1

    def insert(self, unit: ContextUnit) -> None:
        """
        Insere uma nova unidade no hot tier.

        Se o hot tier exceder a capacidade, dispara democao em cascata.
        """
        # SEU CODIGO AQUI
        pass

    def promote(self, unit_id: str) -> ContextUnit | None:
        """
        Promove uma unidade de warm/cold para hot.

        Se o hot tier estiver cheio, demove a unidade de menor
        relevancia (que nao seja head/tail anchor) para warm primeiro.

        Returns:
            A unidade promovida, ou None se nao encontrada.
        """
        # SEU CODIGO AQUI
        pass

    def demote_from_hot(self, current_step: int) -> list[str]:
        """
        Demove unidades do hot tier para warm/cold para liberar espaco.

        Regras:
        1. Head/tail anchors nunca sao demovidas
        2. Ordena as unidades restantes por score de relevancia (menor primeiro)
        3. Demove ate que hot_tokens <= HOT_TIER_TOKEN_CAPACITY
        4. Unidades com relevancia abaixo de WARM_THRESHOLD (0.15) vao direto para cold
        5. As demais vao para warm

        Returns:
            Lista de unit_ids que foram demovidos.
        """
        # SEU CODIGO AQUI
        pass

    def demote_from_warm(self, current_step: int) -> list[str]:
        """
        Demove unidades do warm tier para cold para liberar espaco.

        Similar ao demote_from_hot, mas sem protecao de anchors
        e sem threshold intermediario — tudo vai para cold.
        """
        # SEU CODIGO AQUI
        pass

    def get_hot_context_summary(self) -> dict:
        """
        Retorna um resumo do hot tier para monitoramento.

        Returns:
            {
                "total_units": N,
                "total_tokens": N,
                "capacity_pct": float,
                "anchor_count": N,
                "avg_relevancy": float,
            }
        """
        # SEU CODIGO AQUI
        pass


# ============================================================
# PREFETCH PREDICTOR
# ============================================================

@dataclass
class PrefetchPredictor:
    """
    Antecipa quais unidades em cold/warm serao necessarias
    no proximo passo do agente.

    Usa o grafo de referencias: se o passo atual referencia
    unidades X, Y, Z, o preditor busca unidades que X, Y, Z
    referenciam e que ainda nao estao no hot tier.
    """

    store: TieredContextStore

    def predict(self, current_step: int, lookahead_depth: int = 2) -> list[str]:
        """
        Prediz quais unidades devem ser promovidas para hot
        antes do proximo passo do agente.

        Algoritmo:
        1. Identificar unidades no hot tier que sao "fontes de referencia"
           (unidades com alto reference_count)
        2. Para cada fonte, seguir a cadeia de referenced_by ate lookahead_depth
        3. Coletar unidades alcancaveis que estao em warm ou cold
        4. Ordenar por score de relevancia e retornar os top candidatos
           que cabem no espaco restante do hot tier

        Args:
            current_step: Passo atual do agente.
            lookahead_depth: Profundidade de traversal no grafo de referencias.

        Returns:
            Lista de unit_ids a promover, ordenada por relevancia.
        """
        # SEU CODIGO AQUI
        pass


# ============================================================
# TIER ORCHESTRATOR — coordena insercoes, promocoes, democoes
# ============================================================

@dataclass
class TierOrchestrator:
    """Orquestrador que coordena o ciclo de vida do contexto nos tres tiers."""

    store: TieredContextStore
    predictor: PrefetchPredictor
    current_step: int = 1

    def ingest_context(self, unit: ContextUnit) -> dict:
        """
        Ciclo completo de ingestao de uma nova unidade de contexto.

        Fluxo:
        1. Inserir unidade no hot tier
        2. Atualizar head/tail anchors (manter as ultimas HEAD_TAIL_ANCHOR_COUNT)
        3. Se hot tier estourou: demover para warm/cold
        4. Registrar latencia da operacao

        Returns:
            Dicionario com log da operacao: {unit_id, latency_ms, demotions, tier_after}
        """
        # SEU CODIGO AQUI
        pass

    def step_forward(self, new_step: int) -> dict:
        """
        Avanca para o proximo passo do agente.

        Fluxo:
        1. Atualizar current_step
        2. Executar prefetch preditivo
        3. Promover unidades preditas para hot
        4. Ajustar hot tier se necessario

        Returns:
            Dicionario com: {step, prefetched_count, promoted_count, hot_tokens}
        """
        # SEU CODIGO AQUI
        pass

    def query_context(self, unit_id: str) -> tuple[ContextUnit | None, float]:
        """
        Recupera uma unidade de contexto de qualquer tier,
        promovendo-a para hot se necessario.

        Returns:
            (ContextUnit ou None, latencia_ms da operacao)
        """
        # SEU CODIGO AQUI
        pass

    def get_tier_distribution(self) -> dict:
        """
        Retorna a distribuicao atual de unidades e tokens por tier.

        Returns:
            {
                "hot": {"units": N, "tokens": N, "pct": float},
                "warm": {"units": N, "tokens": N, "pct": float},
                "cold": {"units": N, "tokens": N, "pct": float},
            }
        """
        # SEU CODIGO AQUI
        pass


# ============================================================
# TESTES RAPIDOS: TieredContextStore
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("TESTE DO TIERED CONTEXT STORE")
    print("=" * 60)

    # Teste 1: compute_relevancy_score — unidade recente e referenciada
    unit_recent = ContextUnit(
        unit_id="CTX-A",
        kind=ContextKind.AGENT_DECISION,
        content="decision",
        token_count=200,
        timestamp="2026-01-01T10:00:00Z",
        task_step=10,
        referenced_by=["CTX-B", "CTX-C", "CTX-D", "CTX-E"],
    )
    score = compute_relevancy_score(unit_recent, current_step=12, total_units=40)
    print(f"\nTeste 1: Relevancia de unidade recente e muito referenciada")
    print(f"  Score: {score:.3f}")
    assert score > 0.60, f"Unidade recente com 4 referencias deve ter score > 0.6, obtido {score:.3f}"
    print("  OK: score alto para unidade relevante")

    # Teste 2: compute_relevancy_score — unidade antiga sem referencias
    unit_old = ContextUnit(
        unit_id="CTX-Z",
        kind=ContextKind.LOG_ENTRY,
        content="log",
        token_count=90,
        timestamp="2026-01-01T08:00:00Z",
        task_step=1,
        referenced_by=[],
    )
    score_old = compute_relevancy_score(unit_old, current_step=12, total_units=40)
    print(f"\nTeste 2: Relevancia de unidade antiga sem referencias")
    print(f"  Score: {score_old:.3f}")
    assert score_old < 0.30, f"Unidade antiga sem referencias deve ter score < 0.3, obtido {score_old:.3f}"
    print("  OK: score baixo para unidade obsoleta")

    # Teste 3: Inserir unidades ate estourar hot tier
    store = TieredContextStore()
    orch = TierOrchestrator(store=store, predictor=PrefetchPredictor(store=store))

    print(f"\nTeste 3: Inserir 100 unidades de 200 tokens cada (20,000 tokens total)")
    for i in range(100):
        unit = ContextUnit(
            unit_id=f"CTX-{i:03d}",
            kind=ContextKind.LOG_ENTRY,
            content=f"log entry {i}",
            token_count=200,
            timestamp=f"2026-01-01T{(10 + i // 60):02d}:{i % 60:02d}:00Z",
            task_step=i // 10 + 1,
            referenced_by=[],
        )
        orch.ingest_context(unit)

    dist = orch.get_tier_distribution()
    print(f"  Hot:  {dist['hot']['units']} units, {dist['hot']['tokens']} tokens")
    print(f"  Warm: {dist['warm']['units']} units, {dist['warm']['tokens']} tokens")
    print(f"  Cold: {dist['cold']['units']} units, {dist['cold']['tokens']} tokens")
    assert dist['hot']['tokens'] <= HOT_TIER_TOKEN_CAPACITY, (
        f"Hot tier deve respeitar capacidade de {HOT_TIER_TOKEN_CAPACITY}"
    )
    assert dist['warm']['tokens'] <= WARM_TIER_TOKEN_CAPACITY, (
        f"Warm tier deve respeitar capacidade de {WARM_TIER_TOKEN_CAPACITY}"
    )
    assert dist['hot']['units'] + dist['warm']['units'] + dist['cold']['units'] == 100, (
        "Todas as 100 unidades devem estar em algum tier"
    )
    print("  OK: distribuicao entre tiers respeita capacidades")

    # Teste 4: Head/tail anchors sobrevivem a democao
    print(f"\nTeste 4: Head/tail anchors protegidos")
    anchor_ids = store.head_anchors + store.tail_anchors
    for aid in anchor_ids:
        assert aid in store.hot_units, f"Anchor {aid} deve permanecer no hot tier"
    print(f"  Anchors no hot: {len(anchor_ids)}")
    print(f"  OK: anchors protegidos da democao")

    # Teste 5: Promocao de unidade em cold para hot
    if store.cold_units:
        cold_id = next(iter(store.cold_units))
        print(f"\nTeste 5: Promover {cold_id} de cold para hot")
        unit, latency = orch.query_context(cold_id)
        assert unit is not None, f"Unidade {cold_id} deve ser encontrada"
        assert unit.tier == StorageTier.HOT, f"Unidade deve estar em hot apos promocao"
        assert latency >= TIER_LATENCY_MS[StorageTier.COLD], (
            f"Latencia deve ser >= {TIER_LATENCY_MS[StorageTier.COLD]}ms para cold"
        )
        print(f"  Unidade promovida: tier={unit.tier.value}, latencia={latency}ms")
        print(f"  OK: promocao com latencia correta")

    # Teste 6: Prefetch preditivo
    print(f"\nTeste 6: Prefetch preditivo")
    hot_before = len(store.hot_units)
    result = orch.step_forward(orch.current_step + 1)
    hot_after = len(store.hot_units)
    print(f"  Hot antes do prefetch: {hot_before} unidades")
    print(f"  Hot depois do prefetch: {hot_after} unidades")
    print(f"  Prefetch log: {result}")
    print(f"  OK: step_forward executado")

    print("\n" + "=" * 60)
    print("TODOS OS TESTES DO TIERED CONTEXT STORE PASSARAM")
    print("=" * 60)
```

---

### Parte 3: Simular a Sessao de Incidente com Tiered Storage (35 min)

Agora execute o orquestrador sobre o log de 40 unidades do incidente e compare com o cenario de janela unica:

```python
# ============================================================
# SIMULACAO: Incidente #1247 com Tiered Storage vs. Janela Unica
# ============================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("SIMULACAO: INCIDENTE #1247 — TIERED vs. JANELA UNICA")
    print("=" * 60)

    # Reconstruir unidades a partir do INCIDENT_CONTEXT_LOG
    store = TieredContextStore()
    orch = TierOrchestrator(store=store, predictor=PrefetchPredictor(store=store))

    all_units = []
    for unit_id, kind_str, tokens, step, refs in INCIDENT_CONTEXT_LOG:
        unit = ContextUnit(
            unit_id=unit_id,
            kind=ContextKind(kind_str),
            content=f"Content of {unit_id}",
            token_count=tokens,
            timestamp=f"2026-06-18T{8 + step // 4:02d}:{10 + (step * 7) % 60:02d}:00Z",
            task_step=step,
            referenced_by=refs,
        )
        all_units.append(unit)

    # Ingerir unidades passo a passo
    current_step = 1
    for unit in all_units:
        if unit.task_step > current_step:
            orch.step_forward(unit.task_step)
            current_step = unit.task_step
        orch.ingest_context(unit)

    # Estado final no task_step=12
    dist = orch.get_tier_distribution()
    print(f"\nDISTRIBUICAO FINAL (task_step=12):")
    print(f"  Hot:  {dist['hot']['units']:3d} units, {dist['hot']['tokens']:6d} tokens ({dist['hot']['pct']:.1f}%)")
    print(f"  Warm: {dist['warm']['units']:3d} units, {dist['warm']['tokens']:6d} tokens ({dist['warm']['pct']:.1f}%)")
    print(f"  Cold: {dist['cold']['units']:3d} units, {dist['cold']['tokens']:6d} tokens ({dist['cold']['pct']:.1f}%)")

    hot_summary = store.get_hot_context_summary()
    print(f"\nHOT TIER SUMMARY:")
    print(f"  Unidades: {hot_summary['total_units']}")
    print(f"  Tokens: {hot_summary['total_tokens']}")
    print(f"  Capacidade: {hot_summary['capacity_pct']:.1f}%")
    print(f"  Anchors: {hot_summary['anchor_count']}")

    # Comparacao com janela unica
    total_tokens = sum(u.token_count for u in all_units)
    print(f"\nCOMPARACAO: Tiered Storage vs. Janela Unica")
    print(f"  Janela unica: {len(all_units)} unidades, {total_tokens:,} tokens (100% na ativa)")
    print(f"  Tiered storage: {dist['hot']['units']} unidades no hot, "
          f"{dist['hot']['tokens']:,} tokens na ativa")
    print(f"  Reducao no contexto ativo: "
          f"{(1 - dist['hot']['tokens'] / total_tokens) * 100:.1f}%")

    # Verificar se unidades criticas estao no hot
    critical_refs = ["CTX-035", "CTX-040"]  # unidades do passo 11-12
    print(f"\nUNIDADES CRITICAS (task_steps 11-12):")
    for uid in critical_refs:
        unit = store.get_unit(uid)
        if unit:
            print(f"  {uid}: tier={unit.tier.value}, tokens={unit.token_count}, refs={unit.reference_count}")
        else:
            print(f"  {uid}: NOT FOUND")

    print(f"\nCONCLUSÃO:")
    print(f"  O Tiered Context Storage manteve o hot tier em ~{dist['hot']['tokens']:,} tokens,")
    print(f"  equivalente a {dist['hot']['pct']:.1f}% da capacidade. A janela unica teria")
    print(f"  ocupado {total_tokens:,} tokens — {total_tokens / dist['hot']['tokens']:.1f}x mais.")
    print(f"  O modelo no tiered storage atende a um conjunto pequeno e relevante.")
    print(f"  No modelo de janela unica, 66% do contexto seria ruido nao atendido.")
```

---

## Entregaveis

- Implementacao de `TieredContextStore` com tres tiers e controle de capacidade.
- `TierOrchestrator` coordenando promocao, democao e prefetch.
- `PrefetchPredictor` usando grafo de referencias para antecipar necessidades.
- Simulacao comparativa: tiered storage vs. janela unica.

## Validacao: Criterios de Aceitacao

Seu codigo sera considerado **APROVADO** quando:

### Criterio 1: Diagnostico (Parte 1)

- [ ] Voce calculou o total de tokens das 40 unidades e a ocupacao na janela unica
- [ ] Voce identificou quais unidades ocupariam o hot tier de 16,000 tokens no task_step=12
- [ ] Voce identificou as unidades em cold que deveriam ser promovidas baseado no grafo de referencias
- [ ] Voce comparou a reducao percentual no contexto ativo entre tiered e janela unica

### Criterio 2: Relevancia

- [ ] `compute_relevancy_score()` retorna scores altos (>0.6) para unidades recentes com muitas referencias
- [ ] `compute_relevancy_score()` retorna scores baixos (<0.3) para unidades antigas sem referencias
- [ ] O score e monotonicamente crescente com recencia e reference_count
- [ ] Pesos sao configuraveis e normalizados

### Criterio 3: Tiered Storage

- [ ] Hot tier respeita `HOT_TIER_TOKEN_CAPACITY` apos insercoes e democoes
- [ ] Warm tier respeita `WARM_TIER_TOKEN_CAPACITY` apos insercoes e democoes
- [ ] Cold tier aceita unidades ilimitadas
- [ ] `demote_from_hot()` nunca remove head/tail anchors
- [ ] `promote()` move unidades de cold/warm para hot atomicamente

### Criterio 4: Orquestrador

- [ ] `ingest_context()` insere no hot e dispara democao em cascata se necessario
- [ ] `step_forward()` executa prefetch preditivo antes de avancar o passo
- [ ] `query_context()` promove para hot se a unidade estiver em cold/warm
- [ ] `get_tier_distribution()` reporta contagens e percentuais corretos

### Criterio 5: Prefetch

- [ ] `PrefetchPredictor.predict()` segue o grafo de referencias ate `lookahead_depth`
- [ ] Prefetch so promove unidades que cabem no espaco restante do hot tier
- [ ] Unidades preditas sao ordenadas por score de relevancia

### Criterio 6: Simulacao

- [ ] As 40 unidades do incidente sao distribuidas entre os tres tiers
- [ ] Hot tier mantem as unidades mais relevantes no task_step=12
- [ ] Unidades criticas do final do incidente estao no hot tier
- [ ] A reducao no contexto ativo e reportada e comparada com a janela unica

---

## Rubrica de Avaliacao

| Criterio | Peso | Insuficiente (0-3) | Basico (4-6) | Proficiente (7-8) | Excelente (9-10) |
|---|---|---|---|---|---|
| **Diagnostico (Parte 1)** | 15% | Nao identificou o colapso da janela unica | Identificou parcialmente sem calculos de tokens | Diagnostico completo com contagem e comparacao | Diagnostico + analise de sensibilidade dos thresholds de capacidade |
| **Relevancia + Tiers (Parte 2)** | 40% | Funcoes core nao implementadas | Implementa mas erra em edge cases (anchors, capacidades) | Tiers funcionais com democao em cascata e protecao de anchors | Tiers completos + prefetch preditivo + pesos calibrados |
| **Simulacao (Parte 3)** | 30% | Nao executou a simulacao | Simulacao parcial sem comparacao | Simulacao completa com contraste tiered vs. janela unica | Simulacao + analise da cadeia de referencias + propostas de otimizacao |
| **Testes e verificacao** | 15% | Nenhum cenario passa | 3 criterios passam | 5 criterios passam | Todos os 6 criterios passam |

**Nota final:** Media ponderada. **Aprovacao:** >= 7.0

---

## Dicas para Implementacao

### Para a Relevancia

1. **Relevancia nao e recencia pura.** Uma unidade antiga com muitas referencias (ex: o primeiro diagnostico que todo passo subsequente cita) e mais relevante que uma unidade recente que ninguem referencia. Por isso `reference_count` tem peso 0.40 — o maior da formula.

2. **O step_proximity suaviza a queda.** Uma unidade do passo 10 nao e 10x menos relevante que uma do passo 11. A formula `1 / (1 + |delta|)` garante que a queda e sublinear: delta=1 → 0.5, delta=5 → 0.17, delta=20 → 0.05.

3. **Calibre os pesos com dados reais.** Os pesos default (0.35/0.40/0.25) sao um ponto de partida. Em um sistema real, meca a correlacao entre o score de relevancia e a probabilidade de o modelo referenciar a unidade no proximo passo.

### Para os Tiers

1. **Democao em cascata e inevitavel.** Quando o hot tier enche, demover unidades para warm pode encher o warm tier, disparando democao para cold. Isso e correto — e o comportamento esperado de um sistema de storage em camadas.

2. **Head/tail anchors sao a ancora cognitiva.** As ultimas 3 unidades (tail) mantem o modelo ancorado no contexto imediato. O runbook do passo atual (head) mantem o modelo orientado ao objetivo. Sem anchors, o hot tier pode se encher de contexto irrelevante que por acaso tem score alto.

3. **A latencia simulada importa.** Cold → hot tem latencia de ~100ms — isso e perceptivel para o usuario. O prefetch preditivo existe exatamente para esconder essa latencia: promover contexto de cold para warm antes que o agente precise dele.

### Para o Prefetch

1. **Prefetch e especulativo por natureza.** Nem toda unidade promovida por prefetch sera usada. Isso e aceitavel — o custo de uma promocao desnecessaria e menor que o custo de um cache miss no cold tier durante o raciocinio.

2. **A profundidade do lookahead e um trade-off.** `lookahead_depth=1` so busca referencias diretas. `lookahead_depth=3` pode trazer unidades demais, enchendo o hot tier com contexto especulativo. O default `2` e um equilibrio razoavel.

3. **Prefetch usa o grafo de referencias, nao similaridade.** A decisao de promover e baseada em conexoes reais (quem referenciou quem), nao em similaridade semantica. Isso evita o problema de near-miss distractors que aceleram a degradacao.

---

## Duvidas Comuns

**P: Isso nao e so um cache LRU com tres niveis?**
R: E mais que LRU. LRU usa apenas recencia. O Tiered Context Storage usa relevancia composta (recencia + referencias + proximidade). Uma unidade antiga com 50 referencias pode ter score de relevancia maior que uma unidade recente com 0 referencias. LRU demoveria a antiga; o TieredContextStore mantem a antiga no hot.

**P: Como isso se relaciona com Head-Tail Context Truncation?**
R: Head-Tail Truncation define a estrutura da janela ativa (head + middle + tail). Tiered Context Storage define onde o middle vive e como ele se move. O head e tail do Head-Tail Truncation sao os anchors do Tiered Context Storage. O middle truncado vive no warm/cold tier e e promovido de volta quando necessario.

**P: Qual a diferenca entre warm e cold na pratica?**
R: Warm e "provavelmente util em breve" — contexto das ultimas decisoes, acessivel com latencia de ~1ms. Cold e "historico para consulta" — todas as unidades desde t0, acessivel com latencia de ~100ms. A diferenca de 100x na latencia importa: promover de cold para hot durante o raciocinio introduz uma pausa perceptivel. Promover de warm para hot e quase instantaneo.

**P: Como definir os thresholds de capacidade (16K hot, 64K warm)?**
R: Os thresholds devem ser fracoes da janela total do modelo. Para uma janela de 128K: hot = 12.5% (16K), warm = 50% (64K). O hot tier e pequeno de proposito — o objetivo e manter o working set minimo. O warm tier e maior porque armazena contexto que pode ser util, mas nao esta sendo raciocinado agora. Ajuste conforme o perfil de atencao do modelo: modelos com vies de recencia forte precisam de hot tier menor.

---

## Proximo Passo

Depois de completar este exercicio:
1. Leia `[[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation]]` e observe como os anchors do tiered storage se integram com a estrutura head/middle/tail.
2. Leia `[[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]` — o catalogo de memoria enderecavel e o mecanismo de recuperacao que o tiered storage usa para resolver `query_context()`.
3. (Opcional) Estenda o sistema com `TierMigrationPolicy`: regras configuraraveis que definem quando uma unidade salta diretamente de hot para cold (ex: log entries sem referencias apos 5 minutos) vs. quando passa por warm primeiro.

---

*Exercicio Tiered Context Storage | Nivel 3 - Arquitetura Avancada*

**A janela de contexto nao e um deposito — e um espaco de trabalho que deve ser mantido deliberadamente pequeno.**
