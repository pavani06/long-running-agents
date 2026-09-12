---
title: "Anthropic's CCA Exam as a Field-Guide for Agentic Engineering — Frank Coyle, UC Berkeley"
type: "extract"
source: "youtube"
video_id: "Z-c11pV_uvU"
url: "https://www.youtube.com/watch?v=Z-c11pV_uvU"
channel: "AI Engineer"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-anthropic-s-cca-exam-as-a-field-guide-for-agentic-engineering-frank-coyle-uc-ber--Z-c11pV_uvU.txt]]"
tags: ["agent-loop", "agent-tooling", "agents", "agentic-coding", "arquitetura", "context-engineering", "context-management", "curriculo-conteudo", "escalation", "multi-agent", "permissions", "token-budgeting", "production", "verification"]
thesis: "Frank Coyle defende que se preparar para o novo exame 'Claude Certified Architect' da Anthropic (cronometrado, proctorado, baseado em cenários de produção) é uma via prática para dominar os padrões e anti-padrões da IA agêntica — sobretudo tratamento de stop_reason no loop do agente, isolamento de contexto e especialização de sub-agentes."
concepts: ["anti-padrões (anti-patterns) em sistemas agentivos", "loop do agente (agentic loop) e stop_reason", "teorema de Böhm-Jacopini (sequência + condicional + loop = completude de Turing)", "CLAUDE.md hierárquico em três níveis", "especialização de sub-agentes", "isolamento de subtarefas (subtask isolation)", "groupthink entre agentes colaborativos", "compaction de contexto e limite de tokens", "batch mode para redução de custo", "human-in-the-loop e escalonamento por confiança", "Model Context Protocol (MCP)", "exame baseado em cenários de produção"]
tools: ["Claude Certified Architect exam", "Claude Code", "CLAUDE.md", "Model Context Protocol (MCP)", "batch mode (50% de desconto em tokens)", "algoritmos de compaction de contexto da Anthropic", "saída estruturada em JSON", "stop_reason"]
people: ["Frank Coyle", "UC Berkeley", "Anthropic", "Sister Corita Kent", "Thomas Edison", "Böhm e Jacopini", "Boris Cherny", "Peter Steinberger", "Sam Bwa (autor de livro sobre compressão customizada de contexto)", "John Coltrane"]
claims: ["Verificar sempre o stop_reason no loop do agente (tool_use, end_turn, max_tokens) e tratar respostas parciais causadas por esgotamento de tokens", "O LLM não executa ferramentas: ele é um preditor probabilístico que retorna parâmetros configurados, e seu código executa a ferramenta", "Estruturar o CLAUDE.md em três níveis hierárquicos (raiz do projeto, pasta do projeto, diretórios internos) para regras progressivas", "Especializar sub-agentes com uma ou duas ferramentas em vez de sobrecarregar um único agente com todas as ferramentas", "Evitar que o contexto de sub-agentes vaze para o contexto principal, pois mais contexto significa mais custo em tokens e mais confusão do modelo", "Passar ao agente crítico apenas claim e evidência (não o raciocínio original) para mitigar groupthink entre agentes", "Isolar saídas de subtarefas via fork e devolver apenas resumos ao contexto principal", "Monitorar a contagem de tokens e disparar compaction quando ultrapassar um limite (ex.: 150 mil tokens)", "É possível escrever lógica customizada de compressão de contexto estendendo uma classe base", "Nunca usar modos interativos/permissivos do Claude Code em pipelines de CI; configurar execução não-interativa ponta a ponta", "Usar batch mode para 50% de redução no custo de tokens, com resultado garantido em até 24 horas", "Incluir human-in-the-loop com checagem de confiança e escalonamento para humanos quando a confiança for baixa", "O exame custa US$99 para indivíduos, pode ser tentado a cada 6 meses, cobre 5 domínios (arquitetura agentiva 27%, Claude Code 20%, prompt engineering, design de ferramentas/MCP, gestão de contexto e confiabilidade) e sorteia 4 de 6 cenários de produção", "A combinação sequência + condicional + loop basta para completude de Turing (Böhm-Jacopini, 1966), o que explica por que loops são o núcleo do poder dos agentes"]
deep_dive: "medium"
deep_dive_reason: "Oferece anti-padrões acionáveis relevantes a harness e context-engineering (stop_reason, isolamento de contexto, compaction, batch mode), mas em tom introdutório de visão geral do exame, sem novidade arquitetural profunda."
---

