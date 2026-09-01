---
title: "Exercício 14: Unified Tool Surface Flywheel — Uma Autoridade de Tool, Todos os Consumidores, Todo Upgrade É Compartilhado"
type: exercise
level: 3
aliases: ["unified tool surface flywheel", "tool surface unification", "única autoridade de tool", "UI CLI API mesma tool", "agente consumindo a API pública", "tool failure as API signal", "flywheel de superfície única", "no agent-only backdoors"]
tags: ["curriculo-conteudo", "nivel-3", "agentes-orquestracao", "harness-engineering", "production", "tool-unification", "arquitetura", "error-handling", "harness", "stack-tooling"]
relates-to: ["[[docs/canonical/unified-tool-surface-flywheel|Unified Tool Surface Flywheel]]", "[[docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-patterns|Clay Eval Stack Patterns]]", "[[docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-classification|Clay Eval Stack Classification]]", "[[docs/canonical/file-system-materialization|File-System Materialization]]", "[[docs/canonical/deterministic-tool-dispatch|Deterministic Tool Dispatch]]", "[[docs/canonical/production-failure-regression-flywheel|Production-Failure Regression Flywheel]]", "[[docs/canonical/closed-loop-help-api|Closed-Loop Help API]]", "[[curriculum/03-nivel-3-advanced-architecture/exercises/exercise-13-production-offline-drift-taxonomy|Exercício 13: Production-to-Offline Feedback Loop with Drift Taxonomy]]", "[[curriculum/03-nivel-3-advanced-architecture/exercises/exercise-17-self-iterating-agent-loop|Exercício 17: Self-Iterating Agent Loop]]"]
duration: "90-120 min"
last_updated: 2026-08-31
---

# 🔁 Exercício 14: Unified Tool Surface Flywheel — Uma Autoridade de Tool, Todos os Consumidores, Todo Upgrade É Compartilhado
## Nível 3 — Arquitetura Avançada

**Tempo Estimado:** 90-120 minutos
**Dificuldade:** (Avançado)
**Pré-requisito:** Ter lido `03-file-based-coordination.md` (Nível 3) + `docs/canonical/deterministic-tool-dispatch.md` + Exercício 13
**Objetivo:** Consolidar UI, CLI, API pública e agentes internos sobre uma única autoridade de tool por operação — de forma que toda falha de tool do agente dobre como sinal de qualidade da API pública, e todo upgrade beneficie todos os consumidores de uma vez

---

## 📖 Prólogo: O Ticket Que Duas Equipes Já Tinham Resolvido

### Segunda-feira, 10h03. Ticket #4471, cliente da API pública do KODA.

```
SUPPORT (ticket #4471):
  "Cliente integra via REST /products/search e recebe resultados
   com produtos DESATIVADOS no catálogo. Reproduzível com
   ?category=creatina&include_out_of_stock=false."

API_TEAM: "investigando. vou subir um fix na endpoint esta semana."

── 40 minutos depois, no canal do time de agentes ─────────────────

AGENT_TEAM: "psst: a gente consertou esse bug há 12 dias.
             O recomendador interno tava filtrando direto no
             product_search.py — a query ignorava include_out_of_stock
             quando category estava presente. Fix no PR #2210."

API_TEAM: "espera. vocês têm uma SEGUNDA implementação de busca
           de produtos?"

AGENT_TEAM: "tecnicamente três: a da UI (React), a nossa lib
             interna (product_search.py) e a API pública (Go).
             ...por que? todo mundo faz assim."

API_TEAM: "porque o cliente pagante passou 12 dias com o bug que
           vocês já tinham diagnosticado nos traces do agente.
           E ninguém soube."
```

**O custo das três verdades:**

