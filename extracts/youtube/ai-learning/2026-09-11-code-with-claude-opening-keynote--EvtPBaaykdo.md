---
title: "Code with Claude Opening Keynote"
type: "extract"
source: "youtube"
video_id: "EvtPBaaykdo"
url: "https://www.youtube.com/watch?v=EvtPBaaykdo"
channel: "Anthropic"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-code-with-claude-opening-keynote--EvtPBaaykdo.txt]]"
tags: ["agents", "agentic-coding", "agent-tooling", "harness", "context-engineering", "memory-architecture", "cross-session", "model-selection", "multi-agent", "token-budgeting", "runtime", "production", "roadmap", "evals", "governanca"]
thesis: "No primeiro developer conference da Anthropic (Code with Claude), a empresa lançou Claude Opus 4 e Sonnet 4 juntamente com uma suíte de plataforma — code execution, MCP connector, Files API com memória auto-gerenciada e prompt caching de 1 hora — para viabilizar agentes de codificação autônomos de múltiplas horas, com Claude Code em GA servindo como harness multi-superfície (terminal, VS Code, JetBrains, GitHub)."
concepts: ["Lançamento de Claude Opus 4 e Sonnet 4 como modelos híbridos (resposta rápida + extended thinking)", "Opus 4 para workflows agênticos complexos vs Sonnet 4 como daily driver de custo-eficiência", "Correção de overeagerness e reward hacking no Sonnet 4", "Execução autônoma de tarefas de múltiplas horas (6-7h) com gerenciamento próprio de to-do list e memória", "Code execution tool: Claude escreve, executa, observa resultados e refina iterativamente", "Model Context Protocol (MCP) como conector universal de ferramentas/dados para agentes", "Memória auto-gerenciada via Files API: leitura/escrita de arquivos de memória para manter contexto entre sessões", "Prompt caching com TTL estendido de 5min para 1h para workflows agênticos longos", "Claude Code como agente de codificação em GA: integrações IDE com diff views inline e SDK para workflows customizados", "Autocorreção/super-ação de agentes em paralelo (flaky tests, cobertura, on-call triage)", "Três pilares de agentes segundo Krieger: contextual intelligence, long-running execution, genuine collaboration", "Autonomia inteligente com checkpoints humanos (architectural safety checkpoints)", "Interpretabilidade como base de auditoria de agentes (Golden Gate Claude, ensaio de Amodei)", "Inner loop (editor) e outer loop (assíncrono) do SDLC com camada agêntica", "Self-improvement: Claude Code ajudando a construir a si mesmo"]
tools: ["Claude Opus 4", "Claude Sonnet 4", "Claude Code", "Claude Code SDK", "Claude Code no GitHub (Actions/PRs/issues, beta)", "Anthropic API (Messages API)", "MCP Connector", "Files API", "Code execution tool", "Web search tool (durante raciocínio)", "Prompt caching (TTL 1h)", "Prompt improver e evaluations", "VS Code e JetBrains extensions", "GitHub CLI", "GitHub Copilot / Copilot coding agent", "Excalidraw", "Amazon Bedrock", "Google Cloud Vertex AI", "Amazon Alexa+", "Golden Gate Claude", "Sentry, Zapier, Asana (integrações MCP)", "Notion", "TurboTax", "Thompson Reuters CoCounsel"]
people: ["Mike Krieger (CPO, Anthropic; cofundador do Instagram e Artifact)", "Dario Amodei (CEO e cofundador, Anthropic)", "Cat Wu (PM de Claude Code, Anthropic)", "Michael Gerstenhaber (Head de Produto da API Platform, Anthropic)", "Mario Rodriguez (GitHub)", "Boris (tech lead criador do Claude Code)", "Kevin Scott (CTO da Microsoft)", "Anthropic", "GitHub/Microsoft", "Amazon (Alexa)", "Cursor", "Novo Nordisk", "Notion"]
claims: ["Opus 4 executa autonomamente tarefas que levam humanos 6-7 horas (SOTA em SWE-bench e Terminal Bench) e Rocketzin reportou 7 horas de execução sustentada", "Sonnet 4 é melhoria estrita sobre Sonnet 3.7 no mesmo custo, corrigindo overeagerness e reward hacking", "A janela de trabalho autônomo cresceu de minutos (Claude 3) para ~45 min (Claude 3.5) para horas, dobrando a cada poucos meses", "Prompt caching de 1h (12x o TTL de 5min) reduz custo em até 90% e latência em até 85%, viabilizando agentes longos; >50% dos tokens de entrada já são cached, dobrando efetivamente o contexto", "Memória entre sessões é implementável com pouco overhead via Files API + cookbook da Anthropic: Claude lê e escreve arquivos de memória mantendo contexto ao longo do tempo", "Rodar Claude Code na raiz do repositório em vez de por-repo permite que o agente navegue múltiplos codebases (frontend/backend) automaticamente", "Claude Code reduziu o onboarding técnico na Anthropic de 2-3 semanas para 2-3 dias", "Demo real: Claude Code implementou componente de tabela no Excalidraw (com testes e lint passando) em 90 minutos a partir de um único prompt", "O Claude Code SDK permite instâncias paralelas para corrigir flaky tests, aumentar cobertura e fazer on-call triage", "MCP tem 3.000+ integrações comunitárias e foi adotado por Microsoft, Google, OpenAI, Block, Atlassian, Zapier e Linear em menos de um ano", "GitHub escolheu Sonnet para o Copilot coding agent com base em evals próprias: conhecimento de engenharia, problem-solving e instruction following com ferramentas/MCP", "Os novos modelos usam ferramentas (ex.: web search) durante o raciocínio e executam múltiplas ferramentas em paralelo", "Cada feature de plataforma incorpora checkpoints de segurança arquiteturais: aprovações humanas configuráveis por ação, robustez a prompt injection e feedback loops transparentes", "Pesquisa econômica da Anthropic indica que IA amplia tarefas em vez de substituir funções inteiras"]
deep_dive: "medium"
deep_dive_reason: "Keynote de lançamento com densidade relevante de anúncios acionáveis (SDK do Claude Code, memória via Files API, caching 1h, paralelismo de agentes, checkpoints de governança), mas sem aprofundamento arquitetural ou técnico que caracterizaria um deep dive alto, misturado com conteúdo promocional."
---

