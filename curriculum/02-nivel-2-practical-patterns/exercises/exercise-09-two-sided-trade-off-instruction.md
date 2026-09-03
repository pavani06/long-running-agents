---
title: "Exercício 9: Two-Sided Trade-off Instruction — Dizer os Dois Lados do Custo, Não Só o Barato"
type: exercise
level: "N2"
aliases: ["two-sided trade-off instruction", "instrução de trade-off de dois lados", "counter-cost", "single-objective overfit", "under-escalation", "cost of not escalating"]
tags: ["curriculo-conteudo", "nivel-2", "agentes-orquestracao", "context-engineering", "evals", "production"]
relates-to: ["[[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-patterns|Padrões The Prompting Playbook]]", "[[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-classification|Classificação The Prompting Playbook]]", "[[docs/canonical/closed-loop-help-api|Closed-Loop Help API]]", "[[docs/canonical/human-afk-task-routing-gate|Human-AFK Task Routing Gate]]", "[[docs/canonical/tested-degradation-ladder|Tested Degradation Ladder]]", "[[curriculum/02-nivel-2-practical-patterns/exercises/exercise-08-defensive-patch-ledger|Exercício 8: Defensive Patch Ledger]]", "[[curriculum/03-nivel-3-advanced-architecture/exercises/exercise-22-capability-escalation-ladder|Exercício 22: Capability Escalation Ladder]]"]
duration: "60-90 min"
last_updated: 2026-09-02
---

# ⚖️ Exercício 9: Two-Sided Trade-off Instruction — Dizer os Dois Lados do Custo, Não Só o Barato
## Nível 2 — Padrões Práticos

**Tempo Estimado:** 60-90 minutos
**Dificuldade:** (Intermediário)
**Pré-requisito:** Ter lido `03-rubric-design.md` (Nível 2) + `docs/canonical/closed-loop-help-api.md` + ter feito o [[curriculum/02-nivel-2-practical-patterns/exercises/exercise-08-defensive-patch-ledger|Exercício 8: Defensive Patch Ledger]]
**Objetivo:** Escrever instruções de ação custosa (escalonar, reembolsar, handoff) declarando OS DOIS LADOS do trade-off — o custo de agir E o counter-cost de evitar errado — para eliminar o single-objective overfit, e manter a instrução alinhada com o que o eval define como correto

---

## 📖 Prólogo: O Agente Que Aprendeu Demais a Não Escalonar

### Quarta-feira, 14h20. Review semanal de ops do agente de suporte do KODA.

```
OPS_LEAD:   "gente, o escalonamento pra humano caiu pra quase
             zero. 0,4% dos tickets. A meta de custo que a
             gente escreveu no prompt era 'reduzir escalonamentos
             caros' — mission accomplished?"

ANALYST:    "só que olhem os tickets que VIRARAM incidente essa
             semana: 11 casos de fraude/chargeback que o agente
             tentou resolver sozinho. Cada chargeback custa
             R$ 480 em média. O escalonamento custa R$ 8 em
             tempo de humano. Ele economizou 8 pra perder 480.
             Onze vezes."

PROMPT_OWN: "o prompt diz: 'Escalonar custa R$ 8 por ticket —
             evite escalonar a menos que seja absolutamente
             necessário'. A gente escreveu SÓ o lado caro."

ANALYST:    "e 'a menos que seja absolutamente necessário' pra
             um modelo otimizador é o mesmo que 'quase nunca'.
             Ele passou a tratar cada escalonamento como derrota.
             É overfit num objetivo único."

OPS_LEAD:   "e o pior: nosso eval de calibração define que os
             casos de fraude DEVEM escalar. O prompt e o eval
             puxam pra direções opostas. O que o modelo deve
             aprender?"

PROMPT_OWN: "que fraude é raro. A instrução só fala de custo;
             o eval só fala de quando escalar. Se a instrução
             declarasse os dois lados — o custo de escalonar E
             o counter-cost de NÃO escalonar um caso de fraude —
             o julgamento por caso voltava a ser do modelo."
```

