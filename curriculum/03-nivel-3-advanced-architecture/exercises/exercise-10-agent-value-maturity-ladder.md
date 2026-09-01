---
title: "Exercício 10: Agent Value Maturity Ladder — Auditar o Roadmap Contra a Escada de Valor"
type: curriculum-exercise
nivel: 3
aliases: ["agent value maturity ladder", "value maturity ladder", "escada de maturidade de valor", "escada de valor", "switching cost ladder", "habituation listener", "wow collapse", "colapso do wow", "hiper-personalização"]
tags: ["curriculo-conteudo", "nivel-3", "evals", "production", "analise-estrutural", "governanca", "stack-tooling"]
relates-to: ["[[docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-analysis|GTM AI Agents Analysis]]", "[[docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-classification|GTM AI Agents Classification]]", "[[docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-patterns|GTM AI Agents Patterns]]", "[[docs/canonical/autonomy-curriculum-sampling|Autonomy Curriculum Sampling]]", "[[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]]", "[[docs/canonical/eval-to-production-correlation-tracking|Eval-to-Production Correlation Tracking]]", "[[curriculum/03-nivel-3-advanced-architecture/05-harness-evolution|Harness Evolution]]", "[[curriculum/03-nivel-3-advanced-architecture/exercises/exercise-09-trial-retention-attribution-split|Exercício 9: Trial-Retention Attribution Split]]"]
last_updated: 2026-08-30
---

# 🪜 Exercício 10: Agent Value Maturity Ladder — Auditar o Roadmap Contra a Escada de Valor
## Nível 3 — Arquitetura Avançada

**Tempo Estimado:** 90-120 minutos
**Dificuldade:** ⭐⭐⭐⭐ (Avançado)
**Pré-requisito:** Ter lido `05-harness-evolution.md` (Nível 3) + Exercício 9 (`exercise-09-trial-retention-attribution-split.md`)
**Objetivo:** Modelar a escada de valor de um agente em quatro estágios — talk-to-data → automate-workflows → team-empowerment → hyper-personalization — com listener de habituação que detecta o colapso do "wow" (Parte 1), auditar um roadmap de deploy contra a escada detectando degraus pulados, estágios não-ganhos e risco de estagnação fora da cadência de 1-2 meses (Parte 2), e reparar o plano reordenando os estágios enquanto verifica que cada degrau eleva o custo de troca — o lock-in que novidade crua não compra (Parte 3)

---

## 📖 Prólogo: O Encontro Que o ChatGPT Roubou

**Quatro meses depois do GA do KODA-QA. Revisão trimestral do KODA-Assist. O estágio 1 — "converse com seus dados" — foi um sucesso estrondoso: 215 vendedores escaparam da fila de duas semanas dos analistas. O clima na sala, hoje, é outro.**

```
DIRETORIA:   "Uso do KODA-QA: estabilizou. Estabilizou é palavra
             bonita para 'parou de crescer'. E olhem os comentários
             do NPS interno do mês."

ANALISTA:    "▸ 'no começo era mágico, agora é... o básico'
             ▸ 'o ChatGPT do meu irmão monta uma tabela melhor'
             ▸ 'quando ele mesmo escreve o rascunho de e-mail
                pro meu cliente?'
             ▸ (um vendedor, São Paulo): 'se não melhorar, eu
                volto pro meu fluxo de planilha. Dá no mesmo.'"

HEAD DE GS:  "Eu digo o que a gente faz: o próximo lançamento tem
             que ser GRANDE. CRM hiper-personalizado — a IA escreve
             e-mail por vendedor, conhece cada cliente, agenda,
             acompanha. Hiper-personalização total. Apresentação
             pronta, o comitê adora."

ARQUITETA:   "Antes de o comitê adorar: esse plano pula do degrau
             1 direto pro degrau 4."

HEAD DE GS:  "Degrau?"

ARQUITETA:   "A jornada de valor de um agente é uma escada:

               4. HIPER-PERSONALIZAÇÃO  (contexto vivo por vendedor)
               3. EMPODERAMENTO DO TIME (squads criam próprios skills)
               2. AUTOMATAR WORKFLOWS   (monitora, rascunha, humano revisa)
               1. CONVERSAR COM DADOS   (KODA-QA — onde estamos)

             Três regras dessa escada:

             Regra 1 — o wow COLAPSA. O que hoje é 'mágico' vira
             linha de base em meses. Vocês estão ouvindo esse
             colapso acontecer nos comentários do NPS.

             Regra 2 — cada degrau só se sustenta na confiança do
             anterior. Pular pro degrau 4 sem nunca ter entregue
             automação de workflow (degrau 2) queima a confiança
             de que a escada inteira depende — e o vendedor que ameaçou
             voltar pra planilha não vai perdoar um salto de
             grife que falhe.

             Regra 3 — o remédio pra habituação não é um salto
             maior, é o PRÓXIMO DEGRAU NA CADÊNCIA. Um a dois
             meses por estágio. O degrau 2 que vocês têm na
             gaveta há dois meses — monitorar inbox, rascunhar
             resposta, vendedor revisa e envia — é exatamente o
             que os comentários estão pedindo ('quando ele mesmo
             escreve o rascunho?').

             E tem um bônus que o plano do GS não compra: cada
             degrau subido eleva o custo de troca. Dados na
             plataforma = hábito. Workflows automatizados = o
             trabalho do vendedor TECE o produto. Skills do time
             = os próprios squads constroem em cima. Contexto
             pessoal = insubstituível. Isso é lock-in que
             novidade nenhuma compra — e a escada é a única
             forma de construí-lo sem trair a confiança."

DIRETORIA:   "Então me provem. Auditorem o plano do GS contra
             essa escada — números, não adjetivos."
```

**A auditoria que você vai implementar encontrou, no plano original:**

