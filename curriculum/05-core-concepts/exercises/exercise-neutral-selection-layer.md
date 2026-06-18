---
title: "Exercicio: Implementar uma Neutral Selection Layer para Contexto Multi-Modelo"
type: exercise
level: "N3"
aliases: ["neutral selection layer", "model-agnostic context", "vendor-independent selection", "context router", "multi-tenant registry", "vendor adapter", "portable context format"]
tags: [curriculo-conteudo, context-engineering, agentes-orquestracao, harness-engineering]
duration: "2-3h"
relates-to: ["[[docs/analysis/2026-06-18-memory-selection-problem/2026-06-18-memory-selection-problem-patterns|Memory Selection Patterns]]", "[[docs/analysis/2026-06-18-memory-selection-problem/2026-06-18-memory-selection-problem-classification|Memory Selection Classification]]", "[[docs/canonical/llm-as-fuzzy-compiler|LLM as Fuzzy Compiler]]", "[[docs/canonical/hybrid-context-stack|Hybrid Context Stack]]", "[[docs/canonical/versioned-durable-agent-state|Versioned Durable Agent State]]"]
last_updated: 2026-06-18
---
# Exercicio: Implementar uma Neutral Selection Layer para Contexto Multi-Modelo
## Nivel 3 - Arquitetura Avancada

## Objetivo

Implementar uma camada de selecao de contexto independente de vendor que traduz contexto entre formatos nativos de diferentes modelos, mantendo um registro multi-tenant e garantindo que o ativo mais duravel da organizacao — o contexto — sobreviva a migracoes de modelo.

**Tempo Estimado:** 2-3 horas
**Dificuldade:** Avancado
**Pre-requisito:** Ter lido `[[docs/canonical/llm-as-fuzzy-compiler|LLM as Fuzzy Compiler]]`, `[[docs/canonical/hybrid-context-stack|Hybrid Context Stack]]` e `[[docs/canonical/versioned-durable-agent-state|Versioned Durable Agent State]]`
**Objetivo:** Implementar uma `NeutralSelectionLayer` com formato agnostico de contexto, `ContextRouter` para queries multi-agente, `MultiTenantRegistry` com isolamento, e `VendorAdapter` para traducao entre formatos.

---

## Prologo: O Contexto Que Virou Refem

### Quinta-feira, 16h. Sala de arquitetura.

```
CTO: "O time de AI quer migrar do GPT-5 para o Claude-5.
     Benchmark mostra 23% menos alucinacao em diagnosticos
     medicos. A migracao e para semana que vem."
```

O time de plataforma da **MedAssist** tinha construido um agente de triagem medica que operava desde janeiro. O agente acumulava contexto de cada sessao — historico do paciente, diagnosticos diferenciais, exames solicitados, contraindicacoes — e armazenava tudo usando a API nativa de memoria do modelo atual.

Eram 47,000 sessoes. O contexto acumulado era o ativo mais valioso da organizacao: patterns de diagnostico que nao estavam em nenhum textbook, correlacoes entre sintomas que so emergiam com escala.

```
═══════════════════════════════════════════════════════════════
        RELATORIO DE IMPACTO — MIGRACAO DE MODELO
═══════════════════════════════════════════════════════════════

CONTEXTO ACUMULADO:
  Sessoes:          47,000
  Unidades de contexto: ~1,200,000
  Formato atual:    GPT-5 Memory API (proprietario)

PROBLEMA:
  O contexto foi armazenado no formato nativo do GPT-5.
  A API de memoria do Claude-5 tem schema DIFERENTE.
  Migrar 1.2M de unidades de contexto requer:
    - Mapear schema GPT-5 → Claude-5 (manual, 8 semanas)
    - Validar que nenhum contexto foi corrompido (2 semanas)
    - Rodar em shadow mode por 30 dias para garantir paridade

  Custo total da migracao: 16 semanas de engenharia.
  Enquanto isso, o time nao pode usar o Claude-5 em producao.

CAUSA RAIZ:
  O contexto — o ativo mais duravel da organizacao — foi
  soldado ao formato proprietario de um unico vendor.
  A decisao de "usar a API nativa de memoria porque e mais
  facil" transformou o contexto em refem do roadmap alheio.
═══════════════════════════════════════════════════════════════
```

```
ARQUITETA (post-mortem): "Contexto e o ativo mais duravel que uma
                          organizacao agentica produz. Modelos mudam.
                          APIs mudam. Vendors mudam. O contexto
                          precisa sobreviver a tudo isso.
                          
                          O que faltava: uma Neutral Selection Layer.
                          Um formato agnostico de contexto que qualquer
                          modelo consome. Um ContextRouter que qualquer
                          agente consulta. Um VendorAdapter que traduz
                          do formato agnostico para o formato nativo
                          de cada modelo — e vice-versa."
```

**O que teria evitado tudo:**

> Neutral Selection Layer: uma camada de selecao de contexto que desacopla o armazenamento do contexto (formato agnostico) do consumo do contexto (formato nativo de cada modelo). O contexto e armazenado uma vez em formato padronizado. Cada modelo recebe uma traducao sob medida. Migrar de vendor significa apenas escrever um novo adapter — nao reescrever 1.2M de unidades de contexto.

**Sua missao:** Construir uma `NeutralSelectionLayer` que implementa exatamente essa independencia de vendor.

---

## Cenario: Multi-Model Context Selection na MedAssist

### Contexto

Voce e o engenheiro de plataforma responsavel pela migracao de modelo na **MedAssist**. A organizacao opera tres agentes que usam modelos diferentes:

| Agente | Modelo Atual | Proposito | Sessoes |
|---|---|---|---|
| `triage-agent` | GPT-5 (OpenAI) | Triagem inicial de pacientes | 47,000 |
| `specialist-agent` | Claude-4 (Anthropic) | Diagnosticos especializados | 12,000 |
| `followup-agent` | Gemini-2 (Google) | Follow-up pos-consulta | 8,300 |

Cada agente gera e consome contexto em seu proprio formato nativo. Quando um paciente passa pela triagem (GPT-5) e depois ve um especialista (Claude-4), o contexto da triagem deveria estar disponivel para o especialista — mas na pratica, os formatos sao incompativeis e o contexto se perde na transicao.

O CTO determinou que a plataforma deve:
1. Migrar `triage-agent` de GPT-5 para Claude-5 em 4 semanas (nao 16).
2. Permitir que qualquer agente consulte contexto de qualquer sessao, independente do modelo que a gerou.
3. Garantir que proximas migracoes de modelo custem dias, nao meses.

