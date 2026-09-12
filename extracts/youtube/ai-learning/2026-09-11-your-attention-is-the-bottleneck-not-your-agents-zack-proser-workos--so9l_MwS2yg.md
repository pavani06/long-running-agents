---
title: "Your Attention Is the Bottleneck, Not Your Agents — Zack Proser, WorkOS"
type: "extract"
source: "youtube"
video_id: "so9l_MwS2yg"
url: "https://www.youtube.com/watch?v=so9l_MwS2yg"
channel: "AI Engineer"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-your-attention-is-the-bottleneck-not-your-agents-zack-proser-workos--so9l_MwS2yg.txt]]"
tags: ["agents", "agentic-coding", "agent-loop", "agent-tooling", "harness", "gate-design", "verification", "multi-agent", "cross-session", "knowledge-management", "code-review", "monitoramento", "process"]
thesis: "Com agentes de IA escalando quase infinitamente, o gargalo passou a ser a atenção e a energia do desenvolvedor humano, que precisa redesenhar seu fluxo de trabalho (camadas de sinal, voz, controle remoto e auto-melhoria do harness) para sustentar qualidade sem burnout."
concepts: ["agentes não são mais o gargalo; a atenção humana é a restrição rígida", "signal layers: agentes filtrando Slack e Linear via MCP para proteger o foco", "fluxos voice-first (~184 wpm vs ~90 wpm digitando) habilitando workflows paralelos", "remote control de sessões do Claude Code pelo celular, integrando focus mode e diffuse mode (shower principle)", "gates de verificação em 3 níveis: lint/build/testes unitários via hooks; verificação no navegador; revisor estilo constitutional AI", "auto-melhoria do harness: revisão semanal dos logs JSONL de conversas para extrair skills faltantes", "hooks ao fim da sessão para persistir aprendizados num datastore separado (Obsidian/markdown)", "turno noturno de agentes: cron jobs, tickets marcados como agent-ready no Linear, loop a cada 15 minutos", "git worktrees para paralelismo real entre agentes em tarefas grandes", "delegar apenas código que você é qualificado para revisar; usar LLMs para acelerar aprendizado profundo", "dados biométricos (Oura Ring via MCP) integrados ao loop de trabalho para gestão holística de energia"]
tools: ["Claude Code", "MCP", "Slack", "Linear", "Cursor", "Codex", "Zed", "GitHub / GitHub Mobile", "Vercel bot", "Opus 4.6", "GPT-4.1", "ChatGPT Advanced Voice Mode", "OpenClaw", "Twilio", "Oura Ring", "Chrome Use", "Computer Use", "Obsidian", "Whisper Flow (open source)", "AWS"]
people: ["Zach (WorkOS)", "WorkOS", "Simon Willison (citado como Simon Wilson)", "Nick (colega)", "Anthropic", "OpenAI"]
claims: ["Dê ao Claude Code acesso MCP a Slack e Linear para deduplicar solicitações e destacar prioridades, reduzindo o custo das trocas de contexto", "Configure verificação em gates: (1) lint/build/testes unitários via hooks, (2) click-through no navegador com Chrome use, (3) agente revisor constitucional que audita o trabalho", "Ative o remote control do Claude Code para dirigir sessões rodando na sua máquina a partir do celular via LTE enquanto caminha", "Rode uma passagem semanal do agente sobre os arquivos JSONL de conversas locais para identificar skills, MCP servers e ferramentas faltantes e apertar o loop", "Use hooks ao fim de cada sessão/merge para salvar pontos de dificuldade em markdown ou Obsidian antes da análise semanal", "Marque tickets Linear com uma tag agent-ready com subtarefas de bugs/features e rode um loop a cada 15 minutos, dia e noite, para churn contínuo", "Use git worktrees e prompts bem definidos para rodar múltiplos agentes em paralelo em features que tocam toda a pilha", "Codificação por voz atinge ~184 wpm contra ~90 wpm digitando, permitindo dirigir vários agentes em paralelo antes de um dev tradicional terminar o primeiro prompt", "Não delegue a agentes código que você não saberia escrever ou revisar; mantenha deep work manual para construir julgamento e detectar alucinações", "Comente em linguagem natural em PRs no GitHub Mobile (@claude, @cursor, @vercelbot) para iterar sem voltar à mesa", "Integre dados biométricos via MCP (Oura Ring) para o agente ajustar escopo conforme sono e energia, evitando burnout acelerado"]
deep_dive: "medium"
deep_dive_reason: "Oferece táticas concretas e relevantes a harness, gates de verificação e loops de agentes (revisão de JSONL, turno noturno, worktrees), mas permanece um relato pessoal de produtividade sem aprofundamento arquitetural ou avaliação sistemática."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-ex-nasa-dev-reveals-his-agentic-engineering-workflow--xgkjtF89-44|Ex-NASA dev reveals his Agentic Engineering Workflow]]", "[[extracts/youtube/ai-learning/2026-09-11-no-vibes-allowed-solving-hard-problems-in-complex-codebases-dex-horthy-humanlaye--rmvDxxNubIg|No Vibes Allowed: Solving Hard Problems in Complex Codebases – Dex Horthy, HumanLayer]]", "[[extracts/youtube/ai-learning/2026-09-11-the-golden-age-of-ai-engineering-alexander-embiricos-romain-huet-peter-steinberg--pMggiOb18tc|The Golden Age of AI Engineering — Alexander Embiricos & Romain Huet & Peter Steinberger, OpenAI]]", "[[extracts/youtube/ai-learning/2026-09-11-l8-principal-s-agentic-engineering-setup-just-copy-him--8ZgpAXe5V5w|L8 Principal's Agentic Engineering Setup (just copy him)]]", "[[extracts/youtube/ai-learning/2026-09-11-75m-founder-reveals-his-agentic-engineering-setup--QBfXiWvM0qc|$75M founder reveals his Agentic Engineering setup]]", "[[extracts/youtube/ai-learning/2026-09-11-l8-principal-s-agentic-engineering-workflow--iQyg-KypKAA|L8 Principal's Agentic Engineering Workflow]]"]
---

