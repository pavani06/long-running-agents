---
title: "Exercicio: Implementar Behavioral Eval Path Analysis (Layer 3)"
type: exercise
level: "N3"
aliases: ["behavioral eval exercise", "path analysis exercise", "duplicate detection exercise", "loop detection exercise", "wrong path right answer exercise", "tool call analysis"]
tags: [curriculo-conteudo, evals, agentes-orquestracao, production]
duration: "2-3h"
relates-to:
  - "[[docs/analysis/2026-06-26-the-production-ai-playbook-deploying-agents-at-enterprise-sc/2026-06-26-the-production-ai-playbook-deploying-agents-at-enterprise-sc-patterns|Bhaumik Patterns §5]]"
  - "[[docs/analysis/2026-06-26-the-production-ai-playbook-deploying-agents-at-enterprise-sc/2026-06-26-the-production-ai-playbook-deploying-agents-at-enterprise-sc-classification|Pattern Classification]]"
  - "[[docs/canonical/trace-instrumentation|Trace Instrumentation]]"
  - "[[docs/canonical/eval-tier-stratification|Eval Tier Stratification]]"
  - "[[docs/canonical/deterministic-tool-dispatch|Deterministic Tool Dispatch]]"
  - "[[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]]"
  - "[[.opencode/skills/behavioral-eval-path-analysis/SKILL|Behavioral Eval Path Analysis Skill]]"
  - "[[.opencode/skills/quality-improvement-loop/SKILL|Quality Improvement Loop]]"
last_updated: 2026-06-26
---
# Exercicio: Implementar Behavioral Eval Path Analysis (Layer 3)

## Nivel 3 — Arquitetura Avancada

## Objetivo

Implementar um sistema de analise comportamental de traces de execucao de agentes — o Layer 3 da arquitetura de avaliacao em 3 camadas. Voce vai construir detectores de duplicatas, loops, uso incorreto de ferramentas, e atribuicao de custo por query.

**Tempo Estimado:** 2-3 horas
**Dificuldade:** Avancado
**Pre-requisito:** Ter lido `[[docs/canonical/trace-instrumentation|Trace Instrumentation]]`, `[[docs/canonical/deterministic-tool-dispatch|Deterministic Tool Dispatch]]` e `[[docs/canonical/eval-tier-stratification|Eval Tier Stratification]]`
**Objetivo:** Implementar `DuplicateDetector`, `LoopDetector`, `ToolDispatchValidator`, `CostAttributor` e o pipeline `BehavioralEvalPipeline` que consome spans de trace e gera um relatorio de behavioral eval.

---

## Prologo: O Agente Que Custava 5x Mais Que o Necessario

### Quinta-feira, 14h20. Reuniao de custos.

```
CFO: "O budget de infra do agente KODA triplicou este mes.
      O time de engenharia diz que o agente esta funcionando
      perfeitamente — respostas corretas, clientes satisfeitos.
      Entao por que o custo por query subiu de R$ 0,08 para
      R$ 0,34?"

ENG LEAD: "As respostas estao corretas. Os clientes estao felizes.
          Nao recebemos nenhum report de erro."

SRE: (projeta tela) "Deixa eu mostrar os traces da ultima hora..."

TRACE — QUERY TIPICA DE SALDO:
  tool_call #1: db_query("SELECT balance FROM accounts WHERE id=123")    → R$ 1.234,56
  tool_call #2: db_query("SELECT balance FROM accounts WHERE id=123")    → R$ 1.234,56
  tool_call #3: db_query("SELECT balance FROM accounts WHERE id=123")    → R$ 1.234,56
  tool_call #4: api_call("payment-gateway", "/accounts/123")            → R$ 1.234,56
  tool_call #5: sub_agent("verify-balance", account_id=123)             → R$ 1.234,56
  tool_call #6: db_query("SELECT * FROM accounts WHERE id=123")         → {...todos os campos...}

  RESPOSTA: "Seu saldo e R$ 1.234,56" ✓ CORRETO!

CFO: "..."
ENG LEAD: "..."
SRE: "6 chamadas para pegar UM dado que precisa de UMA chamada.
      O avaliador semantico diz 'aprovado, resposta correta'.
      O avaliador comportamental diria 'REPROVADO — 6x o custo necessario'."
```

O postmortem revelou que ninguem estava olhando para o **caminho** que o agente percorria — so para a **resposta final**. O agente passava em todos os testes semanticos e de formato. Mas cada query custava 5x mais do que deveria. Com 80.000 queries/mes, o desperdicio era de R$ 20.800 mensais.

```
═══════════════════════════════════════════════════════════════
        POSTMORTEM — INCIDENTE DE CUSTO #KODA-042
═══════════════════════════════════════════════════════════════

QUERIES ANALISADAS: 1.000 (amostra de 1h)
QUERIES COM DUPLICATAS: 340 (34%)
QUERIES COM LOOPS: 47 (4.7%)
QUERIES COM FERRAMENTA INCORRETA: 112 (11.2%)
CUSTO TOTAL OBSERVADO: R$ 340,00/hora
CUSTO TOTAL OTIMO: R$ 68,00/hora (apenas as chamadas necessarias)
DESPERDICIO: R$ 272,00/hora = R$ 6.528/dia = R$ 195.840/mes

CAUSA RAIZ:
  O pipeline de avaliacao so tinha Layer 1 (formato/PII) e
  Layer 2 (semantico). O Layer 3 — behavioral eval — nao existia.
  O agente evoluiu para um padrao de "peca desculpas em vez de
  pedir permissao" com tool calls: chamava tudo que podia e
  filtrava depois. O resultado final era correto, o caminho
  era um desastre financeiro.
═══════════════════════════════════════════════════════════════
```

```
ARQUITETA (post-mortem): "O problema e de avaliacao. Nosso sistema
                          de testes mede SE a resposta esta certa,
                          nao COMO o agente chegou ate ela. O que
                          faltava: Behavioral Eval Path Analysis —
                          um detector que analisa a sequencia de
                          tool calls e sinaliza duplicatas, loops,
                          ferramentas erradas e custo excessivo.
                          Sem isso, o agente pode estar queimando
                          dinheiro e ninguem vai notar."
```

**O que teria evitado tudo:**

> Behavioral Eval Path Analysis (Layer 3): dados os spans de trace de uma execucao, detectar chamadas duplicadas (mesma tool + mesmos parametros), loops (ciclos A→B→A sem informacao nova), uso de ferramenta incorreta (API externa quando DB local bastaria), e atribuir custo real em dolares a cada query. O resultado: um score comportamental que complementa o score semantico, revelando o "wrong path, right answer" que as outras camadas de avaliacao nao enxergam.

**Sua missao:** Construir o `BehavioralEvalPipeline` que implementa exatamente essa analise.

---

## Cenario: Auditoria Comportamental do Agente KODA

### Contexto

Voce e o engenheiro de plataforma responsavel pela qualidade do agente KODA na **MercuryPay**. O CFO acabou de aprovar um budget extra para infraestrutura de agentes, mas com uma condicao: **todo mes, o time de engenharia deve apresentar um relatorio de behavioral eval mostrando que o custo por query esta dentro do esperado.**

O time de SRE te entrega um dump de 30 spans de trace de uma sessao tipica do agente KODA. Sua tarefa e construir o pipeline que analisa esses spans e gera o relatorio comportamental.

### Dados de Entrada

Voce recebe 30 spans de trace de uma sessao do agente KODA processando queries de clientes. Cada span representa uma tool call ou delegacao:

```json
[
  {
    "span_id": "span_001",
    "session_id": "ses_koda_20260626",
    "tool_name": "db_query",
    "params": {"query": "SELECT balance FROM accounts WHERE id=123", "db": "postgres-main"},
    "timestamp": "2026-06-26T14:30:01Z",
    "duration_ms": 45,
    "success": true,
    "tokens": 120,
    "category": "simple-lookup"
  },
  {
    "span_id": "span_002",
    "tool_name": "db_query",
    "params": {"query": "SELECT balance FROM accounts WHERE id=123", "db": "postgres-main"},
    "timestamp": "2026-06-26T14:30:02Z",
    "duration_ms": 42,
    "success": true,
    "tokens": 120,
    "category": "simple-lookup"
  },
  {
    "span_id": "span_003",
    "tool_name": "db_query",
    "params": {"query": "SELECT balance FROM accounts WHERE id=123", "db": "postgres-main"},
    "timestamp": "2026-06-26T14:30:03Z",
    "duration_ms": 44,
    "success": true,
    "tokens": 120,
    "category": "simple-lookup"
  },
  {
    "span_id": "span_004",
    "tool_name": "api_call",
    "params": {"endpoint": "/accounts/123", "provider": "payment-gateway"},
    "timestamp": "2026-06-26T14:30:04Z",
    "duration_ms": 230,
    "success": true,
    "tokens": 250,
    "category": "simple-lookup"
  },
  {
    "span_id": "span_005",
    "tool_name": "sub_agent",
    "params": {"agent": "verify-balance", "args": {"account_id": 123}},
    "timestamp": "2026-06-26T14:30:05Z",
    "duration_ms": 3200,
    "success": true,
    "tokens": 1500,
    "category": "simple-lookup"
  },
  {
    "span_id": "span_006",
    "tool_name": "db_query",
    "params": {"query": "SELECT * FROM accounts WHERE id=123", "db": "postgres-main"},
    "timestamp": "2026-06-26T14:30:08Z",
    "duration_ms": 55,
    "success": true,
    "tokens": 450,
    "category": "simple-lookup"
  },
  {
    "span_id": "span_007",
    "tool_name": "db_query",
    "params": {"query": "SELECT id, name, price FROM products WHERE category='suplementos'", "db": "postgres-main"},
    "timestamp": "2026-06-26T14:30:15Z",
    "duration_ms": 80,
    "success": true,
    "tokens": 350,
    "category": "search"
  },
  {
    "span_id": "span_008",
    "tool_name": "search_tool",
    "params": {"query": "suplementos whey protein", "index": "products"},
    "timestamp": "2026-06-26T14:30:16Z",
    "duration_ms": 120,
    "success": true,
    "tokens": 200,
    "category": "search"
  },
  {
    "span_id": "span_009",
    "tool_name": "search_tool",
    "params": {"query": "suplementos whey protein", "index": "products"},
    "timestamp": "2026-06-26T14:30:17Z",
    "duration_ms": 115,
    "success": true,
    "tokens": 200,
    "category": "search"
  },
  {
    "span_id": "span_010",
    "tool_name": "db_query",
    "params": {"query": "SELECT id, name, price FROM products WHERE category='suplementos'", "db": "postgres-main"},
    "timestamp": "2026-06-26T14:30:18Z",
    "duration_ms": 82,
    "success": true,
    "tokens": 350,
    "category": "search"
  },
  {
    "span_id": "span_011",
    "tool_name": "search_tool",
    "params": {"query": "suplementos whey protein", "index": "products"},
    "timestamp": "2026-06-26T14:30:19Z",
    "duration_ms": 118,
    "success": true,
    "tokens": 200,
    "category": "search"
  },
  {
    "span_id": "span_012",
    "tool_name": "llm_call",
    "params": {"prompt": "Resuma os resultados de busca", "model": "deepseek-v4"},
    "timestamp": "2026-06-26T14:30:20Z",
    "duration_ms": 1800,
    "success": true,
    "tokens": 800,
    "category": "search"
  },
  {
    "span_id": "span_013",
    "tool_name": "search_tool",
    "params": {"query": "whey protein isolado 1kg", "index": "products"},
    "timestamp": "2026-06-26T14:30:25Z",
    "duration_ms": 130,
    "success": true,
    "tokens": 220,
    "category": "search"
  },
  {
    "span_id": "span_014",
    "tool_name": "search_tool",
    "params": {"query": "whey protein isolado 1kg", "index": "products"},
    "timestamp": "2026-06-26T14:30:26Z",
    "duration_ms": 125,
    "success": true,
    "tokens": 220,
    "category": "search"
  },
  {
    "span_id": "span_015",
    "tool_name": "api_call",
    "params": {"endpoint": "/products/search", "provider": "external-catalog"},
    "timestamp": "2026-06-26T14:30:27Z",
    "duration_ms": 350,
    "success": true,
    "tokens": 400,
    "category": "search"
  },
  {
    "span_id": "span_016",
    "tool_name": "search_tool",
    "params": {"query": "whey protein isolado 1kg", "index": "products"},
    "timestamp": "2026-06-26T14:30:29Z",
    "duration_ms": 122,
    "success": true,
    "tokens": 220,
    "category": "search"
  },
  {
    "span_id": "span_017",
    "tool_name": "db_query",
    "params": {"query": "SELECT id, name, price, stock FROM products WHERE name ILIKE '%whey%'", "db": "postgres-main"},
    "timestamp": "2026-06-26T14:30:30Z",
    "duration_ms": 90,
    "success": true,
    "tokens": 400,
    "category": "search"
  },
  {
    "span_id": "span_018",
    "tool_name": "llm_call",
    "params": {"prompt": "Recomende o melhor whey protein", "model": "deepseek-v4"},
    "timestamp": "2026-06-26T14:30:32Z",
    "duration_ms": 2100,
    "success": true,
    "tokens": 950,
    "category": "search"
  },
  {
    "span_id": "span_019",
    "tool_name": "db_query",
    "params": {"query": "SELECT * FROM orders WHERE customer_id=456 ORDER BY created_at DESC LIMIT 5", "db": "postgres-main"},
    "timestamp": "2026-06-26T14:30:40Z",
    "duration_ms": 70,
    "success": true,
    "tokens": 300,
    "category": "multi-step-reasoning"
  },
  {
    "span_id": "span_020",
    "tool_name": "db_query",
    "params": {"query": "SELECT * FROM orders WHERE customer_id=456 ORDER BY created_at DESC LIMIT 5", "db": "postgres-main"},
    "timestamp": "2026-06-26T14:30:41Z",
    "duration_ms": 68,
    "success": true,
    "tokens": 300,
    "category": "multi-step-reasoning"
  },
  {
    "span_id": "span_021",
    "tool_name": "llm_call",
    "params": {"prompt": "Analise o historico de pedidos", "model": "deepseek-v4"},
    "timestamp": "2026-06-26T14:30:43Z",
    "duration_ms": 2500,
    "success": true,
    "tokens": 1100,
    "category": "multi-step-reasoning"
  },
  {
    "span_id": "span_022",
    "tool_name": "db_query",
    "params": {"query": "SELECT * FROM orders WHERE customer_id=456 ORDER BY created_at DESC LIMIT 5", "db": "postgres-main"},
    "timestamp": "2026-06-26T14:30:46Z",
    "duration_ms": 72,
    "success": true,
    "tokens": 300,
    "category": "multi-step-reasoning"
  },
  {
    "span_id": "span_023",
    "tool_name": "api_call",
    "params": {"endpoint": "/customers/456/preferences", "provider": "crm"},
    "timestamp": "2026-06-26T14:30:48Z",
    "duration_ms": 400,
    "success": true,
    "tokens": 500,
    "category": "multi-step-reasoning"
  },
  {
    "span_id": "span_024",
    "tool_name": "sub_agent",
    "params": {"agent": "recommend-products", "args": {"customer_id": 456}},
    "timestamp": "2026-06-26T14:30:50Z",
    "duration_ms": 4500,
    "success": true,
    "tokens": 2000,
    "category": "multi-step-reasoning"
  },
  {
    "span_id": "span_025",
    "tool_name": "db_query",
    "params": {"query": "SELECT * FROM orders WHERE customer_id=456 ORDER BY created_at DESC LIMIT 5", "db": "postgres-main"},
    "timestamp": "2026-06-26T14:30:55Z",
    "duration_ms": 69,
    "success": true,
    "tokens": 300,
    "category": "multi-step-reasoning"
  },
  {
    "span_id": "span_026",
    "tool_name": "llm_call",
    "params": {"prompt": "Gere recomendacoes finais", "model": "deepseek-v4"},
    "timestamp": "2026-06-26T14:30:58Z",
    "duration_ms": 2200,
    "success": true,
    "tokens": 1000,
    "category": "multi-step-reasoning"
  },
  {
    "span_id": "span_027",
    "tool_name": "db_query",
    "params": {"query": "UPDATE orders SET status='confirmed' WHERE id=789", "db": "postgres-main"},
    "timestamp": "2026-06-26T14:31:05Z",
    "duration_ms": 35,
    "success": true,
    "tokens": 80,
    "category": "transactional"
  },
  {
    "span_id": "span_028",
    "tool_name": "api_call",
    "params": {"endpoint": "/orders/789/confirm", "provider": "payment-gateway"},
    "timestamp": "2026-06-26T14:31:06Z",
    "duration_ms": 500,
    "success": true,
    "tokens": 300,
    "category": "transactional"
  },
  {
    "span_id": "span_029",
    "tool_name": "db_query",
    "params": {"query": "UPDATE orders SET status='confirmed' WHERE id=789", "db": "postgres-main"},
    "timestamp": "2026-06-26T14:31:07Z",
    "duration_ms": 38,
    "success": true,
    "tokens": 80,
    "category": "transactional"
  },
  {
    "span_id": "span_030",
    "tool_name": "api_call",
    "params": {"endpoint": "/notifications/send", "provider": "notification-service"},
    "timestamp": "2026-06-26T14:31:08Z",
    "duration_ms": 180,
    "success": true,
    "tokens": 150,
    "category": "transactional"
  }
]
```

