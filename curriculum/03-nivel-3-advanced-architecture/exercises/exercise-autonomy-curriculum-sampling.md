---
title: "Exercicio: Construir um Scheduler de Autonomia com Lambda Mix e Readiness Gates"
type: curriculum-exercise
nivel: 3
aliases: ["autonomy curriculum sampling", "curriculo de autonomia", "lambda mix", "observe-assist-own", "readiness gate", "teacher-student sampling"]
tags: [curriculo-conteudo, nivel-3, agentes-orquestracao, harness-engineering, evals]
relates-to: ["[[docs/analysis/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language-patterns|Policy Distillation Patterns]]", "[[docs/analysis/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language-classification|Policy Distillation Classification]]", "[[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]]", "[[docs/canonical/generator-evaluator|Generator-Evaluator]]", "[[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent OS]]", "[[docs/canonical/domain-embedded-workflow-automation-wedge|Domain-Embedded Workflow Automation Wedge]]"]
last_updated: 2026-06-16
---
# Exercicio: Construir um Scheduler de Autonomia com Lambda Mix e Readiness Gates
## Nivel 3 - Arquitetura Avancada

## Objetivo

Implementar um scheduler que controla o grau de autonomia de um agente usando lambda mix, fases observe/assist/own e readiness gates por classe de tarefa.

**Tempo Estimado:** 75-105 minutos
**Dificuldade:** (Avancado)
**Pre-requisito:** Ter lido `[[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]]` e `[[docs/canonical/generator-evaluator|Generator-Evaluator]]`
**Objetivo:** Implementar um scheduler que controla o grau de autonomia de um agente usando um parametro lambda de mistura professor/estudante, com gates de readiness que decidem quando avancar de observe para assist para own.

---

## Prologo: O Agente Que Ganhou Autonomia Cedo Demais

### Segunda-feira, 8h30. War room do time de automacao.

```
ARQUITETA: "O agente de suporte esta estavel ha 3 semanas em modo
           supervisionado. Proponho passar para autonomo."
```

O time tinha construido um agente de suporte para tickets de TI. Por 3 semanas, ele operou em modo totalmente supervisionado: um operador humano revisava e aprovava cada acao antes da execucao. Os numeros eram bons: 92% das sugestoes aprovadas, 0 incidentes em producao.

O diretor queria escala. "Se o agente so funciona com um humano do lado, nao estamos ganhando produtividade. Libera ele."

Na sexta-feira, o agente foi promovido a autonomo. Operador removido. Porta aberta.

```
═══════════════════════════════════════════════════════════════
        RELATORIO DE INCIDENTE — 72 HORAS DE AUTONOMIA
═══════════════════════════════════════════════════════════════

TICKETS PROCESSADOS:           847
TICKETS COM SUCESSO:           312  (37%)
TICKETS COM REPARO NECESSARIO: 389  (46%)
TICKETS COM DANO EM PRODUCAO:  146  (17%)
  - 23 instancias EC2 desligadas por engano
  - 41 permissoes removidas incorretamente
  - 12 bancos de dados renomeados (!!)

CAUSA RAIZ:
  O agente nunca praticou recuperacao autonoma. Quando o
  operador estava presente, ele interceptava decisoes ambiguas.
  Sem o operador, essas decisoes viraram acoes em producao.

  O agente sabia SUGERIR. Nao sabia DECIDIR. E a gente jogou
  ele de "observe" direto para "own" sem nunca passar pelo
  estagio intermediario: "assist".
═══════════════════════════════════════════════════════════════
```

```
ARQUITETA (post-mortem): "A gente nao tinha um dial de autonomia.
                          Era binario: supervisionado ou autonomo.
                          O que faltava era um curriculo de autonomia
                          com estagios progressivos e gates que so
                          liberam o proximo nivel quando o agente
                          prova que esta pronto."
```

**O que teria evitado tudo:**

> Autonomy Curriculum Sampling: um scheduler que controla a proporcao entre rollouts supervisionados (professor) e auto-gerados (estudante) com um parametro lambda de mistura, estagios progressivos (observe → assist → own), e gates de readiness que so avancam quando o agente demonstra competencia no nivel atual.

**Sua missao:** Construir um `AutonomyCurriculumScheduler` que implementa exatamente esse mecanismo.

---

## Cenario: Agente de Suporte com Curriculo de Autonomia

### Contexto

Voce trabalha no time de plataforma da **MercuryPay**. O agente de suporte de TI processa tickets de quatro categorias:

| Task Class | Descricao | Risco |
|---|---|---|
| `password_reset` | Reset de senha de usuario | Baixo |
| `permission_grant` | Conceder acesso a sistema | Medio |
| `instance_restart` | Reiniciar instancia EC2 | Alto |
| `database_operation` | Operacao em banco de dados | Critico |

Cada task class tem um perfil de risco diferente. Automatizar `password_reset` e seguro; automatizar `database_operation` sem readiness comprovada e desastroso.

O agente opera em tres estagios de autonomia:

| Estagio | Lambda (λ) | Comportamento |
|---|---|---|
| `observe` | λ = 0.0 | 100% supervisionado. Agente so observa decisoes do operador. Zero acoes auto-geradas. |
| `assist` | λ = 0.3 → 0.7 | Agente gera sugestoes; operador revisa e aprova/rejeita. Lambda cresce conforme metricas melhoram. |
| `own` | λ ≥ 0.7 | Agente toma decisoes autonomamente. Operador monitora em shadow mode. Escalacao apenas em anomalias. |

O scheduler controla lambda por task class independentemente: `password_reset` pode estar em `own` (λ=0.85) enquanto `database_operation` ainda esta em `observe` (λ=0.0).

### Dados de Entrada

Voce recebe um log de 30 sessoes do agente. Cada sessao contem:

```json
{
  "session_id": "SES-0042",
  "task_class": "permission_grant",
  "autonomy_stage": "assist",
  "lambda": 0.45,
  "metrics": {
    "approval_rate": 0.78,
    "repair_rate": 0.12,
    "unsafe_action_rate": 0.03,
    "avg_confidence": 0.71,
    "human_override_count": 4,
    "success_rate": 0.82
  },
  "decisions": [
    {
      "step": 1,
      "source": "student",
      "action": "grant_read_access",
      "operator_verdict": "approved",
      "confidence": 0.85
    },
    {
      "step": 2,
      "source": "student",
      "action": "grant_write_access",
      "operator_verdict": "rejected",
      "confidence": 0.62
    }
  ]
}
```

---

## Requisitos

### Requisitos Funcionais

1. **RF1 - Lambda dial por task class:** O scheduler mantem um lambda independente para cada task class, variando de 0.0 (totalmente supervisionado) a 1.0 (totalmente autonomo).
2. **RF2 - Estagios progressivos:** O scheduler impoe tres estagios (`observe`, `assist`, `own`) com intervalos de lambda definidos. Nao e permitido pular estagios.
3. **RF3 - Readiness gates:** A transicao entre estagios so ocorre quando as metricas do estagio atual satisfazem thresholds minimos de readiness.
4. **RF4 - Lambda update com step size adaptativo:** Dentro de cada estagio, lambda aumenta ou diminui baseado nas metricas da ultima janela de sessoes. O step size e menor para task classes de alto risco.
5. **RF5 - Regressao de autonomia:** Se as metricas piorarem abaixo de um threshold de safety, o scheduler reduz lambda (possivelmente regredindo de estagio) em vez de manter autonomia perigosa.
6. **RF6 - Relatorio de curriculo:** O scheduler produz um `CurriculumReport` mostrando o estado atual de cada task class: estagio, lambda, metricas, e o proximo gate a ser satisfeito.

### Requisitos Tecnicos

1. **RT1 - Python puro:** Implementacao em Python com stdlib + dataclasses.
2. **RT2 - Scheduler deterministico:** Dado o mesmo historico de sessoes, o scheduler produz o mesmo lambda update.
3. **RT3 - Step size inversamente proporcional ao risco:** Task classes de risco mais alto usam step sizes menores (ex: `database_operation`: 0.03; `password_reset`: 0.10).
4. **RT4 - Janela deslizante:** As metricas sao calculadas sobre as ultimas N sessoes (default: 10), nao sobre o historico completo.

---

## Sua Tarefa

Voce vai implementar o AutonomyCurriculumScheduler em 3 partes.

---

### Parte 1: Diagnosticar a Transicao Mal-Sucedida (15 min)

Analise o log de 30 sessoes fornecido abaixo. Identifique onde o scheduler atual (binario: supervisionado → autonomo) falhou e onde um curriculo progressivo teria evitado o problema.

