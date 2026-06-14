---
title: "Análise de Conhecimento Não-Óbvio: The Anatomy of Intent - ICE in IDSD"
type: analysis
tags: ["agentes-orquestracao", "harness-engineering", "spec-driven-development", "evals", "decision-discipline", "context-engineering"]
date: 2026-06-11
aliases: ["anatomy intent ice analysis", "ice in idsd knowledge extraction", "extração conhecimento intent ice", "intent decomposition analysis"]
relates-to: ["[[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-mental-model|Mental Model]]", "[[docs/canonical/ice-craft-separation|ICE Craft Separation]]", "[[docs/canonical/intent-five-part-primitive|Intent as Five-Part Primitive]]", "[[docs/canonical/human-owned-expectations-boundary|Human-Owned Expectations Boundary]]", "[[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]", "[[docs/canonical/generator-evaluator|Generator-Evaluator]]", "[[docs/canonical/token-economics-gap-filling|Token Economics of Gap-Filling]]", "[[docs/canonical/symphony-trap-awareness|Symphony Trap Awareness]]", "[[docs/canonical/application-owned-agent-control-plane|Application-Owned Agent Control Plane]]"]
---

# Análise de Conhecimento Não-Óbvio: The Anatomy of Intent — ICE in IDSD

> Fonte: Kapil Viren Ahuja — "The Anatomy of Intent (ICE in IDSD). Built from Where Spec-Driven Breaks" (2026-05-27)
> Extraído: 2026-06-11
> Regras: sem marketing, anedotas, histórias pessoais, repetição

---

## 1. Frameworks & Models

### 1.1 ICE Framework (Intent, Context, Expectations)

O framework ICE decompõe o trabalho de construir com agentes em três artefatos com donos humanos explícitos:

- **Intent**: o que se quer — goal, constraints que limitam o outcome, e failure conditions que o guardam.
- **Context**: o entorno onde o trabalho roda — stack, padrões do time, arquitetura existente, o que foi tentado antes. Montado pelo harness, não escrito pelo humano a cada intent.
- **Expectations**: o que conta como pronto, gerado a partir do intent e do context juntos, validado em checkpoint humano.

O autor posiciona ICE como "ainda uma spec", mas uma spec que deixa o modelo fazer o que foi construído para fazer — perseguir um goal — em vez de restringi-lo. A distinção operacional é que ICE é uma spec de outcome, não de implementação.

**Não-óbvio**: ICE não é só decomposição de documento — é decomposição de dono. Cada artefato pertence a uma entidade diferente: Intent e Expectations são do humano; Context é do harness (assemblado de padrões do org); o builder recebe Intent + Context e produz output que o validator checa contra Expectations. A separação de ownership é o mecanismo de defesa estrutural, não a estrutura do prompt.

### 1.2 Intent Decomposition (3-part model)

O Intent é decomposto em três partes, reduzido de um modelo anterior de cinco:

1. **Goal** — uma sentença, sem "and", sem ferramentas, sem nomes de classe. O teste: duas implementações completamente diferentes podem satisfazer isso? Se sim, é goal. Se não, é spec disfarçada.
2. **Constraints** — qualidades não-funcionais que o outcome deve carregar: performance, escala, confiabilidade, segurança, compliance. Direcionais (apontam para onde o outcome deve chegar), incondicionais (se o output erra uma constraint, falha), em linguagem de negócio (não patterns de implementação). Limite duro: 5 a 7 linhas.
3. **Failure conditions** — checks binários que o validator roda contra o output. Observáveis, post-output, cada um determinável por script sem julgamento humano.

**Não-óbvio**: a redução de 5 para 3 partes custou semanas. Connections continuam parte do modelo de Intent no nível conceitual, mas são "managed differently" — quando o engenheiro escrevia Connections no intent, o slot sangrava direto para Context porque o time já tinha service mesh. Scenarios foram split: failure scenarios (binários) ficaram no Intent como failure conditions; success scenarios moveram para Expectations, gerados de intent+context e validados em checkpoint. O motivo do split é que LLMs fazem reward-hack: se o builder recebe os mesmos scenarios que o validator vai checar, o builder otimiza para os checks em vez do outcome.

