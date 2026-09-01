---
title: "Exercício 7: Eval Coverage Matrix — o Portfólio de Evals Como Matriz 2x2, Não Como Bateria de Goldens"
type: exercise
level: "N2"
aliases: ["eval coverage matrix", "matriz de cobertura de evals", "2x2 determinismo x deployment", "quadrantes de eval", "gap list de evals", "portfolio de avaliação", "a few things in each box"]
tags: [curriculo-conteudo, nivel-2, exercicio, evals, harness-engineering, governanca, coverage-matrix, eval-portfolio, quadrant-analysis, gap-analysis, python, dataclass]
relates-to: ["[[docs/canonical/eval-coverage-matrix|Eval Coverage Matrix]]", "[[docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-patterns|Clay Eval Stack Patterns]]", "[[docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-classification|Clay Eval Stack Classification]]", "[[docs/canonical/3-layer-evaluation-architecture|3-Layer Evaluation Architecture]]", "[[docs/canonical/eval-tier-stratification|Eval Tier Stratification]]", "[[docs/canonical/evals-as-brakes|Evals-as-Brakes]]", "[[curriculum/02-nivel-2-practical-patterns/exercises/exercise-06-perceived-eval|Exercício 6: Perceived-Eval]]", "[[curriculum/03-nivel-3-advanced-architecture/exercises/exercise-13-production-offline-drift-taxonomy|Exercício 13: Production-to-Offline Feedback Loop with Drift Taxonomy]]"]
duration: "60-90 min"
last_updated: 2026-08-31
---

# 🗺️ Exercício 7: Eval Coverage Matrix — o Portfólio de Evals Como Matriz 2x2, Não Como Bateria de Goldens
## Nível 2 — Padrões Práticos

**Tempo Estimado:** 60-90 minutos
**Dificuldade:** (Intermediário)
**Pré-requisito:** Ter lido `03-rubric-design.md` (Nível 2) + `docs/canonical/3-layer-evaluation-architecture.md`
**Objetivo:** Representar todo o portfólio de avaliação de um agente numa matriz 2x2 (determinismo × deployment), detectar quadrantes cegos por classe de modo de falha, e planejar alocação de investimento com piso de cobertura por quadrante — em vez de profundidade num quadrante só

---

## 📖 Prólogo: A Suite 100% Verde Que Não Viu o Incidente

### Sexta-feira, 09h12. Release 2.14 do agente de atendimento do KODA entra em canary.

```
CI: "eval-suite: 150/150 PASS (goldens) — 4min12s
     constraint-checks: 88/88 PASS — 1min03s
     llm-judge-similarity: 97% — 11min45s
     TOTAL: verde. Ship it."

PM:  "ship."

── 36 horas depois ──────────────────────────────────────────────

SUPPORT: "temos ~200 conversas/dia em que o agente entra em loop
          de reformulação depois do 5º turno. Cliente repete a
          pergunta, agente repete a resposta. Churn subindo."

ENG_LEAD: "como isso passou? rodamos 150 goldens!"

TRACE_ANALYST: "porque os 150 goldens são single-turn. O loop só
                existe em sessões longas, com comportamento do
                usuário real — e nenhum eval nosso olha isso.
                Todo o nosso portfólio mora no mesmo quadrante."
```

**O custo do quadrante único:**

