---
title: "Mental Model: The Prompting Playbook"
type: analysis
tags: ["agentes-orquestracao", "curriculo-conteudo", "harness-engineering", "governanca", "context-engineering", "evals"]
date: 2026-09-02
aliases: ["prompting playbook mental model", "repo mental model 2026-09-02", "long-running-agents mental model"]
last_updated: 2026-09-02
relates-to: ["[[docs/system-of-record|System of Record]]", "[[README|Repository README]]", "[[curriculum/README|Curriculum README]]", "[[curriculum/GLOSSARY|Glossary]]", "[[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]", "[[docs/canonical/generator-evaluator|Generator-Evaluator]]", "[[AGENTS|Agent Rules]]"]
sources: ["[[AGENTS|AGENTS]]", "[[README|README]]", "[[docs/system-of-record|System of Record]]", "[[curriculum/README|Curriculum README]]", "[[curriculum/MASTER_PLAN|Master Plan]]", "[[curriculum/GLOSSARY|Glossary]]", "[[docs/decisions/2026-06-24-skill-canons-bridge-implementation|Skill-Canons Bridge ADR]]", "[[docs/decisions/2026-09-01-vault-federation-consultable-registry|Vault Federation ADR]]", "[[.opencode/skills/analyze-and-improve/SKILL|analyze-and-improve SKILL]]"]
---

# Mental Model: long-running-agents

**Date:** 2026-09-02
**Repo:** `long-running-agents`
**Type:** `mental-model`
**Base commit:** `2b56b98` (branch `main`)
**Scope:** repository-only reading. This artifact does not analyze the external source document; it models the repository as it exists at the base commit.

## 1. Project Goals

- Ser base de conhecimento e programa curricular para construir sistemas de IA que operam de forma confiável por horas, dias ou pelo tempo que a tarefa exigir, sem perder contexto, capacidade de planejamento ou julgamento de qualidade (`README.md:12`).
- Atacar as três falhas estruturais de agentes long-running — perda de contexto, planejamento frágil e autoavaliação cega — através de **harness engineering**: a disciplina de construir a infraestrutura de suporte que envolve o modelo, em vez de prompts melhores ou modelos maiores (`README.md:24`, `README.md:26`, `README.md:28`, `README.md:30`).
- Entregar o produto principal: um currículo completo de 12 semanas, 4 níveis de profundidade, 8 conceitos core e 35+ diagramas, ancorado no caso real KODA, agente de venda de suplementos via WhatsApp (`curriculum/README.md:13`, `curriculum/README.md:34`, `docs/system-of-record.md:83`).
- Manter uma biblioteca canônica de padrões de arquitetura agentica — 185 padrões ativos segundo o system of record — cada um documentando problema, mecanismo de solução e trade-offs (`docs/system-of-record.md:181`, `README.md:67`).
- Operar como um sistema, não só conhecimento: pipeline `analyze-and-improve` em `harness/` com 7 fases, 3 agentes em `.opencode/agents/`, 36 skills em `.opencode/skills/` e dashboards Obsidian (`README.md:102`, `README.md:103`, `README.md:104`, `.opencode/skills/analyze-and-improve/SKILL.md:49`).
- Servir pessoas de negócio com skill em construção de agentes, de iniciantes a operadores de produção (`README.md:34`).
- Governação documental estrita: precedência ADRs > canonical > evidence > analysis > archive > READMEs, com conflitos resolvidos pelo system of record (`docs/system-of-record.md:14`-`docs/system-of-record.md:21`, `AGENTS.md:82`-`AGENTS.md:91`).

## 2. Architecture

### Core Abstractions

