---
title: "Ban-to-Source-of-Truth Rebalancing"
type: canonical
status: accepted
date: 2026-09-02
tags: ["context-engineering", "harness", "governanca"]
aliases: ["ban to source of truth", "rebalanceamento ban para source of truth", "withholding inverse hallucination", "prohibition rebalancing"]
last_updated: 2026-09-02
relates-to: ["[[docs/canonical/prompt-as-code-causal-change-management|Prompt-as-Code Causal Change Management]]", "[[docs/canonical/invariant-compensation-split|Invariant-Compensation Split]]", "[[docs/canonical/stable-harness-prompt|Stable Harness Prompt]]"]
sources: ["[[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-patterns|The Prompting Playbook Patterns]]", "[[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-classification|The Prompting Playbook Classification]]"]
---

# Ban-to-Source-of-Truth Rebalancing

**Type:** Canonical Pattern
**Status:** accepted
**Source:** [[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-patterns|The Prompting Playbook Patterns]] (padrão 11)
**Classification:** Partial Coverage / Medium ([[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-classification|The Prompting Playbook Classification]]:211, :262)
**Precedence:** Level 2 ([[docs/system-of-record|System of Record]])

---

## Problema

Bans defensivos escritos para o fracasso de um modelo antigo ("never give plan details, point to the URL") fazem modelos novos, mais instruction-following, reterem informação que eles de fato têm no contexto — **o fracasso inverso da hallucination**: em vez de inventar o que não sabe, o modelo esconde o que sabe ([[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-patterns|The Prompting Playbook Patterns]]:215). A mesma instrução que protegia contra invenção agora produz under-delivery, e a ban list só cresce.

## Solução

Substituir a proibição por uma **designação balanceada da fonte de verdade** ([[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-patterns|The Prompting Playbook Patterns]]:217-221):

```text
ANTES (ban)                    DEPOIS (source of truth)
─────────────────────          ─────────────────────────────
"Never give plan details.      "The customer record in context
 Point to the URL."             is the accurate source of truth;
                                answer from it."
+ dados autoritativos          + mesma garantia anti-hallucination
  já presentes no contexto        sem withhold
```

O mecanismo é uma só jogada para os dois lados da falha: **designar a fonte de verdade em vez de proibir a saída** — conserta hallucination (o modelo responde a partir dos dados designados, não da imaginação) e conserta withholding (o modelo tem permissão explícita de servir o que está na fonte) ([[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-patterns|The Prompting Playbook Patterns]]:223). Efeitos colaterais positivos: prompt mais curto (ban lists longas removidas) e fim do over-compliance de modelos novos a proibições antigas (`:224-225`).

Três condições de contorno (`:227-229`):

1. Os dados in-context precisam ser confiáveis — contexto ruim passa a ser servido com confiança.
2. Julgar quais bans ainda são load-bearing depende do ledger de rationale (o padrão declara essa dependência explicitamente).
3. Suavizar um ban pode reexpor a falha original que ele corrigiu — o caso tem que ser eval'd antes e depois.

## Implementação neste repositório

### O que já existe

- O mecanismo de decay que torna bans de modelo antigo perigosos é canônico: [[docs/canonical/invariant-compensation-split|Invariant-Compensation Split]]:23 — compensação escrita para um modelo de 32K ainda custando latência/tokens depois que o modelo novo não precisa dela; `:67` — teste de decisão: "Separate domain risk from model weakness — if the failure still exists with a better model, it is an invariant candidate".
- O audit que permite julgar quais bans ainda são load-bearing: [[docs/canonical/prompt-as-code-causal-change-management|Prompt-as-Code Causal Change Management]]:30-59 — as três perguntas causais obrigatórias (why changed / what failure caused it / what failure it addresses) para cada mudança de prompt, com rollback e audit trail.
- Designação de source of truth existe em objetos adjacentes: KODA registra `source_of_truth` por campo de output como mitigação de falha ([[curriculum/06-knowledge-graphs/02-koda-feature-dependencies|KODA Feature Dependencies]]:1373 — provenance de dados, não design de instrução); `curriculum/05-core-concepts/02-planning-execution-separation.md:366` usa "single source of truth" para a phase contract (objeto diferente: contrato de fase, não dado de cliente in-context vs ban).

