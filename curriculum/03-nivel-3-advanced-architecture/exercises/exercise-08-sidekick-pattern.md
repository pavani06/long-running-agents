---
title: "Exercício 8: Sidekick — o Agente que Guia Quem Faz"
type: curriculum-exercise
nivel: 3
aliases: ["sidekick pattern", "ratatouille pattern", "padrão sidekick", "agente que guia quem faz", "fronteira física", "telemetria de trabalho físico", "el mike"]
tags: ["curriculo-conteudo", "nivel-3", "agentes-orquestracao", "governanca", "telemetry", "agent-loop", "evals", "mhc-backend", "stack-tooling"]
relates-to: ["[[docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-analysis|Kavak Playbook Analysis]]", "[[docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-classification|Kavak Playbook Classification]]", "[[docs/canonical/sidekick-pattern-physical-boundaries|Sidekick Pattern at Physical Boundaries]]", "[[docs/canonical/model-agnostic-agent-vm-harness|Model-Agnostic Agent-VM Harness]]", "[[docs/canonical/presence-in-the-loop-metric|Presence-in-the-Loop Metric]]", "[[curriculum/03-nivel-3-advanced-architecture/exercises/exercise-07-mega-expert-consolidation|Exercício 7: Mega-Expert Consolidation]]", "[[curriculum/05-core-concepts/07-multi-agent-coordination|Multi-Agent Coordination]]"]
last_updated: 2026-08-30
---

# 🔧 Exercício 8: Sidekick — o Agente que Guia Quem Faz
## Nível 3 — Arquitetura Avançada

**Tempo Estimado:** 90-120 minutos
**Dificuldade:** ⭐⭐⭐⭐ (Avançado)
**Pré-requisito:** Ter lido a Pattern 13 em `05-core-concepts/07-multi-agent-coordination.md` + Exercício 7 (`exercise-07-mega-expert-consolidation.md`)
**Objetivo:** Construir o loop completo do sidekick em fronteiras físicas: diagnosticar o open-loop (agente abre chamado e esquece — nenhum dado de melhoria volta), implementar a sessão sidekick (agente guia passo a passo, humano executa com destreza/sentidos, confirmações e notas de voz retornam como telemetria) e fechar o loop (anomalias recorrentes viram casos de regressão no corpus de evals, métricas de negócio — custo de garantia e CSAT — batem as metas)

---

## 📖 Prólogo: O Chamado #4471 Que Ninguém Leu de Volta

**Terça-feira, 7h40. Ruth, mecânica há 14 anos, recebe o primeiro carro do turno no Centro de Inspeção. O sistema "inteligente" da oficina manda mensagem:**

```
SAC-BOT:    "Não consigo executar inspeção física. Abrindo chamado
             #4471 para a fila de manutenção."
             [CHAMADO ABERTO ▶ e esquecido]

Ruth:       (para si mesma) "Chamado pra quê? Tô com o carro aqui
             na minha bancada. Vou fazer do meu jeito, como sempre."

             [Ruth inspeciona do próprio jeito: 22 minutos,
              sem checklist, sem registro estruturado]

SAC-BOT:    "Chamado #4471 aguardando atendimento humano.
             Prazo SLA: 48h."
             [o carro já saiu há 44 horas]
```

**Na sexta, a mesa do gerente recebe o relatório do trimestre:**

```
╔══════════════════════════════════════════════════════════════════╗
║           O TRABALHO FÍSICO QUE O SOFTWARE ESQUECEU              ║
║                                                                  ║
║  Chamados abertos pela fila de manutenção:     412               ║
║  Chamados com retorno/feedback ao sistema:       0               ║
║  Notas de voz dos mecânicos aproveitadas:        0               ║
║  Casos de eval gerados a partir da oficina:      0               ║
║                                                                  ║
║  Custos:                                                        ║
║    Garantia (defeitos que a inspeção deveria pegar): +8% tri     ║
║    Retrabalho de inspeções:                     23%              ║
║    Tempo médio de inspeção:                     38 min           ║
║    CSAT pós-revisão:                            3.9 / 5.0        ║
║                                                                  ║
║  Os 140 mecânicos trabalham IGUAL há 5 anos. Nenhum             ║
║  aprendizado do pátio voltou pra o sistema. O agente             ║
║  não sabe o que acontece depois de "abrir chamado".             ║
╚══════════════════════════════════════════════════════════════════╝
```

Na retrospectiva de segunda-feira:

```
Head de Ops: "O custo de garantia subindo de novo. A inspeção é
              feita por gente experiente, não entendo."

Arquiteta:   "Exatamente. Gente experiente — 140 mecânicos com
              destreza e sentidos que nenhum agente tem. O
              problema não é a falta de software na oficina.
              É a DIREÇÃO do software que existe: ele abre um
              chamado pra fila humana e esquece. Open-loop.
              Nada do que Ruth vê com os olhos dela volta pra
              o sistema. O aprendizado morre no pátio.

              A inversão é o padrão sidekick — o 'Ratatouille':
              o agente VAI JUNTO. No MESMO harness da frota, ele
              guia Ruth passo a passo: procedimento de inspeção,
              tolerâncias, dicas. Ruth executa — as mãos e os
              ouvidos são dela. E cada confirmação e nota de voz
              volta como telemetria: alimenta o estado do agente
              daquele carro e, quando algo estranho acontece,
              vira caso de eval pra frota inteira.

              Regra de escopo: humano-no-loop SÓ onde presença
              física é exigida — tipo entregar a chave. Na Kavak
              são 96% das interações e 95% das transações
              totalmente agent-handled; o resto é fronteira
              física, não fallback generalizado.

              E o resultado é de negócio: qualidade de inspeção
              sobe, custo de garantia cai ~20-26%, CSAT sobe."

Ruth:        "Então o agente vai me dizer como fazer meu trabalho?"

Arquiteta:   "O agente traz o procedimento documentado — o
              checklist com as tolerâncias que hoje vive na
              cabeça de cada um — e as dicas dos melhores. Você
              confirma o passo crítico com uma nota de voz. Se
              você ouvir um ruído que o procedimento não previa,
              ISSO vira caso de teste. Você deixa de ser a
              exceção silenciosa do sistema e vira a fronteira
              sensorial dele."
```

