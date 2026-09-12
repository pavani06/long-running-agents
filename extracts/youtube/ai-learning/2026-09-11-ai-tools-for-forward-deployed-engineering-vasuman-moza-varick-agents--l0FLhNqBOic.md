---
title: "AI tools for Forward Deployed Engineering — Vasuman Moza, Varick Agents"
type: "extract"
source: "youtube"
video_id: "l0FLhNqBOic"
url: "https://www.youtube.com/watch?v=l0FLhNqBOic"
channel: "AI Engineer"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-ai-tools-for-forward-deployed-engineering-vasuman-moza-varick-agents--l0FLhNqBOic.txt]]"
tags: ["agents", "agent-tooling", "context-engineering", "knowledge-management", "ontologia", "process", "production", "model-selection", "arquitetura", "evals", "governanca", "stack-tooling"]
thesis: "A execução de trabalho por IA deixou de ser o gargalo (modelos e harnesses com MCP/browser-use já executam quase perfeitamente); o próximo gargalo é a profundidade de entendimento e reengenharia dos processos de cada cliente, escalável apenas com engenharia forward-deployed (FDE) amplificada por um FD agent interno que opera sobre um grafo de dependências da empresa."
concepts: ["Forward Deployed Engineering (FDE) e o FDE assistido por IA", "FD agent em três estágios: agente de engajamento, agente de workflow embutido na plataforma e assistente autônomo para mudanças de workflow", "Grafo de dependências (DAG) como fonte única de verdade do funcionamento da empresa", "Entity resolution entre fontes (email, Slack, documentação) para identificar pessoas e owners de processo", "Post-training de modelos open-source para equilibrar detalhe e concisão onde modelos de fronteira falham", "Ambiente de RL com ferramentas customizadas para travessia confiável do knowledge graph", "Reengenharia de processos em torno da IA (mistura de passos autônomos, human-in-the-loop e humanos) em vez de colar IA sobre processos quebrados", "Documentação do golden path vs. realidade dos caminhos de falha e exceções", "Construção de agentes sobre sistemas de registro existentes sem exigir migração", "Governança e evals embutidos na plataforma de agentes", "Mapeamento de processo via entrevistas com process leads (AP, AR, reconciliação, billing, FP&A)"]
tools: ["Veric OS", "FD Agent (interno da Veric)", "Cursor", "Claude", "Codex", "Factory", "Granola", "Kimi K2.6", "NetSuite", "Salesforce", "Microsoft Dynamics", "SAP", "Postgres", "MCP", "browser-use tooling"]
people: ["Voss (CEO, Veric Agents)", "JD Puit (head de engenharia/plataforma, Veric)", "Veric Agents", "Anthropic", "OpenAI", "Cursor", "Factory", "MIT (estudo citado sobre falha de pilotos de IA generativa)"]
claims: ["Execução de knowledge work está praticamente resolvida pelos modelos e harnesses atuais; o gargalo migrou para extrair, modelar e reengenhariar o contexto específico de cada negócio", "Estatísticas citadas: ~95% dos pilotos de IA generativa não chegam à produção (MIT) e 87% não geram ROI mensurável, porque IA é aplicada sobre processos quebrados", "Entrevistas com process leads devem capturar caminhos de falha reais (quem assume, tempos de ciclo, exceções), pois a documentação existente cobre só o golden path", "O redesenho do workflow deve mudar o suficiente para capturar ROI sem quebrar adoção: exemplo de 8 passos, 4 autônomos, 3 com human-in-the-loop e 1 permanente para humano por risco ou baixa singularidade", "Em enterprise, construa agentes sobre os sistemas de registro (NetSuite, SAP, Salesforce, Dynamics) em vez de pedir migração — cliente citado gastou US$5M e 5 anos migrando para NetSuite e não tem apetite para mudar", "Representar a empresa como grafo de dependências funciona porque processos enterprise são majoritariamente lineares com ciclos e os owners de processo querem execução guiada por dependência", "Modelos de fronteira são excessivamente verbosos e não sabem distinguir detalhe crítico de detalhe dispensável; post-training sobre modelos open-source (ex.: Kimi K2.6) restaura o balanço detalhe/clareza", "Travessia confiável do knowledge graph exige treinar ferramentas customizadas via RL: entity resolution entre identidades, detecção de ciclos de redundância e violações do DAG", "Estágios do FD agent: assistente de engajamento que sintetiza docs/notas e resolve entidades; agente de workflow dentro da plataforma que valida o fluxo construído pelo FDE e aponta edge cases; assistente autônomo que processa emails de mudança e aplica alterações no workflow sem intervenção do FDE", "Transformações departamentais holísticas entregam ROI de 25–75% contra 5–10% de point solutions (prospecting em vendas ou AP isolado em finanças)", "O FD agent permite que um único FDE gerencie várias frentes de comunicação com clientes simultaneamente, evitando escalar headcount exponencialmente"]
deep_dive: "medium"
deep_dive_reason: "Há nuggets arquiteturais acionáveis e relativamente novos (grafo de dependências como fonte de verdade, post-training de modelos open-source para concisão, ambiente RL com ferramentas customizadas para travessia do knowledge graph, agente de workflow embutido na plataforma), mas o conteúdo é diluído por pitch promocional da Veric e carece de detalhes concretos sobre evals e harness."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-the-future-of-ai-agents-with-andrew-ng-interrupt-26--OaRhpwz_TGM|The Future of AI Agents with Andrew Ng | Interrupt 26]]", "[[extracts/youtube/ai-learning/2026-09-11-stanford-cs153-frontier-systems-the-ai-native-company-how-one-founder-becomes-a--Lri2LNYtERM|Stanford CS153 Frontier Systems | The AI Native Company: How One Founder Becomes a 1000x Engineer]]", "[[extracts/youtube/ai-learning/2026-09-11-75m-founder-reveals-his-agentic-engineering-setup--QBfXiWvM0qc|$75M founder reveals his Agentic Engineering setup]]", "[[extracts/youtube/ai-learning/2026-09-11-agentic-engineering-explained-by-a-10x-developer--FU5_kpTAVDo|Agentic Engineering, explained by a 10x developer]]", "[[extracts/youtube/ai-learning/2026-09-11-how-to-build-your-entire-ai-workforce-in-one-afternoon-live-demo--oulVKbk0umo|How to Build Your Entire AI Workforce in One Afternoon (Live Demo)]]", "[[extracts/youtube/ai-learning/2026-09-11-l8-principal-s-agentic-engineering-setup-just-copy-him--8ZgpAXe5V5w|L8 Principal's Agentic Engineering Setup (just copy him)]]", "[[extracts/youtube/ai-learning/2026-09-11-rip-to-rpa-how-ai-makes-operations-work--O6DtzLGLNWY|RIP to RPA: How AI Makes Operations Work]]", "[[extracts/youtube/ai-learning/2026-09-11-the-production-ai-playbook-deploying-agents-at-enterprise-scale-sandipan-bhaumik--ObTPqBGsEbA|The Production AI Playbook: Deploying Agents at Enterprise Scale — Sandipan Bhaumik, Databricks]]", "[[extracts/youtube/ai-learning/2026-09-11-o-treinamento-secreto-da-ia-que-vai-mudar-tudo-vetto-ai--Z4BXg02i8sI|O treinamento secreto da IA que vai mudar tudo | Vetto AI]]", "[[extracts/youtube/ai-learning/2026-09-11-the-enterprise-ai-stack-behind-stripes-company-brain-kai--AbZODZ_4VaM|The enterprise AI stack behind Stripe’s company brain “Kai”]]", "[[extracts/youtube/ai-learning/2026-09-11-why-we-killed-our-multi-agent-pipeline-subbiah-sethuraman-and-abhilash-asokan-zs--u6jJcIFDLE4|Why We Killed Our Multi-Agent Pipeline — Subbiah Sethuraman and Abhilash Asokan, ZS Associates]]"]
theme: "Agentes em Produção com Evals"
---

# AI tools for Forward Deployed Engineering — Vasuman Moza, Varick Agents

## Tese
A execução de trabalho por IA deixou de ser o gargalo (modelos e harnesses com MCP/browser-use já executam quase perfeitamente); o próximo gargalo é a profundidade de entendimento e reengenharia dos processos de cada cliente, escalável apenas com engenharia forward-deployed (FDE) amplificada por um FD agent interno que opera sobre um grafo de dependências da empresa.

## Conceitos-chave
- Forward Deployed Engineering (FDE) e o FDE assistido por IA
- FD agent em três estágios: agente de engajamento, agente de workflow embutido na plataforma e assistente autônomo para mudanças de workflow
- Grafo de dependências (DAG) como fonte única de verdade do funcionamento da empresa
- Entity resolution entre fontes (email, Slack, documentação) para identificar pessoas e owners de processo
- Post-training de modelos open-source para equilibrar detalhe e concisão onde modelos de fronteira falham
- Ambiente de RL com ferramentas customizadas para travessia confiável do knowledge graph
- Reengenharia de processos em torno da IA (mistura de passos autônomos, human-in-the-loop e humanos) em vez de colar IA sobre processos quebrados
- Documentação do golden path vs. realidade dos caminhos de falha e exceções
- Construção de agentes sobre sistemas de registro existentes sem exigir migração
- Governança e evals embutidos na plataforma de agentes
- Mapeamento de processo via entrevistas com process leads (AP, AR, reconciliação, billing, FP&A)

## Ferramentas & pessoas
**Ferramentas:** Veric OS, FD Agent (interno da Veric), Cursor, Claude, Codex, Factory, Granola, Kimi K2.6, NetSuite, Salesforce, Microsoft Dynamics, SAP, Postgres, MCP, browser-use tooling

**Pessoas/orgs:** Voss (CEO, Veric Agents), JD Puit (head de engenharia/plataforma, Veric), Veric Agents, Anthropic, OpenAI, Cursor, Factory, MIT (estudo citado sobre falha de pilotos de IA generativa)

## Claims acionáveis
- Execução de knowledge work está praticamente resolvida pelos modelos e harnesses atuais; o gargalo migrou para extrair, modelar e reengenhariar o contexto específico de cada negócio
- Estatísticas citadas: ~95% dos pilotos de IA generativa não chegam à produção (MIT) e 87% não geram ROI mensurável, porque IA é aplicada sobre processos quebrados
- Entrevistas com process leads devem capturar caminhos de falha reais (quem assume, tempos de ciclo, exceções), pois a documentação existente cobre só o golden path
- O redesenho do workflow deve mudar o suficiente para capturar ROI sem quebrar adoção: exemplo de 8 passos, 4 autônomos, 3 com human-in-the-loop e 1 permanente para humano por risco ou baixa singularidade
- Em enterprise, construa agentes sobre os sistemas de registro (NetSuite, SAP, Salesforce, Dynamics) em vez de pedir migração — cliente citado gastou US$5M e 5 anos migrando para NetSuite e não tem apetite para mudar
- Representar a empresa como grafo de dependências funciona porque processos enterprise são majoritariamente lineares com ciclos e os owners de processo querem execução guiada por dependência
- Modelos de fronteira são excessivamente verbosos e não sabem distinguir detalhe crítico de detalhe dispensável; post-training sobre modelos open-source (ex.: Kimi K2.6) restaura o balanço detalhe/clareza
- Travessia confiável do knowledge graph exige treinar ferramentas customizadas via RL: entity resolution entre identidades, detecção de ciclos de redundância e violações do DAG
- Estágios do FD agent: assistente de engajamento que sintetiza docs/notas e resolve entidades; agente de workflow dentro da plataforma que valida o fluxo construído pelo FDE e aponta edge cases; assistente autônomo que processa emails de mudança e aplica alterações no workflow sem intervenção do FDE
- Transformações departamentais holísticas entregam ROI de 25–75% contra 5–10% de point solutions (prospecting em vendas ou AP isolado em finanças)
- O FD agent permite que um único FDE gerencie várias frentes de comunicação com clientes simultaneamente, evitando escalar headcount exponencialmente

> **Deep dive:** `medium` — Há nuggets arquiteturais acionáveis e relativamente novos (grafo de dependências como fonte de verdade, post-training de modelos open-source para concisão, ambiente RL com ferramentas customizadas para travessia do knowledge graph, agente de workflow embutido na plataforma), mas o conteúdo é diluído por pitch promocional da Veric e carece de detalhes concretos sobre evals e harness.
