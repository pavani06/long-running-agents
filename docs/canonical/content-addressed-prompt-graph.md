---
title: "Content-Addressed Prompt Graph"
type: canonical
tags: ["context-engineering", "harness-engineering", "production", "evals", "agentes-orquestracao"]
aliases: ["content-addressed prompts", "prompt graph of hashes", "grafo de hashes do prompt", "prompt content addressing", "exact-input reconstruction"]
last_updated: 2026-09-02
relates-to:
  - "[[docs/canonical/prompt-as-code-causal-change-management|Prompt-as-Code with Causal Change Management]]"
  - "[[docs/canonical/stable-harness-prompt|Stable Harness Prompt During Context Reduction]]"
  - "[[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]"
  - "[[docs/canonical/graph-addressed-context-placement|Graph-Addressed Context Placement]]"
  - "[[docs/canonical/production-grounded-eval-sampling|Production-Grounded Eval Sampling]]"
  - "[[docs/canonical/failure-accrued-runtime-growth|Failure-Accrued Runtime Growth]]"
sources:
  - "[[docs/analysis/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt-analysis|Analise Agent Frameworks Considered Harmful]]"
  - "[[docs/analysis/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt/classification|Classification: Agent Frameworks Considered Harmful]]"
---

# Content-Addressed Prompt Graph

**Type:** Canonical Pattern
**Status:** Active
**Source:** AI Engineer — Remi Louf (.txt), "Agent Frameworks Considered Harmful" (2026-08-22)
**Classification:** Partial Coverage (P1, High integration value)
**Precedence:** Level 2 ([[docs/system-of-record|System of Record]])

---

## Problema

E impossivel saber o que efetivamente entrou no contexto do modelo. A sessao de chat **nao representa o prompt real**: compaction faz o contexto renderizado diferir do enviado, quirks de provider escondem detalhes de montagem, e thinking traces nao sao compartilhados — voce "tem uma ideia" do que entrou, nunca a certeza (analysis.md:68-79). Consequencias: prompts mudam sem rastro, compaction vira manipulacao de strings, e a regressao fica irreproduzivel — no caso-fonte, um market brief "virou lixo" apos uma semana de tweaks de prompt sem que ninguem conseguisse lembrar qual mudanca quebrou (analysis.md:207).

O repo versiona prompts em granularidade de commit e exige versao de prompt no replay, mas versionamento git responde "qual texto estava deployado em T", nao "que componentes exatos compuseram o input renderizado desta run" (classification.md:44).

## Solucao

Enderecar cada componente do prompt por **hash de conteudo** (estilo git/Nix) e representar o prompt como **grafo de hashes antes da renderizacao em texto** (analysis.md:113-124):

1. Decompor o prompt em partes: system prompt, descricao de cada skill, descricao de cada tool, user message.
2. Armazenar cada parte enderecada por hash de conteudo.
3. Antes de renderizar texto, o prompt e uma lista/grafo de hashes.
4. Armazenar a resposta do modelo no mesmo esquema: toda resposta traca de volta ao prompt exato, e do prompt ao conteudo exato do contexto.

Um unico primitivo, varias capacidades de graca (analysis.md:125-135):

| Capacidade | Mecanismo |
|---|---|
| Debug | Reconstrucao exata do input do modelo |
| Diffs entre runs | Funcao que mostra qual componente mudou (user message? skill? tool?) e quais runs eram continuacao da mesma sessao |
| Replay | Reconstruir a request do grafo e reenviar identica — com outro modelo ou modificada (caso relatado: trocar por open-source ao ver o custo subir) |
| Compaction | Manipulacao de grafo, nao de strings |
| KV cache | Management "indiretamente" mais facil |
| Auditabilidade | Em escala: saber exatamente o que aconteceu e porque o agente retornou o que retornou |

## Implementacao neste repositorio

### O que ja existe

Os vizinhos cobrem versionamento, enderecamento e endereco por grafo, cada um por um mecanismo que **nao** e content addressing:

- [[docs/canonical/prompt-as-code-causal-change-management|Prompt-as-Code with Causal Change Management]]: prompts como artefatos versionados em git com commit causal (`:28`); rollback por `git revert` e deploy por commit (`:80-85`); audit trail responde "what was the exact prompt text deployed" por ponto no tempo **via historico git** (`:100-105`) — granularidade de commit, nao de hash de conteudo.
- [[docs/canonical/stable-harness-prompt|Stable Harness Prompt During Context Reduction]]: replay exige versoes de prompt, rubric, catalog e schema (`:52`); metadados de versao de prompt em artefatos de replay (`:62`) — exige a versao, nao reconstrói o prompt exato.
- [[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]: `id`/`kind`/`location`/`preview`/`scope`/`tool`/`path` estaveis por peca de contexto omitida (`:28-43`) — enderecamento por ID de catalogo, nao por hash de conteudo.
- [[docs/canonical/graph-addressed-context-placement|Graph-Addressed Context Placement]]: conhecimento ancorado em nos do grafo de software, retrieval por traversia (classification.md:52) — grafo como endereco de contexto, nao de componentes de prompt.
- [[docs/canonical/production-grounded-eval-sampling|Production-Grounded Eval Sampling]]: replay de interacoes reais representativas (classification.md:53) — replay de conversa, nao reconstrucao do prompt exato por hashes.

### O que falta

(classification.md:54) — greps por `content-address` e `hash` em `docs/canonical/`, `docs/decisions/`, `curriculum/`, `.opencode/` nao encontram nada fora do proprio pacote-fonte:

1. **Funcao de hash sobre componentes de prompt** (system/skill/tool/user) e armazenamento enderecado por conteudo.
2. **Prompt como grafo de hashes antes da renderizacao**, com resposta ligada ao prompt exato que a produziu.
3. **Diffs por componente entre runs** e replay identico do input exato (troca de modelo por custo com verificacao de satisfatoriedade).
4. **Compaction como manipulacao de grafo** em vez de edicao de strings.

## Tradeoffs

| Beneficio | Custo |
|---|---|
| Debug por reconstrucao exata do input do modelo | "Deep rabbit hole": investimento grande, na palavra do proprio autor |
| Regressao de prompt rastreavel (qual mudanca quebrou o output) | Nasceu de uma falha de producao, nao de um plano: exige a dor antes da peca |
| Troca de modelo por custo com replay identico e avaliacao da saida | Exige disciplina de content addressing em toda peca de prompt, sem excecoes |
| Compaction como manipulacao de grafo; KV cache mais facil | Duplicacao de armazenamento por conteudo (garbage collection de nos mortos) |

## Relacao com outros padroes

- **Fundamenta mecanicamente:** [[docs/canonical/prompt-as-code-causal-change-management|Prompt-as-Code with Causal Change Management]] (commit causal por cima do endereco estavel) e [[docs/canonical/stable-harness-prompt|Stable Harness Prompt During Context Reduction]] (a versao exigida no replay passa a ser reconstructivel por hashes).
- **Complementa:** [[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]] (catalogo endereca o que foi omitido; hashes enderecam o que entrou) e [[docs/canonical/graph-addressed-context-placement|Graph-Addressed Context Placement]] (grafo de software para colocacao; grafo de hashes para composicao).
- **Da substrato a:** [[docs/canonical/production-grounded-eval-sampling|Production-Grounded Eval Sampling]] — replay representativo vira replay de input exato.
- **E peca justificada por falha em:** [[docs/canonical/failure-accrued-runtime-growth|Failure-Accrued Runtime Growth]] — o mapa falha-de-producao → primitiva inclui "regressao irreproduzivel → prompts content-addressed".

## Referencias

- `docs/analysis/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt-analysis.md:68-79` — o chat e uma mentira: compaction, quirks de provider, thinking traces ocultos.
- `docs/analysis/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt-analysis.md:113-135` — mecanismo do grafo de hashes e capacidades derivadas.
- `docs/analysis/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt-patterns.md:38-59` — padrao 2 extraido: inputs, outputs, beneficios, limitacoes.
- `docs/analysis/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt/classification.md:40-56` — classificacao Partial Coverage (High) com evidencia file:line e NOT_FOUND.
- [[docs/canonical/prompt-as-code-causal-change-management|Prompt-as-Code with Causal Change Management]]`:28, :80-85, :100-105` — versionamento por commit causal, rollback, audit trail via git.
- [[docs/canonical/stable-harness-prompt|Stable Harness Prompt During Context Reduction]]`:52, :62` — versoes exigidas no replay; metadados de versao em artefatos de replay.
- [[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]`:28-43` — catalogo de memoria omitida enderecada por ID.
