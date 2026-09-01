---
title: "Exercício 13: Production-to-Offline Feedback Loop with Drift Taxonomy — Evals Verdes Não São Produto Saudável"
type: exercise
level: 3
aliases: ["production-to-offline feedback loop", "drift taxonomy", "taxonomia de drift", "data drift vs judge drift", "eval-set mirroring", "evals stale", "diagnóstico diferencial de evals", "production to offline loop"]
tags: [curriculo-conteudo, nivel-3, exercicio, evals, production, harness-engineering, governanca, drift-taxonomy, eval-refresh, use-case-classification, golden-annotation, python, dataclass]
relates-to: ["[[docs/canonical/production-to-offline-feedback-loop|Production-to-Offline Feedback Loop with Drift Taxonomy]]", "[[docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-patterns|Clay Eval Stack Patterns]]", "[[docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-classification|Clay Eval Stack Classification]]", "[[docs/canonical/production-failure-regression-flywheel|Production-Failure Regression Flywheel]]", "[[docs/canonical/living-eval-dataset|Living Eval Dataset]]", "[[docs/canonical/eval-to-production-correlation-tracking|Eval-to-Production Correlation Tracking]]", "[[docs/canonical/model-switch-driven-eval-hardening|Model-Switch-Driven Eval Hardening]]", "[[curriculum/02-nivel-2-practical-patterns/exercises/exercise-06-perceived-eval|Exercício 6: Perceived-Eval]]", "[[curriculum/02-nivel-2-practical-patterns/exercises/exercise-07-eval-coverage-matrix|Exercício 7: Eval Coverage Matrix]]", "[[curriculum/03-nivel-3-advanced-architecture/exercises/exercise-16-bulk-in-context-trace-analysis|Exercício 16: Bulk In-Context Trace Analysis]]"]
duration: "90-120 min"
last_updated: 2026-08-31
---

# 🩺 Exercício 13: Production-to-Offline Feedback Loop with Drift Taxonomy — Evals Verdes Não São Produto Saudável
## Nível 3 — Arquitetura Avançada

**Tempo Estimado:** 90-120 minutos
**Dificuldade:** (Avançado)
**Pré-requisito:** Ter lido `05-harness-evolution.md` (Nível 3) + `docs/canonical/production-failure-regression-flywheel.md` + Exercício 6 (Perceived-Eval)
**Objetivo:** Fechar o loop produção→offline que converte sinais de produção (tickets, correções de usuário, flags de online evaluators) em casos de eval duráveis — e implementar o diagnóstico diferencial que separa "as evals ficaram stale" em três modos distintos de deriva: data drift, judge drift e eval-set mirroring

---

## 📖 Prólogo: Três Meses de Verde, Um Produto Apodrecendo

### Terça-feira, reunião de métricas. O painel que ninguém queria explicar.

```
EVAL DASHBOARD (CI, últimos 90 dias):
  suite "koda-rec-v7":  150/150 PASS todos os dias. Verde. Sempre verde.

PRODUTO (mesmos 90 dias):
  CSAT do fluxo de recomendação:  4.6 → 4.1 → 3.7
  Tickets "assistente não entende":  12/mês → 58/mês
  Perceived-eval (Exercício 6):  correction_rate 8% → 24%

PM:  "as evals estão verdes há 3 meses e o produto caiu 0.9 no CSAT.
      As evals estão... stale?"

ENG1: "vamos revisar o golden set, então."
ENG2: "ou recalibrar o LLM-judge."
ENG3: "ou trocar os casos — must be outdated."

PM:  "qual dos três?"

ENG1/2/3: [silêncio]
```

**A mesma frase, três doenças diferentes:**

