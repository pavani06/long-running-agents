# System of Record

Mapa das fontes canônicas do `long-running-agents`. Quando duas fontes divergirem, a precedência abaixo resolve o conflito.

## Precedência

1. **ADRs aceitos** em `docs/decisions/` — decisões de arquitetura formalizadas e aprovadas
2. **Documentação canônica ativa** em `docs/canonical/` — descrições autoritativas de sistemas e contratos
3. **Evidências validadas** em `docs/evidence/` — benchmarks, resultados de teste, métricas
4. **Análises e diagnósticos** em `docs/analysis/` — investigações pontuais, comparações, diagnósticos
5. **Documentos históricos** em `docs/archive/` — versões anteriores, documentos obsoletos
6. **READMEs, planos, agent definitions e resumos operacionais** — fontes de entrada, não autoritativas

## Domínios do projeto

### Agentes e orquestração

O sistema de agentes é definido em `.opencode/` e segue o modelo HoP (Handoff Protocol): cada agente tem um escopo fechado, um dono, e gates de validação.

| Fonte | Cobre |
|---|---|
| [.opencode/agents/hop-orchestrator-rezek.md](.opencode/agents/hop-orchestrator-rezek.md) | Orquestrador principal — governança, source-of-truth, coordenação |
| [.opencode/agents/koda-hop-init-basic.md](.opencode/agents/koda-hop-init-basic.md) | Subagente de inicial guiada do KODA |
| [.opencode/agents/hop-live-whatsapp-tester.md](.opencode/agents/hop-live-whatsapp-tester.md) | Subagente de teste live de WhatsApp |
| [.opencode/skills/issue-start/SKILL.md](.opencode/skills/issue-start/SKILL.md) | Workflow claim → worktree → execution brief |
| [.opencode/skills/issue-review/SKILL.md](.opencode/skills/issue-review/SKILL.md) | Workflow validação → draft PR → second-agent review |
| [.opencode/skills/issue-finish/SKILL.md](.opencode/skills/issue-finish/SKILL.md) | Workflow merge → cleanup branch/worktree/labels |
| [.opencode/skills/issue-workflow/SKILL.md](.opencode/skills/issue-workflow/SKILL.md) | Ciclo completo de lifecycle de issue |
| [.opencode/skills/refine-issue/SKILL.md](.opencode/skills/refine-issue/SKILL.md) | Decomposição de issues em sub-issues com dependências |
| [.opencode/skills/orchestrator/SKILL.md](.opencode/skills/orchestrator/SKILL.md) | Coordenação de agentes paralelos, dashboard de status |
| [.opencode/skills/doc-coauthoring/SKILL.md](.opencode/skills/doc-coauthoring/SKILL.md) | Workflow de co-autoria de documentação |
| [.opencode/skills/writing-plans/SKILL.md](.opencode/skills/writing-plans/SKILL.md) | Criação de planos de implementação detalhados |
| [.opencode/skills/error-context-hygiene/SKILL.md](.opencode/skills/error-context-hygiene/SKILL.md) | Skill de implementação: 4 regras de higiene de erro no contexto |
| [.opencode/skills/analyze-and-improve/SKILL.md](.opencode/skills/analyze-and-improve/SKILL.md) | Pipeline knowledge → patterns → classification → improvements |
| [AGENTS.md](AGENTS.md) | Regras operacionais obrigatórias para agentes e colaboradores |

> **Pendente**: `docs/canonical/agent-lifecycle.md` descrevendo o ciclo claim → worktree → implement → review → merge → cleanup.

### Currículo e conteúdo

O currículo é o produto principal do repositório: um programa completo de 12 semanas sobre construção de agentes long-running aplicados ao KODA.

