# 🏋️ Exercício 2: Implementar Pipeline Completo de Customer Journey com Agentes Coordenados
## Nível 4 — KODA-Específico

**Tempo Estimado:** 120-180 minutos
**Dificuldade:** ⭐⭐⭐⭐⭐ (Expert)
**Pré-requisito:** Ter lido `01-koda-architecture.md` + `02-customer-journey-flows.md` + ter completado Nível 3
**Objetivo:** Construir um pipeline de 4 estágios com 7 agentes coordenados via file-based state persistence que cobre a jornada completa: discovery → recomendação → pedido → pós-venda

---

## 📖 Prólogo: A Terça-Feira em Que o KODA Perdeu um Cliente de R$ 380... e Depois o Recuperou

**Terça-feira, 10h42. Loja FutanBear. WhatsApp corporativo.**

Patrícia tinha 34 anos, treinava há 8 meses e nunca havia comprado suplementos online. Uma amiga recomendou a FutanBear. Ela abriu o WhatsApp com uma única certeza: queria algo para ajudar na recuperação pós-treino.

Não sabia que existia whey protein, creatina, BCAA, glutamina, beta-alanina. Não sabia a diferença entre concentrado, isolado e hidrolisado. Não sabia que era intolerante à lactose — só descobriria isso na conversa, quando o KODA perguntou se ela sentia desconforto depois de tomar leite.

Ela também não sabia que sua jornada inteira — da primeira mensagem até o pedido entregue e o follow-up 60 dias depois — seria orquestrada por **sete agentes diferentes**, cada um com uma responsabilidade clara e finita, coordenados por arquivos JSON que jamais mentem.

O que Patrícia sabia era simples: *"Oi, quero algo pra me recuperar melhor depois do treino. Meu orçamento é R$ 200."*

Vinte e dois minutos depois, ela teria fechado um pedido de R$ 178,90. Sessenta dias depois, ela compraria de novo. E seis meses depois, ela seria uma cliente fiel com ticket médio de R$ 340.

Mas antes disso, às 10h42 daquela terça-feira, aconteceu algo que quase custou tudo.

O KODA original — um agente único, sem pipeline, sem coordenação, sem estado — recebeu a mensagem da Patrícia e fez o que agentes únicos sempre fazem com clientes novos: **tentou fazer tudo ao mesmo tempo**.

Ele perguntou o objetivo. Depois perguntou o orçamento. Depois recomendou um whey. Depois sugeriu uma creatina. Depois tentou fechar o pedido. Depois esqueceu o orçamento. Depois recomendou um produto com lactose para uma cliente que havia mencionado desconforto com leite. Depois processou o pagamento com o CEP errado. Depois não fez follow-up. Depois perdeu a cliente.

A culpa não era do modelo. O Claude Opus que rodava o KODA era excelente. A culpa era da **arquitetura**: um agente só tentando ser planner, vendedor, caixa, suporte e gerente de relacionamento ao mesmo tempo.

Foi aí que a equipe KODA desenhou o que você vai implementar hoje.

Em vez de um agente, **sete**. Em vez de uma conversa linear, **uma máquina de estados com quatro estágios e guard conditions**. Em vez de memória frágil dentro da context window, **state persistence em arquivos JSON que sobrevivem a crashes, reinicializações e conversas de 4 horas**.

Este exercício é a síntese de tudo que você aprendeu nos Níveis 1, 2 e 3. Não é um exercício sobre um padrão. É um exercício sobre **todos os padrões orquestrados juntos**.

Você vai construir um sistema que recebe uma mensagem de WhatsApp, classifica a intenção, coleta contexto, aplica restrições, recomenda produtos com evidência, processa pagamento, gerencia fulfillment e agenda follow-up. Tudo com agentes independentes, cada um lendo e escrevendo arquivos JSON que formam um audit trail completo.

E quando terminar, você não vai apenas *entender* como o KODA funciona.

Você vai poder **recriá-lo do zero**.

---

## 🎯 Objetivo

Você vai implementar um **harness de customer journey completo** com sete agentes especializados que colaboram para guiar um cliente por quatro estágios de jornada no KODA:

1. **Discovery Agent:** Classifica intenção da mensagem, coleta contexto inicial e decide se o cliente está pronto para avançar
2. **Catalog Agent:** Consulta o catálogo de produtos, aplica filtros (restrições alimentares, orçamento, preferências) e retorna candidatos
3. **Generator Agent:** Produz resposta natural e personalizada para o WhatsApp com os produtos recomendados
4. **Evaluator Agent:** Valida a resposta candidata contra restrições, rubricas de qualidade e regras de negócio antes de expor ao cliente
5. **Order Agent:** Processa checkout, confirma endereço, gerencia pagamento e cria o pedido
6. **Fulfillment Agent:** Gerencia tracking de entrega, confirma recebimento e atualiza status do pedido
7. **Retention Agent:** Agenda follow-ups, monitora recompra e gerencia re-engajamento

O sistema usa **file-based state persistence** — cada agente lê e escreve arquivos JSON no diretório `state/<conversation_id>/`. Isso cria um audit trail completo, permite retomar conversas após falhas e possibilita debugar cada decisão meses depois.

**Resultado Final:** Você entenderá na prática como orquestrar múltiplos agentes em um pipeline de negócio real, com máquina de estados, guard conditions, coordenação por arquivos e métricas de qualidade.

---

## 🔗 Conexão com os Níveis 1, 2 e 3

Este exercício consolida todo o currículo. Cada conceito que você aprendeu aparece aqui como uma peça do sistema:

| Nível | Conceito | Onde Aparece Neste Exercício |
|-------|----------|------------------------------|
| **Nível 1** | Token Budgeting | Cada agente recebe apenas o contexto necessário — state files evitam poluir a context window |
| **Nível 1** | Planning vs Execution | Discovery Agent planeja a jornada, Generator executa cada etapa |
| **Nível 1** | Self-Evaluation Collapse | Evaluator nunca é o Generator — sycophancy é bloqueada por design |
| **Nível 2** | Generator/Evaluator | Generator produz resposta, Evaluator aprova ou rejeita com feedback |
| **Nível 2** | Sprint Contracts | Cada transição de estágio é um contrato: entradas, saídas e guard conditions explícitas |
| **Nível 2** | Rubric Design | Evaluator usa rubricas objetivas (preço ≤ orçamento, lactose_free = True, etc.) |
| **Nível 2** | Trace Reading | Todo estado é arquivo JSON versionado — audit trail completo |
| **Nível 3** | Multi-Agent Systems | Sete agentes com responsabilidades separadas, orquestrados por pipeline |
| **Nível 3** | State Persistence | Estado persiste em arquivos — conversas sobrevivem a reinicializações |
| **Nível 3** | File-Based Coordination | Cada agente lê e escreve arquivos JSON como contrato de comunicação |
| **Nível 3** | Harness Evolution | O pipeline é modular — agentes podem ser substituídos ou removidos sem quebrar o sistema |

---

## 📋 Requisitos

### Funcionais

- [ ] Sistema recebe uma mensagem do cliente e determina o estágio atual da jornada
- [ ] Discovery Agent classifica intenção (`PRODUCT_DISCOVERY`, `ORDER_STATUS`, `SUPPORT`, `RICOMPRA`, etc.)
- [ ] Discovery Agent coleta ou atualiza o perfil do cliente (restrições, preferências, orçamento)
- [ ] Catalog Agent filtra produtos por categoria, restrições alimentares, faixa de preço e disponibilidade
- [ ] Generator Agent produz resposta natural em português, tom de WhatsApp, personalizada ao cliente
- [ ] Evaluator Agent valida resposta contra rubricas de negócio e restrições do cliente
- [ ] Se Evaluator rejeita, Generator recebe feedback e tenta novamente (máximo 2 retries)
- [ ] Se 2 retries falham, sistema retorna fallback seguro
- [ ] Order Agent monta carrinho, confirma endereço, processa pagamento simulado
- [ ] Fulfillment Agent gera tracking, confirma entrega e atualiza status
- [ ] Retention Agent agenda follow-up baseado na duração estimada do produto
- [ ] Máquina de estados gerencia transições: AWARENESS → CONSIDERATION → DECISION → RETENTION
- [ ] Cada transição tem guard conditions explícitas
- [ ] Todo estado persiste em arquivos JSON no diretório `state/<conversation_id>/`
- [ ] Pipeline cobre todas as etapas da jornada (discovery, recomendação, pedido, pós-venda)
- [ ] Sistema de métricas mede: taxa de aprovação, latência, precisão de orçamento, taxa de conversão

### Não-Funcionais

- [ ] Código Python com type hints em todas as funções públicas
- [ ] Nenhum `except: pass` vazio
- [ ] Nenhum `# type: ignore`
- [ ] Arquivos JSON incluem `schema_version`, `conversation_id` e `timestamp`
- [ ] Escrita atômica de arquivos (usar `tempfile` para evitar corrupção)
- [ ] Funções são puras sempre que possível (recebem dados, retornam dados, não dependem de estado global)

---

## 📐 Arquitetura do Sistema

### Diagrama ASCII da Arquitetura Completa

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                    CUSTOMER JOURNEY PIPELINE — ARQUITETURA COMPLETA                        │
│                         7 Agentes · 4 Estágios · File-Based State                          │
└─────────────────────────────────────────────────────────────────────────────────────────┘

                              ┌──────────────────────┐
                              │    WHATSAPP CLIENT   │
                              │  (mensagem recebida) │
                              └──────────┬───────────┘
                                         │
                                         ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                     ORCHESTRATOR                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐ │
│  │                          run_customer_journey_turn()                                  │ │
│  │                                                                                       │ │
│  │  1. Carrega state.json do disco                                                       │ │
│  │  2. Determina estágio atual (AWARENESS/CONSIDERATION/DECISION/RETENTION)              │ │
│  │  3. Avalia guard conditions para transições                                           │ │
│  │  4. Executa pipeline do estágio com loop Generator/Evaluator                           │ │
│  │  5. Se aprovado: atualiza state.json e envia resposta                                  │ │
│  │  6. Se rejeitado após retries: fallback seguro                                         │ │
│  └─────────────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────────────┘
                                         │
         ┌───────────────────────────────┼───────────────────────────────┐
         │                               │                               │
         ▼                               ▼                               ▼
┌──────────────────┐          ┌──────────────────┐          ┌──────────────────┐
│   ESTÁGIO 1      │          │   ESTÁGIO 2      │          │   ESTÁGIO 3      │
│   AWARENESS      │          │   CONSIDERATION  │          │   DECISION        │
├──────────────────┤          ├──────────────────┤          ├──────────────────┤
│                  │          │                  │          │                  │
│ ┌──────────────┐ │          │ ┌──────────────┐ │          │ ┌──────────────┐ │
│ │ DISCOVERY    │ │          │ │ DISCOVERY    │ │          │ │ ORDER        │ │
│ │ AGENT        │─┤          │ │ (refinamento)│ │          │ │ AGENT        │ │
│ │              │ │          │ └──────┬───────┘ │          │ │              │ │
│ │ classifica   │ │          │        │         │          │ │ checkout     │ │
│ │ intenção     │ │          │        ▼         │          │ │ payment      │ │
│ │ coleta       │ │          │ ┌──────────────┐ │          │ │ confirmation │ │
│ │ contexto     │ │          │ │ CATALOG      │ │          │ └──────┬───────┘ │
│ └──────┬───────┘ │          │ │ AGENT        │ │          │        │         │
│        │         │          │ │              │ │          │        ▼         │
│        ▼         │          │ │ filtra       │ │          │ ┌──────────────┐ │
│ ┌──────────────┐ │          │ │ produtos     │ │          │ │ FULFILLMENT  │ │
│ │ GUARD CHECK  │ │          │ │ ranqueia     │ │          │ │ AGENT        │ │
│ │              │ │          │ └──────┬───────┘ │          │ │              │ │
│ │ contexto     │ │          │        │         │          │ │ tracking     │ │
│ │ suficiente?  │ │          │        ▼         │          │ │ delivery     │ │
│ └──────┬───────┘ │          │ ┌──────────────┐ │          │ │ status       │ │
│        │         │          │ │ GENERATOR    │ │          │ └──────────────┘ │
│   [NÃO]│  [SIM]  │          │ │ AGENT        │ │          │                  │
│     ┌──┘  └──┐   │          │ │              │ │          │                  │
│     │        │   │          │ │ resposta     │ │          └──────────────────┘
│     ▼        │   │          │ │ candidata    │ │                   │
│  CONTINUA    │   │          │ └──────┬───────┘ │                   │
│  AWARENESS   │   │          │        │         │                   ▼
│              │   │          │        ▼         │          ┌──────────────────┐
└──────────────┘   │          │ ┌──────────────┐ │          │   ESTÁGIO 4      │
                   │          │ │ EVALUATOR    │ │          │   RETENTION      │
                   │          │ │ AGENT        │ │          ├──────────────────┤
                   │          │ │              │ │          │                  │
                   │          │ │ valida       │ │          │ ┌──────────────┐ │
                   │          │ │ restrições   │ │          │ │ RETENTION    │ │
                   │          │ │ rubricas     │ │          │ │ AGENT        │ │
                   │          │ └──────┬───────┘ │          │ │              │ │
                   │          │        │         │          │ │ follow-up    │ │
                   │          │  [REJ]  │  [APR]  │          │ │ re-engage    │ │
                   │          │    ┌────┘    └──┐ │          │ │ support      │ │
                   │          │    │            │ │          │ └──────────────┘ │
                   │          │    ▼            │ │          │                  │
                   │          │ RETRY LOOP      │ │          └──────────────────┘
                   │          │ (max 2)         │ │
                   │          │    │            │ │
                   │          │    └───► FALHA?  │ │
                   │          │         FALLBACK │ │
                   │          │                  │ │
                   │          └──────────────────┘ │
                   │                               │
                   ▼                               ▼
            ┌──────────────────────────────────────────────┐
            │           STATE PERSISTENCE LAYER             │
            │                                              │
            │  state/<conversation_id>/                    │
            │  ├── profile.json         (perfil cliente)   │
            │  ├── state.json           (estado atual)     │
            │  ├── catalog_results.json (busca produtos)   │
            │  ├── generation.json      (resposta candidata)│
            │  ├── evaluation.json      (resultado avaliacao)│
            │  ├── order.json           (dados do pedido)  │
            │  ├── fulfillment.json     (tracking/entrega) │
            │  └── retention.json       (follow-ups)       │
            └──────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────┐
