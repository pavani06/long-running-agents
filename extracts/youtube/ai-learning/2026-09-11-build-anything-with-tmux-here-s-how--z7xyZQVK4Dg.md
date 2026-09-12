---
title: "Build Anything with Tmux, Here's How"
type: "extract"
source: "youtube"
video_id: "z7xyZQVK4Dg"
url: "https://www.youtube.com/watch?v=z7xyZQVK4Dg"
channel: "David Ondrej"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-build-anything-with-tmux-here-s-how--z7xyZQVK4Dg.txt]]"
tags: ["agent-tooling", "agentic-coding", "agents", "multi-agent", "runtime", "stack-tooling"]
thesis: "O tmux rodando em um VPS acessado via SSH é apresentado como infraestrutura essencial para engenharia agêntica, pois mantém sessões de terminal persistentes onde múltiplos agentes (Codex CLI, Claude Code) podem rodar por horas ou dias independentemente do laptop local."
concepts: ["terminal multiplexer (tmux)", "persistência de sessões (detach/reattach)", "hierarquia sessões/janelas/panes", "VPS (virtual private server)", "SSH e SSH tunneling", "execução paralela de múltiplos agentes", "comandos de agente de longa duração (/go, /goal)", "mouse mode no tmux", "tmux como substrate para setups multi-agent", "autenticação via device code"]
tools: ["tmux", "Hostinger (plano KVM2)", "Codex CLI", "Claude Code", "Terminus", "Svelte", "Vite", "Homebrew", "Ubuntu", "Cloudflare", "Vercel", "Supabase", "ChatGPT Pro", "npm", "GitHub", "OBS"]
people: ["David (autor do vídeo, cupom Hostinger)", "Peter Steinberger (criador do OpenClaw)", "Mario Zechner/Mario Zakner (criador do Pi)", "OpenAI", "Anthropic", "Hostinger"]
claims: ["Instale tmux via 'brew install tmux' (macOS) ou 'apt install tmux' (Ubuntu) e crie sessões nomeadas com 'tmux new -s <nome>', reconectando com 'tmux attach -t <nome>' e listando com 'tmux ls'", "Habilite mouse mode com 'set -g mouse on' para poder clicar entre panes e rolar o terminal", "Atalhos essenciais do tmux: Ctrl+B D (detach), Ctrl+B % (split horizontal), Ctrl+B \" (split vertical), lembrando de soltar Ctrl+B antes da segunda tecla", "Rode os agentes em um VPS acessado por SSH para que continuem executando mesmo se o laptop desconectar, fechar ou descarregar", "Recursos como /go (Codex) e /goal (Claude Code, Hermes) podem rodar por horas ou dias e exigem terminal persistente em servidor em vez da máquina local", "Instale Codex CLI e Claude Code diretamente no VPS e autentique via device code ou assinatura (ChatGPT/Claude)", "Use múltiplos panes e sessões do tmux para rodar vários agentes em paralelo no mesmo projeto ou em projetos diferentes; agentes podem ler outros panes programaticamente, funcionando como substrate multi-agent", "Use o app Terminus no iPhone para gerenciar sessões SSH/tmux pelo celular quando agentes travam longe do computador", "Exponha apps em desenvolvimento no VPS (ex.: 'npm run dev --host 0.0.0.0' na porta 5173) e acesse via túnel SSH pelo navegador local", "'tmux kill-server' encerra todas as sessões; 'exit' fecha um pane individual", "Flags como 'codex --yolo' e 'claude --dangerously-skip-permissions' reduzem prompts de permissão durante execução autônoma (com risco associado)", "O setup completo (VPS + tmux + CLIs de agente) pode ser feito em 40-60 minutos mesmo por não-devops"]
deep_dive: "low"
deep_dive_reason: "Tutorial introdutório e patrocinado sobre uma prática consagrada (tmux+VPS) com dicas operacionais úteis, mas sem novidade arquitetural nem profundidade em harness, evals, context-engineering ou governança."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-mastering-claude-code-in-30-minutes--6eBSHbLKuN0|Mastering Claude Code in 30 minutes]]", "[[extracts/youtube/ai-learning/2026-09-11-claude-code-best-practices-code-w-claude--gv0WHhKelSE|Claude Code best practices | Code w/ Claude]]", "[[extracts/youtube/ai-learning/2026-09-11-how-to-use-cursor-agent-for-beginners--2gBcO3ht0ws|How to use Cursor Agent for beginners]]", "[[extracts/youtube/ai-learning/2026-09-11-pi-architecture-explained-agent-loop-tools-tui-and-more--gTeujlv8qK0|PI Architecture EXPLAINED | Agent Loop, Tools, TUI and More]]", "[[extracts/youtube/ai-learning/2026-09-11-full-workshop-setting-yourself-up-for-success-jason-liu-openai-codex--il1c1a2FufU|Full Workshop: Setting Yourself Up for Success —Jason Liu, OpenAI Codex]]", "[[extracts/youtube/ai-learning/2026-09-11-5-simple-ai-agents-you-must-have-beginners-guide--WLvQCIUWebs|5 simple AI Agents you must have - beginners guide]]"]
theme: "Codificação Agêntica com Claude Code"
---

