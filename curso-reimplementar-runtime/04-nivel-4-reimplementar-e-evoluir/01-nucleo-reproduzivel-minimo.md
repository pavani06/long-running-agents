---
title: "O núcleo reproduzível mínimo: o que precisa existir para o sistema rodar"
type: curriculum-lesson
nivel: 4
aliases: ["núcleo mínimo", "checklist de reimplementação", "essencial vs acessório", "minimum reproducible core"]
tags: [curriculo-conteudo, nivel-4, reimplementacao, nucleo-minimo, loop, gate, substrato, obsidian-eval, checklist]
relates-to:
  - "[[vault:sisyphus-runtime/roles/momus|Charter — Momus]]"
  - "[[vault:sisyphus-runtime/facts/_global/dispatch-rule-post-exec-gate|Rule: Post-Exec Gate]]"
  - "[[vault:sisyphus-runtime/facts/_global/index|Facts Index — Global]]"
  - "[[vault:long-running-agents/docs/canonical/owner-of-no-role-design|Owner-of-No-Role]]"
  - "[[vault:long-running-agents/docs/canonical/split-brain-planning-review|Split-Brain Planning/Review]]"
last_updated: 2026-08-13
---

# 🧬 O núcleo reproduzível mínimo
## O que precisa existir para o sistema rodar — e o que é só conveniência

**Tempo Estimado:** 75 minutos
**Nível:** 4 — Reimplementar e Evoluir
**Pré-requisito:** Níveis 1–3 completos (substrato, máquina e governança)
**Status:** 🟢 FUNDAÇÃO — é o checklist que separa "copiei um vault" de "reimplementei o sistema"

---

## 📖 Prólogo: o vault que alguém copiou e que não rodava

Imagine que você recebe um `.zip` do `sisyphus-runtime` inteiro — todos os `facts/`, todos os
`roles/`, o `meta/registry.md`, os `dispatches/`. Você descompacta noutra máquina e roda. **Nada
acontece.** Não porque falta um arquivo: porque o vault não é o sistema. O vault é o *rastro* que
o sistema deixou ao rodar. Copiar o rastro não reconstrói quem andou.

O sistema é um **procedimento** — o loop `dispatch → review → gate → execução efêmera → verify →
registry` — que, ao rodar, materializa arquivos. Se você copia os arquivos mas não instancia o
procedimento, tem um museu, não uma máquina. Este é o erro que o Nível 4 inteiro existe para
prevenir, e esta primeira lição é o inventário do que, de fato, precisa estar de pé para o
procedimento rodar.

A pergunta que organiza tudo: **se eu apagasse isto, o loop ainda fecharia um ciclo honesto?** Se
sim, é acessório. Se não, é núcleo. Vamos passar cada peça por essa pergunta.

---

## 🧠 O conceito: cinco coisas têm de existir juntas

O núcleo reproduzível mínimo tem **cinco componentes**, e a palavra "juntas" é a lição: cada um
sozinho é inerte. O substrato sem o loop é um diretório de notas; o loop sem gate é uma esteira que
mente para si mesma; o gate sem papéis separados é um construtor avaliando o próprio trabalho.

### 1. O loop operacional — o procedimento, não os arquivos

`dispatch → review → gate → execução efêmera → verify → registry`. **Não há porta lateral de
escrita no vault.** Todo artefato que existe no runtime nasceu passando por aqui, ou é anomalia a
escalar. Se na sua reimplementação existe *qualquer* caminho pelo qual um arquivo entra em `facts/`
ou `roles/` sem passar por um dispatch revisado e um gate, você não reimplementou o loop — você
construiu um vault com uma convenção decorativa.

**Teste de existência:** peça a si mesmo "qual foi o dispatch que autorizou este arquivo?" para
três arquivos ao acaso. Se algum não tem resposta, o loop tem furo.

### 2. A topologia de papéis — cabeças separadas, não funções de um script

Os charters em `roles/`. O mínimo indispensável não é "todos os sete papéis"; é a **separação que
torna o gate honesto**:

- **orchestrator** — coordena o loop e faz o gate. *Owner-of-no-role*: não faz o trabalho, roteia-o
  e mede o disco. (`[[vault:long-running-agents/docs/canonical/owner-of-no-role-design|Owner-of-No-Role]]`)
- **planner** — produz o spec/plano.
- **momus** — o avaliador adversarial, cabeça **separada** do planner
  (`[[vault:sisyphus-runtime/roles/momus|Charter — Momus]]`). É efêmero: nasce, revisa um artefato,
  escreve o veredito, morre.
- **executor** — executa o dispatch aprovado numa **sessão efêmera** descartável.

