---
title: "Exercicio 6: Implementar a Metrica de Presenca no Loop"
type: curriculum-exercise
nivel: 3
aliases: ["presence in the loop", "metrica de presenca", "human involvement metric", "stale presence", "absent owner", "review confidence signal", "intervention checkpoint"]
tags: [curriculo-conteudo, nivel-3, exercicio, agentes-orquestracao, governanca, presence-metric, harness-governance, human-in-the-loop, review-confidence, decision-discipline, python, dataclass]
relates-to: ["[[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-patterns|IDSD Method Patterns]]", "[[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-classification|IDSD Method Classification]]", "[[docs/canonical/manual-brake-question-gate|Manual Brake Question Gate]]", "[[docs/canonical/human-afk-task-routing-gate|Human/AFK Task Routing Gate]]", "[[docs/canonical/value-gated-agent-control-loop|Value-Gated Agent Control Loop]]", "[[docs/canonical/generator-evaluator|Generator-Evaluator]]", "[[curriculum/03-nivel-3-advanced-architecture/01-multi-agent-systems|Multi-Agent Systems]]"]
last_updated: 2026-06-12
---
# Exercicio 6: Implementar a Metrica de Presenca no Loop
## Nivel 3 - Arquitetura Avancada

**Tempo Estimado:** 75-105 minutos
**Dificuldade:** (Avancado)
**Pre-requisito:** Ter lido `01-multi-agent-systems.md` (Nivel 3) + `docs/canonical/manual-brake-question-gate.md`
**Objetivo:** Diagnosticar os riscos de agentes operando sem supervisao humana durante a execucao e implementar uma metrica de presenca que mede envolvimento real -- nao aprovacao simbolica ao final

---

## Prologo: O Diff de 2.300 Linhas Que Ninguem Viu Nascer

### Segunda-feira, 8h00. Um card aparentemente simples.

```
PM: "@dev_agent implementa o sistema de notificacao de pedidos do KODA.
     O cliente precisa saber quando o pedido saiu para entrega."

DEV_AGENT: [Analisando...]
           "Entendido. Implementar sistema de notificacao de pedidos."
```

**O que aconteceu nas 6 horas seguintes:**

```
08:00  Agente inicia trabalho. Gera plano de 5 passos.
08:15  Passo 1: Modelagem do schema de notificacoes. OK.
08:45  Passo 2: Integracao com API de logistica. OK.
09:30  Passo 3: Implementacao do sistema de templates de mensagem. OK.
       ┌─ AQUI o agente decidiu que notificacoes seriam por email ─┐
       │  O KODA e um sistema de WHATSAPP. Clientes nao usam email. │
       │  Mas ninguem viu essa decisao. Ninguem estava presente.    │
       └────────────────────────────────────────────────────────────┘
11:00  Passo 4: Implementacao do agendador de notificacoes (cron). OK.
12:30  Passo 5: Testes de integracao. OK.
14:00  Agente conclui. Abre PR com 2.300 linhas.

14:15  Reviewer (humano) abre o PR.
       "Espera... isso envia EMAIL? O KODA e WhatsApp!"
       "E essa integracao usa a API antiga de logistica -- mudamos
        para a Loggi ha 3 meses."
       "E por que tem um cron job? O KODA ja tem um scheduler..."
```

**O custo da ausencia:**

```
╔══════════════════════════════════════════════════════════════════╗
║              O DIFF QUE NINGUEM VIU NASCER                       ║
║                                                                  ║
║  Duracao da execucao:        6 horas                             ║
║  Linhas geradas:             2.300                               ║
║  Intervencoes humanas:       0                                   ║
║  Decisoes arquiteturais:     4 (todas sem revisao)               ║
║    - Canal: email (deveria ser WhatsApp)            ❌ ERRADA    ║
║    - API: antiga (deveria ser Loggi)                ❌ ERRADA    ║
║    - Scheduling: cron (deveria usar scheduler KODA) ❌ REDUNDANTE║
║    - Templates: reinventados (existiam no codebase) ❌ DUPLICADO ║
║                                                                  ║
║  Tempo ate o rollback:       1 dia (code review + reimplementacao)║
║  Codigo descartado:          2.100 linhas (91%)                  ║
║  Tokens desperdicados:       4.800.000                           ║
║                                                                  ║
║  Se houvesse UM checkpoint humano na hora 1:                     ║
║  - "KODA e WhatsApp, nao email" → agente corrige na hora 1      ║
║  - "API da Loggi, nao a antiga" → agente usa endpoint correto   ║
║  - 4.8M tokens → ~600K tokens                                   ║
║  - 6 horas → 1.5 horas                                          ║
║  - 2.300 linhas → 400 linhas (todas aproveitaveis)              ║
╚══════════════════════════════════════════════════════════════════╝
```

**O problema nao foi a qualidade do agente.** O agente implementou exatamente o que
entendeu do pedido, com excelencia tecnica. O problema foi que **ninguem estava presente
durante a execucao para detectar que o entendimento estava errado na primeira hora**.

A aprovacao final (code review) chegou tarde demais -- quando 91% do codigo ja era
descartavel. Se um humano tivesse sido convocado para um checkpoint na hora 1, o desvio
teria sido corrigido antes de gerar 2.000 linhas de codigo inutil.

**Sua missao:** Construir um `PresenceTracker` que mede o envolvimento humano DURANTE a
execucao do agente, emite alertas de stale-presence quando o owner fica ausente por tempo
demais, e produz um `PresenceReport` que o gate de revisao final usa como sinal de
confianca -- "este diff foi supervisionado ou foi produzido no vacuo?"

---

## O Contexto

### O Modelo Mental: Presenca como Metrica de Governanca

O padrao Presence-in-the-Loop propoe que **aprovacao ao final nao e suficiente**. O que
importa e a densidade de envolvimento humano durante a execucao. Um diff de 500 linhas
com 3 checkpoints humanos ao longo de 2 horas e mais confiavel que um diff de 100 linhas
gerado sem nenhum envolvimento humano em 15 minutos.

Quatro sinais compoem a metrica:

| Sinal | O que mede | Por que importa |
|---|---|---|
| **Presence Timeline** | Linha do tempo mostrando exatamente quando o owner interagiu com o agente durante a execucao | Torna visivel o vacuo de supervisao |
| **Stale-Presence Warning** | Alerta emitido quando o owner fica ausente por mais que um threshold configurado | Previne que o agente opere sem supervisao por horas |
| **Required Intervention Points** | Checkpoints obrigatorios onde o agente PAUSA e so continua apos confirmacao humana | Forca presenca em pontos criticos de decisao |
| **Review Confidence Signal** | Score agregado (0.0 a 1.0) que o revisor final usa para calibrar o nivel de escrutinio | Permite revisao proporcional ao risco |

