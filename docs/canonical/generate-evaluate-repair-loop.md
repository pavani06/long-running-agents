---
title: "Generate-Evaluate-Repair Loop"
type: canonical
status: accepted
date: 2026-09-02
tags: ["evals", "agentes-orquestracao", "harness-engineering", "error-handling"]
aliases: ["generate evaluate repair", "loop gerar avaliar reparar", "three prompt decomposition", "repair loop economics"]
last_updated: 2026-09-02
relates-to: ["[[docs/canonical/generator-evaluator|Generator-Evaluator]]", "[[docs/canonical/structured-generation-constraint-validation-circuit|Structured Generation and Constraint Validation Circuit]]", "[[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]", "[[docs/canonical/token-economics-gap-filling|Token Economics Gap Filling]]", "[[docs/canonical/plan-execute-verify|Plan-Execute-Verify]]", "[[docs/canonical/tested-degradation-ladder|Tested Degradation Ladder]]"]
sources: ["[[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-patterns|The Prompting Playbook Patterns]]", "[[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-classification|The Prompting Playbook Classification]]"]
---

# Generate-Evaluate-Repair Loop

**Type:** Canonical Pattern
**Status:** accepted
**Source:** [[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-patterns|The Prompting Playbook Patterns]] (padrão 10)
**Classification:** Partial Coverage / Medium ([[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-classification|The Prompting Playbook Classification]]:190, :261)
**Precedence:** Level 2 ([[docs/system-of-record|System of Record]])

---

## Problema

Um mega-prompt único que gera, verifica e corrige no mesmo contexto queima tokens e não termina dentro do output limit; e soft requirements congeladas em código resistem a mudança ([[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-patterns|The Prompting Playbook Patterns]]:195). As rotas intuitivas de conserto — modelo maior (upsizing) ou output limit maior — passam os casos destruindo a economia de tokens e latência.

## Solução

Decompor em **três prompts simples e independentes**, com o loop fechado por violações estruturadas ([[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-patterns|The Prompting Playbook Patterns]]:197-202):

1. **Generator** — produz o primeiro draft da tarefa.
2. **Evaluator** — checa cada regra com evidência citada de cada violação; soft constraints injetadas no prompt do evaluator em runtime (ajustar preferência é editar texto, não deploy de backend).
3. **Repairer** — aplica fixes direcionados a partir das violações reportadas.

```text
Task spec (hard + soft constraints)
        |
        v
   GENERATOR  ──draft──►  EVALUATOR
                          (cada regra, evidência por violação;
                           soft constraints injetadas em runtime)
                              |
                    approve ──┼── reject + violation report
                       |            |
                       v            v
                   artifact     REPAIRER
                                (fixes direcionados)
                                  |
                                  └──► draft corrigido ──► EVALUATOR
```

Dois elementos carregam o valor do padrão:

- **Economia como critério de decisão**: no caso-fonte, o loop passou todos os casos com menos tokens e latência menores que as rotas de bigger-model e bigger-limit ([[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-patterns|The Prompting Playbook Patterns]]:201, :204). Passar o eval não basta; a rota vencedora é a que passa no menor custo.
- **Cada prompt permanece simples** — independente e isoladamente maintainable e testable; três prompts simples no lugar de um mega-prompt ([[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-patterns|The Prompting Playbook Patterns]]:206).

O loop admite otimização e é limitado pela qualidade do Repairer; casos patológicos podem exigir mais iterações ([[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-patterns|The Prompting Playbook Patterns]]:208, :210) — por isso o loop precisa ser bounded.

## Implementação neste repositório

### O que já existe

O loop existe em profundidade canônica e curricular:

- [[docs/canonical/generator-evaluator|Generator-Evaluator]]:31 — dois agentes; o Evaluator devolve veredito approve/reject com feedback específico; `:70-72` — output rejeitado "volta para GENERATOR com feedback"; `:116` — "Rejection loops add latency if Generator needs multiple revisions".
- A lição de N2 operacionaliza o loop com feedback estruturado — `severity`, `issue_code`, `issue_text`, `affected_item`, `fix_instruction` ("Exatamente o que o Generator precisa fazer") — e loop bounded com `max_iterations: 3` e `action_if_max: "escalate_to_human"` ([[curriculum/02-nivel-2-practical-patterns/01-generator-evaluator-pattern|Generator-Evaluator Pattern]]:752-767, :712-722).
- A orquestração KODA de N3 chama literalmente `generator_agent.repair_recommendation(draft, evaluation)` — repair direcionado pela avaliação ([[curriculum/03-nivel-3-advanced-architecture/koda-applications/nivel-3-koda|Nível 3 KODA]]:383-396).
- [[docs/canonical/structured-generation-constraint-validation-circuit|Structured Generation and Constraint Validation Circuit]]:29 — geração, validação, repair/rejection, risk flags e audit como um único caminho.
- Evidência por avaliação: [[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]:33 (violation detail por linha de constraint) e [[curriculum/05-core-concepts/08-evaluation-rubrics|Evaluation Rubrics]]:1218 (trace registra "evidence citada, hard rule aplicada").

### O que falta

(Classificação:192, :203 — NOT_FOUND com locais pesquisados.)

1. **A decomposição em três prompts** — no repo, quem repara é o próprio Generator sob feedback (mesma capacidade, decomposição diferente); o variant com repairer independente como opção de maintainability não está formalizado.
2. **A comparação econômica que motiva o loop** — loop vs. model-upsizing vs. output-limit-inflating em tokens e latência. O repo cobre outro trade-off: [[docs/canonical/token-economics-gap-filling|Token Economics Gap Filling]] (custo de inferência vs. custo de especificação), não decomposição vs. upsizing.
3. **Soft constraints injetadas no prompt do evaluator em runtime** — mesmo NOT_FOUND do padrão 7 ([[docs/canonical/hard-soft-constraint-grader-split|Hard/Soft Constraint Grader Split]]).

## Tradeoffs

| Benefício | Custo |
|---|---|
| Passa os casos com menos tokens e latência que bigger-model e bigger-limit | Três prompts para manter em vez de um; o loop ainda admite otimização |
| Soft constraints runtime-adjustables no evaluator, sem mudança de backend | O evaluator é LLM: custo e não-determinismo nos julgamentos soft |
| Cada prompt simples, independente, maintainable e testable | A qualidade do Repairer limita o loop; casos patológicos podem precisar de mais iterações |
| Violation report estruturado com evidência por regra | Latência adicional por iteração de rejeição (generator-evaluator:116) |

## Relação com outros padrões

- **Generaliza:** [[docs/canonical/generator-evaluator|Generator-Evaluator]] — mesmo loop generate→evaluate→reject-with-feedback; este padrão adiciona o repairer independente e o critério econômico.
- **Componível com:** [[docs/canonical/structured-generation-constraint-validation-circuit|Structured Generation and Constraint Validation Circuit]] — o circuito é a versão single-path (geração, validação, repair/rejection, audit); o loop é a versão multi-prompt.
- **Depende de:** [[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]] — a evidência por violação que alimenta o repair.
- **Argumento econômico para:** [[docs/canonical/plan-execute-verify|Plan-Execute-Verify]] e o currículo de decomposition — decomposição vence upsizing; contrasta com [[docs/canonical/token-economics-gap-filling|Token Economics Gap Filling]] (outro eixo de economia de tokens).
- **Adjacente a:** [[docs/canonical/tested-degradation-ladder|Tested Degradation Ladder]]:42 — "Retry with repair" é o degrau de recuperação de falha em runtime; este padrão é o loop de qualidade do artifact.

## Referências

- [[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-patterns|The Prompting Playbook Patterns]]:192-210 — definição do padrão 10 (inputs, outputs, benefícios, limitações).
- [[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-classification|The Prompting Playbook Classification]]:188-205 — Partial Coverage/Medium com evidência file:line e NOT_FOUND.
- [[docs/canonical/generator-evaluator|Generator-Evaluator]]:31, :70-72, :115-116 — veredito com feedback, loop de rejeição, trade-off de latência.
- [[curriculum/02-nivel-2-practical-patterns/01-generator-evaluator-pattern|Generator-Evaluator Pattern]]:712-722, :752-767 — `max_iterations`, `escalate_to_human`, feedback estruturado com `fix_instruction`.
- [[curriculum/03-nivel-3-advanced-architecture/koda-applications/nivel-3-koda|Nível 3 KODA]]:383-396 — `repair_recommendation(draft, evaluation)` na orquestração.
- [[docs/canonical/structured-generation-constraint-validation-circuit|Structured Generation and Constraint Validation Circuit]]:29 — geração + validação + repair/rejection + audit.
- [[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]:33 — violation detail por constraint.
- [[docs/canonical/token-economics-gap-filling|Token Economics Gap Filling]] — trade-off adjacente (inferência vs. especificação), não decomposição vs. upsizing.

---

*Criado: 2026-09-02 | De: The Prompting Playbook classification | Precedência: canonical*
