---
title: "AI Model vs Agentic Harness: What Actually Drives AI"
type: "extract"
source: "youtube"
video_id: "ZELPNFXJ4_o"
url: "https://www.youtube.com/watch?v=ZELPNFXJ4_o"
channel: "IBM Technology"
extracted: "2026-09-19"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-19-ai-model-vs-agentic-harness-what-actually-drives-ai--ZELPNFXJ4_o.txt]]"
tags: ["harness", "harness-engineering", "agent-loop", "agent-context", "context-engineering", "context-management", "agent-tooling", "agents", "memory-architecture", "verification", "model-selection", "analise-estrutural"]
thesis: "A diferença de desempenho entre produtos de IA vem menos do modelo subjacente e mais do agentic harness que o envolve — ferramentas, memória e agentic loop — sendo o agente a soma de modelo + harness, com a fronteira entre os dois cada vez mais fluida."
concepts: ["modelo de IA vs agentic harness", "metáfora do cérebro no pote (brain in a jar)", "agente = modelo + harness", "três componentes do harness: ferramentas, memória e agentic loop", "computer use (controle de cursor e tela)", "arquivos de instrução persistentes (agents.md) carregados a cada sessão", "compaction do contexto: sumarizar histórico e podar saídas redundantes de ferramentas", "busca seletiva no repositório (grep, busca semântica, índices de código) em vez de despejar o codebase no contexto", "agentic loop plan → act → observe → repeat", "verificação contínua no loop (testes, screenshots, modelo revisor separado)", "acesso à linha de comando como mecanismo genérico de ferramenta", "fronteira fluida: planejamento de longo horizonte e autoverificação migrando do harness para o modelo", "harness molda consistência via convenções e arquivos de projeto"]
tools: ["ChatGPT", "Claude", "MCP (Model Context Protocol)", "agents.md", "grep", "sandbox de execução de código", "computer use", "linha de comando/terminal"]
people: []
claims: ["Ao avaliar um produto de IA, pergunte separadamente qual modelo e qual harness estão sendo usados — um modelo brilhante em um harness pode travar em outro.", "Atribua a maior parte dos ganhos recentes de capacidade a melhorias de harness (ferramentas, tratamento de memória, loops com verificação), não apenas a modelos novos.", "Use MCP para que ferramentas se conectem a qualquer harness compatível sem serem reconstruídas a cada vez.", "Dê ao harness acesso à linha de comando para que o modelo reaproveite qualquer software já instalado na máquina.", "Persista convenções do projeto em um agents.md carregado no contexto no início de cada sessão.", "Implemente compaction: quando a janela de contexto encher, sumarize o que importa e pode saídas redundantes de ferramentas.", "Prefira busca seletiva (grep, semântica, índices de código) a injetar o repositório inteiro no contexto.", "Rode verificação continuamente ao longo do loop: testes, screenshots e um segundo modelo atuando como revisor para evitar deriva em tarefas longas.", "Reformule 'a IA é boa em X?' como 'qual modelo + qual harness para X?'", "Observe que capacidades antes exclusivas do harness (planejamento longo, autoverificação) estão sendo treinadas diretamente nos modelos, enquanto comportamentos do modelo (consistência) passam a ser moldados por convenções do harness."]
deep_dive: "medium"
deep_dive_reason: "É um primer introdutório bem estruturado sobre a anatomia do harness (ferramentas/memória/loop) com decomposição conceitual clara e diretamente relevante a harness e context-engineering, mas sem técnicas novas ou profundidade arquitetural além do nível básico."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-why-the-harness-matters-more-than-the-model-yc-paper-club--n9xKblqyQ28|Why The Harness Matters More Than The Model | YC Paper Club]]", "[[extracts/youtube/ai-learning/2026-09-11-harnesses-in-ai-a-deep-dive-tejas-kumar-ibm--C_GG5g38vLU|Harnesses in AI: A Deep Dive — Tejas Kumar, IBM]]", "[[extracts/youtube/ai-learning/2026-09-11-when-to-build-your-own-agent-harness-harrison-chase-langchain--HI2q3ci3Iuc|When to Build Your Own Agent Harness | Harrison Chase, LangChain]]", "[[extracts/youtube/ai-learning/2026-09-11-harness-engineering-what-separates-top-agentic-engineers-right-now--ulNsa0sD8N0|Harness Engineering: What Separates Top Agentic Engineers Right Now]]", "[[extracts/youtube/ai-learning/2026-09-11-harness-engineering-how-to-build-software-when-humans-steer-agents-execute-ryan--am_oeAoUhew|Harness Engineering: How to Build Software When Humans Steer, Agents Execute — Ryan Lopopolo, OpenAI]]", "[[extracts/youtube/ai-learning/2026-09-11-agentic-engineering-working-with-ai-not-just-using-it-brendan-o-leary--BEKc4P87XKo|Agentic Engineering: Working With AI, Not Just Using It — Brendan O'Leary]]"]
theme: "Agentic Coding Workflows"
---

# AI Model vs Agentic Harness: What Actually Drives AI

## Tese
A diferença de desempenho entre produtos de IA vem menos do modelo subjacente e mais do agentic harness que o envolve — ferramentas, memória e agentic loop — sendo o agente a soma de modelo + harness, com a fronteira entre os dois cada vez mais fluida.

## Conceitos-chave
- modelo de IA vs agentic harness
- metáfora do cérebro no pote (brain in a jar)
- agente = modelo + harness
- três componentes do harness: ferramentas, memória e agentic loop
- computer use (controle de cursor e tela)
- arquivos de instrução persistentes (agents.md) carregados a cada sessão
- compaction do contexto: sumarizar histórico e podar saídas redundantes de ferramentas
- busca seletiva no repositório (grep, busca semântica, índices de código) em vez de despejar o codebase no contexto
- agentic loop plan → act → observe → repeat
- verificação contínua no loop (testes, screenshots, modelo revisor separado)
- acesso à linha de comando como mecanismo genérico de ferramenta
- fronteira fluida: planejamento de longo horizonte e autoverificação migrando do harness para o modelo
- harness molda consistência via convenções e arquivos de projeto

## Ferramentas & pessoas
**Ferramentas:** ChatGPT, Claude, MCP (Model Context Protocol), agents.md, grep, sandbox de execução de código, computer use, linha de comando/terminal

**Pessoas/orgs:** —

## Claims acionáveis
- Ao avaliar um produto de IA, pergunte separadamente qual modelo e qual harness estão sendo usados — um modelo brilhante em um harness pode travar em outro.
- Atribua a maior parte dos ganhos recentes de capacidade a melhorias de harness (ferramentas, tratamento de memória, loops com verificação), não apenas a modelos novos.
- Use MCP para que ferramentas se conectem a qualquer harness compatível sem serem reconstruídas a cada vez.
- Dê ao harness acesso à linha de comando para que o modelo reaproveite qualquer software já instalado na máquina.
- Persista convenções do projeto em um agents.md carregado no contexto no início de cada sessão.
- Implemente compaction: quando a janela de contexto encher, sumarize o que importa e pode saídas redundantes de ferramentas.
- Prefira busca seletiva (grep, semântica, índices de código) a injetar o repositório inteiro no contexto.
- Rode verificação continuamente ao longo do loop: testes, screenshots e um segundo modelo atuando como revisor para evitar deriva em tarefas longas.
- Reformule 'a IA é boa em X?' como 'qual modelo + qual harness para X?'
- Observe que capacidades antes exclusivas do harness (planejamento longo, autoverificação) estão sendo treinadas diretamente nos modelos, enquanto comportamentos do modelo (consistência) passam a ser moldados por convenções do harness.

> **Deep dive:** `medium` — É um primer introdutório bem estruturado sobre a anatomia do harness (ferramentas/memória/loop) com decomposição conceitual clara e diretamente relevante a harness e context-engineering, mas sem técnicas novas ou profundidade arquitetural além do nível básico.