Os outros três — **meta**, **protocol**, **launch-convention** — são núcleo de *governança* e
entram formalmente na lição 02 e no Nível 3; mas a topologia mínima *para um ciclo fechar honesto*
são estes quatro, porque é entre eles que vive o **split-brain**
(`[[vault:long-running-agents/docs/canonical/split-brain-planning-review|Split-Brain Planning/Review]]`).

**Por que a separação é núcleo e não organização:** se o planner pode *declarar* que foi avaliado,
o split-brain colapsa — ele virou avaliador de si mesmo com uma frase. A cicatriz que prova isso é o
`caso-momus-skip` do Nível 3. Colapsar planner e momus não é "simplificar"; é remover a única coisa
que impede o sistema de mentir para si.

### 3. A disciplina de gate — medir o disco, não ler a promessa

Esta é a peça que quase todo reimplementador subestima, porque parece um detalhe de implementação.
Não é. É **a lei física do sistema**. Um gate:

- **Camada 1 — diff mecânico de escritas nomeadas: SEMPRE.** O conjunto de arquivos tocados é
  comparado, por mtime + listagem, contra a lista de escritas nomeadas do dispatch. Incondicional —
  nenhuma frase dispensa. (`[[vault:sisyphus-runtime/facts/_global/dispatch-rule-post-exec-gate|Rule: Post-Exec Gate]]`)
- **Camada 2 — julgamento adversarial (momus-saída): escalonado.** Sobe só quando a Camada 1 não
  resolve, e nunca *no lugar* dela.

O núcleo aqui é a Camada 1 e a regra que ela encarna: **texto-base**. Um gate não pergunta "o
artefato afirma X?"; pergunta "o disco demonstra X de forma que um terceiro reproduza a medição?".
Se você reimplementar gates que leem campos de aprovação em vez de medir o disco, seu sistema tem a
classe de defeito mais recorrente do runtime embutida de fábrica.

### 4. O substrato de persistência — facts / state / registry

A camada de dados do Nível 1, agora vista como *o que o loop precisa poder ler e escrever*:

- **`facts/_global/`** — os fatos duráveis: como o sistema lembra entre sessões. Tipados por
  frontmatter (`type: durable-fact`, `kind`, `confidence`, `valid_from`). Núcleo.
- **`state/current/`** — o estado corrente (handoffs, mandato da sessão viva). Núcleo — sem ele, o
  loop não tem "onde estou".
- **`meta/registry.md`** — o painel vivo da meta-camada. **Derivado e não-autoritativo**: abrigo,
  não autoridade. Núcleo *operacional*, mas com uma ressalva que é meio-curso: **o disco vence**.
  Se o registry diverge dos arquivos, os arquivos são a verdade e a divergência é anomalia.

> ⚠️ **Armadilha clássica:** tratar o `registry.md` como fonte de verdade porque é conveniente
> lê-lo. Ele é conveniência; a autoridade está nos arquivos que ele resume.

### 5. `obsidian-eval` — a única porta de acesso ao vault

A camada de acesso. Toda leitura/escrita de conteúdo de nota passa por ela — **nunca pelo app
Obsidian**. Prefira `query` (predicado sobre frontmatter) a `search` (texto). Sem esta porta única,
você perde a propriedade que torna o resto verificável: que *todo* acesso é interceptável,
tipável e auditável. É o que faz "medir o disco" ser uma operação e não uma metáfora.

---

## 📋 O checklist: núcleo vs. acessório

Passe cada item pela pergunta do prólogo — *"se eu apagasse isto, o loop ainda fecharia um ciclo
honesto?"*.

### ✅ Núcleo (sem isto, não há sistema)

| Componente | Encarnação mínima | O que quebra sem ele |
|---|---|---|
| **Loop** | Um caminho único `dispatch → gate → execução efêmera → verify` | Escrita entra sem autorização; nada é rastreável |
| **Split-brain** | `planner` ≠ `momus` (cabeças separadas) | Construtor aprova o próprio trabalho; gate vira teatro |
| **Owner-of-no-role** | `orchestrator` roteia e mede, não executa | Coordenador escreve o artefato e some o gate |
| **Gate Camada 1** | Diff mecânico de escritas nomeadas, sempre | O modo de falha mais caro (plan-step-substitution) passa |
| **Texto-base** | Gate mede disco (hash/mtime), não lê campo | Afirmação de estado sem prova vira "durável" |
| **`facts/_global/`** | Fatos duráveis tipados | Sistema não lembra entre sessões |
| **`state/current/`** | Estado/handoff corrente | Loop não sabe "onde está" |
| **`obsidian-eval`** | Porta única de acesso ao vault | Acesso não é auditável; medir o disco vira metáfora |

