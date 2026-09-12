---
title: "How to INSTANTLY Generate N8N Workflows Using Claude"
type: "extract"
source: "youtube"
video_id: "9tj4MxCV6g0"
url: "https://www.youtube.com/watch?v=9tj4MxCV6g0"
channel: "Ethan Nelson"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-how-to-instantly-generate-n8n-workflows-using-claude--9tj4MxCV6g0.txt]]"
tags: ["agent-tooling", "context-engineering", "knowledge-management", "process", "stack-tooling", "verification"]
thesis: "Um projeto no Claude com instruções de sistema e uma base de conhecimento de JSONs de workflows n8n pode gerar ou recriar automações a partir de prompts, screenshots ou transcrições, entregando cerca de 80% do build e acelerando drasticamente a entrega de agências de automação."
concepts: ["Claude Projects como harness de geração de workflows", "Base de conhecimento com exemplos (JSONs de workflows) como contexto few-shot", "Instruções de sistema em XML para formatação de saída", "Engenharia reversa de workflows a partir de screenshots", "Geração de workflows a partir de transcrições de tutoriais", "Saída como artifact/arquivo JSON baixável e importável no n8n", "Validação de JSON completo antes da importação", "Limites de comprimento de mensagem dividindo JSON em múltiplos arquivos", "Correção manual dos ~20% restantes (nós quebrados, API keys)", "Espectro serviços produtizados vs. builds totalmente custom", "Delegação de builds 80% completos a contractors com Loom de 5 minutos", "Escopagem de projetos custom a partir de transcrição de call de vendas"]
tools: ["Claude (Projects)", "n8n", "Airtable", "OpenAI", "Make", "Tally Forms", "PandaDoc", "Supabase", "Loom", "YouTube", "DuckDuckGo", "comey.ai (gerador de transcrições de vídeo)"]
people: ["Ethan (autor do vídeo, dono de agência de IA)", "AI Agent University (comunidade promovida no vídeo)"]
claims: ["Configure um Claude Project com instruções de sistema (prompt XML) e faça upload de JSONs de workflows n8n reais como knowledge base para habilitar a geração de novos workflows", "Peça explicitamente que a saída seja um artifact JSON baixável e que o JSON seja válido do início ao fim", "A geração atinge ~80% do workflow em 1-2 prompts, exigindo revisão manual (ex.: reconectar nós OpenAI, inserir API keys)", "Workflows podem ser recriados apenas colando um screenshot no Claude dentro do projeto", "Transcrições de tutoriais do YouTube podem ser usadas como especificação para gerar o workflow correspondente", "Claude pode atingir o limite de comprimento de mensagem e dividir o JSON em dois arquivos; verifique a completude antes de importar", "Erros de 'invalid JSON data' na importação do n8n indicam geração incompleta; peça para continuar/regenerar", "Use o gerador para escopar projetos customizados (faixa de US$ 3-12 mil, recentemente US$ 8-12 mil) e delegar o build a contractors com um Loom de 5 minutos", "Prefira começar com builds totalmente custom e acumular sistemas até emergir um serviço produtizado, em vez de visar produtização desde o início"]
deep_dive: "low"
deep_dive_reason: "Tutorial promocional de agência com um único padrão replicável (projeto Claude + base de exemplos JSON) apresentado em demos superficiais, sem profundidade em harness, evals, arquitetura ou governança."
---

# How to INSTANTLY Generate N8N Workflows Using Claude

## Tese
Um projeto no Claude com instruções de sistema e uma base de conhecimento de JSONs de workflows n8n pode gerar ou recriar automações a partir de prompts, screenshots ou transcrições, entregando cerca de 80% do build e acelerando drasticamente a entrega de agências de automação.

## Conceitos-chave
- Claude Projects como harness de geração de workflows
- Base de conhecimento com exemplos (JSONs de workflows) como contexto few-shot
- Instruções de sistema em XML para formatação de saída
- Engenharia reversa de workflows a partir de screenshots
- Geração de workflows a partir de transcrições de tutoriais
- Saída como artifact/arquivo JSON baixável e importável no n8n
- Validação de JSON completo antes da importação
- Limites de comprimento de mensagem dividindo JSON em múltiplos arquivos
- Correção manual dos ~20% restantes (nós quebrados, API keys)
- Espectro serviços produtizados vs. builds totalmente custom
- Delegação de builds 80% completos a contractors com Loom de 5 minutos
- Escopagem de projetos custom a partir de transcrição de call de vendas

## Ferramentas & pessoas
**Ferramentas:** Claude (Projects), n8n, Airtable, OpenAI, Make, Tally Forms, PandaDoc, Supabase, Loom, YouTube, DuckDuckGo, comey.ai (gerador de transcrições de vídeo)

**Pessoas/orgs:** Ethan (autor do vídeo, dono de agência de IA), AI Agent University (comunidade promovida no vídeo)

## Claims acionáveis
- Configure um Claude Project com instruções de sistema (prompt XML) e faça upload de JSONs de workflows n8n reais como knowledge base para habilitar a geração de novos workflows
- Peça explicitamente que a saída seja um artifact JSON baixável e que o JSON seja válido do início ao fim
- A geração atinge ~80% do workflow em 1-2 prompts, exigindo revisão manual (ex.: reconectar nós OpenAI, inserir API keys)
- Workflows podem ser recriados apenas colando um screenshot no Claude dentro do projeto
- Transcrições de tutoriais do YouTube podem ser usadas como especificação para gerar o workflow correspondente
- Claude pode atingir o limite de comprimento de mensagem e dividir o JSON em dois arquivos; verifique a completude antes de importar
- Erros de 'invalid JSON data' na importação do n8n indicam geração incompleta; peça para continuar/regenerar
- Use o gerador para escopar projetos customizados (faixa de US$ 3-12 mil, recentemente US$ 8-12 mil) e delegar o build a contractors com um Loom de 5 minutos
- Prefira começar com builds totalmente custom e acumular sistemas até emergir um serviço produtizado, em vez de visar produtização desde o início

> **Deep dive:** `low` — Tutorial promocional de agência com um único padrão replicável (projeto Claude + base de exemplos JSON) apresentado em demos superficiais, sem profundidade em harness, evals, arquitetura ou governança.
