---
title: "How to Create Agent Swarms With the NEW OpenAI Assistants API"
type: "extract"
source: "youtube"
video_id: "8fMnAZI1bdA"
url: "https://www.youtube.com/watch?v=8fMnAZI1bdA"
channel: "Arseny Shatokhin"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-how-to-create-agent-swarms-with-the-new-openai-assistants-api--8fMnAZI1bdA.txt]]"
tags: ["agents", "multi-agent", "agent-loop", "agent-tooling", "arquitetura", "frameworks", "token-budgeting", "production", "state", "verification", "error-handling", "stack-tooling"]
thesis: "É possível recriar um sistema multiagente estilo AutoGen em produção com apenas 5-6 funções sobre a nova Assistants API da OpenAI, ganhando controle, steerability e eficiência de tokens em relação ao framework original."
concepts: ["padrão user proxy agent", "arquitetura de load balancer inspirada em Kubernetes", "recursão em sistemas de agentes", "chain of thought como parâmetro de função (por chamada, não global)", "Single Responsibility Principle aplicado a agentes", "modelo threads/messages/runs da Assistants API", "runs assíncronos com polling até 'completed' ou 'requires_action'", "definição de funções como schemas Pydantic", "threads separados por agente (agents_and_threads)", "steerability e prevenção de loops infinitos", "comunicação entre agentes via ferramenta sendMessage", "guardrails e lógica customizada por caso de uso"]
tools: ["OpenAI Assistants API (beta)", "Instructor", "Pydantic", "AutoGen", "yFinance", "subprocess (Python)", "Code Interpreter", "web browsing (ferramenta nativa)"]
people: ["Jason Liu", "OpenAI", "Meta", "Tesla"]
claims: ["Recriar o AutoGen exige apenas 5-6 funções sobre a Assistants API, resultando em sistema mais controlável, customizável e implantável em produção.", "A biblioteca Instructor permite definir funções OpenAI como schemas Pydantic com validação de entrada e saída, mais conveniente que JSON cru.", "Runs da Assistants API são assíncronos: é preciso fazer polling até o status 'completed' ou 'requires_action', e neste último devolver a saída da função antes de reexecutar o run.", "Adicionar um parâmetro 'chain of thought' à definição da função força o modelo a planejar passo a passo antes de executá-la, aumentando a precisão sem um prompt global de CoT, economizando tokens e latência em produção.", "Modelar o user proxy como load balancer que distribui requisições a agentes especializados e conversa com eles até a tarefa ser concluída melhora a steerability do sistema.", "Armazenar um thread separado por agente em um objeto global (agents_and_threads) mantém conversas isoladas entre o proxy e cada agente.", "Restringir a comunicação apenas ao par proxy-agente (sem conversa direta entre agentes executores) previne loops infinitos e aumenta o controle; pode ser estendido adicionando mais threads e liberando o sendMessage para outros agentes.", "Para adicionar um novo agente: defina suas tools como schemas Pydantic, registre-o em agents_and_threads, adicione o nome ao literal 'recipient' do sendMessage e descreva seu papel na descrição da propriedade.", "O sistema reproduziu o exemplo clássico do AutoGen (gráfico YTD de Meta e Tesla) desperdiçando menos tokens.", "O Code Interpreter nativo não executa arquivos locais e tem limitações; execução local exige subprocess próprio.", "Aplicar o Single Responsibility Principle (cada agente com uma única responsabilidade) facilita adicionar e substituir componentes quando há erros.", "Instruir o user proxy a manter comunicação contínua com os outros agentes até a conclusão da tarefa tem grande impacto no comportamento global do sistema e vale experimentação."]
deep_dive: "medium"
deep_dive_reason: "Tutorial prático com insights arquiteturais acionáveis (padrão load balancer, CoT por chamada, isolamento de threads por agente), mas sem profundidade em evals, harness, governança ou ontologia, e com trechos promocionais."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-research-agent-3-0-build-a-group-of-ai-researchers-here-is-how--AVInhYBUnKs|\"Research agent 3.0 - Build a group of AI researchers\" - Here is how]]", "[[extracts/youtube/ai-learning/2026-09-11-could-a-swarm-of-autonomous-ai-agents-be-the-ultimate-business-asset-stage-1--UL55C80TEb8|Could a Swarm of Autonomous AI Agents be the Ultimate Business Asset? - Stage 1]]", "[[extracts/youtube/ai-learning/2026-09-11-from-zero-to-your-first-ai-agent-in-25-minutes-no-coding--EH5jx5qPabU|From Zero to Your First AI Agent in 25 Minutes (No Coding)]]", "[[extracts/youtube/ai-learning/2026-09-11-how-google-deepmind-runs-agents-at-scale-kp-sawhney-ian-ballantyne-google-deepmi--7gujZrJ9L5I|How Google DeepMind Runs Agents at Scale — KP Sawhney & Ian Ballantyne, Google DeepMind]]", "[[extracts/youtube/ai-learning/2026-09-11-2025-ai-agent-masterclass-learn-how-to-build-anything-with-llms--HkFDWwmtZ-M|2025 AI AGENT Masterclass - Learn How To Build ANYTHING With LLMs]]", "[[extracts/youtube/ai-learning/2026-09-11-power-each-ai-agent-with-a-different-local-llm-autogen-ollama-tutorial--y7wMTwJN7rA|Power Each AI Agent With A Different LOCAL LLM (AutoGen + Ollama Tutorial)]]"]
theme: "Orquestração Multiagente em Escala"
---

