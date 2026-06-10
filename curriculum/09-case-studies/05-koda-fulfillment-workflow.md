---
title: "Estudo de Caso 5 (KODA): Fulfillment & Same-Day Delivery"
type: curriculum-case-study
aliases: []
tags: [curriculo-conteudo, caso-de-estudo, entrega-no-mesmo-dia, logistica, coordenacao-multi-agente, estado-persistente, rastreamento-de-entregas, operacao-continua]
relates-to: ["[[docs/canonical/serializable-pause-resume-state|Serializable Pause/Resume State]]", "[[docs/canonical/domain-embedded-workflow-automation-wedge|Domain-Embedded Workflow Automation]]"]
last_updated: 2026-06-10
---
# Estudo de Caso 5 (KODA): Fulfillment & Same-Day Delivery

**Nível de Complexidade:** Nível 4  
**Foco:** State Persistence complexo · Coordenação multi-agente · Operação contínua  
**Contexto:** KODA promete entrega no mesmo dia como diferencial competitivo

---

## Problema

A promessa de same-day delivery é um diferencial crítico do KODA — e também seu desafio operacional mais complexo. Cada entrega requer:

1. Coordenação com o estoque do armazém  
2. Verificação de packing correto  
3. Atribuição de motorista disponível  
4. Otimização de rota em tempo real  
5. Atualizações contínuas ao cliente  
6. Confirmação de entrega com assinatura/foto

Tudo isso deve acontecer em horas, com alta confiabilidade, para dezenas de pedidos simultâneos. Um sistema manual ou de agente único não escala nem garante a consistência necessária.

---

## Solução: 3-Agent System com Persistent State

AGENT 1 — Logistics Planner

├─ Execução: A cada 30 minutos (de 6h às 18h)

├─ Input: Pedidos do dia \+ motoristas disponíveis \+ mapa de tráfego

├─ Processo: Otimização de rotas, balanceamento de carga por motorista

├─ Output: fulfillment\_plan.json (atualizado a cada ciclo)

└─ Custo: $0.15 por execução, 2 minutos de runtime

AGENT 2 — Fulfillment Executor

├─ Execução: Contínua das 6h às 20h (14 horas de runtime)

├─ Input: fulfillment\_plan.json (lido a cada 5 min)

├─ Processo: Coordena armazém, despacha motoristas, envia updates aos clientes

├─ Output: fulfillment\_status.json (atualizado a cada 5 min)

└─ Custo: $1.20/hora → \~$16.80/dia

AGENT 3 — Quality Verifier

├─ Execução: Spot checks durante o dia \+ relatório final às 20h

├─ Input: fulfillment\_status.json \+ feedback de clientes

├─ Processo: Verifica amostra de 10% das entregas, captura anomalias

├─ Output: verification\_report.json

└─ Custo: $0.80/dia (spot checks \+ EOD report)

---

## State Files — Fonte de Verdade Distribuída

// fulfillment-state/fulfillment\_plan.json (atualizado a cada 30 min)

{

  "timestamp": "2026-05-23T08:00:00Z",

  "orders\_to\_fulfill": 47,

  "drivers\_available": 8,

  "routes": \[

    {

      "driver\_id": "drv\_001",

      "driver\_name": "Carlos Silva",

      "orders": \["ord\_123", "ord\_124", "ord\_125"\],

      "estimated\_time\_minutes": 90,

      "stops": 3,

      "zone": "Pinheiros"

    },

    {

      "driver\_id": "drv\_002",

      "orders": \["ord\_126", "ord\_127", "ord\_128", "ord\_129"\],

      "estimated\_time\_minutes": 110,

      "stops": 4,

      "zone": "Vila Madalena"

    }

  \]

}

// fulfillment-state/fulfillment\_status.json (atualizado a cada 5 min — LIVE)

{

  "timestamp": "2026-05-23T14:30:00Z",

  "orders\_progress": {

    "ord\_123": {

      "status": "delivered",

      "delivered\_at": "2026-05-23T11:15:00Z",

      "signature": "verified",

      "customer\_rating": 5

    },

    "ord\_126": {

      "status": "in\_transit",

      "driver": "drv\_002",

      "current\_stop": 2,

      "eta": "2026-05-23T15:00:00Z",

      "customer\_notified": true,

      "last\_update": "2026-05-23T14:25:00Z"

    },

    "ord\_131": {

      "status": "issue\_detected",

      "issue": "Endereço não localizado",

      "agent\_action": "Contacting customer via WhatsApp",

      "resolution\_eta": "2026-05-23T15:30:00Z"

    }

  }

}

