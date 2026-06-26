---
title: "Exercicio: Multi-Provider Model Routing com Resiliencia de Capacidade"
type: exercise
level: "N2"
aliases: ["multi-provider routing", "roteamento multi-provedor", "provider fallback", "capacity resilience", "model routing black friday"]
tags: [curriculo-conteudo, nivel-2, exercicio, agentes-orquestracao, model-selection, resilience, provider-agnostic, fallback-chain, rate-limiting]
duration: "60-75 min"
relates-to: ["[[docs/analysis/2026-06-26-the-best-ai-agents-are-simpler-than-you-think/2026-06-26-the-best-ai-agents-are-simpler-than-you-think-patterns|Sierra Patterns]]", "[[docs/analysis/2026-06-26-the-best-ai-agents-are-simpler-than-you-think/2026-06-26-the-best-ai-agents-are-simpler-than-you-think-classification|Classification]]", "[[docs/canonical/neutral-selection-layer|Neutral Selection Layer]]", "[[docs/canonical/model-switching-architecture-enterprise-eval-gate|Model-Switching Architecture]]"]
last_updated: 2026-06-26
---
# Exercicio: Multi-Provider Model Routing com Resiliencia de Capacidade
## Nivel 2 - Padroes Praticos

**Tempo Estimado:** 60-75 minutos
**Dificuldade:** Intermediario
**Pre-requisito:** Ter lido `02-sprint-contracts.md` (Nivel 2) + completado Exercicio 3
**Objetivo:** Construir um roteador multi-provedor com deteccao de capacidade, fallback em cadeia e restricoes de regiao enterprise

---

## Prologo: A Black Friday Que Derrubou o Agente Unico

### Sexta-feira, 06h00. O trafego comecou a subir.

```
SRE: "O agente de busca de produtos esta com latencia de 12 segundos."
ENG: "E a OpenAI. Rate limit. 429 em 40% das chamadas."
PM: "Troca pra Anthropic."
ENG: "A Anthropic tambem esta saturada. Unico cluster, mesma regiao."
```

O `SearchAgent` da **FitStore** foi arquitetado com dependencia de fornecedor unico: toda chamada de busca, classificacao de intencao e geracao de resposta ia para o mesmo modelo no mesmo provedor. Funcionava para 5 mil consultas por dia. Na Black Friday, 80 mil consultas em 6 horas.

O agente nao tinha:
- Roteamento entre provedores (OpenAI, Anthropic, DeepSeek, Groq) por tarefa
- Monitoramento de capacidade em tempo real por provedor
- Cadeia de fallback quando o primario atingia rate limit
- Restricoes de regiao cloud por cliente enterprise

Cada falha de rate limit gerava um stack trace de 40 linhas no contexto do agente. Em 20 minutos, a janela de contexto era 70% stack traces de "429 Too Many Requests". O agente comecou a responder "estou com dificuldades tecnicas" para 60% das consultas.

**O que deveria ter acontecido:**

```
[route] task=product_search → provider=deepseek (openai: 98% capacity, anthropic: 94%)
[route] task=intent_classify → provider=groq (latencia < 50ms)
[route] task=enterprise_acme_corp → provider=azure (restricao de regiao: west-europe)
[fallback] deepseek timeout → promot=anthropic (tentativa 2/3)
[capacity] all providers > 85% → backpressure: queue novas requisicoes
```

**Sua missao:** Construir um `ProviderRouter` que distribui tarefas entre 5 provedores, monitora capacidade, aplica fallback em cadeia e respeita restricoes de regiao por cliente.

---

## Cenario: FitStore SearchAgent na Black Friday

### Contexto

Voce recebeu a arquitetura do `SearchAgent` da **FitStore** -- um agente de e-commerce que processa consultas de busca de produtos, classificacao de intencao e geracao de respostas. Durante a Black Friday, o agente processou 80 mil consultas em 6 horas com 5 provedores disponiveis.

Cada tarefa do agente tem:

```json
{
  "task_id": "T-4821",
  "type": "product_search",
  "customer_id": "acme_corp",
  "priority": "high",
  "max_latency_ms": 500,
  "min_quality_tier": "frontier",
  "cloud_region_constraint": null,
  "payload_tokens": 1200
}
```

Cada provedor reporta seu estado a cada 30 segundos:

```json
{
  "provider": "openai",
  "status": "degraded",
  "capacity_pct": 92.0,
  "rate_limit_remaining": 120,
  "rate_limit_reset_ms": 45000,
  "avg_latency_ms": 340,
  "region": "us-east-1",
  "supported_regions": ["us-east-1", "eu-west-1"],
  "quality_tier": "frontier"
}
```

### Dados de Entrada

O sistema monitora 5 provedores com caracteristicas distintas:

| Provedor | Quality Tier | Latencia Media | Rate Limit/min | Regioes |
|---|---|---|---|---|
| openai | frontier | 280ms | 3500 | us-east-1, eu-west-1 |
| anthropic | frontier | 310ms | 2000 | us-east-1, eu-west-1 |
| deepseek | frontier | 400ms | 5000 | us-east-1 |
| groq | fast | 45ms | 30000 | us-east-1, eu-west-1, ap-south-1 |
| azure | enterprise | 350ms | 10000 | us-east-1, eu-west-1, ap-south-1, sa-east-1 |

---

## Requisitos

### Requisitos Funcionais

1. **RF1 - Roteamento por task type:** Cada tipo de tarefa (`product_search`, `intent_classify`, `response_gen`) tem um conjunto de provedores elegiveis e um quality tier minimo
2. **RF2 - Fallback em cadeia:** Quando o provedor primario esta acima de 85% de capacidade, o roteador tenta o secundario, depois o terciario. Maximo 3 tentativas por tarefa
3. **RF3 - Restricao de regiao enterprise:** Clientes enterprise com `cloud_region_constraint` so podem ser roteados para provedores que suportam aquela regiao. Se nenhum provedor elegivel atende a restricao, a tarefa e rejeitada com `[rejected] region_constraint_violation`
4. **RF4 - Backpressure global:** Quando TODOS os provedores estao acima de 85% de capacidade, novas tarefas de prioridade `low` sao enfileiradas; `high` e `critical` sao roteadas para o provedor menos saturado
5. **RF5 - Quality tier gating:** Tarefas que exigem `quality_tier: frontier` nao podem ser roteadas para provedores `fast` ou `enterprise`. Tarefas `fast` podem ser roteadas para qualquer tier, priorizando latencia
6. **RF6 - Circuit breaker por provedor:** Se um provedor retorna `status: "down"` ou latencia > 2000ms por 3 medicoes consecutivas, ele e removido do pool por 5 minutos

### Requisitos Tecnicos

1. **RT1 - Python puro:** Implementacao em Python com stdlib + dataclasses
2. **RT2 - Simulacao deterministica:** Estado dos provedores e pre-carregado em fixtures; sem chamadas de rede reais
3. **RT3 - Log de roteamento:** Cada decisao de roteamento gera uma entrada de log no formato `[route] task=<id> → provider=<name> (reason: <...>)`

---

## Sua Tarefa

Voce vai implementar o `ProviderRouter` em 3 partes.

---

### Parte 1: Diagnosticar o Colapso de Provedor Unico (10 min)

Analise o cenario abaixo. A **FitStore** usava apenas OpenAI para todas as tarefas na Black Friday de 2025.

```python
# Cenario: Black Friday 2025 — provedor unico (OpenAI)
# 80 mil consultas em 6 horas, todas roteadas para openai

TASKS_SIMULATED = {
    "product_search": 38000,
    "intent_classify": 25000,
    "response_gen": 17000,
}

OPENAI_CAPACITY = {
    "rate_limit_per_minute": 3500,
    "avg_tokens_per_task": 1500,
    "max_tokens_per_minute": 4_500_000,  # ~3500 chamadas * 1500 tokens
}

# TAREFA: Responda no codigo como comentario:
#
# 1. Quantas chamadas por minuto a FitStore precisava processar no pico?
#    (assuma distribuicao uniforme ao longo das 6 horas)
#
# 2. O rate limit da OpenAI (3500 chamadas/min) era suficiente?
#    Se nao, qual o deficit por minuto?
#
# 3. Se a Anthropic tem rate limit de 2000/min e a DeepSeek de 5000/min,
#    qual seria a capacidade combinada se as tarefas fossem distribuidas?
#
# 4. Qual a economia de latencia se intent_classify (45% das tarefas)
#    fosse roteada para Groq (45ms) em vez de OpenAI (280ms)?
```

