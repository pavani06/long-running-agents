---
name: two-implementations-goal-test
description: "Heuristica para distinguir goals de specs disfarcadas: 'Duas implementacoes completamente diferentes conseguiriam satisfazer isso?' Se sim, e um goal. Se nao, e uma spec escondida no campo errado. Usar durante a escrita ou revisao de intents, como gate pre-flight antes do Grill-Me, ou quando o agente esta recebendo instrucoes que parecem 'implemente X com Y usando Z' em vez de 'entregue o outcome W'. Dispara com: 'two implementations test', 'teste das duas implementacoes', 'goal vs spec', 'isso e goal ou spec', 'spec disfarcada', 'spec in disguise', 'goal purity test', 'is this a goal', 'distinguir goal de spec', 'goal classification', 'method-bound goal', 'outcome vs implementation', 'spec disguised as goal'."
license: MIT
compatibility: opencode
metadata:
  audience: all-agents
  workflow: alignment
  priority: high
  source: "The Anatomy of Intent - ICE in IDSD (Kapil Viren Ahuja, 2026)"
---

## What I Do

Eu aplico uma unica pergunta de revisao para classificar uma sentenca candidata como goal ou spec disfarcada: **"Duas implementacoes completamente diferentes conseguiriam satisfazer isso?"**

Meu trabalho nao e gerar implementacoes -- e aplicar o teste mais barato e mais decisivo para garantir que o campo Goal do intent descreve um outcome, nao um metodo. Cada sentenca que passa no teste preserva o espaco de decisao do agente. Cada sentenca que falha revela uma spec que foi escrita no lugar errado e deve ser reclassificada como Context, Constraint, ou removida do Goal.

O veredito e binario:

- **GOAL**: duas (ou mais) implementacoes materialmente diferentes podem satisfazer a sentenca. Ex: "Build a service that handles the product catalog" -- poderia ser Go + PostgreSQL, Node + MongoDB, Rust + SQLite. O agente decide.
- **SPEC DISFARCADA**: so uma implementacao (ou uma familia estreita) satisfaz. Ex: "Build a Go microservice with gRPC and PostgreSQL" -- a sentenca escolheu stack, protocolo, storage. Nao ha decisao para o agente tomar; ele e um typist.

## When to Use Me

Carregue esta skill quando:

- Voce esta escrevendo ou revisando o campo Descricao (Goal) de um intent de cinco partes e quer garantir que ele descreve um outcome, nao um metodo
- O ciclo de alinhamento ([[.opencode/skills/intent-five-part-primitive/SKILL|intent-five-part-primitive]], [[docs/canonical/grill-me-alignment-interview|Grill-Me]]) esta para iniciar e os goals candidatos precisam de purificacao antes da entrevista
- O agente esta recebendo instrucoes que ditam stack, protocolos, nomes de classe, ou escolhas de storage -- o sintoma classico de spec-in-disguise goal
- Voce suspeita que o humano escreveu o metodo no goal porque o outcome estava claro na cabeca, mas a solucao ja estava formada (failure pattern #1 documentado na fonte)
- Uma tarefa chega com descricao do tipo "implementa X usando Y com Z" -- a presenca de implementacao no goal e o trigger
- Voce esta treinando alguem (ou um agente) a escrever intents de qualidade e precisa de um exemplo concreto da diferenca entre goal e spec
- O [[.opencode/skills/goal-atomicity-split/SKILL|goal-atomicity-split]] identificou multiplos intents, e cada fragmento precisa ser classificado como goal ou spec antes de seguir

Nao use quando:

- A ferramenta ou stack e uma constraint externa genuina (ex: "deve usar PostgreSQL porque o banco corporativo e PostgreSQL"). Neste caso, nao e spec disfarcada -- e constraint que pertence ao campo Constraints, e voce deve remove-la do Goal, nao questiona-la.
- O intent e puramente exploratorio ("descubra qual stack funciona melhor para X") -- o goal e descobrir, nao entregar, e o two-implementations test nao se aplica a metas de investigacao
- A tarefa e um hotfix ou incidente SEV1/SEV2 onde a urgencia operacional substitui a pureza do goal (mas registre o desvio para o postmortem)
- O agente ja esta em execucao e o intent ja foi validado -- o teste e pre-flight, nao mid-execution

## The Anti-Pattern

```
ANTI-PATTERN: Spec escrita no campo Goal porque o outcome esta claro na cabeca
do humano, que instintivamente escreve a solucao como se fosse o problema.

Cenario:
  1. Um stakeholder quer um catalogo de produtos. Na cabeca dele, a solucao
     e "um microservico em Go com gRPC e PostgreSQL" -- ele ja decidiu tudo.
  2. O intent chega como: "Build a Go microservice with gRPC and PostgreSQL
     for the product catalog."
  3. O agente recebe isso como Goal. Nao ha decisao para tomar: a stack
     (Go), o protocolo (gRPC), e o storage (PostgreSQL) estao decididos.
     O agente e um typist, nao um decision-maker.
  4. O agente implementa exatamente o que foi pedido. Go, gRPC, PostgreSQL.
     O codigo compila. Os testes passam.
  5. Seis meses depois: o time descobre que um servico REST em Node com
     MongoDB teria custado 1/3 do esforco e resolvido o mesmo problema.
     Mas o agente nunca considerou isso -- o Goal nao deixou.

Consequencia:
  - O agente perdeu a oportunidade de tomar decisoes de design que o harness
    confiou a ele
  - O intent virou spec sem que ninguem percebesse -- o pior drift possivel
    porque e invisivel (a spec se parece com um goal, so que nao e)
  - O time pagou o custo da disciplina de escrever intent sem receber o
    beneficio (o agente nao usou julgamento proprio)
  - A ilusao de "estamos fazendo intent-driven" enquanto o workflow real
    e spec-driven com outro nome
```

## The Pattern

```
PATTERN: Uma pergunta unica aplicada como gate pre-flight antes que o Goal
seja entregue ao agente.

Fluxo:

  Goal candidato chega
       │
       ▼
  ┌─────────────────────────────────────────────────────────┐
  │ PASSO 1: Leia o goal candidato em voz alta               │
  │                                                         │
  │ "O que esta escrito no campo Goal do intent?"            │
  └─────────────────────────────────────────────────────────┘
       │
       ▼
  ┌─────────────────────────────────────────────────────────┐
  │ PASSO 2: Pergunte: "Duas implementacoes COMPLETAMENTE    │
  │          DIFERENTES conseguiriam satisfazer isso?"       │
  │                                                         │
  │ "Completamente diferentes" significa diferenças em:      │
  │   - Stack (linguagem, framework, runtime)                │
  │   - Protocolo (REST vs gRPC vs GraphQL vs eventos)       │
  │   - Storage (SQL vs NoSQL vs file-based vs in-memory)    │
  │   - Arquitetura (monolith vs microservices vs serverless)│
  │   - Padroes (MVC vs event-driven vs CQRS vs pipeline)    │
  │                                                         │
  │ NAO e "completamente diferente" se so muda:              │
  │   - Nome de variavel ou funcao                           │
  │   - Lib dentro da mesma stack (ex: Express vs Fastify)   │
  │   - Organizacao de arquivos ou estilo de codigo          │
  └─────────────────────────────────────────────────────────┘
       │
       ▼
  ┌─────────────────────────────────────────────────────────┐
  │ PASSO 3: Aplique o veredito                              │
  │                                                         │
  │ Se SIM (duas+ implementacoes satisfazem):                │
  │   → GOAL. A sentenca descreve um outcome. O agente       │
  │     tem espaco de decisao para escolher COMO entregar.   │
  │     Continue.                                            │
  │                                                         │
  │ Se NAO (so uma implementacao ou familia estreita):       │
  │   → SPEC DISFARCADA. A sentenca descreve um metodo.      │
  │     Reclassifique:                                       │
  │     - Extraia o outcome real (o que o usuario quer)      │
  │     - Mova escolhas de implementacao para Context        │
  │     - Mova restricoes de stack para Constraints          │
  │     - Reescreva o Goal como outcome puro                 │
  └─────────────────────────────────────────────────────────┘
       │
       ▼
  ┌─────────────────────────────────────────────────────────┐
  │ PASSO 4: Se reclassificado, valide o novo Goal           │
  │                                                         │
  │ O novo Goal tambem passa no two-implementations test?    │
  │   → SIM: Goal purificado, pronto para o agente            │
  │   → NAO: Ainda ha spec escondida. Repita.                │
  └─────────────────────────────────────────────────────────┘
```

### Exemplo Concreto: Spec → Goal

```
ORIGINAL (spec disfarcada):
  "Build a Go microservice with gRPC and PostgreSQL
   for the product catalog."

Two-implementations test:
  Daria pra implementar isso em Node + REST + MongoDB?
  → A sentenca original diz "Go", "gRPC", "PostgreSQL".
    Nao, nao daria. A sentenca escolheu tudo.
  → SPEC DISFARCADA.

RECLASSIFICACAO:
  Outcome real: "Um catalogo de produtos que o frontend
  pode consultar."
  → Goal: "Build a service that handles the product catalog."
  → Stack (Go) → removido (o agente decide, ou vira Constraint
    se Go for obrigatorio por razao externa)
  → Protocolo (gRPC) → removido (ou Context se for padrao do time)
  → Storage (PostgreSQL) → removido (ou Constraint se houver
    politica de banco)

NOVO GOAL (purificado):
  "Build a service that handles the product catalog —
   clients can search, filter, and retrieve product
   information by ID."

Two-implementations test no novo goal:
  Daria pra implementar em Go + gRPC + PostgreSQL? Sim.
  E em Node + REST + MongoDB? Sim.
  E em Rust + GraphQL + SQLite? Sim.
  → GOAL. O agente pode decidir COMO.
```

### Casos Ambiguos

Nem toda sentenca e trivial de classificar. Quando houver duvida:

| Cenario | Verdicto | Racional |
|---|---|---|
| "Build a REST API for orders" | SPEC | "REST" e escolha de protocolo. O outcome e "clients can create and query orders" -- o protocolo e detalhe de implementacao. Se REST e constraint externa, mova para Constraints. |
| "Add authentication to the checkout flow" | GOAL | Pode ser JWT + middleware, OAuth + gateway, session + cookie. Varias implementacoes satisfazem. |
| "Migrate the user database from MySQL to PostgreSQL" | SPEC | So uma implementacao satisfaz (MySQL → PostgreSQL). Isso nao e um goal -- e uma tarefa de migracao com metodo fixo. Se ela precisa ser feita, e um intent com metodo deterministico, nao um goal que o agente pode decidir como alcancar. |
| "Reduce checkout latency to under 200ms" | GOAL | Pode ser caching, query optimization, CDN, async processing, database index. Varias estrategias satisfazem. |
| "Use React hooks for state management" | SPEC | Nem parece goal. E uma instrucao de implementacao. Pertence ao Context (padroes do time) ou nao pertence ao intent. |

## Implementation Rules

1. **O teste e binario, nao probabilistico.** "Maybe two implementations could..." nao e suficiente. Voce precisa conseguir nomear duas implementacoes concretas e materialmente diferentes que ambas satisfazem a sentenca. Se nao consegue nomea-las, a sentenca e spec.

2. **"Completamente diferente" tem criterio objetivo.** Stack, protocolo, storage, arquitetura, e padroes sao os eixos de diferenciacao. Mudar o nome da funcao ou trocar Express por Fastify nao conta como implementacao diferente. O teste existe para verificar se o agente tem latitude de design real -- nao cosmética.

3. **Spec rejeitada nao e descartada -- e reclassificada.** O Goal purificado nao perde informacao. As escolhas de implementacao removidas do Goal sao roteadas para o destino correto: padroes do time → Context, restricoes externas → Constraints, instrucoes de coding → removidas ou documentadas no harness.

4. **O teste nao substitui julgamento humano, mas o reduz a uma pergunta.** Casos ambiguos existem (ex: "REST API" quando o time so usa REST). A pergunta força a explicitacao: se REST e uma decisao real do time, documente como Context. Se nao e, deixe o agente decidir. O teste revela a decisao escondida.

5. **Aplique o teste ANTES do Grill-Me, nao durante.** Goals purificados tornam a entrevista de alinhamento mais produtiva porque cada pergunta do Grill-Me opera sobre um outcome real, nao sobre uma spec mal rotulada. spec-in-disguise goals desperdicam o tempo da entrevista.

6. **O teste compoe com o Goal Atomicity Split.** Primeiro, split goals por conjuncao (goal-atomicity-split). Depois, para cada goal atomico resultante, aplique o two-implementations test. A ordem importa: um goal com "and" pode ter uma parte que e goal e outra que e spec -- o split revela isso.

## Integration with Existing Repo Infrastructure

O two-implementations test funciona como gate de pureza do Goal, complementando a infraestrutura de alinhamento e decomposicao:

| Componente Existente | Como o Two-Implementations Test complementa |
|---|---|
| [[.opencode/skills/intent-five-part-primitive/SKILL|intent-five-part-primitive]] | O primitivo de cinco partes tem o campo Descricao (Goal). O two-implementations test valida se o conteudo desse campo e de fato um goal, nao uma spec. E um gate de qualidade que opera sobre o campo antes da completude gate. |
| [[docs/canonical/grill-me-alignment-interview|Grill-Me Alignment Interview]] | O Grill-Me entrevista o requisitante sobre escopo, arquitetura e constraints. Se o Goal e uma spec disfarcada, a entrevista pergunta sobre a implementacao em vez do outcome. O two-implementations test purifica o Goal antes da entrevista, garantindo que as perguntas do Grill-Me operam sobre outcomes. |
| [[.opencode/skills/goal-atomicity-split/SKILL|goal-atomicity-split]] | O atomicity split quebra intents multi-goal em fragmentos atomicos. O two-implementations test classifica cada fragmento como goal ou spec. O fluxo composto: split → test → purifica → entrega. |
| [[docs/canonical/ice-craft-separation|ICE Craft Separation]] | A separacao de crafts define que o humano escreve o Goal. O two-implementations test garante que o humano escreveu um outcome no campo Goal, nao um metodo -- preservando a separacao que a arquitetura exige. |
| [[docs/canonical/vertical-slice-issue-generation|Vertical Slice Issue Generation]] | Issues geradas como fatias verticais herdam o Goal do intent. Se o Goal e uma spec disfarcada, a issue gerada e uma tarefa de implementacao sem decisao -- o oposto de uma fatia vertical com comportamento observavel. |
| [[docs/canonical/generator-evaluator|Generator-Evaluator]] | O Generator recebe o Goal como contrato de trabalho. Se o Goal e uma spec, o Generator nao tem o que decidir -- vira um executor deterministico, desperdicando a capacidade de geracao que a arquitetura confia a ele. |
| [[docs/canonical/shared-design-concept-handoff|Shared Design Concept Handoff]] | O handoff transporta o Goal purificado para artefatos downstream. Um Goal que passou no two-implementations test garante que o conceito transportado e um outcome, nao uma decisao de design prematura. |

## Quality Gates

Antes de declarar um Goal como validado pelo two-implementations test, verifique:

- [ ] O Goal foi lido em voz alta e o teste foi aplicado explicitamente (nao assumido)
- [ ] Duas implementacoes concretas foram nomeadas -- com stack, protocolo e storage diferentes -- que ambas satisfazem o Goal
- [ ] As implementacoes nomeadas sao materialmente diferentes (nao apenas cosmeticamente: trocar Express por Fastify nao conta)
- [ ] Se o teste falhou (SPEC DISFARCADA): o outcome real foi extraido e reescrito como Goal puro
- [ ] As escolhas de implementacao removidas do Goal foram roteadas para o destino correto (Context, Constraints, ou removidas)
- [ ] O novo Goal purificado tambem passa no two-implementations test (validacao recursiva)
- [ ] O Goal purificado nao contem nomes de ferramentas, protocolos, stacks, classes ou padroes de implementacao -- a menos que sejam constraints externas documentadas
- [ ] O teste foi aplicado ANTES que o agente recebesse o intent (pre-flight, nao mid-execution)

## References

- [[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-analysis|Anatomy of Intent Analysis]]:174 -- Failure pattern #1: Spec-in-disguise goal e two-implementations test como mitigacao
- [[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-patterns|Anatomy of Intent Patterns]]:60-81 -- Pattern 3: Two-Implementations Goal Test
- [[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-classification|Anatomy of Intent Classification]]:85-110 -- Classificacao como Missing (Medium integration value)
- [[docs/canonical/intent-five-part-primitive|Intent as Five-Part Primitive]] -- estrutura de cinco campos onde o Goal (Descricao) e validado
- [[docs/canonical/grill-me-alignment-interview|Grill-Me Alignment Interview]] -- entrevista de alinhamento que recebe o Goal purificado
- [[docs/canonical/ice-craft-separation|ICE Craft Separation]] -- separacao de crafts que o teste protege
- [[docs/canonical/generator-evaluator|Generator-Evaluator]] -- Generator que recebe o Goal como contrato de trabalho
- [[.opencode/skills/goal-atomicity-split/SKILL|goal-atomicity-split]] -- decomposicao de goals que precede o two-implementations test

---

*Created: 2026-06-14 | Source: The Anatomy of Intent - ICE in IDSD — Pattern 3 (Missing, Medium value)*
