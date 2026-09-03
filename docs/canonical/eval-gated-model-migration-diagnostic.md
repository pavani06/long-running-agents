---
title: "Eval-Gated Model Migration Diagnostic"
type: canonical
status: accepted
date: 2026-09-02
tags: ["evals", "agentes-orquestracao", "harness-engineering", "production"]
aliases: ["eval gated migration diagnostic", "behavior vs capability diagnosis", "diagnostico de migracao de modelo", "violation count signal"]
last_updated: 2026-09-02
relates-to: ["[[docs/canonical/model-switching-architecture-enterprise-eval-gate|Model-Switching Architecture Enterprise Eval Gate]]", "[[docs/canonical/model-switch-driven-eval-hardening|Model-Switch-Driven Eval Hardening]]", "[[docs/canonical/3-layer-evaluation-architecture|3-Layer Evaluation Architecture]]", "[[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]", "[[docs/canonical/living-eval-dataset|Living Eval Dataset]]", "[[docs/canonical/defensive-patch-ledger|Defensive Patch Ledger]]", "[[docs/canonical/capability-escalation-ladder|Capability Escalation Ladder]]"]
sources: ["[[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-patterns|The Prompting Playbook Patterns]]", "[[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-classification|The Prompting Playbook Classification]]"]
---

# Eval-Gated Model Migration Diagnostic

**Type:** Canonical Pattern
**Status:** Accepted
**Source:** [[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-patterns|The Prompting Playbook Patterns]] (padrão 1)
**Classification:** Partial Coverage (P2, Medium integration value)
**Precedence:** Level 2 ([[docs/system-of-record|System of Record]])

---

## Problema

Quando um prompt de produção migra para um novo modelo e a performance cai, o time não consegue distinguir **diferença de comportamento** (remediável por tuning de prompt/harness) de **capability gap** (nenhuma quantidade de prompting resolve). Sem essa distinção, o esforço é queimado promptando ao redor de um déficit de capacidade que pede outro remédio: troca de modelo, decomposição ou ferramenta.

O gate de migração existente no repo decide Switch/Hold/Hybrid no nível do portfólio, comparando candidato vs. atual por categoria, mas nunca responde, por caso que falha, se prompting é a alavanca certa ([[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-classification|The Prompting Playbook Classification]]:26).

Há ainda um segundo problema de sinal: pass/fail binário é grosseiro. Quando a suite não move o score, não se sabe se o modelo está melhorando por baixo. Uma métrica de **violation count** (contagem de violações por regra por caso) dá sinal direcional que pass/fail esconde.

## Solução

Adicionar uma etapa de diagnóstico por falha dentro do comparison report do gate de migração. O padrão define:

**Inputs:**

1. Prompt de produção sendo migrado para o novo modelo.
2. Eval suite cobrindo o comportamento do prompt, executada antes e depois da migração.
3. Resultados pass/fail por caso mais uma métrica de violation count.

**Outputs:**

1. Diagnóstico por falha: behavior difference vs. capability gap.
2. Sinal de regression test para a decisão de migração (e para toda migração futura).

**Mecanismo, passo a passo:**

1. **Rodar a suite nos dois modelos** e produzir o comparison report (por camada, por categoria, casos de regressão, custo por query), como já prescrito em [[docs/canonical/model-switching-architecture-enterprise-eval-gate|Model-Switching Architecture Enterprise Eval Gate]].
2. **Revalidar cada caso que regrediu antes de concluir**: variância natural entre runs pode imitar regressão; reexecutar o caso específico.
3. **Classificar cada falha** em uma das duas causas únicas possíveis:
   - **Behavior difference**: o modelo tem a capacidade (raciocínio, conhecimento, instruction following) mas o formato/estilo/interpretacao da instrução diverge do esperado. Remédio: ajustar prompt ou harness.
   - **Capability gap**: a capacidade exigida pelo caso está fora do alcance do modelo. Remédio: não é prompting; é capability escalation (modelo maior, decomposição, ferramenta).
4. **Registrar violation counts** por caso/rea. Quando pass/fail não se move entre candidatos, a contagem de violações dá sinal direcional: capability melhorando.
5. **Alimentar a decisão Switch/Hold/Hybrid** com o diagnóstico agregado: regressões de comportamento são endereçáveis antes do switch; regressões de capability são bloqueadores ou delimitam o escopo Hybrid.

A mesma suite, por construção, funciona como regression suite para toda migração futura.

## Implementação neste repositório

### O que já existe

