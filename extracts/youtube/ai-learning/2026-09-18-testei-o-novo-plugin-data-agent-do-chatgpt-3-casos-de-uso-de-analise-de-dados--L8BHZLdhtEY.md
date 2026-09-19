---
title: "Testei o NOVO PLUGIN DATA AGENT do ChatGPT: 3 Casos de Uso de Análise de dados"
type: "extract"
source: "youtube"
video_id: "L8BHZLdhtEY"
url: "https://www.youtube.com/watch?v=L8BHZLdhtEY"
channel: "Antonio Bennati | Dados & IA"
extracted: "2026-09-18"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-18-testei-o-novo-plugin-data-agent-do-chatgpt-3-casos-de-uso-de-analise-de-dados--L8BHZLdhtEY.txt]]"
tags: ["agent-tooling", "agents", "analise", "data-platform", "model-selection", "stack-tooling", "verification", "process", "agent-context"]
thesis: "O novo agente de dados do ChatGPT (plugin Data Analytics) agrupa skills de análise, qualidade de dados e visualização com conectores a planilhas, bancos e BI, permitindo gerar análises, dashboards publicáveis e relatórios auditáveis a partir de prompts simples com perguntas de negócio."
concepts: ["agente de dados / plugin Data Analytics", "plugins e skills compostas (data quality, KPI reporting, diagnóstico de métricas, visualização)", "conectores de dados (Google Drive, Supabase, BigQuery, Databricks, MongoDB, Power BI, Tableau, Omni, Oracle BI)", "seleção de modelo e nível de esforço versus capacidade do plugin", "prompts orientados a perguntas de negócio em vez de especificações de gráficos", "verificação de resultados via SQL gerado pelo agente", "qualidade de dados autônoma (datas como texto, nulos, duplicatas, consistência matemática)", "leitura de modelo semântico do Power BI (não screenshot)", "automação de atualização periódica de dashboard ligada ao banco", "memória/proatividade do ChatGPT com dados dos apps", "gate de plano/versão para conectores (BigQuery, Power BI desktop)"]
tools: ["ChatGPT", "Data Analytics plugin (data agent)", "Google Drive", "Supabase", "BigQuery", "Databricks", "MongoDB", "Power BI", "Tableau", "Omni", "Oracle BI", "Gmail", "ChatGPT Sites (canvas/dashboards)", "ChatGPT Desktop", "modelos Terra e Astra"]
people: ["OpenAI", "Antônio Benatti", "Anthropic", "Google", "Microsoft", "Supabase"]
claims: ["Instale o plugin Data Analytics pela página do recurso e invoque-o no chat com @dataanalytics antes de pedir análises", "Para análises relativamente simples, um modelo intermediário (Terra) com esforço alto basta, pois as skills do plugin já entregam a capacidade analítica — dispensando o modelo topo (Astra)", "Inclua perguntas de negócio no prompt (ex.: desempenho melhorou ou piorou? qual canal não converte?) para o agente desenhar dashboards e insights orientados à decisão, sem especificar gráficos", "O agente detecta e corrige automaticamente problemas de qualidade como datas armazenadas como texto, nulos, duplicatas e inconsistências matemáticas antes de calcular", "Use 'view data source' para copiar a SQL gerada e rodá-la no banco (ex.: Supabase) para validar os números do dashboard — padrão de auditoria replicável", "O conector BigQuery está disponível apenas em plano avançado; o plugin do Power BI funciona somente no app desktop do ChatGPT, não na versão web", "Combine o plugin Power BI + data agent para ler o modelo semântico de um relatório aberto e responder perguntas de prioridade para liderança; especifique 'não altere o relatório' se quiser apenas leitura", "Dashboards publicados via Sites podem ser compartilhados por link ou e-mail e ter atualização agendada (ex.: semanal) sincronizada com o banco conectado", "Com o conector Gmail, o agente gera rascunho de relatório em HTML no corpo do e-mail com cards, conclusões e link para o dashboard", "Desativar memória nas configurações do ChatGPT impede que dados dos apps sejam usados proativamente para sugestões", "Referencie explicitamente o nome da planilha/tabela no prompt para garantir que o agente use a fonte correta de dados"]
deep_dive: "medium"
deep_dive_reason: "Tutorial replicável com dicas acionáveis (seleção de modelo versus skills do plugin, prompts por perguntas de negócio, validação via SQL e portões de plano/conector), mas sem profundidade arquitetural em harness, evals ou governança e com tom promocional de canal."
theme: "Tutoriais de ferramentas de IA"
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-chatgpt-for-business-updates--9lSRViLugE0|ChatGPT for Business Updates]]", "[[extracts/youtube/ai-learning/2026-09-11-5-simple-ai-agents-you-must-have-beginners-guide--WLvQCIUWebs|5 simple AI Agents you must have - beginners guide]]", "[[extracts/youtube/ai-learning/2026-09-11-from-zero-to-your-first-ai-agent-in-25-minutes-no-coding--EH5jx5qPabU|From Zero to Your First AI Agent in 25 Minutes (No Coding)]]", "[[extracts/youtube/ai-learning/2026-09-11-7-mind-blowing-new-use-cases-for-chatgpt-in-2025-big-changes-ahead--8IUkOAvMP-M|7 Mind-Blowing NEW Use Cases For ChatGPT in 2025 (Big Changes Ahead)]]", "[[extracts/youtube/ai-learning/2026-09-11-10-insane-ai-agent-use-cases-in-n8n-steal-these--Dt6u-yFEpsk|10 Insane AI Agent Use Cases in n8n! (steal these)]]", "[[extracts/youtube/ai-learning/2026-09-11-building-gtm-ai-agents-lessons-from-deploying-to-6-000-users-sait-izmit-snowflak--DrTdD-ttjCY|Building GTM AI Agents: Lessons from Deploying to 6,000 Users — Sait Izmit, Snowflake]]", "[[extracts/youtube/ai-learning/2026-09-11-performance-monitor-is-going-enterprise--ZIt_R8GwP7s|Performance Monitor is Going Enterprise]]"]
---