```
╔══════════════════════════════════════════════════════════════════╗
║        SUITE VERDE, PRODUTO CEGO — O INVENTÁRIO DE SÁBADO        ║
║                                                                  ║
║  Mecanismos de eval do time (todos OFFLINE):                     ║
║   ✓ 150 goldens determinísticos (single-turn)                    ║
║   ✓ 88 constraint checks estruturados                            ║
║   ✓ 1 LLM-judge de similaridade                                  ║
║                                                                  ║
║  O que o incidente exigia (nenhum existia):                      ║
║   ✗ eval comportamental de sessão longa (N+1)      → ONLINE*     ║
║   ✗ sinal percebido do usuário (correção/abandono)  ONLINE/ND    ║
║   ✗ bulk trace analysis p/ achar a frequência      → OFFLINE/ND  ║
║   ✗ A/B com gate de métricas de produção           → ONLINE/ND   ║
║                                                                  ║
║  Incidentes no quadrante vazio:  1 (e cresciendo)                ║
║  Tempo p/ diagnosticar:          36h (com suite verde!)          ║
║  Clientes afetados:              ~200/dia                        ║
║                                                                  ║
║  * o comportamento de loop só se manifesta em execução real      ║
╚══════════════════════════════════════════════════════════════════╝
```

**O problema não é a qualidade dos goldens.** Os 150 goldens são bons — para o que eles
cobrem. O problema é que a equipe nunca olhou para o portfólio como um portfólio: cada
mecanismo foi adicionado quando doeu, um por vez, e todos caíram no mesmo quadrante
(offline, majoritariamente determinístico). Nenhuma classe de modo de falha fora desse
quadrante tinha detector — o incidente era invisível por construção.

O repo vive exatamente esta cegueira estruturada: cada doc canônico estratifica por um
eixo só — `3-layer-evaluation-architecture` por **mecanismo** (`docs/canonical/3-layer-evaluation-architecture.md:28`),
`eval-tier-stratification` por **velocidade/trigger** (`docs/canonical/eval-tier-stratification.md:32-36`)
— e a matriz 2x2 do padrão (determinismo × deployment) com meta de cobertura
formalmente **não existe** (`...classification.md:15-27`).

**Sua missão:** implementar uma `EvalCoverageMatrix` que classifica cada mecanismo de eval
do inventário nos dois eixos, produz o mapa de cobertura com a meta "algumas coisas em
cada quadrante" (*a few things in each box* — piso, não teto), lista os gaps por classe de
modo de falha, e gera um `AllocationPlan` que diz qual mecanismo construir primeiro para
qual quadrante vazio — considerando restrições reais de observabilidade (volume de traces,
capacidade de contatar clientes).

---

## 🧠 O Contexto

### O Modelo Mental: Cobertura Como Piso por Quadrante, Não Profundidade num Só

O padrão Eval Coverage Matrix (`...patterns.md:15-35`) parte de uma observação: times de
agentes **sobre-investem num único estilo de avaliação** (quase sempre goldens offline) e
ficam cegos para modos de falha que moram em outras combinações de determinismo ×
deployment. A resposta é tratar o portfólio como matriz:

```
                     DETERMINÍSTICO          NÃO-DETERMINÍSTICO
                ┌─────────────────────────┬─────────────────────────┐
                │ goldens exatos          │ LLM-as-judge            │
   OFFLINE      │ constraint checks       │ behavioral path analysis│
                │ schema assertions       │ bulk trace analysis*    │
                ├─────────────────────────┼─────────────────────────┤
                │ métricas de produto     │ perceived-eval          │
   ONLINE       │ (latency, erro 5xx)     │ A/B + eval gates        │
                │ canary gates            │ online evaluators       │
                └─────────────────────────┴─────────────────────────┘
   * offline no deployment, não-determinístico no veredito —
     por isso o eixo "determinismo" é sobre o VEREDITO, não sobre o input
```

Três decisões de design que o exercício codifica:

1. **"A few things in each box" é piso, não meta.** O objetivo é que cada classe de modo
   de falha tenha ao menos um detector; profundidade além do piso é escolha de
   investimento, não virtude.
2. **O quadrante online/não-determinístico é o mais negligenciado** — e é onde vive o
   sinal percebido do usuário (Exercício 6). A matriz torna esse sinal first-class em vez
   de afterthought.
