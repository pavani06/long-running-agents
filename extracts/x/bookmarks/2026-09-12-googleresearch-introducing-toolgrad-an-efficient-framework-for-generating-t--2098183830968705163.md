---
title: "ToolGrad: geração de datasets de tool-use"
type: "extract"
source: "x"
status_id: "2098183830968705163"
handle: "GoogleResearch"
url: "https://x.com/GoogleResearch/status/2098183830968705163"
created_at: "2026-09-10T22:56:22.000Z"
extracted: "2026-09-13"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-12-googleresearch-introducing-toolgrad-an-efficient-framework-for-generating-t--2098183830968705163.json]]"
tags: ["agent-tooling", "agents", "data-platform", "evals", "performance"]
topic: "ToolGrad: geração de datasets de tool-use"
summary: "Google Research apresenta ToolGrad (ACL 2026), framework que inverte o paradigma tradicional gerando primeiro a cadeia ground-truth de uso de ferramentas e só depois o prompt do usuário, atingindo quase 100% de pass rate na geração de dados com menor custo. Modelos Gemma-3 fine-tuned no dataset ToolGrad-500 igualam ou superam LLMs proprietários SoTA no Berkeley Function Calling Leaderboard."
key_points: ["Paradigma answer-first: anotar da solução de tool-use para a query é mais fácil e exige um único passo de LLM, versus o approach query-first com DFS agent (ToolBench/ToolACE) que destila trajetórias de exploração custosa", "Arquitetura iterativa de 4 módulos inspirada em TextGrad: API Proposer (narrow down candidatos), API Executors (testes paralelos), API Selector (age como gradiente textual escolhendo a melhor chamada) e LLM Updater (revê query e resposta sintéticas)", "ToolGrad-12B (Gemma-3-12B fine-tuned) pontua 83.1 no BFCL, competitivo com gemini-2.5-pro (83.2) e claude-4.5 Opus (82.8), e à frente de gpt-5 (74.4), ToolACE e Hammer-2.1-7B", "Self-evolving: Gemma-3-12B fine-tuned em dados gerados por gemini-2.5-flash-lite supera o próprio modelo professor que gerou os dados", "Work futuro inclui escalar para ecossistemas de APIs dinâmicos e aprendizado contínuo on-the-fly para personalização"]
entities: ["ToolGrad", "Google Research", "Gemma-3", "Gemini", "gemini-2.5-flash-lite", "gemini-2.5-pro", "Claude-4.5 Opus", "GPT-5", "ToolBench", "ToolACE", "TextGrad", "Berkeley Function Calling Leaderboard", "Hammer-2.1-7B", "InstructPipe", "ACL 2026", "Zhongyi Zhou", "Ruofei Du"]
content_type: "announcement"
revisit: "high"
grounded_in: "article"
links: ["https://goo.gle/4xNKTNH"]
media: ["https://pbs.twimg.com/media/HR4-_mXbYAAtbYn.jpg"]
---

# ToolGrad: geração de datasets de tool-use

**@GoogleResearch** · [2098183830968705163](https://x.com/GoogleResearch/status/2098183830968705163) · `announcement`

## Resumo
Google Research apresenta ToolGrad (ACL 2026), framework que inverte o paradigma tradicional gerando primeiro a cadeia ground-truth de uso de ferramentas e só depois o prompt do usuário, atingindo quase 100% de pass rate na geração de dados com menor custo. Modelos Gemma-3 fine-tuned no dataset ToolGrad-500 igualam ou superam LLMs proprietários SoTA no Berkeley Function Calling Leaderboard.

## Pontos-chave
- Paradigma answer-first: anotar da solução de tool-use para a query é mais fácil e exige um único passo de LLM, versus o approach query-first com DFS agent (ToolBench/ToolACE) que destila trajetórias de exploração custosa
- Arquitetura iterativa de 4 módulos inspirada em TextGrad: API Proposer (narrow down candidatos), API Executors (testes paralelos), API Selector (age como gradiente textual escolhendo a melhor chamada) e LLM Updater (revê query e resposta sintéticas)
- ToolGrad-12B (Gemma-3-12B fine-tuned) pontua 83.1 no BFCL, competitivo com gemini-2.5-pro (83.2) e claude-4.5 Opus (82.8), e à frente de gpt-5 (74.4), ToolACE e Hammer-2.1-7B
- Self-evolving: Gemma-3-12B fine-tuned em dados gerados por gemini-2.5-flash-lite supera o próprio modelo professor que gerou os dados
- Work futuro inclui escalar para ecossistemas de APIs dinâmicos e aprendizado contínuo on-the-fly para personalização

## Links
- https://goo.gle/4xNKTNH

## Entidades
ToolGrad, Google Research, Gemma-3, Gemini, gemini-2.5-flash-lite, gemini-2.5-pro, Claude-4.5 Opus, GPT-5, ToolBench, ToolACE, TextGrad, Berkeley Function Calling Leaderboard, Hammer-2.1-7B, InstructPipe, ACL 2026, Zhongyi Zhou, Ruofei Du

> **Revisit:** `high` · **fonte:** `article`
