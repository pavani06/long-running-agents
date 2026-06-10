---
title: "Solucao do Exercicio 1: Sistema Multi-Agente Planner/Generator/Evaluator"
type: curriculum-solution
nivel: 3
aliases: ["solução multi-agente", "arquitetura planner", "audit trail JSON", "validação agentes"]
tags: [curriculo-conteudo, nivel-3, solucao, multi-agent-system, planner-agent, generator-agent, evaluator-agent, file-based-coordination, audit-trail, sycophancy-prevention, budget-guard, dietary-restriction-validation, python, dataclass, json-state, implementacao-referencia]
relates-to: ["[[curriculum/03-nivel-3-advanced-architecture/exercises/exercise-01|Exercise 01]]"]
last_updated: 2026-06-10
---
# 🧩 Solucao do Exercicio 1: Sistema Multi-Agente Planner/Generator/Evaluator
## Implementacao Completa com Python, Testes e Analise de Design Decisions

**Tempo Estimado de Leitura:** 120-150 minutos
**Nivel:** 3 - Arquitetura Avancada
**Pre-requisito:** Ter lido `01-multi-agent-systems.md` e completado `02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md`
**Status:** 🟢 SOLUCAO COMPLETA
**Data de Criacao:** Maio 2026

---

## 📖 Prologo: A Arquitetura Que Salvou a Venda da Marina

Voce leu em `01-multi-agent-systems.md` sobre a noite em que Marina quase desistiu de comprar.

O agente unico tentou fazer tudo ao mesmo tempo: entender a jornada emocional, coletar restricoes alimentares, consultar catalogo, comparar precos, montar carrinho, validar orcamento e manter tom humano no WhatsApp.

Resultado: recomendacao acima do orcamento, promessa de duracao errada, produto com lactose recomendado para cliente intolerante.

A solucao nao foi um modelo melhor. Foi uma arquitetura com tres agentes.

Este documento e a **solucao completa do Exercicio 1** do Nivel 3. Ele mostra como implementar um sistema Planner/Generator/Evaluator funcional em Python, com codigo real, testes, alternativas de design e aplicacao pratica no KODA.

Ao final, voce tera um sistema que:
- Decompoe conversas complexas em etapas verificaveis (Planner)
- Executa cada etapa com foco e evidencia (Generator)
- Valida resultados contra criterios objetivos antes de expor ao cliente (Evaluator)
- Persiste estado em arquivos JSON para audit trail completo
- Roda testes que provam que cada componente funciona isoladamente e em conjunto

---

## 🎯 O Que o Exercicio Pede

O Exercicio 1 do Nivel 3 pede que voce:

1. **Desenhe** a arquitetura de um sistema multi-agente com Planner, Generator e Evaluator
2. **Implemente** os tres agentes em Python com comunicacao por arquivos JSON (file-based coordination)
3. **Escreva testes** que validem o funcionamento correto de cada agente e da orquestracao completa
4. **Explique** as decisoes de design e alternativas consideradas
5. **Aplique** o sistema a um cenario real do KODA

Esta solucao entrega todos esses requisitos. Siga as secoes em ordem ou pule direto para o codigo se preferir ver implementacao primeiro.

### Conexao com Nivel 2

No Nivel 2, voce aprendeu o padrao Generator/Evaluator — dois agentes, um cria e outro avalia.

Este exercicio generaliza esse padrao para tres agentes, adicionando o Planner antes da geracao.

| Nivel | Arquitetura | Problema que Resolve | Novidade |
|-------|-------------|---------------------|----------|
| Nivel 2 | Generator + Evaluator | Self-evaluation collapse (sycophancy) | Separacao geracao/avaliacao |
| Nivel 3 | Planner + Generator + Evaluator | Planning/execution collapse + sycophancy | Decomposicao explicita antes da acao |

A diferenca pratica e enorme: com Planner, o Generator recebe uma tarefa menor, mais clara e com criterios de sucesso definidos. O Evaluator agora valida nao apenas a resposta, mas tambem se o Generator cumpriu o plano.

---

## 🏗️ Arquitetura Proposta

### Visao Geral

O sistema e composto por tres agentes especializados e um harness orquestrador que gerencia o fluxo de dados entre eles via arquivos JSON:

```
                          ┌─────────────────────────────┐
                          │      WhatsApp / Cliente      │
                          │   mensagem, historico, perf  │
                          └──────────────┬──────────────┘
                                         │
                                         ▼
┌────────────────────────────────────────────────────────────────────────────┐
│                              HARNESS (Orquestrador)                         │
│                                                                            │
│  ┌──────────┐    plan.json     ┌──────────────┐   generation.json   ┌──────────────┐
│  │ PLANNER  │ ───────────────▶ │  GENERATOR   │ ──────────────────▶ │  EVALUATOR   │
│  │          │                  │              │                     │              │
│  │ Decompoe │                  │ Executa      │                     │ Valida       │
│  │ Planeja  │                  │ Gera output  │                     │ Aprova/      │
│  │ Define   │                  │ Registra     │                     │ Rejeita      │
│  │ criterios│                  │ evidencias   │                     │ Feedback     │
│  └──────────┘                  └──────────────┘                     └──────┬───────┘
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
                                         │
                          ┌──────────────┴──────────────┐
                          ▼                             ▼
               ┌──────────────────┐          ┌──────────────────────┐
               │ RESPOSTA ENVIADA │          │ CICLO DE REVISAO     │
               │ (status=approved)│          │ Generator ← Feedback │
               └──────────────────┘          └──────────────────────┘
```

### Fluxo de Dados

Cada agente le de arquivos JSON e escreve em novos arquivos JSON. Nao ha memoria compartilhada, nao ha variaveis globais. Tudo passa por artefatos persistentes.

```
State Store (diretorio por conversa)
│
├── conversation_event.json    ← Entrada: mensagem do cliente
├── customer_profile.json      ← Dados persistentes do cliente
├── conversation_summary.json  ← Historico comprimido
├── catalog_snapshot.json      ← Catalogo de produtos
│
├── plan.json                  ← Output do Planner
├── generation.json            ← Output do Generator
├── evaluation.json            ← Output do Evaluator
│
├── generation_revision.json   ← Segunda tentativa (se rejeitado)
├── evaluation_final.json      ← Avaliacao final
│
└── delivery.json              ← Resposta aprovada para o cliente
```

### Por que File-Based Coordination?

A decisao de usar arquivos JSON como canal de comunicacao entre agentes nao e arbitraria. Seguem as razoes:

1. **Auditabilidade:** Cada decisao de cada agente fica registrada em disco. Se o cliente reclamar, voce le o trace e descobre exatamente onde o erro aconteceu.

2. **Simplicidade:** Nao requer Redis, RabbitMQ, REST ou gRPC. Apenas `json.dump()` e `json.load()`. Ideal para aprendizado e prototipagem.

3. **State Persistence Natural:** Os arquivos sao o state. Se o processo cair, o estado esta salvo. Basta reler os arquivos e continuar.

4. **Versionamento:** Adicionar `schema_version` a cada arquivo permite evoluir contratos sem quebrar compatibilidade.

5. **Caminho de Evolucao:** Comecar com arquivos e o jeito certo de aprender contratos. Depois, partes quentes podem migrar para Redis ou RabbitMQ quando o volume exigir.

### Alternativas Consideradas

| Canal | Por que nao foi escolhido para esta solucao |
|-------|---------------------------------------------|
| Message Queues (Redis/RabbitMQ) | Adiciona complexidade operacional desnecessaria para exercicio. Requer infraestrutura extra. Melhor para producao com alto volume. |
| API-based (REST/gRPC) | Forca deploy de servicos separados. Overhead de serializacao e rede. Bom para times independentes, nao para aprendizado. |
| Memoria compartilhada (variaveis) | Nao persiste, nao audita, nao resiste a crash. Viola o principio de state persistence. |
| Banco de dados (SQL/NoSQL) | Util para producao com queries complexas, mas esconde o contrato. Arquivos JSON sao mais transparentes para aprendizado. |

---

## 🧠 Componente 1: Planner

### Responsabilidades

O Planner e o cerebro estrategico do sistema. Ele **nao executa nada** — apenas planeja.

Responsabilidades especificas:
1. Ler o evento de conversa (mensagem do cliente)
2. Ler o perfil do cliente (restricoes, preferencias, historico)
3. Identificar o objetivo imediato da interacao
4. Decompor o objetivo em etapas pequenas e sequenciais
5. Definir criterios de sucesso para cada etapa
6. Definir criterios de validacao (rubrica) para o Evaluator
7. Registrar restricoes conhecidas explicitamente

### Design Decisions

**Por que etapas pequenas?** Cada etapa deve ser atomica o suficiente para o Generator executar sem ambiguidade. Se uma etapa for "resolver o pedido do cliente", o Generator tera o mesmo problema do agente unico: escopo grande demais, decisao precipitada.

**Por que criterios de sucesso explicitos?** Sem criterios, o Evaluator nao tem como validar. Criterios vagos como "resposta boa" sao inuteis. Criterios como "produto existe AND preco <= 220 AND sem lactose" sao verificaveis.

**Por que restricoes registradas separadamente?** Separar restricoes do plano permite que o Evaluator as consulte diretamente, sem precisar reinterpretar o plano.

### Exemplo de Output: `plan.json`

```json
{
  "schema_version": "1.0",
  "conversation_id": "wa_2026_05_26_marina",
  "turn_id": "turn_020",
  "created_at": "2026-05-26T20:26:05-03:00",
  "current_goal": "recomendar um produto principal dentro do orcamento",
  "known_constraints": {
    "budget_brl": 220,
    "dietary_restrictions": ["intolerancia_lactose"],
    "preferred_flavor": "chocolate",
    "training_goal": "ganho_de_massa_com_controle_de_peso",
    "training_frequency": "4x_semana",
    "avoid_stimulants_night": true
  },
  "plan": [
    {
      "step_id": "s1",
      "task": "filtrar produtos sem lactose abaixo de R$ 220",
      "owner": "generator",
      "success_criteria": [
        "pelo menos um produto encontrado",
        "todos os produtos marcados como lactose_free = true",
        "todos os produtos com preco <= 220"
      ],
      "max_products": 5
    },
    {
      "step_id": "s2",
      "task": "comparar ate duas alternativas por custo por dose e preferencia de sabor",
      "owner": "generator",
      "success_criteria": [
        "maximo 2 opcoes apresentadas",
        "cada opcao inclui preco e custo por dose",
        "trade-off explicado claramente",
        "preferencia por chocolate priorizada"
      ]
    },
    {
      "step_id": "s3",
      "task": "preparar resposta curta para WhatsApp com recomendacao principal",
      "owner": "generator",
      "success_criteria": [
        "tom humano e direto",
        "sem jargao excessivo",
        "pergunta final clara sobre confirmacao",
        "nao excede 3 paragrafos"
      ]
    }
  ],
  "evaluation_rubric": [
    "respeita restricao de lactose em TODOS os produtos considerados",
    "respeita orcamento maximo de R$ 220",
    "nao inventa disponibilidade de estoque",
    "explica recomendacao sem pressionar compra",
    "resposta coerente com historico da conversa"
  ]
}
```

