---
title: "Exercício 22: Capability Escalation Ladder — O Degrau Certo na Ordem Certa, Decidido pela Economia"
type: exercise
level: 3
aliases: ["capability escalation ladder", "escada de escalonamento de capacidade", "capability budget instruction architecture", "economic winner entre rotas", "violation counts como sinal direcional", "four rungs"]
tags: ["curriculo-conteudo", "nivel-3", "agentes-orquestracao", "harness-engineering", "evals", "arquitetura", "production"]
relates-to: ["[[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-patterns|Padrões The Prompting Playbook]]", "[[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-classification|Classificação The Prompting Playbook]]", "[[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-mental-model|Mental Model: The Prompting Playbook]]", "[[docs/canonical/task-routed-model-tiering|Task-Routed Model Tiering]]", "[[docs/canonical/generator-evaluator|Generator-Evaluator]]", "[[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]]", "[[docs/canonical/model-switching-architecture-enterprise-eval-gate|Model-Switching Architecture Enterprise Eval Gate]]", "[[docs/canonical/tested-degradation-ladder|Tested Degradation Ladder]]", "[[curriculum/02-nivel-2-practical-patterns/exercises/exercise-08-defensive-patch-ledger|Exercício 8: Defensive Patch Ledger]]", "[[curriculum/02-nivel-2-practical-patterns/exercises/exercise-09-two-sided-trade-off-instruction|Exercício 9: Two-Sided Trade-off Instruction]]", "[[curriculum/03-nivel-3-advanced-architecture/exercises/exercise-21-agent-kernel-runtime|Exercício 21: Agent Kernel Runtime]]"]
duration: "90-120 min"
last_updated: 2026-09-02
---

# 🪜 Exercício 22: Capability Escalation Ladder — O Degrau Certo na Ordem Certa, Decidido pela Economia
## Nível 3 — Arquitetura Avançada

**Tempo Estimado:** 90-120 minutos
**Dificuldade:** (Avançado)
**Pré-requisito:** Ter lido `05-harness-evolution.md` (Nível 3) + `docs/canonical/task-routed-model-tiering.md` + `docs/canonical/generator-evaluator.md`; recomendados os [[curriculum/02-nivel-2-practical-patterns/exercises/exercise-08-defensive-patch-ledger|Exercício 8]] e [[curriculum/02-nivel-2-practical-patterns/exercises/exercise-09-two-sided-trade-off-instruction|Exercício 9]] (mesma família do fonte)
**Objetivo:** Substituir o chute de alavanca (modelo maior? mais thinking? prompt melhor? decompor?) por um protocolo ORDENADO de escalonamento de capacidade — capability, budget, instruction, architecture — em que cada degrau é medido em pass/fail, violation count, tokens e latência, e o vencedor é ECONÔMICO entre as rotas que passam

---

## 📖 Prólogo: O Time Que Comprou um Modelo Caro Para Resolver um Problema de Arquitetura

### Terça-feira, 16h47. War room: a task de recomendação complexa do KODA reprova 5/5 no eval.

```
LEAD:      "a task 'consolidated multi-item recommendation' está
            0/5 no eval do tier-1. O cliente de enterprise paga por
            ela. Precisamos disso passando até sexta."

ENG_A:     "fácil: sobe pro tier-3. Modelo maior resolve."
ENG_B:     "caro. Mexe no reasoning budget primeiro — adaptive
            thinking. Metade do custo."
ENG_C:     "ou a gente decompõe: um agente gera por item, um
            evaluator checa, um repairer corrige. Eu consigo
            esboçar hoje."

LEAD:      "três propostas, zero dados. Quem testa o quê?"

ENG_A:     "eu já subi pro tier-3 ontem, num branch. Passa 5/5.
            Mas olha a fatura: 3,1x os tokens por caso e latência
            média de 9s. O da semana passada — 5s."

LEAD:      "passou o eval e reprovou a economia. E agora é sexta
            e a gente tem UM dado medido de UMA rota. O protocolo
            aqui era alguém chutar uma alavanca e torcer."

ENG_C:     "e o pior: ninguém anotou os violation counts do caminho.
            O tier-1 com instruction melhorava de 0/5 pra 2/5 —
            pass/fail não mexeu, mas as violações caíram de 9 pra 6.
            Sinal direcional. Se a gente tivesse a escalada
            ORDENADA, teria visto isso ANTES de pagar o tier-3."

LEAD:      "então fica o combinado: ninguém mais puxa alavanca de
            capacidade sem subir a escada — degrau por degrau,
            medindo custo, e o vencedor é o mais barato que passa."
```

**O custo do escalonamento sem protocolo:**

