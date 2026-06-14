---
name: goal-atomicity-split
description: "Decompoe intents multi-goal em sentencas atomicas: um goal = uma sentenca, sem 'and', sem 'then', sem 'and also'. Escaneia o Goal por conjuncoes e coordenação, split em intents atomicos independentes, e opcionalmente estabelece dependencias entre eles. Previne que agentes otimizem para uma parte do goal enquanto abandonam silenciosamente a outra. Usar durante a escrita de intents, como pre-flight antes do Grill-Me, ou quando o agente entrega outputs que 'meio que resolvem' mas falham em um dos outcomes. Dispara com: 'goal atomicity', 'atomicidade do goal', 'split goal', 'goal splitting', 'dividir goal', 'um goal por sentenca', 'one goal one sentence', 'no and in goal', 'multi-goal intent', 'conjunction split', 'separar goals', 'goal decomposition', 'intentos atomicos', 'goal coordination', 'coordinated intents'."
license: MIT
compatibility: opencode
metadata:
  audience: all-agents
  workflow: alignment
  priority: high
  source: "The Anatomy of Intent - ICE in IDSD (Kapil Viren Ahuja, 2026)"
---

## What I Do

Eu aplico uma regra simples e implacavel: **um goal = uma sentenca, sem "and".** Escaneio o campo Goal (Descricao) do intent por conjuncoes, coordenacao, e clausulas multi-outcome. Cada conjuncao encontrada sinaliza um intent escondido que precisa ser extraido para seu proprio Goal atomico.

Meu trabalho nao e ditar quantos intents o time deve ter -- e garantir que cada intent descreve um unico outcome, para que o agente possa persegui-lo sem tradeoffs silenciosos entre partes do mesmo Goal. Um agente que recebe "construa o catalogo E o carrinho E o checkout" vai otimizar para uma dessas coisas e improvisar o resto. Um agente que recebe tres Goals atomicos trata cada um como um contrato independente.

O veredito e:

- **ATOMICO**: o Goal descreve exatamente um outcome. Nenhuma conjuncao, coordenacao, ou clausula dependente.
- **MULTI-GOAL**: o Goal contem "and", "then", "also", virgulas de coordenacao, ou multiplos verbos principais que descrevem outcomes distintos. Deve ser split.

## When to Use Me

Carregue esta skill quando:

- Voce esta escrevendo ou revisando o campo Descricao (Goal) de um intent e a sentenca tem "and", "e", "then", "depois", "also", "alem disso", ou virgulas que conectam outcomes distintos
- Um agente entregou um output que resolve 80% do Goal mas falha nos 20% restantes -- o sintoma classico de multi-goal intent onde o agente otimizou para a parte dominante
- O ciclo de alinhamento ([[.opencode/skills/intent-five-part-primitive/SKILL|intent-five-part-primitive]], [[docs/canonical/grill-me-alignment-interview|Grill-Me]]) esta para iniciar e o Goal candidato parece "carregado" -- muitas coisas em uma frase so
- Voce suspeita que a complexidade de coordenacao entre outcomes esta escondida dentro de uma unica sentenca, e o split vai revelar dependencias que precisam ser explicitas
- O [[.opencode/skills/two-implementations-goal-test/SKILL|two-implementations-goal-test]] identificou que o Goal e um goal, mas ainda parece conter multiplos outcomes -- atomicidade e pureza sao gates distintos
- Uma tarefa de "epic" chega como um unico intent -- epics sao colecoes de intents atomicos, nao intents gigantes
- Voce quer que o orquestrador possa paralelizar, sequenciar, ou rotear trabalho entre agentes diferentes -- isso so e possivel se cada intent e atomico

Nao use quando:

- O Goal ja e uma unica sentenca com um unico verbo principal e sem conjuncoes -- nao ha o que split
- A conjuncao no Goal e parte de uma lista de atributos do MESMO outcome (ex: "Build a service that handles search, filtering, and pagination" -- search + filtering + pagination sao features do mesmo servico, nao outcomes independentes)
- O Goal descreve um fluxo sequencial que e intrinsecamente um unico outcome (ex: "Authenticate the user and redirect to dashboard" -- e um fluxo, nao dois outcomes)
- Voce esta no meio de um incidente SEV1/SEV2 e a urgencia operacional substitui a disciplina de decomposicao (mas registre o intent composto para split post-mortem)

## The Anti-Pattern

```
ANTI-PATTERN: Multi-goal intent que esconde complexidade de coordenacao
atras de uma unica sentenca com "and".

Cenario:
  1. Um stakeholder escreve: "Build the product catalog, shopping cart,
     and checkout flow for the e-commerce platform."
  2. O agente recebe isso como um unico Goal. Tres outcomes distintos
     (catalog, cart, checkout) competem pela atencao do agente.
  3. O agente implementa o catalogo com profundidade (e a primeira coisa
     na sentenca, recebe mais tokens de atencao). O carrinho fica
     superficial. O checkout e um stub.
  4. O output "passa" porque o catalogo funciona. O stakeholder descobre
     duas semanas depois que o carrinho nao persiste entre sessoes e o
     checkout nao calcula frete.
  5. Ninguem percebeu que o Goal tinha tres outcomes porque "and" parece
     inocente -- mas ele escondeu que o agente precisava balancear tres
     contratos dentro de um unico intent.

Consequencia:
  - O agente otimizou para a parte dominante do Goal e improvisou o resto
  - Validacao enfraquecida: como validar tres outcomes com um unico
    conjunto de cenarios de sucesso e falha?
  - Coordenacao invisivel: catalog → cart → checkout e uma dependencia
    real, mas o intent unico nao a declara -- o agente pode implementar
    checkout antes do cart e descobrir o problema tarde
  - Impossibilidade de paralelizacao: com um unico intent, um unico
    agente faz tudo sequencialmente. Com tres intents atomicos, tres
    agentes poderiam trabalhar em paralelo
```

## The Pattern

```
PATTERN: Scan de conjuncoes → split em intents atomicos → ordenacao
opcional de dependencias.

Fluxo:

  Goal candidato chega
       │
       ▼
  ┌─────────────────────────────────────────────────────────┐
  │ PASSO 1: Scan de conjuncoes e coordenacao               │
  │                                                         │
  │ Identifique TODAS as ocorrencias de:                     │
  │   - "and" / "e" conectando verbos ou clausulas           │
  │   - "then" / "depois" / "em seguida" (sequencia)         │
  │   - "also" / "alem disso" / "tambem" (adição)            │
  │   - Virgulas em listas de outcomes (ex: "X, Y, and Z")   │
  │   - Verbos multiplos no imperativo (ex: "Create X.       │
  │     Update Y. Delete Z.")                                │
  │                                                         │
  │ CUIDADO: ignore conjuncoes DENTRO de um unico outcome.   │
  │ "Search, filter, and paginate products" → um outcome     │
  │ (servico de catalogo), nao tres. O criterio e: cada      │
  │ fragmento descreve um RESULTADO DISTINTO que um usuario   │
  │ ou sistema downstream experimentaria separadamente?      │
  └─────────────────────────────────────────────────────────┘
       │
       ▼
  ┌─────────────────────────────────────────────────────────┐
  │ PASSO 2: Extraia cada outcome atomico                    │
  │                                                         │
  │ Para cada fragmento identificado, escreva uma sentenca   │
  │ completa no formato:                                     │
  │   "<verbo> <objeto> <contexto opcional>"                 │
  │                                                         │
  │ Regras:                                                  │
  │   - Uma sentenca por outcome                             │
  │   - Sem "and", "then", "also"                            │
  │   - Sem referencias a outros outcomes na mesma sentenca  │
  │     (ex: "depois que X estiver pronto" → isso e          │
  │      dependencia, nao faz parte do Goal)                 │
  └─────────────────────────────────────────────────────────┘
       │
       ▼
  ┌─────────────────────────────────────────────────────────┐
  │ PASSO 3: (Opcional) Estabeleca dependencias               │
  │                                                         │
  │ Se os outcomes atomicos tem relacao de precedencia:      │
  │   - Catalog deve existir antes do Cart                   │
  │   - Cart deve existir antes do Checkout                  │
  │                                                         │
  │ Registre no campo Conexoes de cada intent:               │
  │   - "Depende de: [intent X]"                             │
  │   - "Desbloqueia: [intent Y]"                            │
  │                                                         │
  │ Isso permite que o orquestrador sequencie corretamente.  │
  └─────────────────────────────────────────────────────────┘
       │
       ▼
  ┌─────────────────────────────────────────────────────────┐
  │ PASSO 4: Valide cada Goal atomico                        │
  │                                                         │
  │ Para cada Goal atomico resultante:                       │
  │   - Aplique o two-implementations test (e um goal?)      │
  │   - Verifique que e uma sentenca unica sem conjuncoes    │
  │   - Confirme que descreve um outcome observavel          │
  │                                                         │
  │ Se um fragmento ainda tem conjuncao → split de novo.     │
  │ Se um fragmento falha no two-implementations test →      │
  │   e spec, nao goal. Reclassifique.                       │
  └─────────────────────────────────────────────────────────┘
```