**Sua missão:** implementar o loop completo — diagnóstico do open-loop, sessão sidekick com confirmação de passos críticos, e o fechamento com anomalias virando casos de regressão e métricas de garantia/CSAT batendo as metas. Este padrão foi classificado como `Missing` (nenhuma cobertura em docs, código, skills ou currículo antes do canonical) em `docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-classification.yaml:217-229` — este exercício é a primeira implementação curricular.

---

## 🧠 O Contexto

### O Modelo Mental: Excluir × Esquecer × Guiar

O padrão vem da Kavak: o mesmo harness de escalação da frota, com o agente indo junto guiando um mecânico humano (procedimento de inspeção, dicas), usado onde destreza/sentidos são insubstituíveis (~800 mecânicos). Resultado: qualidade de inspeção sobe, consertos mais rápidos/baratos, custo de garantia cai ~20-26%, CSAT sobe (`docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-analysis.md:98-100`). O nome interno é "Ratatouille" / El Mike.

Três arquiteturas competem pela fronteira física:

| Arquitetura | Como funciona | Por que falha |
|---|---|---|
| **Excluir agentes do físico** | Software não participa da inspeção/reparo; oficina é caixa-preta | Qualidade, custo e garantia ficam sem inteligência de software; conhecimento tribal nunca compound |
| **Open-loop (chamado esquecido)** | Agente não consegue executar → abre chamado pra fila humana e esquece | O sinal de aprendizado morre na entrega: "nenhum dado de melhoria → sistema empaca" (`...analysis.md:164`) |
| **Sidekick (o padrão)** | Mesmo harness da frota, agente guia o humano passo a passo; execuções voltam como telemetria | É a única que fecha o loop: o físico herda a inteligência da frota e alimenta os evals dela |

A aposta estrutural é a mesma inversão do Exercício 7 e do help API: **humanos servem agentes** — "the help API, the three-role topology, the sidekick/Ratatouille pattern, and skill-building humans all reverse the default direction of service" (`...analysis.md:176`).

### Fronteiras do padrão (o que NÃO é sidekick)

1. **Sidekick ≠ humano-no-loop generalizado.** O escopo é exclusivamente a fronteira física genuína: "96% das interações e 95% das transações totalmente agent-handled; humanos permanecem só onde presença física é exigida (tipo entregar a chave do carro)" (`...analysis.md:105-106`). Humano-como-fallback-decisório é outro padrão.

2. **Sidekick ≠ escalonamento de julgamento.** Quando o humano entra para DECIDIR/revisar a saída de um agente, a direção é inversa (humano intervém em tarefa do agente) — isso é o território do `docs/canonical/presence-in-the-loop-metric.md` e do Exercício 6. No sidekick, o agente guia a execução física do humano.

3. **Sidekick ≠ automação física total.** Sem humano presente não existe canal de telemetria nem quem execute: o gap sensor/atuador é real ("o agente vê só o que a telemetria humana retorna", canonical). Tentar automatizar tudo é a fantasia anti-padrão.

4. **Procedimento não se inventa em runtime.** Os passos vêm do procedimento documentado (manual de inspeção, guia de reparo) com instrução, tolerância e resultado esperado. Orientação inventada pelo agente na hora é alucinação, não procedimento.

### O Que Você Vai Construir

1. **`OpenLoopAnalyzer`** (Parte 1 — Diagnóstico): lê o log de um turno e quantifica o open-loop (chamados abertos, trabalho sem agente, notas de voz retornadas, casos de eval gerados)
2. **`SidekickSession`** (Parte 2 — Implementação): o loop guiar → executar → registrar com `GuidanceStep` (procedimento com tolerâncias/dicas) e `TelemetryEvent` (confirmações e notas de voz voltando), com passos críticos exigindo confirmação humana
3. **`SidekickPipeline`** (Parte 3 — Fechamento do loop): anomalias recorrentes viram `RegressionCase` no corpus de evals; `OutcomeMetrics` (custo de garantia, CSAT) batem as metas e sustentam o veredito da frota

O domínio de exemplo é o Centro de Inspeção do prólogo: procedimento de inspeção de 6 passos (`INSP-COMPACT-2026`), a mecânica Ruth (`MEC-142`), e uma anomalia real (ruído no freio traseiro) que aparece 2 vezes na frota — o caso de teste que o sistema antigo nunca capturou.

---

## ✅ Requisitos

### Funcionais

- [ ] `OpenLoopAnalyzer.diagnose()` produz um `LoopDiagnosis` com: total de entradas, chamados abertos, trabalho executado sem agente, notas de voz retornadas e casos de eval gerados
- [ ] `is_open_loop()` retorna `True` quando houve atividade (chamados OU trabalho sem agente) E nenhum caso de eval foi gerado — o sinal de aprendizado morreu
- [ ] `SidekickSession.guide_next()` retorna o próximo passo não confirmado do procedimento, em ordem (`None` quando completo)
- [ ] `SidekickSession.record()` registra um `TelemetryEvent` e rejeita (raise `ValueError`) telemetria de passo inexistente no procedimento
- [ ] `critical_confirmed()` retorna `True` somente quando TODO passo `requires_confirmation` tem confirmação na telemetria
- [ ] `progress()` retorna a fração de passos confirmados (0.0-1.0)
- [ ] `SidekickPipeline.close_loop()` produz um `ShiftReport` onde anomalias com contagem frota >= `MIN_ANOMALY_OCCURRENCES` viram `RegressionCase` com a nota de voz como `anomaly_note`
- [ ] `OutcomeMetrics.meets_targets()` exige: qualidade >= 0.90, `warranty_cost_delta <= -WARRANTY_REDUCTION_TARGET` (meta -20%, como no caso Kavak), CSAT >= 0.80, retrabalho <= 0.10
- [ ] `SidekickPipeline.fleet_verdict()` aprova a frota somente quando TODOS os reports têm métricas anexadas E todas batem as metas

