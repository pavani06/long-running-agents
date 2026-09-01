---
title: "Classificação — Inside Clay's Eval Stack (300M Agent Runs, One LangSmith Pipeline)"
type: analysis
date: 2026-08-31
tags: ["evals", "harness-engineering", "production", "governanca"]
aliases: ["classificação clay eval stack", "clay classification consolidada"]
relates-to: ["[[docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-patterns|Patterns Clay Eval Stack]]", "[[docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-mental-model|Mental Model]]", "[[docs/system-of-record|System of Record]]"]
---

# Classificação — Clay Eval Stack vs. long-running-agents

Consolidação dos batches 1 e 2: 16 padrões classificados com evidência, seguindo a precedência do SOR (decisions/ > canonical/ > evidence/ > analysis/ > curriculum/ > READMEs). Batches-fonte: `-classification-batch-1.md` e `-classification-batch-2.md`.


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

## 9. Unified Tool Surface Flywheel

**Classification: Partial Coverage** — Integration value: **High**

**Justification.** Os elementos existem isolados: o repo ensina interface universal para agentes (file-system materialization), dispatch unico de tools, e flywheels de falha-para-melhoria. O que falta e a mecanica central do padrao Clay: uma unica autoridade de tool exposta identicamente como UI, CLI e API publica, com agentes internos consumindo exatamente as mesmas tools — de forma que toda falha de tool do agente dobre como sinal de qualidade da API publica.

**Evidence.**

- `docs/canonical/file-system-materialization.md:48` — espectro de materializacao: o agente opera "using the same tools it would use for any software project"; `:34` — "the interface should be designed for the agent's strengths" (substrato universal de acesso, analogo mais proximo).
- `docs/canonical/file-system-materialization.md:38` — "Materialize everything into files, git, and grep... The file system is the universal interface that every coding model understands".
- `docs/system-of-record.md:178` — `deterministic-tool-dispatch.md` (12FA Padrao 2): autoridade unica de dispatch (tools como JSON + codigo deterministico).
- `docs/canonical/production-failure-regression-flywheel.md:28` — "Every production failure that reveals a behavioral gap should become a durable eval regression case" (a metade falha-melhora do flywheel, sem o lado API publica).
- `docs/system-of-record.md:312` — `closed-loop-help-api.md` (Kavak): agente trava -> help API -> resolucao vira training data (loop de falha-para-aprimoramento voltado ao agente, nao a superficie publica).
- `docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-classification.md:38` — auditoria propria do repo: File-System Materialization e o analogo de "universal tooling surface", mas a implementacao concreta e NOT_FOUND.

**NOT_FOUND (o que falta).** Unica tool authority servindo UI + CLI + API publica simultaneamente; agentes internos como consumidores das mesmas tools de clientes externos; "every agent tool failure doubles as public API quality signal". Busca: grep `tool surface|single tool|same tools|UI, CLI|UI/CLI|public API` em `*.md` do repo inteiro — matches apenas em `docs/canonical/file-system-materialization.md:48` e no proprio pacote-fonte Clay (`docs/analysis/2026-08-31-inside-clay-s-eval-stack-.../`).

**Integration value: High.** O reframe conecta tres docs canonicas existentes (file-system-materialization, deterministic-tool-dispatch, production-failure-regression-flywheel) sob uma tese de produto: superficie unica como multiplicador de pontos de captura de falha. E a generalizacao que o repo ensina por partes, nunca nomeada.

---

## 10. Shadow Builds on Separated Compute

**Classification: Partial Coverage** — Integration value: **Medium**

**Justification.** O repo tem mecanicas adjacentes em profundidade: shadow deployment de comparacao (curriculo), staged shadow tests + canary + rollback (declarados Better Implementation pelo proprio repo para rollout gates), e worktree isolado por issue (separacao de execucao por construcao). Falta o nucleo do padrao Clay: alvo de deploy shadow para artefatos construidos por agentes e separacao arquitetural entre plano de serving e plano de development compute, com guardrails definidos up-front que concedem autonomia de build.

