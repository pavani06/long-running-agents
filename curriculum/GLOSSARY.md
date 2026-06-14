---
title: "📖 GLOSSÁRIO: Termos Essenciais"
type: curriculum-index
aliases: ["glossário termos", "definições", "terminologia"]
tags: [curriculo-conteudo, reference]
relates-to: ["[[docs/system-of-record|System of Record]]", "[[curriculum/INDEX|Curriculum Index]]", "[[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]"]
last_updated: 2026-06-10
---
# 📖 GLOSSÁRIO: Termos Essenciais

Referência rápida de termos usados neste programa.

---

## A

### Agent (Agente)
**Definição:** Uma entidade autônoma de IA (geralmente baseada em LLM) que pode tomar ações, usar ferramentas e executar tarefas em sequência.

**Em KODA:** KODA é um agente que interage com clientes via WhatsApp.

**Nível:** 1

**Ver também:** Sub-agent, Multi-agent system

---

### Agent Loop (Loop do Agente)
**Definição:** O ciclo repetitivo onde um agente: recebe input → pensa → toma ação → recebe resultado → repete.

**Exemplo:** KODA recebe mensagem → pensa → checa catálogo → responde → aguarda próxima mensagem.

**Nível:** 1

---

### Amnesia (Context Amnesia)
**Definição:** Quando um agente "esquece" contexto anterior por ter excedido janela de contexto.

**Problema:** KODA não lembraria de preferências do cliente após 30-60 minutos.

**Solução:** State persistence + memory management.

**Nível:** 1

---

### Architecture Decision Record (ADR)
**Definição:** Documento que registra uma decisão de arquitetura significativa, seu contexto e consequências.

**Em KODA:** "Por que usamos Planner/Generator/Evaluator e não um único agente?"

**Template:** Veja `08-tools-templates/architecture-decision-record-template.md`

**Nível:** 3

---

## C

### Closed-Loop Company
**Definição:** Modelo operacional em que agentes leem estado real da empresa, como código, issues, reuniões, artefatos e decisões, e devolvem próximos trabalhos, bugs e atualizações de decisão para fechar o ciclo entre observação e execução. No currículo, use este termo como ponte para [[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent Operating System]].

**Nível:** 3

---

### Compaction (Contexto Compaction)
**Definição:** Processo de resumir ou comprimir contexto antigo para fazer espaço para novo contexto, mantendo informações-chave.

**Server-Side:** Realizado pelo servidor/modelo, não pelo agente.

**Nível:** 3

---

### Compartmented Evaluation Architecture (Arquitetura de Avaliacao Compartimentada)

**Definição:** Padrão arquitetural onde Builder (Generator) e Validator (Evaluator) recebem superfícies de informação seladas -- o Builder recebe apenas goal e constraints, o Validator recebe failure conditions (potencialmente encriptados ou ocultos). A compartimentação impede que o Builder faça reward-hacking otimizando outputs para checks visíveis em vez de outcomes reais.

**Por que importa:** O Generator-Evaluator separa responsabilidades, mas sem superfícies seladas o Generator pode acessar as rubricas do Evaluator e otimizar contra elas. Compartimentação formaliza a fronteira de informação: o que o Builder pode ver vs. o que o Validator usa para julgar. Isso fornece uma defesa estrutural contra o agente otimizar para checks em vez de outcomes.

**Elementos-chave:** Superfícies de informação seladas, failure conditions ocultas ou encriptadas do Builder, audit trail de visibilidade de informação, prevenção de leakage (não copiar failure conditions para o prompt do Builder), e "reward-hacking prevention" como intenção de design explícita.

**Em KODA:** No Product Discovery, o Generator recebe customer_context e goal, mas não recebe as failure conditions detalhadas do Evaluator. O Evaluator verifica contra rubrica que o Generator não viu, criando um teste cego que impede otimização superficial.

**Nível:** 3

**Ver também:** [[docs/canonical/compartmented-evaluation-architecture|Compartmented Evaluation Architecture]], [[docs/canonical/generator-evaluator|Generator-Evaluator]], [[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]], Generator/Evaluator Pattern

---

### Constraint Budget Gate (Gate de Orcamento de Constraints)

**Definição:** Heurística que impõe um limite rígido de 5 a 7 constraints direcionais e incondicionais em linguagem de negócio para cada tarefa. Constraints que escolhem ferramentas, nomeiam padrões ou descrevem implementação são reclassificadas como contexto; checks que medem output viram failure conditions. Previne que listas de constraints cresçam até virarem especificações de implementação disfarçadas.

**Por que importa:** O repositório já trata o crescimento de constraint lists como risco ("Constraint list can grow large, adding evaluation latency"). O Constraint Budget Gate transforma esse risco em disciplina: um limite numérico explícito que força o author de intent a priorizar o que realmente é constraint (guia o Builder) vs. o que é contexto ou failure condition.

**A regra dos 5-7:** Constraints devem ser direcionais ("o produto não pode conter lactose"), incondicionais (não "se possível, evite lactose"), e em linguagem de negócio (não "usar campo lactose_free=True no filtro SQL"). O número 5-7 é uma heurística calibrada por domínio, não uma prova matemática.

