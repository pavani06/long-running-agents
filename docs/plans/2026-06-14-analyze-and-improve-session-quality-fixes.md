# analyze-and-improve — Correções de Qualidade de Sessão (Anatomy of Intent) — Plano de Execução

**Objetivo:** Corrigir 3 falhas de processo e UX identificadas na execução do pipeline analyze-and-improve em 2026-06-14 (The Anatomy of Intent — ICE in IDSD). 1 alteração no `harness-analysis.sh`, 2 alterações na `SKILL.md`, 1 novo script.
**Fase:** Planejamento → Implementação
**Dependências:** Nenhuma (correções autônomas)
**Duração estimada:** 1 sessão (60-90 min)

---

## Contexto

A execução do pipeline no documento "The Anatomy of Intent" (Kapil Viren Ahuja, 2026-05-27) expôs três falhas recorrentes:

1. **PROGRESS.md stale entre sessões** — O pipeline canary-test concluiu e foi commitado, mas o `PROGRESS.md` permaneceu com estado "In Progress: phase-0". O setup sobrescreveu corretamente, mas o arquivo commitado entre pipelines carrega lixo de sessão anterior. Nesta sessão, o mesmo padrão se repetiu: o `PROGRESS.md` commitado tem seções duplicadas, itens unchecked órfãos, e análise context stale.

2. **Full rebuild desnecessário** — Havia um modelo mental de 2 dias (`2026-06-12-idsd-method`) do mesmo autor e mesma série temática. O default `incremental=false` foi aplicado sem questionamento, resultando em ~10min e ~50K tokens extras vs um incremental de 3-5min. O skill não tem heurística de elegibilidade automática para modo incremental.

3. **Gap de heartbeat durante Phase 4** — 3 agentes paralelos rodaram por ~7 minutos. O orquestrador ficou em silêncio total, sem atualizações de progresso. O usuário precisou cutucar ("e ai") para verificar se a sessão estava viva. A Rule 17 (Background Task Discipline) foi interpretada como "silêncio total" em vez de "não aja sobre resultados parciais, mas comunique progresso".

---

## Tarefas

### Tarefa 1: PROGRESS.md — Reset automático após pipeline

**Problema:** `PROGRESS.md` é escrito no setup e mutado durante o pipeline, mas nunca resetado. Após commit, o arquivo permanece com estado da sessão anterior (fases checked, contexto stale), poluindo o repositório entre execuções.

**Solução:** Adicionar passo `phase-done` que reseta `PROGRESS.md` para template limpo. Executar durante a Phase 5 (Integration) ou como passo final antes do Commit Gate.

**Artefatos:**
- Entrada: `.opencode/skills/analyze-and-improve/harness/setup-analysis.sh` (template de referência)
- Saída 1: `.opencode/skills/analyze-and-improve/harness/templates/PROGRESS-clean.md` (novo template limpo)
- Saída 2: `.opencode/skills/analyze-and-improve/SKILL.md` (nova seção no Commit Gate)

- [ ] **Passo 1: Criar template limpo.**
  Criar `harness/templates/PROGRESS-clean.md` com o conteúdo mínimo — sem contexto de análise, sem fases checked:
  ```
  # PROGRESS.md — Análise de fonte externa

  > Pipeline analyze-and-improve gerenciado pelo harness.
  > Cada fase é uma feature com contrato default-FAIL.
  > O harness avança automaticamente entre fases.

  ## Done

  <!-- Fases concluídas e aprovadas pelo evaluator -->

  ## In Progress

  <!-- A fase atual. Exatamente UMA por vez. -->

  ## Next

  <!-- Próximas fases na fila -->

  ## Notes

  - Stack: Node.js, OpenCode agents, Obsidian-compatible markdown
  - Rodar: não se aplica (análise de documento, não build de código)
  - Testar: `bash scripts/check-obsidian-conventions.sh`
  ```

- [ ] **Passo 2: Adicionar passo de reset ao SKILL.md.**
  Na seção "Commit Gate" do `SKILL.md`, adicionar após o passo de push:
  ```
  ### Passo 2.5: Resetar PROGRESS.md para template limpo

  Após commit bem-sucedido (antes ou depois do push, a critério do usuário),
  o orquestrador DEVE resetar PROGRESS.md para o estado limpo:

  ```bash
  cp harness/templates/PROGRESS-clean.md PROGRESS.md
  git add PROGRESS.md
  git commit -m "chore(harness): reset PROGRESS.md after pipeline completion"
  ```

  Se o usuário optar por não commitar o reset, o arquivo fica modificado
  localmente e será sobrescrito pelo próximo `setup-analysis.sh`.

  **ANTI-PATTERN:** Deixar `PROGRESS.md` com contexto de análise concluída
  commitado no repositório. Isso polui o estado entre sessões e causa falsos
  positivos de "pipeline em andamento" na próxima execução.
  ```

