---
title: "A topologia de papéis: quem faz, quem julga, quem roteia"
type: curriculum-lesson
nivel: 2
aliases: ["topologia de papéis", "os oito papéis", "roster", "owner-of-no-role", "split-brain"]
tags: [curriculo-conteudo, nivel-2, a-maquina, roles, owner-of-no-role, split-brain, hub-and-spoke]
relates-to:
  - "[[vault:sisyphus-runtime/roles/_index|Roles — Índice e Topologia]]"
  - "[[vault:sisyphus-runtime/roles/orchestrator|Charter — Orquestrador]]"
  - "[[vault:sisyphus-runtime/roles/momus|Charter — Momus]]"
  - "[[vault:long-running-agents/docs/canonical/owner-of-no-role-design|Owner-of-No Role Design]]"
  - "[[vault:long-running-agents/docs/canonical/split-brain-planning-review|Split-Brain Planning/Review]]"
  - "[[vault:long-running-agents/docs/canonical/generator-evaluator|Generator-Evaluator]]"
last_updated: 2026-08-13
---

# 🕸️ A topologia de papéis: quem faz, quem julga, quem roteia
## Oito papéis, e por que o que coordena não é o que trabalha

**Tempo Estimado:** 45 minutos
**Nível:** 2 — A Máquina
**Pré-requisito:** `01-nivel-1-substrato/` (o substrato: vault, fatos duráveis, estado)
**Status:** 🟢 PORTA DE ENTRADA DO NÍVEL 2 — leia antes do loop

---

## 📖 Prólogo: o hub que se recusou a ajudar

Imagine a cena, porque ela acontece dezenas de vezes por dia dentro deste sistema.

Um planejador termina de redigir um dispatch e o entrega ao orquestrador. O dispatch
tem um erro pequeno, óbvio, de uma linha: uma escrita nomeada aponta para o path errado.
O orquestrador — que sabe ler, que tem o arquivo aberto na frente dele, que corrigiria
isso em três segundos — **não corrige.**

Ele não corrige porque corrigir é escrever. E escrever é o trabalho de outro papel. Se
o orquestrador emenda o dispatch, ele acabou de virar autor de um artefato que ninguém
revisou — o dele. O Momus que revisar aquele dispatch vai revisar o texto do planejador,
não a emenda silenciosa do hub. O gate teria um buraco do tamanho exato do "eu só ajeitei
uma coisinha".

Então o orquestrador faz a única coisa que o charter dele permite: devolve ao planejador
por `[handoff]` e diz *"conserte você, e reemita para nova review"*. Parece burrice. É o
oposto: é a única forma de o sistema nunca ter um artefato que escapou do gate porque quem
guarda o gate resolveu ser prestativo.

Este é o coração do Nível 2. Os papéis não estão separados por **capacidade** — todos são
a mesma família de modelo, todos sabem escrever, revisar e planejar. Estão separados por
**autoridade**. E a separação mais importante de todas é a do papel que coordena tudo e
não produz nada.

---

## 🧠 O conceito: oito papéis, três classes

O sistema é uma camada de governança sobre mensageria de sessões. Ele tem **oito papéis**,
e a forma mais honesta de os enxergar é em três classes: quem roda o ciclo (cinco sessões),
quem julga a exceção (um humano), e o que conecta todo mundo (dois contratos).

### Classe 1 — As cinco sessões que rodam o ciclo

| Papel | Vida | Fala com | O que faz |
|---|---|---|---|
| **Orquestrador** | standing, 1 por tópico | planejador, momus, executor, meta | Hub burro e mecânico. Roteia, aplica gates, spawna. Não redige, não decide fora das travas. |
| **Planejador** | standing, 1 por tópico | orquestrador | Redige o dispatch spec-first (escritas nomeadas + escopo negativo). Não executa, não aprova o próprio plano. |
| **Momus** | efêmero, 1 por review | orquestrador | Revisor adversarial. Nasce limpo, tenta derrubar um artefato, escreve o veredito, morre. |
| **Executor** | efêmero, 1 por dispatch | orquestrador | Materializa **só** as escritas nomeadas. Divergiu do plano → `[blocker]`. Morre ao terminar. |
| **Meta** | standing, 1 global | orquestradores, operador | Painel + roteador fino. Registro de tópicos + inbox único de escalação. **Não aprova dispatch.** |

Duas distinções de **vida** carregam metade do design:

- **Standing** (orquestrador, planejador, meta) — persistem porque **acumulam memória**. Um
  planejador que renasce a cada dispatch replaneja do zero e repete erros já aprendidos.