**O custo da instrução de um lado só:**

```
╔══════════════════════════════════════════════════════════════════╗
║   R$ 8 CONTRA R$ 480 — A ARITMÉTICA QUE O PROMPT ESCONDEU          ║
║                                                                  ║
║  Instrução vigente (um lado só):                                 ║
║   "Escalonar custa R$ 8 por ticket — evite escalonar a menos      ║
║    que seja absolutamente necessário"                            ║
║                                                                  ║
║  O que o modelo ouviu:      "escalonamento = derrota"             ║
║  Taxa de escalonamento:     6,2% → 0,4%                          ║
║                                                                  ║
║  Semana seguinte:                                                ║
║   11 fraudes não escalonadas × R$ 480 (chargeback)   = R$ 5.280  ║
║   economia de escalonamento (68 × R$ 8)              = R$   544  ║
║   ────────────────────────────────────────────────────────────   ║
║   prejuízo líquido da otimização                    = R$ 4.736  ║
║                                                                  ║
║  Eval de calibração (fraude → escalona): 0/11 — e o eval é       ║
║  VERDE no resto, então ninguém olhava                            ║
║                                                                  ║
║  O reframe: modelos melhoram em julgar trade-offs — a instrução  ║
║  deve declarar os DOIS lados e deixar o julgamento por caso      ║
║  (patterns.md:104)                                               ║
╚══════════════════════════════════════════════════════════════════╝
```

**O problema não é dar custo.** Dar o custo é correto — número no prompt é
melhor que vago. O problema é dar **um** lado: "escalation costs $8" sem o
counter-cost de evitar errado faz o modelo over-otimizar o único objetivo
enunciado e nunca escalonar, mesmo quando escalonar é o correto
(`...patterns.md:95`). O repo do curso é exatamente cego aqui: a cobertura de
escalonamento é **arquitetural** (degradation ladder como rung de falha,
closed-loop help API, routing gate) e **nunca instrucional** — nenhum doc
ensina a desenhar a economia da instrução de ação custosa
(`...classification.md:95,100` — Missing com NOT_FOUND em todo `docs/canonical/`).

**Sua missão:** implementar o `TradeOffInstruction` — a instrução balanceada
com `cost_side` e `counter_cost_side` quantificados e um `judgment_rule`
explícito; o `InstructionLinter` que caça instruções de um lado só (custo sem
counter-cost, ou o inverso) e as reescreve em dois lados; e o simulador de
política que roda o lote de tickets do prólogo sob a política one-sided
(escalonamento colapsa para ~0, prejuízo líquido de R$ 4.736) contra a
two-sided (julgamento por caso: fraude escala, dúvida de plano não), com o
alinhamento prompt-vs-eval verificado no final.

---

## 🧠 O Contexto

### O Modelo Mental: A Instrução Como Economia Declarada, o Julgamento Como Decisão por Caso

O padrão é um princípio de design de instrução com três engrenagens
(`...patterns.md:96-106`):

```
   INSTRUÇÃO DE UM LADO SÓ                 INSTRUÇÃO DE DOIS LADOS
   ┌──────────────────────────┐            ┌──────────────────────────────┐
   │ "Escalonar custa R$ 8.   │            │ "Escalonar custa R$ 8 de     │
   │  Evite."                 │            │  tempo de humano. NÃO esca-  │
   │                          │            │  lonar um caso de fraude     │
   │  modelo ouve:            │            │  expõe chargeback de R$ 480  │
   │  "minimize escalonamento"│            │  e dano de confiança. Julgue │
   │                          │            │  por caso qual lado domina." │
   └───────────┬──────────────┘            └───────────────┬──────────────┘
               ▼                                           ▼
   política implícita:                      política declarada:
   escalate_rate → ~0%                      decide por caso, comparando
   (single-objective overfit)               R$ 8 contra o risco do caso
               │                                           │
               ▼                                           ▼
   eval de calibração: FAIL                eval de calibração: PASS
   (fraude nunca escala)                   (fraude escala, dúvida não)
   → prompt e eval divergem                → prompt e eval descrevem o
                                             MESMO comportamento correto
```

