---
title: "Code-review workflow com julgamentos LLM"
type: "extract"
source: "x"
status_id: "2100341005690298687"
handle: "devagrawal09"
url: "https://x.com/devagrawal09/status/2100341005690298687"
created_at: "2026-09-16T21:48:12.000Z"
extracted: "2026-09-18"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-18-devagrawal09-built-jev-review-a-small-code-review-workflow-powered-by-typ--2100341005690298687.json]]"
tags: ["code-review", "harness", "gate-design", "agent-tooling", "stack-tooling"]
topic: "Code-review workflow com julgamentos LLM"
summary: "Jev Review é uma ferramenta local de code review que analisa Git diffs ou codebases completos usando julgamentos estruturados e limitados via TypeSafe Jev, com orquestração mantida em código e resultados em dashboard local. Vale salvar como referência de arquitetura em camadas para compor julgamentos de modelo rápidos e tipados em um pipeline de revisão."
key_points: ["Orquestração fica em código; Jev é usado apenas para julgamentos limitados em estágios: risk matrix -> score de perfis -> seleção de evidências -> classificação de mecanismo -> severidade -> roteamento condicional de revisores", "Dois pontos de entrada: revisão de diff (mudanças) e scan completo de codebase; usa testes alterados/relacionados como contexto ao julgar lacunas de cobertura", "Avalia correção, segurança, confiabilidade, compatibilidade e cobertura de testes; seleciona hunks concretos do diff antes de pontuar impacto; thresholds e política de workflow aplicados em código (não no modelo)", "Arquitetura em camadas com dependência só descendente (cli/dashboard -> review -> adapters -> domain), enforced por script que falha o build em imports ascendentes ou ciclos; dashboard binda em 127.0.0.1 e nunca serve arquivos de ambiente", "Limitações explícitas: sem diagnósticos de compilador, analisadores estáticos ou indexação de repositório; achados são prompts de revisão, não prova de defeito"]
entities: ["Jev Review", "TypeSafe AI", "Jev", "Node.js", "Git", "npm", "@devagrawal09"]
content_type: "tool"
revisit: "high"
grounded_in: "article"
thin: false
links: ["https://github.com/devagrawal09/jev-review"]
media: []
theme: "Tooling para agentes de código"
relates-to: ["[[extracts/x/bookmarks/2026-09-12-steipete-hit-a-new-record-with-our-autoreview-skill-66-rounds-on-a-gn--2080899298838098034|Autoreview: code review multi-engine]]", "[[extracts/x/bookmarks/2026-09-12-chrisshort-alibaba-open-code-review-battle-tested-at-alibaba-s-scale-hy--2098555200680218872|ferramenta de code review híbrida]]", "[[extracts/x/bookmarks/2026-09-18-redp314-got-jev-to-review-my-prs-200x-cheaper-than-claude-and-it-ans--2100585126652481915|Code review barato via typesafe]]", "[[extracts/x/bookmarks/2026-09-17-trending_repos-trending-repository-of-the-day-open-code-review-fast-efficie--2100194977523331489|Open Code Review da Alibaba]]", "[[extracts/x/bookmarks/2026-09-15-agenticgirl-alibaba-open-sourced-the-code-reviewer-it-says-has-served-te--2099087022900367845|Open-source code reviewer do Alibaba]]", "[[extracts/x/bookmarks/2026-09-12-mihail_eric-line-by-line-code-review-will-soon-disappear-the-future-is-a--2098097592001548319|revisão de código risco-gateada]]", "[[extracts/x/bookmarks/2026-09-14-riverai7z-pi-review-pi-install-git-https-t-co-ezws490o0e--2098752822221365732|Plugin de code review para Pi]]", "[[extracts/x/bookmarks/2026-09-19-moritzkremb-p-s-i-ll-be-testing-jev-extensively-this-week-and-figuring-o--2100895941717070056|Testes da ferramenta Jev]]", "[[extracts/x/bookmarks/2026-09-12-ibesh_tech-bcherny-the-review-bar-should-follow-blast-radius-not-who-wr--2098218598997336384|Code review e blast radius]]", "[[extracts/x/bookmarks/2026-09-16-schteppe-the-crap-change-risk-anti-patterns-metric-is-a-software-qual--2099728101366276474|Métrica CRAP de risco de mudança]]", "[[extracts/x/bookmarks/2026-09-12-dan_jeffries1-tell-me-you-have-zero-devops-skills-without-telling-me-you-g--2098411466697097235|Comparação LLM e malware]]"]
---

# Code-review workflow com julgamentos LLM

**@devagrawal09** · [2100341005690298687](https://x.com/devagrawal09/status/2100341005690298687) · `tool`

## Resumo
Jev Review é uma ferramenta local de code review que analisa Git diffs ou codebases completos usando julgamentos estruturados e limitados via TypeSafe Jev, com orquestração mantida em código e resultados em dashboard local. Vale salvar como referência de arquitetura em camadas para compor julgamentos de modelo rápidos e tipados em um pipeline de revisão.

## Pontos-chave
- Orquestração fica em código; Jev é usado apenas para julgamentos limitados em estágios: risk matrix -> score de perfis -> seleção de evidências -> classificação de mecanismo -> severidade -> roteamento condicional de revisores
- Dois pontos de entrada: revisão de diff (mudanças) e scan completo de codebase; usa testes alterados/relacionados como contexto ao julgar lacunas de cobertura
- Avalia correção, segurança, confiabilidade, compatibilidade e cobertura de testes; seleciona hunks concretos do diff antes de pontuar impacto; thresholds e política de workflow aplicados em código (não no modelo)
- Arquitetura em camadas com dependência só descendente (cli/dashboard -> review -> adapters -> domain), enforced por script que falha o build em imports ascendentes ou ciclos; dashboard binda em 127.0.0.1 e nunca serve arquivos de ambiente
- Limitações explícitas: sem diagnósticos de compilador, analisadores estáticos ou indexação de repositório; achados são prompts de revisão, não prova de defeito

## Links
- https://github.com/devagrawal09/jev-review

## Entidades
Jev Review, TypeSafe AI, Jev, Node.js, Git, npm, @devagrawal09

> **Revisit:** `high` · **fonte:** `article`
