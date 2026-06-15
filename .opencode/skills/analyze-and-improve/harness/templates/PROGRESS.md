# PROGRESS.md — Análise de fonte externa

> Pipeline analyze-and-improve gerenciado pelo harness.
> Cada fase é uma feature com contrato default-FAIL.
> O harness avança automaticamente entre fases.

## Done

<!-- Fases concluídas e aprovadas pelo evaluator -->
<!-- Formato: - [x] phase-N: descrição - commit abc1234 [evaluator: PASS] -->

## In Progress

<!-- A fase atual. Exatamente UMA por vez. -->

- [ ] phase-0: Repository Mental Model
  - Output esperado: docs/analysis/{{DATE}}-{{SOURCE_SLUG}}/{{DATE}}-{{SOURCE_SLUG}}-mental-model.md + .yaml
  - Delegado: ultrabrain
  - Bloqueios: nenhum

## Next

- [ ] phase-1: Knowledge Extraction
- [ ] phase-2: Pattern Extraction
- [ ] phase-3: Classification
- [ ] phase-4: Improvement Generation
- [ ] phase-5: Integration
- [ ] phase-6: Curriculum Deep Integration (opcional)

## Analysis Context

- **source**: {{SOURCE}}
- **date**: {{DATE}}
- **source-slug**: {{SOURCE_SLUG}}
- **output_dir**: docs/analysis/{{DATE}}-{{SOURCE_SLUG}}/

## Notes

- Stack: Node.js, OpenCode agents, Obsidian-compatible markdown
- Rodar: não se aplica (análise de documento, não build de código)
- Testar: `npx tsx scripts/validate-obsidian.ts`
- Evidência: outputs em docs/analysis/{{DATE}}-{{SOURCE_SLUG}}/
- Commits: `git commit -m "analysis({{SOURCE_SLUG}}): <fase>"`
