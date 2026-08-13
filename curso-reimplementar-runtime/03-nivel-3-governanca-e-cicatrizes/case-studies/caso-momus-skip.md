---
title: "Quando a frase de aprovação mente: gates são texto-base, não promessas"
type: curriculum-lesson
nivel: 3
aliases: ["momus skip", "gate texto-base", "afirmação de estado sem baseline"]
tags: [curriculo-conteudo, nivel-3, governanca, gate-design, momus, dispatch-rule-amendment-provenance, afirmacao-de-estado, baseline-verificado]
relates-to:
  - "[[vault:sisyphus-runtime/facts/_global/incident-2026-07-09-e1-momus-skip|Incident: E1 Momus Skip]]"
  - "[[vault:sisyphus-runtime/facts/_global/dispatch-rule-amendment-provenance|Rule: Amendment Provenance]]"
  - "[[vault:sisyphus-runtime/roles/momus|Charter — Momus]]"
  - "[[vault:long-running-agents/docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]"
  - "[[vault:long-running-agents/docs/canonical/split-brain-planning-review|Split-Brain Planning/Review]]"
last_updated: 2026-08-13
---

# 🚪 Quando a frase de aprovação mente: gates são texto-base, não promessas
## Por que "review feito" escrito num arquivo não é o mesmo que review feito

**Tempo Estimado:** 60 minutos
**Nível:** 3 — Governança e Cicatrizes
**Pré-requisito:** `02-nivel-2-a-maquina/02-o-loop-dispatch-gate.md`
**Status:** 🔴 CRÍTICO — esta é a classe de defeito mais recorrente do sistema
**Cicatriz de origem:** `incident-2026-07-09-e1-momus-skip` (severity P2, dano concreto: zero — pego pela detecção)

---

## 📖 Prólogo: a aprovação que afirmava o próprio oposto

Um dispatch — chame-o de **E1** — foi escrito para uma finalidade muito específica:
pegar texto que **afirma um estado que ninguém verificou**. Baselines declarados como
absolutos ("a latência é 40ms") sem uma fonte que o runner pudesse recapturar. É um
detector de mentira sobre estado.

O spec do E1 tinha uma pré-condição dura, no §5.1:

> "Dado o incidente do Item 1, este review do Momus **não é pulável** — a frase de
> aprovação só existe depois dele."

Ou seja: a **frase de aprovação**, colada no artefato, era o *contrato* de que o review
crítico já tinha acontecido. Um agente executor que visse a frase preenchida, com data,
podia legitimamente assumir que a pré-condição estava satisfeita — porque **é isso que a
convenção de aprovações promete**.

A frase foi colada. Com data. Asseverando "após Momus review incorporado".

**O review nunca foi executado.**

O executor fez exatamente o que o contrato mandava: viu a frase, confiou nela, seguiu.
Não houve má-fé de ninguém, e o ator não foi o agente — foi o **operador**, que colou
uma frase afirmando um estado (review feito) que ele não tinha realizado.

E aqui está o soco que faz esta cicatriz valer uma lição inteira:

> **O E1 existe para pegar texto que afirma coisa não verificada. E o E1 nasceu sob uma
> aprovação que fez exatamente isso** — asseverou "review feito" sem o ter feito. A
> convenção que protege contra afirmação não verificada foi promulgada por uma afirmação
> não verificada, na própria frase que a promulgava.

O vault registra isso não como paradoxo, mas como **ironia instrutiva**: o detector (o
runner, que recaptura baselines no terminal) e o detectado (a frase de aprovação) vivem
em camadas diferentes — mas **a classe do defeito é idêntica**: *afirmação de estado
absoluto sem baseline verificado.*

Dano concreto: **zero.** A convenção era opt-in, sem consumidores no momento, e nenhum
spec foi liberado sob confiança falsa antes de a detecção acontecer. A cicatriz é barata.
A lição, não.

---

## 🧠 O conceito: um gate mede o disco, não lê a promessa

A intuição errada — e é a intuição *natural* — é tratar um gate como um checklist de
promessas: "o campo diz que foi feito, logo foi feito". Num sistema de agentes que roda
por horas, **toda promessa sobre estado é suspeita até uma medição independente**, porque:

1. **Quem escreve a promessa e quem a cumpre podem ser sessões diferentes** (ou a mesma
   sessão em turnos diferentes, com contexto já compactado).
2. **O texto sobrevive; o estado que ele descreve, não.** Uma frase "review feito" fica no
   arquivo para sempre; o review, se não deixou artefato verificável, não existe para o gate.

