# 🧠 Exercício 1: Implementar Sistema Multi-Agente Planner/Generator/Evaluator
## Nível 3 — Arquitetura Avançada

**Tempo Estimado:** 60-90 minutos
**Dificuldade:** ⭐⭐⭐⭐ (Avançado)
**Pré-requisito:** Ter lido `01-multi-agent-systems.md` + `02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md`
**Objetivo:** Construir um harness de 3 agentes que decompoe, executa e valida uma recomendacao de produto no KODA

---

## 📖 Prólogo: O Pedido Que Custou um Cliente

**Segunda-feira, 16h15. Loja de suplementos online.**

Rafael acabou de entrar no WhatsApp do KODA. Ele treina ha 3 meses, tem resultados decentes, mas sente que precisa de algo a mais. Um amigo recomendou creatina. Ele nao sabe nada sobre creatina — so sabe que o amigo falou que "ajuda no treino".

```
16:15 Rafael: Oi, quero comprar creatina. O que voce tem?
16:15 KODA: Ola Rafael! Temos varias opcoes. Creatina monohidratada, micronizada, 
       com sabor, sem sabor. Qual e seu objetivo principal?
```

Ate aqui, tudo bem. O agente unico esta sendo util.

```
16:17 Rafael: Meu objetivo e ganhar forca. Treino 5x por semana. Tenho R$ 80.
16:18 KODA: Perfeito. Com R$ 80, temos otimas opcoes. Creatina monohidratada 300g 
       por R$ 69,90 ou creatina micronizada 250g por R$ 74,90.
```

Rafael ficou interessado. Duas opcoes, precos dentro do orcamento. O KODA parecia util.

```
16:20 Rafael: Qual a diferenca entre monohidratada e micronizada?
16:21 KODA: A micronizada tem particulas menores, dissolve melhor e pode causar menos 
       desconforto gastrico. A monohidratada e a mais estudada, eficacia comprovada, 
       mas algumas pessoas relatam leve inchaco.
16:22 Rafael: Entao a micronizada e melhor?
16:22 KODA: Depende do que voce valoriza. Se quer maxima absorcao e menos desconforto, 
       a micronizada. Se quer o melhor custo-beneficio com a mesma eficacia, a monohidratada.
```

Resposta boa. Informativa, balanceada.

```
16:24 Rafael: Tem alguma promocao?
16:24 KODA: A monohidratada 300g esta com 10% de desconto no combo com whey protein. 
       Ficaria R$ 62,91. A micronizada nao tem promocao ativa no momento.
```

Mais uma resposta util. O KODA esta entregando valor.

**Minuto 14: a conversa muda.**

```
16:29 Rafael: E whey protein? Quanto custa? Qual o melhor?
16:30 KODA: Temos Whey Concentrado 1kg por R$ 89,90 e Whey Isolado 900g por R$ 139,90. 
       Recomendo o Isolado para melhor pureza, menos lactose e absorcao mais rapida.
```

Rafael nao perguntou sobre pureza ou lactose. Ele perguntou sobre preco e qualidade. O KODA assumiu preferencias que o cliente nunca expressou.

```
16:32 Rafael: Mas eu falei que meu orcamento e R$ 80.
16:32 KODA: Voce tem razao, me desculpe. O Whey Concentrado 1kg esta por R$ 89,90, 
       um pouco acima. Posso procurar opcoes menores?
16:33 Rafael: Nao, espera. Eu queria creatina. Por que voce mudou para whey?
```

A conversa comecou a descarrilhar. O agente unico perdeu o foco. Ele seguiu o cliente na tangente do whey protein, esquecendo que o objetivo original era creatina e o orcamento era R$ 80.

```
16:35 Rafael: Olha, deixa pra la. Vou comprar em outro lugar.
16:35 KODA: Sinto muito pela confusao, Rafael. Posso te ajudar com a creatina agora, 
       dentro do seu orcamento de R$ 80.
16:36 Rafael: Nao, obrigado. Ate mais.
```

**Rafael saiu. A venda foi perdida.**

O que aconteceu? O KODA nao era um agente ruim. Ele respondeu bem a perguntas diretas. Ele conhecia os produtos. Ele era educado.

O problema nao estava na qualidade das respostas individuais.

O problema estava na orquestracao.

### A Autopsia da Conversa

Quando a equipe KODA analisou o trace dessa conversa, encontrou tres falhas arquiteturais:

**Falha 1: Perda de Objetivo (Drift de Contexto)**

O cliente comecou pedindo creatina. No minuto 14, perguntou sobre whey protein por curiosidade. O agente unico tratou essa curiosidade como uma mudanca de objetivo. Em vez de responder brevemente e voltar ao foco, ele abandonou completamente a missao creatina e iniciou um fluxo novo de recomendacao de whey.

Sem um Planner dedicado que mantivesse o objetivo registrado, o agente seguiu a tangente.

**Falha 2: Violacao de Restricao (Orcamento Ignorado)**

O cliente estabeleceu orcamento de R$ 80. O KODA registrou esse valor. Mesmo assim, quando recomendou whey, ignorou completamente o limite. Recomendou produtos de R$ 89,90 e R$ 139,90 — ambos acima do orcamento.

Sem um Evaluator dedicado que verificasse restricoes antes da resposta, o KODA nao percebeu a violacao de contrato.

**Falha 3: Auto-Aprovacao (Sycophancy)**

Quando o cliente apontou o problema do orcamento, o KODA pediu desculpas e se ofereceu para "procurar opcoes menores". Mas essa correcao foi reativa — aconteceu depois que o cliente ja havia perdido a paciencia. Se um Evaluator tivesse examinado cada resposta antes do envio, o erro do orcamento teria sido capturado antes de chegar ao cliente.

### O Que Teria Acontecido com Multi-Agente?

Se essa mesma conversa tivesse passado por um sistema Planner/Generator/Evaluator:

1. **Planner** teria registrado: "objetivo principal = creatina dentro de R$ 80, tangente whey = curiosidade apenas, responder brevemente e voltar ao foco"
2. **Generator** teria recebido um plano claro: "responda curiosidade sobre whey em 1 frase e retome recomendacao de creatina"
3. **Evaluator** teria verificado: "orcamento R$ 80 respeitado? Objetivo creatina mantido? Tangente whey nao virou novo fluxo?"

O resultado: Rafael teria recebido uma resposta curta sobre whey ("Temos opcoes a partir de R$ 89,90, um pouco acima do seu orcamento atual") e o foco teria voltado imediatamente para a creatina. A venda provavelmente teria sido fechada.

Esta e a diferenca entre um agente unico tentando fazer tudo e um sistema multi-agente com responsabilidades separadas.

Neste exercicio, voce vai construir exatamente esse sistema.

---

## 🎯 Objetivo

Voce vai implementar um **harness multi-agente** com tres agentes especializados que colaboram para gerar recomendacoes seguras no KODA:

1. **Planner Agent:** Decompoe a tarefa do cliente em etapas, define criterios de sucesso e cria rubricas de avaliacao
2. **Generator Agent:** Executa cada etapa planejada, consulta dados de produto e gera respostas candidatas
3. **Evaluator Agent:** Valida cada resposta contra criterios, verifica restricoes e aprova ou rejeita com feedback

O sistema usa **file-based coordination** — cada agente le e escreve arquivos JSON como contrato de comunicacao. Isso cria um audit trail completo e permite debugar cada decisao.

**Resultado Final:** Voce entendera na pratica por que separar planejamento, execucao e avaliacao produz recomendacoes mais seguras e conversas mais longas sem degradacao.

---

## 📋 Requisitos

### Funcionais

- [ ] Sistema recebe uma mensagem do cliente e retorna resposta aprovada ou fallback
- [ ] Planner decompoe a tarefa, define `plan.json` com etapas e criterios de sucesso
- [ ] Generator executa a etapa designada, produz `generation.json` com resposta candidata e evidencias
- [ ] Evaluator valida `generation.json` contra `plan.json`, produz `evaluation.json` com status (`approved` ou `rejected`)
- [ ] Se rejeitado, Generator recebe feedback e tenta novamente (maximo 2 revisoes)
- [ ] Se aprovado, resposta e entregue ao cliente
- [ ] Se 2 revisoes falham, sistema retorna fallback seguro ("Preciso confirmar um detalhe antes de responder")
- [ ] Todo o estado e persistido em arquivos JSON no diretorio `state/<conversation_id>/`
- [ ] Cada arquivo inclui `schema_version`, `conversation_id` e timestamp