Três propriedades definem o padrão:

1. **Counter-cost é dado de primeira classe.** "The counter-cost of wrongly
   avoiding it (refund exposure, customer trust)" é input do padrão
   (`...patterns.md:99`) — quantificado quando possível, qualitativo quando
   não. Sem counter-cost, não há trade-off; há meta única disfarçada.

2. **O julgamento migra da regra para o caso.** "As models improve at making
   trade-offs, stating both sides lets them exercise that judgment"
   (`...patterns.md:104`). A instrução deixa de ser um gatilho ("se fraude,
   então") e passa a ser uma economia ("R$ 8 contra R$ 480 — você decide"). O
   trade-off explícito: "Converts a hard rule into a judgment; behavior
   becomes less deterministic" (`...patterns.md:109`) — determinismo menor é o
   preço, e o eval é a rede.

3. **A instrução e o eval têm que concordar.** "The framing must stay aligned
   with what the eval defines as correct" (`...patterns.md:110`). O incidente
   do prólogo é duplo: a instrução puxava para não-escalonar e o eval pedia
   escalonamento de fraude — "Resolves prompt-vs-eval conflict when both
   describe the desired behavior consistently" (`...patterns.md:106`).

Os vizinhos do repo, e por que não resolvem sozinhos: o
`tested-degradation-ladder` trata escalonamento como **rung de falha em
runtime** (`docs/canonical/tested-degradation-ladder.md:29`) — não como
economia de instrução; o `closed-loop-help-api` fecha o LOOP do escalonamento
terminal (`docs/canonical/closed-loop-help-api.md:30-32`) — não decide quando;
o `human-afk-task-routing-gate` roteia por **tipo de tarefa**
(`docs/canonical/human-afk-task-routing-gate.md:37`) — não por trade-off. O
padrão é a camada instrucional que falta por cima deles.

### O Que Você Vai Construir

1. `TradeOffInstruction` — a instrução balanceada: `action`, `cost_side`
   (unidade + valor), `counter_cost_side` (unidade + valor + quando domina),
   `judgment_rule` (o texto que vai pro prompt)
2. `OneSidedFinding` — o achado do linter: instrução que enuncia um lado só,
   com o lado faltante nomeado
3. `InstructionLinter` — varre o prompt procurando instruções de custo de
   ação; `lint()` acha o one-sided, `rewrite()` devolve o texto em dois lados
   com `judgment_rule`
4. `DecisionPolicy` — o simulador: `ONE_SIDED` (segue só o custo enunciado),
   `TWO_SIDED` (compara os dois lados por caso); `EscalationCase` com o
   counter-cost real de não escalar
5. `run_week()` — o lote do prólogo: 180 tickets sob as duas políticas, com
   custo líquido, taxa de escalonamento e `prompt_eval_alignment` por política

---

## 📋 Cenário

O lote da semana do agente de suporte do KODA, condensado em classes de caso
(o fixture gera as contagens):

| Classe de caso | Casos | Escalar é correto? | Custo de escalar | Counter-cost de NÃO escalar |
|---|---|---|---|---|
| fraude/chargeback suspeito | 11 | sim | R$ 8 | R$ 480 (chargeback) |
| dúvida de plano coberto | 68 | não | R$ 8 | R$ 0 (FAQ resolve) |
| churn de cliente top | 6 | sim | R$ 8 | R$ 600 (LTV em risco) |
| reset de senha | 95 | não | R$ 8 | R$ 0 (self-service) |

A política `ONE_SIDED` conhece só "escalonar custa R$ 8, evite" — ela
escalone apenas quando o caso explicitamente diz "MARCAÇÃO OBRIGATÓRIA" (0
casos no lote: o colapso do prólogo). A política `TWO_SIDED` compara, por
caso, R$ 8 contra o counter-cost declarado e escala quando o counter-cost
domina.

---

## ✅ Requisitos

### Requisitos Funcionais

1. **RF1 — Dois lados como estrutura:** `TradeOffInstruction` exige `cost_side`
   e `counter_cost_side` não vazios (unidade + valor) e um `judgment_rule`
   não vazio; construir com um lado faltante levanta
   `OneSidedInstructionError` nomeando o lado ausente.
2. **RF2 — O linter acha o one-sided:** `InstructionLinter.lint(prompt)`
   retorna um `OneSidedFinding` por instrução que enuncia custo de ação sem
   counter-cost (padrão: linha com custo/verbo de ação sem contra-custo na
   mesma instrução), com o lado faltante nomeado.
3. **RF3 — O rewrite é dois-lados:** `rewrite(finding, counter)` devolve texto
   que cita os dois valores e termina delegando o julgamento por caso — sem
   virar regra dura ("sempre/nunca escalone" são proibidos no output do
   rewrite).
4. **RF4 — Simulação das duas políticas:** `DecisionPolicy` decide por caso:
   `ONE_SIDED` escala só com marcação obrigatória; `TWO_SIDED` escala quando
   `counter_cost > cost`, decide `escalate_correct` corretamente nas 4 classes
   do cenário.
5. **RF5 — Contabilidade do incidente:** `run_week()` reporta por política:
   taxa de escalonamento, custo de escalonamento, prejuízo de counter-cost
   (casos errados), custo líquido total. ONE_SIDED fecha o número do prólogo:
   0 escalonamentos, R$ 5.280 + R$ 3.600 de prejuízo; TWO_SIDED escala os 17
   corretos (11 fraude + 6 churn) a R$ 136 e evita os R$ 8.880 de prejuízo.
6. **RF6 — Alinhamento prompt-vs-eval:** `run_week()` avalia cada política
   contra o eval de calibração (os casos cuja resposta correta é
   `escalate_correct`): ONE_SIDED pontua 0/17, TWO_SIDED 17/17 — a instrução
   balanceada é a que descreve o mesmo comportamento que o eval define como
   correto (`...patterns.md:106`).

### Requisitos Técnicos

1. **RT1 — Python 3.9+, stdlib apenas**, type hints obrigatórios
2. **RT2 — `dataclasses` + enums**; o linter trabalha por linha com marcação
   explícita de instrução (linhas do fixture entre `<instruction>` ...
   `</instruction>`); simulação determinística
3. **RT3 — Funções puras:** decisão e contabilidade não mutam os casos
4. **RT4 — Toda decisão rastreável:** a `TWO_SIDED` carrega na decisão o
   counter-cost comparado (uma linha citável por caso)

---

## 🏗️ Arquitetura do Sistema

```
┌────────────────────────────────────────────────────────────────────────┐
│                 TWO-SIDED TRADE-OFF INSTRUCTION                         │
│                                                                        │
│  PROMPT (fixture)                    INSTRUCTION LINTER (RF2, RF3)      │
│  <instruction>                       lint() → OneSidedFinding           │
│  Escalonar custa R$ 8...            ┌────────────────────────────┐     │
│  Evite...                           │ lado declarado: cost       │     │
│  </instruction>                     │ faltante:    counter_cost  │     │
│         │                           └──────────┬─────────────────┘     │
│         │ one-sided                            │ rewrite()             │
│         ▼                                      ▼                       │
│  TradeOffInstruction (RF1)            texto em 2 lados + judgment_rule  │
│  cost_side / counter_cost_side /                                              │
│  judgment_rule                                │                         │
│         │                                     │                         │
│         ▼                                     ▼                         │
│  DECISION POLICY (RF4)               DECISION POLICY                     │
│  ONE_SIDED: evita → colapso          TWO_SIDED: R$ 8 vs R$ 480 por caso  │
│         │                                     │                         │
│         ▼                                     ▼                         │
│  WEEK REPORT (RF5, RF6)                                                │
│  ONE_SIDED: esc=0/180, prejuízo R$ 8.880, eval 0/17                     │
│  TWO_SIDED: esc=17/180 (R$ 136), prejuízo R$ 0,   eval 17/17            │
│  → alinhamento prompt-vs-eval só existe na duas-lados                   │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 🎯 Sua Tarefa em 3 Partes

### Parte 1 — Diagnosticar o overfit de objetivo único (15 min)

Com o prólogo: por que "a menos que seja absolutamente necessário" não
protege contra o colapso? Faça a aritmética do incidente (economia de R$ 544
contra prejuízo de R$ 8.880) e responda: por que o eval verde no resto da
suite escondeu o problema? Responda como comentário.

### Parte 2 — Instrução balanceada e linter (35 min)

Implemente `TradeOffInstruction` com `OneSidedInstructionError` (RF1) e o
`InstructionLinter` com `lint()` e `rewrite()` (RF2-RF3).

### Parte 3 — Simulação das duas políticas (30 min)

Implemente `DecisionPolicy` nas duas variantes (RF4) e `run_week()` (RF5-RF6):
o lote de 180 tickets, o custo líquido de cada política e o placar do eval de
calibração.

---

## 💻 Starter Code

```python
"""
Exercício 9 — Two-Sided Trade-off Instruction
Nível 2 — Padrões Práticos

Instruções de ação custosa declaram os DOIS lados: o custo de agir e o
counter-cost de evitar errado. Um lado só vira single-objective overfit.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


# ============================================================================
# DATA MODELS — a instrução como economia declarada
# ============================================================================

class Side(Enum):
    COST = "cost"                    # o lado de agir (escalonar, reembolsar)
    COUNTER_COST = "counter_cost"    # o lado de evitar errado


@dataclass(frozen=True)
class CostSide:
    """Um lado do trade-off, quantificado (RF1)."""
    side: Side
    description: str     # ex.: "tempo de humano por ticket"
    unit: str            # ex.: "BRL"
    amount: float        # ex.: 8.0


class OneSidedInstructionError(Exception):
    """Instrução com um lado só não constrói (RF1)."""


@dataclass(frozen=True)
class TradeOffInstruction:
    """
    A instrução balanceada (RF1): dois lados + judgment_rule que delega
    a decisão por caso. "A balanced instruction declaring both sides of
    the trade-off, letting the model make the judgment per case"
    (patterns.md:102).
    """
    action: str                 # ex.: "escalonar para humano"
    cost_side: CostSide
    counter_cost_side: CostSide
    judgment_rule: str          # quando um lado domina o outro, em texto

    def render(self) -> str:
        """O texto que vai pro prompt: dois lados + julgamento por caso."""
        # TODO: implemente
        raise NotImplementedError


@dataclass(frozen=True)
class OneSidedFinding:
    """O achado do linter (RF2): instrução que enunciou um lado só."""
    line: int
    text: str
    declared: Side       # o lado que a instrução enunciou
    missing: Side        # o lado que faltou


# ============================================================================
# LINTER + REWRITE
# ============================================================================

@dataclass(frozen=True)
class InstructionLinter:
    """
    Varre o prompt (RF2). Convenção do fixture: cada instrução vive entre
    <instruction> e </instruction>; uma instrução é ONE-SIDED quando enuncia
    um lado (padrão de custo/verbo de ação OU contra-custo) sem o outro
    dentro da MESMA instrução.
    """
    prompt: str

    def lint(self) -> list[OneSidedFinding]:
        # TODO: implemente
        raise NotImplementedError

    def rewrite(self, finding: OneSidedFinding,
                counter: CostSide, judgment_rule: str) -> str:
        """
        O texto em dois lados (RF3): cita os dois valores e termina
        delegando o julgamento por caso. Palavras de regra dura
        ("sempre", "nunca") são proibidas no output.
        """
        # TODO: implemente
        raise NotImplementedError


# ============================================================================
# SIMULAÇÃO — as duas políticas
# ============================================================================

class PolicyKind(Enum):
    ONE_SIDED = "one_sided"   # conhece só o lado do custo → evita sempre
    TWO_SIDED = "two_sided"   # compara os dois lados por caso


@dataclass(frozen=True)
class EscalationCase:
    """Um ticket do lote: classe, marcação e os dois custos reais."""
    case_id: str
    category: str            # "fraude" | "plano" | "churn-top" | "senha"
    mandatory_flag: bool     # marcação OBRIGATÓRIA (não existe no lote)
    escalate_cost: float     # R$ 8 em todo caso
    counter_cost: float      # prejuízo de NÃO escalar quando devia
    escalate_correct: bool   # o que o eval de calibração define como certo


@dataclass(frozen=True)
class Decision:
    case_id: str
    escalated: bool
    rationale: str           # uma linha citável (RT4) — vazio no ONE_SIDED


@dataclass(frozen=True)
class DecisionPolicy:
    kind: PolicyKind
    escalate_cost_threshold: float = 8.0   # o custo conhecido da ação

    def decide(self, case: EscalationCase) -> Decision:
        """
        ONE_SIDED (RF4): escala só com mandatory_flag — o colapso do
          prólogo (nenhum caso do lote tem a flag).
        TWO_SIDED (RF4): escala quando counter_cost > escalate_cost;
          a rationale cita os dois valores comparados (RT4).
        """
        # TODO: implemente
        raise NotImplementedError


@dataclass
class WeekReport:
    policy: PolicyKind
    total_cases: int = 0
    escalations: int = 0
    escalation_spend: float = 0.0       # custo de escalar (R$ 8 cada)
    counter_cost_damage: float = 0.0    # prejuízo dos que DEVIA e não escalou
    net_cost: float = 0.0               # spend + damage
    eval_score: tuple[int, int] = (0, 0)  # acertos/total vs escalate_correct


def run_week(cases: list[EscalationCase],
             policy: DecisionPolicy) -> WeekReport:
    """
    O lote do prólogo (RF5, RF6): decisões, contabilidade e o placar do
    eval de calibração (cases com escalate_correct=True).
    """
    # TODO: implemente
    raise NotImplementedError


# ============================================================================
# FIXTURES — o prompt e o lote da semana
# ============================================================================

KODA_PROMPT = """<instruction>
Escalonar custa R$ 8 por ticket em tempo de humano.
Evite escalonar a menos que seja absolutamente necessário.
</instruction>
<instruction>
Antes de responder, confira a política de reembolso no catálogo.
</instruction>"""


def build_week() -> list[EscalationCase]:
    """180 tickets em 4 classes (cenário): 17 com escalate_correct=True."""
    cases: list[EscalationCase] = []
    for i in range(11):   # fraude: escalar é correto
        cases.append(EscalationCase(
            f"fraude-{i}", "fraude", False, 8.0, 480.0, True))
    for i in range(68):   # dúvida de plano: self-service resolve
        cases.append(EscalationCase(
            f"plano-{i}", "plano", False, 8.0, 0.0, False))
    for i in range(6):    # churn top: escalar é correto (LTV em risco)
        cases.append(EscalationCase(
            f"churn-{i}", "churn-top", False, 8.0, 600.0, True))
    for i in range(95):   # senha: self-service resolve
        cases.append(EscalationCase(
            f"senha-{i}", "senha", False, 8.0, 0.0, False))
    return cases


# ============================================================================
# TESTS
# ============================================================================

def test_instruction_requires_both_sides():
    only_cost = CostSide(Side.COST, "tempo de humano", "BRL", 8.0)
    try:
        TradeOffInstruction(
            action="escalonar", cost_side=only_cost,
            counter_cost_side=only_cost, judgment_rule="",
        )
        raise AssertionError("judgment_rule vazio deve recusar (RF1)")
    except OneSidedInstructionError as exc:
        assert "judgment" in str(exc), "a exceção nomeia o que faltou"
    print("TESTE 1 PASSOU")


def test_linter_finds_one_sided():
    linter = InstructionLinter(KODA_PROMPT)
    findings = linter.lint()
    assert len(findings) == 1, "só a instrução de custo é one-sided (RF2)"
    finding = findings[0]
    assert finding.declared == Side.COST
    assert finding.missing == Side.COUNTER_COST
    print("TESTE 2 PASSOU")


def test_rewrite_is_two_sided():
    linter = InstructionLinter(KODA_PROMPT)
    finding = linter.lint()[0]
    counter = CostSide(
        Side.COUNTER_COST, "chargeback de fraude não escalada", "BRL", 480.0)
    rewritten = linter.rewrite(
        finding, counter, "escale quando o counter-cost dominar o caso")
    lowered = rewritten.lower()
    assert "8" in rewritten and "480" in rewritten, "cita os dois valores (RF3)"
    assert "nunca" not in lowered and "sempre" not in lowered, (
        "rewrite não vira regra dura (RF3)")
    print("TESTE 3 PASSOU")


def test_two_policies_two_outcomes():
    cases = build_week()
    one = run_week(cases, DecisionPolicy(PolicyKind.ONE_SIDED))
    two = run_week(cases, DecisionPolicy(PolicyKind.TWO_SIDED))

    # ONE_SIDED: o colapso do prólogo (RF5)
    assert one.escalations == 0
    assert one.counter_cost_damage == 11 * 480.0 + 6 * 600.0, "R$ 8.880"
    assert one.eval_score == (0, 17), "eval de calibração zera (RF6)"

    # TWO_SIDED: o julgamento por caso (RF5)
    assert two.escalations == 17, "fraude + churn-top (RF4)"
    assert two.escalation_spend == 17 * 8.0, "R$ 136"
    assert two.counter_cost_damage == 0.0
    assert two.net_cost < one.net_cost, "a dois-lados vence no líquido"
    assert two.eval_score == (17, 17), "alinhada com o eval (RF6)"
    print("TESTE 4 PASSOU")


if __name__ == "__main__":
    print("=" * 60)
    print("EXERCÍCIO 9: TWO-SIDED TRADE-OFF INSTRUCTION")
    print("=" * 60)
    # Descomente após implementar:
    # test_instruction_requires_both_sides()
    # test_linter_finds_one_sided()
    # test_rewrite_is_two_sided()
    # test_two_policies_two_outcomes()
    print("\nTODO: implemente TradeOffInstruction.render,")
    print("InstructionLinter.lint/rewrite, DecisionPolicy.decide e run_week")
```

---

## ✅ Validação: Critérios de Aceitação

Seu código será considerado **APROVADO** quando:

- [ ] `TradeOffInstruction` recusa lado faltante e `judgment_rule` vazio com `OneSidedInstructionError` nomeando o que faltou (RF1)
- [ ] `lint()` acha exatamente a instrução de custo do fixture como one-sided (a de política de reembolso não é) com lado faltante correto (RF2)
- [ ] `rewrite()` cita os dois valores e não contém "sempre"/"nunca" — julgamento delegado, não regra dura (RF3)
- [ ] `ONE_SIDED` escala 0/180 com R$ 8.880 de prejuízo; `TWO_SIDED` escala os 17 corretos a R$ 136 com prejuízo zero (RF4, RF5)
- [ ] Placar do eval de calibração: 0/17 contra 17/17 — o alinhamento prompt-vs-eval só existe na dois-lados (RF6)
- [ ] Toda decisão `TWO_SIDED` carrega rationale citável com os dois valores comparados (RT4)

---

## 📊 Rubric de Avaliação

| Critério | Peso | Insuficiente (0-3) | Básico (4-6) | Proficiente (7-8) | Excelente (9-10) |
|---|---|---|---|---|---|
| **Instrução balanceada (Parte 2)** | 25% | Não implementada | Dois lados sem quantificar | Lados quantificados + judgment_rule obrigatório | `render()` lê como prompt real: economia declarada + julgamento delegado |
| **Linter (Parte 2)** | 25% | Não implementado | Marca qualquer instrução | Acha só a de um lado, com lado faltante nomeado | Não gera falso positivo na instrução neutra do fixture |
| **Simulação (Parte 3)** | 30% | Não implementada | Uma política só | Duas políticas com contabilidade fechando os números do prólogo | Rationale por decisão e net_cost comparando as políticas |
| **Alinhamento com eval (Parte 3)** | 20% | Ausente | Placar calculado sem narrativa | 0/17 vs 17/17 ligado ao conflito prompt-eval do prólogo | Explica por que instrução e eval devem descrever o MESMO correto |

**Nota final:** Média ponderada. **Aprovação:** >= 7.0

---

## 💡 Dicas para Implementação

1. **O linter não precisa de NLP.** Use a convenção do fixture: instruções entre `<instruction>`/`</instruction>`; um lado enunciado = texto de custo de ação (contém cifra/palavra de custo) sem contra-custo na MESMA instrução. A instrução de política de reembolso não fala de custo de ação — ela deve passar batida. Se seu linter marca ela, é falso positivo (e o rubric cobra).
2. **A decisão TWO_SIDED é uma comparação, não um gatilho.** `counter_cost > escalate_cost` — nada de `if category == "fraude"`. No dia em que a fraude custar R$ 6, a instrução de dois lados continua certa e o gatilho hardcoded para de ser. É a diferença entre julgamento e regra.
3. **O prejuízo só conta onde `escalate_correct` é True.** Não escalar um reset de senha não gera counter-cost — o self-service resolve (counter_cost 0). Misturar os dois lados na contabilidade infla o dano e destrói a comparação com o prólogo.

---

## ❓ Dúvidas Comuns

**P: Então toda instrução de custo deve virar julgamento por caso?**
R: Não — e o padrão diz o custo: "Converts a hard rule into a judgment; behavior becomes less deterministic" (`...patterns.md:109`). Regra dura continua certa quando o trade-off não existe (PII, segurança — aí o certo é o veto estrutural). O padrão se aplica à ação cujo custo varia por caso: escalonar, reembolsar, handoff. Se o custo é constante e alto em TODOS os casos, a regra dura é a economia correta.

**P: Isso não é a tested-degradation-ladder?**
R: Não — são camadas. O ladder ordena o que fazer quando algo FALHA em runtime (classificar, retry, fallback, humano — `docs/canonical/tested-degradation-ladder.md:29`); este padrão ensina o prompt a decidir ANTES de falhar se a ação custosa vale a pena neste caso. Um responde "como se recupera", o outro "quando se paga".

**P: Onde o counter-cost vem de?**
R: De conhecer o domínio "well enough to state them" (`...patterns.md:108`). O time do prólogo conhecia: chargeback de R$ 480, LTV de cliente top. Quando não dá para quantificar, o counter-cost qualitativo ("dano de confiança em cliente recorrente") ainda é infinitamente melhor que ausente — a ausência é o overfit.

**P: Por que o eval de calibração não segurou o incidente sozinho?**
R: Segurou — localmente (0/11 no que olhava). O problema é que o resto da suite estava verde e ninguém rodava o placar de calibração no review do prompt. O padrão resolve na ponta que faltava: a instrução passa a descrever o mesmo comportamento que o eval define, e o conflito some (`...patterns.md:106`).

---

## 🚀 Próximo Passo

Depois de completar este exercício:

1. Leia o padrão 5 completo e sua classificação: `docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-patterns.md:92-110` e `...classification.md:91-102` — Missing: a cobertura de escalonamento do repo é arquitetural, nunca instrucional
2. Siga a série: [[curriculum/02-nivel-2-practical-patterns/exercises/exercise-08-defensive-patch-ledger|Exercício 8]] audita o patch que sobrou → este exercício o reescreve em dois lados → [[curriculum/03-nivel-3-advanced-architecture/exercises/exercise-22-capability-escalation-ladder|Exercício 22]] escala a capacidade quando nenhum prompt resolve
3. Aplique ao KODA real: escolha UMA instrução de custo do prompt de suporte e escreva o counter-cost dela. Se ninguém no time souber o número, esse é o achado — e o trabalho.

---

*Exercício 9 | Nível 2 — Padrões Práticos | Two-Sided Trade-off Instruction*

**Quem declara só o lado barato ensina o modelo a economizar errado — diga os dois lados e deixe o caso decidir.**
