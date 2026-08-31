---
title: "Exercício 12: Semantic-Rule-Gated Auto Approve/Block — Decidir Merge por Regras Codificadas, Nunca por Discrição"
type: exercise
level: 3
aliases: ["semantic rule gated auto approve block", "semantic-rule-gated auto approve", "auto approve auto block por regras semânticas", "rule-gated merge decision", "rule ledger", "ledger de regras semânticas", "widening gradual de automação", "auditable auto approve"]
tags: [curriculo-conteudo, agentes-orquestracao, code-review, governanca, evals, context-engineering, production, semantic-rule-gating, auto-approve-block, rule-ledger, python, dataclass]
relates-to: ["[[docs/canonical/semantic-rule-gated-auto-approve-block|Semantic-Rule-Gated Auto Approve/Block]]", "[[docs/analysis/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co-patterns|Source Patterns]]", "[[docs/analysis/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co-classification|Source Classification]]", "[[docs/canonical/evals-as-brakes|Evals-as-Brakes]]", "[[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]]", "[[docs/canonical/shadow-review-pipeline|Shadow Review Pipeline]]", "[[docs/canonical/human-review-staged-workflow-automation|Human-Review Staged Workflow Automation]]", "[[curriculum/03-nivel-3-advanced-architecture/exercises/exercise-11-software-graph-review-substrate|Exercício 11: Software Graph Review Substrate]]"]
duration: "90-120 min"
---

# ⚖️ Exercício 12: Semantic-Rule-Gated Auto Approve/Block — Decidir Merge por Regras Codificadas, Nunca por Discrição
## Nível 3 — Arquitetura Avançada

**Tempo Estimado:** 90-120 minutos
**Dificuldade:** ⭐⭐⭐⭐ (Avançado)
**Pré-requisito:** Ter lido `docs/canonical/evals-as-brakes.md` + Exercício 11 (`exercise-11-software-graph-review-substrate.md`) e Exercício 7 (`exercise-shadow-review-pipeline.md`, Nível 3 — Operacional)
**Objetivo:** Construir o ledger de regras semânticas codificadas com proveniência — cada regra carrega o incidente/discussão que a originou (Parte 1), o motor de decisão onde approve/block decorre SOMENTE de regras ativas, com relatório de auditoria que lista as regras violadas e o link para todas as regras aplicadas, e casos uncoded roteados para humano por design (Parte 2), e o pipeline de alargamento gradual: telemetria por período, candidatas a regra extraídas dos findings uncoded, e a simulação que prova que a taxa de automação cresce acumulando regras — não confiança de modelo (Parte 3)

---

## 📖 Prólogo: O Approve Que Ninguém Sabia Explicar

**MeridianPay, três semanas depois do P0 do Exercício 11. O time tinha acabado de ligar o "auto-approve com IA" — o reviewer bot decide sozinho quando a confiança passa de 0.85. Quinta-feira, reunião de governança com o comitê de risco.**

```
╔══════════════════════════════════════════════════════════════════╗
║           COMITÊ DE RISCO — AUDITORIA DO AUTO-APPROVE            ║
║                                                                  ║
║  AUDITORA:      "PR-47 foi auto-aprovado na terça e quebrou o    ║
║                 settlement do domingo. Pergunta de auditoria:    ║
║                 POR QUE foi aprovado?"                           ║
║                                                                  ║
║  TECH LEAD:     "O modelo teve confiança 0.91. O threshold       ║
║                 era 0.85."                                       ║
║                                                                  ║
║  AUDITORA:      "0.91 de quê? Baseado em quê? Quem decidiu que   ║
║                 0.85 é o número certo? Se eu perguntar de novo   ║
║                 amanhã, o modelo dá o mesmo 0.91 para o mesmo    ║
║                 diff?"                                           ║
║                                                                  ║
║  TECH LEAD:     "...provavelmente não. É um modelo."             ║
║                                                                  ║
║  AUDITORA:      "Então o critério de merge da empresa é uma      ║
║                 função que ninguém consegue citar, reproduzir    ║
║                 nem controlar. Vocês não têm um gate. Têm um     ║
║                 oráculo. Devolvam o approve para humanos ou       ║
║                 tragam algo auditável."                          ║
╚══════════════════════════════════════════════════════════════════╝
```

A sala de guerra, na mesma noite:

```
DIRETORA DE ENG:  "Desligar tudo?"

PLATAFORMA:       "Não. Codificar. O problema não é automatizar o
                   approve — é AUTOMATIZAR POR DISCRICÃO. A pergunta
                   certa não é 'o modelo confia?', é 'quais regras
                   este PR viola ou satisfaz?'.

                   Regra 1 (bloqueio): interpolação de string em
                   query SQL — veio do INC-2025-091.
                   Regra 2 (bloqueio): null-check obrigatório antes
                   de acesso em objetos de pagamento — veio do RCA
                   de março.
                   Regra 3 (approve): suite completa verde no CI.
                   Regra 4 (approve): diff só toca paths com cobertura
                   de eval >= 0.9.

                   O motor decide SOENTE por esse ledger: violou
                   bloqueio → BLOCK com a regra citada; satisfez
                   todas as approve e nenhum finding sem regra →
                   AUTO_APPROVE; QUALQUER coisa fora das regras →
                   HUMAN_REVIEW. Nunca 'porque o modelo achou ok'.

                   E o ledger cresce com o tempo: todo finding sem
                   regra vira candidata a regra. A cada candidatura
                   codificada, a automação alarga um degrau — 'step
                   by step by adding more rules for blocking and more
                   rules for approving over time'."

DIRETORA:         "E o comitê?"

PLATAFORMA:       "Cada decisão vem com o relatório: regras violadas,
                   regras satisfeitas, e o link para TODAS as regras
                   aplicadas. Auditoria de uma linha: o veredito é uma
                   consequência lógica do ledger, não uma opinião."
```

**O pipeline que você vai implementar roda essa mudança de regime:** no mês 1, com 4 regras no ledger, 50% das decisões são automáticas e os findings uncoded (`error-handling-gap`, `naming-style`) vão para humano — e alimentam a fila de candidatas. No mês 2, `error-handling-gap` vira a regra R-003 (proveniência: os findings uncoded do mês 1), e a mesma classe de PR passa de HUMAN_REVIEW para BLOCK — sem mudar uma linha do motor. A automação alargou porque o contexto acumulou.

