---
title: "Observability-Threshold Eval Trigger"
type: canonical
aliases: ["threshold de observabilidade", "gatilho estrutural de investimento em evals", "capacity-based eval trigger"]
tags: ["evals", "production", "governanca"]
last_updated: 2026-08-31
relates-to: ["[[docs/canonical/pain-signal-eval-progression-gate|Pain-Signal Eval Progression Gate]]", "[[docs/canonical/eval-investment-parity|Eval Investment Parity]]", "[[docs/canonical/eval-dashboard-primary-detection-surface|Eval Dashboard Primary Detection Surface]]", "[[docs/canonical/evals-as-brakes|Evals as Brakes]]", "[[docs/canonical/centralized-cross-framework-tracing|Centralized Cross-Framework Tracing]]", "[[docs/canonical/eval-tier-stratification|Eval Tier Stratification]]"]
sources: ["[[docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-patterns|Clay Eval Stack Patterns]]"]
---
# Observability-Threshold Eval Trigger

**Type:** canonical
**Status:** active
**Source:** Inside Clay's Eval Stack (LangChain; thresholds na fonte: 300M runs/mês, 100K mensagens/semana) — `docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/`
**Classification:** Partial Coverage — Integration value: Medium (P2)
**Precedence:** document-level 2 (canonical) per `docs/system-of-record.md`

---

## Problem

Times sub-investem em evals enquanto humanos ainda conseguem inspecionar cada trace — e batem num penhasco quando o volume torna a inspeção **estruturalmente impossível**. Ninguém consegue revisar 300M runs/mês; nenhum time de support consegue contatar todos os clientes relevantes de 100K mensagens/semana. Quando o penhasco chega, retrofitar evals em escala é muito mais caro do que tê-las começado antes.

O padrão também nomeia o oposto: **maturity theater** — investir em infraestrutura de eval antes que a estrutura exija, queimando esforço em evals pesadas para volumes que um humano ainda cobre sozinho. Faltava o gatilho que separa os dois regimes.

## Solution

Um **gatilho de decisão binário baseado em capacidade estrutural de observação**, não em dor sentida nem em roadmap:

1. **Medir volume continuamente** — runs/mês, mensagens/semana (o threshold só é detectado se o volume for medido; detecção tardia é o modo de falha).
2. **Modelar a capacidade humana de observação** — quantos traces um revisor cobre por semana; quantos clientes são contatáveis. É um modelo empírico por produto, não uma constante universal.
3. **Regra de decisão:** abaixo do threshold (humanos ainda conseguem inspecionar/contactar) → tolerar evals leves, sem culpa; acima do threshold (incapacidade estrutural de observar) → **investimento em evals torna-se não-negociável** — não é prioridade, é condição de operação.
4. **Nomear a condição de falha** — o crossing é um evento explícito ("structurally impossible to observe"), não um sentimento difuso de que as coisas pioraram.

Distinção-chave em relação ao gatilho por dor ([[docs/canonical/pain-signal-eval-progression-gate|Pain-Signal Eval Progression Gate]]): dor é **reativa** (sinal já observado, algo quebrou); threshold estrutural é **antecipativo** (a capacidade de observar desaparece antes de a dor acumular). Os dois se complementam: dor dispara o menor eval que resolve o problema observado; o threshold dispara o investimento estrutural quando a observação humana não é mais opção.

## Implementation in this repo

### What already exists

Gatilhos de investimento maduros, mas todos **pain-based**:

- [[docs/canonical/pain-signal-eval-progression-gate|Pain-Signal Eval Progression Gate]] — "eval maturity as a gate driven by pain signals instead of a calendar roadmap"; "Approve only the smallest eval capability that addresses the observed pain" (`docs/canonical/pain-signal-eval-progression-gate.md:28,36`).
- [[docs/canonical/pull-based-infrastructure-on-pain|Pull-Based Infrastructure on Pain]] — "stack mínimo de lançamento e endurecimento reativo puxado por dor, não por antecipação" (`docs/system-of-record.md:321`).
- Volume aparece como **sinal de fase**, não como threshold de capacidade: Fase 4 sai por "volume suficiente e representatividade aparente" (`docs/analysis/2026-06-10-eval-maturity-phases/2026-06-10-eval-maturity-phases-analysis.md:31`).
- Quanto investir (não quando se torna obrigatório): [[docs/canonical/eval-investment-parity|Eval Investment Parity]] (`docs/system-of-record.md:313`).
- A resposta ao volume sem o gatilho que a justifica: [[docs/canonical/eval-dashboard-primary-detection-surface|Eval Dashboard Primary Detection Surface]] (`docs/system-of-record.md:282`).