// fulfillment-state/verification\_report.json (EOD)

{

  "date": "2026-05-23",

  "orders\_fulfilled": 47,

  "on\_time": 46,

  "late": 1,

  "quality\_score": 98,

  "issues\_detected": \[

    {

      "order\_id": "ord\_999",

      "issue": "Endereço inicial incorreto",

      "resolution": "Corrigido via agente, re-roteado em 8 min",

      "impact": "Atraso de 15 min — still same-day"

    }

  \],

  "learnings\_for\_tomorrow": \[

    "Zona Sul: tráfego pesado às 17h — alocar 15min extra",

    "Motorista drv\_003: rota otimizada renderizou 2 paradas extras"

  \]

}

---

## Fluxo de Coordenação em Tempo Real

06:00 — Planner acorda

        Lê: Pedidos confirmados desde 20h (ontem) \+ novos pedidos da madrugada

        Processa: Otimização de rotas para 8 motoristas, 47 pedidos

        Escreve: fulfillment\_plan.json

        Custo: $0.15, 2 minutos

06:30 — Executor inicia operação

        Lê: fulfillment\_plan.json

        Despacha: Notificações ao armazém, briefing dos motoristas

        Monitora: Status de packing (ETA 08:00 para maioria)

08:00 — Motoristas partem

        Executor atualiza: fulfillment\_status.json a cada 5 min

        Envia: Updates de ETA ao cliente via WhatsApp

        Trata: Anomalias em tempo real (endereço errado, cliente ausente)

10:00 — Verifier faz primeiro spot check

        Amostra: 5 entregas aleatórias (10% do total)

        Verifica: Produto correto? Condição do pacote? Cliente satisfeito?

        Grava: Findings parciais em verification\_report.json

14:00 — Planner re-executa (ciclo de 30 min)

        Re-otimiza: Rotas com base em tráfego atual

        Reatribui: Pedidos de motoristas com atraso para outros disponíveis

20:00 — Executor encerra operação

        Status final: 47/47 pedidos processados

        Verifier: Gera relatório EOD completo

        Planner: Lê learnings para ajustar amanhã

---

## Resultados

ANTES (Manual \+ Agente Único):

├─ Pedidos fulfillados same-day: 85%

├─ Entregas com atraso: 12%

├─ Endereço errado: 3%

├─ Satisfação do cliente: 72%

└─ Trabalho manual: \~30 horas/dia de operação

DEPOIS (3-Agent System \+ State Persistence):

├─ Pedidos fulfillados same-day: 99.5%

├─ Entregas com atraso: 1%

├─ Endereço errado: 0.1%

├─ Satisfação do cliente: 94%

└─ Trabalho manual: \~2 horas/dia (apenas exceções críticas)

---

## Padrões-Chave Utilizados

1. **Planner/Executor/Verifier:** Separação clara de concerns estratégicos, operacionais e de qualidade  
2. **Persistent State:** JSON files como única fonte de verdade — sobrevivem a falhas de agente  
3. **Real-Time Updates:** fulfillment\_status.json atualizado a cada 5 minutos  
4. **Continuous Operation:** Executor roda 14+ horas com suporte a compaction  
5. **Verification Loop:** Spot checks capturam problemas sem verificar tudo (eficiência)  
6. **Learning Loop:** Relatório EOD alimenta otimizações do dia seguinte

---

## Lições Aprendidas

1. **Persistent state é inegociável:** Não se pode perder o rastro de pedidos em trânsito  
2. **Real-time updates importam:** Clientes informados aceitam pequenos atrasos com muito mais tolerância  
3. **Operação contínua é viável:** Agentes com compaction suportam 12+ horas sem degradação  
4. **Spot verification é suficiente:** Verificar 10% captura \>85% dos problemas sistêmicos  
5. **Learning loop amplifica valor:** Cada dia o sistema fica marginalmente melhor  
6. **Custo não cresce linearmente:** 47 pedidos custam apenas 20% mais que 10 — escala favorável

---

## Custo Total de Operação por Dia

Agent 1 (Planner):     24 execuções × $0.15 \= $3.60/dia

Agent 2 (Executor):    14 horas × $1.20    \= $16.80/dia

Agent 3 (Verifier):    Spot checks \+ EOD   \= $0.80/dia

                                             ─────────

TOTAL:                                       $21.20/dia

Com 47 pedidos/dia:    $0.45 por pedido

Margem adicional:      Bem abaixo do custo de um erro (\~$30 em suporte/reembolso)

ROI do sistema:        \~66x (custo de erro prevenido vs. custo do agente)

---

