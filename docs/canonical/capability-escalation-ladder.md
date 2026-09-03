---
title: "Capability Escalation Ladder"
type: canonical
status: accepted
date: 2026-09-02
tags: ["harness-engineering", "agentes-orquestracao", "evals", "production"]
aliases: ["capability escalation ladder", "escalation ladder de alavancas", "model upsizing vs decomposition", "economic winner analysis"]
last_updated: 2026-09-02
relates-to: ["[[docs/canonical/task-routed-model-tiering|Task-Routed Model Tiering]]", "[[docs/canonical/generator-evaluator|Generator-Evaluator]]", "[[docs/canonical/plan-execute-verify|Plan-Execute-Verify]]", "[[docs/canonical/model-agnostic-agent-vm-harness|Model-Agnostic Agent-VM Harness]]", "[[docs/canonical/eval-gated-model-migration-diagnostic|Eval-Gated Model Migration Diagnostic]]", "[[docs/canonical/two-sided-trade-off-instruction|Two-Sided Trade-off Instruction]]", "[[docs/canonical/structural-prompt-hygiene|Structural Prompt Hygiene]]", "[[docs/canonical/token-economics-gap-filling|Token Economics Gap Filling]]"]
sources: ["[[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-patterns|The Prompting Playbook Patterns]]", "[[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-classification|The Prompting Playbook Classification]]"]
---

# Capability Escalation Ladder

**Type:** Canonical Pattern
**Status:** Accepted
**Source:** [[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-patterns|The Prompting Playbook Patterns]] (padrão 6)
**Classification:** Missing (P0, High integration value)
**Precedence:** Level 2 ([[docs/system-of-record|System of Record]])

---

## Problema

Quando um agente falha uma tarefa difícil, o time adivinha qual alavanca puxar: bigger model, more thinking, better prompt ou decomposition. A ordenação ad hoc desperdiça spend e esconde o vencedor econômico. O modo de falha mais caro: uma rota passa nos evals mas falha na economia (o triplo de tokens e latência), e sem comparação de custo/latency entre rotas que passam, o time shipa a primeira que funcionou.

Os dois ladders existentes no repo são padrões diferentes: o tested degradation ladder ordena handling de falha runtime (retry, fallback, escalation humana), e o agent-value maturity ladder é um modelo de maturidade organizacional. Nenhum ordena alavancas de investimento de capability para uma tarefa que falha ([[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-classification|The Prompting Playbook Classification]]:110).

## Solução

Uma exploração ordenada de quatro rungs de escalada, com custo e latência medidos por rung e comparação entre as rotas que passam:

```
[Tarefa falhando no eval, com violation counts]
        |
        v
1. Capability: larger model          (trocar o modelo por um maior)
        |
        v
2. Reasoning budget: adaptive thinking (mais orçamento de raciocínio no mesmo modelo)
        |
        v
3. Instruction: improved instructions (melhor prompt; higiene, fixes dirigidos)
        |
        v
4. Architecture: decomposition        (generator-evaluator, plan-execute-verify, repair loops)
        |
        v
[Comparar custo/latência entre as rotas que passam]
        |
        v
[Vencedor econômico: tipicamente o último rung]
```

**Inputs:** uma tarefa falhando com eval suite e violation counts; os quatro rungs; custo e latência medidos por rung.

**Outputs:** a exploração ordenada (capability, depois budget, depois instruction, depois architecture); comparação custo/qualidade entre rotas que passam; o vencedor econômico.

**Regras do padrão:**

1. **Ordem fixa, do rung barato ao caro de testar**: cada rung é barato de testar relativo ao seguinte. Model upsizing é um config change; decomposition é engenharia (três prompts para manter em vez de um).
2. **Violation counts como sinal direcional ao longo da escalada**: entre rungs, a contagem de violações mostra se a capability está melhorando mesmo quando pass/fail não moveu (mesma métrica do [[docs/canonical/eval-gated-model-migration-diagnostic|Eval-Gated Model Migration Diagnostic]]).
3. **Pass/fail não decide; a economia decide**: rungs iniciais podem passar evals a custo inaceitável. A comparação de custo/latência entre rotas que passam é parte do padrão, não afterthought.
4. **O vencedor econômico tipicamente é o último rung**: no caso-fonte, o rung de decomposition passou tudo no menor custo. É a tese harness-over-model em miniatura: decompor o trabalho vence upsizar o modelo.

## Implementação neste repositório

### O que já existe

As alavancas existem separadamente, cada uma com cobertura canônica:

- **Rung capability (tiering)**: [[docs/canonical/task-routed-model-tiering|Task-Routed Model Tiering]] roteia por subtarefa para custo/latência de tarefas que funcionam (`docs/canonical/task-routed-model-tiering.md:32`), não como escalada de tarefas que falham.
- **Rung architecture (decomposition)**: [[docs/canonical/generator-evaluator|Generator-Evaluator]] (dois agentes com loop de feedback) e [[docs/canonical/plan-execute-verify|Plan-Execute-Verify]] (fases com gates de sucesso) fornecem os componentes do rung vencedor.
- **Disciplina de ROI**: [[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]] governa adicionar/medir/remover componentes de harness com ROI.