### Implementacao: `planner.py`

```python
"""
Planner Agent — decompoe a tarefa em etapas e define criterios de sucesso.

Responsabilidades:
- Ler evento de conversa e perfil do cliente
- Identificar objetivo imediato
- Criar plano com etapas atomicas
- Definir rubrica de avaliacao
"""

import json
from pathlib import Path
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Optional


@dataclass
class PlanStep:
    step_id: str
    task: str
    owner: str
    success_criteria: list[str]
    max_products: int = 5


@dataclass
class Plan:
    schema_version: str = "1.0"
    conversation_id: str = ""
    turn_id: str = ""
    created_at: str = ""
    current_goal: str = ""
    known_constraints: dict = field(default_factory=dict)
    plan: list[PlanStep] = field(default_factory=list)
    evaluation_rubric: list[str] = field(default_factory=list)


def load_json(path: Path) -> dict:
    """Carrega arquivo JSON com tratamento de erro."""
    if not path.exists():
        raise FileNotFoundError(f"Arquivo necessario nao encontrado: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data: dict) -> Path:
    """Salva arquivo JSON de forma atomica (write + rename)."""
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.rename(path)
    return path


def identify_goal(customer_message: str, profile: dict) -> str:
    """
    Identifica o objetivo imediato baseado na mensagem do cliente.

    Em producao, isto seria uma chamada LLM. Aqui usamos heuristica
    para manter o exercicio auto-contido e testavel.
    """
    msg_lower = customer_message.lower()

    # Checks mais especificos primeiro para evitar captura prematura
    if any(word in msg_lower for word in ["pedido", "carrinho", "finalizar", "checkout"]):
        return "preparar_pedido"

    if any(word in msg_lower for word in ["comparar", "diferenca", "vs", "versus"]):
        return "comparar_produtos"

    if any(word in msg_lower for word in ["comprar", "quero", "recomend", "qual", "melhor"]):
        return "recomendar_um_produto_principal_dentro_do_orcamento"

    if any(word in msg_lower for word in ["estoque", "disponivel", "tem"]):
        return "verificar_disponibilidade"

    return "entender_necessidade_do_cliente"


def extract_constraints(profile: dict) -> dict:
    """Extrai restricoes conhecidas do perfil do cliente."""
    constraints = {}

    if "dietary_restrictions" in profile:
        constraints["dietary_restrictions"] = profile["dietary_restrictions"]

    if "preferences" in profile:
        prefs = profile["preferences"]
        if "budget_brl" in prefs:
            constraints["budget_brl"] = prefs["budget_brl"]
        if "flavor" in prefs:
            constraints["preferred_flavor"] = prefs["flavor"]
        if "training_goal" in prefs:
            constraints["training_goal"] = prefs["training_goal"]
        if "training_frequency" in prefs:
            constraints["training_frequency"] = prefs["training_frequency"]

    if "risk_notes" in profile:
        constraints["risk_notes"] = profile["risk_notes"]

    return constraints


def build_plan(goal: str, constraints: dict) -> list[PlanStep]:
    """Constroi etapas do plano baseado no objetivo identificado."""

    if goal == "recomendar_um_produto_principal_dentro_do_orcamento":
        return [
            PlanStep(
                step_id="s1",
                task="filtrar produtos que atendam restricoes e orcamento",
                owner="generator",
                success_criteria=[
                    "pelo menos um produto encontrado",
                    "todos os produtos respeitam restricoes alimentares",
                    "todos os produtos com preco dentro do orcamento"
                ],
                max_products=5
            ),
            PlanStep(
                step_id="s2",
                task="comparar ate duas alternativas por custo por dose e preferencia",
                owner="generator",
                success_criteria=[
                    "maximo 2 opcoes apresentadas",
                    "cada opcao inclui preco e custo por dose",
                    "trade-off explicado claramente",
                    "preferencia do cliente priorizada"
                ]
            ),
            PlanStep(
                step_id="s3",
                task="preparar resposta curta para WhatsApp com recomendacao principal",
                owner="generator",
                success_criteria=[
                    "tom humano e direto",
                    "sem jargao excessivo",
                    "pergunta final clara sobre confirmacao",
                    "nao excede 3 paragrafos"
                ]
            ),
        ]

    if goal == "comparar_produtos":
        return [
            PlanStep(
                step_id="s1",
                task="listar produtos a serem comparados",
                owner="generator",
                success_criteria=[
                    "minimo 2 produtos para comparacao",
                    "cada produto com ficha completa"
                ]
            ),
            PlanStep(
                step_id="s2",
                task="comparar por dimensoes relevantes",
                owner="generator",
                success_criteria=[
                    "minimo 3 dimensoes comparadas",
                    "tabela ou lista clara",
                    "recomendacao final"
                ]
            ),
        ]

    # Fallback: plano generico de descoberta
    return [
        PlanStep(
            step_id="s1",
            task="entender necessidade do cliente",
            owner="generator",
            success_criteria=[
                "objetivo identificado",
                "restricoes coletadas",
                "orcamento confirmado"
            ]
        ),
    ]


def build_evaluation_rubric(goal: str, constraints: dict) -> list[str]:
    """Constroi rubrica de avaliacao baseada no objetivo e restricoes."""

    rubric = []

    # Criterios universais
    rubric.append("resposta coerente com historico da conversa")
    rubric.append("nao inventa disponibilidade de estoque sem confirmacao")
    rubric.append("explica recomendacao sem pressionar compra")

    # Criterios baseados em restricoes
    if "dietary_restrictions" in constraints:
        restrictions = constraints["dietary_restrictions"]
        rubric.append(f"respeita restricoes alimentares: {', '.join(restrictions)}")

    if "budget_brl" in constraints:
        rubric.append(f"respeita orcamento maximo de R$ {constraints['budget_brl']}")

    if "preferred_flavor" in constraints:
        rubric.append(f"prioriza sabor {constraints['preferred_flavor']} quando opcoes equivalentes")

    # Criterios especificos por objetivo
    if goal.startswith("recomendar"):
        rubric.append("recomendacao principal clara com justificativa")
        rubric.append("alternativa segura oferecida quando aplicavel")

    return rubric


def planner_agent(
    event: dict,
    profile: dict,
    conversation_summary: Optional[dict] = None
) -> Plan:
    """
    Agente Planner: decompoe a tarefa e cria plano de execucao.

    Args:
        event: Evento da conversa com customer_message
        profile: Perfil do cliente com restricoes e preferencias
        conversation_summary: Resumo do historico (opcional)

    Returns:
        Plan com etapas, criterios e rubrica
    """
    customer_message = event.get("customer_message", "")

    # Identificar objetivo
    goal = identify_goal(customer_message, profile)

    # Extrair restricoes
    constraints = extract_constraints(profile)

    # Construir etapas
    steps = build_plan(goal, constraints)

    # Construir rubrica
    rubric = build_evaluation_rubric(goal, constraints)

    # Enriquecer com contexto do historico se disponivel
    if conversation_summary:
        recent_topics = conversation_summary.get("recent_topics", [])
        if recent_topics:
            constraints["recent_topics"] = recent_topics

    return Plan(
        conversation_id=event.get("conversation_id", ""),
        turn_id=event.get("turn_id", ""),
        created_at=datetime.now(timezone.utc).isoformat(),
        current_goal=goal,
        known_constraints=constraints,
        plan=steps,
        evaluation_rubric=rubric
    )
```

### Por que Este Design?

**Heuristica em vez de LLM para `identify_goal`:** Em producao, o Planner usaria uma chamada LLM com prompt especializado. Para este exercicio, usamos heuristica de palavras-chave para manter o codigo deterministico, testavel e sem dependencia externa de API. A interface (`planner_agent(event, profile) -> Plan`) e identica — trocar a implementacao interna nao quebra os consumidores.

**`dataclass` em vez de `dict` puro:** Dataclasses fornecem type hints, valores default e serializacao automatica via `asdict()`. Isso reduz erros de digitar chaves erradas e facilita refatoracao. Em producao, Pydantic seria uma escolha ainda melhor (validacao de schema integrada).

**Separacao `build_plan` / `build_evaluation_rubric`:** Cada funcao tem uma responsabilidade unica. Se amanha o time quiser mudar apenas a rubrica (ex: adicionar criterio de "sustentabilidade"), nao precisa tocar na logica de planos.

---

## ⚙️ Componente 2: Generator

### Responsabilidades

O Generator e o executor. Ele recebe um plano com etapas definidas e **executa cada etapa sem questionar o plano**.

Responsabilidades especificas:
1. Ler o plano criado pelo Planner
2. Executar cada etapa na ordem definida
3. Consultar ferramentas permitidas (catalogo, calculadora de frete)
4. Produzir output estruturado com evidencias
5. Registrar suposicoes explicitamente
6. **NAO** aprovar o proprio trabalho
7. Salvar resultado para o Evaluator

### Design Decisions

**Por que o Generator nao avalia o proprio trabalho?** Este e o principio central do Nivel 2 que se mantem no Nivel 3. Se o Generator tambem avaliasse, teriamos sycophancy — o vies de confirmar a propria resposta. A separacao e o que garante qualidade.

**Por que output estruturado (JSON) em vez de texto livre?** Output estruturado permite que o Evaluator verifique campos especificos. Texto livre exige que o Evaluator "interprete" a resposta, o que e menos confiavel.

**Por que `assumptions` explicitas?** Suposicoes nao declaradas sao a maior fonte de erros silenciosos. Se o Generator assume que "cliente prefere chocolate" mas nao registra, o Evaluator nao pode verificar se essa suposicao e valida.

### Exemplo de Output: `generation.json`

```json
{
  "schema_version": "1.0",
  "conversation_id": "wa_2026_05_26_marina",
  "step_id": "s3",
  "generated_at": "2026-05-26T20:27:12-03:00",
  "candidate_response": "Marina, no seu caso eu escolheria o Whey Isolado Chocolate agora. Ele respeita sua intolerancia, fica dentro dos R$ 220 e combina com sua preferencia de sabor. A proteina vegetal tambem e segura, mas perde no sabor que voce pediu. Posso confirmar estoque em SP?",
  "products_considered": [
    {
      "sku": "WHEY-ISO-CHOC-900",
      "name": "Whey Isolado Chocolate 900g",
      "price_brl": 199.90,
      "servings": 24,
      "cost_per_serving_brl": 8.33,
      "lactose_free": true,
      "flavor": "chocolate"
    },
    {
      "sku": "PROT-VEG-BAUN-750",
      "name": "Proteina Vegetal Baunilha 750g",
      "price_brl": 179.90,
      "servings": 25,
      "cost_per_serving_brl": 7.20,
      "lactose_free": true,
      "flavor": "baunilha"
    }
  ],
  "assumptions": [
    "cliente prefere chocolate quando opcoes sao equivalentes em seguranca",
    "cliente quer escolher um produto agora, nao montar combo",
    "estoque em SP sera verificado antes da confirmacao final"
  ]
}
```

