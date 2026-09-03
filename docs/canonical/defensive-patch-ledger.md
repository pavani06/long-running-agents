---
title: "Defensive Patch Ledger"
type: canonical
status: accepted
date: 2026-09-02
tags: ["harness-engineering", "governanca", "agentes-orquestracao", "production"]
aliases: ["defensive patch ledger", "patch audit", "ledger de patches defensivos", "migration-triggered patch audit"]
last_updated: 2026-09-02
relates-to: ["[[docs/canonical/prompt-as-code-causal-change-management|Prompt-as-Code Causal Change Management]]", "[[docs/canonical/invariant-compensation-split|Invariant-Compensation Split]]", "[[docs/canonical/eval-gated-model-migration-diagnostic|Eval-Gated Model Migration Diagnostic]]", "[[docs/canonical/model-switching-architecture-enterprise-eval-gate|Model-Switching Architecture Enterprise Eval Gate]]", "[[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]]", "[[docs/canonical/structural-prompt-hygiene|Structural Prompt Hygiene]]", "[[docs/canonical/model-agnostic-agent-vm-harness|Model-Agnostic Agent-VM Harness]]"]
sources: ["[[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-patterns|The Prompting Playbook Patterns]]", "[[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-classification|The Prompting Playbook Classification]]"]
---

# Defensive Patch Ledger

**Type:** Canonical Pattern
**Status:** Accepted
**Source:** [[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-patterns|The Prompting Playbook Patterns]] (padrão 4)
**Classification:** Partial Coverage (P1, High integration value)
**Precedence:** Level 2 ([[docs/system-of-record|System of Record]])

---

## Problema

Prompts acumulam **patches defensivos** escritos para falhas de modelos anteriores: instruções que existem porque um modelo antigo falhava de um jeito específico. Modelos mais novos e melhores em instruction following **overfitam** esses patches: obedecem instruções que perderam a razão de ser, tipicamente over-complying proibições e recusando trabalho válido. E ninguém sabe qual patch remover porque o porquê nunca foi registrado.

Sem o ledger, patch debt é um passivo invisível: cresce silenciosamente, deprecia com cada geração de modelo, e a migração de modelo dispara apenas um eval re-run, nunca a pergunta "quais patches esta migração tornou obsoletos?".

## Solução

Um ledger que acopla duas metades já canônicas no repo, o registro de rationale no momento da escrita e a lógica de decaimento por geração de modelo, em um procedimento operacional de migração:

**Inputs:**

1. Um prompt sob version control.
2. Um rationale registrado para cada mudança defensiva: por que foi adicionada, qual falha endereçava, em que era/geração de modelo.

**Outputs:**

1. Um histórico auditável mapeando cada instrução defensiva à falha de era-de-modelo que a justificou.
2. A capacidade de backtracking ou neutralização de patches durante migração de modelo.

**Regras operacionais:**

1. **Rationale no write time ou nunca**: o porquê de cada patch defensivo é registrado quando o patch entra, via commit causal (trigger, diagnosis, intent). Registro posterior não existe.
2. **Migração dispara patch audit, não apenas eval re-run**: quando o modelo troca, o audit percorre o ledger e julga patch a patch: a falha que este patch endereçava ainda existe no novo modelo? O padrão de decisão é o do invariant-compensation split: separar domain risk de model weakness; se a falha persiste com modelo melhor, é invariante candidato; se não persiste, o patch é compensation em decaimento e vira removal candidate.
3. **Patches depreciam entre gerações**: compensações que só faziam sentido para um modelo mais antigo viram cost surface (tokens, latência, instrução conflitante). O audit transforma patch debt de passivo invisível em **inventário deprecável**.
4. **O audit não decide sozinho**: o ledger diz por que cada patch existe; o julgamento de obsolescência ainda é do audit com evidência (eval, shadow test), porque remover patch defensivo pode re-expor a falha original.

## Implementação neste repositório

### O que já existe

As duas metades existem, em canonicals ativos separados:

- **Metade ledger (rationale no write time)**: [[docs/canonical/prompt-as-code-causal-change-management|Prompt-as-Code Causal Change Management]] exige as três perguntas obrigatórias de commit para toda mudança de prompt: causal trigger (incidente/regressão de eval), diagnostic context e predictive intent (`docs/canonical/prompt-as-code-causal-change-management.md:32-59`); infraestrutura de rollback via git com deploy-by-commit e audit trail de rollback (`:80-85`); e o audit trail cumulativo que responde "por que esta mudança foi feita? Que falha a disparou?" (`:98-105`).
- **Metade decaimento (lógica de era de modelo)**: [[docs/canonical/invariant-compensation-split|Invariant-Compensation Split]] documenta o caso de decaimento: um Context Loader mantido depois que um modelo mais novo não precisava mais dele, ainda custando 450ms e 1200 tokens por turno (`docs/canonical/invariant-compensation-split.md:23`); as regras centrais, incluindo "Record the rationale: If future maintainers cannot tell why it exists, governance has failed" (`:64-70`) e o decision test "Separate domain risk from model weakness" (`:67`).

### O que falta

O acoplamento, isto é, o frame de defensive-patch que une as duas metades em um procedimento de migração:

1. **A regra migração → patch audit**. NOT_FOUND: grep `defensive|patch audit|patches` em `docs/canonical/` retorna 10 hits em 7 arquivos; o mais próximo é `docs/canonical/measured-harness-evolution-lifecycle.md:44` ("BUILD is defensive because a new model's production limits are still unknown"), que trata de construir defensivamente, não de auditar patches acumulados na migração; nenhum doc liga patch ledger à troca de modelo como trigger ([[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-classification|The Prompting Playbook Classification]]:85).
2. **O conceito de overfit de patch**: modelos novos e mais instruction-following over-complying patches de modelos antigos, como classe de falha.
3. **O inventário deprecável**: patch debt tratado como inventário auditável por geração de modelo.

## Tradeoffs

| Benefício | Custo |
|---|---|
| Transforma patch debt de passivo invisível em inventário depreciable | Custo de disciplina: o rationale deve ser registrado no write time ou nunca |
| Migração de modelo dispara patch audit, não só eval re-run | O ledger não decide sozinho quais patches são obsoletos; julgamento do audit continua necessário |
| Operacionaliza o invariant-compensation split: compensações decaem entre gerações; invariantes de domínio sobrevivem | Depende de infraestrutura de prompt-as-code (version control) já instituída |
| Backtracking de patch individual com contexto completo (qual falha, qual modelo, qual era) | Remover patch pode re-expor a falha original; cada remoção precisa eval |

## Relação com outros padrões

- **Operacionaliza:** [[docs/canonical/prompt-as-code-causal-change-management|Prompt-as-Code Causal Change Management]] (o ledger de rationale) e [[docs/canonical/invariant-compensation-split|Invariant-Compensation Split]] (a lógica de decaimento por geração de modelo); o patch audit é o procedimento que consome os dois.
- **Disparado por:** [[docs/canonical/eval-gated-model-migration-diagnostic|Eval-Gated Model Migration Diagnostic]]: a migração diagnosticada é o evento que abre o patch audit.
- **Estende o procedimento de:** [[docs/canonical/model-switching-architecture-enterprise-eval-gate|Model-Switching Architecture Enterprise Eval Gate]]: a migração completa é eval re-run (gate) mais patch audit (ledger).
- **Alinha com:** [[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]]: o patch audit é o SIMPLIFY aplicado ao plano de instrução, com as mesmas exigências de ROI e evidência antes de remover.
- **Depende de:** [[docs/canonical/structural-prompt-hygiene|Structural Prompt Hygiene]]: patches defensivos só são auditáveis quando visíveis como seções estruturadas do prompt.
- **Serve a tese de:** [[docs/canonical/model-agnostic-agent-vm-harness|Model-Agnostic Agent-VM Harness]]: se o modelo é slot swapável, o que não é invariante de domínio (patches, compensações) precisa de ledger para depreciação limpa a cada step-change.

## Referências

- `docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-patterns.md:73-90` (seção 4): definição do padrão, inputs, outputs, benefícios, limitações.
- `docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-classification.md:75-87` (seção 4): Partial Coverage (High), evidência file:line e NOT_FOUND.
- `docs/canonical/prompt-as-code-causal-change-management.md:32-59`, `:80-85`, `:98-105`: perguntas causais, rollback, audit trail.
- `docs/canonical/invariant-compensation-split.md:23`, `:64-70`, `:67`: caso Context Loader, regras de rationale e decision test.
- `docs/canonical/measured-harness-evolution-lifecycle.md:44`: BUILD defensivo (adjacente rejeitado na classificação).

---

*Created: 2026-09-02 | From: The Prompting Playbook classification (Batch 1, pattern 4) | Precedence: canonical*
