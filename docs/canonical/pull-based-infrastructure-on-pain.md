---
title: "Pull-Based Infrastructure on Pain"
type: canonical
tags: ["evals", "harness-engineering", "harness", "decision-discipline", "production"]
Status: Active
Source: "AI Engineer talk — Sait Izmit, Snowflake (GTM assistant: 6.000 usuários, ~40k perguntas/semana)"
Classification: "Partial Coverage (P2, Medium integration value)"
Precedence: "Level 2 (docs/system-of-record.md)"
last_updated: 2026-08-30
aliases: ["pull on pain", "pain-driven infrastructure", "minimal launch stack", "reactive hardening"]
relates-to:
  - "[[docs/canonical/pain-signal-eval-progression-gate|Pain-Signal Eval Progression Gate]]"
  - "[[docs/canonical/eval-investment-parity|Eval-Investment Parity]]"
  - "[[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]]"
  - "[[docs/canonical/symphony-trap-awareness|Symphony Trap Awareness]]"
  - "[[docs/canonical/continuous-re-architecture-budget|Continuous Re-Architecture Budget]]"
  - "[[docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-analysis|GTM AI Agents Analysis]]"
sources:
  - "[[docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-patterns|GTM AI Agents Patterns]]"
  - "[[docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-classification|GTM AI Agents Classification]]"
---

# Pull-Based Infrastructure on Pain

**Type:** Canonical Pattern
**Status:** Active
**Source:** AI Engineer talk — Sait Izmit, Snowflake (GTM assistant: lançado com 9 páginas de instruções e Google Doc)
**Classification:** Partial Coverage (P2, Medium integration value)
**Precedence:** Level 2 ([[docs/system-of-record|System of Record]])

---

## Problema

Pré-construir infraestrutura perfeita (CI/CD, suites de eval, sistemas de skills) atrasa o lançamento além da janela de aprendizado; empresas travam tentando **comprar** a arquitetura perfeita em vez de construir, lançar e aprender (`docs/analysis/...-patterns.md:282-285`).

O caso-fonte delimita o stack mínimo de lançamento: 9 páginas de instruções de agente, um par de ferramentas de analista, views semânticas, um serviço de busca, e versionamento de instruções num Google Doc (`docs/analysis/...-patterns.md:286-287`). Nada de CI/CD, evals, skills ou progressive disclosure no dia um — tudo isso chegou **depois**, na sequência em que a ausência doeu em escala (6.000 usuários, 40k perguntas/semana).

O custo do caminho oposto é compounding: esperar maturidade arquitectural entrega a liderança de aprendizado (e de logs) ao concorrente que lançou mínimo — os padrões de taxonomia de logs e circuito gap-to-content **dependem desse volume** (`docs/analysis/...-patterns.md:293-295`).

## Solução

Adicionar infraestrutura **reativamente, na sequência em que sua ausência vira o binding constraint** (`docs/analysis/...-patterns.md:289-290`):

| Ordem | Infraestrutura | Dor que a puxa |
|---|---|---|
| 1 | CI/CD para instruções de agente | Versionamento em Google Doc doendo em escala |
| 2 | Infraestrutura de eval (unit tests, routing tests) | Regressões invisíveis entre versões |
| 3 | Skills | Instruções crescendo além do razoável (processos repetidos) |
| 4 | Progressive disclosure | Limite de janela de instrução sendo atingido |
| 5 | User memory + task scheduling | Usuários voltando sem contexto; trabalho agendado |
| 6 | Interfaces além de chat (Slack) | Demanda por canais onde o trabalho acontece |

Regras operacionais (`docs/analysis/...-patterns.md:296-310`):

1. **Cada investimento responde a uma restrição sentida, não a especulação.**
2. **A dor precisa estar visível** — o que exige contato real com produção.
3. **O sequenciamento é descoberto, não planejado**: lança mínimo, sente cada binding constraint como dor concreta em escala, adiciona apenas a infraestrutura que remove aquela restrição, repete.
4. **O imposto de re-arquitetura é aceito explicitamente** (30-40% permanente — ver [[docs/canonical/continuous-re-architecture-budget|Continuous Re-Architecture Budget]]).

A consequência deliberada: aprender em escala de 6.000 usuários meses antes do caminho de arquitetura-perfeita (`docs/analysis/...-patterns.md:291`).

## Implementação neste repositório

### O que já existe

A filosofia pull-on-pain existe em profundidade canônica, mas **escopada a capacidade de eval e governança de harness** (classification:255-278):

