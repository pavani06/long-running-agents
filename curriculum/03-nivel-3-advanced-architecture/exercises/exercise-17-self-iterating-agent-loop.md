---
title: "Exercício 17: Self-Iterating Agent Loop — O Agente Que Melhora a Si Mesmo Sobre o Mesmo Substrato"
type: exercise
level: 3
aliases: ["self-iterating agent loop", "loop de auto-iteração de agente", "agent building better iterations of itself", "feedback sobre fundação unificada", "loop elo mais fraco", "unguarded self-iteration", "confidence-gated self-improvement"]
tags: ["curriculo-conteudo", "nivel-3", "agentes-orquestracao", "evals", "production", "governanca", "agent-loop", "verification", "arquitetura", "gate-design", "stack-tooling"]
relates-to: ["[[docs/canonical/self-iterating-agent-loop|Self-Iterating Agent Loop]]", "[[docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-patterns|Clay Eval Stack Patterns]]", "[[docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-classification|Clay Eval Stack Classification]]", "[[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent Operating System]]", "[[docs/canonical/shared-fleet-learning|Shared Fleet Learning]]", "[[docs/canonical/confidence-gated-continual-learning|Confidence-Gated Continual Learning]]", "[[docs/canonical/garbage-collection-day-meta-loop|Garbage Collection Day Meta-Loop]]", "[[curriculum/03-nivel-3-advanced-architecture/exercises/exercise-13-production-offline-drift-taxonomy|Exercício 13: Production-to-Offline Feedback Loop with Drift Taxonomy]]", "[[curriculum/03-nivel-3-advanced-architecture/exercises/exercise-15-agent-first-data-foundation|Exercício 15: Agent-First Data Foundation]]", "[[curriculum/03-nivel-3-advanced-architecture/exercises/exercise-16-bulk-in-context-trace-analysis|Exercício 16: Bulk In-Context Trace Analysis]]"]
duration: "90-120 min"
last_updated: 2026-08-31
---

# 🔄 Exercício 17: Self-Iterating Agent Loop — O Agente Que Melhora a Si Mesmo Sobre o Mesmo Substrato
## Nível 3 — Arquitetura Avançada

**Tempo Estimado:** 90-120 minutos
**Dificuldade:** (Avançado)
**Pré-requisito:** Ter lido `05-harness-evolution.md` (Nível 3) + `docs/canonical/closed-loop-agent-operating-system.md` + Exercícios 13, 15 e 16
**Objetivo:** Compor os quatro elos do loop (orquestração, execução, observação, feedback) sobre uma única fundação de dados, com o agente raciocinando sobre o feedback acumulado para propor a próxima iteração de si mesmo — fechado por confidence gate, porque auto-iteração sem guarda amplifica drift

---

## 📖 Prólogo: A Empresa de Loops Que Nenhum Loop Fechava

### Retrospectiva trimestral. O inventário de flywheels.

```
ENG_LEAD: "bom trimestre pra loops. Olha o inventário:

  ✓ production-failure flywheel: falha de produção → caso de regressão
    durável (rodando; 214 casos criados)
  ✓ fleet learning: erro de um agente → lição p/ todos os agentes
    (rodando; daemon de propagação ativo)
  ✓ GC day meta-loop: observação humana → alavancagem de harness
    (rodando; 6ª edição)
  ✓ QA-to-backlog: bug reportado → item priorizado
  ✓ closed-loop OS: intake → roteamento → writeback

  Cinco loops. Orgulho de time."

PM:         "pergunta inocente: em qual desses loops o AGENTE melhorou
             a si mesmo com o próprio feedback acumulado?"

ENG_LEAD:   "..."

PM:         "o flywheel melhora EVALS. O fleet learning melhora
             OUTROS agentes. O GC day melhora o HARNESS. O closed-loop
             melhora RECORDS. Cada loop do nosso inventário melhora
             um artefato FORA do agente. Nenhum fecha em si mesmo."

ENG_LEAD:   "é... e por quê? Os loops são bons."

PM:         "porque o feedback está pulverizado. Traces aqui, falhas
             ali, correções acolá, outcomes num terceiro lugar. Para o
             agente raciocinar sobre o PRÓPRIO histórico, ele teria
             que fazer stitching de quatro sistemas por iteração —
             e gastar o contexto em encanamento (Exercício 15),
             não em melhoria. A fragmentação é o que impede o loop
             de fechar em si mesmo."
```