**Categorias de query presentes neste trace:**

| Categoria | Spans | Template esperado |
|-----------|-------|-------------------|
| `simple-lookup` | span_001 a span_006 | 1× `db_query` (max 2 calls) |
| `search` | span_007 a span_018 | 1-3× `search_tool` ou `db_query` + 1× `llm_call` (max 5 calls) |
| `multi-step-reasoning` | span_019 a span_026 | N× `db_query` + 1× `llm_call` (max N+3 calls) |
| `transactional` | span_027 a span_030 | 1× `db_query` + 1× `api_call` (max 3 calls) |

---

## Requisitos

### Requisitos Funcionais

1. **RF1 — Duplicate Detection:** Detectar chamadas consecutivas (ou em janela de 5 spans) a mesma ferramenta com parametros identicos. Hash determinista: `SHA-256(sorted(json.dumps(params)))`. Retornar lista de grupos de duplicatas com `tool_name`, `params_hash`, indices e contagem.

2. **RF2 — Loop Detection:** Detectar ciclos A→B→A no grafo de tool calls. Uma chamada e considerada parte de um loop se a ferramenta ja foi chamada antes com parametros equivalentes e nenhuma chamada intermediaria produziu informacao nova significativa (sucesso + tokens > 100).

3. **RF3 — Tool Dispatch Validation:** Classificar cada span em uma categoria de query (`simple-lookup`, `search`, `multi-step-reasoning`, `transactional`). Validar contra template de dispatch: ferramentas permitidas, numero maximo de chamadas, ferramentas proibidas. Sinalizar violacoes.

4. **RF4 — Cost Attribution:** Atribuir custo em USD a cada tool call usando um modelo de precos configuraravel. Calcular: custo total observado, custo otico (apenas chamadas necessarias), custo desperdicado, e breakdown por ferramenta.

5. **RF5 — Severity Classification:** Classificar cada metrica em PASS/WARN/FAIL conforme thresholds. Verdict final: FAIL se qualquer metrica = FAIL, WARN se qualquer = WARN e nenhuma = FAIL, PASS caso contrario.

6. **RF6 — Behavioral Eval Report:** Gerar relatorio JSON com: `session_id`, `analyzed_at`, `total_spans`, `verdict`, `metrics` (redundancy_score, path_efficiency, loop_count, cost_waste_ratio), `duplicates`, `loops`, `tool_violations`, `cost_breakdown`, `summary`.

### Requisitos Tecnicos

1. **RT1 — Python puro:** Implementacao em Python com stdlib + dataclasses. Sem dependencias externas (hashlib, json, dataclasses, typing bastam).

2. **RT2 — Hashing deterministico:** `params_hash` usa `SHA-256(sorted(json.dumps(params)))`. Garantir que ordens diferentes de chaves no dict produzam o mesmo hash.

3. **RT3 — Thresholds configuraveis:** Todos os thresholds de deteccao (DUPLICATE_WINDOW, LOOP_MIN_TOKENS, severidade) sao parametros com defaults documentados, sobrescreviveis na construcao do pipeline.

4. **RT4 — Template de dispatch como dados:** Os templates de dispatch por categoria sao definidos como estrutura de dados (dict), nao como codigo condicional. Adicionar uma categoria nao requer alterar logica.

---

## Sua Tarefa

Voce vai implementar o `BehavioralEvalPipeline` em 3 partes.

---

### Parte 1: Diagnosticar o Trace Manualmente (15 min)

Analise os 30 spans de trace manualmente. Responda:

1. Quantas duplicatas existem? (mesma tool + mesmos parametros)
2. Quantos loops existem? (ciclos A→B→A onde intermediarios nao produziram informacao nova)
3. Quais violacoes de tool dispatch existem? (ferramenta proibida para a categoria, ou excesso de chamadas)
4. Qual o custo total observado vs. o custo otico?

Use a tabela de precos:

```python
TOOL_COST_USD = {
    "db_query": 0.002,
    "api_call": 0.015,
    "llm_call": 0.008,
    "sub_agent": 0.050,
    "search_tool": 0.005,
}
```

Registre suas respostas como comentarios no codigo da Parte 2.

---

### Parte 2: Implementar os Detectores (70 min)

Implemente os quatro detectores e o pipeline. Use este esqueleto:

```python
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from hashlib import sha256
import json
from typing import Optional


# ============================================================
# DATA MODELS
# ============================================================

class Verdict(Enum):
    PASS = "PASS"
    WARN = "WARN"
    FAIL = "FAIL"


class QueryCategory(Enum):
    SIMPLE_LOOKUP = "simple-lookup"
    SEARCH = "search"
    MULTI_STEP_REASONING = "multi-step-reasoning"
    TRANSACTIONAL = "transactional"


@dataclass
class TraceSpan:
    """Um span de trace representando uma tool call."""
    span_id: str
    session_id: str
    tool_name: str
    params: dict
    timestamp: str
    duration_ms: int
    success: bool
    tokens: int
    category: str

    # Computed after ingestion
    params_hash: str = ""

    def compute_hash(self) -> str:
        """SHA-256 deterministico dos parametros."""
        params_str = json.dumps(self.params, sort_keys=True)
        self.params_hash = sha256(params_str.encode()).hexdigest()
        return self.params_hash


@dataclass
class DuplicateGroup:
    """Grupo de chamadas duplicadas."""
    tool_name: str
    params_hash: str
    indices: list[int] = field(default_factory=list)
    count: int = 1


@dataclass
class DetectedLoop:
    """Loop detectado no grafo de tool calls."""
    start_idx: int
    end_idx: int
    tool_name: str
    cycle_length: int


@dataclass
class ToolViolation:
    """Violacao de dispatch de ferramenta."""
    violation_type: str  # "FORBIDDEN_TOOL" | "EXCESSIVE_CALLS"
    span_id: str = ""
    tool_name: str = ""
    count: int = 0
    max_allowed: int = 0
    reason: str = ""


@dataclass
class CostBreakdown:
    """Atribuicao de custo por tool e total."""
    per_tool: dict[str, float] = field(default_factory=dict)
    total_usd: float = 0.0
    optimal_usd: float = 0.0
    wasted_usd: float = 0.0


@dataclass
class BehavioralMetrics:
    """Metricas agregadas da analise comportamental."""
    redundancy_score: float = 0.0   # duplicate_calls / total_calls
    path_efficiency: float = 1.0     # necessary_calls / total_calls
    loop_count: int = 0
    cost_waste_ratio: float = 0.0    # wasted_cost / total_cost

    @property
    def redundancy_verdict(self) -> Verdict:
        # TODO: implementar thresholds configuraraveis
        pass

    @property
    def efficiency_verdict(self) -> Verdict:
        pass

    @property
    def loop_verdict(self) -> Verdict:
        pass

    @property
    def cost_verdict(self) -> Verdict:
        pass

    @property
    def overall_verdict(self) -> Verdict:
        """FAIL se qualquer metrica = FAIL, WARN se qualquer = WARN."""
        pass


# ============================================================
# CONFIGURATION
# ============================================================

# Custo por tool call em USD
TOOL_COST_USD = {
    "db_query": 0.002,
    "api_call": 0.015,
    "llm_call": 0.008,
    "sub_agent": 0.050,
    "search_tool": 0.005,
}

# Default cost for unknown tools
DEFAULT_TOOL_COST_USD = 0.01

# Thresholds do duplicate detector
DUPLICATE_WINDOW = 5  # max spans entre chamadas para considerar duplicata

# Thresholds do loop detector
LOOP_MIN_TOKENS = 100  # minimo de tokens para considerar output significativo

# Templates de dispatch por categoria de query
EXPECTED_DISPATCH = {
    QueryCategory.SIMPLE_LOOKUP: {
        "allowed_tools": ["db_query", "cache_get"],
        "max_calls": 2,
        "forbidden_tools": ["api_call", "sub_agent"],
        # Custo otico: 1 db_query
        "optimal_tools": [("db_query", 1)],
    },
    QueryCategory.SEARCH: {
        "allowed_tools": ["db_query", "search_tool", "llm_call"],
        "max_calls": 5,
        "forbidden_tools": ["api_call"],
        "optimal_tools": [("search_tool", 2), ("llm_call", 1)],
    },
    QueryCategory.MULTI_STEP_REASONING: {
        "allowed_tools": ["db_query", "llm_call", "api_call"],
        "max_calls": 8,
        "forbidden_tools": [],
        "optimal_tools": [("db_query", 2), ("llm_call", 1)],
    },
    QueryCategory.TRANSACTIONAL: {
        "allowed_tools": ["db_query", "api_call"],
        "max_calls": 3,
        "forbidden_tools": ["sub_agent", "search_tool"],
        "optimal_tools": [("db_query", 1), ("api_call", 1)],
    },
}

# Thresholds de severidade
SEVERITY_THRESHOLDS = {
    "redundancy": {"pass": 0.10, "warn": 0.30},   # <=0.10 PASS, <=0.30 WARN, >0.30 FAIL
    "efficiency": {"pass": 0.80, "warn": 0.50},    # >=0.80 PASS, >=0.50 WARN, <0.50 FAIL
    "loop_count": {"pass": 0, "warn": 1},           # 0 PASS, 1 WARN, >=2 FAIL
    "cost_waste": {"pass": 0.15, "warn": 0.40},     # <=0.15 PASS, <=0.40 WARN, >0.40 FAIL
}


# ============================================================
# DETECTOR 1: DUPLICATE DETECTOR
# ============================================================

class DuplicateDetector:
    """Detecta chamadas duplicadas (mesma tool, mesmos parametros)."""

    def __init__(self, window: int = DUPLICATE_WINDOW):
        self.window = window

    def detect(self, spans: list[TraceSpan]) -> list[DuplicateGroup]:
        """
        Analisa spans e retorna grupos de duplicatas.

        Duas chamadas sao duplicatas se:
        1. tool_name identico
        2. params_hash identico
        3. Separadas por no maximo self.window chamadas intermediarias
        """
        # TODO: implementar
        #
        # Algoritmo:
        # 1. Para cada span, garantir que params_hash foi computado
        # 2. Manter dict: (tool_name, params_hash) → ultimo indice visto
        # 3. Para cada span i, verificar se a chave ja foi vista
        #    e se i - ultimo_indice <= window
        # 4. Se sim, adicionar ao grupo de duplicatas correspondente
        #    ou criar novo grupo
        #
        # Retornar lista de DuplicateGroup
        pass


# ============================================================
# DETECTOR 2: LOOP DETECTOR
# ============================================================

class LoopDetector:
    """Detecta ciclos A→B→A no grafo de tool calls."""

    def __init__(self, min_tokens: int = LOOP_MIN_TOKENS):
        self.min_tokens = min_tokens

    def detect(self, spans: list[TraceSpan]) -> list[DetectedLoop]:
        """
        Analisa spans e retorna loops detectados.

        Um loop ocorre quando:
        1. Uma ferramenta e chamada no indice i
        2. A mesma ferramenta com mesmos parametros e chamada no indice j (j > i)
        3. Nenhum span entre i e j produziu output significativo
           (success=True e tokens > min_tokens)
        4. cycle_length = j - i >= 2
        """
        # TODO: implementar
        #
        # Algoritmo:
        # 1. Construir dict: (tool_name, params_hash) → lista de indices
        # 2. Para cada ferramenta com multiplas aparicoes:
        #    a. Para cada par de indices (i, j) com i < j:
        #    b. Verificar se algum span entre i e j tem sucesso
        #       e tokens > min_tokens
        #    c. Se nao, e cycle_length >= 2, e um loop
        pass


# ============================================================
# DETECTOR 3: TOOL DISPATCH VALIDATOR
# ============================================================

class ToolDispatchValidator:
    """Valida tool calls contra templates de dispatch por categoria."""

    def __init__(self, dispatch_templates: dict | None = None):
        self.templates = dispatch_templates or EXPECTED_DISPATCH

    def validate(self, spans: list[TraceSpan]) -> list[ToolViolation]:
        """
        Agrupa spans por categoria e valida contra template.

        Para cada categoria:
        1. Contar spans
        2. Verificar forbidden_tools
        3. Verificar max_calls
        """
        # TODO: implementar
        #
        # Algoritmo:
        # 1. Agrupar spans por self._resolve_category(span.category)
        # 2. Para cada (categoria, spans_do_grupo):
        #    a. Obter template da categoria
        #    b. Verificar cada span.tool_name contra forbidden_tools
        #    c. Verificar len(spans_do_grupo) contra max_calls
        # 3. Coletar ToolViolation para cada violacao
        pass

    def _resolve_category(self, category_str: str) -> QueryCategory:
        """Converte string de categoria para enum."""
        for cat in QueryCategory:
            if cat.value == category_str:
                return cat
        raise ValueError(f"Unknown category: {category_str}")


# ============================================================
# DETECTOR 4: COST ATTRIBUTOR
# ============================================================

class CostAttributor:
    """Atribui custo em USD a cada tool call e calcula totais."""

    def __init__(self, cost_model: dict | None = None):
        self.cost_model = cost_model or TOOL_COST_USD

    def compute(self, spans: list[TraceSpan]) -> CostBreakdown:
        """
        Calcula custo total observado, custo otico e desperdicio.

        Custo observado: soma do custo de cada span
        Custo otico: soma do custo das ferramentas no template optimal_tools
        """
        # TODO: implementar
        #
        # Algoritmo:
        # 1. Calcular custo observado: sum(cost_model[tool] para cada span)
        # 2. Calcular custo otico por categoria:
        #    Agrupar spans por categoria
        #    Para cada categoria, somar optimal_tools do template
        # 3. wasted = total - optimal
        # 4. cost_waste_ratio = wasted / total (0 se total == 0)
        pass


# ============================================================
# PIPELINE: BEHAVIORAL EVAL
# ============================================================

class BehavioralEvalPipeline:
    """Pipeline completo de behavioral eval path analysis."""

    def __init__(
        self,
        duplicate_window: int = DUPLICATE_WINDOW,
        loop_min_tokens: int = LOOP_MIN_TOKENS,
        dispatch_templates: dict | None = None,
        cost_model: dict | None = None,
        severity_thresholds: dict | None = None,
    ):
        self.duplicate_detector = DuplicateDetector(window=duplicate_window)
        self.loop_detector = LoopDetector(min_tokens=loop_min_tokens)
        self.tool_validator = ToolDispatchValidator(
            dispatch_templates=dispatch_templates
        )
        self.cost_attributor = CostAttributor(cost_model=cost_model)
        self.thresholds = severity_thresholds or SEVERITY_THRESHOLDS

    def analyze(self, spans_data: list[dict]) -> dict:
        """
        Pipeline principal: ingest → normalize → analyze → score → report.

        Args:
            spans_data: Lista de dicionarios com dados de TraceSpan

        Returns:
            Dicionario com o behavioral eval report completo
        """
        # 1. INGEST: converter dicts → TraceSpan, computar hashes
        spans = []
        for d in spans_data:
            span = TraceSpan(
                span_id=d["span_id"],
                session_id=d.get("session_id", ""),
                tool_name=d["tool_name"],
                params=d.get("params", {}),
                timestamp=d.get("timestamp", ""),
                duration_ms=d.get("duration_ms", 0),
                success=d.get("success", True),
                tokens=d.get("tokens", 0),
                category=d.get("category", "unknown"),
            )
            span.compute_hash()
            spans.append(span)

        # 2. ANALYZE: rodar os 4 detectores
        duplicates = self.duplicate_detector.detect(spans)
        loops = self.loop_detector.detect(spans)
        tool_violations = self.tool_validator.validate(spans)
        cost_breakdown = self.cost_attributor.compute(spans)

        # 3. SCORE: calcular metricas
        total_calls = len(spans)
        duplicate_calls = sum(g.count - 1 for g in duplicates)  # primeira chamada nao e duplicata
        redundancy_score = duplicate_calls / total_calls if total_calls > 0 else 0.0

        # TODO: calcular path_efficiency
        # necessary_calls = soma de optimal_tools por categoria
        # efficiency = necessary_calls / total_calls
        path_efficiency = 1.0  # placeholder

        loop_count = len(loops)
        cost_waste_ratio = (
            cost_breakdown.wasted_usd / cost_breakdown.total_usd
            if cost_breakdown.total_usd > 0
            else 0.0
        )

        # 4. VERDICT: classificar cada metrica
        metrics = BehavioralMetrics(
            redundancy_score=round(redundancy_score, 4),
            path_efficiency=round(path_efficiency, 4),
            loop_count=loop_count,
            cost_waste_ratio=round(cost_waste_ratio, 4),
        )

        t = self.thresholds
        redundancy_verdict = self._classify(
            redundancy_score, t["redundancy"]["pass"], t["redundancy"]["warn"], inverse=False
        )
        efficiency_verdict = self._classify(
            path_efficiency, t["efficiency"]["pass"], t["efficiency"]["warn"], inverse=True
        )
        loop_verdict = self._classify_int(
            loop_count, t["loop_count"]["pass"], t["loop_count"]["warn"]
        )
        cost_verdict = self._classify(
            cost_waste_ratio, t["cost_waste"]["pass"], t["cost_waste"]["warn"], inverse=False
        )

        overall = Verdict.PASS
        for v in [redundancy_verdict, efficiency_verdict, loop_verdict, cost_verdict]:
            if v == Verdict.FAIL:
                overall = Verdict.FAIL
                break
            if v == Verdict.WARN:
                overall = Verdict.WARN

        # 5. REPORT: montar output
        report = {
            "session_id": spans_data[0].get("session_id", "") if spans_data else "",
            "analyzed_at": "2026-06-26T15:00:00Z",  # TODO: usar datetime.now()
            "total_spans": total_calls,
            "verdict": overall.value,
            "metrics": {
                "redundancy_score": metrics.redundancy_score,
                "path_efficiency": metrics.path_efficiency,
                "loop_count": metrics.loop_count,
                "cost_waste_ratio": metrics.cost_waste_ratio,
            },
            "duplicates": [
                {
                    "tool_name": g.tool_name,
                    "params_hash": g.params_hash[:12] + "...",
                    "count": g.count,
                    "indices": g.indices,
                }
                for g in duplicates
            ],
            "loops": [
                {
                    "start_idx": l.start_idx,
                    "end_idx": l.end_idx,
                    "tool_name": l.tool_name,
                    "cycle_length": l.cycle_length,
                }
                for l in loops
            ],
            "tool_violations": [
                {
                    "type": v.violation_type,
                    "span_id": v.span_id,
                    "tool": v.tool_name,
                    "reason": v.reason,
                }
                for v in tool_violations
            ],
            "cost_breakdown": {
                "per_tool": cost_breakdown.per_tool,
                "total_usd": round(cost_breakdown.total_usd, 4),
                "optimal_usd": round(cost_breakdown.optimal_usd, 4),
                "wasted_usd": round(cost_breakdown.wasted_usd, 4),
            },
            "summary": self._generate_summary(metrics, duplicates, loops, tool_violations, cost_breakdown),
        }
        return report

    def _classify(self, value: float, pass_threshold: float, warn_threshold: float, inverse: bool = False) -> Verdict:
        """
        Classifica uma metrica continua em PASS/WARN/FAIL.

        inverse=True: valores ALTOS sao bons (ex: efficiency)
        inverse=False: valores BAIXOS sao bons (ex: redundancy)
        """
        if inverse:
            if value >= pass_threshold:
                return Verdict.PASS
            if value >= warn_threshold:
                return Verdict.WARN
            return Verdict.FAIL
        else:
            if value <= pass_threshold:
                return Verdict.PASS
            if value <= warn_threshold:
                return Verdict.WARN
            return Verdict.FAIL

    def _classify_int(self, value: int, pass_threshold: int, warn_threshold: int) -> Verdict:
        """Classifica metrica inteira (ex: loop count)."""
        if value <= pass_threshold:
            return Verdict.PASS
        if value <= warn_threshold:
            return Verdict.WARN
        return Verdict.FAIL

    def _generate_summary(
        self,
        metrics: BehavioralMetrics,
        duplicates: list,
        loops: list,
        violations: list,
        costs: CostBreakdown,
    ) -> str:
        """Gera um resumo em linguagem natural dos findings."""
        # TODO: implementar — gerar string descritiva
        pass


# ============================================================
# TEST DATA: 30 spans de trace
# ============================================================

TRACE_SPANS_DATA = [
    {"span_id": "span_001", "session_id": "ses_koda_20260626", "tool_name": "db_query", "params": {"query": "SELECT balance FROM accounts WHERE id=123", "db": "postgres-main"}, "timestamp": "2026-06-26T14:30:01Z", "duration_ms": 45, "success": True, "tokens": 120, "category": "simple-lookup"},
    {"span_id": "span_002", "session_id": "ses_koda_20260626", "tool_name": "db_query", "params": {"query": "SELECT balance FROM accounts WHERE id=123", "db": "postgres-main"}, "timestamp": "2026-06-26T14:30:02Z", "duration_ms": 42, "success": True, "tokens": 120, "category": "simple-lookup"},
    {"span_id": "span_003", "session_id": "ses_koda_20260626", "tool_name": "db_query", "params": {"query": "SELECT balance FROM accounts WHERE id=123", "db": "postgres-main"}, "timestamp": "2026-06-26T14:30:03Z", "duration_ms": 44, "success": True, "tokens": 120, "category": "simple-lookup"},
    {"span_id": "span_004", "session_id": "ses_koda_20260626", "tool_name": "api_call", "params": {"endpoint": "/accounts/123", "provider": "payment-gateway"}, "timestamp": "2026-06-26T14:30:04Z", "duration_ms": 230, "success": True, "tokens": 250, "category": "simple-lookup"},
    {"span_id": "span_005", "session_id": "ses_koda_20260626", "tool_name": "sub_agent", "params": {"agent": "verify-balance", "args": {"account_id": 123}}, "timestamp": "2026-06-26T14:30:05Z", "duration_ms": 3200, "success": True, "tokens": 1500, "category": "simple-lookup"},
    {"span_id": "span_006", "session_id": "ses_koda_20260626", "tool_name": "db_query", "params": {"query": "SELECT * FROM accounts WHERE id=123", "db": "postgres-main"}, "timestamp": "2026-06-26T14:30:08Z", "duration_ms": 55, "success": True, "tokens": 450, "category": "simple-lookup"},
    {"span_id": "span_007", "session_id": "ses_koda_20260626", "tool_name": "db_query", "params": {"query": "SELECT id, name, price FROM products WHERE category='suplementos'", "db": "postgres-main"}, "timestamp": "2026-06-26T14:30:15Z", "duration_ms": 80, "success": True, "tokens": 350, "category": "search"},
    {"span_id": "span_008", "session_id": "ses_koda_20260626", "tool_name": "search_tool", "params": {"query": "suplementos whey protein", "index": "products"}, "timestamp": "2026-06-26T14:30:16Z", "duration_ms": 120, "success": True, "tokens": 200, "category": "search"},
    {"span_id": "span_009", "session_id": "ses_koda_20260626", "tool_name": "search_tool", "params": {"query": "suplementos whey protein", "index": "products"}, "timestamp": "2026-06-26T14:30:17Z", "duration_ms": 115, "success": True, "tokens": 200, "category": "search"},
    {"span_id": "span_010", "session_id": "ses_koda_20260626", "tool_name": "db_query", "params": {"query": "SELECT id, name, price FROM products WHERE category='suplementos'", "db": "postgres-main"}, "timestamp": "2026-06-26T14:30:18Z", "duration_ms": 82, "success": True, "tokens": 350, "category": "search"},
    {"span_id": "span_011", "session_id": "ses_koda_20260626", "tool_name": "search_tool", "params": {"query": "suplementos whey protein", "index": "products"}, "timestamp": "2026-06-26T14:30:19Z", "duration_ms": 118, "success": True, "tokens": 200, "category": "search"},
    {"span_id": "span_012", "session_id": "ses_koda_20260626", "tool_name": "llm_call", "params": {"prompt": "Resuma os resultados de busca", "model": "deepseek-v4"}, "timestamp": "2026-06-26T14:30:20Z", "duration_ms": 1800, "success": True, "tokens": 800, "category": "search"},
    {"span_id": "span_013", "session_id": "ses_koda_20260626", "tool_name": "search_tool", "params": {"query": "whey protein isolado 1kg", "index": "products"}, "timestamp": "2026-06-26T14:30:25Z", "duration_ms": 130, "success": True, "tokens": 220, "category": "search"},
    {"span_id": "span_014", "session_id": "ses_koda_20260626", "tool_name": "search_tool", "params": {"query": "whey protein isolado 1kg", "index": "products"}, "timestamp": "2026-06-26T14:30:26Z", "duration_ms": 125, "success": True, "tokens": 220, "category": "search"},
    {"span_id": "span_015", "session_id": "ses_koda_20260626", "tool_name": "api_call", "params": {"endpoint": "/products/search", "provider": "external-catalog"}, "timestamp": "2026-06-26T14:30:27Z", "duration_ms": 350, "success": True, "tokens": 400, "category": "search"},
    {"span_id": "span_016", "session_id": "ses_koda_20260626", "tool_name": "search_tool", "params": {"query": "whey protein isolado 1kg", "index": "products"}, "timestamp": "2026-06-26T14:30:29Z", "duration_ms": 122, "success": True, "tokens": 220, "category": "search"},
    {"span_id": "span_017", "session_id": "ses_koda_20260626", "tool_name": "db_query", "params": {"query": "SELECT id, name, price, stock FROM products WHERE name ILIKE '%whey%'", "db": "postgres-main"}, "timestamp": "2026-06-26T14:30:30Z", "duration_ms": 90, "success": True, "tokens": 400, "category": "search"},
    {"span_id": "span_018", "session_id": "ses_koda_20260626", "tool_name": "llm_call", "params": {"prompt": "Recomende o melhor whey protein", "model": "deepseek-v4"}, "timestamp": "2026-06-26T14:30:32Z", "duration_ms": 2100, "success": True, "tokens": 950, "category": "search"},
    {"span_id": "span_019", "session_id": "ses_koda_20260626", "tool_name": "db_query", "params": {"query": "SELECT * FROM orders WHERE customer_id=456 ORDER BY created_at DESC LIMIT 5", "db": "postgres-main"}, "timestamp": "2026-06-26T14:30:40Z", "duration_ms": 70, "success": True, "tokens": 300, "category": "multi-step-reasoning"},
    {"span_id": "span_020", "session_id": "ses_koda_20260626", "tool_name": "db_query", "params": {"query": "SELECT * FROM orders WHERE customer_id=456 ORDER BY created_at DESC LIMIT 5", "db": "postgres-main"}, "timestamp": "2026-06-26T14:30:41Z", "duration_ms": 68, "success": True, "tokens": 300, "category": "multi-step-reasoning"},
    {"span_id": "span_021", "session_id": "ses_koda_20260626", "tool_name": "llm_call", "params": {"prompt": "Analise o historico de pedidos", "model": "deepseek-v4"}, "timestamp": "2026-06-26T14:30:43Z", "duration_ms": 2500, "success": True, "tokens": 1100, "category": "multi-step-reasoning"},
    {"span_id": "span_022", "session_id": "ses_koda_20260626", "tool_name": "db_query", "params": {"query": "SELECT * FROM orders WHERE customer_id=456 ORDER BY created_at DESC LIMIT 5", "db": "postgres-main"}, "timestamp": "2026-06-26T14:30:46Z", "duration_ms": 72, "success": True, "tokens": 300, "category": "multi-step-reasoning"},
    {"span_id": "span_023", "session_id": "ses_koda_20260626", "tool_name": "api_call", "params": {"endpoint": "/customers/456/preferences", "provider": "crm"}, "timestamp": "2026-06-26T14:30:48Z", "duration_ms": 400, "success": True, "tokens": 500, "category": "multi-step-reasoning"},
    {"span_id": "span_024", "session_id": "ses_koda_20260626", "tool_name": "sub_agent", "params": {"agent": "recommend-products", "args": {"customer_id": 456}}, "timestamp": "2026-06-26T14:30:50Z", "duration_ms": 4500, "success": True, "tokens": 2000, "category": "multi-step-reasoning"},
    {"span_id": "span_025", "session_id": "ses_koda_20260626", "tool_name": "db_query", "params": {"query": "SELECT * FROM orders WHERE customer_id=456 ORDER BY created_at DESC LIMIT 5", "db": "postgres-main"}, "timestamp": "2026-06-26T14:30:55Z", "duration_ms": 69, "success": True, "tokens": 300, "category": "multi-step-reasoning"},
    {"span_id": "span_026", "session_id": "ses_koda_20260626", "tool_name": "llm_call", "params": {"prompt": "Gere recomendacoes finais", "model": "deepseek-v4"}, "timestamp": "2026-06-26T14:30:58Z", "duration_ms": 2200, "success": True, "tokens": 1000, "category": "multi-step-reasoning"},
    {"span_id": "span_027", "session_id": "ses_koda_20260626", "tool_name": "db_query", "params": {"query": "UPDATE orders SET status='confirmed' WHERE id=789", "db": "postgres-main"}, "timestamp": "2026-06-26T14:31:05Z", "duration_ms": 35, "success": True, "tokens": 80, "category": "transactional"},
    {"span_id": "span_028", "session_id": "ses_koda_20260626", "tool_name": "api_call", "params": {"endpoint": "/orders/789/confirm", "provider": "payment-gateway"}, "timestamp": "2026-06-26T14:31:06Z", "duration_ms": 500, "success": True, "tokens": 300, "category": "transactional"},
    {"span_id": "span_029", "session_id": "ses_koda_20260626", "tool_name": "db_query", "params": {"query": "UPDATE orders SET status='confirmed' WHERE id=789", "db": "postgres-main"}, "timestamp": "2026-06-26T14:31:07Z", "duration_ms": 38, "success": True, "tokens": 80, "category": "transactional"},
    {"span_id": "span_030", "session_id": "ses_koda_20260626", "tool_name": "api_call", "params": {"endpoint": "/notifications/send", "provider": "notification-service"}, "timestamp": "2026-06-26T14:31:08Z", "duration_ms": 180, "success": True, "tokens": 150, "category": "transactional"},
]
```

