---
title: "The Production AI Playbook — Deploying Agents at Enterprise Scale (Sandipan Bhaumik, Databricks)"
type: analysis
date: 2026-06-26
domain: production-ai-playbook
aliases: ["production AI playbook", "enterprise AI agents", "Databricks production framework", "5-pillar framework", "Bhaumik production AI"]
tags: [analise, agentes-orquestracao, evals, production, governanca, monitoramento]
last_updated: 2026-06-26
relates-to: ["[[docs/canonical/eval-tier-stratification|Eval Tier Stratification]]", "[[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]]", "[[docs/canonical/production-grounded-eval-sampling|Production-Grounded Eval Sampling]]", "[[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]", "[[docs/canonical/deterministic-tool-dispatch|Deterministic Tool Dispatch]]", "[[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]]", "[[docs/canonical/generator-evaluator|Generator/Evaluator]]", "[[docs/canonical/pain-signal-eval-progression-gate|Pain-Signal Eval Progression Gate]]"]
---

# The Production AI Playbook: Deploying Agents at Enterprise Scale

> **Fonte**: Sandipan Bhaumik (Databricks) — "The Production AI Playbook: Deploying Agents at Enterprise Scale", AI Engineer Conference, 37 min talk.
> **Source URL**: https://www.youtube.com/watch?v=ObTPqBGsEbA
> **Sintetizado**: 2026-06-26 a partir de 5 análises independentes de chunks do mesmo transcript.

---

## 1. Frameworks & Models

### 1.1 5-Pillar Production AI Framework

Bhaumik apresenta um framework de 5 pilares que deve ser projetado **antes de qualquer código**. Os pilares são interdependentes e não sequenciais — cada um influencia os demais desde o primeiro dia de design.

| Pilar | Função | Por que sem ele o sistema quebra |
|---|---|---|
| **Evaluation** | Medir se o agente está produzindo outputs de qualidade | Sem evals, você não sabe se está melhorando ou regredindo a cada deploy |
| **Observability** | Tracing, logging, dashboards — visibilidade completa da cadeia de execução | Sem tracing, falhas são invisíveis; o agente dá respostas confiantes mas erradas e você só descobre pelo CSAT |
| **Data Foundation** | Ingestão, processamento, embeddings, atualização de knowledge bases | 60% do tempo do projeto; dados construídos para humanos (tolerantes a ambiguidade) falham com agentes (intolerantes) |
| **Multi-Agent Orchestration** | Coordenação entre agentes especializados com padrões de fault tolerance | Sem coreografia explícita, agentes fazem chamadas redundantes, entram em loops, ou falham parcialmente sem rollback |
| **Governance** | PII detection, prompt versioning, model change management, compliance | 47 PII breaches capturados na fase de testes; sem governance, esses dados vazam em produção |

**Insight operacional central**: "Agents don't forgive you" — a qualidade de dados que funciona para dashboards humanos não funciona para agentes. Cada ambiguidade, inconsistência ou staleness nos dados se transforma em falha visível do agente.

### 1.2 3-Layer Evaluation Architecture

A arquitetura de avaliação em 3 camadas, onde a camada 3 é a mais negligenciada mas a que captura as falhas mais caras:

| Camada                                | Tipo                                                                         | O que avalia                                                                                    | Custo                      | Frequência                                  |
| ------------------------------------- | ---------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- | -------------------------- | ------------------------------------------- |
| **Layer 1 — Deterministic**           | Regex, NER, PII detection, schema validation                                 | Fatos objetivos, formato de output, presença de dados sensíveis                                 | Baixo (zero LLM)           | CI + every PR                               |
| **Layer 2 — Semantic / LLM-as-Judge** | Groundedness, safety, relevance, faithfulness                                | Qualidade semântica da resposta: o agente respondeu o que foi perguntado? Respeitou o contexto? | Médio (LLM calls)          | PR + nightly                                |
| **Layer 3 — Behavioral**              | Tool call analysis, loop detection, duplicate API detection, path efficiency | O agente chegou à resposta pelo caminho correto?                                                | Alto (full trace analysis) | Merge to main (suite completa), CI (subset) |

