---
title: "Gap-to-Content Feedback Circuit"
type: canonical
tags: ["knowledge-management", "evals", "production", "agentes-orquestracao", "agentic-coding"]
Status: Active
Source: "AI Engineer talk — Sait Izmit, Snowflake (GTM assistant: battle cards geradas em minutos)"
Classification: "Partial Coverage (P2, Medium integration value)"
Precedence: "Level 2 (docs/system-of-record.md)"
last_updated: 2026-08-30
aliases: ["gap-to-content loop", "battle card generation", "enablement feedback circuit", "content flywheel"]
relates-to:
  - "[[docs/canonical/llm-classified-log-taxonomy|LLM-Classified Log Taxonomy]]"
  - "[[docs/canonical/on-policy-rollout-feedback-loop|On-Policy Rollout Feedback Loop]]"
  - "[[docs/canonical/production-contact-training-loop|Production-Contact Training Loop]]"
  - "[[docs/canonical/confidence-gated-continual-learning|Confidence-Gated Continual Learning]]"
  - "[[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]]"
  - "[[docs/canonical/qa-to-backlog-feedback-loop|QA-to-Backlog Feedback Loop]]"
  - "[[docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-analysis|GTM AI Agents Analysis]]"
sources:
  - "[[docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-patterns|GTM AI Agents Patterns]]"
  - "[[docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-classification|GTM AI Agents Classification]]"
---

# Gap-to-Content Feedback Circuit

**Type:** Canonical Pattern
**Status:** Active
**Source:** AI Engineer talk — Sait Izmit, Snowflake (GTM assistant: 1M+ perguntas, gaps de conhecimento detectados em logs)
**Classification:** Partial Coverage (P2, Medium integration value)
**Precedence:** Level 2 ([[docs/system-of-record|System of Record]])

---

## Problema

Gaps de conhecimento (ex.: um lançamento de produto novo) tradicionalmente exigem ~100 entrevistas de vendedores por semana para detectar e documentar — um loop que humanos não sustentam (`docs/analysis/...-patterns.md:376-379`).

O instante concreto: um novo produto é lançado. Vendedores começam a receber perguntas que ninguém sabe responder; o conhecimento existe disperso em Confluence, Jira, Slack e PRDs; a documentação de enablement (battle cards) chega semanas depois, quando já está defasada; e o agente — que responde essas mesmas perguntas — não fica sabendo de nada. Três consumidores do mesmo gap (vendedores, time de enablement, agente) com três loops manuais independentes.

## Solução

Fechar o circuito **do gap classificado ao conteúdo gerado, e do conteúdo de volta ao agente** (`docs/analysis/...-patterns.md:381-405`):

| Componente | Função |
|---|---|
| Query de tópicos emergentes | Interroga a taxonomia de logs classificados por tópicos novos ou sem resposta |
| Ingestão de fontes | Confluence, Jira, Slack, PRDs — o conhecimento interno disperso |
| Gerador de conteúdo | Battle cards e docs de enablement gerados em minutos |
| Canal de feed-back | O conteúdo gerado volta ao agente como conhecimento |

Fluxo (`docs/analysis/...-patterns.md:400-405`): query nos logs classificados por tópicos emergentes/não respondidos → ingerir as fontes internas relacionadas → gerar battle cards e docs de enablement em minutos → **alimentar o conteúdo de volta ao agente como conhecimento** → confirmar o fechamento do gap nos logs subsequentes.

Três propriedades distinguem o circuito dos loops de melhoria comuns (`docs/analysis/...-patterns.md:385-394`):

1. **Artefato duplo**: o mesmo conteúdo serve ao humano (enablement) e ao agente (conhecimento) — uma geração, dois consumidores sincronizados da mesma fonte.
2. **Trigger demand-side**: o que dispara o circuito é demanda medida (classificação de logs), não palpite de roadmap.
3. **Confirmação de fechamento**: o circuito só fecha quando os logs subsequentes mostram o gap fechado — o próprio instrumento de detecção é o verificador.

Riscos declarados: qualidade de ingestão varia entre fontes; conteúdo gerado precisa de review antes de voltar ao agente; risco de **feedback echo** — as respostas do próprio agente moldam os logs de perguntas futuros, amplificando vieses.

## Implementação neste repositório

### O que já existe

Múltiplos circuitos gap→melhoria existem como canonical — mas os artefatos de update são eval cases, políticas ou itens de backlog, não conteúdo de enablement (classification:324-347):

