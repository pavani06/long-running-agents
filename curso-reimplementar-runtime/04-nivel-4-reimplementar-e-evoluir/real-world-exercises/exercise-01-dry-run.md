---
title: "Exercício 01 — Reimplementação seca ponta a ponta numa máquina limpa"
type: curriculum-lesson
nivel: 4
aliases: ["dry-run", "reimplementação seca", "exercício ponta a ponta", "exercise 01"]
tags: [curriculo-conteudo, nivel-4, exercicio, dry-run, reimplementacao, medicao-de-terceiro]
relates-to:
  - "[[vault:sisyphus-runtime/facts/_global/dispatch-rule-post-exec-gate|Rule: Post-Exec Gate]]"
  - "[[vault:sisyphus-runtime/roles/momus|Charter — Momus]]"
last_updated: 2026-08-13
---

# 🏗️ Exercício 01 — Reimplementação seca ponta a ponta
## De um diretório vazio a um ciclo do loop fechado, provável por um terceiro

**Tempo Estimado:** 3–5 horas
**Nível:** 4 — Reimplementar e Evoluir
**Pré-requisito:** Lições `01`, `02` e `03` do Nível 4; os templates de `08-tools-templates/`
**Status:** 🔴 EXERCÍCIO-CHAVE — só "passa" por medição de terceiro, nunca por auto-aprovação

---

## 🎯 O que você vai provar

Que você consegue pegar uma **máquina limpa** (ou um diretório temporário — `mktemp -d` serve) e, sem
copiar o vault de referência, levantar um `sisyphus-runtime` mínimo que fecha **um** ciclo do loop de
forma que outra pessoa reconstrua a cadeia inteira lendo só o disco.

Este exercício é o casamento das três lições: você monta o **núcleo mínimo** (01), roda o **bootstrap**
(02) e faz **uma evolução de schema** (03). O critério não é "funciona na minha máquina" — é "um
terceiro reproduz cada elo".

> ⚠️ **A regra que o exercício encarna.** *Afirmação sobre estado não vira durável sem passar por
> medição de terceiro.* Você **não aprova o próprio dry-run.** Esse é o ponto pedagógico inteiro — o
> mesmo achado central que o sistema descobriu a caro (Nível 3) é o seu critério de nota aqui.

---

## 📋 As quatro fases

### Fase A — O esqueleto (núcleo mínimo, lição 01)

1. `mktemp -d` (ou uma VM/container limpo). Este é o seu vault novo.
2. Copie **a árvore** de `[[08-tools-templates/skeleton/README.md]]` — pastas vazias, nada de fatos.
3. Instale a porta única de acesso (`obsidian-eval` ou o seu equivalente). Nenhuma escrita no vault
   pode acontecer por fora dela.

**Portão de fase A:** um `find` mostra a árvore mínima, vazia. **Nenhum fato importado do vault de
referência** — se aparecer um `constraints.md` com "prometheus-exporter bloqueia wal_checkpoint",
você importou memória alheia e a fase A falhou.

### Fase B — Os papéis e o primeiro registry (bootstrap, lição 02)

1. Escreva os quatro charters de núcleo em `roles/` (`orchestrator`, `planner`, `momus`, `executor`)
   com `[[08-tools-templates/templates/charter.template.md]]`. Escreva `momus` e `orchestrator`
   **antes** de qualquer dispatch.
2. Escreva o `meta/registry.md` **magro** — uma linha, o bootstrap em si.

**Portão de fase B:** o split-brain existe como *identidade de sessão*, não só como dois arquivos. O
`momus.md` declara que nasce limpo, sem o contexto de quem planejou.

### Fase C — Um ciclo completo (o loop fecha)

1. Escreva **um** dispatch com `[[08-tools-templates/templates/dispatch.template.md]]`, cuja escrita
   nomeada seja *um* fato durável em `facts/_global/` (use `[[08-tools-templates/templates/durable-fact.template.md]]`).
2. Rode o loop inteiro:
   - momus-**entrada** (sessão nova) → veredito **em arquivo** em `oracle-reviews/`;
   - execução efêmera, com **baseline de mtime + listagem** tomada como primeiro ato;
   - gate **Camada 1** (diff mecânico das escritas nomeadas);
   - momus-**saída** obrigatório (a escrita tocou `facts/` — governança se revisa);
   - `verify` → atualização do `registry.md`, **por último**.

**Portão de fase C:** a cadeia `dispatch → veredito-entrada → execução → veredito-saída → fato` está
inteira em disco, e cada elo casa por hash/mtime.
(`[[vault:sisyphus-runtime/facts/_global/dispatch-rule-post-exec-gate|Rule: Post-Exec Gate]]`)

### Fase D — Uma evolução de schema (lição 03)

1. Evolua o schema de governança: adicione **um** novo `kind` de fato durável, ou **um** campo
   obrigatório novo num artefato — aditivo, com fronteira de legado explícita (`schema: vN`).
2. Faça-o por um dispatch dedicado, com momus-saída obrigatório.
3. Prove que os fatos anteriores (o da fase C) **continuam válidos** sem o campo novo — não os
   converta.

**Portão de fase D:** a mudança de schema tem proveniência (texto-base com hash, veredito que a
motivou), e nenhum fato durável anterior foi perdido ou reescrito.

---

## ✅ Critério de aprovação — medição de terceiro (obrigatória)

O dry-run **não passa por você dizer que passou.** Ele passa assim:

1. Você entrega a um terceiro **apenas o vault produzido** — sem narração, sem "deixa eu te
   explicar". O disco fala por si ou não fala.
2. O terceiro, lendo só o disco, tem de:
   - **(a)** reconstruir a cadeia da fase C — apontar, para o fato durável final, o dispatch que o
     autorizou, o veredito-entrada e o veredito-saída, cada um por hash/mtime;
   - **(b)** confirmar que o momus-saída é **prova** (arquivo de veredito com sessão, findings,
     localização), não uma frase de aprovação sem lastro;
   - **(c)** confirmar que a evolução de schema da fase D é aditiva e não perdeu nenhum fato anterior.
3. Se em qualquer ponto o terceiro precisar **te perguntar** "mas isto rodou mesmo?", esse elo é
   promessa, não prova — e o dry-run **não passou** nessa fase.

> 🔴 **O modo de falha que este critério pega é o do `caso-momus-skip`.** Se você colou uma frase de
> aprovação em vez de deixar o veredito como arquivo verificável, o terceiro vai bater exatamente
> nesse elo. Todo mundo cola a frase-promessa em algum momento — o critério existe porque *você
> também vai*, e o objetivo é que o disco te pegue antes de o hábito virar sistema.

---

## 🧾 O que entregar (o pacote de aprovação)

- O caminho do vault produzido (o `mktemp -d` ou o container).
- **Nada além dele.** Se você sentir vontade de anexar um `README explicando`, essa vontade é o
  sintoma: o disco deveria bastar. Anexe, se quiser, apenas a *lista de arquivos* da cadeia da fase
  C, cada um com seu `md5sum` e `mtime` — para o terceiro conferir, não para substituir a leitura
  dele.

---

## 🔗 Para ir fundo

- As três lições que este exercício casa: `01-nucleo-reproduzivel-minimo.md`, `02-bootstrap-nova-maquina.md`, `03-evoluir-o-schema-global.md`
- A regra do gate: `[[vault:sisyphus-runtime/facts/_global/dispatch-rule-post-exec-gate|Rule: Post-Exec Gate]]`
- O charter do adversário: `[[vault:sisyphus-runtime/roles/momus|Charter — Momus]]`
- **Solução guiada:** `solutions/solution-01-dry-run.md`