**Por que a Layer 3 é crítica**: um agente pode dar a resposta correta ("seu saldo é R$ 1.234,56") pelo caminho errado (3 chamadas redundantes ao banco, 2 chamadas a uma API externa desnecessária). Em demo, parece ótimo. Em produção com 20.000 chamadas/mês, cada uma dessas chamadas redundantes custa dinheiro e latência.

### 1.3 Eval-Driven Development Timeline

A inversão mais contraintuitiva do framework: o modelo é selecionado na **semana 7** de um projeto de 8 semanas. A infraestrutura de avaliação é construída primeiro.

| Semana | Atividade | Artefato |
|---|---|---|
| 1-2 | Evaluation layer | 200 casos reais de agentes humanos → golden dataset inicial |
| 3-6 | Data foundation + tracing infrastructure | Pipelines de ingestão, embedding updates, centralized trace collection |
| 7-8 | Model selection via data-driven comparison | Rodar todos os modelos candidatos contra o eval dataset → escolher o que performa melhor nos dados reais |

**Resultado**: "Model selection became very quick" — com 200 casos reais, semanas de debate subjetivo foram eliminadas. O eval dataset decidiu.

### 1.4 Data Flywheel

O eval dataset é um organismo vivo que cresce monotonicamente:

1. **Início**: ~200 casos reais de agentes humanos (golden answers)
2. **Cada incidente de produção** → novo caso de teste adicionado ao dataset
3. **Cada nova feature** → novos cenários de teste
4. **Resultado**: "The bigger it grows, the better your system will be"

Cada incidente deixa uma "cicatriz permanente" na suite de testes, prevenindo regressão. O dataset precisa de categorização (security, login, tool calls), ownership explícito, e manutenção ativa — caso contrário vira um monólito ingerenciável.

### 1.5 Production Incident Playbook

O playbook de 5 etapas que integra com sistemas ITSM existentes:

```
Detect → Diagnose → Contain → Fix → Add to Living Dataset
```

| Etapa | Ação | Ferramenta |
|---|---|---|
| **Detect** | CSAT drop, alerta de anomalia, PII breach flag | Eval dashboard (superfície primária de detecção, não logs) |
| **Diagnose** | Tracing revela onde a falha ocorreu (stale embeddings, prompt drift, tool loop) | Centralized trace collection + LLM judge reports |
| **Contain** | Prompt rollback, human deflection, circuit breaker | Versioned prompt store + routing layer |
| **Fix** | Correção da causa raiz (ex: update vector DB com novo policy document) | Eval dataset reports identificam o gap específico |
| **Add to Dataset** | Novo caso de teste cobre o cenário exato da falha | Living eval dataset |

**Exemplo real**: banco mudou taxas de juros, enviou emails para clientes, mas o vector DB não foi atualizado com o novo policy document. CSAT caiu. Tracing revelou embeddings stale. Sem tracing → falha invisível, agente continuava dando respostas confiantes e erradas.

---

## 2. Patterns & Architectures

### 2.1 Multi-Agent Orchestration Patterns

Três padrões de orquestração com trade-offs claros:

| Padrão | Mecanismo | Latência | Debugabilidade | Quando usar |
|---|---|---|---|---|
| **Orchestrator-Worker** | Agente central distribui tarefas para workers especializados e agrega resultados | Alta (round-trips) | Alta (tudo passa pelo orchestrator) | Fluxos complexos, compliance, auditoria |
| **Choreography** | Agentes se comunicam diretamente via eventos, sem coordenador central | Baixa (comunicação direta) | Baixa (difícil rastrear quem fez o quê) | Baixa latência crítica, agentes independentes |
| **Human-in-the-Loop** | Confidence threshold dispara intervenção humana; agente pausa e escala | Variável | Alta (decisão humana documentada) | Decisões de alto risco, compliance regulatório |

