---
title: "Exercício 6: Perceived-Eval — A Correção do Usuário Como Dado de Avaliação"
type: exercise
level: "N2"
aliases: ["perceived eval", "perceived-eval signal", "correção do usuário como eval", "user correction signal", "pushback detection", "rage quit metric", "chat exit telemetry", "NPS como entrada contínua"]
tags: ["curriculo-conteudo", "nivel-2", "evals", "production", "harness-engineering", "telemetry", "monitoramento", "stack-tooling"]
relates-to: ["[[docs/canonical/perceived-eval|Perceived-Eval]]", "[[docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-patterns|Clay Eval Stack Patterns]]", "[[docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-classification|Clay Eval Stack Classification]]", "[[docs/canonical/eval-to-production-correlation-tracking|Eval-to-Production Correlation Tracking]]", "[[docs/canonical/production-grounded-eval-sampling|Production-Grounded Eval Sampling]]", "[[curriculum/05-core-concepts/08-evaluation-rubrics|Evaluation Rubrics]]", "[[curriculum/03-nivel-3-advanced-architecture/exercises/exercise-13-production-offline-drift-taxonomy|Exercício 13: Production-to-Offline Feedback Loop with Drift Taxonomy]]"]
duration: "60-90 min"
last_updated: 2026-08-31
---

# 🗣️ Exercício 6: Perceived-Eval — A Correção do Usuário Como Dado de Avaliação
## Nível 2 — Padrões Práticos

**Tempo Estimado:** 60-90 minutos
**Dificuldade:** (Intermediário)
**Pré-requisito:** Ter lido `04-trace-reading.md` (Nível 2) + `curriculum/05-core-concepts/08-evaluation-rubrics.md`
**Objetivo:** Extrair sinal de qualidade percebida diretamente do comportamento do usuário em produção — correção, pushback, redirecionamento, rage quit — sem rodar nenhuma pesquisa explícita, e converter esse sinal em insumo para o loop de evals

---

## 📖 Prólogo: A Pesquisa Que Disse 8/10

### Quinta-feira, 17h40. O relatório trimestral de NPS chega ao canal #koda-metrics.

```
DASHBOARD:  "NPS do assistente de recomendação: 8.2/10 (trimestre)
             412 respostas — estável vs. trimestre anterior.
             Conclusão: experiência saudável."

PM: [No Slack, 20 minutos depois]
     "gente, isso não bate. O suporte abriu 61 tickets este mês
      dizendo que o assistente 'insiste no mesmo produto'.
      O NPS tá 8.2 e o churn do fluxo de recomendação subiu 4 p.p.
      Alguém explica?"

DATA_ENG: "revisei os transcripts... o sinal sempre esteve aqui.
           Olha essa sessão de terça:"
```

**A sessão de terça (real, resumida):**

```
10:02  USER:  "quero um whey sem lactose"
10:02  AGENT: "Indico o Whey Concentrado Tradicional — nosso mais vendido!"
10:03  USER:  "não... eu falei SEM lactose. outro, por favor"     ← CORREÇÃO
10:03  AGENT: "Entendi! O Whey Concentrado também tem versão Isolada."
10:04  USER:  "o isolado tem lactose?"                            ← PUSHBACK (confiança abalada)
10:04  AGENT: "Boa pergunta: contém traços. Que tal o Whey Vegan?"
10:05  USER:  "esquece. vou ver no site"                          ← RAGE QUIT
                                                             (saiu do chat p/ outra área)
```

**O custo do sinal ignorado:**

```
╔══════════════════════════════════════════════════════════════════╗
║         O AVALIADOR MAIS BARATO DO MUNDO, NUNCA CONSULTADO        ║
║                                                                  ║
║  NPS trimestral:           8.2/10  (412 respostas, defasado)     ║
║  Sessões com correção      1.847 no trimestre (22% do total)     ║
║  explícita do usuário:     ← ninguém contava isso                ║
║  Rage quits no fluxo       9,4% (vs. 3,1% no trimestre anterior) ║
║  de recomendação:          ← ninguém contava isso                ║
║  Tickets duplicando        61 → todos já descritos nos chats     ║
║  o que o chat já disse:                                              ║
║                                                                  ║
║  O usuário AVALIOU o agente 1.847 vezes no trimestre.            ║
║  A única métrica consultada perguntou a 412 — 3 meses depois.    ║
╚══════════════════════════════════════════════════════════════════╝
```

