---
title: "Solução do Exercício 02: Pipeline Multi-Agent da Jornada KODA"
type: curriculum-solution
nivel: 4
aliases: []
tags: [curriculo-conteudo, nivel-4, solucao, multi-agent-pipeline, state-machine, journey-stage, file-based-coordination, guard-conditions, customer-journey, discovery-agent, catalog-agent, order-agent, fulfillment-agent, retention-agent, python, implementacao-referencia]
last_updated: 2026-06-10
---
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
+--------------------------------------------------------------------------------------+
|                         PIPELINE MULTI-AGENT KODA, EXERCÍCIO 02                      |
+--------------------------------------------------------------------------------------+

                                +-------------------------+
                                | Cliente no WhatsApp     |
                                | Marina envia intenção   |
                                +------------+------------+
                                             | customer_message.json
                                             v
+--------------------------------------------------------------------------------------+
| ORCHESTRATOR                                                                         |
| Controla ordem, retries, fallback, métricas e passagem entre fases                    |
+------------+-------------------------------------------------------------------------+
             |
             v
      +-------------+      plan.json
      | Planner     |--------------------------------------------------------------+
      +------+------+                                                              |
             |                                                                     |
             v                                                                     |
      +-------------+      discovery_state.json      customer_profile.json          |
      | Discovery   |---------------------------------------------------------+     |
      +------+------+                                                         |     |
             |                                                                |     |
             v                                                                |     |
      +-------------+      catalog_snapshot.json                               |     |
      | Catalog     |----------------------------------------------------+     |     |
      +------+------+                                                    |     |     |
             |                                                           |     |     |
             v                                                           |     |     |
      +-------------+      recommendation_draft.json                      |     |     |
      | Generator   |----------------------------------------------+      |     |     |
      +------+------+                                              |      |     |     |
             |                                                     |      |     |     |
             v                                                     |      |     |     |
      +-------------+      evaluation_verdict.json                 |      |     |     |
      | Evaluator   |----------------------------------------------+      |     |     |
      +------+------+                                                     |     |     |
             |                                                            |     |     |
             | aprovado                                                   |     |     |
             v                                                            |     |     |
      +-------------+      order_state.json                               |     |     |
      | Order       |-----------------------------------------------------+     |     |
      +------+------+                                                           |     |
             |                                                                  |     |
             v                                                                  |     |
      +-------------+      payment_state.json                                    |     |
      | Payment     |------------------------------------------------------------+     |
      +------+------+                                                                 |
             |                                                                         |
             v                                                                         |
      +-------------+      fulfillment_state.json                                       |
      | Fulfillment |-------------------------------------------------------------------+
      +-------------+

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

## 🧬 Conexão com Níveis 1, 2 e 3

Esta solução do Nível 4 não existe no vácuo. Cada decisão de código e arquitetura aplica conceitos que você estudou nos três níveis anteriores. A tabela abaixo mostra exatamente onde cada padrão aparece no pipeline.

### Nível 1 → Esta solução

| Conceito do Nível 1 | Onde aparece nesta solução | Como protege o pipeline |
|---|---|---|
| Context Amnesia (Problema 1) | `customer_profile.json` e `catalog_snapshot.json` persistem restrições, orçamento e inventário | Se o Generator perder contexto durante retry, relê os arquivos — a restrição "sem lactose" nunca depende de memória efêmera |
| Token Budgeting | O Planner divide a jornada em etapas pequenas, cada agente recebe apenas o contexto que precisa | Um agente que tentasse processar awareness, recommendation E payment em uma única janela esgotaria tokens e misturaria responsabilidades |
| Planning/Execution Collapse (Problema 2) | `plan.json` separa o planejamento (Planner) da execução (Discovery → Fulfillment) | O Generator não decide o escopo da tarefa — ele recebe um plano pronto e executa. O Orchestrator garante que nenhuma etapa pule |
| Self-Evaluation Collapse (Problema 3) | Generator e Evaluator são agentes separados com incentivos opostos | O Generator cria com temperatura alta e confiança. O Evaluator verifica com rubrica rígida e temperatura baixa. Sycophancy é estruturalmente bloqueada |
| Basic Harness Patterns | Cada agente tem validação de entrada e saída, fallback próprio e limite de retries | Se o Catalog retorna lista vazia, o fallback do Catalog é acionado — não o fallback genérico do Orchestrator |

### Nível 2 → Esta solução

| Padrão do Nível 2 | Implementação nesta solução | Ganho mensurável |
|---|---|---|
| Generator/Evaluator | `Recommendation Agent` (Generator) + `Quality Agent` (Evaluator) com loop de feedback via `evaluation_verdict.json` | O Evaluator rejeita recomendação com lactose ou acima do orçamento; o Generator recebe feedback específico e corrige na segunda tentativa |
| Sprint Contracts | Cada state file é um contrato: `discovery_state.json` declara seu schema, `catalog_snapshot.json` declara quais campos são obrigatórios | Se o Catalog entrega SKU sem o campo `lactose_free`, o Generator rejeita a entrada em vez de assumir um valor padrão |
| Rubric Design | `Evaluator.rubric` define 5 critérios com pesos: segurança (35%), orçamento (25%), estoque (20%), clareza (15%), coerência (5%) | Score final ponderado decide aprovação. Um produto seguro mas caro pode passar, mas um barato com lactose é bloqueado independentemente dos outros critérios |
| Trace Reading | `audit_log.jsonl` registra cada transição de fase, score, retry e fallback | Se Marina reclamar, o trace mostra exatamente: "turno 12, Generator tentativa 2, Evaluator score 0.81, critério reprovado: lactose_present" |

