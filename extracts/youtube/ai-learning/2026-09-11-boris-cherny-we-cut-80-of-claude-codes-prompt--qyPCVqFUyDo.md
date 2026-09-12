---
title: "Boris Cherny: We Cut 80% of Claude Code’s Prompt"
type: "extract"
source: "youtube"
video_id: "qyPCVqFUyDo"
url: "https://www.youtube.com/watch?v=qyPCVqFUyDo"
channel: "Y Combinator"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-boris-cherny-we-cut-80-of-claude-codes-prompt--qyPCVqFUyDo.txt]]"
tags: ["harness-engineering", "evals", "agentic-coding", "agent-fleets", "multi-agent", "context-engineering", "verification", "model-selection", "runtime", "testes-qa", "production", "permissions", "agent-loop", "context-management"]
thesis: "Com Opus 5, construir produtos agênticos tornou-se uma ciência empírica de 'desobstruir' o modelo: deletar e reconstruir prompts/harness via ablação a cada geração de modelo, dar tarefas mais difíceis com mecanismos de verificação, e explorar o 'product overhang' orquestrando milhares de agentes (dynamic workflows, loops/routines) para elicitar capacidades latentes."
concepts: ["Ablação de system prompt (deletar e reconstruir linha a linha como eval)", "Product overhang vs hobbling (capacidades do modelo não realizadas por produtos que atrapalham)", "Dynamic workflows como nova forma de test-time compute e 'álgebra de agentes' (sequência/paralelo, milhares de agentes em sandbox Bun/VM)", "Loops e routines (cron local vs em nuvem) para manutenção autônoma de codebases pela própria Claude", "Verificação como elemento mais importante do design de tarefas (test suites, screenshots pixel a pixel em VM)", "Resistência a prompt injection via três camadas: alinhamento + classificador baseado em interpretabilidade mecanicista (neurônios) + classificador de auto mode", "Deletar CLAUDE.md, skills e hooks a cada novo modelo e só readicionar instruções após falhas repetidas", "Evals vivem 1-3 gerações de modelo até saturar, então são descartados e recriados", "Elicitation gap: capacidades não treinadas descobertas por experimentação (ex: desenhar com OpenCV)", "Dar tarefas de alto nível com guardrails e critérios de saída em vez de instruções passo a passo (unlearning da sobrespecificação)", "Agentes de longa duração: tarefas rodando dias/semanas/meses sem scaffolding", "Automanutenção de código: rotinas diárias de dead code, shipping de experimentos, cobertura de testes e 'abstraction police'"]
tools: ["Claude Code", "Opus 5", "Sonnet 3.5", "Arc AGI 3", "CLAUDE_CODE_SIMPLE=1", "CLAUDE.md", "dynamic workflows", "loops", "routines", "Claude Tag (Claude no Slack)", "Claude desktop app (Electron)", "Swift", "Bun", "Zig", "Rust", "Node.js", "GitHub Actions (macOS runner/VM)", "OpenCV", "MCP", "Slack", "auto mode classifier", "prompt injection classifier", "TI-83 (BASIC e assembly)"]
people: ["Boris Cherny (criador do Claude Code)", "Anthropic", "Chris Olah (interpretabilidade mecanicista)", "Bun team / Jared", "Y Combinator (público do evento)"]
claims: ["A cada novo modelo, delete o system prompt inteiro e reconstrua por ablação, reintroduzindo linha a linha para medir o impacto de cada instrução", "A cada ~6 meses delete CLAUDE.md, skills e hooks e teste o que o novo modelo faz sem eles antes de readicionar", "Use CLAUDE_CODE_SIMPLE=1 como ablação: remove todos os prompts (inclusive das tools) e o modelo pode ficar até mais inteligente", "Evals devem ser continuamente anexados e mantidos até saturarem; tipicamente vivem apenas 1-3 gerações de modelo", "Dê tarefas um nível acima do que você acha que o modelo consegue, descrevendo tarefa, guardrails e critérios de saída, e deixe o modelo trabalhar", "Projete verificação do trabalho (test suites, screenshots, análise estática/dinâmica) como o componente central de qualquer tarefa agêntica difícil", "Basta dizer 'use a workflow' no Claude Code para disparar dynamic workflows que orquestram dezenas a milhares de agentes em sequência e paralelo", "O runtime Bun foi reescrito de Zig para Rust pelo modelo em 11 dias, com steering humano, verificado por test suites, e está em produção no Claude Code", "Rewrite do app desktop Electron→Swift roda há 2+ semanas comparando screenshots pixel a pixel em VM macOS no GitHub, com a Claude postando progresso num canal Slack", "Use loops (cron local) e routines (cron em nuvem) para tarefas repetitivas; a Anthropic roda 20-30 rotinas diárias onde a Claude mantém seus próprios apps (dead code, experimentos, testes, unificação de abstrações)", "Reataque problemas antigos com cada novo modelo: a tarefa impossível na geração anterior pode funcionar agora (elicitation gap)", "Opus 5 combinaado com auto mode roda dias/semanas/meses sem scaffolding e não é mais prompt-injetável observável, via três camadas de defesa", "Todo o harness do Claude Code se reescreve a cada modelo; o código restante é majoritariamente segurança, permissões, análise estática e UI", "Há dezenas/centenas de capacidades não comercializadas nos modelos atuais (ex: desenho com OpenCV) esperando produtos que as elicitem", "Coding 'resolvido' não é universal: o modelo ainda falha em sistemas profundos, sistemas distribuídos e verificação pixel-perfect de UI", "A mentalidade vencedora é empírica: esqueça priors de modelos antigos, observe falhas reais e itere; não siga influenciadores ou truques únicos"]
deep_dive: "high"
deep_dive_reason: "Densidade alta de insight acionável e arquitetural inédito sobre harness-engineering (ablação de prompts), evals (saturação por geração), agent-fleets (dynamic workflows, loops/routines com milhares de agentes) e elicitação via verificação, direto do criador do Claude Code no lançamento do Opus 5."
---

