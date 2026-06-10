---
title: "Exercício 2: Implement Sprint Contracts com Generator/Evaluator"
type: curriculum-exercise
nivel: 2
aliases: []
tags: [curriculo-conteudo, nivel-2, exercicio, generator-evaluator-pattern, sprint-contract, pipeline-orchestration, retry-loop, order-checkout, double-discount-prevention, catalog-validation, python, dataclass]
last_updated: 2026-06-10
---
# 🏗️ Exercício 2: Implement Sprint Contracts com Generator/Evaluator
## Nível 2 - Padrões Práticos

**Tempo Estimado:** 60-90 minutos  
**Dificuldade:** ⭐⭐⭐ (Avançado)  
**Pré-requisito:** Ter lido `02-sprint-contracts.md` + completado Exercício 1  
**Objetivo:** Implementar um Sprint Contract completo em Python e validá-lo com o padrão Generator/Evaluator

---

## 📖 Prólogo: O Checkout Que Deu Errado

### Segunda-feira, 16h45. Um pedido que parecia simples.

```
CLIENTE: "KODA, quero finalizar minha compra!"
KODA: "Claro! Você tem no carrinho:
       - Whey Vegano 100% (R$ 95,00)
       - BCAA Premium (R$ 65,00)
       - Creatina Monohidratada (R$ 45,00)
       Total: R$ 205,00"

CLIENTE: "Perfeito! Tenho cupom PRIMEIRA20 e sou membro do clube."

KODA: [Processando...]
      "Ok, aplicando cupom 20%... R$ 205 - R$ 41 = R$ 164
       Desconto de clube: 10%... R$ 164 - R$ 16,40 = R$ 147,60
       Frete: Grátis (acima de R$ 100)
       Total final: R$ 147,60"

CLIENTE: "Ótimo! Pode confirmar."

KODA: "Pedido #7821 confirmado! Total: R$ 147,60"
```

**Parece perfeito, certo?**

Mas o que o cliente não viu:

```
❌ Cupom PRIMEIRA20 era para PRIMEIRA COMPRA — e o cliente já comprou antes
❌ Desconto de clube NÃO é cumulativo com cupons promocionais
❌ O BCAA Premium estava com preço de ontem (hoje subiu para R$ 72)
❌ KODA não validou o estoque da Creatina (tinha só 1 unidade reservada para outro cliente)
```

**Resultado real:** Pedido cancelado 3 horas depois. Cliente furioso. Reembolso processado. Confiança perdida.

### O Que Faltou?

Faltou um **Sprint Contract para o Checkout** — um acordo explícito entre o Generator (que processa o pedido) e o Evaluator (que valida cada passo) sobre o que significa "pedido pronto para confirmar".

Sem contrato, o Generator fez o que achou melhor. O Evaluator nunca foi consultado porque... não existia.

**Sua missão neste exercício:** Construir esse contrato. Implementá-lo em Python. E validá-lo com o padrão Generator/Evaluator.

---

## 🎯 O Cenário: Order Checkout no KODA

### Contexto de Negócio

O **Order Checkout Sprint** é o momento mais crítico de qualquer conversa no KODA. É quando o cliente decide comprar e o sistema precisa:

1. Validar que todos os produtos ainda estão disponíveis
2. Aplicar descontos corretamente (sem double-dipping)
3. Verificar regras de negócio (cupons, clube, frete)
4. Calcular o total final com precisão
5. Confirmar o pedido somente quando tudo estiver correto

### Atores

| Ator | Responsabilidade |
|------|-----------------|
| **Generator (OrderProcessor)** | Recebe o carrinho, aplica descontos, calcula totais, gera o pedido |
| **Evaluator (OrderValidator)** | Valida cada passo contra o contrato, aprova ou rejeita |
| **Cliente** | Fornece cupons, confirma dados, espera transparência |

### Dados de Entrada

O Generator recebe do contexto da conversa:

```json
{
  "customer_id": "wa_5511987654321",
  "customer_name": "Ana Oliveira",
  "customer_tier": "club_member",
  "first_purchase": false,
  "cart": {
    "items": [
      {"sku": "WHEY-VEGAN-001", "name": "Whey Vegano 100%", "qty": 1, "unit_price": 95.00},
      {"sku": "BCAA-PREMIUM-001", "name": "BCAA Premium", "qty": 1, "unit_price": 65.00},
      {"sku": "CREATINE-MONO-001", "name": "Creatina Monohidratada", "qty": 1, "unit_price": 45.00}
    ]
  },
  "promo_code": "PRIMEIRA20",
  "shipping_zip": "01310-000"
}
```

---

## 📋 Requisitos

### Requisitos Funcionais

1. **RF1 - Validação de Estoque:** Todo produto no carrinho deve ter `stock_qty >= qty` no momento do checkout
2. **RF2 - Validação de Preço:** O preço unitário usado deve ser o preço atual do catálogo (não o preço de quando o produto foi adicionado ao carrinho)
3. **RF3 - Aplicação de Cupom:** Cupons devem ser validados contra a base de promoções ativas. Cupons de primeira compra (`first_purchase_only`) não podem ser usados por clientes recorrentes
4. **RF4 - Desconto de Clube:** Membros do clube recebem 10% de desconto, mas este desconto NÃO é cumulativo com cupons promocionais. O sistema deve aplicar o MAIOR desconto, não ambos
5. **RF5 - Frete Grátis:** Pedidos acima de R$ 100 têm frete grátis. Abaixo disso, frete fixo de R$ 15
6. **RF6 - Total Final:** O total deve ser calculado como `subtotal - melhor_desconto + frete` e nunca pode ser negativo

### Requisitos Técnicos

1. **RT1 - Contrato como Código:** O Sprint Contract deve ser implementado como classes Python com validações explícitas (use dataclasses, Pydantic, ou dicionários tipados)
2. **RT2 - Separação Generator/Evaluator:** Generator e Evaluator devem ser funções ou classes separadas, comunicando-se via um dicionário de estado compartilhado
3. **RT3 - Feedback Estruturado:** Quando o Evaluator rejeita, deve retornar um dicionário de `issues` com `severity`, `field` e `message`
4. **RT4 - Máximo de 3 Tentativas:** Se o Generator falhar 3 vezes, o sistema deve escalar para revisão humana
5. **RT5 - Código Mínimo:** A implementação completa (Generator + Evaluator + Orquestrador) deve ter no mínimo 200 linhas de Python

---

## 📝 Sua Tarefa

Você vai implementar o **Order Checkout Sprint** em 4 partes.

---

### Parte 1: Especificar o Sprint Contract (20 min)

Antes de escrever código, defina o contrato no formato visual. Use o template que você aprendeu no Exercício 1:

```
╔═══════════════════════════════════════════════════════╗
║     SPRINT CONTRACT: Order Checkout                  ║
╠═══════════════════════════════════════════════════════╣
║ GERADOR: OrderProcessor (Generator)                  ║
║ AVALIADOR: OrderValidator (Evaluator)                ║
║ DURAÇÃO: 5 minutos máximo                            ║
╠═══════════════════════════════════════════════════════╣
║ 📥 INPUT SPECIFICATION                               ║
║ • [Liste pelo menos 5 campos de entrada]             ║
║ • [Inclua tipos e constraints]                       ║
╠═══════════════════════════════════════════════════════╣
║ ✅ SUCCESS CRITERIA                                  ║
║ • [Pelo menos 6 critérios testáveis]                 ║
║ • [Use operadores: ==, >, <, !=, in, not in]         ║
╠═══════════════════════════════════════════════════════╣
║ ⚠️ FAILURE HANDLING                                  ║
║ • [Pelo menos 5 cenários de falha]                   ║
║ • [Cada um com ação específica]                      ║
╚═══════════════════════════════════════════════════════╝
```

**Dica:** Consulte `02-sprint-contracts.md` (Seção "Os 3 Pilares") para referência.

---

### Parte 2: Implementar o Generator — OrderProcessor (30 min)

Implemente em Python o Generator que processa o pedido. Ele deve:

1. Receber os dados do carrinho e do cliente
2. Consultar o catálogo para preços atualizados
3. Validar o cupom contra a base de promoções
4. Aplicar a regra de desconto (maior entre cupom e clube)
5. Calcular frete
6. Retornar um dicionário com o pedido processado