```
╔══════════════════════════════════════════════════════════════════╗
║           AUDITORIA DO PLANO "KODA-ASSIST-ORIGINAL"              ║
║           (auditado no mês 4)                                     ║
║                                                                  ║
║  Itens:                                                          ║
║   P1  Converse com seus dados        estágio 1  mês 0  ✅ shippado║
║   P2  CRM hiper-personalizado        estágio 4  mês 6  ⏳ plano  ║
║                                                                  ║
║  Sinais (estágio 1):                                             ║
║   mês 1  wow           "escaparam da fila de analistas"          ║
║   mês 2  habituação    "ninguém mais comenta nas reuniões"       ║
║   mês 3  habituação    "virou ferramenta padrão do dia a dia"    ║
║   mês 4  comparação    "o ChatGPT monta tabela melhor"           ║
║   mês 4  demanda       "quando ele mesmo escreve o rascunho?"    ║
║   mês 5  demanda       "quero que ele monitore meu inbox"        ║
║                                                                  ║
║  FINDINGS:                                                       ║
║   🟥 SKIPPED_STAGE    P2 pula os degraus 2 e 3 — não existem     ║
║                       no plano                                   ║
║   🟥 UNEARNED_STAGE   P2 (estágio 4, mês 6) shipa com os estágios ║
║                       2 e 3 não-shippados — confiança não ganhada║
║   🟥 STALL_RISK       Estágio 1 habitua no mês 3; próximo ship   ║
║                       no mês 6 → gap de 3 meses > cadência de 2. ║
║                       Meses 3-5 expostos a churn ("volto pra     ║
║                       planilha")                                 ║
║                                                                  ║
║  Custo de troca do estado no mês 6: {1,4} = 1.0 + 3.0 = 4.0     ║
║  Custo de troca da escada completa: {1,2,3,4} = 8.5              ║
╚══════════════════════════════════════════════════════════════════╝
```

O plano foi reparado na própria reunião: estágio 2 no mês 5 (a automação com revisão humana que estava na gaveta), estágio 3 no mês 7, estágio 4 no mês 9 — cadência de 2 meses por degrau, zero findings, e o custo de troca acumulado mais que dobra (8.5 vs 4.0) sem pular confiança nenhuma.

**Sua missão:** implementar a auditoria completa — modelagem da escada e do listener de habituação, os checks que pegam o plano do GS, e o reparo com auditoria de custo de troca e simulação do colapso do wow. Este padrão não existe em nenhum lugar do repositório (classificado como `Missing` em `docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-classification.yaml:348-369`) — você está construindo a primeira implementação.

---

## 🧠 O Contexto

### O Modelo Mental: Quatro Estágios de Valor, Uma Escada de Custos de Troca

O padrão vem do caso Snowflake: a jornada observada dos times de venda conforme a capacidade do agente aprofunda (`docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-analysis.md:62-67`):

| Estágio | Nome | O que o usuário ganha | Custo de troca criado |
|---|---|---|---|
| 1 | **Talk to your data** | Democratização de dados; fuga de 1.000 dashboards e filas de 2 semanas dos analistas | Hábito de dados na plataforma (peso 1.0) |
| 2 | **Automate my workflows** | Orquestração via conexões externas: monitora inbox/Slack, rascunha respostas, humano revisa e envia | O trabalho diário do usuário tece o produto (peso 2.5) |
| 3 | **Team empowerment** | Squads constroem próprios skills, dashboards, apps, automações, alertas | Artefatos do time vivem na plataforma (peso 2.0) |
| 4 | **Hyper-personalization** | Tudo personalizado por vendedor E por cliente, com contexto vivo | Contexto pessoal insubstituível (peso 3.0) |

A tese estratégica tem duas metades que se sustentam:

1. **O wow colapsa.** O status de "rockstar" decai em meses; a capacidade vira hábito, depois linha de base — e os usuários voltam com frustrações e comparações com outros produtos de IA (`...analysis.md:57-60`). A postura operacional é paranoia institucionalizada: "toda vez que as pessoas estão felizes, você deveria estar paranoico" — planeje o que mostrar daqui a um ou dois meses (`...analysis.md:59`). Parado em qualquer estágio, a disrupção chega em 1-2 meses porque o custo de troca é quase zero até você construí-lo (`...analysis.md:60`).

2. **A escada é a resposta.** Cada estágio eleva a dependência do usuário na plataforma — lock-in estratégico que novidade crua não ganha; a confiança ganha em cada estágio compra o direito de iterar no seguinte (`...analysis.md:167`). A síntese do caso é literal: o modelo de maturidade em quatro estágios **também é uma escada de custo de troca** (`...analysis.md:167`).

A cadência importa tanto quanto a ordem: um a dois meses por próximo estágio (`...patterns.md:432`), com o listener de sinais de habituação/frustração dizendo quando o relógio começou a correr (`...patterns.md:431`).

### Fronteiras do padrão (o que NÃO é esta escada)

1. **Escada de valor de produto ≠ escada de autonomia de agente.** O repositório já tem uma escada famosa — Observe → Assist → Own — mas ela mede a autonomia de *execução do agente* numa tarefa (`docs/canonical/autonomy-curriculum-sampling.md:60`), com gates de prontidão por fase (`:58`). Objeto errado: aqui os degraus são *estágios de valor percebido pelo usuário do produto*. A classificação é explícita: "nearest ladder, wrong object" (`...classification.yaml:358-359`).

2. **Escada de valor ≠ lifecycle de componente.** O `docs/canonical/measured-harness-evolution-lifecycle.md:29` modela harness como lifecycle medido — progressão de *infraestrutura*, não de valor de produto. Complementares: o lifecycle governa como o harness evolui por dentro; a escada governa o que o usuário recebe a cada onda.

3. **Estágio 2 não é autonomia plena — o envio irreversível é humano.** A automação do degrau 2 do caso original é monitorar canais → rascunhar no Gmail → **vendedor revisa e envia** (`...analysis.md:65`). O exercício plaqueia isso no item R2 do plano reparado: "rascunho com revisão humana". Autonomia sem gate é outro padrão (e outro exercício).

4. **Pular degrau não é ambição, é dívida de confiança.** "Skipping stages burns the trust the ladder depends on" (`...patterns.md:428`): estágios pressupõem a confiança dos anteriores. O plano do GS (1 → 4) não é ousado; é a mesma aposta de novidade que já está colapsando no estágio 1 — agora com mais superfície de falha.

5. **Habituação não é retenção.** O Exercício 9 usou retorno semanal para separar problema de produto de problema de ativação; aqui, o listener de habituação roteia a *próxima entrega da escada* — o usuário pode estar retido (volta toda semana) e ainda assim habituado (o wow morreu, o churn está cronometrado). Métricas de produção como retenção são o chão (`docs/canonical/eval-to-production-correlation-tracking.md:35`); o sinal de habituação é o teto que está descendo.

### O Que Você Vai Construir

