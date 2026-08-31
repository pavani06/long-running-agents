---
title: "Skill Hardening: Correções da Análise Adversarial (ingest-and-improve + pipeline + indexer)"
type: plan
date: 2026-08-31
aliases: ["skill hardening plan", "plano correções skills", "adversarial fixes plan"]
tags: ["governanca", "harness-engineering"]
relates-to: ["[[docs/canonical/manual-brake-question-gate|Manual Brake Question Gate]]", "[[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]]", "[[docs/canonical/intent-five-part-primitive|Intent Five-Part Primitive]]", "[[docs/canonical/constraint-budget-gate|Constraint Budget Gate]]"]
---

# Skill Hardening — Plano de Execução

**Objetivo:** Implementar as 8 correções derivadas da análise adversarial da sessão de 2026-08-30, endurecendo os 4 skill files que permitiram as falhas (premissa falsa em delegação, ambiente errado, commit fora de escopo, PASS estrutural, gate morto, estado residual, conflito wrapper/spec, gap-repair improvisado).

**Fase:** Implementação (diagnóstico já fechado na análise adversarial da sessão)

**Dependências:** Nenhuma externa. Edições de texto em 4 SKILL.md + 1 template JSON.

**Duração estimada:** 1-1.5h (uma sessão)

**Canonical grounding:** yellow tier — 2 canons injetados (intent-five-part-primitive, constraint-budget-gate). Sessão longa, budget reduzido. `manual-brake-question-gate` aplicado na seção Vale a pena; `measured-harness-evolution-lifecycle` aplicado no Eixo 2.

**Intent (cinco partes, resumo):**
- **Description:** As 4 skills que orquestram o fluxo knowledge→curriculum permitiram 7 falhas confirmadas na sessão de 2026-08-30; este plano corrige os textos das skills para que a próxima execução não as repita.
- **Constraints:** ver seção abaixo (6, dentro do budget 5-7)
- **Failure scenarios:** SKILL.md com frontmatter YAML quebrado; regra nova referenciando seção que não existe; gate novo que depende de mecanismo inexistente (repetir o erro do AI_LIGHT_CATEGORY); plano commitado sem validator passar.
- **Success scenarios:** todas as 8 correções aplicadas nos paths canônicos; cada regra nova validada por grep; `validate-obsidian.ts` verde; commits pushados nos 2 repos após aprovação.
- **Connections:** `validate-obsidian.ts` (Rule 16), template `test-results.json` (contrato do harness), cross-references ingest-and-improve ↔ analyze-and-improve, lint do knowledge-indexer.

## Constraints (budget gate: 6/7)

1. Correções SOMENTE nos 4 SKILL.md alvo + template `test-results.json`; nenhum refactor de código de harness.
2. Cada regra nova com no máximo ~15 linhas por seção — texto de skill, não ensaio.
3. Toda tarefa verificável por comando concreto (grep/py_compile/validator), com saída esperada.
4. Trabalho exclusivamente nos paths canônicos `/mnt/c/Users/pavan/{Raw-Knowledge,long-running-agents}` — nunca nos clones `/home` (achado 2).
5. Commits separados por repo; push apenas após aprovação explícita do operador (Commit Gate).
6. Texto novo das skills em inglês (idioma dominante do corpus — dogfooding do achado 1).

## Vale a pena? (manual-brake-question-gate)

Sim. Custo ~1h de edição de texto; as 8 falhas custaram horas de sessão, sincronização manual e deixaram inconsistência commitada em `main`. As regras compostam: cada execução futura das skills passa pelos gates novos. Abortar faria a análise adversarial virar apenas registro histórico.

---

## Fase 1 — Raw-Knowledge (`/mnt/c/Users/pavan/Raw-Knowledge/.opencode/skills/`)

### Tarefa 1: Environment resolution no ingest-and-improve (achado 2)

**Artefatos:**
- Entrada: `ingest-and-improve/SKILL.md`
- Saída: mesmo arquivo com Step -1 + gate novo

- [ ] **Passo 1:** Na tabela Invocation, trocar o default de `target-repo` de `/mnt/c/Users/pavan/long-running-agents` para `resolve via Obsidian vault registry; a registered vault path wins over defaults and fresh clones`.
  Esperado: linha da tabela atualizada.