```
╔══════════════════════════════════════════════════════════════════╗
║           TRÊS SUPERFÍCIES, TRÊS IMPLEMENTAÇÕES, ZERO FLYWHEEL     ║
║                                                                  ║
║  product_search:                                                 ║
║    UI (React)          ── implementação A                        ║
║    lib interna agente  ── implementação B  ← fix há 12 dias      ║
║    API pública (Go)    ── implementação C  ← bug vive há 12 dias ║
║                                                                  ║
║  Sinal de falha disponível nos traces do agente: DESPERDIÇADO    ║
║  (o agente executa ~8k buscas/dia; o bug apareceu ~340x         ║
║   nos traces ANTES do primeiro ticket)                           ║
║                                                                  ║
║  Cliente afetado:      1 pagante (que reclamou) + N calados     ║
║  Tempo de resolução:   12 dias (vs. ~1 se o sinal circulasse)   ║
║  Esforço duplicado:    2 fixes do mesmo bug em 2 codebases      ║
║  Auditção de contrato: impossível (não há contrato único)       ║
╚══════════════════════════════════════════════════════════════════╝
```

**O problema não é o bug.** Bugs acontecem em qualquer arquitetura. O problema é que a
falha foi *observada 340 vezes* pela superfície do agente e permaneceu invisível para a
API pública — porque superfícies duplicadas não compartilham só código, compartilham
**pontos de captura de falha**. O padrão Unified Tool Surface Flywheel propõe a
consolidação radical: **uma única autoridade de tool por operação, exposta identicamente
como UI, CLI e API pública, com os agentes internos consumindo exatamente as mesmas
tools** — de forma que toda falha de tool do agente dobre como sinal de qualidade da API
pública (`...patterns.md:185-205`).

O repo tem as peças isoladas — interface universal via materialização
(`docs/canonical/file-system-materialization.md:38,48`), dispatch único determinístico
(SOR:178), flywheels de falha-para-melhoria (`production-failure-regression-flywheel.md:28`)
— mas a mecânica central (autoridade única servindo UI+CLI+API com agentes como
consumidores das mesmas tools dos clientes) é NOT_FOUND (`...classification.md:165`).

**Sua missão:** implementar o `ToolSurfaceRegistry` que garante uma autoridade por tool
com superfícies ligadas a ela (recusando duplicações e backdoors agent-only), o
`ToolCallLedger` que registra invocações de todas as superfícies num plano só, e a
`FlywheelAnalysis` que converte falhas observadas em qualquer superfície em propostas de
melhoria ranqueadas por blast radius — com a invariável dupla: *every agent tool failure
doubles as public API quality signal*.

---

## 🧠 O Contexto

### O Modelo Mental: Superfície Única Como Multiplicador de Pontos de Captura

O padrão inverte a intuição de "agentes precisam de tools especiais". Em vez de o agente
ter tools próprias (mais rápidas de construir, mas que divergem), o agente consome **a
mesma autoridade** que os clientes externos:

```
   ┌─────────┐   ┌─────────┐   ┌────────────┐   ┌──────────────────┐
   │   UI    │   │   CLI   │   │ API pública │   │ agente interno   │
   └────┬────┘   └────┬────┘   └─────┬──────┘   └────────┬─────────┘
        │             │              │                   │
        ▼             ▼              ▼                   ▼
   ┌──────────────────────────────────────────────────────────────┐
   │        AUTORIDADE ÚNICA: tools.search_products v4            │
   │        (contrato versionado, uma implementação)              │
   └──────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
   ┌──────────────────────────────────────────────────────────────┐
   │   TOOL CALL LEDGER — toda invocação de toda superfície       │
   │   (caller, surface, ok/fail, error_code, latency)            │
   └──────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
   ┌──────────────────────────────────────────────────────────────┐
   │   FLYWHEEL ANALYSIS                                          │
   │   falha observada em QUALQUER superfície                     │
   │     → sinal de qualidade da AUTORIDADE                       │
   │     → melhoria proposta → upgrade da autoridade              │
   │     → TODOS os consumidores melhoram de uma vez              │
   └──────────────────────────────────────────────────────────────┘
```

Três decisões estruturais que o exercício codifica:

1. **Uma autoridade por tool.** Superfícies são *bindings* (UI, CLI, API, agente) para a
   mesma implementação versionada — nunca implementações paralelas. Divergência é
   detectável e rejeitada no registro.
2. **Sem backdoors agent-only.** A disciplina custosa do padrão: recusar a ferramenta
   "só para o agente" que bypassa a autoridade. Ela sempre parece pragmática no começo
   (`requires discipline to refuse agent-only backdoor tools`, `...patterns.md:203`) e é
   exatamente o que recria as três verdades.
