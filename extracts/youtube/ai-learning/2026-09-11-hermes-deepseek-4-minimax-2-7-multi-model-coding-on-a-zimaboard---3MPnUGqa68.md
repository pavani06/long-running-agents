---
title: "Hermes + DeepSeek 4 + MiniMax 2.7: Multi-Model Coding on a ZimaBoard"
type: "extract"
source: "youtube"
video_id: "-3MPnUGqa68"
url: "https://www.youtube.com/watch?v=-3MPnUGqa68"
channel: "Zero to MVP"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-hermes-deepseek-4-minimax-2-7-multi-model-coding-on-a-zimaboard---3MPnUGqa68.txt]]"
tags: ["agents", "multi-agent", "agent-tooling", "agentic-coding", "agent-loop", "verification", "model-selection", "process", "runtime"]
thesis: "Um agente Hermes executando 24/7 em um single-board computer (Zimaboard 2) pode coordenar modelos LLM externos (DeepSeek como cérebro e MiniMax via OpenCode ou mecanismo nativo de delegate task) para planejar, implementar, verificar e auditar tarefas de desenvolvimento de software quase autonomamente."
concepts: ["coordenação multi-modelo com agente orquestrador", "delegação de tarefas (delegate task) para modelo externo", "planejamento detalhado antes da implementação", "verificação por tarefa e auditoria técnica ao final", "autonomia com mínima intervenção humana", "execução de agente 24/7 em hardware dedicado", "isolamento de ambiente entre agente e máquina do usuário", "persistência de sessões via tmux e acesso SSH", "geração de relatórios de execução pelo agente", "atualização do system prompt para rotear escrita de código ao modelo delegado", "compilação para binário único como critério de leveza (Nim)"]
tools: ["Hermes (agente)", "DeepSeek", "MiniMax 2.7", "OpenCode", "Zimaboard 2", "tmux", "SSH", "Bun", "Rust", "Nim", "MacBook"]
people: ["DeepSeek", "MiniMax", "Zimaboard"]
claims: ["Rodar o agente em um single-board computer 24/7 elimina interrupções causadas por fechar laptops e fornece isolamento bidirecional de ambiente (reboots do host não afetam o agente e vice-versa)", "O modelo de escrita de código pode ser plugado via OpenCode ou via seção 'delegation' da configuração do Hermes, bastando adicionar o provider e atualizar o system prompt para usar a ferramenta delegate task", "tmux permite conectar e desconcontar por SSH quantas vezes quiser sem afetar processos em execução, e permite abrir outro terminal para instalar dependências (ex.: Rust) sem interromper o agente", "Na primeira tarefa (exportação PDF/HTML em editor markdown com backend Rust), Hermes planejou, delegou ao MiniMax, verificou cada tarefa individualmente e concluiu em cerca de 9 minutos", "O export HTML reproduziu fielmente imagens, formatação e cores, enquanto o PDF perdeu as imagens mas manteve texto, formatação e cores", "Na segunda tarefa (serviço web agregador de RSS em Nim), o Hermes gerou um plano grande e detalhado, o implementou sem intervenção e realizou auditoria técnica final encontrando 4 bugs — porém esperou aprovação humana em vez de corrigi-los automaticamente", "O agregador em Nim compilou em um binário único de menos de 700KB, com toda a funcionalidade do servidor", "A sincronização de feeds do serviço ocorre apenas no startup (sem botão dedicado) e cliques em títulos de artigos não funcionavam — bugs deixados para iteração futura", "Verificação funcional final exigiu copiar o código para outra máquina, pois o board não tem monitor nem ambiente gráfico"]
deep_dive: "medium"
deep_dive_reason: "Demonstração prática com detalhes acionáveis de configuração de delegação multi-modelo, verificação por tarefa e auditoria final, mas sem profundidade arquitetural, evals formais ou novidade técnica substantiva."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-hermes-co-founder-on-building-an-ai-agent-that-improves-itself-karan-malhotra--UWjh5Z4s8jY|Hermes Co-Founder on Building an AI Agent That Improves Itself | Karan Malhotra]]", "[[extracts/youtube/ai-learning/2026-09-11-l8-principal-s-agentic-engineering-setup-just-copy-him--8ZgpAXe5V5w|L8 Principal's Agentic Engineering Setup (just copy him)]]", "[[extracts/youtube/ai-learning/2026-09-11-dynamic-subagents-how-to-run-parallel-agents-reliably-in-deep-agents--5AkdMangfNk|Dynamic Subagents: How to Run Parallel Agents Reliably in Deep Agents]]", "[[extracts/youtube/ai-learning/2026-09-11-the-multi-agent-architecture-that-actually-ships-luke-alvoeiro-factory--ow1we5PzK-o|The Multi-Agent Architecture That Actually Ships — Luke Alvoeiro, Factory]]", "[[extracts/youtube/ai-learning/2026-09-11-how-i-automate-my-own-job-at-hugging-face-using-agents-niels-rogge-hugging-face--FLUoowDJg4I|How I automate my own job at Hugging Face using agents — Niels Rogge, Hugging Face]]", "[[extracts/youtube/ai-learning/2026-09-11-anthropic-workshop-build-agents-that-run-for-hours-ash-prabaker-andrew-wilson--mR-WAvEPRwE|Anthropic Workshop: Build Agents That Run for Hours — Ash Prabaker & Andrew Wilson]]"]
theme: "Processo de Engenharia Agêntica"
---

# Hermes + DeepSeek 4 + MiniMax 2.7: Multi-Model Coding on a ZimaBoard

## Tese
Um agente Hermes executando 24/7 em um single-board computer (Zimaboard 2) pode coordenar modelos LLM externos (DeepSeek como cérebro e MiniMax via OpenCode ou mecanismo nativo de delegate task) para planejar, implementar, verificar e auditar tarefas de desenvolvimento de software quase autonomamente.

## Conceitos-chave
- coordenação multi-modelo com agente orquestrador
- delegação de tarefas (delegate task) para modelo externo
- planejamento detalhado antes da implementação
- verificação por tarefa e auditoria técnica ao final
- autonomia com mínima intervenção humana
- execução de agente 24/7 em hardware dedicado
- isolamento de ambiente entre agente e máquina do usuário
- persistência de sessões via tmux e acesso SSH
- geração de relatórios de execução pelo agente
- atualização do system prompt para rotear escrita de código ao modelo delegado
- compilação para binário único como critério de leveza (Nim)

## Ferramentas & pessoas
**Ferramentas:** Hermes (agente), DeepSeek, MiniMax 2.7, OpenCode, Zimaboard 2, tmux, SSH, Bun, Rust, Nim, MacBook

**Pessoas/orgs:** DeepSeek, MiniMax, Zimaboard

## Claims acionáveis
- Rodar o agente em um single-board computer 24/7 elimina interrupções causadas por fechar laptops e fornece isolamento bidirecional de ambiente (reboots do host não afetam o agente e vice-versa)
- O modelo de escrita de código pode ser plugado via OpenCode ou via seção 'delegation' da configuração do Hermes, bastando adicionar o provider e atualizar o system prompt para usar a ferramenta delegate task
- tmux permite conectar e desconcontar por SSH quantas vezes quiser sem afetar processos em execução, e permite abrir outro terminal para instalar dependências (ex.: Rust) sem interromper o agente
- Na primeira tarefa (exportação PDF/HTML em editor markdown com backend Rust), Hermes planejou, delegou ao MiniMax, verificou cada tarefa individualmente e concluiu em cerca de 9 minutos
- O export HTML reproduziu fielmente imagens, formatação e cores, enquanto o PDF perdeu as imagens mas manteve texto, formatação e cores
- Na segunda tarefa (serviço web agregador de RSS em Nim), o Hermes gerou um plano grande e detalhado, o implementou sem intervenção e realizou auditoria técnica final encontrando 4 bugs — porém esperou aprovação humana em vez de corrigi-los automaticamente
- O agregador em Nim compilou em um binário único de menos de 700KB, com toda a funcionalidade do servidor
- A sincronização de feeds do serviço ocorre apenas no startup (sem botão dedicado) e cliques em títulos de artigos não funcionavam — bugs deixados para iteração futura
- Verificação funcional final exigiu copiar o código para outra máquina, pois o board não tem monitor nem ambiente gráfico

> **Deep dive:** `medium` — Demonstração prática com detalhes acionáveis de configuração de delegação multi-modelo, verificação por tarefa e auditoria final, mas sem profundidade arquitetural, evals formais ou novidade técnica substantiva.
