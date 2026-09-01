---
title: "Production-to-Offline Feedback Loop with Drift Taxonomy"
type: canonical
aliases: ["production to offline loop", "drift taxonomy", "taxonomia de drift", "eval drift", "judge drift", "eval-set mirroring", "data drift"]
tags: ["evals", "production", "harness-engineering"]
last_updated: 2026-08-31
relates-to:
  - "[[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]]"
  - "[[docs/canonical/living-eval-dataset|Living Eval Dataset]]"
  - "[[docs/canonical/production-grounded-eval-sampling|Production-Grounded Eval Sampling]]"
  - "[[docs/canonical/eval-to-production-correlation-tracking|Eval-to-Production Correlation Tracking]]"
  - "[[docs/canonical/model-switch-driven-eval-hardening|Model-Switch-Driven Eval Hardening]]"
  - "[[docs/canonical/perceived-eval|Perceived-Eval]]"
  - "[[docs/canonical/bulk-in-context-trace-analysis|Bulk In-Context Trace Analysis]]"
sources:
  - "[[docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-patterns|Clay Eval Stack Patterns (2026-08-31)]]"
---

# Production-to-Offline Feedback Loop with Drift Taxonomy

**Type:** Canonical Pattern
**Status:** Active
**Source:** Inside Clay's Eval Stack (300M Agent Runs, One LangSmith Pipeline) — LangChain, via `docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/`
**Classification:** Partial Coverage (P1) — integration value High
**Precedence:** Level 2 ([[docs/system-of-record|System of Record]])

---

## Problem

Eval sets offline param de representar a produção *silenciosamente*: evals passando coexistem com o produto degradando. A fonte declara esse "the hardest part to set up" e um problema não resolvido em escala (`docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-patterns.md:58-79`).

O diagnóstico costuma ficar no nível indiferenciado de "os evals estão stale" — que esconde **três falhas distintas** com causas e remédios diferentes. Sem a separação, o time trata data drift com reanotação de goldens (custo alto, remédio errado) ou trata judge drift com refresh do dataset (não corrige nada).

## Solution

Dois componentes: o **loop** produção→offline (majoritariamente coberto pelo repo) e a **taxonomia de drift** (o delta deste padrão).

### O loop

Sinais de produção → refresh do eval set (`...-patterns.md:62-70`):

- **Sinais de entrada:** exemplos de online evaluators, tickets de suporte, eventos de perceived-eval (correções de usuário — ver [[docs/canonical/perceived-eval|Perceived-Eval]]).
- **Goldens anotados por humanos** como sinal de referência — é o que permite detectar overfitting do LLM-judge.
- **Use-case classifier** com tagging de casos de uso sobre traces de produção.
- **Outputs:** exemplos de eval refreshed puxados da produção; audit de cobertura comparando casos de uso testados vs. casos de uso reais.

### A taxonomia de drift — três modos

Diagnóstico diferencial para "evals stale" (`...-patterns.md:69`):

| Modo | O que derivou | Sinal característico | Remédio |
|---|---|---|---|
| **Data drift** | A distribuição de tráfego de produção mudou; o eval set testa o passado | Novos casos de uso aparecem no use-case tagging sem cobertura no eval set | Refresh por amostragem de produção; casos novos viram evals |
| **Judge drift** | O LLM-judge mudou de comportamento (troca de modelo, prompt, rubrica) | Divergência entre judge e goldens anotados por humanos nos mesmos casos | Reanotar/revalidar o judge contra goldens humanos; revalidação por troca de modelo |
| **Eval-set mirroring** | O eval set foi overfitado: o sistema decorou os casos do set sem generalizar | Score de eval alto com outcomes de produção estagnados ou caindo | Rotação de casos; novos casos de produção nunca vistos pelo dev loop |

O loop é declarado **não resolvido em escala**: sempre atrasa as mudanças de produção, exige instrumentação e trabalho humano de anotação, e o próprio use-case classifier pode rotular tráfego errado (`...-patterns.md:76-78`).

