---
title: "How to create any n8n workflow using ChatGPT"
type: "extract"
source: "youtube"
video_id: "lZuxqbw8IX4"
url: "https://www.youtube.com/watch?v=lZuxqbw8IX4"
channel: "David Ondrej"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-how-to-create-any-n8n-workflow-using-chatgpt--lZuxqbw8IX4.txt]]"
tags: ["agent-tooling", "agents", "multi-agent", "classification", "model-selection", "runtime", "stack-tooling", "process", "error-handling", "testes-qa", "production", "escalation"]
thesis: "É possível gerar workflows completos do n8n em JSON via ChatGPT (modelo de raciocínio o3) usando um projeto com system prompt e arquivos de exemplo, importar no n8n, corrigir credenciais/erros e implantar em VPS — eliminando horas de construção manual."
concepts: ["geração de workflows via LLM com few-shot de arquivos JSON de exemplo", "system prompt em projetos do ChatGPT referenciado em todo chat", "modelo de raciocínio (o3) vs modelo rápido para gerar JSON estruturado", "importação de workflow por arquivo JSON no n8n", "form trigger com elementos de formulário e URLs de teste/produção", "nó Switch com roteamento por correspondência exata de palavra-chave", "agentes especializados paralelos por tipo de bug (5 branches)", "AI agent com tools (Google Sheets read/append, Gmail send)", "seleção de modelo para agentes (GPT-4.1 por custo e aderência a instruções)", "criação de credenciais (OpenAI API key, Google OAuth via Google Cloud Console)", "mapeamento de parâmetros gerado por IA nas tools", "pin de dados de teste para reexecutar nodes individualmente", "ativação de workflow e URL de produção", "deploy em VPS com template one-click vs cloud com cobrança por execução"]
tools: ["ChatGPT", "OpenAI o3", "GPT-4.1", "GPT-4o", "Codex", "n8n", "Google Sheets", "Gmail", "Google Drive", "Google Cloud Console", "Discord", "Telegram", "Slack", "Hostinger VPS (KVM2)", "New Society"]
people: ["David Andre", "Vectal.ai", "OpenAI", "Hostinger", "n8n"]
claims: ["Configure um projeto no ChatGPT com system prompt detalhado + 4 arquivos JSON de exemplo para gerar workflows n8n prontos para importar", "Use um modelo de raciocínio (o3) em vez de modelos instantâneos (4o) ao gerar JSON de workflows complexos, pois o raciocínio prolongado melhora a estrutura", "Escolha GPT-4.1 como modelo dos agentes n8n pelo melhor custo-benefício e confiabilidade em seguir instruções", "No nó Switch do n8n, a regra de roteamento exige correspondência exata da palavra-chave com a opção do dropdown do formulário", "Desative temporariamente nodes downstream para conseguir testar o workflow quando há erros pendentes", "Fixe (pin) os dados de teste no n8n para reexecutar nodes individuais sem repetir o trigger do formulário", "Salve constantemente no n8n, pois recarregar a página sem salvar perde todo o progresso", "Use o botão 'AI generated' nos parâmetros das tools (Sheets/Gmail) para o modelo definir mapeamento de campos, assunto e corpo de e-mail", "Se o seletor de documento do Google Sheets não carregar no n8n, copie o ID do documento diretamente da URL e use o modo 'by ID'", "Erro de credencial OpenAI frequentemente se resolve adicionando crédito/billing na plataforma (US$2-3)", "Hospede agentes n8n em VPS (Hostinger KVM2, 8GB RAM, template one-click n8n) em vez do n8n cloud quando o custo por execução for limitante", "Agentes não implantados nunca rodam: ative o workflow e use a URL de produção (ou deploy em VPS) para execução autônoma", "Ao travar em qualquer etapa, volte ao ChatGPT/o3 com web search e descreva o erro claramente em vez de depurar às cegas"]
deep_dive: "low"
deep_dive_reason: "Tutorial passo-a-passo introdutório com técnica pouco nova (few-shot para gerar JSON) e forte carga promocional (Hostinger e comunidade paga), sem profundidade em harness, evals, governança ou arquitetura além de padrões triviais de orquestração."
---