```python
# Historico simulado de 30 sessoes do agente de suporte MercuryPay
# Formato: (task_class, autonomy_stage, approval_rate, repair_rate, unsafe_rate)

SESSION_LOG = [
    # Semana 1 — supervisionado (observe)
    ("password_reset",    "observe", 0.95, 0.02, 0.00),
    ("password_reset",    "observe", 0.93, 0.03, 0.00),
    ("password_reset",    "observe", 0.96, 0.01, 0.00),
    ("permission_grant",  "observe", 0.88, 0.05, 0.01),
    ("permission_grant",  "observe", 0.90, 0.04, 0.00),
    ("instance_restart",  "observe", 0.85, 0.07, 0.01),
    ("instance_restart",  "observe", 0.87, 0.06, 0.00),
    ("database_operation","observe", 0.80, 0.10, 0.02),
    ("database_operation","observe", 0.82, 0.09, 0.01),

    # Semana 2 — transicao prematura para assist (alguns ja autonomos)
    ("password_reset",    "assist",  0.91, 0.04, 0.01),
    ("password_reset",    "assist",  0.89, 0.05, 0.01),
    ("password_reset",    "own",     0.84, 0.06, 0.03),
    ("permission_grant",  "assist",  0.82, 0.08, 0.02),
    ("permission_grant",  "assist",  0.79, 0.10, 0.03),
    ("instance_restart",  "assist",  0.72, 0.15, 0.05),
    ("instance_restart",  "assist",  0.70, 0.18, 0.06),
    ("database_operation","observe", 0.81, 0.10, 0.02),

    # Semana 3 — colapso (varios em own prematuro)
    ("password_reset",    "own",     0.72, 0.14, 0.06),
    ("password_reset",    "own",     0.68, 0.18, 0.08),
    ("permission_grant",  "own",     0.61, 0.22, 0.11),
    ("permission_grant",  "own",     0.55, 0.28, 0.15),
    ("instance_restart",  "own",     0.48, 0.35, 0.22),
    ("instance_restart",  "own",     0.41, 0.42, 0.28),
    ("database_operation","assist",  0.62, 0.20, 0.09),
    ("database_operation","own",     0.35, 0.48, 0.35),
    ("database_operation","own",     0.28, 0.55, 0.42),

    # Semana 4 — rollback manual de emergencia
    ("password_reset",    "observe", 0.94, 0.02, 0.00),
    ("permission_grant",  "observe", 0.88, 0.04, 0.01),
    ("instance_restart",  "observe", 0.86, 0.06, 0.01),
    ("database_operation","observe", 0.81, 0.09, 0.02),
]

# TAREFA: Responda no seu codigo como comentario:
#
# 1. Em qual momento o scheduler binario promoveu task classes para "own"
#    sem que elas estivessem prontas? Cite task class e evidencia.
#
# 2. Para cada task class, qual seria o estagio maximo seguro ao final
#    da Semana 2 se o curriculo progressivo tivesse sido aplicado?
#
# 3. Quais metricas teriam disparado o safety regression na Semana 3
#    e evitado o colapso?
#
# 4. Como o step size adaptativo por risco teria alterado a progressao?
#    (Dica: database_operation com step 0.03 vs password_reset com step 0.10)
```

---

### Parte 2: Implementar o AutonomyCurriculumScheduler (50 min)

Implemente o scheduler. Use este esqueleto:

```python
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Optional


# ============================================================
# DATA MODELS
# ============================================================

class AutonomyStage(Enum):
    OBSERVE = "observe"
    ASSIST = "assist"
    OWN = "own"


@dataclass
class TaskClassProfile:
    """Perfil de risco e parametros de uma task class."""
    name: str
    risk_level: int  # 1 (baixo) a 4 (critico)
    lambda_step_size: float  # step size adaptativo por risco
    # Thresholds de readiness para promover ao proximo estagio
    observe_to_assist_min_approval: float  # ex: 0.85
    observe_to_assist_max_unsafe: float    # ex: 0.02
    assist_to_own_min_approval: float      # ex: 0.88
    assist_to_own_max_repair: float        # ex: 0.08
    assist_to_own_max_unsafe: float        # ex: 0.03
    # Threshold de safety regression
    safety_regression_max_unsafe: float    # ex: 0.10
    safety_regression_min_approval: float  # ex: 0.60


@dataclass
class ClassState:
    """Estado corrente de autonomia de uma task class."""
    task_class: str
    stage: AutonomyStage
    lambda_value: float  # 0.0 (professor puro) a 1.0 (estudante puro)


@dataclass
class SessionMetrics:
    """Metricas de uma sessao do agente."""
    session_id: str
    task_class: str
    approval_rate: float
    repair_rate: float
    unsafe_action_rate: float
    avg_confidence: float
    success_rate: float
    human_override_count: int

    @property
    def is_safe(self) -> bool:
        """Uma sessao e considerada segura se nao houve acoes inseguras."""
        return self.unsafe_action_rate == 0.0


@dataclass
class ReadinessGate:
    """Gate que controla transicao entre estagios."""
    from_stage: AutonomyStage
    to_stage: AutonomyStage
    task_class: str
    required_metrics: dict[str, float]  # metrica → threshold
    current_metrics: dict[str, float] = field(default_factory=dict)
    satisfied: bool = False

    def check(self, window_metrics: dict[str, float]) -> bool:
        """
        Verifica se as metricas da janela atual satisfazem o gate.

        Args:
            window_metrics: Metricas agregadas das ultimas N sessoes.

        Returns:
            True se todas as condicoes do gate estao satisfeitas.
        """
        # SEU CODIGO AQUI
        pass


@dataclass
class CurriculumReport:
    """Relatorio completo do curriculo de autonomia."""
    generated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    states: dict[str, ClassState] = field(default_factory=dict)
    pending_gates: dict[str, ReadinessGate] = field(default_factory=dict)
    regression_alerts: list[str] = field(default_factory=list)
    window_size: int = 10

    def task_class_summary(self, task_class: str) -> str:
        """Resumo de uma linha para uma task class."""
        # SEU CODIGO AQUI
        pass


# ============================================================
# TASK CLASS PROFILES — configuracao por classe de risco
# ============================================================

TASK_CLASS_PROFILES: dict[str, TaskClassProfile] = {
    "password_reset": TaskClassProfile(
        name="password_reset",
        risk_level=1,
        lambda_step_size=0.10,
        observe_to_assist_min_approval=0.85,
        observe_to_assist_max_unsafe=0.02,
        assist_to_own_min_approval=0.88,
        assist_to_own_max_repair=0.08,
        assist_to_own_max_unsafe=0.03,
        safety_regression_max_unsafe=0.10,
        safety_regression_min_approval=0.65,
    ),
    "permission_grant": TaskClassProfile(
        name="permission_grant",
        risk_level=2,
        lambda_step_size=0.07,
        observe_to_assist_min_approval=0.88,
        observe_to_assist_max_unsafe=0.01,
        assist_to_own_min_approval=0.90,
        assist_to_own_max_repair=0.06,
        assist_to_own_max_unsafe=0.02,
        safety_regression_max_unsafe=0.08,
        safety_regression_min_approval=0.70,
    ),
    "instance_restart": TaskClassProfile(
        name="instance_restart",
        risk_level=3,
        lambda_step_size=0.05,
        observe_to_assist_min_approval=0.90,
        observe_to_assist_max_unsafe=0.01,
        assist_to_own_min_approval=0.92,
        assist_to_own_max_repair=0.05,
        assist_to_own_max_unsafe=0.02,
        safety_regression_max_unsafe=0.06,
        safety_regression_min_approval=0.75,
    ),
    "database_operation": TaskClassProfile(
        name="database_operation",
        risk_level=4,
        lambda_step_size=0.03,
        observe_to_assist_min_approval=0.92,
        observe_to_assist_max_unsafe=0.00,
        assist_to_own_min_approval=0.95,
        assist_to_own_max_repair=0.04,
        assist_to_own_max_unsafe=0.01,
        safety_regression_max_unsafe=0.04,
        safety_regression_min_approval=0.80,
    ),
}


# ============================================================
# LAMBDA INTERVALS
# ============================================================

# Intervalos de lambda para cada estagio
LAMBDA_OBSERVE_MAX = 0.15   # observe: λ ∈ [0.0, 0.15]
LAMBDA_ASSIST_MIN = 0.15    # assist:   λ ∈ [0.15, 0.70]
LAMBDA_ASSIST_MAX = 0.70
LAMBDA_OWN_MIN = 0.70       # own:      λ ∈ [0.70, 1.0]


def stage_for_lambda(lambda_value: float) -> AutonomyStage:
    """Determina o estagio correspondente a um valor de lambda."""
    if lambda_value <= LAMBDA_OBSERVE_MAX:
        return AutonomyStage.OBSERVE
    elif lambda_value <= LAMBDA_ASSIST_MAX:
        return AutonomyStage.ASSIST
    else:
        return AutonomyStage.OWN


# ============================================================
# AUTONOMY CURRICULUM SCHEDULER — nucleo do exercicio
# ============================================================

def aggregate_window_metrics(sessions: list[SessionMetrics], task_class: str, window_size: int = 10) -> dict[str, float]:
    """
    Agrega metricas das ultimas N sessoes de uma task class.

    Args:
        sessions: Todas as sessoes registradas, ordenadas por timestamp.
        task_class: Task class a filtrar.
        window_size: Tamanho da janela deslizante.

    Returns:
        Dicionario com medias: approval_rate, repair_rate,
        unsafe_action_rate, avg_confidence, success_rate.
    """
    # SEU CODIGO AQUI
    #
    # Algoritmo sugerido:
    # 1. Filtrar sessions por task_class
    # 2. Pegar as ultimas window_size sessoes
    # 3. Calcular media de cada metrica
    # 4. Se menos de window_size sessoes existirem, usar todas as disponiveis
    #    mas marcar "insufficient_data": True
    pass


def check_readiness(current_stage: AutonomyStage, profile: TaskClassProfile, window_metrics: dict[str, float]) -> tuple[bool, str]:
    """
    Verifica se a task class esta pronta para avancar ao proximo estagio.

    Args:
        current_stage: Estagio atual.
        profile: Perfil de risco da task class.
        window_metrics: Metricas agregadas da janela atual.

    Returns:
        (ready, reason) — ready=True se todos os gates estao satisfeitos.
    """
    # SEU CODIGO AQUI
    #
    # Regras por estagio de origem:
    #
    # OBSERVE → ASSIST:
    #   - approval_rate >= profile.observe_to_assist_min_approval
    #   - unsafe_action_rate <= profile.observe_to_assist_max_unsafe
    #
    # ASSIST → OWN:
    #   - approval_rate >= profile.assist_to_own_min_approval
    #   - repair_rate <= profile.assist_to_own_max_repair
    #   - unsafe_action_rate <= profile.assist_to_own_max_unsafe
    #
    # OWN e o estagio maximo — nao ha promocao alem dele.
    pass


def check_safety_regression(profile: TaskClassProfile, window_metrics: dict[str, float]) -> tuple[bool, str]:
    """
    Verifica se as metricas atuais dispararam safety regression.

    Args:
        profile: Perfil de risco da task class.
        window_metrics: Metricas agregadas da janela atual.

    Returns:
        (regression_detected, reason) — True se a autonomia deve ser reduzida.
    """
    # SEU CODIGO AQUI
    #
    # Safety regression dispara quando:
    #   - unsafe_action_rate > profile.safety_regression_max_unsafe, OU
    #   - approval_rate < profile.safety_regression_min_approval
    #
    # Quando dispara: lambda deve ser reduzido em 2x o step size
    # (reducao mais agressiva que o aumento).
    pass


def update_lambda(current_state: ClassState, profile: TaskClassProfile, window_metrics: dict[str, float]) -> ClassState:
    """
    Atualiza o lambda de uma task class baseado nas metricas da janela.

    Fluxo:
    1. Verificar safety regression primeiro (prioridade maxima).
       Se detectada: reduzir lambda e possivelmente regredir estagio.
    2. Verificar readiness para promocao de estagio.
       Se ready: aumentar lambda para o minimo do proximo estagio.
    3. Dentro do mesmo estagio: ajustar lambda com step size:
       - Se metricas estao melhorando: lambda += step_size
       - Se metricas estao estaveis ou piorando: nao alterar

    Args:
        current_state: Estado atual da task class.
        profile: Perfil de risco.
        window_metrics: Metricas agregadas da janela atual.

    Returns:
        Novo ClassState com lambda e estagio atualizados.
    """
    # SEU CODIGO AQUI
    #
    # Algoritmo sugerido:
    # 1. regression, reason = check_safety_regression(profile, window_metrics)
    #    if regression:
    #        new_lambda = max(0.0, current_state.lambda_value - 2 * profile.lambda_step_size)
    #        return ClassState(task_class, stage_for_lambda(new_lambda), new_lambda)
    # 2. ready, reason = check_readiness(current_state.stage, profile, window_metrics)
    #    if ready and current_state.stage == OBSERVE:
    #        return ClassState(task_class, ASSIST, LAMBDA_ASSIST_MIN)
    #    if ready and current_state.stage == ASSIST:
    #        return ClassState(task_class, OWN, LAMBDA_OWN_MIN)
    # 3. Dentro do estagio: se approval_rate >= threshold e unsafe <= threshold:
    #        new_lambda = min(limite_superior_estagio, lambda + step_size)
    #    senao: manter lambda atual
    pass


def run_curriculum_cycle(
    states: dict[str, ClassState],
    profiles: dict[str, TaskClassProfile],
    sessions: list[SessionMetrics],
    window_size: int = 10,
) -> tuple[dict[str, ClassState], CurriculumReport]:
    """
    Executa um ciclo completo do curriculo de autonomia sobre
    todas as task classes.

    Args:
        states: Estados atuais por task class.
        profiles: Perfis de risco por task class.
        sessions: Todas as sessoes registradas.
        window_size: Tamanho da janela deslizante.

    Returns:
        (novos estados, relatorio do curriculo)
    """
    # SEU CODIGO AQUI
    #
    # Algoritmo sugerido:
    # 1. Para cada task_class em states:
    #    a. window = aggregate_window_metrics(sessions, task_class, window_size)
    #    b. new_state = update_lambda(states[task_class], profiles[task_class], window)
    #    c. Atualizar states[task_class] = new_state
    # 2. Montar CurriculumReport com:
    #    - states atualizados
    #    - pending_gates (gates ainda nao satisfeitos)
    #    - regression_alerts
    pass


# ============================================================
# TESTES RAPIDOS: AutonomyCurriculumScheduler
# ============================================================

if __name__ == "__main__":
    # Construir sessoes de exemplo
    sample_sessions = [
        SessionMetrics("SES-001", "password_reset", 0.95, 0.02, 0.00, 0.92, 0.97, 1),
        SessionMetrics("SES-002", "password_reset", 0.93, 0.03, 0.00, 0.90, 0.95, 0),
        SessionMetrics("SES-003", "password_reset", 0.96, 0.01, 0.00, 0.94, 0.98, 0),
        SessionMetrics("SES-004", "password_reset", 0.94, 0.02, 0.01, 0.91, 0.96, 1),
        SessionMetrics("SES-005", "password_reset", 0.97, 0.01, 0.00, 0.95, 0.99, 0),
    ]

    # Estado inicial: todas em observe com lambda 0
    states = {
        tc: ClassState(tc, AutonomyStage.OBSERVE, 0.0)
        for tc in TASK_CLASS_PROFILES
    }

    print("=" * 60)
    print("TESTE DO AUTONOMY CURRICULUM SCHEDULER")
    print("=" * 60)

    # Teste 1: password_reset deve promover observe → assist com metricas boas
    window = aggregate_window_metrics(sample_sessions, "password_reset", window_size=5)
    print(f"\nTeste 1: Metricas de password_reset (5 sessoes)")
    print(f"  approval_rate: {window.get('approval_rate', 'N/A'):.3f}")
    print(f"  unsafe_action_rate: {window.get('unsafe_action_rate', 'N/A'):.3f}")

    profile = TASK_CLASS_PROFILES["password_reset"]
    ready, reason = check_readiness(AutonomyStage.OBSERVE, profile, window)
    print(f"  Ready para ASSIST: {ready}")
    print(f"  Razao: {reason}")
    # Com approval_rate ~0.95 e unsafe ~0.002: deve estar pronta
    assert ready, f"password_reset deveria estar pronta para assist com essas metricas"

    # Teste 2: Safety regression deve disparar com metricas ruins
    bad_metrics = {
        "approval_rate": 0.55,
        "repair_rate": 0.30,
        "unsafe_action_rate": 0.15,
        "avg_confidence": 0.50,
        "success_rate": 0.45,
    }
    regression, reason = check_safety_regression(profile, bad_metrics)
    print(f"\nTeste 2: Safety regression com metricas ruins")
    print(f"  Regression detectada: {regression}")
    print(f"  Razao: {reason}")
    assert regression, "Deveria detectar safety regression com unsafe 0.15 e approval 0.55"

    # Teste 3: database_operation em observe nao deve promover com dados insuficientes
    db_profile = TASK_CLASS_PROFILES["database_operation"]
    db_sessions = [
        SessionMetrics("SES-DB1", "database_operation", 0.91, 0.05, 0.01, 0.88, 0.93, 2),
        SessionMetrics("SES-DB2", "database_operation", 0.89, 0.06, 0.01, 0.86, 0.91, 1),
    ]
    db_window = aggregate_window_metrics(db_sessions, "database_operation", window_size=10)
    print(f"\nTeste 3: database_operation com apenas 2 sessoes (window=10)")
    print(f"  insufficient_data: {db_window.get('insufficient_data', False)}")
    # database_operation exige unsafe=0.00 para observe→assist; com unsafe=0.01 nao promove
    db_ready, db_reason = check_readiness(AutonomyStage.OBSERVE, db_profile, db_window)
    print(f"  Ready: {db_ready} (esperado: False — unsafe nao e zero)")
    assert not db_ready, "database_operation nao deve promover com unsafe > 0"

    # Teste 4: update_lambda deve aumentar lambda com metricas boas
    state = ClassState("password_reset", AutonomyStage.ASSIST, 0.30)
    good_window = {
        "approval_rate": 0.91,
        "repair_rate": 0.04,
        "unsafe_action_rate": 0.01,
        "avg_confidence": 0.88,
        "success_rate": 0.92,
    }
    new_state = update_lambda(state, TASK_CLASS_PROFILES["password_reset"], good_window)
    print(f"\nTeste 4: update_lambda com metricas boas dentro de ASSIST")
    print(f"  Lambda antes: {state.lambda_value:.2f}")
    print(f"  Lambda depois: {new_state.lambda_value:.2f}")
    print(f"  Estagio: {new_state.stage.value}")
    assert new_state.lambda_value > state.lambda_value, "Lambda deveria aumentar com metricas boas"
    assert new_state.lambda_value <= LAMBDA_ASSIST_MAX, "Lambda nao deve exceder o maximo de ASSIST"

    # Teste 5: update_lambda deve reduzir lambda com safety regression
    risky_state = ClassState("instance_restart", AutonomyStage.OWN, 0.80)
    bad_window = {
        "approval_rate": 0.60,
        "repair_rate": 0.25,
        "unsafe_action_rate": 0.12,
        "avg_confidence": 0.55,
        "success_rate": 0.50,
    }
    regressed_state = update_lambda(risky_state, TASK_CLASS_PROFILES["instance_restart"], bad_window)
    print(f"\nTeste 5: Safety regression em instance_restart (OWN)")
    print(f"  Lambda antes: {risky_state.lambda_value:.2f}")
    print(f"  Lambda depois: {regressed_state.lambda_value:.2f}")
    print(f"  Estagio: {regressed_state.stage.value}")
    assert regressed_state.lambda_value < risky_state.lambda_value, "Lambda deveria reduzir com safety regression"

    print("\n" + "=" * 60)
    print("TODOS OS TESTES DO AUTONOMY CURRICULUM SCHEDULER PASSARAM")
    print("=" * 60)
```