Este padrão não existe implementado no repositório: a classificação o marcou `Partial Coverage` com valor de integração `High` (`docs/analysis/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co-classification.md:102-117`) — os gates existentes são dirigidos por thresholds de eval e tiers de confiança, nunca por um conjunto expansivo de regras semânticas acumuladas como contexto auditable. Você está construindo a primeira implementação.

---

## 🧠 O Contexto

### O Modelo Mental: o Critério de Decisão é Contexto Acumulado, não Capacidade do Modelo

O padrão vem da talk "The Last Human Code Review" (Itamar Friedman, Qodo): ao atingir maturidade de context engine com grafo, "now you're ready to start approving and blocking PRs automatically. And you want to do that not just by letting AI choose by yourself rather giving some semantic rules... when do you guys approve or block a PR and that knowledge also needs to be accumulated as part of your context" (`docs/analysis/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co-analysis.md:72-75`).

O mecanismo tem quatro propriedades load-bearing:

| Propriedade | Mecanismo | O que resolve |
|---|---|---|
| **Só regras** | Veredito é consequência lógica do ledger ativo; a API do motor não recebe score/confiança de modelo | "Humans can trust and audit and control" — auditoria de uma linha |
| **Uncoded → humano** | Finding sem regra roteia para HUMAN_REVIEW, sempre | "Coverage is limited to codified rules; uncoded cases still need humans" (`...patterns.md:121`) |
| **Acúmulo como contexto** | Cada regra carrega proveniência (incidente/RCA que a originou); findings uncoded viram candidatas | O critério de approve/block é ele mesmo contexto acumulado |
| **Alargamento gradual** | Automação cresce codificando regras, uma a uma — nunca big-bang | "Gradually... step by step by adding more rules for blocking and more rules for approving over time" (`...analysis.md:75`) |

A simetria com a tese central da fonte: confiança é infraestrutura de conhecimento, não capacidade de modelo (`...analysis.md:38-42`). Aqui a tese é levada ao extremo — nem a decisão final fica com o modelo.

### Fronteiras do padrão (o que NÃO é este motor)

1. **Regras semânticas ≠ threshold de eval.** O [[docs/canonical/evals-as-brakes|Evals-as-Brakes]] define o tier `auto-merge` gated em `eval_coverage >= 0.9 of changed behaviors`, PR eval report e correlação eval-produção (`docs/canonical/evals-as-brakes.md:59-63`) — gates quantitativos sobre métricas de teste. Aqui o gate é um conjunto de regras *semânticas* codificadas (o que é aceitável neste códigobase) que cresce por acumulação. Os dois se compõem: uma regra APPROVE pode *citar* cobertura de eval como condição (a regra R-102 do exercício faz exatamente isso) — a diferença é que a regra é um artefato versionado com proveniência, não um número no CI.

2. **Uncoded → humano ≠ modelo decide.** O [[docs/canonical/pre-commit-ai-review-gate|Pre-Commit AI Review Gate]] opera política de confiança em tiers ("block when high-confidence fail", `docs/canonical/pre-commit-ai-review-gate.md:75`) — a confiança do achado participa da decisão. Aqui a confiança não existe na API do motor: o achado ou cita uma regra (decidível) ou é uncoded (humano). É a diferença entre gate por evidência classificada e gate por discrição estruturada.

3. **Alargamento por regras ≠ graduação por concordância.** O [[docs/canonical/shadow-review-pipeline|Shadow Review Pipeline]] gradua checks de advisory para blocking por métricas de concordância AI-vs-humano (`docs/canonical/shadow-review-pipeline.md:31`). Aqui ninguém "gradua": adiciona-se regra nova ao ledger, com proveniência. O sinal de prontidão é diferente — lá, agreement; aqui, o fluxo de findings uncoded que justifica a codificação.

4. **AUTO_APPROVE ≠ envio irreversível.** O [[docs/canonical/human-review-staged-workflow-automation|Human-Review Staged Workflow Automation]] mantém o humano dono do ato irreversível ("O envio irreversível permanece humano", `docs/canonical/human-review-staged-workflow-automation.md:58`). Este exercício decide *merge de PR* por regras; deploy/send irreversível continua sendo estágio humano de outro padrão. A classificação da fonte nota exatamente essa contraposição (`...classification.md:114`).

5. **Este motor ≠ o grafo do Exercício 11.** O [[curriculum/03-nivel-3-advanced-architecture/exercises/exercise-11-software-graph-review-substrate|Exercício 11]] produz os achados estruturais (colisão cross-PR, mudança quebradora de contrato); este exercício decide o veredito a partir de regras. Na fonte, a progressão é explícita: context engine e grafo são os pré-requisitos ("Context-engine and graph maturity (patterns 1-2) as prerequisites", `...patterns.md:111`). Aqui os findings chegam prontos — o foco é o substrato de decisão.

### O Que Você Vai Construir

1. **`RuleLedger`** (Parte 1 — o contexto acumulado): regras semânticas com `rule_id`, kind (BLOCK/APPROVE), statement, scope e proveniência; inserção idempotente por id
2. **`DecisionEngine.decide`** (Parte 2 — o motor): BLOCK por regra violada; AUTO_APPROVE somente com todas as APPROVE satisfeitas e zero findings uncoded; HUMAN_REVIEW em todo o resto — e o `DecisionReport` com a trilha de auditoria (regras aplicadas, violadas, satisfeitas, uncoded)
3. **`AutomationTelemetry` + `run_governance_simulation`** (Parte 3 — o alargamento): taxa de automação por período, categorias uncoded como candidatas a regra, e a simulação de dois meses provando que a automação cresce por acumulação de regras — `render_review_report` fecha com a interface humana de auditoria

O domínio é o MeridianPay dos Exercícios 7 e 11: o ledger v1 com as 4 regras da sala de guerra, os 6 PRs do mês 1, e o ledger v2 com a regra codificada a partir dos uncoded do mês 1.

---

## 📋 Cenário

### O Ledger v1 (mês 1 — as 4 regras da sala de guerra)

| ID | Kind | Statement | Proveniência |
|---|---|---|---|
| R-001 | BLOCK | Proibida interpolação de string em queries SQL (parametrized queries obrigatórias) | INC-2025-091 |
| R-002 | BLOCK | Null-check obrigatório antes de acesso a atributo em objetos de pagamento | RCA 2026-03 |
| R-101 | APPROVE | Suite completa de testes verde no CI | Decisão do time, 2026-07 |
| R-102 | APPROVE | Diff toca apenas paths com cobertura de eval >= 0.9 | evals-as-brakes |

