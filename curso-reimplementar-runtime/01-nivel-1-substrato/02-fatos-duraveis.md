---
title: "Fatos duráveis: como o sistema lembra entre sessões"
type: curriculum-lesson
nivel: 1
aliases: ["fatos duráveis", "durable-fact", "schema de fato", "memória durável"]
tags: [curriculo-conteudo, nivel-1, substrato, durable-fact, facts, frontmatter, schema]
relates-to:
  - "[[vault:sisyphus-runtime/facts/_global/index|Índice de Fatos — Global]]"
  - "[[vault:sisyphus-runtime/facts/_global/constraints|Constraints Acumuladas]]"
  - "[[vault:sisyphus-runtime/facts/_global/principles|Principles Acumulados]]"
  - "[[vault:sisyphus-runtime/facts/_global/ground-truth|Ground Truth Assertions]]"
  - "[[01-layout-do-vault|Lição 01 — Layout do Vault]]"
  - "[[GLOSSARY|Glossário]]"
last_updated: 2026-08-13
---

# 🧠 Fatos duráveis: como o sistema lembra entre sessões
## O schema tipado que transforma uma sessão descartável em memória permanente

**Tempo Estimado:** 50 minutos
**Nível:** 1 — O Substrato
**Pré-requisito:** `01-layout-do-vault.md`
**Status:** 🟢 FUNDAÇÃO — sem isto, todo aprendizado do sistema evapora no fim da sessão

---

## 📖 Prólogo: a mesma verdade, escrita três vezes

Abra `facts/_global/constraints.md` e olhe as duas primeiras linhas do corpo com atenção
cirúrgica. Você vai encontrar isto, quase literalmente:

> - "Toda operacao de vault passa por obsidian-eval, nunca pelo app Obsidian CLI" (source: canonical-context skill 2026-06-15)
> - "Toda operacao de vault passa por obsidian-eval, nunca pelo app Obsidian CLI" (source: canonical-context update 2026-06-15)

A **mesma** constraint, no **mesmo** dia, apensada **duas** vezes por sessões diferentes que
não sabiam uma da outra. Nenhuma estava errada. Cada uma tinha uma boa razão para gravar aquilo
como durável. E é exatamente por isso que existe: o sistema **acumula** — não deduplica sozinho,
não confia que "alguém já anotou". Se uma verdade importa, ela é escrita, com a sua `source`, e
o disco fica com a evidência dupla em vez de com a promessa de que já estava lá.

É a mesma disciplina do [[GLOSSARY|Achado central]] do sistema, vista do outro lado: *afirmação
sobre estado não vira durável sem passar por medição*. Um fato durável é o que sobra quando a
sessão que o descobriu já morreu. Ele precisa carregar, no próprio corpo, tudo o que um estranho
precisa para confiar nele — porque quem vai lê-lo **é** um estranho: a próxima sessão, sem o seu
contexto, sem a sua memória de trabalho.

---

## 🧠 O conceito: um fato é um par (asserção, procedência) tipado no frontmatter

Um [[GLOSSARY|fato durável]] mora em `facts/` e é uma nota Markdown cujo **frontmatter** carrega
o tipo e o metadado, e cujo **corpo** carrega as asserções. O que faz dele "durável" não é onde
está — é o schema que permite recuperá-lo por predicado meses depois.

### O frontmatter tipado

O campo mestre é `type: durable-fact`. O `kind` diz *que espécie* de verdade é:

| `kind` | O que é | Exemplo real (arquivo) |
|---|---|---|
| `constraint` | uma regra dura, um "nunca/sempre" | `facts/_global/constraints.md` |
| `preference` | uma inclinação, mais fraca que constraint | `facts/_global/preferences.md` |
| `principle` | um princípio de conduta acumulado | `facts/_global/principles.md` |
| `ground-truth` | asserção imutável definida por humano | `facts/_global/ground-truth.md` |

Além do `kind`, o schema típico traz:

- **`confidence`** (`high` / `medium` / `low`) — o quanto o sistema confia neste fato. Uma
  `preference` costuma nascer `medium`; uma `constraint` de AGENTS.md nasce `high`.
- **`valid_from`** — a data a partir da qual o fato vale. É o que permite raciocínio temporal:
  um fato não é atemporal, ele **entra em vigor**.
- **`repo`** — o namespace (`_global` ou um projeto). Isola a memória por repo.
- **`last_updated`**, **`source`/`defined_by`**, **`relates-to`** — procedência e ligações.

