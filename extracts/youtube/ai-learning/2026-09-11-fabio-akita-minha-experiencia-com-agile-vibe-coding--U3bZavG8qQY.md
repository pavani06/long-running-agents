---
title: "Fabio Akita: Minha Experiência com Agile Vibe Coding"
type: "extract"
source: "youtube"
video_id: "U3bZavG8qQY"
url: "https://www.youtube.com/watch?v=U3bZavG8qQY"
channel: "Tropical on Rails"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-fabio-akita-minha-experiencia-com-agile-vibe-coding--U3bZavG8qQY.txt]]"
tags: ["agentic-coding", "agents", "agent-loop", "agent-tooling", "model-selection", "evals", "token-budgeting", "context-management", "spec-driven-development", "testes-qa", "error-handling", "code-review", "process", "stack-tooling", "knowledge-management", "macroeconomia", "analise"]
thesis: "A IA não substitui nem nivela engenheiros — ela amplifica quem você já é: desde novembro de 2025 (GPT 5.1 + Opus 4.5) tornou-se viável programar tratando agentes de código como programadores juniores gerenciados com disciplina real de engenharia (testes, revisão contínua, iteração e descarte), e quem não obtém aceleração de 5-10x está usando o LLM do jeito errado, como gerador de snippets."
concepts: ["IA reflete quem você é: acelera 10x tanto excelência quanto dívida técnica", "LLM como loot box: geração estocástica de tokens (top K, top P, temperature)", "Pós-treinamento para bajular/concordar, não para dar a resposta certa", "Histórico de chat como contexto de personalidade que enviesa novas sessões", "Corrida de parâmetros 2022-2024 e teto da curva-S: +1 ordem de grandeza em parâmetros custa +2 em energia", "2025 como ano dos agentes: autorretificação na sessão e problema de agent loops infinitos", "Turning point em novembro/2025 com GPT 5.1 e Claude Opus 4.5", "Thinking mode + tool calling: cadeia de comandos (ler/gravar arquivos, bash) com resultados devolvidos como contexto", "Papel do humano como tech lead/PM/QA mentorando o agente-júnior", "Método PILOT: Plan, Investigate, Polish, Operate, Test, adjust em loop", "Instruction files incrementais (CLAUDE.md/AGENTS.md) em vez de spec único gigante", "Testes de regressão após cada bug fix e gates pré-push (cobertura, lint, análise estática)", "Agile vibe coding = XP/ágil real: testes, CI, pairing com o agente", "Fundamentos de CS antes de ferramentas; sem base só se produz slop", "Descarte barato de código: iterar 20-30 vezes e jogar fora", "Banda de memória > capacidade para inferência local (DDR4/DDR5/LPDDR5 lentos; só GDDR7)", "Requisitos de modelo para code agents: prompt caching, tool calling treinado, deep thinking", "Economia de tokens: assinaturas subsidiadas vs pay-per-token; não economizar tokens", "Engenharia reversa clean-room do código vazado do Claude Code", "Senior que não ensina não é senior; experiência como poda dos 19 caminhos que falham", "Próxima corrida da indústria: otimização de energia/inferência (prompt caching, KV cache) em vez de parâmetros"]
tools: ["Claude Code", "Claude Opus 4.5", "Claude Sonnet 4.5/4.6", "OpenAI Codex", "GPT 5.1", "ChatGPT", "Cursor", "VS Code", "Vim", "OpenCode", "Frank Code (reescrita do OpenCode em Rust)", "GLM 5.1", "Qwen 3.5-35B", "DeepSeek", "ElevenLabs", "Whisper", "Qwen 3 TTS", "Stable Diffusion", "Flux", "LoRA", "Rails", "Ruby", "Ruby LLM", "SimpleCov", "Brakeman", "RuboCop", "Tailwind", "Rust", "React", "TypeScript", "CLAUDE.md/AGENTS.md", "NVIDIA RTX 5090 (GDDR7, 32GB VRAM)", "AMD Ryzen AI Max (128GB)", "Makita Chronicles / Marvin (bot)", "Git", "GitHub", "Google Play Store", "Spotify", "YouTube"]
people: ["Fabio Akita", "Codeminer 42", "Talisson (sócio)", "Cirdes (organizador do evento)", "Anthropic", "OpenAI", "Alibaba", "NVIDIA", "Amazon", "Microsoft", "Meta", "Asami Arts (artista VTuber)", "Frank Rosenblatt (criador do Perceptron)", "Martin Fowler", "Igor (Flow Podcast)", "Vilela", "Muji (canal de drama)", "Tropical Ruby (conferência)", "Hoyoverse", "Nijisanji", "Vshojo", "ElevenLabs"]
claims: ["Se a IA não te acelera 5-10x, você está usando errado: não a use como gerador de snippets no editor (estilo Cursor), e sim em imersão de dias sem tocar no editor", "Trate o agente como júnior com tarefas gerenciais/QA (rodar cobertura, adicionar regressão, refatorar em partial) em vez de comandos linha a linha", "Siga o método PILOT (Planejar, Investigar, Polir, Operar, Testar, ajustar) em loop contínuo", "Construa CLAUDE.md/AGENTS.md incrementalmente conforme observa falhas; inclua regras como 'todo bug fix ganha teste de regressão' e 'rodar SimpleCov/Brakeman/RuboCop antes do git push'", "Não comece com arquivo de instruções gigante: desperdiça contexto e cria instruções conflitantes", "Spec-driven de prompt único não funciona; é preciso avaliar e corrigir o agente passo a passo", "Modelos práticos para uso diário: Claude Opus, GPT High e no máximo GLM 5.1; Sonnet/GLM bastam só para apps pequenos; automação complexa exige Opus", "Evite DeepSeek (sem prompt caching, tool calling fraco) e variantes Qwen Coder; o único open puro útil é Qwen 3.5-35B; destilados de Claude sobre Qwen geram código que não roda", "Nunca instale OpenCode na máquina local; se precisar, use VPS isolada — ou reescreva você mesmo (feito em 2 dias em Rust)", "Reescreva sistemas legados como experimento de 2 dias abrindo o agente no diretório do código", "Faça seu próprio benchmark de modelos (~5 minutos por modelo com script de harness) em vez de perguntar a gurus", "Pare de economizar tokens: assinaturas (ex.: US$ 200 Max 20x) são subsidiadas versus ~US$ 1.000 em pay-per-token; use intensivamente agora e espere preços dobrarem/triplicarem", "Para inferência local priorize banda (GDDR7/RTX 5090 com 32GB); DDR4, DDR5, LPDDR5 e Ryzen AI Max 128GB são lentos/inviáveis para agentes", "Modelos menores e rápidos que falham rápido com feedback podem chegar a resultados melhores que modelos grandes lentos", "Descarte código sem culpa: itere 20-30 vezes e ajuste estilo/nomenclatura depois via follow-up, não durante", "Modelo de code agent precisa de três coisas: prompt caching, tool calling treinado e deep thinking", "TTS open source (Whisper + Qwen 3 TTS) é ruim para podcast; use comercial (ElevenLabs) com tags de emoção", "Novembro/2025 (GPT 5.1 + Opus 4.5) marcou o ponto em que programar com agentes se tornou de fato viável", "A próxima corrida da indústria é otimização de energia/inferência (prompt caching, KV cache, deep thinking), não mais parâmetros", "Empresa que não treina juniores com seniores e depende de uma pessoa só é frágil; senior que não ensina não é senior"]
deep_dive: "high"
deep_dive_reason: "Alta densidade de insight acionável com dados primários raros (300k linhas/500h, benchmark de 30 modelos, rankings pós-nov/2025) e relevância direta a agent-tooling, context-management de instruction files e evals de modelos, apesar do tom anedótico em partes."
---

