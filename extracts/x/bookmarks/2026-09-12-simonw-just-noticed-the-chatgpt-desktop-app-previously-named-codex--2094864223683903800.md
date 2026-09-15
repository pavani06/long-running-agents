---
title: "LibreOffice embutido no ChatGPT desktop"
type: "extract"
source: "x"
status_id: "2094864223683903800"
handle: "simonw"
url: "https://x.com/simonw/status/2094864223683903800"
created_at: "2026-09-01T19:05:26.000Z"
extracted: "2026-09-13"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-12-simonw-just-noticed-the-chatgpt-desktop-app-previously-named-codex--2094864223683903800.json]]"
tags: ["agent-tooling", "stack-tooling", "arquitetura"]
topic: "LibreOffice embutido no ChatGPT desktop"
summary: "Simon Willison descobriu que o app desktop do ChatGPT (antes chamado Codex) da OpenAI embute uma cópia completa do LibreOffice escondida em ~/.cache, provavelmente para converter e manipular documentos de escritório usados pelo agente. Vale salvar como pista de arquitetura para agentes que processam arquivos docx/xlsx/pptx."
key_points: ["O app desktop do ChatGPT (anteriormente nomeado Codex) inclui uma cópia completa do LibreOffice.", "A cópia fica escondida em uma pasta oculta dentro do diretório ~/.cache.", "Uso provável: conversão/leitura headless de formatos Office (docx, xlsx, pptx), permitindo que o agente manipule documentos.", "Pista prática para quem constrói agentes desktop: empacotar LibreOffice é uma forma robusta de suportar documentos sem reimplementar parsers."]
entities: ["OpenAI", "ChatGPT", "Codex", "LibreOffice", "Simon Willison"]
content_type: "announcement"
revisit: "medium"
grounded_in: "tweet"
links: []
media: ["https://pbs.twimg.com/media/HRJztBsbIAAHRok.jpg"]
thin: false
relates-to: ["[[extracts/x/bookmarks/2026-09-12-simonw-here-s-my-attempt-at-explaining-what-chatgpt-work-can-actual--2094214737957691854|Capacidades do ChatGPT Work]]", "[[extracts/x/bookmarks/2026-09-12-openai-now-available-chatgpt-for-financial-services-this-is-a-tailo--2098118191029624911|ChatGPT para serviços financeiros]]", "[[extracts/x/bookmarks/2026-09-12-chatgpt-now-everyone-can-put-data-to-work-were-introducing-a-new-dat--2098065296968011853|Data agent no ChatGPT Work]]", "[[extracts/x/bookmarks/2026-09-12-andrewyng-openworker-an-open-source-agent-that-doesn-t-just-chat-but-c--2092315079576555806|OpenWorker: agente open source de tarefas locais]]", "[[extracts/x/bookmarks/2026-09-12-mattpocockuk-my-ide-is-discord-https-t-co-xsihrc2kle--2087555290174566491|Discord como IDE]]", "[[extracts/x/bookmarks/2026-09-12-hnshah-im-late-to-this-party-but-https-t-co-2qvqvyamhq-just-showed--2098603214065332290|Lançamento agent-native com demo de Excel]]"]
theme: "Tooling de IA e Performance"
---

# LibreOffice embutido no ChatGPT desktop

**@simonw** · [2094864223683903800](https://x.com/simonw/status/2094864223683903800) · `announcement`

## Resumo
Simon Willison descobriu que o app desktop do ChatGPT (antes chamado Codex) da OpenAI embute uma cópia completa do LibreOffice escondida em ~/.cache, provavelmente para converter e manipular documentos de escritório usados pelo agente. Vale salvar como pista de arquitetura para agentes que processam arquivos docx/xlsx/pptx.

## Pontos-chave
- O app desktop do ChatGPT (anteriormente nomeado Codex) inclui uma cópia completa do LibreOffice.
- A cópia fica escondida em uma pasta oculta dentro do diretório ~/.cache.
- Uso provável: conversão/leitura headless de formatos Office (docx, xlsx, pptx), permitindo que o agente manipule documentos.
- Pista prática para quem constrói agentes desktop: empacotar LibreOffice é uma forma robusta de suportar documentos sem reimplementar parsers.

## Entidades
OpenAI, ChatGPT, Codex, LibreOffice, Simon Willison

> **Revisit:** `medium` · **fonte:** `tweet`