### Técnicos

- [ ] Python 3.9+ com type hints
- [ ] `dataclasses` para todos os modelos de dados (`GuidanceStep`, `TelemetryEvent`, `ShiftEntry`, `ShiftLog`, `LoopDiagnosis`, `SidekickSession`, `RegressionCase`, `OutcomeMetrics`, `ShiftReport`)
- [ ] `guide_next()`, `critical_confirmed()` e `progress()` são determinísticos e derivados apenas do estado (procedimento + telemetria)
- [ ] `GuidanceStep` é imutável (`frozen=True`) — procedimento não muda durante a sessão
- [ ] Thresholds (`MIN_ANOMALY_OCCURRENCES`, `WARRANTY_REDUCTION_TARGET`) são constantes nomeadas no módulo

### Validação

- [ ] Cenário 1: Turno open-loop (3 chamados, 4 trabalhos sem agente, 0 notas, 0 evals) → `is_open_loop == True`
- [ ] Cenário 2: Turno sidekick (6 notas de voz, 1 caso de eval, 0 chamados) → `is_open_loop == False`
- [ ] Cenário 3: `guide_next()` percorre o procedimento em ordem; após todas as confirmações, `progress() == 1.0` e `critical_confirmed() == True`
- [ ] Cenário 4: `record()` com `step_id` inexistente levanta `ValueError`; passo crítico sem confirmação mantém `critical_confirmed() == False`
- [ ] Cenário 5: Anomalia no S05 com contagem frota 2 >= `MIN_ANOMALY_OCCURRENCES` vira `RegressionCase` com a nota de voz
- [ ] Cenário 6: Métricas (qualidade 0.93, garantia -0.24, CSAT 0.88, retrabalho 0.06) batem as metas; frota com todos os reports aprovados → `fleet_verdict() == True`

---

## 🏗️ Arquitetura do Sistema

### Diagrama ASCII

```
┌──────────────────────────────────────────────────────────────────┐
│                SIDEKICK PATTERN — PIPELINE COMPLETO              │
│                                                                   │
│  PARTE 1 — DIAGNÓSTICO DO OPEN-LOOP                               │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │                OPEN-LOOP ANALYZER                        │     │
│  │                                                            │     │
│  │  Log do turno (ANTES):                                    │     │
│  │  ┌──────────────────────────────────────────────────────┐ │     │
│  │  │ ticket_opened ×3 → work_done ×4 → (nada volta)       │ │     │
│  │  │   ▲ 0 notas de voz   ▲ 0 casos de eval               │ │     │
│  │  └──────────────────────────────────────────────────────┘ │     │
│  │  → LoopDiagnosis { is_open_loop: True }                   │     │
│  └───────────────────────────┬────────────────────────────────┘     │
│                              ▼                                      │
│  PARTE 2 — SESSÃO SIDEKICK (mesmo harness da frota)                │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │   SIDEKICK (guia)            RUTH / MEC-142 (executa)   │     │
│  │  ┌──────────────┐   guia    ┌──────────────┐            │     │
│  │  │ GuidanceStep │──────────▶│ destreza +   │            │     │
│  │  │ instrução +  │  voz/tela │ sentidos     │            │     │
│  │  │ tip/tolerância│          └──────┬───────┘            │     │
│  │  └──────────────┘                  │ telemetria          │     │
│  │       ▲                            ▼                     │     │
│  │  ┌──────────────────────────────────────────┐           │     │
│  │  │ TelemetryEvent: step, confirmed,          │           │     │
│  │  │ voice_note, anomaly                       │           │     │
│  │  │ ✔ passo crítico exige confirmação         │           │     │
│  │  │ ✔ passo inexistente → ValueError          │           │     │
│  │  └──────────────────────────────────────────┘           │     │
│  └───────────────────────────┬────────────────────────────────┘     │
│                              ▼                                      │
│  PARTE 3 — FECHAMENTO DO LOOP                                      │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │  telemetria ─▶ anomalias recorrentes (>= 2× na frota)    │     │
│  │                     │                                     │     │
│  │                     ▼                                     │     │
│  │             RegressionCase (corpus de evals)              │     │
│  │                                                            │     │
│  │  OutcomeMetrics:                                          │     │
│  │    qualidade 0.93 ✔   garantia -0.24 (meta -0.20) ✔      │     │
│  │    CSAT 0.88 ✔       retrabalho 0.06 ✔                  │     │
│  │                                                            │     │
│  │  fleet_verdict: TODOS os reports com metas → ✅          │     │
│  └──────────────────────────────────────────────────────────┘     │
└──────────────────────────────────────────────────────────────────┘
```

---

## 🎯 Sua Tarefa em 3 Partes

### Parte 1 — Diagnóstico (`OpenLoopAnalyzer.diagnose` + `LoopDiagnosis.is_open_loop`)
Implemente a contagem do open-loop a partir de um `ShiftLog`. O diagnóstico é o que justifica o sidekick: sem números, "a oficina não melhora" é anecdota.

### Parte 2 — Sessão sidekick (`SidekickSession.guide_next` / `record` / `critical_confirmed` / `progress`)
Implemente o loop guiar → executar → registrar: próximo passo pendente, telemetria voltando com validação, passos críticos exigindo confirmação humana explícita.

### Parte 3 — Fechamento do loop (`SidekickPipeline.close_loop` / `attach_metrics` / `fleet_verdict` + `OutcomeMetrics.meets_targets`)
Transforme telemetria em evals (anomalias recorrentes viram casos de regressão), anexe métricas de negócio e verifique o veredito da frota.

---

## 💻 Starter Code

