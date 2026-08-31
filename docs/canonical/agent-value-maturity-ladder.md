---
title: "Agent Value Maturity Ladder"
type: canonical
tags: ["production", "decision-discipline", "governanca", "agentes-orquestracao"]
Status: Active
Source: "AI Engineer talk — Sait Izmit, Snowflake (GTM assistant: 6.000 usuários, 1M+ perguntas)"
Classification: "Missing (Medium integration value)"
Precedence: "Level 2 (docs/system-of-record.md)"
last_updated: 2026-08-30
aliases: ["value maturity ladder", "switching-cost ladder", "wow-collapse paranoia", "agent value stages"]
relates-to:
  - "[[docs/canonical/autonomy-curriculum-sampling|Autonomy Curriculum Sampling]]"
  - "[[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]]"
  - "[[docs/canonical/quality-over-coverage-trust-scoping|Quality-Over-Coverage Trust Scoping]]"
  - "[[docs/canonical/human-review-staged-workflow-automation|Human-Review Staged Workflow Automation]]"
  - "[[docs/canonical/skill-resolver-skillify-capability-pipeline|Skill-Resolver Skillify Capability Pipeline]]"
  - "[[docs/canonical/owner-led-activation-blitz|Owner-Led Activation Blitz]]"
  - "[[docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-analysis|GTM AI Agents Analysis]]"
sources:
  - "[[docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-patterns|GTM AI Agents Patterns]]"
  - "[[docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-classification|GTM AI Agents Classification]]"
---

# Agent Value Maturity Ladder

**Type:** Canonical Pattern
**Status:** Active
**Source:** AI Engineer talk — Sait Izmit, Snowflake (GTM assistant: 6.000 usuários, 1M+ perguntas, ~40k perguntas/semana, ~20 skills)
**Classification:** Missing (Medium integration value)
**Precedence:** Level 2 ([[docs/system-of-record|System of Record]])

---

## Problema

Deployments de agentes travam no primeiro estágio de valor enquanto o fator wow colapsa em meses — a capacidade vira baseline e o produto "parece pior" sem ter piorado. Simultaneamente, custos de troca quase nulos deixam o usuário sair em 1-2 meses se a plataforma parar no tempo (`docs/analysis/...-patterns.md:407-410`).

Dois mecanismos compõem o problema:

1. **Habituação.** Usuários retornam comparando o agente com outros produtos de IA que usaram; o que era impressionante no lançamento é expectativa mínima dois meses depois. Sem um listener explícito para esses sinais (comparações, frustração), a queda de percepção só aparece como churn.
2. **Ausência de escada.** Sem um roadmap de estágios de valor deliberado, o time reage ao wow-collapse com melhorias incrementais dentro do mesmo estágio — o que não restaura a distinção nem constrói dependência.

## Solução

Um **roadmap de capacidades em estágios que funciona simultaneamente como escada de switching costs** (`docs/analysis/...-patterns.md:415-420`):

| Estágio | Valor para o usuário | Mecanismo | Switching cost construído |
|---|---|---|---|
| 1. Talk to your data | Democratização: escapar de 1.000 dashboards e filas de 2 semanas com analistas | Q&A sobre dados conectados | Dados de trabalho consolidados na plataforma |
| 2. Automate my workflows | Ações, não só respostas | Orquestração MCP com revisão humana (padrão Human-Review Staged) | Workflows operacionais rodando no agente |
| 3. Team empowerment | Times constroem os próprios skills, dashboards, apps, alertas | Biblioteca de skills como superfície de empoderamento | Ativos construídos pelos próprios times |
| 4. Hyper-personalization | Por vendedor e por cliente | Contexto vivo de clientes e contatos | Memória/contexto acumulado irreplicável |

Regras operacionais (`docs/analysis/...-patterns.md:421-439`):

1. **Paranoia institucionalizada**: "every time people are happy, you should be paranoid" — converter o wow-collapse em próximos estágios planejados, não em pânico reativo.
2. **Cadência de 1-2 meses por estágio** — o próximo "showing" é planejado antes de o atual virar baseline.
3. **Listener de habituação/frustração** — comparações explícitas dos usuários com outros produtos de IA são o sinal de que o estágio atual está virando baseline.
4. **Cada estágio pressupõe a confiança do anterior** — pular estágios queima a confiança que a escada depende.

