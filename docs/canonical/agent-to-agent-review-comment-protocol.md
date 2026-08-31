---
title: "Agent-to-Agent Review Comment Protocol"
type: canonical
tags: ["code-review", "agentes-orquestracao", "agentic-coding"]
Status: Active
Source: "AI Engineer talk — Itamar Friedman, Qodo (The Last Human Code Review: Building Trust in AI-Generated Code)"
Classification: "Partial Coverage (P2, Medium integration value)"
Precedence: "Level 2 (docs/system-of-record.md)"
last_updated: 2026-08-31
aliases: ["agent to agent review comment", "agent-parseable review comment", "dear agent comment", "background fix task", "fix PR cherry-pick"]
relates-to:
  - "[[docs/canonical/semantic-rule-gated-auto-approve-block|Semantic-Rule-Gated Auto Approve/Block]]"
  - "[[docs/canonical/generator-evaluator|Generator-Evaluator]]"
  - "[[docs/canonical/qa-to-backlog-feedback-loop|QA-to-Backlog Feedback Loop]]"
  - "[[docs/canonical/shadow-review-pipeline|Shadow Review Pipeline]]"
  - "[[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]]"
sources:
  - "[[docs/analysis/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co-patterns|Source Patterns]]"
  - "[[docs/analysis/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co-classification|Classification]]"
  - "[[docs/analysis/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co-analysis|Knowledge Extraction]]"
---

# Agent-to-Agent Review Comment Protocol