- [ ] **Passo 2:** Inserir seção `## Step -1 — Environment resolution` antes de `## Step 0`: ler `~/.config/obsidian/obsidian.json` (ou equivalente), resolver paths canônicos de vault e target-repo; se a cópia de trabalho difere do canônico, STOP e perguntar ao operador.
  Esperado: seção presente entre a Invocation e o Step 0.
- [ ] **Passo 3:** Adicionar ao checklist Gates: `[ ] Ambiente canônico resolvido contra o registro do Obsidian (não assumido)`.
- [ ] **Verificação:** `grep -c "Step -1" SKILL.md` = 1; `grep -c "vault registry" SKILL.md` >= 2; frontmatter YAML intacto (`python3 -c "import yaml; yaml.safe_load(open('ingest-and-improve/SKILL.md').read().split('---')[1])"` sem erro).

### Tarefa 2: Regra incremental alinhada ao Passo 0-pre (achado 7)

**Artefatos:**
- Entrada: `ingest-and-improve/SKILL.md`
- Saída: parâmetro `incremental` reescrito

- [ ] **Passo 1:** Na tabela Invocation, reescrever a linha `incremental`: `Auto = run the FULL Passo 0-pre eligibility check from analyze-and-improve SKILL.md (recency AND thematic relevance AND delta count). The 30-day heuristic alone is insufficient: deltas > 10 force full rebuild regardless of recency.`
- [ ] **Passo 2:** No corpo do Step 2 (bloco do STEER.md), ajustar a frase de decisão auto para referenciar o Passo 0-pre completo (coerência com a tabela).
- [ ] **Verificação:** `grep -c "Passo 0-pre" SKILL.md` >= 2 (tabela + Step 2); nenhuma ocorrência restante de "Auto = incremental SOMENTE se" (a regra antiga).

### Tarefa 3: Remover o gate morto AI_LIGHT_CATEGORY (achado 5)

**Artefatos:**
- Entrada: `ingest-and-improve/SKILL.md`
- Saída: Step 2 reescrito sem o export; anti-pattern novo

- [ ] **Passo 1:** Substituir o conteúdo do `## Step 2` sobre o export por: usar as categorias da tabela Phase → Agent Mapping do harness; env-var tiering não existe no caminho nativo (mecanismo removido; categorias corretas já estão na tabela).
- [ ] **Passo 2:** Remover o item `[ ] AI_LIGHT_CATEGORY=quick exportado antes do harness` do checklist Gates; renumerar/ajustar a lista.
- [ ] **Passo 3:** Adicionar ao Anti-Patterns: `**Relying on mechanisms you did not verify exist.** Before gating execution on an env var, script, or flag, grep the pipeline code for it. A gate satisfied by dead configuration is a false pass.`
- [ ] **Verificação:** `grep -c "AI_LIGHT_CATEGORY" SKILL.md` = 0; `grep -c "dead configuration" SKILL.md` = 1.

### Tarefa 4: Step 5 — Cleanup (achado 6)

**Artefatos:**
- Entrada: `ingest-and-improve/SKILL.md`
- Saída: nova seção Step 5 + gate item

- [ ] **Passo 1:** Adicionar `## Step 5 — Cleanup and state reconciliation` após o Step 4: (a) canonical vs working-copy reconciliados (push + fast-forward, ou divergência declarada no report); (b) listar symlinks/env exports/dependências temporárias criadas; (c) deletar clones de trabalho criados pela sessão, salvo pedido do operador.
- [ ] **Passo 2:** Adicionar ao Gates: `[ ] Estado residual reconciliado e declarado (Step 5)`.
- [ ] **Verificação:** `grep -c "Step 5" SKILL.md` >= 1; Gates com o item novo.

### Tarefa 5: Vault hygiene gate no knowledge-indexer (achado 3)

**Artefatos:**
- Entrada: `knowledge-indexer/SKILL.md`
- Saída: Step 0 novo na Operation: Ingest

- [ ] **Passo 1:** Inserir `### Step 0 — Vault hygiene check (BEFORE Step 1)` antes de "Step 1 — Find unprocessed sources": rodar `git status --short`; se houver mudanças não-commitadas pré-existentes NÃO criadas por você: STOP e perguntar ao operador. Nunca `git add -A` sobre estado alheio, nunca stash para prosseguir, nunca empurrar trabalho pré-existente como efeito colateral — ele pertence a outra sessão com outro escopo de aprovação.
- [ ] **Verificação:** `grep -c "Vault hygiene" SKILL.md` = 1; frontmatter YAML intacto.

