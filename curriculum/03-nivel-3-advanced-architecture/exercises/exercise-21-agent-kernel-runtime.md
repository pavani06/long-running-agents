---
title: "Exercício 21: Agent Kernel Runtime — O Agente como Processo de Primeira Classe do SEU Sistema"
type: exercise
level: 3
aliases: ["agent kernel runtime", "kernel de agentes", "agente como processo de primeira classe", "scheduler isolamento journaling", "runtime próprio vs framework", "inversão de posse do framework", "agent process isolation"]
tags: ["curriculo-conteudo", "nivel-3", "agentes-orquestracao", "arquitetura", "harness-engineering", "production", "governanca", "agent-loop", "stack-tooling"]
relates-to: ["[[docs/analysis/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt-patterns|Padrões Agent Frameworks Considered Harmful]]", "[[docs/analysis/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt-classification|Classificação Agent Frameworks Considered Harmful]]", "[[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]", "[[docs/canonical/model-agnostic-agent-vm-harness|Model-Agnostic Agent VM Harness]]", "[[docs/canonical/alarm-clock-agent-lifecycle|Alarm-Clock Agent Lifecycle]]", "[[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent Operating System]]", "[[docs/canonical/goal-driven-agents-over-workflows|Goal-Driven Agents over Workflows]]", "[[curriculum/03-nivel-3-advanced-architecture/exercises/exercise-18-typed-event-boundaries|Exercício 18: Typed Tool and Event Boundaries]]", "[[curriculum/03-nivel-3-advanced-architecture/exercises/exercise-20-causal-event-log|Exercício 20: Append-Only Causal Event Log]]"]
duration: "90-120 min"
last_updated: 2026-09-02
---

# ⚙️ Exercício 21: Agent Kernel Runtime — O Agente como Processo de Primeira Classe do SEU Sistema
## Nível 3 — Arquitetura Avançada

**Tempo Estimado:** 90-120 minutos
**Dificuldade:** (Avançado)
**Pré-requisito:** Ter lido `01-multi-agent-systems.md` (Nível 3) + `docs/canonical/owned-agent-control-loop.md` + Exercícios 18 (fronteiras tipadas) e 20 (log causal)
**Objetivo:** Unificar as três responsabilidades clássicas de SO — agendamento, isolamento por processo e journaling — num runtime próprio onde o agente é processo de primeira classe do sistema do usuário, o kernel não sabe o que o agente faz, e o frontend de definição troca sem trocar o kernel

---

## 📖 Prólogo: O Agente Que Virou Plugin de Terceiro

### Reunião de migração. O framework muda a API de novo.

```
ENG_LEAD:   "o LangGraph vai mudar a API de checkpoint na v2. Nossos
             seis agentes param até migrarmos. Duas semanas de trabalho
             — de novo."

PM:         "pergunta desconfortável: quem é dono de quem aqui? Nossos
             agentes, os prompts, o estado de execução — tudo isso é
             NOSSO ou é DELES?"

ENG_LEAD:   "técnica e legalmente é nosso. Operacionalmente... o loop
             de execução vive dentro do graph deles. A iteração dentro
             do grafo é gerenciada pelo framework — o canonical até
             documenta isso como estado atual a gente"

PM:         "então quando o framework respira, a frota para. O agente
             deixou de ser um processo do NOSSO sistema e virou um
             plugin do sistema DELES."

ENG_LEAD:   "é a inversão exata. Deveria ser o contrário: o runtime
             chama o agente, nunca o agente dentro da abstração do
             runtime de terceiro. E olha o irônico: o SO resolve isso
             há 50 anos. Agendamento, isolamento por processo, journal.
             A gente reinventa essas três palavras por framework."

PM:         "e se a gente pegasse as três emprestadas de vez?"
```

**O custo da posse invertida:**