---

### Parte 2: Implementar o ProviderRouter (40 min)

```python
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
import time


# ============================================================
# DATA MODELS
# ============================================================

class TaskType(Enum):
    PRODUCT_SEARCH = "product_search"
    INTENT_CLASSIFY = "intent_classify"
    RESPONSE_GEN = "response_gen"


class QualityTier(Enum):
    FRONTIER = "frontier"    # OpenAI, Anthropic, DeepSeek
    FAST = "fast"            # Groq
    ENTERPRISE = "enterprise"  # Azure


class ProviderStatus(Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"  # > 85% capacity
    DOWN = "down"


class TaskPriority(Enum):
    LOW = "low"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class Task:
    task_id: str
    type: TaskType
    customer_id: str
    priority: TaskPriority
    max_latency_ms: int
    min_quality_tier: QualityTier
    cloud_region_constraint: Optional[str] = None
    payload_tokens: int = 0


@dataclass
class ProviderState:
    name: str
    quality_tier: QualityTier
    status: ProviderStatus
    capacity_pct: float
    rate_limit_remaining: int
    rate_limit_reset_ms: int
    avg_latency_ms: float
    supported_regions: list[str] = field(default_factory=list)
    consecutive_failures: int = 0
    circuit_open_until: float = 0.0  # timestamp ate quando o circuito esta aberto

    def is_available(self) -> bool:
        """Provedor disponivel se nao estiver DOWN e circuito nao aberto."""
        if self.status == ProviderStatus.DOWN:
            return False
        if time.time() < self.circuit_open_until:
            return False
        return True

    def has_capacity_headroom(self) -> bool:
        """Tem folga se abaixo de 85% de capacidade."""
        return self.capacity_pct < 85.0

    def supports_region(self, region: Optional[str]) -> bool:
        """Verifica se o provedor suporta a regiao exigida."""
        if region is None:
            return True
        return region in self.supported_regions

    def meets_quality_tier(self, required: QualityTier) -> bool:
        """Verifica se o provedor atende ao tier de qualidade minimo."""
        # SEU CODIGO AQUI
        # frontier → aceita frontier
        # enterprise → aceita enterprise, frontier
        # fast → aceita qualquer tier
        pass


# ============================================================
# TASK ELIGIBILITY — define provedores elegiveis por tipo de tarefa
# ============================================================

TASK_ELIGIBLE_PROVIDERS = {
    TaskType.PRODUCT_SEARCH: {
        "primary": ["openai", "anthropic", "deepseek"],
        "min_quality_tier": QualityTier.FRONTIER,
        "max_latency_ms": 500,
    },
    TaskType.INTENT_CLASSIFY: {
        "primary": ["groq", "deepseek", "openai"],
        "min_quality_tier": QualityTier.FAST,
        "max_latency_ms": 100,
    },
    TaskType.RESPONSE_GEN: {
        "primary": ["anthropic", "openai", "deepseek"],
        "min_quality_tier": QualityTier.FRONTIER,
        "max_latency_ms": 800,
    },
}

# Fallback global: se todos os primarios falharem, tenta estes
GLOBAL_FALLBACK = ["azure"]


# ============================================================
# PROVIDER ROUTER — nucleo do exercicio
# ============================================================

@dataclass
class ProviderRouter:
    providers: dict[str, ProviderState] = field(default_factory=dict)
    route_log: list[str] = field(default_factory=list)
    circuit_breaker_cooldown_ms: int = 300_000  # 5 minutos

    def update_provider_state(self, state: ProviderState) -> None:
        """Atualiza o estado de um provedor no pool."""
        self.providers[state.name] = state

    def get_eligible_providers(self, task: Task) -> list[str]:
        """
        Retorna a lista de provedores elegiveis para uma tarefa,
        ordenada por prioridade (primarios primeiro, fallback depois).

        Filtra por:
        1. Tipo de tarefa (TASK_ELIGIBLE_PROVIDERS)
        2. Quality tier minimo
        3. Restricao de regiao do cliente
        4. Provedor disponivel (nao DOWN, circuito nao aberto)
        5. Latencia abaixo do maximo da tarefa
        """
        # SEU CODIGO AQUI
        pass

    def select_provider(self, task: Task, candidates: list[str]) -> Optional[str]:
        """
        Seleciona o melhor provedor entre os candidatos.

        Criterios em ordem:
        1. Capacidade < 85% (has_capacity_headroom)
        2. Se todos acima de 85%: escolhe o menos saturado
        3. Desempate por menor latencia
        """
        # SEU CODIGO AQUI
        pass

    def route(self, task: Task) -> dict:
        """
        Roteia uma tarefa para o melhor provedor disponivel.

        Fluxo completo:
        1. Obter provedores elegiveis para a tarefa
        2. Se nenhum elegivel: rejeitar com motivo
        3. Selecionar o melhor provedor entre os elegiveis
        4. Se o selecionado estiver > 85%: tentar fallback (max 3 tentativas)
        5. Se todos os elegiveis > 85% E prioridade LOW: enfileirar (backpressure)
        6. Para prioridade HIGH/CRITICAL: rotear para o menos saturado mesmo > 85%
        7. Registrar decisao no route_log
        8. Retornar dicionario com provider, status, reason

        Returns:
            {"provider": str|None, "status": "routed"|"queued"|"rejected", "reason": str}
        """
        # SEU CODIGO AQUI
        pass

    def apply_circuit_breaker(self, provider_name: str) -> None:
        """
        Abre o circuito de um provedor apos 3 medicoes consecutivas
        com status DOWN ou latencia > 2000ms.
        O circuito fecha automaticamente apos circuit_breaker_cooldown_ms.
        """
        provider = self.providers.get(provider_name)
        if not provider:
            return
        # SEU CODIGO AQUI
        pass

    def is_global_backpressure(self) -> bool:
        """Retorna True se TODOS os provedores disponiveis estao > 85%."""
        # SEU CODIGO AQUI
        pass

    def get_least_saturated(self, candidates: list[str]) -> Optional[str]:
        """Retorna o provedor com menor capacity_pct entre os candidatos."""
        # SEU CODIGO AQUI
        pass


# ============================================================
# TESTES RAPIDOS
# ============================================================

if __name__ == "__main__":
    # Setup: 5 provedores em estado inicial
    router = ProviderRouter()

    # Fixtures de provedores
    providers_fixture = [
        ProviderState("openai", QualityTier.FRONTIER, ProviderStatus.HEALTHY,
                      45.0, 2000, 60000, 280, ["us-east-1", "eu-west-1"]),
        ProviderState("anthropic", QualityTier.FRONTIER, ProviderStatus.HEALTHY,
                      38.0, 1500, 60000, 310, ["us-east-1", "eu-west-1"]),
        ProviderState("deepseek", QualityTier.FRONTIER, ProviderStatus.HEALTHY,
                      60.0, 3000, 60000, 400, ["us-east-1"]),
        ProviderState("groq", QualityTier.FAST, ProviderStatus.HEALTHY,
                      22.0, 25000, 60000, 45, ["us-east-1", "eu-west-1", "ap-south-1"]),
        ProviderState("azure", QualityTier.ENTERPRISE, ProviderStatus.HEALTHY,
                      30.0, 8000, 60000, 350, ["us-east-1", "eu-west-1", "ap-south-1", "sa-east-1"]),
    ]
    for p in providers_fixture:
        router.update_provider_state(p)

    # Teste 1: Roteamento normal — product_search vai para frontier
    task1 = Task("T-001", TaskType.PRODUCT_SEARCH, "regular_customer",
                 TaskPriority.HIGH, 500, QualityTier.FRONTIER)
    result = router.route(task1)
    print(f"Teste 1: {result}")
    assert result["status"] == "routed", f"Esperado routed, obtido {result['status']}"
    assert result["provider"] in ["openai", "anthropic", "deepseek"], \
        f"product_search deve ir para frontier, nao {result['provider']}"
    print("  OK: product_search roteado para frontier")

    # Teste 2: intent_classify prioriza latencia → Groq (45ms)
    task2 = Task("T-002", TaskType.INTENT_CLASSIFY, "regular_customer",
                 TaskPriority.HIGH, 100, QualityTier.FAST)
    result2 = router.route(task2)
    print(f"Teste 2: {result2}")
    assert result2["provider"] == "groq", \
        f"intent_classify deve priorizar Groq (menor latencia), obtido {result2['provider']}"
    print("  OK: intent_classify roteado para Groq")

    # Teste 3: Restricao de regiao enterprise — sa-east-1 so Azure
    task3 = Task("T-003", TaskType.PRODUCT_SEARCH, "enterprise_br",
                 TaskPriority.CRITICAL, 500, QualityTier.FRONTIER,
                 cloud_region_constraint="sa-east-1")
    result3 = router.route(task3)
    print(f"Teste 3: {result3}")
    assert result3["provider"] == "azure", \
        f"Cliente sa-east-1 deve ir para Azure, obtido {result3['provider']}"
    print("  OK: restricao de regiao respeitada")

    # Teste 4: Backpressure — todos provedores > 85%
    for name in router.providers:
        router.providers[name].capacity_pct = 92.0
    task4 = Task("T-004", TaskType.PRODUCT_SEARCH, "regular_customer",
                 TaskPriority.LOW, 500, QualityTier.FRONTIER)
    result4 = router.route(task4)
    print(f"Teste 4: {result4}")
    assert result4["status"] == "queued", \
        f"Tarefa LOW em backpressure deve ser enfileirada, obtido {result4['status']}"
    print("  OK: backpressure ativado para prioridade LOW")

    # Teste 5: Tarefa CRITICAL fura backpressure
    task5 = Task("T-005", TaskType.RESPONSE_GEN, "vip_customer",
                 TaskPriority.CRITICAL, 800, QualityTier.FRONTIER)
    result5 = router.route(task5)
    print(f"Teste 5: {result5}")
    assert result5["status"] == "routed", \
        f"Tarefa CRITICAL deve furar backpressure, obtido {result5['status']}"
    print("  OK: prioridade CRITICAL fura backpressure")

    # Teste 6: Circuit breaker
    for _ in range(3):
        groq = router.providers["groq"]
        groq.status = ProviderStatus.DOWN
        groq.consecutive_failures += 1
    router.apply_circuit_breaker("groq")
    assert not router.providers["groq"].is_available(), \
        "Groq deve estar indisponivel apos 3 falhas consecutivas"
    print("  OK: circuit breaker aberto para Groq")

    print(f"\nRoute log ({len(router.route_log)} entradas):")
    for entry in router.route_log:
        print(f"  {entry}")

    print("\n" + "=" * 60)
    print("TODOS OS TESTES DO PROVIDER ROUTER PASSARAM")
    print("=" * 60)
```

