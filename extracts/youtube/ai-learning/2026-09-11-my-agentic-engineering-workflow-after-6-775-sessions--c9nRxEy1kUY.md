---
title: "My Agentic Engineering Workflow (after 6,775 sessions)"
type: "extract"
source: "youtube"
video_id: "c9nRxEy1kUY"
url: "https://www.youtube.com/watch?v=c9nRxEy1kUY"
channel: "David Ondrej"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-my-agentic-engineering-workflow-after-6-775-sessions--c9nRxEy1kUY.txt]]"
tags: ["agent-fleets", "agent-tooling", "agents", "agentic-coding", "agentes-orquestracao", "code-review", "cross-session", "decision-discipline", "harness", "harness-engineering", "model-selection", "multi-agent", "permissions", "production", "runtime", "stack-tooling", "state", "token-budgeting", "verification"]
thesis: "Agentic engineering em 2026 exige uma stack pessoal própria — interfaces unificadas com rastreamento de estado, assinaturas de modelos subsidiadas em vez de preço de API, cloud agents auto-hospedados em VPS próprio com Herder + SSH para evitar lock-in de ecossistema, e um sistema de skills/hooks para revisão multi-modelo, guardrails de segurança e serialização de pushes — mantendo o humano no comando das decisões de arquitetura e de gosto."
concepts: ["Interface unificada multi-agente/multi-modelo", "Rastreamento de estado de agentes (idle/running/blocked/done)", "Arquitetura manager-agent orquestrando worker-agents", "Fila de prioridade de agentes (P1–P4) em vez de troca aleatória", "Economia de assinaturas subsidiadas vs. preço de API", "Cloud agents vs. agentes locais (escalabilidade, isolamento, persistência, sessões duráveis)", "Lock-in de ecossistema e migração para servidor próprio", "Sessões persistentes de agentes via runtime em VPS + SSH", "Harnesses auto-melhoráveis (geração de skills sob incerteza)", "Presending de prompts", "Skills como workflows reutilizáveis", "Revisão multi-modelo deduplicada (total review)", "Frontloading de decisões humanas antes do build (ask-and-build)", "Guard hooks pre-tool-call como guardrails", "Lock de push em nível de SO (flock) para serializar CI/CD de agentes paralelos", "Git work trees para isolamento de agentes em paralelo", "Roteamento de modelos por tipo de tarefa", "Revisão cruzada entre famílias de modelos", "Anti-revisão recursiva (alucinação de bugs)", "Ditação por voz para acelerar prompts", "Aliases de terminal e text replacements para eficiência", "Higiene de segredos (env files; nunca em skills/prompts)", "Setup de infraestrutura descrito em linguagem natural ao agente", "Composição de agentes: usar um agente para instalar e configurar outros"]
tools: ["BB", "CMAX", "Ghostty", "Herder", "Coral (fork de Zellij)", "Zellij", "tmux", "Cursor / Cursor CLI", "Claude Code", "Codex / ChatGPT", "OpenCode Go", "Pi Agent (pi.dev)", "OpenClaw", "Hermes Agent", "Prime Agent", "Grok 4.6 / 4.7", "Fable", "GPT 5.6 Soul", "Kimi K3", "GLM 5.3", "DeepSeek V4 Pro", "Hostinger VPS (plano KVM2)", "SuperWhisper", "Glo", "WhisperFlow", "Raycast", "Deep API (skill)", "OpenRouter", "GitHub"]
people: ["David Andre", "Jack Roberts", "Mario (convidado de podcast)", "Armen (convidado de podcast)", "Hostinger (patrocinador)", "Cursor (empresa)", "OpenAI", "Anthropic", "SpaceX / Elon Musk", "Devon", "AMP"]
claims: ["Use uma interface open source unificada (BB) para rodar qualquer agente, assinatura e modelo numa única UI, com sub-agentes lançados pelo agente pai", "Nunca pague preço de API; assinaturas subsidiadas (Codex, Claude Code, Cursor) entregam mais tokens por dinheiro", "Empilhe assinaturas conforme orçamento: OpenCode Go a US$10 como base, depois ChatGPT/Codex, Claude Code e Cursor nos patamares de US$30/50/70/110/210 por mês", "Evite lock-in de ecossistema rodando cloud agents em VPS próprio com Herder para sessões persistentes e SSH para acesso de qualquer dispositivo", "Delegue ao agente o setup completo do servidor em inglês simples: SSH, análise da máquina, instalação de Node/Python/Git/Herder e de outros harnesses", "Nunca coloque credenciais ou variáveis de ambiente em skills ou prompts; guarde em env files e referencie apenas a localização", "Crie aliases globais (ex.: CC para claude --dangerously-bypass-permissions, CX para codex em yolo) para comandos longos repetidos", "Nunca use YOLO/bypass-permissions sem um guard hook pre-tool-call que bloqueie deletes recursivos, comandos git/github perigosos, pipes de download e acesso a password managers", "Serialize pushes de agentes paralelos com lock de nível de SO (flock) cobrindo merge, verify, push, CI, deploy e health check para não travar CI/CD", "Rode revisão 'total review' (dois modelos de famílias diferentes consolidados numa lista deduplicada) em mudanças médias/grandes", "Evite revisões recursivas: modelos alucinam bugs inexistentes; uma checagem cruzada, corrigir o pior e publicar", "Frontload decisões arquiteturais com ask-and-build antes de codar; modelos implementam bem mas carecem de gosto e julgamento — o humano decide", "Use work trees apenas em projetos médios/grandes com 15+ agentes paralelos; em projetos pequenos permaneça num branch único", "Use harness auto-melhorável (Hermes ou Prime) em tarefas incertas e geradoras de skills; use harness clássico (Codex, Claude Code, Pi) em trabalho específico e determinístico", "Roteie modelos por tarefa: Fable para planejamento e projetos novos, GPT 5.6 Soul com reasoning máximo para bugs profundos, Grok 4.6 como padrão (mais barato/rápido), Kimi K3 para front-end", "Reserve um dia inteiro para testar cada novo modelo nos seus próprios workflows em vez de confiar em opiniões de terceiros", "Adote ditado por voz (3–4x mais rápido que digitação) para enviar prompts e text replacements/Raycast para prompts repetidos", "Use a skill Deep API para scraping, deep research e contatos onde as buscas básicas dos harnesses falham ou são bloqueadas", "Predição: em 3–6 meses o padrão será um manager agent gerenciando muitos worker agents, tornando interfaces de estado de agente essenciais", "Predição: a assinatura do Cursor se tornará um ótimo negócio em 2–4 meses graças ao compute da SpaceX pós-aquisição"]
deep_dive: "medium"
deep_dive_reason: "Há densidade prática relevante em harnesses, permissões, multi-agente e disciplina de revisão, mas o conteúdo é diluído por trechos promocionais (patrocínio de VPS) e um tour de ferramentas sem novidade arquitetural profunda."
---

