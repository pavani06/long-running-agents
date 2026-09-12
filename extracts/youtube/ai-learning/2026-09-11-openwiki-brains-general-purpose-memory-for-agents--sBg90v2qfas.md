---
title: "OpenWiki Brains, general-purpose memory for agents"
type: "extract"
source: "youtube"
video_id: "sBg90v2qfas"
url: "https://www.youtube.com/watch?v=sBg90v2qfas"
channel: "LangChain"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-openwiki-brains-general-purpose-memory-for-agents--sBg90v2qfas.txt]]"
tags: ["memory-architecture", "context-management", "knowledge-management", "agent-tooling", "agents", "runtime", "process", "tracing"]
thesis: "LangChain anuncia o modo \"personal brains\" do OpenWiki, um agente open source que gera e mantém memória geral proativa para agentes, ingerindo sequencialmente múltiplas fontes pessoais (Notion, Gmail, X, web search, Hacker News) via cron local e consolidando tudo num wiki acessível a qualquer sessão de agente na máquina."
concepts: ["memória proativa vs. reativa (contraste com ChatGPT/Claude)", "wiki brief como system prompt da geração de memória", "prompts por conector orientando a ingestão", "ingestão sequencial de conectores para poupar contexto do agente", "busca agêntica (agentic search) para fontes sem API de mudanças incrementais", "arquivo open questions como mecanismo anti-alucinação", "cron local vs. GitHub Actions (escopo máquina vs. repo)", "diretório de memória na raiz do computador acessível a todas as sessões de agente", "wiki totalmente gerado e mantido pelo agente com edição humana opcional", "wake nativo do Mac para jobs noturnos"]
tools: ["OpenWiki", "LangSmith", "OpenAI / GPT", "Notion", "Gmail", "X (Twitter)", "Hacker News", "GitHub Actions", "Slack (em breve)", "macOS cron/wake"]
people: ["LangChain", "OpenAI", "Anthropic (Claude)", "GitHub", "Notion"]
claims: ["Configuração via `openwiki personal init` segue fluxo de onboarding similar ao codebase memory, com provider de modelo, chave do LangSmith para tracing, wiki brief editável e cron local (default 2h da manhã)", "É preciso habilitar o wake nativo do Mac, senão o job noturno de atualização não roda se o computador estiver desligado", "Cada conector aceita um prompt próprio (ex.: 'prioritize pages related to applied AI and customer feedback') para guiar onde e como o agente busca documentos", "O X/Twitter exige developer account e OAuth client app; o Notion autentica via OAuth no navegador; suporta-se múltiplas conexões por fonte", "A ingestão é deliberadamente sequencial: um conector por vez, com sessão fresca a cada fonte, para reduzir carga de contexto e evitar conflitos/sobreposição de dados", "Sem API incremental (caso Notion), o agente recebe o prompt do conector + ferramenta de query e executa busca agêntica; no X, baixa tweets, bookmarks e snapshot do feed das últimas 24h", "O arquivo open questions faz o agente registrar perguntas sem resposta em vez de alucinar: inspeciona o arquivo no início de cada run, revisita ao final, e o humano pode responder/adicionar perguntas manualmente que serão absorvidas na próxima run", "O diretório openwiki fica na raiz do computador (não no repo) com wiki (sources, commitments, open questions, personal logistics, quick start, index, themes), logs, dados de conectores, backups, onboarding.json, instructions.md e arquivo de secrets", "instructions.md é relido a cada run, então edições humanas no brief e no wiki são incorporadas automaticamente nas execuções seguintes"]
deep_dive: "medium"
deep_dive_reason: "Contém insights arquiteturais acionáveis e relativamente novos (memória proativa, ingestão sequencial para gestão de contexto, padrão open questions anti-alucinação), mas o grosso do conteúdo é um walkthrough tutorial/promocional de setup do produto."
---

# OpenWiki Brains, general-purpose memory for agents

## Tese
LangChain anuncia o modo "personal brains" do OpenWiki, um agente open source que gera e mantém memória geral proativa para agentes, ingerindo sequencialmente múltiplas fontes pessoais (Notion, Gmail, X, web search, Hacker News) via cron local e consolidando tudo num wiki acessível a qualquer sessão de agente na máquina.

## Conceitos-chave
- memória proativa vs. reativa (contraste com ChatGPT/Claude)
- wiki brief como system prompt da geração de memória
- prompts por conector orientando a ingestão
- ingestão sequencial de conectores para poupar contexto do agente
- busca agêntica (agentic search) para fontes sem API de mudanças incrementais
- arquivo open questions como mecanismo anti-alucinação
- cron local vs. GitHub Actions (escopo máquina vs. repo)
- diretório de memória na raiz do computador acessível a todas as sessões de agente
- wiki totalmente gerado e mantido pelo agente com edição humana opcional
- wake nativo do Mac para jobs noturnos

## Ferramentas & pessoas
**Ferramentas:** OpenWiki, LangSmith, OpenAI / GPT, Notion, Gmail, X (Twitter), Hacker News, GitHub Actions, Slack (em breve), macOS cron/wake

**Pessoas/orgs:** LangChain, OpenAI, Anthropic (Claude), GitHub, Notion

## Claims acionáveis
- Configuração via `openwiki personal init` segue fluxo de onboarding similar ao codebase memory, com provider de modelo, chave do LangSmith para tracing, wiki brief editável e cron local (default 2h da manhã)
- É preciso habilitar o wake nativo do Mac, senão o job noturno de atualização não roda se o computador estiver desligado
- Cada conector aceita um prompt próprio (ex.: 'prioritize pages related to applied AI and customer feedback') para guiar onde e como o agente busca documentos
- O X/Twitter exige developer account e OAuth client app; o Notion autentica via OAuth no navegador; suporta-se múltiplas conexões por fonte
- A ingestão é deliberadamente sequencial: um conector por vez, com sessão fresca a cada fonte, para reduzir carga de contexto e evitar conflitos/sobreposição de dados
- Sem API incremental (caso Notion), o agente recebe o prompt do conector + ferramenta de query e executa busca agêntica; no X, baixa tweets, bookmarks e snapshot do feed das últimas 24h
- O arquivo open questions faz o agente registrar perguntas sem resposta em vez de alucinar: inspeciona o arquivo no início de cada run, revisita ao final, e o humano pode responder/adicionar perguntas manualmente que serão absorvidas na próxima run
- O diretório openwiki fica na raiz do computador (não no repo) com wiki (sources, commitments, open questions, personal logistics, quick start, index, themes), logs, dados de conectores, backups, onboarding.json, instructions.md e arquivo de secrets
- instructions.md é relido a cada run, então edições humanas no brief e no wiki são incorporadas automaticamente nas execuções seguintes

> **Deep dive:** `medium` — Contém insights arquiteturais acionáveis e relativamente novos (memória proativa, ingestão sequencial para gestão de contexto, padrão open questions anti-alucinação), mas o grosso do conteúdo é um walkthrough tutorial/promocional de setup do produto.