**Em KODA:** Uma intent de Product Discovery poderia ter constraints como: (1) produto sem lactose, (2) preço <= R$ 220, (3) em estoque em SP, (4) não recomendar estimulantes noturnos, (5) explicar trade-off quando preferência conflita com restrição. Se a lista chega a 12 itens, o gate força reclassificação: metade vira contexto ou failure conditions.

**Nível:** 3

**Ver também:** [[docs/canonical/constraint-budget-gate|Constraint Budget Gate]], [[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]], [[docs/canonical/intent-five-part-primitive|Intent Five-Part Primitive]], [[curriculum/03-nivel-3-advanced-architecture/exercises/exercise-constraint-budget-gate|Exercício: Constraint Budget Gate]]

---

### Constraint-Failure Decision Rule (Regra de Decisao Constraint-Failure)

**Definição:** Heurística de classificação que pergunta: "Saber isso mudaria como o Builder escreve código?" Se sim, é uma constraint (guia o Builder durante a geração). Se não -- só pode ser verificado depois que o output existe -- é uma failure condition (guia o Validator durante a checagem). Previne que times misturem orientação de Builder com checks de Validator.

**Por que importa:** O five-part intent tem campos separados para constraints e failure scenarios, mas nenhum mecanismo diz ao author como decidir qual campo usar para cada item. A decision rule resolve isso com uma única pergunta operacional. Constraints que só fazem sentido depois do output (ex: "a mensagem final não deve ter mais de 300 caracteres") são failure conditions, não constraints.

**A pergunta-âncora:** "Se eu contasse isso ao Builder ANTES dele começar, ele escreveria código diferente?" Se sim → constraint. Se não → failure condition. Exemplo: "o produto não pode ter lactose" muda como o Builder busca no catálogo → constraint. "A resposta final deve ser educada" só pode ser verificada depois → failure condition.

**Em KODA:** Na criação de um Sprint Contract para recomendação, a regra classifica "não recomendar produtos com lactose" como constraint (muda a busca) e "explicação deve conectar produto ao objetivo" como failure condition (só pode ser avaliada no output final). Essa classificação determina qual agente recebe cada informação.

**Nível:** 3

**Ver também:** [[docs/canonical/constraint-failure-decision-rule|Constraint-Failure Decision Rule]], [[docs/canonical/intent-five-part-primitive|Intent Five-Part Primitive]], [[docs/canonical/human-owned-expectations-boundary|Human-Owned Expectations Boundary]], [[curriculum/03-nivel-3-advanced-architecture/exercises/exercise-constraint-failure-decision-rule|Exercício: Constraint-Failure Decision Rule]]

---

### Context Anxiety
**Definição:** Comportamento observado onde agentes se comportam de forma ansiosa/com pressa ao se aproximarem do limite de contexto.

**Manifestação:** Respostas mais curtas e decisões precipitadas quando próximo do final da janela.

**Solução:** Harness moderno (4.6+) reduz drasticamente este problema.

**Nível:** 1

---

### Context Rot (Degradação de Contexto)
**Definição:** Perda gradual de coerência conforme o agente avança na janela de contexto.

**Manifestação:** Começando bem, mas 2 horas depois as decisões não fazem sentido.

**Nível:** 1

---

### Context Window
**Definição:** Número total de tokens que um modelo pode processar por vez. É a "memória imediata" do agente.

**Exemplo:**
- Claude Opus 4.6: 1,000,000 tokens (≈ 750,000 palavras)
- O suficiente para ~6 horas de trabalho contínuo

**Em KODA:** Quantidade de conversação + histórico que KODA pode "ver" por vez.

**Nível:** 1

---

### Context Progressive Disclosure
**Definição:** Arquitetura de contexto em que instruções e capacidades ficam em diretórios de skills carregados por regras de trigger, em vez de viverem todas em um prompt monolítico. O padrão canônico é [[docs/canonical/resolver-based-context-progressive-disclosure|Resolver-Based Context Progressive Disclosure]].

**Nível:** 3

---

### Contract (Sprint Contract)
**Definição:** Acordo negociado entre generator e evaluator sobre o que "pronto" significa antes de começar.

**Exemplo:**
- Generator: "Vou implementar checkout com Stripe"
- Evaluator: "Aceito se: (1) testa com 3 cartões reais, (2) maneja erros, (3) não deixa dados expostos"
- Ambos concordam: contrato feito.

**Nível:** 2

---

## E

### Evaluator (Avaliador)
**Definição:** Um agente separado responsável por avaliar e gravar o trabalho de um Generator.

**Características:**
- Usa Playwright para testar aplicações web
- Avalia contra rubrics definidos
- Fornece feedback estruturado

**Em KODA:** Avaliador verifica se recomendação de produto é boa e se pedido é processado corretamente.

**Ver também:** Generator, Generator/Evaluator Pattern

**Nível:** 2

---

### Evaluation Rubric
**Definição:** Conjunto de critérios mensuráveis para avaliar qualidade subjetiva.