### Nível 3 → Esta solução

| Conceito do Nível 3 | Implementação | Por que foi necessário aqui |
|---|---|---|
| Multi-Agent Systems | 8 agentes independentes (Planner, Discovery, Catalog, Generator, Evaluator, Order, Payment, Fulfillment) orquestrados por um harness central | Um agente único não teria capacidade de raciocinar sobre awareness e fulfillment na mesma janela sem degradação. A separação permite que cada um use temperatura e tokens otimizados para sua tarefa |
| State Persistence | 8 arquivos JSON + 1 audit log JSONL persistem toda transição em disco | Se o processo cair entre Payment e Fulfillment, o Orchestrator relê `payment_state.json` e retoma do ponto exato, sem cobrar duas vezes e sem perder o pedido |
| File-Based Coordination | Comunicação entre agentes via arquivos no diretório `state/{customer_id}/`, sem memória compartilhada, sem fila, sem REST | Auditabilidade total: abrir `evaluation_verdict.json` mostra exatamente qual critério falhou, quando, e com qual evidência. Em produção, esse mesmo contrato migra para uma API sem mudar o modelo mental |
| Harness Evolution | O Orchestrator abstrai a ordem dos agentes; remover ou adicionar um agente não requer reescrever os demais | Se amanhã o time decidir inserir um `FraudCheckAgent` entre Payment e Fulfillment, basta adicionar o agente e um state file — os outros agentes continuam intactos |

### O fio condutor

O que conecta Nível 1, 2 e 3 a esta solução não é memorização de padrões — é um princípio arquitetural que se repete em toda a pilha:

> **Nenhum agente decide sozinho sobre segurança do cliente.**

No Nível 1, você aprendeu que agentes esquecem. Aqui, `customer_profile.json` existe para que lactose nunca seja esquecida.

No Nível 2, você aprendeu que agentes não sabem se autoavaliar. Aqui, o Evaluator existe para que nenhum Generator aprove a própria recomendação.

No Nível 3, você aprendeu que sistemas multi-agent precisam de coordenação explícita. Aqui, o Orchestrator e os state files existem para que a ordem das etapas seja contratual, não acidental.

E no Nível 4, você está vendo esses três princípios operando juntos em uma jornada comercial real. Não é teoria. É o KODA em produção.

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

Nesta etapa, o Planner interpreta a mensagem de Marina e conclui que a intenção é compra, não uma dúvida genérica. Ele organiza a jornada em um plano explícito, destacando a restrição sem lactose, o teto de R$ 150 e a preferência por chocolate. O resultado vai para `plan.json`, que funciona como checkpoint para as próximas fases e como contrato de avanço do Orchestrator. Se algo faltar aqui, todo o restante do fluxo nasce com contexto incompleto.

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

O Discovery Agent transforma a mensagem em um perfil estruturado e confirma os detalhes que realmente importam para a venda. Ele registra em `customer_profile.json` a restrição sem lactose, o orçamento de R$ 150 e a preferência por chocolate, além de qualquer evidência útil para explicar a decisão. Esse arquivo vira a fonte única para Catalog e Recommendation, evitando releituras divergentes do texto cru. A etapa reduz a chance de uma recomendação insegura por falta de contexto.

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

O Catalog Agent cruza o perfil com o estoque e elimina qualquer SKU fora da regra, priorizando opções sem lactose, dentro do orçamento e realmente disponíveis. Ele escreve `catalog_snapshot.json` com o recorte elegível e com o motivo da exclusão do restante, para que a próxima etapa não precise refazer a triagem. Isso protege a jornada contra inventário imaginário e mantém a recomendação ancorada em opções reais. Para Marina, a função desta fase é reduzir a lista até sobrar apenas o que ainda faz sentido.

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

Aqui o agente de Recommendation atua como Generator e monta um rascunho de recomendação em linguagem natural. Ele combina o perfil de Marina com o snapshot do catálogo para justificar por que aquele item atende à restrição sem lactose, ao orçamento e ao sabor desejado. O artefato `recommendation_draft.json` guarda a proposta antes de qualquer aprovação automática, permitindo revisão rastreável. Se o draft ficar vago ou exagerado, a etapa seguinte consegue apontar exatamente o que precisa melhorar.

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

O Quality Agent lê o rascunho e verifica se a recomendação é segura, fiel ao catálogo e clara para Marina. Em vez de aprovar a melhor frase, ele compara critérios objetivos e escreve `evaluation_verdict.json` com o resultado da checagem e o feedback necessário para revisão. Quando rejeita, a mensagem volta com instruções específicas, não com uma reprovação genérica. Isso transforma a avaliação em proteção real antes de a recomendação virar pedido.

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

Depois da aprovação, o Order Agent converte a recomendação validada em pedido e grava `order_state.json`. Ele fixa o SKU, o valor e os dados de checkout para que o restante da jornada opere sobre um estado consistente, não sobre texto solto. Essa etapa é onde a intenção vira compromisso operacional, então o contrato precisa estar fechado. Para Marina, isso evita troca de produto na reta final.

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

O Payment Agent confere o pagamento simulado e escreve `payment_state.json` apenas quando o valor confere com o pedido. Ele garante que a cobrança corresponda ao que foi aprovado e que não haja divergência entre o que Marina viu e o que o sistema registrou. Se o valor destoar, a etapa não avança e o Orchestrator recebe um sinal claro de falha. Isso impede que um checkout incorreto contamine o fulfillment.

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

