---
title: "Bootstrap numa máquina nova: do esqueleto vazio ao primeiro ciclo fechado"
type: curriculum-lesson
nivel: 4
aliases: ["bootstrap", "nova máquina", "primeiro dispatch", "do zero ao loop"]
tags: [curriculo-conteudo, nivel-4, reimplementacao, bootstrap, skeleton, primeiro-dispatch, registry, roles]
relates-to:
  - "[[vault:sisyphus-runtime/roles/momus|Charter — Momus]]"
  - "[[vault:sisyphus-runtime/facts/_global/dispatch-rule-post-exec-gate|Rule: Post-Exec Gate]]"
  - "[[vault:sisyphus-runtime/facts/_global/dispatch-rule-confidentiality|Rule: Confidencialidade]]"
  - "[[vault:long-running-agents/docs/canonical/split-brain-planning-review|Split-Brain Planning/Review]]"
  - "[[vault:long-running-agents/docs/canonical/owner-of-no-role-design|Owner-of-No-Role]]"
last_updated: 2026-08-13
---

# 🚀 Bootstrap numa máquina nova
## Do esqueleto vazio ao primeiro ciclo do loop fechado com honestidade

**Tempo Estimado:** 90 minutos (leitura) + a reimplementação em si
**Nível:** 4 — Reimplementar e Evoluir
**Pré-requisito:** `01-nucleo-reproduzivel-minimo.md`
**Status:** 🟢 PRÁTICO — é o passo a passo que a lição 01 tornou possível

---

## 📖 Prólogo: o problema do primeiro gate

Todo bootstrap tem o mesmo paradoxo: o gate é a peça que impede o sistema de mentir, mas quando você
está construindo o *primeiro* gate, não há gate para verificá-lo. O runtime real viveu isso — o
`dispatch-rule-post-exec-gate` nasceu numa "decisão 7 do bootstrap de roles", num dispatch que
instalava as próprias regras que o revisariam. A camada que escreve as regras é a que mais precisa
ser revisada, e no bootstrap ela ainda não tem revisor.

A resposta do sistema não foi "confie no operador nesta primeira vez". Foi **encadear**: o primeiro
gate mecânico (Camada 1, o diff) não precisa de julgamento — precisa só de um `find` e um `md5sum`.
Ele funciona no minuto zero, antes de qualquer momus existir. Você começa o bootstrap pelo gate que
não depende de ninguém lembrar de nada, e só depois liga os que dependem de julgamento.

Este é o fio que atravessa o passo a passo abaixo: **construa na ordem em que cada peça pode ser
verificada pela peça anterior.** Nunca instale um componente cuja correção você não tem como medir
ainda.

---

## 🧠 Os cinco passos, na ordem verificável

### Passo 1 — Criar o esqueleto (a árvore, não os arquivos)

Copie a estrutura de diretórios de `[[08-tools-templates/skeleton/README.md]]` — **a única pasta do
curso feita para ser copiada**. Ela é a árvore mínima da lição 01, materializada:

```
facts/_global/   state/current/   sessions/   catalog/   meta/   roles/   dispatches/   traces/
```

> ⚠️ **Copie a árvore, não os fatos.** O esqueleto é pastas vazias (mais um índice comentado). Os
> `facts/` são específicos da sua máquina e do seu trabalho — eles nascem do loop, não do `.zip`. Um
> reimplementador que copia os fatos duráveis do vault de referência importou memória alheia: fatos
> como "prometheus-exporter bloqueia wal_checkpoint" (ver `constraints.md` do vault real) são
> verdades *daquela* máquina, não da sua.

**Verificação deste passo:** a árvore existe e está vazia (exceto os READMEs do skeleton). Um `find`
confirma. Este é o único passo cuja verificação é trivial — aproveite, porque a partir daqui cada
verificação exige o gate que você ainda está montando.

### Passo 2 — Bootstrap dos papéis (os charters)

Escreva os quatro charters de núcleo em `roles/`, usando
`[[08-tools-templates/templates/charter.template.md]]`:

- `roles/orchestrator.md` — o *owner-of-no-role*
  (`[[vault:long-running-agents/docs/canonical/owner-of-no-role-design|Owner-of-No-Role]]`).