# Fabio Akita: Minha Experiência com Agile Vibe Coding

## Tese
A IA não substitui nem nivela engenheiros — ela amplifica quem você já é: desde novembro de 2025 (GPT 5.1 + Opus 4.5) tornou-se viável programar tratando agentes de código como programadores juniores gerenciados com disciplina real de engenharia (testes, revisão contínua, iteração e descarte), e quem não obtém aceleração de 5-10x está usando o LLM do jeito errado, como gerador de snippets.

## Conceitos-chave
- IA reflete quem você é: acelera 10x tanto excelência quanto dívida técnica
- LLM como loot box: geração estocástica de tokens (top K, top P, temperature)
- Pós-treinamento para bajular/concordar, não para dar a resposta certa
- Histórico de chat como contexto de personalidade que enviesa novas sessões
- Corrida de parâmetros 2022-2024 e teto da curva-S: +1 ordem de grandeza em parâmetros custa +2 em energia
- 2025 como ano dos agentes: autorretificação na sessão e problema de agent loops infinitos
- Turning point em novembro/2025 com GPT 5.1 e Claude Opus 4.5
- Thinking mode + tool calling: cadeia de comandos (ler/gravar arquivos, bash) com resultados devolvidos como contexto
- Papel do humano como tech lead/PM/QA mentorando o agente-júnior
- Método PILOT: Plan, Investigate, Polish, Operate, Test, adjust em loop
- Instruction files incrementais (CLAUDE.md/AGENTS.md) em vez de spec único gigante
- Testes de regressão após cada bug fix e gates pré-push (cobertura, lint, análise estática)
- Agile vibe coding = XP/ágil real: testes, CI, pairing com o agente
- Fundamentos de CS antes de ferramentas; sem base só se produz slop
- Descarte barato de código: iterar 20-30 vezes e jogar fora
- Banda de memória > capacidade para inferência local (DDR4/DDR5/LPDDR5 lentos; só GDDR7)
- Requisitos de modelo para code agents: prompt caching, tool calling treinado, deep thinking
- Economia de tokens: assinaturas subsidiadas vs pay-per-token; não economizar tokens
- Engenharia reversa clean-room do código vazado do Claude Code
- Senior que não ensina não é senior; experiência como poda dos 19 caminhos que falham
- Próxima corrida da indústria: otimização de energia/inferência (prompt caching, KV cache) em vez de parâmetros

