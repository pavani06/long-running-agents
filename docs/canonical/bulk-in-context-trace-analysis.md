---
title: "Bulk In-Context Trace Analysis"
type: canonical
aliases: ["bulk trace analysis", "in-context trace analysis", "análise em massa de traces", "trend-finding over traces", "10k trace sample"]
tags: ["evals", "production", "harness-engineering"]
last_updated: 2026-08-31
relates-to:
  - "[[docs/canonical/centralized-cross-framework-tracing|Centralized Cross-Framework Tracing]]"
  - "[[docs/canonical/trace-instrumentation|Trace Instrumentation]]"
  - "[[docs/canonical/llm-classified-log-taxonomy|LLM-Classified Log Taxonomy]]"
  - "[[docs/canonical/behavioral-eval-path-analysis|Behavioral Eval Path Analysis]]"
  - "[[docs/canonical/production-to-offline-feedback-loop|Production-to-Offline Feedback Loop]]"
  - "[[docs/canonical/living-eval-dataset|Living Eval Dataset]]"
  - "[[docs/canonical/eval-coverage-matrix|Eval Coverage Matrix]]"
sources:
  - "[[docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-patterns|Clay Eval Stack Patterns (2026-08-31)]]"
---

# Bulk In-Context Trace Analysis

**Type:** Canonical Pattern
**Status:** Active
**Source:** Inside Clay's Eval Stack (300M Agent Runs, One LangSmith Pipeline) — LangChain, via `docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/`
**Classification:** Partial Coverage (P1) — integration value High
**Precedence:** Level 2 ([[docs/system-of-record|System of Record]])

---

## Problem

Vibe review de traces — humanos olhando um punhado de exemplos — não encontra tendências através de traces de produção em alto volume (`docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-patterns.md:310-329`).

A alternativa determinística (queries SQL sobre traces) responde perguntas já formuladas, mas não *descobre* perguntas; a alternativa de classificação LLM por item rotula cada trace numa taxonomia conhecida, mas não sintetiza tendências novas. O gap é qualitativo: ninguém "lê" o corpus inteiro.

## Solution

Submeter uma **amostra grande de traces (na ordem de 10.000 exemplos)** in-context a um frontier model, com goal de *trend-finding* (`...-patterns.md:315-321`):

1. **Amostra em escala** — ~10k traces de produção (não 5, não 50: o ponto é volume que nenhum humano lê).
2. **Frontier model como leitor** — o passo de capacidade (step change) de modelos frontier com contexto longo é o habilitador: conversão direta de melhoria de modelo em observabilidade (`...-patterns.md:325`).
3. **Goals e sub-agentes estruturam a análise** — a análise é agêntica e harnessada, não um prompt solto: goals de tendência, sub-agentes por fatia, consolidação de findings.
4. **Outputs:** relatórios de tendência sobre o corpus; padrões de falha candidatos; alimentação direta do loop produção→offline como casos-candidatos de eval e teste.

É o **substituto escalável do vibe review**: mesmo tipo de julgamento qualitativo, mas sobre o corpus inteiro amostrado, e re-executável.

Limitações estruturais (`...-patterns.md:327-329`): depende de um step change de capacidade (modelos menores não fazem); a análise em si é nondeterminística e precisa da própria validação; custo por passada não é trivial em escala de 10k exemplos.

## Implementation in this repo

### What already exists

A infraestrutura de trace e a análise por-item existem em profundidade (`...-classification.md:270-286`):