### 2.2 Fault Tolerance Patterns (aplicados na camada de orquestração)

| Padrão | Problema | Mecanismo |
|---|---|---|
| **Saga** | Transação distribuída entre múltiplos agentes | Cada step tem uma compensating action; se um step falha, os anteriores são revertidos |
| **Compensation** | Falha parcial em workflow multi-agent | Rollback das operações já concluídas via ações compensatórias |
| **Circuit Breaker** | Falhas em cascata (um agente lento degrada todos) | Threshold de falhas → abre circuito → fallback para resposta padrão ou humano |

### 2.3 Centralized Trace Collection

Em enterprises, múltiplos frameworks de agentes (CrewAI, LangChain, custom) rodam em múltiplas clouds. A estratégia:

```
Todos os frameworks → Collect traces → Centralized trace layer → Multiple consumers
```

Consumidores da camada centralizada:
- **Dashboards** — visão unificada de todos os agentes
- **Text-to-SQL** — queries ad-hoc sobre comportamento dos agentes
- **LLM Judges** — avaliação automatizada de qualidade
- **Auditors** — compliance e auditoria
- **Online Monitoring** — detecção de anomalias em tempo real

**Regulatory gate**: "In Europe or regulated industries, you cannot even onboard AI into production without tracing" — observabilidade não é opcional, é pré-requisito regulatório.

### 2.4 Prompt-as-Code with Change Management

Prompt versionado como código, com disciplina de commit message que documenta causalidade:

Cada alteração de prompt deve responder 3 perguntas no commit:
1. **Por que mudou?** (causal trigger — ex: "bank changed interest rate policy")
2. **Que falha causou a mudança?** (diagnostic context — ex: "CSAT dropped 15% on balance inquiry queries")
3. **Que falha essa mudança endereça?** (predictive intent — ex: "prevents stale rate information when policy docs update")

Commits genéricos ("updated prompt", "improved response") são insuficientes para debugging e rollback.

### 2.5 Living Eval Dataset Governance

O dataset cresce e precisa de estrutura:

- **Categorização**: security, login, tool calls, knowledge retrieval, math/reasoning
- **Ownership**: cada categoria tem um dono responsável pela qualidade dos casos
- **Particionamento para custo**: subset rápido para CI, suite completa no merge to main
- **Manutenção**: casos obsoletos são arquivados (não deletados — rastreabilidade)

### 2.6 Behavioral Eval Cost Governance

| Ambiente | O que roda | Custo | Gatilho |
|---|---|---|---|
| **CI (PR)** | Subset estratificado (representativo de cada categoria) | Baixo | Todo push |
| **Nightly** | Suite completa Layer 1 + Layer 2 | Médio | Agendado |
| **Merge to main** | Suite completa Layer 1 + 2 + 3 (behavioral) | Alto | Merge event |

### 2.7 Data Architecture Stack (Databricks)

```
Cloud Storage → Delta Lake (tabular properties on raw data)
  → Unity Catalog (centralized permissions, PII tagging)
    → Applications (agents, dashboards, LLM judges)
```

Unity Catalog injeta contexto de governance nas queries: PII tags viajam do catálogo até o prompt do agente, permitindo que o modelo saiba quais campos são sensíveis sem expor os dados.

### 2.8 Dual Data Strategy

| Tipo | Propósito | Exemplos |
|---|---|---|
| **Question Data** | O que o agente precisa responder | Policy documents, FAQs, product catalogs, knowledge bases |
| **Tracking Data** | Observabilidade do que aconteceu | Traces, logs, eval results, CSAT scores, latency metrics |

Cada tipo requer schema próprio, pipeline de ingestão próprio, e estratégia de atualização própria. Tentar usar o mesmo pipeline para ambos cria acoplamento que quebra quando um evolui.

---

## 3. Operational Lessons

### 3.1 What Worked

