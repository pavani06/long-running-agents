<!--
  TEMPLATE — Dispatch (unidade de trabalho especificada e revisada)
  =====================================================================
  Copie para dispatches/<topico>/dispatch-<slug>.md, apague os comentários e preencha.

  O QUE É: a unidade de trabalho, escrita e REVISADA antes de qualquer execução.
  Carrega o spec, as pré-condições e os gates. Vive em dispatches/.

  A LEI: nada nasce fora do loop. Um dispatch é executado por uma SESSÃO EFÊMERA
  descartável — não pelo papel que o coordena. O coordenador despacha e faz o gate;
  ele não escreve o artefato final.

  O TESTE que o Momus-entrada aplica a este arquivo:
    - As ESCRITAS NOMEADAS são exaustivas e literais? (nada de "e o que mais for
      necessário")
    - O ESCOPO NEGATIVO cobre as tentações concretas deste dispatch?
    - A spec por arquivo é executável por uma sessão SEM contexto, sem interpretar?
    - A VERIFICAÇÃO é mecânica e falsificável, ou é "conferir que ficou bom"?
-->

# Dispatch — <título curto do que este dispatch faz>

**Classe:** `<custodia | produto | ...>`   <!-- governa qual gate se aplica -->
**Status:** <v1 | reemissão de vN, motivo>
**Tipo:** <edição in-place | criação | ...>. **Vault-only?** <sim/não>. Toca <N> arquivos.
**Data:** 2026-01-01
**Tópico:** `<topico>`
**Redigido por:** `<topico>-planner` · **Reportar para:** `<topico>-orchestrator`

---

## Proveniência do texto-base
<!-- Obrigatório se este dispatch EMENDA um artefato já aprovado. Ver
     dispatch-rule-amendment-provenance. Cada linha é um ponteiro medido, com hash. -->

| | |
|---|---|
| **Texto-base a emendar** | `<path>` · `md5 <hash>` · <N> linhas · mtime `<...>` · **medido por <quem>** |
| **Veredito que motiva** | `oracle-reviews/<topico>/<arquivo>.md` · `session: <...>` · **<PASS/FAIL>** |
| **Autoridade da mudança** | `[TYPE: directive]` do operador, <data> — custódia: <onde> |
| **Regras que vinculam** | `dispatch-rule-<...>` · `dispatch-rule-<...>` |

> ## Autoridade única
>
> O executor **trata este arquivo como autoridade única** e ignora qualquer contexto
> anterior da própria sessão. Nada fora deste dispatch autoriza uma escrita. Se algo
> aqui for ambíguo, impossível, ou conflitar com o disco: **pare e emita
> `[TYPE: blocker]`** ao orquestrador, no ponto exato. **Não improvise** —
> substituição de passo do plano no meio da execução é proibida
> (`dispatch-rule-plan-step-substitution`).

---

## 1. Objetivo

<!-- Uma frase. O que este dispatch entrega. Não o porquê (isso é contexto), o QUÊ. -->

## 2. Contexto pinado
<!-- Tudo que o executor precisa saber, INLINADO. Ele não deve ter de buscar a norma
     em facts/ ou nos vereditos — os ponteiros acima existem para o Momus conferir a
     derivação, não para o executor caçar a regra. -->

## 3. Escritas nomeadas (exaustivas e literais)

<!-- A lista FECHADA de arquivos que a execução pode tocar. O gate Camada 1 compara o
     que foi tocado contra ESTA lista. Nada de "e arquivos auxiliares se necessário". -->

1. `<path/exato/1>` — <o que muda, spec por arquivo, executável sem interpretar>
2. `<path/exato/2>` — <...>

## 4. Escopo negativo (o que NÃO tocar)

- **Não** tocar `<...>`.
- **Não** criar `<...>`.
- **Não** <a tentação concreta que este dispatch específico oferece>.

## 5. Pré-condições

- <estado que precisa ser verdade ANTES de executar, verificável em disco>
- <se uma pré-condição é "review feito", ela aponta para o ARTEFATO do review
  (com hash/mtime), nunca para uma frase que o afirma — ver caso-momus-skip>

## 6. Verificação (mecânica e falsificável)

<!-- Como o gate prova DONE. Comandos concretos, não "conferir que ficou bom".
     Camada 1 (SEMPRE): diff de mtime das escritas nomeadas contra a baseline.
     Camada 2 (se aplicável): Momus-saída — obrigatório se tocou facts/ ou roles/,
     código/config/regra, fase destrutiva, >2 escritas, ou PASS-WITH-RESERVATIONS. -->

- **Camada 1:** `find <dir> -newer <baseline>` mostra EXATAMENTE as escritas nomeadas.
- **Camada 2:** <obrigatória? por qual gatilho do dispatch-rule-post-exec-gate?>
- **Gate <N>:** `<comando>` → resultado esperado `<...>` (falsificável)

## 7. O que mudou em relação à versão anterior
<!-- Só em reemissões. A lista literal do delta contra a vN anterior, que permanece
     em disco intacta. -->
