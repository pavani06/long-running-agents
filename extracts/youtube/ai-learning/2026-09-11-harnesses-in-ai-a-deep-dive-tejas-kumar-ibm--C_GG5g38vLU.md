---
title: "Harnesses in AI: A Deep Dive — Tejas Kumar, IBM"
type: "extract"
source: "youtube"
video_id: "C_GG5g38vLU"
url: "https://www.youtube.com/watch?v=C_GG5g38vLU"
channel: "AI Engineer"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-harnesses-in-ai-a-deep-dive-tejas-kumar-ibm--C_GG5g38vLU.txt]]"
tags: ["harness", "harness-engineering", "agent-loop", "verification", "context-management", "error-handling", "model-selection", "token-budgeting", "tracing", "agentic-coding", "runtime", "roadmap"]
thesis: "Um agent harness é tudo o que envolve o modelo — registro de ferramentas, gestão de contexto, guardrails, agent loop e passo de verificação — para ancorar modelos caixa-preta não-determinísticos num ambiente estável e determinístico controlado por você, mudando o resultado do agente sem tocar no prompt e viabilizando modelos baratos."
concepts: ["Agent harness: tudo ao redor do modelo que dá grounding na realidade", "Harness vs. test harness de ML (glorified test suite)", "Anatomia do harness: tool registry, modelo, primitivas de gestão de contexto, guardrails, agent loop, verify step", "Harness como loop ao redor do agent loop (max attempts)", "Guardrails compostos: max iterações e max mensagens", "Compressão de contexto naive (preserva system prompt, user prompt e as 2 últimas mensagens)", "Verificação determinística baseada no trace/histórico de tool calls para detectar mentira do agente", "Login handler determinístico no harness com acesso seguro a segredos (variáveis de ambiente)", "Anti-padrão: 'promptar mais forte' / mudar system prompt em vez de mudar o harness", "Custo e confiabilidade: 'pagamos aluguel' por tokens e o modelo servido é caixa-preta (podem servir outro modelo)", "Harnesses gerados dinamicamente on-the-fly pelo próprio agente antes da tarefa (previsão 2027, 'plan mode on steroids')"]
tools: ["Claude Code", "Cursor", "Codex", "Playwright", "Playwright MCP", "Chromium", "GPT-3.5 Turbo", "GPT OSS", "Qwen", "Claude Pro", "Claude Opus", "Claude Sonnet", "IBM Watson", "OpenAI SDK", "OpenRAG (open-rag, IBM)", "Hacker News", "npm", "GitHub"]
people: ["Tis (palestrante, AI Developer Advocate na IBM)", "IBM", "Anthropic", "Google", "OpenAI", "Nilix (autor do post upvotado no Hacker News)"]
claims: ["Não corrija falhas do agente alterando prompts; construa/altere o harness — no demo o prompt ficou fixo e o resultado mudou radicalmente", "Implemente um verify step determinístico que inspeciona o histórico de tool calls para detectar sucesso falso (ex.: clique em upvote sem login efetivo, redirecionamento não recuperado)", "Trate autenticação no harness, não no agente: um handler determinístico injeta credenciais de forma segura (com acesso a segredos) e notifica o agente via mensagem na fila", "Use guardrails compostos: limite de iterações (ex.: 6 passos), limite de mensagens com compressão de contexto, e max attempts no nível do harness (ex.: 3 tentativas antes de desistir)", "Com um bom harness, modelos baratos/antigos (GPT-3.5 Turbo, Qwen, GPT OSS) completam tarefas de browser-use, reduzindo custo de inferência", "O harness pode ser um loop externo que re-executa tentativas do agent loop e aplica verificação entre elas", "Empresas usam harness de segurança enterprise (OpenRAG) para RAG sobre dados siloados (Teams calls, PDFs, invoices) em ambientes privados", "Previsão de roadmap: 2025 ano dos agentes, 2026 dos harnesses, 2027 de harnesses gerados dinamicamente pelo agente antes de executar a tarefa"]
deep_dive: "high"
deep_dive_reason: "Construção incremental ao vivo de um harness com padrões arquitetônicos concretos e replicáveis (verify-on-trace, login determinístico com segredos, guardrails compostos, compressão de contexto) diretamente relevantes a harness-engineering, apesar do tom introdutório em partes."
---