│  LEGENDA:                                                                 │
│  ──► Fluxo normal de dados                                              │
│  ◄── Feedback loop (Evaluator → Generator)                              │
│  ....► Transição de estágio (via guard condition)                       │
└──────────────────────────────────────────────────────────────────────────┘
```

### Tabela de Agentes e Responsabilidades

| Agente | Estágio | Input | Output | Responsabilidade |
|--------|---------|-------|--------|------------------|
| **Discovery** | AWARENESS | Mensagem do cliente, histórico | `profile.json`, intenção classificada | Classificar intenção, extrair entidades, coletar contexto |
| **Catalog** | CONSIDERATION | `profile.json`, intenção | `catalog_results.json` | Filtrar catálogo por restrições, ranquear por relevância |
| **Generator** | CONSIDERATION | `catalog_results.json`, `profile.json` | `generation.json` | Produzir resposta natural em PT-BR, tom WhatsApp |
| **Evaluator** | CONSIDERATION | `generation.json`, `profile.json`, rubricas | `evaluation.json` | Validar restrições, orçamento, qualidade da resposta |
| **Order** | DECISION | `profile.json`, produto escolhido | `order.json` | Processar checkout, pagamento, confirmar pedido |
| **Fulfillment** | DECISION | `order.json` | `fulfillment.json` | Gerar tracking, confirmar entrega |
| **Retention** | RETENTION | `order.json`, `profile.json` | `retention.json` | Agendar follow-up, gerenciar re-engajamento |

---

## 🔀 Estratégias de Coordenação: Tabela Comparativa

Antes de implementar, entenda as diferentes formas de coordenar agentes e por que este exercício usa file-based coordination:

| Estratégia | Como Funciona | Latência | Confiabilidade | Auditabilidade | Complexidade | Quando Usar |
|------------|---------------|----------|----------------|----------------|--------------|-------------|
| **Sequencial Síncrono** | Agentes executam em fila, um após o outro | Alta (soma de latências) | Média (ponto único de falha) | Alta (ordem determinística) | Baixa | Pipelines lineares com dependências fortes |
| **Paralelo (Fan-Out)** | Múltiplos agentes executam simultaneamente | Baixa (latência do mais lento) | Média (resultados parciais) | Baixa (difícil reproduzir ordem) | Média | Etapas independentes (ex: buscar em 3 catálogos ao mesmo tempo) |
| **Event-Driven (Pub/Sub)** | Agentes escutam eventos e reagem | Muito Baixa | Alta (desacoplado, retry automático) | Muito Baixa (difícil rastrear) | Alta | Sistemas assíncronos com muitas fontes de eventos |
| **File-Based Coordination** | Agentes leem/escrevem em arquivos compartilhados | Média (I/O de disco) | Alta (cada arquivo é checkpoint) | Muito Alta (audit trail em arquivos) | Média | Pipelines que precisam de debug, auditoria e retomada |
| **Message Queue (Fila)** | Agentes publicam/consomem mensagens em fila | Baixa | Muito Alta (persistência, DLQ) | Média (logs de fila, não de negócio) | Alta | Produção em escala, múltiplos workers |
| **Orquestrador Central** | Um agente mestre coordena os demais | Média | Média (orquestrador é single point) | Alta (orquestrador loga tudo) | Média | Fluxos com decisiones condicionais complexas |
| **Choreography (Dança)** | Cada agente sabe qual é o próximo e chama diretamente | Baixa | Baixa (se um falha, corrente quebra) | Baixa (rastreamento difícil) | Muito Alta | Raramente — quase sempre inferior a orquestração |

**Neste exercício, usamos File-Based Coordination com Orquestrador Central.** O Orquestrador (`run_customer_journey_turn`) gerencia o fluxo entre estágios e agentes, enquanto cada agente lê e escreve arquivos JSON no diretório de estado. Essa combinação oferece:

- **Audit trail completo:** cada decisão é um arquivo versionável
- **Retomada após falha:** se o sistema cair, o estado está no disco
- **Debugabilidade:** abra o diretório `state/<id>/` e veja exatamente o que aconteceu
- **Simplicidade:** sem dependência de filas, bancos ou serviços externos — ideal para aprendizado e protótipos

Em produção, o KODA evoluiu para message queues (RabbitMQ) com PostgreSQL para state persistence. Mas o contrato entre agentes — os schemas JSON — permaneceu idêntico ao que você vai implementar aqui.

---

## 📝 O Exercício

O exercício está dividido em 5 partes. Complete-as em ordem — cada parte constrói sobre a anterior.

### Parte 1: Modelos de Dados e Funções Auxiliares (20-30 min)

Implemente os data models e funções auxiliares que todo o sistema vai usar.

#### 1.1 Data Models

```python
import json
import tempfile
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional
from enum import Enum


class JourneyStage(str, Enum):
    """Estágios da jornada do cliente no KODA."""
    ENTRY = "ENTRY"
    AWARENESS = "AWARENESS"
    CONSIDERATION = "CONSIDERATION"
    DECISION = "DECISION"
    RETENTION = "RETENTION"


class Intent(str, Enum):
    """Classificações de intenção do cliente."""
    PRODUCT_DISCOVERY = "PRODUCT_DISCOVERY"
    ORDER_STATUS = "ORDER_STATUS"
    SUPPORT = "SUPPORT"
    RICOMPRA = "RICOMPRA"
    RECLAMACAO = "RECLAMACAO"
    UNKNOWN = "UNKNOWN"


class EvalStatus(str, Enum):
    """Status de avaliação do Evaluator."""
    APPROVED = "approved"
    REJECTED = "rejected"


@dataclass
class Product:
    """Produto no catálogo simulado do KODA."""
    sku: str
    name: str
    category: str
    price_brl: float
    servings: int
    lactose_free: bool
    gluten_free: bool
    vegan: bool
    in_stock: bool
    rating: float
    description: str = ""


@dataclass
class CustomerProfile:
    """Perfil do cliente com preferências e restrições."""
    customer_id: str
    name: str
    whatsapp_number: str
    budget_brl: Optional[float] = None
    dietary_restrictions: list[str] = field(default_factory=list)
    allergies: list[str] = field(default_factory=list)
    training_goal: Optional[str] = None
    training_frequency: Optional[str] = None
    preferred_flavor: Optional[str] = None
    preferred_format: Optional[str] = None
    purchase_history: list[dict[str, Any]] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class JourneyState:
    """Estado atual da jornada do cliente."""
    schema_version: str = "2.0"
    conversation_id: str = ""
    customer_id: str = ""
    current_stage: JourneyStage = JourneyStage.ENTRY
    current_sub_state: str = ""
    stage_history: list[dict[str, Any]] = field(default_factory=list)
    context: dict[str, Any] = field(default_factory=dict)
    metrics: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class Generation:
    """Resposta candidata do Generator."""
    schema_version: str = "2.0"
    conversation_id: str = ""
    candidate_response: str = ""
    products_mentioned: list[str] = field(default_factory=list)
    tone: str = "whatsapp_natural"
    generated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class RubricResult:
    """Resultado individual de um critério da rubrica."""
    criterion: str
    passed: bool
    evidence: str


@dataclass
class Evaluation:
    """Resultado da avaliação do Evaluator."""
    schema_version: str = "2.0"
    conversation_id: str = ""
    status: str = ""
    rubric_results: list[RubricResult] = field(default_factory=list)
    feedback: str = ""
    checked_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class Order:
    """Dados do pedido processado pelo Order Agent."""
    schema_version: str = "2.0"
    conversation_id: str = ""
    order_id: str = ""
    items: list[dict[str, Any]] = field(default_factory=list)
    total_brl: float = 0.0
    discount_applied: float = 0.0
    shipping_address: dict[str, str] = field(default_factory=dict)
    payment_method: str = ""
    payment_status: str = "pending"
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class Fulfillment:
    """Dados de fulfillment do pedido."""
    schema_version: str = "2.0"
    conversation_id: str = ""
    order_id: str = ""
    tracking_code: str = ""
    carrier: str = ""
    estimated_delivery: str = ""
    status: str = "processing"
    delivered_at: Optional[str] = None
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class Retention:
    """Dados de retenção e follow-up."""
    schema_version: str = "2.0"
    conversation_id: str = ""
    customer_id: str = ""
    follow_up_scheduled_at: str = ""
    follow_up_type: str = ""
    re_engagement_offers: list[dict[str, Any]] = field(default_factory=list)
    last_contact_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class ConversationTurn:
    """Um turno de conversa (mensagem do cliente + resposta do sistema)."""
    conversation_id: str
    turn_id: str
    customer_message: str
    received_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
```

#### 1.2 Funções Auxiliares de Persistência

Implemente estas funções no seu código:

```python
def write_json(data: Any, filepath: Path) -> None:
    """Escreve dados em JSON com escrita atômica (via tempfile).

    Args:
        data: Objeto Python serializável (dataclass, dict, list)
        filepath: Caminho de destino do arquivo JSON

    Must Do:
        - Usar tempfile.NamedTemporaryFile para escrita atômica
        - Garantir que o diretório pai existe (criar se necessário)
        - Escrever com indent=2, ensure_ascii=False
        - Tratar dataclasses convertendo para dict via dataclasses.asdict()
    """
    # TODO: Implementar


def read_json(filepath: Path) -> dict[str, Any]:
    """Lê e retorna dados de um arquivo JSON.

    Args:
        filepath: Caminho do arquivo JSON

    Returns:
        Dicionário com os dados do arquivo

    Raises:
        FileNotFoundError: Se o arquivo não existe
        json.JSONDecodeError: Se o JSON é inválido
    """
    # TODO: Implementar


def ensure_state_dir(conversation_id: str, base_dir: str = "state") -> Path:
    """Garante que o diretório de estado da conversa existe.

    Args:
        conversation_id: ID único da conversa
        base_dir: Diretório base para estado

    Returns:
        Path do diretório criado
    """
    # TODO: Implementar


def update_journey_state(
    state: JourneyState,
    new_stage: JourneyStage,
    trigger: str,
    guard_evaluation: str = "ALL_PASS",
    conversation_id: str = "",
) -> JourneyState:
    """Atualiza o estado da jornada, registrando a transição no histórico.

    Args:
        state: Estado atual da jornada
        new_stage: Novo estágio para transição
        trigger: O que disparou a transição
        guard_evaluation: Resultado da avaliação das guards
        conversation_id: ID da conversa (se não definido no state)

    Returns:
        JourneyState atualizado com nova etapa e histórico
    """
    # TODO: Implementar
```

### Parte 2: Implementação dos Agentes (40-60 min)

Implemente cada agente como uma função pura que recebe dados e retorna um dataclass.

#### 2.1 Discovery Agent — `discovery_agent`

O Discovery Agent é o primeiro ponto de contato. Ele classifica a intenção da mensagem do cliente e extrai informações do perfil.

```python
def discovery_agent(
    customer_message: str,
    existing_profile: Optional[CustomerProfile] = None,
    conversation_id: str = "",
) -> tuple[Intent, CustomerProfile]:
    """Classifica intenção e coleta/atualiza perfil do cliente.

    Estratégia de classificação (determinística, sem LLM):
    - Palavras-chave para detectar intenção
    - Regex para extrair valores monetários (orçamento)
    - Lista de restrições conhecidas para detectar alergias/dietas

    Args:
        customer_message: Mensagem recebida do cliente no WhatsApp
        existing_profile: Perfil existente (None se primeira interação)
        conversation_id: ID único da conversa

    Returns:
        Tuple com (Intent classificada, CustomerProfile atualizado)

    Regras de classificação:
        "quero comprar", "preciso de", "recomenda" → PRODUCT_DISCOVERY
        "onde está meu pedido", "tracking", "entrega" → ORDER_STATUS
        "problema", "errado", "defeito", "reclamar" → RECLAMACAO
        "comprar de novo", "mesmo de antes", "recorrente" → RICOMPRA
        "dúvida", "como usar", "ajuda" → SUPPORT
        Nenhum match → UNKNOWN

    Extração de entidades:
        "R$ X" ou "X reais" → budget_brl
        "intolerante a lactose", "sem lactose" → dietary_restrictions.append("lactose_free")
        "vegetariano", "vegano" → dietary_restrictions.append(...)
        "alérgico a X" → allergies.append(X)
        "treino X vezes", "treino Xx por semana" → training_frequency
    """
    # TODO: Implementar
```

#### 2.2 Catalog Agent — `catalog_agent`

```python
def catalog_agent(
    intent: Intent,
    profile: CustomerProfile,
    catalog: list[Product],
    max_results: int = 5,
) -> list[Product]:
    """Filtra e ranqueia produtos do catálogo baseado no perfil e intenção.

    Regras de filtro (aplicadas em ordem):
    1. Se intent é PRODUCT_DISCOVERY: filtra por categoria inferida da mensagem
       - "whey", "proteína" → category == "whey_protein"
       - "creatina" → category == "creatina"
       - "pré-treino", "pré treino" → category == "pre_workout"
       - "dormir", "sono" → category == "sono"
       - "recuperação", "pós-treino" → category == "post_workout"
       - Sem categoria clara → todos os produtos
    2. Se "lactose_free" em dietary_restrictions: lactose_free == True
    3. Se "gluten_free" em dietary_restrictions: gluten_free == True
    4. Se "vegano" em dietary_restrictions: vegan == True
    5. Se budget_brl definido: price_brl <= budget_brl
    6. Apenas produtos com in_stock == True
    7. Ordena por rating decrescente
    8. Limita a max_results

    Args:
        intent: Intenção classificada
        profile: Perfil do cliente com restrições
        catalog: Lista completa de produtos
        max_results: Número máximo de resultados

    Returns:
        Lista de produtos filtrados e ranqueados
    """
    # TODO: Implementar