### Tecnicos

- [ ] Python 3.9+ (type hints nativos, sem necessidade de `from __future__`)
- [ ] Usar apenas biblioteca padrao (`json`, `pathlib`, `datetime`, `dataclasses`, `typing`)
- [ ] Nao usar frameworks externos (Flask, FastAPI, Pydantic)
- [ ] Estrutura de diretorios: `state/<conversation_id>/` com arquivos `plan.json`, `generation.json`, `evaluation.json`
- [ ] Funcoes puras para cada agente (recebem dados, retornam dados, nao tem efeitos colaterais exceto escrita em disco)
- [ ] Type hints em todas as funcoes publicas
- [ ] Docstrings no formato Google-style para cada funcao

### Validação

- [ ] Cenario 1 (caminho feliz): recomendacao aprovada na primeira tentativa
- [ ] Cenario 2 (rejeicao): recomendacao viola restricao, avaliador rejeita, generator corrige
- [ ] Cenario 3 (fallback): duas tentativas falham, sistema retorna mensagem segura
- [ ] Cenario 4 (orcamento): sistema nunca recomenda produto acima do budget
- [ ] Cenario 5 (restricao alimentar): sistema nunca recomenda produto com alergeno bloqueado
- [ ] Cenario 6 (audit trail): todos os arquivos JSON sao gerados e contem os campos obrigatorios

---

## 🏗️ Arquitetura do Sistema

### Diagrama ASCII

```
┌──────────────────────────────────────────────────────────────────────┐
│                          WHATSAPP CLIENTE                             │
│     Mensagem: "Quero comprar creatina, R$ 80, intolerante a lactose"  │
└────────────────────────────────┬─────────────────────────────────────┘
                                 │
                                 ▼
┌──────────────────────────────────────────────────────────────────────┐
│                           STATE STORE                                 │
│   state/conv_rafael_001/                                              │
│   ├── customer_profile.json   (preferencias, restricoes, budget)      │
│   ├── product_catalog.json    (dados simulados de produtos)           │
│   └── conversation_event.json (mensagem recebida + timestamp)         │
└────────────────────────────────┬─────────────────────────────────────┘
                                 │
                                 ▼
┌──────────────────────────────────────────────────────────────────────┐
│                         PLANNER AGENT                                 │
│  Input:  conversation_event.json + customer_profile.json              │
│  Output: plan.json                                                    │
│                                                                       │
│  Responsabilidades:                                                   │
│  • Identifica objetivo principal (ex: "comprar creatina")             │
│  • Extrai restricoes (ex: budget=R$80, no_lactose)                    │
│  • Cria etapas numeradas (step_id, task, owner, success_criteria)     │
│  • Define rubrica de avaliacao (criterios que Evaluator vai verificar)│
│  • Registra tangentes como "curiosidade, nao mudar objetivo"          │
└────────────────────────────────┬─────────────────────────────────────┘
                                 │ plan.json
                                 ▼
┌──────────────────────────────────────────────────────────────────────┐
│                        GENERATOR AGENT                                │
│  Input:  plan.json + product_catalog.json                             │
│  Output: generation.json                                              │
│                                                                       │
│  Responsabilidades:                                                   │
│  • Le o plano e identifica a etapa atual                              │
│  • Consulta product_catalog.json para buscar produtos                 │
│  • Filtra produtos por restricoes (lactose, budget, categoria)        │
│  • Gera resposta candidata em portugues natural                       │
│  • Registra evidencias (quais produtos foram considerados)            │
│  • Registra suposicoes explicitamente                                 │
│  • NAO aprova o proprio trabalho                                      │
└────────────────────────────────┬─────────────────────────────────────┘
                                 │ generation.json
                                 ▼
┌──────────────────────────────────────────────────────────────────────┐
│                        EVALUATOR AGENT                                │
│  Input:  plan.json + generation.json + customer_profile.json          │
│  Output: evaluation.json                                              │
│                                                                       │
│  Responsabilidades:                                                   │
│  • Le o plano original (criterios de sucesso)                         │
│  • Le a resposta candidata do Generator                               │
│  • Verifica CADA criterio da rubrica                                 │
│  • Verifica restricoes do customer_profile (budget, alergias)         │
│  • Verifica se ha afirmacoes sem evidencia                            │
│  • Decide: approved ou rejected                                       │
│  • Se rejected: fornece feedback especifico (qual criterio falhou)    │
│  • Se approved: prepara resposta final para o cliente                 │
└───────────────┬───────────────────────────────────┬───────────────────┘
                │ approved                          │ rejected
                ▼                                   ▼
┌──────────────────────────────┐    ┌──────────────────────────────────┐
│  Resposta final para cliente │    │  Feedback para Generator         │
│  "Rafael, recomendo a        │    │  "orcamento excedido: R$89,90 >  │
│   Creatina Monohidratada      │    │   R$80. Refiltrar por budget."   │
│   300g, R$ 69,90..."         │    │                                   │
└──────────────────────────────┘    └──────────────┬───────────────────┘
                                                   │
                                                   ▼
                                        ┌──────────────────────────────┐
                                        │  Novo ciclo: Generator tenta │
                                        │  novamente (max 2 revisoes)  │
                                        │  Se falhar: fallback seguro  │
                                        └──────────────────────────────┘
```

### Data Flow Entre Agentes

| Etapa | Input | Output | Dono | Arquivo |
|-------|-------|--------|------|---------|
| Entrada | Mensagem WhatsApp + perfil + catalogo | Evento de conversa | Harness | `conversation_event.json` |
| Planejamento | Evento + perfil + catalogo | Plano com etapas e rubrica | Planner | `plan.json` |
| Geracao | Plano + catalogo | Resposta candidata + evidencias | Generator | `generation.json` |
| Avaliacao | Plano + geracao + perfil | Decisao + feedback | Evaluator | `evaluation.json` |
| Entrega | Resposta aprovada | Mensagem final | Harness | `delivery.json` |

---

## 🚀 Starter Code