- **Infraestrutura de tracing** — [[docs/canonical/centralized-cross-framework-tracing|Centralized Cross-Framework Tracing]] (`docs/system-of-record.md:291`): schema unificado com text-to-SQL query interface e trace sampling em escala enterprise; [[docs/canonical/trace-instrumentation|Trace Instrumentation]] (tracer.ts, telemetry.db, span pipeline).
- **Classificação LLM em escala** — [[docs/canonical/llm-classified-log-taxonomy|LLM-Classified Log Taxonomy]] (`docs/canonical/llm-classified-log-taxonomy.md:48,53`): pipeline de classificação LLM sobre ~40k perguntas/semana com tiering de modelo e amostragem — mas **classificação por item em taxonomia**, não sintese in-context de tendências.
- **Análise comportamental determinística** — [[docs/canonical/behavioral-eval-path-analysis|Behavioral Eval Path Analysis]] (`docs/canonical/behavioral-eval-path-analysis.md:34`): Layer 3 consome a execução completa via algoritmos determinísticos; a própria doc registra que a lógica de consumo é NOT_FOUND no repo (`:158-165`).
- **Trace reading ensinado** — `curriculum/07-implementation-guides/05-trace-analysis-guide.md` e `curriculum/02-nivel-2-practical-patterns/04-trace-reading.md` (5.089 linhas, o maior arquivo do currículo).

### What is missing

O mecanismo in-context em massa (`...-classification.md:284`):

1. **Submissão in-context de amostra grande (~10k) a frontier model** — grep `10k examples|bulk trace|in-context.*trace|large trace sample` → sem mecânica fora do pacote-fonte; `10.000` ocorre apenas como escala de volume, nunca como tamanho de amostra de análise LLM.
2. **Prompts de trend-finding** — goals de descoberta de tendências sobre o corpus.
3. **Findings → novos eval cases como pipeline nomeado** — a ponta que conecta tendências detectadas ao growth do eval set.
4. **O reconhecimento do frontier-model step change como conversor direto em observabilidade** — a tese de que cada geração de modelo amplia o que é "legível".

Note a direção oposta existente no currículo: Always-On Monitoring comprime 10.000 conversas → 5 para revisão humana (`curriculum/05-core-concepts/08-evaluation-rubrics.md:5923`) — comprimir volume para humano, onde este padrão expande volume para o modelo.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Escala a revisão qualitativa ao volume de produção — substitui o vibe review de punhado de exemplos | Depende de step change de frontier model; modelos menores não fazem |
| Findings alimentam o loop produção→offline e crescem o eval set | A análise é ela própria nondeterminística e precisa de validação própria |
| Cada geração de modelo frontier converte-se diretamente em mais observabilidade | Custo por passada não-trivial em escala de 10k exemplos |
| Converte a infraestrutura de trace já existente (tracer, telemetry.db, spans) em detecção de tendências | Exige amostragem representativa — amostra enviesada produz tendências enviesadas |

## Relationship to Other Patterns

- **Consome infraestrutura de:** [[docs/canonical/centralized-cross-framework-tracing|Centralized Cross-Framework Tracing]] e [[docs/canonical/trace-instrumentation|Trace Instrumentation]] — o pipeline de spans é a matéria-prima.
- **Complementa:** [[docs/canonical/llm-classified-log-taxonomy|LLM-Classified Log Taxonomy]] — classificação por-item em taxonomia conhecida vs. síntese in-context de tendências novas; dois LLM-at-scale sobre o mesmo tráfego.
- **Complementa:** [[docs/canonical/behavioral-eval-path-analysis|Behavioral Eval Path Analysis]] — path analysis determinístico por caso vs. trend-finding qualitativo por corpus.
- **Alimenta:** [[docs/canonical/production-to-offline-feedback-loop|Production-to-Offline Feedback Loop]] e [[docs/canonical/living-eval-dataset|Living Eval Dataset]] — tendências detectadas viram casos de eval.
- **Ocupa quadrante de:** [[docs/canonical/eval-coverage-matrix|Eval Coverage Matrix]] — mecanismo offline/nondeterministic de descoberta.

## References

- `docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-patterns.md:310-329` — definição original do padrão.
- `docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-classification.md:270-286` — classificação Partial Coverage/High com evidência.
- `docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-classification.yaml:261-276` — evidência estruturada.
- `docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-analysis.md` — extração de conhecimento da fonte.

---

*Created: 2026-08-31 | From: Clay eval stack classification (P1) | Precedence: canonical*
