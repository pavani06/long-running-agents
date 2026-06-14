# analyze-and-improve — Correções Pós-Review (IDSD Method) — Plano de Execução

**Objetivo:** Corrigir as falhas de processo e qualidade identificadas na revisão do pipeline analyze-and-improve executado em 2026-06-12 (IDSD Method). 5 alterações na SKILL.md + 4 correções pontuais em arquivos.
**Fase:** Implementação
**Dependências:** Review consolidada da sessão IDSD Method (Agents 1-3)
**Duração estimada:** 1 sessão (60-90 min)

---
## Contexto

A execução do pipeline no documento IDSD (Kapil Viren Ahuja) expôs falhas de processo e qualidade:

**Processo (Agent 2 — FAIL):**
- Phase 0 sync falhou 3x antes de funcionar em background. Wall clock de 2-2.5h com ~47min de agent time.
- Pipeline estagnou entre fases — o orquestrador esperava input implícito em vez de avançar automaticamente.
- Phase 6 (+628 linhas) e Phase 4d (+4m46s) alongaram critical path sem ganho proporcional.

**Qualidade (Agent 3 — PASS com 3 Low):**
- `ice-craft-separation.md` omite `symphony-trap-awareness` no `relates-to`.
- `04-sprint-contracts.md` e `02-token-budgeting.md` têm `relates-to` desatualizados após integração curricular.

---
## Tarefas

### Tarefa 1: SKILL.md — Background-first como política obrigatória

**Artefatos:**
- Entrada: `.opencode/skills/analyze-and-improve/SKILL.md`
- Saída: mesmo arquivo, seção nova ou parágrafo adicionado

- [ ] **Passo 1: Localizar o ponto de inserção.**
  Comando: `rg -n "run_in_background" .opencode/skills/analyze-and-improve/SKILL.md`
  Esperado: identificar todas as menções atuais a `run_in_background` (estão nos blocos de exemplo de `task()`).

- [ ] **Passo 2: Adicionar regra na seção "Anti-Patterns".**
  Inserir após o último anti-pattern existente:
  ```
  - **Usar sync para fases de leitura pesada.** Fases que leem mais de 5 arquivos
    ou usam `ultrabrain`/`deep` como categoria DEVEM usar `run_in_background=true`.
    O harness interpreta silêncio como travamento em sync; background tem janela de
    inatividade maior e evita aborts.
  ```
  Esperado: anti-pattern visível na lista.

- [ ] **Passo 3: Atualizar todos os blocos de exemplo `task()` para background.**
  Para cada bloco `task()` nas fases 0, 1, 2, 3, 4a-d, 5, 6: trocar `run_in_background=false` por `run_in_background=true` nas fases 0, 1, 2, 3 (4a-c já são background). Fases 4d, 5, 6 mantêm sync pois são rápidas e dependem de outputs anteriores.
  Esperado: fases pesadas com `run_in_background=true`.

- [ ] **Passo 4: Verificação.**
  Comando: `rg "run_in_background=false" .opencode/skills/analyze-and-improve/SKILL.md`
  Esperado: apenas fases 4d, 5, 6 com false; fases 0-3 com true.

---

### Tarefa 2: SKILL.md — Paralelismo Phase 0 + Phase 1

**Artefatos:**
- Entrada: `.opencode/skills/analyze-and-improve/SKILL.md`
- Saída: mesmo arquivo, seção de execução atualizada

- [ ] **Passo 1: Localizar o fluxo de execução.**
  Comando: `rg -n "Phase 0" .opencode/skills/analyze-and-improve/SKILL.md | head -20`
  Esperado: identificar a seção que descreve a ordem de execução (provavelmente "Execution mechanism" ou similar).

- [ ] **Passo 2: Inserir regra de paralelismo.**
  Após a descrição da Phase 0 e Phase 1, adicionar:
  ```
  **Phase 0 e Phase 1 podem rodar em paralelo** quando o documento fonte
  (parâmetro `source`) já está disponível no início da sessão. A Phase 0
  lê o repositório; a Phase 1 lê o documento fonte — são independentes.
  Dispare ambas com `run_in_background=true` no mesmo turno e colete os
  resultados antes de prosseguir para Phase 2.
  ```
  Esperado: instrução de paralelismo visível.

- [ ] **Passo 3: Verificação.**
  Comando: `rg "podem rodar em paralelo" .opencode/skills/analyze-and-improve/SKILL.md`
  Esperado: 1 match.

---

### Tarefa 3: SKILL.md — Pipeline autônomo (auto-avanço entre fases)

**Artefatos:**
- Entrada: `.opencode/skills/analyze-and-improve/SKILL.md`
- Saída: mesmo arquivo, anti-pattern novo + instrução

