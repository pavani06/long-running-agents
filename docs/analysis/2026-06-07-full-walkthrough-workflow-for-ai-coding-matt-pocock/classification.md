---
title: "Classification: Matt Pocock AI Coding Workflow Patterns"
type: analysis
tags: ["agentes-orquestracao", "context-engineering", "evals", "governanca"]
date: 2026-06-07
aliases: ["matt pocock workflow classification", "full walkthrough pattern classification"]
relates-to: ["[[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/mental-model|Mental Model]]", "[[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/patterns|Patterns]]", "[[docs/system-of-record|System of Record]]", "[[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent Operating System]]", "[[docs/canonical/hybrid-context-stack|Hybrid Context Stack]]"]
sources: ["[[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/patterns|Patterns]]", "[[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/mental-model|Mental Model]]", "[[docs/system-of-record|System of Record]]"]
---
# Classification: Matt Pocock AI Coding Workflow Patterns
## Method
Classificacao feita contra o repositorio `long-running-agents` usando a precedencia: `docs/decisions/` > `docs/canonical/` > `docs/evidence/` > `docs/analysis/` > `curriculum/` > READMEs e operacionais. `docs/decisions/` esta vazio, entao a camada mais forte encontrada foi `docs/canonical/` ou `.opencode/skills/` quando o padrao e operacional. As buscas de `NOT_FOUND` citam os locais pesquisados e ignoram hits dentro deste proprio pacote de analise quando eles apenas repetem a fonte extraida.
## 1. Smart-Zone Context Management
**Classification:** Better Implementation
**Integration value:** Low
**Justification:** O padrao extraido combina disciplina de smart zone, thresholds de reset/delegacao e review em contexto fresco. O repositorio ja tem uma versao canonica mais madura: monitor de saude de tokens por fase, stack hibrida com ordem de inclusao e trace, handoff consciente de budget e preservacao de prompt estavel. A lacuna nao e conceitual; e apenas operacionalizacao continua em runtime.
**Evidence:**
- `docs/canonical/phase-gated-token-health-monitor.md:29 define monitor por turno/iteracao com remaining budget, burn-rate forecast, fase, acao deterministica e razao auditavel.`
- `docs/canonical/phase-gated-token-health-monitor.md:61-67 define fases green/yellow/orange/red com acoes continue, monitor, summarize/compress e new_session/handoff/force_terminate.`
- `docs/canonical/hybrid-context-stack.md:30-42 define uma stack budget-aware com camadas ordenadas, catalogo recuperavel e handoff antes de enfraquecer o harness.`
- `docs/canonical/budget-aware-session-handoff.md:57-64 define trigger, payload de fresh session, continuity message e reset de budget.`
- `docs/canonical/stable-harness-prompt.md:28-41 separa prompt estavel de payload reducivel e preserva o contrato do harness durante reducao de contexto.`
**Gap or integration note:** Nenhuma lacuna de padrao equivalente; o valor de integracao e cross-reference para docs canonicos existentes.
## 2. Grill-Me Alignment Interview
**Classification:** Partial Coverage
**Integration value:** High
**Justification:** O repositorio tem coautoria de documentos com perguntas de contexto e split-brain review para separar julgamento de engenharia e destino, mas nao ha um workflow de entrevista um-pergunta-por-vez com respostas recomendadas, ledger de decisoes e deferrals antes de PRD/issues.
**Evidence:**
- `.opencode/skills/doc-coauthoring/SKILL.md:20-23 define contexto, refinamento e reader testing para documentos.`
- `.opencode/skills/doc-coauthoring/SKILL.md:88-98 manda gerar 5-10 perguntas de clarificacao e sair quando as perguntas demonstrarem entendimento.`
- `docs/canonical/split-brain-planning-review.md:28-41 define revisores independentes de engenharia e produto/destino, com decisoes e ambicoes deferidas registradas.`
- Search NOT_FOUND in docs/, curriculum/, .opencode/, README.md, AGENTS.md for Grill-Me, alignment interview, one-question-at-a-time, recommended-answer, deferred decisions outside this analysis package: only docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/analysis.md:80 and patterns.md:37-67 matched the extracted source package.
**Gap or integration note:** Falta skill ou doc canonico para entrevista de alinhamento guiada, respostas recomendadas e ledger de decisoes/deferrals.
## 3. Shared Design Concept Handoff
**Classification:** Partial Coverage
**Integration value:** High
**Justification:** Ha mecanismos adjacentes para contexto inicial, brief de execucao e reconciliacao de reviewers, mas nao existe uma camada formal que declare a conversa de alinhamento como ativo principal e preserve o conceito compartilhado para PRD, issue generation e review.
**Evidence:**
- `.opencode/skills/doc-coauthoring/SKILL.md:28-42 coleta meta-contexto, audiencia, impacto, formato e constraints antes de redigir.`
- `.opencode/skills/issue-start/SKILL.md:111-147 cria execution brief com objetivo, success criteria, escopo, out-of-scope, estrategia e validacao.`
- `docs/canonical/split-brain-planning-review.md:35-41 exige reconciliar outputs, registrar discordancias, tradeoffs aceitos e ambicao deferida.`
- Search NOT_FOUND in docs/, curriculum/, .opencode/, README.md, AGENTS.md for shared design concept, design concept handoff, assumption summary, trust boundary: only this analysis package matched those exact mechanics.
**Gap or integration note:** Falta contrato de handoff do conceito compartilhado que conecte entrevista, PRD, issues e criterios de review.
## 4. Destination PRD
**Classification:** Partial Coverage
**Integration value:** Medium
**Justification:** O repositorio suporta PRDs/specs via doc-coauthoring e planos/briefs com objetivo, escopo, criterios e validacao, mas nao formaliza PRD como artefato navegacional temporario que aponta destino sem virar fonte permanente da verdade.
**Evidence:**
- `.opencode/skills/doc-coauthoring/SKILL.md:12-15 aciona o workflow para PRD, design doc, decision doc e RFC.`
- `.opencode/skills/writing-plans/SKILL.md:40-52 define header de plano com goal, architecture e tech stack.`
- `.opencode/skills/issue-start/SKILL.md:117-147 define brief com objective, success criteria, in/out of scope, strategy e validation plan.`
- `docs/system-of-record.md:14-21 estabelece precedencia documental, mas nao um ciclo de vida especifico para PRDs.`
- Search NOT_FOUND in docs/, curriculum/, .opencode/, README.md, AGENTS.md for Destination PRD, navigational PRD, PRD as destination outside this analysis package: only docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/analysis.md:56-60 and patterns.md:79-98 matched the full reframe.
**Gap or integration note:** Falta template/skill/canonico de PRD de destino com validade por fase e relacao explicita com issue generation.
## 5. Human/AFK Task Routing Gate
**Classification:** Partial Coverage
**Integration value:** High
**Justification:** O repositorio tem roteamento operacional por issues, worktrees, labels, blockers e sugestao de proxima tarefa, mas nao formaliza um gate que classifica explicitamente tarefas AFK-ready versus human-in-loop por ambiguidade, arquitetura, QA e julgamento de produto.
**Evidence:**
- `.opencode/skills/orchestrator/SKILL.md:51-63 define prioridade para sugerir proxima tarefa, pulando agent:working, blocked e blockers abertos.`
- `.opencode/skills/issue-start/SKILL.md:38-45 impede roubar trabalho ja claimado por agent:working ou assignee.`
- `docs/canonical/closed-loop-agent-operating-system.md:32-35 inclui priority synthesis, execution routing e feedback writeback.`
- `docs/canonical/split-brain-planning-review.md:37-41 reserva review extra para roadmaps de alto impacto, apostas ambiguas e grandes mudancas de agent-system.`
- Search NOT_FOUND in docs/, curriculum/, .opencode/, README.md, AGENTS.md for AFK-ready, human-in-loop task classifier, ambiguity detector outside this analysis package: only this analysis package matched the explicit Human/AFK routing reframe.
**Gap or integration note:** Falta matriz/skill de classificacao AFK vs humano com criterios de ambiguidade, feedback-loop readiness e module boundaries.
## 6. Vertical-Slice Issue Generation
**Classification:** Partial Coverage
**Integration value:** High
**Justification:** A skill refine-issue faz decomposicao com dependencias, sub-issues, acceptance criteria e verification gate, mas sua granularidade preferida e arquivo ou par de arquivos. Isso cobre rastreabilidade e bloqueios, mas perde a mecanica central de fatias verticais atravessando camadas para comportamento observavel.
**Evidence:**
- `.opencode/skills/refine-issue/SKILL.md:8-21 transforma uma issue em sub-issues focadas, com dependencias e execucao autonoma.`
- `.opencode/skills/refine-issue/SKILL.md:46-70 define sub-issues por arquivo/par, verify command, acceptance criteria, blocked by e enables.`
- `.opencode/skills/refine-issue/SKILL.md:80-86 exige Verification Gate final que valida todos os criterios antes do parent completar.`
- `.opencode/skills/issue-workflow/SKILL.md:59-82 cria sub-issues com acceptance criteria e bloco BLOCKED BY.`
- Search NOT_FOUND in docs/, curriculum/, .opencode/, README.md, AGENTS.md for vertical slice, behavior path, layer-spanning outside this analysis package: only this analysis package matched vertical-slice mechanics.
**Gap or integration note:** Falta orientar issue generation por caminhos de comportamento observavel cross-layer, nao apenas por arquivos e dependencias.
## 7. Agent Kanban
**Classification:** Partial Coverage
**Integration value:** Medium
**Justification:** Ha dashboard operacional, labels, blocked handling e um plano antigo com colunas Kanban, mas nao ha um Agent Kanban canonico com AFK/human labels, intake de QA, ready queue e semantica de ownership como camada de controle de concorrencia.
**Evidence:**
- `.opencode/skills/orchestrator/SKILL.md:27-49 define dashboard de issues, PRs, worktrees, status ready/active e tratamento de blocked.`
- `.opencode/skills/orchestrator/SKILL.md:55-63 define regra de sugestao de proxima issue nao bloqueada.`
- `.opencode/skills/orchestrator/SKILL.md:165-180 documenta blocker handling e retorno para fila.`
- `docs/plans/2026-05-26-curriculum-completion-strategy.md:367-374 define um GitHub Project Kanban com Backlog, In Progress, Review e Done.`
- Search NOT_FOUND in docs/, curriculum/, .opencode/, README.md, AGENTS.md for Agent Kanban, AFK/human labels, QA intake lane outside this analysis package: only this analysis package matched the full board semantics.
**Gap or integration note:** Falta canonico/skill que una board, labels AFK/human, blockers, ownership e intake de QA em um contrato.
## 8. Ralph/AFK Implementation Loop
**Classification:** Partial Coverage
**Integration value:** Medium
**Justification:** O repositorio possui lifecycle forte para uma issue, com setup, exploracao, brief, validacao, review, PR, merge aprovado e cleanup. Tambem registra Ralph Loop no glossario como tecnica anterior. O que falta e uma policy de loop AFK que carregue a proxima issue ready, implemente, valide, registre status e decida continuar ou parar.
**Evidence:**
- `.opencode/skills/issue-start/SKILL.md:12-15 define claim, branch/worktree isolado, leitura de contexto e brief antes da implementacao.`
- `.opencode/skills/issue-review/SKILL.md:44-77 exige gates reais de validacao e parar em falha antes do PR.`
- `.opencode/skills/issue-finish/SKILL.md:12-15 verifica PR, checks, approvals, merge, close issue, cleanup e release de agent:working.`
- `curriculum/GLOSSARY.md:356-370 define Ralph Loop como agente em loop incremental e registra status substituido por generator/evaluator.`
- Search NOT_FOUND in docs/, curriculum/, .opencode/, README.md, AGENTS.md for ready issue loader, continue-or-stop policy, AFK implementation loop outside this analysis package: only this analysis package matched the complete loop.
**Gap or integration note:** Falta policy operacional para continuar automaticamente entre ready issues e registrar outcomes por iteracao.
## 9. Feedback-Loop-Gated Implementation
**Classification:** Already Exists
**Integration value:** Low
**Justification:** O padrao ja esta documentado e operacionalizado em profundidade equivalente: sucesso precisa ser definido e verificado, planos separam plan/execute/verify, issue-review roda gates reais e PR-gated eval enforcement exige evidencias para superficies sensiveis.
**Evidence:**
- `AGENTS.md:30-32 exige definir sucesso e verificar com checks concretos.`
- `AGENTS.md:53-62 manda usar scripts reais de package.json como lint e test:unit conforme superficie.`
- `docs/canonical/plan-execute-verify.md:68-74 define fases Plan, Execute, Verify com gates antes de prosseguir.`
- `.opencode/skills/issue-review/SKILL.md:44-77 exige validacao, gates de package.json, falha bloqueante e resumo de evidencias para PR.`
- `docs/canonical/pr-gated-eval-enforcement.md:28-53 exige reports de eval, baseline/candidate, tiers, deltas, thresholds, failure examples e merge policy.`
**Gap or integration note:** Sem lacuna relevante para integracao; apenas cross-reference ao conjunto existente.
## 10. Fresh-Context Review
**Classification:** Already Exists
**Integration value:** Low
**Justification:** O repositorio ja exige review fora do contexto ruidoso do implementador: issue-review roda compact antes de CI/PR, coleta diff e contexto, delega second-agent review e para antes do merge. Isso cobre a separacao builder/evaluator do padrao.
**Evidence:**
- `.opencode/skills/issue-review/SKILL.md:38-40 exige /compact antes de CI e PR creation para entrar no review com contexto limpo focado no diff e validacao.`
- `.opencode/skills/issue-review/SKILL.md:155-164 coleta diff, diff stat, commits e issue body como contexto de review.`
- `.opencode/skills/issue-review/SKILL.md:166-188 delega second-agent review com escopo de correctness, tests, tenant isolation, crossroad policy, eval evidence e security.`
- `.opencode/skills/issue-review/SKILL.md:200-226 reporta findings e para antes do merge.`
- `docs/canonical/generator-evaluator.md:31-32 formaliza separar geracao e avaliacao em agentes distintos.`
**Gap or integration note:** Sem lacuna relevante para o padrao; o fluxo existente e equivalente.
## 11. Sandboxed Parallel Agents
**Classification:** Partial Coverage
**Integration value:** Medium
**Justification:** O repositorio cobre worktree e branch por issue, ownership por label e orquestracao de sessoes paralelas. A lacuna e isolamento runtime/container e uma politica canonica de integracao/conflito para agentes paralelos alem do fluxo de PR/merge.
**Evidence:**
- `AGENTS.md:36-41 recomenda branch main, worktrees para trabalho paralelo e agent:working para ownership.`
- `.opencode/skills/issue-start/SKILL.md:54-88 deriva branch/worktree, cria worktree a partir de origin/main e para se ja existir.`
- `.opencode/skills/orchestrator/SKILL.md:12-15 coordena sessoes paralelas de agentes em GitHub issues.`
- `.opencode/skills/orchestrator/SKILL.md:27-36 coleta issues, PRs, worktrees e labels para dashboard.`
- `.opencode/skills/issue-finish/SKILL.md:50-68 verifica merge readiness antes de merge.`
**Gap or integration note:** Falta isolamento de runtime/container e politica completa de integracao de branches paralelas apos conflito.
## 12. Sub-Agent Exploration Compression
**Classification:** Partial Coverage
**Integration value:** Medium
**Justification:** O repositorio usa delegacao para exploracao e pipelines multiagente, e docs canonicos permitem resumir/delegar bulk. Ainda nao existe um contrato especifico de sub-agent exploration compression com pergunta de exploracao, summary channel, output refs e obrigacao de verificacao pelo main agent.
**Evidence:**
- `.opencode/skills/refine-issue/SKILL.md:37-45 manda usar Explore agent ou busca direta para mapear arquivos, padroes, dependencias e testes.`
- `.opencode/skills/analyze-and-improve/SKILL.md:48-56 define pipeline em fases delegadas a sub-agentes especializados.`
- `docs/canonical/stable-harness-prompt.md:37-39 permite que tool/trace bulk seja resumido, externalizado ou delegado.`
- `docs/canonical/addressable-memory-catalog.md:75-81 diz que o catalogo funciona com sub-agent outputs e que sub-agents podem retornar output_ref compactos.`
- Search NOT_FOUND in docs/, curriculum/, .opencode/, README.md, AGENTS.md for Sub-Agent Exploration Compression, summary channel, condensed findings report outside this analysis package: only this analysis package matched the full contract.
**Gap or integration note:** Falta schema/skill para prompts de exploracao estreitos, achados condensados, output_ref e verificacao obrigatoria pelo agente principal.
## 13. Architecture-as-Agent-Affordance Refactoring
**Classification:** Partial Coverage
**Integration value:** High
**Justification:** O repositorio valoriza interfaces, boundaries, split-brain review e discovery de workflow, mas nao formaliza arquitetura como affordance para agentes: deep modules, interfaces simples, testes de fronteira e reducao de carga cognitiva para sessoes futuras.
**Evidence:**
- `.opencode/skills/writing-plans/SKILL.md:22-30 orienta mapear arquivos, responsabilidades, boundaries e interfaces antes de definir tarefas.`
- `docs/canonical/split-brain-planning-review.md:32-40 avalia escopo, dependencias, testes, risco e preserva tradeoffs aceitos.`
- `docs/canonical/domain-embedded-workflow-automation-wedge.md:41-48 separa integracao deterministica de julgamento do modelo e escolhe slices com evidencia before/after.`
- `AGENTS.md:86-90 exige seguir padroes existentes e manter scripts/funcoes pequenos, explicitos e testaveis.`
- Search NOT_FOUND in docs/, curriculum/, .opencode/, README.md, AGENTS.md for Architecture-as-Agent-Affordance, deep module, agent affordance outside this analysis package: only docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/analysis.md:68-72 and patterns.md:268-291 matched the full reframe.
**Gap or integration note:** Falta canonico/refactoring skill para dependency clusters, deep module boundaries, public interfaces simples e boundary tests como affordances de agente.
## 14. Phase-Scoped Documentation Hygiene
**Classification:** Partial Coverage
**Integration value:** Medium
**Justification:** O repositorio tem precedencia documental, Obsidian conventions, archive como camada historica e lifecycle de harness com archive reversivel. A lacuna e aplicar isso a PRDs/planos/issues por fase, marcando ou arquivando artefatos de planejamento stale depois da implementacao para nao contaminar retrieval.
**Evidence:**
- `docs/system-of-record.md:14-21 define precedencia entre ADRs, canonicos, evidencias, analises, archive e READMEs.`
- `AGENTS.md:120-147 exige frontmatter Obsidian e campos obrigatorios para docs de analise/canonicos.`
- `AGENTS.md:223-238 exige relates-to para evitar documentos ilhados.`
- `docs/canonical/measured-harness-evolution-lifecycle.md:50-62 define REMOVE com archive, README, ADR, metricas, validacao e reativacao.`
- `docs/canonical/epistemic-memory-graph.md:36-49 inclui epistemic_status, last_verified e labels para distinguir stale memory antes de agir.`
- Search NOT_FOUND in docs/, curriculum/, .opencode/, README.md, AGENTS.md for phase-scoped documentation hygiene, stale PRDs, retrieval hygiene outside this analysis package: only this analysis package matched the PRD/plan lifecycle pattern.
**Gap or integration note:** Falta politica de lifecycle para PRDs e planos: ativo, concluido, stale, arquivado/removido e status explicito para retrieval.
## 15. QA-to-Backlog Feedback Loop
**Classification:** Partial Coverage
**Integration value:** High
**Justification:** O repositorio tem flywheel de falhas de producao para evals, issue-workflow para comentarios/blockers e closed-loop OS para writeback. Falta formalizar QA e review findings como entrada de backlog/vertical slices, com severidade, prioridade, blockers e regression checks.
**Evidence:**
- `docs/canonical/production-failure-regression-flywheel.md:28-40 transforma falhas de producao em casos duraveis de regressao com trace, labels, tier e link para incident/PR.`
- `docs/canonical/closed-loop-agent-operating-system.md:32-35 inclui feedback writeback como superficie do OS.`
- `docs/canonical/closed-loop-agent-operating-system.md:43-45 exige ownership, validacao e memory update antes de writeback autoritativo.`
- `.opencode/skills/issue-workflow/SKILL.md:18-25 manda atualizar acceptance criteria, comentar progresso/decisoes/blockers e postar handoff.`
- `.opencode/skills/orchestrator/SKILL.md:165-180 trata blockers e comenta intervencao manual.`
- Search NOT_FOUND in docs/, curriculum/, .opencode/, README.md, AGENTS.md for QA-to-Backlog, QA intake lane, QA findings backlog outside this analysis package: only this analysis package matched the exact loop.
**Gap or integration note:** Falta intake de QA/review findings para issue generation, triagem de severidade e regressao associada no Kanban.
## Summary Table
| # | Pattern | Classification | Integration value |
|---|---|---|---|
| 1 | Smart-Zone Context Management | Better Implementation | Low |
| 2 | Grill-Me Alignment Interview | Partial Coverage | High |
| 3 | Shared Design Concept Handoff | Partial Coverage | High |
| 4 | Destination PRD | Partial Coverage | Medium |
| 5 | Human/AFK Task Routing Gate | Partial Coverage | High |
| 6 | Vertical-Slice Issue Generation | Partial Coverage | High |
| 7 | Agent Kanban | Partial Coverage | Medium |
| 8 | Ralph/AFK Implementation Loop | Partial Coverage | Medium |
| 9 | Feedback-Loop-Gated Implementation | Already Exists | Low |
| 10 | Fresh-Context Review | Already Exists | Low |
| 11 | Sandboxed Parallel Agents | Partial Coverage | Medium |
| 12 | Sub-Agent Exploration Compression | Partial Coverage | Medium |
| 13 | Architecture-as-Agent-Affordance Refactoring | Partial Coverage | High |
| 14 | Phase-Scoped Documentation Hygiene | Partial Coverage | Medium |
| 15 | QA-to-Backlog Feedback Loop | Partial Coverage | High |

## Classification Counts
- Better Implementation: 1
- Already Exists: 2
- Partial Coverage: 12
- Missing: 0