**Exemplo para design:**
- Design Quality: 1-10 (coerente? bonito?)
- Originality: 1-10 (padrão ou custom?)
- Craft: 1-10 (tipografia, espaçamento?)
- Functionality: 1-10 (tudo funciona?)

**Em KODA:**
- Relevância da recomendação: 1-10
- Clareza da resposta: 1-10
- Adequação de preço/promoção: 1-10

**Template:** Veja `08-tools-templates/evaluation-rubric-template.md`

**Nível:** 2

---

## F

### Failure Pattern Classification Loop (Loop de Classificacao de Padroes de Falha)
**Definicao:** Ritual semanal onde o time revisa falhas, erros e comportamentos indesejados dos agentes, classifica-os por categoria (context_loss, tool_misuse, state_persistence, rubric_gap, prompt_regression, safety_escape, latency_cost) e converte padroes recorrentes em guardrails automatizados (lint rules, skills, reviewer prompts, testes de regressao).

**Componentes:** Taxonomia de falhas, cadencia semanal de revisao, pipeline de conversao de observacao humana em automacao de harness, deduplicacao de casos, tier assignment (fast/medium/deep) e pruning de casos obsoletos.

**Em KODA:** Toda sexta-feira, o time revisa tickets de suporte, traces de falha e rejeicoes do Evaluator. Encontrou 7 bugs de navegacao por teclado no mes? Vira um lint rule. Cupons vencidos passaram 3 vezes? Vira um caso de regressao no tier fast. O objetivo e eliminar classes de comportamento, nao instancias.

**Ver tambem:** Garbage Collection Day, Production Failure Regression Flywheel, Tested Degradation Ladder

**Nivel:** 3

---

### Fuzzy Compiler (LLM as Fuzzy Compiler)
**Definicao:** Modelo mental que trata o LLM como um compilador fuzzy, o harness como passes de otimizacao, e o codigo gerado como artefato de build descartavel. O ativo duravel nao e o codigo que o agente produziu -- sao as constraints de dominio, as regras de negocio e as rubricas de qualidade que geraram aquele codigo.

**Implicacao:** Quando o modelo melhora, voce nao reescreve codigo -- voce recompila o mesmo source com um backend melhor. As constraints de dominio ("cliente alergico nunca recebe produto com alergeno") sobrevivem a qualquer troca de modelo. As compensacoes de modelo ("recarregue perfil a cada 3 turns") sao candidatas a remocao.

**Componentes do modelo mental:**
- Source code = constraints de dominio, regras de negocio, rubricas de qualidade
- Compiler = o harness (prompts + lint rules + validators + reviewers)
- Optimization passes = cada validacao que o harness aplica
- Backend = o modelo de LLM especifico
- Binary / build artifact = o codigo gerado pelo agente

**Ver tambem:** Invariant-Compensation Split, Harness Evolution, Measured Harness Evolution Lifecycle

**Nivel:** 3

---

## G

### Garbage Collection Day (Dia de Coleta de Lixo do Harness)
**Definicao:** Meta-loop semanal (tipicamente sexta-feira) onde feedback humano de revisao de codigo, tickets de suporte e observacoes de producao e sistematicamente convertido em guardrails automatizados do harness. Fecha o ciclo entre "um humano percebeu um padrao" e "o harness impede esse padrao automaticamente".

**Mecanica:** Toda semana, o time revisa: (1) categorias de slop observadas em revisoes de PR, (2) tickets de suporte com causa raiz de harness, (3) falsos positivos e falsos negativos do Evaluator, (4) escapes de seguranca ou qualidade. Cada categoria identificada gera uma acao concreta: nova lint rule, atualizacao de skill, ajuste de reviewer prompt, ou novo caso de regressao.

**Por que importa:** Sem este ritual semanal, o conhecimento de revisao fica na cabeca dos revisores humanos. Com ele, cada observacao vira um guardrail que protege todos os agentes futuros. E a diferenca entre "o revisor apontou isso 14 vezes" e "o revisor apontou isso uma vez e nunca mais".

**Ver tambem:** Failure Pattern Classification Loop, QA-to-Backlog Feedback Loop, Production Failure Regression Flywheel

**Nivel:** 3

---

### Goal Atomicity Split (Divisao Atomica de Metas)

**Definição:** Heurística que exige que cada goal seja uma única frase sem conjunções. Quando "e" aparece na descrição de um goal, ele deve ser dividido em múltiplos goals atômicos. "Melhorar a busca e adicionar filtro de preço" vira dois goals: (1) melhorar a busca, (2) adicionar filtro de preço. Previne que intents multi-goal escondam complexidade de coordenação.

**Por que importa:** Goals compostos escondem trade-offs. Um agente que recebe "otimizar latência e melhorar cobertura" não sabe qual priorizar quando os dois conflitam. A atomicidade força o outcome owner a decidir prioridades ANTES da execução, quando o custo da decisão é baixo. Cada goal atômico pode ter seu próprio Sprint Contract, suas próprias constraints, e seu próprio Evaluator.

**A regra do "e":** Percorra a descrição do goal. Cada "e" que conecta duas ações independentes é um ponto de split. "E" que conecta detalhes de uma mesma ação ("buscar produtos sem lactose e abaixo de R$ 50") não necessariamente exige split -- o teste é: as duas partes podem ser implementadas e verificadas independentemente?

