---
title: "State-Of-The-Art Prompting For AI Agents"
type: "extract"
source: "youtube"
video_id: "DL82mGde6wo"
url: "https://www.youtube.com/watch?v=DL82mGde6wo"
channel: "Y Combinator"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-state-of-the-art-prompting-for-ai-agents--DL82mGde6wo.txt]]"
tags: ["context-engineering", "evals", "agents", "agent-tooling", "model-selection", "error-handling", "escalation", "verification", "observability", "tracing", "testes-qa", "decision-discipline", "investimentos", "instituicoes", "process", "arquitetura", "production", "classification"]
thesis: "A engenharia de prompts em agentes verticais de IA amadureceu para uma disciplina arquitetural — com camadas de prompt (sistema/desenvolvedor/usuário), metaprompting, escape hatches e evals como o verdadeiro ativo de IP — executada por fundadores técnicos que atuam como forward deployed engineers junto aos clientes de nicho."
concepts: ["Metaprompting (prompts que geram versões melhores de si mesmos em loop)", "Prompt folding (classificador gera prompt especializado por consulta)", "Arquitetura em camadas system/developer/user prompt", "Escape hatch: instruir o LLM a parar e perguntar quando falta informação em vez de alucinar", "Parâmetro de resposta 'debug info' onde o modelo reclama de instruções confusas ao desenvolvedor", "Evals como crown jewels (mais valiosos que os prompts)", "Worked examples / few-shot para tarefas complexas demais para especificar em prosa", "Tags XML em prompts por causa do pós-treino com RLHF", "Thinking traces como ferramenta de debug de prompts (Gemini 2.5 Pro via API)", "Gemini de contexto longo usado como REPL para observar raciocínio em tempo real", "Padrão de destilação: meta-prompt com modelo grande, deploy em modelo rápido para baixa latência (voice AI)", "Personalidades distintas de modelos ao aplicar rubrics (o3 rígido vs Gemini 2.5 Pro flexível)", "Modelos como Claude (mais steerável) vs Llama 4 (exige mais steering, menos RLHF)", "Fork/merge de prompts entre clientes para evitar virar consultoria", "Rubrics numéricas ancoradas (escala 0-100) para scoring com LLMs", "Forward Deployed Engineer (modelo Palantir) aplicado a vendas de vertical AI", "Kaizen aplicado a prompts: quem opera o processo é quem melhor o melhora", "Analogia com test-driven development: exemplos funcionam como testes para LLMs"]
tools: ["Parahelp", "Gemini 2.5 Pro", "OpenAI o3", "Claude", "Llama 4", "Groq", "Palantir Foundry", "gemini.google.com", "ChatGPT", "Google Docs"]
people: ["Y Combinator", "Jared", "Diana", "Harj", "Gary (Gary Tan)", "Eric Bacon (head de dados da YC)", "Ryan Peterson (Flexport)", "Peter Thiel", "Alex Karp", "Stephen Cohen", "Joe Lonsdale", "Nathan Gettings", "Palantir", "Perplexity", "Replit", "Bolt", "Ducky", "Tropier", "Jasberry", "Giger ML", "Zepto", "Happy Robot", "Flexport", "FBI", "Benchmark", "Thrive", "Salesforce", "Oracle", "Booz Allen"]
claims: ["Estruture prompts como documentos longos com definição de papel, tarefa explícita, plano passo a passo, restrições, formato de saída e worked examples, usando markdown e tags XML (modelos pós-treinados com RLHF seguem XML melhor)", "Separe o prompt em camadas: system prompt (API de alto nível da empresa), developer prompt (contexto específico do cliente) e user prompt (input do usuário final)", "Dê ao LLM um escape hatch explícito: se faltar informação para decidir, não invente — pare e pergunte ao desenvolvedor", "Inclua um campo 'debug info' no formato de resposta onde o modelo reporta instruções confusas ou subespecificadas; os outputs de produção viram um to-do list de correções para o time de engenharia", "Use metaprompting em loop: alimente o prompt atual mais os casos de falha no LLM cru para gerar versões melhoradas em vez de reescrever manualmente", "Para tarefas difíceis de especificar em prosa (ex.: detectar bug N+1 em código), injete exemplos difíceis reais no meta prompt em vez de tentar descrever regras", "Meta-proptimize com modelos grandes (o3/Claude) e faça deploy em modelos pequenos/rápidos (ex.: Groq) quando latência é crítica, como em voice AI", "Trate evals como o ativo mais valioso da empresa: sem evals não se sabe por que o prompt foi escrito assim nem como melhorá-lo com segurança", "Capture evals por etnografia: sente-se ao lado do especialista de domínio (ex.: gerente regional de vendas de tratores) e codifique seus fluxos de decisão — isso é o moat de vertical AI", "Use as thinking traces do Gemini 2.5 Pro (agora disponíveis via API) como REPL: rode o prompt exemplo por exemplo observando o raciocínio em tempo real para identificar falhas", "Escolha o modelo conforme a tarefa: o3 segue rubrics de forma rígida e literal, enquanto Gemini 2.5 Pro raciocina sobre exceções — diferentes 'personalidades' se adequam a diferentes necessidades de julgamento", "Ao pedir scores numéricos, forneça rubrics ancoradas (ex.: 0-100 com descrições claras de cada faixa)", "Fundadores técnicos devem atuar como forward deployed engineers: descoberta in loco, ajuste do prompt/produto, e demo impressionante na reunião seguinte para fechar deals de 6-7 dígitos", "Acumule notas de falhas observadas em um doc e peça a um modelo grande que sugira edições no prompt para incorporá-las"]
deep_dive: "high"
deep_dive_reason: "Alta densidade de práticas acionáveis e arquiteturais de context-engineering e evals (camadas de prompt, escape hatch, parâmetro debug info, metaprompting/prompt folding, destilação para latência) com casos raros e concretos como o prompt real da Parahelp revelado e a tese de evals como crown jewels, diretamente relevantes a harness, context-engineering e evals."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-ai-prompt-engineering-a-deep-dive--T9aRN5JkmL8|AI prompt engineering: A deep dive]]", "[[extracts/youtube/ai-learning/2026-09-11-the-prompting-playbook--G2B0YWuJUgI|The prompting playbook]]", "[[extracts/youtube/ai-learning/2026-09-11-next-level-prompts-10-mins-into-advanced-prompting--69bH4IHZivs|\"Next Level Prompts?\" - 10 mins into advanced prompting]]", "[[extracts/youtube/ai-learning/2026-09-11-prompting-101-code-w-claude--ysPbXH0LpIE|Prompting 101 | Code w/ Claude]]", "[[extracts/youtube/ai-learning/2026-09-11-google-s-9-hour-ai-prompt-engineering-course-in-20-minutes--p09yRj47kNM|Google's 9 Hour AI Prompt Engineering Course In 20 Minutes]]", "[[extracts/youtube/ai-learning/2026-09-11-5-simple-but-weird-chatgpt-5-tricks-to-get-a-10x-better-response--emV9Wo_UuGQ|5 simple (but weird) ChatGPT-5 tricks to get a 10x better response]]", "[[extracts/youtube/ai-learning/2026-09-11-the-master-prompt-method-unlock-ais-full-potential-part-1--_K_F_icxtrI|The Master Prompt Method: Unlock AI’s Full Potential (Part 1)]]", "[[extracts/youtube/ai-learning/2026-09-11-the-master-prompt-method-build-your-ai-operating-system--yNpbnrlAFzA|The Master Prompt Method: Build Your AI Operating System]]", "[[extracts/youtube/ai-learning/2026-09-11-master-the-perfect-chatgpt-prompt-formula-in-just-8-minutes--jC4v5AS4RIM|Master the Perfect ChatGPT Prompt Formula (in just 8 minutes)!]]", "[[extracts/youtube/ai-learning/2026-09-11-the-best-chatgpt-prompt-i-ve-ever-created-i-spent-2-months-curating-this-prompt--ABCqfaTjNd4|The best ChatGPT Prompt I've ever created - I spent 2 months curating this prompt to write prompts]]"]
---

# State-Of-The-Art Prompting For AI Agents

## Tese
A engenharia de prompts em agentes verticais de IA amadureceu para uma disciplina arquitetural — com camadas de prompt (sistema/desenvolvedor/usuário), metaprompting, escape hatches e evals como o verdadeiro ativo de IP — executada por fundadores técnicos que atuam como forward deployed engineers junto aos clientes de nicho.

## Conceitos-chave
- Metaprompting (prompts que geram versões melhores de si mesmos em loop)
- Prompt folding (classificador gera prompt especializado por consulta)
- Arquitetura em camadas system/developer/user prompt
- Escape hatch: instruir o LLM a parar e perguntar quando falta informação em vez de alucinar
- Parâmetro de resposta 'debug info' onde o modelo reclama de instruções confusas ao desenvolvedor
- Evals como crown jewels (mais valiosos que os prompts)
- Worked examples / few-shot para tarefas complexas demais para especificar em prosa
- Tags XML em prompts por causa do pós-treino com RLHF
- Thinking traces como ferramenta de debug de prompts (Gemini 2.5 Pro via API)
- Gemini de contexto longo usado como REPL para observar raciocínio em tempo real
- Padrão de destilação: meta-prompt com modelo grande, deploy em modelo rápido para baixa latência (voice AI)
- Personalidades distintas de modelos ao aplicar rubrics (o3 rígido vs Gemini 2.5 Pro flexível)
- Modelos como Claude (mais steerável) vs Llama 4 (exige mais steering, menos RLHF)
- Fork/merge de prompts entre clientes para evitar virar consultoria
- Rubrics numéricas ancoradas (escala 0-100) para scoring com LLMs
- Forward Deployed Engineer (modelo Palantir) aplicado a vendas de vertical AI
- Kaizen aplicado a prompts: quem opera o processo é quem melhor o melhora
- Analogia com test-driven development: exemplos funcionam como testes para LLMs

## Ferramentas & pessoas
**Ferramentas:** Parahelp, Gemini 2.5 Pro, OpenAI o3, Claude, Llama 4, Groq, Palantir Foundry, gemini.google.com, ChatGPT, Google Docs

**Pessoas/orgs:** Y Combinator, Jared, Diana, Harj, Gary (Gary Tan), Eric Bacon (head de dados da YC), Ryan Peterson (Flexport), Peter Thiel, Alex Karp, Stephen Cohen, Joe Lonsdale, Nathan Gettings, Palantir, Perplexity, Replit, Bolt, Ducky, Tropier, Jasberry, Giger ML, Zepto, Happy Robot, Flexport, FBI, Benchmark, Thrive, Salesforce, Oracle, Booz Allen

## Claims acionáveis
- Estruture prompts como documentos longos com definição de papel, tarefa explícita, plano passo a passo, restrições, formato de saída e worked examples, usando markdown e tags XML (modelos pós-treinados com RLHF seguem XML melhor)
- Separe o prompt em camadas: system prompt (API de alto nível da empresa), developer prompt (contexto específico do cliente) e user prompt (input do usuário final)
- Dê ao LLM um escape hatch explícito: se faltar informação para decidir, não invente — pare e pergunte ao desenvolvedor
- Inclua um campo 'debug info' no formato de resposta onde o modelo reporta instruções confusas ou subespecificadas; os outputs de produção viram um to-do list de correções para o time de engenharia
- Use metaprompting em loop: alimente o prompt atual mais os casos de falha no LLM cru para gerar versões melhoradas em vez de reescrever manualmente
- Para tarefas difíceis de especificar em prosa (ex.: detectar bug N+1 em código), injete exemplos difíceis reais no meta prompt em vez de tentar descrever regras
- Meta-proptimize com modelos grandes (o3/Claude) e faça deploy em modelos pequenos/rápidos (ex.: Groq) quando latência é crítica, como em voice AI
- Trate evals como o ativo mais valioso da empresa: sem evals não se sabe por que o prompt foi escrito assim nem como melhorá-lo com segurança
- Capture evals por etnografia: sente-se ao lado do especialista de domínio (ex.: gerente regional de vendas de tratores) e codifique seus fluxos de decisão — isso é o moat de vertical AI
- Use as thinking traces do Gemini 2.5 Pro (agora disponíveis via API) como REPL: rode o prompt exemplo por exemplo observando o raciocínio em tempo real para identificar falhas
- Escolha o modelo conforme a tarefa: o3 segue rubrics de forma rígida e literal, enquanto Gemini 2.5 Pro raciocina sobre exceções — diferentes 'personalidades' se adequam a diferentes necessidades de julgamento
- Ao pedir scores numéricos, forneça rubrics ancoradas (ex.: 0-100 com descrições claras de cada faixa)
- Fundadores técnicos devem atuar como forward deployed engineers: descoberta in loco, ajuste do prompt/produto, e demo impressionante na reunião seguinte para fechar deals de 6-7 dígitos
- Acumule notas de falhas observadas em um doc e peça a um modelo grande que sugira edições no prompt para incorporá-las

> **Deep dive:** `high` — Alta densidade de práticas acionáveis e arquiteturais de context-engineering e evals (camadas de prompt, escape hatch, parâmetro debug info, metaprompting/prompt folding, destilação para latência) com casos raros e concretos como o prompt real da Parahelp revelado e a tese de evals como crown jewels, diretamente relevantes a harness, context-engineering e evals.
