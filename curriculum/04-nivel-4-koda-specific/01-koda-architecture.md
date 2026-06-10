---
title: "Arquitetura KODA: O Sistema que Transformou um Chatbot em uma Operação Comercial"
type: curriculum-lesson
nivel: 4
aliases: []
tags: [curriculo-conteudo, nivel-4, koda, arquitetura-de-agentes, pipeline-de-vendas, integracao-whatsapp-business, coordenacao-multi-agente, persistencia-de-estado, fluxo-de-dados-end-to-end, auditoria-e-observabilidade, tratamento-de-erros, seguranca-operacional, evolucao-de-harness]
last_updated: 2026-06-10
---
# 🏗️ Arquitetura KODA: O Sistema que Transformou um Chatbot em uma Operação Comercial
## Visão Completa da Arquitetura do Agente de Vendas via WhatsApp — Componentes, Fluxo de Dados, Integração e Pipeline

**Tempo Estimado:** 90 minutos  
**Nível:** 4 — KODA-Específico  
**Pré-requisitos:** Ter completado Nível 1 (Fundamentos), Nível 2 (Padrões Práticos), Nível 3 (Arquitetura Avançada)  
**Status:** 🔴 CRÍTICO — Fundação de todo o Nível 4  
**Data de Criação:** Maio 2026  

---

## 📖 Prólogo: A Manhã em que Fernando Olhou Para o Quadro Branco

Fernando estava parado diante do quadro branco da KODA há 47 minutos.

Eram 07h23 de uma quarta-feira. O café esfriava na mesa. O escritório ainda vazio.

No quadro, quatro versões da arquitetura do KODA estavam desenhadas lado a lado:

```
VERSÃO 1 (Março 2026)          VERSÃO 2 (Abril 2026)
┌──────────┐                   ┌──────────┐
│ WhatsApp │                   │ WhatsApp │
└────┬─────┘                   └────┬─────┘
     │                              │
┌────▼─────┐                   ┌────▼──────────┐
│  KODA    │                   │  KODA Agent   │
│  (único  │                   │  + Generator  │
│  agente) │                   │  + Evaluator  │
└──────────┘                   └───────────────┘

VERSÃO 3 (Maio 2026)           VERSÃO 4 (HOJE — em branco)
┌──────────┐                   ┌──────────────────────┐
│ WhatsApp │                   │                      │
└────┬─────┘                   │    ARQUITETURA       │
     │                         │    COMPLETA DO       │
┌────▼──────────────────┐      │    KODA              │
│ Planner → Generator   │      │                      │
│   ↓         ↓         │      │    (em construção)   │
│ Discovery  Evaluator  │      │                      │
│   ↓         ↓         │      │                      │
│ Order → Fulfillment   │      │                      │
└───────────────────────┘      └──────────────────────┘
```

Fernando apontou para a Versão 4 em branco e disse em voz alta, para ninguém:

> *"O KODA não é mais um agente. É uma operação. E uma operação precisa de arquitetura documentada."*

O que Fernando entendeu naquela manhã mudou tudo.

O KODA começou como um experimento. Um agente único que respondia clientes no WhatsApp. Funcionava para conversas de 5 minutos. Quebrava em conversas de 2 horas.

A Versão 1 resolveu o básico. State persistence para alergias. Token budgeting para conversas longas. Harness patterns para validação. O KODA parou de quebrar.

A Versão 2 adicionou qualidade. Generator/Evaluator para recomendações melhores. Sprint contracts para coordenação entre módulos. Rubrics para avaliar qualidade real. Trace reading para diagnosticar falhas. O KODA ficou confiável.

A Versão 3 transformou o KODA em sistema. Multi-agent com Planner, Discovery, Catalog, Generator, Evaluator, Order, Fulfillment, Recovery. State persistence com SQLite e JSON checkpoints. File-based coordination com locks e status files. Server-side compaction para conversas de 4 horas. Harness evolution para remover components obsoletos. O KODA ficou maduro.

E agora, naquela manhã de maio, Fernando olhava para o quadro em branco da **Versão 4**.

Ele sabia o que precisava estar ali.

Não era um novo padrão. Não era um novo truque de prompting.

Era a **documentação completa da arquitetura**. Cada componente. Cada fluxo de dados. Cada decisão de design. Cada integração. Cada pipeline. Cada trade-off.

Porque uma arquitetura que só existe na cabeça de três engenheiros não é arquitetura — é dívida técnica esperando para explodir.

Este módulo é o quadro branco preenchido.

Você vai ver o que Fernando viu. Vai entender o que cada componente faz. Vai saber como os dados fluem do WhatsApp até o fulfillment. Vai conhecer a integração com a WhatsApp Business API. Vai dominar o pipeline completo: discovery, pedido, fulfillment. Vai entender como os padrões de Nível 1, 2 e 3 se conectam em uma arquitetura real.

E no final, você não vai apenas "conhecer" a arquitetura KODA.

Você vai poder **desenhá-la do zero**.

---

## 🎯 Objetivos Deste Módulo

Ao final deste módulo, você será capaz de:

- ✅ **Desenhar a arquitetura completa do KODA** incluindo todos os componentes, camadas, fluxos de dados e integrações
- ✅ **Explicar o fluxo de dados end-to-end** do WhatsApp Business API até a resposta final ao cliente, passando por todos os agentes internos
- ✅ **Identificar a responsabilidade de cada componente** e como eles se coordenam para executar o pipeline de vendas
- ✅ **Mapear a conexão entre padrões de N1-N3 e a implementação real do KODA**, sabendo onde cada conceito foi aplicado
- ✅ **Compreender a integração com WhatsApp Business API**, incluindo webhooks, templates, media handling e rate limits
- ✅ **Dominar o pipeline de vendas**: discovery → recomendação → carrinho → pedido → pagamento → fulfillment
- ✅ **Avaliar trade-offs arquiteturais** com base em métricas reais de latência, custo e confiabilidade
- ✅ **Propor melhorias arquiteturais** usando os princípios de harness evolution

---

## 🧭 Roadmap Visual do Módulo

```
ENTRADA: Você completou N1, N2 e N3
  │
  ├─ SEÇÃO 1: Visão Geral da Arquitetura (o quadro completo)
  │   └─ Diagrama ASCII da arquitetura
  │   └─ Tabela de componentes e responsabilidades
  │
  ├─ SEÇÃO 2: O Pipeline de Vendas (discovery → pedido → fulfillment)
  │   └─ Cada etapa com agentes, artefatos e verificações
  │
  ├─ SEÇÃO 3: Fluxo de Dados Completo (WhatsApp → Agente → ML → Resposta)
  │   └─ Rastreamento de uma mensagem do início ao fim
  │
  ├─ SEÇÃO 4: Integração WhatsApp Business API
  │   └─ Webhooks, templates, media, rate limits, Cloud API
  │
  ├─ SEÇÃO 5: Estratégias de Coordenação Multi-Agente
  │   └─ Tabela comparativa de estratégias usadas no KODA
  │
  ├─ SEÇÃO 6: Conexão Explícita com Padrões N1-N3
  │   └─ Onde cada conceito de N1-N3 foi aplicado no KODA
  │
  ├─ SEÇÃO 7: Estado Atual do Harness KODA
  │   └─ Componentes ativos, custos, valor, decisões pendentes
  │
  ├─ SEÇÃO 8: Aplicações KODA — Casos Reais
  │   └─ Discovery, Order, Fulfillment em detalhes de produção
  │
  ├─ SEÇÃO 9: O Que Você Aprendeu (Resumo)
  │   └─ Key takeaways e checklist de domínio
  │
  └─ SAÍDA: Você desenha, explica e melhora a arquitetura KODA
```

---

## 🏛️ Seção 1: Visão Geral da Arquitetura KODA

### O Que é o KODA?

KODA é um **agente de vendas conversacional via WhatsApp** especializado em suplementos nutricionais. Ele não é um chatbot estático — é um sistema multi-agente que mantém conversas de 2 a 4 horas, entende restrições alimentares complexas, recomenda produtos personalizados, processa pedidos completos e gerencia fulfillment.

**Características fundamentais:**

| Característica | Descrição |
|---|---|
| **Canal** | WhatsApp Business API (Cloud API) |
| **Duração típica de conversa** | 30 minutos a 4 horas |
| **Agentes internos** | 8 agentes especializados |
| **Modelo primário** | Claude Opus 4.6 (Generator) + Claude Sonnet 4.6 (Evaluator, Planner) |
| **Persistência** | SQLite + JSON checkpoint files |
| **Coordenação** | File-based com locks, status manifests e audit trail |
| **Pipeline de vendas** | Discovery → Recomendação → Carrinho → Pedido → Pagamento → Fulfillment |
| **Métricas atuais** | 98% precisão em recomendações, 99.8% pedidos sem erro, <2% devolução |

### Os 5 Princípios Arquiteturais do KODA

Antes de mergulhar nos componentes, entenda os princípios que guiaram cada decisão:

1. **Separation of Concerns Absoluta**: Nenhum agente faz duas coisas conflitantes. Generator gera. Evaluator avalia. Discovery descobre. Order processa. Cada agente tem uma responsabilidade e apenas uma.

2. **State Over Memory**: O KODA nunca confia na memória do modelo para lembrar informações críticas. Alergias, orçamento, preferências, status de pedido — tudo persiste em arquivos e bancos, não em tokens.

3. **Artifacts Over Promises**: Agentes não se comunicam por "espero que você faça X". Comunicam-se por artefatos (JSON files) que são lidos, validados e auditados.

4. **Fail Fast, Recover Gracefully**: Se algo quebra, o sistema para imediatamente com diagnóstico claro. O Recovery Agent retoma do último checkpoint, não do zero.

5. **Evolve the Harness**: Componentes de harness (guards, validators, compactors) são tratados como código temporário. Quando o modelo melhora, removemos componentes que deixaram de agregar valor.

---

### Diagrama ASCII da Arquitetura Completa do KODA

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                           ARQUITETURA KODA — VISÃO COMPLETA                          │
│                        WhatsApp Sales Agent — Maio 2026                              │
└─────────────────────────────────────────────────────────────────────────────────────┘

                              ┌──────────────────────┐
                              │    CLIENTE FINAL     │
                              │  (WhatsApp Mobile)   │
                              └──────────┬───────────┘
                                         │ mensagem
                                         ▼
┌────────────────────────────────────────────────────────────────────────────────────┐
│                          WHATSAPP BUSINESS API LAYER                                 │
│  ┌─────────────────────┐  ┌──────────────────┐  ┌─────────────────────────────┐    │
│  │ Webhook Receiver    │  │ Message Sender    │  │ Media Handler               │    │
│  │ (POST /webhook)     │  │ (POST /messages)  │  │ (images, PDFs, catalogs)    │    │
│  └─────────┬───────────┘  └──────────────────┘  └─────────────────────────────┘    │
└────────────┼────────────────────────────────────────────────────────────────────────┘
             │ mensagem recebida
             ▼
┌────────────────────────────────────────────────────────────────────────────────────┐
│                          ORCHESTRATION LAYER                                         │
│  ┌──────────────────────────────────────────────────────────────────────────────┐  │
│  │                            ORCHESTRATOR                                       │  │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌──────────────────────┐   │  │
│  │  │ Planner    │  │ Router     │  │ Scheduler  │  │ Recovery Manager     │   │  │
│  │  │ Agent      │  │ (intent    │  │ (agent     │  │ (checkpoint reload,  │   │  │
│  │  │ (divide    │  │  routing)  │  │  ordering) │  │  retry logic)        │   │  │
│  │  │  jornada)  │  │            │  │            │  │                      │   │  │
│  │  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘  └──────────┬───────────┘   │  │
│  └────────┼───────────────┼───────────────┼────────────────────┼───────────────┘  │
└───────────┼───────────────┼───────────────┼────────────────────┼──────────────────┘
            │               │               │                    │
            ▼               ▼               ▼                    ▼
┌────────────────────────────────────────────────────────────────────────────────────┐
│                          AGENT LAYER (agentes especializados)                        │
│                                                                                     │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐                  │
│  │ DISCOVERY AGENT  │  │  CATALOG AGENT   │  │ GENERATOR AGENT  │                  │
│  │ ──────────────── │  │ ──────────────── │  │ ──────────────── │                  │
│  │ Extrai:          │  │ Consulta:        │  │ Cria:            │                  │
│  │ • intenção       │  │ • SKU database   │  │ • recomendações  │                  │
│  │ • restrições     │  │ • inventário     │  │ • respostas      │                  │
│  │ • preferências   │  │ • preços live    │  │ • carrinho       │                  │
│  │ • orçamento      │  │ • promoções      │  │ • explicações    │                  │
│  │                  │  │                  │  │                  │                  │
│  │ Output:          │  │ Output:          │  │ Output:          │                  │
│  │ customer.json    │  │ catalog.json     │  │ draft.json       │                  │
│  └────────┬─────────┘  └────────┬─────────┘  └────────┬─────────┘                  │
│           │                     │                     │                             │
│  ┌────────┴─────────────────────┴─────────────────────┴─────────┐                  │
│  │                     EVALUATOR AGENT                           │                  │
│  │ ──────────────────────────────────────────────────────────── │                  │
│  │ Valida contra rubrics:                                        │                  │
│  │ • produto existe?  • restrições respeitadas?  • preço ok?    │                  │
│  │ • em estoque?  • tom apropriado?  • sem contradições?        │                  │
│  │                                                               │                  │
│  │ Output: evaluation.json (APPROVED ou REJECTED + feedback)     │                  │
│  └──────────────────────────┬───────────────────────────────────┘                  │
│                             │ (se APPROVED)                                         │
│              ┌──────────────┼──────────────┐                                        │
│              ▼              ▼              ▼                                        │
│  ┌──────────────────┐ ┌────────────┐ ┌──────────────────┐                          │
│  │  ORDER AGENT     │ │ PAYMENT    │ │ FULFILLMENT      │                          │
│  │ ──────────────── │ │ AGENT      │ │ AGENT            │                          │
│  │ • monta carrinho │ │ • processa │ │ • reserva estoque │                          │
│  │ • calcula total  │ │ • confirma │ │ • gera tracking   │                          │
│  │ • aplica cupom   │ │ • idempot. │ │ • agenda entrega  │                          │
│  │ • gera pedido    │ │            │ │ • confirma ETA    │                          │
│  │                  │ │            │ │                   │                          │
│  │ Output:          │ │ Output:    │ │ Output:           │                          │
│  │ order.json       │ │ txn.json   │ │ fulfillment.json  │                          │
│  └──────────────────┘ └────────────┘ └──────────────────┘                          │
└────────────────────────────────────────────────────────────────────────────────────┘
             │                     │                     │
             └─────────────────────┼─────────────────────┘
                                   │
                                   ▼