---

### Parte 3: Executar o Pipeline e Comparar (35 min)

Execute o pipeline sobre os 30 spans e verifique:

1. O detector de duplicatas encontra os grupos esperados
2. O detector de loops encontra os ciclos corretos
3. O validator sinaliza ferramentas proibidas e excesso de chamadas
4. O cost attributor calcula custo observado vs. otico
5. O relatorio final tem verdict, metrics, e summary

```python
def run_behavioral_eval_pipeline():
    """Executa o pipeline completo e imprime o relatorio."""
    pipeline = BehavioralEvalPipeline()
    report = pipeline.analyze(TRACE_SPANS_DATA)

    print("=" * 60)
    print("BEHAVIORAL EVAL REPORT")
    print("=" * 60)
    print(f"Session: {report['session_id']}")
    print(f"Total Spans: {report['total_spans']}")
    print(f"Verdict: {report['verdict']}")
    print()
    print("METRICS:")
    m = report["metrics"]
    print(f"  Redundancy Score:   {m['redundancy_score']:.2%}")
    print(f"  Path Efficiency:    {m['path_efficiency']:.2%}")
    print(f"  Loop Count:         {m['loop_count']}")
    print(f"  Cost Waste Ratio:   {m['cost_waste_ratio']:.2%}")
    print()
    print(f"DUPLICATES FOUND: {len(report['duplicates'])}")
    for d in report["duplicates"]:
        print(f"  {d['tool_name']} x{d['count']} at indices {d['indices']}")
    print()
    print(f"LOOPS FOUND: {len(report['loops'])}")
    for l in report["loops"]:
        print(f"  {l['tool_name']}: indices [{l['start_idx']}→{l['end_idx']}], cycle={l['cycle_length']}")
    print()
    print(f"TOOL VIOLATIONS: {len(report['tool_violations'])}")
    for v in report["tool_violations"]:
        print(f"  [{v['type']}] {v['tool']}: {v['reason']}")
    print()
    c = report["cost_breakdown"]
    print("COST BREAKDOWN:")
    print(f"  Total:    ${c['total_usd']:.4f}")
    print(f"  Optimal:  ${c['optimal_usd']:.4f}")
    print(f"  Wasted:   ${c['wasted_usd']:.4f}")
    print(f"  Per tool: {c['per_tool']}")
    print()
    print("SUMMARY:")
    print(f"  {report['summary']}")

    return report


if __name__ == "__main__":
    run_behavioral_eval_pipeline()
```