### Os PRs do Mês 1 (W1)

| PR | Findings | Approve inputs | Veredito esperado |
|---|---|---|---|
| PR-301 | sql-injection → viola **R-001** | R-101 ✓, R-102 ✓ | **BLOCK** (auditável) |
| PR-302 | null-safety → viola **R-002** | R-101 ✓, R-102 ✓ | **BLOCK** |
| PR-303 | nenhum | R-101 ✓, R-102 ✓ | **AUTO_APPROVE** |
| PR-304 | error-handling-gap → **uncoded** | R-101 ✓, R-102 ✓ | **HUMAN_REVIEW** |
| PR-305 | nenhum | R-101 ✓, R-102 **✗** | **HUMAN_REVIEW** |
| PR-306 | naming-style → **uncoded** | R-101 ✓, R-102 ✓ | **HUMAN_REVIEW** |

### O Ledger v2 (mês 2 — acumulação)

| ID | Kind | Statement | Proveniência |
|---|---|---|---|
| R-003 (novo) | BLOCK | Exceções de boundary tratadas antes do handler HTTP | Findings uncoded de W1 |

No mês 2, `naming-style` ainda não foi codificada (volume insuficiente — gradual significa também *não* codificar por enquanto). Os mesmos shapes de PR rodam de novo: o PR com `error-handling-gap` agora cita R-003 e vira BLOCK — o motor não mudou, o ledger cresceu.

---

## ✅ Requisitos

### Funcionais

- [ ] `SemanticRule` carrega `rule_id`, `kind` (BLOCK/APPROVE), `statement`, `scope`, `source` (incidente/RCA/discussão de origem) e `added_at`
- [ ] `RuleLedger.add_rule` rejeita `rule_id` duplicado com `ValueError`; `active_rules()` retorna as regras ordenadas por `rule_id`; `get(rule_id)` recupera regra ou `None`
- [ ] `DecisionEngine.decide(pr, ledger)` aplica, em ordem: (1) `applied_rules` = todas as regras ativas; (2) `violated_rules` = findings cujo `violated_rule` é regra BLOCK ativa; (3) violou → `BLOCK`; (4) `uncoded_findings` = categorias dos findings sem regra; (5) approve rules split em satisfeitas/insatisfeitas via `approve_inputs`; (6) sem uncoded E sem insatisfeita → `AUTO_APPROVE`; (7) senão → `HUMAN_REVIEW`
- [ ] A API do motor não possui nenhum campo de score/confiança de modelo — finding ou cita regra ou é uncoded (invariante estrutural do padrão)
- [ ] `DecisionReport` lista `applied_rules` (a base da auditoria), `violated_rules`, `satisfied_approve_rules`, `unsatisfied_approve_rules`, `uncoded_findings` e `rationale` citando os `rule_id` relevantes
- [ ] `AutomationTelemetry.automation_rate()` = (AUTO_APPROVE + BLOCK) / total (0.0 se vazio); `uncoded_categories()` = categorias uncoded únicas ordenadas; `propose_rule_candidates()` = as uncoded como candidatas à codificação
- [ ] `render_review_report(report, ledger)` produz a interface humana de auditoria: veredito, regras violadas com statement, e **o link para todas as regras aplicadas**
- [ ] Na simulação de dois períodos: W1 com ledger v1 → taxa 0.5; W2 com ledger v2 → taxa estritamente maior; todo report tem `applied_rules` não-vazio

### Técnicos

- [ ] Python 3.9+ com type hints (`from __future__ import annotations`)
- [ ] Apenas biblioteca padrão; `dataclasses` para todos os modelos, `Enum` para `Verdict` e `RuleKind`
- [ ] `decide()` é puro, determinístico e sem I/O — mesma entrada + mesmo ledger = mesmo veredito (reprodutibilidade de auditoria)
- [ ] `AUTO_VERDICTS` como constante nomeada; nenhum "magic string" para veredito
- [ ] Dados de teste 100% determinísticos (ledgers e batches declarados literalmente nos builders)

### Validação

- [ ] Cenário 1: PR-301 → BLOCK com `violated_rules == ["R-001"]` e `applied_rules` contendo as 4 regras ativas
- [ ] Cenário 2: PR-303 → AUTO_APPROVE com zero insatisfeitas; PR-305 (approve input faltante) → HUMAN_REVIEW
- [ ] Cenário 3: PR-304 (uncoded) → HUMAN_REVIEW com `uncoded_findings == ["error-handling-gap"]` — nunca decidido pela máquina
- [ ] Cenário 4: mesmo shape de PR no ledger v1 → HUMAN_REVIEW; no ledger v2 (R-003 codificada) → BLOCK — o veredito muda por acumulação, não por modelo
- [ ] Cenário 5: taxa W1 == 0.5; taxa W2 > taxa W1; `"error-handling-gap"` em `propose_rule_candidates()` de W1
- [ ] Cenário 6: `render_review_report` contém o `pr_id`, os ids das regras violadas E de todas as regras aplicadas

---

## 🏗️ Arquitetura do Sistema

