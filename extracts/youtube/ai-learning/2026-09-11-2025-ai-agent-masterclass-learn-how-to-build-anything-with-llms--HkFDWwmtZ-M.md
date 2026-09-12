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
