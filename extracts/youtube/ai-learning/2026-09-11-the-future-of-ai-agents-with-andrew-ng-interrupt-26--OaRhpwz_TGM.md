---
title: "The Future of AI Agents with Andrew Ng | Interrupt 26"
type: "extract"
source: "youtube"
video_id: "OaRhpwz_TGM"
url: "https://www.youtube.com/watch?v=OaRhpwz_TGM"
channel: "LangChain"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-the-future-of-ai-agents-with-andrew-ng-interrupt-26--OaRhpwz_TGM.txt]]"
tags: ["agentic-coding", "agents", "agent-tooling", "context-engineering", "knowledge-management", "model-selection", "data-platform", "governanca", "permissions", "evals", "observability", "decision-discipline", "process", "stack-tooling", "arquitetura", "instituicoes", "curriculo-conteudo"]
thesis: "Com agentes de codificação acelerando a construção de software em 10-100x, a vantagem competitiva migra para equipes pequenas de generalistas altamente capacitados, redesenho top-down de workflows completos (não automação pontual), contexto/documentação fresca para agentes, re-arquitetura de dados não estruturados e preservação de opcionalidade de vendors."
concepts: ["product management bottleneck (e todos os demais gargalos: marketing, jurídico, design)", "equipes pequenas (1-10) de generalistas de alto contexto e altamente empoderados dentro de guardrails amplos", "princípio do pombal de papéis (múltiplas funções por humano em equipes enxutas)", "mental model de building blocks / bricks de LEGO combinatórios (blocos de IA: RAG, frameworks de agentes, evals, guardrails; blocos não-IA: UI, identidade, persistência)", "limitação de knowledge cutoff de coding agents em APIs muito novas", "Context Hub como 'Stack Overflow para agentes de IA'", "educação como conversa interativa: vídeo simulado interrompível e demos em JavaScript clicáveis em vez de vídeo estático", "inovação bottom-up ('mil flores') vs. movimento top-down com escopo amplo", "exemplo de underwriting de empréstimo: produto 'aprovado em 10 minutos' via redesenho do workflow inteiro", "economia de custos vs. direcionamento a crescimento (sem teto prático)", "metas incrementais (2%) forçam apenas trabalhar mais; metas transformadoras (20-50%) forçam criatividade", "portfólio de poucas apostas bem financiadas após análise técnica + de negócios", "forward deployed engineers (FDEs) e suas habilidades (evals, observabilidade, change management, pushback técnico)", "neutralidade de vendors e valor da opcionalidade em contratos", "modelos open-weight persistentemente 6-9 meses atrás da fronteira", "arquitetura de dados AI-ready/agent-ready para dados não estruturados (texto, imagem, PDF, áudio, vídeo)", "permissões desenhadas para humanos, não para agentes (herança de permissões por agentes)", "schema-on-read: NoSQL para iteração rápida de prototipagem vs. relacional em produção de larga escala"]
tools: ["Claude Code", "OpenAI Codex", "Gemini CLI", "OpenCode", "Context Hub (Rohit Prasad/Andrew Ng)", "Context Hub (LangChain)", "CodeDream.ai", "LangSmith", "MongoDB", "nano-banana (API)", "cursos DeepLearning.AI/Coursera"]
people: ["Andrew Ng", "Rohit Prasad", "Chris Tann", "Harrison Chase", "Aaron", "CJ", "DeepLearning.AI", "Coursera", "AI Fund", "AI Aspire", "LangChain", "OpenAI", "Casa Branca/administração americana"]
claims: ["Combine inovação bottom-up com um movimento top-down de alguém com escopo amplo para redesenhar o workflow completo (ex.: empréstimo aprovado em 10 minutos), visando crescimento em vez de apenas eficiência incremental", "Monte equipes de 1-10 engenheiros generalistas de alto contexto, altamente empoderados, que também redijam copy de marketing e primeiros rascunhos de termos de serviço com apoio de IA", "Domine um portfólio amplo de building blocks (RAG, frameworks, evals, guardrails, UI, identidade, persistência) e use coding agents para montá-los combinatoriamente", "Injete documentação atualizada nos coding agents via Context Hub porque eles não conhecem APIs lançadas após o knowledge cutoff (ex.: nano-banana)", "Preserve opcionalidade de vendors: quase nunca assine contratos superiores a um ano independentemente dos descontos, pois o modelo/agent líder muda rápido; prefira ferramentas neutras como LangSmith e questione se FDEs de um único vendor reduzem sua opcionalidade", "Use modelos open-weight (por vezes fine-tunados) para muitos casos de uso, pois ficam ~6-9 meses atrás da fronteira a custo muito menor; defenda open source/open weight para preservar opcionalidade", "Re-arquitete dados não estruturados (PDFs, texto, áudio, vídeo) para entregá-los aos agentes no momento e lugar certos; espere projetos de dezenas a centenas de milhões de dólares para tornar dados AI-ready, enfrentando fragmentação, ausência de schema consensual, permissões desenhadas para humanos e lacunas de governança/observabilidade", "Prefira NoSQL (MongoDB) com schema-on-read na prototipagem rápida para evitar o custo de migrações de schema; migre para bancos relacionais/escaláveis apenas em workloads de produção muito grandes", "Estabeleça metas transformadoras (20-50% de crescimento) em vez de incrementais (2%), pois metas grandes forçam soluções criativas em vez de apenas trabalhar mais", "Filtre portfólios massivos de ideias (ex.: planilha com 300 itens) via análise técnica e de negócios combinadas até um punhado de apostas com capital significativo, alocadas top-down", "Valorize FDEs embutidos por acelerarem projetos (entendimento de negócio, evals, observabilidade, change management, pushback sobre inviabilidade técnica), mas planeje ter muitos mais engenheiros de IA internos do que FDEs", "Transforme educação de cursos para conversas interativas (CodeDream.ai): apresentador de IA interrompível e demos em JavaScript clicáveis no lugar de vídeo/slides estáticos", "Use agentic coding para baratear radicalmente prototipagem e experimentação, mas reconheça que a alocação de recursos ainda exige decisão top-down de portfólio"]
deep_dive: "medium"
deep_dive_reason: "Oferece várias teses acionáveis e relevantes (permissões para agentes, arquitetura de dados não estruturados, opcionalidade de vendors, desenho de equipes), mas é um chat estratégico de alto nível, com trechos promocionais e sem profundidade técnica ou arquitetural detalhada."
---

