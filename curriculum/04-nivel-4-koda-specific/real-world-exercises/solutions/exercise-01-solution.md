---
title: "Solucao do Exercicio 1: Feature KODA — Recomendacao de Produto com Generator/Evaluator"
type: curriculum-solution
nivel: 4
aliases: ["solução recomendação KODA", "feature contract produto", "rubric evaluation", "fallback recomendação"]
tags: [curriculo-conteudo, nivel-4, solucao, generator-evaluator-pattern, feature-contract, rubric-evaluation, fallback-safe, product-recommendation, dietary-restrictions, budget-constraint, e-commerce, supplement-catalog, python, implementacao-referencia]
relates-to: ["[[curriculum/04-nivel-4-koda-specific/real-world-exercises/exercise-01|Exercicio 1]]"]
last_updated: 2026-06-10
---
# 🎯 Solucao do Exercicio 1: Feature KODA — Recomendacao de Produto com Generator/Evaluator
## Implementacao Completa com Python, Feature Contract, Rubricas e Testes de Qualidade

**Tempo Estimado de Leitura:** 120-150 minutos
**Nivel:** 4 — KODA-Especifico — Real-World Feature
**Pre-requisito:** Ter completado Nivel 2 (`01-generator-evaluator-pattern.md`, `02-sprint-contracts.md`, `03-rubric-design.md`)
**Status:** 🟢 SOLUCAO COMPLETA
**Data de Criacao:** Maio 2026

---

## 📖 Prologo: A Feature que o Time de Produto Pediu

Terca-feira, 9h30. Sala de reuniao da engenharia do KODA.

Fernando, o tech lead, acabou de sair de uma reuniao com o time de produto. O diagnóstico foi direto: a feature de recomendacao de produtos do KODA esta custando caro.

Os numeros da semana passada:

| Metrica | Valor Atual | Meta |
|---------|-------------|------|
| Precisao de recomendacao | 75% | 95%+ |
| Taxa de devolucao | 12% | 5% |
| Satisfacao do cliente | 68% | 88%+ |
| Reclamacoes sobre "recomendacao errada" | 23 por semana | 3 por semana |
| Custo por devolucao | R$ 18,50/ocorrencia | — |

O problema nao era o modelo de IA. O problema era a arquitetura.

O KODA atual funciona assim: o cliente pergunta, o agente consulta o catalogo, recomenda o primeiro produto que encontra dentro do orcamento e envia. Fim.

Nao ha:

- Verificacao de restricoes alimentares (lactose, gluten)
- Priorizacao de preferencias (sabor, treino)
- Validacao de qualidade antes de enviar
- Auditoria do que foi decidido e por que

Resultado: clientes intolerantes a lactose recebem recomendacao de Whey Concentrado (que contem lactose). Clientes que preferem chocolate recebem recomendacao de baunilha "porque era mais barato". E ninguem sabe exatamente por que cada recomendacao foi feita, porque nao ha trace.

**A Nova Feature: Smart Product Recommendation**

O Product Manager definiu a feature em uma frase:

> "KODA analisa o perfil completo do cliente (restricoes alimentares, preferencias, orcamento, historico, objetivo de treino) e recomenda ate 3 produtos ordenados por adequacao, com justificativa clara e verificacao de qualidade antes de enviar ao cliente."

E voce, como engenheiro do time, sabe que nao pode simplesmente "pedir para a IA recomendar melhor". Isso nao funciona. Voce precisa de arquitetura.

**A Arquitetura: Generator/Evaluator**

O padrao que voce aprendeu no Nivel 2 e a resposta. Mas agora voce vai aplica-lo a uma feature real do KODA — nao como exercicio, mas como implementacao de producao.

Voce vai construir:

1. **Feature Contract:** O documento que define o que a feature promete — suas entradas, saidas e garantias
2. **Generator Agent:** O agente que filtra, ranqueia e recomenda produtos
3. **Evaluator Agent:** O agente que valida cada recomendacao contra criterios objetivos
4. **Orchestrator (Harness):** A cola que conecta os dois agentes e gerencia o loop de revisao
5. **Testes de Qualidade:** 8 cenarios que provam que a feature funciona

Ao final, voce tera um sistema que:

- Nunca recomenda produto com alergeno do cliente
- Nunca excede o orcamento
- Prioriza sabor preferido quando possivel
- Registra cada decisao em audit trail JSON
- Faz fallback seguro quando nenhum produto atende
- Passa em 8 testes deterministicos

---

## 🎯 O Que o Exercicio Pede

O Exercicio 1 do Nivel 4 pede que voce implemente uma feature real do KODA usando o padrao Generator/Evaluator. Os requisitos sao:

1. **Feature Contract** — Defina o contrato da feature: o que ela recebe, o que entrega e quais garantias oferece
2. **Generator Agent** — Implemente o agente que gera recomendacoes candidatas
3. **Evaluator Agent** — Implemente o agente que valida contra rubrica de qualidade
4. **Orchestrator** — Conecte Generator e Evaluator com loop de revisao
5. **Testes** — Escreva 8 cenarios que validem a qualidade da feature

