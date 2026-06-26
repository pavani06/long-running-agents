---
title: "Exercicio: Regulated Data Boundary com Isolamento Arquitetural de Pagamento"
type: exercise
level: "N4"
aliases: ["regulated data boundary", "fronteira de dados regulados", "pci isolation", "isolamento de pagamento KODA", "payment boundary", "data compliance architecture"]
tags: [curriculo-conteudo, nivel-4, exercicio, governanca, security, koda, pci-compliance, data-isolation, payment-processing, architectural-boundary]
duration: "60-75 min"
relates-to: ["[[docs/analysis/2026-06-26-the-best-ai-agents-are-simpler-than-you-think/2026-06-26-the-best-ai-agents-are-simpler-than-you-think-patterns|Sierra Patterns]]", "[[docs/analysis/2026-06-26-the-best-ai-agents-are-simpler-than-you-think/2026-06-26-the-best-ai-agents-are-simpler-than-you-think-classification|Classification]]", "[[docs/canonical/governance-context-injection-pii-prevention|Governance Context Injection — PII Prevention]]", "[[curriculum/04-nivel-4-koda-specific/01-koda-architecture|Arquitetura KODA]]", "[[curriculum/04-nivel-4-koda-specific/02-customer-journey-flows|Customer Journey Flows]]"]
last_updated: 2026-06-26
---
# Exercicio: Regulated Data Boundary com Isolamento Arquitetural de Pagamento
## Nivel 4 — KODA-Especifico

**Tempo Estimado:** 60-75 minutos
**Dificuldade:** Avancado
**Pre-requisito:** Ter lido `01-koda-architecture.md` e `02-customer-journey-flows.md` (Nivel 4)
**Objetivo:** Construir um boundary de isolamento arquitetural que impede que dados de pagamento entrem no contexto do LLM, usando o caso real do KODA processando pagamentos via WhatsApp

---

## Prologo: O Dia em Que o Token de Cartao Vazou pro Modelo

### Quinta-feira, 16h45. Uma conversa normal de WhatsApp.

```
CLIENTE: "KODA, quero comprar Whey Isolado. Meu cartao e 4532-XXXX-XXXX-7890."
KODA:    [Chamando process_payment...]
         [Modelo ve: "cartao 4532-XXXX-XXXX-7890, CVV 123"]
         [Processa pagamento com sucesso]
KODA:    "Pagamento aprovado! Seu pedido chega em 3 dias uteis."
```

Tudo parecia normal. Mas o que aconteceu nos bastidores foi grave: o numero do cartao e CVV do cliente entraram no prompt do LLM. O modelo "viu" dados de pagamento. Nenhum provedor de LLM (OpenAI, Anthropic, DeepSeek) tem certificacao PCI DSS. O dado trafegou por infraestrutura nao certificada.

**O auditor de compliance descobriu 3 meses depois.** Multa de R$ 50 mil. Re-certificacao PCI suspensa por 6 meses. O KODA ficou proibido de processar pagamentos via WhatsApp durante a suspensao.

**O que aconteceu:** O `process_payment` era uma tool do agente — uma funcao Python chamada pelo LLM. O prompt continha: "O cliente quer pagar com cartao 4532-XXXX-XXXX-7890, CVV 123". A tool extraia do prompt e chamava a API de pagamento. O numero do cartao transitou pelo contexto do LLM.

**O que deveria ter acontecido:**

```
┌─────────────────────────────────────────────────────┐
│ LLM CONTEXT (zona nao-PCI)                          │
│ "Cliente quer pagar. Payment token: pay_tok_A7X9"   │
│  → O LLM nunca ve o numero do cartao               │
└──────────────────┬──────────────────────────────────┘
                   │ token de pagamento
                   ▼
┌─────────────────────────────────────────────────────┐
│ REGULATED DATA BOUNDARY (zona PCI)                  │
│ • Extrai numero do cartao do input original         │
│ • Processa pagamento via gateway PCI-certificado    │
│ • Retorna APENAS payment_token para o LLM           │
│ • Nunca compartilha cartao/CVV com o LLM            │
└─────────────────────────────────────────────────────┘
```