```
╔══════════════════════════════════════════════════════════════════╗
║   FRAMEWORKS JUST CALL CODE — SÓ QUE AO CONTRÁRIO                  ║
║                                                                  ║
║  A tese do fonte (patterns.md:123):                              ║
║  "frameworks just call code; your agents live inside their        ║
║   abstractions" — o agente deixa de ser processo isolado do       ║
║   SEU sistema e vira plugin de terceiro                           ║
║                                                                  ║
║  Onde o repo está hoje:                                          ║
║   • o problema está documentado com força — tabela               ║
║     Framework-Owned vs Developer-Owned (owned-agent-control-     ║
║     loop.md:22-27,77-85)                                         ║
║   • mas a implementação de referência DELEGA o loop ao LangGraph ║
║     (owned-agent-control-loop.md:107) — o exato estado que o     ║
║     padrão denuncia                                               ║
║                                                                  ║
║  As três peças existem SOLTAS no repo:                            ║
║   agendamento → alarm-clock (wake-work-sleep, :44-48)             ║
║   isolamento → VM harness (per-agent VM, model-agnostic:45)       ║
║   journaling → tracing centralizado + o log causal do Ex. 20      ║
║                                                                  ║
║  O que NÃO existe (classification.md:135, NOT_FOUND): nenhum      ║
║  runtime une scheduler + isolamento + journal com o agente como   ║
║  processo de primeira classe — o kernel-named-pattern             ║
╚══════════════════════════════════════════════════════════════════╝
```

**O problema não é usar framework.** É a direção da chamada. Um SO clássico agenda
processos, isola a execução de cada um e registra o que aconteceu — e **não sabe nem
precisa saber** o que o processo faz dentro (`...patterns.md:129`). O padrão reusa
essas três responsabilidades literais: o runtime é do usuário, o agente é processo
dele, e o framework — quando existe — vira biblioteca chamada, nunca o recipiente
(`...patterns.md:133`). O repo tem as três peças soltas (alarm-clock, VM harness,
tracing) e a inversão documentada como problema; o que não tem é a unificação
ensinável (`...classification.md:127,137`).

**Sua missão:** implementar o `AgentKernel` — o `Scheduler` que acorda specs por
tick e por evento (determinístico), o `Isolation` que dá a cada agente um
`AgentProcess` com estado próprio e contenção de crash (um agente que explode vira
FAILED, a frota segue), o `Journal` que registra o ciclo de vida (spawn/tick/
conclusão/falha) sem inspecionar o conteúdo do agente, os `AgentSpec`s declarativos
da userland que o kernel carrega de QUALQUER frontend — e a prova da inversão: o
kernel não importa um único agente concreto, e a frota inteira se define como dados.

---

## 🧠 O Contexto

### O Modelo Mental: Três Responsabilidades de SO, Agente como Processo

O padrão é um reframe de posse com mecânica conhecida
(`...patterns.md:133`: reutilizar responsabilidades clássicas de SO em vez de
reinventá-las). Quatro propriedades o definem:

1. **O kernel tem três papéis e nenhum conhecimento:**

```
                USERLAND (dados, não código do kernel)
   ┌──────────────────────────────────────────────────────┐
   │ AgentSpec: transcriber │ summarizer │ poster          │
   │   entry: o que fazer quando acorda                   │
   │   trigger: TICK n | EVENT tipo X (Ex. 18/20)         │
   │   accepts/emits: eventos tipados                     │
   └───────────────────────┬──────────────────────────────┘
                           ▼ kernel CARREGA a definição
   ┌──────────────────────────────────────────────────────┐
   │ AGENT KERNEL                                          │
   │                                                      │
   │ SCHEDULER    quem acorda agora? (tick + triggers)    │
   │ ISOLATION    cada agente = AgentProcess com estado   │
   │              próprio; crash contido ao processo      │
   │ JOURNAL      registra CICLO DE VIDA — spawn, tick,   │
   │              done, failed — nunca o conteúdo         │
   │                                                      │
   │        "ao kernel não importa o que o agente faz"    │
   │         (patterns.md:129)                            │
   └──────────────────────────────────────────────────────┘
```

2. **A inversão é testável.** O kernel chama o agente (via callback registrado da
   userland); o agente nunca chama o kernel por dentro — ele emite eventos e termina.
   Framework inverte isso: o agente vive DENTRO da abstração de terceiro, e a
   implementação de referência do repo está exatamente aí
   (`docs/canonical/owned-agent-control-loop.md:107`).

3. **Isolamento com contenção de crash.** Cada processo tem estado próprio
   (vizinhaça do slot "Per-agent VM" do `model-agnostic-agent-vm-harness.md:45`);
   um agente que levanta exceção vira FAILED no journal e o tick segue — a frota não
   herda o crash.

4. **O frontend é trocável.** A definição do agente é formato da userland
   (`...patterns.md:135`): markdown, YAML, dataclasses, dicts — o kernel só conhece
   `AgentSpec`. Trocar o frontend não toca no kernel; os `.opencode/agents/*.md`
   do repo são um frontend real desse contrato (`...classification.md:105`).

