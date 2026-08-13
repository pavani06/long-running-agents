---
title: "obsidian-eval: a única porta de acesso ao vault"
type: curriculum-lesson
nivel: 1
aliases: ["obsidian-eval", "camada de acesso", "query vs search", "nunca usar o app"]
tags: [curriculo-conteudo, nivel-1, substrato, obsidian-eval, query, search, camada-de-acesso]
relates-to:
  - "[[vault:sisyphus-runtime/README|README do Runtime — Como usar]]"
  - "[[vault:sisyphus-runtime/facts/_global/preferences|Preferences: query > search]]"
  - "[[vault:sisyphus-runtime/facts/_global/principles|Principles]]"
  - "[[vault:sisyphus-runtime/facts/_global/ground-truth|Ground Truth]]"
  - "[[03-estado-e-handoffs|Lição 03 — Estado e Handoffs]]"
  - "[[GLOSSARY|Glossário]]"
last_updated: 2026-08-13
---

# 🔌 obsidian-eval: a única porta de acesso ao vault
## Por que `query` vence `search`, e por que o app Obsidian está proibido

**Tempo Estimado:** 45 minutos
**Nível:** 1 — O Substrato
**Pré-requisito:** `03-estado-e-handoffs.md`
**Status:** 🟢 FUNDAÇÃO — é o verbo com que você lê e escreve tudo do Nível 1

---

## 📖 Prólogo: a regra que foi escrita tantas vezes que virou ground-truth

Nas lições anteriores você já tropeçou nela três vezes, em três gavetas diferentes:

- Em `facts/_global/principles.md`: *"sempre usar obsidian-eval query em vez de search"*
  (confidence: **high**, evidence: 2 handoffs).
- Em `facts/_global/preferences.md`: *"Preferir obsidian-eval sobre obsidian CLI"*.
- Em `facts/_global/ground-truth.md`, elevada a **imutável, definida por humano**: *"Sempre
  usar obsidian-eval para operações em vaults, nunca o app Obsidian CLI"* — com o rationale:
  *"obsidian-eval é a interface canônica. Bypassá-lo quebra o modelo de runtime."*

Poucas regras no sistema aparecem como preference, como principle **e** como ground-truth ao
mesmo tempo. Quando uma verdade é escrita em todas as camadas de confiança, é porque o sistema
já pagou pelo erro oposto. A camada de acesso não é um detalhe de conveniência — é o que
mantém o modelo do runtime coerente. Toda escrita passa pela mesma porta, então toda escrita
é auditável, tipada e reproduzível. Abra uma porta lateral (o app) e o [[GLOSSARY|loop
operacional]] perde a garantia de que "não há porta de escrita fora do loop".

---

## 🧠 O conceito: uma CLI que fala frontmatter

[[GLOSSARY|obsidian-eval]] é a camada de acesso ao vault: uma CLI que lê e escreve as notas
Markdown **entendendo o frontmatter YAML** como dado estruturado. Você não abre o app, não
edita o arquivo à mão para operações de conteúdo — você chama o `obsidian-eval` contra o path
do vault. A forma geral (do `README` do runtime):

```bash
obsidian-eval ~/sisyphus-runtime <comando> [args]
```

### Os verbos de leitura: `scan`, `query`, `search`

```bash
# Panorama do vault inteiro
obsidian-eval ~/sisyphus-runtime scan

# QUERY — predicado sobre frontmatter (o jeito certo)
obsidian-eval ~/sisyphus-runtime query "filter(n => n.frontmatter.type === 'durable-fact')"

# QUERY — cruzando campos: handoffs de um repo específico
obsidian-eval ~/sisyphus-runtime query "filter(n => n.frontmatter.type === 'session-handoff' && n.frontmatter.repo === 'long-running-agents')"
```

**`query` vs `search` — a distinção que a lição inteira gira em torno:**

- **`query`** avalia um **predicado sobre o frontmatter estruturado**. Você pergunta por *tipo*,
  *kind*, *repo*, *confidence* — os campos tipados das lições 02 e 03. A resposta é **precisa**:
  ou o frontmatter satisfaz o predicado, ou não. É determinística e reproduzível.
- **`search`** é **texto livre** no corpo. Ela acha strings, não fatos. Sofre de falso-positivo
  (a palavra aparece numa citação, num exemplo, num comentário) e falso-negativo (o fato existe
  mas com outra redação). É a busca do desesperado.