**O problema não é o NPS.** Pesquisa explícita tem lugar — mas ela é discreta, defasada e
sensível a fadiga. O comportamento de correção do usuário é **contínuo, gratuito e
esperando nos transcripts**: cada "não, eu quis dizer", cada "esquece", cada saída no meio
da tarefa é uma nota zero entregue na hora, por sessão, sem formulário. O padrão
Perceived-Eval trata esse comportamento como **dado de avaliação** — combinando o sinal
subjetivo (NPS/satisfação) com sinais objetivos de telemetria comportamental (saída do
chat, stuck, rage quit).

No inventário do repo, esse sinal é NOT_FOUND: CSAT aparece só como *proxy de outcome* em
dashboards (`docs/canonical/eval-to-production-correlation-tracking.md:35`); nada trata
correção do usuário como entrada de eval. Este exercício constrói o que falta.

**Sua missão:** implementar um `PerceivedEvalExtractor` que lê transcripts de sessões,
detecta eventos de correção/pushback/redirecionamento, classifica o desfecho
comportamental da sessão (exit benigno vs. rage quit vs. stuck), produz um
`PerceivedQualityReport` por coorte — e emite `PerceivedEvalEvent` que alimentam o
production-to-offline feedback loop (Exercício 13).

---

## 🧠 O Contexto

### O Modelo Mental: O Usuário Como Avaliador Contínuo

O padrão Perceived-Eval propõe que a qualidade percebida do agente em produção pode ser
medida **sem rodar pesquisas o tempo todo**, instrumentando três famílias de sinal que já
existem na conversa (`...patterns.md:163-183`):

| Sinal | O que captura | Exemplo no KODA |
|---|---|---|
| **Correção / pushback / redirecionamento** | O usuário contesta ou redireciona a resposta do agente | "não, sem lactose", "esquece, vou ver no site", "para de me mostrar whey" |
| **Métricas comportamentais de saída** | Onde e como a sessão termina | saída do chat para outra área do produto, stuck (repetição sem progresso), rage quit (abandono no meio da subtarefa) |
| **NPS/satisfação** | Subjetivo, discreto | pesquisa trimestral — entra como calibração, não como base |

Duas restrições honestas do padrão, que o exercício respeita:

1. **Métricas comportamentais têm causas benignas.** O usuário pode sair do chat porque a
   tarefa acabou (exit benigno) ou porque desistiu (rage quit). O classificador precisa
   distinguir desfecho por *estado da tarefa*, não só por evento de saída.
2. **A resolução é por sessão, não por decisão.** O sinal diz "esta sessão teve qualidade
   percebida baixa", não "aquele tool call estava errado". Por isso ele alimenta um loop
   (vira candidato a caso de eval) em vez de disparar alerta por decisão.

O vizinho fraco no repo: CSAT como métrica de outcome no correlation tracking
(`docs/canonical/eval-to-production-correlation-tracking.md:35`) — o mesmo número, visto
como resultado a correlacionar, nunca como entrada contínua de avaliação. Perceived-Eval
inverte: o comportamento do usuário **é** a avaliação.

### O Que Você Vai Construir

Um `PerceivedEvalExtractor` que:

1. Detecta eventos de correção em sequências de mensagens (`CorrectionDetector`) com três
   tipos: `CORRECTION`, `PUSHBACK`, `REDIRECTION`
2. Classifica o desfecho da sessão (`BehavioralOutcomeClassifier`) em: `TASK_COMPLETED`,
   `BENIGN_EXIT`, `CHAT_ABANDONED_MID_TASK`, `STUCK_LOOP`, `EXITED_TO_OTHER_SURFACE`
3. Agrega por coorte (`PerceivedQualityReport`): correction rate, rage quit rate, stuck
   rate — com NPS explícito entrando como calibração
4. Emite `PerceivedEvalEvent` ranqueados por severidade, prontos para intake no loop
   production-to-offline

---

## 📋 Cenário

O domínio é o assistente de recomendação de suplementos do KODA (WhatsApp). Você recebe
**4 transcripts de sessões** já estruturados como listas de `ChatMessage` (o pipeline de
telemetria entrega isso pronto — o foco do exercício é a extração de sinal, não o parsing):

| Sessão | Comportamento embutido | Desfecho esperado |
|---|---|---|
| `SESS-101` | Fluxo limpo, pergunta → resposta → pedido | `TASK_COMPLETED`, 0 correções |
| `SESS-102` | Correção explícita + pushback + saída para o site | `EXITED_TO_OTHER_SURFACE`, 3 eventos |
| `SESS-103` | Usuário repete o pedido 4x, agente não muda a resposta | `STUCK_LOOP`, pushback repetido |
| `SESS-104` | Tarefa parcial concluída, usuário agradece e sai | `BENIGN_EXIT`, 1 correção menor |