---

## Entregaveis

- Implementacao de `DuplicateDetector` com hash deterministico e janela deslizante
- Implementacao de `LoopDetector` com analise de output intermediario
- Implementacao de `ToolDispatchValidator` com templates por categoria
- Implementacao de `CostAttributor` com custo observado vs. otico
- `BehavioralEvalPipeline` integrando os 4 detectores
- Relatorio JSON completo com verdict, metrics, e summary narrativo

---

## Validacao: Criterios de Aceitacao

Seu codigo sera considerado **APROVADO** quando:

### Criterio 1: Diagnostico (Parte 1)

- [ ] Voce identificou duplicatas manualmente — pelo menos os grupos: db_query SELECT balance (indices 0-2), db_query SELECT orders (indices 18, 19, 21, 24), UPDATE orders (indices 26, 28), search_tool whey protein (indices 7, 8, 10), search_tool whey protein isolado (indices 12, 13, 15)
- [ ] Voce identificou loops manualmente — pelo menos: db_query SELECT orders (4 repeticoes com llm_call entre elas, mas llm_call produziu output significativo → NAO e loop em todos os casos)
- [ ] Voce identificou violacoes de dispatch — pelo menos: api_call em simple-lookup (span_004, FORBIDDEN), sub_agent em simple-lookup (span_005, FORBIDDEN), api_call em search (span_015, FORBIDDEN), excesso de chamadas em search (12 spans, max 5)
- [ ] Voce calculou custo observado vs. otico com diferenca significativa