| Abstraction | Role | Evidence |
|---|---|---|
| System of record | Fonte da verdade: resolve conflitos entre documentos via cadeia de precedência e mapeia os domínios do projeto. | `docs/system-of-record.md:12`, `docs/system-of-record.md:14`-`docs/system-of-record.md:21` |
| Domínios do projeto | Seis domínios mapeados: Agentes e orquestração, Currículo e conteúdo, Portal web, Stack e tooling, Governança de repositório, Testes e QA — cada um com tabela de fontes autoritativas. | `docs/system-of-record.md:23`-`docs/system-of-record.md:29`, `docs/system-of-record.md:83`, `docs/system-of-record.md:110`, `docs/system-of-record.md:123`, `docs/system-of-record.md:141`, `docs/system-of-record.md:155` |
| Biblioteca canônica de padrões | `docs/canonical/` com 185 padrões ativos (186 arquivos `.md` no disco), cobrindo context engineering, evals, harness design, multi-agent coordination, token economics, orquestração por eventos e governança. | `docs/system-of-record.md:179`-`docs/system-of-record.md:181`, `docs/system-of-record.md:183`-`docs/system-of-record.md:368` |
| Currículo | Produto principal: programa de 12 semanas em 4 níveis + 8 conceitos core + knowledge graphs + guias + templates + case studies + referências. | `docs/system-of-record.md:83`, `docs/system-of-record.md:87`-`docs/system-of-record.md:104`, `curriculum/README.md:13` |
| Sistema de agentes `.opencode` | Modelo HoP (Handoff Protocol): 3 agentes com escopo fechado, dono e gates de validação. Rezek orquestra (primário, governança/coordenação); KODA Init Basic conduz inicialização guiada (subagente, sem write/edit/bash); Live WhatsApp Tester projeta e roda testes live do KODA (subagente). | `docs/system-of-record.md:27`, `.opencode/agents/hop-orchestrator-rezek.md:21`, `.opencode/agents/koda-hop-init-basic.md:16`, `.opencode/agents/koda-hop-init-basic.md:2`-`.opencode/agents/koda-hop-init-basic.md:8`, `.opencode/agents/hop-live-whatsapp-tester.md:16`-`.opencode/agents/hop-live-whatsapp-tester.md:20` |
| Skills (36) | Workflow executável: lifecycle de issues (issue-start/review/finish/workflow), orquestração, documentação, planos, error hygiene, shadow review, token budget, constraint gates, intent decomposition, implementação de padrões canônicos. | `.opencode/skills/` (36 diretórios com SKILL.md), `README.md:104`, `docs/system-of-record.md:36`-`docs/system-of-record.md:68` |
| Harness `analyze-and-improve` | Pipeline de 7 fases (0: mental model; 1: extração; 2: padrões; 3: classificação; 4: melhorias; 5: integração; 6: integração curricular default), com cache, retry, model tiering, schemas, chunking, trajectory, eval e refinement; executável via skill harness ou `harness/harness-analysis.sh`. | `.opencode/skills/analyze-and-improve/SKILL.md:49`-`.opencode/skills/analyze-and-improve/SKILL.md:57`, `.opencode/skills/analyze-and-improve/SKILL.md:92`-`.opencode/skills/analyze-and-improve/SKILL.md:103`, `docs/system-of-record.md:46` |
| Domínio caso KODA | Caso real aplicado: venda de suplementos via WhatsApp com descoberta de produtos, processamento de pedidos, fulfillment e entrega no mesmo dia; conversas de 2+ horas como constraint de confiabilidade. | `curriculum/GLOSSARY.md:544`-`curriculum/GLOSSARY.md:553`, `curriculum/README.md:34` |
| ADRs | Decisões arquiteturais formalizadas e aceitas: Skill-Canons Bridge (5 decisões cross-cutting sobre bridging skills↔canons) e Vault Federation (registro consultável multi-vault + roteamento por domínio). | `docs/system-of-record.md:169`-`docs/system-of-record.md:171`, `docs/decisions/2026-06-24-skill-canons-bridge-implementation.md:35`-`docs/decisions/2026-06-24-skill-canons-bridge-implementation.md:42`, `docs/decisions/2026-09-01-vault-federation-consultable-registry.md:35`-`docs/decisions/2026-09-01-vault-federation-consultable-registry.md:41` |
| Gestão de conhecimento Obsidian | Wikilinks `[[path|display]]` para toda referência interna, frontmatter obrigatória com `type`/`tags`/`aliases`/`relates-to`, tags derivadas dos domínios do SOR, slugs lowercase com hífens, validação por `scripts/validate-obsidian.ts` (hard error em CI para `relates-to` ausente). | `AGENTS.md:136`-`AGENTS.md:257`, `README.md:158`, `README.md:161` |
| Stack e tooling | Node >= 20.18.0 ESM, ESLint 10 + plugin-n + unicorn + 2 regras customizadas (`no-catch-message`, `no-raw-console-in-scripts`), scripts npm `lint`/`test:unit`/`test:integration`/`validate:obsidian`, OpenCode + MCP context7, `obsidian-eval` para navegação entre vaults. | `package.json:5`-`package.json:14`, `README.md:155`-`README.md:161`, `docs/system-of-record.md:127`-`docs/system-of-record.md:135` |

