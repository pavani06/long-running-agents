---
title: "Human-Review Staged Workflow Automation"
type: canonical
tags: ["agentes-orquestracao", "production", "governanca"]
Status: Active
Source: "AI Engineer talk — Sait Izmit, Snowflake (GTM assistant: 5-6 conexões MCP, ~20 skills)"
Classification: "Partial Coverage (P2, Medium integration value)"
Precedence: "Level 2 (docs/system-of-record.md)"
last_updated: 2026-08-30
aliases: ["staged workflow automation", "human-owned send", "monitor draft review send", "reviewed-draft automation"]
relates-to:
  - "[[docs/canonical/autonomy-curriculum-sampling|Autonomy Curriculum Sampling]]"
  - "[[docs/canonical/domain-embedded-workflow-automation-wedge|Domain-Embedded Workflow Automation Wedge]]"
  - "[[docs/canonical/human-afk-task-routing-gate|Human-AFK Task Routing Gate]]"
  - "[[docs/canonical/tested-degradation-ladder|Tested Degradation Ladder]]"
  - "[[docs/canonical/manual-brake-question-gate|Manual Brake Question Gate]]"
  - "[[docs/canonical/agent-value-maturity-ladder|Agent Value Maturity Ladder]]"
  - "[[docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-analysis|GTM AI Agents Analysis]]"
sources:
  - "[[docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-patterns|GTM AI Agents Patterns]]"
  - "[[docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-classification|GTM AI Agents Classification]]"
---

# Human-Review Staged Workflow Automation

**Type:** Canonical Pattern
**Status:** Active
**Source:** AI Engineer talk — Sait Izmit, Snowflake (GTM assistant: monitor de inbox/Slack → draft em Gmail → revisão humana → envio humano)
**Classification:** Partial Coverage (P2, Medium integration value)
**Precedence:** Level 2 ([[docs/system-of-record|System of Record]])

---

## Problema

Data Q&A sozinho topo no estágio de valor "talk to your data", enquanto ações outbound totalmente autônomas são inseguras de confiar ao agente no dia um (`docs/analysis/...-patterns.md:247-250`). O dilema aparente: ou o agente responde perguntas (valor baixo, risco baixo), ou age sozinho (valor alto, risco inaceitável).

O falso dilema esconde o degrau que falta: automação de **ação externa com envio irreversível propriedade do humano**. Sem esse degrau, times ou estagnam no Q&A (o agente nunca cruza de insight para ação) ou queimam confiança com envios autônomos prematuros.

Nota de escopo repo: os gates de review do repo protegem decisões de código/merge — não ações externas de saída. A classificação registra: "Repo review gates protect code/merge decisions, not outbound external actions" (classification:249-254).

## Solução

Workflows em estágios para ações externas: o agente **monitora canais, rascunha respostas, e o humano revisa e envia** (`docs/analysis/...-patterns.md:256-259`).

| Componente | Função |
|---|---|
| Channel monitors | Agente monitora inbox e Slack carregando perguntas de clientes sobre produtos |
| Conexões MCP | 5-6 sistemas externos (leitura de canais, escrita de drafts) |
| Draft target | O agente escreve o rascunho da resposta em Gmail — sem enviar |
| Human review gate | O vendedor revisa o rascunho |
| Send action (human-owned) | O envio irreversível é sempre executado pelo humano |

Fluxo (`docs/analysis/...-patterns.md:274-280`): agente monitora inbox/Slack → detecta perguntas de clientes sobre produtos → rascunha resposta em Gmail → humano revisa → humano envia → agente automatiza progressivamente o follow-up em estágios subsequentes.

As duas propriedades que carregam o padrão:

1. **O envio irreversível permanece humano.** O review não é fase transitória a ser "otimizada" — é o freio de segurança permanente para a classe de ação irreversível (eco do gate de pergunta-freio em [[docs/canonical/manual-brake-question-gate|Manual Brake Question Gate]]).
2. **Usuários auto-adotaram o fluxo em estágios como trust builder** (`docs/analysis/...-patterns.md:261`) — cada estágio de revisão constrói a confiança que justifica o seguinte, alimentando a escada de valor (padrão Agent Value Maturity Ladder, estágio 2).

## Implementação neste repositório

### O que já existe

O gate de review humano e a autonomia graduada existem em profundidade canônica (classification:223-254):