O Fulfillment Agent usa o pagamento confirmado para abrir separação, registrar rastreio e persistir `fulfillment_state.json`. Aqui a jornada deixa de ser promessa e passa a refletir uma operação já encaminhada no mundo real, com evidência suficiente para acompanhamento. O artefato final permite notificar Marina com número de rastreio e previsão, sem depender de memória efêmera. É o fechamento do ciclo: do sinal inicial ao status operacional auditável.

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

### Exemplos de state files gerados (caso Marina)

Abaixo está o conteúdo real que o pipeline gera para cada arquivo de estado na execução bem-sucedida da jornada de Marina. Use estes exemplos como referência de contrato ao estender o pipeline.

**`customer_profile.json`** — gerado pelo Discovery Agent:
```json
{
  "schema_version": "1.0",
  "customer_id": "wa_5511998765432",
  "name": "Marina",
  "goal": "pre_treino",
  "dietary_restrictions": ["intolerancia_lactose"],
  "budget_brl": 150,
  "preferred_flavor": "chocolate",
  "training_context": "retomando_treinos",
  "confidence_scores": {
    "goal": 0.95,
    "lactose_restriction": 0.98,
    "budget": 0.90,
    "flavor": 1.0
  },
  "created_at": "2026-05-28T18:42:00Z"
}
```

**`catalog_snapshot.json`** — gerado pelo Catalog Agent:
```json
{
  "schema_version": "1.0",
  "requested_by": "customer_profile.json",
  "eligible": [
    {
      "sku": "PRE-WHEY-CHOC-900",
      "name": "KODA Pré-Treino Cacao Focus sem Lactose",
      "price_brl": 139.90,
      "lactose_free": true,
      "flavor": "chocolate",
      "stock_qty": 23,
      "warehouse": "SP-CENTRO-01",
      "servings": 30
    }
  ],
  "excluded": [
    {"sku": "PRE-CAFE-LACT-500", "reason": "lactose_present"},
    {"sku": "PRE-TREINO-MOR-600", "reason": "flavor_mismatch"},
    {"sku": "PRE-PREMIUM-CHOC-300", "reason": "budget_exceeded", "price_brl": 189.90},
    {"sku": "PRE-CAFE-ZER-500", "reason": "out_of_stock"}
  ],
  "snapshot_at": "2026-05-28T18:42:01Z"
}
```

**`recommendation_draft.json`** — gerado pelo Generator (tentativa 1):
```json
{
  "generation_id": "gen_1",
  "iteration": 1,
  "candidate_response": "Marina, recomendo o KODA Pré-Treino Cacao Focus! Ele é sem lactose, custa R$ 139,90 e tem sabor chocolate como você prefere. Perfeito para retomar os treinos com energia.",
  "products_considered": [
    {"sku": "PRE-WHEY-CHOC-900", "name": "KODA Pré-Treino Cacao Focus sem Lactose", "price_brl": 139.90, "lactose_free": true, "flavor": "chocolate"}
  ],
  "assumptions": ["cliente retomando treinos — prefere dose moderada", "chocolate é preferência declarada e confirmada"],
  "generated_at": "2026-05-28T18:42:02Z"
}
```

**`evaluation_verdict.json`** — gerado pelo Evaluator (aprova na tentativa 2):
```json
{
  "verdict_id": "eval_2",
  "iteration": 2,
  "verdict": "APPROVED",
  "rubric_results": [
    {"criterion": "lactose_free", "passed": true, "evidence": "SKU PRE-WHEY-CHOC-900 marcado lactose_free=true"},
    {"criterion": "budget_respected", "passed": true, "evidence": "R$ 139.90 <= R$ 150.00"},
    {"criterion": "flavor_match", "passed": true, "evidence": "flavor=chocolate confere com preferred_flavor"},
    {"criterion": "clarity", "passed": true, "evidence": "resposta menciona restrição, preço e sabor em linguagem natural"},
    {"criterion": "stock_confirmed", "passed": true, "evidence": "23 unidades em SP-CENTRO-01"}
  ],
  "overall_score": 0.94,
  "checked_at": "2026-05-28T18:42:03Z"
}
```

**`order_state.json`** — gerado pelo Order Agent:
```json
{
  "order_id": "KDA-8F3A21",
  "sku": "PRE-WHEY-CHOC-900",
  "qty": 1,
  "unit_price_brl": 139.90,
  "total_brl": 139.90,
  "customer_id": "wa_5511998765432",
  "shipping_address": "São Paulo, SP",
  "status": "confirmed",
  "created_at": "2026-05-28T18:42:04Z"
}
```

**`payment_state.json`** — gerado pelo Payment Agent:
```json
{
  "payment_id": "PIX-KDA-8F3A21",
  "order_id": "KDA-8F3A21",
  "method": "pix",
  "amount_brl": 139.90,
  "status": "confirmed",
  "reference": "pix_kda_8f3a21_20260528",
  "confirmed_at": "2026-05-28T18:42:05Z"
}
```

**`fulfillment_state.json`** — gerado pelo Fulfillment Agent:
```json
{
  "ticket_id": "FUL-7729KDA",
  "order_id": "KDA-8F3A21",
  "warehouse": "SP-CENTRO-01",
  "carrier": "KODA Entregas",
  "tracking_code": "BR482913775KDA",
  "estimated_delivery": "2026-05-30",
  "notification_sent": true,
  "created_at": "2026-05-28T18:42:06Z"
}
```

