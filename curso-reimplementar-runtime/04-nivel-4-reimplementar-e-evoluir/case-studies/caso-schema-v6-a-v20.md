---
title: "Caso: a migração real v6 → v20 do telemetry.db, e a forense de um número sem timestamp"
type: curriculum-lesson
nivel: 4
aliases: ["caso schema v6 a v20", "forense schema_version", "migração incremental real", "quem escreveu 20"]
tags: [curriculo-conteudo, nivel-4, case-study, schema-version, migration, forense, telemetry, divergencia-de-codebase]
relates-to:
  - "[[vault:sisyphus-runtime/forensics-schema-version-20|Forense: schema_version = 20]]"
  - "[[vault:sisyphus-runtime/facts/_global/index|Facts Index — Global]]"
  - "[[vault:sisyphus-runtime/facts/_global/dispatch-rule-post-exec-gate|Rule: Post-Exec Gate]]"
  - "[[vault:long-running-agents/docs/canonical/durable-fact-selective-history|Durable Fact Selective History]]"
last_updated: 2026-08-13
---

# 🔬 Caso: a migração real v6 → v20
## Como um schema chegou ao 20 sem ninguém digitar "20" — e o que a forense ensina

**Tempo Estimado:** 60 minutos
**Nível:** 4 — Reimplementar e Evoluir
**Pré-requisito:** `03-evoluir-o-schema-global.md`
**Status:** 🟢 ESTUDO DE CASO — baseado na investigação real de 2026-08-11
**Fonte primária:** `[[vault:sisyphus-runtime/forensics-schema-version-20|Forense: schema_version = 20]]`

---

## 📖 Prólogo: a pergunta simples sem resposta simples

Em 2026-08-11 alguém abriu o `telemetry.db` do runtime e olhou a tabela `schema_version`. Ela tem
uma definição de brutal simplicidade:

```sql
CREATE TABLE schema_version ( version INTEGER NOT NULL );
```

Uma coluna. Uma linha. Valor: `20`. **Sem timestamp** — a tabela não guarda *quando* o número foi
escrito. A pergunta que iniciou a investigação era a mais simples possível: *quem escreveu 20, e
quando?* E a resposta demorou uma forense inteira, porque a resposta honesta é: **ninguém escreveu
20 diretamente.** Nenhum arquivo de código, em nenhum commit, contém `VALUES(20)`. Rodar
`git log --all -S "SCHEMA_VERSION = 20"` no repo `~/.config/opencode/` retornou vazio.

O 20 não foi *digitado*. Foi *derivado* — produzido por um loop de migração que subiu o banco de 18
para 20, um degrau de cada vez, na primeira execução de um collector cujo código esperava 20 contra
um banco que estava em 18. Este caso é a anatomia dessa derivação, e cada lição dele é uma regra que
você vai reimplementar.

---

## 🧩 Como o número foi reconstruído: forense sem timestamp

A tabela não datava a escrita, então a investigação teve de datar por **fora** — via backups e mtime
dos arquivos. Essa é a primeira lição transferível: **quando o dado não carrega sua própria
proveniência temporal, o disco à volta dele ainda carrega.** A timeline saiu dos backups:

| Backup | mtime | `schema_version` | Delta |
|---|---|---|---|
| `telemetry.db.qa-backup` | 2026-06-20 | **6** | — |
| `telemetry-backup-20260704-202606.db` | 2026-07-04 20:26 | **15** | 6 → 15 |
| `telemetry.db.bak-2026-07-04` | 2026-07-04 21:04 | **18** | 15 → 18 |
| `telemetry.db` (live) | 2026-08-11 | **20** | 18 → 20 |

Repare no que a tabela mostra: o schema **nunca saltou**. Foi 6 → 15 num período, 15 → 18 noutro, 18
→ 20 no último. Entre cada par há uma sequência de degraus (7, 8, 9, ...). O banco viveu em cada
número intermediário. **Não existe "de 6 para 20"; existe uma escada de catorze degraus, e o DB
pisou em cada um.**

