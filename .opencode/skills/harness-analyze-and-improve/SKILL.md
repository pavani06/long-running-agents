---
name: harness-analyze-and-improve
description: "Executa o pipeline analyze-and-improve fase por fase via delegacao nativa task(). Suporta mode=once (uma fase) e mode=feature:phase-N (fase especifica). Dispara com: 'run harness', 'execute pipeline', 'harness --once', 'run phase-N', 'harness analyze and improve'."
license: MIT
compatibility: opencode
metadata:
  audience: all-agents
  workflow: orchestration
  priority: high
---

## What I Do

Orquestro a execucao do pipeline `analyze-and-improve` diretamente via `task()`, sem depender de sub-processo `opencode run` (que nao completa background agents corretamente).

Leio `PROGRESS.md` e `harness/test-results.json` para determinar a proxima fase pendente, delego para o agente apropriado conforme a prescricao da skill `analyze-and-improve`, e atualizo o progresso apos cada fase.

## Dual Execution Mechanism

O harness existe em duas formas. Use a correta para seu contexto:

| Mecanismo | Quando usar | Arquivo |
|---|---|---|
| **Skill harness** (esta skill) | Dentro de uma sessao opencode | `.opencode/skills/harness-analyze-and-improve/SKILL.md` |
| **Bash harness** | Terminal real (bash externo) | `harness/harness-analysis.sh` |

**Skill harness**: Usa `task()` nativo do opencode para delegar cada fase. Funciona dentro de sessoes opencode porque nao depende de sub-processo. Aproveita o sistema de background agents e continuacao de sessao do opencode.

**Bash harness**: Script shell que invoca `opencode run`. Util para automacao externa e CI/CD. Requer ambiente bash completo (grep, python3/jq, date, mkdir). Nao funciona quando invocado de dentro de uma sessao opencode.

Ambos leem os mesmos arquivos de contrato (`PROGRESS.md`, `harness/test-results.json`) e produzem os mesmos outputs. Sao intercambiaveis — voce pode alternar entre eles a qualquer momento.

## Invocation

| Param | Required | Description |
|---|---|---|
| `mode` | No | `once` (default), `loop` (todas as fases), ou `feature:<phase-N>` (fase especifica) |

Examples:
```
Load harness-analyze-and-improve with mode=once
Load harness-analyze-and-improve with mode=feature:phase-0
Load harness-analyze-and-improve with mode=loop
```

## Phase → Agent Mapping

Conforme `analyze-and-improve` SKILL.md:

| Phase | Agent | Category |
|---|---|---|
| phase-0 | ultrabrain | Repository Mental Model |
| phase-1 | deep | Knowledge Extraction |
| phase-2 | ultrabrain | Pattern Extraction |
| phase-3 | deep or ultrabrain | Classification |
| phase-4 | deep (parallel) | Improvement Generation |
| phase-5 | quick | Integration |
| phase-6 | deep | Curriculum Deep Integration |

> **Nota Phase 3**: Para classificacao com mais de 8 padroes, divida em lotes de no maximo 8 padroes por agente. Se `deep` abortar, use `ultrabrain` como fallback.

## Execution Flow

### Step 1: Read Context

Read these files to understand the current state:
- `PROGRESS.md` — analysis context (source, date, slug, output_dir)
- `harness/test-results.json` — phase contracts with passes/evaluated_by status

### Step 2: Determine Next Phase

Find the first phase in `test-results.json` where `passes` is `false`. Skip phases where `evaluated_by` is already set (they were evaluated but not passing — needs rework).

If `mode=feature:<phase-N>`, force that phase regardless of state.

### Step 3: Check Steering

Read `harness/templates/STEER.md`. If it has content beyond the placeholder, inject it as operator steering into the delegation prompt, then restore the placeholder template (do not leave the file empty).

### Step 4: Delegate Phase

Extract from PROGRESS.md:
- `source` (path to source document)
- `date` (YYYY-MM-DD)
- `source-slug` (short slug)
- `output_dir` = `docs/analysis/<date>-<source-slug>/`

Build a delegation prompt following the `analyze-and-improve` skill's prescription for that phase. Use `task()` with the correct category.

TARGET_REPOSITORY block in EVERY delegation — use absolute paths:
```
TARGET_REPOSITORY:
  path: <absolute-path-to-repo>
  name: <repo-name>
  output_dir: <absolute-path-to-repo>/docs/analysis/<date>-<source-slug>/
  system_of_record: <absolute-path-to-repo>/docs/system-of-record.md
  branch: main
```

**CRITICAL**: All file paths in delegation prompts must be absolute. Never use relative paths — agents may resolve them from wrong working directories.

### Step 5: Verify Output

After the delegation completes:
1. Read each evidence file listed in `test-results.json` for that phase
2. Confirm files exist and have substantial content
3. Log evidence to `harness/.evidence-reads` (one path per line)

### Step 6: Evaluate

Run a self-check:
- Do output files exist and have substantial content?
- Does content match the phase objective?
- Are Obsidian conventions followed (if applicable)? Check for mandatory fields: `type`, `tags`, `aliases`, `relates-to`.
- Run `bash scripts/check-obsidian-conventions.sh` (if available)

If PASS:
- Update `harness/test-results.json`: set `evaluated_by` to `"evaluator"` for that phase
- Update `PROGRESS.md`: use `write` to rewrite the file (not `edit`). PROGRESS.md is short and `edit` often fails on whitespace mismatches.

If NEEDS_WORK:
- Write findings to `NEXT_FINDINGS.md`
- Do NOT update test-results.json (so harness retries on next run)

### Step 7: Advance or Stop

- If `mode=once`: stop after one phase
- If `mode=feature:<phase-N>`: stop after that phase
- If `mode=loop`: go back to Step 2 for the next pending phase
- If no more pending phases: report completion

## Kill Switch

Before each phase, check if `AGENT_STOP` file exists at repo root. If yes, stop the loop.

## Commit Gate

NEVER commit without asking the user. After each phase completes:
1. Show `git diff --stat`
2. Ask: "Commit phase-N?"
3. If yes: commit with message `analysis(<slug>): phase <N>`
4. Ask: "Push?"
5. If yes: `git push`

## Anti-Patterns

- Executar fase diretamente em vez de delegar via `task()`
- Pular verificacao de output (ler os arquivos gerados)
- Esquecer o bloco TARGET_REPOSITORY na delegacao
- Usar paths relativos em delegacoes — sempre absolutos
- Commitar sem perguntar ao usuario
- Executar Phase 6 sem antes verificar se ha Missing ou Partial Coverage High
- Usar `edit` no PROGRESS.md — use `write` (reescrita completa)

## Reference

- Skill `analyze-and-improve`: pipeline specification with delegation patterns per phase
- `PROGRESS.md`: analysis context and phase tracking
- `harness/test-results.json`: contract per phase (passes, evidence, evaluated_by)
- `harness/harness-analysis.sh`: bash harness para execucao externa