### Arquitetura da Neutral Selection Layer

```
┌──────────────────────────────────────────────────────────────────────┐
│                     NEUTRAL SELECTION LAYER                            │
│                                                                        │
│  ┌──────────────────────────────────────────────────────────────────┐ │
│  │               MODEL-AGNOSTIC CONTEXT FORMAT                       │ │
│  │                                                                    │ │
│  │  {                                                                 │ │
│  │    "context_id": "ctx-4f7a2b",                                    │ │
│  │    "session_id": "ses-2026-06-18-001",                            │ │
│  │    "agent_id": "triage-agent",                                     │ │
│  │    "model_id": "gpt-5",                                           │ │
│  │    "kind": "patient_history",                                      │ │
│  │    "content": {                                                    │ │
│  │      "text": "Paciente relata dor toracica ha 3 dias...",         │ │
│  │      "structured": {"symptom": "dor_toracica", "duration_days": 3}│ │
│  │    },                                                              │ │
│  │    "metadata": {                                                   │ │
│  │      "timestamp": "2026-06-18T14:30:00Z",                         │ │
│  │      "relevance_tags": ["cardiovascular", "urgencia"],            │ │
│  │      "provenance": "triage-agent step 3"                           │ │
│  │    },                                                              │ │
│  │    "tenant": "medassist-producao"                                  │ │
│  │  }                                                                 │ │
│  └──────────────────────────────────────────────────────────────────┘ │
│                                                                        │
│  ┌─────────────────┐  ┌──────────────────┐  ┌─────────────────────┐  │
│  │ Context Router   │  │ Multi-Tenant      │  │ Vendor Adapters     │  │
│  │                  │  │ Registry          │  │                     │  │
│  │ Recebe queries   │  │                   │  │ GPT-5 ↔ agnostic   │  │
│  │ de qualquer      │  │ Isola contexto    │  │ Claude-5 ↔ agnostic│  │
│  │ agente/modelo    │  │ por tenant        │  │ Gemini ↔ agnostic  │  │
│  └────────┬─────────┘  └────────┬──────────┘  └──────────┬──────────┘  │
│           │                      │                         │             │
└───────────┼──────────────────────┼─────────────────────────┼─────────────┘
            │                      │                         │
            ▼                      ▼                         ▼
    ┌──────────────┐     ┌──────────────┐          ┌──────────────┐
    │ GPT-5 Agent  │     │ Claude Agent │          │ Gemini Agent │
    │ (triagem)    │     │ (especialista)│         │ (follow-up)  │
    └──────────────┘     └──────────────┘          └──────────────┘
```

### Dados de Entrada

Voce recebe um lote de contexto de tres sessoes que atravessaram multiplos agentes:

```json
{
  "session_id": "ses-2026-06-18-001",
  "patient_id": "PAT-8842",
  "context_units": [
    {
      "context_id": "ctx-001",
      "agent_id": "triage-agent",
      "model_id": "gpt-5",
      "kind": "patient_history",
      "content": {"text": "Paciente 67 anos, hipertenso, dor toracica ha 3 dias"},
      "native_format": "gpt5_memory_api_v2"
    },
    {
      "context_id": "ctx-002",
      "agent_id": "triage-agent",
      "model_id": "gpt-5",
      "kind": "differential_diagnosis",
      "content": {"text": "DDx: 1) Angina instavel 2) IAM 3) Ansiedade"},
      "native_format": "gpt5_memory_api_v2"
    },
    {
      "context_id": "ctx-003",
      "agent_id": "specialist-agent",
      "model_id": "claude-4",
      "kind": "exam_request",
      "content": {"text": "Solicitar: ECG, Troponina, Raio-X torax"},
      "native_format": "claude_memory_v1"
    },
    {
      "context_id": "ctx-004",
      "agent_id": "specialist-agent",
      "model_id": "claude-4",
      "kind": "contraindication",
      "content": {"text": "Paciente alergico a contraste iodado"},
      "native_format": "claude_memory_v1"
    },
    {
      "context_id": "ctx-005",
      "agent_id": "followup-agent",
      "model_id": "gemini-2",
      "kind": "followup_plan",
      "content": {"text": "Retorno em 7 dias. Monitorar pressao arterial."},
      "native_format": "gemini_context_v3"
    }
  ]
}
```

Note que `ctx-001` e `ctx-002` estao em formato GPT-5; `ctx-003` e `ctx-004` em formato Claude-4; `ctx-005` em formato Gemini-2. Nenhum agente consegue ler contexto de outro sem adaptacao.

---

## Requisitos

### Requisitos Funcionais

1. **RF1 - Formato agnostico canonico:** Definir um `AgnosticContextUnit` que representa qualquer contexto independente de vendor. Campos minimos: `context_id`, `session_id`, `agent_id`, `model_id`, `kind`, `content` (texto + dados estruturados), `metadata`.
2. **RF2 - Multi-Tenant Registry:** O `MultiTenantRegistry` armazena contexto por tenant (`medassist-producao`, `medassist-staging`) com isolamento. Queries em um tenant nunca retornam contexto de outro.
3. **RF3 - Vendor Adapters:** Cada vendor tem um adapter que traduz: `to_agnostic()` (nativo → agnostico) e `to_native()` (agnostico → nativo). Adapters implementam uma interface comum.
4. **RF4 - Context Router:** O `ContextRouter` recebe queries de qualquer agente (ex: "contexto do paciente PAT-8842 nas ultimas 24h") e retorna resultados em formato agnostico. O agente que consome entao usa o VendorAdapter para traduzir ao seu formato nativo.
5. **RF5 - Migracao de modelo como operacao O(1):** Migrar um agente de um modelo para outro requer apenas trocar o `VendorAdapter` associado ao agente — zero migracao de dados.
6. **RF6 - Audibilidade cross-tenant:** Operacoes de leitura e escrita no registry sao registradas com `(timestamp, agent_id, operation, context_id)` para auditoria.

### Requisitos Tecnicos

1. **RT1 - Python puro:** Implementacao em Python com stdlib + dataclasses.
2. **RT2 - Interface de adapter estrita:** Todo `VendorAdapter` implementa `to_agnostic(raw_context: dict) -> AgnosticContextUnit` e `to_native(agnostic: AgnosticContextUnit) -> dict`.
3. **RT3 - Isolamento de tenant sem leaks:** O router so acessa contexto se `agent.tenant == context.tenant`.
4. **RT4 - Traducao reversivel:** `to_agnostic(to_native(unit)) == unit` para todos os adapters (round-trip property).

