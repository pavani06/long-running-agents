---
title: "Caso de regressão: telemetria do qi-loop sem correlação pai-filho (2026-09-01)"
type: evidence
date: 2026-09-01
tags: ["testes-qa", "evals", "production", "harness-engineering"]
aliases: ["caso telemetria qi-loop", "qi-loop telemetry correlation break", "primeiro caso do failure flywheel"]
relates-to: ["[[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]]", "[[docs/analysis/2026-09-01-adversarial-review-cl-epic-3-territory|Adversarial review CL-EPIC 3]]", "[[docs/canonical/trace-instrumentation|Trace Instrumentation]]", "[[docs/evidence/README|README de docs/evidence]]"]
sources: ["vault:sisyphus-runtime/docs/analysis/2026-09-01-adversarial-review-issue-195-execution.md", "vault:sisyphus-runtime/sessions/runtime/2026-09-02-121647-sisyphus-handoff.md", "https://github.com/pavani06/long-running-agents/issues/195", "https://github.com/pavani06/long-running-agents/issues/211"]
---

# Caso de regressão: telemetria do qi-loop sem correlação pai-filho

**Tipo:** evidence
**Status:** capturado, correção pendente (backfill a executar)
**Origem:** execução da issue #195 (ciclo qi-loop) em 2026-09-01; detecção em review adversarial pós-merge do PR #196
**Schema:** definido em [[docs/evidence/README|README de docs/evidence]]