Os vizinhos do repo, e por que não fecham sozinhos: o `owned-agent-control-loop`
diagnostica a inversão mas documenta a delegação ao LangGraph (`...md:107`); o
`alarm-clock-agent-lifecycle` tem wake-work-sleep com self-scheduling — agendamento
sem runtime único (`...md:44-48`, e o próprio canonical registra que faltava
scheduler, `:85`); o `model-agnostic-agent-vm-harness` tem o slot de VM por agente —
isolamento sem scheduler nem journal no mesmo runtime (`...md:55-70`); o
`closed-loop-agent-operating-system` é OS de OPERAÇÕES da frota (intake/roteamento/
writeback), não kernel de processos — e se declara Partial porque a mecânica está
espalhada (`...md:61-68`).

### O Que Você Vai Construir

1. `AgentSpec` — a definição declarativa da userland: agent_id, entry (a função da
   userland), trigger (tick ou evento), accepts/emits
2. `AgentProcess` — o processo de primeira classe: estado próprio (dict fechado),
   status PENDING/RUNNING/DONE/FAILED, e o resultado do último run
3. `Scheduler` — decide quem acorda: agents de tick acordam em `tick % interval == 0`;
   agents de evento acordam quando o evento do seu trigger está na caixa; ordem
   determinística por agent_id
4. `Journal` — o registro de ciclo de vida (SPAWNED/TICKED/DONE/FAILED) com causa
   (qual tick, qual trigger); SEM payload do agente — o kernel não inspeciona conteúdo
5. `AgentKernel.spawn()/tick()` — carrega specs, executa os acordados com isolamento
   (exceção contida → FAILED), publica eventos emitidos na caixa interna (passando
   pela noção de fronteira do Exercício 18: só tipo declarado em `emits`)
6. `run_fleet()` — a simulação: transcriber (evento) → summarizer (evento) → poster
   (tick), com o summarizer CRASHANDO na primeira passada — frota contida, journal
   completo — e a prova da troca de frontend: os mesmos specs carregados de dicts
   produzem comportamento idêntico

---

## 📋 Cenário

A fleet de nota de voz do KODA, agora como processos: o `webhook-sim` (tick 1) recebe
a nota e emite `voice_note.received`; o `transcriber` acorda por esse evento, emite
`transcription.completed`; o `summarizer` acorda pela transcrição, emite
`brief.drafted` — e na PRIMEIRA rodada ele crasha (payload inesperado); o `poster`
acorda por tick 2 e posta o que houver. Sem kernel: o crash do summarizer derrubaria a
pipeline inteira (o poster nunca roda, o trabalho do webhook morre com ele). Com
kernel: summarizer vira FAILED no journal com a causa, o tick 2 roda o poster, e o
journal conta a história completa sem nunca ter lido o conteúdo de nenhum agente. No
final, a mesma fleet redefinida a partir de dicts crus (o "frontend alternativo")
roda idêntica.

---

## ✅ Requisitos

### Requisitos Funcionais

1. **RF1 — Spec declarativa, kernel agnóstico:** `AgentSpec` carrega agent_id, entry
   (callback da userland), trigger (`TickTrigger(interval)` ou
   `EventTrigger(event_type)`) e tuple `emits`; o kernel não referencia NENHUM agente
   concreto — `spawn()` aceita qualquer spec compatível.
2. **RF2 — Agendamento determinístico:** a cada `tick()`, acordam (em ordem estável
   por agent_id) os processos de tick cujo `interval` divide o tick atual, e os de
   evento cujo trigger está na caixa de eventos ainda não consumida por eles; nada
   mais acorda.
3. **RF3 — Isolamento e contenção:** cada `AgentProcess` tem estado próprio (dict)
   inacessível a outros processos; exceção levantada por um entry marca SÓ aquele
   processo como FAILED (com `error` registrado no processo e a causa no journal) e o
   tick continua; o kernel nunca propaga exceção de agente.
4. **RF4 — Journal de ciclo de vida, não de conteúdo:** o journal registra
   SPAWNED/TICKED/DONE/FAILED com (tick, agent_id, detalhe operacional); NENHUMA
   entrada carrega payload ou output do agente — o kernel não sabe o que o agente
   faz.
5. **RF5 — Emissão pela fronteira:** evento publicado por um processo precisa estar
   no `emits` da spec (a fronteira mínima do Exercício 18); emissão não declarada é
   descartada com registro de violação no journal (`EMISSION_REJECTED`) — não barra o
   processo.