---

## 🔧 Debug e Troubleshooting do Pipeline

Quando o pipeline falha, a primeira reação não deve ser "melhorar o prompt". Deve ser abrir o state file da etapa que falhou. Esta seção mostra o roteiro de diagnóstico para cada ponto de falha comum.

### Diagnóstico por sintoma

| Sintoma | State file para abrir primeiro | O que procurar | Ação provável |
|---|---|---|---|
| Planner cria plano errado (ex: trata compra como dúvida) | `plan.json` | Campo `current_goal` — está correto? A mensagem original está preservada em `customer_message.json`? | Revisar heurística de `identify_goal()` no Planner. Adicionar palavras-chave que o caso real usa |
| Discovery não extrai restrição | `discovery_state.json` → campo `confidence` para lactose | O score de confiança está abaixo do threshold? O campo `evidence` mostra que a restrição foi encontrada na mensagem? | Ajustar `extract_constraints()` para reconhecer variações como "não posso lactose", "intolerante a leite" |
| Catalog retorna lista vazia | `catalog_snapshot.json` → campos `eligible` e `excluded` | Todos os SKUs estão em `excluded`? Qual campo (lactose, preço, estoque) motivou a exclusão de cada um? | Ampliar catálogo simulado ou revisar regras de filtro. Verificar se `budget_brl` foi interpretado corretamente |
| Generator produz recomendação genérica | `recommendation_draft.json` → campo `products_considered` | A lista está vazia? O campo `assumptions` revela que o agente ignorou restrições? | O Generator pode estar recebendo `catalog_snapshot` vazio. Verificar etapa anterior primeiro |
| Evaluator rejeita sistematicamente (3 retries) | `evaluation_verdict.json` das 3 tentativas | O mesmo critério falha nas 3? O feedback está sendo interpretado pelo Generator? As tentativas seguintes mudam algo ou repetem o mesmo erro? | Se o mesmo critério falha sempre, a rubrica pode estar impossível de satisfazer. Se o feedback é ignorado, o Generator não está lendo `feedback.json` |
| Order cria pedido com SKU errado | `order_state.json` | O `sku` no pedido confere com o `sku` aprovado em `evaluation_verdict.json`? | Bug no Order Agent: está lendo o draft em vez do verdict. Corrigir `input` do Order para apontar para `evaluation_verdict.json` |
| Payment falha com valor divergente | `payment_state.json` vs `order_state.json` | O `total_brl` no pagamento é igual ao `total_brl` no pedido? | Erro de arredondamento ou desconto aplicado duas vezes. Adicionar validação de `abs(payment.total - order.total) < 0.01` |
| Fulfillment não gera rastreio | `fulfillment_state.json` | O campo `tracking_code` está presente? O `payment_status` em `payment_state.json` é `confirmed`? | Verificar se o Fulfillment Agent está condicionado corretamente ao status do pagamento |

### Fluxo de diagnóstico rápido

```
1. Identifique a etapa que falhou (via trace do Orchestrator ou log de erro)
   │
2. Abra o state file de ENTRADA da etapa
   └─ O agente recebeu dados corretos?
      ├─ SIM → o problema está na lógica interna do agente
      └─ NÃO → o problema está na etapa ANTERIOR
         └─ Volte ao passo 1 para a etapa anterior
   │
3. Abra o state file de SAÍDA da etapa
   └─ O output tem os campos obrigatórios?
      ├─ SIM mas valores errados → revisar a função de processamento
      └─ NÃO (campos ausentes) → revisar a serialização do agente
   │
4. Compare entrada e saída com a mesma etapa em uma execução bem-sucedida
   └─ O que mudou no input que causou o desvio?
```

### Checklist pré-produção

Antes de considerar este pipeline pronto para produção, verifique:

- [ ] Todos os arquivos de estado têm `schema_version` no campo raiz
- [ ] O Orchestrator registra `error_logged` em `audit_log.jsonl` em todo fallback
- [ ] Nenhum agente escreve em state file de outro agente (respeito a contrato)
- [ ] O diretório `state/` é limpo entre execuções de teste (evita contaminação)
- [ ] O `max_iterations=3` é respeitado em todos os loops de retry
- [ ] Fallback de Payment nunca promete captura antes de confirmação
- [ ] Fallback de Fulfillment nunca gera rastreio falso
- [ ] Todos os `dataclass` têm validação de tipos nos campos críticos (`price_brl >= 0`, `lactose_free: bool`)
- [ ] O caso Marina roda do início ao fim sem intervenção manual

### Padrões de erro e suas correções

Estes são os erros mais comuns que aparecem quando o time começa a executar o pipeline com dados reais, e como corrigi-los sem reescrever a arquitetura.

**Erro 1: `FileNotFoundError` ao ler state file de etapa anterior**

Sintoma: o Catalog Agent falha com "Arquivo necessário não encontrado: customer_profile.json".

Causa provável: o Orchestrator está executando os agentes em paralelo em vez de sequencial, ou o Discovery Agent falhou silenciosamente sem lançar exceção.

Correção: verifique a ordem no `run_pipeline()`. O Catalog só pode rodar DEPOIS do Discovery. Adicione um assert explícito: `assert Path("state/.../customer_profile.json").exists(), "Discovery Agent deve rodar antes do Catalog"`.

**Erro 2: `KeyError: 'lactose_free'` no Evaluator**