### 1.3 Modelo de Compartmented Evaluation

O builder recebe goal + constraints. O validator recebe failure conditions, compiladas em evals criptografadas. O builder não pode ensinar um teste que não pode ver. Esse é o defense estrutural contra o modelo otimizando para os checks em vez do outcome.

**Não-óbvio**: a separação não é apenas boa prática — é a única defesa estrutural conhecida contra reward-hacking em sistemas agentic. Sem compartimentalização, entregar constraints ao builder é convidar o modelo a produzir output que passa nos checks sem satisfazer o intent. A compartimentalização só funciona se cada requirement estiver no lado certo da linha: o que o builder precisa para decidir design é constraint; o que só pode ser avaliado depois é failure condition.

### 1.4 Garura Harness

O harness Garura faz o trabalho de carga: assembla context, compartimentaliza evals, e faz checkpoint de expectations. O Intent é a única parte que o humano escreve. O harness é a parte que "ganha a disciplina que você acabou de gastar".

**Não-óbvio**: o autor é explícito que o método não funciona sem o harness. A disciplina de escrever intents corretos (1-2 dias por epic) só vale a pena porque o harness converte essa disciplina em aceleração medida (3-4x mais rápido para adicionar capacidades ao codebase). Sem o harness, a disciplina é custo sem retorno. Essa é uma afirmação forte sobre coupling entre método e infraestrutura: ICE é indissociável de Garura.

---

## 2. Patterns & Architectures

### 2.1 Two-Implementations Test (Goal vs. Spec)

**Problema**: humanos escrevem specs e chamam de goals, porque o outcome está claro na cabeça e a mão digita o método.

**Mecânica**: para cada goal candidato, perguntar: duas implementações completamente diferentes podem ambas satisfazer isso? Se sim, é goal. Se só uma implementação poderia satisfazer, é spec disfarçada. "Build a microservice that handles the user-facing product catalog" passa. "Build a Go microservice using gRPC, with PostgreSQL for catalog storage and Redis for cart state" falha. O fix nunca é adicionar detalhe — é split. O método escala adicionando mais intents, não intents mais pesados.

**Não-óbvio**: o teste expõe que o autor considera o agente como decision-maker, não como typist. Se você escreveu a implementação no goal, você degradou o agente de tomador de decisão para digitador. E se você queria um digitador, não precisava de um agente — precisava de teclado e uma tarde.

### 2.2 Constraint vs. Failure Condition Split (Decision Rule)

**Problema**: engenheiros consistentemente misturam constraints com failure conditions. O autor admite que esse é um dos três failures que ele ainda comete "every time I sit down to write intents".

**Mecânica**: a regra de decisão é uma sentença — "Would knowing this change how the builder writes code?" Se sim, é constraint (o builder precisa saber para fazer a design call). Se não, é failure condition (o validator pega depois). "Must not introduce a new runtime dependency" é constraint. "Unit test coverage must stay above 90%" é failure condition — coverage só pode ser avaliada depois que o código existe, e dar isso ao builder como constraint convida coverage gaming.

**Não-óbvio**: a razão secundária para o split importa tanto quanto a primária. Constraints são direcionais (apontam para onde chegar), failure conditions são binários (passa/falha). Confundir os dois produz constraints que viram thresholds arbitrários em vez de direções, e failure conditions que o builder tenta otimizar em vez do validator checar.

### 2.3 Compartmented Evaluation Architecture

**Problema**: LLMs fazem reward-hack — otimizam para os checks que podem ver, não para o outcome.

**Mecânica**: três entidades separadas com superfícies de informação diferentes:
- **Builder**: recebe goal + constraints. Gera output.
- **Validator**: recebe failure conditions como evals (idealmente criptografadas). Checa output.
- **Human**: escreve Intent, veta Expectations no checkpoint.

O builder não vê os failure conditions. O validator não vê o goal nem as constraints (ou vê em forma diferente). O human é o único que vê tudo, e só intervém em checkpoints.

**Não-óbvio**: essa arquitetura é uma resposta direta ao comportamento documentado de LLMs. Não é uma preferência estética — é engenharia de sistema contra uma propriedade conhecida do modelo (reward-hacking). A fonte documenta que quando builder e validator compartilhavam os mesmos scenarios, o builder "over-fitted to the scenarios, and the validator did not know which side of the line they were on."