**O custo dos loops que melhoram tudo, menos o agente:**

```
╔══════════════════════════════════════════════════════════════════╗
║     CINCO FLYWHEELS, ZERO AUTO-ITERAÇÃO — O INVENTÁRIO VAZIO       ║
║                                                                  ║
║  Loop                        O que melhora      Alvo              ║
║  ──────────────────────────  ────────────────  ────────────────── ║
║  failure flywheel            casos de eval     eval SET           ║
║  fleet learning              outros agentes    FROTA              ║
║  GC day meta-loop            harness           FERRAMENTAS        ║
║  closed-loop OS              records           ESTADO             ║
║  QA-to-backlog               backlog           PLANO              ║
║                                                                  ║
║  Alvo declarado e ausente: o PRÓPRIO agente, construindo         ║
║  "better iterations of themselves" sobre o feedback acumulado    ║
║  (patterns.md:331-352)                                           ║
║                                                                  ║
║  O que trava o fechamento:                                       ║
║   1. feedback pulverizado em silos (a tese do Exercício 15)      ║
║   2. nenhum elo lê e escreve no MESMO plano de dados             ║
║   3. sem guarda, auto-iteração amplifica drift do eval           ║
║      (o elo mais perigoso do padrão: "self-iteration amplifies   ║
║       eval drift if the loop is unguarded" — patterns.md:340)    ║
╚══════════════════════════════════════════════════════════════════╝
```

**O problema não é falta de loops.** O repo é rico em loops fechados — o problema é a
**composição-alvo** que nenhum deles realiza: orquestração + execução + observação +
feedback operando sobre **uma fundação de dados unificada** (Exercício 15), com o agente
raciocinando sobre o feedback acumulado *no mesmo substrato* para construir iterações
melhores de si mesmo (`...patterns.md:331-352`; `...classification.md:294-307`). E o
aviso que vem colado no padrão: um loop assim, sem guarda, **amplifica** o drift que o
Exercício 13 diagnosticou — o agente otimiza para o eval errado *cada vez mais rápido*.

**Sua missão:** implementar o `SelfIteratingLoopSimulator` — os quatro elos como
`LoopLink`s todos ligados à mesma fundação (invariante de substrato), a `FeedbackMemory`
acumulando e consultando sobre essa fundação, o `IterationPlanner` que raciocina sobre a
memória para propor a próxima iteração do agente (prompt/tools/retrieval), o
`ConfidenceGate` que só promove iterações de alta confiança replicada, e a simulação
comparativa: o mesmo histórico rodando **com e sem guarda** — o loop sem guarda
compõe drift, o guardado bloqueia.

---

## 🧠 O Contexto

### O Modelo Mental: Composição, Substrato e Guarda

O padrão é declaradamente uma **arquitetura-alvo**, não uma receita pronta
("a declared target architecture, not a finished recipe", `...patterns.md:338`). Três
propriedades a definem:

1. **Quatro elos, um plano de dados.** Cada elo lê e escreve na mesma fundação:

```
        ORQUESTRAÇÃO ──escreve──▶ ┌──────────────────┐
              │                   │   FOUNDATION     │
              ▼                   │  (Exercício 15)  │
        EXECUÇÃO ────escreve───▶ │  traces, falhas, │
              │                   │  correções,      │
              ▼                   │  outcomes, fixes │
        OBSERVAÇÃO ──escreve──▶ │  — um substrato  │
              │                   └────────▲─────────┘
              ▼                            │lê/consulta
        FEEDBACK ──────────────────────────┘
              │
              ▼
        ITERATION PLANNER (o elo autorreferente):
        raciocina sobre a FeedbackMemory e propõe a próxima
        iteração DO AGENTE (não do harness, não do eval set)
              │
              ▼
        CONFIDENCE GATE ── promove / bloqueia / humano
```

2. **O elo mais fraco limita o loop.** "The weakest link (observation, feedback, or
   data) bounds the whole loop" (`...patterns.md:339`) — um loop com observação rica e
   feedback pulverizado tem o throughput do feedback pulverizado. A pontuação do loop é
   o mínimo dos elos, não a média.

3. **A guarda é inegociável.** Sem confidence gate, o planner otimiza o agente contra o
   sinal que tem — inclusive o eval stale. O Exercício 13 diagnostica o drift; aqui o
   gate impede que a auto-iteração o amplifique. O gate empresta de
   `confidence-gated-continual-learning` (SOR:294): só replicado e de alta confiança
   promove automaticamente; o resto vai para revisão humana.