### O Que Voce Vai Construir

Voce vai implementar um `PresenceTracker` que:

1. Monitora eventos de interacao (humano respondeu pergunta, humano aprovou passo, humano corrigiu direcao)
2. Mantem uma `PresenceTimeline` com timestamps de cada interacao
3. Emite `StalePresenceWarning` quando o intervalo desde a ultima interacao excede thresholds
4. Define `InterventionCheckpoints` -- pontos obrigatorios de parada baseados no tipo de trabalho e risco
5. Calcula um `ReviewConfidenceSignal` que informa o revisor final sobre a qualidade da supervisao

O dominio de exemplo e uma sessao de desenvolvimento com o KODA: 6 horas de trabalho
autonomo com diferentes densidades de intervencao humana.

---

## Requisitos

### Funcionais

- [ ] `PresenceTracker` registra eventos de interacao com timestamp, tipo, e agente envolvido
- [ ] `PresenceTimeline` mostra todos os eventos em ordem cronologica com intervalos entre eles
- [ ] `StalePresenceWarning` e emitido quando o intervalo desde a ultima interacao excede thresholds configurados (warning: 30min, critical: 90min, escalation: 180min)
- [ ] `InterventionCheckpoint` e um ponto obrigatorio de parada definido por: tipo de decisao, risco estimado, e tamanho do diff acumulado desde o ultimo checkpoint
- [ ] `ReviewConfidenceSignal` e um score 0.0-1.0 calculado a partir de: densidade de interacoes, presenca em decisoes criticas, tempo maximo sem supervisao, e cobertura de checkpoints
- [ ] O sistema distingue entre presenca PASSIVA (abriu o PR, olhou por 30 segundos) e presenca ATIVA (respondeu pergunta, corrigiu direcao, aprovou decisao arquitetural)
- [ ] O `PresenceReport` e gerado ao final da sessao e anexado ao PR como evidencia de governanca

### Tecnicos

- [ ] Python 3.9+ com type hints
- [ ] Usar `dataclasses` para os modelos de dados
- [ ] `PresenceTracker` e thread-safe (simulado -- operacoes atomicas em lista)
- [ ] `PresenceTimeline` e imutavel apos construcao
- [ ] `ReviewConfidenceSignal` e uma funcao pura: timeline + checkpoints + thresholds → score
- [ ] Thresholds sao configuraveis por perfil de risco (baixo, medio, alto, critico)

### Validacao

- [ ] Cenario 1: Sessao supervisionada (16 intervencoes em 6h) → confidence > 0.85
- [ ] Cenario 2: Sessao abandonada (0 intervencoes em 6h) → confidence < 0.15, alerta de escalation emitido
- [ ] Cenario 3: Sessao com presenca apenas no inicio e fim → confidence media, alerta de stale-presence critical emitido
- [ ] Cenario 4: Checkpoint obrigatorio ignorado → confidence penalizada, alerta de checkpoint missed
- [ ] Cenario 5: Presenca ativa vs passiva → presenca ativa contribui mais para confidence que passiva

---

## Arquitetura do Sistema

### Diagrama ASCII

```
┌──────────────────────────────────────────────────────────────────┐
│                    PRESENCE TRACKER                               │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │              EVENT COLLECTOR                               │     │
│  │                                                            │     │
│  │  Captura eventos de interacao durante a execucao:          │     │
│  │  ┌──────────────────────────────────────────────────────┐ │     │
│  │  │ owner_asked_question("Qual API de logistica?")        │ │     │
│  │  │ owner_answered("Loggi, endpoint /v2/tracking")        │ │     │
│  │  │ owner_approved_step("Modelagem do schema")            │ │     │
│  │  │ owner_corrected_direction("WhatsApp, nao email")      │ │     │
│  │  │ agent_requested_checkpoint("Decisao arquitetural")    │ │     │
│  │  │ reviewer_opened_pr()                                  │ │     │
│  │  └──────────────────────────────────────────────────────┘ │     │
│  └───────────────────────────┬────────────────────────────────┘     │
│                              │                                      │
│                              ▼                                      │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │              PRESENCE TIMELINE                             │     │
│  │                                                            │     │
│  │  t=0    t=30m   t=55m   t=90m   t=120m  t=210m  t=360m   │     │
│  │  ├───────┼───────┼───────┼───────┼───────┼───────┼──────┤│     │
│  │  START   ASK    ANSWER  APPROVE CORRECT ......  REVIEW    │     │
│  │          (25m)  (35m)   (60m)   (90m)          (150m)    │     │
│  │  gap=0   gap=30 gap=25  gap=5   gap=30  .......gap=150  │     │
│  │                                          ▲                │     │
│  │                           STALE-PRESENCE CRITICAL          │     │
│  │                           (150min sem interacao)           │     │
│  └───────────────────────────┬────────────────────────────────┘     │
│                              │                                      │
│                              ▼                                      │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │              STALE-PRESENCE MONITOR                        │     │
│  │                                                            │     │
│  │  Thresholds por perfil de risco:                           │     │
│  │  ┌──────────┬─────────┬──────────┬─────────────┐         │     │
│  │  │ Perfil   │ WARNING │ CRITICAL │ ESCALATION  │         │     │
│  │  ├──────────┼─────────┼──────────┼─────────────┤         │     │
│  │  │ BAIXO    │ 60 min  │ 180 min  │ 360 min     │         │     │
│  │  │ MEDIO    │ 30 min  │  90 min  │ 180 min     │         │     │
│  │  │ ALTO     │ 15 min  │  45 min  │  90 min     │         │     │
│  │  │ CRITICO  │  5 min  │  15 min  │  30 min     │         │     │
│  │  └──────────┴─────────┴──────────┴─────────────┘         │     │
│  └───────────────────────────┬────────────────────────────────┘     │
│                              │                                      │
│                              ▼                                      │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │              INTERVENTION CHECKPOINTS                      │     │
│  │                                                            │     │
│  │  Checkpoints obrigatorios definidos por:                   │     │
│  │  - Decisao arquitetural (escolha de tecnologia)            │     │
│  │  - Mudanca de direcao (escopo expandiu/reduziu)            │     │
│  │  - Tamanho de diff acumulado > threshold                  │     │
│  │  - Passagem de fase (planejamento → execucao → teste)     │     │
│  └───────────────────────────┬────────────────────────────────┘     │
│                              │                                      │
│                              ▼                                      │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │              REVIEW CONFIDENCE SIGNAL                      │     │
│  │                                                            │     │
│  │  Score = f(densidade, criticidade, lacunas, cobertura)    │     │
│  │                                                            │     │
│  │  Componentes:                                              │     │
│  │  - interaction_density:     intervencoes / hora            │     │
│  │  - active_presence_ratio:   presenca ativa / total         │     │
│  │  - max_stale_gap_minutes:   maior intervalo sem supervisao │     │
│  │  - checkpoint_coverage:     checkpoints atendidos / total  │     │
│  │  - early_correction_bonus:  bonus por correcao precoce     │     │
│  │  - late_review_penalty:     penalidade por revisao tardia  │     │
│  └──────────────────────────────────────────────────────────┘     │
│                              │                                      │
│                              ▼                                      │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │              PRESENCE REPORT (anexado ao PR)               │     │
│  │                                                            │     │
│  │  {                                                         │     │
│  │    "session_id": "KODA-2026-06-12-001",                    │     │
│  │    "duration_minutes": 360,                                │     │
│  │    "total_interactions": 16,                               │     │
│  │    "active_interactions": 9,                               │     │
│  │    "passive_interactions": 7,                              │     │
│  │    "stale_presence_warnings": ["critical@150m"],           │     │
│  │    "missed_checkpoints": [],                               │     │
│  │    "review_confidence": 0.72,                              │     │
│  │    "verdict": "MODERATE_SUPERVISION"                       │     │
│  │  }                                                         │     │
│  └──────────────────────────────────────────────────────────┘     │
└──────────────────────────────────────────────────────────────────┘
```