```
╔══════════════════════════════════════════════════════════════════╗
║   UMA TASK FALHANDO, TRÊS CHUTES, NENHUMA MEDIDA COMPLETA          ║
║                                                                  ║
║  Task: consolidated multi-item recommendation (enterprise)       ║
║  Eval: 5 casos, tier-1 (atual): 0/5, 9 violações de constraint   ║
║                                                                  ║
║  O que o time fez:                                               ║
║   ✓ ENG_A puxou CAPABILITY (tier-3) — 5/5, mas 3,1x tokens,      ║
║     9s/caso — "passou o eval, reprovou a economia"               ║
║   ✓ ENG_B SUGERIU budget — nunca mediu                           ║
║   ✓ ENG_C SUGERIU decomposição — nunca mediu                     ║
║   ✗ ninguém mediu instruction como degrau                         ║
║   ✗ ninguém registrou violation counts ao longo do caminho       ║
║                                                                  ║
║  O que faltava — a escada do fonte (patterns.md:118-122):        ║
║   1. CAPABILITY (modelo maior)                                   ║
║   2. REASONING BUDGET (adaptive thinking)                        ║
║   3. INSTRUCTION (prompt melhor)                                 ║
║   4. ARCHITECTURE (decomposição em agentes simples)              ║
║   cada degrau medido: pass/fail + violações + tokens + latência; ║
║   vencedor ECONÔMICO entre os que passam — no fonte, foi o       ║
║   ÚLTIMO degrau (patterns.md:126)                                ║
╚══════════════════════════════════════════════════════════════════╝
```

**O problema não é escolher a alavanca errada.** Cada alavanca do fonte é
legítima — modelo maior, reasoning budget, instrução, decomposição. O
problema é o **chute sem ordem e sem medida**: "teams guess which lever to
pull; ad hoc ordering wastes spend and hides the economic winner"
(`...patterns.md:115`). O repo do curso tem cada alavanca isolada — tiering
para rotear custo por subtask (`docs/canonical/task-routed-model-tiering.md:32`),
generator-evaluator como escolha de arquitetura
(`docs/canonical/generator-evaluator.md:31`), lifecycle com disciplina de ROI
(`docs/canonical/measured-harness-evolution-lifecycle.md`) — mas **nenhum
procedimento ordenado que as percorra para uma task que reprova**, e nenhuma
comparação econômica entre as rotas que passam (`...classification.md:110`
— Missing com NOT_FOUND em todo `docs/canonical/`; os dois "ladders" do repo
são outros padrões: degradation ladder ordena FALHA de runtime, maturity
ladder é modelo organizacional).

E a tese do repo inteiro está em jogo: no caso do fonte, o degrau de
**decomposição** passou tudo no MENOR custo (`...patterns.md:126`) —
harness vence modelo exatamente onde upsize parecia o caminho curto
(`...classification.md:116`). É o argumento central do mental model do
fonte: garantias migram do prompt para o harness; capacidade migra do
modelo para a arquitetura.

**Sua missão:** implementar a `CapabilityEscalationLadder` — os quatro
degraus (`CAPABILITY`, `REASONING_BUDGET`, `INSTRUCTION`, `ARCHITECTURE`)
na ordem canônica, cada degrau com sua `RouteConfig` e sua `RouteResult`
medida (pass/fail por caso, violation count, tokens, latência); a subida
que para no primeiro degrau que passa MAS continua medindo os demais para a
comparação econômica; o `economic_winner()` que escolhe entre as rotas
aprovadas por custo com latência como tiebreaker; a flag
`passes_evals_fails_economics` para rotas como o tier-3 do prólogo; e o
sinal direcional — violation counts caindo com pass/fail parado — como
progresso visível ao longo da escada.

---

## 🧠 O Contexto

### O Modelo Mental: Ordem Fixa, Medida por Degrau, Decisão Econômica

O padrão tem três propriedades que o exercício codifica
(`...patterns.md:121-130`):

```
   TASK REPROVANDO no eval (tier-1: 0/5, 9 violações)
        │
        ▼
   ┌─────────────────────────────────────────────────────────────┐
   │  ESCADA — sobe na ordem, mede CADA degrau (pass + violações  │
   │  + tokens + latência)                                        │
   │                                                              │
   │  degrau 1  CAPABILITY      modelo maior        barato p/     │
   │  degrau 2  REASONING       adaptive thinking   testar,       │
   │            BUDGET                               caro p/      │
   │  degrau 3  INSTRUCTION     prompt melhor       manter        │
   │  degrau 4  ARCHITECTURE    3 prompts simples                │
   │                                                              │
   │  primeiro degrau que passa: para a SUBIDA                    │
   │  mas as rotas aprovadas seguem para a COMPARAÇÃO             │
   └──────────────────────┬───────────────────────────────────────┘
                          ▼
   ┌─────────────────────────────────────────────────────────────┐
   │  DECISÃO ECONÔMICA entre as aprovadas                        │
   │                                                              │
   │  tier-3:      5/5   3,1x tokens   9,0s  → passa evals,       │
   │                                               FALHA economics│
   │  decomposição: 5/5  1,2x tokens   6,5s → VENCEDORA           │
   │                                                              │
   │  violações ao longo do caminho: 9 → 7 → 6 → 0                │
   │  (sinal direcional: patterns.md:124)                         │
   └─────────────────────────────────────────────────────────────┘
```