| Lição | Evidência |
|---|---|
| **Eval-first, model-last** | Modelo selecionado na semana 7 com 200 casos reais; "model selection became very quick" |
| **Living eval dataset** | Cresce de ~200 para N casos; cada incidente adiciona um caso; monotonic growth |
| **Behavioral eval catching redundant tool calls** | Um agente respondeu corretamente sobre saldo mas fez 3 chamadas DB + 2 APIs externas desnecessárias; detectado pela Layer 3 |
| **Centralized cross-framework tracing** | Múltiplos frameworks em múltiplas clouds → uma camada de tracing → consumidores padronizados |
| **Deterministic eval como primeira linha** | 47 PII breaches capturados na fase de testes, antes de produção |
| **Eval dashboard como superfície primária de detecção** | CSAT drops e regressões de qualidade detectados no dashboard, não em logs/APM |
| **Data foundation como investimento principal** | 60% do tempo do projeto alocado a dados; "Agents don't forgive you" |

### 3.2 What Failed

| Falha | Contexto | Custo |
|---|---|---|
| **POC de 6 meses / $85K sem observabilidade** | Construído sem evals, sem métricas, sem accountability. "Ninguém sabia se o sistema estava funcionando ou não." | $85.000 e 6 meses perdidos |
| **Model-first approach** | Selecionar modelo antes de construir infraestrutura de avaliação → debates subjetivos, sem dados para decidir | Semanas de debate substituídas por horas de eval |
| **Stale RAG data (vector DB desatualizado)** | Banco mudou taxas de juros, enviou emails, mas o vector DB não foi atualizado. CSAT caiu. | Danos de reputação, clientes recebendo informações erradas |
| **Agentes sem accountability design** | Sem tracing, sem métricas por agente, impossível atribuir falhas a componentes específicos | Debugging cego, finger-pointing entre times |

### 3.3 What Surprised

| Surpresa | Por que foi contraintuitivo |
|---|---|
| **Qualidade de dados consome 60% do projeto** | Esperava-se que model tuning ou prompt engineering dominasse o esforço; na prática, dados construídos para humanos não funcionam para agentes |
| **Observabilidade é gate regulatório, não nice-to-have** | Em mercados regulados (Europa), não se pode fazer onboarding de AI sem tracing — é pré-requisito de compliance, não decisão de engenharia |
| **Seleção de modelo pode ser adiada até a semana 7** | A intuição de "escolher o melhor modelo primeiro" é invertida: a infra de eval decide o modelo, não o contrário |
| **Behavioral eval revela o "caminho errado com resposta certa"** | Foco tradicional em avaliar a resposta final (Layer 2) esconde ineficiências que custam caro em escala |
| **Business-success-first pipeline funciona** | Definir sucesso em termos de negócio (60% deflection rate), criar golden answers manualmente, e só depois construir pipeline Python — mais rápido que começar pela engenharia |

---

## 4. Tradeoffs

### 4.1 Orchestrator-Worker vs Choreography

| Dimensão | Orchestrator-Worker | Choreography |
|---|---|---|
| **Controle** | Centralizado, previsível | Descentralizado, emergente |
| **Debugabilidade** | Alta (tudo passa pelo orchestrator) | Baixa (eventos assíncronos, difícil rastrear causalidade) |
| **Latência** | Maior (round-trips pelo coordenador) | Menor (comunicação direta entre agentes) |
| **Resiliência** | Single point of failure (orchestrator) | Sem single point, mas falhas parciais mais difíceis de detectar |
| **Recomendação** | Use quando compliance, auditoria, ou debugging são críticos | Use quando latência é o constraint dominante e os agentes são independentes |

### 4.2 Early vs Late Model Selection

| Abordagem | Vantagem | Desvantagem |
|---|---|---|
| **Early (tradicional)** | Time ganha familiaridade com o modelo | Escolha baseada em intuição/benchmarks públicos, não nos dados reais da empresa |
| **Late (eval-driven)** | Escolha baseada em desempenho real contra o eval dataset da empresa | Requer disciplina para construir infra de eval antes de qualquer experimentação com modelos |