```python
"""
Exercicio 1 — Sistema Multi-Agente Planner/Generator/Evaluator
Nivel 3 — Arquitetura Avancada

Implemente um harness de 3 agentes que colaboram via arquivos JSON
para gerar recomendacoes seguras de suplementos no KODA.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class Product:
    """Representa um produto no catalogo simulado do KODA."""
    sku: str
    name: str
    category: str           # ex: "creatina", "whey", "pre_treino"
    price_brl: float
    servings: int
    lactose_free: bool
    gluten_free: bool
    in_stock: bool
    rating: float           # 0.0 a 5.0


@dataclass
class CustomerProfile:
    """Perfil do cliente com preferencias e restricoes."""
    customer_id: str
    name: str
    budget_brl: float
    dietary_restrictions: list[str] = field(default_factory=list)
    preferred_flavor: Optional[str] = None
    training_goal: Optional[str] = None
    training_frequency: Optional[str] = None


@dataclass
class ConversationEvent:
    """Evento de entrada: mensagem recebida do WhatsApp."""
    conversation_id: str
    turn_id: str
    customer_message: str
    received_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class PlanStep:
    """Uma etapa do plano criado pelo Planner."""
    step_id: str
    task: str
    owner: str                      # "generator"
    success_criteria: list[str] = field(default_factory=list)


@dataclass
class Plan:
    """Plano completo criado pelo Planner."""
    schema_version: str = "1.0"
    conversation_id: str = ""
    current_goal: str = ""
    known_constraints: dict[str, Any] = field(default_factory=dict)
    steps: list[PlanStep] = field(default_factory=list)
    evaluation_rubric: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class Generation:
    """Resposta candidata gerada pelo Generator."""
    schema_version: str = "1.0"
    conversation_id: str = ""
    step_id: str = ""
    candidate_response: str = ""
    products_considered: list[dict[str, Any]] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)
    generated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class RubricResult:
    """Resultado da verificacao de um criterio da rubrica."""
    criterion: str
    passed: bool
    evidence: str


@dataclass
class Evaluation:
    """Resultado da avaliacao feita pelo Evaluator."""
    schema_version: str = "1.0"
    conversation_id: str = ""
    evaluated_step_id: str = ""
    status: str = ""                # "approved" ou "rejected"
    rubric_results: list[RubricResult] = field(default_factory=list)
    feedback: str = ""              # presente apenas se rejected
    checked_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def write_json(directory: Path, filename: str, data: Any) -> Path:
    """
    Escreve dados em arquivo JSON de forma atomica.

    Args:
        directory: Diretorio de destino (ex: state/conv_001)
        filename: Nome do arquivo (ex: plan.json)
        data: Dados a serializar (dict ou dataclass)

    Returns:
        Path do arquivo escrito.

    Raises:
        OSError: Se nao for possivel criar o diretorio ou escrever o arquivo.
    """
    # TODO: Implementar escrita atomica com arquivo temporario
    # 1. Converter dataclass para dict se necessario
    # 2. Criar diretorio (parents=True, exist_ok=True)
    # 3. Escrever em arquivo temporario primeiro
    # 4. Renomear arquivo temporario para nome final (operacao atomica)
    pass


def read_json(filepath: Path) -> dict[str, Any]:
    """
    Le arquivo JSON e retorna como dicionario.

    Args:
        filepath: Caminho completo do arquivo JSON.

    Returns:
        Dicionario com os dados do arquivo.

    Raises:
        FileNotFoundError: Se o arquivo nao existir.
        json.JSONDecodeError: Se o JSON for invalido.
    """
    # TODO: Implementar leitura de arquivo JSON
    # 1. Abrir arquivo com encoding utf-8
    # 2. Fazer json.load()
    # 3. Retornar dicionario
    pass


def dataclass_to_dict(obj: Any) -> dict[str, Any]:
    """
    Converte uma dataclass (ou lista de dataclasses) para dicionario serializavel.

    Args:
        obj: Instancia de dataclass ou lista delas.

    Returns:
        Dicionario ou lista de dicionarios.
    """
    # TODO: Implementar conversao recursiva dataclass -> dict
    # 1. Se for dataclass, usar asdict()
    # 2. Se for lista, converter cada elemento
    # 3. Se for dict, processar valores recursivamente
    pass


# ============================================================================
# PRODUCT CATALOG (Dados simulados)
# ============================================================================

PRODUCT_CATALOG: list[Product] = [
    Product(
        sku="CREA-MONO-300",
        name="Creatina Monohidratada 300g",
        category="creatina",
        price_brl=69.90,
        servings=60,
        lactose_free=True,
        gluten_free=True,
        in_stock=True,
        rating=4.8,
    ),
    Product(
        sku="CREA-MICRO-250",
        name="Creatina Micronizada 250g",
        category="creatina",
        price_brl=74.90,
        servings=50,
        lactose_free=True,
        gluten_free=True,
        in_stock=True,
        rating=4.6,
    ),
    Product(
        sku="WHEY-CONC-CHOC-1000",
        name="Whey Concentrado Chocolate 1kg",
        category="whey",
        price_brl=89.90,
        servings=30,
        lactose_free=False,
        gluten_free=True,
        in_stock=True,
        rating=4.5,
    ),
    Product(
        sku="WHEY-ISO-CHOC-900",
        name="Whey Isolado Chocolate 900g",
        category="whey",
        price_brl=139.90,
        servings=27,
        lactose_free=True,
        gluten_free=True,
        in_stock=True,
        rating=4.7,
    ),
    Product(
        sku="WHEY-VEG-BAUN-750",
        name="Proteina Vegetal Baunilha 750g",
        category="whey",
        price_brl=99.90,
        servings=25,
        lactose_free=True,
        gluten_free=True,
        in_stock=True,
        rating=4.3,
    ),
    Product(
        sku="PRE-TREINO-CAFE-300",
        name="Pre-Treino Cafeina 300g",
        category="pre_treino",
        price_brl=79.90,
        servings=30,
        lactose_free=True,
        gluten_free=True,
        in_stock=False,
        rating=4.4,
    ),
    Product(
        sku="BCAA-PO-200",
        name="BCAA em Po 200g",
        category="bcaa",
        price_brl=59.90,
        servings=40,
        lactose_free=True,
        gluten_free=True,
        in_stock=True,
        rating=4.1,
    ),
    Product(
        sku="CREA-CREA-150",
        name="Creatina Creapure 150g",
        category="creatina",
        price_brl=89.90,
        servings=30,
        lactose_free=True,
        gluten_free=True,
        in_stock=True,
        rating=4.9,
    ),
]


# ============================================================================
# PLANNER AGENT
# ============================================================================

def planner_agent(
    event: ConversationEvent,
    profile: CustomerProfile,
    catalog: list[Product],
) -> Plan:
    """
    Planner Agent: decompoe a tarefa do cliente em etapas e define criterios.

    Responsabilidades:
    1. Identificar o objetivo principal da mensagem do cliente
    2. Extrair restricoes conhecidas (budget, alergias, preferencias)
    3. Criar ate 3 etapas (steps) com criterios de sucesso
    4. Definir rubrica de avaliacao para o Evaluator

    Args:
        event: Evento de conversa com a mensagem do cliente.
        profile: Perfil do cliente com budget, restricoes e preferencias.
        catalog: Lista de produtos disponiveis.

    Returns:
        Plan com etapas e rubrica de avaliacao.

    Exemplo de output esperado:
        Plan(
            conversation_id="conv_rafael_001",
            current_goal="recomendar creatina dentro do orcamento de R$ 80",
            known_constraints={"budget_brl": 80.0, "lactose_free": True},
            steps=[
                PlanStep(step_id="s1", task="filtrar produtos da categoria desejada",
                         success_criteria=["categoria correta", "em estoque"]),
                PlanStep(step_id="s2", task="aplicar restricoes e orcamento",
                         success_criteria=["preco <= budget", "sem lactose se required"]),
                PlanStep(step_id="s3", task="preparar resposta curta para WhatsApp",
                         success_criteria=["tom humano", "objetivo mantido", "sem jargao"]),
            ],
            evaluation_rubric=[
                "respeita orcamento definido no perfil",
                "respeita restricoes alimentares",
                "nao recomenda produto fora de estoque",
                "mantem foco no objetivo principal",
                "explica recomendacao sem pressionar compra",
            ],
        )
    """
    # TODO: Implementar o Planner Agent
    #
    # Algoritmo sugerido:
    # 1. Analisar event.customer_message para extrair categoria desejada
    #    - Procurar palavras-chave: "creatina", "whey", "pre treino", "bcaa"
    #    - Se nao encontrar, assumir "todos"
    #
    # 2. Extrair restricoes do profile:
    #    - budget_brl: usar profile.budget_brl
    #    - lactose_free: True se "intolerancia a lactose" ou "lactose" em dietary_restrictions
    #    - gluten_free: True se "gluten" em dietary_restrictions
    #
    # 3. Criar 3 etapas (steps):
    #    - s1: filtrar por categoria e estoque
    #    - s2: aplicar restricoes (budget, lactose, gluten)
    #    - s3: preparar resposta final
    #
    # 4. Definir evaluation_rubric com 5 criterios
    #
    # 5. Preencher Plan e retornar
    pass


# ============================================================================
# GENERATOR AGENT
# ============================================================================

def generator_agent(
    plan: Plan,
    catalog: list[Product],
    evaluator_feedback: Optional[str] = None,
) -> Generation:
    """
    Generator Agent: executa uma etapa do plano e gera resposta candidata.

    Responsabilidades:
    1. Executar a etapa designada no plano
    2. Filtrar produtos do catalogo conforme criterios
    3. Gerar resposta candidata em linguagem natural
    4. Registrar produtos considerados e suposicoes
    5. NAO aprovar o proprio trabalho

    Args:
        plan: Plano com etapas e criterios de sucesso.
        catalog: Lista de produtos disponiveis.
        evaluator_feedback: Se presente, e uma revisao (feedback do Evaluator).

    Returns:
        Generation com resposta candidata, produtos considerados e suposicoes.

    Exemplo de output esperado:
        Generation(
            conversation_id="conv_rafael_001",
            step_id="s1",
            candidate_response="Rafael, encontrei 3 creatinas em estoque: "
                              "Monohidratada 300g (R$69,90), Micronizada 250g "
                              "(R$74,90) e Creapure 150g (R$89,90).",
            products_considered=[
                {"sku": "CREA-MONO-300", "price_brl": 69.90},
                {"sku": "CREA-MICRO-250", "price_brl": 74.90},
                {"sku": "CREA-CREA-150", "price_brl": 89.90},
            ],
            assumptions=["cliente quer ate 2 opcoes para comparar"],
        )
    """
    # TODO: Implementar o Generator Agent
    #
    # Algoritmo sugerido:
    # 1. Se evaluator_feedback existe, estamos em modo revisao:
    #    - Tentar corrigir o problema apontado no feedback
    #    - Refiltrar produtos conforme necessario
    #
    # 2. Identificar a etapa atual do plano (primeira etapa pendente)
    #
    # 3. Filtrar catalogo:
    #    a. Filtrar por category (extraida do goal do plan)
    #    b. Filtrar por in_stock == True
    #    c. Filtrar por price_brl <= budget (se budget definido em constraints)
    #    d. Filtrar por lactose_free (se lactose_free em constraints)
    #    e. Filtrar por gluten_free (se gluten_free em constraints)
    #
    # 4. Se nao houver produtos apos filtros, retornar Generation vazia
    #    com candidate_response indicando que nao ha matches
    #
    # 5. Ordenar produtos por rating (desc) e limitar a 3 resultados
    #
    # 6. Gerar candidate_response em portugues natural:
    #    - Incluir nome do cliente (plan.known_constraints ou perfil)
    #    - Listar produtos com preco
    #    - Destacar o melhor (maior rating)
    #    - Terminar com pergunta clara
    #
    # 7. Registrar products_considered e assumptions
    #
    # 8. Retornar Generation preenchida
    pass


# ============================================================================
# EVALUATOR AGENT
# ============================================================================

def evaluator_agent(
    plan: Plan,
    generation: Generation,
    profile: CustomerProfile,
) -> Evaluation:
    """
    Evaluator Agent: valida resposta candidata contra criterios e restricoes.

    Responsabilidades:
    1. Verificar CADA criterio da rubrica do plano
    2. Verificar restricoes do perfil do cliente
    3. Verificar se ha afirmacoes sem evidencia
    4. Decidir: approved ou rejected
    5. Se rejected: fornecer feedback especifico

    Args:
        plan: Plano original com criterios de sucesso e rubrica.
        generation: Resposta candidata gerada pelo Generator.
        profile: Perfil do cliente com restricoes.

    Returns:
        Evaluation com status, resultados da rubrica e feedback (se rejeitado).

    Exemplo de output esperado (approved):
        Evaluation(
            conversation_id="conv_rafael_001",
            evaluated_step_id="s1",
            status="approved",
            rubric_results=[
                RubricResult(criterion="respeita orcamento", passed=True,
                            evidence="todos os produtos listados estao <= R$80"),
                RubricResult(criterion="respeita restricoes alimentares", passed=True,
                            evidence="todos os produtos sao lactose_free=True"),
                RubricResult(criterion="nao recomenda fora de estoque", passed=True,
                            evidence="todos os produtos tem in_stock=True"),
                RubricResult(criterion="mantem foco no objetivo", passed=True,
                            evidence="resposta menciona apenas creatina"),
                RubricResult(criterion="tom humano", passed=True,
                            evidence="resposta curta, direta, com pergunta ao final"),
            ],
        )

    Exemplo de output esperado (rejected):
        Evaluation(
            conversation_id="conv_rafael_001",
            evaluated_step_id="s1",
            status="rejected",
            rubric_results=[
                RubricResult(criterion="respeita orcamento", passed=False,
                            evidence="Creapure 150g custa R$89.90 > budget R$80"),
                ...
            ],
            feedback="Produto CREA-CREA-150 excede orcamento. Remover e refiltrar.",
        )
    """
    # TODO: Implementar o Evaluator Agent
    #
    # Algoritmo sugerido:
    # 1. Criar lista de rubric_results vazia
    #
    # 2. Para cada criterio em plan.evaluation_rubric, verificar:
    #
    #    "respeita orcamento definido no perfil":
    #       - Para cada produto em products_considered, verificar price_brl <= profile.budget_brl
    #       - Se algum exceder: failed
    #
    #    "respeita restricoes alimentares":
    #       - Se "lactose" em profile.dietary_restrictions, verificar lactose_free=True
    #       - Se "gluten" em profile.dietary_restrictions, verificar gluten_free=True
    #
    #    "nao recomenda produto fora de estoque":
    #       - Verificar in_stock=True para todos os produtos considerados
    #
    #    "mantem foco no objetivo principal":
    #       - Verificar se candidate_response menciona o current_goal
    #       - Verificar se nao faz tangentes (outras categorias alem da desejada)
    #
    #    "explica recomendacao sem pressionar compra":
    #       - Verificar se candidate_response tem explicacao
    #       - Verificar se NAO tem linguagem de pressao ("aproveite", "so hoje", "nao perca")
    #
    # 3. Se TODOS os criterios passaram: status = "approved"
    #    Se ALGUM criterio falhou: status = "rejected", feedback = explicacao do que falhou
    #
    # 4. Preencher checked_at com timestamp atual
    #
    # 5. Retornar Evaluation preenchida
    pass


# ============================================================================
# ORCHESTRATOR (HARNESS)
# ============================================================================

def run_customer_turn(
    state_dir: Path,
    event: ConversationEvent,
    profile: CustomerProfile,
    catalog: list[Product],
    max_revisions: int = 2,
) -> str:
    """
    Orquestrador principal: coordena Planner -> Generator -> Evaluator.

    Fluxo:
    1. Planner analisa evento e cria plano
    2. Generator executa etapa e gera resposta candidata
    3. Evaluator valida resposta
    4. Se aprovado: retorna resposta para o cliente
    5. Se rejeitado: Generator tenta novamente (ate max_revisions vezes)
    6. Se esgotar revisoes: retorna fallback seguro

    Args:
        state_dir: Diretorio para persistir arquivos de estado.
        event: Evento de conversa com a mensagem do cliente.
        profile: Perfil do cliente.
        catalog: Lista de produtos disponiveis.
        max_revisions: Numero maximo de tentativas de revisao (default: 2).

    Returns:
        String com a resposta final para o cliente ou fallback seguro.

    Raises:
        ValueError: Se o state_dir nao for um diretorio valido.
    """
    # TODO: Implementar o orquestrador
    #
    # Algoritmo sugerido:
    # 1. Validar que state_dir existe ou pode ser criado
    #
    # 2. Persistir conversation_event.json
    #
    # 3. Executar planner_agent() -> plan
    #    Persistir plan.json
    #
    # 4. Executar generator_agent() -> generation
    #    Persistir generation.json
    #
    # 5. Executar evaluator_agent() -> evaluation
    #    Persistir evaluation.json
    #
    # 6. Loop de revisao:
    #    revision_count = 0
    #    ENQUANTO evaluation.status != "approved" E revision_count < max_revisions:
    #        revision_count += 1
    #        generation = generator_agent(plan, catalog, evaluation.feedback)
    #        Persistir generation_revision_{n}.json
    #        evaluation = evaluator_agent(plan, generation, profile)
    #        Persistir evaluation_revision_{n}.json
    #
    # 7. Se evaluation.status == "approved":
    #        Persistir delivery.json
    #        Retornar generation.candidate_response
    #
    # 8. Senao (esgotou revisoes):
    #        Retornar mensagem de fallback seguro:
    #        "Preciso confirmar um detalhe antes de te responder com seguranca. 
    #         Posso verificar e retornar em instantes?"
    pass


# ============================================================================
# TESTS / EXEMPLOS DE USO
# ============================================================================

def setup_test_state() -> tuple[Path, CustomerProfile, list[Product]]:
    """
    Prepara ambiente de teste: cria diretorio de estado e dados de exemplo.

    Returns:
        Tupla com (state_dir, perfil_cliente, catalogo).
    """
    # Cenário: Rafael quer comprar creatina, R$ 80, intolerante a lactose
    state_dir = Path("state/conv_rafael_001")
    state_dir.mkdir(parents=True, exist_ok=True)

    profile = CustomerProfile(
        customer_id="cust_rafael_001",
        name="Rafael",
        budget_brl=80.0,
        dietary_restrictions=["intolerancia_lactose"],
        preferred_flavor="natural",
        training_goal="ganho_de_forca",
        training_frequency="5x_semana",
    )

    return state_dir, profile, PRODUCT_CATALOG


def test_cenario_1_caminho_feliz():
    """Cenario 1: recomendacao aprovada na primeira tentativa."""
    print("\\n" + "=" * 60)
    print("🧪 TESTE 1: Caminho Feliz — Recomendacao Aprovada")
    print("=" * 60)

    state_dir, profile, catalog = setup_test_state()

    event = ConversationEvent(
        conversation_id="conv_rafael_001",
        turn_id="turn_001",
        customer_message="Quero comprar creatina. Meu orcamento e R$ 80.",
    )

    # Executar o harness
    response = run_customer_turn(state_dir, event, profile, catalog)

    # Validacoes
    print(f"\\n📤 Resposta final: {response}")

    # Verificar que os arquivos foram criados
    plan_path = state_dir / "plan.json"
    gen_path = state_dir / "generation.json"
    eval_path = state_dir / "evaluation.json"

    assert plan_path.exists(), "plan.json deveria existir"
    assert gen_path.exists(), "generation.json deveria existir"
    assert eval_path.exists(), "evaluation.json deveria existir"

    # Verificar conteudo da avaliacao
    evaluation = json.loads(eval_path.read_text())
    assert evaluation["status"] == "approved", (
        f"Esperado 'approved', obtido '{evaluation['status']}'"
    )

    # Verificar que resposta nao e fallback
    assert "Preciso confirmar" not in response, (
        "Resposta nao deveria ser fallback no caminho feliz"
    )

    print("✅ Teste 1 passou!")


def test_cenario_2_rejeicao_e_correcao():
    """Cenario 2: recomendacao viola restricao, avaliador rejeita, generator corrige."""
    print("\\n" + "=" * 60)
    print("🧪 TESTE 2: Rejeicao e Correcao — Budget Excedido")
    print("=" * 60)

    state_dir = Path("state/conv_marina_002")
    state_dir.mkdir(parents=True, exist_ok=True)

    # Marina tem budget baixo — qualquer whey vai estourar
    profile = CustomerProfile(
        customer_id="cust_marina_002",
        name="Marina",
        budget_brl=50.0,  # Budget muito baixo para whey
        dietary_restrictions=["intolerancia_lactose"],
        preferred_flavor="chocolate",
        training_goal="ganho_de_massa",
        training_frequency="4x_semana",
    )

    event = ConversationEvent(
        conversation_id="conv_marina_002",
        turn_id="turn_001",
        customer_message="Quero comprar whey protein sabor chocolate.",
    )

    response = run_customer_turn(state_dir, event, profile, catalog)

    print(f"\\n📤 Resposta final: {response}")

    # Verificar que o sistema lidou com a situacao (aprovado ou fallback)
    eval_path = state_dir / "evaluation.json"
    assert eval_path.exists(), "evaluation.json deveria existir"

    evaluation = json.loads(eval_path.read_text())

    # Se approved, verificar que budget foi respeitado
    if evaluation["status"] == "approved":
        generation = json.loads((state_dir / "generation.json").read_text())
        for p in generation.get("products_considered", []):
            assert p["price_brl"] <= 50.0, (
                f"Produto {p.get('sku')} com preco {p['price_brl']} "
                f"excede budget de R$ 50.0"
            )
    # Se rejected apos 2 revisoes, fallback e aceitavel
    else:
        assert "Preciso confirmar" in response, (
            "Fallback esperado quando budget e impossivel de atender"
        )

    print("✅ Teste 2 passou!")


def test_cenario_3_fallback_apos_duas_revisoes():
    """Cenario 3: duas tentativas falham, sistema retorna fallback seguro."""
    print("\\n" + "=" * 60)
    print("🧪 TESTE 3: Fallback Apos 2 Revisoes Falhas")
    print("=" * 60)

    state_dir = Path("state/conv_pedro_003")
    state_dir.mkdir(parents=True, exist_ok=True)

    # Pedro tem restricoes contraditorias — quer whey mas so pode gastar R$ 15
    profile = CustomerProfile(
        customer_id="cust_pedro_003",
        name="Pedro",
        budget_brl=15.0,  # Nenhum produto no catalogo cabe nesse budget
        dietary_restrictions=["intolerancia_lactose", "intolerancia_gluten"],
        preferred_flavor="baunilha",
        training_goal="ganho_de_massa",
    )

    event = ConversationEvent(
        conversation_id="conv_pedro_003",
        turn_id="turn_001",
        customer_message="Quero o melhor whey protein que tiver.",
    )

    response = run_customer_turn(state_dir, event, profile, catalog, max_revisions=2)

    print(f"\\n📤 Resposta final: {response}")

    # Com budget de R$15, nenhum whey cabe — o sistema deve retornar fallback
    eval_final_path = state_dir / "evaluation.json"
    if eval_final_path.exists():
        evaluation = json.loads(eval_final_path.read_text())
        if evaluation["status"] == "rejected":
            # Deve ter retornado fallback
            assert "Preciso confirmar" in response, (
                "Fallback esperado quando budget impossivel"
            )
        # Se approved, o Generator encontrou algo (ex: BCAA de R$59.90 ainda > R$15)
        # Nesse caso, o Evaluator deve ter rejeitado e gerado fallback

    print("✅ Teste 3 passou!")


def test_cenario_4_respeito_ao_orcamento():
    """Cenario 4: sistema nunca recomenda produto acima do budget."""
    print("\\n" + "=" * 60)
    print("🧪 TESTE 4: Garantia de Respeito ao Orcamento")
    print("=" * 60)

    state_dir = Path("state/conv_ana_004")
    state_dir.mkdir(parents=True, exist_ok=True)

    # Ana tem budget de R$ 70
    profile = CustomerProfile(
        customer_id="cust_ana_004",
        name="Ana",
        budget_brl=70.0,
        dietary_restrictions=[],
        preferred_flavor="natural",
        training_goal="resistencia",
    )

    event = ConversationEvent(
        conversation_id="conv_ana_004",
        turn_id="turn_001",
        customer_message="Quero comprar creatina.",
    )

    response = run_customer_turn(state_dir, event, profile, catalog)

    print(f"\\n📤 Resposta final: {response}")

    # Carregar generation e verificar cada produto
    gen_path = state_dir / "generation.json"
    if gen_path.exists():
        generation = json.loads(gen_path.read_text())
        for p in generation.get("products_considered", []):
            assert p["price_brl"] <= 70.0, (
                f"VIOLACAO: {p.get('sku')} custa R$ {p['price_brl']} > budget R$ 70.0"
            )
        print(f"  Produtos considerados: {len(generation['products_considered'])}")
        for p in generation["products_considered"]:
            print(f"  - {p.get('sku')}: R$ {p['price_brl']}")

    print("✅ Teste 4 passou!")


def test_cenario_5_respeito_restricao_alimentar():
    """Cenario 5: sistema nunca recomenda produto com alergeno bloqueado."""
    print("\\n" + "=" * 60)
    print("🧪 TESTE 5: Garantia de Respeito a Restricao Alimentar")
    print("=" * 60)

    state_dir = Path("state/conv_bruno_005")
    state_dir.mkdir(parents=True, exist_ok=True)

    profile = CustomerProfile(
        customer_id="cust_bruno_005",
        name="Bruno",
        budget_brl=150.0,
        dietary_restrictions=["intolerancia_lactose"],
        preferred_flavor="chocolate",
        training_goal="ganho_de_massa",
    )

    event = ConversationEvent(
        conversation_id="conv_bruno_005",
        turn_id="turn_001",
        customer_message="Quero comprar whey protein.",
    )

    response = run_customer_turn(state_dir, event, profile, catalog)

    print(f"\\n📤 Resposta final: {response}")

    # Verificar que nenhum produto com lactose foi recomendado
    gen_path = state_dir / "generation.json"
    if gen_path.exists():
        generation = json.loads(gen_path.read_text())
        # Precisamos cruzar com o catalogo para verificar lactose_free
        for p in generation.get("products_considered", []):
            sku = p.get("sku")
            # Encontrar no catalogo
            product = next((prod for prod in catalog if prod.sku == sku), None)
            if product:
                assert product.lactose_free, (
                    f"VIOLACAO: {sku} nao e lactose_free, "
                    f"mas cliente tem intolerancia a lactose"
                )
        print(f"  Produtos considerados: {len(generation['products_considered'])}")
        for p in generation["products_considered"]:
            print(f"  - {p.get('sku')}: R$ {p['price_brl']}")

    print("✅ Teste 5 passou!")


def test_cenario_6_audit_trail():
    """Cenario 6: todos os arquivos JSON tem campos obrigatorios."""
    print("\\n" + "=" * 60)
    print("🧪 TESTE 6: Audit Trail — Campos Obrigatorios nos JSONs")
    print("=" * 60)

    state_dir, profile, catalog = setup_test_state()

    event = ConversationEvent(
        conversation_id="conv_rafael_001",
        turn_id="turn_006",
        customer_message="Qual a melhor creatina ate R$ 80?",
    )

    response = run_customer_turn(state_dir, event, profile, catalog)

    # Verificar plan.json
    plan_path = state_dir / "plan.json"
    assert plan_path.exists(), "plan.json nao existe"
    plan = json.loads(plan_path.read_text())
    required_plan_fields = ["schema_version", "conversation_id",
                             "current_goal", "steps", "evaluation_rubric"]
    for field in required_plan_fields:
        assert field in plan, f"plan.json: campo '{field}' ausente"
    assert len(plan["steps"]) > 0, "plan.json: steps nao pode ser vazio"
    assert len(plan["evaluation_rubric"]) > 0, "plan.json: evaluation_rubric nao pode ser vazio"

    # Verificar generation.json
    gen_path = state_dir / "generation.json"
    assert gen_path.exists(), "generation.json nao existe"
    generation = json.loads(gen_path.read_text())
    required_gen_fields = ["schema_version", "conversation_id",
                            "candidate_response", "products_considered"]
    for field in required_gen_fields:
        assert field in generation, f"generation.json: campo '{field}' ausente"
    assert len(generation["candidate_response"]) > 0, (
        "generation.json: candidate_response nao pode ser vazio"
    )

    # Verificar evaluation.json
    eval_path = state_dir / "evaluation.json"
    assert eval_path.exists(), "evaluation.json nao existe"
    evaluation = json.loads(eval_path.read_text())
    required_eval_fields = ["schema_version", "conversation_id",
                             "evaluated_step_id", "status", "rubric_results"]
    for field in required_eval_fields:
        assert field in evaluation, f"evaluation.json: campo '{field}' ausente"
    assert evaluation["status"] in ("approved", "rejected"), (
        f"status invalido: {evaluation['status']}"
    )
    assert len(evaluation["rubric_results"]) > 0, (
        "evaluation.json: rubric_results nao pode ser vazio"
    )

    print(f"\\n📁 Arquivos gerados em: {state_dir}")
    for f in sorted(state_dir.iterdir()):
        print(f"  {'📄' if f.is_file() else '📁'} {f.name}")

    print("✅ Teste 6 passou!")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("EXERCICIO 1: SISTEMA MULTI-AGENTE PLANNER/GENERATOR/EVALUATOR")
    print("=" * 60)

    # Quando implementado, descomente para testar:
    # test_cenario_1_caminho_feliz()
    # test_cenario_2_rejeicao_e_correcao()
    # test_cenario_3_fallback_apos_duas_revisoes()
    # test_cenario_4_respeito_ao_orcamento()
    # test_cenario_5_respeito_restricao_alimentar()
    # test_cenario_6_audit_trail()

    print("\\n📝 TODO: Implemente as funcoes acima!")
    print("   1. write_json / read_json / dataclass_to_dict")
    print("   2. planner_agent")
    print("   3. generator_agent")
    print("   4. evaluator_agent")
    print("   5. run_customer_turn")
    print("   Apos implementar, descomente os testes em main()")
```