┌────────────────────────────────────────────────────────────────────────────────────┐
│                          PERSISTENCE LAYER                                           │
│                                                                                     │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐    │
│  │ SQLite DB      │  │ JSON State     │  │ Lock Files     │  │ Audit Trail    │    │
│  │ ────────────── │  │ Files          │  │ ────────────── │  │ ────────────── │    │
│  │ • customers    │  │ ────────────── │  │ • order.lock   │  │ • audit.jsonl  │    │
│  │ • products     │  │ • customer.json│  │ • catalog.lock │  │ • todas as     │    │
│  │ • orders       │  │ • order.json   │  │ • fulfillment  │  │   operações    │    │
│  │ • inventory    │  │ • cart.json    │  │   .lock        │  │   registradas  │    │
│  │ • checkpoints  │  │ • state.json   │  │ • retry.lock   │  │ • timestamps   │    │
│  └────────────────┘  └────────────────┘  └────────────────┘  └────────────────┘    │
└────────────────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌────────────────────────────────────────────────────────────────────────────────────┐
│                          INFRASTRUCTURE & EXTERNAL SERVICES                          │
│                                                                                     │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐    │
│  │ Claude API     │  │ WhatsApp       │  │ Inventory       │  │ Payment        │    │
│  │ (Opus + Sonnet)│  │ Cloud API      │  │ System          │  │ Gateway         │    │
│  └────────────────┘  └────────────────┘  └────────────────┘  └────────────────┘    │
└────────────────────────────────────────────────────────────────────────────────────┘
```

---

### Tabela de Componentes e Responsabilidades

| # | Componente | Camada | Responsabilidade Principal | Input | Output | Dependências |
|---|---|---|---|---|---|---|
| 1 | **WhatsApp Webhook Receiver** | WhatsApp API | Recebe mensagens do cliente via webhook, valida assinatura HMAC | POST /webhook com payload JSON | Mensagem validada para Orchestrator | WhatsApp Cloud API |
| 2 | **WhatsApp Message Sender** | WhatsApp API | Envia respostas, templates, mídia para o cliente | Mensagem formatada + phone_number_id | Confirmação de entrega (message_id) | WhatsApp Cloud API |
| 3 | **Media Handler** | WhatsApp API | Processa imagens, PDFs, catálogos enviados ou recebidos | Media ID do WhatsApp | URL de mídia + metadata | WhatsApp Cloud API |
| 4 | **Orchestrator** | Orchestration | Gerencia o ciclo de vida completo de uma conversa, roteia para agentes | Mensagem do cliente + conversation_id | Próximo agente a executar | Planner, Router, Recovery Manager |
| 5 | **Planner Agent** | Orchestration | Divide a jornada do cliente em etapas (sprints) com contratos claros | customer.json + conversation_history | plan.json (etapas, contratos, dependências) | Orchestrator |
| 6 | **Router** | Orchestration | Classifica intenção da mensagem e roteia para agente especializado | Mensagem do cliente + conversation_state | agent_target + intent_classification | Planner |
| 7 | **Recovery Manager** | Orchestration | Detecta falhas, carrega checkpoints, gerencia retry logic | Error signal + conversation_id | Checkpoint reload + retry instruction | SQLite, Lock Files |
| 8 | **Discovery Agent** | Agent | Extrai intenção, restrições, preferências, orçamento do cliente | Mensagens do cliente + histórico | customer.json (perfil completo estruturado) | Claude Opus, SQLite |
| 9 | **Catalog Agent** | Agent | Consulta catálogo de produtos, inventário, preços, promoções | customer.json (restrições, budget) | catalog.json (produtos filtrados) | Inventory System, SQLite |
| 10 | **Generator Agent** | Agent | Gera recomendações, respostas, carrinho, explicações | customer.json + catalog.json + plan.json | draft.json (recomendações + justificativas) | Claude Opus, Catalog Agent |
| 11 | **Evaluator Agent** | Agent | Avalia output do Generator contra rubrics e restrições | draft.json + customer.json + rubrics | evaluation.json (APPROVED/REJECTED + score) | Claude Sonnet, rubrics |
| 12 | **Order Agent** | Agent | Monta carrinho, calcula total, aplica cupons, gera pedido | draft.json (aprovado) + customer.json | order.json (pedido completo) | Payment Agent |
| 13 | **Payment Agent** | Agent | Processa pagamento com idempotência, confirma transação | order.json + payment_method | txn.json (transação confirmada) | Payment Gateway |
| 14 | **Fulfillment Agent** | Agent | Reserva estoque, agenda entrega, gera tracking, confirma ETA | order.json (pago) + inventory | fulfillment.json (tracking + ETA) | Inventory System |
| 15 | **SQLite Database** | Persistence | Armazena customers, products, orders, inventory, checkpoints | SQL queries dos agentes | Dados estruturados persistentes | Nenhuma |
| 16 | **JSON State Files** | Persistence | Estado volátil de conversas: customer context, drafts, orders | Escrita por agentes, leitura por outros agentes | Estado serializado em JSON | File system |
| 17 | **Lock Files** | Persistence | Coordenação de acesso exclusivo a recursos compartilhados | Agent lock request | Lock adquirido ou rejeitado | File system |
| 18 | **Audit Trail** | Persistence | Registro imutável de todas as operações com timestamps | Cada evento do sistema | audit.jsonl (append-only log) | File system |
| 19 | **Claude API** | Infrastructure | Modelos de linguagem: Opus (Generator) + Sonnet (Evaluator/Planner) | Prompts + contexto | Respostas estruturadas (JSON) | Anthropic API |
| 20 | **Inventory System** | Infrastructure | Sistema externo de gestão de estoque e catálogo | SKU queries | Disponibilidade, preço, localização | External API |
| 21 | **Payment Gateway** | Infrastructure | Processador de pagamentos externo | Payment request | Transaction ID, status | External API |

---

## 🔄 Seção 2: O Pipeline de Vendas Completo

O KODA executa um pipeline de vendas de 6 etapas. Cada etapa é um sprint com contrato definido, artefatos de entrada e saída, e verificação pelo Evaluator.

### Visão Macro do Pipeline

```
ETAPA 1          ETAPA 2          ETAPA 3          ETAPA 4          ETAPA 5          ETAPA 6
DISCOVERY   →    CATALOG     →    RECOMMEND    →    ORDER       →    PAYMENT     →    FULFILLMENT
───────────────────────────────────────────────────────────────────────────────────────────────
"Quem é       "O que temos   "O que eu       "Monte o        "Cobre o        "Entregue o
o cliente?"   pra ele?"      recomendo?"     pedido"         cliente"        produto"

Output:       Output:        Output:         Output:         Output:         Output:
customer.json catalog.json   draft.json      order.json      txn.json        fulfillment.json
                +
               evaluation.json
```

### Etapa 1: Discovery — "Quem é o cliente?"

**Objetivo:** Extrair e estruturar todas as informações relevantes do cliente.

**Agente:** Discovery Agent

**O que acontece:**

1. O Discovery Agent recebe as mensagens iniciais do cliente
2. Analisa a conversa para extrair:
   - **Intenção primária:** O que o cliente quer? (comprar, pesquisar, reclamar, tirar dúvida)
   - **Objetivo de consumo:** Para que serve? (ganho muscular, emagrecimento, energia, saúde geral)
   - **Restrições alimentares:** Alergias, intolerâncias, restrições religiosas ou éticas
   - **Preferências:** Sabor, textura, marca, tipo de produto
   - **Orçamento:** Faixa de preço, sensibilidade a preço
   - **Nível de conhecimento:** Iniciante, intermediário, avançado
   - **Histórico:** Compras anteriores, produtos que não gostou
   - **Urgência:** Precisa para quando? Entrega rápida?
3. Estrutura tudo em `customer.json`
4. Se faltar informação crítica (ex: restrições alimentares), o Discovery Agent pergunta antes de avançar

**Artefato: customer.json**

```json
{
  "customer_id": "wa_5511987654321",
  "session_id": "sess_20260527_001",
  "discovered_at": "2026-05-27T14:32:00Z",
  "intent": {
    "primary": "purchase",
    "goal": "ganho_muscular",
    "confidence": 0.95
  },
  "profile": {
    "name": "João Silva",
    "level": "intermediario",
    "training_frequency": "5x_semana",
    "training_type": "musculacao"
  },
  "restrictions": {
    "allergies": ["amendoim"],
    "intolerances": ["lactose"],
    "dietary": [],
    "religious": [],
    "medical": []
  },
  "preferences": {
    "flavors": ["chocolate", "morango"],
    "brands": [],
    "format": "po",
    "avoid": ["sabor artificial muito forte"]
  },
  "budget": {
    "max_per_product": 200,
    "max_total": 350,
    "sensitive_to_price": false
  },
  "history": {
    "previous_purchases": [
      {"sku": "WHEY-001", "name": "Whey Concentrado", "liked": true},
      {"sku": "CREATINA-002", "name": "Creatina Mono", "liked": true}
    ],
    "previous_returns": [],
    "previous_complaints": ["WHEY-VEGAN-003 gosto muito ruim"]
  },
  "urgency": {
    "needs_by": "2026-05-29",
    "delivery_preference": "fastest",
    "same_day_eligible": true
  }
}
```

**Verificação do Evaluator nesta etapa:**

| Critério | Peso | O que verifica |
|---|---|---|
| Intenção clara | 30% | O objetivo primário está bem definido? |
| Restrições completas | 40% | Todas as restrições foram extraídas? Se há dúvida, Discovery perguntou? |
| Orçamento realista | 15% | O budget está dentro de faixas razoáveis? |
| Histórico contextualizado | 15% | Compras anteriores e preferências estão capturadas? |

**Conexão com Níveis Anteriores:**

- **N1 — State Persistence:** `customer.json` é a implementação direta do princípio "não confie na memória do agente". Este arquivo será lido por todos os agentes subsequentes.
- **N2 — Sprint Contracts:** Discovery tem contrato explícito: recebe mensagens brutas, entrega `customer.json` com todos os campos obrigatórios preenchidos.
- **N3 — Multi-Agent:** Discovery é um agente especializado, não o KODA inteiro tentando fazer tudo.

---

### Etapa 2: Catalog — "O que temos para ele?"

**Objetivo:** Consultar o catálogo de produtos filtrando pelas restrições e preferências do cliente.

**Agente:** Catalog Agent

**O que acontece:**

1. Catalog Agent lê `customer.json`
2. Consulta o Inventory System com filtros:
   - Categoria de produto alinhada ao objetivo (ex: whey protein, creatina, BCAA)
   - Sem alérgenos das restrições (ex: sem lactose, sem amendoim)
   - Dentro do orçamento máximo
   - Em estoque na região do cliente
   - Preferências de sabor e formato
3. Enriquece com dados live: preço atual, estoque real, promoções ativas
4. Retorna `catalog.json` com produtos candidatos (5-15 opções)

**Artefato: catalog.json**

```json
{
  "catalog_id": "cat_20260527_001",
  "queried_at": "2026-05-27T14:32:15Z",
  "filters_applied": {
    "category": ["whey_protein", "creatine"],
    "exclude_allergens": ["lactose", "amendoim"],
    "max_price": 200,
    "in_stock_region": "SP",
    "flavors": ["chocolate", "morango"]
  },
  "products": [
    {
      "sku": "WHEY-VEGAN-005",
      "name": "Whey Vegano 100% Premium",
      "category": "whey_protein",
      "price_base": 149.90,
      "price_promo": 129.90,
      "stock_sp": 47,
      "rating": 4.8,
      "lactose_free": true,
      "vegan": true,
      "flavors_available": ["chocolate", "morango", "baunilha"],
      "protein_per_serving_g": 28,
      "servings": 30,
      "delivery_days_sp": 1
    }
  ],
  "total_candidates": 8,
  "promotions_active": ["VERAO20", "CLUBE15"]
}
```

**Verificação do Evaluator nesta etapa:**

| Critério | Peso | O que verifica |
|---|---|---|
| Filtros aplicados corretamente | 35% | Nenhum produto com alérgeno passou? Budget respeitado? |
| Dados live válidos | 30% | Preço e estoque são do momento da consulta? |
| Cobertura suficiente | 20% | Pelo menos 3 produtos candidatos? |
| Promoções consideradas | 15% | Cupons e descontos de clube foram incluídos? |

**Conexão com Níveis Anteriores:**

- **N1 — Token Budgeting:** Catalog Agent retorna apenas produtos relevantes, evitando carregar catálogo inteiro no contexto.
- **N2 — Sprint Contracts:** Catalog tem contrato: recebe `customer.json`, entrega `catalog.json` com produtos filtrados e validados.
- **N3 — State Persistence:** Consulta SQLite para cache de catálogo, reduzindo chamadas ao Inventory System externo.

---

### Etapa 3: Recommend — "O que eu recomendo?"

**Objetivo:** Gerar recomendações personalizadas e avaliá-las antes de mostrar ao cliente.

**Agentes:** Generator Agent → Evaluator Agent (ciclo Generator/Evaluator)

**O que acontece:**

1. **Generator lê** `customer.json` + `catalog.json` + `plan.json`
2. **Generator gera** 3-5 recomendações, cada uma com:
   - Produto principal + rationale
   - Preço final (com descontos aplicados)
   - Comparação com alternativas
   - Explicação amigável para o cliente
3. **Generator escreve** `draft.json`
4. **Evaluator lê** `draft.json` + `customer.json` (para verificar restrições)
5. **Evaluator avalia** cada recomendação contra rubrics:
   - Restrições respeitadas?
   - Preço dentro do orçamento?
   - Produto em estoque?
   - Explicação clara e útil?
   - Tom de voz apropriado?
6. **Se aprovado:** Recomendação segue para o cliente
7. **Se rejeitado:** Evaluator escreve `feedback.json` e Generator tenta novamente (máx 3 iterações)

**Artefato: draft.json (Generator output)**

```json
{
  "generation_id": "gen_20260527_001",
  "iteration": 1,
  "generated_at": "2026-05-27T14:32:45Z",
  "recommendations": [
    {
      "rank": 1,
      "sku": "WHEY-VEGAN-005",
      "name": "Whey Vegano 100% Premium",
      "price_base": 149.90,
      "price_final": 110.43,
      "discounts_applied": ["CLUBE15", "VERAO20"],
      "rationale": "Melhor opção para o João: vegano (sem lactose garantido), sem amendoim, sabor chocolate (preferência), 28g proteína/dose, estoque em SP com entrega amanhã. Preço final com descontos: R$ 110,43 — dentro do orçamento.",
      "comparative": "Comparado ao Whey Concentrado (que João comprou antes): 100% livre de lactose, maior pureza proteica, melhor digestão. Supera a experiência anterior com Whey Vegano (gosto ruim) porque este tem rating 4.8 em sabor."
    }
  ],
  "generator_confidence": 0.85,
  "notes": "Cliente tem histórico de rejeitar sabor artificial. Esta recomendação prioriza sabor natural."
}
```

**Artefato: evaluation.json (Evaluator output)**

```json
{
  "evaluation_id": "eval_20260527_001",
  "generation_id": "gen_20260527_001",
  "evaluated_at": "2026-05-27T14:33:00Z",
  "verdict": "APPROVED",
  "rubric_scores": {
    "restrictions_respected": {
      "score": 10,
      "max": 10,
      "detail": "Sem lactose (vegano). Sem amendoim. Todas as restrições verificadas contra ficha técnica do produto."
    },
    "budget_within_range": {
      "score": 10,
      "max": 10,
      "detail": "R$ 110,43 final, dentro do orçamento de R$ 200."
    },
    "in_stock_verified": {
      "score": 10,
      "max": 10,
      "detail": "47 unidades em SP. Confirmação live do inventory system."
    },
    "explanation_clarity": {
      "score": 9,
      "max": 10,
      "detail": "Explicação clara, aborda histórico do cliente, compara com compras anteriores. Poderia mencionar dosagem recomendada."
    },
    "tone_appropriateness": {
      "score": 10,
      "max": 10,
      "detail": "Tom amigável, consultivo, sem ser insistente."
    },
    "no_contradictions": {
      "score": 10,
      "max": 10,
      "detail": "Nenhuma contradição com informações anteriores do cliente."
    }
  },
  "overall_score": 9.8,
  "approval_threshold": 7.0,
  "status": "APPROVED"
}
```

**Verificação do Evaluator nesta etapa:**

| Critério | Peso | O que verifica |
|---|---|---|
| Restrições respeitadas | 30% | Cada restrição do cliente foi checada contra cada produto? |
| Orçamento | 20% | Preço final (com descontos) ≤ budget_max? |
| Estoque | 15% | Estoque confirmado live, não cache antigo? |
| Clareza | 15% | Cliente vai entender a recomendação? |
| Tom | 10% | Tom consultivo, não insistente ou robótico? |
| Consistência | 10% | Não contradiz informações anteriores? |

**Conexão com Níveis Anteriores:**

- **N1 — Generator/Evaluator (preview):** Primeira menção do padrão no N1, implementado completamente aqui.
- **N2 — Generator/Evaluator Pattern:** Implementação completa com iterações, feedback loop, e rubrics.
- **N2 — Rubric Design:** Rubrics com 6 dimensões, pesos e thresholds.
- **N3 — Multi-Agent:** Generator e Evaluator como agentes separados, com artefatos como canal de comunicação.

---

### Etapa 4: Order — "Monte o pedido"

**Objetivo:** Transformar a recomendação aprovada em um pedido formal.

**Agente:** Order Agent

**O que acontece:**

1. Order Agent lê `draft.json` (aprovado) + `customer.json`
2. Monta o carrinho:
   - Produto(s) selecionado(s) com quantidade
   - Aplica descontos e cupons
   - Calcula frete baseado no CEP e modalidade
   - Gera subtotal, descontos, total final
3. Valida regras de negócio:
   - Cupom ainda é válido?
   - Desconto de clube aplicado?
   - Sem double-discount?
   - Quantidade máxima por cliente?
4. Gera `order.json`

**Artefato: order.json**

```json
{
  "order_id": "ORD-20260527-0042",
  "customer_id": "wa_5511987654321",
  "created_at": "2026-05-27T14:33:30Z",
  "status": "pending_payment",
  "items": [
    {
      "sku": "WHEY-VEGAN-005",
      "name": "Whey Vegano 100% Premium",
      "quantity": 2,
      "unit_price": 149.90,
      "total_price": 299.80
    }
  ],
  "subtotal": 299.80,
  "discounts": [
    {"code": "CLUBE15", "type": "club_member", "amount": 44.97},
    {"code": "VERAO20", "type": "promotional", "amount": 50.97}
  ],
  "shipping": {
    "cep": "01310-100",
    "method": "same_day",
    "cost": 14.90
  },
  "total": 218.76,
  "applied_coupons": ["CLUBE15", "VERAO20"],
  "double_discount_check": "passed"
}
```

**Conexão com Níveis Anteriores:**

- **N2 — Sprint Contracts:** Order Agent tem contrato rígido de entrada e saída. Se dados de entrada não correspondem ao schema esperado, falha imediatamente.
- **N3 — File-Based Coordination:** Antes de criar o pedido, Order Agent adquire `order.lock.json` para evitar pedidos duplicados (problema da Marina no N3).
- **N3 — State Persistence:** `order.json` é salvo em SQLite com checkpoint. Se o servidor reiniciar, o pedido não é perdido (problema do Pedro no N3).

---

### Etapa 5: Payment — "Cobre o cliente"

**Objetivo:** Processar o pagamento com garantia de idempotência.

**Agente:** Payment Agent

**O que acontece:**

1. Payment Agent lê `order.json`
2. Verifica idempotência: este pedido já foi cobrado?
3. Se não: envia requisição ao Payment Gateway
4. Aguarda confirmação
5. Registra transação em `txn.json`
6. Atualiza status do pedido para `paid`

**Regra de ouro do Payment Agent:**

> *"Nunca cobre duas vezes. Se a primeira tentativa teve timeout, NÃO tente de novo sem verificar idempotency key."*

**Artefato: txn.json**

```json
{
  "transaction_id": "txn_abc123def456",
  "order_id": "ORD-20260527-0042",
  "idempotency_key": "idem_ORD-20260527-0042_v1",
  "amount": 218.76,
  "currency": "BRL",
  "method": "credit_card",
  "status": "confirmed",
  "gateway_response": "approved",
  "processed_at": "2026-05-27T14:33:45Z"
}
```

**Conexão com Níveis Anteriores:**

- **N2 — Generator/Evaluator:** Payment Agent é verificado pelo Evaluator ANTES de cobrar: o valor está correto? Descontos aplicados? Sem double-charge?
- **N3 — File-Based Coordination:** Payment Agent adquire `payment.lock.json` antes de processar. Se timeout, verifica idempotency key antes de retentar.
- **N3 — State Persistence:** `txn.json` é o registro canônico da transação. Se tudo mais falhar, este arquivo é a verdade.

---

### Etapa 6: Fulfillment — "Entregue o produto"

**Objetivo:** Reservar estoque, gerar tracking e confirmar entrega.

**Agente:** Fulfillment Agent

**O que acontece:**

1. Fulfillment Agent lê `order.json` (status = paid) + `customer.json` (endereço, urgência)
2. Consulta Inventory System: confirma estoque (pode ter mudado desde a recomendação)
3. Reserva unidades (diminui estoque disponível)
4. Seleciona armazém mais próximo do cliente
5. Gera tracking number
6. Calcula ETA realista (com buffer de 30min para same-day)
7. Agenda coleta/entrega
8. Gera `fulfillment.json`

**Artefato: fulfillment.json**

```json
{
  "fulfillment_id": "ful_20260527_001",
  "order_id": "ORD-20260527-0042",
  "status": "reserved",
  "items_reserved": [
    {"sku": "WHEY-VEGAN-005", "quantity": 2, "warehouse": "SP-01"}
  ],
  "delivery": {
    "method": "same_day",
    "tracking_number": "TRK-789456123",
    "carrier": "Loggi",
    "eta": "2026-05-27T18:30:00-03:00",
    "buffer_minutes": 30,
    "address_confirmed": true
  },
  "created_at": "2026-05-27T14:34:00Z"
}
```

**Verificação do Evaluator (Fulfillment):**

| Critério | O que verifica |
|---|---|
| Estoque confirmado | Unidades reservadas correspondem ao pedido? |
| ETA realista | Tempo de entrega + buffer ≤ promessa ao cliente? |
| Endereço válido | CEP existe? Região atendida? |
| Tracking gerado | Número de rastreio é válido? |

**Conexão com Níveis Anteriores:**

- **N3 — Multi-Agent:** Na versão completa, Fulfillment pode usar 3 sub-agentes paralelos (Armazém, Rota, Entregador) coordenados por um Evaluator.
- **N3 — Server-Side Compaction:** Se a conversa durou 4h, o contexto para o Fulfillment Agent é compactado para apenas: restrições + endereço + pedido confirmado.
- **N3 — Harness Evolution:** Se o modelo consegue gerar tracking e ETA sem o Fulfillment Agent separado, este agente pode ser absorvido pelo Order Agent.

---

## 📡 Seção 3: Fluxo de Dados Completo — WhatsApp → Agente → ML → Resposta

### Rastreando uma Mensagem do Início ao Fim

Vamos rastrear exatamente o que acontece quando um cliente envia uma mensagem no WhatsApp. Esta é a jornada completa de uma única mensagem através de todas as camadas da arquitetura KODA.

```
TEMPO (ms)   ETAPA                              COMPONENTE
───────────────────────────────────────────────────────────────────────────
0            Cliente digita e envia mensagem     WhatsApp Client
             "Quero um whey sem lactose"
             
