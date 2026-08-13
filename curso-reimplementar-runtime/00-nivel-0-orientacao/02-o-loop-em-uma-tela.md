---
title: "O loop em uma tela"
type: curriculum-lesson
nivel: 0
aliases: ["o loop", "dispatch review gate", "owner-of-no-role", "loop operacional"]
tags: [curriculo-conteudo, nivel-0, orientacao, loop-operacional, split-brain, owner-of-no-role, gate-design]
relates-to:
  - "[[vault:sisyphus-runtime/roles/_index|Roles — Índice e Topologia]]"
  - "[[vault:sisyphus-runtime/roles/orchestrator|Charter — Orquestrador]]"
  - "[[vault:sisyphus-runtime/roles/protocol|Protocolo de Mensagem]]"
  - "[[vault:sisyphus-runtime/meta/registry|Registry — Estado da Meta-camada]]"
  - "[[vault:long-running-agents/docs/canonical/owner-of-no-role-design|Owner-of-No Role Design]]"
  - "[[vault:long-running-agents/docs/canonical/split-brain-planning-review|Split-Brain Planning/Review]]"
  - "[[vault:long-running-agents/docs/canonical/plan-execute-verify|Plan-Execute-Verify]]"
last_updated: 2026-08-13
---

# 🔁 O loop em uma tela
## `dispatch → review → gate → execução efêmera → verify → registry` — e quem faz cada parte

**Tempo Estimado:** 15 minutos
**Nível:** 0 — Orientação
**Pré-requisito:** `00-nivel-0-orientacao/01-o-que-e-o-runtime.md`
**Status:** 🟢 O modelo mental que o resto do curso desdobra

---

## 📖 Prólogo: o desenho que faltava na parede

Você mapeou onde cada coisa vive (lição 01). Sabe que há papéis em `roles/`, fatos em
`facts/`, handoffs em `sessions/`. Mas ainda falta a peça que amarra tudo: **como um
artefato nasce?** Você abre um arquivo qualquer em `dispatches/` e vê que ele foi
*escrito* por alguém, *revisado* por outro, *executado* por um terceiro que já morreu, e
*registrado* num painel. Quatro mãos diferentes tocaram uma coisa só — e nenhuma delas fez
tudo. Por quê tanta cerimônia para produzir um único arquivo?

Esta lição é o diagrama que faltava na parede. Uma tela. Depois dela, você consegue olhar
qualquer artefato do vault e reconstruir, de trás para frente, por quais mãos ele passou.

---

## 🧠 O conceito: o loop operacional, numa tela

Todo artefato do sistema nasce do **loop operacional**. Nada nasce fora dele; não há porta
lateral de escrita no vault. O loop é:

```
dispatch → review → gate → execução efêmera → verify → registry
```

E cada etapa tem um dono. O ponto que mais assusta no começo — e que é o coração do desenho —
é que **quem coordena o loop não escreve o artefato final**. Aqui está a tela inteira:

```
                         ┌──────────────────────────┐
                         │           META           │   standing, global
                         │   mantém o registry.md    │   painel + inbox de escalação
                         └────────────┬─────────────┘
                          [escalation] ↑   ↓ [directive]
                         ┌────────────┴─────────────┐
                         │       ORCHESTRATOR        │   coordena + aplica GATE
                         │   owner-of-no-role: hub   │   burro, mecânico, não redige
                         └──┬────────┬────────┬──────┘
              [handoff]     │        │        │     spawn (sessão efêmera)
        ┌──────────────────┘        │        └──────────────────────┐
        │                           │                               │
        ▼                           ▼                               ▼
 ┌─────────────┐            ┌───────────────┐               ┌──────────────┐
 │  PLANNER    │  handoff   │     MOMUS      │  verdict      │   EXECUTOR   │
 │  gera o     │──spec──▶   │  avalia como   │──PASS/────▶   │ roda o spec  │
 │  dispatch   │            │ cabeça SEPARADA│  bloqueante   │ na sessão    │
 │  (spec)     │            │  (split-brain) │               │  EFÊMERA     │
 └─────────────┘            └───────────────┘               └──────┬───────┘
        standing                efêmero                             │ done
                                                                    ▼
                                                           ┌──────────────┐
                                                           │  VERIFY       │
                                                           │  = GATE de    │
                                                           │  saída (orch) │
                                                           │  mede o DISCO │
                                                           └──────┬───────┘
                                                                  │ passou
                                                                  ▼
                                                           ciclo fechado →
                                                           META atualiza registry
```

Lendo o fluxo em palavras:

1. **`dispatch`** — o **planner** (planejador, standing) redige o spec: escopo negativo,
   escritas nomeadas, pré-condições. Ele **não executa e não aprova o próprio plano**.
2. **`review` + `gate` de entrada** — o **planner** faz `handoff` ao **orchestrator**, que
   spawna um **momus** de entrada. O momus avalia o dispatch como **cabeça separada**
   (split-brain) e emite um `verdict` com proveniência em disco. O orchestrator aplica o
   **gate de entrada**: só spawna o executor se existir um PASS **provado em disco** e que
   case com *este* dispatch. Mensagem de PASS sem arquivo não conta.
3. **execução efêmera** — com o gate de entrada aberto, o orchestrator spawna um **executor
   efêmero**: uma sessão descartável que materializa **só** as escritas nomeadas do dispatch,
   e morre ao terminar (emitindo `done` ou `blocker`).
