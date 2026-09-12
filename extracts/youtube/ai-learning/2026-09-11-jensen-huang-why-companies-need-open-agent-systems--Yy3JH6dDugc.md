---
title: "Jensen Huang: Why companies need open agent systems"
type: "extract"
source: "youtube"
video_id: "Yy3JH6dDugc"
url: "https://www.youtube.com/watch?v=Yy3JH6dDugc"
channel: "LangChain"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-jensen-huang-why-companies-need-open-agent-systems--Yy3JH6dDugc.txt]]"
tags: ["agents", "agent-fleets", "agent-tooling", "arquitetura", "context-engineering", "evals", "frameworks", "governanca", "harness", "harness-engineering", "memory-architecture", "model-selection", "multi-agent", "permissions", "runtime", "stack-tooling"]
thesis: "Jensen Huang argumenta que, com modelos open-weight quase de fronteira (Nemotron 3 Ultra) combinados a harnesses abertos (LangChain Deep Agents), runtimes seguros (OpenShell) e pós-treinamento do modelo contra o harness, toda empresa pode construir 'super agentes' proprietários e especializados no domínio — e que no futuro as empresas serão construídas sobre harnesses, não sobre processos de negócio."
concepts: ["harness em torno do LLM", "super agentes especializados por domínio", "modelos open-weight vs. modelos de fronteira", "sub-agentes para tarefas específicas (otimização de supply chain, floorplanning de chips)", "pós-treinamento do modelo contra o harness", "afinamento do harness por modelo (prompts e ferramentas distintos por modelo)", "flywheel de uso e melhoria contínua", "memória de trabalho e de longo prazo, compaction, knowledge graphs, RAG", "guardrails e safeguards", "evals e benchmarks conduzidos por especialistas de domínio", "sandbox, controle de acesso e segurança no runtime de agentes", "blueprints de implantação de agentes", "inteligência barata e rápida permite explorar maior espaço de busca e achar melhores respostas", "demanda massiva por tokens/inteligência subestimada", "analogia de RH/onboarding para implantação de agentes (permissões, ferramentas, contexto, skills file)", "governança, confiança e controle empresarial sobre agentes"]
tools: ["LangChain", "LangChain Deep Agents", "Nemotron 3 Ultra", "Claude Code", "Codex", "OpenClaw", "OpenShell", "NVIDIA Blueprints (NemoClaw)", "DGX Spark", "DGX Station", "Claude Opus", "DeepSeek", "MiniMax"]
people: ["Jensen Huang", "NVIDIA", "LangChain", "Anthropic", "OpenAI", "Google", "Nemotron Coalition", "DeepSeek", "MiniMax"]
claims: ["Nemotron 3 Ultra dentro de Deep Agents atinge 86% em benchmark interno, contra 87% do Claude Opus e 82–83% de DeepSeek e MiniMax, evidenciando que modelos open-weight recentes alcançam performance quase de fronteira", "Nemotron 3 Ultra custa cerca de 10x menos que o Opus, e inteligência barata e rápida permite ao agente iterar por um espaço de busca maior e encontrar respostas melhores", "Diferentes modelos precisam de prompts e ferramentas diferentes: ajustar o harness ao modelo específico eleva significativamente o desempenho do sistema", "Estratégia recomendada para empresas: começar com modelos de fronteira (Claude Code, Codex) e só especializar com harness aberto + open weights quando o modelo estiver 'bom o suficiente'", "Pós-treinar o modelo dentro/para o harness na tarefa específica eleva o teto do sistema completo — capacidade que não existia antes", "Construa sub-agentes especializados de propósito único (ex.: otimização de supply chain, floorplanning de chip design) com Deep Agents + Nemotron conectados a conhecimento e ferramentas proprietárias", "Sem resolver sandbox, controle de acesso e segurança, é impossível implantar agentes: trate o onboarding do agente como RH (permissões por função, ferramentas, acesso a dados, documento de missão/skills)", "Mais uso de IA aumenta contratações: engenheiros de software migram de escrever código para construir agentes, evals, benchmarks e guardrails", "Empresas são coleções de workflows proprietários; no futuro serão construídas sobre harnesses, com frameworks como LangChain funcionando como o 'sistema operacional da empresa'", "Foi anunciado um blueprint com Deep Agents + OpenShell + Nemotron 3 Ultra para empresas implantarem agentes em cloud, on-prem, DGX Spark ou DGX Station", "Inteligência proprietária de domínio não deve ser terceirizada — a exigência de stacks abertos vem do controle sobre conhecimento e processos que definem a identidade da empresa"]
deep_dive: "medium"
deep_dive_reason: "Contém pontos acionáveis e relevantes (números de benchmark, custo 10x, tuning de harness por modelo, pós-treinamento contra o harness, analogia de RH para permissões de agentes), mas é uma conversa de evento com tom acentuadamente promocional e sem profundidade arquitetural ou novidade técnica que justifique o tier alto."
---