### What is missing

O gatilho capacity-based inteiro:

1. Nenhum modelo de capacidade de observação humana (traces reviewáveis por semana, clientes contatáveis). NOT_FOUND: grep `human observation|inspect every trace|observation capacity|maturity theater` em `*.md` → zero matches fora do pacote-fonte.
2. Métricas de volume comparadas contra essa capacidade (runs/mês vs capacidade de revisão).
3. A regra de decisão "structural inability to observe → eval investment non-negotiable". O framing de custo de volume existe (`docs/canonical/centralized-cross-framework-tracing.md:162` — "Trace volume at enterprise scale... demands significant storage and processing infrastructure"), mas como problema de infra, não como gatilho de investimento.

Add:

1. Um modelo de capacidade de observação por produto (traces/revisor/semana; clientes contatáveis/semana).
2. Dashboard de volume vs capacidade com linha de threshold e alerta de crossing.
3. Política: crossing do threshold entrou no roadmap de evals como item não-negociável, com nome ("structural inability to observe").

## Tradeoffs

| Benefit | Cost |
|---|---|
| Alinha investimento com necessidade estrutural em vez de maturity theater | Crossing detectado tarde se o volume não for medido continuamente |
| Evita engenharia de eval prematura enquanto a observação ainda é humanamente possível | Retrofitar evals em escala é mais caro do que começar antes |
| Nomeia a condição de falha que força a transição (300M runs/mês, 100K mensagens/semana na fonte) | Thresholds são valores empíricos por produto, não constantes universais |
| Complementa o gate de dor com um gatilho antecipativo | Modelar capacidade humana requer calibração empírica contínua |

## Relationship to Other Patterns

- **Complements:** [[docs/canonical/pain-signal-eval-progression-gate|Pain-Signal Eval Progression Gate]] — dor (reativo, menor capability que resolve) vs capacidade estrutural (antecipativo, investimento não-negociável); juntos cobrem os dois regimes de gatilho.
- **Answers "when":** [[docs/canonical/eval-investment-parity|Eval Investment Parity]] responde *quanto* investir; este padrão responde *quando* o investimento se torna obrigatório.
- **Justifies:** [[docs/canonical/eval-dashboard-primary-detection-surface|Eval Dashboard Primary Detection Surface]] — o dashboard como resposta primária ao volume é o que vem depois do crossing.
- **Measures via:** [[docs/canonical/centralized-cross-framework-tracing|Centralized Cross-Framework Tracing]] — a infraestrutura de tracing é a fonte das métricas de volume.
- **Feeds:** [[docs/canonical/eval-tier-stratification|Eval Tier Stratification]] e [[docs/canonical/evals-as-brakes|Evals as Brakes]] — o crossing define quando a suite precisa existir para que freios e tiers tenham o que governar.

## References

- `docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-patterns.md:291` — definição original do padrão.
- `docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-classification.md` — §14, classificação Partial Coverage/Medium com evidência.
- `docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-classification-batch-2.md` — batch-fonte da classificação.
- `docs/canonical/pain-signal-eval-progression-gate.md:28,36` — gatilho pain-based (anel mais próximo).
- `docs/system-of-record.md:282,313,321` — dashboard de detecção, paridade de investimento, pull-based on pain.
- `docs/analysis/2026-06-10-eval-maturity-phases/2026-06-10-eval-maturity-phases-analysis.md:31` — volume como sinal de fase.
- `docs/canonical/centralized-cross-framework-tracing.md:162` — custo de volume de traces.

---

*Created: 2026-08-31 | From: Clay Eval Stack classification | Precedence: canonical*