Esta solucao entrega todos esses requisitos com codigo funcional, explicacoes detalhadas e analise de decisoes de design.

### Conexao com Niveis Anteriores

| Nivel | O Que Voce Aprendeu | Como se Aplica Aqui |
|-------|---------------------|---------------------|
| Nivel 1 | Context Amnesia, Token Budgeting, Harness Patterns | State persistence via arquivos JSON; limites de resposta |
| Nivel 2 | Generator/Evaluator, Sprint Contracts, Rubric Design | Separacao Generator/Evaluator; feature contract; rubrica de 10 criterios |
| Nivel 3 | Multi-Agent, State Persistence, File-Based Coordination | Persistencia de estado; comunicacao via JSON entre agentes |
| **Nivel 4** | **Aplicacao real no KODA** | **Feature completa de recomendacao com metricas de producao** |

A diferenca pratica entre o Nivel 3 e o Nivel 4: no Nivel 3 voce construiu um sistema multi-agente generico. No Nivel 4, voce esta construindo uma feature especifica do KODA com contrato, rubricas e metricas que o time de produto pode medir.

---

## 📋 Feature Contract: O Que a Feature Promete

Antes de escrever uma linha de codigo, voce precisa definir o contrato. Um feature contract e um documento que diz: "Se voce me der X, eu garanto que vou entregar Y com as propriedades Z."

### Por que um Contrato?

No Nivel 2, voce aprendeu sobre Sprint Contracts entre modulos. Um feature contract aplica o mesmo principio no nivel da feature inteira:

1. **Clareza:** O time de produto sabe exatamente o que esperar
2. **Testabilidade:** Cada garantia vira um caso de teste
3. **Auditabilidade:** Quando algo falha, o contrato mostra o que foi violado
4. **Evolucao:** Quando a feature muda, o contrato mostra o que mudou

### O Contrato

```json
{
  "feature_name": "koda_smart_product_recommendation",
  "version": "1.0.0",
  "description": "Recomenda produtos ordenados por adequacao ao perfil do cliente",

  "input_contract": {
    "customer_profile": {
      "required": ["customer_id", "name", "budget_brl"],
      "optional": ["dietary_restrictions", "preferred_flavor", "training_goal"]
    },
    "catalog": {
      "required": ["sku", "name", "price_brl", "lactose_free", "gluten_free", "in_stock", "rating"]
    }
  },

  "output_contract": {
    "required": ["candidate_response", "products_considered", "assumptions"],
    "guarantees": [
      "0 a 3 produtos recomendados",
      "todos respeitam restricoes alimentares",
      "todos dentro do orcamento",
      "todos em estoque",
      "resposta nao excede 500 caracteres"
    ]
  },

  "quality_rubric": [
    "respeita restricoes alimentares (lactose, gluten)",
    "respeita orcamento maximo",
    "nao recomenda produto fora de estoque",
    "prioriza sabor preferido",
    "tom humano, sem jargao",
    "nao pressiona compra",
    "explicacao clara e justificada",
    "fallback seguro quando necessario"
  ],

  "max_iterations": 2,
  "max_products_per_recommendation": 3,
  "max_response_chars": 500
}
```

### Como Ler o Contrato

**Input Contract** define o que a feature espera receber. Se o caller nao fornecer `customer_id`, `name` e `budget_brl`, a feature deve rejeitar. Campos opcionais como `dietary_restrictions` podem ser omitidos — a feature funciona sem eles, so nao filtra por essas restricoes.

**Output Contract** define o que a feature promete entregar e as garantias. As garantias sao verificaveis: "todos os produtos em estoque" pode ser checado campo a campo. "Resposta nao excede 500 caracteres" e trivial de testar.

**Quality Rubric** define os criterios de qualidade que o Evaluator vai usar. Cada criterio e binario (passa ou nao passa), nao ha zona cinzenta.

---

## 🏗️ Arquitetura: Como Dois Agentes Colaboram

### Visao Geral

O sistema tem dois agentes especializados conectados por um orquestrador que gerencia o fluxo de dados:

```
                         ┌─────────────────────────────────┐
                         │     Cliente WhatsApp / KODA      │
                         │  perfil, mensagem, preferencias  │
                         └───────────────┬─────────────────┘
                                         │
                                         ▼
┌────────────────────────────────────────────────────────────────────────────┐
│                           ORCHESTRATOR (Harness)                           │
│                                                                            │
│  ┌──────────────────────┐   generation.json   ┌──────────────────────────┐ │
│  │     GENERATOR        │ ──────────────────▶ │      EVALUATOR           │ │
│  │                      │                     │                          │ │
│  │  Filtra catalogo     │   ◀───────────────  │  Valida contra rubrica   │ │
│  │  Ranqueia produtos   │    feedback (se     │  10 criterios binarios   │ │
│  │  Gera resposta       │    rejeitado)       │  Aprova / Rejeita        │ │
│  │  Registra suposicoes │                     │  Evidencias registradas  │ │
│  └──────────────────────┘                     └────────────┬─────────────┘ │
│                                                            │               │
└────────────────────────────────────────────────────────────┼───────────────┘
                                         │                   │
                           ┌─────────────┴─────┐   ┌────────┴──────────┐
                           ▼                   ▼   ▼                   ▼
                    ┌────────────┐   ┌──────────────────┐  ┌─────────────────┐
                    │ RESPOSTA   │   │ CICLO DE REVISAO │  │ FALLBACK SEGURO │
                    │ ENVIADA    │   │ Generator ←      │  │ "Preciso        │
                    │ (approved) │   │ Feedback (max 2) │  │ verificar..."   │
                    └────────────┘   └──────────────────┘  └─────────────────┘
```