```

#### 2.3 Generator Agent — `generator_agent`

```python
def generator_agent(
    profile: CustomerProfile,
    products: list[Product],
    conversation_id: str = "",
) -> Generation:
    """Gera resposta natural em PT-BR para WhatsApp.

    A resposta deve seguir o tom KODA:
    - Saudação personalizada com nome do cliente
    - Apresentação dos produtos com emojis relevantes
    - Informação de preço e características principais
    - Pergunta de engajamento no final

    Template de resposta:
    ```
    Oi {nome}! Encontrei {N} opções que se encaixam no que você procura:

    {para cada produto:}
    🏷️ {nome_produto}
    ✅ {caracteristica_1}
    ✅ {caracteristica_2}
    ✅ {caracteristica_3}
    💰 {preco}
    ⭐ {rating}/5

    {pergunta_engajamento}
    ```

    Args:
        profile: Perfil do cliente
        products: Lista de produtos candidatos (já filtrados)
        conversation_id: ID único da conversa

    Returns:
        Generation com resposta candidata
    """
    # TODO: Implementar
```

#### 2.4 Evaluator Agent — `evaluator_agent`

```python
def evaluator_agent(
    generation: Generation,
    profile: CustomerProfile,
    products: list[Product],
    conversation_id: str = "",
) -> Evaluation:
    """Avalia resposta candidata contra rubricas de negócio.

    Rubricas obrigatórias (todas devem passar):

    1. RESTRICAO_ORCAMENTO:
       - Se profile.budget_brl está definido:
         NENHUM produto em generation.products_mentioned tem price_brl > profile.budget_brl

    2. RESTRICAO_LACTOSE:
       - Se "lactose_free" em profile.dietary_restrictions:
         TODO produto mencionado tem lactose_free == True

    3. RESTRICAO_GLUTEN:
       - Se "gluten_free" em profile.dietary_restrictions:
         TODO produto mencionado tem gluten_free == True

    4. RESTRICAO_VEGANO:
       - Se "vegano" em profile.dietary_restrictions:
         TODO produto mencionado tem vegan == True

    5. RESPOSTA_NAO_VAZIA:
       - len(generation.candidate_response) > 10

    6. TOM_WHATSAPP:
       - len(generation.candidate_response) <= 800 (WhatsApp é mensagem curta)

    7. PRODUTOS_EM_ESTOQUE:
       - TODO produto em generation.products_mentioned tem in_stock == True

    8. PERSONALIZACAO:
       - profile.name está presente em generation.candidate_response
         (a resposta menciona o nome do cliente)

    Args:
        generation: Resposta candidata do Generator
        profile: Perfil do cliente (para verificar restrições)
        products: Produtos mencionados na resposta
        conversation_id: ID único da conversa

    Returns:
        Evaluation com status (approved/rejected) e detalhes de cada rubrica
    """
    # TODO: Implementar
```

#### 2.5 Order Agent — `order_agent`

```python
def order_agent(
    profile: CustomerProfile,
    selected_product_sku: str,
    shipping_address: dict[str, str],
    payment_method: str,
    catalog: list[Product],
    conversation_id: str = "",
) -> Order:
    """Processa o pedido: valida SKU, calcula total, aplica desconto, simula pagamento.

    Regras de negócio:
    - Se produto não existe no catálogo: retorna Order com payment_status = "rejected"
    - Se produto fora de estoque: retorna Order com payment_status = "rejected"
    - Desconto de 5% para pagamento via PIX
    - Desconto de 10% para cliente com 2+ compras no histórico
    - Descontos NÃO são cumulativos (aplica o maior)
    - Formato de endereço: {"street": str, "number": str, "city": str, "state": str, "zip": str}
    - Valida se ZIP tem 8 dígitos (formato XXXXXXXX)
    - Se ZIP inválido: retorna Order com payment_status = "rejected"

    Args:
        profile: Perfil do cliente
        selected_product_sku: SKU do produto escolhido
        shipping_address: Dicionário com endereço de entrega
        payment_method: "pix" ou "credit_card"
        catalog: Catálogo completo de produtos
        conversation_id: ID único da conversa

    Returns:
        Order com status do pagamento e dados do pedido
    """
    # TODO: Implementar
```

#### 2.6 Fulfillment Agent — `fulfillment_agent`

```python
def fulfillment_agent(
    order: Order,
    conversation_id: str = "",
) -> Fulfillment:
    """Gera dados de fulfillment após pedido confirmado.

    Simula a criação de tracking e estimativa de entrega:
    - Gera tracking_code como "KDA-" + 6 dígitos aleatórios
    - Define carrier baseado no state do endereço
      (SP → "Loggi", RJ/MG → "Total Express", demais → "Correios")
    - estimated_delivery = hoje + prazo do carrier
      (Loggi: +1 dia, Total Express: +3 dias, Correios: +7 dias)
    - Status inicial: "processing"

    Só processa se order.payment_status == "confirmed"

    Args:
        order: Pedido confirmado
        conversation_id: ID único da conversa

    Returns:
        Fulfillment com tracking e estimativa
    """
    # TODO: Implementar
```

#### 2.7 Retention Agent — `retention_agent`

```python
def retention_agent(
    profile: CustomerProfile,
    order: Order,
    conversation_id: str = "",
) -> Retention:
    """Agenda follow-up e prepara ofertas de re-engajamento.

    Lógica de follow-up:
    - Calcula data de follow-up baseada no número de servings do produto
      (assumir 1 serving/dia → follow-up quando ~80% das servings consumidas)
    - Tipo de follow-up: "ESTOQUE_ACABANDO"

    Ofertas de re-engajamento:
    - Se cliente tem 0 compras anteriores: desconto de 10% na próxima
    - Se cliente tem 1+ compras: desconto de 15% + frete grátis
    - Se ticket médio > R$ 200: oferta de combo (sugere produto complementar)

    Args:
        profile: Perfil do cliente com histórico
        order: Pedido concluído
        conversation_id: ID único da conversa

    Returns:
        Retention com follow-up agendado e ofertas
    """
    # TODO: Implementar
```

### Parte 3: Máquina de Estados e Guard Conditions (20-30 min)

Implemente a lógica de transição entre estágios da jornada.

```python
def evaluate_guard_conditions(
    state: JourneyState,
    profile: CustomerProfile,
) -> list[dict[str, Any]]:
    """Avalia quais transições são possíveis a partir do estado atual.

    Para cada transição possível, verifica as guard conditions.
    Retorna lista de transições com status (ALL_PASS / FAIL).

    Transições e suas guards:

    ENTRY → AWARENESS:
        - Sempre permitido (primeira mensagem)

    AWARENESS → CONSIDERATION:
        - profile.name não está vazio (sabemos quem é)
        - state.context["intent_classified"] == True
        - state.context["minimal_context_collected"] == True

    AWARENESS → AWARENESS (loop):
        - Sempre permitido (continua coletando contexto)

    CONSIDERATION → DECISION:
        - state.context["product_selected"] == True
        - state.context["product_validated"] == True
        - profile.budget_brl não é None OU produto cabe no orçamento

    CONSIDERATION → CONSIDERATION (loop):
        - Sempre permitido

    DECISION → RETENTION:
        - state.context["payment_confirmed"] == True
        - state.context["order_created"] == True

    DECISION → CONSIDERATION (volta):
        - state.context["customer_cancelled"] == True

    RETENTION → CONSIDERATION (re-engajamento):
        - state.context["customer_wants_rebuy"] == True

    Args:
        state: Estado atual da jornada
        profile: Perfil do cliente

    Returns:
        Lista de transições possíveis com avaliações
    """
    # TODO: Implementar


def select_transition(
    possible_transitions: list[dict[str, Any]],
    customer_message: str = "",
) -> dict[str, Any]:
    """Seleciona a melhor transição dentre as possíveis.

    Prioridade:
    1. Handoff humano (se cliente pede explicitamente)
    2. Timeout (se inativo > 30 min) — verificar state.updated_at
    3. Transição de avanço (AWARENESS→CONSIDERATION, etc.)
    4. Loop (permanece no estado atual)

    Args:
        possible_transitions: Lista de transições avaliadas
        customer_message: Mensagem atual do cliente

    Returns:
        A transição selecionada (a de maior prioridade)
    """
    # TODO: Implementar
```

### Parte 4: Orquestrador Principal (30-40 min)

Implemente o orquestrador que conecta todos os agentes.

```python
def run_customer_journey_turn(
    customer_message: str,
    conversation_id: str,
    catalog: list[Product],
    base_state_dir: str = "state",
) -> dict[str, Any]:
    """Orquestra um turno completo da jornada do cliente.

    Pipeline:
    1. Carrega state.json do disco (ou cria novo se primeira mensagem)
    2. Carrega profile.json do disco (ou cria novo)
    3. Executa discovery_agent() para classificar intenção
    4. Salva profile.json atualizado
    5. Avalia guard conditions com evaluate_guard_conditions()
    6. Seleciona transição com select_transition()
    7. Executa pipeline do estágio:
       - Se AWARENESS: resposta de coleta de contexto
       - Se CONSIDERATION: catalog → generator → evaluator → retry loop
       - Se DECISION: order → fulfillment
       - Se RETENTION: retention
    8. Se aprovado: persiste novo estado e retorna resposta
    9. Se rejeitado após retries: fallback seguro

    Retry loop (CONSIDERATION):
    - Tentativa 1: generator_agent() → evaluator_agent()
    - Se REJECTED: generator_agent() com feedback → evaluator_agent()
    - Se REJECTED novamente: fallback
    - Máximo 2 retries (3 tentativas no total)

    Fallback seguro:
    "Preciso confirmar um detalhe antes de continuar. Só um momento! 😊"

    Args:
        customer_message: Mensagem recebida do cliente
        conversation_id: ID único da conversa
        catalog: Catálogo completo de produtos
        base_state_dir: Diretório base para arquivos de estado

    Returns:
        Dicionário com:
        - "response": str (resposta para enviar ao cliente)
        - "state": JourneyState (estado atualizado)
        - "evaluation": Optional[Evaluation] (se passou pelo Evaluator)
        - "order": Optional[Order] (se passou pelo Order Agent)
        - "stage": JourneyStage (estágio atual)
    """
    # TODO: Implementar