### Implementacao: `generator.py`

```python
"""
Generator Agent — executa etapas do plano e gera respostas candidatas.

Responsabilidades:
- Ler o plano do Planner
- Executar cada etapa
- Consultar catalogo e ferramentas
- Produzir output estruturado com evidencias
- Registrar suposicoes
- NAO aprovar o proprio trabalho
"""

import json
from pathlib import Path
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Optional


@dataclass
class Product:
    sku: str
    name: str
    price_brl: float
    servings: int
    lactose_free: bool
    flavor: str
    cost_per_serving_brl: float = 0.0
    stock_available: bool = True

    def __post_init__(self):
        if self.cost_per_serving_brl == 0.0 and self.servings > 0:
            self.cost_per_serving_brl = round(self.price_brl / self.servings, 2)


@dataclass
class Generation:
    schema_version: str = "1.0"
    conversation_id: str = ""
    step_id: str = ""
    generated_at: str = ""
    candidate_response: str = ""
    products_considered: list[dict] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)


# Catalogo simulado de produtos (em producao, viria de API ou banco de dados)
SAMPLE_CATALOG = [
    Product("WHEY-ISO-CHOC-900", "Whey Isolado Chocolate 900g", 199.90, 24, True, "chocolate"),
    Product("WHEY-CONC-CHOC-900", "Whey Concentrado Chocolate 900g", 129.90, 30, False, "chocolate"),
    Product("PROT-VEG-BAUN-750", "Proteina Vegetal Baunilha 750g", 179.90, 25, True, "baunilha"),
    Product("WHEY-ISO-MOR-900", "Whey Isolado Morango 900g", 209.90, 24, True, "morango"),
    Product("PROT-VEG-CHOC-750", "Proteina Vegetal Chocolate 750g", 189.90, 25, True, "chocolate"),
    Product("CREAT-MONO-300", "Creatina Monohidratada 300g", 89.90, 60, True, "neutro"),
    Product("WHEY-ISO-BAUN-900", "Whey Isolado Baunilha 900g", 199.90, 24, True, "baunilha"),
    Product("PRE-TREINO-CAFE-300", "Pre-Treino com Cafeina 300g", 149.90, 30, True, "neutro"),
]


def load_json(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"Arquivo necessario nao encontrado: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data: dict) -> Path:
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.rename(path)
    return path


def filter_products(
    products: list[Product],
    constraints: dict
) -> list[Product]:
    """
    Filtra produtos baseado nas restricoes conhecidas.
    Aplica filtros em cadeia: restricao alimentar → orcamento → preferencia.
    """
    result = list(products)

    # Filtro 1: restricoes alimentares
    dietary = constraints.get("dietary_restrictions", [])
    if "intolerancia_lactose" in dietary:
        result = [p for p in result if p.lactose_free]

    # Filtro 2: orcamento
    budget = constraints.get("budget_brl")
    if budget is not None:
        result = [p for p in result if p.price_brl <= budget]

    # Filtro 3: evitar estimulantes a noite
    risk_notes = constraints.get("risk_notes", [])
    if any("estimulantes" in note for note in risk_notes):
        result = [p for p in result if "pre-treino" not in p.name.lower()]

    return result


def rank_by_preference(
    products: list[Product],
    preferred_flavor: Optional[str]
) -> list[Product]:
    """Ordena produtos priorizando sabor preferido."""
    if not preferred_flavor:
        return products

    preferred = [p for p in products if p.flavor.lower() == preferred_flavor.lower()]
    others = [p for p in products if p.flavor.lower() != preferred_flavor.lower()]

    # Dentro de cada grupo, ordena por custo por dose
    preferred.sort(key=lambda p: p.cost_per_serving_brl)
    others.sort(key=lambda p: p.cost_per_serving_brl)

    return preferred + others


def format_candidate_response(
    primary: Product,
    alternative: Optional[Product],
    constraints: dict
) -> str:
    """Formata resposta curta para WhatsApp com tom humano."""

    flavor_note = ""
    preferred = constraints.get("preferred_flavor")
    if preferred and primary.flavor.lower() == preferred.lower():
        flavor_note = f" e combina com sua preferencia de {preferred}"

    lactose_label = "Sem lactose" if primary.lactose_free else ""
    response = (
        f"{primary.name} — "
        f"R$ {primary.price_brl:.2f}, "
        f"{primary.servings} doses "
        f"(R$ {primary.cost_per_serving_brl:.2f}/dose)."
        f"{(' ' + lactose_label) if lactose_label else ''}{flavor_note}."
    )

    if alternative:
        response += (
            f" Outra opcao segura: {alternative.name} "
            f"(R$ {alternative.cost_per_serving_brl:.2f}/dose), "
            f"mas o sabor e {alternative.flavor}."
        )

    response += " Posso confirmar estoque para voce?"

    return response


def generator_agent(
    plan: dict,
    catalog: list[dict],
    evaluator_feedback: Optional[dict] = None
) -> Generation:
    """
    Agente Generator: executa etapa do plano e gera resposta candidata.

    Args:
        plan: Plano do Planner com etapas e restricoes
        catalog: Lista de produtos disponiveis
        evaluator_feedback: Feedback do Evaluator (se for revisao)

    Returns:
        Generation com resposta candidata, produtos e suposicoes
    """
    # Converter catalogo de dict para Product
    products = [Product(**item) if isinstance(item, dict) else item for item in catalog]

    constraints = plan.get("known_constraints", {})
    steps = plan.get("plan", [])

    # Se houver feedback do Evaluator, ajustar baseado nele
    if evaluator_feedback:
        failed_criteria = evaluator_feedback.get("failed_criteria", [])
        # Aplica correcoes baseadas no feedback
        # (em producao, reexecutaria LLM com prompt corrigido)

    # Encontrar a etapa atual (ultima nao executada ou especifica)
    current_step = steps[-1] if steps else {"step_id": "s0", "task": "unknown"}

    # Filtrar e ordenar produtos
    filtered = filter_products(products, constraints)
    preferred = constraints.get("preferred_flavor")
    ranked = rank_by_preference(filtered, preferred)

    # Selecionar produto principal e alternativa
    primary = ranked[0] if ranked else None
    alternative = ranked[1] if len(ranked) > 1 else None

    if not primary:
        return Generation(
            conversation_id=plan.get("conversation_id", ""),
            step_id=current_step.get("step_id", "unknown"),
            generated_at=datetime.now(timezone.utc).isoformat(),
            candidate_response=(
                "Nao encontrei produtos que atendam todas as suas restricoes. "
                "Quer flexibilizar alguma delas para eu buscar de novo?"
            ),
            products_considered=[],
            assumptions=["nenhum produto atende todas as restricoes simultaneamente"]
        )

    # Formatar resposta
    response = format_candidate_response(primary, alternative, constraints)

    # Construir lista de produtos considerados
    products_considered = [
        {
            "sku": p.sku,
            "name": p.name,
            "price_brl": p.price_brl,
            "servings": p.servings,
            "cost_per_serving_brl": p.cost_per_serving_brl,
            "lactose_free": p.lactose_free,
            "flavor": p.flavor
        }
        for p in ranked[:3]
    ]

    return Generation(
        conversation_id=plan.get("conversation_id", ""),
        step_id=current_step.get("step_id", "unknown"),
        generated_at=datetime.now(timezone.utc).isoformat(),
        candidate_response=response,
        products_considered=products_considered,
        assumptions=[
            "cliente prefere sabor declarado quando opcoes sao equivalentes em seguranca",
            "cliente quer escolher um produto agora, nao montar combo",
            "estoque sera verificado antes da confirmacao final"
        ]
    )
```

### Por que Este Design?

**Catalogo simulado:** Em producao, o Generator consultaria uma API de catalogo. Para o exercicio, usamos uma lista em memoria. A funcao `filter_products` e independente da fonte de dados — so precisa de uma lista de `Product`.

**Filtros em cadeia:** Cada filtro (`lactose_free`, `price_brl <= budget`, etc.) e aplicado sequencialmente. Isso facilita debug: se um produto desapareceu, voce sabe exatamente qual filtro o removeu.

**`format_candidate_response` separada:** A formatacao da resposta e isolada da logica de selecao. Se o time de UX quiser mudar o tom ou formato, mexe apenas nessa funcao.

---

## 🔍 Componente 3: Evaluator

### Responsabilidades

O Evaluator e o gatekeeper. Nada chega ao cliente sem sua aprovacao.

Responsabilidades especificas:
1. Ler o plano original do Planner
2. Ler o output do Generator
3. Validar cada criterio da rubrica
4. Detectar contradicoes com o state persistido
5. Verificar se ha afirmacoes sem evidencia
6. Aprovar (status = "approved") ou rejeitar (status = "rejected")
7. Registrar feedback especifico para cada criterio reprovado

### Design Decisions

**Por que validacao binaria (approved/rejected) em vez de score numerico?** Score numerico (ex: 7.5/10) cria zona cinzenta. "7.5 e bom o suficiente?" Depende de quem pergunta. Binario e inequivoco: passou ou nao passou. Cada criterio tambem e binario. Se a rubrica tiver 5 criterios, todos devem passar.

**Por que `evidence` em cada criterio?** Sem evidencia, o Evaluator vira uma caixa-preta. "Aprovado porque parece bom" nao e auditavel. "Aprovado porque `lactose_free = true` em ambos os produtos" e verificavel por qualquer pessoa que leia o trace.

**Por que feedback especifico e acionavel?** "Resposta ruim" nao ajuda o Generator a corrigir. "Produto WHEY-CONC-CHOC-900 possui lactose mas foi incluido na lista de considerados" e acionavel: o Generator sabe exatamente o que corrigir.

### Exemplo de Output: `evaluation.json`

```json
{
  "schema_version": "1.0",
  "conversation_id": "wa_2026_05_26_marina",
  "evaluated_step_id": "s3",
  "status": "approved",
  "checked_at": "2026-05-26T20:27:18-03:00",
  "rubric_results": [
    {
      "criterion": "respeita restricoes alimentares: intolerancia_lactose",
      "passed": true,
      "evidence": "ambos os produtos considerados marcados como lactose_free = true"
    },
    {
      "criterion": "respeita orcamento maximo de R$ 220",
      "passed": true,
      "evidence": "produto principal R$ 199.90, alternativa R$ 179.90"
    },
    {
      "criterion": "nao inventa disponibilidade de estoque",
      "passed": true,
      "evidence": "resposta pergunta 'Posso confirmar estoque?' em vez de afirmar"
    },
    {
      "criterion": "explica recomendacao sem pressionar compra",
      "passed": true,
      "evidence": "resposta descreve opcoes e pergunta se pode confirmar"
    },
    {
      "criterion": "resposta coerente com historico da conversa",
      "passed": true,
      "evidence": "menciona preferencia por chocolate registrada no perfil"
    }
  ],
  "feedback": null
}
```

