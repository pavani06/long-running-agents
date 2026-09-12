---
title: "OpenAI DevDay 2024 | Virtual AMA with Sam Altman, moderated by Harry Stebbings, 20VC"
type: "extract"
source: "youtube"
video_id: "Hn27upT2m_o"
url: "https://www.youtube.com/watch?v=Hn27upT2m_o"
channel: "OpenAI"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-openai-devday-2024-virtual-ama-with-sam-altman-moderated-by-harry-stebbings-20vc--Hn27upT2m_o.txt]]"
tags: ["agents", "agent-fleets", "agent-tooling", "model-selection", "investimentos", "roadmap", "decision-discipline", "knowledge-management", "memory-architecture", "stack-tooling", "analise"]
thesis: "Sam Altman defende que modelos de raciocínio (série O) são o vetor estratégico central da OpenAI e que startups devem construir produtos que se beneficiam da melhoria contínua dos modelos, em vez de remendar limitações atuais que futuras gerações eliminarão."
concepts: ["modelos de raciocínio (série O) como alavanca estratégica", "definição de agente: tarefa de longa duração com supervisão mínima", "agente como colega sênior que executa tarefas de dias/semanas", "paralelismo massivo de agentes (exemplo das 300 ligações a restaurantes)", "transição de falar sobre 'modelos' para falar sobre 'sistemas'", "pricing por compute (GPUs dedicadas) vs. pricing por assento", "modelos como ativos em depreciação cuja receita justifica o investimento", "scaling laws e trajetória contínua de melhoria de capacidade", "crítica a analogias históricas (internet, eletricidade); analogia do transistor", "decisões 51/49 e rede de 15-20 especialistas para consulta", "barreira extrema de talento ao contratar (jovens + experientes)", "dial controlável pelo usuário entre latência e acurácia", "IA pessoal que conhece toda a sua vida e acessa todos os seus dados", "no-code tools para fundadores não técnicos", "papel do open source como mecanismo de entrega no ecossistema de IA", "complexidade fractal do ecossistema (energia, chips, networking, pesquisa, produto) como principal risco"]
tools: ["OpenAI o1 (série O)", "GPT-4", "GPT-3.5", "ChatGPT", "OpenAI API", "Real-time API", "OpenTable", "Llama", "Cursor", "Slack"]
people: ["Sam Altman", "Harry Stebbings (20VC)", "OpenAI", "Anthropic", "Keith Rabois", "Peter Thiel", "Larry Ellison", "Masayoshi Son (SoftBank)", "Kevin Weil", "Y Combinator", "equipe do Cursor"]
claims: ["Construa produtos que se beneficiam de modelos cada vez melhores; não construa ferramentas que apenas remendam uma limitação atual do modelo", "Raciocínio é a área mais importante de foco e deve destravar contribuições para nova ciência e código muito difícil", "o1 aponta para modelos capazes de grandes tarefas agênticas, mas há enorme infraestrutura e scaffolding a construir", "Desenvolvedores usam múltiplos modelos; o discurso da indústria deve migrar de 'modelos' para 'sistemas'", "O trade-off latência/acurácia deve ser controlável pelo usuário como um dial", "O pricing pode evoluir para cobrança por compute dedicado (1, 10 ou 100 GPUs trabalhando continuamente nos seus problemas) em vez de por assento", "Entrar na corrida de modelos de fundação custará menos que US$ 100 bilhões, contrariando a estimativa de Larry Ellison", "Espere progresso rápido em modelos baseados em imagem sob o novo paradigma de tempo de inferência", "Trilhões de dólares de novo market cap serão criados por produtos/serviços de IA antes impossíveis ou impraticáveis", "A oportunidade negligenciada é uma IA que entende toda a sua vida e tem acesso a todos os seus dados, sem exigir contexto literalmente infinito", "Se começasse hoje aos ~23 anos, Altman construiria um vertical habilitado por IA (ex.: o melhor tutor de IA)", "A trajetória de melhoria dos modelos continuará 'por um longo tempo', apesar de runs de treino falhos e comportamentos não compreendidos", "Para decisões difíceis, mantenha 15-20 pessoas com instintos e contexto confiáveis em domínios específicos em vez de depender de um único conselheiro", "Contrate com barreira extrema de talento em qualquer idade; estratégias exclusivamente jovens ou exclusivamente experientes são equivocadas"]
deep_dive: "medium"
deep_dive_reason: "Entrevista estratégica com insights acionáveis sobre posicionamento de startups, definição de agentes e pricing por compute, mas sem densidade técnica ou arquitetural em harness, evals, context-engineering ou governança, com trechos conversacionais e redundantes."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-stanford-cs153-frontier-systems-scale-agi-and-the-future-of-everything--F_7M4Hc-usM|Stanford CS153 Frontier Systems | Scale, AGI, and the Future of Everything]]", "[[extracts/youtube/ai-learning/2026-09-11-openais-cpo-on-how-ai-changes-must-have-skills-moats-coding-startup-playbooks-mo--scsW6_2SPC4|OpenAI’s CPO on how AI changes must-have skills, moats, coding, startup playbooks, more | Kevin Weil]]", "[[extracts/youtube/ai-learning/2026-09-11-how-to-understand-the-next-wave-of-ai-before-everyone-else-tibo-interview--4qjEgPojjzM|How to Understand the Next Wave of AI Before Everyone Else | Tibo Interview]]", "[[extracts/youtube/ai-learning/2026-09-11-stanford-ms-e435-economics-of-the-ai-supercycle-spring-2026-infrasctructure-ente--sRvrXL83N-c|Stanford MS&E435 Economics of the AI Supercycle | Spring 2026 | Infrasctructure, Enterprise AI, SaaS]]", "[[extracts/youtube/ai-learning/2026-09-11-inside-the-mind-of-anthropic-ceo-dario-amodei-the-circuit-extended-interview--x2VHFgyawPE|Inside the Mind of Anthropic CEO Dario Amodei | The Circuit | Extended Interview]]", "[[extracts/youtube/ai-learning/2026-09-11-the-future-of-ai-agents-with-andrew-ng-interrupt-26--OaRhpwz_TGM|The Future of AI Agents with Andrew Ng | Interrupt 26]]"]
---