1. **`ValueStage` + `HabituationListener`** (Parte 1 — Modelagem): os quatro estágios com pesos de custo de troca, e o listener que classifica o estado de um estágio (`wow` / `habituated` / `frustrated`) a partir dos sinais de adoção
2. **`DeploymentPlanAudit`** (Parte 2 — Auditoria): os três checks de bloqueio — `SKIPPED_STAGE` (degrau sem item no plano), `UNEARNED_STAGE` (item que shipa antes do predecessor) e `STALL_RISK` (habituação detectada com próximo ship fora da cadência de 2 meses) — mais o check de instrumentação `MISSING_SIGNALS`
3. **`SwitchingCostAudit` + `WowCollapseSimulator`** (Parte 3 — Reparo): o plano reparado passa limpo na re-auditoria, cada degrau soma custo de troca monotonicamente, e a simulação mostra os meses expostos a churn do plano original (3, 4, 5) zerando no reparado

O domínio é o KODA-Assist do Exercício 9, quatro meses depois: o KODA-QA (estágio 1) habitucou, e o roadmap na mesa pula para o estágio 4.

---

## ✅ Requisitos

### Funcionais

- [ ] `ValueStage` tem os 4 estágios com `.value` na ordem 1→4 e `SWITCHING_COST_WEIGHTS` cobre todos
- [ ] `HabituationListener.stage_status()` retorna: `frustrated` se qualquer sinal `frustration`/`comparison` no estágio até o mês; `habituated` se >= `HABITUATION_THRESHOLD` (2) sinais de `habituation`; senão `wow`. Sinais `wow` e `demand_next` não mudam o estado — demanda do próximo estágio é apetite, não churn
- [ ] `DeploymentPlan.shipped_stages(at_month)` retorna estágios com item de `ship_month <= at_month`; `next_ship_month(after_month)` retorna o menor `ship_month` > `after_month` entre os itens (ou `None`)
- [ ] `DeploymentPlanAudit.audit()` produz, na ordem: `MISSING_SIGNALS` (medium) se a lista de sinais for vazia; `SKIPPED_STAGE` (high) para cada item de estágio k com algum degrau j < k **sem nenhum item no plano**; `UNEARNED_STAGE` (high) para cada item de estágio k cujos degraus j < k não estão shippados no `ship_month` do item; `STALL_RISK` (high) se o estágio ativo no mês da auditoria sai de `wow` no mês `detection` e o próximo ship após `detection` demora mais que `CADENCE_MAX_MONTHS` (ou não existe)
- [ ] `PlanAudit.has_blocking_findings` é `True` com qualquer finding high
- [ ] `SwitchingCostAudit.total_cost()` soma os pesos dos estágios shippados; `is_monotonic_ladder()` exige (a) custo total não-decrescente ao longo dos meses dados e (b) em nenhum mês um estágio k shippado sem que 1..k-1 também estejam
- [ ] `WowCollapseSimulator.simulate()` retorna os meses em risco: a partir do mês em que o estágio ativo sai de `wow` (`detection`), todos os meses até o próximo ship (exclusive) se o gap exceder a cadência — ou até o horizonte se não houver próximo ship

### Técnicos

- [ ] Python 3.9+ com type hints
- [ ] `dataclasses` para todos os modelos (`AdoptionSignal`, `RoadmapItem`, `DeploymentPlan`, `AuditFinding`, `PlanAudit`) e `Enum` para `ValueStage` e `AuditCode`
- [ ] `stage_status()`, `total_cost()` e `audit()` são determinísticos, sem estado e sem I/O
- [ ] Constantes nomeadas: `CADENCE_MAX_MONTHS = 2`, `HABITUATION_THRESHOLD = 2`, `SWITCHING_COST_WEIGHTS`
- [ ] Dados de teste 100% determinísticos (sinais e planos declarados literalmente)

### Validação

- [ ] Cenário 1: custos por estágio — {1} = 1.0, {1,2} = 3.5, {1,2,3} = 5.5, {1,2,3,4} = 8.5, e o salto {1,4} = 4.0
- [ ] Cenário 2: plano original auditado no mês 4 → `SKIPPED_STAGE` + `UNEARNED_STAGE` + `STALL_RISK`, todos high, todos no item P2; `has_blocking_findings == True`
- [ ] Cenário 3: listener — estágio 1 é `wow` até o mês 2, `habituated` no mês 3, `frustrated` no mês 4 (comparação)
- [ ] Cenário 4: plano reparado auditado nos meses 4 e 10 → zero findings de bloqueio; plano original com sinais vazios → `MISSING_SIGNALS`
- [ ] Cenário 5: simulador — original tem meses de risco `[3, 4, 5]`; reparado tem `[]`; plano sem próximo ship tem risco do detection até o horizonte
- [ ] Cenário 6: escada monotônica — reparado é monotônico em `[0, 5, 7, 9]` com custo final 8.5; original **não** é monotônico em `[0, 6]` (estágio 4 shippado sem 2 e 3)

---

## 🏗️ Arquitetura do Sistema

### Diagrama ASCII

```
┌──────────────────────────────────────────────────────────────────┐
│              AGENT VALUE MATURITY LADDER — AUDIT                  │
│                                                                   │
│  PARTE 1 — MODELAGEM (escada + listener)                          │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │   4. HYPER_PERSONALIZATION      custo de troca 3.0      │     │
│  │   3. TEAM_EMPOWERMENT                          2.0      │     │
│  │   2. AUTOMATE_WORKFLOWS                         2.5      │     │
│  │   1. TALK_TO_DATA                               1.0      │     │
│  │                                                           │     │
│  │   AdoptionSignal(month, kind, stage)                      │     │
│  │     wow ▸ habituation ▸ comparison ▸ frustration          │     │
│  │     demand_next (apetite pelo próximo degrau — não é     │     │
│  │     sinal de churn)                                       │     │
│  │                                                           │     │
│  │   HabituationListener.stage_status(signals, stage, m)     │     │
│  │     frustrated  ◄─ qualquer comparison/frustration        │     │
│  │     habituated ◄─ 2+ habituation                          │     │
│  │     wow        ◄─ caso contrário                          │     │
│  └───────────────────────────┬────────────────────────────────┘   │
│                              ▼                                    │
│  PARTE 2 — AUDITORIA DO PLANO (os checks que pegam o plano GS)    │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │  DeploymentPlan: P1(estágio 1, mês 0)                    │     │
│  │                  P2(estágio 4, mês 6)  ◄── o salto       │     │
│  │                                                           │     │
│  │  MISSING_SIGNALS  sinais=[] → auditoria cega (medium)     │     │
│  │  SKIPPED_STAGE    degraus 2,3 sem NENHUM item (high)     │     │
│  │  UNEARNED_STAGE   P2 shipa mês 6 com 2,3 não-shippados   │     │
│  │                   (high)                                  │     │
│  │  STALL_RISK       estágio ativo habitua mês 3 ▸ próximo  │     │
│  │                   ship mês 6 ▸ gap 3 > cadência 2 (high) │     │
│  │                                                           │     │
│  │  → PlanAudit.has_blocking_findings == True                │     │
│  └───────────────────────────┬────────────────────────────────┘   │
│                              ▼                                    │
│  PARTE 3 — REPARO + CUSTO DE TROCA + SIMULAÇÃO                    │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │  Reparado: R1(est.1, mês 0) R2(est.2, mês 5)             │     │
│  │             R3(est.3, mês 7) R4(est.4, mês 9)            │     │
│  │  → re-auditoria nos meses 4 e 10: zero bloqueios         │     │
│  │                                                           │     │
│  │  Custo de troca (soma dos degraus shippados):            │     │
│  │    original mês 6: {1,4} = 4.0  (o salto)                │     │
│  │    reparado mês 9: {1,2,3,4} = 8.5  (a escada)           │     │
│  │                                                           │     │
│  │  WowCollapseSimulator:                                    │     │
│  │    original:  detection mês 3, ship mês 6, gap 3         │     │
│  │              → meses de risco [3, 4, 5]                  │     │
│  │    reparado:  detection mês 3, ship mês 5, gap 2         │     │
│  │              → meses de risco []                         │     │
│  └──────────────────────────────────────────────────────────┘     │
└──────────────────────────────────────────────────────────────────┘
```

