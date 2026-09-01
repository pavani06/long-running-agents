---
title: "Exercício 15: Agent-First Data Foundation — Dados Projetados Para Quem Lê Literalmente"
type: exercise
level: 3
aliases: ["agent-first data foundation", "fundação de dados agent-first", "dados para agentes", "agents as design-time first-class user", "stitching de bancos", "data foundation como playground", "60% do esforço em dados"]
tags: [curriculo-conteudo, nivel-3, exercicio, agentes-orquestracao, data-platform, production, harness-engineering, data-foundation, freshness-sla, schema-explicitness, consolidation-plan, python, dataclass]
relates-to: ["[[docs/canonical/agent-first-data-foundation|Agent-First Data Foundation]]", "[[docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-patterns|Clay Eval Stack Patterns]]", "[[docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-classification|Clay Eval Stack Classification]]", "[[docs/canonical/agent-specific-data-freshness-pipeline|Agent-Specific Data Freshness Pipeline]]", "[[docs/canonical/centralized-data-plane-inherited-rbac|Centralized Data Plane (Inherited RBAC)]]", "[[docs/canonical/file-system-materialization|File-System Materialization]]", "[[docs/canonical/epistemic-memory-graph|Epistemic Memory Graph]]", "[[curriculum/03-nivel-3-advanced-architecture/exercises/exercise-14-unified-tool-surface-flywheel|Exercício 14: Unified Tool Surface Flywheel]]", "[[curriculum/03-nivel-3-advanced-architecture/exercises/exercise-17-self-iterating-agent-loop|Exercício 17: Self-Iterating Agent Loop]]"]
duration: "90-120 min"
last_updated: 2026-08-31
---

# 🧱 Exercício 15: Agent-First Data Foundation — Dados Projetados Para Quem Lê Literalmente
## Nível 3 — Arquitetura Avançada

**Tempo Estimado:** 90-120 minutos
**Dificuldade:** (Avançado)
**Pré-requisito:** Ter lido `02-state-persistence.md` (Nível 3) + `docs/canonical/agent-specific-data-freshness-pipeline.md` + Exercício 14
**Objetivo:** Tratar o agente como usuário de primeira classe em design-time da plataforma de dados — medir o custo de stitching cross-banco que a fragmentação impõe, pontuar a prontidão de cada dataset para consumo agêntico (freshness, explicitude, ambiguidade), e produzir um plano de consolidação que elimina o gargalo concreto dos learning loops

---

## 📖 Prólogo: A Sessão de 60 Tool Calls em Que 40 Foram Encanamento

### Quarta-feira, 14h00. O CEO pergunta a coisa simples.

```
CEO: "quais use cases do assistente degradaram nas últimas 2 semanas?
      Quero antes da reunião de board de amanhã."

ANALYST_AGENT: [plano de 4 passos]
  1. buscar conversas por use case ......... LangFuse API (traces)
  2. cruzar com CSAT ....................... Postgres `support.csat`
  3. filtrar por coorte de cliente ......... Metabase (SQL contra outro PG)
  4. checar mudanças de catálogo ........... Sheets do time de marketing

[2 horas depois]

ANALYST_AGENT: "Não consigo responder com confiança. Explicando:
  - traces e CSAT não compartilham chave de cliente (precisei
    inferir por telefone em E.164 vs. formato local: 40 tool calls
    de normalização)
  - o Sheets de catálogo mudou de nome de coluna semana passada
    (mais 12 calls de descoberta e 3 de retry)
  - o Metabase só aceita query por usuário humano (roleplay via
    service account que expira a cada 30 min: 4 re-autenticações)
  Conclusão: orçamento de contexto esgotado antes da análise."

ANALYST: "40 das 60 calls foram encanamento. A análise em si eram 4."
```

**O custo da fragmentação:**

