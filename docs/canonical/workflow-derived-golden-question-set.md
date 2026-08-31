---
title: "Workflow-Derived Golden Question Set"
type: canonical
tags: ["evals", "production", "governanca"]
Status: Active
Source: "AI Engineer talk — Sait Izmit, Snowflake (GTM assistant: 6.000 usuários, 1M+ perguntas)"
Classification: "Partial Coverage (P2, Medium integration value)"
Precedence: "Level 2 (docs/system-of-record.md)"
last_updated: 2026-08-30
aliases: ["golden question set", "workflow-derived eval questions", "pre-launch golden set", "150 questions"]
relates-to:
  - "[[docs/canonical/business-outcome-first-eval-pipeline|Business-Outcome-First Eval Pipeline]]"
  - "[[docs/canonical/repeatable-agent-spot-check-set|Repeatable Agent Spot-Check Set]]"
  - "[[docs/canonical/eval-driven-development-timeline|Eval-Driven Development Timeline]]"
  - "[[docs/canonical/domain-embedded-workflow-automation-wedge|Domain-Embedded Workflow Automation Wedge]]"
  - "[[docs/canonical/quality-over-coverage-trust-scoping|Quality-Over-Coverage Trust Scoping]]"
  - "[[docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-analysis|GTM AI Agents Analysis]]"
sources:
  - "[[docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-patterns|GTM AI Agents Patterns]]"
  - "[[docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-classification|GTM AI Agents Classification]]"
---

# Workflow-Derived Golden Question Set

**Type:** Canonical Pattern
**Status:** Active
**Source:** AI Engineer talk — Sait Izmit, Snowflake (GTM assistant: 6.000 usuários, 1M+ perguntas, ~20 skills)
**Classification:** Partial Coverage (P2, Medium integration value)
**Precedence:** Level 2 ([[docs/system-of-record|System of Record]])

---

## Problema

Eval sets construídos a partir do inventário de dados conectados testam a **cobertura**, não o **trabalho** — os gaps de qualidade ficam invisíveis até usuários reais os atingirem (`docs/analysis/...-patterns.md:22-25`). O anti-padrão: o time conecta Salesforce, transcripts e views semânticas, e deriva as perguntas de eval daí ("o que dá para perguntar?"). O eval mede o que a implementação expõe, não o que o job-to-be-done exige.

O caso-fonte demonstra o custo de não ter o set: na Snowflake, o workflow de vendas real foi extraído para uma planilha e ~150 perguntas foram escritas **antes de qualquer dado ser conectado** — e a primeira execução do agente contra o golden set retornou 50% de acurácia, capturando o gap de qualidade pré-launch somente porque o set existia (`docs/analysis/...-patterns.md:26-33`). Engenharia objetou que "os dados ainda não estão conectados" — a objeção é exatamente o ponto: o set não depende do estado da implementação.

## Solução

Autorar o golden set a partir do **workflow real extraído**, não do inventário de dados, como passo zero da construção do eval (`docs/analysis/...-patterns.md:48-53`):

1. **Extrair o workflow real** para um artefato explícito (o processo de vendas capturado numa planilha).
2. **Escrever N perguntas** (~150) que os usuários realmente farão, independentes do que está conectado.
3. **Executar o agente contra o set** antes do lançamento.
4. **Registrar o score de acurácia como baseline** de qualidade (no caso-fonte: 50% na primeira execução).
5. **Gatear o lançamento pelo score**; re-executar conforme cobertura e features crescem.

Propriedades centrais (`docs/analysis/...-patterns.md:34-41`):

- Torna o gap de qualidade **mensurável antes de qualquer usuário vê-lo**.
- Ancora o eval no job-to-be-done, não no inventário de dados.
- É **independente do estado da implementação** — pode ser autorado antes de o agente existir.
- Permanece como **instrumento permanente de regressão** conforme cobertura e features crescem.

Limitações declaradas: exige acesso ao workflow e expertise de domínio antes do build; o set deve ser mantido conforme o workflow evolui; e é tão bom quanto a extração do workflow — casos exploratórios imprevistos escapam.

## Implementação neste repositório

### O que já existe

A maquinaria de golden answers e seeds de eval existe em profundidade canônica — mas ancorada em **logs de produção** (exige sistema rodando):

