# PROGRESS.md — Análise de fonte externa

> Pipeline analyze-and-improve gerenciado pelo harness.
> Cada fase é uma feature com contrato default-FAIL.
> O harness avança automaticamente entre fases.

## Done

<!-- Fases concluídas e aprovadas pelo evaluator -->

## In Progress

<!-- A fase atual. Exatamente UMA por vez. -->

## Next

<!-- Próximas fases na fila -->

## Notes

- Stack: Node.js, OpenCode agents, Obsidian-compatible markdown
- Rodar: não se aplica (análise de documento, não build de código)
- Testar: `npx tsx scripts/validate-obsidian.ts`
- 2026-09-01 — QI Epic iter 4 (#197): correções do adversarial review da execução da #195. S1-S6 + I5/I7 + pin `@pavani/obsidian-eval`; I1-I4/I6 como disciplina (fact/skill). 9 issues fechadas com handoff; re-verificação 10/10 PASS; CI main verde. Plano: `docs/plans/2026-09-01-qi-loop-iter4-review-195-fixes.md` (commits neste repo: `8650a01`, `be9f48d`, `be9143e`, `7638ec7`; demais em agent-skills, opencode-config, scripts e sisyphus-runtime).
