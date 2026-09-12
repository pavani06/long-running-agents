---
title: "The Art of Loop Engineering: How to Build Agents That Improve Over Time"
type: "extract"
source: "youtube"
video_id: "jPPiZ22DY3g"
url: "https://www.youtube.com/watch?v=jPPiZ22DY3g"
channel: "LangChain"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-the-art-of-loop-engineering-how-to-build-agents-that-improve-over-time--jPPiZ22DY3g.txt]]"
tags: ["agent-loop", "harness-engineering", "verification", "evals", "gate-design", "memory-architecture", "context-engineering", "token-budgeting", "tracing", "observability", "multi-agent", "runtime", "production", "agent-tooling"]
thesis: "O diferencial competitivo dos agentes não está no agente em si, mas nos quatro loops aninhados construídos ao seu redor — agent loop núcleo, verification loop, event-driven loop e self-improvement loop — que progressivamente automatizam a execução, a confiabilidade, a escala e a melhoria contínua do próprio harness."
concepts: ["Engenharia de loops (taxonomia de 4 níveis aninhados e combináveis)", "Agent loop núcleo (modelo → chamada de ferramentas → observações, até concluir a tarefa)", "Verification loop / loop /goal (grader pontuando contra rubrica e critérios explícitos)", "Event-driven loop (gatilhos agendados ou por evento integrados a Slack, Gmail e GitHub)", "Self-improvement / hill climbing loop (agente auxiliar analisando traces para atualizar o harness)", "Harness do agente (modelo + ferramentas + prompts + skills + memória em torno do modelo)", "Ciclo de vida de desenvolvimento de agentes (build, test, deploy, monitor)", "Middleware de rubrica/goal plugável e stack de middleware composável", "Consolidação de memória entre execuções (melhorias procedurais vs. semânticas/preferências de usuário)", "Posicionamento de human-in-the-loop em 4 pontos (tool calls sensíveis, ciclo do grader, artefatos/PRs, mudanças de harness)", "Dois tipos de evals: baseline tipo unit-test e end-to-end desafiador para hill climbing", "Compressão de prompts para mitigar context rot e custo em loops longos", "Trade-off latency × custo × corretude na seleção de modelo e rigidez do grader", "Guardrails de runtime: timeouts e limite máximo de ciclos em sub-agentes", "Traces como fonte de verdade para agentes não-determinísticos", "Memória estruturada como wiki do repositório e wikis pessoais semânticas"]
tools: ["LangSmith", "LangChain", "LangGraph", "Deep Agents", "Decode", "LangSmith Engine", "LangSmith Fleet", "Open Wiki", "Eval engineering (skill/blog da LangChain)", "Claude Code", "Codex", "Slack", "Gmail", "OLM Gateway (LangSmith)"]
people: ["Sydney (product manager do time open source da LangChain)", "LangChain", "Nick (time open source da LangChain)"]
claims: ["Selecione o modelo proporcional à complexidade da tarefa e otimize as descrições de ferramentas no loop núcleo para equilibrar custo e capacidade.", "Adicione um grader com rubrica explícita e revisável após o ciclo do agente; exibir os critérios ao usuário (como o /goal do Decode) aumenta transparência e controle fino.", "Use loops de verificação para permitir modelos mais baratos em tarefas difíceis, aceitando o trade-off de maior latency.", "Plugue o middleware de rubrica/goal open source em qualquer agente (ex.: deep agents) para ganhar confiabilidade sem reescrever o harness.", "Integre gatilhos agendados ou por evento (Slack, Gmail, GitHub) para que os agentes sejam efetivamente usados e melhorem os sistemas onde estão embutidos.", "Rode um agente auxiliar sobre os traces após cada execução para detectar modos de falha (argumentos errados, tool call crítica ausente, preferências ignoradas) e propor mudanças no harness.", "Priorize mudanças em memória, skills e prompts antes de alterar arquitetura/runtime; mude o runtime apenas quando um passo determinístico (ex.: compliance) for necessário.", "Não feche o loop de self-improvement sem uma suite de evals que justifique os merges e detecte regressões.", "Mantenha dois tipos de evals: baseline tipo unit-test para funcionalidade mínima e evals end-to-end desafiadores sobre os quais fazer hill climbing.", "Posicione human approval em quatro pontos: tool calls sensíveis (ex.: enviar email, reservar viagem), ciclo do grader/verificador, artefatos de resultado (PRs) e mudanças de código do harness.", "Use discrição do modelo para decidir quando aprovação humana é necessária e direcione aprovações ao usuário final quando possível, para escalar os fluxos em produção.", "Comprima prompts e iterações anteriores ao reentrar no loop de nova tentativa (mantendo artifact atual + rubrica) para mitigar context rot e custo em loops longos.", "Aplique guardrails como timeouts e número máximo de ciclos em sub-agentes para conter a latency acumulada dos loops.", "Quando o sinal de recompensa é ambíguo, use anotação humana dos critérios gerados para treinar o gerador/avaliador de critérios do grader.", "Estruture memória em duas frentes: wiki do repositório para travessia eficiente por coding agents e wikis pessoais semânticas, atualizadas pelo próprio loop de self-improvement.", "Versione todas as mudanças de harness propostas por agentes de melhoria e audite-as via traces com visão de trajetória e breadcrumbs de impacto nas ferramentas.", "Autogenere evals a partir de traces ao vivo com o contexto do repositório (skill de eval engineering) quando não há ground truth disponível."]
deep_dive: "medium"
deep_dive_reason: "Oferece uma taxonomia arquitetural clara (quatro loops) com conselhos acionáveis em Q&A sobre graders, evals, memória e human-in-the-loop altamente relevantes para harness e evals, mas grande parte sintetiza práticas já estabelecidas e carrega viés promocional da plataforma LangSmith."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-ex-nasa-dev-reveals-his-agentic-engineering-workflow--xgkjtF89-44|Ex-NASA dev reveals his Agentic Engineering Workflow]]", "[[extracts/youtube/ai-learning/2026-09-11-loop-engineering-to-graph-engineering--BOOfy3Yshtw|Loop Engineering to Graph Engineering]]", "[[extracts/youtube/ai-learning/2026-09-11-when-to-build-your-own-agent-harness-harrison-chase-langchain--HI2q3ci3Iuc|When to Build Your Own Agent Harness | Harrison Chase, LangChain]]", "[[extracts/youtube/ai-learning/2026-09-11-wtf-is-loop-engineer-how-to-setup-for-real--W6x-hb44C0c|wtf is Loop Engineer & how to setup for real]]", "[[extracts/youtube/ai-learning/2026-09-11-the-golden-age-of-ai-engineering-alexander-embiricos-romain-huet-peter-steinberg--pMggiOb18tc|The Golden Age of AI Engineering — Alexander Embiricos & Romain Huet & Peter Steinberger, OpenAI]]", "[[extracts/youtube/ai-learning/2026-09-11-l8-principal-s-agentic-engineering-setup-just-copy-him--8ZgpAXe5V5w|L8 Principal's Agentic Engineering Setup (just copy him)]]", "[[extracts/youtube/ai-learning/2026-09-11-7-insane-loops-you-need-to-try-right-now--F4a8aMLb678|7 INSANE loops you need to try right now]]", "[[extracts/youtube/ai-learning/2026-09-11-anthropic-workshop-build-agents-that-run-for-hours-ash-prabaker-andrew-wilson--mR-WAvEPRwE|Anthropic Workshop: Build Agents That Run for Hours — Ash Prabaker & Andrew Wilson]]", "[[extracts/youtube/ai-learning/2026-09-11-deep-agents-explained--GbzEDgcuGJU|Deep Agents Explained]]", "[[extracts/youtube/ai-learning/2026-09-11-why-more-context-makes-your-agent-dumber-and-what-to-do-about-it-nupur-sharma-qo--EcqMYoIV57A|Why More Context Makes Your Agent Dumber and What to Do About It — Nupur Sharma, Qodo]]", "[[extracts/youtube/ai-learning/2026-09-11-hard-won-lessons-from-building-effective-ai-coding-agents-nik-pash-cline--I8fs4omN1no|Hard Won Lessons from Building Effective AI Coding Agents – Nik Pash, Cline]]", "[[extracts/youtube/ai-learning/2026-09-11-how-lovable-self-improves-every-hour-benjamin-verbeek-lovable--KA5kPbdkK2E|How Lovable self-improves every hour — Benjamin Verbeek, Lovable]]", "[[extracts/youtube/ai-learning/2026-09-11-building-closed-loop-evals-for-a-multimodal-agent-at-scale-soumya-gupta-jai-chop--31GUkCBD-Uc|Building Closed-Loop Evals for a Multimodal Agent at Scale — Soumya Gupta & Jai Chopra, Uber]]", "[[extracts/youtube/ai-learning/2026-09-11-pi-architecture-explained-agent-loop-tools-tui-and-more--gTeujlv8qK0|PI Architecture EXPLAINED | Agent Loop, Tools, TUI and More]]"]
---

# The Art of Loop Engineering: How to Build Agents That Improve Over Time

## Tese
O diferencial competitivo dos agentes não está no agente em si, mas nos quatro loops aninhados construídos ao seu redor — agent loop núcleo, verification loop, event-driven loop e self-improvement loop — que progressivamente automatizam a execução, a confiabilidade, a escala e a melhoria contínua do próprio harness.

## Conceitos-chave
- Engenharia de loops (taxonomia de 4 níveis aninhados e combináveis)
- Agent loop núcleo (modelo → chamada de ferramentas → observações, até concluir a tarefa)
- Verification loop / loop /goal (grader pontuando contra rubrica e critérios explícitos)
- Event-driven loop (gatilhos agendados ou por evento integrados a Slack, Gmail e GitHub)
- Self-improvement / hill climbing loop (agente auxiliar analisando traces para atualizar o harness)
- Harness do agente (modelo + ferramentas + prompts + skills + memória em torno do modelo)
- Ciclo de vida de desenvolvimento de agentes (build, test, deploy, monitor)
- Middleware de rubrica/goal plugável e stack de middleware composável
- Consolidação de memória entre execuções (melhorias procedurais vs. semânticas/preferências de usuário)
- Posicionamento de human-in-the-loop em 4 pontos (tool calls sensíveis, ciclo do grader, artefatos/PRs, mudanças de harness)
- Dois tipos de evals: baseline tipo unit-test e end-to-end desafiador para hill climbing
- Compressão de prompts para mitigar context rot e custo em loops longos
- Trade-off latency × custo × corretude na seleção de modelo e rigidez do grader
- Guardrails de runtime: timeouts e limite máximo de ciclos em sub-agentes
- Traces como fonte de verdade para agentes não-determinísticos
- Memória estruturada como wiki do repositório e wikis pessoais semânticas

## Ferramentas & pessoas
**Ferramentas:** LangSmith, LangChain, LangGraph, Deep Agents, Decode, LangSmith Engine, LangSmith Fleet, Open Wiki, Eval engineering (skill/blog da LangChain), Claude Code, Codex, Slack, Gmail, OLM Gateway (LangSmith)

**Pessoas/orgs:** Sydney (product manager do time open source da LangChain), LangChain, Nick (time open source da LangChain)

## Claims acionáveis
- Selecione o modelo proporcional à complexidade da tarefa e otimize as descrições de ferramentas no loop núcleo para equilibrar custo e capacidade.
- Adicione um grader com rubrica explícita e revisável após o ciclo do agente; exibir os critérios ao usuário (como o /goal do Decode) aumenta transparência e controle fino.
- Use loops de verificação para permitir modelos mais baratos em tarefas difíceis, aceitando o trade-off de maior latency.
- Plugue o middleware de rubrica/goal open source em qualquer agente (ex.: deep agents) para ganhar confiabilidade sem reescrever o harness.
- Integre gatilhos agendados ou por evento (Slack, Gmail, GitHub) para que os agentes sejam efetivamente usados e melhorem os sistemas onde estão embutidos.
- Rode um agente auxiliar sobre os traces após cada execução para detectar modos de falha (argumentos errados, tool call crítica ausente, preferências ignoradas) e propor mudanças no harness.
- Priorize mudanças em memória, skills e prompts antes de alterar arquitetura/runtime; mude o runtime apenas quando um passo determinístico (ex.: compliance) for necessário.
- Não feche o loop de self-improvement sem uma suite de evals que justifique os merges e detecte regressões.
- Mantenha dois tipos de evals: baseline tipo unit-test para funcionalidade mínima e evals end-to-end desafiadores sobre os quais fazer hill climbing.
- Posicione human approval em quatro pontos: tool calls sensíveis (ex.: enviar email, reservar viagem), ciclo do grader/verificador, artefatos de resultado (PRs) e mudanças de código do harness.
- Use discrição do modelo para decidir quando aprovação humana é necessária e direcione aprovações ao usuário final quando possível, para escalar os fluxos em produção.
- Comprima prompts e iterações anteriores ao reentrar no loop de nova tentativa (mantendo artifact atual + rubrica) para mitigar context rot e custo em loops longos.
- Aplique guardrails como timeouts e número máximo de ciclos em sub-agentes para conter a latency acumulada dos loops.
- Quando o sinal de recompensa é ambíguo, use anotação humana dos critérios gerados para treinar o gerador/avaliador de critérios do grader.
- Estruture memória em duas frentes: wiki do repositório para travessia eficiente por coding agents e wikis pessoais semânticas, atualizadas pelo próprio loop de self-improvement.
- Versione todas as mudanças de harness propostas por agentes de melhoria e audite-as via traces com visão de trajetória e breadcrumbs de impacto nas ferramentas.
- Autogenere evals a partir de traces ao vivo com o contexto do repositório (skill de eval engineering) quando não há ground truth disponível.

> **Deep dive:** `medium` — Oferece uma taxonomia arquitetural clara (quatro loops) com conselhos acionáveis em Q&A sobre graders, evals, memória e human-in-the-loop altamente relevantes para harness e evals, mas grande parte sintetiza práticas já estabelecidas e carrega viés promocional da plataforma LangSmith.