```
┌──────────────────────────────────────────────────────────────────┐
│         SEMANTIC-RULE-GATED AUTO APPROVE/BLOCK                    │
│                                                                   │
│  PARTE 1 — O LEDGER (o contexto acumulado)                        │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │  RuleLedger                                             │     │
│  │   R-001 BLOCK  sem SQL interpolada      [INC-2025-091]  │     │
│  │   R-002 BLOCK  null-check em pagamento  [RCA 2026-03]   │     │
│  │   R-101 APPROVE suite verde no CI       [time 2026-07]  │     │
│  │   R-102 APPROVE cobertura eval >= 0.9   [evals-brakes]  │     │
│  │        + R-003 BLOCK (mês 2)            [uncoded de W1] │     │
│  │   cada regra = proveniência + statement + scope          │     │
│  └───────────────────────────┬────────────────────────────────┘   │
│                              ▼                                    │
│  PARTE 2 — O MOTOR (só regras; zero discrição)                    │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │  PR + findings ──► DecisionEngine.decide(pr, ledger)     │     │
│  │                                                          │     │
│  │  1. finding cita regra BLOCK violada?                    │     │
│  │        sim ──► BLOCK (regra citada no rationale)         │     │
│  │  2. finding uncoded (sem regra)?                         │     │
│  │        sim ──► HUMAN_REVIEW (sempre — nunca discrição)   │     │
│  │  3. todas as APPROVE satisfeitas?                        │     │
│  │        sim ──► AUTO_APPROVE                              │     │
│  │        não  ──► HUMAN_REVIEW (condição faltante citada)  │     │
│  │                                                          │     │
│  │  DecisionReport = trilha de auditoria:                   │     │
│  │    applied_rules (TODAS) · violated · satisfied ·        │     │
│  │    unsatisfied · uncoded · rationale                     │     │
│  └───────────────────────────┬────────────────────────────────┘   │
│                              ▼                                    │
│  PARTE 3 — O ALARGAMENTO (automação cresce com o ledger)          │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │  W1 (ledger v1):  BLOCK×2 · AUTO×1 · HUMAN×3 → taxa 0.5  │     │
│  │     uncoded: error-handling-gap, naming-style            │     │
│  │     propose_rule_candidates() ──┐                        │     │
│  │                                 ▼                        │     │
│  │  codifica R-003 (error-handling-gap) — naming espera     │     │
│  │  volume (gradual também é NÃO codificar)                 │     │
│  │                                                          │     │
│  │  W2 (ledger v2):  BLOCK×3 · AUTO×1 · HUMAN×2 → taxa 0.67 │     │
│  │                                                          │     │
│  │  invariante: todo veredito tem applied_rules não-vazio   │     │
│  │  render_review_report → interface humana auditável       │     │
│  └──────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────┘
```

---

## 🎯 Sua Tarefa em 3 Partes

### Parte 1 — Modelar o ledger (`RuleLedger`, `SemanticRule`)
O ledger é o artefato de contexto do padrão: cada regra é conhecimento codificado com proveniência — o incidente que a justifica é parte do dado, porque é ele que torna a regra auditável ("por que existe esta regra?" é tão importante quanto "por que este PR foi bloqueado?"). A imutabilidade de id (duplicado rejeita) é o que mantém a trilha de auditoria íntegra.

### Parte 2 — Construir o motor (`DecisionEngine.decide`)
A ordem das perguntas é a semântica de governança: primeiro BLOCK (uma violação codificada basta), depois uncoded (o que não tem regra nunca é decidido pela máquina), por fim approve (a ausência de violação não é aprovação — aprovação exige condições positivas satisfeitas). O `DecisionReport` não é log: é o documento que a auditora do prólogo pediu — regras violadas com citación e o conjunto completo de regras aplicadas.

### Parte 3 — Provar o alargamento (`AutomationTelemetry`, `run_governance_simulation`)
A telemetria fecha o ciclo: decisões automáticas / total mede quão largo o funil está; `uncoded_categories` alimenta a fila de candidatas; a simulação de dois períodos prova a tese — o mesmo motor, ledgers diferentes, taxas diferentes. E `render_review_report` materializa a interface humana: "a link to all the rules that were being used... that's for human in order to trust" (`...analysis.md:58`).

---

## 💻 Starter Code

