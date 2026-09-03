---
title: "Hard/Soft Constraint Grader Split"
type: canonical
status: accepted
date: 2026-09-02
tags: ["evals", "agentes-orquestracao", "harness-engineering"]
aliases: ["hard soft constraint split", "separação hard soft constraints", "deterministic grader llm judge", "constraint grader partition"]
last_updated: 2026-09-02
relates-to: ["[[docs/canonical/3-layer-evaluation-architecture|3-Layer Evaluation Architecture]]", "[[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]", "[[docs/canonical/generator-evaluator|Generator-Evaluator]]", "[[docs/canonical/magnitude-direction-verifier-split|Magnitude-Direction Verifier Split]]", "[[docs/canonical/eval-tier-stratification|Eval Tier Stratification]]"]
sources: ["[[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-patterns|The Prompting Playbook Patterns]]", "[[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-classification|The Prompting Playbook Classification]]"]
---

# Hard/Soft Constraint Grader Split

**Type:** Canonical Pattern
**Status:** accepted
**Source:** [[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-patterns|The Prompting Playbook Patterns]] (padrão 7)
**Classification:** Partial Coverage / Medium ([[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-classification|The Prompting Playbook Classification]]:128, :258)
**Precedence:** Level 2 ([[docs/system-of-record|System of Record]])

---

## Problema

Outputs de agentes misturam dois tipos de exigência com naturezas opostas: regras binárias (formato, campos obrigatórios, proibições) e preferências difusas (tom, completude, qualidade percebida). Quando os dois são entregues a um único juiz — tipicamente um LLM judge — o resultado é um dos dois fracassos simétricos: hard rules graduadas de forma não determinística (o juiz aprova ora sim ora não uma regra que deveria ser binária), ou soft preferences ossificadas em checklist rígido ([[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-patterns|The Prompting Playbook Patterns]]:135).

O custo é duplo: paga-se custo de LLM e não-determinismo por checagens que um regex/schema faria por zero; e perde-se o sinal direcional — quando o pass/fail binário não se move, não há métrica intermediária que mostre se a capacidade está melhorando.

## Solução

Particionar as constraints da tarefa em duas classes e atribuir a cada uma o grader certo:

1. **Hard constraints** (binárias, contáveis) → função determinística (regex, schema validation, parser). Executa em múltiplos trials por candidato e reporta **violation counts por regra por trial** — sinal direcional barato: mesmo quando o pass/fail não se move, a contagem de violações por regra mostra se o candidato está convergindo ([[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-patterns|The Prompting Playbook Patterns]]:137-138, :142, :147).
2. **Soft constraints** (preferências) → prompt do LLM evaluator, carregando as preferências como conteúdo de prompt. Isso torna as soft constraints **runtime-tunable**: ajustar a preferência é editar texto do evaluator, não deploy de backend ([[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-patterns|The Prompting Playbook Patterns]]:139, :143, :146).

```text
Task constraints
        |
        v
  Partition (hard vs soft)
        |                         |
        v                         v
  HARD (binary, countable)   SOFT (preferences)
  deterministic checker      LLM evaluator prompt
  regex / schema / parser    (runtime-editable content)
        |                         |
        v                         v
  violation counts          soft judgment
  per rule per trial        (approve / reject + rationale)
```

A partição exige disciplina: constraint ambígua força a escolha de lado, e o evaluator LLM conserva não-determinismo e custo na porção soft ([[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-patterns|The Prompting Playbook Patterns]]:149-151).

## Implementação neste repositório

### O que já existe

- A partição central existe em profundidade canônica, generalizada por tipo de mecanismo: [[docs/canonical/3-layer-evaluation-architecture|3-Layer Evaluation Architecture]] separa Layer 1 Deterministic (regex, schema validation, NER PII, custo zero de LLM, bloqueia deploy/resposta — `:30-43`) de Layer 2 Semantic/LLM-as-Judge (groundedness, safety, relevance — `:45-59`).
- [[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]] define a matriz de verificação `constraint -> check -> pass/fail -> violation detail`, com veredito agregado aprovado só se todas as linhas passarem (`:31-33`).
- O currículo já prescreve a direção do split nas correções de anti-padrões: "Implementar verificacao programatica de hard rules (nao depender so do LLM)" ([[curriculum/05-core-concepts/08-evaluation-rubrics|Evaluation Rubrics]]:2176), hard rules como veto ("Transformar a falha em veto, não em peso", `:705`; "hard rules PRIMEIRO. Sempre", `:1232`).

