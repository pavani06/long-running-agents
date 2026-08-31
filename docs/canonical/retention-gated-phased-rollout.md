---
title: "Retention-Gated Phased Rollout"
type: canonical
tags: ["evals", "production", "governanca"]
Status: Active
Source: "AI Engineer talk — Sait Izmit, Snowflake (GTM assistant: 6.000 usuários, 1M+ perguntas)"
Classification: "Partial Coverage (P2, Medium integration value)"
Precedence: "Level 2 (docs/system-of-record.md)"
last_updated: 2026-08-30
aliases: ["retention gate", "phased rollout retention", "beta cohort rollout", "weekly-active gate"]
relates-to:
  - "[[docs/canonical/production-grounded-eval-sampling|Production-Grounded Eval Sampling]]"
  - "[[docs/canonical/carve-out-pilot-hard-target|Carve-Out Pilot with Hard P&L Target]]"
  - "[[docs/canonical/autonomy-curriculum-sampling|Autonomy Curriculum Sampling]]"
  - "[[docs/canonical/eval-to-production-correlation-tracking|Eval-to-Production Correlation Tracking]]"
  - "[[docs/canonical/trial-retention-attribution-split|Trial-Retention Attribution Split]]"
  - "[[docs/canonical/quality-over-coverage-trust-scoping|Quality-Over-Coverage Trust Scoping]]"
  - "[[docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-analysis|GTM AI Agents Analysis]]"
sources:
  - "[[docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-patterns|GTM AI Agents Patterns]]"
  - "[[docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-classification|GTM AI Agents Classification]]"
---

# Retention-Gated Phased Rollout

**Type:** Canonical Pattern
**Status:** Active
**Source:** AI Engineer talk — Sait Izmit, Snowflake (GTM assistant: 6.000 usuários, ~600 no beta de 10%)
**Classification:** Partial Coverage (P2, Medium integration value)
**Precedence:** Level 2 ([[docs/system-of-record|System of Record]])

---

## Problema

Um sistema não-determinístico não pode ser exposto com segurança a uma organização inteira de uma vez — e uso de novidade mascara se existe fit real de workflow (`docs/analysis/...-patterns.md:86-89`).

Dois eixos de falha:

1. **Exposição total.** GA imediato para 6.000 usuários transforma cada gap de qualidade em queima de confiança em massa (ver [[docs/canonical/quality-over-coverage-trust-scoping|Quality-Over-Coverage Trust Scoping]] — as primeiras ~5 perguntas decidem o retorno).
2. **Métrica errada no gate.** Adoção inicial (novidade) parece sucesso; sem retenção weekly-active como gate, a progressão de fases avança sobre sinais falsos. O repo registra o análogo de eval: scores verdes que deixam de prever outcomes (`docs/canonical/eval-to-production-correlation-tracking.md:22`).

O repo tem rollout faseado para infraestrutura (shadow/canary/rollback) e pilotos com regra de saída — mas falta o **eixo população de usuários**: nenhuma doc gateia progressão de rollout por retenção (classification:94-98).

## Solução

Progressão de exposição em três fases sobre a população de usuários, com gate duro de retenção (`docs/analysis/...-patterns.md:107-118`):

| Fase | População | Objetivo | Sinal |
|---|---|---|---|
| Piloto | Cohort AI-native que dá feedback | Lixar arestas por algumas semanas | Qualidade do feedback |
| Beta | 10% (~600 de 6.000) | Provar que o MVP é real | Clustering de requests "connect this data" + retenção |
| GA | Organização inteira | Escala | **Gate: >70% de retenção weekly-active** |

Componentes (`docs/analysis/...-patterns.md:107-112`): cohort de piloto; cohort de beta (10%); análise de clustering de requests; métrica de retenção weekly-active; gate de GA (>70%).

Fluxo (`docs/analysis/...-patterns.md:113-118`): pilotar com usuários AI-native por algumas semanas e lixar arestas → expandir para beta de 10% → fazer cluster dos requests "connect this data" para achar concentrações que definem dados must-have (se existe MVP para os workflows diários) → medir retenção weekly-active → abrir GA somente quando retenção superar 70% e acurácia/cobertura estiverem provadas.

A carga mecânica distinctive: **clustering de concentração de requests** define os dados must-have — a evidência do que é MVP não vem de entrevistas, vem da distribuição dos pedidos reais. E o gate de GA combina três provas: acurácia (zona de qualidade), cobertura (dados must-have conectados) e retenção (fit de workflow) — qualquer uma faltando segura a fase.

## Implementação neste repositório

### O que já existe

Rollout faseado existe para outros eixos (classification:74-98):

