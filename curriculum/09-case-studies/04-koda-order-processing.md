# Estudo de Caso 4 (KODA): Order Processing

**Nível de Complexidade:** Nível 3  
**Foco:** Sprint Contracts para workflows multi-step  
**Contexto:** Processamento de pedidos com preço de clube e fulfillment same-day

---

## Problema

O processamento de pedidos do KODA é intrinsecamente complexo — 6 etapas sequenciais com dependências críticas entre si:

1. Validar cliente (membro ativo? pagamento cadastrado?)  
2. Verificar inventário (disponível? reservar unidades?)  
3. Calcular preço (desconto de clube \+ bulk \+ promoções)  
4. Aplicar promoções (sem double-discount)  
5. Processar pagamento (cobrar valor correto uma única vez)  
6. Agendar fulfillment (same-day ou agendado)

Com um agente único, \~5% dos pedidos apresentavam erros — preço errado, cobranças duplicadas, endereço incorreto. Cada erro custava tempo de suporte, reembolsos e erosão de confiança do cliente.

---

## Solução: Sprint Contracts Multi-Step

Cada etapa do processamento foi modelada como um sprint independente, com contrato explícito de input/output:

SPRINT 1 — Validar Cliente

Contrato: "Recebe customer\_id → retorna {valid: bool, customer\_data: {...}}"

Generator: Consulta base de clientes

Evaluator: Verifica existência, status ativo, pagamento cadastrado

Teste: 10 IDs reais e fictícios

Critério de aprovação: 100% de precisão (zero falsos positivos)

SPRINT 2 — Verificar Inventário

Contrato: "Recebe \[sku\] → retorna \[{sku, qty\_available, reserved: bool}\]"

Generator: Consulta inventário em tempo real

Evaluator: Verifica quantidades, reserva itens, trata race conditions

Teste: Pedidos concorrentes, cenários de estoque baixo

Critério: Race conditions tratadas, reserva atômica

SPRINT 3 — Calcular Preço

Contrato: "Recebe {customer, items} → retorna {subtotal, discounts, total}"

Generator: Aplica preço de clube, desconto por volume, promoções

Evaluator: Verifica matemática, confere termos da promoção, previne double-discount

Teste: Edge cases (promos expiradas, descontos conflitantes)

Critério: Zero erros de arredondamento, sem double-discount

SPRINT 4 — Processar Pagamento

Contrato: "Recebe {customer, total} → retorna {success: bool, transaction\_id: str}"

Generator: Chama API de pagamento

Evaluator: Verifica transação, checa duplicatas, grava recibo

Teste: Flows reais de pagamento, tratamento de erros

Critério: Idempotência garantida (nunca cobrar duas vezes)

SPRINT 5 — Agendar Fulfillment

Contrato: "Recebe {order\_id, address} → retorna {tracking\_id, eta}"

Generator: Contata sistema de fulfillment, agenda entrega

Evaluator: Verifica endereço válido, ETA razoável, confirmação completa

Teste: Same-day delivery, localizações extremas

Critério: ETA realista, tracking ativo em \< 60 segundos

---

## State Persistence por Pedido

// order-state/order\_12345.json

{

  "customer\_id": "cust\_999",

  "items": \[

    {"sku": "WHEY-001", "qty": 2, "price": 89.90},

    {"sku": "CARBO-001", "qty": 1, "price": 175.00}

  \],

  "validations": {

    "customer\_valid": true,

    "inventory\_reserved": true,

    "price\_calculated": true,

    "payment\_processed": true,

    "fulfillment\_scheduled": true

  },

  "financials": {

    "subtotal": 354.80,

    "club\_discount": \-35.48,

    "promo\_discount": \-17.50,

    "total": 301.82

  },

  "status": "confirmed",

  "created": "2026-05-23T10:30:00Z",

  "tracking\_id": "TRK-789456",

  "eta": "2026-05-23T16:00:00Z"

}

// order-state/order\_audit.log

2026-05-23T10:30:00Z \- Pedido criado (wa\_5511999999999)

2026-05-23T10:30:15Z \- Cliente validado (cust\_999, membro ativo)

2026-05-23T10:30:45Z \- Inventário reservado (WHEY-001 x2, CARBO-001 x1)

2026-05-23T10:31:00Z \- Preço calculado (R$354.80 → R$301.82 com descontos)

2026-05-23T10:31:30Z \- Pagamento processado (txn\_abc123, R$301.82)

2026-05-23T10:32:00Z \- Fulfillment agendado (TRK-789456, ETA 16h00)

O audit log é fundamental: quando um pedido falha, sabe-se exatamente em qual sprint e por quê.

---

## Resultados

ANTES (Agente Único):

├─ Precisão do pedido: 95% (5% com erros)

├─ Breakdown de erros:

│   ├─ Preço errado:       2%

│   ├─ Cobranças duplas:   1%

│   ├─ Endereço errado:    1%

│   └─ Não fulfillado:     1%

├─ Reclamações de clientes: Alto

└─ Taxa de revisão manual: 10%

DEPOIS (Sprint Contracts):

├─ Precisão do pedido: 99.8% (0.2% com erros)

├─ Breakdown de erros:

│   ├─ Preço errado:       0.05%

│   ├─ Cobranças duplas:   0%

│   ├─ Endereço errado:    0.1%

│   └─ Não fulfillado:     0.05%

├─ Reclamações de clientes: Redução de 80%

└─ Taxa de revisão manual: 1%

---

## Padrões-Chave Utilizados

1. **Sprint Contracts:** Critérios de aceitação claros por etapa — sem ambiguidade  
2. **State Persistence:** Rastreamento do pedido através das 6 etapas via JSON  
3. **Multi-Agent:** Cada sprint é um subprocesso isolado  
4. **Evaluation Layer:** Verificação antes de prosseguir para a próxima etapa  
5. **Error Localization:** Falha em sprint específico \= localização imediata do problema

---

## Lições Aprendidas

1. **Contratos previnem erros:** Definições claras de input/output eliminam ambiguidade  
2. **State tracking é crítico:** Sempre saber exatamente em que etapa o pedido está  
3. **Fail early é mais seguro:** Melhor rejeitar na Sprint 1 do que processar dados ruins  
4. **Camadas de validação funcionam:** Cada sprint verifica o trabalho do anterior  
5. **Audit trail é obrigatório:** Recuperação de falhas requer saber o que aconteceu quando

---

---