| Fonte | Cobre |
|---|---|
| [curriculum/README.md](curriculum/README.md) | Visão geral do programa, estrutura, métricas de sucesso |
| [curriculum/MASTER_PLAN.md](curriculum/MASTER_PLAN.md) | Plano mestre com todos os níveis e conceitos |
| [curriculum/INDEX.md](curriculum/INDEX.md) | Índice executivo com navegação por perfil |
| [curriculum/QUICK_START.md](curriculum/QUICK_START.md) | Onboarding rápido em 45 minutos |
| [curriculum/EXECUTION_PLAN.md](curriculum/EXECUTION_PLAN.md) | Cronograma detalhado de 12 semanas |
| [curriculum/GLOSSARY.md](curriculum/GLOSSARY.md) | Glossário de termos técnicos |
| `curriculum/01-nivel-1-fundamentals/` | Nível 1 — conceitos fundamentais (3-4h) |
| `curriculum/02-nivel-2-practical-patterns/` | Nível 2 — padrões práticos (6-8h) |
| `curriculum/03-nivel-3-advanced-architecture/` | Nível 3 — arquitetura avançada (8-10h) |
| `curriculum/04-nivel-4-koda-specific/` | Nível 4 — aplicação específica ao KODA (contínuo) |
| `curriculum/05-core-concepts/` | 8 conceitos core com explicações, graphs e checklists |
| `curriculum/06-knowledge-graphs/` | 35+ diagramas Mermaid |
| `curriculum/07-implementation-guides/` | Guias de setup, progressão, harness design |
| `curriculum/08-tools-templates/` | Templates de sprint contract, rubrica, ADR, progress tracker |
| `curriculum/09-case-studies/` | 5 estudos de caso (retro-game-maker, browser-daw, 3× KODA) |
| `curriculum/10-references/` | Referências externas e timeline de capacidade de modelos |
| [rawfiles/](rawfiles/) | Material-fonte usado para gerar o currículo |
| [prompts/](prompts/) | Prompts usados na geração do conteúdo do currículo |

> **Pendente**: `docs/canonical/curriculum-model.md` definindo taxonomia de níveis, tipos de artefato e critérios de qualidade.

### Portal web

Três artefatos HTML estáticos e uma proposta de arquitetura futura.

| Fonte | Cobre |
|---|---|
| [web/koda_course_portal.html](web/koda_course_portal.html) | Portal do curso — data-driven, vanilla JS, metadata-only |
| [web/koda_knowledge_graphs_35_diagrams.html](web/koda_knowledge_graphs_35_diagrams.html) | Visualizador dos 35 diagramas Mermaid com renderização sequencial |
| [web/mhc_visao_estrategica.html](web/mhc_visao_estrategica.html) | Visão estratégica MHC |
| [webpage/analise-arquitetural.md](webpage/analise-arquitetural.md) | Proposta de arquitetura SPA com content chunking, hash routing, lazy Mermaid, busca full-text, dark mode |

> **Pendente**: `docs/canonical/portal-architecture.md` quando a SPA proposta for implementada.

### Stack e tooling

| Fonte | Cobre |
|---|---|
| [package.json](package.json) | Dependências, scripts, engine Node (>= 20.18, ESM) |
| [jsconfig.json](jsconfig.json) | Configuração de módulos e paths para o editor |
| [eslint.config.js](eslint.config.js) | Regras de lint: ESLint 10 + plugin-n + unicorn + 2 regras customizadas |
| [eslint-rules/no-catch-message.js](eslint-rules/no-catch-message.js) | Regra customizada: proíbe mensagem em catch vazio |
| [eslint-rules/no-raw-console-in-scripts.js](eslint-rules/no-raw-console-in-scripts.js) | Regra customizada: proíbe console.log direto em scripts |
| [.editorconfig](.editorconfig) | Convenções de formatação (UTF-8, LF, indent 2 espaços) |
| [Makefile](Makefile) | Atalhos para lint e testes |
| [.env.example](.env.example) | Template de variáveis de ambiente |
| [opencode.json](opencode.json) | Configuração do OpenCode (MCP context7) |

### Governança de repositório

| Fonte | Cobre |
|---|---|
| [.github/PULL_REQUEST_TEMPLATE.md](.github/PULL_REQUEST_TEMPLATE.md) | Template de PR com checklist de crossroad files e revisão |
| [.github/CODEOWNERS](.github/CODEOWNERS) | Política de code ownership para crossroad files |
| [.github/ISSUE_TEMPLATE/](.github/ISSUE_TEMPLATE/) | Templates de issue (config.yml, technical.md) |
| [.github/dependabot.yml](.github/dependabot.yml) | Configuração de atualização automática de dependências |
| [scripts/create-curriculum-issues.sh](scripts/create-curriculum-issues.sh) | Script de automação de criação de issues do currículo |