**Sua missao:** Construir um `PaymentBoundary` que isola arquiteturalmente os dados de pagamento do contexto do LLM. O boundary extrai dados sensiveis do input do usuario, processa o pagamento em uma zona PCI isolada, e retorna apenas um token opaco para o LLM.

---

## Cenario: KODA Processando Pagamento no WhatsApp

### Contexto

O KODA e um agente de vendas de suplementos via WhatsApp. Durante o fluxo de compra, o cliente envia dados de pagamento em linguagem natural:

```
"Pago com cartao de credito. Numero 4916-XXXX-XXXX-3210, validade 08/27, CVV 456. 
 Meu CPF e 123.456.789-00. Divide em 3x por favor."
```

O fluxo ATUAL (quebrado):

```
1. Mensagem do cliente entra no prompt do LLM (incluindo cartao, CVV, CPF)
2. LLM chama a tool process_payment() extraindo dados do proprio prompt
3. Tool processa pagamento e retorna resultado para o LLM
4. LLM gera resposta "Pagamento aprovado!"

Problema: Passos 1 e 4 expoem dados PCI ao LLM.
```

O fluxo CORRETO com Regulated Data Boundary:

```
1. Interceptador pre-LLM detecta intencao de pagamento
2. Extrai dados de pagamento da mensagem original (ANTES do LLM)
3. Envia para PaymentBoundary (zona PCI isolada)
4. PaymentBoundary processa pagamento, retorna payment_token
5. Substitui dados sensiveis pelo token na mensagem
6. LLM recebe: "Pago com cartao [payment_token: pay_tok_X7K2]. Divide em 3x."
7. LLM usa payment_token para consultar STATUS do pagamento (nunca os dados)
```

### Dados de Entrada

```python
# Mensagens reais de clientes KODA (dados de pagamento simulados)
CUSTOMER_MESSAGES = [
    {
        "message_id": "MSG-001",
        "raw_text": "Quero comprar 2 Whey. Cartao 4532-8765-1234-5678, validade 12/25, CVV 321. CPF 987.654.321-00.",
        "has_payment_data": True,
    },
    {
        "message_id": "MSG-002",
        "raw_text": "Tem como parcelar? Meu cartao e 5214-7890-4561-2345, vencimento 03/27, codigo 789.",
        "has_payment_data": True,
    },
    {
        "message_id": "MSG-003",
        "raw_text": "Qual o prazo de entrega para Sao Paulo?",
        "has_payment_data": False,
    },
    {
        "message_id": "MSG-004",
        "raw_text": "Vou pagar no pix. Minha chave e 11987654321.",
        "has_payment_data": True,  # PIX key tambem e dado sensivel
    },
    {
        "message_id": "MSG-005",
        "raw_text": "Pode enviar para: Joao Silva, CPF 456.789.123-00, Rua Augusta 1500, apto 42, Sao Paulo-SP, 01304-001. Cartao 4024-0071-2345-6789, 05/26, 567.",
        "has_payment_data": True,
    },
]
```

---

## Requisitos

### Requisitos Funcionais

1. **RF1 - Deteccao pre-LLM:** Antes de qualquer mensagem entrar no prompt do LLM, o `PaymentDetector` analisa o texto e detecta se ha dados de pagamento (numeros de cartao, CVV, dados de PIX, CPF)
2. **RF2 - Extracao e sanitizacao:** Se dados de pagamento forem detectados, o `PaymentExtractor` extrai os dados sensiveis e o `PaymentSanitizer` substitui por tokens opacos no texto que vai para o LLM
3. **RF3 - Boundary isolado:** O `PaymentBoundary` processa o pagamento em uma zona isolada. O LLM nunca recebe o numero do cartao, CVV, ou dados de PIX. O boundary retorna apenas um `payment_token` e um `status`
4. **RF4 - Token query pelo LLM:** O LLM pode consultar o status de um pagamento usando o `payment_token`, mas nunca recebe os dados originais do pagamento de volta
5. **RF5 - Dados de endereco:** Dados de endereco (rua, numero, CEP) NAO sao removidos — o LLM precisa deles para calcular frete e prazo de entrega. Apenas dados PCI/PII financeiros sao isolados
6. **RF6 - Log de auditoria:** Cada transacao no boundary gera uma entrada de auditoria com: timestamp, payment_token (nunca o cartao), status, e ID da mensagem original