---

## Sua Tarefa

Voce vai implementar a `NeutralSelectionLayer` em 3 partes.

---

### Parte 1: Diagnosticar o Vendor Lock-In (15 min)

Analise o cenario de migracao da MedAssist. Responda:

1. Quantas unidades de contexto precisariam ser migradas se o `triage-agent` mudar de GPT-5 para Claude-5?
2. Quais unidades de contexto sao inacessiveis ao `specialist-agent` (Claude-4) no formato atual?
3. Se a Neutral Selection Layer ja estivesse implementada, qual seria o esforco de migracao (em passos concretos)?

```python
# Contexto atual da MedAssist antes da migracao
# Formato: (context_id, agent_id, model_id, kind, native_format, tenant)

MEDASSIST_CONTEXT_INVENTORY = [
    # Agente de triagem (GPT-5) — sera migrado para Claude-5
    ("ctx-001", "triage-agent",    "gpt-5",    "patient_history",        "gpt5_memory_api_v2",  "medassist-producao"),
    ("ctx-002", "triage-agent",    "gpt-5",    "differential_diagnosis", "gpt5_memory_api_v2",  "medassist-producao"),
    ("ctx-003", "triage-agent",    "gpt-5",    "vital_signs",            "gpt5_memory_api_v2",  "medassist-producao"),
    ("ctx-004", "triage-agent",    "gpt-5",    "medication_list",        "gpt5_memory_api_v2",  "medassist-producao"),
    ("ctx-005", "triage-agent",    "gpt-5",    "chief_complaint",        "gpt5_memory_api_v2",  "medassist-producao"),
    # Agente especialista (Claude-4)
    ("ctx-006", "specialist-agent","claude-4", "exam_request",           "claude_memory_v1",    "medassist-producao"),
    ("ctx-007", "specialist-agent","claude-4", "contraindication",       "claude_memory_v1",    "medassist-producao"),
    ("ctx-008", "specialist-agent","claude-4", "specialist_opinion",     "claude_memory_v1",    "medassist-producao"),
    # Agente de follow-up (Gemini-2)
    ("ctx-009", "followup-agent",  "gemini-2", "followup_plan",          "gemini_context_v3",   "medassist-producao"),
    ("ctx-010", "followup-agent",  "gemini-2", "lifestyle_recommendation","gemini_context_v3",   "medassist-producao"),
    # Staging tenant
    ("ctx-011", "triage-agent",    "gpt-5",    "patient_history",        "gpt5_memory_api_v2",  "medassist-staging"),
    ("ctx-012", "specialist-agent","claude-4", "exam_request",           "claude_memory_v1",    "medassist-staging"),
]

# TAREFA: Responda no seu codigo como comentario:
#
# 1. Quantas unidades de contexto existem no tenant "medassist-producao"?
#    Quantas estao em formato GPT-5 e precisariam ser migradas se o
#    triage-agent mudar de modelo SEM a Neutral Selection Layer?
#
# 2. Quantas unidades de contexto o specialist-agent (Claude-4)
#    NAO consegue ler porque estao em formato GPT-5 ou Gemini?
#    Isso significa que o especialista esta tomando decisoes sem
#    acesso ao historico completo da triagem?
#
# 3. Com a Neutral Selection Layer, a migracao do triage-agent de
#    GPT-5 para Claude-5 envolveria:
#    a. Reescrever quantas unidades de contexto?
#    b. Alterar quantos VendorAdapters?
#    c. Quanto tempo de engenharia (comparado as 16 semanas)?
#
# 4. O contexto "ctx-011" (staging tenant) pode ser acessado por
#    um agente no tenant "medassist-producao"? Por que isso e
#    importante para seguranca de dados medicos?
```

---

### Parte 2: Implementar a NeutralSelectionLayer (70 min)

Implemente a camada de selecao neutra. Use este esqueleto:

```python
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


# ============================================================
# DATA MODELS
# ============================================================

class ContextKind(Enum):
    PATIENT_HISTORY = "patient_history"
    DIFFERENTIAL_DIAGNOSIS = "differential_diagnosis"
    EXAM_REQUEST = "exam_request"
    CONTRAINDICATION = "contraindication"
    VITAL_SIGNS = "vital_signs"
    MEDICATION_LIST = "medication_list"
    CHIEF_COMPLAINT = "chief_complaint"
    SPECIALIST_OPINION = "specialist_opinion"
    FOLLOWUP_PLAN = "followup_plan"
    LIFESTYLE_RECOMMENDATION = "lifestyle_recommendation"
    OTHER = "other"


@dataclass
class AgnosticContextUnit:
    """
    Formato canonico agnostico de contexto.

    Este e o "lingua franca" — todo contexto e armazenado neste
    formato, independente do modelo que o gerou. VendorAdapters
    traduzem de/para os formatos nativos.
    """
    context_id: str
    session_id: str
    agent_id: str
    model_id: str
    kind: ContextKind
    content: dict[str, Any]  # {"text": "...", "structured": {...}}
    metadata: dict[str, Any] = field(default_factory=dict)
    tenant: str = "default"
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, AgnosticContextUnit):
            return NotImplemented
        return (
            self.context_id == other.context_id
            and self.session_id == other.session_id
            and self.agent_id == other.agent_id
            and self.model_id == other.model_id
            and self.kind == other.kind
            and self.content == other.content
            and self.metadata == other.metadata
            and self.tenant == other.tenant
        )


# ============================================================
# VENDOR ADAPTER INTERFACE
# ============================================================

class VendorAdapter(ABC):
    """
    Interface que todo adapter de vendor deve implementar.

    Cada adapter sabe traduzir entre o formato agnostico e
    o formato nativo de um modelo especifico.
    """

    @property
    @abstractmethod
    def vendor_name(self) -> str:
        """Nome do vendor (ex: 'openai', 'anthropic', 'google')."""
        ...

    @property
    @abstractmethod
    def supported_models(self) -> list[str]:
        """Modelos suportados por este adapter (ex: ['gpt-5', 'gpt-4'])."""
        ...

    @abstractmethod
    def to_agnostic(self, raw_context: dict[str, Any]) -> AgnosticContextUnit:
        """
        Traduz contexto do formato nativo do vendor para o formato agnostico.

        Args:
            raw_context: Contexto no formato nativo do vendor.
                         Campos minimos esperados dependem do vendor.

        Returns:
            AgnosticContextUnit no formato canonico.
        """
        ...

    @abstractmethod
    def to_native(self, agnostic: AgnosticContextUnit) -> dict[str, Any]:
        """
        Traduz contexto do formato agnostico para o formato nativo do vendor.

        Args:
            agnostic: Unidade de contexto em formato canonico.

        Returns:
            Dicionario no formato nativo do vendor.
        """
        ...


# ============================================================
# VENDOR ADAPTERS — implementacoes concretas
# ============================================================

class OpenAIGPT5Adapter(VendorAdapter):
    """Adapter para GPT-5 (OpenAI)."""

    @property
    def vendor_name(self) -> str:
        return "openai"

    @property
    def supported_models(self) -> list[str]:
        return ["gpt-5", "gpt-4", "gpt-4-turbo"]

    def to_agnostic(self, raw_context: dict[str, Any]) -> AgnosticContextUnit:
        """
        Traduz do formato nativo GPT-5 para agnostico.

        Formato nativo GPT-5 esperado:
        {
            "memory_id": str,
            "thread_id": str,
            "agent": str,
            "model": str,
            "memory_type": str,
            "body": {"text": str, "data": dict},
            "meta": dict,
            "org_id": str,
        }
        """
        # SEU CODIGO AQUI
        pass

    def to_native(self, agnostic: AgnosticContextUnit) -> dict[str, Any]:
        """
        Traduz do formato agnostico para GPT-5 nativo.
        """
        # SEU CODIGO AQUI
        pass


class AnthropicClaudeAdapter(VendorAdapter):
    """Adapter para Claude-4 e Claude-5 (Anthropic)."""

    @property
    def vendor_name(self) -> str:
        return "anthropic"

    @property
    def supported_models(self) -> list[str]:
        return ["claude-4", "claude-5", "claude-opus"]

    def to_agnostic(self, raw_context: dict[str, Any]) -> AgnosticContextUnit:
        """
        Traduz do formato nativo Claude para agnostico.

        Formato nativo Claude esperado:
        {
            "context_ref": str,
            "conversation_id": str,
            "actor_id": str,
            "model_version": str,
            "context_type": str,
            "blocks": [{"text": str, "data": dict}],
            "annotations": dict,
            "workspace_id": str,
        }
        """
        # SEU CODIGO AQUI
        pass

    def to_native(self, agnostic: AgnosticContextUnit) -> dict[str, Any]:
        """
        Traduz do formato agnostico para Claude nativo.
        """
        # SEU CODIGO AQUI
        pass


class GoogleGeminiAdapter(VendorAdapter):
    """Adapter para Gemini-2 (Google)."""

    @property
    def vendor_name(self) -> str:
        return "google"

    @property
    def supported_models(self) -> list[str]:
        return ["gemini-2", "gemini-pro"]

    def to_agnostic(self, raw_context: dict[str, Any]) -> AgnosticContextUnit:
        """
        Traduz do formato nativo Gemini para agnostico.

        Formato nativo Gemini esperado:
        {
            "context_id": str,
            "project_id": str,
            "agent_name": str,
            "model_id": str,
            "context_category": str,
            "parts": [{"text": str, "structured_data": dict}],
            "labels": dict,
            "environment": str,
        }
        """
        # SEU CODIGO AQUI
        pass

    def to_native(self, agnostic: AgnosticContextUnit) -> dict[str, Any]:
        """
        Traduz do formato agnostico para Gemini nativo.
        """
        # SEU CODIGO AQUI
        pass


# ============================================================
# MULTI-TENANT REGISTRY
# ============================================================

@dataclass
class AuditEntry:
    """Entrada de auditoria para operacoes no registry."""
    timestamp: str
    agent_id: str
    operation: str  # "write", "read", "delete"
    context_id: str
    tenant: str


@dataclass
class MultiTenantRegistry:
    """
    Registro de contexto com isolamento por tenant.

    Armazena contexto em formato agnostico e garante que
    queries em um tenant nunca acessam contexto de outro.
    """

    # context_id → AgnosticContextUnit
    _store: dict[str, AgnosticContextUnit] = field(default_factory=dict)
    # context_id → tenant
    _tenant_index: dict[str, str] = field(default_factory=dict)
    # Lista de auditoria
    _audit_log: list[AuditEntry] = field(default_factory=list)

    def write(self, unit: AgnosticContextUnit, agent_id: str) -> None:
        """
        Armazena uma unidade de contexto no registro.

        Args:
            unit: Unidade em formato agnostico.
            agent_id: ID do agente que esta escrevendo.
        """
        # SEU CODIGO AQUI
        #
        # 1. Armazenar unit em _store por context_id
        # 2. Indexar tenant em _tenant_index
        # 3. Registrar AuditEntry de "write"
        pass

    def read(self, context_id: str, agent_tenant: str, agent_id: str) -> AgnosticContextUnit | None:
        """
        Le uma unidade de contexto, verificando isolamento de tenant.

        Args:
            context_id: ID da unidade.
            agent_tenant: Tenant do agente que esta lendo.
            agent_id: ID do agente.

        Returns:
            AgnosticContextUnit se encontrada e tenant compativel, None caso contrario.

        Raises:
            TenantIsolationError: Se o tenant do contexto nao corresponde ao do agente.
        """
        # SEU CODIGO AQUI
        #
        # 1. Buscar unit em _store
        # 2. Verificar tenant da unit vs. agent_tenant
        # 3. Se tenants diferentes: levantar TenantIsolationError
        # 4. Registrar AuditEntry de "read"
        # 5. Retornar unit
        pass

    def query_by_session(self, session_id: str, agent_tenant: str) -> list[AgnosticContextUnit]:
        """
        Retorna todo contexto de uma sessao no tenant do agente.

        Args:
            session_id: ID da sessao.
            agent_tenant: Tenant do agente consultando.

        Returns:
            Lista de AgnosticContextUnit da sessao no tenant.
        """
        # SEU CODIGO AQUI
        pass

    def query_by_agent(self, agent_id: str, agent_tenant: str) -> list[AgnosticContextUnit]:
        """
        Retorna todo contexto gerado por um agente no tenant.

        Args:
            agent_id: ID do agente.
            agent_tenant: Tenant do agente consultando.

        Returns:
            Lista de AgnosticContextUnit geradas pelo agente no tenant.
        """
        # SEU CODIGO AQUI
        pass

    def get_audit_trail(self, tenant: str | None = None) -> list[AuditEntry]:
        """
        Retorna a trilha de auditoria, opcionalmente filtrada por tenant.

        Args:
            tenant: Filtrar por tenant (None = todos).

        Returns:
            Lista de AuditEntry.
        """
        # SEU CODIGO AQUI
        pass

    def tenant_stats(self) -> dict[str, int]:
        """
        Retorna contagem de unidades por tenant.

        Returns:
            {"medassist-producao": N, "medassist-staging": M}
        """
        # SEU CODIGO AQUI
        pass


# ============================================================
# TENANT ISOLATION ERROR
# ============================================================

class TenantIsolationError(Exception):
    """Violacao de isolamento de tenant."""
    pass


# ============================================================
# CONTEXT ROUTER
# ============================================================

@dataclass
class AgentRegistration:
    """Registro de um agente na plataforma."""
    agent_id: str
    tenant: str
    current_model: str  # modelo atual do agente


@dataclass
class ContextRouter:
    """
    Roteador de queries de contexto.

    Recebe queries de qualquer agente, resolve qual adapter usar
    baseado no modelo do agente, e retorna contexto no formato
    apropriado.
    """

    registry: MultiTenantRegistry
    adapters: dict[str, VendorAdapter] = field(default_factory=dict)
    agents: dict[str, AgentRegistration] = field(default_factory=dict)

    def register_adapter(self, adapter: VendorAdapter) -> None:
        """
        Registra um VendorAdapter.

        O adapter e indexado por vendor_name e por cada model
        que suporta.
        """
        # SEU CODIGO AQUI
        pass

    def register_agent(self, agent: AgentRegistration) -> None:
        """Registra um agente na plataforma."""
        # SEU CODIGO AQUI
        pass

    def get_adapter_for_model(self, model_id: str) -> VendorAdapter | None:
        """
        Resolve o VendorAdapter para um modelo especifico.

        Returns:
            VendorAdapter ou None se o modelo nao tem adapter.
        """
        # SEU CODIGO AQUI
        pass

    def ingest_context(self, agent_id: str, raw_context: dict[str, Any]) -> AgnosticContextUnit | None:
        """
        Ingestao de contexto: agente gera contexto em formato nativo,
        router traduz para agnostico e armazena no registry.

        Args:
            agent_id: ID do agente gerando contexto.
            raw_context: Contexto no formato nativo do modelo do agente.

        Returns:
            AgnosticContextUnit armazenada, ou None se o agente/modelo
            nao tem adapter registrado.
        """
        # SEU CODIGO AQUI
        #
        # 1. Buscar AgentRegistration
        # 2. Resolver adapter para current_model do agente
        # 3. Traduzir raw → agnostic via adapter.to_agnostic()
        # 4. Garantir que tenant da unit = tenant do agente
        # 5. Armazenar no registry via registry.write()
        # 6. Retornar a unidade agnostica
        pass

    def query_context(
        self, agent_id: str, session_id: str | None = None, target_agent_id: str | None = None
    ) -> list[dict[str, Any]]:
        """
        Query de contexto: agente consulta contexto de uma sessao
        ou de outro agente. Router resolve tenant, busca no registry,
        e traduz para o formato nativo do agente consulente.

        Args:
            agent_id: ID do agente consultando.
            session_id: Filtrar por sessao (None = sem filtro).
            target_agent_id: Filtrar por agente gerador (None = sem filtro).

        Returns:
            Lista de contexto no formato nativo do agente consulente.
        """
        # SEU CODIGO AQUI
        #
        # 1. Buscar AgentRegistration
        # 2. Buscar contexto no registry:
        #    - Se session_id: registry.query_by_session()
        #    - Se target_agent_id: registry.query_by_agent()
        #    - Ambos: intersecao
        # 3. Resolver adapter para current_model do agente
        # 4. Traduzir cada unidade: adapter.to_native()
        # 5. Retornar lista de dicionarios nativos
        pass

    def migrate_agent_model(self, agent_id: str, new_model: str) -> bool:
        """
        Migra um agente para um novo modelo.

        Esta e a operacao que demonstra o valor da Neutral Selection Layer:
        - Zero migracao de dados
        - Apenas atualiza o current_model no AgentRegistration
        - Desde que exista um VendorAdapter para new_model

        Args:
            agent_id: ID do agente.
            new_model: Novo modelo.

        Returns:
            True se a migracao foi bem-sucedida, False se nao ha adapter.

        Raises:
            ValueError: Se o agente nao existe.
        """
        # SEU CODIGO AQUI
        pass


# ============================================================
# ROUND-TRIP TEST
# ============================================================

def test_round_trip(adapter: VendorAdapter, raw_context: dict[str, Any]) -> bool:
    """
    Verifica a propriedade de round-trip para um adapter.

    to_agnostic(to_native(unit)) == unit

    Returns:
        True se o round-trip preserva a unidade.
    """
    agnostic = adapter.to_agnostic(raw_context)
    native = adapter.to_native(agnostic)
    agnostic_again = adapter.to_agnostic(native)
    return agnostic == agnostic_again


# ============================================================
# TESTES RAPIDOS: NeutralSelectionLayer
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("TESTE DA NEUTRAL SELECTION LAYER")
    print("=" * 60)

    # Configurar sistema
    registry = MultiTenantRegistry()
    router = ContextRouter(registry=registry)

    # Registrar adapters
    router.register_adapter(OpenAIGPT5Adapter())
    router.register_adapter(AnthropicClaudeAdapter())
    router.register_adapter(GoogleGeminiAdapter())

    # Registrar agentes
    router.register_agent(AgentRegistration("triage-agent", "medassist-producao", "gpt-5"))
    router.register_agent(AgentRegistration("specialist-agent", "medassist-producao", "claude-4"))
    router.register_agent(AgentRegistration("followup-agent", "medassist-producao", "gemini-2"))

    # Teste 1: Ingestao de contexto em formato GPT-5
    print(f"\nTeste 1: Ingestao de contexto GPT-5 via triage-agent")
    gpt5_raw = {
        "memory_id": "mem-001",
        "thread_id": "thread-pha-001",
        "agent": "triage-agent",
        "model": "gpt-5",
        "memory_type": "patient_history",
        "body": {"text": "Paciente 67 anos, hipertenso, dor toracica ha 3 dias", "data": {"age": 67, "condition": "hypertension"}},
        "meta": {"timestamp": "2026-06-18T14:30:00Z", "tags": ["cardiovascular", "urgencia"]},
        "org_id": "medassist-producao",
    }
    unit = router.ingest_context("triage-agent", gpt5_raw)
    assert unit is not None, "Ingestao deve retornar unidade agnostica"
    assert unit.kind == ContextKind.PATIENT_HISTORY
    assert unit.tenant == "medassist-producao"
    print(f"  OK: Contexto GPT-5 ingerido como agnostico: kind={unit.kind.value}, tenant={unit.tenant}")

    # Teste 2: Ingestao de contexto Claude-4
    print(f"\nTeste 2: Ingestao de contexto Claude-4 via specialist-agent")
    claude_raw = {
        "context_ref": "ctx-ref-002",
        "conversation_id": "thread-pha-001",
        "actor_id": "specialist-agent",
        "model_version": "claude-4",
        "context_type": "contraindication",
        "blocks": [{"text": "Paciente alergico a contraste iodado", "data": {"allergen": "iodine_contrast"}}],
        "annotations": {"severity": "critical", "source": "patient_record"},
        "workspace_id": "medassist-producao",
    }
    unit2 = router.ingest_context("specialist-agent", claude_raw)
    assert unit2 is not None
    print(f"  OK: Contexto Claude-4 ingerido como agnostico: kind={unit2.kind.value}")

    # Teste 3: Query cross-model — specialist-agent (Claude-4) consulta contexto do triage-agent (GPT-5)
    print(f"\nTeste 3: Cross-model query — Claude-4 le contexto gerado por GPT-5")
    native_contexts = router.query_context(
        agent_id="specialist-agent",
        target_agent_id="triage-agent"
    )
    assert len(native_contexts) > 0, "Specialist-agent deve conseguir ler contexto do triage-agent"
    assert isinstance(native_contexts[0], dict), "Resultado deve ser formato nativo Claude"
    print(f"  OK: Specialist-agent (Claude-4) leu {len(native_contexts)} unidades do triage-agent (GPT-5)")
    print(f"  Formato de saida: Claude nativo")

    # Teste 4: Tenant isolation — agente em staging nao pode acessar contexto de producao
    print(f"\nTeste 4: Isolamento de tenant — staging vs. producao")
    router.register_agent(AgentRegistration("staging-agent", "medassist-staging", "gpt-5"))

    # Ingerir contexto no tenant staging
    staging_raw = {
        "memory_id": "mem-stg-001",
        "thread_id": "thread-stg-001",
        "agent": "staging-agent",
        "model": "gpt-5",
        "memory_type": "patient_history",
        "body": {"text": "Dados de paciente staging", "data": {}},
        "meta": {"timestamp": "2026-06-18T15:00:00Z", "tags": []},
        "org_id": "medassist-staging",
    }
    router.ingest_context("staging-agent", staging_raw)

    # staging-agent tenta ler contexto de producao
    try:
        native = router.query_context(agent_id="staging-agent", target_agent_id="triage-agent")
        # Se nao levantou excecao, a lista deve estar vazia
        print(f"  Staging agent leu {len(native)} unidades — esperado 0 (isolamento)")
        assert len(native) == 0, "Staging agent nao deve acessar contexto de producao"
    except TenantIsolationError:
        print(f"  TenantIsolationError corretamente levantada")
    print(f"  OK: Isolamento de tenant funcionando")

    # Teste 5: Migracao de modelo — triage-agent migra de GPT-5 para Claude-5
    print(f"\nTeste 5: Migracao de modelo — GPT-5 → Claude-5")
    # Registrar adapter Claude-5 (usa o mesmo adapter Anthropic)
    assert router.migrate_agent_model("triage-agent", "claude-5"), "Migracao deve ser bem-sucedida"
    agent = router.agents["triage-agent"]
    assert agent.current_model == "claude-5", "Modelo deve ser atualizado"
    print(f"  OK: triage-agent migrado para {agent.current_model}")
    print(f"  Unidades de contexto migradas: 0 (zero migracao de dados)")
    print(f"  VendorAdapters alterados: 0 (Claude-5 usa mesmo adapter Anthropic)")

    # Teste 6: Round-trip property para GPT-5 adapter
    print(f"\nTeste 6: Round-trip GPT-5 adapter")
    gpt_adapter = router.get_adapter_for_model("gpt-5")
    assert gpt_adapter is not None
    round_trip_ok = test_round_trip(gpt_adapter, gpt5_raw)
    print(f"  Round-trip GPT-5: {'PASSOU' if round_trip_ok else 'FALHOU'}")
    assert round_trip_ok, "GPT-5 adapter deve preservar round-trip"

    # Teste 7: Audit trail
    print(f"\nTeste 7: Trilha de auditoria")
    audit = registry.get_audit_trail()
    print(f"  Total de operacoes registradas: {len(audit)}")
    assert len(audit) > 0, "Deve haver entradas de auditoria"
    # Verificar que operacoes de staging e producao sao distintas
    prod_ops = [e for e in audit if e.tenant == "medassist-producao"]
    stg_ops = [e for e in audit if e.tenant == "medassist-staging"]
    print(f"  Produção: {len(prod_ops)} operacoes")
    print(f"  Staging: {len(stg_ops)} operacoes")
    print(f"  OK: Auditoria funcionando")

    print("\n" + "=" * 60)
    print("TODOS OS TESTES DA NEUTRAL SELECTION LAYER PASSARAM")
    print("=" * 60)
```