### Relationships

- `AGENTS.md` governa comportamento operacional dos agentes (17 regras: uma tarefa por sessão, minimum viable change, mudança cirúrgica, verificação antes de pronto, gates de validação reais) enquanto `docs/system-of-record.md` governa autoridade documental; a regra 8 do AGENTS.md delega resolução de conflito ao SOR (`AGENTS.md:14`-`AGENTS.md:130`, `docs/system-of-record.md:12`-`docs/system-of-record.md:21`).
- O SOR mapeia cada domínio às suas fontes: o domínio "Agentes e orquestração" aponta para os 3 agentes, as 33+ skills listadas e os canônicos de eventos/runtime; o domínio "Currículo e conteúdo" aponta para os master documents e as 10 pastas numeradas (`docs/system-of-record.md:31`-`docs/system-of-record.md:79`, `docs/system-of-record.md:85`-`docs/system-of-record.md:106`).
- O currículo progride do genérico ao específico: níveis 1-3 ensinam confiabilidade de agentes long-running de forma geral; o nível 4 aplica os mesmos abstrações à arquitetura KODA, customer journeys, feature patterns e rubrics (`curriculum/README.md:212`-`curriculum/README.md:267`).
- O pipeline `analyze-and-improve` conecta conhecimento externo ao repositório: fonte externa → análise/padrões/classificação em `docs/analysis/<date>-<slug>/` → artefatos definitivos (canonical docs, skills, exercícios em `curriculum/`) → atualização do SOR e índices na fase de integração; a Phase 0 (este mental model) lê só o repositório e roda em paralelo com a Phase 1, que lê a fonte externa (`.opencode/skills/analyze-and-improve/SKILL.md:105`, `.opencode/skills/analyze-and-improve/SKILL.md:140`-`.opencode/skills/analyze-and-improve/SKILL.md:158`).
- Canônicos de context formam um cluster: stable-harness-prompt, head-tail truncation, durable-fact selective history, summary buffer, topic bucketing, hybrid context stack, addressable memory catalog, tiered storage, deliberate forgetting, smallest sufficient context (`docs/system-of-record.md:197`-`docs/system-of-record.md:209`, `docs/system-of-record.md:279`-`docs/system-of-record.md:284`).
- Canônicos de eval formam uma progressão: pain-signal gate → spot-check set → production sampling → tier stratification → PR-gated enforcement → regression flywheel → correlation tracking; consolidada na 3-layer evaluation architecture (Deterministic/Semantic/Behavioral) e no living eval dataset (`docs/system-of-record.md:210`-`docs/system-of-record.md:217`, `docs/system-of-record.md:298`, `docs/system-of-record.md:300`).
- As skills operacionais implementam o mesmo mindset de harness para o próprio repositório: issue lifecycle claim → worktree → implement → review → merge → cleanup com label `agent:working`, formalizado no canonical `agent-lifecycle` (`docs/system-of-record.md:78`, `AGENTS.md:52`-`AGENTS.md:58`).
- ADRs estendem o repositório para fora dele: o bridge skills↔canons conecta o ecossistema de skills global aos padrões do vault; a federação de vaults registra 7 vaults Obsidian como wikillm consultável com roteamento por domínio no skill consumidor (`docs/decisions/2026-06-24-skill-canons-bridge-implementation.md:27`-`docs/decisions/2026-06-24-skill-canons-bridge-implementation.md:31`, `docs/decisions/2026-09-01-vault-federation-consultable-registry.md:25`-`docs/decisions/2026-09-01-vault-federation-consultable-registry.md:41`).

## 3. Patterns