- [[docs/canonical/model-switching-architecture-enterprise-eval-gate|Model-Switching Architecture Enterprise Eval Gate]] cobre a metade gate em profundidade canônica: comparação side-by-side candidato vs. atual contra o enterprise eval dataset, com breakdown por categoria e casos de regressão específicos (`docs/canonical/model-switching-architecture-enterprise-eval-gate.md:43-59`), e o framework de decisão Switch/Hold/Hybrid dirigido pelos dados de comparação (`:61-71`).
- [[docs/canonical/model-switch-driven-eval-hardening|Model-Switch-Driven Eval Hardening]] traz o "switch as regression detection": a suite existente roda sobre os outputs do novo provider, com pass/fail comparado ao provider anterior (`docs/canonical/model-switch-driven-eval-hardening.md:40`).
- [[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]] fornece a primitiva de report por violação: uma linha por constraint com pass/fail binário e violation detail (`docs/canonical/constraint-anchored-evaluation.md:31-33`), base natural para o violation count.
- [[docs/canonical/living-eval-dataset|Living Eval Dataset]] fornece a suite que cresce monotonicamente e serve de regression suite para migrações (`docs/canonical/living-eval-dataset.md:28`).

### O que falta

1. **O núcleo diagnóstico**: classificação por falha em behavior difference vs. capability gap. NOT_FOUND: grep `capability gap` em `docs/` retorna apenas os arquivos desta análise e `docs/canonical/invariant-compensation-split.md:49` (label de diagrama do ramo de compensação, não um diagnóstico de migração) ([[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-classification|The Prompting Playbook Classification]]:33).
2. **A métrica de violation count** como sinal direcional. NOT_FOUND: grep `violation count|violations per|per-rule violation|count-based` em `docs/canonical/` sem matches ([[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-classification|The Prompting Playbook Classification]]:34).
3. **Nota de implementação**: o próprio canonical de model-switching declara que a infraestrutura concreta de switching "does not exist" no repo, é design documentado (`docs/canonical/model-switching-architecture-enterprise-eval-gate.md:24`). O diagnóstico aqui é a extensão do design, não de código existente.

## Tradeoffs

| Benefício | Custo |
|---|---|
| Separa as duas únicas causas possíveis de falha pós-migração, cada uma com remédio distinto | Exige que a eval suite exista antes da migração; sem ela, iteração é vibes |
| Dobra como regression suite para toda migração futura | Variância natural entre runs pode imitar regressão; cada caso precisa revalidação antes da conclusão |
| Violation counts dão sinal direcional (capability melhorando) mesmo com pass/fail parado | Multi-trial para contagem de violações multiplica o runtime da avaliação |
| Diagnóstico agregado qualifica a decisão Switch/Hold/Hybrid (regressão de comportamento é endereçável; de capability é bloqueadora) | Só tão representativo quanto a taxonomia de casos da suite (ver [[docs/canonical/control-edge-boundary-eval-taxonomy|Control/Edge/Boundary Eval Taxonomy]]) |

## Relação com outros padrões

- **Estende:** [[docs/canonical/model-switching-architecture-enterprise-eval-gate|Model-Switching Architecture Enterprise Eval Gate]]: o diagnóstico por falha é a etapa que falta dentro do comparison report existente.
- **Compõe com:** [[docs/canonical/model-switch-driven-eval-hardening|Model-Switch-Driven Eval Hardening]]: o switch como regression detection ganha a pergunta "por caso, a falha é de comportamento ou de capacidade?".
- **Usa:** [[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]] para a matriz de verificação que produz violation detail por regra.
- **Usa:** [[docs/canonical/living-eval-dataset|Living Eval Dataset]] e [[docs/canonical/3-layer-evaluation-architecture|3-Layer Evaluation Architecture]] como a suite e o breakdown por camada do diagnóstico.
- **Dispara:** [[docs/canonical/defensive-patch-ledger|Defensive Patch Ledger]]: a migração diagnosticada é o gatilho do patch audit, não apenas do eval re-run.
- **Desagua em:** [[docs/canonical/capability-escalation-ladder|Capability Escalation Ladder]]: falhas classificadas como capability gap entram no procedimento ordenado de escalada de alavancas.
- **Representatividade por:** [[docs/canonical/control-edge-boundary-eval-taxonomy|Control/Edge/Boundary Eval Taxonomy]]: a qualidade do diagnóstico é limitada pela taxonomia de casos da suite.

## Referências

- `docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-patterns.md:16-34` (seção 1): definição do padrão, inputs, outputs, benefícios, limitações.
- `docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-classification.md:22-36` (seção 1): Partial Coverage, evidência file:line e NOT_FOUND.
- `docs/canonical/model-switching-architecture-enterprise-eval-gate.md:43-59` e `:61-71`: comparison report e decisão Switch/Hold/Hybrid.
- `docs/canonical/model-switch-driven-eval-hardening.md:40`: switch as regression detection.
- `docs/canonical/constraint-anchored-evaluation.md:31-33`: verificação por constraint com violation detail.
- `docs/canonical/model-switching-architecture-enterprise-eval-gate.md:24`: infraestrutura de switching declarada como não implementada.

---

*Created: 2026-09-02 | From: The Prompting Playbook classification (Batch 1, pattern 1) | Precedence: canonical*
