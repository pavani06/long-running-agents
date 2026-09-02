---
title: "Exercício 20: Append-Only Causal Event Log — O Log É a Memória do Sistema"
type: exercise
level: 3
aliases: ["append-only causal event log", "log de eventos causal append-only", "causal event log", "caused_by event log", "cadeia causal de eventos", "log como memória do sistema", "reconstrução causal de falha"]
tags: ["curriculo-conteudo", "nivel-3", "agentes-orquestracao", "error-handling", "production", "arquitetura", "harness-engineering", "observability", "verification"]
relates-to: ["[[docs/analysis/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt-patterns|Padrões Agent Frameworks Considered Harmful]]", "[[docs/analysis/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt-classification|Classificação Agent Frameworks Considered Harmful]]", "[[docs/canonical/centralized-cross-framework-tracing|Centralized Cross-Framework Tracing]]", "[[docs/canonical/behavioral-eval-path-analysis|Behavioral Eval Path Analysis]]", "[[docs/canonical/asymmetric-failure-correction-router|Asymmetric Failure Correction Router]]", "[[curriculum/06-knowledge-graphs/detailed-graphs/generator-evaluator-graphs|Generator-Evaluator Graphs]]", "[[curriculum/05-core-concepts/07-multi-agent-coordination|Multi-Agent Coordination]]", "[[curriculum/03-nivel-3-advanced-architecture/exercises/exercise-18-typed-event-boundaries|Exercício 18: Typed Tool and Event Boundaries]]", "[[curriculum/03-nivel-3-advanced-architecture/exercises/exercise-21-agent-kernel-runtime|Exercício 21: Agent Kernel Runtime]]"]
duration: "90-120 min"
last_updated: 2026-09-02
---

# 📜 Exercício 20: Append-Only Causal Event Log — O Log É a Memória do Sistema
## Nível 3 — Arquitetura Avançada

**Tempo Estimado:** 90-120 minutos
**Dificuldade:** (Avançado)
**Pré-requisito:** Ter lido `03-file-based-coordination.md` (Nível 3) + `docs/canonical/centralized-cross-framework-tracing.md` + Exercício 18 (fronteiras tipadas)
**Objetivo:** Construir o destino único append-only para TODOS os agentes e processos, com ligações causais capturadas NO MOMENTO do evento (`caused_by`) — tornando qualquer falha navegável de volta ao gatilho pela cadeia causal, sem trabalho perdido e sem reconstrução posterior

---

## 📖 Prólogo: A Nota de Voz Que Sumiu Entre Dois Agentes

### Post-mortem do daily brief. Terceira tentativa.

```
ONCALL:      "o daily brief de hoje não foi postado. Na verdade, o
              problema começou ontem: uma nota de voz importante do
              cliente sumiu. Ela foi recebida — tenho o webhook — mas
              não chegou no brief."

ENG_A:       "do meu lado o transcriber rodou. Vejo o log dele: 14:02
              'transcription.completed'. Se ele rodou, a transcrição
              existe."

ENG_B:       "do meu lado o summarizer NÃO rodou pra essa nota. Meu log
              mostra que ele processou outra nota às 14:05 e pronto.
              Mas espera — o log do transcriber diz 'completed' com
              payload vazio? duration_seconds: null?"

ONCALL:      "então o que aconteceu com o áudio?"

ENG_A:       "não sei. O log do transcriber é um arquivo próprio, o do
              summarizer é outro, o do poster é um terceiro. Cada um
              com formato diferente, timestamp de timezone diferente,
              e NENHUM diz qual evento disparou qual. Para remontar a
              história eu teria que casar três logs na mão por timestamp
              — e timestamp não é causalidade: dois eventos no mesmo
              segundo não me dizem quem causou quem."

ONCALL:      "resumo: são 3-4 agentes e a gente já tem major debugging
              headaches. O trabalho da nota se perdeu ENTRE os passos,
              e o sistema não sabe contar a história."
```

**O custo dos logs por agente sem causa:**