## Ferramentas & pessoas
**Ferramentas:** Claude Code, Claude Opus 4.5, Claude Sonnet 4.5/4.6, OpenAI Codex, GPT 5.1, ChatGPT, Cursor, VS Code, Vim, OpenCode, Frank Code (reescrita do OpenCode em Rust), GLM 5.1, Qwen 3.5-35B, DeepSeek, ElevenLabs, Whisper, Qwen 3 TTS, Stable Diffusion, Flux, LoRA, Rails, Ruby, Ruby LLM, SimpleCov, Brakeman, RuboCop, Tailwind, Rust, React, TypeScript, CLAUDE.md/AGENTS.md, NVIDIA RTX 5090 (GDDR7, 32GB VRAM), AMD Ryzen AI Max (128GB), Makita Chronicles / Marvin (bot), Git, GitHub, Google Play Store, Spotify, YouTube

**Pessoas/orgs:** Fabio Akita, Codeminer 42, Talisson (sócio), Cirdes (organizador do evento), Anthropic, OpenAI, Alibaba, NVIDIA, Amazon, Microsoft, Meta, Asami Arts (artista VTuber), Frank Rosenblatt (criador do Perceptron), Martin Fowler, Igor (Flow Podcast), Vilela, Muji (canal de drama), Tropical Ruby (conferência), Hoyoverse, Nijisanji, Vshojo, ElevenLabs

## Claims acionáveis
- Se a IA não te acelera 5-10x, você está usando errado: não a use como gerador de snippets no editor (estilo Cursor), e sim em imersão de dias sem tocar no editor
- Trate o agente como júnior com tarefas gerenciais/QA (rodar cobertura, adicionar regressão, refatorar em partial) em vez de comandos linha a linha
- Siga o método PILOT (Planejar, Investigar, Polir, Operar, Testar, ajustar) em loop contínuo
- Construa CLAUDE.md/AGENTS.md incrementalmente conforme observa falhas; inclua regras como 'todo bug fix ganha teste de regressão' e 'rodar SimpleCov/Brakeman/RuboCop antes do git push'
- Não comece com arquivo de instruções gigante: desperdiça contexto e cria instruções conflitantes
- Spec-driven de prompt único não funciona; é preciso avaliar e corrigir o agente passo a passo
- Modelos práticos para uso diário: Claude Opus, GPT High e no máximo GLM 5.1; Sonnet/GLM bastam só para apps pequenos; automação complexa exige Opus
- Evite DeepSeek (sem prompt caching, tool calling fraco) e variantes Qwen Coder; o único open puro útil é Qwen 3.5-35B; destilados de Claude sobre Qwen geram código que não roda
- Nunca instale OpenCode na máquina local; se precisar, use VPS isolada — ou reescreva você mesmo (feito em 2 dias em Rust)
- Reescreva sistemas legados como experimento de 2 dias abrindo o agente no diretório do código
- Faça seu próprio benchmark de modelos (~5 minutos por modelo com script de harness) em vez de perguntar a gurus
- Pare de economizar tokens: assinaturas (ex.: US$ 200 Max 20x) são subsidiadas versus ~US$ 1.000 em pay-per-token; use intensivamente agora e espere preços dobrarem/triplicarem
- Para inferência local priorize banda (GDDR7/RTX 5090 com 32GB); DDR4, DDR5, LPDDR5 e Ryzen AI Max 128GB são lentos/inviáveis para agentes
- Modelos menores e rápidos que falham rápido com feedback podem chegar a resultados melhores que modelos grandes lentos
- Descarte código sem culpa: itere 20-30 vezes e ajuste estilo/nomenclatura depois via follow-up, não durante
- Modelo de code agent precisa de três coisas: prompt caching, tool calling treinado e deep thinking
- TTS open source (Whisper + Qwen 3 TTS) é ruim para podcast; use comercial (ElevenLabs) com tags de emoção
- Novembro/2025 (GPT 5.1 + Opus 4.5) marcou o ponto em que programar com agentes se tornou de fato viável
- A próxima corrida da indústria é otimização de energia/inferência (prompt caching, KV cache, deep thinking), não mais parâmetros
- Empresa que não treina juniores com seniores e depende de uma pessoa só é frágil; senior que não ensina não é senior

> **Deep dive:** `high` — Alta densidade de insight acionável com dados primários raros (300k linhas/500h, benchmark de 30 modelos, rankings pós-nov/2025) e relevância direta a agent-tooling, context-management de instruction files e evals de modelos, apesar do tom anedótico em partes.