- **Progressão graduada:** [[docs/canonical/autonomy-curriculum-sampling|Autonomy Curriculum Sampling]] — "Phase progression | Observe (human does, agent watches) -> Assist (agent proposes, human approves) -> Own (agent executes, human monitors exceptions)" (`docs/canonical/autonomy-curriculum-sampling.md:60`).
- **Preservação de review operator-side:** [[docs/canonical/domain-embedded-workflow-automation-wedge|Domain-Embedded Workflow Automation Wedge]] — "Preserve operator review for cases where authority, risk, or missing data makes full automation unsafe" (`docs/canonical/domain-embedded-workflow-automation-wedge.md:47`).
- **Roteamento por segurança:** [[docs/canonical/human-afk-task-routing-gate|Human-AFK Task Routing Gate]] — "The gate classifies every task as AFK-ready (safe for autonomous agent execution) or human-in-loop (requires human judgment before, during, or after execution)" (`docs/canonical/human-afk-task-routing-gate.md:30`).
- **Escalação humana com contexto:** [[docs/canonical/tested-degradation-ladder|Tested Degradation Ladder]] — "escalates to a human with summarized context when automated recovery is insufficient, logs the outcome, and tests each rung before production reliance" (`docs/canonical/tested-degradation-ladder.md:29`).
- **Freio antes de ações irreversíveis:** [[docs/canonical/manual-brake-question-gate|Manual Brake Question Gate]] — interrupção obrigatória antes de ações irreversíveis do agente.

### O que falta

(classification:243-254) — busca da classificação: automação faseada de ações externas com envio humano (monitor → draft → review → send), channel monitors, ou staging de valor insight→ação em `docs/canonical/`, `curriculum/`, `.opencode/skills/` (`draft|send|inbox|Slack|channel monitor`; `MCP` — zero matches em `docs/canonical/`):

1. **O reframe de staging de valor** — automação de draft revisado para ações externas como **segundo degrau deliberado de valor** além de data Q&A, com o envio irreversível humano.
2. **Channel monitors** — monitoramento de inbox/Slack como superfície de entrada do agente; o repo não tem padrão de monitor de canal.
3. **Conexões MCP** — zero presença de MCP no corpus canônico; o mecanismo de integração com sistemas externos não existe aqui.
4. **Auto-adoção do fluxo em estágios como trust builder** — a dinâmica comportamental de usuários escolhendo o fluxo revisado não está registrada.

## Tradeoffs

| Benefício | Custo |
|---|---|
| Move valor de insight para ação sem confiar envios irreversíveis ao agente | Humano no loop limita throughput |
| Review humano como freio de segurança; vendedores auto-adotaram o fluxo | Qualidade do review depende da UI de drafting e da diligência do revisor |
| Cada estágio constrói a confiança que justifica o próximo | Cada sistema externo exige conexão MCP primeiro |
| Follow-up automatiza progressivamente em estágios posteriores | Inseguro se estágios forem pulados prematuramente |

## Relação com outros padrões

- **Instancia:** [[docs/canonical/autonomy-curriculum-sampling|Autonomy Curriculum Sampling]] — o fluxo monitor→draft→review→send é a fase Assist (proposta+aprovação) aplicada a ações externas, com o envio como exceção permanente de human-in-loop.
- **Aplica a regra de:** [[docs/canonical/domain-embedded-workflow-automation-wedge|Domain-Embedded Workflow Automation Wedge]] (`:47`) — review preservado onde autoridade/risco torna automação total insegura.
- **Roteia por:** [[docs/canonical/human-afk-task-routing-gate|Human-AFK Task Routing Gate]] — a classificação AFK/human-in-loop decide quais estágios podem avançar.
- **Compartilha o princípio de:** [[docs/canonical/manual-brake-question-gate|Manual Brake Question Gate]] (irreversibilidade exige freio humano) e [[docs/canonical/tested-degradation-ladder|Tested Degradation Ladder]] (escalação humana com contexto, degraus testados).
- **É o estágio 2 de:** [[docs/canonical/agent-value-maturity-ladder|Agent Value Maturity Ladder]] — "Automate my workflows (MCP orchestration; pattern 8)" (`docs/analysis/...-patterns.md:418`).

## Referências

- `docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-patterns.md:247-280` — padrão extraído: monitor→draft→review→send, componentes, fluxo, auto-adoção.
- `docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-classification.yaml:223-254` — classificação Partial Coverage (Medium) com NOT_FOUND de draft/send/inbox/Slack/MCP.
- `docs/canonical/autonomy-curriculum-sampling.md:60` — progressão observe→assist→own.
- `docs/canonical/domain-embedded-workflow-automation-wedge.md:47` — preservar review operator.
- `docs/canonical/human-afk-task-routing-gate.md:30` — classificação AFK-ready vs. human-in-loop.
- `docs/canonical/tested-degradation-ladder.md:29` — escalação humana com contexto resumido.