```
╔══════════════════════════════════════════════════════════════════╗
║   TRÊS LOGS, ZERO HISTÓRIA — TRABALHO PERDIDO ENTRE OS PASSOS      ║
║                                                                  ║
║  O que o repo já tem          O que falta (a definição do         ║
║  ─────────────────────────    padrão, patterns.md:61-79)          ║
║  audit_log.jsonl append-only  ligações causais capturadas NO      ║
║  (curriculum, sem causa)      MOMENTO do evento (caused_by)       ║
║  trace store imutável com     UM destino único OBRIGATÓRIO para   ║
║  parent_span_id               todos os agentes e processos        ║
║  (span ≠ evento; hierarquia   cadeia navegável de qualquer FALHA  ║
║  de span ≠ causalidade de     de volta ao GATILHO                 ║
║  evento)                      "o log é a memória do sistema;      ║
║  pipeline tracer.ts →         nada é perdido, tudo é observado"   ║
║  telemetry.db (existente)     reconstrução POSTERIOR de causa     ║
║                               não é confiável (patterns.md:79)    ║
║                                                                  ║
║  classification.md:64: parent_span_id é hierarquia de span, não   ║
║  causalidade de evento — os dois mecanismos definidores faltam    ║
╚══════════════════════════════════════════════════════════════════╝
```

**O problema não é falta de log.** O repo ensina `audit_log.jsonl` append-only desde os
graph generators (`curriculum/06-knowledge-graphs/detailed-graphs/generator-evaluator-graphs.md:355`)
e opera tracing centralizado com schema unificado (`docs/canonical/centralized-cross-framework-tracing.md:28-55`).
O problema são os dois mecanismos que DEFINEM o padrão e não existem
(`...classification.md:64`): **causalidade capturada no publish** (`caused_by` de
evento para evento — não `parent_span_id`, que é hierarquia de execução) e o
**destino único obrigatório** para todos — cada agente com seu log próprio é o estado
que produz o post-mortem do prólogo.

**Sua missão:** implementar o `CausalEventLog` — a API de publish que exige
`caused_by` no momento do evento e é append-only por construção (sem update, sem
delete; correção se faz publicando um evento de correção), o `trace_back()` que navega
da falha ao gatilho pela cadeia, as queries de log único (`events_by`,
`events_of_type`), e a simulação do pipeline de nota de voz: a variante em que o
transcriber publicou SEM `caused_by` — e a cadeia quebra com gap declarado, porque
reconstrução posterior não é confiável (`...patterns.md:79`).

---

## 🧠 O Contexto

### O Modelo Mental: Publicar É Declarar Causa; Corrigir É Publicar

O padrão é a memória do sistema como invariante: "nothing is lost, everything is
observed" (`...patterns.md:70`). Quatro propriedades o definem:

1. **A causa nasce com o evento.** O `caused_by` aponta para o(s) event_id(s) que
   dispararam este — capturado no publish, nunca inferido depois
   (`...patterns.md:67`). Timestamp casado na mão é arqueologia; `caused_by` é
   testemunho no momento:

```
   webhook                 transcriber              summarizer
     │                        │                        │
     ▼ publish                ▼ publish                ▼ publish
   ┌─────────────────────────────────────────────────────────────┐
   │  CAUSAL EVENT LOG (destino único, append-only)               │
   │                                                             │
   │  e1 voice_note.received     caused_by: ()                   │
   │  e2 transcription.completed caused_by: (e1)                 │
   │  e3 brief.drafted           caused_by: (e2)                 │
   │  e4 slack.post_failed       caused_by: (e3)   ← A FALHA     │
   │                                                             │
   │  trace_back(e4) → [e4, e3, e2, e1]                          │
   │  a falha navega de volta ao gatilho em 4 saltos,             │
   │  sem casar timestamp, sem ler três arquivos                 │
   └─────────────────────────────────────────────────────────────┘
```

2. **Append-only por construção, não por convenção.** A API não tem update nem
   delete. Evento errado? Publica-se um evento de CORREÇÃO que referencia o errado —
   a história fica íntegra com o erro DENTRO dela. O `_log()` em modo `"a"` do
   Exercício 01 de N2 é append físico sem garantia de imutabilidade; aqui a
   imutabilidade é da interface (`curriculum/02-nivel-2-practical-patterns/exercises/solutions/exercise-01-solution.md:1748-1759`
   vs. o padrão).

3. **Um destino, todos os publicadores.** O valor depende de TODO evento ser
   publicado no log único (`...patterns.md:78`) — agente com log próprio é trabalho
   perdido esperando acontecer. A publicação é a única forma de estado sair de um
   processo.

