---
title: "Evoluir o schema global: versionar, migrar e promover sem quebrar fatos duráveis"
type: curriculum-lesson
nivel: 4
aliases: ["evoluir o schema", "schema global", "migrations", "schema_version", "promover padrão"]
tags: [curriculo-conteudo, nivel-4, schema, schema-version, migration, durable-fact, promover-padrao, novo-papel]
relates-to:
  - "[[vault:sisyphus-runtime/facts/_global/index|Facts Index — Global]]"
  - "[[vault:sisyphus-runtime/facts/_global/dispatch-rule-post-exec-gate|Rule: Post-Exec Gate]]"
  - "[[vault:sisyphus-runtime/roles/momus|Charter — Momus]]"
  - "[[vault:sisyphus-runtime/facts/_global/dispatch-rule-amendment-provenance|Rule: Amendment Provenance]]"
  - "[[vault:long-running-agents/docs/canonical/durable-fact-selective-history|Durable Fact Selective History]]"
last_updated: 2026-08-13
---

# 🧬 Evoluir o schema global
## O segundo objetivo do operador: mudar as regras sem quebrar o que o sistema já sabe

**Tempo Estimado:** 90 minutos
**Nível:** 4 — Reimplementar e Evoluir
**Pré-requisito:** `02-bootstrap-nova-maquina.md`
**Status:** 🟡 O SEGUNDO ALVO — reimplementar mantém o sistema vivo; evoluir o schema o faz crescer

---

## 📖 Prólogo: o schema que chegou ao 20 sem ninguém digitar "20"

Em 2026-08-11, alguém investigou por que o `telemetry.db` do runtime estava em `schema_version = 20`.
A tabela tinha uma única linha, sem timestamp: só o número `20`. A pergunta simples — *quem escreveu
20?* — não tinha resposta simples. Porque **ninguém escreveu 20**. Nenhum arquivo de código continha
`VALUES(20)`. O número foi produzido por um *loop de migração* que subiu o DB de 18 para 20, um passo
de cada vez, na primeira vez que um collector com `SCHEMA_VERSION = 20` rodou contra um banco em 18.

Essa é a forma madura de evoluir um schema, e o caso completo é o
`case-studies/caso-schema-v6-a-v20.md`. O que interessa ao prólogo é a moral: **um schema evoluído
não é um schema reescrito.** O DB nunca foi "de 18 para 20" num salto. Foi 18 → 19 → 20, cada passo
uma migração que preservou tudo que já estava lá. Ninguém apagou as 216 sessões e recomeçou com o
schema novo. Os fatos sobreviveram à mudança da regra que os organiza.

Este é o princípio inteiro desta lição, e ele vale igual para o `telemetry.db` (schema de dados) e
para os `facts/` e `roles/` (schema de *governança*): **evoluir o schema = migrar entre versões
preservando os fatos duráveis.** Se sua evolução quebra um fato que o sistema já aprendeu, você não
evoluiu o schema — você amputou a memória.

---

## 🧠 O conceito: schema tem versão, e versão tem migração

### O que é "o schema global" no runtime

Há dois schemas, e a lição vale para os dois:

1. **O schema de dados** — a estrutura do `telemetry.db` (tabelas, colunas, índices), versionada por
   um inteiro em `schema_version`. Evolui por *migrations* de código.
2. **O schema de governança** — a forma dos `type: durable-fact`, dos charters, dos vereditos, das
   `dispatch-rule-*`. Não tem um inteiro global, mas tem versionamento *local* onde importa: o
   `momus.md` do vault carrega `schema: v1` no bloco do veredito, e trata "vereditos escritos antes
   desta emenda **não são migrados**" como fronteira do legado.

Os dois obedecem à mesma disciplina. Vamos ao caso do inteiro primeiro, porque é o mais nítido.

### Versionamento: o número não é decorativo, é o contrato de compatibilidade

`schema_version = 20` significa uma coisa operacional precisa: código que espera `< 20` deve
**recusar-se a rodar** contra este DB, não adivinhar. O runtime real tem isso literal:

> `if (current.version === null || current.version > SCHEMA_VERSION) throw new Error("Unsupported
> telemetry DB schema version ...")`

Ou seja: se o DB está numa versão *à frente* do código, o código para — não corrompe. E se está
*atrás*, o loop de migração o sobe. O número é o que torna essa decisão mecânica em vez de
adivinhação. **Um schema sem versão não é evoluível** — você nunca sabe se um dado veio de antes ou
depois de uma mudança.

### Migrations: incrementais, ordenadas, um passo de cada vez

A regra de ouro que o caso v6→v20 grava: você nunca migra de A para C. Você migra A → B → C, e cada
degrau é uma migração idempotente e ordenada. No runtime:

```
for (let targetVersion = fromVersion + 1; targetVersion <= SCHEMA_VERSION; targetVersion++) {
  aplica_migration(targetVersion);
  UPDATE schema_version SET version = targetVersion;   // grava o degrau ANTES do próximo
}
```

Três propriedades que você tem de reproduzir na sua reimplementação:

- **Ordenada.** Sempre `fromVersion + 1`. Nunca pula degraus.
- **Persistente por degrau.** O `UPDATE` grava *cada* passo. Se a máquina cai entre 19 e 20, o DB
  fica em 19 — um estado válido — e o próximo run continua de 19. Não há "meio de 20".
- **Convergente.** Rodar o loop num DB já em 20 é no-op (`20 <= 20` é falso na entrada seguinte). A
  migração é segura de re-rodar.

### O paralelo em governança: adicionar um novo tipo de fato ou papel

Quando você evolui o *schema de governança* — adicionar um `kind` novo ao `durable-fact`, um novo
papel em `roles/`, um novo campo obrigatório num veredito — a "migração" é o mesmo movimento:

1. **Aditivo antes de destrutivo.** Adicione o campo/tipo novo como *opcional* primeiro. Os fatos
   antigos continuam válidos sem ele. (O `momus.md` faz exatamente isto: campos aposentados "não
   aparecem em veredito **novo**", mas os antigos "leia-os como estão, não os converta".)
2. **A fronteira do legado é explícita.** `schema: v1` marca o que é novo; a ausência de `schema:`
   marca o legado. Você **não migra prova**: reescrever um veredito antigo é reescrever a evidência
   sobre a qual dois gates repousam.
3. **Um passo por dispatch.** Cada mudança de schema é um dispatch próprio, revisado. Nunca "de
   passagem", junto com outra coisa.

---

## 🔒 As três restrições que impedem a evolução de quebrar a memória

### Restrição 1 — Governança se revisa (o gate mais duro se aplica)

Pela regra do post-exec-gate, **qualquer escrita em `facts/` ou `roles/` torna o momus-saída
obrigatório**. Evoluir o schema global É escrever em `facts/`/`roles/` por definição. Logo, **toda
evolução de schema passa pelo caminho caro do gate.**
(`[[vault:sisyphus-runtime/facts/_global/dispatch-rule-post-exec-gate|Rule: Post-Exec Gate]]`)

Por quê, na palavra do próprio vault: um erro em código é um bug; um erro numa `dispatch-rule-*` ou
num charter é **um gate silenciosamente afrouxado que se propaga por todos os ciclos futuros, e que
nenhum gate posterior detecta — porque o gate posterior é justamente o que foi alterado.** A camada
que escreve as regras é a que mais precisa ser revisada.

### Restrição 2 — Proveniência da emenda (de onde veio a mudança)

Toda alteração de um artefato de governança já aprovado carrega sua **proveniência**: qual texto-base
(com hash, tamanho, mtime), qual veredito a motivou, qual a autoridade da mudança
(`[[vault:sisyphus-runtime/facts/_global/dispatch-rule-amendment-provenance|Rule: Amendment Provenance]]`).
Isto é o que torna uma migração de schema *auditável* — o análogo, na governança, do que o loop de
`UPDATE schema_version` faz no DB: cada degrau deixa rastro.

> 🔴 **A cicatriz que fundou esta restrição.** Uma frase de aprovação asseverou "review incorporado"
> sem o review ter acontecido (`caso-momus-skip`, Nível 3). Se uma mudança de schema entra sob uma
> afirmação de estado não medida, você propaga um schema não-revisado por todos os ciclos futuros. A
> proveniência é o que fecha esse buraco.

### Restrição 3 — Preservar o durável (a migração não perde fato)

O princípio do prólogo, operacionalizado. Uma migração — de dados ou de governança — que descarta um
fato durável falhou, mesmo que "rode". O padrão canônico
`[[vault:long-running-agents/docs/canonical/durable-fact-selective-history|Durable Fact Selective History]]`
governa o que se preserva e como. No DB, isso é "as 216 sessões continuam lá após o 20". Na
governança, é "o veredito legado se lê como está, não se converte".

---

## 📋 Playbook: como evoluir o schema, passo a passo

**Cenário A — bump do schema de dados (nova tabela/coluna na telemetria):**

1. Incremente `SCHEMA_VERSION` no código, **e escreva a migração do degrau novo** (`N-1 → N`).
2. A migração é aditiva e idempotente: cria a tabela/coluna, não destrói dado existente.
3. O loop de migração sobe qualquer DB antigo, um degrau de cada vez, gravando cada passo.
4. Guarde a compatibilidade: código velho contra DB novo **para**, não adivinha.
5. **Verifique num backup real** — pegue um DB numa versão antiga e rode a migração; conte as linhas
   antes e depois. Fato preservado = contagem não regride.

**Cenário B — novo `kind` de fato durável, ou novo papel:**

1. Escreva um dispatch dedicado (nunca "de passagem").
2. Adicione o tipo/papel como aditivo; os fatos antigos permanecem válidos.
3. Se um campo novo é obrigatório *daqui pra frente*, marque a fronteira (`schema: vN`) e declare o
   legado como não-migrável.
4. Passe pelo momus-saída obrigatório (governança se revisa).
5. Atualize o `index.md` de `facts/` — mas só *depois* de o gate passar (o índice é derivado).

**Cenário C — promover um padrão (de prática recorrente a regra):**

1. Junte a evidência de que o padrão já convergiu na prática. (No vault real: o campo `dispatch:`
   "convergiu sozinho para o formato certo, sem o schema existir" — 20 caminhos contra 1 id legado
   *antes* de a regra ser escrita.)
2. Escreva a regra descrevendo o que a prática já faz, não uma aspiração nova.
3. Marque a fronteira do legado e **não converta** os artefatos antigos.
4. Momus-saída obrigatório.

> 💡 **A promoção mais honesta descreve o presente, não legisla o futuro.** Um padrão que já
> convergiu sozinho é forte porque a evidência de que funciona já está no disco. Uma regra que
> *inventa* um formato que ninguém usa ainda é uma aposta, e o vault trata aposta e fato diferente.

---

## 🔎 A armadilha da reescrita de prova

O reflexo natural, ao evoluir um schema, é "limpar": migrar os artefatos antigos para o formato novo
para que tudo fique uniforme. **O runtime proíbe isso onde o artefato é prova.** Um veredito antigo,
um incident, um fato durável com `valid_from` no passado — reescrevê-los para o schema novo apaga a
evidência de *quando* e *sob que regra* eles foram produzidos. A uniformidade cosmética custa a
auditabilidade, e a auditabilidade é o que torna o sistema incapaz de mentir sobre a própria
história.

A regra prática: **schema novo governa artefato novo; o legado se lê, não se converte.** A fronteira
(o `schema: vN`, o `valid_from`, a ausência do campo novo) é informação, não sujeira a limpar.

---

## 🧪 Exercício

**Contexto.** Seu runtime reimplementado está em pé (lição 02) e você precisa evoluir o schema.

1. **Bump de dados.** Adicione uma coluna a uma tabela da sua telemetria. Escreva a migração do
   degrau `N-1 → N`, incremente a versão, e prove — contra um backup numa versão antiga — que a
   contagem de linhas **não regride** após a migração. Documente o antes/depois com números.
2. **Promoção de padrão.** Escolha um campo de frontmatter que na sua prática já aparece em duas
   formas. Meça a distribuição (quantas de cada forma, em disco). Escreva a regra que promove a forma
   majoritária, **marcando a fronteira do legado** — e mostre que sua regra descreve o presente, não
   inventa o futuro.
3. **Tente a reescrita errada.** Migre *um* artefato legado para o schema novo. Depois argumente, em
   três linhas, que evidência você acabou de apagar — e reverta.

**Critério de aprovação (medição de terceiro):** para o passo 1, entregue a outra pessoa o backup
antigo e o seu código de migração. Ela roda a migração de forma independente e confere que (a) a
versão sobe um degrau de cada vez e (b) nenhum fato foi perdido — a contagem que ela mede bate com a
sua. Se ela não consegue reproduzir a preservação, sua migração destrói memória. Você não certifica a
própria migração.

---

## 🔗 Para ir fundo

- O estudo de caso completo: `case-studies/caso-schema-v6-a-v20.md`
- O gate que toda evolução de schema aciona: `[[vault:sisyphus-runtime/facts/_global/dispatch-rule-post-exec-gate|Rule: Post-Exec Gate]]`
- A proveniência da emenda: `[[vault:sisyphus-runtime/facts/_global/dispatch-rule-amendment-provenance|Rule: Amendment Provenance]]`
- A fronteira do legado num schema real: `[[vault:sisyphus-runtime/roles/momus|Charter — Momus]]` (bloco `schema: v1`)
- O índice de fatos a atualizar por último: `[[vault:sisyphus-runtime/facts/_global/index|Facts Index — Global]]`
- Padrão canônico da preservação: `[[vault:long-running-agents/docs/canonical/durable-fact-selective-history|Durable Fact Selective History]]`