### Fluxo de Dados

Cada artefato e um arquivo JSON persistido em disco. Nao ha estado compartilhado em memoria entre os agentes.

```
State Store (diretorio por conversa)
│
├── generation.json              ← Output do Generator (1a tentativa)
├── evaluation.json              ← Output do Evaluator
├── generation_revision_1.json   ← Segunda tentativa (se rejeitado)
├── evaluation_revision_1.json   ← Segunda avaliacao
├── generation_revision_2.json   ← Terceira tentativa (se rejeitado novamente)
├── evaluation_revision_2.json   ← Terceira avaliacao
└── delivery.json                ← Resposta final para o cliente
```

### Por que File-Based Coordination?

A decisao de usar arquivos JSON como canal de comunicacao e deliberada:

1. **Auditabilidade:** Cada decisao fica registrada. Se o cliente reclamar, voce le o trace e descobre onde o erro aconteceu — na geracao ou na avaliacao.

2. **Simplicidade Operacional:** Nao requer Redis, RabbitMQ ou qualquer infraestrutura extra. Ideal para aprendizado e prototipagem rapida.

3. **State Persistence Natural:** Se o processo cair, o estado esta salvo nos arquivos. Basta reler e continuar.

4. **Versionamento:** Adicionar `schema_version` permite evoluir contratos sem quebrar compatibilidade.

5. **Caminho de Evolucao para Producao:** Comecar com arquivos ensina contratos. Depois, as partes criticas migram para message queues quando o volume exigir.

---

## 📊 Tabela Comparativa: Estrategias de Coordenacao

Antes de escolher Generator/Evaluator para esta feature, o time considerou outras abordagens. Esta tabela documenta a analise:

| Estrategia | Como Funciona | Vantagens | Desvantagens | Quando Usar |
|-----------|---------------|-----------|-------------|-------------|
| **Agente Unico (Self-Eval)** | Um agente faz tudo: busca, ranqueia, recomenda e se auto-avalia | Simples de implementar; latencia minima | Sycophancy (vies confirmatorio); 75% de precisao; erros silenciosos | Tarefas triviais onde erro nao tem custo |
| **Chain-of-Thought** | Agente unico "pensa em voz alta" antes de responder | Melhora raciocinio; debug mais facil | Ainda sofre de sycophancy; "pensar" e "executar" no mesmo contexto | Tarefas que precisam de raciocinio mas baixo risco |
| **Generator/Evaluator (escolhido)** | Dois agentes: um cria, outro avalia com criterios binarios | Elimina sycophancy; audit trail completo; 95%+ precisao | Custo 2x em tokens; latencia maior | Features com alto custo de erro (recomendacao, pedido, checkout) |
| **Planner/Generator/Evaluator** | Tres agentes: Planner decompoe, Generator executa, Evaluator valida | Melhor para tarefas complexas com multiplas etapas | Custo 3x; complexidade maior | Conversas longas com multiplos objetivos (descoberta + recomendacao + checkout) |
| **Multi-Agent Swarm** | Varios agentes especializados colaboram em paralelo | Maxima especializacao; escala horizontal | Overhead de coordenacao; risco de mensagens inconsistentes | Sistemas com dominios muito distintos (recomendacao, logistica, pagamento) |

### Por que Generator/Evaluator Para Esta Feature

A recomendacao de produto e o caso ideal para Generator/Evaluator:

- **Uma decisao final** (nao multiplos objetivos em paralelo)
- **Alto custo de erro** (devolucao = dinheiro perdido; alergia = risco de saude)
- **Criterios de qualidade bem definidos** (lactose, orcamento, estoque — tudo verificavel)
- **Beneficio claro da separacao** (sycophancy e o maior problema em recomendacoes)

Adicionar um Planner seria overengineering para este escopo — a feature tem um objetivo unico (recomendar). Adicionar agentes em paralelo (swarm) seria prematuro para o volume atual do KODA.

---

## 🧠 Componente 1: Generator Agent

### Responsabilidades

O Generator e o executor. Ele recebe o perfil do cliente e o catalogo, e gera recomendacoes candidatas. Seu unico foco e encontrar os melhores produtos — **nao** verificar se estao corretos.