3. **A falha do agente é amostra gratuita da API.** O agente interno executa a tool em
   volume alto e variado; quando ele falha, a API pública teria falhado igual — o cliente
   que não reclamou ainda foi representado. O custo assumido: superfície pública de
   falha maior (bugs induzidos pelo agente ficam visíveis, `...patterns.md:201`).

### O Que Você Vai Construir

1. `ToolSpec` — a autoridade: nome, versão, contrato, superfícies ligadas
2. `ToolSurfaceRegistry` — registra authorities e bindings; **rejeita** duplicação
   (segunda implementação da mesma operação) e backdoor agent-only
3. `ToolCallLedger` — invocações de todas as superfícies num plano consultável
4. `FlywheelAnalysis` — agrega falhas por authority, calcula blast radius
   (quantas superfícies/consumidores afetados), emite `ToolImprovementProposal` com o
   link explícito "falha do agente = sinal da API pública"

---

## 📋 Cenário

O estado do KODA (pós-audit do prólogo), pronto no starter:

- **Tools do domínio de catálogo:** `search_products`, `get_product_details`,
  `check_stock`
- **Registro proposto:** `search_products` como authority v4 com bindings
  `UI`/`CLI`/`PUBLIC_API`/`INTERNAL_AGENT`; `get_product_details` authority v2 com
  bindings `UI`/`PUBLIC_API`/`INTERNAL_AGENT`
- **Tentativas de registro que o sistema deve recusar:**
  - `product_search_legacy.py` como segunda authority para a mesma operação de busca
    (a duplicação do prólogo)
  - `search_products_raw_sql` com binding exclusivo `INTERNAL_AGENT` (o backdoor)
- **Ledger de 24h** (amostra no starter): ~8k calls do agente (o bug
  `OUT_OF_STOCK_LEAK` aparece 340x), ~1.2k da API pública (o mesmo erro 3x — os
  "calados" antes do ticket), UI e CLI saudáveis
- **Incidente do prólogo** como caso de teste ponta a ponta

---

## ✅ Requisitos

### Requisitos Funcionais

1. **RF1 — Autoridade única:** `ToolSurfaceRegistry.register_authority()` recusa uma
   segunda authority para operação já registrada (`RegistryError("duplicate authority")`)
   — a duplicação do prólogo não pode nem entrar.
2. **RF2 — Bindings, não cópias:** `bind_surface()` liga uma superfície (`UI`, `CLI`,
   `PUBLIC_API`, `INTERNAL_AGENT`) a uma authority existente; binding para authority
   inexistente é recusado.
3. **RF3 — Sem backdoors:** toda authority deve ter ao menos um binding de superfície
   *externa* (`UI`/`CLI`/`PUBLIC_API`). Authority com binding exclusivo
   `INTERNAL_AGENT` é recusada com `RegistryError("agent-only backdoor")`.
4. **RF4 — Ledger unificado:** `ToolCallRecord` carrega authority, versão, superfície,
   caller, `ok`, `error_code`, `latency_ms`; `ToolCallLedger.record()` aceita registro
   de qualquer superfície e `query()` filtra por authority/superfície/error_code.
5. **RF5 — Falha do agente é sinal da API:** `FlywheelAnalysis.analyze()` produz, para
   cada authority com falhas, um `ToolImprovementProposal` que inclui
   `api_quality_signal: bool` — `True` quando a falha foi observada em superfície
   `INTERNAL_AGENT` (ou qualquer superfície) e a authority tem binding `PUBLIC_API`
   (a API teria falhado igual).
6. **RF6 — Blast radius ranqueia:** propostas ordenadas por
   `affected_surfaces × failure_count` (o bug de `search_products`, presente em 3
   superfícies com 343 ocorrências, ranqueia acima de um bug só do agente).
7. **RF7 — Upgrade compartilhado:** `apply_proposal()` sobe a versão da authority e
   produz `upgrade_report` listando todas as superfícies/consumidores beneficiados de
   uma vez (nenhum consumidor fica na versão antiga).

### Requisitos Técnicos

1. **RT1 — Python 3.9+, stdlib apenas**, type hints obrigatórios
2. **RT2 — `dataclasses` + enums**; registry sem estado global — injeção explícita
3. **RT3 — Registro é a invariante:** nenhuma análise roda sobre registry inválido
   (analyze valida e recusa)
