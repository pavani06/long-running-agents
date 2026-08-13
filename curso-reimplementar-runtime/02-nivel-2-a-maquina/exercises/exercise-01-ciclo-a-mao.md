---
title: "Exercício 01 — Um ciclo à mão: dispatch → review → gate → execução → verify → registry"
type: curriculum-exercise
nivel: 2
aliases: ["ciclo à mão", "exercise-01-ciclo", "rode um ciclo", "loop à mão"]
tags: [curriculo-conteudo, nivel-2, a-maquina, exercicio, loop, gate-design, medicao-de-terceiro]
relates-to:
  - "[[vault:sisyphus-runtime/roles/orchestrator|Charter — Orquestrador]]"
  - "[[vault:sisyphus-runtime/roles/momus|Charter — Momus]]"
  - "[[vault:sisyphus-runtime/facts/_global/dispatch-rule-post-exec-gate|Regra — Post-Exec Gate]]"
  - "[[vault:long-running-agents/docs/canonical/plan-execute-verify|Plan-Execute-Verify]]"
last_updated: 2026-08-13
---

# 🛠️ Exercício 01 — Um ciclo à mão
## Você vai ser os cinco papéis, um de cada vez, e rodar o loop inteiro numa pasta de brinquedo

**Tempo Estimado:** 90 minutos
**Nível:** 2 — A Máquina
**Pré-requisito:** as três lições do Nível 2 (`01`, `02`, `03`)
**Status:** 🟡 EXERCÍCIO-CHAVE — não se auto-aprova (medição de terceiro obrigatória)

---

## 🎯 O que você vai fazer

Você vai rodar **um ciclo completo do loop** — `dispatch → review → gate → execução efêmera
→ verify → registry` — **à mão**, sem frota de sessões, numa pasta de brinquedo. Você vai
encarnar cada papel por vez, e a regra que você tem de honrar é a que dói: **quem faz um
estágio não valida o próprio estágio.** No fim, o gate de saída não é conferido por você —
é conferido por um terceiro, porque é isso que a lição inteira ensina.

O objetivo **não** é escrever um dispatch impressionante. É sentir, no corpo, por que a
execução mora numa "sessão" separada de quem a despacha, e por que o gate mede o disco em vez
de ler a sua palavra.

> ⚠️ **Não toque no vault real.** Este exercício roda inteiro numa pasta de brinquedo (ex.:
> `/tmp/ciclo-a-mao/`). Você está *simulando* a estrutura do runtime, não escrevendo nele.

---

## 📐 Preparação

Monte a pasta de brinquedo com a forma mínima do vault (um tópico chamado `treino`):

```bash
mkdir -p /tmp/ciclo-a-mao/{dispatches/treino,oracle-reviews/treino,sessions/treino,state/treino/current,facts/_global}
cd /tmp/ciclo-a-mao
```

Você vai usar **três "sessões" separadas** para não trapacear com o contexto. Na prática:
abra **três terminais** (ou três abas), e trate cada um como uma sessão que só sabe o que
está em disco. Um terminal é o **hub/planejador/meta** (papéis standing), um é o **Momus**
(efêmero), um é o **executor** (efêmero). A regra de ouro: **um terminal nunca "lembra" o que
o outro pensou — ele só lê arquivos.**

---

## 🔟 Os passos (encarne um papel por vez)

### Passo 1 — 📝 PLANEJADOR: redija um dispatch trivial

No terminal-hub, escreva `dispatches/treino/dispatch-saudacao-v1.md`. A tarefa é
deliberadamente trivial (uma escrita só), para o foco ficar no *loop*, não no conteúdo.
Inclua as **cinco partes do intent** (Lição 03), com as duas obrigatórias explícitas:

- **Objetivo:** criar um arquivo de saudação com um conteúdo fixo.
- **Escritas nomeadas (literal, exaustivo):** `state/treino/current/saudacao.md` — e mais nada.
- **Escopo negativo:** não criar índice, não tocar `facts/`, não renomear nada, não criar
  outros arquivos em `state/`.
- **Verificação:** o arquivo existe, contém *exatamente* a linha especificada, e nenhum outro
  arquivo foi criado. Evidência a colar: `ls -la state/treino/current/` + `cat` do arquivo.
- **Destino/classe:** `Classe: custodia`; reportar `done` ao hub; handoff em `sessions/treino/`.

### Passo 2 — 🔀 ORQUESTRADOR: receba o handoff, não execute ainda

No terminal-hub, "receba" o dispatch. **Não crie o arquivo de saudação.** O charter proíbe:
o hub não redige e não executa. A única ação correta é spawnar um Momus-entrada. Simule o
spawn abrindo o **terminal-Momus** e dando a ele *só* isto: o path do dispatch e a instrução
"revise como Momus-entrada". Nada do que você pensou no passo 1.

### Passo 3 — 🔍 MOMUS-ENTRADA: julgue o plano e escreva o veredito em disco

No terminal-Momus, leia **só** `dispatch-saudacao-v1.md`. Julgue o *plano* (as escritas
nomeadas são exaustivas? o escopo negativo cobre as tentações? a verificação é mecânica?).
Escreva o veredito em `oracle-reviews/treino/2026-08-13-dispatch-saudacao-v1-entrada.md` com
o **bloco de proveniência obrigatório**:

```yaml
type: momus-verdict
topic: treino
dispatch: dispatches/treino/dispatch-saudacao-v1.md
reviewed:
  - dispatches/treino/dispatch-saudacao-v1.md
review_kind: entrada
veredito: PASS
findings: { bloqueante: 0, alto: 0, medio: 0, baixo: 0 }
session: treino-momus-1
schema: v1
```
(mais `date:` fora do bloco). **O arquivo é o veredito.** Depois, "morra" (feche a aba).

### Passo 4 — 🚪 ORQUESTRADOR: gate de entrada (leia o ARQUIVO, não a memória)

De volta ao terminal-hub, aplique o gate de entrada **sem** usar o que você "sabe" que o
Momus decidiu — leia o arquivo do veredito. Cheque, na ordem: o arquivo existe? o campo
`dispatch:` casa com o `REF` do dispatch? `review_kind: entrada`? bloqueantes = 0? Se tudo
casa → **tire sua baseline agora** (`ls -la --time-style=full-iso state/treino/current/ >
/tmp/ciclo-a-mao/baseline-hub.txt`) e spawne o executor (abra o terminal-executor).

### Passo 5 — ⚙️ EXECUTOR: materialize SÓ as escritas nomeadas, numa sessão separada

No terminal-executor, leia **só** o dispatch (autoridade única). Tire sua própria baseline,
crie **exatamente** `state/treino/current/saudacao.md` com a linha especificada, rode a
verificação do dispatch e cole a evidência num handoff em
`sessions/treino/2026-08-13-saudacao-done.md`. Emita `done` (uma linha para o hub) e "morra".

### Passo 6 — 📏 ORQUESTRADOR: gate de saída, Camada 1 (diff mecânico, SUA baseline)

De volta ao hub, rode a Camada 1: compare o disco atual contra `baseline-hub.txt` (a **sua**,
não a do executor). O conjunto de arquivos tocados é **exatamente** `{saudacao.md}`? Se sim,
Camada 1 passou. Se o executor tocou qualquer coisa a mais → suspeita de plan-step-substitution
→ você *pararia* e escalaria.

### Passo 7 — 👁️ ORQUESTRADOR: Camada 2, decida se o Momus-saída é obrigatório

Aplique `dispatch-rule-post-exec-gate`. Este dispatch é trivial, ≤2 arquivos, não-destrutivo,
sem arquivo sensível, e **não tocou `facts/` nem `roles/`** → o Momus-saída é **dispensado**.
Registre a decisão e por que a regra a permite.

### Passo 8 — ✅ REGISTRY: feche o ciclo

Anote em `state/treino/current/` (ou num `registry.md` de brinquedo) que o ciclo fechou:
dispatch, veredito, done, resultado do gate. Este é o "registry" derivado — se ele divergir
do disco, o disco vence.

### Passo 9 — 🕳️ Agora quebre o loop de propósito (o achado da lição)

Repita o ciclo com **um** sabotage, à sua escolha, e observe qual estágio deveria pegá-lo:
- (a) O executor cria **também** `state/treino/current/extra.md` (fora das escritas nomeadas).
- (b) O veredito do Momus tem `dispatch:` apontando para *outro* dispatch (proveniência não casa).
- (c) O "hub" pula o Momus e spawna o executor direto (sem veredito em disco).

Documente: **qual estágio pega cada sabotagem, e qual gatilho de escalação dispara.**

---

## ✅ Critério de aprovação — MEDIÇÃO DE TERCEIRO (obrigatória)

Este exercício **não se auto-aprova**. Coerente com o achado central do sistema — *afirmação
sobre estado não vira durável sem passar por medição de terceiro* — quem confere o seu gate
**não é você**.

Entregue a **outra pessoa** (ou outra sessão limpa) apenas o conteúdo da sua pasta de
brinquedo — os arquivos, não a sua narrativa. O terceiro deve, **lendo só o disco**:

1. **Reproduzir a Camada 1 do gate de saída:** tirar o diff entre a sua `baseline-hub.txt` e o
   estado final, e confirmar de forma **independente** que o executor tocou *exatamente* as
   escritas nomeadas — sem confiar no seu relatório nem no do executor.
2. **Casar a proveniência do veredito:** confirmar que o campo `dispatch:` do arquivo em
   `oracle-reviews/treino/` é idêntico ao `REF` do dispatch, e que `review_kind: entrada`.
3. **Confirmar as três sabotagens do passo 9:** para cada uma, verificar em disco que o estágio
   que você apontou realmente a pega — e que o gatilho de escalação bate com o charter.

O seu ciclo **só "passa"** quando o terceiro confirma os três itens **medindo o disco**, não
lendo a sua descrição. Se a medição dele divergir da sua afirmação, **a divergência é o
resultado** — e é exatamente o defeito que o sistema inteiro existe para pegar. Você não
aprova o próprio ciclo; esse é o ponto pedagógico inteiro.

> 💡 **Solução comentada:** `exercises/solutions/solution-01-ciclo-a-mao.md`