### Requisitos Tecnicos

1. **RT1 - Python puro:** Implementacao em Python com stdlib + dataclasses
2. **RT2 - Regex para deteccao:** Deteccao de cartoes, CVV, CPF e chaves PIX via regex (sem dependencias externas)
3. **RT3 - Boundary como modulo separado:** O `PaymentBoundary` e um modulo Python que simula uma chamada a um servico externo PCI-certificado (na pratica, uma funcao com latencia simulada de 200ms)

---

## Sua Tarefa

Voce vai implementar o `PaymentBoundary` em 3 partes.

---

### Parte 1: Diagnosticar o Vazamento de Dados PCI (10 min)

Analise as mensagens `CUSTOMER_MESSAGES` acima e identifique:

```python
# TAREFA: Para cada mensagem, responda manualmente:
#
# MSG-001: Quais dados sensiveis estao presentes?
#          R: cartao (4532-...), validade, CVV, CPF
#          O que entraria no prompt do LLM no fluxo ATUAL?
#          R: tudo — o texto completo
#          O que deveria entrar no prompt do LLM no fluxo CORRETO?
#          R: "Quero comprar 2 Whey. [payment_token: pay_tok_...]. [cpf_token: cpf_tok_...]."
#
# MSG-002: (responda)
# MSG-003: (responda)
# MSG-004: (responda)
# MSG-005: (responda)
#
# 2. Alem de dados de cartao, que outros dados sensiveis um agente KODA
#    poderia receber que NAO deveriam entrar no prompt do LLM?
#
# 3. Por que "policy controls" (ex: "nao coloque cartao no prompt") nao sao
#    suficientes? Qual a diferenca entre policy control e architectural isolation?
```

---

### Parte 2: Implementar o PaymentBoundary (45 min)