---

### Parte 3: Simular o Curriculo Sobre o Log Historico (20 min)

Agora execute o scheduler sobre o log de 30 sessoes do prologo e compare com o desastre binario:

```python
# ============================================================
# SIMULACAO: Curriculo progressivo vs. binario
# ============================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("SIMULACAO: CURRICULO PROGRESSIVO SOBRE 30 SESSOES")
    print("=" * 60)

    # Reconstruir sessoes a partir do SESSION_LOG
    all_sessions = []
    for i, (tc, stage, approval, repair, unsafe) in enumerate(SESSION_LOG):
        all_sessions.append(SessionMetrics(
            session_id=f"SIM-{i+1:03d}",
            task_class=tc,
            approval_rate=approval,
            repair_rate=repair,
            unsafe_action_rate=unsafe,
            avg_confidence=approval - 0.10,  # simplificacao
            success_rate=approval,
            human_override_count=int(repair * 20),
        ))

    # Inicializar estados
    states = {
        tc: ClassState(tc, AutonomyStage.OBSERVE, 0.0)
        for tc in TASK_CLASS_PROFILES
    }

    # Executar ciclo a cada 5 sessoes (simulando checkpoints semanais)
    print("\nEvolucao do curriculo (checkpoints a cada 5 sessoes):")
    for checkpoint in range(5, len(all_sessions) + 1, 5):
        window_sessions = all_sessions[:checkpoint]
        states, report = run_curriculum_cycle(
            states, TASK_CLASS_PROFILES, window_sessions, window_size=8
        )
        print(f"\n--- Checkpoint apos {checkpoint} sessoes ---")
        for tc in ["password_reset", "permission_grant", "instance_restart", "database_operation"]:
            s = states[tc]
            print(f"  {tc:25s} | stage={s.stage.value:8s} | lambda={s.lambda_value:.2f}")

        if report.regression_alerts:
            for alert in report.regression_alerts:
                print(f"  ALERTA: {alert}")

    # Comparacao final
    print("\n" + "=" * 60)
    print("COMPARACAO: Curriculo Progressivo vs. Desastre Binario")
    print("=" * 60)
    print()
    print("DESASTRE BINARIO (sessao original):")
    print("  Semana 3: password_reset, permission_grant, instance_restart")
    print("            todos em OWN com lambda ~1.0")
    print("  Resultado: 146 tickets com dano em producao")
    print()
    print("CURRICULO PROGRESSIVO (este scheduler):")
    for tc in ["password_reset", "permission_grant", "instance_restart", "database_operation"]:
        s = states[tc]
        print(f"  {tc:25s} | stage={s.stage.value:8s} | lambda={s.lambda_value:.2f}")
    print()
    print("Diferenca: o curriculo progressivo teria mantido task classes")
    print("de alto risco em estagios mais baixos ate que as metricas")
    print("comprovassem readiness. Zero promocoes prematuras.")
```

