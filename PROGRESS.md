# PROGRESS.md — Análise de fonte externa

> Pipeline analyze-and-improve gerenciado pelo harness.
> Cada fase é uma feature com contrato default-FAIL.
> O harness avança automaticamente entre fases.

## Done

- [x] qi-loop iter 1: skill-hardening adversarial findings (2026-08-31) — 8 findings (4 P1 / 4 P2) → REC-001..008 → epic #157 + issues #158-#167 → implementação (commits 1c927a4 RK, f19cb1d LRA) → re-verificação 8/8 PASS

<!-- Fases concluídas e aprovadas pelo evaluator -->

- [x] qi-loop iter 1: review-work 5-lane (2026-08-30) → 11 findings P0/P1 → REC-001..012 → 11 issues (#146-#156) → implementação → re-verificação 15/15 PASS
  - Commits: dfb67d8 (LRA) · e2d2a0d (RK) · Epic #145 fechado
  - Destaques: key hardening (stdin+mktemp+unset), untrusted source handling, Passo 0c executado, Sidekick completo (skill+exercise-08+índices), factory de certificação, contagens derivadas do YAML
  - Detalhes: docs/plans/2026-08-30-qi-loop-kavak-fixes.md

## In Progress

<!-- A fase atual. Exatamente UMA por vez. -->

## Next

<!-- Próximas fases na fila -->

## Notes

- Stack: Node.js, OpenCode agents, Obsidian-compatible markdown
- Rodar: não se aplica (análise de documento, não build de código)
- Testar: `npx tsx scripts/validate-obsidian.ts`