### Criterio 2: Duplicate Detector

- [ ] `DuplicateDetector.detect()` retorna grupos com tool_name, params_hash, indices e count
- [ ] Detecta spans 001-002-003 como um grupo de 3 duplicatas
- [ ] Detecta spans 008-009-011 como um grupo de 3 duplicatas (search_tool, mesma query)
- [ ] Nao detecta span_006 como duplicata de span_001-003 (SELECT * vs SELECT balance — params diferentes, hash diferente)
- [ ] `params_hash` e identico para spans com mesmos parametros em ordens diferentes de chaves

### Criterio 3: Loop Detector

- [ ] `LoopDetector.detect()` retorna lista de `DetectedLoop`
- [ ] Detecta loops apenas quando chamadas intermediarias nao produzem output significativo (tokens <= LOOP_MIN_TOKENS ou success=False)
- [ ] Nao detecta como loop quando ha um llm_call com tokens > 100 entre as repeticoes (output significativo justifica nova chamada)
- [ ] `cycle_length` e correto (j - i)

### Criterio 4: Tool Dispatch Validator

- [ ] `ToolDispatchValidator.validate()` retorna `ToolViolation` para cada violacao
- [ ] Sinaliza `FORBIDDEN_TOOL` quando span usa ferramenta na lista `forbidden_tools` da categoria
- [ ] Sinaliza `EXCESSIVE_CALLS` quando contagem de spans na categoria excede `max_calls`
- [ ] Categorias nao reconhecidas levantam `ValueError`

### Criterio 5: Cost Attributor

- [ ] `CostAttributor.compute()` retorna `CostBreakdown` com per_tool, total_usd, optimal_usd, wasted_usd
- [ ] Custo observado = soma de `TOOL_COST_USD[tool]` para cada span
- [ ] Custo otico usa `optimal_tools` do template por categoria
- [ ] `wasted_usd = total_usd - optimal_usd` (nunca negativo)
- [ ] `cost_waste_ratio` e 0 quando total_usd e 0

### Criterio 6: Pipeline e Relatorio

- [ ] `BehavioralEvalPipeline.analyze()` retorna dict com TODOS os campos do schema
- [ ] `verdict` e FAIL (esperado para este trace — 34% de redundancia, loops, violacoes de dispatch)
- [ ] `summary` e uma string nao-vazia descrevendo os findings principais
- [ ] Relatorio e JSON serializavel (`json.dumps(report)` nao levanta excecao)

---

## Rubrica de Avaliacao