> **Nota**: O PR template referencia crossroad files (`src/lib/safe-console.js`, `src/lib/logger.js`, etc.) e `docs/guides/crossroad-change-policy.md` que ainda não existem no repositório. Esses arquivos devem ser criados quando houver código fonte.

## Decisões de arquitetura (ADRs)

`docs/decisions/` está vazio. Nenhum ADR formal foi registrado.

Tópicos candidatos a ADR:
- Escolha de stack do portal (vanilla JS estático vs. framework)
- Modelo de content chunking e carregamento sob demanda
- Estratégia de persistência de estado entre agentes
- Política de versionamento do currículo

## Documentação canônica pendente

`docs/canonical/` não está mais vazio. Há 4 padrões canônicos ativos.

### Padrões canônicos ativos

| Documento | Cobre |
|---|---|
| `error-context-hygiene.md` | Padrão 6 (12FA): higiene de erros no contexto do agente |
| `deterministic-tool-dispatch.md` | Padrão 2 (12FA): dispatch determinístico de ferramentas |
| `owned-agent-control-loop.md` | Padrão 3 (12FA): loop de controle do agente com 4 componentes |
| `serializable-pause-resume-state.md` | Padrão 4 (12FA): serialização de estado para pause/resume |

### Documentos esperados quando o domínio correspondente amadurecer

| Documento | Cobre |
|---|---|
| `agent-lifecycle.md` | Ciclo completo claim → worktree → implement → review → merge → cleanup |
| `curriculum-model.md` | Taxonomia de níveis, tipos de artefato, critérios de qualidade |
| `portal-architecture.md` | Decisões de design do portal, modelo de dados, pipeline de renderização |
| `crossroad-change-policy.md` | Política de alteração em arquivos de alto blast radius |

## Análises e diagnósticos

Diagnósticos do backend MHC/KODA em `docs/analysis/mhc-backend/`:

- [2026-05-28-output-validation-structured-generation.md](docs/analysis/mhc-backend/2026-05-28-output-validation-structured-generation.md) — validação estruturada com Zod/LangChain
- [2026-05-28-janela-deslizante-contexto.md](docs/analysis/mhc-backend/2026-05-28-janela-deslizante-contexto.md) — janela deslizante, resumo e metadados no contexto do agente
- [2026-05-28-output-validation-state-persistence.md](docs/analysis/mhc-backend/2026-05-28-output-validation-state-persistence.md) — camadas de validação e persistência de estado
- [2026-05-26-nivel-3-comparacao.md](docs/analysis/mhc-backend/2026-05-26-nivel-3-comparacao.md) — comparação KODA vs. padrões Nível 3
- [2026-05-26-harness-diagnostic.md](docs/analysis/mhc-backend/2026-05-26-harness-diagnostic.md) — arquitetura KODA vs. padrões de harness
- [2026-05-26-nivel-2-diagnostic.md](docs/analysis/mhc-backend/2026-05-26-nivel-2-diagnostic.md) — maturidade de padrões Nível 2 no sistema
- [2026-05-26-pedido-bling-agente.md](docs/analysis/mhc-backend/2026-05-26-pedido-bling-agente.md) — falha de notificação de pedido pago (webhook/ERP)

### Análises comparativas (12-Factor Agents)

| Arquivo | Cobre |
|---|---|
| `2026-06-09-12-factor-agents/analysis.md` | Extração de conhecimento não-óbvio da talk 12-Factor Agents |
| `2026-06-09-12-factor-agents/analysis.yaml` | YAML com frameworks, padrões, lições operacionais |
| `2026-06-09-12-factor-agents/patterns.md` | 8 padrões agentic extraídos com 6 campos cada |
| `2026-06-09-12-factor-agents/patterns.yaml` | YAML com componentes e fluxo por padrão |
| `2026-06-09-12-factor-agents/classification.md` | Classificação comparativa dos 8 padrões vs. repo |
| `2026-06-09-12-factor-agents/classification.yaml` | YAML com evidência por padrão |
| `2026-06-09-12-factor-agents/integration-roadmap.md` | Roadmap de integração dos padrões ao currículo |

## Planos

- [docs/plans/2026-05-26-curriculum-completion-strategy.md](docs/plans/2026-05-26-curriculum-completion-strategy.md) — estratégia de execução para completar o currículo via GitHub Issues/Milestones

---

*Última atualização: 2026-06-09*
