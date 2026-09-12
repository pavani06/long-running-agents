---
title: "How We Build Effective Agents: Barry Zhang, Anthropic"
type: "extract"
source: "youtube"
video_id: "D7_ipDqhtwk"
url: "https://www.youtube.com/watch?v=D7_ipDqhtwk"
channel: "AI Engineer"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-how-we-build-effective-agents-barry-zhang-anthropic--D7_ipDqhtwk.txt]]"
tags: ["agents", "agent-loop", "context-engineering", "context-management", "token-budgeting", "multi-agent", "agentic-coding", "error-handling", "verification", "decision-discipline", "permissions", "arquitetura", "production"]
thesis: "Agentes devem ser construídos apenas para tarefas complexas, valiosas e verificáveis, mantidos na forma mais simples possível (modelo + ferramentas em loop) e iterados adotando a perspectiva do contexto limitado do próprio agente."
concepts: ["Distinção entre workflows (fluxo de controle predefinido) e agentes (trajetória autodecidida com feedback do ambiente)", "Agente como 'modelo usando ferramentas em um loop'", "Três componentes fundamentais: ambiente, conjunto de ferramentas e system prompt", "Checklist de quando construir um agente: complexidade da tarefa, valor, derisking de capacidades críticas, custo e descobribilidade de erros", "Economia de tokens: orçamento de ~US$0,10 por tarefa equivale a 30-50 mil tokens", "Coding como caso de uso ideal por ter saída verificável (unit tests, CI)", "Empatia de contexto: operar apenas com os 10-20k tokens que o agente vê", "Usar o próprio modelo para auditar prompts, descrições de ferramentas e trajetórias", "Otimizações pós-iteração: cache de trajetória, paralelização de tool calls, apresentação de progresso para confiança do usuário", "Agentes budget-aware (orçamentos de tempo, dinheiro e tokens)", "Ferramentas autoevolutivas: meta-tool para o agente desenhar sua própria ergonomia de ferramentas", "Colaboração multi-agente com sub-agentes protegendo a context window do agente principal", "Comunicação assíncrona entre agentes como questão aberta além do turno síncrono usuário-assistente"]
tools: ["Claude (referido como 'cloud' na transcrição)", "MCP (Model Context Protocol)", "Unit tests / CI como mecanismo de verificação", "Blog post 'Building Effective Agents'"]
people: ["Barry (palestrante, co-autor do blog post)", "Erik/Eric (co-autor)", "Anthropic (implícita, equipe de go-to-market e autores do blog)", "Mahes (workshop de MCP)", "swyx ('Swix', autor do post sobre 'first AI engineer')", "Meta", "AI Engineer Summit"]
claims: ["Se a árvore de decisão da tarefa é mapeável, construa um workflow explícito e otimize cada nó em vez de usar um agente", "Verifique se o valor da tarefa justifica o custo de exploração em tokens (ex.: orçamento de US$0,10 só permite 30-50k tokens)", "Antes de escalar, deriske capacidades críticas (ex.: coding agent deve escrever, debugar e se recuperar de erros) pois gargalos multiplicam custo e latência", "Mitigue erros de alto risco limitando escopo: acesso somente leitura e human-in-the-loop", "Prefira casos de uso com saída facilmente verificável, como código validado por unit tests e CI", "Construa primeiro apenas os três componentes (ambiente, ferramentas, prompt) e otimize depois (cache de trajetória, tool calls paralelas, UI de progresso)", "Faça uma tarefa completa da perspectiva do agente (ex.: só screenshot estático + descrição) para descobrir quais informações de contexto faltam", "Restrinja-se aos 10-20k tokens do contexto do agente para avaliar se ele é suficiente e coerente", "Cole o system prompt e descrições de ferramentas no Claude para detectar ambiguidade e ajustar parâmetros", "Jogue a trajetória completa do agente no Claude e pergunte por que decisões foram tomadas e o que ajudaria", "Defina e imponha orçamentos (tempo, dinheiro, tokens) como pré-requisito para implantar agentes em produção", "Generalize a iteração assistida por modelo de descrições de ferramenta em uma meta-tool onde agentes melhoram sua própria ergonomia de ferramentas", "Use sub-agentes para proteger a context window do agente principal em cenários multi-agente", "Projete comunicação assíncrona entre agentes em vez de depender apenas de turnos síncronos usuário-assistente"]
deep_dive: "medium"
deep_dive_reason: "Oferece heurísticas acionáveis (checklist de uso, orçamento em tokens, auditoria de contexto pelo próprio modelo) relevantes a context-engineering e agent-loop, mas é essencialmente um recap da visão já amplamente difundida do blog 'Building Effective Agents', com profundidade arquitetural limitada."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-build-systems-not-code-angie-jones-agentic-ai-foundation--ZD9-4fW2HhM|Build Systems, Not Code - Angie Jones, Agentic AI Foundation]]", "[[extracts/youtube/ai-learning/2026-09-11-12-factor-agents-patterns-of-reliable-llm-applications-dex-horthy-humanlayer--8kMaTybvDUw|12-Factor Agents: Patterns of reliable LLM applications — Dex Horthy, HumanLayer]]", "[[extracts/youtube/ai-learning/2026-09-11-ex-nasa-dev-reveals-his-agentic-engineering-workflow--xgkjtF89-44|Ex-NASA dev reveals his Agentic Engineering Workflow]]", "[[extracts/youtube/ai-learning/2026-09-11-tool-skill-or-subagent-decomposing-an-agent-that-outgrew-its-prompt--mWvtOHlZM-I|Tool, skill, or subagent? Decomposing an agent that outgrew its prompt]]", "[[extracts/youtube/ai-learning/2026-09-11-l8-principal-s-agentic-engineering-setup-just-copy-him--8ZgpAXe5V5w|L8 Principal's Agentic Engineering Setup (just copy him)]]", "[[extracts/youtube/ai-learning/2026-09-11-how-i-deleted-95-of-my-agent-skills-and-got-better-results-nick-nisi-workos--vy7o1g2iHY8|How I deleted 95% of my agent skills and got better results — Nick Nisi, WorkOS]]", "[[extracts/youtube/ai-learning/2026-09-11-building-agent-interfaces-lessons-from-chrome-devtools-mcp-for-agents-michael-ha--_B4Pv9ttFgY|Building Agent Interfaces: Lessons from Chrome DevTools (MCP) for Agents — Michael Hablich, Google]]", "[[extracts/youtube/ai-learning/2026-09-11-anthropic-s-cca-exam-as-a-field-guide-for-agentic-engineering-frank-coyle-uc-ber--Z-c11pV_uvU|Anthropic's CCA Exam as a Field-Guide for Agentic Engineering — Frank Coyle, UC Berkeley]]"]
---