---

### Parte 3: Simular Black Friday com Load Distribution (25 min)

```python
# ============================================================
# SIMULACAO: Black Friday com 5 provedores
# ============================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("SIMULACAO: BLACK FRIDAY — DISTRIBUICAO MULTI-PROVEDOR")
    print("=" * 60)

    # Reset: restaurar capacidades saudaveis para todos provedores
    for p in providers_fixture:
        router.update_provider_state(p)

    # Gerar 200 tarefas simuladas (amostra dos 80 mil)
    import random
    random.seed(42)

    tasks = []
    for i in range(200):
        ttype = random.choice(list(TaskType))
        priority = random.choices(
            [TaskPriority.LOW, TaskPriority.HIGH, TaskPriority.CRITICAL],
            weights=[0.6, 0.3, 0.1]
        )[0]
        region = random.choice([None, None, None, "eu-west-1", "sa-east-1"])

        task = Task(
            task_id=f"T-{i:04d}",
            type=ttype,
            customer_id=f"cust_{random.randint(1, 50)}",
            priority=priority,
            max_latency_ms=500 if ttype != TaskType.INTENT_CLASSIFY else 100,
            min_quality_tier=QualityTier.FRONTIER if ttype != TaskType.INTENT_CLASSIFY else QualityTier.FAST,
            cloud_region_constraint=region,
            payload_tokens=random.randint(500, 3000),
        )
        tasks.append(task)

    # Roteamento simulado — a cada 20 tarefas, degradar um provedor
    results = {"routed": 0, "queued": 0, "rejected": 0}
    provider_hits = {name: 0 for name in router.providers}

    for idx, task in enumerate(tasks):
        # Simular degradacao progressiva
        if idx % 40 == 0 and idx > 0:
            victim = list(router.providers.keys())[idx // 40 % 5]
            router.providers[victim].capacity_pct = min(98.0, router.providers[victim].capacity_pct + 25.0)

        result = router.route(task)
        results[result["status"]] += 1
        if result["provider"]:
            provider_hits[result["provider"]] += 1

    print(f"\nRESULTADOS DA SIMULACAO (200 tarefas):")
    print(f"  Roteadas: {results['routed']}")
    print(f"  Enfileiradas (backpressure): {results['queued']}")
    print(f"  Rejeitadas: {results['rejected']}")
    print(f"\nDISTRIBUICAO POR PROVEDOR:")
    for name, hits in sorted(provider_hits.items(), key=lambda x: -x[1]):
        pct = hits / max(results['routed'], 1) * 100
        print(f"  {name:12s}: {hits:3d} tarefas ({pct:5.1f}%)")

    # VERIFICACAO: Nenhuma tarefa deveria ter sido rejeitada se ha provedores
    assert results["rejected"] == 0, \
        f"Com 5 provedores, nenhuma tarefa deveria ser rejeitada. Rejeitadas: {results['rejected']}"
    print(f"\n  VERIFICACAO: 0 rejeicoes com 5 provedores — OK")
```