**Type:** Canonical Pattern
**Status:** Active
**Source:** AI Engineer talk — Itamar Friedman, Qodo ([The Last Human Code Review: Building Trust in AI-Generated Code](https://www.youtube.com/watch?v=s-aixZYJG4c))
**Classification:** Partial Coverage (P2, Medium integration value)
**Precedence:** Level 2 ([[docs/system-of-record|System of Record]])

---

## Problema

Um reviewer automatizado precisa passar **estado utilizável** para o próximo agente que tocar o PR, não apenas exibir achados para humanos (`docs/analysis/...-patterns.md:87`). Review comment endereçado a humano força o próximo agente a redescobrir os issues do zero — o estado de review morre na interface humana.

O problema é de contrato de interface: sem um formato agent-parseable que carregue o estado do review (quais issues, quais regras, quais fixes prontos), o loop fecha no humano em vez de fechar no próximo agente.

## Solução

Comentário estruturado endereçado ao próximo agente + fix pré-computado como artefato (`docs/analysis/...-analysis.md:62-64`): "Hey dear agent, Qodo just reviewed this PR and has found five different issues. Qodo already spent some background task and used Claude Code for example harness in order to do fixes and there is a closed PR... with all the fixes". O agente seguinte ganha "a cherrypicking moment" com "all the code that is actually passing your rules your standard".

| Componente | Função |
|---|---|
| Comentário agent-addressed | Achados do review (N issues) estruturados num formato agent-parseable, endereçado ao próximo agente do PR |
| Background fix task | Harness (Claude Code citado na demo) executa as correções em background |
| Fix-PR fechado | PR contendo os fixes como artefato consumível, não como instrução de refazer |
| Cherry-pick pelo próximo agente | O agente seguinte parte do código que já passa as regras/standards |
| Regras aplicadas | O conjunto de regras que o código deve passar referencia a camada codificada |

Fluxo (`docs/analysis/...-patterns.md:91-95`): review automatizado encontra N issues → publica comentário endereçado ao próximo agente → dispara background fix task via harness → fix-PR fechado com as correções → o próximo agente cherry-picks o código aderente às regras → o review humano reduz-se a cherry-picking de fixes pré-verificados.

## Implementação neste repositório

### O que já existe

Os ingredientes existem em profundidade canônica, mas nenhuma peça é o protocolo (classification:89-96):

- **Veredito com feedback estruturado:** [[docs/canonical/generator-evaluator|Generator-Evaluator]] — "The Evaluator is impartial and constraint-facing: it receives the candidate output, reads persisted client state, applies quality rubrics and business rules, and returns an approve or reject verdict with specific feedback" (`docs/canonical/generator-evaluator.md:31`) — loop de mesma iteração, não estado cross-session de PR.
- **Findings como trabalho claimable:** [[docs/canonical/qa-to-backlog-feedback-loop|QA-to-Backlog Feedback Loop]] — "The new issues enter the Agent Kanban with severity labels, QA-intake metadata (source PR, finding ID, reviewer), and blocker relationships. Agents claim them through the normal ready-queue flow" (`docs/canonical/qa-to-backlog-feedback-loop.md:42`).
- **Findings estruturados por check:** [[docs/canonical/shadow-review-pipeline|Shadow Review Pipeline]] — outputs incluem "Non-blocking AI review trace for each change" e "Data-backed threshold decisions: which checks graduate to blocking" (`docs/canonical/shadow-review-pipeline.md:62-65`) — endereçados a humanos/dashboard.
- **Review de segundo agente:** o issue-review skill "validates the worktree, creates a draft PR, runs second-agent review, and stops before merge" (`docs/canonical/pr-gated-eval-enforcement.md:61`) — review-to-human, não review-to-next-agent.

### O que falta

(classification:96) — greps `cherry-pick|cherry pick` em `docs/` matched apenas dentro do próprio pacote-fonte; `dear agent|agent-to-agent|agent-parseable|background fix|fix task` em `docs/canonical/` matched só [[docs/canonical/architecture-as-agent-affordance|Architecture as Agent Affordance]] (`:24`, `:26`, `:30`), onde "next agent" significa navegabilidade de codebase, não contrato de comentário:

1. **Contrato de comentário agent-addressed** — nenhum formato de comentário carrega estado de review para o próximo agente que toca o PR.
2. **Background fix task como artefato** — não existe noção de tarefa de correção disparada em background pelo reviewer, produzindo PR fechado consumível.
3. **Endgame do cherry-pick** — a inversão "human review reduz-se a cherry-picking de fixes pré-verificados" está inteiramente ausente do corpus.

## Tradeoffs

| Benefício | Custo |
|---|---|
| O próximo agente começa do estado do review em vez de redescobrir os issues | Depende de harness com execução de background task |
| Fixes chegam pré-computados como artefatos, não como instruções de refazer | O formato do comentário precisa ser agent-parseable para carregar estado |
| Review humano reduz-se a cherry-picking de código que já passa as regras | Cherry-pick assume fixes confiáveis e verificáveis contra as regras |

## Relação com outros padrões

- **Completa o loop de:** [[docs/canonical/generator-evaluator|Generator-Evaluator]] — o veredito com feedback ganha um envelope cross-session endereçado ao próximo agente.
- **Roteia como:** [[docs/canonical/qa-to-backlog-feedback-loop|QA-to-Backlog Feedback Loop]] — findings como trabalho claimable; aqui o trabalho chega pré-executado (fix-PR), não apenas enfileirado.
- **Consome output de:** [[docs/canonical/shadow-review-pipeline|Shadow Review Pipeline]] — os findings estruturados por check são o payload natural do comentário agent-addressed.
- **Referencia as regras de:** [[docs/canonical/semantic-rule-gated-auto-approve-block|Semantic-Rule-Gated Auto Approve/Block]] — o "passing your rules your standard" do cherry-pick pressupõe regras codificadas.
- **Fronteira com:** [[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]] — o fluxo repo para no merge para revisão humana; este protocolo é o degrau que fecharia o loop no próximo agente antes dessa parada.

## Referências

- `docs/analysis/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co-patterns.md:84-103` — padrão extraído: problema, inputs, outputs, benefícios, limitações.
- `docs/analysis/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co-classification.md:85-98` — classificação Partial Coverage (Medium) com evidência e NOT_FOUND de cherry-pick.
- `docs/analysis/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co-analysis.md:60-64` — demo do protocolo: comentário "dear agent", background fix via harness, PR fechado, cherry-pick.
- `docs/canonical/generator-evaluator.md:31` — veredito approve/reject com feedback específico.
- `docs/canonical/qa-to-backlog-feedback-loop.md:42` — findings como issues claimable no Agent Kanban.
- `docs/canonical/shadow-review-pipeline.md:62-65` — outputs estruturados do shadow review.
- `docs/canonical/pr-gated-eval-enforcement.md:61` — issue-review skill: second-agent review que para antes do merge.