- [ ] **Passo 1: Adicionar anti-pattern.**
  Na seção "Anti-Patterns", adicionar:
  ```
  - **Esperar input do usuário entre fases.** O pipeline é determinístico:
    output da fase N é input da N+1. Após cada `task()` completar, o
    orquestrador DEVE coletar o resultado, atualizar PROGRESS.md e disparar
    a próxima fase IMEDIATAMENTE. Os únicos gates que param o pipeline são
    o Commit Gate (perguntar antes de commit/push) e interrupção explícita
    do usuário.
  ```
  Esperado: anti-pattern visível.

- [ ] **Passo 2: Adicionar instrução no fluxo de execução.**
  Na seção que descreve o mecanismo de execução, adicionar parágrafo:
  ```
  O orquestrador NÃO deve pausar entre fases para check-in. O pipeline
  avança automaticamente: coleta output → atualiza PROGRESS.md → dispara
  próxima fase. Interrupção só por Commit Gate ou comando explícito.
  ```
  Esperado: instrução visível.

- [ ] **Passo 3: Verificação.**
  Comando: `rg "NÃO deve pausar entre fases" .opencode/skills/analyze-and-improve/SKILL.md`
  Esperado: 1 match.

---

### Tarefa 4: SKILL.md — Phase 6 como opt-in

**Artefatos:**
- Entrada: `.opencode/skills/analyze-and-improve/SKILL.md`
- Saída: mesmo arquivo, status da Phase 6 alterado

- [ ] **Passo 1: Localizar descrição da Phase 6.**
  Comando: `rg -n "Phase 6" .opencode/skills/analyze-and-improve/SKILL.md`
  Esperado: múltiplos matches. Identificar cabeçalho e descrição da fase.

- [ ] **Passo 2: Alterar status de "opcional" para "opt-in".**
  Substituir menções a "Phase 6: Curriculum Deep Integration (opcional)" por
  "Phase 6: Curriculum Deep Integration (opt-in — executar apenas quando solicitado)".
  Adicionar no início da seção da Phase 6:
  ```
  Esta fase NÃO faz parte do pipeline default. O orquestrador só a executa
  quando o usuário solicita explicitamente ("faça a integração curricular",
  "execute a Phase 6"). O escopo padrão do pipeline termina na Phase 5.
  ```
  Esperado: descrição reflete opt-in.

- [ ] **Passo 3: Atualizar a lista "Next" no template do PROGRESS.md (se existir).**
  Comando: `rg "phase-6" .opencode/skills/analyze-and-improve/SKILL.md`
  Se houver template de PROGRESS.md com phase-6 listada como default, remover.
  Esperado: phase-6 não aparece como fase automática.

- [ ] **Passo 4: Verificação.**
  Comando: `rg -i "opt-in" .opencode/skills/analyze-and-improve/SKILL.md`
  Esperado: pelo menos 1 match confirmando o novo status.

---

### Tarefa 5: SKILL.md — Fundir Phase 4d (Roadmap) na Phase 4a ou Phase 5

**Artefatos:**
- Entrada: `.opencode/skills/analyze-and-improve/SKILL.md`
- Saída: mesmo arquivo, Phase 4d removida como fase separada

- [ ] **Passo 1: Localizar definição da Phase 4d.**
  Comando: `rg -n "Phase 4.*Roadmap\|Integration Roadmap\|phase-4d\|4d" .opencode/skills/analyze-and-improve/SKILL.md`
  Esperado: identificar o bloco de delegação e descrição da Phase 4d.

- [ ] **Passo 2: Mover a responsabilidade do roadmap para a Phase 5.**
  Na seção da Phase 5, adicionar ao início:
  ```
  Antes de atualizar os índices, o agente DEVE ler os outputs da Phase 4
  (canonical docs, skills, exercises) e gerar uma seção de "Artifacts Created"
  dentro do próprio system-of-record.md ou como subseção da atualização.
  Isso substitui a antiga Phase 4d (integration roadmap separado).
  ```
  Esperado: instrução na Phase 5.

- [ ] **Passo 3: Remover ou comentar o bloco de delegação da Phase 4d.**
  Opção A: remover completamente o bloco `task(category="deep", ...)` da Phase 4d.
  Opção B: prefixar com comentário `<!-- OBSOLETO: fundido na Phase 5 -->`.
  Preferir opção A.
  Esperado: Phase 4d não aparece mais como fase independente.

- [ ] **Passo 4: Atualizar lista de fases e gates.**
  Procurar listas que enumeram as fases (como "Phases 0-5 obrigatórias, 6 opcional")
  e remover menção a 4d como fase separada.
  Esperado: referências consolidadas.

- [ ] **Passo 5: Verificação.**
  Comando: `rg -i "phase-4d\|Phase 4d\|4d.*roadmap\|roadmap.*4d" .opencode/skills/analyze-and-improve/SKILL.md`
  Esperado: zero matches (ou apenas comentários de obsolescência).

---

### Tarefa 6: PROGRESS.md — Remover bloco "In Progress" stale