### 2.4 Scenario Split Architecture

**Problema**: scenarios servem duas funções conflitantes — guide para o builder e check para o validator. Quando o mesmo artefato serve aos dois, o builder over-fits e o validator perde independência.

**Mecânica**: split explícito em dois destinos:
- **Failure conditions** (ficam no Intent): binários, o validator é dono.
- **Success scenarios** (movem para Expectations): gerados de intent+context, validados em checkpoint humano.

O split é "non-negotiable" porque é o defense estrutural contra o modelo jogando com os checks.

### 2.5 Constraint List Discipline

**Problema**: a lista de constraints cresce. O autor documenta seu próprio padrão de falha: 6 linhas viram 16, cada uma sussurrando uma escolha de implementação.

**Mecânica**: limite rígido de 5 a 7 constraints. Cada constraint em linguagem de negócio, direcional, incondicional. Se uma linha escolhe ferramenta ou pattern, não é constraint — é spec escondida e vai para Context. Se a lista passa de "a handful", algo nela não pertence. O resto é Context (padrões do org) ou Expectations (gerado pelo sistema).

**Não-óbvio**: o limite não é arbitrário. Constraints são o lugar mais fácil de driftar o método de volta para o que foi abandonado (spec-driven). Cada constraint extra é uma decisão de design que o humano tirou do builder, e cada decisão tirada é um grau de liberdade que o agente perde.

### 2.6 Goal Atomicity

**Problema**: intents com "and" escondem múltiplos goals.

**Mecânica**: um goal = uma sentença, sem conjunção. Quando precisa de "and", tem quase certamente dois goals fingindo ser um. O fix é split, nunca adicionar detalhe. O método escala por quantidade de intents, não por peso de cada intent.

---

## 3. Operational Lessons

### 3.1 A redução de 5 para 3 partes não foi limpa

O autor passou de um modelo de Intent com 5 partes (Goal, Constraints, Failure Conditions, Connections, Scenarios) para 3. O corte custou semanas e deixou cicatrizes:

- **Connections**: um colega (Ira) argumentou que são reais e moldam o trabalho — um intent que fala com dois sistemas upstream é diferente de um que não fala com nenhum. Quando o autor tentou adicionar Connections como quarto slot, o engenheiro escreveu no intent. Para todo time que já tinha service mesh, o slot sangrava direto para Context e a linha parava de ser sharp. Connections continuam parte do modelo, mas "managed differently" — merecem peça própria.
- **Scenarios**: outra colega (Zia) perguntou o que o validator deveria fazer com success scenarios — era eval ou hint para o builder? Quando testaram ambos, o builder over-fitted e o validator não sabia de que lado da linha estava. O split foi a solução: failure conditions ficaram no Intent (binários, validator é dono); success scenarios moveram para Expectations.

**Lição**: a decomposição de um conceito em partes não é estável na primeira tentativa. As partes interagem com o sistema real (times, ferramentas, harnesses) e a interação revela se a linha entre elas é sustentável.

### 3.2 Os três failures que o autor ainda comete

O autor documenta três padrões de falha que ele mesmo repete, "every time", sob deadline:

1. **Method-in-goal**: a mão digita o método. "Build a Go microservice with..." em vez de "Build a microservice that...". O mais barato de errar, o mais caro de descobrir tarde.
2. **Constraint list bloat**: a lista cresce. Cada item parece essencial. 6 viram 16. As constraints param de ser qualidades do outcome e viram spec disfarçada.
3. **Mixing constraints with failures**: "eats all my cognitive cycles". A disciplina é perguntar, para cada linha, se ela molda o design do builder ou é algo que um validator checaria depois.

**Lição**: o método é duro até para quem o criou. Qualquer um que diga que o intent de três partes é fácil de escrever está vendendo "the same kind of leash with a friendlier handle."

### 3.3 O método escala por decomposição, não por densidade