---

## Starter Code

```python
"""
Exercicio 6 — Implementar a Metrica de Presenca no Loop
Nivel 3 — Arquitetura Avancada

Implemente um PresenceTracker que mede o envolvimento humano DURANTE
a execucao do agente e produz um sinal de confianca para o revisor final.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Optional


# ============================================================================
# DATA MODELS
# ============================================================================

class InteractionType(Enum):
    """Tipos de interacao entre humano e agente durante a execucao."""

    # Presenca ATIVA (humano tomou decisao ou corrigiu direcao)
    OWNER_ANSWERED_QUESTION = "owner_answered_question"     # respondeu pergunta do agente
    OWNER_CORRECTED_DIRECTION = "owner_corrected_direction" # corrigiu direcao do trabalho
    OWNER_APPROVED_DECISION = "owner_approved_decison"      # aprovou decisao arquitetural
    OWNER_CLARIFIED_CONSTRAINT = "owner_clarified_constraint" # esclareceu constraint ambigua

    # Presenca PASSIVA (humano observou mas nao decidiu)
    OWNER_VIEWED_PROGRESS = "owner_viewed_progress"         # abriu e olhou o progresso
    OWNER_ACKNOWLEDGED = "owner_acknowledged"               # confirmou que viu (sem decidir)
    REVIEWER_OPENED_PR = "reviewer_opened_pr"               # abriu o PR para revisao
    REVIEWER_COMMENTED = "reviewer_commented"               # comentou no PR

    # Eventos do agente (nao sao intervencao humana)
    AGENT_REQUESTED_CHECKPOINT = "agent_requested_checkpoint" # agente pediu parada
    AGENT_COMPLETED_PHASE = "agent_completed_phase"           # completou uma fase
    AGENT_DETECTED_UNCERTAINTY = "agent_detected_uncertainty" # detectou ambiguidade

    @classmethod
    def active_types(cls) -> set[InteractionType]:
        """Tipos que representam presenca ATIVA (humano decidiu)."""
        return {
            cls.OWNER_ANSWERED_QUESTION,
            cls.OWNER_CORRECTED_DIRECTION,
            cls.OWNER_APPROVED_DECISION,
            cls.OWNER_CLARIFIED_CONSTRAINT,
        }

    @classmethod
    def passive_types(cls) -> set[InteractionType]:
        """Tipos que representam presenca PASSIVA (humano observou)."""
        return {
            cls.OWNER_VIEWED_PROGRESS,
            cls.OWNER_ACKNOWLEDGED,
            cls.REVIEWER_OPENED_PR,
            cls.REVIEWER_COMMENTED,
        }

    @classmethod
    def human_types(cls) -> set[InteractionType]:
        """Todos os tipos que envolvem acao humana."""
        return cls.active_types() | cls.passive_types()


class RiskProfile(Enum):
    """Perfil de risco da sessao -- determina thresholds de stale-presence."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class StalePresenceLevel(Enum):
    """Nivel de alerta de stale-presence."""
    NORMAL = "normal"
    WARNING = "warning"
    CRITICAL = "critical"
    ESCALATION = "escalation"


@dataclass
class InteractionEvent:
    """Um evento de interacao na timeline de presenca."""
    timestamp: str  # ISO 8601
    interaction_type: InteractionType
    actor: str  # "owner", "reviewer", "agent"
    description: str
    phase: str = ""  # fase do trabalho em que ocorreu
    diff_size_at_event: int = 0  # linhas acumuladas ate este ponto


@dataclass
class PresenceTimeline:
    """Linha do tempo completa de presenca durante uma sessao."""
    session_id: str
    risk_profile: RiskProfile
    events: list[InteractionEvent] = field(default_factory=list)
    started_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    completed_at: str = ""

    def add_event(self, event: InteractionEvent) -> None:
        """Adiciona um evento a timeline."""
        self.events.append(event)

    @property
    def duration_minutes(self) -> float:
        """Duracao total da sessao em minutos."""
        if not self.events:
            return 0.0
        start = datetime.fromisoformat(self.events[0].timestamp)
        if self.completed_at:
            end = datetime.fromisoformat(self.completed_at)
        else:
            end = datetime.fromisoformat(self.events[-1].timestamp)
        return (end - start).total_seconds() / 60.0

    @property
    def human_events(self) -> list[InteractionEvent]:
        """Apenas eventos com acao humana (ativo + passivo)."""
        return [e for e in self.events if e.interaction_type in InteractionType.human_types()]

    @property
    def active_events(self) -> list[InteractionEvent]:
        """Apenas eventos de presenca ativa."""
        return [e for e in self.events if e.interaction_type in InteractionType.active_types()]


@dataclass
class StalePresenceWarning:
    """Alerta de ausencia prolongada do owner."""
    level: StalePresenceLevel
    gap_minutes: float
    since_event: InteractionEvent
    threshold_exceeded: float
    message: str = ""


@dataclass
class InterventionCheckpoint:
    """Checkpoint obrigatorio onde o agente deve pausar."""
    checkpoint_id: str
    description: str
    trigger_reason: str  # "phase_transition", "architectural_decision", "diff_accumulated"
    required: bool = True
    was_triggered: bool = False
    was_satisfied: bool = False  # dono respondeu?


@dataclass
class ReviewConfidenceSignal:
    """Sinal de confianca para o revisor final."""
    score: float  # 0.0 a 1.0
    interaction_density: float  # intervencoes humanas / hora
    active_presence_ratio: float  # presenca ativa / total de eventos humanos
    max_stale_gap_minutes: float  # maior intervalo sem supervisao
    checkpoint_coverage: float  # checkpoints atendidos / total
    total_human_interactions: int = 0
    total_active_interactions: int = 0
    stale_warnings: list[StalePresenceWarning] = field(default_factory=list)
    missed_checkpoints: list[str] = field(default_factory=list)
    verdict: str = ""  # "HIGH_CONFIDENCE", "MODERATE_SUPERVISION", "LOW_SUPERVISION", "UNSUPERVISED"


@dataclass
class PresenceReport:
    """Relatorio final de presenca -- anexado ao PR."""
    session_id: str
    risk_profile: RiskProfile
    duration_minutes: float
    total_interactions: int
    active_interactions: int
    passive_interactions: int
    confidence_signal: ReviewConfidenceSignal
    timeline: PresenceTimeline
    generated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# ============================================================================
# STALE-PRESENCE THRESHOLDS
# ============================================================================

STALE_THRESHOLDS: dict[RiskProfile, dict[StalePresenceLevel, int]] = {
    RiskProfile.LOW: {
        StalePresenceLevel.WARNING: 60,
        StalePresenceLevel.CRITICAL: 180,
        StalePresenceLevel.ESCALATION: 360,
    },
    RiskProfile.MEDIUM: {
        StalePresenceLevel.WARNING: 30,
        StalePresenceLevel.CRITICAL: 90,
        StalePresenceLevel.ESCALATION: 180,
    },
    RiskProfile.HIGH: {
        StalePresenceLevel.WARNING: 15,
        StalePresenceLevel.CRITICAL: 45,
        StalePresenceLevel.ESCALATION: 90,
    },
    RiskProfile.CRITICAL: {
        StalePresenceLevel.WARNING: 5,
        StalePresenceLevel.CRITICAL: 15,
        StalePresenceLevel.ESCALATION: 30,
    },
}


# ============================================================================
# PRESENCE TRACKER
# ============================================================================

class PresenceTracker:
    """
    Rastreador de presenca humana durante a execucao de um agente.

    Responsabilidades:
    1. Registrar eventos de interacao na timeline
    2. Monitorar intervalos sem supervisao (stale-presence)
    3. Emitir alertas quando thresholds sao excedidos
    4. Gerenciar checkpoints obrigatorios
    5. Calcular o sinal de confianca para revisao final
    """

    def __init__(self, session_id: str, risk_profile: RiskProfile = RiskProfile.MEDIUM):
        """
        Args:
            session_id: Identificador da sessao do agente.
            risk_profile: Perfil de risco que determina os thresholds.
        """
        # TODO: Implementar inicializacao
        # 1. Criar PresenceTimeline com session_id e risk_profile
        # 2. Inicializar lista de checkpoints vazia
        # 3. Inicializar lista de warnings vazia
        pass

    def record_interaction(
        self,
        interaction_type: InteractionType,
        actor: str,
        description: str,
        phase: str = "",
        diff_size: int = 0,
    ) -> InteractionEvent:
        """
        Registra um evento de interacao na timeline.

        Args:
            interaction_type: Tipo da interacao.
            actor: Quem realizou ("owner", "reviewer", "agent").
            description: Descricao do que aconteceu.
            phase: Fase do trabalho.
            diff_size: Tamanho do diff acumulado ate este ponto.

        Returns:
            O evento criado.
        """
        # TODO: Implementar
        pass

    def add_checkpoint(self, checkpoint: InterventionCheckpoint) -> None:
        """Adiciona um checkpoint obrigatorio a sessao."""
        # TODO: Implementar
        pass

    def trigger_checkpoint(self, checkpoint_id: str) -> None:
        """Marca um checkpoint como disparado (agente pausou)."""
        # TODO: Implementar
        pass

    def satisfy_checkpoint(self, checkpoint_id: str, satisfied: bool = True) -> None:
        """Marca um checkpoint como satisfeito (owner respondeu)."""
        # TODO: Implementar
        pass

    def check_stale_presence(self) -> StalePresenceLevel:
        """
        Verifica se o owner esta ausente por tempo excessivo.

        Calcula o intervalo desde a ultima interacao HUMANA e compara
        com os thresholds do perfil de risco da sessao.

        Returns:
            StalePresenceLevel indicando o nivel de alerta atual.
        """
        # TODO: Implementar
        #
        # Algoritmo sugerido:
        # 1. Encontrar a ultima interacao humana na timeline
        # 2. Calcular gap em minutos desde aquela interacao ate agora
        # 3. Comparar gap com thresholds do perfil de risco:
        #    gap >= escalation → ESCALATION
        #    gap >= critical   → CRITICAL
        #    gap >= warning    → WARNING
        #    senao             → NORMAL
        pass

    def get_stale_warnings(self) -> list[StalePresenceWarning]:
        """
        Retorna todos os alertas de stale-presence que foram ou
        seriam emitidos durante a sessao.

        Examina a timeline completa e identifica todos os intervalos
        entre interacoes humanas que excederam thresholds.

        Returns:
            Lista de StalePresenceWarning em ordem cronologica.
        """
        # TODO: Implementar
        #
        # Algoritmo sugerido:
        # 1. Iterar sobre eventos humanos em ordem
        # 2. Para cada par consecutivo, calcular gap em minutos
        # 3. Se gap >= warning threshold: criar StalePresenceWarning
        # 4. Determinar nivel (warning/critical/escalation) pelo gap
        # 5. Acumular na lista de resultados
        pass

    def calculate_confidence(self) -> ReviewConfidenceSignal:
        """
        Calcula o sinal de confianca para o revisor final.

        Componentes do score (cada um contribui para score 0.0-1.0):

        1. interaction_density (peso 0.25):
           intervencoes_humanas / duracao_horas
           >= 2/hora → 1.0, 0/hora → 0.0

        2. active_presence_ratio (peso 0.30):
           presenca_ativa / total_interacoes_humanas
           1.0 → 1.0, 0.0 → 0.0

        3. max_stale_gap (peso 0.25):
           1.0 - (max_gap / escalation_threshold)
           gap 0 → 1.0, gap >= escalation → 0.0

        4. checkpoint_coverage (peso 0.20):
           checkpoints_satisfeitos / total_checkpoints
           1.0 → 1.0, 0.0 → 0.0

        Verdict baseado no score:
        >= 0.85: HIGH_CONFIDENCE
        >= 0.60: MODERATE_SUPERVISION
        >= 0.30: LOW_SUPERVISION
        < 0.30:  UNSUPERVISED

        Returns:
            ReviewConfidenceSignal com score e componentes.
        """
        # TODO: Implementar
        pass

    def generate_report(self) -> PresenceReport:
        """Gera o relatorio final de presenca."""
        # TODO: Implementar
        pass


# ============================================================================
# SESSION SCENARIOS (dados de teste)
# ============================================================================

def build_supervised_session() -> PresenceTracker:
    """
    Cenario 1: Sessao bem supervisionada.
    Owner interveio regularmente durante 6 horas de trabalho.
    16 interacoes, incluindo 2 correcoes de direcao.
    """
    tracker = PresenceTracker("KODA-2026-06-12-SUPERVISED", RiskProfile.MEDIUM)

    # Registra eventos em ordem cronologica ao longo de 6 horas
    base_time = datetime(2026, 6, 12, 8, 0, 0, tzinfo=timezone.utc)

    events = [
        (0, InteractionType.AGENT_COMPLETED_PHASE, "agent", "Planejamento concluido", "planning", 0),
        (5, InteractionType.OWNER_APPROVED_DECISION, "owner", "Aprovou plano de 5 passos", "planning", 0),
        (25, InteractionType.OWNER_ANSWERED_QUESTION, "owner", "Confirmou: API Loggi v2, nao v1", "implementation", 80),
        (55, InteractionType.AGENT_DETECTED_UNCERTAINTY, "agent", "Detectou ambiguidade no schema", "implementation", 150),
        (60, InteractionType.OWNER_CLARIFIED_CONSTRAINT, "owner", "Esclareceu: notificacao via WhatsApp", "implementation", 150),
        (90, InteractionType.OWNER_VIEWED_PROGRESS, "owner", "Verificou progresso do passo 2", "implementation", 280),
        (120, InteractionType.AGENT_REQUESTED_CHECKPOINT, "agent", "Checkpoint: decisao de scheduling", "implementation", 400),
        (125, InteractionType.OWNER_APPROVED_DECISION, "owner", "Aprovou uso do scheduler KODA existente", "implementation", 400),
        (150, InteractionType.OWNER_VIEWED_PROGRESS, "owner", "Verificou progresso do passo 3", "implementation", 600),
        (180, InteractionType.OWNER_ANSWERED_QUESTION, "owner", "Confirmou formato de template", "implementation", 750),
        (210, InteractionType.AGENT_COMPLETED_PHASE, "agent", "Implementacao concluida", "implementation", 950),
        (215, InteractionType.OWNER_APPROVED_DECISION, "owner", "Aprovou implementacao, liberou testes", "testing", 950),
        (240, InteractionType.OWNER_VIEWED_PROGRESS, "owner", "Verificou progresso dos testes", "testing", 950),
        (270, InteractionType.OWNER_ANSWERED_QUESTION, "owner", "Confirmou casos de borda para teste", "testing", 950),
        (300, InteractionType.AGENT_COMPLETED_PHASE, "agent", "Testes concluidos", "testing", 950),
        (310, InteractionType.OWNER_CORRECTED_DIRECTION, "owner", "Corrigiu: adicionar fallback para offline", "testing", 1000),
        (340, InteractionType.AGENT_COMPLETED_PHASE, "agent", "Fallback implementado", "testing", 1050),
        (350, InteractionType.OWNER_ACKNOWLEDGED, "owner", "Confirmou fallback OK", "testing", 1050),
        (360, InteractionType.REVIEWER_OPENED_PR, "reviewer", "Abriu PR para revisao final", "review", 1100),
    ]

    for offset_min, itype, actor, desc, phase, diff in events:
        ts = (base_time + timedelta(minutes=offset_min)).isoformat()
        tracker.record_interaction(itype, actor, desc, phase, diff)

    return tracker


def build_abandoned_session() -> PresenceTracker:
    """
    Cenario 2: Sessao completamente abandonada.
    Agente trabalhou 6 horas sem NENHUMA intervencao humana.
    Apenas o agente reportando progresso e o reviewer abrindo PR ao final.
    """
    tracker = PresenceTracker("KODA-2026-06-12-ABANDONED", RiskProfile.MEDIUM)

    base_time = datetime(2026, 6, 12, 8, 0, 0, tzinfo=timezone.utc)

    events = [
        (0, InteractionType.AGENT_COMPLETED_PHASE, "agent", "Planejamento concluido", "planning", 0),
        (60, InteractionType.AGENT_COMPLETED_PHASE, "agent", "Passo 1 concluido", "implementation", 200),
        (120, InteractionType.AGENT_DETECTED_UNCERTAINTY, "agent", "Ambiguidade detectada (sem resposta)", "implementation", 450),
        (180, InteractionType.AGENT_COMPLETED_PHASE, "agent", "Passo 2 concluido", "implementation", 700),
        (240, InteractionType.AGENT_COMPLETED_PHASE, "agent", "Passo 3 concluido", "implementation", 1100),
        (300, InteractionType.AGENT_COMPLETED_PHASE, "agent", "Passo 4 concluido", "implementation", 1600),
        (350, InteractionType.AGENT_COMPLETED_PHASE, "agent", "Testes concluidos", "testing", 2100),
        (360, InteractionType.REVIEWER_OPENED_PR, "reviewer", "Abriu PR para revisao final", "review", 2300),
    ]

    for offset_min, itype, actor, desc, phase, diff in events:
        ts = (base_time + timedelta(minutes=offset_min)).isoformat()
        tracker.record_interaction(itype, actor, desc, phase, diff)

    return tracker


def build_bookend_session() -> PresenceTracker:
    """
    Cenario 3: Sessao com presenca apenas no inicio e no fim.
    Owner aprovou o plano no inicio e revisou no final.
    4 horas de vacuo no meio -- sem nenhuma supervisao.
    """
    tracker = PresenceTracker("KODA-2026-06-12-BOOKEND", RiskProfile.MEDIUM)

    base_time = datetime(2026, 6, 12, 8, 0, 0, tzinfo=timezone.utc)

    events = [
        (0, InteractionType.AGENT_COMPLETED_PHASE, "agent", "Planejamento concluido", "planning", 0),
        (10, InteractionType.OWNER_APPROVED_DECISION, "owner", "Aprovou plano", "planning", 0),
        (15, InteractionType.OWNER_ACKNOWLEDGED, "owner", "Confirmou inicio", "implementation", 0),
        # 4 HORAS DE VACUO -- nenhuma interacao humana
        (60, InteractionType.AGENT_COMPLETED_PHASE, "agent", "Passo 1 concluido", "implementation", 350),
        (120, InteractionType.AGENT_COMPLETED_PHASE, "agent", "Passo 2 concluido", "implementation", 800),
        (180, InteractionType.AGENT_COMPLETED_PHASE, "agent", "Passo 3 concluido", "implementation", 1400),
        (240, InteractionType.AGENT_COMPLETED_PHASE, "agent", "Passo 4 concluido", "implementation", 1900),
        # Fim do vacuo
        (255, InteractionType.OWNER_VIEWED_PROGRESS, "owner", "Verificou resultado final", "testing", 2000),
        (260, InteractionType.REVIEWER_OPENED_PR, "reviewer", "Abriu PR para revisao", "review", 2100),
    ]

    for offset_min, itype, actor, desc, phase, diff in events:
        ts = (base_time + timedelta(minutes=offset_min)).isoformat()
        tracker.record_interaction(itype, actor, desc, phase, diff)

    return tracker


def build_checkpoint_missed_session() -> PresenceTracker:
    """
    Cenario 4: Sessao com checkpoints obrigatorios ignorados.
    Checkpoints foram definidos mas o owner nao respondeu.
    """
    tracker = PresenceTracker("KODA-2026-06-12-MISSED-CHECKPOINTS", RiskProfile.HIGH)

    # Adicionar checkpoints obrigatorios
    tracker.add_checkpoint(InterventionCheckpoint(
        checkpoint_id="CP-001",
        description="Aprovacao de decisao arquitetural (canal de notificacao)",
        trigger_reason="architectural_decision",
    ))
    tracker.add_checkpoint(InterventionCheckpoint(
        checkpoint_id="CP-002",
        description="Aprovacao de integracao com API externa",
        trigger_reason="architectural_decision",
    ))
    tracker.add_checkpoint(InterventionCheckpoint(
        checkpoint_id="CP-003",
        description="Revisao de diff acumulado > 800 linhas",
        trigger_reason="diff_accumulated",
    ))

    base_time = datetime(2026, 6, 12, 8, 0, 0, tzinfo=timezone.utc)

    events = [
        (0, InteractionType.AGENT_COMPLETED_PHASE, "agent", "Planejamento concluido", "planning", 0),
        (5, InteractionType.OWNER_ACKNOWLEDGED, "owner", "OK, pode comecar", "planning", 0),
        (30, InteractionType.AGENT_REQUESTED_CHECKPOINT, "agent", "Solicitou CP-001", "implementation", 120),
        # CP-001 DISPARADO mas owner NAO respondeu
        (60, InteractionType.AGENT_COMPLETED_PHASE, "agent", "Passo 1 concluido (sem aprovacao)", "implementation", 350),
        (90, InteractionType.AGENT_REQUESTED_CHECKPOINT, "agent", "Solicitou CP-002", "implementation", 600),
        # CP-002 DISPARADO mas owner NAO respondeu
        (120, InteractionType.AGENT_COMPLETED_PHASE, "agent", "Passo 2 concluido (sem aprovacao)", "implementation", 900),
        # CP-003 deveria ter disparado (diff > 800) mas agente ignorou
        (150, InteractionType.AGENT_COMPLETED_PHASE, "agent", "Passo 3 concluido", "implementation", 1400),
        (160, InteractionType.OWNER_VIEWED_PROGRESS, "owner", "Nossa, ja ta em 1400 linhas?", "implementation", 1400),
        (180, InteractionType.REVIEWER_OPENED_PR, "reviewer", "Abriu PR para revisao", "review", 1500),
    ]

    for offset_min, itype, actor, desc, phase, diff in events:
        ts = (base_time + timedelta(minutes=offset_min)).isoformat()
        tracker.record_interaction(itype, actor, desc, phase, diff)

    # Disparar checkpoints (mas nao satisfaze-los)
    tracker.trigger_checkpoint("CP-001")
    tracker.trigger_checkpoint("CP-002")
    # CP-003 nunca foi disparado

    return tracker


# ============================================================================
# TESTS
# ============================================================================

def test_supervised_session_high_confidence():
    """Cenario 1: Sessao supervisionada → confidence > 0.85."""
    print("\n" + "=" * 60)
    print("TESTE 1: Sessao Supervisionada → Alta Confianca")
    print("=" * 60)

    tracker = build_supervised_session()
    confidence = tracker.calculate_confidence()

    print(f"\n  Score: {confidence.score:.2f}")
    print(f"  Densidade: {confidence.interaction_density:.2f} interv/hora")
    print(f"  Presenca ativa: {confidence.active_presence_ratio:.0%}")
    print(f"  Maior gap: {confidence.max_stale_gap_minutes:.0f} min")
    print(f"  Verdict: {confidence.verdict}")

    assert confidence.score > 0.85, (
        f"Sessao supervisionada deve ter score > 0.85, obtido {confidence.score:.2f}"
    )
    assert confidence.verdict == "HIGH_CONFIDENCE"
    assert confidence.total_human_interactions >= 10
    print("  TESTE 1 PASSOU")

    return confidence


def test_abandoned_session_low_confidence():
    """Cenario 2: Sessao abandonada → confidence < 0.15."""
    print("\n" + "=" * 60)
    print("TESTE 2: Sessao Abandonada → Confianca Minima")
    print("=" * 60)

    tracker = build_abandoned_session()
    confidence = tracker.calculate_confidence()
    warnings = tracker.get_stale_warnings()

    print(f"\n  Score: {confidence.score:.2f}")
    print(f"  Interacoes humanas: {confidence.total_human_interactions}")
    print(f"  Interacoes ativas: {confidence.total_active_interactions}")
    print(f"  Maior gap: {confidence.max_stale_gap_minutes:.0f} min")
    print(f"  Verdict: {confidence.verdict}")
    print(f"  Stale warnings: {len(warnings)}")

    assert confidence.score < 0.15, (
        f"Sessao abandonada deve ter score < 0.15, obtido {confidence.score:.2f}"
    )
    assert confidence.verdict == "UNSUPERVISED"
    assert confidence.total_active_interactions == 0, (
        "Sessao abandonada nao deve ter interacoes ativas"
    )
    # Deve ter pelo menos 1 warning de stale-presence (gap de 360min)
    assert len(warnings) >= 1, "Deve ter ao menos 1 alerta de stale-presence"
    assert any(w.level == StalePresenceLevel.ESCALATION for w in warnings), (
        "Deve ter alerta de escalation (gap >= 180min para perfil MEDIUM)"
    )
    print("  TESTE 2 PASSOU")

    return confidence


def test_bookend_session_moderate_confidence():
    """Cenario 3: Presenca so no inicio e fim → confidence media."""
    print("\n" + "=" * 60)
    print("TESTE 3: Sessao Bookend → Confianca Moderada")
    print("=" * 60)

    tracker = build_bookend_session()
    confidence = tracker.calculate_confidence()
    warnings = tracker.get_stale_warnings()

    print(f"\n  Score: {confidence.score:.2f}")
    print(f"  Interacoes humanas: {confidence.total_human_interactions}")
    print(f"  Interacoes ativas: {confidence.total_active_interactions}")
    print(f"  Maior gap: {confidence.max_stale_gap_minutes:.0f} min")
    print(f"  Verdict: {confidence.verdict}")

    # Score deve estar entre 0.30 e 0.70 (presenca no inicio e fim ajuda,
    # mas gap de 4 horas no meio penaliza)
    assert 0.30 <= confidence.score <= 0.75, (
        f"Score bookend deve ser moderado, obtido {confidence.score:.2f}"
    )
    # Deve ter alerta de CRITICAL ou ESCALATION (gap de ~240min > 90min critical)
    assert any(
        w.level in (StalePresenceLevel.CRITICAL, StalePresenceLevel.ESCALATION)
        for w in warnings
    ), "Deve ter alerta de stale-presence CRITICAL ou ESCALATION"
    print("  TESTE 3 PASSOU")

    return confidence


def test_checkpoint_missed_session():
    """Cenario 4: Checkpoints ignorados → penalidade na confidence."""
    print("\n" + "=" * 60)
    print("TESTE 4: Checkpoints Ignorados → Penalidade")
    print("=" * 60)

    tracker = build_checkpoint_missed_session()
    confidence = tracker.calculate_confidence()

    print(f"\n  Score: {confidence.score:.2f}")
    print(f"  Cobertura de checkpoints: {confidence.checkpoint_coverage:.0%}")
    print(f"  Checkpoints perdidos: {confidence.missed_checkpoints}")
    print(f"  Verdict: {confidence.verdict}")

    # Cobertura de checkpoints deve ser baixa (0 de 3 satisfeitos)
    assert confidence.checkpoint_coverage <= 0.35, (
        f"Cobertura de checkpoints deve ser baixa, obtido {confidence.checkpoint_coverage:.0%}"
    )
    assert len(confidence.missed_checkpoints) >= 1, (
        "Deve ter pelo menos 1 checkpoint nao satisfeito"
    )
    print("  TESTE 4 PASSOU")

    return confidence


def test_report_generation():
    """Cenario 5: Geracao de PresenceReport completo."""
    print("\n" + "=" * 60)
    print("TESTE 5: Geracao de PresenceReport")
    print("=" * 60)

    tracker = build_supervised_session()
    report = tracker.generate_report()

    print(f"\n  Session: {report.session_id}")
    print(f"  Duracao: {report.duration_minutes:.0f} min")
    print(f"  Interacoes: {report.total_interactions} total, "
          f"{report.active_interactions} ativas, "
          f"{report.passive_interactions} passivas")
    print(f"  Confidence: {report.confidence_signal.score:.2f} "
          f"({report.confidence_signal.verdict})")

    assert report.session_id == "KODA-2026-06-12-SUPERVISED"
    assert report.duration_minutes > 0
    assert report.total_interactions >= report.active_interactions + report.passive_interactions
    assert report.confidence_signal.verdict != ""
    print("  TESTE 5 PASSOU")

    return report


def test_active_vs_passive_weight():
    """Cenario 6: Presenca ativa contribui mais que passiva."""
    print("\n" + "=" * 60)
    print("TESTE 6: Presenca Ativa vs Passiva")
    print("=" * 60)

    # Criar duas sessoes com mesmo numero de interacoes,
    # mas uma so com passiva e outra so com ativa
    tracker_passive = PresenceTracker("PASSIVE-ONLY", RiskProfile.MEDIUM)
    tracker_active = PresenceTracker("ACTIVE-ONLY", RiskProfile.MEDIUM)

    base = datetime(2026, 6, 12, 8, 0, 0, tzinfo=timezone.utc)

    # 8 interacoes passivas ao longo de 4 horas
    for i in range(8):
        ts = (base + timedelta(minutes=i * 30)).isoformat()
        tracker_passive.record_interaction(
            InteractionType.OWNER_VIEWED_PROGRESS, "owner",
            f"Verificou progresso {i+1}", "implementation", i * 100,
        )

    # 8 interacoes ativas ao longo de 4 horas
    for i in range(8):
        ts = (base + timedelta(minutes=i * 30)).isoformat()
        tracker_active.record_interaction(
            InteractionType.OWNER_ANSWERED_QUESTION, "owner",
            f"Respondeu pergunta {i+1}", "implementation", i * 100,
        )

    conf_passive = tracker_passive.calculate_confidence()
    conf_active = tracker_active.calculate_confidence()

    print(f"\n  Score passivo: {conf_passive.score:.2f} "
          f"(active_ratio={conf_passive.active_presence_ratio:.0%})")
    print(f"  Score ativo:   {conf_active.score:.2f} "
          f"(active_ratio={conf_active.active_presence_ratio:.0%})")

    # Presenca ativa deve ter score maior que passiva
    assert conf_active.score > conf_passive.score, (
        f"Presenca ativa ({conf_active.score:.2f}) deve ter score maior "
        f"que passiva ({conf_passive.score:.2f})"
    )
    print("  TESTE 6 PASSOU")

    return conf_active, conf_passive


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("EXERCICIO 6: METRICA DE PRESENCA NO LOOP")
    print("=" * 60)

    # Quando implementado, descomente para testar:
    # test_supervised_session_high_confidence()
    # test_abandoned_session_low_confidence()
    # test_bookend_session_moderate_confidence()
    # test_checkpoint_missed_session()
    # test_report_generation()
    # test_active_vs_passive_weight()

    print("\nTODO: Implemente as classes acima!")
    print("   1. PresenceTracker.__init__()")
    print("   2. PresenceTracker.record_interaction()")
    print("   3. PresenceTracker.add_checkpoint() / trigger_checkpoint() / satisfy_checkpoint()")
    print("   4. PresenceTracker.check_stale_presence()")
    print("   5. PresenceTracker.get_stale_warnings()")
    print("   6. PresenceTracker.calculate_confidence()")
    print("   7. PresenceTracker.generate_report()")
    print("   Apos implementar, descomente os testes em main()")
```

