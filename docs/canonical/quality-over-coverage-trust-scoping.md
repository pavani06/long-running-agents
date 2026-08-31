---
title: "Quality-Over-Coverage Trust Scoping"
type: canonical
tags: ["evals", "governanca", "decision-discipline", "production"]
Status: Active
Source: "AI Engineer talk — Sait Izmit, Snowflake (GTM assistant: 6.000 usuários, 1M+ perguntas)"
Classification: "Partial Coverage (P2, Medium integration value)"
Precedence: "Level 2 (docs/system-of-record.md)"
last_updated: 2026-08-30
aliases: ["trust scoping", "accuracy-zone launch scope", "quality over coverage", "trust as unit of account"]
relates-to:
  - "[[docs/canonical/evals-as-brakes|Evals-as-Brakes]]"
  - "[[docs/canonical/domain-embedded-workflow-automation-wedge|Domain-Embedded Workflow Automation Wedge]]"
  - "[[docs/canonical/carve-out-pilot-hard-target|Carve-Out Pilot with Hard P&L Target]]"
  - "[[docs/canonical/workflow-derived-golden-question-set|Workflow-Derived Golden Question Set]]"
  - "[[docs/canonical/retention-gated-phased-rollout|Retention-Gated Phased Rollout]]"
  - "[[docs/canonical/agent-value-maturity-ladder|Agent Value Maturity Ladder]]"
  - "[[docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-analysis|GTM AI Agents Analysis]]"
sources:
  - "[[docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-patterns|GTM AI Agents Patterns]]"
  - "[[docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-classification|GTM AI Agents Classification]]"
---

# Quality-Over-Coverage Trust Scoping

**Type:** Canonical Pattern
**Status:** Active
**Source:** AI Engineer talk — Sait Izmit, Snowflake (GTM assistant: 6.000 usuários, 1M+ perguntas, ~40k perguntas/semana)
**Classification:** Partial Coverage (P2, Medium integration value)
**Precedence:** Level 2 ([[docs/system-of-record|System of Record]])

---

## Problema

Uma superfície de agente free-form exposta antes de sua zona de acurácia estar engenheirada destrói confiança no primeiro contato: as **primeiras ~5 perguntas** decidem se o usuário volta, e a recuperação custa 10x ou nunca acontece (`docs/analysis/...-patterns.md:55-58`).

A economia da assimetria de confiança é o coração do problema: confiança é difícil de ganhar, perde-se numa noite e custa 10x para recuperar. Um launch amplo a 70% de acurácia maximiza a superfície de primeiros contatos ruins; cada usuário que queima as primeiras 5 perguntas numa zona de baixa acurácia é um usuário que escreve o produto como "não funciona" — independentemente da qualidade nas zonas boas.

O repo nomeia as duas metades separadas — shipping gated por qualidade ([[docs/canonical/evals-as-brakes|Evals-as-Brakes]]) e slicing narrow-first ([[docs/canonical/domain-embedded-workflow-automation-wedge|Domain-Embedded Workflow Automation Wedge]]) — mas nenhuma doc frameia **confiança como unidade de conta para o escopo de exposição** (classification:65-69).

## Solução

Cortar o escopo de launch pela **zona de alta acurácia** sobre o espaço de perguntas candidatas: 50 perguntas a 95% de acurácia em vez de 100 a 70 (`docs/analysis/...-patterns.md:62-64`).

Componentes (`docs/analysis/...-patterns.md:74-78`):

| Componente | Função |
|---|---|
| Definição da zona de alta acurácia | Mapear perguntas candidatas para zonas de acurácia (exige golden set com score por zona) |
| Corte do escopo de launch | Publicar apenas a zona de alta acurácia na superfície user-facing |
| Roadmap de cobertura pós-launch | 60% dos dados foram adicionados 6-7 meses **depois** do launch no caso-fonte |
| Monitor de sinal de demanda | Usuários pedindo mais ("Can I get more of that?") como gatilho de expansão |

Fluxo (`docs/analysis/...-patterns.md:79-84`): mapear perguntas candidatas para zonas de acurácia → cortar o escopo de launch para a zona alta → lançar estreito com alta acurácia → monitorar sinais de demanda → expandir cobertura incrementalmente **somente depois** de a confiança estar estabelecida.

A dinâmica contra-intuitiva que o caso-fonte comprova: começar pequeno **não bloqueou** a adoção — protegeu a confiança enquanto a expansão acontecia; usuários com as primeiras 5 perguntas atendidas na zona alta passam a pedir mais, puxando a expansão organicamente (`docs/analysis/...-patterns.md:66-69`). A cobertura total virou roadmap, não requisito de launch.