- `roles/planner.md` — gera o spec.
- `roles/momus.md` — o adversário efêmero
  (`[[vault:sisyphus-runtime/roles/momus|Charter — Momus]]` é a referência viva).
- `roles/executor.md` — executa na sessão efêmera.

**A ordem importa e não é arbitrária.** Escreva o `momus.md` e o `orchestrator.md` *antes* de
escrever qualquer dispatch, porque o gate que revisará seu primeiro dispatch é definido por eles. Se
você escrever o dispatch primeiro, terá um dispatch sem revisor — o furo do prólogo.

> 🔴 **O split-brain é uma restrição de *identidade de sessão*, não só de arquivo.** Ter
> `planner.md` e `momus.md` como arquivos separados não basta. O que precisa ser verdade é que a
> *sessão* que roda o momus nasce limpa, sem o contexto da que planejou
> (`[[vault:long-running-agents/docs/canonical/split-brain-planning-review|Split-Brain Planning/Review]]`).
> Se na sua reimplementação o mesmo processo planeja e revisa, os arquivos separados são decoração.

**Verificação deste passo:** cada charter declara escritas nomeadas, escopo negativo e um produto
verificável? Aqui você já pode rodar o primeiro momus-entrada *manualmente* — leia um charter com a
pergunta "uma sessão sem contexto executaria isto sem interpretar?".

### Passo 3 — Escrever o primeiro `meta/registry.md`

O painel vivo da meta-camada. No minuto zero ele tem uma linha: o bootstrap em si. Lembre da lição
01: o registry é **derivado e não-autoritativo**. Você o escreve por conveniência operacional, não
porque ele é fonte de verdade — a verdade são os charters que você acabou de escrever.

> ⚠️ **Não faça o registry preceder os arquivos.** Um erro comum é redigir um registry rico
> ("tópicos ativos: runtime, telemetria, ...") antes de os artefatos existirem. Isso inverte a
> autoridade: o disco passa a *dever* bater com o registry, quando é o registry que deve derivar do
> disco. Escreva o registry magro e deixe-o crescer atrás dos fatos.

**Verificação deste passo:** cada linha do registry aponta para um arquivo que existe? Se aponta
para algo que ainda não existe, é promessa, não estado.

### Passo 4 — O primeiro dispatch

Agora, e só agora, escreva um dispatch usando
`[[08-tools-templates/templates/dispatch.template.md]]`. O primeiro dispatch canônico é pequeno de
propósito — o objetivo não é fazer trabalho, é **provar que o loop fecha**. Bom candidato: "criar o
primeiro fato durável em `facts/_global/`", que exercita escrita no substrato governado.

O dispatch precisa carregar, no mínimo: a **classe**, as **escritas nomeadas** (exaustivas e
literais — nada de "e o que mais for necessário"), o **escopo negativo**, e a **verificação
mecânica e falsificável**.

> 💡 **Escolha um primeiro dispatch cuja escrita seja em `facts/`.** Pela regra do post-exec-gate,
> *qualquer escrita em `facts/` ou `roles/` torna o momus-saída obrigatório* — "governança se
> revisa". Você quer que seu primeiro ciclo exercite o caminho *caro* do gate, não o trivial, porque
> é o caminho caro que prova que o split-brain está de pé.

**Verificação deste passo:** o dispatch passa por um momus-entrada (sessão nova, limpa)? O veredito
foi escrito **como arquivo** em `oracle-reviews/`, e a mensagem é só o ponteiro?

### Passo 5 — Fechar o ciclo: execução efêmera, gate, verify

- **Execução:** uma sessão efêmera, descartável, executa o dispatch aprovado. O executor toma a
  **baseline de mtime + listagem como primeiro ato** (é isto que torna a Camada 1 mensurável depois).
- **Gate Camada 1:** o orquestrador compara os arquivos tocados contra as escritas nomeadas. Tocou
  exatamente o nomeado → passou. Tocou algo fora, ou faltou → escala.
  (`[[vault:sisyphus-runtime/facts/_global/dispatch-rule-post-exec-gate|Rule: Post-Exec Gate]]`)