# How to create any n8n workflow using ChatGPT

## Tese
É possível gerar workflows completos do n8n em JSON via ChatGPT (modelo de raciocínio o3) usando um projeto com system prompt e arquivos de exemplo, importar no n8n, corrigir credenciais/erros e implantar em VPS — eliminando horas de construção manual.

## Conceitos-chave
- geração de workflows via LLM com few-shot de arquivos JSON de exemplo
- system prompt em projetos do ChatGPT referenciado em todo chat
- modelo de raciocínio (o3) vs modelo rápido para gerar JSON estruturado
- importação de workflow por arquivo JSON no n8n
- form trigger com elementos de formulário e URLs de teste/produção
- nó Switch com roteamento por correspondência exata de palavra-chave
- agentes especializados paralelos por tipo de bug (5 branches)
- AI agent com tools (Google Sheets read/append, Gmail send)
- seleção de modelo para agentes (GPT-4.1 por custo e aderência a instruções)
- criação de credenciais (OpenAI API key, Google OAuth via Google Cloud Console)
- mapeamento de parâmetros gerado por IA nas tools
- pin de dados de teste para reexecutar nodes individualmente
- ativação de workflow e URL de produção
- deploy em VPS com template one-click vs cloud com cobrança por execução

## Ferramentas & pessoas
**Ferramentas:** ChatGPT, OpenAI o3, GPT-4.1, GPT-4o, Codex, n8n, Google Sheets, Gmail, Google Drive, Google Cloud Console, Discord, Telegram, Slack, Hostinger VPS (KVM2), New Society

**Pessoas/orgs:** David Andre, Vectal.ai, OpenAI, Hostinger, n8n

## Claims acionáveis
- Configure um projeto no ChatGPT com system prompt detalhado + 4 arquivos JSON de exemplo para gerar workflows n8n prontos para importar
- Use um modelo de raciocínio (o3) em vez de modelos instantâneos (4o) ao gerar JSON de workflows complexos, pois o raciocínio prolongado melhora a estrutura
- Escolha GPT-4.1 como modelo dos agentes n8n pelo melhor custo-benefício e confiabilidade em seguir instruções
- No nó Switch do n8n, a regra de roteamento exige correspondência exata da palavra-chave com a opção do dropdown do formulário
- Desative temporariamente nodes downstream para conseguir testar o workflow quando há erros pendentes
- Fixe (pin) os dados de teste no n8n para reexecutar nodes individuais sem repetir o trigger do formulário
- Salve constantemente no n8n, pois recarregar a página sem salvar perde todo o progresso
- Use o botão 'AI generated' nos parâmetros das tools (Sheets/Gmail) para o modelo definir mapeamento de campos, assunto e corpo de e-mail
- Se o seletor de documento do Google Sheets não carregar no n8n, copie o ID do documento diretamente da URL e use o modo 'by ID'
- Erro de credencial OpenAI frequentemente se resolve adicionando crédito/billing na plataforma (US$2-3)
- Hospede agentes n8n em VPS (Hostinger KVM2, 8GB RAM, template one-click n8n) em vez do n8n cloud quando o custo por execução for limitante
- Agentes não implantados nunca rodam: ative o workflow e use a URL de produção (ou deploy em VPS) para execução autônoma
- Ao travar em qualquer etapa, volte ao ChatGPT/o3 com web search e descreva o erro claramente em vez de depurar às cegas

> **Deep dive:** `low` — Tutorial passo-a-passo introdutório com técnica pouco nova (few-shot para gerar JSON) e forte carga promocional (Hostinger e comunidade paga), sem profundidade em harness, evals, governança ou arquitetura além de padrões triviais de orquestração.