- [[docs/canonical/pain-signal-eval-progression-gate|Pain-Signal Eval Progression Gate]] — o princípio: maturidade de eval gateada por sinais de dor, não por roadmap de calendário (`:28`); "Approve only the smallest eval capability that addresses the observed pain" (`:36`); tabela de trigger pain-signal→capacidade-mínima + decision record (`:40-51`).
- [[docs/canonical/eval-investment-parity|Eval-Investment Parity]] — a reconciliação declarada: "pain-signal gating governs which capability to build next" (`docs/canonical/eval-investment-parity.md:58`).
- [[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]] — harness como lifecycle medido, não arquitetura one-time (`:29`); ROI threshold, cadência trimestral, One In One Out (`:52-62`).
- [[docs/canonical/symphony-trap-awareness|Symphony Trap Awareness]] — a postura anti-upfront-spec nomeia o modo de falha push-based (`:27`); build then distill (`:33`).
- Ativo no system-of-record como canonical Level 2 (`docs/system-of-record.md:198`).

### O que falta

(classification:272-278) — NOT_FOUND para o padrão full-stack e o sequenciamento minimal-launch: busca por `pull-based`, `on pain`, `minimal launch`, `reactive hardening` em `docs/decisions/`, `docs/canonical/`, `docs/evidence/`, `docs/analysis/`, `curriculum/`, `.opencode/skills/`:

1. **A generalização do pull-on-pain para a stack completa** — CI/CD, skills, progressive disclosure, memory e interfaces; o repo aplica o princípio só a capacidade de eval e governança de harness.
2. **O sequenciamento minimal-launch** — a noção explícita de stack mínimo de lançamento (instruções versionadas em doc, sem CI/CD) como decisão legítima que aceita o imposto de re-arquitetura.
3. **A sequência descoberta de hardening** — a ordem CI/CD → evals → skills → progressive disclosure → memory/scheduling → interfaces como consequência de bindings sucessivos, não como roadmap pré-escrito.

## Tradeoffs

| Benefício | Custo |
|---|---|
| Cada investimento de infraestrutura responde a uma restrição sentida, não especulação | Versionamento em Google Doc dói antes do CI/CD chegar |
| Launch cedo compounding aprendizado e logs — volume que alimenta taxonomia e circuitos de gap | incorre no imposto permanente de re-arquitetura de 30-40% |
| Evita o custo compounding de concorrência de esperar maturidade | A dor precisa estar visível, o que exige contato real com produção |
| Sequenciamento descoberto adapta-se ao domínio real em vez do imaginado | Stack mínimo é frágil em falha de escala antes do primeiro endurecimento |

## Relação com outros padrões

- **Generaliza:** [[docs/canonical/pain-signal-eval-progression-gate|Pain-Signal Eval Progression Gate]] — mesmo princípio pull-on-pain, estendido da capacidade de eval para a stack inteira de infraestrutura.
- **Reconcilia com:** [[docs/canonical/eval-investment-parity|Eval-Investment Parity]] — parity governa alocação agregada em escala de frota; pull-on-pain governa o que construir antes disso.
- **Convive com:** [[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]] — o lifecycle BUILD→REMOVE governa cada componente depois que o pull o trouxe à existência.
- **Anti-dote ao modo de falha de:** [[docs/canonical/symphony-trap-awareness|Symphony Trap Awareness]] — upfront-spec push-based é exatamente o que este padrão evita.
- **Paga a conta de:** [[docs/canonical/continuous-re-architecture-budget|Continuous Re-Architecture Budget]] — o lançamento mínimo é o gerador do imposto que o budget aloca.

## Referências

- `docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-patterns.md:282-310` — padrão extraído: stack mínimo, sequência reativa de hardening, aprendizado em escala.
- `docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-classification.yaml:255-278` — classificação Partial Coverage (Medium) com evidência e NOT_FOUND.
- `docs/canonical/pain-signal-eval-progression-gate.md:28, :36, :40-51` — princípio pull, menor capacidade suficiente, tabela de triggers.
- `docs/canonical/eval-investment-parity.md:58` — reconciliação declarada.
- `docs/canonical/measured-harness-evolution-lifecycle.md:29, :52-62` — lifecycle medido com ROI e cadência.
- `docs/canonical/symphony-trap-awareness.md:27, :33` — anti-upfront-spec; build then distill.
- `docs/system-of-record.md:198` — pain-signal gate como canonical ativa (Level 2).