6. **RF6 — Frontend trocável:** `specs_from_dicts()` constrói as mesmas specs a
   partir de dicts crus (o formato da userland: YAML/JSON-like); `run_fleet()` com
   specs de dataclass e specs de dict produz journals com a MESMA sequência de
   (tick, agent_id, tipo de entrada) — o kernel não sente a troca.

### Requisitos Técnicos

1. **RT1 — Python 3.9+, stdlib apenas**, type hints obrigatórios
2. **RT2 — `dataclasses` + enums**; callbacks da userland tipados
   (`Callable[[AgentContext], AgentResult]`); simulação determinística
3. **RT3 — Kernel sem I/O e sem estado global**: toda mutação passa por
   spawn/tick; a caixa de eventos é interna e só se enche via emissões validadas
4. **RT4 — Prova de agnosticismo:** o módulo do kernel não importa módulo de agente
   algum; agentes são injetados via spec

---

## 🏗️ Arquitetura do Sistema

```
┌────────────────────────────────────────────────────────────────────────┐
│                       AGENT KERNEL RUNTIME                             │
│                                                                        │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │ FRONTENDS (userland — trocáveis, RF6)                           │    │
│  │ dataclasses │ dicts/YAML │ (markdown no repo real: .opencode/)   │    │
│  └──────────────────────────┬─────────────────────────────────────┘    │
│                             ▼ AgentSpec                                │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │ SCHEDULER (RF2)                                                 │    │
│  │ tick n: quem acorda? tick-interval ∨ event-trigger na caixa     │    │
│  │ ordem estável por agent_id — determinismo testável               │    │
│  └──────────────────────────┬─────────────────────────────────────┘    │
│                             ▼                                          │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │ ISOLATION (RF3) — agente = processo de primeira classe           │    │
│  │ estado próprio por processo │ crash → FAILED contido              │   │
│  │ emissão pela fronteira (RF5): fora de emits → rejeitada          │    │
│  └──────────────────────────┬─────────────────────────────────────┘    │
│                             ▼                                          │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │ JOURNAL (RF4) — ciclo de vida, nunca conteúdo                    │    │
│  │ SPAWNED │ TICKED │ DONE │ FAILED │ EMISSION_REJECTED             │    │
│  │ ao kernel não importa o que o agente faz (patterns.md:129)      │    │
│  └────────────────────────────────────────────────────────────────┘    │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 🎯 Sua Tarefa em 3 Partes

### Parte 1 — Diagnosticar a inversão no repo (15 min)

Com a tabela do prólogo: para cada peça solta do repo (alarm-clock, VM harness,
tracing centralizado), diga qual responsabilidade do kernel ela cobre e qual falta
para a unificação. Depois: onde a implementação de referência do repo delega o loop
ao framework (cite o canonical)? Responda como comentário.

### Parte 2 — Specs, processos e scheduler (40 min)

Implemente `AgentSpec`/triggers, `AgentProcess`, `AgentContext`/`AgentResult`,
`Scheduler.decide()` (RF1-RF2) e o isolamento do processo (RF3).

### Parte 3 — Kernel, journal e a frota (45 min)

Implemente `AgentKernel.spawn()/tick()` com journal de ciclo de vida (RF4), a
fronteira de emissão (RF5) e `run_fleet()` nas duas passadas (crash contido; frontend
de dicts com journal idêntico) (RF6).

---

## 💻 Starter Code

```python
"""
Exercício 21 — Agent Kernel Runtime
Nível 3 — Arquitetura Avançada

Três responsabilidades clássicas de SO num runtime próprio: scheduler
(acorda por tick e por evento), isolamento (agente = processo de
primeira classe, crash contido) e journaling (ciclo de vida, nunca
conteúdo). O kernel chama o agente; o agente nunca vive dentro do
kernel de terceiro.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Mapping, Optional, Sequence, Union


# ============================================================================
# DATA MODELS — a userland
# ============================================================================

@dataclass(frozen=True)
class TickTrigger:
    interval: int                 # acorda quando tick % interval == 0


@dataclass(frozen=True)
class EventTrigger:
    event_type: str               # acorda quando o evento está na caixa


Trigger = Union[TickTrigger, EventTrigger]


@dataclass(frozen=True)
class OutboundEvent:
    event_type: str
    payload: Mapping[str, object]


@dataclass(frozen=True)
class AgentResult:
    """O que o agente devolve ao kernel ao terminar o run."""
    note: str = ""                              # ciclo de vida apenas
    emitted: tuple[OutboundEvent, ...] = ()     # passa pela fronteira (RF5)


# O callback da userland: recebe o contexto, devolve o resultado.
# O agente NUNCA chama o kernel por dentro (a inversão, patterns.md:123).
AgentEntry = Callable[["AgentContext"], AgentResult]


@dataclass(frozen=True)
class AgentSpec:
    """A definição declarativa — dados, não código do kernel (RF1)."""
    agent_id: str
    entry: AgentEntry
    trigger: Trigger
    emits: tuple[str, ...] = ()   # tipos que DECLARA emitir (Exercício 18)


class ProcessStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    DONE = "done"
    FAILED = "failed"


@dataclass
class AgentProcess:
    """O agente como processo de primeira classe (RF3)."""
    spec: AgentSpec
    status: ProcessStatus = ProcessStatus.PENDING
    state: dict[str, object] = field(default_factory=dict)  # privado
    error: Optional[str] = None
    last_note: str = ""


@dataclass(frozen=True)
class AgentContext:
    """O que o kernel entrega ao processo ao acordá-lo — e NADA mais."""
    agent_id: str
    tick: int
    state: Mapping[str, object]          # leitura do estado do processo
    inbox: tuple[OutboundEvent, ...]     # triggers de evento consumidos


# ============================================================================
# JOURNAL — ciclo de vida, nunca conteúdo (RF4)
# ============================================================================

class JournalEntryType(Enum):
    SPAWNED = "spawned"
    TICKED = "ticked"                  # processo acordado num tick
    DONE = "done"
    FAILED = "failed"
    EMISSION_REJECTED = "emission_rejected"   # fronteira (RF5)


@dataclass(frozen=True)
class JournalEntry:
    tick: int
    agent_id: str
    entry_type: JournalEntryType
    detail: str                        # operacional: causa, tipo de evento


@dataclass
class Journal:
    _entries: list[JournalEntry] = field(default_factory=list)

    def record(self, tick: int, agent_id: str,
               entry_type: JournalEntryType, detail: str = "") -> None:
        # TODO: implemente
        raise NotImplementedError

    def of_agent(self, agent_id: str) -> tuple[JournalEntry, ...]:
        # TODO: implemente
        raise NotImplementedError

    def all(self) -> tuple[JournalEntry, ...]:
        # TODO: implemente
        raise NotImplementedError

    def lifeline_signature(self) -> tuple[tuple[int, str, str], ...]:
        """(tick, agent_id, entry_type) de toda entrada — a identidade
        comportamental usada para provar a troca de frontend (RF6)."""
        # TODO: implemente
        raise NotImplementedError


# ============================================================================
# SCHEDULER — quem acorda (RF2)
# ============================================================================

@dataclass(frozen=True)
class QueuedEvent:
    """Evento na caixa interna do kernel, com o tick em que chegou."""
    event: OutboundEvent
    tick: int


@dataclass
class Scheduler:
    """Decide quem acorda — determinístico por construção (RF2)."""

    def decide(
        self,
        processes: Sequence[AgentProcess],
        tick: int,
        inbox: Sequence[QueuedEvent],
        consumed_by: Mapping[str, tuple[str, ...]],
    ) -> list[AgentProcess]:
        """
        Acordam, em ordem estável por agent_id:
          - tick processes com tick % interval == 0
          - event processes cujo event_type de trigger está na caixa e
            AINDA não foi consumido por eles (consumed_by mapeia
            agent_id → ids/tipos já consumidos; use o tipo+tick como
            chave de consumo)
        """
        # TODO: implemente
        raise NotImplementedError


# ============================================================================
# KERNEL — spawn, tick, isolamento, fronteira (RF1, RF3-RF5)
# ============================================================================

class AgentKernel:
    """Agenda processos, isola execução, registra journal (RF1)."""

    def __init__(self) -> None:
        self.journal = Journal()
        self._processes: dict[str, AgentProcess] = {}
        self._inbox: list[QueuedEvent] = []
        self._consumed: dict[str, list[tuple[str, int]]] = {}

    def spawn(self, spec: AgentSpec) -> AgentProcess:
        """Carrega a definição e registra SPAWNED (RF1, RF4)."""
        # TODO: implemente
        raise NotImplementedError

    def tick(self, tick: int) -> None:
        """
        Um passo do kernel:
          1. scheduler decide quem acorda (RF2)
          2. para cada acordado, em ordem: constrói AgentContext
             (estado + inbox do trigger), marca RUNNING/TICKED, chama
             entry com isolamento (RF3):
               - sucesso → DONE, emissões validadas contra emits (RF5)
               - exceção → FAILED com causa; NÃO propaga (RF3)
          3. eventos aceitos entram na caixa interna (RT3)
        """
        # TODO: implemente
        raise NotImplementedError

    def process(self, agent_id: str) -> Optional[AgentProcess]:
        # TODO: implemente
        raise NotImplementedError


# ============================================================================
# PARTE 3 — A FROTA DE NOTA DE VOZ (frontend: dataclasses)
# ============================================================================

def webhook_entry(ctx: AgentContext) -> AgentResult:
    """Tick 1: recebe a nota e emite voice_note.received (uma vez)."""
    if "sent" in ctx.state:
        return AgentResult(note="idle")
    return AgentResult(
        note="voice note received",
        emitted=(OutboundEvent("voice_note.received", {"note_id": "n-42"}),),
    )


def transcriber_entry(ctx: AgentContext) -> AgentResult:
    """Acorda por voice_note.received; emite transcription.completed."""
    return AgentResult(
        note="transcribed",
        emitted=(OutboundEvent("transcription.completed",
                               {"text": "reunião, fone, 300"}),),
    )


def summarizer_entry(ctx: AgentContext) -> AgentResult:
    """Acorda por transcription.completed — CRASHA na primeira vez
    (payload inesperado), sussa na segunda."""
    runs = int(ctx.state.get("runs", 0)) + 1
    if runs == 1:
        raise ValueError("unexpected transcript shape (v1)")
    return AgentResult(
        note="brief drafted",
        emitted=(OutboundEvent("brief.drafted", {"summary": "cliente quer fone"}),),
    )


def poster_entry(ctx: AgentContext) -> AgentResult:
    """Tick 2: posta o que houver na caixa que ele aceita."""
    return AgentResult(note="posted to slack")


def build_fleet_specs() -> list[AgentSpec]:
    return [
        AgentSpec("webhook-sim", webhook_entry, TickTrigger(1),
                  emits=("voice_note.received",)),
        AgentSpec("transcriber", transcriber_entry,
                  EventTrigger("voice_note.received"),
                  emits=("transcription.completed",)),
        AgentSpec("summarizer", summarizer_entry,
                  EventTrigger("transcription.completed"),
                  emits=("brief.drafted",)),
        AgentSpec("poster", poster_entry, TickTrigger(2)),
    ]


def specs_from_dicts(dicts: list[dict[str, object]],
                     entries: Mapping[str, AgentEntry]) -> list[AgentSpec]:
    """
    Frontend alternativo (RF6): constrói specs de dicts crus (o formato
    YAML/JSON-like da userland), resolvendo o entry pelo nome em
    `entries`. O kernel não sente a diferença.
    """
    # TODO: implemente
    raise NotImplementedError


@dataclass(frozen=True)
class FleetRun:
    journal: Journal
    statuses: Mapping[str, ProcessStatus]


def run_fleet(specs: list[AgentSpec], ticks: int = 3) -> FleetRun:
    """
    Sobe o kernel, spawna todos, roda `ticks` ticks. Retorna o journal
    e o status final de cada processo.
    """
    # TODO: implemente
    raise NotImplementedError


# ============================================================================
# TESTS
# ============================================================================

def test_scheduler_determinism():
    specs = build_fleet_specs()
    procs = [AgentProcess(s) for s in specs]
    inbox = [QueuedEvent(OutboundEvent("voice_note.received", {}), 1)]
    woke = Scheduler().decide(procs, tick=2, inbox=inbox, consumed_by={})
    ids = [p.spec.agent_id for p in woke]
    assert ids == sorted(ids), "ordem estável por agent_id (RF2)"
    assert "poster" in ids and "webhook-sim" in ids, "tick 1 e 2 dividem 2"
    assert "transcriber" in ids, "evento na caixa acorda"
    assert "summarizer" not in ids, "sem trigger na caixa não acorda"
    print("TESTE 1 PASSOU")


def test_crash_contained_and_journal_complete():
    run = run_fleet(build_fleet_specs(), ticks=3)
    statuses = run.statuses
    assert statuses["summarizer"] in (ProcessStatus.FAILED, ProcessStatus.DONE), (
        "primeiro run falha; re-trigger no tick seguinte pode recuperar (RF3)"
    )
    # o crash NÃO derrubou a frota: os ticks seguintes rodaram
    journal = run.journal
    assert journal.of_agent("poster"), "poster rodou mesmo com crash alheio (RF3)"
    failed = [e for e in journal.all() if e.entry_type == JournalEntryType.FAILED]
    assert failed and "summarizer" in failed[0].agent_id
    # o journal é de ciclo de vida: nenhuma entrada carrega payload
    assert all(
        e.entry_type in set(JournalEntryType) for e in journal.all()
    ), "journal tipado em ciclo de vida (RF4)"
    print("TESTE 2 PASSOU")


def test_emission_boundary():
    def rogue_entry(ctx: AgentContext) -> AgentResult:
        return AgentResult(
            emitted=(OutboundEvent("voice_note.received", {"rogue": True}),),
        )

    kernel = AgentKernel()
    kernel.spawn(AgentSpec("rogue", rogue_entry, TickTrigger(1),
                           emits=()))              # não declara emitir nada
    kernel.tick(1)
    rejected = [e for e in kernel.journal.all()
                if e.entry_type == JournalEntryType.EMISSION_REJECTED]
    assert rejected, "emissão fora de emits é rejeitada e registrada (RF5)"
    assert kernel.process("rogue").status != ProcessStatus.FAILED, (
        "rejeição de emissão não mata o processo (RF5)"
    )
    print("TESTE 3 PASSOU")


def test_frontend_swap_is_invisible():
    run_a = run_fleet(build_fleet_specs(), ticks=3)
    dicts = [
        {"agent_id": "webhook-sim", "entry": "webhook_entry",
         "trigger": {"kind": "tick", "interval": 1},
         "emits": ["voice_note.received"]},
        {"agent_id": "transcriber", "entry": "transcriber_entry",
         "trigger": {"kind": "event", "event_type": "voice_note.received"},
         "emits": ["transcription.completed"]},
        {"agent_id": "summarizer", "entry": "summarizer_entry",
         "trigger": {"kind": "event", "event_type": "transcription.completed"},
         "emits": ["brief.drafted"]},
        {"agent_id": "poster", "entry": "poster_entry",
         "trigger": {"kind": "tick", "interval": 2}},
    ]
    entries = {
        "webhook_entry": webhook_entry, "transcriber_entry": transcriber_entry,
        "summarizer_entry": summarizer_entry, "poster_entry": poster_entry,
    }
    specs_b = specs_from_dicts(dicts, entries)
    run_b = run_fleet(specs_b, ticks=3)
    assert run_a.journal.lifeline_signature() == run_b.journal.lifeline_signature(), (
        "frontend trocou, comportamento idêntico (RF6)"
    )
    print("TESTE 4 PASSOU")


if __name__ == "__main__":
    print("=" * 60)
    print("EXERCÍCIO 21: AGENT KERNEL RUNTIME")
    print("=" * 60)
    # Descomente após implementar:
    # test_scheduler_determinism()
    # test_crash_contained_and_journal_complete()
    # test_emission_boundary()
    # test_frontend_swap_is_invisible()
    print("\nTODO: implemente specs, processos, scheduler, journal,")
    print("kernel e run_fleet")
```

---

## ✅ Validação: Critérios de Aceitação

Seu código será considerado **APROVADO** quando:

- [ ] O scheduler acorda exatamente quem deve (tick divisor + trigger na caixa não consumido), em ordem estável por agent_id (RF2)
- [ ] O crash do summarizer no primeiro run NÃO propaga: processo FAILED com causa no journal, poster e webhook seguem rodando nos ticks seguintes (RF3)
- [ ] Estado de processo é inacessível a outros processos — o contexto entrega apenas o estado do próprio agente e a inbox do trigger (RF3)
- [ ] O journal registra apenas SPAWNED/TICKED/DONE/FAILED/EMISSION_REJECTED com detalhe operacional — nenhuma entrada carrega payload de agente (RF4)
- [ ] Emissão fora de `emits` é rejeitada com entrada de journal e o processo sobrevive (RF5)
- [ ] Specs construídas de dicts (frontend alternativo) produzem `lifeline_signature()` idêntica às de dataclass — o kernel não sente a troca (RF6)
- [ ] O módulo do kernel não referencia nenhum agente concreto: agentes entram só via `AgentSpec` (RF1, RT4)

---

## 📊 Rubric de Avaliação

| Critério | Peso | Insuficiente (0-3) | Básico (4-6) | Proficiente (7-8) | Excelente (9-10) |
|---|---|---|---|---|---|
| **Specs + Scheduler (Parte 2)** | 25% | Não implementados | Acorda todos por tick | Tick + evento com consumo rastreado | Ordem estável e determinismo testáveis |
| **Isolamento (Parte 2-3)** | 25% | Não implementado | try/except solto | Crash contido + estado privado por processo | Contexto mínimo: agente não vê nem kernel nem vizinhos |
| **Journal (Parte 3)** | 20% | Não implementado | Log com payload de agente | Ciclo de vida tipado, sem conteúdo | Causa em FAILED e assinatura comportamental extraível |
| **Frota + troca de frontend (Parte 3)** | 30% | Não implementada | Frota sem crash | Crash contido na frota + fronteira de emissão | lifeline idêntica entre frontends — a inversão provada em código |

**Nota final:** Média ponderada. **Aprovação:** >= 7.0

---

## 💡 Dicas para Implementação

1. **O journal é a prova do "não sei o que o agente faz".** Se você pegar-se tentando logar o payload da transcrição para "facilitar o debug", você moveu a inteligência do agente para dentro do kernel. O conteúdo do agente vive no log causal do Exercício 20 (publicado pelo próprio agente); o journal do kernel só conta ciclo de vida — as duas memórias se complementam sem se duplicar.
2. **Isole o crash no tick, não no agente.** O `try/except` fica no loop de execução do `tick()`, envolvendo a chamada do entry — um lugar só. Exceção capturada vira `FAILED` + causa; o `for` segue para o próximo processo. Conter no entry de cada agente seria delegar isolamento à userland — exatamente o que um kernel não faz.
3. **A troca de frontend é o teste da tese.** Se `specs_from_dicts` precisou de um `if agent_id == "summarizer"`, o frontend não é trocável — o kernel aprendeu um agente. A resolução de entry POR NOME no mapping é o que mantém o kernel cego: dados entram, callback sai, agente nenhum é citado.

---

## ❓ Dúvidas Comuns

**P: Isso manda jogar o LangGraph fora?**
R: Manda inverter a direção da chamada. O padrão denuncia o agente vivendo DENTRO da abstração de terceiro (`...patterns.md:123`); o canonical do repo documenta a mesma inversão e registra que a implementação atual delega o loop ao LangGraph (`docs/canonical/owned-agent-control-loop.md:107`). Framework como BIBLIOTECA chamada pelo seu kernel é compatível com o padrão; framework como RECIPIENTE que chama seu código é o estado denunciado.

**P: Por que "kernel não sabe o que o agente faz" é requisito, e não omissão?**
R: Porque é o que permite a troca de frontend (RF6) e a evolução independente: agente de voz, agente de CRM, agente de review — o kernel agenda, isola e jorna todos sem alterar uma linha (`...patterns.md:129`). No dia em que o kernel entende payload de transcrição, existe acoplamento de domínio no runtime — e a migração da v2 do prólogo volta a doer.

**P: Isolamento de verdade não precisa de processo OS/container de verdade?**
R: Em produção, sim — o slot "Per-agent VM" do `model-agnostic-agent-vm-harness.md:45` é o vizinho de infra. Este exercício isola o que dá para isolar em stdlib: estado privado, crash contido, contexto mínimo. A mecânica de posse (quem vê o quê, quem sobrevive a quem) é a mesma; o borda de runtime é detalhe de implantação.

**P: Onde entram os Exercícios 18 e 20 aqui?**
R: 18 é a política de admissão de eventos (a caixa do kernel só aceita emissões declaradas — RF5 é a fronteira mínima); 20 é a memória de conteúdo (o journal registra ciclo de vida; o log causal registra o que os agentes publicaram). O kernel completo do fonte usa os três: scheduler + isolamento + journal, com fronteiras tipadas e log causal como infra (`...patterns.md:137`).

---

## 🚀 Próximo Passo

Depois de completar este exercício:

1. Leia o padrão 6 completo e sua classificação: `docs/analysis/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt-patterns.md:120-138` e `...classification.md:123-137` — o frame que amarra owned-loop, VM harness e alarm-clock num único modelo ensinável
2. Feche a série: Exercício 18 tipou as fronteiras → Exercício 19 endereçou o input exato → Exercício 20 deu memória causal ao sistema → este exercício montou o runtime que os três pressupõem — juntos, são a tese "agent frameworks considered harmful" reduzida a código
3. Escreva o ADO do KODA: qual das três responsabilidades está mais madura no repo hoje (schedule, isolamento, journal) e qual seria a primeira peça a unificar num runtime próprio?

---

*Exercício 21 | Nível 3 — Arquitetura Avançada | Agent Kernel Runtime*

**Frameworks just call code — nunca o contrário. O agente é processo do SEU sistema; o kernel agenda, isola e registra, sem saber o que ele faz.**
