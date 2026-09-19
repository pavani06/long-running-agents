---
title: "Métrica CRAP de risco de mudança"
type: "extract"
source: "x"
status_id: "2099728101366276474"
handle: "schteppe"
url: "https://x.com/schteppe/status/2099728101366276474"
created_at: "2026-09-15T05:12:45.000Z"
extracted: "2026-09-17"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-16-schteppe-the-crap-change-risk-anti-patterns-metric-is-a-software-qual--2099728101366276474.json]]"
tags: ["code-review", "testes-qa", "analise"]
topic: "Métrica CRAP de risco de mudança"
summary: "A métrica CRAP (Change Risk Anti-Patterns) combina complexidade ciclomática e cobertura de testes automatizados para quantificar o risco de modificar uma função ou método, via CRAP(m) = comp(m)^2 * (1 - cov(m))^3 + comp(m). Vale salvar como referência prática para priorizar refatoração e testes onde mudanças são mais arriscadas."
key_points: ["CRAP(m) = comp(m)^2 * (1 - cov(m))^3 + comp(m): o risco cresce quadraticamente com a complexidade e é amplificado pela falta de cobertura de testes.", "Código altamente complexo mas bem coberto por testes tem CRAP baixo — cobertura reduz o risco de alteração; código simples sem testes ainda assim pontua baixo devido ao termo aditivo comp(m).", "Serve como triagem objetiva em code review e manutenção: aponta funções que merecem refatoração (reduzir complexidade) ou mais testes (aumentar cobertura) antes de mudanças.", "Difundida pelo Google Testing Blog (post 'This Code is CRAP', 2011), ligando métricas estáticas de qualidade a risco de manutenção."]
entities: ["CRAP (Change Risk Anti-Patterns)", "Google Testing Blog"]
content_type: "resource"
revisit: "medium"
grounded_in: "tweet"
thin: false
links: ["https://testing.googleblog.com/2011/02/this-code-is-crap.html"]
media: []
theme: "Tooling para agentes de código"
relates-to: ["[[extracts/x/bookmarks/2026-09-12-mattpocockuk-starting-to-wonder-if-the-smartest-way-to-reduce-slop-is-jus--2094500508224409852|reduzir código para reduzir slop]]", "[[extracts/x/bookmarks/2026-09-18-redp314-got-jev-to-review-my-prs-200x-cheaper-than-claude-and-it-ans--2100585126652481915|Code review barato via typesafe]]", "[[extracts/x/bookmarks/2026-09-12-mihail_eric-line-by-line-code-review-will-soon-disappear-the-future-is-a--2098097592001548319|revisão de código risco-gateada]]", "[[extracts/x/bookmarks/2026-09-12-chrisshort-alibaba-open-code-review-battle-tested-at-alibaba-s-scale-hy--2098555200680218872|ferramenta de code review híbrida]]", "[[extracts/x/bookmarks/2026-09-18-devagrawal09-built-jev-review-a-small-code-review-workflow-powered-by-typ--2100341005690298687|Code-review workflow com julgamentos LLM]]", "[[extracts/x/bookmarks/2026-09-12-ibesh_tech-bcherny-the-review-bar-should-follow-blast-radius-not-who-wr--2098218598997336384|Code review e blast radius]]"]
---

# Métrica CRAP de risco de mudança

**@schteppe** · [2099728101366276474](https://x.com/schteppe/status/2099728101366276474) · `resource`

## Resumo
A métrica CRAP (Change Risk Anti-Patterns) combina complexidade ciclomática e cobertura de testes automatizados para quantificar o risco de modificar uma função ou método, via CRAP(m) = comp(m)^2 * (1 - cov(m))^3 + comp(m). Vale salvar como referência prática para priorizar refatoração e testes onde mudanças são mais arriscadas.

## Pontos-chave
- CRAP(m) = comp(m)^2 * (1 - cov(m))^3 + comp(m): o risco cresce quadraticamente com a complexidade e é amplificado pela falta de cobertura de testes.
- Código altamente complexo mas bem coberto por testes tem CRAP baixo — cobertura reduz o risco de alteração; código simples sem testes ainda assim pontua baixo devido ao termo aditivo comp(m).
- Serve como triagem objetiva em code review e manutenção: aponta funções que merecem refatoração (reduzir complexidade) ou mais testes (aumentar cobertura) antes de mudanças.
- Difundida pelo Google Testing Blog (post 'This Code is CRAP', 2011), ligando métricas estáticas de qualidade a risco de manutenção.

## Links
- https://testing.googleblog.com/2011/02/this-code-is-crap.html

## Entidades
CRAP (Change Risk Anti-Patterns), Google Testing Blog

> **Revisit:** `medium` · **fonte:** `tweet`