4. **RT4 — Ledger imutável por registro:** records são frozen; apendar é a única mutação

---

## 🏗️ Arquitetura do Sistema

```
┌───────────────────────────────────────────────────────────────────────┐
│                   UNIFIED TOOL SURFACE FLYWHEEL                        │
│                                                                       │
│  REGISTRY (a invariante)                                              │
│  ┌─────────────────────────────────────────────────────────────┐      │
│  │ authorities:                                                │      │
│  │   tools.search_products v4  ── bindings: UI, CLI,           │      │
│  │                               PUBLIC_API, INTERNAL_AGENT    │      │
│  │   tools.get_product_details v2 ── bindings: UI, PUBLIC_API, │      │
│  │                                  INTERNAL_AGENT             │      │
│  │                                                             │      │
│  │ GUARDS:                                                     │      │
│  │   ✗ duplicate authority p/ mesma operação   (RF1)           │      │
│  │   ✗ agent-only backdoor (sem superfície externa) (RF3)      │      │
│  │   ✗ binding para authority inexistente      (RF2)           │      │
│  └──────────────────────────┬──────────────────────────────────┘      │
│                             ▼                                         │
│  LEDGER (um plano, todas as superfícies)                              │
│  ┌─────────────────────────────────────────────────────────────┐      │
│  │ INTERNAL_AGENT │ search_products v4 │ FAIL OUT_OF_STOCK_LEAK │      │
│  │ PUBLIC_API     │ search_products v4 │ FAIL OUT_OF_STOCK_LEAK │      │
│  │ INTERNAL_AGENT │ get_product_details │ FAIL STALE_CACHE      │      │
│  │ UI / CLI       │ search_products v4 │ ok...                  │      │
│  └──────────────────────────┬──────────────────────────────────┘      │
│                             ▼                                         │
│  FLYWHEEL ANALYSIS                                                     │
│  ┌─────────────────────────────────────────────────────────────┐      │
│  │ por authority: failure_count, error_codes, affected_surfaces│      │
│  │ api_quality_signal: falha em qualquer superfície + binding   │      │
│  │   PUBLIC_API → a API teria falhado igual        (RF5)        │      │
│  │ blast_radius = affected_surfaces × failure_count (RF6)       │      │
│  │ → ToolImprovementProposal (ranqueado)                        │      │
│  └──────────────────────────┬──────────────────────────────────┘      │
│                             ▼                                         │
│  UPGRADE COMPARTILHADO (RF7)                                          │
│  ┌─────────────────────────────────────────────────────────────┐      │
│  │ tools.search_products v4 → v5                                │      │
│  │ upgrade_report: UI ✓ CLI ✓ PUBLIC_API ✓ INTERNAL_AGENT ✓    │      │
│  │ "todo consumidor melhorou de uma vez"                        │      │
│  └─────────────────────────────────────────────────────────────┘      │
└───────────────────────────────────────────────────────────────────────┘
```

---

## 🎯 Sua Tarefa em 3 Partes

### Parte 1 — Diagnosticar as três verdades (15 min)

Com o cenário do prólogo: quantas vezes o bug foi observado antes do primeiro ticket?
Quem observou e por que o sinal não circulou? Responda como comentário, e identifique
qual das três implementações (A/B/C) seria a authority certa na migração — e o que
acontece com as outras duas.

### Parte 2 — Registry e ledger (40 min)

Implemente `ToolSurfaceRegistry` com os três guards (RF1-RF3) e o `ToolCallLedger`
unificado (RF4). Verifique que as duas tentativas de registro do cenário são recusadas
com os erros corretos.

### Parte 3 — Flywheel (45 min)

Implemente `FlywheelAnalysis.analyze()` com `api_quality_signal` e blast radius (RF5-RF6),
e `apply_proposal()` com o upgrade report (RF7). Verifique o caso ponta a ponta do
prólogo: as 340 falhas do agente viram proposta #1 com `api_quality_signal=True`.

---

## 💻 Starter Code

