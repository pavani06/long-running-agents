---
title: "Continuous Re-Architecture Budget"
type: canonical
tags: ["harness-engineering", "governanca", "decision-discipline", "production"]
Status: Active
Source: "AI Engineer talk — Sait Izmit, Snowflake (GTM assistant: 6.000 usuários, ondas de skills/MCP/progressive disclosure)"
Classification: "Partial Coverage (P2, Medium integration value)"
Precedence: "Level 2 (docs/system-of-record.md)"
last_updated: 2026-08-30
aliases: ["re-architecture budget", "60-70/30-40 split", "portfolio split", "wave absorption budget"]
relates-to:
  - "[[docs/canonical/eval-investment-parity|Eval-Investment Parity]]"
  - "[[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]]"
  - "[[docs/canonical/garbage-collection-day-meta-loop|Garbage Collection Day Meta-Loop]]"
  - "[[docs/canonical/model-agnostic-agent-vm-harness|Model-Agnostic Agent-VM Harness]]"
  - "[[docs/canonical/deferred-ledger-agentic-work|Deferred-Ledger Agentic Work]]"
  - "[[docs/canonical/pull-based-infrastructure-on-pain|Pull-Based Infrastructure on Pain]]"
  - "[[docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-analysis|GTM AI Agents Analysis]]"
sources:
  - "[[docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-patterns|GTM AI Agents Patterns]]"
  - "[[docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-classification|GTM AI Agents Classification]]"
---

# Continuous Re-Architecture Budget

**Type:** Canonical Pattern
**Status:** Active
**Source:** AI Engineer talk — Sait Izmit, Snowflake (GTM assistant: ondas de skills, MCP e progressive disclosure absorvidas em produção)
**Classification:** Partial Coverage (P2, Medium integration value)
**Precedence:** Level 2 ([[docs/system-of-record|System of Record]])

---

## Problema

Stacks de agente churnam em ondas (skills, MCP, progressive disclosure); times que alocam zero capacidade para absorção ou **congelam** em mecânicas legadas ou **trasham** de forma imprevisível (`docs/analysis/...-patterns.md:312-315`).

O dilema: cada onda de mecânica nova força uma escolha. Absorver cedo custa capacidade de feature agora; absorver tarde (ou nunca) deixa a stack presa a mecânicas que o ecossistema abandonou — e a migração tardia acontece sob pressão, quando dói, com reescrita emergencial em vez de pivot planejado. Sem uma alocação explícita, a escolha é feita sprint a sprint por pressão de deadline — que sempre vence — até que a dívida force o congelamento ou o thrash.

## Solução

Um **split de portfólio permanente**: 60-70% da capacidade de sprint em features/qualidade novas, 30-40% em re-arquitetura contínua (`docs/analysis/...-patterns.md:320-322`).

| Componente | Função |
|---|---|
| Regra de split de portfólio (60-70/30-40) | Alocação permanente, decidida uma vez, defendida contra pressão de feature |
| Watchlist de ondas de tecnologia | Vigiar mecânicas entrantes relevantes ao stack (skills, MCP, progressive disclosure) |
| Auditoria de drift vs. PRD | O design original do PRD como referência; ~80% persiste, drift é auditado |
| Trigger de pivot de mecânicas | Pivotar mecânicas cedo, dentro do budget, em vez de sob pressão |

Fluxo (`docs/analysis/...-patterns.md:336-341`): fixar o split permanente em steady state → vigiar ondas de mecânicas → pivotar mecânicas cedo dentro do budget de re-arquitetura → auditar drift contra o PRD original → manter o núcleo validado estável.

Propriedades resultantes (`docs/analysis/...-patterns.md:322-327`): o design central sobrevive ao churn (80% de persistência) porque mecânicas pivotam cedo em vez de sob pressão; capacidade compounding em vez de freeze legado; alocação previsível previne thrash e stagnação simultaneamente.

Riscos declarados (`docs/analysis/...-patterns.md:327-330`): imposto permanente de 30%+ sobre velocidade de feature; assume que o core design está certo — um core errado também persiste 80%; exige disciplina para que a re-arquitetura nunca coma o budget de feature.

## Implementação neste repositório

### O que já existe

Regras de alocação permanente e cadências de re-investimento existem para outras trilhas (classification:279-300):

