---
title: "Emergent Event Topology"
type: canonical
tags: ["agentes-orquestracao", "multi-agent", "harness-engineering", "context-engineering"]
aliases: ["event topology", "topologia emergente por eventos", "zero declared edges", "choreography by typed events", "event-driven agent topology"]
last_updated: 2026-09-02
relates-to:
  - "[[docs/canonical/goal-driven-agents-over-workflows|Goal-Driven Agents over Workflows]]"
  - "[[docs/canonical/multi-agent-fault-tolerance|Multi-Agent Fault Tolerance]]"
  - "[[docs/canonical/append-only-causal-event-log|Append-Only Causal Event Log]]"
  - "[[docs/canonical/typed-event-boundaries|Typed Event Boundaries]]"
  - "[[docs/canonical/agent-as-declarative-file|Agent as Declarative File]]"
  - "[[docs/canonical/agent-specific-data-freshness-pipeline|Agent-Specific Data Freshness Pipeline]]"
sources:
  - "[[docs/analysis/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt-analysis|Analise Agent Frameworks Considered Harmful]]"
  - "[[docs/analysis/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt/classification|Classification: Agent Frameworks Considered Harmful]]"
---

# Emergent Event Topology

**Type:** Canonical Pattern
**Status:** Active (ensinado como contraste, nao como arquitetura substituta do canon orchestrator-first)
**Source:** AI Engineer — Remi Louf (.txt), "Agent Frameworks Considered Harmful" (2026-08-22)
**Classification:** Partial Coverage (P2, Medium integration value)
**Precedence:** Level 2 ([[docs/system-of-record|System of Record]])

---

## Problema

Grafos de agentes definidos em codigo — o que frameworks vendem — criam arestas para manter e restringem contribuicao a quem codifica a orquestracao (analysis.md:148-149). Cada novo participante exige editar o grafo; cada edicao do grafo e um deploy de codigo.

Este doc formaliza o reframe que o repo nao tem: agentes comunicando-se **somente** por pub/sub de eventos tipados com **zero arestas declaradas**. Sua funcao no corpus e completar o espectro orchestrator-vs-choreography que o curriculum ensina por partes, e dar mecanismo a critica de DAGs que o canon ja faz por outro caminho.

## Solucao

Nenhuma aresta declarada em codigo. Agentes apenas **publicam e assinam eventos tipados**; a topologia "emerge do que o log diz que aconteceu" (analysis.md:150-153):

| Mecanismo | Papel |
|---|---|
| Eventos tipados publicos e conhecidos | Contrato entre publicador e assinantes (schemas no registry) |
| Log de eventos | Unico registro do que aconteceu; a topologia so existe nele |
| Assinaturas no arquivo do agente | Extensao = dropar um novo arquivo de agente que conhece os eventos existentes, sem codar |
| Fan-in / fan-out | Gratis: derivam das assinaturas, nao de arestas escritas |

Pipeline real descrito em producao (analysis.md:154-159):

```text
voice note dropada → evento
  → agente transcritor (aceita nota; retorna notas duraveis + emite voice-note-processed)
  → agente daily-brief (consome saida do cron + notas duraveis)
  → produz o brief → evento slack.message.post
  → processo assinante posta no Slack
```

Nenhum ponto desse pipeline conhece o pipeline; cada no conhece apenas eventos. Zero arestas para manter; contribuicao desacoplada do codigo de orquestracao.

**Posicionamento contra o canon do repo:** o repo e orchestrator-first por decisao — [[docs/canonical/multi-agent-fault-tolerance|Multi-Agent Fault Tolerance]] canonicaliza workflows `Agent A → Agent B → Agent C` com Saga rollback e contrato por step (`:20-40`), e o orchestrator skill coordena por dashboard central (classification.md:91). Este padrao **nao substitui** esse canon: e o extremo choreography do espectro, ensinado como contraste (classification.md:94). Quando a tolerancia a falha precisa de compensacao transacional e contrato por step, o modelo orchestrator-first permanece; quando a extensibilidade por contribuicao nao-tecnica domina, o extremo emergente ganha.

## Implementacao neste repositorio

### O que ja existe