```

### Parte 5: Catálogo de Produtos e Cenários de Teste (20-30 min)

#### 5.1 Catálogo de Produtos

Implemente um catálogo com pelo menos 15 produtos simulados da FutanBear:

```python
FUTANBEAR_CATALOG: list[Product] = [
    # Whey Proteins
    Product(
        sku="WHEY-CONC-900",
        name="Whey Protein Concentrado 900g",
        category="whey_protein",
        price_brl=99.90,
        servings=30,
        lactose_free=False,
        gluten_free=True,
        vegan=False,
        in_stock=True,
        rating=4.5,
        description="Proteína de alta qualidade para ganho de massa muscular. 24g de proteína por dose.",
    ),
    Product(
        sku="WHEY-ISO-900",
        name="Whey Protein Isolado 900g",
        category="whey_protein",
        price_brl=159.90,
        servings=30,
        lactose_free=True,
        gluten_free=True,
        vegan=False,
        in_stock=True,
        rating=4.8,
        description="Whey isolado com baixíssimo teor de lactose. 27g de proteína pura por dose.",
    ),
    Product(
        sku="WHEY-VEG-800",
        name="Proteína Vegetal Blend 800g",
        category="whey_protein",
        price_brl=129.90,
        servings=25,
        lactose_free=True,
        gluten_free=True,
        vegan=True,
        in_stock=True,
        rating=4.3,
        description="Blend de ervilha, arroz e quinoa. 22g de proteína vegetal por dose.",
    ),
    # Creatinas
    Product(
        sku="CREA-MONO-300",
        name="Creatina Monohidratada 300g",
        category="creatina",
        price_brl=69.90,
        servings=60,
        lactose_free=True,
        gluten_free=True,
        vegan=True,
        in_stock=True,
        rating=4.9,
        description="Creatina pura monohidratada. A mais estudada e comprovada do mercado.",
    ),
    Product(
        sku="CREA-MICRO-250",
        name="Creatina Micronizada 250g",
        category="creatina",
        price_brl=74.90,
        servings=50,
        lactose_free=True,
        gluten_free=True,
        vegan=True,
        in_stock=True,
        rating=4.7,
        description="Partículas menores para melhor absorção. Ideal para quem tem sensibilidade gástrica.",
    ),
    # Pré-Treinos
    Product(
        sku="PRE-BASIC-300",
        name="Pré-Treino Básico 300g",
        category="pre_workout",
        price_brl=89.90,
        servings=30,
        lactose_free=True,
        gluten_free=True,
        vegan=False,
        in_stock=True,
        rating=4.4,
        description="Energia e foco para seu treino. Com cafeína, beta-alanina e arginina.",
    ),
    Product(
        sku="PRE-VEG-270",
        name="Pré-Treino Vegano 270g",
        category="pre_workout",
        price_brl=109.90,
        servings=30,
        lactose_free=True,
        gluten_free=True,
        vegan=True,
        in_stock=True,
        rating=4.6,
        description="Energia 100% vegetal. Cafeína de guaraná, beta-alanina vegana.",
    ),
    # Sono e Relaxamento
    Product(
        sku="SONO-MEL-120",
        name="Melatonina 120 Cápsulas",
        category="sono",
        price_brl=49.90,
        servings=120,
        lactose_free=True,
        gluten_free=True,
        vegan=False,
        in_stock=True,
        rating=4.5,
        description="Ajuda a regular o ciclo do sono. 3mg por cápsula.",
    ),
    Product(
        sku="SONO-MAG-90",
        name="Magnésio Quelato 90 Cápsulas",
        category="sono",
        price_brl=59.90,
        servings=90,
        lactose_free=True,
        gluten_free=True,
        vegan=True,
        in_stock=True,
        rating=4.7,
        description="Relaxa o sistema nervoso e melhora a qualidade do sono. 400mg por cápsula.",
    ),
    Product(
        sku="SONO-HERB-90",
        name="Blend Herbal Noturno 90 Cápsulas",
        category="sono",
        price_brl=72.00,
        servings=90,
        lactose_free=True,
        gluten_free=True,
        vegan=True,
        in_stock=True,
        rating=4.4,
        description="Camomila, valeriana e passiflora. 100% natural, sem hormônios.",
    ),
    # Recuperação Pós-Treino
    Product(
        sku="REC-BCAA-400",
        name="BCAA 400g",
        category="post_workout",
        price_brl=79.90,
        servings=40,
        lactose_free=True,
        gluten_free=True,
        vegan=False,
        in_stock=True,
        rating=4.3,
        description="Aminoácidos de cadeia ramificada para recuperação muscular.",
    ),
    Product(
        sku="REC-GLUT-300",
        name="L-Glutamina 300g",
        category="post_workout",
        price_brl=69.90,
        servings=60,
        lactose_free=True,
        gluten_free=True,
        vegan=False,
        in_stock=True,
        rating=4.5,
        description="Acelera a recuperação muscular e fortalece o sistema imunológico.",
    ),
    Product(
        sku="REC-ZMA-120",
        name="ZMA 120 Cápsulas",
        category="post_workout",
        price_brl=89.90,
        servings=120,
        lactose_free=True,
        gluten_free=True,
        vegan=True,
        in_stock=True,
        rating=4.6,
        description="Zinco, Magnésio e Vitamina B6. Melhora recuperação e qualidade do sono.",
    ),
    # Fora de estoque (para testar filtro)
    Product(
        sku="WHEY-HYDRO-800",
        name="Whey Protein Hidrolisado 800g",
        category="whey_protein",
        price_brl=199.90,
        servings=25,
        lactose_free=True,
        gluten_free=True,
        vegan=False,
        in_stock=False,
        rating=4.9,
        description="Absorção ultra-rápida. Ideal para pós-treino imediato.",
    ),
    # Produto caro (para testar orçamento)
    Product(
        sku="PRE-ELITE-500",
        name="Pré-Treino Elite 500g",
        category="pre_workout",
        price_brl=249.90,
        servings=50,
        lactose_free=True,
        gluten_free=True,
        vegan=False,
        in_stock=True,
        rating=4.8,
        description="Fórmula premium com 12 ativos. Performance máxima garantida.",
    ),
]
```

#### 5.2 Cenários de Teste

Implemente os seguintes cenários como funções de teste:

```python
def test_scenario_1_happy_path() -> bool:
    """
    Cenário 1: Jornada Completa (Caminho Feliz)

    Cliente: "Oi, quero comprar whey protein. Meu orçamento é R$ 180."
    → Discovery classifica: PRODUCT_DISCOVERY, extrai budget_brl=180.00
    → Catalog filtra: whey_protein, price <= 180, in_stock
    → Generator produz resposta com produtos
    → Evaluator aprova (todos os critérios passam)

    Verificações:
    - Intent == PRODUCT_DISCOVERY
    - profile.budget_brl == 180.0
    - Nenhum produto retornado tem price_brl > 180
    - Todos os produtos retornados têm category == "whey_protein"
    - Todos os produtos retornados têm in_stock == True
    - generation.candidate_response não está vazia
    - evaluation.status == "approved"
    """
    # TODO: Implementar


def test_scenario_2_lactose_restriction() -> bool:
    """
    Cenário 2: Restrição de Lactose

    Cliente: "Preciso de whey, mas sou intolerante a lactose. Até R$ 200."
    → Discovery detecta restrição: lactose_free
    → Catalog filtra: whey_protein, lactose_free=True, price <= 200
    → Evaluator verifica que NENHUM produto recomendado tem lactose

    Verificações:
    - "lactose_free" in profile.dietary_restrictions
    - Nenhum produto retornado tem lactose_free == False
    - evaluation.rubric_results para RESTRICAO_LACTOSE: passed == True
    """
    # TODO: Implementar


def test_scenario_3_budget_violation() -> bool:
    """
    Cenário 3: Violação de Orçamento Detectada

    Cliente: "Quero o melhor pré-treino que tiver. Orçamento R$ 50."
    → Catalog filtra: pre_workout, price <= 50
    → Se nenhum produto no orçamento: lista vazia
    → Generator produz resposta informando que não há opções no orçamento
    → Evaluator verifica que nenhum produto acima de R$ 50 foi recomendado

    Verificações:
    - products_retornados é lista vazia OU todos têm price <= 50
    - Se lista vazia: generation.candidate_response informa a situação
    - evaluation.status é "approved" (resposta honesta é aprovada)
    """
    # TODO: Implementar


def test_scenario_4_vegan_customer() -> bool:
    """
    Cenário 4: Cliente Vegano

    Cliente: "Sou vegano. Tem proteína pra mim?"
    → Discovery detecta: dietary_restrictions = ["vegano"]
    → Catalog filtra: vegan=True
    → Generator usa tom adequado (foco em produtos vegetais)
    → Evaluator verifica que todos os produtos são veganos

    Verificações:
    - "vegano" in profile.dietary_restrictions
    - Nenhum produto retornado tem vegan == False
    - generation.candidate_response contém "vegano" ou "vegetal"
    """
    # TODO: Implementar


def test_scenario_5_evaluator_rejection_and_retry() -> bool:
    """
    Cenário 5: Rejeição + Retry + Fallback

    Simula uma situação onde o Generator produz resposta que viola restrição.
    → 1a tentativa: resposta inclui produto com lactose para cliente intolerante
    → Evaluator: REJECTED (RESTRICAO_LACTOSE falhou)
    → Generator recebe feedback e tenta novamente
    → 2a tentativa: resposta ainda inclui produto com lactose
    → Evaluator: REJECTED
    → Sistema retorna fallback seguro

    Verificações:
    - evaluation_1.status == "rejected"
    - evaluation_2.status == "rejected"
    - Resposta final é o fallback seguro
    - Fallback não contém recomendação de produto
    """
    # TODO: Implementar


def test_scenario_6_full_order_pipeline() -> bool:
    """
    Cenário 6: Pipeline de Pedido Completo

    Simula jornada completa:
    1. Discovery: classifica PRODUCT_DISCOVERY, extrai perfil
    2. Catalog: filtra produtos
    3. Generator: produz recomendação
    4. Evaluator: aprova
    5. Simula cliente escolhendo produto (SKU = "WHEY-ISO-900")
    6. Order: processa pedido com PIX e endereço válido
    7. Fulfillment: gera tracking
    8. Retention: agenda follow-up

    Verificações:
    - order.payment_status == "confirmed"
    - order.total_brl > 0 (com desconto PIX: 5%)
    - fulfillment.tracking_code começa com "KDA-"
    - retention.follow_up_scheduled_at é uma data futura
    - Arquivos JSON foram criados em state/<conversation_id>/
    """
    # TODO: Implementar


def test_scenario_7_order_with_invalid_zip() -> bool:
    """
    Cenário 7: Pedido com CEP Inválido

    Cliente fornece CEP com formato inválido ("123").
    → Order Agent detecta ZIP inválido
    → payment_status = "rejected"
    → Sistema retorna mensagem pedindo CEP correto

    Verificações:
    - order.payment_status == "rejected"
    - Resposta contém instrução sobre CEP
    """
    # TODO: Implementar


def test_scenario_8_out_of_stock_product() -> bool:
    """
    Cenário 8: Produto Fora de Estoque

    Cliente tenta comprar WHEY-HYDRO-800 (in_stock=False).
    → Order Agent detecta fora de estoque
    → payment_status = "rejected"
    → Sistema sugere produto alternativo

    Verificações:
    - order.payment_status == "rejected"
    - Resposta contém sugestão alternativa
    """
    # TODO: Implementar
```

---

## 🧪 Cenários de Teste: Visão Geral

| # | Cenário | O Que Testa | Resultado Esperado |
|---|---------|-------------|-------------------|
| 1 | Caminho Feliz | Pipeline completo sem restrições | Aprovado, 3-5 produtos recomendados |
| 2 | Restrição Lactose | Filtro de alergia alimentar | Nenhum produto com lactose |
| 3 | Orçamento Impossível | Filtro de preço com budget baixo | Resposta honesta, sem recomendar acima |
| 4 | Cliente Vegano | Filtro de preferência alimentar | Apenas produtos veganos |
| 5 | Rejeição + Retry | Loop Generator/Evaluator | Fallback seguro após 2 rejeições |
| 6 | Pipeline Pedido | Order + Fulfillment + Retention | Pedido criado, tracking gerado, follow-up agendado |
| 7 | CEP Inválido | Validação de entrada | Pedido rejeitado, mensagem de correção |
| 8 | Fora de Estoque | Verificação de disponibilidade | Pedido rejeitado, alternativa sugerida |

---

## 📊 Rubricas de Avaliação

Seu exercício será avaliado nos seguintes critérios:

### Rubricas Funcionais (60%)

| # | Critério | Peso | Como Verificar |
|---|----------|------|----------------|
| R1 | Discovery classifica corretamente as 6 intenções | 10% | Rodar 6 mensagens de teste com intenções diferentes |
| R2 | Catalog aplica todos os filtros (categoria, restrições, preço, estoque) | 10% | Verificar resultados para perfil com múltiplas restrições |
| R3 | Generator produz resposta em PT-BR com nome do cliente e emojis | 10% | Inspecionar `candidate_response` |
| R4 | Evaluator aplica todas as 8 rubricas e retorna evidência | 15% | Verificar `rubric_results` para cada cenário |
| R5 | Retry loop funciona: rejeita → feedback → retry → aprova ou fallback | 5% | Cenário 5 |
| R6 | Pipeline de pedido cobre checkout, pagamento e fulfillment | 5% | Cenário 6 |
| R7 | Retention agenda follow-up com data calculada | 5% | Cenário 6 |

### Rubricas Técnicas (25%)

| # | Critério | Peso | Como Verificar |
|---|----------|------|----------------|
| T1 | Todos os data classes têm type hints | 5% | Inspeção visual do código |
| T2 | `write_json` usa escrita atômica com `tempfile` | 5% | Inspeção da implementação |
| T3 | Arquivos JSON incluem `schema_version`, `conversation_id`, timestamp | 5% | Verificar arquivos gerados nos testes |
| T4 | Nenhum `except: pass` vazio ou `# type: ignore` | 5% | Busca textual no código |
| T5 | Funções são puras (não dependem de estado global) | 5% | Inspeção visual: sem `global`, sem variáveis de módulo mutáveis |

### Rubricas de Cenários (15%)

| # | Critério | Peso | Como Verificar |
|---|----------|------|----------------|
| C1 | Cenário 1 (caminho feliz) passa | 3% | Executar `test_scenario_1_happy_path()` |
| C2 | Cenário 2 (lactose) passa | 3% | Executar `test_scenario_2_lactose_restriction()` |
| C3 | Cenário 5 (retry/fallback) passa | 3% | Executar `test_scenario_5_evaluator_rejection_and_retry()` |
| C4 | Cenário 6 (pipeline completo) passa | 3% | Executar `test_scenario_6_full_order_pipeline()` |
| C5 | Cenário 7 (CEP inválido) passa | 3% | Executar `test_scenario_7_order_with_invalid_zip()` |

---

## 🏪 Aplicação KODA: Como Este Pipeline Roda em Produção

O pipeline que você implementou é uma versão simplificada — mas arquiteturalmente fiel — do que roda no KODA em produção. Entenda as diferenças e o que permanece igual:

### O Que é Igual

| Elemento | Seu Código | KODA Produção |
|----------|-----------|---------------|
| **Separação de agentes** | 7 funções puras | 7 serviços independentes (cada um em seu container) |
| **Contrato JSON** | Dataclasses com `schema_version` | Exatamente os mesmos schemas, validados com JSON Schema |
| **Guard conditions** | `evaluate_guard_conditions()` | Implementado como middleware no orchestrator |
| **Retry loop** | Máximo 2 retries com fallback | Máximo 3 retries, fallback com escalation para humano |
| **State persistence** | Arquivos JSON em disco | PostgreSQL + Redis cache |
| **Audit trail** | Arquivos `state/<id>/` | Tabelas `conversation_events`, `agent_decisions`, `evaluation_log` |

### O Que Evoluiu

| Elemento | Seu Código | KODA Produção |
|----------|-----------|---------------|
| **Classificação de intenção** | Regex determinística | Claude Sonnet com few-shot prompting + fallback determinístico |
| **Geração de resposta** | Template Python | Claude Opus com system prompt por estágio |
| **Avaliação** | Regras Python determinísticas | Claude Sonnet como Evaluator + regras determinísticas como safety net |
| **Coordenação** | Função síncrona | RabbitMQ com filas por estágio |
| **Catálogo** | Lista hardcoded | API REST com cache Redis, atualização em tempo real |
| **Pagamento** | Simulado | Integração com Stripe/Pix via API |
| **Tracking** | Simulado | Integração com Loggi/Correios API |

### O Que Você Deve Aprender com Essa Comparação

O padrão arquitetural — agentes independentes, contrato JSON, guard conditions, retry loop, audit trail — **é o mesmo** tanto no seu protótipo de 500 linhas quanto no sistema de produção com 8 serviços e 3 integrações externas.

A diferença está na **implementação dos componentes**, não na **arquitetura dos componentes**.

Isso significa que o código que você escreveu hoje é uma **maquete arquitetural** que escala. Quando o KODA precisar crescer, você não vai redesenhar a arquitetura. Vai apenas substituir funções Python por serviços HTTP, funções determinísticas por chamadas a LLMs, e escrita em disco por escrita em banco de dados.

