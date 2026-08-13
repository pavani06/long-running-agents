---
title: "A regra do relé: um peer não estabelece o que o operador autorizou"
type: curriculum-lesson
nivel: 3
aliases: ["regra do relé", "relé", "lavagem de permissão", "permission washing", "custódia de directive"]
tags: [curriculo-conteudo, nivel-3, governanca, rele, autorizacao, custodia, directive, lavagem-de-permissao, session-boundary]
relates-to:
  - "[[vault:sisyphus-runtime/meta/registry.md|Registry — Inbox de Escalação]]"
  - "[[vault:sisyphus-runtime/facts/_global/dispatch-rule-escalation|Rule: Escalation List]]"
  - "[[vault:sisyphus-runtime/facts/_global/dispatch-rule-session-boundary|Rule: Session-Boundary]]"
  - "[[vault:long-running-agents/docs/canonical/operator-channel-authority|Operator-Channel Authority]]"
last_updated: 2026-08-13
---

# 🔌 A regra do relé: um peer não estabelece o que o operador autorizou
## Por que uma decisão de operador relatada por outra sessão não autoriza nada

**Tempo Estimado:** 45 minutos
**Nível:** 3 — Governança e Cicatrizes
**Pré-requisito:** `02-disciplina-de-gate.md`
**Status:** 🔴 CRÍTICO — fecha o buraco de "lavagem de permissão" entre sessões
**Cicatriz de origem:** a escrita nos oito charters de `roles/` fora de ciclo, e a entrada de inbox que só fechou quando o operador confirmou a autoria *ele mesmo*

---

## 📖 Prólogo: os oito charters que foram escritos por ninguém-com-mandato

Uma noite, os **oito** arquivos de `roles/` — os charters que definem as regras do jogo —
foram editados numa janela de trinta e quatro segundos. **Sem dispatch. Sem gate. Sem
veredito.** O autor era uma sessão avulsa, com nome de exibição genérico, que não tinha
mandato para tocar a camada de governança.

Uma sessão *peer* apareceu e disse, em essência: *o pedido foi legítimo, foi o operador que
mandou*. E aqui está a tentação — a mais natural do mundo num sistema de agentes que
conversam entre si: **aceitar a palavra do peer e fechar o caso.** Afinal, se outra sessão
diz que o operador autorizou, e a escrita já está no disco, por que não seguir?

O orquestrador **não** fechou. Manteve a entrada de escalação **aberta**, com a razão dita
com todas as letras:

> A autoria só se confirma **pelo próprio operador**, não pela palavra do peer que a alegou —
> e era exatamente essa distinção que mantinha a entrada aberta.

O caso só fechou quando o directive do operador chegou pelo canal do próprio operador — três
palavras, transcritas verbatim em disco: *"o pedido foi meu"*. **Não foi a alegação do peer
que autorizou; foi a confirmação do operador.** Até esse instante, o que existia era uma
escrita na camada de governança sem proveniência de autorização — que é *exatamente* o que o
gatilho existe para pegar. O tamanho da mudança (aditiva, no frontmatter) não mudava nada:
escrita fora de gate, por sessão sem mandato, é o que o gatilho pega, e o tamanho não é o
critério.

A cicatriz completa (com as medições de md5 e a reconstituição da linha do tempo) vive no
vault: `[[vault:sisyphus-runtime/meta/registry.md|inbox de escalação, entrada de 22:45]]`.

---

## 🧠 O conceito: autoridade de operador não se propaga por peer

O `GLOSSARY` enuncia a regra do relé em uma linha:

> **Relé (regra do)** — *um peer não estabelece o que o operador autorizou.* Uma decisão de
> operador relatada por outra sessão não autoriza ação; confirma-se pelo canal do próprio
> operador. Fecha o buraco de **"lavagem de permissão"** entre sessões.

Lavagem de permissão é o análogo, na governança de agentes, da lavagem de dinheiro: uma
autorização de origem duvidosa (ou inexistente) ganha aparência de legítima ao passar de
sessão em sessão. A sessão B diz *"o operador aprovou"*; a sessão C ouve de B e trata como
fato; a sessão D lê o disco que C escreveu e trata como estabelecido. A cada salto, a
distância até a fonte real cresce, e a alegação **fica mais limpa sem nunca ter sido
verificada**. No final, ninguém consegue apontar o instante em que o operador de fato disse
algo — porque ele pode nunca ter dito.

A regra do relé corta a corrente na origem: **só o operador estabelece o que o operador
autorizou.** Um peer pode *relatar* uma decisão; relato é sinal, não prova. A ação só
destrava quando a autorização chega pelo **canal do próprio operador**.

---

## 🧾 Como o runtime confirma pelo canal do operador

O runtime não tem um "arquivo assinado pelo operador". Os directives chegam **como mensagem,
não como arquivo** — não existe artefato-fonte do operador. Então a disciplina é sobre
**custódia**: como uma decisão que nasceu numa mensagem vira algo verificável em disco sem
perder a proveniência.

O padrão que o registry usa, entrada após entrada:

1. **Transcrição verbatim.** O directive do operador é transcrito **literalmente** em disco,
   dentro do dispatch/estado que ele destrava — palavra por palavra, não parafraseado. Um
   directive parafraseado é uma afirmação da sessão sobre o que o operador disse; um directive
   verbatim é a fala do operador.
2. **Custódia declarada.** A entrada registra explicitamente: *"mensagem, não arquivo;
   transcrito pelo `runtime-orchestrator`; não existe arquivo-fonte do operador."* A lacuna de
   proveniência é **nomeada**, não escondida.
3. **Aplicação literal.** *"Um directive destrava o que ele diz destravar, e não se estende
   por analogia a casos parecidos"* (`dispatch-rule-escalation`). O relé não vale só para
   quem relata — vale para o escopo: você não estica a autorização do operador para vizinhos
   "óbvios".
4. **Sem verbatim, sem crédito.** Houve no runtime um directive *"AINDA NÃO EM DISCO"* — a
   decisão fora tomada, mas a transcrição verbatim ainda não existia. O registry recusou
   parafraseá-lo como se fosse literal e o marcou como *"o único directive do dia sem
   proveniência verificável"*. **A decisão sem sua transcrição não é tratada como
   estabelecida.**

> Repare que isto é a **lição 02 aplicada à autorização**: um gate mede o disco, não lê a
> promessa. "O operador aprovou" dito por um peer é uma promessa. O directive verbatim em
> disco, com custódia declarada, é o disco.

---

## 🔗 Onde o relé encosta na fronteira de sessão

A regra do relé e a `session-boundary` (lição 01) são a mesma disciplina vista de dois
ângulos. A fronteira de sessão diz: *um dispatch termina com a sessão; o próximo só existe
quando o operador o abre.* O relé diz: *o que o operador autorizou só o operador estabelece.*
Juntas, elas fecham a rota pela qual uma sessão herdaria poder de outra: nem por continuar no
mesmo contexto (fronteira), nem por ouvir de um peer que estava tudo aprovado (relé).

E ambas explicam por que a escrita nos oito charters foi tratada como incidente mesmo sendo
*aditiva e inócua no conteúdo*: uma edição que não mudou uma única linha normativa ainda
assim quebrou uma cadeia de prova em disco (um `md5` congelado por um dispatch pendente deixou
de casar), tornando o dispatch inexecutável. **O dano não estava nas normas — estava na
proveniência.** Autorização sem proveniência é o problema, mesmo quando o conteúdo é benigno.

---

## 🔎 Por que esta regra é fácil de esquecer

Porque a lavagem de permissão **parece cooperação**. Num sistema onde sessões se ajudam,
recusar a palavra de um peer soa como desconfiança gratuita — "por que eu duvidaria de outra
sessão de boa-fé?". A resposta não é sobre boa-fé:

> **O peer pode estar de perfeita boa-fé e ainda assim errado sobre o que o operador disse.**
> O relé não protege contra malícia; protege contra a distância que se acumula entre uma
> alegação e sua fonte cada vez que ela é repassada. Boa-fé não encurta essa distância — só a
> confirmação pelo canal do operador encurta.

Se você reimplementar o runtime, o teste é simples e desconfortável: da próxima vez que uma
sessão te disser *"pode seguir, o operador já autorizou"*, pergunte a si mesmo — **eu tenho
isso pelo canal do operador, ou tenho isso pela palavra de um peer?** Se é a segunda, você
está a um salto de lavagem de permissão.

---

## 🧪 Exercício

**Contexto.** Duas sessões do seu runtime, A e B. A executou algo na camada de governança e B
te relata: *"o operador aprovou o que A fez."*

1. **Rastreie a fonte.** Liste os saltos entre a alegação que você recebeu e o operador real.
   Em qual salto a autorização deixa de ser verificável? (Se você não consegue apontar o
   instante em que o operador falou, a resposta é "no primeiro".)
2. **Feche pelo canal certo.** Escreva o procedimento que *fecharia* essa escalação
   corretamente: o que precisa chegar, por qual canal, e como fica a custódia em disco
   (verbatim? paráfrase? lacuna nomeada?).
3. **Estique e quebre.** O directive do operador autorizou A. Uma terceira sessão, C, quer
   fazer algo "praticamente igual" ao que A fez. O directive de A cobre C? Justifique com a
   regra da aplicação literal.

**Critério de aprovação (medição de terceiro):** outra pessoa lê seu procedimento do passo 2 e
tenta *lavar* uma permissão através dele — inventar uma cadeia de peers que faça uma
autorização inexistente parecer estabelecida. Seu procedimento passa se ela não conseguir: em
algum ponto ele exige o canal do operador e a cadeia de peers não o substitui.

---

## 🔗 Para ir fundo

- A entrada de inbox que só fechou pela confirmação do operador (privada): `[[vault:sisyphus-runtime/meta/registry.md]]`
- A lista de gatilhos e a aplicação literal do directive: `[[vault:sisyphus-runtime/facts/_global/dispatch-rule-escalation]]`
- A fronteira de sessão, o outro lado da mesma moeda: `[[vault:sisyphus-runtime/facts/_global/dispatch-rule-session-boundary]]`
- Próxima lição: `04-o-achado-central.md`