# How to Create Agent Swarms With the NEW OpenAI Assistants API

## Tese
É possível recriar um sistema multiagente estilo AutoGen em produção com apenas 5-6 funções sobre a nova Assistants API da OpenAI, ganhando controle, steerability e eficiência de tokens em relação ao framework original.

## Conceitos-chave
- padrão user proxy agent
- arquitetura de load balancer inspirada em Kubernetes
- recursão em sistemas de agentes
- chain of thought como parâmetro de função (por chamada, não global)
- Single Responsibility Principle aplicado a agentes
- modelo threads/messages/runs da Assistants API
- runs assíncronos com polling até 'completed' ou 'requires_action'
- definição de funções como schemas Pydantic
- threads separados por agente (agents_and_threads)
- steerability e prevenção de loops infinitos
- comunicação entre agentes via ferramenta sendMessage
- guardrails e lógica customizada por caso de uso

## Ferramentas & pessoas
**Ferramentas:** OpenAI Assistants API (beta), Instructor, Pydantic, AutoGen, yFinance, subprocess (Python), Code Interpreter, web browsing (ferramenta nativa)

**Pessoas/orgs:** Jason Liu, OpenAI, Meta, Tesla

## Claims acionáveis
- Recriar o AutoGen exige apenas 5-6 funções sobre a Assistants API, resultando em sistema mais controlável, customizável e implantável em produção.
- A biblioteca Instructor permite definir funções OpenAI como schemas Pydantic com validação de entrada e saída, mais conveniente que JSON cru.
- Runs da Assistants API são assíncronos: é preciso fazer polling até o status 'completed' ou 'requires_action', e neste último devolver a saída da função antes de reexecutar o run.
- Adicionar um parâmetro 'chain of thought' à definição da função força o modelo a planejar passo a passo antes de executá-la, aumentando a precisão sem um prompt global de CoT, economizando tokens e latência em produção.
- Modelar o user proxy como load balancer que distribui requisições a agentes especializados e conversa com eles até a tarefa ser concluída melhora a steerability do sistema.
- Armazenar um thread separado por agente em um objeto global (agents_and_threads) mantém conversas isoladas entre o proxy e cada agente.
- Restringir a comunicação apenas ao par proxy-agente (sem conversa direta entre agentes executores) previne loops infinitos e aumenta o controle; pode ser estendido adicionando mais threads e liberando o sendMessage para outros agentes.
- Para adicionar um novo agente: defina suas tools como schemas Pydantic, registre-o em agents_and_threads, adicione o nome ao literal 'recipient' do sendMessage e descreva seu papel na descrição da propriedade.
- O sistema reproduziu o exemplo clássico do AutoGen (gráfico YTD de Meta e Tesla) desperdiçando menos tokens.
- O Code Interpreter nativo não executa arquivos locais e tem limitações; execução local exige subprocess próprio.
- Aplicar o Single Responsibility Principle (cada agente com uma única responsabilidade) facilita adicionar e substituir componentes quando há erros.
- Instruir o user proxy a manter comunicação contínua com os outros agentes até a conclusão da tarefa tem grande impacto no comportamento global do sistema e vale experimentação.

> **Deep dive:** `medium` — Tutorial prático com insights arquiteturais acionáveis (padrão load balancer, CoT por chamada, isolamento de threads por agente), mas sem profundidade em evals, harness, governança ou ontologia, e com trechos promocionais.