---

## 🎯 Sua Tarefa em 3 Partes

### Parte 1 — Modelar a escada (`ValueStage`, `HabituationListener`)
O modelo precisa carregar as duas semânticas ao mesmo tempo: a ordem dos degraus (com os pesos de custo de troca que a etapa 3 audita) e o estado de habituação por estágio (o relógio do wow). Atenção ao detalhe semântico dos kinds de sinal: `comparison` e `frustration` são churn falando; `demand_next` é o usuário pedindo o próximo degrau — apetite, não risco.

### Parte 2 — Auditar o plano (`DeploymentPlan`, `DeploymentPlanAudit`)
Os três checks de bloqueio têm condições distintas: `SKIPPED_STAGE` olha o plano **inteiro** (o degrau existe em algum item, shipped ou não?); `UNEARNED_STAGE` olha o **estado no ship_month do item** (o predecessor já estava shippado quando este sai?); `STALL_RISK` cruza o listener com a cadência (o wow quebrou quando, e o próximo socorro chega em quanto tempo?). A auditoria roda num mês de referência (`audit_month`) — o "agora" da revisão trimestral.

### Parte 3 — Reparar e provar (`SwitchingCostAudit`, `WowCollapseSimulator`)
O plano reparado (R1-R4, já fornecido nos dados) precisa passar limpo na re-auditoria; a auditoria de custo de troca prova que a escada constrói mais lock-in que o salto (8.5 vs 4.0) de forma monotônica; e o simulador quantifica os meses expostos a churn de cada plano — o número que fecha a reunião.

---

## 💻 Starter Code