---

## 🏗️ Como Comecar

### Passo 1: Implementar as Funcoes Auxiliares (15 min)

Comece pelas funcoes `write_json`, `read_json` e `dataclass_to_dict`. Sao simples, independentes e necessarias para todo o resto.

```python
def write_json(directory: Path, filename: str, data: Any) -> Path:
    import tempfile
    directory.mkdir(parents=True, exist_ok=True)
    # Escrever em arquivo temporario no mesmo diretorio
    # Garante atomicidade: ou o arquivo final existe completo, ou nao existe
    tmp_path = directory / f".{filename}.tmp"
    tmp_path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2, default=str),
        encoding="utf-8",
    )
    final_path = directory / filename
    tmp_path.rename(final_path)  # Operacao atomica no mesmo filesystem
    return final_path
```

Dica: use `asdict()` do modulo `dataclasses` para converter dataclasses em dicionarios. Para listas, itere e converta cada elemento.

### Passo 2: Implementar o Planner Agent (15 min)

O Planner e o agente mais conceitual. Foque em:

1. **Analisar a mensagem:** procure por palavras-chave como "creatina", "whey", "pre treino", "bcaa" no texto da mensagem do cliente (use `.lower()` para case-insensitive). Se nenhuma for encontrada, assuma categoria "todos".