Use este esqueleto como ponto de partida:

```python
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from enum import Enum
import json

# ============================================================
# DATA MODELS
# ============================================================

class Severity(Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

@dataclass
class CartItem:
    sku: str
    name: str
    qty: int
    unit_price: float

@dataclass
class CustomerContext:
    customer_id: str
    customer_name: str
    customer_tier: str          # "club_member" ou "regular"
    first_purchase: bool
    promo_code: Optional[str] = None
    shipping_zip: str = ""

@dataclass
class PromoRecord:
    code: str
    discount_percent: float
    first_purchase_only: bool
    active: bool
    min_purchase: float = 0.0

@dataclass
class CatalogRecord:
    sku: str
    name: str
    current_price: float
    stock_qty: int

# ============================================================
# MOCK DATABASES (simulando APIs reais do KODA)
# ============================================================

CATALOG_DB: Dict[str, CatalogRecord] = {
    "WHEY-VEGAN-001": CatalogRecord(
        sku="WHEY-VEGAN-001",
        name="Whey Vegano 100%",
        current_price=95.00,
        stock_qty=47
    ),
    "BCAA-PREMIUM-001": CatalogRecord(
        sku="BCAA-PREMIUM-001",
        name="BCAA Premium",
        current_price=72.00,  # Preço subiu! Era 65.00
        stock_qty=12
    ),
    "CREATINE-MONO-001": CatalogRecord(
        sku="CREATINE-MONO-001",
        name="Creatina Monohidratada",
        current_price=45.00,
        stock_qty=0  # Sem estoque!
    ),
}

PROMO_DB: Dict[str, PromoRecord] = {
    "PRIMEIRA20": PromoRecord(
        code="PRIMEIRA20",
        discount_percent=20.0,
        first_purchase_only=True,
        active=True,
        min_purchase=50.00
    ),
    "CLUBE10": PromoRecord(
        code="CLUBE10",
        discount_percent=10.0,
        first_purchase_only=False,
        active=True,
    ),
}

# ============================================================
# GENERATOR: OrderProcessor
# ============================================================

# TODO: Implemente a função abaixo
def generator_process_order(
    customer: CustomerContext,
    cart_items: List[CartItem],
    catalog: Dict[str, CatalogRecord],
    promos: Dict[str, PromoRecord]
) -> Dict[str, Any]:
    """
    Processa um pedido de checkout e retorna o pedido estruturado.

    Deve implementar:
    1. Validação de estoque para cada item
    2. Atualização de preços pelo catálogo
    3. Validação de cupom (first_purchase_only?)
    4. Regra de desconto: aplicar o MAIOR entre cupom e clube (não cumulativo)
    5. Cálculo de frete (grátis acima de R$ 100)
    6. Cálculo do total final

    Returns:
        Dict com as chaves:
        - "order_id": str
        - "items": lista de itens processados (com preço atualizado)
        - "subtotal": float
        - "discount_applied": dict com "type", "percent", "amount"
        - "shipping": float
        - "total": float
        - "warnings": lista de strings
        - "status": "draft"
    """
    # SEU CÓDIGO AQUI
    pass


# ============================================================
# TESTE RÁPIDO DO GENERATOR
# ============================================================

if __name__ == "__main__":
    # Cenário: Ana Oliveira, membro do clube, NÃO é primeira compra
    customer = CustomerContext(
        customer_id="wa_5511987654321",
        customer_name="Ana Oliveira",
        customer_tier="club_member",
        first_purchase=False,
        promo_code="PRIMEIRA20",
        shipping_zip="01310-000"
    )

    cart = [
        CartItem(sku="WHEY-VEGAN-001", name="Whey Vegano 100%", qty=1, unit_price=95.00),
        CartItem(sku="BCAA-PREMIUM-001", name="BCAA Premium", qty=1, unit_price=65.00),
        CartItem(sku="CREATINE-MONO-001", name="Creatina Monohidratada", qty=1, unit_price=45.00),
    ]

    result = generator_process_order(customer, cart, CATALOG_DB, PROMO_DB)
    print(json.dumps(result, indent=2, ensure_ascii=False))
```