```python
"""
Exercício 14 — Unified Tool Surface Flywheel
Nível 3 — Arquitetura Avançada

Uma autoridade de tool por operação, exposta como UI/CLI/API pública/agente.
Toda falha observada em qualquer superfície é sinal de qualidade da autoridade.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


# ============================================================================
# DATA MODELS
# ============================================================================

class Surface(Enum):
    UI = "ui"
    CLI = "cli"
    PUBLIC_API = "public_api"
    INTERNAL_AGENT = "internal_agent"

    @classmethod
    def external(cls) -> set["Surface"]:
        """Superfícies consumidas por clientes externos ao time de agentes."""
        return {cls.UI, cls.CLI, cls.PUBLIC_API}


class RegistryError(Exception):
    """Violação da invariante do registro."""
    def __init__(self, code: str, detail: str) -> None:
        self.code = code
        super().__init__(f"{code}: {detail}")


@dataclass(frozen=True)
class ToolSpec:
    """A autoridade: UMA implementação versionada de UMA operação."""
    authority_id: str          # ex.: "tools.search_products"
    operation: str             # ex.: "catalog.search_products"
    version: int
    contract: str              # referência do contrato (schema/OpenAPI path)

    @property
    def next_version(self) -> "ToolSpec":
        # TODO: implemente — mesma authority, version + 1
        raise NotImplementedError


@dataclass
class ToolSurfaceRegistry:
    """A invariante: uma authority por operação; bindings, não cópias."""
    authorities: dict[str, ToolSpec] = field(default_factory=dict)
    operation_index: dict[str, str] = field(default_factory=dict)  # operation → authority_id
    bindings: dict[str, set[Surface]] = field(default_factory=dict)

    def register_authority(self, spec: ToolSpec) -> None:
        """
        Recusas (RegistryError):
          "duplicate_authority" — operação já tem uma authority
        """
        # TODO: implemente
        raise NotImplementedError

    def bind_surface(self, authority_id: str, surface: Surface) -> None:
        """
        Recusas:
          "unknown_authority"   — authority não registrada
          "agent_only_backdoor" — primeiro binding seria exclusivamente
                                  INTERNAL_AGENT e nenhuma superfície externa
                                  está ligada nem prevista (RF3)
        Dica: valide o backdoor no bind — se surface é INTERNAL_AGENT e o
        conjunto de bindings resultante não intersecta Surface.external(),
        recuse. (Bindings externos podem vir antes OU depois; para o exercício,
        exija que TODO authority tenha ao menos um binding externo no momento
        do primeiro bind de INTERNAL_AGENT, OU exija finalize_authority().)
        """
        # TODO: implemente
        raise NotImplementedError

    def validate(self) -> None:
        """Levanta RegistryError se qualquer authority ficou sem binding externo."""
        # TODO: implemente
        raise NotImplementedError


@dataclass(frozen=True)
class ToolCallRecord:
    """Uma invocação — de qualquer superfície, num plano só."""
    authority_id: str
    version: int
    surface: Surface
    caller: str              # "rec-agent-01" | "customer_acme" | "webapp" | ...
    ok: bool
    error_code: str | None = None
    latency_ms: int = 0


@dataclass
class ToolCallLedger:
    records: list[ToolCallRecord] = field(default_factory=list)

    def record(self, rec: ToolCallRecord) -> None:
        # TODO: implemente (apensar; records são frozen)
        raise NotImplementedError

    def query(
        self,
        authority_id: str | None = None,
        surface: Surface | None = None,
        error_code: str | None = None,
        only_failures: bool = False,
    ) -> list[ToolCallRecord]:
        # TODO: implemente
        raise NotImplementedError


# ============================================================================
# PARTE 3 — FLYWHEEL ANALYSIS
# ============================================================================

@dataclass(frozen=True)
class ToolImprovementProposal:
    proposal_id: str
    authority_id: str
    error_code: str
    failure_count: int
    affected_surfaces: list[Surface]
    blast_radius: int                    # affected_surfaces × failure_count
    api_quality_signal: bool             # RF5: a API pública teria falhado igual
    evidence: str


@dataclass(frozen=True)
class UpgradeReport:
    authority_id: str
    from_version: int
    to_version: int
    beneficiaries: list[str]             # superfícies + callers beneficiados


@dataclass
class FlywheelAnalysis:
    registry: ToolSurfaceRegistry
    ledger: ToolCallLedger

    def analyze(self) -> list[ToolImprovementProposal]:
        """
        1. registry.validate() — análise não roda sobre invariante quebrada
        2. por authority × error_code: failure_count e superfícies afetadas
        3. api_quality_signal = authority tem binding PUBLIC_API e a falha
           foi observada (em qualquer superfície — tipicamente INTERNAL_AGENT
           em volume alto antes do cliente reclamar)
        4. ranquear por blast_radius desc
        """
        # TODO: implemente
        raise NotImplementedError

    def apply_proposal(self, proposal: ToolImprovementProposal) -> UpgradeReport:
        """
        Sobe a versão da authority e reporta TODOS os beneficiários:
        cada binding + cada caller distinto que invocou a authority.
        Nenhum consumidor fica na versão antiga (RF7).
        """
        # TODO: implemente
        raise NotImplementedError


# ============================================================================
# FIXTURES — o cenário pós-audit
# ============================================================================

def build_registry() -> ToolSurfaceRegistry:
    reg = ToolSurfaceRegistry()
    reg.register_authority(ToolSpec(
        "tools.search_products", "catalog.search_products", 4,
        contract="openapi:/products/search v4",
    ))
    for s in (Surface.UI, Surface.CLI, Surface.PUBLIC_API, Surface.INTERNAL_AGENT):
        reg.bind_surface("tools.search_products", s)
    reg.register_authority(ToolSpec(
        "tools.get_product_details", "catalog.get_product_details", 2,
        contract="openapi:/products/{id} v2",
    ))
    for s in (Surface.UI, Surface.PUBLIC_API, Surface.INTERNAL_AGENT):
        reg.bind_surface("tools.get_product_details", s)
    return reg


def ledger_24h() -> ToolCallLedger:
    """Amostra de 24h: o bug do prólogo + um bug menor só do agente."""
    led = ToolCallLedger()
    # bug OUT_OF_STOCK_LEAK: 340x no agente, 3x na API pública (os calados)
    for _ in range(340):
        led.record(ToolCallRecord(
            "tools.search_products", 4, Surface.INTERNAL_AGENT,
            "rec-agent-01", ok=False, error_code="OUT_OF_STOCK_LEAK", latency_ms=210,
        ))
    for _ in range(3):
        led.record(ToolCallRecord(
            "tools.search_products", 4, Surface.PUBLIC_API,
            "customer_acme", ok=False, error_code="OUT_OF_STOCK_LEAK", latency_ms=180,
        ))
    # tráfego saudável de fundo
    for _ in range(7600):
        led.record(ToolCallRecord(
            "tools.search_products", 4, Surface.INTERNAL_AGENT,
            "rec-agent-01", ok=True, latency_ms=95,
        ))
    for _ in range(1200):
        led.record(ToolCallRecord(
            "tools.search_products", 4, Surface.PUBLIC_API,
            "customer_acme", ok=True, latency_ms=120,
        ))
    # bug menor: cache stale só perceptível pelo agente (multi-get)
    for _ in range(12):
        led.record(ToolCallRecord(
            "tools.get_product_details", 2, Surface.INTERNAL_AGENT,
            "rec-agent-01", ok=False, error_code="STALE_CACHE", latency_ms=60,
        ))
    return led


# ============================================================================
# TESTS
# ============================================================================

def test_registry_rejects_duplicate_authority():
    reg = build_registry()
    try:
        reg.register_authority(ToolSpec(
            "tools.product_search_legacy", "catalog.search_products", 1,
            contract="legacy:product_search.py",
        ))
        raise AssertionError("duplicação do prólogo deve ser recusada")
    except RegistryError as e:
        assert e.code == "duplicate_authority"
    print("TESTE 1 PASSOU")


def test_registry_rejects_agent_only_backdoor():
    reg = ToolSurfaceRegistry()
    reg.register_authority(ToolSpec(
        "tools.search_products_raw_sql", "catalog.search_products_raw", 1,
        contract="none (raw sql)",
    ))
    try:
        reg.bind_surface("tools.search_products_raw_sql", Surface.INTERNAL_AGENT)
        raise AssertionError("backdoor agent-only deve ser recusado")
    except RegistryError as e:
        assert e.code == "agent_only_backdoor"
    # com um binding externo primeiro, o mesmo binding de agente é aceito
    reg.bind_surface("tools.search_products_raw_sql", Surface.PUBLIC_API)
    reg.bind_surface("tools.search_products_raw_sql", Surface.INTERNAL_AGENT)
    print("TESTE 2 PASSOU")


def test_ledger_queries_cross_surface():
    led = ledger_24h()
    fails = led.query(authority_id="tools.search_products", only_failures=True)
    agent_fails = [r for r in fails if r.surface == Surface.INTERNAL_AGENT]
    api_fails = [r for r in fails if r.surface == Surface.PUBLIC_API]
    assert len(agent_fails) == 340
    assert len(api_fails) == 3
    assert all(r.error_code == "OUT_OF_STOCK_LEAK" for r in fails)
    print("TESTE 3 PASSOU")


def test_flywheel_agent_failure_is_api_signal():
    analysis = FlywheelAnalysis(build_registry(), ledger_24h())
    proposals = analysis.analyze()

    assert proposals, "deve haver ao menos 2 propostas"
    top = proposals[0]
    # OUT_OF_STOCK_LEAK: 343 falhas em 2 superfícies → blast radius maior
    assert top.error_code == "OUT_OF_STOCK_LEAK"
    assert top.failure_count == 343
    assert set(top.affected_surfaces) == {Surface.INTERNAL_AGENT, Surface.PUBLIC_API}
    assert top.blast_radius == 343 * 2
    # RF5: a falha observada no agente é sinal da API pública
    assert top.api_quality_signal is True
    # o bug menor do agente também é sinal da API (get_product_details tem
    # binding PUBLIC_API — a API teria falhado igual), mas ranqueia abaixo
    stale = next(p for p in proposals if p.error_code == "STALE_CACHE")
    assert stale.api_quality_signal is True
    assert stale.blast_radius < top.blast_radius
    print("TESTE 4 PASSOU")


def test_upgrade_is_shared():
    reg, led = build_registry(), ledger_24h()
    analysis = FlywheelAnalysis(reg, led)
    top = analysis.analyze()[0]
    report = analysis.apply_proposal(top)

    assert report.authority_id == "tools.search_products"
    assert report.from_version == 4 and report.to_version == 5
    beneficiaries = set(report.beneficiaries)
    # TODAS as superfícies e callers distintos beneficiados de uma vez
    assert {"ui", "cli", "public_api", "internal_agent"} <= beneficiaries
    assert "customer_acme" in beneficiaries and "rec-agent-01" in beneficiaries
    assert reg.authorities["tools.search_products"].version == 5
    print("TESTE 5 PASSOU")


if __name__ == "__main__":
    print("=" * 60)
    print("EXERCÍCIO 14: UNIFIED TOOL SURFACE FLYWHEEL")
    print("=" * 60)
    # Descomente após implementar:
    # test_registry_rejects_duplicate_authority()
    # test_registry_rejects_agent_only_backdoor()
    # test_ledger_queries_cross_surface()
    # test_flywheel_agent_failure_is_api_signal()
    # test_upgrade_is_shared()
    print("\nTODO: implemente registry+guards, ledger e FlywheelAnalysis")
```