- **Efêmero** (momus, executor) — nascem, fazem uma coisa, morrem. A efemeridade não é
  economia: é **higiene**. Um Momus reutilizado lê o v2 pelas lentes do v1 e converge para
  aprovação por familiaridade. A independência vem de *nascer limpo*, não de disciplina.

### Classe 2 — O juiz de exceção

O **operador humano** é o oitavo papel — e não aparece na tabela de sessões porque **não
é uma sessão**. Ele é o **juiz de exceção**: só entra quando um gate dispara uma
`[escalation]`. O sistema mecanizou o relé humano (o `SendMessage` faz o que antes um
humano fazia à mão, mensagem por mensagem); o operador só é chamado quando a lista de
escalação bate. Colocá-lo em qualquer outro ponto do fluxo recria o gargalo que o sistema
inteiro existe para remover.

### Classe 3 — Os dois contratos que conectam todos

Estes dois não são sessões que agem — são as **regras que todos os outros falam**. Sem eles,
os cinco papéis seriam cinco processos que não sabem se endereçar:

- **`protocol`** — o contrato de mensagem: envelope fixo, vocabulário fechado de sete `TYPE`,
  e o princípio **mensagem = sinal, arquivo = verdade** (o payload nunca vai no corpo; a
  mensagem é ponteiro para um arquivo no vault).
- **`launch-convention`** — como uma sessão nasce e se nomeia. O nome (`<topic>-<role>[-<n>]`)
  **é o endereço** do `SendMessage`; efêmeros levam sufixo numérico **sempre**, porque a
  colisão perigosa é sequencial — um executor que morreu e outro que nasceu dez minutos
  depois com o mesmo nome herdaria mensagens que não eram dele.

> Nota de contagem: os oito mapeiam os oito charters em `roles/` — trocando o `_index`
> (que é o mapa, não um papel) pelo operador (que é papel, mas não é charter porque não é
> sessão). Cinco sessões + um juiz + dois contratos.

---

## 🎯 A topologia: hub-and-spoke por tópico

Os papéis não formam uma malha onde todos falam com todos. Formam uma **estrela**, com o
orquestrador no centro:

```
                    ┌────────────────────┐
                    │        META         │   (global, 1 instância)
                    │  registry + inbox   │
                    └──────────┬──────────┘
                   [escalation]↑   ↓[directive]
                    ┌──────────┴──────────┐
                    │    ORQUESTRADOR     │   (standing, 1 por tópico)
                    │   — o HUB burro —   │
                    └──────────┬──────────┘
          ┌──────────┬─────────┼─────────┬──────────┐
          │          │         │         │          │
     ┌────▼────┐ ┌───▼───┐ ┌───▼────┐ ┌──▼─────┐
     │PLANEJADOR│ │ MOMUS │ │EXECUTOR│ │ MOMUS  │
     │(standing)│ │entrada│ │(efêmero)│ │ saída  │
     └─────────┘ └───────┘ └────────┘ └────────┘
                  efêmero    efêmero    efêmero
```

Uma regra dura governa esse desenho: **os spokes nunca falam entre si.** O planejador não
fala com o executor. O Momus não fala com o planejador. Toda mensagem passa pelo hub.

Isso é deliberado, e é a razão de o desenho ser estrela e não malha: **o hub é o único
ponto onde os gates são aplicados.** Um caminho lateral — o planejador entregando o dispatch
direto ao executor, "para ganhar tempo" — seria um gate contornado. A topologia não é uma
escolha de conveniência; é a materialização física da regra "nada passa sem gate".

---

## 🧩 Os dois padrões que você precisa levar deste nível

Dois nomes canônicos explicam por que a topologia tem a forma que tem. Se você reimplementar
o runtime, são estes dois que você não pode errar.

### Owner-of-no-role: o orquestrador não faz o trabalho

O orquestrador **não possui nenhum papel de execução**. Ele não redige (isso é do planejador),
não revisa (isso é do Momus), não materializa artefato (isso é do executor). O valor dele é
**rotear e aplicar o gate** — não fazer o trabalho.

Isso parece desperdício até você ver a falha que evita. Um coordenador que *também* produz
tem um conflito de interesse estrutural: ele é, ao mesmo tempo, o autor de um artefato e o
guardião do gate que aquele artefato tem de passar. No instante em que o hub escreve uma
linha, ele vira parte auditada — e não existe mais ninguém acima dele para auditar. O
`owner-of-no-role-design` é a regra de que **quem guarda o gate não pode ter pele no
resultado que o gate julga.**

