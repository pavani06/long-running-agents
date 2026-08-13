---
title: "Exercício 01 — O esqueleto vazio do vault numa máquina nova"
type: curriculum-exercise
nivel: 1
aliases: ["exercício 01", "skeleton do vault", "árvore mínima do runtime"]
tags: [curriculo-conteudo, nivel-1, exercicio, substrato, skeleton, layout]
relates-to:
  - "[[01-layout-do-vault|Lição 01 — Layout do Vault]]"
  - "[[vault:sisyphus-runtime/_moc-runtime|MOC: Sisyphus Runtime]]"
  - "[[exercises/solutions/solution-01-skeleton|Solução comentada 01]]"
last_updated: 2026-08-13
---

# 🏗️ Exercício 01 — O esqueleto vazio do vault numa máquina nova
## Construir a árvore de diretórios mínima do runtime, do zero

**Tempo Estimado:** 30 minutos
**Nível:** 1 — O Substrato
**Pré-requisito:** `01-layout-do-vault.md`
**Status:** 🟢 PRÁTICO — o primeiro ato de reimplementação

---

## 🎯 Objetivo

Você acabou de sentar numa máquina limpa. Não há vault. Sua tarefa é levantar o **esqueleto**
do `sisyphus-runtime` — a árvore de diretórios mínima, com as gavetas certas e as semânticas
certas — sem nenhum conteúdo ainda. É o "terreno demarcado" antes de a memória começar a
acumular.

Não é copiar o vault real (você não pode — ele é privado e nunca vira git). É **reconstruir a
topologia** a partir do que você aprendeu na lição 01.

---

## 📋 O que entregar

1. **A árvore mínima.** Crie, sob um diretório novo (ex.: `~/sisyphus-runtime`), a estrutura de
   primeiro nível com as oito gavetas do sistema e as partições `_global`. No mínimo:
   - `facts/_global/`
   - `state/current/` e `state/archive/`
   - `sessions/_global/`
   - `catalog/`
   - `traces/`
   - `meta/`
   - `roles/`
   - `dispatches/`
2. **O ponto de entrada.** Um `_moc-runtime.md` e um `MANIFEST.md` mínimos na raiz — só o
   frontmatter e um título; conteúdo vem depois. O MANIFEST deve declarar `exports:
   [sessions, facts, state]`.
3. **A prova de que NÃO é git.** Demonstre que o diretório **não** é um repositório git e
   explique, em uma frase, por quê (lição 01: requests verbatim + decisões privadas).
4. **A verificação.** Rode um comando que liste a árvore que você criou e confirme que cada
   gaveta existe. (Dica: `find <vault> -maxdepth 2 -type d`.)

---

## ✅ Critério de aprovação (medição de terceiro)

Coerente com o princípio do curso: **você não aprova o próprio esqueleto**. Entregue a outra
pessoa **apenas** a saída do seu `find` (não o seu passo-a-passo) e peça que ela:

- (a) classifique cada diretório como *acumula / substitui / deriva* sem consultar a sua lição;
- (b) aponte qualquer gaveta faltante ou sobrando.

O exercício passa quando um terceiro reconstrói as semânticas a partir só da sua árvore e não
encontra gaveta faltante. Se ele precisa te perguntar "e onde ficam os handoffs?", a topologia
reprovou.

---

## ⚠️ Armadilhas plantadas (todas viraram lição real)

- Criar `state/` sem separar `current/` de `archive/` → você recria o "stale por 18 dias".
- Esquecer o `_global` em `facts/` e `sessions/` → você perde o namespace denominador-comum.
- Rodar `git init` "só para versionar" → viola a regra dura do `README` do runtime.
- Criar um `notes/` ou `docs/` genérico → não existe gaveta genérica; cada diretório é uma
  promessa. Se não sabe onde algo vai, ele provavelmente não vai.

> 💡 **Solução comentada:** `exercises/solutions/solution-01-skeleton.md`