1. **A ordem não é prestígio, é custo de teste.** "Each rung is cheap to
   test relative to the next" (`...patterns.md:124`) — capability e budget
   são mudanças de configuração; instruction é reescrita de prompt;
   architecture é engenharia. A escada testa o barato primeiro SEM prender a
   decisão ao primeiro que passa: "Early rungs can pass evals at
   unacceptable cost; pass/fail alone does not decide" (`...patterns.md:129`).
   É a diferença deste padrão para o eval-gate de migração (que compara
   candidatos a MODELO entre si — `docs/canonical/model-switching-architecture-enterprise-eval-gate.md:61-71`)
   e para o tiering (que roteia SUBTASKS que funcionam —
   `docs/canonical/task-routed-model-tiering.md:32`): aqui a task está
   REPROVANDO e as alavancas são de naturezas diferentes.

2. **Violation count é o sinal direcional.** Pass/fail é degrau binário; a
   contagem de violações por rota mostra se a capacidade está MELHORANDO
   mesmo com o binário parado — 0/5 → 2/5 com 9 → 6 violações é progresso
   real (`...patterns.md:124`). Sem esse registro, degraus intermediários
   parecem fracasso total e o time pula direto pro upsize.

3. **O vencedor é econômico.** "A cost/quality comparison across the routes
   that pass; the economic winner is typically the last rung"
   (`...patterns.md:122`). No fonte e no fixture, a decomposição — três
   prompts simples em vez de um modelo triplicado — passa tudo com o menor
   custo. O preço: "three prompts to maintain instead of one"
   (`...patterns.md:128`), o custo de manutenção que o lifecycle de harness
   evolution do repo já governa (`docs/canonical/measured-harness-evolution-lifecycle.md`).

### O Que Você Vai Construir

1. `Rung` / `RouteConfig` — os quatro degraus na ordem canônica, cada um com
   sua configuração (modelo, thinking budget, variante de instrução,
   decomposição em subagentes)
2. `RouteResult` — a medida por rota: casos aprovados, total, violation
   count, tokens por caso, latência por caso, `passed` (todos os casos)
3. `CapabilityEscalationLadder.run()` — sobe na ordem, para no primeiro
   `passed`, mas mede TODAS as rotas (as aprovadas para a comparação; as
   reprovadas como evidência do sinal direcional)
4. `economic_winner()` — entre as aprovadas: menor custo por caso, latência
   como tiebreaker; rota aprovada acima do budget leva
   `passes_evals_fails_economics`
5. `run_escalation()` — o pipeline do prólogo: a task enterprise reprovando,
   as 4 rotas medidas, o tier-3 reprovado na economia, a decomposição
   vencedora, e a trilha de violações 9 → 7 → 6 → 0 ao longo da escada

---

## 📋 Cenário

A task `consolidated-multi-item-recommendation` do KODA: dado um carrinho
com 4 itens e restrições cruzadas (compatibilidade, orçamento, prazo de
entrega), produzir UMA recomendação consolidada que satisfaz 4 constraints
duras. O eval tem 5 casos; cada caso reprova com qualquer violação.

Rotas medidas (dados do fixture, determinísticos):

| Rota | Modelo | Config | Casos | Violações | Tokens/caso | Latência/caso |
|---|---|---|---|---|---|---|
| baseline (tier-1) | gen-3 tier-1 | atual | 0/5 | 9 | 4.000 | 5,0s |
| degrau 1 CAPABILITY | tier-3 | upsize | 5/5 | 0 | 12.400 | 9,0s |
| degrau 2 BUDGET | tier-1 | thinking alto | 3/5 | 7 | 6.100 | 7,5s |
| degrau 3 INSTRUCTION | tier-1 | prompt v2 | 2/5 | 6 | 4.400 | 5,4s |
| degrau 4 ARCHITECTURE | 3 subagentes tier-1 | gen/eval/repair | 5/5 | 0 | 4.800 | 6,5s |

Budget econômico do produto: 8.000 tokens e 8,0s por caso (o contrato
enterprise). O degrau 1 passa o eval e estoura os dois; o degrau 4 passa o
eval dentro dos dois.

---

## ✅ Requisitos

### Requisitos Funcionais

1. **RF1 — Quatro degraus, ordem canônica:** `Rung` enumera CAPABILITY,
   REASONING_BUDGET, INSTRUCTION, ARCHITECTURE nessa ordem; a escada recusa
   `RouteConfig` de rung duplicado e expõe a ordem como dado consultável
   (`patterns.md:118`).