| Pattern | Where Defined | Maturity |
|---|---|---|
| Owned Agent Control Loop | `docs/canonical/owned-agent-control-loop.md`; listado em `docs/system-of-record.md:189` | Canonical ativo. Loop decomposto em Prompt, Context Builder, Switch Statement e Loop com pontos de intervenção explícitos; destacado no README como padrão para builders (`README.md:73`). |
| Deterministic Tool Dispatch | `docs/canonical/deterministic-tool-dispatch.md`; `docs/system-of-record.md:188` | Canonical ativo (Padrão 2, 12FA). Ferramentas como JSON + código determinístico (`README.md:74`). |
| Error Context Hygiene | `docs/canonical/error-context-hygiene.md` + skill `.opencode/skills/error-context-hygiene/`; `docs/system-of-record.md:187`, `docs/system-of-record.md:45` | Canonical ativo (Padrão 6, 12FA) com skill de implementação das 4 regras de higiene (`README.md:75`). |
| Serializable Pause/Resume State | `docs/canonical/serializable-pause-resume-state.md`; `docs/system-of-record.md:190` | Canonical ativo (Padrão 4, 12FA) (`README.md:76`). |
| Head-Tail Context Truncation | `docs/canonical/head-tail-context-truncation.md`; `docs/system-of-record.md:197` | Canonical ativo; preserva cabeça e cauda com meio recuperável por handle (`README.md:77`). |
| Addressable Memory Catalog | `docs/canonical/addressable-memory-catalog.md`; `docs/system-of-record.md:206` | Canonical ativo; catálogo com `id`, `location`, `preview`, `scope`, `fetch` (`README.md:78`). |
| Budget-Aware Session Handoff | `docs/canonical/budget-aware-session-handoff.md`; `docs/system-of-record.md:205` | Canonical ativo; handoff preserva estado durável e reseta contexto antes do estouro de orçamento (`README.md:81`). |
| Generator/Evaluator | `docs/canonical/generator-evaluator.md`; `docs/system-of-record.md:228` | Canonical ativo; dois agentes com loop de feedback e rubricas objetivas (`README.md:82`); ensinado no nível 2 (`curriculum/README.md:228`-`curriculum/README.md:233`). |
| Plan-Execute-Verify | `docs/canonical/plan-execute-verify.md`; `docs/system-of-record.md:227` | Canonical ativo; três fases com contratos de entrada/saída por fase (`README.md:83`). |
| Eval Tier Stratification | `docs/canonical/eval-tier-stratification.md`; `docs/system-of-record.md:213` | Canonical ativo; fast (inner loop) / medium (PR gate) / deep (release/canary) (`README.md:79`). |
| Pain-Signal Eval Progression Gate | `docs/canonical/pain-signal-eval-progression-gate.md`; `docs/system-of-record.md:210` | Canonical ativo; investimento em evals guiado por sinais de dor reais (`README.md:80`). |
| Production Failure Regression Flywheel | `docs/canonical/production-failure-regression-flywheel.md`; `docs/system-of-record.md:216` | Canonical ativo; falhas de produção convertidas em evals estratificadas (`README.md:84`). Primeiro caso real registrado em `docs/evidence/` (`docs/system-of-record.md:163`). |
| 3-Layer Evaluation Architecture | `docs/canonical/3-layer-evaluation-architecture.md`; `docs/system-of-record.md:298` | Canonical ativo; Deterministic/Semantic/Behavioral por tipo de mecanismo. |
| Living Eval Dataset | `docs/canonical/living-eval-dataset.md`; `docs/system-of-record.md:300` | Canonical ativo; crescimento monotônico com cada incidente de produção. |
| Measured Harness Evolution Lifecycle | `docs/canonical/measured-harness-evolution-lifecycle.md`; `docs/system-of-record.md:196` | Canonical ativo; ciclo BUILD → STABILIZE → SIMPLIFY → REMOVE com ROI e reativação (`docs/system-of-record.md:162`). |
| Typed Event Boundaries | `docs/canonical/typed-event-boundaries.md`; `docs/system-of-record.md:360` | Canonical ativo; schema validado em runtime nas duas fronteiras (agente-ferramentas, agente-agentes); a fronteira rejeita, não corrige (`curriculum/GLOSSARY.md:980`-`curriculum/GLOSSARY.md:981`). |
| Agent Kernel Runtime | `docs/canonical/agent-kernel-runtime.md`; `docs/system-of-record.md:365` | Canonical ativo; agente como processo com scheduling, isolamento e journaling (`curriculum/GLOSSARY.md:54`-`curriculum/GLOSSARY.md:57`). |
| Cron plus Typed Events Orchestration | `docs/canonical/cron-plus-typed-events-orchestration.md`; `docs/system-of-record.md:366` | Canonical ativo; duas primitivas (cron + eventos tipados) como superfície declarativa completa (`curriculum/GLOSSARY.md:242`-`curriculum/GLOSSARY.md:243`). |
| Agent Lifecycle (issue skills) | `.opencode/skills/issue-start/`, `issue-review/`, `issue-finish/`, `issue-workflow/`; `docs/system-of-record.md:78` | Operacionalmente ativo via 4 skills; formalizado como canonical `agent-lifecycle` com label único `agent:working`. |
| Karpathy Guidelines | `.opencode/skills/karpathy-guidelines/SKILL.md`; referenciado em `AGENTS.md:24`, `AGENTS.md:32`, `AGENTS.md:40`, `AGENTS.md:48` | Skill ativa; princípios comportamentais (Think Before Coding, Simplicity First, Surgical Changes, Goal-Driven Execution) embutidos nas Rules 1-4 do AGENTS.md. |
| Skill-Canons Bridge | `docs/decisions/2026-06-24-skill-canons-bridge-implementation.md` | ADR accepted; 3 níveis de bridging, inline injection (Opção B), promotion rule D8, budget gate 4 fases; 3 skills com Level 3 Full Bridge (`docs/decisions/2026-06-24-skill-canons-bridge-implementation.md:35`-`docs/decisions/2026-06-24-skill-canons-bridge-implementation.md:42`). |
| Vault Federation | `docs/decisions/2026-09-01-vault-federation-consultable-registry.md` | ADR accepted; 7 vaults federados via notas `vault-entry` + roteamento por domínio no `canonical-context` (`docs/decisions/2026-09-01-vault-federation-consultable-registry.md:77`-`docs/decisions/2026-09-01-vault-federation-consultable-registry.md:83`). |
| Analyze-and-improve pipeline | `.opencode/skills/analyze-and-improve/SKILL.md` | Skill ativa; 7 fases com delegation a sub-agentes, dois mecanismos de execução (skill harness e bash harness) e formato de artifacts manifest desde 2026-06-14 (`docs/system-of-record.md:480`-`docs/system-of-record.md:485`). |