**Recomendação de Bhaumik**: late selection. O eval dataset empresarial é o único benchmark que importa. Benchmarks públicos medem performance geral, não performance no domínio específico da empresa.

### 4.3 Behavioral Eval: Breadth vs Cost

| Tradeoff | Decisão |
|---|---|
| **Cobertura completa** de behavioral evals em cada commit | Custo proibitivo (rodar todos os cenários com tracing completo) |
| **Subset em CI** de behavioral evals | Menor cobertura, feedback mais rápido |
| **Solução híbrida**: CI roda subset estratificado por categoria; merge to main roda suite completa | Equilíbrio entre custo e cobertura |

### 4.4 Single Model vs Multi-Model Flexibility

| Abordagem | Risco |
|---|---|
| **Single model** | Vendor lock-in; se o provider muda o modelo, performance pode degradar sem aviso |
| **Multi-model architecture** | Complexidade operacional, mas permite testar novos modelos contra o eval dataset e trocar quando necessário |

**Recomendação**: arquitetura deve suportar model switching. Quando o provider atualiza o modelo, rode o eval dataset empresarial (não benchmarks públicos) para decidir se a troca é segura.

### 4.5 Data Quality Tolerance: Human-Forgiving vs Agent-Unforgiving

| Audiência | Tolerância a dados ruins | Exemplo |
|---|---|---|
| **Humanos** | Alta — inferem contexto, ignoram inconsistências, perdoam ambiguidades | Um humano lê um policy document desatualizado e pensa "isso deve ter mudado" |
| **Agentes** | Zero — tratam dados literalmente, amplificam inconsistências, respondem com confiança sobre informação errada | Um agente lê o mesmo documento stale e responde com confiança "sua taxa de juros é X%" |

Este gap de tolerância é o motivo pelo qual 60% do esforço vai para data foundation. Não é possível "consertar" dados ruins com prompts melhores.

---

## 5. Failure Patterns

### 5.1 The Demo Trap

| Elemento | Descrição |
|---|---|
| **Padrão** | Construir um agente que funciona perfeitamente em demo (5 queries) e assumir que está pronto para produção (20.000 queries/mês) |
| **Causa** | Demo não expõe: stale data, edge cases, PII leaks, tool call redundância, degradação sob carga |
| **Mitigação** | Eval dataset com 200+ casos reais + behavioral eval suite + tracing desde o dia 1 |
| **Severidade** | Critical — foi exatamente o que causou o fracasso do POC de $85K |

### 5.2 Missing Behavioral Eval Layer

| Elemento | Descrição |
|---|---|
| **Padrão** | Avaliar apenas a resposta final (Layer 1 + 2), ignorando o caminho que o agente percorreu |
| **Causa** | Behavioral eval é mais caro e complexo de implementar; times focam no que é fácil |
| **Mitigação** | Implementar Layer 3 com tracing de tool calls; detectar chamadas redundantes, loops, e APIs duplicadas |
| **Severidade** | High — "you can have the right answer with the wrong path" |

### 5.3 Stale RAG Data

| Elemento | Descrição |
|---|---|
| **Padrão** | Documentos de política/produto mudam na organização, mas o vector DB não é atualizado. Agente continua respondendo com embeddings antigos. |
| **Causa** | Pipeline de ingestão de dados não tem trigger automático quando documentos fonte mudam |
| **Mitigação** | Tracing detecta queda de CSAT → diagnóstico revela embeddings stale → pipeline de atualização automática |
| **Severidade** | Critical — danos de reputação e compliance quando clientes recebem informação errada |

### 5.4 Uncategorized Eval Dataset