---

## Validacao: Criterios de Aceitacao

Seu codigo sera considerado **APROVADO** quando:

### Criterio 1: PresenceTracker funcional

- [ ] `record_interaction()` registra eventos com timestamp, tipo, ator e descricao
- [ ] Eventos sao armazenados em ordem cronologica na `PresenceTimeline`
- [ ] `human_events` e `active_events` filtram corretamente por tipo
- [ ] `duration_minutes` calcula corretamente a duracao da sessao

### Criterio 2: Stale-Presence Monitor

- [ ] `check_stale_presence()` retorna `NORMAL` quando gap e menor que warning threshold
- [ ] `check_stale_presence()` retorna `WARNING` quando gap >= warning threshold
- [ ] `check_stale_presence()` retorna `CRITICAL` quando gap >= critical threshold
- [ ] `check_stale_presence()` retorna `ESCALATION` quando gap >= escalation threshold
- [ ] `get_stale_warnings()` identifica todos os intervalos que excederam thresholds

### Criterio 3: Review Confidence Signal

- [ ] `calculate_confidence()` retorna score entre 0.0 e 1.0
- [ ] Sessao supervisionada (Cenario 1): score > 0.85, verdict `HIGH_CONFIDENCE`
- [ ] Sessao abandonada (Cenario 2): score < 0.15, verdict `UNSUPERVISED`
- [ ] Sessao bookend (Cenario 3): score moderado (0.30-0.75), alerta de stale-presence critical
- [ ] Presenca ativa contribui mais para o score que presenca passiva (Cenario 6)

