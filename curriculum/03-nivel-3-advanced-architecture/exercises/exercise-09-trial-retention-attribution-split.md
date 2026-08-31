---
title: "Exercício 9: Trial-Retention Attribution Split — Atribuir a Falha de Ativação Antes de Decidir o Fix"
type: curriculum-exercise
nivel: 3
aliases: ["trial-retention attribution split", "trial retention split", "atribuição trial vs retorno", "split de ativação", "activation attribution", "never-tried vs tried-and-left", "bandeira de trial"]
tags: [curriculo-conteudo, nivel-3, exercicio, evals, production, trial-retention-attribution, activation-diagnostic, ownership-routing, retention-metric, python, dataclass]
relates-to: ["[[docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-analysis|GTM AI Agents Analysis]]", "[[docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-classification|GTM AI Agents Classification]]", "[[docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-patterns|GTM AI Agents Patterns]]", "[[docs/canonical/eval-to-production-correlation-tracking|Eval-to-Production Correlation Tracking]]", "[[docs/canonical/qa-to-backlog-feedback-loop|QA-to-Backlog Feedback Loop]]", "[[curriculum/03-nivel-3-advanced-architecture/01-multi-agent-systems|Multi-Agent Systems]]", "[[curriculum/03-nivel-3-advanced-architecture/exercises/exercise-10-agent-value-maturity-ladder|Exercício 10: Agent Value Maturity Ladder]]"]
last_updated: 2026-08-30
---

# 📉 Exercício 9: Trial-Retention Attribution Split — Atribuir a Falha de Ativação Antes de Decidir o Fix
## Nível 3 — Arquitetura Avançada

**Tempo Estimado:** 75-105 minutos
**Dificuldade:** ⭐⭐⭐ (Intermediário-Avançado)
**Pré-requisito:** Ter lido `01-multi-agent-systems.md` (Nível 3) + `docs/canonical/eval-to-production-correlation-tracking.md`
**Objetivo:** Construir a instrumentação de ativação completa de um agente interno: bandeira de trial por usuário e métrica de retorno semanal a partir do log bruto de telemetria (Parte 1), a regra de atribuição em dois ramos — tentou-e-não-voltou → problema de produto; nunca-tentou → problema de change management — com guardas estatísticos de coorte e janela estável (Parte 2), e o pipeline de re-check que reaplica o split após cada intervenção, roteando a propriedade do fix em vez de decretar um rollback genérico (Parte 3)

---

## 📖 Prólogo: A Reunião Que Iria Matar o Produto Certo

**Duas semanas depois do GA. Terça-feira, 9h02. KODA-Assist — o assistente de dados para os 215 vendedores da FutanBear — está na agenda da diretoria.**

```
DIRETORIA:   "Antes de falar de roadmap: os números. Sem animar."

ANALISTA:    "Ativos semanais: baixíssimo. Dos 215 vendedores com
             acesso, menos da metade logou nas últimas duas semanas.
             Curva de uso: flat desde o lançamento."

DIRETORIA:   "Flat?! Lançamos há duas semanas com fanfarra, e o
             produto é... flat. Conclusão óbvia: o assistente não
             presta. A pergunta que eu trago é se rollback ou
             reconstrução."

PRODUTO:     "Momento. Eu peço 24h antes de qualquer decisão. Uma
             pergunta que esse dashboard não responde: desses 215,
             QUANTOS ABRIRAM o assistente pelo menos uma vez?"

ANALISTA:    "...o dashboard mede logins por semana. Não sei quem
             nunca abriu."

DIRETORIA:   "E isso importa por quê?"

PRODUTO:     "Porque são duas doenças diferentes com dois donos
             diferentes:

             ┌─ QUEM TENTOU e não voltou ──→ problema de PRODUTO.
             │   O produto teve a chance e perdeu o usuário. Dono:
             │   o time de produto, com fix de qualidade.
             │
             └─ QUEM NEM TENTOU ───────────→ problema de CHANGE
                 MANAGEMENT. O produto pode ser ótimo — quem pode
                 dizer? — mas ninguém acendeu o fogão. Dono: o
                 owner do lançamento, com demos, dashboards por
                 squad e patrocínio de liderança.

             Se 80% nunca abriram, 'uso baixo' não é veredito
             sobre o produto. É veredito sobre a ativação."

DIRETORIA:   "E se for os dois ao mesmo tempo?"

PRODUTO:     "Aí o split mostra, squad por squad, qual doença está
             onde. Rollback é uma decisão cara aplicada no escuro."
```

**O que os 24h revelaram (números do exercício que você vai implementar):**

```
╔══════════════════════════════════════════════════════════════════╗
║           O SPLIT QUE O DASHBOARD NÃO FAZIA                      ║
║                                                                  ║
║  Squad            Eligíveis  Tentou  Voltou  Trial   Retorno     ║
║  ───────────────  ─────────  ──────  ──────  ─────   ───────     ║
║  INBOUND               40      36      33   90,0%    91,7%  ✅   ║
║  OUTBOUND              32      29      12   90,6%    41,4%  🐛   ║
║  RETAIL                48      10       9   20,8%    90,0%  📣   ║
║  PHARMACY              44       9       8   20,5%    88,9%  📣   ║
║  MARKETPLACE           51      11      10   21,6%    90,9%  📣   ║
║  PILOT (n=5)            5       5       4     —        —    ⚠️    ║
║                                                                  ║
║  ORG (215 eligíveis): tentou 95 (44,2%)  ·  voltou 72/95 (75,8%) ║
║                                                                  ║
║  Leitura do split:                                              ║
║   · ORG: trial 44,2% < piso 60% com retorno 75,8% ≥ piso 70%    ║
║     → CHANGE MANAGEMENT. O produto NÃO falhou onde foi usado.   ║
║   · OUTBOUND: trial alto + retorno 41,4% → problema REAL de     ║
║     produto (as semantic views de prospecção estavam defasadas) ║
║   · RETAIL/PHARMACY/MARKETPLACE: nem tentaram → ativação        ║
║   · PILOT: n=5 → ruído estatístico, não diagnostica nada        ║
║                                                                  ║
║  A diretoria quase matou o produto por uma doença que ele       ║
║  não tinha — e deixaria passar uma que ele tinha (OUTBOUND).    ║
╚══════════════════════════════════════════════════════════════════╝
```

Na semana seguinte, dois fixes saíram — nenhum deles foi rollback:

```
→ Product-team (dono do ramo produto): refez as semantic views de
  prospecção do OUTBOUND. Retorno do squad: 41,4% → 89,7%.
→ Activation-owner (dono do ramo change management): 60-70% do
  tempo em demos ao vivo + dashboard de adoção por squad para
  RETAIL, PHARMACY e MARKETPLACE. Trial dos três squads:
  ~21% → ~80%.
```