- **Canais e workers com eventos no curriculum:** tres canais de comunicacao ensinados (file-based, Redis/RabbitMQ, APIs) e workers consumindo/publicando eventos com `event_type` e `reply_to` — mas o Evaluator espera todos os resultados: coordenacao declarada, nao topologia emergente (classification.md:87).
- **Fan-out/fan-in e choreography nomeados:** fan-out/fan-in ensinado como divisao/recombinacao explicita por um orquestrador; choreography mencionada como alternativa ("um evento escutado por varios agentes") sem virar arquitetura (classification.md:88).
- **Critica filosofica alinhada:** [[docs/canonical/goal-driven-agents-over-workflows|Goal-Driven Agents over Workflows]] rejeita workflow DAG como unidade de especificacao (`:27-33`) e sustenta que "goals age better than orchestration graphs" (`:88`) — o vizinho conceitual, sem propor eventos tipados como mecanismo.
- **Pipeline event-driven especificado:** [[docs/canonical/agent-specific-data-freshness-pipeline|Agent-Specific Data Freshness Pipeline]] desenha mudanca de documento → re-ingest → re-embed com triggers tipados, declarado nao implementado (classification.md:90-91).

### O que falta

(classification.md:92) — event bus no corpus aparece so como middleware de coleta de traces e como ideia futura de "adaptive mesh":

1. **O reframe zero-arestas** com topologia reconstruida do log — nenhuma arquitetura do repo comunica apenas por eventos.
2. **Extensao por drop de arquivo** que assina schemas publicos existentes (depende de event schema registry, tambem ausente).
3. **Runtime de pub/sub ou subscription-dispatch em codigo** — nenhum broker no repo.

## Tradeoffs

| Beneficio | Custo |
|---|---|
| Zero arestas para manter | Nenhuma visao global declarada: a topologia so existe no log |
| Fan-in e fan-out gratis, das assinaturas | Descoberta depende de conhecer os eventos existentes |
| Extensao do sistema sem codar (drop de arquivo de agente) | Debug depende integralmente do log causal |
| Contribuicao desacoplada do codigo de orquestracao | Tensao declarada com o canon orchestrator-first (Saga, contrato por step) |

## Relacao com outros padroes

- **Depende de:** [[docs/canonical/typed-event-boundaries|Typed Event Boundaries]] (eventos com schema publico) e [[docs/canonical/append-only-causal-event-log|Append-Only Causal Event Log]] (o log e a unica representacao da topologia e o unico caminho de debug).
- **Habilitada por:** [[docs/canonical/agent-as-declarative-file|Agent as Declarative File]] — assinaturas de eventos como campo do arquivo declarativo tornam a extensao por drop-de-arquivo possivel.
- **Contraste com:** [[docs/canonical/multi-agent-fault-tolerance|Multi-Agent Fault Tolerance]] — orchestrator-first com Saga e contrato por step; este padrao e o extremo oposto do espectro.
- **Da mecanismo a:** [[docs/canonical/goal-driven-agents-over-workflows|Goal-Driven Agents over Workflows]] — a critica do DAG ganha uma alternativa concreta de coordenacao sem grafo.
- **Adjacente a:** [[docs/canonical/agent-specific-data-freshness-pipeline|Agent-Specific Data Freshness Pipeline]] — pipeline event-driven especificado; seria o primeiro caso de uso natural no repo.
- **Superficie de:** [[docs/canonical/cron-plus-typed-events-orchestration|Cron plus Typed Events Orchestration]] — eventos tipados sao o eixo "porque" daquela superficie.

## Referencias

- `docs/analysis/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt-analysis.md:146-159` — topologia emergente: reframe, mecanismo, pipeline real de producao.
- `docs/analysis/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt-patterns.md:81-99` — padrao 4 extraido: inputs, outputs, beneficios, limitacoes.
- `docs/analysis/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt/classification.md:80-94` — classificacao Partial Coverage (Medium) com evidencia file:line, contra-evidencia orchestrator-first e NOT_FOUND.
- [[docs/canonical/goal-driven-agents-over-workflows|Goal-Driven Agents over Workflows]]`:27-33, :88` — critica do workflow DAG e "goals age better".
- [[docs/canonical/multi-agent-fault-tolerance|Multi-Agent Fault Tolerance]]`:20-40` — canon orchestrator-first: workflow A→B→C, Saga, contrato por step.
