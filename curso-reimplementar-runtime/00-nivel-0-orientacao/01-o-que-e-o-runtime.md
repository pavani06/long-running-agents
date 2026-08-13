---
title: "O que você vai reconstruir"
type: curriculum-lesson
nivel: 0
aliases: ["o que é o runtime", "backplane operacional", "materialização dos padrões", "prime directives"]
tags: [curriculo-conteudo, nivel-0, orientacao, sisyphus-runtime, backplane, prime-directives]
relates-to:
  - "[[vault:sisyphus-runtime/README|README do Runtime]]"
  - "[[vault:sisyphus-runtime/_moc-runtime|MOC — Sisyphus Runtime]]"
  - "[[vault:sisyphus-runtime/roles/_index|Roles — Índice e Topologia]]"
  - "[[vault:long-running-agents/docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent Operating System]]"
  - "[[vault:long-running-agents/docs/canonical/external-state-persistence|External State Persistence]]"
last_updated: 2026-08-13
---

# 🧭 O que você vai reconstruir
## O runtime não é uma pasta de arquivos — é um procedimento que virou arquivos

**Tempo Estimado:** 15 minutos
**Nível:** 0 — Orientação
**Pré-requisito:** nenhum
**Status:** 🟢 PONTO DE PARTIDA — leia antes de qualquer outra lição

---

## 📖 Prólogo: a herança sem manual

Você acaba de receber acesso a uma máquina. Nela, um diretório: `sisyphus-runtime`.
Dentro dele, centenas de notas em Markdown — `roles/`, `facts/`, `dispatches/`,
`sessions/`, `state/`, `meta/`. Nenhuma delas se apresenta. Não há `SETUP.md` que
diga "rode isto e o sistema sobe", porque **não há nada para subir**: não é um serviço,
não há processo escutando uma porta.

A pessoa (ou a sessão) que operava isto não está mais aqui. O que ficou é o rastro que
o sistema deixou de si mesmo enquanto trabalhava. Você abre um arquivo em `sessions/` e
lê um handoff endereçado a "a próxima sessão" — que agora é você. Abre um em `facts/` e
encontra uma asserção datada, com `confidence`, como se alguém tivesse deixado um bilhete
para o futuro dizendo "isto aqui é verdade, não re-descubra".

O instinto é o errado: copiar a pasta inteira para a sua máquina e declarar "reimplementado".
Você vai ver, ao longo do curso, por que isso reproduz os arquivos mas **não** reproduz o
sistema. Por ora, fique com a pergunta certa: *o que este diretório está tentando ser?*

---

## 🧠 O conceito: backplane operacional, materialização de padrões

O `sisyphus-runtime` é o **backplane operacional** do sistema de agentes Sisyphus. Não é
o app, não é o modelo. É o vault privado onde o sistema **persiste o que precisa lembrar
entre sessões** — porque uma sessão de agente morre, e sem um lugar durável fora dela, todo
o trabalho morreria junto.

Quatro coisas vivem aqui, e vale gravá-las porque o exercício vai atrás de cada uma:

1. **Handoffs** (`sessions/`) — o bastão passado de uma sessão para a próxima. Payload
   budget-aware: o suficiente para retomar sem reler tudo.
2. **Fatos duráveis** (`facts/`) — asserções acumuladas com frontmatter tipado
   (`type: durable-fact`): constraints, preferences, principles, baselines. É como o
   sistema lembra entre sessões.
3. **Estado corrente** (`state/`) — o que está em execução agora, entre turnos.
4. **Catálogo / meta** (`meta/`, `_moc-runtime.md`) — memória endereçável e o painel vivo
   da meta-camada (o `registry.md`).

A frase-chave: **o runtime é a materialização dos padrões canônicos.** Os padrões — o
desenho de como um sistema de agentes de longa duração deve operar — vivem em *outro* vault
(`long-running-agents/docs/canonical/`). O `sisyphus-runtime` é **uma** implementação
conforme daqueles padrões. Os charters em `roles/` apontam explicitamente para a sua
linhagem canônica (ver o `relates-to` de qualquer um deles). Reimplementar não é inventar
um sistema novo: é materializar os mesmos padrões, de novo, corretamente.

### Os prime directives