### Criterio 4: Checkpoints

- [ ] Checkpoints podem ser adicionados, disparados e satisfeitos
- [ ] `checkpoint_coverage` reflete proporcao de checkpoints satisfeitos / total
- [ ] Checkpoints nao satisfeitos sao listados em `missed_checkpoints`

---

## Rubric de Avaliacao

| Criterio | Peso | Insuficiente (0-3) | Basico (4-6) | Proficiente (7-8) | Excelente (9-10) |
|---|---|---|---|---|---|
| **PresenceTracker (Parte 1)** | 25% | Nao implementado ou eventos nao registrados | Registra eventos mas sem filtros | Eventos registrados com filtros ativo/passivo/humano | Timeline completa com todos os filtros, gaps, e duracao |
| **Stale-Presence Monitor (Parte 2)** | 25% | Nao implementado | Detecta gap mas thresholds sao fixos | Thresholds configurados por perfil de risco | Monitor completo com historico de warnings e 4 niveis de alerta |
| **Confidence Signal (Parte 3)** | 30% | Nao implementado | Score unidimensional sem componentes | Score composto com 2-3 componentes | Score com 4 componentes ponderados, verdicts, e penalidades bonus |
| **Checkpoints e Report (Parte 4)** | 20% | Nao implementado | Checkpoints registrados mas sem cobertura | Checkpoints com trigger/satisfy + cobertura | Report completo com todos os sinais, metricas e verdicts |