### Tarefa 6: Operation: Gap-Repair no knowledge-indexer (achado 8)

**Artefatos:**
- Entrada: `knowledge-indexer/SKILL.md`
- Saída: nova operação documentada

- [ ] **Passo 1:** Adicionar `## Operation: Gap-Repair` após a Operation: Ingest: (1) encontrar referências sem página com o one-liner de lint do próprio arquivo (seção Lint); (2) para cada alvo, criar a página grounded na source que a referencia (schema completo, proveniência); (3) atualizar `index.md` + `log.md` com entrada `gap-repair`; (4) re-rodar o lint até zero; (5) checar órfãos (>= 2 inbound links por página nova).
- [ ] **Verificação:** `grep -c "Operation: Gap-Repair" SKILL.md` = 1.

### Tarefa 7: Commit + push Raw-Knowledge

- [ ] **Passo 1:** `git -C /mnt/c/Users/pavan/Raw-Knowledge diff --stat` — escopo = só os 2 SKILL.md.
- [ ] **Passo 2:** Perguntar ao operador; se aprovado: commit único `docs(skills): harden ingest-and-improve + knowledge-indexer (adversarial session findings)` e push.
  Esperado: working tree limpo após push.

---

## Fase 2 — long-running-agents (`/mnt/c/Users/pavan/long-running-agents/.opencode/skills/`)

### Tarefa 8: No fabricated premises no analyze-and-improve (achado 1)

**Artefatos:**
- Entrada: `analyze-and-improve/SKILL.md`
- Saída: regra transversal de delegação + anti-pattern

- [ ] **Passo 1:** Na seção `## Target Repository Context`, acrescentar subseção `### No fabricated premises in delegations`: todo prompt de delegação instrui o sub-agente a DETECTAR convenções dominantes (idioma, estilo, formato) lendo 2-3 artefatos irmãos do diretório alvo — nunca afirmá-las. Conflito entre instrução do operador e convenção detectada → sub-agente para e reporta antes de escrever.
- [ ] **Passo 2:** Adicionar ao `## Anti-Patterns`: `**Asserting unverifiable premises in delegation prompts.** The sub-agent either inherits your error silently or stalls trying to resolve it. Ten seconds of grep before writing the prompt prevents both.`
- [ ] **Verificação:** `grep -c "fabricated premises" SKILL.md` >= 2 (seção + anti-pattern); frontmatter intacto.

### Tarefa 9: Avaliação semântica no harness Step 6 (achado 4)

**Artefatos:**
- Entrada: `harness-analyze-and-improve/SKILL.md` + `.opencode/skills/analyze-and-improve/harness/templates/test-results.json`
- Saída: Step 6 expandido + campo opcional no template

- [ ] **Passo 1:** Substituir a seção `### Step 6: Evaluate` por versão com 3 verificações semânticas proporcionais: (a) **Citation sampling** — 3 citações file:line por artefato conferidas contra os arquivos reais; qualquer erro = NEEDS_WORK; (b) **Executable content** — blocos de código de exercises/skills extraídos e compilados (`python3` + `compile()` por bloco markdown) antes do PASS; (c) **Source fidelity** (Phase 1) — 3 claims de `analysis.md` conferidas por grep contra a source (regras untrusted-source preservadas; leitura permanece delimitada).
- [ ] **Passo 2:** No mesmo Step 6, instruir registro de `verification_depth: structural|semantic` por fase no `test-results.json`; tratar ausência do campo como `structural` (retrocompatível).
- [ ] **Passo 3:** Adicionar `verification_depth: structural` ao template `test-results.json` para cada fase (o bootstrap novo já nasce com o campo).
- [ ] **Verificação:** `python3 -c "import json; d=json.load(open('.opencode/skills/analyze-and-improve/harness/templates/test-results.json')); print(all('verification_depth' in (d['phases'] if 'phases' in d else d)[f'phase-{i}'] for i in range(7)))"` = True; `grep -c "Citation sampling" SKILL.md` = 1.

### Tarefa 10: Commit + push long-running-agents