```python
"""
Exercício 12 — Semantic-Rule-Gated Auto Approve/Block
Nível 3 — Arquitetura Avançada

Pipeline: ledger de regras semânticas com proveniência → motor de
decisão onde approve/block decorre somente de regras ativas (uncoded
→ humano, sempre) → telemetria e simulação do alargamento gradual
por acumulação de regras.

Fonte do padrão: docs/analysis/2026-08-31-the-last-human-code-review-
building-trust-in-ai-generated-co/2026-08-31-the-last-human-code-review-
building-trust-in-ai-generated-co-patterns.md:105-123 (padrão 5,
Semantic-Rule-Gated Auto Approve/Block).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


# ============================================================================
# VEREDITOS E KINDS DE REGRA
# ============================================================================

class Verdict(Enum):
    AUTO_APPROVE = "auto_approve"    # todas as APPROVE satisfeitas, zero uncoded
    BLOCK = "block"                  # regra BLOCK ativa violada
    HUMAN_REVIEW = "human_review"    # uncoded ou condição de approve faltante


class RuleKind(Enum):
    BLOCK = "block"       # violação => bloqueia o merge
    APPROVE = "approve"   # condição => habilita auto-approve


AUTO_VERDICTS = {Verdict.AUTO_APPROVE, Verdict.BLOCK}


# ============================================================================
# PARTE 1 — O LEDGER: REGRAS SEMÂNTICAS COM PROVENIÊNCIA
# ============================================================================

@dataclass
class SemanticRule:
    """
    Uma regra semântica codificada — a unidade de contexto do padrão.

    A proveniência (source) é parte do dado: a regra é auditável
    porque carrega o incidente/RCA/discussão que a justifica.
    """
    rule_id: str
    kind: RuleKind
    statement: str
    scope: list[str] = field(default_factory=list)
    source: str = ""
    added_at: str = ""


class RuleLedger:
    """O contexto acumulado: todas as regras semânticas ativas."""

    def __init__(self) -> None:
        self._rules: dict[str, SemanticRule] = {}

    def add_rule(self, rule: SemanticRule) -> None:
        """
        TODO (Parte 1): inserir regra no ledger.

        Raises:
            ValueError: se rule_id já existir (id imutável preserva
                a integridade da trilha de auditoria).
        """
        # TODO: Implementar
        pass

    def active_rules(self) -> list[SemanticRule]:
        """TODO (Parte 1): regras ativas ordenadas por rule_id."""
        # TODO: Implementar
        pass

    def get(self, rule_id: str) -> SemanticRule | None:
        """TODO (Parte 1): recuperar regra por id (ou None)."""
        # TODO: Implementar
        pass


# ============================================================================
# PARTE 2 — O MOTOR: DECISÃO SOMENTE POR REGRAS
# ============================================================================

@dataclass
class ReviewFinding:
    """
    Um finding do reviewer para um PR.

    violated_rule preenchido => o finding cita uma regra codificada.
    violated_rule None       => uncoded: nenhuma regra cobre o caso
                                (a fila de candidatas do padrão).
    """
    finding_id: str
    category: str
    violated_rule: str | None = None
    details: str = ""


@dataclass
class PRCase:
    """
    Um PR submetido ao gate.

    Nota estrutural: NÃO existe campo de score/confiança de modelo.
    O finding ou cita regra (decidível) ou é uncoded (humano decide).
    """
    pr_id: str
    files: list[str] = field(default_factory=list)
    findings: list[ReviewFinding] = field(default_factory=list)
    approve_inputs: dict[str, bool] = field(default_factory=dict)


@dataclass
class DecisionReport:
    """A trilha de auditoria de uma decisão de merge."""
    pr_id: str
    verdict: Verdict
    applied_rules: list[str] = field(default_factory=list)
    violated_rules: list[str] = field(default_factory=list)
    satisfied_approve_rules: list[str] = field(default_factory=list)
    unsatisfied_approve_rules: list[str] = field(default_factory=list)
    uncoded_findings: list[str] = field(default_factory=list)
    rationale: str = ""


class DecisionEngine:
    """Approve/block dirigidos SOMENTE por regras codificadas."""

    @staticmethod
    def decide(pr: PRCase, ledger: RuleLedger) -> DecisionReport:
        """
        TODO (Parte 2): decidir o veredito de um PR contra o ledger.

        Ordem (a semântica de governança):
          1. applied_rules = ids de TODAS as regras ativas
             (a base citável da auditoria — sempre não-vazia aqui).
          2. violated_rules = findings cujo violated_rule existe no
             ledger E é RuleKind.BLOCK (ordem estável dos findings).
          3. violated_rules não-vazio => Verdict.BLOCK.
          4. uncoded_findings = categorias dos findings com
             violated_rule None (sem duplicatas, ordenadas).
          5. approve rules ativas: satisfied = approve_inputs[rid]
             is True; o resto = unsatisfied.
          6. sem uncoded E sem unsatisfied => Verdict.AUTO_APPROVE.
          7. senão => Verdict.HUMAN_REVIEW.
          8. rationale citando os rule_id que fundamentam o veredito.

        Args:
            pr: O PR com findings e approve inputs.
            ledger: O ledger de regras ativas.

        Returns:
            DecisionReport — veredito + trilha completa de auditoria.
        """
        # TODO: Implementar
        pass


# ============================================================================
# PARTE 3 — TELEMETRIA, SIMULAÇÃO E INTERFACE DE AUDITORIA
# ============================================================================

class AutomationTelemetry:
    """Telemetria do funil de decisão por período."""

    def __init__(self) -> None:
        self.reports: list[DecisionReport] = []

    def record(self, report: DecisionReport) -> None:
        """TODO (Parte 3): registrar uma decisão."""
        # TODO: Implementar
        pass

    def automation_rate(self) -> float:
        """
        TODO (Parte 3): (AUTO_APPROVE + BLOCK) / total de decisões.

        Returns:
            Float em [0.0, 1.0]; 0.0 se nenhuma decisão registrada.
        """
        # TODO: Implementar
        pass

    def uncoded_categories(self) -> list[str]:
        """TODO (Parte 3): categorias uncoded únicas, ordenadas."""
        # TODO: Implementar
        pass

    def propose_rule_candidates(self) -> list[str]:
        """
        TODO (Parte 3): as uncoded_categories() como candidatas a
        codificação — o insumo do alargamento gradual.
        """
        # TODO: Implementar
        pass


def run_governance_simulation(
    prs: list[PRCase],
    ledger: RuleLedger,
) -> AutomationTelemetry:
    """
    TODO (Parte 3): rodar o gate sobre um batch de PRs.

    Fluxo: para cada PR, decidir contra o ledger e registrar na
    telemetria (a mesma API que o CI consumiria).

    Args:
        prs: O batch do período.
        ledger: O ledger vigente no período.

    Returns:
        AutomationTelemetry com todas as decisões do período.
    """
    # TODO: Implementar
    pass


def render_review_report(
    report: DecisionReport,
    ledger: RuleLedger,
) -> str:
    """
    TODO (Parte 3): a interface humana de auditoria.

    Conteúdo obrigatório:
      - pr_id e veredito
      - cada regra violada com seu statement ("o que exige a regra")
      - o link (rule_id + statement) para TODAS as regras aplicadas
        — "that's for human in order to trust... the results"
        (analysis.md:58)

    Args:
        report: A decisão a renderizar.
        ledger: O ledger de onde as regras vêm.

    Returns:
        String multilinha pronta para o comentário do PR.
    """
    # TODO: Implementar
    pass


# ============================================================================
# DADOS DE TESTE — MERIDIANPAY (o regime pós-comitê de risco)
# ============================================================================

def build_rules_v1() -> RuleLedger:
    """Ledger do mês 1: as 4 regras da sala de guerra."""
    ledger = RuleLedger()
    ledger.add_rule(SemanticRule(
        rule_id="R-001",
        kind=RuleKind.BLOCK,
        statement="Proibida interpolação de string em queries SQL; parametrized queries obrigatórias",
        scope=["src/db/**"],
        source="INC-2025-091",
        added_at="2026-08-01",
    ))
    ledger.add_rule(SemanticRule(
        rule_id="R-002",
        kind=RuleKind.BLOCK,
        statement="Null-check obrigatório antes de acesso a atributo em objetos de pagamento",
        scope=["src/payment/**"],
        source="RCA 2026-03",
        added_at="2026-08-01",
    ))
    ledger.add_rule(SemanticRule(
        rule_id="R-101",
        kind=RuleKind.APPROVE,
        statement="Suite completa de testes verde no CI",
        scope=["**"],
        source="Decisão do time, 2026-07",
        added_at="2026-08-01",
    ))
    ledger.add_rule(SemanticRule(
        rule_id="R-102",
        kind=RuleKind.APPROVE,
        statement="Diff toca apenas paths com cobertura de eval >= 0.9",
        scope=["**"],
        source="evals-as-brakes",
        added_at="2026-08-01",
    ))
    return ledger


def build_rules_v2() -> RuleLedger:
    """Ledger do mês 2: v1 + R-003, codificada dos uncoded de W1."""
    ledger = build_rules_v1()
    ledger.add_rule(SemanticRule(
        rule_id="R-003",
        kind=RuleKind.BLOCK,
        statement="Exceções de boundary tratadas antes do handler HTTP",
        scope=["src/api/**"],
        source="Findings uncoded de W1 (error-handling-gap)",
        added_at="2026-09-01",
    ))
    return ledger


def _approve_inputs(green_ci: bool = True, eval_covered: bool = True) -> dict[str, bool]:
    return {"R-101": green_ci, "R-102": eval_covered}


def build_pr_batch_w1() -> list[PRCase]:
    """Os 6 PRs do mês 1 (tabela do Cenário)."""
    return [
        PRCase(
            pr_id="PR-301",
            files=["src/db/queries.py"],
            findings=[ReviewFinding(
                finding_id="F-1", category="sql-injection",
                violated_rule="R-001",
                details="f-string interpolada em SELECT",
            )],
            approve_inputs=_approve_inputs(),
        ),
        PRCase(
            pr_id="PR-302",
            files=["src/payment/gateway.py"],
            findings=[ReviewFinding(
                finding_id="F-2", category="null-safety",
                violated_rule="R-002",
                details="payment_method sem guard antes de .validate()",
            )],
            approve_inputs=_approve_inputs(),
        ),
        PRCase(
            pr_id="PR-303",
            files=["src/reports/format.py"],
            findings=[],
            approve_inputs=_approve_inputs(),
        ),
        PRCase(
            pr_id="PR-304",
            files=["src/api/handlers.py"],
            findings=[ReviewFinding(
                finding_id="F-3", category="error-handling-gap",
                violated_rule=None,
                details="process_payment() sem try/except no boundary",
            )],
            approve_inputs=_approve_inputs(),
        ),
        PRCase(
            pr_id="PR-305",
            files=["src/experimental/scraper.py"],
            findings=[],
            approve_inputs=_approve_inputs(green_ci=True, eval_covered=False),
        ),
        PRCase(
            pr_id="PR-306",
            files=["src/utils/strings.py"],
            findings=[ReviewFinding(
                finding_id="F-4", category="naming-style",
                violated_rule=None,
                details="variável 'q' fora da convenção",
            )],
            approve_inputs=_approve_inputs(),
        ),
    ]


def build_pr_batch_w2() -> list[PRCase]:
    """
    Os PRs do mês 2: mesmos shapes; o anti-pattern de error-handling
    agora cita R-003 (a regra codificada a partir dos uncoded de W1).
    naming-style permanece uncoded — gradual também é NÃO codificar.
    """
    batch = build_pr_batch_w1()
    for pr in batch:
        if pr.pr_id == "PR-304":
            pr.findings = [ReviewFinding(
                finding_id="F-3b", category="error-handling-gap",
                violated_rule="R-003",
                details="process_payment() sem try/except no boundary",
            )]
    return batch


# ============================================================================
# TESTES
# ============================================================================

def test_1_block_auditavel():
    """Cenário 1: BLOCK é consequência lógica do ledger, com citação."""
    print("\n" + "=" * 60)
    print("TESTE 1: BLOCK Auditável — regra citada, trilha completa")
    print("=" * 60)

    ledger = build_rules_v1()
    pr_301 = build_pr_batch_w1()[0]
    report = DecisionEngine.decide(pr_301, ledger)

    assert report.verdict == Verdict.BLOCK
    assert report.violated_rules == ["R-001"], (
        f"esperado ['R-001'], obtido {report.violated_rules}"
    )
    assert set(report.applied_rules) == {"R-001", "R-002", "R-101", "R-102"}, (
        "a auditoria lista TODAS as regras aplicadas"
    )
    assert "R-001" in report.rationale, "o rationale cita a regra violada"

    print(f"  PR-301 → {report.verdict.value} por {report.violated_rules}")
    print(f"  regras aplicadas: {sorted(report.applied_rules)}")
    print("  TESTE 1 PASSOU")


def test_2_auto_approve_por_regras():
    """Cenário 2: aprovação exige condições positivas satisfeitas."""
    print("\n" + "=" * 60)
    print("TESTE 2: AUTO_APPROVE — todas as APPROVE satisfeitas")
    print("=" * 60)

    ledger = build_rules_v1()
    batch = build_pr_batch_w1()

    r303 = DecisionEngine.decide(batch[2], ledger)
    assert r303.verdict == Verdict.AUTO_APPROVE
    assert r303.unsatisfied_approve_rules == []
    assert r303.violated_rules == []

    r305 = DecisionEngine.decide(batch[4], ledger)
    assert r305.verdict == Verdict.HUMAN_REVIEW, (
        "approve input faltante (R-102) NÃO é auto-approve por confiança"
    )
    assert r305.unsatisfied_approve_rules == ["R-102"]

    print(f"  PR-303 → {r303.verdict.value} (R-101 + R-102 satisfeitas)")
    print(f"  PR-305 → {r305.verdict.value} (R-102 insatisfeita)")
    print("  TESTE 2 PASSOU")


def test_3_uncoded_e_humano():
    """Cenário 3: caso sem regra nunca é decidido pela máquina."""
    print("\n" + "=" * 60)
    print("TESTE 3: Uncoded → HUMAN_REVIEW, sempre")
    print("=" * 60)

    ledger = build_rules_v1()
    batch = build_pr_batch_w1()

    r304 = DecisionEngine.decide(batch[3], ledger)
    assert r304.verdict == Verdict.HUMAN_REVIEW
    assert r304.uncoded_findings == ["error-handling-gap"]
    assert r304.violated_rules == []

    r306 = DecisionEngine.decide(batch[5], ledger)
    assert r306.verdict == Verdict.HUMAN_REVIEW
    assert r306.uncoded_findings == ["naming-style"]

    print(f"  PR-304 → {r304.verdict.value} (uncoded: {r304.uncoded_findings})")
    print(f"  PR-306 → {r306.verdict.value} (uncoded: {r306.uncoded_findings})")
    print("  TESTE 3 PASSOU")


def test_4_acumulacao_muda_veredito():
    """Cenário 4: mesmo anti-pattern, ledgers diferentes, vereditos diferentes."""
    print("\n" + "=" * 60)
    print("TESTE 4: Acumulação — o ledger cresce, o motor não muda")
    print("=" * 60)

    v1 = build_rules_v1()
    v2 = build_rules_v2()

    pr_w1 = build_pr_batch_w1()[3]      # error-handling-gap uncoded
    pr_w2 = build_pr_batch_w2()[3]      # mesmo gap, agora cita R-003

    r_v1 = DecisionEngine.decide(pr_w1, v1)
    r_v2 = DecisionEngine.decide(pr_w2, v2)

    assert r_v1.verdict == Verdict.HUMAN_REVIEW
    assert r_v2.verdict == Verdict.BLOCK
    assert r_v2.violated_rules == ["R-003"], (
        "o veredito mudou porque a regra FOI CODIFICADA"
    )
    print(f"  W1 (sem regra):  {r_v1.verdict.value}")
    print(f"  W2 (com R-003):  {r_v2.verdict.value} por {r_v2.violated_rules}")
    print("  TESTE 4 PASSOU")


def test_5_alargamento_gradual():
    """Cenário 5: a taxa de automação cresce acumulando regras."""
    print("\n" + "=" * 60)
    print("TESTE 5: Alargamento — taxa W1 0.5, taxa W2 maior")
    print("=" * 60)

    t1 = run_governance_simulation(build_pr_batch_w1(), build_rules_v1())
    t2 = run_governance_simulation(build_pr_batch_w2(), build_rules_v2())

    assert abs(t1.automation_rate() - 0.5) < 1e-9, (
        f"W1: 3 automáticas em 6, obtido {t1.automation_rate()}"
    )
    assert t2.automation_rate() > t1.automation_rate(), (
        "a automação alarga por acumulação de regras, não por confiança"
    )
    assert "error-handling-gap" in t1.propose_rule_candidates(), (
        "os uncoded de W1 alimentam a fila de candidatas"
    )
    assert all(rep.applied_rules for rep in t1.reports + t2.reports), (
        "invariante de auditoria: nenhum veredito sem regra aplicada"
    )

    print(f"  taxa W1: {t1.automation_rate():.2f}  (3/6 automáticas)")
    print(f"  taxa W2: {t2.automation_rate():.2f}  (4/6 automáticas)")
    print(f"  candidatas de W1: {t1.propose_rule_candidates()}")
    print("  TESTE 5 PASSOU")


def test_6_interface_de_auditoria():
    """Cenário 6: o relatório renderizado cita violadas E aplicadas."""
    print("\n" + "=" * 60)
    print("TESTE 6: Interface Humana — link para todas as regras")
    print("=" * 60)

    ledger = build_rules_v1()
    report = DecisionEngine.decide(build_pr_batch_w1()[0], ledger)
    rendered = render_review_report(report, ledger)

    assert "PR-301" in rendered
    assert "R-001" in rendered and "block" in rendered.lower()
    assert "R-101" in rendered and "R-102" in rendered, (
        "TODAS as regras aplicadas aparecem — auditoria por link"
    )
    assert "INC-2025-091" in rendered, "a proveniência da regra é citável"

    print(rendered)
    print("  TESTE 6 PASSOU")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("EXERCÍCIO 12: SEMANTIC-RULE-GATED AUTO APPROVE/BLOCK")
    print("=" * 60)

    # Quando implementado, descomente para testar:
    # test_1_block_auditavel()
    # test_2_auto_approve_por_regras()
    # test_3_uncoded_e_humano()
    # test_4_acumulacao_muda_veredito()
    # test_5_alargamento_gradual()
    # test_6_interface_de_auditoria()

    print("\nTODO: Implemente as partes acima!")
    print("   1. RuleLedger — regras com proveniência, id imutável")
    print("   2. DecisionEngine.decide() — BLOCK/uncoded/approve, nesta ordem")
    print("   3. Telemetria + simulação + render_review_report()")
    print("   Após implementar, descomente os testes em main()")
```