# Code with Claude Opening Keynote

## Tese
No primeiro developer conference da Anthropic (Code with Claude), a empresa lançou Claude Opus 4 e Sonnet 4 juntamente com uma suíte de plataforma — code execution, MCP connector, Files API com memória auto-gerenciada e prompt caching de 1 hora — para viabilizar agentes de codificação autônomos de múltiplas horas, com Claude Code em GA servindo como harness multi-superfície (terminal, VS Code, JetBrains, GitHub).

## Conceitos-chave
- Lançamento de Claude Opus 4 e Sonnet 4 como modelos híbridos (resposta rápida + extended thinking)
- Opus 4 para workflows agênticos complexos vs Sonnet 4 como daily driver de custo-eficiência
- Correção de overeagerness e reward hacking no Sonnet 4
- Execução autônoma de tarefas de múltiplas horas (6-7h) com gerenciamento próprio de to-do list e memória
- Code execution tool: Claude escreve, executa, observa resultados e refina iterativamente
- Model Context Protocol (MCP) como conector universal de ferramentas/dados para agentes
- Memória auto-gerenciada via Files API: leitura/escrita de arquivos de memória para manter contexto entre sessões
- Prompt caching com TTL estendido de 5min para 1h para workflows agênticos longos
- Claude Code como agente de codificação em GA: integrações IDE com diff views inline e SDK para workflows customizados
- Autocorreção/super-ação de agentes em paralelo (flaky tests, cobertura, on-call triage)
- Três pilares de agentes segundo Krieger: contextual intelligence, long-running execution, genuine collaboration
- Autonomia inteligente com checkpoints humanos (architectural safety checkpoints)
- Interpretabilidade como base de auditoria de agentes (Golden Gate Claude, ensaio de Amodei)
- Inner loop (editor) e outer loop (assíncrono) do SDLC com camada agêntica
- Self-improvement: Claude Code ajudando a construir a si mesmo