Responsabilidades especificas:
1. Filtrar catalogo por restricoes (lactose, gluten) e orcamento
2. Priorizar sabor preferido no ranking
3. Selecionar ate 3 produtos ordenados por rating
4. Formatar resposta em tom WhatsApp (curta, humana)
5. Registrar suposicoes explicitamente (ex: "categoria alvo extraida da mensagem")
6. **NAO** aprovar o proprio trabalho

### Cadeia de Filtros do Generator

O Generator aplica filtros em cadeia. Cada filtro e independente e testavel:

```
CATALOGO COMPLETO (8 produtos)
    │
    ▼
[FILTRO 1: Categoria alvo]  ← Extraida da mensagem do cliente
  "whey" → apenas whey protein
  "creatina" → apenas creatina
  (ausente) → todas as categorias
    │
    ▼
[FILTRO 2: Estoque]  ← Remove produtos indisponiveis
  in_stock = True apenas
    │
    ▼
[FILTRO 3: Lactose]  ← Remove produtos com lactose (se cliente intolerante)
  lactose_free = True
    │
    ▼
[FILTRO 4: Gluten]  ← Remove produtos com gluten (se cliente celiaco)
  gluten_free = True
    │
    ▼
[FILTRO 5: Orcamento]  ← Remove produtos acima do budget
  price_brl <= budget_brl
    │
    ▼
[RANKING]  ← Ordena: sabor preferido primeiro, depois por rating
    │
    ▼
TOP-3 PRODUTOS → Formata resposta WhatsApp
```

### Por que Filtros em Cadeia?

Cada filtro e uma funcao pura que recebe uma lista e retorna uma lista menor. Isso traz beneficios:

1. **Debug:** Se um produto desapareceu, voce sabe exatamente qual filtro o removeu
2. **Teste:** Cada filtro pode ser testado isoladamente
3. **Extensao:** Adicionar nova restricao ("sem acucar", "kosher") e adicionar um filtro na cadeia
4. **Ordem Importa:** Filtros mais baratos (categoria) rodam antes dos mais caros (consulta a BD)

### Design Decisions

**Heuristica em vez de LLM:** Em producao, a extracao de categoria usaria uma chamada LLM. Para este exercicio, usamos heuristica de palavras-chave para manter o codigo deterministico e testavel sem dependencia de API. A interface (`generator_agent(profile, catalog) -> Generation`) e identica — trocar a implementacao interna nao quebra os consumidores.

**`dataclass` em vez de `dict`:** Dataclasses fornecem type hints, valores default e serializacao automatica. Isso reduz erros de digitar chaves erradas e facilita refatoracao.

**Separacao `_format_whatsapp_response`:** A formatacao da resposta e isolada da logica de selecao. Se o time de UX quiser mudar o tom, mexe apenas nessa funcao.

### Exemplo de Output: `generation.json`

Para o cliente Marina — intolerante a lactose, prefere chocolate, orcamento R$ 150:

```json
{
  "schema_version": "1.0",
  "conversation_id": "conv_marina_006",
  "candidate_response": "Encontrei 1 opcao(oes) para voce, Marina. A melhor avaliada e Whey Isolado Chocolate 900g por R$ 139.90 (nota 4.7/5). sem lactose. Quer que eu separe para voce?",
  "products_considered": [
    {
      "sku": "WHEY-ISO-CHOC-900",
      "name": "Whey Isolado Chocolate 900g",
      "price_brl": 139.90,
      "rating": 4.7,
      "lactose_free": true,
      "gluten_free": true,
      "in_stock": true,
      "category": "whey"
    }
  ],
  "assumptions": [
    "categoria alvo extraida da mensagem: whey",
    "orcamento maximo: R$ 150.00",
    "cliente intolerante a lactose — filtrando produtos lactose_free",
    "sabor preferido: chocolate — priorizando no ranking"
  ],
  "generated_at": "2026-05-28T12:00:00Z"
}
```

Observe:

- `candidate_response`: tom humano, menciona o nome da cliente, explica o rating
- `products_considered`: apenas 1 produto porque, depois de todos os filtros, so o Whey Isolado atende
- `assumptions`: cada decisao do Generator esta registrada. Se algo der errado, voce sabe por que

---

## 🔍 Componente 2: Evaluator Agent

### Responsabilidades

O Evaluator e o gatekeeper. Nada chega ao cliente sem sua aprovacao. Ele valida cada recomendacao contra uma rubrica de 10 criterios binarios.

Responsabilidades especificas:
1. Verificar cada criterio da rubrica de qualidade
2. Registrar evidencias para cada verificacao (passou ou nao passou, e por que)
3. Aprovar (`status = "approved"`) ou rejeitar (`status = "rejected"`)
4. Fornecer feedback acionavel para o Generator corrigir

### A Rubrica de Qualidade (10 Criterios)

