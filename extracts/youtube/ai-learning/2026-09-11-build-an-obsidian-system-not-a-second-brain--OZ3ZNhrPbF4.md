---
title: "Build an Obsidian SYSTEM Not a Second Brain!"
type: "extract"
source: "youtube"
video_id: "OZ3ZNhrPbF4"
url: "https://www.youtube.com/watch?v=OZ3ZNhrPbF4"
channel: "Eric Michaud"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-build-an-obsidian-system-not-a-second-brain--OZ3ZNhrPbF4.txt]]"
tags: ["knowledge-management", "context-management", "agent-tooling", "memory-architecture", "telemetry", "stack-tooling", "process", "analise"]
thesis: "Obsidian deve ser operado como um sistema único de trabalho (captura, inteligência, relatório e execução no mesmo lugar) em vez de workflows isolados, com agentes de IA complementando o vault como camada de automação e o vault servindo de memória para os agentes."
concepts: ["sistema vs. workflow (pensar em sistema, não em workflows isolados)", "vault Obsidian como sistema operacional pessoal", "camada de inteligência sobre notas (dashboard custom/mini app)", "daily notes com métricas modeladas como properties", "log de atividades contínuo como telemetry pessoal", "rotina de dois comandos (/today e close day)", "quick capture para inbox de ideias", "correlação de ações vs. resultados via gráficos sobrepostos (ex.: semanas de alta receita)", "fricção de troca de contexto como custo de produtividade", "Obsidian como memory layer para agentes de IA", "agente preenchendo gaps de entrada no vault e vice-versa", "agent-loop diário de abertura e fechamento com métricas"]
tools: ["Obsidian", "plugin custom de dashboard/inteligência", "Claude Code (mencionado como 'cloud code')", "Terminal / localhost embutido", "Canvas e views de gráficos do Obsidian", "ditado por voz", "Telegram", "Slack", "YouTube", "Skool (comunidade do autor)"]
people: ["YouTube", "Skool"]
claims: ["Inicie o dia com um único comando (ex.: '/today') executado por um agente que agrega calendário, inbox e carryovers do dia anterior para definir as 3 prioridades do dia", "Feche o dia com um comando (ex.: 'close day') usando ditado por voz para preencher as métricas restantes (tempo com família, esforço de 0-10) que são registradas automaticamente nas notas", "Modele as métricas diárias como properties das daily notes para que fiquem consultáveis pela camada de inteligência", "Registre toda atividade dentro do vault para depois correlacionar ações com resultados (ex.: replicar as ações das semanas de alta receita) usando gráficos sobrepostos", "Construa um mini app/plugin custom que lê as daily notes e expõe dashboard, heat map semanal, tendências e métricas de foco", "Elimine fricção de troca de contexto mantendo browser, terminal, agente e dashboard no mesmo ambiente, em vez de alternar entre aplicativos separados", "Use quick capture para jogar ideias num inbox e marque hábitos diários com toggles direto no dashboard", "Popule as prioridades diárias automaticamente a partir das notas do dia anterior, carregando pendências", "Trate o vault como o local único onde o trabalho acontece (não só captura), evitando o 'cemitério de notas' típico de PKMs"]
deep_dive: "low"
deep_dive_reason: "Tour promocional de vault com algumas práticas acionáveis (rotina de dois comandos, log de atividades), mas sem profundidade arquitetural em harness, context-engineering ou engenharia de agentes, terminando em pitch de comunidade paga."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-turn-10-994-notes-into-memory-paul-iusztin-decoding-ai-louis-francois-bouchard-t--ZRM_TfEZcIo|Turn 10,994 Notes Into Memory - Paul Iusztin, Decoding AI & Louis-François Bouchard, Towards AI]]", "[[extracts/youtube/ai-learning/2026-09-11-this-claude-code-x-obsidian-agentic-os-will-be-the-new-meta--njHuj8OxIVI|This Claude Code x Obsidian Agentic OS Will Be The New Meta]]", "[[extracts/youtube/ai-learning/2026-09-11-full-workshop-setting-yourself-up-for-success-jason-liu-openai-codex--il1c1a2FufU|Full Workshop: Setting Yourself Up for Success —Jason Liu, OpenAI Codex]]", "[[extracts/youtube/ai-learning/2026-09-11-build-a-claude-knowledge-base-that-self-improves--ib74sLgjIBM|Build A Claude Knowledge Base That Self-Improves!]]", "[[extracts/youtube/ai-learning/2026-09-11-ex-uber-dev-explains-his-multi-agent-workflow--utb7zYbK10c|Ex-Uber dev explains his Multi-Agent Workflow]]", "[[extracts/youtube/ai-learning/2026-09-11-matt-pococks-agentic-engineering-workflow-just-copy-him--nQwJVHCtDDY|Matt Pocock’s Agentic Engineering Workflow (just copy him)]]"]
---

# Build an Obsidian SYSTEM Not a Second Brain!

## Tese
Obsidian deve ser operado como um sistema único de trabalho (captura, inteligência, relatório e execução no mesmo lugar) em vez de workflows isolados, com agentes de IA complementando o vault como camada de automação e o vault servindo de memória para os agentes.

## Conceitos-chave
- sistema vs. workflow (pensar em sistema, não em workflows isolados)
- vault Obsidian como sistema operacional pessoal
- camada de inteligência sobre notas (dashboard custom/mini app)
- daily notes com métricas modeladas como properties
- log de atividades contínuo como telemetry pessoal
- rotina de dois comandos (/today e close day)
- quick capture para inbox de ideias
- correlação de ações vs. resultados via gráficos sobrepostos (ex.: semanas de alta receita)
- fricção de troca de contexto como custo de produtividade
- Obsidian como memory layer para agentes de IA
- agente preenchendo gaps de entrada no vault e vice-versa
- agent-loop diário de abertura e fechamento com métricas

## Ferramentas & pessoas
**Ferramentas:** Obsidian, plugin custom de dashboard/inteligência, Claude Code (mencionado como 'cloud code'), Terminal / localhost embutido, Canvas e views de gráficos do Obsidian, ditado por voz, Telegram, Slack, YouTube, Skool (comunidade do autor)

**Pessoas/orgs:** YouTube, Skool

## Claims acionáveis
- Inicie o dia com um único comando (ex.: '/today') executado por um agente que agrega calendário, inbox e carryovers do dia anterior para definir as 3 prioridades do dia
- Feche o dia com um comando (ex.: 'close day') usando ditado por voz para preencher as métricas restantes (tempo com família, esforço de 0-10) que são registradas automaticamente nas notas
- Modele as métricas diárias como properties das daily notes para que fiquem consultáveis pela camada de inteligência
- Registre toda atividade dentro do vault para depois correlacionar ações com resultados (ex.: replicar as ações das semanas de alta receita) usando gráficos sobrepostos
- Construa um mini app/plugin custom que lê as daily notes e expõe dashboard, heat map semanal, tendências e métricas de foco
- Elimine fricção de troca de contexto mantendo browser, terminal, agente e dashboard no mesmo ambiente, em vez de alternar entre aplicativos separados
- Use quick capture para jogar ideias num inbox e marque hábitos diários com toggles direto no dashboard
- Popule as prioridades diárias automaticamente a partir das notas do dia anterior, carregando pendências
- Trate o vault como o local único onde o trabalho acontece (não só captura), evitando o 'cemitério de notas' típico de PKMs

> **Deep dive:** `low` — Tour promocional de vault com algumas práticas acionáveis (rotina de dois comandos, log de atividades), mas sem profundidade arquitetural em harness, context-engineering ou engenharia de agentes, terminando em pitch de comunidade paga.
