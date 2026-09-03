# PROGRESS.md — Análise de fonte externa

> Pipeline analyze-and-improve gerenciado pelo harness.
> Cada fase é uma feature com contrato default-FAIL.
> O harness avança automaticamente entre fases.

## Done

<!-- Fases concluídas e aprovadas pelo evaluator -->
<!-- Formato: - [x] phase-N: descrição - commit abc1234 [evaluator: PASS] -->

- [x] phase-0: Repository Mental Model [evaluator: PASS, semantic, 410s]
- [x] phase-1: Knowledge Extraction [evaluator: PASS, semantic, 531s]
- [x] phase-2: Pattern Extraction [evaluator: PASS, semantic, 420s]
- [x] phase-3: Classification [evaluator: PASS, semantic, 659s] (2 batches consolidados inline)
- [x] phase-4: Improvement Generation [evaluator: PASS, semantic] (10 canonical + 2 skills + 3 exercises + manifest)
- [x] phase-5: Integration [evaluator: PASS, semantic, 589s] (contagens recomputadas; SOR 196, skills 38)
- [x] phase-6: Curriculum Deep Integration [evaluator: PASS, semantic, 1017s] (2 batches, partição por arquivo; Passo 0c executado, cap 5 respeitado)

## In Progress

<!-- A fase atual. Exatamente UMA por vez. -->

- [ ] Commit Gate: plano nomeado apresentado, aguardando aprovação do operador

## Next

- [ ] Push (aprovação separada)

## Analysis Context

- **source**: /home/pavanpavan/raw-knowledge/sources/2026-09-02-the-prompting-playbook.md
- **date**: 2026-09-02
- **source-slug**: the-prompting-playbook
- **output_dir**: docs/analysis/2026-09-02-the-prompting-playbook/

## Notes

- Stack: Node.js, OpenCode agents, Obsidian-compatible markdown
- Rodar: não se aplica (análise de documento, não build de código)
- Testar: `npx tsx scripts/validate-obsidian.ts`
- Evidência: outputs em docs/analysis/2026-09-02-the-prompting-playbook/
- Commits: `git commit -m "analysis(the-prompting-playbook): <fase>"`
