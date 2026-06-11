# PROGRESS.md — Análise de fonte externa

> Pipeline analyze-and-improve gerenciado pelo harness.
> Cada fase é uma feature com contrato default-FAIL.
> O harness.sh avança automaticamente entre fases.

## Done

<!-- Fases concluídas e aprovadas pelo evaluator -->
<!-- Formato: - [x] phase-N: descrição - commit abc1234 [evaluator: PASS] -->

## In Progress

<!-- A fase atual. Exatamente UMA por vez. -->

- [ ] phase-0: Repository Mental Model
  - Output esperado: docs/analysis/<date>-<slug>/mental-model.md + .yaml
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

- **source**: /mnt/c/Users/pavan/raw-knowledge/sources/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock.md
- **date**: 2026-06-07
- **source-slug**: full-walkthrough-workflow-for-ai-coding-matt-pocock
- **output_dir**: docs/analysis/<date>-<source-slug>/

## Notes

- Stack: Node.js, OpenCode agents, Obsidian-compatible markdown
- Rodar: não se aplica (análise de documento, não build de código)
- Testar: `bash scripts/check-obsidian-conventions.sh`
- Evidência: outputs em docs/analysis/<date>-<slug>/
- Commits: `git commit -m "analysis(<slug>): <fase>"`
