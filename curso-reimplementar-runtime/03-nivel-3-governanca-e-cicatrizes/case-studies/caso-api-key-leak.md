---
title: "Vazamento de credencial: o output que vira artefato contaminado"
type: curriculum-casestudy
nivel: 3
aliases: ["caso api key leak", "vazamento de credencial", "secret redaction", "confidencialidade por conteúdo", "artefato contaminado"]
tags: [curriculo-conteudo, nivel-3, governanca, case-study, confidentiality, secret-redaction, security, subagente, artefato-contaminado]
relates-to:
  - "[[vault:sisyphus-runtime/facts/_global/incident-2026-07-23-deepseek-api-key-leak|Incident: API key leak]]"
  - "[[vault:sisyphus-runtime/facts/_global/dispatch-rule-confidentiality|Rule: Confidentiality]]"
  - "[[vault:sisyphus-runtime/facts/_global/dispatch-rule-post-exec-gate|Rule: Post-Exec Gate]]"
  - "[[vault:long-running-agents/docs/canonical/regulated-data-boundary|Regulated Data Boundary]]"
last_updated: 2026-08-13
---

# 🔑 Caso: vazamento de credencial — o output que vira artefato contaminado
## Como o runtime trata segredos, e por que a pasta nunca é a fronteira

**Tempo Estimado:** 40 minutos
**Nível:** 3 — Governança e Cicatrizes
**Pré-requisito:** `01-a-familia-de-regras.md`
**Status:** 🔴 P0 — este incidente permanece OPEN no vault, por decisão registrada do operador
**Cicatriz de origem:** `incident-2026-07-23-deepseek-api-key-leak` (severity P0; classe security / subclasse secret-leak)

---

## 📖 Prólogo: a chave que apareceu três vezes num export que ninguém checou

Durante a **revisão adversarial** de um plano — o momento em que uma sessão vasculha o
trabalho de outra atrás de defeitos — um subagente de investigação forense fez o que
subagentes de investigação fazem: imprimiu o que encontrou. Só que o que ele encontrou, e
imprimiu **em texto plano no output**, era o valor integral de uma **chave de API** de
produção.

O valor apareceu **três vezes** no export daquela sessão. E o export não ficou parado: ele
**transitou por Downloads e por um canal de chat**. A partir daí, a regra a descrever o
estado é fria: *qualquer parte com acesso ao export ou ao chat onde ele passou possui o valor
integral da chave.*

O detalhe que faz deste caso um irmão do achado central (lição 04) é este:

> **A própria sessão que produziu o export não flagrou o próprio vazamento.** O vazamento só
> foi percebido por **revisão externa posterior** — outra cabeça, do outro lado de um gate. A
> sessão que continha o segredo não se auto-detectou.

Um papel que produz o artefato não é um bom auditor do próprio artefato. O vazamento foi pego
porque houve um segundo par de olhos — exatamente o padrão que o Nível 3 inteiro repete.

A cicatriz completa (com as citações de proveniência) vive no vault, e **ela mesma se
redige**: o valor da chave **não é reproduzido** ali, nem aqui. Este curso segue a mesma
regra — não há valor, prefixo, nem forma da credencial neste texto.
`[[vault:sisyphus-runtime/facts/_global/incident-2026-07-23-deepseek-api-key-leak]]`

---

## 🧠 O conceito central: output que contém segredo é artefato contaminado

A frase que a regra derivada cristaliza é a lente para o caso inteiro:

> **Output que contenha um segredo é um artefato contaminado.**

Isso reenquadra o problema. O vazamento não foi o instante em que o subagente imprimiu a
chave — foi o **artefato** que a impressão produziu. O export contaminado é um objeto durável
que carrega o segredo para onde quer que vá: Downloads, chat, backup, qualquer cópia. A
contaminação não é o ato; é a coisa que o ato deixa para trás, e que continua vazando
enquanto existir.

Por isso a remediação não é "não imprima mais". É estrutural, em duas frentes:

1. **A credencial vazada tem de ser rotacionada** — o segredo exposto deixa de valer.
2. **O artefato contaminado é tratado como contaminado** — não se distribui, e uma varredura
   de segredo no fechamento existe para pegá-lo antes que ele saia.

---

## ⚠️ A decisão do operador, e por que o caso segue OPEN

Aqui o caso ensina algo que os outros do nível não ensinam: **nem toda cicatriz fecha.**

O operador decidiu **não rotacionar a chave imediatamente**, e essa decisão está registrada
explicitamente **como ato do operador, não como recomendação do agente**. As consequências
estão escritas sem atenuação no incidente: a chave vazada segue válida; a superfície de
exposição (o export e o chat por onde passou) está inalterada; a regra de redação **não está
em vigor formal**; e um dispatch que dependia da rotação como precondição fica **bloqueado**.

O que torna este registro exemplar não é a decisão em si — é a **honestidade do registro sobre
ela**. O incidente permanece `status: open`, marca "risco continuado", e distingue com cuidado
uma frase de spec que dizia *"rotação executada"* (a **intenção** declarada no dia do
vazamento) do **estado de fato** (a rotação não ocorreu). É o achado central aplicado à
segurança: *afirmação sobre estado não vira verdade porque um spec a escreveu.* A rotação só é
real quando o disco a mostra — e o disco mostra que ela não aconteceu.

> Uma cicatriz honesta registra também as decisões que a mantêm aberta. Esconder que o risco
> continua seria a mesma patologia do dia inteiro: um artefato afirmando um estado (resolvido)
> que o estado não sustenta.

---

## 🗂️ A regra que nasceu: confidencialidade é por conteúdo, não por pasta

Deste incidente deriva a `dispatch-rule-confidentiality`. Seu princípio-mãe, herdado do acervo
que o originou:

> **Varra por conteúdo, não por pasta.** Uma pasta "restricted" é atalho de extração, não
> anonimização: material sensível vaza para fora dela.

A regra tem duas metades:

**Regra A — zonas restritas são read-DENY por padrão.** Um executor nunca abre, lê, faz
`grep`, `cat`, cita ou transcreve material de uma zona restrita declarada. E há um corolário
mecânico que é puro *garantia-estrutural-sobre-obediência*: nenhum comando **recursivo**
enraíza acima de uma zona restrita sem excluí-la **pelo mecanismo do próprio comando** —
`grep --exclude-dir`, `rg -g '!zona/**'`, `find -prune`. O caso mais instrutivo:

> **`md5sum -c MANIFEST` NÃO tem mecanismo de exclusão** — ele abre byte a byte todo arquivo
> do manifesto, a zona restrita inclusive. Um gate de integridade, inocente, é uma porta de
> leitura da zona restrita. Verificar manifesto que abranja zona restrita exige `[directive]`,
> como qualquer outra leitura dela.

**Regra B — confidencialidade é por conteúdo, esteja onde estiver.** Ao esbarrar, **em
qualquer pasta**, em conversa privada com terceiros identificáveis, perímetro societário/M&A,
ou segredo/credencial, o executor registra **só existência + natureza + local — nunca o
conteúdo**. E o "local" é truncado ao diretório quando o próprio nome do arquivo carrega o
nome de um terceiro. Se o trabalho *depende* do material, o executor não o reproduz: registra
ponteiro truncado + natureza e emite `[blocker]`. **A decisão de expor é do operador.**

`[[vault:sisyphus-runtime/facts/_global/dispatch-rule-confidentiality|Confidentiality]]`

---

## 🔗 Como a regra alcança cada papel — e vira gate

A confidencialidade não é uma boa intenção; é uma **condição verificável** costurada no loop,
e o desenho dela é uma aula de como uma regra *chega* a quem precisa dela:

- **O executor não lê `facts/`.** Então a regra não pode viver só num fact e esperar que o
  executor a obedeça. O **planejador** inlina no *escopo negativo do dispatch* o deny-por-padrão,
  o corolário do recursivo e o tratamento por conteúdo. O executor obedece o **dispatch**.
- **Momus-entrada** é a garantia estrutural: um dispatch que toque zona restrita, ou cujo
  material caia nas categorias da Regra B, **cujo escopo negativo não carregue essas
  cláusulas → achado BLOQUEANTE.** Isto transforma o dever do planejador de *memória* em
  *condição verificável*, rodada pelo papel que comprovadamente lê a regra.
- **Momus-saída** varre o **artefato inteiro** (não amostra) contra as três categorias —
  nomes próprios de terceiros, citação direta, número societário. E, crucialmente, **não** é um
  `grep` pela palavra "restricted": buscar a palavra da pasta seria repetir o erro de tratar a
  pasta como fronteira.
- **Post-exec-gate:** tocar zona restrita ou qualquer categoria da Regra B **torna o dispatch
  "sensível"** — e "sensível" dispara a Camada 2 (Momus-saída obrigatório). É assim que a
  varredura de segredo no fechamento vira a *primeira peça de máquina* da regra.

Repare no fecho: a defesa contra vazamento **não depende de a sessão que vaza se auto-detectar**
— e foi bom, porque no incidente ela não se detectou. A defesa é um Momus novo, do outro lado
de um gate, varrendo o artefato inteiro. Medição de terceiro, outra vez.

---

## 🧪 Exercício

**Contexto.** Seu runtime tem um acervo com material sensível e você vai despachar um trabalho
que o toca.

1. **Ache a porta de leitura inocente.** Liste os comandos do seu fluxo que enraízam
   recursivamente (`grep -r`, `md5sum -c`, `find`, `ls -R`, indexadores). Para cada um,
   responda: ele tem mecanismo de exclusão da zona restrita, e você o usou? O `md5sum -c` de
   manifesto é o caso-armadilha — o que você faz com ele?
2. **Contamine e detecte.** Faça um artefato de execução conter deliberadamente um segredo de
   teste (uma credencial falsa). Sua varredura de fechamento o pega **por conteúdo** (padrão
   de credencial em qualquer pasta), ou você só olhou a pasta "restricted"? Prove que ela pega
   o segredo mesmo fora de qualquer zona nomeada.
3. **Escreva sem reproduzir.** Simule esbarrar num arquivo cujo nome já é o nome de um
   terceiro. Escreva o registro correto — existência + natureza + local truncado ao diretório
   — sem que o nome do terceiro apareça em lugar nenhum do seu output.

**Critério de aprovação (medição de terceiro):** outra pessoa roda sua varredura do passo 2
contra um artefato onde ela mesma escondeu um segredo **fora** de qualquer pasta restrita.
Passa se a varredura o encontra por conteúdo. Se ela só encontra o que está dentro de
"restricted", você tratou a pasta como fronteira — que é exatamente o defeito que a regra
existe para fechar.

---

## 🔗 Para ir fundo

- Cicatriz completa, auto-redigida (privada): `[[vault:sisyphus-runtime/facts/_global/incident-2026-07-23-deepseek-api-key-leak]]`
- A regra derivada, com o enforcement por papel: `[[vault:sisyphus-runtime/facts/_global/dispatch-rule-confidentiality]]`
- "Sensível" dispara a Camada 2: `[[vault:sisyphus-runtime/facts/_global/dispatch-rule-post-exec-gate]]`
- Padrão canônico: `[[vault:long-running-agents/docs/canonical/regulated-data-boundary|Regulated Data Boundary]]`
- A lição-mãe: `01-a-familia-de-regras.md`
