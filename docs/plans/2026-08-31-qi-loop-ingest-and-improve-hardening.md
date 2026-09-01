# Plano QI Loop iter3 — Hardening ingest-and-improve + pipeline + harness

- **Data:** 2026-08-31
- **Origem:** review adversarial Oracle (bg_6fbc0a9f) sobre a execução `Uny6LpmjraI` (commits 19e0845..c40cae1)
- **RECs:** `~/.reflection/qi-loop-iter3-recommendations-ingest-hardening.md` (13 RECs, 23 findings)
- **Repos:** RK = `/mnt/c/Users/pavan/raw-knowledge` · LRA = `/mnt/c/Users/pavan/long-running-agents`
- **Epic:** issue criada em pavani06/long-running-agents (hub; commits pousam nos repos de cada arquivo)

## Tarefas → issues (mapeamento)

| Issue | REC | Sev | Repo/arquivo | Tarefa |
|---|---|---|---|---|
| 1 | REC-001 | P0 | RK wrapper SKILL.md | Fallback de resolução cross-repo do harness + `harness_resolution` no report |
| 2 | REC-002 | P1 | RK wrapper SKILL.md | Step -1 hard gate: target-repo único, dedup subordinado, RAW_REPO/TARGET_REPO imutáveis |
| 3 | REC-003 | P1 | RK wrapper SKILL.md | Step 1.5 disposition gate + Commit Gate RK + report "5 itens" + Gates |
| 4 | REC-004 | P1 | LRA analyze SKILL.md | Unificação 0-pre/0a: deltas read-only antes de decidir; incremental=true não pula gates |
| 5 | REC-005 | P1 | LRA analyze SKILL.md | Contrato Passo 0c: PHASE0_BASE_COMMIT, schema com base_commit, cp filenames, timing gate |
| 6 | REC-006 | P1 | LRA analyze SKILL.md | Write-assignment formal (OWNED_FILES/FORBIDDEN_FILES, batches ≤8, numbering de exercícios, Phase 6 por arquivo) |
| 7 | REC-007 | P2 | LRA analyze SKILL.md | Bundle P2: Phase 2 INLINE/FILE, Phase 5 recount total, Missing example dentro do exercise |
| 8 | REC-008 | P1 | LRA harness SKILL.md + templates/test-results.json | verification_checks auditáveis + ban de evidence vazio |
| 9 | REC-009 | P1 | LRA harness SKILL.md | Invariantes de duração/timestamp + validação pré-summary |
| 10 | REC-010 | P1 | LRA harness SKILL.md + analyze SKILL.md (Commit Gate) | Cadência: commit plan nomeado, 1 aprovação por plano, push separado |
| 11 | REC-011 | P2 | RK youtube-transcript SKILL.md | RUN_DATE/RUN_TZ_OFFSET/RUN_TIMESTAMP_UTC + serpapi no template de log |
| 12 | REC-012 | P1 | LRA mapa-mental-repo/ + harness/test-results.json | Reparo de estado: base_commit no yaml versionado, verification_checks retroativos (15 samples re-executados), durações derivadas de git |
| 13 | REC-013 | P1 | RK sources/ + log.md | Disposição da source: commit + push; deference entry do indexer |

## Ondas de execução

Grafo: dentro de um mesmo arquivo as edições são seriais (evita conflito de edit); cadeias distintas rodam em paralelo.

- **Onda 1** (4 cadeias paralelas):
  - Cadeia A (RK wrapper): 1 → 2 → 3
  - Cadeia B (LRA analyze): 4 → 5 → 6 → 7
  - Cadeia C (LRA harness): 8 → 9 → 10 (10 toca analyze SKILL.md: só após B concluir)
  - Cadeia D (RK youtube): 11
- **Onda 2** (estado, após onda 1):
  - 12 (depende de 5, 8, 9)
  - 13 (depende de 3)

## Re-verificação (determinística, por REC)

- REC-001: grep "Resolução cross-repo" + "harness_resolution" no wrapper
- REC-002: grep "exatamente um candidato|RAW_REPO" + ordem Step -1 antes de Step 0
- REC-003: grep "Step 1.5|deference|5 itens" + Gates listam disposition
- REC-004: grep "read-only" no Passo 0 + frase "nunca gates" em incremental=true
- REC-005: grep "PHASE0_BASE_COMMIT" + "base_commit" no schema + cp com `<date>-<source-slug>-mental-model`
- REC-006: grep "OWNED_FILES" + "particione por arquivo"
- REC-007: grep "INLINE" + "FILE" na Phase 2; "recomputada do filesystem" cobrindo canonicals na Phase 5; ação Missing sem "+ example"
- REC-008: grep "verification_checks" + proibição de evidence vazio; template JSON tem o campo
- REC-009: grep "duration_seconds" invariante + validação de timestamps
- REC-010: grep "commit plan" no harness + Commit Gate do pipeline alinhado
- REC-011: grep "RUN_TIMESTAMP_UTC" + "serpapi" no template de log
- REC-012: `python3 -c yaml` no yaml versionado tem meta.base_commit; `git log --name-only <base>..HEAD` retorna >10 paths; test-results.json tem verification_checks não vazio nas phases 0-3 e durações ≥ 0 coerentes com timestamps
- REC-013: `git -C RK status --short` vazio para sources/log; `git -C RK log -1 --stat` mostra a source page; deference entry no log.md

## Encerramento

- [ ] 13 issues fechadas com handoff
- [ ] P0/P1 zerados, P2 resolvidos (REC-007, REC-011)
- [ ] Comentário de encerramento no epic: finding → correção → issue → commit
- [ ] Plano carimbado; state.json atualizado; PR-less (commits diretos, estilo do repo)

## Execução

- [ ] Iniciada: 2026-08-31
- [ ] Onda 1: _
- [ ] Onda 2: _
- [ ] Re-verificação: _
- [ ] Epic fechado: _
