---
title: "Context as Code (Meta Harness)"
type: canonical
aliases: ["context as code", "context base", "meta harness"]
tags: ["context-engineering", "agent-context", "documentation-as-code", "repo-as-context"]
last_updated: 2026-09-14
relates-to: ["[[docs/canonical/agent-as-declarative-file|Agent as Declarative File]]", "[[docs/canonical/error-context-hygiene|Error Context Hygiene]]", "[[docs/decisions/2026-09-14-evidence-provenance-non-collapse|Evidence Provenance Non-Collapse]]", "[[docs/system-of-record|System of Record]]"]
sources: ["75M Founder Reveals His Agentic Engineering Setup (YouTube, QBfXiWvM0qc)"]
---
# Context as Code (Meta Harness)

**Type:** Canonical Pattern
**Status:** Active
**Source:** "75M Founder Reveals His Agentic Engineering Setup" (YouTube), adapted for long-running-agents
**Classification:** Missing como *padrão nomeado* na camada canônica; **já materializado na prática** ao longo do repo (originado da análise `docs/analysis/2026-09-11-75m-founder-reveals-his-agentic-engineering-setup/`). Este doc **nomeia e reforça** uma prática existente — não a introduz do zero.
**Precedence:** Level 2 (`docs/system-of-record.md`)

---

## Problema

Repositórios ricos em código mas pobres em significado são indigestos para agentes de IA: sem artefatos que expliquem *por que* cada feature existe, o agente infere intenção a partir da implementação, gerando respostas genéricas, mudanças que violam decisões de design e perda de contexto em sessões longas. O conhecimento fica implícito na cabeça dos mantenedores ou em canais efêmeros.

## Mecanismo

Tratar o repositório como um *context base*, não apenas como um *code base*:

- **Artefatos de significado versionados** junto ao código: padrões curados, decisões de arquitetura, currículo e modelos mentais do domínio.
- **Parseabilidade**: estrutura previsível (frontmatter + cabeçalhos + campos fixos) para que agentes localizem e carreguem só o contexto relevante.
- **Sincronização validável**: mudança de comportamento exige atualizar o artefato correspondente; o contexto é validável por lint/CI tanto quanto o código.
- **Inversão de investimento**: mais engenharia na curadoria do contexto (intenção, restrições, critérios) do que na execução manual — o agente executa; o humano curadoria o contexto.

## Como este repositório já pratica

Este repo **já é** um context base; o padrão nomeia o que ele faz e aponta onde endurecer. Camadas de contexto existentes:

- **`docs/canonical/`** — 100+ padrões curados (este próprio doc): a camada de significado sobre o código, cada um com problema/mecanismo/trade-offs e `relates-to`.
- **`docs/decisions/`** — ADRs registram o *porquê* de decisões (ex.: [[docs/decisions/2026-09-14-evidence-provenance-non-collapse|Evidence Provenance Non-Collapse]]).
- **`curriculum/`** — lições e exercícios por nível, transformando padrões em forma aprendível.
- **`mapa-mental-repo/`** — modelos mentais por fonte, destilando contexto do corpus bruto.
- **`docs/system-of-record.md`** — precedência/ordenação entre essas camadas de contexto.
- **Convenções de frontmatter + `validate-obsidian`** — a propriedade "parseável + lintável" que o mecanismo exige, já aplicada aos docs.
- **`scripts/analyze-and-improve/`** — o índice semântico e o pipeline que *consomem* esses artefatos (retrieval por seção), fechando o laço "contexto usado, não só armazenado".

Padrões relacionados que já expressam a mesma tese: [[docs/canonical/agent-as-declarative-file|Agent as Declarative File]] (o agente definido como arquivo) e [[docs/canonical/error-context-hygiene|Error Context Hygiene]] (higiene do contexto em falhas).

## Trade-offs

- **Custo upfront**: exige disciplina para escrever e manter o contexto estruturado.
- **Competição com entrega**: a curadoria do contexto disputa o tempo de features; sem patrocínio, degrada.
- **Teto de qualidade**: o output do agente não supera a qualidade do contexto — contexto stale produz mudanças confiantes e erradas.
- **Risco de cerimônia**: artefatos não consumidos por nenhum fluxo (agente, revisão, onboarding) viram burocracia morta.

## O que falta endurecer

Ancoradas no mecanismo acima, as lacunas concretas neste repo (não novos conceitos, apenas pontos de disciplina já implícitos):

- **Gate de sincronização**: hoje nada obriga um PR que altera comportamento a atualizar o artefato de contexto correspondente — a sincronização é convenção, não CI.
- **Caminho de consumo explícito**: o `analyze-and-improve` já indexa docs; falta tornar explícito *quais* artefatos cada fluxo de agente carrega (prompt de sistema, indexação seletiva) para garantir consumo, não só armazenamento.
