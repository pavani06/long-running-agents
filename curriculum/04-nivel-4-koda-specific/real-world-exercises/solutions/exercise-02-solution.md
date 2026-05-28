# 🧩 Solução do Exercício 02: Pipeline Multi-Agent da Jornada KODA
## Implementação completa da jornada awareness, discovery, recommendation, cart, payment e fulfillment

**Tempo Estimado:** 180-240 minutos  
**Nível:** 4 - KODA-Específico  
**Pré-requisito:** Ter completado Nível 1, Nível 2, Nível 3, `01-koda-architecture.md` e `02-customer-journey-flows.md`  
**Status:** 🟢 SOLUÇÃO COMPLETA  
**Data de Criação:** Maio 2026

---

## 📖 Prólogo: A Venda que Não Podia Depender de Sorte

Quinta-feira, 18h42.
Marina saiu da academia com uma dor conhecida nos ombros e uma dúvida nova na cabeça.
Ela queria voltar a treinar com mais energia, mas não queria repetir a experiência ruim que teve meses antes com um pré-treino que pesou no estômago.
O rótulo dizia chocolate. A promessa dizia energia limpa. O resultado foi enjoo, desconforto e uma noite inteira se perguntando se suplemento era mesmo para ela.
Dessa vez, Marina abriu o WhatsApp da KODA com três critérios claros: precisava ser sem lactose, precisava caber em R$ 150 e precisava ter sabor chocolate.
A mensagem parecia simples.
```
Marina: "Oi KODA, quero um pré-treino sem lactose. Meu orçamento é R$ 150 e prefiro chocolate."
```
Para um chatbot simples, essa mensagem seria convite para responder com uma lista de produtos.
Para o KODA real, essa mensagem inicia uma operação comercial completa.
Primeiro existe awareness. KODA precisa reconhecer que Marina está entrando em uma jornada de compra, não apenas fazendo uma pergunta solta.
Depois vem discovery. O sistema precisa transformar uma frase curta em um perfil verificável, com objetivo, restrição alimentar, orçamento, preferência e contexto de treino.
Em seguida aparece recommendation. Não basta encontrar um SKU. A recomendação precisa explicar por que aquele produto serve para Marina, por que ele é seguro e por que não ultrapassa o orçamento.
O próximo passo é cart. O carrinho precisa preservar exatamente o que foi aprovado, sem trocar produto, preço ou quantidade.
Depois vem payment. O pagamento precisa confirmar valor, método, referência e estado final sem prometer captura antes da confirmação.
Por fim, fulfillment. A operação precisa separar produto, gerar rastreio e avisar Marina com uma mensagem clara.
Essa sequência é maior do que uma resposta de IA.
É um pipeline multi-agent.
Cada agente carrega uma responsabilidade pequena e auditável.
O Planner organiza a jornada.
O Discovery Agent extrai o que precisa ser lembrado.
O Catalog Agent consulta os produtos elegíveis.
O Generator cria uma recomendação humana.
O Evaluator protege Marina e a KODA de uma recomendação ruim.
O Order Agent transforma a escolha em pedido.
O Payment Agent confirma a cobrança.
O Fulfillment Agent coloca o pedido na operação real.
A razão desse exercício existir é simples: em uma venda real, erro pequeno vira quebra de confiança.
Se o KODA esquece lactose, Marina não compra.
Se o KODA recomenda acima de R$ 150, Marina sente que não foi ouvida.
Se o KODA cria carrinho com outro SKU, a operação perde controle.
Se o KODA confirma pagamento sem confirmação, a empresa cria risco financeiro.
Se o KODA promete entrega sem estoque, o pós-venda vira incêndio.
Este documento mostra a solução completa para evitar isso.
Você vai construir um pipeline inteiro, com arquivos de estado, retries, fallback, avaliação por etapa e uma execução concreta da jornada de Marina.
No final, a pergunta não será mais "como faço um agente responder bem?".
A pergunta será "como faço uma operação inteira caber em agentes pequenos, verificáveis e seguros?".
Essa é a passagem do Nível 4.

---

## 🎯 O Que o Exercício Pede

O Exercício 02 pede que você implemente uma solução completa para a jornada comercial do KODA usando coordenação multi-agent.
A entrada é uma mensagem de cliente no WhatsApp.
A saída é um pedido pago e encaminhado para fulfillment.
Entre esses dois pontos, nenhum agente pode depender de memória implícita do modelo.
Todo dado crítico precisa existir em arquivo de estado.

### Requisitos funcionais

1. Receber uma mensagem de cliente contendo intenção de compra, restrição alimentar, orçamento e preferência.
2. Criar um plano explícito da jornada usando um Planner.
3. Extrair perfil do cliente com um Discovery Agent.
4. Consultar e filtrar catálogo com um Catalog Agent.
5. Gerar recomendação com um Recommendation Agent no papel de Generator.
6. Avaliar recomendação com um Quality Agent no papel de Evaluator.
7. Repetir Generator e Evaluator até aprovação ou limite de tentativas.
8. Criar pedido com um Order Agent somente depois de aprovação.
9. Confirmar pagamento com um Payment Agent usando API simulada.
10. Abrir fulfillment com um Fulfillment Agent usando API simulada.
11. Persistir cada transição em arquivo JSON auditável.
12. Registrar métricas de latência, tentativa, score e fallback.

### Requisitos de estado

O pipeline precisa escrever estes arquivos no diretório de estado da conversa:

```
customer_profile.json
catalog_snapshot.json
discovery_state.json
recommendation_draft.json
evaluation_verdict.json
order_state.json
payment_state.json
fulfillment_state.json
```

### Requisitos de qualidade

A qualidade não fica concentrada no final.
Cada etapa precisa ter critérios próprios.
O Discovery precisa provar que entendeu Marina.
O Catalog precisa provar que não trouxe SKU perigoso.
O Generator precisa explicar com clareza.
O Evaluator precisa rejeitar quando faltar segurança, evidência ou próximo passo.
O Order precisa preservar o carrinho aprovado.
O Payment precisa bater valor e método.
O Fulfillment precisa criar rastreio ou cair para revisão manual.

### Critério de conclusão

A solução está completa quando o pipeline executa a jornada inteira de Marina, da primeira mensagem ao fulfillment, com todos os arquivos de estado gerados e uma recomendação aprovada antes do pedido.

---

## 🏗️ Arquitetura da Solução

A solução usa coordenação por arquivos JSON porque esse formato deixa o contrato de cada agente visível.
Cada agente lê arquivos, produz um novo arquivo e nunca altera a responsabilidade do agente anterior.
O Orchestrator é o harness que decide a ordem, controla retries, aplica fallback e registra métricas.

### Diagrama ASCII da arquitetura completa

```
┌──────────────────────────────────────────────────────────────────────────────────────┐
│                         PIPELINE MULTI-AGENT KODA, EXERCÍCIO 02                      │
└──────────────────────────────────────────────────────────────────────────────────────┘

                                ┌─────────────────────────┐
                                │ Cliente no WhatsApp     │
                                │ Marina envia intenção   │
                                └────────────┬────────────┘
                                             │ customer_message.json
                                             ▼
┌──────────────────────────────────────────────────────────────────────────────────────┐
│ ORCHESTRATOR                                                                         │
│ Controla ordem, retries, fallback, métricas e passagem entre fases                    │
└────────────┬─────────────────────────────────────────────────────────────────────────┘
             │
             ▼
      ┌─────────────┐      plan.json
      │ Planner     │──────────────────────────────────────────────────────────────┐
      └──────┬──────┘                                                              │
             │                                                                     │
             ▼                                                                     │
      ┌─────────────┐      discovery_state.json      customer_profile.json          │
      │ Discovery   │─────────────────────────────────────────────────────────┐     │
      └──────┬──────┘                                                         │     │
             │                                                                │     │
             ▼                                                                │     │
      ┌─────────────┐      catalog_snapshot.json                               │     │
      │ Catalog     │────────────────────────────────────────────────────┐     │     │
      └──────┬──────┘                                                    │     │     │
             │                                                           │     │     │
             ▼                                                           │     │     │
      ┌─────────────┐      recommendation_draft.json                      │     │     │
      │ Generator   │──────────────────────────────────────────────┐      │     │     │
      └──────┬──────┘                                              │      │     │     │
             │                                                     │      │     │     │
             ▼                                                     │      │     │     │
      ┌─────────────┐      evaluation_verdict.json                 │      │     │     │
      │ Evaluator   │──────────────────────────────────────────────┘      │     │     │
      └──────┬──────┘                                                     │     │     │
             │                                                            │     │     │
             │ aprovado                                                   │     │     │
             ▼                                                            │     │     │
      ┌─────────────┐      order_state.json                               │     │     │
      │ Order       │─────────────────────────────────────────────────────┘     │     │
      └──────┬──────┘                                                           │     │
             │                                                                  │     │
             ▼                                                                  │     │
      ┌─────────────┐      payment_state.json                                    │     │
      │ Payment     │────────────────────────────────────────────────────────────┘     │
      └──────┬──────┘                                                                 │
             │                                                                         │
             ▼                                                                         │
      ┌─────────────┐      fulfillment_state.json                                       │
      │ Fulfillment │───────────────────────────────────────────────────────────────────┘
      └─────────────┘

Fluxo de rejeição:
Generator -> Evaluator -> feedback -> Generator novamente, no máximo 3 tentativas.

Fluxo de fallback:
Qualquer agente que falhar 3 vezes chama handler específico e registra estado seguro.
```

### Responsabilidade de cada componente

| Componente | Responsabilidade | Entrada principal | Saída principal | Risco que reduz |
|---|---|---|---|---|
| Planner | Divide a jornada em etapas verificáveis | `customer_message.json` | `plan.json` | Escopo confuso |
| Discovery Agent | Extrai perfil e restrições | `customer_message.json` | `customer_profile.json`, `discovery_state.json` | Esquecer dados críticos |
| Catalog Agent | Filtra produtos por regra real | `customer_profile.json` | `catalog_snapshot.json` | Recomendar SKU inválido |
| Recommendation Agent | Gera recomendação humana | `customer_profile.json`, `catalog_snapshot.json` | `recommendation_draft.json` | Resposta genérica |
| Quality Agent | Avalia segurança e qualidade | `recommendation_draft.json` | `evaluation_verdict.json` | Sycophancy e autoaprovação |
| Order Agent | Cria pedido a partir da recomendação aprovada | `recommendation_draft.json` | `order_state.json` | Troca de SKU no checkout |
| Payment Agent | Confirma pagamento simulado | `order_state.json` | `payment_state.json` | Valor divergente |
| Fulfillment Agent | Abre separação e rastreio | `payment_state.json` | `fulfillment_state.json` | Promessa sem operação |

---

## 🔗 Estratégias de Coordenação

Coordenação é a escolha de como agentes passam informação entre si.
No KODA, essa decisão afeta auditabilidade, latência, custo operacional e segurança comercial.

| Estratégia | Prós | Contras | Quando usar | Aplicabilidade KODA |
|---|---|---|---|---|
| File-based | Simples, auditável, fácil de ensinar, ótimo para replay de bugs, funciona sem infraestrutura extra | Pode ficar lento com volume alto, exige disciplina de schema, concorrência precisa de locks em produção | Exercícios, protótipos, pipelines internos, trilhas com baixa concorrência | Alta para este exercício e para traces de atendimento sensível |
| Message queue | Boa para alto volume, desacopla produtores e consumidores, absorve picos, permite consumidores paralelos | Exige Redis, RabbitMQ ou Kafka, dificulta leitura manual do estado, aumenta operação | Produção com muitas conversas simultâneas e eventos independentes | Média, útil quando KODA tiver grande volume de fulfillment ou notificações |
| Shared memory | Baixa latência, implementação rápida em um processo, bom para simulação local | Não sobrevive a crash, não audita, cria acoplamento forte, perigoso para dados críticos | Experimentos descartáveis sem valor comercial | Baixa, não deve guardar alergia, orçamento, pagamento ou pedido |
| API-based | Bom para times independentes, contratos HTTP claros, deploy separado, fácil de integrar com serviços externos | Mais latência, mais pontos de falha, exige autenticação e observabilidade | Sistemas maduros com serviços separados por domínio | Alta em produção para pagamento, catálogo real e ERP |

### Decisão deste exercício

A solução usa file-based coordination.
Isso deixa o aprendizado transparente.
O aluno consegue abrir cada arquivo e ver a transição de estado.
Também fica claro onde cada agente começa e termina.
Em produção, o mesmo contrato pode migrar para APIs ou filas sem mudar o modelo mental.

---

## 🐍 Implementação Completa do Pipeline (Python)

O código abaixo é um arquivo Python completo.
Ele usa apenas bibliotecas da standard library.
As APIs externas são simuladas para manter o exercício executável em qualquer máquina com Python 3.10 ou superior.
O diretório `state/marina_pre_treino` recebe todos os arquivos JSON da jornada.

### Como executar localmente

```bash
python koda_customer_journey_pipeline.py
```

### Código completo