**Sua missão:** implementar o pipeline completo — instrumentação (trial flag + retorno semanal a partir de eventos brutos), regra de atribuição com dois ramos e guardas estatísticos, e o loop de re-check que roteia propriedade depois de cada intervenção. Este padrão não existe em nenhum lugar do repositório (classificado como `Missing` em `docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-classification.yaml:99-123`) — você está construindo a primeira implementação.

---

## 🧠 O Contexto

### O Modelo Mental: Uso Baixo é um Sintoma, Não um Diagnóstico

O padrão vem do caso Snowflake: duas semanas depois do GA para 6.000 usuários, a gestão viu números baixos — e o diagnóstico correto foi o split: **apenas 20% da organização tinha sequer tentado o produto** (`docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-analysis.md:48-51`). A regra:

| Ramo | Condição | Diagnóstico | Dono do fix |
|---|---|---|---|
| **Tentou e não voltou** | trial alto + retorno baixo | Problema de **produto** | Time de produto (qualidade/accuracy) |
| **Nem tentou** | trial baixo | Problema de **change management** | Owner do lançamento (demos, dashboards, patrocínio) |

O split existe para **prevenir a misatribuição de uma falha de ativação à qualidade do produto** (`...analysis.md:153`) — e, no caso do Snowflake, desarmou o alarme da gestão "com um mecanismo, não com um argumento" (`...patterns.md:131-133`).

Note a simetria invertida: o dashboard da diretoria olhava "ativos semanais" (um número só, denominador = toda a org). O split olha **duas taxas com denominadores diferentes**: trial = tentou/eligíveis; retorno = voltou/tentou. Confundir o denominador do retorno (dividir por eligíveis em vez de por quem tentou) destrói o diagnóstico — é a armadilha clássica que o exercício plaqueia com assert.

### Fronteiras do padrão (o que NÃO é este split)

1. **O split é diagnóstico, não terapêutico.** Ele não conserta nem produto nem ativação — ele só roteia a propriedade do fix (`...patterns.md:137`). A Parte 3 aplica intervenções de fora (vindas do dono certo); o split apenas re-verifica.

2. **Atribuição de ativação ≠ atribuição de custo.** O repositório já atribui custo de tokens por gap (`docs/canonical/token-economics-gap-filling.md:33`) e custo por trace (`docs/system-of-record.md:202`) — eixos diferentes. Aqui o objeto é **falha de adoção de usuário**, que não tinha instrumento nenhum (`...classification.yaml:119-123`).

3. **Retorno como denomina... como veredito de uso real.** O repositório já rastreia retenção como *métrica de outcome* (`docs/canonical/eval-to-production-correlation-tracking.md:35`), mas nunca como **eixo de diagnóstico de ativação**. A distinção: lá retenção valida se evals predizem produção; aqui retorno separa duas falhas operacionais com donos diferentes. O princípio vizinho é o mesmo — "eval scores viram falsos sinais de segurança quando param de predizer outcomes de usuário" (`docs/canonical/eval-to-production-correlation-tracking.md:22`): aqui, "uso agregado vira falso sinal de qualidade quando mistura quem nunca abriu".

4. **Roteamento de ativação ≠ roteamento de findings de QA.** O `docs/canonical/qa-to-backlog-feedback-loop.md:32` roteia *achados de review* por severidade/posse; aqui roteia *estados de população* (tentou/não-tentou). A gramática de triagem é emprestada, o objeto é novo.

5. **O ramo never-tried não é o Owner-Led Activation Blitz.** O blitz (demos em 60-70% do tempo do owner, dashboards por squad, ranking público) é o *tratamento* organizacional do ramo never-tried — classificado como integração `Low` e deliberadamente deixado fora do currículo (padrão só-organizacional sem casa curricular forte, `...classification.yaml:124-147`). Neste exercício o blitz entra como intervenção de dados (`InterventionKind.ACTIVATION_BLITZ`), não como mecânica a implementar.

### O Que Você Vai Construir

1. **`TelemetryInstrumenter` + `UserActivation`** (Parte 1 — Instrumentação): do log bruto de sessões + roster da org, computar por usuário a bandeira de trial (≥1 sessão na janela) e o retorno (ativo em ≥2 semanas distintas)
2. **`ActivationAggregator` + `AttributionRule`** (Parte 2 — Regra): taxas por squad com os denominadores certos + regra de dois ramos com guardas (coorte mínima, janela estável) e roteamento de dono
3. **`AttributionPipeline` + re-check** (Parte 3 — Pipeline): diagnóstico da org inteira, aplicação de intervenções do dono certo (`ProductFix` / `ActivationBlitz`) e re-diagnóstico na janela seguinte, provando que o split previne o rollback errado

O domínio é o KODA-Assist: 215 vendedores em 6 squads, duas semanas pós-GA — os números exatos do prólogo.

---

## ✅ Requisitos

### Funcionais