50-100       WhatsApp entrega webhook            WhatsApp Cloud API
             POST /webhook → KODA server
             
100-150      Validação HMAC + parse              Webhook Receiver
             Verifica assinatura, extrai:
             - from (phone_number_id)
             - text (mensagem)
             - timestamp
             
150-200      Load conversation state             Recovery Manager
             Busca conversation_id pelo phone
             Se nova: cria customer.json vazio
             Se existente: carrega estado do SQLite
             
200-250      Classifica intenção                 Router
             "Quero um whey sem lactose" →
             intent: purchase_request
             target_agent: Discovery
             
250-300      Planner decide próximos passos      Planner Agent
             Se cliente novo: Sprint 1 = Discovery
             Se já conhecido: Sprint N = Catalog
             
300-350      Discovery extrai perfil              Discovery Agent
             Processa mensagem + histórico
             Atualiza customer.json:
             - goal: comprar_whey
             - restrictions: [lactose]
             
350-500      Evaluator verifica Discovery         Evaluator Agent
             customer.json completo?
             Restrições capturadas?
             → APPROVED
             
500-600      Catalog busca produtos               Catalog Agent
             Query: whey protein, sem lactose,
             em estoque SP, até R$ 200
             → 8 produtos candidatos
             
600-700      Generator cria recomendações         Generator Agent
             Prompt: customer.json + catalog.json
             → 3 recomendações com rationale
             
700-850      Evaluator avalia recomendações       Evaluator Agent
             Verifica cada produto contra rubrics:
             lactose_free? budget? stock? tone?
             → APPROVED (score 9.2)
             
850-900      Formata resposta para WhatsApp       Message Sender
             Template: mensagem amigável +
             produtos formatados + emojis
             
900-1000     Envia via WhatsApp Cloud API         Message Sender
             POST /messages → WhatsApp
             
1000-1200    Cliente recebe mensagem              WhatsApp Client
             "Encontrei 3 wheys sem lactose! 🥇..."
             
TOTAL: ~1.2 segundos para primeira resposta
```

### O Papel do ML (Claude API) no Fluxo

O "ML" no fluxo KODA não é um componente monolítico — são **múltiplas chamadas estratégicas** ao Claude API, cada uma com configuração específica:

| Chamada | Modelo | Temperatura | Max Tokens | Propósito |
|---|---|---|---|---|
| Discovery | Claude Opus 4.6 | 0.3 | 1500 | Extração precisa de perfil (baixa temp = consistente) |
| Generator | Claude Opus 4.6 | 0.8 | 2000 | Criatividade para gerar múltiplas recomendações |
| Evaluator | Claude Sonnet 4.6 | 0.2 | 1000 | Rigor na avaliação (baixa temp = sem variação) |
| Planner | Claude Sonnet 4.6 | 0.3 | 800 | Decisões de roteamento consistentes |
| Order | Claude Sonnet 4.6 | 0.1 | 1200 | Cálculos precisos, zero tolerância a erro |
| Recovery | Claude Sonnet 4.6 | 0.3 | 600 | Diagnóstico de falha e decisão de retry |

**Por que modelos diferentes?**

- **Opus** para Generator: precisa de criatividade para explorar opções diferentes, considerar trade-offs, gerar explicações naturais
- **Sonnet** para Evaluator: precisa de velocidade e consistência, não criatividade. Avaliar contra rubrics é tarefa estruturada
- **Sonnet** para todo o resto: custo 3-5x menor que Opus, latência 2x menor, qualidade suficiente para tarefas estruturadas

**Custo por conversa típica (2 horas, ~15 interações):**

```
Discovery:     3 chamadas  × ~1500 tokens =  4.500 tokens
Generator:     5 chamadas  × ~2000 tokens = 10.000 tokens
Evaluator:     5 chamadas  × ~1000 tokens =  5.000 tokens
Planner:       2 chamadas  ×  ~800 tokens =  1.600 tokens
Order:         1 chamada   × ~1200 tokens =  1.200 tokens
Recovery:      0-2 chamadas (só em falha) =    800 tokens
                                           ─────────
TOTAL:                                      ~23.100 tokens
Custo estimado (Opus + Sonnet mix):         ~$0.15-0.25 USD
```

---

## 📱 Seção 4: Integração WhatsApp Business API

### Arquitetura da Integração

O KODA se comunica com o WhatsApp exclusivamente através da **WhatsApp Business Cloud API** (não a On-Premises API). Toda a comunicação é via HTTPS REST.

```
┌──────────────────────────────────────────────────────────────┐
│                  WHATSAPP BUSINESS API INTEGRATION            │
│                                                               │
│  ┌─────────────────────┐         ┌─────────────────────────┐ │
│  │   KODA Server       │         │  WhatsApp Cloud API     │ │
│  │                     │         │                         │ │
│  │  Webhook Receiver   │◄────────┤  POST /webhook          │ │
│  │  (valida HMAC)      │         │  (envia mensagens)      │ │
│  │                     │         │                         │ │
│  │  Message Sender     │────────►│  POST /{version}/       │ │
│  │  (envia respostas)  │         │  {phone_number_id}/     │ │
│  │                     │         │  messages               │ │
│  │                     │         │                         │ │
│  │  Media Handler      │◄───────►│  GET/POST /{version}/   │ │
│  │  (upload/download)  │         │  {media_id}             │ │
│  └─────────────────────┘         └─────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```

### Componentes de Integração

#### 1. Webhook Receiver

**Responsabilidade:** Receber e validar mensagens enviadas pelos clientes.

**Fluxo:**
1. WhatsApp envia POST para `https://koda.api.com/webhook`
2. KODA verifica assinatura HMAC-SHA256 no header `x-hub-signature-256`
3. Se válido: extrai mensagem do payload JSON
4. Se inválido: retorna 403 (mensagem descartada — pode ser ataque)

**Estrutura do payload recebido:**

```json
{
  "object": "whatsapp_business_account",
  "entry": [{
    "id": "WHATSAPP_BUSINESS_ACCOUNT_ID",
    "changes": [{
      "value": {
        "messaging_product": "whatsapp",
        "metadata": {
          "display_phone_number": "5511999999999",
          "phone_number_id": "123456789"
        },
        "contacts": [{
          "profile": {"name": "João Silva"},
          "wa_id": "5511987654321"
        }],
        "messages": [{
          "from": "5511987654321",
          "id": "wamid.abc123",
          "timestamp": "1716811200",
          "type": "text",
          "text": {"body": "Quero um whey sem lactose"}
        }]
      }
    }]
  }]
}
```

#### 2. Message Sender

**Responsabilidade:** Enviar respostas para o cliente via WhatsApp Cloud API.

**Tipos de mensagem suportados pelo KODA:**

| Tipo | Uso no KODA | Exemplo |
|---|---|---|
| **text** | Respostas conversacionais, recomendações | "Encontrei 3 wheys sem lactose!" |
| **interactive** | Botões de ação rápida, listas de produtos | "Escolha uma opção:" [Comprar] [Ver detalhes] [Falar com humano] |
| **image** | Fotos de produtos, tabela nutricional | Imagem do produto com link de compra |
| **document** | Catálogo em PDF, invoice | PDF com detalhes do pedido |
| **template** | Notificações: confirmação de pedido, tracking | "Seu pedido #0042 foi enviado! Tracking: TRK-789" |

**Exemplo de envio de mensagem interativa (recomendação):**

```json
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "5511987654321",
  "type": "interactive",
  "interactive": {
    "type": "list",
    "header": {
      "type": "text",
      "text": "🥇 Recomendações para você, João!"
    },
    "body": {
      "text": "Encontrei 3 wheys 100% sem lactose com ótimo custo-benefício:"
    },
    "footer": {
      "text": "Toque em uma opção para ver detalhes"
    },
    "action": {
      "button": "Ver opções",
      "sections": [{
        "title": "Top 3 Recomendações",
        "rows": [
          {
            "id": "WHEY-VEGAN-005",
            "title": "Whey Vegano Premium",
            "description": "R$ 110,43 — Melhor custo-benefício ⭐4.8"
          },
          {
            "id": "WHEY-ISOLADO-008",
            "title": "Whey Isolado Zero Lactose",
            "description": "R$ 135,00 — Máxima pureza ⭐4.7"
          },
          {
            "id": "PROTEINA-VEGAN-003",
            "title": "Proteína Vegetal Mix",
            "description": "R$ 89,90 — Mais econômico ⭐4.5"
          }
        ]
      }]
    }
  }
}
```

#### 3. Media Handler

**Responsabilidade:** Gerenciar upload e download de mídia (imagens, documentos).

**Fluxo de upload (ex: enviar foto de produto):**
1. KODA faz POST para `/{version}/{phone_number_id}/media` com o binário da imagem
2. WhatsApp retorna `media_id`
3. KODA envia mensagem tipo `image` referenciando o `media_id`

**Fluxo de download (ex: cliente envia foto):**
1. Webhook recebe mensagem tipo `image` com `media_id`
2. KODA faz GET para `/{version}/{media_id}` para obter URL de download
3. KODA faz download da imagem e processa (se necessário)

#### 4. Rate Limits e Resiliência

A WhatsApp Cloud API impõe limites que o KODA precisa respeitar:

| Limite | Valor | Estratégia KODA |
|---|---|---|
| **Messages per second** | 250/s (varia por qualidade do número) | Fila interna com throttling, nunca excede 80% do limite |
| **Concurrent connections** | 100 | Connection pool gerenciado |
| **Media upload size** | 64MB (images), 100MB (documents) | Compressão de imagens antes do upload |
| **Template messages** | Limitado por quality rating | Templates só para notificações transacionais |
| **Webhook timeout** | 20s para responder | KODA responde 200 OK imediatamente, processa async |

**Estratégia de retry do KODA para falhas de envio:**