## Implementação neste repositório

### O que já existe

As duas metades do reframe (classification:46-64):

- **Shipping gated por qualidade:** [[docs/canonical/evals-as-brakes|Evals-as-Brakes]] — "Organizations respond to AI risk with the wrong dial: they slow down. ... Companies that go slow do so because they lack brakes (evals), not because slowness is safe" (`docs/canonical/evals-as-brakes.md:32`); "shipping velocity and safety are treated as independent dials" (`:34`).
- **Slicing narrow-first:** [[docs/canonical/domain-embedded-workflow-automation-wedge|Domain-Embedded Workflow Automation Wedge]] — "Choose a workflow slice that operators already perform repeatedly and painfully" (`docs/canonical/domain-embedded-workflow-automation-wedge.md:43`); [[docs/canonical/carve-out-pilot-hard-target|Carve-Out Pilot with Hard P&L Target]] — "Carve out one contained operating unit, install an agent in the standard harness as its operator (the 'AI CEO'), and make a hard P&L number the eval readout" (`docs/canonical/carve-out-pilot-hard-target.md:41`) — contenção de piloto, não de superfície user-facing.

### O que falta

(classification:65-69) — busca da classificação: `trust` (case-insensitive) em `docs/canonical/` retorna **zero** matches (2026-08-30); NOT_FOUND para mapeamento de zona de acurácia, corte de escopo de launch e roadmap de cobertura pós-launch:

1. **Escopo do launch pela zona de acurácia** — o reframe 50@95% vs. 100@70: nenhuma doc dimensiona a superfície user-facing de lançamento pela distribuição de acurácia sobre o espaço de perguntas.
2. **Economia da assimetria de confiança** — primeiras ~5 perguntas, recuperação a 10x, como argumento quantitativo de design de escopo.
3. **Roadmap de cobertura pós-launch** — cobertura explícita como roadmap sequenciado pós-confiança (60% dos dados adicionados após o launch).
4. **Monitor de sinal de demanda como gatilho de expansão** — "usuários pedindo mais" como trigger operacional nomeado.

## Tradeoffs

| Benefício | Custo |
|---|---|
| As primeiras cinco perguntas caem dentro da zona de alta acurácia | Escopo de launch deliberadamente estreito frustra stakeholders que exigem amplitude |
| Usuários pedem mais em vez de descartar o produto — expansão puxada organicamente | A cobertura diferida precisa de fato shipar no roadmap |
| Começar pequeno não bloqueou adoção; protegeu confiança durante a expansão | Exige o golden set com score por zona para saber onde está a zona alta (dependência do padrão-fonte) |
| Confiança como unidade de conta torna o tradeoff escopo×qualidade explicitamente decidível | Sinais de demanda são qualitativos; expansão sem monitor vira palpite |

## Relação com outros padrões

- **Depende de:** [[docs/canonical/workflow-derived-golden-question-set|Workflow-Derived Golden Question Set]] — sem score por zona de perguntas não há mapa de acurácia para cortar o escopo ("Demands pattern 1 to know where the high-accuracy zone is", `docs/analysis/...-patterns.md:73`).
- **Reframe de:** [[docs/canonical/evals-as-brakes|Evals-as-Brakes]] — freios governam velocidade de shipping; aqui o freio governa a **superfície de exposição** ao usuário.
- **Estende:** [[docs/canonical/domain-embedded-workflow-automation-wedge|Domain-Embedded Workflow Automation Wedge]] e [[docs/canonical/carve-out-pilot-hard-target|Carve-Out Pilot with Hard P&L Target]] — slicing estreito aplicado ao eixo user-facing de launch.
- **Alimenta:** [[docs/canonical/retention-gated-phased-rollout|Retention-Gated Phased Rollout]] — o escopo de qualidade é o que o gate de retenção mede; [[docs/canonical/agent-value-maturity-ladder|Agent Value Maturity Ladder]] — o estágio 1 da escada nasce com este escopo.

## Referências

- `docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-patterns.md:55-84` — padrão extraído: assimetria de confiança, 50@95% vs. 100@70, roadmap de cobertura, sinal de demanda.
- `docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-classification.yaml:42-69` — classificação Partial Coverage (Medium), NOT_FOUND de `trust` em docs/canonical/, justificativa das duas metades.
- `docs/canonical/evals-as-brakes.md:32, :34` — freios vs. lentidão; dials independentes.
- `docs/canonical/domain-embedded-workflow-automation-wedge.md:43` — slice repetido e doloroso.
- `docs/canonical/carve-out-pilot-hard-target.md:41` — contenção de piloto com readout P&L.
