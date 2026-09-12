---
title: "Google's OKF - The New Way to Structure Your Knowledge for Agents"
type: "extract"
source: "youtube"
video_id: "MY9F9K7wWX4"
url: "https://www.youtube.com/watch?v=MY9F9K7wWX4"
channel: "Marie Haynes "
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-google-s-okf-the-new-way-to-structure-your-knowledge-for-agents--MY9F9K7wWX4.txt]]"
tags: ["ontologia", "knowledge-management", "context-engineering", "agents", "memory-architecture", "index", "documentation-publishing", "process", "stack-tooling", "arquitetura", "analise"]
thesis: "O Open Knowledge Format (OKF) do Google é uma especificação mínima baseada em markdown que estrutura conhecimento de negócios/pessoal em 'knowledge bundles' de arquivos-conceito consumíveis por agentes, formalizando o padrão LLM-wiki de Andrej Karpathy e abrindo uma nova economia de venda de conhecimento curado para agentes."
concepts: ["Open Knowledge Format (OKF)", "LLM wiki pattern", "knowledge bundle (diretório de diretórios com arquivos markdown)", "arquivo-conceito (uma unidade de conhecimento por arquivo markdown)", "YAML front matter (type, title, description, resource tags, timestamp)", "index file obrigatório por bundle", "log file para rastrear atualizações do agente", "cross-linking formando knowledge graph", "type 'playbook' (processo disparado por evento)", "manutenção incremental do wiki pelo LLM (atualizar entidades, revisar resumos, notar contradições)", "'semantic unbaking'", "descoberta de OKF via llms.txt", "contraste com RAG (mapa curado vs. recuperação em massa)", "contraste com schema (conceitos naturais vs. mapear toda entidade)", "venda de bundles de conhecimento proprietário (advogado, contador, SEO)"]
tools: ["Google OKF", "Markdown", "YAML", "GitHub (spec.md)", "Notion", "Obsidian", "NotebookLM", "Gemini", "BigQuery", "GA4", "llms.txt", "MCP/WebMCP", "ferramenta de conversão de páginas web em OKF (autoria incerta na transcrição)"]
people: ["Google", "Andrej Karpathy", "Marie Haynes (autora do vídeo)", "Saganthan Mahana Dawson (nome possivelmente distorcido na transcrição)"]
claims: ["OKF formaliza o LLM wiki pattern descrito por Andrej Karpathy: o LLM constrói e mantém incrementalmente um wiki persistente em vez de apenas recuperar de documentos brutos em query time", "Cada arquivo markdown em um bundle representa um conceito único, e um site pode gerar dezenas de conceitos em vez de converter cada página 1:1", "Todo bundle precisa de um index file, e um log file permite ao agente registrar o que atualizou e quando", "Não há schema registry; o formato é intencionalmente minimalista, com YAML front matter (type, title, description, resource tags, timestamp) seguido de corpo livre com links e citações opcionais", "Delegue ao LLM a geração do YAML front matter fornecendo o spec.md do GitHub", "O type 'playbook' codifica processos disparados por eventos (ex.: diagnóstico de queda de tráfego), instruindo o agente onde buscar no 'cérebro' do negócio", "Ao adicionar novas fontes, o agente deve integrar em páginas-conceito existentes e descobrir novos links, não criar conceitos duplicados", "OKF substitui a suposição do RAG/LLM sobre como organizar dados (ex.: pedidos de clientes no BigQuery) pela forma explícita da organização", "A descoberta de OKFs por agentes provavelmente ocorrerá via llms.txt apontando para o bundle", "Duas fontes de receita: prestar serviço de estruturação de OKF para negócios e vender bundles de conhecimento proprietário que se integram ao OKF do comprador", "Método prático de aprendizado: colocar a documentação do Google e o spec.md no NotebookLM e pedir ao Gemini 20 ideias de uso no seu negócio", "Bundles podem ser armazenados gratuitamente em repositórios git ou organizadores markdown como Notion/Obsidian, sem software proprietário"]
deep_dive: "medium"
deep_dive_reason: "Apresenta uma especificação nova e estruturante (OKF/LLM-wiki) com detalhes operacionais acionáveis e relevância direta a ontologia e context-engineering, mas é uma visão inicial e entusiasmada de uma v1 proposta, com muita especulação sobre monetização e sem profundidade em harness, evals ou governança."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-building-docs-for-agents-not-humans-inside-openwiki--XNX-1h2K-9U|Building Docs for Agents, Not Humans: Inside OpenWiki]]", "[[extracts/youtube/ai-learning/2026-09-11-turn-10-994-notes-into-memory-paul-iusztin-decoding-ai-louis-francois-bouchard-t--ZRM_TfEZcIo|Turn 10,994 Notes Into Memory - Paul Iusztin, Decoding AI & Louis-François Bouchard, Towards AI]]", "[[extracts/youtube/ai-learning/2026-09-11-build-a-claude-knowledge-base-that-self-improves--ib74sLgjIBM|Build A Claude Knowledge Base That Self-Improves!]]", "[[extracts/youtube/ai-learning/2026-09-11-i-want-llama3-to-perform-10x-with-my-private-knowledge-local-agentic-rag-w-llama--u5Vcrwpzoz8|\"I want Llama3 to perform 10x with my private knowledge\" - Local Agentic RAG w/ llama3]]", "[[extracts/youtube/ai-learning/2026-09-11-from-coding-to-knowledge-work-agents-karan-vaidya-composio--xxfMT-bPEmU|From coding to Knowledge work agents — Karan Vaidya, Composio]]", "[[extracts/youtube/ai-learning/2026-09-11-openwiki-brains-general-purpose-memory-for-agents--sBg90v2qfas|OpenWiki Brains, general-purpose memory for agents]]"]
---

# Google's OKF - The New Way to Structure Your Knowledge for Agents

## Tese
O Open Knowledge Format (OKF) do Google é uma especificação mínima baseada em markdown que estrutura conhecimento de negócios/pessoal em 'knowledge bundles' de arquivos-conceito consumíveis por agentes, formalizando o padrão LLM-wiki de Andrej Karpathy e abrindo uma nova economia de venda de conhecimento curado para agentes.

## Conceitos-chave
- Open Knowledge Format (OKF)
- LLM wiki pattern
- knowledge bundle (diretório de diretórios com arquivos markdown)
- arquivo-conceito (uma unidade de conhecimento por arquivo markdown)
- YAML front matter (type, title, description, resource tags, timestamp)
- index file obrigatório por bundle
- log file para rastrear atualizações do agente
- cross-linking formando knowledge graph
- type 'playbook' (processo disparado por evento)
- manutenção incremental do wiki pelo LLM (atualizar entidades, revisar resumos, notar contradições)
- 'semantic unbaking'
- descoberta de OKF via llms.txt
- contraste com RAG (mapa curado vs. recuperação em massa)
- contraste com schema (conceitos naturais vs. mapear toda entidade)
- venda de bundles de conhecimento proprietário (advogado, contador, SEO)

## Ferramentas & pessoas
**Ferramentas:** Google OKF, Markdown, YAML, GitHub (spec.md), Notion, Obsidian, NotebookLM, Gemini, BigQuery, GA4, llms.txt, MCP/WebMCP, ferramenta de conversão de páginas web em OKF (autoria incerta na transcrição)

**Pessoas/orgs:** Google, Andrej Karpathy, Marie Haynes (autora do vídeo), Saganthan Mahana Dawson (nome possivelmente distorcido na transcrição)

## Claims acionáveis
- OKF formaliza o LLM wiki pattern descrito por Andrej Karpathy: o LLM constrói e mantém incrementalmente um wiki persistente em vez de apenas recuperar de documentos brutos em query time
- Cada arquivo markdown em um bundle representa um conceito único, e um site pode gerar dezenas de conceitos em vez de converter cada página 1:1
- Todo bundle precisa de um index file, e um log file permite ao agente registrar o que atualizou e quando
- Não há schema registry; o formato é intencionalmente minimalista, com YAML front matter (type, title, description, resource tags, timestamp) seguido de corpo livre com links e citações opcionais
- Delegue ao LLM a geração do YAML front matter fornecendo o spec.md do GitHub
- O type 'playbook' codifica processos disparados por eventos (ex.: diagnóstico de queda de tráfego), instruindo o agente onde buscar no 'cérebro' do negócio
- Ao adicionar novas fontes, o agente deve integrar em páginas-conceito existentes e descobrir novos links, não criar conceitos duplicados
- OKF substitui a suposição do RAG/LLM sobre como organizar dados (ex.: pedidos de clientes no BigQuery) pela forma explícita da organização
- A descoberta de OKFs por agentes provavelmente ocorrerá via llms.txt apontando para o bundle
- Duas fontes de receita: prestar serviço de estruturação de OKF para negócios e vender bundles de conhecimento proprietário que se integram ao OKF do comprador
- Método prático de aprendizado: colocar a documentação do Google e o spec.md no NotebookLM e pedir ao Gemini 20 ideias de uso no seu negócio
- Bundles podem ser armazenados gratuitamente em repositórios git ou organizadores markdown como Notion/Obsidian, sem software proprietário

> **Deep dive:** `medium` — Apresenta uma especificação nova e estruturante (OKF/LLM-wiki) com detalhes operacionais acionáveis e relevância direta a ontologia e context-engineering, mas é uma visão inicial e entusiasmada de uma v1 proposta, com muita especulação sobre monetização e sem profundidade em harness, evals ou governança.