---

## ✅ Validação: Critérios de Aceitação

Seu código será considerado **APROVADO** quando:

- [ ] `register_authority()` recusa a segunda authority para `catalog.search_products` com `duplicate_authority` (RF1)
- [ ] `bind_surface()` recusa binding exclusivo `INTERNAL_AGENT` com `agent_only_backdoor` e aceita o mesmo binding após um binding externo (RF3)
- [ ] `ledger.query()` cruza superfícies: 340 falhas do agente + 3 da API para o mesmo error code (RF4)
- [ ] `analyze()` produz proposta #1 `OUT_OF_STOCK_LEAK` com 343 falhas, 2 superfícies, blast radius 686 e `api_quality_signal=True` (RF5-RF6)
- [ ] O bug `STALE_CACHE` (só do agente, authority com binding API) também carrega `api_quality_signal=True` e ranqueia abaixo
- [ ] `apply_proposal()` sobe `search_products` v4→v5 e o `UpgradeReport` lista as 4 superfícies + os 2 callers — ninguém fica para trás (RF7)
- [ ] `analyze()` recusa rodar sobre registry sem `validate()` passar (RT3)

---

## 📊 Rubric de Avaliação

| Critério | Peso | Insuficiente (0-3) | Básico (4-6) | Proficiente (7-8) | Excelente (9-10) |
|---|---|---|---|---|---|
| **Registry + guards (Parte 2)** | 30% | Não implementado | Registra sem guards | RF1+RF2 | Três guards + validate() como pré-condição de análise |
| **Ledger (Parte 2)** | 20% | Não implementado | Records sem query | Query multi-filtro | Frozen records + plano único cross-surface auditável |
| **FlywheelAnalysis (Parte 3)** | 35% | Não implementado | Conta falhas sem ranking | Blast radius + ranking | api_quality_signal como cidadão de primeira classe com evidência |
| **Upgrade compartilhado (Parte 3)** | 15% | Não implementado | Sobe versão | Report de superfícies | Superfícies + callers distintos, "ninguém fica para trás" verificável |