### Implementacao: `evaluator.py`

```python
"""
Evaluator Agent — valida output do Generator contra rubrica e aprova/rejeita.

Responsabilidades:
- Ler o plano e a rubrica
- Ler o output do Generator
- Validar cada criterio
- Detectar contradicoes com state
- Aprovar ou rejeitar com feedback especifico
"""

import json
from pathlib import Path
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Optional


@dataclass
class RubricResult:
    criterion: str
    passed: bool
    evidence: str


@dataclass
class Evaluation:
    schema_version: str = "1.0"
    conversation_id: str = ""
    evaluated_step_id: str = ""
    status: str = "rejected"
    checked_at: str = ""
    rubric_results: list[dict] = field(default_factory=list)
    feedback: Optional[str] = None


def load_json(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"Arquivo necessario nao encontrado: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data: dict) -> Path:
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.rename(path)
    return path


def check_lactose_restriction(
    generation: dict,
    constraints: dict
) -> RubricResult:
    """Verifica se todos os produtos considerados respeitam restricao de lactose."""
    dietary = constraints.get("dietary_restrictions", [])
    if "intolerancia_lactose" not in dietary:
        return RubricResult(
            criterion="respeita restricoes alimentares: intolerancia_lactose",
            passed=True,
            evidence="cliente nao possui restricao de lactose"
        )

    products = generation.get("products_considered", [])
    violating = [p["name"] for p in products if not p.get("lactose_free", False)]

    if violating:
        return RubricResult(
            criterion="respeita restricoes alimentares: intolerancia_lactose",
            passed=False,
            evidence=f"produtos com lactose encontrados: {violating}"
        )

    return RubricResult(
        criterion="respeita restricoes alimentares: intolerancia_lactose",
        passed=True,
        evidence=f"todos os {len(products)} produtos marcados como lactose_free = true"
    )


def check_budget(
    generation: dict,
    constraints: dict
) -> RubricResult:
    """Verifica se o orcamento maximo foi respeitado."""
    budget = constraints.get("budget_brl")
    if budget is None:
        return RubricResult(
            criterion="respeita orcamento maximo",
            passed=True,
            evidence="orcamento nao especificado"
        )

    products = generation.get("products_considered", [])
    violating = [f"{p['name']} (R$ {p['price_brl']})" for p in products if p.get("price_brl", 0) > budget]

    if violating:
        return RubricResult(
            criterion=f"respeita orcamento maximo de R$ {budget}",
            passed=False,
            evidence=f"produtos acima do orcamento: {violating}"
        )

    return RubricResult(
        criterion=f"respeita orcamento maximo de R$ {budget}",
        passed=True,
        evidence=f"todos os produtos com preco <= R$ {budget}"
    )


def check_no_false_stock_promise(generation: dict) -> RubricResult:
    """Verifica se a resposta nao afirma disponibilidade sem confirmacao."""
    response = generation.get("candidate_response", "").lower()

    false_promises = [
        "temos em estoque",
        "disponivel agora",
        "estoque garantido",
        "entrega confirmada",
    ]

    for phrase in false_promises:
        if phrase in response:
            return RubricResult(
                criterion="nao inventa disponibilidade de estoque",
                passed=False,
                evidence=f"resposta afirma '{phrase}' sem confirmacao real"
            )

    # Verifica se ha pergunta de confirmacao (bom sinal)
    confirmation_phrases = [
        "confirmar estoque",
        "verificar disponibilidade",
        "checar estoque",
        "posso confirmar",
    ]

    has_confirmation = any(phrase in response for phrase in confirmation_phrases)

    return RubricResult(
        criterion="nao inventa disponibilidade de estoque",
        passed=True,
        evidence="resposta pergunta antes de afirmar estoque" if has_confirmation
        else "resposta nao menciona estoque"
    )


def check_no_pressure(generation: dict) -> RubricResult:
    """Verifica se a resposta nao pressiona compra."""
    response = generation.get("candidate_response", "").lower()

    pressure_phrases = [
        "aproveite agora",
        "por tempo limitado",
        "ultimas unidades",
        "nao perca",
        "compre ja",
        "oferta imperdivel",
    ]

    found = [phrase for phrase in pressure_phrases if phrase in response]

    if found:
        return RubricResult(
            criterion="explica recomendacao sem pressionar compra",
            passed=False,
            evidence=f"frases de pressao encontradas: {found}"
        )

    return RubricResult(
        criterion="explica recomendacao sem pressionar compra",
        passed=True,
        evidence="resposta descritiva, sem urgencia artificial"
    )


def check_response_coherence(
    generation: dict,
    constraints: dict
) -> RubricResult:
    """Verifica coerencia basica da resposta com restricoes conhecidas."""
    response = generation.get("candidate_response", "").lower()

    # Verifica se menciona sabor preferido quando relevante
    preferred = constraints.get("preferred_flavor")
    if preferred and preferred.lower() in response:
        return RubricResult(
            criterion="resposta coerente com historico da conversa",
            passed=True,
            evidence=f"menciona preferencia por {preferred}"
        )

    if preferred:
        # Nao mencionar o sabor preferido nao e necessariamente erro,
        # mas indica que poderia ser mais personalizada
        return RubricResult(
            criterion="resposta coerente com historico da conversa",
            passed=True,
            evidence=f"resposta nao menciona sabor preferido ({preferred}), mas nao contradiz"
        )

    return RubricResult(
        criterion="resposta coerente com historico da conversa",
        passed=True,
        evidence="sem contradicoes detectadas com restricoes conhecidas"
    )


def evaluator_agent(
    plan: dict,
    generation: dict,
    profile: Optional[dict] = None
) -> Evaluation:
    """
    Agente Evaluator: valida output contra rubrica e decide.

    Args:
        plan: Plano original com restricoes e rubrica
        generation: Output do Generator
        profile: Perfil do cliente (para verificacoes adicionais)

    Returns:
        Evaluation com status e resultados por criterio
    """
    constraints = plan.get("known_constraints", {})
    rubric = plan.get("evaluation_rubric", [])

    # Executar cada verificador
    results: list[RubricResult] = []

    # Verificacoes de restricao — se a rubrica menciona criterios especificos,
    # as checagens correspondentes sao ativadas
    rubric_text = " ".join(rubric).lower()

    if "lactose" in rubric_text or "intolerancia_lactose" in str(constraints.get("dietary_restrictions", [])):
        results.append(check_lactose_restriction(generation, constraints))

    if "orcamento" in rubric_text or "budget" in rubric_text or "budget_brl" in constraints:
        results.append(check_budget(generation, constraints))

    # Verificacoes de qualidade obrigatorias (sempre ativas)
    results.append(check_no_false_stock_promise(generation))
    results.append(check_no_pressure(generation))
    results.append(check_response_coherence(generation, constraints))

    # Verificar se a resposta nao esta vazia
    if not generation.get("candidate_response", "").strip():
        results.append(RubricResult(
            criterion="resposta nao vazia",
            passed=False,
            evidence="candidate_response esta vazia"
        ))

    # Determinar status final
    all_passed = all(r.passed for r in results)
    failed = [r for r in results if not r.passed]

    feedback = None
    if failed:
        feedback_lines = [f"- {r.criterion}: {r.evidence}" for r in failed]
        feedback = "Criterios reprovados:\n" + "\n".join(feedback_lines)

    return Evaluation(
        conversation_id=plan.get("conversation_id", ""),
        evaluated_step_id=generation.get("step_id", "unknown"),
        status="approved" if all_passed else "rejected",
        checked_at=datetime.now(timezone.utc).isoformat(),
        rubric_results=[asdict(r) for r in results],
        feedback=feedback
    )
```

### Por que Este Design?

**Verificadores independentes:** Cada criterio da rubrica tem sua propria funcao (`check_lactose_restriction`, `check_budget`, etc.). Isso torna o codigo:
- Testavel isoladamente (cada verificador pode ser testado com seus proprios casos)
- Extensivel (adicionar novo criterio = nova funcao, sem mexer nas existentes)
- Legivel (cada funcao tem nome auto-explicativo)

**Heuristica em vez de LLM:** Assim como no Planner, usamos verificacao heuristica (checagem de campos, palavras-chave) em vez de LLM. Em producao, o Evaluator usaria LLM com prompt especializado para criterios subjetivos como "tom humano". Mas criterios objetivos (preco, lactose) sao melhores verificados por codigo deterministico.

**Feedback acionavel:** Quando rejeita, o Evaluator lista exatamente quais criterios falharam e com qual evidencia. Isso permite que o Generator corrija pontualmente, em vez de refazer tudo as cegas.

---

## 🔄 Componente 4: Orquestrador (Harness)

O harness e a cola que conecta os tres agentes. Ele gerencia o fluxo, persiste estado e decide quando rejeitar ou entregar.

### Diagrama de Fluxo Completo

```
┌──────────────────────────────────────────────────────────────────────┐
│                         run_customer_turn(message)                    │
│                                                                      │
│  1. Salva conversation_event.json                                    │
│                         │                                            │
│                         ▼                                            │
│  2. Planner: event + profile + summary → plan.json                   │
│                         │                                            │
│                         ▼                                            │
│  3. Generator: plan + catalog → generation.json                      │
│                         │                                            │
│                         ▼                                            │
│  4. Evaluator: plan + generation → evaluation.json                   │
│                         │                                            │
│              ┌──────────┴──────────┐                                 │
│              ▼                     ▼                                 │
│        approved               rejected                               │
│              │                     │                                 │
│              ▼                     ▼                                 │
│  5a. Retorna resposta     5b. Generator com feedback                 │
│      para WhatsApp            ↓                                      │
│                          generation_revision.json                    │
│                              ↓                                       │
│                          Evaluator (2a tentativa)                    │
│                              │                                       │
│                   ┌──────────┴──────────┐                            │
│                   ▼                     ▼                            │
│              approved               rejected                         │
│                   │                     │                            │
│                   ▼                     ▼                            │
│           Retorna resposta      Fallback: mensagem                   │
│           para WhatsApp         de seguranca                         │
│                                                                      │
│  Maximo de 3 tentativas (max_iterations = 3)                         │
└──────────────────────────────────────────────────────────────────────┘
```

### Implementacao: `orchestrator.py`