# Boris Cherny: We Cut 80% of Claude Code’s Prompt

## Tese
Com Opus 5, construir produtos agênticos tornou-se uma ciência empírica de 'desobstruir' o modelo: deletar e reconstruir prompts/harness via ablação a cada geração de modelo, dar tarefas mais difíceis com mecanismos de verificação, e explorar o 'product overhang' orquestrando milhares de agentes (dynamic workflows, loops/routines) para elicitar capacidades latentes.

## Conceitos-chave
- Ablação de system prompt (deletar e reconstruir linha a linha como eval)
- Product overhang vs hobbling (capacidades do modelo não realizadas por produtos que atrapalham)
- Dynamic workflows como nova forma de test-time compute e 'álgebra de agentes' (sequência/paralelo, milhares de agentes em sandbox Bun/VM)
- Loops e routines (cron local vs em nuvem) para manutenção autônoma de codebases pela própria Claude
- Verificação como elemento mais importante do design de tarefas (test suites, screenshots pixel a pixel em VM)
- Resistência a prompt injection via três camadas: alinhamento + classificador baseado em interpretabilidade mecanicista (neurônios) + classificador de auto mode
- Deletar CLAUDE.md, skills e hooks a cada novo modelo e só readicionar instruções após falhas repetidas
- Evals vivem 1-3 gerações de modelo até saturar, então são descartados e recriados
- Elicitation gap: capacidades não treinadas descobertas por experimentação (ex: desenhar com OpenCV)
- Dar tarefas de alto nível com guardrails e critérios de saída em vez de instruções passo a passo (unlearning da sobrespecificação)
- Agentes de longa duração: tarefas rodando dias/semanas/meses sem scaffolding
- Automanutenção de código: rotinas diárias de dead code, shipping de experimentos, cobertura de testes e 'abstraction police'

## Ferramentas & pessoas
**Ferramentas:** Claude Code, Opus 5, Sonnet 3.5, Arc AGI 3, CLAUDE_CODE_SIMPLE=1, CLAUDE.md, dynamic workflows, loops, routines, Claude Tag (Claude no Slack), Claude desktop app (Electron), Swift, Bun, Zig, Rust, Node.js, GitHub Actions (macOS runner/VM), OpenCV, MCP, Slack, auto mode classifier, prompt injection classifier, TI-83 (BASIC e assembly)

**Pessoas/orgs:** Boris Cherny (criador do Claude Code), Anthropic, Chris Olah (interpretabilidade mecanicista), Bun team / Jared, Y Combinator (público do evento)

## Claims acionáveis
- A cada novo modelo, delete o system prompt inteiro e reconstrua por ablação, reintroduzindo linha a linha para medir o impacto de cada instrução
- A cada ~6 meses delete CLAUDE.md, skills e hooks e teste o que o novo modelo faz sem eles antes de readicionar
- Use CLAUDE_CODE_SIMPLE=1 como ablação: remove todos os prompts (inclusive das tools) e o modelo pode ficar até mais inteligente
- Evals devem ser continuamente anexados e mantidos até saturarem; tipicamente vivem apenas 1-3 gerações de modelo
- Dê tarefas um nível acima do que você acha que o modelo consegue, descrevendo tarefa, guardrails e critérios de saída, e deixe o modelo trabalhar
- Projete verificação do trabalho (test suites, screenshots, análise estática/dinâmica) como o componente central de qualquer tarefa agêntica difícil
- Basta dizer 'use a workflow' no Claude Code para disparar dynamic workflows que orquestram dezenas a milhares de agentes em sequência e paralelo
- O runtime Bun foi reescrito de Zig para Rust pelo modelo em 11 dias, com steering humano, verificado por test suites, e está em produção no Claude Code
- Rewrite do app desktop Electron→Swift roda há 2+ semanas comparando screenshots pixel a pixel em VM macOS no GitHub, com a Claude postando progresso num canal Slack
- Use loops (cron local) e routines (cron em nuvem) para tarefas repetitivas; a Anthropic roda 20-30 rotinas diárias onde a Claude mantém seus próprios apps (dead code, experimentos, testes, unificação de abstrações)
- Reataque problemas antigos com cada novo modelo: a tarefa impossível na geração anterior pode funcionar agora (elicitation gap)
- Opus 5 combinaado com auto mode roda dias/semanas/meses sem scaffolding e não é mais prompt-injetável observável, via três camadas de defesa
- Todo o harness do Claude Code se reescreve a cada modelo; o código restante é majoritariamente segurança, permissões, análise estática e UI
- Há dezenas/centenas de capacidades não comercializadas nos modelos atuais (ex: desenho com OpenCV) esperando produtos que as elicitem
- Coding 'resolvido' não é universal: o modelo ainda falha em sistemas profundos, sistemas distribuídos e verificação pixel-perfect de UI
- A mentalidade vencedora é empírica: esqueça priors de modelos antigos, observe falhas reais e itere; não siga influenciadores ou truques únicos

> **Deep dive:** `high` — Densidade alta de insight acionável e arquitetural inédito sobre harness-engineering (ablação de prompts), evals (saturação por geração), agent-fleets (dynamic workflows, loops/routines com milhares de agentes) e elicitação via verificação, direto do criador do Claude Code no lançamento do Opus 5.
