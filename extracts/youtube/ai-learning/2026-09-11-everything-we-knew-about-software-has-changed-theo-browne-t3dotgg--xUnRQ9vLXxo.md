---
title: "Everything we knew about software has changed — Theo Browne, @t3dotgg ​"
type: "extract"
source: "youtube"
video_id: "xUnRQ9vLXxo"
url: "https://www.youtube.com/watch?v=xUnRQ9vLXxo"
channel: "AI Engineer"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-everything-we-knew-about-software-has-changed-theo-browne-t3dotgg--xUnRQ9vLXxo.txt]]"
tags: ["agents", "agentes-orquestracao", "agentic-coding", "model-selection", "arquitetura", "decision-discipline", "process", "analise-estrutural", "roadmap"]
thesis: "Como os modelos evoluíram da era de tool calls (Sonnet 3.5) para tarefas longas (Opus 4.5) e agora orquestração nativa (Mythos) — melhorando mais rápido que os próprios desenvolvedores —, a única resposta estratégica é 'ir maior': abandonar práticas herdadas da era pré-agentes e construir produtos mais largos, pois cada tier de projeto desceu um nível, a ponto de um arquivo markdown executável competir como produto."
concepts: ["Eras de modelos: tool calls (Sonnet 3.5), tarefas de longa duração (Opus 4.5), orquestração (Mythos)", "Orquestração nativa pelo modelo: spawn de submodelos, decomposição de trabalho e verificação via prompt, sem tooling customizado", "'Go bigger' como imperativo estratégico frente a modelos que melhoram mais rápido que os humanos", "Skeuomorfismo em software: terminal, Vim e identidade de ferramentas como apego ao familiar", "Questionamento de convenções herdadas (env files fora do git, identidade por linguagem, medo de deletar código, guilt-merge de PRs)", "Colapso de tiers de projeto: startup vira side project; markdown executável como novo piso de produto", "Markdown como serviço: pipelines executáveis via Codex/Claude agendados por cron", "Largura (range) vs profundidade (depth) de produto como eixo de decisão estratégica", "Arquitetura extensível pelo usuário: gaps de features deixam de ser problema quando o próprio usuário constrói o que falta (padrão Slack/Slackbot)", "Ausência de custo emocional ao descartar trabalho de agentes"]
tools: ["Claude Sonnet 3.5", "Claude Opus 4.5", "Mythos/Fable (modelo)", "Codex", "Claude", "OBS", "Git", "tmux", "GNU screen", "SSH", "Vim", "cron", "GitHub", "Amazon S3", "AWS RDS", "Vercel", "Slackbot API"]
people: ["Apple", "Vercel", "AWS", "Slack", "Salesforce", "npm"]
claims: ["Sonnet 3.5 foi o primeiro modelo a executar tool calls de forma consistente e confiável o suficiente para coding diário em codebases reais", "Opus 4.5 foi o salto que permitiu tarefas de horas: o modelo testava o próprio trabalho e mantinha o raciocínio de ponta a ponta sem perder o contexto", "Mythos faz orquestração nativa: entende a si mesmo, spawna modelos adicionais, divide o trabalho e verifica o resultado — basta pedir via prompt, sem fábrica de software customizada", "Os modelos estão melhorando mais rápido que os desenvolvedores; a resposta não é 'melhorar' mas aumentar a ambição do que se constrói", "Práticas herdadas devem ser auditadas: perguntar 'isso é feito porque é certo ou porque sempre foi assim?' (ex.: proibição de commit de env files é limitação do Git, não boa prática)", "Sunk cost deve ser combatido: deletar código e resetar costuma ser a solução certa, e guilt-mergear PRs de agentes (ou humanos) deve cessar — trabalho de agente pode ser descartado sem culpa", "Todo tier de projeto desceu um nível: o que exigia startup agora é side project, e o novo piso é um markdown file executável via pipe para Codex ou Claude em cron", "Um markdown file em cron pode substituir um serviço: triagem e revisão de PRs em 4 repositórios GitHub, priorização, publicação de HTML estático no S3 e entrega de URL às 9h diariamente", "A estratégia largura-vs-profundidade inverteu: plataformas deep como Vercel ainda vencem seu nicho, mas o range amplo estilo AWS virou viável — uma plataforma de banco de dados pode ser embutida no produto em 1-2 dias de trabalho", "Arquitetar para extensibilidade transforma gaps de feature em não-problema: se usuários conseguem construir o que falta (como fazem com a Slackbot API), pode-se competir diretamente com incumbentes como Slack, AWS e Salesforce", "O limite do 'grande demais' ficou desconhecido (treinar modelo próprio? SO próprio?), o que exige testar propositadamente o que excede o que 'faz sentido' para descobrir os novos limites"]
deep_dive: "medium"
deep_dive_reason: "Palestra de visão/mindset com insights acionáveis pontuais (orquestração via prompt, markdown como serviço, colapso de tiers, largura vs profundidade), mas sem densidade técnica em harness, evals, context-engineering ou governança que justifique tier alto."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-why-the-frontrunners-say-coding-is-solved-but-engineering-is-not--Q7l8YGiMgUw|Why the Frontrunners Say Coding Is Solved BUT Engineering is Not]]", "[[extracts/youtube/ai-learning/2026-09-11-agentic-engineering-explained-by-a-10x-developer--FU5_kpTAVDo|Agentic Engineering, explained by a 10x developer]]", "[[extracts/youtube/ai-learning/2026-09-11-loop-engineering-to-graph-engineering--BOOfy3Yshtw|Loop Engineering to Graph Engineering]]", "[[extracts/youtube/ai-learning/2026-09-11-head-of-claude-code-on-the-future-of-work-and-productivity--kRgdkOw82F0|Head of Claude Code on the future of work and productivity]]", "[[extracts/youtube/ai-learning/2026-09-11-75m-founder-reveals-his-agentic-engineering-setup--QBfXiWvM0qc|$75M founder reveals his Agentic Engineering setup]]", "[[extracts/youtube/ai-learning/2026-09-11-my-agentic-engineering-workflow-after-6-775-sessions--c9nRxEy1kUY|My Agentic Engineering Workflow (after 6,775 sessions)]]", "[[extracts/youtube/ai-learning/2026-09-11-the-pipeline-is-dead-iris-ten-teije-sky-valley-ambient-computing--bRnoEpoK5m4|The Pipeline Is Dead - Iris ten Teije, Sky Valley Ambient Computing]]"]
theme: "Engenharia de Agentes Confiáveis"
---