O contrato entre os agentes — os dataclasses e os schemas JSON — permanece o mesmo.

### Exemplo Real: Trace de Produção do KODA

Para tornar isso concreto, veja um trace real (anonimizado) de uma conversa que resultou em venda no KODA produção:

```
[2026-05-27 14:22:01] WA_WEBHOOK: mensagem recebida de +55 21 98888-7777
[2026-05-27 14:22:01] ORCHESTRATOR: conversation_id=sess_8f3a, stage=ENTRY
[2026-05-27 14:22:01] DISCOVERY: intent=PRODUCT_DISCOVERY, budget=150.00
[2026-05-27 14:22:01] GUARD: ENTRY→AWARENESS ALL_PASS
[2026-05-27 14:22:02] GENERATOR: response_sent (tom=welcome, chars=142)

[2026-05-27 14:24:15] WA_WEBHOOK: mensagem recebida
[2026-05-27 14:24:15] DISCOVERY: name="Carlos", restriction=lactose_free
[2026-05-27 14:24:15] GUARD: AWARENESS→CONSIDERATION ALL_PASS
[2026-05-27 14:24:15] CATALOG: 15 produtos → 4 após filtros (lactose_free, budget<=150, in_stock)
[2026-05-27 14:24:16] GENERATOR: response_sent (tom=whatsapp_natural, chars=480, products=4)
[2026-05-27 14:24:16] EVALUATOR: status=APPROVED (8/8 rubrics passed)

[2026-05-27 14:31:40] WA_WEBHOOK: mensagem recebida
[2026-05-27 14:31:40] DISCOVERY: intent=PRODUCT_DISCOVERY (continua explorando)
[2026-05-27 14:31:40] CATALOG: mantendo mesmos 4 produtos
[2026-05-27 14:31:41] GENERATOR: response_sent (foco em COMPARISON, chars=620)
[2026-05-27 14:31:41] EVALUATOR: status=APPROVED

[2026-05-27 14:38:55] WA_WEBHOOK: mensagem recebida
[2026-05-27 14:38:55] DISCOVERY: intent=PRODUCT_DISCOVERY, selected_sku=WHEY-ISO-900
[2026-05-27 14:38:55] GUARD: CONSIDERATION→DECISION ALL_PASS
[2026-05-27 14:38:56] ORDER: checkout iniciado, payment_method=pix, total=151.90→144.30 (5% PIX)
[2026-05-27 14:38:56] FULFILLMENT: tracking=KDA-582104, carrier=Loggi, eta=2026-05-28
[2026-05-27 14:38:56] RETENTION: follow_up agendado para 2026-06-21 (80% de 30 dias)

[2026-05-27 14:42:10] WA_WEBHOOK: pagamento confirmado (webhook externo)
[2026-05-27 14:42:10] ORDER: payment_status=confirmed
[2026-05-27 14:42:11] GENERATOR: response_sent (confirmação de pedido, chars=290)
```

Este trace tem 12 segundos de processamento total para 5 interações. Cada decisão é auditável. Se o cliente ligar amanhã reclamando do preço, o time de suporte abre `state/sess_8f3a/order.json` e vê: `total_brl=144.30, discount=7.60 (PIX 5%)`.

### Por Que Esse Pipeline Reduz Erros em 94%

Dados internos do KODA (maio 2026, 2.847 conversas analisadas):

| Métrica | Agente Único (Versão 1) | Pipeline Multi-Agente (Versão 3) | Melhoria |
|---------|------------------------|----------------------------------|----------|
| Precisão de orçamento | 73% | 99.1% | +26pp |
| Respeito a restrições alimentares | 68% | 99.7% | +32pp |
| Erros em pedidos (SKU errado) | 12% | 0.2% | -94% |
| Conversas com fallback | N/A (não existia) | 3.2% | Previne respostas erradas |
| Clientes que voltam em 60 dias | 18% | 47% | +161% |
| Tempo médio até decisão de compra | 34 min | 22 min | -35% |

A diferença não é um modelo melhor. É arquitetura. Sete agentes especializados, cada um fazendo uma coisa bem, com contratos explícitos e guard conditions que previnem estados inválidos.

### Lições de Produção

Três lições que a equipe KODA aprendeu operando este pipeline em produção:

**Lição 1: O Evaluator é seu funcionário mais importante.** Todo bug que chegou ao cliente passou porque o Evaluator não tinha uma rubrica para aquela situação. Quando o KODA recomendou creatina para um cliente com problema renal, a rubrica "verificar contraindicações" não existia. Ela foi adicionada em 4 horas. Hoje, a lista de rubricas do KODA tem 23 critérios — e cada um existe porque um bug real de produção ensinou uma lição.

**Lição 2: State persistence não é otimização — é requisito de negócio.** O KODA já perdeu 3 conversas de 2 horas porque o servidor reiniciou durante um deploy. Depois de implementar escrita de estado a cada transição (não a cada turno), a perda de contexto em reinicializações caiu para zero. O cliente nem percebe que o servidor caiu — o Orchestrator recarrega `state.json` e continua de onde parou.

**Lição 3: Fallback não é falha — é honestidade.** Quando o KODA não tem certeza sobre uma recomendação, ele diz "deixa eu confirmar uma informação e já volto". Isso acontece em 3.2% dos turnos. Desses, 78% são resolvidos com intervenção humana em menos de 5 minutos. Os outros 22% são situações onde o melhor era não responder — como um cliente perguntando sobre interação medicamentosa. O fallback salvou o KODA de recomendações perigosas. Ele não é uma falha do sistema. É uma feature de segurança.

---

## 🎯 Desafios Extra (Opcional)

Se terminar o exercício base antes do tempo, implemente um ou mais destes desafios:

### Desafio 1: Estratégia de Coordenação Paralela

Modifique o orquestrador para que, no estágio CONSIDERATION, o Catalog Agent execute buscas paralelas quando a intenção do cliente não tem categoria específica. Use `concurrent.futures.ThreadPoolExecutor` para buscar em 3 categorias diferentes simultaneamente e depois agregar os resultados.

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def catalog_agent_parallel(
    intent: Intent,
    profile: CustomerProfile,
    catalog: list[Product],
) -> list[Product]:
    """Busca produtos em múltiplas categorias em paralelo."""
    # TODO: Implementar
```

### Desafio 2: Métricas de Qualidade do Pipeline

Implemente um módulo `QualityMetrics` que mede o desempenho do pipeline:

```python
@dataclass
class PipelineMetrics:
    total_turns: int = 0
    approval_rate: float = 0.0          # % de gerações aprovadas na primeira tentativa
    avg_latency_ms: float = 0.0         # latência média por turno
    budget_accuracy: float = 0.0        # % de recomendações que respeitam orçamento
    restriction_accuracy: float = 0.0   # % de recomendações que respeitam restrições
    conversion_rate: float = 0.0        # % de conversas que resultam em pedido
    avg_retries_until_approval: float = 0.0  # média de retries até aprovação
    fallback_rate: float = 0.0          # % de turnos que terminaram em fallback

def compute_pipeline_metrics(conversation_dirs: list[Path]) -> PipelineMetrics:
    """Analisa múltiplas conversas e calcula métricas agregadas."""
    # TODO: Implementar
```

### Desafio 3: Persistência em SQLite

Substitua os arquivos JSON por um banco SQLite com schema normalizado:

```python
import sqlite3

class JourneyStateDB:
    """Gerencia estado de jornadas em SQLite."""

    def __init__(self, db_path: str = "koda_journey.db"):
        self.conn = sqlite3.connect(db_path)
        self._create_tables()

    def _create_tables(self) -> None:
        """Cria tabelas: customers, journeys, turns, generations, evaluations, orders."""
        # TODO: Implementar schema

    def save_journey_state(self, state: JourneyState) -> int:
        """Persiste estado da jornada e retorna ID."""
        # TODO: Implementar

    def load_journey_state(self, conversation_id: str) -> Optional[JourneyState]:
        """Carrega estado da jornada do banco."""
        # TODO: Implementar
```

### Desafio 4: Simulação de Conversa Completa

Implemente um simulador de cliente que interage com o pipeline por múltiplos turnos:

```python
def simulate_full_conversation(
    conversation_id: str,
    initial_message: str,
    num_turns: int = 10,
) -> list[dict[str, Any]]:
    """
    Simula uma conversa completa de N turnos.

    O cliente simulado:
    - Envia mensagem inicial
    - Responde a perguntas do KODA
    - Fornece informações quando solicitado
    - Confirma pedido no estágio DECISION
    - Interage com follow-up no estágio RETENTION

    Retorna lista de turnos com mensagens, estados e métricas.
    """
    # TODO: Implementar
```

---

## ✅ Checklist de Implementação

- [ ] `write_json()` implementada com escrita atômica (tempfile)
- [ ] `read_json()` implementada
- [ ] `ensure_state_dir()` implementada
- [ ] `update_journey_state()` implementada
- [ ] `discovery_agent()` implementada (6 intenções + extração de entidades)
- [ ] `catalog_agent()` implementada (5 filtros + ranqueamento)
- [ ] `generator_agent()` implementada (template PT-BR, emojis, personalização)
- [ ] `evaluator_agent()` implementada (8 rubricas com evidência)
- [ ] `order_agent()` implementada (validação SKU, estoque, ZIP, desconto)
- [ ] `fulfillment_agent()` implementada (tracking, carrier, prazo)
- [ ] `retention_agent()` implementada (follow-up, ofertas)
- [ ] `evaluate_guard_conditions()` implementada (todas as transições)
- [ ] `select_transition()` implementada (prioridades corretas)
- [ ] `run_customer_journey_turn()` implementada (orquestração + retry loop)
- [ ] Catálogo com 15 produtos implementado
- [ ] Cenário 1 (caminho feliz) passa ✅
- [ ] Cenário 2 (restrição lactose) passa ✅
- [ ] Cenário 3 (orçamento impossível) passa ✅
- [ ] Cenário 4 (cliente vegano) passa ✅
- [ ] Cenário 5 (rejeição + retry + fallback) passa ✅
- [ ] Cenário 6 (pipeline pedido completo) passa ✅
- [ ] Cenário 7 (CEP inválido) passa ✅
- [ ] Cenário 8 (fora de estoque) passa ✅
- [ ] Todos os dataclasses têm type hints
- [ ] Nenhum `except: pass` vazio
- [ ] Nenhum `# type: ignore`
- [ ] Arquivos JSON incluem `schema_version`, `conversation_id`, `timestamp`
- [ ] Código segue PEP 8
- [ ] Nenhum placeholder, TBD ou TODO no código de produção

---

## 🔧 Guia de Debug: Como Diagnosticar Falhas no Pipeline

Quando seu pipeline não funciona, a causa NUNCA está em um lugar só. Siga este protocolo de diagnóstico:

### Protocolo de 5 Passos

**Passo 1: Isole o agente com falha**

Rode cada agente isoladamente com dados conhecidos:

```python
# Teste isolado do Discovery
intent, profile = discovery_agent(
    "Quero comprar whey. Orçamento R$ 150.",
    conversation_id="debug_001"
)
print(f"Intent: {intent}")         # Deve ser PRODUCT_DISCOVERY
print(f"Budget: {profile.budget_brl}")  # Deve ser 150.0
```

Se o agente funciona isolado mas falha no pipeline, o problema está na integração (orquestrador ou passagem de dados).

**Passo 2: Verifique os arquivos de estado**

Abra cada arquivo JSON gerado e verifique se os dados estão corretos:

```bash
cat state/debug_001/profile.json | python -m json.tool
cat state/debug_001/evaluation.json | python -m json.tool
```

Compare com os schemas esperados na seção "Estrutura de Arquivos de Estado". Campos faltando, tipos errados ou timestamps nulos são causas comuns de falha.

**Passo 3: Teste as guard conditions isoladamente**

```python
state = JourneyState(
    conversation_id="debug_001",
    current_stage=JourneyStage.AWARENESS,
    context={"intent_classified": True, "minimal_context_collected": True}
)
profile = CustomerProfile(name="Teste", customer_id="x")
transitions = evaluate_guard_conditions(state, profile)
for t in transitions:
    print(f"{t['from']} → {t['to']}: {t['status']}")

# Deve mostrar AWARENESS → CONSIDERATION: ALL_PASS
```

**Passo 4: Force o cenário de falha**

Se o cenário 5 (retry + fallback) não está funcionando, force uma rejeição:

```python
# Injete um perfil com restrição que nunca passa
profile = CustomerProfile(
    name="Debug",
    customer_id="x",
    budget_brl=1.0,  # Nenhum produto cabe
    dietary_restrictions=["lactose_free"]
)
```

Com budget de R$ 1.00, `catalog_agent` retorna lista vazia → Generator produz resposta de "sem opções" → Evaluator verifica budget → se o sistema não trata lista vazia corretamente, o bug aparece aqui.

**Passo 5: Trace o fluxo completo com prints**

Adicione logs temporários no orquestrador:

```python
def run_customer_journey_turn(...):
    print(f"[DEBUG] Estágio atual: {state.current_stage}")
    print(f"[DEBUG] Intenção: {intent}")
    print(f"[DEBUG] Produtos encontrados: {len(products)}")
    print(f"[DEBUG] Status avaliação: {evaluation.status}")
    if evaluation.status == "rejected":
        print(f"[DEBUG] Feedback: {evaluation.feedback}")
```

Remova os prints antes de considerar o código finalizado. Eles são muletas de debug, não instrumentação de produção.

### Tabela de Sintomas e Causas

