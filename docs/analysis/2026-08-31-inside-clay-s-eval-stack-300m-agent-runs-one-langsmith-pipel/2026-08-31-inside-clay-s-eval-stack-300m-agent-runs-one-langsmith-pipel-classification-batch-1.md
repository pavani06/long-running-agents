---
title: "Classificação Batch 1 — Inside Clay's Eval Stack (300M Agent Runs, One LangSmith Pipel)"
type: classification-batch
batch: 1
date: 2026-08-31
tags: ["evals", "harness-engineering", "production", "governanca"]
aliases: ["classificação clay eval stack batch 1", "clay classification batch 1"]
relates-to: ["[[docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-patterns|Patterns Clay Eval Stack]]", "[[docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-mental-model|Mental Model]]", "[[docs/system-of-record|System of Record]]"]
sources: []
---

# Classificação Batch 1 — Clay Eval Stack vs. long-running-agents

Classificação evidência-base dos primeiros 8 padrões de `...-patterns.yaml` contra o repositório, seguindo a precedência do SOR (decisions/ > canonical/ > evidence/ > analysis/ > curriculum/ > READMEs). Nenhuma ADR em `docs/decisions/` trata de evals (única ADR aceita: Skill-Canons Bridge, `docs/system-of-record.md:161`), então o peso recai sobre `docs/canonical/`.

---

## 1. Eval Coverage Matrix

**Classificação: Partial Coverage** | **Valor de integração: High**

**Justificativa:** O catálogo de mecanismos existe distribuído e profundo — o repo tem docs canônicos para goldens, checks estruturados, LLM-as-judge, análise comportamental de traces, A/B/canary e eval humano — mas cada doc estratifica por um eixo só. `3-layer-evaluation-architecture` classifica por **tipo de mecanismo** (Deterministic/Semantic/Behavioral, `docs/canonical/3-layer-evaluation-architecture.md:28,77-83`); `eval-tier-stratification` classifica por **velocidade/trigger** (fast/medium/deep, `docs/canonical/eval-tier-stratification.md:32-36`). A matriz 2x2 do padrão (determinismo × offline/online) com meta de cobertura ("poucos mecanismos por quadrante") e lista de gaps não existe formalizada em lugar nenhum — é o vocabulário de portfólio que falta sobre docs que hoje olham para cada mecanismo isoladamente.

**Evidência:**
- `docs/canonical/3-layer-evaluation-architecture.md:28` — "Organize evaluation into three layers defined by **what they evaluate**, not by when they run" (eixo mecanismo, não determinismo×deployment).
- `docs/canonical/eval-tier-stratification.md:32-36` — tiers fast/medium/deep por runtime/trigger/decision power (eixo custo/tempo).
- Mecanismos do catálogo, cada um com doc próprio: goldens (`docs/canonical/workflow-derived-golden-question-set.md:44-47`; `docs/canonical/living-eval-dataset.md:79`), checks estruturados (`docs/canonical/constraint-anchored-evaluation.md:31-33`), LLM-judge (`docs/canonical/3-layer-evaluation-architecture.md:45-59`), análise comportamental de traces (`docs/canonical/behavioral-eval-path-analysis.md:34`), A/B + canary com eval gates (`docs/articles/evals-ecommerce-koda.md:107`), eval humano/rubricas (`curriculum/05-core-concepts/08-evaluation-rubrics.md`, via `docs/canonical/eval-tier-stratification.md:7`).
- NOT_FOUND: grep `determinism|deterministic.*nondeterministic|offline.*online` em `docs/canonical/` → único hit `docs/canonical/llm-as-fuzzy-compiler.md` (sentido não relacionado, compilação de código). Nenhum doc monta a matriz 2x2 ou o goal de cobertura por quadrante.

**Locais pesquisados:** `docs/canonical/` (grep eixos determinismo/offline/online; leitura dos docs da família evals), `docs/decisions/`, `docs/articles/`, `curriculum/` (via docs de evals), `docs/analysis/` (apenas auto-referências do pacote Clay).

