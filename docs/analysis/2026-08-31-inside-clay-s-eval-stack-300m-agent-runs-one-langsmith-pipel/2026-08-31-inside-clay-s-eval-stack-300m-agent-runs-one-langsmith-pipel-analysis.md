---
title: "Analise de Conhecimento Nao-Obvio: Inside Clay's Eval Stack - 300M Agent Runs, One LangSmith Pipeline"
type: analysis
date: 2026-08-31
domain: evals
aliases: ["clay eval stack", "eval coverage matrix", "production-to-offline drift loop", "agent-first data foundation", "CES"]
tags: [analise, evals, agents, langsmith, data-platform, production, eval-driven-development, tool-unification]
last_updated: 2026-08-31
relates-to: ["[[docs/analysis/2026-06-10-eval-maturity-phases/2026-06-10-eval-maturity-phases-analysis|Eval Maturity Analysis]]", "[[docs/system-of-record|System of Record]]"]
---

# Analise de Conhecimento Nao-Obvio: Inside Clay's Eval Stack

> Fonte: video LangChain (13:01), "Inside Clay's Eval Stack: 300M Agent Runs, One LangSmith Pipeline", publicado 2026-08-28
> Fonte local: `/mnt/c/Users/pavan/raw-knowledge/sources/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel.md`
> Regras: sem marketing, anedotas, historias pessoais, filler ou repeticao

Nota de transricao: o transcript e uma unica linha (`...pipel.md:25`); toda citacao abaixo referencia essa linha com trecho citado. Nomes distorcidos pela transcricao foram normalizados: "Clagent"/"Clayun" -> Claggent; "lane chain"/"lang chain" -> LangChain/LangSmith; "engine" -> ferramenta de bulk analysis de traces do LangSmith; "fable" -> nome de modelo frontier ilegivel na transcricao (registro preservado como "fable").

Contexto minimo (so o necessario para as extracoes): Claggent (agente de pesquisa go-to-market, 300M+ runs/mes) e Sculptor (agente de engenharia go-to-market, 100K+ mensagens/semana, hoje interface primaria do produto) operam em volume onde "there's usually just a high volume of different traces" e nao e possivel olhar trace por trace nem falar com todo cliente (`...pipel.md:25`). Esse e o motivador de todo o resto.

---

## 1. Frameworks & Models

### 1.1 Eval Coverage Matrix (2x2: deterministic/nondeterministic x offline/online)

Modelo central da palestra: organizar evals em uma matriz com o objetivo explicito de ter "a few things in each of these boxes" — cobertura em todos os quadrantes, nao profundidade em um (`...pipel.md:25`).

- **Deterministico + offline**: goldens; evolui para structured eval checks parciais e trajectory/tool assertions (`...pipel.md:25`, "deterministic and offline, you have goldens").
- **Nao-deterministico + offline**: LLM-as-judge; simulated user multi-turn evals (`...pipel.md:25`, "offline and non-deterministic LLM as a judge").
- **Deterministico + online**: metricas objetivas de A/B — latencia, custo, se usuarios saem do chat para outras partes do produto, se travam (stuck), se abandonam (rage quitting) (`...pipel.md:25`).
- **Nao-deterministico + online**: quadrante de maior uso do LangSmith — online evaluators (NPS/satisfacao), perceived-eval (usuario corrigindo/desviando o agente), bulk analysis de traces de producao, human eval de traces (`...pipel.md:25`).

### 1.2 Modelo de tiers de eval por ambiente (fidelidade crescente)

Evals em niveis: local deve ser barato e rapido, propositalmente sem fidelidade ("locally, we don't care about O. We don't have a sandbox. We don't have a VFS"); CI/staging deve ser o mais proximo possivel do production harness, com staging "basically using the same thing as prod" (`...pipel.md:25`). Principio organizador: "meet your developers where they are".

### 1.3 Production -> Offline Feedback Loop (a "dotted arrow") com taxonomia de drift

