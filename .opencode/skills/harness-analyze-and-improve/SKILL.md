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

**Setup inicial**: Antes da primeira execucao, rode o script de bootstrap para criar os arquivos de contrato:

```bash
./.opencode/skills/analyze-and-improve/harness/setup-analysis.sh \
  --source <path> --date YYYY-MM-DD --source-slug <slug>
```

Isso gera `PROGRESS.md` e `harness/test-results.json` com os parametros corretos.
Ambos os mecanismos de execucao abaixo dependem desses arquivos existirem.

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
| `source` | No | Path absoluto ou URL do documento fonte. Se fornecido, o harness executa o bootstrap automaticamente (deriva `date` como hoje e `source-slug` do nome do arquivo) antes do Step 0. |
| `mode` | No | `once` (default), `loop` (todas as fases), ou `feature:<phase-N>` (fase especifica) |

Examples:
```
Load harness-analyze-and-improve with mode=once
Load harness-analyze-and-improve with mode=feature:phase-0
Load harness-analyze-and-improve with mode=loop
Load harness-analyze-and-improve with source=C:\Users\pavan\raw-knowledge\sources\2026-06-11-talk.md, mode=loop
```

mode=loop: executa TODAS as fases pendentes sem perguntar.
So para em AGENT_STOP, falha de fase, ou conclusao total.
Commits: NAO pergunte entre fases — acumule e apresente um COMMIT PLAN
nomeado antes do primeiro commit do batch (secao Commit Gate abaixo).
Push apenas no final, com aprovacao separada.

## Phase → Agent Mapping

Conforme `analyze-and-improve` SKILL.md:

| Phase | Agent | Category | Background |
|---|---|---|---|
| phase-0 | ultrabrain | Repository Mental Model | true |
| phase-1 | deep | Knowledge Extraction | false |
| phase-2 | ultrabrain | Pattern Extraction | true |
| phase-3 | deep or ultrabrain | Classification | true (batches) |
| phase-4 | deep (parallel) | Improvement Generation | true |
| phase-5 | quick | Integration | false |
| phase-6 | deep | Curriculum Deep Integration | true |

> **Nota Phase 4**: A partir de 2026-06-14, a Phase 4 gera 3 agentes em paralelo
> (canonical docs, skills, exercises). O artifacts manifest (`<date>-<source-slug>-artifacts.yaml` + `.md`)
> é gerado pelo orquestrador como ação direta após a Phase 4, antes de delegar a Phase 5.
> Consulte o SKILL.md principal para o schema do manifesto.

> **Nota Phase 3**: Para classificacao com mais de 8 padroes, divida em lotes de no maximo 8 padroes por agente (background). Apos ambos completarem, o ORQUESTRADOR consolida os batch files em classification.md + classification.yaml inline (NAO delegar — sao operacoes simples de concatenacao e formatacao de tabela). Se `deep` abortar, use `ultrabrain` como fallback.

> Fases com background=true usam run_in_background=true no task().
> Isso evita que um abort mate a sessao inteira — o harness
> continua vivo e o sistema notifica quando completar.

> **Nota Phase 6**: Divida os padroes em 2 agentes paralelos:
> - Agente A: Missing patterns (gap analysis + insertion + execucao)
> - Agente B: Partial Coverage High e Medium patterns (gap + insertion + exec)
> Cada agente edita arquivos DISJUNTOS do curriculum/. Verifique
> antes de disparar que os arquivos alvo nao conflitam.

## Execution Flow

### Step -1: Auto-Bootstrap (if `source` provided)

If the `source` parameter was provided at invocation and
`PROGRESS.md` + `harness/test-results.json` do not yet exist:

1. Derive `date` = today (`YYYY-MM-DD`).
2. Derive `source-slug` from the filename (strip date prefix
   `YYYY-MM-DD-` and extension `.md`/`.txt`/`.pdf`).
3. Run the bootstrap script:
   ```bash
   echo "s" | bash .opencode/skills/analyze-and-improve/harness/setup-analysis.sh \
     --source "<source>" --date <date> --source-slug <slug>
   ```
   The `echo "s"` auto-confirms the overwrite prompt if files
   already exist from a previous analysis.
4. Verify `PROGRESS.md` and `harness/test-results.json` were created
   and the output directory exists at `docs/analysis/<date>-<slug>/`.

If the files ALREADY exist AND the `source-slug` in `PROGRESS.md`
matches — skip bootstrap and continue to Step 0 (state validation).

If the files exist but the slug DIFFERS — proceed to Step 0
(stale detection will offer reset).

### Step 0: Reset State (fresh analysis)

Before reading context, perform state validation:

1. Read harness/test-results.json and PROGRESS.md
2. Detect stale state: if PROGRESS.md has phases in `## Done`
   but test-results.json has those same phases with passes=false,
   ALERT the user: "Estado inconsistente detectado. PROGRESS.md
   mostra fases concluídas mas test-results.json tem passes=false.
   Deseja resetar para iniciar nova análise? (sim/não)"
