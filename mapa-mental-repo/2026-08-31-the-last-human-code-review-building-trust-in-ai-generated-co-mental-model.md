---
title: "Mental Model: The Last Human Code Review — Building Trust in AI-Generated Code (Repository Incremental Update)"
type: analysis
tags: ["governanca", "harness-engineering"]
date: 2026-08-31
aliases: ["mental model last human code review", "modelo mental incremental 2026-08-31", "phase 0 mental model 2026-08-31"]
relates-to: ["[[docs/plans/2026-08-31-skill-hardening-adversarial-findings|Skill Hardening Plan]]", "[[docs/system-of-record|System of Record]]", "[[mapa-mental-repo/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-mental-model|Modelo base GTM 2026-08-30]]"]
---

# Mental Model — long-running-agents (atualização incremental, 2026-08-31)

Escopo: repositório apenas. A fonte externa NÃO foi analisada neste passo (Phase 0 modela o repositório; a fonte é tratada por agente separado).

- **Base:** [[mapa-mental-repo/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-mental-model|modelo GTM de 2026-08-30]] (full rebuild, mtime 21:14:47)
- **Modo:** incremental (dias desde a base = 1; relevância temática = MEDIA; deltas = 3)
- **Delta report:** [[docs/analysis/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co/delta-report|delta-report.md]] (3 deltas)

## Changelog incremental

Decisões tomadas por delta (NEW ENTRY / UPDATE / NO CHANGE):