---

## 2. Environment-Tiered Eval Fidelity

**Classificação: Partial Coverage** | **Valor de integração: Medium**

**Justificativa:** As camadas de ambiente existem na prática do currículo — tier fast local (pre-commit), staging shadow tests com dashboards baseline/candidate, fases de canary — mas a estratificação documentada é por **velocidade/trigger**, não por **fidelidade**. O reframe central do padrão (local intencionalmente low-fidelity sem sandbox/VFS; staging compartilha o harness de produção; "só tiers com paridade de produção sustentam claims de release") não está formalizado em nenhum lugar.

**Evidência:**
- `docs/canonical/eval-tier-stratification.md:34` — tier Fast atrelada a "Local change, pre-commit, small PR" (eixo runtime, sem noção de fidelidade).
- `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:913` — config `staging_shadow`; `:1743` — "Shadow test em staging por 2 dias"; `:1802-1848` — execução dia-D começa em staging com dashboard baseline/candidate; `:1691` — "Teste de rollback em staging"; `:1823` — `koda shadow-tests start budget_guard_removal --env staging --duration 48h --sample 100` (mesma CLI, ambiente diferente — paridade staging/produção de facto, não nomeada).
- `docs/canonical/eval-tier-stratification.md:58` — reconhece que o playbook já separa "lint/unit checks, component regression batteries, N+1 long-session gates, staging shadow tests, and canary phases" — camadas existem, sem contrato de fidelidade por tier.
- NOT_FOUND: grep `local.*sandbox|fidelity|paridade|parity` em `curriculum/07-implementation-guides/06-harness-evolution-playbook.md` → 0 matches para sandbox/fidelity/parity. Nenhum doc declara tier local como intencionalmente low-fidelity ou restringe claims de release a tiers com paridade.

**Locais pesquisados:** `docs/canonical/` (família evals), `curriculum/07-implementation-guides/06-harness-evolution-playbook.md` (grep staging/local/fidelity/parity), `curriculum/04-nivel-4-koda-specific/` (via referências cruzadas), `docs/decisions/`.

---

## 3. Production-to-Offline Feedback Loop with Drift Taxonomy

**Classificação: Partial Coverage** | **Valor de integração: High**

**Justificativa:** O loop produção→offline é o padrão mais coberto do batch: o flywheel de 9 passos converte falhas de produção em casos de eval duráveis (`docs/canonical/production-failure-regression-flywheel.md:28-41`), com refresh cadence (`production-grounded-eval-sampling.md:41`), ciclo de vida do dataset (`living-eval-dataset.md:94-99`) e até detecção de decaimento de correlação com triggers de recalibração (`eval-to-production-correlation-tracking.md:38-39`). O que falta é a **taxonomia de drift em três modos** (data drift, judge drift, eval-set mirroring) — o diagnóstico diferencial que separa "evals ficaram stale" em três falhas distintas. `model-switch-driven-eval-hardening` é adjacente ao judge drift (revalidação do dataset a cada troca de modelo, `docs/system-of-record.md:301`) mas não nomeia o modo de falha.

**Evidência:**
- `docs/canonical/production-failure-regression-flywheel.md:28-41` — flywheel completo: intake → capture → privacy → label → dedup → tier → backfill → link → prune.
- `docs/canonical/production-grounded-eval-sampling.md:41` — "Refresh cadence | Scheduled and incident-driven dataset updates".
- `docs/canonical/living-eval-dataset.md:94-99` — lifecycle do dataset (incidente → caso permanente) e infraestrutura operacional (flywheel daemon + QI loop).
- `docs/canonical/eval-to-production-correlation-tracking.md:38-39` — "Decay thresholds" + "Recalibration triggers" (drift-adjacente, sem taxonomia nomeada); `:48-49` — passos de alerta e recalibração.
- `docs/system-of-record.md:301` — `model-switch-driven-eval-hardening`: "cada troca de modelo dispara revalidação completa do dataset de eval".
- NOT_FOUND: grep `judge drift|eval drift|eval-set|data drift|mirroring|stale eval` em `docs/canonical/` → 0 matches. Os 121 hits de "drift" no repo são outros sentidos (context drift, model drift, drift de documentação).

