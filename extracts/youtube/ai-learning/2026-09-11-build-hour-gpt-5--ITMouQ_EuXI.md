---
title: "Build Hour: GPT-5"
type: "extract"
source: "youtube"
video_id: "ITMouQ_EuXI"
url: "https://www.youtube.com/watch?v=ITMouQ_EuXI"
channel: "OpenAI"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-build-hour-gpt-5--ITMouQ_EuXI.txt]]"
tags: ["agentic-coding", "agents", "agent-loop", "agent-tooling", "arquitetura", "context-engineering", "state", "evals", "code-review", "model-selection", "testes-qa", "verification", "monitoramento", "production"]
thesis: "O GPT-5 usado via Responses API habilita agentes de codificação autônomos mais coerentes em tarefas longas ao persistir reasoning items entre chamadas de ferramenta, com steerability (reasoning effort, verbosity, preambles e prompts precisos) determinando ganhos mensuráveis de produção."
concepts: ["Responses API stateful (v2 da Completions API)", "reasoning items / chain-of-thought tokens repassados após tool calls", "reasoning.encrypted_content para orgs ZDR com store=false", "reasoning effort minimal (latência de modelo não-reasoning)", "custom tools / function calling em texto livre", "parâmetro verbosity (afeta saída final e tool calls)", "prompt caching baseado em prefixo inclui reasoning items", "metaprompting (perguntar 'porquê' antes de corrigir o prompt)", "controle de agentic eagerness (persistência vs. profundidade de busca)", "tool preambles (plano e narrativa antes de cada tool call)", "formatação de prompt em XML testada como a melhor", "agent loop com ferramenta única de bash em VM", "apply patch tool para edição eficiente de código", "recuperação de falhas de testes pelo modelo", "LLM-as-judge para avaliação head-to-head de agentes", "agent slider / coerência em horizontes longos", "loop construir-testar-iterar como futuro do web dev"]
tools: ["GPT-5", "OpenAI Responses API", "Completions API", "Codex", "Codex CLI", "OpenAI Playground", "Prompt Optimizer", "Prompt Optimization Cookbook", "MCP servers", "Runloop", "ripgrep", "apply patch tool", "GitHub", "Linear", "Slack", "Cursor", "Windsurf", "OpenAI o3", "Claude Opus 4.1", "Claude Code"]
people: ["OpenAI", "Christine", "Bill", "Eric", "Anoop", "Riley", "Charlie Labs", "Andrej Karpathy", "Alex"]
claims: ["Use a Responses API (não a Completions API) com GPT-5 e repasse os reasoning items após cada tool call: em tarefas agentic de 20-50 chamadas isso rende 2-4% em benchmarks tipo SWE-bench.", "Para orgs ZDR, use store=false com reasoning.encrypted_content para manter os benefícios dos reasoning items sem estado no servidor.", "Reasoning items fazem parte do prefixo de prompt caching, então repassá-los melhora cache: mais barato, mais inteligente e mais rápido.", "reasoning effort minimal entrega a inteligência do GPT-5 com latência próxima à de modelo não-reasoning (demo: 0.9s vs 6.9s com high).", "Custom tools permitem tool calls em texto livre, eliminando o escaping de JSON em agentes de codificação.", "verbosity high produz código mais legível com melhor error handling e funciona bem em casos de agentic coding; experimente por use case.", "Comece com reasoning effort medium; use low para tarefas sensíveis a latência e high (+ verbosity high) para tarefas agentic longas.", "Elimine instruções conflitantes/imprecisas: GPT-5 interpreta literalmente e conflitos degradam performance visivelmente nos reasoning summaries.", "XML superou Markdown/JSON/YAML nos testes internos de estruturação de prompts para GPT-5.", "Metaprompting: pergunte ao modelo por que exibiu um comportamento e só então peça a correção baseada nas razões, em vez de patches pontuais que overfitam o prompt.", "Adicione prompts de persistência para o modelo completar tarefas ponta a ponta; limite a profundidade de busca (ex.: máximo 2 tool calls em vez de 8) para reduzir eagerness excessivo.", "Prompte preambles de ferramenta (estado o objetivo, plano estruturado, narrar cada passo) para monitorar e abortar workflows que descarrilem.", "Deixe espaço explícito para planejamento e auto-reflexão; o modelo já faz isso bem (checklists no Codex).", "Arquitetura da Charlie Labs: agent loop com ferramenta única de bash em VM Runloop (setup TypeScript), ripgrep para contexto, apply patch para edição, execução de testes, commit e PR — com GPT-5 recuperando-se bem de testes falhando.", "O web search tool hospedado foi um add simples que aumentou bastante os resultados do agente.", "Evals da Charlie Labs: +16% sobre o3 no eval de criação de PR (mesmo prompt), +29% após otimização; +5% sobre o3 em PR review; Claude Opus 4.1 foi 46% pior; Charlie venceu 10/10 contra Claude Code via LLM-as-judge.", "Verbosity é o maior desafio da Charlie Labs com GPT-5, exigindo controle ativo."]
deep_dive: "high"
deep_dive_reason: "Alta densidade de insight acionável e arquitetural — mecânica dos reasoning items, statefulness/caching da Responses API, steerability (reasoning effort, verbosity, preambles), playbook de prompting com dados e um harness de agente de produção com evals quantificados (16-29% sobre o3, head-to-head vs. Claude Code)."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-5-simple-but-weird-chatgpt-5-tricks-to-get-a-10x-better-response--emV9Wo_UuGQ|5 simple (but weird) ChatGPT-5 tricks to get a 10x better response]]", "[[extracts/youtube/ai-learning/2026-09-11-openai-just-destroyed-ai-coding-codex-2-0--C06FBVXMLCY|OpenAI just destroyed AI coding… Codex 2.0]]", "[[extracts/youtube/ai-learning/2026-09-11-boris-cherny-we-cut-80-of-claude-codes-prompt--qyPCVqFUyDo|Boris Cherny: We Cut 80% of Claude Code’s Prompt]]", "[[extracts/youtube/ai-learning/2026-09-11-the-prompting-playbook--G2B0YWuJUgI|The prompting playbook]]", "[[extracts/youtube/ai-learning/2026-09-11-anthropic-workshop-build-agents-that-run-for-hours-ash-prabaker-andrew-wilson--mR-WAvEPRwE|Anthropic Workshop: Build Agents That Run for Hours — Ash Prabaker & Andrew Wilson]]", "[[extracts/youtube/ai-learning/2026-09-11-gpt-6-astra-fable-5-1-god-mode--KgKA0A3qlz0|GPT 6 Astra + Fable 5.1 = GOD MODE]]", "[[extracts/youtube/ai-learning/2026-09-11-coding-with-openai-o1-in-cursor-can-we-replace-claude-3-5-now--wwC86t5k77Y|Coding With OpenAI-o1 in Cursor - Can We Replace Claude 3.5 Now?]]", "[[extracts/youtube/ai-learning/2026-09-11-how-did-we-make-deepseek-outperform-opus-4-7--f61DCDwvFis|how did we make deepseek outperform opus 4.7?]]", "[[extracts/youtube/ai-learning/2026-09-11-i-trained-a-reasoning-language-model-with-rl-on-an-unverifiable-task--kxypcfrkUBI|I trained a Reasoning Language Model with RL on an unverifiable task]]", "[[extracts/youtube/ai-learning/2026-09-11-gpt-builder-2-0-upgrade-custom-gpt-with-parallel-function-calling-advanced-gpts--kBFjvQxKnOs|GPT Builder 2.0 🚀 UPGRADE Custom GPT with Parallel Function Calling 🤯 Advanced GPTs Tutorial]]"]
---