---

## ✅ Validação: Critérios de Aceitação

Seu código será considerado **APROVADO** quando:

```python
# 1. BLOCK auditável: veredito com regra citada e trilha completa
ledger_v1 = build_rules_v1()
engine = DecisionEngine()
pr_301, pr_302, pr_303, pr_304, pr_305, pr_306 = build_pr_batch_w1()

r = engine.decide(pr_301, ledger_v1)
assert r.verdict == Verdict.BLOCK
assert r.violated_rules == ["R-001"]
assert set(r.applied_rules) == {"R-001", "R-002", "R-101", "R-102"}

# 2. AUTO_APPROVE somente por condições positivas satisfeitas
r303 = engine.decide(pr_303, ledger_v1)
assert r303.verdict == Verdict.AUTO_APPROVE
assert r303.unsatisfied_approve_rules == []
r305 = engine.decide(pr_305, ledger_v1)
assert r305.verdict == Verdict.HUMAN_REVIEW       # R-102 insatisfeita

# 3. Caso uncoded JAMAIS é decidido pela máquina
r304 = engine.decide(pr_304, ledger_v1)
assert r304.verdict == Verdict.HUMAN_REVIEW
assert r304.uncoded_findings == ["error-handling-gap"]

# 4. Acumulação de regra muda o veredito — o motor, não
ledger_v2 = build_rules_v2()
pr_304_w2 = build_pr_batch_w2()[3]
assert engine.decide(pr_304, ledger_v1).verdict == Verdict.HUMAN_REVIEW
assert engine.decide(pr_304_w2, ledger_v2).verdict == Verdict.BLOCK

# 5. A automação alarga com o ledger, não com a confiança
t1 = run_governance_simulation(build_pr_batch_w1(), ledger_v1)
t2 = run_governance_simulation(build_pr_batch_w2(), ledger_v2)
assert abs(t1.automation_rate() - 0.5) < 1e-9
assert t2.automation_rate() > t1.automation_rate()
assert "error-handling-gap" in t1.propose_rule_candidates()

# 6. Auditoria: todo veredito lista as regras aplicadas
assert all(rep.applied_rules for rep in t1.reports + t2.reports)
rendered = render_review_report(r, ledger_v1)
assert "R-001" in rendered and "R-101" in rendered and "R-102" in rendered
```

