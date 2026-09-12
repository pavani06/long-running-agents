---
title: "Dynamic Subagents: How to Run Parallel Agents Reliably in Deep Agents"
type: "extract"
source: "youtube"
video_id: "5AkdMangfNk"
url: "https://www.youtube.com/watch?v=5AkdMangfNk"
channel: "LangChain"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-dynamic-subagents-how-to-run-parallel-agents-reliably-in-deep-agents--5AkdMangfNk.txt]]"
tags: ["agent-fleets", "agent-loop", "agent-tooling", "agentes-orquestracao", "agentic-coding", "classification", "code-review", "context-engineering", "context-management", "harness", "multi-agent", "observability", "state", "tracing", "verification"]
thesis: "A tese central é que mover a orquestração de subagentes da cabeça do agente (chamadas de ferramenta turno a turno) para código escrito pelo próprio agente — via dynamic subagents com middleware de interpretação de código — torna a decomposição de tarefas grandes em paralelo confiável e completa em escala."
concepts: ["Subagentes dinâmicos (spawn e coordenação programáticos via código)", "Isolamento de contexto (cada subagente roda em sua própria janela de contexto)", "Orquestração em código vs. orquestração no raciocínio do agente", "Code interpreter middleware (sandbox leve in-memory com ferramenta eval)", "Task global (chamada programática await task com descrição, tipo de subagente e response schema)", "Response schemas geradas dinamicamente (resultados tipados que permitem loop/branch)", "Palavra-chave 'workflow' como gatilho para escrever código de orquestração", "Seis padrões de orquestração: Classify and Act, Fan Out and Synthesize, Adversarial Verification, Generate and Filter, Tournament, Loop Until Done", "Variáveis persistentes entre chamadas eval (ex.: all_findings) para fluxos iterativos", "Steering por fraseamento do prompt ('every', 'double check', 'comparing against each other', 'don't stop until')", "Confiabilidade em escala: loops garantem cobertura completa sem depender da discrição do agente", "Controle de fluxo real (loops, branching, retries, paralelismo) em poucas linhas de código"]
tools: ["Deep Agents SDK", "Decode (agente de codificação em terminal da LangChain)", "LangSmith (traces)", "Code interpreter middleware", "eval tool", "task tool / task global"]
people: ["Colin (engenheiro de software na LangChain)", "LangChain", "Anthropic (originadora dos padrões de dynamic workflows)"]
claims: ["Anexe o code interpreter middleware ao seu Deep Agent para habilitar subagentes dinâmicos; em Decode o recurso já vem ativado por padrão.", "Use a palavra-chave 'workflow' na requisição para sinalizar explicitamente que o agente deve escrever código de orquestração em vez de decidir sozinho.", "Passe uma response schema gerada dinamicamente na task global para que o resultado volte tipado, permitindo que o agente faça loop ou branch sobre ele em código.", "Mova orquestração repetitiva (centenas de chamadas) para loops em código para eliminar omissões, encerramentos precoces e trajetórias ruins do agente.", "Faça o steering de cada padrão pelo fraseamento: 'every/all + um resumo único' (Fan Out and Synthesize), 'double check / só os confirmados' (Adversarial Verification), 'várias abordagens e escolha a melhor' (Generate and Filter), 'head-to-head / torneio' (Tournament), 'não pare até não haver nada novo' (Loop Until Done), 'figure out what each one is' (Classify and Act).", "Variáveis criadas em uma chamada eval persistem para as chamadas seguintes, permitindo workflows multi-etapa iterativos sem poluir o contexto principal.", "No padrão Adversarial Verification, rode uma passada ampla de candidatos e uma segunda passada de verificadores independentes, reportando apenas o que sobreviver à verificação.", "A descrição passada a cada subagente funciona como system prompt customizado e pode ser variada por item (ex.: por tipo de arquivo).", "Prefira escrever artefatos em arquivos (sem response schema) quando o produto é o arquivo em si; use schemas tipadas quando o resultado precisa alimentar código posterior.", "Subagentes mantêm o contexto do agente principal limpo: apenas o resultado final retorna ao contexto, mesmo com subagentes fazendo dezenas de tool calls.", "O agente pode misturar chamadas eval (fan-out programático) com chamadas regulares da task tool, preservando flexibilidade na decomposição.", "Use traces do LangSmith para inspecionar cada fase de fan-out, as chamadas eval, os tipos de subagente acionados e os schemas gerados."]
deep_dive: "high"
deep_dive_reason: "Alta densidade de insight acionável e arquitetural — API do middleware, task global tipada, estado persistente entre evals e seis padrões de orquestração com heurísticas de steering — diretamente relevante a harness, agent-fleets, context-engineering e verificação."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-deep-agents-explained--GbzEDgcuGJU|Deep Agents Explained]]", "[[extracts/youtube/ai-learning/2026-09-11-tool-skill-or-subagent-decomposing-an-agent-that-outgrew-its-prompt--mWvtOHlZM-I|Tool, skill, or subagent? Decomposing an agent that outgrew its prompt]]", "[[extracts/youtube/ai-learning/2026-09-11-introducing-managed-deep-agents-interrupt-26--LdQpoK2TzSo|Introducing Managed Deep Agents | Interrupt 26]]", "[[extracts/youtube/ai-learning/2026-09-11-the-best-ai-agents-need-less-code-than-you-think--YqjR4vQwbTc|The best AI agents need less code than you think]]", "[[extracts/youtube/ai-learning/2026-09-11-the-agent-development-lifecycle-build-test-deploy-monitor-interrupt-26--jWy39wavbjY|The Agent Development Lifecycle: Build, Test, Deploy, Monitor | Interrupt 26]]", "[[extracts/youtube/ai-learning/2026-09-11-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipeline--Uny6LpmjraI|Inside Clay's Eval Stack: 300M Agent Runs, One LangSmith Pipeline]]", "[[extracts/youtube/ai-learning/2026-09-11-how-to-use-rlms-in-deep-agents--5_LLMZfKI6w|How to use RLMs in Deep Agents]]", "[[extracts/youtube/ai-learning/2026-09-11-hermes-deepseek-4-minimax-2-7-multi-model-coding-on-a-zimaboard---3MPnUGqa68|Hermes + DeepSeek 4 + MiniMax 2.7: Multi-Model Coding on a ZimaBoard]]"]
---

# Dynamic Subagents: How to Run Parallel Agents Reliably in Deep Agents

## Tese
A tese central é que mover a orquestração de subagentes da cabeça do agente (chamadas de ferramenta turno a turno) para código escrito pelo próprio agente — via dynamic subagents com middleware de interpretação de código — torna a decomposição de tarefas grandes em paralelo confiável e completa em escala.

## Conceitos-chave
- Subagentes dinâmicos (spawn e coordenação programáticos via código)
- Isolamento de contexto (cada subagente roda em sua própria janela de contexto)
- Orquestração em código vs. orquestração no raciocínio do agente
- Code interpreter middleware (sandbox leve in-memory com ferramenta eval)
- Task global (chamada programática await task com descrição, tipo de subagente e response schema)
- Response schemas geradas dinamicamente (resultados tipados que permitem loop/branch)
- Palavra-chave 'workflow' como gatilho para escrever código de orquestração
- Seis padrões de orquestração: Classify and Act, Fan Out and Synthesize, Adversarial Verification, Generate and Filter, Tournament, Loop Until Done
- Variáveis persistentes entre chamadas eval (ex.: all_findings) para fluxos iterativos
- Steering por fraseamento do prompt ('every', 'double check', 'comparing against each other', 'don't stop until')
- Confiabilidade em escala: loops garantem cobertura completa sem depender da discrição do agente
- Controle de fluxo real (loops, branching, retries, paralelismo) em poucas linhas de código

## Ferramentas & pessoas
**Ferramentas:** Deep Agents SDK, Decode (agente de codificação em terminal da LangChain), LangSmith (traces), Code interpreter middleware, eval tool, task tool / task global

**Pessoas/orgs:** Colin (engenheiro de software na LangChain), LangChain, Anthropic (originadora dos padrões de dynamic workflows)

## Claims acionáveis
- Anexe o code interpreter middleware ao seu Deep Agent para habilitar subagentes dinâmicos; em Decode o recurso já vem ativado por padrão.
- Use a palavra-chave 'workflow' na requisição para sinalizar explicitamente que o agente deve escrever código de orquestração em vez de decidir sozinho.
- Passe uma response schema gerada dinamicamente na task global para que o resultado volte tipado, permitindo que o agente faça loop ou branch sobre ele em código.
- Mova orquestração repetitiva (centenas de chamadas) para loops em código para eliminar omissões, encerramentos precoces e trajetórias ruins do agente.
- Faça o steering de cada padrão pelo fraseamento: 'every/all + um resumo único' (Fan Out and Synthesize), 'double check / só os confirmados' (Adversarial Verification), 'várias abordagens e escolha a melhor' (Generate and Filter), 'head-to-head / torneio' (Tournament), 'não pare até não haver nada novo' (Loop Until Done), 'figure out what each one is' (Classify and Act).
- Variáveis criadas em uma chamada eval persistem para as chamadas seguintes, permitindo workflows multi-etapa iterativos sem poluir o contexto principal.
- No padrão Adversarial Verification, rode uma passada ampla de candidatos e uma segunda passada de verificadores independentes, reportando apenas o que sobreviver à verificação.
- A descrição passada a cada subagente funciona como system prompt customizado e pode ser variada por item (ex.: por tipo de arquivo).
- Prefira escrever artefatos em arquivos (sem response schema) quando o produto é o arquivo em si; use schemas tipadas quando o resultado precisa alimentar código posterior.
- Subagentes mantêm o contexto do agente principal limpo: apenas o resultado final retorna ao contexto, mesmo com subagentes fazendo dezenas de tool calls.
- O agente pode misturar chamadas eval (fan-out programático) com chamadas regulares da task tool, preservando flexibilidade na decomposição.
- Use traces do LangSmith para inspecionar cada fase de fan-out, as chamadas eval, os tipos de subagente acionados e os schemas gerados.

> **Deep dive:** `high` — Alta densidade de insight acionável e arquitetural — API do middleware, task global tipada, estado persistente entre evals e seis padrões de orquestração com heurísticas de steering — diretamente relevante a harness, agent-fleets, context-engineering e verificação.