O apresentador nomeia a seta de retorno (producao -> offline evals) como "the hardest part to set up" e declara eval drift / production drift "still an unsolved problem in the agent eval space" (`...pipel.md:25`). Taxonomia de drift apresentada:

- **Data drift**: casos de uso de producao nao sao os que o time testa e faz bug bashing.
- **Judge drift**: cada modelo/familia de LLM judge tem vies interno; hill-climbing em um judge especifico = overfitting nele.
- **Eval-set mirroring**: hill-climbing com eval set pequeno faz o prompt "mirror just those eval examples".

Contramedidas do modelo: puxar exemplos dos online evaluators; usar customer support tickets como sinal de alta qualidade; human-annotated goldens para detectar judge drift; use-case classifiers + use-case tagging para auditar se os evals cobrem os casos de uso reais de producao (`...pipel.md:25`).

### 1.4 Tool Unification Flywheel (UI = CLI = API, agentes internos e externos compartilham tools)

Modelo: qualquer coisa fazivel na UI deve existir no CLI e na API publica; Sculptor usa "the exact same tools that we expose via the CLI and API" (`...pipel.md:25`). O flywheel: agentes invocam as tools; falhas de tool ou de trajetoria geram user signal; isso melhora o agent harness ou a tool em si; a melhoria beneficia todos, incluindo agentes externos. Sinais entram tanto por checks automatizados (bulk trace analysis) quanto por human "vibe based eval" (`...pipel.md:25`).

### 1.5 Agent-First Data Foundation (data lake com agentes como usuarios first-class)

Modelo de migracao para data lake que unifica first-party e third-party data em uma unica plataforma sobre a qual agentes rodam, "building this as agents being the first class user" (`...pipel.md:25`). Requisitos derivados do modelo: guardrails antecipados; shadow builds seguros (agentes constroem novos data models e deployam em S3); separacao entre serving compute e development compute; skills e CLI para acesso nativo; long-running goal execution ("could take an hour it could take two hours") com Athena e praticas de compute em escala.

### 1.6 Self-Iterating Agent Loop (imagem de fechamento)

Arquitetura-alvo declarada: dados de clientes + third-party -> orquestracao -> execucao -> observacao do resultado -> feedback; "all parts of the product are feeding into a single unified data foundation that agents can reason over and build better iterations of themselves" (`...pipel.md:25`). E o flywheel 1.4 generalizado de tools para o produto inteiro.

### 1.7 Modelo de threshold de escala como gatilho de eval

O investimento em evals e narrado como funcao de dois thresholds explicitos: 300M runs/mes em Claggent e 100K mensagens/semana em Sculptor, ambos "past that threshold of where we could actually look at every trace or talk to every customer" (`...pipel.md:25`). Abaixo do threshold, evals "were not great"; acima dele, eval "became non-negotiable".

### 1.8 Evals como habilitador de desenvolvimento agentic

Modelo causal: com uma boa eval suite, e seguro deixar agentes de codigo (Claude, Codex, Devon) e o proprio LLM fazerem mudancas de prompt, "and you know that you're not shipping anything that is going to ruin production" (`...pipel.md:25`). A eval suite e o contrato de seguranca entre agentes desenvolvedores e producao.

---

## 2. Patterns & Architectures

### 2.1 CLI-first eval harness com persistencia remota

- **Problema**: suites de eval que exigem provisionamento de experimento em plataforma (ir ao LangSmith criar experiment, provisionar managed agent) criam atrito que mata o uso.
- **Mecanismo**: "everything is just like a command line eval suite"; roda local, sem sandbox/VFS; todo resultado, mesmo local, e escrito no LangSmith — "Eval should be persistent in version... everything even though it's run locally writes out there. So we store it" (`...pipel.md:25`). Ergonomia local + durabilidade/versionamento central na mesma arquitetura.