3. **Quadrantes escondem diferenças de custo.** O rótulo "online" não diz nada sobre o
   preço: A/B exige tráfego e stakes; perceived-eval é quase grátis (já está no
   transcript). O plano de alocação precisa enxergar custo, não só quadrante.

### O Que Você Vai Construir

1. `EvalMechanism` — o catálogo: nome, veredito determinístico ou não, offline/online,
   custo, status (`ACTIVE`/`PLANNED`/`MISSING`), mecanismos que o repo já tem como exemplos
2. `classify_mechanisms()` — atribuição 2x2 com a regra do veredito
3. `CoverageReport` — contagem por quadrante, gaps (quadrante abaixo do piso), e classe de
   modo de falha exposta por cada quadrante vazio
4. `AllocationPlan` — recomendação por gap: qual mecanismo construir primeiro, dado custo
   e restrições de observabilidade da equipe

---

## 📋 Cenário

O inventário de sábado (o do prólogo), formalizado:

| # | Mecanismo | Existe no repo? | Status |
|---|---|---|---|
| 1 | Golden question set (~150, single-turn) | sim (`workflow-derived-golden-question-set`) | ACTIVE |
| 2 | Constraint/structured checks | sim (`constraint-anchored-evaluation`) | ACTIVE |
| 3 | LLM-judge de similaridade | sim (`3-layer-evaluation-architecture` L2) | ACTIVE |
| 4 | N+1 long-session eval | sim (`n-plus-one-long-session-evals`) — mas o time do prólogo não roda | PLANNED |
| 5 | Behavioral path analysis | sim (`behavioral-eval-path-analysis`) | PLANNED |
| 6 | Perceived-eval (correção/abandono) | **não — Missing** (Exercício 6 constrói) | MISSING |
| 7 | A/B + canary com eval gates | parcial (`evals-ecommerce-koda`) | PLANNED |
| 8 | Bulk in-context trace analysis | não (Exercício 16 constrói) | MISSING |
| 9 | Métricas determinísticas de produção | parcial (telemetria local) | ACTIVE |

Restrições do time: 2 engenheiros, ~40k conversas/semana (humano não lê tudo),
capacidade de contatar ~10 clientes/semana.

---

## ✅ Requisitos

### Requisitos Funcionais

1. **RF1 — Dois eixos, veredito como chave:** cada `EvalMechanism` carrega
   `verdict_determinism` (`DETERMINISTIC`/`NONDETERMINISTIC`) e `deployment`
   (`OFFLINE`/`ONLINE`). O eixo determinismo classifica **o veredito**, não o input
   (goldens têm input fixo e veredito determinístico; LLM-judge tem input fixo e veredito
   não-determinístico).
2. **RF2 — Piso por quadrante:** `CoverageReport` calcula mecanismos `ACTIVE` por
   quadrante; quadrante com menos que `MIN_PER_QUADRANT` (default 2) entra na `gap_list`
   com a classe de modo de falha correspondente.
3. **RF3 — Gap mapeia modo de falha:** cada quadrante vazio lista o que fica invisível —
   offline/det: regressões de conteúdo exato; offline/nd: qualidade sem ground truth;
   online/det: degradação de produto/serviço; online/nd: qualidade percebida e
   comportamental em tráfego real.
4. **RF4 — Alerta de concentração:** portfólio com mecanismos `ACTIVE` >= 6 num único
   quadrante enquanto existe quadrante abaixo do piso gera `concentration_warning` —
   profundidade não compensa cegueira.
5. **RF5 — Alocação com restrições:** `AllocationPlan.recommend()` sugere, para cada gap,
   o mecanismo `MISSING`/`PLANNED` do quadrante com melhor razão (cobertura de modo de
   falha)/(custo), penalizado por exigir restrições que a equipe não tem (ex.: A/B exige
   tráfego segmentado; perceived-eval não exige nada que já não exista).
6. **RF6 — Piso não é teto:** o plano marca explicitamente `floor_not_target: true` —
   recomendar além do piso só quando o modo de falha já causou incidente.

