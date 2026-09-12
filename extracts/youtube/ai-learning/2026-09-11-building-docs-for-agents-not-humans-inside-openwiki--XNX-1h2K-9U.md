---
title: "Building Docs for Agents, Not Humans: Inside OpenWiki"
type: "extract"
source: "youtube"
video_id: "XNX-1h2K-9U"
url: "https://www.youtube.com/watch?v=XNX-1h2K-9U"
channel: "LangChain"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-building-docs-for-agents-not-humans-inside-openwiki--XNX-1h2K-9U.txt]]"
tags: ["context-engineering", "context-management", "knowledge-management", "documentation-publishing", "agent-tooling", "stack-tooling", "memory-architecture", "evals", "token-budgeting", "index", "ontologia", "roadmap"]
thesis: "OpenWiki é uma CLI open source que gera e mantém automaticamente documentação de repositórios estruturada para consumo por agentes (via formato OKF, index, changelog e análise do histórico git), sustentando a tese de que memória de propósito geral é a próxima grande fronteira dos agentes."
concepts: ["Documentação agent-first (fragmentos autossuficientes, headings precisos, otimização para janela de contexto)", "Memória de propósito geral para agentes", "Open Knowledge Format (OKF) com front matter YAML determinístico (type, title, description, resource, tags, timestamp)", "Atualização automática via cron em GitHub Actions", "Geração de docs orientada por histórico do Git (commits, mensagens)", "Estrutura de wiki: quickstart.md, index.md por diretório, log.md como changelog", "Injeção de contexto via AGENTS.md/CLAUDE.md como mecanismo de descoberta pelo agente", "Trade-off geração vs. recuperação de documentação", "Passada determinística pós-agente para conformidade com OKF e metadados", "Arquivos de controle como last_update.json para atualização idempotente", "Ferramentas dedicadas de busca/filtro/query sobre a wiki como evolução da injeção em AGENTS.md"]
tools: ["OpenWiki (CLI, npm, MIT)", "OKF — Google Open Knowledge Format (v0.1/v0.2)", "AGENTS.md", "CLAUDE.md", "GitHub Actions (cron diário)", "DeepSWE (benchmark)", "Git (histórico de commits)", "NPM", "Claude Code"]
people: ["Harrison (CEO)", "Sean", "Andrej Karpathy (referência ao LLM wiki)", "Google (especificação OKF)"]
claims: ["Documentação para agentes deve ser composta de fragmentos autossuficientes com headings precisos e previsíveis, otimizados para caber na janela de contexto, em vez de narrativas com quickstart e screenshots pensados para humanos.", "Adotar front matter determinístico do OKF (type, title, description, tags) permite filtragem e busca rápidas na wiki — ex.: 'retorne todos os docs de arquitetura' — e agrega mais valor na recuperação do que na geração.", "Recuperação de documentação é um problema mais difícil que geração; o próximo passo é dar ao agente ferramentas dedicadas de busca/filtro/query em vez de depender apenas de injeção em AGENTS.md/CLAUDE.md.", "Incluir o histórico do Git (commits e mensagens), e não só o snapshot atual do repo, melhora a qualidade da documentação gerada.", "Em avaliações preliminares com subset do DeepSWE (20 tarefas), OpenWiki reduziu significativamente chamadas de ferramenta, buscas e consumo de tokens, com sucesso subindo levemente de ~7-8 para ~9-10 tarefas.", "A cadência de atualização deve escalar com o volume de commits: cron diário por padrão, ajustável para 4-8 horas em repos de alto tráfego.", "Um changelog (log.md) é essencial para humanos auditarem o que mudou a cada atualização da wiki, já que os arquivos são commitados no codebase.", "A suposição de que só agentes leriam a docs estava errada: humanos continuam no loop e a adição de diagramas (sequência, estado, fluxo) melhorou muito o consumo humano.", "last_update.json permite pular a execução do agente quando não houve mudanças desde a última atualização, evitando custo desnecessário.", "Onboarding de developer tool precisa ser trivial (instalação via npm + openwiki init com wizard) ou ocorre churn; init escreve automaticamente workflow do GitHub Actions e modificação do AGENTS.md."]
deep_dive: "medium"
deep_dive_reason: "Há insight acionável real sobre arquitetura de documentação para agentes (OKF, index/changelog, git-history, injeção via AGENTS.md, dados de eval de consumo de tokens), mas parte da palestra é promocional e o pipeline em si (CLI + cron + agente escrevendo docs) tem novidade moderada em relação a harness/context-engineering de fronteira."
---

