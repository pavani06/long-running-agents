---
title: "Solução 01 — O esqueleto vazio do vault (comentada)"
type: curriculum-exercise
nivel: 1
aliases: ["solução 01", "solution skeleton", "gabarito esqueleto do vault"]
tags: [curriculo-conteudo, nivel-1, solucao, substrato, skeleton, layout]
relates-to:
  - "[[exercises/exercise-01-skeleton|Exercício 01]]"
  - "[[01-layout-do-vault|Lição 01 — Layout do Vault]]"
  - "[[vault:sisyphus-runtime/_moc-runtime|MOC: Sisyphus Runtime]]"
last_updated: 2026-08-13
---

# 🏗️✅ Solução 01 — O esqueleto vazio do vault (comentada)

**Nível:** 1 — O Substrato · **Referente a:** `exercises/exercise-01-skeleton.md`

> ⚠️ Não há **uma** árvore correta — há uma topologia correta. O que segue é uma solução de
> referência; o que importa é a semântica de cada gaveta, não a ordem em que você as criou.

---

## 1) A árvore mínima

```bash
VAULT=~/sisyphus-runtime
mkdir -p "$VAULT"/{facts/_global,state/current,state/archive,sessions/_global,catalog,traces,meta,roles,dispatches}
```

**Comentário — por que cada `mkdir`:**

- `facts/_global/` — a memória que **acumula** (lição 02). O `_global` é o denominador comum;
  projetos ganham `facts/<repo>/` depois.
- `state/current/` **e** `state/archive/` — separados de propósito. `current/` **substitui**
  (uma foto só); `archive/` **congela** as fotos velhas. Foi a ausência dessa separação que
  produziu o "stale por 18 dias" do prólogo da lição 01.
- `sessions/_global/` — os handoffs, que **apensam**, namespaced por repo.
- `catalog/`, `traces/`, `meta/`, `roles/`, `dispatches/` — as demais gavetas, cada uma com a
  sua promessa da tabela da lição 01.

Repare: **não criamos** `notes/`, `docs/`, `tmp/` nem nada genérico. Não existe gaveta
coringa. Se você não sabe onde algo vai, provavelmente ele não entra no substrato.

> Nota: `mkdir` é legítimo aqui porque criar **diretórios** é a exceção documentada do vault —
> operações de conteúdo (notas) é que passam obrigatoriamente por `obsidian-eval` (lição 04).

---

## 2) Ponto de entrada mínimo

`MANIFEST.md` na raiz, espelhando o real (`exports: sessions, facts, state`):

```yaml
---
type: vault-manifest
vault: sisyphus-runtime
exports:
  - sessions
  - facts
  - state
imports:
  - long-running-agents
---

# sisyphus-runtime — Manifest
Private runtime vault: session handoffs, durable facts, current state.
```

`_moc-runtime.md` mínimo — só frontmatter `type: moc` e os entry points como wikilinks. O
conteúdo (as listas de fatos, handoffs, estado) preenche-se conforme o vault ganha notas.

---

## 3) A prova de que NÃO é git

```bash
git -C ~/sisyphus-runtime rev-parse --is-inside-work-tree 2>&1
# esperado: "fatal: not a git repository ..." — que é o resultado DESEJADO
```

**Por quê:** o `README` do runtime é uma regra dura — o vault contém requests verbatim
(`traces/`) e decisões pendentes (`state/`) que não podem vazar em repo. Backup se faz com
`tar`/snapshot, nunca `git init`. Um esqueleto que já é repo git nasce em violação.

---

## 4) Verificação

```bash
find ~/sisyphus-runtime -maxdepth 2 -type d | sort
```

Saída esperada (as oito gavetas + partições):

```
~/sisyphus-runtime
~/sisyphus-runtime/catalog
~/sisyphus-runtime/dispatches
~/sisyphus-runtime/facts
~/sisyphus-runtime/facts/_global
~/sisyphus-runtime/meta
~/sisyphus-runtime/roles
~/sisyphus-runtime/sessions
~/sisyphus-runtime/sessions/_global
~/sisyphus-runtime/state
~/sisyphus-runtime/state/archive
~/sisyphus-runtime/state/current
~/sisyphus-runtime/traces
```

---

## 🧭 Como o terceiro avalia (o que ele deveria concluir)

Dando **só** essa saída de `find` a um colega, ele deveria classificar sem pistas:

| Gaveta | Semântica | Justificativa que ele daria |
|---|---|---|
| `facts/` | acumula | memória durável, cresce |
| `state/current/` | substitui | foto única do agora |
| `state/archive/` | congela | histórico datado de estado |
| `sessions/` | apensa | um handoff por arquivo |
| `catalog/` | indexa | ponteiros para contexto omitido |
| `traces/` | registra | o que aconteceu, cru |
| `meta/` | deriva | registry não-autoritativo |
| `roles/` | define | charters estáveis |
| `dispatches/` | especifica | specs revisados |

Se ele reproduz ≥6 sem te consultar e não aponta gaveta faltante, **o esqueleto passou**.

## ❌ Erros comuns que reprovam

- `state/` sem `current`/`archive` separados → reintroduz o defeito de deriva.
- `facts/` sem `_global` → o terceiro pergunta "onde ficam os fatos que valem para tudo?".
- Repo git presente → viola a regra dura, reprova na entrega 3.