```
Tentativa 1: Imediata
  ↓ (se erro 429 — rate limit)
Tentativa 2: +2s (exponential backoff)
  ↓ (se erro 5xx — server error)
Tentativa 3: +4s
  ↓ (se erro 4xx — client error: NÃO retenta, loga e escala)
Máximo: 3 tentativas para rate limit/server error
```

---

## 🔗 Seção 5: Estratégias de Coordenação Multi-Agente

O KODA usa um ecossistema de 8 agentes que precisam coordenar trabalho sem conflitos. Esta seção analisa as estratégias de coordenação usadas e compara com alternativas.

### Tabela Comparativa de Estratégias de Coordenação

| Estratégia | Como Funciona | Usada no KODA? | Vantagens | Desvantagens | Exemplo no KODA |
|---|---|---|---|---|---|
| **File-Based Coordination** | Agentes escrevem e leem arquivos JSON como canal de comunicação. Locks previnem conflitos. | ✅ Primária | - Auditável (todo estado é arquivo)<br>- Recuperável (checkpoints)<br>- Debuggable (ler arquivos)<br>- Sem dependência de infra | - Latência de I/O<br>- Consistência eventual<br>- Gerenciamento de locks | Generator → draft.json → Evaluator → evaluation.json |
| **Message-Passing (Queue)** | Agentes enviam mensagens para fila (RabbitMQ, SQS). Consumidores processam. | ❌ Não usada | - Baixa latência<br>- Escalável<br>- Desacoplamento forte | - Infra adicional<br>- Perda de mensagens<br>- Difícil debugar | Não usado; KODA prefere simplicidade de arquivos |
| **Shared Database** | Agentes leem/escrevem no mesmo banco. Coordenação por transações. | ✅ Secundária | - Consistência forte<br>- ACID<br>- Queryable | - Acoplamento no schema<br>- Contenção de lock<br>- Migrations dolorosas | SQLite para customers, orders, inventory |
| **Orchestrator Pattern** | Um agente central (Orchestrator) coordena todos os outros. | ✅ Primária | - Controle centralizado<br>- Ordem garantida<br>- Fácil de entender | - Single point of failure<br>- Gargalo<br>- Orchestrator precisa ser resiliente | Planner + Router decidem quem executa e em qual ordem |
| **Choreography (Event-Driven)** | Agentes reagem a eventos. Cada um sabe o que fazer quando X acontece. | ⚠️ Parcial | - Desacoplado<br>- Escalável<br>- Flexível | - Difícil rastrear fluxo<br>- Loops infinitos possíveis<br>- Debugging complexo | Recovery Agent reage a eventos de erro |
| **Blackboard Pattern** | Agentes leem/escrevem em um "quadro negro" compartilhado. | ✅ Sim (via JSON files) | - Flexível<br>- Incremental<br>- Múltiplos contribuidores | - Inconsistência possível<br>- Difícil saber quando "terminou" | JSON state files são o blackboard do KODA |
| **Pipeline (Chain)** | Agentes executam em sequência fixa. Output de A → Input de B. | ✅ Sim | - Simples<br>- Previsível<br>- Fácil validar | - Rígido<br>- Bloqueante<br>- Slowdown em cascata | Pipeline de vendas: Discovery → Catalog → Recommend → Order → Payment → Fulfillment |
| **Parallel with Aggregator** | Múltiplos agentes executam em paralelo. Aggregator consolida resultados. | ✅ Sim (N3+) | - Rápido<br>- Redundância<br>- Múltiplas perspectivas | - Complexo agregar<br>- Conflitos<br>- Custo maior | Fulfillment: 3 sub-agentes paralelos (Armazém, Rota, Entregador) → Evaluator agrega |
| **Retry with Exponential Backoff** | Em falha, agente retenta com intervalo crescente. | ✅ Sim | - Recuperação automática<br>- Lida com falhas transitórias | - Latência extra<br>- Pode mascarar problemas | Recovery Agent com retry logic configurável |
| **Circuit Breaker** | Após N falhas consecutivas, para de chamar serviço por T segundos. | ✅ Sim | - Protege sistema<br>- Evita cascata | - Falso positivo possível<br>- Degradação controlada | Payment Agent: 3 falhas seguidas → circuit open por 60s |

### Por que File-Based Coordination é a Estratégia Primária do KODA?

A decisão de usar arquivos JSON como mecanismo primário de coordenação não foi acidental. Foi uma escolha deliberada baseada em 4 princípios:

**1. Auditabilidade Total**

Quando algo falha, você quer saber EXATAMENTE o que cada agente viu e produziu. Com message-passing, as mensagens desaparecem após consumo. Com file-based, você lê `draft.json`, `evaluation.json`, `feedback.json` e vê o histórico completo.

Exemplo real: um cliente reclamou que o KODA recomendou um produto com lactose. A equipe abriu `evaluation.json` e viu que o Evaluator havia APROVADO incorretamente. O bug estava no Evaluator, não no Generator. Sem arquivos, teriam passado horas tentando adivinhar.

**2. Recuperabilidade**

Se o servidor reiniciar no meio de uma conversa (problema do Pedro no N3), o Recovery Agent recarrega o estado dos arquivos JSON e SQLite. Com message-passing, as mensagens em trânsito seriam perdidas. Com shared database, o estado estaria lá, mas a conexão teria caído.

**3. Debuggability**

Em desenvolvimento, você pode inspecionar arquivos JSON com qualquer editor de texto. Em produção, pode fazer `cat state/wa_5511987654321/draft.json` e ver exatamente o que o Generator produziu. Compare com message-passing: precisa de ferramentas especializadas para inspecionar filas.

**4. Simplicidade Operacional**

File-based coordination não requer infraestrutura adicional. Não precisa de RabbitMQ, Redis Streams, Kafka. O filesystem já está lá. Para uma operação do porte do KODA (centenas de conversas simultâneas, não milhões), essa simplicidade supera a performance teórica de message queues.

**Quando o KODA vai precisar de algo mais sofisticado?**

Se o KODA escalar para dezenas de milhares de conversas simultâneas, file-based coordination vai encontrar limites de I/O e contenção de locks. Nesse ponto, a migração seria:
- JSON files → PostgreSQL com row-level locking (para estado)
- File locks → Redis distributed locks (para coordenação)
- Audit trail → Kafka (para eventos)

Mas em maio de 2026, com centenas de conversas simultâneas, file-based é a escolha certa.

---

## 🧬 Seção 6: Conexão Explícita com Padrões N1-N3

O KODA não foi construído do zero com todos esses padrões. Ele evoluiu através dos 3 níveis do currículo. Esta seção mapeia explicitamente cada conceito de N1, N2 e N3 para sua implementação real no KODA.

### Mapeamento Nível 1 → KODA

| Conceito N1 | Onde está no KODA | Como funciona |
|---|---|---|
| **Context Amnesia** | `customer.json` (state persistence) | Informações críticas (alergias, orçamento) NUNCA dependem da memória do modelo. São persistidas em JSON e SQLite. Todo agente lê `customer.json` antes de agir. |
| **Token Budgeting** | Estratégia de compactação | Conversas longas são sumarizadas preservando fatos críticos. Catalog Agent retorna apenas produtos relevantes. Planner divide jornada em sprints pequenos. |
| **Basic Harness Patterns** | Guardrails de validação | Antes de recomendar: verificar alergias. Antes de cobrar: verificar idempotência. Antes de enviar: verificar tom de voz. |
| **Por que agentes perdem o foco** | Diagnóstico de incidentes | Todo incidente é classificado nos 3 problemas de N1. Ex: "cliente recebeu produto errado" → Problema 3 (Self-Evaluation Collapse). |
| **History Compression** | Server-side compaction (N3) | Compactação classifica fatos por criticidade: [CRITICAL: alergia], [HIGH: orçamento], [MEDIUM: preferência], [LOW: small talk]. |

### Mapeamento Nível 2 → KODA

| Conceito N2 | Onde está no KODA | Como funciona |
|---|---|---|
| **Generator/Evaluator Pattern** | Recommend Stage (Etapa 3) | Generator (Opus, temp 0.8) cria recomendações. Evaluator (Sonnet, temp 0.2) avalia contra rubrics. Ciclo de até 3 iterações com `feedback.json`. |
| **Sprint Contracts** | Todo o pipeline de vendas | Cada etapa tem input contract e output contract. Discovery: `messages → customer.json`. Catalog: `customer.json → catalog.json`. Order: `draft.json → order.json`. |
| **Rubric Design** | Rubrics de avaliação | 6 dimensões com pesos: Restrições (30%), Orçamento (20%), Estoque (15%), Clareza (15%), Tom (10%), Consistência (10%). Threshold: 7.0/10. |
| **Trace Reading** | `audit.jsonl` + debug scripts | Cada evento do sistema é registrado em audit trail. Scripts de debug leem arquivos JSON sequencialmente para reconstruir fluxos. |
| **4 Padrões Integrados** | Nível 2 KODA completo | Generator/Evaluator → Sprint Contracts → Rubric Design → Trace Reading, todos operando em cada conversa. |

### Mapeamento Nível 3 → KODA

| Conceito N3 | Onde está no KODA | Como funciona |
|---|---|---|
| **Multi-Agent Systems** | 8 agentes especializados | Planner, Discovery, Catalog, Generator, Evaluator, Order, Payment, Fulfillment. Cada um com responsabilidade única e artefatos de entrada/saída. |
| **State Persistence** | SQLite + JSON checkpoints | `customer.json`, `order.json`, `cart.json` sobrevivem a restarts. SQLite armazena dados estruturados. Checkpoints permitem recovery. |
| **File-Based Coordination** | Lock files + status manifests | `order.lock.json`, `payment.lock.json` previnem conflitos. `status.json` mostra progresso visível para todos os agentes. |
| **Server-Side Compaction** | Classificação por criticidade | Fatos críticos (alergia) = preservados literalmente. Preferências (sabor) = sumarizadas. Small talk = removido. |
| **Harness Evolution** | Métricas + decision records | Cada componente de harness tem custo medido. Quando modelo melhora, componentes obsoletos são removidos com ADR. |

### Diagrama de Conexão N1-N3 → KODA

```
NÍVEL 1 — FUNDAMENTOS          NÍVEL 2 — PADRÕES               NÍVEL 3 — ARQUITETURA
─────────────────────          ─────────────────               ──────────────────────
Context Amnesia                Generator/Evaluator             Multi-Agent Systems
  │                              │                               │
  ▼                              ▼                               ▼
State Persistence              Recommend Stage                8 agentes especializados
(customer.json)                (draft.json → eval.json)       (Discovery, Catalog, etc.)
  │                              │                               │
  ├──────────────────────────────┼───────────────────────────────┤
  │                              │                               │
Token Budgeting                Sprint Contracts               State Persistence
  │                              │                               │
  ▼                              ▼                               ▼
Compactação + Catalog          Pipeline de vendas              SQLite + JSON checkpoints
Filter (só produtos             (6 etapas com contratos)       (sobrevive a restarts)
relevantes no contexto)
  │                              │                               │
  ├──────────────────────────────┼───────────────────────────────┤
  │                              │                               │
Harness Patterns               Rubric Design                  File-Based Coordination
  │                              │                               │
  ▼                              ▼                               ▼
Guardrails de validação        6 dimensões com pesos           Lock files + status
(verificar alergia antes        e thresholds                   (agentes não conflitam)
de recomendar)
  │                              │                               │
  ├──────────────────────────────┼───────────────────────────────┤
  │                              │                               │
Self-Evaluation Collapse       Trace Reading                  Server-Side Compaction
  │                              │                               │
  ▼                              ▼                               ▼
Evaluator externo               audit.jsonl + debug            Classificação por
(não self-evaluation)           scripts                        criticidade
                                                                │
                                                                ▼
                                                           Harness Evolution
                                                             │
                                                             ▼
                                                           Remoção de componentes
                                                           obsoletos com ADR
```

---

## 🛡️ Seção 7: Estado Atual do Harness KODA

### O que é o "Harness" do KODA?

O **harness** é o conjunto de componentes de suporte que envolvem os agentes: guards, validators, compactors, recovery logic, locks, retry mechanisms. São componentes que não geram valor diretamente para o cliente, mas que previnem falhas.

Pense no harness como o **cinto de segurança** do KODA. Você não percebe que ele existe até que algo dê errado — e aí ele salva a conversa.

### Componentes Ativos do Harness (Maio 2026)

| # | Componente | Função | Custo (latência) | Valor | Decisão |
|---|---|---|---|---|---|
| 1 | **Restriction Guard** | Bloqueia recomendação de produto com alérgeno do cliente | +50ms | CRÍTICO | Manter |
| 2 | **Budget Validator** | Rejeita recomendação acima do orçamento | +30ms | ALTO | Manter |
| 3 | **Stock Verifier** | Confirma estoque live antes de recomendar | +100ms | ALTO | Manter |
| 4 | **Double-Discount Check** | Previne aplicar dois descontos cumulativos incorretamente | +20ms | ALTO | Manter |
| 5 | **Idempotency Guard** | Previne cobrar cliente duas vezes | +80ms | CRÍTICO | Manter |
| 6 | **Tone Checker** | Verifica se resposta tem tom apropriado | +150ms | MÉDIO | Revisar — Claude Opus raramente erra tom |
| 7 | **Length Limiter** | Trunca respostas muito longas (>2000 caracteres) | +10ms | BAIXO | Remover — Generator já respeita max_tokens |
| 8 | **Small Talk Filter** | Remove "oi, tudo bem?" do contexto após compactação | +40ms | BAIXO | Absorver no Compactor |
| 9 | **Retry Manager** | Gerencia retry com exponential backoff | Variável | ALTO | Manter |
| 10 | **Circuit Breaker** | Interrompe chamadas após falhas consecutivas | +5ms | ALTO | Manter |

### Decisões de Harness Evolution Pendentes

**1. Tone Checker — Remover ou Manter?**

- **Argumento para remover:** Claude Opus 4.6 tem tom natural em >99% das respostas. O Tone Checker adiciona 150ms de latência e raramente rejeita algo.
- **Argumento para manter:** Em conversas de 4h, o tom pode degradar com fadiga de contexto. O Tone Checker pegou 3 incidents de tom inadequado no último mês.
- **Decisão pendente:** Coletar mais 1 mês de dados. Se <5 incidents, remover.

**2. Length Limiter — Remover**

- **Decisão:** Remover. O Generator já tem `max_tokens=2000`. O Limiter é redundante e adiciona complexidade sem valor.
- **ADR pendente:** Escrever ADR documentando a remoção.

**3. Small Talk Filter — Absorver no Compactor**

- **Decisão:** Mover a lógica de filtro de small talk para dentro do Server-Side Compactor. Elimina um componente separado.
- **Impacto:** -40ms de latência, -1 componente para manter.

### Métricas do Harness

```
Custo total do harness por conversa:
  Latência adicional: ~485ms
  Tokens adicionais: ~800 tokens
  Componentes: 10
  Componentes candidatos a remoção: 2

Meta para Julho 2026:
  Latência adicional: ~350ms (-28%)
  Componentes: 8 (-20%)
  Sem perda de confiabilidade
```

---

## 💼 Seção 8: Aplicações KODA — Casos Reais em Produção

### Caso 1: Product Discovery com Restrições Complexas

**Cenário real (Maio 2026):**

```
Cliente: "Oi KODA! Sou vegetariano, intolerante à lactose, 
         alérgico a castanhas, e estou treinando para uma 
         maratona. Preciso de algo para resistência, não 
         para hipertrofia. Ah, e moro em Florianópolis."
```

**Como o KODA processou:**

1. **Discovery Agent** extraiu 5 restrições estruturadas:
   - Dieta: vegetariano
   - Intolerância: lactose
   - Alergia: castanhas (inclui amêndoas, nozes, castanha de caju)
   - Objetivo: resistência (não hipertrofia)
   - Local: Florianópolis (afeta estoque e frete)

2. **Catalog Agent** filtrou catálogo de 500+ produtos para 6 candidatos:
   - Todos sem lactose
   - Todos sem castanhas (verificação cruzada com ingredientes)
   - Todos vegetarianos
   - Foco em resistência: carboidratos complexos, eletrólitos, BCAA
   - Em estoque no armazém Sul (PR)