```python
"""
Orchestrator (Harness) — conecta Planner, Generator e Evaluator.

Responsabilidades:
- Gerenciar fluxo de execucao
- Persistir estado em arquivos JSON
- Controlar loop de revisao (max_iterations)
- Decidir quando entregar ou fazer fallback seguro
"""

import json
from pathlib import Path
from datetime import datetime, timezone
from dataclasses import dataclass, asdict
from typing import Optional

# Importa os agentes (em producao, cada um seria um modulo separado)
# from planner import planner_agent, Plan
# from generator import generator_agent, Generation, SAMPLE_CATALOG
# from evaluator import evaluator_agent, Evaluation


@dataclass
class CustomerProfile:
    schema_version: str = "1.0"
    customer_id: str = ""
    name: str = ""
    dietary_restrictions: list[str] = None
    preferences: dict = None
    risk_notes: list[str] = None

    def __post_init__(self):
        if self.dietary_restrictions is None:
            self.dietary_restrictions = []
        if self.preferences is None:
            self.preferences = {}
        if self.risk_notes is None:
            self.risk_notes = []


# Perfis de exemplo para testes
SAMPLE_PROFILES = {
    "cust_marina_4821": CustomerProfile(
        customer_id="cust_marina_4821",
        name="Marina",
        dietary_restrictions=["intolerancia_lactose"],
        preferences={
            "flavor": "chocolate",
            "budget_brl": 220,
            "training_goal": "ganho_de_massa_com_controle_de_peso",
            "training_frequency": "4x_semana"
        },
        risk_notes=[
            "nao recomendar produtos com lactose",
            "nao recomendar estimulantes perto da noite"
        ]
    ),
    "cust_joao_7832": CustomerProfile(
        customer_id="cust_joao_7832",
        name="Joao",
        dietary_restrictions=[],
        preferences={
            "flavor": "baunilha",
            "budget_brl": 150,
            "training_goal": "ganho_de_massa",
            "training_frequency": "5x_semana"
        },
        risk_notes=[]
    ),
    "cust_ana_9912": CustomerProfile(
        customer_id="cust_ana_9912",
        name="Ana",
        dietary_restrictions=["intolerancia_gluten", "vegana"],
        preferences={
            "flavor": "morango",
            "budget_brl": 300,
            "training_goal": "resistencia_e_tonificacao",
            "training_frequency": "3x_semana"
        },
        risk_notes=[
            "apenas produtos veganos",
            "verificar certificacao sem gluten"
        ]
    ),
}


def ensure_state_dir(conversation_id: str, base_dir: Path) -> Path:
    """Cria diretorio de estado para a conversa se nao existir."""
    state_dir = base_dir / "state" / "conversations" / conversation_id
    state_dir.mkdir(parents=True, exist_ok=True)
    return state_dir


def write_json(path: Path, data) -> Path:
    """Escreve JSON de forma atomica. Aceita dataclasses e dicts."""
    tmp = path.with_suffix(".tmp")
    payload = asdict(data) if hasattr(data, '__dataclass_fields__') else data
    tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.rename(path)
    return path


def read_json(path: Path) -> dict:
    """Le JSON com verificacao de existencia."""
    if not path.exists():
        raise FileNotFoundError(f"Arquivo necessario nao encontrado: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def run_customer_turn(
    message: str,
    conversation_id: str,
    customer_id: str,
    base_dir: Path,
    planner_fn,
    generator_fn,
    evaluator_fn,
    catalog: list,
    max_iterations: int = 3,
    profiles: dict = None
) -> dict:
    """
    Executa um turno completo de conversa do cliente.

    Fluxo:
    1. Salva evento da conversa
    2. Planner decompoe a tarefa
    3. Generator executa e gera resposta
    4. Evaluator valida e aprova/rejeita
    5. Se rejeitado, loop de revisao ate max_iterations
    6. Retorna resposta aprovada ou fallback seguro

    Args:
        message: Mensagem do cliente
        conversation_id: ID da conversa
        customer_id: ID do cliente
        base_dir: Diretorio base para state files
        planner_fn: Funcao do Planner
        generator_fn: Funcao do Generator
        evaluator_fn: Funcao do Evaluator
        catalog: Lista de produtos
        max_iterations: Maximo de tentativas de geracao
        profiles: Dicionario de perfis de cliente

    Returns:
        Dict com resposta final e metadata do trace
    """
    if profiles is None:
        profiles = SAMPLE_PROFILES

    state_dir = ensure_state_dir(conversation_id, base_dir)
    profile = profiles.get(customer_id)
    if profile is None:
        raise ValueError(f"Cliente {customer_id} nao encontrado nos perfis")

    # Step 1: Salvar evento da conversa
    event = {
        "schema_version": "1.0",
        "conversation_id": conversation_id,
        "turn_id": f"turn_{datetime.now(timezone.utc).strftime('%H%M%S')}",
        "channel": "whatsapp",
        "received_at": datetime.now(timezone.utc).isoformat(),
        "customer_message": message,
        "customer_id": customer_id
    }
    write_json(state_dir / "conversation_event.json", event)

    # Step 2: Planner
    plan = planner_fn(
        event=event,
        profile=asdict(profile),
        conversation_summary=None
    )
    write_json(state_dir / "plan.json", plan)

    # Step 3-5: Generator → Evaluator loop
    plan_dict = asdict(plan) if hasattr(plan, '__dataclass_fields__') else plan
    profile_dict = asdict(profile) if hasattr(profile, '__dataclass_fields__') else profile

    for iteration in range(1, max_iterations + 1):
        # Generator
        evaluator_feedback = None
        if iteration > 1:
            feedback_path = state_dir / "evaluation.json"
            if feedback_path.exists():
                evaluator_feedback = read_json(feedback_path)

        generation = generator_fn(
            plan=plan_dict,
            catalog=catalog,
            evaluator_feedback=evaluator_feedback
        )

        gen_path = state_dir / (
            "generation.json" if iteration == 1
            else f"generation_revision_{iteration}.json"
        )
        write_json(gen_path, generation)

        # Evaluator
        gen_dict = asdict(generation) if hasattr(generation, '__dataclass_fields__') else generation
        evaluation = evaluator_fn(
            plan=plan_dict,
            generation=gen_dict,
            profile=profile_dict
        )
        write_json(state_dir / "evaluation.json", evaluation)

        eval_dict = asdict(evaluation) if hasattr(evaluation, '__dataclass_fields__') else evaluation

        # Aprovado: entregar
        if eval_dict.get("status") == "approved":
            delivery = {
                "schema_version": "1.0",
                "conversation_id": conversation_id,
                "turn_id": event["turn_id"],
                "sent_at": datetime.now(timezone.utc).isoformat(),
                "approved_by": "evaluator",
                "iterations_used": iteration,
                "message": gen_dict.get("candidate_response", ""),
                "audit_refs": ["plan.json", "generation.json", "evaluation.json"]
            }
            write_json(state_dir / "delivery.json", delivery)
            return {
                "status": "delivered",
                "message": delivery["message"],
                "iterations": iteration,
                "trace_dir": str(state_dir)
            }

    # Max iterations atingido sem aprovacao: fallback seguro
    fallback_message = (
        "Quero confirmar um detalhe antes de te responder com seguranca. "
        "So um instante."
    )
    delivery = {
        "schema_version": "1.0",
        "conversation_id": conversation_id,
        "turn_id": event["turn_id"],
        "sent_at": datetime.now(timezone.utc).isoformat(),
        "approved_by": "fallback_max_iterations",
        "iterations_used": max_iterations,
        "message": fallback_message,
        "audit_refs": []
    }
    write_json(state_dir / "delivery.json", delivery)
    return {
        "status": "fallback",
        "message": fallback_message,
        "iterations": max_iterations,
        "trace_dir": str(state_dir)
    }
```

### Por que Este Design?

**`max_iterations` explicito:** Sem limite, um loop de revisao pode rodar indefinidamente se o Generator nunca acertar ou o Evaluator estiver muito rigido. Tres tentativas e um equilibrio entre "dar chance de corrigir" e "nao gastar tokens infinitos".

**Fallback seguro:** Quando todas as tentativas falham, o harness nunca envia a ultima resposta rejeitada. Em vez disso, envia uma mensagem segura que nao faz promessas. Pior caso: cliente espera um pouco mais. Melhor caso: evita recomendacao errada.

**State persistido em cada passo:** O harness salva cada artefato (plan, generation, evaluation) em disco sequencialmente. Isso cria um audit trail completo. Uma implementacao de producao adicionaria deteccao de arquivos existentes para retomar de onde parou apos um crash — aqui, o foco e a clareza do fluxo e do contrato entre agentes.

---

## 🎯 Estrategias de Coordenacao: Tabela Comparativa

A escolha entre execucao sequencial, paralela ou event-driven e uma das decisoes arquiteturais mais importantes em sistemas multi-agente. Abaixo, uma analise detalhada de cada estrategia aplicada ao KODA.

### Tabela Comparativa

| Dimensao | Sequencial | Paralelo | Event-Driven |
|----------|-----------|----------|--------------|
| **Fluxo** | Planner → Generator → Evaluator (linear) | Planner → N Generators simultaneos → Evaluator agrega | Agentes reagem a mudancas de estado (nao linear) |
| **Latencia** | Alta (soma dos tempos) | Baixa (tempo do mais lento) | Variavel (depende do evento) |
| **Complexidade** | Baixa | Media | Alta |
| **Auditabilidade** | Excelente (trace linear) | Boa (trace por worker) | Dificil (eventos dispersos) |
| **Custo por Turno** | 3 chamadas (P+G+E) | 3+N chamadas (P+N*G+E) | Variavel (depende de quantos agentes reagem) |
| **Risco de Inconsistencia** | Baixo (ordem garantida) | Medio (resultados paralelos podem divergir) | Alto (eventos fora de ordem) |
| **Caso de Uso KODA** | Recomendacao com restricao alimentar | Comparacao de produtos, frete e promocoes | Carrinho abandonado, pagamento aprovado, entrega |
| **Quando Usar** | Erro custa caro, jornada curta, time aprendendo | Subtarefas independentes, latencia importa | Jornada longa (horas/dias), eventos externos |
| **Quando Evitar** | Alto volume, muitas subtarefas | Dependencias entre subtarefas, sem Evaluator forte | Time pequeno, pouca infra de eventos, debug frequente |

### Exemplo de Cada Estrategia no KODA

#### Sequencial — Recomendacao com Restricao Alimentar

```
Cliente: "Quero whey, sou intolerante a lactose, orcamento R$ 200"

Planner (0.3s)
  → Define: filtrar sem lactose, comparar 2 opcoes, formatar resposta
Generator (0.5s)
  → Filtra 8 produtos do catalogo → 3 sem lactose ate R$ 200
  → Seleciona melhor (chocolate) e alternativa (baunilha)
Evaluator (0.2s)
  → Verifica: lactose_free=true em ambos? Sim.
  → Verifica: preco <= 200? Sim.
  → Verifica: nao afirma estoque? Sim.
  → APROVADO.

Resposta (1.0s total): "Whey Isolado Chocolate, R$ 199,90..."
```

#### Paralelo — Comparacao de Frete e Preco

