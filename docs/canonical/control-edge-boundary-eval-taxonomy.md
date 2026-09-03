---
title: "Control/Edge/Boundary Eval Taxonomy"
type: canonical
status: accepted
date: 2026-09-02
tags: ["evals", "agentes-orquestracao", "production", "harness-engineering"]
aliases: ["control edge boundary taxonomy", "case class taxonomy", "boundary case evals", "taxonomia control edge boundary"]
last_updated: 2026-09-02
relates-to: ["[[docs/canonical/living-eval-dataset|Living Eval Dataset]]", "[[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]]", "[[docs/canonical/workflow-derived-golden-question-set|Workflow-Derived Golden Question Set]]", "[[docs/canonical/3-layer-evaluation-architecture|3-Layer Evaluation Architecture]]", "[[docs/canonical/eval-tier-stratification|Eval Tier Stratification]]", "[[docs/canonical/eval-coverage-matrix|Eval Coverage Matrix]]", "[[docs/canonical/human-afk-task-routing-gate|Human/AFK Task Routing Gate]]", "[[docs/canonical/two-sided-trade-off-instruction|Two-Sided Trade-off Instruction]]"]
sources: ["[[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-patterns|The Prompting Playbook Patterns]]", "[[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-classification|The Prompting Playbook Classification]]"]
---

# Control/Edge/Boundary Eval Taxonomy

**Type:** Canonical Pattern
**Status:** Accepted
**Source:** [[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-patterns|The Prompting Playbook Patterns]] (padrão 2)
**Classification:** Partial Coverage (P2, Medium integration value)
**Precedence:** Level 2 ([[docs/system-of-record|System of Record]])

---

## Problema

Eval suites ad hoc não cobrem sistematicamente o que um agente de produção deve preservar: comportamento baseline inequívoco, modos de falha do passado travados por instrução, e a fronteira da própria competência. O problema é que **o significado de uma regressão depende da classe do caso**, mas suites tratam todos os casos iguais: falhar um caso trivialmente must-pass é quebra; falhar um caso de fronteira é perda de calibração. Sem a distinção, o relatório de regressão mistura severidades incomparáveis.

## Solução

Classificar todo caso de eval em três classes, cada uma com semântica de regressão própria:

| Classe | O que testa | Semântica de regressão |
|---|---|---|
| **Control** | Comportamento baseline inequívoco que deve sempre passar | Regressão = breakage: o agente parou de fazer o básico |
| **Edge** | Falhas passadas travadas como testes permanentes por instrução | Regressão = recidiva: uma falha já corrigida voltou |
| **Boundary** | Se o agente sabe quando escalar para humano ou recusar | Regressão = calibration loss: o agente perde a noção do próprio limite |

**Inputs:** o domínio de tarefa do agente e as falhas passadas conhecidas; a política, as ferramentas e os critérios de handoff/refusal.

**Outputs:** uma suite de três classes em que cada caso carrega sua classe como metadado; a classe dirige triagem de regressão (breakage vs. recidiva vs. calibration loss) e prioridade de fix.

Mecanismos específicos:

1. **Control cases**: perguntas inequívocas extraídas do workflow real, com baseline registrado e score gateando o lançamento (o análogo existente é o golden question set).
2. **Edge cases**: cada falha de produção vira adição permanente à suite, codificando memória institucional (o flywheel já faz isso).
3. **Boundary cases**: casos que exercitam o agente no limiar da própria competência, onde a resposta correta é handoff ou refusal, não a resposta da tarefa. Exigem especificar corretamente quando handoff/refusal é o comportamento certo.

## Implementação neste repositório

### O que já existe

Duas das três classes têm análogos canônicos profundos:

- **Classe edge**: [[docs/canonical/living-eval-dataset|Living Eval Dataset]]: "every production incident, every escaped edge case, every new feature specification becomes a permanent addition" (`docs/canonical/living-eval-dataset.md:28`); [[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]]: intake explícito de escaped edge case convertido em regression case durável (`docs/canonical/production-failure-regression-flywheel.md:32`).
- **Classe control (análogo)**: [[docs/canonical/workflow-derived-golden-question-set|Workflow-Derived Golden Question Set]]: golden questions autoradas do workflow real, acurácia de primeira execução registrada como baseline, lançamento gateado por score (`docs/canonical/workflow-derived-golden-question-set.md:44-47`).