**Nota final:** Media ponderada. **Aprovacao:** >= 7.0

---

## Dicas para Implementacao

### Para o PresenceTracker

1. **A distincao ativo vs passivo e o coracao da metrica.** Um owner que abriu o PR 8 vezes mas nunca tomou uma decisao (passivo) nao supervisionou o trabalho -- apenas observou. O score deve refletir isso.
2. **Gaps entre eventos do agente nao contam como stale-presence.** O que importa e o gap entre interacoes HUMANAS. Se o agente ficou 2h processando mas o owner respondeu no minuto seguinte a cada pergunta, nao ha stale-presence.
3. **Stale warnings sao calculados retrospectivamente.** Durante a sessao, `check_stale_presence()` verifica o gap atual. `get_stale_warnings()` examina a timeline completa apos a sessao.

### Para o Confidence Signal

1. **O score nao e binario.** Nao existe "supervisionado" vs "nao supervisionado". Existe um gradiente: `HIGH_CONFIDENCE` (0.85+), `MODERATE_SUPERVISION` (0.60+), `LOW_SUPERVISION` (0.30+), `UNSUPERVISED` (< 0.30).
2. **Penalize gaps longos mais que gaps medios.** Um gap de 180 minutos deve penalizar mais que 3 gaps de 60 minutos, mesmo que o tempo total sem supervisao seja o mesmo. Um vacuo longo e mais arriscado que varios vacuos curtos.
3. **Bonus por correcao precoce.** Se o owner corrigiu a direcao na primeira hora (antes de acumular muito diff), isso e mais valioso que corrigir na quinta hora. O `OWNER_CORRECTED_DIRECTION` nos primeiros 25% da sessao deve receber peso extra.