**Locais pesquisados:** `docs/canonical/` (greps de taxonomia de drift + leitura dos 6 docs do loop), `docs/decisions/`, `docs/analysis/` (auto-referências), `curriculum/` (via correlation tracking references).

---

## 4. CLI-First Eval Harness with Remote Persistence

**Classificação: Partial Coverage** | **Valor de integração: Medium**

**Justificativa:** O repo tem harness de eval CLI-first real e maduro — `harness.sh` roda loop de fases com contrato default-FAIL e persistência local (`test-results.json`, `PROGRESS.md`), e o currículo ensina evals por CLI (`koda shadow-tests start ...`). O que não existe em forma alguma é a **segunda metade do padrão**: backend de persistência remota com write-out automático de todo resultado e histórico versionado/comparável. O próprio repo documenta essa ausência: `eval-to-production-correlation-tracking` lista "Eval history" com run IDs e distribuições como componente de um sistema a ser adicionado.

**Evidência:**
- `harness/GUIDE-analyze-and-improve.md:42` — "`test-results.json` — contrato default-FAIL; harness.sh só avança se evaluator der PASS"; `:39,43` — `PROGRESS.md` estado persistente, retomada automática; `:50-53` — loop `harness.sh`.
- `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:1823` — eval de shadow test disparado por CLI (`koda shadow-tests start ... --env staging`), sem provisioning em UI.
- `docs/canonical/eval-to-production-correlation-tracking.md:34` — "Eval history | Eval run IDs, score distributions, suite/tier, rubric version..." listado como requisito; `:65-76` — seção "What needs to be added" confirma que o sistema de história de evals não existe.
- NOT_FOUND: grep `LangSmith|remote persist|CLI-first|cli first` em `docs/` → apenas os arquivos do próprio pacote Clay. Persistência de resultados é local (arquivos) ou telemetria SQLite local (`docs/system-of-record.md:128`); nenhum store remoto/versionado de resultados de eval.

**Locais pesquisados:** `docs/` (grep LangSmith/remote persist/CLI-first), `docs/canonical/` (família evals), `harness/GUIDE-analyze-and-improve.md` (leitura direta), `docs/system-of-record.md:128` (stack de telemetria), `curriculum/07-implementation-guides/`.

---

## 5. Plug-and-Play Harness with BYO Evaluators

**Classificação: Partial Coverage** | **Valor de integração: Medium**

**Justificativa:** O repo tem um harness compartilhado real que onboarding fontes plugáveis: o pipeline `analyze-and-improve` roda qualquer fonte externa pelas mesmas 7 fases com execução, evaluators, gates e persistência uniforme de artefatos (8 módulos incl. eval, `docs/system-of-record.md:46`). `generator-evaluator` separa a autoria do evaluator como papel distinto (fundação para BYO judges, `docs/canonical/3-layer-evaluation-architecture.md:94`). Falta o contrato específico do padrão: **novos produtos de agente plugando suas suites e evaluators próprios (BYO LLM judges) num harness compartilhado**, com comparabilidade cross-produto. O harness do repo onboarding *fontes de conhecimento*, não *agentes/produtos com evaluators autoriais*; não há doc de contrato de onboarding multi-produto.

