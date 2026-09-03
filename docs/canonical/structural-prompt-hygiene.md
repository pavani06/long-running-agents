---
title: "Structural Prompt Hygiene"
type: canonical
status: accepted
date: 2026-09-02
tags: ["context-engineering", "harness-engineering", "harness", "agentes-orquestracao", "evals"]
aliases: ["prompt hygiene", "structural prompt sectioning", "higiene estrutural de prompt", "xml tagged prompt sections"]
last_updated: 2026-09-02
relates-to: ["[[docs/canonical/stable-harness-prompt|Stable Harness Prompt]]", "[[docs/canonical/prompt-as-code-causal-change-management|Prompt-as-Code Causal Change Management]]", "[[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]", "[[docs/canonical/defensive-patch-ledger|Defensive Patch Ledger]]", "[[docs/canonical/3-layer-evaluation-architecture|3-Layer Evaluation Architecture]]"]
sources: ["[[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-patterns|The Prompting Playbook Patterns]]", "[[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-classification|The Prompting Playbook Classification]]"]
---

# Structural Prompt Hygiene

**Type:** Canonical Pattern
**Status:** Accepted
**Source:** [[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-patterns|The Prompting Playbook Patterns]] (padrão 3)
**Classification:** Partial Coverage (P2, Medium integration value)
**Precedence:** Level 2 ([[docs/system-of-record|System of Record]])

---

## Problema

Prompts de produção com múltiplos donos misturam policy, tone, process, data e defensive patches em texto indiferenciado. O modelo não consegue distinguir as camadas, e os mantenedores também não. Redundância acumulada, web copy colado e false identity claims (o prompt declarando ser algo que não é) agrava: cada instrução nova é interpretada contra um ruído de fundo que ninguém controla.

A regra de bolso do padrão captura o diagnóstico: **se um leitor humano não consegue distinguir guidelines de policy de data, o modelo também não consegue**. A separação conserta os dois de uma vez.

O gap é concreto no repo: o system prompt da aplicação é hand-authored com 1800+ linhas, não versionado nem eval'd como componente separado (`docs/canonical/owned-agent-control-loop.md:102`), gap reconhecido pela própria cadeia canônica (`docs/canonical/prompt-as-code-causal-change-management.md:116`).

## Solução

Higiene estrutural de prompt como operação de refactor mensurável, aplicável a qualquer prompt legado:

**Inputs:**

1. Um prompt legado com concerns misturados, redundância, pasted web copy e false identity claims.
2. Um esquema estrutural de seções, por exemplo XML tags: role, guidelines, policy, tone of voice, data.

**Outputs:**

1. Um prompt com seções logicamente separadas e taggeadas, redundância removida, pasted copy e false identity eliminados.
2. Um uplift de eval medido proveniente da higiene sozinha, antes de qualquer fix dirigido a falha específica.

**Mecanismo, passo a passo:**

1. **Secionar**: envolver cada concern em tags explícitas (`<role>`, `<guidelines>`, `<policy>`, `<tone_of_voice>`, `<data>`). A fronteira visível vale para o modelo e para o mantenedor.
2. **Remover redundância**: instruções repetidas ou contraditórias entre seções colapsam em uma ocorrência na seção certa.
3. **Remover pasted copy e false identity**: texto colado da web e claims de identidade falsas saem; o prompt declara apenas o que é e governa.
4. **Medir antes de fixar**: rodar a eval suite antes e depois da higiene. No caso-fonte, a higiene sozinha produziu uplift antes de qualquer fix dirigido, estabelecendo o baseline limpo sobre o qual fixes dirigidos passam a ser atribuíveis.
5. **Nomear um owner**: a higiene re-acumula rot sem um dono explícito que mantenha a estrutura em toda mudança.

Limites declarados: higiene não corrige modos de falha específicos (isso exige trabalho dirigido); evals pós-higiene ainda mostram variância por caso que precisa revalidação caso a caso.

## Implementação neste repositório

### O que já existe

