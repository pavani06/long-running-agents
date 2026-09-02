---
title: "Exercício 18: Typed Tool and Event Boundaries — Barrar o Inválido na Fronteira, Antes do Efeito"
type: exercise
level: 3
aliases: ["typed tool and event boundaries", "fronteiras tipadas de tools e eventos", "kernel validator de fronteiras", "per-agent event schema", "contrato de eventos por agente", "bad actions impossible not improbable"]
tags: ["curriculo-conteudo", "nivel-3", "agentes-orquestracao", "12-factor-agents", "harness-engineering", "error-handling", "production", "arquitetura", "verification", "context-engineering"]
relates-to: ["[[docs/analysis/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt-patterns|Padrões Agent Frameworks Considered Harmful]]", "[[docs/analysis/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt-classification|Classificação Agent Frameworks Considered Harmful]]", "[[docs/canonical/structured-generation-constraint-validation-circuit|Structured Generation Constraint Validation Circuit]]", "[[docs/canonical/deterministic-tool-dispatch|Deterministic Tool Dispatch]]", "[[docs/canonical/agent-to-agent-review-comment-protocol|Agent-to-Agent Review Comment Protocol]]", "[[docs/canonical/centralized-cross-framework-tracing|Centralized Cross-Framework Tracing]]", "[[curriculum/03-nivel-3-advanced-architecture/exercises/exercise-17-self-iterating-agent-loop|Exercício 17: Self-Iterating Agent Loop]]", "[[curriculum/03-nivel-3-advanced-architecture/exercises/exercise-20-causal-event-log|Exercício 20: Append-Only Causal Event Log]]", "[[curriculum/03-nivel-3-advanced-architecture/exercises/exercise-21-agent-kernel-runtime|Exercício 21: Agent Kernel Runtime]]"]
duration: "90-120 min"
last_updated: 2026-09-02
---

# 🧱 Exercício 18: Typed Tool and Event Boundaries — Barrar o Inválido na Fronteira, Antes do Efeito
## Nível 3 — Arquitetura Avançada

**Tempo Estimado:** 90-120 minutos
**Dificuldade:** (Avançado)
**Pré-requisito:** Ter lido `01-multi-agent-systems.md` (Nível 3) + `docs/canonical/structured-generation-constraint-validation-circuit.md` + `docs/canonical/deterministic-tool-dispatch.md`
**Objetivo:** Fechar as DUAS fronteiras do sistema — agente→ferramenta e agente→agente — com contratos tipados declarados por agente e um validador único no kernel que rejeita tool call e evento não-conformes ANTES de produzirem efeito, tornando ações ruins impossíveis em vez de improváveis

---

## 📖 Prólogo: A Fleet Que Perdia Um Quinto dos Eventos Depois de Publicá-los

### Incidente de sexta-feira. O agente summarizer morreu de novo.

```
ONCALL:      "summarizer caiu de novo. Mesmo sintoma: recebeu um evento
              recommendation.drafted com payload sem o campo catalog_id
              e explodiu no KeyError. Essa é a 4ª vez essa semana."

ENG:         "eu sei. O recommender às vezes emite o schema certo, às
              vezes não — o modelo que ele usa é fraco em structured
              output. A gente valida o output DO MODELO com Zod, mas o
              evento que o agente publica pro próximo agente? Ninguém
              valida. Passa direto."

ONCALL:      "e qual foi a taxa de perda essa semana?"

ENG:         "contando os dois pipelines: ~20% dos eventos publicados
              são rejeitados DOWNSTREAM — quer dizer, depois de já terem
              side effects parciais. O trabalho do recommender se perde,
              o summarizer trava, e a gente descobre pelo crash e não
              pelo contrato."

ONCALL:      "espera. Vocês têm schema validado na fronteira modelo→agente
              e tool tipada na fronteira agente→tool. Como a fronteira
              agente→agente é terra sem lei?"

ENG:         "porque cada fronteira foi resolvida num trimestre
              diferente, por times diferentes, e ninguém desenhou o
              sistema de fronteiras — a gente foi remendando. O validador
              do output do modelo não sabe que eventos existem; o
              dispatcher de tools não sabe que eventos existem; e o
              barramento de eventos confia que 'todo mundo envia o
              payload certo'. Confiança não é contrato."
```

**O custo das fronteiras pela metade:**