## Ferramentas & pessoas
**Ferramentas:** Claude Opus 4, Claude Sonnet 4, Claude Code, Claude Code SDK, Claude Code no GitHub (Actions/PRs/issues, beta), Anthropic API (Messages API), MCP Connector, Files API, Code execution tool, Web search tool (durante raciocínio), Prompt caching (TTL 1h), Prompt improver e evaluations, VS Code e JetBrains extensions, GitHub CLI, GitHub Copilot / Copilot coding agent, Excalidraw, Amazon Bedrock, Google Cloud Vertex AI, Amazon Alexa+, Golden Gate Claude, Sentry, Zapier, Asana (integrações MCP), Notion, TurboTax, Thompson Reuters CoCounsel

**Pessoas/orgs:** Mike Krieger (CPO, Anthropic; cofundador do Instagram e Artifact), Dario Amodei (CEO e cofundador, Anthropic), Cat Wu (PM de Claude Code, Anthropic), Michael Gerstenhaber (Head de Produto da API Platform, Anthropic), Mario Rodriguez (GitHub), Boris (tech lead criador do Claude Code), Kevin Scott (CTO da Microsoft), Anthropic, GitHub/Microsoft, Amazon (Alexa), Cursor, Novo Nordisk, Notion

## Claims acionáveis
- Opus 4 executa autonomamente tarefas que levam humanos 6-7 horas (SOTA em SWE-bench e Terminal Bench) e Rocketzin reportou 7 horas de execução sustentada
- Sonnet 4 é melhoria estrita sobre Sonnet 3.7 no mesmo custo, corrigindo overeagerness e reward hacking
- A janela de trabalho autônomo cresceu de minutos (Claude 3) para ~45 min (Claude 3.5) para horas, dobrando a cada poucos meses
- Prompt caching de 1h (12x o TTL de 5min) reduz custo em até 90% e latência em até 85%, viabilizando agentes longos; >50% dos tokens de entrada já são cached, dobrando efetivamente o contexto
- Memória entre sessões é implementável com pouco overhead via Files API + cookbook da Anthropic: Claude lê e escreve arquivos de memória mantendo contexto ao longo do tempo
- Rodar Claude Code na raiz do repositório em vez de por-repo permite que o agente navegue múltiplos codebases (frontend/backend) automaticamente
- Claude Code reduziu o onboarding técnico na Anthropic de 2-3 semanas para 2-3 dias
- Demo real: Claude Code implementou componente de tabela no Excalidraw (com testes e lint passando) em 90 minutos a partir de um único prompt
- O Claude Code SDK permite instâncias paralelas para corrigir flaky tests, aumentar cobertura e fazer on-call triage
- MCP tem 3.000+ integrações comunitárias e foi adotado por Microsoft, Google, OpenAI, Block, Atlassian, Zapier e Linear em menos de um ano
- GitHub escolheu Sonnet para o Copilot coding agent com base em evals próprias: conhecimento de engenharia, problem-solving e instruction following com ferramentas/MCP
- Os novos modelos usam ferramentas (ex.: web search) durante o raciocínio e executam múltiplas ferramentas em paralelo
- Cada feature de plataforma incorpora checkpoints de segurança arquiteturais: aprovações humanas configuráveis por ação, robustez a prompt injection e feedback loops transparentes
- Pesquisa econômica da Anthropic indica que IA amplia tarefas em vez de substituir funções inteiras

> **Deep dive:** `medium` — Keynote de lançamento com densidade relevante de anúncios acionáveis (SDK do Claude Code, memória via Files API, caching 1h, paralelismo de agentes, checkpoints de governança), mas sem aprofundamento arquitetural ou técnico que caracterizaria um deep dive alto, misturado com conteúdo promocional.
