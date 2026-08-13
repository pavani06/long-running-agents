---
title: "Solução 02 — Escrever e recuperar um fato durável (comentada)"
type: curriculum-exercise
nivel: 1
aliases: ["solução 02", "solution primeiro fato", "gabarito durable-fact query"]
tags: [curriculo-conteudo, nivel-1, solucao, substrato, durable-fact, obsidian-eval, query]
relates-to:
  - "[[exercises/exercise-02-primeiro-fato|Exercício 02]]"
  - "[[02-fatos-duraveis|Lição 02 — Fatos Duráveis]]"
  - "[[04-obsidian-eval|Lição 04 — obsidian-eval]]"
  - "[[vault:sisyphus-runtime/facts/_global/constraints|Constraints Acumuladas]]"
last_updated: 2026-08-13
---

# ✍️✅ Solução 02 — Escrever e recuperar um fato durável (comentada)

**Nível:** 1 — O Substrato · **Referente a:** `exercises/exercise-02-primeiro-fato.md`

---

## 1) O fato válido

O arquivo `facts/_global/constraints.md` que passa no critério — frontmatter tipado + corpo em
lista com procedência:

```yaml
---
id: fact.constraints.global
title: Accumulated Constraints — Global
type: durable-fact
kind: constraint
repo: _global
confidence: high
valid_from: 2026-08-13
last_updated: 2026-08-13
tags:
  - runtime-state
  - constraints
---

## constraints

- "Sempre usar obsidian-eval query em vez de search" (source: session 2026-08-13-nivel1)
```

**Comentário campo a campo:**

- `type: durable-fact` — a chave mestra; é o que o `query` filtra primeiro.
- `kind: constraint` — a espécie. Discrimina de `preference`/`principle`/`ground-truth`.
- `confidence: high` — coerente com o vault real, onde essa exata regra é `high` (evidence: 2
  handoffs).
- `valid_from` — quando o fato entra em vigor. Sem isso, não há raciocínio temporal.
- corpo em **lista**, não prosa — recuperável e diffável (lição 02).
- `(source: ...)` — a procedência **obrigatória**. Sem ela, reprova no critério (b) do terceiro.

---

## 2) Escrita pela porta certa (`obsidian-eval`)

Criar o arquivo do zero com `write`:

```bash
obsidian-eval ~/sisyphus-runtime write facts/_global/constraints.md \
  '{"type":"durable-fact","kind":"constraint","repo":"_global","confidence":"high","valid_from":"2026-08-13"}' \
  '## constraints

- "Sempre usar obsidian-eval query em vez de search" (source: session 2026-08-13-nivel1)'
```

Apensar **outro** item depois, sem reescrever o arquivo, com `append-fact`:

```bash
obsidian-eval ~/sisyphus-runtime append-fact facts/_global/constraints.md constraints \
  -- '- "Toda operacao de vault passa por obsidian-eval, nunca pelo app" (source: ground-truth)'
```

**Por que dois verbos:** `write` **substitui** a nota inteira; `append-fact` **acumula** um item
na lista nomeada (`constraints`) preservando o resto. É o mesmo par de semânticas da lição 01,
agora nos comandos. Editar pelo app faria o mesmo byte no disco — e ainda assim estaria errado,
porque bypassa a única porta auditável do loop (lição 04, regra em três camadas de confiança).

---

## 3) A recuperação por `query`

```bash
obsidian-eval ~/sisyphus-runtime query \
  "filter(n => n.frontmatter.type === 'durable-fact' && n.frontmatter.kind === 'constraint')"
```

Saída esperada (resumida): a nota `facts/_global/constraints.md` aparece, com seu frontmatter e
as constraints do corpo. O predicado casa em `type` **e** `kind` — precisão que só a tipagem
permite.

---

## 4) A prova negativa

```bash
obsidian-eval ~/sisyphus-runtime query \
  "filter(n => n.frontmatter.type === 'durable-fact' && n.frontmatter.kind === 'preference')"
```

Saída esperada: **vazio** (você não escreveu nenhuma `preference`). Se o seu fato aparecesse
aqui, o `kind` estaria errado ou ausente. O vazio prova que a tipagem discrimina — é o oposto do
que `search "constraint"` faria, que traria qualquer nota que **mencione** a palavra.

---

## 🧭 Como o terceiro avalia

Ele recebe **só** o seu `facts/_global/constraints.md`. Escreve o `query` **dele** — que, se o
seu frontmatter está correto, será essencialmente igual ao do passo 3 — e roda. Passa quando:

- (a) o predicado **dele** retorna o seu fato (frontmatter bem tipado), e
- (b) ele rastreia a `source` sem te perguntar.

Se o `query` dele volta vazio, o suspeito nº 1 é typo no `kind` (`contraint`) ou `type` ausente —
a tipagem é literal, e é justamente aí que o terceiro pega o que você não veria sozinho.

## ❌ Erros comuns que reprovam

- Fato sem `(source: ...)` → boato durável; reprova em (b).
- Fato escrito em `state/current/` → confunde *acumula* com *substitui*; não é memória durável.
- Recuperar com `search` em vez de `query` → falso-positivos; o exercício exige predicado sobre
  frontmatter.
- `valid_from` ausente → o fato "existe" mas sem vigência temporal; frágil para raciocínio
  cross-session.