---

### Parte 3: Simular a Migracao de Modelo com e sem Neutral Layer (35 min)

```python
# ============================================================
# SIMULACAO: Migracao GPT-5 → Claude-5
# ============================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("SIMULACAO: MIGRACAO GPT-5 → CLAUDE-5")
    print("=" * 60)

    # Configurar sistema completo com inventario da MedAssist
    registry = MultiTenantRegistry()
    router = ContextRouter(registry=registry)
    router.register_adapter(OpenAIGPT5Adapter())
    router.register_adapter(AnthropicClaudeAdapter())
    router.register_adapter(GoogleGeminiAdapter())

    router.register_agent(AgentRegistration("triage-agent", "medassist-producao", "gpt-5"))
    router.register_agent(AgentRegistration("specialist-agent", "medassist-producao", "claude-4"))
    router.register_agent(AgentRegistration("followup-agent", "medassist-producao", "gemini-2"))
    router.register_agent(AgentRegistration("staging-agent", "medassist-staging", "gpt-5"))

    # Ingerir todo o inventario (simplificado)
    ingested = 0
    for ctx_id, agent_id, model_id, kind_str, native_fmt, tenant in MEDASSIST_CONTEXT_INVENTORY:
        # Construir raw_context baseado no formato nativo
        if native_fmt == "gpt5_memory_api_v2":
            raw = {
                "memory_id": ctx_id, "thread_id": "ses-001", "agent": agent_id,
                "model": model_id, "memory_type": kind_str,
                "body": {"text": f"Content of {ctx_id}", "data": {}},
                "meta": {"timestamp": "2026-06-18T10:00:00Z", "tags": []},
                "org_id": tenant,
            }
        elif native_fmt == "claude_memory_v1":
            raw = {
                "context_ref": ctx_id, "conversation_id": "ses-001", "actor_id": agent_id,
                "model_version": model_id, "context_type": kind_str,
                "blocks": [{"text": f"Content of {ctx_id}", "data": {}}],
                "annotations": {}, "workspace_id": tenant,
            }
        else:  # gemini
            raw = {
                "context_id": ctx_id, "project_id": "medassist", "agent_name": agent_id,
                "model_id": model_id, "context_category": kind_str,
                "parts": [{"text": f"Content of {ctx_id}", "structured_data": {}}],
                "labels": {}, "environment": tenant,
            }

        result = router.ingest_context(agent_id, raw)
        if result:
            ingested += 1

    print(f"  Contexto ingerido: {ingested} unidades")

    # Estatisticas de tenant
    stats = registry.tenant_stats()
    print(f"  Distribuicao por tenant: {stats}")

    # ANTES da migracao: specialist-agent consulta contexto do triage-agent
    print(f"\nANTES DA MIGRACAO:")
    print(f"  triage-agent model: {router.agents['triage-agent'].current_model}")
    ctx_before = router.query_context("specialist-agent", target_agent_id="triage-agent")
    print(f"  Contexto do triage-agent acessivel ao specialist-agent: {len(ctx_before)} unidades")

    # MIGRAR triage-agent de GPT-5 para Claude-5
    print(f"\nMIGRANDO triage-agent: GPT-5 → Claude-5...")
    success = router.migrate_agent_model("triage-agent", "claude-5")
    print(f"  Migracao: {'SUCESSO' if success else 'FALHA'}")

    # DEPOIS da migracao: mesmo contexto, modelos diferentes
    print(f"\nDEPOIS DA MIGRACAO:")
    print(f"  triage-agent model: {router.agents['triage-agent'].current_model}")
    ctx_after = router.query_context("specialist-agent", target_agent_id="triage-agent")
    print(f"  Contexto do triage-agent acessivel ao specialist-agent: {len(ctx_after)} unidades")

    # Verificacao: o contexto sobreviveu a migracao?
    assert len(ctx_before) == len(ctx_after), (
        f"Migracao de modelo nao deve perder contexto: {len(ctx_before)} → {len(ctx_after)}"
    )

    print(f"\nCOMPARACAO: Com Neutral Layer vs. Sem Neutral Layer")
    print(f"  Sem Neutral Layer:")
    print(f"    - 5 unidades GPT-5 precisariam ser convertidas manualmente")
    print(f"    - Schema mapping GPT-5 → Claude-5: ~8 semanas")
    print(f"    - Validacao de integridade: ~2 semanas")
    print(f"    - Shadow mode: ~4 semanas")
    print(f"    - Custo total: ~16 semanas de engenharia")
    print(f"")
    print(f"  Com Neutral Selection Layer:")
    print(f"    - Unidades convertidas: 0 (contexto ja esta em formato agnostico)")
    print(f"    - VendorAdapters alterados: 0 (Claude-5 usa Anthropic adapter)")
    print(f"    - Codigo alterado: 1 linha (migrate_agent_model)")
    print(f"    - Custo total: < 1 hora de engenharia")

    print(f"\nCONCLUSÃO:")
    print(f"  A Neutral Selection Layer transformou uma migracao de 16 semanas")
    print(f"  em uma operacao O(1). O contexto — o ativo mais duravel da")
    print(f"  organizacao — sobreviveu a migracao de modelo sem nenhuma")
    print(f"  alteracao. O vendor adapter absorveu toda a complexidade de")
    print(f"  formato, e o formato agnostico garantiu portabilidade.")
```

