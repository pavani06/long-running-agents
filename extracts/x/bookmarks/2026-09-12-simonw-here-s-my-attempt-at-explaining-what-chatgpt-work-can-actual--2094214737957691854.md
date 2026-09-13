---
title: "Capacidades do ChatGPT Work"
type: "extract"
source: "x"
status_id: "2094214737957691854"
handle: "simonw"
url: "https://x.com/simonw/status/2094214737957691854"
created_at: "2026-08-31T00:04:36.000Z"
extracted: "2026-09-13"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-12-simonw-here-s-my-attempt-at-explaining-what-chatgpt-work-can-actual--2094214737957691854.json]]"
tags: ["agent-tooling", "agents", "multi-agent", "model-selection", "runtime", "harness"]
topic: "Capacidades do ChatGPT Work"
summary: "Explainer detalhado de Simon Willison sobre o ChatGPT Work da OpenAI, decompondo as duas variantes (Cloud e Local) e os recursos exclusivos versus o Chat regular: execução de código com internet aberta, navegador headless Chrome, filesystem persistente entre sessões, publicação de sites e sub-agentes. Vale salvar como referência sobre o harness agêntico consumidor mais capaz da OpenAI, incluindo críticas de segurança e documentação reversa de 223 ferramentas e 44 skills."
key_points: ["ChatGPT Work são dois produtos: Work Cloud (chatgpt.com/apps) e Work Local (app desktop, ex-Codex re-skinado); disponível só para assinantes de US$20+/mês, com sessões faturadas na cota do Codex — o que explica diferenças de modelos disponíveis (Sol, Luna, Terra com níveis de reasoning até Ultra vs. Instant/Medium/High/Pro no Chat).", "Recursos exclusivos do Work vs. Chat: sandbox de execução de código com acesso à internet por padrão aberto (instala pacotes, clona repositórios GitHub, chama APIs), navegador Chrome headless completo que roda JS no DOM e permite takeover humano para senha/2FA sem expor credenciais ao modelo, e filesystem persistente e compartilhado entre sessões em /workspace/scratch.", "Work pode construir e deployar sites completos (ChatGPT Sites) sobre Cloudflare Workers com estado em D1/R2, rodar sub-agentes paralelos com Sol/Luna/Terra e agendar prompts automatizados (ex.: monitorar anúncios diariamente às 8h e atualizar um site a cada hora).", "Willison documentou por engenharia reversa 223 ferramentas registradas e 44 skills (ex.: control-browser via node REPL e API agent.browsers.*, documents, pdf, spreadsheets, sites-building), simplesmente pedindo ao Work que construísse um site de referência de si mesmo.", "Crítica central: o produto combina a 'trifeta letal' (dados privados + conteúdo não confiável + canal de exfiltração) sem explicação pública das defesas contra prompt injection; e a confusão persiste porque a OpenAI documenta por intenção de uso, não por mecânica real, e esconde system prompts e tool descriptions."]
entities: ["Simon Willison", "OpenAI", "ChatGPT Work", "Codex", "Claude", "Cloudflare Workers", "Cloudflare D1", "Cloudflare R2", "GPT-5.6 Sol", "GPT-5.6 Luna", "GPT-5.6 Terra", "Playwright", "datasette-mcp"]
content_type: "resource"
revisit: "high"
grounded_in: "article"
links: ["https://simonwillison.net/2026/Aug/30/understanding-chatgpt-work/"]
media: ["https://pbs.twimg.com/media/HRAlJG_akAEHiQo.jpg"]
---

# Capacidades do ChatGPT Work

**@simonw** · [2094214737957691854](https://x.com/simonw/status/2094214737957691854) · `resource`

## Resumo
Explainer detalhado de Simon Willison sobre o ChatGPT Work da OpenAI, decompondo as duas variantes (Cloud e Local) e os recursos exclusivos versus o Chat regular: execução de código com internet aberta, navegador headless Chrome, filesystem persistente entre sessões, publicação de sites e sub-agentes. Vale salvar como referência sobre o harness agêntico consumidor mais capaz da OpenAI, incluindo críticas de segurança e documentação reversa de 223 ferramentas e 44 skills.

## Pontos-chave
- ChatGPT Work são dois produtos: Work Cloud (chatgpt.com/apps) e Work Local (app desktop, ex-Codex re-skinado); disponível só para assinantes de US$20+/mês, com sessões faturadas na cota do Codex — o que explica diferenças de modelos disponíveis (Sol, Luna, Terra com níveis de reasoning até Ultra vs. Instant/Medium/High/Pro no Chat).
- Recursos exclusivos do Work vs. Chat: sandbox de execução de código com acesso à internet por padrão aberto (instala pacotes, clona repositórios GitHub, chama APIs), navegador Chrome headless completo que roda JS no DOM e permite takeover humano para senha/2FA sem expor credenciais ao modelo, e filesystem persistente e compartilhado entre sessões em /workspace/scratch.
- Work pode construir e deployar sites completos (ChatGPT Sites) sobre Cloudflare Workers com estado em D1/R2, rodar sub-agentes paralelos com Sol/Luna/Terra e agendar prompts automatizados (ex.: monitorar anúncios diariamente às 8h e atualizar um site a cada hora).
- Willison documentou por engenharia reversa 223 ferramentas registradas e 44 skills (ex.: control-browser via node REPL e API agent.browsers.*, documents, pdf, spreadsheets, sites-building), simplesmente pedindo ao Work que construísse um site de referência de si mesmo.
- Crítica central: o produto combina a 'trifeta letal' (dados privados + conteúdo não confiável + canal de exfiltração) sem explicação pública das defesas contra prompt injection; e a confusão persiste porque a OpenAI documenta por intenção de uso, não por mecânica real, e esconde system prompts e tool descriptions.

## Links
- https://simonwillison.net/2026/Aug/30/understanding-chatgpt-work/

## Entidades
Simon Willison, OpenAI, ChatGPT Work, Codex, Claude, Cloudflare Workers, Cloudflare D1, Cloudflare R2, GPT-5.6 Sol, GPT-5.6 Luna, GPT-5.6 Terra, Playwright, datasette-mcp

> **Revisit:** `high` · **fonte:** `article`