# My Agentic Engineering Workflow (after 6,775 sessions)

## Tese
Agentic engineering em 2026 exige uma stack pessoal própria — interfaces unificadas com rastreamento de estado, assinaturas de modelos subsidiadas em vez de preço de API, cloud agents auto-hospedados em VPS próprio com Herder + SSH para evitar lock-in de ecossistema, e um sistema de skills/hooks para revisão multi-modelo, guardrails de segurança e serialização de pushes — mantendo o humano no comando das decisões de arquitetura e de gosto.

## Conceitos-chave
- Interface unificada multi-agente/multi-modelo
- Rastreamento de estado de agentes (idle/running/blocked/done)
- Arquitetura manager-agent orquestrando worker-agents
- Fila de prioridade de agentes (P1–P4) em vez de troca aleatória
- Economia de assinaturas subsidiadas vs. preço de API
- Cloud agents vs. agentes locais (escalabilidade, isolamento, persistência, sessões duráveis)
- Lock-in de ecossistema e migração para servidor próprio
- Sessões persistentes de agentes via runtime em VPS + SSH
- Harnesses auto-melhoráveis (geração de skills sob incerteza)
- Presending de prompts
- Skills como workflows reutilizáveis
- Revisão multi-modelo deduplicada (total review)
- Frontloading de decisões humanas antes do build (ask-and-build)
- Guard hooks pre-tool-call como guardrails
- Lock de push em nível de SO (flock) para serializar CI/CD de agentes paralelos
- Git work trees para isolamento de agentes em paralelo
- Roteamento de modelos por tipo de tarefa
- Revisão cruzada entre famílias de modelos
- Anti-revisão recursiva (alucinação de bugs)
- Ditação por voz para acelerar prompts
- Aliases de terminal e text replacements para eficiência
- Higiene de segredos (env files; nunca em skills/prompts)
- Setup de infraestrutura descrito em linguagem natural ao agente
- Composição de agentes: usar um agente para instalar e configurar outros