---

## Validacao: Criterios de Aceitacao

Seu codigo sera considerado **APROVADO** quando:

### Criterio 1: Diagnostico (Parte 1)

- [ ] Voce calculou o throughput necessario por minuto na Black Friday
- [ ] Voce identificou o deficit de capacidade do provedor unico
- [ ] Voce calculou a capacidade combinada com 3 provedores
- [ ] Voce estimou a economia de latencia com roteamento por task type

### Criterio 2: ProviderRouter core

- [ ] `get_eligible_providers()` filtra corretamente por task type, quality tier, regiao e disponibilidade
- [ ] `select_provider()` prioriza provedores com folga de capacidade
- [ ] `route()` implementa o fluxo completo com fallback em cadeia
- [ ] Restricao de regiao enterprise e respeitada (`sa-east-1` → apenas Azure)

### Criterio 3: Backpressure e prioridades

- [ ] Tarefas LOW sao enfileiradas quando todos provedores > 85%
- [ ] Tarefas CRITICAL furam backpressure e sao roteadas para o menos saturado
- [ ] `is_global_backpressure()` detecta corretamente saturacao total

### Criterio 4: Circuit breaker

- [ ] Apos 3 falhas consecutivas, provedor e removido do pool
- [ ] Circuito fecha automaticamente apos cooldown (5 min na simulacao)

