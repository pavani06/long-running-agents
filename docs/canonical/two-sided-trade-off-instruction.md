---
title: "Two-Sided Trade-off Instruction"
type: canonical
status: accepted
date: 2026-09-02
tags: ["context-engineering", "agentes-orquestracao", "evals", "harness-engineering"]
aliases: ["two-sided instruction", "balanced trade-off instruction", "instrucao de trade-off dois lados", "counter-cost instruction"]
last_updated: 2026-09-02
relates-to: ["[[docs/canonical/generator-evaluator|Generator-Evaluator]]", "[[docs/canonical/structural-guarantee-over-compliance|Structural Guarantee over Compliance]]", "[[docs/canonical/control-edge-boundary-eval-taxonomy|Control/Edge/Boundary Eval Taxonomy]]", "[[docs/canonical/defensive-patch-ledger|Defensive Patch Ledger]]", "[[docs/canonical/tested-degradation-ladder|Tested Degradation Ladder]]", "[[curriculum/05-core-concepts/08-evaluation-rubrics|Evaluation Rubrics]]"]
sources: ["[[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-patterns|The Prompting Playbook Patterns]]", "[[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-classification|The Prompting Playbook Classification]]"]
---

# Two-Sided Trade-off Instruction

**Type:** Canonical Pattern
**Status:** Accepted
**Source:** [[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-patterns|The Prompting Playbook Patterns]] (padrão 5)
**Classification:** Missing (P0, Medium integration value)
**Precedence:** Level 2 ([[docs/system-of-record|System of Record]])

---

## Problema

Instruções que declaram apenas **um lado** da economia de uma ação produzem overfit de objetivo único. O exemplo canônico: o prompt diz "escalation custa $8" e nada mais; o modelo otimiza o único objetivo declarado e **nunca escala**, mesmo quando escalar é o correto. O under-escalation resultante não é falha de capability, é falha de desenho de instrução: o modelo faz exatamente o que a instrução incompleta manda.

O problema tem duas faces:

1. **Single-objective overfit**: só o custo da ação é declarado; o counter-cost de evitá-la erroneamente (exposição a refund, confiança do cliente) fica implícito e invisível.
2. **Prompt-vs-eval conflict**: quando a eval suite espera escalation no caso certo mas o prompt só declara o custo, os dois artefatos descrevem o comportamento desejado de forma inconsistente, e o modelo fica preso entre eles.

## Solução

Instruções balanceadas que declaram **os dois lados do trade-off** e delegam o julgamento por caso ao modelo:

**Inputs:**

1. A ação cuja frequência o prompt deve controlar (escalate, refund, hand off).
2. O lado custo da ação (dinheiro, métricas do time).
3. O counter-cost de evitá-la erroneamente (exposição a refund, confiança do cliente).
4. O comportamento que a eval suite espera.

**Output:** uma instrução balanceada declarando os dois lados, permitindo ao modelo exercer o julgamento por caso.

**Mecanismo:**

1. **Declarar os dois lados na mesma instrução**: "escalation custa $8; não escalar um caso que precisava de humano custa em média $40 de refund e derruba confiança". O modelo passa a ter a economia completa que o julgamento por caso exige.
2. **Alinhar com a eval**: a rubrica que julga escalation precisa codificar o mesmo balanceamento; instrução e rubrica descrevem o comportamento correto de forma consistente. Isso resolve o prompt-vs-eval conflict pela raiz: ambos os lados existem nos dois artefatos.
3. **Converter regra dura em julgamento**: o padrão troca determinismo por julgamento informado. É a escolha certa quando os casos variam (não há regra única correta) e o modelo é bom o suficiente em trade-offs; à medida que modelos melhoram, declarar os dois lados deixa eles exercerem essa capacidade.

**Distinção importante**: este padrão é instructional, não arquitetural. Quando o comportamento correto é determinístico (sempre/nunca), a garantia deve viver em estrutura, não em instrução, por [[docs/canonical/structural-guarantee-over-compliance|Structural Guarantee over Compliance]]. O two-sided instruction aplica-se exatamente à faixa em que não há resposta estrutural: os casos que exigem julgamento.

## Implementação neste repositório

### O que já existe

Nada, em nenhuma forma. A cobertura de escalation do repo é arquitetural, nunca instructional ([[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-classification|The Prompting Playbook Classification]]:95):