---

## 📊 Rubric de Avaliação

| Critério | Peso | Insuficiente (0-3) | Básico (4-6) | Proficiente (7-8) | Excelente (9-10) |
|---|---|---|---|---|---|
| **Ledger (Parte 1)** | 15% | Regras sem proveniência | CRUD de regras funciona | Id imutável + ordenação estável | Proveniência como dado de auditoria ("por que esta regra existe") |
| **Motor (Parte 2)** | 35% | Veredito por confiança/score | BLOCK e AUTO funcionam | Ordem correta (BLOCK → uncoded → approve) com uncoded sempre humano | Rationale citando rule_ids; API sem nenhum canal de discrição |
| **Alargamento (Parte 3)** | 25% | Telemetria ausente | Taxa calcula | Simulação de 2 períodos com crescimento estrito | Candidatas extraídas dos uncoded como o mecanismo do crescimento |
| **Interface de auditoria** | 25% | Sem relatório | Veredito + violadas | + Todas as regras aplicadas com statement | + Proveniência citável — o documento que desarma o comitê |

**Nota final:** Média ponderada. **Aprovação:** >= 7.0

---

## 💡 Dicas para Implementação

### Para o ledger

1. **A proveniência não é comentário, é campo.** `"source": "INC-2025-091"` responde a segunda pergunta de qualquer auditoria (por que a regra existe) com a mesma autoridade que o `rule_id` responde a primeira (o que foi violado).
2. **Duplicado rejeita com `ValueError`.** Se `rule_id` puder ser redefinido silenciosamente, a trilha de auditoria deixa de ser reproduzível: uma decisão antiga citando R-003 passaria a significar outra coisa.

