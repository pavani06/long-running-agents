# Plano: Integration Roadmap → Artifacts Manifest

**Data**: 2026-06-14
**Status**: pronto para execução
**Deriva de**: `.omo/plans/2026-06-14-roadmap-manifest-analysis.md` (análise e decisão Design A vs B)

---

## Decisões consolidadas

| # | Decisão | Resolução |
|---|---|---|
| D1 | Design A vs B | **Design B** --- manifesto como par `.md` + `.yaml` |
| D2 | Quem gera o manifesto | **Orquestrador**, ação direta, pós-Phase 4, pré-Phase 5 |
| D3 | Gate da Phase 4 | **4 itens**: manifesto existe, YAML lista artefatos, `skipped.*` documentado, `.md` tem Integration Map |
| D4 | PC Medium na Phase 6 | **Sempre integrar** --- obrigatório, como Missing e PC High |
| D5 | 8 integration-roadmap.md históricos | **Option A** --- banner de depreciação em cada um |
| D6 | Prompt Phase 5 | Reescrever para ler o manifesto como input |
| D7 | GUIDE-analyze-and-improve.md | Atualizar com contexto, teoria, exemplos práticos |
| D8 | Verification gates (SKILL.md) | Alinhar ao novo modelo |
| D9 | Reference implementations (SKILL.md) | Atualizar para refletir o formato de manifesto |
| D10 | Formato do manifesto | **Par** `.md` + `.yaml` |
| D11 | Nome do arquivo | `<date>-<source-slug>-artifacts.{md,yaml}` |

---

## Escopo: o que NÃO muda

Nenhum artefato de análise existente é regenerado ou convertido:

- 8× `integration-roadmap.md` históricos: conteúdo intacto, só ganham banner
- `docs/canonical/` (55 arquivos): intocados
- `.opencode/skills/` (exceto `analyze-and-improve` e `harness-analyze-and-improve`): intocados
- `curriculum/`: intocado
- `docs/analysis/*/classification.yaml` e demais pares `.md`+`.yaml`: intocados
- `mapa-mental-repo/`: intocado
- `PROGRESS.md` (raiz do repo): verificar referências, mas não é foco principal

---

## Tarefas

### T0: Baseline --- diagnóstico do estado atual

**Objetivo**: Confirmar que as inconsistências documentadas no plano de análise ainda existem.

**Ações**:
1. Rodar `grep -n "Integration roadmap\|Agent 4\|integration.roadmap\|Artifacts Created" .opencode/skills/analyze-and-improve/SKILL.md` e registrar linhas exatas
2. Rodar `grep -n "integration.roadmap\|Agent 4" harness/GUIDE-analyze-and-improve.md` e registrar
3. Rodar `grep -rn "integration.roadmap" .opencode/skills/harness-analyze-and-improve/` e registrar
4. Rodar `grep -rn "integration.roadmap\|Agent 4" harness/templates/` e registrar
5. Listar os 8 `integration-roadmap.md` com `find docs/analysis -name "*integration-roadmap*"`
6. Rodar `bash scripts/check-obsidian-conventions.sh` para baseline

**Gate**: Lista completa de linhas que precisam ser alteradas, organizada por arquivo.

**Estimativa**: 5 min

---

### T1: SKILL.md --- Remover Agent 4 e referências a "integration roadmap"

**Objetivo**: Limpar todas as menções ao Agent 4 e ao antigo `integration-roadmap.md` do SKILL.md principal.

**Ações**:

1. **Linha 140** (Output Directory Structure): Remover `│   <date>-<source-slug>-integration-roadmap.md        # Phase 4` da árvore de diretórios. Substituir por referência ao manifesto.

2. **Linhas 742-770** (Agent 4: Integration Roadmap): Remover o bloco inteiro do Agent 4 --- cabeçalho, prompt `task()`, e nota sobre execução síncrona. O comentário OBSOLETO (linhas 745-746) também é removido, já que o Agent 4 deixa de existir completamente.

3. **Linha 624** (Categoria "New Documentation"): Remover `Roadmap de integracao, cross-reference` da tabela de categorias de melhoria da Phase 4.

4. **Linha 643** (Ordem de criação, item 4): Remover `4. Roadmap de integracao — Conecta tudo ao curriculo existente.`