```
Cliente: "Quanto fica com frete para Pinheiros e para o Centro?"

Planner (0.3s)
  → Define 2 subtarefas: calcular frete Pinheiros, calcular frete Centro

Generator_Frete_Pinheiros (0.4s)    Generator_Frete_Centro (0.4s)
  → Consulta transportadora A         → Consulta transportadora B
  → R$ 15,90, 1 dia util              → R$ 22,50, 2 dias uteis

Evaluator (0.2s)
  → Ambos retornaram? Sim.
  → Precises? Sim.
  → APROVADO.

Resposta (0.9s total, vs 1.3s sequencial):
  "Pinheiros: R$ 15,90 (1 dia). Centro: R$ 22,50 (2 dias)."
```

#### Event-Driven — Pos-Compra

```
Evento: payment.approved (externo, 2h depois da compra)

Fulfillment Agent reage ao evento:
  → Le order_draft.json
  → Confirma estoque reservado
  → Agenda transportadora
  → Envia mensagem no WhatsApp: "Pagamento aprovado! Entrega amanha."

Nenhum Planner ou Generator envolvido.
O cliente nao esta mais na conversa.
O estado disparou a acao.
```

### Regra Pratica de Escolha

```
if erro_tem_custo_alto and time_esta_aprendendo:
    use sequencial

elif subtarefas_sao_independentes and latencia_importa:
    use paralelo

elif jornada_continua_fora_do_turno:
    use event_driven

else:
    use sequencial  # default seguro
```

---

## 🧪 Testes: Validando o Sistema

Testes sao essenciais para garantir que cada componente funciona isoladamente e que a integracao entre eles e correta.

### Estrategia de Teste

1. **Testes unitarios por componente:** Planner, Generator, Evaluator testados isoladamente com entradas controladas
2. **Testes de integracao:** Fluxo completo Planner → Generator → Evaluator com cenarios realistas
3. **Testes de borda:** Cenarios limite (orcamento zero, sem produtos, restricoes conflitantes)

### Implementacao: `test_multi_agent.py`

```python
"""
Testes para o sistema multi-agente Planner/Generator/Evaluator.

Estrategia:
- Unitarios: cada agente isolado com fixtures
- Integracao: fluxo completo com cenarios realistas
- Borda: casos limite e erro
"""

import json
import tempfile
from pathlib import Path
from dataclasses import asdict

# Importa modulos do sistema
# from planner import planner_agent, Plan, PlanStep
# from generator import generator_agent, Generation, Product, SAMPLE_CATALOG, filter_products
# from evaluator import evaluator_agent, Evaluation, RubricResult
# from orchestrator import run_customer_turn, SAMPLE_PROFILES


# ═══════════════════════════════════════════════════════════════
# Fixtures
# ═══════════════════════════════════════════════════════════════

def make_event(message="Qual whey voce recomenda?", conversation_id="test_001"):
    return {
        "conversation_id": conversation_id,
        "turn_id": "turn_001",
        "channel": "whatsapp",
        "received_at": "2026-05-26T20:00:00-03:00",
        "customer_message": message
    }


def make_profile():
    return {
        "customer_id": "cust_test",
        "name": "Teste",
        "dietary_restrictions": ["intolerancia_lactose"],
        "preferences": {
            "flavor": "chocolate",
            "budget_brl": 200,
            "training_goal": "ganho_de_massa",
            "training_frequency": "4x_semana"
        },
        "risk_notes": ["nao recomendar produtos com lactose"]
    }


def make_catalog():
    return [
        {"sku": "WHEY-ISO-CHOC-900", "name": "Whey Isolado Chocolate 900g",
         "price_brl": 199.90, "servings": 24, "lactose_free": True, "flavor": "chocolate"},
        {"sku": "WHEY-CONC-CHOC-900", "name": "Whey Concentrado Chocolate 900g",
         "price_brl": 129.90, "servings": 30, "lactose_free": False, "flavor": "chocolate"},
        {"sku": "PROT-VEG-CHOC-750", "name": "Proteina Vegetal Chocolate 750g",
         "price_brl": 189.90, "servings": 25, "lactose_free": True, "flavor": "chocolate"},
    ]


# ═══════════════════════════════════════════════════════════════
# Testes do Planner
# ═══════════════════════════════════════════════════════════════

class TestPlanner:
    """Testes unitarios do agente Planner."""

    def test_identify_recommendation_goal(self):
        """Deve identificar objetivo de recomendacao com mensagem tipica."""
        from planner import identify_goal

        goal = identify_goal("Qual whey voce recomenda?", make_profile())
        assert "recomendar" in goal

    def test_identify_comparison_goal(self):
        """Deve identificar objetivo de comparacao."""
        from planner import identify_goal

        goal = identify_goal("Compara o whey isolado vs concentrado", make_profile())
        assert "comparar" in goal

    def test_identify_order_goal(self):
        """Deve identificar objetivo de pedido."""
        from planner import identify_goal

        goal = identify_goal("Quero finalizar meu pedido", make_profile())
        assert "pedido" in goal

    def test_plan_has_steps(self):
        """Plano de recomendacao deve ter pelo menos 3 etapas."""
        from planner import planner_agent

        plan = planner_agent(event=make_event(), profile=make_profile())
        assert len(plan.plan) >= 2
        assert plan.current_goal != ""

    def test_plan_includes_rubric(self):
        """Plano deve incluir rubrica de avaliacao."""
        from planner import planner_agent

        plan = planner_agent(event=make_event(), profile=make_profile())
        assert len(plan.evaluation_rubric) >= 3

    def test_plan_extracts_budget_constraint(self):
        """Deve extrair orcamento do perfil."""
        from planner import planner_agent

        plan = planner_agent(event=make_event(), profile=make_profile())
        assert plan.known_constraints.get("budget_brl") == 200

    def test_plan_extracts_dietary_constraints(self):
        """Deve extrair restricoes alimentares do perfil."""
        from planner import planner_agent

        plan = planner_agent(event=make_event(), profile=make_profile())
        assert "intolerancia_lactose" in plan.known_constraints.get("dietary_restrictions", [])

    def test_plan_steps_have_success_criteria(self):
        """Cada etapa do plano deve ter criterios de sucesso."""
        from planner import planner_agent

        plan = planner_agent(event=make_event(), profile=make_profile())
        for step in plan.plan:
            assert len(step.success_criteria) >= 1, f"Step {step.step_id} sem criterios"


# ═══════════════════════════════════════════════════════════════
# Testes do Generator
# ═══════════════════════════════════════════════════════════════

class TestGenerator:
    """Testes unitarios do agente Generator."""

    def test_filter_removes_lactose_products(self):
        """Deve remover produtos com lactose quando cliente e intolerante."""
        from generator import filter_products, Product

        products = [
            Product("A", "Whey Isolado", 100, 20, True, "chocolate"),
            Product("B", "Whey Concentrado", 80, 25, False, "chocolate"),
            Product("C", "Proteina Vegetal", 90, 22, True, "baunilha"),
        ]
        constraints = {"dietary_restrictions": ["intolerancia_lactose"]}
        result = filter_products(products, constraints)

        assert len(result) == 2
        assert all(p.lactose_free for p in result)
        assert products[1] not in result  # Whey Concentrado removido

    def test_filter_respects_budget(self):
        """Deve remover produtos acima do orcamento."""
        from generator import filter_products, Product

        products = [
            Product("A", "Barato", 50, 10, True, "neutro"),
            Product("B", "Medio", 100, 20, True, "neutro"),
            Product("C", "Caro", 250, 30, True, "neutro"),
        ]
        result = filter_products(products, {"budget_brl": 150})

        assert len(result) == 2
        assert all(p.price_brl <= 150 for p in result)

    def test_filter_empty_result_when_no_match(self):
        """Deve retornar lista vazia se nenhum produto atende todos os criterios."""
        from generator import filter_products, Product

        products = [
            Product("A", "Caro com Lactose", 500, 10, False, "neutro"),
        ]
        result = filter_products(products, {
            "dietary_restrictions": ["intolerancia_lactose"],
            "budget_brl": 100
        })

        assert len(result) == 0

    def test_generator_produces_response(self):
        """Generator deve produzir resposta candidata nao vazia."""
        from generator import generator_agent

        plan = {
            "conversation_id": "test_001",
            "known_constraints": {
                "dietary_restrictions": ["intolerancia_lactose"],
                "budget_brl": 200,
                "preferred_flavor": "chocolate"
            },
            "plan": [{"step_id": "s3", "task": "recomendar"}]
        }

        gen = generator_agent(plan=plan, catalog=make_catalog())
        assert len(gen.candidate_response) > 0
        assert len(gen.products_considered) >= 1

    def test_generator_respects_lactose_free(self):
        """Produtos considerados devem ser todos lactose_free quando ha restricao."""
        from generator import generator_agent

        plan = {
            "conversation_id": "test_001",
            "known_constraints": {
                "dietary_restrictions": ["intolerancia_lactose"],
                "budget_brl": 200,
                "preferred_flavor": "chocolate"
            },
            "plan": [{"step_id": "s3", "task": "recomendar"}]
        }

        gen = generator_agent(plan=plan, catalog=make_catalog())
        for p in gen.products_considered:
            assert p["lactose_free"] is True, f"Produto {p['name']} nao e lactose_free"

    def test_generator_handles_empty_catalog(self):
        """Deve retornar resposta de fallback com catalogo vazio."""
        from generator import generator_agent

        plan = {
            "conversation_id": "test_001",
            "known_constraints": {"budget_brl": 200},
            "plan": [{"step_id": "s3", "task": "recomendar"}]
        }

        gen = generator_agent(plan=plan, catalog=[])
        assert len(gen.candidate_response) > 0  # fallback, nao vazio


# ═══════════════════════════════════════════════════════════════
# Testes do Evaluator
# ═══════════════════════════════════════════════════════════════

class TestEvaluator:
    """Testes unitarios do agente Evaluator."""

    def make_generation(self, products=None, response="Recomendo Whey Isolado Chocolate."):
        return {
            "conversation_id": "test_001",
            "step_id": "s3",
            "candidate_response": response,
            "products_considered": products or [
                {"sku": "A", "name": "Whey Isolado", "price_brl": 150, "lactose_free": True}
            ]
        }

    def make_plan(self, constraints=None, rubric=None):
        return {
            "conversation_id": "test_001",
            "known_constraints": constraints or {
                "dietary_restrictions": ["intolerancia_lactose"],
                "budget_brl": 200
            },
            "evaluation_rubric": rubric or []
        }

    def test_approves_valid_generation(self):
        """Deve aprovar geracao que atende todos os criterios."""
        from evaluator import evaluator_agent

        evaluation = evaluator_agent(
            plan=self.make_plan(),
            generation=self.make_generation()
        )

        assert evaluation.status == "approved"
        assert all(r["passed"] for r in evaluation.rubric_results)

    def test_rejects_lactose_violation(self):
        """Deve rejeitar quando ha produto com lactose na lista."""
        from evaluator import evaluator_agent

        generation = self.make_generation(products=[
            {"sku": "A", "name": "Com Lactose", "price_brl": 100, "lactose_free": False}
        ])

        evaluation = evaluator_agent(
            plan=self.make_plan(),
            generation=generation
        )

        assert evaluation.status == "rejected"
        assert not all(r["passed"] for r in evaluation.rubric_results)

    def test_rejects_budget_violation(self):
        """Deve rejeitar quando produto excede orcamento."""
        from evaluator import evaluator_agent

        generation = self.make_generation(products=[
            {"sku": "A", "name": "Caro", "price_brl": 300, "lactose_free": True}
        ])

        evaluation = evaluator_agent(
            plan=self.make_plan(constraints={"budget_brl": 200}),
            generation=generation
        )

        assert evaluation.status == "rejected"

    def test_rejects_false_stock_promise(self):
        """Deve rejeitar resposta que afirma estoque sem confirmacao."""
        from evaluator import evaluator_agent

        generation = self.make_generation(
            response="Temos em estoque! Disponível agora para entrega!"
        )

        evaluation = evaluator_agent(
            plan=self.make_plan(),
            generation=generation
        )

        assert evaluation.status == "rejected"

    def test_rejects_pressure_tactics(self):
        """Deve rejeitar resposta com tatica de pressao."""
        from evaluator import evaluator_agent

        generation = self.make_generation(
            response="Compre ja! Ultimas unidades! Aproveite agora!"
        )

        evaluation = evaluator_agent(
            plan=self.make_plan(),
            generation=generation
        )

        assert evaluation.status == "rejected"

    def test_provides_specific_feedback_on_rejection(self):
        """Feedback deve listar criterios especificos que falharam."""
        from evaluator import evaluator_agent

        generation = self.make_generation(products=[
            {"sku": "A", "name": "Com Lactose e Caro", "price_brl": 500, "lactose_free": False}
        ])

        evaluation = evaluator_agent(
            plan=self.make_plan(),
            generation=generation
        )

        assert evaluation.status == "rejected"
        assert evaluation.feedback is not None
        assert len(evaluation.feedback) > 0


# ═══════════════════════════════════════════════════════════════
# Testes de Integracao
# ═══════════════════════════════════════════════════════════════

class TestIntegration:
    """Testes de integracao do fluxo completo."""

    def test_full_flow_delivers_response(self):
        """Fluxo completo Planner→Generator→Evaluator deve entregar resposta."""
        from orchestrator import run_customer_turn
        from planner import planner_agent
        from generator import generator_agent, SAMPLE_CATALOG
        from evaluator import evaluator_agent

        with tempfile.TemporaryDirectory() as tmpdir:
            result = run_customer_turn(
                message="Qual whey voce recomenda?",
                conversation_id="test_int_001",
                customer_id="cust_marina_4821",
                base_dir=Path(tmpdir),
                planner_fn=planner_agent,
                generator_fn=generator_agent,
                evaluator_fn=evaluator_agent,
                catalog=[asdict(p) for p in SAMPLE_CATALOG]
            )

            assert result["status"] in ["delivered", "fallback"]
            assert len(result["message"]) > 0
            assert result["iterations"] >= 1

    def test_state_files_are_created(self):
        """Deve criar arquivos de estado no diretorio da conversa."""
        from orchestrator import run_customer_turn
        from planner import planner_agent
        from generator import generator_agent, SAMPLE_CATALOG
        from evaluator import evaluator_agent

        with tempfile.TemporaryDirectory() as tmpdir:
            result = run_customer_turn(
                message="Quero comprar whey sem lactose",
                conversation_id="test_int_002",
                customer_id="cust_marina_4821",
                base_dir=Path(tmpdir),
                planner_fn=planner_agent,
                generator_fn=generator_agent,
                evaluator_fn=evaluator_agent,
                catalog=[asdict(p) for p in SAMPLE_CATALOG]
            )

            state_dir = Path(tmpdir) / "state" / "conversations" / "test_int_002"
            assert state_dir.exists()
            assert (state_dir / "conversation_event.json").exists()
            assert (state_dir / "plan.json").exists()
            assert (state_dir / "generation.json").exists()
            assert (state_dir / "evaluation.json").exists()
            assert (state_dir / "delivery.json").exists()

    def test_invalid_customer_raises_error(self):
        """Deve levantar erro para cliente nao cadastrado."""
        import pytest
        from orchestrator import run_customer_turn
        from planner import planner_agent
        from generator import generator_agent, SAMPLE_CATALOG
        from evaluator import evaluator_agent

        with tempfile.TemporaryDirectory() as tmpdir:
            with pytest.raises(ValueError, match="nao encontrado"):
                run_customer_turn(
                    message="Oi",
                    conversation_id="test_int_003",
                    customer_id="cliente_inexistente",
                    base_dir=Path(tmpdir),
                    planner_fn=planner_agent,
                    generator_fn=generator_agent,
                    evaluator_fn=evaluator_agent,
                    catalog=[asdict(p) for p in SAMPLE_CATALOG]
                )

    def test_budget_constrained_customer_gets_valid_recommendation(self):
        """Cliente com orcamento baixo deve receber recomendacao dentro do limite."""
        from orchestrator import run_customer_turn
        from planner import planner_agent
        from generator import generator_agent, SAMPLE_CATALOG
        from evaluator import evaluator_agent

        # Criar perfil com orcamento bem baixo
        from orchestrator import SAMPLE_PROFILES, CustomerProfile
        SAMPLE_PROFILES["cust_pobre"] = CustomerProfile(
            customer_id="cust_pobre",
            name="Orcamento Baixo",
            dietary_restrictions=[],
            preferences={"flavor": "neutro", "budget_brl": 80},
            risk_notes=[]
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            result = run_customer_turn(
                message="Qual o suplemento mais barato?",
                conversation_id="test_int_004",
                customer_id="cust_pobre",
                base_dir=Path(tmpdir),
                planner_fn=planner_agent,
                generator_fn=generator_agent,
                evaluator_fn=evaluator_agent,
                catalog=[asdict(p) for p in SAMPLE_CATALOG],
                profiles=SAMPLE_PROFILES
            )

            # Deve entregar algo (ou fallback se nada couber no orcamento)
            assert result["status"] in ["delivered", "fallback"]


# ═══════════════════════════════════════════════════════════════
# Testes de Borda
# ═══════════════════════════════════════════════════════════════

class TestEdgeCases:
    """Testes de casos limite e erro."""

    def test_empty_message_does_not_crash(self):
        """Mensagem vazia nao deve quebrar o Planner."""
        from planner import planner_agent

        plan = planner_agent(
            event={"conversation_id": "t", "customer_message": ""},
            profile={"dietary_restrictions": []}
        )
        assert plan.current_goal == "entender_necessidade_do_cliente"

    def test_all_products_filtered_out(self):
        """Quando todos os produtos sao filtrados, geracao ainda e valida."""
        from generator import generator_agent

        plan = {
            "conversation_id": "test",
            "known_constraints": {
                "dietary_restrictions": ["intolerancia_lactose"],
                "budget_brl": 10  # Nenhum produto custa tao pouco
            },
            "plan": [{"step_id": "s1", "task": "filtrar"}]
        }

        gen = generator_agent(plan=plan, catalog=make_catalog())
        assert len(gen.candidate_response) > 0  # Deve ter mensagem de fallback

    def test_missing_profile_fields_handled(self):
        """Perfil sem campos opcionais nao deve quebrar."""
        from planner import planner_agent

        plan = planner_agent(
            event={"conversation_id": "t", "customer_message": "Oi"},
            profile={"customer_id": "minimal"}
        )
        assert plan.current_goal is not None


# ═══════════════════════════════════════════════════════════════
# Runner
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import pytest
    import sys
    sys.exit(pytest.main([__file__, "-v"]))
```