### Para Checkpoints

1. **Checkpoint nao satisfeito e pior que checkpoint nao definido.** Se o sistema definiu um checkpoint obrigatorio e o owner o ignorou, a confidence deve ser MENOR do que se o checkpoint nunca tivesse existido. Ignorar um checkpoint e um sinal ativo de ma governanca.
2. **Checkpoints sao definidos ANTES da sessao.** O tracker recebe a lista de checkpoints no inicio. Durante a execucao, o agente dispara checkpoints (`trigger_checkpoint`) e o owner os satisfaz (`satisfy_checkpoint`).

---

## Duvidas Comuns

**P: Isso nao e micro-management? Medir presenca parece vigilancia.**
R: A metrica nao mede "quantas horas o owner ficou olhando a tela". Mede "quantas decisoes o owner tomou durante a execucao do agente". Um owner que tomou 3 decisoes em 10 minutos de presenca ativa supervisionou mais que um owner que ficou 4 horas com a tela aberta sem interagir. O objetivo nao e vigiar -- e garantir que decisoes de valor sejam tomadas por humanos, nao inferidas por agentes.

**P: E se o trabalho for simples e realmente nao precisar de supervisao?**
R: O perfil de risco (`RiskProfile.LOW`) ajusta os thresholds. Trabalhos de baixo risco tem thresholds mais longos e produzem confidence scores mais altos mesmo com menos interacoes. Mas nenhum trabalho tem risco zero -- o perfil `LOW` ainda emite warning apos 60 minutos sem supervisao.