### 2.2 Plug-and-play harness com BYO evaluators

- **Problema**: cada novo produto/agente reconstruir harness de avaliacao.
- **Mecanismo**: um harness compartilhado por todas as partes do produto; novos produtos trazem apenas a propria eval suite e os proprios evaluators (LLM judges); "the rest of the harness is like there for them and it's plug-and-play" (`...pipel.md:25`).

### 2.3 Structured partial checks no lugar de goldens exatos

- **Problema**: goldens quebram com reordenacao irrelevante — "switching the ordering of some keywords or switching the node ordering causes them to break" — e eval ruidoso "just end up getting ignored".
- **Mecanismo**: structured eval checks que avaliam apenas as partes da query que importam ("only look at the parts of the query that we actually care about"), mais tolerantes; trajectory/tool assertions verificam o percurso, nao o texto final — exemplo dado: pergunta de pricing exige que o agente leia a tabela de precos (`...pipel.md:25`). Goldens permanecem apenas para superficies simples (ex.: query language).

### 2.4 Deterministic multi-turn (hardcoded user turns) em vez de simulated-user LLM

- **Problema**: avaliar agentes multi-turn sem introduzir uma segunda fonte de nao-determinismo.
- **Mecanismo**: duas variantes apresentadas — (a) agente-usuario simulado alimentado com exemplos de traces passados dirigindo a conversa ate uma conclusao; (b) turns de usuario hardcoded. Veredito operacional: a variante deterministica "were actually the most useful"; o agente-usuario era "too noisy", virava "another agent that you had to manage and keep up to date and also have evals for", e "ended up not being worth it" (`...pipel.md:25`).

### 2.5 Sinais implicitos de satisfacao como online evaluators

- **Problema**: medir qualidade percebida de agente em producao sem pesquisa explicita o tempo todo.
- **Mecanismo**: perceived-eval — detectar usuario corrigindo o agente, "pushing back on it", tentando guia-lo em outra direcao, como sinal negativo; combinado com NPS e metricas comportamentais objetivas (sair do chat, stuck, rage quit) (`...pipel.md:25`). O comportamento de correcao do usuario e tratado como dado de avaliacao.

### 2.6 Superficie unica de tools (agentes internos = clientes externos)

- **Problema**: divergencia entre o que o produto expoe e o que os proprios agentes usam duplica superficie e esconde falhas.
- **Mecanismo**: mesmas tools expostas via API/CLI sao dadas aos agentes internos; qualquer falha de invocacao observada em producao e sinal para melhorar tool ou harness, melhorando a API publica como efeito colateral (`...pipel.md:25`). Arquitetura: um autoridade de tools, dois consumidores (interno e externo).

### 2.7 Shadow builds com separacao serving/development compute

- **Problema**: agentes construindo novos data models nao podem colocar producao em risco.
- **Mecanismo**: agentes constroem e deployam data models em S3 como shadow builds; a seguranca vem da separacao arquitetural "we're separating out our serving and our development compute", de forma que "running some experiments and not bringing down prod" (`...pipel.md:25`). Guardrails antecipados (up front) em vez de revisao posterior.

### 2.8 Skills + CLI como camada de acesso de agente a dados

- **Problema**: agentes precisam acessar a plataforma de dados nativamente, sem adaptadores humanos.
- **Mecanismo**: investimento em skills e CLI proprios para os agentes; combinado com long-running steps orientados a goal ("here's this goal I want this data model") executando em Athena/compute escalavel por 1-2 horas (`...pipel.md:25`).

### 2.9 Consolidacao de fontes de dados disparates como desbloqueio de agentes

- **Problema**: traces no LangSmith, analytics no Snowflake, dados operacionais em Postgres, first-party no ClickHouse — agentes gastavam capacidade em "try to tie together all these different databases".
- **Mecanismo**: unificacao em uma unica data platform ("this has enabled our agents to do more") transformando o datastore em "a playground for agents" (`...pipel.md:25`). A fragmentacao de dados e tratada como bloqueio arquitetural para agentes, nao meramente inconveniencia para humanos.