**Evidence.**

- `curriculum/05-core-concepts/02-planning-execution-separation.md:2190-2199` — receita de shadow deployment: clonar trafego real, rodar novo Planner em paralelo, executar contratos em sandbox, promover so quando melhor/igual em 98%+ dos casos (shadow de comparacao, nao shadow build de artefato de agente).
- `docs/analysis/2026-06-10-eval-maturity-phases/2026-06-10-eval-maturity-phases-classification.md:121-131` — "Better Implementation" de Canary Eval Rollout Gate: "staged shadow tests, regression batteries, N+1 gates, staged canary percentages, production metrics, trace sampling, rollback commands" (`curriculum/07-implementation-guides/06-harness-evolution-playbook.md:783-790`, `:2434-2444`).
- `.opencode/skills/issue-start/SKILL.md:72,82` — `git worktree add` isolado por issue (`.worktrees/<N>-<slug>`): superficie de execucao separada por construcao para trabalho de agente.
- `docs/system-of-record.md:247` — `shadow-review-pipeline.md`: agente shadow revisa em paralelo pre-merge (shadow de revisao — mecanica diferente de shadow build).

**NOT_FOUND (o que falta).** Shadow deployment target (S3 na fonte) para data models construidos por agentes; separacao serving compute vs development compute como planos arquiteturais; "guardrails defined up front rather than review afterwards" como porta de autonomia de build. Busca: grep `shadow build|shadow deploy|shadow deployment|separated compute|dev compute|serving compute` em `*.md` — matches apenas no pacote-fonte Clay e em `02-planning-execution-separation.md:2190`; grep `Athena|\bS3\b` — nenhuma ocorrencia de shadow target (apenas S3 como storage generico em case studies).

**Integration value: Medium.** O principio "seguranca por construcao, nao por politica" complementa a familia de autonomia/gates do repo (manual-brake-question-gate, accidental-brake-replacement, evals-as-brakes), mas a mecanica de shadow build e especifica de plataformas de dados produto.

---

## 11. Agent-First Data Foundation

**Classification: Partial Coverage** — Integration value: **High**

**Justification.** A intuicao central — dados projetados para consumo de agente, nao para dashboard humano — existe em profundidade no repo, e a propria doc canônica de freshness declara a implementacao ausente. Existe tambem a plataforma unificada first+third-party (Snowflake GTM) com foco em governanca herdada. Falta o reframe Clay: agentes como usuario first-class de design-time de uma fundacao unica, cuja fragmentacao e o gargalo concreto dos learning loops.

**Evidence.**

- `docs/canonical/agent-specific-data-freshness-pipeline.md:22` — "Data pipelines built for human consumption... tolerate staleness, ambiguity, and inconsistency... Agents treat every data point literally" (a tese agent-first dos dados, formulada).
- `docs/canonical/agent-specific-data-freshness-pipeline.md:86` — "No data pipelines designed for agent consumption rather than human dashboard consumption" (a propria doc declara o gap; classificada Missing na implementacao, `:15`).
- `docs/canonical/agent-specific-data-freshness-pipeline.md:93` — "Data quality becomes a first-class engineering concern — 60% of project time may need to be allocated to data foundation".
- `docs/canonical/centralized-data-plane-inherited-rbac.md:44` — "Plataforma unificada de dados | Consolida first-party + third-party em um unico plano"; `:68-70` — o que falta: a arquitetura de consolidacao-e-heranca como pre-requisito.
- `docs/analysis/2026-06-26-the-production-ai-playbook-deploying-agents-at-enterprise-sc/2026-06-26-the-production-ai-playbook-deploying-agents-at-enterprise-sc-analysis.md:375` — ferramentas de dados evoluiram para consumo humano; agentes nao tem essa tolerancia; 60% do esforco vai para data foundation.