- **Alocação de paridade para a trilha de eval:** [[docs/canonical/eval-investment-parity|Eval-Investment Parity]] — "standing parity allocation (agents 50% / evals 50%) as explicit accepted sprint budget" (`docs/canonical/eval-investment-parity.md:43-53`); capacidade de builder reduzida à metade aceita como decisão explícita (`:56`) — regra análoga de alocação permanente, trilha diferente.
- **Cadência de re-investimento de harness:** [[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]] — ciclo trimestral e regra One In One Out governando re-arquitetura de harness (`:60`).
- **Cadência semanal de manutenção:** [[docs/canonical/garbage-collection-day-meta-loop|Garbage Collection Day Meta-Loop]] — working session semanal (`:48`); cadência não negociável sob pressão de feature, time-boxed (`:54`).
- **Stance anti-rewrite por design:** [[docs/canonical/model-agnostic-agent-vm-harness|Model-Agnostic Agent-VM Harness]] — "design constraint: absorb model waves without rewrites" (`:36-37`); "fleet swaps by config change, not rewrite" (`:79`) — o repo evita reescrita tornando o harness model-agnostic, complementar ao budget.
- **Ledgers de retrabalho diferido:** Deferred-Ledger Agentic Work e Carry-Debt Sunset Gate como canonicals ativas (`docs/system-of-record.md:230, :234`).

### O que falta

(classification:294-300) — NOT_FOUND para `60-70`, `30-40`, portfolio split, wave watchlist, PRD drift/drift audit (apenas o pacote-fonte tem matches):

1. **O split de portfólio feature-vs-re-arquitetura** — 60-70/30-40 como alocação permanente; as regras existentes alocam paridade para evals, não portfólio para re-arquitetura.
2. **O watchlist de ondas de tecnologia** — vigilância deliberada de mecânicas entrantes como instrumento.
3. **A auditoria de drift contra o PRD** — com a alegação de 80% de persistência do design original como métrica de governança.

## Tradeoffs

| Benefício | Custo |
|---|---|
| Design central sobrevive ao churn (80% persiste) porque mecânicas pivotam cedo, não sob pressão | Imposto permanente de 30%+ sobre velocidade de feature |
| Capacidade compounding em vez de freeze legado | Assume core design certo — um core errado também persiste 80% |
| Alocação previsível previne thrash e stagnação | Exige disciplina: re-arquitetura nunca pode comer o budget de feature |
| Absorve ondas (skills, MCP, progressive disclosure) dentro de budget destinado | 30-40% é espaço de feature perdido todo sprint — visível para stakeholders |

## Relação com outros padrões

- **Estruturalmente análogo a:** [[docs/canonical/eval-investment-parity|Eval-Investment Parity]] — mesma forma de alocação permanente e defendida; trilha diferente (evals vs. re-arquitetura).
- **Executa dentro de:** [[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]] (cadência trimestral, One In One Out) e [[docs/canonical/garbage-collection-day-meta-loop|Garbage Collection Day Meta-Loop]] (cadência semanal) — o budget aloca capacidade; os lifecycles definem como gastá-la.
- **Reduz a necessidade de:** [[docs/canonical/model-agnostic-agent-vm-harness|Model-Agnostic Agent-VM Harness]] — absorver ondas por design reduz o custo que o budget precisa cobrir; as duas estratégias se reforçam.
- **Contabiliza a dívida de:** [[docs/canonical/deferred-ledger-agentic-work|Deferred-Ledger Agentic Work]] — retrabalho diferido entra no orçamento antes de virar sunset gate.
- **Paga a conta gerada por:** [[docs/canonical/pull-based-infrastructure-on-pain|Pull-Based Infrastructure on Pain]] — o lançamento mínimo gera o imposto de re-arquitetura que este budget aloca ("Incorres the permanent 30-40% re-architecture tax", `docs/analysis/...-patterns.md:298`).

## Referências

- `docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-patterns.md:312-341` — padrão extraído: split 60-70/30-40, watchlist, auditoria de drift, 80% de persistência.
- `docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-classification.yaml:279-300` — classificação Partial Coverage (Medium) com evidência e NOT_FOUND.
- `docs/canonical/eval-investment-parity.md:43-53, :56` — paridade como alocação permanente aceita.
- `docs/canonical/measured-harness-evolution-lifecycle.md:60` — ciclo trimestral e One In One Out.
- `docs/canonical/garbage-collection-day-meta-loop.md:48, :54` — cadência semanal não negociável.
- `docs/canonical/model-agnostic-agent-vm-harness.md:36-37, :79` — absorver ondas sem rewrites.
- `docs/system-of-record.md:230, :234` — deferred-ledger e carry-debt sunset como canonicals ativas.