- Adjacentes pesquisados e rejeitados como não-equivalentes: [[docs/canonical/tested-degradation-ladder|Tested Degradation Ladder]] (`:29`, escalation como rung de falha runtime, não economia de instrução); [[docs/canonical/closed-loop-help-api|Closed-Loop Help API]] (`:30-32`, fechamento de loop de escalation terminal); [[docs/canonical/human-afk-task-routing-gate|Human/AFK Task Routing Gate]] (`:37`, roteamento de julgamento para humanos por tipo de tarefa).

### O que falta

1. **O princípio de desenho**: nenhum documento ensina a declarar custo e counter-cost da mesma ação no prompt para o modelo exercer julgamento por caso. NOT_FOUND: grep repo-wide `cost of escalat|counter-cost|cost of not escalat|stating both sides|balanced instruction` casa apenas os arquivos desta análise ([[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-classification|The Prompting Playbook Classification]]:98).
2. **O tratamento de single-objective overfit** (under-escalation por instrução de um lado só) como classe de falha. NOT_FOUND: grep `trade-off|tradeoff|both sides|under-escalat|over-optimiz` em `docs/canonical/` (30 hits em 23 arquivos) são todos trade-offs arquiteturais ou de design (ex. `docs/canonical/task-routed-model-tiering.md:40`), nenhum sobre desenho de instrução ([[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-classification|The Prompting Playbook Classification]]:99).
3. **Encaixe curricular**: princípio compacto para Level 2 (desenho de prompt/rubric, [[curriculum/05-core-concepts/08-evaluation-rubrics|Evaluation Rubrics]]) e Level 4 (journeys de escalation do KODA), sem dependência de infraestrutura.

## Tradeoffs

| Benefício | Custo |
|---|---|
| Elimina single-objective overfit como under-escalation | Exige conhecer os dois lados bem o suficiente para declará-los |
| Modelos melhores em trade-offs exercem o julgamento que a instrução completa habilita | Converte regra dura em julgamento; comportamento fica menos determinístico |
| Prompt e eval descrevem o comportamento desejado de forma consistente quando ambos carregam os dois lados | O framing precisa permanecer alinhado com o que a eval define como correto |
| Princípio compacto, sem dependência de infraestrutura | Só se aplica onde julgamento é a resposta; comportamento determinístico pertence à estrutura |

## Relação com outros padrões

- **Contraponto de:** [[docs/canonical/structural-guarantee-over-compliance|Structural Guarantee over Compliance]]: garantias determinísticas migram para estrutura; o two-sided instruction cobre a faixa restante onde o correto varia por caso e só o julgamento informado decide.
- **Codificado pela rubrica de:** [[docs/canonical/generator-evaluator|Generator-Evaluator]] e [[curriculum/05-core-concepts/08-evaluation-rubrics|Evaluation Rubrics]]: o Evaluator só aprova escalation balanceada se a rubrica codificar os dois lados que a instrução declara.
- **Verificado pelos boundary cases de:** [[docs/canonical/control-edge-boundary-eval-taxonomy|Control/Edge/Boundary Eval Taxonomy]]: boundary cases testam handoff/refusal; a instrução two-sided define o comportamento correto que eles verificam.
- **Envelhece sob:** [[docs/canonical/defensive-patch-ledger|Defensive Patch Ledger]]: instruções de um lado só são patches defensivos que depreciam; o ledger registra o porquê e o audit decide o rebalanceamento.
- **Distinto de:** [[docs/canonical/tested-degradation-ladder|Tested Degradation Ladder]] (runtime failure rungs) e [[docs/canonical/capability-escalation-ladder|Capability Escalation Ladder]] (alavancas de investimento): este padrão governa o desenho da instrução de decisão, não o mecanismo de escalada.

## Referências

- `docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-patterns.md:92-110` (seção 5): definição do padrão, inputs, outputs, benefícios, limitações.
- `docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-classification.md:91-102` (seção 5): Missing, NOT_FOUND com localizações, adjacentes rejeitados.
- `docs/canonical/tested-degradation-ladder.md:29`, `docs/canonical/closed-loop-help-api.md:30-32`, `docs/canonical/human-afk-task-routing-gate.md:37`: adjacentes arquiteturais não-equivalentes.
- `docs/canonical/task-routed-model-tiering.md:40`: exemplo de trade-off arquitetural (não instructional) retornado pelo grep.

---

*Created: 2026-09-02 | From: The Prompting Playbook classification (Batch 1, pattern 5) | Precedence: canonical*