### Exemplo Concreto: Multi-Goal → Intents Atomicos

```
ORIGINAL (multi-goal):
  "Build the product catalog, shopping cart, and checkout
   flow for the e-commerce platform."

Scan de conjuncoes:
  - Virgula + "and": "catalog, shopping cart, and checkout"
  - Tres outcomes distintos: catalog, cart, checkout

SPLIT:

  Intent #1 (catalog):
    Goal: "Build the product catalog — customers can search,
    filter by category and price, and view product details."
    Conexoes: "Desbloqueia: Intent #2 (shopping cart)"

  Intent #2 (shopping cart):
    Goal: "Build the shopping cart — customers can add items
    from the catalog, adjust quantities, and see the running
    total before checkout."
    Conexoes: "Depende de: Intent #1 (catalog). Desbloqueia:
    Intent #3 (checkout)"

  Intent #3 (checkout):
    Goal: "Build the checkout flow — customers can enter
    shipping, select payment, review the order, and complete
    the purchase."
    Conexoes: "Depende de: Intent #2 (shopping cart)"

Validacao pos-split:
  - Cada Goal e uma sentenca sem "and"? Sim.
  - Cada Goal passa no two-implementations test? Sim
    (catalog poderia ser Go+REST ou Node+GraphQL, etc.)
  - Dependencias estao explicitas? Sim, no campo Conexoes.
```

### Quando NAO Split

Nem toda conjuncao exige split. O criterio e: **cada fragmento descreve um resultado que um usuario ou sistema experimentaria separadamente?**

```
NAO SPLIT (atributos do mesmo outcome):
  "Build a service that handles search, filtering, and
   pagination for the product catalog."

  → Search, filtering, e pagination sao funcionalidades
    do MESMO servico de catalogo. Um usuario nao "experimenta"
    filtragem separadamente da busca -- sao partes de uma
    unica experiencia de descoberta de produtos.

SPLIT (outcomes distintos):
  "Build the product catalog AND the recommendation engine."

  → Catalog e recommendation sao outcomes distintos.
    Um usuario pode usar o catalogo sem recommendations.
    Recommendations podem existir sem o catalogo (ex: baseado
    em historico, nao em catalogo ativo). Sao sistemas
    separados que um usuario experimenta separadamente.
```

### Criterio de Distincao: Outcome vs. Funcionalidade

