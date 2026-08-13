---
title: "Solução 01 — Reimplementação seca: uma trilha comentada, com os erros que ela evita"
type: curriculum-lesson
nivel: 4
aliases: ["solução dry-run", "solution 01", "trilha comentada reimplementação"]
tags: [curriculo-conteudo, nivel-4, solucao, dry-run, reimplementacao, gate, medicao-de-terceiro]
relates-to:
  - "[[vault:sisyphus-runtime/facts/_global/dispatch-rule-post-exec-gate|Rule: Post-Exec Gate]]"
  - "[[vault:sisyphus-runtime/roles/momus|Charter — Momus]]"
  - "[[vault:sisyphus-runtime/facts/_global/dispatch-rule-amendment-provenance|Rule: Amendment Provenance]]"
last_updated: 2026-08-13
---

# ✅ Solução 01 — Reimplementação seca, comentada
## Uma trilha que fecha o ciclo, e os quatro erros que ela existe para evitar

**Tempo Estimado:** leitura 40 minutos
**Nível:** 4 — Reimplementar e Evoluir
**Pré-requisito:** ter tentado `exercise-01-dry-run.md` primeiro
**Status:** 🟢 SOLUÇÃO — uma trilha válida, não a única

---

> ⚠️ **Leia depois de tentar.** Esta solução não é um gabarito para copiar — é uma trilha comentada
> que mostra *por que* cada passo tem a forma que tem. O critério de aprovação continua sendo a
> medição de terceiro; nenhuma solução escrita te aprova.

---

## 🅰️ Fase A — o esqueleto, e o erro de importar memória

```bash
VAULT=$(mktemp -d)          # o vault novo, limpo
cd "$VAULT"
mkdir -p facts/_global state/current sessions catalog meta roles dispatches traces
```

**Comentário.** A tentação, aqui, é `cp -r` do vault de referência "para ganhar tempo". É o **Erro 3**
da lição 02 (importar memória alheia). Os `facts/` do runtime real contêm verdades *daquela* máquina
— por exemplo, o `constraints.md` real diz *"prometheus-exporter mantém conexão readonly bloqueando
wal_checkpoint"*. Isso é uma cicatriz de uma máquina específica, não uma lei do universo. Importá-la é
começar o seu sistema mentindo sobre o próprio estado.

**Portão A verificado:**
```bash
find "$VAULT" -type f    # deve listar só os READMEs do skeleton; zero fatos
```

## 🅱️ Fase B — papéis antes de dispatch, e o split-brain como sessão

Escreva `roles/orchestrator.md`, `roles/planner.md`, `roles/momus.md`, `roles/executor.md` a partir
de `[[08-tools-templates/templates/charter.template.md]]`. **Ordem:** `momus` e `orchestrator`
primeiro.

**Comentário — o paradoxo do primeiro gate (prólogo da lição 02).** Você está escrevendo os charters
que definem o gate que revisará o seu primeiro dispatch. Se escrever o dispatch antes, ele nasce sem
revisor. A saída não é "confie no operador desta vez"; é começar pela **Camada 1**, que é `find` +
`md5sum` e não depende de nenhum momus existir ainda.

O `meta/registry.md` sai **magro**:

```markdown
# Registry — meta
- bootstrap: roles de núcleo escritos (orchestrator, planner, momus, executor). Ver roles/.
```

**Erro 4 evitado** (registry como autoridade): uma linha, apontando para arquivos que já existem.
Nada de "tópicos ativos: ..." antes de os tópicos existirem.

**Comentário sobre o split-brain.** Ter dois arquivos (`planner.md`, `momus.md`) não é o split-brain
— é a *aparência* dele. O que o portão B mede é a cláusula, dentro do `momus.md`, de que a **sessão**
que roda o momus nasce sem o contexto de quem planejou. O `[[vault:sisyphus-runtime/roles/momus|Charter — Momus]]`
real abre com "reuso enviesa" exatamente por isto.

## 🅲 Fase C — o ciclo, e o erro do gate que lê a promessa

