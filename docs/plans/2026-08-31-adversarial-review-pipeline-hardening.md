---
title: "Pipeline Hardening Round 2: Correções da Análise Adversarial da Sessão ingest-and-improve (2026-08-31)"
type: plan
date: 2026-08-31
aliases: ["pipeline hardening round 2", "plano correções sessão code review", "adversarial session 2 fixes"]
tags: ["governanca", "harness-engineering"]
relates-to: ["[[docs/plans/2026-08-31-skill-hardening-adversarial-findings|Skill Hardening Round 1]]", "[[docs/canonical/intent-five-part-primitive|Intent Five-Part Primitive]]", "[[docs/canonical/constraint-budget-gate|Constraint Budget Gate]]"]
---

# Pipeline Hardening Round 2 — Plano de Execução

**Objetivo:** Implementar as 8 correções (D1-D8) aprovadas pelo operador a partir da análise adversarial do Oracle sobre a sessão `ingest-and-improve` de 2026-08-30 (fonte "The Last Human Code Review", commits `69cae32`/`382da27`/`3551444`), cobrindo os findings P0-1, P0-2, P1-1, P1-2, P1-3, P1-4 e P2-1, P2-3, P2-5 do review.

**Fase:** Implementação (diagnóstico fechado no adversarial review; decisões D1-D8 aceitas pelo operador sem ressalvas).

**Dependências:** Nenhuma externa. Edições de texto em 2 SKILL.md + 1 plan doc + 3 artefatos de análise + 1 SKILL.md no vault + log.md.

**Duração estimada:** 45-60 min (uma sessão).

**Canonical grounding:** yellow tier — 2 canons (intent-five-part-primitive, constraint-budget-gate), mesmo tier do Round 1; sessão longa. `manual-brake-question-gate` aplicado na seção Vale a pena; `measured-harness-evolution-lifecycle` aplicado no Eixo 2.

**Intent (cinco partes, resumo):**
- **Description:** A sessão de 2026-08-31 diagnosticou 5 defeitos de spec no pipeline e não patcheou nenhum, além de commitar 3 artefatos com dados falsos ou inconsistentes (número de exercícios, total de deltas, causalidade do timestamp). Este plano corrige as skills para o próximo run e emenda os artefatos já commitados.
- **Constraints:** seção abaixo (7, no limite do budget).
- **Failure scenarios:** regex de substituição não casa (linha mudou de lugar); errata reescreve em vez de anexar; `meta.base_commit` apontando para commit errado quebra o PRÓXIMO scan; validator ganha erro novo; correção do MASTER_PLAN usar número estimado em vez de recontado.
- **Success scenarios:** scan do Passo 0a passa a usar git; as 3 ocorrências da regra de exercises ficam consistentes; `mode=loop` sem auto-commit no texto; delta-report com errata; yaml com causalidade correta e `base_commit`; MASTER_PLAN com número recontado; remote sem redirect; deferência do indexer registrada; validator estável em 16; ambos os repos pushados e sincronizados.
- **Connections:** `validate-obsidian.ts` (Rule 16), contrato `test-results.json`/PROGRESS (intocados), cross-referência com o plano Round 1 (cuja constraint 4 este plano SUPERSEDE parcialmente — ver T1 nota).

## Constraints (budget gate: 7/7)

1. Execução em `/home/pavanpavan/long-running-agents` (I/O nativo, protocolo D7); `/mnt/c/Users/pavan/long-running-agents` recebe apenas fast-forward nos pontos de commit. Raw-knowledge direto em `/mnt/c/Users/pavan/raw-knowledge` (única cópia). **Isto supersedes a constraint 4 do Round 1** ("nunca nos clones /home"), que pressupunha execução bash externa; o protocolo dual agora é decisão registrada do operador (D7).
2. Patches somente de texto; no máximo ~15 linhas por seção nova; zero refactors, zero abstrações novas, zero mudanças de contrato de invocação.
3. Toda tarefa verificável por comando concreto com saída esperada.
4. Pacote de análise `docs/analysis/2026-08-31-.../`: tocar SOMENTE o delta-report (errata anexada, histórico preservado) e os 2 yams do mental model (header + meta). Seção `## Transcript` da source no vault: intocável.
5. `validate-obsidian.ts`: baseline de 16 violações pré-existentes tolerado; ZERO violações novas permitidas.
6. Commits somente nos pontos definidos no plano (T9, T12), com aprovação explícita do operador por repo; push e ff-sync logo após cada aprovação.
7. Texto novo de skill em inglês (idioma dominante do corpus), no estilo das seções vizinhas.