```python
import re
import uuid
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


# ============================================================
# DATA MODELS
# ============================================================

class PaymentStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    APPROVED = "approved"
    DECLINED = "declined"
    ERROR = "error"


@dataclass
class PaymentData:
    """Dados de pagamento extraidos de uma mensagem."""
    card_number: Optional[str] = None
    card_expiry: Optional[str] = None
    card_cvv: Optional[str] = None
    cpf: Optional[str] = None
    pix_key: Optional[str] = None


@dataclass
class PaymentResult:
    """Resultado do processamento no boundary isolado."""
    payment_token: str
    status: PaymentStatus
    masked_card: str        # ex: "4532-XXXX-XXXX-5678"
    installments: int = 1
    error_message: str = ""


@dataclass
class SanitizedMessage:
    """Mensagem sanitizada, pronta para o prompt do LLM."""
    original_id: str
    sanitized_text: str
    payment_token: Optional[str] = None
    has_payment_data: bool = False


@dataclass
class AuditEntry:
    """Entrada de auditoria do boundary."""
    timestamp: str
    payment_token: str
    message_id: str
    status: PaymentStatus
    masked_card: str


# ============================================================
# PAYMENT DETECTOR — regex para detectar dados sensiveis
# ============================================================

# Padroes regex (apenas deteccao, nunca armazenam o valor completo em log)
CARD_PATTERN = re.compile(r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b')
CVV_PATTERN = re.compile(r'\b(?:cvv|cvc|codigo?|cod\.?|cvv:?)\s*:?\s*(\d{3,4})\b', re.IGNORECASE)
CPF_PATTERN = re.compile(r'\b\d{3}\.\d{3}\.\d{3}-\d{2}\b')
PIX_KEY_PATTERN = re.compile(r'(?:pix|chave\s*(?:pix)?)\s*:?\s*(\S+@\S+|\d{11}|[a-f0-9-]{36})', re.IGNORECASE)
EXPIRY_PATTERN = re.compile(r'\b(?:validade|vencimento|expiry?|exp\.?)\s*:?\s*(\d{2}/\d{2,4})\b', re.IGNORECASE)


def detect_payment_data(text: str) -> bool:
    """Detecta se o texto contem dados de pagamento."""
    # SEU CODIGO AQUI
    pass


def extract_payment_data(text: str) -> PaymentData:
    """
    Extrai dados de pagamento do texto.
    Retorna PaymentData com os campos encontrados.
    Campos nao encontrados ficam como None.
    """
    # SEU CODIGO AQUI
    pass


def mask_card(card_number: str) -> str:
    """
    Mascara um numero de cartao para exibicao segura.
    Ex: "4532-8765-1234-5678" → "4532-XXXX-XXXX-5678"
    """
    # SEU CODIGO AQUI
    pass


def sanitize_message(text: str, payment_data: PaymentData) -> str:
    """
    Substitui dados sensiveis por tokens na mensagem.

    Regras:
    - Numero de cartao → "[payment_token: <token>]"
    - CVV → removido completamente (nunca necessario apos pagamento)
    - CPF → "[cpf_token: <token>]" (se existir payment_data.cpf)
    - Chave PIX → "[pix_token: <token>]"
    - Endereco, nome, CEP → MANTIDOS (LLM precisa para frete/entrega)
    - Validade do cartao → removida (nao necessaria apos pagamento)

    Returns:
        Texto sanitizado, seguro para o prompt do LLM.
    """
    # SEU CODIGO AQUI
    pass


# ============================================================
# PAYMENT BOUNDARY — zona PCI isolada
# ============================================================

@dataclass
class PaymentBoundary:
    """
    Boundary de isolamento arquitetural para dados regulados.

    Este modulo simula um servico externo PCI-certificado.
    Na pratica, seria um servico rodando em infraestrutura separada
    com certificacao PCI DSS Level 1. O LLM nunca interage diretamente
    com este modulo — apenas atraves de tokens opacos.
    """

    payment_store: dict[str, PaymentData] = field(default_factory=dict)
    audit_log: list[AuditEntry] = field(default_factory=list)
    simulated_latency_ms: int = 200

    def process_payment(
        self, payment_data: PaymentData, message_id: str, installments: int = 1
    ) -> PaymentResult:
        """
        Processa um pagamento na zona PCI isolada.

        Simula a chamada a um gateway de pagamento PCI-certificado.
        NUNCA retorna dados sensiveis — apenas payment_token + status.

        Args:
            payment_data: Dados de pagamento extraidos da mensagem.
            message_id: ID da mensagem original.
            installments: Numero de parcelas.

        Returns:
            PaymentResult com token opaco e status.
        """
        # Simular latencia de chamada externa
        time.sleep(self.simulated_latency_ms / 1000.0)

        # Gerar token opaco
        token = f"pay_tok_{uuid.uuid4().hex[:8].upper()}"

        # Armazenar dados de pagamento (na pratica, iria para vault PCI)
        self.payment_store[token] = payment_data

        # Simular processamento (90% de chance de aprovacao)
        import random
        status = PaymentStatus.APPROVED if random.random() < 0.9 else PaymentStatus.DECLINED

        # Mascarar cartao para o resultado
        masked = mask_card(payment_data.card_number) if payment_data.card_number else "N/A"

        # Registrar auditoria
        entry = AuditEntry(
            timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            payment_token=token,
            message_id=message_id,
            status=status,
            masked_card=masked,
        )
        self.audit_log.append(entry)

        return PaymentResult(
            payment_token=token,
            status=status,
            masked_card=masked,
            installments=installments,
        )

    def query_payment(self, payment_token: str) -> Optional[PaymentResult]:
        """
        Consulta o status de um pagamento pelo token.
        Esta e a UNICA funcao que o LLM pode chamar — ela retorna
        status e masked_card, nunca os dados originais.
        """
        if payment_token not in self.payment_store:
            return None
        payment_data = self.payment_store[payment_token]
        masked = mask_card(payment_data.card_number) if payment_data.card_number else "N/A"
        return PaymentResult(
            payment_token=payment_token,
            status=PaymentStatus.APPROVED,  # simplificado
            masked_card=masked,
        )


# ============================================================
# KODA MESSAGE PIPELINE — fluxo completo pre-LLM
# ============================================================

@dataclass
class KodaMessagePipeline:
    """Pipeline de processamento de mensagens do KODA antes do LLM."""

    boundary: PaymentBoundary = field(default_factory=PaymentBoundary)
    processed: list[SanitizedMessage] = field(default_factory=list)

    def process_message(self, message_id: str, raw_text: str) -> SanitizedMessage:
        """
        Processa uma mensagem antes de entrar no prompt do LLM.

        Fluxo:
        1. Detectar se ha dados de pagamento (detect_payment_data)
        2. Se sim: extrair dados (extract_payment_data)
        3. Processar pagamento no boundary isolado (boundary.process_payment)
        4. Sanitizar mensagem substituindo dados por tokens
        5. Se nao: retornar mensagem original intacta
        6. Retornar SanitizedMessage com texto seguro para o LLM
        """
        # SEU CODIGO AQUI
        pass

    def get_llm_safe_messages(self) -> list[str]:
        """Retorna apenas os textos sanitizados para injecao no prompt do LLM."""
        return [m.sanitized_text for m in self.processed]


# ============================================================
# TESTES RAPIDOS
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("TESTE DO PAYMENT BOUNDARY")
    print("=" * 60)

    # Teste 1: Detectar dados de pagamento
    assert detect_payment_data(CUSTOMER_MESSAGES[0]["raw_text"]), \
        "MSG-001 deve ser detectada como tendo dados de pagamento"
    assert not detect_payment_data(CUSTOMER_MESSAGES[2]["raw_text"]), \
        "MSG-003 NAO deve ser detectada (pergunta sobre frete)"
    print("Teste 1 OK: deteccao de dados de pagamento funciona")

    # Teste 2: Extrair dados de pagamento
    pd = extract_payment_data(CUSTOMER_MESSAGES[0]["raw_text"])
    assert pd.card_number is not None, "Deve extrair numero do cartao"
    assert pd.cpf is not None, "Deve extrair CPF"
    assert "4532" in pd.card_number, f"Numero do cartao deve conter 4532, obtido {pd.card_number}"
    print(f"Teste 2 OK: extracao — cartao={mask_card(pd.card_number)}, CPF={pd.cpf}")

    # Teste 3: Mascarar cartao
    masked = mask_card("4532-8765-1234-5678")
    assert masked == "4532-XXXX-XXXX-5678", f"Mascara incorreta: {masked}"
    print(f"Teste 3 OK: mascara — {masked}")

    # Teste 4: Sanitizar mensagem
    sanitized = sanitize_message(CUSTOMER_MESSAGES[0]["raw_text"], pd)
    assert "4532" not in sanitized, f"Numero do cartao nao deve aparecer no texto sanitizado: {sanitized}"
    assert "321" not in sanitized or "payment_token" in sanitized, \
        "CVV nao deve aparecer no texto sanitizado"
    assert "cpf_token" in sanitized.lower() or "987.654.321-00" not in sanitized, \
        "CPF deve ser substituido por token"
    print(f"Teste 4 OK: mensagem sanitizada — {sanitized[:120]}...")

    # Teste 5: Pipeline completo
    pipeline = KodaMessagePipeline()
    for msg in CUSTOMER_MESSAGES:
        result = pipeline.process_message(msg["message_id"], msg["raw_text"])
        print(f"\n  {msg['message_id']}: payment_data={result.has_payment_data}")
        print(f"    Original: {msg['raw_text'][:80]}...")
        print(f"    Sanitized: {result.sanitized_text[:80]}...")
        if result.payment_token:
            print(f"    Token: {result.payment_token}")

    # Verificar: nenhuma mensagem sanitizada deve conter dados de cartao
    for msg in pipeline.processed:
        if msg.has_payment_data:
            assert not CARD_PATTERN.search(msg.sanitized_text), \
                f"{msg.original_id}: texto sanitizado contem numero de cartao!"
            assert not CVV_PATTERN.search(msg.sanitized_text), \
                f"{msg.original_id}: texto sanitizado contem CVV!"

    print(f"\nTeste 5 OK: pipeline completo — {len(pipeline.processed)} mensagens processadas")
    print(f"  Nenhum dado PCI no texto sanitizado!")

    # Teste 6: LLM-safe query
    if pipeline.processed[0].payment_token:
        token = pipeline.processed[0].payment_token
        query_result = pipeline.boundary.query_payment(token)
        assert query_result is not None, "Deve encontrar pagamento pelo token"
        assert query_result.payment_token == token, "Token deve corresponder"
        # CRITICO: query_payment NUNCA deve retornar o numero completo do cartao
        assert "4532-8765" not in str(query_result.__dict__), \
            "query_payment() NAO deve expor numero completo do cartao!"
        print(f"Teste 6 OK: LLM-safe query — token={token}, status={query_result.status.value}, card={query_result.masked_card}")

    # Teste 7: Audit log
    print(f"\nTeste 7: Audit log ({len(pipeline.boundary.audit_log)} entradas)")
    for entry in pipeline.boundary.audit_log:
        print(f"  [{entry.timestamp}] token={entry.payment_token} msg={entry.message_id} status={entry.status.value} card={entry.masked_card}")
    # Audit log nunca deve conter numero completo do cartao
    for entry in pipeline.boundary.audit_log:
        assert "4532-8765" not in entry.masked_card or "XXXX" in entry.masked_card, \
            "Audit log NAO deve conter numero completo do cartao!"
    print("  OK: audit log nao contem dados PCI completos")

    print("\n" + "=" * 60)
    print("TODOS OS TESTES DO PAYMENT BOUNDARY PASSARAM")
    print("=" * 60)
```