```python
"""
Exercício 8 — Sidekick: o Agente que Guia Quem Faz
Nível 3 — Arquitetura Avançada

Pipeline: diagnóstico do open-loop → sessão sidekick (agente guia,
humano executa, telemetria retorna) → fechamento do loop (anomalias
viram casos de eval; garantia/CSAT batem as metas).

Fonte do padrão: docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-
a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-
around-ai-analysis.md:98-100 (seção 2.9, Sidekick pattern for physical
work — "Ratatouille" / El Mike).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


# ============================================================================
# CONSTANTES DE GATE E THRESHOLDS
# ============================================================================

MIN_ANOMALY_OCCURRENCES = 2   # anomalia vista 2+ vezes na frota vira eval
WARRANTY_REDUCTION_TARGET = 0.20  # meta: custo de garantia cai >= 20%
QUALITY_TARGET = 0.90         # qualidade de inspeção mínima
CSAT_TARGET = 0.80            # CSAT mínimo
REWORK_MAX = 0.10             # retrabalho máximo tolerado


# ============================================================================
# PARTE 1 — DIAGNÓSTICO DO OPEN-LOOP
# ============================================================================

class EntryKind(Enum):
    TICKET_OPENED = "ticket_opened"            # agente abriu chamado e esqueceu
    WORK_DONE = "work_done"                    # humano executou sem agente guiando
    VOICE_NOTE_RETURNED = "voice_note_returned"  # telemetria do worker voltou
    EVAL_CASE_ADDED = "eval_case_added"        # telemetria virou caso de eval


@dataclass
class ShiftEntry:
    """Um evento registrado num turno da oficina."""
    entry_id: str
    kind: EntryKind
    note: str = ""


@dataclass
class ShiftLog:
    """Log completo de um turno (ANTES open-loop ou DEPOIS sidekick)."""
    shift_id: str
    entries: list[ShiftEntry] = field(default_factory=list)


@dataclass
class LoopDiagnosis:
    """Diagnóstico quantitativo do loop de aprendizado do turno."""
    shift_id: str
    total_entries: int
    tickets_opened: int          # chamados abertos para a fila humana
    work_without_agent: int      # execuções físicas sem agente guiando
    voice_notes_returned: int    # notas de voz que voltaram como telemetria
    eval_cases_added: int        # casos de eval gerados a partir do turno

    def is_open_loop(self) -> bool:
        """
        TODO (Parte 1): retornar True quando houve atividade no turno
        (tickets_opened > 0 OR work_without_agent > 0) E NENHUM caso de
        eval foi gerado (eval_cases_added == 0) — o sinal de
        aprendizado morreu na entrega.
        """
        # TODO: Implementar
        pass


class OpenLoopAnalyzer:
    """Analisa logs de turno e produz diagnósticos de loop."""

    @staticmethod
    def diagnose(log: ShiftLog) -> LoopDiagnosis:
        """
        TODO (Parte 1): percorrer as entradas e contar por EntryKind:
          - tickets_opened:        entradas TICKET_OPENED
          - work_without_agent:    entradas WORK_DONE
          - voice_notes_returned:  entradas VOICE_NOTE_RETURNED
          - eval_cases_added:      entradas EVAL_CASE_ADDED
        """
        # TODO: Implementar
        pass


# ============================================================================
# PARTE 2 — SESSÃO SIDEKICK (guiar → executar → registrar)
# ============================================================================

@dataclass(frozen=True)
class GuidanceStep:
    """
    Um passo do procedimento documentado. Imutável: o procedimento
    não muda durante a sessão — instrução vem do manual, não do improviso.
    """
    step_id: str
    instruction: str                     # o que fazer
    tip: str                             # tolerância/dica ("103 Nm ±4")
    requires_confirmation: bool = False  # passo crítico exige confirmação


@dataclass
class TelemetryEvent:
    """Uma ação do worker retornando pelo canal de guia."""
    step_id: str
    worker_id: str
    confirmed: bool = False   # worker confirmou a execução do passo
    voice_note: str = ""      # nota de voz transcrita (PII removido)
    anomaly: bool = False     # desvio do resultado esperado


@dataclass
class SidekickSession:
    """
    O agente vai junto; o humano executa; a telemetria retorna.

    agent_id roda o MESMO harness da frota (...analysis.md:98) — sem
    stack de assistente paralela. human_worker_id carrega a destreza e
    os sentidos que o software não tem (...analysis.md:99).
    """
    session_id: str
    agent_id: str
    human_worker_id: str
    procedure: list[GuidanceStep] = field(default_factory=list)
    telemetry: list[TelemetryEvent] = field(default_factory=list)

    def guide_next(self) -> GuidanceStep | None:
        """
        TODO (Parte 2): retornar o próximo passo do procedimento (em
        ordem) sem confirmação na telemetria; None se todos confirmados.
        """
        # TODO: Implementar
        pass

    def record(self, event: TelemetryEvent) -> None:
        """
        TODO (Parte 2): registrar a telemetria do worker. Validar que
        event.step_id existe no procedimento; se não existir, levantar
        ValueError — telemetria de passo desconhecido é ruído, não sinal.
        """
        # TODO: Implementar
        pass

    def critical_confirmed(self) -> bool:
        """
        TODO (Parte 2): True somente quando TODO passo com
        requires_confirmation=True tem um TelemetryEvent confirmed
        na sessão. Passo crítico sem confirmação = sessão não fecha.
        """
        # TODO: Implementar
        pass

    def progress(self) -> float:
        """
        TODO (Parte 2): fração de passos do procedimento com confirmação
        na telemetria (0.0-1.0). Procedimento vazio → 0.0.
        """
        # TODO: Implementar
        pass


# ============================================================================
# PARTE 3 — FECHAMENTO DO LOOP (telemetria → evals → métricas)
# ============================================================================

@dataclass
class RegressionCase:
    """Uma anomalia do mundo físico promovida ao corpus de evals."""
    case_id: str
    procedure_id: str
    step_id: str
    anomaly_note: str


@dataclass
class OutcomeMetrics:
    """
    Métricas de negócio, não contadores de atividade (...analysis.md:100):
    o resultado que justifica o sidekick é garantia caindo e CSAT subindo.
    """
    inspection_quality: float   # 0.0-1.0
    warranty_cost_delta: float  # negativo = redução (Kavak: ~-0.20..-0.26)
    csat: float                 # 0.0-1.0
    rework_rate: float          # 0.0-1.0

    def meets_targets(self) -> bool:
        """
        TODO (Parte 3): True quando TODAS as metas batem:
          inspection_quality  >= QUALITY_TARGET
          warranty_cost_delta <= -WARRANTY_REDUCTION_TARGET
          csat                >= CSAT_TARGET
          rework_rate         <= REWORK_MAX
        """
        # TODO: Implementar
        pass


@dataclass
class ShiftReport:
    """Relatório de fechamento de uma sessão sidekick."""
    session_id: str
    progress: float
    critical_confirmed: bool
    anomalies: list[str] = field(default_factory=list)
    regression_cases: list[RegressionCase] = field(default_factory=list)
    metrics: OutcomeMetrics | None = None  # anexado depois do turno


class SidekickPipeline:
    """Pipeline completo: fechamento do loop → métricas → veredito."""

    @staticmethod
    def close_loop(
        session: SidekickSession,
        fleet_anomaly_counts: dict[str, int],
    ) -> ShiftReport:
        """
        TODO (Parte 3): montar o ShiftReport da sessão:
          - progress e critical_confirmed vindos da sessão
          - anomalies: notas de voz dos eventos com anomaly=True
          - regression_cases: para cada evento com anomaly=True cujo
            step_id tem contagem frota >= MIN_ANOMALY_OCCURRENCES,
            um RegressionCase(case_id=f"REG-{session_id}-{step_id}",
            procedure_id=session_id, step_id, anomaly_note=voice_note)
        """
        # TODO: Implementar
        pass

    @staticmethod
    def attach_metrics(report: ShiftReport, metrics: OutcomeMetrics) -> ShiftReport:
        """TODO (Parte 3): anexar métricas ao report e retorná-lo."""
        # TODO: Implementar
        pass

    @staticmethod
    def fleet_verdict(reports: list[ShiftReport]) -> bool:
        """
        TODO (Parte 3): frota aprovada quando TODOS os reports têm
        metrics anexadas (metrics is not None) E todas batem as metas
        (meets_targets()). Lista vazia → False: nada medido, nada aprovado.
        """
        # TODO: Implementar
        pass


# ============================================================================
# DADOS DE TESTE (determinísticos)
# ============================================================================

def build_inspection_procedure() -> list[GuidanceStep]:
    """Procedimento documentado INSP-COMPACT-2026 (6 passos)."""
    return [
        GuidanceStep("S01", "Levantar o veículo e inspecionar pastilhas de freio",
                     "medir espessura: mínimo 3 mm", requires_confirmation=True),
        GuidanceStep("S02", "Calçar as rodas com torque de 103 Nm",
                     "tolerância ±4 Nm; usar chave calibrada", requires_confirmation=True),
        GuidanceStep("S03", "Rodar diagnóstico de bordo (OBD) e registrar códigos",
                     "qualquer código P1xxx exige foto do painel"),
        GuidanceStep("S04", "Documentar o estado do veículo no app (8 fotos)",
                     "incluir pneus e rodas em cada ângulo"),
        GuidanceStep("S05", "Executar teste de rua de 5 km",
                     "escutar freios em baixa velocidade", requires_confirmation=True),
        GuidanceStep("S06", "Entregar as chaves ao cliente",
                     "fronteira física pura — só onde presença é exigida",
                     requires_confirmation=True),
    ]


def build_open_loop_shift() -> ShiftLog:
    """O turno da Ruth ANTES: 3 chamados esquecidos, 4 execuções sem agente."""
    return ShiftLog("TURNO-2026-08-25-OPENLOOP", [
        ShiftEntry("E01", EntryKind.TICKET_OPENED, "chamado #4471: fila de manutenção"),
        ShiftEntry("E02", EntryKind.WORK_DONE, "inspeção improvisada, sem checklist"),
        ShiftEntry("E03", EntryKind.WORK_DONE, "reparo de freio sem registro estruturado"),
        ShiftEntry("E04", EntryKind.TICKET_OPENED, "chamado #4472: fila de manutenção"),
        ShiftEntry("E05", EntryKind.WORK_DONE, "teste de rua sem anotação"),
        ShiftEntry("E06", EntryKind.TICKET_OPENED, "chamado #4473: fila de manutenção"),
        ShiftEntry("E07", EntryKind.WORK_DONE, "entrega de chaves sem confirmação"),
    ])


def build_sidekick_shift() -> ShiftLog:
    """O turno da Ruth DEPOIS: 6 notas de voz voltaram, 1 caso de eval."""
    return ShiftLog("TURNO-2026-08-29-SIDEKICK", [
        ShiftEntry("E01", EntryKind.VOICE_NOTE_RETURNED, "S01 confirmado: pastilhas 5mm"),
        ShiftEntry("E02", EntryKind.VOICE_NOTE_RETURNED, "S02 confirmado: 103 Nm nas 4 rodas"),
        ShiftEntry("E03", EntryKind.VOICE_NOTE_RETURNED, "S03 ok, sem códigos"),
        ShiftEntry("E04", EntryKind.VOICE_NOTE_RETURNED, "S04 8 fotos anexadas"),
        ShiftEntry("E05", EntryKind.VOICE_NOTE_RETURNED, "S05 anomalia: ruído no freio traseiro"),
        ShiftEntry("E06", EntryKind.VOICE_NOTE_RETURNED, "S06 chaves entregues"),
        ShiftEntry("E07", EntryKind.EVAL_CASE_ADDED, "ruído em freio traseiro → caso REG"),
    ])


def build_sidekick_session() -> SidekickSession:
    """A sessão da Ruth com o sidekick: procedimento completo executado."""
    session = SidekickSession(
        session_id="INSP-COMPACT-2026-0142",
        agent_id="inspection-sidekick",   # mesmo harness da frota
        human_worker_id="MEC-142",        # destreza/sentidos insubstituíveis
        procedure=build_inspection_procedure(),
    )
    events = [
        TelemetryEvent("S01", "MEC-142", confirmed=True,
                       voice_note="pastilhas com 5 mm, dentro do mínimo"),
        TelemetryEvent("S02", "MEC-142", confirmed=True,
                       voice_note="103 Nm confirmado nas quatro rodas"),
        TelemetryEvent("S03", "MEC-142", confirmed=True,
                       voice_note="sem códigos de erro"),
        TelemetryEvent("S04", "MEC-142", confirmed=True,
                       voice_note="8 fotos anexadas no app"),
        TelemetryEvent("S05", "MEC-142", confirmed=True, anomaly=True,
                       voice_note="ruído metálico no freio traseiro direito a 40 km/h"),
        TelemetryEvent("S06", "MEC-142", confirmed=True,
                       voice_note="chaves entregues ao cliente"),
    ]
    for e in events:
        session.record(e)
    return session


def build_fleet_anomaly_counts() -> dict[str, int]:
    """Anomalias vistas na frota: o ruído do S05 apareceu 2 vezes."""
    return {"S05": 2}


def build_outcome_metrics() -> OutcomeMetrics:
    """Métricas do piloto sidekick: garantia -24%, CSAT 4.4/5."""
    return OutcomeMetrics(
        inspection_quality=0.93,
        warranty_cost_delta=-0.24,  # dentro da faixa Kavak (~20-26%)
        csat=0.88,
        rework_rate=0.06,
    )


# ============================================================================
# TESTES
# ============================================================================

def test_diagnostico_open_loop():
    """Cenário 1: turno com chamados esquecidos → is_open_loop True."""
    print("\n" + "=" * 60)
    print("TESTE 1: Diagnóstico — Turno Open-Loop")
    print("=" * 60)

    diag = OpenLoopAnalyzer.diagnose(build_open_loop_shift())

    print(f"\n  Chamados abertos:      {diag.tickets_opened}")
    print(f"  Trabalho sem agente:   {diag.work_without_agent}")
    print(f"  Notas de voz:          {diag.voice_notes_returned}")
    print(f"  Casos de eval:         {diag.eval_cases_added}")

    assert diag.tickets_opened == 3, "3 chamados abertos no log"
    assert diag.work_without_agent == 4, "4 execuções sem agente"
    assert diag.voice_notes_returned == 0, "nada voltou do pátio"
    assert diag.eval_cases_added == 0, "nenhum caso de eval gerado"
    assert diag.is_open_loop(), "Turno com atividade e zero eval é open-loop"
    print("  TESTE 1 PASSOU")


def test_diagnostico_closed_loop():
    """Cenário 2: turno sidekick → is_open_loop False."""
    print("\n" + "=" * 60)
    print("TESTE 2: Diagnóstico — Turno Sidekick (loop fechado)")
    print("=" * 60)

    diag = OpenLoopAnalyzer.diagnose(build_sidekick_shift())

    print(f"\n  Notas de voz:          {diag.voice_notes_returned}")
    print(f"  Casos de eval:         {diag.eval_cases_added}")

    assert diag.voice_notes_returned == 6, "6 notas de voz retornaram"
    assert diag.eval_cases_added == 1, "1 caso de eval gerado"
    assert not diag.is_open_loop(), "Turno com telemetria e eval não é open-loop"
    print("  TESTE 2 PASSOU")


def test_guia_passo_a_passo():
    """Cenário 3: guide_next percorre em ordem; progress 1.0; críticos ok."""
    print("\n" + "=" * 60)
    print("TESTE 3: Sessão — Guia Passo a Passo")
    print("=" * 60)

    session = SidekickSession(
        session_id="INSP-WALK",
        agent_id="inspection-sidekick",
        human_worker_id="MEC-142",
        procedure=build_inspection_procedure(),
    )

    walked: list[str] = []
    while (step := session.guide_next()) is not None:
        walked.append(step.step_id)
        session.record(TelemetryEvent(step.step_id, "MEC-142", confirmed=True))

    print(f"\n  Ordem percorrida: {' → '.join(walked)}")
    print(f"  Progresso:        {session.progress():.2f}")

    assert walked == ["S01", "S02", "S03", "S04", "S05", "S06"], (
        "guide_next percorre o procedimento em ordem"
    )
    assert session.progress() == 1.0, "Todos confirmados → progress 1.0"
    assert session.critical_confirmed(), "Todos os críticos confirmados"
    assert session.guide_next() is None, "Procedimento completo → None"
    print("  TESTE 3 PASSOU")


def test_passo_critico_e_validacao():
    """Cenário 4: telemetria de passo inexistente → ValueError."""
    print("\n" + "=" * 60)
    print("TESTE 4: Sessão — Confirmação Crítica e Validação")
    print("=" * 60)

    session = SidekickSession(
        session_id="INSP-CRIT",
        agent_id="inspection-sidekick",
        human_worker_id="MEC-142",
        procedure=build_inspection_procedure(),
    )

    # Nada confirmado ainda: críticos pendentes, progresso zero
    assert not session.critical_confirmed(), "Sem confirmações, críticos pendentes"
    assert session.progress() == 0.0

    # Confirma um passo NÃO crítico: críticos continuam pendentes
    session.record(TelemetryEvent("S03", "MEC-142", confirmed=True))
    assert not session.critical_confirmed(), (
        "Confirmar só o S03 não fecha os passos críticos S01/S02/S05/S06"
    )
    assert 0.0 < session.progress() < 1.0

    # Telemetria de passo inexistente é rejeitada
    try:
        session.record(TelemetryEvent("S99", "MEC-142", confirmed=True))
        raised = False
    except ValueError:
        raised = True
    assert raised, "record() de passo inexistente deve levantar ValueError"
    print("  TESTE 4 PASSOU")


def test_telemetria_vira_caso_de_regressao():
    """Cenário 5: anomalia recorrente vira RegressionCase com a nota."""
    print("\n" + "=" * 60)
    print("TESTE 5: Fechamento — Anomalia → Caso de Regressão")
    print("=" * 60)

    session = build_sidekick_session()
    report = SidekickPipeline.close_loop(session, build_fleet_anomaly_counts())

    print(f"\n  Progresso:          {report.progress:.2f}")
    print(f"  Críticos ok:        {report.critical_confirmed}")
    print(f"  Anomalias:          {report.anomalies}")
    print(f"  Casos de regressão: {[c.case_id for c in report.regression_cases]}")

    assert report.progress == 1.0
    assert report.critical_confirmed
    assert len(report.anomalies) == 1, "Uma anomalia registrada (S05)"
    case = report.regression_cases[0]
    assert case.step_id == "S05", "A anomalia do S05 vira caso"
    assert "ruído" in case.anomaly_note, (
        "A nota de voz do worker vira o anomaly_note do caso"
    )
    assert case.case_id == f"REG-{session.session_id}-S05"
    print("  TESTE 5 PASSOU")


def test_metas_de_negocio():
    """Cenário 6: garantia -24% bate a meta de -20%; frota aprovada."""
    print("\n" + "=" * 60)
    print("TESTE 6: Fechamento — Métricas e Veredito da Frota")
    print("=" * 60)

    metrics = build_outcome_metrics()
    print(f"\n  Qualidade:   {metrics.inspection_quality:.2f} (meta >= {QUALITY_TARGET})")
    print(f"  Garantia:    {metrics.warranty_cost_delta:+.2f} (meta <= {-WARRANTY_REDUCTION_TARGET:+.2f})")
    print(f"  CSAT:        {metrics.csat:.2f} (meta >= {CSAT_TARGET})")
    print(f"  Retrabalho:  {metrics.rework_rate:.2f} (máx {REWORK_MAX})")

    assert metrics.meets_targets(), (
        "Qualidade 0.93, garantia -0.24, CSAT 0.88, retrabalho 0.06 batem as metas"
    )

    # Garantia insuficiente não aprova
    weak = OutcomeMetrics(0.95, -0.10, 0.90, 0.05)
    assert not weak.meets_targets(), "Garantia -0.10 não bate a meta de -0.20"

    # Frota: todos os reports com métricas batendo → aprovada
    session = build_sidekick_session()
    report = SidekickPipeline.close_loop(session, build_fleet_anomaly_counts())
    report = SidekickPipeline.attach_metrics(report, build_outcome_metrics())
    assert report.metrics is not None, "Métricas anexadas ao report"
    assert SidekickPipeline.fleet_verdict([report]), "Frota com 1 report ok → True"

    # Report sem métricas → frota não aprovada (nada medido)
    bare = SidekickPipeline.close_loop(session, build_fleet_anomaly_counts())
    assert not SidekickPipeline.fleet_verdict([bare]), (
        "Report sem métricas não sustenta veredito"
    )
    assert not SidekickPipeline.fleet_verdict([]), "Lista vazia → False"
    print("  TESTE 6 PASSOU")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("EXERCÍCIO 8: SIDEKICK PATTERN AT PHYSICAL BOUNDARIES")
    print("=" * 60)

    # Quando implementado, descomente para testar:
    # test_diagnostico_open_loop()
    # test_diagnostico_closed_loop()
    # test_guia_passo_a_passo()
    # test_passo_critico_e_validacao()
    # test_telemetria_vira_caso_de_regressao()
    # test_metas_de_negocio()

    print("\nTODO: Implemente as partes acima!")
    print("   1. OpenLoopAnalyzer.diagnose() + LoopDiagnosis.is_open_loop()")
    print("   2. SidekickSession.guide_next() / record() / critical_confirmed() / progress()")
    print("   3. OutcomeMetrics.meets_targets()")
    print("   4. SidekickPipeline.close_loop() / attach_metrics() / fleet_verdict()")
    print("   Após implementar, descomente os testes em main()")
```

