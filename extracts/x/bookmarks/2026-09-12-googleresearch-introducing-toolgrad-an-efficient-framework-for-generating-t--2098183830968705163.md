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
thin: false
theme: "Tooling agêntico de engenharia"
relates-to: ["[[extracts/x/bookmarks/2026-09-12-hackernoon-ai-is-raising-the-baseline-for-software-engineering-this-art--2082839180736889054|AI e plataformas de engenharia]]", "[[extracts/x/bookmarks/2026-09-12-dair_ai-the-bitter-lesson-of-tool-calling-tool-calling-is-a-design-c--2086846794840019178|Comparação de métodos de tool calling]]", "[[extracts/x/bookmarks/2026-09-12-openhonor-puro-2b-is-open-beyond-the-weights-technical-report-final-in--2093994412770566256|Puro-2B: receita aberta de pré-treinamento barato]]", "[[extracts/x/bookmarks/2026-09-12-sumanth_077-bytedance-dropped-a-banger-paper-on-self-evolving-agent-harn--2098053941800100294|HarnessDev: self-evolving agent harnesses]]", "[[extracts/x/bookmarks/2026-09-12-akshay_pachaar-karpathys-agentic-engineering-finally-has-proper-devtools-wh--2098398242727940442|DevTools para engenharia agêntica]]", "[[extracts/x/bookmarks/2026-09-12-simonw-here-s-my-attempt-at-explaining-what-chatgpt-work-can-actual--2094214737957691854|Capacidades do ChatGPT Work]]", "[[extracts/x/bookmarks/2026-09-12-pythonhub-soup-fine-tune-and-post-train-llms-in-one-command-no-ssh-no--2092662174443249870|Ferramenta CLI de fine-tuning de LLMs]]", "[[extracts/x/bookmarks/2026-09-12-marwan_3atef-google-cloud-put-data-agent-kit-in-the-ide-and-the-pitch-is--2097976275373531523|Data Agent Kit no IDE]]", "[[extracts/x/bookmarks/2026-09-12-googleresearch-introducing-timesfm-3-a-state-of-the-art-time-series-foundat--2094483372718580066|TimesFM-3: forecasting multivariado]]", "[[extracts/x/bookmarks/2026-09-12-fazle_karim1-googleresearch-i-wonder-how-it-would-do-on-this-research-of--2094501145536315670|GlucoFM: foundation model para CGM]]", "[[extracts/x/bookmarks/2026-09-12-askalphaxiv-introducing-deepseek-v4-1-flash-for-understanding-research-p--2098309348858704095|alphaXiv AI paper Q&A]]"]
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