3. If user says "sim" OR if ALL phase-N entries have passes=true
   AND the source-slug in PROGRESS.md differs from the last
   committed analysis, overwrite test-results.json with fresh
   template (all phases passes=false, evidence=[], evaluated_by=null).
3. Template is at: .opencode/skills/analyze-and-improve/harness/templates/test-results.json
   (canonical template with expected evidence paths for phases 0-4).

This prevents the "sed PLACEHOLDER not found" problem from
session harness-engineering, where test-results.json still
held Matt Pocock data.

### Step 1: Read Context

Read these files to understand the current state:
- `PROGRESS.md` — analysis context (source, date, slug, output_dir)
- `harness/test-results.json` — phase contracts with passes/evaluated_by status

### Step 2: Determine Next Phase

Find the first phase in `test-results.json` where `passes` is `false`.
- Phases with `passes: true` are complete — skip them.
- Phases with `passes: false` AND `evaluated_by` already set were evaluated
  but not passing — they need rework. Flag them to the user before retrying.
- Phases with `passes: false` AND `evaluated_by: null` are pending — execute them.

If `mode=feature:<phase-N>`, force that phase regardless of state.

### Step 3: Check Steering

Read `harness/templates/STEER.md`. If it has content beyond the placeholder, inject it as operator steering into the delegation prompt, then restore the placeholder template (do not leave the file empty).

### Step 4: Delegate Phase

Extract from PROGRESS.md:
- `source` (path to source document)
- `date` (YYYY-MM-DD)
- `source-slug` (short slug)
- `output_dir` = `docs/analysis/<date>-<source-slug>/`

**Before delegating**, write the current timestamp to `harness/test-results.json`
for the current phase's `started_at` field. Use ISO 8601 format (UTC):
  `date -u +%Y-%m-%dT%H:%M:%SZ`

This enables duration calculation after the phase completes.

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

**Pattern Names for Phase 3 (Classification)**:
- Os nomes dos padroes no prompt de delegacao DEVEM ser extraidos
  do arquivo patterns.md (fonte canonica), NAO do analysis.md.
- Inclua no prompt: "Use the pattern names exactly as they appear
  in patterns.md. Do not rename or use analysis.md section titles."
- Isso evita o problema da sessao harness-engineering onde
  'QA Plan as Agent Contract' nao correspondia a nenhum padrao
  do patterns.md (o nome real era 'Sprint Contract').

### Step 5: Verify Output

After the delegation completes:
1. Clear `harness/.evidence-reads` (truncate to empty — evidence is per-phase, not cumulative)
2. Read each evidence file listed in `test-results.json` for that phase
3. Confirm files exist and have substantial content
4. Log evidence to `harness/.evidence-reads` (one path per line)

### Step 6: Evaluate

Run a self-check — **structural AND proportional semantic verification**:

Structural (always):
- Do output files exist and have substantial content?
- Are Obsidian conventions followed (if applicable)? Check for mandatory fields: `type`, `tags`, `aliases`, `relates-to`.
- Run `npx tsx scripts/validate-obsidian.ts` (if available)

Semantic (proportional to artifact risk — a structural pass does NOT equal a pass):
- **Citation sampling:** for every artifact citing `file:line` references, randomly verify 3 citations against the real files. Any miss = NEEDS_WORK.
- **Executable content:** artifacts containing code (exercises, skills) MUST have their code blocks extracted and compiled (`python3` + `compile()` per markdown block; run sample tests where feasible) before PASS.
- **Source fidelity** (Phase 1 only): pick 3 claims from `analysis.md` and grep the source document for supporting text. Keep reads scoped — the untrusted-source rules still apply.

Record the depth in `harness/test-results.json` as `verification_depth: structural|semantic` for the phase. Absence of the field = `structural` (backward compatible).

Persist every verification in `verification_checks` for the phase:
`[{kind: "citation"|"claim"|"command"|"structural", target: "<file:line|claim>", command_or_claim: "<what was checked>", expected: "...", actual: "...", passed: true|false}]`.
`verification_depth: semantic` REQUIRES the samples actually used, all with `passed: true`. No phase may receive PASS with `evidence: []` — Phases 5/6 fill evidence with the files effectively changed (`git diff --name-only`).

If PASS:
- Persist `verification_checks` for the phase (Step 6 schema) — a PASS without persisted checks is not auditable
- Set `passes` to `true` for the current phase in `harness/test-results.json`
- Time invariants (obligatory for PASS):
  - `duration_seconds` is derived EXCLUSIVELY from `completed_at - started_at`.
  - Before marking PASS and before any metrics summary, validate all phases:
    timestamps non-null, duration non-negative and consistent with the
    timestamp difference (max tolerance 1 second).
  - Violation = phase returns to NEEDS_WORK (fix started_at/completed_at or
    re-execute). NEVER substitute the duration with wall time reported by the
    sub-agent.