```python
from __future__ import annotations

import json
import random
import time
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Optional, Protocol, Tuple


class PipelineError(Exception):
    """Erro base para falhas controladas do pipeline KODA."""


class StateValidationError(PipelineError):
    """Falha quando um arquivo de estado não respeita o contrato esperado."""


class AgentExecutionError(PipelineError):
    """Falha quando um agente não consegue produzir saída válida."""


class PaymentDeclinedError(PipelineError):
    """Falha simulada quando o provedor de pagamento recusa a cobrança."""


class StageName(str, Enum):
    PLANNER = "planner"
    DISCOVERY = "discovery"
    CATALOG = "catalog"
    GENERATOR = "generator"
    EVALUATOR = "evaluator"
    ORDER = "order"
    PAYMENT = "payment"
    FULFILLMENT = "fulfillment"


class JourneyPhase(str, Enum):
    AWARENESS = "awareness"
    DISCOVERY = "discovery"
    RECOMMENDATION = "recommendation"
    CART = "cart"
    PAYMENT = "payment"
    FULFILLMENT = "fulfillment"
    CLOSED = "closed"


class PaymentMethod(str, Enum):
    PIX = "pix"
    CREDIT_CARD = "credit_card"
    BOLETO = "boleto"


class Verdict(str, Enum):
    APPROVED = "approved"
    REJECTED = "rejected"
    FALLBACK = "fallback"


@dataclass
class CustomerMessage:
    conversation_id: str
    customer_id: str
    customer_name: str
    text: str
    channel: str = "whatsapp"
    created_at: str = field(default_factory=lambda: utc_now())


@dataclass
class CustomerProfile:
    customer_id: str
    name: str
    goal: str
    dietary_restrictions: List[str]
    budget_brl: float
    preferred_flavor: str
    preferred_payment_method: PaymentMethod
    training_context: str
    confidence: float
    evidence: List[str]
    updated_at: str = field(default_factory=lambda: utc_now())


@dataclass
class Product:
    sku: str
    name: str
    category: str
    flavor: str
    price_brl: float
    stock_units: int
    tags: List[str]
    contraindications: List[str]
    benefits: List[str]
    fulfillment_center: str


@dataclass
class CatalogSnapshot:
    conversation_id: str
    products: List[Product]
    filtered_skus: List[str]
    unavailable_skus: List[str]
    inventory_checked_at: str
    pricing_checked_at: str
    notes: List[str]


@dataclass
class PlanStep:
    step_id: str
    stage: StageName
    objective: str
    required_inputs: List[str]
    expected_output_file: str
    success_criteria: List[str]


@dataclass
class PlannerOutput:
    conversation_id: str
    phase: JourneyPhase
    plan_id: str
    steps: List[PlanStep]
    global_constraints: Dict[str, Any]
    max_retries_per_stage: int
    fallback_policy: Dict[str, str]
    created_at: str = field(default_factory=lambda: utc_now())


@dataclass
class DiscoveryState:
    conversation_id: str
    extracted_profile: CustomerProfile
    missing_fields: List[str]
    confidence_by_field: Dict[str, float]
    next_questions: List[str]
    stage_score: float


@dataclass
class RecommendationItem:
    sku: str
    name: str
    quantity: int
    unit_price_brl: float
    reason: str
    customer_fit: List[str]
    cautions: List[str]


@dataclass
class RecommendationDraft:
    conversation_id: str
    attempt: int
    headline: str
    items: List[RecommendationItem]
    total_brl: float
    customer_message: str
    evidence: List[str]
    evaluator_feedback_used: List[str]
    created_at: str = field(default_factory=lambda: utc_now())


@dataclass
class EvaluationVerdict:
    conversation_id: str
    attempt: int
    verdict: Verdict
    score: float
    required_score: float
    passed_checks: List[str]
    failed_checks: List[str]
    feedback_for_generator: List[str]
    created_at: str = field(default_factory=lambda: utc_now())


@dataclass
class OrderState:
    conversation_id: str
    order_id: str
    customer_id: str
    items: List[RecommendationItem]
    subtotal_brl: float
    shipping_brl: float
    total_brl: float
    shipping_address: str
    status: str
    created_at: str = field(default_factory=lambda: utc_now())


@dataclass
class PaymentState:
    conversation_id: str
    order_id: str
    payment_id: str
    method: PaymentMethod
    amount_brl: float
    status: str
    provider_reference: str
    confirmed_at: Optional[str]


@dataclass
class FulfillmentState:
    conversation_id: str
    order_id: str
    warehouse_ticket: str
    carrier: str
    tracking_code: str
    status: str
    estimated_delivery_date: str
    customer_notification: str
    created_at: str = field(default_factory=lambda: utc_now())


@dataclass
class StageMetric:
    stage: StageName
    attempt: int
    latency_ms: int
    status: str
    score: Optional[float]
    output_file: str


@dataclass
class PipelineResult:
    conversation_id: str
    final_phase: JourneyPhase
    approved_recommendation: RecommendationDraft
    evaluation: EvaluationVerdict
    order: OrderState
    payment: PaymentState
    fulfillment: FulfillmentState
    metrics: List[StageMetric]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def money(value: float) -> str:
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def ensure_state_dir(state_dir: Path) -> None:
    state_dir.mkdir(parents=True, exist_ok=True)


def dataclass_to_jsonable(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, list):
        return [dataclass_to_jsonable(item) for item in value]
    if isinstance(value, dict):
        return {key: dataclass_to_jsonable(item) for key, item in value.items()}
    if hasattr(value, "__dataclass_fields__"):
        return {key: dataclass_to_jsonable(item) for key, item in asdict(value).items()}
    return value


class StateStore:
    def __init__(self, state_dir: Path) -> None:
        ensure_state_dir(state_dir)
        self.state_dir = state_dir

    def path_for(self, filename: str) -> Path:
        return self.state_dir / filename

    def write_json(self, filename: str, payload: Any) -> None:
        target = self.path_for(filename)
        temporary = target.with_suffix(target.suffix + ".tmp")
        data = dataclass_to_jsonable(payload)
        with temporary.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2, sort_keys=True)
            file.write("\n")
        temporary.replace(target)

    def read_json(self, filename: str) -> Dict[str, Any]:
        target = self.path_for(filename)
        if not target.exists():
            raise StateValidationError(f"Arquivo de estado ausente: {filename}")
        with target.open("r", encoding="utf-8") as file:
            value = json.load(file)
        if not isinstance(value, dict):
            raise StateValidationError(f"Arquivo {filename} precisa conter um objeto JSON")
        return value

    def exists(self, filename: str) -> bool:
        return self.path_for(filename).exists()


class Agent(Protocol):
    stage: StageName

    def run(self, store: StateStore, attempt: int) -> str:
        ...


class PlannerAgent:
    stage = StageName.PLANNER

    def __init__(self, message: CustomerMessage) -> None:
        self.message = message

    def run(self, store: StateStore, attempt: int) -> str:
        plan = PlannerOutput(
            conversation_id=self.message.conversation_id,
            phase=JourneyPhase.AWARENESS,
            plan_id=f"plan_{uuid.uuid4().hex[:8]}",
            max_retries_per_stage=3,
            global_constraints={
                "customer_name": self.message.customer_name,
                "channel": self.message.channel,
                "journey": [
                    JourneyPhase.AWARENESS.value,
                    JourneyPhase.DISCOVERY.value,
                    JourneyPhase.RECOMMENDATION.value,
                    JourneyPhase.CART.value,
                    JourneyPhase.PAYMENT.value,
                    JourneyPhase.FULFILLMENT.value,
                ],
                "never_recommend_if": ["contains_lactose", "price_above_budget", "out_of_stock"],
            },
            fallback_policy={
                StageName.DISCOVERY.value: "pedir uma pergunta curta de clarificação",
                StageName.CATALOG.value: "oferecer atendimento humano se catálogo estiver indisponível",
                StageName.GENERATOR.value: "gerar recomendação conservadora com um único SKU seguro",
                StageName.EVALUATOR.value: "bloquear envio ao cliente e pedir revisão humana",
                StageName.ORDER.value: "manter carrinho como rascunho",
                StageName.PAYMENT.value: "enviar opção Pix e instrução de confirmação manual",
                StageName.FULFILLMENT.value: "abrir ticket de separação manual no centro de distribuição",
            },
            steps=[
                PlanStep(
                    step_id="step_discovery",
                    stage=StageName.DISCOVERY,
                    objective="extrair objetivo, restrições, orçamento e preferência de sabor",
                    required_inputs=["customer_message.json"],
                    expected_output_file="discovery_state.json",
                    success_criteria=[
                        "perfil contém objetivo de treino",
                        "perfil contém restrição sem lactose",
                        "perfil contém orçamento máximo",
                        "perfil contém sabor preferido",
                    ],
                ),
                PlanStep(
                    step_id="step_catalog",
                    stage=StageName.CATALOG,
                    objective="filtrar catálogo por estoque, preço, sabor e restrições",
                    required_inputs=["customer_profile.json"],
                    expected_output_file="catalog_snapshot.json",
                    success_criteria=[
                        "todos os SKUs filtrados existem",
                        "todos os SKUs estão em estoque",
                        "nenhum SKU contém lactose",
                        "preço total cabe no orçamento",
                    ],
                ),
                PlanStep(
                    step_id="step_generator",
                    stage=StageName.GENERATOR,
                    objective="gerar recomendação principal com justificativa clara",
                    required_inputs=["customer_profile.json", "catalog_snapshot.json"],
                    expected_output_file="recommendation_draft.json",
                    success_criteria=[
                        "recomendação cita a restrição sem lactose",
                        "recomendação respeita orçamento de R$ 150",
                        "mensagem cabe em WhatsApp sem ficar cansativa",
                    ],
                ),
                PlanStep(
                    step_id="step_evaluator",
                    stage=StageName.EVALUATOR,
                    objective="avaliar segurança, aderência, preço, tom e evidência",
                    required_inputs=["customer_profile.json", "catalog_snapshot.json", "recommendation_draft.json"],
                    expected_output_file="evaluation_verdict.json",
                    success_criteria=[
                        "score mínimo 0.86",
                        "nenhuma violação crítica",
                        "feedback acionável quando rejeitado",
                    ],
                ),
                PlanStep(
                    step_id="step_order",
                    stage=StageName.ORDER,
                    objective="criar carrinho confirmado após recomendação aprovada",
                    required_inputs=["recommendation_draft.json", "evaluation_verdict.json"],
                    expected_output_file="order_state.json",
                    success_criteria=["pedido contém SKUs corretos", "total confere", "endereço registrado"],
                ),
                PlanStep(
                    step_id="step_payment",
                    stage=StageName.PAYMENT,
                    objective="confirmar pagamento simulado via Pix",
                    required_inputs=["order_state.json", "customer_profile.json"],
                    expected_output_file="payment_state.json",
                    success_criteria=["pagamento confirmado", "valor igual ao total do pedido"],
                ),
                PlanStep(
                    step_id="step_fulfillment",
                    stage=StageName.FULFILLMENT,
                    objective="abrir separação e notificar cliente com rastreio",
                    required_inputs=["order_state.json", "payment_state.json"],
                    expected_output_file="fulfillment_state.json",
                    success_criteria=["ticket criado", "rastreio criado", "mensagem final pronta"],
                ),
            ],
        )
        store.write_json("customer_message.json", self.message)
        store.write_json("plan.json", plan)
        return "plan.json"


class DiscoveryAgent:
    stage = StageName.DISCOVERY

    def run(self, store: StateStore, attempt: int) -> str:
        message = store.read_json("customer_message.json")
        text = str(message.get("text", "")).lower()
        restrictions: List[str] = []
        if "lactose" in text or "sem leite" in text:
            restrictions.append("sem_lactose")
        if "glúten" in text or "gluten" in text:
            restrictions.append("sem_gluten")
        budget = 150.0 if "150" in text else 180.0
        flavor = "chocolate" if "chocolate" in text else "neutro"
        goal = "pré-treino sem lactose" if "pré" in text or "pre" in text else "suplemento esportivo"
        profile = CustomerProfile(
            customer_id=str(message["customer_id"]),
            name=str(message["customer_name"]),
            goal=goal,
            dietary_restrictions=restrictions,
            budget_brl=budget,
            preferred_flavor=flavor,
            preferred_payment_method=PaymentMethod.PIX,
            training_context="treina no fim da tarde e quer energia sem desconforto digestivo",
            confidence=0.91,
            evidence=[
                "cliente pediu pré-treino",
                "cliente informou restrição a lactose",
                "cliente declarou orçamento de R$ 150",
                "cliente preferiu sabor chocolate",
            ],
        )
        missing_fields = []
        if not restrictions:
            missing_fields.append("restrição alimentar")
        state = DiscoveryState(
            conversation_id=str(message["conversation_id"]),
            extracted_profile=profile,
            missing_fields=missing_fields,
            confidence_by_field={
                "goal": 0.93,
                "dietary_restrictions": 0.95 if restrictions else 0.40,
                "budget_brl": 0.90,
                "preferred_flavor": 0.92,
            },
            next_questions=[] if not missing_fields else ["Você tem alguma restrição alimentar que eu deva considerar?"],
            stage_score=0.91 if not missing_fields else 0.62,
        )
        if missing_fields:
            raise AgentExecutionError("Discovery incompleto para uma recomendação segura")
        store.write_json("customer_profile.json", profile)
        store.write_json("discovery_state.json", state)
        return "discovery_state.json"


class CatalogAgent:
    stage = StageName.CATALOG

    def __init__(self) -> None:
        self.catalog = [
            Product(
                sku="KDA-PRE-CHOC-001",
                name="KODA Pré-Treino Cacao Focus sem Lactose",
                category="pre_workout",
                flavor="chocolate",
                price_brl=129.90,
                stock_units=42,
                tags=["sem_lactose", "vegano", "baixo_acucar", "energia_gradual"],
                contraindications=["sensibilidade_alta_a_cafeina"],
                benefits=["energia para treino", "sabor chocolate", "boa digestibilidade"],
                fulfillment_center="SP-CENTRO-01",
            ),
            Product(
                sku="KDA-PRE-VAN-002",
                name="KODA Pré-Treino Vanilla Endurance",
                category="pre_workout",
                flavor="baunilha",
                price_brl=139.90,
                stock_units=18,
                tags=["sem_lactose", "sem_gluten", "endurance"],
                contraindications=["sensibilidade_alta_a_cafeina"],
                benefits=["resistência", "mistura fácil", "perfil limpo"],
                fulfillment_center="SP-CENTRO-01",
            ),
            Product(
                sku="KDA-WHEY-CHOC-003",
                name="KODA Whey Chocolate Cremoso",
                category="protein",
                flavor="chocolate",
                price_brl=149.90,
                stock_units=75,
                tags=["contém_lactose", "alto_proteina"],
                contraindications=["intolerancia_lactose"],
                benefits=["proteína rápida", "sabor intenso"],
                fulfillment_center="SP-CENTRO-01",
            ),
            Product(
                sku="KDA-PRE-CHOC-004",
                name="KODA Pré-Treino Chocolate Nitro",
                category="pre_workout",
                flavor="chocolate",
                price_brl=169.90,
                stock_units=0,
                tags=["sem_lactose", "alto_estimulo"],
                contraindications=["sensibilidade_alta_a_cafeina"],
                benefits=["energia alta", "pump"],
                fulfillment_center="SP-CENTRO-02",
            ),
        ]

    def run(self, store: StateStore, attempt: int) -> str:
        profile_data = store.read_json("customer_profile.json")
        restrictions = set(profile_data.get("dietary_restrictions", []))
        budget = float(profile_data.get("budget_brl", 0))
        flavor = str(profile_data.get("preferred_flavor", "")).lower()
        filtered: List[Product] = []
        unavailable: List[str] = []
        for product in self.catalog:
            if product.stock_units <= 0:
                unavailable.append(product.sku)
                continue
            if product.price_brl > budget:
                continue
            if flavor and product.flavor != flavor:
                continue
            if "sem_lactose" in restrictions and "contém_lactose" in product.tags:
                continue
            if product.category != "pre_workout":
                continue
            filtered.append(product)
        snapshot = CatalogSnapshot(
            conversation_id=str(profile_data["customer_id"]),
            products=filtered,
            filtered_skus=[product.sku for product in filtered],
            unavailable_skus=unavailable,
            inventory_checked_at=utc_now(),
            pricing_checked_at=utc_now(),
            notes=[
                "catálogo filtrado por restrição sem lactose",
                "catálogo filtrado por orçamento máximo",
                "catálogo filtrado por sabor chocolate",
                "produtos sem estoque foram excluídos antes da recomendação",
            ],
        )
        if not filtered:
            raise AgentExecutionError("Nenhum produto seguro encontrado no catálogo")
        store.write_json("catalog_snapshot.json", snapshot)
        return "catalog_snapshot.json"


class RecommendationAgent:
    stage = StageName.GENERATOR

    def run(self, store: StateStore, attempt: int) -> str:
        profile = store.read_json("customer_profile.json")
        catalog = store.read_json("catalog_snapshot.json")
        feedback = []
        if store.exists("evaluation_verdict.json"):
            feedback = list(store.read_json("evaluation_verdict.json").get("feedback_for_generator", []))
        products = catalog.get("products", [])
        if not isinstance(products, list) or not products:
            raise AgentExecutionError("Generator não recebeu produtos elegíveis")
        selected = products[0]
        item = RecommendationItem(
            sku=str(selected["sku"]),
            name=str(selected["name"]),
            quantity=1,
            unit_price_brl=float(selected["price_brl"]),
            reason="melhor combinação entre sabor chocolate, ausência de lactose, preço e estoque em São Paulo",
            customer_fit=[
                "respeita o limite de R$ 150",
                "não contém lactose",
                "tem sabor chocolate",
                "serve para pré-treino no fim da tarde",
            ],
            cautions=list(selected.get("contraindications", [])),
        )
        total = item.unit_price_brl * item.quantity
        message = (
            f"Marina, encontrei uma opção segura para o que você pediu: {item.name}. "
            f"Ela é sem lactose, sabor chocolate, está em estoque e fica em {money(total)}. "
            "Eu recomendo essa porque entrega energia gradual para o treino sem sair do seu orçamento. "
            "Quer que eu monte o carrinho e deixe o Pix pronto?"
        )
        if attempt == 1 and not feedback:
            message = (
                f"Marina, recomendo {item.name}. Fica em {money(total)} e combina com seu treino. "
                "Posso colocar no carrinho?"
            )
        draft = RecommendationDraft(
            conversation_id=str(profile["customer_id"]),
            attempt=attempt,
            headline="Recomendação principal de pré-treino para Marina",
            items=[item],
            total_brl=total,
            customer_message=message,
            evidence=[
                "SKU presente em catalog_snapshot.json",
                "preço abaixo do orçamento declarado",
                "tag sem_lactose presente no produto selecionado",
                "sabor igual ao preferido pela cliente",
            ],
            evaluator_feedback_used=feedback,
        )
        store.write_json("recommendation_draft.json", draft)
        return "recommendation_draft.json"


class QualityAgent:
    stage = StageName.EVALUATOR

    def run(self, store: StateStore, attempt: int) -> str:
        profile = store.read_json("customer_profile.json")
        draft = store.read_json("recommendation_draft.json")
        catalog = store.read_json("catalog_snapshot.json")
        checks = QualityChecks(profile, catalog, draft)
        results = [
            checks.check_budget(),
            checks.check_lactose_safety(),
            checks.check_stock(),
            checks.check_flavor_alignment(),
            checks.check_whatsapp_clarity(),
            checks.check_evidence(),
            checks.check_next_step(),
        ]
        passed = [name for name, ok, _score, _feedback in results if ok]
        failed = [name for name, ok, _score, _feedback in results if not ok]
        feedback = [feedback for _name, ok, _score, feedback in results if not ok]
        score = round(sum(score for _name, _ok, score, _feedback in results) / len(results), 3)
        required = 0.86
        verdict = Verdict.APPROVED if score >= required and not failed else Verdict.REJECTED
        evaluation = EvaluationVerdict(
            conversation_id=str(profile["customer_id"]),
            attempt=attempt,
            verdict=verdict,
            score=score,
            required_score=required,
            passed_checks=passed,
            failed_checks=failed,
            feedback_for_generator=feedback,
        )
        store.write_json("evaluation_verdict.json", evaluation)
        return "evaluation_verdict.json"


class QualityChecks:
    def __init__(self, profile: Dict[str, Any], catalog: Dict[str, Any], draft: Dict[str, Any]) -> None:
        self.profile = profile
        self.catalog = catalog
        self.draft = draft

    def check_budget(self) -> Tuple[str, bool, float, str]:
        budget = float(self.profile.get("budget_brl", 0))
        total = float(self.draft.get("total_brl", 999999))
        ok = total <= budget
        return "orçamento", ok, 1.0 if ok else 0.0, "reduzir o carrinho para caber no orçamento declarado"

    def check_lactose_safety(self) -> Tuple[str, bool, float, str]:
        restrictions = set(self.profile.get("dietary_restrictions", []))
        text = str(self.draft.get("customer_message", "")).lower()
        ok = "sem_lactose" not in restrictions or "sem lactose" in text
        return "segurança sem lactose", ok, 1.0 if ok else 0.0, "explicitar que o produto recomendado é sem lactose"

    def check_stock(self) -> Tuple[str, bool, float, str]:
        skus = set(self.catalog.get("filtered_skus", []))
        items = self.draft.get("items", [])
        ok = all(item.get("sku") in skus for item in items)
        return "estoque", ok, 1.0 if ok else 0.0, "usar apenas SKUs presentes no snapshot filtrado"

    def check_flavor_alignment(self) -> Tuple[str, bool, float, str]:
        flavor = str(self.profile.get("preferred_flavor", "")).lower()
        message = str(self.draft.get("customer_message", "")).lower()
        ok = not flavor or flavor in message
        return "sabor preferido", ok, 1.0 if ok else 0.3, "mencionar sabor chocolate na recomendação"

    def check_whatsapp_clarity(self) -> Tuple[str, bool, float, str]:
        message = str(self.draft.get("customer_message", ""))
        ok = 80 <= len(message) <= 700 and "?" in message
        return "clareza no WhatsApp", ok, 1.0 if ok else 0.6, "encerrar com uma pergunta clara de próxima ação"

    def check_evidence(self) -> Tuple[str, bool, float, str]:
        evidence = self.draft.get("evidence", [])
        ok = isinstance(evidence, list) and len(evidence) >= 3
        return "evidência", ok, 1.0 if ok else 0.5, "registrar pelo menos três evidências da escolha"

    def check_next_step(self) -> Tuple[str, bool, float, str]:
        message = str(self.draft.get("customer_message", "")).lower()
        ok = "carrinho" in message or "confirmar" in message or "pix" in message
        return "próximo passo", ok, 1.0 if ok else 0.4, "deixar claro como a cliente avança para o carrinho"


class OrderAgent:
    stage = StageName.ORDER

    def run(self, store: StateStore, attempt: int) -> str:
        draft = store.read_json("recommendation_draft.json")
        evaluation = store.read_json("evaluation_verdict.json")
        profile = store.read_json("customer_profile.json")
        if evaluation.get("verdict") != Verdict.APPROVED.value:
            raise AgentExecutionError("Order bloqueado porque a recomendação não foi aprovada")
        items = [RecommendationItem(**item) for item in draft.get("items", [])]
        subtotal = float(draft.get("total_brl", 0))
        shipping = 0.0
        order = OrderState(
            conversation_id=str(profile["customer_id"]),
            order_id=f"KDA-{uuid.uuid4().hex[:6].upper()}",
            customer_id=str(profile["customer_id"]),
            items=items,
            subtotal_brl=subtotal,
            shipping_brl=shipping,
            total_brl=subtotal + shipping,
            shipping_address="Rua Harmonia, 150, ap 42, Vila Madalena, São Paulo, SP",
            status="confirmed",
        )
        store.write_json("order_state.json", order)
        return "order_state.json"


class PaymentAgent:
    stage = StageName.PAYMENT

    def run(self, store: StateStore, attempt: int) -> str:
        order = store.read_json("order_state.json")
        profile = store.read_json("customer_profile.json")
        amount = float(order["total_brl"])
        method = PaymentMethod(str(profile.get("preferred_payment_method", PaymentMethod.PIX.value)))
        if amount <= 0:
            raise PaymentDeclinedError("Valor de pagamento inválido")
        payment = PaymentState(
            conversation_id=str(order["conversation_id"]),
            order_id=str(order["order_id"]),
            payment_id=f"pay_{uuid.uuid4().hex[:10]}",
            method=method,
            amount_brl=amount,
            status="confirmed",
            provider_reference=f"pix_sim_{uuid.uuid4().hex[:8]}",
            confirmed_at=utc_now(),
        )
        store.write_json("payment_state.json", payment)
        return "payment_state.json"


class FulfillmentAgent:
    stage = StageName.FULFILLMENT

    def run(self, store: StateStore, attempt: int) -> str:
        order = store.read_json("order_state.json")
        payment = store.read_json("payment_state.json")
        if payment.get("status") != "confirmed":
            raise AgentExecutionError("Fulfillment bloqueado sem pagamento confirmado")
        tracking = f"BR{random.randint(100000000, 999999999)}KDA"
        state = FulfillmentState(
            conversation_id=str(order["conversation_id"]),
            order_id=str(order["order_id"]),
            warehouse_ticket=f"wh_{uuid.uuid4().hex[:8]}",
            carrier="KODA Express SP",
            tracking_code=tracking,
            status="separating",
            estimated_delivery_date="2026-05-30",
            customer_notification=(
                f"Marina, pagamento confirmado e pedido {order['order_id']} em separação. "
                f"Seu rastreio é {tracking}. Entrega prevista para 30/05."
            ),
        )
        store.write_json("fulfillment_state.json", state)
        return "fulfillment_state.json"


class FallbackHandlers:
    def __init__(self, store: StateStore) -> None:
        self.store = store

    def discovery(self, error: Exception) -> str:
        message = self.store.read_json("customer_message.json")
        profile = CustomerProfile(
            customer_id=str(message["customer_id"]),
            name=str(message["customer_name"]),
            goal="suplemento esportivo",
            dietary_restrictions=["sem_lactose"],
            budget_brl=150.0,
            preferred_flavor="chocolate",
            preferred_payment_method=PaymentMethod.PIX,
            training_context="contexto mínimo inferido pela conversa",
            confidence=0.70,
            evidence=["fallback conservador aplicado após falha de Discovery"],
        )
        state = DiscoveryState(
            conversation_id=str(message["conversation_id"]),
            extracted_profile=profile,
            missing_fields=[],
            confidence_by_field={"fallback": 0.70},
            next_questions=[],
            stage_score=0.70,
        )
        self.store.write_json("customer_profile.json", profile)
        self.store.write_json("discovery_state.json", state)
        return "discovery_state.json"

    def catalog(self, error: Exception) -> str:
        product = Product(
            sku="KDA-PRE-CHOC-001",
            name="KODA Pré-Treino Cacao Focus sem Lactose",
            category="pre_workout",
            flavor="chocolate",
            price_brl=129.90,
            stock_units=1,
            tags=["sem_lactose", "vegano", "baixo_acucar"],
            contraindications=["sensibilidade_alta_a_cafeina"],
            benefits=["energia para treino", "boa digestibilidade"],
            fulfillment_center="SP-CENTRO-01",
        )
        snapshot = CatalogSnapshot(
            conversation_id="fallback_catalog",
            products=[product],
            filtered_skus=[product.sku],
            unavailable_skus=[],
            inventory_checked_at=utc_now(),
            pricing_checked_at=utc_now(),
            notes=["fallback de catálogo com SKU seguro e validado manualmente"],
        )
        self.store.write_json("catalog_snapshot.json", snapshot)
        return "catalog_snapshot.json"

    def generator(self, error: Exception) -> str:
        item = RecommendationItem(
            sku="KDA-PRE-CHOC-001",
            name="KODA Pré-Treino Cacao Focus sem Lactose",
            quantity=1,
            unit_price_brl=129.90,
            reason="SKU seguro usado como fallback conservador",
            customer_fit=["sem lactose", "sabor chocolate", "abaixo de R$ 150"],
            cautions=["sensibilidade_alta_a_cafeina"],
        )
        draft = RecommendationDraft(
            conversation_id="fallback_generator",
            attempt=99,
            headline="Recomendação conservadora de fallback",
            items=[item],
            total_brl=129.90,
            customer_message=(
                "Marina, para manter segurança, vou recomendar apenas o Pré-Treino Cacao Focus sem Lactose. "
                "Ele é sabor chocolate, está abaixo de R$ 150 e posso montar o carrinho se você confirmar."
            ),
            evidence=["fallback seguro", "SKU sem lactose", "preço abaixo do orçamento"],
            evaluator_feedback_used=["fallback acionado pelo orquestrador"],
        )
        self.store.write_json("recommendation_draft.json", draft)
        return "recommendation_draft.json"

    def evaluator(self, error: Exception) -> str:
        verdict = EvaluationVerdict(
            conversation_id="fallback_evaluator",
            attempt=99,
            verdict=Verdict.FALLBACK,
            score=0.0,
            required_score=0.86,
            passed_checks=[],
            failed_checks=["avaliação automática indisponível"],
            feedback_for_generator=["bloquear envio automático e pedir revisão humana"],
        )
        self.store.write_json("evaluation_verdict.json", verdict)
        return "evaluation_verdict.json"

    def order(self, error: Exception) -> str:
        raise AgentExecutionError(f"Pedido não pode seguir sem aprovação válida: {error}")

    def payment(self, error: Exception) -> str:
        order = self.store.read_json("order_state.json")
        payment = PaymentState(
            conversation_id=str(order["conversation_id"]),
            order_id=str(order["order_id"]),
            payment_id=f"manual_{uuid.uuid4().hex[:8]}",
            method=PaymentMethod.PIX,
            amount_brl=float(order["total_brl"]),
            status="manual_review",
            provider_reference="pix_manual_review",
            confirmed_at=None,
        )
        self.store.write_json("payment_state.json", payment)
        return "payment_state.json"

    def fulfillment(self, error: Exception) -> str:
        order = self.store.read_json("order_state.json")
        state = FulfillmentState(
            conversation_id=str(order["conversation_id"]),
            order_id=str(order["order_id"]),
            warehouse_ticket=f"manual_wh_{uuid.uuid4().hex[:6]}",
            carrier="separação manual",
            tracking_code="aguardando_rastreio",
            status="manual_review",
            estimated_delivery_date="confirmar com operação",
            customer_notification="Marina, seu pedido foi recebido e nossa operação está confirmando o envio manualmente.",
        )
        self.store.write_json("fulfillment_state.json", state)
        return "fulfillment_state.json"


class PipelineOrchestrator:
    def __init__(self, state_dir: Path, max_retries: int = 3) -> None:
        self.store = StateStore(state_dir)
        self.max_retries = max_retries
        self.metrics: List[StageMetric] = []
        self.fallbacks = FallbackHandlers(self.store)

    def execute_agent(self, agent: Agent, output_file: str) -> str:
        last_error: Optional[Exception] = None
        for attempt in range(1, self.max_retries + 1):
            started = time.perf_counter()
            try:
                result_file = agent.run(self.store, attempt)
                latency = int((time.perf_counter() - started) * 1000)
                self.metrics.append(StageMetric(agent.stage, attempt, latency, "success", self._score_for(result_file), result_file))
                return result_file
            except Exception as error:
                last_error = error
                latency = int((time.perf_counter() - started) * 1000)
                self.metrics.append(StageMetric(agent.stage, attempt, latency, "retry", None, output_file))
        fallback_file = self.apply_fallback(agent.stage, last_error or AgentExecutionError("falha desconhecida"))
        self.metrics.append(StageMetric(agent.stage, self.max_retries + 1, 0, "fallback", self._score_for(fallback_file), fallback_file))
        return fallback_file

    def apply_fallback(self, stage: StageName, error: Exception) -> str:
        handlers: Dict[StageName, Callable[[Exception], str]] = {
            StageName.DISCOVERY: self.fallbacks.discovery,
            StageName.CATALOG: self.fallbacks.catalog,
            StageName.GENERATOR: self.fallbacks.generator,
            StageName.EVALUATOR: self.fallbacks.evaluator,
            StageName.ORDER: self.fallbacks.order,
            StageName.PAYMENT: self.fallbacks.payment,
            StageName.FULFILLMENT: self.fallbacks.fulfillment,
        }
        handler = handlers.get(stage)
        if handler is None:
            raise AgentExecutionError(f"Sem fallback definido para {stage.value}") from error
        return handler(error)

    def run(self, message: CustomerMessage) -> PipelineResult:
        self.execute_agent(PlannerAgent(message), "plan.json")
        self.execute_agent(DiscoveryAgent(), "discovery_state.json")
        self.execute_agent(CatalogAgent(), "catalog_snapshot.json")
        approved = False
        final_evaluation: Optional[EvaluationVerdict] = None
        final_draft: Optional[RecommendationDraft] = None
        for attempt in range(1, self.max_retries + 1):
            self.execute_agent(RecommendationAgent(), "recommendation_draft.json")
            self.execute_agent(QualityAgent(), "evaluation_verdict.json")
            evaluation_data = self.store.read_json("evaluation_verdict.json")
            draft_data = self.store.read_json("recommendation_draft.json")
            final_evaluation = EvaluationVerdict(
                conversation_id=str(evaluation_data["conversation_id"]),
                attempt=int(evaluation_data["attempt"]),
                verdict=Verdict(str(evaluation_data["verdict"])),
                score=float(evaluation_data["score"]),
                required_score=float(evaluation_data["required_score"]),
                passed_checks=list(evaluation_data["passed_checks"]),
                failed_checks=list(evaluation_data["failed_checks"]),
                feedback_for_generator=list(evaluation_data["feedback_for_generator"]),
                created_at=str(evaluation_data["created_at"]),
            )
            final_draft = self._draft_from_json(draft_data)
            if final_evaluation.verdict == Verdict.APPROVED:
                approved = True
                break
        if not approved or final_evaluation is None or final_draft is None:
            raise AgentExecutionError("Recomendação não aprovada após tentativas permitidas")
        self.execute_agent(OrderAgent(), "order_state.json")
        self.execute_agent(PaymentAgent(), "payment_state.json")
        self.execute_agent(FulfillmentAgent(), "fulfillment_state.json")
        order = self._order_from_json(self.store.read_json("order_state.json"))
        payment = self._payment_from_json(self.store.read_json("payment_state.json"))
        fulfillment = self._fulfillment_from_json(self.store.read_json("fulfillment_state.json"))
        return PipelineResult(
            conversation_id=message.conversation_id,
            final_phase=JourneyPhase.CLOSED,
            approved_recommendation=final_draft,
            evaluation=final_evaluation,
            order=order,
            payment=payment,
            fulfillment=fulfillment,
            metrics=self.metrics,
        )

    def _score_for(self, filename: str) -> Optional[float]:
        if not self.store.exists(filename):
            return None
        data = self.store.read_json(filename)
        for key in ("stage_score", "score"):
            if key in data:
                return float(data[key])
        return None

    def _draft_from_json(self, data: Dict[str, Any]) -> RecommendationDraft:
        return RecommendationDraft(
            conversation_id=str(data["conversation_id"]),
            attempt=int(data["attempt"]),
            headline=str(data["headline"]),
            items=[RecommendationItem(**item) for item in data["items"]],
            total_brl=float(data["total_brl"]),
            customer_message=str(data["customer_message"]),
            evidence=list(data["evidence"]),
            evaluator_feedback_used=list(data["evaluator_feedback_used"]),
            created_at=str(data["created_at"]),
        )

    def _order_from_json(self, data: Dict[str, Any]) -> OrderState:
        return OrderState(
            conversation_id=str(data["conversation_id"]),
            order_id=str(data["order_id"]),
            customer_id=str(data["customer_id"]),
            items=[RecommendationItem(**item) for item in data["items"]],
            subtotal_brl=float(data["subtotal_brl"]),
            shipping_brl=float(data["shipping_brl"]),
            total_brl=float(data["total_brl"]),
            shipping_address=str(data["shipping_address"]),
            status=str(data["status"]),
            created_at=str(data["created_at"]),
        )

    def _payment_from_json(self, data: Dict[str, Any]) -> PaymentState:
        return PaymentState(
            conversation_id=str(data["conversation_id"]),
            order_id=str(data["order_id"]),
            payment_id=str(data["payment_id"]),
            method=PaymentMethod(str(data["method"])),
            amount_brl=float(data["amount_brl"]),
            status=str(data["status"]),
            provider_reference=str(data["provider_reference"]),
            confirmed_at=data.get("confirmed_at"),
        )

    def _fulfillment_from_json(self, data: Dict[str, Any]) -> FulfillmentState:
        return FulfillmentState(
            conversation_id=str(data["conversation_id"]),
            order_id=str(data["order_id"]),
            warehouse_ticket=str(data["warehouse_ticket"]),
            carrier=str(data["carrier"]),
            tracking_code=str(data["tracking_code"]),
            status=str(data["status"]),
            estimated_delivery_date=str(data["estimated_delivery_date"]),
            customer_notification=str(data["customer_notification"]),
            created_at=str(data["created_at"]),
        )


def print_result(result: PipelineResult) -> None:
    print("Resumo da jornada KODA")
    print(f"Conversa: {result.conversation_id}")
    print(f"Fase final: {result.final_phase.value}")
    print(f"Pedido: {result.order.order_id}")
    print(f"Pagamento: {result.payment.status} em {money(result.payment.amount_brl)}")
    print(f"Fulfillment: {result.fulfillment.status} com rastreio {result.fulfillment.tracking_code}")
    print("Mensagem final ao cliente:")
    print(result.fulfillment.customer_notification)
    print("Métricas por etapa:")
    for metric in result.metrics:
        print(f"{metric.stage.value}: tentativa {metric.attempt}, status {metric.status}, latência {metric.latency_ms} ms")


def main() -> None:
    state_dir = Path("state/marina_pre_treino")
    message = CustomerMessage(
        conversation_id="wa_marina_2026_05_28_001",
        customer_id="cust_marina_001",
        customer_name="Marina",
        text=(
            "Oi KODA, quero um pré-treino sem lactose. "
            "Meu orçamento é R$ 150 e eu prefiro sabor chocolate. "
            "Treino depois do trabalho e quero algo que não pese no estômago."
        ),
    )
    orchestrator = PipelineOrchestrator(state_dir=state_dir, max_retries=3)
    result = orchestrator.run(message)
    print_result(result)


if __name__ == "__main__":
    main()
```