### O que falta

(Classificação:130, :140 — NOT_FOUND com locais pesquisados.)

1. **Guidance de particionamento** — qual constraint vai para qual grader é gap auto-reconhecido do repo: [[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]:77 admite "No guidance on constraint granularity, such as what deserves a hard constraint versus what should remain reviewer judgment".
2. **Violation counts por regra por trial** como convenção de reporting de eval — existe apenas como conceito em um eixo diferente: [[docs/canonical/magnitude-direction-verifier-split|Magnitude-Direction Verifier Split]]:100 particiona confiança interna vs veredito externo, não checker determinístico vs LLM judge.
3. **Soft constraints como conteúdo de evaluator injetado em runtime**, sem deploy de backend — ausente em `docs/decisions/`, `docs/canonical/`, `docs/evidence/`, `curriculum/`, `.opencode/` (grep `violation count`, `soft constraint`, `runtime.*inject` — matches apenas dentro do próprio pacote de análise).

## Tradeoffs

| Benefício | Custo |
|---|---|
| Hard rules graduadas programaticamente, não por juiz não determinístico | Exige partição limpa; constraint ambígua força escolha de lado |
| Soft constraints viram conteúdo de prompt runtime-tunable, sem deploy | O evaluator LLM mantém não-determinismo e custo na porção soft |
| Violation counts dão sinal direcional quando pass/fail não se move | Multi-trial multiplica o runtime do eval |
| Fecha o gap de granularity auto-reconhecido em constraint-anchored-evaluation:77 | Mais uma convenção de reporting para manter |

## Relação com outros padrões

- **Especializa:** [[docs/canonical/3-layer-evaluation-architecture|3-Layer Evaluation Architecture]] — a Layer 1/Layer 2 daquele padrão é a partição por mecanismo; este padrão adiciona o critério de partição por constraint e o reporting por contagem.
- **Depende de:** [[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]] — a matriz de verificação por constraint é o veículo natural dos violation counts por regra.
- **Complementa:** [[docs/canonical/generator-evaluator|Generator-Evaluator]] — o Evaluator carrega as soft constraints; as hard saem dele para o checker determinístico ([[curriculum/05-core-concepts/08-evaluation-rubrics|Evaluation Rubrics]]:705).
- **Compõe com:** [[docs/canonical/magnitude-direction-verifier-split|Magnitude-Direction Verifier Split]] (contagem determinística como sinal de magnitude/evolução) e [[docs/canonical/eval-tier-stratification|Eval Tier Stratification]] (o checker determinístico roda no fast tier; o judge no medium/deep).

## Referências

- [[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-patterns|The Prompting Playbook Patterns]]:132-152 — definição do padrão 7 (inputs, outputs, benefícios, limitações).
- [[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-classification|The Prompting Playbook Classification]]:126-142 — Partial Coverage/Medium com evidência file:line e NOT_FOUND.
- [[docs/canonical/3-layer-evaluation-architecture|3-Layer Evaluation Architecture]]:30-59 — Layer 1 Deterministic e Layer 2 Semantic/LLM-as-Judge.
- [[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]:31-33, :77 — matriz de verificação e gap de granularity.
- [[curriculum/05-core-concepts/08-evaluation-rubrics|Evaluation Rubrics]]:705, :1232, :2176 — hard rule como veto; verificação programática de hard rules.
- [[docs/canonical/magnitude-direction-verifier-split|Magnitude-Direction Verifier Split]]:100 — split adjacente em eixo diferente (confiança interna vs veredito externo).

---

*Criado: 2026-09-02 | De: The Prompting Playbook classification | Precedência: canonical*