**NOT_FOUND (o que falta).** "Agents as the design-time first-class user" como criterio de arquitetura da plataforma; eliminacao de cross-database stitching como gargalo nomeado de learning loops; datastore como "playground for agents"; compute escalavel (Athena-class) para acesso agêntico. Busca: grep `data foundation|unified data|data platform|fragmented datastore|cross-database` em `*.md` — cobertura parcial em freshness/RBAC/production-playbook, sem o framing agent-first de plataforma; grep `first class user|first-class user` — apenas pacote-fonte.

**Integration value: High.** Nomeia o pre-requisito arquitetural que a propria doc de freshness do repo declara ausente; unificaria centralized-data-plane + freshness pipeline + epistemic-memory-graph sob uma tese de fundacao de dados para agentes.

---

## 12. Skills and CLI as Native Agent Data Access

**Classification: Partial Coverage** — Integration value: **Medium**

**Justification.** O repo opera a mecanica do padrao no proprio metabolismo: 35 skills agente-orientadas, CLI `obsidian-eval` para scan/query do vault, substrato de arquivos como interface universal, delegacao goal-level e execucao longa com estado persistente. O que falta e o pareamento especifico: skills + CLI dedicados como acesso nativo a uma plataforma de dados unificada, com execucoes goal-level de 1-2h em compute escalavel cujo output e novo data model.

**Evidence.**

- `docs/system-of-record.md:36-67` — biblioteca de 35 skills em `.opencode/skills/` como superficie operacional primeira-classe dos agentes (o repo e, ele mesmo, um sistema agêntico orientado a skills).
- `README.md:159` — CLI `obsidian-eval` (@pavani/obsidian-eval) "para scan, query, grafo e cross-vault wikilinks" — acesso nativo de dados do knowledge vault sem adaptador humano; `docs/system-of-record.md:127`.
- `docs/canonical/file-system-materialization.md:38,48` — arquivos/git/grep como interface universal que agentes ja dominam.
- `docs/canonical/goal-driven-agents-over-workflows.md:37` — hard goal + "full tool/API access and persistence across the task horizon"; `:54` — "persistence: agent survives across the whole horizon (own plan, own replans)" (delegacao goal-level, nao step-level).
- `docs/system-of-record.md:180` — `serializable-pause-resume-state.md` (12FA Padrao 4): base canônica para execucao longa; harness `harness.sh` + `PROGRESS.md` com estado persistente entre passos (`harness/GUIDE-analyze-and-improve.md`, §1-3).

**NOT_FOUND (o que falta).** Skills/CLI framing como camada de acesso a data platform (o alvo do repo e o vault de conhecimento, nao uma plataforma de dados de produto); execucoes de 1-2 horas em compute escalavel (Athena) com resultado = novo data model; pareamento explicito com shadow builds. Busca: grep `dedicated CLI|goal-level|1-2 hours|long-running goal` em `*.md` — sem correspondencia fora do pacote-fonte.

**Integration value: Medium.** A mecanica ja e nativa do repo (skills + CLI + goals + long-running); o delta e o contexto de plataforma de dados — util principalmente como ponte curricular entre file-system-materialization e goal-driven-agents.

---

## 13. Eval-Gated Autonomy

**Classification: Already Exists** — Integration value: **Low**

**Justification.** Cada componente do padrao Clay existe em profundidade canônica, e a regra de acoplamento central — autonomia/velocidade como funcao da qualidade do eval — esta formulada verbatim em `evals-as-brakes.md`. O gate mecanico (eval pass obrigatorio para mudanca), o sequenciamento evals-first, a graduacao para automacao e o tratamento de mudancas sem revisao humana por diff estao todos documentados como padroes canonicos ativos. O delta Clay (o autor da mundanca ser um agente de codigo/dados, nao um humano) e coberto pelos docs de auto-approve e graduacao comportamental.

**Evidence.**