**Em KODA:** "Recomendar whey e processar pagamento" são dois goals atômicos com ciclos de vida diferentes. O primeiro pertence ao Discovery Agent, o segundo ao Order Agent. Dividi-los evita que o mesmo agente tente recomendar e cobrar na mesma chamada.

**Nível:** 2

**Ver também:** [[docs/canonical/goal-atomicity-split|Goal Atomicity Split]], [[docs/canonical/intent-five-part-primitive|Intent Five-Part Primitive]], [[docs/canonical/vertical-slice-issue-generation|Vertical Slice Issue Generation]], [[curriculum/02-nivel-2-practical-patterns/exercises/exercise-goal-atomicity-split|Exercício: Goal Atomicity Split]]

---

### Generator (Gerador)
**Definição:** Um agente responsável por construir/criar algo.

**Em contexto de pairs:** Trabalha com Evaluator. Generator cria, Evaluator avalia.

**Em KODA:** Generator processa pedidos, Generator descobre produtos.

**Ver também:** Evaluator, Generator/Evaluator Pattern

**Nível:** 2

---

### Generator/Evaluator Pattern
**Definição:** Padrão onde duas entidades (LLMs) separadas colaboram: uma gera, outra avalia.

**Por que funciona:**
- Avaliador pode ser treinado para ser crítico
- Generator não sofre de sycophancy (tendência de agradar)
- Separação de responsabilidades

**Contraste com Self-Evaluation:**
- ❌ Single agent: "Fiz bom trabalho? Sim!"
- ✅ Generator/Evaluator: "Você fez assim. Está errado. Refaça."

**Aplicação KODA:**
```
Generator: Processa pedido
Evaluator: Verifica se order está completa, preços corretos, inventory ok
```

**Nível:** 2

---

### Granularity (Granularidade)
**Definição:** Nível de detalhe dos critérios de avaliação ou decomposição.

**Exemplo:**
- Granularidade baixa: "Produto deve estar correto" ❌
- Granularidade alta: "Produto deve: (1) existir em inventory, (2) ter preço válido, (3) estar em promoção se aplicável" ✅

**Regra:** Quanto mais granular, mais actionable o feedback.

**Nível:** 2

---

## H

### Harness (Estrutura de Suporte)
**Definição:** A infraestrutura e padrões que envolvem um ou mais agentes para fazê-los mais confiáveis por períodos longos.

**Componentes:**
- State persistence (memória)
- Planning mechanisms (planejamento)
- Evaluation loops (avaliação)
- Agent coordination (coordenação)

**Analogia:** Se agente é piloto de avião, harness é o avião + torre de controle + combustível.

**Em KODA:** Toda infraestrutura que sustenta KODA rodando corretamente por horas.

**Nível:** 1

---

### Harness Evolution
**Definição:** Processo de simplificar/remover componentes de harness conforme o modelo melhora.

**Exemplo - Opus 4.5 vs 4.6:**
| Componente | 4.5 | 4.6 |
|-----------|-----|-----|
| Context reset | Essencial | Não precisa |
| Sprint decomp | Necessário | Opcional |
| Eval cadence | Per-sprint | Single pass |

**Princípio:** Não mantenha scaffolding que o modelo não precisa.

**Nível:** 3

---

### Human-Owned Expectations Boundary (Fronteira de Expectativas de Propriedade Humana)

**Definição:** Padrão de governança onde a definição de "pronto" (expectations) é um artefato separado, de autoria exclusiva do outcome owner (quem quer o resultado), e não do Generator (quem implementa) ou do Evaluator (quem avalia). O harness consome esse artefato para validação, mas não o modifica.

**Por que importa:** Sem essa fronteira, agentes decidem o que conta como sucesso durante a execução -- e tendem a definir sucesso como "o que consegui implementar", não como "o que o outcome owner precisava". A fronteira transforma "done" de sensação em artefato auditável.

**Em KODA:** No Product Discovery, a definição de recomendação válida ("sem lactose, em estoque, abaixo de R$ 50, com justificativa conectada ao objetivo") é escrita pelo PM de produto, não pelo Generator que busca no catálogo. O Evaluator julga contra essa definição, não contra sua própria interpretação.

**Nível:** 2

**Ver também:** [[docs/canonical/human-owned-expectations-boundary|Human-Owned Expectations Boundary]], [[docs/canonical/owner-of-no-role-design|Owner-of-No Role Design]], Generator/Evaluator Pattern, Sprint Contract

---

## I

### ICE Craft Separation (Separação de Crafts ICE)

**Definição:** Decomposição do trabalho agentic em três crafts distintos com donos explícitos: **Intent** (o que deve ser feito -- dono: outcome owner), **Context** (informação necessária para executar -- dono: harness), e **Expectations** (definição de pronto -- dono: outcome owner). A separação impede que um único documento monolítico misture intenção, contexto e critérios de validação.

**Por que importa:** Quando intent, context e expectations viajam no mesmo prompt, o agente preenche as lacunas entre eles por inferência. Cada lacuna preenchida por inferência é uma decisão que o outcome owner não tomou. A separação explícita força que cada lacuna seja identificada e fechada pelo dono correto antes da execução.

