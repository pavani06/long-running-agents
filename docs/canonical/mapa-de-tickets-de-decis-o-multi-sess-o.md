---
title: Mapa de tickets de decisão multi-sessão
type: canonical
aliases:
- mapa de tickets de decisão multi-sessão
tags:
- context-engineering
last_updated: '2026-09-15'
relates-to: []
sources:
- 2026-09-11-wayfinder-nothing-is-too-big-to-plan-anymore--F3lL98Pj90o.md
---

# Mapa de tickets de decisão multi-sessão

**Type:** Canonical Pattern
**Source:** `2026-09-11-wayfinder-nothing-is-too-big-to-plan-anymore--F3lL98Pj90o.md` — adaptado para long-running-agents
**Classification:** Missing — ausente no repo; originado da análise da fonte (padrão: Mapa de tickets de decisão multi-sessão).

---

## Problema

Trabalhos grandes demais para caber na smart zone da context window de um agente forçam quebra manual do planejamento, gerenciamento manual de tokens e redução do escopo por limite de memória, não por limite de ambição. O planejamento fica acorrentado a uma única sessão: quando o contexto enche, o plano morre com ele.

## Mecanismo

Representar o planejamento como um **grafo de tickets de decisão** em um issue tracker agnóstico (GitHub Issues, Linear, Jira), com relações de bloqueio entre tickets (este ticket depende daquele). O grafo é gerenciado ao longo de **múltiplas sessões**: cada sessão resolve alguns tickets de decisão, reduzindo progressivamente a "fog of war" — as partes desconhecidas do trabalho. Cada ticket, ao ser resolvido, converte incerteza em decisão registrada fora da context window.

Regra central: tickets de **decisão** ("qual formato de armazenamento?", "o que bloqueia o quê?") são distintos de tickets de **implementação** ("criar tabela X"). O mapa de decisão produz uma spec; a spec é um **documento-destino temporário** — descartada quando o código a incorpora. O estado durável é o grafo no tracker, não o documento.

## Trade-offs

- **Overhead para trabalhos pequenos.** Se o trabalho cabe numa sessão, o mapa é burocracia; planeje direto na sessão.
- **Disciplina taxonômica.** Misturar tickets de decisão com tickets de implementação degrada o grafo num backlog comum, perdindo a função de reduzir incerteza.
- **Custo de manutenção.** Relações de bloqueio precisam ser mantidas à mão quando a realidade muda.
- **Dependência do tracker.** A portabilidade exige que o mecanismo não codifique idiossincrasias de um tracker específico.

## Como se aplicaria aqui

O repo já ensina as peças que este padrão conecta, mas não as conecta: `curriculum/05-core-concepts/02-planning-execution-separation.md` argumenta que o Planner precisa de contexto limpo e que replanning deve ser isolado — exatamente o que um mapa externo de tickets de decisão fornece ao persistir decisões fora da sessão. `curriculum/06-knowledge-graphs/02-koda-feature-dependencies.md` apresenta dependências como arestas documentadas num grafo e planejamento como consulta ao mapa — a mesma estrutura, aplicada a features em vez de decisões. `curriculum/03-nivel-3-advanced-architecture/01-multi-agent-systems.md` cobre decomposição vertical em issues, que é a contraparte de implementação: este padrão definiria a camada de decisão que precede e alimenta essas fatias verticais. Finalmente, `docs/canonical/append-only-causal-event-log.md` trata do mesmo problema de raiz — estado perdido entre passos — mas na execução; o mapa de tickets é o análogo no planejamento. Uma doc canônica aqui deveria posicioná-lo como a ponte entre o grafo de conhecimento do módulo 06 e a separação planejar/executar do módulo 05, com a regra explícita: mapa de decisão se a incerteza não cabe numa sessão; sessão única se cabe.