## Vale a pena? (manual-brake-question-gate)

Sim. O custo é ~1h de edição de texto; a doença deixada no ambiente já mordeu 2 runs (o scan cego por mtime escondeu 25 deltas no run analisado e voltaria a esconder no próximo), e o `mode=loop` contraditório é mina armada para todo orquestrador futuro. As correções compostam: D1 mata 2 bugs num touch só, e os gates novos (reconciliação, recompute, errata) pegam a classe de erro, não o incidente.

---

## Fase 1 — Skills do pipeline (long-running-agents, em `/home`)

### Tarefa 1: Passo 0a baseado em git — mata o scan por mtime (P0-1/D1) e o tie-break alfabético (B/D1)

**Artefatos:**
- Entrada: `.opencode/skills/analyze-and-improve/SKILL.md` (Passo 0a, linhas ~301-321; Passo 0b schema ~:372; Passo 0c ~:383-413)
- Saída: mesmo arquivo com Passo 0a reescrito + `meta.base_commit` no schema e no Passo 0c

- [ ] **Passo 1:** Substituir o item 2 do Passo 0a (seleção da base) por seleção por commit time do arquivo, nunca por `sort` alfabético:
  ```bash
  for f in mapa-mental-repo/*-mental-model.yaml; do
    printf '%s %s\n' "$(git log -1 --format=%ci -- "$f")" "$f"
  done | sort -r | head -1
  ```
  Esperado: em empate de data no nome, o commit mais recente desempata (gtm `21:14:47` vence kavak `17:57`).
- [ ] **Passo 2:** Substituir o item 3 (scan por `find -newer`) por scan git com fallback:
  ```bash
  # BASE_COMMIT: meta.base_commit do yaml; fallback = commit que introduziu o arquivo
  BASE_COMMIT=$(git log --diff-filter=A --format=%h -- mapa-mental-repo/<base>.yaml | tail -1)
  git log --diff-filter=A --name-only --format='' "$BASE_COMMIT..HEAD" -- \
    docs/canonical docs/decisions curriculum .opencode/skills .opencode/agents docs/plans | sort -u
  ```
  Incluir no texto a justificativa de 1 linha: mtime não sobrevive a clone/checkout e o yaml base é sempre o último arquivo copiado pelo Passo 0c do run anterior, então `find -newer` é estruturalmente cego ao run imediatamente anterior.
- [ ] **Passo 3:** Inserir gate de reconciliação como novo item (entre scan e classificação):
  ```bash
  git diff --name-only "$BASE_COMMIT..HEAD" -- docs/canonical docs/decisions curriculum .opencode docs/plans | wc -l
  ```
  Regra: se o total de `git diff` for > 2x o total de deltas classificados, PARAR e re-escanear manualmente antes de decidir o modo. (Teria pegado o 3-vs-28 do run analisado.)
- [ ] **Passo 4:** No schema YAML do Passo 0b (~:372-379), acrescentar `base_commit` ao `meta:`; no Passo 0c, acrescentar passo: antes de copiar para `mapa-mental-repo/`, verificar que o yaml tem `meta.base_commit: <git rev-parse --short HEAD>` e, se ausente, injetar via round-trip python (`yaml.safe_load` → set → `safe_dump`), para o PRÓXIMO run escanear corretamente.
- [ ] **Verificação:** `grep -c "diff-filter=A" SKILL.md` = 2 (scan + fallback); `grep -c "find docs/canonical/ -name '\*.md' -newer" SKILL.md` = 0; `grep -c "base_commit" SKILL.md` >= 3; `python3 -c "import yaml; yaml.safe_load(open('.opencode/skills/analyze-and-improve/SKILL.md').read().split('---')[1])"` sem erro.