```
╔══════════════════════════════════════════════════════════════════╗
║        O AGENTE ENCANADOR — 67% DA EXECUÇÃO É PLUMBING            ║
║                                                                  ║
║  Pergunta (1 linha):     "quais use cases degradaram?"          ║
║  Resposta:               NÃO ENTREGUE (contexto esgotado)       ║
║                                                                  ║
║  Tool calls:             60                                      ║
║   └─ stitching/joins:    40 (67%)  ← chaves, formatos, auth      ║
║   └─ descoberta:         16        ← schemas que ninguém publica║
║   └─ análise real:       4                                           ║
║                                                                  ║
║  A mesma pergunta, pós-consolidação (estimado):                  ║
║   1 query sobre a fundação unificada → 3 tool calls              ║
║                                                                  ║
║  A tese da fonte: a fragmentação é O gargalo dos learning        ║
║  loops — não modelos, não evals. Data primitives primeiro.       ║
║  "60% of project time may need to be allocated to data           ║
║   foundation" (production playbook, via ...classification.md:202)║
╚══════════════════════════════════════════════════════════════════╝
```

**O problema não é o modelo.** O agente era competente — e gastou dois terços da
execução fazendo o trabalho que a plataforma deveria fazer por ele: unificar chaves,
descobrir schemas, re-autenticar. Piores: os dados foram *projetados para dashboards
humanos*, que toleram staleness, ambiguidade e inconsistência; o agente trata cada ponto
de dado literalmente (`agent-specific-data-freshness-pipeline.md:22`). A própria doc
canônica de freshness do repo declara o gap: "No data pipelines designed for agent
consumption rather than human dashboard consumption" (`...md:86`).

O padrão Agent-First Data Foundation nomeia o que falta: **agentes como usuário
first-class de design-time** de uma fundação única — não como consumidor tardio de
quatro sistemas que nunca ouviram falar dele (`...patterns.md:228-249`).

**Sua missão:** implementar o `DataFoundationPlanner` — inventário de fontes com
`StitchingCostModel` (quanto da execução agêntica a fragmentação cobra, por classe de
pergunta), `AgentDataReadinessScore` (freshness, explicitude de schema, ambiguidade,
uniformidade de acesso — os critérios que dashboards humanos perdoam e agentes não), e o
`UnifiedFoundationPlan` que consolida first-party + third-party numa fundação só,
eliminando o stitching das classes de pergunta recorrentes.

---

## 🧠 O Contexto

### O Modelo Mental: O Agente Como Usuário de Design-Time

Três deslocamentos que definem o padrão:

1. **Literalidade em vez de tolerância.** Pipelines para humanos toleram staleness
   ("o dashboard atualiza de hora em hora, ok"), ambiguidade ("a coluna `valor` é
   líquido ou bruto? o analista sabe") e inconsistência ("as duas bases divergem, o
   time confia na oficial"). O agente não tolera nada disso — ele lê literalmente e
   propaga o erro com confiança (`agent-specific-data-freshness-pipeline.md:22`). Cada
   tolerância humana embutida no dado é uma armadilha agêntica.
2. **Consolidação em vez de acesso adaptado.** A resposta à fragmentação não é ensinar
   o agente a fazer stitching melhor (mais prompts, mais tools de join) — é eliminar o
   stitching da lista de coisas que o agente precisa fazer. Quatro sistemas viram uma
   fundação com um plano de acesso (`centralized-data-plane-inherited-rbac.md:44,68-70`).
3. **A fundação precede o payoff.** "Unification effort precedes any agent payoff"
   (`...patterns.md:244`) — a decisão é investir em data primitives antes de qualquer
   promessa de learning loop. O playground vem depois do alicerce.

O critério operacional que o exercício codifica: uma fundação é agent-first quando as
**classes de pergunta recorrentes** do negócio se resolvem com consultas diretas sobre
ela — zero hops de stitching, zero descoberta de schema, zero re-autenticação.

### O Que Você Vai Construir

1. `DataSource` — inventário: sistema, tipo (first/third-party), freshness, schema
   publishing, ambiguidades conhecidas, acesso
2. `QuestionClass` — as perguntas recorrentes do negócio e os *join paths* que exigem
   hoje (o custo de encanamento por pergunta)
3. `StitchingCostModel` — % da execução gasta em stitching por classe de pergunta
4. `AgentDataReadinessScore` — 0.0-1.0 por dataset: freshness SLA, explicitude de
   schema, ambiguidade declarada, uniformidade de acesso
5. `UnifiedFoundationPlan` — grupos de consolidação, guardrails de design-time
   (o que a fundação promete aos agentes), e verificação de eliminação de stitching

---

## 📋 Cenário

O estado de dados do KODA (o do prólogo, formalizado no starter):

| # | Fonte | Tipo | Freshness | Schema publicado | Ambiguidade conhecida | Acesso |
|---|---|---|---|---|---|---|
| 1 | `langfuse_traces` | first-party | tempo real | parcial (spans sem dicionário) | user_id ausente em 30% | API paginada |
| 2 | `pg_support` (tickets, CSAT) | first-party | 15 min | sim | `valor` líquido/bruto ambíguo | SQL direto |
| 3 | `pg_orders` | first-party | tempo real | sim | nenhuma | SQL direto |
| 4 | `mb_analytics` (Metabase) | first-party | diária | não (queries nomeadas) | coortes definidas ad hoc | SQL por usuário humano |
| 5 | `sheets_catalog` (marketing) | third-party | manual | não | colunas renomeadas à vontade | export CSV |
| 6 | `partner_reviews` (API externa) | third-party | 24h | sim | rating 1-5 vs. 1-10 já visto | API key |

Classes de pergunta recorrentes: **"quais use cases degradaram?"** (join 1×2×4, chaves
incompatíveis), **"qual produto teve mais devolução e por quê?"** (3×5), **"o que os
clientes dizem do novo sabor?"** (3×6).

---

## ✅ Requisitos

### Requisitos Funcionais

1. **RF1 — Inventário honesto:** cada `DataSource` declara freshness, se o schema é
   publicado, ambiguidades conhecidas e modo de acesso — dataset sem schema publicado
   ou com ambiguidade NÃO declarada derruba a nota de readiness (a armadilha agêntica
   é a ambiguidade invisível, não a declarada).
2. **RF2 — Custo de stitching por pergunta:** `StitchingCostModel.cost_for()` estima a
   fração da execução agêntica gasta em encanamento: hops de join × fator de
   incompatibilidade de chave + descoberta de schema (por fonte sem schema) +
   autenticação não-uniforme. Retorna fração [0.0, 1.0] e o detalhamento.
3. **RF3 — Alerta de encanador:** classe de pergunta com custo ≥ 0.50 gera
   `STITCHING_DOMINANT` — a pergunta não é analisável, é encanável.
4. **RF4 — Readiness composto:** `AgentDataReadinessScore` pondera freshness (0.25),
   schema explícito (0.30), ausência de ambiguidade (0.25), acesso uniforme (0.20);
   dataset com ambiguidade NÃO declarada recebe 0.0 no componente de ambiguidade.
5. **RF5 — Consolidação elimina stitching:** `UnifiedFoundationPlan.build()` agrupa as
   fontes por entidades de join (customer, product, conversation), define a fundação
   unificada e verifica: para cada classe de pergunta, os join paths antigos são
   substituídos por consulta direta (custo pós-plano < 0.15).
6. **RF6 — Guardrails de design-time:** o plano carrega as promessas da fundação aos
   agentes: freshness SLA por entidade, schema versionado e publicado, ambiguidades
   proibidas (renomear coluna sem versão = breaking change), acesso único com
   credencial de longa duração. Sem guardrails, o plano não é aprovável.
7. **RF7 — Payoff declarado como precedido:** o plano registra `unification_precedes_payoff: true`
   e o percentual de esforço de projeto alocado à fundação (a fonte chega a 60%;
   registre o seu, justificado em uma linha).

### Requisitos Técnicos

1. **RT1 — Python 3.9+, stdlib apenas**, type hints obrigatórios
2. **RT2 — `dataclasses` + enums**; modelos frozen onde possível
3. **RT3 — Custo e score são funções puras** do inventário; sem I/O
4. **RT4 — Detalhe auditável:** todo custo/score carrega o breakdown que o produz

---

## 🏗️ Arquitetura do Sistema

```
┌────────────────────────────────────────────────────────────────────────┐
│                    DATA FOUNDATION PLANNER                              │
│                                                                        │
│  INVENTÁRIO                    CLASSES DE PERGUNTA                     │
│  ┌───────────────────┐        ┌──────────────────────────────┐         │
│  │ langfuse_traces   │        │ "use cases degradaram?"      │         │
│  │ pg_support        │        │   join: traces×csat×coorte   │         │
│  │ pg_orders         │        │ "devoluções e por quê?"      │         │
│  │ mb_analytics      │        │   join: orders×catalog       │         │
│  │ sheets_catalog    │        │ "reviews do novo sabor?"     │         │
│  │ partner_reviews   │        │   join: orders×reviews       │         │
│  └─────────┬─────────┘        └───────────────┬──────────────┘         │
│            └────────────────┬─────────────────┘                        │
│                             ▼                                          │
│  ┌──────────────────────────────────────────────────────────────┐      │
│  │  STITCHING COST MODEL (por pergunta)                          │      │
│  │  hops × incompat. de chave + descoberta + auth não-uniforme   │      │
│  │  ≥ 0.50 → STITCHING_DOMINANT (a pergunta é encanamento)       │      │
│  └──────────────────────────┬───────────────────────────────────┘      │
│                             ▼                                          │
│  ┌──────────────────────────────────────────────────────────────┐      │
│  │  AGENT DATA READINESS (por dataset)                           │      │
│  │  freshness .25 | schema .30 | ambiguidade .25 | acesso .20    │      │
│  │  ambiguidade NÃO declarada → 0.0 no componente               │      │
│  └──────────────────────────┬───────────────────────────────────┘      │
│                             ▼                                          │
│  ┌──────────────────────────────────────────────────────────────┐      │
│  │  UNIFIED FOUNDATION PLAN                                      │      │
│  │  entidades: customer | product | conversation                 │      │
│  │  guardrails: SLA freshness, schema versionado, sem renome     │      │
│  │              silencioso, acesso único longa duração           │      │
│  │  verificação: custo pós-plano < 0.15 por pergunta            │      │
│  │  unification_precedes_payoff: true                            │      │
│  └──────────────────────────────────────────────────────────────┘      │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 🎯 Sua Tarefa em 3 Partes

### Parte 1 — Diagnosticar a sessão encanadora (15 min)

Com o trace do prólogo: classifique as 56 calls de encanamento/descoberta nos três
componentes do custo (chave, schema, auth). Qual fonte contribui mais por componente?
Responda como comentário, e diga qual tolerância humana (staleness, ambiguidade,
inconsistência) cada fonte embute.

### Parte 2 — Custo e readiness (40 min)

Implemente `StitchingCostModel.cost_for()` com `STITCHING_DOMINANT` (RF2-RF3) e
`AgentDataReadinessScore.score()` (RF4). Verifique que a pergunta do CEO do prólogo é
`STITCHING_DOMINANT` e que `sheets_catalog` pontua readiness pior que `pg_orders`.

### Parte 3 — O plano de consolidação (45 min)

Implemente `UnifiedFoundationPlan.build()` com entidades de join, guardrails de
design-time e verificação de eliminação de stitching (RF5-RF7). Verifique que todas as
classes de pergunta caem abaixo de 0.15 pós-plano.

---

## 💻 Starter Code

```python
"""
Exercício 15 — Agent-First Data Foundation
Nível 3 — Arquitetura Avançada

Trate o agente como usuário de primeira classe em design-time: meça o custo
de stitching que a fragmentação impõe, pontue a prontidão agêntica de cada
dataset e planeje a fundação unificada que elimina o encanamento.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


# ============================================================================
# DATA MODELS
# ============================================================================

class FreshnessClass(Enum):
    REAL_TIME = "real_time"        # < 1 min
    MINUTES_15 = "15min"
    HOURLY = "hourly"
    DAILY = "daily"
    MANUAL = "manual"              # atualiza quando alguém lembra


class AccessMode(Enum):
    SQL_DIRECT = "sql_direct"        # credencial de serviço, longa duração
    API_KEY = "api_key"              # estável
    API_PAGINATED = "api_paginated"  # estável, mas paginada
    HUMAN_PROXY = "human_proxy"      # exige roleplay de usuário humano
    CSV_EXPORT = "csv_export"


class Party(Enum):
    FIRST_PARTY = "first_party"
    THIRD_PARTY = "third_party"


@dataclass(frozen=True)
class Ambiguity:
    """Uma ambiguidade CONHECIDA e declarada no inventário."""
    field: str
    description: str        # ex.: "valor é líquido ou bruto"
    declared: bool          # False = armadilha invisível (RF4)


@dataclass(frozen=True)
class DataSource:
    name: str
    party: Party
    entity: str                    # entidade dominante: customer/product/conversation
    freshness: FreshnessClass
    schema_published: bool
    join_key: str | None           # chave canônica p/ cross-source (None = não tem)
    join_key_coverage: float       # fração de linhas com a chave válida
    access: AccessMode
    ambiguities: tuple[Ambiguity, ...] = ()


@dataclass(frozen=True)
class JoinHop:
    from_source: str
    to_source: str
    key_compatible: bool           # False = agente precisa normalizar


@dataclass(frozen=True)
class QuestionClass:
    """Pergunta recorrente do negócio e o caminho que ela exige hoje."""
    question: str
    sources_needed: tuple[str, ...]
    join_hops: tuple[JoinHop, ...]


@dataclass(frozen=True)
class StitchingBreakdown:
    key_normalization: float   # hops incompatíveis × fator
    schema_discovery: float    # fontes sem schema publicado
    auth_overhead: float       # fontes com acesso não-uniforme
    total: float


class StitchingCostModel:
    """Fração da execução agêntica gasta em encanamento (função pura)."""

    STITCHING_DOMINANT_THRESHOLD = 0.50
    KEY_INCOMPAT_FACTOR = 0.18     # por hop incompatível
    DISCOVERY_FACTOR = 0.12        # por fonte sem schema
    AUTH_FACTOR = 0.15             # por fonte com acesso não-uniforme

    def cost_for(
        self, question: QuestionClass, inventory: dict[str, DataSource]
    ) -> StitchingBreakdown:
        """
        total = soma dos três componentes, cap em 1.0.
        Auth não-uniforme: HUMAN_PROXY e CSV_EXPORT (acesso que exige
        adapttação do agente); SQL_DIRECT/API_KEY/API_PAGINATED são uniformes.
        """
        # TODO: implemente
        raise NotImplementedError

    def is_stitching_dominant(self, breakdown: StitchingBreakdown) -> bool:
        # TODO: implemente (RF3)
        raise NotImplementedError


@dataclass(frozen=True)
class ReadinessBreakdown:
    freshness: float
    schema: float
    ambiguity: float
    access: float
    total: float


class AgentDataReadinessScore:
    """Prontidão de um dataset para consumo agêntico (função pura)."""

    WEIGHTS = {"freshness": 0.25, "schema": 0.30, "ambiguity": 0.25, "access": 0.20}

    def score(self, source: DataSource) -> ReadinessBreakdown:
        """
        freshness: REAL_TIME=1.0, MINUTES_15=0.8, HOURLY=0.6, DAILY=0.3, MANUAL=0.1
        schema: publicado=1.0, parcial... (só True/False no inventário: 1.0/0.2)
        ambiguity: 1.0 sem ambiguidades; com ambiguidades DECLARADAS 0.6;
                   qualquer NÃO declarada → 0.0 (a armadilha invisível)
        access: SQL_DIRECT/API_KEY/API_PAGINATED=1.0/0.9/0.8; HUMAN_PROXY=0.1;
                CSV_EXPORT=0.3
        total = soma ponderada
        """
        # TODO: implemente
        raise NotImplementedError


# ============================================================================
# PARTE 3 — PLANO DE CONSOLIDAÇÃO
# ============================================================================

@dataclass(frozen=True)
class FoundationGuardrails:
    freshness_sla: dict[str, FreshnessClass]   # por entidade
    schema_versioned: bool = True
    silent_rename_prohibited: bool = True      # renomear coluna = breaking change
    single_access: AccessMode = AccessMode.SQL_DIRECT
    long_lived_credential: bool = True


@dataclass(frozen=True)
class UnifiedFoundationPlan:
    plan_id: str
    consolidation_groups: dict[str, list[str]]   # entidade → fontes consolidadas
    guardrails: FoundationGuardrails
    unification_precedes_payoff: bool = True
    foundation_effort_share: float = 0.6         # RF7: a fonte chega a 60%
    post_plan_costs: dict[str, float] = field(default_factory=dict)


class DataFoundationPlanner:
    """Inventário + perguntas → custo → readiness → plano."""

    POST_PLAN_COST_TARGET = 0.15
    ENTITY_OF = {"customer", "product", "conversation"}

    def build(
        self,
        inventory: dict[str, DataSource],
        questions: list[QuestionClass],
        cost_model: StitchingCostModel,
        plan_id: str = "koda-foundation-v1",
    ) -> UnifiedFoundationPlan:
        """
        1. agrupe fontes por entidade dominante (consolidation_groups)
        2. guardrails: freshness SLA por entidade = melhor freshness do grupo
        3. pós-plano, toda pergunta é consulta direta sobre a fundação:
           custo residual = 0.05 base + 0.03 por fonte third-party da pergunta
           (third-party continua externa; first-party é consolidada)
        4. verifique: toda pergunta < POST_PLAN_COST_TARGET, senão levante
           ValueError nomeando a pergunta não resolvida
        5. registre foundation_effort_share (RF7)
        """
        # TODO: implemente
        raise NotImplementedError


# ============================================================================
# FIXTURES — o estado de dados do KODA
# ============================================================================

def koda_inventory() -> dict[str, DataSource]:
    return {
        "langfuse_traces": DataSource(
            "langfuse_traces", Party.FIRST_PARTY, "conversation",
            FreshnessClass.REAL_TIME, schema_published=False,
            join_key="customer_phone", join_key_coverage=0.70,
            access=AccessMode.API_PAGINATED,
        ),
        "pg_support": DataSource(
            "pg_support", Party.FIRST_PARTY, "customer",
            FreshnessClass.MINUTES_15, schema_published=True,
            join_key="customer_phone_e164", join_key_coverage=1.0,
            access=AccessMode.SQL_DIRECT,
            ambiguities=(Ambiguity("valor", "líquido ou bruto", declared=True),),
        ),
        "pg_orders": DataSource(
            "pg_orders", Party.FIRST_PARTY, "customer",
            FreshnessClass.REAL_TIME, schema_published=True,
            join_key="customer_id", join_key_coverage=1.0,
            access=AccessMode.SQL_DIRECT,
        ),
        "mb_analytics": DataSource(
            "mb_analytics", Party.FIRST_PARTY, "conversation",
            FreshnessClass.DAILY, schema_published=False,
            join_key=None, join_key_coverage=0.0,
            access=AccessMode.HUMAN_PROXY,
        ),
        "sheets_catalog": DataSource(
            "sheets_catalog", Party.THIRD_PARTY, "product",
            FreshnessClass.MANUAL, schema_published=False,
            join_key="sku", join_key_coverage=0.85,
            access=AccessMode.CSV_EXPORT,
            ambiguities=(Ambiguity("preco", "com ou sem promoção?", declared=False),),
        ),
        "partner_reviews": DataSource(
            "partner_reviews", Party.THIRD_PARTY, "product",
            FreshnessClass.DAILY, schema_published=True,
            join_key="gtin", join_key_coverage=0.60,
            access=AccessMode.API_KEY,
        ),
    }


def koda_questions() -> list[QuestionClass]:
    return [
        QuestionClass(  # a pergunta do CEO
            "quais use cases degradaram nas últimas 2 semanas?",
            ("langfuse_traces", "pg_support", "mb_analytics"),
            (
                JoinHop("langfuse_traces", "pg_support", key_compatible=False),
                JoinHop("pg_support", "mb_analytics", key_compatible=False),
            ),
        ),
        QuestionClass(
            "qual produto teve mais devolução e por quê?",
            ("pg_orders", "sheets_catalog"),
            (JoinHop("pg_orders", "sheets_catalog", key_compatible=True),),
        ),
        QuestionClass(
            "o que os clientes dizem do novo sabor?",
            ("pg_orders", "partner_reviews"),
            (JoinHop("pg_orders", "partner_reviews", key_compatible=False),),
        ),
    ]


# ============================================================================
# TESTS
# ============================================================================

def test_ceo_question_is_stitching_dominant():
    model = StitchingCostModel()
    inv = koda_inventory()
    ceo = koda_questions()[0]
    bd = model.cost_for(ceo, inv)

    assert bd.total >= 0.50, (
        f"a pergunta do CEO deve ser STITCHING_DOMINANT, custo {bd.total:.2f}"
    )
    assert model.is_stitching_dominant(bd)
    assert bd.schema_discovery > 0, "duas fontes sem schema publicado"
    assert bd.auth_overhead > 0, "mb_analytics exige proxy humano"
    print("TESTE 1 PASSOU")


def test_readiness_orders_beats_sheets():
    scorer = AgentDataReadinessScore()
    inv = koda_inventory()
    orders = scorer.score(inv["pg_orders"])
    sheets = scorer.score(inv["sheets_catalog"])

    assert orders.total > 0.85, "pg_orders é o dataset exemplar"
    assert sheets.total < 0.35, "sheets_catalog é a armadilha"
    # a ambiguidade NÃO declarada de preco zera o componente (RF4)
    assert sheets.ambiguity == 0.0
    # a ambiguidade DECLARADA de pg_support não zera
    support = scorer.score(inv["pg_support"])
    assert support.ambiguity == 0.6
    print("TESTE 2 PASSOU")


def test_plan_eliminates_stitching():
    planner = DataFoundationPlanner()
    model = StitchingCostModel()
    plan = planner.build(koda_inventory(), koda_questions(), model)

    groups = plan.consolidation_groups
    assert {"customer", "product", "conversation"} <= set(groups)
    # first-party consolidada por entidade
    assert "pg_support" in groups["customer"]
    assert "langfuse_traces" in groups["conversation"]
    # toda pergunta abaixo do alvo pós-plano
    for q in koda_questions():
        cost = plan.post_plan_costs[q.question]
        assert cost < DataFoundationPlanner.POST_PLAN_COST_TARGET, (
            f"pergunta não resolvida pelo plano: {q.question} ({cost:.2f})"
        )
    # pergunta só first-party custa menos que pergunta com third-party
    c_devolucao = plan.post_plan_costs["qual produto teve mais devolução e por quê?"]
    c_sabor = plan.post_plan_costs["o que os clientes dizem do novo sabor?"]
    assert c_devolucao < c_sabor, "third-party mantém custo residual"
    print("TESTE 3 PASSOU")


def test_guardrails_are_design_time_promises():
    planner = DataFoundationPlanner()
    plan = planner.build(koda_inventory(), koda_questions(), StitchingCostModel())

    g = plan.guardrails
    assert g.schema_versioned and g.silent_rename_prohibited
    assert g.single_access == AccessMode.SQL_DIRECT
    assert g.long_lived_credential
    # SLA por entidade = melhor freshness do grupo
    assert g.freshness_sla["customer"] == FreshnessClass.REAL_TIME
    assert g.freshness_sla["conversation"] == FreshnessClass.REAL_TIME
    # RF7
    assert plan.unification_precedes_payoff is True
    assert 0.3 <= plan.foundation_effort_share <= 0.7
    print("TESTE 4 PASSOU")


if __name__ == "__main__":
    print("=" * 60)
    print("EXERCÍCIO 15: AGENT-FIRST DATA FOUNDATION")
    print("=" * 60)
    # Descomente após implementar:
    # test_ceo_question_is_stitching_dominant()
    # test_readiness_orders_beats_sheets()
    # test_plan_eliminates_stitching()
    # test_guardrails_are_design_time_promises()
    print("\nTODO: implemente StitchingCostModel, AgentDataReadinessScore")
    print("e DataFoundationPlanner.build")
```

---

## ✅ Validação: Critérios de Aceitação

Seu código será considerado **APROVADO** quando:

- [ ] A pergunta do CEO custa ≥ 0.50 e é `STITCHING_DOMINANT`, com breakdown de chave/schema/auth preenchido
- [ ] `pg_orders` pontua readiness > 0.85; `sheets_catalog` < 0.35 com `ambiguity == 0.0` (a não declarada zera — RF4)
- [ ] A ambiguidade *declarada* de `pg_support` dá 0.6 no componente, não zero
- [ ] O plano consolida por entidade (customer/product/conversation) e toda pergunta cai abaixo de 0.15 pós-plano
- [ ] Pergunta com fonte third-party custa mais que pergunta só first-party pós-plano
- [ ] Guardrails de design-time presentes: schema versionado, rename silencioso proibido, acesso único com credencial longa, SLA de freshness por entidade
- [ ] `unification_precedes_payoff: true` com esforço de fundação registrado (0.3–0.7)

---

## 📊 Rubric de Avaliação

| Critério | Peso | Insuficiente (0-3) | Básico (4-6) | Proficiente (7-8) | Excelente (9-10) |
|---|---|---|---|---|---|
| **StitchingCostModel (Parte 2)** | 30% | Não implementado | Conta hops sem componentes | Três componentes com fatores | Breakdown auditável + STITCHING_DOMINANT como veredito |
| **Readiness (Parte 2)** | 25% | Não implementado | Score único sem breakdown | Quatro componentes ponderados | Distinção declarada/não-declarada como regra de armadilha |
| **Plano (Parte 3)** | 30% | Não implementado | Agrupa sem verificar | Eliminação verificada por pergunta | Third-party residual modelado + verificação falha com pergunta nomeada |
| **Guardrails (Parte 3)** | 15% | Ausentes | SLA apenas | Promessas completas | Promessas ligadas à literalidade agêntica (rename = breaking change) |

**Nota final:** Média ponderada. **Aprovação:** >= 7.0

---

## 💡 Dicas para Implementação

1. **Ambiguidade declarada é informação; invisível é armadilha.** A diferença entre 0.6 e 0.0 no componente de ambiguidade é o padrão inteiro em miniatura: dashboards humanos convivem com a ambiguidade invisível porque o analista "sabe"; o agente lê literalmente e erra com confiança. Declarar já é resolver metade.
2. **O custo é da pergunta, não da fonte.** Fontes isoladas podem ser saudáveis; o custo nasce do *caminho* (joins + descoberta + auth). Modele por classe de pergunta — é como o negócio sente o gargalo.
3. **Third-party não se consolida, se contrata.** O plano elimina o stitching *interno*; fontes externas mantêm um residual (0.05 + 0.03/fonte no modelo proposto). Prometer zero para tudo é a menteira que desmoraliza o plano na primeira integração.

---

## ❓ Dúvidas Comuns

**P: Isso não é só um data warehouse moderno com outro nome?**
R: A mecânica de consolidação é parecida; o critério de aceitação é diferente. Um warehouse aceita se serve dashboards; a fundação agent-first aceita se serve *consultas literais* — com freshness SLA, schema versionado e ambiguidade proibida, porque o consumidor não perdoa (`agent-specific-data-freshness-pipeline.md:22`). É o requisito de aceitação que muda o design.

**P: 60% do esforço em fundação não é exagero?**
R: É o número da fonte para o contexto dela (`...classification.md:202`) — e o ponto é a ordem, não a fração exata: "unification effort precedes any agent payoff" (`...patterns.md:244`). Registre a sua fração justificada; o que o exercício exige é que ela seja uma decisão explícita, não um descobrimento tardio.

**P: Por que não ensinar o agente a fazer joins melhores?**
R: Porque isso otimiza o sintoma. Cada hora de agente fazendo stitching é uma hora que não escala — o encanamento consome orçamento de contexto da análise real (o prólogo: 4 calls de análise em 60). A tese do padrão: eliminar o gargalo estrutural vale mais que melhorar o agente que o sofre.

**P: Como isso se conecta ao resto do currículo?**
R: É o pré-requisito declarado do [[curriculum/03-nivel-3-advanced-architecture/exercises/exercise-17-self-iterating-agent-loop|Exercício 17]] — o loop que itera o agente sobre o feedback acumulado só fecha se o feedback estiver numa fundação única (o elo mais fraco do loop é o dado). E espelha o Exercício 14: lá a unificação é da superfície de tools; aqui, do plano de dados.

---

## 🚀 Próximo Passo

Depois de completar este exercício:

1. Leia o padrão 11 completo e sua classificação: `docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-patterns.md:228-249` e `...classification.md:190-206` — a própria doc de freshness do repo declara a implementação ausente
2. Faça o inventário real do KODA: quantas fontes, quantas ambiguidades *não declaradas*, qual pergunta recorrente é `STITCHING_DOMINANT` hoje?
3. Siga para o [[curriculum/03-nivel-3-advanced-architecture/exercises/exercise-16-bulk-in-context-trace-analysis|Exercício 16: Bulk In-Context Trace Analysis]] — a fundação é o que torna a amostra de 10k traces consultável

---

*Exercício 15 | Nível 3 — Arquitetura Avançada | Agent-First Data Foundation*

**O dashboard perdoa o dado ambíguo; o agente casa ele com confiança. Projete para quem lê literalmente.**