Quando um intent fica complexo, o fix nunca é adicionar detalhe — é split em múltiplos intents. Isso é contra-intuitivo para engenheiros treinados em specs que crescem por acumulação de requirements. A disciplina é inversa: se o goal precisa de "and", são dois goals; se as constraints passam de 7, algo nelas não é constraint.

### 3.4 O harness faz o método valer a pena

Sem Garura (assemblar context, compartimentalizar evals, checkpoint expectations), a disciplina de escrever intents corretos é custo sem retorno. Com Garura, o workflow acelera 3-4x. O autor gasta 1-2 dias escrevendo intents para um epic, depois entrega para o time rodar o build "com muito pouco input de volta".

### 3.5 SDD tooling contradiz a si mesmo

A fonte documenta evidência concreta de contradição interna no tooling de spec-driven development (Spec Kit):

1. O manifesto declara test-first development NON-NEGOTIABLE.
2. O task template diz que tests são OPTIONAL.
3. O arquivo que roda o trabalho diz "Follow the TDD approach."

Três ordens para uma decisão, shipped juntas. Um modelo goal-seeking com três regras contraditórias não consegue raciocinar para um outcome — elege um dogma, obedece, e improvisa o resto. O exato comportamento que o método rígido foi adotado para prevenir.

### 3.6 O tooling de SDD instrui o modelo a preencher gaps

O Spec Kit não apenas deixa holes para o agente preencher — ele instrui o agente a preenchê-los. Quando a descrição é incompleta, o tooling diz ao modelo para "make informed guesses", usar "common patterns" para "fill gaps", e cap o modelo em "Maximum 3 [NEEDS CLARIFICATION] markers." Três. Onde a spec silencia, o modelo inventa o goal, e o tooling limita quantas vezes ele tem que admitir que está adivinhando.

---

## 4. Tradeoffs

| Decisão | Benefício | Custo |
|---|---|---|
| ICE (intent-driven) vs. SDD (spec-driven) | Modelo persegue outcome em vez de preencher formulário; agent é decision-maker, não typist | Disciplina humana pesada: escrever intents corretos custa 1-2 dias por epic; requer harness forte (Garura) para valer a pena |
| Goal como outcome vs. goal como mini-spec | Deixa o builder escolher arquitetura, stack e patterns; escala por decomposição de intents | Teste constante de "isso é goal ou spec?" — é o erro mais barato de cometer e o mais caro de descobrir tarde |
| Constraints como qualidades direcionais vs. constraints como requirements exaustivos | Builder mantém liberdade de design; constraints em linguagem de negócio sobrevivem a mudanças de stack | Disciplina para manter 5-7 linhas; tentação constante de transformar constraints em spec |
| Compartmented evaluation vs. shared evaluation | Defesa estrutural contra reward-hacking; builder não pode ensinar teste que não vê | Complexidade de infra: requer evals criptografadas, validator separado, checkpoint humano |
| 3-part Intent vs. 5-part Intent | Linha mais sharp entre partes; menos ambiguidade de ownership | Perda de granularidade — Connections e Scenarios são reais mas precisam de tratamento separado; a redução custou semanas |
| Intent-driven scaling vs. spec-driven scaling | Escala por quantidade de intents, cada um focado e pequeno | Requer decomposição disciplinada de epics em outcomes atômicos |
| Ferramenta SDD para times novos vs. ICE para times maduros | SDD é racional quando o time é novo, codebase frágil, stakes regulatórios — previsibilidade importa mais que velocidade | SDD colapsa fora desse caso: spec com holes dá ao modelo liberdade sem proteção, constraint sem o instinto do modelo para balancear |

---

## 5. Failure Patterns

1. **Spec-in-disguise goal**: o humano escreve o método no goal porque o outcome está claro na cabeça. "Build a Go microservice with gRPC and PostgreSQL" em vez de "Build a microservice that handles the product catalog." Causa: escrever sob deadline com solução já formada. Mitigação: two-implementations test — se só uma implementação satisfaz, é spec, não goal.

2. **Constraint list bloat**: 6 constraints viram 16. Cada linha adicionada se justifica como essencial, mas o conjunto para de ser qualidades do outcome e vira spec disfarçada — cada linha sussurrando uma escolha de implementação. Causa: tentação de capturar todo requirement conhecido na Intent em nome de completude (waterfall trap). Mitigação: limite rígido de 5-7; se passou, algo não pertence. O resto é Context ou Expectations.