## Ferramentas & pessoas
**Ferramentas:** BB, CMAX, Ghostty, Herder, Coral (fork de Zellij), Zellij, tmux, Cursor / Cursor CLI, Claude Code, Codex / ChatGPT, OpenCode Go, Pi Agent (pi.dev), OpenClaw, Hermes Agent, Prime Agent, Grok 4.6 / 4.7, Fable, GPT 5.6 Soul, Kimi K3, GLM 5.3, DeepSeek V4 Pro, Hostinger VPS (plano KVM2), SuperWhisper, Glo, WhisperFlow, Raycast, Deep API (skill), OpenRouter, GitHub

**Pessoas/orgs:** David Andre, Jack Roberts, Mario (convidado de podcast), Armen (convidado de podcast), Hostinger (patrocinador), Cursor (empresa), OpenAI, Anthropic, SpaceX / Elon Musk, Devon, AMP

## Claims acionáveis
- Use uma interface open source unificada (BB) para rodar qualquer agente, assinatura e modelo numa única UI, com sub-agentes lançados pelo agente pai
- Nunca pague preço de API; assinaturas subsidiadas (Codex, Claude Code, Cursor) entregam mais tokens por dinheiro
- Empilhe assinaturas conforme orçamento: OpenCode Go a US$10 como base, depois ChatGPT/Codex, Claude Code e Cursor nos patamares de US$30/50/70/110/210 por mês
- Evite lock-in de ecossistema rodando cloud agents em VPS próprio com Herder para sessões persistentes e SSH para acesso de qualquer dispositivo
- Delegue ao agente o setup completo do servidor em inglês simples: SSH, análise da máquina, instalação de Node/Python/Git/Herder e de outros harnesses
- Nunca coloque credenciais ou variáveis de ambiente em skills ou prompts; guarde em env files e referencie apenas a localização
- Crie aliases globais (ex.: CC para claude --dangerously-bypass-permissions, CX para codex em yolo) para comandos longos repetidos
- Nunca use YOLO/bypass-permissions sem um guard hook pre-tool-call que bloqueie deletes recursivos, comandos git/github perigosos, pipes de download e acesso a password managers
- Serialize pushes de agentes paralelos com lock de nível de SO (flock) cobrindo merge, verify, push, CI, deploy e health check para não travar CI/CD
- Rode revisão 'total review' (dois modelos de famílias diferentes consolidados numa lista deduplicada) em mudanças médias/grandes
- Evite revisões recursivas: modelos alucinam bugs inexistentes; uma checagem cruzada, corrigir o pior e publicar
- Frontload decisões arquiteturais com ask-and-build antes de codar; modelos implementam bem mas carecem de gosto e julgamento — o humano decide
- Use work trees apenas em projetos médios/grandes com 15+ agentes paralelos; em projetos pequenos permaneça num branch único
- Use harness auto-melhorável (Hermes ou Prime) em tarefas incertas e geradoras de skills; use harness clássico (Codex, Claude Code, Pi) em trabalho específico e determinístico
- Roteie modelos por tarefa: Fable para planejamento e projetos novos, GPT 5.6 Soul com reasoning máximo para bugs profundos, Grok 4.6 como padrão (mais barato/rápido), Kimi K3 para front-end
- Reserve um dia inteiro para testar cada novo modelo nos seus próprios workflows em vez de confiar em opiniões de terceiros
- Adote ditado por voz (3–4x mais rápido que digitação) para enviar prompts e text replacements/Raycast para prompts repetidos
- Use a skill Deep API para scraping, deep research e contatos onde as buscas básicas dos harnesses falham ou são bloqueadas
- Predição: em 3–6 meses o padrão será um manager agent gerenciando muitos worker agents, tornando interfaces de estado de agente essenciais
- Predição: a assinatura do Cursor se tornará um ótimo negócio em 2–4 meses graças ao compute da SpaceX pós-aquisição

> **Deep dive:** `medium` — Há densidade prática relevante em harnesses, permissões, multi-agente e disciplina de revisão, mas o conteúdo é diluído por trechos promocionais (patrocínio de VPS) e um tour de ferramentas sem novidade arquitetural profunda.