- `docs/canonical/evals-as-brakes.md:43` — "permitted shipping velocity is a function of eval quality and coverage" (a regra de acoplamento, canônica); `:49-54` — tabela de tiers auto-merge/daily-batch/manual-gate atrelados a cobertura de eval; `:59-63` — tier auto-merge requer `eval_coverage: ">= 0.9 of changed behaviors"` + correlacao eval-producao.
- `docs/canonical/pr-gated-eval-enforcement.md:28` — eval report obrigatorio em PRs que tocam "prompt, model, tool, context, memory, scoring, or agent-loop behavior"; `:51` — "Block merge when thresholds fail unless an explicit waiver is recorded".
- `docs/system-of-record.md:289` — `eval-driven-development-timeline.md`: "6 semanas de infraestrutura de eval antes de qualquer experimentacao com modelos" (evals-first sequencing: a suite precede e restringe a delegacao).
- `docs/canonical/comment-decay-readiness-signal.md:60` — "o tier auto-merge e readiness eval-based" (criterio de graduacao para autonomia); `:42` — criterio comportamental explicito de prontidao para automacao.
- `docs/system-of-record.md:329` — `semantic-rule-gated-auto-approve-block.md` (Qodo): auto-approve de PRs triviais e auto-block de violacoes — mundancas aprovadas sem revisao humana por diff, gateadas por regras semânticas.
- `docs/system-of-record.md:262` — `autonomy-curriculum-sampling.md`: progressao observe-assist-own para autonomia; `docs/system-of-record.md:303` — `model-agnostic-agent-vm-harness.md` (Kavak): modelo swapavel gateado por evals — mudanca de componente validada por eval gate, nao por confianca.
- `docs/system-of-record.md:305` — `evals-as-brakes.md` (Kavak): "so pisa no acelerador se tiver os freios certos" — resposta a risco e construir evals, nao desacelerar.

**Integration value: Low.** Nada estrutural a acrescenter; o maximo seria uma nota curricular conectando as pecas existentes sob o rotulo "eval-gated autonomy" (a formula "autonomy becomes a property of the eval suite, not of trust in the agent" seria uma citacao de sintese, nao nova mecanica).

---

## 14. Observability-Threshold Eval Trigger

**Classification: Partial Coverage** — Integration value: **Medium**

**Justification.** O repo tem gatilhos de investimento em evals maduros, mas de tipo diferente: pain-based (reativo, sinal de dor observado) e nao capacity-based (estrutural, incapacidade humana de observar). A decisao binaria do padrao Clay — abaixo do threshold tolerar evals leves; acima (incapacidade estrutural de inspecionar traces/contatar clientes) investimento nao-negociavel — nao existe em nenhuma superficie.

**Evidence.**

- `docs/canonical/pain-signal-eval-progression-gate.md:28` — "eval maturity as a gate driven by pain signals instead of a calendar roadmap"; `:36` — "Approve only the smallest eval capability that addresses the observed pain" (gatilho por dor, o anello mais proximo).
- `docs/system-of-record.md:321` — `pull-based-infrastructure-on-pain.md` (Snowflake GTM): "stack minimo de lancamento e endurecimento reativo puxado por dor, nao por antecipacao" (investimento reativo, sem modelo de threshold).
- `docs/analysis/2026-06-10-eval-maturity-phases/2026-06-10-eval-maturity-phases-analysis.md:31` — Fase 4: saida por "volume suficiente e representatividade aparente" (volume aparece como sinal de fase, nao como threshold de capacidade humana).
- `docs/system-of-record.md:313` — `eval-investment-parity.md` (Kavak): paridade orçamentaria evals/construcao (quanto investir, nao quando se torna obrigatorio).
- `docs/system-of-record.md:282` — `eval-dashboard-primary-detection-surface.md`: dashboard em tempo real como superficie primaria de deteccao (a resposta ao volume, sem o gatilho que a justifica).

**NOT_FOUND (o que falta).** Modelo de capacidade de observacao humana (traces revieweis por semana, clientes contataveis); metricas de volume (runs/mes, mensagens/semana) comparadas contra essa capacidade; regra de decisao "structural inability to observe -> eval investment non-negotiable"; o conceito de "maturity theater" que o padrao rejeita. Busca: grep `human observation|inspect every trace|observation capacity|maturity theater` em `*.md` — zero matches fora do pacote-fonte; grep `trace volume` — apenas `docs/canonical/centralized-cross-framework-tracing.md:162` (framing de custo/infra, nao de gatilho de investimento).

