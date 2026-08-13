---
title: "O layout do vault: onde o sistema guarda cada coisa e por quê"
type: curriculum-lesson
nivel: 1
aliases: ["layout do vault", "topologia do runtime", "árvore de diretórios do vault", "vault layout"]
tags: [curriculo-conteudo, nivel-1, substrato, vault, topologia, obsidian-eval]
relates-to:
  - "[[vault:sisyphus-runtime/_moc-runtime|MOC: Sisyphus Runtime]]"
  - "[[vault:sisyphus-runtime/README|README do Runtime]]"
  - "[[vault:sisyphus-runtime/MANIFEST|Manifest do Vault]]"
  - "[[GLOSSARY|Glossário]]"
last_updated: 2026-08-13
---

# 🗂️ O layout do vault: onde o sistema guarda cada coisa e por quê
## A topologia da camada de dados — o mapa antes do território

**Tempo Estimado:** 45 minutos
**Nível:** 1 — O Substrato
**Pré-requisito:** Nível 0 (Orientação) — você já sabe o que é o loop e o que é o runtime
**Status:** 🟢 FUNDAÇÃO — nada no Nível 1 faz sentido sem este mapa

---

## 📖 Prólogo: o dia em que o `state/current/` mentiu por 18 dias

Numa sessão de 10 de agosto, alguém abriu o `state/current/` para retomar o trabalho e leu
um objetivo que já não existia. O arquivo dizia uma coisa; o mundo tinha andado. A anotação
de working-memory da própria sessão registra o diagnóstico, seco:

> `state/current/ anterior era de 23/07 (stale), arquivado em state/archive/2026-07-23/`

Dezoito dias de deriva. O estado corrente tinha virado estado *passado* sem ninguém mover.
Ninguém apagou nada, ninguém corrompeu arquivo — o `state/current/` simplesmente **não é um
lugar onde se acumula**; é um lugar que se **substitui**. Quem tratou `current` como se fosse
`archive` acabou lendo uma foto velha como se fosse a janela.

A lição não é sobre um bug. É sobre a coisa mais básica que um reimplementador precisa saber
antes de escrever a primeira nota: **cada diretório do vault tem uma semântica**, e usar o
diretório errado não dá erro — dá uma mentira silenciosa que só aparece dias depois. Você não
pode reconstruir o substrato sem saber o que cada gaveta guarda e, principalmente, o que ela
**recusa** guardar.

---

## 🧠 O conceito: oito gavetas, cada uma com uma promessa

O `sisyphus-runtime` é um [[GLOSSARY|vault]]: um diretório de notas Markdown com frontmatter
YAML, lido e escrito por [[GLOSSARY|obsidian-eval]] e **nunca** pelo app Obsidian. Rode você
mesmo, na máquina que tem o vault:

```bash
find ~/sisyphus-runtime -maxdepth 1 -type d
```

O ponto de entrada canônico é o `_moc-runtime.md` — o MOC (Map of Content) que lista os entry
points e a topologia. Aponte para ele sempre que se perder:
`[[vault:sisyphus-runtime/_moc-runtime|MOC: Sisyphus Runtime]]`.

As gavetas de primeiro nível, e a promessa de cada uma:

| Diretório | O que guarda | Semântica (a promessa) |
|---|---|---|
| `facts/` | [[GLOSSARY|fatos duráveis]] — constraints, preferences, principles, ground-truth, baselines | **Acumula.** É a memória entre sessões. Cresce; raramente encolhe. |
| `state/current/` | objetivo, working-memory, decisões abertas, repo corrente | **Substitui.** Foto do *agora*. Uma versão só. Vira `state/archive/` ao rotacionar. |
| `state/archive/` | fotos antigas de `current/`, datadas | **Congela.** Histórico de estado, nunca reescrito. |
| `sessions/` | [[GLOSSARY|payloads de handoff]] entre sessões, por repo | **Apensa.** Um arquivo por handoff; namespaced por repo (`sessions/<repo>/`). |
| `catalog/` | catálogo de contexto omitido (memória endereçável) | **Indexa.** Ponteiros para conteúdo grande que ficou de fora do contexto. |
| `traces/` | traços de sessão e prompts verbatim | **Registra.** O que de fato aconteceu, cru — inclui request do operador. |
| `meta/` | o `registry.md` da meta-camada | **Deriva.** Estado operacional; **não-autoritativo** (o disco vence). |
| `roles/` | os [[GLOSSARY|charters]] dos papéis (orchestrator, planner, momus, executor, meta, protocol) | **Define.** Quem faz o quê no loop. Estável. |
| `dispatches/` | os [[GLOSSARY|dispatches]]: specs revisados antes de executar, por repo | **Especifica.** A unidade de trabalho, com pré-condições e gates. |