2. **Extrair restricoes do perfil:**
   - `budget_brl` = `profile.budget_brl`
   - `lactose_free` = `True` se qualquer string em `profile.dietary_restrictions` contiver "lactose"
   - `gluten_free` = `True` se qualquer string contiver "gluten"

3. **Criar 3 etapas (PlanStep):**
   - `s1`: Filtrar produtos da categoria desejada, verificar estoque
   - `s2`: Aplicar restricoes de budget, lactose, gluten
   - `s3`: Preparar resposta final em portugues natural

4. **Definir rubrica:** 5 criterios (orcamento, restricoes, estoque, foco, tom humano)

### Passo 3: Implementar o Generator Agent (20 min)

O Generator faz a parte pesada de filtragem de dados:

1. **Identificar a categoria alvo:** extraia do `current_goal` do plano. Ex: se `current_goal` contem "creatina", filtre `product.category == "creatina"`.

2. **Aplicar filtros em cadeia:**
   ```python
   filtered = catalog
   # Filtrar por categoria
   if target_category != "todos":
       filtered = [p for p in filtered if p.category == target_category]
   # Filtrar por estoque
   filtered = [p for p in filtered if p.in_stock]
   # Filtrar por budget
   if plan.known_constraints.get("budget_brl"):
       budget = plan.known_constraints["budget_brl"]
       filtered = [p for p in filtered if p.price_brl <= budget]
   # Filtrar por lactose
   if plan.known_constraints.get("lactose_free"):
       filtered = [p for p in filtered if p.lactose_free]
   # Filtrar por gluten
   if plan.known_constraints.get("gluten_free"):
       filtered = [p for p in filtered if p.gluten_free]
   ```

