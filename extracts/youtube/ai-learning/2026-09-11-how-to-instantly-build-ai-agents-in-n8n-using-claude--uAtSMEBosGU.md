---
title: "How to INSTANTLY Build AI Agents in N8N Using Claude"
type: "extract"
source: "youtube"
video_id: "uAtSMEBosGU"
url: "https://www.youtube.com/watch?v=uAtSMEBosGU"
channel: "Nolan Harper | Chasing AI"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-how-to-instantly-build-ai-agents-in-n8n-using-claude--uAtSMEBosGU.txt]]"
tags: ["context-engineering", "knowledge-management", "agent-tooling", "stack-tooling", "process", "error-handling", "verification", "model-selection", "agentic-coding", "testes-qa", "monitoramento"]
thesis: "Um criador usa o Claude (Opus) em um Project carregado com a documentação do n8n para gerar workflows completos em JSON como ponto de partida, mas o setup manual de credenciais e a depuração de erros ainda exigem intervenção humana significativa."
concepts: ["Injeção de conhecimento em Claude Projects (arquivos README do n8n como contexto)", "Meta-prompting: pedir ao próprio agente o framework de prompt ideal", "Cadeia de modelos: ChatGPT para redigir o prompt a partir do framework gerado pelo Claude", "Estrutura de system prompt (overview, context, instructions, tools, examples, SOPs, final notes)", "Exportação/importação de workflow como JSON", "Setup manual de credenciais em nós vermelhos", "Configuração de error handling (continue using error output) para roteamento condicional", "Teste com trigger manual antes do agendamento", "Human-in-the-loop como verificação final do artefato gerado"]
tools: ["Claude", "Claude 4 Opus", "ChatGPT", "n8n", "Gmail", "Slack", "Google Sheets", "Google Drive", "GitHub", "OpenAI (nó message model / GPT-4.1 mini)", "Microsoft Word", "PDF"]
people: ["Anthropic", "OpenAI", "n8n", "Slack", "Google"]
claims: ["Compilar os READMEs da documentação do n8n e carregá-los como knowledge em um Claude Project permite que o modelo raciocine sobre nós, integrações e estrutura de workflows", "Pedir ao agente que ele mesmo gere o framework/guidelines do prompt produz melhores resultados do que adivinhar o prompt manualmente", "Usar ChatGPT como redator intermediário para expandir o framework em um prompt completo funciona como pipeline de prompt-crafting", "O workflow gerado pelo Claude pode ser baixado como JSON e importado diretamente no n8n com nós, instruções e passos de setup", "Os nós gerados chegam 'vermelhos' e exigem conexão manual de credenciais (Gmail, Slack, Google Sheets) e correção de campos como datetime", "Configurar o comportamento on-error do nó OpenAI para 'continue using error output' é necessário para o roteamento if/else de sucesso vs. erro funcionar", "Variáveis de mensagem no Slack podem não puxar automaticamente e precisam ser reatribuídas à saída correta do nó anterior", "Claude não substitui o especialista em automação ainda, mas serve como starting point sólido quando se fornece contexto sobre inputs, fontes de dados, processamento, outputs e regras do projeto", "A parte difícil da automação é conceituar o workflow, não construí-lo — e é essa habilidade que o autor considera seu maior valor"]
deep_dive: "low"
deep_dive_reason: "Tutorial demonstrativo de nível iniciante, com setup manual passo a passo e apelo promocional, oferecendo padrões úteis (injeção de documentação e meta-prompting) mas sem densidade arquitetural, novidade ou profundidade em harness, evals ou governança."
---

# How to INSTANTLY Build AI Agents in N8N Using Claude

## Tese
Um criador usa o Claude (Opus) em um Project carregado com a documentação do n8n para gerar workflows completos em JSON como ponto de partida, mas o setup manual de credenciais e a depuração de erros ainda exigem intervenção humana significativa.

## Conceitos-chave
- Injeção de conhecimento em Claude Projects (arquivos README do n8n como contexto)
- Meta-prompting: pedir ao próprio agente o framework de prompt ideal
- Cadeia de modelos: ChatGPT para redigir o prompt a partir do framework gerado pelo Claude
- Estrutura de system prompt (overview, context, instructions, tools, examples, SOPs, final notes)
- Exportação/importação de workflow como JSON
- Setup manual de credenciais em nós vermelhos
- Configuração de error handling (continue using error output) para roteamento condicional
- Teste com trigger manual antes do agendamento
- Human-in-the-loop como verificação final do artefato gerado

## Ferramentas & pessoas
**Ferramentas:** Claude, Claude 4 Opus, ChatGPT, n8n, Gmail, Slack, Google Sheets, Google Drive, GitHub, OpenAI (nó message model / GPT-4.1 mini), Microsoft Word, PDF

**Pessoas/orgs:** Anthropic, OpenAI, n8n, Slack, Google

## Claims acionáveis
- Compilar os READMEs da documentação do n8n e carregá-los como knowledge em um Claude Project permite que o modelo raciocine sobre nós, integrações e estrutura de workflows
- Pedir ao agente que ele mesmo gere o framework/guidelines do prompt produz melhores resultados do que adivinhar o prompt manualmente
- Usar ChatGPT como redator intermediário para expandir o framework em um prompt completo funciona como pipeline de prompt-crafting
- O workflow gerado pelo Claude pode ser baixado como JSON e importado diretamente no n8n com nós, instruções e passos de setup
- Os nós gerados chegam 'vermelhos' e exigem conexão manual de credenciais (Gmail, Slack, Google Sheets) e correção de campos como datetime
- Configurar o comportamento on-error do nó OpenAI para 'continue using error output' é necessário para o roteamento if/else de sucesso vs. erro funcionar
- Variáveis de mensagem no Slack podem não puxar automaticamente e precisam ser reatribuídas à saída correta do nó anterior
- Claude não substitui o especialista em automação ainda, mas serve como starting point sólido quando se fornece contexto sobre inputs, fontes de dados, processamento, outputs e regras do projeto
- A parte difícil da automação é conceituar o workflow, não construí-lo — e é essa habilidade que o autor considera seu maior valor

> **Deep dive:** `low` — Tutorial demonstrativo de nível iniciante, com setup manual passo a passo e apelo promocional, oferecendo padrões úteis (injeção de documentação e meta-prompting) mas sem densidade arquitetural, novidade ou profundidade em harness, evals ou governança.
