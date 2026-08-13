---
title: "Exercício: derivar a regra de um incidente e escrever o gate que a pega"
type: curriculum-exercise
nivel: 3
aliases: ["derivar a regra", "exercício regra e gate", "flywheel do incidente"]
tags: [curriculo-conteudo, nivel-3, governanca, exercicio, gate-design, flywheel, fecho, medicao-de-terceiro]
relates-to:
  - "[[vault:sisyphus-runtime/facts/_global/dispatch-rule-escalation|Rule: Escalation List]]"
  - "[[vault:sisyphus-runtime/facts/_global/dispatch-rule-amendment-provenance|Rule: Amendment Provenance]]"
  - "[[vault:sisyphus-runtime/meta/registry.md|Registry — a nota sobre fechos]]"
last_updated: 2026-08-13
---

# 🛠️ Exercício: derivar a regra de um incidente e escrever o gate que a pega
## O flywheel do sistema, feito à mão: incidente → regra → gate → medição de terceiro

**Tempo Estimado:** 75 minutos
**Nível:** 3 — Governança e Cicatrizes
**Pré-requisito:** todas as lições do Nível 3 (`01` a `04`) e os dois casos
**Status:** 🔴 EXERCÍCIO-CHAVE — não é auto-aprovável, por construção
**Solução comentada:** `solutions/solution-01-derivar-a-regra.md` (leia só depois de tentar)

---

## 🎯 O que você vai treinar

O runtime cresce por um **flywheel**, descrito na `dispatch-rule-escalation`:

> gate falhou → incidente registrado em `facts/_global/` → nova `dispatch-rule-*` → se define
> um novo ponto de parada, entra na lista de escalação como gatilho.

Você já leu regras prontas. Agora você vai rodar o flywheel **do zero**: receber um incidente
cru, derivar a regra que ele deveria produzir, e — a parte que separa uma regra que funciona de
uma que só parece funcionar — **escrever o gate que a pega medindo o disco**, não lendo
promessas.

O incidente abaixo é sanitizado e fictício, mas a classe de defeito é a mais recorrente do
sistema (lição 04). Ele **não** corresponde a nenhuma regra já pronta no vault — se você se
pegar escrevendo "isto já é a regra X", olhe de novo: a forma da correção que ele pede é sua
para descobrir.

---

## 📋 O incidente (seu material de trabalho)

> **Incidente — "o índice que se declarou completo" (sanitizado, para exercício)**
>
> **O que aconteceu.** Uma sessão foi encarregada de migrar os tópicos de um runtime para um
> novo `schema-version` (de `v19` para `v20`). Ao terminar, ela atualizou o índice de estado
> em `state/current/` com uma linha de fechamento: *"✅ Todos os 12 tópicos migrados para
> v20."* A frase estava correta **no instante em que foi escrita** — os 12 tópicos existentes
> naquele momento estavam de fato em `v20`.
>
> **A quebra.** Dois dias depois, um 13º tópico foi criado por outra sessão, ainda em `v19`
> (o default do template não tinha sido atualizado). Uma terceira sessão leu o índice, viu
> *"Todos os 12 tópicos migrados para v20"*, e tratou a migração como **encerrada** — não
> re-verificou. Trabalho subsequente assumiu `v20` universal e produziu um artefato que
> quebrou ao encontrar o tópico `v19`.
>
> **A forense.** Ninguém escreveu um número falso. Cada tópico contado estava mesmo em `v20`.
> O que envelheceu foi o **fecho**: a palavra "todos", e o número "12", afirmavam um presente
> que a lista não podia sustentar assim que a população mudou. A frase se tornou falsa **sem
> que ninguém a editasse** — o mundo mudou embaixo dela.
>
> **Dano concreto.** Um artefato quebrado, reconstruído em uma hora. Baixo. Mas "certo por
> sorte até deixar de ser" não valida o processo.

---

## ✅ Suas entregas

### Parte 1 — Classifique o defeito (10 min)