Sintoma: o Evaluator tenta acessar `p.get("lactose_free")` e o campo não existe no dicionário do produto.

Causa provável: o Catalog Agent está populando `eligible` com produtos que não têm o campo `lactose_free`, ou o Generator está referenciando um SKU fora do snapshot.

Correção: adicione validação de schema no Catalog Agent. Todo produto em `eligible` DEVE ter `lactose_free: bool`. Se um SKU do catálogo real não tem esse campo, o Catalog deve marcá-lo como `excluded` com razão `missing_lactose_info`.

**Erro 3: Loop infinito Generator → Evaluator**

Sintoma: o pipeline fica preso em retry, consumindo tokens sem produzir aprovação.

Causa provável: o feedback do Evaluator é genérico ("melhore a recomendação") em vez de específico ("substitua SKU X por Y porque X contém lactose").

Correção: revise a função `evaluator_agent()`. Todo `RubricResult` com `passed=False` deve incluir `evidence` e, idealmente, `fix_instruction`. O Generator deve ler `fix_instruction` e aplicá-la, não reinterpretar o problema.

**Erro 4: `payment_state.json` com valor diferente de `order_state.json`**

Sintoma: o Payment Agent registra R$ 139.90 mas o Order Agent registrou R$ 149.90.

Causa provável: o Payment Agent está recalculando o total a partir dos itens em vez de ler `total_brl` diretamente de `order_state.json`. Arredondamento ou desconto aplicado duas vezes.

Correção: faça o Payment Agent ler `total_brl` do `order_state.json` como valor canônico. Não recalcule. Adicione validação: `if abs(payment_amount - order_total) > 0.01: raise ValueError("Payment amount diverges from order total")`.

**Erro 5: `fulfillment_state.json` sem `tracking_code`**

Sintoma: o Fulfillment Agent roda mas o campo `tracking_code` está vazio.

Causa provável: o status do pagamento em `payment_state.json` não é `"confirmed"` e o Fulfillment Agent não validou essa condição antes de prosseguir.

Correção: adicione guarda explícita no Fulfillment Agent: `if payment_state.get("status") != "confirmed": return fallback_fulfillment("pagamento não confirmado")`.

**Erro 6: `plan.json` com `current_goal` errado após mudança de intenção**

Sintoma: o cliente começa perguntando sobre whey, mas muda para creatina. O plano continua apontando para whey.

Causa provável: o Planner não tem um mecanismo de reavaliação. O `plan.json` é escrito uma vez e nunca revisado.

Correção: adicione um `IntentChangeDetector` no Orchestrator. Antes de cada turno, compare a mensagem atual com o `current_goal` do plano. Se houver divergência (ex: cliente fala de creatina mas plano diz whey), chame o Planner novamente com `replan=True`.

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

Em produção, essa tabela serve como painel de triagem, não como relatório para arquivar. Quando a latência do Planner ou do Discovery sobe, a primeira leitura deve ser o estado gerado e o prompt, porque o sintoma costuma ser escopo excessivo, parsing caro ou contexto desnecessário. Se o Catalog ou o Generator piora, vale comparar o JSON de entrada com o snapshot anterior para descobrir se o problema está no inventário, na expansão de contexto ou na estratégia de geração.

Retry rate crescente pede atenção ao feedback do Evaluator. Se o draft volta várias vezes, a equipe deve abrir `evaluation_verdict.json` e verificar se os critérios estão objetivos o suficiente ou se a rubrica está punindo coisas diferentes em tentativas diferentes. Já um fallback disparando acima do esperado indica que o contrato da etapa está quebrando de forma repetida, então a análise precisa ir para a última fase que mudou estado antes do fallback.

Na prática, a equipe responde sempre às mesmas três perguntas: o problema está na entrada, na regra ou no handoff? O KPI aponta onde olhar primeiro, o trace do Orchestrator confirma em que tentativa ocorreu a degradação e o arquivo de estado mostra qual campo ficou inconsistente. Esse fluxo reduz discussão abstrata e encurta o caminho entre alerta e correção.

---

## 🧩 Como Estender Este Pipeline

O pipeline que você construiu é um template, não um produto fechado. Esta seção mostra três extensões reais que times KODA implementaram a partir desta mesma base.

### Extensão 1: Adicionar um FraudCheckAgent

**Problema:** antes de confirmar pagamento, você quer verificar se o cliente não tem histórico de chargeback ou comportamento suspeito.

**O que muda no pipeline:** insira um agente entre Payment e Fulfillment:

```
Payment Agent → payment_state.json
     │
     ▼
FraudCheckAgent → fraud_check_result.json
     │
     ├── approved ──► Fulfillment Agent
     └── flagged  ──► fallback: escalar para revisão manual
```

**Novo state file — `fraud_check_result.json`:**
```json
{
  "check_id": "FRD-8821",
  "order_id": "KDA-8F3A21",
  "customer_id": "wa_5511998765432",
  "risk_score": 0.12,
  "flags": [],
  "decision": "approved",
  "checked_at": "2026-05-28T18:42:06Z"
}
```