# Build Hour: GPT-5

## Tese
O GPT-5 usado via Responses API habilita agentes de codificação autônomos mais coerentes em tarefas longas ao persistir reasoning items entre chamadas de ferramenta, com steerability (reasoning effort, verbosity, preambles e prompts precisos) determinando ganhos mensuráveis de produção.

## Conceitos-chave
- Responses API stateful (v2 da Completions API)
- reasoning items / chain-of-thought tokens repassados após tool calls
- reasoning.encrypted_content para orgs ZDR com store=false
- reasoning effort minimal (latência de modelo não-reasoning)
- custom tools / function calling em texto livre
- parâmetro verbosity (afeta saída final e tool calls)
- prompt caching baseado em prefixo inclui reasoning items
- metaprompting (perguntar 'porquê' antes de corrigir o prompt)
- controle de agentic eagerness (persistência vs. profundidade de busca)
- tool preambles (plano e narrativa antes de cada tool call)
- formatação de prompt em XML testada como a melhor
- agent loop com ferramenta única de bash em VM
- apply patch tool para edição eficiente de código
- recuperação de falhas de testes pelo modelo
- LLM-as-judge para avaliação head-to-head de agentes
- agent slider / coerência em horizontes longos
- loop construir-testar-iterar como futuro do web dev