**Integration value: Medium.** Complementa o pain-signal gate nomeando quando evals leves deixam de ser aceitaveis; o threshold estrutural e o gatilho faltante na progressao de maturidade que o repo ja ensina.

---

## 15. Bulk In-Context Trace Analysis

**Classification: Partial Coverage** — Integration value: **High**

**Justification.** Analise de traces existe no repo em profundidade (Layer 3 comportamental, tracing centralizado cross-framework, classificacao LLM de logs em escala, guia e licao inteira de trace reading) — mas todos os mecanismos existentes sao ou deterministicos por-item ou classificacao LLM por-item em taxonomia. O mecanismo Clay — amostra de ~10k traces submetida in-context a um frontier model com goal de trend-finding, como substituto escalavel do vibe review — e ausente, incluindo o reconhecimento do frontier-model step change como habilitador.

**Evidence.**

- `docs/canonical/behavioral-eval-path-analysis.md:34` — Layer 3 consome a execucao completa (traces ordenados de tool calls) e produz behavioral scores — via algoritmos deterministicos; `:158-165` — a logica de consumo e NOT_FOUND no repo ("The trace data exists but no evaluation logic consumes it for path analysis").
- `docs/canonical/llm-classified-log-taxonomy.md:48,53` — pipeline de classificacao LLM sobre logs de producao em volume (~40k perguntas/semana) com tiering de modelo e amostragem — LLM-at-scale sobre logs, mas classificacao por item em taxonomia hierarquica, nao sintese de tendencias in-context.
- `docs/system-of-record.md:291` — `centralized-cross-framework-tracing.md`: schema unificado com "text-to-SQL query interface" e trace sampling em escala enterprise; `:162` do doc canônico — "Trace volume at enterprise scale... demands significant storage and processing infrastructure".
- `curriculum/07-implementation-guides/05-trace-analysis-guide.md` — guia de implementacao de analise de traces; `curriculum/02-nivel-2-practical-patterns/04-trace-reading.md` (5.089 linhas, o maior arquivo do curriculo — `webpage/analise-arquitetural.md:13`) — trace reading ensinado em profundidade.
- `curriculum/05-core-concepts/08-evaluation-rubrics.md:5923` — Always-On Monitoring: "taxa de compressao agressiva (ex: 10.000 conversas -> 5 para revisao humana)" — a direcao oposta: comprimir volume para revisao humana, nao expandir volume para sintese pelo modelo.

**NOT_FOUND (o que falta).** Submissao in-context de amostra grande (~10k) de traces a frontier model; prompts de trend-finding; findings -> novos eval cases como pipeline nomeado; frontier-model step change como conversor direto em observabilidade. Busca: grep `10k examples|bulk trace|in-context.*trace|large trace sample` em `*.md` — sem mecanica de analise in-context em massa fora do pacote-fonte; `10\.000` ocorre apenas em contextos de escala de volume/curriculo, nunca como tamanho de amostra de analise LLM.

**Integration value: High.** E o elo que converte a infraestrutura de trace que o repo ja tem (tracer.ts, telemetry.db, span pipeline) e a mecanica de classificacao LLM (llm-classified-log-taxonomy) em deteccao de tendencias em escala — o substituto explicito para vibe review que o batch de gaps do repo procura.

---

## 16. Self-Iterating Agent Loop

**Classification: Partial Coverage** — Integration value: **High**

**Justification.** O repo tem multiplos loops fechados canônicos — closed-loop agent OS (intake->roteamento->writeback), fleet learning (erro->captura->gate->distribuicao), regression flywheel (falha->caso permanente), GC meta-loop (observacao humana->alavancagem de harness) — e a propria analise Kavak registra o "recursive self-improvement loop" no nivel organizacional. O que falta e a composicao-alvo Clay: todos os elos (orquestracao, execucao, observacao, feedback) operando sobre uma fundacao de dados unificada, com agentes raciocinando sobre o feedback acumulado para construir iteracoes melhores de si mesmos. Os loops do repo melhoram harness/evals/docs; nao ha auto-iteracao do agente via substrato de dados.

