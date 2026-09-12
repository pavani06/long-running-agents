---
title: "FINALLY, this AI agent actually works!"
type: "extract"
source: "youtube"
video_id: "XeWZIzndlY4"
url: "https://www.youtube.com/watch?v=XeWZIzndlY4"
channel: "AI Search"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-finally-this-ai-agent-actually-works--XeWZIzndlY4.txt]]"
tags: ["agents", "agent-loop", "agent-tooling", "analise", "error-handling", "permissions", "escalation", "decision-discipline"]
thesis: "Do Browser é uma extensão Chrome com agente de IA que, segundo o teste do revisor, executa tarefas reais de navegador de ponta a ponta (responder e-mails consultando o calendário, engajar no X, pedir comida no Uber Eats, prospectar faculdades e enviar cold emails) com velocidade e robustez superiores a agentes anteriores como AutoGPT, AutoGen e BabyAGI."
concepts: ["agente de uso de navegador (computer use) como extensão Chrome sem código", "autonomia com julgamento próprio ('use your own judgment, no need to ask me')", "integração cruzada de apps no mesmo navegador (Gmail + Google Calendar)", "auto-correção de navegação errada sem intervenção humana", "guardrail operacional: remover métodos de pagamento para impedir compras autônomas", "escalonamento para o humano quando falta credencial (pagamento ausente)", "automação de prospecção e cold outreach (scraping + redação + envio)", "coleta estruturada de dados de pesquisa para Google Docs", "segregação de risco: delegar apenas e-mails de baixo risco ao agente"]
tools: ["Do Browser", "Chrome", "Gmail", "Google Calendar", "Uber Eats", "X (Twitter)", "Wikipedia", "Google Docs", "Google", "Papers with Code", "ChatGPT", "Zotero (citado como 'zoto')", "Semantic Scholar", "Notion AI", "AutoGPT", "AutoGen", "BabyAGI", "Multi-On", "SmithOS", "Claude computer use agent", "Thly (patrocinador; agentes de voz para ligações)", "Salesforce", "Zoho", "Zendesk", "ibuildwebsite.com (portfólio fictício do teste)"]
people: ["Fundador do Do Browser (não nomeado)", "Terren/Terrence (remetente dos e-mails de teste)", "Sam (persona usada no cold email)", "Algonquin College", "Cambrian College", "Canadore College"]
claims: ["Do Browser concluiu múltiplas tarefas reais sem travar em loops infinitos, diferentemente de AutoGPT, AutoGen, BabyAGI, Multi-On, SmithOS e do computer use do Claude", "O agente respondeu três e-mails em cerca de 2 segundos cada, consultando o Google Calendar para oferecer horários coerentes com os blocos ocupados", "Se houver método de pagamento salvo, o agente prossegue e paga pedidos no Uber Eats; o revisor deliberadamente removeu os métodos de pagamento como salvaguarda", "Ao cair no site errado do Canadore College, o agente identificou o erro e rebuscou o site oficial no Google antes de extrair o e-mail", "O agente raspou a Wikipedia, extraiu e-mails de contato de três faculdades canadenses e enviou cold emails personalizadas com link de portfólio, automatizando prospecção e outreach de vendas", "Falhas observadas: não buscou fonte alternativa para o nome do journal ausente e pulou um paper na lista do Papers with Code", "Recomendação prática: usar o agente apenas para e-mails de baixo risco e manter supervisão humana para decisões de alto valor financeiro", "O setup não exige código nem clonar repositórios: basta adicionar a extensão ao Chrome e fazer login com e-mail"]
deep_dive: "low"
deep_dive_reason: "É uma demo/review promocional de produto consumidor, sem densidade de insight arquitetural, metodológico ou de engenharia de harness, context-engineering ou evals."
---

# FINALLY, this AI agent actually works!

## Tese
Do Browser é uma extensão Chrome com agente de IA que, segundo o teste do revisor, executa tarefas reais de navegador de ponta a ponta (responder e-mails consultando o calendário, engajar no X, pedir comida no Uber Eats, prospectar faculdades e enviar cold emails) com velocidade e robustez superiores a agentes anteriores como AutoGPT, AutoGen e BabyAGI.

## Conceitos-chave
- agente de uso de navegador (computer use) como extensão Chrome sem código
- autonomia com julgamento próprio ('use your own judgment, no need to ask me')
- integração cruzada de apps no mesmo navegador (Gmail + Google Calendar)
- auto-correção de navegação errada sem intervenção humana
- guardrail operacional: remover métodos de pagamento para impedir compras autônomas
- escalonamento para o humano quando falta credencial (pagamento ausente)
- automação de prospecção e cold outreach (scraping + redação + envio)
- coleta estruturada de dados de pesquisa para Google Docs
- segregação de risco: delegar apenas e-mails de baixo risco ao agente

## Ferramentas & pessoas
**Ferramentas:** Do Browser, Chrome, Gmail, Google Calendar, Uber Eats, X (Twitter), Wikipedia, Google Docs, Google, Papers with Code, ChatGPT, Zotero (citado como 'zoto'), Semantic Scholar, Notion AI, AutoGPT, AutoGen, BabyAGI, Multi-On, SmithOS, Claude computer use agent, Thly (patrocinador; agentes de voz para ligações), Salesforce, Zoho, Zendesk, ibuildwebsite.com (portfólio fictício do teste)

**Pessoas/orgs:** Fundador do Do Browser (não nomeado), Terren/Terrence (remetente dos e-mails de teste), Sam (persona usada no cold email), Algonquin College, Cambrian College, Canadore College

## Claims acionáveis
- Do Browser concluiu múltiplas tarefas reais sem travar em loops infinitos, diferentemente de AutoGPT, AutoGen, BabyAGI, Multi-On, SmithOS e do computer use do Claude
- O agente respondeu três e-mails em cerca de 2 segundos cada, consultando o Google Calendar para oferecer horários coerentes com os blocos ocupados
- Se houver método de pagamento salvo, o agente prossegue e paga pedidos no Uber Eats; o revisor deliberadamente removeu os métodos de pagamento como salvaguarda
- Ao cair no site errado do Canadore College, o agente identificou o erro e rebuscou o site oficial no Google antes de extrair o e-mail
- O agente raspou a Wikipedia, extraiu e-mails de contato de três faculdades canadenses e enviou cold emails personalizadas com link de portfólio, automatizando prospecção e outreach de vendas
- Falhas observadas: não buscou fonte alternativa para o nome do journal ausente e pulou um paper na lista do Papers with Code
- Recomendação prática: usar o agente apenas para e-mails de baixo risco e manter supervisão humana para decisões de alto valor financeiro
- O setup não exige código nem clonar repositórios: basta adicionar a extensão ao Chrome e fazer login com e-mail

> **Deep dive:** `low` — É uma demo/review promocional de produto consumidor, sem densidade de insight arquitetural, metodológico ou de engenharia de harness, context-engineering ou evals.