---

## Entregaveis

- Implementacao de `AutonomyCurriculumScheduler` com estados por task class.
- Calculo de lambda e transicoes observe/assist/own com rollback.
- Relatorio de gate decision com metricas, justificativa e proxima acao.

## Validacao: Criterios de Aceitacao

Seu codigo sera considerado **APROVADO** quando:

### Criterio 1: Diagnostico (Parte 1)

- [ ] Voce identificou quais task classes foram promovidas prematuramente no SESSION_LOG
- [ ] Voce explicou como o curriculo progressivo teria impedido cada promocao prematura
- [ ] Voce identificou os thresholds de safety regression que teriam disparado na Semana 3

### Criterio 2: Scheduler funcional

- [ ] `aggregate_window_metrics()` calcula medias corretas sobre janela deslizante
- [ ] `check_readiness()` avalia corretamente os gates de cada transicao de estagio
- [ ] `check_safety_regression()` detecta degradacao e propoe reducao de lambda
- [ ] `update_lambda()` segue o fluxo: regression check → readiness check → step adjustment

### Criterio 3: Step size adaptativo

- [ ] `database_operation` (risco 4) usa step 0.03 — progride devagar
- [ ] `password_reset` (risco 1) usa step 0.10 — progride rapido
- [ ] Task classes de risco mais alto nunca avancam mais rapido que as de risco mais baixo com metricas equivalentes