# Harnesses in AI: A Deep Dive — Tejas Kumar, IBM

## Tese
Um agent harness é tudo o que envolve o modelo — registro de ferramentas, gestão de contexto, guardrails, agent loop e passo de verificação — para ancorar modelos caixa-preta não-determinísticos num ambiente estável e determinístico controlado por você, mudando o resultado do agente sem tocar no prompt e viabilizando modelos baratos.

## Conceitos-chave
- Agent harness: tudo ao redor do modelo que dá grounding na realidade
- Harness vs. test harness de ML (glorified test suite)
- Anatomia do harness: tool registry, modelo, primitivas de gestão de contexto, guardrails, agent loop, verify step
- Harness como loop ao redor do agent loop (max attempts)
- Guardrails compostos: max iterações e max mensagens
- Compressão de contexto naive (preserva system prompt, user prompt e as 2 últimas mensagens)
- Verificação determinística baseada no trace/histórico de tool calls para detectar mentira do agente
- Login handler determinístico no harness com acesso seguro a segredos (variáveis de ambiente)
- Anti-padrão: 'promptar mais forte' / mudar system prompt em vez de mudar o harness
- Custo e confiabilidade: 'pagamos aluguel' por tokens e o modelo servido é caixa-preta (podem servir outro modelo)
- Harnesses gerados dinamicamente on-the-fly pelo próprio agente antes da tarefa (previsão 2027, 'plan mode on steroids')

## Ferramentas & pessoas
**Ferramentas:** Claude Code, Cursor, Codex, Playwright, Playwright MCP, Chromium, GPT-3.5 Turbo, GPT OSS, Qwen, Claude Pro, Claude Opus, Claude Sonnet, IBM Watson, OpenAI SDK, OpenRAG (open-rag, IBM), Hacker News, npm, GitHub

**Pessoas/orgs:** Tis (palestrante, AI Developer Advocate na IBM), IBM, Anthropic, Google, OpenAI, Nilix (autor do post upvotado no Hacker News)

## Claims acionáveis
- Não corrija falhas do agente alterando prompts; construa/altere o harness — no demo o prompt ficou fixo e o resultado mudou radicalmente
- Implemente um verify step determinístico que inspeciona o histórico de tool calls para detectar sucesso falso (ex.: clique em upvote sem login efetivo, redirecionamento não recuperado)
- Trate autenticação no harness, não no agente: um handler determinístico injeta credenciais de forma segura (com acesso a segredos) e notifica o agente via mensagem na fila
- Use guardrails compostos: limite de iterações (ex.: 6 passos), limite de mensagens com compressão de contexto, e max attempts no nível do harness (ex.: 3 tentativas antes de desistir)
- Com um bom harness, modelos baratos/antigos (GPT-3.5 Turbo, Qwen, GPT OSS) completam tarefas de browser-use, reduzindo custo de inferência
- O harness pode ser um loop externo que re-executa tentativas do agent loop e aplica verificação entre elas
- Empresas usam harness de segurança enterprise (OpenRAG) para RAG sobre dados siloados (Teams calls, PDFs, invoices) em ambientes privados
- Previsão de roadmap: 2025 ano dos agentes, 2026 dos harnesses, 2027 de harnesses gerados dinamicamente pelo agente antes de executar a tarefa

> **Deep dive:** `high` — Construção incremental ao vivo de um harness com padrões arquitetônicos concretos e replicáveis (verify-on-trace, login determinístico com segredos, guardrails compostos, compressão de contexto) diretamente relevantes a harness-engineering, apesar do tom introdutório em partes.
