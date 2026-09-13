# projects.md — âncoras de ação do digest

Projetos ativos do operador (@fepavani). O **x-digest** lê este arquivo para ancorar as
2–3 ações por tema nos projetos reais — priorizando e aprofundando pelos de **tier** mais alto.

- **Uso:** somente leitura pelo CI (nunca escrito por workflow). Sem PAT amplo.
- **Manutenção:** local, via `gh repo list` (o `gh` do operador já é autenticado) — adicione
  um projeto quando ele passar a merecer ação ancorada. Não precisa ser exaustivo: é lista de
  **prioridade**, não inventário. O que não está aqui ainda aparece como entity/tema.
- **Formato:** agrupado por tier (1 = prioridade/profundidade máxima), `- **<nome>** — <linha concreta>`.
  Teses não-repo no fim.

## Tier 1

- **long-running-agents** — Currículo + padrões canônicos de agentes long-running e os pipelines de dados (youtube, x-bookmarks/digest). Este repositório.
- **sisyphus-runtime** — Runtime Sisyphus: orquestração de sessões e agentes long-running (wake→work→sleep, dispatch, telemetria).
- **scripts** — Infra do runtime Sisyphus: pipeline de telemetria (systemd), sync do vault CIOT, dispatch runners, tooling de reflexão.
- **papers-journal** — Jornal diário dos Daily Papers do Hugging Face: busca, triagem contra perfil de interesse, publica em markdown/HTML.
- **llm-council** — Conselho de LLMs com avaliação cruzada cega (quatro provedores respondem, avaliam-se sem autoria, presidente sintetiza). CLI + MCP.
- **chatshop-io/chatbot-ai** — Umbrella (map + remote control) da frota chatshop-io: manifest `repos.yaml`, justfile runner, agent roles. Sem app code.
- **chatshop-io/mhc-knowledge-base** — KB alinhada a IDSD: governança humana (intents, expectations) + decision contracts executáveis do agente KODA. Monorepo docs-first (Obsidian).
- **chatshop-io/mhc-backend** — Backend do MHC/KODA (agente de conversational commerce esportivo).
- **chatshop-io/commerce** — Serviço de commerce da chatshop-io. _[refinar: 1 linha concreta]_
- **govevo** — GovEvo. _[refinar: 1 linha concreta do projeto]_

## Tier 2

- **agent-skills** — Source of truth das Agent Skills (padrão SKILL.md): pipeline de issues do GitHub para OpenCode, Claude Code e Codex.
- **opencode-config** — Preferências globais do OpenCode: config, AGENTS.md, skills portáteis, restore manifest.
- **obsidian-eval** — Runtime da CLI `obsidian-eval`: scan/query/graph/write + epistemic graph do vault.
- **Raw-Knowledge** — Corpus bruto de conhecimento (fonte para curadoria/análise).
- **HoP** — House of Pace: agente digital KODA para conversational commerce esportivo.
- **sergio-machado** — IB Analysis Department: sistema multi-agente para análise de investment banking (OpenCode).

## Teses / temas não-repo

- **CIOT / AuthPay** — _[refinar: 1 linha concreta da tese CIOT/AuthPay]_
- **Ciclismo / performance** — treino, fisiologia e performance em ciclismo.
- **Mercado brasileiro** — leitura de mercado e macroeconomia do Brasil.