**Evidência:**
- `docs/system-of-record.md:46` — skill `analyze-and-improve`: "Pipeline knowledge → patterns → classification → improvements. Harness com cache, retry, model tiering, schemas, chunking, trajectory, eval, refinement (8 módulos, stdlib)".
- `.opencode/skills/analyze-and-improve/SKILL.md:18` — parâmetro `source` aceita qualquer path/URL/array: a fonte é a parte plugável do harness.
- `harness/GUIDE-analyze-and-improve.md:42,53` — evaluator como gate por fase no harness compartilhado.
- `docs/canonical/3-layer-evaluation-architecture.md:94` — generator-evaluator como fundação do LLM-as-Judge (separação de autoria do evaluator); `docs/canonical/compartmented-evaluation-architecture.md:52-54` — "Generator-Evaluator says 'generate with one agent, evaluate with another'" e a relação structural.
- `docs/system-of-record.md:152` — `skill-testing-conventions` (test harness para skills) — harness de teste uniforme, escopo skills.
- NOT_FOUND: nenhum doc descreve onboarding de novos produtos/agentes com evaluators próprios num harness compartilhado (greps `LangSmith`, leitura da família harness/evals; `docs/canonical/measured-harness-evolution-lifecycle.md` trata de ciclo de vida, não de contrato plug-and-play).

**Locais pesquisados:** `docs/canonical/` (generator-evaluator, compartmented-evaluation, harness lifecycle), `.opencode/skills/analyze-and-improve/SKILL.md`, `harness/GUIDE-analyze-and-improve.md`, `docs/system-of-record.md:36-67`, `docs/decisions/`.

---

## 6. Structured Partial Checks over Exact Goldens

**Classificação: Partial Coverage** | **Valor de integração: Medium**

**Justificativa:** Os três componentes mecânicos existem, cada um profundo em doc canônico próprio: (a) asserções parciais estruturadas — a verification matrix do `constraint-anchored-evaluation` checa só as constraints explícitas (as partes que importam), não o output inteiro; (b) asserções de trajetória/tool calls — os expected execution path templates do `behavioral-eval-path-analysis` (equivalente direto de "pergunta de preço exige leitura da tabela de preços"); (c) goldens — `workflow-derived-golden-question-set` e `living-eval-dataset`. O que falta é o **reframe**: a regra de casar estrictez com estabilidade do output (goldens exatos quebram em reordenação irrelevante → eval ruidoso → suite ignorada; reter goldens exatos só para superfícies simples). O repo na verdade pende para o lado oposto — golden answers humanas como mecanismo geral (`docs/canonical/business-outcome-first-eval-pipeline.md:28` via `workflow-derived-golden-question-set.md:64`) — sem a regra de restrição de goldens a superfícies estáveis.

**Evidência:**
- `docs/canonical/constraint-anchored-evaluation.md:31-33` — verification matrix `constraint -> check -> pass/fail -> violation detail`, aprovando só pelo que importa; `:52-59` — contraste com avaliação subjetiva de output completo.
- `docs/canonical/behavioral-eval-path-analysis.md:76-83` — "Define an expected execution path template per query category... Compare the actual execution path against the template" (asserção de trajetória); templates mantidos junto aos golden answers (`:83`).
- `docs/canonical/3-layer-evaluation-architecture.md:36-39` — Layer 1: asserções estruturais de schema/formato sobre o output.
- `docs/canonical/magnitude-direction-verifier-split.md:100` — verificação graduada (direção sobre magnitude exata) — mesma família de "não exigir o valor exato".
- `docs/canonical/workflow-derived-golden-question-set.md:44-47` — golden set (~150 perguntas) para superfície restrita pré-launch.
- NOT_FOUND: nenhum doc formula o trade goldens-exatos-vs-checks-parciais como problema de ruído/confiança da suite (greps `golden` nos 10 docs canônicos que citam; leitura dos 5 principais). A regra "retire or relax checks that fire on irrelevant reordering" não aparece.

**Locais pesquisados:** `docs/canonical/` (grep `golden` → 10 arquivos, lidos os 5 relevantes; constraint-anchored; behavioral-eval; magnitude-direction), `docs/decisions/`, `curriculum/05-core-concepts/08-evaluation-rubrics.md` (via relações).

---

## 7. Deterministic Multi-Turn Scripts over Simulated Users

**Classificação: Partial Coverage** | **Valor de integração: Medium**