### O que falta

(Classificação:213, :221 — NOT_FOUND com locais pesquisados.)

1. **O movimento de rebalancing em si** — substituir instrução de proibição por designação balanceada do dado in-context como fonte de verdade. Buscas por `ban`, `proibi`, `withhold`, `source of truth`, `source_of_truth`, `grandfather`, `allowance` em `docs/decisions/`, `docs/canonical/`, `docs/evidence/`, `curriculum/`, `.opencode/` só encontram o sentido governance/state-provenance, proibições de política dentro de rubrics, ou os próprios arquivos do pacote de análise.
2. **O framing withholding-como-inverso-da-hallucination** — nenhum doc, código ou material curricular trata os dois como a mesma classe de falha, corrigida pela mesma jogada.
3. **Ban lists como classe de artefato a rebalancear** — prompt-as-code registra o porquê de cada patch, mas não diz como reescrever; este padrão é o complemento operacional.

## Tradeoffs

| Benefício | Custo |
|---|---|
| Corrige withholding com a mesma jogada que corrige hallucination | Exige dados in-context confiáveis; contexto ruim é servido com confiança |
| Prompt mais curto — ban lists longas removidas | Julgar quais bans são load-bearing requer o ledger de rationale (disciplina de write-time) |
| Modelos novos param de over-compliar proibições de modelo antigo | Suavizar um ban pode reexpor a falha original — o caso deve ser eval'd |
| Neutralização governada de patches defensivos em migração de modelo | Dependência: sem prompt-as-code, o audit de bans é palpite |

## Relação com outros padrões

- **Depende de:** [[docs/canonical/prompt-as-code-causal-change-management|Prompt-as-Code Causal Change Management]] — o rationale ledger responde qual ban ainda é load-bearing antes de rebalancear.
- **Opera sobre:** [[docs/canonical/invariant-compensation-split|Invariant-Compensation Split]] — o ban é o caso textual da compensação que decai entre gerações de modelo; este padrão é o "como neutralizar" que aquele classifica como "como decidir".
- **Respeita:** [[docs/canonical/stable-harness-prompt|Stable Harness Prompt]] — o rebalancing reescreve blocos de policy do harness prompt (não do payload redutível), mudança deliberada e versionada.
- **Cousin de designação:** o `source_of_truth` por campo do KODA ([[curriculum/06-knowledge-graphs/02-koda-feature-dependencies|KODA Feature Dependencies]]:1373) designa a fonte no dado; este padrão designa no prompt.

## Referências

- [[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-patterns|The Prompting Playbook Patterns]]:212-229 — definição do padrão 11 (inputs, outputs, benefícios, limitações).
- [[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-classification|The Prompting Playbook Classification]]:209-223 — Partial Coverage/Medium com evidência file:line e NOT_FOUND.
- [[docs/canonical/invariant-compensation-split|Invariant-Compensation Split]]:23, :67 — mecanismo de decay e teste de decisão domínio vs. modelo.
- [[docs/canonical/prompt-as-code-causal-change-management|Prompt-as-Code Causal Change Management]]:30-59 — perguntas causais que viabilizam o audit de bans.
- [[curriculum/06-knowledge-graphs/02-koda-feature-dependencies|KODA Feature Dependencies]]:1373 — `source_of_truth` por campo (provenance de dados).
- `curriculum/05-core-concepts/02-planning-execution-separation.md:366` — single source of truth aplicado à phase contract (adjacente não-equivalente).

---

*Criado: 2026-09-02 | De: The Prompting Playbook classification | Precedência: canonical*