### Tarefa 2: Regra de exercises consistente nos 3 pontos (P1-4/D5)

**Artefatos:**
- Entrada: `.opencode/skills/analyze-and-improve/SKILL.md` (~:769 e ~:809; a `:693` fica canônica)
- Saída: os 3 pontos dizendo a mesma coisa

- [ ] **Passo 1:** No prompt do agente 3 (~:769), trocar `classified as Missing.` por `classified as Missing, and Partial Coverage patterns with Integration Value High (see "Ordem de criacao" item 3). Do not create exercises for P2 unless the orchestrator explicitly lists them in this prompt.`
- [ ] **Passo 2:** No Gate (~:809), trocar `- [ ] P1 patterns (Partial Coverage High) tem canonical doc` por `- [ ] P1 patterns (Partial Coverage High) tem canonical doc + exercise`.
- [ ] **Verificação:** `grep -c "Missing e P1" SKILL.md` >= 1 (regra canônica intacta); `grep -c "Integration Value High (see" SKILL.md` = 1; `grep -c "canonical doc + exercise" SKILL.md` = 1.

### Tarefa 3: `mode=loop` sem auto-commit no texto (P0-2/D5)

**Artefatos:**
- Entrada: `.opencode/skills/harness-analyze-and-improve/SKILL.md` (:58-60)
- Saída: linha 60 apontando para o Commit Gate

- [ ] **Passo 1:** Substituir `Commits cada fase automaticamente. Pergunta push so no final.` por `Commits: pergunte ao operador antes de CADA commit, sem excecao (secao Commit Gate abaixo). Push apenas no final, com aprovacao.`
- [ ] **Verificação:** `grep -c "Commits cada fase automaticamente" SKILL.md` = 0; `grep -c "sem excecao" SKILL.md` = 1; `grep -c "NEVER commit without asking" SKILL.md` = 1 (intacta).

### Tarefa 4: Gate "recompute, never increment" na Phase 5 (D3/D8)

**Artefatos:**
- Entrada: `.opencode/skills/analyze-and-improve/SKILL.md` (Gate da Phase 5, ~:976-979)
- Saída: gate item novo

- [ ] **Passo 1:** Acrescentar ao Gate: `- [ ] Contagens RECOMPUTADAS por comando (ls <dir>/exercises/*.md | wc -l), nunca incrementadas do valor anterior`
- [ ] **Verificação:** `grep -c "nunca incrementadas" SKILL.md` = 1.

### Tarefa 5: Gate de errata do delta-report (D2/P1-2)

**Artefatos:**
- Entrada: `.opencode/skills/analyze-and-improve/SKILL.md` (seção Commit Gate, ~:983-1001)
- Saída: gate item novo

- [ ] **Passo 1:** Acrescentar ao Commit Gate: `- [ ] Se o Passo 0b detectou drift alem do reportado no delta-report.md, o report foi emendado (secao Errata) antes do commit`
- [ ] **Verificação:** `grep -c "Errata" SKILL.md` = 1.

### Tarefa 6: Este plan doc + cross-ref no Round 1

**Artefatos:**
- Entrada: este arquivo; `docs/plans/2026-08-31-skill-hardening-adversarial-findings.md` (:180)
- Saída: plano commitado; uma linha de cross-reference no Carimbo do Round 1

- [ ] **Passo 1:** Anexar ao Carimbo de execução do Round 1: `Round 2 (mesma data): findings da sessão ingest-and-improve de 2026-08-31 geraram o plano docs/plans/2026-08-31-adversarial-review-pipeline-hardening.md; a constraint 4 deste plano (nunca /home) foi supersedida pelo protocolo dual-path aprovado (D7).`
- [ ] **Verificação:** `grep -c "Round 2" docs/plans/2026-08-31-skill-hardening-adversarial-findings.md` = 1; `npx tsx scripts/validate-obsidian.ts` — 16 violações (baseline), nenhuma nos arquivos desta fase.

## Fase 2 — Artefatos de análise (long-running-agents, em `/home`)

### Tarefa 7: Errata no delta-report commitado (P1-2/D2)