| Sentenca | Split? | Racional |
|---|---|---|
| "Build the catalog AND the cart" | SIM | Dois sistemas distintos. Usuario experimenta separadamente. |
| "Build the catalog with search, filter, and sort" | NAO | Funcionalidades do mesmo sistema. Um outcome composto. |
| "Create the API AND write the documentation" | SIM | Dois artefatos distintos com audiencias diferentes (devs vs consumers da API). |
| "Create the API with authentication, rate limiting, and logging" | NAO | Cross-cutting concerns do mesmo artefato. |
| "Notify the user AND update the order status" | SIM | Dois efeitos colaterais distintos em sistemas diferentes. |
| "Notify the user via email and SMS" | NAO | Dois canais para o mesmo outcome (notificacao). |

## Implementation Rules

1. **Um goal = uma sentenca. Sem excecoes.** A regra e mecanica, nao interpretativa: se a sentenca tem "and" ou "e" conectando verbos ou clausulas de outcome, split. A unica excecao e quando as conjuncoes conectam atributos de um MESMO outcome -- e esse julgamento e responsabilidade do revisor, nao do agente.

2. **O criterio de distincao e o usuario final.** Pergunte: "Um usuario ou sistema downstream experimentaria esses dois resultados como coisas separadas?" Se a resposta for sim -- mesmo que "obviamente relacionadas" -- split. Catalog e Cart sao obviamente relacionados, mas um usuario experimenta eles como momentos distintos.

3. **"Then" e "depois" sao dependencias, nao parte do Goal.** "Authenticate the user, then show the dashboard" contem um outcome (dashboard visivel) e uma pre-condicao (autenticacao). A autenticacao e uma constraint ou mecanismo, nao um outcome. Mantenha "Show the dashboard to authenticated users" e trate autenticacao como constraint.

4. **O split produz intents independentes, nao subtasks.** Cada intent atomico deve ser completavel e valido por si so. Se o Intent #2 so faz sentido se o Intent #1 foi completado de um jeito especifico, a dependencia e mais forte que "depende de" -- e um unico intent com fases, nao intents separados.

5. **Conexoes carregam as dependencias.** O campo Conexoes de cada intent atomico deve declarar: (a) de quais outros intents este depende, (b) quais outros intents este desbloqueia, (c) se a dependencia e de completude (so comece quando X terminar) ou de contrato (X define uma interface que Y consome).

6. **O split compoe com o two-implementations test.** Depois de split, cada Goal atomico deve passar pelo two-implementations test. E possivel que um fragmento seja goal (passa) e outro seja spec disfarcada (falha). O split revela essas diferencas que o intent original escondia.

## Integration with Existing Repo Infrastructure

O goal-atomicity-split opera como decompositor de intents, complementando a infraestrutura de alinhamento e orquestracao:

| Componente Existente | Como o Goal Atomicity Split complementa |
|---|---|
| [[.opencode/skills/intent-five-part-primitive/SKILL|intent-five-part-primitive]] | O primitivo de cinco partes define o formato do intent. O atomicity split garante que cada intent contem um unico outcome, prevenindo que o campo Descricao acumule multiplos outcomes e forcando o resto dos campos (constraints, falhas, sucessos, conexoes) a serem preenchidos por outcome, nao por conglomerado. |
| [[.opencode/skills/two-implementations-goal-test/SKILL|two-implementations-goal-test]] | O two-implementations test classifica goal vs spec. O atomicity split decompoe multi-goal em fragmentos atomicos ANTES da classificacao. Fluxo composto: split → test → purifica → entrega. Um goal com "and" pode ter partes que sao goals e partes que sao specs -- so o split revela isso. |
| [[docs/canonical/grill-me-alignment-interview|Grill-Me Alignment Interview]] | O Grill-Me entrevista sobre escopo, arquitetura e constraints. Com intents atomicos, cada entrevista foca em um unico outcome -- as perguntas sao mais precisas e as respostas nao misturam contextos de outcomes diferentes. |
| [[docs/canonical/vertical-slice-issue-generation|Vertical Slice Issue Generation]] | Issues geradas como fatias verticais herdam o Goal. Intents atomicos produzem fatias verticais mais focadas -- uma fatia por outcome, com comportamento observavel bem definido, em vez de uma fatia que tenta cobrir tres outcomes e nao valida nenhum completamente. |
| [[.opencode/skills/refine-issue/SKILL|refine-issue skill]] | O refine-issue decompoe issues em sub-issues com dependencias. O atomicity split opera no nivel acima: garante que a issue chega ao refine-issue com um unico outcome, para que a decomposicao em sub-issues opere sobre um contrato claro. |
| [[.opencode/skills/orchestrator/SKILL|orchestrator skill]] | O orchestrator coordena agentes paralelos. Intents atomicos permitem que o orchestrator paralelize trabalho: se Catalog, Cart e Checkout sao tres intents, tres agentes podem trabalhar simultaneamente (respeitando dependencias). Com um unico intent multi-goal, o orquestrador so pode alocar um agente sequencial. |
| [[docs/canonical/plan-execute-verify|Plan-Execute-Verify]] | A fase de Plan do PEV recebe o Goal. Com um Goal atomico, o plano gerado e focado em um unico resultado. Com um Goal multi-goal, o plano tenta cobrir tudo e frequentemente falha em aprofundar cada outcome. |
| [[docs/canonical/ice-craft-separation|ICE Craft Separation]] | A separacao de crafts atribui o Goal ao humano. O atomicity split ajuda o humano a decompor seu pensamento em outcomes atomicos, prevenindo que a complexidade de coordenacao vaze para o agente como "descubra como fazer tudo isso junto." |