---

## Entregaveis

- Implementacao de `AgnosticContextUnit` como formato canonico de contexto.
- Tres `VendorAdapter`s (GPT-5, Claude, Gemini) com traducao bidirecional.
- `MultiTenantRegistry` com isolamento de tenant e audit trail.
- `ContextRouter` com ingestao, query cross-model e migracao O(1).
- Simulacao de migracao GPT-5 → Claude-5 demonstrando zero migracao de dados.

## Validacao: Criterios de Aceitacao

Seu codigo sera considerado **APROVADO** quando:

### Criterio 1: Diagnostico (Parte 1)

- [ ] Voce identificou quantas unidades seriam afetadas pela migracao sem Neutral Layer
- [ ] Voce identificou o impacto do vendor lock-in no specialist-agent
- [ ] Voce descreveu o esforco de migracao com Neutral Layer (O(1) vs. O(N))
- [ ] Voce explicou por que isolamento de tenant e critico em dados medicos

### Criterio 2: Vendor Adapters

- [ ] Cada adapter implementa `VendorAdapter` com `to_agnostic()` e `to_native()`
- [ ] GPT-5 adapter traduz corretamente entre formatos
- [ ] Claude adapter traduz corretamente entre formatos
- [ ] Gemini adapter traduz corretamente entre formatos
- [ ] `to_agnostic(to_native(unit)) == unit` (round-trip property)