---

## ✅ Validação: Critérios de Aceitação

Seu código será considerado **APROVADO** quando:

### Critério 1: Diagnóstico do open-loop (Parte 1)

- [ ] `diagnose()` conta chamados, trabalho sem agente, notas de voz e casos de eval corretamente por `EntryKind`
- [ ] Turno com atividade e zero casos de eval: `is_open_loop() == True`
- [ ] Turno sidekick (notas de voz + eval gerado): `is_open_loop() == False`

### Critério 2: Sessão sidekick (Parte 2)

- [ ] `guide_next()` percorre o procedimento em ordem e retorna `None` no fim
- [ ] `record()` rejeita telemetria de passo inexistente com `ValueError`
- [ ] `critical_confirmed()` exige confirmação de TODOS os passos `requires_confirmation` (S01, S02, S05, S06)
- [ ] `progress()` == 1.0 somente com todos os passos confirmados

### Critério 3: Fechamento do loop (Parte 3)

- [ ] Anomalia com contagem frota >= `MIN_ANOMALY_OCCURRENCES` vira `RegressionCase` com `anomaly_note` da nota de voz
- [ ] `meets_targets()` exige as 4 metas: qualidade >= 0.90, garantia <= -0.20, CSAT >= 0.80, retrabalho <= 0.10
- [ ] `fleet_verdict()` aprova somente com TODOS os reports medidos e aprovados; report sem métricas reprova; lista vazia reprova

