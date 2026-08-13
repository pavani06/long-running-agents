---
title: "Exercício 02 — Escrever um fato durável e recuperá-lo por query"
type: curriculum-exercise
nivel: 1
aliases: ["exercício 02", "primeiro fato durável", "append-fact e query"]
tags: [curriculo-conteudo, nivel-1, exercicio, substrato, durable-fact, obsidian-eval, query]
relates-to:
  - "[[02-fatos-duraveis|Lição 02 — Fatos Duráveis]]"
  - "[[04-obsidian-eval|Lição 04 — obsidian-eval]]"
  - "[[vault:sisyphus-runtime/facts/_global/constraints|Constraints Acumuladas]]"
  - "[[exercises/solutions/solution-02-primeiro-fato|Solução comentada 02]]"
last_updated: 2026-08-13
---

# ✍️ Exercício 02 — Escrever um fato durável e recuperá-lo por query
## O ciclo completo da memória: apensar com procedência, recuperar por predicado

**Tempo Estimado:** 40 minutos
**Nível:** 1 — O Substrato
**Pré-requisito:** `02-fatos-duraveis.md` e `04-obsidian-eval.md`
**Status:** 🟢 PRÁTICO — o primeiro fato que o seu runtime vai lembrar

---

## 🎯 Objetivo

Fazer a memória durável funcionar de ponta a ponta: escrever **um** `durable-fact` válido, com
frontmatter tipado e procedência, e depois **recuperá-lo** com `obsidian-eval query` — provando
que a próxima sessão conseguiria encontrá-lo por predicado, sem o seu contexto.

Use o esqueleto do exercício 01 como terreno.

---

## 📋 O que entregar

1. **Um fato válido.** Em `facts/_global/constraints.md`, crie (ou apense a) um fato durável com:
   - frontmatter com **`type: durable-fact`**, **`kind: constraint`**, **`confidence`**,
     **`valid_from`**, `repo: _global`, `last_updated`;
   - no corpo, uma lista `## constraints` com **pelo menos um** item terminado em `(source: ...)`.

   A asserção pode ser real do seu ambiente (ex.: *"Sempre usar obsidian-eval query em vez de
   search"* — que no vault real é `confidence: high`).

2. **Escrita pela porta certa.** A criação/apêndice deve passar por `obsidian-eval` — `write`
   para criar o arquivo, `append-fact` para apensar mais itens. **Não** edite pelo app nem à mão
   para o conteúdo. Registre o comando exato que você rodou.

3. **A recuperação.** Escreva e rode o `query` que recupera **só** os fatos de
   `kind: constraint`. Cole a saída. O seu fato tem de aparecer nela.

4. **A prova negativa.** Rode um `query` para `kind: preference` (que você **não** escreveu) e
   mostre que o seu fato **não** aparece — provando que a tipagem discrimina de verdade.

---

## ✅ Critério de aprovação (medição de terceiro)

Coerente com o [[GLOSSARY|Achado central]] do sistema — *afirmação sobre estado não vira durável
sem medição de terceiro* — **você não valida a própria recuperação**. Entregue a outra pessoa
apenas o seu `facts/_global/constraints.md` (não o seu `query`, não a sua saída). Peça que ela:

- (a) escreva, do zero, o `query` que ela usaria para achar constraints, e rode contra o seu
  arquivo;
- (b) confirme que consegue rastrear a `source` do seu fato **sem te perguntar**.

O exercício passa quando o `query` **dela** — não o seu — retorna o seu fato, e a `source` é
rastreável por ela. Se o predicado dela não acha o seu fato, o seu frontmatter está mal tipado.

---

## ⚠️ Armadilhas plantadas

- Item de fato **sem** `(source: ...)` → é boato durável, não fato durável. Reprova no critério (b).
- Pôr o fato em `state/current/` "porque é verdade agora" → confunde *acumula* com *substitui*
  (lição 01/03). Estado não é memória durável.
- Recuperar por `search "constraint"` em vez de `query` sobre `frontmatter.kind` → traz
  falso-positivos (a palavra "constraint" no corpo de outra nota). O passo 3 exige `query`.
- Digitar `kind: contraint` (typo) → o `query` do terceiro não acha nada. A tipagem é literal.

> 💡 **Solução comentada:** `exercises/solutions/solution-02-primeiro-fato.md`
