---
title: "Typed Event Boundaries"
type: canonical
tags: ["agentes-orquestracao", "harness-engineering", "multi-agent", "error-handling", "agent-loop"]
aliases: ["typed event boundary", "fronteira de eventos tipados", "agent-agent event contract", "event schema boundary", "typed tool and event boundaries"]
last_updated: 2026-09-02
relates-to:
  - "[[docs/canonical/structured-generation-constraint-validation-circuit|Structured Generation and Constraint Validation Circuit]]"
  - "[[docs/canonical/deterministic-tool-dispatch|Deterministic Tool Dispatch]]"
  - "[[docs/canonical/agent-to-agent-review-comment-protocol|Agent-to-Agent Review Comment Protocol]]"
  - "[[docs/canonical/agent-kernel-runtime|Agent Kernel Runtime]]"
  - "[[docs/canonical/append-only-causal-event-log|Append-Only Causal Event Log]]"
  - "[[docs/canonical/emergent-event-topology|Emergent Event Topology]]"
sources:
  - "[[docs/analysis/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt-analysis|Analise Agent Frameworks Considered Harmful]]"
  - "[[docs/analysis/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt/classification|Classification: Agent Frameworks Considered Harmful]]"
---

# Typed Event Boundaries

**Type:** Canonical Pattern
**Status:** Active
**Source:** AI Engineer — Remi Louf (.txt), "Agent Frameworks Considered Harmful" (2026-08-22)
**Classification:** Partial Coverage (P1, High integration value)
**Precedence:** Level 2 ([[docs/system-of-record|System of Record]])

---

## Problema

Acoes invalidas do modelo atravessam o runtime sem serem barradas: chamar uma tool inexistente na fronteira agente-ferramentas, ou emitir um evento fora do schema na fronteira agente-agentes. No caso-fonte, com modelos fracos em structured outputs, ~20% dos eventos eram rejeitados somente depois de publicados (analysis.md:102-104), ou seja, a deteccao acontecia tarde demais para impedir o efeito.

O repo cobre a fronteira agente-ferramentas em profundidade canonica, mas a fronteira agente-agentes nao existe como contrato geral: o que um agente aceita e o que retorna para outros agentes e convencao implicita de payload, nao schema declarado e validado (classification.md:26, :34).

## Solucao

Formalizar **duas** fronteiras tipadas com o mundo externo do agente, ambas validadas por schema no kernel, ambas rejeitando carga nao-conforme **antes de produzir efeito**:

| Fronteira | Contrato | Validador |
|---|---|---|
| Agente-ferramentas (typed tool calls) | Schema de input por tool; retorno tipado | Kernel valida o tool call antes do dispatch |
| Agente-agentes (typed events) | Cada agente **declara** os eventos que aceita e os que retorna; structured outputs como contrato de saida | Kernel valida o evento no publish e no consume |

Postura "non-negotiable": o kernel existe para tornar acoes ruins **impossiveis, nao improvaveis** (analysis.md:109-111). A fronteira rejeita, nao corrige: um modelo ruim em structured outputs continua gerando carga rejeitada; o que muda e que essa carga nunca produz efeito.

Declaracao por agente, no formato do proprio agente declarativo:

```yaml
# trecho do arquivo do agente transcritor
events:
  accepts:  [{ schema: voice-note.dropped,  version: 1 }]
  returns:  [{ schema: voice-note.processed, version: 1 },
             { schema: durable-notes.created, version: 2 }]
```

O contrato e consultavel: qualquer agente (ou humano) pode ler o que o outro aceita e retorna antes de publicar. Contratos tipados entre agentes substituem convencoes implicitas de payload (classification.md:32).

## Implementacao neste repositorio

### O que ja existe

A fronteira de saida do modelo e a fronteira de tool call estao cobertas:

- [[docs/canonical/structured-generation-constraint-validation-circuit|Structured Generation and Constraint Validation Circuit]]: circuito de acao-segura com output schema, constraint set de dominio, validador pos-geracao e politica de repair/reject (`:29`); shape validation seguida de domain constraint validation com reject/repair/flag/fallback (`:61-63`) — o lado output do boundary, com a mesma postura de rejeitar antes do efeito.
- [[docs/canonical/deterministic-tool-dispatch|Deterministic Tool Dispatch]]: "Every tool is a `DynamicStructuredTool` with Zod schema input and typed return" (`:74`); dispatch construido sobre o structured output contract (`:107`) — o lado tool-input do boundary.
- [[docs/canonical/agent-to-agent-review-comment-protocol|Agent-to-Agent Review Comment Protocol]]: o analogo agent-agent mais proximo, "sem um formato agent-parseable o loop fecha no humano em vez de fechar no proximo agente" (`:37`) — porem escopado a comentarios de review, nao a schemas de evento gerais.

### O que falta

(classification.md:34) — NOT_FOUND de per-agent event schemas e validador em ambas as fronteiras; greps por `typed event`, `eventos tipados`, `input schema`, `output schema` em `docs/canonical/`, `docs/decisions/`, `docs/evidence/`, `curriculum/`, `.opencode/` cobrem apenas validacao de output de modelo e input de tool:

1. **Declaracao por agente de eventos aceitos/retornados** — nenhum formato de agente do repo declara contratos de evento.
2. **Validador de kernel aplicado a AMBAS as fronteiras** — rejeitar evento nao-conforme no publish/consume antes do efeito, simetrico ao que o circuito de validacao faz para output de modelo.
3. **A extensao do reframe "impossivel, nao improvavel" para eventos entre agentes** — hoje o reframe existe para output (circuito) e tool input (dispatch), nao para a fronteira inter-agente.

## Tradeoffs

| Beneficio | Custo |
|---|---|
| Acoes ruins tornam-se impossiveis, nao apenas improvaveis (postura do kernel) | Custo de schema e validacao em toda fronteira, em toda chamada |
| Elimina a perda de ~20% de eventos invalidos observada antes das fronteiras | Acoplamento a stack de structured outputs do provider |
| Contratos tipados entre agentes substituem convencoes implicitas de payload | A fronteira rejeita, nao corrige: modelo ruim em structured outputs segue gerando carga rejeitada |

## Relacao com outros padroes

- **Completa:** [[docs/canonical/structured-generation-constraint-validation-circuit|Structured Generation and Constraint Validation Circuit]] (fronteira de saida do modelo) e [[docs/canonical/deterministic-tool-dispatch|Deterministic Tool Dispatch]] (fronteira de tool input) — este padrao fecha o triangulo com a fronteira agente-agentes.
- **Generaliza:** [[docs/canonical/agent-to-agent-review-comment-protocol|Agent-to-Agent Review Comment Protocol]] — o comentario parseable e um caso particular de evento tipado entre agentes.
- **E substrato de:** [[docs/canonical/append-only-causal-event-log|Append-Only Causal Event Log]] e [[docs/canonical/emergent-event-topology|Emergent Event Topology]] (ambos assumem eventos com schema conhecido), e da superficie de orquestracao de [[docs/canonical/cron-plus-typed-events-orchestration|Cron plus Typed Events Orchestration]].
- **Executada por:** [[docs/canonical/agent-kernel-runtime|Agent Kernel Runtime]] — o validador de fronteiras e uma responsabilidade do kernel, nao do agente.

## Referencias

- `docs/analysis/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt-analysis.md:100-111` — fronteiras tipadas: problema (~20% rejeitados), mecanismo das duas fronteiras, postura non-negotiable.
- `docs/analysis/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt-patterns.md:17-36` — padrao 1 extraido: inputs, outputs, beneficios, limitacoes.
- `docs/analysis/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt/classification.md:22-36` — classificacao Partial Coverage (High) com evidencia file:line e NOT_FOUND.
- [[docs/canonical/structured-generation-constraint-validation-circuit|Structured Generation and Constraint Validation Circuit]]`:29, :61-63` — circuito output-side com rejeicao antes do efeito.
- [[docs/canonical/deterministic-tool-dispatch|Deterministic Tool Dispatch]]`:74, :107` — Zod schema input e typed return; baseado no structured output contract.
- [[docs/canonical/agent-to-agent-review-comment-protocol|Agent-to-Agent Review Comment Protocol]]`:37` — analogo agent-agent escopado a review comments.