# Your Attention Is the Bottleneck, Not Your Agents — Zack Proser, WorkOS

## Tese
Com agentes de IA escalando quase infinitamente, o gargalo passou a ser a atenção e a energia do desenvolvedor humano, que precisa redesenhar seu fluxo de trabalho (camadas de sinal, voz, controle remoto e auto-melhoria do harness) para sustentar qualidade sem burnout.

## Conceitos-chave
- agentes não são mais o gargalo; a atenção humana é a restrição rígida
- signal layers: agentes filtrando Slack e Linear via MCP para proteger o foco
- fluxos voice-first (~184 wpm vs ~90 wpm digitando) habilitando workflows paralelos
- remote control de sessões do Claude Code pelo celular, integrando focus mode e diffuse mode (shower principle)
- gates de verificação em 3 níveis: lint/build/testes unitários via hooks; verificação no navegador; revisor estilo constitutional AI
- auto-melhoria do harness: revisão semanal dos logs JSONL de conversas para extrair skills faltantes
- hooks ao fim da sessão para persistir aprendizados num datastore separado (Obsidian/markdown)
- turno noturno de agentes: cron jobs, tickets marcados como agent-ready no Linear, loop a cada 15 minutos
- git worktrees para paralelismo real entre agentes em tarefas grandes
- delegar apenas código que você é qualificado para revisar; usar LLMs para acelerar aprendizado profundo
- dados biométricos (Oura Ring via MCP) integrados ao loop de trabalho para gestão holística de energia

## Ferramentas & pessoas
**Ferramentas:** Claude Code, MCP, Slack, Linear, Cursor, Codex, Zed, GitHub / GitHub Mobile, Vercel bot, Opus 4.6, GPT-4.1, ChatGPT Advanced Voice Mode, OpenClaw, Twilio, Oura Ring, Chrome Use, Computer Use, Obsidian, Whisper Flow (open source), AWS

**Pessoas/orgs:** Zach (WorkOS), WorkOS, Simon Willison (citado como Simon Wilson), Nick (colega), Anthropic, OpenAI

## Claims acionáveis
- Dê ao Claude Code acesso MCP a Slack e Linear para deduplicar solicitações e destacar prioridades, reduzindo o custo das trocas de contexto
- Configure verificação em gates: (1) lint/build/testes unitários via hooks, (2) click-through no navegador com Chrome use, (3) agente revisor constitucional que audita o trabalho
- Ative o remote control do Claude Code para dirigir sessões rodando na sua máquina a partir do celular via LTE enquanto caminha
- Rode uma passagem semanal do agente sobre os arquivos JSONL de conversas locais para identificar skills, MCP servers e ferramentas faltantes e apertar o loop
- Use hooks ao fim de cada sessão/merge para salvar pontos de dificuldade em markdown ou Obsidian antes da análise semanal
- Marque tickets Linear com uma tag agent-ready com subtarefas de bugs/features e rode um loop a cada 15 minutos, dia e noite, para churn contínuo
- Use git worktrees e prompts bem definidos para rodar múltiplos agentes em paralelo em features que tocam toda a pilha
- Codificação por voz atinge ~184 wpm contra ~90 wpm digitando, permitindo dirigir vários agentes em paralelo antes de um dev tradicional terminar o primeiro prompt
- Não delegue a agentes código que você não saberia escrever ou revisar; mantenha deep work manual para construir julgamento e detectar alucinações
- Comente em linguagem natural em PRs no GitHub Mobile (@claude, @cursor, @vercelbot) para iterar sem voltar à mesa
- Integre dados biométricos via MCP (Oura Ring) para o agente ajustar escopo conforme sono e energia, evitando burnout acelerado

> **Deep dive:** `medium` — Oferece táticas concretas e relevantes a harness, gates de verificação e loops de agentes (revisão de JSONL, turno noturno, worktrees), mas permanece um relato pessoal de produtividade sem aprofundamento arquitetural ou avaliação sistemática.