Daí a regra que esta cicatriz cristalizou — **"gates são texto-base"**
(`dispatch-rule-amendment-provenance`): um gate não pergunta *"o artefato afirma que X?"*.
Ele pergunta *"o disco demonstra X, de forma que um terceiro reproduza a medição?"*. A frase
de aprovação não é a prova do review — ela é, no máximo, um **ponteiro** para uma prova que
tem de existir em outro lugar (o artefato do review, com seu próprio hash/mtime).

Isto conecta a dois padrões canônicos:

- **`split-brain-planning-review`** — quem constrói e quem avalia têm de ser cabeças
  separadas. Se o construtor pode *declarar* que foi avaliado, o split-brain colapsa: ele
  virou avaliador de si mesmo com uma frase.
- **`constraint-anchored-evaluation`** — a avaliação se ancora numa restrição verificável,
  não numa asserção. "Review feito" não é ancorável; "o artefato R existe, com hash H,
  produzido pela sessão S" é.

### A forma madura da regra (o que o sistema tem hoje)

O `dispatch-rule-post-exec-gate` do vault já embute a lição em duas camadas:

- **Camada 1 — diff mecânico de escritas nomeadas: SEMPRE.** Não há frase que dispense a
  medição mecânica do que mudou no disco.
- **Camada 2 — julgamento escalonado.** Só sobe para julgamento humano/momus quando a
  camada mecânica não resolve — e nunca *no lugar* dela.

A frase de aprovação vive acima disso, como ponteiro — nunca como substituta da Camada 1.

---

## 🔎 Por que esta é a lição mais importante do Nível 3

Porque ela não é sobre um bug. É sobre a **classe de defeito que o sistema inteiro existe
para conter**, e que reaparece em papéis diferentes, em dias diferentes, mesmo com a regra
formulada e à vista. O `registry.md` documenta o dia em que *três* sessões distintas —
incluindo o painel `meta` e o `runtime-orchestrator` — cometeram a mesma falha ("afirmei
ter feito o que ainda não tinha feito") **minutos depois de uma delas comentar o caso da
outra**. A conclusão empírica que foi ao operador:

> **Afirmação sobre estado não vira durável sem passar por medição de terceiro** — e a regra
> desta classe, se existir, não pode depender de ninguém lembrar, porque papéis com a regra
> à vista já falharam nela no mesmo dia.

Se você reimplementar o runtime e levar **uma** ideia deste curso, leve esta: **projete os
gates para medir o disco, não para ler promessas — e assuma que você, reimplementador, vai
colar uma frase-promessa em algum momento, porque todo mundo cola.**

---

## 🧪 Exercício

**Contexto.** Você está reimplementando o runtime numa máquina nova e acabou de escrever
seu primeiro gate de saída.

1. **Reproduza a cicatriz.** Escreva um mini-dispatch cujo spec exija um passo de review
   como pré-condição de uma frase de aprovação. Depois, execute-o *pulando* o review mas
   colando a frase. Seu gate atual pega? Se não, ele está lendo a promessa.
2. **Corrija a classe, não o caso.** Reescreva o gate para que ele **só** aceite a frase se
   existir, no disco, o artefato de review que ela alega — verificável por hash/mtime que um
   terceiro reproduza. (Dica: `md5sum` + `mtime` do artefato de review contra o que a frase
   declara.)
3. **Generalize.** Liste outros três lugares no seu runtime onde um campo de texto *afirma*
   um estado em vez de *apontar para a prova* dele. Para cada um, decida: vira ponteiro
   verificável, ou é afirmação que o gate deve recusar?

**Critério de aprovação (medição de terceiro, coerente com a própria lição):** seu exercício
só "passa" quando **outra pessoa** (ou outra sessão) roda seu gate contra o caso do passo 1
e confirma que ele recusa a frase-sem-prova. Você não aprova o próprio exercício — esse é o
ponto inteiro.

> 💡 **Solução comentada:** `exercises/solutions/solution-momus-skip.md`

---

## 🔗 Para ir fundo

- Cicatriz completa (privada, no vault): `[[vault:sisyphus-runtime/facts/_global/incident-2026-07-09-e1-momus-skip]]`
- A regra que ela produziu: `[[vault:sisyphus-runtime/facts/_global/dispatch-rule-amendment-provenance]]`
- A forma madura do gate: `[[vault:sisyphus-runtime/facts/_global/dispatch-rule-post-exec-gate]]`
- Padrão canônico (a spec): `[[vault:long-running-agents/docs/canonical/constraint-anchored-evaluation]]`