- **Gate Camada 2:** como a escrita foi em `facts/`, um momus-saída **novo** revisa o conteúdo
  contra o spec. Não o momus-entrada — ele já ancorou no plano que aprovou.
- **Verify → registry:** só depois de o gate passar, o registry é atualizado para refletir o novo
  fato. O registry vem **por último**, atrás do disco.

**Verificação deste passo — e do bootstrap inteiro:** um terceiro consegue, lendo só o vault que
você produziu, reconstruir a cadeia `dispatch → veredito-entrada → execução → veredito-saída →
fato`? Se a cadeia está toda em disco e casa por hash/mtime, o loop fechou. Se algum elo é uma
frase sem prova, você reproduziu o `caso-momus-skip` no seu primeiro dia.

---

## 🔎 O que quase todo bootstrap erra

**Erro 1 — construir o vault antes do loop.** É o erro-mãe da lição 01. Você acaba com um museu.
Antídoto: os passos acima nunca escrevem um fato sem um dispatch que o autorize.

**Erro 2 — o primeiro gate que lê a promessa.** No afã de ver o ciclo fechar, você escreve um gate
que confere um campo `review: done` em vez de medir o disco. Ele "passa" e você comemora — instalou a
classe de defeito mais recorrente do sistema no minuto zero. Antídoto: a Camada 1 é `find` +
`md5sum`, não leitura de campo.

**Erro 3 — importar a memória alheia.** Copiar os `facts/` do vault de referência. Antídoto: o
esqueleto é a árvore vazia; os fatos nascem do *seu* loop, na *sua* máquina.

**Erro 4 — o registry como autoridade.** Redigir um registry rico e deixar o disco dever bater com
ele. Antídoto: registry magro, sempre atrás dos arquivos.

> 🔒 **Nota de confidencialidade.** O `sisyphus-runtime` **nunca vira repositório git** — contém
> requests verbatim e decisões que não podem ser expostas
> (`[[vault:sisyphus-runtime/facts/_global/dispatch-rule-confidentiality|Rule: Confidencialidade]]`).
> Seu vault reimplementado herda isso: é local-por-máquina, privado. O que você compartilha é o
> *procedimento* (este curso), nunca o vault.

---

## 🧪 Exercício

**Contexto.** Você tem uma máquina limpa (ou um diretório temporário) e o `08-tools-templates/`.

1. **Bootstrap seco até o passo 3.** Crie a árvore do skeleton, escreva os quatro charters e o
   registry magro. **Não escreva nenhum fato ainda.**
2. **O primeiro ciclo.** Escreva um dispatch cuja escrita nomeada seja *um* fato durável em
   `facts/_global/`. Rode-o pelo loop inteiro: momus-entrada → execução efêmera (com baseline) →
   gate Camada 1 → momus-saída (obrigatório, porque tocou `facts/`) → registry.
3. **Prove a cadeia.** Produza a lista de arquivos que, juntos, demonstram que o ciclo fechou
   honesto — cada um com hash/mtime — de modo que um terceiro reproduza cada elo.

**Critério de aprovação (medição de terceiro):** entregue a outra pessoa **apenas o vault** que você
produziu — sem explicação oral. Ela deve reconstruir a cadeia `dispatch → veredito → fato` só lendo
o disco. Se ela precisar te perguntar "mas o momus rodou mesmo?", algum elo é promessa, não prova, e
o exercício não passou. Você não narra a cadeia; ela tem de estar no disco.

> 💡 **Solução guiada:** `real-world-exercises/solutions/solution-01-dry-run.md`

---

## 🔗 Para ir fundo

- O esqueleto a copiar: `[[08-tools-templates/skeleton/README.md]]`
- Os templates dos artefatos: `[[08-tools-templates/templates/]]`
- A regra do gate que fecha o ciclo: `[[vault:sisyphus-runtime/facts/_global/dispatch-rule-post-exec-gate|Rule: Post-Exec Gate]]`
- O charter do adversário: `[[vault:sisyphus-runtime/roles/momus|Charter — Momus]]`
- Por que o vault é privado: `[[vault:sisyphus-runtime/facts/_global/dispatch-rule-confidentiality|Rule: Confidencialidade]]`
- **Próxima lição:** `03-evoluir-o-schema-global.md` — o segundo objetivo do operador.