**Os três crafts:**
- **Intent Craft:** O que o outcome owner quer. Formalizado como descrição, constraints, failure scenarios, success scenarios e connections.
- **Context Craft:** O que o harness sabe. Catálogo, código, estado do sistema, documentação canônica, decisões de arquitetura.
- **Expectations Craft:** Como saber se deu certo. Rubricas, critérios de aceitação, condições de parada, definição de falha.

**Nível:** 2

**Ver também:** [[docs/canonical/ice-craft-separation|ICE Craft Separation]], Intent as Five-Part Primitive, Human-Owned Expectations Boundary, [[docs/canonical/application-owned-agent-control-plane|Application-Owned Agent Control Plane]]

---

### Intent as Five-Part Primitive (Intenção como Primitiva de Cinco Partes)

**Definição:** Formalização do intent como uma estrutura de cinco campos obrigatórios -- description, constraints, failure scenarios, success scenarios, connections -- que devem ser preenchidos e validados por um Intent Completeness Gate antes que qualquer agente inicie a execução.

**Por que importa:** Intents subespecificados são a causa raiz de grande parte do token waste em sistemas agentic. "Melhora a busca" parece um intent, mas é apenas um título. Sem constraints, o agente não sabe o que não pode quebrar. Sem failure scenarios, não sabe o que constitui erro. Sem connections, não sabe quais sistemas são afetados. O gate rejeita intents incompletos com perguntas direcionadas ao outcome owner.

**Os cinco campos:**
- **Description:** O que deve ser feito (uma frase com verbo de ação e sistema afetado).
- **Constraints:** Limites booleanos verificáveis que o trabalho deve respeitar.
- **Failure Scenarios:** Cenários que definem output errado (condição + comportamento esperado).
- **Success Scenarios:** Cenários que definem output certo (da perspectiva do outcome owner).
- **Connections:** Referências a outros intents, sistemas ou documentos canônicos afetados.

**Nível:** 2

**Ver também:** [[docs/canonical/intent-five-part-primitive|Intent Five-Part Primitive]], [[docs/canonical/grill-me-alignment-interview|Grill-Me Alignment Interview]], [[curriculum/02-nivel-2-practical-patterns/exercises/exercise-05-intent-five-part-primitive|Exercício 5: Intent Five-Part Primitive]], ICE Craft Separation

---

## K

### KODA
**Definição:** Agente conversacional de IA para venda de suplementos esportivos via WhatsApp.

**Capacidades:**
- Descoberta de produtos
- Processamento de pedidos
- Integração com fulfillment
- Entrega no mesmo dia

**Em contexto do programa:** Case study e aplicação prática de todos os padrões.

**Nível:** Todos (com foco em Nível 4)

---

## M

### METR (Model Evaluation Task Completion Rate)
**Definição:** Métrica que mede percentagem de tarefas que um agente completa com sucesso.

**Visualizado como:** Gráfico mostrando duração máxima (horas) que agente pode rodar com 50% de sucesso.

**Benchmark:** Opus 4.6 completa tasks 12 horas com 50% de sucesso (vs 1 hora em Opus 3.5).

**Nível:** 1

---

### Memory / State
**Definição:** Informações que um agente retém entre operações.

**Tipos:**
- **Short-term:** Em contexto atual (rápido, limitado)
- **Long-term:** Em storage externo (lento, ilimitado)
- **File-based:** Em arquivos no disco (estruturado)

**Em KODA:** Conversação atual = short-term, histórico de pedidos = long-term.

**Nível:** 3

---

### MCP (Model Context Protocol)
**Definição:** Protocolo para agentes usarem ferramentas/recursos externas.

**Exemplos:**
- Agente usa MCP para acessar banco de dados
- Agente usa MCP para chamar APIs

**Em KODA:** KODA usa MCP para integrar com catálogo, fulfillment, etc.

**Nível:** 2

---

### Multi-Agent System
**Definição:** Sistema com múltiplos agentes independentes que coordenam entre si.

**Padrão comum:** Planner (strategist) + Generator (executor) + Evaluator (critic).

**Vantagem:** Separação de responsabilidades, melhor qualidade de output.

**Em KODA:** 
- Planner: decide rota (discovery vs order vs fulfillment)
- Generator: executa a tarefa
- Evaluator: verifica qualidade

**Nível:** 3

---

## P

### Planner (Planejador)
**Definição:** Agente especializado em quebrar problema em etapas.

**Entrada:** "Build a retro game maker"  
**Saída:**
```
Sprint 1: Setup projeto, criar canvas
Sprint 2: Sprite editor
Sprint 3: Level designer
Sprint 4: Play mode
```

**Em KODA:** Planner decide: cliente quer descobrir produtos ou fazer pedido?

**Nível:** 2

---

### Post-Training (Pós-treinamento)
**Definição:** Fase após treinamento base do modelo onde é refinado com feedback específico.

**Contexto:** Modelos Claude são continuamente pós-treinados, daí melhorias entre versões.

**Nível:** 1

---