**Novo agente (esqueleto):**
```python
@dataclass
class FraudCheckResult:
    check_id: str
    order_id: str
    customer_id: str
    risk_score: float
    flags: list[str]
    decision: str  # "approved" ou "flagged"

def fraud_check_agent(payment_state: dict, customer_history: dict) -> FraudCheckResult:
    risk = 0.0
    flags = []
    if customer_history.get("chargeback_count", 0) > 0:
        risk += 0.6
        flags.append("prior_chargeback")
    if payment_state.get("amount_brl", 0) > 500:
        risk += 0.1
        flags.append("high_value_order")
    return FraudCheckResult(
        check_id=f"FRD-{uuid.uuid4().hex[:4].upper()}",
        order_id=payment_state["order_id"],
        customer_id=payment_state.get("customer_id", ""),
        risk_score=min(risk, 1.0),
        flags=flags,
        decision="flagged" if risk > 0.5 else "approved"
    )
```

**O que NÃO muda:** Planner, Discovery, Catalog, Generator, Evaluator, Order e Payment continuam exatamente iguais. Isso é harness evolution em prática — adicionar capacidade sem reescrever o que já funciona.

### Extensão 2: Substituir catálogo simulado por API real

**Problema:** o catálogo atual é uma lista em memória. Em produção, os produtos vêm de uma API REST com autenticação.

**O que muda:** apenas a função `fetch_catalog()` dentro do Catalog Agent. A interface com os outros agentes (entrada: `customer_profile.json`, saída: `catalog_snapshot.json`) permanece idêntica.

```python
# Antes (exercício):
SAMPLE_CATALOG = [Product(...), Product(...)]

def fetch_catalog() -> list[Product]:
    return SAMPLE_CATALOG

# Depois (produção):
import requests

def fetch_catalog(api_key: str, base_url: str) -> list[Product]:
    resp = requests.get(
        f"{base_url}/v1/products",
        headers={"Authorization": f"Bearer {api_key}"},
        params={"category": "suplementos", "in_stock": True},
        timeout=5
    )
    resp.raise_for_status()
    return [Product(**item) for item in resp.json()["products"]]
```

**Por que isso funciona:** o contrato do Catalog Agent diz "receba um perfil, devolva um snapshot". De onde os produtos vêm é detalhe de implementação. File-based coordination permite essa troca sem afetar nenhum outro agente.

### Extensão 3: Adicionar notificação pós-fulfillment via WhatsApp

**Problema:** depois que o Fulfillment Agent gera rastreio, você quer notificar a Marina automaticamente pelo WhatsApp.

**O que muda:** adicione um `NotificationAgent` após o Fulfillment:

```python
def notification_agent(fulfillment_state: dict, customer_profile: dict) -> dict:
    tracking = fulfillment_state["tracking_code"]
    eta = fulfillment_state["estimated_delivery"]
    product_name = "KODA Pré-Treino Cacao Focus"

    message = (
        f"{customer_profile['name']}, seu pedido foi separado! 🚀\n"
        f"Rastreio: {tracking}\n"
        f"Previsão de entrega: {eta}\n"
        f"Obrigado por confiar na KODA!"
    )

    # Em produção: chamar WhatsApp Business API
    # send_whatsapp_message(customer_profile["customer_id"], message)

    return {
        "notification_id": f"NOTIF-{uuid.uuid4().hex[:6].upper()}",
        "channel": "whatsapp",
        "recipient": customer_profile["customer_id"],
        "message_preview": message[:80],
        "status": "queued",
        "sent_at": datetime.now(timezone.utc).isoformat()
    }
```

### Princípio de extensão

Toda extensão segue o mesmo padrão de três passos:

1. **Defina o state file** — qual arquivo JSON o novo agente vai produzir? Quais campos são obrigatórios?
2. **Conecte entrada e saída** — de qual state file o novo agente lê? Para qual agente seguinte ele entrega?
3. **Adicione fallback** — o que acontece se o novo agente falhar 3 vezes? Quem é notificado?

Se você seguir esses três passos, qualquer novo agente se integra ao pipeline sem reescrever os existentes. Esse é o valor de uma arquitetura com contratos explícitos: crescer não significa refatorar.

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

## ❓ Perguntas Frequentes

### "Preciso mesmo de 8 agentes? Não é overengineering?"

Depende da criticidade da operação. Para uma venda de R$ 30 sem restrições, talvez não. Para o KODA, onde um erro de lactose pode prejudicar a saúde do cliente e gerar dano reputacional, cada agente existe para eliminar uma classe específica de falha. O Planner evita escopo confuso. O Discovery evita perda de restrição. O Catalog evita SKU inválido. O Generator evita resposta genérica. O Evaluator evita autoaprovação. Order, Payment e Fulfillment evitam que promessas de chat virem operações reais sem verificação. Oito agentes não é overengineering quando cada um reduz um risco que já causou prejuízo real.

### "Posso usar o mesmo modelo (Claude) para todos os agentes?"

Sim, e é o que o exercício faz. Mas em produção, você pode otimizar: use um modelo mais rápido e barato (Haiku) para Catalog (só filtra lista) e Order (só monta pedido), e reserve Opus para Planner e Evaluator (raciocínio mais complexo). O contrato de state file não muda — só a implementação interna de cada agente.

### "File-based coordination não fica lento em produção?"

Para o volume do KODA (centenas de conversas simultâneas, não milhões), funciona bem. O gargalo real não é I/O de arquivo — é latência de LLM. Se a operação crescer para milhares de conversas, você migra os state files mais quentes (`catalog_snapshot.json`, `evaluation_verdict.json`) para Redis ou PostgreSQL sem mudar o contrato. O modelo mental permanece o mesmo: agente lê JSON, produz JSON, próximo agente valida.

### "Como o pipeline lida com conversas simultâneas do mesmo cliente?"