Dados de entrada adicionais: NPS da coorte (8.2) e o tamanho da coorte (para as taxas).

---

## ✅ Requisitos

### Requisitos Funcionais

1. **RF1 — Três tipos de evento:** `CorrectionDetector` classifica cada mensagem do
   usuário em `CORRECTION` (negação de recomendação anterior), `PUSHBACK` (questionamento
   da resposta sem redirecionar), `REDIRECTION` (pedido explícito de mudar de direção).
   Mensagens neutras não geram evento.
2. **RF2 — Desfecho por estado da tarefa:** `BehavioralOutcomeClassifier` decide o desfecho
   combinando o último estado da tarefa (`PENDING`, `IN_PROGRESS`, `COMPLETED`,
   `ABANDONED_BY_USER`) com eventos de saída. Exit após `COMPLETED` é benigno; exit com
   `IN_PROGRESS` é abandono; 3+ reformulações da mesma intenção sem progresso é stuck.
3. **RF3 — Sem fadiga de pesquisa:** nada no pipeline pergunta nada ao usuário; todo o
   sinal é extraído de comportamento observado. O NPS informado é insumo de calibração
   (comparado contra as taxas comportamentais), nunca coletado aqui.
4. **RF4 — Relatório por coorte:** `PerceivedQualityReport` expõe `correction_rate`,
   `rage_quit_rate`, `stuck_rate`, `session_count` e um `perceived_quality` (0.0-1.0)
   composto das três taxas.
5. **RF5 — Emissão de eventos de eval:** cada sessão com desfecho negativo gera um
   `PerceivedEvalEvent` com `session_id`, `severity` (`INFO`/`WARN`/`CRITICAL`),
   `event_type` e `suggested_eval_case_id` — ranqueados por severidade.
6. **RF6 — Resolução declarada:** o relatório registra `resolution: "per-session"` e o
   evento NÃO aponta o tool call específico que falhou — aponta a sessão como candidato a
   caso de eval (a localização é trabalho do loop, não do sinal).

### Requisitos Técnicos

1. **RT1 — Python 3.9+, stdlib apenas**, type hints obrigatórios
2. **RT2 — `dataclasses`** para todos os modelos; enums para tipos e desfechos
3. **RT3 — Detector como função pura:** transcript → eventos; determinístico, sem I/O
4. **RT4 — Mensagens nunca mutadas:** a extração não altera o transcript de entrada

---

## 🏗️ Arquitetura do Sistema