5. **Linhas 770** (nota sobre agentes 1-3 paralelos, 4 síncrono): Simplificar para refletir que agora são só 3 agentes em paralelo.

**Gate**: `grep -n "Agent 4\|integration.roadmap\|Integration roadmap" .opencode/skills/analyze-and-improve/SKILL.md` retorna zero matches, exceto no banner de depreciação do bloco OBSOLETO atualizado (se optarmos por mantê-lo como nota histórica) e nas reference implementations (que serão atualizadas em T8).

**Estimativa**: 15 min

---

### T2: SKILL.md --- Redesenhar Phase 4 Gate

**Objetivo**: Substituir o gate antigo (linha 755) pelos 4 novos itens alinhados ao Design B.

**Local**: Linhas 750-758 (seção `### Gate` da Phase 4).

**Antes**:
```markdown
- [ ] Missing patterns tem canonical doc + skill + exercise
- [ ] P1 patterns (Partial Coverage High) tem canonical doc
- [ ] P2 patterns (Partial Coverage Medium) tem canonical doc (exercise opcional, a criterio do orquestrador)
- [ ] Integration roadmap conecta todos os artefatos criados
- [ ] Nao foram criados artefatos para Already Exists ou Better Implementation
- [ ] **0 Missing e esperado**: ...
- [ ] **Exercicios novos sao criados na Phase 4, NAO na Phase 6.**
```

**Depois**:
```markdown
- [ ] Missing patterns tem canonical doc + skill + exercise
- [ ] P1 patterns (Partial Coverage High) tem canonical doc
- [ ] P2 patterns (Partial Coverage Medium) tem canonical doc (exercise pode ser criado aqui ou postergado para Phase 6)
- [ ] Nao foram criados artefatos para Already Exists ou Better Implementation
- [ ] **0 Missing e esperado**: ...
- [ ] **Exercicios novos sao criados na Phase 4, NAO na Phase 6.**
- [ ] Artifacts manifest (`<date>-<source-slug>-artifacts.yaml` + `.md`) gerado pelo orquestrador em `docs/analysis/<date>-<source-slug>/`
- [ ] Manifest YAML lista todos os artefatos Phase 4 em `artifacts.canonical_docs`, `artifacts.skills`, `artifacts.exercises`
- [ ] Padrões não gerados (Already Exists, Better Implementation) registrados em `skipped.*` com justificativa
- [ ] Manifest Markdown contém "Integration Map" conectando cada artefato às superfícies que Phase 5 deve atualizar
```

**Gate**: Os 4 novos itens são verificáveis: existência de arquivo, campos preenchidos, justificativas presentes, seção Integration Map no `.md`.

**Estimativa**: 10 min

---

### T3: SKILL.md --- Reescrever Phase 5 (integração e prompt delegado)

**Objetivo**: Phase 5 agora LÊ o manifesto (em vez de gerar "Artifacts Created" inline). O prompt delegado instrui o agente a usar o manifesto como input.

**Ações**:

1. **Seção "Artifacts Created Summary" (linhas 775-777)**: Substituir por instrução ao orquestrador para gerar o manifesto ANTES de delegar a Phase 5.

   **Antes**:
   ```markdown
   ### Artifacts Created Summary

   Antes de atualizar os indices, o agente DEVE ler os outputs da Phase 4 (canonical docs, skills, exercises) e gerar uma secao de "Artifacts Created" dentro do proprio system-of-record.md ou como subsecao da atualizacao. Isso substitui a antiga Agent 4 (Integration Roadmap separado).
   ```

   **Depois**:
   ```markdown
   ### Pre-requisito: Artifacts Manifest

   Antes de delegar a Phase 5, o orquestrador DEVE gerar o artifacts manifest (ação direta, não delegada):

   1. Ler `docs/analysis/<date>-<source-slug>/<date>-<source-slug>-classification.yaml`
   2. Listar arquivos criados em `docs/canonical/`, `.opencode/skills/`, `curriculum/` nesta sessão
   3. Gerar `docs/analysis/<date>-<source-slug>/<date>-<source-slug>-artifacts.yaml` com a estrutura tipada (meta, artifacts, skipped, gate)
   4. Gerar `docs/analysis/<date>-<source-slug>/<date>-<source-slug>-artifacts.md` com:
      - Tabela-sumário de artefatos criados
      - Integration Map: tabela conectando cada artefato → índice que Phase 5 deve atualizar
      - Seção de padrões skipped com justificativa

   O manifesto é o contrato que a Phase 5 lê como input. Sem ele, a Phase 5 não sabe o que integrar.
   ```