- [ ] **Passo 3: Verificação.**
  Após editar o SKILL.md, rodar `bash scripts/check-obsidian-conventions.sh` no arquivo (se aplicável). Confirmar que `harness/templates/PROGRESS-clean.md` existe e tem conteúdo mínimo.

---

### Tarefa 2: Modo incremental — Heurística de elegibilidade automática

**Problema:** O orquestrador decide full rebuild vs incremental baseado apenas no parâmetro explícito `incremental=true`. Se o usuário não passa o parâmetro, o default `false` é aplicado sem considerar se o `mapa-mental-repo/` tem um modelo recente e relevante. Isso viola o espírito do AGENTS.md Rule 2 (Minimum Viable Change).

**Solução:** Adicionar ao SKILL.md um passo de "incremental eligibility check" que o orquestrador executa antes de decidir entre full rebuild e incremental. Se o modelo mais recente tem < 7 dias E mesmo domínio temático → sugerir ou adotar incremental.

**Artefatos:**
- Entrada: `.opencode/skills/analyze-and-improve/SKILL.md`
- Saída: mesmo arquivo, nova seção "Incremental Eligibility Check" no início da Phase 0

- [ ] **Passo 1: Localizar ponto de inserção.**
  Comando no SKILL.md: localizar a seção "## Phase 0: Repository Mental Model". O check deve ser inserido ANTES da decisão "Modo Full Rebuild" vs "Modo Incremental", como um passo preliminar executado pelo orquestrador.