# The Future of AI Agents with Andrew Ng | Interrupt 26

## Tese
Com agentes de codificação acelerando a construção de software em 10-100x, a vantagem competitiva migra para equipes pequenas de generalistas altamente capacitados, redesenho top-down de workflows completos (não automação pontual), contexto/documentação fresca para agentes, re-arquitetura de dados não estruturados e preservação de opcionalidade de vendors.

## Conceitos-chave
- product management bottleneck (e todos os demais gargalos: marketing, jurídico, design)
- equipes pequenas (1-10) de generalistas de alto contexto e altamente empoderados dentro de guardrails amplos
- princípio do pombal de papéis (múltiplas funções por humano em equipes enxutas)
- mental model de building blocks / bricks de LEGO combinatórios (blocos de IA: RAG, frameworks de agentes, evals, guardrails; blocos não-IA: UI, identidade, persistência)
- limitação de knowledge cutoff de coding agents em APIs muito novas
- Context Hub como 'Stack Overflow para agentes de IA'
- educação como conversa interativa: vídeo simulado interrompível e demos em JavaScript clicáveis em vez de vídeo estático
- inovação bottom-up ('mil flores') vs. movimento top-down com escopo amplo
- exemplo de underwriting de empréstimo: produto 'aprovado em 10 minutos' via redesenho do workflow inteiro
- economia de custos vs. direcionamento a crescimento (sem teto prático)
- metas incrementais (2%) forçam apenas trabalhar mais; metas transformadoras (20-50%) forçam criatividade
- portfólio de poucas apostas bem financiadas após análise técnica + de negócios
- forward deployed engineers (FDEs) e suas habilidades (evals, observabilidade, change management, pushback técnico)
- neutralidade de vendors e valor da opcionalidade em contratos
- modelos open-weight persistentemente 6-9 meses atrás da fronteira
- arquitetura de dados AI-ready/agent-ready para dados não estruturados (texto, imagem, PDF, áudio, vídeo)
- permissões desenhadas para humanos, não para agentes (herança de permissões por agentes)
- schema-on-read: NoSQL para iteração rápida de prototipagem vs. relacional em produção de larga escala