2. **Prompt delegado (linhas 783-804)**: Reescrever para incluir a leitura do manifesto.

   **Novo prompt**:
   ```typescript
   task(
     category="quick",
     load_skills=["git-master"],
     run_in_background=false,
     prompt="TASK: Update index documents using the artifacts manifest as input.

   TARGET_REPOSITORY:
     path: <absolute-path-to-repo>
     name: <repo-name>
     output_dir: <absolute-path-to-repo>/docs/analysis/<date>-<source-slug>/
     system_of_record: <absolute-path-to-repo>/docs/system-of-record.md
     branch: main

   INPUT: Read the artifacts manifest at:
     - docs/analysis/<date>-<source-slug>/<date>-<source-slug>-artifacts.yaml
     - docs/analysis/<date>-<source-slug>/<date>-<source-slug>-artifacts.md

   The manifest lists ALL artifacts created in Phase 4 and maps each one to the
   index documents that need updating. Use it as your authoritative source.

   CHECK AND UPDATE:
   1. docs/system-of-record.md — add new canonical docs and skills to the
      appropriate domain tables; update last-modified date
   2. curriculum/INDEX.md — add new exercises to the listing
   3. curriculum/README.md — update directory tree if changed
   4. curriculum/MASTER_PLAN.md — update exercise/topic counts if changed

   For each artifact listed in the manifest, follow the Integration Map in the
   .md to know exactly which index document(s) to update.

   MUST NOT:
   - Guess which artifacts were created — use the manifest
   - Skip artifacts listed in the manifest
   - Modify files outside the Integration Map targets

   Then run: git diff --stat to confirm which files were changed.
   Do NOT commit. The orchestrator handles the commit decision."
   )
   ```

**Gate**: O prompt da Phase 5 agora referencia explicitamente o manifesto como input. O agente não precisa adivinhar o que foi criado.

**Estimativa**: 20 min

---

### T4: SKILL.md --- Corrigir PC Medium (consistência Phase 6)

**Objetivo**: Eliminar a ambiguidade "SIM | Phase 6 ou apenas canonical doc, a criterio do orquestrador". PC Medium agora é obrigatório na Phase 6.

**Local**: Linha 839 (tabela "Quando executar" da Phase 6).

**Antes**:
```markdown
| Partial Coverage + Medium | SIM | Phase 6 ou apenas canonical doc, a criterio do orquestrador |
```

**Depois**:
```markdown
| Partial Coverage + Medium | SIM | Integração completa nos módulos existentes — mesma profundidade que PC High |
```

**Também ajustar**:
- Linha 776 (gate Phase 4): `P2 patterns (Partial Coverage Medium) tem canonical doc (exercise pode ser criado aqui ou postergado para Phase 6)` --- já incluso em T2
- Linha 634 (tabela de priorização Phase 4): `Partial Coverage (Medium value) | P2 | Criar canonical doc, postergar exercise` --- mantém, mas o exercise pode ser criado na Phase 4 também se fizer sentido

**Gate**: Consistência total: Missing, PC High, e PC Medium têm o mesmo tratamento na Phase 6 (todos "SIM" obrigatório).

**Estimativa**: 5 min

---

### T5: SKILL.md --- Atualizar Verification Gates (fim do arquivo)

**Objetivo**: Alinhar os gates de verificação global (linhas 981-998) ao novo modelo.

**Mudanças**:

1. **Linha 984**: De `docs/system-of-record.md contem secao "Artifacts Created" listando os outputs da Phase 4 (substitui o antigo integration-roadmap.md)` para:
   ```markdown
   - [ ] `docs/analysis/<date>-<source-slug>/<date>-<source-slug>-artifacts.yaml` existe e lista todos os artefatos Phase 4
   - [ ] `docs/analysis/<date>-<source-slug>/<date>-<source-slug>-artifacts.md` existe e contém Integration Map
   ```