A tese de lock-in: cada estágio eleva a dependência do usuário na plataforma — switching cost estratégico que novidade crua não conquista (`docs/analysis/...-patterns.md:423-424`). A confiança ganha em cada estágio compra o direito de iterar no seguinte.

## Implementação neste repositório

### O que já existe

A forma de progressão em estágios existe para outros objetos — o que falta é o objeto certo (valor de produto de agente):

- [[docs/canonical/autonomy-curriculum-sampling|Autonomy Curriculum Sampling]] — escada observe→assist→own para **autonomia do agente** por classe de tarefa (`docs/canonical/autonomy-curriculum-sampling.md:41, :60`); a classificação registra: "nearest ladder, wrong object (agent autonomy phases observe-assist-own, not product value stages)" (classification:358-359).
- [[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]] — progressão BUILD→STABILIZE→SIMPLIFY→REMOVE para **componentes de harness** (`docs/canonical/measured-harness-evolution-lifecycle.md:29`; classification:360-361).
- Fases de maturidade de **evals** (`docs/system-of-record.md:351-359`; classification:362-363) e níveis de aprendiz do currículo — mesma forma, objetos distintos.
- O eixo valor/adopção tem "casa" no repo sem conteúdo: `README.md:34` confirma business people como audiência (classification:364-365).
- Switching costs aparecem apenas em domínio cruzado: análise de mercado de energia (`docs/canonical/energy-value-chain-spread-analysis.md:90`; classification:356-357).

### O que falta

Estágios de valor de produto de agente como estratégia de adoção e lock-in não existem em nenhuma forma (classification:365-369):

1. **Modelo de estágios de valor** (data Q&A → automação de workflow → empoderamento de times → hiper-personalização).
2. **Escada de switching costs** como critério de design do roadmap.
3. **Listener de habituação** (wow-collapse como sinal operacional).
4. **Roadmap de capacidades em estágios** com cadência deliberada de 1-2 meses.

## Tradeoffs

| Benefício | Custo |
|---|---|
| Paranoia institucionalizada converte wow-collapse em próximos estágios planejados | Exige investimento compounding por estágio; estágios pressupõem a confiança dos anteriores |
| Cada estágio eleva switching costs — lock-in estratégico que novidade não ganha | O estágio de personalização exige infraestrutura de contexto vivo de clientes/contatos |
| Confiança ganha por estágio compra o direito de iterar no seguinte | Pular estágios queima a confiança que a escada depende |
| Sinais de habituação tornam a queda de percepção visível antes do churn | Cadência de 1-2 meses disputa prioridade com demanda de feature reativa |

## Relação com outros padrões

- **Lança em:** [[docs/canonical/quality-over-coverage-trust-scoping|Quality-Over-Coverage Trust Scoping]] — o estágio 1 nasce com escopo cortado para a zona de alta precisão; a confiança inicial é pré-requisito da escada.
- **Estágio 2 é:** [[docs/canonical/human-review-staged-workflow-automation|Human-Review Staged Workflow Automation]] — automação com revisão humana é o degrau de valor "insight→ação".
- **Estágio 3 é:** [[docs/canonical/skill-resolver-skillify-capability-pipeline|Skill-Resolver Skillify Capability Pipeline]] — a biblioteca de skills como superfície de empoderamento dos times.
- **Espelha (objeto diferente):** [[docs/canonical/autonomy-curriculum-sampling|Autonomy Curriculum Sampling]] — progressão com gates por métricas, aplicada a autonomia do agente, não a valor de produto; [[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]] — ciclo de vida medido para componentes.
- **Complementa:** [[docs/canonical/owner-led-activation-blitz|Owner-Led Activation Blitz]] — o blitz enche o funil; a escada converte uso em retenção e dependência.

## Referências

- `docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-patterns.md:407-440` — padrão extraído: quatro estágios, sinais de habituação, cadência, paranoia institucionalizada.
- `docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-classification.yaml:348-369` — classificação Missing (Medium) com NOT_FOUND e adjacentes de objeto errado.
- `docs/canonical/autonomy-curriculum-sampling.md:41, :60` — escada observe/assist/own (autonomia, não valor de produto).
- `docs/canonical/energy-value-chain-spread-analysis.md:90` — switching costs em domínio distinto.
- `docs/system-of-record.md:351-359` — fases de maturidade de evals (maturidade de evals, não valor de agente).