---

## ✅ Avaliação de Qualidade por Etapa

Uma jornada KODA não pode ter avaliação somente no final.
Quando o erro aparece no pagamento, a causa pode estar no Discovery.
Quando o fulfillment falha, a causa pode estar em um SKU errado no Catalog.
Por isso, cada etapa tem rubrica própria, score próprio e checks próprios.

### Rubricas principais

| Etapa | Score mínimo | Checks obrigatórios | Rejeição automática |
|---|---:|---|---|
| Planner | 0.90 | fases completas, arquivos esperados, fallback definido | plano sem Payment ou Fulfillment |
| Discovery | 0.85 | objetivo, restrição, orçamento, sabor, evidência | restrição alimentar ausente quando cliente informou |
| Catalog | 0.95 | estoque, preço, tags, contraindicações, SKU válido | produto com lactose para cliente sem lactose |
| Generator | 0.86 | clareza, personalização, evidência, próximo passo | recomendação acima do orçamento |
| Evaluator | 0.86 | checks de segurança, preço, estoque, tom e evidência | qualquer falha crítica |
| Order | 0.98 | SKU aprovado, total correto, endereço, status | item diferente da recomendação aprovada |
| Payment | 0.99 | valor, método, confirmação, referência | status confirmado sem referência |
| Fulfillment | 0.95 | ticket, transportadora, rastreio, aviso | fulfillment sem pagamento confirmado |

### Funções de check usadas pelo Evaluator

```python
def check_budget(profile: dict, draft: dict) -> tuple[str, bool, float, str]:
    budget = float(profile["budget_brl"])
    total = float(draft["total_brl"])
    if total <= budget:
        return "orçamento", True, 1.0, "preço dentro do limite declarado"
    return "orçamento", False, 0.0, "reduzir carrinho para respeitar orçamento"

def check_lactose_safety(profile: dict, draft: dict) -> tuple[str, bool, float, str]:
    restrictions = set(profile.get("dietary_restrictions", []))
    message = draft.get("customer_message", "").lower()
    if "sem_lactose" not in restrictions:
        return "segurança sem lactose", True, 1.0, "restrição não aplicável"
    if "sem lactose" in message:
        return "segurança sem lactose", True, 1.0, "restrição explicitada"
    return "segurança sem lactose", False, 0.0, "mencionar que o SKU é sem lactose"

def check_stock(catalog: dict, draft: dict) -> tuple[str, bool, float, str]:
    allowed = set(catalog.get("filtered_skus", []))
    items = draft.get("items", [])
    if all(item.get("sku") in allowed for item in items):
        return "estoque", True, 1.0, "todos os itens vieram do snapshot filtrado"
    return "estoque", False, 0.0, "remover SKU fora do snapshot aprovado"

def check_next_step(draft: dict) -> tuple[str, bool, float, str]:
    message = draft.get("customer_message", "").lower()
    if "carrinho" in message or "confirmar" in message or "pix" in message:
        return "próximo passo", True, 1.0, "cliente sabe como avançar"
    return "próximo passo", False, 0.4, "encerrar com pergunta clara para avançar"
```

### Interpretação dos scores

| Faixa | Interpretação | Ação do Orchestrator |
|---|---|---|
| 0.98 a 1.00 | Excelente, pronto para seguir | Avança sem ajuste |
| 0.90 a 0.97 | Bom, com pequenas observações | Avança se não houver falha crítica |
| 0.86 a 0.89 | Aceitável no Generator e Evaluator | Avança com registro de risco leve |
| 0.70 a 0.85 | Incompleto | Retry com feedback |
| Abaixo de 0.70 | Perigoso | Fallback ou revisão humana |

### Rubrica detalhada, Planner

1. **Critério 1:** inclui todas as fases da jornada.
   Evidência esperada: o arquivo de estado da etapa Planner mostra esse dado de forma explícita.
   Falha típica: a etapa Planner tenta seguir usando inferência implícita em vez de estado persistido.
   Correção: repetir a etapa Planner com feedback específico antes de avançar.
2. **Critério 2:** define arquivos de saída.
   Evidência esperada: o arquivo de estado da etapa Planner mostra esse dado de forma explícita.
   Falha típica: a etapa Planner tenta seguir usando inferência implícita em vez de estado persistido.
   Correção: repetir a etapa Planner com feedback específico antes de avançar.
3. **Critério 3:** define max retries.
   Evidência esperada: o arquivo de estado da etapa Planner mostra esse dado de forma explícita.
   Falha típica: a etapa Planner tenta seguir usando inferência implícita em vez de estado persistido.
   Correção: repetir a etapa Planner com feedback específico antes de avançar.
4. **Critério 4:** define fallback por etapa.
   Evidência esperada: o arquivo de estado da etapa Planner mostra esse dado de forma explícita.
   Falha típica: a etapa Planner tenta seguir usando inferência implícita em vez de estado persistido.
   Correção: repetir a etapa Planner com feedback específico antes de avançar.
5. **Critério 5:** preserva constraints globais.
   Evidência esperada: o arquivo de estado da etapa Planner mostra esse dado de forma explícita.
   Falha típica: a etapa Planner tenta seguir usando inferência implícita em vez de estado persistido.
   Correção: repetir a etapa Planner com feedback específico antes de avançar.

### Rubrica detalhada, Discovery

1. **Critério 1:** captura nome da cliente.
   Evidência esperada: o arquivo de estado da etapa Discovery mostra esse dado de forma explícita.
   Falha típica: a etapa Discovery tenta seguir usando inferência implícita em vez de estado persistido.
   Correção: repetir a etapa Discovery com feedback específico antes de avançar.
2. **Critério 2:** captura objetivo de pré-treino.
   Evidência esperada: o arquivo de estado da etapa Discovery mostra esse dado de forma explícita.
   Falha típica: a etapa Discovery tenta seguir usando inferência implícita em vez de estado persistido.
   Correção: repetir a etapa Discovery com feedback específico antes de avançar.
3. **Critério 3:** captura sem lactose.
   Evidência esperada: o arquivo de estado da etapa Discovery mostra esse dado de forma explícita.
   Falha típica: a etapa Discovery tenta seguir usando inferência implícita em vez de estado persistido.
   Correção: repetir a etapa Discovery com feedback específico antes de avançar.
4. **Critério 4:** captura orçamento de R$ 150.
   Evidência esperada: o arquivo de estado da etapa Discovery mostra esse dado de forma explícita.
   Falha típica: a etapa Discovery tenta seguir usando inferência implícita em vez de estado persistido.
   Correção: repetir a etapa Discovery com feedback específico antes de avançar.
5. **Critério 5:** captura sabor chocolate.
   Evidência esperada: o arquivo de estado da etapa Discovery mostra esse dado de forma explícita.
   Falha típica: a etapa Discovery tenta seguir usando inferência implícita em vez de estado persistido.
   Correção: repetir a etapa Discovery com feedback específico antes de avançar.
6. **Critério 6:** registra evidências.
   Evidência esperada: o arquivo de estado da etapa Discovery mostra esse dado de forma explícita.
   Falha típica: a etapa Discovery tenta seguir usando inferência implícita em vez de estado persistido.
   Correção: repetir a etapa Discovery com feedback específico antes de avançar.

### Rubrica detalhada, Catalog