---

## 📊 Rubric de Avaliação

| Critério | Peso | Insuficiente (0-3) | Básico (4-6) | Proficiente (7-8) | Excelente (9-10) |
|---|---|---|---|---|---|
| **Diagnóstico (Parte 1)** | 20% | Não implementado | Conta entradas mas erra a regra do loop | Contadores corretos + regra atividade-sem-eval aplicada | Diagnóstico completo contrastando o sinal que morre (chamado) com o que volta (telemetria) |
| **Sessão Sidekick (Parte 2)** | 25% | Não implementado | `guide_next` funciona sem validação | Guia em ordem + `ValueError` em passo desconhecido | Loop guiar→executar→registrar completo com confirmação explícita de passos críticos bloqueando o fechamento |
| **Fechamento do Loop (Parte 3)** | 35% | Não implementado | Report sem casos de regressão | Anomalia recorrente vira `RegressionCase` com nota de voz | Telemetria→evals + métricas de negócio com metas explícitas e veredito de frota que reprova o não medido |
| **Escopo e Fronteira** | 20% | Não implementado | Trata sidekick como fallback generalizado | Escopo na fronteira física com política explícita | Contraste explícito: sidekick ≠ escalonamento de julgamento (Ex. 6) ≠ automação total; procedimento documentado, não inventado |