### 2.10 Evals-first para tarefas longas de dados

- **Problema**: delegar a agentes tarefas de dados de horas sem criterio de sucesso definido.
- **Mecanica**: "Setting up evals first and driving towards those agents can go and do things with your data" — a eval suite precede e dirige a autonomia (`...pipel.md:25`).

---

## 3. Operational Lessons

- **Evals ruins no inicio sao a norma; escala corrige a prioridade**: "when we first built out some of our like agentic products, our evals were not great"; o que mudou foi volume (bilhoes de runs) e tarefas end-to-end longas (`...pipel.md:25`).
- **A eval suite e o pré-requisito para delegar mudancas de prompt a agentes de codigo** (Claude/Codex/Devon) sem risco de ruin production — eval e condicao de autonomia, nao acompanhamento (`...pipel.md:25`).
- **Goldens funcionam so em superficies simples**: confirmado para query language; em outputs complexos, quebram por reordenacao e sao ignorados (`...pipel.md:25`).
- **Eval ruidoso e eval morto**: "noisy evals just end up getting ignored" — a stricness do check tem que casar com a estabilidade do que se afirma (`...pipel.md:25`).
- **Determinismo ganha de realismo em multi-turn**: hardcoded user turns foram o formato mais util; simulated user custa mais para manter do que entrega (`...pipel.md:25`).
- **A seta producao->offline e a parte mais dura**: mais dificil que qualquer avaliador individual; drift de dados, de judge e de eval set sao os tres modos de falha nomeados (`...pipel.md:25`).
- **Support tickets como fonte de alta qualidade de sinal de cliente**, junto com online evaluators e goldens human-anotados (`...pipel.md:25`).
- **Human vibe-based eval continua valendo** junto de checks automatizados — "usually my favorite" (`...pipel.md:25`).
- **Step change de modelo frontier habilitou analise in-context em massa**: com o modelo citado como "fable" ficou possivel "look at these 10,000 examples and find trends", substituindo a pratica vibe-based de olhar poucos exemplos; sub-agents, goals e harnesses novos completam a habilitacao (`...pipel.md:25`).
- **Fragmentacao de datastores era o gargalo concreto** dos learning loops ("hard to scale this with our data primitives"), nao falta de modelos ou de evals (`...pipel.md:25`).

---

## 4. Tradeoffs

- **Goldens exatos vs structured partial checks** — beneficio: determinismo e simplicidade; custo: brittleness a reordenacao irrelevante. Decisao: goldens so para superficies simples; partial checks + trajectory assertions para o resto (`...pipel.md:25`).
- **Simulated-user LLM vs deterministic multi-turn** — beneficio: cobertura realista de conversas; custo: noise + o usuario simulado exige management, updates e proprias evals. Decisao: deterministico (`...pipel.md:25`).
- **Fidelidade local vs velocidade local** — beneficio do local sem sandbox/VFS: barato e rapido; custo: nao reproduz producao, compensado pelo tier staging = prod (`...pipel.md:25`).
- **Ergonomia CLI vs recursos de plataforma** — tudo pela CLI, nada de provisionar experimento na UI; custo aceito: menor riqueza local, mitigada pela escrita automatica em LangSmith (`...pipel.md:25`).
- **Expor tools publicamente (API/CLI) para agentes externos** — beneficio: flywheel de melhoria via falhas observadas + valor para clientes-agentes; custo: superficie publica maior e falhas visiveis (`...pipel.md:25`).
- **Migracao para data lake** — beneficio: first + third party num plano so, agentes first-class, shadow builds, tarefas longas em escala; custo: migracao arquitetural de quatro sistemas (LangSmith, Snowflake, Postgres, ClickHouse) (`...pipel.md:25`).
- **Separar serving e development compute** — beneficio: experimentos nao derrubam prod; custo: explicitamente reconhecido como incomum para startups ("which isn't the case for a lot of startups I know"), ou seja, custo de infraestrutura duplicada (`...pipel.md:25`).
- **Hill-climbing em LLM judge** — beneficio: grading automatico escalavel; custo: overfitting no vies do judge; mitigado com goldens human-anotados e rotatividade de exemplos (`...pipel.md:25`).