```
╔══════════════════════════════════════════════════════════════════╗
║   TRÊS FRONTEIRAS, UM VALIDADOR — O SISTEMA PELA METADE            ║
║                                                                  ║
║  Fronteira            Estado no repo        Quem barra            ║
║  ───────────────────  ────────────────────  ─────────────────────  ║
║  modelo → agente      coberta (canônico)    constraint circuit    ║
║  agente → tool        coberta (canônico)    Zod + dispatch        ║
║  agente → agente      SEM COBERTURA         ninguém (confiança)   ║
║                                                                  ║
║  Sintoma observado no fonte original: com modelos fracos em      ║
║  structured outputs, ~20% dos eventos eram rejeitados DEPOIS de  ║
║  publicados (patterns.md:20) — o repo do curso tem o mesmo buraco ║
║  na fronteira agente→agente (classification.md:34, NOT_FOUND de   ║
║  schemas de evento por agente e validador nas duas fronteiras)    ║
║                                                                  ║
║  O reframe do padrão: "make bad actions impossible, not just      ║
║  improbable" — a validação é do KERNEL, aplicada em TODA          ║
║  fronteira, ANTES do efeito (patterns.md:30)                      ║
╚══════════════════════════════════════════════════════════════════╝
```

**O problema não é o modelo fraco.** Modelo ruim em structured output vai gerar carga
inválida — isso é dado (`...patterns.md:36`: "a fronteira rejeita, não corrige"). O
problema é **onde** a carga inválida é barrada: hoje ela atravessa o runtime, é
publicada, produz efeito parcial, e mata o agente seguinte. O padrão do fonte move a
rejeição para **antes da publicação**: cada agente declara um contrato (quais eventos
aceita, quais emite, quais tools usa), e um validador no kernel — o mesmo para as duas
fronteiras — rejeita o que não conforma no momento da travessia. O que o repo já tem
de maturidade (o circuito de constraint validation na saída do modelo, o dispatch
determinístico com Zod na entrada de tools) é exatamente a metade que falta
generalizar para eventos (`...classification.md:26`).

**Sua missão:** implementar o `TypedBoundaryKernel` — contratos por agente
(`AgentContract` com schemas de eventos aceitos/emitidos e de tools usadas), o
registro central (`ContractRegistry`), o validador único aplicado na fronteira de
tools E na de eventos (`validate_tool_call` / `validate_event`), o log de efeitos que
só registra o que passou, e a simulação comparativa: o mesmo lote de emissões do
modelo fraco, com e sem fronteiras — sem, ~20% se perde depois de publicado; com,
zero publicado inválido (rejeitado na fronteira, com razão auditável).

---

## 🧠 O Contexto

### O Modelo Mental: Contrato por Agente, Validador no Kernel, Efeito Só Depois

O padrão é declaradamente uma postura "non-negotiable" do kernel
(`...patterns.md:30`): a fronteira **rejeita**, não tenta consertar. Três
propriedades a definem:

1. **O contrato é do agente, não da mensagem.** Cada agente declara o que aceita e o
   que retorna — na fronteira tool (quais tools, com quais argumentos) e na fronteira
   evento (quais tipos emite, com qual payload). Isso substitui convenções implícitas
   de payload por contratos tipados consultáveis (`...patterns.md:32`):

```
        MODELO FRACO (structured output ruim — dado, não bug)
              │
              ▼
   ┌─────────────────────────────────────────────────┐
   │  FRONTeira agente→tool                          │
   │  kernel valida: tool existe no contrato?        │
   │  args conformam o schema da tool?               │
   └───────────────┬─────────────────┬───────────────┘
                   │ passou          │ rejeitou
                   ▼                 ▼
              EFEITO EXECUTADO   BoundaryRejection
                   │            (ANTES do efeito)
                   ▼
   ┌─────────────────────────────────────────────────┐
   │  FRONTeira agente→agente                        │
   │  kernel valida: evento declarado como emitido?  │
   │  payload conforma o schema do tipo?             │
   └───────────────┬─────────────────┬───────────────┘
                   │ passou          │ rejeitou
                   ▼                 ▼
            EVENTO PUBLICADO   BoundaryRejection
            (o consumidor       (nada publicado —
             pode confiar)      trabalho NÃO se perde:
                                a razão volta pro emissor)
```

2. **Um validador, duas fronteiras.** O valor não está em ter validação em algum
   lugar — o repo já tem, na saída do modelo e na entrada de tools. O valor está no
   validador ser **do kernel e aplicado em ambas as fronteiras** com a mesma postura:
   barrar antes do efeito (`...classification.md:26`). É isso que o repo não tem: a
   busca por "typed event" e "eventos tipados" no repo retorna apenas validação de
   output de modelo e input de tool (`...classification.md:34`).