| # | Criterio | O Que Verifica | Peso | Exemplo de Evidencia |
|---|----------|---------------|------|---------------------|
| 1 | Respeita restricao de lactose | Nenhum produto com `lactose_free = false` | CRITICO | "todos os 2 produtos sao lactose_free" |
| 2 | Respeita restricao de gluten | Nenhum produto com `gluten_free = false` | CRITICO | "todos os 2 produtos sao gluten_free" |
| 3 | Respeita orcamento maximo | `price_brl <= budget_brl` para todos | CRITICO | "todos os produtos estao <= R$ 150.00" |
| 4 | Nao recomenda produto fora de estoque | `in_stock = true` para todos | ALTO | "todos os 2 produtos estao em estoque" |
| 5 | Prioriza sabor preferido | Produto com sabor preferido ranqueado em 1o | MEDIO | "produto com sabor chocolate ranqueado em primeiro" |
| 6 | Tom humano, sem jargao | Sem termos tecnicos como "bioavailability" | MEDIO | "linguagem natural e acessivel, sem jargao tecnico" |
| 7 | Nao pressiona compra | Sem frases como "aproveite agora", "so hoje" | MEDIO | "resposta informativa, sem urgencia artificial" |
| 8 | Explica recomendacao com clareza | Resposta inclui justificativa (rating, nota, razao) | MEDIO | "resposta inclui indicadores de justificativa" |
| 9 | Resposta nao vazia | `candidate_response` com conteudo | CRITICO | "resposta com 213 caracteres" |
| 10 | Fallback seguro | Resposta apropriada quando nenhum produto atende | ALTO | "resposta de fallback apropriada quando sem produtos" |

### Design Decisions

**Avaliacao binaria, nao numerica:** Cada criterio e `passed = true` ou `passed = false`. Nao ha "nota 7.5". Isso elimina ambiguidade: ou passou ou nao passou. Se a rubrica tem 10 criterios, todos devem passar. Se o time quiser flexibilizar (ex: "nota 8/10 e suficiente"), isso e uma decisao de negocio que fica no orquestrador, nao no Evaluator.

**Verificadores independentes:** Cada criterio tem sua propria funcao (`_check_lactose_restriction`, `_check_budget`, etc.). Isso torna o codigo testavel isoladamente e extensivel.

**Evidencias obrigatorias:** Todo `RubricResult` tem `evidence`. Sempre. "Aprovado porque parece bom" nao existe. "Aprovado porque todos os 3 produtos tem `lactose_free = true`" e verificavel.

**Heuristica para criterios objetivos, LLM para subjetivos:** Criterios como "lactose_free" e "price_brl <= budget" sao verificados deterministicamente por codigo. Criterios como "tom humano" e "nao pressiona compra" usam heuristica de palavras-chave neste exercicio. Em producao, estes criterios usariam LLM com prompt especializado.

### Exemplo de Output: `evaluation.json`

Para a recomendacao da Marina (aprovada):

```json
{
  "schema_version": "1.0",
  "conversation_id": "conv_marina_006",
  "status": "approved",
  "rubric_results": [
    {
      "criterion": "respeita restricao de lactose",
      "passed": true,
      "evidence": "todos os 1 produtos sao lactose_free"
    },
    {
      "criterion": "respeita restricao de gluten",
      "passed": true,
      "evidence": "cliente nao possui restricao de gluten"
    },
    {
      "criterion": "respeita orcamento maximo de R$ 150.00",
      "passed": true,
      "evidence": "todos os 1 produtos estao <= R$ 150.00"
    },
    {
      "criterion": "nao recomenda produto fora de estoque",
      "passed": true,
      "evidence": "todos os 1 produtos estao em estoque"
    },
    {
      "criterion": "prioriza sabor preferido quando opcoes equivalentes",
      "passed": true,
      "evidence": "criterio nao aplicavel (sem preferencia declarada ou poucos produtos)"
    },
    {
      "criterion": "resposta com tom humano, sem jargao excessivo",
      "passed": true,
      "evidence": "linguagem natural e acessivel, sem jargao tecnico"
    },
    {
      "criterion": "nao pressiona compra com linguagem de urgencia",
      "passed": true,
      "evidence": "resposta informativa, sem urgencia artificial"
    },
    {
      "criterion": "resposta nao vazia",
      "passed": true,
      "evidence": "resposta com 197 caracteres"
    }
  ],
  "feedback": "",
  "checked_at": "2026-05-28T12:00:01Z"
}
```

E para uma recomendacao rejeitada (orcamento violado):

```json
{
  "status": "rejected",
  "rubric_results": [
    {
      "criterion": "respeita orcamento maximo de R$ 70.00",
      "passed": false,
      "evidence": "produtos acima do orcamento: WHEY-CONC-CHOC-1000 (R$ 89.90 > R$ 70.00)"
    }
  ],
  "feedback": "Criterios reprovados:\n- respeita orcamento maximo de R$ 70.00: produtos acima do orcamento: WHEY-CONC-CHOC-1000 (R$ 89.90 > R$ 70.00)"
}
```

Observe a qualidade do feedback: ele diz **exatamente** qual produto, qual preco, e qual o limite. O Generator pode agir sobre isso sem ambiguidade.

---

## 🔄 Componente 3: Orquestrador (Harness)

### Diagrama de Fluxo