## Ferramentas & pessoas
**Ferramentas:** GPT-5, OpenAI Responses API, Completions API, Codex, Codex CLI, OpenAI Playground, Prompt Optimizer, Prompt Optimization Cookbook, MCP servers, Runloop, ripgrep, apply patch tool, GitHub, Linear, Slack, Cursor, Windsurf, OpenAI o3, Claude Opus 4.1, Claude Code

**Pessoas/orgs:** OpenAI, Christine, Bill, Eric, Anoop, Riley, Charlie Labs, Andrej Karpathy, Alex

## Claims acionáveis
- Use a Responses API (não a Completions API) com GPT-5 e repasse os reasoning items após cada tool call: em tarefas agentic de 20-50 chamadas isso rende 2-4% em benchmarks tipo SWE-bench.
- Para orgs ZDR, use store=false com reasoning.encrypted_content para manter os benefícios dos reasoning items sem estado no servidor.
- Reasoning items fazem parte do prefixo de prompt caching, então repassá-los melhora cache: mais barato, mais inteligente e mais rápido.
- reasoning effort minimal entrega a inteligência do GPT-5 com latência próxima à de modelo não-reasoning (demo: 0.9s vs 6.9s com high).
- Custom tools permitem tool calls em texto livre, eliminando o escaping de JSON em agentes de codificação.
- verbosity high produz código mais legível com melhor error handling e funciona bem em casos de agentic coding; experimente por use case.
- Comece com reasoning effort medium; use low para tarefas sensíveis a latência e high (+ verbosity high) para tarefas agentic longas.
- Elimine instruções conflitantes/imprecisas: GPT-5 interpreta literalmente e conflitos degradam performance visivelmente nos reasoning summaries.
- XML superou Markdown/JSON/YAML nos testes internos de estruturação de prompts para GPT-5.
- Metaprompting: pergunte ao modelo por que exibiu um comportamento e só então peça a correção baseada nas razões, em vez de patches pontuais que overfitam o prompt.
- Adicione prompts de persistência para o modelo completar tarefas ponta a ponta; limite a profundidade de busca (ex.: máximo 2 tool calls em vez de 8) para reduzir eagerness excessivo.
- Prompte preambles de ferramenta (estado o objetivo, plano estruturado, narrar cada passo) para monitorar e abortar workflows que descarrilem.
- Deixe espaço explícito para planejamento e auto-reflexão; o modelo já faz isso bem (checklists no Codex).
- Arquitetura da Charlie Labs: agent loop com ferramenta única de bash em VM Runloop (setup TypeScript), ripgrep para contexto, apply patch para edição, execução de testes, commit e PR — com GPT-5 recuperando-se bem de testes falhando.
- O web search tool hospedado foi um add simples que aumentou bastante os resultados do agente.
- Evals da Charlie Labs: +16% sobre o3 no eval de criação de PR (mesmo prompt), +29% após otimização; +5% sobre o3 em PR review; Claude Opus 4.1 foi 46% pior; Charlie venceu 10/10 contra Claude Code via LLM-as-judge.
- Verbosity é o maior desafio da Charlie Labs com GPT-5, exigindo controle ativo.

> **Deep dive:** `high` — Alta densidade de insight acionável e arquitetural — mecânica dos reasoning items, statefulness/caching da Responses API, steerability (reasoning effort, verbosity, preambles), playbook de prompting com dados e um harness de agente de produção com evals quantificados (16-29% sobre o3, head-to-head vs. Claude Code).
