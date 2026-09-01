---
title: "Unified Tool Surface Flywheel"
type: canonical
aliases: ["unified tool surface", "single tool authority", "flywheel de superfície única de tools", "UI CLI API parity", "agent tool failure as API signal"]
tags: ["agentes-orquestracao", "harness-engineering", "production"]
last_updated: 2026-08-31
relates-to:
  - "[[docs/canonical/file-system-materialization|File-System Materialization]]"
  - "[[docs/canonical/deterministic-tool-dispatch|Deterministic Tool Dispatch]]"
  - "[[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]]"
  - "[[docs/canonical/closed-loop-help-api|Closed-Loop Help API]]"
  - "[[docs/canonical/bulk-in-context-trace-analysis|Bulk In-Context Trace Analysis]]"
  - "[[docs/canonical/self-iterating-agent-loop|Self-Iterating Agent Loop]]"
sources:
  - "[[docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-patterns|Clay Eval Stack Patterns (2026-08-31)]]"
---

# Unified Tool Surface Flywheel

**Type:** Canonical Pattern
**Status:** Active
**Source:** Inside Clay's Eval Stack (300M Agent Runs, One LangSmith Pipeline) — LangChain, via `docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/`
**Classification:** Partial Coverage (P1) — integration value High
**Precedence:** Level 2 ([[docs/system-of-record|System of Record]])

---

## Problem

Divergência entre o que o produto expõe e o que os agentes internos usam duplica superfície de manutenção e esconde falhas (`docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-patterns.md:185-205`).

Quando agentes internos consomem tools paralelas às da UI/CLI/API públicas, cada superfície falha separadamente: um bug de tool do agente não ensina nada sobre a API pública, e uma melhoria na API não chega ao agente. O time paga N superfícies e colhe 1/N do sinal de falha.

## Solution

Uma **única autoridade de tool** exposta identicamente como UI, CLI e API pública, com agentes internos consumindo exatamente as mesmas tools que clientes externos (`...-patterns.md:190-192`):

1. **Uma implementação, três superfícies** — UI, CLI e API pública são renderizações da mesma tool authority, não caminhos de código separados.
2. **Agentes internos como consumidores das mesmas tools** — o agente de engenharia invoca a tool pública, não um backdoor interno.
3. **Cada falha de tool do agente dobra como sinal de qualidade da API pública** — o tráfego agêntico vira teste contínuo da superfície externa.
4. **Flywheel:** observações de falha de invocação (de bulk trace analysis e vibe review humana) → melhorias de tool e harness → benefício simultâneo para agentes internos, clientes externos e agentes externos (`...-patterns.md:192-196`).

Disciplina necessária: recusar tools backdoor exclusivas de agente — qualquer atalho interno quebra o casamento entre sinal agêntico e qualidade pública (`...-patterns.md:204`).

## Implementation in this repo

### What already exists

Os três elementos existem isolados (`...-classification.md:150-167`):

- **Interface universal para agentes** — [[docs/canonical/file-system-materialization|File-System Materialization]]: "Materialize everything into files, git, and grep... The file system is the universal interface that every coding model understands" (`docs/canonical/file-system-materialization.md:38`); o agente opera "using the same tools it would use for any software project" (`:48`) — o análogo mais próximo de universal tooling surface.
- **Autoridade única de dispatch** — [[docs/canonical/deterministic-tool-dispatch|Deterministic Tool Dispatch]] (12FA Padrão 2, `docs/system-of-record.md:178`): tools como JSON + código determinístico com dispatch único.
- **Metade falha-melhora do flywheel** — [[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]] (`docs/canonical/production-failure-regression-flywheel.md:28`): toda falha de produção vira caso de regressão durável — sem o lado API pública.
- **Loop de falha-para-aprimoramento voltado ao agente** — [[docs/canonical/closed-loop-help-api|Closed-Loop Help API]] (Kavak, `docs/system-of-record.md:312`): resolução vira training data.

### What is missing

A mecânica central (`...-classification.md:165`):

1. **Única tool authority servindo UI + CLI + API pública simultaneamente** — não existe; grep `tool surface|single tool|same tools|UI, CLI|UI/CLI|public API` em `*.md` do repo retorna apenas `file-system-materialization.md:48` e o pacote-fonte.
2. **Agentes internos como consumidores das mesmas tools de clientes externos** — o repo não tem produto com API pública consumida pelos próprios agentes.
3. **"Agent tool failure doubles as public API quality signal"** — a tese de produto que converte superfície única em multiplicador de pontos de captura de falha.
4. A própria auditoria Kavak registrou o gap: File-System Materialization é o análogo de "universal tooling surface", mas a implementação concreta é NOT_FOUND (`docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-classification.md:38`).

## Tradeoffs

| Benefit | Cost |
|---|---|
| Cada falha de tool do agente dobra como sinal de qualidade da API pública | Superfície pública de falha maior: falhas induzidas por agente ficam visíveis |
| Menos superfícies divergentes = mais pontos onde coletar sinal de falha | O design da API pública fica constrangido pelas necessidades do agente |
| Melhorias beneficiam agentes internos, clientes externos e agentes externos de uma vez | Exige disciplina para recusar tools backdoor exclusivas de agente |
| O tráfego agêntico vira teste contínuo e gratuito da superfície externa | A tool authority vira artefato crossroad: mudança afeta todos os consumidores |

## Relationship to Other Patterns

- **Compõe:** [[docs/canonical/file-system-materialization|File-System Materialization]] (substrato de interface universal) + [[docs/canonical/deterministic-tool-dispatch|Deterministic Tool Dispatch]] (autoridade de dispatch) + [[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]] (conversão falha→caso) sob uma tese de produto: superfície única como multiplicador de captura de falha.
- **Complementa:** [[docs/canonical/closed-loop-help-api|Closed-Loop Help API]] — loop de falha-para-aprimoramento voltado ao agente; aqui o loop volta-se para a superfície pública.
- **Recebe observações de:** [[docs/canonical/bulk-in-context-trace-analysis|Bulk In-Context Trace Analysis]] — detecção de tendências de falha de invocação alimenta o flywheel.
- **Generalizado por:** [[docs/canonical/self-iterating-agent-loop|Self-Iterating Agent Loop]] — o flywheel de tools é o caso específico; o loop auto-iterante estende a tese para o produto inteiro.

## References

- `docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-patterns.md:185-205` — definição original do padrão.
- `docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-classification.md:150-167` — classificação Partial Coverage/High com evidência.
- `docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-classification.yaml:166-182` — evidência estruturada.
- `docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-classification.md:38` — auditoria prévia: universal tooling surface NOT_FOUND.
- `docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-analysis.md` — extração de conhecimento da fonte.

---

*Created: 2026-08-31 | From: Clay eval stack classification (P1) | Precedence: canonical*