### Persona-Based Documentation (Documentacao Baseada em Personas)
**Definicao:** Modelo onde cada especialista do time (front-end architect, security engineer, UX engineer, product owner) documenta sua especialidade como um documento NFR duravel. Agentes implementadores carregam as personas relevantes para a tarefa antes de codar. Revisores carregam as personas relevantes para o diff automaticamente.

**Por que importa:** Substitui o modelo de um AGENTS.md universal e generico por documentos especializados que multiplicam conhecimento. Uma atualizacao no Security Persona melhora todos os agentes que tocam em auth a partir do dia seguinte. Elimina o gargalo onde o especialista humano precisa apontar os mesmos problemas em todo PR.

**Mecanica de dispatch:**
- PR toca em `.tsx`? Carrega Frontend Persona + UX Persona
- PR toca em `auth`? Carrega Security Persona
- PR toca em `analytics`? Carrega Product Persona

**Em KODA:** Camila (Frontend) mantem 12 regras sobre autocomplete, aria, CSS variables e state machines. Roberta (Security) mantem 8 regras sobre tokens, XSS, CORS e sanitizacao. Todo agente que implementa formulario recebe as regras das duas automaticamente.

**Ver tambem:** AGENTS.md, Durable Non-Functional Requirements Memory, Reviewer Agents as CI Gates

**Nivel:** 3

---

### Presence-in-the-Loop Metric (Métrica de Presença no Loop)

**Definição:** Métrica de governança que mede o envolvimento humano DURANTE a execução do agente -- não apenas a aprovação simbólica ao final. Composta por quatro sinais: presence timeline (linha do tempo de interações), stale-presence warnings (alertas de ausência prolongada), required intervention points (checkpoints obrigatórios de parada), e review confidence signal (score de 0.0 a 1.0 que calibra o escrutínio do revisor final).

**Por que importa:** Aprovação final chega tarde demais. Um agente pode gerar 2.300 linhas em 6 horas sem supervisão, e o code review descobrir na hora 7 que a premissa estava errada desde a hora 1. A métrica de presença força intervenção cedo, quando corrigir é barato, e produz um sinal de confiança que informa o revisor se aquele diff foi supervisionado ou produzido no vácuo.

**Quatro sinais:**
- **Presence Timeline:** Registro cronológico de cada interação humana (pergunta respondida, direção corrigida, decisão aprovada).
- **Stale-Presence Warnings:** Alertas quando o owner fica ausente além de thresholds configurados por perfil de risco (warning, critical, escalation).
- **Intervention Checkpoints:** Pontos obrigatórios de parada antes de decisões arquiteturais, mudanças de direção ou acúmulo de diff.
- **Review Confidence Signal:** Score agregado baseado em densidade de interações, presença ativa vs passiva, gaps de supervisão e cobertura de checkpoints.

**Nível:** 3

**Ver também:** [[docs/canonical/presence-in-the-loop-metric|Presence-in-the-Loop Metric]], [[docs/canonical/manual-brake-question-gate|Manual Brake Question Gate]], [[docs/canonical/human-afk-task-routing-gate|Human/AFK Task Routing Gate]], [[curriculum/03-nivel-3-advanced-architecture/exercises/exercise-06-presence-in-the-loop-metric|Exercício 6: Presence-in-the-Loop]]

---

## R

### Ralph Loop (Ralph Technique)
**Definição:** Técnica onde um agente roda em loop incrementally, resolvendo um task por iteração.

**Origem:** Jeffrey Huntley, julho 2025.

**Pseudocódigo:**
```
while not complete:
  claude-code --prompt-file PROMPT.md
  check if done
  if done: break
  else: update PROMPT.md with learnings
```

**Status em KODA:** Padrão anterior, substituído por generator/evaluator.

**Nível:** 2

---

### Rubric
**Definição:** Ver "Evaluation Rubric"

**Nível:** 2

---

## S

### Skillify Pipeline
**Definição:** Pipeline de hardening que transforma um workflow que funcionou uma vez em uma skill roteável, testada e resolvível, com unit tests, LLM evals, integration tests, resolver trigger, trigger eval, check-resolvable, smoke test e schema. Veja [[docs/canonical/skill-resolver-skillify-capability-pipeline|Skill-Resolver-Skillify Capability Pipeline]].

**Nível:** 3

---

### Self-Evaluation (Autossavaliação)
**Definição:** Quando um agente avalia seu próprio trabalho.

**Problema:** Agents são sycophantic (tendem a agradar), aprovam trabalho ruim.

**❌ Não faça isto:**
```
Agent: Criei o feature.
Agent: É bom? Sim, muito bom!
```

**✅ Faça isto:**
```
Generator: Criei o feature.
Evaluator: É bom? Não, porque...
```

**Lição:** Sempre use Evaluator separado!

**Nível:** 2

---

### Specification (Spec)
**Definição:** Descrição detalhada do que algo deve fazer.

**Exemplo baixa qualidade:** "Build um jogo"  
**Exemplo alta qualidade:**
```
Features:
1. Sprite editor com palette de 54 cores
2. Level designer com grid-based layout
3. Play mode com physics engine
4. Score tracking

Constraints:
- HTML/CSS/JS only
- Mobile responsive
- Same-day delivery (sic)
```