# Build Anything with Tmux, Here's How

## Tese
O tmux rodando em um VPS acessado via SSH é apresentado como infraestrutura essencial para engenharia agêntica, pois mantém sessões de terminal persistentes onde múltiplos agentes (Codex CLI, Claude Code) podem rodar por horas ou dias independentemente do laptop local.

## Conceitos-chave
- terminal multiplexer (tmux)
- persistência de sessões (detach/reattach)
- hierarquia sessões/janelas/panes
- VPS (virtual private server)
- SSH e SSH tunneling
- execução paralela de múltiplos agentes
- comandos de agente de longa duração (/go, /goal)
- mouse mode no tmux
- tmux como substrate para setups multi-agent
- autenticação via device code

## Ferramentas & pessoas
**Ferramentas:** tmux, Hostinger (plano KVM2), Codex CLI, Claude Code, Terminus, Svelte, Vite, Homebrew, Ubuntu, Cloudflare, Vercel, Supabase, ChatGPT Pro, npm, GitHub, OBS

**Pessoas/orgs:** David (autor do vídeo, cupom Hostinger), Peter Steinberger (criador do OpenClaw), Mario Zechner/Mario Zakner (criador do Pi), OpenAI, Anthropic, Hostinger

## Claims acionáveis
- Instale tmux via 'brew install tmux' (macOS) ou 'apt install tmux' (Ubuntu) e crie sessões nomeadas com 'tmux new -s <nome>', reconectando com 'tmux attach -t <nome>' e listando com 'tmux ls'
- Habilite mouse mode com 'set -g mouse on' para poder clicar entre panes e rolar o terminal
- Atalhos essenciais do tmux: Ctrl+B D (detach), Ctrl+B % (split horizontal), Ctrl+B " (split vertical), lembrando de soltar Ctrl+B antes da segunda tecla
- Rode os agentes em um VPS acessado por SSH para que continuem executando mesmo se o laptop desconectar, fechar ou descarregar
- Recursos como /go (Codex) e /goal (Claude Code, Hermes) podem rodar por horas ou dias e exigem terminal persistente em servidor em vez da máquina local
- Instale Codex CLI e Claude Code diretamente no VPS e autentique via device code ou assinatura (ChatGPT/Claude)
- Use múltiplos panes e sessões do tmux para rodar vários agentes em paralelo no mesmo projeto ou em projetos diferentes; agentes podem ler outros panes programaticamente, funcionando como substrate multi-agent
- Use o app Terminus no iPhone para gerenciar sessões SSH/tmux pelo celular quando agentes travam longe do computador
- Exponha apps em desenvolvimento no VPS (ex.: 'npm run dev --host 0.0.0.0' na porta 5173) e acesse via túnel SSH pelo navegador local
- 'tmux kill-server' encerra todas as sessões; 'exit' fecha um pane individual
- Flags como 'codex --yolo' e 'claude --dangerously-skip-permissions' reduzem prompts de permissão durante execução autônoma (com risco associado)
- O setup completo (VPS + tmux + CLIs de agente) pode ser feito em 40-60 minutos mesmo por não-devops

> **Deep dive:** `low` — Tutorial introdutório e patrocinado sobre uma prática consagrada (tmux+VPS) com dicas operacionais úteis, mas sem novidade arquitetural nem profundidade em harness, evals, context-engineering ou governança.