```
╔══════════════════════════════════════════════════════════════════╗
║      "AS EVALS ESTÃO STALE" — O DIAGNÓSTICO INDIFERENCIADO        ║
║                                                                  ║
║  O time disse UMA frase. O problema eram TRÊS falhas:            ║
║                                                                  ║
║  1. DATA DRIFT — o tráfego mudou, o eval set não acompanhou      ║
║     Nova feature "planos de assinatura" lançada; 31% do tráfego  ║
║     real agora são perguntas de assinatura. O eval set tem ZERO  ║
║     casos de assinatura. As evals estão certas sobre um mundo    ║
║     que não existe mais.                                         ║
║                                                                  ║
║  2. JUDGE DRIFT — o juiz ficou leniente                          ║
║     Troca silenciosa de modelo do LLM-judge em junho; acordo     ║
║     judge-vs-goldens-humanos caiu de 0.89 para 0.61. O judge     ║
║     aprova tudo; os 150 "PASS" valem pouco.                      ║
║                                                                  ║
║  3. EVAL-SET MIRRORING — o conjunto espelha a si mesmo           ║
║     62% dos casos do set são variações de 3 incidentes de março  ║
║     (duplicação por herança de "casos parecidos"). O set testa   ║
║     exaustivamente março. Produção está em agosto.               ║
║                                                                  ║
║  Os três remédios são DIFERENTES e INCOMPATÍVEIS entre si:       ║
║    data drift  → refresh de casos (puxar da produção)            ║
║    judge drift → recalibrar/revalidar o judge (goldens humanos)  ║
║    mirroring   → deduplicar e recompor a mistura do set          ║
║  Aplicar o remédio errado = 3 semanas perdidas.                  ║
╚══════════════════════════════════════════════════════════════════╝
```

**O loop existe no repo; a taxonomia não.** O flywheel de 9 passos que converte falha de
produção em caso de regressão durável é canônico e profundo
(`docs/canonical/production-failure-regression-flywheel.md:28-41`), com refresh cadence,
lifecycle de dataset e tracking de decaimento de correlação. O que **não existe em lugar
nenhum** é a taxonomia dos três modos de deriva — os greps de `judge drift|eval-set|data
drift|mirroring` em `docs/canonical/` dão zero (`...classification.md:59`). Sem ela, o
loop mais maduro do repo trata três doenças com um remédio só.

**Sua missão:** implementar o `DriftDiagnostician` — o diagnóstico diferencial que lê
distribuições de produção vs. eval set, acordo do judge contra goldens humanos e métricas
de duplicação do set, e nomeia o modo de deriva. Depois, fechar o `OfflineRefreshLoop`:
sinais de produção (tickets, eventos perceived-eval, flags de online evaluator) entram;
casos de eval refreshados e um diagnóstico de deriva saem.

---

## 🧠 O Contexto

### O Modelo Mental: Loop + Diagnóstico Diferencial

O padrão tem duas metades (`...patterns.md:58-79`):

**Metade 1 — o loop.** Produção vira eval continuamente:

```
 produção ──► sinais (tickets, correções de usuário, online evaluator,
             trace analysis findings)
                 │
                 ▼
           intake ──► captura ──► rotulagem ──► classificação de use case
                 │
                 ▼
           refresh do eval set (adicionar casos novos, podar redundância)
                 │
                 ▼
           eval set ◄──┐ (e o ciclo recomeça: produção sempre muda antes)
```

O repo já tem esta metade canonicamente: o flywheel de 9 passos
(`production-failure-regression-flywheel.md:28-41` — intake → capture → privacy → label →
dedup → tier → backfill → link → prune). O Exercício 6 construiu uma fonte de sinal
(perceived-eval events); o Exercício 16 construirá outra (findings de bulk analysis).

**Metade 2 — a taxonomia (o que falta).** Quando o loop não roda (ou roda devagar), o
eval set deriva da produção em três modos com causas, detectores e remédios distintos:

| Modo | Causa | Detector | Remédio |
|---|---|---|---|
| **Data drift** | Tráfego de produção mudou (novos use cases, novo mix) | Distribuição de use cases na produção ≠ distribuição no eval set | Refresh: puxar casos dos use cases sub-representados |
| **Judge drift** | O veredito do LLM-judge mudou (troca de modelo, prompt) sem revalidação | Acordo judge-vs-goldens-humanos caiu (os goldens anotados são a referência) | Revalidar/recalibrar o judge — refresh de casos não resolve |
| **Eval-set mirroring** | O set cresceu por herança/duplicação, não por amostragem | Alta duplicação interna + cobertura baixa dos top use cases reais | Deduplicar e recompor a mistura |

A regra de ouro do diagnóstico diferencial: **ele precisa dos três exames antes de
opinar** — porque os modos coexistem, e o remédio do data drift (adicionar casos)
piora o mirroring (mais duplicação) se aplicado às cegas.

### O Que Você Vai Construir

1. `UseCaseDistribution` — snapshot comparável de distribuição (produção vs. eval set),
   com divergência total (distância L1) por use case