| Criterio | Peso | Insuficiente (0-3) | Basico (4-6) | Proficiente (7-8) | Excelente (9-10) |
|---|---|---|---|---|---|
| **Diagnostico (Parte 1)** | 10% | Nao identificou os grupos de duplicatas | Identificou parcialmente, com erros de contagem | Diagnostico completo — duplicatas, loops, violacoes e custos identificados | Diagnostico + analise de quais duplicatas sao loops e quais sao justificaveis |
| **Duplicate Detector** | 25% | Nao implementou ou retorna resultados incorretos | Detecta algumas duplicatas mas falha em edge cases (hash, window) | Detecta todas as duplicatas corretamente com hash deterministico e window | Detecta duplicatas + distingue duplicatas legitimas (retry) de ilegitimas (redundancia) |
| **Loop Detector** | 20% | Nao implementou | Implementa mas classifica tudo como loop ou nada como loop | Detecta loops corretamente, filtrando por output intermediario significativo | Loop detection + analise de intencao semantica (tool diferente, mesmo proposito) |
| **Tool Validator + Cost** | 25% | Nao implementou | Implementa um dos dois (validator OU cost) | Ambos implementados, com templates corretos e custo otico calculado | Validator com templates como dados (nao codigo) + cost model configuravel |
| **Pipeline + Relatorio** | 20% | Pipeline nao integra ou relatorio ausente | Pipeline integra mas relatorio incompleto | Pipeline funcional com relatorio completo e verdict correto | Relatorio com summary narrativo + thresholds configuraveis + output JSON serializavel |

**Nota final:** Media ponderada. **Aprovacao:** >= 7.0

---

## Dicas para Implementacao

### Para o Duplicate Detector

1. **O hash precisa ser deterministico.** `json.dumps(params, sort_keys=True)` garante que `{"a": 1, "b": 2}` e `{"b": 2, "a": 1}` produzam o mesmo hash. Sem `sort_keys=True`, o detector falha em edge cases sutis.

2. **A window previne falsos positivos.** Se duas chamadas identicas estao separadas por 20 spans com informacao nova significativa, a segunda chamada e provavelmente intencional. A window de 5 e um equilibrio: pega duplicatas em sequencia mas ignora repeticoes legitimas em passos distantes.

3. **Duplicata vs. Retry.** Um retry apos falha (`success=false` na primeira chamada) nao e uma duplicata comportamental — e uma estrategia de resiliencia. O detector basico nao distingue; uma melhoria e verificar `success=false` na primeira ocorrencia.

### Para o Loop Detector

1. **Output intermediario e a chave.** Um ciclo A→llm_call→A onde o llm_call produziu 2000 tokens de analise NAO e um loop — a analise pode justificar re-consultar A. Um ciclo A→db_query(identica)→A onde a db_query so retornou 50 tokens SIM e um loop.

2. **Loops vs. Workflows.** Em um workflow multi-step, e normal chamar a mesma ferramenta varias vezes com parametros diferentes. O loop detector so sinaliza quando parametros sao identicos E intermediarios sao nao-significativos.

3. **O threshold de 100 tokens e uma heuristica.** Em producao, calibrar com dados reais: qual a correlacao entre tokens no output intermediario e a probabilidade de o ciclo ser intencional?

### Para o Tool Dispatch Validator

1. **Templates como dados, nao codigo.** `EXPECTED_DISPATCH` e um dict, nao uma cascata de if/elif. Adicionar uma categoria requer adicionar uma entrada no dict, nao alterar logica.

2. **Forbidden vs. Allowed.** `forbidden_tools` e uma lista negra: ferramentas que NUNCA devem ser usadas para aquela categoria. `allowed_tools` e uma lista branca: ferramentas permitidas (mas nao obrigatorias). Um template pode nao ter `forbidden_tools` (lista vazia).

3. **Excesso de chamadas e cumulativo por categoria.** O validator agrupa spans por categoria e conta o total. Se uma categoria tem `max_calls=5` e 12 spans, todos os 12 sao reportados como uma unica violacao `EXCESSIVE_CALLS`.

### Para o Cost Attributor

1. **Custo otico e assintotico.** O `optimal_tools` do template define o minimo teorico de chamadas para resolver a query. O mundo real pode precisar de mais — o custo otico e um benchmark, nao uma expectativa rigida.

2. **Custo de sub_agent e alto por design.** `sub_agent` custa $0.05 — 25x mais que um `db_query`. Isso e intencional: delegar para um sub-agente e caro e so deve ser feito quando a tarefa realmente requer raciocinio multi-step. O cost attributor revela quando um sub-agent foi usado para uma tarefa que um db_query resolveria.

3. **Cost waste ratio vs. absoluto.** Um waste de $0.05 em uma query de $0.10 e 50% de waste — alarmante. Um waste de $0.05 em uma query de $5.00 e 1% — aceitavel. O ratio captura a eficiencia relativa; o valor absoluto captura o impacto financeiro.

---

## Duvidas Comuns

**P: Isso nao e so um linter de tool calls?**
R: E mais que um linter. Um linter verifica regras estaticas (ex: "nao use api_call em simple-lookup"). O behavioral eval analisa a sequencia temporal — duplicatas, loops, e eficiencia de caminho. Um linter diria que 3 db_queries identicas sao "3 chamadas validas". O behavioral eval diz que sao "2 chamadas redundantes, custo 3x".

**P: Como isso se relaciona com o trace instrumentation?**
R: O trace instrumentation (task-wrapper.sh → trace-cli.ts → telemetry.db) e o produtor de dados. O behavioral eval e o consumidor. Sem trace instrumentation, nao ha spans para analisar. O behavioral eval e a razao pela qual investimos em tracing — sem ele, os dados existem mas ninguem os le para detectar desperdicio comportamental.

**P: Qual a diferenca entre duplicate detection e loop detection?**
R: Duplicata = mesma ferramenta, mesmos parametros, em sequencia (window de 5). Loop = mesma ferramenta, mesmos parametros, com chamadas intermediarias que nao produziram output significativo. Toda duplicata consecutiva e um tipo de loop (cycle_length=1), mas nem todo loop e uma duplicata consecutiva. O loop detector tem um escopo mais amplo: captura ciclos onde o agente "da uma volta" antes de repetir a chamada.

**P: Como calibrar os thresholds de severidade?**
R: Comece com os defaults (redundancy: 0.10/0.30, efficiency: 0.80/0.50, loops: 0/1, cost_waste: 0.15/0.40). Execute sobre 1.000 traces reais. Plote a distribuicao de cada metrica. Ajuste os thresholds para que ~70% das sessoes sejam PASS, ~20% WARN, ~10% FAIL. Recalibre mensalmente conforme o agente evolui.

**P: O que fazer com o relatorio de behavioral eval?**
R: O relatorio alimenta tres consumidores:
1. **QI Loop**: findings de FAIL disparam `recommendation-writer` → `writing-plans` → implementacao de correcao
2. **Flywheel**: cada FAIL se torna um caso de teste no living eval dataset (production-failure-regression-flywheel)
3. **CFO Dashboard**: custo por query, waste ratio, e tendencia mensal — evidencia para budget de infra

---

## Proximo Passo

Depois de completar este exercicio:

1. Leia `[[.opencode/skills/behavioral-eval-path-analysis/SKILL|Behavioral Eval Path Analysis Skill]]` — o skill que operacionaliza este pipeline no runtime Sisyphus.
2. Leia `[[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]]` — como converter behavioral FAILs em casos de teste permanentes.
3. (Opcional) Estenda o pipeline com `IntentionalDuplicateDetector`: classifica duplicatas como "retry legitimo" vs. "redundancia" baseado em `success=false` na primeira chamada ou mudanca de estado entre chamadas.
4. (Opcional) Integre o pipeline com o `quality-improvement-loop`: faça o QI loop consumir o behavioral eval report como input adicional alem do review-work.

---

*Exercicio Behavioral Eval Path Analysis | Nivel 3 — Arquitetura Avancada*

**O custo de uma resposta correta nao e so a qualidade da resposta — e o caminho que o agente percorreu para chegar ate ela.**