---

### Parte 3: Implementar o Evaluator — OrderValidator (25 min)

Implemente o Evaluator que valida o pedido gerado contra o Sprint Contract. Ele deve:

1. Receber o dicionário de saída do Generator
2. Validar cada critério de sucesso definido no contrato (Parte 1)
3. Retornar `APPROVED` ou `REJECTED` com feedback estruturado

```python
# ============================================================
# EVALUATOR: OrderValidator
# ============================================================

# TODO: Implemente a função abaixo
def evaluator_validate_order(
    order: Dict[str, Any],
    customer: CustomerContext,
    catalog: Dict[str, CatalogRecord],
    contract_criteria: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Valida um pedido contra o Sprint Contract.

    Para cada critério no contrato, verifica se o pedido atende.
    Critérios que falham são adicionados à lista de "issues".

    Args:
        order: saída do generator_process_order()
        customer: contexto do cliente (para validações cruzadas)
        catalog: catálogo atual (para validação de preço/estoque)
        contract_criteria: lista de critérios do contrato,
            cada um com {"name", "check", "severity"}

    Returns:
        Dict com:
        - "verdict": "APPROVED" | "REJECTED"
        - "score": float (0-10)
        - "checks": lista de resultados por critério
        - "issues": lista de problemas encontrados
        - "overall_score": float
        - "approval_threshold": float
    """
    # SEU CÓDIGO AQUI
    pass


# ============================================================
# CONTRACT CRITERIA (referência para o Evaluator)
# ============================================================

CHECKOUT_CONTRACT_CRITERIA = [
    {
        "name": "all_items_in_stock",
        "description": "Todos os itens devem estar em estoque (stock_qty >= qty)",
        "severity": Severity.CRITICAL.value,
    },
    {
        "name": "prices_match_catalog",
        "description": "Preços dos itens devem corresponder ao catálogo atual",
        "severity": Severity.HIGH.value,
    },
    {
        "name": "promo_code_valid",
        "description": "Cupom deve existir, estar ativo, e ser aplicável ao cliente",
        "severity": Severity.CRITICAL.value,
    },
    {
        "name": "no_double_discount",
        "description": "Desconto de clube e cupom NÃO podem ser cumulativos",
        "severity": Severity.CRITICAL.value,
    },
    {
        "name": "best_discount_applied",
        "description": "O maior desconto disponível deve ser aplicado",
        "severity": Severity.HIGH.value,
    },
    {
        "name": "shipping_correct",
        "description": "Frete grátis para pedidos >= R$ 100, senão R$ 15",
        "severity": Severity.MEDIUM.value,
    },
    {
        "name": "total_not_negative",
        "description": "Total final não pode ser negativo",
        "severity": Severity.CRITICAL.value,
    },
    {
        "name": "total_matches_math",
        "description": "Total = subtotal - desconto + frete",
        "severity": Severity.CRITICAL.value,
    },
    {
        "name": "order_not_empty",
        "description": "O pedido deve ter pelo menos 1 item",
        "severity": Severity.CRITICAL.value,
    },
]
```

---

### Parte 4: Pipeline Generator/Evaluator (15 min)

Implemente o orquestrador que conecta Generator e Evaluator, implementando o loop de feedback com no máximo 3 tentativas:

```python
# ============================================================
# ORCHESTRATOR: Pipeline Generator → Evaluator
# ============================================================

MAX_RETRIES = 3
APPROVAL_THRESHOLD = 7.0

# TODO: Implemente a função abaixo
def checkout_pipeline(
    customer: CustomerContext,
    cart_items: List[CartItem],
    catalog: Dict[str, CatalogRecord],
    promos: Dict[str, PromoRecord],
    criteria: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Pipeline completo do Checkout: Generator → Evaluator → Retry/Final.

    Fluxo:
    1. Generator processa o pedido
    2. Evaluator valida contra os critérios
    3. Se APPROVED → retorna o pedido
    4. Se REJECTED → extrai feedback, alimenta o Generator, tenta novamente
    5. Se 3 tentativas falharem → escalar para humano

    Returns:
        Dict com:
        - "final_order": pedido aprovado (ou None)
        - "status": "approved" | "rejected" | "escalated"
        - "attempts": número de tentativas
        - "history": lista de resultados de cada tentativa
    """
    # SEU CÓDIGO AQUI
    pass


# ============================================================
# TESTE COMPLETO
# ============================================================

if __name__ == "__main__":
    customer = CustomerContext(
        customer_id="wa_5511987654321",
        customer_name="Ana Oliveira",
        customer_tier="club_member",
        first_purchase=False,
        promo_code="PRIMEIRA20",
        shipping_zip="01310-000"
    )

    cart = [
        CartItem(sku="WHEY-VEGAN-001", name="Whey Vegano 100%", qty=1, unit_price=95.00),
        CartItem(sku="BCAA-PREMIUM-001", name="BCAA Premium", qty=1, unit_price=65.00),
        CartItem(sku="CREATINE-MONO-001", name="Creatina Monohidratada", qty=1, unit_price=45.00),
    ]

    result = checkout_pipeline(
        customer, cart, CATALOG_DB, PROMO_DB, CHECKOUT_CONTRACT_CRITERIA
    )

    print("\n" + "=" * 60)
    print("RESULTADO FINAL DO CHECKOUT")
    print("=" * 60)
    print(json.dumps(result, indent=2, ensure_ascii=False))
```

---

## ✅ Validação: Critérios de Aceitação

Seu código será considerado **APROVADO** quando passar em todos estes cenários:

### Cenário 1: Pedido Válido (Deve Passar)

```python
def test_valid_order_approved():
    """Cliente regular, sem cupom, 2 itens em estoque, total > 100."""
    customer = CustomerContext(
        customer_id="wa_test",
        customer_name="Teste",
        customer_tier="regular",
        first_purchase=True,
        promo_code=None,
        shipping_zip="01310-000"
    )
    cart = [
        CartItem(sku="WHEY-VEGAN-001", name="Whey Vegano", qty=1, unit_price=95.00),
        CartItem(sku="BCAA-PREMIUM-001", name="BCAA Premium", qty=1, unit_price=72.00),
    ]

    result = checkout_pipeline(customer, cart, CATALOG_DB, PROMO_DB, CHECKOUT_CONTRACT_CRITERIA)

    assert result["status"] == "approved", f"Esperado 'approved', obtido '{result['status']}'"
    order = result["final_order"]
    assert order["subtotal"] == 167.00
    assert order["shipping"] == 0.0  # Frete grátis (> 100)
    assert order["total"] == 167.00
    print("✅ Cenário 1 passou: Pedido válido aprovado")
```

### Cenário 2: Cupom Inválido (Deve Rejeitar e Corrigir)

```python
def test_invalid_promo_rejected_then_corrected():
    """Cliente NÃO é primeira compra, mas usa cupom first_purchase_only.
       Deve rejeitar, remover cupom, e aprovar com desconto de clube."""
    customer = CustomerContext(
        customer_id="wa_test",
        customer_name="Teste",
        customer_tier="club_member",
        first_purchase=False,  # ← NÃO é primeira compra
        promo_code="PRIMEIRA20",  # ← Cupom exige primeira compra
        shipping_zip="01310-000"
    )
    cart = [
        CartItem(sku="WHEY-VEGAN-001", name="Whey Vegano", qty=1, unit_price=95.00),
    ]

    result = checkout_pipeline(customer, cart, CATALOG_DB, PROMO_DB, CHECKOUT_CONTRACT_CRITERIA)

    assert result["status"] == "approved", f"Esperado 'approved', obtido '{result['status']}'"
    order = result["final_order"]
    # Deve ter aplicado desconto de clube (10%), não o cupom
    assert order["discount_applied"]["type"] == "club_member"
    assert order["total"] == 100.50  # 95 - 9.50 (clube) + 15 (frete, subtotal < 100)
    # Deve ter warning sobre cupom rejeitado
    assert any("PRIMEIRA20" in w for w in order.get("warnings", []))
    print("✅ Cenário 2 passou: Cupom inválido rejeitado, clube aplicado")
```

