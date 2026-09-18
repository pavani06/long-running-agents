---
title: "Your agents lack context: Here's how to fix \"You're absolutely right!\" — Brandon Waselnuk, Unblocked"
type: "extract"
source: "youtube"
video_id: "KcVkq5L-0f0"
url: "https://www.youtube.com/watch?v=KcVkq5L-0f0"
channel: "AI Engineer"
extracted: "2026-09-15"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-15-your-agents-lack-context-here-s-how-to-fix-you-re-absolutely-right-brandon-wasel--KcVkq5L-0f0.txt]]"
tags: ["context-engineering", "agent-context", "context-management", "knowledge-management", "token-budgeting", "permissions", "governanca", "index", "repo-as-context", "agent-tooling", "agentic-coding", "code-review", "multi-agent", "data-platform"]
thesis: "O gargalo dos agentes de IA deixou de ser inteligência e passou a ser contexto: sem uma 'context engine' que hidrate o agente com o conhecimento operacional da organização, o custo de contexto ruim se compõe em doom loops, desperdício de tokens e review tax à medida que os agentes escalam."
concepts: ["Context engineering e 'context engine' como camada central para agentes", "O humano como 'context engine' construído ao longo de anos de trabalho em equipe", "Custo composto de contexto ruim (shift-left aplicado a contexto, não só a bugs)", "Curated context trap: repositórios de markdown curados apodrecem e têm problema de distribuição e curadoria", "MCP plateau: descrições mal escritas de ferramentas/servidores impedem chamadas corretas", "Satisfaction of search bias: agente para ao encontrar a primeira informação plausível", "Metáfora da linha d'água: o que o agente não vê (rollout, feature flags, conversas no Slack) causa P0 em produção", "Seis características de um context engine: contexto unificado do sistema, recuperação direcionada, resolução de conflitos, relevância personalizada, otimização de tokens, enforcement de permissões", "RAG sozinho não responde perguntas relacionais; combinar RAG com descoberta de schema e queries determinísticas", "Grafo social de expertise via commits e reviews do GitHub para focar contexto", "Indexação e deduplicação de arquivos de regras do repositório", "Doom loops e review tax como falhas de escala em agentes paralelos e revisores de código por IA"]
tools: ["Unblocked", "Social commit network (open source)", "Repo rules agent (open source)", "Beyond RAG workshop workbook (6 PRs empilhados)", "readiness.getunblocked.com (quiz de nível de adoção)", "GitHub", "Slack", "MCP", "OAuth/SSO", "OpenAI API", "Anthropic"]
people: ["Brandon (Unblocked)", "AJ (LinkedIn)", "Unblocked", "LinkedIn", "Workday", "General Motors", "Anthropic", "OpenAI", "Rasheen"]
claims: ["Código gerado por IA deve parecer escrito por alguém que está há anos na equipe; o que falta é contexto organizacional, não inteligência do modelo", "Contexto incorreto no início da sessão se compõe em custo: wasted search tokens, rework e doom loops de correção", "Repositórios de contexto curados manualmente apodrecem como qualquer documentação e exigem um curador 'onipotente'", "Agentes podem nunca chamar uma ferramenta MCP por causa de descrições mal escritas, e o satisfaction of search bias faz o agente parar na primeira fonte encontrada ignorando fontes mais recentes (ex.: conversa no Slack da noite anterior)", "Acesso à informação não é compreensão: entregar entendimento ao modelo exige técnicas adicionais além de ingestão", "Em teste controlado (mesmo prompt e mesmo modelo), a tarefa consumiu ~21M de tokens sem contexto vs ~10,8M com contexto, economizando ~2 horas de wall-clock e melhorando a qualidade da resposta", "RAG isolado não responde perguntas relacionais como 'quais PRs abertos trabalhei na última semana com autenticação'; é necessário descobrir schema e gerar queries determinísticas", "O context engine deve resolver conflitos entre fontes (diagrama antigo vs Slack recente), respeitar permissões e governance para não vazar informação de projetos secretos, e otimizar respostas por superfície (humano vs machine-to-machine)", "Fornecer um 'mapa' completo de contexto permite ao modelo descobrir o território e revelar unknown unknowns da organização", "Casos de uso vão além de código: customer success resolvendo tickets em tempo real e vendas fechando negócios mais cedo consultando o context engine no campo"]
deep_dive: "medium"
deep_dive_reason: "Apresenta densidade conceitual útil (armadilhas do contexto curado e do MCP, satisfaction of search bias, seis características de um context engine, métricas de economia de tokens e técnica RAG+queries relacionais) com ferramentas open source, mas permanece em nível de visão geral de palestra comercial, sem detalhes de implementação ou arquitetura aprofundados."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-why-more-context-makes-your-agent-dumber-and-what-to-do-about-it-nupur-sharma-qo--EcqMYoIV57A|Why More Context Makes Your Agent Dumber and What to Do About It — Nupur Sharma, Qodo]]", "[[extracts/youtube/ai-learning/2026-09-11-agentic-engineering-working-with-ai-not-just-using-it-brendan-o-leary--BEKc4P87XKo|Agentic Engineering: Working With AI, Not Just Using It — Brendan O'Leary]]", "[[extracts/youtube/ai-learning/2026-09-11-how-we-solved-context-management-in-agents-sally-ann-delucia--esY99nYXxR4|How we solved Context Management in Agents — Sally-Ann Delucia]]", "[[extracts/youtube/ai-learning/2026-09-11-no-vibes-allowed-solving-hard-problems-in-complex-codebases-dex-horthy-humanlaye--rmvDxxNubIg|No Vibes Allowed: Solving Hard Problems in Complex Codebases – Dex Horthy, HumanLayer]]", "[[extracts/youtube/ai-learning/2026-09-11-ex-nasa-dev-reveals-his-agentic-engineering-workflow--xgkjtF89-44|Ex-NASA dev reveals his Agentic Engineering Workflow]]", "[[extracts/youtube/ai-learning/2026-09-11-why-enterprise-ai-adoption-is-slower-than-you-think-aaron-levie-box-harrison-cha--agSRMrhNTf4|Why Enterprise AI Adoption Is Slower Than You Think — Aaron Levie (Box) + Harrison Chase]]", "[[extracts/youtube/ai-learning/2026-09-17-if-we-want-them-to-do-knowledge-work-design-them-as-knowledge-agents-benjamin-cl--O84lhGc1OOI|If we want them to do Knowledge Work, design them as Knowledge Agents — Benjamin Clavié, Mixedbread]]", "[[extracts/youtube/ai-learning/2026-09-11-understanding-is-the-new-bottleneck-geoffrey-litt-notion--WkBPX-oDMnA|Understanding is the new bottleneck — Geoffrey Litt, Notion]]", "[[extracts/youtube/ai-learning/2026-09-11-context-graphs-for-explainable-decision-aware-ai-agents-andreas-kollegger-zaid-z--abvQEhvRI_c|Context Graphs for Explainable, Decision-Aware AI Agents — Andreas Kollegger & Zaid Zaim, Neo4j]]", "[[extracts/youtube/ai-learning/2026-09-11-your-company-brain-will-leak-secrets-how-we-stopped-it-for-big-banks-tanmai-gopa--0uC6u0lJJl4|Your company brain will leak secrets: how we stopped it for big banks — Tanmai Gopal, PromptQL]]", "[[extracts/youtube/ai-learning/2026-09-11-why-your-agents-need-decision-traces-not-just-documents-zach-blumenfeld-neo4j--B9h9ovW5H9U|Why your agents need decision traces, not just documents — Zach Blumenfeld, Neo4j]]"]
theme: "Ciclo de Vida e Evals de Agentes"
---

# Your agents lack context: Here's how to fix "You're absolutely right!" — Brandon Waselnuk, Unblocked

## Tese
O gargalo dos agentes de IA deixou de ser inteligência e passou a ser contexto: sem uma 'context engine' que hidrate o agente com o conhecimento operacional da organização, o custo de contexto ruim se compõe em doom loops, desperdício de tokens e review tax à medida que os agentes escalam.

## Conceitos-chave
- Context engineering e 'context engine' como camada central para agentes
- O humano como 'context engine' construído ao longo de anos de trabalho em equipe
- Custo composto de contexto ruim (shift-left aplicado a contexto, não só a bugs)
- Curated context trap: repositórios de markdown curados apodrecem e têm problema de distribuição e curadoria
- MCP plateau: descrições mal escritas de ferramentas/servidores impedem chamadas corretas
- Satisfaction of search bias: agente para ao encontrar a primeira informação plausível
- Metáfora da linha d'água: o que o agente não vê (rollout, feature flags, conversas no Slack) causa P0 em produção
- Seis características de um context engine: contexto unificado do sistema, recuperação direcionada, resolução de conflitos, relevância personalizada, otimização de tokens, enforcement de permissões
- RAG sozinho não responde perguntas relacionais; combinar RAG com descoberta de schema e queries determinísticas
- Grafo social de expertise via commits e reviews do GitHub para focar contexto
- Indexação e deduplicação de arquivos de regras do repositório
- Doom loops e review tax como falhas de escala em agentes paralelos e revisores de código por IA

## Ferramentas & pessoas
**Ferramentas:** Unblocked, Social commit network (open source), Repo rules agent (open source), Beyond RAG workshop workbook (6 PRs empilhados), readiness.getunblocked.com (quiz de nível de adoção), GitHub, Slack, MCP, OAuth/SSO, OpenAI API, Anthropic

**Pessoas/orgs:** Brandon (Unblocked), AJ (LinkedIn), Unblocked, LinkedIn, Workday, General Motors, Anthropic, OpenAI, Rasheen

## Claims acionáveis
- Código gerado por IA deve parecer escrito por alguém que está há anos na equipe; o que falta é contexto organizacional, não inteligência do modelo
- Contexto incorreto no início da sessão se compõe em custo: wasted search tokens, rework e doom loops de correção
- Repositórios de contexto curados manualmente apodrecem como qualquer documentação e exigem um curador 'onipotente'
- Agentes podem nunca chamar uma ferramenta MCP por causa de descrições mal escritas, e o satisfaction of search bias faz o agente parar na primeira fonte encontrada ignorando fontes mais recentes (ex.: conversa no Slack da noite anterior)
- Acesso à informação não é compreensão: entregar entendimento ao modelo exige técnicas adicionais além de ingestão
- Em teste controlado (mesmo prompt e mesmo modelo), a tarefa consumiu ~21M de tokens sem contexto vs ~10,8M com contexto, economizando ~2 horas de wall-clock e melhorando a qualidade da resposta
- RAG isolado não responde perguntas relacionais como 'quais PRs abertos trabalhei na última semana com autenticação'; é necessário descobrir schema e gerar queries determinísticas
- O context engine deve resolver conflitos entre fontes (diagrama antigo vs Slack recente), respeitar permissões e governance para não vazar informação de projetos secretos, e otimizar respostas por superfície (humano vs machine-to-machine)
- Fornecer um 'mapa' completo de contexto permite ao modelo descobrir o território e revelar unknown unknowns da organização
- Casos de uso vão além de código: customer success resolvendo tickets em tempo real e vendas fechando negócios mais cedo consultando o context engine no campo

> **Deep dive:** `medium` — Apresenta densidade conceitual útil (armadilhas do contexto curado e do MCP, satisfaction of search bias, seis características de um context engine, métricas de economia de tokens e técnica RAG+queries relacionais) com ferramentas open source, mas permanece em nível de visão geral de palestra comercial, sem detalhes de implementação ou arquitetura aprofundados.