**Artefatos:**
- Entrada: `docs/analysis/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co/delta-report.md`
- Saída: seção `## Errata (2026-08-31, pós-descoberta de drift)` ANEXADA ao fim (histórico preservado, nada reescrito acima)

- [ ] **Passo 1:** Anexar seção Errata com: (a) total real de deltas = 28 (25 do output Phase 4 do próprio run GTM via `5292e11`: 12 canonical + 2 skills + 2 exercises + 9 enriquecimentos; + 3 deltas verdadeiros); (b) a premissa da linha 55 ("já refletidos na base") era falsa — o run que produziu a base não pode estar refletido nela, pois a Phase 0 daquele run precede a Phase 4 do mesmo run; (c) o modo incremental foi mantido por decisão do operador com o drift já absorbido pelo Passo 0b, e o gate novo (T5) passa a exigir emenda antes do commit.
- [ ] **Verificação:** `grep -c "## Errata" delta-report.md` = 1; `grep -c "Total real de deltas: 28" delta-report.md` = 1; as linhas 1-81 do arquivo idênticas a `git show HEAD:...delta-report.md` (`git diff` do arquivo mostra apenas linhas adicionadas no fim).

### Tarefa 8: Header do mental-model.yaml — causalidade e timestamp corretos + base_commit (P1-3/D1)

**Artefatos:**
- Entrada: os 2 yams (emenda em ambos): `docs/analysis/2026-08-31-.../2026-08-31-...-mental-model.yaml` e `mapa-mental-repo/2026-08-31-...-mental-model.yaml`
- Saída: headers idênticos e corretos; `meta.base_commit: b7e45fe` nos 2

- [ ] **Passo 1:** Corrigir o header comentado (linhas ~3-8): "postdatou" → "antedata em 4 milissegundos" (arquivos do GTM mtime `21:14:47.3338` vs yaml `.3378`); remover o timestamp fantasma `21:13:47` e citar os horários verificáveis (author time `21:13:27`, committer/mtime `21:14:47`, fonte `git log --format=%ai/%ci 5292e11` e `stat`).
- [ ] **Passo 2:** Adicionar `base_commit: 'b7e45fe'` ao bloco `meta:` dos 2 yams (o modelo descreve o repositório exatamente até esse HEAD; o próximo run escaneia `b7e45fe..HEAD`).
- [ ] **Passo 3:** Espelhar a correção no `.md` do mental model SE ele repetir a causalidade invertida (verificar com grep antes).
- [ ] **Verificação:** `grep -c "postdatou" <yaml>` = 0 nos 2; `grep -c "21:13:47" <yaml>` = 0 nos 2; `grep -c "base_commit: 'b7e45fe'" <yaml>` = 1 nos 2; `python3 -c "import yaml; yaml.safe_load(open('<yaml>'))"` sem erro nos 2; `diff <(sed -n '1,12p' docs/analysis/...yaml) <(sed -n '1,12p' mapa-mental-repo/...yaml)` vazio.

### Tarefa 9: MASTER_PLAN.md:258 — recontar, não incrementar (P1-1/D3)

**Artefatos:**
- Entrada: `curriculum/MASTER_PLAN.md` (:258)
- Saída: número recontado pela convenção "por diretório da seção"

- [ ] **Passo 1:** Recount no momento da execução: `ls -1 curriculum/03-nivel-3-advanced-architecture/exercises/*.md | wc -l` (a tabela da seção em :245-252 lista só esse diretório). Valor esperado hoje: **16** (12 numerados + 4 nomeados).
- [ ] **Passo 2:** Escrever o número RECONTADO (não 16 de memória): a linha vira `Completei os <recount> exercícios do Nível 3`, e a linha da tabela equivalente (:247 se existir) recebe o mesmo número.
- [ ] **Verificação:** `grep -oP 'Completei os \K[0-9]+(?= exercícios do Nível 3)' curriculum/MASTER_PLAN.md` == `ls -1 curriculum/03-nivel-3-advanced-architecture/exercises/*.md | wc -l`.

## Fase 3 — Raw-Knowledge (`/mnt/c/Users/pavan/raw-knowledge`)

### Tarefa 10: Remote URL sem redirect (P2-5/D4)

