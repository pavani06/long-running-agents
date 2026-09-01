---
title: "Structured Partial Checks over Exact Goldens"
type: canonical
aliases: ["partial checks vs goldens", "strictez casada com estabilidade", "assertions on what matters"]
tags: ["evals"]
last_updated: 2026-08-31
relates-to: ["[[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]", "[[docs/canonical/behavioral-eval-path-analysis|Behavioral Eval Path Analysis]]", "[[docs/canonical/3-layer-evaluation-architecture|3-Layer Evaluation Architecture]]", "[[docs/canonical/magnitude-direction-verifier-split|Magnitude-Direction Verifier Split]]", "[[docs/canonical/workflow-derived-golden-question-set|Workflow-Derived Golden Question Set]]", "[[docs/canonical/living-eval-dataset|Living Eval Dataset]]", "[[docs/canonical/evals-as-brakes|Evals as Brakes]]"]
sources: ["[[docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-patterns|Clay Eval Stack Patterns]]"]
---
# Structured Partial Checks over Exact Goldens

**Type:** canonical
**Status:** active
**Source:** Inside Clay's Eval Stack (LangChain) — `docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/`
**Classification:** Partial Coverage — Integration value: Medium (P2)
**Precedence:** document-level 2 (canonical) per `docs/system-of-record.md`

---

## Problem

Goldens de output exato quebram em reordenação irrelevante — ordem de keywords, ordem de nós, formatação — e o eval vira ruído. A consequência não é apenas falso-positivo chato: é a **morte por desatenção**. Suites ruidosas "just end up getting ignored" — o time aprende que vermelho não significa nada, e o sinal que importava morre junto com o ruído.

O problema de fundo é casar a **estrictez do check** com a **estabilidade do output**: superfícies instáveis (texto livre, listas reordenáveis) exigem asserções parciais sobre as partes que importam; superfícies estáveis (query language, schemas fechados) toleram goldens exatos. Aplicar golden exato na superfície errada gera eval ruidoso; aplicar check parcial frouxo demais gera falso-verde.

## Solution

Regra de alocação: a estrictez do mecanismo de verificação é função da estabilidade da superfície de output.

1. **Asserções parciais estruturadas** — verificar apenas o subconjunto do output que importa para a query: campos obrigatórios presentes, valores-chave corretos, invariantes de schema. O resto do output é explicitamente ignorado.
2. **Asserções de trajetória/tool calls** — verificar o que o agente *fez*, não só o texto final: "pergunta de preço exige leitura da tabela de preços" é uma asserção sobre o caminho de execução, imune à redação do output.
3. **Goldens exatos retidos só para superfícies simples e estáveis** — query languages e contratos fechados, onde o output correto é único e a reordenação é ela mesma um bug.
4. **Manutenção anti-ruído** — reformular ou aposentar checks que disparam sobre reordenação irrelevante ("retire or relax checks that fire on irrelevant reordering"); a confiança da suite é o ativo a proteger.

## Implementation in this repo

### What already exists

Os três componentes mecânicos existem, cada um profundo em doc canônico próprio:

- **Asserções parciais:** a verification matrix do [[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]] checa só as constraints explícitas — `constraint -> check -> pass/fail -> violation detail` (`docs/canonical/constraint-anchored-evaluation.md:31-33`), com contraste explícito contra avaliação subjetiva de output completo (`:52-59`).
- **Asserções de trajetória:** os expected execution path templates do [[docs/canonical/behavioral-eval-path-analysis|Behavioral Eval Path Analysis]] — "Define an expected execution path template per query category... Compare the actual execution path against the template" (`docs/canonical/behavioral-eval-path-analysis.md:76-83`), mantidos junto aos golden answers (`:83`).
- **Asserções estruturais de schema/formato:** Layer 1 do [[docs/canonical/3-layer-evaluation-architecture|3-Layer Evaluation Architecture]] (`docs/canonical/3-layer-evaluation-architecture.md:36-39`).
- **Verificação graduada:** [[docs/canonical/magnitude-direction-verifier-split|Magnitude-Direction Verifier Split]] verifica direção sobre magnitude exata (`docs/canonical/magnitude-direction-verifier-split.md:100`) — mesma família de "não exigir o valor exato".
- **Goldens:** [[docs/canonical/workflow-derived-golden-question-set|Workflow-Derived Golden Question Set]] (~150 perguntas para superfície restrita pré-launch, `:44-47`) e [[docs/canonical/living-eval-dataset|Living Eval Dataset]].