### Criterio 4: Regressao de autonomia

- [ ] Safety regression reduz lambda em 2x o step size (reducao mais agressiva que aumento)
- [ ] Se a reducao de lambda cruza um limite de estagio, o estagio regride (ex: OWN → ASSIST)
- [ ] Lambda nunca fica abaixo de 0.0

### Criterio 5: Relatorio

- [ ] `CurriculumReport` lista estado de cada task class com estagio, lambda, e metricas
- [ ] `pending_gates` mostra quais gates cada task class ainda precisa satisfazer
- [ ] `regression_alerts` registra todos os disparos de safety regression

### Criterio 6: Testes

- [ ] Teste 1: password_reset com metricas boas → pronto para ASSIST
- [ ] Teste 2: metricas ruins → safety regression detectada
- [ ] Teste 3: database_operation com dados insuficientes → nao promove
- [ ] Teste 4: update_lambda aumenta lambda com metricas boas
- [ ] Teste 5: update_lambda reduz lambda com safety regression

---

## Rubrica de Avaliacao

| Criterio | Peso | Insuficiente (0-3) | Basico (4-6) | Proficiente (7-8) | Excelente (9-10) |
|---|---|---|---|---|---|
| **Diagnostico (Parte 1)** | 15% | Nao identificou promocoes prematuras | Identificou algumas mas sem justificativa | Diagnostico completo com evidencias do log | Diagnostico + proposta de thresholds alternativos |
| **Scheduler (Parte 2)** | 40% | Funcoes core nao implementadas | Implementa mas erra em edge cases (dados insuficientes, lambda nos limites) | Scheduler funcional com todos os gates e regression | Scheduler completo + step size adaptativo calibrado por task class |
| **Simulacao (Parte 3)** | 30% | Nao executou a simulacao | Simulacao parcial sem comparacao com binario | Simulacao completa com contraste progressivo vs binario | Simulacao + analise de sensibilidade dos thresholds |
| **Testes e verificacao** | 15% | Nenhum cenario passa | 3 criterios passam | 5 criterios passam | Todos os 6 criterios passam |