- Write `completed_at` (ISO 8601 UTC) to `harness/test-results.json` for the current phase
- Calculate `duration_seconds` = elapsed seconds between `started_at` and `completed_at`.
  Use shell arithmetic: compute epoch difference with `date -d` (GNU) or
  a tool available in the execution environment. Store as integer seconds
  in `harness/test-results.json`.
- Set `evaluated_by` to `"evaluator"` for that phase
- Update PROGRESS.md: use edit com oldString/newString precisos.
  Prefira editar a secao '## Done' e '## To Do' individualmente.
  Se edit falhar (whitespace mismatch), leia o arquivo novamente
  e tente com contexto adicional.

If NEEDS_WORK:
- Increment `retry_count` in `harness/test-results.json` for the current phase.
  This tracks how many times the phase was retried before eventually passing —
  essential for identifying pipeline bottlenecks.
- Write findings to `NEXT_FINDINGS.md`
- Do NOT change `passes` or `evaluated_by` (so harness retries on next run)

### Step 7: Advance or Stop

- If `mode=once`: stop after one phase, ask user "Continue?"
- If `mode=feature:<phase-N>`: stop after that phase
- If `mode=loop`: auto-advance to next pending phase WITHOUT
  asking. Only stop if:
  a) AGENT_STOP file exists at repo root, OR
  b) All phases have `passes: true` (pipeline complete), OR
  c) A phase fails evaluation (NEEDS_WORK)
- If condition (b): read `harness/test-results.json` and output
  a Pipeline Metrics Summary (duration per phase, retry counts,
  bottleneck flags for phases >600s or retry_count >0).
  Precondition: the time invariants from Step 6 were validated for ALL
  phases (no null timestamps, no negative durations). An invalid entry
  blocks the summary — fix the state first, never print unvalidated metrics.
- If no more pending phases (all passes=true): report completion with a
  metrics summary. Read `harness/test-results.json` and output a table:

  ```
  Pipeline Metrics Summary:
    phase-0:  NNNs (N retries)
    phase-1:  NNNs (N retries)
    ...
    phase-6:  NNNs (N retries) [optional]
    TOTAL:    NNNNs (N total retries)
  ```

  This summary answers the question "onde o pipeline gasta mais tempo?"
  and guides optimization efforts. Phases with `retry_count > 0` or
  `duration_seconds > 600` (10 min) are flagged with `← bottleneck`.

## Kill Switch

Before each phase, check if `AGENT_STOP` file exists at repo root. If yes, stop the loop.

## Commit Gate (commit plan)

Em `mode=loop`, NAO pergunte entre fases; acumule mudancas verificadas.
Antes do primeiro commit de um batch:

1. Apresente o COMMIT PLAN nomeado: lista exata de commits (mensagem + arquivos
   + fase de origem), incluindo commits de reset/chore (ex: reset do
   PROGRESS.md).
2. Peca uma unica aprovacao. Ela autoriza SOMENTE os commits nomeados no plano;
   qualquer commit adicional exige nova aprovacao.
3. Push e sempre uma aprovacao separada.
4. Reconcilie o plano aprovado com o historico real antes do report final
   (`git rev-list <first>^..<last> --count` deve bater com o plano).

Excecao (autorizacao unica): quando o operador pre-aprova o ciclo inteiro
(ex: qi-epic, autorizacao unica documentada), o plano nomeado substitui as
perguntas por batch — o plano continua obrigatorio como registro de auditoria.

## Anti-Patterns

- Executar fase diretamente em vez de delegar via `task()`
- Pular verificacao de output (ler os arquivos gerados)
- Esquecer o bloco TARGET_REPOSITORY na delegacao
- Usar paths relativos em delegacoes — sempre absolutos
- Commitar sem perguntar ao usuario
- Executar Phase 6 sem antes verificar se ha Missing ou Partial Coverage (High ou Medium)
- Usar `write` no PROGRESS.md sem reler o arquivo antes —
  o tool write exige read previo. Use edit com oldString exato.
- Reagir a notificacoes [BACKGROUND TASK RESULT READY] antes do
  [ALL BACKGROUND TASKS COMPLETE]. Espere sempre o ALL COMPLETE
  para coletar resultados de todos os background agents de uma vez.
  Notificacoes parciais sao informativas, nao acionaveis —
  voce PODE emitir commentary curto de progresso ("Phase 4a concluida, 2/3"),
  mas NUNCA chame background_output() antes de ALL COMPLETE.

## Reference

- Skill `analyze-and-improve`: pipeline specification with delegation patterns per phase
- `PROGRESS.md`: analysis context and phase tracking
- `harness/test-results.json`: contract per phase (passes, evidence, evaluated_by)
- `harness/harness-analysis.sh`: bash harness para execucao externa