| # | Delta | Decisão | O que mudou |
|---|---|---|---|
| 1 | `.opencode/skills/analyze-and-improve/SKILL.md` (commit `f19cb1d`, +11 linhas) | UPDATE | Abstração "Pipeline de análise" e pattern "Pipeline analyze-and-improve" agora registram a regra **no-fabricated-premises** (`SKILL.md:130-138`, anti-pattern em `:1125`): delegação nunca afirma convenções como fato; sub-agente detecta lendo 2-3 artefatos irmãos. Novo termo na terminologia. |
| 2 | `.opencode/skills/harness-analyze-and-improve/SKILL.md` (commit `f19cb1d`, +12/-10) | UPDATE | Abstração "Runtime do harness" e pattern do pipeline agora registram o gate de avaliação **estrutural + semântico proporcional ao risco** (`SKILL.md:206-219`): citation sampling, executable content (python3 + compile), source fidelity (Phase 1), com `verification_depth: structural|semantic` por fase (`templates/test-results.json:14`). Novo termo `verification_depth`. |
| 3 | [[docs/plans/2026-08-31-skill-hardening-adversarial-findings|docs/plans/2026-08-31-skill-hardening-adversarial-findings.md]] (novo-plano, 169 linhas) | NEW ENTRY | Plano de execução das 8 correções da análise adversarial de 2026-08-30, executado via qi-epic (epic #157, issues #158-#167) com re-verificação 8/8 PASS (`:175-179`). Entrou como relationship (ciclo de hardening qi-loop) e alimentou os gaps novos. |

### Drift extra descoberto no Passo 0b

O scan de deltas do Passo 0a usa `find -newer` sobre o mtime do yaml base (21:14:47). O output Phase 4 do **próprio run GTM** foi commitado às 21:13:27 (`5292e11`) — segundos antes da cópia da base — e não apareceu no delta report. Este modelo incorpora esse drift:

- **12 canonical docs novos** (GTM, 2026-08-30): `agent-value-maturity-ladder`, `centralized-data-plane-inherited-rbac`, `continuous-re-architecture-budget`, `gap-to-content-feedback-circuit`, `human-review-staged-workflow-automation`, `llm-classified-log-taxonomy`, `owner-led-activation-blitz`, `pull-based-infrastructure-on-pain`, `quality-over-coverage-trust-scoping`, `retention-gated-phased-rollout`, `trial-retention-attribution-split`, `workflow-derived-golden-question-set` (commit `5292e11`; SOR atualizado para 154 em `docs/system-of-record.md:171`).
- **2 skills novas**: `agent-value-maturity-ladder` e `trial-retention-attribution-split` (listadas em `docs/system-of-record.md:66-67`).
- **2 exercises novos**: `exercise-09-trial-retention-attribution-split.md` e `exercise-10-agent-value-maturity-ladder.md` em `curriculum/03-nivel-3-advanced-architecture/exercises/`.
- **9 enriquecimentos de currículo**, incluindo `05-core-concepts/06-harness-evolution.md` (+93) e `05-core-concepts/08-evaluation-rubrics.md` (+150).
- Consequência: citações a linhas do SOR e do `curriculum/README.md` nas entradas alteradas foram re-verificadas e atualizadas.

### Gaps fechados vs mantidos

Nenhuma das 15 gaps da base foi fechada por `f19cb1d`: as 8 falhas da análise adversarial nunca estiveram na lista de gaps da base (posterior a ela) e todas as 8 foram fechadas com 8/8 PASS ([[docs/plans/2026-08-31-skill-hardening-adversarial-findings|plano]], `:175-179`) — portanto não entram como gaps abertas. Três gaps novas foram adicionadas (ver seção Gaps).

---

## Goals

1. Base de conhecimento e currículo para agentes long-running confiáveis: sistemas de IA que operam por horas ou dias sem perder contexto, planejamento ou julgamento de qualidade (README.md:12).
2. Ensinar e operacionalizar harness engineering: degradação de agentes longos é lacuna de engenharia, não limitação de modelo; harness é a infraestrutura de suporte ao redor do modelo (README.md:16-18).
3. Atacar três falhas estruturais: perda de contexto, planejamento frágil, autoavaliação cega (README.md:24-30).
4. Entregar currículo de 12 semanas como produto principal: 4 níveis, 8 conceitos core, 35+ diagramas, ancorado no caso real KODA — agente de venda de suplementos via WhatsApp, conversas de 2+ horas (curriculum/README.md:13; docs/system-of-record.md:71-72).
5. Rodar pipeline automatizado de análise de conhecimento externo: harness analyze-and-improve em 7 fases com evaluators e gates, convertendo fontes externas em canonical docs, skills e exercícios (README.md:102, :136).
6. Servir de template de sistema de agentes reutilizável: `.opencode/` com Handoff Protocol, skills e agentes adaptáveis a outros projetos (README.md:140).
7. Governar documentação por precedência: ADRs > canonical > evidence > analysis > archive > READMEs via system of record (docs/system-of-record.md:14-21).
8. Disciplina operacional de agentes: uma tarefa por sessão, não assumir, mudança mínima, sucesso verificável, issues/branches traceáveis, gates reais (AGENTS.md:14-16, :26-32, :42-48, :69-78).
9. Audiência: pessoas de negócio com skill em construção de agentes, de iniciantes a operadores de produção (README.md:34).

*(carregados inalterados da base — os deltas não alteram goals)*

## Architecture

### Abstractions

| Abstração | Role | Evidência |
|---|---|---|
| System of Record | Mapa das fontes canônicas; resolve conflitos por precedência; define os 6 domínios do projeto | docs/system-of-record.md:12, :14-21, :23 |
| Biblioteca de padrões canônicos **[UPDATE]** | Camada autoritativa de padrões agentic ativos; **154 arquivos .md** em `docs/canonical/` (inclui cluster Kavak e **pacote GTM 2026-08-30 — 12 docs via commit 5292e11**); cada padrão documenta problema/mecanismo/trade-offs. Base declarava 142 — o próprio run GTM adicionou 12 docs após o snapshot da Phase 0 | docs/system-of-record.md:171; directory listing 2026-08-31 (154 .md); commit 5292e11 |
| Currículo | Produto principal: 12 semanas, 4 níveis, 8 conceitos core, master docs e diretórios 01-10 | docs/system-of-record.md:71-97 |
| Sistema de agentes .opencode/ (HoP) | Modelo HoP (House of Pace) / Handoff Protocol: escopo fechado, dono e gates de validação por agente | docs/system-of-record.md:27; AGENTS.md:9 |
| Agentes HoP (3) | hop-orchestrator-rezek, koda-hop-init-basic, hop-live-whatsapp-tester | README.md:103; .opencode/agents/hop-orchestrator-rezek.md:21-39; .opencode/agents/koda-hop-init-basic.md:16-26; .opencode/agents/hop-live-whatsapp-tester.md:20, :35-59 |
| Camada de skills **[UPDATE]** | **35 diretórios** em `.opencode/skills/` (issue lifecycle, orquestração, docs, planos, error hygiene, shadow review, token budget, constraint gates, intent decomposition, analyze-and-improve, mega-expert-consolidation, sidekick-pattern-physical-boundaries, **agent-value-maturity-ladder, trial-retention-attribution-split**, etc.). Base declarava 33; pacote GTM (commit 5292e11) adicionou as 2 novas | docs/system-of-record.md:66-67; directory listing 2026-08-31 (35); commit 5292e11 |
| Pipeline de análise (analyze-and-improve) **[UPDATE f19cb1d]** | Conhecimento → mental model → extração → padrões → classificação → integração; 8 módulos stdlib com cache, retry, model tiering, schemas, chunking, trajectory, eval, refinement. Phase 0 opera em modo full ou incremental (Passos 0-pre/0a/0b/0c, cache datado em `mapa-mental-repo/`) e as delegações seguem a regra **no-fabricated-premises**: o prompt nunca afirma convenções do repo como fato — o sub-agente detecta a convenção dominante lendo 2-3 artefatos irmãos; conflito com instrução do operador → para e reporta antes de escrever | docs/system-of-record.md:46; README.md:102; .opencode/skills/analyze-and-improve/SKILL.md:21, :130-138 |
| Runtime do harness **[UPDATE f19cb1d]** | `harness/` com GUIDE-analyze-and-improve.md, harness-analysis.sh, templates/, test-results.json. O gate de avaliação (Step 6) passou de estrutural para **estrutural + semântico proporcional ao risco**: citation sampling (3 citações file:line conferidas; qualquer erro = NEEDS_WORK), executable content (blocos compilados via python3+compile antes de PASS), source fidelity (Phase 1: 3 claims contra a fonte); profundidade registrada por fase como `verification_depth: structural|semantic` (ausência = structural, retrocompatível) | harness/ directory listing 2026-08-30; .opencode/skills/harness-analyze-and-improve/SKILL.md:206-219; .opencode/skills/analyze-and-improve/harness/templates/test-results.json:14 |
| Domínio aplicado KODA | Product discovery, order processing, fulfillment, journeys, rubrics; conversas de 2+ horas via WhatsApp | curriculum/README.md:34; README.md:20 |
| Stack e tooling | Node >= 20.18.0 ESM, ESLint 10 + 2 regras customizadas, OpenCode, Obsidian (wikilinks/dataview), CLI obsidian-eval, portais HTML estáticos com Mermaid | README.md:153-161; docs/system-of-record.md:113-128 |
| Estado de runtime | `.runtime/` e `artifacts/` guardam estado de execução; modificação casual proibida (Rule 15) | AGENTS.md:11, :132-134 |
| Governança GitHub | PR template com checklist de crossroad files, CODEOWNERS, issue templates, dependabot, script de issues do currículo | docs/system-of-record.md:130-142 |
| Mapas mentais de fontes | `mapa-mental-repo/` guarda mental models dos pipelines (5 ativos em 2026-08-30, incluindo kavak) | mapa-mental-repo/ directory listing 2026-08-30 |

### Relationships

Carregadas da base (10, inalteradas): AGENTS.md × System of Record (AGENTS.md:80-91); currículo aponta para `docs/canonical/` (curriculum/README.md:351-358); pipeline transforma fontes em artefatos (README.md:136; docs/system-of-record.md:408-415); ADR Skill-Canons Bridge (docs/decisions/2026-06-24-skill-canons-bridge-implementation.md:35-43); canonical docs referenciam pacote de origem (docs/canonical/evals-as-brakes.md:20-23); Generator/Evaluator × cluster de evals (docs/system-of-record.md:210-216); trace instrumentation × telemetria Sisyphus (docs/system-of-record.md:125-128); currículo converge para N4 KODA (curriculum/README.md:246-259); glossário referencia canonicals via wikilink (curriculum/GLOSSARY.md:37, :102, :118, :134); handoff koda-hop-init-basic → hop-live-whatsapp-tester (.opencode/agents/koda-hop-init-basic.md:50; .opencode/agents/hop-live-whatsapp-tester.md:56-57).

Novas (2):

- **Ciclo de hardening qi-loop [NOVO]:** análise adversarial da sessão de 2026-08-30 → plano em `docs/plans/` com tarefas verificáveis por grep/py_compile/validator → commits separados por repo (`f19cb1d` em long-running-agents; `1c927a4` em Raw-Knowledge) → re-verificação 8/8 PASS com carimbo de execução. ([[docs/plans/2026-08-31-skill-hardening-adversarial-findings|plano]]:12, :149-151, :175-179)
- **Gate de avaliação × validador Obsidian [NOVO]:** o Step 6 do orquestrador integra `npx tsx scripts/validate-obsidian.ts` como check estrutural e o sampling de citações/compilação de código como check semântico; conflito entre instrução do operador e convenção detectada suspende o sub-agente. (.opencode/skills/harness-analyze-and-improve/SKILL.md:210-218; .opencode/skills/analyze-and-improve/SKILL.md:134-138)

## Patterns

62 padrões canônicos carregados inalterados da base (12-Factor, context, evals, planning, Kavak cluster, Sierra cluster — ver YAML espelho para a lista completa com `where_defined` e `maturity`).

**Novos — pacote GTM 2026-08-30 (commit 5292e11), não capturado pelo scan de mtime da base [NOVO 2026-08-31]:**

| Pattern | where_defined | maturity |
|---|---|---|
| Agent Value Maturity Ladder | docs/canonical/agent-value-maturity-ladder.md (SOR :327) + skill + exercise-10 | active-canonical + skill + exercise (GTM) |
| Trial-Retention Attribution Split | docs/canonical/trial-retention-attribution-split.md (SOR :325) + skill + exercise-09 | active-canonical + skill + exercise (GTM) |
| Centralized Data Plane with Inherited RBAC | docs/canonical/centralized-data-plane-inherited-rbac.md | active-canonical (GTM) |
| Continuous Re-Architecture Budget | docs/canonical/continuous-re-architecture-budget.md | active-canonical (GTM) |
| Gap-to-Content Feedback Circuit | docs/canonical/gap-to-content-feedback-circuit.md | active-canonical (GTM) |
| Human-Review Staged Workflow Automation | docs/canonical/human-review-staged-workflow-automation.md | active-canonical (GTM) |
| LLM-Classified Log Taxonomy | docs/canonical/llm-classified-log-taxonomy.md | active-canonical (GTM) |
| Owner-Led Activation Blitz | docs/canonical/owner-led-activation-blitz.md | active-canonical (GTM) |
| Pull-Based Infrastructure on Pain | docs/canonical/pull-based-infrastructure-on-pain.md | active-canonical (GTM) |
| Quality-Over-Coverage Trust Scoping | docs/canonical/quality-over-coverage-trust-scoping.md | active-canonical (GTM) |
| Retention-Gated Phased Rollout | docs/canonical/retention-gated-phased-rollout.md | active-canonical (GTM) |
| Workflow-Derived Golden Question Set | docs/canonical/workflow-derived-golden-question-set.md | active-canonical (GTM) |

**Atualizado [UPDATE f19cb1d]:**

- **Pipeline analyze-and-improve** (operational-pipeline) — 7 fases, cache Phases 1+2, pacote analysis/patterns/classification/mental-model/artifacts; modo incremental com Passos 0a-0c e cache `mapa-mental-repo/`; **avaliação estrutural + semântica com `verification_depth`; delegações sem premissas fabricadas**. (.opencode/skills/analyze-and-improve/SKILL.md:49-57, :130-138, :296-421 + .opencode/skills/harness-analyze-and-improve/SKILL.md:206-219, commit f19cb1d)

Conventions/skills carregadas inalteradas: issue lifecycle (.opencode/skills/issue-*), karpathy-guidelines, Obsidian document conventions (AGENTS.md Rule 16 + scripts/validate-obsidian.ts), commit/PR style (Rule 6), Skill-Canons Bridge (ADR aceito).

## Terminology

22 termos carregados inalterados da base (ver YAML espelho). Novos:

| Term | Definition | Source |
|---|---|---|
| **verification_depth** [NOVO] | Campo por fase em `harness/test-results.json` (structural\|semantic) que registra a profundidade da avaliação do orquestrador; PASS puramente estrutural não é mais suficiente — verificação semântica proporcional ao risco do artefato. Ausência = structural (retrocompatível). Commit f19cb1d. | .opencode/skills/harness-analyze-and-improve/SKILL.md:214-219; .opencode/skills/analyze-and-improve/harness/templates/test-results.json:14 |
| **No fabricated premises (regra de delegação)** [NOVO] | Prompt de delegação nunca afirma convenções do repo (idioma, estilo, formato, contagens, inventário) como fato; o sub-agente detecta a convenção dominante lendo 2-3 artefatos irmãos e reporta; conflito com instrução do operador → para e reporta antes de escrever. Commit f19cb1d. | .opencode/skills/analyze-and-improve/SKILL.md:130-138, :1125 |

## Curriculum

Estrutura de níveis e conceitos carregada inalterada da base (4 níveis; 8 conceitos core, todos ⏳ — tabela agora em curriculum/README.md:275-282).

**Nota atualizada [UPDATE 2026-08-31]:** conceitos 06 (harness-evolution, +93 linhas) e 08 (evaluation-rubrics, +150 linhas) foram re-enriquecidos pelo pacote GTM 2026-08-30 (commit 5292e11), além do enriquecimento kavak prévio (commits 2e38fea/dfb67d8). Exercises novos do pacote GTM em `curriculum/03-nivel-3-advanced-architecture/exercises/`: `exercise-09-trial-retention-attribution-split.md` (992 linhas) e `exercise-10-agent-value-maturity-ladder.md` (887 linhas).

## Gaps

**Removidas: nenhuma.** As 8 falhas da análise adversarial nunca constavam na lista da base e foram todas fechadas (8/8 PASS — [[docs/plans/2026-08-31-skill-hardening-adversarial-findings|plano]]:175-179).

**Carregadas da base (15; citações de SOR/README re-verificadas onde o pacote GTM deslocou linhas):**

1. `docs/canonical/agent-lifecycle.md` pendente — docs/system-of-record.md:70 (era :68)
2. `docs/canonical/curriculum-model.md` pendente — docs/system-of-record.md:99 (era :97)
3. `docs/canonical/portal-architecture.md` pendente — docs/system-of-record.md:112 (era :110)
4. `crossroad-change-policy.md` + `src/lib/*` inexistentes — docs/system-of-record.md:144 (era :142)
5. Tabela de canonical docs pendentes — docs/system-of-record.md:70, :99, :112, :144, :334
6. ADRs candidatos não formalizados — docs/system-of-record.md:165-167 (bullets finais)
7. Ações pendentes do ADR Skill-Canons Bridge — docs/decisions/2026-06-24-skill-canons-bridge-implementation.md:91-93 (inalterada)
8. FAQ do currículo em construção — curriculum/README.md:69, :491 (era :489)
9. 8 conceitos core ⏳ — curriculum/README.md:275-282 (era :271-280)
10. Drift de contagem de canonical docs **[atualizada]**: SOR agora declara 154 e o diretório tem 154 .md; README segue 85+ — docs/system-of-record.md:171 vs README.md:67 vs listing 2026-08-31 (base registrava SOR ~116 vs diretório 142)
11. Drift de contagem de skills **[atualizada]**: README declara 28; diretório tem 35 entradas (SOR já lista as 2 novas do GTM) — README.md:104 vs docs/system-of-record.md:66-67 vs listing 2026-08-31 (base registrava 33)
12. Skill devils-advocate no SOR mas ausente do diretório — docs/system-of-record.md:63 vs listing (reconfirmado 2026-08-31)
13. Nomenclatura de níveis inconsistente — docs/system-of-record.md:84-90 (era :82-88)
14. `curso-reimplementar-runtime/` (PR #144) não mapeado no SOR — listing vs docs/system-of-record.md:23-151 (inalterada)
15. `operator-channel-authority.md` e `structural-guarantee-over-compliance.md` fora da tabela de padrões ativos — listing 2026-08-31; grep sem resultado no SOR (reconfirmado)

**Novas [2026-08-31]:**

16. `task-wrapper.sh` ausente — trace instrumentation do qi-epic de hardening pulada (desvio documentado). ([[docs/plans/2026-08-31-skill-hardening-adversarial-findings|plano]]:179)
17. `validate-obsidian.ts` com 16 erros pré-existentes de pacotes antigos, tolerados como conhecidos. ([[docs/plans/2026-08-31-skill-hardening-adversarial-findings|plano]]:143)
18. Scan de deltas do Passo 0a por mtime (`find -newer`) perde artefatos gravados segundos antes da cópia do modelo base: o pacote GTM (commit `5292e11`, 21:13) não apareceu no delta report porque o yaml base tem mtime 21:14:47. ([[docs/analysis/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co/delta-report|delta-report]]:40-48 vs `git show 5292e11`)

---

*Espelho tipado: `2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co-mental-model.yaml` (mesmo diretório). Toda afirmação carrega referência file:line verificada por leitura direta em 2026-08-31; entradas inalteradas da base mantêm as citações originais.*
