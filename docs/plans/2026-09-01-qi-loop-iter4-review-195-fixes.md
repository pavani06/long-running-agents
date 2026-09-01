---
title: "QI-loop iter 4: correções do adversarial review da execução da issue #195"
type: plan
date: 2026-09-01
aliases: ["qi-loop iter 4", "plano correções review 195", "epic 197"]
tags: ["governanca", "harness-engineering"]
relates-to: ["[[docs/plans/2026-08-31-adversarial-review-pipeline-hardening|Pipeline Hardening Round 2]]"]
---

# QI-loop iter 4 — Plano: correções do adversarial review da issue #195

**Data:** 2026-09-01 · **RECs:** `~/.reflection/qi-loop-iter4-recommendations.md` · **Fonte:** `~/sisyphus-runtime/docs/analysis/2026-09-01-adversarial-review-issue-195-execution.md`
**Epic host:** pavani06/long-running-agents (precedente iter 3, epic #181; frontmatter do review declara `repo: long-running-agents`)
**Gating (pedido do operador):** Gate 1 = aprovação destes RECs + plano. Gate 2 = após criação do epic/issues, antes da execução. Fases 5-7 autônomas.

## Repos tocados

| Repo | Path | Issues |
|---|---|---|
| long-running-agents | `/home/pavanpavan/long-running-agents` | epic, T1, T7, T8 |
| opencode-config | `/home/pavanpavan/.config/opencode` | T2, T3, T4, T9 |
| scripts | `/home/pavanpavan/scripts` | T5, T9 |
| sisyphus-runtime | `/home/pavanpavan/sisyphus-runtime` | T5, T6, T10 (facts/docs) |
| local não-git | `~/.agents/skills/implement/` | T6 (edição local, documentada) |

## Ondas

### Onda 1 — Quick/paralelo (sem dependências)

| Issue | Tarefa | REC | Finding | Repo principal |
|---|---|---|---|---|
| T1 | Pin `@pavani/obsidian-eval` ^0.2.2→^0.2.1 + CI verde | REC-007 | F10, dívida #195 | LRA |
| T2 | issue-start: gates por blast radius + branch reuse + CI baseline | REC-005 | F9, F10 | opencode-config |
| T3 | issue-review (+review-work): router mecânico vs semântico | REC-006 | F10 | opencode-config |
| T4 | canonical-context: fail-fast sem taskContext | REC-012 | F8 | opencode-config |
| T5 | Script native-worktree + durable fact WSL | REC-003 | F2, F4 | scripts + sisyphus-runtime |
| T6 | Facts de disciplina I1-I4 (assert destrutivo, dry-run, baseline único, censo de formato) + skill implement local | REC-008..011 | F3-F6 | sisyphus-runtime + local |

### Onda 2 — Medium/paralelo (independentes entre si)

| Issue | Tarefa | REC | Finding | Repo principal |
|---|---|---|---|---|
| T7 | Validador `--checks/--paths/--json` + cache por hash | REC-001 | F2 | LRA |
| T8 | API YAML frontmatter (dry-run, atômico, manifesto, flow+block) | REC-004 | F3, F5 | LRA |
| T9 | Telemetria: finalização de sessão + correlação pai-filho task_calls | REC-002 | F1 | scripts + opencode-config |

### Onda 3 — Encerramento (depende de todas)

| Issue | Tarefa |
|---|---|
| T10 | Varredura documental (PROGRESS.md LRA, stamp deste plano, state.json, hands-offs) + comentário de fechamento do epic + re-verificação consolidada |

## Dependências

- T10 depende de T1-T9.
- Nenhuma outra dependência dura. Nota: T6 (fact de checks direcionados) referencia as flags do T7; como T6 é onda 1, o fact menciona as flags por contrato (`--checks/--paths`), não pela entrega — sem acoplamento.
- T7 e T8 tocam `scripts/` do LRA: commits separados, sem conflito de arquivo (validate-obsidian.ts vs novo módulo).

## Restrições transversais

- NÃO alterar conteúdo semântico de docs do vault LRA (só frontmatter/tooling/código).
- Stage seletivo: nunca `.env`, `.obsidian/`, `telemetry.db`, caches.
- Push autorizado nos 4 repos git como parte do fluxo (Gate 1/2).
- Commits conventional por repo; body de issues auto-contido (Epic/REC/Finding/Repo, Tarefas, Aceite, Depende/Desbloqueia, Handoff).
- task-wrapper.sh ausente → trace instrumentation pulada (desvio documentado).
- Fase 1 = diagnóstico reusado do review Oracle existente (desvio documentado, findings mecânicos com file:line).

## Re-verificação (Fase 6)

Um check determinístico por REC (comando + saída esperada), ex.: REC-007 `grep -q '"@pavani/obsidian-eval": "\^0.2.1"' package.json`; REC-001 run com `--paths` + 2ª run com cache hit; REC-002 query SQL com parent não-nulo; REC-004 dry-run não escreve + apply atômico em fixture; skills: grep dos critérios nos SKILL.md; facts: validador do runtime 0 erro nos novos facts.

## Carimbo de execução

(pendente — preencher na Fase 7)
