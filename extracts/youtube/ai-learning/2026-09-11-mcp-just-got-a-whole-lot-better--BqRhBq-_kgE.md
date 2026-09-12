---
title: "MCP Just Got a Whole Lot Better"
type: "extract"
source: "youtube"
video_id: "BqRhBq-_kgE"
url: "https://www.youtube.com/watch?v=BqRhBq-_kgE"
channel: "Neon Postgres"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-mcp-just-got-a-whole-lot-better--BqRhBq-_kgE.txt]]"
tags: ["agent-tooling", "agents", "arquitetura", "context-engineering", "context-management", "token-budgeting", "stack-tooling", "frameworks", "permissions"]
thesis: "Com clientes de agente assumindo descoberta progressiva de ferramentas e chamada programática (code mode), construtores de servidores MCP devem expor tanto endpoints brutos quanto workflows ergonômicos empacotados (estilo SDK), deixando o servidor controlar a disponibilidade de ferramentas e o cliente controlar descoberta e execução."
concepts: ["MCP servers e evolução de padrões de design", "Mapeamento um-para-one de endpoints de API para tools", "Abordagem em camadas de tool calls (buscar endpoints / inspecionar definição / executar requisição)", "Progressive tool discovery (padrão no lado do cliente)", "Programmatic tool calling / code mode (agente escreve script em sandbox encadeando tools)", "Eficiência de tokens como critério de design de tools", "Camada ergonômica sobre SDK gerado (bundling de workflows comuns)", "Pacote de tools separado com adaptadores para frameworks de agentes", "Categorização e escoping de tools por acesso do agente", "Divisão de responsabilidade servidor (disponibilidade) vs cliente (descoberta/execução)"]
tools: ["MCP", "Neon", "Neon MCP server", "neon-tools (pacote)", "OpenAPI spec", "Codex", "Claude Code", "Mastra", "Eve"]
people: ["Neon"]
claims: ["Mapear cada endpoint de API para um tool próprio infla o context window com centenas de tools antes mesmo da sessão começar", "Endpoints muito similares entre si confundem o agente na seleção do tool correto", "A abordagem em camadas (buscar/inspecionar/executar) reduz centenas de tools para 2-3 chamadas", "Progressive tool discovery migrou do servidor para o cliente e é hoje best practice recomendada para clientes MCP", "Em code mode, o agente escreve um script que encadeia tools num sandbox e só o resultado final volta ao modelo, economizando tokens", "Não se deve voltar ao mapeamento 1:1: empacotar workflows comuns (como SDKs fazem) em tools únicos é mais eficiente em tokens", "Exemplo Neon: criar branch exige 3 chamadas de API (criar branch, anexar compute, obter connection string) que o SDK empacota em createWithCompute", "Arquitetura recomendável: SDK gerado do OpenAPI cobrindo todos os endpoints + camada fina de métodos ergonômicos por cima, tudo convertido em tool calls", "Extrair tools para um pacote separado permite servir tanto o servidor MCP quanto adaptadores para frameworks como Mastra e Eve", "Organizar tools em categorias permite restringir o escopo de ferramentas disponíveis ao agente", "Princípio de design: o servidor controla quais tools existem; o cliente decide como descobri-las e executá-las", "APIs simples podem tolerar mapeamento 1:1, mas infraestrutura complexa como Neon se beneficia de atalhos ergonômicos que evitam erros repetidos do agente"]
deep_dive: "medium"
deep_dive_reason: "Oferece padrões arquiteturais concretos e acionáveis para design de tools MCP com racional de eficiência de tokens, mas é uma visão geral acessível centrada na abordagem de um único vendor, sem profundidade técnica ou novidade suficiente para tier alto."
---

# MCP Just Got a Whole Lot Better

## Tese
Com clientes de agente assumindo descoberta progressiva de ferramentas e chamada programática (code mode), construtores de servidores MCP devem expor tanto endpoints brutos quanto workflows ergonômicos empacotados (estilo SDK), deixando o servidor controlar a disponibilidade de ferramentas e o cliente controlar descoberta e execução.

## Conceitos-chave
- MCP servers e evolução de padrões de design
- Mapeamento um-para-one de endpoints de API para tools
- Abordagem em camadas de tool calls (buscar endpoints / inspecionar definição / executar requisição)
- Progressive tool discovery (padrão no lado do cliente)
- Programmatic tool calling / code mode (agente escreve script em sandbox encadeando tools)
- Eficiência de tokens como critério de design de tools
- Camada ergonômica sobre SDK gerado (bundling de workflows comuns)
- Pacote de tools separado com adaptadores para frameworks de agentes
- Categorização e escoping de tools por acesso do agente
- Divisão de responsabilidade servidor (disponibilidade) vs cliente (descoberta/execução)

## Ferramentas & pessoas
**Ferramentas:** MCP, Neon, Neon MCP server, neon-tools (pacote), OpenAPI spec, Codex, Claude Code, Mastra, Eve

**Pessoas/orgs:** Neon

## Claims acionáveis
- Mapear cada endpoint de API para um tool próprio infla o context window com centenas de tools antes mesmo da sessão começar
- Endpoints muito similares entre si confundem o agente na seleção do tool correto
- A abordagem em camadas (buscar/inspecionar/executar) reduz centenas de tools para 2-3 chamadas
- Progressive tool discovery migrou do servidor para o cliente e é hoje best practice recomendada para clientes MCP
- Em code mode, o agente escreve um script que encadeia tools num sandbox e só o resultado final volta ao modelo, economizando tokens
- Não se deve voltar ao mapeamento 1:1: empacotar workflows comuns (como SDKs fazem) em tools únicos é mais eficiente em tokens
- Exemplo Neon: criar branch exige 3 chamadas de API (criar branch, anexar compute, obter connection string) que o SDK empacota em createWithCompute
- Arquitetura recomendável: SDK gerado do OpenAPI cobrindo todos os endpoints + camada fina de métodos ergonômicos por cima, tudo convertido em tool calls
- Extrair tools para um pacote separado permite servir tanto o servidor MCP quanto adaptadores para frameworks como Mastra e Eve
- Organizar tools em categorias permite restringir o escopo de ferramentas disponíveis ao agente
- Princípio de design: o servidor controla quais tools existem; o cliente decide como descobri-las e executá-las
- APIs simples podem tolerar mapeamento 1:1, mas infraestrutura complexa como Neon se beneficia de atalhos ergonômicos que evitam erros repetidos do agente

> **Deep dive:** `medium` — Oferece padrões arquiteturais concretos e acionáveis para design de tools MCP com racional de eficiência de tokens, mas é uma visão geral acessível centrada na abordagem de um único vendor, sem profundidade técnica ou novidade suficiente para tier alto.