E o cruzamento que fechou a datação: o commit que introduziu `SCHEMA_VERSION = 20` no código
(`316d40a`, "graduation_window table") é de **2026-07-07 03:57**. Logo, a transição 18 → 20 no DB só
pode ter ocorrido *depois* dessa data. O código veio primeiro; o número no banco veio quando o código
rodou. Proveniência reconstruída por triangulação de mtime, não por um campo que alguém teve o
cuidado de gravar.

---

## ⚙️ A cadeia que escreveu o 20 (a mecânica exata)

A forense rastreou a execução real que gravou o número:

```
session-end-hook.sh                (hook do opencode ao fim de uma sessão)
  → collect-session.sh             (SCRIPT_DIR = ~/scripts/telemetry/)
    → node collector.js
      → initDb()  (de ./db.js)
        → SELECT MAX(version) FROM schema_version  → 18
        → 18 < SCHEMA_VERSION (20)  → executa migrations 19 e 20
        → UPDATE schema_version SET version = 19   (grava o degrau 19)
        → UPDATE schema_version SET version = 20   (grava o degrau 20)
```

Três propriedades da lição 03, aqui em carne viva:

- **Ordenada e por degrau.** O loop é `for (targetVersion = fromVersion+1; targetVersion <=
  SCHEMA_VERSION; targetVersion++)`. Ele gravou 19 *e depois* 20 — nunca 20 direto. Se o processo
  caísse entre os dois `UPDATE`, o DB ficaria em 19, um estado válido.
- **Convergente.** Uma vez em 20, a condição de entrada (`current.version < SCHEMA_VERSION`) fica
  falsa, e o loop vira no-op. Re-rodar é seguro.
- **Aditiva e preservadora.** As tabelas das migrations 19 e 20 (`graduation_window`, `budget_phase`,
  colunas novas) foram *adicionadas*. As 216 sessões e 775 `task_calls` que já estavam no banco
  **continuaram lá** — 149 delas criadas depois de 2026-07-07, o que prova que o pipeline seguiu
  ingerindo através da migração. **O schema mudou; o fato durável não se perdeu.** É a lição 03
  inteira, verificada em produção.

---

## 🔀 O achado incômodo: dois codebases, um schema

A investigação começou querendo saber *quem escreveu 20* e terminou revelando um problema mais fundo:
**havia dois codebases divergentes escrevendo no mesmo conceito de schema.**

| Codebase | `SCHEMA_VERSION` | Papel |
|---|---|---|
| `~/scripts/telemetry/` | **20** | Canônico — o que o pipeline operacional roda |
| `~/.config/opencode/operational/telemetry/` | **11** | Stale — último sync foi em 2026-06-30 (v8→v10) |

O collector operacional roda de `~/scripts/telemetry/` (v20), então **o pipeline funciona
normalmente** — a última sessão registrada é de ontem, o crescimento é consistente. Mas qualquer
código que chame `initDb()` do path stale (`~/.config/opencode/`, v11) lança exceção na hora:

```
throw new Error("Unsupported telemetry DB schema version 20; this code supports version 11")
```

E aqui está a beleza da guarda de versão: o código stale **não corrompe o banco**. Ele **para**. A
verificação `current.version > SCHEMA_VERSION` transforma "DB à frente do código" numa recusa limpa,
não numa adivinhação silenciosa. O que ficou bloqueado — testes, uma migração v11 pendente — ficou
bloqueado *ruidosamente*, com uma mensagem exata, em vez de escrever lixo. **A guarda de versão é o
que faz a divergência ser um problema visível em vez de uma corrupção silenciosa.**