- [ ] **Passo 2: Adicionar seção "Incremental Eligibility Check".**
  Inserir entre o cabeçalho "## Phase 0" e a subseção "### Modo Full Rebuild":
  ```
  ### Passo 0-pre: Incremental Eligibility Check (orquestrador — NÃO delegar)

  Antes de decidir entre full rebuild e incremental, o orquestrador DEVE:

  1. **Verificar modelos recentes**: Liste `mapa-mental-repo/*.yaml` por data.
     Se o diretório está vazio → full rebuild (sem escolha).

  2. **Carregar o modelo mais recente**: Leia o `.yaml` mais recente.
     Extraia `meta.date` e os campos `terminology`, `goals`, `patterns`.

  3. **Calcular relevância temática**: Compare o `source-slug` da análise atual
     com o `source-slug` do modelo. Heurísticas de match:
     - Ambos contêm o mesmo acrônimo (ex: "idsd", "ice", "sdd") → ALTA
     - Ambos pertencem à mesma série do mesmo autor → ALTA
     - Compartilham ≥2 domínios de system-of-record → MÉDIA
     - Sem sobreposição temática → BAIXA

  4. **Decidir modo**:
     - Se `dias_desde_modelo <= 7` E `relevância >= MÉDIA` → **adotar incremental automaticamente** (sem perguntar)
     - Se `dias_desde_modelo <= 30` E `relevância == ALTA` → **adotar incremental automaticamente**
     - Se `dias_desde_modelo <= 30` E `relevância == MÉDIA` → **sugerir incremental ao usuário** via commentary
     - Caso contrário → full rebuild (default)

  5. **Documentar a decisão** no commentary: "Usando modo incremental com base em
     `mapa-mental-repo/<modelo-anterior>` (X dias, relevância Y)."

  Se incremental for adotado, pular para "### Modo Incremental". Caso contrário,
  prosseguir com "### Modo Full Rebuild".
  ```

- [ ] **Passo 3: Atualizar a descrição do parâmetro `incremental`.**
  No topo do SKILL.md, na tabela de parâmetros, adicionar à descrição de `incremental`:
  ```
  | `incremental` | Não | Boolean, default `false`. Quando `true`, Phase 0 reusa o modelo mental mais recente. **Novo:** Se não especificado, o orquestrador aplica heurística de elegibilidade automática (Passo 0-pre). Passe `incremental=false` explicitamente para forçar full rebuild mesmo com modelo recente. |
  ```

- [ ] **Passo 4: Verificação.**
  Teste mental com 3 cenários:
  - Cenário A: `mapa-mental-repo/` vazio → full rebuild (correto)
  - Cenário B: modelo de 2 dias, mesmo autor, mesma série → incremental automático (correto)
  - Cenário C: modelo de 25 dias, domínio diferente → full rebuild (correto)

---

### Tarefa 3: Progress heartbeat — Comunicação durante background tasks

**Problema:** Durante execução de background tasks (Phase 4, tipicamente 4-7 minutos), o orquestrador fica em silêncio total. O usuário não tem visibilidade de progresso e precisa cutucar manualmente. A Rule 17 foi interpretada como "não emita nada" quando deveria ser "não colete outputs, mas comunique milestones".

**Solução:** Adicionar regra explícita no SKILL.md: a cada notificação `[BACKGROUND TASK RESULT READY]`, o orquestrador emite um commentary curto com progresso. A Rule 17 do AGENTS.md também deve ser atualizada para explicitar essa distinção.

**Artefatos:**
- Entrada 1: `.opencode/skills/analyze-and-improve/SKILL.md`
- Entrada 2: `AGENTS.md` (Rule 17)
- Saída: ambos os arquivos modificados

- [ ] **Passo 1: Adicionar regra de heartbeat ao SKILL.md.**
  Na seção "Anti-Patterns" do SKILL.md, adicionar:
  ```
  - **Ficar em silêncio durante background tasks.** Quando agentes paralelos
    estão rodando (Phase 4 típica), o orquestrador DEVE emitir commentary de
    progresso a cada notificação `[BACKGROUND TASK RESULT READY]`. O formato:
    "Phase 4a concluída (4m23s), 2/3 completos. Aguardando 4c (exercises)."
    Isso mantém o humano no loop sem violar a Rule 17 — o orquestrador NÃO
    coleta outputs parciais, apenas sinaliza milestones.
  ```

- [ ] **Passo 2: Adicionar regra de heartbeat à seção de execução da Phase 4.**
  No bloco de delegação da Phase 4 (após dispatches paralelos), adicionar:
  ```
  ### Heartbeat durante execução paralela

  Enquanto os agentes 1-3 rodam em background, o orquestrador DEVE:

  1. A cada notificação `[BACKGROUND TASK RESULT READY]`, emitir commentary:
     "Phase 4a concluída (XmYs), N/3 completos. Aguardando restantes."
  2. NUNCA chamar `background_output()` antes de `ALL COMPLETE`.
  3. Se o tempo total estimado exceder 5 minutos, emitir um commentary
     adicional com ETA: "Exercises é o mais longo (~7min histórico)."
  4. Após `ALL COMPLETE`, coletar todos os outputs em batch e prosseguir.
  ```

- [ ] **Passo 3: Atualizar AGENTS.md Rule 17.**
  A Rule 17 atual diz:
  > Do NOT react to individual [BACKGROUND TASK RESULT READY] notifications.
  > These are informational only.

  Clarificar a distinção entre "react" (agir/coletar) e "acknowledge" (comunicar):
  ```
  ## Rule 17: Background Task Discipline

  When using parallel background agents (run_in_background=true):

  - Do NOT collect results from individual [BACKGROUND TASK RESULT READY]
    notifications via background_output(). These are informational only
    for progress tracking, not action triggers.
  - You MAY emit short commentary acknowledging progress ("Phase 4a done,
    2/3 complete") — this keeps the human in the loop without violating
    the rule against premature result collection.
  - Wait for [ALL BACKGROUND TASKS COMPLETE] before collecting
    any results via background_output().
  - Collect ALL results in a single batch after ALL COMPLETE.
  ```

- [ ] **Passo 4: Verificação.**
  Teste mental: simular Phase 4 com 3 background tasks.
  - Notificação 1 (bg_1 pronto) → commentary "1/3" emitido, sem background_output
  - Notificação 2 (bg_2 pronto) → commentary "2/3" emitido, sem background_output
  - Notificação 3 (ALL COMPLETE) → background_output nos 3, prossegue pipeline
  - Entre notificações: o usuário vê 3 commentaries de heartbeat, não 8 minutos de silêncio

---

## Sequência de execução

```
1. Tarefa 3, Passo 3: AGENTS.md Rule 17 (clarificação)     ← menos acoplada
2. Tarefa 1, Passo 1: PROGRESS-clean.md (template novo)     ← independente
3. Tarefa 1, Passo 2: SKILL.md Commit Gate (reset)          ← depende de 1.1
4. Tarefa 2, Passo 2: SKILL.md Phase 0 (eligibility check)  ← independente
5. Tarefa 2, Passo 3: SKILL.md parâmetro incremental        ← mesmo arquivo que 1.2
6. Tarefa 3, Passo 1: SKILL.md Anti-Patterns (heartbeat)    ← mesmo arquivo
7. Tarefa 3, Passo 2: SKILL.md Phase 4 (heartbeat)          ← mesmo arquivo
```

As tarefas 3.1 (AGENTS.md) e 1.1 (template) são independentes e podem ser feitas em paralelo. As edições no SKILL.md (1.2, 2.2, 2.3, 3.1-skill, 3.2) são no mesmo arquivo — fazer sequencialmente para evitar conflitos de `edit`.

---

## Verificação final

- [ ] `bash scripts/check-obsidian-conventions.sh` passa limpo
- [ ] `git diff --stat` mostra apenas `AGENTS.md`, `SKILL.md`, `PROGRESS-clean.md`
- [ ] Teste mental dos 3 cenários de incremental eligibility (Tarefa 2, Passo 4)
- [ ] Teste mental do heartbeat (Tarefa 3, Passo 4)
- [ ] `PROGRESS-clean.md` é um subset estrito de `PROGRESS.md` (não introduz novos campos)