### Criterio 5: Simulacao Black Friday

- [ ] 200 tarefas distribuidas entre 5 provedores
- [ ] Zero rejeicoes com provedores disponiveis
- [ ] Route log documenta cada decisao

---

## Rubrica de Avaliacao

| Criterio | Peso | Insuficiente (0-3) | Basico (4-6) | Proficiente (7-8) | Excelente (9-10) |
|---|---|---|---|---|---|
| **Diagnostico (Parte 1)** | 15% | Nao identificou o deficit de capacidade | Identificou deficit mas sem calculos | Calculos completos com throughput e latencia | Analise de sensibilidade com diferentes combinacoes de provedores |
| **Router core (Parte 2)** | 40% | Nao implementado ou hardcoded | Roteia mas ignora regiao ou quality tier | Roteamento completo com fallback | Circuit breaker + backpressure + route log detalhado |
| **Simulacao (Parte 3)** | 30% | Nao executou | Simulacao parcial sem degradacao | Simulacao com degradacao progressiva e distribuicao | Simulacao com metricas de resiliencia (uptime, latencia p95) |
| **Testes e verificacao** | 15% | Nenhum cenario passa | 3 criterios passam | 4 criterios passam | Todos os 5 criterios passam |

**Nota final:** Media ponderada. **Aprovacao:** >= 7.0