> 🔎 **Sutileza que a forense isolou:** a baixa cobertura de uma métrica (`plugin_realtime`) foi
> *erroneamente* atribuída ao schema_version=20. A forense provou que não: o coletor ingere
> normalmente; a causa da baixa cobertura era falta de instrumentação de spans, não o schema. O
> schema=20 é "divergência entre dois codebases", **não** "pipeline quebrado". Diagnosticar a causa
> errada teria "consertado" o schema e deixado o bug real de pé.

---

## 💡 O que este caso ensina para a sua reimplementação

**1. Versionar não é decoração — é o contrato que transforma incompatibilidade em recusa limpa.**
Sem o inteiro `schema_version` e a guarda `> SCHEMA_VERSION`, o código stale teria adivinhado a forma
do banco e escrito lixo. Com ele, parou e apontou. Reimplemente a guarda **antes** de precisar dela.

**2. Migração é uma escada, nunca um salto.** O DB pisou em cada degrau de 6 a 20. Grave cada passo
(`UPDATE` por degrau) para que uma queda no meio deixe um estado válido, não um "meio de 20".

**3. Aditivo preserva; o durável sobrevive à mudança da regra.** As 216 sessões atravessaram catorze
bumps de schema intactas. Se a sua migração perde um fato, ela falhou mesmo "rodando".
(`[[vault:long-running-agents/docs/canonical/durable-fact-selective-history|Durable Fact Selective History]]`)

**4. Quando o dado não carrega proveniência, o disco à volta carrega — mas dependa dela o mínimo.**
A forense conseguiu datar o 20 por mtime de backups. Deu certo, mas foi trabalhoso e probabilístico.
A lição de design: uma tabela `schema_version` com uma coluna `applied_at` teria tornado a forense
um `SELECT`. Ao reimplementar, prefira que o schema **date suas próprias migrações**.

**5. Um schema global disperso em dois codebases é dívida, não redundância.** A causa raiz não foi um
bug de migração — foi *dois lugares* definindo a mesma verdade e um deles ficando para trás. Na sua
reimplementação, o schema global tem **um** dono canônico. A duplicação é a doença; o sync manual é o
sintoma que sempre atrasa.

---

## 🧪 Exercício de leitura forense

1. **Reconstrua a datação.** Com a tabela de backups acima, explique por que a transição 18 → 20
   *tem* de ser posterior a 2026-07-07, e não pode ser inferida com mais precisão que "entre 07-07 e
   08-11". Que dado, se existisse, colapsaria esse intervalo num instante?
2. **Simule a guarda.** Descreva o que teria acontecido se o código stale (v11) **não** tivesse a
   guarda `> SCHEMA_VERSION` e rodasse `initDb()` contra o banco em 20. Qual das duas falhas é
   preferível, e por quê: "parar com erro" ou "rodar adivinhando"?
3. **Ache a causa que quase enganou.** Explique por que atribuir a baixa cobertura de
   `plugin_realtime` ao `schema_version=20` seria diagnosticar a causa errada — e o que se perderia
   ao "consertar" o schema.

**Critério de aprovação (medição de terceiro):** entregue suas respostas a alguém que leia a forense
original (`[[vault:sisyphus-runtime/forensics-schema-version-20|Forense: schema_version = 20]]`) e
confira, seção por seção (b, e, f), se sua reconstrução bate com a evidência que a forense de fato
apresentou. Onde você inferiu além do que o disco sustenta, é achado contra a sua leitura.

---

## 🔗 Para ir fundo

- **Fonte primária (privada, no vault):** `[[vault:sisyphus-runtime/forensics-schema-version-20|Forense: schema_version = 20]]`
- A lição que este caso instancia: `03-evoluir-o-schema-global.md`
- Por que governança se revisa: `[[vault:sisyphus-runtime/facts/_global/dispatch-rule-post-exec-gate|Rule: Post-Exec Gate]]`
- Preservação do durável: `[[vault:long-running-agents/docs/canonical/durable-fact-selective-history|Durable Fact Selective History]]`