## Quality Gates

Antes de declarar os intents atomicos como prontos para execucao, verifique:

- [ ] O scan de conjuncoes foi executado no Goal original e todas as ocorrencias de "and", "e", "then", "also" e virgulas de coordenacao foram identificadas
- [ ] Cada Goal atomico resultante e exatamente uma sentenca, sem conjuncoes, sem "and", sem "then"
- [ ] Nenhum Goal atomico contem referencia a outro outcome na mesma sentenca (dependencias vao no campo Conexoes, nao no Goal)
- [ ] Cada Goal atomico descreve um outcome que um usuario ou sistema experimentaria separadamente (nao apenas funcionalidades do mesmo outcome)
- [ ] Cada Goal atomico passa no [[.opencode/skills/two-implementations-goal-test/SKILL|two-implementations-goal-test]] (e um goal, nao uma spec)
- [ ] Dependencias entre intents atomicos estao declaradas no campo Conexoes: "Depende de" e "Desbloqueia"
- [ ] O tipo de dependencia esta especificado: completude (so comece quando X terminar) ou contrato (X define interface que Y consome)
- [ ] O numero de intents atomicos resultantes e gerenciável -- se o split produziu 15+ intents, o Goal original provavelmente era um epic, e intents intermediarios de coordenacao podem ser necessarios

## References

- [[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-analysis|Anatomy of Intent Analysis]]:136 -- Goal atomicity: "se o goal precisa de 'and', sao dois goals"
- [[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-patterns|Anatomy of Intent Patterns]]:82-103 -- Pattern 4: Goal Atomicity Split
- [[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-classification|Anatomy of Intent Classification]]:113-138 -- Classificacao como Missing (Medium integration value)
- [[docs/canonical/intent-five-part-primitive|Intent as Five-Part Primitive]] -- estrutura que recebe os Goals atomicos
- [[.opencode/skills/two-implementations-goal-test/SKILL|two-implementations-goal-test]] -- gate de pureza aplicado apos o split
- [[docs/canonical/vertical-slice-issue-generation|Vertical Slice Issue Generation]] -- geracao de issues a partir de intents atomicos
- [[.opencode/skills/refine-issue/SKILL|refine-issue skill]] -- decomposicao de issues em sub-issues
- [[.opencode/skills/orchestrator/SKILL|orchestrator skill]] -- coordenacao de agentes com intents atomicos paralelizaveis
- [[docs/canonical/plan-execute-verify|Plan-Execute-Verify]] -- fase de plan que opera sobre Goals atomicos

---

*Created: 2026-06-14 | Source: The Anatomy of Intent - ICE in IDSD — Pattern 4 (Missing, Medium value)*