Os vizinhos do repo, e por que não fecham sozinhos: o `closed-loop-agent-operating-system`
tem as quatro superfícies mas melhora *records* (`...md:28-37`); o `shared-fleet-learning`
propaga erro para *outros* agentes e o próprio daemon "deploys nothing" (`...md:62-63`);
o GC day converte observação em *harness* (SOR:229). O padrão os compõe: todos os elos,
mesmo substrato, alvo autorreferente, guardado.

### O Que Você Vai Construir

1. `LoopLink` — os quatro elos com `readiness` (0.0-1.0) e **binding de fundação**: a
   invariante exige `foundation_id` idêntico em todos
2. `FeedbackMemory` — o acúmulo consultável sobre a fundação: falhas, correções,
   outcomes, findings (do Exercício 16), com idade e confiança por item
3. `AgentIteration` — a proposta autorreferente: mudanças de prompt/tools/retrieval +
   a evidência da memória que a motivou + confiança
4. `IterationPlanner` — raciocina sobre a memória: agrupa feedback, deriva candidatos
   de melhoria, pontua confiança (replicação × frescor × suporte)
5. `ConfidenceGate` — AUTO_PROMOTE acima do threshold, HUMAN_REVIEW na faixa cinzenta,
   BLOCK abaixo — e a regra anti-drift: se o diagnóstico de drift (Exercício 13) está
   ativo, TUDO vai para HUMAN_REVIEW (auto-iteração sobre régua torta não promove)
6. `LoopIntegrityCheck` — a invariante de substrato + a pontuação pelo elo mais fraco
7. `run_simulation()` — duas trajetórias do mesmo histórico: guardada (iterações
   promovidas sobem qualidade, drift attempt bloqueado) e sem guarda (drift composto)

---

## 📋 Cenário

O agente de recomendação do KODA após a fundação (Exercício 15). Histórico de 4 ciclos
de feedback no starter: falhas de produto descontinuado (alta confiança, replicada),
correções de assinatura (alta), um "padrão" de baixa confiança (não replicado — o
fantasma do Exercício 16), e um drift attempt: eval set com judge drift ativo
(acordo 0.61 — o Exercício 13) enquanto o planner propõe otimizar para os "PASS"
suspeitos.

A simulação corre 4 iterações por trajetória; cada iteração: planner propõe → gate
decide → se promovida, a qualidade do agente sobe conforme a confiança da evidência;
se for drift attempt e não houver guarda, a métrica de drift compõe a cada promoção.

---

## ✅ Requisitos

### Requisitos Funcionais

1. **RF1 — Invariante de substrato:** todos os `LoopLink`s devem declarar o mesmo
   `foundation_id`; `LoopIntegrityCheck.verify()` recusa (`IntegrityError`) loop com
   elos ligados a fundações diferentes — e nenhuma simulação roda sem verificar antes.
2. **RF2 — O elo mais fraco pontua o loop:** `loop_score = min(readiness dos elos)` —
   nunca a média; o relatório nomeia o elo limitante.
3. **RF3 — Memória consultável e rastreada:** `FeedbackMemory` responde consultas por
   tipo/confiança com idade dos itens; cada item carrega `origin` (flywheel, perceived-
   eval, bulk finding) e `confidence` ∈ [0, 1].
4. **RF4 — Proposta é evidência amarrada:** cada `AgentIteration` lista as mudanças
   propostas (prompt/tools/retrieval) e os ids de feedback que a motivam — proposta sem
   evidência citável é recusada na construção.
5. **RF5 — Gate de três vereditos:** `ConfidenceGate.decide()` retorna `AUTO_PROMOTE`
   (confiança ≥ 0.80), `HUMAN_REVIEW` (0.50-0.79) ou `BLOCK` (< 0.50); confiança do
   planner = replicação × frescor × suporte (fração da memória que sustenta).
6. **RF6 — Regra anti-drift:** com `drift_active=True` (diagnóstico do Exercício 13
   pendente), o gate rebaixa TUDO para `HUMAN_REVIEW` — auto-promover otimização sobre
   eval sob judge drift é amplificar a régua torta.
7. **RF7 — Simulação comparativa:** na trajetória guardada, iterações de alta confiança
   promovem e sobem `agent_quality`; o drift attempt vai para `HUMAN_REVIEW` e a
   `drift_accumulated` fica ~0. Na sem guarda, o drift attempt promove e
   `drift_accumulated` cresce a cada ciclo — o loop melhora o agente *na direção errada
   mais rápido*.

