---
title: "\"Next Level Prompts?\" - 10 mins into advanced prompting"
type: "extract"
source: "youtube"
video_id: "69bH4IHZivs"
url: "https://www.youtube.com/watch?v=69bH4IHZivs"
channel: "AI Jason"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-next-level-prompts-10-mins-into-advanced-prompting--69bH4IHZivs.txt]]"
tags: ["frameworks", "evals", "classification", "stack-tooling", "process", "agent-tooling"]
thesis: "Frameworks de engenharia de prompt como o Guidance permitem programar prompts com estrutura de saída, lógica condicional, respostas restritas e funções customizadas para obter resultados consistentes em escala, complementados por bibliotecas comunitárias (FlowGPT) e ferramentas de avaliação automática de prompts (GPT prompt engineer / Prompts Royale)."
concepts: ["engenharia de prompt", "controle estrutural de saída", "variáveis de template em prompts", "geração restrita a respostas predefinidas", "lógica condicional (if) dentro de prompts", "blocos ocultos (hidden=true) para lógica interna", "chamada de funções customizadas dentro do prompt", "few-shot prompting", "LLM como avaliador (evaluation machine)", "seleção de prompts por avaliação em múltiplas rodadas", "descoberta de prompts em bibliotecas comunitárias", "conversão de linguagem natural para JSON e URLs dinâmicas"]
tools: ["Guidance", "Visual Studio Code", "Jupyter Notebook", "OpenAI (text-davinci, GPT-3.5, GPT-4)", "Llama", "QuickChart", "Pollinations", "Streamlit", "FlowGPT", "GPT prompt engineer", "Prompts Royale", "GitHub"]
people: ["Microsoft", "OpenAI", "FlowGPT (comunidade)", "Steve Jobs (citado em exemplo)"]
claims: ["Use o Guidance para programar prompts com variáveis em chaves duplas e o termo especial gen para controlar exatamente a estrutura da saída do LLM", "Restrinja a saída do modelo a uma lista de respostas predefinidas para manter o raciocínio do LLM mas eliminar criatividade indesejada (ex.: respostas de e-mail e atendimento ao cliente)", "Implemente condições if dentro do prompt para disparar fluxos distintos, como resposta de contensão quando um cliente é classificado como rude ou agendamento imediato quando a prioridade é alta", "Envolva lógica interna em blocos com atributo hidden=true para omiti-la da saída final visível", "Combine classificação de prioridade + bloco condicional para inserir mensagens fixas (ex.: link de calendário) que não devem ser alteradas pelo modelo", "Acople funções customizadas ao prompt para transformar JSON gerado pelo modelo em URLs de API, gerando gráficos em tempo real via QuickChart ou imagens via Pollinations", "Use few-shot examples dentro do prompt para ensinar o modelo a converter linguagem natural em estruturas JSON específicas", "Consulte o FlowGPT como ponto de partida para descobrir prompts votados pela comunidade antes de criar os seus", "Não confie na geração autônoma de prompts por GPT-4: os prompts gerados são inferiores aos escritos manualmente, mas o framework de avaliação (20-30 rodadas de teste comparativo) é valioso", "Use o Prompts Royale para colar manualmente 2-3 variações de prompt que você escreveu e obter um score comparativo de desempenho em escala", "Considere o uso do Guidance apesar de bugs e documentação limitada, pois os blocos básicos já permitem prompts avançados; e espere ainda um processo iterativo de fine-tuning do prompt"]
deep_dive: "medium"
deep_dive_reason: "O vídeo entrega técnicas acionáveis de programação de prompts e avaliação comparativa de prompts, mas é um tutorial de nível introdutório-intermediário sem profundidade arquitetural ou novidade relevante em harness, context-engineering ou governança."
---

# "Next Level Prompts?" - 10 mins into advanced prompting

## Tese
Frameworks de engenharia de prompt como o Guidance permitem programar prompts com estrutura de saída, lógica condicional, respostas restritas e funções customizadas para obter resultados consistentes em escala, complementados por bibliotecas comunitárias (FlowGPT) e ferramentas de avaliação automática de prompts (GPT prompt engineer / Prompts Royale).

## Conceitos-chave
- engenharia de prompt
- controle estrutural de saída
- variáveis de template em prompts
- geração restrita a respostas predefinidas
- lógica condicional (if) dentro de prompts
- blocos ocultos (hidden=true) para lógica interna
- chamada de funções customizadas dentro do prompt
- few-shot prompting
- LLM como avaliador (evaluation machine)
- seleção de prompts por avaliação em múltiplas rodadas
- descoberta de prompts em bibliotecas comunitárias
- conversão de linguagem natural para JSON e URLs dinâmicas

## Ferramentas & pessoas
**Ferramentas:** Guidance, Visual Studio Code, Jupyter Notebook, OpenAI (text-davinci, GPT-3.5, GPT-4), Llama, QuickChart, Pollinations, Streamlit, FlowGPT, GPT prompt engineer, Prompts Royale, GitHub

**Pessoas/orgs:** Microsoft, OpenAI, FlowGPT (comunidade), Steve Jobs (citado em exemplo)

## Claims acionáveis
- Use o Guidance para programar prompts com variáveis em chaves duplas e o termo especial gen para controlar exatamente a estrutura da saída do LLM
- Restrinja a saída do modelo a uma lista de respostas predefinidas para manter o raciocínio do LLM mas eliminar criatividade indesejada (ex.: respostas de e-mail e atendimento ao cliente)
- Implemente condições if dentro do prompt para disparar fluxos distintos, como resposta de contensão quando um cliente é classificado como rude ou agendamento imediato quando a prioridade é alta
- Envolva lógica interna em blocos com atributo hidden=true para omiti-la da saída final visível
- Combine classificação de prioridade + bloco condicional para inserir mensagens fixas (ex.: link de calendário) que não devem ser alteradas pelo modelo
- Acople funções customizadas ao prompt para transformar JSON gerado pelo modelo em URLs de API, gerando gráficos em tempo real via QuickChart ou imagens via Pollinations
- Use few-shot examples dentro do prompt para ensinar o modelo a converter linguagem natural em estruturas JSON específicas
- Consulte o FlowGPT como ponto de partida para descobrir prompts votados pela comunidade antes de criar os seus
- Não confie na geração autônoma de prompts por GPT-4: os prompts gerados são inferiores aos escritos manualmente, mas o framework de avaliação (20-30 rodadas de teste comparativo) é valioso
- Use o Prompts Royale para colar manualmente 2-3 variações de prompt que você escreveu e obter um score comparativo de desempenho em escala
- Considere o uso do Guidance apesar de bugs e documentação limitada, pois os blocos básicos já permitem prompts avançados; e espere ainda um processo iterativo de fine-tuning do prompt

> **Deep dive:** `medium` — O vídeo entrega técnicas acionáveis de programação de prompts e avaliação comparativa de prompts, mas é um tutorial de nível introdutório-intermediário sem profundidade arquitetural ou novidade relevante em harness, context-engineering ou governança.