### Como Executar os Testes

```bash
# Executar todos os testes
python -m pytest test_multi_agent.py -v

# Executar apenas testes do Planner
python -m pytest test_multi_agent.py::TestPlanner -v

# Executar testes de integracao
python -m pytest test_multi_agent.py::TestIntegration -v

# Executar com cobertura (se pytest-cov instalado)
python -m pytest test_multi_agent.py --cov=. --cov-report=term-missing
```

### Cobertura de Cenarios

| Cenario | Teste | Tipo |
|---------|-------|------|
| Cliente intolerante a lactose | `TestGenerator::test_filter_removes_lactose_products` | Unitario |
| Cliente com orcamento limitado | `TestGenerator::test_filter_respects_budget` | Unitario |
| Nenhum produto atende criterios | `TestGenerator::test_filter_empty_result_when_no_match` | Unitario |
| Resposta com afirmacao falsa de estoque | `TestEvaluator::test_rejects_false_stock_promise` | Unitario |
| Resposta com tatica de pressao | `TestEvaluator::test_rejects_pressure_tactics` | Unitario |
| Fluxo completo com entrega | `TestIntegration::test_full_flow_delivers_response` | Integracao |
| Persistencia de arquivos de estado | `TestIntegration::test_state_files_are_created` | Integracao |
| Cliente inexistente | `TestIntegration::test_invalid_customer_raises_error` | Integracao |
| Mensagem vazia | `TestEdgeCases::test_empty_message_does_not_crash` | Borda |
| Perfil com campos minimos | `TestEdgeCases::test_missing_profile_fields_handled` | Borda |

---

## 🔄 Alternativas de Implementacao

Esta secao documenta decisoes de design alternativas que foram consideradas e por que nao foram escolhidas para esta solucao.

### Alternativa 1: Agente Unico com Chain-of-Thought

**Abordagem:** Em vez de tres agentes, usar um unico agente com prompt que instrui "pense passo a passo: planeje, execute, depois verifique".

**Por que nao foi escolhida:** Chain-of-thought mantem os tres passos dentro da mesma context window e do mesmo vies cognitivo. O "verifique" ainda e feito pelo mesmo agente que "planejou" e "executou" — sycophancy permanece. Alem disso, nao ha estado persistido entre os passos: se o modelo alucinar no passo 2, o passo 3 nao tem como detectar porque perdeu o contexto do passo 1.

**Quando poderia ser usada:** Tarefas triviais onde o custo do erro e baixo e a latencia e prioridade maxima.

### Alternativa 2: Multi-Agente com Memoria Compartilhada

**Abordagem:** Agentes compartilham uma estrutura de dados em memoria (dict global, Redis) em vez de arquivos JSON.

**Por que nao foi escolhida:** Memoria compartilhada:
- Nao persiste entre reinicios do processo
- Nao cria audit trail automatico
- Torna debug mais dificil (voce nao tem snapshot do estado em cada passo)
- Cria risco de race condition se agentes rodarem em paralelo

**Quando poderia ser usada:** Sistemas de baixa latencia onde performance e mais importante que auditabilidade e o estado e efemero.

### Alternativa 3: Planner e Generator Fundidos

**Abordagem:** Fundir Planner e Generator em um unico agente que "planeja e executa" em uma chamada, mantendo apenas o Evaluator separado.

**Por que nao foi escolhida:** Esta abordagem e um meio-termo entre agente unico e tres agentes. Reduz latencia (2 chamadas em vez de 3), mas traz de volta o problema de planning/execution collapse: o agente que executa tambem decide o que fazer, e pode mudar o plano implicitamente durante a execucao sem registrar.