Quatro regras de autoridade que valem antes de qualquer código. Elas não são preferências;
são as condições sob as quais o vault existe:

- **Nunca git.** Este diretório **nunca** vira repositório git. Ele contém requests verbatim
  e decisões pendentes que não podem ser expostas em repo. Backup, se preciso, é `tar` ou
  snapshot de filesystem — nunca `git init`.
- **Local-por-máquina.** O vault mora no `home` (`~`), privado no Linux/WSL. Não há sync,
  não há repositório central. Isso é design, não limitação temporária — e tem consequência
  dura na topologia (um tópico é ancorado à máquina cujo vault guarda seu estado).
- **O disco vence.** Quando um resumo, índice ou registro diverge do que está nos arquivos,
  **os arquivos são a verdade**, e a divergência é anomalia a escalar. O `registry.md` é
  derivado e operacional — abrigo, não autoridade.
- **Acesso via `obsidian-eval`, nunca pelo app.** O vault é lido e escrito conceitualmente
  pela camada `obsidian-eval` (prefira `query` sobre frontmatter a `search` de texto).
  Abrir no app Obsidian é para humano olhar, não é a interface do sistema.

### Copiar o vault ≠ reimplementar o runtime

Aqui está a tese do curso inteiro, em uma linha: **copiar a pasta reproduz os arquivos;
reimplementar reconstrói o procedimento que os produziu.**

Um vault copiado é um retrato morto de um estado. Ele não tem o **loop** que gera artefatos
(`dispatch → review → gate → execução efêmera → verify → registry`), não tem os **papéis**
que rodam esse loop, e — o mais fácil de perder — não tem a **disciplina de gate** que
impede o sistema de mentir para si mesmo. Reimplementar é reconstruir essas três coisas.
Os arquivos são o sedimento; o curso ensina o rio.

---

## 🧪 Exercício: onde vive cada coisa?

**Contexto.** Você tem o vault existente à mão e quer construir o mapa mental antes de
qualquer coisa. Nada de escrita — só leitura, via `obsidian-eval`.

Para cada uma das quatro coisas, rode um comando de leitura e anote **o path onde ela mora**
e **um exemplo concreto** que você encontrou:

1. **Handoffs.** Liste os handoffs de sessão e ache o mais recente:
   ```bash
   obsidian-eval ~/sisyphus-runtime query "filter(n => n.frontmatter.type === 'session-handoff')"
   ```
   Em que diretório eles caem? Qual o de maior data?

2. **Fatos duráveis.** Liste os fatos e separe por `kind`:
   ```bash
   obsidian-eval ~/sisyphus-runtime query "filter(n => n.frontmatter.type === 'durable-fact')"
   ```
   Quantos são `constraint`? Quantos `principle`?

3. **Estado corrente.** Faça um scan e localize `state/current/`:
   ```bash
   obsidian-eval ~/sisyphus-runtime scan
   ```
   O que há em `state/current/execution-graph` e `state/current/relevance-log`?

4. **Catálogo / meta.** Abra os pontos de entrada — o `_moc-runtime.md` e o
   `meta/registry.md` — e liste os tópicos vivos e a inbox de escalação.

**Produto do exercício:** uma tabela de 4 linhas (coisa → path → exemplo). Guarde-a: ela é
o esqueleto que você vai *reconstruir* no Nível 4.

**Critério de aprovação (medição de terceiro):** seu mapa só "passa" quando outra pessoa
(ou outra sessão) roda os mesmos quatro comandos e confirma que os paths e exemplos que você
anotou batem com o disco. Você não aprova o próprio mapa — coerente com o achado central do
sistema, afirmação sobre estado não vira durável sem passar por medição de terceiro.

---

## 🔗 Para ir fundo

- README do runtime (os prime directives, na fonte): `[[vault:sisyphus-runtime/README|README do Runtime]]`
- Mapa de navegação do vault: `[[vault:sisyphus-runtime/_moc-runtime|MOC — Sisyphus Runtime]]`
- Os papéis que rodam o loop (próximo passo): `[[vault:sisyphus-runtime/roles/_index|Roles — Índice e Topologia]]`
- Padrão canônico que o runtime materializa: `[[vault:long-running-agents/docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent Operating System]]`
- Próxima lição: `02-o-loop-em-uma-tela.md` — o loop inteiro numa só tela.