- [ ] **Passo 1:** `git remote set-url origin https://github.com/pavani06/Raw-Knowledge.git`
- [ ] **Verificação:** `git remote get-url origin` = a URL nova; `git ls-remote --heads origin` exit 0.

### Tarefa 11: ingest-and-improve — deferência do indexer (P2-3/D6) e protocolo dual-path (P2-1/D7)

**Artefatos:**
- Entrada: `.opencode/skills/ingest-and-improve/SKILL.md` (Step 4 ~:126-133; Step -1 ~:35-43)
- Saída: regra anti-órfão no Step 4; protocolo dual-path no Step -1

- [ ] **Passo 1:** No Step 4 (Report), acrescentar item: `- Source orphan check: if the source page remains status: unprocessed, either chain the knowledge-indexer now OR append an explicit deference entry to log.md (owner + date + reason). A source must never end the session without one of the two.`
- [ ] **Passo 2:** No Step -1, acrescentar parágrafo (protocolo dual-path, decisão D7 do operador): quando o registry nomear o path canônico em `/mnt/c` (DrvFs, I/O lento) e existir cópia working em `/home` (ext4, I/O nativo) no mesmo HEAD limpo, executar o pipeline na cópia `/home` e aplicar fast-forward ao path canônico nos pontos de commit — sem re-perguntar ao operador. Se as cópias divergirem em HEAD ou conteúdo, aí sim STOP e perguntar. Registry nunca deve apontar para path WSL-only (o Obsidian do Windows não lê `\\wsl\...` de forma confiável para vaults grandes).
- [ ] **Verificação:** `grep -c "orphan check" SKILL.md` = 1; `grep -c "dual-path" SKILL.md` = 1; frontmatter YAML intacto.

### Tarefa 12: Deferência registrada para a fonte órfã ATUAL (P2-3/D6, aplicado ao estado)

**Artefatos:**
- Entrada: `/mnt/c/Users/pavan/raw-knowledge/log.md`
- Saída: entrada nova `deference`

- [ ] **Passo 1:** Anexar ao log.md: `## 2026-08-31T<HH:MM>Z — deference | knowledge-indexer não executado` com: source `sources/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co.md` permanece `status: unprocessed`; a curadoria na ontologia (concepts/entities) ficou fora do escopo do run do pipeline; dono: operador; re-executar via `@knowledge-indexer` quando conveniente.
- [ ] **Verificação:** `grep -c "deference" log.md` = 1; working tree do raw-knowledge contém só log.md + SKILL.md modificados.

## Fase 4 — Commits, push e sincronização (gates do operador)

### Tarefa 13: Commit + push long-running-agents + ff-sync

- [ ] **Passo 1:** `git diff --stat` — escopo = 2 SKILL.md + 2 plan docs + delta-report + 2 yams + 2 md (se T8 passo 3 aplicar) + MASTER_PLAN. Nada mais.
- [ ] **Passo 2:** `npx tsx scripts/validate-obsidian.ts` — 16 violações (baseline), zero novas.
- [ ] **Passo 3:** Perguntar ao operador. Se aprovado: commit A `docs(skills): harden pipeline skills (adversarial session 2 findings)` (2 SKILL.md + plan docs) e commit B `fix(analysis): errata delta-report, mental-model header, MASTER_PLAN recount` (artefatos); push.
- [ ] **Passo 4:** `git -C /mnt/c/Users/pavan/long-running-agents pull --ff-only origin main`. Esperado: ambas as cópias no mesmo HEAD, dirty=0.

### Tarefa 14: Commit + push raw-knowledge

- [ ] **Passo 1:** Perguntar ao operador (um único turno para T13+T14 sempre que possível). Se aprovado: commit `docs(skills): dual-path protocol + indexer deference rule (adversarial session 2)` (SKILL.md + log.md); push.

## Gate de conclusão (E2E)