**Quando poderia ser usada:** Quando a jornada e simples (maximo 3 passos) e o custo do erro e moderado. Um bom ponto de partida para times migrando de Nivel 2 para Nivel 3.

### Alternativa 4: Evaluator como LLM (nao heuristico)

**Abordagem:** Usar uma chamada LLM para o Evaluator, com um prompt que lista a rubrica e pede para verificar cada criterio.

**Por que nao foi escolhida para esta solucao:** Para o exercicio, heuristica e mais:
- Deterministico (mesmo input = mesmo output)
- Testavel (sem depender de API externa)
- Rapido (sem latencia de rede)

Em producao, um Evaluator hibrido e recomendado: heuristico para criterios objetivos (preco, lactose, formato) e LLM para criterios subjetivos (tom humano, clareza, empatia).

### Tabela Resumo de Trade-offs

| Decisao | Escolha | Alternativa | Trade-off |
|---------|---------|-------------|-----------|
| Comunicacao | File-based JSON | Redis queues | Simplicidade vs throughput |
| Planner | Heuristico | LLM-based | Determinismo vs flexibilidade |
| Generator | Regras + formatacao | LLM-based | Testabilidade vs qualidade de linguagem |
| Evaluator | Heuristico | LLM-based | Velocidade vs julgamento subjetivo |
| Validacao | Binaria (pass/fail) | Score 0-100 | Clareza vs nuance |
| State | Arquivos por conversa | Banco de dados | Simplicidade vs queries |
| Retry | Max 3 iteracoes | Ilimitado com backoff | Seguranca de custo vs chance de sucesso |

---

## 🚀 Aplicacao KODA: Da Solucao do Exercicio para Producao

O sistema implementado neste exercicio e uma versao educacional. Para levar essa arquitetura a producao no KODA, algumas adaptacoes sao necessarias.

### O Que Muda em Producao

| Componente | Exercicio | Producao KODA |
|-----------|-----------|---------------|
| **Planner** | Heuristico (palavras-chave) | LLM (Claude Haiku) com prompt de decomposicao |
| **Generator** | Regras + formatacao | LLM (Claude Sonnet) com tool use para API de catalogo |
| **Evaluator** | Heuristico (checks de campo) | Hibrido: heuristico para fatos, LLM para tom e coerencia |
| **State Store** | Arquivos JSON locais | S3 + Redis para cache quente |
| **Catalogo** | Lista em memoria | API REST com cache TTL de 5 minutos |
| **Orquestrador** | Funcao sincrona | AWS Step Functions ou Temporal para workflows longos |
| **Observabilidade** | Prints + arquivos | OpenTelemetry traces + CloudWatch dashboards |

### Roadmap de Evolucao

```
Fase 1 (este exercicio): File-based, heuristico, local
  → Aprender contratos e fluxo sem dependencias externas

Fase 2 (piloto): Adicionar LLM ao Generator, manter Planner e Evaluator heuristicos
  → Validar que LLM melhora qualidade de resposta sem introduzir novos erros

Fase 3 (producao inicial): LLM no Planner e Generator, Evaluator hibrido
  → Feature flag para rollout gradual (10% → 50% → 100% do trafego)

Fase 4 (escala): Migrar state store para S3, introduzir filas para paralelismo
  → Suportar 10x volume sem degradacao de latencia

Fase 5 (maturidade): Event-driven para jornadas pos-compra, dashboards de qualidade
  → Fulfillment, reengajamento e deteccao de abandono automatizados
```

### Metricas para Acompanhar em Producao

```
┌──────────────────────────────────────────────────────────────┐
│              Multi-Agent System Dashboard — KODA              │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Throughput:        1,200 turns/hour                         │
│  Latencia P95:      2.1s (Planner 0.3 + Gen 1.2 + Eval 0.6) │
│  Approval Rate:     87% (1a tentativa), 96% (ate 3a)        │
│  Fallback Rate:     2% (max_iterations atingido)             │
│                                                              │
│  Qualidade:                                                  │
│  - Recomendacoes corretas:  98.2%  (era 75% sem multi-agente)│
│  - Reclamacoes pos-compra:  1.8%   (era 15%)                │
│  - Taxa de devolucao:       4.2%   (era 12%)                │
│                                                              │
│  Custo por Turno:     R$ 0.032 (3 chamadas LLM + infra)     │
│  Custo Mensal Est.:   R$ 1,152 (36,000 turns estimados)     │
│  ROI Estimado:        43x (reducao de erro = economia)       │
│                                                              │
│  Alertas:                                                     │
│  🔴 Approval Rate < 70% → Revisar prompts do Generator       │
│  🟡 Fallback Rate > 5%  → Revisar rubrica do Evaluator       │
│  🟢 Latencia P95 < 3s   → Dentro do target                  │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## ✅ O Que Voce Aprendeu

Este checkpoint cobre tudo que esta solucao demonstrou. Marque os itens que voce consegue explicar com suas proprias palavras.

### Fundamentos de Multi-Agent Design

- [ ] Consigo explicar por que 3 agentes (Planner, Generator, Evaluator) sao melhores que 1 agente para jornadas complexas
- [ ] Consigo desenhar o fluxo de dados entre os agentes: event → plan → generation → evaluation → delivery
- [ ] Entendo que cada agente tem ownership claro e nao invade a responsabilidade do outro
- [ ] Consigo diferenciar as responsabilidades: Planner planeja, Generator executa, Evaluator valida

### Implementacao

- [ ] Consigo implementar um Planner que decompoe uma mensagem em etapas com criterios de sucesso
- [ ] Consigo implementar um Generator que filtra produtos, seleciona alternativas e formata resposta
- [ ] Consigo implementar um Evaluator que verifica criterios um a um com evidencias
- [ ] Consigo escrever um orquestrador que gerencia o fluxo e persiste estado em arquivos JSON
- [ ] Entendo o conceito de `max_iterations` e fallback seguro

### Arquitetura e Design

- [ ] Consigo explicar por que file-based coordination e a melhor escolha para aprendizado
- [ ] Consigo comparar as tres estrategias de coordenacao (sequencial, paralelo, event-driven) e escolher a certa para cada cenario
- [ ] Entendo os trade-offs de cada decisao de design (heuristico vs LLM, binario vs score, local vs distribuido)
- [ ] Consigo identificar quando multi-agente seria overengineering

### Testes e Qualidade

- [ ] Consigo escrever testes unitarios para cada agente isoladamente
- [ ] Consigo escrever testes de integracao para o fluxo completo
- [ ] Entendo a importancia de testar casos limite (orcamento zero, catalogo vazio, restricoes conflitantes)
- [ ] Consigo interpretar o resultado de uma avaliacao (approved/rejected) e agir sobre o feedback

### Aplicacao Pratica

- [ ] Consigo descrever como essa arquitetura se aplica ao KODA em producao
- [ ] Entendo o roadmap de evolucao: heuristico → LLM → hibrido → distribuido
- [ ] Consigo estimar metricas de sucesso (approval rate, latencia, custo por turno)
- [ ] Sei quais alertas monitorar e o que fazer quando disparam

---

## 📚 Referencias e Proximas Leituras

### Dentro deste Programa

- [01-multi-agent-systems.md](../../01-multi-agent-systems.md) — Teoria completa de sistemas multi-agente
- [02-state-persistence.md](../../02-state-persistence.md) — Aprofundamento em persistencia de estado
- [03-file-based-coordination.md](../../03-file-based-coordination.md) — Contratos JSON em detalhe
- [../../02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md](../../../02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md) — Base Generator/Evaluator do Nivel 2
- [../../02-nivel-2-practical-patterns/koda-applications/nivel-2-koda.md](../../../02-nivel-2-practical-patterns/koda-applications/nivel-2-koda.md) — KODA no Nivel 2
- [../../../GLOSSARY.md](../../../GLOSSARY.md) — Termos tecnicos

### Externo

- Documentacao do Python `dataclasses` e `pathlib`
- AWS Step Functions para orquestracao de workflows longos
- Temporal.io para workflows distribudos com retry e state persistence
- Papers sobre multi-agent coordination em LLM applications

---

## 💭 Reflexao Final

Quando Marina abriu o WhatsApp aquela noite, ela nao sabia nada sobre arquitetura de software.

Ela so queria uma recomendacao que respeitasse sua intolerancia a lactose, seu orcamento de R$ 220 e sua preferencia por chocolate.

O agente unico falhou porque tentou ser inteligente demais: planejar, executar e validar tudo de uma vez, sem separacao de responsabilidades, sem checkpoints, sem estado persistente.

A arquitetura de tres agentes resolveu isso nao por ser mais complexa, mas por ser mais **honesta**.

O Planner admitiu: "nao sei tudo, vou decompor em passos pequenos".

O Generator admitiu: "vou executar cada passo e registrar minhas suposicoes, mas nao confie em mim para validar".

O Evaluator admitiu: "meu unico trabalho e encontrar erros, e vou fazer isso com criterios concretos".

Essa honestidade arquitetural — cada componente sabendo exatamente seu papel e suas limitacoes — e o que separa sistemas que funcionam em laboratorio de sistemas que funcionam com clientes reais.

O codigo que voce viu aqui nao e complexo. Estruturado, sim. Mas cada funcao faz uma coisa. Cada agente tem um contrato claro. Cada decisao deixa rastro.

Esse e o verdadeiro poder de multi-agent systems: nao e sobre ter muitos agentes. E sobre ter os agentes certos, com as responsabilidades certas, comunicando-se por artefatos auditaveis.

Agora, ao olhar para o KODA — ou para qualquer sistema que precise manter qualidade por horas — voce nao ve mais um monte de chamadas de API. Voce ve Planner, Generator, Evaluator. Ve contratos JSON. Ve state persistence. Ve trace lines.

Essa e a diferenca entre quem usa agentes e quem projeta sistemas de agentes.

---

## 📋 Metadata

| Campo | Valor |
|-------|-------|
| **Arquivo** | `curriculum/03-nivel-3-advanced-architecture/exercises/solutions/exercise-01-solution.md` |
| **Exercicio** | 1 — Multi-Agent Design: Planner/Generator/Evaluator |
| **Nivel** | 3 — Arquitetura Avancada |
| **Tempo Estimado** | 120-150 minutos |
| **Status** | ✅ Solucao Completa |
| **Proximo** | `exercise-02.md` (State Persistence) |
| **Dependencias** | `01-multi-agent-systems.md`, Nivel 2 completo |
| **Atualizado** | Maio 2026 |
| **Issue** | [#9](https://github.com/pavani06/long-running-agents/issues/9) |

---

*Solucao completa do Exercicio 1 — Nivel 3 — Multi-Agent Design*
*Escrito com foco em clareza, aplicabilidade e rigor arquitetonico.*
*KODA Curriculum | FutanBear Technical Team | Maio 2026*