3. **Ordenar e limitar:** ordene por `rating` decrescente, mantenha no maximo 3.

4. **Gerar resposta natural:**
   ```python
   if not filtered:
       response = f"{profile.name}, nao encontrei produtos que atendam todos os seus criterios. "
       response += "Quer ajustar alguma preferencia?"
   else:
       best = filtered[0]
       response = f"{profile.name}, encontrei {len(filtered)} opcoes. "
       response += f"A melhor e {best.name} por R$ {best.price_brl:.2f} "
       response += f"(nota {best.rating}). "
       if len(filtered) > 1:
           response += f"Tambem temos {filtered[1].name} por R$ {filtered[1].price_brl:.2f}. "
       response += "Qual prefere?"
   ```

5. Se estiver em modo revisao (`evaluator_feedback` existe), refaca a filtragem corrigindo o problema apontado.

### Passo 4: Implementar o Evaluator Agent (20 min)

O Evaluator e deterministico — sem LLM, pura logica de validacao:

1. **Iterar sobre `plan.evaluation_rubric`** — para cada criterio, implementar uma verificacao:

   | Criterio | Como Verificar |
   |----------|---------------|
   | "respeita orcamento" | Para cada produto em `products_considered`, verificar `price_brl <= profile.budget_brl` |
   | "respeita restricoes alimentares" | Verificar `lactose_free` e `gluten_free` conforme `profile.dietary_restrictions` |
   | "nao recomenda fora de estoque" | Para cada produto, verificar `in_stock == True` |
   | "mantem foco no objetivo" | Verificar se `candidate_response` nao menciona categorias diferentes da `current_goal` |
   | "explica sem pressionar" | Verificar ausencia de palavras de pressao: "aproveite", "so hoje", "nao perca", "ultimas unidades" |

