---
title: "Ryan Lopopolo - Harness Engineering: How to Build Software When Humans Steer and Agents Execute"
type: "extract"
source: "youtube"
video_id: "c8bE0cj7vHY"
url: "https://www.youtube.com/watch?v=c8bE0cj7vHY"
channel: "AI Native Dev"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-ryan-lopopolo-harness-engineering-how-to-build-software-when-humans-steer-and-ag--c8bE0cj7vHY.txt]]"
tags: ["harness-engineering", "harness", "context-engineering", "context-management", "code-review", "agent-loop", "agentic-coding", "gate-design", "verification", "testes-qa", "error-handling", "knowledge-management", "multi-agent", "evals", "stack-tooling", "decision-discipline"]
thesis: "Harness engineering consiste em tornar legível e entregar just-in-time ao agente de código o contexto do que significa 'fazer um bom trabalho' — via loop operacional escrito, guardrails estáticos e revisores-LLM — para que cada feedback humano vire uma restrição permanente e nenhum erro se repita."
concepts: ["harness engineering", "just-in-time prompt injection via saídas de tool calls", "auto compaction da janela de contexto", "atenção humana e do modelo como limite fundamental (attention soma a 1)", "code base como prompt", "loop operacional numerado no arquivo do agente (grounding → execução → revisão)", "personas de revisão como guardrails em markdown", "LLM-as-judge colaborando no thread do PR", "guardrails estáticos (lint, tipagem, cobertura, snapshot tests)", "shift right das intervenções humanas (em vez de shift left)", "captura sistemática de feedback humano como sinal de contexto faltante", "poda do latent space via codificação de decisões do time", "agente como membro do time com bias toward merge e evidências", "tempo humano síncrono como recurso escasso e paralelização de sessões"]
tools: ["OpenAI Codex CLI", "Codex app (computer use / browser use / automations)", "GPT-5.2", "Claude Opus 4.5", "o3 (modelo de raciocínio)", "Slack", "ESLint", "ffmpeg", "Docker", "Xvfb/headless display", "React", "VS Code", "Artichoke (interpretador Ruby em Rust)", "artichoke-rand-mt (Mersenne Twister)"]
people: ["Ryan (palestrante, OpenAI)", "OpenAI", "Anthropic (Claude Opus 4.5, citado)", "AI Native DevCon"]
claims: ["Com agentes, os limites fundamentais passam a ser tempo humano síncrono, atenção (que soma a 1) e janela de contexto — projete o trabalho para remover atenção humana do processo e rodar sessões em paralelo", "Nunca dê o mesmo feedback de revisão duas vezes: converta cada erro recorrente em guardrail estático (lint, teste, checagem) que torna o erro impossível", "Posicione intervenções o mais à direita possível no pipeline e só desloque para a esquerda quando feedback recorrente chegar à etapa final ou quando guardrails forem perdidos em auto compaction em tarefas de 15+ janelas de contexto", "Escreva um loop operacional numerado no arquivo do agente: grounding em docs/ticket, spider por ADRs e design docs, e checagem de critical user journeys antes de codar", "Exploite o fato de que saídas de tool calls recebem menos peso na auto compaction para corrigir o modelo just-in-time sem poluir o contexto inicial", "Escreva testes especificamente para agentes: mensagens de erro descritivas apontando para runbooks de remediação, tolerando truncamento de outputs — diferentes dos testes para humanos", "Bana estaticamente tipos any/unknown (exceto em boundaries como handlers de input raiz e banco) e exija 100% de tipagem para eliminar type-shaped probing", "Exigir snapshot test com 100% branch coverage por componente React induz naturalmente decomposição, pureza e fim do prop drilling", "Implemente revisores-agente como matrix CI job apontando para markdowns de personas/guardrails; LLMs-juíze colaboram no thread do PR e o agente implementador se autocorrige", "Capture todo review comment, interrupção humana, build falho e exceção de produção como sinal de contexto faltante e rode subagentes sobre esses dados (nightly) para destilar guardrails ausentes e prompts melhores", "Padronize stacks no repositório (ex.: um único stack de observabilidade), pois o código em si é prompt e padrões unificados reduzem a atenção que o modelo gasta para escolher entre alternativas", "Trate o merge como ato social: biased toward merge, exigindo evidências do agente (logs de staging, screenshots, vídeo de reprodução via computer use/browser use) como faria com um colega humano", "Converta conversas em threads do Slack em guardrails: mencione o agente na thread e peça um PR que adicione o conteúdo ao set estático de guardrails — forma barata de socializar melhorias para o time", "O humano deve operar como group tech lead: cuidar de invariantes, interfaces e confiabilidade dos artefatos, não de supervisionar a digitação do agente"]
deep_dive: "high"
deep_dive_reason: "Alta densidade de padrões arquiteturais acionáveis e inéditos (injeção just-in-time via tool outputs, revisores como CI job, feedback→guardrail estático, shift right) diretamente no núcleo de harness e context engineering, vindos de um praticante da OpenAI que afirma ter cunhado o termo."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-harness-engineering-how-to-build-software-when-humans-steer-agents-execute-ryan--am_oeAoUhew|Harness Engineering: How to Build Software When Humans Steer, Agents Execute — Ryan Lopopolo, OpenAI]]", "[[extracts/youtube/ai-learning/2026-09-11-harness-engineering-what-separates-top-agentic-engineers-right-now--ulNsa0sD8N0|Harness Engineering: What Separates Top Agentic Engineers Right Now]]", "[[extracts/youtube/ai-learning/2026-09-11-the-engineer-of-the-future-is-the-person-who-is-able-to-choose-what-is-worth-doi--n97BCfyFIvw|\"The engineer of the future is the person who is able to choose what is worth doing.\" — Addy Osmani]]", "[[extracts/youtube/ai-learning/2026-09-11-ex-nasa-dev-reveals-his-agentic-engineering-workflow--xgkjtF89-44|Ex-NASA dev reveals his Agentic Engineering Workflow]]", "[[extracts/youtube/ai-learning/2026-09-11-the-golden-age-of-ai-engineering-alexander-embiricos-romain-huet-peter-steinberg--pMggiOb18tc|The Golden Age of AI Engineering — Alexander Embiricos & Romain Huet & Peter Steinberger, OpenAI]]", "[[extracts/youtube/ai-learning/2026-09-11-when-to-build-your-own-agent-harness-harrison-chase-langchain--HI2q3ci3Iuc|When to Build Your Own Agent Harness | Harrison Chase, LangChain]]", "[[extracts/youtube/ai-learning/2026-09-11-harness-engineering-is-not-enough-why-software-factories-fail-dex-horthy-humanla--Ib5GBkD555M|Harness Engineering is not Enough: Why Software Factories Fail — Dex Horthy, HumanLayer]]", "[[extracts/youtube/ai-learning/2026-09-11-harnesses-in-ai-a-deep-dive-tejas-kumar-ibm--C_GG5g38vLU|Harnesses in AI: A Deep Dive — Tejas Kumar, IBM]]", "[[extracts/youtube/ai-learning/2026-09-11-bdd-adr-prd-wtf-capturing-decisions-for-humans-and-ai-alike-michal-cichra-safe-i--504PvfXou5Y|BDD, ADR, PRD, WTF: Capturing Decisions for Humans and AI Alike — Michal Cichra, Safe Intelligence]]", "[[extracts/youtube/ai-learning/2026-09-11-wtf-is-loop-engineer-how-to-setup-for-real--W6x-hb44C0c|wtf is Loop Engineer & how to setup for real]]"]
theme: "Processo de Engenharia Agêntica"
---

# Ryan Lopopolo - Harness Engineering: How to Build Software When Humans Steer and Agents Execute

## Tese
Harness engineering consiste em tornar legível e entregar just-in-time ao agente de código o contexto do que significa 'fazer um bom trabalho' — via loop operacional escrito, guardrails estáticos e revisores-LLM — para que cada feedback humano vire uma restrição permanente e nenhum erro se repita.

## Conceitos-chave
- harness engineering
- just-in-time prompt injection via saídas de tool calls
- auto compaction da janela de contexto
- atenção humana e do modelo como limite fundamental (attention soma a 1)
- code base como prompt
- loop operacional numerado no arquivo do agente (grounding → execução → revisão)
- personas de revisão como guardrails em markdown
- LLM-as-judge colaborando no thread do PR
- guardrails estáticos (lint, tipagem, cobertura, snapshot tests)
- shift right das intervenções humanas (em vez de shift left)
- captura sistemática de feedback humano como sinal de contexto faltante
- poda do latent space via codificação de decisões do time
- agente como membro do time com bias toward merge e evidências
- tempo humano síncrono como recurso escasso e paralelização de sessões

## Ferramentas & pessoas
**Ferramentas:** OpenAI Codex CLI, Codex app (computer use / browser use / automations), GPT-5.2, Claude Opus 4.5, o3 (modelo de raciocínio), Slack, ESLint, ffmpeg, Docker, Xvfb/headless display, React, VS Code, Artichoke (interpretador Ruby em Rust), artichoke-rand-mt (Mersenne Twister)

**Pessoas/orgs:** Ryan (palestrante, OpenAI), OpenAI, Anthropic (Claude Opus 4.5, citado), AI Native DevCon

## Claims acionáveis
- Com agentes, os limites fundamentais passam a ser tempo humano síncrono, atenção (que soma a 1) e janela de contexto — projete o trabalho para remover atenção humana do processo e rodar sessões em paralelo
- Nunca dê o mesmo feedback de revisão duas vezes: converta cada erro recorrente em guardrail estático (lint, teste, checagem) que torna o erro impossível
- Posicione intervenções o mais à direita possível no pipeline e só desloque para a esquerda quando feedback recorrente chegar à etapa final ou quando guardrails forem perdidos em auto compaction em tarefas de 15+ janelas de contexto
- Escreva um loop operacional numerado no arquivo do agente: grounding em docs/ticket, spider por ADRs e design docs, e checagem de critical user journeys antes de codar
- Exploite o fato de que saídas de tool calls recebem menos peso na auto compaction para corrigir o modelo just-in-time sem poluir o contexto inicial
- Escreva testes especificamente para agentes: mensagens de erro descritivas apontando para runbooks de remediação, tolerando truncamento de outputs — diferentes dos testes para humanos
- Bana estaticamente tipos any/unknown (exceto em boundaries como handlers de input raiz e banco) e exija 100% de tipagem para eliminar type-shaped probing
- Exigir snapshot test com 100% branch coverage por componente React induz naturalmente decomposição, pureza e fim do prop drilling
- Implemente revisores-agente como matrix CI job apontando para markdowns de personas/guardrails; LLMs-juíze colaboram no thread do PR e o agente implementador se autocorrige
- Capture todo review comment, interrupção humana, build falho e exceção de produção como sinal de contexto faltante e rode subagentes sobre esses dados (nightly) para destilar guardrails ausentes e prompts melhores
- Padronize stacks no repositório (ex.: um único stack de observabilidade), pois o código em si é prompt e padrões unificados reduzem a atenção que o modelo gasta para escolher entre alternativas
- Trate o merge como ato social: biased toward merge, exigindo evidências do agente (logs de staging, screenshots, vídeo de reprodução via computer use/browser use) como faria com um colega humano
- Converta conversas em threads do Slack em guardrails: mencione o agente na thread e peça um PR que adicione o conteúdo ao set estático de guardrails — forma barata de socializar melhorias para o time
- O humano deve operar como group tech lead: cuidar de invariantes, interfaces e confiabilidade dos artefatos, não de supervisionar a digitação do agente

> **Deep dive:** `high` — Alta densidade de padrões arquiteturais acionáveis e inéditos (injeção just-in-time via tool outputs, revisores como CI job, feedback→guardrail estático, shift right) diretamente no núcleo de harness e context engineering, vindos de um praticante da OpenAI que afirma ter cunhado o termo.