**Nota final:** Média ponderada. **Aprovação:** >= 7.0

---

## 💡 Dicas para Implementação

### Para o diagnóstico

1. **A assinatura do open-loop é "atividade sem aprendizado".** Não é ausência de software — o SAC-BOT fazia muita coisa (abria chamados!). O open-loop é haver trabalho (chamados OU execução) e NENHUM caso de eval gerado. O sinal de aprendizado morre na entrega (`...analysis.md:164`).
2. **O diagnóstico justifica o projeto.** "412 chamados, 0 retornos, 0 casos de eval, garantia +8%" é o que transforma "a oficina não melhora" em caso de sidekick.

### Para a sessão

1. **Procedimento é documentação, não improviso.** `GuidanceStep` é `frozen=True` porque a instrução e a tolerância vêm do manual de inspeção. Se seu agente gera passos em runtime, você construiu uma alucinação guiada, não um sidekick.
2. **Passo crítico é uma confirmação, não uma suposição.** `critical_confirmed()` deriva do cruzamento procedimento × telemetria — nada de flag booleana mantida à mão.
3. **Telemetria de passo desconhecido é ruído.** O `ValueError` do `record()` protege o corpus de evals: caso de regressão só nasce de passo que existe no procedimento.

### Para o fechamento

1. **O valor do padrão mora no loop, não na guia.** Guiar Ruth é metade; a outra metade é o ruído do freio traseiro (visto 2× na frota) virar caso de teste para os evals da frota inteira. Sem essa conversão, você tem um checklist falante — e o sistema continua empacando.
2. **Métricas de negócio, não contadores de atividade.** O caso Kavak se sustenta em qualidade de inspeção, custo de garantia ~20-26% abaixo e CSAT acima (`...analysis.md:100`). "Notas de voz coletadas" é sinal sem verdade, da mesma família dos KPIs superficiais que o playbook rejeita.
3. **Não medido ≠ aprovado.** `fleet_verdict()` reprova report sem métricas: a ausência de medição é exactly o estado do open-loop que você diagnosticou na Parte 1.

