---
title: "Trial-Retention Attribution Split"
type: canonical
tags: ["evals", "production", "decision-discipline"]
Status: Active
Source: "AI Engineer talk — Sait Izmit, Snowflake (GTM assistant: 6.000 usuários, 1M+ perguntas)"
Classification: "Missing (Medium integration value)"
Precedence: "Level 2 (docs/system-of-record.md)"
last_updated: 2026-08-30
aliases: ["trial retention split", "activation attribution", "tried vs returned", "trial-retention diagnostic"]
relates-to:
  - "[[docs/canonical/eval-to-production-correlation-tracking|Eval-to-Production Correlation Tracking]]"
  - "[[docs/canonical/qa-to-backlog-feedback-loop|QA-to-Backlog Feedback Loop]]"
  - "[[docs/canonical/retention-gated-phased-rollout|Retention-Gated Phased Rollout]]"
  - "[[docs/canonical/owner-led-activation-blitz|Owner-Led Activation Blitz]]"
  - "[[docs/canonical/agent-value-maturity-ladder|Agent Value Maturity Ladder]]"
  - "[[docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-analysis|GTM AI Agents Analysis]]"
sources:
  - "[[docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-patterns|GTM AI Agents Patterns]]"
  - "[[docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-classification|GTM AI Agents Classification]]"
---

# Trial-Retention Attribution Split

**Type:** Canonical Pattern
**Status:** Active
**Source:** AI Engineer talk — Sait Izmit, Snowflake (GTM assistant: 6.000 usuários, 1M+ perguntas, ~40k perguntas/semana)
**Classification:** Missing (Medium integration value)
**Precedence:** Level 2 ([[docs/system-of-record|System of Record]])

---

## Problema

Números de uso baixos logo após o lançamento são lidos como falha de produto quando o problema real é que a maior parte da organização simplesmente nunca experimentou o agente. No caso Snowflake, apenas 20% havia experimentado o assistente duas semanas depois do GA — o alarme de "ninguém usa" era, na verdade, um alarme de ativação, não de qualidade (`docs/analysis/...-patterns.md:120-123`).

Sem um instrumento que separe as duas populações, a resposta organizacional padrão é um rollback ou retrabalho genérico de produto: ataca-se a precisão, a cobertura ou o escopo quando o defeito está no change management (ninguém fez o onboarding), ou vice-versa. O custo de uma atribuição errada é dobrado: o time de produto corrige um produto que não é o gargalo, enquanto a falha real de ativação segue invisível.

A instância repo-side mais próxima desse engano é a advertência de [[docs/canonical/eval-to-production-correlation-tracking|Eval-to-Production Correlation Tracking]]: "Eval scores become false safety signals when they stop predicting user outcomes" (`docs/canonical/eval-to-production-correlation-tracking.md:22`). Aqui a inversão é simétrica: métricas agregadas de uso viram falsos sinais de *falha de produto* quando deixam de prever qual população está sendo medida.

## Solução

Instrumentar per-usuário a distinção entre **experimentou** (trial flag) e **voltou** (retorno/semanas ativas) e transformar a combinação das duas taxas em uma regra de diagnóstico com roteamento de ownership:

| Ramo do diagnóstico | Leitura | Dono da correção |
|---|---|---|
| Experimentou e não voltou | Problema de **produto** (qualidade, cobertura, valor percebido) | Time de produto |
| Nunca experimentou | Problema de **change management** (onboarding, comunicação, patrocínio) | Trabalho de ativação |

Mecanismo em prosa: um flag de trial por usuário é gravado no primeiro contato real (não no acesso à landing page); a retenção é medida como retorno em janela fixa (ex.: semanalmente ativo); o par (taxa de trial, taxa de retorno) é recalculado a cada intervenção. A regra de roteamento é o coração do padrão: cada ramo tem um dono diferente, e a intervenção errada fica visível porque o split não se move.

Fluxo operacional (`docs/analysis/...-patterns.md:143-148`):

1. Instrumentar quem já experimentou o produto (per-user trial flag).
2. Medir quem retorna (weekly active).
3. Retorno baixo → problema de produto; rotear para o time de produto.
4. Trial baixo → problema de change management; rotear para o trabalho de ativação.
5. Re-verificar o split após cada intervenção.