- **Separação funcional de concerns**: [[docs/canonical/stable-harness-prompt|Stable Harness Prompt]] enumera role, policy, tool contracts, safety boundaries, response format e evaluation behavior como concerns distintos do harness prompt (`docs/canonical/stable-harness-prompt.md:22`) e define o context builder montando cada chamada a partir de blocos distintos com política de redução por bloco (`docs/canonical/stable-harness-prompt.md:30-39`).
- **Disciplina de versionamento e ownership**: [[docs/canonical/prompt-as-code-causal-change-management|Prompt-as-Code Causal Change Management]] fornece o versionamento e o commit causal (trigger, diagnosis, intent) que governam mudanças no prompt já higienizado.
- **Superfície concreta onde aplicar**: o system prompt hand-authored de 1800+ linhas, não versionado nem eval'd como componente separado (`docs/canonical/owned-agent-control-loop.md:102`).

### O que falta

1. **As mecânicas de higiene propriamente ditas**: seccionamento XML-tagged de um prompt legado de concerns misturados (role/guidelines/policy/tone/data), remoção de redundância e de false identity/pasted copy. NOT_FOUND: grep repo-wide `XML tag|tagged section|tone of voice|prompt hygiene|structural prompt` casa apenas os arquivos desta própria análise; nenhum canonical, curriculum ou skill cobre tagged sectioning ou higiene de refactor de prompt ([[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-classification|The Prompting Playbook Classification]]:67).
2. **A regra de bolso** (human readability como proxy de model parsability) como ensino curricular.
3. **O resultado medido de uplift-antes-do-fix-dirigido** como caso de ensino: higiene barata com ganho mensurado antes de trabalho dirigido.

## Tradeoffs

| Benefício | Custo |
|---|---|
| Barata: no caso-fonte produziu uplift medido antes de qualquer fix dirigido | Delimitada: higiene não corrige modos de falha específicos, que exigem trabalho dirigido |
| Regra de bolso auditável por humano: separação legível é separação parseável | Exige owner explícito para prevenir que o rot re-acumule |
| Reutilizável em qualquer estágio de manutenção de prompt, especialmente conforme prompts crescem | Avaliações pós-higiene ainda mostram variância por caso, revalidável caso a caso |
| Estabelece o baseline limpo que torna fixes dirigidos atribuíveis | Refactor de prompt legado de 1800+ linhas é trabalho manual de leitura e classificação

## Relação com outros padrões

- **Aplica-se à superfície de:** [[docs/canonical/stable-harness-prompt|Stable Harness Prompt]]: os concerns enumerados lá (role, policy, tool contracts, safety boundaries, response format, evaluation behavior) são as seções naturais do esquema de tags; a política de blocos existente visa preservação durante context reduction, e a higiene adiciona o refactor de seccionamento.
- **Governada por:** [[docs/canonical/prompt-as-code-causal-change-management|Prompt-as-Code Causal Change Management]]: o refactor de higiene é ele mesmo uma mudança de prompt que carrega trigger (eval baseline sujo), diagnosis e intent no commit causal.
- **Endereça o gap de:** [[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]] (`:102`): o prompt de 1800+ linhas não versionado é a superfície concreta onde a higiene se aplica primeiro.
- **Habilita:** [[docs/canonical/defensive-patch-ledger|Defensive Patch Ledger]]: patches defensivos só são auditáveis quando visíveis como seções; higiene estrutural é pré-requisito de leitura do ledger.
- **Medida por:** [[docs/canonical/3-layer-evaluation-architecture|3-Layer Evaluation Architecture]]: o uplift de higiene é quantificado pela suite estratificada existente.

## Referências

- `docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-patterns.md:54-71` (seção 3): definição do padrão, esquema XML, regra de bolso, benefícios, limitações.
- `docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-classification.md:57-69` (seção 3): Partial Coverage, evidência file:line e NOT_FOUND.
- `docs/canonical/stable-harness-prompt.md:22` e `:30-39`: concerns distintos e montagem por blocos com política de redução.
- `docs/canonical/prompt-as-code-causal-change-management.md:116`: superfície concreta (prompt hand-authored de 1800+ linhas) via gap registrado em `docs/canonical/owned-agent-control-loop.md:102`.
- `docs/canonical/owned-agent-control-loop.md:102`: prompt não versionado nem eval'd como componente separado.

---

*Created: 2026-09-02 | From: The Prompting Playbook classification (Batch 1, pattern 3) | Precedence: canonical*
