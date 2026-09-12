---
title: "The best AI agents are simpler than you think"
type: "extract"
source: "youtube"
video_id: "uCKhOmth2ms"
url: "https://www.youtube.com/watch?v=uCKhOmth2ms"
channel: "LangChain"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-the-best-ai-agents-are-simpler-than-you-think--uCKhOmth2ms.txt]]"
tags: ["harness", "context-engineering", "model-selection", "evals", "multi-agent", "agent-loop", "agent-tooling", "arquitetura", "governanca", "production", "classification", "data-platform", "knowledge-management", "decision-discipline", "stack-tooling", "agents", "runtime"]
thesis: "Sierra sustenta que o comércio agentic superará o e-commerce e, para viabilizá-lo, construiu uma plataforma de experiência do cliente com harness de voz de baixíssima latência que orquestra constelações de 10-15 modelos por turno, uma camada no-code (Journeys) que compila isomorficamente para código, infraestrutura isolada de pagamentos (PCI DSS Nível 1) e engenharia de contexto como disciplina central."
concepts: ["comércio agentic (agentic commerce)", "constelação de modelos por turno de conversa", "compilação determinística e isomórfica no-code <-> código", "execução especulativa e paralelismo em agentes de voz", "ensembling de transcrição (decisão por silêncio entre dois modelos)", "trade-off latência-qualidade-custo", "progressive disclosure de contexto", "compacção de prompt sem incoerência", "evals como base para troca e hill climbing de modelos", "preço baseado em resultado (comissão sobre vendas)", "agente autor (Ghostwriter) escrevendo Journeys em vez de código", "Agent Data Platform: dados estruturados + conversa não estruturada", "risco de regurgitação em fine-tuning/RL", "enviando o organograma (quando multi-agente espelha a estrutura de times)", "abstrações amigáveis aos modelos (sistema de arquivos, git, diffs)", "isolamento de infraestrutura de pagamento (PCI DSS Nível 1)", "governança de release e change management para Fortune 20", "MCP: agente como cliente e servidor (ChatGPT apps)", "evolução de fluxos rígidos para regras declarativas raciocinadas pelo modelo", "modelos in-house para recuperação/reranking de conhecimento"]
tools: ["Sierra", "Agent OS", "Agent SDK", "Journeys", "Ghostwriter", "Explorer", "Agent Studio", "Agent Data Platform", "MCP (Model Context Protocol)", "ChatGPT apps", "Codex", "Claude Code", "LangGraph", "deep agents (pacote novo)", "Redfin AI search", "Shopify", "Stripe", "Sentry", "Alexa", "modelos Claude/Gemini/GPT"]
people: ["Zach Renault Wedin (head of product, Sierra)", "Sierra", "OpenAI", "Anthropic", "Google", "Redfin", "Fortune 20/50/100 (base de clientes)"]
claims: ["10-15 modelos distintos podem ser invocados por turno de conversa, misturando modelos de fronteira, classificadores baratos e modelos in-house especializados", "Journeys compila determinística e isomorficamente para código do Agent SDK, permitindo ida e volta entre no-code e código como se fossem o mesmo artefato", "A compilação não-determinística de texto livre para especificação de agentes gerou mais mal do que bem nos experimentos da Sierra; prefira DSL declarativa para times de operações", "Encontre os modelos onde eles estão (~80% do tempo): materialize tudo em sistema de arquivos, git e diffs para os agentes codificarem; invista em ensinar novas abstrações só em casos especiais", "Em voz é preciso responder em 1-2 segundos; paralelize pensar/ouvir/falar e use execução especulativa (buscar respostas antes de saber se precisará delas)", "Rode dois transcritores em paralelo: se o modelo que alucina em silêncio sinaliza silêncio, confie nele; caso contrário, confie no outro", "Nenhum provedor de LLM é certificado PCI; isole a infraestrutura de pagamento em cluster separado para que dados de cartão nunca cheguem a um LLM externo", "Engenharia de contexto é mostrar ao agente tudo de que ele precisa e nada mais; conforme os modelos melhoram, pode-se ser menos preciso", "Não insira contexto no prompt antes de ser relevante e, ao compactar, evite histórico incoerente com o system prompt (causa comum de alucinações)", "Sempre que parecer que o modelo é burro, o problema provavelmente é seu (prompt/contexto mal construído)", "Prompt caching é bom para velocidade e custo, mas a qualidade vem primeiro; não invalidar o cache sem motivo, mas sem fanatismo", "Evals robustos tornam a troca entre modelos de inteligência comparável basicamente um trade-off de latência/qualidade/custo; a primeira migração revela que o eval era mais fraco do que se pensava", "Nunca fine-tune em dados cuja regurgitação seria problemática; e RL frequentemente é erro de arredondamento frente ao avanço dos modelos de fronteira em 3-6 meses", "O suporte multi-provedor da Sierra foi impulsionado por capacidade (picos de Black Friday/Cyber Monday) e não só por custo, com load tests na escala de bilhões de conversas por ano", "Em sistemas multi-agente, se a motivação é apenas times separados trabalhando em agentes separados, você está enviando seu organograma", "O SDK evoluiu de fluxos rígidos (colete o e-mail antes de confirmar) para pré-requisitos declarados como regras da jornada que o modelo raciocina como cumprir", "Comunicação agente-a-agente mais comum é chamada de API direta (economiza tokens e garante precisão); MCP e A2A são suportados, inclusive agentes Sierra como servidores MCP para ChatGPT apps", "Ghostwriter (autoria) e Explorer (análise) convergem para um harness compartilhado especialista no Agent Studio, com arquitetura semelhante a Claude Code/Codex para loops longos de análise"]
deep_dive: "high"
deep_dive_reason: "Alta densidade de detalhes arquiteturais novos e acionáveis sobre harness de voz, constelação de modelos, execução especulativa, compilação isomórfica no-code-código, isolamento PCI e engenharia de contexto, diretamente relevantes a harness, context-engineering, evals, model-selection e governança."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-the-agent-development-life-cycle-zack-reneau-wedeen-sierra--0vBKv9yAQi4|The Agent Development Life Cycle — Zack Reneau-Wedeen, Sierra]]", "[[extracts/youtube/ai-learning/2026-09-11-the-future-of-ai-agents-what-will-interrupt-2027-look-like-interrupt-26--R9K2574YEAg|The Future of AI Agents: What Will Interrupt 2027 Look Like? | Interrupt 26]]", "[[extracts/youtube/ai-learning/2026-09-11-l8-principal-s-agentic-engineering-setup-just-copy-him--8ZgpAXe5V5w|L8 Principal's Agentic Engineering Setup (just copy him)]]", "[[extracts/youtube/ai-learning/2026-09-11-how-to-understand-the-next-wave-of-ai-before-everyone-else-tibo-interview--4qjEgPojjzM|How to Understand the Next Wave of AI Before Everyone Else | Tibo Interview]]", "[[extracts/youtube/ai-learning/2026-09-11-how-to-build-your-entire-ai-workforce-in-one-afternoon-live-demo--oulVKbk0umo|How to Build Your Entire AI Workforce in One Afternoon (Live Demo)]]", "[[extracts/youtube/ai-learning/2026-09-11-the-future-of-ai-agents-with-andrew-ng-interrupt-26--OaRhpwz_TGM|The Future of AI Agents with Andrew Ng | Interrupt 26]]", "[[extracts/youtube/ai-learning/2026-09-11-build-an-agent-in-10-mins-with-ai-sdk-5-with-nico-albanese-from-vercel-ai-demo-d--TjAbtsPC-Sw|Build An Agent in 10 mins with AI SDK 5 with Nico Albanese from Vercel, AI Demo Days]]"]
---

# The best AI agents are simpler than you think

## Tese
Sierra sustenta que o comércio agentic superará o e-commerce e, para viabilizá-lo, construiu uma plataforma de experiência do cliente com harness de voz de baixíssima latência que orquestra constelações de 10-15 modelos por turno, uma camada no-code (Journeys) que compila isomorficamente para código, infraestrutura isolada de pagamentos (PCI DSS Nível 1) e engenharia de contexto como disciplina central.

## Conceitos-chave
- comércio agentic (agentic commerce)
- constelação de modelos por turno de conversa
- compilação determinística e isomórfica no-code <-> código
- execução especulativa e paralelismo em agentes de voz
- ensembling de transcrição (decisão por silêncio entre dois modelos)
- trade-off latência-qualidade-custo
- progressive disclosure de contexto
- compacção de prompt sem incoerência
- evals como base para troca e hill climbing de modelos
- preço baseado em resultado (comissão sobre vendas)
- agente autor (Ghostwriter) escrevendo Journeys em vez de código
- Agent Data Platform: dados estruturados + conversa não estruturada
- risco de regurgitação em fine-tuning/RL
- enviando o organograma (quando multi-agente espelha a estrutura de times)
- abstrações amigáveis aos modelos (sistema de arquivos, git, diffs)
- isolamento de infraestrutura de pagamento (PCI DSS Nível 1)
- governança de release e change management para Fortune 20
- MCP: agente como cliente e servidor (ChatGPT apps)
- evolução de fluxos rígidos para regras declarativas raciocinadas pelo modelo
- modelos in-house para recuperação/reranking de conhecimento

## Ferramentas & pessoas
**Ferramentas:** Sierra, Agent OS, Agent SDK, Journeys, Ghostwriter, Explorer, Agent Studio, Agent Data Platform, MCP (Model Context Protocol), ChatGPT apps, Codex, Claude Code, LangGraph, deep agents (pacote novo), Redfin AI search, Shopify, Stripe, Sentry, Alexa, modelos Claude/Gemini/GPT

**Pessoas/orgs:** Zach Renault Wedin (head of product, Sierra), Sierra, OpenAI, Anthropic, Google, Redfin, Fortune 20/50/100 (base de clientes)

## Claims acionáveis
- 10-15 modelos distintos podem ser invocados por turno de conversa, misturando modelos de fronteira, classificadores baratos e modelos in-house especializados
- Journeys compila determinística e isomorficamente para código do Agent SDK, permitindo ida e volta entre no-code e código como se fossem o mesmo artefato
- A compilação não-determinística de texto livre para especificação de agentes gerou mais mal do que bem nos experimentos da Sierra; prefira DSL declarativa para times de operações
- Encontre os modelos onde eles estão (~80% do tempo): materialize tudo em sistema de arquivos, git e diffs para os agentes codificarem; invista em ensinar novas abstrações só em casos especiais
- Em voz é preciso responder em 1-2 segundos; paralelize pensar/ouvir/falar e use execução especulativa (buscar respostas antes de saber se precisará delas)
- Rode dois transcritores em paralelo: se o modelo que alucina em silêncio sinaliza silêncio, confie nele; caso contrário, confie no outro
- Nenhum provedor de LLM é certificado PCI; isole a infraestrutura de pagamento em cluster separado para que dados de cartão nunca cheguem a um LLM externo
- Engenharia de contexto é mostrar ao agente tudo de que ele precisa e nada mais; conforme os modelos melhoram, pode-se ser menos preciso
- Não insira contexto no prompt antes de ser relevante e, ao compactar, evite histórico incoerente com o system prompt (causa comum de alucinações)
- Sempre que parecer que o modelo é burro, o problema provavelmente é seu (prompt/contexto mal construído)
- Prompt caching é bom para velocidade e custo, mas a qualidade vem primeiro; não invalidar o cache sem motivo, mas sem fanatismo
- Evals robustos tornam a troca entre modelos de inteligência comparável basicamente um trade-off de latência/qualidade/custo; a primeira migração revela que o eval era mais fraco do que se pensava
- Nunca fine-tune em dados cuja regurgitação seria problemática; e RL frequentemente é erro de arredondamento frente ao avanço dos modelos de fronteira em 3-6 meses
- O suporte multi-provedor da Sierra foi impulsionado por capacidade (picos de Black Friday/Cyber Monday) e não só por custo, com load tests na escala de bilhões de conversas por ano
- Em sistemas multi-agente, se a motivação é apenas times separados trabalhando em agentes separados, você está enviando seu organograma
- O SDK evoluiu de fluxos rígidos (colete o e-mail antes de confirmar) para pré-requisitos declarados como regras da jornada que o modelo raciocina como cumprir
- Comunicação agente-a-agente mais comum é chamada de API direta (economiza tokens e garante precisão); MCP e A2A são suportados, inclusive agentes Sierra como servidores MCP para ChatGPT apps
- Ghostwriter (autoria) e Explorer (análise) convergem para um harness compartilhado especialista no Agent Studio, com arquitetura semelhante a Claude Code/Codex para loops longos de análise

> **Deep dive:** `high` — Alta densidade de detalhes arquiteturais novos e acionáveis sobre harness de voz, constelação de modelos, execução especulativa, compilação isomórfica no-code-código, isolamento PCI e engenharia de contexto, diretamente relevantes a harness, context-engineering, evals, model-selection e governança.
