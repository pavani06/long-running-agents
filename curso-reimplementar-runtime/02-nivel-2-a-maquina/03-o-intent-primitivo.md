---
title: "O intent primitivo: como uma intenção vira um dispatch determinístico"
type: curriculum-lesson
nivel: 2
aliases: ["intent primitivo", "five-part primitive", "dispatch determinístico", "deterministic tool dispatch"]
tags: [curriculo-conteudo, nivel-2, a-maquina, intent, dispatch, deterministic-tool-dispatch, five-part-primitive]
relates-to:
  - "[[vault:sisyphus-runtime/roles/planner|Charter — Planejador]]"
  - "[[vault:sisyphus-runtime/roles/protocol|Protocolo de Mensagem]]"
  - "[[vault:sisyphus-runtime/roles/launch-convention|Convenção de Launch]]"
  - "[[vault:long-running-agents/docs/canonical/intent-five-part-primitive|Intent as Five-Part Primitive]]"
  - "[[vault:long-running-agents/docs/canonical/deterministic-tool-dispatch|Deterministic Tool Dispatch]]"
last_updated: 2026-08-13
---

# 🎯 O intent primitivo: como uma intenção vira um dispatch determinístico
## As cinco partes que transformam "eu quero X" em um contrato que qualquer sessão executa igual

**Tempo Estimado:** 45 minutos
**Nível:** 2 — A Máquina
**Pré-requisito:** `02-nivel-2-a-maquina/02-o-loop-dispatch-gate.md`
**Status:** 🟢 A UNIDADE ATÔMICA — o dispatch por dentro

---

## 📖 Prólogo: o pedido de uma linha que virou três coisas diferentes

Alguém pediu: *"organize os fatos duráveis."*

Você dá esse pedido a três executores independentes, cada um numa sessão limpa. O primeiro
cria um índice novo em `facts/_moc.md`. O segundo renomeia metade dos arquivos para um
padrão "mais consistente". O terceiro edita o frontmatter de cada fato para adicionar uma
tag `organizado: true`. Os três estão convencidos de que fizeram exatamente o que foi pedido.
Os três fizeram coisas incompatíveis. E não há como o gate de saída dizer qual estava certo,
porque **o pedido nunca disse o que "organizar" significa em disco.**

O problema não é que os executores são desobedientes. É que uma **intenção** — "organize" —
não é executável. Ela é um sentimento sobre um estado desejado, e sentimentos não têm
escritas nomeadas. Entre a intenção e a execução falta uma tradução: alguém tem de converter
"eu quero X" num **contrato** tão específico que três sessões independentes produzam o
**mesmo** resultado, e que um gate mecânico consiga dizer se o resultado bate.

Esse contrato é o **dispatch**. E o que garante que ele seja determinístico — que não deixe
espaço para o executor "interpretar" — é a sua estrutura de cinco partes. Esta lição é sobre
como uma intenção vaga atravessa essa estrutura e sai do outro lado como uma ordem que não
admite dois resultados diferentes.

---

## 🧠 O conceito: o intent five-part primitive

O padrão canônico `intent-five-part-primitive` diz que uma intenção só está pronta para
virar trabalho quando foi decomposta em **cinco partes**. Enquanto faltar qualquer uma, o
que você tem é um desejo, não um dispatch — e um desejo dado a um executor vira improviso.
O planejador é o papel que faz essa decomposição; é literalmente a única coisa que ele faz,
e "isso é muito".

As cinco partes, mapeadas para os elementos que o charter do planejador exige:

| # | Parte do intent | No dispatch (charter do planejador) | O que responde |
|---|---|---|---|
| 1 | **Objetivo** | Autoridade única + spec por arquivo | *O que este dispatch quer que exista em disco?* |
| 2 | **Fronteira positiva** | **Escritas nomeadas** (lista exaustiva e literal de paths) | *Quais arquivos podem ser criados/modificados?* |
| 3 | **Fronteira negativa** | **Escopo negativo** (o que é proibido) | *O que um executor bem-intencionado faria a mais, "ajudando"?* |
| 4 | **Verificação** | Checks que o executor roda antes de `done`, com evidência colada | *Como sabemos, mecanicamente, que ficou certo?* |
| 5 | **Destino** | Report + classe (`custodia`/`produto`) + onde persistir o handoff | *Para quem vai o resultado e sob qual regime de gate?* |

Duas dessas partes são **obrigatórias sob pena de o dispatch ser malformado** — e um
dispatch malformado é reprovado pelo Momus-entrada antes de chegar a qualquer executor:

- **Escritas nomeadas** (parte 2). Paths completos, um por linha. Não "os arquivos de
  configuração", não "o que for necessário". Se não está na lista, o executor não toca. Essa
  lista é *exatamente* o que o gate de saída usa como referência do diff mecânico — uma lista
  vaga torna o gate de saída inaplicável, e **um gate inaplicável é um gate ausente**.
- **Escopo negativo** (parte 3). Não é redundante com as escritas nomeadas: ele captura as
  **tentações concretas** daquele dispatch. "Não mova o legado", "não rode `git init`", "não
  crie `state/<topic>/` ainda". É onde o planejador antecipa o improviso plausível.

### Por que cinco, e não "um prompt bem escrito"