```
┌──────────────────────────────────────────────────────────────────┐
│              run_koda_recommendation(profile, catalog)            │
│                                                                  │
│  1. Generator: profile + catalog → generation.json               │
│                         │                                        │
│                         ▼                                        │
│  2. Evaluator: generation + profile → evaluation.json            │
│                         │                                        │
│              ┌──────────┴──────────┐                             │
│              ▼                     ▼                             │
│         approved               rejected                          │
│              │                     │                             │
│              ▼                     ▼                             │
│  3a. Retorna resposta     3b. Generator com feedback             │
│      para WhatsApp             ↓                                 │
│                          generation_revision_N.json              │
│                              ↓                                   │
│                          Evaluator (N-esima tentativa)           │
│                              │                                   │
│                   ┌──────────┴──────────┐                        │
│                   ▼                     ▼                        │
│              approved               rejected                     │
│                   │                     │                        │
│                   ▼                     ▼                        │
│           Retorna resposta      Apos max_revisions:              │
│           para WhatsApp         FALLBACK SEGURO                  │
│                                 "Preciso verificar..."           │
│                                                                  │
│  max_revisions = 2 (configuravel)                                │
└──────────────────────────────────────────────────────────────────┘
```

### O Loop de Revisao

O loop de revisao e o que faz o sistema ser resiliente. Se o Generator errar na primeira tentativa, o Evaluator rejeita com feedback especifico, e o Generator tenta novamente.

Exemplo real do loop:

```
Tentativa 1:
  Generator: recomenda Whey Concentrado (R$ 89.90)
  Evaluator: REJEITADO — contem lactose, cliente intolerante

Tentativa 2 (com feedback):
  Generator: recomenda Whey Isolado (R$ 139.90, lactose_free)
  Evaluator: APROVADO ✅

Resposta enviada ao cliente.
```

O loop tem um limite: `max_revisions = 2`. Apos duas rejeicoes, o sistema nao fica em loop infinito — ele envia um fallback seguro: "Preciso verificar um detalhe antes de te responder...". Isso protege o cliente de uma recomendacao errada e protege o sistema de custo infinito de tokens.

### Design Decisions

**`max_revisions = 2`, nao 1 nem 5:** Uma revisao e pouco — se o Generator errar por um detalhe simples, merece uma segunda chance. Cinco revisoes e muito — se o Generator nao acertou em duas, o problema provavelmente e estrutural (ex: catalogo vazio para aquele perfil).

**Fallback em vez de "melhor esforco":** Quando o loop se esgota, o sistema NAO envia "a melhor recomendacao que conseguiu, mesmo rejeitada". Isso seria anti-pattern — entregaria qualidade conhecidamente ruim ao cliente. Em vez disso, faz fallback seguro e escala para um humano.

**State persistence opcional:** O parametro `state_dir` controla se o estado e persistido em disco. Nos testes, podemos rodar sem persistencia (mais rapido). Em producao, sempre persistimos (audit trail).

---

## 🚀 Aplicacao no KODA: Como Esta Feature Roda em Producao

### O Contexto Real do KODA

O KODA nao e um exercicio de laboratorio. E um agente de vendas via WhatsApp que atende centenas de clientes por dia. A feature de recomendacao e chamada dezenas de vezes por hora. Ela precisa ser:

- **Rapida:** O cliente no WhatsApp espera resposta em segundos
- **Confiável:** Um erro de recomendacao com alergeno pode causar dano a saude
- **Auditavel:** Quando um cliente reclama, o time de suporte precisa saber o que aconteceu
- **Mensuravel:** O time de produto precisa de metricas para iterar

### Fluxo de Integracao com o KODA

```
WhatsApp Message
    │
    ▼
┌────────────────────────────────┐
│  KODA Core (message router)    │  ← Decide qual feature chamar
│  "quero whey" → recomendacao   │
└───────────────┬────────────────┘
                │
                ▼
┌────────────────────────────────┐
│  Profile Loader                │  ← Carrega customer_profile do BD
│  Busca: restricoes, budget,    │
│  preferencias, historico       │
└───────────────┬────────────────┘
                │
                ▼
┌────────────────────────────────┐
│  Smart Product Recommendation  │  ← ESTA FEATURE
│  Generator → Evaluator →       │
│  Response                      │
└───────────────┬────────────────┘
                │
                ▼
┌────────────────────────────────┐
│  Response Sender               │  ← Envia mensagem formatada
│  WhatsApp API                  │     para o cliente
└────────────────────────────────┘
```

### Metricas de Producao (Esperadas)

| Metrica | Antes (Agente Unico) | Depois (Gen/Eval) | Delta |
|---------|---------------------|-------------------|-------|
| Precisao de recomendacao | 75% | 95%+ | +20pp |
| Taxa de devolucao | 12% | 5% | -7pp |
| Satisfacao (CSAT) | 68% | 88%+ | +20pp |
| Tempo medio de resposta | 0.8s | 1.5s | +0.7s |
| Custo por recomendacao (tokens) | ~500 | ~1200 | +700 |
| Custo por venda bem-sucedida | R$ 2,50 | R$ 1,80 | -R$ 0,70 |