Por isso o sistema gravou `query > search` em três camadas: um runtime que recupera memória por
`search` recupera *aproximações*; um que recupera por `query` recupera *o schema*. Toda a lição
02 (fatos tipados) e 03 (state/handoff tipados) existe **para que** `query` funcione. Usar
`search` sobre dados tipados é jogar fora a tipagem que você se deu o trabalho de criar.

> Regra prática: se você consegue expressar a pergunta como predicado sobre um campo do
> frontmatter, é `query`. Só caia para `search` quando a informação vive genuinamente no corpo
> em texto livre e não há campo que a capture — e, quando isso acontecer com frequência,
> considere **promover** aquele texto a um campo de frontmatter.

### Os verbos de escrita: `write` e `append-fact`

```bash
# WRITE — cria/sobrescreve uma nota inteira (frontmatter + corpo)
obsidian-eval ~/sisyphus-runtime write sessions/repo/2026-08-13-handoff.md '{"type":"session-handoff"}' '# Handoff'

# APPEND-FACT — apensa um item a uma lista de fato durável, sem reescrever o resto
obsidian-eval ~/sisyphus-runtime append-fact facts/repo/constraints.md constraints -- '- "Nova constraint" (source: session 2026-08-13)'
```

Note o casamento com os verbos do substrato: `write` para o que **substitui** (`state/current/`),
`append-fact` para o que **acumula** (`facts/`). A CLI tem um verbo para cada semântica da
lição 01.

### A exceção documentada: operações de diretório

Há **uma** brecha, e ela é explícita numa constraint do vault: operações de **diretório**
(`mkdir`, `mv`) são a única exceção — usadas só para **arquivar/mover** notas quando o
`obsidian-eval` não oferece comando equivalente (ex.: rotacionar `state/current/` para
`state/archive/`, lição 03). Nunca para *conteúdo*. E, mesmo aí, o app Obsidian CLI (`obsidian`)
segue **proibido**.

### Resolução de vaults

`obsidian-eval` resolve nomes de vault para paths via um registry. Você pode sobrescrever com a
env var `OBSIDIAN_EVAL_VAULTS` (JSON nome→path) e verificar com:

```bash
obsidian-eval list-vaults              # lista vaults conhecidos
obsidian-eval resolve-vault long-running-agents   # path de um vault
```

Isso é o que faz um wikilink `[[vault:long-running-agents/...]]` resolver na sua máquina — e o
que você vai configurar ao reimplementar o runtime num ambiente novo (Nível 4).

---

## 🔎 Por que esta lição fecha o Nível 1

Porque as três lições anteriores descrevem **o que** o substrato guarda; esta descreve **como
você toca nele sem quebrá-lo**. Um reimplementador que monta `facts/`, `state/` e `sessions/`
perfeitos mas lê tudo por `search` — ou pior, edita pelo app — construiu o substrato certo com
a porta errada, e a garantia de auditabilidade do loop cai por terra. A porta é única de
propósito: uma porta, um log, uma verdade.

---

## 🧪 Exercício

**Contexto.** Você tem o vault (ou uma cópia) e o `obsidian-eval` instalado.

1. **Query, não search.** Escreva o `query` que recupera **só** os fatos de `kind: constraint`
   do `_global`. Depois, escreva a `search` "equivalente" e liste dois falso-positivos ou
   falso-negativos que ela produziria e o `query` não.
2. **Case o verbo à semântica.** Para cada operação abaixo, diga qual comando usar e por quê:
   (a) atualizar o `objective.md` do `state/current/`; (b) registrar mais uma constraint
   acumulada; (c) mover o `state/current/` de ontem para `archive/`.
3. **Defenda a porta.** Em duas frases, explique a um colega por que editar um fato pelo app
   Obsidian — mesmo que "dê o mesmo resultado no arquivo" — viola o modelo do runtime.

**Critério de aprovação (medição de terceiro):** outra pessoa roda o seu `query` do passo 1
contra o vault e confirma que ele retorna exatamente o conjunto de constraints — nem a mais
(falso-positivo de search) nem a menos. Você não valida o próprio predicado.

> 💡 Escrever e recuperar um fato de ponta a ponta é o `exercises/exercise-02-primeiro-fato.md`.

---

## 🔗 Para ir fundo

- Comandos reais, seção "Como usar": `[[vault:sisyphus-runtime/README|README do Runtime]]`
- A regra em três camadas: `[[vault:sisyphus-runtime/facts/_global/principles|Principles]]` · `[[vault:sisyphus-runtime/facts/_global/ground-truth|Ground Truth]]`
- Fim do Nível 1. A seguir: **Nível 2 — A Máquina** (os papéis e o loop `dispatch → gate`).