| Elemento | Descrição |
|---|---|
| **Padrão** | Eval dataset cresce sem categorização, ownership, ou manutenção → vira monólito ingerenciável |
| **Causa** | Times adicionam casos mas ninguém é dono da estrutura |
| **Mitigação** | Categorizar por domínio (security, login, tool calls, knowledge), atribuir owners, particionar para CI vs full suite |
| **Severidade** | Medium — não quebra o sistema imediatamente, mas corrói a utilidade do dataset ao longo do tempo |

### 5.5 Opaque Prompt History

| Elemento | Descrição |
|---|---|
| **Padrão** | Prompts versionados sem documentação de causalidade; commits genéricos ("updated prompt", "improved response") |
| **Causa** | Prompt engineering tratado como arte, não como engenharia; falta de disciplina de change management |
| **Mitigação** | Prompt commit message discipline: documentar trigger, diagnóstico, e intenção preditiva |
| **Severidade** | High — impossibilita rollback informado e debug de regressões de prompt |

### 5.6 PII Breaches

| Elemento | Descrição |
|---|---|
| **Padrão** | Dados pessoais (CPF, telefone, endereço) vazam em respostas do agente porque o modelo não sabe quais campos são sensíveis |
| **Causa** | Falta de PII tagging no data catalog; modelo trata todos os dados como públicos |
| **Mitigação** | Unity Catalog com PII tagging → governance context injetado no prompt → modelo sabe quais campos não pode expor |
| **Severidade** | Critical — 47 breaches capturados na fase de testes; cada um seria um incidente de compliance em produção |

### 5.7 Reliance on Public Benchmarks

| Elemento | Descrição |
|---|---|
| **Padrão** | Selecionar modelo baseado em benchmarks públicos (MMLU, HumanEval, etc.) em vez de performance no domínio específico da empresa |
| **Causa** | Benchmarks públicos são a única métrica disponível antes de construir eval dataset próprio |
| **Mitigação** | Construir eval dataset empresarial primeiro; usar apenas ele para decidir qual modelo usar e quando trocar |
| **Severidade** | Medium — pode levar a escolhas de modelo subótimas para o domínio específico |

### 5.8 No Accountability Design

| Elemento | Descrição |
|---|---|
| **Padrão** | Sistema multi-agente sem tracing por agente, sem métricas individuais, sem capacidade de atribuir falhas |
| **Causa** | Tracing implementado como afterthought ou não implementado |
| **Mitigação** | Centralized trace collection desde o dia 1; cada agente tem seu próprio span; métricas por agente visíveis no dashboard |
| **Severidade** | Critical — o POC de $85K falhou exatamente por falta de accountability: "ninguém sabia se o sistema estava funcionando" |

---

## 6. Key Quotes

> **1.** "Agents don't forgive you. Data that works for humans — who infer context, ignore inconsistencies, and forgive ambiguity — fails catastrophically with agents that treat every data point literally."

> **2.** "You can have the right answer with the wrong path. The agent correctly tells you your balance but made 3 redundant database calls and 2 unnecessary API calls. Fine in a demo; expensive at 20,000 calls per month."

> **3.** "In Europe or regulated industries, you cannot even onboard AI into production without tracing. Observability isn't an engineering nice-to-have — it's a regulatory prerequisite."

> **4.** "Model selection became very quick once we had 200 real cases in our eval dataset. Weeks of subjective debate replaced by hours of data-driven comparison."

> **5.** "The eval dataset is a living organism. It starts with ~200 real cases from human agents. Every production failure adds a new case. The bigger it grows, the better your system becomes."

> **6.** "Every incident leaves a permanent scar in the test suite. That scar prevents the same failure from happening twice."

---

## 7. Synthesis

### 7.1 O Modelo Eval-as-Immune-System

A arquitetura de avaliação de Bhaumik funciona como um sistema imunológico para agentes em produção. A camada determinística (Layer 1) age como barreira inata — bloqueia patógenos conhecidos (PII, formatos inválidos) com regras rígidas. A camada semântica (Layer 2) age como imunidade adaptativa — aprende a reconhecer respostas de baixa qualidade contextual. A camada comportamental (Layer 3) é o equivalente a monitorar os órgãos internos — verifica se o metabolismo do agente (tool calls, API usage) está saudável, não apenas se o output final parece correto.