Porque cada parte fecha um caminho de divergência específico. Tire a parte 3 (escopo negativo)
e o executor "melhora" o que não foi pedido. Tire a parte 4 (verificação) e o `done` vira uma
afirmação sem prova. Tire a parte 2 (escritas nomeadas) e o gate de saída não tem contra o quê
comparar. As cinco partes não são um formulário burocrático — são **cinco buracos por onde a
intenção vaza para virar improviso**, tapados um a um.

---

## ⚙️ Deterministic tool dispatch: por que a mesma entrada dá a mesma ação

O segundo padrão desta lição é `deterministic-tool-dispatch`, e é ele que garante que o
sistema seja **auditável**. A ideia: dada a mesma entrada verificável, o sistema toma sempre
a **mesma** ação — sem ponderação, sem "nesse caso específico".

Você já viu isso rodando, sem o nome, na lição anterior. O orquestrador é um **autômato**:
recebe um `TYPE`, checa uma condição em disco, executa uma ação de uma tabela. Ele não
interpreta. E o `protocol` reforça: o **vocabulário de `TYPE` é fechado** (sete tipos, nada
fora da lista); um `TYPE` desconhecido não é interpretado com boa vontade, é tratado como
malformado e escalado.

O dispatch determinístico é a mesma disciplina aplicada à *intenção*: assim como o hub não
improvisa uma ação para um `TYPE` que não conhece, o executor não improvisa um resultado para
uma spec que não especifica. A cadeia inteira é determinística de ponta a ponta:

```
intenção vaga  ──(planejador: decompõe em 5 partes)──►  dispatch
   "organize"        objetivo + escritas nomeadas +          (contrato
                     escopo negativo + verificação +          determinístico)
                     destino
                          │
                          ▼
              ┌──────────────────────────────────┐
              │  deterministic tool dispatch:     │
              │  mesma entrada → mesma ação        │
              │  — o executor não interpreta,      │
              │    materializa as escritas nomeadas│
              │  — o hub não pondera, casa e roteia│
              └──────────────────────────────────┘
                          │
                          ▼
        três executores independentes → o MESMO resultado
        gate mecânico → decide PASS/FAIL sem julgar intenção
```

O teste de que um dispatch é determinístico é o do prólogo, invertido: **três executores
independentes, cada um numa sessão limpa, produzem o mesmo resultado.** Se produzem resultados
diferentes, a intenção não foi decomposta — sobrou espaço de interpretação, e esse espaço é
onde o improviso mora.

> 🔑 Ponte com o Nível 1: o dispatch aponta, não carrega. As cinco partes referenciam paths e
> specs no vault; a mensagem `[handoff]` que o entrega é **ponteiro, nunca payload** — o corpo
> diz *que* o dispatch existe e *onde*, e o contrato inteiro mora no arquivo, auditável depois
> do fim da sessão. Mesmo princípio do `protocol`: mensagem = sinal, arquivo = verdade.

---

## 🧪 Exercício: decomponha uma intenção e teste o determinismo

**Contexto.** Leitura de `roles/planner.md` §1 e raciocínio. Sem escrita no vault.

1. **Ache as cinco partes num dispatch real.** Abra um dos dispatches em
   `dispatches/runtime/` (por exemplo `dispatch-schema-veredito.md`). Localize, no texto, cada
   uma das cinco partes do intent. Alguma está implícita ou ausente? Se sim, qual buraco de
   divergência ela deixa aberto?

2. **Decomponha uma intenção vaga.** Pegue "organize os fatos duráveis" (o prólogo) e escreva
   as cinco partes que a tornariam determinística. Seja concreto: quais escritas nomeadas
   (paths literais)? Qual escopo negativo (o que um executor "prestativo" faria a mais)? Qual
   verificação mecânica prova que ficou certo?

3. **O teste dos três executores.** Para o seu dispatch do passo 2, argumente em duas frases
   por que três sessões limpas produziriam o **mesmo** resultado. Se você não consegue
   argumentar isso, qual das cinco partes ainda está frouxa?

4. **A parte que quebra o gate.** Qual das cinco partes, se deixada vaga, torna o gate de
   saída (Camada 1) inaplicável? Explique por que "um gate inaplicável é um gate ausente".

**Critério de aprovação (medição de terceiro):** suas cinco partes só "passam" quando **outra
pessoa** (ou outra sessão) pega o seu dispatch do passo 2, o executa mentalmente como um
executor de escopo fechado, e confirma que (a) não precisou interpretar nada e (b) chegou ao
mesmo resultado que você previu. Se ela divergiu, o dispatch não era determinístico — e a
divergência dela é o achado, não a opinião dela. Você não aprova a própria decomposição.

---

## 🔗 Para ir fundo

- O que faz um dispatch, na fonte: `[[vault:sisyphus-runtime/roles/planner|Charter — Planejador]]`
- O contrato de mensagem (ponteiro, não payload): `[[vault:sisyphus-runtime/roles/protocol|Protocolo de Mensagem]]`
- Como a sessão nasce com o `TOPIC` e o charter: `[[vault:sisyphus-runtime/roles/launch-convention|Convenção de Launch]]`
- Padrão canônico — a intenção em cinco partes: `[[vault:long-running-agents/docs/canonical/intent-five-part-primitive|Intent as Five-Part Primitive]]`
- Padrão canônico — mesma entrada, mesma ação: `[[vault:long-running-agents/docs/canonical/deterministic-tool-dispatch|Deterministic Tool Dispatch]]`
- Próximo passo: `exercises/exercise-01-ciclo-a-mao.md` — rode um ciclo completo à mão.
