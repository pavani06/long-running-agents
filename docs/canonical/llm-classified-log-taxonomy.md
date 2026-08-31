---
title: "LLM-Classified Log Taxonomy"
type: canonical
tags: ["evals", "production", "knowledge-management", "agentes-orquestracao"]
Status: Active
Source: "AI Engineer talk — Sait Izmit, Snowflake (GTM assistant: 6.000 usuários, 1,2M perguntas, ~40k/semana)"
Classification: "Partial Coverage, High integration value (P1)"
Precedence: "Level 2 (docs/system-of-record.md)"
last_updated: 2026-08-30
aliases: ["log taxonomy", "demand taxonomy", "feature-gap radar", "llm log classification"]
relates-to:
  - "[[docs/canonical/3-layer-evaluation-architecture|3-Layer Evaluation Architecture]]"
  - "[[docs/canonical/failure-pattern-classification-loop|Failure Pattern Classification Loop]]"
  - "[[docs/canonical/eval-dashboard-primary-detection-surface|Eval Dashboard Primary Detection Surface]]"
  - "[[docs/canonical/production-contact-training-loop|Production-Contact Training Loop]]"
  - "[[docs/canonical/semantic-topic-bucketing|Semantic Topic Bucketing]]"
  - "[[docs/canonical/gap-to-content-feedback-circuit|Gap-to-Content Feedback Circuit]]"
  - "[[docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-analysis|GTM AI Agents Analysis]]"
sources:
  - "[[docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-patterns|GTM AI Agents Patterns]]"
  - "[[docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-classification|GTM AI Agents Classification]]"
---

# LLM-Classified Log Taxonomy

**Type:** Canonical Pattern
**Status:** Active
**Source:** AI Engineer talk — Sait Izmit, Snowflake (GTM assistant: 6.000 usuários, 1,2M perguntas totais, ~40k perguntas/semana)
**Classification:** Partial Coverage, High integration value (P1)
**Precedence:** Level 2 ([[docs/system-of-record|System of Record]])

---

## Problema

Dezenas de milhares de perguntas por semana não podem ser lidas por humanos, e entrevistas amostram uma fração minúscula e atrasada do que os usuários realmente perguntam (`docs/analysis/...-patterns.md:343-346`). No caso Snowflake, o loop tradicional de detecção de gaps de conhecimento exigiria ~100 entrevistas de vendedores por semana — um loop que humanos não sustentam.

Sem um instrumento de classificação em escala, três consumidores ficam cegos:

1. **Produto** não vê em que tópicos a demanda se concentra (feature gaps).
2. **Enablement** não sabe que conteúdo produzir (ver [[docs/canonical/gap-to-content-feedback-circuit|Gap-to-Content Feedback Circuit]]).
3. **Roadmap de cobertura** não tem evidência para sequenciar expansão (ver [[docs/canonical/quality-over-coverage-trust-scoping|Quality-Over-Coverage Trust Scoping]]).

O repo tem toda a mecânica de classificação por LLM — mas apontada para o **lado da oferta** (comportamento e falhas do agente). Nenhum instrumento existente classifica o **lado da demanda** (o que os usuários pedem).

## Solução

Um pipeline de classificação LLM sobre os logs de perguntas de produção que produz uma **taxonomia hierárquica de demanda** em near-real-time, com custo controlado (`docs/analysis/...-patterns.md:365-374`):

| Componente | Função |
|---|---|
| Pipeline de coleta de logs | Perguntas de produção em volume (~40k/semana no caso-fonte) |
| Job de classificação LLM com controles de custo | Classifica cada pergunta na taxonomia sem "quebrar o banco" — tiering de modelo e amostragem |
| Store de taxonomia hierárquica | category → subcategory → example questions |
| Queries de feature-gap radar | Concentrações de perguntas sem resposta ou respondidas mal (perguntas repetidas, usuários "xingando o agente") |

Fluxo: coletar logs → classificar na taxonomia a custo controlado → evidenciar concentrações de tópicos não respondidos/pobres → expor a taxonomia para os consumidores downstream (circuito gap-to-content, roadmap de cobertura).

Propriedades operacionais que fazem o padrão funcionar (`docs/analysis/...-patterns.md:352-364`):

- **Detecção em minutos**: substitui ~100 entrevistas/semana por lag de minutos.
- **Um instrumento, três consumidores**: feature gaps, conteúdo de enablement, matchmaking cross-time.
- **Sinais de qualidade como proxies heurísticos**: perguntas repetidas e frustração do usuário marcam gaps mesmo sem eval formal.
- **Cold start**: precisa de volume acumulado antes de a taxonomia ser útil; drift da taxonomia exige disciplina de manutenção e re-classificação.

## Implementação neste repositório

### O que já existe

A mecânica de classificação LLM e a colheita de logs existem em profundidade canônica — apontadas para comportamento/falha do agente:

- **Camada LLM-as-Judge**: Layer 2 Semantic da [[docs/canonical/3-layer-evaluation-architecture|3-Layer Evaluation Architecture]] (`docs/canonical/3-layer-evaluation-architecture.md:45` — Layer 2 Semantic/LLM-as-Judge definida; `:82` — LLM-as-Judge com rubrica como mecanismo da superfície de qualidade).
- **Loop de classificação com mapeamento classe→superfície**: [[docs/canonical/failure-pattern-classification-loop|Failure Pattern Classification Loop]] (`:31-33` — loop observe-classify-build-verify; `:54-63` — taxonomia de root cause com mapeamento classe→superfície).
- **Dashboard como superfície primária de detecção**: [[docs/canonical/eval-dashboard-primary-detection-surface|Eval Dashboard Primary Detection Surface]] (`:50` — pain signals visíveis; `:77` — anomaly alerts calibrados por camada).
- **Colheita de interações de produção**: [[docs/canonical/production-contact-training-loop|Production-Contact Training Loop]] (`:64-66` — harvesting de interações reais para o corpus crescente; precedente de fonte de dados).
- **Precedente de ferramentagem**: skill analyze-and-improve — pipeline LLM de extração/classificação com model tiering (`docs/system-of-record.md:46`); semantic-topic-bucketing como agrupamento por tópico, mas para retenção de contexto — objeto diferente (`docs/system-of-record.md:191`).

### O que falta

O reframe demand-side (classification:317-323):

1. **Taxonomia hierárquica de demanda sobre logs de perguntas do usuário** — todo instrumento existente classifica comportamento ou falhas do agente; nenhum classifica o que os usuários pedem. Busca da classificação: `log taxonomy|question log|battle card|demand taxonomy` em `docs/canonical/`, `docs/analysis/`, `curriculum/`, `.opencode/` — matches apenas no pacote-fonte.
2. **Feature-gap radar** — queries de concentração de perguntas sem resposta/mal respondidas como superfície de produto.
3. **Classificação com custo engenheirado em escala** — 40k perguntas/semana exige tiering/amostragem deliberados, ausentes como padrão nomeado (o tiering existe em analyze-and-improve como ferramentagem, não como padrão de instrumento de demanda).

## Tradeoffs

| Benefício | Custo |
|---|---|
| Substitui ~100 entrevistas/semana por detecção com lag de minutos | Engenharia de custo não trivial para classificar 40k perguntas/semana |
| Um instrumento, três consumidores: feature gaps, enablement, matchmaking | Drift da taxonomia exige manutenção e re-classificação contínuas |
| Roadmap de cobertura moldado por evidência de demanda real | Sinais de qualidade (perguntas repetidas, frustração) são proxies heurísticos |
| Near-real-time: gap de conhecimento visível antes do churn/entrevista | Cold start — precisa de volume acumulado antes de ser útil |

## Relação com outros padrões

- **Depende de:** [[docs/canonical/production-contact-training-loop|Production-Contact Training Loop]] — a colheita de interações reais é a fonte do log; agente lab-only não gera demanda para classificar.
- **Reutiliza a mecânica de:** [[docs/canonical/3-layer-evaluation-architecture|3-Layer Evaluation Architecture]] (Layer 2 LLM-as-Judge) e [[docs/canonical/failure-pattern-classification-loop|Failure Pattern Classification Loop]] (loop de classificação) — mesma máquina, objeto invertido: demanda em vez de falha.
- **Alimenta:** [[docs/canonical/gap-to-content-feedback-circuit|Gap-to-Content Feedback Circuit]] — a taxonomia é o trigger upstream do circuito de conteúdo; [[docs/canonical/quality-over-coverage-trust-scoping|Quality-Over-Coverage Trust Scoping]] — o radar de gaps evidencia onde expandir cobertura pós-launch.
- **Superfície de:** [[docs/canonical/eval-dashboard-primary-detection-surface|Eval Dashboard Primary Detection Surface]] — o radar de gaps é candidato à mesma posição de "primeira tela aberta" para o lado da demanda.
- **Distinto de:** [[docs/canonical/semantic-topic-bucketing|Semantic Topic Bucketing]] — bucketing agrupa contexto para retenção; aqui a taxonomia classifica demanda para decisão de produto.

## Referências

- `docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-patterns.md:343-374` — padrão extraído: problema (40k/semana ilegível), componentes, fluxo, limitações.
- `docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-classification.yaml:301-323` — classificação Partial Coverage/High (P1) com evidência e NOT_FOUND.
- `docs/canonical/3-layer-evaluation-architecture.md:45, :82` — Layer 2 LLM-as-Judge.
- `docs/canonical/failure-pattern-classification-loop.md:31-33, :54-63` — loop de classificação e taxonomia de root cause.
- `docs/canonical/eval-dashboard-primary-detection-surface.md:50, :77` — detecção e anomaly alerts.
- `docs/canonical/production-contact-training-loop.md:64-66` — colheita de produção.
- `docs/system-of-record.md:46, :191` — analyze-and-improve (tiering) e semantic-topic-bucketing (objeto distinto).