O living eval dataset é a memória imunológica: cada incidente deixa uma "cicatriz" permanente que previne reinfecção. Este modelo explica por que sistemas sem a camada 3 parecem saudáveis em demo mas colapsam em produção — é como ter um sistema imunológico que só olha para a pele (output final) e ignora falência de órgãos internos (tool loops, chamadas redundantes).

### 7.2 A Inversão do Model-Selection-First

O insight mais contraintuitivo do framework é a inversão temporal: selecionar o modelo na semana 7, não na semana 1. Esta inversão resolve um problema fundamental de causalidade — você não pode avaliar se um modelo é bom para o seu domínio até ter um eval dataset que represente esse domínio. Tentar escolher o modelo primeiro é como escolher uma lente antes de saber o que você vai fotografar.

Implicação para times de engenharia: parem de debater qual modelo usar. Invistam esse tempo em construir o eval dataset. O dataset responderá a pergunta com dados, não com opiniões.

### 7.3 O Regulatory Forcing Function na Observabilidade

Bhaumik revela um mecanismo de adoção que não é óbvio para times em mercados não regulados: a observabilidade não é adotada porque é boa prática de engenharia — é adotada porque reguladores a exigem. Este forcing function resolve o problema de incentivos: sem requerimento regulatório, times pulam tracing porque o custo é imediato e o benefício é futuro. Com requerimento regulatório, tracing é custo de entrada no mercado, não opção de engenharia.

Para times em mercados não regulados, o insight é: trate tracing como se fosse regulatório. O custo de não ter tracing (falhas invisíveis, debugging cego, incapacidade de atribuir falhas) é maior que o custo de implementá-lo.

### 7.4 O Data Quality Problem como Dominant Constraint

A alocação de 60% do tempo para data foundation é o dado mais revelador do case study. Não é prompt engineering, não é model tuning, não é arquitetura de agentes — é qualidade de dados. Isso reflete uma assimetria fundamental: ferramentas de dados evoluíram para servir consumo humano (dashboards, relatórios, análise), onde ambiguidade e inconsistência são toleradas. Agentes não têm essa tolerância.

A implicação arquitetural é profunda: o pipeline de dados para agentes precisa de um nível de qualidade (freshness guarantees, consistency checks, update triggers) que pipelines para consumo humano não precisam. Times que subestimam isso repetem o padrão do POC de $85K.

### 7.5 O Gap Entre Demo e Produção é Comportamental, Não Semântico

A distinção entre Layer 2 (semântica) e Layer 3 (comportamental) revela por que tantos agentes falham na transição demo → produção. Em demo, você avalia 5 queries e verifica se as respostas fazem sentido (Layer 2). Em produção com 20.000 chamadas/mês, o problema não é se as respostas fazem sentido — é quantas chamadas redundantes o agente faz para chegar nelas, se ele entra em loops, se consome APIs desnecessárias.

O gap demo→produção é fundamentalmente um gap de behavioral eval. Times que só investem em Layer 1 e 2 estão avaliando a pele do sistema enquanto os órgãos internos falham.

### 7.6 Governança como Pré-Produção, Não Post-Produção

Os 47 PII breaches capturados na fase de testes são o argumento mais forte para governance como pilar de design, não como auditoria post-hoc. Se a governance tivesse sido adicionada depois do deploy, cada um desses 47 breaches teria sido um incidente de compliance em produção. O PII tagging no catálogo de dados (Unity Catalog) injetando contexto de governance nos prompts é um padrão arquitetural que previne vazamentos antes que eles aconteçam — não um processo de revisão manual que os detecta depois.

---

*Síntese concluída a partir de 5 análises independentes de chunks do transcript da talk "The Production AI Playbook: Deploying Agents at Enterprise Scale" por Sandipan Bhaumik (Databricks), apresentada no AI Engineer Conference.*