2. **Linha 998**: Remover `integration-roadmap.md existe` (se ainda estiver presente). Já verificado pelo item acima.

**Gate**:
- `grep -n "integration.roadmap\|Artifacts Created" .opencode/skills/analyze-and-improve/SKILL.md | tail -20` --- nas linhas 981-998, não deve haver menção a "integration-roadmap.md" nem "Artifacts Created" no system-of-record
- Novos itens de verificação mencionam `artifacts.yaml` e `artifacts.md`

**Estimativa**: 5 min

---

### T6: SKILL.md --- Atualizar Reference Implementations

**Objetivo**: Atualizar as tabelas de referência (linhas 1002-1053) para refletir que sessões futuras usarão manifesto, e marcar as históricas como legacy.

**Ações**:

1. **Sessão 1 (linha 1021)**: Onde diz `docs/analysis/2026-06-09-12-factor-agents/2026-06-09-12-factor-agents-integration-roadmap.md`, substituir por:
   ```markdown
   | | `docs/analysis/2026-06-09-12-factor-agents/2026-06-09-12-factor-agents-integration-roadmap.md` (formato legacy) |
   ```

2. **Sessão 2 (linha 1045)**: Mesmo tratamento:
   ```markdown
   | | `docs/analysis/2026-06-09-how-we-solved-context-management-in-agents/2026-06-09-how-we-solved-context-management-in-agents-integration-roadmap.md` (formato legacy) |
   ```

3. Adicionar nota no fim da seção:
   ```markdown
   > **Nota sobre formato**: Sessões a partir de 2026-06-14 usam o artifacts manifest
   > (`<date>-<source-slug>-artifacts.{md,yaml}`) em vez de `integration-roadmap.md`.
   > O formato e o contrato entre fases evoluíram; o conteúdo (rastreabilidade
   > classificação → artefatos → integração) é preservado.
   ```

**Gate**: As duas referências históricas agora sinalizam "formato legacy". Nenhuma informação é perdida.

**Estimativa**: 10 min

---

### T7: SKILL.md --- Adicionar template do Manifesto YAML

**Objetivo**: Incluir no SKILL.md o schema de referência do artifacts manifest YAML para que o orquestrador saiba exatamente o que gerar.

**Local**: Nova subseção dentro da Phase 5, após "Pre-requisito: Artifacts Manifest".

**Conteúdo**:
```markdown
### Schema do Artifacts Manifest YAML

```yaml
meta:
  type: artifact-manifest
  date: <YYYY-MM-DD>
  source_slug: <slug>
  classification_file: docs/analysis/<date>-<source-slug>/<date>-<source-slug>-classification.yaml

artifacts:
  canonical_docs:
    - path: docs/canonical/<slug>.md
      pattern: <pattern-name>
      classification: Missing | Partial Coverage
      priority: P0 | P1 | P2
  skills:
    - path: .opencode/skills/<slug>/SKILL.md
      pattern: <pattern-name>
      classification: Missing
  exercises:
    - path: curriculum/<level>/exercises/<filename>.md
      pattern: <pattern-name>
      classification: Missing
  examples: []

skipped:
  already_exists:
    - pattern: <pattern-name>
      evidence: <file:line reference>
  better_implementation:
    - pattern: <pattern-name>
      reason: <why repo version is superior>

gate:
  phase4_complete: true
  artifacts_count:
    canonical_docs: <N>
    skills: <N>
    exercises: <N>
  notes: []
```
```

### Schema do Artifacts Manifest Markdown

```markdown
---
title: "Artifacts Manifest: <source-title>"
type: analysis
date: <YYYY-MM-DD>
aliases: ["manifesto <slug>", "artifacts <slug>"]
tags: ["analise", "roadmap", "<dominio>"]
relates-to:
  - "[[docs/analysis/<date>-<source-slug>/<date>-<source-slug>-classification|Classificação]]"
---

# Artifacts Manifest: <source-title>

## Summary

| # | Pattern | Classification | Priority | Artifacts Created |
|---|---|---|---|---|
| 1 | ... | Missing | P0 | canonical, skill, exercise |
| 2 | ... | Partial Coverage | P1 | canonical |
| ... | ... | ... | ... | ... |

## Integration Map

| Artifact | Path | Updates |
|---|---|---|
| `<name>` canonical doc | `docs/canonical/<slug>.md` | `system-of-record.md` → domínio `<dominio>` |
| `<name>` skill | `.opencode/skills/<slug>/SKILL.md` | `system-of-record.md` → domínio `<dominio>` |
| `<name>` exercise | `curriculum/<level>/exercises/<file>.md` | `INDEX.md`, `README.md`, `MASTER_PLAN.md` |

## Skipped

| Pattern | Reason |
|---|---|
| `<name>` | Already Exists — ver `docs/canonical/<slug>.md` |
| `<name>` | Better Implementation — repo version is superior |
```