2. **Decidir status:**
   ```python
   all_passed = all(r.passed for r in rubric_results)
   status = "approved" if all_passed else "rejected"
   feedback = "" if all_passed else "Criterios que falharam: " + ", ".join(
       r.criterion for r in rubric_results if not r.passed
   )
   ```

### Passo 5: Implementar o Orquestrador (15 min)

O `run_customer_turn` conecta tudo:

1. Persistir `conversation_event.json`
2. Chamar `planner_agent()` → persistir `plan.json`
3. Chamar `generator_agent()` → persistir `generation.json`
4. Chamar `evaluator_agent()` → persistir `evaluation.json`
5. Loop de revisao (ate `max_revisions`):
   - Se `rejected`: chamar `generator_agent()` com `evaluator_feedback`
   - Persistir `generation_revision_{n}.json`
   - Re-avaliar
6. Retornar resposta aprovada ou fallback

### Passo 6: Testar (5 min)

Descomente os 6 cenarios de teste em `main()` e execute:
```bash
python exercise-01.py
```

Todos os testes devem passar com ✅.

---

## 📊 Estrategias de Coordenacao: Tabela Comparativa

O sistema que voce construiu usa coordenacao **sequencial**. Mas existem outras estrategias. Aqui esta a comparacao:

| Estrategia | Fluxo | Vantagens | Desvantagens | Quando Usar no KODA |
|------------|-------|-----------|--------------|---------------------|
| **Sequencial** | Planner → Generator → Evaluator | Simples de implementar, auditavel, facil de debugar, cada etapa tem dono claro | Maior latencia total (cada etapa espera a anterior), nao escala para multiplas recomendacoes simultaneas | Recomendacao com risco alimentar, fechamento de pedido, qualquer cenario onde erro custa caro |
| **Paralelo** | Planner cria subtarefas, varios Generators executam ao mesmo tempo, Evaluator agrega | Reduz latencia visivel, explora alternativas simultaneas, bom para comparacao | Exige agregacao cuidadosa, risco de resultados inconsistentes, mais complexo de debugar | Comparar produtos, frete e preco em paralelo; cliente quer ver "todas as opcoes rapidamente" |
| **Event-driven** | Agentes reagem a mudancas de estado (ex: pagamento aprovado dispara Fulfillment Agent) | Bom para jornadas longas (horas/dias), desacopla componentes, permite retomada apos falha | Mais dificil de observar o fluxo completo, exige governanca de eventos, state deve ser fonte da verdade | Atualizacao de estoque em tempo real, abandono de carrinho com follow-up, pagamento aprovado → tracking |

### Sinais de que voce deve mudar de estrategia:

- **Sequencial → Paralelo:** Quando o cliente pergunta "compara todas as opcoes" e a latencia comeca a incomodar
- **Paralelo → Event-driven:** Quando a jornada continua depois que o cliente sai do WhatsApp (ex: callback de pagamento)
- **Event-driven → Sequencial:** Quando o fluxo esta confuso demais, ninguem sabe o que dispara o que, e e hora de simplificar

### Regra Pratica para KODA:

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│  Comece SEMPRE sequencial.                                       │
│                                                                  │
│  So paralelize tarefas comprovadamente independentes.            │
│                                                                  │
│  Use event-driven apenas para jornadas que sobrevivem            │
│  alem do turno atual da conversa.                                │
│                                                                  │
│  Se nao consegue explicar o beneficio em 1 frase,                │
│  a estrategia mais simples e a correta.                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔧 Aplicacao KODA: Da Teoria a Producao

O exercicio que voce implementou e uma versao simplificada do que o KODA real usa em producao. Aqui esta como cada componente evolui:

### O Que Voce Implementou (Curriculo)

| Componente | Implementacao |
|------------|--------------|
| Catalogo | Lista hardcoded de 8 produtos em Python |
| State Store | Arquivos JSON em `state/<conversation_id>/` |
| Planner | Funcao pura que analisa mensagem e cria plano |
| Generator | Funcao pura que filtra catalogo e gera texto |
| Evaluator | Funcao pura que valida contra rubrica |
| Orquestrador | Funcao `run_customer_turn()` que encadeia chamadas |

### O Que o KODA Real Usa (Producao)

| Componente | Evolucao |
|------------|----------|
| Catalogo | API REST que consulta banco de dados real com 2000+ SKUs, precos dinamicos e estoque em tempo real |
| State Store | Redis para cache rapido + PostgreSQL para persistencia duravel. Diretorio `state/` vira bucket S3/MinIO para auditoria |
| Planner | Prompt engineering avancado com few-shot examples. Contexto inclui historico de compras, sazonalidade e perfil nutricional |
| Generator | Agente que consulta 3 APIs em paralelo: catalogo, preco, frete. Resposta passa por template engine antes de chegar ao Evaluator |
| Evaluator | Rubrica com 15+ criterios incluindo tom de voz, conformidade legal (ANVISA), pricing minimo e checagem de cross-selling etico |
| Orquestrador | Event-driven com RabbitMQ. Cada agente e um consumer independente. Handoffs sao eventos, nao chamadas diretas de funcao |

### O Que NAO Muda

Apesar da diferenca de escala, os principios sao os mesmos:

1. **Separacao de responsabilidades:** Planner, Generator e Evaluator continuam sendo entidades distintas, mesmo que cada um seja um servico separado
2. **State como contrato:** `plan.json`, `generation.json`, `evaluation.json` viram mensagens em fila, mas a estrutura e o contrato permanecem
3. **Avaliacao independente:** O Evaluator nunca e o Generator. Sycophancy continua sendo combatida por design
4. **Audit trail:** Todo estado e persistido, permitindo replay e debug de qualquer conversa
5. **Fallback seguro:** Se o sistema nao consegue aprovar uma resposta apos N tentativas, ele admite que precisa de ajuda humana

### Exemplo Real: Trace de uma Conversa KODA em Producao

```
state/conv_2026_05_26_marina/
├── 01_inbound_message.json          # "Quero comprar whey, R$ 220, intolerante a lactose"
├── 02_welcome_response.json         # Welcome Agent: saudacao e intencao
├── 03_customer_needs.json           # Discovery Agent: objetivo, restricoes, budget
├── 04_plan.json                     # Planner: "recomendar whey isolado sem lactose"
├── 05_generation.json               # Generator: Whey Isolado Chocolate R$199.90
├── 06_evaluation.json               # Evaluator: APPROVED (budget OK, lactose OK, em estoque)
├── 07_recommendation_set.json       # Recommendation Agent: produto principal + alternativa
├── 08_order_draft.json              # Order Agent: pedido montado, aguardando pagamento
├── 09_payment_approved.json         # Evento externo: pagamento confirmado
├── 10_fulfillment_plan.json         # Fulfillment Agent: tracking e pos-venda
└── 11_delivery.json                 # Resposta final enviada ao cliente
```

Cada arquivo e um checkpoint. Se o cliente reclamar amanha, a equipe abre esse diretorio e sabe exatamente o que aconteceu, quando e por que.

---

## 🎯 Desafios Extra (Opcional)

Se terminar o exercicio base antes do tempo, implemente um ou mais destes desafios:

### Desafio 1: Estrategia Paralela

Modifique o orquestrador para que, quando o plano tiver multiplas etapas independentes, o Generator execute-as em paralelo usando `concurrent.futures.ThreadPoolExecutor`. O Evaluator deve agregar todos os resultados antes de decidir.

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def run_parallel_generators(plan: Plan, catalog: list[Product]) -> list[Generation]:
    """Executa cada step do plano em paralelo e coleta resultados."""
    # TODO: Implementar
    pass