Veja a forma canônica no cabeçalho de `facts/_global/constraints.md`
(`[[vault:sisyphus-runtime/facts/_global/constraints|Constraints Acumuladas]]`): `type:
durable-fact`, `kind: constraint`, `confidence: high`, `valid_from: 2026-06-01`.

### A procedência é obrigatória, não decorativa

Repare que **cada linha** de constraint termina com `(source: ...)`. Isso não é estilo — é o
que separa um fato durável de um boato durável. Uma constraint global do sistema é explícita:

> "Nao inventar citacoes, saidas de ferramenta ou resultados de verificacao"

Um fato sem `source` é uma asserção que ninguém pode reproduzir — exatamente a classe de defeito
que o sistema inteiro combate. O `ground-truth.md` leva isso ao extremo: é `defined_by: "human"`,
`immutable`, e cada asserção vem com o seu `rationale`. Ground-truth é o que **não se discute**;
constraint/preference/principle é o que o sistema **aprendeu** e pode reavaliar.

### Corpo: a lista, não a prosa

O corpo de um fato acumulado é uma **lista** de asserções curtas, não um ensaio. Isto é
deliberado: uma lista é recuperável e diffável; prosa não é. (No Nível 3 você verá que "prosa vs
estrutura" foi causa raiz de incidente real de gate.) Cada item é uma frase + a sua `source`.

### Como o sistema de fato "lembra"

O ciclo é: uma sessão descobre algo que vale entre sessões → apensa como fato durável (via
`obsidian-eval append-fact`, na lição 04) → a próxima sessão, ao iniciar, **recupera** os fatos
por predicado sobre o frontmatter (`type === 'durable-fact'`). A memória não é mágica: é um
diretório que acumula + uma camada de acesso que consulta. O índice `facts/_global/index.md`
(`[[vault:sisyphus-runtime/facts/_global/index|Índice de Fatos]]`) é o mapa navegável desses
fatos — mas, coerente com "o disco vence", ele é **derivado**: se o índice e os arquivos
divergirem, os arquivos ganham.

---

## 🔎 Por que esta lição é o coração do substrato

Porque "aprender entre sessões" é a promessa inteira do runtime, e ela se reduz a esta mecânica:
um schema tipado + procedência + acumulação. Tire a tipagem e você não recupera nada por
predicado. Tire a `source` e você não pode confiar. Tire o `valid_from` e você perde o tempo.
Um reimplementador que acerta o schema de `durable-fact` já tem metade do substrato de pé; quem
erra constrói um bloco de notas que esquece tudo no logout.

---

## 🧪 Exercício

**Contexto.** Você vai escrever o primeiro fato durável do seu runtime reimplementado.

1. **Classifique.** Pegue três verdades sobre o seu ambiente (ex.: "sempre uso `obsidian-eval
   query` em vez de `search`"). Para cada uma, decida o `kind`: é `constraint`, `preference`,
   `principle` ou `ground-truth`? Justifique a escolha — a fronteira constraint↔preference é a
   mais sutil.
2. **Dê procedência.** Escreva cada uma como um item de lista terminado em `(source: ...)`. Sem
   `source` reproduzível, o item não conta.
3. **Recupere.** Depois de gravar, imagine o predicado que a próxima sessão usaria para achar só
   os seus fatos de `kind: constraint`. (Você implementa isso de verdade no
   `exercises/exercise-02-primeiro-fato.md`.)

**Critério de aprovação (medição de terceiro):** outra pessoa lê o seu fato **sem o seu contexto**
e consegue (a) dizer por que ele é durável e não estado corrente, e (b) reproduzir a `source`. Se
ela não consegue rastrear a origem, o fato reprovou — independente de você achar que está claro.

> 💡 A escrita real e a recuperação com `obsidian-eval` estão no exercício 02 e na sua solução.

---

## 🔗 Para ir fundo

- Schema em uso — constraints: `[[vault:sisyphus-runtime/facts/_global/constraints|Constraints]]`
- Ground-truth imutável: `[[vault:sisyphus-runtime/facts/_global/ground-truth|Ground Truth]]`
- Principles acumulados: `[[vault:sisyphus-runtime/facts/_global/principles|Principles]]`
- Índice (derivado): `[[vault:sisyphus-runtime/facts/_global/index|Índice de Fatos]]`
- Próxima lição: `03-estado-e-handoffs.md` — a memória que *substitui* e a que *passa adiante*