- [ ] `ActivationWindow.span_weeks` e `is_stable()` — janela estável requer `span_weeks >= MIN_WINDOW_WEEKS` (2)
- [ ] `UserActivation.trial_flag` é `True` com ≥1 semana ativa; `UserActivation.returning` é `True` com ≥`MIN_RETURN_WEEKS` (2) semanas distintas ativas
- [ ] `TelemetryInstrumenter.instrument()` retorna uma entrada para **cada usuário do roster** (usuário sem evento = `trial_flag False`, não registro ausente) e **ignora eventos fora da janela**
- [ ] `SquadActivationStats.trial_rate` = tentou/eligíveis; `return_rate` = voltou/**tentou** (0.0 se ninguém tentou) — denominadores distintos
- [ ] `AttributionRule.diagnose()` aplica, em ordem: guarda de janela (`INSUFFICIENT_DATA`), guarda de coorte (`eligible_users < MIN_COHORT` → `INSUFFICIENT_DATA`), ramo trial (`< TRIAL_FLOOR` → `CHANGE_MANAGEMENT`, dono `activation-owner`), ramo retorno (`< RETURN_FLOOR` → `PRODUCT_PROBLEM`, dono `product-team`), senão `HEALTHY` (dono `None`)
- [ ] `AttributionPipeline.run()` produz `ReCheckReport` com o diagnóstico de cada squad **e da org inteira** (a regra é scale-free: a org é tratada como um "squad" agregado)
- [ ] `apply_intervention()` retorna novas specs: `ProductFix` eleva `returning` do squad-alvo; `ActivationBlitz` eleva `tried` (e `returning` proporcionalmente) — nunca mexe no squad errado
- [ ] Após `ProductFix` no OUTBOUND e `ActivationBlitz` em RETAIL/PHARMACY/MARKETPLACE, o re-check W2 mostra: zero squads em `PRODUCT_PROBLEM`, zero em `CHANGE_MANAGEMENT` (entre elegíveis), e PILOT **continua** `INSUFFICIENT_DATA` (guarda sobrevive a blitz)

### Técnicos

- [ ] Python 3.9+ com type hints
- [ ] `dataclasses` para todos os modelos (`SessionEvent`, `RosterEntry`, `ActivationWindow`, `UserActivation`, `SquadActivationStats`, `AttributionDiagnosis`, `SquadSpec`, `Intervention`, `ReCheckReport`)
- [ ] `Enum` para `ActivationVerdict` e `InterventionKind`; roteamento de dono em constante nomeada (`OWNERSHIP_ROUTING`)
- [ ] `diagnose()` é determinístico, sem estado e sem I/O
- [ ] Thresholds (`TRIAL_FLOOR`, `RETURN_FLOOR`, `MIN_COHORT`, `MIN_WINDOW_WEEKS`, `MIN_RETURN_WEEKS`) são constantes nomeadas no módulo
- [ ] Dados de teste 100% determinísticos (gerados a partir de specs por squad — sem aleatoriedade)

### Validação

- [ ] Cenário 1: usuário com eventos só fora da janela → sem trial; usuário ativo em 1 semana → trial sem retorno; ativo em 3 semanas → trial + retorno
- [ ] Cenário 2: RETAIL tem `trial_rate == 10/48` e `return_rate == 9/10` (denominador é quem tentou)
- [ ] Cenário 3: OUTBOUND → `PRODUCT_PROBLEM` com dono `product-team`; RETAIL → `CHANGE_MANAGEMENT` com dono `activation-owner`; INBOUND → `HEALTHY` com dono `None`
- [ ] Cenário 4: PILOT (n=5) → `INSUFFICIENT_DATA` por coorte; janela de 1 semana → `INSUFFICIENT_DATA` para todos
- [ ] Cenário 5: diagnóstico da org (trial 44,2% < 60%, retorno 75,8% ≥ 70%) → `CHANGE_MANAGEMENT`, **nunca** `PRODUCT_PROBLEM` — o split desarma o rollback
- [ ] Cenário 6: re-check pós-intervenção — OUTBOUND vira `HEALTHY`, os três squads de ativação viram `HEALTHY`, PILOT continua bloqueado

---

## 🏗️ Arquitetura do Sistema

### Diagrama ASCII

```
┌──────────────────────────────────────────────────────────────────┐
│              TRIAL-RETENTION ATTRIBUTION SPLIT                    │
│                                                                   │
│  PARTE 1 — INSTRUMENTAÇÃO (o que o dashboard não fazia)           │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │  Roster (215 usuários)  +  Log de sessões (bruto)       │     │
│  │        │                        │                        │     │
│  │        └──────────┬─────────────┘                        │     │
│  │                   ▼                                      │     │
│  │       TelemetryInstrumenter.instrument(roster,           │     │
│  │                                 events, window)          │     │
│  │                   ▼                                      │     │
│  │  UserActivation { trial_flag, active_weeks, returning }  │     │
│  │   nunca abriu ────► trial_flag=False  (existe no mapa!)  │     │
│  │   abriu 1 semana ─► trial=True, returning=False          │     │
│  │   2+ semanas ─────► trial=True, returning=True           │     │
│  └───────────────────────────┬────────────────────────────────┘   │
│                              ▼                                    │
│  PARTE 2 — REGRA DE ATRIBUIÇÃO (dois ramos + guardas)             │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │  SquadActivationStats                                     │     │
│  │    trial_rate  = tentou / eligíveis                       │     │
│  │    return_rate = voltou  / TENTOU   ◄── denominador!      │     │
│  │                                                           │     │
│  │  GUARDAS (antes de qualquer ramo):                        │     │
│  │    janela estável? (>= 2 semanas)   não → INSUFFICIENT    │     │
│  │    coorte   >= MIN_COHORT (8)?      não → INSUFFICIENT    │     │
│  │                                                           │     │
│  │  RAMO 1: trial_rate < 0.60                                │     │
│  │    → CHANGE_MANAGEMENT · dono: activation-owner           │     │
│  │  RAMO 2: return_rate < 0.70                               │     │
│  │    → PRODUCT_PROBLEM    · dono: product-team              │     │
│  │  senão → HEALTHY · dono: None                             │     │
│  └───────────────────────────┬────────────────────────────────┘   │
│                              ▼                                    │
│  PARTE 3 — PIPELINE DE RE-CHECK (intervenção → re-diagnóstico)    │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │  W1: diagnose org + squads                                │     │
│  │        OUTBOUND 🐛 product  │ RETAIL/PHARMA/MKT 📣 change │     │
│  │                    │ dono certo aplica o fix              │     │
│  │                    ▼                                      │     │
│  │  ProductFix(OUTBOUND): semantic views → retorno sobe      │     │
│  │  ActivationBlitz(RETAIL, PHARMACY, MARKETPLACE):          │     │
│  │                    demos + dashboards → trial sobe         │     │
│  │                    ▼                                      │     │
│  │  W2: re-diagnose                                          │     │
│  │    PRODUCT_PROBLEM: []   CHANGE_MANAGEMENT: []            │     │
│  │    HEALTHY: 4 squads      PILOT: INSUFFICIENT (persiste)  │     │
│  │                                                           │     │
│  │  Invariante anti-rollback: org com trial baixo + retorno  │     │
│  │  alto NUNCA diagnostica PRODUCT_PROBLEM                   │     │
│  └──────────────────────────────────────────────────────────┘     │
└──────────────────────────────────────────────────────────────────┘
```

---

## 🎯 Sua Tarefa em 3 Partes

### Parte 1 — Instrumentação (`ActivationWindow`, `UserActivation`, `TelemetryInstrumenter`)
O dashboard da diretoria media "ativos na semana". Você precisa de duas coisas que ele não tinha: **quem nunca abriu** (por isso o roster entra — usuário sem evento precisa existir com `trial_flag False`) e **quem voltou** (semanas distintas ativas ≥ 2). Eventos fora da janela de medição são ruído e devem ser ignorados.

### Parte 2 — Regra de atribuição (`ActivationAggregator`, `AttributionRule`)
Taxas por squad com os denominadores certos, e a regra em dois ramos **depois** das guardas estatísticas: janela instável e coorte pequena diagnosticam nada (`INSUFFICIENT_DATA`) — o PILOT n=5 do prólogo existe exatamente para plaquear o erro de diagnosticar ruído. Cada veredito carrega seu dono via `OWNERSHIP_ROUTING`.

### Parte 3 — Pipeline de re-check (`AttributionPipeline`, `apply_intervention`)
Diagnóstico da org inteira (a org é um "squad" agregado — a regra se reutiliza sem código novo), aplicação das intervenções **do dono certo** e re-diagnóstico na janela seguinte. O invariante do pipeline: uma org com trial baixo e retorno alto jamais recebe veredito de produto — é isso que desarma o rollback na diretoria.

---

## 💻 Starter Code

```python
"""
Exercício 9 — Trial-Retention Attribution Split
Nível 3 — Arquitetura Avançada

Pipeline: instrumentação (trial flag + retorno semanal) → regra de
atribuição em dois ramos com guardas estatísticos → re-check pós-
intervenção com roteamento de propriedade.

Fonte do padrão: docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-
deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-
deploying-to-6000-users-analysis.md:48-51 (seção 1.6, Activation vs.
retention attribution split).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


# ============================================================================
# CONSTANTES DE THRESHOLD (os números do prólogo)
# ============================================================================

TRIAL_FLOOR = 0.60      # abaixo disso: change management (ninguém tentou)
RETURN_FLOOR = 0.70     # abaixo disso: problema de produto (tentaram, não voltaram)
MIN_COHORT = 8          # squad menor que isso não diagnostica nada
MIN_WINDOW_WEEKS = 2    # janela menor que isso é ruído de lançamento
MIN_RETURN_WEEKS = 2    # "voltou" = ativo em 2+ semanas distintas

OWNERSHIP_ROUTING = {
    # veredito → dono do fix (o split roteia propriedade, não aplica fix)
    "product_problem": "product-team",
    "change_management": "activation-owner",
}


class ActivationVerdict(Enum):
    PRODUCT_PROBLEM = "product_problem"        # tentou e não voltou
    CHANGE_MANAGEMENT = "change_management"    # nem tentou
    HEALTHY = "healthy"                        # passou nos dois pisos
    INSUFFICIENT_DATA = "insufficient_data"    # guarda estatística


# ============================================================================
# PARTE 1 — INSTRUMENTAÇÃO
# ============================================================================

@dataclass
class SessionEvent:
    """Uma sessão bruta do KODA-Assist (log de telemetria)."""
    user_id: str
    squad_id: str
    week: int          # semana relativa ao GA (0, 1, 2, ...)


@dataclass
class RosterEntry:
    """Um usuário elegível da org (mesmo que nunca tenha aberto o produto)."""
    user_id: str
    squad_id: str


@dataclass
class ActivationWindow:
    """Janela de medição, em semanas relativas ao GA (end inclusivo)."""
    start_week: int
    end_week: int

    @property
    def span_weeks(self) -> int:
        """TODO (Parte 1): quantidade de semanas cobertas (end - start + 1)."""
        # TODO: Implementar
        pass

    def is_stable(self) -> bool:
        """
        TODO (Parte 1): True quando span_weeks >= MIN_WINDOW_WEEKS.
        Janela de 1 semana é ruído de lançamento — não diagnostica.
        """
        # TODO: Implementar
        pass

    def contains(self, week: int) -> bool:
        """TODO (Parte 1): a semana está dentro [start_week, end_week]?"""
        # TODO: Implementar
        pass


@dataclass
class UserActivation:
    """
    Estado de ativação de UM usuário, computado da telemetria.

    trial_flag  — abriu o produto ao menos uma vez na janela
    returning   — voltou: ativo em >= MIN_RETURN_WEEKS semanas distintas
    """
    user_id: str
    squad_id: str
    active_weeks: set[int] = field(default_factory=set)

    @property
    def trial_flag(self) -> bool:
        """TODO (Parte 1): pelo menos 1 semana ativa."""
        # TODO: Implementar
        pass

    @property
    def returning(self) -> bool:
        """TODO (Parte 1): len(active_weeks) >= MIN_RETURN_WEEKS."""
        # TODO: Implementar
        pass


class TelemetryInstrumenter:
    """Transforma log bruto de sessões em estado de ativação por usuário."""

    @staticmethod
    def instrument(
        roster: list[RosterEntry],
        events: list[SessionEvent],
        window: ActivationWindow,
    ) -> dict[str, UserActivation]:
        """
        TODO (Parte 1): construir o mapa user_id -> UserActivation.

        Regras:
          - TODO usuário do roster recebe uma entrada (sem evento =>
            active_weeks vazio => trial_flag False). Usuário que nunca
            abriu É dado do diagnóstico, não registro ausente.
          - Eventos FORA da janela são ignorados (window.contains).
          - Eventos agregam a semana em active_weeks do usuário.
        """
        # TODO: Implementar
        pass


# ============================================================================
# PARTE 2 — AGREGAÇÃO E REGRA DE ATRIBUIÇÃO
# ============================================================================

@dataclass
class SquadActivationStats:
    """Taxas de ativação de um squad (ou da org agregada)."""
    squad_id: str
    eligible_users: int
    tried_users: int
    returning_users: int

    @property
    def trial_rate(self) -> float:
        """
        TODO (Parte 2): tentou / eligíveis.
        Denominador é a população toda — o ramo never-tried olha quem
        ficou de fora. Zero eligíveis => 0.0.
        """
        # TODO: Implementar
        pass

    @property
    def return_rate(self) -> float:
        """
        TODO (Parte 2): voltou / TENTOU (não eligíveis!).
        O retorno é condicional a ter experimentado — dividir por
        eligíveis diluiria o problema de produto com quem nem abriu.
        Zero tentativas => 0.0.
        """
        # TODO: Implementar
        pass


class ActivationAggregator:
    """Agrega ativação por usuário em stats por squad e da org."""

    @staticmethod
    def squad_stats(
        activations: dict[str, UserActivation],
    ) -> dict[str, SquadActivationStats]:
        """
        TODO (Parte 2): para cada squad presente nas ativações:
        eligible = todos os usuários do squad, tried = trial_flag True,
        returning = returning True.
        """
        # TODO: Implementar
        pass

    @staticmethod
    def org_stats(
        activations: dict[str, UserActivation],
    ) -> SquadActivationStats:
        """
        TODO (Parte 2): o mesmo, agregando TODOS os usuários num único
        SquadActivationStats com squad_id = ORG_SQUAD_ID. A org é tratada
        como um "squad" — a regra de atribuição é scale-free.
        """
        # TODO: Implementar
        pass


ORG_SQUAD_ID = "__ORG__"


@dataclass
class AttributionDiagnosis:
    """Veredito do split para um squad (ou a org)."""
    squad_id: str
    verdict: ActivationVerdict
    owner: str | None      # quem aplica o fix (None se HEALTHY/INSUFFICIENT)
    trial_rate: float
    return_rate: float
    rationale: str         # por que este ramo (texto para a diretoria)


class AttributionRule:
    """A regra em dois ramos, com guardas estatísticos antes de tudo."""

    @staticmethod
    def diagnose(stats: SquadActivationStats, window: ActivationWindow) -> AttributionDiagnosis:
        """
        TODO (Parte 2): aplicar EM ORDEM:

        1. Guarda de janela: not window.is_stable()
             → INSUFFICIENT_DATA ("janela instável")
        2. Guarda de coorte: stats.eligible_users < MIN_COHORT
             → INSUFFICIENT_DATA ("coorte pequena")
        3. Ramo 1: stats.trial_rate < TRIAL_FLOOR
             → CHANGE_MANAGEMENT, dono OWNERSHIP_ROUTING do veredito
        4. Ramo 2: stats.return_rate < RETURN_FLOOR
             → PRODUCT_PROBLEM, dono OWNERSHIP_ROUTING do veredito
        5. Senão → HEALTHY, dono None

        rationale deve nomear a taxa que disparou o ramo (o mecanismo
        que desarma a diretoria é um número, não um argumento).
        """
        # TODO: Implementar
        pass


# ============================================================================
# PARTE 3 — PIPELINE DE RE-CHECK
# ============================================================================

class InterventionKind(Enum):
    PRODUCT_FIX = "product_fix"            # dono: product-team
    ACTIVATION_BLITZ = "activation_blitz"  # dono: activation-owner


@dataclass
class SquadSpec:
    """Especificação determinística de um squad (gera os dados de teste)."""
    squad_id: str
    users: int        # elegíveis
    tried: int        # quantos abrem o produto na janela
    returning: int    # dos que abrem, quantos voltam (2+ semanas)


@dataclass
class Intervention:
    """Intervenção aplicada pelo DONO certo entre as janelas."""
    kind: InterventionKind
    target_squad: str
    new_tried: int | None = None       # blitz eleva trial
    new_returning: int | None = None   # product fix eleva retorno


def build_roster(specs: list[SquadSpec]) -> list[RosterEntry]:
    """
    Expande as specs no roster: usuários "u-<squad>-<i>".
    Implementado — determinístico, sem aleatoriedade.
    """
    roster: list[RosterEntry] = []
    for spec in specs:
        for i in range(spec.users):
            roster.append(RosterEntry(f"u-{spec.squad_id}-{i}", spec.squad_id))
    return roster


def build_events(specs: list[SquadSpec], week_offset: int) -> list[SessionEvent]:
    """
    Expande as specs em eventos, a partir da semana week_offset:

      - os primeiros `tried` usuários abrem o produto;
      - dos que abrem, os primeiros `returning` são ativos em 3 semanas
        (week_offset, +1, +2) => returning True;
      - o restante dos que abrem tem 1 semana só => trial sem retorno.

    Implementado — determinístico.
    """
    events: list[SessionEvent] = []
    for spec in specs:
        for i in range(spec.tried):
            user_id = f"u-{spec.squad_id}-{i}"
            if i < spec.returning:
                weeks = (week_offset, week_offset + 1, week_offset + 2)
            else:
                weeks = (week_offset,)
            for week in weeks:
                events.append(SessionEvent(user_id, spec.squad_id, week))
    return events


def apply_intervention(
    specs: list[SquadSpec], intervention: Intervention
) -> list[SquadSpec]:
    """
    TODO (Parte 3): retornar NOVAS specs (não mutar as originais),
    alterando APENAS o squad-alvo:
      - PRODUCT_FIX:      returning → new_returning (se dado)
      - ACTIVATION_BLITZ: tried → new_tried e returning → new_returning
    Squad não-alvo permanece idêntico.
    """
    # TODO: Implementar
    pass


@dataclass
class ReCheckReport:
    """Diagnóstico completo de uma janela: squads + org."""
    window_label: str
    diagnoses: dict[str, AttributionDiagnosis]  # squad_id -> diagnóstico

    @property
    def product_problem_squads(self) -> list[str]:
        """
        TODO (Parte 3): squads com veredito PRODUCT_PROBLEM
        (exclui a chave ORG_SQUAD_ID — o agregado da org não é squad).
        """
        # TODO: Implementar
        pass

    @property
    def change_management_squads(self) -> list[str]:
        """
        TODO (Parte 3): squads com veredito CHANGE_MANAGEMENT
        (exclui a chave ORG_SQUAD_ID).
        """
        # TODO: Implementar
        pass

    @property
    def healthy_squads(self) -> list[str]:
        """
        TODO (Parte 3): squads HEALTHY (exclui ORG_SQUAD_ID e os
        bloqueados por guarda — INSUFFICIENT_DATA não é saúde).
        """
        # TODO: Implementar
        pass

    @property
    def blocked_squads(self) -> list[str]:
        """
        TODO (Parte 3): squads INSUFFICIENT_DATA (guarda estatística;
        exclui ORG_SQUAD_ID).
        """
        # TODO: Implementar
        pass


class AttributionPipeline:
    """Instrumenta → agrega → diagnostica squads + org numa janela."""

    @staticmethod
    def run(window_label: str, specs: list[SquadSpec], window: ActivationWindow) -> ReCheckReport:
        """
        TODO (Parte 3): pipeline completo de UMA janela:
          1. roster + eventos a partir das specs (week_offset = window.start_week)
          2. instrument() com a janela
          3. squad_stats() + org_stats()
          4. diagnose() para cada squad E para a org (chave ORG_SQUAD_ID)
        """
        # TODO: Implementar
        pass


# ============================================================================
# DADOS DE TESTE (determinísticos — os números do prólogo)
# ============================================================================

def build_w1_specs() -> list[SquadSpec]:
    """
    Duas semanas pós-GA do KODA-Assist: 215 vendedores em 6 squads.
    INBOUND saudável; OUTBOUND com problema real de produto
    (semantic views de prospecção defasadas); RETAIL/PHARMACY/
    MARKETPLACE sem ativação; PILOT pequena demais para diagnosticar.
    """
    return [
        SquadSpec("SQUAD-INBOUND", 40, 36, 33),      # trial 90,0%  retorno 91,7% ✅
        SquadSpec("SQUAD-OUTBOUND", 32, 29, 12),     # trial 90,6%  retorno 41,4% 🐛
        SquadSpec("SQUAD-RETAIL", 48, 10, 9),        # trial 20,8%  retorno 90,0% 📣
        SquadSpec("SQUAD-PHARMACY", 44, 9, 8),       # trial 20,5%  retorno 88,9% 📣
        SquadSpec("SQUAD-MARKETPLACE", 51, 11, 10),  # trial 21,6%  retorno 90,9% 📣
        SquadSpec("SQUAD-PILOT", 5, 5, 4),           # n=5 < MIN_COHORT ⚠️
    ]


def build_w2_interventions() -> list[Intervention]:
    """Fixes do dono certo entre W1 e W2 (nada de rollback)."""
    return [
        # product-team refaz as semantic views de prospecção
        Intervention(InterventionKind.PRODUCT_FIX, "SQUAD-OUTBOUND", new_returning=26),
        # activation-owner: demos + dashboard por squad nos 3 squads 📣
        Intervention(InterventionKind.ACTIVATION_BLITZ, "SQUAD-RETAIL",
                     new_tried=38, new_returning=34),
        Intervention(InterventionKind.ACTIVATION_BLITZ, "SQUAD-PHARMACY",
                     new_tried=35, new_returning=31),
        Intervention(InterventionKind.ACTIVATION_BLITZ, "SQUAD-MARKETPLACE",
                     new_tried=41, new_returning=37),
    ]


W1 = ActivationWindow(0, 2)   # semanas 0-2 pós-GA (estável: 3 semanas)
W2 = ActivationWindow(4, 6)   # semanas 4-6, após as intervenções


# ============================================================================
# TESTES
# ============================================================================

def test_1_instrumentacao_trial_e_retorno():
    """Cenário 1: trial flag e retorno computados do log bruto."""
    print("\n" + "=" * 60)
    print("TESTE 1: Instrumentação — Trial Flag e Retorno")
    print("=" * 60)

    specs = [SquadSpec("SQUAD-X", 10, 4, 3)]
    roster = build_roster(specs)
    events = build_events(specs, week_offset=0)

    acts = TelemetryInstrumenter.instrument(roster, events, ActivationWindow(0, 2))

    assert len(acts) == 10, "TODO usuário do roster recebe entrada (mesmo sem evento)"
    tried = [a for a in acts.values() if a.trial_flag]
    returning = [a for a in acts.values() if a.returning]
    never = [a for a in acts.values() if not a.trial_flag]

    print(f"\n  Usuários: {len(acts)}  tentaram: {len(tried)}  "
          f"voltaram: {len(returning)}  nunca: {len(never)}")

    assert len(tried) == 4, "4 usuários com evento => trial"
    assert len(returning) == 3, "3 ativos em 3 semanas => returning"
    assert len(never) == 6, "6 sem evento => trial_flag False (e existem!)"

    # Eventos fora da janela são invisíveis
    acts_fora = TelemetryInstrumenter.instrument(
        roster, events, ActivationWindow(10, 12)
    )
    assert all(not a.trial_flag for a in acts_fora.values()), (
        "Eventos das semanas 0-2 não podem vazar para a janela 10-12"
    )
    print("  TESTE 1 PASSOU")


def test_2_taxas_e_denominadores():
    """Cenário 2: trial divide por eligíveis; retorno divide por QUEM TENTOU."""
    print("\n" + "=" * 60)
    print("TESTE 2: Taxas por Squad — Denominadores Certos")
    print("=" * 60)

    acts = TelemetryInstrumenter.instrument(
        build_roster(build_w1_specs()), build_events(build_w1_specs(), 0), W1
    )
    stats = ActivationAggregator.squad_stats(acts)
    retail = stats["SQUAD-RETAIL"]
    outbound = stats["SQUAD-OUTBOUND"]

    print(f"\n  RETAIL:   trial={retail.trial_rate:.3f}  retorno={retail.return_rate:.3f}")
    print(f"  OUTBOUND: trial={outbound.trial_rate:.3f}  retorno={outbound.return_rate:.3f}")

    assert retail.trial_rate == 10 / 48, "trial = tentou / eligíveis"
    assert retail.return_rate == 9 / 10, (
        "retorno = voltou / TENTOU (9/10 = 0.9), nao voltou/eligiveis (9/48)"
    )
    assert outbound.return_rate == 12 / 29, "denominador do retorno e quem tentou"
    assert stats["SQUAD-PILOT"].return_rate == 4 / 5, "piloto: 4/5 entre os que tentaram"
    print("  TESTE 2 PASSOU")


def test_3_regra_dois_ramos():
    """Cenário 3: os dois ramos com donos roteados."""
    print("\n" + "=" * 60)
    print("TESTE 3: Regra de Atribuição — Dois Ramos")
    print("=" * 60)

    acts = TelemetryInstrumenter.instrument(
        build_roster(build_w1_specs()), build_events(build_w1_specs(), 0), W1
    )
    stats = ActivationAggregator.squad_stats(acts)

    outbound = AttributionRule.diagnose(stats["SQUAD-OUTBOUND"], W1)
    retail = AttributionRule.diagnose(stats["SQUAD-RETAIL"], W1)
    inbound = AttributionRule.diagnose(stats["SQUAD-INBOUND"], W1)

    print(f"\n  OUTBOUND: {outbound.verdict.value:18s} dono={outbound.owner}")
    print(f"  RETAIL:   {retail.verdict.value:18s} dono={retail.owner}")
    print(f"  INBOUND:  {inbound.verdict.value:18s} dono={inbound.owner}")

    assert outbound.verdict == ActivationVerdict.PRODUCT_PROBLEM
    assert outbound.owner == "product-team", "tentou e nao voltou => produto"
    assert "41" in outbound.rationale or "retorno" in outbound.rationale.lower()

    assert retail.verdict == ActivationVerdict.CHANGE_MANAGEMENT
    assert retail.owner == "activation-owner", "nem tentou => change management"

    assert inbound.verdict == ActivationVerdict.HEALTHY
    assert inbound.owner is None
    print("  TESTE 3 PASSOU")


def test_4_guardas_estatisticos():
    """Cenário 4: coorte pequena e janela instável não diagnosticam nada."""
    print("\n" + "=" * 60)
    print("TESTE 4: Guardas Estatísticos")
    print("=" * 60)

    acts = TelemetryInstrumenter.instrument(
        build_roster(build_w1_specs()), build_events(build_w1_specs(), 0), W1
    )
    stats = ActivationAggregator.squad_stats(acts)

    pilot = AttributionRule.diagnose(stats["SQUAD-PILOT"], W1)
    print(f"\n  PILOT (n=5): {pilot.verdict.value}")
    assert pilot.verdict == ActivationVerdict.INSUFFICIENT_DATA, (
        "n=5 < MIN_COHORT: taxas boas nao autorizam diagnostico"
    )
    assert pilot.owner is None

    # Janela de 1 semana: ate o INBOUND saudavel fica bloqueado
    instavel = ActivationWindow(0, 0)
    assert not instavel.is_stable(), "janela de 1 semana e instavel"
    inbound_instavel = AttributionRule.diagnose(stats["SQUAD-INBOUND"], instavel)
    print(f"  INBOUND em janela de 1 semana: {inbound_instavel.verdict.value}")
    assert inbound_instavel.verdict == ActivationVerdict.INSUFFICIENT_DATA
    print("  TESTE 4 PASSOU")


def test_5_split_previne_rollback():
    """Cenário 5: org com trial baixo + retorno alto NUNCA e problema de produto."""
    print("\n" + "=" * 60)
    print("TESTE 5: O Split Desarma o Rollback")
    print("=" * 60)

    acts = TelemetryInstrumenter.instrument(
        build_roster(build_w1_specs()), build_events(build_w1_specs(), 0), W1
    )
    org = ActivationAggregator.org_stats(acts)
    diag = AttributionRule.diagnose(org, W1)

    print(f"\n  ORG: trial={diag.trial_rate:.3f}  retorno={diag.return_rate:.3f}")
    print(f"       veredito={diag.verdict.value}  dono={diag.owner}")
    print(f"       {diag.rationale}")

    assert org.trial_rate == 95 / 215, "44,2% da org tentou (95/215)"
    assert org.return_rate == 72 / 95, "75,8% dos que tentaram voltaram (72/95)"
    assert diag.verdict == ActivationVerdict.CHANGE_MANAGEMENT, (
        "trial 44,2% < 60% com retorno 75,8% >= 70% => change management"
    )
    assert diag.verdict != ActivationVerdict.PRODUCT_PROBLEM, (
        "uso baixo causado por never-tried nao e veredito de produto"
    )
    assert diag.owner == "activation-owner"
    print("  TESTE 5 PASSOU")


def test_6_recheck_pos_intervencao():
    """Cenário 6: dono certo aplica o fix; re-check mostra a org convergindo."""
    print("\n" + "=" * 60)
    print("TESTE 6: Re-Check Pós-Intervenção")
    print("=" * 60)

    report_w1 = AttributionPipeline.run("W1", build_w1_specs(), W1)
    print(f"\n  W1 produto:     {report_w1.product_problem_squads}")
    print(f"     change mgmt: {report_w1.change_management_squads}")
    print(f"     saudáveis:   {report_w1.healthy_squads}")
    print(f"     bloqueados:  {report_w1.blocked_squads}")

    assert report_w1.product_problem_squads == ["SQUAD-OUTBOUND"]
    assert sorted(report_w1.change_management_squads) == [
        "SQUAD-MARKETPLACE", "SQUAD-PHARMACY", "SQUAD-RETAIL"
    ]
    assert report_w1.healthy_squads == ["SQUAD-INBOUND"]
    assert report_w1.blocked_squads == ["SQUAD-PILOT"]

    # Donos aplicam os fixes entre janelas
    specs_w2 = build_w1_specs()
    for intervention in build_w2_interventions():
        specs_w2 = apply_intervention(specs_w2, intervention)

    report_w2 = AttributionPipeline.run("W2", specs_w2, W2)
    print(f"\n  W2 produto:     {report_w2.product_problem_squads}")
    print(f"     change mgmt: {report_w2.change_management_squads}")
    print(f"     saudáveis:   {sorted(report_w2.healthy_squads)}")
    print(f"     bloqueados:  {report_w2.blocked_squads}")

    assert report_w2.product_problem_squads == [], "product fix resolveu OUTBOUND"
    assert report_w2.change_management_squads == [], "blitz resolveu a ativacao"
    assert sorted(report_w2.healthy_squads) == [
        "SQUAD-INBOUND", "SQUAD-MARKETPLACE", "SQUAD-OUTBOUND",
        "SQUAD-PHARMACY", "SQUAD-RETAIL",
    ]
    assert report_w2.blocked_squads == ["SQUAD-PILOT"], (
        "guarda de coorte sobrevive a blitz: n=5 continua sem diagnostico"
    )
    print("  TESTE 6 PASSOU")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("EXERCÍCIO 9: TRIAL-RETENTION ATTRIBUTION SPLIT")
    print("=" * 60)

    # Quando implementado, descomente para testar:
    # test_1_instrumentacao_trial_e_retorno()
    # test_2_taxas_e_denominadores()
    # test_3_regra_dois_ramos()
    # test_4_guardas_estatisticos()
    # test_5_split_previne_rollback()
    # test_6_recheck_pos_intervencao()

    print("\nTODO: Implemente as partes acima!")
    print("   1. ActivationWindow.span_weeks / is_stable / contains")
    print("   2. UserActivation.trial_flag / returning")
    print("   3. TelemetryInstrumenter.instrument()")
    print("   4. SquadActivationStats.trial_rate / return_rate (denominadores!)")
    print("   5. ActivationAggregator.squad_stats / org_stats")
    print("   6. AttributionRule.diagnose() com guardas e dois ramos")
    print("   7. apply_intervention() + ReCheckReport + AttributionPipeline.run()")
    print("   Após implementar, descomente os testes em main()")
```

---

## ✅ Validação: Critérios de Aceitação

Seu código será considerado **APROVADO** quando:

### Critério 1: Instrumentação (Parte 1)

- [ ] Usuário do roster sem evento aparece no mapa com `trial_flag == False`
- [ ] Ativo em 1 semana → trial sem retorno; ativo em 2+ semanas → trial + retorno
- [ ] Eventos fora da janela de medição são ignorados
- [ ] `is_stable()` retorna `False` para janela de 1 semana

### Critério 2: Taxas e denominadores (Parte 2)

- [ ] `trial_rate` divide por **eligíveis** (RETAIL: 10/48)
- [ ] `return_rate` divide por **tentou** (RETAIL: 9/10 — não 9/48)
- [ ] Denominador zero retorna 0.0 sem exceção

### Critério 3: Regra com guardas e roteamento (Parte 2)

- [ ] Guardas (janela, coorte) executam **antes** dos ramos
- [ ] OUTBOUND → `PRODUCT_PROBLEM` dono `product-team`; RETAIL → `CHANGE_MANAGEMENT` dono `activation-owner`; INBOUND → `HEALTHY` dono `None`
- [ ] PILOT (n=5) → `INSUFFICIENT_DATA` mesmo com taxas boas
- [ ] `rationale` nomeia a taxa/rama que disparou o veredito

### Critério 4: Pipeline de re-check (Parte 3)

- [ ] Diagnóstico da org reutiliza a mesma regra (scale-free) e retorna `CHANGE_MANAGEMENT` — nunca `PRODUCT_PROBLEM`
- [ ] `ProductFix` altera só `returning` do squad-alvo; `ActivationBlitz` altera `tried`/`returning` — specs originais não são mutadas
- [ ] W2: zero `PRODUCT_PROBLEM`, zero `CHANGE_MANAGEMENT`, 5 squads `HEALTHY`, PILOT persiste `INSUFFICIENT_DATA`

---

## 📊 Rubric de Avaliação

| Critério | Peso | Insuficiente (0-3) | Básico (4-6) | Proficiente (7-8) | Excelente (9-10) |
|---|---|---|---|---|---|
| **Instrumentação (Parte 1)** | 20% | Não implementado | Computa trial mas perde usuários sem evento | Trial + retorno corretos com janela filtrando eventos | Roster como fonte de eligíveis + imutabilidade de eventos fora da janela explicitadas |
| **Taxas + Regra (Parte 2)** | 35% | Não implementado | Denominadores trocados (retorno/eligíveis) | Dois ramos corretos com guardas antes e donos roteados | Rationale por ramo nomeando a taxa disparadora; regra scale-free reutilizada para a org |
| **Pipeline de re-check (Parte 3)** | 30% | Não implementado | Diagnostica W1 mas não aplica intervenções | Intervenções imutáveis + re-diagnóstico W2 com guardas persistindo | Sequência W1→W2 auditável mostrando a org convergindo squad por squad |
| **Interpretação anti-misattribution** | 15% | Repete o veredito agregado da diretoria | Distingue os ramos mas sem donos | Split roteia dono e previne o rollback no cenário org | Explica por que uso agregado é falso sinal de qualidade (analogia com eval-vs-produção) |

**Nota final:** Média ponderada. **Aprovação:** >= 7.0

---

## 💡 Dicas para Implementação

### Para a instrumentação

1. **O roster é a fonte da verdade da população.** Construir o mapa só a partir dos eventos apagaria exatamente a população que define o ramo never-tried — quem nunca abriu não deixa evento. Iterar o roster e enriquecer com eventos é a ordem certa.
2. **`returning` é sobre semanas distintas, não sessões.** Um usuário entusiasmado com 5 sessões na semana de lançamento tentou; não voltou. `active_weeks` é um `set[int]` — a estrutura já modela a semântica.

### Para a regra

1. **Guardas antes de ramos, sempre.** O PILOT tem retorno 80% e trial 100% — taxas lindas, população minúscula. Diagnosticar ruído é como declarar vitória com eval de 3 casos; o repositório exige dataset mínimo para benchmark (`MIN_EVAL_CASES` no Exercício 7) pela mesma razão estatística.
2. **O denominador do retorno é quem tentou.** É o erro mais comum do exercício: dividir retorno por eligíveis mistura as duas doenças num número só — exatamente o que o dashboard da diretoria fazia. O split existe para separar o que o denominador errado mistura.
3. **A regra é scale-free de propósito.** Squad, região ou org inteira: mesmas guardas, mesmos pisos, mesmos donos. Se você escreveu `diagnose_org()` com lógica própria, você duplicou a regra — reutilize `diagnose()` com o `SquadActivationStats` agregado.

### Para o pipeline

1. **Intervenção não é mutação.** `apply_intervention` devolve specs novas: o re-check precisa das duas janelas lado a lado para ser auditável (W1 vs W2 é o argumento que convence a diretoria na segunda reunião).
2. **A blitz não compra diagnóstico.** O PILOT continua `INSUFFICIENT_DATA` em W2 mesmo depois de intervenção — a guarda é sobre a população, não sobre a intenção. Isso é feature, não bug.

---

## ❓ Dúvidas Comuns

**P: Por que 60% de piso de trial, se o caso Snowflake tinha só 20%?**
R: Os pisos são parâmetros da org, não constantes universais. `TRIAL_FLOOR = 0.60` codifica "a diretoria só lê o ramo de produto quando a maioria da população experimentou"; com 44,2% de trial, o veredito org é change management. O caso real (20%) estaria ainda mais profundamente no mesmo ramo. O exercício ensina a mecânica; o calibramento é decisão de cada lançamento.

**P: Retorno semanal não é o mesmo gate de retenção do rollout faseado?**
R: São usos diferentes do mesmo sinal. No rollout faseado, retenção >70% é **gate de avanço** (beta → GA). Aqui, retorno é **eixo de diagnóstico** — separa problema de produto de problema de ativação depois do GA. O repositório já rastreia retenção como outcome (`docs/canonical/eval-to-production-correlation-tracking.md:35`); o que este exercício adiciona é o uso atributivo, com dono roteado por ramo.

**P: Isso não é só "segmentar o dashboard por squad"?**
R: Segmentar por squad mostraria os mesmos números sem o veredito. O split tem três peças que um dashboard não tem: bandeira de trial **por usuário** (quem nunca abriu), a **regra** que mapeia taxas → doença → dono, e o **re-check** que fecha o loop depois da intervenção. Sem a regra, os números continuam abertos a interpretação da diretoria — que era o problema original.

**P: O que faço com o ramo never-tried na vida real?**
R: O dono roteado (`activation-owner`) aplica o tratamento organizacional: demos ao vivo, dashboards de adoção por squad, patrocínio de liderança. Essa mecânica (Owner-Led Activation Blitz) foi classificada como integração `Low` e ficou fora do currículo por decisão do repositório — padrões só-organizacionais sem casa curricular forte (`...classification.yaml:124-147`). Aqui ela entra só como `InterventionKind.ACTIVATION_BLITZ` nos dados.

**P: Por que `INSUFFICIENT_DATA` em vez de tratar o PILOT como saudável (taxas boas)?**
R: Porque o inverso do ruído também é ruído. Com n=5, o intervalo de confiança das taxas é enorme — o PILOT poderia estar em qualquer veredito. Declarar `HEALTHY` por taxas favoráveis é o mesmo erro estatístico de declarar `PRODUCT_PROBLEM` por taxas ruins: ler sinal onde só há variância.

---

## 🚀 Próximo Passo

Depois de completar este exercício:

1. Leia a seção 1.6 ("Activation vs. retention attribution split") e o failure pattern correspondente em `docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-analysis.md:48-51` e `:153` — e a entrada completa da classificação `Missing` em `...classification.yaml:99-123`
2. Compare com `docs/canonical/eval-to-production-correlation-tracking.md:22` — mesmo princípio de falso sinal (eval que não prediz produção ↔ uso agregado que não mede qualidade), objeto diferente
3. Continue para o [[curriculum/03-nivel-3-advanced-architecture/exercises/exercise-10-agent-value-maturity-ladder|Exercício 10: Agent Value Maturity Ladder]] — a continuação da mesma história: meses depois, os vendedores que o split ativou se habituaram ao produto, o "wow" virou linha de base, e a pergunta vira "para onde vai a escada de valor"

---

*Exercício 9 | Nível 3 — Arquitetura Avançada | Trial-Retention Attribution Split*

**Uso baixo não é veredito de produto até o split dizer qual doença ele é.**
