---
title: "📖 GLOSSÁRIO: Termos Essenciais"
type: curriculum-index
aliases: ["glossario", "termos", "definicoes"]
tags: [curriculo-conteudo, reference]
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

## G

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

### Nível 3 (Arquitetura Avançada)
- Multi-Agent System
- Memory/State, Compaction
- Harness Evolution
- Closed-Loop Company, Skillify Pipeline, Context Progressive Disclosure
- Architecture Decision Record

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