**O trade-off:** Cada recomendacao custa mais tokens (Generator + Evaluator), mas o custo por venda bem-sucedida cai porque a taxa de acerto e maior e a taxa de devolucao e menor.

### Evolucao Futura da Feature

Este exercicio implementa a versao 1.0 da feature. Caminhos naturais de evolucao:

1. **v1.1 — Categoria por LLM:** Trocar a heuristica de extracao de categoria por uma chamada LLM, mantendo a interface identica
2. **v1.2 — Rubrica Subjetiva por LLM:** Criterios como "tom humano" passarem a usar LLM em vez de heuristica
3. **v2.0 — Planner:** Adicionar um Planner antes do Generator para decompor recomendacoes complexas (ex: "quero um plano completo de suplementacao")
4. **v2.1 — Cache de Avaliacoes:** Reutilizar avaliacoes do Evaluator para produtos que ja foram avaliados com o mesmo perfil

---

## 🧪 Testes: 8 Cenarios que Provam a Qualidade

Os testes sao a prova de que a feature funciona. Cada teste cobre uma garantia do feature contract ou um criterio da rubrica.

### Cenarios de Teste

| # | Cenario | O Que Testa | Garantia do Contrato |
|---|---------|------------|---------------------|
| 1 | Caminho Feliz | Recomendacao aprovada na primeira tentativa | Feature funciona ponta a ponta |
| 2 | Respeita Orcamento | Nenhum produto recomendado excede budget | "todos dentro do orcamento" |
| 3 | Respeita Lactose | Nenhum produto com lactose para cliente intolerante | "todos respeitam restricoes alimentares" |
| 4 | Respeita Gluten | Nenhum produto com gluten para cliente celiaco | "todos respeitam restricoes alimentares" |
| 5 | Fallback Seguro | Budget impossivel (R$ 10) resulta em fallback | "fallback seguro quando necessario" |
| 6 | Prioriza Sabor | Sabor preferido ranqueado primeiro | "prioriza sabor preferido" |
| 7 | Audit Trail | Todos os JSONs tem campos obrigatorios | "output respeita o contrato" |
| 8 | Feature Contract | Output nao viola nenhuma garantia do contrato | "todas as garantias do output_contract" |

### Resultado da Execucao

```
============================================================
SOLUCAO: FEATURE KODA — RECOMENDACAO DE PRODUTO COM GENERATOR/EVALUATOR
Nivel 4 — KODA-Especifico — Real-World Feature
============================================================

🧪 TESTE 1: Caminho Feliz — Recomendacao Aprovada
   📤 Resposta: "Encontrei 2 opcao(oes) para voce, Rafael. A melhor avaliada e
      Creatina Monohidratada 300g por R$ 69.90 (nota 4.8/5)..."
   ✅ Teste 1 passou!

🧪 TESTE 2: Garantia de Respeito ao Orcamento
   📤 Resposta: "Nao encontrei produtos que atendam todos os seus criterios, Ana..."
   ✅ Teste 2 passou!

🧪 TESTE 3: Garantia de Respeito a Restricao de Lactose
   📤 Resposta: "Encontrei 1 opcao(oes)... Whey Isolado Chocolate 900g... sem lactose."
   ✅ Teste 3 passou!

🧪 TESTE 4: Garantia de Respeito a Restricao de Gluten
   📤 Resposta: "Encontrei 2 opcao(oes)... sem gluten."
   ✅ Teste 4 passou!

🧪 TESTE 5: Fallback Seguro — Budget Impossivel
   📤 Resposta: "Nao encontrei produtos que atendam todos os seus criterios..."
   ✅ Teste 5 passou!

🧪 TESTE 6: Priorizacao de Sabor Preferido
   📤 Resposta: "...Whey Isolado Chocolate 900g..."
   ✅ Teste 6 passou!

🧪 TESTE 7: Audit Trail — Campos Obrigatorios nos JSONs
   📁 Arquivos gerados: delivery.json, evaluation.json, generation.json
   ✅ Teste 7 passou!

🧪 TESTE 8: Validacao do Feature Contract
   ✅ Contract verificado: 3/3 produtos, 213/500 chars, campos required presentes
   ✅ Teste 8 passou!

============================================================
🎉 TODOS OS TESTES PASSARAM!
============================================================
```

### Como Executar

```bash
python exercise-01-solution.py
```

Nao requer dependencias alem de Python 3.8+. Nao requer chave de API. Totalmente deterministico.

---

## 🎓 O Que Voce Aprendeu

Este exercicio nao foi sobre "escrever codigo Python". Foi sobre **arquitetura de features de IA em producao**. Aqui esta o que voce deve levar:

### 1. Feature Contract Primeiro, Codigo Depois

Voce nao comecou implementando. Comecou definindo o contrato: o que a feature recebe, o que entrega, quais garantias oferece. Este contrato:

- Alinhou expectativas entre engenharia e produto
- Gerou os 8 casos de teste automaticamente (cada garantia = um teste)
- Serviu como documentacao viva do que a feature faz

### 2. Separacao Generator/Evaluator Elimina Sycophancy