- [ ] **Passo 1:** `git -C /mnt/c/Users/pavan/long-running-agents diff --stat` — escopo = 2 SKILL.md + 1 template JSON.
- [ ] **Passo 2:** Este plano (`docs/plans/2026-08-31-...md`) entra no mesmo commit ou em commit separado `docs(plans): ...`.
- [ ] **Passo 3:** `npx tsx scripts/validate-obsidian.ts` — 0 erros envolvendo o plano novo (16 erros pré-existentes de pacotes antigos são tolerados e conhecidos).
- [ ] **Passo 4:** Perguntar ao operador; se aprovado: commit + push.
  Esperado: working tree limpo.

---

## Gate de conclusão (E2E)

Re-execução mental do cenário da sessão de 2026-08-30 contra as skills corrigidas: com T1-T4, a wrapper teria parado no Step -1 (ambiente), não exportado env morto (T3), resolvido incremental sem vai-e-vem (T2) e deixado estado reconciliado (T4); com T5, o vault sujo teria bloqueado o commit alheio (T5); com T8-T9, o PT-BR teria sido detectado (T8) e o PASS estrutural teria caído para NEEDS_WORK até o sampling passar (T9). Se qualquer correção não sobreviver a esse replay, a tarefa correspondente reabre.

## Análise por Eixo

### Eixo 1 — Verificação e dependências
Todas as 10 tarefas têm verificação por comando com saída esperada (grep com contagens, py_compile-like do YAML, json assertion do template, validator do repo). Gate de conclusão = replay do cenário adversarial + validator verde. Zero dependências externas novas; a única "dependência" afetada é o template `test-results.json`, cujo campo novo é opcional e retrocompatível (ausência = structural).

### Eixo 2 — Manutenção futura
Sem dívida nova: as regras são texto localizado, sem abstração. Risco de retrabalho baixo — o mecanismo de tiering morto é REMOVIDO em vez de implementado (decisão consciente: implementá-lo seria feature nova sem demanda de custo medida; se custo de modelo virar dor, o measured-harness-evolution-lifecycle puxa a implementação como STABILIZE dirigido por dor). Os 4 SKILL.md são substrato compartilhado entre repos e sessões — as edições são aditivas e localizadas, sem alterar contratos de invocação existentes (parâmetros e modos preservados).

### Eixo 3 — Impacto arquitetural
Toca componentes compartilhados (as skills SÃO o protocolo entre sessões), mas nenhuma mudança altera fluxo de dados, persistência ou comunicação entre skills — apenas adiciona gates de decisão. Sem ADR necessário (nenhuma decisão de arquitetura; são correções de disciplina operacional). Alinhado com o roadmap: a sessão kavak/qi-loop já estabeleceu o padrão de "findings de revisão → correção documentada em docs/plans" (ver `docs/plans/2026-08-30-qi-loop-kavak-fixes.md`), este plano segue o mesmo ciclo.

## Compliance Gate

- Toda tarefa com verificação concreta: sim (10/10, comandos + saída esperada).
- 3 eixos documentados: sim.
- Placeholders: nenhum.
- Rastreabilidade aos canons: intent-five-part → seção Intent com 5 campos; constraint-budget → 6 constraints direcionais em business language (nenhum nomeia ferramenta/padrão de implementação); manual-brake → seção "Vale a pena?"; measured-harness-evolution → Eixo 2 (remoção do tiering como decisão STABILIZE-por-dor). Desvio: constraint-failure-decision-rule não injetado (tier yellow) — classificação constraint-vs-failure do plano usa o bom senso das definições presentes nos canons carregados.

---

## Carimbo de execução

**Executado em 2026-08-31 via qi-epic (epic #157, issues #158-#167, todos fechados com handoff).**

- Commits: Raw-Knowledge `1c927a4` (skills wrapper+indexer) · long-running-agents `f19cb1d` (skills pipeline + este plano)
- Re-verificação: **8/8 critérios PASS** (um check determinístico por finding)
- Desvios documentados: (1) Fases 1-3 do qi-epic puladas — diagnóstico/prescrição/plano já existiam (análise adversarial in-session); (2) task-wrapper.sh ausente — trace instrumentation pulada; (3) quoting de backticks truncou 5 comentários de handoff — corrigidos com comentários completos de seguimento.
- Ruído fora do stage: `.obsidian/` e edição pré-existente em analysis de 2026-06-26 permanecem não-commitados no vault (estado local do operador, intocado).