```python
"""
Exercício 10 — Agent Value Maturity Ladder
Nível 3 — Arquitetura Avançada

Pipeline: modelagem da escada de valor (4 estágios + listener de
habituação) → auditoria de roadmap contra a escada → reparo com
auditoria de custo de troca e simulação do colapso do wow.

Fonte do padrão: docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-
deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-
deploying-to-6000-users-analysis.md:62-67 (seção 1.9, Four-stage GTM
value maturity model).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


# ============================================================================
# CONSTANTES DE ESCADA E CADÊNCIA
# ============================================================================

CADENCE_MAX_MONTHS = 2      # 1-2 meses por próximo estágio (patterns.md:432)
HABITUATION_THRESHOLD = 2   # 2+ sinais de habituação => o wow quebrou

# Peso de custo de troca criado por cada degrau subido (analysis.md:167:
# o modelo de maturidade também é uma escada de switching cost).
SWITCHING_COST_WEIGHTS = {
    1: 1.0,   # TALK_TO_DATA: hábito de dados na plataforma
    2: 2.5,   # AUTOMATE_WORKFLOWS: o trabalho diário tece o produto
    3: 2.0,   # TEAM_EMPOWERMENT: artefatos do time vivem na plataforma
    4: 3.0,   # HYPER_PERSONALIZATION: contexto pessoal insubstituível
}


class ValueStage(Enum):
    TALK_TO_DATA = 1
    AUTOMATE_WORKFLOWS = 2
    TEAM_EMPOWERMENT = 3
    HYPER_PERSONALIZATION = 4


class AuditCode(Enum):
    SKIPPED_STAGE = "skipped_stage"          # degrau sem NENHUM item no plano
    UNEARNED_STAGE = "unearned_stage"        # shipa antes do predecessor
    STALL_RISK = "stall_risk"                # habituação + cadência quebrada
    MISSING_SIGNALS = "missing_signals"      # auditoria sem instrumentação


# ============================================================================
# PARTE 1 — MODELAGEM: SINAIS E LISTENER DE HABITUAÇÃO
# ============================================================================

@dataclass
class AdoptionSignal:
    """
    Um sinal de adoção observado na produção (NPS, entrevistas, logs).

    kind:
      wow          — entusiasmo de lançamento
      habituation  — "virou o básico, ninguém comenta"
      comparison   — "o produto X faz melhor" (churn falando)
      frustration  — reclamação direta
      demand_next  — pedindo o PRÓXIMO degrau (apetite, não churn)
    """
    month: int
    kind: str
    stage: ValueStage
    note: str = ""


class HabituationListener:
    """Classifica o estado de wow de um estágio a partir dos sinais."""

    @staticmethod
    def stage_status(
        signals: list[AdoptionSignal],
        stage: ValueStage,
        up_to_month: int | None = None,
    ) -> str:
        """
        TODO (Parte 1): retornar "wow" | "habituated" | "frustrated".

        Regras (sinais do estágio, com month <= up_to_month se dado):
          1. qualquer "comparison" ou "frustration" → "frustrated"
          2. >= HABITUATION_THRESHOLD sinais "habituation" → "habituated"
          3. senão → "wow"

        "wow" e "demand_next" NÃO mudam o estado — demanda do próximo
        degrau é apetite, não churn.
        """
        # TODO: Implementar
        pass


# ============================================================================
# PARTE 2 — PLANO DE DEPLOY E AUDITORIA
# ============================================================================

@dataclass
class RoadmapItem:
    """Um item de roadmap: capacidade de um estágio, mês de ship."""
    item_id: str
    title: str
    stage: ValueStage
    ship_month: int


@dataclass
class DeploymentPlan:
    """O roadmap completo do agente."""
    plan_id: str
    items: list[RoadmapItem] = field(default_factory=list)

    def shipped_stages(self, at_month: int) -> set[ValueStage]:
        """
        TODO (Parte 2): estágios com pelo menos um item de
        ship_month <= at_month.
        """
        # TODO: Implementar
        pass

    def next_ship_month(self, after_month: int) -> int | None:
        """
        TODO (Parte 2): o menor ship_month entre os itens que é
        > after_month; None se não há próximo ship.
        """
        # TODO: Implementar
        pass


@dataclass
class AuditFinding:
    """Um achado da auditoria contra a escada."""
    code: AuditCode
    severity: str          # "high" (bloqueia) | "medium"
    item_id: str | None    # item responsável (None p/ plan-level)
    rationale: str         # o número, não o adjetivo


@dataclass
class PlanAudit:
    """Resultado da auditoria de um plano."""
    plan_id: str
    findings: list[AuditFinding] = field(default_factory=list)

    @property
    def has_blocking_findings(self) -> bool:
        """TODO (Parte 2): qualquer finding com severity "high"."""
        # TODO: Implementar
        pass


class DeploymentPlanAudit:
    """Audita um plano de deploy contra a escada de valor."""

    @staticmethod
    def audit(
        plan: DeploymentPlan,
        signals: list[AdoptionSignal],
        audit_month: int,
    ) -> PlanAudit:
        """
        TODO (Parte 2): emitir findings NA ORDEM:

        1. MISSING_SIGNALS (medium, item None) se `signals` é vazio —
           sem instrumentação a auditoria está cega.

        2. SKIPPED_STAGE (high) — para cada item de estágio k: se existe
           degrau j < k SEM NENHUM item no plano (shipped ou planejado),
           o degrau foi pulado da escada.

        3. UNEARNED_STAGE (high) — para cada item de estágio k: se algum
           degrau j < k NÃO está em shipped_stages(item.ship_month), o
           item shipa confiança que não foi ganha.

        4. STALL_RISK (high, item None) — se há sinais E estágio ativo
           (max de shipped_stages(audit_month)):
             detection = menor mês m <= audit_month em que
               stage_status(signals, ativo, up_to_month=m) != "wow"
             next_ship = next_ship_month(after_month=detection)
             se detection existe E (next_ship é None OU
                next_ship - detection > CADENCE_MAX_MONTHS) → finding
               com o gap no rationale.

        Simplificação declarada: o STALL_RISK usa o estágio ativo no
        audit_month para toda a janela histórica.
        """
        # TODO: Implementar
        pass


# ============================================================================
# PARTE 3 — CUSTO DE TROCA E SIMULAÇÃO DO COLAPSO DO WOW
# ============================================================================

class SwitchingCostAudit:
    """A meia-escada estratégica: cada degrau eleva o custo de troca."""

    @staticmethod
    def stage_costs(shipped: set[ValueStage]) -> dict[ValueStage, float]:
        """TODO (Parte 3): {estágio: peso} apenas dos estágios shippados."""
        # TODO: Implementar
        pass

    @staticmethod
    def total_cost(shipped: set[ValueStage]) -> float:
        """
        TODO (Parte 3): soma dos SWITCHING_COST_WEIGHTS dos estágios
        shippados.
        """
        # TODO: Implementar
        pass

    @staticmethod
    def is_monotonic_ladder(plan: DeploymentPlan, at_months: list[int]) -> bool:
        """
        TODO (Parte 3): True quando, para a lista de meses (na ordem dada):
          a) total_cost(shipped_stages(m)) é não-decrescente; E
          b) em nenhum mês um estágio k está shippado sem que TODOS os
             degraus 1..k-1 também estejam.
        """
        # TODO: Implementar
        pass


class WowCollapseSimulator:
    """
    Quantifica os meses expostos a churn pelo colapso do wow.

    O relógio começa no mês em que o estágio ativo sai de "wow"
    (detection). Se o próximo ship chega dentro da cadência, nada
    acontece; se demora mais que CADENCE_MAX_MONTHS (ou nunca chega),
    todos os meses de detection até o ship (exclusive) ficam em risco.
    """

    @staticmethod
    def simulate(
        plan: DeploymentPlan,
        signals: list[AdoptionSignal],
        horizon: int,
    ) -> list[int]:
        """
        TODO (Parte 3):
          1. detection = menor mês m em que o estágio ativo NAQUELE mês
             tem stage_status(..., up_to_month=m) != "wow"
             (estágio ativo = max de shipped_stages(m); sem estágio
             ativo, o mês não conta)
          2. next_ship = plan.next_ship_month(after_month=detection)
          3. se detection não existe → []
             senão se next_ship é None → [detection .. horizon]
             senão se next_ship - detection > CADENCE_MAX_MONTHS
               → [detection .. next_ship - 1]
             senão → []
        """
        # TODO: Implementar
        pass


# ============================================================================
# DADOS DE TESTE (determinísticos — a revisão trimestral do prólogo)
# ============================================================================

def build_stage1_signals() -> list[AdoptionSignal]:
    """
    Sinais do estágio 1 (KODA-QA) coletados nos 5 primeiros meses.
    O wow quebra no mês 3 (2ª habituação); a comparação chega no mês 4;
    as demandas por rascunho/inbox são apetite pelo DEGRAU 2.
    """
    s1 = ValueStage.TALK_TO_DATA
    return [
        AdoptionSignal(1, "wow", s1, "vendedores escaparam da fila de analistas"),
        AdoptionSignal(2, "habituation", s1, "ninguém mais comenta nas reuniões"),
        AdoptionSignal(3, "habituation", s1, "virou ferramenta padrão do dia a dia"),
        AdoptionSignal(4, "comparison", s1, "o ChatGPT monta uma tabela melhor"),
        AdoptionSignal(4, "demand_next", s1, "quando ele mesmo escreve o rascunho de e-mail?"),
        AdoptionSignal(5, "demand_next", s1, "quero que ele monitore meu inbox"),
    ]


def build_original_plan() -> DeploymentPlan:
    """
    O plano do Head de GS: o salto 1 → 4. O estágio 1 shippado no mês 0;
    o CRM hiper-personalizado planejado para o mês 6. Degraus 2 e 3?
    Não existem — é isso que a auditoria precisa pegar.
    """
    return DeploymentPlan("KODA-ASSIST-ORIGINAL", [
        RoadmapItem("P1", "KODA-QA: converse com seus dados",
                    ValueStage.TALK_TO_DATA, 0),
        RoadmapItem("P2", "CRM hiper-personalizado com IA",
                    ValueStage.HYPER_PERSONALIZATION, 6),
    ])


def build_repaired_plan() -> DeploymentPlan:
    """
    O plano reparado na reunião: um degrau por vez, cadência de 2 meses.
    R2 mantém o envio irreversível humano (monitora → rascunha →
    vendedor revisa e envia) — analysis.md:65.
    """
    return DeploymentPlan("KODA-ASSIST-REPARADO", [
        RoadmapItem("R1", "KODA-QA: converse com seus dados",
                    ValueStage.TALK_TO_DATA, 0),
        RoadmapItem("R2", "Monitorar inbox/Slack + rascunho no Gmail com revisão humana",
                    ValueStage.AUTOMATE_WORKFLOWS, 5),
        RoadmapItem("R3", "Squads constroem próprios skills e dashboards",
                    ValueStage.TEAM_EMPOWERMENT, 7),
        RoadmapItem("R4", "Hiper-personalização com contexto vivo por vendedor",
                    ValueStage.HYPER_PERSONALIZATION, 9),
    ])


# ============================================================================
# TESTES
# ============================================================================

def test_1_escada_e_custos_de_troca():
    """Cenário 1: os quatro degraus e o custo de troca de cada conjunto."""
    print("\n" + "=" * 60)
    print("TESTE 1: Escada e Custos de Troca")
    print("=" * 60)

    S1, S2, S3, S4 = (ValueStage.TALK_TO_DATA, ValueStage.AUTOMATE_WORKFLOWS,
                      ValueStage.TEAM_EMPOWERMENT, ValueStage.HYPER_PERSONALIZATION)

    assert [s.value for s in (S1, S2, S3, S4)] == [1, 2, 3, 4], "ordem 1→4"
    for stage in (S1, S2, S3, S4):
        assert stage.value in SWITCHING_COST_WEIGHTS, "todo degrau tem peso"

    costs = {
        frozenset([S1]): 1.0,
        frozenset([S1, S2]): 3.5,
        frozenset([S1, S2, S3]): 5.5,
        frozenset([S1, S2, S3, S4]): 8.5,
        frozenset([S1, S4]): 4.0,   # o salto do plano do GS
    }
    for stages, expected in costs.items():
        got = SwitchingCostAudit.total_cost(set(stages))
        print(f"\n  {sorted(s.value for s in stages)}  custo={got:.1f}  esperado={expected:.1f}")
        assert abs(got - expected) < 1e-9

    assert SwitchingCostAudit.total_cost(set([S1, S2, S3, S4])) > \
           SwitchingCostAudit.total_cost(set([S1, S4])), (
        "a escada completa constrói mais lock-in que o salto"
    )
    print("  TESTE 1 PASSOU")


def test_2_auditoria_do_plano_original():
    """Cenário 2: os três bloqueios no plano do Head de GS (audit_month=4)."""
    print("\n" + "=" * 60)
    print("TESTE 2: Auditoria — Plano Original (o salto 1→4)")
    print("=" * 60)

    audit = DeploymentPlanAudit.audit(
        build_original_plan(), build_stage1_signals(), audit_month=4
    )
    codes = {f.code for f in audit.findings}

    print(f"\n  Findings:")
    for f in audit.findings:
        print(f"   {f.severity:6s} {f.code.value:16s} item={f.item_id}")
        print(f"          {f.rationale}")

    assert AuditCode.SKIPPED_STAGE in codes, "degraus 2 e 3 não existem no plano"
    assert AuditCode.UNEARNED_STAGE in codes, "P2 shipa sem ganhar os degraus anteriores"
    assert AuditCode.STALL_RISK in codes, "habituação mês 3 + ship mês 6 = gap 3"

    for f in audit.findings:
        if f.code in (AuditCode.SKIPPED_STAGE, AuditCode.UNEARNED_STAGE):
            assert f.item_id == "P2", "o item do salto é o responsável"
            assert f.severity == "high"
    assert audit.has_blocking_findings, "o plano original bloqueia"
    print("  TESTE 2 PASSOU")


def test_3_listener_de_habituacao():
    """Cenário 3: wow → habituated → frustrated ao longo dos meses."""
    print("\n" + "=" * 60)
    print("TESTE 3: Listener de Habituação")
    print("=" * 60)

    signals = build_stage1_signals()
    s1 = ValueStage.TALK_TO_DATA

    status = {m: HabituationListener.stage_status(signals, s1, up_to_month=m)
              for m in (1, 2, 3, 4)}
    print(f"\n  {status}")

    assert status[1] == "wow", "mês 1: só entusiasmo"
    assert status[2] == "wow", "mês 2: 1 habituação ainda é wow"
    assert status[3] == "habituated", "mês 3: 2 habituações => o wow quebrou"
    assert status[4] == "frustrated", "mês 4: comparação com outro produto"

    # demand_next não é churn: sem as habituações, demandas não quebram o wow
    so_demandas = [s for s in signals if s.kind == "demand_next"]
    assert HabituationListener.stage_status(so_demandas, s1) == "wow"

    # estágio sem sinais: wow (a auditoria de MISSING_SIGNALS cobre a cegueira)
    assert HabituationListener.stage_status(signals, ValueStage.TEAM_EMPOWERMENT) == "wow"
    print("  TESTE 3 PASSOU")


def test_4_reparo_passa_limpo():
    """Cenário 4: plano reparado sem bloqueios; sinais vazios → MISSING_SIGNALS."""
    print("\n" + "=" * 60)
    print("TESTE 4: Re-Auditoria — Plano Reparado")
    print("=" * 60)

    signals = build_stage1_signals()
    for month in (4, 10):
        audit = DeploymentPlanAudit.audit(build_repaired_plan(), signals, month)
        print(f"\n  mês {month}: {[f.code.value for f in audit.findings]}")
        blocking = [f for f in audit.findings if f.severity == "high"]
        assert blocking == [], f"reparado não bloqueia no mês {month}"
        assert not audit.has_blocking_findings

    # Auditoria cega: sem sinais, o finding é de instrumentação
    cega = DeploymentPlanAudit.audit(build_original_plan(), [], audit_month=4)
    codes = {f.code for f in cega.findings}
    assert AuditCode.MISSING_SIGNALS in codes, "sem sinais a auditoria está cega"
    missing = next(f for f in cega.findings if f.code == AuditCode.MISSING_SIGNALS)
    assert missing.severity == "medium"
    print("\n  sinais=[] → MISSING_SIGNALS (medium) ✓")
    print("  TESTE 4 PASSOU")


def test_5_simulador_do_colapso():
    """Cenário 5: meses expostos a churn — original [3,4,5], reparado []."""
    print("\n" + "=" * 60)
    print("TESTE 5: Simulador do Colapso do Wow")
    print("=" * 60)

    signals = build_stage1_signals()

    risco_original = WowCollapseSimulator.simulate(build_original_plan(), signals, 8)
    risco_reparado = WowCollapseSimulator.simulate(build_repaired_plan(), signals, 8)

    print(f"\n  Original:  meses de risco {risco_original}")
    print(f"  Reparado:  meses de risco {risco_reparado}")

    assert risco_original == [3, 4, 5], (
        "detection mês 3, ship mês 6, gap 3 > 2 → risco até o ship"
    )
    assert risco_reparado == [], "ship no mês 5 chega dentro da cadência"

    # Sem próximo ship: o risco corre até o horizonte
    so_estagio1 = DeploymentPlan("SO-ESTAGIO-1", [
        RoadmapItem("P1", "KODA-QA", ValueStage.TALK_TO_DATA, 0),
    ])
    risco_sem_ship = WowCollapseSimulator.simulate(so_estagio1, signals, 8)
    print(f"  Sem próximo ship: {risco_sem_ship}")
    assert risco_sem_ship == [3, 4, 5, 6, 7, 8], (
        "parado no estágio 1, todo mês após o detection é churn exposto"
    )
    print("  TESTE 5 PASSOU")


def test_6_escada_monotonica():
    """Cenário 6: reparo é monotônico (8.5 no fim); o salto não é."""
    print("\n" + "=" * 60)
    print("TESTE 6: Escada Monotônica de Custo de Troca")
    print("=" * 60)

    reparado = build_repaired_plan()
    original = build_original_plan()

    assert SwitchingCostAudit.is_monotonic_ladder(reparado, [0, 5, 7, 9])
    assert not SwitchingCostAudit.is_monotonic_ladder(original, [0, 6]), (
        "estágio 4 shippado no mês 6 sem os degraus 2 e 3"
    )

    final = SwitchingCostAudit.total_cost(reparado.shipped_stages(9))
    salto = SwitchingCostAudit.total_cost(original.shipped_stages(6))
    print(f"\n  Escada completa (mês 9): {final:.1f}")
    print(f"  Salto 1→4 (mês 6):       {salto:.1f}")

    assert final == 8.5 and salto == 4.0
    custos_por_estagio = SwitchingCostAudit.stage_costs(reparado.shipped_stages(9))
    assert len(custos_por_estagio) == 4, "os quatro degraus contribuem"
    print("  TESTE 6 PASSOU")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("EXERCÍCIO 10: AGENT VALUE MATURITY LADDER")
    print("=" * 60)

    # Quando implementado, descomente para testar:
    # test_1_escada_e_custos_de_troca()
    # test_2_auditoria_do_plano_original()
    # test_3_listener_de_habituacao()
    # test_4_reparo_passa_limpo()
    # test_5_simulador_do_colapso()
    # test_6_escada_monotonica()

    print("\nTODO: Implemente as partes acima!")
    print("   1. HabituationListener.stage_status()")
    print("   2. DeploymentPlan.shipped_stages() / next_ship_month()")
    print("   3. PlanAudit.has_blocking_findings + DeploymentPlanAudit.audit()")
    print("   4. SwitchingCostAudit.stage_costs / total_cost / is_monotonic_ladder")
    print("   5. WowCollapseSimulator.simulate()")
    print("   Após implementar, descomente os testes em main()")
```

