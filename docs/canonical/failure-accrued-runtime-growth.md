---
title: "Failure-Accrued Runtime Growth"
type: canonical
tags: ["harness-engineering", "production", "decision-discipline", "evals"]
aliases: ["runtime como sedimento das falhas", "failure-accrued runtime", "mapa falha-primitiva", "paguei a divida conforme ela aparecia", "accrual por erro"]
last_updated: 2026-09-02
relates-to:
  - "[[docs/canonical/pull-based-infrastructure-on-pain|Pull-Based Infrastructure on Pain]]"
  - "[[docs/canonical/pain-signal-eval-progression-gate|Pain-Signal Eval Progression Gate]]"
  - "[[docs/canonical/symphony-trap-awareness|Symphony Trap Awareness]]"
  - "[[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]]"
  - "[[docs/canonical/append-only-causal-event-log|Append-Only Causal Event Log]]"
  - "[[docs/canonical/content-addressed-prompt-graph|Content-Addressed Prompt Graph]]"
  - "[[docs/canonical/agent-kernel-runtime|Agent Kernel Runtime]]"
sources:
  - "[[docs/analysis/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt-analysis|Analise Agent Frameworks Considered Harmful]]"
  - "[[docs/analysis/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt/classification|Classification: Agent Frameworks Considered Harmful]]"
---

# Failure-Accrued Runtime Growth

**Type:** Canonical Pattern
**Status:** Active
**Source:** AI Engineer — Remi Louf (.txt), "Agent Frameworks Considered Harmful" (2026-08-22)
**Classification:** Partial Coverage (P2, Medium integration value)
**Precedence:** Level 2 ([[docs/system-of-record|System of Record]])

---

## Problema

Design upfront de runtime produz pecas especulativas sem justificativa observada — o risco exato que [[docs/canonical/pull-based-infrastructure-on-pain|Pull-Based Infrastructure on Pain]] canonicaliza ("Adicionar infraestrutura reativamente, na sequencia em que sua ausencia vira o binding constraint", `:43`) e que o proprio pull-on-pain registra como escopado demais no repo: aplicado so a capacidade de eval e governanca de harness (`:77-81`).

Este padrao e a **instanciacao do principio em granularidade de primitiva de runtime**: o mapa 1:1 de cada falha de producao observada para a peca minima de runtime que a elimina, na ordem em que a falha apareceu — "paguei a divida conforme ela aparecia" (analysis.md:92-93). E o contraponto explicito ao design upfront de "agent operating systems".

## Solucao

O runtime como **sedimento das falhas**, nao design anterior a elas (analysis.md:212-213). Cada modo de falha real de producao gera exatamente uma peca (analysis.md:86-90):

| Falha observada em producao | Peca do runtime que nasceu dela | Canonical desta familia |
|---|---|---|
| Nota de voz sumiu (nada persistido entre passos) | Log append-only — "tudo salvo para sempre" | [[docs/canonical/append-only-causal-event-log|Append-Only Causal Event Log]] |
| Brief postado 2x no Slack (multiplas tentativas sem contagem, sem dedup) | Fila propriamente dita: contagem de tentativas + dedup | (fila com retry/dedup: sem canonical proprio) |
| Prompt destruido sem regressao rastreavel (market brief virou lixo apos semana de tweaks) | Prompts content-addressed | [[docs/canonical/content-addressed-prompt-graph|Content-Addressed Prompt Graph]] |

Regras operacionais:

1. **Uma falha, uma peca minima** — nada especulativo: cada componente do runtime tem uma justificativa observada (patterns.md:172).
2. **A ordem e a ordem das falhas** — o sequenciamento e descoberto, nao planejado (mesma regra do pull-on-pain, `:58-59`).
3. **A primeira versao e rapida e incompleta** — ~1 dia com Codex; o resto do tempo vai para modos de falha e runtime (analysis.md:183).
4. **As falhas sao o metodo, nao o acidente** — o sistema quebra em producao primeiro porque a producao e a unica fonte de justificativa (patterns.md:176).

## Implementacao neste repositorio

### O que ja existe

O principio em profundidade canonica, escopado a eval e governanca de harness (classification.md:161-165):