Por isso o prólogo: o hub que se recusa a corrigir o typo não é burro por acidente. Ele é
**burro por projeto** — "esperteza no gate é risco". Um autômato que checa condições
verificáveis em disco e executa ações de uma tabela é auditável; um hub que pondera "nesse
caso dá pra seguir" é um gate que varia com o humor.

### Split-brain: quem constrói não é quem julga

O planejador e o Momus são **cabeças separadas**, e essa separação é o segundo pilar. O
planejador **gera** o plano; o Momus **avalia** o plano. Nunca a mesma sessão faz as duas
coisas.

A razão é o modo de falha que o `split-brain-planning-review` (e sua encarnação
`generator-evaluator`) existe para bloquear: **se o construtor pode declarar que foi
avaliado, o split-brain colapsa.** Ele vira avaliador de si mesmo com uma frase — e um
avaliador que aprova o próprio trabalho não é um avaliador, é um carimbo. O planejador é
explicitamente proibido de aprovar o próprio plano; a auto-aprovação é justamente o gargalo
que este sistema existe para remover, e removê-lo por auto-indulgência é pior que mantê-lo.

O Momus leva a separação ao extremo: ele nasce **sem o contexto** da sessão que o spawnou.
A entrada dele é o artefato, o dispatch, os charters e as regras — nada da conversa que
produziu o plano. Ele não pergunta ao planejador "o que você quis dizer"; se o dispatch
precisa de esclarecimento oral, ele está ambíguo, e **ambiguidade é um achado, não um
obstáculo**.

> ⚠️ O split-brain tem uma cicatriz real com nome e data: um review que foi *declarado*
> feito sem ter sido feito, numa frase de aprovação colada com data. A lição inteira está
> no Nível 3 (`case-studies/caso-momus-skip.md`). Por ora, guarde a forma: **quem constrói
> não assina o próprio veredito.**

---

## 🧪 Exercício: mapeie os papéis e ache o buraco

**Contexto.** Você tem o vault à mão. Nada de escrita — leitura dos charters e raciocínio.

1. **Roster em suas palavras.** Leia `roles/_index.md` §1 e §2. Preencha uma tabela de cinco
   linhas (as cinco sessões) com três colunas: *vida* (standing/efêmero), *com quem fala*, e
   *uma frase do que faz*. Para cada efêmero, escreva **por que** ele é efêmero.

2. **Ache a violação de owner-of-no-role.** Aqui estão quatro situações. Em **duas** delas o
   orquestrador está fazendo algo que o charter dele proíbe. Ache as duas e diga qual regra
   quebram:
   - (a) O orquestrador recebe um `handoff` e spawna o Momus-entrada.
   - (b) O orquestrador vê um typo no dispatch e o corrige antes de spawnar o Momus.
   - (c) O orquestrador lê o veredito PASS em disco e spawna o executor.
   - (d) O veredito não existe em disco, mas a mensagem do Momus disse "PASS", e o
     orquestrador spawna o executor mesmo assim.

3. **Ache a violação de split-brain.** Uma sessão redige um dispatch, o executa, e cola no
   relatório "plano auto-revisado, sem achados". Qual é exatamente a fronteira que ela
   cruzou, e qual papel deveria ter feito a revisão?

4. **Por que a estrela?** Em duas frases: o que aconteceria com os gates se o planejador
   pudesse entregar o dispatch direto ao executor, sem passar pelo hub?

**Critério de aprovação (medição de terceiro):** seu mapa e suas respostas só "passam"
quando **outra pessoa** (ou outra sessão) lê os charters em `roles/` e confirma que a sua
tabela bate, que as duas violações do passo 2 são (b) e (d), e que a fronteira do passo 3 é
o `split-brain`. Você não aprova o próprio mapa — coerente com o achado central do sistema.

---

## 🔗 Para ir fundo

- O roster e a topologia, na fonte: `[[vault:sisyphus-runtime/roles/_index|Roles — Índice e Topologia]]`
- O hub burro por projeto: `[[vault:sisyphus-runtime/roles/orchestrator|Charter — Orquestrador]]`
- O adversário efêmero: `[[vault:sisyphus-runtime/roles/momus|Charter — Momus]]`
- Padrão canônico — o coordenador que não trabalha: `[[vault:long-running-agents/docs/canonical/owner-of-no-role-design|Owner-of-No Role Design]]`
- Padrão canônico — construtor ≠ avaliador: `[[vault:long-running-agents/docs/canonical/split-brain-planning-review|Split-Brain Planning/Review]]`
- Próxima lição: `02-o-loop-dispatch-gate.md` — como esses papéis, juntos, fecham um ciclo.