3. **Rejeitar não é corrigir.** A fronteira rejeita; o modelo ruim continua gerando
   carga rejeitada (`...patterns.md:36`). Quem decide o que fazer com a rejeição
   (retry com mensagem de erro, reparo, desistir) é a política do emissor — a
   fronteira só garante que nada inválido atravessa.

Os vizinhos do repo, e por que não fecham sozinhos: o
`structured-generation-constraint-validation-circuit` valida a saída do MODELO e
rejeita/repara no post-generation (`...md:61-63`) — não toca eventos entre agentes; o
`deterministic-tool-dispatch` tipa a entrada de TOOLS com Zod (`...md:74`) — não toca
eventos; o `agent-to-agent-review-comment-protocol` cria um formato agent-parseable
para UM domínio (comentários de review, `...md:37`) — é o analogo mais próximo, mas
escopado, não um contrato geral de eventos. O padrão os generaliza.

### O Que Você Vai Construir

1. `EventSchema` / `ToolSchema` — o contrato de um tipo de evento (campos exigidos e
   tipos) e de uma tool (nome, campos e tipos dos argumentos)
2. `AgentContract` — a declaração por agente: eventos aceitos, eventos emitidos,
   tools usadas (tudo congelado, tudo consultável)
3. `ContractRegistry` — o registro central: registra contratos, recusa duplicatas,
   responde "qual o contrato do agente X"
4. `TypedBoundaryKernel` — o validador único: `validate_tool_call()` na fronteira
   agente→tool e `validate_event()` na fronteira agente→agente; toda rejeição carrega
   `RejectionReason` e detalhe auditável
5. `EffectLog` — registra APENAS o que atravessou (tool executada, evento publicado);
   a prova de que nada inválido produziu efeito
6. `run_shift()` — a simulação comparativa: 10 emissões do modelo fraco (2 inválidas —
   os 20% do fonte), sem fronteiras (2 eventos publicados inválidos, 2 consumers
   mortos) e com fronteiras (0 publicados inválidos, 2 rejeitados com razão)

---

## 📋 Cenário

O pipeline de recomendação do KODA após a fundação (Exercício 15): o `recommender`
gera rascunhos, o `summarizer` condensa para o WhatsApp, o `poster` publica. O
`recommender` roda num modelo barato, fraco em structured output. Numa janela de
manhã ele emite 10 ações: 8 conformes, 1 evento `recommendation.drafted` sem o campo
exigido `catalog_id`, e 1 tool call `search_catalog` com `query` como `int` em vez de
`str`. Sem fronteiras, os dois inválidos atravessam: o evento mata o `summarizer`
(KeyError downstream), a tool executa com payload torto e retorna lixo. Com
fronteiras, os dois são rejeitados na travessia — com razão — e nada inválido publica
ou executa.

---

## ✅ Requisitos

### Requisitos Funcionais

1. **RF1 — Contrato por agente:** cada `AgentContract` declara eventos aceitos,
   eventos emitidos e tools com schemas; o `ContractRegistry` recusa agente
   duplicado (`DuplicateContractError`) e agente sem contrato não atravessa fronteira
   nenhuma (`UnknownAgentError`).
2. **RF2 — Fronteira agente→tool:** `validate_tool_call()` rejeita tool fora do
   contrato do agente (`UNKNOWN_TOOL`), campo exigido ausente (`MISSING_FIELD`) e
   tipo errado (`WRONG_TYPE`); tool conforme retorna o `ToolCall` validado para
   execução.
3. **RF3 — Fronteira agente→agente:** `validate_event()` rejeita tipo que o agente
   NÃO declarou como emitido (`UNDECLARED_EMISSION`), tipo inexistente no registro
   (`UNKNOWN_EVENT_TYPE`), campo ausente (`MISSING_FIELD`) e tipo errado
   (`WRONG_TYPE`); evento conforme retorna o `Event` validado para publicação.
4. **RF4 — Efeito só depois da validação:** `EffectLog` só registra tools executadas
   e eventos publicados que passaram pelo kernel; Nenhuma rejeição aparece como
   efeito — a invariante do "antes do efeito".
5. **RF5 — Rejeição auditável:** toda `BoundaryRejection` carrega a fronteira, o
   `RejectionReason` e o detalhe (qual campo, qual tipo esperado); a fronteira
   rejeita, não corrige — nenhum path de validação altera o payload.
