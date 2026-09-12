---
title: "Why More Context Makes Your Agent Dumber and What to Do About It — Nupur Sharma, Qodo"
type: "extract"
source: "youtube"
video_id: "EcqMYoIV57A"
url: "https://www.youtube.com/watch?v=EcqMYoIV57A"
channel: "AI Engineer"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-why-more-context-makes-your-agent-dumber-and-what-to-do-about-it-nupur-sharma-qo--EcqMYoIV57A.txt]]"
tags: ["agents", "agent-fleets", "agent-loop", "multi-agent", "context-engineering", "context-management", "code-review", "gate-design", "model-selection", "token-budgeting", "arquitetura", "knowledge-management", "verification", "governanca", "production"]
thesis: "A confiabilidade de agentes em produção vem menos de janelas de contexto maiores e mais de otimização estratégica de contexto por agente, orquestração híbrida 80/20 com gates determinísticos e frotas de agentes especialistas filtradas por um judge agent."
concepts: ["Padrão em U de atenção (LLMs retêm início e fim, descartam o contexto do meio)", "Otimização estratégica de contexto vs. despejo de contexto", "Context engine (indexação + ranking com desafios de escala)", "Sumarização hierárquica por arquivo/pasta", "Grafo de conhecimento para dependências lógicas multi-repo", "Retrieval iterativo (índice tipo ficha de biblioteca)", "Self-correction com critic node", "Orchestration paradox (agente pesquisa métodos em vez de resolver o problema)", "Abordagem híbrida 80/20 (exploração livre + gates determinísticos)", "Counters e timeouts para quebrar loops de agente", "Mixture of agents (agentes especialistas atômicos)", "Judge agent (coerência e filtragem de relevância dos resultados)", "Contexto escopado por agente em vez de compartilhado", "Calibração via histórico de PRs e guidelines organizacionais", "Ponderação por aceitação do desenvolvedor (rules vs. bugs ponderados)"]
tools: ["Kodo", "LangChain", "Claude Opus", "MCP", "Jira"]
people: ["Nupur", "Kodo", "ISO", "SOC 2"]
claims: ["LLMs seguem uma 'curva U': processam o início e o fim do contexto e purgam o meio, então fornecer o codebase inteiro degrada resultados — valide empiricamente se o modelo usa o contexto fornecido", "Para times internos (não-produto) construindo agentes para processos próprios, retrieval iterativo tem o melhor trade-off: baixo input do desenvolvedor, bons resultados e custo por token maior", "Context engines escalam mal: com 600-700 repositórios o mapeamento e a indexação ficam lentos e imprevisíveis, então só vale construir se for o core do produto", "Sumarização hierárquica exige alto processamento LLM upfront e reindexação a cada mudança de arquivo; grafo de conhecimento exige alto input inicial do dev mas funciona bem com dependências lógicas multi-repo", "Quebre loops de pesquisa do agente com counters (aceitar o último resultado após 4-5 iterações) ou timeouts (ex.: 5 minutos) e seguir com o que existe", "Use modelos de alta capacidade de raciocínio nos 80% exploratórios (descoberta, planejamento, escolha de ferramenta) e modelos baratos/determinísticos nos 20% de validação e sumarização com hard gates (se X então Y)", "Evite um mega-agente multitarefa: ele se sobrecarrega e silenciosamente abandona tarefas (4 tarefas → foca em 2); prefira agentes especialistas pequenos por tarefa", "Adicione um judge agent que verifica se os resultados dos especialistas fazem sentido juntos e são relevantes ao objetivo original, podendo reconsultar o contexto antes de entregar", "Passe o histórico de PRs duas vezes: uma para calibrar a detecção dos sub-agentes e outra para o judge agent filtrar recomendações com base em como revisores/devs reagiram no passado", "Resultados organization-specific exigem que o cliente suba guidelines de arquitetura/compliance em um portal; sem isso o agente só entrega genérico out-of-the-box", "Classifique achados em 'rules' (sempre sinalizadas, independem de histórico) vs. 'bugs' ponderados: sugestões aceitas ganham peso futuro e rejeitadas repetidamente (~10x) perdem peso", "Use LangChain como camada de infraestrutura/comunicação entre agentes, com um agente dedicado a consolidar resultados e compor o prompt refinado do próximo agente"]
deep_dive: "high"
deep_dive_reason: "Densa em padrões arquiteturais acionáveis com trade-offs explícitos (roteamento de contexto por agente, gates determinísticos 80/20, quebra de loops com counters/timeouts, judge agent, ponderação por aceitação) diretamente relevantes a harness, context-engineering e agent-fleets, com novidade prática além do senso comum."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-no-vibes-allowed-solving-hard-problems-in-complex-codebases-dex-horthy-humanlaye--rmvDxxNubIg|No Vibes Allowed: Solving Hard Problems in Complex Codebases – Dex Horthy, HumanLayer]]", "[[extracts/youtube/ai-learning/2026-09-11-ex-nasa-dev-reveals-his-agentic-engineering-workflow--xgkjtF89-44|Ex-NASA dev reveals his Agentic Engineering Workflow]]", "[[extracts/youtube/ai-learning/2026-09-11-how-we-solved-context-management-in-agents-sally-ann-delucia--esY99nYXxR4|How we solved Context Management in Agents — Sally-Ann Delucia]]", "[[extracts/youtube/ai-learning/2026-09-11-the-best-ai-agents-need-less-code-than-you-think--YqjR4vQwbTc|The best AI agents need less code than you think]]", "[[extracts/youtube/ai-learning/2026-09-11-12-factor-agents-patterns-of-reliable-llm-applications-dex-horthy-humanlayer--8kMaTybvDUw|12-Factor Agents: Patterns of reliable LLM applications — Dex Horthy, HumanLayer]]", "[[extracts/youtube/ai-learning/2026-09-11-the-art-of-loop-engineering-how-to-build-agents-that-improve-over-time--jPPiZ22DY3g|The Art of Loop Engineering: How to Build Agents That Improve Over Time]]", "[[extracts/youtube/ai-learning/2026-09-11-inside-cogent-s-three-agent-architecture-for-autonomous-defense-geng-sng-co-foun--D6XWu54oG4g|Inside Cogent's three-agent architecture for autonomous defense | Geng Sng (Co-founder, Cogent)]]", "[[extracts/youtube/ai-learning/2026-09-11-how-uber-built-ai-agents-that-save-21-000-developer-hours-with-langgraph-langcha--Bugs0dVcNI8|How Uber Built AI Agents That Save 21,000 Developer Hours with LangGraph | LangChain Interrupt]]", "[[extracts/youtube/ai-learning/2026-09-11-why-we-killed-our-multi-agent-pipeline-subbiah-sethuraman-and-abhilash-asokan-zs--u6jJcIFDLE4|Why We Killed Our Multi-Agent Pipeline — Subbiah Sethuraman and Abhilash Asokan, ZS Associates]]", "[[extracts/youtube/ai-learning/2026-09-11-context-graphs-for-explainable-decision-aware-ai-agents-andreas-kollegger-zaid-z--abvQEhvRI_c|Context Graphs for Explainable, Decision-Aware AI Agents — Andreas Kollegger & Zaid Zaim, Neo4j]]", "[[extracts/youtube/ai-learning/2026-09-11-why-your-agents-need-decision-traces-not-just-documents-zach-blumenfeld-neo4j--B9h9ovW5H9U|Why your agents need decision traces, not just documents — Zach Blumenfeld, Neo4j]]", "[[extracts/youtube/ai-learning/2026-09-11-i-want-llama3-to-perform-10x-with-my-private-knowledge-local-agentic-rag-w-llama--u5Vcrwpzoz8|\"I want Llama3 to perform 10x with my private knowledge\" - Local Agentic RAG w/ llama3]]", "[[extracts/youtube/ai-learning/2026-09-11-benchmarking-semantic-code-retrieval-on-claude-code-kuba-rogut-turbopuffer--zKk7sDMGDEQ|Benchmarking semantic code retrieval on Claude Code — Kuba Rogut, Turbopuffer]]"]
---

# Why More Context Makes Your Agent Dumber and What to Do About It — Nupur Sharma, Qodo

## Tese
A confiabilidade de agentes em produção vem menos de janelas de contexto maiores e mais de otimização estratégica de contexto por agente, orquestração híbrida 80/20 com gates determinísticos e frotas de agentes especialistas filtradas por um judge agent.

## Conceitos-chave
- Padrão em U de atenção (LLMs retêm início e fim, descartam o contexto do meio)
- Otimização estratégica de contexto vs. despejo de contexto
- Context engine (indexação + ranking com desafios de escala)
- Sumarização hierárquica por arquivo/pasta
- Grafo de conhecimento para dependências lógicas multi-repo
- Retrieval iterativo (índice tipo ficha de biblioteca)
- Self-correction com critic node
- Orchestration paradox (agente pesquisa métodos em vez de resolver o problema)
- Abordagem híbrida 80/20 (exploração livre + gates determinísticos)
- Counters e timeouts para quebrar loops de agente
- Mixture of agents (agentes especialistas atômicos)
- Judge agent (coerência e filtragem de relevância dos resultados)
- Contexto escopado por agente em vez de compartilhado
- Calibração via histórico de PRs e guidelines organizacionais
- Ponderação por aceitação do desenvolvedor (rules vs. bugs ponderados)

## Ferramentas & pessoas
**Ferramentas:** Kodo, LangChain, Claude Opus, MCP, Jira

**Pessoas/orgs:** Nupur, Kodo, ISO, SOC 2

## Claims acionáveis
- LLMs seguem uma 'curva U': processam o início e o fim do contexto e purgam o meio, então fornecer o codebase inteiro degrada resultados — valide empiricamente se o modelo usa o contexto fornecido
- Para times internos (não-produto) construindo agentes para processos próprios, retrieval iterativo tem o melhor trade-off: baixo input do desenvolvedor, bons resultados e custo por token maior
- Context engines escalam mal: com 600-700 repositórios o mapeamento e a indexação ficam lentos e imprevisíveis, então só vale construir se for o core do produto
- Sumarização hierárquica exige alto processamento LLM upfront e reindexação a cada mudança de arquivo; grafo de conhecimento exige alto input inicial do dev mas funciona bem com dependências lógicas multi-repo
- Quebre loops de pesquisa do agente com counters (aceitar o último resultado após 4-5 iterações) ou timeouts (ex.: 5 minutos) e seguir com o que existe
- Use modelos de alta capacidade de raciocínio nos 80% exploratórios (descoberta, planejamento, escolha de ferramenta) e modelos baratos/determinísticos nos 20% de validação e sumarização com hard gates (se X então Y)
- Evite um mega-agente multitarefa: ele se sobrecarrega e silenciosamente abandona tarefas (4 tarefas → foca em 2); prefira agentes especialistas pequenos por tarefa
- Adicione um judge agent que verifica se os resultados dos especialistas fazem sentido juntos e são relevantes ao objetivo original, podendo reconsultar o contexto antes de entregar
- Passe o histórico de PRs duas vezes: uma para calibrar a detecção dos sub-agentes e outra para o judge agent filtrar recomendações com base em como revisores/devs reagiram no passado
- Resultados organization-specific exigem que o cliente suba guidelines de arquitetura/compliance em um portal; sem isso o agente só entrega genérico out-of-the-box
- Classifique achados em 'rules' (sempre sinalizadas, independem de histórico) vs. 'bugs' ponderados: sugestões aceitas ganham peso futuro e rejeitadas repetidamente (~10x) perdem peso
- Use LangChain como camada de infraestrutura/comunicação entre agentes, com um agente dedicado a consolidar resultados e compor o prompt refinado do próximo agente

> **Deep dive:** `high` — Densa em padrões arquiteturais acionáveis com trade-offs explícitos (roteamento de contexto por agente, gates determinísticos 80/20, quebra de loops com counters/timeouts, judge agent, ponderação por aceitação) diretamente relevantes a harness, context-engineering e agent-fleets, com novidade prática além do senso comum.