**Em KODA:** Product spec detalhado antes de implementar feature.

**Nível:** 2

---

### Sprint
**Definição:** Unidade de trabalho bem-definida, tipicamente 30-120 minutos de execução do agente.

**Em contexto tradicional:** 1-2 semanas de trabalho humano.

**Em contexto agente:** 30-120 minutos de tempo de agente.

**Em KODA:** "Discover products" = 1 sprint, "Process order" = 1 sprint.

**Nível:** 2

---

### Sprint Contract
**Definição:** Ver "Contract"

**Nível:** 2

---

### Sycophancy
**Definição:** Tendência de LLMs em agradar o usuário, mesmo que isso signifique aprovar qualidade inferior.

**Manifestação:**
- Agent diz "Fiz bem" mesmo se fez mal
- Agent evita crítica negativa
- Agent concorda com usuário mesmo se estiver errado

**Solução:** Separar em dois LLMs (Generator + Evaluator), treinar Evaluator para ser crítico.

**Nível:** 2

---

## T

### Token
**Definição:** Unidade básica de texto que um LLM processa. Tipicamente ~4 caracteres.

**Context window:** Número máximo de tokens que modelo pode processar por vez.

**Orçamento:** "Temos X tokens, gastamos Y no histórico, restam Z para a resposta."

**Em KODA:** Se conversação tem 50k tokens, restam 950k para a resposta (em Opus 4.6 de 1M).

**Nível:** 1

---

### Token Budget / Token Accounting
**Definição:** Gerenciamento consciente de quantos tokens você usa/tem disponível.

**Exemplo:**
```
Total tokens: 200,000
Usar para: Histórico = 50,000, Instruções = 10,000
Restante: 140,000 para agent rodar
```

**Nível:** 1

---

### Token Economics of Gap-Filling (Economia de Tokens do Preenchimento de Lacunas)

**Definição:** Modelo de atribuição de custo que conecta tokens gastos a lacunas específicas nos campos de Intent, Context e Expectations. A premissa central: agentes que preenchem lacunas de ICE durante a execução queimam exponencialmente mais tokens por outcome concluído do que agentes que recebem ICE completo antes de começar.

**Por que importa:** O token ledger do harness sabe quanto você gastou. O burn rate monitor sabe a que velocidade. Mas nenhum dos dois sabe POR QUE o custo foi alto. Gap-filling token economics fecha esse loop: identifica que 40% dos tokens foram gastos preenchendo a lacuna "quem precisa disso", ou que os retries 3-7 foram causados por uma constraint ambígua que deveria estar no intent. Isso torna o cost-proxy do Manual Brake mensurável.

**Mecanismo de atribuição:**
- **Gap-cost report:** Relatório que mapeia cada retry e cada turno de clarificação a um campo ICE específico ausente ou ambíguo.
- **Missing-context request:** Quando o agente detecta que falta um dado para decidir, emite uma pergunta direcionada ao outcome owner em vez de inferir.
- **Budget guardrail:** Se o custo de gap-filling excede um threshold, o harness para e exige clarificação em vez de continuar queimando tokens.

**Nível:** 2

**Ver também:** [[docs/canonical/token-economics-gap-filling|Token Economics of Gap-Filling]], [[docs/canonical/explicit-token-budget-ledger|Explicit Token Budget Ledger]], [[docs/canonical/burn-rate-runtime-forecast|Burn Rate Runtime Forecast]], Token Budget, ICE Craft Separation

---

### Trace (Agent Trace)
**Definição:** Log detalhado de cada passo que um agente toma.

**Contém:**
- Input recebido
- Reasoning do agente
- Ações tomadas
- Output produzido

**Valor:** Ferramenta de debugging mais poderosa para entender agent behavior.

**Como usar:** Leia traces quando agent não faz o esperado.

**Lição:** "Ler traces é seu loop de debugging principal."

**Nível:** 2

---

### Two-Implementations Goal Test (Teste das Duas Implementacoes)

**Definição:** Heurística para distinguir goals de especificações disfarçadas. A pergunta de revisão: "Duas implementações substancialmente diferentes podem ambas satisfazer isto?" Se sim, é um goal (descreve O QUE alcançar). Se não, é uma especificação mascarada de goal (descreve COMO implementar). "Mostrar produtos ordenados por relevância" é goal; "usar TF-IDF com similaridade de cosseno no Pinecone" é especificação.

**Por que importa:** Agentes tratam especificações como ordens literais. Se o intent diz "implementar com Pinecone", o agente implementa com Pinecone -- mesmo que uma busca simples resolva melhor. O teste das duas implementações expõe especificações que chegaram vestidas de goal e força o outcome owner a separar O QUE de COMO antes da execução.

**A pergunta-âncora:** "Se eu lesse apenas este goal e desse para dois times diferentes, eles produziriam soluções fundamentalmente diferentes que ainda assim satisfariam o outcome owner?" Se sim → goal puro. Se não → tem especificação embutida. Remova a especificação do goal e mova para constraints (se for restrição real) ou para contexto (se for preferência de implementação).