**Justificativa:** A mecânica central existe canonizada: `n-plus-one-long-session-evals` carrega um fixture fixo de N turnos (user turns hardcoded/derivados de traces reais) e testa o turno N+1 — multi-turn determinístico por construção, com o agente sob teste como único elemento variável. Fixtures derivados de conversas reais também existem (spot-check set com traces KODA reconstruídos, replay de produção). O que não existe é a **decisão explícita contra simulated-user LLM**: o trade "segundo agente não determinístico que precisa dos próprios updates e evals; aposentar quando manutenção excede valor" não é discutido em doc, código ou currículo — os greps só encontram o próprio pacote Clay.

**Evidência:**
- `docs/canonical/n-plus-one-long-session-evals.md:28-38` — "Load a realistic N-turn conversation fixture. Apply the production context strategy. Ask the next-turn prompt..." (turnos fixos scriptados; `:38` — fixtures incluem follow-ups que referenciam produtos/decisões anteriores).
- `docs/canonical/repeatable-agent-spot-check-set.md:59-60` — 4 traces KODA reais reconstruídos como casos repetíveis (seed traces de conversas passadas); `docs/canonical/production-grounded-eval-sampling.md:40` — replay infrastructure (fixtures de produção).
- NOT_FOUND: grep `user simulator|usuário simulado|simulated-user|agente usuário` em `docs/` → apenas `2026-08-31-inside-clay-...-patterns.md:146` e `...-analysis.md:88` (auto-referências). Nenhum doc discute simulated users como alternativa rejeitada.

**Locais pesquisados:** `docs/canonical/` (n-plus-one, spot-check, production-grounded), `docs/` (grep simulated user em PT/EN), `docs/analysis/2026-06-09-how-we-solved-context-management-in-agents/` (fonte do N+1), `curriculum/` (via N+1 references), `docs/decisions/`.

---

## 8. Perceived-Eval

**Classificação: Missing** | **Valor de integração: High**

**Justificativa:** Nenhum doc, código ou currículo trata o comportamento de correção do usuário como dado de avaliação. Os componentes do padrão — detector de correction/pushback/redirection, métricas comportamentais de saída do chat/stuck/rage quit, NPS como entrada contínua — não existem em forma alguma. O que existe é só o vizinho fraco: CSAT como *proxy de outcome* numa lista de métricas de produção (`eval-to-production-correlation-tracking.md:35`; playbook `:1596`), e monitoramento de produção com triagem humana (`always-on-monitoring-human-triage`, SOR:300) — este monitora anomalias do sistema, não qualidade percebida pelo usuário final. `presence-in-the-loop-metric` calibra intervenção de operadores humanos, não percepção de usuários.

**Evidência (NOT_FOUND):**
- Grep `NPS|rage quit|perceived quality|user correction|pushback` em `docs/` → apenas os arquivos do pacote Clay + `docs/articles/evals-ecommerce-koda.md` (cujo conteúdo nas linhas casadas — 107, 109, 167 — é amostragem de produção/A-B, sem mecânica de perceived-eval).
- Grep `correção do usuário|cliente corrige|usuário corrige` no repo inteiro → 0 matches.
- CSAT aparece só como métrica de outcome: `docs/canonical/eval-to-production-correlation-tracking.md:35` ("CSAT proxy" na tabela de production outcomes); `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:1596` (dashboard baseline/candidate).
- Adjacentes distintos: `docs/system-of-record.md:300` (`always-on-monitoring-human-triage` — anomalias com triagem humana); `docs/system-of-record.md:238` (`presence-in-the-loop-metric` — intervenção de operadores).

**Locais pesquisados:** `docs/canonical/` (greps EN/PT acima; leitura de eval-to-production-correlation-tracking), `docs/articles/`, `docs/analysis/` (só auto-referências), `curriculum/` (grep repo-wide CSAT/satisfação → 34 arquivos, todos como métrica de dashboard/outcome, nenhum como sinal de eval), `.opencode/skills/`, `docs/decisions/`.

---

*Batch 1 de 2 — 8 padrões classificados. O orquestrador consolida os batches no classification.md final.*