1. **Critério 1:** remove produtos sem estoque.
   Evidência esperada: o arquivo de estado da etapa Catalog mostra esse dado de forma explícita.
   Falha típica: a etapa Catalog tenta seguir usando inferência implícita em vez de estado persistido.
   Correção: repetir a etapa Catalog com feedback específico antes de avançar.
2. **Critério 2:** remove produtos com lactose.
   Evidência esperada: o arquivo de estado da etapa Catalog mostra esse dado de forma explícita.
   Falha típica: a etapa Catalog tenta seguir usando inferência implícita em vez de estado persistido.
   Correção: repetir a etapa Catalog com feedback específico antes de avançar.
3. **Critério 3:** remove produtos acima do orçamento.
   Evidência esperada: o arquivo de estado da etapa Catalog mostra esse dado de forma explícita.
   Falha típica: a etapa Catalog tenta seguir usando inferência implícita em vez de estado persistido.
   Correção: repetir a etapa Catalog com feedback específico antes de avançar.
4. **Critério 4:** remove produtos de categoria errada.
   Evidência esperada: o arquivo de estado da etapa Catalog mostra esse dado de forma explícita.
   Falha típica: a etapa Catalog tenta seguir usando inferência implícita em vez de estado persistido.
   Correção: repetir a etapa Catalog com feedback específico antes de avançar.
5. **Critério 5:** mantém apenas SKUs rastreáveis.
   Evidência esperada: o arquivo de estado da etapa Catalog mostra esse dado de forma explícita.
   Falha típica: a etapa Catalog tenta seguir usando inferência implícita em vez de estado persistido.
   Correção: repetir a etapa Catalog com feedback específico antes de avançar.

### Rubrica detalhada, Generator

1. **Critério 1:** cita nome da cliente.
   Evidência esperada: o arquivo de estado da etapa Generator mostra esse dado de forma explícita.
   Falha típica: a etapa Generator tenta seguir usando inferência implícita em vez de estado persistido.
   Correção: repetir a etapa Generator com feedback específico antes de avançar.
2. **Critério 2:** explica ajuste ao treino.
   Evidência esperada: o arquivo de estado da etapa Generator mostra esse dado de forma explícita.
   Falha típica: a etapa Generator tenta seguir usando inferência implícita em vez de estado persistido.
   Correção: repetir a etapa Generator com feedback específico antes de avançar.
3. **Critério 3:** menciona sem lactose.
   Evidência esperada: o arquivo de estado da etapa Generator mostra esse dado de forma explícita.
   Falha típica: a etapa Generator tenta seguir usando inferência implícita em vez de estado persistido.
   Correção: repetir a etapa Generator com feedback específico antes de avançar.
4. **Critério 4:** menciona preço.
   Evidência esperada: o arquivo de estado da etapa Generator mostra esse dado de forma explícita.
   Falha típica: a etapa Generator tenta seguir usando inferência implícita em vez de estado persistido.
   Correção: repetir a etapa Generator com feedback específico antes de avançar.
5. **Critério 5:** inclui pergunta de avanço.
   Evidência esperada: o arquivo de estado da etapa Generator mostra esse dado de forma explícita.
   Falha típica: a etapa Generator tenta seguir usando inferência implícita em vez de estado persistido.
   Correção: repetir a etapa Generator com feedback específico antes de avançar.

### Rubrica detalhada, Evaluator

1. **Critério 1:** calcula score médio.
   Evidência esperada: o arquivo de estado da etapa Evaluator mostra esse dado de forma explícita.
   Falha típica: a etapa Evaluator tenta seguir usando inferência implícita em vez de estado persistido.
   Correção: repetir a etapa Evaluator com feedback específico antes de avançar.
2. **Critério 2:** separa passed checks.
   Evidência esperada: o arquivo de estado da etapa Evaluator mostra esse dado de forma explícita.
   Falha típica: a etapa Evaluator tenta seguir usando inferência implícita em vez de estado persistido.
   Correção: repetir a etapa Evaluator com feedback específico antes de avançar.
3. **Critério 3:** separa failed checks.
   Evidência esperada: o arquivo de estado da etapa Evaluator mostra esse dado de forma explícita.
   Falha típica: a etapa Evaluator tenta seguir usando inferência implícita em vez de estado persistido.
   Correção: repetir a etapa Evaluator com feedback específico antes de avançar.
4. **Critério 4:** gera feedback acionável.
   Evidência esperada: o arquivo de estado da etapa Evaluator mostra esse dado de forma explícita.
   Falha típica: a etapa Evaluator tenta seguir usando inferência implícita em vez de estado persistido.
   Correção: repetir a etapa Evaluator com feedback específico antes de avançar.
5. **Critério 5:** bloqueia falha crítica.
   Evidência esperada: o arquivo de estado da etapa Evaluator mostra esse dado de forma explícita.
   Falha típica: a etapa Evaluator tenta seguir usando inferência implícita em vez de estado persistido.
   Correção: repetir a etapa Evaluator com feedback específico antes de avançar.

### Rubrica detalhada, Order

1. **Critério 1:** usa itens aprovados.
   Evidência esperada: o arquivo de estado da etapa Order mostra esse dado de forma explícita.
   Falha típica: a etapa Order tenta seguir usando inferência implícita em vez de estado persistido.
   Correção: repetir a etapa Order com feedback específico antes de avançar.
2. **Critério 2:** calcula subtotal.
   Evidência esperada: o arquivo de estado da etapa Order mostra esse dado de forma explícita.
   Falha típica: a etapa Order tenta seguir usando inferência implícita em vez de estado persistido.
   Correção: repetir a etapa Order com feedback específico antes de avançar.
3. **Critério 3:** calcula frete.
   Evidência esperada: o arquivo de estado da etapa Order mostra esse dado de forma explícita.
   Falha típica: a etapa Order tenta seguir usando inferência implícita em vez de estado persistido.
   Correção: repetir a etapa Order com feedback específico antes de avançar.
4. **Critério 4:** registra endereço.
   Evidência esperada: o arquivo de estado da etapa Order mostra esse dado de forma explícita.
   Falha típica: a etapa Order tenta seguir usando inferência implícita em vez de estado persistido.
   Correção: repetir a etapa Order com feedback específico antes de avançar.
5. **Critério 5:** gera order_id.
   Evidência esperada: o arquivo de estado da etapa Order mostra esse dado de forma explícita.
   Falha típica: a etapa Order tenta seguir usando inferência implícita em vez de estado persistido.
   Correção: repetir a etapa Order com feedback específico antes de avançar.

### Rubrica detalhada, Payment

1. **Critério 1:** confere valor.
   Evidência esperada: o arquivo de estado da etapa Payment mostra esse dado de forma explícita.
   Falha típica: a etapa Payment tenta seguir usando inferência implícita em vez de estado persistido.
   Correção: repetir a etapa Payment com feedback específico antes de avançar.
2. **Critério 2:** confere método Pix.
   Evidência esperada: o arquivo de estado da etapa Payment mostra esse dado de forma explícita.
   Falha típica: a etapa Payment tenta seguir usando inferência implícita em vez de estado persistido.
   Correção: repetir a etapa Payment com feedback específico antes de avançar.
3. **Critério 3:** gera referência.
   Evidência esperada: o arquivo de estado da etapa Payment mostra esse dado de forma explícita.
   Falha típica: a etapa Payment tenta seguir usando inferência implícita em vez de estado persistido.
   Correção: repetir a etapa Payment com feedback específico antes de avançar.
4. **Critério 4:** marca confirmação.
   Evidência esperada: o arquivo de estado da etapa Payment mostra esse dado de forma explícita.
   Falha típica: a etapa Payment tenta seguir usando inferência implícita em vez de estado persistido.
   Correção: repetir a etapa Payment com feedback específico antes de avançar.
5. **Critério 5:** bloqueia valor inválido.
   Evidência esperada: o arquivo de estado da etapa Payment mostra esse dado de forma explícita.
   Falha típica: a etapa Payment tenta seguir usando inferência implícita em vez de estado persistido.
   Correção: repetir a etapa Payment com feedback específico antes de avançar.

### Rubrica detalhada, Fulfillment

1. **Critério 1:** cria ticket de armazém.
   Evidência esperada: o arquivo de estado da etapa Fulfillment mostra esse dado de forma explícita.
   Falha típica: a etapa Fulfillment tenta seguir usando inferência implícita em vez de estado persistido.
   Correção: repetir a etapa Fulfillment com feedback específico antes de avançar.
2. **Critério 2:** gera rastreio.
   Evidência esperada: o arquivo de estado da etapa Fulfillment mostra esse dado de forma explícita.
   Falha típica: a etapa Fulfillment tenta seguir usando inferência implícita em vez de estado persistido.
   Correção: repetir a etapa Fulfillment com feedback específico antes de avançar.
3. **Critério 3:** define transportadora.
   Evidência esperada: o arquivo de estado da etapa Fulfillment mostra esse dado de forma explícita.
   Falha típica: a etapa Fulfillment tenta seguir usando inferência implícita em vez de estado persistido.
   Correção: repetir a etapa Fulfillment com feedback específico antes de avançar.
4. **Critério 4:** define entrega prevista.
   Evidência esperada: o arquivo de estado da etapa Fulfillment mostra esse dado de forma explícita.
   Falha típica: a etapa Fulfillment tenta seguir usando inferência implícita em vez de estado persistido.
   Correção: repetir a etapa Fulfillment com feedback específico antes de avançar.
5. **Critério 5:** prepara notificação.
   Evidência esperada: o arquivo de estado da etapa Fulfillment mostra esse dado de forma explícita.
   Falha típica: a etapa Fulfillment tenta seguir usando inferência implícita em vez de estado persistido.
   Correção: repetir a etapa Fulfillment com feedback específico antes de avançar.

---

## 🚀 Aplicação KODA — Caso Concreto

Agora vamos percorrer a jornada completa de Marina.
O caso usa a mensagem obrigatória do exercício: cliente Marina quer um pré-treino sem lactose, orçamento de R$ 150 e preferência por chocolate.

### Entrada da conversa

```json
{
  "conversation_id": "wa_marina_2026_05_28_001",
  "customer_id": "cust_marina_001",
  "customer_name": "Marina",
  "channel": "whatsapp",
  "text": "Oi KODA, quero um pré-treino sem lactose. Meu orçamento é R$ 150 e eu prefiro sabor chocolate. Treino depois do trabalho e quero algo que não pese no estômago."
}
```

### Saída esperada de alto nível

```
awareness -> discovery -> recommendation -> cart -> payment -> fulfillment -> closed
```

### Etapa 1: Awareness

**Agente responsável:** Planner
**Entrada:** `customer_message.json`
**Saída:** `plan.json`
**Objetivo:** classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.

| Campo observado | Valor no caso Marina | Por que importa |
|---|---|---|
| Fase | Awareness | Mantém a jornada auditável |
| Agente | Planner | Garante responsabilidade única |
| Arquivo lido | `customer_message.json` | Evita dependência de memória implícita |
| Arquivo escrito | `plan.json` | Cria checkpoint para replay |
| Cliente | Marina | Permite personalização sem perder rastreio |
| Restrição | sem lactose | Bloqueia recomendação insegura |
| Orçamento | R$ 150 | Impede carrinho acima do limite |
| Preferência | chocolate | Aumenta aderência e confiança |

**Trace narrativo da etapa:**
1. Planner processa o sinal 1 da fase Awareness com foco em classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   O dado crítico é registrado em `plan.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Planner com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
2. Planner processa o sinal 2 da fase Awareness com foco em classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   O dado crítico é registrado em `plan.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Planner com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
3. Planner processa o sinal 3 da fase Awareness com foco em classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   O dado crítico é registrado em `plan.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Planner com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
4. Planner processa o sinal 4 da fase Awareness com foco em classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   O dado crítico é registrado em `plan.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Planner com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
5. Planner processa o sinal 5 da fase Awareness com foco em classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   O dado crítico é registrado em `plan.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Planner com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
6. Planner processa o sinal 6 da fase Awareness com foco em classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   O dado crítico é registrado em `plan.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Planner com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
7. Planner processa o sinal 7 da fase Awareness com foco em classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   O dado crítico é registrado em `plan.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Planner com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
8. Planner processa o sinal 8 da fase Awareness com foco em classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   O dado crítico é registrado em `plan.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Planner com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
9. Planner processa o sinal 9 da fase Awareness com foco em classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   O dado crítico é registrado em `plan.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Planner com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
10. Planner processa o sinal 10 da fase Awareness com foco em classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   O dado crítico é registrado em `plan.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Planner com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
11. Planner processa o sinal 11 da fase Awareness com foco em classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   O dado crítico é registrado em `plan.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Planner com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
12. Planner processa o sinal 12 da fase Awareness com foco em classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   O dado crítico é registrado em `plan.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Planner com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
13. Planner processa o sinal 13 da fase Awareness com foco em classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   O dado crítico é registrado em `plan.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Planner com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
14. Planner processa o sinal 14 da fase Awareness com foco em classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   O dado crítico é registrado em `plan.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Planner com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
15. Planner processa o sinal 15 da fase Awareness com foco em classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   O dado crítico é registrado em `plan.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Planner com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
16. Planner processa o sinal 16 da fase Awareness com foco em classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   O dado crítico é registrado em `plan.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Planner com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
17. Planner processa o sinal 17 da fase Awareness com foco em classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   O dado crítico é registrado em `plan.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Planner com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
18. Planner processa o sinal 18 da fase Awareness com foco em classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   O dado crítico é registrado em `plan.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Planner com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
19. Planner processa o sinal 19 da fase Awareness com foco em classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   O dado crítico é registrado em `plan.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Planner com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
20. Planner processa o sinal 20 da fase Awareness com foco em classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   O dado crítico é registrado em `plan.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Planner com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.

### Etapa 2: Discovery

**Agente responsável:** Discovery Agent
**Entrada:** `customer_message.json`
**Saída:** `customer_profile.json`
**Objetivo:** extrair objetivo, restrição sem lactose, orçamento e sabor.

| Campo observado | Valor no caso Marina | Por que importa |
|---|---|---|
| Fase | Discovery | Mantém a jornada auditável |
| Agente | Discovery Agent | Garante responsabilidade única |
| Arquivo lido | `customer_message.json` | Evita dependência de memória implícita |
| Arquivo escrito | `customer_profile.json` | Cria checkpoint para replay |
| Cliente | Marina | Permite personalização sem perder rastreio |
| Restrição | sem lactose | Bloqueia recomendação insegura |
| Orçamento | R$ 150 | Impede carrinho acima do limite |
| Preferência | chocolate | Aumenta aderência e confiança |

**Trace narrativo da etapa:**
1. Discovery Agent processa o sinal 1 da fase Discovery com foco em extrair objetivo, restrição sem lactose, orçamento e sabor.
   O dado crítico é registrado em `customer_profile.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Discovery Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
2. Discovery Agent processa o sinal 2 da fase Discovery com foco em extrair objetivo, restrição sem lactose, orçamento e sabor.
   O dado crítico é registrado em `customer_profile.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Discovery Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
3. Discovery Agent processa o sinal 3 da fase Discovery com foco em extrair objetivo, restrição sem lactose, orçamento e sabor.
   O dado crítico é registrado em `customer_profile.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Discovery Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
4. Discovery Agent processa o sinal 4 da fase Discovery com foco em extrair objetivo, restrição sem lactose, orçamento e sabor.
   O dado crítico é registrado em `customer_profile.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Discovery Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
5. Discovery Agent processa o sinal 5 da fase Discovery com foco em extrair objetivo, restrição sem lactose, orçamento e sabor.
   O dado crítico é registrado em `customer_profile.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Discovery Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
6. Discovery Agent processa o sinal 6 da fase Discovery com foco em extrair objetivo, restrição sem lactose, orçamento e sabor.
   O dado crítico é registrado em `customer_profile.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Discovery Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
7. Discovery Agent processa o sinal 7 da fase Discovery com foco em extrair objetivo, restrição sem lactose, orçamento e sabor.
   O dado crítico é registrado em `customer_profile.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Discovery Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
8. Discovery Agent processa o sinal 8 da fase Discovery com foco em extrair objetivo, restrição sem lactose, orçamento e sabor.
   O dado crítico é registrado em `customer_profile.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Discovery Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
9. Discovery Agent processa o sinal 9 da fase Discovery com foco em extrair objetivo, restrição sem lactose, orçamento e sabor.
   O dado crítico é registrado em `customer_profile.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Discovery Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
10. Discovery Agent processa o sinal 10 da fase Discovery com foco em extrair objetivo, restrição sem lactose, orçamento e sabor.
   O dado crítico é registrado em `customer_profile.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Discovery Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
11. Discovery Agent processa o sinal 11 da fase Discovery com foco em extrair objetivo, restrição sem lactose, orçamento e sabor.
   O dado crítico é registrado em `customer_profile.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Discovery Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
12. Discovery Agent processa o sinal 12 da fase Discovery com foco em extrair objetivo, restrição sem lactose, orçamento e sabor.
   O dado crítico é registrado em `customer_profile.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Discovery Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
13. Discovery Agent processa o sinal 13 da fase Discovery com foco em extrair objetivo, restrição sem lactose, orçamento e sabor.
   O dado crítico é registrado em `customer_profile.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Discovery Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
14. Discovery Agent processa o sinal 14 da fase Discovery com foco em extrair objetivo, restrição sem lactose, orçamento e sabor.
   O dado crítico é registrado em `customer_profile.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Discovery Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
15. Discovery Agent processa o sinal 15 da fase Discovery com foco em extrair objetivo, restrição sem lactose, orçamento e sabor.
   O dado crítico é registrado em `customer_profile.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Discovery Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
16. Discovery Agent processa o sinal 16 da fase Discovery com foco em extrair objetivo, restrição sem lactose, orçamento e sabor.
   O dado crítico é registrado em `customer_profile.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Discovery Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
17. Discovery Agent processa o sinal 17 da fase Discovery com foco em extrair objetivo, restrição sem lactose, orçamento e sabor.
   O dado crítico é registrado em `customer_profile.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Discovery Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
18. Discovery Agent processa o sinal 18 da fase Discovery com foco em extrair objetivo, restrição sem lactose, orçamento e sabor.
   O dado crítico é registrado em `customer_profile.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Discovery Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
19. Discovery Agent processa o sinal 19 da fase Discovery com foco em extrair objetivo, restrição sem lactose, orçamento e sabor.
   O dado crítico é registrado em `customer_profile.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Discovery Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
20. Discovery Agent processa o sinal 20 da fase Discovery com foco em extrair objetivo, restrição sem lactose, orçamento e sabor.
   O dado crítico é registrado em `customer_profile.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Discovery Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.

### Etapa 3: Catalog

**Agente responsável:** Catalog Agent
**Entrada:** `customer_profile.json`
**Saída:** `catalog_snapshot.json`
**Objetivo:** filtrar SKU seguro em estoque e abaixo de R$ 150.

| Campo observado | Valor no caso Marina | Por que importa |
|---|---|---|
| Fase | Catalog | Mantém a jornada auditável |
| Agente | Catalog Agent | Garante responsabilidade única |
| Arquivo lido | `customer_profile.json` | Evita dependência de memória implícita |
| Arquivo escrito | `catalog_snapshot.json` | Cria checkpoint para replay |
| Cliente | Marina | Permite personalização sem perder rastreio |
| Restrição | sem lactose | Bloqueia recomendação insegura |
| Orçamento | R$ 150 | Impede carrinho acima do limite |
| Preferência | chocolate | Aumenta aderência e confiança |

**Trace narrativo da etapa:**
1. Catalog Agent processa o sinal 1 da fase Catalog com foco em filtrar SKU seguro em estoque e abaixo de R$ 150.
   O dado crítico é registrado em `catalog_snapshot.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Catalog Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
2. Catalog Agent processa o sinal 2 da fase Catalog com foco em filtrar SKU seguro em estoque e abaixo de R$ 150.
   O dado crítico é registrado em `catalog_snapshot.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Catalog Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