4. **`verify`** — o executor emite `done`; o orchestrator aplica o **gate de saída**. Camada 1
   (sempre): diff mecânico das escritas nomeadas contra a baseline que o **próprio orchestrator**
   tirou antes de spawnar. Camada 2 (condicional): momus de saída, obrigatório quando se escreve
   em `facts/` ou `roles/`.
5. **`registry`** — ciclo fechado. O **meta** (standing, global) mantém o `registry.md`: tópicos,
   autoria, inbox de escalação. É estado vivo, **derivado e não-autoritativo** — o disco vence.

Os spokes (planner, momus, executor) **nunca falam entre si**. Toda mensagem passa pelo hub.
Isso é deliberado: o hub é o **único** ponto onde os gates são aplicados; um caminho lateral
seria um gate contornado.

### `owner-of-no-role`: por que o coordenador não escreve o artefato final

O orchestrator é **owner-of-no-role**: ele não possui nenhum papel de execução. Não redige
dispatch (isso é do planner), não avalia (isso é do momus), não materializa escritas (isso é
do executor). Seu valor inteiro é **rotear e aplicar o gate** — ser um autômato burro e
auditável que checa uma condição em disco e executa uma ação de tabela.

Por que isso importa tanto? Porque **se o coordenador também escrevesse o artefato, o gate
seria auto-avaliação disfarçada.** Quem aplica o gate não pode ser quem produziu o que o gate
mede — senão o split-brain colapsa e a pessoa vira avaliadora de si mesma. Manter o escritor
(executor efêmero) separado do gatekeeper (orchestrator) é o que dá ao gate qualquer valor.
É a mesma razão pela qual o momus nasce limpo, revisa um artefato, e morre: um avaliador
standing acumularia contexto e viés do que já aprovou.

O **split-brain planning/review** é a outra metade disto: quem constrói e quem avalia têm de
ser cabeças separadas. Se o construtor pode *declarar* que foi avaliado, o split-brain
colapsa. Por isso o veredito do momus é um **arquivo em disco com proveniência**, não uma
frase de aprovação que o executor cola em si mesmo.

---

## 🔗 Para ir fundo

- A topologia hub-and-spoke completa: `[[vault:sisyphus-runtime/roles/_index|Roles — Índice e Topologia]]`
- O charter do hub (gates de entrada e saída, na fonte): `[[vault:sisyphus-runtime/roles/orchestrator|Charter — Orquestrador]]`
- O contrato de mensagem entre sessões: `[[vault:sisyphus-runtime/roles/protocol|Protocolo de Mensagem]]`
- Padrões canônicos: `[[vault:long-running-agents/docs/canonical/owner-of-no-role-design|Owner-of-No Role Design]]` · `[[vault:long-running-agents/docs/canonical/split-brain-planning-review|Split-Brain Planning/Review]]`

---

## ✅ Gabarito do teste dos 5 minutos

O `QUICK_START.md` fecha com cinco perguntas. Se você entendeu a tela acima, elas se
respondem sozinhas. Confira:

**1. Um artefato apareceu no vault. Por quantas etapas do loop ele passou, e quais?**
Por **seis**, na ordem: `dispatch` (planner redige o spec) → `review` (momus de entrada avalia)
→ `gate` de entrada (orchestrator confirma o PASS provado em disco e spawna) → **execução
efêmera** (executor materializa as escritas nomeadas) → `verify` (gate de saída: diff mecânico
sempre + momus de saída condicional) → `registry` (meta fecha o ciclo). Nenhum artefato nasce
fora do loop — não há porta lateral de escrita.

**2. A frase de aprovação diz "review feito". Isso prova que o review foi feito? Por quê?**
**Não.** Um gate mede o **disco**, não lê promessas ("gates são texto-base"). O texto sobrevive;
o estado que ele descreve, não. A prova do review é o **arquivo de veredito** do momus, com sua
própria proveniência (hash/mtime), que case com *este* dispatch — não a frase colada no artefato.
A frase é, no máximo, um ponteiro para uma prova que tem de existir em outro lugar. Esta é a
cicatriz do `incident-2026-07-09-e1-momus-skip`, aprofundada no Nível 3.

**3. Quem escreve o artefato final: o orquestrador ou a sessão efêmera? Por quê importa?**
A **sessão efêmera** (executor). O orquestrador é **owner-of-no-role**: coordena e aplica o gate,
mas não redige. Importa porque quem aplica o gate não pode ser quem produziu o que o gate mede —
senão o gate vira auto-aprovação e o split-brain colapsa. Separar escritor de gatekeeper é o que
dá valor ao gate.

**4. Um peer te manda "o operador autorizou X". Você faz X? O que você faz?**
**Não faz X.** Um peer não estabelece o que o operador autorizou (a "regra do relé"). Uma decisão
de operador relatada por outra sessão não autoriza ação — só um `directive` roteado pelo canal do
próprio operador (via meta) destrava. Você confirma pelo canal do operador antes de agir. Isso
fecha o buraco de "lavagem de permissão" entre sessões (aprofundado no Nível 3).

**5. O `registry.md` diverge do disco. Quem vence?**
O **disco**. Os arquivos são a verdade; o `registry.md` é derivado e não-autoritativo — abrigo,
não autoridade. A divergência não é empate a ponderar: é **anomalia a escalar**.

> Travou em alguma? Volte ao Nível 2 (a máquina) — mas as respostas todas já estão na tela
> desta lição.