# Jensen Huang: Why companies need open agent systems

## Tese
Jensen Huang argumenta que, com modelos open-weight quase de fronteira (Nemotron 3 Ultra) combinados a harnesses abertos (LangChain Deep Agents), runtimes seguros (OpenShell) e pós-treinamento do modelo contra o harness, toda empresa pode construir 'super agentes' proprietários e especializados no domínio — e que no futuro as empresas serão construídas sobre harnesses, não sobre processos de negócio.

## Conceitos-chave
- harness em torno do LLM
- super agentes especializados por domínio
- modelos open-weight vs. modelos de fronteira
- sub-agentes para tarefas específicas (otimização de supply chain, floorplanning de chips)
- pós-treinamento do modelo contra o harness
- afinamento do harness por modelo (prompts e ferramentas distintos por modelo)
- flywheel de uso e melhoria contínua
- memória de trabalho e de longo prazo, compaction, knowledge graphs, RAG
- guardrails e safeguards
- evals e benchmarks conduzidos por especialistas de domínio
- sandbox, controle de acesso e segurança no runtime de agentes
- blueprints de implantação de agentes
- inteligência barata e rápida permite explorar maior espaço de busca e achar melhores respostas
- demanda massiva por tokens/inteligência subestimada
- analogia de RH/onboarding para implantação de agentes (permissões, ferramentas, contexto, skills file)
- governança, confiança e controle empresarial sobre agentes

## Ferramentas & pessoas
**Ferramentas:** LangChain, LangChain Deep Agents, Nemotron 3 Ultra, Claude Code, Codex, OpenClaw, OpenShell, NVIDIA Blueprints (NemoClaw), DGX Spark, DGX Station, Claude Opus, DeepSeek, MiniMax

**Pessoas/orgs:** Jensen Huang, NVIDIA, LangChain, Anthropic, OpenAI, Google, Nemotron Coalition, DeepSeek, MiniMax

## Claims acionáveis
- Nemotron 3 Ultra dentro de Deep Agents atinge 86% em benchmark interno, contra 87% do Claude Opus e 82–83% de DeepSeek e MiniMax, evidenciando que modelos open-weight recentes alcançam performance quase de fronteira
- Nemotron 3 Ultra custa cerca de 10x menos que o Opus, e inteligência barata e rápida permite ao agente iterar por um espaço de busca maior e encontrar respostas melhores
- Diferentes modelos precisam de prompts e ferramentas diferentes: ajustar o harness ao modelo específico eleva significativamente o desempenho do sistema
- Estratégia recomendada para empresas: começar com modelos de fronteira (Claude Code, Codex) e só especializar com harness aberto + open weights quando o modelo estiver 'bom o suficiente'
- Pós-treinar o modelo dentro/para o harness na tarefa específica eleva o teto do sistema completo — capacidade que não existia antes
- Construa sub-agentes especializados de propósito único (ex.: otimização de supply chain, floorplanning de chip design) com Deep Agents + Nemotron conectados a conhecimento e ferramentas proprietárias
- Sem resolver sandbox, controle de acesso e segurança, é impossível implantar agentes: trate o onboarding do agente como RH (permissões por função, ferramentas, acesso a dados, documento de missão/skills)
- Mais uso de IA aumenta contratações: engenheiros de software migram de escrever código para construir agentes, evals, benchmarks e guardrails
- Empresas são coleções de workflows proprietários; no futuro serão construídas sobre harnesses, com frameworks como LangChain funcionando como o 'sistema operacional da empresa'
- Foi anunciado um blueprint com Deep Agents + OpenShell + Nemotron 3 Ultra para empresas implantarem agentes em cloud, on-prem, DGX Spark ou DGX Station
- Inteligência proprietária de domínio não deve ser terceirizada — a exigência de stacks abertos vem do controle sobre conhecimento e processos que definem a identidade da empresa

> **Deep dive:** `medium` — Contém pontos acionáveis e relevantes (números de benchmark, custo 10x, tuning de harness por modelo, pós-treinamento contra o harness, analogia de RH para permissões de agentes), mas é uma conversa de evento com tom acentuadamente promocional e sem profundidade arquitetural ou novidade técnica que justifique o tier alto.