### As três semânticas que você não pode confundir

Tudo acima colapsa em três verbos. Errar o verbo é o defeito do prólogo:

1. **Acumula** (`facts/`, `sessions/`): você *apensa*. O passado permanece. Apagar aqui é
   perder memória.
2. **Substitui** (`state/current/`): existe **uma** versão. Escrever aqui é sobrescrever. Se
   você quer o histórico, ele vai para `state/archive/` — não para cá.
3. **Deriva** (`meta/registry.md`, índices): é resumo do que os arquivos-fonte dizem. Quando
   diverge da fonte, **os arquivos são a verdade** — o princípio [[GLOSSARY|O disco vence]].
   O `registry.md` é abrigo, não autoridade.

### Namespacing por repo

`facts/`, `sessions/`, `state/` e `dispatches/` são particionados por repo. Há sempre o
`_global` (fatos e handoffs que valem para o sistema todo) e um subdiretório por projeto
(`sessions/long-running-agents/`, `state/runtime/`, etc.). Isso mantém a memória de um repo
sem contaminar a de outro. O `_global` é o denominador comum.

### Por que privado, por que sem git

O vault **nunca vira repositório git** — o `README` do runtime é explícito: contém requests
verbatim (em `traces/`) e decisões pendentes (em `state/`) que não podem ser expostos. Backup
se faz com `tar` ou snapshot de filesystem, nunca `git init`. Guarde isso: é a razão pela qual
o curso **aponta, não copia** — o conteúdo real mora só na máquina que tem o vault.

---

## 🔎 Por que esta é a primeira lição do Nível 1

Porque a topologia é um contrato, e contratos silenciosos são os que mais machucam. Um `state/`
tratado como `archive` mente por 18 dias. Um fato escrito em `traces/` some da memória durável.
Um handoff escrito em `state/current/` é sobrescrito no próximo turno. Nenhum desses erros
levanta exceção — todos levantam **deriva**. Aprender o mapa é aprender a não cavar a própria
armadilha.

Nas próximas três lições descemos em cada gaveta crítica: `facts/` (lição 02), `state/` +
`sessions/` (lição 03) e a camada de acesso `obsidian-eval` que toca todas elas (lição 04).

---

## 🧪 Exercício

**Contexto.** Você tem acesso ao vault real (ou a uma cópia dele) numa máquina.

1. **Mapeie o território.** Rode `find ~/sisyphus-runtime -maxdepth 2 -type d` e, para cada
   diretório de primeiro nível, escreva numa frase a sua semântica: *acumula*, *substitui* ou
   *deriva*.
2. **Ache a partição.** Liste os subdiretórios de `sessions/`. Quantos repos têm namespace
   próprio? Qual é o papel do `_global`?
3. **Prove o prólogo.** Abra `state/current/objective.md` e `state/archive/` (o mais recente).
   Sem editar nada, explique como um leitor confundiria um pelo outro — e qual campo do
   frontmatter (`last_updated`) o teria salvado.

**Critério de aprovação (medição de terceiro):** seu mapa só "passa" quando outra pessoa pega
a sua tabela de semânticas e, sem ver a sua, reproduz a classificação de pelo menos 6 das 8
gavetas. Você não aprova o próprio mapa.

> 💡 O esqueleto vazio dessa árvore você constrói no `exercises/exercise-01-skeleton.md`.

---

## 🔗 Para ir fundo

- Ponto de entrada e topologia: `[[vault:sisyphus-runtime/_moc-runtime|MOC: Sisyphus Runtime]]`
- Por que sem git / como usar: `[[vault:sisyphus-runtime/README|README do Runtime]]`
- O que o vault exporta/importa: `[[vault:sisyphus-runtime/MANIFEST|Manifest]]`
- Próxima lição: `02-fatos-duraveis.md` — a gaveta que *acumula*