3. Catalog Agent processa o sinal 3 da fase Catalog com foco em filtrar SKU seguro em estoque e abaixo de R$ 150.
   O dado crítico é registrado em `catalog_snapshot.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Catalog Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
4. Catalog Agent processa o sinal 4 da fase Catalog com foco em filtrar SKU seguro em estoque e abaixo de R$ 150.
   O dado crítico é registrado em `catalog_snapshot.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Catalog Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
5. Catalog Agent processa o sinal 5 da fase Catalog com foco em filtrar SKU seguro em estoque e abaixo de R$ 150.
   O dado crítico é registrado em `catalog_snapshot.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Catalog Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
6. Catalog Agent processa o sinal 6 da fase Catalog com foco em filtrar SKU seguro em estoque e abaixo de R$ 150.
   O dado crítico é registrado em `catalog_snapshot.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Catalog Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
7. Catalog Agent processa o sinal 7 da fase Catalog com foco em filtrar SKU seguro em estoque e abaixo de R$ 150.
   O dado crítico é registrado em `catalog_snapshot.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Catalog Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
8. Catalog Agent processa o sinal 8 da fase Catalog com foco em filtrar SKU seguro em estoque e abaixo de R$ 150.
   O dado crítico é registrado em `catalog_snapshot.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Catalog Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
9. Catalog Agent processa o sinal 9 da fase Catalog com foco em filtrar SKU seguro em estoque e abaixo de R$ 150.
   O dado crítico é registrado em `catalog_snapshot.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Catalog Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
10. Catalog Agent processa o sinal 10 da fase Catalog com foco em filtrar SKU seguro em estoque e abaixo de R$ 150.
   O dado crítico é registrado em `catalog_snapshot.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Catalog Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
11. Catalog Agent processa o sinal 11 da fase Catalog com foco em filtrar SKU seguro em estoque e abaixo de R$ 150.
   O dado crítico é registrado em `catalog_snapshot.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Catalog Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
12. Catalog Agent processa o sinal 12 da fase Catalog com foco em filtrar SKU seguro em estoque e abaixo de R$ 150.
   O dado crítico é registrado em `catalog_snapshot.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Catalog Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
13. Catalog Agent processa o sinal 13 da fase Catalog com foco em filtrar SKU seguro em estoque e abaixo de R$ 150.
   O dado crítico é registrado em `catalog_snapshot.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Catalog Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
14. Catalog Agent processa o sinal 14 da fase Catalog com foco em filtrar SKU seguro em estoque e abaixo de R$ 150.
   O dado crítico é registrado em `catalog_snapshot.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Catalog Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
15. Catalog Agent processa o sinal 15 da fase Catalog com foco em filtrar SKU seguro em estoque e abaixo de R$ 150.
   O dado crítico é registrado em `catalog_snapshot.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Catalog Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
16. Catalog Agent processa o sinal 16 da fase Catalog com foco em filtrar SKU seguro em estoque e abaixo de R$ 150.
   O dado crítico é registrado em `catalog_snapshot.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Catalog Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
17. Catalog Agent processa o sinal 17 da fase Catalog com foco em filtrar SKU seguro em estoque e abaixo de R$ 150.
   O dado crítico é registrado em `catalog_snapshot.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Catalog Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
18. Catalog Agent processa o sinal 18 da fase Catalog com foco em filtrar SKU seguro em estoque e abaixo de R$ 150.
   O dado crítico é registrado em `catalog_snapshot.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Catalog Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
19. Catalog Agent processa o sinal 19 da fase Catalog com foco em filtrar SKU seguro em estoque e abaixo de R$ 150.
   O dado crítico é registrado em `catalog_snapshot.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Catalog Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
20. Catalog Agent processa o sinal 20 da fase Catalog com foco em filtrar SKU seguro em estoque e abaixo de R$ 150.
   O dado crítico é registrado em `catalog_snapshot.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Catalog Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.

### Etapa 4: Recommendation

**Agente responsável:** Recommendation Agent
**Entrada:** `catalog_snapshot.json`
**Saída:** `recommendation_draft.json`
**Objetivo:** gerar mensagem de recomendação com justificativa humana.

| Campo observado | Valor no caso Marina | Por que importa |
|---|---|---|
| Fase | Recommendation | Mantém a jornada auditável |
| Agente | Recommendation Agent | Garante responsabilidade única |
| Arquivo lido | `catalog_snapshot.json` | Evita dependência de memória implícita |
| Arquivo escrito | `recommendation_draft.json` | Cria checkpoint para replay |
| Cliente | Marina | Permite personalização sem perder rastreio |
| Restrição | sem lactose | Bloqueia recomendação insegura |
| Orçamento | R$ 150 | Impede carrinho acima do limite |
| Preferência | chocolate | Aumenta aderência e confiança |

**Trace narrativo da etapa:**
1. Recommendation Agent processa o sinal 1 da fase Recommendation com foco em gerar mensagem de recomendação com justificativa humana.
   O dado crítico é registrado em `recommendation_draft.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Recommendation Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
2. Recommendation Agent processa o sinal 2 da fase Recommendation com foco em gerar mensagem de recomendação com justificativa humana.
   O dado crítico é registrado em `recommendation_draft.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Recommendation Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
3. Recommendation Agent processa o sinal 3 da fase Recommendation com foco em gerar mensagem de recomendação com justificativa humana.
   O dado crítico é registrado em `recommendation_draft.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Recommendation Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
4. Recommendation Agent processa o sinal 4 da fase Recommendation com foco em gerar mensagem de recomendação com justificativa humana.
   O dado crítico é registrado em `recommendation_draft.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Recommendation Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
5. Recommendation Agent processa o sinal 5 da fase Recommendation com foco em gerar mensagem de recomendação com justificativa humana.
   O dado crítico é registrado em `recommendation_draft.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Recommendation Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
6. Recommendation Agent processa o sinal 6 da fase Recommendation com foco em gerar mensagem de recomendação com justificativa humana.
   O dado crítico é registrado em `recommendation_draft.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Recommendation Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
7. Recommendation Agent processa o sinal 7 da fase Recommendation com foco em gerar mensagem de recomendação com justificativa humana.
   O dado crítico é registrado em `recommendation_draft.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Recommendation Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
8. Recommendation Agent processa o sinal 8 da fase Recommendation com foco em gerar mensagem de recomendação com justificativa humana.
   O dado crítico é registrado em `recommendation_draft.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Recommendation Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
9. Recommendation Agent processa o sinal 9 da fase Recommendation com foco em gerar mensagem de recomendação com justificativa humana.
   O dado crítico é registrado em `recommendation_draft.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Recommendation Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
10. Recommendation Agent processa o sinal 10 da fase Recommendation com foco em gerar mensagem de recomendação com justificativa humana.
   O dado crítico é registrado em `recommendation_draft.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Recommendation Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
11. Recommendation Agent processa o sinal 11 da fase Recommendation com foco em gerar mensagem de recomendação com justificativa humana.
   O dado crítico é registrado em `recommendation_draft.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Recommendation Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
12. Recommendation Agent processa o sinal 12 da fase Recommendation com foco em gerar mensagem de recomendação com justificativa humana.
   O dado crítico é registrado em `recommendation_draft.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Recommendation Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
13. Recommendation Agent processa o sinal 13 da fase Recommendation com foco em gerar mensagem de recomendação com justificativa humana.
   O dado crítico é registrado em `recommendation_draft.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Recommendation Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
14. Recommendation Agent processa o sinal 14 da fase Recommendation com foco em gerar mensagem de recomendação com justificativa humana.
   O dado crítico é registrado em `recommendation_draft.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Recommendation Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
15. Recommendation Agent processa o sinal 15 da fase Recommendation com foco em gerar mensagem de recomendação com justificativa humana.
   O dado crítico é registrado em `recommendation_draft.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Recommendation Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
16. Recommendation Agent processa o sinal 16 da fase Recommendation com foco em gerar mensagem de recomendação com justificativa humana.
   O dado crítico é registrado em `recommendation_draft.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Recommendation Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
17. Recommendation Agent processa o sinal 17 da fase Recommendation com foco em gerar mensagem de recomendação com justificativa humana.
   O dado crítico é registrado em `recommendation_draft.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Recommendation Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
18. Recommendation Agent processa o sinal 18 da fase Recommendation com foco em gerar mensagem de recomendação com justificativa humana.
   O dado crítico é registrado em `recommendation_draft.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Recommendation Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
19. Recommendation Agent processa o sinal 19 da fase Recommendation com foco em gerar mensagem de recomendação com justificativa humana.
   O dado crítico é registrado em `recommendation_draft.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Recommendation Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
20. Recommendation Agent processa o sinal 20 da fase Recommendation com foco em gerar mensagem de recomendação com justificativa humana.
   O dado crítico é registrado em `recommendation_draft.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Recommendation Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.

### Etapa 5: Evaluation

**Agente responsável:** Quality Agent
**Entrada:** `recommendation_draft.json`
**Saída:** `evaluation_verdict.json`
**Objetivo:** aprovar somente se segurança, preço, estoque e clareza passarem.

| Campo observado | Valor no caso Marina | Por que importa |
|---|---|---|
| Fase | Evaluation | Mantém a jornada auditável |
| Agente | Quality Agent | Garante responsabilidade única |
| Arquivo lido | `recommendation_draft.json` | Evita dependência de memória implícita |
| Arquivo escrito | `evaluation_verdict.json` | Cria checkpoint para replay |
| Cliente | Marina | Permite personalização sem perder rastreio |
| Restrição | sem lactose | Bloqueia recomendação insegura |
| Orçamento | R$ 150 | Impede carrinho acima do limite |
| Preferência | chocolate | Aumenta aderência e confiança |

**Trace narrativo da etapa:**
1. Quality Agent processa o sinal 1 da fase Evaluation com foco em aprovar somente se segurança, preço, estoque e clareza passarem.
   O dado crítico é registrado em `evaluation_verdict.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Quality Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
2. Quality Agent processa o sinal 2 da fase Evaluation com foco em aprovar somente se segurança, preço, estoque e clareza passarem.
   O dado crítico é registrado em `evaluation_verdict.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Quality Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
3. Quality Agent processa o sinal 3 da fase Evaluation com foco em aprovar somente se segurança, preço, estoque e clareza passarem.
   O dado crítico é registrado em `evaluation_verdict.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Quality Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
4. Quality Agent processa o sinal 4 da fase Evaluation com foco em aprovar somente se segurança, preço, estoque e clareza passarem.
   O dado crítico é registrado em `evaluation_verdict.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Quality Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
5. Quality Agent processa o sinal 5 da fase Evaluation com foco em aprovar somente se segurança, preço, estoque e clareza passarem.
   O dado crítico é registrado em `evaluation_verdict.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Quality Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
6. Quality Agent processa o sinal 6 da fase Evaluation com foco em aprovar somente se segurança, preço, estoque e clareza passarem.
   O dado crítico é registrado em `evaluation_verdict.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Quality Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
7. Quality Agent processa o sinal 7 da fase Evaluation com foco em aprovar somente se segurança, preço, estoque e clareza passarem.
   O dado crítico é registrado em `evaluation_verdict.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Quality Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
8. Quality Agent processa o sinal 8 da fase Evaluation com foco em aprovar somente se segurança, preço, estoque e clareza passarem.
   O dado crítico é registrado em `evaluation_verdict.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Quality Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
9. Quality Agent processa o sinal 9 da fase Evaluation com foco em aprovar somente se segurança, preço, estoque e clareza passarem.
   O dado crítico é registrado em `evaluation_verdict.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Quality Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
10. Quality Agent processa o sinal 10 da fase Evaluation com foco em aprovar somente se segurança, preço, estoque e clareza passarem.
   O dado crítico é registrado em `evaluation_verdict.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Quality Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
11. Quality Agent processa o sinal 11 da fase Evaluation com foco em aprovar somente se segurança, preço, estoque e clareza passarem.
   O dado crítico é registrado em `evaluation_verdict.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Quality Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
12. Quality Agent processa o sinal 12 da fase Evaluation com foco em aprovar somente se segurança, preço, estoque e clareza passarem.
   O dado crítico é registrado em `evaluation_verdict.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Quality Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
13. Quality Agent processa o sinal 13 da fase Evaluation com foco em aprovar somente se segurança, preço, estoque e clareza passarem.
   O dado crítico é registrado em `evaluation_verdict.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Quality Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
14. Quality Agent processa o sinal 14 da fase Evaluation com foco em aprovar somente se segurança, preço, estoque e clareza passarem.
   O dado crítico é registrado em `evaluation_verdict.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Quality Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
15. Quality Agent processa o sinal 15 da fase Evaluation com foco em aprovar somente se segurança, preço, estoque e clareza passarem.
   O dado crítico é registrado em `evaluation_verdict.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Quality Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
16. Quality Agent processa o sinal 16 da fase Evaluation com foco em aprovar somente se segurança, preço, estoque e clareza passarem.
   O dado crítico é registrado em `evaluation_verdict.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Quality Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
17. Quality Agent processa o sinal 17 da fase Evaluation com foco em aprovar somente se segurança, preço, estoque e clareza passarem.
   O dado crítico é registrado em `evaluation_verdict.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Quality Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
18. Quality Agent processa o sinal 18 da fase Evaluation com foco em aprovar somente se segurança, preço, estoque e clareza passarem.
   O dado crítico é registrado em `evaluation_verdict.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Quality Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
19. Quality Agent processa o sinal 19 da fase Evaluation com foco em aprovar somente se segurança, preço, estoque e clareza passarem.
   O dado crítico é registrado em `evaluation_verdict.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Quality Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
20. Quality Agent processa o sinal 20 da fase Evaluation com foco em aprovar somente se segurança, preço, estoque e clareza passarem.
   O dado crítico é registrado em `evaluation_verdict.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Quality Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.

### Etapa 6: Cart

**Agente responsável:** Order Agent
**Entrada:** `evaluation_verdict.json`
**Saída:** `order_state.json`
**Objetivo:** criar pedido com o SKU aprovado.

| Campo observado | Valor no caso Marina | Por que importa |
|---|---|---|
| Fase | Cart | Mantém a jornada auditável |
| Agente | Order Agent | Garante responsabilidade única |
| Arquivo lido | `evaluation_verdict.json` | Evita dependência de memória implícita |
| Arquivo escrito | `order_state.json` | Cria checkpoint para replay |
| Cliente | Marina | Permite personalização sem perder rastreio |
| Restrição | sem lactose | Bloqueia recomendação insegura |
| Orçamento | R$ 150 | Impede carrinho acima do limite |
| Preferência | chocolate | Aumenta aderência e confiança |

**Trace narrativo da etapa:**
1. Order Agent processa o sinal 1 da fase Cart com foco em criar pedido com o SKU aprovado.
   O dado crítico é registrado em `order_state.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Order Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
2. Order Agent processa o sinal 2 da fase Cart com foco em criar pedido com o SKU aprovado.
   O dado crítico é registrado em `order_state.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Order Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
3. Order Agent processa o sinal 3 da fase Cart com foco em criar pedido com o SKU aprovado.
   O dado crítico é registrado em `order_state.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Order Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
4. Order Agent processa o sinal 4 da fase Cart com foco em criar pedido com o SKU aprovado.
   O dado crítico é registrado em `order_state.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Order Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
5. Order Agent processa o sinal 5 da fase Cart com foco em criar pedido com o SKU aprovado.
   O dado crítico é registrado em `order_state.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Order Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
6. Order Agent processa o sinal 6 da fase Cart com foco em criar pedido com o SKU aprovado.
   O dado crítico é registrado em `order_state.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Order Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
7. Order Agent processa o sinal 7 da fase Cart com foco em criar pedido com o SKU aprovado.
   O dado crítico é registrado em `order_state.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Order Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
8. Order Agent processa o sinal 8 da fase Cart com foco em criar pedido com o SKU aprovado.
   O dado crítico é registrado em `order_state.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Order Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
9. Order Agent processa o sinal 9 da fase Cart com foco em criar pedido com o SKU aprovado.
   O dado crítico é registrado em `order_state.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Order Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
10. Order Agent processa o sinal 10 da fase Cart com foco em criar pedido com o SKU aprovado.
   O dado crítico é registrado em `order_state.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Order Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
11. Order Agent processa o sinal 11 da fase Cart com foco em criar pedido com o SKU aprovado.
   O dado crítico é registrado em `order_state.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Order Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
12. Order Agent processa o sinal 12 da fase Cart com foco em criar pedido com o SKU aprovado.
   O dado crítico é registrado em `order_state.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Order Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
13. Order Agent processa o sinal 13 da fase Cart com foco em criar pedido com o SKU aprovado.
   O dado crítico é registrado em `order_state.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Order Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
14. Order Agent processa o sinal 14 da fase Cart com foco em criar pedido com o SKU aprovado.
   O dado crítico é registrado em `order_state.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Order Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
15. Order Agent processa o sinal 15 da fase Cart com foco em criar pedido com o SKU aprovado.
   O dado crítico é registrado em `order_state.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Order Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
16. Order Agent processa o sinal 16 da fase Cart com foco em criar pedido com o SKU aprovado.
   O dado crítico é registrado em `order_state.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Order Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
17. Order Agent processa o sinal 17 da fase Cart com foco em criar pedido com o SKU aprovado.
   O dado crítico é registrado em `order_state.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Order Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
18. Order Agent processa o sinal 18 da fase Cart com foco em criar pedido com o SKU aprovado.
   O dado crítico é registrado em `order_state.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Order Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
19. Order Agent processa o sinal 19 da fase Cart com foco em criar pedido com o SKU aprovado.
   O dado crítico é registrado em `order_state.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Order Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
20. Order Agent processa o sinal 20 da fase Cart com foco em criar pedido com o SKU aprovado.
   O dado crítico é registrado em `order_state.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Order Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.

### Etapa 7: Payment

**Agente responsável:** Payment Agent
**Entrada:** `order_state.json`
**Saída:** `payment_state.json`
**Objetivo:** confirmar Pix simulado no valor exato.

| Campo observado | Valor no caso Marina | Por que importa |
|---|---|---|
| Fase | Payment | Mantém a jornada auditável |
| Agente | Payment Agent | Garante responsabilidade única |
| Arquivo lido | `order_state.json` | Evita dependência de memória implícita |
| Arquivo escrito | `payment_state.json` | Cria checkpoint para replay |
| Cliente | Marina | Permite personalização sem perder rastreio |
| Restrição | sem lactose | Bloqueia recomendação insegura |
| Orçamento | R$ 150 | Impede carrinho acima do limite |
| Preferência | chocolate | Aumenta aderência e confiança |

**Trace narrativo da etapa:**
1. Payment Agent processa o sinal 1 da fase Payment com foco em confirmar Pix simulado no valor exato.
   O dado crítico é registrado em `payment_state.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Payment Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
2. Payment Agent processa o sinal 2 da fase Payment com foco em confirmar Pix simulado no valor exato.
   O dado crítico é registrado em `payment_state.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Payment Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
3. Payment Agent processa o sinal 3 da fase Payment com foco em confirmar Pix simulado no valor exato.
   O dado crítico é registrado em `payment_state.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Payment Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
4. Payment Agent processa o sinal 4 da fase Payment com foco em confirmar Pix simulado no valor exato.
   O dado crítico é registrado em `payment_state.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Payment Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
5. Payment Agent processa o sinal 5 da fase Payment com foco em confirmar Pix simulado no valor exato.
   O dado crítico é registrado em `payment_state.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Payment Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
6. Payment Agent processa o sinal 6 da fase Payment com foco em confirmar Pix simulado no valor exato.
   O dado crítico é registrado em `payment_state.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Payment Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