- [[docs/canonical/pull-based-infrastructure-on-pain|Pull-Based Infrastructure on Pain]]:43 — adicao reativa quando a ausencia vira binding constraint; tabela 1:1 infra ← dor `:45-52`; "Cada investimento responde a uma restricao sentida, nao a especulacao" e "O sequenciamento e descoberto, nao planejado" `:56-59`.
- [[docs/canonical/pain-signal-eval-progression-gate|Pain-Signal Eval Progression Gate]] — maturidade gateada por pain signals; "smallest eval capability that addresses the observed pain" com tabela de triggers (classification.md:162).
- [[docs/canonical/symphony-trap-awareness|Symphony Trap Awareness]] — anti-upfront-spec: especificacoes emergem de sistemas rodando; "build then distill" (`:27, :33`).
- [[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]] — falha vira ativo duravel no **output de eval**, nao em primitiva de runtime (classification.md:164).

### O que falta

(classification.md:165-166) — o proprio pull-on-pain declara NOT_FOUND para a generalizacao full-stack; nenhum doc mapeia incidentes nomeados a primitivas de runtime interno na ordem de aparecimento:

1. **O mapa 1:1 falha-de-producao → primitiva-de-runtime** (journal/queue/content-addressing) com a ordem de aparecimento registrada.
2. **O framing "runtime como sedimento das falhas"** — o acumulado tem historia causal, nao roadmap.
3. **A aplicacao do pull-on-pain a pecas de kernel** — log causal, fila com dedup, content addressing como pecas justificadas falha a falha, fortalecendo o cross-reference com [[docs/canonical/agent-kernel-runtime|Agent Kernel Runtime]].

## Tradeoffs

| Beneficio | Custo |
|---|---|
| Nada especulativo: cada peca tem justificativa observada em producao | O sistema quebra em producao primeiro: as falhas sao o metodo |
| Contraponto pragmatico ao design upfront de "agent operating systems" | Exige observabilidade e producao real rodando para gerar as falhas |
| Primeira versao funcional rapida (~1 dia); o resto do tempo vai para modos de falha e runtime | Custo de estabilidade durante o acrescimo sucessivo de pecas |

## Relacao com outros padroes

- **Instancia:** [[docs/canonical/pull-based-infrastructure-on-pain|Pull-Based Infrastructure on Pain]] — mesmo principio pull-on-pain, agora em granularidade de primitiva de runtime (a tabela deste doc e a linha 1:1 daquele).
- **Herda o gate de:** [[docs/canonical/pain-signal-eval-progression-gate|Pain-Signal Eval Progression Gate]] — a menor peca que endereca a dor observada.
- **Companheiro anti-upfront de:** [[docs/canonical/symphony-trap-awareness|Symphony Trap Awareness]] — build then distill no nivel do runtime.
- **Contraparte de:** [[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]] — o flywheel converte falha em ativo de eval; este padrao converte falha em primitiva de runtime. Duas saidas para o mesmo incidente.
- **E o ledger de justificativa de:** [[docs/canonical/agent-kernel-runtime|Agent Kernel Runtime]] — cada peca do kernel entra com sua falha-fonte registrada; as pecas citadas sao [[docs/canonical/append-only-causal-event-log|Append-Only Causal Event Log]] e [[docs/canonical/content-addressed-prompt-graph|Content-Addressed Prompt Graph]].

## Referencias

- `docs/analysis/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt-analysis.md:81-94` — runtime como divida paga por falha: tabela falha → peca; "paguei a divida conforme ela aparecia".
- `docs/analysis/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt-analysis.md:212-213` — padrao transversal: o runtime e o sedimento das falhas.
- `docs/analysis/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt-patterns.md:160-178` — padrao 8 extraido: inputs, outputs, beneficios, limitacoes.
- `docs/analysis/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt/classification.md:154-168` — classificacao Partial Coverage (Medium) com evidencia file:line e NOT_FOUND do mapa runtime.
- [[docs/canonical/pull-based-infrastructure-on-pain|Pull-Based Infrastructure on Pain]]`:43, :45-52, :56-59, :77-81` — principio, tabela infra ← dor, regras, gap declarado.
- [[docs/canonical/symphony-trap-awareness|Symphony Trap Awareness]]`:27, :33` — anti-upstream; build then distill.