### Cenário 3: Produto Sem Estoque (Deve Rejeitar)

```python
def test_out_of_stock_rejected():
    """Creatina está sem estoque (stock_qty=0). Deve ser rejeitado."""
    customer = CustomerContext(
        customer_id="wa_test",
        customer_name="Teste",
        customer_tier="regular",
        first_purchase=True,
        promo_code=None,
        shipping_zip="01310-000"
    )
    cart = [
        CartItem(sku="CREATINE-MONO-001", name="Creatina", qty=1, unit_price=45.00),
    ]

    result = checkout_pipeline(customer, cart, CATALOG_DB, PROMO_DB, CHECKOUT_CONTRACT_CRITERIA)

    assert result["status"] in ("rejected", "escalated"), \
        f"Esperado 'rejected' ou 'escalated', obtido '{result['status']}'"
    print("✅ Cenário 3 passou: Produto sem estoque rejeitado")
```

### Cenário 4: Double Discount Bloqueado

```python
def test_no_double_discount():
    """Cliente com cupom válido E desconto de clube.
       Deve aplicar APENAS o maior desconto."""
    customer = CustomerContext(
        customer_id="wa_test",
        customer_name="Teste",
        customer_tier="club_member",
        first_purchase=True,  # Pode usar PRIMEIRA20
        promo_code="PRIMEIRA20",  # 20% de desconto
        shipping_zip="01310-000"
    )
    cart = [
        CartItem(sku="WHEY-VEGAN-001", name="Whey Vegano", qty=1, unit_price=95.00),
    ]

    result = checkout_pipeline(customer, cart, CATALOG_DB, PROMO_DB, CHECKOUT_CONTRACT_CRITERIA)

    assert result["status"] == "approved"
    order = result["final_order"]
    # Cupom 20% (19.00) > Clube 10% (9.50) → deve aplicar cupom
    assert order["discount_applied"]["percent"] == 20.0
    # NÃO deve ter dois descontos
    assert order["discount_applied"]["type"] == "promo_code"
    print("✅ Cenário 4 passou: Double discount bloqueado, maior desconto aplicado")
```

---

## 📊 Rubric de Avaliação

| Critério | Peso | Insuficiente (0-3) | Básico (4-6) | Proficiente (7-8) | Excelente (9-10) |
|----------|------|-------------------|-------------|------------------|-----------------|
| **Contract (Parte 1)** | 20% | Contrato vago ou incompleto | Template preenchido mas genérico | Critérios testáveis, falhas cobertas | Contrato preciso, cobre edge cases |
| **Generator (Parte 2)** | 30% | Não implementado ou com erros | Funciona para happy path | Lida com erros, cálculos corretos | Código limpo, warnings úteis, bem comentado |
| **Evaluator (Parte 3)** | 25% | Não implementado | Valida alguns critérios | Valida todos os critérios, feedback claro | Issues estruturadas, severidade correta |
| **Pipeline (Parte 4)** | 15% | Não implementado | Loop básico sem retry | Retry com feedback, max 3 tentativas | Escala para humano, log de tentativas |
| **Testes (Cenários)** | 10% | Nenhum cenário passa | 1-2 cenários passam | 3 cenários passam | Todos os 4 cenários passam |

**Nota final:** Média ponderada. **Aprovação:** ≥ 7.0

---

## 💡 Dicas para Implementação

### Para o Generator

1. **Consulte o catálogo antes de tudo.** O preço que o cliente viu 20 minutos atrás pode estar desatualizado.
2. **Valide o estoque cedo.** Se um item está sem estoque, avise imediatamente — não espere o Evaluator descobrir.
3. **Warnings são seus amigos.** Se o cupom for inválido, não silencie. Adicione um warning e continue com o próximo melhor desconto.
4. **A regra do maior desconto:** Compare `promo_discount_amount` com `club_discount_amount` e aplique o maior. Não some.

### Para o Evaluator