# Anthropic's CCA Exam as a Field-Guide for Agentic Engineering — Frank Coyle, UC Berkeley

## Tese
Frank Coyle defende que se preparar para o novo exame 'Claude Certified Architect' da Anthropic (cronometrado, proctorado, baseado em cenários de produção) é uma via prática para dominar os padrões e anti-padrões da IA agêntica — sobretudo tratamento de stop_reason no loop do agente, isolamento de contexto e especialização de sub-agentes.

## Conceitos-chave
- anti-padrões (anti-patterns) em sistemas agentivos
- loop do agente (agentic loop) e stop_reason
- teorema de Böhm-Jacopini (sequência + condicional + loop = completude de Turing)
- CLAUDE.md hierárquico em três níveis
- especialização de sub-agentes
- isolamento de subtarefas (subtask isolation)
- groupthink entre agentes colaborativos
- compaction de contexto e limite de tokens
- batch mode para redução de custo
- human-in-the-loop e escalonamento por confiança
- Model Context Protocol (MCP)
- exame baseado em cenários de produção

## Ferramentas & pessoas
**Ferramentas:** Claude Certified Architect exam, Claude Code, CLAUDE.md, Model Context Protocol (MCP), batch mode (50% de desconto em tokens), algoritmos de compaction de contexto da Anthropic, saída estruturada em JSON, stop_reason

**Pessoas/orgs:** Frank Coyle, UC Berkeley, Anthropic, Sister Corita Kent, Thomas Edison, Böhm e Jacopini, Boris Cherny, Peter Steinberger, Sam Bwa (autor de livro sobre compressão customizada de contexto), John Coltrane

## Claims acionáveis
- Verificar sempre o stop_reason no loop do agente (tool_use, end_turn, max_tokens) e tratar respostas parciais causadas por esgotamento de tokens
- O LLM não executa ferramentas: ele é um preditor probabilístico que retorna parâmetros configurados, e seu código executa a ferramenta
- Estruturar o CLAUDE.md em três níveis hierárquicos (raiz do projeto, pasta do projeto, diretórios internos) para regras progressivas
- Especializar sub-agentes com uma ou duas ferramentas em vez de sobrecarregar um único agente com todas as ferramentas
- Evitar que o contexto de sub-agentes vaze para o contexto principal, pois mais contexto significa mais custo em tokens e mais confusão do modelo
- Passar ao agente crítico apenas claim e evidência (não o raciocínio original) para mitigar groupthink entre agentes
- Isolar saídas de subtarefas via fork e devolver apenas resumos ao contexto principal
- Monitorar a contagem de tokens e disparar compaction quando ultrapassar um limite (ex.: 150 mil tokens)
- É possível escrever lógica customizada de compressão de contexto estendendo uma classe base
- Nunca usar modos interativos/permissivos do Claude Code em pipelines de CI; configurar execução não-interativa ponta a ponta
- Usar batch mode para 50% de redução no custo de tokens, com resultado garantido em até 24 horas
- Incluir human-in-the-loop com checagem de confiança e escalonamento para humanos quando a confiança for baixa
- O exame custa US$99 para indivíduos, pode ser tentado a cada 6 meses, cobre 5 domínios (arquitetura agentiva 27%, Claude Code 20%, prompt engineering, design de ferramentas/MCP, gestão de contexto e confiabilidade) e sorteia 4 de 6 cenários de produção
- A combinação sequência + condicional + loop basta para completude de Turing (Böhm-Jacopini, 1966), o que explica por que loops são o núcleo do poder dos agentes

> **Deep dive:** `medium` — Oferece anti-padrões acionáveis relevantes a harness e context-engineering (stop_reason, isolamento de contexto, compaction, batch mode), mas em tom introdutório de visão geral do exame, sem novidade arquitetural profunda.
