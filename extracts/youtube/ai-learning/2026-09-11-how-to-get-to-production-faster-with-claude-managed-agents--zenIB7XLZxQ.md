---
title: "How to get to production faster with Claude Managed Agents"
type: "extract"
source: "youtube"
video_id: "zenIB7XLZxQ"
url: "https://www.youtube.com/watch?v=zenIB7XLZxQ"
channel: "Claude"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-how-to-get-to-production-faster-with-claude-managed-agents--zenIB7XLZxQ.txt]]"
tags: ["agent-fleets", "agents", "agent-tooling", "arquitetura", "context-engineering", "cross-session", "governanca", "harness", "memory-architecture", "multi-agent", "observability", "permissions", "runtime", "state", "tracing"]
thesis: "Claude Managed Agents é a plataforma da Anthropic que empacota primitivas compostáveis — definição de agente, sandboxes, sessões com event stream, orquestração multi-agente, outcomes, memory/dreaming, self-hosted sandboxes e MCP tunnels — para que desenvolvedores escalem agentes à medida que o gargalo migra da inteligência do modelo para a infraestrutura."
concepts: ["definição de agente como pacote de configuração (system prompt, modelo, skills, ferramentas, permissões, identidade)", "ambiente de execução sandboxed com network allowlist e pacotes pré-instalados", "taxonomia de event stream: eventos de usuário, de agente, de sessão e span", "interrupção e human-in-the-loop via confirmações de ferramenta", "outcome-oriented agentic activity (agente trabalha horas e retorna ao concluir)", "multi-agent orchestration com threads de contexto próprio e passagem de mensagens", "outcomes como rubrica com loop de auto-avaliação e iteração", "long-lived memory stores entre sessões", "dreaming: consolidação e edição de memórias sobre milhares de sessões", "self-hosted sandboxes (BYO compute dentro do próprio VPC/perímetro)", "MCP tunnels: proxy + túnel seguro sem exposição pública", "identidade e authz para agentes, incluindo cadeias de agentes derivados", "microVMs vs isolates como primitivas de sandboxing", "pause/resume/fork de sandboxes para exploração de múltiplos desfechos", "GPU sandboxes para RL e otimização de inferência", "padrão 'human emulator': agente instala apps legados e loga para entregar resultado end-to-end", "resumabilidade de tarefas de longa duração", "autenticação delegada: permissões do humano vs permissões do agente em seu nome", "harnesses multiplayer vs single-player síncrono", "auto-otimização de configuração a partir do transcript da sessão"]
tools: ["Claude Managed Agents", "Claude Code", "Claude API skill (no Claude Code)", "Managed Agents CLI", "Anthropic cookbooks", "MCP", "MCP tunnels", "Cloudflare microVMs e isolates", "Cloudflare email service", "Cloudflare browser rendering", "Daytona sandboxes", "Modal GPU sandboxes", "Vercel Fluid Compute", "NVIDIA profiler"]
people: ["Anthropic", "Michael (Anthropic, MTS)", "Harrison (Anthropic, MTS)", "Boris", "Mike (Cloudflare)", "Ivonne (Daytona)", "Ashot (Modal)", "Luke (Vercel)", "DoorDash", "Andrej Karpathy"]
claims: ["O gargalo para a capacidade dos agentes deslocou-se da inteligência do modelo para a infraestrutura (identidade, credenciais, sandboxing, observabilidade).", "Defina um agente como bundle de configuração — system prompt, modelo, skills, ferramentas, permissões e identidade — antes de provisionar ambiente e sessão.", "Toda sessão expõe um event stream taxonomizado em eventos de usuário, agente, sessão e span, permitindo observabilidade em tempo real e interrupção para redirecionar o agente.", "Multi-agent orchestration permite ao Claude spawnar threads de agente com context windows próprias e delegar trabalho especializado via mensagens entre agentes.", "Outcomes definem uma rubrica que dispara grading iterativo em loop até que o agente julgue os resultados satisfatórios — um mecanismo nativo de verificação.", "Memory via long-lived stores torna cada sessão melhor que a anterior; dreaming (research preview) reflete sobre milhares de sessões para criar e editar memórias em escala.", "Self-hosted sandboxes permitem rodar ferramentas no próprio VPC com políticas de rede e audit logs próprios; a plataforma apenas sinaliza quando um novo sandbox deve ser provisionado.", "MCP tunnels expõem servidores MCP privados ao agente por meio de uma camada proxy e túnel seguro, sem expor nada na internet pública.", "Cloudflare aposta em duas primitivas complementares: microVMs para experiência completa de developer e isolates com spin-up em milissegundos para escalar quando o custo de inteligência cair.", "Daytona opera pelo princípio 'agentes precisam do que humanos precisam' — specs, OS, GPU variados — com pausa/resume/fork para que agentes tentem múltiplos desfechos.", "Modal escalam centenas de milhares de sandboxes em minutos em todas as regiões; GPU sandboxes já sustentam agentes que otimizam inferência via hill-climbing com NVIDIA profiler.", "Identidade de agente precisa propagar-se por cadeias de agentes que criam outros agentes, com filtragem de egress e least-privilege — ainda sem protocolo unificado na indústria.", "Para integração rápida, use a skill de Claude API no Claude Code, o CLI do Managed Agents e os cookbooks com exemplos copy-paste.", "Transcripts de sessão podem ser lidos pelo próprio Claude para sugerir otimizações de configuração (ex.: reduzir script Python de 20s de runtime).", "Problemas abertos citados pelos parceiros: resumabilidade de tarefas longas, autenticação delegada humano-vs-agente, fork/time-travel de estados e harnesses multiplayer em vez de single-player síncrono."]
deep_dive: "medium"
deep_dive_reason: "Anuncia primitivas novas e relevantes a harness, agent-fleets e governança (orquestração multi-agente, outcomes, dreaming, MCP tunnels, self-hosted sandboxes) com painel arquitetural genuíno, mas o formato de lançamento de produto e a demo promocional limitam a densidade de insight implementacional."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-ship-your-first-managed-agent--19HDQ9HppOA|Ship your first Managed Agent]]", "[[extracts/youtube/ai-learning/2026-09-11-how-founders-build-on-claude-managed-agents--hm8NzEd5io0|How founders build on Claude Managed Agents]]", "[[extracts/youtube/ai-learning/2026-09-11-building-with-claude-managed-agents-and-asana-ai-teammates--BrpB-h1e--k|Building with Claude Managed Agents and Asana AI teammates]]", "[[extracts/youtube/ai-learning/2026-09-11-code-with-claude-opening-keynote--EvtPBaaykdo|Code with Claude Opening Keynote]]", "[[extracts/youtube/ai-learning/2026-09-11-anthropic-s-applied-ai-team-on-the-evolution-of-agentic-surfaces--K0X9QDRkIdg|Anthropic's Applied AI team on the Evolution of Agentic Surfaces]]", "[[extracts/youtube/ai-learning/2026-09-11-how-the-claude-code-team-uses-claude-code--S-sYlFiGFv8|How the Claude Code team uses Claude Code]]", "[[extracts/youtube/ai-learning/2026-09-11-introducing-managed-deep-agents-interrupt-26--LdQpoK2TzSo|Introducing Managed Deep Agents | Interrupt 26]]", "[[extracts/youtube/ai-learning/2026-09-11-claude-codes-new-intent-md-what-is-it--LoMOPj-lO8U|Claude Codes New INTENT.MD, What is It?]]", "[[extracts/youtube/ai-learning/2026-09-11-build-a-proactive-agent-workflow-with-claude-code--eSP7PLTXNy8|Build a proactive agent workflow with Claude Code]]", "[[extracts/youtube/ai-learning/2026-09-11-building-ai-agents-with-claude-demo--_al9YYnF2xI|Building AI Agents with Claude! (Demo)]]", "[[extracts/youtube/ai-learning/2026-09-11-unlock-autonomous-ai-agents-with-auth-md-michael-grinich-mcp-night-agent-mode-ke--Dqp_b8GHLXU|Unlock Autonomous AI Agents with auth.md, Michael Grinich | MCP Night: Agent Mode Keynote]]", "[[extracts/youtube/ai-learning/2026-09-11-claude-mcp-how-to-modify-your-servers-to-the-next-level--aIAxWr5ix1o|Claude MCP - How To Modify Your Servers To The Next Level]]"]
---

# How to get to production faster with Claude Managed Agents

## Tese
Claude Managed Agents é a plataforma da Anthropic que empacota primitivas compostáveis — definição de agente, sandboxes, sessões com event stream, orquestração multi-agente, outcomes, memory/dreaming, self-hosted sandboxes e MCP tunnels — para que desenvolvedores escalem agentes à medida que o gargalo migra da inteligência do modelo para a infraestrutura.

## Conceitos-chave
- definição de agente como pacote de configuração (system prompt, modelo, skills, ferramentas, permissões, identidade)
- ambiente de execução sandboxed com network allowlist e pacotes pré-instalados
- taxonomia de event stream: eventos de usuário, de agente, de sessão e span
- interrupção e human-in-the-loop via confirmações de ferramenta
- outcome-oriented agentic activity (agente trabalha horas e retorna ao concluir)
- multi-agent orchestration com threads de contexto próprio e passagem de mensagens
- outcomes como rubrica com loop de auto-avaliação e iteração
- long-lived memory stores entre sessões
- dreaming: consolidação e edição de memórias sobre milhares de sessões
- self-hosted sandboxes (BYO compute dentro do próprio VPC/perímetro)
- MCP tunnels: proxy + túnel seguro sem exposição pública
- identidade e authz para agentes, incluindo cadeias de agentes derivados
- microVMs vs isolates como primitivas de sandboxing
- pause/resume/fork de sandboxes para exploração de múltiplos desfechos
- GPU sandboxes para RL e otimização de inferência
- padrão 'human emulator': agente instala apps legados e loga para entregar resultado end-to-end
- resumabilidade de tarefas de longa duração
- autenticação delegada: permissões do humano vs permissões do agente em seu nome
- harnesses multiplayer vs single-player síncrono
- auto-otimização de configuração a partir do transcript da sessão

## Ferramentas & pessoas
**Ferramentas:** Claude Managed Agents, Claude Code, Claude API skill (no Claude Code), Managed Agents CLI, Anthropic cookbooks, MCP, MCP tunnels, Cloudflare microVMs e isolates, Cloudflare email service, Cloudflare browser rendering, Daytona sandboxes, Modal GPU sandboxes, Vercel Fluid Compute, NVIDIA profiler

**Pessoas/orgs:** Anthropic, Michael (Anthropic, MTS), Harrison (Anthropic, MTS), Boris, Mike (Cloudflare), Ivonne (Daytona), Ashot (Modal), Luke (Vercel), DoorDash, Andrej Karpathy

## Claims acionáveis
- O gargalo para a capacidade dos agentes deslocou-se da inteligência do modelo para a infraestrutura (identidade, credenciais, sandboxing, observabilidade).
- Defina um agente como bundle de configuração — system prompt, modelo, skills, ferramentas, permissões e identidade — antes de provisionar ambiente e sessão.
- Toda sessão expõe um event stream taxonomizado em eventos de usuário, agente, sessão e span, permitindo observabilidade em tempo real e interrupção para redirecionar o agente.
- Multi-agent orchestration permite ao Claude spawnar threads de agente com context windows próprias e delegar trabalho especializado via mensagens entre agentes.
- Outcomes definem uma rubrica que dispara grading iterativo em loop até que o agente julgue os resultados satisfatórios — um mecanismo nativo de verificação.
- Memory via long-lived stores torna cada sessão melhor que a anterior; dreaming (research preview) reflete sobre milhares de sessões para criar e editar memórias em escala.
- Self-hosted sandboxes permitem rodar ferramentas no próprio VPC com políticas de rede e audit logs próprios; a plataforma apenas sinaliza quando um novo sandbox deve ser provisionado.
- MCP tunnels expõem servidores MCP privados ao agente por meio de uma camada proxy e túnel seguro, sem expor nada na internet pública.
- Cloudflare aposta em duas primitivas complementares: microVMs para experiência completa de developer e isolates com spin-up em milissegundos para escalar quando o custo de inteligência cair.
- Daytona opera pelo princípio 'agentes precisam do que humanos precisam' — specs, OS, GPU variados — com pausa/resume/fork para que agentes tentem múltiplos desfechos.
- Modal escalam centenas de milhares de sandboxes em minutos em todas as regiões; GPU sandboxes já sustentam agentes que otimizam inferência via hill-climbing com NVIDIA profiler.
- Identidade de agente precisa propagar-se por cadeias de agentes que criam outros agentes, com filtragem de egress e least-privilege — ainda sem protocolo unificado na indústria.
- Para integração rápida, use a skill de Claude API no Claude Code, o CLI do Managed Agents e os cookbooks com exemplos copy-paste.
- Transcripts de sessão podem ser lidos pelo próprio Claude para sugerir otimizações de configuração (ex.: reduzir script Python de 20s de runtime).
- Problemas abertos citados pelos parceiros: resumabilidade de tarefas longas, autenticação delegada humano-vs-agente, fork/time-travel de estados e harnesses multiplayer em vez de single-player síncrono.

> **Deep dive:** `medium` — Anuncia primitivas novas e relevantes a harness, agent-fleets e governança (orquestração multi-agente, outcomes, dreaming, MCP tunnels, self-hosted sandboxes) com painel arquitetural genuíno, mas o formato de lançamento de produto e a demo promocional limitam a densidade de insight implementacional.