**Em KODA:** "Recomendar produtos com TF-IDF no Pinecone" falha no teste (só uma implementação possível). "Cliente vê recomendações personalizadas baseadas no histórico" passa (múltiplas implementações: busca semântica, filtro por categoria, modelo de afinidade, etc.).

**Nível:** 2

**Ver também:** [[docs/canonical/two-implementations-goal-test|Two-Implementations Goal Test]], [[docs/canonical/intent-five-part-primitive|Intent Five-Part Primitive]], [[docs/canonical/grill-me-alignment-interview|Grill-Me Alignment Interview]], [[curriculum/02-nivel-2-practical-patterns/exercises/exercise-two-implementations-goal-test|Exercício: Two-Implementations Goal Test]]

---

## V

### Verification Loop (Loop de Verificação)
**Definição:** Ciclo onde gerador cria algo, verificador testa, feedback é retornado.

**Exemplo:**
```
Generator → Cria feature
Test → Roda testes automatizados
Evaluator → Valida contra rubric
Feedback → Volta ao Generator
```

**Em KODA:** Após gerar pedido, verificamos se está completo.

**Nível:** 2

---

## W

### Weights / Model Weights
**Definição:** Os parâmetros internos (números) de um modelo de IA que determinam seu comportamento.

**Contexto:** "Baking behavior into the weights" = treinar o modelo para ser melhor naquela tarefa.

**Em evolução Claude:** Cada nova versão tem weights melhorados.

**Nível:** 1

---

## Siglas e Acrônimos

| Sigla | Significado | Onde Usar |
|-------|------------|----------|
| **ADR** | Architecture Decision Record | Documentar decisões |
| **AI** | Artificial Intelligence | Geral |
| **API** | Application Programming Interface | Integrações |
| **DAW** | Digital Audio Workstation | Case study |
| **LLM** | Large Language Model | Geral |
| **MCP** | Model Context Protocol | Ferramentas/APIs |
| **METR** | Model Evaluation Task Completion Rate | Métricas |
| **QA** | Quality Assurance | Testes |
| **RL** | Reinforcement Learning | Pós-treinamento |

---

## Conceitos Relacionados por Nível

### Nível 1 (Fundamentos)
- Agent, Agent Loop, Amnesia
- Context Window, Context Rot, Context Anxiety
- Harness, Token, Token Budget
- METR, Weights

### Nível 2 (Padrões Práticos)
- Evaluator, Generator, Generator/Evaluator Pattern
- Contract (Sprint Contract)
- Evaluation Rubric, Granularity
- Planner, Self-Evaluation, Sycophancy
- Sprint, Trace, Verification Loop
- MCP, Ralph Loop
- ICE Craft Separation, Intent as Five-Part Primitive
- Human-Owned Expectations Boundary
- Token Economics of Gap-Filling
- Two-Implementations Goal Test, Goal Atomicity Split

### Nível 3 (Arquitetura Avançada)
- Multi-Agent System
- Memory/State, Compaction
- Harness Evolution
- Closed-Loop Company, Skillify Pipeline, Context Progressive Disclosure
- Architecture Decision Record
- LLM as Fuzzy Compiler, Invariant-Compensation Split
- Persona-Based Documentation, Failure Pattern Classification Loop
- Garbage Collection Day, QA-to-Backlog Feedback Loop
- Presence-in-the-Loop Metric
- Constraint Budget Gate, Constraint-Failure Decision Rule
- Compartmented Evaluation Architecture

### Nível 4 (KODA-Específico)
- KODA, suas capacidades e aplicações
- Como todos os conceitos se aplicam a KODA

---

## Como Usar Este Glossário

**Você não entende um termo?**
1. Procure aqui
2. Leia a seção "Ver também"
3. Vá para o arquivo indicado em "Nível"

**Exemplo:**
Você vê "Generator/Evaluator" mas não entende.
→ Leia definição aqui
→ Vá para `02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md`
→ Faça os exercícios

---

## Termos Frequentemente Confundidos

### Context Window vs. Token
- **Context Window:** Total de tokens que modelo pode processar
- **Token:** Unidade individual de texto

### Sprint vs. Loop
- **Sprint:** Unidade discreta de trabalho (30-120 min)
- **Loop:** Ciclo repetitivo que pode ter múltiplos sprints

### Harness vs. Agent
- **Agent:** A IA que faz o trabalho
- **Harness:** Infraestrutura que sustenta o agent

### Evaluator vs. Evaluation Rubric
- **Evaluator:** O agente que avalia
- **Rubric:** Os critérios pelos quais avalia

### Self-Evaluation vs. Verification
- **Self-Evaluation:** Agent avalia seu próprio trabalho (❌ ruim)
- **Verification:** Evaluator separado verifica (✅ bom)

---

## Referências Cruzadas

**Quer entender mais?**

- Histórico de evolução: → `10-references/model-capability-timeline.md`
- Exemplos práticos: → `09-case-studies/`
- Padrões detalhados: → `05-core-concepts/`
- Knowledge Graphs: → `06-knowledge-graphs/`

---

*Glossário | Referência de termos | v1.0*