### O que falta

O procedimento ordenado em si:

1. **Nenhuma ordenação de alavancas para tarefa que falha**. NOT_FOUND: grep `bigger model|larger model|model upsiz|escalation ladder|reasoning budget|adaptive thinking` em `docs/canonical/` retorna 2 hits, ambos cross-references ao degradation ladder runtime (`docs/canonical/multi-agent-fault-tolerance.md:110`, `docs/canonical/multi-provider-model-routing.md:85`) ([[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-classification|The Prompting Playbook Classification]]:113).
2. **Adjacentes não-equivalentes**: [[docs/canonical/tested-degradation-ladder|Tested Degradation Ladder]] (`:29`: classify, retry, safe fallback, human escalation para falha runtime); [[docs/canonical/task-routed-model-tiering|Task-Routed Model Tiering]] (`:32`: routing por custo/latência de tarefas funcionando); [[docs/canonical/model-switching-architecture-enterprise-eval-gate|Model-Switching Architecture Enterprise Eval Gate]] (`:61-71`: gate de migração entre candidatos, não ordenação intra-tarefa); [[docs/canonical/invariant-compensation-split|Invariant-Compensation Split]] (`:23`: medir compensações obsoletas, não escolher entre alavancas) ([[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-classification|The Prompting Playbook Classification]]:114).
3. **A análise de vencedor econômico**: comparação custo/latência entre rotas que passam, com o argumento econômico de que decomposition vence upsizing. [[docs/canonical/token-economics-gap-filling|Token Economics Gap Filling]] cobre custo de inferência vs. especificação, um trade-off diferente.

## Tradeoffs

| Benefício | Custo |
|---|---|
| Cada rung é barato de testar relativo ao seguinte; a ordem evita pular direto ao caro | Rungs tardios custam mais engenharia (três prompts para manter em vez de um) |
| Impede shippar rotas que passam evals mas falham economia (triplo tokens e latência) | Rungs iniciais podem passar evals a custo inaceitável; pass/fail sozinho não decide |
| Violation counts dão sinal direcional ao longo da escalada | Sem infraestrutura de eval para comparar rungs, o ladder é sem sentido |
| No caso-fonte, o rung de decomposition passou tudo no menor custo | A engenharia do rung vencedor precisa manutenção contínua pós-escolha |

## Relação com outros padrões

- **Unifica:** [[docs/canonical/task-routed-model-tiering|Task-Routed Model Tiering]] (rung capability), [[docs/canonical/structural-prompt-hygiene|Structural Prompt Hygiene]] e [[docs/canonical/two-sided-trade-off-instruction|Two-Sided Trade-off Instruction]] (rung instruction) e [[docs/canonical/generator-evaluator|Generator-Evaluator]] com [[docs/canonical/plan-execute-verify|Plan-Execute-Verify]] (rung architecture) sob um protocolo de escalada único.
- **Usa:** [[docs/canonical/eval-gated-model-migration-diagnostic|Eval-Gated Model Migration Diagnostic]]: o diagnóstico behavior-vs-capability classifica a falha antes de escolher o rung, e os violation counts dão o sinal direcional entre rungs.
- **Materializa a tese de:** [[docs/canonical/model-agnostic-agent-vm-harness|Model-Agnostic Agent-VM Harness]] e da tese central do repo de atacar falhas estruturais via harness engineering em vez de modelos melhores ou prompts maiores (`docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-mental-model.md:23`): o ladder é o procedimento medido dessa tese, e o caso-fonte (decomposition vencendo em economia) é o argumento.
- **Contrasta com:** [[docs/canonical/tested-degradation-ladder|Tested Degradation Ladder]]: degraus de falha runtime (retry/fallback/humano) vs. degraus de investimento de capability; dois ladders ortogonais que se compõem.
- **Adjacente a:** [[docs/canonical/token-economics-gap-filling|Token Economics Gap Filling]]: economia de tokens como critério de decisão entre rotas que passam.

## Referências

- `docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-patterns.md:112-130` (seção 6): definição do padrão, quatro rungs, benefícios, limitações.
- `docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-classification.md:106-116` (seção 6): Missing (High), NOT_FOUND com localizações, adjacentes rejeitados, tese harness-over-model.
- `docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-mental-model.md:23`: harness engineering em vez de prompts melhores ou modelos maiores.
- `docs/canonical/task-routed-model-tiering.md:32`: tier routing para tarefas funcionando.
- `docs/canonical/tested-degradation-ladder.md:29`: ladder de falha runtime (não-equivalente).
- `docs/canonical/model-switching-architecture-enterprise-eval-gate.md:61-71`: gate de migração (não-equivalente).
- `docs/canonical/invariant-compensation-split.md:23`: compensações obsoletas (não-equivalente).

---

*Created: 2026-09-02 | From: The Prompting Playbook classification (Batch 1, pattern 6) | Precedence: canonical*