4. **Gap é gap, não hipótese.** Quando um evento foi publicado sem `caused_by` (ou
   um publicador burlou o log), a cadeia QUEBRA naquele ponto — e o `trace_back()`
   reporta a quebra declarada, não uma reconstrução especulativa por timestamp
   (`...patterns.md:79`).

Os vizinhos do repo, e por que não fecham sozinhos: o tracing centralizado tem
`trace_id`/`span_id`/`parent_span_id` — hierarquia de SPAN, Agrupamento de execução
(`docs/canonical/centralized-cross-framework-tracing.md:28-55`); o
`behavioral-eval-path-analysis` preserva "causal ordering" como ORDEM de execução, não
evento→evento (`...md:34-45`); os learning logs imutáveis do
`asymmetric-failure-correction-router` são append-only mas declarados ausentes no repo
(`...md:98-103`). O NOT_FOUND resume: sem `caused_by`/`parent_event_id` em lugar
nenhum (`...classification.md:74`).

### O Que Você Vai Construir

1. `Event` — event_id, timestamp, publisher, event_type, payload e
   `caused_by: tuple[str, ...]` (a causa nasce com o evento)
2. `CausalEventLog` — destino único: `publish()` exige causalidade declarada
   (raiz publica com tupla vazia), recusa `caused_by` apontando para evento inexistente
   (`UnknownCauseError`); SEM update, SEM delete — append-only por construção
3. `trace_back(event_id)` — navega da falha ao gatilho pela cadeia de `caused_by`;
   encontra gap (evento sem causa declarada no meio do caminho) → retorna a cadeia
   parcial + `IncompleteChain` com o ponto da quebra
4. `correction_of` — o mecanismo de correção: publica um evento que REFERENCIA o
   errado; a história nunca reescreve
5. Queries de log único — `events_by(publisher)`, `events_of_type(type)`: um log,
   todas as perguntas
6. `run_pipeline()` — a simulação do post-mortem: o pipeline completo da nota de voz
   com a falha no poster, nas duas variantes — completa (cadeia navegável até o
   webhook) e com gap (transcriber burlou a causalidade; cadeia quebra com
   `IncompleteChain` declarado)

---

## 📋 Cenário

O pipeline de nota de voz do KODA: webhook recebe o áudio (`voice_note.received`,
raiz), transcriber processa (`transcription.completed`), summarizer monta o rascunho
(`brief.drafted`), poster publica no Slack (`slack.post_failed` — o áudio chega, a
falha é no token do poster). O post-mortem precisa responder em uma query: "o que
disparou a falha do poster?" — resposta: a cadeia até `voice_note.received`. Na
segunda variante, o transcriber foi atualizado às pressas e publica
`transcription.completed` SEM `caused_by` (log "opcional" no código novo): a mesma
query agora quebra no gap — e o relatório DIZ onde quebra, sem inventar o elo por
timestamp. No fim, a correção do payload errado do transcriber entra como evento de
correção que referencia o original.

---

## ✅ Requisitos

### Requisitos Funcionais

1. **RF1 — Causalidade no publish:** `publish()` recebe `caused_by` junto com o
   evento; causa apontando para event_id inexistente explode
   (`UnknownCauseError`); só a raiz da cadeia publica com tupla vazia — e raiz sem
   causa prévia é a ÚNICA tupla vazia aceita.
2. **RF2 — Append-only por construção:** a classe não expõe update nem delete de
   evento; `events` cresce monotonicamente e `seq` nunca reusa número; corrigir é
   publicar `Event` com `correction_of=event_id_errado` — o errado permanece.
3. **RF3 — trace_back navegável:** `trace_back(failure_id)` retorna a cadeia
   ordenada [falha, ..., gatilho] seguindo `caused_by`; no cenário completo, a
   cadeia do `slack.post_failed` termina em `voice_note.received`.
4. **RF4 — Gap é declarado, não especulado:** cadeia contendo evento de publicador
   que burlou a causa (publicado com `caused_by=()` fora da raiz) produz
   `IncompleteChain` com o event_id da quebra; o trace NÃO casa por timestamp para
   "adivinhar" o elo faltante.
5. **RF5 — Um log, todas as perguntas:** `events_by(publisher)` e
   `events_of_type(event_type)` respondem sobre o log único; nenhum publicador tem
   log próprio no design.
6. **RF6 — Correção dentro da história:** o evento de correção referencia o
   original; `latest_version(event_type, key)` retorna a correção quando existe —
   sem reescrever o passado.