# Testei o NOVO PLUGIN DATA AGENT do ChatGPT: 3 Casos de Uso de Análise de dados

## Tese
O novo agente de dados do ChatGPT (plugin Data Analytics) agrupa skills de análise, qualidade de dados e visualização com conectores a planilhas, bancos e BI, permitindo gerar análises, dashboards publicáveis e relatórios auditáveis a partir de prompts simples com perguntas de negócio.

## Conceitos-chave
- agente de dados / plugin Data Analytics
- plugins e skills compostas (data quality, KPI reporting, diagnóstico de métricas, visualização)
- conectores de dados (Google Drive, Supabase, BigQuery, Databricks, MongoDB, Power BI, Tableau, Omni, Oracle BI)
- seleção de modelo e nível de esforço versus capacidade do plugin
- prompts orientados a perguntas de negócio em vez de especificações de gráficos
- verificação de resultados via SQL gerado pelo agente
- qualidade de dados autônoma (datas como texto, nulos, duplicatas, consistência matemática)
- leitura de modelo semântico do Power BI (não screenshot)
- automação de atualização periódica de dashboard ligada ao banco
- memória/proatividade do ChatGPT com dados dos apps
- gate de plano/versão para conectores (BigQuery, Power BI desktop)

## Ferramentas & pessoas
**Ferramentas:** ChatGPT, Data Analytics plugin (data agent), Google Drive, Supabase, BigQuery, Databricks, MongoDB, Power BI, Tableau, Omni, Oracle BI, Gmail, ChatGPT Sites (canvas/dashboards), ChatGPT Desktop, modelos Terra e Astra

**Pessoas/orgs:** OpenAI, Antônio Benatti, Anthropic, Google, Microsoft, Supabase

## Claims acionáveis
- Instale o plugin Data Analytics pela página do recurso e invoque-o no chat com @dataanalytics antes de pedir análises
- Para análises relativamente simples, um modelo intermediário (Terra) com esforço alto basta, pois as skills do plugin já entregam a capacidade analítica — dispensando o modelo topo (Astra)
- Inclua perguntas de negócio no prompt (ex.: desempenho melhorou ou piorou? qual canal não converte?) para o agente desenhar dashboards e insights orientados à decisão, sem especificar gráficos
- O agente detecta e corrige automaticamente problemas de qualidade como datas armazenadas como texto, nulos, duplicatas e inconsistências matemáticas antes de calcular
- Use 'view data source' para copiar a SQL gerada e rodá-la no banco (ex.: Supabase) para validar os números do dashboard — padrão de auditoria replicável
- O conector BigQuery está disponível apenas em plano avançado; o plugin do Power BI funciona somente no app desktop do ChatGPT, não na versão web
- Combine o plugin Power BI + data agent para ler o modelo semântico de um relatório aberto e responder perguntas de prioridade para liderança; especifique 'não altere o relatório' se quiser apenas leitura
- Dashboards publicados via Sites podem ser compartilhados por link ou e-mail e ter atualização agendada (ex.: semanal) sincronizada com o banco conectado
- Com o conector Gmail, o agente gera rascunho de relatório em HTML no corpo do e-mail com cards, conclusões e link para o dashboard
- Desativar memória nas configurações do ChatGPT impede que dados dos apps sejam usados proativamente para sugestões
- Referencie explicitamente o nome da planilha/tabela no prompt para garantir que o agente use a fonte correta de dados

> **Deep dive:** `medium` — Tutorial replicável com dicas acionáveis (seleção de modelo versus skills do plugin, prompts por perguntas de negócio, validação via SQL e portões de plano/conector), mas sem profundidade arquitetural em harness, evals ou governança e com tom promocional de canal.