### 🟡 Acessório (útil, mas o loop fecha sem)

| Componente | Por que é acessório | Quando adicionar |
|---|---|---|
| **`meta/registry.md`** | Derivado; o disco vence. O loop fecha lendo os arquivos | Assim que houver mais de um tópico vivo |
| **`traces/`** | Telemetria e forense — enriquece, não habilita | Quando você quiser *medir* o sistema (ver `schema_version`) |
| **`catalog/`, `recon/`, `evidence/`, `oracle-reviews/`** | Pastas de produto/insumo de dispatches concretos | Conforme os dispatches os criarem |
| **7 papéis completos** | 4 fecham um ciclo honesto; os outros 3 governam | Ao introduzir governança (lição 02 e Nível 3) |
| **`reminders/`, `prompts/`** | Ergonomia operacional | Nunca são pré-condição de correção |

> 💡 **Regra de leitura da tabela:** um acessório nunca deve virar pré-condição de um gate. Se seu
> gate depende do `registry.md` para decidir PASS/FAIL, você promoveu um acessório a autoridade — e
> reabriu o buraco do "disco vence".

---

## 🔎 Por que "juntas" é a palavra que carrega a lição

Um reimplementador apressado constrói na ordem errada: primeiro o vault bonito (fácil, tangível),
depois "quando der" o gate (chato, invisível quando funciona). O resultado é um sistema que **parece**
o runtime por semanas e então, num dia qualquer, incorpora um artefato errado porque o gate nunca
mediu o disco de verdade. O `registry.md` do vault real documenta o dia em que *três* sessões
distintas cometeram a mesma falha de "afirmei ter feito o que não fiz" — **com a regra à vista**.

A conclusão empírica que foi ao operador — e que é a espinha do Nível 4 inteiro:

> **Afirmação sobre estado não vira durável sem passar por medição de terceiro.** E a regra dessa
> classe, se existir, não pode depender de alguém lembrar — porque papéis com a regra à vista já
> falharam nela no mesmo dia. Tem de estar **no gate**.

Por isso o núcleo mínimo não é uma lista de pastas. É uma lista de **restrições estruturais** que,
juntas, tornam o sistema incapaz de mentir para si mesmo. Tire uma e o sistema volta a poder.

---

## 🧪 Exercício

**Contexto.** Você vai reimplementar o runtime, mas antes precisa provar que entende o que é núcleo.

1. **Inventário reverso.** Rode `obsidian-eval` (ou `find`) sobre o vault de referência e liste dez
   arquivos ao acaso de `facts/` e `roles/`. Para cada um, responda: *qual dispatch o autorizou?* e
   *qual gate mediria a sua correção?*. Marque os que você não consegue responder — são os furos do
   seu modelo mental.
2. **Corte cada peça, uma de cada vez.** Escreva, para cada um dos cinco componentes de núcleo, uma
   frase de uma linha: *"sem este, o próximo ciclo do loop consegue mentir assim: ___"*. Se você não
   consegue completar a frase, ou o componente é acessório, ou você ainda não entendeu por que é
   núcleo.
3. **Defenda um acessório.** Escolha `meta/registry.md`. Escreva por que ele é *conveniência* e não
   *autoridade*, e descreva um bug concreto que nasce de tratá-lo como fonte de verdade.

**Critério de aprovação (medição de terceiro, coerente com o achado central):** seu inventário do
passo 1 só "passa" quando **outra pessoa** pega três dos seus arquivos, tenta responder as duas
perguntas de forma independente, e chega às mesmas respostas que você. Divergência = seu modelo do
loop ainda tem furo. Você não aprova o próprio inventário.

---

## 🔗 Para ir fundo

- Charter que encarna o split-brain: `[[vault:sisyphus-runtime/roles/momus|Charter — Momus]]`
- A disciplina de gate em duas camadas: `[[vault:sisyphus-runtime/facts/_global/dispatch-rule-post-exec-gate|Rule: Post-Exec Gate]]`
- O índice de fatos que o substrato precisa: `[[vault:sisyphus-runtime/facts/_global/index|Facts Index — Global]]`
- Padrão canônico do orquestrador: `[[vault:long-running-agents/docs/canonical/owner-of-no-role-design|Owner-of-No-Role]]`
- Padrão canônico da separação: `[[vault:long-running-agents/docs/canonical/split-brain-planning-review|Split-Brain Planning/Review]]`
- **Próxima lição:** `02-bootstrap-nova-maquina.md` — de checklist a máquina em pé.