Propriedades que tornam o padrão utilizável: é apenas diagnóstico (não corrige nada sozinho — explicita para onde a correção vai); exige janela de medição estável (primeiras semanas são ruidosas); e desarma alarme de gestão com mecanismo, não com argumento (`docs/analysis/...-patterns.md:131-137`).

## Implementação neste repositório

### O que já existe

- A disciplina de não confiar em métrica agregada sem validar contra o outcome real: [[docs/canonical/eval-to-production-correlation-tracking|Eval-to-Production Correlation Tracking]] (`docs/canonical/eval-to-production-correlation-tracking.md:22` — scores de eval como falsos sinais de segurança quando deixam de prever outcomes de usuário; a retenção já é lista como outcome rastreável em `:35`).
- Roteamento estruturado de achados com severidade, ownership e conversão em itens de trabalho: [[docs/canonical/qa-to-backlog-feedback-loop|QA-to-Backlog Feedback Loop]] (`docs/canonical/qa-to-backlog-feedback-loop.md:32` — capturar achados como observações estruturadas, triar por severidade/bloqueio/ownership, converter em issues). É o análogo de roteamento, mas para achados de QA, não para diagnósticos de ativação.

### O que falta

O mecanismo não existe em nenhuma forma (classification:119-123):

1. **Flag de trial per-usuário** — nenhuma telemetria distingue "experimentou" de "voltou".
2. **A regra de diagnóstico de dois ramos** — tried-and-did-not-return vs. never-tried não aparece em nenhum doc, skill ou currículo. Busca da classificação: `attribution` em `docs/canonical/` retorna apenas atribuição de custo de tokens (`docs/canonical/token-economics-gap-filling.md:33`) e de trace (`docs/system-of-record.md:202`) — eixos diferentes; `activation|adoption|trial` retorna apenas de-risking de harness, ativação de papel HoP e campos de log `feature_activation` — nada equivalente.
3. **Roteamento de ownership de falhas de ativação** — o roteamento adjacente existente (QA-to-backlog) roteia achados de review, não diagnósticos de ativação.

## Tradeoffs

| Benefício | Custo |
|---|---|
| Previne atribuir falha de ativação à qualidade do produto (e vice-versa) | Exige instrumentação limpa de trial/retenção desde o dia um |
| Desarma alarme de gestão com mecanismo, não com argumento | Janelas iniciais são ruidosas; o split precisa de período estável de medição |
| Roteia a correção para o dono que pode de fato aplicá-la | Apenas diagnóstico — não corrige nenhum dos dois lados sozinho |
| Alimenta [[docs/canonical/retention-gated-phased-rollout|Retention-Gated Phased Rollout]] e [[docs/canonical/owner-led-activation-blitz|Owner-Led Activation Blitz]] com o sinal que decide qual disparar | Intervenções simultâneas nos dois eixos confundem o split; exige re-check serial |

## Relação com outros padrões

- **Depende de:** [[docs/canonical/eval-to-production-correlation-tracking|Eval-to-Production Correlation Tracking]] — a retenção medida aqui é um dos outcomes que a correlação valida como sinal verdadeiro.
- **Alimenta:** [[docs/canonical/owner-led-activation-blitz|Owner-Led Activation Blitz]] — o ramo never-tried é o gatilho direto do programa de ativação; [[docs/canonical/retention-gated-phased-rollout|Retention-Gated Phased Rollout]] — o ramo tried-and-did-not-return bloqueia a progressão de fase (o gate de retenção falha).
- **Complementa:** [[docs/canonical/qa-to-backlog-feedback-loop|QA-to-Backlog Feedback Loop]] — mesmo formato de captura→triagem→roteamento, objeto diferente (achados de QA vs. diagnósticos de ativação); [[docs/canonical/agent-value-maturity-ladder|Agent Value Maturity Ladder]] — retenção baixa no ramo de produto pode indicar estagnação de estágio de valor.

## Referências

- `docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-patterns.md:120-148` — padrão extraído: problema, inputs, outputs, componentes e fluxo do split trial/retenção.
- `docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-classification.yaml:99-123` — classificação Missing (Medium) com evidência NOT_FOUND e adjacentes.
- `docs/canonical/eval-to-production-correlation-tracking.md:22, :35` — falsos sinais de segurança; retenção como outcome rastreável.
- `docs/canonical/qa-to-backlog-feedback-loop.md:32` — captura/triage/roteamento estruturado (análogo adjacente).