---

## Dicas para Implementacao

### Para o Roteador

1. **A ordem dos fallbacks importa.** O primario deve ser o melhor provedor para a tarefa (menor latencia, maior capacidade). O secundario deve ser o proximo melhor que atende aos mesmos criterios. Nao e aleatorio -- e uma cadeia de preferencia declinante.

2. **Regiao e um hard constraint.** Se um cliente enterprise exige `sa-east-1` e nenhum provedor frontier atende, a tarefa NAO pode ser roteada para um provedor `us-east-1` -- isso violaria o contrato enterprise. O roteador deve rejeitar a tarefa com `region_constraint_violation`.

3. **Backpressure nao e rejeicao.** Enfileirar uma tarefa LOW durante saturacao e diferente de rejeita-la. A fila permite que a tarefa seja processada quando a capacidade voltar. Rejeicao e falha permanente.

### Para o Circuit Breaker

1. **Consecutive failures, nao total failures.** 3 falhas consecutivas abrem o circuito. 3 falhas em 1000 chamadas com sucessos intercalados nao abrem -- isso seria um falso positivo.

2. **O cooldown e um timer, nao um contador.** Apos 5 minutos, o circuito fecha automaticamente -- nao depende de um health check externo. Isso evita que um provedor fique permanentemente fora do pool por uma rajada de falhas transitorias.

---

## Duvidas Comuns

**P: Isso nao e so um load balancer?**
R: E mais que um load balancer. Um load balancer distribui uniformemente. O ProviderRouter toma decisoes baseadas em: tipo de tarefa (product_search vs intent_classify), quality tier minimo (frontier vs fast), restricoes de regiao enterprise, e prioridade da tarefa. Um load balancer nao sabe o que e uma tarefa de `intent_classify` nem que ela pode ir para Groq enquanto `product_search` precisa de frontier.

**P: Por que nao usar um unico provedor com auto-scaling?**
R: Auto-scaling resolve capacidade, mas nao resolve: (a) vendor lock-in, (b) restricoes de regiao enterprise que um unico provedor pode nao atender, (c) outages de provedor (single point of failure). Multi-provider routing e sobre resiliencia arquitetural, nao apenas sobre escala.

**P: Como isso se relaciona com o Neutral Selection Layer?**
R: O Neutral Selection Layer (`docs/canonical/neutral-selection-layer.md`) define o formato model-agnostic de contexto que permite trocar de provedor sem reescrever prompts. O ProviderRouter e a camada de decisao que escolhe QUAL provedor usar. Eles sao complementares: o Neutral Selection Layer garante que o prompt funciona em qualquer provedor; o ProviderRouter decide qual provedor recebe o prompt.

---

## Proximo Passo

Depois de completar este exercicio:
1. Leia `[[docs/canonical/model-switching-architecture-enterprise-eval-gate|Model-Switching Architecture]]` para entender como evals garantem que a troca de provedor nao degrada qualidade
2. Leia `[[docs/canonical/neutral-selection-layer|Neutral Selection Layer]]` para entender o formato model-agnostic de contexto
3. (Opcional) Estenda o roteador com `cost_aware_routing`: adicione precos por token para cada provedor e otimize roteamento por custo total

---

*Exercicio Multi-Provider Routing | Nivel 2 - Padroes Praticos*

**Um provedor e um ponto unico de falha. Cinco provedores sao um pool de capacidade.**