# Everything we knew about software has changed — Theo Browne, @t3dotgg ​

## Tese
Como os modelos evoluíram da era de tool calls (Sonnet 3.5) para tarefas longas (Opus 4.5) e agora orquestração nativa (Mythos) — melhorando mais rápido que os próprios desenvolvedores —, a única resposta estratégica é 'ir maior': abandonar práticas herdadas da era pré-agentes e construir produtos mais largos, pois cada tier de projeto desceu um nível, a ponto de um arquivo markdown executável competir como produto.

## Conceitos-chave
- Eras de modelos: tool calls (Sonnet 3.5), tarefas de longa duração (Opus 4.5), orquestração (Mythos)
- Orquestração nativa pelo modelo: spawn de submodelos, decomposição de trabalho e verificação via prompt, sem tooling customizado
- 'Go bigger' como imperativo estratégico frente a modelos que melhoram mais rápido que os humanos
- Skeuomorfismo em software: terminal, Vim e identidade de ferramentas como apego ao familiar
- Questionamento de convenções herdadas (env files fora do git, identidade por linguagem, medo de deletar código, guilt-merge de PRs)
- Colapso de tiers de projeto: startup vira side project; markdown executável como novo piso de produto
- Markdown como serviço: pipelines executáveis via Codex/Claude agendados por cron
- Largura (range) vs profundidade (depth) de produto como eixo de decisão estratégica
- Arquitetura extensível pelo usuário: gaps de features deixam de ser problema quando o próprio usuário constrói o que falta (padrão Slack/Slackbot)
- Ausência de custo emocional ao descartar trabalho de agentes

## Ferramentas & pessoas
**Ferramentas:** Claude Sonnet 3.5, Claude Opus 4.5, Mythos/Fable (modelo), Codex, Claude, OBS, Git, tmux, GNU screen, SSH, Vim, cron, GitHub, Amazon S3, AWS RDS, Vercel, Slackbot API

**Pessoas/orgs:** Apple, Vercel, AWS, Slack, Salesforce, npm

## Claims acionáveis
- Sonnet 3.5 foi o primeiro modelo a executar tool calls de forma consistente e confiável o suficiente para coding diário em codebases reais
- Opus 4.5 foi o salto que permitiu tarefas de horas: o modelo testava o próprio trabalho e mantinha o raciocínio de ponta a ponta sem perder o contexto
- Mythos faz orquestração nativa: entende a si mesmo, spawna modelos adicionais, divide o trabalho e verifica o resultado — basta pedir via prompt, sem fábrica de software customizada
- Os modelos estão melhorando mais rápido que os desenvolvedores; a resposta não é 'melhorar' mas aumentar a ambição do que se constrói
- Práticas herdadas devem ser auditadas: perguntar 'isso é feito porque é certo ou porque sempre foi assim?' (ex.: proibição de commit de env files é limitação do Git, não boa prática)
- Sunk cost deve ser combatido: deletar código e resetar costuma ser a solução certa, e guilt-mergear PRs de agentes (ou humanos) deve cessar — trabalho de agente pode ser descartado sem culpa
- Todo tier de projeto desceu um nível: o que exigia startup agora é side project, e o novo piso é um markdown file executável via pipe para Codex ou Claude em cron
- Um markdown file em cron pode substituir um serviço: triagem e revisão de PRs em 4 repositórios GitHub, priorização, publicação de HTML estático no S3 e entrega de URL às 9h diariamente
- A estratégia largura-vs-profundidade inverteu: plataformas deep como Vercel ainda vencem seu nicho, mas o range amplo estilo AWS virou viável — uma plataforma de banco de dados pode ser embutida no produto em 1-2 dias de trabalho
- Arquitetar para extensibilidade transforma gaps de feature em não-problema: se usuários conseguem construir o que falta (como fazem com a Slackbot API), pode-se competir diretamente com incumbentes como Slack, AWS e Salesforce
- O limite do 'grande demais' ficou desconhecido (treinar modelo próprio? SO próprio?), o que exige testar propositadamente o que excede o que 'faz sentido' para descobrir os novos limites

> **Deep dive:** `medium` — Palestra de visão/mindset com insights acionáveis pontuais (orquestração via prompt, markdown como serviço, colapso de tiers, largura vs profundidade), mas sem densidade técnica em harness, evals, context-engineering ou governança que justifique tier alto.