2. **RF2 — Medida completa por rota:** cada `RouteResult` carrega casos
   aprovados/total, violation count somado, tokens e latência por caso;
   `passed` só é True com TODOS os casos aprovados — sem média, sem parcial.
3. **RF3 — Subida que para, comparação que continua:** `run()` sobe na ordem
   e interrompe a SUBIDA no primeiro `passed`, mas o relatório final contém
   TODAS as rotas medidas (aprovadas para a decisão, reprovadas como trilha
   de evidência) — parar cedo não pode esconder rotas mais baratas.
4. **RF4 — Sinal direcional:** o relatório expõe a trilha de violation
   counts na ordem da escada (9 → 7 → 6 → 0 no fixture) — rota reprovada com
   menos violações que a anterior registra progresso de capacidade, não
   fracasso repetido (`patterns.md:124`).
5. **RF5 — Decisão econômica:** `economic_winner()` escolhe entre as rotas
   aprovadas por menor custo (tokens/caso), com latência como tiebreaker;
   rota aprovada fora do budget recebe `passes_evals_fails_economics: True`
   e NÃO pode vencer (`patterns.md:125`).
6. **RF6 — O pipeline do prólogo:** `run_escalation()` reproduz o cenário: o
   tier-3 aprovado e economicamente reprovado, a decomposição vencedora
   (4.800 tokens, 6,5s), baseline 0/5 com 9 violações, e a trilha de
   violações decrescendo ao longo da escada.

### Requisitos Técnicos

1. **RT1 — Python 3.9+, stdlib apenas**, type hints obrigatórios
2. **RT2 — `dataclasses` + enums**; rotas e resultados congelados; a escada
   recebe medições PRONTAS por rota (o fixture é determinístico — sem
   chamadas de modelo, sem I/O)
3. **RT3 — Funções puras de decisão:** `(rotas medidas, budget) → (vencedora
   | veredito econômico)`; a decisão nunca muta os resultados
4. **RT4 — Decisão rastreável:** o vencedor carrega uma rationale de uma
   linha citando as rotas aprovadas comparadas e os números que decidiram

---

## 🏗️ Arquitetura do Sistema