- [[docs/canonical/on-policy-rollout-feedback-loop|On-Policy Rollout Feedback Loop]] — "scored prefixes fed back as update targets (prompt rules, skills, eval cases, memory policy)" (`:41`).
- [[docs/canonical/production-contact-training-loop|Production-Contact Training Loop]] — "expose, harvest, feed back as updates, redeploy, repeat" (`:37`); loop diário montado (`:39-54`); peças faltantes declaradas (`:69-75`).
- [[docs/canonical/confidence-gated-continual-learning|Confidence-Gated Continual Learning]] — "four-stage detect-suggest-review-deploy loop, confidence-gated (closest structural analog)" (`:32`).
- [[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]] — "production failures become durable eval regression cases" (`:28`).
- [[docs/canonical/qa-to-backlog-feedback-loop|QA-to-Backlog Feedback Loop]] — "capture, triage, convert, return-to-board" (`:30-44`); gap de conversão estruturada declarado (`:57-59`).
- Ferramentagem repo-side: skill analyze-and-improve — pipeline automatizado knowledge→content para o próprio repositório (`docs/system-of-record.md:46`).

### O que falta

(classification:340-347) — NOT_FOUND para `battle card`, `enablement`, `gap-to-content`, `feedback circuit` em `docs/`, `curriculum/`, `.opencode/` (apenas o pacote-fonte tem matches):

1. **O trigger demand-side de logs classificados** — nenhum circuito existente dispara a partir de demanda medida (depende de [[docs/canonical/llm-classified-log-taxonomy|LLM-Classified Log Taxonomy]] upstream).
2. **O artefato de conteúdo de enablement gerado** — battle cards como output de pipeline; os circuitos existentes produzem eval cases/policies/backlog.
3. **O canal de feed-back para conhecimento do agente** — o conteúdo gerado retornando como fonte do agente.
4. **A confirmação de fechamento do gap** — verificação nos logs subsequentes de que o gap sumiu.

## Tradeoffs

| Benefício | Custo |
|---|---|
| Um loop humanamente inviável (~100 entrevistas/semana) torna-se automatizado | Depende da taxonomia de logs upstream — sem classificação não há gap detectável |
| Cobertura do agente expande guiada por demanda medida, não por palpite | Qualidade de ingestão varia entre fontes internas (Confluence/Jira/Slack/PRDs) |
| Conteúdo de enablement e conhecimento do agente sincronizados da mesma fonte | Conteúdo gerado precisa de review antes de voltar ao agente |
| Confirmação de fechamento nos logs torna o circuito auto-verificável | Risco de feedback echo: as respostas do agente moldam os logs futuros |

## Relação com outros padrões

- **Depende de:** [[docs/canonical/llm-classified-log-taxonomy|LLM-Classified Log Taxonomy]] — a query de tópicos emergentes/não respondidos é o gatilho; sem classificação de demanda, o circuito é cego.
- **Estruturalmente análogo a:** [[docs/canonical/confidence-gated-continual-learning|Confidence-Gated Continual Learning]] (detect→suggest→review→deploy) e [[docs/canonical/on-policy-rollout-feedback-loop|On-Policy Rollout Feedback Loop]] (rollout colhido → update targets) — mesma forma de loop; o artefato aqui é conteúdo, não policy/eval case.
- **Fecha o ciclo de:** [[docs/canonical/production-contact-training-loop|Production-Contact Training Loop]] — o harvest de produção aqui vira conhecimento gerado, não só eval corpus.
- **Distinto de:** [[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]] (gap de falha → caso de regressão) e [[docs/canonical/qa-to-backlog-feedback-loop|QA-to-Backlog Feedback Loop]] (achado de QA → issue) — demanda medida → conteúdo é o quarto quadrante: falha, QA e demanda como três triggers, três artefatos.

## Referências

- `docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-patterns.md:376-405` — padrão extraído: gap de conhecimento, geração de battle cards, feed-back, confirmação.
- `docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-classification.yaml:324-347` — classificação Partial Coverage (Medium) com evidência e NOT_FOUND.
- `docs/canonical/on-policy-rollout-feedback-loop.md:41` — scored prefixes como update targets.
- `docs/canonical/production-contact-training-loop.md:37, :39-54, :69-75` — loop diário e peças declaradas faltantes.
- `docs/canonical/confidence-gated-continual-learning.md:32` — loop detect-suggest-review-deploy gateado por confiança.
- `docs/canonical/production-failure-regression-flywheel.md:28` — falhas como casos de regressão.
- `docs/canonical/qa-to-backlog-feedback-loop.md:30-44, :57-59` — captura/triage/conversão e gap declarado.
- `docs/system-of-record.md:46` — analyze-and-improve como pipeline knowledge→content.