### O que falta

1. **A classe boundary**: casos de eval testando se o agente sabe quando handoff para humano ou recusa, isto é, calibração da própria aresta de competência. As fontes de critério existem espalhadas ([[docs/canonical/human-afk-task-routing-gate|Human/AFK Task Routing Gate]] roteia por tipo de tarefa; o curriculum de rubricas trata escalation), mas nenhuma vira eval class.
2. **A taxonomia em si** como classificação de caso com semântica de regressão por classe. NOT_FOUND: grep `control case|edge case|boundary case|capability boundary|knows when to (refuse|hand off|escalate)` em `docs/canonical/` retorna 26 hits em 15 arquivos, todos usos incidentais de "edge case" (ex. `docs/canonical/pain-signal-eval-progression-gate.md:48`); nenhum define a taxonomia testa calibração de handoff/refusal como classe de eval ([[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-classification|The Prompting Playbook Classification]]:51).
3. **O eixo case-class como quarta lente de estratificação**: as estratificações existentes são todas de eixo único: por tipo de mecanismo (`docs/canonical/3-layer-evaluation-architecture.md:28`), por velocidade/trigger (`docs/canonical/eval-tier-stratification.md:32-36`), confirmado por [[docs/canonical/eval-coverage-matrix|Eval Coverage Matrix]] (`docs/canonical/eval-coverage-matrix.md:66-68`).

## Tradeoffs

| Benefício | Custo |
|---|---|
| Significado de regressão vira específico por classe: control = breakage; edge = recidiva; boundary = calibration loss | Exige curadoria deliberada para mapear casos nas três classes |
| Codifica memória institucional de falhas passadas como testes permanentes | Cada nova falha de produção cresce o conjunto edge; a suite precisa manutenção |
| Testa o self-knowledge dos limites do agente, não só skill de tarefa | Boundary cases dependem de especificar corretamente quando handoff ou refusal é o certo |
| Complementa as três lentes existentes de eval com um quarto eixo (classe de caso) | Mais um eixo de metadado para manter consistente em todo caso da suite |

## Relação com outros padrões

- **Materializa a classe edge com:** [[docs/canonical/living-eval-dataset|Living Eval Dataset]] e [[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]] (intake e permanência já existem; a taxonomia só rotula).
- **Materializa a classe control com:** [[docs/canonical/workflow-derived-golden-question-set|Workflow-Derived Golden Question Set]] (baseline e gate já existem).
- **Complementa:** [[docs/canonical/3-layer-evaluation-architecture|3-Layer Evaluation Architecture]] (eixo mecanismo), [[docs/canonical/eval-tier-stratification|Eval Tier Stratification]] (eixo velocidade/trigger) e [[docs/canonical/eval-coverage-matrix|Eval Coverage Matrix]] (eixo determinismo × deployment): a case-class é o quarto eixo de estratificação.
- **Consome critérios de:** [[docs/canonical/human-afk-task-routing-gate|Human/AFK Task Routing Gate]] e de [[docs/canonical/two-sided-trade-off-instruction|Two-Sided Trade-off Instruction]]: os critérios de handoff/refusal e o desenho da instrução de escalation definem o comportamento correto que os boundary cases verificam.
- **Limita:** [[docs/canonical/eval-gated-model-migration-diagnostic|Eval-Gated Model Migration Diagnostic]]: o diagnóstico de migração é só tão representativo quanto a taxonomia de casos da suite.

## Referências

- `docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-patterns.md:36-52` (seção 2): definição do padrão, três classes, benefícios, limitações.
- `docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-classification.md:40-53` (seção 2): Partial Coverage, evidência file:line e NOT_FOUND.
- `docs/canonical/living-eval-dataset.md:28`: cada incidente vira adição permanente.
- `docs/canonical/production-failure-regression-flywheel.md:32`: intake de escaped edge case.
- `docs/canonical/workflow-derived-golden-question-set.md:44-47`: golden questions com baseline e gate.
- `docs/canonical/eval-coverage-matrix.md:66-68`: estratificações existentes são de eixo único.

---

*Created: 2026-09-02 | From: The Prompting Playbook classification (Batch 1, pattern 2) | Precedence: canonical*