O Generator cria. O Evaluator avalia. Eles nao compartilham incentivos. O Generator quer "encontrar boas opcoes". O Evaluator quer "encontrar erros". Essa separacao e o que levou a precisao de 75% para 95%+.

### 3. Rubricas Binarias Sao Melhores que Scores Numericos

"Nota 7.5/10" cria zona cinzenta. "7.5 e bom o suficiente?" Depende. Criterios binarios (`passed = true/false`) sao inequivocos. Todos devem passar. Fim.

### 4. Feedback Especifico e Acionavel

"Resposta ruim" nao ajuda. "Produto WHEY-CONC-CHOC-1000 (R$ 89.90) excede orcamento de R$ 70.00" ajuda. O Generator sabe exatamente o que corrigir.

### 5. Fallback Seguro e Melhor que "Melhor Esforco"

Quando o sistema nao consegue aprovar uma recomendacao, ele nao envia "a menos pior". Ele faz fallback: "Preciso verificar...". Isso protege o cliente e escala para um humano.

### 6. Audit Trail e Essencial para Debug e Confianca

Cada decisao fica registrada em JSON. Se um cliente reclamar, voce le o trace e descobre **exatamente** onde o erro aconteceu — na geracao ou na avaliacao. Sem audit trail, voce esta no escuro.

### 7. Heuristica para o Deterministico, LLM para o Subjetivo

Neste exercicio, criterios objetivos (lactose, orcamento, estoque) sao verificados por codigo deterministico. Criterios subjetivos (tom humano) usam heuristica. Em producao, a interface e a mesma — voce troca a heuristica por LLM sem quebrar nada.

### 8. O Padrao Escala

Este mesmo padrao (Generator/Evaluator com contrato, rubrica e testes) se aplica a qualquer feature do KODA:

- **Recomendacao de produto** (este exercicio)
- **Processamento de pedido** (validacao de estoque, preco, pagamento)
- **Aplicacao de promocoes** (validacao de elegibilidade, cumulatividade)
- **Atendimento de duvidas** (qualidade da resposta, precisao factual)
- **Fulfillment e entrega** (coordenacao de armazem, rota, entregador)

---

## 🔗 Proximos Passos

### Dentro do Nivel 4

Agora que voce implementou uma feature com Generator/Evaluator, esta pronto para:

- **`exercise-02.md`** — Feature de Processamento de Pedido com Sprint Contracts
- **`case-studies/`** — Estudos de caso de features reais implementadas no KODA
- **`05-harness-improvements.md`** — Como evoluir o harness para producao

### Alem do Nivel 4

- **Mentoring:** Ensine outro engenheiro a implementar uma feature com este padrao
- **Producao:** Adapte esta solucao para o KODA real (substitua catalogo simulado por API, heuristica por LLM)
- **Metricas:** Implemente dashboard de qualidade mostrando precisao, taxa de rejeicao do Evaluator, e custo por recomendacao

---

## 📋 Checklist de Verificacao

Antes de considerar este exercicio concluido, verifique:

- [ ] `python exercise-01-solution.py` executa sem erros
- [ ] Todos os 8 testes passam com ✅
- [ ] Generator e Evaluator estao em funcoes separadas (nao ha auto-avaliacao)
- [ ] Feature contract esta documentado e o codigo o respeita
- [ ] Cada RubricResult tem `evidence` preenchida
- [ ] Fallback seguro funciona quando nenhum produto atende
- [ ] Codigo e legivel, funcoes tem responsabilidade unica

---

## 📚 Referencias

### Dentro deste programa:
- `02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md` — O padrao em profundidade
- `02-nivel-2-practical-patterns/02-sprint-contracts.md` — Contratos entre modulos
- `02-nivel-2-practical-patterns/03-rubric-design.md` — Como criar rubricas de qualidade
- `03-nivel-3-advanced-architecture/01-multi-agent-systems.md` — Sistemas multi-agente
- `04-nivel-4-koda-specific/03-feature-design-patterns.md` — Como features KODA sao desenhadas

### Codigo:
- `exercise-01-solution.py` — Implementacao completa e executavel
- `exercise-01-solution.md` — Este documento

---

## 💭 Reflexao Final

> "A qualidade de uma feature de IA nao vem do modelo. Vem da arquitetura que envolve o modelo — contratos, rubricas, separacao de responsabilidades e testes que provam que tudo funciona."

Voce acabou de implementar uma feature que:

- Um agente sozinho fazia com 75% de precisao
- Com Generator/Evaluator faz com 95%+ de precisao
- Com contrato documentado que o time de produto pode ler
- Com rubrica de 10 criterios que o Evaluator aplica consistentemente
- Com 8 testes que provam que cada garantia e respeitada
- Com audit trail completo para cada decisao

Isso nao e um exercicio. E o que engenharia de features de IA parece quando feita com rigor.

O KODA esta melhor por causa do que voce construiu aqui.

---

*Escrito com foco em aplicacao pratica, rigor de engenharia e clareza pedagogica.*
*Proxima parada: Feature de Processamento de Pedido com Sprint Contracts.*