### Criterio 3: Multi-Tenant Registry

- [ ] `write()` armazena e indexa por tenant
- [ ] `read()` verifica tenant e rejeita acesso cross-tenant
- [ ] `query_by_session()` filtra por tenant
- [ ] `query_by_agent()` filtra por tenant
- [ ] `get_audit_trail()` registra todas as operacoes

### Criterio 4: Context Router

- [ ] `ingest_context()` traduz nativo → agnostico e armazena
- [ ] `query_context()` busca e traduz agnostico → nativo do consulente
- [ ] `migrate_agent_model()` atualiza modelo sem migrar dados
- [ ] Cross-model query funciona (agente Claude le contexto gerado por agente GPT-5)

### Criterio 5: Isolamento de Tenant

- [ ] Agente em "medassist-staging" nao acessa contexto de "medassist-producao"
- [ ] Agente em "medassist-producao" nao acessa contexto de "medassist-staging"
- [ ] `tenant_stats()` reporta distribuicao correta

### Criterio 6: Migracao

- [ ] Migracao GPT-5 → Claude-5 preserva todo contexto existente
- [ ] Numero de unidades acessiveis antes e depois da migracao e identico
- [ ] Nenhuma unidade de contexto foi alterada durante a migracao

---

## Rubrica de Avaliacao