---

### Parte 3: Integracao com o Fluxo KODA (20 min)

```python
# ============================================================
# SIMULACAO: Fluxo KODA com e sem PaymentBoundary
# ============================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("SIMULACAO: KODA — COM vs. SEM PaymentBoundary")
    print("=" * 60)

    # Cenario: 3 mensagens de um cliente no fluxo de compra
    conversation = [
        ("MSG-A1", "Quanto custa o Whey Isolado 1kg?"),
        ("MSG-A2", "Vou levar 2. Meu cartao 4532-1111-2222-3333, validade 08/27, CVV 123. CPF 111.222.333-44."),
        ("MSG-A3", "Obrigado! Qual o prazo de entrega?"),
    ]

    # SEM boundary (fluxo quebrado — ATUAL)
    print("\n--- FLUXO SEM BOUNDARY (quebrado) ---")
    for msg_id, text in conversation:
        print(f"\n[LLM prompt] {msg_id}: {text}")
        # Problema: MSG-A2 contem cartao + CVV + CPF no prompt do LLM
        if msg_id == "MSG-A2":
            print("  ⚠️  ALERTA PCI: Numero de cartao, CVV e CPF no prompt do LLM!")

    # COM boundary (fluxo correto)
    print("\n--- FLUXO COM BOUNDARY (correto) ---")
    pipeline = KodaMessagePipeline()
    for msg_id, text in conversation:
        result = pipeline.process_message(msg_id, text)
        print(f"\n[LLM prompt] {msg_id}: {result.sanitized_text}")
        if result.payment_token:
            print(f"  ✅ PCI SAFE: Dados isolados no boundary. Token: {result.payment_token}")

    # Metricas de compliance
    total_with_payment = sum(1 for m in pipeline.processed if m.has_payment_data)
    total_safe = sum(
        1 for m in pipeline.processed
        if not CARD_PATTERN.search(m.sanitized_text)
    )
    print(f"\nMETRICAS DE COMPLIANCE:")
    print(f"  Mensagens com dados de pagamento: {total_with_payment}")
    print(f"  Mensagens seguras para LLM: {total_safe}/{len(pipeline.processed)}")
    print(f"  Compliance: {'✅ 100%' if total_safe == len(pipeline.processed) else '❌ VIOLACAO'}")

    # TAREFA FINAL: Responda
    # 1. Se o KODA processa 500 pagamentos/dia, quantos numeros de cartao
    #    entrariam no prompt do LLM SEM o boundary?
    # 2. Qual o impacto de compliance se o provedor de LLM (ex: OpenAI)
    #    armazena logs de prompt por 30 dias?
    # 3. Alem de pagamento, que outros tipos de dados regulados o KODA
    #    poderia precisar isolar no futuro? (LGPD, dados de saude, etc.)
```