| Sintoma | Causa Provável | Verifique |
|---------|---------------|-----------|
| `json.JSONDecodeError` ao carregar estado | Arquivo corrompido (escrita não-atômica) | `write_json` está usando `tempfile`? |
| `KeyError: 'current_stage'` | `state.json` não foi criado ou está vazio | Orchestrator está chamando `ensure_state_dir`? |
| Agente avança sem nome do cliente | Guard condition não verifica `profile.name != ""` | `evaluate_guard_conditions` para AWARENESS→CONSIDERATION |
| Produto com lactose recomendado para intolerante | Catalog não filtra OU Evaluator não verifica | Ambos! Catalog filtra + Evaluator valida (defesa em profundidade) |
| Retry loop infinito | Contador de retries não está sendo incrementado | Orchestrator: variável `retry_count` sendo passada corretamente? |
| Fallback nunca é chamado | Condição de retry > max_retries não é verificada | `if retry_count >= MAX_RETRIES: return FALLBACK_RESPONSE` |
| `order.json` com `total_brl=0` | Desconto não calculado OU produto não encontrado no catálogo | `order_agent`: busca pelo SKU retorna `None`? |
| Tracking sempre "Correios" | Carrier não está usando o estado do endereço | `fulfillment_agent`: `if "SP" in address["state"]` está correto? |
| Follow-up agendado no passado | Cálculo de datas usando `datetime.now()` errado | `retention_agent`: `timedelta(days=...)` está positivo? |

---

## 🧪 Teste de Integração: Conectando Todos os Agentes

Além dos 8 cenários unitários, implemente um teste de integração que simula uma conversa completa de 5 turnos:

```python
def test_integration_full_conversation() -> bool:
    """
    Simula a conversa completa da Patrícia (5 turnos).

    Turno 1: "Oi, quero algo pra me recuperar depois do treino. R$ 200."
    Turno 2: "Patrícia. Sou intolerante a lactose."
    Turno 3: "Gostei do ZMA. Me fala mais."
    Turno 4: "Vou levar o ZMA."
    Turno 5: "Meu endereço é Rua Augusta, 1500, SP, 01310100. Pode ser PIX?"

    Verificações:
    - Turno 1: estágio AWARENESS, intent=PRODUCT_DISCOVERY
    - Turno 2: estágio CONSIDERATION, perfil com lactose_free
    - Turno 3: resposta do Generator aprovada pelo Evaluator
    - Turno 4: estado avança para DECISION
    - Turno 5: order.json criado, fulfillment.json criado,
      retention.json criado com follow-up futuro
    - Nenhum turno retornou fallback
    - state.json tem 4+ transições registradas
    - Todos os arquivos JSON têm schema_version="2.0"
    """
    conv_id = f"integration_test_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"

    # Turno 1
    result = run_customer_journey_turn(
        "Oi, quero algo pra me recuperar melhor depois do treino. Meu orçamento é R$ 200.",
        conv_id, FUTANBEAR_CATALOG
    )
    assert result["stage"] == JourneyStage.AWARENESS
    assert "orçamento" in result["response"].lower() or "nome" in result["response"].lower()

    # Turno 2
    result = run_customer_journey_turn(
        "Patrícia. E sim, sou intolerante a lactose.",
        conv_id, FUTANBEAR_CATALOG
    )
    assert result["stage"] == JourneyStage.CONSIDERATION
    assert result["evaluation"] is not None
    assert result["evaluation"].status == "approved"

    # Turno 3
    result = run_customer_journey_turn(
        "Gostei do ZMA. Me fala mais sobre ele.",
        conv_id, FUTANBEAR_CATALOG
    )
    assert result["stage"] == JourneyStage.CONSIDERATION
    assert "ZMA" in result["response"]

    # Turno 4
    result = run_customer_journey_turn(
        "Vou levar o ZMA mesmo. Pode fechar o pedido.",
        conv_id, FUTANBEAR_CATALOG
    )
    assert result["stage"] == JourneyStage.DECISION

    # Turno 5
    result = run_customer_journey_turn(
        "Meu endereço é Rua Augusta, 1500, São Paulo, SP, 01310100. Pago no PIX.",
        conv_id, FUTANBEAR_CATALOG
    )
    assert result["order"] is not None
    assert result["order"].payment_status == "confirmed"
    assert result["order"].total_brl > 0

    # Verificações finais
    state_dir = Path(f"state/{conv_id}")
    assert (state_dir / "profile.json").exists()
    assert (state_dir / "state.json").exists()
    assert (state_dir / "generation.json").exists()
    assert (state_dir / "evaluation.json").exists()
    assert (state_dir / "order.json").exists()
    assert (state_dir / "fulfillment.json").exists()
    assert (state_dir / "retention.json").exists()

    # Verificar schema_version em todos os arquivos
    for json_file in state_dir.glob("*.json"):
        data = read_json(json_file)
        assert "schema_version" in data, f"schema_version ausente em {json_file.name}"
        assert data["schema_version"] == "2.0", f"Versão errada em {json_file.name}"

    # Verificar histórico de transições
    state_data = read_json(state_dir / "state.json")
    assert len(state_data["stage_history"]) >= 3  # Pelo menos 3 transições

    return True
```

Este teste de integração é o seu **smoke test**: se ele passa, o pipeline está estruturalmente correto. Se falha, volte ao protocolo de debug de 5 passos.

---

## 📊 Métricas de Pipeline: Como Medir a Qualidade do Seu Sistema

Implemente esta função para avaliar a qualidade do seu pipeline:

```python
@dataclass
class PipelineReport:
    """Relatório de qualidade do pipeline após N conversas."""
    total_conversations: int = 0
    total_turns: int = 0
    approval_rate: float = 0.0
    budget_violations: int = 0
    restriction_violations: int = 0
    fallback_rate: float = 0.0
    avg_products_recommended: float = 0.0
    conversion_rate: float = 0.0


def generate_pipeline_report(conversation_ids: list[str]) -> PipelineReport:
    """Analisa múltiplas conversas e gera relatório de qualidade.

    Para cada conversa no diretório state/<conversation_id>/:
    - Conta turnos (avaliações feitas)
    - Calcula taxa de aprovação (avaliações aprovadas / total)
    - Conta violações de orçamento e restrições
    - Calcula taxa de fallback
    - Mede conversão (% de conversas com pedido confirmado)

    Use este relatório para iterar no seu código:
    - approval_rate < 80%: Generator precisa melhorar
    - budget_violations > 0: Catalog ou Evaluator com bug
    - restriction_violations > 0: Catalog não está filtrando corretamente
    - fallback_rate > 30%: Pipeline muito restritivo, afrouxe critérios
    - conversion_rate < 20%: Jornada de compra tem atrito
    """
    # TODO: Implementar
```

---

## 💡 Dicas de Implementação

**Dica 1:** Comece pelos modelos de dados. Os dataclasses são o contrato do sistema. Se eles estiverem corretos, o resto flui.

**Dica 2:** Implemente e teste um agente por vez. Comece pelo Discovery — é o mais simples e independe dos outros. Depois Catalog, Generator, Evaluator. Deixe Order/Fulfillment/Retention para depois que o pipeline base estiver funcionando.

**Dica 3:** O Discovery Agent pode usar `re.findall(r'R\$\s*(\d+[\.,]?\d*)', message)` para extrair orçamento. Simples e eficaz.

**Dica 4:** O Evaluator é o coração da segurança. Gaste tempo extra aqui. Cada rubrica deve ter uma verificação objetiva. Nada de "parece bom". SEMPRE use comparações concretas: `price <= budget`, `lactose_free == True`.

**Dica 5:** No retry loop, o Generator deve receber o `evaluation.feedback` como contexto adicional. Use esse feedback para corrigir a resposta. Ex: se o feedback diz "RESTRICAO_ORCAMENTO falhou", filtre novamente removendo produtos acima do orçamento.

**Dica 6:** Para testar o fallback rapidamente, use um perfil com `budget_brl=1.0` — nenhum produto cabe nesse orçamento, forçando fallback em todos os cenários.

**Dica 7:** Os arquivos JSON são seu audit trail. Se algo falhar, abra `state/<id>/evaluation.json` e leia o campo `rubric_results` — ele diz exatamente qual critério falhou e por quê.

**Dica 8:** Mantenha as respostas do Generator curtas. WhatsApp é um meio de mensagens rápidas. Respostas longas (acima de 5 linhas) parecem robóticas. O Evaluator pode verificar `len(candidate_response) < 800` como critério extra.

**Dica 9:** Para testar transições de estágio, você pode pular o pipeline normal injetando um `state.json` pré-montado com `current_stage=CONSIDERATION` e contexto preenchido. Isso permite testar estágios avançados sem rodar a jornada inteira.

**Dica 10:** Use `dataclasses.asdict()` para converter dataclasses em dicts antes de escrever JSON. Isso evita escrever serializadores manuais para cada classe.

---

## ✅ Validação Final

Sua implementação está correta se:

1. ✅ Todos os 8 cenários de teste passam
2. ✅ Discovery classifica corretamente as 6 intenções (PRODUCT_DISCOVERY, ORDER_STATUS, SUPPORT, RICOMPRA, RECLAMACAO, UNKNOWN)
3. ✅ Nenhum produto acima do orçamento aparece em `catalog_results`
4. ✅ Nenhum produto com restrição violada aparece em `catalog_results`
5. ✅ `generation.json` tem `candidate_response` preenchida com nome do cliente
6. ✅ `evaluation.json` tem `status` válido e `rubric_results` com evidências
7. ✅ Fallback é retornado quando 2 retries falham
8. ✅ `order.json` tem `payment_status` e `total_brl` calculados
9. ✅ `fulfillment.json` tem `tracking_code` no formato KDA-XXXXXX
10. ✅ `retention.json` tem `follow_up_scheduled_at` como data futura
11. ✅ `state.json` registra todas as transições no `stage_history`
12. ✅ Código tem type hints em todas as funções públicas
13. ✅ Nenhum `except: pass` vazio ou `# type: ignore`
14. ✅ Todos os arquivos JSON incluem `schema_version`, `conversation_id` e timestamp
15. ✅ Pipeline cobre todas as etapas: discovery → recomendação → pedido → pós-venda

---

## 🎓 O Que Você Aprendeu

Após completar este exercício, você entende na prática:

- ✅ **Orquestração de múltiplos agentes:** Como 7 agentes especializados colaboram via contratos JSON, cada um com responsabilidade única e finita

- ✅ **Máquina de estados em pipeline de negócio:** Como AWARENESS → CONSIDERATION → DECISION → RETENTION formam uma jornada completa com guard conditions explícitas

- ✅ **File-based coordination em escala:** Como arquivos JSON viram o contrato de comunicação entre agentes — simples, auditável e pronto para evoluir para filas e bancos

- ✅ **Separação de responsabilidades como segurança:** Por que o Generator nunca avalia e o Evaluator nunca gera — e como isso previne sycophancy e auto-aprovação

- ✅ **Retry loop com fallback seguro:** Como implementar um harness que detecta falhas, fornece feedback, re-tenta e, quando tudo falha, admite limitação em vez de arriscar

- ✅ **Validação determinística de regras de negócio:** Como rubricas objetivas (preço ≤ orçamento, lactose_free = True) protegem o cliente sem depender de outro LLM

- ✅ **Pipeline completo de vendas:** Do discovery à retenção, como cada etapa adiciona valor e como a transição entre elas é governada por condições verificáveis

- ✅ **Audit trail como ferramenta de debug:** Como cada decisão é registrada em arquivos versionáveis, permitindo reconstruir qualquer conversa meses depois

- ✅ **Design que escala:** Que a arquitetura de agentes com contratos JSON escala naturalmente de um protótipo Python para um sistema distribuído com filas, APIs e bancos de dados

- ✅ **Conexão com todo o currículo:** Como Token Budgeting (N1), Generator/Evaluator (N2), State Persistence (N3) e Customer Journey Flows (N4) se integram em um sistema coeso

---

## 🔍 Walkthrough Detalhado: Execução Passo a Passo

Para consolidar seu entendimento, vamos acompanhar exatamente o que acontece quando Patrícia envia sua primeira mensagem.

### Turno 1: "Oi, quero algo pra me recuperar melhor depois do treino. Meu orçamento é R$ 200."

**Passo 1 — Orchestrator carrega estado:**
```
state/conv_patricia_001/ não existe → primeiro contato
Cria JourneyState com current_stage=ENTRY
Cria CustomerProfile com customer_id="wa_5511999999999"
```

**Passo 2 — Discovery Agent processa:**
```
Entrada: "Oi, quero algo pra me recuperar melhor depois do treino. Meu orçamento é R$ 200."
→ Regex encontra: "R$ 200" → budget_brl = 200.00
→ Palavras-chave: "recuperar", "pós-treino"? ("depois do treino") → PRODUCT_DISCOVERY
→ Sem menção a restrições alimentares → dietary_restrictions = []
→ Intenção classificada: PRODUCT_DISCOVERY

Saída:
  Intent.PRODUCT_DISCOVERY
  CustomerProfile(budget_brl=200.00, dietary_restrictions=[], training_goal="recuperação")
```

**Passo 3 — Guard Conditions:**
```
Estágio atual: ENTRY
Transição possível: ENTRY → AWARENESS (sempre permitida)
→ Seleciona AWARENESS
```

**Passo 4 — Estágio AWARENESS:**
```
Como o perfil não tem nome, o sistema pergunta:
"Oi! Antes de te mostrar os produtos, me conta: qual seu nome? 
E você tem alguma restrição alimentar? (intolerância a lactose, vegetariano, etc.)"
```

**Passo 5 — Persistência:**
```
Salva state/conv_patricia_001/state.json:
{
  "current_stage": "AWARENESS",
  "stage_history": [
    {"from": "ENTRY", "to": "AWARENESS", "trigger": "first_message"}
  ],
  "context": {"intent_classified": true, "minimal_context_collected": false}
}

Salva state/conv_patricia_001/profile.json:
{
  "customer_id": "wa_5511999999999",
  "budget_brl": 200.00,
  "dietary_restrictions": []
}
```

### Turno 2: "Patrícia. E sim, sou intolerante a lactose."

**Passo 1 — Orchestrator carrega estado:**
```
Carrega profile.json → budget_brl=200, dietary_restrictions=[]
Carrega state.json → current_stage=AWARENESS, minimal_context_collected=false
```