### Requisitos Técnicos

1. **RT1 — Python 3.9+, stdlib apenas**, type hints obrigatórios
2. **RT2 — `dataclasses` congelados** para `Event` e `IncompleteChain`; o log é a
   única estrutura mutável, e só via `publish()`
3. **RT3 — `trace_back`/queries como funções puras** do estado do log; I/O nenhum
4. **RT4 — Determinismo:** ids sequenciais (`e-000001...`), timestamps fornecidos
   pelo caller (relógio injetado), ordem estável em todas as queries

---

## 🏗️ Arquitetura do Sistema

```
┌────────────────────────────────────────────────────────────────────────┐
│                   APPEND-ONLY CAUSAL EVENT LOG                         │
│                                                                        │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │ PUBLISHERS (todos — webhook, transcriber, summarizer, poster)   │    │
│  │ cada um declara a causa NO MOMENTO do evento (RF1)              │    │
│  └──────────────────────────┬─────────────────────────────────────┘    │
│                             ▼ publish(caused_by=(...))                  │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │ CAUSAL EVENT LOG — destino único, append-only (RF2, RF5)        │    │
│  │ • sem update, sem delete — correção PUBLICA correction_of (RF6) │    │
│  │ • UnknownCauseError em causa fantasma                           │    │
│  │ • "o log é a memória do sistema" (patterns.md:70)               │    │
│  └──────────────────────────┬─────────────────────────────────────┘    │
│                             ▼                                          │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │ QUERIES CAUSAIS (RF3, RF4)                                      │    │
│  │ trace_back(falha) → cadeia até o gatilho                        │    │
│  │   gap no meio → IncompleteChain(quebra declarada) (RF4)          │    │
│  │ events_by(publisher) / events_of_type(type) — log único (RF5)   │    │
│  └────────────────────────────────────────────────────────────────┘    │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 🎯 Sua Tarefa em 3 Partes

### Parte 1 — Diagnosticar o post-mortem (15 min)

Com o prólogo: por que casar os três logs por timestamp não reconstrói a causa? O que
o `parent_span_id` do tracing centralizado do repo agrupa que o `caused_by` deste
padrão conecta — e por que são mecanismos diferentes? Responda como comentário.

### Parte 2 — O log e a causalidade no publish (40 min)

Implemente `Event`, `CausalEventLog.publish()` com validação de causa (RF1-RF2),
a correção por `correction_of` (RF6) e as queries de log único (RF5).

### Parte 3 — trace_back e a simulação com gap (45 min)

Implemente `trace_back()` com `IncompleteChain` (RF3-RF4) e `run_pipeline()` nas duas
variantes do cenário. Verifique: cadeia completa navega da falha ao webhook; variante
com gap quebra declarada no evento do transcriber.

---

## 💻 Starter Code

```python
"""
Exercício 20 — Append-Only Causal Event Log
Nível 3 — Arquitetura Avançada

Destino único append-only para todos os agentes e processos, com
causalidade capturada no publish (caused_by). O log é a memória do
sistema: nada se perde, tudo é observado, e qualquer falha navega
de volta ao gatilho pela cadeia causal.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping, Optional, Sequence, Tuple


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass(frozen=True)
class Event:
    """Um evento publicado — a causa nasce com ele (RF1)."""
    event_id: str
    seq: int                      # monotônico, nunca reusado (RF2)
    ts: float                     # relógio injetado pelo caller (RT4)
    publisher: str                # quem publicou
    event_type: str               # ex.: "transcription.completed"
    payload: Mapping[str, object]
    caused_by: Tuple[str, ...] = ()          # event_ids que o dispararam
    correction_of: Optional[str] = None      # RF6: corrige SEM reescrever


class UnknownCauseError(Exception):
    """caused_by aponta para evento que não existe (RF1)."""


@dataclass(frozen=True)
class IncompleteChain:
    """A quebra declarada da cadeia (RF4) — gap é gap, não hipótese."""
    chain: Tuple[Event, ...]      # o que dá para navegar honestamente
    broke_at: str                 # event_id onde a causa não foi declarada
    reason: str


@dataclass(frozen=True)
class TraceResult:
    """trace_back: cadeia completa OU cadeia parcial + quebra."""
    chain: Tuple[Event, ...]
    incomplete: Optional[IncompleteChain] = None   # None = cadeia íntegra

    @property
    def reached_root(self) -> bool:
        """True quando navegou até um evento raiz (caused_by vazio)."""
        # TODO: implemente
        raise NotImplementedError


# ============================================================================
# O LOG — destino único, append-only
# ============================================================================

class CausalEventLog:
    """
    A memória do sistema (RF2, RF5):
      - publish() é a ÚNICA forma de estado entrar
      - sem update, sem delete — correção publica correction_of (RF6)
      - todos os publicadores, um destino
    """

    def __init__(self) -> None:
        self._events: list[Event] = []
        self._by_id: dict[str, Event] = {}
        self._seq: int = 0

    # -- publicação ----------------------------------------------------------

    def publish(
        self,
        ts: float,
        publisher: str,
        event_type: str,
        payload: Mapping[str, object],
        caused_by: Tuple[str, ...] = (),
        correction_of: Optional[str] = None,
    ) -> Event:
        """
        Valida (RF1):
          - cada id em caused_by existe (senão UnknownCauseError)
          - caused_by vazio só na raiz: se o publisher JÁ publicou algo
            causado antes, tupla vazia é gap declarado — aceite o evento
            (o gap aparece no trace_back como IncompleteChain, RF4).
        Constrói id "e-{seq:06d}", seq monotônico, e anexa (RF2).
        """
        # TODO: implemente
        raise NotImplementedError

    # -- consultas (funções puras do estado) ----------------------------------

    def event(self, event_id: str) -> Optional[Event]:
        # TODO: implemente
        raise NotImplementedError

    def events(self) -> Tuple[Event, ...]:
        """Fotografia ordenada do log (imutável para o caller)."""
        # TODO: implemente
        raise NotImplementedError

    def events_by(self, publisher: str) -> Tuple[Event, ...]:
        """Um log, todas as perguntas (RF5)."""
        # TODO: implemente
        raise NotImplementedError

    def events_of_type(self, event_type: str) -> Tuple[Event, ...]:
        # TODO: implemente
        raise NotImplementedError

    def latest_version(self, event: Event) -> Event:
        """A correção mais recente que referencia `event` (RF6), ou ele
        mesmo se ninguém corrigiu. correction_of é cade: correção de
        correção conta."""
        # TODO: implemente
        raise NotImplementedError

    # -- navegação causal ------------------------------------------------------

    def trace_back(self, failure_id: str) -> TraceResult:
        """
        Navega caused_by da falha ao gatilho (RF3).
        Gap (evento não-raiz com caused_by vazio no caminho) →
        TraceResult com IncompleteChain declarando a quebra (RF4).
        Nunca case por timestamp: reconstrução posterior não é
        confiável (patterns.md:79).
        """
        # TODO: implemente
        raise NotImplementedError


# ============================================================================
# PARTE 3 — SIMULAÇÃO: o post-mortem da nota de voz
# ============================================================================

@dataclass(frozen=True)
class PipelineReport:
    label: str
    failure: Event
    trace: TraceResult
    root_reached: bool


def run_pipeline(log: CausalEventLog, transcriber_declares_cause: bool) -> PipelineReport:
    """
    O pipeline do cenário, determinístico (RT4):
      t=1.0  webhook     voice_note.received      caused_by: ()          [raiz]
      t=2.0  transcriber transcription.completed caused_by: (e-000001)
             — na variante SEM causa: caused_by=() (o update apressado)
      t=3.0  summarizer  brief.drafted            caused_by: (transcrição)
      t=4.0  poster      slack.post_failed        caused_by: (brief)
    Depois: trace_back da falha (slack.post_failed) e o veredicto —
    root_reached=True na variante completa; False + IncompleteChain na
    variante com gap (quebrada no evento do transcriber).
    """
    # TODO: implemente
    raise NotImplementedError


def publish_correction(log: CausalEventLog, wrong: Event) -> Event:
    """
    O payload do transcriber saiu vazio (duration_seconds: null).
    Publique transcription.completed CORRIGIDO referenciando o original
    (correction_of) — a história nunca reescreve (RF6).
    """
    # TODO: implemente
    raise NotImplementedError


# ============================================================================
# FIXTURES
# ============================================================================

def build_complete_log() -> CausalEventLog:
    log = CausalEventLog()
    run_pipeline(log, transcriber_declares_cause=True)
    return log


def build_gapped_log() -> CausalEventLog:
    log = CausalEventLog()
    run_pipeline(log, transcriber_declares_cause=False)
    return log


# ============================================================================
# TESTS
# ============================================================================

def test_publish_validates_cause():
    log = CausalEventLog()
    root = log.publish(1.0, "webhook", "voice_note.received", {"note_id": "n-42"})
    assert root.caused_by == ()
    try:
        log.publish(2.0, "webhook", "voice_note.received",
                    {"note_id": "n-43"}, caused_by=("e-999999",))
        raise AssertionError("causa fantasma deve explodir (RF1)")
    except UnknownCauseError:
        pass
    ids = [e.event_id for e in log.events()]
    assert len(set(ids)) == len(ids), "ids únicos, seq monotônico (RF2)"
    print("TESTE 1 PASSOU")


def test_trace_back_complete():
    log = build_complete_log()
    failure = log.events_of_type("slack.post_failed")[0]
    result = log.trace_back(failure.event_id)
    assert result.reached_root, "cadeia íntegra chega à raiz (RF3)"
    assert result.incomplete is None
    types = [e.event_type for e in result.chain]
    assert types == ["slack.post_failed", "brief.drafted",
                     "transcription.completed", "voice_note.received"]
    print("TESTE 2 PASSOU")


def test_gap_is_declared_not_speculated():
    log = build_gapped_log()
    failure = log.events_of_type("slack.post_failed")[0]
    result = log.trace_back(failure.event_id)
    assert not result.reached_root, "gap interrompe a navegação (RF4)"
    assert result.incomplete is not None
    broke = result.incomplete.broke_at
    broke_event = log.event(broke)
    assert broke_event is not None
    assert broke_event.publisher == "transcriber", (
        "a quebra é nomeada no evento sem causa declarada"
    )
    assert broke_event.caused_by == ()
    print("TESTE 3 PASSOU")


def test_single_log_and_correction():
    log = build_complete_log()
    # RF5: um log responde por publicador e por tipo
    assert len(log.events_by("webhook")) == 1
    assert len(log.events_of_type("transcription.completed")) == 1
    all_types = {e.event_type for e in log.events()}
    assert {"voice_note.received", "transcription.completed",
            "brief.drafted", "slack.post_failed"} <= all_types

    # RF6: correção publica, não reescreve
    wrong = log.events_of_type("transcription.completed")[0]
    before = len(log.events())
    corrected = publish_correction(log, wrong)
    assert len(log.events()) == before + 1, "correção anexa (RF2)"
    assert corrected.correction_of == wrong.event_id
    assert log.event(wrong.event_id) is not None, "o original permanece"
    assert log.latest_version(wrong).event_id == corrected.event_id
    print("TESTE 4 PASSOU")


if __name__ == "__main__":
    print("=" * 60)
    print("EXERCÍCIO 20: APPEND-ONLY CAUSAL EVENT LOG")
    print("=" * 60)
    # Descomente após implementar:
    # test_publish_validates_cause()
    # test_trace_back_complete()
    # test_gap_is_declared_not_speculated()
    # test_single_log_and_correction()
    print("\nTODO: implemente Event, log com causalidade no publish,")
    print("trace_back com gap declarado, correção e run_pipeline")
```

---

## ✅ Validação: Critérios de Aceitação

Seu código será considerado **APROVADO** quando:

- [ ] `publish()` valida cada causa (`UnknownCauseError` para fantasma), ids são únicos e seq monotônico; raiz publica com tupla vazia (RF1-RF2)
- [ ] `trace_back(slack.post_failed)` na variante completa retorna exatamente a cadeia de 4 eventos até `voice_note.received` com `reached_root=True` (RF3)
- [ ] Na variante com gap, o trace quebra COM `IncompleteChain` nomeando o evento do transcriber e sua causa vazia — nenhum casamento por timestamp (RF4)
- [ ] `events_by`/`events_of_type` respondem sobre o log único; nenhum publicador tem estrutura própria (RF5)
- [ ] Correção anexa novo evento com `correction_of`, o original permanece e `latest_version` resolve a correção (RF6)
- [ ] O log não expõe update nem delete — append-only por construção, não por convenção (RF2)

---

## 📊 Rubric de Avaliação

| Critério | Peso | Insuficiente (0-3) | Básico (4-6) | Proficiente (7-8) | Excelente (9-10) |
|---|---|---|---|---|---|
| **Publish causal (Parte 2)** | 25% | Não implementado | Anexa sem validar causa | Causa validada + raiz vs. gap tipados | Gap aceito no publish com semântica definida para o trace |
| **Append-only + correção (Parte 2)** | 20% | Mutação exposta | Append sem correção | Sem update/delete + correction_of encadeado | latest_version resolve cadeia de correções |
| **trace_back (Parte 3)** | 30% | Não implementado | Um salto só | Cadeia completa até a raiz | IncompleteChain nomeia a quebra — gap é gap |
| **Simulação com gap (Parte 3)** | 25% | Não implementada | Só a variante completa | Duas variantes divergentes | A lição visível: sem disciplina de publish, a memória do sistema fura — e o sistema CONFESSA |

**Nota final:** Média ponderada. **Aprovação:** >= 7.0

---

## 💡 Dicas para Implementação

1. **Valide a causa antes de anexar, não depois.** O `UnknownCauseError` no publish é a mesma postura do Exercício 18: barrar na fronteira, antes do efeito. Um evento anexado com causa fantasma corromperia a memória — e nesta arquitetura a memória É o sistema.
2. **Distinga raiz de gap no trace, não no publish.** O publish aceita tupla vazia (ele não sabe se é raiz legítima ou burlação); quem revela a diferença é o `trace_back`: cadeia que encontra `caused_by=()` no MEIO do caminho quebra ali. Isso preserva o append (o log não recusa o mundo real) sem mentir sobre a história.
3. **Resista ao casamento por timestamp.** Quando o trace quebrar, vai dar vontade de procurar "o evento mais próximo de t-0.5 do mesmo publisher" para fechar o elo. Releia `patterns.md:79`: causalidade capturada depois não é confiável. O `IncompleteChain` honesto vale mais que a cadeia inventada — é ele que aciona o fix no publicador relapso.

---

## ❓ Dúvidas Comuns

**P: Isso não é o tracing centralizado do repo?**
R: É o vizinho que falta fechar. O tracing unifica `trace_id`/`span_id`/`parent_span_id` — hierarquia de EXECUÇÃO, agrupando operações sob uma chamada (`docs/canonical/centralized-cross-framework-tracing.md:28-55`). O `caused_by` conecta EVENTO a EVENTO através de processos: a transcrição completar CAUSOU o rascunho do brief. Span responde "o que rodou junto"; causa responde "o que disparou o quê" (`...classification.md:64`).

**P: Por que a variante com gap é parte do exercício, e não um caso de erro?**
R: Porque a limitação declarada do padrão é que "o valor do log depende de todo evento ser publicado" com causa (`...patterns.md:78`) — e sistema real tem publicador relapso. O design honesto não impede o gap (o log não pode recusar o mundo); ele torna o gap VISÍVEL na primeira query. A dor do gap é o que gera a disciplina de publish.

**P: E o volume? Append-only cresce para sempre.**
R: É a limitação assumida (`...patterns.md:77`): storage cresce sem remoção — o preço de "nada é perdido". Mitigações (snapshot + log compactado) existem no mundo de event sourcing, mas removem eventos do caminho de consulta; o padrão as trata como operação posterior, não como parte da mecânica causal.

**P: A correção por evento novo não polui o log?**
R: Ela o mantém honesto: o erro e a correção ficam na história, cada um com causa — auditoria é justamente poder contar essa história (`...patterns.md:70`). Reescrever o evento apagaria a evidência de QUE o erro existiu e QUANDO foi corrigido, as duas coisas que um post-mortem precisa.

---

## 🚀 Próximo Passo

Depois de completar este exercício:

1. Leia o padrão 3 completo e sua classificação: `docs/analysis/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt-patterns.md:61-79` e `...classification.md:60-76` — o delta incremental sobre `telemetry.db` e `audit_log.jsonl` que o repo já opera
2. Siga a série: Exercício 18 tipou o que atravessa as fronteiras → este exercício dá ao que atravessou uma memória causal única → Exercício 21 monta o kernel cujo journal É esse log
3. Escreva o ADO do KODA: qual incidente dos últimos 30 dias precisaria de `trace_back` — e qual publicador do pipeline atual burlaria a causalidade no primeiro dia?

---

*Exercício 20 | Nível 3 — Arquitetura Avançada | Append-Only Causal Event Log*

**Timestamp não é causalidade. A causa nasce com o evento — ou a cadeia quebra, e quebra declarada.**