3. **Generator** criou 3 recomendações:
   - 🥇 Maltodextrina + Eletrólitos (R$ 89) — energia sustentada
   - 🥈 BCAA Vegano (R$ 65) — recuperação muscular
   - 🥉 Gel de Carboidrato (R$ 45) — reposição durante prova

4. **Evaluator** aprovou as 3 (score 9.1) após verificar:
   - Nenhum produto contém castanhas (checagem de ingredientes)
   - Todos são vegetarianos (certificação)
   - Todos sem lactose (ficha técnica)

5. **Resultado:** Cliente comprou os 3 produtos. Voltou 2 semanas depois para recomprar.

**O que poderia ter dado errado sem a arquitetura:**

- Agente único: confundiria "castanhas" com "castanha de caju" vs "castanha-do-pará"
- Sem persistence: esqueceria que o cliente é vegetariano após 30 minutos de conversa
- Sem Evaluator: recomendaria whey protein (contém lactose, não é vegetariano)

---

### Caso 2: Order Processing com Cupom e Urgência

**Cenário real (Maio 2026):**

```
Cliente: "KODA, preciso de 2 wheys veganos chocolate e 1 creatina. 
         Tenho cupom PRIMEIRA50. Preciso que chegue amanhã porque 
         vou viajar. Dá tempo?"
```

**Como o KODA processou:**

1. **Order Agent** montou o carrinho:
   - 2x Whey Vegano Chocolate (SKU WHEY-VEGAN-005): 2 × R$ 149,90 = R$ 299,80
   - 1x Creatina Monohidratada (SKU CREATINA-002): 1 × R$ 65,00 = R$ 65,00
   - Subtotal: R$ 364,80

2. **Cupom PRIMEIRA50 validado:**
   - Válido? ✅ (primeiro pedido do cliente)
   - Não expirou? ✅ (válido até 30/06/2026)
   - Cumulativo com clube? ✅ (cliente não é membro do clube)
   - Desconto: 50% no item mais caro → -R$ 74,95

3. **Frete calculado:**
   - CEP: São Paulo — armazém SP-01
   - Same-day possível? ✅ (pedido antes das 15h)
   - Custo: R$ 19,90

4. **Total: R$ 364,80 - R$ 74,95 + R$ 19,90 = R$ 309,75**

5. **Payment Agent:**
   - Idempotency key gerada: `idem_ORD-20260527-0055_v1`
   - Transação processada: `txn_def789ghi012`
   - Status: confirmed

6. **Fulfillment Agent:**
   - Estoque verificado: WHEY-VEGAN-005 (45 un), CREATINA-002 (120 un)
   - Reserva confirmada
   - Tracking: TRK-456789123 (Loggi)
   - ETA: 27/05/2026 17:30 (2h de buffer)

7. **Resposta ao cliente:**
   ```
   "Tudo certo, João! 🎉
   
   Pedido #0055 confirmado:
   ✅ 2x Whey Vegano Chocolate
   ✅ 1x Creatina Monohidratada
   💰 Total: R$ 309,75 (economizou R$ 74,95 com PRIMEIRA50!)
   🚚 Chega hoje até 17:30
   📦 Tracking: TRK-456789123
   
   Posso ajudar com mais alguma coisa?"
   ```

**O que a arquitetura preveniu:**

- **Sem Order Agent:** Cupom aplicado incorretamente (50% no total, não no item mais caro)
- **Sem Payment Agent:** Risco de double-charge se timeout
- **Sem Fulfillment Agent:** Promessa de same-day sem verificar estoque real

---

### Caso 3: Recovery de Conversa Após Restart

**Cenário real (Maio 2026):**

O servidor do KODA foi reiniciado para deploy às 03:00 da manhã. Um cliente noturno (insônia) estava no meio de uma conversa de 2 horas. Ele tinha:
- Carrinho montado com 3 produtos
- Cupom aplicado
- Meio de pagamento selecionado
- Prestes a confirmar

**O que aconteceu:**

1. 03:00:01 — Servidor reinicia. Conexão com WhatsApp mantida (webhook re-registra).
2. 03:00:02 — Cliente envia: "Confirma o pedido então"
3. 03:00:03 — Webhook recebe mensagem
4. 03:00:03 — **Recovery Manager** detecta: conversation_id existe mas estado em memória foi perdido
5. 03:00:03 — Recovery Manager carrega do SQLite:
   - `customer.json` → perfil completo
   - `cart.json` → carrinho com 3 produtos
   - `order.json` → pedido pendente de pagamento
6. 03:00:04 — Recovery Manager carrega último checkpoint: estado está em "awaiting_payment_confirmation"
7. 03:00:04 — Pipeline retoma exatamente de onde parou
8. 03:00:05 — Payment Agent processa (verifica idempotência — não cobrado ainda)
9. 03:00:06 — Pedido confirmado. Cliente recebe tracking.

**Cliente nunca soube que o servidor reiniciou.**

**Sem Recovery Manager:**
- KODA responderia: "Olá! Como posso ajudar?" (como se fosse primeira conversa)
- Cliente: "Ué, mas eu já montei o carrinho todo!"
- Cliente precisaria refazer toda a conversa de 2 horas
- Experiência terrível, possível perda do cliente

---

## 📊 Seção 9: O Que Você Aprendeu

### Resumo dos Conceitos-Chave

| # | Conceito | Em uma frase |
|---|---|---|
| 1 | **Arquitetura em camadas** | WhatsApp API → Orchestration → Agent → Persistence → Infrastructure |
| 2 | **Pipeline de vendas** | 6 etapas com contratos: Discovery → Catalog → Recommend → Order → Payment → Fulfillment |
| 3 | **Fluxo de dados** | Mensagem do WhatsApp percorre todas as camadas em ~1.2s, passando por validação, classificação, geração, avaliação e envio |
| 4 | **Integração WhatsApp** | Webhook receiver + message sender + media handler + rate limits + retry logic |
| 5 | **Coordenação multi-agente** | File-based coordination como estratégia primária, com locks, status files e audit trail |
| 6 | **Conexão N1-N3** | Cada padrão dos níveis anteriores tem uma implementação concreta e rastreável no KODA |
| 7 | **Harness evolution** | Componentes de suporte são medidos por custo/valor. Obsoletos são removidos com ADR |
| 8 | **Generator/Evaluator em produção** | Opus (criativo) gera, Sonnet (rigoroso) avalia. Ciclo de até 3 iterações |
| 9 | **State persistence** | SQLite + JSON checkpoints garantem que nada é perdido em restarts |
| 10 | **Recovery automático** | Recovery Manager recarrega estado e retoma pipeline sem o cliente perceber |

### Checklist de Domínio

Antes de avançar para os próximos módulos do Nível 4, verifique se você consegue:

- [ ] Desenhar o diagrama ASCII da arquitetura completa de memória
- [ ] Explicar o fluxo de dados end-to-end de uma mensagem do WhatsApp
- [ ] Listar os 8 agentes e suas responsabilidades
- [ ] Descrever as 6 etapas do pipeline de vendas com entradas e saídas
- [ ] Explicar por que file-based coordination é a escolha primária
- [ ] Mapear 3 conceitos de N1, N2 e N3 para implementações no KODA
- [ ] Identificar qual componente de harness deve ser removido e por quê
- [ ] Explicar a estratégia de retry para WhatsApp API
- [ ] Calcular o custo estimado de tokens para uma conversa típica
- [ ] Diagnosticar um incidente real usando a classificação de problemas N1-N3

Se respondeu "não" para alguma:
- Releia a seção correspondente
- Desenhe o componente no papel
- Pense em um cenário onde ele seria crítico

---

## 🔮 Próximos Passos

Agora que você domina a arquitetura KODA, está pronto para mergulhar nos detalhes específicos:

### Próximo Módulo: `02-customer-journey-flows.md` (90 min)
Os fluxos completos de jornada do cliente: da descoberta ao pós-venda. Cada estado, transição, edge case e recovery path.

### Depois: `03-feature-design-patterns.md` (90 min)
Padrões de design para implementar novas features no KODA. Como estender a arquitetura sem quebrar o que funciona.

### Em Seguida: `04-evaluation-rubrics-koda.md` (90 min)
Rubrics completas para cada etapa do pipeline. Como calibrar thresholds. Como evoluir rubrics com dados reais.

### Finalmente: `05-harness-improvements.md` (90 min)
Estratégia completa de harness evolution. Como medir, decidir, remover e documentar mudanças no harness.

---

## ❓ FAQ

### P: "Por que 8 agentes? Não é complexo demais?"
**R:** Cada agente tem uma responsabilidade e apenas uma. A alternativa — um agente fazendo tudo — é que é complexa (e frágil). 8 agentes simples são mais fáceis de entender, testar e debugar que 1 agente complexo.

### P: "File-based coordination não é lento?"
**R:** Para centenas de conversas simultâneas, não. A latência de I/O de arquivo é ~1-5ms. Compare com latência de LLM (500-2000ms): o overhead de coordenação é <1% do tempo total. Quando o KODA escalar para dezenas de milhares de conversas, migraremos para Redis/PostgreSQL.

### P: "Por que usar Opus para Generator e Sonnet para Evaluator? Não poderia ser o contrário?"
**R:** Generator precisa de criatividade (explorar opções, considerar trade-offs, gerar explicações naturais). Opus é melhor nisso. Evaluator precisa de consistência e velocidade (aplicar rubrics é tarefa estruturada). Sonnet é 3-5x mais barato e igualmente bom para avaliação.

### P: "O que acontece se o WhatsApp Cloud API estiver fora do ar?"
**R:** O KODA mantém um buffer de mensagens pendentes. Se a API estiver fora, as respostas são enfileiradas e enviadas quando o serviço voltar. O cliente pode perceber delay, mas não perda de contexto. Templates de notificação (pedido confirmado, tracking) são re-enviados automaticamente.

### P: "Como vocês sabem que o harness está funcionando?"
**R:** Cada componente de harness gera métricas: quantas vezes foi acionado, quantas vezes rejeitou algo, quantas dessas rejeições eram corretas. Essas métricas são revisadas mensalmente. Componentes com baixa taxa de acionamento ou alta taxa de falsos positivos são candidatos a remoção.

### P: "Qual é o plano para quando Claude Opus 5.0 for lançado?"
**R:** Harness evolution. Vamos reavaliar cada componente: o modelo novo consegue fazer X sem o guard? Se sim, removemos o guard. O modelo novo é bom o suficiente para Generator E Evaluator? Se sim, consolidamos. A arquitetura é desenhada para evoluir com o modelo, não para ser estática.

### P: "O KODA funciona em outros países além do Brasil?"
**R:** Sim, a arquitetura é agnóstica de país. O WhatsApp Cloud API funciona globalmente. O que muda é: catálogo de produtos (regional), moeda (BRL, USD, etc.), idioma (português, espanhol, inglês), regras fiscais (impostos, cupons). Essas variações são configuradas, não codificadas.

### P: "Quanto custa rodar o KODA por mês?"
**R:** Para o volume atual (Maio 2026): ~247 conversas/dia, ~7.400 conversas/mês. Custo Claude API: ~R$ 2.500/mês. Infraestrutura (2 VMs + NFS): ~R$ 1.200/mês. Custo total: ~R$ 3.700/mês. Custo por conversa: ~R$ 0,50. ROI: cada venda gera em média R$ 50 de margem. Com 38 vendas/dia, margem mensal ~R$ 57.000. ROI = 15x.

### P: "Como vocês lidam com clientes que falam com muitos erros de português ou gírias?"
**R:** O Discovery Agent usa Claude Opus, que tem excelente compreensão de linguagem natural, incluindo erros ortográficos, gírias e abreviações comuns no WhatsApp ("vc", "blz", "eh"). Se a intenção não está clara, o Discovery pergunta educadamente: "Só para confirmar, você está procurando X, é isso?"

### P: "O KODA consegue vender produtos que não são suplementos?"
**R:** A arquitetura é genérica para e-commerce conversacional. Para vender outro tipo de produto (ex: eletrônicos, roupas), você precisaria: (1) trocar o catálogo de produtos, (2) ajustar rubrics para o novo domínio, (3) treinar Discovery para novas intenções. A arquitetura de agentes, pipeline e coordenação permanece a mesma.

### P: "Como vocês sabem se uma recomendação foi realmente boa? O cliente pode não reclamar."
**R:** Três formas: (1) taxa de recompra — cliente que voltou provavelmente gostou, (2) avaliação pós-compra — KODA pergunta "Gostou do produto?" após alguns dias, (3) taxa de devolução — se ninguém devolve, as recomendações estão boas. A combinação dessas 3 métricas dá uma visão real da qualidade.

### P: "Qual foi o pior incidente que o KODA já teve?"
**R:** Março 2026: um bug no Order Agent fez com que o desconto de clube (15%) fosse aplicado DUAS VEZES em 12 pedidos. Isso aconteceu porque o Order Agent não validava "double-discount" naquela época. O prejuízo foi de R$ 840 em descontos indevidos. Aprendizado: implementamos o Double-Discount Check no harness, que previne isso com 100% de eficácia desde então.

### P: "O que fazer se o KODA começar a agir de forma estranha em produção?"
**R:** 1) Abra o dashboard, veja qual agente está com métricas degradadas. 2) Abra o audit trail, procure por `"verdict":"REJECTED"` para ver se o Evaluator está rejeitando mais que o normal. 3) Se for um agente específico, veja os últimos `draft.json`, `evaluation.json` para aquela conversa. 4) Se for geral, verifique se houve deploy recente ou mudança de modelo. 5) Em último caso: circuit breaker no agente problemático, escala para on-call.

### P: "Posso usar o KODA como referência para construir meu próprio agente de vendas?"
**R:** Sim! A arquitetura descrita neste módulo é intencionalmente genérica: pipeline de vendas, agentes especializados, file-based coordination, state persistence, evaluator externo. Você pode adaptar para seu domínio trocando: catálogo, rubrics, integração de canal (WhatsApp → Telegram, Web, etc.), e domínio dos agentes.

### P: "Qual é a diferença entre o Planner Agent e o Orchestrator?"
**R:** O Orchestrator é o motor de execução (o código que coordena, chama agentes, gerencia locks). O Planner Agent é um agente de IA que decide O QUE fazer (quais sprints, em qual ordem, com quais contratos). Orchestrator = como executar. Planner = o que executar.

### P: "Por que SQLite e não PostgreSQL?"
**R:** SQLite é single-writer, o que é uma limitação, mas também uma simplificação. Para a carga atual do KODA (~200 conversas simultâneas), SQLite é mais que suficiente. Quando escalarmos para milhares de conversas simultâneas, migraremos para PostgreSQL. A decisão foi: complexidade certa para o tamanho certo.

### P: "Como o KODA lida com clientes que alternam entre português e inglês?"
**R:** O Discovery Agent detecta o idioma predominante e ajusta as respostas. Se o cliente mistura ("quero um whey protein, but without lactose"), o KODA responde no idioma predominante da conversa. Termos técnicos são mantidos em inglês (whey protein, BCAA, etc.) como convenção.

### P: "O KODA pode iniciar conversas ou só responde?"
**R:** O KODA só responde a mensagens iniciadas pelo cliente (requisito do WhatsApp Business API). Ele pode enviar templates de notificação (pedido confirmado, tracking, follow-up pós-compra) dentro de 24h da última mensagem do cliente. Após 24h, só templates aprovados pelo WhatsApp.

### P: "Qual é o plano de disaster recovery?"
**R:** (1) Backup diário do SQLite para storage externo. (2) JSON state files são replicados via NFS para storage secundário. (3) Audit trail é append-only e replicado. (4) Em caso de perda total do datacenter primário: restore do backup mais recente (perda máxima: 24h de dados de conversa; pedidos financeiros têm backup separado em tempo real). (5) Tempo de recovery: ~30 minutos para voltar ao ar.

