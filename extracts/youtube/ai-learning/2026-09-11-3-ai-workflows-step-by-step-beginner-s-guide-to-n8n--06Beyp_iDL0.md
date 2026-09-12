---
title: "3 AI Workflows Step-by-Step (Beginner's Guide to n8n)"
type: "extract"
source: "youtube"
video_id: "06Beyp_iDL0"
url: "https://www.youtube.com/watch?v=06Beyp_iDL0"
channel: "Nate Herk | AI Automation"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-3-ai-workflows-step-by-step-beginner-s-guide-to-n8n--06Beyp_iDL0.txt]]"
tags: ["agents", "agent-tooling", "agentes-orquestracao", "classification", "knowledge-management", "context-management", "model-selection", "permissions", "error-handling", "verification", "testes-qa", "process", "production", "stack-tooling", "index"]
thesis: "Um tutorial introdutório que constrói três workflows em n8n (pipeline RAG com chatbot, resposta automática de suporte por email e criação de conteúdo para LinkedIn) demonstrando passo a passo a configuração de credenciais OAuth/API (Google Cloud, Pinecone, OpenRouter, OpenAI, Tavily) e a composição de agentes de IA com base de conhecimento vetorial, classificação de emails e busca na web."
concepts: ["RAG (Retrieval Augmented Generation)", "Vector database e embeddings", "Chunking / text splitting (recursive character text splitter)", "Namespaces para organização de dados no índice vetorial", "Credenciais OAuth2 (client ID, secret, consent screen, redirect URI, test user)", "Triggers de workflow (Google Drive, Gmail, schedule, manual)", "AI agent com chat model, system prompt e tools", "Descrição de tools para direcionar uso pelo agente", "Text classifier para roteamento por categorias", "HTTP request: POST vs GET e importação de cURL", "Pinned data para testes reprodutíveis", "Alterar status de linha em Google Sheets para evitar reprocessamento"]
tools: ["n8n", "Pinecone", "Google Drive", "Google Docs", "Gmail", "Google Sheets", "Google Cloud", "OpenRouter", "OpenAI text-embedding-3-small", "Claude 3.5 Sonnet", "GPT-4o mini", "Google Gemini 2.0 Flash", "Tavily API", "Excalidraw"]
people: ["Nate Herk (apresentador)", "OpenAI", "Anthropic", "Google", "Perplexity", "Tech Haven Solutions (empresa fictícia do demo)"]
claims: ["Todo workflow em n8n precisa de um trigger que o inicia (ex.: novo arquivo em pasta do Google Drive).", "A configuração OAuth do Google exige: habilitar a API específica, criar OAuth consent screen, adicionar-se como test user mantendo o app em modo teste, e criar um client web app com o redirect URI copiado do n8n.", "O modelo de embeddings usado na consulta deve ser exatamente o mesmo usado na ingestão no índice, senão a automação quebra.", "Use namespaces no Pinecone (ex.: 'FAQ') para organizar dados dentro de um índice e referencie o namespace correto na tool do agente, caso contrário ele não encontra a informação.", "O recursive character text splitter preserva o contexto global do documento ao fatiá-lo; defaults: chunk size 1000 e overlap 0.", "Dê nome e descrição claros à tool do agente (ex.: 'knowledge base — call this tool to access the policy and FAQ database') para controlar quando ele a usa.", "System prompts refinam comportamento do agente: persona, tom (emojis), assinatura e formato de saída (ex.: outputar apenas o corpo do email, sem assunto).", "Desative 'simplify' no trigger do Gmail para emails longos não serem truncados no conteúdo recuperado.", "Use pinned data no n8n para re-executar testes sem reconsultar a fonte original.", "Um text classifier com categorias e descrições (idealmente com exemplos de emails passados para maior acurácia) roteia cada email para um branch diferente de lógica.", "Responder email usando o message ID original mantém a resposta na mesma thread em vez de criar nova conversa.", "Desmarcar 'append n8n attribution' remove a nota 'sent by n8n' do email enviado.", "Erro 'provider returned error' em chat model geralmente indica problema na API key: resete a chave ou troque temporariamente de modelo para isolar a causa.", "Importar o comando cURL da documentação da API preenche automaticamente o nó HTTP Request (método, URL, headers, body).", "POST é usado quando se envia body data ao serviço; GET basta para apenas acessar/scrapar informação.", "Em Google Sheets, filtre pela coluna status igual a 'to do' com 'return only first matching row' para processar uma linha por execução e depois atualize o status para 'created' evitando duplicatas.", "Ativar o workflow (active) faz o schedule trigger rodar automaticamente em produção; use manual trigger para demonstrações.", "É possível estender o workflow de suporte com labels no Gmail e novos branches/classificações (ex.: financeiro) ligados a knowledge bases diferentes."]
deep_dive: "low"
deep_dive_reason: "Tutorial introdutório passo a passo de ferramenta com conceitos básicos de RAG e setup de credenciais, útil operacionalmente mas sem novidade arquitetural nem profundidade em harness, evals, agent-fleets ou governança."
---