## 4. Abstractions (Terminology)

| Term | Definition | Source |
|---|---|---|
| Agent | Entidade autônoma de IA (geralmente LLM) que pode tomar ações, usar ferramentas e executar tarefas em sequência. | `curriculum/GLOSSARY.md:17`-`curriculum/GLOSSARY.md:18` |
| Agent Loop | Ciclo repetitivo: recebe input → pensa → toma ação → recebe resultado → repete. | `curriculum/GLOSSARY.md:65`-`curriculum/GLOSSARY.md:66` |
| Harness | Infraestrutura e padrões que envolvem um ou mais agentes para fazê-los mais confiáveis por períodos longos (state persistence, planning, evaluation loops, coordenação). | `curriculum/GLOSSARY.md:457`-`curriculum/GLOSSARY.md:464` |
| Harness Evolution | Processo de simplificar/remover componentes de harness conforme o modelo melhora. | `curriculum/GLOSSARY.md:474`-`curriculum/GLOSSARY.md:475` |
| Context Window | Número total de tokens que um modelo pode processar por vez; a "memória imediata" do agente. | `curriculum/GLOSSARY.md:197`-`curriculum/GLOSSARY.md:198` |
| Context Amnesia | Agente "esquece" contexto anterior por ter excedido a janela de contexto. | `curriculum/GLOSSARY.md:74`-`curriculum/GLOSSARY.md:75` |
| Compaction | Resumir ou comprimir contexto antigo para abrir espaço, mantendo informações-chave; server-side quando feito pelo servidor/modelo. | `curriculum/GLOSSARY.md:120`-`curriculum/GLOSSARY.md:123` |
| Token Budget / Token Accounting | Gerenciamento consciente de quantos tokens se usa e tem disponível. | `curriculum/GLOSSARY.md:898`-`curriculum/GLOSSARY.md:899` |
| Generator/Evaluator Pattern | Duas entidades (LLMs) separadas colaboram: uma gera, outra avalia; elimina sycophancy na autoavaliação. | `curriculum/GLOSSARY.md:420`-`curriculum/GLOSSARY.md:426` |
| Evaluator | Agente separado responsável por avaliar e gravar o trabalho de um Generator, contra rubrics definidas. | `curriculum/GLOSSARY.md:294`-`curriculum/GLOSSARY.md:295` |
| Sprint Contract | Acordo negociado entre generator e evaluator sobre o que "pronto" significa antes de começar. | `curriculum/GLOSSARY.md:230`-`curriculum/GLOSSARY.md:231` |
| Multi-Agent System | Sistema com múltiplos agentes independentes que coordenam entre si; padrão comum Planner + Generator + Evaluator. | `curriculum/GLOSSARY.md:599`-`curriculum/GLOSSARY.md:601` |
| Trace | Log detalhado de cada passo que um agente toma (input, reasoning, ações, output). | `curriculum/GLOSSARY.md:945`-`curriculum/GLOSSARY.md:946` |
| Sycophancy | Tendência de LLMs em agradar o usuário, mesmo aprovando qualidade inferior; solução: separar Generator + Evaluator. | `curriculum/GLOSSARY.md:869`-`curriculum/GLOSSARY.md:877` |
| KODA | Agente conversacional de IA para venda de suplementos esportivos via WhatsApp (descoberta, pedidos, fulfillment, entrega same-day); case study do programa. | `curriculum/GLOSSARY.md:544`-`curriculum/GLOSSARY.md:553` |
| METR | Model Evaluation Task Completion Rate: percentual de tarefas completadas com sucesso; benchmark de duração com 50% de sucesso. | `curriculum/GLOSSARY.md:561`-`curriculum/GLOSSARY.md:566` |
| HoP (House of Pace) | Modelo de orquestração dos agentes do repositório; cada agente tem escopo fechado, dono e gates de validação. | `docs/system-of-record.md:27`, `.opencode/agents/hop-orchestrator-rezek.md:21` |
| Agent as Declarative File | Agente definido como arquivo markdown/YAML escaneado pelo runtime, com `events` (aceita/retorna, com schema) e `schedule` (cron) como campos do formato. | `curriculum/GLOSSARY.md:28`-`curriculum/GLOSSARY.md:33` |
| Agent Kernel Runtime | Runtime que sustenta a frota como kernel de SO: agendamento, isolamento e journaling; o agente é processo de primeira classe. | `curriculum/GLOSSARY.md:54`-`curriculum/GLOSSARY.md:57` |
| Typed Event Boundary | Contrato de schema validado em runtime nas duas fronteiras do agente com o mundo externo; a fronteira rejeita, não corrige. | `curriculum/GLOSSARY.md:980`-`curriculum/GLOSSARY.md:981` |
| Closed-Loop Company | Modelo operacional em que agentes leem estado real da empresa e devolvem próximos trabalhos, bugs e atualizações de decisão. | `curriculum/GLOSSARY.md:113`-`curriculum/GLOSSARY.md:114` |
| Context Health Monitoring | Extensão do token health monitoring para qualidade: effective context size, near-miss rate, contradiction rate, health score contínuo. | `curriculum/GLOSSARY.md:210`-`curriculum/GLOSSARY.md:213` |
| Bulk In-Context Trace Analysis | ~10k traces de produção submetidos in-context a um frontier model para trend-finding; findings viram casos de eval. | `curriculum/GLOSSARY.md:98`-`curriculum/GLOSSARY.md:101` |