---

## ✅ Validação: Critérios de Aceitação

Seu código será considerado **APROVADO** quando:

### Critério 1: Modelagem da escada (Parte 1)

- [ ] Os 4 estágios na ordem 1→4 com pesos cobrindo todos os degraus
- [ ] `stage_status` distingue `wow` / `habituated` / `frustrated` com o limiar de 2 habituações
- [ ] `demand_next` e `wow` não mudam o estado (apetite ≠ churn)
- [ ] `up_to_month` filtra sinais futuros (o status no mês 3 não vê o sinal do mês 4)

### Critério 2: Auditoria do plano (Parte 2)

- [ ] `MISSING_SIGNALS` (medium) quando a lista de sinais é vazia
- [ ] `SKIPPED_STAGE` (high) no P2 — degraus 2 e 3 sem item algum no plano
- [ ] `UNEARNED_STAGE` (high) no P2 — shipa no mês 6 com predecessores não-shippados
- [ ] `STALL_RISK` (high) com o gap no rationale — detection mês 3, próximo ship mês 6, gap 3 > 2
- [ ] `has_blocking_findings == True` para o plano original; `False` para o reparado nos meses 4 e 10

### Critério 3: Reparo, custo de troca e simulação (Parte 3)

- [ ] `total_cost`: {1} = 1.0, {1,2} = 3.5, {1,2,3} = 5.5, {1,2,3,4} = 8.5, {1,4} = 4.0
- [ ] `is_monotonic_ladder`: reparado `True` em `[0, 5, 7, 9]`; original `False` em `[0, 6]`
- [ ] Simulador: original `[3, 4, 5]`; reparado `[]`; sem próximo ship, risco até o horizonte
- [ ] A escada completa (8.5) supera o salto (4.0) — o número que fecha a reunião