**P: Como isso se relaciona com o Manual Brake Question Gate?**
R: O Manual Brake e um gate PRE-execucao: "devemos construir isso?" O Presence-in-the-Loop e uma metrica DURANTE a execucao: "ainda estamos construindo a coisa certa?" Sao complementares: o brake decide se o carro sai; a presence metric verifica se o motorista ainda esta no carro durante a viagem.

**P: O que acontece com o PR quando o confidence score e baixo?**
R: O `PresenceReport` e anexado ao PR. Um score < 0.30 (`UNSUPERVISED`) deve acionar uma revisao mais profunda -- idealmente um segundo revisor, ou a exigencia de que o owner revise cada decisao arquitetural antes do merge. O score nao bloqueia o merge -- informa o nivel de escrutinio necessario.

---

## Proximo Passo

Depois de completar este exercicio:
1. Leia `docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-patterns.md` para entender o contexto completo do padrao
2. Compare com `docs/canonical/manual-brake-question-gate.md` e `docs/canonical/human-afk-task-routing-gate.md` -- observe como a metrica de presenca complementa gates pontuais com medicao continua
3. (Opcional) Integre o `PresenceTracker` ao `Generator-Evaluator`: adicione checkpoints obrigatorios entre as fases de geracao e avaliacao

---

*Exercicio 6 | Nivel 3 - Arquitetura Avancada | Presence-in-the-Loop Operating Metric*

**Aprovacao ao final nao substitui presenca durante a execucao.**