- **Infraestrutura:** [[docs/canonical/production-grounded-eval-sampling|Production-Grounded Eval Sampling]] — "staged shadow tests, canaries, production metrics, rollback, and observation exceed the canary gate pattern" (`docs/canonical/production-grounded-eval-sampling.md:107`).
- **Piloto com regra de saída:** [[docs/canonical/carve-out-pilot-hard-target|Carve-Out Pilot with Hard P&L Target]] — "exit: [scale-to-next-city, iterate-harness, kill]" (`docs/canonical/carve-out-pilot-hard-target.md:66`).
- **Readiness gates por métricas:** [[docs/canonical/autonomy-curriculum-sampling|Autonomy Curriculum Sampling]] — "Readiness gates | Per-phase metrics that must pass before advancing lambda: task success rate, repair rate, unsafe-action rate, evaluator confidence" (`docs/canonical/autonomy-curriculum-sampling.md:58`).
- **Retenção como outcome rastreável (não como gate):** [[docs/canonical/eval-to-production-correlation-tracking|Eval-to-Production Correlation Tracking]] — "Production outcomes | Task success, complaints, escalations, support tickets, CSAT proxy, latency, cost, retention, or domain-specific success metrics" (`docs/canonical/eval-to-production-correlation-tracking.md:35`).

### O que falta

(classification:89-98) — busca da classificação: `weekly-active|beta cohort|retention-gated GA|request clustering` em `docs/canonical/`, `curriculum/`, `.opencode/skills/`, `docs/system-of-record.md` — matches canônicos de "retention" são retenção de memória/dados ou timers de purge de telemetria:

1. **O eixo população de usuários** — piloto AI-native → beta de 10% → GA não existe como progressão de rollout; o rollout faseado do repo é de infraestrutura (shadow/canary) e de piloto organizacional (carve-out).
2. **Gate de GA por retenção weekly-active (>70%)** — retenção aparece só como outcome rastreável, nunca como gate de progressão de fase.
3. **Clustering de concentração de requests** como definidor de dados must-have — não existe como mecanismo de decisão de cobertura.

## Tradeoffs

| Benefício | Custo |
|---|---|
| Ganha as primeiras cinco perguntas sem queimar pontes com a organização inteira | Rollout mais lento; disciplina de gate pode atrasar o GA |
| Prova que o MVP é real via clustering de requests + retenção, não anedotas | Exige instrumentação de retenção desde o dia um |
| GA só ocorre com acurácia, cobertura e retenção todas provadas | Qualidade do piloto depende de recrutar usuários genuinamente AI-native |
| Clustering define must-have data com evidência de demanda | A enxurrada de requests "connect this data" precisa de triagem para não virar backlog cego |

## Relação com outros padrões

- **Depende de:** [[docs/canonical/quality-over-coverage-trust-scoping|Quality-Over-Coverage Trust Scoping]] — o escopo de alta acurácia é o que o piloto lixa e o beta mede; sem zona de qualidade, o gate de retenção falha por construction.
- **Validado por:** [[docs/canonical/eval-to-production-correlation-tracking|Eval-to-Production Correlation Tracking]] — a retenção gateando fases é o outcome que valida os scores de eval do lado do usuário.
- **Espelha:** [[docs/canonical/autonomy-curriculum-sampling|Autonomy Curriculum Sampling]] — progressão com readiness gates por métrica, aplicada à exposição de população em vez da autonomia do agente; [[docs/canonical/production-grounded-eval-sampling|Production-Grounded Eval Sampling]] e [[docs/canonical/carve-out-pilot-hard-target|Carve-Out Pilot with Hard P&L Target]] — rollout faseado nos eixos infraestrutura e piloto contido.
- **Alimenta:** [[docs/canonical/trial-retention-attribution-split|Trial-Retention Attribution Split]] — pós-GA, o split assume o monitoramento da retenção que este padrão instalou como gate.

## Referências

- `docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-patterns.md:86-118` — padrão extraído: piloto AI-native, beta 10%, clustering de requests, gate >70% weekly-active.
- `docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-classification.yaml:70-98` — classificação Partial Coverage (Medium) com NOT_FOUND de weekly-active/beta cohort.
- `docs/canonical/production-grounded-eval-sampling.md:107` — staged shadow/canary/rollback (eixo infraestrutura).
- `docs/canonical/carve-out-pilot-hard-target.md:66` — regra de saída do piloto.
- `docs/canonical/autonomy-curriculum-sampling.md:58` — readiness gates por métrica.
- `docs/canonical/eval-to-production-correlation-tracking.md:35` — retenção como outcome rastreável.