**Nota final:** Média ponderada. **Aprovação:** >= 7.0

---

## 💡 Dicas para Implementação

1. **O guard do backdoor é uma decisão de produto, não um detalhe.** A ferramenta agent-only sempre chega com boa justificativa ("é só um SELECT rápido"). Recuse-a no registro — se a operação importa para o agente, importa para a API; se não importa para ninguém externo, pergunte por que ela existe.
2. **Blast radius motiva prioridade.** 12 falhas só do agente (STALE_CACHE) são menos urgentes que 343 em duas superfícies — não por contagem, mas por alcance. O produto é `affected_surfaces × failure_count`, não a contagem pura.
3. **O agente é seu cliente mais barato de instrumentar.** Ele faz 8k calls/dia com variação que nenhum cliente gera sozinho; quando a authority quebra com ele, quebraria com os outros. As 340 observações do prólogo eram o ticket #4471 escrito 12 dias antes — só não tinha canal.

---

## ❓ Dúvidas Comuns

**P: Expor o agente à API pública não amplia a superfície de falha pública?**
R: Sim — e o padrão assume isso explicitamente ("larger public failure surface", `...patterns.md:201`). Bugs induzidos pelo agente ficam visíveis para clientes. A aposta é que uma superfície única com sinal rico vale mais que três superfícies cegas.