### P: "O que acontece se dois clientes diferentes comprarem o último item em estoque ao mesmo tempo?"
**R:** O sistema de locks previne isso. Quando o primeiro cliente inicia o checkout, o Fulfillment Agent adquire `inventory.lock.json` para aquele SKU e reserva as unidades. Se o segundo cliente tentar comprar simultaneamente, ele encontrará o lock e aguardará. Quando o lock for liberado, o inventário já estará atualizado (0 unidades). O segundo cliente receberá: "Desculpe, este produto acabou de esgotar. Posso sugerir uma alternativa?"

### P: "Como vocês testam mudanças no KODA sem afetar clientes reais?"
**R:** (1) Testes unitários e de integração no CI. (2) Deploy canário: nova versão em 1 instância com 10% do tráfego. (3) WhatsApp Sandbox: ambiente de teste com número de WhatsApp dedicado para testes manuais. (4) Shadow mode: nova versão processa conversas reais em paralelo (sem enviar resposta) e compara output com a versão atual. (5) Rollback automático se métricas degradarem >10%.

### P: "Qual foi a decisão arquitetural mais difícil que vocês tomaram?"
**R:** Escolher file-based coordination em vez de message queue (RabbitMQ/Kafka). A decisão foi controversa na época — parecia "pouco escalável". Mas se provou correta: a simplicidade de debugar com `cat` e `grep` nos arquivos JSON salvou dezenas de horas de investigação. A migração para message queue está planejada, mas apenas quando a carga atual (centenas de conversas) for 10x maior. A lição: não otimize prematuramente.

### P: "O KODA usa RAG (Retrieval-Augmented Generation)?"
**R:** Sim, indiretamente. O Catalog Agent faz retrieval do catálogo de produtos e inventário (via Inventory System + SQLite cache). O Discovery Agent faz retrieval do histórico do cliente (via SQLite). Mas não usamos vector databases ou embeddings — o catálogo do KODA tem ~500 produtos, e filtros estruturados (categoria, preço, alergênicos) são mais eficazes e determinísticos que busca semântica para este volume.

### P: "Como vocês mantêm a qualidade das respostas ao longo do tempo? Não há 'drift'?"
**R:** Monitoramos 3 métricas de drift: (1) Taxa de aprovação do Evaluator — se começar a cair, algo mudou no Generator ou nos dados. (2) Satisfação do cliente (medida por recompra e avaliações) — se cair, a qualidade percebida piorou. (3) Distribuição de scores das rubrics — se a média cair, recalibramos. Revisão trimestral de rubrics garante que os critérios de qualidade evoluem com o negócio.

### P: "Se eu tivesse que resumir a arquitetura KODA em 3 princípios, quais seriam?"
**R:** (1) **Separe geração de avaliação** — nunca deixe o mesmo agente criar e julgar. (2) **Persista o que é crítico** — alergias, orçamento e pedidos vivem no disco, não na memória do modelo. (3) **Evolua o harness** — o que era necessário com Claude 3.5 pode ser peso morto com Claude 5.0. Meça, decida, remova.

---

## 🎨 Diagrama Resumo: A Arquitetura KODA em Uma Página

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                         KODA — ARQUITETURA RESUMIDA                          ║
║                     WhatsApp Sales Agent — Maio 2026                         ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║  📱 WHATSAPP API LAYER                                                        ║
║  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                       ║
║  │ Webhook Recv │  │ Message Sender│  │ Media Handler│                       ║
║  └──────┬───────┘  └──────────────┘  └──────────────┘                       ║
║         │                                                                     ║
║  🎯 ORCHESTRATION LAYER                                                       ║
║  ┌──────────────────────────────────────────────────────────────────┐       ║
║  │ Orchestrator: Planner → Router → Scheduler → Recovery Manager     │       ║
║  └──────────────────────────────────────────────────────────────────┘       ║
║         │                                                                     ║
║  🤖 AGENT LAYER                                                               ║
║  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌────────┐    ║
║  │Discovery│→│ Catalog │→│Generator│→│Evaluator│→│  Order  │→│Payment │    ║
║  │         │ │         │ │ (Opus)  │ │ (Sonnet)│ │         │ │(no LLM)│    ║
║  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘ └───┬────┘    ║
║                                                                   │         ║
║  ┌──────────────────────────────────────────────────────────────┘         ║
║  │  ┌──────────────┐                                                       ║
║  └─►│ Fulfillment  │                                                       ║
║     └──────────────┘                                                       ║
║                                                                               ║
║  💾 PERSISTENCE LAYER                                                         ║
║  ┌────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐                      ║
║  │ SQLite │  │ JSON     │  │ Lock     │  │ Audit    │                      ║
║  │        │  │ State    │  │ Files    │  │ Trail    │                      ║
║  └────────┘  └──────────┘  └──────────┘  └──────────┘                      ║
║                                                                               ║
║  ⚙️  INFRASTRUCTURE                                                            ║
║  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐                    ║
║  │ Claude   │  │ WhatsApp │  │ Inventory│  │ Payment  │                    ║
║  │ API      │  │ Cloud API│  │ System   │  │ Gateway  │                    ║
║  └──────────┘  └──────────┘  └──────────┘  └──────────┘                    ║
║                                                                               ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  📊 MÉTRICAS-CHAVE (Maio 2026)                                                ║
║  Precisão: 98.1%  │  Conversas/dia: 247  │  Vendas/dia: 38                  ║
║  Custo/conv: $0.17  │  Latência p95: 2.1s  │  Uptime: 99.97%               ║
║                                                                               ║
║  🔗 NÍVEIS APLICADOS                                                          ║
║  N1: State Persistence, Token Budgeting, Basic Harness                       ║
║  N2: Generator/Evaluator, Sprint Contracts, Rubrics, Trace Reading           ║
║  N3: Multi-Agent, File-Based Coord, Compaction, Harness Evolution            ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## ✅ Checklist de Auditoria de Arquitetura

Use esta checklist para revisar a arquitetura KODA periodicamente (recomendado: a cada 3 meses ou após grandes mudanças).

### Camada WhatsApp API
- [ ] Validação HMAC está ativa em 100% dos webhooks?
- [ ] Rate limits estão sendo respeitados (<80% do limite)?
- [ ] Retry com exponential backoff está configurado?
- [ ] Templates de notificação estão com quality rating "GREEN"?
- [ ] Media uploads estão sendo comprimidos antes do envio?

### Camada Orchestration
- [ ] Planner Agent está dividindo jornadas em sprints ≤5 etapas?
- [ ] Router está classificando intenções com >95% de precisão?
- [ ] Recovery Manager tem checkpoints a cada sprint concluído?
- [ ] Timeout máximo de execução está configurado (não infinito)?

### Camada Agent
- [ ] Cada agente tem responsabilidade única e clara?
- [ ] Nenhum agente está fazendo self-evaluation?
- [ ] Artefatos de entrada e saída estão documentados com schema?
- [ ] Temperatura e max_tokens estão otimizados para cada agente?
- [ ] Fallback de modelo está configurado para cada agente?

### Camada Persistence
- [ ] SQLite está com backup diário configurado?
- [ ] JSON state files têm backup (.bak) antes de escrita?
- [ ] Lock files têm TTL configurado (não infinito)?
- [ ] Audit trail é append-only (nunca modificado)?
- [ ] Rotação de audit trail está ativa (>30 dias)?

### Pipeline de Vendas
- [ ] Customer.json é validado pelo Evaluator antes de avançar?
- [ ] Catalog.json usa dados live (não cache expirado)?
- [ ] Draft.json passa por Evaluator com rubrics antes do cliente?
- [ ] Order.json tem double-discount check?
- [ ] Payment tem idempotency key única por pedido?
- [ ] Fulfillment verifica estoque live (não cache)?

### Segurança
- [ ] PII está sendo sanitizada nos logs?
- [ ] Dados de cartão NUNCA passam pelo KODA?
- [ ] Rate limit por cliente está ativo?
- [ ] Circuit breaker está configurado para serviços externos?

### Evolução
- [ ] Métricas de cada componente de harness são coletadas?
- [ ] Componentes com baixo valor são identificados?
- [ ] ADRs são escritos para remoções?
- [ ] O harness está menor que no trimestre anterior?

---

## 🔧 Seção 10: Error Handling e Resiliência

### A Filosofia de Erro do KODA

O KODA opera sob o princípio de que **falhas são inevitáveis**. A pergunta não é "se" algo vai falhar, mas "quando" e "como o sistema reage".

A filosofia de erro segue 4 regras:

1. **Fail Fast**: Se algo está errado, pare imediatamente. Não continue com dados inconsistentes.
2. **Fail Loud**: Erros são registrados com contexto completo. Nada de `try { } catch (e) {}` silencioso.
3. **Fail Safe**: Se possível, degrade gracefulmente. Não perca o carrinho do cliente.
4. **Fail Once**: Retry é controlado. Nada de loops infinitos.

### Hierarquia de Erros do KODA

```
SEVERITY    TIPO                    AÇÃO                           EXEMPLO
─────────────────────────────────────────────────────────────────────────────
CRITICAL    Dados inconsistentes    Aborta pipeline,                customer.json
            ou risco ao cliente     escala para Recovery           com ID inválido

HIGH        Falha de agente ou      Retry (máx 3x) com             Generator
            serviço externo         exponential backoff            timeout

MEDIUM      Degradação de           Continua com warn,             Catalog retornou
            qualidade               registra para revisão          3 produtos, não 8

LOW         Ineficiência            Continua, métrica              2ª iteração do
                                    registrada                     Generator
```

### Cenários de Falha e Recuperação

| Cenário | Gatilho | Resposta do KODA | Impacto no Cliente |
|---|---|---|---|
| **WhatsApp API fora do ar** | Erro 5xx persistente | Mensagens enfileiradas, enviadas quando API volta | Delay na resposta (segundos a minutos) |
| **Claude API timeout** | Generator >10s sem resposta | Retry com backoff. Se 3 falhas, escala para modelo fallback (Sonnet para Generator) | Resposta pode ser menos criativa, mas ainda funcional |
| **Inventory System fora do ar** | Catalog Agent timeout | Usa cache de inventário (SQLite, <5min old). Se cache expirado, informa cliente: "Estou verificando estoque..." | Pequeno delay, possível imprecisão se estoque mudou |
| **Payment Gateway timeout** | Payment Agent timeout | Verifica idempotency key ANTES de retentar. Se já cobrado, retorna confirmação | Zero risco de double-charge |
| **Servidor restart** | SIGTERM/SIGKILL | Recovery Manager recarrega estado do SQLite + JSON checkpoints | Imperceptível (<2s) |
| **Lock contention** | 2 agentes tentando mesmo lock | Segundo agente espera (TTL 5s) e retenta. Se timeout, loga e escala | Nenhum (resolvido internamente) |
| **Corrupção de JSON state file** | JSONDecodeError ao ler | Tenta ler backup (.bak). Se também corrompido, recarrega do SQLite checkpoint | Possível perda de estado parcial |
| **Modelo gera output mal formatado** | JSONDecodeError no Evaluator | Generator é chamado novamente com feedback: "Output deve ser JSON válido" | Delay de 1-2s para retentativa |

### Código: Retry com Exponential Backoff

```python
async def agent_with_retry(agent_fn, max_retries=3, base_delay_ms=1000):
    """Wrapper que adiciona retry com exponential backoff a qualquer agente."""
    for attempt in range(max_retries):
        try:
            return await agent_fn()
        except RetryableError as e:
            if attempt == max_retries - 1:
                raise MaxRetriesExceeded(f"Agente falhou após {max_retries} tentativas: {e}")
            delay_s = (2 ** attempt) * (base_delay_ms / 1000)
            await asyncio.sleep(delay_s)
            log_warning(f"Retry {attempt + 1}/{max_retries} do agente. Delay: {delay_s}s")
        except NonRetryableError:
            raise  # Não retenta. Erro é fatal.
```

---

## 📈 Seção 11: Monitoramento e Observabilidade

### As 3 Perguntas que o Monitoramento Responde

1. **O sistema está saudável agora?** → Health checks, dashboards, alertas
2. **O que aconteceu naquela conversa específica?** → Audit trail, trace reading
3. **Estamos melhorando ou piorando?** → Métricas de tendência, KPIs

### Métricas-Chave por Agente

| Agente | Métrica Primária | Target | Alerta se | Ação |
|---|---|---|---|---|
| **Discovery** | Taxa de extração completa | >95% | <90% | Revisar prompts de extração |
| **Catalog** | Precisão de filtro | >99% | <97% | Verificar sync com Inventory |
| **Generator** | Taxa de aprovação (1ª tentativa) | >80% | <70% | Revisar rubrics ou Generator prompt |
| **Evaluator** | Falsos positivos (aprovou errado) | <0.5% | >1% | Recalibrar rubrics |
| **Order** | Erros de cálculo | <0.1% | >0.5% | Revisar lógica de desconto |
| **Payment** | Double-charge incidents | 0 | >0 | P0 — parar tudo, investigar |
| **Fulfillment** | Acurácia de ETA | >90% | <85% | Revisar buffer de tempo |

### Audit Trail: O Registro Imutável

Cada operação no KODA gera uma entrada no `audit.jsonl`. Este arquivo é append-only e nunca é modificado.

```jsonl
{"ts":"2026-05-27T14:30:00Z","ev":"session_start","sid":"sess_001","cust":"wa_5511987654321"}
{"ts":"2026-05-27T14:30:05Z","ev":"webhook_received","msg_id":"wamid.abc","intent":"purchase_request"}
{"ts":"2026-05-27T14:30:10Z","ev":"agent_called","agent":"Discovery","sid":"sess_001"}
{"ts":"2026-05-27T14:30:15Z","ev":"artifact_written","file":"customer.json","agent":"Discovery"}
{"ts":"2026-05-27T14:30:15Z","ev":"agent_called","agent":"Evaluator","target":"Discovery_output"}
{"ts":"2026-05-27T14:30:18Z","ev":"evaluation_complete","verdict":"APPROVED","score":9.5}
{"ts":"2026-05-27T14:30:20Z","ev":"agent_called","agent":"Catalog","sid":"sess_001"}
{"ts":"2026-05-27T14:30:25Z","ev":"artifact_written","file":"catalog.json","agent":"Catalog","products":8}
{"ts":"2026-05-27T14:30:30Z","ev":"agent_called","agent":"Generator","sid":"sess_001"}
{"ts":"2026-05-27T14:30:45Z","ev":"artifact_written","file":"draft.json","agent":"Generator","iteration":1}
{"ts":"2026-05-27T14:30:50Z","ev":"agent_called","agent":"Evaluator","target":"Generator_output"}
{"ts":"2026-05-27T14:30:55Z","ev":"evaluation_complete","verdict":"REJECTED","score":5.2,"reason":"budget_exceeded"}
{"ts":"2026-05-27T14:30:55Z","ev":"feedback_written","file":"feedback.json","issues":["budget"]}
{"ts":"2026-05-27T14:31:00Z","ev":"agent_called","agent":"Generator","sid":"sess_001","iteration":2}
{"ts":"2026-05-27T14:31:15Z","ev":"artifact_written","file":"draft.json","agent":"Generator","iteration":2}
{"ts":"2026-05-27T14:31:20Z","ev":"agent_called","agent":"Evaluator","target":"Generator_output_v2"}
{"ts":"2026-05-27T14:31:25Z","ev":"evaluation_complete","verdict":"APPROVED","score":9.2}
{"ts":"2026-05-27T14:31:30Z","ev":"message_sent","msg_id":"wamid.def","type":"interactive"}
{"ts":"2026-05-27T14:31:30Z","ev":"session_active","sid":"sess_001","status":"awaiting_customer_response"}
```

---

## 🎯 Seção 12: Exercícios de Fixação

### Exercício 1: Desenhe a Arquitetura

**Instrução:** Sem consultar o documento, desenhe o diagrama ASCII da arquitetura KODA incluindo:
- As 5 camadas
- Os 8 agentes com suas responsabilidades
- O fluxo de dados entre camadas
- Os artefatos (arquivos JSON) produzidos por cada agente

**Tempo:** 15 minutos

---

### Exercício 2: Diagnosticando um Incidente

**Cenário:** Você recebe este relato do suporte:

```
"Cliente ligou reclamando. Ele conversou com o KODA por 3 horas ontem.
No final, o KODA recomendou um whey protein com creatina.
O cliente já tinha dito que NÃO QUER creatina, só whey puro.
O KODA tinha anotado essa restrição no começo da conversa.
Mas 3 horas depois, recomendou o produto errado."
```

**Perguntas:**

1. Qual(is) dos 3 problemas de Nível 1 está(ão) se manifestando aqui? Justifique.
2. Em qual etapa do pipeline de vendas a falha ocorreu? (Discovery? Catalog? Recommend?)
3. Qual componente da arquitetura deveria ter prevenido este erro? O que pode ter falhado?
4. Proponha uma melhoria concreta no harness para evitar que isso se repita.

---

### Exercício 3: Calculando o Pipeline

**Cenário:** Um cliente com: orçamento máximo R$ 250, alergia a castanha de caju, preferência sabor baunilha, membro do clube (15% desconto), cupom BEMVINDO20 (20% no primeiro pedido).

**Catálogo filtrado:**
| SKU | Nome | Preço | Sem castanha? | Sabor baunilha? |
|---|---|---|---|---|
| WHEY-A | Whey Pro | R$ 180 | ✅ Sim | ✅ Sim |
| WHEY-B | Whey Max | R$ 220 | ✅ Sim | ❌ Não |
| WHEY-C | Whey Fit | R$ 150 | ❌ Contém | ✅ Sim |
| WHEY-D | Whey Premium | R$ 260 | ✅ Sim | ✅ Sim |

**Perguntas:**

1. Quais produtos passam pelo filtro do Catalog Agent? Por quê?
2. Se o Generator recomendar WHEY-A com cupom BEMVINDO20, o Order Agent deve aplicar também o desconto de clube? Justifique.
3. Calcule o preço final de WHEY-A considerando a regra: "desconto de clube NÃO é cumulativo com cupons promocionais. Aplica-se o maior."

---

### Exercício 4: Coordenação Multi-Agente

**Cenário:** Dois agentes tentam processar o mesmo pedido ao mesmo tempo:
- Order Agent cria `order.json` para o pedido #0088
- Payment Agent lê `order.json` e tenta cobrar
- Simultaneamente, Recovery Agent detecta um possível problema e tenta reverter o pedido

**Perguntas:**

1. Como o sistema de locks previne conflitos neste cenário?
2. Se o Payment Agent já iniciou a cobrança quando o Recovery Agent tenta reverter, o que acontece?
3. Projete o fluxo de locks para este cenário: quem adquire qual lock, em qual ordem?

---

### Exercício 5: Harness Evolution

**Cenário:** Claude Opus 5.0 foi lançado. Ele tem: janela de contexto de 2M tokens (dobro do Opus 4.6), melhor precisão em restrições (99.7% vs 98% atual), custo 30% menor por token.

**Perguntas:**

1. Quais componentes do harness atuais são candidatos a remoção com Opus 5.0? Justifique.
2. O Tone Checker (150ms, raramente rejeita) deve ser removido? Justifique com dados.
3. Se você remover o Restriction Guard, qual métrica você monitoraria para confirmar que a decisão foi correta?
4. Escreva um esboço de ADR para a remoção do Length Limiter.

---

## 🔐 Seção 13: Considerações de Segurança

### Superfície de Ataque do KODA

| Vetor | Risco | Mitigação |
|---|---|---|
| **Webhook spoofing** | Atacante envia mensagens falsas como se fossem clientes | Validação HMAC-SHA256 obrigatória em todo webhook |
| **Injection via mensagem** | Cliente envia prompt injection para manipular KODA | System prompt blinda contra instruções do usuário |
| **Data exfiltration** | KODA vaza dados de outros clientes | `customer.json` é isolado por `customer_id` |
| **Payment fraud** | Atacante manipula preço no carrinho | Order Agent recalcula preço server-side |
| **PII em logs** | Dados pessoais vazam em logs | Sanitização de PII. Phone numbers hasheados. Nomes truncados |
| **Race condition em inventário** | 2 clientes compram o último item | Lock files + inventário live. Reservation é atômica |
| **Denial of Wallet** | Atacante gera conversas infinitas para gastar tokens | Rate limit por phone number: máx 50 mensagens/hora |

### Política de Dados

```
DADOS QUE O KODA ARMAZENA:
✅ customer.json: preferências, restrições, histórico de compras
✅ order.json: pedidos, valores, status
❌ NUNCA: dados de cartão de crédito
❌ NUNCA: documentos de identidade

RETENÇÃO:
- Dados de conversa: 90 dias
- Dados de pedido: 5 anos (obrigação fiscal)
- Audit trail: 1 ano
```

---

## 🎓 Seção 14: Lições Aprendidas e Anti-Padrões

### O que Aprendemos Construindo o KODA

| # | Lição | Contexto |
|---|---|---|
| 1 | **Simplicidade primeiro** | File-based coordination funcionou para centenas de conversas. Se tivéssemos começado com Kafka, semanas perdidas. |
| 2 | **Separação de concerns** | O maior salto de qualidade (75% → 98%) veio de SEPARAR Generator de Evaluator, não de melhorar prompts. |
| 3 | **Tudo crítico vai para o disco** | Alergias, orçamento, pedidos. Nada fica só na memória do modelo. |
| 4 | **Métricas ou feeling? Métricas.** | Precisão 98% é métrica. Latência p95 é métrica. Sem números, você está adivinhando. |
| 5 | **Remova o que não agrega valor** | Harness evolution é contínuo. Length Limiter removido. Small Talk Filter absorvido. |
| 6 | **Audit trail salva investigações** | Quando algo falha, o `audit.jsonl` conta a história completa. |
| 7 | **Circuit breaker previne cascata** | 3 falhas consecutivas → circuit open → protege o sistema. |
| 8 | **Idempotência é sagrada** | Cobrar cliente duas vezes é inaceitável. Idempotency keys garantem zero double-charge. |

### Anti-Padrões que o KODA Evitou

| Anti-Padrão | Por que é ruim | Como o KODA evita |
|---|---|---|
| **God Agent** | Um agente faz tudo | 8 agentes especializados com responsabilidades únicas |
| **Memory-Only State** | Estado em RAM. Restart = perda total | SQLite + JSON checkpoints + Recovery Manager |
| **Self-Evaluation** | Agente avalia o próprio trabalho | Evaluator é agente separado, incentivado a encontrar erros |
| **Silent Failures** | Erros engolidos, sistema parece OK | Fail loud: todo erro logado com contexto completo |
| **Infinite Retries** | Consome recursos, nunca resolve | Máximo 3 retries. Depois, escala para humano |
| **Premature Optimization** | Kafka antes de precisar | File-based coordination. SQLite. Simples e suficiente |
| **Static Harness** | Acumula complexidade sem revisão | Harness evolution: métricas, ADRs, remoção de obsoletos |

---

## 🗂️ Seção 15: Referência de Schemas de Dados

Esta seção documenta todos os schemas JSON usados na arquitetura KODA. Use como referência rápida quando estiver implementando ou debugando.

### Schema: customer.json (Discovery Agent output)

```
customer.json
├── customer_id: string (ex: "wa_5511987654321")
├── session_id: string (ex: "sess_20260527_001")
├── discovered_at: ISO8601 timestamp
├── intent
│   ├── primary: string (purchase | research | complaint | question)
│   ├── goal: string (ganho_muscular | emagrecimento | energia | saude_geral)
│   └── confidence: float (0.0 a 1.0)
├── profile
│   ├── name: string
│   ├── level: string (iniciante | intermediario | avancado)
│   ├── training_frequency: string
│   └── training_type: string
├── restrictions
│   ├── allergies: string[]
│   ├── intolerances: string[]
│   ├── dietary: string[]
│   ├── religious: string[]
│   └── medical: string[]
├── preferences
│   ├── flavors: string[]
│   ├── brands: string[]
│   ├── format: string (po | capsula | liquido | barra)
│   └── avoid: string[]
├── budget
│   ├── max_per_product: number
│   ├── max_total: number
│   └── sensitive_to_price: boolean
├── history
│   ├── previous_purchases: [{sku, name, liked}]
│   ├── previous_returns: []
│   └── previous_complaints: string[]
└── urgency
    ├── needs_by: ISO8601 date
    ├── delivery_preference: string (fastest | cheapest | scheduled)
    └── same_day_eligible: boolean
```

### Schema: catalog.json (Catalog Agent output)

```
catalog.json
├── catalog_id: string
├── queried_at: ISO8601 timestamp
├── filters_applied
│   ├── category: string[]
│   ├── exclude_allergens: string[]
│   ├── max_price: number
│   ├── in_stock_region: string
│   └── flavors: string[]
├── products: Product[]
│   └── Product
│       ├── sku: string
│       ├── name: string
│       ├── category: string
│       ├── price_base: number
│       ├── price_promo: number | null
│       ├── stock_{region}: number
│       ├── rating: number (0.0 a 5.0)
│       ├── lactose_free: boolean
│       ├── vegan: boolean
│       ├── flavors_available: string[]
│       ├── protein_per_serving_g: number
│       ├── servings: number
│       └── delivery_days_{region}: number
├── total_candidates: number
└── promotions_active: string[]
```

### Schema: draft.json (Generator Agent output)

```
draft.json
├── generation_id: string
├── iteration: number (1 a 3)
├── generated_at: ISO8601 timestamp
├── recommendations: Recommendation[]
│   └── Recommendation
│       ├── rank: number
│       ├── sku: string
│       ├── name: string
│       ├── price_base: number
│       ├── price_final: number
│       ├── discounts_applied: string[]
│       ├── rationale: string (explicação para o cliente)
│       └── comparative: string (comparação com alternativas)
├── generator_confidence: float (0.0 a 1.0)
└── notes: string (notas internas do Generator)
```

### Schema: evaluation.json (Evaluator Agent output)

```
evaluation.json
├── evaluation_id: string
├── generation_id: string (referência ao draft.json)
├── evaluated_at: ISO8601 timestamp
├── verdict: "APPROVED" | "REJECTED"
├── rubric_scores
│   ├── restrictions_respected: {score, max, detail}
│   ├── budget_within_range: {score, max, detail}
│   ├── in_stock_verified: {score, max, detail}
│   ├── explanation_clarity: {score, max, detail}
│   ├── tone_appropriateness: {score, max, detail}
│   └── no_contradictions: {score, max, detail}
├── overall_score: number (0.0 a 10.0)
├── approval_threshold: number (default: 7.0)
├── status: "APPROVED" | "REJECTED"
└── issues?: Issue[]
    └── Issue {product, issue, severity, message}
```

### Schema: order.json (Order Agent output)

```
order.json
├── order_id: string (ex: "ORD-20260527-0042")
├── customer_id: string
├── created_at: ISO8601 timestamp
├── status: string (pending_payment | paid | fulfilled | cancelled)
├── items: OrderItem[]
│   └── OrderItem {sku, name, quantity, unit_price, total_price}
├── subtotal: number
├── discounts: Discount[]
│   └── Discount {code, type, amount}
├── shipping: {cep, method, cost}
├── total: number
├── applied_coupons: string[]
└── double_discount_check: "passed" | "failed"
```

### Schema: txn.json (Payment Agent output)

```
txn.json
├── transaction_id: string
├── order_id: string
├── idempotency_key: string
├── amount: number
├── currency: string
├── method: string
├── status: "confirmed" | "failed" | "pending"
├── gateway_response: string
└── processed_at: ISO8601 timestamp
```

### Schema: fulfillment.json (Fulfillment Agent output)

```
fulfillment.json
├── fulfillment_id: string
├── order_id: string
├── status: string (reserved | picked | shipped | delivered)
├── items_reserved: ReservedItem[]
│   └── ReservedItem {sku, quantity, warehouse}
├── delivery
│   ├── method: string
│   ├── tracking_number: string
│   ├── carrier: string
│   ├── eta: ISO8601 timestamp
│   ├── buffer_minutes: number
│   └── address_confirmed: boolean
└── created_at: ISO8601 timestamp
```

### Schema: audit.jsonl (Audit Trail)

```
Cada linha é um JSON autônomo com:
├── ts: ISO8601 timestamp (sempre presente)
├── ev: string (evento: session_start, webhook_received, agent_called, etc.)
├── sid: string (session_id, quando aplicável)
├── cust: string (customer_id, quando aplicável)
├── agent: string (nome do agente, quando aplicável)
├── file: string (artefato escrito, quando aplicável)
├── verdict: "APPROVED" | "REJECTED" (quando aplicável)
├── score: number (quando aplicável)
└── ... campos adicionais específicos do evento
```

---

## 🔄 Seção 16: Guia de Migração — De Agente Único para Multi-Agente

### O Caminho que o KODA Percorreu

Se você está começando um projeto similar ao KODA, provavelmente não quer implementar 8 agentes de uma vez. Esta seção mostra o caminho de migração incremental que o KODA seguiu — e que você pode seguir também.

### Fase 0: Protótipo (1 agente)

```
WHATSAPP → [KODA único] → RESPOSTA

Características:
- 1 agente faz tudo
- Prompt grande com instruções
- Sem persistência de estado
- Sem avaliação separada

Métricas típicas:
- Precisão: 70-75%
- Conversas máximas: ~45 minutos antes de degradar
- Recuperação de restart: zero

Quando migrar:
- Clientes reclamam de inconsistência
- Conversas >1h ficam ruins
- Você não consegue debugar por que algo falhou
```

### Fase 1: Nível 1 — Fundação (1 agente + harness)

```
WHATSAPP → [KODA + State Persistence + Token Budgeting + Validators] → RESPOSTA

O que adicionar:
✅ customer.json (persistência de estado crítico)
✅ Token budgeting (reserva de espaço para pensar)
✅ Validators básicos (alergia, orçamento)

Tempo: 1-2 semanas
Ganho: Precisão sobe para 80-85%. Conversas de 2h funcionam.
```

### Fase 2: Nível 2 — Qualidade (Generator + Evaluator)

```
WHATSAPP → [Generator] → [Evaluator] → RESPOSTA

O que adicionar:
✅ Generator Agent (cria recomendações)
✅ Evaluator Agent (avalia contra rubrics)
✅ Feedback loop (até 3 iterações)

Tempo: 2-3 semanas
Ganho: Precisão sobe para 92-95%. Maior salto de qualidade.
```

### Fase 3: Nível 3 Inicial — Especialização (4 agentes)

```
WHATSAPP → [Discovery] → [Catalog] → [Generator] → [Evaluator] → RESPOSTA

O que adicionar:
✅ Discovery Agent (extrai perfil, separado do Generator)
✅ Catalog Agent (filtra produtos, separado do Generator)
✅ Sprint Contracts entre agentes

Tempo: 2-3 semanas
Ganho: Precisão 95-97%. Melhor separação de concerns.
```

### Fase 4: Nível 3 Completo — Pipeline (6-8 agentes)

```
WHATSAPP → [Discovery → Catalog → Generator → Evaluator → Order → Payment → Fulfillment]
                   ↑                     ↑                    ↑
            [Planner]            [Recovery Manager]    [Lock Files]

O que adicionar:
✅ Order Agent, Payment Agent, Fulfillment Agent
✅ Planner Agent (roteamento)
✅ Recovery Manager (checkpoint + retry)
✅ Lock files (coordenação)
✅ Server-Side Compaction

Tempo: 3-4 semanas
Ganho: Pipeline completo. Recuperação de falhas. 98%+ precisão.
```

### Tabela Comparativa das Fases

| Fase | Agentes | Precisão | Duração máx conversa | Custo/conv | Complexidade |
|---|---|---|---|---|---|
| 0 | 1 | 70-75% | 45 min | $0.03 | Baixa |
| 1 | 1 + harness | 80-85% | 2h | $0.05 | Média-baixa |
| 2 | 3 (Gen+Eval+Cat) | 92-95% | 2h | $0.10 | Média |
| 3 | 4-5 | 95-97% | 3h | $0.13 | Média-alta |
| 4 | 8 completo | 98%+ | 4h+ | $0.17 | Alta |

### Quando Pular Fases