## 5. Curriculum Structure

- **Formato:** programa completo de 12 semanas, 4 níveis, 8 conceitos core, 35+ diagramas Mermaid; 30-50h por pessoa (`curriculum/README.md:13`, `curriculum/README.md:306`).
- **Níveis:**
  - Nível 1 — Fundamentos (3-4h): por que agentes falham em tarefas longas, context windows, token budgeting, harness patterns básicos (`curriculum/README.md:212`-`curriculum/README.md:220`).
  - Nível 2 — Padrões Práticos (6-8h): Generator/Evaluator, Sprint Contracts, Rubric Design, Trace Reading (`curriculum/README.md:226`-`curriculum/README.md:237`).
  - Nível 3 — Arquitetura Avançada (8-10h): multi-agent systems, state persistence, file-based coordination, server-side compaction, harness evolution (`curriculum/README.md:241`-`curriculum/README.md:253`).
  - Nível 4 — Aplicação KODA (contínuo): arquitetura KODA, customer journeys, feature patterns, rubrics, harness improvements, real-world exercises e case studies (`curriculum/README.md:256`-`curriculum/README.md:267`).
  - Diretórios adicionais de nível apenas com exercícios: `03-nivel-3-operational/` (shadow review, severity calibration), `03-nivel-arquiteto/` (owner-of-no-role), `04-nivel-3-engenharia-avancada/` (behavioral eval path analysis) (`curriculum/MASTER_PLAN.md:109`-`curriculum/MASTER_PLAN.md:120`).