Este é o primeiro caso de regressão registrado em `docs/evidence/` pelo flywheel de [[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]] (issue #211, epic #208). A análise-fonte do incidente vive fora deste repo, no vault de runtime; por isso é referenciada com a sintaxe cross-vault sancionada pelo ADR Vault Federation (`docs/decisions/2026-09-01-vault-federation-consultable-registry.md`), nunca como wikilink.

## ID do caso

`2026-09-01-qi-loop-telemetry-correlation-break` (o slug do arquivo é o identificador canônico, AGENTS.md Rule 16.5).

## Captura: interação e trace (passo 2)

Nenhum fixture bruto é copiado para este repo. A evidência primária é a análise adversarial da execução da issue #195, no vault de runtime:

- `vault:sisyphus-runtime/docs/analysis/2026-09-01-adversarial-review-issue-195-execution.md:25` (falha P1 "Telemetria inutilizável para governança"): `telemetry.db` com a sessão `agent=NULL`, `repo=NULL`, **0 `task_calls`** (33 `tool_calls` sem correlação); última entrada da tabela é o subagente oracle, sem correlação pai-filho. Causa raiz registrada: finalização/coleta prematura + ausência de correlação pai-filho. Alegação re-verificada pelo orquestrador em 2026-09-01: confirmada (mesma fonte, linha 15).
- Contexto da sessão incidente: fluxo `/issue-start` → implementação → `/issue-review` (oracle second-agent) → `/issue-finish`, PR #196 merged (squash `152efe8`), oracle executado por gpt-5.6-sol (mesma fonte, linhas 15 e 21).

A recorrência de 2026-09-02 está registrada na seção [Recorrência](#recorrencia-2026-09-02-mesmo-caso) abaixo.

## Versões (passo 2)

| Componente | Versão/estado no incidente |
|---|---|
| Repo `long-running-agents` (incidente 1) | main em `152efe8` (squash do PR #196) |
| Stack de telemetria (`~/scripts/telemetry/`, fora do repo) | `tracer.ts`, `trace-cli.ts`, `task-wrapper.sh`, `collector.ts` (SQLite), `collect-session.sh`, `session-end-hook.sh` (`docs/system-of-record.md:129`); versionamento numérico não localizado |
| Skill `qi-epic` | sem versão numérica; defeitos conhecidos Q1 (sandbox-first), Q2 (body-file) e G1 (push_mode) documentados na meta-review do vault, conforme handoff `vault:sisyphus-runtime/sessions/runtime/2026-09-02-121647-sisyphus-handoff.md:284` |
| Vault `sisyphus-runtime` (recorrência) | commitado até `60650a7` (mesmo handoff, linha 225) |

## Comportamento esperado vs observado (passo 4)

**Esperado:** ao fim de uma sessão qi-loop, `telemetry.db` permite reconstruir quem executou (agente), em qual repo, quantos `task_calls` ocorreram e a linhagem orquestrador→subagentes. É o contrato da stack de telemetria (`docs/system-of-record.md:129`) e é exatamente o objeto do reparo estrutural S2 da análise-fonte ("finalização de sessão e correlação pai-filho de task_calls", linha 73).

**Observado (2026-09-01):** sessão com `agent=NULL`, `repo=NULL`, 0 `task_calls`; 33 `tool_calls` sem correlação entre si; última entrada é o subagente oracle sem vínculo com a sessão pai. Qualquer narrativa de custo baseada nessa telemetria é falsa precisão (análise-fonte, linha 25).

**Observado (2026-09-02, recorrência):** collector crasha com `NOT NULL constraint failed: sessions.started_at` ao fazer merge de transcript de export SQL; bypass `--no-collect` aplicado; safety net `telemetry-collect.timer` (handoff, linha 286).

## Classe de falha (taxonomia do flywheel)

**Classe: Tool misuse** (`docs/canonical/production-failure-regression-flywheel.md:47`: "Wrong tool, wrong arguments, wrong order, missing tool call").

Justificativa do encaixe: a causa raiz do incidente 1 é coleta prematura (tool de coleta invocada fora de ordem, antes do fim da sessão) com `task_calls` nunca registrados (missing tool-call records); a recorrência é o `session-end-hook` entregando ao collector um transcript de export SQL que ele não parseia (wrong arguments, 2 formatos tentados), crashando no merge.

### Nota de divergência teoria-vs-prática (registro exigido pelo handoff da issue #211)

A taxonomia do flywheel (`:42-53`) não possui classe de observabilidade. Telemetria quebrada é um gap de medição: o comportamento do agente pode ter sido correto, mas o sistema perdeu a capacidade de verificá-lo, e por isso nenhuma das 8 classes descreve a falha de frente. `Tool misuse` foi escolhida como a mais próxima porque descreve a cadeia causal nos dois eventos (wrong order, missing records, wrong arguments). Alternativas consideradas e rejeitadas:

- "Latency or cost regression" (`:51`, "Correct behavior became too slow or expensive"): sugestão original do corpo da issue #211, refutada pela revisão de território F-A2 (`docs/analysis/2026-09-01-adversarial-review-cl-epic-3-territory.md:47-51`): nada ficou lento ou caro, ficou invisível.
- "State persistence" (`:49`, "Cart, order, memory, or workflow state corrupted"): descreve o sintoma do incidente 1 (linhas com NULL), não a causa, e não cobre a recorrência (crash de merge, não corrupção de estado de workflow).

Esta é a primeira divergência conhecida entre o flywheel teórico e a prática de registrar casos. Fica registrada aqui, no caso, sem editar o canonical. Se uma classe de observabilidade for adicionada à taxonomia no futuro, este caso deve ser reclassificado.

## Privacidade e retenção (passo 3)

Nenhuma fixture bruta de produção foi copiada: o caso referencia artefatos do vault privado (análise, handoff) e cita apenas os campos de telemetria necessários ao diagnóstico. `telemetry.db` não é reproduzido (contém paths de sessão). Regras gerais de promoção/retenção: [[docs/evidence/README|README de docs/evidence]].

## Dedupe e cobertura (passo 5)

`docs/evidence/` continha apenas `.gitkeep` até este caso (verificado em 2026-09-02; confirmado pela revisão de território `:26` e `:85`). Não há caso anterior contra o qual deduplicar; este é o caso nº 1 da pasta. A falha de 2026-09-02 é da mesma classe e do mesmo mecanismo (pipeline de coleta da mesma stack) e por isso foi anexada a este caso como recorrência, não aberta como caso novo, conforme o passo 5 do flywheel e a recomendação explícita da re-verificação de território (`:93`).

## Recorrência 2026-09-02 (mesmo caso)

- **Evento:** collector da sessão de 2026-09-02 do vault runtime crasha com `NOT NULL constraint failed: sessions.started_at` ao fazer merge de um transcript proveniente de export SQL (defeito do `session-end-hook`; 2 formatos tentados).
- **Bypass aplicado:** `--no-collect` (documentado no handoff).
- **Safety net:** `telemetry-collect.timer`.
- **Registro:** `vault:sisyphus-runtime/sessions/runtime/2026-09-02-121647-sisyphus-handoff.md:286`; nota de contexto na revisão de território (`:93`).
- **Leitura de cobertura:** duas ocorrências da mesma classe em dois dias consecutivos confirmam que o defeito é da camada de coleta, não de uma sessão específica, e elevam a urgência do reparo S2.

## Baseline e candidate (passo 7)

- **Baseline:** FAIL documentado. Incidente 1 (2026-09-01) e recorrência (2026-09-02) provam que o caso falha no estado atual da stack: a telemetria não sustenta governança.
- **Candidate:** pendente. O reparo é o item S2 da análise-fonte ("Reparar telemetria: finalização de sessão e correlação pai-filho de task_calls", prioridade 2, linha 73), não executado até esta data. Quando S2 aterrissar, o backfill deve reexecutar uma sessão com subagente e registrar aqui `agent`, `repo`, `task_calls > 0` e a aresta pai-filho presentes em `telemetry.db`.

## Tier (passo 6)

Pendente de atribuição. `docs/evidence/` ainda não tem suite nem tiers; o caso exige sessão real com coleta de telemetria (não é um fast check determinístico). A atribuição será feita contra [[docs/canonical/eval-tier-stratification|Eval Tier Stratification]] quando houver suite.

## Links (passo 8)

- Incidente de origem: [issue #195](https://github.com/pavani06/long-running-agents/issues/195) (repo pavani06/long-running-agents); merge no PR #196 (squash `152efe8`).
- Análise-fonte: `vault:sisyphus-runtime/docs/analysis/2026-09-01-adversarial-review-issue-195-execution.md`.
- Task que criou este caso: [issue #211](https://github.com/pavani06/long-running-agents/issues/211) (epic #208, CL3-3).
- Recorrência: `vault:sisyphus-runtime/sessions/runtime/2026-09-02-121647-sisyphus-handoff.md`.

## Estado dos 9 passos do flywheel

| Passo (`:30-40`) | Estado neste caso |
|---|---|
| 1. Intake | Feito: incidente da issue #195 detectado em review adversarial |
| 2. Captura (interação, trace, versões) | Feito por referência (seção Captura e seção Versões) |
| 3. Privacidade/retenção | Feito (seção Privacidade) |
| 4. Label esperado/observado + classe | Feito (Tool misuse + nota de divergência) |
| 5. Dedupe/cobertura | Feito (pasta vazia; recorrência anexada a este caso) |
| 6. Tier | Pendente (sem suite em `docs/evidence/`) |
| 7. Backfill baseline/candidate | Pendente (reparo S2 não executado) |
| 8. Link ao incidente/analysis | Feito (seção Links) |
| 9. Prune/merge de duplicados | N/A (primeiro caso) |

---

*Criado: 2026-09-02 a partir da análise-fonte de 2026-09-01 | Issue #211 (epic #208) | Precedência: evidence (nível 3)*