```

### Desafio 2: Metricas de Qualidade

Implemente um sistema de metricas que mede:
- **Precisao de orcamento:** % de recomendacoes que respeitam o budget
- **Precisao de restricao:** % de recomendacoes que respeitam alergias
- **Taxa de aprovacao:** % de geracoes aprovadas na primeira tentativa
- **Latencia media:** tempo entre mensagem do cliente e resposta final

```python
@dataclass
class QualityMetrics:
    budget_accuracy: float       # 0.0 a 1.0
    restriction_accuracy: float  # 0.0 a 1.0
    first_try_approval_rate: float
    avg_latency_ms: float

def compute_metrics(conversation_logs: list[Path]) -> QualityMetrics:
    """Calcula metricas a partir dos arquivos de estado de varias conversas."""
    # TODO: Implementar
    pass
```

### Desafio 3: Persistencia em SQLite

Substitua os arquivos JSON por um banco SQLite. Cada agente escreve em tabelas normalizadas em vez de arquivos soltos.

```python
import sqlite3

class StateDB:
    """Gerencia estado de conversas em SQLite."""
    
    def __init__(self, db_path: str = "koda_state.db"):
        self.conn = sqlite3.connect(db_path)
        self._create_tables()
    
    def _create_tables(self):
        """Cria tabelas: conversations, plans, generations, evaluations."""
        # TODO: Implementar schema
        pass
    
    def save_plan(self, plan: Plan) -> int:
        """Insere plano e retorna ID."""
        # TODO: Implementar
        pass
```

### Desafio 4: Integracao com Claude API (Simulada)

Adapte o Generator para usar uma chamada real a API do Claude em vez de gerar texto deterministico. Para nao depender de rede, implemente um mock que retorna respostas pre-definidas baseadas no input.

```python
def generator_with_claude(plan: Plan, catalog: list[Product]) -> Generation:
    """
    Versao do Generator que usa Claude para gerar a resposta natural.
    Em producao, isso chamaria a API anthropic.
    Para o exercicio, implemente um mock deterministico.
    """
    # TODO: Implementar mock da API Claude
    pass
```

---

## 📊 Checklist de Implementacao

- [ ] Funcao `write_json` implementada (escrita atomica com tempfile)
- [ ] Funcao `read_json` implementada
- [ ] Funcao `dataclass_to_dict` implementada (suporta dataclasses, listas, dicts aninhados)
- [ ] Funcao `planner_agent` implementada (analisa mensagem, extrai categoria, cria 3 steps)
- [ ] Funcao `generator_agent` implementada (filtra catalogo, gera resposta natural)
- [ ] Funcao `evaluator_agent` implementada (valida rubrica, decide approved/rejected)
- [ ] Funcao `run_customer_turn` implementada (orquestra fluxo completo com loop de revisao)
- [ ] Cenario 1 (caminho feliz) passa ✅
- [ ] Cenario 2 (rejeicao + correcao) passa ✅
- [ ] Cenario 3 (fallback apos 2 revisoes) passa ✅
- [ ] Cenario 4 (respeito ao orcamento) passa ✅
- [ ] Cenario 5 (respeito a restricao alimentar) passa ✅
- [ ] Cenario 6 (audit trail) passa ✅
- [ ] Todos os type hints estao corretos (verificar com `mypy` se disponivel)
- [ ] Codigo segue PEP 8 (verificar com `flake8` ou `ruff` se disponivel)

---

## 💡 Dicas de Implementacao

**Dica 1:** Comece pelas funcoes auxiliares. `write_json` e `read_json` sao usadas por todo o sistema. Se estiverem corretas, o resto flui.

**Dica 2:** O Planner nao precisa de NLP avancado. Use `if "creatina" in mensagem.lower()` para detectar a categoria. E simples, deterministico e suficiente para o exercicio.

**Dica 3:** O Generator deve sempre verificar `in_stock` antes de recomendar. Produto fora de estoque = nao aparece na resposta. Periodo.

**Dica 4:** O Evaluator e o coracao da seguranca. Gaste tempo extra aqui. Cada criterio da rubrica deve ter uma verificacao objetiva. Nada de "parece bom". SEMPRE verifique com comparacoes concretas: `price_brl <= budget_brl`, `lactose_free == True`.

**Dica 5:** No loop de revisao, o Generator recebe `evaluator_feedback`. Use esse feedback para re-filtrar produtos. Ex: se o feedback diz "orcamento excedido", re-filtre removendo produtos acima do budget.

**Dica 6:** Teste com `max_window_messages` pequeno ou budget impossivel para ver o fallback em acao rapidamente. Ex: `budget_brl=1.0` força fallback em qualquer cenario.

**Dica 7:** Os arquivos JSON sao seu audit trail. Se algo falhar, abra `state/<id>/evaluation.json` e leia o campo `rubric_results` — ele diz exatamente qual criterio falhou e por que.

**Dica 8:** Mantenha as respostas curtas. WhatsApp e um meio de mensagens rapidas. Respostas longas (5+ linhas) parecem roboticas. O Evaluator pode verificar `len(candidate_response) < 500` como criterio extra.

---

## ✅ Validacao Final

Sua implementacao esta correta se:

1. ✅ Todos os 6 cenarios de teste passam
2. ✅ Nenhum produto acima do budget aparece em `products_considered`
3. ✅ Nenhum produto com alergeno bloqueado aparece em `products_considered`
4. ✅ `plan.json` tem pelo menos 1 step e 5 criterios de rubrica
5. ✅ `generation.json` tem `candidate_response` e `products_considered` preenchidos
6. ✅ `evaluation.json` tem `status` valido e `rubric_results` com evidencias
7. ✅ Fallback e retornado quando 2 revisoes falham
8. ✅ Codigo tem type hints em todas as funcoes publicas
9. ✅ Nao ha `except: pass` vazio ou `# type: ignore`
10. ✅ Todos os arquivos JSON incluem `schema_version`, `conversation_id` e timestamp

---

## 🎓 O Que Voce Aprendeu

Apos completar este exercicio, voce entende na pratica:

- ✅ **Por que separar responsabilidades:** Planner, Generator e Evaluator como entidades distintas, cada uma com ownership claro e criterios de sucesso definidos

- ✅ **File-based coordination:** Como usar arquivos JSON como contrato entre agentes — simples, auditavel e suficiente para ambientes de aprendizado e prototipos

- ✅ **Orquestracao com loop de revisao:** Como implementar um harness que detecta falhas, fornece feedback e re-tenta com limite maximo de tentativas

- ✅ **Validacao deterministica:** Como o Evaluator aplica criterios objetivos (preco, estoque, alergenos) sem depender de outro LLM para julgar qualidade

- ✅ **Fallback seguro:** Como projetar um sistema que, quando nao consegue gerar uma resposta segura, admite limitacao em vez de arriscar uma resposta errada

- ✅ **Audit trail:** Como cada decisao e registrada em arquivos versionaveis, permitindo debugar qualquer conversa meses depois

- ✅ **Estrategias de coordenacao:** Quando usar sequencial, paralelo ou event-driven, e como a escolha impacta latencia, complexidade e confiabilidade

- ✅ **Evolucao para producao:** Como o que voce implementou (funcoes puras + JSON) evolui naturalmente para filas, APIs e bancos de dados quando o sistema escala

- ✅ **Design anti-overengineering:** Que multi-agente nao e resposta para tudo — so faz sentido quando o beneficio da separacao supera o custo da complexidade adicional

---

## 📚 Referencias & Proximas Leituras

- `curriculum/03-nivel-3-advanced-architecture/01-multi-agent-systems.md` — Teoria completa de sistemas multi-agente com KODA
- `curriculum/02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md` — Base Generator/Evaluator que este exercicio expande
- `curriculum/03-nivel-3-advanced-architecture/02-state-persistence.md` — Como estado externo sustenta agentes em jornadas longas
- `curriculum/03-nivel-3-advanced-architecture/03-file-based-coordination.md` — Aprofundamento em contratos por arquivos JSON
- `curriculum/03-nivel-3-advanced-architecture/05-harness-evolution.md` — Como o harness cresce sem virar caos

**Proximo exercicio:** `exercise-02.md` — Implementar State Persistence com Compaction

---

*Exercicio 1 | Nivel 3 — Arquitetura Avancada | Curso Long-Running Agents | FutanBear Technical Program*

**Boa sorte! Ao final deste exercicio, voce tera construido o coracao arquitetural que separa um chatbot simples de um sistema confiavel.** 🚀