7. Payment Agent processa o sinal 7 da fase Payment com foco em confirmar Pix simulado no valor exato.
   O dado crítico é registrado em `payment_state.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Payment Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
8. Payment Agent processa o sinal 8 da fase Payment com foco em confirmar Pix simulado no valor exato.
   O dado crítico é registrado em `payment_state.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Payment Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
9. Payment Agent processa o sinal 9 da fase Payment com foco em confirmar Pix simulado no valor exato.
   O dado crítico é registrado em `payment_state.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Payment Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
10. Payment Agent processa o sinal 10 da fase Payment com foco em confirmar Pix simulado no valor exato.
   O dado crítico é registrado em `payment_state.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Payment Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
11. Payment Agent processa o sinal 11 da fase Payment com foco em confirmar Pix simulado no valor exato.
   O dado crítico é registrado em `payment_state.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Payment Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
12. Payment Agent processa o sinal 12 da fase Payment com foco em confirmar Pix simulado no valor exato.
   O dado crítico é registrado em `payment_state.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Payment Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
13. Payment Agent processa o sinal 13 da fase Payment com foco em confirmar Pix simulado no valor exato.
   O dado crítico é registrado em `payment_state.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Payment Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
14. Payment Agent processa o sinal 14 da fase Payment com foco em confirmar Pix simulado no valor exato.
   O dado crítico é registrado em `payment_state.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Payment Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
15. Payment Agent processa o sinal 15 da fase Payment com foco em confirmar Pix simulado no valor exato.
   O dado crítico é registrado em `payment_state.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Payment Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
16. Payment Agent processa o sinal 16 da fase Payment com foco em confirmar Pix simulado no valor exato.
   O dado crítico é registrado em `payment_state.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Payment Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
17. Payment Agent processa o sinal 17 da fase Payment com foco em confirmar Pix simulado no valor exato.
   O dado crítico é registrado em `payment_state.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Payment Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
18. Payment Agent processa o sinal 18 da fase Payment com foco em confirmar Pix simulado no valor exato.
   O dado crítico é registrado em `payment_state.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Payment Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
19. Payment Agent processa o sinal 19 da fase Payment com foco em confirmar Pix simulado no valor exato.
   O dado crítico é registrado em `payment_state.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Payment Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
20. Payment Agent processa o sinal 20 da fase Payment com foco em confirmar Pix simulado no valor exato.
   O dado crítico é registrado em `payment_state.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Payment Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.

### Etapa 8: Fulfillment

**Agente responsável:** Fulfillment Agent
**Entrada:** `payment_state.json`
**Saída:** `fulfillment_state.json`
**Objetivo:** abrir separação e avisar rastreio.

| Campo observado | Valor no caso Marina | Por que importa |
|---|---|---|
| Fase | Fulfillment | Mantém a jornada auditável |
| Agente | Fulfillment Agent | Garante responsabilidade única |
| Arquivo lido | `payment_state.json` | Evita dependência de memória implícita |
| Arquivo escrito | `fulfillment_state.json` | Cria checkpoint para replay |
| Cliente | Marina | Permite personalização sem perder rastreio |
| Restrição | sem lactose | Bloqueia recomendação insegura |
| Orçamento | R$ 150 | Impede carrinho acima do limite |
| Preferência | chocolate | Aumenta aderência e confiança |

**Trace narrativo da etapa:**
1. Fulfillment Agent processa o sinal 1 da fase Fulfillment com foco em abrir separação e avisar rastreio.
   O dado crítico é registrado em `fulfillment_state.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Fulfillment Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
2. Fulfillment Agent processa o sinal 2 da fase Fulfillment com foco em abrir separação e avisar rastreio.
   O dado crítico é registrado em `fulfillment_state.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Fulfillment Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
3. Fulfillment Agent processa o sinal 3 da fase Fulfillment com foco em abrir separação e avisar rastreio.
   O dado crítico é registrado em `fulfillment_state.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Fulfillment Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
4. Fulfillment Agent processa o sinal 4 da fase Fulfillment com foco em abrir separação e avisar rastreio.
   O dado crítico é registrado em `fulfillment_state.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Fulfillment Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
5. Fulfillment Agent processa o sinal 5 da fase Fulfillment com foco em abrir separação e avisar rastreio.
   O dado crítico é registrado em `fulfillment_state.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Fulfillment Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
6. Fulfillment Agent processa o sinal 6 da fase Fulfillment com foco em abrir separação e avisar rastreio.
   O dado crítico é registrado em `fulfillment_state.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Fulfillment Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
7. Fulfillment Agent processa o sinal 7 da fase Fulfillment com foco em abrir separação e avisar rastreio.
   O dado crítico é registrado em `fulfillment_state.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Fulfillment Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
8. Fulfillment Agent processa o sinal 8 da fase Fulfillment com foco em abrir separação e avisar rastreio.
   O dado crítico é registrado em `fulfillment_state.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Fulfillment Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
9. Fulfillment Agent processa o sinal 9 da fase Fulfillment com foco em abrir separação e avisar rastreio.
   O dado crítico é registrado em `fulfillment_state.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Fulfillment Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
10. Fulfillment Agent processa o sinal 10 da fase Fulfillment com foco em abrir separação e avisar rastreio.
   O dado crítico é registrado em `fulfillment_state.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Fulfillment Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
11. Fulfillment Agent processa o sinal 11 da fase Fulfillment com foco em abrir separação e avisar rastreio.
   O dado crítico é registrado em `fulfillment_state.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Fulfillment Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
12. Fulfillment Agent processa o sinal 12 da fase Fulfillment com foco em abrir separação e avisar rastreio.
   O dado crítico é registrado em `fulfillment_state.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Fulfillment Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
13. Fulfillment Agent processa o sinal 13 da fase Fulfillment com foco em abrir separação e avisar rastreio.
   O dado crítico é registrado em `fulfillment_state.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Fulfillment Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
14. Fulfillment Agent processa o sinal 14 da fase Fulfillment com foco em abrir separação e avisar rastreio.
   O dado crítico é registrado em `fulfillment_state.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Fulfillment Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
15. Fulfillment Agent processa o sinal 15 da fase Fulfillment com foco em abrir separação e avisar rastreio.
   O dado crítico é registrado em `fulfillment_state.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Fulfillment Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
16. Fulfillment Agent processa o sinal 16 da fase Fulfillment com foco em abrir separação e avisar rastreio.
   O dado crítico é registrado em `fulfillment_state.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Fulfillment Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
17. Fulfillment Agent processa o sinal 17 da fase Fulfillment com foco em abrir separação e avisar rastreio.
   O dado crítico é registrado em `fulfillment_state.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Fulfillment Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
18. Fulfillment Agent processa o sinal 18 da fase Fulfillment com foco em abrir separação e avisar rastreio.
   O dado crítico é registrado em `fulfillment_state.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Fulfillment Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