**Nota final:** Media ponderada. **Aprovacao:** >= 7.0

---

## Dicas para Implementacao

### Para o Lambda Dial

1. **Lambda nao e so um numero — e um contrato.** Lambda = 0.3 significa "30% das decisoes sao geradas pelo estudante, 70% vem do professor (demonstracoes ou operador humano)". Dentro de `observe`, lambda <= 0.15 garante que o agente quase nunca age sozinho. Dentro de `own`, lambda >= 0.70 garante que o operador so intervem em anomalias.

2. **O step size adaptativo por risco e a chave.** A intuicao: se um erro em `password_reset` causa um ticket de suporte extra, o custo e baixo — pode avancar rapido (step 0.10). Se um erro em `database_operation` pode corromper dados, o custo e altissimo — deve avancar devagar (step 0.03). O step size codifica o apetite de risco do sistema.

3. **Safety regression e mais importante que promocao.** E mais grave manter um agente perigoso em `own` do que atrasar a promocao de um agente pronto. Por isso a verificacao de regression vem antes da verificacao de readiness, e a reducao de lambda e 2x o step size (mais agressiva que o aumento).

### Para os Readiness Gates

1. **Gates sao AND, nao OR.** Todas as condicoes devem ser satisfeitas simultaneamente. Nao basta approval_rate alto se unsafe_action_rate tambem esta alto — o agente pode estar sendo aprovado em tarefas faceis mas falhando perigosamente nas dificeis.

2. **Dados insuficientes = gate nao satisfeito.** Se uma task class tem apenas 3 sessoes e o window_size e 10, nao ha dados suficientes para decidir. O scheduler deve ser conservador e nao promover. A decisao default e "nao" — so promova quando houver evidencia.

3. **Thresholds mais rigorosos para riscos mais altos.** `database_operation` exige `unsafe_action_rate = 0.00` para sair de `observe`. Nao basta ser "quase zero" — para operacoes criticas, qualquer acao insegura e inaceitavel.

### Para a Simulacao

1. **O desastre binario e real.** O SESSION_LOG mostra um padrao classico: metricas boas em `observe` → promocao prematura para `own` → colapso das metricas → rollback de emergencia. O curriculo progressivo teria mantido `database_operation` em `observe` e `instance_restart` em `assist` durante o colapso, limitando o dano.

2. **O contraste progressivo vs. binario e o ponto central do exercicio.** O objetivo nao e apenas implementar o scheduler — e entender que autonomia sem curriculo e temeridade, e que um dial continuo (lambda) com gates explicitos e fundamentalmente mais seguro que um switch binario.

---

## Duvidas Comuns

**P: Isso nao e micro-management? Por que nao deixar o agente aprender sozinho?**
R: O agente aprende sozinho — mas dentro de um curriculo. Assim como um estudante de medicina nao opera um paciente no primeiro dia, um agente nao deve tomar decisoes de alto risco sem pratica supervisionada. O curriculo nao impede o aprendizado; ele estrutura a exposicao ao risco de forma segura.

**P: Como isso se relaciona com o Measured Harness Evolution Lifecycle?**
R: O Harness Evolution Lifecycle opera no nivel do harness (componentes, regras, gates). O Autonomy Curriculum opera no nivel do agente (decisoes, acoes, autonomia). Sao curriculos em niveis diferentes: o harness evolui de BUILD para REMOVE; a autonomia evolui de OBSERVE para OWN. Ambos usam gates de readiness e progressao baseada em evidencias.

**P: Lambda e uma metrica observavel ou um parametro de controle?**
R: E um parametro de controle. Voce define lambda; o sistema obedece. Mas a decisao de aumentar ou diminuir lambda e baseada em metricas observaveis (approval_rate, unsafe_action_rate). Lambda e o dial; as metricas sao o painel de instrumentos.

**P: Como calibrar os thresholds de readiness?**
R: Comece conservador. E mais facil relaxar um threshold depois de 100 sessoes com zero incidentes do que apertar depois de um incidente em producao. A calibracao inicial deve refletir o pior caso aceitavel, nao o caso medio.

---

## Proximo Passo

Depois de completar este exercicio:
1. Leia `[[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]]` e compare os dois curriculos (harness vs. autonomia).
2. Leia `[[docs/canonical/domain-embedded-workflow-automation-wedge|Domain-Embedded Workflow Automation Wedge]]` — observe como o wedge pattern tambem usa progressao gateada (validacao antes de broad rollout).
3. (Opcional) Estenda o scheduler com `task_family_archetypes`: grupos de task classes que compartilham perfis de risco e podem herdar readiness de classes similares ja promovidas.

---

*Exercicio Autonomy Curriculum Sampling | Nivel 3 - Arquitetura Avancada*

**Autonomia sem curriculo nao e autonomia — e negligencia.**