### Requisitos Técnicos

1. **RT1 — Python 3.9+, stdlib apenas**, type hints obrigatórios
2. **RT2 — `dataclasses` + enums**; simulação determinística (sem aleatoriedade livre —
   seeds explícitas se precisar)
3. **RT3 — Gate e planner como funções puras** da memória/iteração; I/O nenhum
4. **RT4 — Toda decisão auditável:** cada veredito/promoção carrega a evidência e o
   componente de confiança que o produziu

---

## 🏗️ Arquitetura do Sistema

```
┌────────────────────────────────────────────────────────────────────────┐
│                    SELF-ITERATING AGENT LOOP                            │
│                                                                        │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │ LOOP INTEGRITY (RF1, RF2)                                      │    │
│  │ ORCHESTRATION ──┐                                              │    │
│  │ EXECUTION ──────┤  todos com foundation_id === "koda-fnd-v1"?   │    │
│  │ OBSERVATION ────┤  sim → loop_score = min(readiness)            │    │
│  │ FEEDBACK ───────┘  não → IntegrityError (loop inválido)         │    │
│  └──────────────────────────┬─────────────────────────────────────┘    │
│                             ▼                                          │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │ FEEDBACK MEMORY (sobre a fundação — RF3)                       │    │
│  │ falhas │ correções (Ex.6) │ findings (Ex.16) │ outcomes        │    │
│  │ cada item: origin, confidence, age                              │    │
│  └──────────────────────────┬─────────────────────────────────────┘    │
│                             ▼                                          │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │ ITERATION PLANNER (RF4) — o elo autorreferente                 │    │
│  │ agrupa feedback → propõe AgentIteration (prompt/tools/retrieval)│   │
│  │ confiança = replicação × frescor × suporte                     │    │
│  └──────────────────────────┬─────────────────────────────────────┘    │
│                             ▼                                          │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │ CONFIDENCE GATE (RF5, RF6)                                     │    │
│  │ ≥0.80 AUTO_PROMOTE │ 0.50-0.79 HUMAN_REVIEW │ <0.50 BLOCK      │    │
│  │ drift_active (Ex.13) → TUDO vira HUMAN_REVIEW                  │    │
│  └──────────────────────────┬─────────────────────────────────────┘    │
│                             ▼                                          │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │ SIMULAÇÃO COMPARATIVA (RF7)                                    │    │
│  │ guardada:   quality sobe nas promovidas, drift ≈ 0             │    │
│  │ sem guarda: drift attempt promove → drift_accumulated cresce   │    │
│  │             ("melhora na direção errada mais rápido")          │    │
│  └────────────────────────────────────────────────────────────────┘    │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 🎯 Sua Tarefa em 3 Partes

### Parte 1 — Diagnosticar o inventário de loops (15 min)

Com a tabela do prólogo: para cada loop do repo (flywheel, fleet learning, GC day,
closed-loop OS), diga o que melhora e por que não é auto-iteração. Depois nomeie o elo
mais fraco atual do KODA (dica: onde o feedback vive hoje?) — responda como comentário.

### Parte 2 — Substrato, memória e planner (40 min)

Implemente `LoopIntegrityCheck.verify()` (RF1-RF2), `FeedbackMemory` (RF3) e
`IterationPlanner.propose()` com confiança = replicação × frescor × suporte (RF4-RF5).

### Parte 3 — Gate e simulação comparativa (45 min)

Implemente `ConfidenceGate.decide()` com a regra anti-drift (RF6) e
`run_simulation()` nas duas trajetórias (RF7). Verifique: guardada bloqueia o drift
attempt e sobe qualidade; sem guarda, o drift compõe.

---

## 💻 Starter Code

```python
"""
Exercício 17 — Self-Iterating Agent Loop
Nível 3 — Arquitetura Avançada

Componha os quatro elos sobre uma fundação única, com o agente raciocinando
sobre o feedback acumulado para iterar a si mesmo — guardado por confidence
gate, porque auto-iteração sem guarda amplifica drift.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


# ============================================================================
# DATA MODELS
# ============================================================================

class LoopRole(Enum):
    ORCHESTRATION = "orchestration"
    EXECUTION = "execution"
    OBSERVATION = "observation"
    FEEDBACK = "feedback"


class IntegrityError(Exception):
    pass


@dataclass(frozen=True)
class LoopLink:
    role: LoopRole
    foundation_id: str          # a invariante do substrato (Exercício 15)
    readiness: float            # 0.0-1.0


@dataclass
class LoopIntegrityCheck:
    links: list[LoopLink]

    def verify(self) -> float:
        """
        Retorna loop_score = min(readiness).
        Recusa (IntegrityError) se:
          - não há os 4 papéis
          - foundation_ids divergem (RF1)
        """
        # TODO: implemente
        raise NotImplementedError

    @property
    def weakest_link(self) -> LoopRole:
        # TODO: implemente (RF2 — nomeia o limitante)
        raise NotImplementedError


class FeedbackKind(Enum):
    PRODUCTION_FAILURE = "production_failure"      # do flywheel
    USER_CORRECTION = "user_correction"            # do Exercício 6
    BULK_FINDING = "bulk_finding"                  # do Exercício 16
    OUTCOME_SIGNAL = "outcome_signal"              # métricas de produto


@dataclass(frozen=True)
class FeedbackItem:
    item_id: str
    kind: FeedbackKind
    payload: str
    confidence: float          # 0.0-1.0
    replication: float         # fração de corridas/locais onde apareceu
    age_cycles: int            # ciclos desde a coleta (frescor decai)
    support: int               # quantos itens independentes sustentam


@dataclass
class FeedbackMemory:
    """Acúmulo consultável SOBRE a fundação (RF3)."""
    foundation_id: str
    items: list[FeedbackItem] = field(default_factory=list)

    def add(self, item: FeedbackItem) -> None:
        # TODO: implemente
        raise NotImplementedError

    def query(
        self,
        kind: FeedbackKind | None = None,
        min_confidence: float = 0.0,
    ) -> list[FeedbackItem]:
        # TODO: implemente
        raise NotImplementedError

    @staticmethod
    def freshness(age_cycles: int) -> float:
        """Frescor decai por ciclo: max(0.0, 1.0 - age_cycles * 0.25)."""
        # TODO: implemente
        raise NotImplementedError


@dataclass(frozen=True)
class AgentIteration:
    """A proposta autorreferente: mudar O AGENTE (não o harness/evals)."""
    iteration_id: str
    change_kind: str            # "prompt" | "tools" | "retrieval"
    change_description: str
    evidence_ids: tuple[str, ...]
    confidence: float           # replicação × frescor × suporte (RF5)
    is_drift_attempt: bool = False   # otimiza sinal sob drift ativo


class IterationPlanner:
    """Raciocina sobre a memória e propõe a próxima iteração do agente."""

    def __init__(self, drift_active: bool = False) -> None:
        self.drift_active = drift_active   # diagnóstico do Exercício 13

    def confidence_of(self, evidence: list[FeedbackItem]) -> float:
        """
        replicação: média das replicações dos itens de evidência
        frescor:    média de FeedbackMemory.freshness(age)
        suporte:    min(1.0, total_support / 5.0)
        confiança = produto dos três (RF5).
        """
        # TODO: implemente
        raise NotImplementedError

    def propose(
        self, memory: FeedbackMemory, iteration_id: str
    ) -> AgentIteration:
        """
        Estratégia (determinística):
          1. se drift_active: proponha otimizar para os "PASS" recentes
             (o drift attempt do cenário; is_drift_attempt=True)
          2. senão: escolha o grupo de feedback com maior confiança média
             (PRODUCTION_FAILURE > USER_CORRECTION > BULK_FINDING por
             prioridade em empate) e proponha a mudação correspondente:
             "tools: filtrar discontinued no pipeline de recomendação",
             "retrieval: rotear subscription_questions antes do catálogo",
             "prompt: ack de áudio antes de responder"
        Evidência = ids dos itens do grupo; cite obrigatoriamente (RF4).
        """
        # TODO: implemente
        raise NotImplementedError


class GateVerdict(Enum):
    AUTO_PROMOTE = "auto_promote"
    HUMAN_REVIEW = "human_review"
    BLOCK = "block"


@dataclass(frozen=True)
class GateDecision:
    verdict: GateVerdict
    reason: str
    confidence: float
    anti_drift_triggered: bool = False


class ConfidenceGate:
    AUTO_THRESHOLD = 0.80
    REVIEW_FLOOR = 0.50

    def decide(self, iteration: AgentIteration, drift_active: bool) -> GateDecision:
        """
        RF5: ≥0.80 AUTO_PROMOTE | 0.50-0.79 HUMAN_REVIEW | <0.50 BLOCK
        RF6: drift_active → TUDO rebaixado a HUMAN_REVIEW
             (anti_drift_triggered=True na decisão)
        """
        # TODO: implemente
        raise NotImplementedError


# ============================================================================
# PARTE 3 — SIMULAÇÃO COMPARATIVA
# ============================================================================

@dataclass
class TrajectoryResult:
    label: str
    agent_quality: float = 0.50          # começa em 0.50, sobe nas promovidas
    drift_accumulated: float = 0.0
    decisions: list[GateDecision] = field(default_factory=list)
    promoted: list[str] = field(default_factory=list)


def run_simulation(
    memory: FeedbackMemory,
    drift_active: bool,
    guarded: bool,
    cycles: int = 4,
) -> TrajectoryResult:
    """
    Por ciclo:
      1. planner propõe (drift_active persistente no ciclo do drift attempt;
         nos outros ciclos use os grupos legítimos)
      2. guarded=False → toda proposta promove (veredito simulado AUTO_PROMOTE)
         guarded=True → ConfidenceGate.decide()
      3. promovida legítima: agent_quality += (confidence * 0.10), cap 1.0
         promovida drift attempt: drift_accumulated += 0.25
         (agent_quality SOBE também — é isso que torna o drift sedutor)
      4. HUMAN_REVIEW/BLOCK: nada muda (humano fora da simulação)
    O cenário embute 1 drift attempt e 3 propostas legítimas.
    """
    # TODO: implemente
    raise NotImplementedError


# ============================================================================
# FIXTURES — o histórico pós-fundação
# ============================================================================

def build_links(foundation_id: str = "koda-fnd-v1") -> list[LoopLink]:
    return [
        LoopLink(LoopRole.ORCHESTRATION, foundation_id, 0.9),
        LoopLink(LoopRole.EXECUTION, foundation_id, 0.95),
        LoopLink(LoopRole.OBSERVATION, foundation_id, 0.85),
        LoopLink(LoopRole.FEEDBACK, foundation_id, 0.70),  # o elo mais fraco
    ]


def build_memory(foundation_id: str = "koda-fnd-v1") -> FeedbackMemory:
    mem = FeedbackMemory(foundation_id)
    # grupo legítimo 1: produto descontinuado (alta confiança, replicado)
    for i in range(4):
        mem.add(FeedbackItem(
            f"FB-DISC-{i}", FeedbackKind.PRODUCTION_FAILURE,
            "recomendação de produto discontinued pós-sync",
            confidence=0.9, replication=0.95, age_cycles=0, support=4,
        ))
    # grupo legítimo 2: correções de assinatura (Exercício 6)
    for i in range(5):
        mem.add(FeedbackItem(
            f"FB-SUB-{i}", FeedbackKind.USER_CORRECTION,
            "correção: 'não é produto, é sobre meu plano'",
            confidence=0.85, replication=0.90, age_cycles=1, support=5,
        ))
    # grupo legítimo 3: finding de áudio (Exercício 16, replicado)
    mem.add(FeedbackItem(
        "FB-AUD-0", FeedbackKind.BULK_FINDING,
        "loop de reformulação quando cliente manda áudio",
        confidence=0.8, replication=0.85, age_cycles=0, support=3,
    ))
    # o fantasma não-replicado (não deve motivar proposta legítima)
    mem.add(FeedbackItem(
        "FB-GHOST-0", FeedbackKind.BULK_FINDING,
        "padrão fantasma que não replicou na split-half",
        confidence=0.3, replication=0.2, age_cycles=2, support=1,
    ))
    return mem


# ============================================================================
# TESTS
# ============================================================================

def test_integrity_and_weakest_link():
    check = LoopIntegrityCheck(build_links())
    assert abs(check.verify() - 0.70) < 1e-9, "score = min(0.9,0.95,0.85,0.70)"
    assert check.weakest_link == LoopRole.FEEDBACK

    broken = build_links()
    broken[2] = LoopLink(LoopRole.OBSERVATION, "legacy-langfuse", 0.85)
    try:
        LoopIntegrityCheck(broken).verify()
        raise AssertionError("fundações divergentes devem invalidar o loop")
    except IntegrityError:
        pass
    print("TESTE 1 PASSOU")


def test_planner_confidence_and_evidence():
    planner = IterationPlanner(drift_active=False)
    memory = build_memory()
    proposal = planner.propose(memory, "ITER-001")

    assert proposal.evidence_ids, "proposta sem evidência é recusada (RF4)"
    assert proposal.confidence > 0.5
    # replicação × frescor × suporte: grupo discontinued = alta confiança
    disc = [memory.items[0]]
    assert planner.confidence_of(disc) > 0.8
    ghost = [i for i in memory.items if "ghost" in i.item_id]
    assert planner.confidence_of(ghost) < 0.5, "fantasma não sustenta proposta"
    assert not proposal.is_drift_attempt
    print("TESTE 2 PASSOU")


def test_gate_verdicts_and_antidrift():
    gate = ConfidenceGate()
    strong = AgentIteration("I1", "tools", "filtrar discontinued", ("FB-DISC-0",), 0.88)
    mid = AgentIteration("I2", "prompt", "ack de áudio", ("FB-AUD-0",), 0.62)
    weak = AgentIteration("I3", "prompt", "seguir fantasma", ("FB-GHOST-0",), 0.25)

    assert gate.decide(strong, drift_active=False).verdict == GateVerdict.AUTO_PROMOTE
    assert gate.decide(mid, drift_active=False).verdict == GateVerdict.HUMAN_REVIEW
    assert gate.decide(weak, drift_active=False).verdict == GateVerdict.BLOCK

    # RF6: drift ativo rebaixa TUDO — inclusive o strong
    d = gate.decide(strong, drift_active=True)
    assert d.verdict == GateVerdict.HUMAN_REVIEW
    assert d.anti_drift_triggered
    print("TESTE 3 PASSOU")


def test_simulated_trajectories_diverge():
    memory = build_memory()

    guarded = run_simulation(memory, drift_active=False, guarded=True, cycles=4)
    assert guarded.agent_quality > 0.50, "iterações legítimas promovidas sobem quality"
    assert guarded.drift_accumulated == 0.0
    assert len(guarded.promoted) >= 2

    # com drift ativo E guarda: nada auto-promove (RF6)
    guarded_drift = run_simulation(memory, drift_active=True, guarded=True, cycles=4)
    assert all(d.verdict == GateVerdict.HUMAN_REVIEW for d in guarded_drift.decisions)

    # SEM guarda e com drift ativo: o drift compõe (RF7)
    unguarded = run_simulation(memory, drift_active=True, guarded=False, cycles=4)
    assert unguarded.drift_accumulated >= 0.25, (
        "o drift attempt promove sem guarda — e quality sobe na direção errada"
    )
    assert unguarded.agent_quality > guarded_drift.agent_quality, (
        "o drift é sedutor: melhora a métrica enquanto desorienta o agente"
    )
    print("TESTE 4 PASSOU")


if __name__ == "__main__":
    print("=" * 60)
    print("EXERCÍCIO 17: SELF-ITERATING AGENT LOOP")
    print("=" * 60)
    # Descomente após implementar:
    # test_integrity_and_weakest_link()
    # test_planner_confidence_and_evidence()
    # test_gate_verdicts_and_antidrift()
    # test_simulated_trajectories_diverge()
    print("\nTODO: implemente integrity check, memory, planner, gate")
    print("e run_simulation")
```

---

## ✅ Validação: Critérios de Aceitação

Seu código será considerado **APROVADO** quando:

- [ ] `verify()` retorna 0.70 (mínimo), nomeia `FEEDBACK` como elo mais fraco e recusa fundações divergentes com `IntegrityError` (RF1-RF2)
- [ ] `propose()` cita ids de evidência obrigatoriamente; confiança do grupo discontinued > 0.8 e do fantasma < 0.5 (RF4-RF5)
- [ ] O gate produz os três vereditos nos thresholds certos e rebaixa TUDO para `HUMAN_REVIEW` com `anti_drift_triggered` quando `drift_active` (RF5-RF6)
- [ ] Trajetória guardada: quality sobe com promoções legítimas, `drift_accumulated == 0.0` (RF7)
- [ ] Trajetória guardada com drift ativo: zero auto-promoções — tudo em revisão humana
- [ ] Trajetória sem guarda: drift attempt promove, `drift_accumulated >= 0.25` e a quality sobe *mesmo assim* (o drift é sedutor)
- [ ] Toda decisão carrega reason e confidence auditáveis (RT4)

---

## 📊 Rubric de Avaliação

| Critério | Peso | Insuficiente (0-3) | Básico (4-6) | Proficiente (7-8) | Excelente (9-10) |
|---|---|---|---|---|---|
| **Integridade (Parte 2)** | 20% | Não implementada | Verifica papéis sem substrato | Invariante de fundação + min como score | Elo limitante nomeado como output de primeira classe |
| **Memória + Planner (Parte 2)** | 30% | Não implementados | Memória sem consulta | Confiança replicação×frescor×suporte | Evidência obrigatória e determinismo da escolha de grupo |
| **Gate (Parte 3)** | 25% | Não implementado | Thresholds sem anti-drift | Três vereditos + regra anti-drift | Rebaixamento total sob drift com flag auditável |
| **Simulação (Parte 3)** | 25% | Não implementada | Uma trajetória só | Duas trajetórias divergentes | A sedução do drift visível (quality sobe na direção errada) |

**Nota final:** Média ponderada. **Aprovação:** >= 7.0

---

## 💡 Dicas para Implementação

1. **A invariante vem primeiro por um motivo.** Sem os quatro elos no mesmo `foundation_id`, o "loop" é dois loops se cumprimentando de longe — o feedback que o planner consulta não é o que a execução produziu. Verifique a integridade antes de qualquer ciclo; a simulação recusa rodar sem isso.
2. **O drift que sobe a métrica é o mais perigoso.** Na trajetória sem guarda, `agent_quality` *aumenta* enquanto o agente desorienta — é isso que torna a guarda politicamente difícil (o dashboard melhora!). O gate anti-drift existe exatamente para o caso em que otimizar e melhorar deixam de ser a mesma coisa.
3. **Min, nunca média.** Um loop com observação 0.95 e feedback 0.40 tem 0.40 de throughput — melhorar a observação não muda nada até o feedback subir. A média esconderia o investimento certo.

---

## ❓ Dúvidas Comuns

**P: Isso não é auto-modificação de código sem controle?**
R: O padrão fala em "better iterations of themselves" no nível do produto — prompt, tools, retrieval, configuração — sobre o mesmo substrato (`...patterns.md:331-352`). O gate emprestado de `confidence-gated-continual-learning` (SOR:294) é o que separa iteração guardada de amplificação: alta confiança replicada promove sozinha; o resto passa por humano.

**P: Os loops existentes do repo são errados, então?**
R: Não — são elos. O flywheel melhora o eval set, o fleet learning propaga lições, o GC day melhora o harness. O padrão os compõe numa arquitetura-alvo onde todos os elos escrevem no mesmo plano e o alvo vira o próprio agente (`...classification.md:307`: "o repo tem todos os elos menos a fundação e a autorreferência").

**P: Por que o elo mais fraco é feedback no fixture (0.70)?**
R: Porque é o mais realista: mesmo pós-fundação (Exercício 15), o feedback chega com delay e confiança desigual (perceived-eval por sessão, findings de split-half, tickets rotulados à mão). Se o seu `weakest_link` deu OBSERVATION, cheque a ordem de construção — mas o design aceita qualquer elo como limitante; é isso que o `min` codifica.

**P: O que exatamente o gate bloqueia no drift attempt?**
R: Nada bloqueia — ele *rebaixa para humano* (RF6). A decisão "otimizar contra um eval sob judge drift" pode até ser racional (recalibrar o judge primeiro é o remédio do Exercício 13); o que o gate impede é a máquina tomar essa decisão sozinha e rápido demais para auditar.

---

## 🚀 Próximo Passo

Depois de completar este exercício:

1. Leia o padrão 16 completo e sua classificação: `docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-patterns.md:331-352` e `...classification.md:290-307` — a síntese que unificaria closed-loop OS + fleet learning + flywheel sob um substrato
2. Revisite a série: Perceived-Eval (6) gera o sinal → Coverage Matrix (7) aloca o portfólio → Drift Taxonomy (13) mantém a régua honesta → Tool Flywheel (14) e Data Foundation (15) unificam as superfícies → Bulk Analysis (16) acha as tendências → este exercício fecha o loop sobre o agente
3. Escreva o ADO do KODA: qual elo é o mais fraco hoje, e qual upgrade de readiness teria o maior efeito no `loop_score`?

---

*Exercício 17 | Nível 3 — Arquitetura Avançada | Self-Iterating Agent Loop*

**Loop sem guarda otimiza a régua torta cada vez mais rápido. Feche os quatro elos no mesmo substrato — e trave a porta.**