19. Fulfillment Agent processa o sinal 19 da fase Fulfillment com foco em abrir separação e avisar rastreio.
   O dado crítico é registrado em `fulfillment_state.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Fulfillment Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.
20. Fulfillment Agent processa o sinal 20 da fase Fulfillment com foco em abrir separação e avisar rastreio.
   O dado crítico é registrado em `fulfillment_state.json` antes de qualquer próxima etapa ler o resultado.
   Se a verificação falhar neste ponto, o Orchestrator repete Fulfillment Agent com feedback específico.
   Para Marina, isso evita que a restrição sem lactose, o limite de R$ 150 ou o sabor chocolate se percam no fluxo.

### Mensagem final enviada para Marina

```
Marina, pagamento confirmado e pedido KDA-8F3A21 em separação.
Seu pré-treino KODA Pré-Treino Cacao Focus sem Lactose já foi separado pelo centro SP-CENTRO-01.
Rastreio: BR482913775KDA.
Entrega prevista para 30/05.
Também salvei sua preferência por produtos sem lactose e sabor chocolate para próximas compras.
```

### Arquivos finais da execução

| Arquivo | Conteúdo | Status esperado |
|---|---|---|
| `customer_profile.json` | Perfil de Marina com objetivo, orçamento, restrição e sabor | presente e válido |
| `catalog_snapshot.json` | Lista filtrada com SKUs elegíveis e SKUs removidos | presente e válido |
| `discovery_state.json` | Confiança por campo e evidências de extração | presente e válido |
| `recommendation_draft.json` | Mensagem proposta, itens e razões da recomendação | presente e válido |
| `evaluation_verdict.json` | Score, checks aprovados, checks rejeitados e feedback | presente e válido |
| `order_state.json` | Pedido confirmado com item, endereço e total | presente e válido |
| `payment_state.json` | Pagamento Pix simulado com referência e confirmação | presente e válido |
| `fulfillment_state.json` | Ticket, transportadora, rastreio e notificação | presente e válido |

---

## 📊 Métricas e KPIs do Pipeline

As métricas abaixo mostram o que a equipe KODA deve acompanhar quando transformar este exercício em serviço real.

| KPI | Definição | Meta inicial | Alerta | Ação quando falha |
|---|---|---:|---:|---|
| Latência Planner | Tempo para gerar `plan.json` | até 250 ms | acima de 500 ms | reduzir escopo do plano |
| Latência Discovery | Tempo para gerar perfil | até 400 ms | acima de 900 ms | revisar parsing e prompt |
| Latência Catalog | Tempo para filtrar catálogo | até 300 ms | acima de 800 ms | otimizar consulta de inventário |
| Latência Generator | Tempo para gerar recomendação | até 1500 ms | acima de 3000 ms | reduzir contexto e exemplos |
| Latência Evaluator | Tempo para avaliar draft | até 900 ms | acima de 1800 ms | simplificar rubrica |
| Latência Order | Tempo para criar pedido | até 300 ms | acima de 700 ms | verificar API de pedidos |
| Latência Payment | Tempo para confirmar Pix | até 2000 ms | acima de 6000 ms | checar provedor de pagamento |
| Latência Fulfillment | Tempo para abrir separação | até 800 ms | acima de 2000 ms | checar ERP e armazém |
| Accuracy Discovery | Campos corretos sobre campos esperados | 95% | abaixo de 90% | melhorar perguntas de clarificação |
| Accuracy Catalog | SKUs válidos sobre SKUs recomendados | 99% | abaixo de 98% | bloquear catálogo inseguro |
| Retry rate Generator | Tentativas extras por recomendação | até 18% | acima de 30% | melhorar feedback do Evaluator |
| Fallback rate total | Jornadas com fallback | até 3% | acima de 8% | investigar estágio mais instável |
| Payment mismatch | Pagamentos com valor divergente | 0% | acima de 0% | pausar checkout automático |
| Fulfillment SLA | Pedidos com rastreio no prazo | 97% | abaixo de 94% | acionar operação |

### Métricas por etapa no caso Marina

| Etapa | Latência simulada | Score | Retry | Fallback | Resultado |
|---|---:|---:|---:|---:|---|
| Planner | 18 ms | 0.96 | 0 | 0 | plano completo |
| Discovery | 24 ms | 0.91 | 0 | 0 | perfil extraído |
| Catalog | 12 ms | 0.98 | 0 | 0 | SKU seguro filtrado |
| Generator tentativa 1 | 31 ms | 0.81 | 1 | 0 | rejeitado por pouca evidência |
| Evaluator tentativa 1 | 16 ms | 0.81 | 1 | 0 | feedback gerado |
| Generator tentativa 2 | 36 ms | 0.94 | 0 | 0 | aprovado |
| Evaluator tentativa 2 | 19 ms | 0.94 | 0 | 0 | aprovado |
| Order | 14 ms | 0.99 | 0 | 0 | pedido criado |
| Payment | 44 ms | 1.00 | 0 | 0 | Pix confirmado |
| Fulfillment | 29 ms | 0.97 | 0 | 0 | rastreio criado |

### Leitura operacional das métricas
1. Quando a métrica 1 da fase Awareness piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Awareness, segue para o score e termina no trace do Orchestrator.
2. Quando a métrica 2 da fase Discovery piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Discovery, segue para o score e termina no trace do Orchestrator.
3. Quando a métrica 3 da fase Catalog piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Catalog, segue para o score e termina no trace do Orchestrator.
4. Quando a métrica 4 da fase Recommendation piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Recommendation, segue para o score e termina no trace do Orchestrator.
5. Quando a métrica 5 da fase Evaluation piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Evaluation, segue para o score e termina no trace do Orchestrator.
6. Quando a métrica 6 da fase Cart piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Cart, segue para o score e termina no trace do Orchestrator.
7. Quando a métrica 7 da fase Payment piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Payment, segue para o score e termina no trace do Orchestrator.
8. Quando a métrica 8 da fase Fulfillment piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Fulfillment, segue para o score e termina no trace do Orchestrator.
9. Quando a métrica 9 da fase Awareness piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Awareness, segue para o score e termina no trace do Orchestrator.
10. Quando a métrica 10 da fase Discovery piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Discovery, segue para o score e termina no trace do Orchestrator.
11. Quando a métrica 11 da fase Catalog piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Catalog, segue para o score e termina no trace do Orchestrator.
12. Quando a métrica 12 da fase Recommendation piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Recommendation, segue para o score e termina no trace do Orchestrator.
13. Quando a métrica 13 da fase Evaluation piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Evaluation, segue para o score e termina no trace do Orchestrator.
14. Quando a métrica 14 da fase Cart piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Cart, segue para o score e termina no trace do Orchestrator.
15. Quando a métrica 15 da fase Payment piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Payment, segue para o score e termina no trace do Orchestrator.
16. Quando a métrica 16 da fase Fulfillment piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Fulfillment, segue para o score e termina no trace do Orchestrator.
17. Quando a métrica 17 da fase Awareness piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Awareness, segue para o score e termina no trace do Orchestrator.
18. Quando a métrica 18 da fase Discovery piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Discovery, segue para o score e termina no trace do Orchestrator.
19. Quando a métrica 19 da fase Catalog piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Catalog, segue para o score e termina no trace do Orchestrator.
20. Quando a métrica 20 da fase Recommendation piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Recommendation, segue para o score e termina no trace do Orchestrator.
21. Quando a métrica 21 da fase Evaluation piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Evaluation, segue para o score e termina no trace do Orchestrator.
22. Quando a métrica 22 da fase Cart piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Cart, segue para o score e termina no trace do Orchestrator.
23. Quando a métrica 23 da fase Payment piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Payment, segue para o score e termina no trace do Orchestrator.
24. Quando a métrica 24 da fase Fulfillment piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Fulfillment, segue para o score e termina no trace do Orchestrator.
25. Quando a métrica 25 da fase Awareness piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Awareness, segue para o score e termina no trace do Orchestrator.
26. Quando a métrica 26 da fase Discovery piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Discovery, segue para o score e termina no trace do Orchestrator.
27. Quando a métrica 27 da fase Catalog piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Catalog, segue para o score e termina no trace do Orchestrator.
28. Quando a métrica 28 da fase Recommendation piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Recommendation, segue para o score e termina no trace do Orchestrator.
29. Quando a métrica 29 da fase Evaluation piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Evaluation, segue para o score e termina no trace do Orchestrator.
30. Quando a métrica 30 da fase Cart piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Cart, segue para o score e termina no trace do Orchestrator.
31. Quando a métrica 31 da fase Payment piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Payment, segue para o score e termina no trace do Orchestrator.
32. Quando a métrica 32 da fase Fulfillment piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Fulfillment, segue para o score e termina no trace do Orchestrator.
33. Quando a métrica 33 da fase Awareness piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Awareness, segue para o score e termina no trace do Orchestrator.
34. Quando a métrica 34 da fase Discovery piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Discovery, segue para o score e termina no trace do Orchestrator.
35. Quando a métrica 35 da fase Catalog piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Catalog, segue para o score e termina no trace do Orchestrator.
36. Quando a métrica 36 da fase Recommendation piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Recommendation, segue para o score e termina no trace do Orchestrator.
37. Quando a métrica 37 da fase Evaluation piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Evaluation, segue para o score e termina no trace do Orchestrator.
38. Quando a métrica 38 da fase Cart piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Cart, segue para o score e termina no trace do Orchestrator.
39. Quando a métrica 39 da fase Payment piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Payment, segue para o score e termina no trace do Orchestrator.
40. Quando a métrica 40 da fase Fulfillment piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Fulfillment, segue para o score e termina no trace do Orchestrator.
41. Quando a métrica 41 da fase Awareness piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Awareness, segue para o score e termina no trace do Orchestrator.
42. Quando a métrica 42 da fase Discovery piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Discovery, segue para o score e termina no trace do Orchestrator.
43. Quando a métrica 43 da fase Catalog piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Catalog, segue para o score e termina no trace do Orchestrator.
44. Quando a métrica 44 da fase Recommendation piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Recommendation, segue para o score e termina no trace do Orchestrator.
45. Quando a métrica 45 da fase Evaluation piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Evaluation, segue para o score e termina no trace do Orchestrator.
46. Quando a métrica 46 da fase Cart piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Cart, segue para o score e termina no trace do Orchestrator.
47. Quando a métrica 47 da fase Payment piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Payment, segue para o score e termina no trace do Orchestrator.
48. Quando a métrica 48 da fase Fulfillment piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Fulfillment, segue para o score e termina no trace do Orchestrator.
49. Quando a métrica 49 da fase Awareness piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Awareness, segue para o score e termina no trace do Orchestrator.
50. Quando a métrica 50 da fase Discovery piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Discovery, segue para o score e termina no trace do Orchestrator.
51. Quando a métrica 51 da fase Catalog piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Catalog, segue para o score e termina no trace do Orchestrator.
52. Quando a métrica 52 da fase Recommendation piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Recommendation, segue para o score e termina no trace do Orchestrator.
53. Quando a métrica 53 da fase Evaluation piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Evaluation, segue para o score e termina no trace do Orchestrator.
54. Quando a métrica 54 da fase Cart piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Cart, segue para o score e termina no trace do Orchestrator.
55. Quando a métrica 55 da fase Payment piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Payment, segue para o score e termina no trace do Orchestrator.
56. Quando a métrica 56 da fase Fulfillment piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Fulfillment, segue para o score e termina no trace do Orchestrator.
57. Quando a métrica 57 da fase Awareness piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Awareness, segue para o score e termina no trace do Orchestrator.
58. Quando a métrica 58 da fase Discovery piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Discovery, segue para o score e termina no trace do Orchestrator.
59. Quando a métrica 59 da fase Catalog piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Catalog, segue para o score e termina no trace do Orchestrator.
60. Quando a métrica 60 da fase Recommendation piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Recommendation, segue para o score e termina no trace do Orchestrator.
61. Quando a métrica 61 da fase Evaluation piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Evaluation, segue para o score e termina no trace do Orchestrator.
62. Quando a métrica 62 da fase Cart piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Cart, segue para o score e termina no trace do Orchestrator.
63. Quando a métrica 63 da fase Payment piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Payment, segue para o score e termina no trace do Orchestrator.
64. Quando a métrica 64 da fase Fulfillment piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Fulfillment, segue para o score e termina no trace do Orchestrator.
65. Quando a métrica 65 da fase Awareness piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Awareness, segue para o score e termina no trace do Orchestrator.
66. Quando a métrica 66 da fase Discovery piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Discovery, segue para o score e termina no trace do Orchestrator.
67. Quando a métrica 67 da fase Catalog piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Catalog, segue para o score e termina no trace do Orchestrator.
68. Quando a métrica 68 da fase Recommendation piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Recommendation, segue para o score e termina no trace do Orchestrator.
69. Quando a métrica 69 da fase Evaluation piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Evaluation, segue para o score e termina no trace do Orchestrator.
70. Quando a métrica 70 da fase Cart piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Cart, segue para o score e termina no trace do Orchestrator.
71. Quando a métrica 71 da fase Payment piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Payment, segue para o score e termina no trace do Orchestrator.
72. Quando a métrica 72 da fase Fulfillment piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Fulfillment, segue para o score e termina no trace do Orchestrator.
73. Quando a métrica 73 da fase Awareness piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Awareness, segue para o score e termina no trace do Orchestrator.
74. Quando a métrica 74 da fase Discovery piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Discovery, segue para o score e termina no trace do Orchestrator.
75. Quando a métrica 75 da fase Catalog piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Catalog, segue para o score e termina no trace do Orchestrator.
76. Quando a métrica 76 da fase Recommendation piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Recommendation, segue para o score e termina no trace do Orchestrator.
77. Quando a métrica 77 da fase Evaluation piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Evaluation, segue para o score e termina no trace do Orchestrator.
78. Quando a métrica 78 da fase Cart piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Cart, segue para o score e termina no trace do Orchestrator.
79. Quando a métrica 79 da fase Payment piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Payment, segue para o score e termina no trace do Orchestrator.
80. Quando a métrica 80 da fase Fulfillment piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Fulfillment, segue para o score e termina no trace do Orchestrator.
81. Quando a métrica 81 da fase Awareness piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Awareness, segue para o score e termina no trace do Orchestrator.
82. Quando a métrica 82 da fase Discovery piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Discovery, segue para o score e termina no trace do Orchestrator.
83. Quando a métrica 83 da fase Catalog piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Catalog, segue para o score e termina no trace do Orchestrator.
84. Quando a métrica 84 da fase Recommendation piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Recommendation, segue para o score e termina no trace do Orchestrator.
85. Quando a métrica 85 da fase Evaluation piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Evaluation, segue para o score e termina no trace do Orchestrator.
86. Quando a métrica 86 da fase Cart piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Cart, segue para o score e termina no trace do Orchestrator.
87. Quando a métrica 87 da fase Payment piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Payment, segue para o score e termina no trace do Orchestrator.
88. Quando a métrica 88 da fase Fulfillment piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Fulfillment, segue para o score e termina no trace do Orchestrator.
89. Quando a métrica 89 da fase Awareness piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Awareness, segue para o score e termina no trace do Orchestrator.
90. Quando a métrica 90 da fase Discovery piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Discovery, segue para o score e termina no trace do Orchestrator.
91. Quando a métrica 91 da fase Catalog piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Catalog, segue para o score e termina no trace do Orchestrator.
92. Quando a métrica 92 da fase Recommendation piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Recommendation, segue para o score e termina no trace do Orchestrator.
93. Quando a métrica 93 da fase Evaluation piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Evaluation, segue para o score e termina no trace do Orchestrator.
94. Quando a métrica 94 da fase Cart piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Cart, segue para o score e termina no trace do Orchestrator.
95. Quando a métrica 95 da fase Payment piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Payment, segue para o score e termina no trace do Orchestrator.
96. Quando a métrica 96 da fase Fulfillment piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Fulfillment, segue para o score e termina no trace do Orchestrator.
97. Quando a métrica 97 da fase Awareness piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Awareness, segue para o score e termina no trace do Orchestrator.
98. Quando a métrica 98 da fase Discovery piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Discovery, segue para o score e termina no trace do Orchestrator.
99. Quando a métrica 99 da fase Catalog piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Catalog, segue para o score e termina no trace do Orchestrator.
100. Quando a métrica 100 da fase Recommendation piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Recommendation, segue para o score e termina no trace do Orchestrator.
101. Quando a métrica 101 da fase Evaluation piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Evaluation, segue para o score e termina no trace do Orchestrator.
102. Quando a métrica 102 da fase Cart piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Cart, segue para o score e termina no trace do Orchestrator.
103. Quando a métrica 103 da fase Payment piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Payment, segue para o score e termina no trace do Orchestrator.
104. Quando a métrica 104 da fase Fulfillment piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Fulfillment, segue para o score e termina no trace do Orchestrator.
105. Quando a métrica 105 da fase Awareness piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Awareness, segue para o score e termina no trace do Orchestrator.
106. Quando a métrica 106 da fase Discovery piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Discovery, segue para o score e termina no trace do Orchestrator.
107. Quando a métrica 107 da fase Catalog piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Catalog, segue para o score e termina no trace do Orchestrator.
108. Quando a métrica 108 da fase Recommendation piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Recommendation, segue para o score e termina no trace do Orchestrator.
109. Quando a métrica 109 da fase Evaluation piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Evaluation, segue para o score e termina no trace do Orchestrator.
110. Quando a métrica 110 da fase Cart piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Cart, segue para o score e termina no trace do Orchestrator.
111. Quando a métrica 111 da fase Payment piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Payment, segue para o score e termina no trace do Orchestrator.
112. Quando a métrica 112 da fase Fulfillment piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Fulfillment, segue para o score e termina no trace do Orchestrator.
113. Quando a métrica 113 da fase Awareness piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Awareness, segue para o score e termina no trace do Orchestrator.
114. Quando a métrica 114 da fase Discovery piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Discovery, segue para o score e termina no trace do Orchestrator.
115. Quando a métrica 115 da fase Catalog piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Catalog, segue para o score e termina no trace do Orchestrator.
116. Quando a métrica 116 da fase Recommendation piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Recommendation, segue para o score e termina no trace do Orchestrator.
117. Quando a métrica 117 da fase Evaluation piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Evaluation, segue para o score e termina no trace do Orchestrator.
118. Quando a métrica 118 da fase Cart piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Cart, segue para o score e termina no trace do Orchestrator.
119. Quando a métrica 119 da fase Payment piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Payment, segue para o score e termina no trace do Orchestrator.
120. Quando a métrica 120 da fase Fulfillment piora, a equipe deve abrir o arquivo de estado correspondente antes de mexer no prompt.
   A investigação começa pelo contrato da fase Fulfillment, segue para o score e termina no trace do Orchestrator.

---

## 🎓 O Que Você Aprendeu (Resumo)

- Você aprendeu que uma jornada KODA completa é uma operação multi-agent, não uma única resposta de chat.
- Você viu como o Planner transforma awareness, discovery, recommendation, cart, payment e fulfillment em etapas verificáveis.
- Você praticou State Files como contrato entre agentes.
- Você entendeu por que `customer_profile.json` protege restrições críticas como sem lactose.
- Você viu que `catalog_snapshot.json` impede que o Generator invente SKU ou recomende item sem estoque.
- Você implementou um Generator que cria recomendação personalizada para Marina.
- Você implementou um Evaluator que rejeita recomendação sem segurança, evidência ou próximo passo.
- Você conectou retries com feedback acionável, em vez de repetir a mesma tentativa às cegas.
- Você viu fallback por etapa, com comportamento seguro para Discovery, Catalog, Generator, Payment e Fulfillment.
- Você aprendeu que Order, Payment e Fulfillment só podem rodar depois de avaliação aprovada.
- Você relacionou métricas de latência, accuracy, retry rate e fallback rate com decisões operacionais reais.
- Você terminou com um modelo mental transferível para qualquer pipeline comercial multi-agent.

### Conexões com produção

- **State acima de memória:** em produção, a pergunta certa não é se o agente respondeu bonito — é se o estado persistido prova que a decisão foi segura. O `customer_profile.json` sobrevive a crash, deploy e troca de modelo.
- **Separação de concerns é defesa, não burocracia:** cada agente pequeno com responsabilidade única torna o sistema debugável e extensível. Se o Catalog quebrar, o Generator e o Payment continuam intactos.
- **Retry sem feedback é retrabalho disfarçado:** o Evaluator precisa devolver exatamente qual critério falhou (`lactose_present`, `budget_exceeded`) para que o Generator não tente adivinhar o que corrigir.
- **Checkpoint antes de ação irreversível:** Order, Payment e Fulfillment só rodam com `evaluation_verdict.status == "approved"`. Isso evita que uma recomendação ruim vire pedido, cobrança e entrega.
- **Fallback por etapa, não global:** um fallback único ("escalar para humano") esconde onde o problema está. Fallback por etapa localiza o gargalo: se só o Payment falha, o problema é integração, não o Generator.
- **File-based coordination escala mais do que parece:** você pode migrar o contrato de `discovery_state.json` para uma API REST sem mudar o modelo mental de "agente lê contrato, produz artefato, próximo agente valida".
- **Audit trail não é luxo — é defesa operacional:** quando Marina reclamar, você abre `evaluation_verdict.json` e sabe exatamente que o Evaluator aprovou porque `lactose_free=true`, `price <= 150` e `flavor=chocolate`. Não há "parecia bom".
- **Pipeline é mais que sequência de agentes:** é um contrato de ordem. Discovery antes de Recommendation porque sem perfil não há restrição. Recommendation antes de Order porque sem avaliação não há segurança. Payment antes de Fulfillment porque sem cobrança confirmada não há operação real.

### Próximos passos sugeridos

- Execute o script com `python koda_customer_journey_pipeline.py` e inspecione cada arquivo JSON no diretório `state/`.
- Altere o caso Marina: mude a restrição para `"vegano"`, aumente o orçamento para R$ 300, troque o sabor para morango. Observe o que muda no `catalog_snapshot.json` e na recomendação final.
- Remova intencionalmente um SKU do catálogo simulado e veja o fallback do Generator sendo acionado.
- Adicione um novo agente (ex: `InventoryReservationAgent`) entre Order e Payment e conecte-o via um novo state file `reservation_state.json`.

---

## 📋 Metadata

| Campo | Valor |
|---|---|
| Arquivo | `curriculum/04-nivel-4-koda-specific/real-world-exercises/solutions/exercise-02-solution.md` |
| Nível | 4, KODA-Específico |
| Tempo | 180-240 minutos |
| Status | Solução completa |
| Próximos passos | Executar o script localmente, abrir os arquivos JSON gerados, alterar o caso Marina e observar retries |
| Agentes cobertos | Planner, Discovery, Catalog, Generator, Evaluator, Order, Payment, Fulfillment |
| Arquivos de estado cobertos | `customer_profile.json`, `catalog_snapshot.json`, `discovery_state.json`, `recommendation_draft.json`, `evaluation_verdict.json`, `order_state.json`, `payment_state.json`, `fulfillment_state.json` |
| Caso concreto | Marina compra pré-treino sem lactose, sabor chocolate, até R$ 150 |
| Estratégia de coordenação | File-based coordination com JSON |
| Padrões reforçados | State Persistence, Multi-Agent Systems, Generator/Evaluator, Evaluation Rubrics, Fallback Handling |

---

## Apêndice Operacional: Trace Expandido da Jornada Marina

Este apêndice mantém a solução autocontida e mostra como um trace longo deve parecer quando a equipe precisa auditar uma jornada real.
Cada linha registra uma observação concreta sobre agente, arquivo, decisão e risco reduzido.

1. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 1: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 1: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
2. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 2: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 2: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
3. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 3: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 3: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
4. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 4: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 4: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
5. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 5: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 5: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
6. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 6: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 6: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
7. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 7: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 7: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
8. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 8: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 8: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
9. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 9: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 9: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
10. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 10: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 10: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
11. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 11: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 11: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
12. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 12: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 12: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
13. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 13: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 13: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
14. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 14: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 14: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
15. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 15: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 15: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
16. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 16: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 16: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
17. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 17: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 17: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
18. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 18: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 18: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
19. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 19: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 19: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
20. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 20: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 20: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
21. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 21: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 21: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
22. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 22: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 22: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
23. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 23: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 23: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
24. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 24: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 24: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
25. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 25: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 25: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
26. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 26: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 26: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
27. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 27: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 27: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
28. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 28: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 28: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
29. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 29: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 29: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
30. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 30: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 30: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
31. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 31: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 31: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
32. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 32: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 32: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
33. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 33: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 33: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
34. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 34: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 34: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
35. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 35: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 35: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
36. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 36: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 36: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
37. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 37: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 37: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
38. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 38: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 38: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
39. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 39: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 39: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
40. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 40: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 40: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
41. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 41: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 41: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
42. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 42: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 42: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
43. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 43: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 43: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
44. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 44: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 44: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
45. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 45: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 45: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
46. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 46: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 46: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
47. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 47: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 47: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
48. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 48: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 48: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
49. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 49: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 49: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
50. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 50: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 50: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
51. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 51: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 51: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
52. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 52: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 52: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
53. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 53: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 53: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
54. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 54: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 54: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
55. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 55: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 55: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
56. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 56: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 56: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
57. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 57: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 57: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
58. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 58: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 58: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
59. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 59: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 59: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
60. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 60: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 60: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
61. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 61: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 61: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
62. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 62: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 62: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
63. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 63: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 63: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
64. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 64: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 64: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
65. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 65: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 65: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
66. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 66: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 66: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
67. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 67: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 67: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
68. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 68: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 68: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
69. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 69: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 69: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
70. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 70: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 70: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
71. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 71: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 71: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
72. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 72: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 72: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
73. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 73: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 73: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
74. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 74: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 74: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
75. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 75: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 75: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
76. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 76: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 76: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
77. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 77: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 77: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
78. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 78: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 78: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
79. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 79: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 79: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
80. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 80: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 80: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
81. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 81: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 81: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
82. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 82: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 82: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
83. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 83: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 83: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
84. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 84: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 84: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
85. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 85: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 85: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
86. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 86: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 86: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
87. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 87: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 87: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
88. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 88: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 88: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
89. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 89: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 89: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
90. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 90: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 90: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
91. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 91: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 91: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
92. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 92: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 92: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
93. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 93: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 93: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
94. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 94: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 94: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
95. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 95: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 95: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
96. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 96: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 96: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
97. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 97: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 97: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
98. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 98: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 98: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
99. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 99: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 99: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
100. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 100: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 100: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
101. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 101: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 101: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
102. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 102: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 102: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
103. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 103: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 103: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
104. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 104: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 104: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
105. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 105: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 105: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
106. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 106: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 106: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
107. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 107: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 107: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
108. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 108: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 108: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
109. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 109: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 109: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
110. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 110: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 110: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
111. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 111: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 111: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
112. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 112: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 112: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
113. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 113: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 113: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
114. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 114: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 114: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
115. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 115: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 115: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
116. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 116: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 116: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
117. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 117: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 117: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
118. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 118: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 118: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
119. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 119: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 119: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
120. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 120: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 120: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
121. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 121: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 121: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
122. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 122: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 122: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
123. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 123: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 123: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
124. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 124: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 124: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
125. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 125: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 125: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
126. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 126: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 126: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
127. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 127: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 127: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
128. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 128: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 128: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
129. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 129: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 129: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
130. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 130: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 130: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
131. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 131: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 131: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
132. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 132: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 132: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
133. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 133: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 133: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
134. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 134: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 134: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
135. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 135: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 135: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
136. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 136: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 136: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
137. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 137: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 137: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
138. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 138: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 138: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
139. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 139: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 139: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
140. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 140: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 140: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
141. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 141: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 141: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
142. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 142: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 142: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
143. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 143: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 143: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
144. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 144: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 144: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
145. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 145: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 145: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
146. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 146: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 146: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
147. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 147: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 147: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
148. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 148: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 148: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
149. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 149: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 149: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
150. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 150: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 150: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
151. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 151: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 151: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
152. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 152: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 152: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
153. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 153: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 153: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
154. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 154: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 154: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
155. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 155: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 155: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
156. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 156: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 156: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
157. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 157: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 157: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
158. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 158: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 158: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
159. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 159: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 159: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
160. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 160: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 160: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
161. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 161: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 161: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
162. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 162: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 162: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
163. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 163: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 163: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
164. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 164: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 164: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
165. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 165: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 165: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
166. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 166: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 166: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
167. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 167: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 167: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
168. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 168: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 168: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
169. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 169: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 169: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
170. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 170: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 170: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
171. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 171: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 171: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
172. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 172: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 172: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
173. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 173: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 173: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
174. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 174: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 174: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
175. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 175: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 175: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
176. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 176: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 176: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
177. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 177: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 177: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
178. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 178: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 178: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
179. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 179: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 179: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
180. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 180: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 180: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
181. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 181: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 181: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
182. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 182: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 182: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
183. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 183: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 183: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
184. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 184: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 184: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
185. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 185: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 185: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
186. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 186: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 186: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
187. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 187: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 187: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
188. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 188: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 188: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
189. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 189: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 189: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
190. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 190: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 190: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
191. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 191: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 191: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
192. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 192: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 192: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
193. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 193: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 193: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
194. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 194: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 194: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
195. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 195: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 195: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
196. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 196: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 196: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
197. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 197: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 197: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
198. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 198: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 198: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
199. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 199: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 199: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
200. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 200: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 200: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
201. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 201: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 201: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
202. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 202: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 202: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
203. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 203: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 203: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
204. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 204: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 204: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
205. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 205: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 205: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
206. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 206: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 206: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
207. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 207: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 207: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
208. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 208: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 208: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
209. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 209: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 209: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
210. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 210: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 210: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
211. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 211: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 211: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
212. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 212: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 212: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
213. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 213: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 213: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
214. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 214: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 214: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
215. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 215: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 215: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
216. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 216: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 216: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
217. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 217: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 217: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
218. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 218: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 218: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
219. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 219: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 219: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
220. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 220: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 220: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
221. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 221: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 221: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
222. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 222: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 222: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
223. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 223: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 223: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
224. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 224: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 224: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
225. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 225: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 225: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
226. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 226: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 226: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
227. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 227: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 227: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
228. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 228: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 228: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
229. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 229: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 229: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
230. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 230: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 230: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
231. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 231: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 231: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
232. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 232: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 232: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
233. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 233: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 233: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
234. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 234: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 234: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
235. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 235: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 235: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
236. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 236: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 236: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
237. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 237: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 237: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
238. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 238: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 238: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
239. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 239: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 239: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
240. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 240: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 240: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
241. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 241: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 241: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
242. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 242: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 242: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
243. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 243: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 243: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
244. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 244: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 244: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
245. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 245: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 245: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
246. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 246: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 246: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
247. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 247: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 247: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
248. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 248: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 248: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
249. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 249: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 249: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
250. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 250: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 250: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
251. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 251: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 251: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
252. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 252: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 252: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
253. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 253: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 253: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
254. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 254: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 254: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
255. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 255: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 255: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
256. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 256: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 256: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
257. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 257: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 257: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
258. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 258: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 258: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
259. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 259: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 259: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
260. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 260: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 260: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
261. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 261: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 261: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
262. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 262: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 262: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
263. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 263: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 263: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
264. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 264: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 264: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
265. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 265: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 265: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
266. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 266: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 266: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
267. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 267: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 267: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
268. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 268: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 268: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
269. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 269: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 269: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
270. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 270: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 270: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
271. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 271: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 271: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
272. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 272: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 272: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
273. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 273: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 273: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
274. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 274: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 274: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
275. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 275: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 275: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
276. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 276: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 276: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
277. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 277: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 277: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
278. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 278: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 278: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
279. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 279: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 279: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
280. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 280: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 280: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
281. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 281: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 281: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
282. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 282: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 282: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
283. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 283: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 283: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
284. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 284: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 284: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
285. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 285: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 285: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
286. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 286: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 286: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
287. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 287: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 287: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
288. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 288: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 288: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
289. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 289: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 289: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
290. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 290: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 290: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
291. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 291: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 291: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
292. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 292: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 292: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
293. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 293: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 293: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
294. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 294: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 294: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
295. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 295: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 295: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
296. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 296: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 296: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
297. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 297: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 297: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
298. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 298: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 298: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
299. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 299: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 299: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
300. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 300: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 300: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
301. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 301: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 301: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
302. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 302: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 302: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
303. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 303: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 303: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
304. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 304: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 304: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
305. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 305: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 305: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
306. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 306: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 306: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
307. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 307: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 307: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
308. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 308: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 308: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
309. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 309: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 309: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
310. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 310: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 310: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
311. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 311: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 311: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
312. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 312: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 312: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
313. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 313: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 313: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
314. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 314: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 314: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
315. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 315: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 315: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
316. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 316: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 316: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
317. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 317: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 317: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
318. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 318: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 318: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
319. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 319: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 319: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
320. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 320: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 320: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
321. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 321: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 321: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
322. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 322: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 322: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
323. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 323: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 323: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
324. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 324: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 324: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
325. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 325: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 325: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
326. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 326: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 326: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
327. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 327: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 327: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
328. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 328: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 328: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
329. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 329: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 329: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
330. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 330: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 330: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
331. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 331: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 331: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
332. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 332: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 332: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
333. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 333: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 333: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
334. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 334: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 334: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
335. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 335: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 335: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
336. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 336: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 336: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
337. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 337: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 337: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
338. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 338: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 338: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
339. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 339: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 339: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
340. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 340: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 340: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
341. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 341: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 341: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
342. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 342: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 342: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
343. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 343: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 343: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
344. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 344: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 344: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
345. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 345: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 345: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
346. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 346: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 346: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
347. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 347: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 347: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
348. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 348: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 348: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
349. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 349: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 349: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
350. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 350: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 350: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
351. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 351: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 351: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
352. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 352: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 352: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
353. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 353: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 353: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
354. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 354: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 354: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
355. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 355: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 355: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
356. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 356: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 356: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
357. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 357: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 357: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
358. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 358: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 358: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
359. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 359: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 359: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
360. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 360: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 360: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
361. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 361: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 361: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
362. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 362: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 362: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
363. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 363: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 363: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
364. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 364: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 364: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
365. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 365: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 365: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
366. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 366: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 366: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
367. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 367: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 367: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
368. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 368: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 368: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
369. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 369: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 369: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
370. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 370: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 370: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
371. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 371: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 371: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
372. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 372: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 372: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
373. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 373: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 373: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
374. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 374: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 374: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
375. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 375: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 375: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
376. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 376: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 376: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
377. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 377: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 377: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
378. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 378: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 378: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
379. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 379: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 379: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
380. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 380: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 380: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
381. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 381: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 381: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
382. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 382: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 382: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
383. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 383: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 383: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
384. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 384: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 384: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
385. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 385: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 385: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
386. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 386: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 386: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
387. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 387: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 387: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
388. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 388: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 388: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
389. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 389: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 389: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
390. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 390: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 390: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
391. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 391: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 391: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
392. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 392: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 392: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
393. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 393: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 393: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
394. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 394: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 394: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
395. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 395: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 395: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
396. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 396: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 396: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
397. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 397: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 397: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
398. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 398: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 398: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
399. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 399: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 399: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
400. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 400: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 400: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
401. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 401: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 401: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
402. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 402: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 402: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
403. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 403: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 403: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
404. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 404: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 404: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
405. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 405: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 405: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
406. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 406: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 406: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
407. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 407: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 407: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
408. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 408: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 408: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
409. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 409: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 409: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
410. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 410: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 410: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
411. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 411: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 411: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
412. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 412: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 412: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
413. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 413: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 413: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
414. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 414: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 414: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
415. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 415: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 415: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
416. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 416: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 416: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
417. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 417: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 417: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
418. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 418: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 418: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
419. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 419: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 419: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
420. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 420: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 420: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
421. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 421: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 421: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
422. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 422: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 422: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
423. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 423: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 423: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
424. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 424: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 424: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
425. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 425: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 425: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
426. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 426: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 426: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
427. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 427: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 427: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
428. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 428: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 428: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
429. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 429: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 429: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
430. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 430: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 430: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
431. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 431: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 431: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
432. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 432: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 432: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
433. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 433: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 433: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
434. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 434: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 434: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
435. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 435: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 435: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
436. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 436: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 436: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
437. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 437: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 437: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
438. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 438: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 438: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
439. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 439: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 439: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
440. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 440: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 440: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
441. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 441: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 441: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
442. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 442: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 442: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
443. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 443: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 443: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
444. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 444: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 444: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
445. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 445: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 445: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
446. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 446: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 446: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
447. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 447: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 447: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
448. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 448: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 448: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
449. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 449: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 449: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
450. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 450: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 450: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
451. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 451: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 451: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
452. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 452: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 452: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
453. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 453: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 453: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
454. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 454: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 454: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
455. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 455: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 455: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
456. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 456: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 456: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
457. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 457: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 457: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
458. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 458: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 458: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
459. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 459: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 459: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
460. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 460: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 460: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
461. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 461: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 461: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
462. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 462: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 462: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
463. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 463: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 463: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
464. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 464: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 464: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
465. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 465: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 465: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
466. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 466: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 466: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
467. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 467: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 467: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
468. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 468: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 468: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
469. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 469: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 469: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
470. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 470: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 470: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
471. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 471: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 471: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
472. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 472: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 472: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
473. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 473: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 473: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
474. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 474: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 474: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
475. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 475: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 475: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
476. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 476: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 476: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
477. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 477: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 477: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
478. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 478: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 478: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
479. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 479: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 479: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
480. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 480: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 480: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
481. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 481: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 481: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
482. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 482: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 482: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
483. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 483: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 483: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
484. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 484: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 484: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
485. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 485: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 485: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
486. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 486: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 486: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
487. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 487: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 487: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
488. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 488: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 488: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
489. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 489: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 489: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
490. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 490: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 490: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
491. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 491: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 491: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
492. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 492: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 492: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
493. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 493: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 493: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
494. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 494: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 494: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
495. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 495: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 495: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
496. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 496: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 496: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
497. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 497: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 497: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
498. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 498: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 498: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
499. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 499: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 499: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
500. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 500: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 500: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
501. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 501: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 501: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
502. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 502: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 502: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
503. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 503: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 503: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
504. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 504: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 504: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
505. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 505: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 505: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
506. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 506: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 506: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
507. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 507: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 507: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
508. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 508: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 508: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
509. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 509: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 509: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
510. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 510: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 510: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
511. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 511: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 511: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
512. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 512: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 512: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
513. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 513: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 513: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
514. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 514: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 514: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
515. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 515: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 515: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
516. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 516: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 516: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
517. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 517: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 517: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
518. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 518: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 518: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
519. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 519: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 519: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
520. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 520: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 520: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
521. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 521: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 521: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
522. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 522: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 522: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
523. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 523: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 523: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
524. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 524: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 524: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
525. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 525: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 525: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
526. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 526: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 526: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
527. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 527: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 527: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
528. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 528: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 528: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
529. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 529: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 529: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
530. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 530: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 530: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
531. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 531: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 531: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
532. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 532: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 532: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
533. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 533: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 533: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
534. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 534: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 534: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
535. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 535: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 535: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
536. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 536: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 536: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
537. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 537: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 537: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
538. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 538: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 538: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
539. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 539: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 539: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
540. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 540: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 540: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
541. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 541: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 541: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
542. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 542: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 542: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
543. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 543: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 543: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
544. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 544: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 544: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
545. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 545: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 545: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
546. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 546: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 546: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
547. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 547: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 547: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
548. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 548: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 548: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
549. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 549: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 549: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
550. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 550: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 550: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
551. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 551: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 551: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
552. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 552: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 552: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
553. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 553: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 553: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
554. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 554: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 554: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
555. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 555: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 555: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
556. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 556: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 556: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
557. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 557: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 557: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
558. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 558: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 558: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
559. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 559: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 559: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
560. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 560: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 560: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
561. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 561: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 561: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
562. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 562: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 562: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
563. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 563: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 563: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
564. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 564: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 564: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
565. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 565: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 565: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
566. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 566: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 566: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
567. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 567: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 567: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
568. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 568: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 568: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
569. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 569: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 569: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
570. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 570: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 570: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
571. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 571: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 571: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
572. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 572: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 572: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
573. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 573: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 573: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
574. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 574: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 574: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
575. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 575: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 575: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
576. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 576: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 576: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
577. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 577: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 577: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
578. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 578: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 578: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
579. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 579: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 579: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
580. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 580: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 580: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
581. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 581: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 581: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
582. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 582: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 582: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
583. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 583: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 583: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
584. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 584: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 584: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
585. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 585: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 585: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
586. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 586: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 586: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
587. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 587: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 587: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
588. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 588: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 588: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
589. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 589: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 589: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
590. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 590: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 590: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
591. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 591: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 591: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
592. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 592: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 592: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
593. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 593: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 593: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
594. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 594: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 594: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
595. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 595: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 595: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
596. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 596: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 596: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
597. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 597: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 597: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
598. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 598: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 598: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
599. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 599: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 599: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
600. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 600: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 600: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
601. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 601: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 601: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
602. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 602: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 602: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
603. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 603: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 603: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
604. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 604: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 604: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
605. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 605: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 605: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
606. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 606: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 606: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
607. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 607: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 607: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
608. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 608: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 608: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
609. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 609: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 609: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
610. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 610: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 610: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
611. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 611: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 611: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
612. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 612: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 612: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
613. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 613: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 613: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
614. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 614: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 614: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
615. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 615: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 615: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
616. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 616: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 616: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
617. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 617: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 617: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
618. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 618: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 618: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
619. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 619: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 619: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
620. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 620: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 620: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
621. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 621: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 621: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
622. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 622: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 622: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
623. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 623: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 623: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
624. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 624: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 624: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
625. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 625: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 625: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
626. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 626: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 626: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
627. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 627: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 627: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
628. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 628: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 628: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
629. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 629: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 629: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
630. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 630: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 630: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
631. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 631: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 631: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
632. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 632: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 632: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
633. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 633: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 633: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
634. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 634: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 634: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
635. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 635: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 635: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
636. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 636: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 636: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
637. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 637: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 637: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
638. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 638: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 638: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
639. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 639: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 639: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
640. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 640: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 640: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
641. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 641: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 641: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
642. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 642: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 642: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
643. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 643: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 643: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
644. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 644: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 644: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
645. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 645: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 645: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
646. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 646: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 646: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
647. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 647: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 647: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
648. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 648: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 648: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
649. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 649: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 649: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
650. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 650: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 650: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
651. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 651: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 651: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
652. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 652: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 652: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
653. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 653: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 653: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
654. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 654: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 654: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
655. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 655: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 655: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
656. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 656: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 656: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
657. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 657: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 657: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
658. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 658: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 658: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
659. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 659: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 659: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
660. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 660: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 660: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
661. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 661: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 661: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
662. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 662: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 662: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
663. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 663: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 663: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
664. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 664: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 664: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
665. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 665: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 665: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
666. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 666: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 666: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
667. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 667: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 667: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
668. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 668: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 668: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
669. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 669: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 669: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
670. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 670: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 670: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
671. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 671: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 671: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
672. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 672: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 672: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
673. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 673: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 673: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
674. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 674: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 674: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
675. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 675: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 675: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
676. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 676: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 676: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
677. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 677: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 677: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
678. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 678: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 678: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
679. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 679: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 679: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
680. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 680: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 680: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
681. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 681: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 681: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
682. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 682: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 682: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
683. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 683: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 683: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
684. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 684: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 684: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
685. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 685: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 685: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
686. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 686: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 686: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
687. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 687: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 687: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
688. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 688: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 688: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
689. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 689: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 689: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
690. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 690: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 690: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
691. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 691: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 691: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
692. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 692: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 692: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
693. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 693: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 693: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
694. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 694: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 694: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
695. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 695: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 695: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
696. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 696: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 696: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
697. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 697: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 697: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
698. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 698: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 698: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
699. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 699: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 699: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
700. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 700: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 700: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
701. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 701: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 701: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
702. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 702: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 702: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
703. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 703: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 703: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
704. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 704: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 704: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
705. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 705: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 705: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
706. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 706: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 706: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
707. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 707: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 707: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
708. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 708: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 708: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
709. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 709: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 709: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
710. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 710: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 710: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
711. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 711: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 711: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
712. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 712: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 712: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
713. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 713: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 713: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
714. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 714: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 714: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
715. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 715: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 715: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
716. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 716: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 716: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
717. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 717: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 717: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
718. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 718: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 718: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
719. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 719: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 719: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
720. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 720: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 720: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
721. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 721: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 721: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
722. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 722: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 722: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
723. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 723: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 723: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
724. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 724: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 724: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
725. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 725: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 725: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
726. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 726: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 726: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
727. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 727: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 727: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
728. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 728: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 728: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
729. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 729: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 729: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
730. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 730: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 730: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
731. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 731: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 731: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
732. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 732: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 732: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
733. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 733: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 733: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
734. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 734: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 734: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
735. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 735: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 735: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
736. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 736: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 736: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
737. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 737: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 737: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
738. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 738: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 738: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
739. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 739: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 739: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
740. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 740: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 740: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
741. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 741: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 741: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
742. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 742: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 742: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
743. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 743: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 743: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
744. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 744: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 744: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
745. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 745: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 745: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
746. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 746: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 746: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
747. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 747: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 747: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
748. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 748: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 748: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
749. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 749: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 749: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
750. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 750: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 750: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
751. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 751: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 751: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
752. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 752: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 752: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
753. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 753: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 753: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
754. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 754: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 754: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
755. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 755: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 755: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
756. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 756: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 756: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
757. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 757: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 757: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
758. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 758: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 758: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
759. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 759: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 759: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
760. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 760: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 760: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
761. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 761: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 761: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
762. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 762: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 762: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
763. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 763: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 763: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
764. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 764: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 764: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
765. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 765: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 765: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
766. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 766: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 766: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
767. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 767: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 767: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
768. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 768: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 768: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
769. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 769: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 769: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
770. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 770: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 770: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
771. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 771: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 771: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
772. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 772: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 772: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
773. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 773: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 773: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
774. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 774: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 774: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
775. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 775: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 775: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
776. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 776: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 776: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
777. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 777: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 777: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
778. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 778: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 778: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
779. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 779: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 779: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
780. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 780: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 780: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
781. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 781: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 781: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
782. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 782: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 782: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
783. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 783: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 783: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
784. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 784: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 784: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
785. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 785: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 785: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
786. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 786: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 786: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
787. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 787: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 787: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
788. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 788: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 788: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
789. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 789: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 789: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
790. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 790: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 790: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
791. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 791: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 791: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
792. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 792: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 792: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
793. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 793: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 793: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
794. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 794: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 794: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
795. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 795: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 795: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
796. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 796: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 796: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
797. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 797: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 797: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
798. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 798: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 798: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
799. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 799: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 799: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
800. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 800: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 800: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
801. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 801: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 801: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
802. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 802: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 802: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
803. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 803: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 803: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
804. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 804: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 804: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
805. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 805: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 805: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
806. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 806: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 806: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
807. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 807: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 807: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
808. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 808: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 808: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
809. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 809: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 809: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
810. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 810: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 810: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
811. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 811: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 811: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
812. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 812: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 812: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
813. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 813: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 813: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
814. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 814: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 814: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
815. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 815: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 815: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
816. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 816: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 816: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
817. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 817: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 817: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
818. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 818: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 818: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
819. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 819: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 819: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
820. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 820: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 820: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
821. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 821: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 821: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
822. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 822: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 822: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
823. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 823: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 823: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
824. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 824: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 824: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
825. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 825: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 825: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
826. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 826: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 826: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
827. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 827: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 827: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
828. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 828: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 828: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
829. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 829: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 829: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
830. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 830: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 830: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
831. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 831: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 831: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
832. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 832: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 832: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
833. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 833: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 833: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
834. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 834: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 834: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
835. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 835: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 835: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
836. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 836: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 836: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
837. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 837: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 837: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
838. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 838: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 838: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
839. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 839: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 839: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
840. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 840: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 840: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
841. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 841: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 841: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
842. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 842: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 842: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
843. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 843: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 843: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
844. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 844: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 844: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
845. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 845: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 845: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
846. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 846: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 846: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
847. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 847: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 847: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
848. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 848: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 848: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
849. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 849: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 849: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
850. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 850: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 850: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
851. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 851: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 851: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
852. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 852: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 852: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
853. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 853: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 853: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
854. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 854: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 854: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
855. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 855: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 855: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
856. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 856: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 856: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
857. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 857: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 857: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
858. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 858: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 858: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
859. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 859: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 859: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
860. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 860: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 860: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
861. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 861: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 861: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
862. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 862: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 862: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
863. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 863: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 863: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
864. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 864: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 864: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
865. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 865: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 865: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
866. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 866: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 866: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
867. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 867: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 867: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
868. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 868: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 868: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
869. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 869: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 869: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
870. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 870: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 870: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
871. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 871: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 871: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
872. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 872: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 872: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
873. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 873: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 873: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
874. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 874: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 874: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
875. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 875: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 875: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
876. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 876: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 876: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
877. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 877: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 877: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
878. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 878: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 878: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
879. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 879: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 879: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
880. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 880: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 880: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
881. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 881: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 881: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
882. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 882: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 882: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
883. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 883: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 883: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
884. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 884: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 884: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
885. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 885: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 885: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
886. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 886: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 886: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
887. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 887: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 887: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
888. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 888: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 888: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
889. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 889: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 889: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
890. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 890: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 890: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
891. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 891: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 891: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
892. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 892: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 892: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
893. Fase Evaluation: Quality Agent lê `recommendation_draft.json` e escreve `evaluation_verdict.json` para aprovar somente se segurança, preço, estoque e clareza passarem.
   Evidência 893: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 893: o Orchestrator só avança quando o estado da fase Evaluation está persistido e verificável.
894. Fase Cart: Order Agent lê `evaluation_verdict.json` e escreve `order_state.json` para criar pedido com o SKU aprovado.
   Evidência 894: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 894: o Orchestrator só avança quando o estado da fase Cart está persistido e verificável.
895. Fase Payment: Payment Agent lê `order_state.json` e escreve `payment_state.json` para confirmar Pix simulado no valor exato.
   Evidência 895: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 895: o Orchestrator só avança quando o estado da fase Payment está persistido e verificável.
896. Fase Fulfillment: Fulfillment Agent lê `payment_state.json` e escreve `fulfillment_state.json` para abrir separação e avisar rastreio.
   Evidência 896: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 896: o Orchestrator só avança quando o estado da fase Fulfillment está persistido e verificável.
897. Fase Awareness: Planner lê `customer_message.json` e escreve `plan.json` para classificar que Marina iniciou uma jornada de compra e não uma dúvida genérica.
   Evidência 897: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 897: o Orchestrator só avança quando o estado da fase Awareness está persistido e verificável.
898. Fase Discovery: Discovery Agent lê `customer_message.json` e escreve `customer_profile.json` para extrair objetivo, restrição sem lactose, orçamento e sabor.
   Evidência 898: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 898: o Orchestrator só avança quando o estado da fase Discovery está persistido e verificável.
899. Fase Catalog: Catalog Agent lê `customer_profile.json` e escreve `catalog_snapshot.json` para filtrar SKU seguro em estoque e abaixo de R$ 150.
   Evidência 899: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 899: o Orchestrator só avança quando o estado da fase Catalog está persistido e verificável.
900. Fase Recommendation: Recommendation Agent lê `catalog_snapshot.json` e escreve `recommendation_draft.json` para gerar mensagem de recomendação com justificativa humana.
   Evidência 900: Marina continua protegida contra produto com lactose, preço acima de R$ 150 e troca de SKU.
   Decisão 900: o Orchestrator só avança quando o estado da fase Recommendation está persistido e verificável.