---

## Validacao: Criterios de Aceitacao

Seu codigo sera considerado **APROVADO** quando:

### Criterio 1: Diagnostico (Parte 1)

- [ ] Voce identificou todos os dados sensiveis nas 5 mensagens
- [ ] Voce explicou a diferenca entre policy control e architectural isolation
- [ ] Voce listou outros tipos de dados regulados alem de pagamento

### Criterio 2: Deteccao e Extracao

- [ ] `detect_payment_data()` identifica corretamente mensagens com e sem dados PCI
- [ ] `extract_payment_data()` extrai cartao, CVV, CPF e chave PIX
- [ ] `mask_card()` formata corretamente (4532-XXXX-XXXX-5678)

### Criterio 3: Sanitizacao

- [ ] `sanitize_message()` remove numero do cartao e substitui por token
- [ ] `sanitize_message()` remove CVV completamente
- [ ] `sanitize_message()` MANTEM endereco e CEP (LLM precisa)
- [ ] `sanitize_message()` substitui CPF por token

### Criterio 4: Boundary e Pipeline

- [ ] `PaymentBoundary.process_payment()` retorna apenas token + status + masked_card
- [ ] `PaymentBoundary.query_payment()` NUNCA retorna dados originais do cartao
- [ ] `KodaMessagePipeline.process_message()` aplica o fluxo completo
- [ ] Nenhuma mensagem sanitizada contem dados PCI

