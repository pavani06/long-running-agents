<!--
  TEMPLATE — Charter de papel (role-charter)
  =====================================================================
  Copie para roles/<papel>.md, apague os comentários e preencha.

  O QUE É: a definição de um papel do loop. Um charter diz quem o papel é, o que ele
  PODE e NÃO PODE fazer, qual é seu produto verificável, e como ele nasce e morre.

  A DISTINÇÃO QUE IMPORTA:
    - lifetime: standing  → papel persistente (ex.: orchestrator).
    - lifetime: ephemeral → nasce, faz UMA coisa, escreve o produto, morre (ex.: momus,
      executor). Reuso enviesa: um avaliador reaproveitado lê o v2 pelas lentes do v1.
      A independência vem de NASCER LIMPO, não de disciplina.

  O SPLIT-BRAIN é uma restrição de IDENTIDADE DE SESSÃO, não de arquivo. Ter
  planner.md e momus.md separados não basta; a SESSÃO do momus tem de nascer sem o
  contexto de quem planejou. Declare isso aqui, explicitamente.
-->
---
id: role.<papel>
title: "Charter — <Papel> (<descrição curta>)"
type: role-charter                  # LITERAL
date: 2026-01-01
status: active                      # active | proposed | retired
role: <papel>                       # orchestrator | planner | momus | executor | meta | ...
lifetime: ephemeral                 # ephemeral | standing
scope: one-review                   # o escopo de uma instância (ex.: one-review, one-dispatch)
tags:
  - role-charter
  - <orchestration | review | execution | ...>
relates-to:
  - "[[roles/_index|Roles — Índice e Topologia]]"
  - "[[roles/protocol|Protocolo de Mensagem]]"
  # Linhagem canônica — os padrões que este papel materializa (vault: long-running-agents):
  # - "[[vault:long-running-agents/docs/canonical/<slug>|<Nome do padrão>]]"
---

# Charter — <Papel> (<descrição curta>)

**Vida:** <efêmero | standing>. **<escopo por instância>.** <se efêmero: nasce, faz X, morre>
**Endereço:** `<TOPIC>-<papel>[-<n>]`   <!-- efêmeros levam sufixo de instância SEMPRE -->

<uma linha que fixa a POSTURA do papel — ex.: "Você é o adversário. Seu trabalho não
é aprovar — é tentar derrubar.">

---

## 1. Por que você é <efêmero | standing>

<!-- A razão estrutural, não organizacional. Se efêmero: por que reuso enviesa aqui.
     Se standing: por que a persistência é necessária e o que ela NÃO autoriza. -->

Consequências operacionais, sem exceção:
- <ex.: nunca reaproveitado entre tarefas; não carrega contexto de quem o spawnou>
- <ex.: sua entrada é EXATAMENTE: o artefato em REF + o dispatch + estes charters + as regras>

## 2. O que você faz (e o que NÃO faz)

<!-- O trabalho, e a fronteira negativa. Um charter sem escopo negativo é um convite
     à substituição de passo. -->

- **Faz:** <...>
- **Não faz:** <ex.: o diff mecânico NÃO é seu trabalho — o orquestrador já o rodou>

## 3. Produto: <o artefato verificável>

<!-- O QUE o papel escreve, ONDE, e com que forma. Se o produto tem frontmatter
     obrigatório (ex.: o veredito do momus), fixe os campos com nomes EXATOS aqui:
     um nome por coisa, forma fixa. Um campo que aparece em duas formas em disco vira
     ato de interpretação no gate — e o gate mede o disco, não interpreta prosa. -->

Escreva um arquivo em `<dir>/`. **O arquivo é o produto; a mensagem é só o ponteiro.**

## 4. Ao terminar

```
[TO: <destino>] [FROM: <TOPIC>-<papel>-<n>] [TOPIC: <TOPIC>]
[TYPE: <tipo>] [REF: <path do artefato>]
<resumo de uma linha>
```

<!-- Se efêmero: -->
E **morre**. Não acompanha o que fazem com o produto, não negocia, não revisa a
correção. **O arquivo é a prova; a mensagem não é.** Escreva o arquivo ANTES da mensagem
— um `[TYPE: ...]` sem arquivo correspondente é malformado e será escalado.