## Ferramentas & pessoas
**Ferramentas:** Claude Code, OpenAI Codex, Gemini CLI, OpenCode, Context Hub (Rohit Prasad/Andrew Ng), Context Hub (LangChain), CodeDream.ai, LangSmith, MongoDB, nano-banana (API), cursos DeepLearning.AI/Coursera

**Pessoas/orgs:** Andrew Ng, Rohit Prasad, Chris Tann, Harrison Chase, Aaron, CJ, DeepLearning.AI, Coursera, AI Fund, AI Aspire, LangChain, OpenAI, Casa Branca/administração americana

## Claims acionáveis
- Combine inovação bottom-up com um movimento top-down de alguém com escopo amplo para redesenhar o workflow completo (ex.: empréstimo aprovado em 10 minutos), visando crescimento em vez de apenas eficiência incremental
- Monte equipes de 1-10 engenheiros generalistas de alto contexto, altamente empoderados, que também redijam copy de marketing e primeiros rascunhos de termos de serviço com apoio de IA
- Domine um portfólio amplo de building blocks (RAG, frameworks, evals, guardrails, UI, identidade, persistência) e use coding agents para montá-los combinatoriamente
- Injete documentação atualizada nos coding agents via Context Hub porque eles não conhecem APIs lançadas após o knowledge cutoff (ex.: nano-banana)
- Preserve opcionalidade de vendors: quase nunca assine contratos superiores a um ano independentemente dos descontos, pois o modelo/agent líder muda rápido; prefira ferramentas neutras como LangSmith e questione se FDEs de um único vendor reduzem sua opcionalidade
- Use modelos open-weight (por vezes fine-tunados) para muitos casos de uso, pois ficam ~6-9 meses atrás da fronteira a custo muito menor; defenda open source/open weight para preservar opcionalidade
- Re-arquitete dados não estruturados (PDFs, texto, áudio, vídeo) para entregá-los aos agentes no momento e lugar certos; espere projetos de dezenas a centenas de milhões de dólares para tornar dados AI-ready, enfrentando fragmentação, ausência de schema consensual, permissões desenhadas para humanos e lacunas de governança/observabilidade
- Prefira NoSQL (MongoDB) com schema-on-read na prototipagem rápida para evitar o custo de migrações de schema; migre para bancos relacionais/escaláveis apenas em workloads de produção muito grandes
- Estabeleça metas transformadoras (20-50% de crescimento) em vez de incrementais (2%), pois metas grandes forçam soluções criativas em vez de apenas trabalhar mais
- Filtre portfólios massivos de ideias (ex.: planilha com 300 itens) via análise técnica e de negócios combinadas até um punhado de apostas com capital significativo, alocadas top-down
- Valorize FDEs embutidos por acelerarem projetos (entendimento de negócio, evals, observabilidade, change management, pushback sobre inviabilidade técnica), mas planeje ter muitos mais engenheiros de IA internos do que FDEs
- Transforme educação de cursos para conversas interativas (CodeDream.ai): apresentador de IA interrompível e demos em JavaScript clicáveis no lugar de vídeo/slides estáticos
- Use agentic coding para baratear radicalmente prototipagem e experimentação, mas reconheça que a alocação de recursos ainda exige decisão top-down de portfólio

> **Deep dive:** `medium` — Oferece várias teses acionáveis e relevantes (permissões para agentes, arquitetura de dados não estruturados, opcionalidade de vendors, desenho de equipes), mas é um chat estratégico de alto nível, com trechos promocionais e sem profundidade técnica ou arquitetural detalhada.
