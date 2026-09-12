---
title: "The agent-ready web: Simplify user actions with WebMCP — Tara Agyemang, Google"
type: "extract"
source: "youtube"
video_id: "ghJmWQCIHRM"
url: "https://www.youtube.com/watch?v=ghJmWQCIHRM"
channel: "AI Engineer"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-the-agent-ready-web-simplify-user-actions-with-webmcp-tara-agyemang-google--ghJmWQCIHRM.txt]]"
tags: ["agent-tooling", "agents", "arquitetura", "runtime", "stack-tooling", "observability", "testes-qa"]
thesis: "WebMCP é um padrão web proposto pelo Google Chrome que permite aos sites expor capacidades como ferramentas estruturadas para agentes de IA no navegador, substituindo processos frágeis e caros em tokens de screen-scraping do DOM."
concepts: ["WebMCP (Model Context Protocol para web)", "Diferença entre MCP (server-side) e WebMCP (client-side, in-browser)", "API declarativa: atributos em formulários HTML geram JSON schema automaticamente", "API imperativa: registerTool com schema customizado e bloco execute", "Agent-ready websites: acessibilidade e HTML semântico como fundação para agentes", "Ferramentas com escopo por página (page-scoped tools)", "Atributo agent-invoked para distinguir preenchimento por agente vs humano", "Sincronização da UI com chamadas de ferramentas", "Handoff entre usuário humano e agente de IA durante a navegação", "Loop de chamadas repetidas de ferramentas pelo agente até completar a tarefa", "Mapeamento de prompts em linguagem natural para parâmetros de ferramentas"]
tools: ["WebMCP", "MCP (Model Context Protocol)", "Google Chrome", "Chrome Canary", "Chrome 146+ com flags experimentais", "Gemini 2.5", "Gemini 3.1", "Model Context Tool Inspector (extensão Chrome)", "Eval CLI tool (repositório GitHub do WebMCP)", "Demos do GitHub (maze game, concert site)"]
people: ["Tara (Google Chrome DevRel)", "Google Chrome team", "Google DeepMind", "Chrome DevRel team"]
claims: ["Melhorar acessibilidade, HTML semântico, Core Web Vitals e UX já deixa um site na metade do caminho para ser agent-ready", "WebMCP melhora significativamente performance e confiabilidade de agentes navegando em sites, em comparação com parsing de DOM/screenshot", "Agentes atuais gastam muitos tokens processando DOM inteiro, árvore de acessibilidade e screenshots para cliques simples, e podem falhar se o layout mudar (ex.: anúncio carregando)", "A API declarativa gera JSON schema automaticamente a partir dos campos do formulário HTML usando tool name e tool description como atributos", "A API imperativa exige schema manual, nome, descrição detalhada e um bloco execute que chama JavaScript existente e retorna resultado ao agente", "Ferramentas são registradas por página: navegar para nova página expõe novo conjunto de ferramentas", "É essencial manter a UI em sincronia com as chamadas de ferramentas para o usuário acompanhar o que o agente faz", "Etapas sensíveis como pagamento/checkout devem permanecer manuais para o usuário confirmar gasto real", "WebMCP só funciona com a janela do navegador aberta, pois todas as ferramentas vivem no client-side", "Para testar: Chrome 146+ (de preferência Canary), habilitar flag de teste do WebMCP, instalar o Model Context Tool Inspector", "Prompts mais refinados (ex.: informar localização da saída) tornam o agente mais eficiente no uso das ferramentas", "A API está em early preview experimental e mudará; o programa pede feedback de desenvolvedores via blog do programa e repositório GitHub"]
deep_dive: "medium"
deep_dive_reason: "A palestra oferece detalhes práticos acionáveis das duas APIs e do setup experimental, mas é majoritariamente introdutória e demonstrativa, sem densidade arquitetural profunda em harness, evals ou governança."
---

# The agent-ready web: Simplify user actions with WebMCP — Tara Agyemang, Google

## Tese
WebMCP é um padrão web proposto pelo Google Chrome que permite aos sites expor capacidades como ferramentas estruturadas para agentes de IA no navegador, substituindo processos frágeis e caros em tokens de screen-scraping do DOM.

## Conceitos-chave
- WebMCP (Model Context Protocol para web)
- Diferença entre MCP (server-side) e WebMCP (client-side, in-browser)
- API declarativa: atributos em formulários HTML geram JSON schema automaticamente
- API imperativa: registerTool com schema customizado e bloco execute
- Agent-ready websites: acessibilidade e HTML semântico como fundação para agentes
- Ferramentas com escopo por página (page-scoped tools)
- Atributo agent-invoked para distinguir preenchimento por agente vs humano
- Sincronização da UI com chamadas de ferramentas
- Handoff entre usuário humano e agente de IA durante a navegação
- Loop de chamadas repetidas de ferramentas pelo agente até completar a tarefa
- Mapeamento de prompts em linguagem natural para parâmetros de ferramentas

## Ferramentas & pessoas
**Ferramentas:** WebMCP, MCP (Model Context Protocol), Google Chrome, Chrome Canary, Chrome 146+ com flags experimentais, Gemini 2.5, Gemini 3.1, Model Context Tool Inspector (extensão Chrome), Eval CLI tool (repositório GitHub do WebMCP), Demos do GitHub (maze game, concert site)

**Pessoas/orgs:** Tara (Google Chrome DevRel), Google Chrome team, Google DeepMind, Chrome DevRel team

## Claims acionáveis
- Melhorar acessibilidade, HTML semântico, Core Web Vitals e UX já deixa um site na metade do caminho para ser agent-ready
- WebMCP melhora significativamente performance e confiabilidade de agentes navegando em sites, em comparação com parsing de DOM/screenshot
- Agentes atuais gastam muitos tokens processando DOM inteiro, árvore de acessibilidade e screenshots para cliques simples, e podem falhar se o layout mudar (ex.: anúncio carregando)
- A API declarativa gera JSON schema automaticamente a partir dos campos do formulário HTML usando tool name e tool description como atributos
- A API imperativa exige schema manual, nome, descrição detalhada e um bloco execute que chama JavaScript existente e retorna resultado ao agente
- Ferramentas são registradas por página: navegar para nova página expõe novo conjunto de ferramentas
- É essencial manter a UI em sincronia com as chamadas de ferramentas para o usuário acompanhar o que o agente faz
- Etapas sensíveis como pagamento/checkout devem permanecer manuais para o usuário confirmar gasto real
- WebMCP só funciona com a janela do navegador aberta, pois todas as ferramentas vivem no client-side
- Para testar: Chrome 146+ (de preferência Canary), habilitar flag de teste do WebMCP, instalar o Model Context Tool Inspector
- Prompts mais refinados (ex.: informar localização da saída) tornam o agente mais eficiente no uso das ferramentas
- A API está em early preview experimental e mudará; o programa pede feedback de desenvolvedores via blog do programa e repositório GitHub

> **Deep dive:** `medium` — A palestra oferece detalhes práticos acionáveis das duas APIs e do setup experimental, mas é majoritariamente introdutória e demonstrativa, sem densidade arquitetural profunda em harness, evals ou governança.