**P: Isso não é só "compartilhar código entre serviços"?**
R: Sharing de código é o mecanismo; a invariante é o *registro*. Sem registry com guards, sharing degrada de volta para três cópias no primeiro prazo apertado. Compare com [[docs/canonical/deterministic-tool-dispatch|Deterministic Tool Dispatch]]: lá a autoridade é o dispatch; aqui a autoridade é a tool em si — mesma disciplina, outro nível.

**P: Por que não deixar o agente com tools melhores que as da API (superiores, internas)?**
R: Porque "melhor que a API" significa divergente da API — o agente passa a viver num produto que não existe para o cliente, e todo sinal que ele gera para de representar a experiência pública. É a versão fancy das três verdades.

**P: Qual a relação com o File-System Materialization do repo?**
R: É o vizinho conceitual: `file-system-materialization.md:48` defende o file system como interface universal que o agente já domina — um *substrato* unificado. O padrão aqui fecha o ciclo inverso: a unificação não serve só para o agente consumir, mas para o consumo do agente *informar a qualidade da superfície* (`...classification.md:167`).

---

## 🚀 Próximo Passo

Depois de completar este exercício:

1. Leia o padrão 9 completo e sua classificação: `docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-patterns.md:185-205` e `...classification.md:150-167` — as três docs canônicas que o reframe conecta
2. Audite o KODA real: para cada operação de catálogo/pedido, quantas implementações existem hoje? Qual seria a authority de cada uma e quais guards o migration exigiria?
3. Siga para o [[curriculum/03-nivel-3-advanced-architecture/exercises/exercise-15-agent-first-data-foundation|Exercício 15: Agent-First Data Foundation]] — a unificação que o flywheel pressupõe quando a "tool" é dados

---

*Exercício 14 | Nível 3 — Arquitetura Avançada | Unified Tool Surface Flywheel*

**O agente que consome a API pública é o cliente que reclama 340 vezes antes do ticket. Superfície única, sinal compartilhado.**