### Para o motor

1. **A ordem é a semântica.** BLOCK antes de uncoded antes de approve. Um PR com violação E finding uncoded é BLOCK — a violação codificada já decide; o uncoded é registrado, não consultado.
2. **`approve_inputs` faltante é insatisfeita.** `pr.approve_inputs.get(rid) is True` — ausência de sinal nunca aprova. É o inverso exato da discrição: dúvida vai para humano.
3. **Rationale cita ids, não adjetivos.** "Bloqueado por violar R-001" é auditável; "bloqueado por risco de segurança" é o oráculo do prólogo com outra roupa.

### Para o alargamento

1. **Taxa conta BLOCK como automação.** Decidir bloquear também é decisão automática — o funil que a auditoria mede é "decisões sem humano", nos dois sentidos.
2. **`naming-style` fica uncoded de propósito.** A simulação W2 codifica só `error-handling-gap`. Gradual significa que cada candidatura precisa de justificativa (volume, recorrência) — codificar tudo de uma vez é o big-bang que o padrão rejeita (`...analysis.md:75`).
3. **O teste 4 é a tese do padrão em miniatura.** Mesmo motor, mesma classe de anti-pattern, ledgers diferentes → vereditos diferentes. Se algum dia o veredito mudar sem mudança de ledger, você reintroduziu discrição pela porta dos fundos.

---

## ❓ Dúvidas Comuns

**P: Por que proibir score de confiança se o Pre-Commit AI Review Gate do repo usa tiers de confiança?**
R: Porque os padrões otimizam coisas diferentes. O [[docs/canonical/pre-commit-ai-review-gate|Pre-Commit AI Review Gate]] policya por tiers de confiança do achado ("High: unambiguous violation of a documented rule → Block", `docs/canonical/pre-commit-ai-review-gate.md:79`) — e note que o tier alto já é "violação de regra documentada". Este padrão leva a mesma intuição ao limite: o achado que decide é só o que cita regra; o resto é uncoded → humano. A classificação da fonte é explícita: os gates existentes são "eval-threshold/confidence driven", o que falta é o "expanding set of codified semantic rules accumulated as auditable context" (`...classification.md:115`).

**P: Automação a 100% é o objetivo?**
R: Não — automação *auditável e controlável* é o objetivo. A taxa de automação é consequência do tamanho do ledger, e o ledger cresce pela fila de candidatas com justificativa. O teto natural é a cobertura das regras: "Coverage is limited to codified rules; uncoded cases still need humans" (`...patterns.md:121`) — o residual humano é feature de governança, não dívida.

**P: Isso substitui o Evals-as-Brakes?**
R: Complementa. O [[docs/canonical/evals-as-brakes|Evals-as-Brakes]] governa a *velocidade* pelo freio de evals (o tier auto-merge exige cobertura e correlação, `docs/canonical/evals-as-brakes.md:59-63`); aqui as regras APPROVE *citam* essas condições como critério positivo (a R-102 do exercício é literalmente a cobertura >= 0.9). O que muda é a forma do critério: número no CI vira regra versionada com proveniência no ledger — consultável na trilha de qualquer decisão.

**P: Onde o Exercício 11 entra nisto?**
R: A fonte é explícita: context engine e grafo são pré-requisitos do auto approve/block ("Context-engine and graph maturity (patterns 1-2) as prerequisites", `...patterns.md:111`). Na composição completa, os `CollisionFinding` do [[curriculum/03-nivel-3-advanced-architecture/exercises/exercise-11-software-graph-review-substrate|Exercício 11]] seriam findings que citam uma regra BLOCK de contrato ("mudança quebradora de contrato requer consumidor atualizado no mesmo PR") — o grafo detecta, o ledger decide.

**P: `run_governance_simulation` parece trivial (um loop). Por que existe?**
R: Porque isola a superfície de composição: é a única função que o CI consumiria (batch + ledger → telemetria). Quando o Exercício 7 (shadow) entra na composição — regras novas começam advisory, graduam para blocking — é neste loop que o período de shadow se insere, sem tocar no motor.

---

## 🚀 Próximo Passo

Depois de completar este exercício:

1. Leia o padrão 5 completo e sua classificação em `docs/analysis/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co-patterns.md:105-123` e `...classification.md:102-117` — e o canônico [[docs/canonical/semantic-rule-gated-auto-approve-block|Semantic-Rule-Gated Auto Approve/Block]]
2. Compare com [[docs/canonical/evals-as-brakes|Evals-as-Brakes]] e [[docs/canonical/shadow-review-pipeline|Shadow Review Pipeline]]: threshold de eval, graduação por concordância e regra semântica acumulada são três substratos de decisão distintos — desenhe qual seria o order de adoção num time do zero
3. Volte ao [[curriculum/03-nivel-3-advanced-architecture/exercises/exercise-11-software-graph-review-substrate|Exercício 11]] e conecte: escreva a regra BLOCK que consome `CollisionFinding` ("colisão cross-PR no mesmo campo de contrato bloqueia até coordenação") e rode o motor sobre os reports do grafo — o pipeline completo da fonte, ponta a ponta

---

*Exercício 12 | Nível 3 — Arquitetura Avançada | Semantic-Rule-Gated Auto Approve/Block*

**Se o veredito não cita uma regra, não é uma decisão — é uma opinião.**