**Passo 2 — Discovery Agent processa:**
```
Entrada: "Patrícia. E sim, sou intolerante a lactose."
→ Nome detectado: "Patrícia"
→ Restrição detectada: "intolerante a lactose" → dietary_restrictions.append("lactose_free")
→ Intenção: a conversa continua, mantém PRODUCT_DISCOVERY

Saída:
  Intent.PRODUCT_DISCOVERY
  CustomerProfile(name="Patrícia", budget_brl=200.00, dietary_restrictions=["lactose_free"])
```

**Passo 3 — Guard Conditions:**
```
Estágio atual: AWARENESS
Avalia AWARENESS → CONSIDERATION:
  - profile.name != "" ✓ ("Patrícia")
  - state.context["intent_classified"] == True ✓
  - state.context["minimal_context_collected"] ← atualiza para True
→ Transição selecionada: AWARENESS → CONSIDERATION
```

**Passo 4 — Estágio CONSIDERATION: Catalog Agent:**
```
Entrada: intent=PRODUCT_DISCOVERY, profile (lactose_free, budget=200)
→ Categoria inferida: "recuperação", "depois do treino" → post_workout
→ Filtros aplicados:
  1. category == "post_workout"
  2. lactose_free == True (restrição)
  3. price_brl <= 200.00 (orçamento)
  4. in_stock == True

Resultado (do catálogo):
  - REC-ZMA-120: ZMA, R$ 89.90, lactose_free=True, vegan=True, rating=4.6
  - REC-GLUT-300: L-Glutamina, R$ 69.90, lactose_free=True, rating=4.5
  - REC-BCAA-400: BCAA, R$ 79.90, lactose_free=True, rating=4.3
```

**Passo 5 — Generator Agent:**
```
Gera resposta:
"Oi Patrícia! 🌟 Encontrei 3 opções excelentes para sua recuperação pós-treino, 
todas sem lactose:

🏷️ ZMA 120 Cápsulas
✅ Zinco, Magnésio e Vitamina B6
✅ Melhora recuperação e qualidade do sono
✅ 100% vegano
💰 R$ 89,90
⭐ 4.6/5

🏷️ L-Glutamina 300g
✅ Acelera recuperação muscular
✅ Fortalece sistema imunológico
✅ 60 doses
💰 R$ 69,90
⭐ 4.5/5

🏷️ BCAA 400g
✅ Aminoácidos para recuperação
✅ 40 doses
✅ Ótimo custo-benefício
💰 R$ 79,90
⭐ 4.3/5

Qual desses combina mais com sua rotina? Posso te explicar melhor qualquer um! 😊"
```

**Passo 6 — Evaluator Agent:**
```
Verifica 8 rubricas:
1. RESTRICAO_ORCAMENTO: max=89.90 <= 200.00 → PASS
2. RESTRICAO_LACTOSE: todos lactose_free=True → PASS
3. RESTRICAO_GLUTEN: não aplicável (sem restrição) → PASS
4. RESTRICAO_VEGANO: não aplicável → PASS
5. RESPOSTA_NAO_VAZIA: len=580 > 10 → PASS
6. TOM_WHATSAPP: len=580 <= 800 → PASS
7. PRODUTOS_EM_ESTOQUE: todos in_stock=True → PASS
8. PERSONALIZACAO: "Patrícia" está na resposta → PASS

Status: APPROVED ✓
```

**Passo 7 — Resposta enviada ao cliente.**

```
state/conv_patricia_001/ agora contém:
├── profile.json          (atualizado com nome + restrições)
├── state.json            (CONSIDERATION, histórico de transições)
├── catalog_results.json  (3 produtos filtrados)
├── generation.json       (resposta candidata)
└── evaluation.json       (status: approved, 8/8 rubricas)
```

### Turno 5: "Vou de ZMA. Pode fechar o pedido."

Após alguns turnos de esclarecimento, Patrícia decide comprar.

**Passo — Estágio DECISION: Order Agent:**
```
Entrada: SKU="REC-ZMA-120", endereço={...}, payment_method="pix"
→ Valida SKU: REC-ZMA-120 existe em FUTANBEAR_CATALOG ✓
→ Valida estoque: in_stock=True ✓
→ Valida CEP: "01310100" → 8 dígitos ✓
→ Calcula total: R$ 89.90
→ Desconto PIX (5%): -R$ 4.50
→ Total final: R$ 85.40
→ payment_status: "confirmed"

Arquivo order.json:
{
  "order_id": "KDA-PATRICIA-001",
  "items": [{"sku": "REC-ZMA-120", "qty": 1, "price": 89.90}],
  "total_brl": 85.40,
  "discount_applied": 4.50,
  "payment_method": "pix",
  "payment_status": "confirmed"
}
```

**Passo — Fulfillment Agent:**
```
Entrada: order (status=confirmed, endereço em SP)
→ carrier = "Loggi" (SP)
→ estimated_delivery = hoje + 1 dia = "2026-05-29"
→ tracking_code = "KDA-847291"

Arquivo fulfillment.json:
{
  "tracking_code": "KDA-847291",
  "carrier": "Loggi",
  "estimated_delivery": "2026-05-29",
  "status": "processing"
}
```

**Passo — Retention Agent:**
```
Entrada: profile (primeira compra), order (REC-ZMA-120, 120 servings)
→ follow_up em 96 dias (80% de 120 dias de consumo)
→ oferta: 10% desconto na próxima compra (cliente novo)
→ follow_up_type: "ESTOQUE_ACABANDO"

Arquivo retention.json:
{
  "follow_up_scheduled_at": "2026-08-31T...",
  "follow_up_type": "ESTOQUE_ACABANDO",
  "re_engagement_offers": [
    {"type": "discount", "value": "10%", "condition": "segunda_compra"}
  ]
}
```

**Passo — Transição DECISION → RETENTION:**
```
Guard conditions:
- payment_confirmed: True ✓
- order_created: True ✓
→ Transição executada
```

### O Que Este Trace Demonstra

Em 5 turnos de conversa:
- **7 agentes** especializados colaboraram (Discovery, Catalog, Generator, Evaluator, Order, Fulfillment, Retention)
- **3 estágios** da jornada foram percorridos (AWARENESS → CONSIDERATION → DECISION → RETENTION)
- **12 arquivos JSON** foram criados como audit trail
- **8 rubricas** foram verificadas em cada resposta
- **Nenhuma** restrição foi violada (orçamento R$ 200, lactose_free obrigatório)
- **Nenhum** agente tentou fazer o trabalho de outro

Se daqui a 3 meses Patrícia reclamar que o pedido veio errado, a equipe KODA abre `state/conv_patricia_001/` e reconstrói exatamente o que aconteceu, quando e por quê.

---

## ⚠️ Armadilhas Comuns e Como Evitá-las

### Armadilha 1: "Vou fazer o Generator também avaliar"

**O erro:** Colocar lógica de validação dentro do Generator para "ser mais rápido".

**Por que é perigoso:** O Generator quer agradar. Se ele também avalia, ele vai aprovar a própria resposta — sycophancy. Um estudo interno do KODA mostrou que agentes que se auto-avaliam têm taxa de erro 4x maior que sistemas com Evaluator independente.

**Como evitar:** O Generator NUNCA chama `evaluator_agent()`. O Generator NUNCA lê `evaluation.json`. A única conexão entre eles é o Orchestrator. Se você está tentado a colocar um `if` de validação no Generator, pare — isso é responsabilidade do Evaluator.

### Armadilha 2: "Vou pular a guard condition e ir direto para o próximo estágio"

**O erro:** Hardcodar transições de estágio em vez de verificar as guards.

**Por que é perigoso:** Guards existem para prevenir estados inválidos. Se você pula a verificação `profile.name != ""`, o Generator vai produzir "Oi {vazio}!" — uma resposta que destrói a confiança do cliente em 3 caracteres.

**Como evitar:** SEMPRE chame `evaluate_guard_conditions()` antes de qualquer transição. Se uma guard falha, o sistema deve permanecer no estágio atual e coletar o que falta. Teste com perfis incompletos — se o sistema avança sem nome, sua guard está quebrada.

### Armadilha 3: "Vou usar o catálogo como variável global"

**O erro:** Declarar `FUTANBEAR_CATALOG` como global e acessá-lo diretamente de dentro dos agentes.

**Por que é perigoso:** Agentes acoplados a dados globais não são testáveis isoladamente. Se você quiser testar o Catalog Agent com um catálogo diferente (ex: só 3 produtos), não consegue — ele sempre lê o global. Além disso, em produção, o catálogo viria de uma API — e seu agente não pode depender de um `import` estático.

**Como evitar:** Todos os agentes recebem o catálogo como parâmetro. `catalog_agent(catalog=meu_catalogo)`, não `catalog_agent()` lendo `FUTANBEAR_CATALOG` do módulo. Isso permite teste isolado e evolução para API sem reescrever o agente.

### Armadilha 4: "Vou escrever o JSON direto no arquivo sem tempfile"

**O erro:** Usar `open(path, 'w').write(json.dumps(data))` em vez de escrita atômica.

**Por que é perigoso:** Se o processo cair no meio do `write`, o arquivo fica corrompido (JSON inválido pela metade). Na próxima leitura, `json.load()` explode e o sistema perde o estado da conversa. Com 500 conversas ativas simultâneas em produção, isso significa 500 clientes perdidos.

**Como evitar:** SEMPRE use `tempfile.NamedTemporaryFile` + `os.replace`. A escrita atômica garante que o arquivo só aparece no destino quando está completamente escrito e válido. É 4 linhas a mais de código que previnem corrupção de dados em escala.

### Armadilha 5: "Vou fazer o Evaluator chamar outro LLM"

**O erro:** Usar um LLM (como Claude) para avaliar a resposta do Generator, em vez de regras determinísticas.

**Por que é perigoso:** Um LLM avaliando outro LLM introduz os mesmos vieses. Se o Generator disse "R$ 89,90" mas o orçamento é R$ 80, um LLM-Evaluator pode achar que "está perto o suficiente" e aprovar. Regras determinísticas nunca "acham" — elas comparam: `89.90 <= 80.00 → False → REJECTED`.

**Como evitar:** Use o Evaluator determinístico para todas as regras de negócio (orçamento, restrições, estoque). Use LLM-Evaluator apenas para critérios subjetivos (tom da resposta, clareza, empatia) — e mesmo assim, como camada adicional, não substituta. O KODA em produção usa ambos: regras determinísticas como safety net, LLM como quality assessor.

### Armadilha 6: "Se o orçamento é impossível, não mostro nada"

**O erro:** Quando nenhum produto cabe no orçamento, retornar lista vazia e uma resposta genérica.

**Por que é perigoso:** "Nenhum produto encontrado" quebra a confiança. O cliente forneceu uma restrição real (orçamento) e recebeu silêncio. Melhor: ser transparente sobre a limitação.

**Como evitar:** Quando `catalog_agent()` retorna lista vazia, o Generator deve produzir uma resposta honesta: "Patrícia, com orçamento de R$ 50, não temos pré-treinos nessa faixa no momento. Mas tenho opções a partir de R$ 89,90. Quer dar uma olhada mesmo assim? Ou prefere que eu sugira algo em outra categoria?" O Evaluator aprova essa resposta — transparência é qualidade.

### Armadilha 7: "Vou testar só o caminho feliz"

**O erro:** Rodar apenas o cenário 1 e assumir que o sistema funciona.

**Por que é perigoso:** O caminho feliz testa ~20% do código. Os outros 80% estão nos cenários de erro: restrições violadas, orçamento impossível, retry loop, fallback, CEP inválido, produto fora de estoque. Bugs nesses cenários aparecem em produção, com clientes reais.

**Como evitar:** Execute TODOS os 8 cenários. Se algum falhar, corrija antes de considerar o exercício completo. O cenário 5 (retry + fallback) é particularmente revelador — 80% dos alunos encontram bugs nele na primeira tentativa.

---

## 📂 Estrutura de Arquivos de Estado: O Contrato Completo

Entenda exatamente o que cada arquivo contém e como os agentes os usam:

### `profile.json` — O Perfil do Cliente

```json
{
  "schema_version": "2.0",
  "conversation_id": "conv_patricia_001",
  "customer_id": "wa_5511999999999",
  "name": "Patrícia",
  "whatsapp_number": "+55 11 99999-9999",
  "budget_brl": 200.00,
  "dietary_restrictions": ["lactose_free"],
  "allergies": [],
  "training_goal": "recuperação pós-treino",
  "training_frequency": "5x por semana",
  "preferred_flavor": null,
  "preferred_format": "cápsulas",
  "purchase_history": [],
  "created_at": "2026-05-28T10:42:00Z",
  "updated_at": "2026-05-28T10:45:00Z"
}
```

**Quem escreve:** Discovery Agent (a cada turno, se novas informações foram extraídas)
**Quem lê:** Catalog Agent, Generator Agent, Evaluator Agent, Order Agent, Retention Agent

### `state.json` — O Estado da Jornada

```json
{
  "schema_version": "2.0",
  "conversation_id": "conv_patricia_001",
  "customer_id": "wa_5511999999999",
  "current_stage": "CONSIDERATION",
  "current_sub_state": "COMPARISON",
  "stage_history": [
    {
      "from": "ENTRY",
      "to": "AWARENESS",
      "timestamp": "2026-05-28T10:42:01Z",
      "trigger": "first_message",
      "guard_evaluation": "ALL_PASS"
    },
    {
      "from": "AWARENESS",
      "to": "CONSIDERATION",
      "timestamp": "2026-05-28T10:45:00Z",
      "trigger": "context_sufficient",
      "guard_evaluation": "ALL_PASS"
    }
  ],
  "context": {
    "intent_classified": true,
    "minimal_context_collected": true,
    "product_selected": false,
    "product_validated": false
  },
  "metrics": {
    "messages_exchanged": 4,
    "products_shown": 3,
    "time_in_current_stage_seconds": 180,
    "total_session_time_seconds": 320
  },
  "created_at": "2026-05-28T10:42:00Z",
  "updated_at": "2026-05-28T10:45:00Z"
}
```