**Gate**:
- `grep -c "artifacts:" .opencode/skills/analyze-and-improve/SKILL.md` deve retornar pelo menos 1 (schema YAML com `artifacts.canonical_docs`, `artifacts.skills`, `artifacts.exercises`)
- `grep -c "Integration Map" .opencode/skills/analyze-and-improve/SKILL.md` deve retornar pelo menos 2 (template .md + explicação na Phase 5)
- `grep -c "skipped:" .opencode/skills/analyze-and-improve/SKILL.md` deve retornar pelo menos 1 (seção `skipped.already_exists` e `skipped.better_implementation`)

**Estimativa**: 15 min

**Objetivo**: Sinalizar o formato legacy sem quebrar wikilinks ou conteúdo.

**Ações**:

Para cada um dos 8 arquivos:
1. `docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/...-integration-roadmap.md`
2. `docs/analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/...-integration-roadmap.md`
3. `docs/analysis/2026-06-09-12-factor-agents/...-integration-roadmap.md`
4. `docs/analysis/2026-06-09-how-we-solved-context-management-in-agents/...-integration-roadmap.md`
5. `docs/analysis/2026-06-10-eval-maturity-phases/...-integration-roadmap.md`
6. `docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/...-integration-roadmap.md`
7. `docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/...-integration-roadmap.md`
8. `docs/analysis/2026-06-12-idsd-method/...-integration-roadmap.md`

Inserir APÓS o frontmatter (após o segundo `---`):

```markdown
> [!warning] Formato legado
> Este arquivo usa o formato histórico `integration-roadmap.md`.
> Sessões a partir de 2026-06-14 usam `<date>-<source-slug>-artifacts.{md,yaml}`.
> Preservado para rastreabilidade e estabilidade de wikilinks.
```

**Gate**: Todos os 8 arquivos têm o banner. `git diff --stat` mostra apenas os 8 arquivos alterados (1 linha cada). `bash scripts/check-obsidian-conventions.sh` passa (banners são blockquotes, não quebram frontmatter).

**Estimativa**: 15 min

---

### T9: Atualizar docs/system-of-record.md

**Objetivo**: Adicionar nota sobre o formato legacy nas seções de análises históricas.

**Local**: Seção "Análises e diagnósticos" (linhas 216-286).

**Ação**: Adicionar nota após a lista de análises:
```markdown
> **Nota sobre formato**: Sessões de análise anteriores a 2026-06-14 contêm
> `integration-roadmap.md` (formato legacy). Sessões a partir de 2026-06-14 usam
> `<date>-<source-slug>-artifacts.{md,yaml}` como artifacts manifest.
> Ambos os formatos servem ao mesmo propósito: rastreabilidade classificação →
> artefatos → integração. Consulte o [[.opencode/skills/analyze-and-improve/SKILL|analyze-and-improve SKILL.md]]
> para o contrato atual.
```

Também atualizar `last_updated: 2026-06-14`.

**Gate**: `bash scripts/check-obsidian-conventions.sh` passa.

**Estimativa**: 5 min

---

### T10: Atualizar harness/GUIDE-analyze-and-improve.md

**Objetivo**: Atualizar o guia operacional para refletir o novo contrato entre fases e o artifacts manifest. Qualidade de referência: contexto, teoria, exemplos práticos.

**Ações**:

1. **Linha 18** (tabela de fases): Alterar output da Phase 4 de `integration-roadmap.md` para `artifacts manifest (.md + .yaml)`. Adicionar nota de que a Phase 4 produz artefatos concretos e o orquestrador gera o manifesto.

