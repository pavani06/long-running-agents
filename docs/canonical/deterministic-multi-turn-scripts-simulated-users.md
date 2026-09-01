---
title: "Deterministic Multi-Turn Scripts over Simulated Users"
type: canonical
aliases: ["multi-turn determinístico", "hardcoded user turns", "scripts contra simulated users"]
tags: ["evals", "agentes-orquestracao"]
last_updated: 2026-08-31
relates-to: ["[[docs/canonical/n-plus-one-long-session-evals|N+1 Long-Session Evals]]", "[[docs/canonical/repeatable-agent-spot-check-set|Repeatable Agent Spot-Check Set]]", "[[docs/canonical/production-grounded-eval-sampling|Production-Grounded Eval Sampling]]", "[[docs/canonical/living-eval-dataset|Living Eval Dataset]]", "[[docs/canonical/eval-tier-stratification|Eval Tier Stratification]]", "[[docs/canonical/structured-partial-checks-exact-goldens|Structured Partial Checks over Exact Goldens]]"]
sources: ["[[docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-patterns|Clay Eval Stack Patterns]]"]
---
# Deterministic Multi-Turn Scripts over Simulated Users

**Type:** canonical
**Status:** active
**Source:** Inside Clay's Eval Stack (LangChain) — `docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/`
**Classification:** Partial Coverage — Integration value: Medium (P2)
**Precedence:** document-level 2 (canonical) per `docs/system-of-record.md`

---

## Problem

Avaliar agentes multi-turn com um **simulated-user LLM** adiciona um segundo agente não determinístico ao sistema sob teste. O simulador é ruidoso, envelhece junto com os modelos, precisa dos próprios updates e das próprias evals — uma cauda de manutenção que na fonte "ended up not being worth it". Pior: com dois agentes variando, uma falha não diz qual dos dois regrediu; o eval perde o poder de isolamento que é sua razão de existir.

O problema não é simular usuários em si; é pagar não-determinismo duplo num mecanismo cujo trabalho é produzir comparações estáveis entre prompts e harnesses.

## Solution

Avaliar multi-turn com **user turns fixos e scriptados**:

1. **Hardcoded user turns** — o roteiro da conversa é um fixture; o comportamento do usuário não varia entre runs.
2. **Seed conversations derivadas de traces reais** — quando scripted puro é pouco representativo, os turnos são derivados de conversas reais de produção (realismo sem não-determinismo: o trace é congelado no fixture).
3. **Agente sob teste como único elemento variável** — determinismo por construção; diff entre runs é atribuível ao agente.
4. **Condições de fim de conversa explícitas** — o fixture declara quando a conversa termina e qual é o turno alvo da asserção.
5. **Decisão explícita contra simulated-user LLM** — o trade é documentado: o simulador só se justifica se a manutenção dele ficar abaixo do valor; na prática, turnos hardcoded foram "the most useful" formato multi-turn.

## Implementation in this repo

### What already exists

A mecânica central existe canonizada:

- [[docs/canonical/n-plus-one-long-session-evals|N+1 Long-Session Evals]] carrega um fixture fixo de N turnos (user turns hardcoded/derivados de traces reais) e testa o turno N+1: "Load a realistic N-turn conversation fixture. Apply the production context strategy. Ask the next-turn prompt..." (`docs/canonical/n-plus-one-long-session-evals.md:28-38`) — multi-turn determinístico por construção; `:38` — fixtures incluem follow-ups que referenciam produtos/decisões anteriores.
- Fixtures derivados de conversas reais: [[docs/canonical/repeatable-agent-spot-check-set|Repeatable Agent Spot-Check Set]] — 4 traces KODA reais reconstruídos como casos repetíveis (`docs/canonical/repeatable-agent-spot-check-set.md:59-60`); replay infrastructure em [[docs/canonical/production-grounded-eval-sampling|Production-Grounded Eval Sampling]] (`docs/canonical/production-grounded-eval-sampling.md:40`).

### What is missing

A **decisão explícita contra simulated-user LLM** — o outro lado do trade:

1. Nenhum doc, código ou currículo discute simulated users como alternativa avaliada e rejeitada; o trade "segundo agente não determinístico que precisa dos próprios updates e evals; aposentar quando manutenção excede valor" não existe. NOT_FOUND: grep `user simulator|usuário simulado|simulated-user|agente usuário` em `docs/` → apenas auto-referências do pacote-fonte Clay.
2. Sem a decisão documentada, o padrão fica indefinido contra a alternativa: nada impede que alguém reintroduza um simulador sem conhecer o argumento contra.

Add:

1. Nota de decisão (postponed/rejected alternative) registrando simulated-user LLM como caminho avaliado e descartado, com o critério de manutenção-vs-valor.
2. Guia de autoria de fixtures multi-turn: hardcoded puro vs derivado de trace real, e quando cada um.
3. Convenção de condições de fim de conversa e turno-alvo nos fixtures.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Remove um componente cujo custo de manutenção excedeu o valor na fonte | Turnos fixos exploram só caminhos scriptados; drift conversacional não scriptado fica coberto |
| Determinismo isola o agente sob teste como único elemento variável | Cobertura cresce apenas com esforço de autoria de fixtures |
| Comparações determinísticas entre mudanças de prompt e harness | Realismo sacrificado; resultados superestimam robustez em conversas selvagens |
| Fixtures de traces reais dão representatividade sem não-determinismo | Traces congelados envelhecem; refresh depende do loop produção→offline |

## Relationship to Other Patterns

- **Same mechanics as:** [[docs/canonical/n-plus-one-long-session-evals|N+1 Long-Session Evals]] — o fixture N+1 é a implementação canônica do padrão no repo; este doc adiciona a decisão contra a alternativa (simulated user).
- **Uses:** [[docs/canonical/repeatable-agent-spot-check-set|Repeatable Agent Spot-Check Set]] e [[docs/canonical/production-grounded-eval-sampling|Production-Grounded Eval Sampling]] — fontes de fixtures derivados de produção.
- **Feeds:** [[docs/canonical/living-eval-dataset|Living Eval Dataset]] — fixtures de trace real são casos do dataset vivo.
- **Fits in:** [[docs/canonical/eval-tier-stratification|Eval Tier Stratification]] — suites multi-turn determinísticas são tier medium/deep por runtime.
- **Complements:** [[docs/canonical/structured-partial-checks-exact-goldens|Structured Partial Checks over Exact Goldens]] — a asserção sobre o turno-alvo segue a mesma regra de estrictez casada com estabilidade.

## References

- `docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-patterns.md:143` — definição original do padrão.
- `docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-classification.md` — §7, classificação Partial Coverage/Medium com evidência.
- `docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-classification-batch-1.md` — batch-fonte da classificação.
- `docs/canonical/n-plus-one-long-session-evals.md:28-38` — fixture fixo de N turnos, turno N+1 como alvo.
- `docs/canonical/repeatable-agent-spot-check-set.md:59-60` — traces KODA reconstruídos como casos repetíveis.
- `docs/canonical/production-grounded-eval-sampling.md:40` — replay infrastructure.

---

*Created: 2026-08-31 | From: Clay Eval Stack classification | Precedence: canonical*