---

## 📊 Rubric de Avaliação

| Critério | Peso | Insuficiente (0-3) | Básico (4-6) | Proficiente (7-8) | Excelente (9-10) |
|---|---|---|---|---|---|
| **Modelagem (Parte 1)** | 20% | Não implementado | Listener conta sinais mas ignora `up_to_month` | Transições wow→habituated→frustrated corretas com `demand_next` neutro | Semântica dos kinds explicitada: comparação é churn falando, demanda é apetite |
| **Auditoria (Parte 2)** | 35% | Não implementado | Um check só (tipicamente SKIPPED) | Os três bloqueios + MISSING_SIGNALS com severidades certas | SKIPPED vs UNEARNED distinguidos por design (plano-inteiro vs estado-no-ship) e o gap da cadência no rationale |
| **Reparo + Simulação (Parte 3)** | 30% | Não implementado | Custo calcula mas monotonicidade falha | total_cost + is_monotonic_ladder + simulador com os três cenários | Meses de risco como argumento quantitativo do reparo (3,4,5 → []) |
| **Interpretação estratégica** | 15% | Trata a escada como roadmap cosmético | Ordena estágios sem justificar | Conecta cadência ao colapso do wow | Articula a dupla tese: paranoia institucionalizada + custo de troca como resposta ao churn |