1. **Seja implacável.** Seu trabalho é encontrar erros, não passar tudo.
2. **Feedback específico.** "Cupom inválido" não ajuda. "PRIMEIRA20 exige primeira compra, mas cliente é recorrente" ajuda.
3. **Severidade importa.** `CRITICAL` = bloqueia o pedido. `MEDIUM` = warning mas não bloqueia.
4. **Verifique a matemática.** `total == subtotal - discount_amount + shipping` — sempre.
5. **Valide o OUTPUT do Generator, não o INPUT do cliente.** Se o cliente forneceu um cupom inválido mas o Generator corretamente avisou e aplicou o desconto de clube, isso é um ACERTO do Generator, não um erro. O Evaluator deve verificar se o desconto aplicado faz sentido, não se o cupom original era válido.
6. **Cuidado com pedidos vazios.** Se todos os itens forem removidos (por exemplo, por falta de estoque), o pedido não pode ser aprovado mesmo que todos os outros critérios passem. Adicione uma verificação de `len(items) > 0`.

### Para o Pipeline

1. **Extraia o feedback.** Quando o Evaluator rejeitar, pegue as `issues` e transforme em instruções para o Generator.
2. **Limite as tentativas.** 3 tentativas é o padrão KODA. Na terceira falha, escale.
3. **Registre o histórico.** Cada tentativa deve ser logada para debug futuro (trace reading).

---

## 🎓 Dúvidas Comuns

**P: Preciso usar exatamente as classes fornecidas no esqueleto?**
R: As classes (`CartItem`, `CustomerContext`, etc.) são obrigatórias. Você pode adicionar campos e métodos, mas não remover os existentes.

**P: Posso usar bibliotecas externas como Pydantic?**
R: O exercício foi desenhado para Python puro (stdlib + dataclasses). Se quiser usar Pydantic como desafio extra, fique à vontade — mas o código base usa apenas `dataclasses`.

**P: O que acontece se o cupom e o desconto de clube tiverem o mesmo valor?**
R: Aplique apenas um deles (não importa qual). O importante é não aplicar os dois.

**P: Preciso implementar os testes exatamente como estão?**
R: Os 4 cenários de teste são seu critério de aceitação. Você pode escrevê-los como funções `assert`, como testes `pytest`, ou como scripts de verificação manual. O importante é que todos passem.

**P: Meu Generator pode "trapacear" e já retornar o pedido perfeito na primeira tentativa?**
R: O Generator deve ser honesto — ele processa o pedido com as informações que tem. Se houver problemas (cupom inválido, estoque zerado), ele deve registrá-los como warnings. O Evaluator é quem decide se aprova ou rejeita.

---

## 📁 Estrutura de Entrega

Seu código final deve estar organizado assim:

```
seu-diretorio/
├── sprint_contract_checkout.py    # Generator + Evaluator + Pipeline
├── test_scenarios.py              # Os 4 cenários de teste
└── contract_spec.md               # (Opcional) Contrato em formato visual
```

---

## 🎯 Checklist de Conclusão

Antes de considerar o exercício completo, verifique:

- [ ] Sprint Contract especificado com Input + Criteria + Failure Handling (Parte 1)
- [ ] `generator_process_order()` implementado e funcional (Parte 2)
- [ ] `evaluator_validate_order()` implementado e funcional (Parte 3)
- [ ] `checkout_pipeline()` implementado com retry e feedback (Parte 4)
- [ ] Código total ≥ 200 linhas
- [ ] Cenário 1 passa: Pedido válido aprovado
- [ ] Cenário 2 passa: Cupom inválido rejeitado e corrigido
- [ ] Cenário 3 passa: Produto sem estoque rejeitado
- [ ] Cenário 4 passa: Double discount bloqueado
- [ ] Pedido não fica vazio após remoção de itens (critério `order_not_empty`)

---

## 🚀 Próximo Passo

Depois de completar este exercício:
1. Revise seu código — há algo que poderia ser mais claro?
2. Compare com a solução em `exercises/solutions/exercise-02-solution.md`
3. Vá para **Exercício 3: Handle Failure Scenarios** — simular o que acontece quando o contrato é violado em produção

---

*Exercício 2 | Nível 2 - Padrões Práticos | Sprint Contracts + Generator/Evaluator*

**Hora de construir! O KODA conta com você.** 🏗️