2. `JudgeAgreementAudit` — acordo judge-vs-goldens-humanos sobre um conjunto de
   referência anotado (a defesa contra judge drift, exigida também por
   `model-switch-driven-eval-hardening`, SOR:301)
3. `SetDuplicationMetrics` — taxa de duplicação/near-dup do eval set + cobertura dos top
   use cases de produção
4. `DriftDiagnostician.diagnose()` — differential que emite `DriftDiagnosis` com o(s)
   modo(s), evidência e remédio prescrito
5. `OfflineRefreshLoop.run()` — sinais → intake → refresh (add/promote/prune) →
   re-diagnóstico (o loop fecha contra o próprio diagnóstico)

---

## 📋 Cenário

O estado do KODA em agosto/2026 (dados prontos no starter):

**Produção (classificada por use case):** 40k conversas/semana — `subscription_questions`
31%, `product_recommendation` 26%, `order_tracking` 22%, `allergy_constraints` 15%,
`small_talk` 6%.

**Eval set `koda-rec-v7` (150 casos):** `product_recommendation` 58% (sendo 62% das
mensagens variações de 3 incidentes de março), `order_tracking` 30%,
`allergy_constraints` 12%, `subscription_questions` **0%**, `small_talk` 0%.

**Judge:** `llm-judge-v3` — acordo com 40 goldens anotados por humanos: 0.61 (baseline
histórico 0.89; threshold de alerta 0.75).

**Sinais de produção da semana:** 58 tickets "não entende" (majoritariamente assinatura),
1.847 perceived-eval events com correção (Exercício 6), 9 flags de online evaluator.

---

## ✅ Requisitos

### Requisitos Funcionais

1. **RF1 — Distribuições comparáveis:** `UseCaseDistribution.l1_divergence()` retorna a
   divergência total contra outra distribuição e a lista de use cases
   sub-representados (share de produção ≥ 10% e share do set < 1/3 disso).
2. **RF2 — Auditoria do judge:** `JudgeAgreementAudit` recebe vereditos do judge e
   goldens humanos sobre o mesmo conjunto de referência e calcula `agreement`; abaixo de
   `alert_threshold` (0.75) o exame acusa judge drift.
3. **RF3 — Mirroring por duplicação:** `SetDuplicationMetrics` calcula `duplication_rate`
   (casos marcados como variantes de um mesmo incidente / total) e
   `top_usecase_coverage` (share dos top-3 use cases de produção cobertos pelo set);
   mirroring = duplicação ≥ 0.5 com cobertura < 0.6.
4. **RF4 — Diagnóstico diferencial:** `DriftDiagnostician.diagnose()` exige os **três
   exames**; emite um `DriftDiagnosis` com todos os modos detectados (podem coexistir),
   a evidência de cada um e o remédio prescrito por modo. Sem exame completo →
   `INCONCLUSIVE` com o exame faltante nomeado (nunca adivinha).
5. **RF5 — Prioridade de remédio:** quando judge drift coexiste com data drift, o
   diagnóstico ordena: primeiro judge (vereditos não confiáveis invalidam qualquer
   medição de qualidade dos novos casos), depois dados, depois mirroring.
6. **RF6 — Loop fecha:** `OfflineRefreshLoop.run()` consome sinais de produção (tickets +
   perceived-eval events + online evaluator flags), classifica use case, adiciona casos
   dos use cases sub-representados, poda duplicados, e o re-diagnóstico pós-refresh
   mostra data drift e mirroring resolvidos (judge drift permanece — é remédio de
   recalibração, não de refresh).
7. **RF7 — O loop sempre atrasa:** o refresh registra `lags_production: true` — o
   diagnóstico pós-refresh compara contra a produção *atual*, e qualquer use case novo
   desde então é drift de novo. (Honestidade estrutural, não bug.)

### Requisitos Técnicos

1. **RT1 — Python 3.9+, stdlib apenas**, type hints obrigatórios
2. **RT2 — `dataclasses` + enums**; `DriftMode` como `Flag` (modos coexistem)
3. **RT3 — Diagnóstico como função pura** dos três exames; sem I/O, sem estado oculto
4. **RT4 — Evidência citável:** cada modo no diagnóstico carrega os números que o
   evidenciam (divergência, acordo, duplicação)

---

## 🏗️ Arquitetura do Sistema