2. **Linha 528** (tabela de referência rápida): Alterar evidência da Phase 4 de `integration-roadmap.md` para `artifacts.yaml + artifacts.md + artefatos concretos`.

3. **Linhas 562-567** (exemplo de output): Atualizar a listagem para refletir o novo par de arquivos.

4. **Nova subseção**: Adicionar "O Artifacts Manifest" explicando:
   - O que é (contrato entre Phase 4 e Phase 5)
   - Quem gera (orquestrador, ação direta)
   - Formato (YAML estruturado + Markdown com Integration Map)
   - Exemplo concreto baseado na sessão 12-Factor Agents

5. **Linhas 599-603** (Próximos passos): Adicionar item sobre a migração para artifacts manifest como concluída.

**Gate**:
- `grep -c "integration.roadmap" harness/GUIDE-analyze-and-improve.md` --- zero matches (todas as referências foram substituídas por "artifacts manifest" ou "manifesto")
- `grep -c "artifacts manifest\|artifacts.yaml\|Artifacts Manifest" harness/GUIDE-analyze-and-improve.md` --- pelo menos 3 matches (tabela de fases, referência rápida, nova subseção)
- `grep -c "Agent 4" harness/GUIDE-analyze-and-improve.md` --- zero matches
- Nova subseção "O Artifacts Manifest" existe e contém exemplo concreto com nome de arquivo real da sessão 12-Factor Agents

**Estimativa**: 25 min

---

### T11: Atualizar harness-analyze-and-improve/SKILL.md

**Objetivo**: Sincronizar o skill harness com as mudanças do SKILL.md principal.

**Ações**:

1. Verificar se o harness-analyze-and-improve reference "Agent 4" ou "integration-roadmap"
2. Atualizar mapeamento Phase→Agent para refletir 3 agentes na Phase 4 (não 4)
3. Atualizar referências a outputs da Phase 4
4. Adicionar nota sobre o artifacts manifest

**Gate**:
- `grep -c "integration.roadmap\|Agent 4" .opencode/skills/harness-analyze-and-improve/SKILL.md` --- zero matches
- `grep -c "artifacts manifest\|artifacts.yaml" .opencode/skills/harness-analyze-and-improve/SKILL.md` --- pelo menos 1 match (nota sobre o manifesto)
- Mapeamento Phase→Agent mostra 3 agentes na Phase 4 (não 4)

**Estimativa**: 15 min

---

### T12: Atualizar .opencode/skills/analyze-and-improve/harness/templates/test-results.json

**Objetivo**: Corrigir o campo `evidence` da Phase 4 no template canônico de contrato.

**Ações**:

1. Localizar `phase-4` no template
2. Alterar `evidence` para refletir os outputs reais da Phase 4:
   ```json
   "phase-4": {
     "passes": false,
     "evidence": [
       "docs/canonical/<novos>.md",
       ".opencode/skills/<novos>/SKILL.md",
       "curriculum/.../<novos-exercicios>.md",
       "docs/analysis/<date>-<slug>/<date>-<slug>-artifacts.yaml",
       "docs/analysis/<date>-<slug>/<date>-<slug>-artifacts.md"
     ],
     ...
   }
   ```

**Gate**: `python3 -c "import json; json.load(open('.opencode/skills/analyze-and-improve/harness/templates/test-results.json'))"` --- JSON válido, sem erros de parse

**Estimativa**: 5 min

---

### T13: Atualizar .opencode/skills/analyze-and-improve/harness/templates/PROGRESS.md

**Objetivo**: Remover referências ao integration-roadmap no template de progresso.

**Ações**:

1. Buscar por "integration-roadmap" ou "roadmap" no template
2. Atualizar descrição da Phase 4 para mencionar o artifacts manifest

**Gate**:
- `grep -i "integration.roadmap\|Agent 4" .opencode/skills/analyze-and-improve/harness/templates/PROGRESS.md` não deve retornar matches
- Template mantém estrutura de seções (Done, In Progress, Next, Analysis Context, Notes)

**Estimativa**: 5 min

---

### T14: QA Final

**Objetivo**: Validar que todas as mudanças estão consistentes e nenhuma referência quebrada permanece.

**Ações**:

1. `grep -rn "integration.roadmap\|Agent 4" .opencode/skills/analyze-and-improve/SKILL.md` --- deve retornar zero matches exceto nas reference implementations (marcadas "legacy") e possivelmente no bloco OBSOLETO
2. `grep -rn "integration.roadmap\|Agent 4" .opencode/skills/harness-analyze-and-improve/SKILL.md` --- zero matches
3. `grep -rn "integration.roadmap" harness/` --- zero matches (exceto GUIDE que referencia como histórico)
4. `bash scripts/check-obsidian-conventions.sh` --- deve passar
5. `python3 -c "import json; json.load(open('.opencode/skills/analyze-and-improve/harness/templates/test-results.json'))"` --- JSON válido
6. `git diff --stat` --- revisar escopo: apenas os arquivos esperados foram alterados
7. Verificar que os 8 `integration-roadmap.md` têm o banner e nenhum outro conteúdo foi alterado
8. Verificar que `docs/system-of-record.md` tem `last_updated: 2026-06-14`

**Gate**: Todos os checks passam. Nenhum arquivo fora do escopo foi alterado.

**Estimativa**: 15 min

---

## Ordem de execução recomendada

```
T0 (baseline)
  │
  ├─► T1 (remover Agent 4)
  ├─► T2 (redesenhar Phase 4 gate)
  ├─► T4 (corrigir PC Medium)
  │
  ├─► T3 (reescrever Phase 5)    ── depende de T1+T2
  ├─► T7 (template manifesto)     ── independente, pode ser paralelo
  │
  ├─► T5 (verification gates)     ── depende de T1+T2+T3
  ├─► T6 (reference impls)        ── depende de T1
  │
  ├─► T8 (banners históricos)     ── totalmente independente
  ├─► T9 (system-of-record.md)    ── independente
  ├─► T10 (GUIDE)                 ── independente
  ├─► T11 (harness-analyze)       ── independente
  ├─► T12 (test-results.json)     ── independente
  ├─► T13 (PROGRESS.md)           ── independente
  │
  └─► T14 (QA final)              ── depende de todas acima
```

T0-T4 são sequenciais dentro do SKILL.md (mesmo arquivo). T8-T13 são independentes entre si e podem ser paralelizados. T3 depende de T1+T2. T5 e T6 dependem das anteriores no SKILL.md.

---

## Riscos e mitigação

| Risco | Probabilidade | Mitigação |
|---|---|---|
| `edit` falhar por whitespace em trechos longos | Média | Preferir `write` para seções inteiras do SKILL.md quando o `edit` falhar repetidamente. O arquivo tem 1053 linhas; reescrita controlada de seções é aceitável. |
| Wikilinks quebrados nos banners de depreciação | Baixa | Banners são blockquotes após frontmatter; não afetam wikilinks. Validar com `check-obsidian-conventions.sh`. |
| `grep` falso-positivo em referências legítimas (ex: "integration" em outro contexto) | Baixa | Revisar cada match manualmente. O padrão `integration.roadmap` é específico o suficiente. |
| Conflito com worktree de outra sessão | Baixa | Verificar `git status` antes de começar. Esta sessão foca apenas nos arquivos de configuração/skill. |

---

## Artefatos gerados por este plano

| Arquivo | Tipo | Mudança |
|---|---|---|
| `.opencode/skills/analyze-and-improve/SKILL.md` | Skill principal | ~8 seções alteradas (T1-T7) |
| `.opencode/skills/harness-analyze-and-improve/SKILL.md` | Skill harness | Sincronização (T11) |
| `harness/GUIDE-analyze-and-improve.md` | Guia operacional | Atualização substancial (T10) |
| `.opencode/skills/analyze-and-improve/harness/templates/test-results.json` | Template canônico | Campo evidence Phase 4 (T12) |
| `.opencode/skills/analyze-and-improve/harness/templates/PROGRESS.md` | Template | Referências (T13) |
| `docs/system-of-record.md` | Índice canônico | Nota sobre formato legacy (T9) |
| 8× `docs/analysis/*/integration-roadmap.md` | Históricos | Banner de depreciação (T8) |

Nenhum arquivo novo é criado. O artifacts manifest template vive inline no SKILL.md, não como arquivo separado.
