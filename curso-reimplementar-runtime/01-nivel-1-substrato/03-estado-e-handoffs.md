---
title: "Estado corrente e handoffs: a memória que substitui e a que passa adiante"
type: curriculum-lesson
nivel: 1
aliases: ["estado e handoffs", "state/current", "session-handoff", "handoff budget-aware", "continuidade"]
tags: [curriculo-conteudo, nivel-1, substrato, state, session-handoff, budget-aware, continuidade]
relates-to:
  - "[[vault:sisyphus-runtime/state/current/objective|Objetivo Corrente]]"
  - "[[vault:sisyphus-runtime/state/current/working-memory|Working Memory]]"
  - "[[vault:sisyphus-runtime/state/current/open-decisions|Decisões Abertas]]"
  - "[[vault:sisyphus-runtime/sessions/_global/2026-06-16-sisyphus-budget-red-handoff|Handoff Budget Red]]"
  - "[[vault:sisyphus-runtime/catalog/omitted-context|Catálogo de Contexto Omitido]]"
  - "[[02-fatos-duraveis|Lição 02 — Fatos Duráveis]]"
  - "[[GLOSSARY|Glossário]]"
last_updated: 2026-08-13
---

# 🔄 Estado corrente e handoffs: a memória que substitui e a que passa adiante
## Como uma sessão que vai morrer entrega o bastão para a próxima sem perder o passo

**Tempo Estimado:** 55 minutos
**Nível:** 1 — O Substrato
**Pré-requisito:** `02-fatos-duraveis.md`
**Status:** 🟢 FUNDAÇÃO — é o mecanismo de continuidade; sem ele, cada sessão recomeça do zero

---

## 📖 Prólogo: a sessão que sabia que ia morrer

Em 16 de junho, uma variável de ambiente forçou o cenário que todo sistema de longa duração
teme: `BUDGET_FORCE_PHASE=red`. Orçamento no vermelho. A sessão não tinha mais fôlego para
continuar o trabalho — e, em vez de morrer no meio da frase, ela fez a única coisa digna que
uma sessão pode fazer ao acabar: **escreveu um handoff**.

O arquivo `sessions/_global/2026-06-16-sisyphus-budget-red-handoff.md` é esse bastão. Olhe o
frontmatter dele — não é prosa de despedida, é um **payload estruturado**:

> `budget_percentage: <=20%` · `trigger: red-phase` · `open_decisions: [validar que canonical-context carrega handoff..., verificar budget ledger..., confirmar arquivamento de state/current/]` · `continuity_message: "Retomar teste E2E: carregar contexto..."`

A sessão sabia quanto orçamento tinha (`budget_context`), sabia o que deixou em aberto
(`open_decisions`), e escreveu a **mensagem de continuidade** que a próxima sessão leria como
primeira instrução. Ela morreu ordenada. A próxima acordou sabendo exatamente onde pegar.

Essa é a diferença entre um sistema que roda por horas e um que roda por *sessões encadeadas*
por dias: o handoff. E o handoff só funciona porque o `state/current/` — a foto do agora — foi
**arquivado** no mesmo gesto, para não mentir para a sessão seguinte (o defeito do prólogo da
lição 01).

---

## 🧠 O conceito: duas memórias de curto prazo, com verbos opostos

O Nível 1 tem três memórias. A durável (`facts/`, lição 02) *acumula*. As outras duas, desta
lição, são de curto prazo e têm verbos opostos entre si:

### `state/current/` — a foto que se **substitui**

É o *agora* do sistema, em quatro arquivos vivos (rode `ls ~/sisyphus-runtime/state/current/`):

| Arquivo | O que carrega |
|---|---|
| `objective.md` | o objetivo corrente, em uma frase densa |
| `working-memory.md` | a lista de "o que está na cabeça" desta fase |
| `open-decisions.md` | decisões pendentes de operador/sessão |
| `repo.md` | qual repo é o foco corrente |

Existe **uma** versão de cada. Escrever é sobrescrever. Quando o foco vira, o `current/` inteiro
rotaciona para `state/archive/<data>/` — e é isso que impede o "stale por 18 dias". O
`last_updated` (ISO 8601, ex.: `2026-08-10T23:08:34Z`) é o detector de deriva: se o `current`
está velho, ele está mentindo.

### `sessions/` — o bastão que se **passa adiante**

Cada [[GLOSSARY|handoff]] é uma nota `type: session-handoff`, namespaced por repo
(`sessions/_global/`, `sessions/long-running-agents/`...). Diferente do `current`, sessions
**apensa**: cada handoff é um arquivo novo, datado, que fica. É o registro histórico de como o
bastão passou de mão em mão.