# 3 AI Workflows Step-by-Step (Beginner's Guide to n8n)

## Tese
Um tutorial introdutório que constrói três workflows em n8n (pipeline RAG com chatbot, resposta automática de suporte por email e criação de conteúdo para LinkedIn) demonstrando passo a passo a configuração de credenciais OAuth/API (Google Cloud, Pinecone, OpenRouter, OpenAI, Tavily) e a composição de agentes de IA com base de conhecimento vetorial, classificação de emails e busca na web.

## Conceitos-chave
- RAG (Retrieval Augmented Generation)
- Vector database e embeddings
- Chunking / text splitting (recursive character text splitter)
- Namespaces para organização de dados no índice vetorial
- Credenciais OAuth2 (client ID, secret, consent screen, redirect URI, test user)
- Triggers de workflow (Google Drive, Gmail, schedule, manual)
- AI agent com chat model, system prompt e tools
- Descrição de tools para direcionar uso pelo agente
- Text classifier para roteamento por categorias
- HTTP request: POST vs GET e importação de cURL
- Pinned data para testes reprodutíveis
- Alterar status de linha em Google Sheets para evitar reprocessamento

## Ferramentas & pessoas
**Ferramentas:** n8n, Pinecone, Google Drive, Google Docs, Gmail, Google Sheets, Google Cloud, OpenRouter, OpenAI text-embedding-3-small, Claude 3.5 Sonnet, GPT-4o mini, Google Gemini 2.0 Flash, Tavily API, Excalidraw

**Pessoas/orgs:** Nate Herk (apresentador), OpenAI, Anthropic, Google, Perplexity, Tech Haven Solutions (empresa fictícia do demo)

## Claims acionáveis
- Todo workflow em n8n precisa de um trigger que o inicia (ex.: novo arquivo em pasta do Google Drive).
- A configuração OAuth do Google exige: habilitar a API específica, criar OAuth consent screen, adicionar-se como test user mantendo o app em modo teste, e criar um client web app com o redirect URI copiado do n8n.
- O modelo de embeddings usado na consulta deve ser exatamente o mesmo usado na ingestão no índice, senão a automação quebra.
- Use namespaces no Pinecone (ex.: 'FAQ') para organizar dados dentro de um índice e referencie o namespace correto na tool do agente, caso contrário ele não encontra a informação.
- O recursive character text splitter preserva o contexto global do documento ao fatiá-lo; defaults: chunk size 1000 e overlap 0.
- Dê nome e descrição claros à tool do agente (ex.: 'knowledge base — call this tool to access the policy and FAQ database') para controlar quando ele a usa.
- System prompts refinam comportamento do agente: persona, tom (emojis), assinatura e formato de saída (ex.: outputar apenas o corpo do email, sem assunto).
- Desative 'simplify' no trigger do Gmail para emails longos não serem truncados no conteúdo recuperado.
- Use pinned data no n8n para re-executar testes sem reconsultar a fonte original.
- Um text classifier com categorias e descrições (idealmente com exemplos de emails passados para maior acurácia) roteia cada email para um branch diferente de lógica.
- Responder email usando o message ID original mantém a resposta na mesma thread em vez de criar nova conversa.
- Desmarcar 'append n8n attribution' remove a nota 'sent by n8n' do email enviado.
- Erro 'provider returned error' em chat model geralmente indica problema na API key: resete a chave ou troque temporariamente de modelo para isolar a causa.
- Importar o comando cURL da documentação da API preenche automaticamente o nó HTTP Request (método, URL, headers, body).
- POST é usado quando se envia body data ao serviço; GET basta para apenas acessar/scrapar informação.
- Em Google Sheets, filtre pela coluna status igual a 'to do' com 'return only first matching row' para processar uma linha por execução e depois atualize o status para 'created' evitando duplicatas.
- Ativar o workflow (active) faz o schedule trigger rodar automaticamente em produção; use manual trigger para demonstrações.
- É possível estender o workflow de suporte com labels no Gmail e novos branches/classificações (ex.: financeiro) ligados a knowledge bases diferentes.

> **Deep dive:** `low` — Tutorial introdutório passo a passo de ferramenta com conceitos básicos de RAG e setup de credenciais, útil operacionalmente mas sem novidade arquitetural nem profundidade em harness, evals, agent-fleets ou governança.