- [[docs/canonical/business-outcome-first-eval-pipeline|Business-Outcome-First Eval Pipeline]] — a sequência invertida: "Invert the eval pipeline construction sequence: define business success first, then create golden answers from domain experts, then build the technical pipeline" (`docs/canonical/business-outcome-first-eval-pipeline.md:28`); o sourcing: "Source ~200 real production queries from human agent logs (not synthetic queries)" (`:55`); e o gate: "This enables evidence-based go/no-go deployment decisions: deploy when predicted deflection rate exceeds the business target" (`:75`).
- [[docs/canonical/domain-embedded-workflow-automation-wedge|Domain-Embedded Workflow Automation Wedge]] — "Domain eval seeds | Cases derived from observed work, including successful paths and exception paths" (`docs/canonical/domain-embedded-workflow-automation-wedge.md:39`) — o artefato de descoberta existe; falta ele como fonte de perguntas.
- [[docs/canonical/repeatable-agent-spot-check-set|Repeatable Agent Spot-Check Set]] — "Choose 5-15 cases that cover the highest-value and highest-risk workflows" (`docs/canonical/repeatable-agent-spot-check-set.md:46`) — o subset de spot-check, não o set integral.
- [[docs/canonical/eval-driven-development-timeline|Eval-Driven Development Timeline]] — "Golden answers: domain experts author correct responses for the initial ~200 queries; build the living eval dataset with categorization taxonomy" (`docs/canonical/eval-driven-development-timeline.md:37`).

### O que falta

(classification:36-41)

1. **A passagem de autoria pré-build** — ~150 perguntas derivadas do artefato de workflow extraído **antes de qualquer dado ser conectado**. As golden answers do repo nascem de logs de produção queries; o caminho "workflow → perguntas → agente inexistente ainda" não existe.
2. **O artefato de extração de workflow como fonte de perguntas** — a descoberta do wedge produz eval seeds observados, mas não um question set autoral derivado do workflow documentado.
3. **O baseline de acurácia de primeira execução gravado** — o "catch" de 50% pré-launch; o repo não registra primeira execução como baseline de referência.
4. **Encaixe**: seria o **Step 0** do Business-Outcome-First Eval Pipeline (autoria antes dos ~200 queries de produção) e entrada no currículo de produção N4/KODA (classification:40-41).

## Tradeoffs

| Benefício | Custo |
|---|---|
| Gap de qualidade mensurável antes de qualquer usuário ver (o 50% foi capturado pré-launch porque o set existia) | Exige acesso ao workflow e expertise de domínio antes do build |
| Eval ancorado no job-to-be-done, não no inventário de dados | O set deve ser mantido conforme o workflow evolui |
| Independente do estado da implementação: autorável antes de o agente existir | Só tão bom quanto a extração do workflow — casos exploratórios imprevistos escapam |
| Instrumento permanente de regressão conforme cobertura cresce | ~150 perguntas autorais custam tempo de especialista que o sourcing de logs de produção não cobra |

## Relação com outros padrões

- **Step 0 de:** [[docs/canonical/business-outcome-first-eval-pipeline|Business-Outcome-First Eval Pipeline]] — o golden set workflow-derived precede e habilita o sourcing de ~200 queries de produção; sem ele, o pipeline só começa depois de existir sistema rodando.
- **Fonte de:** [[docs/canonical/repeatable-agent-spot-check-set|Repeatable Agent Spot-Check Set]] — o golden set é a fonte da qual os 5-15 spot-checks de maior valor/risco são selecionados.
- **Estende:** [[docs/canonical/domain-embedded-workflow-automation-wedge|Domain-Embedded Workflow Automation Wedge]] — os shadowing notes e o decision inventory da descoberta são a matéria-prima da extração de workflow.
- **Sequencia com:** [[docs/canonical/eval-driven-development-timeline|Eval-Driven Development Timeline]] — eval-first já é a sequência canônica; este padrão adiciona a autoria pré-agente.
- **Habilita:** [[docs/canonical/quality-over-coverage-trust-scoping|Quality-Over-Coverage Trust Scoping]] — sem score por zona de perguntas, não há como mapear zonas de acurácia para cortar o escopo de launch.

## Referências

- `docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-patterns.md:22-53` — padrão extraído: workflow em planilha, ~150 perguntas pré-conexão, primeira execução a 50%, gate de lançamento.
- `docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-classification.yaml:8-41` — classificação Partial Coverage (Medium) com evidência file:line e mecânicas faltantes.
- `docs/canonical/business-outcome-first-eval-pipeline.md:28, :55, :75` — sequência invertida, sourcing de golden answers, gate go/no-go.
- `docs/canonical/domain-embedded-workflow-automation-wedge.md:39` — domain eval seeds de trabalho observado.
- `docs/canonical/repeatable-agent-spot-check-set.md:46` — seleção 5-15 casos de maior valor/risco.
- `docs/canonical/eval-driven-development-timeline.md:37` — golden answers de domain experts com taxonomia.