### Criterio 5: Audit trail

- [ ] Cada pagamento gera uma entrada de auditoria
- [ ] Audit log contem apenas `masked_card`, nunca o numero completo

---

## Rubrica de Avaliacao

| Criterio | Peso | Insuficiente (0-3) | Basico (4-6) | Proficiente (7-8) | Excelente (9-10) |
|---|---|---|---|---|---|
| **Diagnostico (Parte 1)** | 15% | Nao identificou os dados sensiveis | Identificou parcialmente | Identificou todos os dados + explicou policy vs architecture | Diagnosticou + propos outros boundaries regulados |
| **Deteccao + Extracao (Parte 2)** | 30% | Regex nao funcionam | Detecta mas nao extrai todos os campos | Extracao completa com mascara | Extracao robusta com edge cases (formatos variaveis de cartao) |
| **Sanitizacao + Boundary (Parte 2)** | 35% | Boundary nao implementado | Sanitiza mas boundary vaza dados | Boundary isolado com token query segura | Pipeline completo com zero vazamentos em todos os cenarios |
| **Simulacao + Testes** | 20% | Nenhum cenario passa | 3 criterios passam | 4 criterios passam | Todos os 5 criterios passam + metricas de compliance |

**Nota final:** Media ponderada. **Aprovacao:** >= 7.0

---

## Dicas para Implementacao

### Para a Deteccao

1. **Regex nao e perfeito, mas e deterministico.** Um cartao digitado como "4 5 3 2" nao sera detectado pelo regex. Mas o regex cobre 95% dos casos reais (clientes digitam cartao no formato padrao). Para os 5% restantes, um segundo estagio de deteccao com LLM rodando em infraestrutura isolada pode complementar — mas isso e avancado.