Replay do cenário contra as skills corrigidas: (1) simular o Passo 0a novo contra a base `2026-08-31` — `BASE_COMMIT` resolve para `b7e45fe`, o scan `b7e45fe..HEAD` lista exatamente os arquivos dos commits de hardening desta sessão (nem 0, nem 28), e a reconciliação passa; (2) com os 3 pontos da Phase 4 alinhados, um run com 0 Missing e 2 P1 produziria exatamente o que o run analisado produziu, agora por regra e não por julgamento; (3) um orquestrador lendo `mode=loop` não encontra mais autorização de commit automático; (4) o delta-report tem errata e o gate novo teria exigido a emenda antes do commit original; (5) o remote do raw-knowledge responde sem redirect. Se qualquer item falhar, a tarefa correspondente reabre.

## Análise por Eixo

### Eixo 1 — Verificação e dependências
Todas as 14 tarefas têm verificação por comando com saída esperada (grep com contagens, yaml parse, wc -l, ls-remote, validator). Gate de conclusão = replay E2E + validator estável em 16. Zero dependências novas; a única dependência afetada é o campo `meta.base_commit` (aditivo, com fallback para modelos antigos via `--diff-filter=A`).

### Eixo 2 — Manutenção futura
Reduz dívida: os 5 defeitos de spec descobertos no run e deixados em pé (P1-4) são patcheados, e o padrão do Round 1 ("findings → plano → patch") é seguido com o cross-reference mútuo entre os planos. Risco de retrabalho baixo: o fallback do `base_commit` mantém compatibilidade com os 5 modelos antigos sem migração. O protocolo dual-path (D7) codifica o que a sessão já executou, eliminando a re-pergunta do Step -1.

### Eixo 3 — Impacto arquitetural
Toca o substrato compartilhado (as skills são o protocolo entre sessões), mas as mudanças são gates de decisão e seleção de mecanismo, sem alterar fluxo de dados ou contratos de invocação. Sem ADR novo: o dual-path é decisão operacional registrada no próprio skill e no plano (o Operador aprovou via D7); se futuramente o vault migrar para o WSL nativo, o protocolo é revogado em um parágrafo. Alinhado ao ciclo estabelecido: adversarial review → plano → patch → re-verificação.

## Compliance Gate

- Toda tarefa com verificação concreta: sim (14/14).
- 3 eixos documentados: sim.
- Placeholders: nenhum (o único valor "a preencher na execução" é o recount do T9, cujo comando e valor esperado estão explícitos).
- Rastreabilidade: intent-five-part → seção Intent; constraint-budget → 7 constraints em linguagem de negócio; manual-brake → "Vale a pena?"; measured-harness-evolution → Eixo 2 (patches como STABILIZE dirigido por dor medida em 2 runs). Desvio: constraint-failure-decision-rule não injetado (tier yellow), mesma justificativa do Round 1.

---

## Carimbo de execução

**Executado em 2026-08-31 nesta sessão (qi-epic epic #168, issues #169-#180, todas fechadas com handoff).**

- Commits: long-running-agents `da3a141` (commit A: skills + plan docs) · `9e1651c` (commit B: artefatos de análise) · raw-knowledge `310b097` (commit C: ingest SKILL + log.md)
- Re-verificação: **9/9 findings PASS** (um check determinístico por finding, todos os aceites das issues verificados no disco)
- Gate E2E (T1): simulação do novo Passo 0a com `BASE_COMMIT=b7e45fe` → scan=23, diff bruto=23, reconciliação razão 1.0 PASS. O scan enxerga o run anterior inteiro (pipeline + hardening), que é o comportamento correto: o modelo 2026-08-31 descreve o repo na Phase 0, antes do próprio output. O gate esperava errado "só os arquivos de hardening" — correção registrada aqui.
- Desvios documentados: (1) Fases 1-2 do qi-loop puladas (diagnóstico = adversarial review; RECs persistidos em `~/.reflection/qi-loop-iter2-recommendations.md`); (2) `task-wrapper.sh` ausente — trace instrumentation pulada; (3) aceite da issue #169 ajustado: `diff-filter=A`=2 com composição 1 comando (fallback) + 1 comentário ("SEM --diff-filter=A"), porque o E2E pegou o scan com filtro subcontando `atualizacao`; (4) estado do qi-loop em `~/.reflection/qi-loop-iter2-state-long-running-agents.json` (o `state.json` global pertence à sonda #27, intocado).
- Ruído fora do stage: nenhum — `git status` limpo nos 3 repos após push e ff-sync.