**Nota final:** Média ponderada. **Aprovação:** >= 7.0

---

## 💡 Dicas para Implementação

### Para a modelagem

1. **`up_to_month` é a memória do listener.** O status do mês 3 deve computar só com sinais até o mês 3 — sem esse filtro, a comparação do mês 4 "vaza" para trás e o detection erra. É o mesmo discipline de janela do Exercício 9 (`ActivationWindow.contains`), agora no eixo temporal de meses.
2. **A ordem das regras importa.** Uma comparação no mês 4 com zero habituações é `frustrated` (regra 1 antes da regra 2) — um usuário que compara já churnou de espírito, mesmo sem habituar.

### Para a auditoria

1. **SKIPPED e UNEARNED são checks diferentes por design.** SKIPPED olha o papel: "o degrau 3 existe em algum lugar do plano?". UNEARNED olha o tempo: "quando o P2 shipar no mês 6, o degrau 3 já estará de pé?". Um plano pode ter todos os degraus (sem SKIPPED) e ainda shipar fora de ordem (UNEARNED).
2. **O STALL_RISK cruza duas fontes.** O listener diz *quando* o wow quebrou; o plano diz *quando* o socorro chega. O finding só existe na intersecção: gap maior que a cadência. Se sua auditoria emite STALL sem número de gap no rationale, ela voltou a ser adjetivo — a diretoria pediu números.
3. **Estágio ativo no audit_month.** A simplificação declarada no docstring (usar o estágio ativo no mês da auditoria para toda a janela) é suficiente para o cenário e mantém o código honesto — uma versão completa recalcula o estágio ativo mês a mês, como o `WowCollapseSimulator` faz.

### Para o reparo e a simulação

1. **O simulador marca `[detection, next_ship)`.** O mês do ship não é de risco: a capacidade nova chega nele. Off-by-one aqui muda `[3, 4, 5]` para `[3, 4, 5, 6]` e o teste plaqueia.
2. **Lock-in é soma, não máximo.** `total_cost` soma os pesos dos degraus shippados — o custo de troca do estado {1,2,3,4} acumula o hábito de dados E os workflows E os artefatos do time E o contexto pessoal. É por isso que a escada (8.5) supera o salto (4.0): o salto nunca coletou os degraus intermediários.
3. **Monotonicidade tem duas faces.** Custos não-decrescentes (nada "deshipa") E nenhum degrau no ar (k shippado implica 1..k-1 shippados). O original falha na segunda face — e é a face que queima confiança.

---

## ❓ Dúvidas Comuns

**P: Por que o peso do estágio 3 (2.0) é menor que o do estágio 2 (2.5)? A escada não deveria ser crescente?**
R: Os pesos modelam custo de troca, não dificuldade. Workflows automatizados (estágio 2) têm o trabalho diário do usuário no produto — arrancar isso dói mais que migrar artefatos de time (estágio 3), que são recriáveis em outra plataforma com esforço. A monotonicidade exigida é do custo *acumulado* do estado, não do peso individual por degrau.

**P: Isso não é a escada de autonomia (Observe → Assist → Own) aplicada a produto?**
R: Não — a classificação é explícita sobre isso: "nearest ladder, wrong object" (`...classification.yaml:358-359`). Observe→Assist→Own mede a autonomia de *execução do agente* dentro de uma tarefa, com gates de prontidão (`docs/canonical/autonomy-curriculum-sampling.md:60`). Aqui os degraus medem *valor percebido pelo usuário do produto*. As duas escadas coexistem: um agente pode operar em Own num workflow do estágio 2.

**P: O que exatamente quebra quando se pula estágio?**
R: A confiança que sustenta o próximo degrau. "Skipping stages burns the trust the ladder depends on" (`...patterns.md:428`): o estágio 4 (hiper-personalização com contexto vivo) presupõe que o usuário já confia o suficiente para entregar contexto íntimo de clientes — confiança construída pelos estágios 2 e 3, onde o produto provou revisão humana e empoderamento. Saltar entrega contexto a um produto sem histórico — e o usuário que já compara com o ChatGPT não dá essa segunda chance de graça.

**P: Meu simulador trata estágio sem sinais como `wow`. Isso não esconde risco?**
R: Para o estágio ativo sem sinal algum, sim — e é por isso que a auditoria tem `MISSING_SIGNALS` como achado separado (medium): a resposta certa para cegueira de instrumentação é consertar a instrumentação, não inferir otimismo. Na dúvida, auditoria honesta distingue "sem risco" de "sem dados".

**P: Por que cadência de 2 meses e não "o mais rápido possível"?**
R: A cadência vem do caso: um a dois meses por próximo estágio (`...patterns.md:432`), calibrado pela velocidade do colapso do wow — parado, a disrupção chega em 1-2 meses porque o custo de troca é quase zero (`...analysis.md:60`). Mais rápido que a cadência queima a equipe; mais lento presenteia o churn. O `CADENCE_MAX_MONTHS` é o contrato entre os dois relógios.

---

## 🚀 Próximo Passo

Depois de completar este exercício:

1. Leia as seções 1.8-1.9 ("Collapsing wow factor" e "Four-stage GTM value maturity model") e o synthesis final em `docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-analysis.md:57-67` e `:167` — e a entrada completa da classificação `Missing` em `...classification.yaml:348-369`
2. Compare com `docs/canonical/measured-harness-evolution-lifecycle.md:29` — lifecycle de componente (infraestrutura) vs escada de valor (produto): as duas progressões governam ondas diferentes do mesmo sistema
3. Volte ao [[curriculum/03-nivel-3-advanced-architecture/exercises/exercise-09-trial-retention-attribution-split|Exercício 9]] e conecte: o listener de habituação deste exercício é o consumidor natural da telemetria de ativação daquele — o split diagnostica quem não subiu no degrau 1; o listener detecta quando quem subiu já não sente o degrau

---

*Exercício 10 | Nível 3 — Arquitetura Avançada | Agent Value Maturity Ladder*

**Toda vez que as pessoas estão felizes, você deveria estar paranoico — e ter o próximo degrau datado.**
