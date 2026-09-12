---
title: "2025 AI AGENT Masterclass - Learn How To Build ANYTHING With LLMs"
type: "extract"
source: "youtube"
video_id: "HkFDWwmtZ-M"
url: "https://www.youtube.com/watch?v=HkFDWwmtZ-M"
channel: "All About AI"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-2025-ai-agent-masterclass-learn-how-to-build-anything-with-llms--HkFDWwmtZ-M.txt]]"
tags: ["agents", "agent-loop", "agent-tooling", "agentic-coding", "multi-agent", "model-selection", "evals", "classification", "arquitetura", "process", "verification", "gate-design"]
thesis: "O transcript é um tutorial que implementa em código, com OpenAI API e Cursor, os padrões de workflows agentic publicados pela Anthropic (LLM aumentada, prompt chaining, roteamento, paralelização, orchestrator-workers e evaluator-optimizer), defendendo que se deve começar com soluções simples e adotar sistemas multi-step agentic apenas quando elas falharem."
concepts: ["Distinção entre workflows (LLMs e tools orquestrados por caminhos de código predefinidos) e agentes (LLM direciona dinamicamente seu próprio processo e uso de tools)", "LLM aumentada (retrieval, tools e memory como blocos fundamentais)", "Prompt chaining (decomposição em passos sequenciais, cada chamada processa a saída da anterior, com gates de qualidade)", "Roteamento (classificar input e direcionar para modelo ou prompt especializado)", "Paralelização (sectioning em subtarefas independentes e voting com múltiplas execuções)", "Orchestrator-workers (LLM central decompõe a tarefa, delega a workers e sintetiza os resultados)", "Evaluator-optimizer (loop de geração, avaliação e refinamento, akin a LLM-as-judge)", "Tool/function calling com schema de função", "Trade-off entre latência, custo e acurácia na escolha de padrões e modelos", "System prompts para impor requisitos e formato de saída", "Autonomia de agentes, erros compostos e necessidade de sandbox e guardrails"]
tools: ["OpenAI API (GPT-4o, GPT-4o mini, o1 mini)", "Cursor (com Claude como agente de código)", "OpenWeather API (tool de exemplo)", "Model Context Protocol (MCP)"]
people: ["Anthropic", "OpenAI"]
claims: ["Comece com prompts simples, otimize-os e só adicione sistemas agentic multi-step quando a solução simples falhar — sucesso não exige o sistema mais sofisticado, mas o certo para a necessidade", "Roteamento reduz custo ao enviar queries conversacionais simples para modelos menores/mais baratos e raciocínio complexo para modelos maiores, ao custo de uma chamada extra de API e latência adicional", "Prompt chaining troca latência por acurácia ao tornar cada chamada LLM uma tarefa mais simples, com gates entre passos", "Paralelizar chamadas LLM (ex.: via threads/async) economiza tempo em relação à execução serial e permite agregar múltiplas perspectivas num agente sintetizador", "Evaluator-optimizer só é eficaz quando existem critérios de avaliação claros (ex.: qualidade de código), sendo inadequado para tarefas sem critérios objetivos", "Avaliadores LLM tendem a ser lenientes e aprovar rapidamente, exigindo cuidado com system prompt e escolha do modelo avaliador", "Confiar em saída JSON do avaliador gera falhas frequentes de formatação; prefira formatos de resposta mais robustos", "System messages (ex.: 'retorne a resposta como um poema') são o mecanismo para impor requisitos específicos de saída", "Agentes autônomos têm custo alto e risco de erros compostos; teste extensivamente em ambientes sandbox com guardrails apropriados antes de produção"]
deep_dive: "low"
deep_dive_reason: "Tutorial introdutório que reimplementa em código padrões já publicados pela Anthropic com exemplos-brinquedo (clima, Fibonacci), sem novidade arquitetural nem profundidade em harness, evals ou governança."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-12-factor-agents-patterns-of-reliable-llm-applications-dex-horthy-humanlayer--8kMaTybvDUw|12-Factor Agents: Patterns of reliable LLM applications — Dex Horthy, HumanLayer]]", "[[extracts/youtube/ai-learning/2026-09-11-n8n-full-tutorial-building-ai-agents-in-2025-for-beginners--ZbIVOy_GPyQ|N8N Full Tutorial: Building AI Agents in 2025 for Beginners!]]", "[[extracts/youtube/ai-learning/2026-09-11-how-i-automate-my-own-job-at-hugging-face-using-agents-niels-rogge-hugging-face--FLUoowDJg4I|How I automate my own job at Hugging Face using agents — Niels Rogge, Hugging Face]]", "[[extracts/youtube/ai-learning/2026-09-11-from-zero-to-your-first-ai-agent-in-25-minutes-no-coding--EH5jx5qPabU|From Zero to Your First AI Agent in 25 Minutes (No Coding)]]", "[[extracts/youtube/ai-learning/2026-09-11-full-walkthrough-workflow-for-ai-coding-matt-pocock---QFHIoCo-Ko|Full Walkthrough: Workflow for AI Coding — Matt Pocock]]", "[[extracts/youtube/ai-learning/2026-09-11-research-agent-3-0-build-a-group-of-ai-researchers-here-is-how--AVInhYBUnKs|\"Research agent 3.0 - Build a group of AI researchers\" - Here is how]]", "[[extracts/youtube/ai-learning/2026-09-11-how-to-build-super-effective-ai-agents-full-tutorial-cursor-openai--MSO4qCiwTjQ|How to Build Super Effective AI AGENTS - FULL TUTORIAL | Cursor - OpenAI]]", "[[extracts/youtube/ai-learning/2026-09-11-how-to-build-deep-research-google-docs-ai-agents-full-tutorial--yQ4F553zhQw|How to Build Deep Research Google Docs AI AGENTS - Full Tutorial]]", "[[extracts/youtube/ai-learning/2026-09-11-we-ve-been-building-ai-agents-wrong-until-now--pC17ge_2n0Q|We've Been Building AI Agents WRONG Until Now]]", "[[extracts/youtube/ai-learning/2026-09-11-pydanticai-the-new-agent-builder-on-the-block--UnH7S5044GA|PydanticAI - The NEW Agent Builder on the Block]]", "[[extracts/youtube/ai-learning/2026-09-11-how-to-use-rlms-in-deep-agents--5_LLMZfKI6w|How to use RLMs in Deep Agents]]", "[[extracts/youtube/ai-learning/2026-09-11-how-to-create-agent-swarms-with-the-new-openai-assistants-api--8fMnAZI1bdA|How to Create Agent Swarms With the NEW OpenAI Assistants API]]", "[[extracts/youtube/ai-learning/2026-09-11-this-ai-agent-can-do-basically-everything-agent-zero--kTs3kDlKc8w|This AI Agent can do basically everything - Agent Zero]]", "[[extracts/youtube/ai-learning/2026-09-11-power-each-ai-agent-with-a-different-local-llm-autogen-ollama-tutorial--y7wMTwJN7rA|Power Each AI Agent With A Different LOCAL LLM (AutoGen + Ollama Tutorial)]]", "[[extracts/youtube/ai-learning/2026-09-11-automate-complex-workflows-with-openai-o3--ydJNqND6N_Y|Automate complex workflows with OpenAI o3]]", "[[extracts/youtube/ai-learning/2026-09-11-i-want-llama3-to-perform-10x-with-my-private-knowledge-local-agentic-rag-w-llama--u5Vcrwpzoz8|\"I want Llama3 to perform 10x with my private knowledge\" - Local Agentic RAG w/ llama3]]", "[[extracts/youtube/ai-learning/2026-09-11-intro-to-fine-tuning-large-language-models--H-oCV5brtU4|Intro to Fine-Tuning Large Language Models]]", "[[extracts/youtube/ai-learning/2026-09-11-why-agentic-systems-need-ontologies-frank-coyle-uc-berkeley--Sir59K8ZDPU|Why Agentic Systems Need Ontologies — Frank Coyle, UC Berkeley]]"]
---

# 2025 AI AGENT Masterclass - Learn How To Build ANYTHING With LLMs

## Tese
O transcript é um tutorial que implementa em código, com OpenAI API e Cursor, os padrões de workflows agentic publicados pela Anthropic (LLM aumentada, prompt chaining, roteamento, paralelização, orchestrator-workers e evaluator-optimizer), defendendo que se deve começar com soluções simples e adotar sistemas multi-step agentic apenas quando elas falharem.

## Conceitos-chave
- Distinção entre workflows (LLMs e tools orquestrados por caminhos de código predefinidos) e agentes (LLM direciona dinamicamente seu próprio processo e uso de tools)
- LLM aumentada (retrieval, tools e memory como blocos fundamentais)
- Prompt chaining (decomposição em passos sequenciais, cada chamada processa a saída da anterior, com gates de qualidade)
- Roteamento (classificar input e direcionar para modelo ou prompt especializado)
- Paralelização (sectioning em subtarefas independentes e voting com múltiplas execuções)
- Orchestrator-workers (LLM central decompõe a tarefa, delega a workers e sintetiza os resultados)
- Evaluator-optimizer (loop de geração, avaliação e refinamento, akin a LLM-as-judge)
- Tool/function calling com schema de função
- Trade-off entre latência, custo e acurácia na escolha de padrões e modelos
- System prompts para impor requisitos e formato de saída
- Autonomia de agentes, erros compostos e necessidade de sandbox e guardrails

## Ferramentas & pessoas
**Ferramentas:** OpenAI API (GPT-4o, GPT-4o mini, o1 mini), Cursor (com Claude como agente de código), OpenWeather API (tool de exemplo), Model Context Protocol (MCP)

**Pessoas/orgs:** Anthropic, OpenAI

## Claims acionáveis
- Comece com prompts simples, otimize-os e só adicione sistemas agentic multi-step quando a solução simples falhar — sucesso não exige o sistema mais sofisticado, mas o certo para a necessidade
- Roteamento reduz custo ao enviar queries conversacionais simples para modelos menores/mais baratos e raciocínio complexo para modelos maiores, ao custo de uma chamada extra de API e latência adicional
- Prompt chaining troca latência por acurácia ao tornar cada chamada LLM uma tarefa mais simples, com gates entre passos
- Paralelizar chamadas LLM (ex.: via threads/async) economiza tempo em relação à execução serial e permite agregar múltiplas perspectivas num agente sintetizador
- Evaluator-optimizer só é eficaz quando existem critérios de avaliação claros (ex.: qualidade de código), sendo inadequado para tarefas sem critérios objetivos
- Avaliadores LLM tendem a ser lenientes e aprovar rapidamente, exigindo cuidado com system prompt e escolha do modelo avaliador
- Confiar em saída JSON do avaliador gera falhas frequentes de formatação; prefira formatos de resposta mais robustos
- System messages (ex.: 'retorne a resposta como um poema') são o mecanismo para impor requisitos específicos de saída
- Agentes autônomos têm custo alto e risco de erros compostos; teste extensivamente em ambientes sandbox com guardrails apropriados antes de produção

> **Deep dive:** `low` — Tutorial introdutório que reimplementa em código padrões já publicados pela Anthropic com exemplos-brinquedo (clima, Fibonacci), sem novidade arquitetural nem profundidade em harness, evals ou governança.