Cada conversa tem seu próprio diretório de estado (`state/{customer_id}_{session_id}/`). O `customer_profile.json` pode ser compartilhado (o perfil do cliente é o mesmo), mas `plan.json`, `recommendation_draft.json` e os demais são isolados por sessão. Isso evita que duas conversas paralelas da Marina se contaminem.

### "O que acontece se o cliente mudar de ideia no meio da jornada?"

O Orchestrator detecta que o `current_goal` em `plan.json` não corresponde mais à intenção atual e chama o Planner novamente — mas agora com contexto de "o cliente mudou de ideia". O estado anterior não é descartado (fica no diretório para auditoria), mas uma nova ramificação é criada com `plan_v2.json`. Em produção, você adicionaria um `IntentChangeAgent` para gerenciar essa transição explicitamente.

### "Este pipeline funciona sem Claude? Posso usar GPT-4o ou Gemini?"

Sim. O pipeline é agnóstico de modelo. Cada agente chama `call_llm(prompt)` — a função interna pode apontar para Claude, GPT-4o, Gemini ou qualquer endpoint compatível com OpenAI API. O contrato (state files JSON) não depende do provedor. A única adaptação necessária é ajustar os system prompts para o estilo de resposta de cada modelo.

### "Qual a diferença entre este pipeline e um workflow do Temporal ou Airflow?"

Ferramentas como Temporal e Airflow orquestram tarefas determinísticas (ex: "chame API X, espere, chame API Y"). Este pipeline orquestra agentes de LLM, que são não-determinísticos por natureza. O state file não é só um checkpoint de progresso — é um contrato semântico. O Evaluator não verifica só "a etapa terminou?", mas "o output da etapa é seguro e correto?". Essa camada semântica de validação é o que diferencia pipelines de agentes de workflows tradicionais.

### "Posso paralelizar agentes que não dependem um do outro?"

Sim, e isso reduz latência significativamente. No pipeline atual, Discovery, Catalog e Recommendation são sequenciais. Mas você poderia paralelizar: enquanto o Planner roda, o Discovery já começa a extrair perfil. Ou, após o Catalog, rodar 3 Generators em paralelo com estratégias diferentes e depois um Evaluator consolidar. O Orchestrator precisaria gerenciar o `gather` dos resultados, mas os contratos de state file não mudam — cada agente ainda lê seu input e escreve seu output.

### "Como monitorar este pipeline em produção?"

Você precisa de três camadas de observabilidade:

1. **Métricas de negócio:** latência por etapa, retry rate, fallback rate, approval rate do Evaluator. Exporte via Prometheus ou similar a partir do Orchestrator.

2. **Logs estruturados:** cada evento do `audit_log.jsonl` deve ser enviado para um sistema de logging centralizado (CloudWatch, Datadog, Grafana Loki) com campos indexáveis: `session_id`, `agent`, `event_type`, `verdict`, `score`.

3. **Alertas:** defina thresholds. Se `fallback_rate > 5%` por 15 minutos, alerte o time de plantão. Se `evaluator_rejection_rate > 30%`, algo está errado com o catálogo ou com o prompt do Generator — investigue antes que clientes percebam.

O pipeline já produz os dados. A camada de observabilidade é o que transforma esses dados em ação.

### "O que mais muda quando este pipeline vai para produção de verdade?"

Além da infraestrutura (APIs reais, autenticação, observabilidade), três coisas que este exercício deliberadamente simplifica e que você precisará resolver:

1. **Tratamento de sessão:** o pipeline atual assume uma sessão por execução. Em produção, o Orchestrator precisa gerenciar múltiplas sessões simultâneas, cada uma com seu próprio diretório de estado e ciclo de vida.

2. **Gestão de timeout de LLM:** chamadas de API podem levar 30 segundos ou mais. O Orchestrator precisa de timeout configurável por agente e estratégia de retry com backoff exponencial.

3. **Versionamento de schema:** quando você adicionar um campo novo ao `customer_profile.json` (ex: `preferred_payment_method`), agentes antigos que não conhecem esse campo não podem quebrar. Adote `schema_version` desde o primeiro deploy e faça os agentes ignorarem campos desconhecidos.

Nenhuma dessas três coisas exige reescrever a arquitetura. São camadas que se adicionam sobre a base que você já construiu.

---

## ⚠️ Anti-Padrões Que Este Pipeline Evita

Reconhecer o que NÃO fazer é tão importante quanto saber o que fazer. Abaixo estão os anti-padrões que times de IA cometem — e que esta arquitetura foi desenhada para prevenir.

### Anti-padrão 1: "Agente Único Faz-Tudo"

**Sintoma:** um único prompt tenta cobrir awareness, recomendação, preço e checkout.

**Por que falha:** a janela de contexto mistura responsabilidades diferentes. O modelo confunde "entender o cliente" com "cobrar o cliente". Erros em uma etapa contaminam as demais. A latência é alta porque cada resposta processa o pipeline inteiro.

**Como esta solução evita:** 8 agentes com contratos de entrada e saída explícitos. Cada um recebe só o contexto que precisa.

### Anti-padrão 2: "Autoavaliação Confiante"

**Sintoma:** o mesmo agente que recomenda também aprova a própria recomendação.

**Por que falha:** sycophancy. O modelo sempre encontra uma razão para concordar consigo mesmo. A taxa de erro silencioso fica entre 10-15%.

**Como esta solução evita:** Generator e Evaluator são agentes separados com incentivos opostos. O Evaluator é medido por "quantos erros encontrou", não por "quantos aprovou".