### O que faz um handoff ser *budget-aware*

O adjetivo é o coração da coisa. Um handoff não é escrito "quando dá" — ele é **disparado por
orçamento**. O frontmatter do exemplo carrega:

- **`trigger`** — o que causou o handoff (`red-phase`, orçamento no vermelho).
- **`budget_percentage`** e **`budget_context`** (`burn_rate`, `accelerating`, `phase_reason`)
  — quanto restava e se estava acelerando. A próxima sessão sabe se herda uma corrida ou uma
  caminhada.
- **`open_decisions`** — o que ficou pendente (espelha o `state/current/open-decisions.md`).
- **`continuity_message`** — a **primeira instrução** que a próxima sessão executa. É o bastão.
- **`memory_handles`** — ponteiros para contexto grande omitido (ligação com `catalog/`, adiante).
- **`summary_buffer`** — o resumo do que a sessão fez, comprimido.

A ideia canônica: uma sessão que sente o orçamento acabar **prefere gastar os últimos tokens
escrevendo um handoff limpo** a gastar tentando terminar e morrer no meio. Um handoff bom é mais
valioso que meio trabalho a mais.

### `catalog/` — o que não coube no handoff

Nem tudo cabe no payload. O `catalog/omitted-context.md`
(`[[vault:sisyphus-runtime/catalog/omitted-context|Catálogo]]`) é a **memória endereçável**: uma
tabela de contexto que ficou de fora, com `ID | Kind | Location | Preview | Fetch`. O handoff
carrega o *handle* (o ID leve); o catálogo diz **como buscar** o conteúdo pesado se a próxima
sessão precisar. É a diferença entre carregar a biblioteca e carregar o cartão do acervo.

### O ciclo de vida de um handoff

Repare no frontmatter do exemplo: `status: reflected`, `reflected_at`, `reflection_batch`. Um
handoff nasce, é consumido pela sessão seguinte, e depois é **refletido** — processado em lote
para extrair o que virou fato durável. É assim que a memória de curto prazo (`sessions/`)
alimenta a de longo prazo (`facts/`): o handoff é efêmero-com-registro; o que ele ensinou, se
durável, migra para `facts/`.

---

## 🔎 Por que esta lição fecha o tripé da memória

Fatos (lição 02) são o que o sistema *sabe*. Estado e handoffs (esta) são o que o sistema *está
fazendo* e *como entrega o bastão*. Sem `facts/`, cada sessão reaprende tudo. Sem `state/` +
`sessions/`, cada sessão recomeça sem saber onde a anterior parou. O runtime só é "long-running"
porque encadeia sessões curtas por este mecanismo — e o `budget-aware` é o que garante que a
corrente não arrebente justo quando o orçamento aperta.

---

## 🧪 Exercício

**Contexto.** Simule o fim de uma sessão sua sob pressão de orçamento.

1. **Tire a foto.** Preencha os quatro arquivos de um `state/current/` (`objective`,
   `working-memory`, `open-decisions`, `repo`) para uma tarefa qualquer que você esteja fazendo.
   Ponha `last_updated` em ISO 8601.
2. **Escreva o bastão.** Componha um `session-handoff` com o frontmatter budget-aware: `trigger`,
   `budget_percentage`, `open_decisions`, e — o campo que mais importa — um `continuity_message`
   que a próxima sessão possa executar **sem te perguntar nada**.
3. **Rotacione.** Descreva o gesto que arquiva o `current/` atual em `state/archive/<data>/`
   antes de o próximo foco sobrescrever. Por que este passo evita o "stale por 18 dias"?

**Critério de aprovação (medição de terceiro):** entregue **apenas** o seu handoff (sem o
`state/current/`, sem conversa) a outra pessoa e peça que ela diga qual é o próximo passo. Se ela
acerta o próximo passo só lendo o `continuity_message` e `open_decisions`, o bastão passou. Se ela
precisa te perguntar, o handoff reprovou.

> 💡 A camada que escreve tudo isso — `obsidian-eval write` / `append-fact` — é a próxima lição.

---

## 🔗 Para ir fundo

- O estado corrente vivo: `[[vault:sisyphus-runtime/state/current/objective|Objetivo]]` · `[[vault:sisyphus-runtime/state/current/working-memory|Working Memory]]`
- Handoff budget-aware real: `[[vault:sisyphus-runtime/sessions/_global/2026-06-16-sisyphus-budget-red-handoff|Handoff Red Phase]]`
- Memória endereçável: `[[vault:sisyphus-runtime/catalog/omitted-context|Catálogo de Contexto Omitido]]`
- Próxima lição: `04-obsidian-eval.md` — a camada de acesso que toca todas as gavetas