6. **RF6 — Simulação comparativa:** sem fronteiras, o lote de 10 emissões publica 2
   inválidos (perda de 20% downstream: `events_lost == 2`); com fronteiras,
   `events_lost == 0`, `rejections == 2` e `published == 8` — a perda observada no
   fonte original é eliminada na travessia.

### Requisitos Técnicos

1. **RT1 — Python 3.9+, stdlib apenas**, type hints obrigatórios
2. **RT2 — `dataclasses` + enums**, tudo congelado onde faz sentido (contratos são
   imutáveis); simulação determinística (sem aleatoriedade)
3. **RT3 — Kernel como funções puras** de (contrato, ação) → (validado | rejeição);
   I/O nenhum
4. **RT4 — Toda rejeição rastreável:** reason + detalhe suficientes para o emissor
   reagir sem inspectar o código do kernel

---

## 🏗️ Arquitetura do Sistema

```
┌────────────────────────────────────────────────────────────────────────┐
│                     TYPED BOUNDARY KERNEL                               │
│                                                                        │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │ CONTRACT REGISTRY (RF1)                                        │    │
│  │ AgentContract: recommender | summarizer | poster               │    │
│  │   .emits  → quais tipos de evento declara emitir               │    │
│  │   .accepts→ quais tipos de evento declara consumir             │    │
│  │   .tools  → quais tools, com schema de argumentos              │    │
│  └──────────────────────────┬─────────────────────────────────────┘    │
│                             ▼                                          │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │ FRONTIERA agente→tool (RF2)          FRONTIERA agente→agente    │    │
│  │ validate_tool_call()                  validate_event() (RF3)    │    │
│  │ UNKNOWN_TOOL / MISSING_FIELD /        UNDECLARED_EMISSION /     │    │
│  │ WRONG_TYPE                            UNKNOWN_EVENT_TYPE /      │    │
│  │        │                              MISSING_FIELD / WRONG_TYPE│    │
│  │        ▼                                      ▼                 │    │
│  │ ToolCall validado ──► EffectLog      Event validado ──► EffectLog│   │
│  │ (executa)            (RF4)           (publica)        (RF4)     │    │
│  └──────────────────────────┬─────────────────────────────────────┘    │
│                             ▼                                          │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │ SIMULAÇÃO COMPARATIVA (RF6)                                    │    │
│  │ lote: 10 emissões do modelo fraco (2 inválidas = os 20%)       │    │
│  │ sem fronteiras: published=10, invalid_published=2, lost=2      │    │
│  │ com fronteiras: published=8, rejections=2, lost=0              │    │
│  └────────────────────────────────────────────────────────────────┘    │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 🎯 Sua Tarefa em 3 Partes

### Parte 1 — Diagnosticar as fronteiras do incidente (15 min)

Com o prólogo: para cada uma das 3 fronteiras (modelo→agente, agente→tool,
agente→agente), diga qual mecanismo do repo a cobre hoje (cite o canonical) e onde a
carga inválida do incidente atravessou. Depois responda: por que "validar no
consumidor" (try/except no summarizer) NÃO é o padrão? Responda como comentário.

### Parte 2 — Contratos e o validador único (40 min)

Implemente `EventSchema`/`ToolSchema`, `AgentContract`, `ContractRegistry` (RF1) e o
`TypedBoundaryKernel` com as duas fronteiras (RF2-RF3), com `EffectLog` provando a
invariante do efeito (RF4-RF5).

### Parte 3 — Simulação comparativa (35 min)

Implemente `run_shift()` (RF6): o mesmo lote de 10 emissões nas duas configurações.
Verifique: sem fronteiras, 2 inválidos publicados e `events_lost == 2`; com
fronteiras, 0 perdidos, 2 rejeitados com razão auditável.

---

## 💻 Starter Code

```python
"""
Exercício 18 — Typed Tool and Event Boundaries
Nível 3 — Arquitetura Avançada

Contratos declarados por agente + validador único no kernel aplicado às
duas fronteiras (agente→tool e agente→agente). A fronteira rejeita antes
do efeito: ação ruim fica impossível, não só improvável.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Mapping, Union


# ============================================================================
# DATA MODELS — o contrato
# ============================================================================

FieldType = type          # int | str | float | bool (tipos simples)


@dataclass(frozen=True)
class EventSchema:
    """O contrato de um tipo de evento na fronteira agente→agente."""
    event_type: str                      # ex.: "recommendation.drafted"
    fields: Mapping[str, FieldType]      # nome → tipo exigido


@dataclass(frozen=True)
class ToolSchema:
    """O contrato de uma tool na fronteira agente→tool."""
    tool_name: str                       # ex.: "search_catalog"
    fields: Mapping[str, FieldType]      # argumentos exigidos


@dataclass(frozen=True)
class AgentContract:
    """A declaração do agente: o que emite, o que aceita, o que usa (RF1).

    Substitui convenção implícita de payload por contrato consultável
    (patterns.md:32) — o análogo inter-agentes do DynamicStructuredTool
    com Zod do deterministic-tool-dispatch.md:74.
    """
    agent_id: str
    emits: tuple[EventSchema, ...]
    accepts: tuple[EventSchema, ...]
    tools: tuple[ToolSchema, ...]

    def emitted_type(self, event_type: str) -> EventSchema | None:
        """O schema do tipo que ESTE agente declarou emitir, ou None."""
        # TODO: implemente
        raise NotImplementedError

    def tool(self, tool_name: str) -> ToolSchema | None:
        """O schema da tool que ESTE agente declarou usar, ou None."""
        # TODO: implemente
        raise NotImplementedError


class DuplicateContractError(Exception):
    pass


class UnknownAgentError(Exception):
    pass


class ContractRegistry:
    """Registro central dos contratos — a fonte do kernel (RF1)."""

    def __init__(self) -> None:
        self._contracts: dict[str, AgentContract] = {}

    def register(self, contract: AgentContract) -> None:
        """Recusa agente duplicado (DuplicateContractError)."""
        # TODO: implemente
        raise NotImplementedError

    def contract_for(self, agent_id: str) -> AgentContract:
        """Agente sem contrato não atravessa fronteira (UnknownAgentError)."""
        # TODO: implemente
        raise NotImplementedError


# ============================================================================
# O KERNEL — validador único, duas fronteiras
# ============================================================================

class Frontier(Enum):
    TOOL = "tool"          # agente → ferramenta
    EVENT = "event"        # agente → agente


class RejectionReason(Enum):
    UNKNOWN_TOOL = "unknown_tool"
    UNDECLARED_EMISSION = "undeclared_emission"
    UNKNOWN_EVENT_TYPE = "unknown_event_type"
    MISSING_FIELD = "missing_field"
    WRONG_TYPE = "wrong_type"


@dataclass(frozen=True)
class BoundaryRejection:
    """A rejeição auditável (RF5): fronteira + razão + detalhe.

    A fronteira rejeita, não corrige (patterns.md:36): nenhum campo
    desta estrutura sugere mutação do payload original.
    """
    frontier: Frontier
    reason: RejectionReason
    detail: str


@dataclass(frozen=True)
class ToolCall:
    """Tool call validada — pronta para execução (efeito)."""
    agent_id: str
    tool_name: str
    args: Mapping[str, object]


@dataclass(frozen=True)
class Event:
    """Evento validado — pronto para publicação (efeito)."""
    event_type: str
    publisher: str
    payload: Mapping[str, object]


Validation = Union[ToolCall, Event, BoundaryRejection]


class TypedBoundaryKernel:
    """O validador único aplicado às DUAS fronteiras (RF2, RF3)."""

    def __init__(self, registry: ContractRegistry) -> None:
        self._registry = registry

    def validate_tool_call(
        self, agent_id: str, tool_name: str, args: Mapping[str, object]
    ) -> ToolCall | BoundaryRejection:
        """
        Recusa: UNKNOWN_TOOL (tool fora do contrato), MISSING_FIELD,
        WRONG_TYPE. Conforme → ToolCall validada (RF2).
        """
        # TODO: implemente (dica: um helper privado de validação de
        # campos contra Mapping[str, FieldType] serve às duas fronteiras)
        raise NotImplementedError

    def validate_event(
        self, agent_id: str, event_type: str, payload: Mapping[str, object]
    ) -> Event | BoundaryRejection:
        """
        Recusa: UNDECLARED_EMISSION (agente não declarou emitir o tipo),
        UNKNOWN_EVENT_TYPE (tipo sem schema no contrato), MISSING_FIELD,
        WRONG_TYPE. Conforme → Event validado (RF3).
        """
        # TODO: implemente
        raise NotImplementedError


@dataclass
class EffectLog:
    """Registra APENAS o que atravessou (RF4) — a prova do antes-do-efeito."""
    executed_tools: list[ToolCall] = field(default_factory=list)
    published_events: list[Event] = field(default_factory=list)

    @property
    def total_effects(self) -> int:
        # TODO: implemente
        raise NotImplementedError


# ============================================================================
# PARTE 3 — SIMULAÇÃO COMPARATIVA
# ============================================================================

class EmissionKind(Enum):
    TOOL_CALL = "tool_call"
    EVENT = "event"


@dataclass(frozen=True)
class Emission:
    """Uma ação bruta do modelo fraco, ANTES de qualquer validação."""
    kind: EmissionKind
    agent_id: str
    name: str                       # tool_name ou event_type
    data: Mapping[str, object]      # args ou payload


@dataclass
class ShiftResult:
    label: str
    published: int = 0              # eventos que atravessaram (ou passaram reto)
    executed: int = 0               # tools que atravessaram (ou passaram reto)
    invalid_published: int = 0      # inválidos que PUBLICARAM (sem fronteiras)
    events_lost: int = 0            # consumers mortos downstream
    rejections: list[BoundaryRejection] = field(default_factory=list)
    effects: EffectLog = field(default_factory=EffectLog)


def run_shift(
    registry: ContractRegistry, emissions: list[Emission], boundaries: bool
) -> ShiftResult:
    """
    boundaries=False: tudo atravessa sem validação; emissões inválidas
      contam em invalid_published e cada uma mata um consumer
      (events_lost += 1 por evento inválido publicado; tool inválida
      executa e conta em executed, mas não mata consumer).
    boundaries=True: TypedBoundaryKernel decide; inválido NÃO publica
      nem executa — vira BoundaryRejection auditável (RF6).
    O lote do fixture tem 10 emissões, 2 inválidas (~20% do fonte,
    patterns.md:20).
    """
    # TODO: implemente
    raise NotImplementedError


# ============================================================================
# FIXTURES — o pipeline de recomendação do KODA
# ============================================================================

def build_registry() -> ContractRegistry:
    drafted = EventSchema("recommendation.drafted", {"catalog_id": str, "score": float})
    condensed = EventSchema("recommendation.condensed", {"summary": str})
    posted = EventSchema("recommendation.posted", {"message_id": str})
    search = ToolSchema("search_catalog", {"query": str})

    registry = ContractRegistry()
    registry.register(AgentContract(
        agent_id="recommender",
        emits=(drafted,),
        accepts=(),
        tools=(search,),
    ))
    registry.register(AgentContract(
        agent_id="summarizer",
        emits=(condensed,),
        accepts=(drafted,),
        tools=(),
    ))
    registry.register(AgentContract(
        agent_id="poster",
        emits=(posted,),
        accepts=(condensed,),
        tools=(),
    ))
    return registry


def build_morning_batch() -> list[Emission]:
    """10 emissões do modelo fraco: 8 conformes, 2 inválidas (os ~20%)."""
    batch: list[Emission] = []
    for i in range(6):  # 6 eventos conformes
        batch.append(Emission(
            EmissionKind.EVENT, "recommender", "recommendation.drafted",
            {"catalog_id": f"sku-{i:03d}", "score": 0.7 + i * 0.02},
        ))
    # 2 tool calls conformes
    batch.append(Emission(
        EmissionKind.TOOL_CALL, "recommender", "search_catalog",
        {"query": "fone bluetooth"},
    ))
    batch.append(Emission(
        EmissionKind.TOOL_CALL, "recommender", "search_catalog",
        {"query": "carregador usb-c"},
    ))
    # inválida 1: evento SEM catalog_id (mata o summarizer downstream)
    batch.append(Emission(
        EmissionKind.EVENT, "recommender", "recommendation.drafted",
        {"score": 0.91},
    ))
    # inválida 2: tool com query como int (payload torto)
    batch.append(Emission(
        EmissionKind.TOOL_CALL, "recommender", "search_catalog",
        {"query": 404},
    ))
    return batch


# ============================================================================
# TESTS
# ============================================================================

def test_registry_contracts():
    reg = build_registry()
    contract = reg.contract_for("recommender")
    assert contract.emitted_type("recommendation.drafted") is not None
    assert contract.emitted_type("recommendation.posted") is None
    try:
        reg.register(contract)
        raise AssertionError("duplicata deve ser recusada (RF1)")
    except DuplicateContractError:
        pass
    try:
        reg.contract_for("ghost-agent")
        raise AssertionError("agente sem contrato deve explodir (RF1)")
    except UnknownAgentError:
        pass
    print("TESTE 1 PASSOU")


def test_tool_frontier():
    kernel = TypedBoundaryKernel(build_registry())
    ok = kernel.validate_tool_call(
        "recommender", "search_catalog", {"query": "fone"}
    )
    assert isinstance(ok, ToolCall), "tool conforme deve passar (RF2)"
    missing = kernel.validate_tool_call("recommender", "search_catalog", {})
    assert isinstance(missing, BoundaryRejection)
    assert missing.reason == RejectionReason.MISSING_FIELD
    wrong = kernel.validate_tool_call(
        "recommender", "search_catalog", {"query": 404}
    )
    assert isinstance(wrong, BoundaryRejection)
    assert wrong.reason == RejectionReason.WRONG_TYPE
    unknown = kernel.validate_tool_call(
        "summarizer", "search_catalog", {"query": "x"}
    )
    assert isinstance(unknown, BoundaryRejection)
    assert unknown.reason == RejectionReason.UNKNOWN_TOOL
    print("TESTE 2 PASSOU")


def test_event_frontier():
    kernel = TypedBoundaryKernel(build_registry())
    ok = kernel.validate_event(
        "recommender", "recommendation.drafted",
        {"catalog_id": "sku-001", "score": 0.8},
    )
    assert isinstance(ok, Event), "evento conforme deve passar (RF3)"
    undeclared = kernel.validate_event(
        "recommender", "recommendation.posted", {"message_id": "m-1"}
    )
    assert isinstance(undeclared, BoundaryRejection)
    assert undeclared.reason == RejectionReason.UNDECLARED_EMISSION
    missing = kernel.validate_event(
        "recommender", "recommendation.drafted", {"score": 0.9}
    )
    assert isinstance(missing, BoundaryRejection)
    assert missing.reason == RejectionReason.MISSING_FIELD
    wrong = kernel.validate_event(
        "recommender", "recommendation.drafted",
        {"catalog_id": 7, "score": 0.9},
    )
    assert isinstance(wrong, BoundaryRejection)
    assert wrong.reason == RejectionReason.WRONG_TYPE
    print("TESTE 3 PASSOU")


def test_simulation_closes_the_hole():
    reg = build_registry()
    batch = build_morning_batch()

    open_ = run_shift(reg, batch, boundaries=False)
    assert open_.invalid_published == 1, "o evento sem campo publica e mata consumer"
    assert open_.events_lost == 1
    assert open_.published == 7 and open_.executed == 3, "sem fronteiras, tudo passa"
    assert open_.rejections == []

    closed = run_shift(reg, batch, boundaries=True)
    assert closed.events_lost == 0, "com fronteiras, nada inválido publica (RF6)"
    assert closed.invalid_published == 0
    assert closed.published == 6 and closed.executed == 2
    assert len(closed.rejections) == 2, "as 2 inválidas rejeitadas com razão (RF5)"
    reasons = {r.reason for r in closed.rejections}
    assert reasons == {RejectionReason.MISSING_FIELD, RejectionReason.WRONG_TYPE}
    assert closed.effects.total_effects == 8, "EffectLog só registra o que passou (RF4)"
    print("TESTE 4 PASSOU")


if __name__ == "__main__":
    print("=" * 60)
    print("EXERCÍCIO 18: TYPED TOOL AND EVENT BOUNDARIES")
    print("=" * 60)
    # Descomente após implementar:
    # test_registry_contracts()
    # test_tool_frontier()
    # test_event_frontier()
    # test_simulation_closes_the_hole()
    print("\nTODO: implemente contracts, registry, kernel, effect log")
    print("e run_shift")
```

---

## ✅ Validação: Critérios de Aceitação

Seu código será considerado **APROVADO** quando:

- [ ] O registry recusa duplicata (`DuplicateContractError`) e agente sem contrato (`UnknownAgentError`); contrato expõe schemas consultáveis (RF1)
- [ ] `validate_tool_call()` produz os três motivos de rejeição e retorna `ToolCall` para o conforme (RF2)
- [ ] `validate_event()` produz `UNDECLARED_EMISSION`, `UNKNOWN_EVENT_TYPE`, `MISSING_FIELD`, `WRONG_TYPE` e retorna `Event` para o conforme (RF3)
- [ ] `EffectLog` só contém o que atravessou; nenhuma rejeição vira efeito (RF4)
- [ ] Toda rejeição carrega fronteira + razão + detalhe; nenhum path altera o payload original (RF5)
- [ ] Sem fronteiras: evento inválido publica, `events_lost == 1`; com fronteiras: `events_lost == 0`, 2 rejeições, 8 efeitos (RF6)

---

## 📊 Rubric de Avaliação

| Critério | Peso | Insuficiente (0-3) | Básico (4-6) | Proficiente (7-8) | Excelente (9-10) |
|---|---|---|---|---|---|
| **Contratos + Registry (Parte 2)** | 25% | Não implementados | Contratos sem imutabilidade | Contratos congelados + duplicata/agente desconhecido recusados | Schemas consultáveis como fonte única do kernel |
| **Fronteira tool (Parte 2)** | 20% | Não implementada | Valida só presença de campo | Três razões de rejeição + retorno tipado | Helper único de validação de campos compartilhado entre fronteiras |
| **Fronteira evento (Parte 2)** | 25% | Não implementada | Valida só tipo conhecido | Emissão declarada por agente + 4 razões de rejeição | Postura rejeita-não-corrige explícita no design |
| **Simulação (Parte 3)** | 30% | Não implementada | Uma configuração só | Duas configurações divergentes com números do fixture | EffectLog como prova do antes-do-efeito e rejeições auditáveis |

**Nota final:** Média ponderada. **Aprovação:** >= 7.0

---

## 💡 Dicas para Implementação

1. **Um helper, duas fronteiras.** A validação de `Mapping[str, object]` contra `Mapping[str, FieldType]` (campo existe? tipo bate?) é idêntica para tool e evento. Escreva uma vez, use nas duas — o padrão é UM validador no kernel, não dois validadores acidentais que driftam.
2. **A ordem das checagens importa para a razão.** Na fronteira de evento, cheque primeiro se o agente declarou emitir o tipo (`UNDECLARED_EMISSION`), depois os campos. Um evento `recommendation.posted` emitido pelo recommender com payload perfeito ainda é rejeitado — o contrato é do agente, não da mensagem.
3. **Não "conserte" o payload na validação.** Se der vontade de fazer cast de `int` para `str` no `query: 404`, releia `patterns.md:36`: a fronteira rejeita, não corrige. Corrigir na fronteira esconde o modelo fraco e transfere o custo do bug para o validador.

---

## ❓ Dúvidas Comuns

**P: Se a fronteira rejeita e o modelo continua fraco, não só troquei crash por rejeição?**
R: Trocou crash DOWNSTREAM (consumer morto, trabalho publicado perdido, efeito parcial) por rejeição determinística ANTES do efeito, com razão que o emissor pode reagir (retry com o erro, reparo, desistir). A perda de ~20% vira 0% de trabalho perdido: o inválido nunca publica (`...patterns.md:31`).

**P: Isso não é o constraint validation circuit de novo?**
R: É a generalização. O circuito do canon valida a saída do MODELO com schema + constraints no post-generation (`docs/canonical/structured-generation-constraint-validation-circuit.md:61-63`); o deterministic-tool-dispatch tipa a entrada de TOOLS com Zod (`docs/canonical/deterministic-tool-dispatch.md:74`). O que nenhum cobre é a fronteira agente→agente com contrato por agente — o NOT_FOUND da classificação (`...classification.md:34`).

**P: Por que o contrato declara `accepts` se o kernel valida emissão?**
R: Porque "aceita" é o outro lado do mesmo contrato: o consumidor declara o que espera receber, e o registro pode checar compatibilidade (quem emite `X` tem alguém que aceita `X`). Neste exercício `accepts` documenta a intenção e aparece no cenário; o kernel do Exercício 21 usa esses mesmos contratos para acordar processos por evento.

**P: Onde as fronteiras ficam no runtime real?**
R: No kernel — é o que o Exercício 21 formaliza: scheduler + isolamento + journaling, com as fronteiras tipadas como a política de admissão do kernel. O log causal do Exercício 20 registra o que atravessou (o `EffectLog` daqui é a versão mínima dele).

---

## 🚀 Próximo Passo

Depois de completar este exercício:

1. Leia o padrão 1 completo e sua classificação: `docs/analysis/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt-patterns.md:17-36` e `...classification.md:22-36` — a fronteira que falta ao repo e o vocabulário que ele já possui para absorvê-la
2. Siga a série: este exercício tipa o que atravessa as fronteiras → Exercício 20 dá ao que atravessou uma memória causal única e imutável → Exercício 21 monta o kernel que agenda, isola e jorna os agentes que vivem atrás dessas fronteiras
3. Escreva o ADO do KODA: qual par emissor→consumer do pipeline atual troca payload por convenção implícita hoje, e qual seria o `EventSchema` mínimo para torná-lo contrato?

---

*Exercício 18 | Nível 3 — Arquitetura Avançada | Typed Tool and Event Boundaries*

**Ação ruim se barra na fronteira, antes do efeito — impossível, não improvável.**