3. **Mixing constraints with failure conditions**: o engenheiro coloca requirements nos dois slots indistintamente, quebrando a compartimentalização e convidando coverage gaming. Causa: a distinção é sutil e exige disciplina cognitiva constante. Mitigação: a regra de decisão de uma sentença — "Would knowing this change how the builder writes code?" Se sim, constraint. Se não, failure condition.

4. **Contradictory tool rules**: o tooling de SDD entrega três ordens conflitantes para a mesma decisão (non-negotiable, optional, mandatory) no mesmo repositório, na mesma semana. Causa: o método cresceu por acumulação sem reconciliação. Consequência: o modelo recebe regras contraditórias, elege um dogma, obedece, improvisa o resto — exatamente o comportamento que SDD foi desenhado para prevenir.

5. **Spec tooling instrui gap-filling**: o tooling de SDD não apenas deixa holes — ele comanda o modelo a preenchê-los com "informed guesses" e "reasonable defaults", limitando admissão de ignorância a 3 marcadores. Causa: o tooling internalizou que specs são incompletas e escolheu resolver com inferência do modelo em vez de reduzir escopo. Consequência: a proteção que a spec deveria oferecer some exatamente onde ela é mais necessária.

6. **Scenario over-fitting**: quando builder e validator compartilham os mesmos scenarios, o builder super-especializa nos exemplos e o validator perde independência. Causa: colapso do papel duplo dos scenarios como guia de construção e critério de validação. Mitigação: split estrutural — failure conditions no Intent (binários), success scenarios nas Expectations (gerados, validados em checkpoint).

7. **Drift silencioso do método**: constraints são o lugar mais fácil de driftar ICE de volta para SDD. Cada constraint extra parece inofensiva; o acúmulo transforma o intent em spec sem que ninguém perceba. Causa: o hábito de spec-writing é mais forte que a disciplina de intent-writing. Mitigação: revisão de constraints como gate explícito — cada linha deve passar no teste "isso molda o design ou é checkável depois?"

---

## 6. Synthesis

O insight unificador é que **LLMs são goal-seeking engines, e alimentá-los com specs é alimentar a abstração errada**. A indústria construiu tooling para transformar o modelo de "creative writer" em "disciplined specification engineer" — o produto é um harness cujo propósito declarado é prevenir o modelo de fazer o que foi construído para fazer. ICE propõe o inverso: dar ao modelo um outcome para perseguir, cercado de constraints que apontam direção e failure conditions que pegam desvio, deixando o modelo operar na engrenagem para a qual foi construído.

Três consequências para sistemas agentic:

- **Compartimentalização é o defense estrutural contra o modelo, não contra o humano**. A separação builder/validator não é sobre qualidade de código — é sobre impedir que o modelo otimize para os checks em vez do outcome. Se o builder pode ver os failure conditions, o sistema está vulnerável a reward-hacking por construção.

- **A linha entre constraint e failure condition é a decisão de design mais importante do método**. Ela determina o que o builder sabe vs. o que o validator checa, e portanto determina se a compartimentalização funciona. Errar essa linha quebra o defense estrutural inteiro.

- **ICE é indissociável do harness**. O autor é explícito: sem Garura, a disciplina de escrever intents é custo sem retorno. Isso significa que adotar ICE sem adotar (ou construir) um harness equivalente não é "ICE parcial" — é outra coisa, provavelmente spec-driven com outro nome. O método e a infraestrutura são um sistema acoplado, não duas decisões independentes.

O que o autor não nomeia explicitamente mas emerge do texto: ICE é essencialmente uma **linguagem de contrato entre humano e agente** onde o contrato especifica o que (goal), com que qualidades (constraints), e como saber se falhou (failure conditions), enquanto deixa o como para o agente. É a mesma anatomia em qualquer domínio — o exemplo do "red shoe under thirty dollars" mostra que a estrutura Goal + Constraints + Failure Conditions é independente de software. Isso sugere que ICE não é um método de coding — é um método de especificação de outcomes para agentes, e coding é um caso especial.