## Implementation in this repo

### What already exists

O loop produção→offline é o padrão mais coberto do pacote-fonte (`...-classification.md:47-61`):

- **Flywheel de 9 passos** — `docs/canonical/production-failure-regression-flywheel.md:28-41`: intake → capture → privacy → label → dedup → tier → backfill → link → prune.
- **Refresh cadence** — `docs/canonical/production-grounded-eval-sampling.md:41`: updates agendados e dirigidos por incidente.
- **Ciclo de vida do dataset** — `docs/canonical/living-eval-dataset.md:94-99`: incidente → caso permanente, com flywheel daemon e QI loop.
- **Detecção de decaimento** — `docs/canonical/eval-to-production-correlation-tracking.md:38-39`: decay thresholds + recalibration triggers (drift-adjacente, sem taxonomia nomeada).
- **Caso especial de judge drift** — [[docs/canonical/model-switch-driven-eval-hardening|Model-Switch-Driven Eval Hardening]] (`docs/system-of-record.md:301`): revalidação completa do dataset a cada troca de modelo — a resposta certa para um dos gatilhos de judge drift, sem nomear o modo de falha.

### What is missing

A taxonomia (`...-classification.md:59`):

1. **Os três modos nomeados** (data drift, judge drift, eval-set mirroring) — grep `judge drift|eval drift|eval-set|data drift|mirroring|stale eval` em `docs/canonical/` → 0 matches; os 121 hits de "drift" no repo são outros sentidos (context drift, model drift, drift de documentação).
2. **O protocolo de diagnóstico diferencial** — qual sinal discrimina qual modo e qual remédio corresponde a qual modo.
3. **Goldens anotados por humanos como referência anti-overfitting do judge** — o repo usa golden answers, mas não como controle de deriva do judge.
4. **Use-case classifier sobre traces de produção** como audit de cobertura do eval set.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Separa três falhas distintas em vez de brigar com um "evals stale" indiferenciado | Declarado não resolvido em escala — o loop sempre atrasa as mudanças de produção |
| Converte tickets de suporte e correções de usuário em combustível de eval de alta qualidade | Exige instrumentação de produção e trabalho humano de anotação |
| Goldens humanos dão referência para detectar overfitting do LLM-judge | O use-case classifier pode ele próprio rotular tráfego errado |
| Remédio certo por modo: evita gastar reanotação em data drift e refresh em judge drift | Manter a matriz modo→sinal→remédio exige disciplina de atualização |

## Relationship to Other Patterns

- **Depende do loop de:** [[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]] (captura), [[docs/canonical/production-grounded-eval-sampling|Production-Grounded Eval Sampling]] (refresh), [[docs/canonical/living-eval-dataset|Living Eval Dataset]] (ciclo de vida).
- **Recebe sinal de decaimento de:** [[docs/canonical/eval-to-production-correlation-tracking|Eval-to-Production Correlation Tracking]] — decay thresholds são o gatilho; esta taxonomia é o diagnóstico.
- **Especializa:** [[docs/canonical/model-switch-driven-eval-hardening|Model-Switch-Driven Eval Hardening]] — troca de modelo é um gatilho de judge drift; a revalidação completa é o remédio nomeado para esse subcaso.
- **Consome inputs de:** [[docs/canonical/perceived-eval|Perceived-Eval]] (correções de usuário) e [[docs/canonical/bulk-in-context-trace-analysis|Bulk In-Context Trace Analysis]] (tendências de falha como casos-candidatos).

## References

- `docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-patterns.md:58-79` — definição original do padrão.
- `docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-classification.md:47-61` — classificação Partial Coverage/High com evidência.
- `docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-classification.yaml:50-67` — evidência estruturada.
- `docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-analysis.md` — extração de conhecimento da fonte.

---

*Created: 2026-08-31 | From: Clay eval stack classification (P1) | Precedence: canonical*
