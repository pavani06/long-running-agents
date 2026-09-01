---
title: "Perceived-Eval"
type: canonical
aliases: ["perceived eval", "user correction as eval signal", "avaliação percebida", "rage quit metric", "chat exit metric"]
tags: ["evals", "production", "agentes-orquestracao"]
last_updated: 2026-08-31
relates-to:
  - "[[docs/canonical/production-to-offline-feedback-loop|Production-to-Offline Feedback Loop]]"
  - "[[docs/canonical/eval-to-production-correlation-tracking|Eval-to-Production Correlation Tracking]]"
  - "[[docs/canonical/always-on-monitoring-human-triage|Always-On Monitoring with Human Triage]]"
  - "[[docs/canonical/presence-in-the-loop-metric|Presence-in-the-Loop Metric]]"
  - "[[docs/canonical/llm-classified-log-taxonomy|LLM-Classified Log Taxonomy]]"
  - "[[docs/canonical/eval-coverage-matrix|Eval Coverage Matrix]]"
sources:
  - "[[docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-patterns|Clay Eval Stack Patterns (2026-08-31)]]"
---

# Perceived-Eval

**Type:** Canonical Pattern
**Status:** Active
**Source:** Inside Clay's Eval Stack (300M Agent Runs, One LangSmith Pipeline) — LangChain, via `docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/`
**Classification:** Missing (P0) — integration value High
**Precedence:** Level 2 ([[docs/system-of-record|System of Record]])

---

## Problem

Medir a qualidade *percebida* do agente em produção sem rodar surveys explícitos o tempo todo. Sondas de satisfação são caras, intermitentes e sofrem de survey fatigue; sem elas, o time fica cego para o caso em que o agente produz output tecnicamente aceitável mas o usuário o experienciou como errado, lento ou inútil (`docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-patterns.md:163-184`).

O sinal mais rico — o comportamento de correção do usuário dentro da conversa — evapora se não for instrumentado: o usuário que *corrige* o agente ("não, eu quis dizer X"), que faz *pushback* ("isso está errado") ou que tenta *redirecionar* a conversa está produzindo, gratuitamente, um julgamento de qualidade item a item. Sem um padrão que capture esse comportamento como dado, ele nunca vira eval.

## Solution

Tratar o comportamento de correção do usuário como dado de avaliação, com três famílias de sinal (`...-patterns.md:166-175`):

1. **Eventos de correção/pushback/redirection** extraídos dos traces de conversa em produção: detecção (por classificador ou regra) de turnos em que o usuário contesta, corrige ou tenta guiar o agente para outro lugar. Cada evento é um sinal negativo de qualidade no nível da decisão, não da sessão.
2. **Telemetria comportamental objetiva** que delimita falha percebida: saída do chat para outras áreas do produto, *stuck* (usuário sem progresso), *rage quit* (abandono abrupto). São métricas online contínuas, sem survey.
3. **NPS/satisfação como entrada contínua**, pareada com as métricas comportamentais — subjetivo e objetivo se confirmam mutuamente.

Propriedades operacionais: o sinal é coletado continuamente (sem fadiga de survey); a resolução é por sessão, não por decisão (`...-patterns.md:183`); e os eventos alimentam o loop produção→offline como casos-candidatos de eval.

Métricas comportamentais têm causas benignas (tarefa concluída, usuário explorando) — por isso o padrão exige a combinação: correção + telemetria + NPS, nunca um sinal isolado (`...-patterns.md:181-182`).

## Implementation in this repo

### What already exists

Apenas vizinhos fracos, todos com escopo distinto:

- **CSAT como proxy de outcome** — `docs/canonical/eval-to-production-correlation-tracking.md:35` lista "CSAT proxy" na tabela de production outcomes, e `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:1596` o usa em dashboard baseline/candidate. Nos dois casos é métrica de resultado correlacionada, não sinal de eval contínuo.
- **always-on-monitoring-human-triage** (`docs/system-of-record.md:300`) — monitora anomalias *do sistema* com triagem humana; não qualidade percebida *pelo usuário final*.
- **presence-in-the-loop-metric** (`docs/system-of-record.md:238`) — calibra intervenção de operadores humanos no workflow; não percepção de usuários do produto.
- **llm-classified-log-taxonomy** — minera as *perguntas* dos usuários em logs como radar de gaps; não captura o comportamento de *correção* nem métricas de abandono.

### What is missing

Tudo, na classificação Missing (P0) (`...-classification.md:132-144`):

1. **Detector de correction/pushback/redirection** sobre traces de conversa — greps `NPS|rage quit|perceived quality|user correction|pushback` e `correção do usuário|cliente corrige|usuário corrige` retornam 0 matches fora do pacote-fonte.
2. **Métricas comportamentais de saída do chat/stuck/rage quit** — não existem em doc, código ou currículo.
3. **NPS como entrada contínua de eval** — CSAT aparece em 34 arquivos como métrica de dashboard/outcome, nunca como sinal de eval.
4. **O posicionamento do sinal no portfólio** — como quadrante online/nondeterministic da [[docs/canonical/eval-coverage-matrix|Eval Coverage Matrix]] e como input do [[docs/canonical/production-to-offline-feedback-loop|Production-to-Offline Feedback Loop]].

## Tradeoffs

| Benefit | Cost |
|---|---|
| Trata o comportamento de correção do próprio usuário como dado de avaliação — sinal gratuito e contínuo | Exige instrumentação confiável para detectar correções e pushback nos traces |
| Sem survey fatigue; coleta contínua em todo o tráfego de produção | Métricas comportamentais têm causas benignas (tarefa feita, exploração) — precisam de triangulação |
| Combina sinal subjetivo (NPS) e objetivo (comportamental) que se confirmam | Resolução é por sessão, não por decisão — não localiza a falha exata |
| Alimenta o loop produção→offline com casos de alta qualidade | Requer tráfego real de produção e volume suficiente para o sinal estabilizar |

## Relationship to Other Patterns

- **Alimenta:** [[docs/canonical/production-to-offline-feedback-loop|Production-to-Offline Feedback Loop]] — eventos de correção são produção-signals de entrada do refresh do eval set.
- **Ocupa quadrante de:** [[docs/canonical/eval-coverage-matrix|Eval Coverage Matrix]] — o sinal online/nondeterministic que o portfólio costuma deixar vazio.
- **Complementa:** [[docs/canonical/eval-to-production-correlation-tracking|Eval-to-Production Correlation Tracking]] — perceived-eval fornece o outcome percebido que a correlação eval↔produção precisa medir além de CSAT pontual.
- **Distinto de:** [[docs/canonical/always-on-monitoring-human-triage|Always-On Monitoring with Human Triage]] — anomalias do sistema vs. qualidade percebida pelo usuário.
- **Distinto de:** [[docs/canonical/presence-in-the-loop-metric|Presence-in-the-Loop Metric]] — intervenção de operadores vs. percepção de usuários.
- **Complementa:** [[docs/canonical/llm-classified-log-taxonomy|LLM-Classified Log Taxonomy]] — duas minerações distintas do tráfego do usuário (perguntas vs. correções/comportamento).

## References

- `docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-patterns.md:163-184` — definição original do padrão.
- `docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-classification.md:132-144` — classificação Missing/High com evidência NOT_FOUND.
- `docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-classification.yaml:145-165` — evidência estruturada.
- `docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-analysis.md` — extração de conhecimento da fonte.

---

*Created: 2026-08-31 | From: Clay eval stack classification (P0) | Precedence: canonical*