# OpenAI DevDay 2024 | Virtual AMA with Sam Altman, moderated by Harry Stebbings, 20VC

## Tese
Sam Altman defende que modelos de raciocínio (série O) são o vetor estratégico central da OpenAI e que startups devem construir produtos que se beneficiam da melhoria contínua dos modelos, em vez de remendar limitações atuais que futuras gerações eliminarão.

## Conceitos-chave
- modelos de raciocínio (série O) como alavanca estratégica
- definição de agente: tarefa de longa duração com supervisão mínima
- agente como colega sênior que executa tarefas de dias/semanas
- paralelismo massivo de agentes (exemplo das 300 ligações a restaurantes)
- transição de falar sobre 'modelos' para falar sobre 'sistemas'
- pricing por compute (GPUs dedicadas) vs. pricing por assento
- modelos como ativos em depreciação cuja receita justifica o investimento
- scaling laws e trajetória contínua de melhoria de capacidade
- crítica a analogias históricas (internet, eletricidade); analogia do transistor
- decisões 51/49 e rede de 15-20 especialistas para consulta
- barreira extrema de talento ao contratar (jovens + experientes)
- dial controlável pelo usuário entre latência e acurácia
- IA pessoal que conhece toda a sua vida e acessa todos os seus dados
- no-code tools para fundadores não técnicos
- papel do open source como mecanismo de entrega no ecossistema de IA
- complexidade fractal do ecossistema (energia, chips, networking, pesquisa, produto) como principal risco

## Ferramentas & pessoas
**Ferramentas:** OpenAI o1 (série O), GPT-4, GPT-3.5, ChatGPT, OpenAI API, Real-time API, OpenTable, Llama, Cursor, Slack

**Pessoas/orgs:** Sam Altman, Harry Stebbings (20VC), OpenAI, Anthropic, Keith Rabois, Peter Thiel, Larry Ellison, Masayoshi Son (SoftBank), Kevin Weil, Y Combinator, equipe do Cursor

## Claims acionáveis
- Construa produtos que se beneficiam de modelos cada vez melhores; não construa ferramentas que apenas remendam uma limitação atual do modelo
- Raciocínio é a área mais importante de foco e deve destravar contribuições para nova ciência e código muito difícil
- o1 aponta para modelos capazes de grandes tarefas agênticas, mas há enorme infraestrutura e scaffolding a construir
- Desenvolvedores usam múltiplos modelos; o discurso da indústria deve migrar de 'modelos' para 'sistemas'
- O trade-off latência/acurácia deve ser controlável pelo usuário como um dial
- O pricing pode evoluir para cobrança por compute dedicado (1, 10 ou 100 GPUs trabalhando continuamente nos seus problemas) em vez de por assento
- Entrar na corrida de modelos de fundação custará menos que US$ 100 bilhões, contrariando a estimativa de Larry Ellison
- Espere progresso rápido em modelos baseados em imagem sob o novo paradigma de tempo de inferência
- Trilhões de dólares de novo market cap serão criados por produtos/serviços de IA antes impossíveis ou impraticáveis
- A oportunidade negligenciada é uma IA que entende toda a sua vida e tem acesso a todos os seus dados, sem exigir contexto literalmente infinito
- Se começasse hoje aos ~23 anos, Altman construiria um vertical habilitado por IA (ex.: o melhor tutor de IA)
- A trajetória de melhoria dos modelos continuará 'por um longo tempo', apesar de runs de treino falhos e comportamentos não compreendidos
- Para decisões difíceis, mantenha 15-20 pessoas com instintos e contexto confiáveis em domínios específicos em vez de depender de um único conselheiro
- Contrate com barreira extrema de talento em qualquer idade; estratégias exclusivamente jovens ou exclusivamente experientes são equivocadas

> **Deep dive:** `medium` — Entrevista estratégica com insights acionáveis sobre posicionamento de startups, definição de agentes e pricing por compute, mas sem densidade técnica ou arquitetural em harness, evals, context-engineering ou governança, com trechos conversacionais e redundantes.