# How We Build Effective Agents: Barry Zhang, Anthropic

## Tese
Agentes devem ser construídos apenas para tarefas complexas, valiosas e verificáveis, mantidos na forma mais simples possível (modelo + ferramentas em loop) e iterados adotando a perspectiva do contexto limitado do próprio agente.

## Conceitos-chave
- Distinção entre workflows (fluxo de controle predefinido) e agentes (trajetória autodecidida com feedback do ambiente)
- Agente como 'modelo usando ferramentas em um loop'
- Três componentes fundamentais: ambiente, conjunto de ferramentas e system prompt
- Checklist de quando construir um agente: complexidade da tarefa, valor, derisking de capacidades críticas, custo e descobribilidade de erros
- Economia de tokens: orçamento de ~US$0,10 por tarefa equivale a 30-50 mil tokens
- Coding como caso de uso ideal por ter saída verificável (unit tests, CI)
- Empatia de contexto: operar apenas com os 10-20k tokens que o agente vê
- Usar o próprio modelo para auditar prompts, descrições de ferramentas e trajetórias
- Otimizações pós-iteração: cache de trajetória, paralelização de tool calls, apresentação de progresso para confiança do usuário
- Agentes budget-aware (orçamentos de tempo, dinheiro e tokens)
- Ferramentas autoevolutivas: meta-tool para o agente desenhar sua própria ergonomia de ferramentas
- Colaboração multi-agente com sub-agentes protegendo a context window do agente principal
- Comunicação assíncrona entre agentes como questão aberta além do turno síncrono usuário-assistente

## Ferramentas & pessoas
**Ferramentas:** Claude (referido como 'cloud' na transcrição), MCP (Model Context Protocol), Unit tests / CI como mecanismo de verificação, Blog post 'Building Effective Agents'

**Pessoas/orgs:** Barry (palestrante, co-autor do blog post), Erik/Eric (co-autor), Anthropic (implícita, equipe de go-to-market e autores do blog), Mahes (workshop de MCP), swyx ('Swix', autor do post sobre 'first AI engineer'), Meta, AI Engineer Summit

## Claims acionáveis
- Se a árvore de decisão da tarefa é mapeável, construa um workflow explícito e otimize cada nó em vez de usar um agente
- Verifique se o valor da tarefa justifica o custo de exploração em tokens (ex.: orçamento de US$0,10 só permite 30-50k tokens)
- Antes de escalar, deriske capacidades críticas (ex.: coding agent deve escrever, debugar e se recuperar de erros) pois gargalos multiplicam custo e latência
- Mitigue erros de alto risco limitando escopo: acesso somente leitura e human-in-the-loop
- Prefira casos de uso com saída facilmente verificável, como código validado por unit tests e CI
- Construa primeiro apenas os três componentes (ambiente, ferramentas, prompt) e otimize depois (cache de trajetória, tool calls paralelas, UI de progresso)
- Faça uma tarefa completa da perspectiva do agente (ex.: só screenshot estático + descrição) para descobrir quais informações de contexto faltam
- Restrinja-se aos 10-20k tokens do contexto do agente para avaliar se ele é suficiente e coerente
- Cole o system prompt e descrições de ferramentas no Claude para detectar ambiguidade e ajustar parâmetros
- Jogue a trajetória completa do agente no Claude e pergunte por que decisões foram tomadas e o que ajudaria
- Defina e imponha orçamentos (tempo, dinheiro, tokens) como pré-requisito para implantar agentes em produção
- Generalize a iteração assistida por modelo de descrições de ferramenta em uma meta-tool onde agentes melhoram sua própria ergonomia de ferramentas
- Use sub-agentes para proteger a context window do agente principal em cenários multi-agente
- Projete comunicação assíncrona entre agentes em vez de depender apenas de turnos síncronos usuário-assistente

> **Deep dive:** `medium` — Oferece heurísticas acionáveis (checklist de uso, orçamento em tokens, auditoria de contexto pelo próprio modelo) relevantes a context-engineering e agent-loop, mas é essencialmente um recap da visão já amplamente difundida do blog 'Building Effective Agents', com profundidade arquitetural limitada.