**Artefatos:**
- Entrada: `PROGRESS.md`
- Saída: mesmo arquivo, seções "In Progress" e "Next" limpas

- [ ] **Passo 1: Remover bloco stale.**
  No arquivo `PROGRESS.md`, localizar a seção `## In Progress` (linhas 27-36) e `## Next` (linhas 38-45).
  Como todas as fases estão em `## Done`, remover completamente as seções "In Progress" e "Next"
  (ou deixar "Next" vazio como placeholder).
  Comando: `edit` para remover linhas 27-45.
  Esperado: PROGRESS.md só tem `## Done` e `## Analysis Context`.

- [ ] **Passo 2: Verificação.**
  Comando: `rg "In Progress" PROGRESS.md`
  Esperado: zero matches (ou apenas no cabeçalho explicativo no topo).

---

### Tarefa 7: ice-craft-separation.md — Completar relates-to

**Artefatos:**
- Entrada: `docs/canonical/ice-craft-separation.md:7`
- Saída: mesmo arquivo, `relates-to` com 1 link adicionado

- [ ] **Passo 1: Adicionar symphony-trap-awareness ao relates-to.**
  Localizar a linha 7 (`relates-to:`). Adicionar `"[[docs/canonical/symphony-trap-awareness|Symphony Trap Awareness]]"` à lista.
  Esperado: relates-to referencia todos os 5 canônicos irmãos.

- [ ] **Passo 2: Verificação.**
  Comando: `rg "symphony-trap-awareness" docs/canonical/ice-craft-separation.md`
  Esperado: 1+ matches.

---

### Tarefa 8: 04-sprint-contracts.md — Atualizar relates-to com canônicos ICE

**Artefatos:**
- Entrada: `curriculum/05-core-concepts/04-sprint-contracts.md:6`
- Saída: mesmo arquivo, `relates-to` com 3 links adicionados

- [ ] **Passo 1: Ler o frontmatter atual.**
  Comando: `sed -n '1,15p' curriculum/05-core-concepts/04-sprint-contracts.md`
  Esperado: visualizar o bloco YAML completo.

- [ ] **Passo 2: Adicionar os 3 canônicos ICE.**
  No campo `relates-to:`, adicionar:
  - `"[[docs/canonical/ice-craft-separation|ICE Craft Separation]]"`
  - `"[[docs/canonical/intent-five-part-primitive|Intent as Five-Part Primitive]]"`
  - `"[[docs/canonical/human-owned-expectations-boundary|Human-Owned Expectations Boundary]]"`
  Esperado: relates-to inclui os docs referenciados no corpo (linhas 715-717).

- [ ] **Passo 3: Verificação.**
  Comando: `rg "ice-craft-separation" curriculum/05-core-concepts/04-sprint-contracts.md`
  Esperado: matches no frontmatter E no corpo.

---

### Tarefa 9: 02-token-budgeting.md — Atualizar relates-to com token-economics

**Artefatos:**
- Entrada: `curriculum/01-nivel-1-fundamentals/02-token-budgeting.md:7`
- Saída: mesmo arquivo, `relates-to` com 2 links adicionados

- [ ] **Passo 1: Ler o frontmatter atual.**
  Comando: `sed -n '1,15p' curriculum/01-nivel-1-fundamentals/02-token-budgeting.md`
  Esperado: visualizar o bloco YAML completo.

- [ ] **Passo 2: Adicionar os 2 canônicos de token economics.**
  No campo `relates-to:`, adicionar:
  - `"[[docs/canonical/token-economics-gap-filling|Token Economics of Gap-Filling]]"`
  - `"[[docs/canonical/intent-five-part-primitive|Intent as Five-Part Primitive]]"`
  Esperado: relates-to inclui os docs referenciados no corpo (linhas 842-843).

- [ ] **Passo 3: Verificação.**
  Comando: `rg "token-economics-gap-filling" curriculum/01-nivel-1-fundamentals/02-token-budgeting.md`
  Esperado: 1+ matches.

---

## Verificação Final

- [ ] `rg "run_in_background=false" .opencode/skills/analyze-and-improve/SKILL.md` → apenas fases leves
- [ ] `rg "In Progress" PROGRESS.md` → zero matches no corpo
- [ ] `rg -i "symphony-trap-awareness" docs/canonical/ice-craft-separation.md` → presente
- [ ] `rg "ice-craft-separation" curriculum/05-core-concepts/04-sprint-contracts.md` → no frontmatter
- [ ] `rg "token-economics-gap-filling" curriculum/01-nivel-1-fundamentals/02-token-budgeting.md` → presente
- [ ] `bash scripts/check-obsidian-conventions.sh` → sem novas violações (as 5 preexistentes permanecem)
- [ ] `git diff --stat` → apenas os 6 arquivos alterados (SKILL.md, PROGRESS.md, 3 curriculum, 1 canonical)
- [ ] NÃO commitar — o Commit Gate pertence ao orquestrador