### Requisitos Técnicos

1. **RT1 — Python 3.9+, stdlib apenas**, type hints obrigatórios
2. **RT2 — `dataclasses` + enums**; matriz representável como `dict[Quadrant, list[str]]`
3. **RT3 — Funções puras:** classificação e relatório não mutam o inventário
4. **RT4 — Imprimível:** `render_ascii()` desenha a matriz 2x2 com contagens

---

## 🏗️ Arquitetura do Sistema

```
┌──────────────────────────────────────────────────────────────────────┐
│                     EVAL COVERAGE MATRIX                              │
│                                                                       │
│  INVENTÁRIO (catalog de mecanismos)                                   │
│    EvalMechanism(name, verdict_determinism, deployment,               │
│                  cost_tier, status, failure_classes)                  │
│          │                                                            │
│          ▼                                                            │
│  ┌────────────────────────┐                                           │
│  │  classify_mechanisms   │  regra: eixo determinismo = VEREDITO      │
│  └──────────┬─────────────┘                                           │
│             ▼                                                         │
│  ┌───────────────────────────────────────────────┐                   │
│  │  COVERAGE REPORT                              │                   │
│  │  ┌──────────────┬──────────────┬───────────┐  │                   │
│  │  │ Quadrant     │ ACTIVE count │ gap?      │  │                   │
│  │  ├──────────────┼──────────────┼───────────┤  │                   │
│  │  │ OFFLINE/DET  │      3       │  ok       │  │                   │
│  │  │ OFFLINE/ND   │      1       │  GAP (<2) │  │                   │
│  │  │ ONLINE/DET   │      1       │  GAP (<2) │  │                   │
│  │  │ ONLINE/ND    │      0       │  GAP (0)  │  │  ← onde morava     │
│  │  └──────────────┴──────────────┴───────────┘  │    o incidente     │
│  │  concentration_warning quando >=6 num box     │                   │
│  │  + failure-mode class por quadrante vazio     │                   │
│  └──────────┬────────────────────────────────────┘                   │
│             ▼                                                         │
│  ┌───────────────────────────────────────────────┐                   │
│  │  ALLOCATION PLAN                              │                   │
│  │  gap ONLINE/ND → perceived-eval (custo baixo, │                   │
│  │                  sem restrição nova)          │                   │
│  │  gap OFFLINE/ND → behavioral path (planned)   │                   │
│  │  gap ONLINE/DET → canary gates (planned)      │                   │
│  │  floor_not_target: true                       │                   │
│  └───────────────────────────────────────────────┘                   │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 🎯 Sua Tarefa em 3 Partes

### Parte 1 — Diagnosticar a cegueira estruturada (10 min)

Com o inventário do starter: em qual quadrante estava o modo de falha do incidente (loop
em sessão longa com usuário real)? Por que nenhum dos mecanismos `ACTIVE` podia vê-lo?
Responda como comentário, citando qual mecanismo do inventário teria detectado o loop se
estivesse `ACTIVE`.

### Parte 2 — Matriz e relatório de cobertura (35 min)

Implemente `classify_mechanisms()` e `CoverageReport.build()`, incluindo `gap_list` com
classe de modo de falha, `concentration_warning` e `render_ascii()`.

### Parte 3 — Plano de alocação (20 min)

Implemente `AllocationPlan.recommend()`: para cada gap, ordene candidatos do quadrante por
(cobertura × disponibilidade)/(custo), respeitando as restrições do time. Verifique que
perceived-eval vem antes de A/B para o gap online/ND (mesma classe de modo de falha,
custo assimétrico).

---

## 💻 Starter Code

```python
"""
Exercício 7 — Eval Coverage Matrix
Nível 2 — Padrões Práticos

Represente o portfólio de evals como matriz 2x2 (determinismo do veredito ×
deployment), detecte quadrantes cegos e planeje alocação com piso por quadrante.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


# ============================================================================
# DATA MODELS
# ============================================================================

class VerdictDeterminism(Enum):
    """O VEREDITO do mecanismo é determinístico? (não o input)"""
    DETERMINISTIC = "deterministic"        # mesmo input → sempre mesmo veredito
    NONDETERMINISTIC = "nondeterministic"  # veredito envolve juiz/modelo/comportamento


class Deployment(Enum):
    OFFLINE = "offline"  # roda fora do tráfego real (CI, batch, harness)
    ONLINE = "online"    # roda sobre tráfego/produção (canary, A/B, telemetry)


class Quadrant(Enum):
    OFFLINE_DET = "offline+deterministic"
    OFFLINE_ND = "offline+nondeterministic"
    ONLINE_DET = "online+deterministic"
    ONLINE_ND = "online+nondeterministic"

    @classmethod
    def of(cls, d: VerdictDeterminism, dep: Deployment) -> "Quadrant":
        # TODO: implemente a atribuição 2x2
        raise NotImplementedError


class MechanismStatus(Enum):
    ACTIVE = "active"      # roda hoje (CI, agendado ou em produção)
    PLANNED = "planned"    # existe no repo/roadmap, ainda não roda
    MISSING = "missing"    # não existe em lugar nenhum


class CostTier(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


# Classes de modo de falha que ficam INVISÍVEIS quando o quadrante está vazio
FAILURE_MODE_BY_QUADRANT = {
    Quadrant.OFFLINE_DET: "regressões de conteúdo/formato exato",
    Quadrant.OFFLINE_ND: "qualidade sem ground truth único (coerência, julgamento)",
    Quadrant.ONLINE_DET: "degradação de serviço/produto (latência, erro, SLA)",
    Quadrant.ONLINE_ND: (
        "qualidade percebida e comportamental em tráfego real "
        "(loops longos, correção do usuário, abandono)"
    ),
}


@dataclass(frozen=True)
class EvalMechanism:
    name: str
    determinism: VerdictDeterminism
    deployment: Deployment
    status: MechanismStatus
    cost: CostTier
    # Exigências que a equipe pode não ter (para a alocação):
    requires_traffic_split: bool = False   # A/B precisa de segmentação
    requires_human_review_capacity: bool = False  # contato com clientes


@dataclass(frozen=True)
class CoverageGap:
    quadrant: Quadrant
    active_count: int
    failure_mode_exposed: str


@dataclass
class CoverageReport:
    matrix: dict[Quadrant, list[str]] = field(default_factory=dict)
    gap_list: list[CoverageGap] = field(default_factory=list)
    concentration_warning: str | None = None
    min_per_quadrant: int = 2

    @classmethod
    def build(
        cls, mechanisms: list[EvalMechanism], min_per_quadrant: int = 2
    ) -> "CoverageReport":
        """
        1. matriz: apenas mecanismos ACTIVE contam para cobertura
           (PLANNED/MISSING aparecem na renderização, mas não somam)
        2. gap: quadrante com ACTIVE < min_per_quadrant
        3. concentration_warning: >= 6 ACTIVE num quadrante enquanto
           outro quadrante está em gap
        """
        # TODO: implemente
        raise NotImplementedError

    def render_ascii(self) -> str:
        """Desenha a matriz 2x2 com contagens ACTIVE (e +planned/missing)."""
        # TODO: implemente
        raise NotImplementedError


@dataclass(frozen=True)
class Recommendation:
    gap: CoverageGap
    mechanism: EvalMechanism
    rationale: str
    floor_not_target: bool = True


@dataclass
class AllocationPlan:
    constraints_traffic_split_available: bool = False
    constraints_human_contact_per_week: int = 10
    recommendations: list[Recommendation] = field(default_factory=list)

    def recommend(self, report: CoverageReport, candidates: list[EvalMechanism]) -> None:
        """
        Para cada gap, escolha 1 mecanismo candidato do MESMO quadrante:
          score = cobertura_da_classe_de_falha / custo
          - custo: LOW=1, MEDIUM=2, HIGH=3
          - candidato que exige restrição ausente é penalizado (×2 de custo)
            ou descartado se a restrição for impossível (traffic split off)
          - desempate: MISSING > PLANNED (o que falta vale mais que o adiado)
        rationale em uma linha, citando a restrição considerada.
        """
        # TODO: implemente
        raise NotImplementedError


# ============================================================================
# FIXTURES — o inventário de sábado
# ============================================================================

def saturday_inventory() -> list[EvalMechanism]:
    return [
        EvalMechanism(
            "golden-question-set", VerdictDeterminism.DETERMINISTIC,
            Deployment.OFFLINE, MechanismStatus.ACTIVE, CostTier.LOW,
        ),
        EvalMechanism(
            "constraint-anchored-checks", VerdictDeterminism.DETERMINISTIC,
            Deployment.OFFLINE, MechanismStatus.ACTIVE, CostTier.LOW,
        ),
        EvalMechanism(
            "production-metrics-det", VerdictDeterminism.DETERMINISTIC,
            Deployment.ONLINE, MechanismStatus.ACTIVE, CostTier.LOW,
        ),
        EvalMechanism(
            "llm-judge-similarity", VerdictDeterminism.NONDETERMINISTIC,
            Deployment.OFFLINE, MechanismStatus.ACTIVE, CostTier.MEDIUM,
        ),
        # ── o restante: PLANNED / MISSING ──────────────────────────────
        EvalMechanism(
            "n-plus-one-long-session", VerdictDeterminism.DETERMINISTIC,
            Deployment.OFFLINE, MechanismStatus.PLANNED, CostTier.MEDIUM,
        ),
        EvalMechanism(
            "behavioral-path-analysis", VerdictDeterminism.NONDETERMINISTIC,
            Deployment.OFFLINE, MechanismStatus.PLANNED, CostTier.MEDIUM,
        ),
        EvalMechanism(
            "ab-canary-eval-gates", VerdictDeterminism.NONDETERMINISTIC,
            Deployment.ONLINE, MechanismStatus.PLANNED, CostTier.HIGH,
            requires_traffic_split=True,
        ),
        EvalMechanism(
            "perceived-eval", VerdictDeterminism.NONDETERMINISTIC,
            Deployment.ONLINE, MechanismStatus.MISSING, CostTier.LOW,
        ),
        EvalMechanism(
            "bulk-in-context-trace-analysis", VerdictDeterminism.NONDETERMINISTIC,
            Deployment.OFFLINE, MechanismStatus.MISSING, CostTier.MEDIUM,
            requires_human_review_capacity=True,
        ),
    ]


# ============================================================================
# TESTS
# ============================================================================

def test_classification_2x2():
    mech = saturday_inventory()
    by_name = {m.name: m for m in mech}
    q = Quadrant.of(
        by_name["llm-judge-similarity"].determinism,
        by_name["llm-judge-similarity"].deployment,
    )
    # LLM-judge: input fixo, VEREDITO não-determinístico → OFFLINE/ND
    assert q == Quadrant.OFFLINE_ND
    q2 = Quadrant.of(
        by_name["perceived-eval"].determinism,
        by_name["perceived-eval"].deployment,
    )
    assert q2 == Quadrant.ONLINE_ND
    print("TESTE 1 PASSOU")


def test_gaps_and_failure_modes():
    report = CoverageReport.build(saturday_inventory())
    gap_quadrants = {g.quadrant for g in report.gap_list}

    # ONLINE/ND está a zero — onde morava o incidente
    assert Quadrant.ONLINE_ND in gap_quadrants
    online_nd_gap = next(g for g in report.gap_list if g.quadrant == Quadrant.ONLINE_ND)
    assert online_nd_gap.active_count == 0
    assert "percebida" in online_nd_gap.failure_mode_exposed
    # OFFLINE/DET tem 2 ACTIVE (goldens + checks) → sem gap
    assert Quadrant.OFFLINE_DET not in gap_quadrants
    print("TESTE 2 PASSOU")


def test_concentration_warning():
    inventory = saturday_inventory()
    # inflar OFFLINE/DET com 4 mecanismos ACTIVE extras → concentração 6
    for extra in range(4):
        inventory.append(EvalMechanism(
            f"extra-det-{extra}", VerdictDeterminism.DETERMINISTIC,
            Deployment.OFFLINE, MechanismStatus.ACTIVE, CostTier.LOW,
        ))
    report = CoverageReport.build(inventory)
    assert report.concentration_warning is not None, (
        "6 ACTIVE num quadrante com outro em gap deve disparar warning"
    )
    print("TESTE 3 PASSOU")


def test_allocation_respects_constraints():
    report = CoverageReport.build(saturday_inventory())
    plan = AllocationPlan(constraints_traffic_split_available=False)
    plan.recommend(report, saturday_inventory())

    assert len(plan.recommendations) == len(report.gap_list)
    rec_online_nd = next(
        r for r in plan.recommendations
        if r.gap.quadrant == Quadrant.ONLINE_ND
    )
    # perceived-eval (LOW, sem restrição) ganha de A/B (HIGH, exige traffic split)
    assert rec_online_nd.mechanism.name == "perceived-eval"
    assert "traffic" in rec_online_nd.rationale or "custo" in rec_online_nd.rationale
    assert all(r.floor_not_target for r in plan.recommendations)
    print("TESTE 4 PASSOU")


if __name__ == "__main__":
    print("=" * 60)
    print("EXERCÍCIO 7: EVAL COVERAGE MATRIX")
    print("=" * 60)
    # Descomente após implementar:
    # test_classification_2x2()
    # test_gaps_and_failure_modes()
    # test_concentration_warning()
    # test_allocation_respects_constraints()
    print("\nTODO: implemente Quadrant.of, CoverageReport.build,")
    print("render_ascii e AllocationPlan.recommend")
```

---

## ✅ Validação: Critérios de Aceitação

Seu código será considerado **APROVADO** quando:

- [ ] `Quadrant.of()` classifica LLM-judge como `OFFLINE_ND` (veredito, não input) e perceived-eval como `ONLINE_ND`
- [ ] `CoverageReport.build()` detecta os 3 gaps do inventário de sábado, com `ONLINE_ND` a zero e a classe de modo de falha correta por gap
- [ ] `OFFLINE_DET` com 2 `ACTIVE` não gera gap (piso satisfeito)
- [ ] `concentration_warning` dispara no portfólio inflado (6 num box, outro em gap)
- [ ] `AllocationPlan.recommend()` escolhe perceived-eval sobre A/B para `ONLINE_ND`, com rationale citando a restrição (traffic split indisponível)
- [ ] Toda recomendação carrega `floor_not_target: true`
- [ ] `render_ascii()` imprime a matriz 2x2 legível com contagens

---

## 📊 Rubric de Avaliação

| Critério | Peso | Insuficiente (0-3) | Básico (4-6) | Proficiente (7-8) | Excelente (9-10) |
|---|---|---|---|---|---|
| **Classificação 2x2 (Parte 2)** | 25% | Não implementada | Eixos trocados | Atribuição correta | Regra do veredito explícita e documentada (input ≠ veredito) |
| **CoverageReport (Parte 2)** | 30% | Não implementado | Contagens sem gaps | Gaps com piso configurável | Gaps + classe de falha + concentration_warning + render |
| **AllocationPlan (Parte 3)** | 30% | Não implementado | Recomenda qualquer candidato do quadrante | Custo e restrições no score | Penalização/descarte por restrição, desempate MISSING>PLANNED, rationale citável |
| **Diagnóstico (Parte 1)** | 15% | Sem resposta | Incidente localizado sem quadrante | Quadrante + mecanismo que veria | Quadrante + mecanismo + por que os ACTIVE eram cegos por construção |

**Nota final:** Média ponderada. **Aprovação:** >= 7.0

---

## 💡 Dicas para Implementação

1. **O eixo determinismo classifica o veredito.** Essa é a pegadinha central: goldens e LLM-judge têm o mesmo input fixo — o que os separa é o juiz. Se sua regra olha para o input, LLM-judge cai no quadrante errado e a matriz inteira perde o sentido.
2. **Piso barato primeiro.** A alocação certa não é "o melhor mecanismo do quadrante" — é o melhor mecanismo *que a equipe consegue ligar esta semana*. Perceived-eval (Exercício 6) cobre a mesma classe de falha de um A/B com uma fração do custo e nenhuma restrição de tráfego.
3. **Concentração é sintoma, não erro.** O warning não proíbe profundidade; ele nomeia a assimetria. Um time pode decidir manter 6 mecanismos offline/det — mas a decisão deve ser explícita, com o gap na mesa.

---

## ❓ Dúvidas Comuns

**P: Isso substitui a 3-Layer Evaluation Architecture?**
R: Não — é ortogonal e complementar. As 3 layers estratificam por **o que** avaliam (`docs/canonical/3-layer-evaluation-architecture.md:28`); os tiers estratificam por **quando/custo** (`docs/canonical/eval-tier-stratification.md:32-36`); a matriz estratifica por **determinismo do veredito × deployment**. Mesmo mecanismo aparece nos três mapas com rótulos diferentes — e é exatamente essa multidimensionalidade que o portfólio precisa (`...classification.md:19`).

**P: Por que 2 por quadrante e não 1?**
R: O padrão pede "a few things in each box" (`...patterns.md:25`) — piso deliberadamente vago. O default 2 do exercício é conservador: com 1, qualquer falso positivo do mecanismo único do quadrante vira cegueira de novo. Configure conforme o contexto.

**P: Onde os mecanismos do repo se encaixam?**
R: O catálogo já existe, distribuído: goldens (`workflow-derived-golden-question-set`), checks (`constraint-anchored-evaluation`), LLM-judge (`3-layer-evaluation-architecture:45-59`), behavioral (`behavioral-eval-path-analysis`), A/B/canary (`evals-ecommerce-koda:107`), eval humano (`08-evaluation-rubrics`) — o que não existia era a matriz por cima deles (`...classification.md:24-25`).

**P: Bulk trace analysis é offline — por que não-determinístico?**
R: Porque o *veredito* (quais tendências existem) sai de um modelo raciocinando in-context, não de uma asserção fixa. Input offline, juiz não-determinístico: `OFFLINE_ND`. É o argumento inteiro do RF1.

---

## 🚀 Próximo Passo

Depois de completar este exercício:

1. Leia o padrão 1 completo e sua classificação: `docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-patterns.md:15-35` e `...classification.md:15-27` — Partial Coverage High: os mecanismos existiam, o vocabulário de portfólio não
2. Aplique a matriz ao portfólio real do KODA: quais mecanismos do repo estão `ACTIVE` de verdade no seu harness, e qual quadrante está vazio hoje?
3. Siga para o [[curriculum/03-nivel-3-advanced-architecture/exercises/exercise-13-production-offline-drift-taxonomy|Exercício 13: Production-to-Offline Feedback Loop with Drift Taxonomy]] — o mecanismo que mantém o quadrante offline honesto contra a deriva

---

*Exercício 7 | Nível 2 — Padrões Práticos | Eval Coverage Matrix*

**Suite verde em um quadrante é cegueira organizada. Algumas coisas em cada caixa.**
