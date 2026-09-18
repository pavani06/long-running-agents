---
title: "High Throughput Agentic Engineering with Kun"
type: "extract"
source: "youtube"
video_id: "MSbacZ99E14"
url: "https://www.youtube.com/watch?v=MSbacZ99E14"
channel: "Kun Chen"
extracted: "2026-09-15"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-15-high-throughput-agentic-engineering-with-kun--MSbacZ99E14.txt]]"
tags: ["agent-fleets", "agentes-orquestracao", "multi-agent", "harness", "model-selection", "stack-tooling", "context-engineering", "context-management", "token-budgeting", "monitoramento", "decision-discipline", "gate-design", "code-review", "verification", "error-handling", "cross-session", "governanca"]
thesis: "Um único agente orquestrador ('first mate') que detém todo o contexto e intento do usuário pode despachar uma frota paralela de sub-agentes ('crew mates' e 'second mates') com roteamento de modelo por regras e cota, devolvendo ao humano apenas protótipos visuais e decisões — maximizando throughput em dezenas de projetos."
concepts: ["Padrão first mate: um único agente orquestrador como interface única do usuário", "Crew mates: sub-agentes despachados para execução", "Second mates: orquestradores por domínio, cada um sendo um first mate completo com memória e instruções próprias", "Regras de dispatch (crew_dispatch.json) mapeando tipo de tarefa para modelo/harness", "Roteamento por cota disponível quando múltiplos modelos casam numa regra", "Distinção follow-up (enfileirado) vs steer (imediato) no envio de prompts", "Modo calm: ocultar tool calls e ruído do terminal para preservar atenção humana", "Bearings: snapshot das tarefas ativas e decisões pendentes ('captain's calls') da frota", "Ahoy: skill barata de sumarização para recuperar o que o orquestrador relatou desde a última mensagem", "Lavish: artefatos HTML interativos para revisão visual de protótipos com decisões estruturadas", "Políticas por projeto: direct PR + yolo vs pipeline no-mistakes", "Pipeline no-mistakes: revisão adversarial com risk assessment e validação viva por cenários end-to-end", "Auto-compação por threshold fixo (500k tokens) em vez de gestão manual do contexto", "Gestão multi-máquina de sessões via multiplexer (Herder) com Mac Mini headless", "Relay omni-canal: mentions no Discord e no X chegando à sessão única do orquestrador", "Entrada por voz como padrão para prompts em linguagem natural", "Backpass: análise de sessões passadas dos agentes para melhorar AGENTS.md/CLAUDE.md"]
tools: ["Herder", "First Mate", "pi (harness)", "Claude Code", "Grok 4.5", "Grok 4.6", "Claude Opus 5", "Fable", "Codex", "GPT 5.6", "Kimi K3", "Astra", "Sonnet", "Luna", "Quota Axi", "Backpass", "Lavish", "No-mistakes", "Fly With Me", "Ship", "Eddie's Wallets", "Treehouse", "GitHub", "Discord", "X (Twitter)", "Mac Mini"]
people: ["Kun", "Meta", "Microsoft", "Atlassian", "Anthropic", "OpenAI", "Cursor", "Tibo"]
claims: ["Fale com um único agente orquestrador que despacha sub-agentes em vez de alternar manualmente entre sessões", "Não presuma que modelos novos são melhores; teste você mesmo (ex.: Grok 4.5 preferido ao 4.6 por velocidade e objetividade)", "Mantenha um arquivo de regras de dispatch (crew_dispatch.json) mapeando tipos de tarefa a modelos/harnesses específicos, configurável pelo próprio agente a partir de preferências", "Quando várias regras/modelos casam, consulte uma CLI de cota e escolha o modelo com mais quota disponível para não desperdiçar assinaturas", "Oculte tool calls do terminal (modo calm, com indicador de atividade) para focar no que fazer a seguir", "Use follow-up enfileirado (alt+enter) para não distrair o orquestrador e steer (enter) apenas para redirecionar imediatamente", "Escale por domínio: crie second mates, cada um um first mate completo, para absorver verticais quando o orquestrador fica sobrecarregado", "Rode second mates exigentes numa máquina headless (Mac Mini) gerenciada pelo multiplexer de sessões", "Colete snapshots periódicos (bearings) das decisões pendentes da frota e decida em lote numa UI interativa", "Peça três variantes por ideia de protótipo entregues como artefato HTML interativo com recomendações e decisões estruturadas", "Não gerencie o contexto manualmente: defina um threshold de auto-compação (500k tokens; no Claude Code via variável de ambiente, pois o default de 1M é alto demais)", "A atenção e o tempo humanos são o gargalo mais caro; otimize-os decidindo o que construir, não microeconomizando tokens", "Defina políticas de merge por projeto: yolo para projetos de baixo risco, no-mistakes para mudanças que mereceriam revisão humana", "Heurística de gate: só ative validação adversarial (no-mistakes) quando você pediria revisão de um peer humano para aquela mudança", "Confie em PRs com risk assessment baixo e evidências de testes vivos por cenários sem ler cada linha de código", "Use uma skill de sumarização barata (ahoy) para recuperar mensagens perdidas e decisões abertas do orquestrador", "Funnele reports de bugs de Discord e X para a sessão única do orquestrador via bots de relay", "Deixe o orquestrador tratar erros transientes com retry automático (ex.: erro 500 do GitHub ao criar PR)", "Analise o histórico de sessões dos agentes para melhorar continuamente AGENTS.md/CLAUDE.md (Backpass)"]
deep_dive: "high"
deep_dive_reason: "Densidade alta e novidade arquitetural diretamente relevantes a agent-fleets, harness e governança: regras de dispatch com roteamento por cota, hierarquia first/second mates multi-máquina, políticas de PR por projeto e pipeline de validação com gates e evidências."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-l8-principal-s-agentic-engineering-setup-just-copy-him--8ZgpAXe5V5w|L8 Principal's Agentic Engineering Setup (just copy him)]]", "[[extracts/youtube/ai-learning/2026-09-11-l8-principal-s-agentic-engineering-workflow--iQyg-KypKAA|L8 Principal's Agentic Engineering Workflow]]", "[[extracts/youtube/ai-learning/2026-09-11-how-the-claude-code-team-uses-claude-code--S-sYlFiGFv8|How the Claude Code team uses Claude Code]]", "[[extracts/youtube/ai-learning/2026-09-11-how-founders-build-on-claude-managed-agents--hm8NzEd5io0|How founders build on Claude Managed Agents]]", "[[extracts/youtube/ai-learning/2026-09-11-loop-engineering-to-graph-engineering--BOOfy3Yshtw|Loop Engineering to Graph Engineering]]", "[[extracts/youtube/ai-learning/2026-09-11-ex-nasa-dev-reveals-his-agentic-engineering-workflow--xgkjtF89-44|Ex-NASA dev reveals his Agentic Engineering Workflow]]", "[[extracts/youtube/ai-learning/2026-09-11-tool-skill-or-subagent-decomposing-an-agent-that-outgrew-its-prompt--mWvtOHlZM-I|Tool, skill, or subagent? Decomposing an agent that outgrew its prompt]]", "[[extracts/youtube/ai-learning/2026-09-11-how-i-automate-my-own-job-at-hugging-face-using-agents-niels-rogge-hugging-face--FLUoowDJg4I|How I automate my own job at Hugging Face using agents — Niels Rogge, Hugging Face]]", "[[extracts/youtube/ai-learning/2026-09-11-getting-started-with-omnigent-the-coding-agent-meta-harness--AyV0hum_hA8|Getting Started with Omnigent | The Coding Agent Meta-Harness]]", "[[extracts/youtube/ai-learning/2026-09-11-hermes-deepseek-4-minimax-2-7-multi-model-coding-on-a-zimaboard---3MPnUGqa68|Hermes + DeepSeek 4 + MiniMax 2.7: Multi-Model Coding on a ZimaBoard]]", "[[extracts/youtube/ai-learning/2026-09-11-wayfinder-nothing-is-too-big-to-plan-anymore--F3lL98Pj90o|/wayfinder: Nothing is too big to plan anymore]]", "[[extracts/youtube/ai-learning/2026-09-11-build-anything-with-tmux-here-s-how--z7xyZQVK4Dg|Build Anything with Tmux, Here's How]]"]
theme: "Agent Harnesses and Tooling"
---

# High Throughput Agentic Engineering with Kun

## Tese
Um único agente orquestrador ('first mate') que detém todo o contexto e intento do usuário pode despachar uma frota paralela de sub-agentes ('crew mates' e 'second mates') com roteamento de modelo por regras e cota, devolvendo ao humano apenas protótipos visuais e decisões — maximizando throughput em dezenas de projetos.

## Conceitos-chave
- Padrão first mate: um único agente orquestrador como interface única do usuário
- Crew mates: sub-agentes despachados para execução
- Second mates: orquestradores por domínio, cada um sendo um first mate completo com memória e instruções próprias
- Regras de dispatch (crew_dispatch.json) mapeando tipo de tarefa para modelo/harness
- Roteamento por cota disponível quando múltiplos modelos casam numa regra
- Distinção follow-up (enfileirado) vs steer (imediato) no envio de prompts
- Modo calm: ocultar tool calls e ruído do terminal para preservar atenção humana
- Bearings: snapshot das tarefas ativas e decisões pendentes ('captain's calls') da frota
- Ahoy: skill barata de sumarização para recuperar o que o orquestrador relatou desde a última mensagem
- Lavish: artefatos HTML interativos para revisão visual de protótipos com decisões estruturadas
- Políticas por projeto: direct PR + yolo vs pipeline no-mistakes
- Pipeline no-mistakes: revisão adversarial com risk assessment e validação viva por cenários end-to-end
- Auto-compação por threshold fixo (500k tokens) em vez de gestão manual do contexto
- Gestão multi-máquina de sessões via multiplexer (Herder) com Mac Mini headless
- Relay omni-canal: mentions no Discord e no X chegando à sessão única do orquestrador
- Entrada por voz como padrão para prompts em linguagem natural
- Backpass: análise de sessões passadas dos agentes para melhorar AGENTS.md/CLAUDE.md

## Ferramentas & pessoas
**Ferramentas:** Herder, First Mate, pi (harness), Claude Code, Grok 4.5, Grok 4.6, Claude Opus 5, Fable, Codex, GPT 5.6, Kimi K3, Astra, Sonnet, Luna, Quota Axi, Backpass, Lavish, No-mistakes, Fly With Me, Ship, Eddie's Wallets, Treehouse, GitHub, Discord, X (Twitter), Mac Mini

**Pessoas/orgs:** Kun, Meta, Microsoft, Atlassian, Anthropic, OpenAI, Cursor, Tibo

## Claims acionáveis
- Fale com um único agente orquestrador que despacha sub-agentes em vez de alternar manualmente entre sessões
- Não presuma que modelos novos são melhores; teste você mesmo (ex.: Grok 4.5 preferido ao 4.6 por velocidade e objetividade)
- Mantenha um arquivo de regras de dispatch (crew_dispatch.json) mapeando tipos de tarefa a modelos/harnesses específicos, configurável pelo próprio agente a partir de preferências
- Quando várias regras/modelos casam, consulte uma CLI de cota e escolha o modelo com mais quota disponível para não desperdiçar assinaturas
- Oculte tool calls do terminal (modo calm, com indicador de atividade) para focar no que fazer a seguir
- Use follow-up enfileirado (alt+enter) para não distrair o orquestrador e steer (enter) apenas para redirecionar imediatamente
- Escale por domínio: crie second mates, cada um um first mate completo, para absorver verticais quando o orquestrador fica sobrecarregado
- Rode second mates exigentes numa máquina headless (Mac Mini) gerenciada pelo multiplexer de sessões
- Colete snapshots periódicos (bearings) das decisões pendentes da frota e decida em lote numa UI interativa
- Peça três variantes por ideia de protótipo entregues como artefato HTML interativo com recomendações e decisões estruturadas
- Não gerencie o contexto manualmente: defina um threshold de auto-compação (500k tokens; no Claude Code via variável de ambiente, pois o default de 1M é alto demais)
- A atenção e o tempo humanos são o gargalo mais caro; otimize-os decidindo o que construir, não microeconomizando tokens
- Defina políticas de merge por projeto: yolo para projetos de baixo risco, no-mistakes para mudanças que mereceriam revisão humana
- Heurística de gate: só ative validação adversarial (no-mistakes) quando você pediria revisão de um peer humano para aquela mudança
- Confie em PRs com risk assessment baixo e evidências de testes vivos por cenários sem ler cada linha de código
- Use uma skill de sumarização barata (ahoy) para recuperar mensagens perdidas e decisões abertas do orquestrador
- Funnele reports de bugs de Discord e X para a sessão única do orquestrador via bots de relay
- Deixe o orquestrador tratar erros transientes com retry automático (ex.: erro 500 do GitHub ao criar PR)
- Analise o histórico de sessões dos agentes para melhorar continuamente AGENTS.md/CLAUDE.md (Backpass)

> **Deep dive:** `high` — Densidade alta e novidade arquitetural diretamente relevantes a agent-fleets, harness e governança: regras de dispatch com roteamento por cota, hierarquia first/second mates multi-máquina, políticas de PR por projeto e pipeline de validação com gates e evidências.