---

## ❓ Dúvidas Comuns

**P: Isso não é "humano-no-loop" genérico?**
R: Não — o escopo é a fronteira física genuína. Na Kavak, 96% das interações e 95% das transações são totalmente agent-handled; humanos permanecem só onde presença física é exigida, tipo entregar a chave do carro (`...analysis.md:105-106`). O `docs/canonical/sidekick-pattern-physical-boundaries.md` chama isso de regra de escopo: humano-como-fallback-generalizado é o anti-padrão, e a fronteira é decisão de policy que deriva com a capacidade robótica.

**P: Qual a diferença para o Exercício 6 (presence-in-the-loop-metric)?**
R: A direção do serviço. No Exercício 6 o humano intervém numa tarefa do agente (decide/revisa saída) e a métrica mede essa presença. Aqui o agente guia a execução física do humano — mesma inversão "humanos servem agentes" do help API e do Exercício 7 (`...analysis.md:176`). São as duas faces da fronteira, com padrões diferentes de cada lado.

**P: Por que não automatizar a inspeção de vez?**
R: Porque o gap sensor/atuador é real: destreza e sentidos são insubstituíveis (~800 mecânicos na Kavak, `...analysis.md:99`), e o agente vê só o que a telemetria humana retorna (canonical, tradeoffs). A automação total sem canal de telemetria é a fantasia que abre espaço para o chamado esquecido.

**P: Nota de voz do trabalhador não vira vigilância?**
R: O canal é de telemetria de procedimento (passo, confirmação, anomalia), não de vigilância: PII removido antes de entrar no corpus de eval, e a nota existe para alimentar o estado do agente e os evals da frota. A regra está nas Implementation Rules do canonical.

**P: Por que a anomalia precisa aparecer 2 vezes para virar caso?**
R: `MIN_ANOMALY_OCCURRENCES = 2` filtra o ruído do sinal: um evento único pode ser o disco de freio daquele carro; a recorrência na frota indica um modo de falha do procedimento ou do veículo — isso sim vira caso de regressão para os evals.

---

## 🚀 Próximo Passo

Depois de completar este exercício:

1. Leia o canonical completo em `docs/canonical/sidekick-pattern-physical-boundaries.md` — problema, solução, o exemplo `sidekick-session.yaml` e os tradeoffs — e a entrada da classificação `Missing` em `docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-classification.yaml:217-229`
2. Releia a Pattern 13 em `curriculum/05-core-concepts/07-multi-agent-coordination.md:749-773` — agora com o loop implementado, a regra de escopo (humanos só na fronteira física) fica concreta
3. (Opcional) Extensão: conecte o `SidekickSession` ao `carve-out-pilot-hard-target` (canonical) — o loop de plan-push diário com notas de voz (`...analysis.md:50`) é o mesmo canal visto de cima: um sidekick por worker vira o plano diário da unidade inteira

---

*Exercício 8 | Nível 3 — Arquitetura Avançada | Sidekick Pattern at Physical Boundaries*

**O agente guia quem faz; o que quem faz vê, volta. Sem telemetria não há frota — há chamados esquecidos.**