- **Pule da Fase 0 para Fase 2** se você já tem clientes reais e o problema principal é qualidade de recomendação
- **Pule da Fase 2 para Fase 4** se você precisa de pipeline completo de vendas (carrinho → pagamento → entrega)
- **Fique na Fase 3** se seu produto é apenas recomendação (sem venda direta)

### Checklist de Migração

Para cada transição de fase, verifique:

- [ ] Testes de regressão passam (conversas antigas ainda funcionam)
- [ ] Métricas da fase anterior não degradaram
- [ ] Nova fase entrega a melhoria prometida (ex: precisão subiu?)
- [ ] Custo adicional é justificado pelo ganho
- [ ] Equipe entende os novos componentes
- [ ] Documentação atualizada (este arquivo!)

---

## 🔍 Seção 17: Troubleshooting — Quando as Coisas Dão Errado

### Guia Rápido de Diagnóstico

Esta seção é para quando você está de plantão e algo quebrou. Siga o fluxo:

```
ALERTA DISPAROU
    │
    ▼
1. Qual agente? ──► Dashboard → Agent Health
    │
    ▼
2. O que mudou? ──► Deploy recente? Mudança de modelo? Pico de tráfego?
    │
    ▼
3. Olhe o audit trail ──► grep pelo customer_id ou session_id
    │
    ▼
4. Leia os artefatos ──► customer.json, draft.json, evaluation.json
    │
    ▼
5. Reproduza ──► Replay da conversa com os mesmos inputs
    │
    ▼
6. Corrija ──► Ajuste prompt, rubrica, ou configuração
    │
    ▼
7. Verifique ──► O mesmo cenário agora passa?
```

### Sintoma 1: "Recomendações estão piores que o normal"

**Diagnóstico diferencial:**

| Causa provável | Como verificar | Solução |
|---|---|---|
| **Modelo foi trocado** | Verificar changelog de deploy | Reverter modelo ou ajustar prompts |
| **Catálogo desatualizado** | `catalog.json` tem produtos indisponíveis? | Forçar sync com Inventory System |
| **Rubric descalibrada** | Evaluator está aprovando tudo? (>99% approval) | Aumentar threshold ou adicionar dimensões |
| **Prompt injection por cliente** | Mensagens do cliente contêm instruções? | Reforçar system prompt |
| **Contexto muito grande** | Conversas >4h estão degradando? | Ajustar compaction agressividade |

### Sintoma 2: "Cliente recebeu duas confirmações de pedido"

**Causa mais comum:** Race condition entre Order Agent e Recovery Agent.

**Como diagnosticar:**
```bash
# Olhe o audit trail deste cliente
grep "ORD-2026-XXXX" audit.jsonl

# Você deve ver ALGO como:
# {"ev":"agent_called","agent":"Order"}
# {"ev":"agent_called","agent":"Recovery"}  ← SE isto existe, é race condition
```

**Solução:**
1. Verifique se `order.lock.json` está sendo adquirido antes de criar pedido
2. Verifique se Recovery Agent verifica `order.lock.json` antes de agir
3. Adicione TTL ao lock (se lock existe há >30s, algo está errado)

### Sintoma 3: "KODA não responde — cliente esperando"

**Diagnóstico rápido:**

```bash
# 1. Health check
curl https://koda.api.com/health

# 2. Conversas ativas
SELECT COUNT(*) FROM active_sessions WHERE status = 'awaiting_agent';

# 3. Último evento do cliente
grep "wa_5511987654321" audit.jsonl | tail -1

# 4. Lock contention?
ls -la /shared/locks/ | wc -l  # Muitos locks = contenção
```

**Causas comuns:**

| Sintoma adicional | Causa | Solução |
|---|---|---|
| Health check OK, mas sem resposta | Agent em loop de retry | Verificar circuit breaker; forçar reset |
| Locks acumulados | Agente morreu com lock adquirido | Implementar TTL nos locks |
| WhatsApp API retornando 429 | Rate limit | Reduzir envio, enfileirar mensagens |
| Claude API timeout | Modelo sobrecarregado | Fallback para modelo alternativo |

### Sintoma 4: "Pedido foi cobrado mas não foi entregue"

**Este é o cenário mais grave.** Significa que Payment passou mas Fulfillment falhou.

**Diagnóstico:**
```bash
# 1. O pagamento foi confirmado?
grep "ORD-XXXX" audit.jsonl | grep "payment"

# 2. O fulfillment foi acionado?
grep "ORD-XXXX" audit.jsonl | grep "fulfillment"

# 3. Se fulfillment NÃO foi acionado, veja por quê:
# - Order foi marcado como paid?
# - Recovery Manager tentou recuperar?
```

**Solução:**
1. Se pagamento OK mas fulfillment não iniciou: execute Fulfillment Agent manualmente com `order.json`
2. Se fulfillment iniciou mas falhou: veja `fulfillment.json` para diagnóstico
3. Notifique o cliente proativamente: "Detectamos um atraso no seu pedido. Já estamos corrigindo."

---

## 💻 Seção 18: Exemplos de Código — Implementação de Referência

### Orchestrator: O Maestro do KODA

```python
# orchestrator.py — Implementação de referência do Orchestrator do KODA
import asyncio
import json
import time
from pathlib import Path

class KodaOrchestrator:
    """
    Orquestra o ciclo de vida de uma conversa KODA.
    Responsável por: roteamento, sequenciamento, recovery.
    """

    def __init__(self, state_dir="/shared/state"):
        self.state_dir = Path(state_dir)
        self.agents = {}  # Será populado com instâncias dos agentes
        self.active_sessions = {}

    async def handle_message(self, phone_number_id, message_text):
        """Ponto de entrada: mensagem chegou do WhatsApp."""
        customer_id = f"wa_{phone_number_id}"
        session_id = self._get_or_create_session(customer_id)

        try:
            # 1. Carregar estado (ou criar novo)
            state = await self._load_state(customer_id)

            # 2. Planner decide próximos passos
            plan = await self.agents["planner"].plan(state, message_text)

            # 3. Executar cada sprint do plano
            for sprint in plan["sprints"]:
                result = await self._execute_sprint(sprint, state)
                if result["status"] == "error":
                    # Recovery: tentar recuperar ou escalar
                    recovery = await self.agents["recovery"].recover(
                        state, sprint, result["error"]
                    )
                    if recovery["action"] == "retry":
                        result = await self._execute_sprint(sprint, state)
                    elif recovery["action"] == "escalate":
                        await self._escalate_to_human(customer_id, sprint, result["error"])
                        return

            # 4. Enviar resposta final ao cliente
            await self._send_response(customer_id, result)

            # 5. Registrar no audit trail
            self._audit(session_id, "session_completed", result)

        except Exception as e:
            self._audit(session_id, "session_error", {"error": str(e)})
            await self._handle_unexpected_error(customer_id, e)

    async def _execute_sprint(self, sprint, state):
        """Executa um sprint: chama agente → avalia → decide."""
        agent_name = sprint["agent"]
        agent = self.agents[agent_name]

        # Adquirir lock se necessário
        lock = None
        if sprint.get("requires_lock"):
            lock = await self._acquire_lock(state["customer_id"], agent_name)

        try:
            # Executar agente
            output = await agent.execute(state, sprint["contract"])
            self._write_artifact(state["customer_id"], sprint["output_file"], output)

            # Avaliar output
            evaluation = await self.agents["evaluator"].evaluate(
                output, state, sprint["rubric"]
            )
            self._write_artifact(state["customer_id"], "evaluation.json", evaluation)

            if evaluation["verdict"] == "REJECTED" and sprint.get("retry", 0) < 3:
                # Feedback loop: devolver ao agente com feedback
                feedback = evaluation.get("issues", [])
                sprint["retry"] = sprint.get("retry", 0) + 1
                state["feedback"] = feedback
                return await self._execute_sprint(sprint, state)

            return {"status": "ok", "output": output, "evaluation": evaluation}

        finally:
            if lock:
                await self._release_lock(lock)


### Por que modelos diferentes para agentes diferentes?

Cada agente no KODA tem necessidades diferentes. Usar o mesmo modelo para tudo seria como usar um caminhão para ir à padaria — funciona, mas é caro e ineficiente.

| Agente | Modelo | Temperatura | Max Tokens | Custo/chamada | Por que este modelo? |
|---|---|---|---|---|---|
| **Discovery** | Claude Opus 4.6 | 0.3 | 1500 | ~$0.015 | Precisão na extração de perfil. Erro aqui contamina todo o pipeline. |
| **Catalog** | Claude Sonnet 4.6 | 0.1 | 800 | ~$0.003 | Tarefa estruturada (filtrar JSON). Não precisa de criatividade. |
| **Generator** | Claude Opus 4.6 | 0.8 | 2000 | ~$0.020 | Criatividade para explorar opções e gerar explicações naturais. Maior custo, maior valor. |
| **Evaluator** | Claude Sonnet 4.6 | 0.2 | 1000 | ~$0.004 | Rigor na avaliação. Temperatura baixa = scores consistentes entre chamadas. |
| **Planner** | Claude Sonnet 4.6 | 0.3 | 800 | ~$0.003 | Decisões de roteamento são estruturadas. Sonnet é suficiente. |
| **Order** | Claude Sonnet 4.6 | 0.1 | 1200 | ~$0.004 | Cálculos precisos. Temperatura mínima para zero variação. |
| **Payment** | (sem LLM) | — | — | $0 | Lógica determinística. Não usa Claude. Só chama Payment Gateway API. |
| **Fulfillment** | Claude Sonnet 4.6 | 0.2 | 800 | ~$0.003 | Coordenação de armazém/rota/entregador. Tarefa estruturada. |
| **Recovery** | Claude Sonnet 4.6 | 0.3 | 600 | ~$0.002 | Diagnóstico de falha. Só chamado em incidentes (~1% das conversas). |

### Mix de Custo por Conversa Típica

```
┌─────────────────────────────────────────────────────────────────────┐
│                    CUSTO POR CONVERSA (2 horas, ~15 interações)      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Agente        │ Chamadas │ Tokens/cham │ Total Tokens │ Custo      │
│  ──────────────┼──────────┼─────────────┼──────────────┼──────────  │
│  Discovery     │    2     │    1500     │     3000     │ $0.030     │
│  Catalog       │    2     │     800     │     1600     │ $0.006     │
│  Generator     │    5     │    2000     │    10000     │ $0.100     │
│  Evaluator     │    5     │    1000     │     5000     │ $0.020     │
│  Planner       │    2     │     800     │     1600     │ $0.006     │
│  Order         │    1     │    1200     │     1200     │ $0.004     │
│  Payment       │    0     │       0     │        0     │ $0.000     │
│  Fulfillment   │    1     │     800     │      800     │ $0.003     │
│  Recovery      │    0*    │     600     │        0*    │ $0.000*    │
│  ──────────────┼──────────┼─────────────┼──────────────┼──────────  │
│  TOTAL         │   18     │             │    23200     │ $0.169     │
│                                                                      │
│  *Recovery só é chamado em ~1% das conversas (incidentes)           │
│                                                                      │
│  Custo LLM por conversa:  ~$0.17 USD (~R$ 0,85)                     │
│  Venda média por conversa: ~R$ 222,37                               │
│  Margem média:             ~R$ 50,00                                │
│  ROI do LLM:               58x                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### Estratégia de Fallback de Modelos

Se o modelo primário falhar, o KODA tem uma cadeia de fallback:

| Agente | Primário | Fallback 1 | Fallback 2 | Impacto no cliente |
|---|---|---|---|---|
| **Generator** | Claude Opus 4.6 | Claude Sonnet 4.6 | Claude Haiku 4.6 | Menos criativo, mas funcional |
| **Evaluator** | Claude Sonnet 4.6 | Claude Haiku 4.6 | (regras determinísticas) | Scores menos precisos, threshold sobe para 8.0 |
| **Discovery** | Claude Opus 4.6 | Claude Sonnet 4.6 | (template de perguntas) | Extração menos precisa, faz mais perguntas |
| **Demais agentes** | Claude Sonnet 4.6 | Claude Haiku 4.6 | (lógica determinística) | Leve degradação de qualidade |

**Regra de fallback:** Se o primário falhar 2x consecutivas, migra para fallback. Se fallback também falhar, escala para humano (suporte).

---


> *"Arquitetura não é sobre desenhar o sistema perfeito. É sobre desenhar um sistema que você consegue entender, debugar, evoluir e — quando necessário — simplificar."*

O KODA de março de 2026 era um agente único com um prompt gigante. Funcionava para conversas curtas. Quebrava em conversas longas.

O KODA de maio de 2026 é uma operação comercial com 8 agentes, pipeline de vendas, persistência, coordenação e recovery. Funciona para conversas de 4 horas. Sobrevive a restarts. Não perde alergias. Não cobra duas vezes.

Mas esta arquitetura não é o destino final. É uma plataforma.

Conforme os modelos melhoram, componentes serão removidos. Conforme o KODA escala, file-based coordination evoluirá para distributed coordination. Conforme novas features são adicionadas, novos agentes serão criados — ou existentes serão estendidos.

A arquitetura que você aprendeu aqui é o ponto de partida para pensar sobre o KODA como um **sistema**, não como um **prompt**.

Você agora consegue olhar para o quadro branco do Fernando e ver não um diagrama — mas uma operação viva.

Isso é Nível 4.

---

**Pronto para `02-customer-journey-flows.md`? A jornada do cliente te espera.**

---

*Escrito com base na arquitetura real do KODA em produção, Maio 2026.*  
*Este documento é a fundação de todo o Nível 4. Todos os módulos subsequentes referenciam esta arquitetura.*

---

## 📝 Nota Final: O Que Este Documento Representa

Este documento não é apenas uma descrição de arquitetura. É o **registro canônico de como o KODA funciona em Maio de 2026**.

Ele existe para que:

1. **Novos membros da equipe** possam entender o sistema completo em 90 minutos, sem depender de conhecimento tribal
2. **Decisões de design** tenham um ponto de referência — "por que fizemos assim?" está respondido aqui
3. **Mudanças futuras** possam ser avaliadas contra a arquitetura atual — "esta mudança respeita os princípios arquiteturais?"
4. **Incidentes** possam ser diagnosticados rapidamente — "qual componente falhou?" está mapeado aqui
5. **O KODA sobreviva aos seus criadores** — se Fernando e o time original saírem, o conhecimento não sai com eles

Este documento deve ser atualizado sempre que a arquitetura mudar significativamente. A versão atual reflete o estado em Maio de 2026. Se você está lendo isso em Setembro de 2026 e algo parece desatualizado, **atualize o documento**.

A arquitetura evolui. A documentação também.

---

## 🎬 Reflexão Final

> *"Arquitetura não é sobre desenhar o sistema perfeito. É sobre desenhar um sistema que você consegue entender, debugar, evoluir e — quando necessário — simplificar."*

O KODA de março de 2026 era um agente único com um prompt gigante. Funcionava para conversas curtas. Quebrava em conversas longas.

O KODA de maio de 2026 é uma operação comercial com 8 agentes, pipeline de vendas, persistência, coordenação e recovery. Funciona para conversas de 4 horas. Sobrevive a restarts. Não perde alergias. Não cobra duas vezes.

Mas esta arquitetura não é o destino final. É uma plataforma.

Conforme os modelos melhoram, componentes serão removidos. Conforme o KODA escala, file-based coordination evoluirá para distributed coordination. Conforme novas features são adicionadas, novos agentes serão criados — ou existentes serão estendidos.

A arquitetura que você aprendeu aqui é o ponto de partida para pensar sobre o KODA como um **sistema**, não como um **prompt**.

Você agora consegue olhar para o quadro branco do Fernando e ver não um diagrama — mas uma operação viva.

Isso é Nível 4.

---

## 📋 Metadata

| Campo | Valor |
|---|---|
| **Arquivo** | 01-koda-architecture.md |
| **Nível** | 4 — KODA-Específico |
| **Tempo** | 90 minutos |
| **Status** | ✅ Completo |
| **Próximo** | 02-customer-journey-flows.md |
| **Referenciado por** | Todos os módulos do Nível 4 |
| **Atualizado** | Maio 2026 |