Em três a cinco linhas: a que **classe** este incidente pertence? Conecte-o explicitamente ao
achado central da lição 04 e à nota do `registry.md` sobre **fechos**. A afirmação era um
*fato falso* ou um *fecho que envelheceu*? Por que a distinção muda a correção?

### Parte 2 — Derive a regra (20 min)

Escreva a `dispatch-rule-*` que este incidente deveria produzir, no formato do vault:
**Rule** (uma frase imperativa), **Rationale**, **What qualifies** / **What does NOT qualify**,
**Enforcement**. Duas armadilhas para evitar:

- **Não escreva "seja mais cuidadoso com resumos".** Isso é obediência, não estrutura (lição
  01). Se a sua regra depende de alguém *lembrar* de re-verificar, ela já falhou pelo mesmo
  motivo que o dia inteiro da lição 04 falhou.
- **Ataque a classe, não o caso.** A regra não é sobre migrações de schema. É sobre a forma
  geral de que um **fecho** ("todos", "N itens", "completo") não se valida olhando o artefato.

### Parte 3 — Escreva o gate que a pega (30 min)

Este é o núcleo. Escreva o gate que mediria o **disco** para detectar a violação — sem ler a
promessa do índice. Ele precisa:

1. **Enumerar a população referente por fonte independente** — não confiar na contagem que o
   artefato declara. (Dica: pergunte ao disco quantos tópicos existem e qual o `schema-version`
   de cada, em vez de acreditar no "12".)
2. **Falhar fechado** — se a fonte independente não puder ser enumerada, retornar ao operador
   com o observado, nunca assumir "completo".
3. **Ser auto-arquivável** — poder ser citado num relatório sem se auto-disparar (lição 02).

Entregue o gate como um comando (ou pequeno script) executável, com o `EXPECT` declarado e o
`T_ref`/baseline explicitado se for o caso.

### Parte 4 — Decida se vira gatilho de escalação (10 min)

A regra define um novo **ponto de parada** que o orquestrador deveria escalar? Se sim, escreva
o gatilho como uma linha verificável mecanicamente (no estilo dos 11 gatilhos existentes). Se
não, justifique por que a Camada 1 do `post-exec-gate` já o cobre.

---

## 🧷 Critério de aprovação — medição de terceiro (inegociável)

Coerente com o achado central que este exercício inteiro ensina, **você não aprova o próprio
trabalho.** O exercício "passa" quando **outra pessoa** (ou outra sessão) faz o seguinte e
confirma:

1. Pega o seu gate da Parte 3 e o roda contra um estado onde ela mesma **acrescentou um 13º
   item fora do fecho declarado** (um tópico `v19` novo, um índice que ainda diz "todos os 12").
2. Confirma que o seu gate **recusa** esse estado — que ele reprova a afirmação de completude
   medindo a população real, sem que você precise admitir que a lista envelheceu.
3. Tenta **lavar a promessa**: alterar só o texto do índice ("agora são 13, todos v20") sem
   migrar o 13º, e confirma que o gate ainda pega — porque ele mede o `schema-version` de cada
   tópico no disco, não a frase.

Se o revisor consegue fazer o seu gate aprovar um fecho falso, ele está lendo a promessa. Volte
à Parte 3.

> ⚠️ **Não leia a solução antes de ter as quatro partes escritas e o gate rodando.** A solução
> comentada mostra *uma* forma correta — não a única — e discute os erros mais comuns. Ela vale
> muito mais depois da sua tentativa do que no lugar dela.

---

## 🔗 Para ir fundo

- A nota do registry sobre fechos datados × não-datados (privada): `[[vault:sisyphus-runtime/meta/registry.md]]`
- O flywheel e a lista de gatilhos: `[[vault:sisyphus-runtime/facts/_global/dispatch-rule-escalation]]`
- "Gates são texto-base": `[[vault:sisyphus-runtime/facts/_global/dispatch-rule-amendment-provenance]]`
- Solução comentada: `solutions/solution-01-derivar-a-regra.md`