# Building Docs for Agents, Not Humans: Inside OpenWiki

## Tese
OpenWiki é uma CLI open source que gera e mantém automaticamente documentação de repositórios estruturada para consumo por agentes (via formato OKF, index, changelog e análise do histórico git), sustentando a tese de que memória de propósito geral é a próxima grande fronteira dos agentes.

## Conceitos-chave
- Documentação agent-first (fragmentos autossuficientes, headings precisos, otimização para janela de contexto)
- Memória de propósito geral para agentes
- Open Knowledge Format (OKF) com front matter YAML determinístico (type, title, description, resource, tags, timestamp)
- Atualização automática via cron em GitHub Actions
- Geração de docs orientada por histórico do Git (commits, mensagens)
- Estrutura de wiki: quickstart.md, index.md por diretório, log.md como changelog
- Injeção de contexto via AGENTS.md/CLAUDE.md como mecanismo de descoberta pelo agente
- Trade-off geração vs. recuperação de documentação
- Passada determinística pós-agente para conformidade com OKF e metadados
- Arquivos de controle como last_update.json para atualização idempotente
- Ferramentas dedicadas de busca/filtro/query sobre a wiki como evolução da injeção em AGENTS.md

## Ferramentas & pessoas
**Ferramentas:** OpenWiki (CLI, npm, MIT), OKF — Google Open Knowledge Format (v0.1/v0.2), AGENTS.md, CLAUDE.md, GitHub Actions (cron diário), DeepSWE (benchmark), Git (histórico de commits), NPM, Claude Code

**Pessoas/orgs:** Harrison (CEO), Sean, Andrej Karpathy (referência ao LLM wiki), Google (especificação OKF)

## Claims acionáveis
- Documentação para agentes deve ser composta de fragmentos autossuficientes com headings precisos e previsíveis, otimizados para caber na janela de contexto, em vez de narrativas com quickstart e screenshots pensados para humanos.
- Adotar front matter determinístico do OKF (type, title, description, tags) permite filtragem e busca rápidas na wiki — ex.: 'retorne todos os docs de arquitetura' — e agrega mais valor na recuperação do que na geração.
- Recuperação de documentação é um problema mais difícil que geração; o próximo passo é dar ao agente ferramentas dedicadas de busca/filtro/query em vez de depender apenas de injeção em AGENTS.md/CLAUDE.md.
- Incluir o histórico do Git (commits e mensagens), e não só o snapshot atual do repo, melhora a qualidade da documentação gerada.
- Em avaliações preliminares com subset do DeepSWE (20 tarefas), OpenWiki reduziu significativamente chamadas de ferramenta, buscas e consumo de tokens, com sucesso subindo levemente de ~7-8 para ~9-10 tarefas.
- A cadência de atualização deve escalar com o volume de commits: cron diário por padrão, ajustável para 4-8 horas em repos de alto tráfego.
- Um changelog (log.md) é essencial para humanos auditarem o que mudou a cada atualização da wiki, já que os arquivos são commitados no codebase.
- A suposição de que só agentes leriam a docs estava errada: humanos continuam no loop e a adição de diagramas (sequência, estado, fluxo) melhorou muito o consumo humano.
- last_update.json permite pular a execução do agente quando não houve mudanças desde a última atualização, evitando custo desnecessário.
- Onboarding de developer tool precisa ser trivial (instalação via npm + openwiki init com wizard) ou ocorre churn; init escreve automaticamente workflow do GitHub Actions e modificação do AGENTS.md.

> **Deep dive:** `medium` — Há insight acionável real sobre arquitetura de documentação para agentes (OKF, index/changelog, git-history, injeção via AGENTS.md, dados de eval de consumo de tokens), mas parte da palestra é promocional e o pipeline em si (CLI + cron + agente escrevendo docs) tem novidade moderada em relação a harness/context-engineering de fronteira.