2. **Falsos positivos sao aceitaveis.** E melhor sanitizar uma mensagem que nao tinha dados de pagamento do que deixar passar uma que tinha. O custo de um falso positivo e substituir um trecho de texto por um token; o custo de um falso negativo e uma violacao PCI.

3. **O detector deve rodar ANTES do LLM.** Se o detector rodar como uma tool chamada PELO LLM, o dado ja entrou no prompt. A deteccao pre-LLM e o que torna o boundary arquitetural, nao apenas uma policy.

### Para o Boundary

1. **O boundary e um modulo, nao uma sugestao.** Nao existe "opcional" no boundary — toda mensagem passa pelo pipeline. Se o detector falhar, a mensagem vai para o LLM como esta, mas o boundary NAO foi desligado — ele falhou. A distincao importa para compliance.

2. **Tokens sao opacos por design.** O LLM recebe `pay_tok_A7X9`, nao `payment_id: 42`. Tokos opacos impedem que o modelo infira informacao sobre o pagamento (ex: IDs sequenciais revelam volume de transacoes).

3. **O audit log e para compliance, nao para debug.** O log registra que um pagamento foi processado, por qual mensagem, com qual resultado. Ele NAO registra o numero do cartao. Se um auditor precisar do numero do cartao, ele vai ao vault PCI — um sistema separado com controles de acesso proprios.

---

## Duvidas Comuns

**P: Isso nao e so um filtro de PII?**
R: E mais que um filtro. Um filtro de PII remove dados sensiveis do texto. O Regulated Data Boundary REDIRECIONA os dados para uma zona isolada, processa a operacao regulada (pagamento), e retorna um token. O filtro diz "nao coloque isso no prompt". O boundary diz "processe isso em infraestrutura certificada e informe o LLM apenas do resultado".

**P: O LLM ainda pode mencionar o cartao na resposta?**
R: Nao — o LLM nunca viu o numero do cartao. Ele so viu `[payment_token: pay_tok_X7K2]`. Se o LLM tentar mencionar o cartao, ele nao tem a informacao para isso. O maximo que ele pode dizer e: "Pagamento com cartao terminado em 5678 aprovado" — que ele recebeu via `query_payment()` com `masked_card`.

**P: Como isso se aplica a outros dominios alem de pagamento?**
R: O mesmo padrao se aplica a: (a) dados de saude (HIPAA) — diagnosticos e exames nunca entram no LLM, apenas tokens de prontuario; (b) autenticacao — senhas e tokens de sessao nunca entram no LLM; (c) documentos de identidade — RG, CNH, passaporte. Qualquer dado regulado por compliance segue o mesmo boundary: extrair → isolar → tokenizar.

**P: Isso nao aumenta a latencia?**
R: Sim. O `PaymentBoundary.process_payment()` tem latencia simulada de 200ms. Na pratica, uma chamada a um gateway PCI pode levar 500-2000ms. Mas essa latencia e inevitavel — processar um pagamento sempre leva tempo. A diferenca e que, com o boundary, a latencia ocorre em infraestrutura certificada, nao no prompt do LLM.

---

## Proximo Passo

Depois de completar este exercicio:
1. Leia `[[docs/canonical/governance-context-injection-pii-prevention|Governance Context Injection — PII Prevention]]` para entender a camada de policy complementar ao boundary arquitetural
2. Leia `[[curriculum/04-nivel-4-koda-specific/01-koda-architecture|Arquitetura KODA]]` para ver como o PaymentBoundary se integra ao pipeline completo do KODA
3. (Opcional) Estenda o boundary com `HealthDataBoundary` — mesmo padrao para dados de saude (ex: KODA perguntando sobre restricoes alimentares com implicacoes medicas)

---

*Exercicio Regulated Data Boundary | Nivel 4 — KODA-Especifico*

**Dados regulados nao pertencem ao prompt do LLM. Pertencem a uma zona arquiteturalmente isolada com certificacao propria.**