---

## 5. Failure Patterns

- **Eval rot por ruido**: goldens quebram por keyword/node ordering; consequencia observada: a suite e ignorada ("noisy evals just end up getting ignored"). Causa: stricness maior que a estabilidade do output. Mitigacao: partial checks que so olham o que importa (`...pipel.md:25`).
- **Data drift**: producao usa o produto de formas que o time nao testa. Causa: eval sets construidos do que o time conhece. Mitigacao: use-case tagging contra producao e importacao de exemplos de online evaluators (`...pipel.md:25`).
- **Judge drift**: overfitting no vies interno de um LLM judge especifico por hill-climbing continuo. Mitigacao: human-annotated goldens como referencia para detectar o desvio (`...pipel.md:25`).
- **Prompt mirroring**: eval set pequeno faz o prompt convergir aos proprios exemplos. Mitigacao: rotatividade/ampliacao do set via sinais de producao e support tickets (`...pipel.md:25`).
- **Simulated-user como componente podre**: agente-usuario ruidoso que exige ciclo proprio de manutecao e eval. Mitigacao: substituir por turns hardcoded (`...pipel.md:25`).
- **Experimento derruba producao**: risco estrutural quando serving e development compute compartilham infra. Mitigacao: separacao de compute + shadow builds em S3 (`...pipel.md:25`).
- **Dados fragmentados bloqueiam agentes**: quatro datastores (LangSmith, Snowflake, Postgres, ClickHouse) forcando os agentes a costurar bases. Mitigacao: data lake unificado (`...pipel.md:25`).
- **Sinais comportamentais de falha em producao** (mapear, nao prevenir): usuario preso (stuck), rage quit, saida do chat para outras partes do produto — tratados como metricas deterministicas online que delimitam falha percobida (`...pipel.md:25`).

---

## 6. Synthesis

O fio cruzado da palestra, nao nomeado pelo autor: **eval e uma propriedade da superficie do produto, nao dos testes**. Cada decisao aparentemente nao-eval — UI=CLI=API, agentes internos usando as tools publicas, unificar quatro datastores num lago — e na verdade decisao de avaliacao: reduzir o numero de superficies que podem divergir multiplica os pontos onde sinal de falha pode ser coletado e devolvido ao loop offline. O "flywheel" e a arquitetura de dados sao a infraestrutura da dotted arrow. Segunda tese implicita: **determinismo e o recurso escasso** — a hierarquia de preferencias observavel e (1) assercao parcial deterministica, (2) multi-turn com turns hardcoded, (3) LLM judge, (4) agente simulado, e cada passo em direcao a nao-determinismo adiciona um componente que precisa das suas proprias evals, updates e controle de drift; componentes que adicionam meta-trabalho acima do valor entregue sao cortados. Terceira: **o threshold de escala, nao a maturidade, e o gatilho de investimento** — o mesmo time conviveu com evals ruins enquanto pôde olhar traces; a incapacidade estrutural de observar (300M runs/mes) e o que torna eval "non-negotiable" e, em seguida, o que torna seguro delegar o proprio desenvolvimento (mudancas de prompt por agentes de codigo) a essa eval suite. A maturacao descrita aqui e um caso concreto do modelo em [[docs/analysis/2026-06-10-eval-maturity-phases/2026-06-10-eval-maturity-phases-analysis|Eval Maturity Analysis]], com a acrescimo do quadrante online-nao-deterministico e da taxonomia de drift como areas abertas.