```
┌────────────────────────────────────────────────────────────────────────┐
│                 CAPABILITY ESCALATION LADDER                            │
│                                                                        │
│  ROUTE CONFIGS (RF1)                 ROUTE RESULTS (RF2)                │
│  CAPABILITY      → tier-3            baseline: 0/5, viol=9, 4.0k tok   │
│  REASONING_BUDGET→ thinking alto     degrau1:  5/5, viol=0, 12.4k tok  │
│  INSTRUCTION     → prompt v2         degrau2:  3/5, viol=7, 6.1k tok   │
│  ARCHITECTURE    → gen/eval/repair   degrau3:  2/5, viol=6, 4.4k tok   │
│        │                             degrau4:  5/5, viol=0, 4.8k tok   │
│        ▼                                      ▲                         │
│  ┌────────────────────────────────────────┐   │                         │
│  │ LADDER.run() (RF3)                     │   │ todas as rotas         │
│  │ sobe na ordem; SUBIDA para no 1º passed│───┘ medidas               │
│  └────────────────────┬───────────────────┘                             │
│                       ▼                                                 │
│  ┌────────────────────────────────────────────────────────────┐        │
│  │ DECISÃO ECONÔMICA (RF5)                                    │        │
│  │ aprovadas: tier-3 (12.4k, 9.0s) ✗budget | decomposição     │        │
│  │ (4.8k, 6.5s) ✓budget → VENCEDORA: decomposição             │        │
│  │ tier-3 → passes_evals_fails_economics                      │        │
│  │ trilha de violações (RF4): 9 → 7 → 6 → 0                   │        │
│  └────────────────────────────────────────────────────────────┘        │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 🎯 Sua Tarefa em 3 Partes

### Parte 1 — Diagnosticar o war room (15 min)

Com o prólogo: classifique as três propostas (ENG_A, B, C) em rungs da
escada. Por que "passou o eval e reprovou a economia" foi detectado só DEPOIS
do upsize? O que o sinal 0/5→2/5 com 9→6 violações teria mudado na decisão?
Responda como comentário, citando `patterns.md`.

### Parte 2 — Degraus, rotas e a subida (40 min)

Implemente `Rung`/`RouteConfig` com a ordem canônica (RF1), `RouteResult`
com a medida completa (RF2) e `CapabilityEscalationLadder.run()` com a
subida que para e a comparação que continua (RF3-RF4).

### Parte 3 — Decisão econômica e o pipeline (35 min)

Implemente `economic_winner()` com o veto de budget (RF5) e
`run_escalation()` reproduzindo o cenário completo do prólogo (RF6): o
tier-3 reprovado na economia, a decomposição vencedora, a trilha de
violações decrescente.

---

## 💻 Starter Code

```python
"""
Exercício 22 — Capability Escalation Ladder
Nível 3 — Arquitetura Avançada

Quando uma task reprova: capability, budget, instruction, architecture —
nessa ordem, cada degrau medido, e o vencedor é econômico entre as rotas
que passam. Pass/fail sozinho não decide.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


# ============================================================================
# DATA MODELS — os degraus e as rotas
# ============================================================================

class Rung(Enum):
    """
    Os quatro degraus na ordem canônica (patterns.md:118): capability,
    depois budget, depois instruction, depois architecture. A ordem é de
    CUSTO DE TESTE — cada degrau é barato de testar relativo ao próximo
    (patterns.md:124).
    """
    CAPABILITY = "capability"            # modelo maior
    REASONING_BUDGET = "reasoning_budget"  # adaptive thinking
    INSTRUCTION = "instruction"          # prompt melhor
    ARCHITECTURE = "architecture"        # decomposição em agentes simples


@dataclass(frozen=True)
class RouteConfig:
    """A configuração de UMA rota por degrau (RF1)."""
    rung: Rung
    label: str                    # ex.: "tier-3-upsize"
    model: str                    # ex.: "gen-3-tier-1"
    thinking_budget: str = "default"
    instruction_variant: str = "v1"
    decomposition: tuple[str, ...] = ()   # subagentes, ex.: ("generator", "evaluator", "repairer")


class DuplicateRungError(Exception):
    """A escada mede UM degrau por vez (RF1)."""


@dataclass(frozen=True)
class RouteResult:
    """
    A medida completa por rota (RF2): pass/fail por caso (binário, sem
    média), violation count somado, tokens e latência POR CASO.
    """
    config: RouteConfig
    cases_passed: int
    cases_total: int
    violation_count: int
    tokens_per_case: int
    latency_per_case_s: float

    @property
    def passed(self) -> bool:
        """True só com TODOS os casos aprovados (RF2)."""
        # TODO: implemente
        raise NotImplementedError


@dataclass(frozen=True)
class Budget:
    """O contrato econômico do produto (RF5)."""
    max_tokens_per_case: int
    max_latency_per_case_s: float

    def within(self, result: RouteResult) -> bool:
        # TODO: implemente
        raise NotImplementedError


# ============================================================================
# A ESCADA
# ============================================================================

@dataclass(frozen=True)
class LadderReport:
    """O relatório da subida (RF3, RF4)."""
    results: tuple[RouteResult, ...]     # TODAS as rotas medidas, na ordem
    first_passing: RouteResult | None    # onde a SUBIDA parou
    climb_stopped_early: bool = False

    @property
    def passing_routes(self) -> list[RouteResult]:
        # TODO: implemente
        raise NotImplementedError

    @property
    def violation_trail(self) -> list[int]:
        """
        A trilha de violation counts na ordem da escada (RF4) — inclui o
        baseline se registrado. Ex. do fixture: [9, 0, 7, 6, 0].
        """
        # TODO: implemente
        raise NotImplementedError

    def directional_progress(self) -> bool:
        """
        True se alguma rota REPROVADA tem menos violações que a anterior —
        capacidade melhorando com pass/fail parado (patterns.md:124).
        """
        # TODO: implemente
        raise NotImplementedError


class CapabilityEscalationLadder:
    """
    A escada (RF3): sobe na ordem canônica, interrompe a SUBIDA no
    primeiro passed, mas o relatório carrega TODAS as rotas medidas —
    parar cedo não pode esconder rotas mais baratas.
    """

    def __init__(self, routes: list[RouteConfig],
                 measurements: dict[str, RouteResult]) -> None:
        """
        routes: na ordem da escada; measurements: label → resultado.
        Recusa rung duplicado (DuplicateRungError, RF1).
        """
        # TODO: implemente (valide duplicatas e guarde a ordem)
        raise NotImplementedError

    def run(self, baseline: RouteResult | None = None) -> LadderReport:
        """
        Percorre os rungs EM ORDEM consumindo as medições:
          - resultado passed → REGISTRA e interrompe a SUBIDA
            (climb_stopped_early=True se há rungs não testados)
          - resultado reprovado → REGISTRA e continua
        Todas as rotas registradas entram no relatório final (RF3).
        """
        # TODO: implemente
        raise NotImplementedError


# ============================================================================
# A DECISÃO ECONÔMICA
# ============================================================================

@dataclass(frozen=True)
class EconomicVerdict:
    """O veredito econômico (RF5, RT4)."""
    winner: RouteResult | None
    rationale: str                                  # uma linha citável
    fails_economics: list[RouteResult] = field(default_factory=list)


def economic_winner(report: LadderReport, budget: Budget) -> EconomicVerdict:
    """
    Entre as rotas APROVADAS (RF5):
      1. fora do budget → fails_economics (passes evals, fails economics,
         patterns.md:125) — NÃO pode vencer
      2. dentro do budget → menor tokens_per_case vence;
         desempate por latency_per_case_s
      3. nenhuma aprovada dentro do budget → winner None, rationale
         dizendo que a escada não resolveu economicamente
    A rationale cita as rotas comparadas e os números (RT4).
    """
    # TODO: implemente
    raise NotImplementedError


# ============================================================================
# PARTE 3 — O PIPELINE DO PRÓLOGO
# ============================================================================

@dataclass
class EscalationOutcome:
    winner_label: str | None = None
    tier3_fails_economics: bool = False
    violation_trail: list[int] = field(default_factory=list)
    directional_progress_seen: bool = False
    baseline_passed: bool = False


def run_escalation() -> EscalationOutcome:
    """
    O pipeline do prólogo (RF6): baseline 0/5 (9 violações); degrau 1
    tier-3 5/5 mas 12.400 tokens e 9,0s (fora do budget de 8.000/8,0);
    degraus 2-3 reprovados com violações caindo (7, 6); degrau 4
    decomposição 5/5 com 4.800 tokens e 6,5s — vencedora. Trilha
    completa: [9, 0, 7, 6, 0]; progresso direcional visível nos degraus
    2-3.
    """
    # TODO: implemente
    raise NotImplementedError


# ============================================================================
# FIXTURES — as medições do war room (determinísticas)
# ============================================================================

ENTERPRISE_BUDGET = Budget(max_tokens_per_case=8000, max_latency_per_case_s=8.0)


def war_room_routes() -> list[RouteConfig]:
    return [
        RouteConfig(Rung.CAPABILITY, "tier-3-upsize", "gen-3-tier-3"),
        RouteConfig(Rung.REASONING_BUDGET, "tier-1-thinking-high",
                    "gen-3-tier-1", thinking_budget="high"),
        RouteConfig(Rung.INSTRUCTION, "tier-1-prompt-v2",
                    "gen-3-tier-1", instruction_variant="v2"),
        RouteConfig(Rung.ARCHITECTURE, "gen-eval-repair-decomposition",
                    "gen-3-tier-1",
                    decomposition=("generator", "evaluator", "repairer")),
    ]


def war_room_measurements() -> dict[str, RouteResult]:
    """As medições da tabela do cenário."""
    routes = {r.label: r for r in war_room_routes()}
    return {
        "baseline-tier-1": RouteResult(
            RouteConfig(Rung.INSTRUCTION, "baseline-tier-1", "gen-3-tier-1"),
            cases_passed=0, cases_total=5, violation_count=9,
            tokens_per_case=4000, latency_per_case_s=5.0),
        "tier-3-upsize": RouteResult(
            routes["tier-3-upsize"],
            cases_passed=5, cases_total=5, violation_count=0,
            tokens_per_case=12400, latency_per_case_s=9.0),
        "tier-1-thinking-high": RouteResult(
            routes["tier-1-thinking-high"],
            cases_passed=3, cases_total=5, violation_count=7,
            tokens_per_case=6100, latency_per_case_s=7.5),
        "tier-1-prompt-v2": RouteResult(
            routes["tier-1-prompt-v2"],
            cases_passed=2, cases_total=5, violation_count=6,
            tokens_per_case=4400, latency_per_case_s=5.4),
        "gen-eval-repair-decomposition": RouteResult(
            routes["gen-eval-repair-decomposition"],
            cases_passed=5, cases_total=5, violation_count=0,
            tokens_per_case=4800, latency_per_case_s=6.5),
    }


# ============================================================================
# TESTS
# ============================================================================

def test_rung_order_canonical():
    order = [r.name for r in Rung]
    assert order == ["CAPABILITY", "REASONING_BUDGET", "INSTRUCTION",
                     "ARCHITECTURE"], "ordem canônica (RF1)"
    print("TESTE 1 PASSOU")


def test_duplicate_rung_refused():
    routes = war_room_routes()
    dup = routes + [RouteConfig(Rung.CAPABILITY, "another-upsize",
                                "gen-3-tier-3x")]
    try:
        CapabilityEscalationLadder(dup, war_room_measurements())
        raise AssertionError("rung duplicado deve recusar (RF1)")
    except DuplicateRungError:
        pass
    print("TESTE 2 PASSOU")


def test_climb_stops_but_report_is_complete():
    ladder = CapabilityEscalationLadder(
        war_room_routes(), war_room_measurements())
    report = ladder.run(baseline=war_room_measurements()["baseline-tier-1"])

    # a subida para no degrau 1 (tier-3, 5/5)
    assert report.first_passing is not None
    assert report.first_passing.config.rung == Rung.CAPABILITY
    assert report.climb_stopped_early, "degraus 2-4 não foram 'necessários' (RF3)"
    # mas o relatório carrega TODAS as rotas medidas
    assert len(report.results) == 4, "comparação completa (RF3)"
    assert len(report.passing_routes) == 2, "tier-3 e decomposição aprovadas"
    print("TESTE 3 PASSOU")


def test_directional_signal_in_the_trail():
    ladder = CapabilityEscalationLadder(
        war_room_routes(), war_room_measurements())
    report = ladder.run(baseline=war_room_measurements()["baseline-tier-1"])

    assert report.violation_trail == [9, 0, 7, 6, 0], "trilha do cenário (RF4)"
    assert report.directional_progress(), (
        "degraus 2-3 reprovados com violações caindo = progresso (RF4)")
    print("TESTE 4 PASSOU")


def test_economics_veto_and_winner():
    ladder = CapabilityEscalationLadder(
        war_room_routes(), war_room_measurements())
    report = ladder.run()
    verdict = economic_winner(report, ENTERPRISE_BUDGET)

    tier3 = next(r for r in report.passing_routes
                 if r.config.rung == Rung.CAPABILITY)
    assert tier3 in verdict.fails_economics, (
        "tier-3: passes evals, fails economics (RF5)")
    assert verdict.winner is not None
    assert verdict.winner.config.rung == Rung.ARCHITECTURE, (
        "a decomposição é a vencedora econômica (RF5)")
    assert "4800" in verdict.rationale or "12.400" in verdict.rationale or \
        "12400" in verdict.rationale, "rationale cita os números (RT4)"
    print("TESTE 5 PASSOU")


def test_pipeline_reproduces_the_war_room():
    outcome = run_escalation()
    assert outcome.winner_label == "gen-eval-repair-decomposition"
    assert outcome.tier3_fails_economics
    assert outcome.violation_trail == [9, 0, 7, 6, 0]
    assert outcome.directional_progress_seen
    assert not outcome.baseline_passed
    print("TESTE 6 PASSOU")


if __name__ == "__main__":
    print("=" * 60)
    print("EXERCÍCIO 22: CAPABILITY ESCALATION LADDER")
    print("=" * 60)
    # Descomente após implementar:
    # test_rung_order_canonical()
    # test_duplicate_rung_refused()
    # test_climb_stops_but_report_is_complete()
    # test_directional_signal_in_the_trail()
    # test_economics_veto_and_winner()
    # test_pipeline_reproduces_the_war_room()
    print("\nTODO: implemente RouteResult.passed, LadderReport,")
    print("CapabilityEscalationLadder.run, economic_winner e")
    print("run_escalation")
```

---

## ✅ Validação: Critérios de Aceitação

Seu código será considerado **APROVADO** quando:

- [ ] `Rung` na ordem canônica (capability → budget → instruction → architecture) e rung duplicado recusado (RF1)
- [ ] `RouteResult.passed` exige TODOS os casos; a medida carrega violações, tokens e latência por caso (RF2)
- [ ] A subida para no primeiro aprovado (tier-3, degrau 1) com `climb_stopped_early=True`, mas o relatório carrega as 4 rotas e as 2 aprovadas (RF3)
- [ ] `violation_trail == [9, 0, 7, 6, 0]` e `directional_progress()` é True nos degraus reprovados com violações caindo (RF4)
- [ ] O tier-3 aprovado cai em `fails_economics` (fora do budget 8.000/8,0) e a decomposição vence com rationale citando os números (RF5, RT4)
- [ ] `run_escalation()` fecha o prólogo: vencedora `gen-eval-repair-decomposition`, trilha completa, baseline reprovado (RF6)

---

## 📊 Rubric de Avaliação

| Critério | Peso | Insuficiente (0-3) | Básico (4-6) | Proficiente (7-8) | Excelente (9-10) |
|---|---|---|---|---|---|
| **Degraus e ordem (Parte 2)** | 15% | Não implementados | Rungs sem ordem | Ordem canônica + duplicata recusada | Ordem justificada por custo de teste no design |
| **Medida e subida (Parte 2)** | 30% | Não implementadas | Mede só pass/fail | Medida completa (4 eixos) + subida que para + relatório completo | Separação explícita SUBIDA (para) vs COMPARAÇÃO (continua) |
| **Sinal direcional (Parte 2)** | 15% | Ausente | Trilha sem leitura | Trilha + directional_progress corretos | Interpreta degraus reprovados como progresso de capacidade |
| **Decisão econômica (Parte 3)** | 25% | Não implementada | Vence o primeiro que passa | Veto de budget + custo com tiebreaker de latência | Rationale citável com os números das rotas comparadas |
| **Pipeline (Parte 3)** | 15% | Não roda | Números parciais | Reproduz o prólogo completo (vencedora, veto, trilha) | Outcome lê como a ata que o war room deveria ter tido |

**Nota final:** Média ponderada. **Aprovação:** >= 7.0

---

## 💡 Dicas para Implementação

1. **"Parar a subida" não é "parar de medir".** O erro clássico deste padrão é retornar no primeiro `passed` — aí o tier-3 vence por ordem e a decomposição mais barata nunca aparece. No fixture as medições JÁ EXISTEM (determinísticas): `run()` registra tudo, interrompe apenas a exploração futura. Se seu `LadderReport` tem menos rotas que a escada, releia o RF3.
2. **O budget é veto, não peso.** Rota fora do budget não "perde pontos" — ela é inelegível, vai para `fails_economics`, e a decisão corre entre as elegíveis. Peso permitiria um monstro de 12.400 tokens vencer por passar 5/5 "com desconto". "Pass/fail alone does not decide" — economics é outra porta, não outro peso (`...patterns.md:129`).
3. **A trilha de violações inclui o baseline.** `[9, 0, 7, 6, 0]` — o 9 do baseline é o que dá sentido à queda dos degraus 2-3. E note o aparente paradoxo: o degrau 1 tem 0 violações e 5/5, os degraus 2-3 "pioram" para 7 e 6 — a trilha lê por POSIÇÃO na escada, e o progresso direcional compara degraus REPROVADOS consecutivos (7 < 9 do baseline, 6 < 7). Não é sequência monotônica global; é capacidade emergindo com o binário travado.

---

## ❓ Dúvidas Comuns

**P: Por que capability vem primeiro se architecture costuma vencer?**
R: Pelo custo de TESTE, não pelo custo de manter. "Each rung is cheap to test relative to the next" (`...patterns.md:124`): trocar modelo é uma config; decompor é engenharia de dias. A escada testa o barato primeiro para só pagar engenharia quando o barato não resolve — ou resolve caro demais. O vencedor típico sendo o último degrau (`...patterns.md:122`) é o RESULTADO medido, não a aposta.

**P: Isso não é o tested-degradation-ladder do repo?**
R: Não — é o vizinho mais confundido. O degradation ladder ordena MANEJO DE FALHA em runtime (classificar, retry, fallback seguro, humano — `docs/canonical/tested-degradation-ladder.md:29`); esta escada ordena INVESTIMENTO DE CAPACIDADE numa task que reprova o eval, comparando custos entre rotas que PASSAM (`...classification.md:114` rejeita a equivalência explicitamente). Um é plano de contingência; o outro é procedimento de escalada.

**P: E o model-switching eval-gate — mesma coisa?**
R: Complemento em outro eixo. O gate compara MODELOS candidatos entre si com a suite como regression test (`docs/canonical/model-switching-architecture-enterprise-eval-gate.md:61-71`); a escada compara ALAVANCAS de natureza diferente (modelo, budget, prompt, arquitetura) para UMA task reprovando. O gate decide migração de frota; a escada decide resgate de task.

**P: Quando a decomposição vence, o que o repo ganha?**
R: A tese central: o caso do fonte — decomposição passa tudo no menor custo (`...patterns.md:126`) — é exatamente o harness-over-model que o mental model do fonte enuncia (`2026-09-02-the-prompting-playbook-mental-model.md:23`). O preço é "three prompts to maintain instead of one" (`...patterns.md:128`), e é aí que entra o lifecycle: o harness evoluído passa a ser medido e mantido como ativo (`docs/canonical/measured-harness-evolution-lifecycle.md`).

**P: Budget de 8.000 tokens não é arbitrário demais?**
R: É o CONTRATO, e contratos são arbitrários por natureza — o cliente enterprise pagou por 8.000/8,0. O padrão não discute o número; exige que o número EXISTA e que a decisão o respeite. Sem budget declarado, toda rota que passa vence e o upsize vence sempre — que é como o war room do prólogo quase acabou com uma fatura 3,1x.

---

## 🚀 Próximo Passo

Depois de completar este exercício:

1. Leia o padrão 6 completo e sua classificação: `docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-patterns.md:112-130` e `...classification.md:106-116` — Missing/High: as alavancas existiam isoladas; o protocolo ordenado com economia é o que falta
2. Siga a série: [[curriculum/02-nivel-2-practical-patterns/exercises/exercise-08-defensive-patch-ledger|Exercício 8]] audita o que o prompt carrega → [[curriculum/02-nivel-2-practical-patterns/exercises/exercise-09-two-sided-trade-off-instruction|Exercício 9]] balanceia o que a instrução declara → este exercício escala a capacidade quando prompt não é o gabarito → [[curriculum/03-nivel-3-advanced-architecture/exercises/exercise-21-agent-kernel-runtime|Exercício 21]] roda a arquitetura vencedora num kernel com fronteiras tipadas
3. Aplique ao KODA real: escolha UMA task que reprova hoje e escreva a ata que falta — as 4 rotas, os 4 eixos de medida por rota, o budget, e o vencedor econômico. Se sua equipe não tem o número do budget, esse é o primeiro achado.

---

*Exercício 22 | Nível 3 — Arquitetura Avançada | Capability Escalation Ladder*

**Pass/fail diz se passa; a economia diz se fica — suba a escada medindo cada degrau.**