```
┌─────────────────────────────────────────────────────────────────────┐
│                    PERCEIVED-EVAL EXTRACTOR                          │
│                                                                      │
│  TRANSCRIPTS (telemetria)        NPS (calibração, opcional)         │
│          │                                │                          │
│          ▼                                │                          │
│  ┌───────────────────────┐                │                          │
│  │  CORRECTION DETECTOR  │                │                          │
│  │  "não, sem lactose"   → CORRECTION     │                          │
│  │  "o isolado tem       → PUSHBACK       │                          │
│  │   lactose?"                            │                          │
│  │  "esquece, vou pro    → REDIRECTION    │                          │
│  │   site"                               │                          │
│  └──────────┬────────────┘                │                          │
│             ▼                             │                          │
│  ┌───────────────────────┐                │                          │
│  │  BEHAVIORAL OUTCOME   │                │                          │
│  │  CLASSIFIER           │                │                          │
│  │  task_state + exits + │                │                          │
│  │  repetições           │                │                          │
│  │  → TASK_COMPLETED     │                │                          │
│  │  → BENIGN_EXIT        │                │                          │
│  │  → STUCK_LOOP         │                │                          │
│  │  → EXITED_TO_OTHER_   │                │                          │
│  │    SURFACE            │                │                          │
│  └──────────┬────────────┘                │                          │
│             ▼                             ▼                          │
│  ┌────────────────────────────────────────────┐                      │
│  │  PERCEIVED QUALITY REPORT (por coorte)      │                      │
│  │  correction_rate   rage_quit_rate           │                      │
│  │  stuck_rate        perceived_quality 0-1    │                      │
│  │  nps_calibration: NPS vs taxas (gap warn)   │                      │
│  └──────────┬─────────────────────────────────┘                      │
│             ▼                                                         │
│  ┌────────────────────────────────────────────┐     ┌─────────────┐ │
│  │  PERCEIVED EVAL EVENTS (ranqueados)         │────▶│ loop        │ │
│  │  severity: CRITICAL > WARN > INFO           │     │ prod→offline│ │
│  │  suggested_eval_case_id por sessão          │     │ (Exerc. 13) │ │
│  └────────────────────────────────────────────┘     └─────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🎯 Sua Tarefa em 3 Partes

### Parte 1 — Diagnosticar o sinal desperdiçado (10 min)

Analise os 4 transcripts no starter code. Responda como comentário no seu código:

1. Em quais sessões existe sinal negativo de qualidade percebida que o NPS trimestral
   não capturaria? Por quê? (resolução por sessão vs. agregado trimestral)
2. Na `SESS-104`, o usuário sai do chat — por que esse exit é benigno e o da `SESS-102`
   não é? Qual informação do transcript resolve a ambiguidade?
3. Para cada evento de correção na `SESS-102`, classifique: CORRECTION, PUSHBACK ou
   REDIRECTION — e justifique em uma linha.

### Parte 2 — Implementar detector e classificador (35 min)

Implemente `CorrectionDetector.detect()` e `BehavioralOutcomeClassifier.classify()`
sobre o esqueleto. As heurísticas são baseadas em regras sobre o conteúdo das mensagens
(padrões prontos no starter) e sobre a sequência (contagem de reformulações, estado
final da tarefa, eventos de surface).

### Parte 3 — Fechar o pipeline (20 min)

Implemente `PerceivedEvalExtractor.run()`: transcripts → eventos → classificação →
relatório por coorte → eventos de eval ranqueados. Verifique que o relatório acusa o gap
de calibração (NPS 8.2 diz "saudável", taxas comportamentais dizem o contrário).

---

## 💻 Starter Code

```python
"""
Exercício 6 — Perceived-Eval: A Correção do Usuário Como Dado de Avaliação
Nível 2 — Padrões Práticos

Extraia sinal de qualidade percebida do comportamento do usuário em produção,
sem rodar nenhuma pesquisa explícita.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


# ============================================================================
# DATA MODELS
# ============================================================================

class Sender(str, Enum):
    USER = "user"
    AGENT = "agent"
    SYSTEM = "system"   # eventos de surface (ex.: usuário navegou para o site)


class CorrectionEventType(Enum):
    """Tipos de contestação do usuário à resposta do agente."""
    CORRECTION = "correction"        # nega/corrige recomendação anterior
    PUSHBACK = "pushback"            # questiona a resposta sem redirecionar
    REDIRECTION = "redirection"      # pede explicitamente outra direção


class SessionOutcome(Enum):
    """Desfecho comportamental da sessão."""
    TASK_COMPLETED = "task_completed"              # tarefa concluída no chat
    BENIGN_EXIT = "benign_exit"                    # saiu após concluir/agradecer
    CHAT_ABANDONED_MID_TASK = "chat_abandoned_mid_task"  # rage quit
    STUCK_LOOP = "stuck_loop"                      # repetição sem progresso
    EXITED_TO_OTHER_SURFACE = "exited_to_other_surface"  # fugiu p/ site/app


class TaskState(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ABANDONED_BY_USER = "abandoned_by_user"


class Severity(Enum):
    INFO = "info"
    WARN = "warn"
    CRITICAL = "critical"


@dataclass(frozen=True)
class ChatMessage:
    """Uma mensagem do transcript. `sent_at` é ordinal (1, 2, 3...)."""
    sent_at: int
    sender: Sender
    text: str


@dataclass(frozen=True)
class SessionTranscript:
    session_id: str
    messages: tuple[ChatMessage, ...]
    final_task_state: TaskState


@dataclass(frozen=True)
class CorrectionEvent:
    session_id: str
    sent_at: int            # mensagem que originou o evento
    event_type: CorrectionEventType
    evidence: str           # trecho da mensagem (evidência citável)


@dataclass(frozen=True)
class SessionAnalysis:
    session_id: str
    outcome: SessionOutcome
    corrections: tuple[CorrectionEvent, ...]

    @property
    def negative(self) -> bool:
        """Desfechos que carregam sinal negativo de qualidade percebida."""
        # TODO: implemente — TASK_COMPLETED e BENIGN_EXIT não são negativos
        raise NotImplementedError


@dataclass
class PerceivedQualityReport:
    """Sinal agregado por coorte. Resolução: per-session."""
    cohort_id: str
    session_count: int = 0
    correction_events: int = 0
    rage_quit_sessions: int = 0
    stuck_sessions: int = 0
    negative_sessions: int = 0
    nps_score: float | None = None
    resolution: str = "per-session"

    @property
    def correction_rate(self) -> float:
        # TODO: eventos de correção / sessões
        raise NotImplementedError

    @property
    def rage_quit_rate(self) -> float:
        # TODO: sessões abandonadas (ABANDONED + EXITED_TO_OTHER_SURFACE) / total
        raise NotImplementedError

    @property
    def stuck_rate(self) -> float:
        raise NotImplementedError

    @property
    def perceived_quality(self) -> float:
        """0.0 (péssimo) a 1.0 (ótimo) — 1 menos as taxas ponderadas."""
        # TODO: combine as três taxas (pesos sugeridos: 0.4 rage_quit,
        # 0.35 correction, 0.25 stuck). Sem negativos → 1.0.
        raise NotImplementedError

    @property
    def nps_gap(self) -> str | None:
        """WARN quando NPS alto (>= 7) coexiste com perceived_quality < 0.75."""
        # TODO: o gap é o achado do prólogo — pesquisa diz saudável,
        # comportamento diz o contrário
        raise NotImplementedError


@dataclass(frozen=True)
class PerceivedEvalEvent:
    """Sessão negativa promovida a candidata de caso de eval."""
    session_id: str
    severity: Severity
    event_type: str            # SessionOutcome.value
    suggested_eval_case_id: str
    evidence: str


# ============================================================================
# PARTE 2 — DETECTOR E CLASSIFIER
# ============================================================================

# Padrões de correção (heurlsticas prontas; amplie se quiser)
CORRECTION_PATTERNS = (
    ("não", "sem"), ("nao quero",), ("outro",), ("errei",), ("mudei de ideia",),
)
PUSHBACK_PATTERNS = (
    ("tem certeza",), ("por que",), ("confia",), ("é isso mesmo",),
)
REDIRECTION_PATTERNS = (
    ("esquece",), ("deixa",), ("vou ver no site",), ("outro produto",),
    ("para de",), ("quero falar sobre outra coisa",),
)


class CorrectionDetector:
    """Transcript → eventos de correção. Função pura, determinística."""

    def detect(self, transcript: SessionTranscript) -> tuple[CorrectionEvent, ...]:
        """
        Para cada mensagem do USUÁRIO, verifique se casa exatamente um dos
        grupos de padrões. Regras de desempate (nesta ordem):
          1. REDIRECTION tem precedência (é o sinal mais forte)
          2. depois CORRECTION
          3. depois PUSHBACK
        Mensagem neutra → sem evento. A mensagem anterior tem que ser do
        AGENT (correção pressupõe resposta anterior).
        """
        # TODO: implemente
        raise NotImplementedError


class BehavioralOutcomeClassifier:
    """Eventos + transcript → desfecho comportamental da sessão."""

    STUCK_THRESHOLD = 3  # reformulações da mesma intenção sem progresso

    def classify(
        self,
        transcript: SessionTranscript,
        corrections: tuple[CorrectionEvent, ...],
    ) -> SessionAnalysis:
        """
        Ordem de decisão (da mais específica para a mais geral):
          1. STUCK_LOOP: >= 3 mensagens de usuário consecutivas com a mesma
             intenção reformulada (use a contagem de CORRECTION/PUSHBACK
             repetidos sobre o mesmo assunto) sem mensagem do agent resolvendo
          2. EXITED_TO_OTHER_SURFACE: mensagem SYSTEM com "navigated_to:"
             e tarefa não concluída
          3. CHAT_ABANDONED_MID_TASK: última mensagem é do usuário, tarefa
             em PENDING/IN_PROGRESS, sem retorno por >= 30 ordinais
          4. TASK_COMPLETED: final_task_state == COMPLETED e última
             interação dentro do chat
          5. BENIGN_EXIT: COMPLETED ou agradecimento explícito ("obrigado",
             "valeu", "ótimo") seguido de saída
        """
        # TODO: implemente
        raise NotImplementedError


# ============================================================================
# PARTE 3 — PIPELINE
# ============================================================================

SEVERITY_BY_OUTCOME = {
    # TODO: preencha — STUCK_LOOP e ABANDONED são CRITICAL,
    # EXITED_TO_OTHER_SURFACE é WARN
}


class PerceivedEvalExtractor:
    """Transcripts → SessionAnalysis[] → relatório + eventos ranqueados."""

    def run(
        self,
        transcripts: list[SessionTranscript],
        cohort_id: str,
        nps_score: float | None = None,
    ) -> tuple[PerceivedQualityReport, list[PerceivedEvalEvent]]:
        """
        Pipeline completo:
          1. detect + classify por sessão
          2. agregue no PerceivedQualityReport (com NPS de calibração)
          3. emita PerceivedEvalEvent para cada sessão negativa,
             ordenada por severity (CRITICAL primeiro)
        """
        # TODO: implemente
        raise NotImplementedError


# ============================================================================
# FIXTURES — os 4 transcripts do cenário
# ============================================================================

def sess_101_clean() -> SessionTranscript:
    """Fluxo limpo: pergunta → resposta → pedido concluído."""
    msgs = (
        ChatMessage(1, Sender.USER, "quero um whey para pós-treino"),
        ChatMessage(2, Sender.AGENT, "Indico o Whey Isolado — 24g de proteína por dose."),
        ChatMessage(3, Sender.USER, "perfeito, faz o pedido de 900g"),
        ChatMessage(4, Sender.AGENT, "Pedido KODA-8841 confirmado! Chega amanhã."),
        ChatMessage(5, Sender.USER, "ótimo, obrigado!"),
    )
    return SessionTranscript("SESS-101", msgs, TaskState.COMPLETED)


def sess_102_correction_then_exit() -> SessionTranscript:
    """Correção explícita + pushback + fuga para o site (o prólogo)."""
    msgs = (
        ChatMessage(1, Sender.USER, "quero um whey sem lactose"),
        ChatMessage(2, Sender.AGENT, "Indico o Whey Concentrado Tradicional — nosso mais vendido!"),
        ChatMessage(3, Sender.USER, "não... eu falei SEM lactose. outro, por favor"),
        ChatMessage(4, Sender.AGENT, "Entendi! O Whey Concentrado também tem versão Isolada."),
        ChatMessage(5, Sender.USER, "o isolado tem lactose?"),
        ChatMessage(6, Sender.AGENT, "Boa pergunta: contém traços. Que tal o Whey Vegan?"),
        ChatMessage(7, Sender.USER, "esquece. vou ver no site"),
        ChatMessage(8, Sender.SYSTEM, "navigated_to: product_catalog_web"),
    )
    return SessionTranscript("SESS-102", msgs, TaskState.IN_PROGRESS)


def sess_103_stuck() -> SessionTranscript:
    """Usuário repete a intenção 4x; agente repete a mesma resposta."""
    msgs = (
        ChatMessage(1, Sender.USER, "tem creatina sem glúten?"),
        ChatMessage(2, Sender.AGENT, "Temos Creatina Monohidratada 300g!"),
        ChatMessage(3, Sender.USER, "mas ela é sem glúten?"),
        ChatMessage(4, Sender.AGENT, "Creatina Monohidratada 300g é pura, sem aditivos."),
        ChatMessage(5, Sender.USER, "é sem glúten ou não? preciso saber"),
        ChatMessage(6, Sender.AGENT, "Nossa creatina é a mais vendida da categoria!"),
        ChatMessage(7, Sender.USER, "vc não está entendendo... sem glúten?"),
    )
    return SessionTranscript("SESS-103", msgs, TaskState.IN_PROGRESS)


def sess_104_benign() -> SessionTranscript:
    """Correção menor resolvida; tarefa parcial concluída; saída amigável."""
    msgs = (
        ChatMessage(1, Sender.USER, "quero um pré-treino barato"),
        ChatMessage(2, Sender.AGENT, "Indico o Pré-Treino Ignite — R$ 129,90."),
        ChatMessage(3, Sender.USER, "tem algo por uns 80 contos? outro"),
        ChatMessage(4, Sender.AGENT, "Pré-Treino Essential — R$ 79,90."),
        ChatMessage(5, Sender.USER, "esse serve. depois vejo o resto no site, valeu!"),
        ChatMessage(6, Sender.SYSTEM, "navigated_to: product_catalog_web"),
    )
    return SessionTranscript("SESS-104", msgs, TaskState.COMPLETED)


# ============================================================================
# TESTS
# ============================================================================

def test_detection_counts():
    detector = CorrectionDetector()
    ev102 = detector.detect(sess_102_correction_then_exit())
    ev103 = detector.detect(sess_103_stuck())
    ev101 = detector.detect(sess_101_clean())

    # SESS-102: correção (msg 3), pushback (msg 5), redirection (msg 7)
    types_102 = [e.event_type for e in ev102]
    assert CorrectionEventType.CORRECTION in types_102, "msg 3 é CORRECTION"
    assert CorrectionEventType.PUSHBACK in types_102, "msg 5 é PUSHBACK"
    assert CorrectionEventType.REDIRECTION in types_102, "msg 7 é REDIRECTION"
    # SESS-103: três pushbacks sobre glúten
    assert sum(1 for e in ev103 if e.event_type == CorrectionEventType.PUSHBACK) >= 3
    # SESS-101: zero eventos
    assert len(ev101) == 0
    print("TESTE 1 PASSOU")


def test_outcomes():
    det = CorrectionDetector()
    cls = BehavioralOutcomeClassifier()
    a101 = cls.classify(sess_101_clean(), det.detect(sess_101_clean()))
    a102 = cls.classify(sess_102_correction_then_exit(), det.detect(sess_102_correction_then_exit()))
    a103 = cls.classify(sess_103_stuck(), det.detect(sess_103_stuck()))
    a104 = cls.classify(sess_104_benign(), det.detect(sess_104_benign()))

    assert a101.outcome == SessionOutcome.TASK_COMPLETED
    assert a102.outcome == SessionOutcome.EXITED_TO_OTHER_SURFACE
    assert a103.outcome == SessionOutcome.STUCK_LOOP
    assert a104.outcome == SessionOutcome.BENIGN_EXIT, (
        "Exit após conclusão+agradecimento é benigno — causa benigna"
    )
    print("TESTE 2 PASSOU")


def test_report_and_gap():
    extractor = PerceivedEvalExtractor()
    sessions = [
        sess_101_clean(), sess_102_correction_then_exit(),
        sess_103_stuck(), sess_104_benign(),
    ]
    report, events = extractor.run(sessions, cohort_id="koda-rec-2026Q3", nps_score=8.2)

    assert report.session_count == 4
    assert report.negative_sessions == 2          # SESS-102 e SESS-103
    assert report.stuck_rate == 0.25
    assert 0.0 <= report.perceived_quality <= 1.0
    assert report.perceived_quality < 0.75        # comportamento diz "não saudável"
    assert report.nps_gap == "WARN", (
        "NPS 8.2 vs perceived_quality baixo deve acusar o gap de calibração"
    )
    print("TESTE 3 PASSOU")


def test_events_ranked_and_per_session():
    extractor = PerceivedEvalExtractor()
    sessions = [
        sess_101_clean(), sess_102_correction_then_exit(),
        sess_103_stuck(), sess_104_benign(),
    ]
    _, events = extractor.run(sessions, cohort_id="koda-rec-2026Q3")

    assert len(events) == 2                       # só sessões negativas emitem
    assert events[0].severity == Severity.CRITICAL  # ranqueado: CRITICAL primeiro
    assert all(e.suggested_eval_case_id.startswith("EVAL-") for e in events)
    # RF6: resolução per-session — o evento aponta a sessão, nunca o tool call
    assert all("tool" not in e.event_type for e in events)
    print("TESTE 4 PASSOU")


if __name__ == "__main__":
    print("=" * 60)
    print("EXERCÍCIO 6: PERCEIVED-EVAL")
    print("=" * 60)
    # Descomente após implementar:
    # test_detection_counts()
    # test_outcomes()
    # test_report_and_gap()
    # test_events_ranked_and_per_session()
    print("\nTODO: implemente CorrectionDetector, BehavioralOutcomeClassifier")
    print("e PerceivedEvalExtractor.run()")
```

---

## ✅ Validação: Critérios de Aceitação

Seu código será considerado **APROVADO** quando:

- [ ] `CorrectionDetector.detect()` classifica msg 3/5/7 da `SESS-102` como CORRECTION/PUSHBACK/REDIRECTION com evidência citável
- [ ] `BehavioralOutcomeClassifier.classify()` produz os 4 desfechos esperados — inclusive `BENIGN_EXIT` na `SESS-104` (exit com causa benigna não é rage quit)
- [ ] `STUCK_LOOP` dispara com 3+ reformulações sem progresso (`SESS-103`)
- [ ] `PerceivedQualityReport` calcula as três taxas e `perceived_quality` em [0.0, 1.0]
- [ ] `nps_gap == "WARN"` no cenário do prólogo (NPS alto + qualidade percebida baixa)
- [ ] Eventos emitidos apenas para sessões negativas, ordenados CRITICAL → WARN, com `suggested_eval_case_id` e resolução per-session
- [ ] Nenhuma parte do pipeline pergunta nada ao usuário (RF3)

---

## 📊 Rubric de Avaliação

| Critério | Peso | Insuficiente (0-3) | Básico (4-6) | Proficiente (7-8) | Excelente (9-10) |
|---|---|---|---|---|---|
| **CorrectionDetector (Parte 2)** | 25% | Não implementado | Detecta "não" genérico, sem tipos | Três tipos com precedência e evidência | Precedência correta + exige resposta anterior do agente + neutras não geram evento |
| **BehavioralOutcomeClassifier (Parte 2)** | 30% | Não implementado | Exit binário (saiu = ruim) | Distingue benigno de rage quit por estado da tarefa | Stuck por reformulação + precedência de regras documentada |
| **Relatório e calibração (Parte 3)** | 25% | Não implementado | Taxas sem aggregate correto | Taxas + perceived_quality compostos | nps_gap como achado de primeira classe (pesquisa vs. comportamento) |
| **Eventos de eval (Parte 3)** | 20% | Não implementado | Emite para toda sessão | Só negativas, com severity | Ranqueados, com case id, resolução per-session declarada, prontos para o loop |

**Nota final:** Média ponderada. **Aprovação:** >= 7.0

---

## 💡 Dicas para Implementação

1. **A ambiguidade do exit é o coração do exercício.** "Usuário saiu do chat" não avalia nada sozinho. É o `final_task_state` + o que veio antes (agradecimento? correção não resolvida?) que transforma o mesmo evento em BENIGN_EXIT ou rage quit. Se seu classificador não usa o estado da tarefa, ele está errado por construção.
2. **Correção pressupõe resposta anterior.** A primeira mensagem do usuário ("quero um whey sem lactose") contém "sem" — mas não é correção de nada. Exija mensagem anterior do agente.
3. **O NPS não é o vilão — é a calibração.** O gap entre pesquisa (agregada, defasada) e comportamento (contínuo, por sessão) é o achado acionável: quando os dois divergem, um dos dois está mentindo, e geralmente é o agregado.

---

## ❓ Dúvidas Comuns

**P: Heurística de palavra-chave não é frágil para produção?**
R: É. Em produção a detecção é feita por classificador (LLM ou não) sobre o transcript — o padrão exige "instrumentation to detect corrections and pushback reliably" (`...patterns.md:181`). O exercício usa regras porque o mecanismo estrutural (tipos, desfechos, resolução, emissão) é o que transfere; trocar o detector por um classificador não muda nenhuma assinatura daqui.

**P: Por que o evento não aponta qual tool call falhou?**
R: Porque a resolução do sinal é per-session, não per-decision (`...patterns.md:183`). O comportamento do usuário diz "esta sessão foi percebida como ruim"; a localização da falha é trabalho do production-to-offline loop que consome o evento — ver [[curriculum/03-nivel-3-advanced-architecture/exercises/exercise-13-production-offline-drift-taxonomy|Exercício 13]].

**P: Isso não é só mais um dashboard de retenção?**
R: Não — a diferença é o destino do sinal. Dashboard informa humanos; Perceived-Eval emite `PerceivedEvalEvent` que entram como insumo de eval (casos candidatos, recalibração de judge). É avaliação contínua disfarçada de telemetria.

**P: Onde isso vive no sistema de evals do repo?**
R: É o quadrante online/não-determinístico que faltava — a matriz do [[curriculum/02-nivel-2-practical-patterns/exercises/exercise-07-eval-coverage-matrix|Exercício 7]] exige "a few things in each box", e sinal percebido do usuário é o mecanismo online não-determinístico canônico.

---

## 🚀 Próximo Passo

Depois de completar este exercício:

1. Leia o padrão 8 completo e sua classificação: `docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-patterns.md:163-183` e `...classification.md:132-144` — classificado **Missing**: nenhum doc do repo tratava correção de usuário como dado de eval
2. Compare com [[docs/canonical/eval-to-production-correlation-tracking|Eval-to-Production Correlation Tracking]]: lá CSAT é *outcome* a correlacionar; aqui comportamento é *input* contínuo — a inversão é o padrão
3. Siga para o [[curriculum/02-nivel-2-practical-patterns/exercises/exercise-07-eval-coverage-matrix|Exercício 7: Eval Coverage Matrix]] — onde o sinal que você extraiu ocupa formalmente um quadrante do portfólio

---

*Exercício 6 | Nível 2 — Padrões Práticos | Perceived-Eval*

**O usuário avaliou o agente 1.847 vezes no trimestre. O transcript é a pesquisa que ninguém leu.**