```
┌────────────────────────────────────────────────────────────────────────┐
│              PRODUCTION-TO-OFFLINE FEEDBACK LOOP                        │
│                                                                        │
│  SINAIS DE PRODUÇÃO                                                    │
│  ┌─────────────┐ ┌─────────────┐ ┌──────────────┐ ┌────────────────┐   │
│  │ tickets      │ │ perceived-  │ │ online       │ │ bulk trace     │   │
│  │ suporte      │ │ eval events │ │ evaluator    │ │ findings       │   │
│  │              │ │ (Exerc. 6)  │ │ flags        │ │ (Exerc. 16)    │   │
│  └──────┬──────┘ └──────┬──────┘ └──────┬───────┘ └───────┬────────┘   │
│         └───────────────┴───────┬───────┴─────────────────┘            │
│                                 ▼                                      │
│                     ┌───────────────────────┐                          │
│                     │  INTAKE + rotulagem   │                          │
│                     │  (use case classifier)│                          │
│                     └───────────┬───────────┘                          │
│                                 ▼                                      │
│   ┌──────────────────────────────────────────────────────────┐         │
│   │           DRIFT DIAGNOSTICIAN (diferencial)               │         │
│   │                                                           │         │
│   │  EXAME 1: distribuição    EXAME 2: acordo do judge        │         │
│   │  produção vs eval set     judge vs goldens humanos        │         │
│   │  L1 > 0.25 → DATA_DRIFT  agreement < 0.75 → JUDGE_DRIFT   │         │
│   │                                                           │         │
│   │  EXAME 3: duplicação do set                               │         │
│   │  dup >= 0.5 & cobertura < 0.6 → EVAL_SET_MIRRORING        │         │
│   │                                                           │         │
│   │  ordem de remédio: JUDGE → DATA → MIRRORING               │         │
│   └───────────────────────────┬───────────────────────────────┘         │
│                                 ▼                                      │
│                     ┌───────────────────────┐   refresh (add/promote/   │
│                     │  EVAL SET REFRESH     │   prune) + re-diagnóstico │
│                     │  koda-rec-v7 → v8     │   (RF7: sempre atrasado   │
│                     └───────────┬───────────┘   em relação à produção)  │
│                                 │                                      │
│                                 └──────────► eval set (offline)        │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 🎯 Sua Tarefa em 3 Partes

### Parte 1 — Diagnóstico qualitativo (15 min)

Com o painel do cenário (sem código): nomeie o(s) modo(s) de deriva presentes e a ordem
de remédio. Justifique em comentário por que "adicionar casos de assinatura" sozinho não
resolve — qual modo piora e qual permanece intocado?

### Parte 2 — O diagnóstico diferencial (45 min)

Implemente `UseCaseDistribution.l1_divergence()`, `JudgeAgreementAudit.agreement()`,
`SetDuplicationMetrics` e `DriftDiagnostician.diagnose()` com a ordem de remédio do RF5.

### Parte 3 — Fechar o loop (40 min)

Implemente `OfflineRefreshLoop.run()`: intake dos sinais → refresh → re-diagnóstico.
Verifique que o refresh resolve data drift e mirroring mas não judge drift (RF6), e que o
loop declara seu atraso estrutural (RF7).

---

## 💻 Starter Code

```python
"""
Exercício 13 — Production-to-Offline Feedback Loop with Drift Taxonomy
Nível 3 — Arquitetura Avançada

Feche o loop produção→offline e implemente o diagnóstico diferencial que
separa "evals stale" em três modos: data drift, judge drift, eval-set mirroring.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, Flag, auto


# ============================================================================
# DATA MODELS
# ============================================================================

class DriftMode(Flag):
    """Modos de deriva — coexistem."""
    NONE = 0
    DATA_DRIFT = auto()         # tráfego mudou, o set não acompanhou
    JUDGE_DRIFT = auto()        # o juiz mudou sem revalidação
    EVAL_SET_MIRRORING = auto()  # o set espelha a si mesmo (duplicação)

    @property
    def remedy(self) -> str:
        return {
            DriftMode.DATA_DRIFT: "refresh: puxar casos dos use cases sub-representados",
            DriftMode.JUDGE_DRIFT: "recalibrar: revalidar judge contra goldens humanos",
            DriftMode.EVAL_SET_MIRRORING: "recompor: deduplicar e rebalancear o set",
        }.get(self, "nenhum")


@dataclass(frozen=True)
class UseCaseDistribution:
    """Snapshot de distribuição de use cases (produção OU eval set)."""
    source: str                        # "production" | "eval-set-v7"
    total: int                         # conversas ou casos
    shares: dict[str, float]           # use_case → fração [0.0, 1.0]

    def l1_divergence(self, other: "UseCaseDistribution") -> float:
        """Divergência total: sum |share_self - share_other| sobre a união."""
        # TODO: implemente
        raise NotImplementedError

    def underrepresented(
        self, production: "UseCaseDistribution", floor: float = 0.10
    ) -> list[tuple[str, float, float]]:
        """
        Use cases com share de produção >= floor cujo share aqui é < 1/3
        disso. Retorna (use_case, prod_share, set_share).
        """
        # TODO: implemente
        raise NotImplementedError


@dataclass(frozen=True)
class JudgeAgreementAudit:
    """Exame 2: o judge ainda concorda com humanos?"""
    judge_verdicts: tuple[bool, ...]    # PASS/FAIL do judge por golden
    human_verdicts: tuple[bool, ...]    # PASS/FAIL do humano por golden
    alert_threshold: float = 0.75

    @property
    def agreement(self) -> float:
        """Fração de vereditos idênticos sobre o MESMO conjunto."""
        # TODO: implemente
        raise NotImplementedError

    @property
    def is_drifted(self) -> bool:
        # TODO: implemente
        raise NotImplementedError


@dataclass(frozen=True)
class EvalSetComposition:
    """Composição do eval set para o exame 3."""
    case_count: int
    variant_of_incident: dict[str, int]  # incidente-originário → n. de variantes
    cases_by_use_case: dict[str, int]

    @property
    def duplication_rate(self) -> float:
        """
        Fração de casos que são variantes de um incidente existente.
        Um caso original de cada incidente não é duplicata; as variantes sim.
        """
        # TODO: implemente
        raise NotImplementedError

    def top_usecase_coverage(
        self, production: UseCaseDistribution, top_n: int = 3
    ) -> float:
        """
        Soma dos shares do set (normalizados a 1.0) sobre os top-N use
        cases de produção por share.
        """
        # TODO: implemente
        raise NotImplementedError


@dataclass(frozen=True)
class DriftEvidence:
    numbers: dict[str, float]   # evidência citável: l1, agreement, dup...
    detail: str


@dataclass(frozen=True)
class DriftDiagnosis:
    modes: DriftMode
    evidence: dict[DriftMode, DriftEvidence]
    remedy_order: list[DriftMode]
    inconclusive_missing_exam: str | None = None


@dataclass(frozen=True)
class ProductionSignal:
    """Um sinal de produção pronto para intake (já rotulado)."""
    signal_id: str
    kind: str                 # "ticket" | "perceived_eval_event" | "online_evaluator_flag"
    use_case: str
    transcript_excerpt: str


class DriftDiagnostician:
    """Diagnóstico diferencial — função pura dos três exames."""

    L1_ALERT = 0.25
    DUP_RATE_ALERT = 0.50
    COVERAGE_FLOOR = 0.60

    def diagnose(
        self,
        production: UseCaseDistribution,
        eval_set: UseCaseDistribution,
        composition: EvalSetComposition,
        judge_audit: JudgeAgreementAudit | None = None,
    ) -> DriftDiagnosis:
        """
        Regras:
          DATA_DRIFT: l1_divergence > L1_ALERT (evidência: l1 + underrepresented)
          JUDGE_DRIFT: judge audit presente e is_drifted (evidência: agreement)
          MIRRORING: duplication_rate >= DUP_RATE_ALERT e
                     top_usecase_coverage < COVERAGE_FLOOR
          Sem judge_audit → modes não incluem JUDGE_DRIFT, mas o diagnóstico
          é INCONCLUSIVE para judge (exame faltante nomeado) — RF4: nunca adivinha.
          remedy_order: JUDGE primeiro, depois DATA, depois MIRRORING (RF5).
        """
        # TODO: implemente
        raise NotImplementedError


# ============================================================================
# PARTE 3 — O LOOP
# ============================================================================

@dataclass
class RefreshResult:
    added_cases: list[str] = field(default_factory=list)
    pruned_cases: list[str] = field(default_factory=list)
    new_set_version: str = ""
    post_refresh_diagnosis: DriftDiagnosis | None = None
    lags_production: bool = True   # RF7: honestidade estrutural


class OfflineRefreshLoop:
    """
    Sinais de produção → intake (use case) → refresh → re-diagnóstico.
    O refresh resolve o que refresh resolve; judge drift é remédio à parte.
    """

    def __init__(self, diagnostician: DriftDiagnostician) -> None:
        self.diagnostician = diagnostician

    def run(
        self,
        signals: list[ProductionSignal],
        production: UseCaseDistribution,
        eval_set: UseCaseDistribution,
        composition: EvalSetComposition,
        judge_audit: JudgeAgreementAudit | None = None,
    ) -> RefreshResult:
        """
        1. diagnose() ANTES do refresh (pré-existentes contam como contexto)
        2. intake: agrupe signals por use_case; para cada use case
           sub-representado com sinais, adicione casos (1 caso por 3 sinais,
           mínimo 1, cap de 15 por use case — o flywheel tem dedup/tier depois)
        3. prune: reduza variantes de incidentes até duplication_rate < 0.30
        4. re-diagnose com a NOVA composição (RF6: data/mirroring resolvem,
           judge drift permanece) e marque lags_production
        """
        # TODO: implemente
        raise NotImplementedError


# ============================================================================
# FIXTURES — o estado de agosto/2026 do cenário
# ============================================================================

def production_august() -> UseCaseDistribution:
    return UseCaseDistribution("production", 40_000, {
        "subscription_questions": 0.31,
        "product_recommendation": 0.26,
        "order_tracking": 0.22,
        "allergy_constraints": 0.15,
        "small_talk": 0.06,
    })


def eval_set_v7() -> UseCaseDistribution:
    return UseCaseDistribution("eval-set-v7", 150, {
        "product_recommendation": 0.58,
        "order_tracking": 0.30,
        "allergy_constraints": 0.12,
        # subscription_questions: 0% — o buraco do data drift
        # small_talk: 0%
    })


def eval_set_v7_composition() -> EvalSetComposition:
    # 62% dos casos de recomendação são variantes de 3 incidentes de março
    return EvalSetComposition(
        case_count=150,
        variant_of_incident={
            "INC-2026-03-011-whey-loop": 29,
            "INC-2026-03-019-creatina-gluten": 33,
            "INC-2026-03-027-pretreino-preco": 25,
        },
        cases_by_use_case={
            "product_recommendation": 87,   # 58% de 150
            "order_tracking": 45,           # 30%
            "allergy_constraints": 18,      # 12%
        },
    )


def judge_audit_august() -> JudgeAgreementAudit:
    """Acordo 0.61: 40 goldens, judge erra 15 deles (baseline 0.89)."""
    human = (True,) * 28 + (False,) * 12
    judge = (True,) * 25 + (False,) * 0 + (True,) * 12 + (False,) * 3
    # 25 acertos nos True + 0... construa explicitamente abaixo
    judge = tuple(
        [True] * 24 + [False] * 4 + [True] * 11 + [False] * 1
    )
    return JudgeAgreementAudit(
        judge_verdicts=tuple(judge),
        human_verdicts=human,
    )


def week_signals() -> list[ProductionSignal]:
    """58 tickets + 1847 perceived-eval (amostrados como 20) + 9 flags."""
    signals: list[ProductionSignal] = []
    for i in range(20):  # amostra dos tickets de assinatura
        signals.append(ProductionSignal(
            f"TICK-{i}", "ticket", "subscription_questions",
            "cliente pergunta como trocar o plano e o agente responde com produto",
        ))
    for i in range(20):  # amostra dos perceived-eval events (Exercício 6)
        signals.append(ProductionSignal(
            f"PEE-{i}", "perceived_eval_event", "subscription_questions",
            "correção do usuário: 'não é isso, é sobre meu plano'",
        ))
    for i in range(9):   # flags do online evaluator
        signals.append(ProductionSignal(
            f"OEE-{i}", "online_evaluator_flag", "allergy_constraints",
            "flag: resposta ignorou restrição declarada no perfil",
        ))
    return signals


# ============================================================================
# TESTS
# ============================================================================

def test_l1_and_underrepresented():
    prod, eset = production_august(), eval_set_v7()
    l1 = eset.l1_divergence(prod)
    # |0-0.31| + |0.58-0.26| + |0.30-0.22| + |0.12-0.15| + |0-0.06| = 0.74
    assert abs(l1 - 0.74) < 1e-6, f"L1 esperado 0.74, obtido {l1:.4f}"
    under = dict(eset.underrepresented(prod))
    assert "subscription_questions" in under, (
        "31% da produção com 0% no set é o sub-representado óbvio"
    )
    assert under["subscription_questions"][1] >= 0.10
    print("TESTE 1 PASSOU")


def test_judge_audit():
    audit = judge_audit_august()
    # 40 goldens; judge concorda em 24+... calcule: o fixture deve dar 0.61
    assert 0.55 <= audit.agreement <= 0.70, (
        f"agreement esperado ~0.61, obtido {audit.agreement:.2f}"
    )
    assert audit.is_drifted, "0.61 < 0.75 → judge drift"
    print("TESTE 2 PASSOU")


def test_differential_diagnosis():
    diag = DriftDiagnostician().diagnose(
        production_august(), eval_set_v7(),
        eval_set_v7_composition(), judge_audit_august(),
    )
    # Os TRÊS modos coexistem no cenário
    assert DriftMode.DATA_DRIFT in diag.modes
    assert DriftMode.JUDGE_DRIFT in diag.modes
    assert DriftMode.EVAL_SET_MIRRORING in diag.modes
    # Remédio: judge primeiro (RF5)
    assert diag.remedy_order[0] == DriftMode.JUDGE_DRIFT
    # Evidência citável presente
    assert "agreement" in diag.evidence[DriftMode.JUDGE_DRIFT].numbers
    assert "l1" in diag.evidence[DriftMode.DATA_DRIFT].numbers
    print("TESTE 3 PASSOU")


def test_inconclusive_without_exam():
    diag = DriftDiagnostician().diagnose(
        production_august(), eval_set_v7(),
        eval_set_v7_composition(), judge_audit=None,
    )
    assert DriftMode.JUDGE_DRIFT not in diag.modes
    assert diag.inconclusive_missing_exam is not None, (
        "sem auditoria do judge o diagnóstico declara o exame faltante"
    )
    print("TESTE 4 PASSOU")


def test_loop_closes():
    loop = OfflineRefreshLoop(DriftDiagnostician())
    result = loop.run(
        week_signals(), production_august(), eval_set_v7(),
        eval_set_v7_composition(), judge_audit_august(),
    )
    post = result.post_refresh_diagnosis
    assert post is not None
    assert DriftMode.DATA_DRIFT not in post.modes, (
        "refresh puxou casos de assinatura → data drift resolvido"
    )
    assert DriftMode.EVAL_SET_MIRRORING not in post.modes, (
        "prune de variantes → mirroring resolvido"
    )
    assert DriftMode.JUDGE_DRIFT in post.modes, (
        "judge drift NÃO é resolúvel com refresh de casos (RF6)"
    )
    assert result.lags_production is True
    assert any("subscription" in c for c in result.added_cases)
    print("TESTE 5 PASSOU")


if __name__ == "__main__":
    print("=" * 60)
    print("EXERCÍCIO 13: PRODUCTION-TO-OFFLINE + DRIFT TAXONOMY")
    print("=" * 60)
    # Descomente após implementar:
    # test_l1_and_underrepresented()
    # test_judge_audit()
    # test_differential_diagnosis()
    # test_inconclusive_without_exam()
    # test_loop_closes()
    print("\nTODO: implemente distribuições, exames, DriftDiagnostician")
    print("e OfflineRefreshLoop")
```

---

## ✅ Validação: Critérios de Aceitação

Seu código será considerado **APROVADO** quando:

- [ ] `l1_divergence()` retorna 0.74 para o par produção/set do cenário e identifica `subscription_questions` como sub-representado
- [ ] `JudgeAgreementAudit` calcula acordo ~0.61 e acusa deriva (< 0.75)
- [ ] `duplication_rate` reflete as 87 variantes de 3 incidentes de março (≈ 0.56 — os originais não contam como duplicata)
- [ ] `diagnose()` detecta os **três** modos simultaneamente, com remédio ordenado JUDGE → DATA → MIRRORING e evidência numérica citável
- [ ] Sem auditoria do judge, o diagnóstico é `INCONCLUSIVE` para judge com o exame faltante nomeado — nunca adivinha (RF4)
- [ ] `OfflineRefreshLoop.run()` resolve data drift e mirroring no re-diagnóstico, mantém judge drift, adiciona casos de assinatura e poda variantes
- [ ] O refresh declara `lags_production: true` (RF7)

---

## 📊 Rubric de Avaliação

| Critério | Peso | Insuficiente (0-3) | Básico (4-6) | Proficiente (7-8) | Excelente (9-10) |
|---|---|---|---|---|---|
| **Exames (Parte 2)** | 25% | Não implementados | Um exame correto | Três exames corretos | Três exames com evidência citável e thresholds nomeados |
| **Diagnóstico diferencial (Parte 2)** | 30% | Não implementado | Um modo por vez, sem coexistência | Flag-based, modos coexistem | Coexistência + ordem de remédio + INCONCLUSIVE sem exame |
| **Loop (Parte 3)** | 30% | Não implementado | Adiciona casos sem re-diagnóstico | Refresh + re-diagnóstico corretos | Add/promote/prune com caps + judge drift intocado + lags_production |
| **Diagnóstico qualitativo (Parte 1)** | 15% | Sem resposta | Um modo identificado | Três modos + ordem | Três modos + por que o remédio único piora um deles |

**Nota final:** Média ponderada. **Aprovação:** >= 7.0

---

## 💡 Dicas para Implementação

1. **Judge primeiro é lógica de medição, não preferência.** Se o veredito do judge não é confiável, o "PASS" dos novos casos puxados da produção não significa nada — você estaria calibrando contra uma régua torta. Recalibrar a régua vem antes de medir com ela.
2. **Original não é duplicata.** No `duplication_rate`, cada incidente-originário contribui com 1 caso legítimo; só as *variantes* contam. Se sua taxa deu 0.58 em vez de ~0.56, você contou os originais.
3. **Mirroring e data drift pioram um ao outro.** A resposta intuitiva ao data drift ("adicionar casos parecidos com os que já tenho, por segurança") é exatamente o que produz mirroring. O prune de variantes é parte do mesmo refresh, não uma etapa opcional — é o passo `dedup` do flywheel canônico (`production-failure-regression-flywheel.md:28-41`).
4. **O loop é declaradamente imperfeito.** A fonte chama o setup de "the hardest part" e declara não-resolvido em escala (`...patterns.md:60`). Modelar `lags_production` não é pessimismo — é impedir que o time trate o set v8 como em dia.

---

## ❓ Dúvidas Comuns

**P: Por que goldens anotados por humanos são obrigatórios para detectar judge drift?**
R: Porque o drift do judge é invisível de dentro: o judge sempre concorda consigo mesmo. Só uma referência externa ao juiz (humanos) detecta que o juiz mudou. É o mesmo princípio de `model-switch-driven-eval-hardening` (SOR:301): toda troca de modelo dispara revalidação completa do dataset — aqui, revalidação do *juiz* contra as anotações.

**P: Isso não é o flywheel de produção que já existe no repo?**
R: A metade loop, sim — e por isso este exercício a reutiliza em vez de reinventar. O delta é a taxonomia: o flywheel responde "como converter falha em caso durável"; o diagnostician responde "por que o set parou de representar a produção" — pergunta que o flywheel não faz (`...classification.md:51`).

**P: L1 é a distância certa? Poderia ser Jensen-Shannon.**
R: Poderia — JS é simétrica e limitada, L1 é mais simples de explicar e auditar. O que não é negociável é comparar distribuições de *use case*, não de tokens: a unidade de drift aqui é o mix de trabalho que o agente recebe.

**P: O que muda se os três modos apontarem para o mesmo use case?**
R: Nada na ordem dos remédios — eles são sobre *mecanismo*, não sobre use case. O refresh adiciona casos; a recomposição deduplica; a recalibração do judge é ortogonal ao conteúdo dos casos.

---

## 🚀 Próximo Passo

Depois de completar este exercício:

1. Leia o padrão 3 completo e sua classificação: `docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-patterns.md:58-79` e `...classification.md:47-61` — o loop mais coberto do batch, a taxonomia NOT_FOUND
2. Compare com `docs/canonical/eval-to-production-correlation-tracking.md:38-39` — decay thresholds e recalibration triggers são drift-adjacentes; sua taxonomia dá nome ao que lá é sintoma
3. Siga para o [[curriculum/03-nivel-3-advanced-architecture/exercises/exercise-14-unified-tool-surface-flywheel|Exercício 14: Unified Tool Surface Flywheel]] — o outro loop que transforma falha observada em melhoria, agora na superfície de tools

---

*Exercício 13 | Nível 3 — Arquitetura Avançada | Production-to-Offline Feedback Loop with Drift Taxonomy*

**"As evals estão stale" são três doenças com uma frase. Diagnóstico diferencial antes de receitar.**
