---
title: "Environment-Tiered Eval Fidelity"
type: canonical
aliases: ["fidelidade por ambiente", "environment fidelity tiers", "local staging production eval fidelity"]
tags: ["evals", "harness-engineering", "production"]
last_updated: 2026-08-31
relates-to: ["[[docs/canonical/eval-tier-stratification|Eval Tier Stratification]]", "[[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]]", "[[docs/canonical/production-grounded-eval-sampling|Production-Grounded Eval Sampling]]", "[[docs/canonical/eval-to-production-correlation-tracking|Eval-to-Production Correlation Tracking]]"]
sources: ["[[docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-patterns|Clay Eval Stack Patterns]]"]
---
# Environment-Tiered Eval Fidelity

**Type:** canonical
**Status:** active
**Source:** Inside Clay's Eval Stack (LangChain) — `docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/`
**Classification:** Partial Coverage — Integration value: Medium (P2)
**Precedence:** document-level 2 (canonical) per `docs/system-of-record.md`

---

## Problem

Um único ambiente de eval enfrenta um dilema: ou reproduz a produção (lento, caro, bloqueia a iteração local) ou é rápido mas deriva do comportamento de produção. Times que fingem que os dois são o mesmo ambiente acabam EITHER com inner-loop travado OR com resultado local tratado como evidência de release — e o segundo caso é o perigoso: um eval local que não reproduz sandbox, virtual filesystem e dependências reais aprova mudanças que quebram em produção.

O problema não é ter ambientes distintos (local, staging, produção); é **não declarar o contrato de fidelidade de cada um**. Sem esse contrato, ninguém sabe quais claims cada ambiente pode sustentar.

## Solution

Estratificar evals por **ambiente** com um contrato explícito de fidelidade por tier — um eixo distinto do eixo velocidade/trigger de [[docs/canonical/eval-tier-stratification|Eval Tier Stratification]]:

| Ambiente | Contrato de fidelidade | Papel |
|---|---|---|
| Local | **Intencionalmente low-fidelity** — sem sandbox, sem virtual filesystem, sem dependências reais | Barato e rápido por design; sustenta o hábito de rodar evals constantemente; **não sustenta claims de release** |
| Staging | **Paridade máxima com produção** — "basically using the same thing as prod" (mesmo harness, mesmas dependências) | Sustenta claims de pré-release; shadow tests e dashboards baseline/candidate vivem aqui |
| Production | Fidelidade por definição | Canary, métricas online, observabilidade |

Mecanismo:

1. **Tier assignment por tipo de eval** — cada eval declara em qual ambiente roda; a suite local aceita perder fidelidade em troca de velocidade.
2. **Local deliberadamente incompleto** — a ausência de sandbox/VFS é uma decisão, não um atraso de implementação; bugs que só reproduzem com dependências reais são aceitos como fuga conhecida do tier local.
3. **Staging compartilha o harness de produção** — mesma CLI, mesmo pipeline, só muda o alvo (`--env staging`); paridade é de facto, mantida por construção.
4. **Claims de release só em tiers com paridade** — resultados locais não gateiam produção; a regra explícita interrompe a pretensão de que "passou local = pronto".
5. **"Meet your developers where they are"** — o tier local otimiza o workflow existente do dev (terminal, pre-commit), não o workflow ideal da plataforma.

## Implementation in this repo

### What already exists

As camadas de ambiente existem na prática do currículo e do playbook:

- [[docs/canonical/eval-tier-stratification|Eval Tier Stratification]] atrela o tier Fast a "Local change, pre-commit, small PR" (`docs/canonical/eval-tier-stratification.md:34`) — camada local existe, classificada por eixo runtime.
- O playbook do harness já opera staging como ambiente separado com paridade de facto: config `staging_shadow` (`curriculum/07-implementation-guides/06-harness-evolution-playbook.md:913`), "Shadow test em staging por 2 dias" (`:1743`), execução dia-D começando em staging com dashboard baseline/candidate (`:1802-1848`), teste de rollback em staging (`:1691`), e a mesma CLI apontando para outro ambiente — `koda shadow-tests start budget_guard_removal --env staging --duration 48h --sample 100` (`:1823`).
- `docs/canonical/eval-tier-stratification.md:58` reconhece que o playbook já separa lint/unit checks, regression batteries, N+1 long-session gates, staging shadow tests e canary phases.

### What is missing

O contrato de fidelidade por tier não está formalizado em lugar nenhum:

1. Nenhum doc declara o tier local como **intencionalmente low-fidelity** (sem sandbox/VFS) nem nomeia as fugas aceitas.
2. Nenhum doc formula a regra "**só tiers com paridade de produção sustentam claims de release**".
3. NOT_FOUND: grep `local.*sandbox|fidelity|paridade|parity` em `curriculum/07-implementation-guides/06-harness-evolution-playbook.md` → 0 matches para sandbox/fidelity/parity; a paridade staging/produção é de facto (mesma CLI), nunca nomeada como contrato.

Add:

1. Um campo `environment` (local/staging/production) com contrato de fidelidade no metadata de tier de [[docs/canonical/eval-tier-stratification|Eval Tier Stratification]].
2. Declaração explícita das fugas conhecidas do tier local (o que ele não pode detectar).
3. Regra de gate: PRs e releases exigem evidência de tier com paridade; resultado local vale como sinal de inner-loop apenas.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Velocidade local sustenta o hábito de rodar evals constantemente | Tier local sabidamente carece de fidelidade; seus resultados não podem gatear claims de produção |
| Fidelidade de staging preserva a validade do sinal para decisões de release | Manter paridade staging/produção custa engenharia contínua |
| Tiering explícito interrompe a pretensão de que resultado local = resultado de produção | Bugs que só reproduzem com sandbox/VFS/dependências reais escapam do tier local |
| Mesma CLI e mesmo harness em staging/produção reduzem drift de ferramenta | Dashboards e dependências de staging duplicam infraestrutura |

## Relationship to Other Patterns

- **Complements:** [[docs/canonical/eval-tier-stratification|Eval Tier Stratification]] — eixos ortogonais: stratification por velocidade/trigger (fast/medium/deep) define **quando** cada eval roda; fidelity por ambiente define **em que condições** e qual claim o resultado sustenta.
- **Enables:** [[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]] — o gate de PR precisa saber quais ambientes produzem evidência admissível.
- **Uses:** [[docs/canonical/production-grounded-eval-sampling|Production-Grounded Eval Sampling]] — replay de produção é o mecanismo natural do tier de maior fidelidade.
- **Feeds:** [[docs/canonical/eval-to-production-correlation-tracking|Eval-to-Production Correlation Tracking]] — a correlação só é mensurável quando o ambiente do eval tem paridade declarada.

## References

- `docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-patterns.md:36` — definição original do padrão (inputs/outputs/benefits/limitations).
- `docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-classification.md` — §2, classificação Partial Coverage/Medium com evidência.
- `docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-classification-batch-1.md` — batch-fonte da classificação.
- `docs/canonical/eval-tier-stratification.md:34,58` — tiers por runtime; camadas de ambiente já separadas no playbook.
- `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:913,1691,1743,1802-1848,1823` — staging_shadow, rollback, shadow tests, dashboard baseline/candidate, mesma CLI com `--env staging`.

---

*Created: 2026-08-31 | From: Clay Eval Stack classification | Precedence: canonical*