### Anti-padrão 3: "Memória Implícita como Fonte da Verdade"

**Sintoma:** restrições do cliente (alergias, orçamento) existem apenas na janela de contexto do modelo.

**Por que falha:** quando a conversa cresce ou o contexto é comprimido, informações críticas somem silenciosamente. O agente "esquece" que o cliente é alérgico.

**Como esta solução evita:** `customer_profile.json` persiste restrições em disco. Todo agente que precisa delas relê o arquivo. Alergia não depende de memória.

### Anti-padrão 4: "Fallback Genérico"

**Sintoma:** qualquer erro em qualquer etapa ativa o mesmo fallback: "escalar para humano".

**Por que falha:** você perde a capacidade de diagnosticar qual etapa quebrou. "Humano resolve" vira a resposta padrão e o pipeline nunca amadurece.

**Como esta solução evita:** cada agente tem seu próprio fallback com mensagem específica. Se o Catalog falha, o fallback diz "não encontrei produtos com esses critérios". Se o Payment falha, o fallback diz "houve um problema com o pagamento". Diagnóstico preciso → correção rápida.

### Anti-padrão 5: "Retry Cego"

**Sintoma:** quando o Evaluator rejeita, o Generator tenta de novo sem receber feedback específico.

**Por que falha:** o Generator repete o mesmo erro porque não sabe o que corrigir. Três tentativas idênticas consomem tokens sem melhorar o resultado.

**Como esta solução evita:** o Evaluator escreve `feedback.json` com o critério exato que falhou (`lactose_present`, `budget_exceeded`). O Generator lê esse feedback e ajusta apenas o que precisa.

---

## 🗺️ Referência Rápida: Navegando Este Documento

| Se você quer... | Vá para... | Linha aproximada |
|---|---|---|
| Entender por que este exercício existe | Prólogo | topo do documento |
| Ver os requisitos completos do exercício | O Que o Exercício Pede | após o Prólogo |
| Estudar a arquitetura do pipeline | Arquitetura da Solução + Conexão com Níveis 1-3 | após requisitos |
| Copiar o código Python completo | Implementação Completa do Pipeline | seção 🐍 |
| Ver como cada agente é avaliado | Avaliação de Qualidade por Etapa | após implementação |
| Acompanhar uma execução real | Aplicação KODA — Caso Concreto | seção 🚀 |
| Diagnosticar falhas no pipeline | Debug e Troubleshooting | antes das métricas |
| Estender o pipeline com novos agentes | Como Estender Este Pipeline | antes do resumo |
| Evitar erros comuns de design | Anti-Padrões Que Este Pipeline Evita | antes do fechamento |
| Tirar dúvidas conceituais | Perguntas Frequentes | seção ❓ |

### Navegação por state file

| State file | Quem escreve | Quem lê | Onde é discutido |
|---|---|---|---|
| `customer_message.json` | Sistema (entrada) | Planner, Discovery | Prólogo, Requisitos |
| `plan.json` | Planner | Orchestrator, Generator | Conexão com Níveis, Etapa 1 |
| `customer_profile.json` | Discovery Agent | Catalog, Generator, Evaluator | Etapa 2, Debug erro 1 |
| `discovery_state.json` | Discovery Agent | Catalog (validação) | Avaliação de Qualidade |
| `catalog_snapshot.json` | Catalog Agent | Generator | Etapa 3, Extensão 2 |
| `recommendation_draft.json` | Generator | Evaluator | Etapa 4, Exemplos JSON |
| `evaluation_verdict.json` | Evaluator | Orchestrator, Order | Etapa 5, Debug erro 3 |
| `feedback.json` | Evaluator (se rejeitado) | Generator (retry) | Anti-padrão 5 |
| `order_state.json` | Order Agent | Payment | Etapa 6, Debug erro 4 |
| `payment_state.json` | Payment Agent | Fulfillment | Etapa 7, Debug erro 4 |
| `fulfillment_state.json` | Fulfillment Agent | Notification (futuro) | Etapa 8, Debug erro 5 |
| `audit_log.jsonl` | Orchestrator | Time de operação | Checklist pré-produção |

### Comandos úteis para exploração

```bash
# Executar o pipeline completo com o caso Marina
python koda_customer_journey_pipeline.py

# Listar todos os arquivos de estado gerados
ls -la state/wa_5511998765432/

# Ver o plano gerado pelo Planner
cat state/wa_5511998765432/plan.json | python -m json.tool

# Ver o veredito do Evaluator
cat state/wa_5511998765432/evaluation_verdict.json | python -m json.tool

# Seguir o audit log em tempo real (durante execução)
tail -f state/wa_5511998765432/audit_log.jsonl

# Contar quantas vezes cada evento apareceu no log
cut -d'"' -f4 state/wa_5511998765432/audit_log.jsonl | sort | uniq -c | sort -rn

# Extrair apenas eventos de erro do log
grep "error\|rejected\|fallback" state/wa_5511998765432/audit_log.jsonl

# Comparar dois state files (ex: order vs payment)
diff <(cat state/wa_5511998765432/order_state.json | python -m json.tool) \
     <(cat state/wa_5511998765432/payment_state.json | python -m json.tool)
```

---

Um trace completo de produção teria centenas de entradas — o conceito importante é que cada entrada liga evidência, decisão e proteção. Quando o time mantém esse vínculo, auditoria, debugging e evolução de prompt deixam de depender de memória humana e passam a seguir o mesmo contrato do sistema.

---