### What is missing

O **reframe** — a regra de decisão que os compõe:

1. Nenhum doc formula o trade goldens-exatos-vs-checks-parciais como problema de **ruído e confiança da suite** (NOT_FOUND: grep `golden` nos 10 docs canônicos que citam; leitura dos 5 principais).
2. A regra "retire or relax checks that fire on irrelevant reordering" não aparece em lugar nenhum.
3. O repo pende para o lado oposto: golden answers humanas como mecanismo geral (`docs/canonical/business-outcome-first-eval-pipeline.md:28`, via `workflow-derived-golden-question-set.md:64`), **sem a restrição de goldens a superfícies estáveis**.

Add:

1. Classificação de superfícies de output por estabilidade (estável → golden exato; instável → checks parciais + trajetória).
2. Política de manutenção: check ruidoso é bug da suite, não do agente; aposentar ou relaxar.
3. Metadado por caso indicando o mecanismo de verificação e a razão da escolha.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Estrictez casada com estabilidade mantém a suite confiada e viva | Escolher "o que importa" é juízo de valor que pode esconder regressões nas partes ignoradas |
| Asserções de trajetória testam o que o agente fez, não só o texto final | Checks parciais não certificam correção do output completo |
| Menos falsas falhas → devs param de ignorar a suite | Exige output estruturado para assertar; superfícies free-text resistem |
| Goldens exatos onde são fortes (query language) ficam baratos e inequívocos | Manutenção contínua: a fronteira estável/instável muda conforme o produto evolui |

## Relationship to Other Patterns

- **Composed of:** [[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]] (asserções parciais), [[docs/canonical/behavioral-eval-path-analysis|Behavioral Eval Path Analysis]] (asserções de trajetória) e [[docs/canonical/workflow-derived-golden-question-set|Workflow-Derived Golden Question Set]] / [[docs/canonical/living-eval-dataset|Living Eval Dataset]] (goldens) — este doc é a regra de alocação entre eles.
- **Layer of:** [[docs/canonical/3-layer-evaluation-architecture|3-Layer Evaluation Architecture]] — a regra opera dentro das Layers 1 e 3.
- **Same family:** [[docs/canonical/magnitude-direction-verifier-split|Magnitude-Direction Verifier Split]] — verificação graduada como forma de não exigir o valor exato.
- **Protects:** [[docs/canonical/evals-as-brakes|Evals as Brakes]] — freio só funciona enquanto a suite é confiada; ruído de golden exato corrói a confiança que o gate pressupõe.

## References

- `docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-patterns.md:121` — definição original do padrão.
- `docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-classification.md` — §6, classificação Partial Coverage/Medium com evidência.
- `docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-classification-batch-1.md` — batch-fonte da classificação.
- `docs/canonical/constraint-anchored-evaluation.md:31-33,52-59` — verification matrix.
- `docs/canonical/behavioral-eval-path-analysis.md:76-83` — expected execution path templates.
- `docs/canonical/3-layer-evaluation-architecture.md:36-39` — Layer 1 structured assertions.
- `docs/canonical/magnitude-direction-verifier-split.md:100` — verificação graduada.
- `docs/canonical/workflow-derived-golden-question-set.md:44-47` — golden set para superfície restrita.

---

*Created: 2026-08-31 | From: Clay Eval Stack classification | Precedence: canonical*