**Dispatch** (`dispatches/dispatch-primeiro-fato.md`), do `dispatch.template.md`. Escrita nomeada
única e literal: `facts/_global/paths.md`. Escopo negativo explícito ("não tocar roles/, não criar
índice"). Verificação mecânica.

**O loop, elo por elo:**

1. **momus-entrada** → escreve `oracle-reviews/2026-08-13-primeiro-fato-entrada.md`, veredito `PASS`.
   O veredito é **arquivo**; a mensagem `[verdict]` é só o ponteiro.
2. **Baseline** — o executor, como primeiro ato:
   ```bash
   find facts/_global -type f -printf '%p %T@\n' | sort > /tmp/baseline.txt
   ```
3. **Execução efêmera** cria `facts/_global/paths.md` (e nada mais).
4. **Gate Camada 1** — o orquestrador:
   ```bash
   find facts/_global -type f -printf '%p %T@\n' | sort > /tmp/after.txt
   diff /tmp/baseline.txt /tmp/after.txt    # exatamente 1 arquivo novo, o nomeado
   ```
   Tocou exatamente a escrita nomeada → passou. Tocou algo fora, ou faltou → escala.
5. **momus-saída** (obrigatório — tocou `facts/`) → `oracle-reviews/2026-08-13-primeiro-fato-saida.md`.
   Um momus **novo**, não o de entrada.
6. **verify → registry** — só agora o `registry.md` ganha a linha do novo fato.

> 🔴 **O Erro 2 (o gate que lê a promessa) mora no passo 4.** A versão errada seria conferir um campo
> `review: done` no dispatch em vez de rodar o `diff`. Ela "passa" e instala, no minuto zero, a classe
> de defeito do `caso-momus-skip`. A Camada 1 correta **mede o disco** — `find` + `diff` de mtime —
> nunca lê um campo. (`[[vault:sisyphus-runtime/facts/_global/dispatch-rule-post-exec-gate|Rule: Post-Exec Gate]]`)

**Portão C verificado:** a cadeia `dispatch-primeiro-fato.md → veredito-entrada → paths.md →
veredito-saída` existe em disco, cada arquivo com `md5sum`+`mtime`, e o registry só menciona o fato
*depois* de o gate ter passado.

## 🅳 Fase D — evolução de schema aditiva, sem reescrever prova

Suponha que você queira que todo fato durável novo carregue um campo `evidence_verified: bool`.

1. **Dispatch dedicado** — não "de passagem". Escreve a nova convenção em
   `facts/_global/durable-fact-schema.md`, com proveniência
   (`[[vault:sisyphus-runtime/facts/_global/dispatch-rule-amendment-provenance|Rule: Amendment Provenance]]`):
   o texto-base, o veredito que motivou, a autoridade.
2. **Fronteira do legado.** A regra diz: *fatos com `schema: v2` carregam `evidence_verified`; fatos
   sem `schema:` são legado — leia como estão, não converta.* O `paths.md` da fase C **não** ganha o
   campo à força.
3. **momus-saída obrigatório** (mexeu em `facts/`).
4. **Prova de preservação:** o `paths.md` continua um fato válido sem o campo novo.

> 🔴 **O Erro da reescrita de prova (lição 03).** A tentação é editar `paths.md` para "uniformizar" e
> pôr `evidence_verified: true` nele. Isso apaga a evidência de que ele nasceu sob o schema antigo. A
> uniformidade cosmética custa a auditabilidade. O passo 3 do exercício pede que você faça isso *de
> propósito* e depois reverta, para sentir o que se perde.

## 🤝 A entrega — e por que ela é magra

Você entrega **só o `$VAULT`**. Se você sentiu vontade de anexar um documento explicando a cadeia,
essa vontade é o diagnóstico: o disco deveria bastar. A única anexação legítima é a *lista* dos
arquivos da cadeia C com `md5sum`+`mtime` — para o terceiro **conferir**, não para ele **acreditar**.

**O que um bom terceiro vai fazer** (e por que sua solução tem de sobreviver a isto):

- Pegar o `paths.md`, achar o dispatch que o autorizou, e casar o hash do veredito-saída com a sessão
  que o escreveu. Se o veredito-saída for uma frase colada no dispatch em vez de um arquivo em
  `oracle-reviews/`, ele para aqui e reprova a fase C.
- Contar os fatos antes e depois da fase D. Se algum sumiu, ou se o `paths.md` foi reescrito, reprova
  a fase D.

Se a sua trilha sobrevive a esse terceiro sem você abrir a boca, o dry-run passou. Se em algum ponto
você precisou explicar, aquele elo era promessa — e o exercício inteiro existe para te ensinar a
diferença antes que ela vire um incident.

---

## 🧭 Os quatro erros, em uma tabela

| Erro | Onde aparece | O antídoto na trilha |
|---|---|---|
| Importar memória alheia | Fase A (`cp -r` do vault de referência) | Árvore vazia; fatos nascem do *seu* loop |
| Gate que lê a promessa | Fase C, passo 4 | Camada 1 = `find` + `diff` de mtime, nunca campo |
| Registry como autoridade | Fase B | Registry magro, sempre atrás do disco |
| Reescrever prova | Fase D | Schema novo governa artefato novo; legado não se converte |

---

## 🔗 Para ir fundo

- O enunciado: `../exercise-01-dry-run.md`
- A regra do gate: `[[vault:sisyphus-runtime/facts/_global/dispatch-rule-post-exec-gate|Rule: Post-Exec Gate]]`
- A cicatriz que o critério de terceiro pega: `caso-momus-skip` (Nível 3)
- Proveniência da emenda de schema: `[[vault:sisyphus-runtime/facts/_global/dispatch-rule-amendment-provenance|Rule: Amendment Provenance]]`