**Evidence.**

- `docs/canonical/closed-loop-agent-operating-system.md:28-37` — quatro superficies do loop (state intake, priority synthesis, execution routing, feedback writeback); `:37` — "observe state, decide what should happen next, route execution, validate the outcome, and update the records that future agents will trust".
- `docs/canonical/shared-fleet-learning.md:37` — loop "one agent's error -> all agents' behavior" com canal de propagacao; `:62-63` — o elo fraco nomeado: o flywheel daemon "deploys nothing — it surfaces findings for human review" (captura sem deploy).
- `docs/canonical/production-failure-regression-flywheel.md:28` — toda falha de producao vira caso de regressao duravel (feedback como eval, nao como dados de auto-melhoria).
- `docs/system-of-record.md:229` — `garbage-collection-day-meta-loop.md`: meta-loop semanal de melhoria do harness; `:93` do doc canônico — "Converts human observations into accumulating harness leverage".
- `docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-analysis.md:53` — "aim the recursive self-improvement loop at the organization (harness + evals + agents absorbing each new model)" (o loop recursivo existe como tese organizacional, sem substrato de dados unificado).
- `docs/system-of-record.md:294` — `confidence-gated-continual-learning.md` (Sierra): aprendizado continuo gateado por confianca — o gate que tornaria auto-iteracao segura.

**NOT_FOUND (o que falta).** "All parts of the product are feeding into a single unified data foundation that agents can reason over" — o substrato unico (depende do gap do padrao 11); agentes construindo "better iterations of themselves" a partir do feedback acumulado (o alvo declarado e autorreferente; os loops do repo melhoram artefatos externos ao agente); um doc que una orchestration + execution + observation + feedback sobre o mesmo plano de dados. Busca: grep `self-iterat|self-improv|build better iterations|iterate on themselves` em `*.md` — apenas pacote-fonte e usos pontuais (`contextual-severity-calibration.md:106` descreve um loop de calibracao local, nao auto-iteracao de agente).

**Integration value: High.** E a arquitetura-alvo que unificaria closed-loop OS + fleet learning + flywheel sob um substrato de dados; o repo tem todos os elos menos a fundacao e a autorreferencia — e a sintese que a Phase de integracao poderia nomear como visao de longo prazo do repositorio.

---

---

## Tabela-sumário consolidada

| # | Pattern | Classification | Integration Value |
|---|---|---|---|
| 1 | Eval Coverage Matrix | Partial Coverage | High |
| 2 | Environment-Tiered Eval Fidelity | Partial Coverage | Medium |
| 3 | Production-to-Offline Feedback Loop with Drift Taxonomy | Partial Coverage | High |
| 4 | CLI-First Eval Harness with Remote Persistence | Partial Coverage | Medium |
| 5 | Plug-and-Play Harness with BYO Evaluators | Partial Coverage | Medium |
| 6 | Structured Partial Checks over Exact Goldens | Partial Coverage | Medium |
| 7 | Deterministic Multi-Turn Scripts over Simulated Users | Partial Coverage | Medium |
| 8 | Perceived-Eval | Missing | High |
| 9 | Unified Tool Surface Flywheel | Partial Coverage | High |
| 10 | Shadow Builds on Separated Compute | Partial Coverage | Medium |
| 11 | Agent-First Data Foundation | Partial Coverage | High |
| 12 | Skills and CLI as Native Agent Data Access | Partial Coverage | Medium |
| 13 | Eval-Gated Autonomy | Already Exists | Low |
| 14 | Observability-Threshold Eval Trigger | Partial Coverage | Medium |
| 15 | Bulk In-Context Trace Analysis | Partial Coverage | High |
| 16 | Self-Iterating Agent Loop | Partial Coverage | High |