- **8 conceitos core** (`05-core-concepts/`), cada um com explicação profunda, 3 knowledge graphs, aplicação KODA e checklist: Context Management, Planning vs. Execution, Generator/Evaluator, Sprint Contracts, State Persistence, Harness Evolution, Multi-Agent Coordination, Evaluation Rubrics (`curriculum/README.md:271`-`curriculum/README.md:288`).
- **Estrutura de diretórios:** pastas numeradas 01-10 (níveis, core concepts, knowledge graphs, implementation guides, tools/templates, case studies, references) + master documents (QUICK_START, MASTER_PLAN, INDEX, EXECUTION_PLAN, FAQ, GLOSSARY) (`curriculum/README.md:57`-`curriculum/README.md:206`).
- **Cronograma:** semanas 1-2 fundação (N1), 3-4 padrões (N2), 5-6 arquitetura (N3 subconjunto), 7-12 aplicação (N4) (`curriculum/README.md:296`-`curriculum/README.md:304`).
- **Pontos de entrada por perfil:** Quick Start (45 min), Master Plan, Execution Plan, Glossary, Knowledge Index (`README.md:36`-`README.md:46`).
- **Case studies:** 5 estudos (retro-game-maker, browser-daw, 3× KODA) em `09-case-studies/` (`docs/system-of-record.md:103`).

## 6. Existing Gaps

| Gap | Where Documented |
|---|---|
| `docs/canonical/curriculum-model.md` pendente: taxonomia de níveis, tipos de artefato e critérios de qualidade do currículo. | `docs/system-of-record.md:108`, `docs/system-of-record.md:372` |
| `docs/canonical/portal-architecture.md` pendente até a SPA proposta ser implementada. | `docs/system-of-record.md:121`, `docs/system-of-record.md:373` |
| `docs/canonical/crossroad-change-policy.md` pendente; o PR template referencia crossroad files (`src/lib/safe-console.js`, `src/lib/logger.js`, etc.) que ainda não existem no repositório — criar quando houver código fonte. | `docs/system-of-record.md:153`, `docs/system-of-record.md:374` |
| `docs/canonical/obsidian-document-conventions.md` só precisa ser criado se a convenção crescer além da AGENTS.md Rule 16. | `docs/system-of-record.md:375` |
| Tópicos candidatos a ADR ainda não decididos: stack do portal (vanilla vs. framework), content chunking, persistência de estado entre agentes, versionamento do currículo. | `docs/system-of-record.md:173`-`docs/system-of-record.md:177` |
| Ações pendentes do ADR Skill-Canons Bridge: atualizar system-design para budget gate de 4 fases, extrair shared module quando >5 skills tiverem bridge, capturar runs manuais de baseline. | `docs/decisions/2026-06-24-skill-canons-bridge-implementation.md:91`-`docs/decisions/2026-06-24-skill-canons-bridge-implementation.md:93` |
| Ações pendentes do ADR Vault Federation: incluir `mhc-knowledge-base` como 8ª vault-entry quando o domínio for reativado; regenerar grafo federado quando obsidian-eval e hop-ecosystem-atlas ganharem index no padrão Karpathy. | `docs/decisions/2026-09-01-vault-federation-consultable-registry.md:84`-`docs/decisions/2026-09-01-vault-federation-consultable-registry.md:85` |
| FAQ do currículo "em construção". | `curriculum/README.md:69`, `curriculum/README.md:497` |
| Status dos 8 conceitos core marcado como pendente (⏳) na tabela de overview do currículo. | `curriculum/README.md:279`-`curriculum/README.md:288` |
| Contagem divergente de padrões canônicos entre README (176) e SOR (185) — SOR é autoritativo pela precedência; o disco tem 186 arquivos `.md` em `docs/canonical/`. | `README.md:67`, `docs/system-of-record.md:181`, contagem de diretório em `docs/canonical/` |