**Quem escreve:** Orchestrator (`run_customer_journey_turn`)
**Quem lê:** Orchestrator, `evaluate_guard_conditions`

### `generation.json` — A Resposta Candidata

```json
{
  "schema_version": "2.0",
  "conversation_id": "conv_patricia_001",
  "candidate_response": "Oi Patrícia! 🌟 Encontrei 3 opções...",
  "products_mentioned": ["REC-ZMA-120", "REC-GLUT-300", "REC-BCAA-400"],
  "tone": "whatsapp_natural",
  "generated_at": "2026-05-28T10:45:01Z"
}
```

**Quem escreve:** Generator Agent
**Quem lê:** Evaluator Agent

### `evaluation.json` — O Veredito

```json
{
  "schema_version": "2.0",
  "conversation_id": "conv_patricia_001",
  "status": "approved",
  "rubric_results": [
    {
      "criterion": "RESTRICAO_ORCAMENTO",
      "passed": true,
      "evidence": "Preço máximo recomendado: R$ 89.90. Orçamento: R$ 200.00. Todos os produtos dentro do limite."
    },
    {
      "criterion": "RESTRICAO_LACTOSE",
      "passed": true,
      "evidence": "3 produtos verificados. Todos lactose_free=True. Restrição do cliente respeitada."
    },
    {
      "criterion": "TOM_WHATSAPP",
      "passed": true,
      "evidence": "Resposta tem 580 caracteres (limite: 800). Tom natural, emojis apropriados."
    },
    {
      "criterion": "PERSONALIZACAO",
      "passed": true,
      "evidence": "Nome 'Patrícia' encontrado na saudação inicial da resposta."
    }
  ],
  "feedback": "",
  "checked_at": "2026-05-28T10:45:02Z"
}
```

**Quem escreve:** Evaluator Agent
**Quem lê:** Orchestrator (para decidir se aprova ou inicia retry)

### `order.json` — O Pedido

```json
{
  "schema_version": "2.0",
  "conversation_id": "conv_patricia_001",
  "order_id": "KDA-PATRICIA-001",
  "items": [
    {"sku": "REC-ZMA-120", "name": "ZMA 120 Cápsulas", "qty": 1, "unit_price_brl": 89.90}
  ],
  "total_brl": 85.40,
  "discount_applied": 4.50,
  "shipping_address": {
    "street": "Rua Augusta",
    "number": "1500",
    "city": "São Paulo",
    "state": "SP",
    "zip": "01310100"
  },
  "payment_method": "pix",
  "payment_status": "confirmed",
  "created_at": "2026-05-28T10:52:00Z"
}
```

**Quem escreve:** Order Agent
**Quem lê:** Fulfillment Agent, Retention Agent

### `fulfillment.json` — O Tracking

```json
{
  "schema_version": "2.0",
  "conversation_id": "conv_patricia_001",
  "order_id": "KDA-PATRICIA-001",
  "tracking_code": "KDA-847291",
  "carrier": "Loggi",
  "estimated_delivery": "2026-05-29",
  "status": "processing",
  "delivered_at": null,
  "updated_at": "2026-05-28T10:52:01Z"
}
```

**Quem escreve:** Fulfillment Agent
**Quem lê:** Retention Agent (para calcular data de follow-up após entrega)

### `retention.json` — O Follow-Up

```json
{
  "schema_version": "2.0",
  "conversation_id": "conv_patricia_001",
  "customer_id": "wa_5511999999999",
  "follow_up_scheduled_at": "2026-08-31T10:52:00Z",
  "follow_up_type": "ESTOQUE_ACABANDO",
  "re_engagement_offers": [
    {
      "type": "discount",
      "value": "10%",
      "condition": "segunda_compra",
      "message": "Patrícia, seu ZMA deve estar acabando! Volte e ganhe 10% off na próxima compra."
    }
  ],
  "last_contact_at": "2026-05-28T10:52:00Z"
}
```

**Quem escreve:** Retention Agent
**Quem lê:** Orchestrator (no próximo contato do cliente, para decidir se é momento de follow-up)

### O Fluxo Completo de Arquivos por Turno

```
TURNO 1 (ENTRY → AWARENESS):
  profile.json (criado)
  state.json (criado)

TURNO 2 (AWARENESS → CONSIDERATION):
  profile.json (atualizado)
  state.json (atualizado)
  catalog_results.json (criado)
  generation.json (criado)
  evaluation.json (criado)

TURNO 5 (CONSIDERATION → DECISION → RETENTION):
  profile.json (atualizado)
  state.json (atualizado)
  catalog_results.json (atualizado)
  generation.json (atualizado)
  evaluation.json (atualizado)
  order.json (criado)
  fulfillment.json (criado)
  retention.json (criado)
```

Cada arquivo é um checkpoint. Se o servidor cair no meio do turno 5, o Orchestrator recarrega `state.json`, vê que `current_stage=CONSIDERATION` e retoma de onde parou.

---

## ❓ Perguntas Frequentes (FAQ)

**P: Por que 7 agentes? Não bastam 3?**

R: Três agentes (Planner, Generator, Evaluator) resolvem o problema de qualidade de resposta — mas não resolvem o problema de negócio completo. No KODA, o pipeline de vendas envolve: classificar intenção (Discovery), buscar produtos (Catalog), gerar resposta (Generator), validar qualidade (Evaluator), processar pagamento (Order), gerenciar entrega (Fulfillment) e fidelizar (Retention). Cada uma dessas responsabilidades tem regras de negócio diferentes. Colocar todas em 3 agentes forced você a escrever código que faz "if intent=ORDER: processa pagamento elif intent=DISCOVERY: busca produtos" — e isso escala mal. Sete agentes = sete responsabilidades bem definidas = código que cresce sem virar monólito.

**P: File-based coordination é lento. Por que não usar filas desde o começo?**

R: Porque você está aprendendo. Filas (RabbitMQ, Kafka) adicionam complexidade operacional que obscurece os conceitos fundamentais. Quando você domina o contrato entre agentes via arquivos JSON, migrar para filas é mecânico: em vez de `write_json("plan.json", data)`, você faz `channel.publish("plan_queue", data)`. O contrato — o schema JSON — permanece idêntico. Aprendizado > performance em exercícios educacionais.

**P: Por que o Generator não usa a API do Claude?**

R: Porque o objetivo deste exercício é a arquitetura de coordenação, não a qualidade da geração de texto. Um Generator baseado em template Python é determinístico e previsível — você sabe exatamente o que vai sair. Isso permite testar o sistema sem depender de APIs externas. Em produção, você substitui o Generator de template por um Generator que chama a API do Claude. O contrato (`generation.json`) não muda.

**P: Posso pular os testes e só implementar os agentes?**

R: Não. Os 8 cenários de teste SÃO a especificação do sistema. Implementar sem testar é construir sem planta. Além disso, pipelines multi-agente têm bugs sutis que só aparecem na interação entre agentes — teste unitário por agente não pega esses bugs. Os cenários de teste simulam exatamente essas interações.

**P: Qual é a diferença entre este exercício e o exercício 1 do Nível 3?**

R: O exercício 1 do Nível 3 foca em 3 agentes (Planner, Generator, Evaluator) operando em um domínio restrito (recomendação de produto). Este exercício expande para 7 agentes, 4 estágios de jornada, máquina de estados completa com guard conditions e pipeline de negócio fim-a-fim (discovery → venda → pós-venda). O Nível 3 ensina o padrão. O Nível 4 ensina a operação.

**P: Meu retry loop não está chamando o fallback. O que fazer?**

R: Verifique três coisas: (1) `retry_count` está sendo incrementado dentro do loop? (2) A condição `if retry_count >= MAX_RETRIES: return FALLBACK` está ANTES de chamar o Generator novamente? (3) O Evaluator está realmente retornando `REJECTED` ou está sempre aprovando? Force uma rejeição com `budget_brl=1.0` para testar.

**P: Preciso implementar TODOS os desafios extras?**

R: Não. Os desafios extras são para quem terminar o exercício base antes do tempo estimado (180 minutos). O exercício base — 7 agentes, pipeline funcional, 8 cenários de teste passando — já é nota máxima. Os desafios são para aprofundamento.

**P: Como sei se meu código está "bom o suficiente"?**

R: Três critérios objetivos: (1) Todos os 8 cenários de teste passam sem modificação manual de estado entre turnos, (2) O teste de integração (`test_integration_full_conversation`) roda do início ao fim sem asserts quebrados, (3) Nenhum arquivo JSON gerado tem campos ausentes ou tipos errados (leia cada arquivo com `json.load` e verifique). Se esses três passam, seu código está excelente. Refinamentos de estilo (nomes de variável, formatação) são secundários.

**P: Posso modificar os dataclasses ou adicionar novos?**

R: Pode — desde que não remova campos obrigatórios e mantenha `schema_version`, `conversation_id` e timestamp em todos os arquivos JSON. Os dataclasses fornecidos são o contrato mínimo. Se precisar de campos adicionais (ex: `preferred_brand` no perfil, `payment_id` no pedido), adicione. Mas não remova o que já existe — os agentes dependem desses campos.

**P: Este pipeline funcionaria para outro tipo de negócio (não-suplementos)?**

R: Sim. A arquitetura é genérica. Os agentes Discovery, Catalog, Generator, Evaluator, Order, Fulfillment e Retention não sabem que estão vendendo suplementos — eles operam sobre dataclasses abstratas (`Product`, `CustomerProfile`, `Order`). Para adaptar a uma loja de roupas, você só precisa: (1) mudar o catálogo de produtos, (2) ajustar as regras de filtro do Catalog (trocar `lactose_free` por `size_available`), (3) ajustar o template do Generator. A máquina de estados, as guard conditions e o retry loop permanecem idênticos.

---

## 📚 Referências & Próximas Leituras

- `curriculum/04-nivel-4-koda-specific/01-koda-architecture.md` — Arquitetura completa do KODA (8 agentes, pipeline, integração WhatsApp)
- `curriculum/04-nivel-4-koda-specific/02-customer-journey-flows.md` — Máquina de estados completa com sub-estados e guard conditions
- `curriculum/04-nivel-4-koda-specific/03-feature-design-patterns.md` — Como desenhar novas features no KODA com contratos explícitos
- `curriculum/03-nivel-3-advanced-architecture/01-multi-agent-systems.md` — Teoria de sistemas multi-agente aplicada ao KODA
- `curriculum/03-nivel-3-advanced-architecture/03-file-based-coordination.md` — Aprofundamento em coordenação por arquivos
- `curriculum/03-nivel-3-advanced-architecture/02-state-persistence.md` — Fundamentos de persistência de estado
- `curriculum/02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md` — Base Generator/Evaluator
- `curriculum/02-nivel-2-practical-patterns/03-rubric-design.md` — Design de rubricas de avaliação
- `curriculum/09-case-studies/04-koda-order-processing.md` — Case study real de processamento de pedidos
- `curriculum/09-case-studies/05-koda-fulfillment-workflow.md` — Case study real de fulfillment

**Solução de referência:** `real-world-exercises/solutions/exercise-02-solution.py`

**Próximo exercício:** `exercise-03.md` — Implementar Harness Evolution e Remoção de Componentes Obsoletos no KODA

---

*Exercício 2 | Nível 4 — KODA-Específico | Curso Long-Running Agents | FutanBear Technical Program*

**Boa sorte! Ao final deste exercício, você terá construído um pipeline completo de customer journey — o coração operacional do KODA.** 🚀

---

### O Que Vem Depois

Este exercício é o ponto de virada do currículo. Até aqui, você aprendeu padrões isolados (N1), aplicou padrões em duplas (N2), orquestrou três agentes (N3) e agora construiu um sistema completo com sete agentes em pipeline de negócio (N4).

O que você construiu aqui não é um exercício acadêmico. É uma **maquete arquitetural 1:1** do que roda em produção no KODA. As diferenças são de escala, não de design:
- Onde você usa funções Python, o KODA usa serviços em containers
- Onde você usa arquivos JSON, o KODA usa PostgreSQL + Redis
- Onde você usa templates, o KODA usa Claude Opus + Claude Sonnet
- Onde você usa regex, o KODA usa few-shot prompting com fallback determinístico

Mas o contrato entre os agentes — os dataclasses, os schemas JSON, as guard conditions, o retry loop, o audit trail — **são idênticos**.

Quando você for entrevistado para uma posição de engenharia de agentes e te perguntarem "você já construiu um sistema multi-agente em produção?", você pode responder: "Sim. Sete agentes. Pipeline de customer journey. File-based coordination com transições por guard conditions. Retry loop com fallback. Audit trail completo. E eu posso te mostrar o código."

Porque você acabou de construí-lo.

**Próximo passo:** Quando estiver pronto, avance para `exercise-03.md` — Harness Evolution. Você vai aprender a identificar quais componentes do seu pipeline são temporários (porque o modelo ainda não é bom o suficiente) e como removê-los quando o modelo evoluir — mantendo o sistema enxuto sem perder segurança.

> **Nota sobre a solução:** O arquivo `real-world-exercises/solutions/exercise-02-solution.py` contém a implementação de referência completa. Use-a apenas como último recurso — o aprendizado real está em construir cada agente, depurar cada guard condition e ver seus 8 cenários de teste passando um por um. A solução existe para destravar, não para substituir o processo de descoberta.

> **Dica de estudo:** Após completar o exercício, volte ao `02-customer-journey-flows.md` e releia o Prólogo da Marina. Você vai perceber que cada decisão que o KODA tomou naquela conversa agora tem um agente, uma guard condition e um arquivo JSON correspondente no pipeline que você construiu. O que antes era "mágica" agora é código. Esse é o sinal de que o Nível 4 foi internalizado.

*Fim do Exercício 2*