| Criterio | Peso | Insuficiente (0-3) | Basico (4-6) | Proficiente (7-8) | Excelente (9-10) |
|---|---|---|---|---|---|
| **Diagnostico (Parte 1)** | 15% | Nao identificou o vendor lock-in | Identificou parcialmente sem quantificar | Diagnostico completo com contagens e cenarios | Diagnostico + analise de outros riscos de vendor lock-in |
| **Adapters + Registry (Parte 2)** | 40% | Funcoes core nao implementadas | Implementa 1-2 adapters com erros de traducao | 3 adapters funcionais + registry com isolamento | Adapters + registry + round-trip + audit trail completos |
| **Simulacao (Parte 3)** | 30% | Nao executou a simulacao | Simulacao parcial sem migracao | Migracao completa com contraste antes/depois | Migracao + analise de custo de engenharia + recomendacao de rollout |
| **Testes e verificacao** | 15% | Nenhum cenario passa | 3 criterios passam | 5 criterios passam | Todos os 6 criterios passam |

**Nota final:** Media ponderada. **Aprovacao:** >= 7.0

---

## Dicas para Implementacao

### Para os Vendor Adapters

1. **Cada adapter e um boundary object.** Ele encapsula todo o conhecimento sobre o formato proprietario de um vendor. Quando um vendor muda sua API, apenas um adapter precisa ser atualizado — o resto do sistema nao sabe e nao precisa saber.

2. **O formato nativo e um dicionario, nao um schema rigido.** Em producao, o formato nativo de cada vendor muda com versoes de API. O adapter deve ser tolerante a campos extras e campos ausentes. Use `.get()` com defaults, nao acesso direto a chaves.

3. **A propriedade de round-trip e o teste de sanidade.** Se `to_agnostic(to_native(unit)) != unit`, ha perda de informacao na traducao. Isso e um bug critico — significa que contexto esta sendo corrompido silenciosamente. Priorize passar no round-trip test antes de qualquer outro.

### Para o Multi-Tenant Registry

1. **Isolamento de tenant e seguranca, nao organizacao.** Em um sistema medico, misturar contexto de staging com producao pode expor dados de pacientes a ambientes de teste. O isolamento e uma propriedade de seguranca, nao uma conveniencia.

2. **Audit trail e compliance.** Toda leitura e registrada — nao apenas escritas. Em sistemas medicos, saber quem leu qual contexto e tao importante quanto saber quem escreveu. O audit trail e a base para auditorias de HIPAA e GDPR.

3. **Nao presuma que tenant == string simples.** Em producao, tenants podem ser hierarquicos (`org/medassist/producao`). O sistema atual usa strings planas, mas a arquitetura suporta extensao para tenants hierarquicos.

### Para o Context Router

1. **O router e stateless em relacao ao contexto.** Ele nao armazena contexto — apenas roteia. O registry e o source of truth. Isso significa que o router pode ser escalado horizontalmente sem preocupacao com consistencia.

2. **Cross-model query e o caso de uso principal.** O valor da Neutral Selection Layer nao e armazenar contexto em formato agnostico — e permitir que agentes com modelos diferentes compartilhem contexto. Sem isso, cada agente vive em um silo.

3. **Migracao de modelo e uma operacao de configuracao, nao de dados.** `migrate_agent_model` so atualiza o `current_model` no registro. E uma operacao O(1) porque o contexto nunca foi armazenado em formato proprietario. Este e o payoff arquitetonico.

---

## Duvidas Comuns

**P: Isso nao adiciona latencia? Toda query precisa de traducao.**
R: Adiciona, mas e uma latencia de O(1) por unidade (um dict mapping). Comparado com a latencia de inferencia do modelo (segundos), e negligenciavel. O custo e pago uma vez na ingestao (nativo → agnostico) e uma vez na query (agnostico → nativo). O beneficio — independencia de vendor — justifica o custo.

**P: E se o formato agnostico nao capturar toda a informacao do formato nativo?**
R: O formato agnostico deve ser um superconjunto semantico dos formatos nativos. Se um vendor adiciona um campo que nao tem equivalente no formato agnostico, esse campo vai no `metadata` como extensao. O adapter e responsavel por preservar o que e semanticamente importante e colocar o resto em metadata.

**P: Como isso se relaciona com LLM as Fuzzy Compiler?**
R: O LLM as Fuzzy Compiler diz que codigo gerado e descartavel e constraints sao duraveis. A Neutral Selection Layer aplica o mesmo principio ao contexto: formato de armazenamento e duravel (agnostico), formato de consumo e descartavel (nativo, gerado pelo adapter). O contexto sobrevive a migracoes de "compilador" (modelo) porque o formato de armazenamento e independente.

**P: Quantos adapters preciso manter?**
R: Um por vendor, nao um por modelo. O Anthropic adapter serve Claude-4, Claude-5, Claude-Opus. Se o vendor mudar radicalmente o formato (ex: Anthropic lancar "Claude Context API v2"), voce escreve um novo adapter ou estende o existente. O ponto e que isso e trabalho de 1-2 dias, nao 16 semanas.

---

## Proximo Passo

Depois de completar este exercicio:
1. Leia `[[docs/canonical/llm-as-fuzzy-compiler|LLM as Fuzzy Compiler]]` e observe o paralelo: formato agnostico = codigo preservado, formato nativo = codigo gerado descartavel.
2. Leia `[[docs/canonical/hybrid-context-stack|Hybrid Context Stack]]` — a stack hibrida de contexto define camadas de montagem; a Neutral Selection Layer garante que essas camadas sejam preenchidas com contexto portavel.
3. (Opcional) Estenda o sistema com `ModelCapabilityDetector`: um modulo que consulta as capacidades de cada modelo (tamanho de janela, suporte a structured output) e ajusta a traducao do adapter para maximizar a qualidade do contexto entregue.

---

*Exercicio Neutral Selection Layer | Nivel 3 - Arquitetura Avancada*

**Contexto e o ativo mais duravel de uma organizacao agentica. Nao o solde ao roadmap de um vendor.**
