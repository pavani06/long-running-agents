---
title: "Agentic Engineering: Working With AI, Not Just Using It — Brendan O'Leary"
type: "extract"
source: "youtube"
video_id: "BEKc4P87XKo"
url: "https://www.youtube.com/watch?v=BEKc4P87XKo"
channel: "AI Engineer"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-agentic-engineering-working-with-ai-not-just-using-it-brendan-o-leary--BEKc4P87XKo.txt]]"
tags: ["agentic-coding", "agents", "agent-loop", "context-engineering", "context-management", "token-budgeting", "permissions", "multi-agent", "code-review", "model-selection", "knowledge-management", "memory-architecture", "verification", "process"]
thesis: "Engenharia agêntica significa deixar de usar IA como autocomplete e passar a trabalhar com agentes como colaboradores juniores rápidos e bem-lidos mas sem julgamento, dirigindo-os por meio de context engineering deliberado (persistir, selecionar, comprimir e isolar contexto) e do loop pesquisa→plano→implementação."
concepts: ["Agentic engineering: mudança de 'usar máquinas' para 'trabalhar com máquinas' (Armin Ronacher)", "Mental model do agente como junior developer entusiasmado, bem-lido e 'confiantemente errado', sem contexto de negócio", "Context engineering (Karpathy): arte e ciência de preencher a janela com apenas o necessário para o próximo passo", "Degradação de qualidade quando o contexto passa de ~50% da janela; mais contexto pode deixar o modelo 'mais burro'", "Contexto ruim envenena a saída: tarefas misturadas, comentários desatualizados e tentativas de 'corrigir a rota' reativam padrões negativos", "Quatro práticas de gestão de contexto: persistir fora da janela (scratchpads, memory files), seleção criteriosa, sumarizar/comprimir, isolar por sessão ou agente", "Loop pesquisa→plano→implementação com revisão humana em cada fase antes de codar", "Modos especializados: ask (somente pesquisa/leitura), architect (plano), code (implementação)", "Plan file: passos específicos, comandos de teste para verificação e escopo explícito dentro/fora", "Uso de modelo menor/mais barato na implementação quando o plano está claro", "agents.md como padrão de facto para regras always-on vs skills.md como playbooks sob demanda", "Handoff entre agentes: agente resume a sessão para o próximo agente (IA escrevendo prompts para IA)", "Ajuste de permissões/auto-aprovação por ferramenta e agentes paralelos com work trees", "Git local como primeira revisão do trabalho do agente antes do PR para colegas", "Custo de tokens: todo o histórico é reenviado como input; cada MCP server adiciona tokens ao system prompt"]
tools: ["Kilo Code (kilo.ai)", "GitHub Copilot", "MCP (Model Context Protocol)", "GitHub MCP", "Context7", "Postgres MCP", "Git", "GitLab", "VS Code", "Balsamiq", "Flask", "OpenClaw", "Kilo Claw", "path.lo.ai", "Slack"]
people: ["Armin Ronacher (criador do Flask)", "Andrej Karpathy", "Dex Horthy", "Kilo Code", "GitLab", "GitHub"]
claims: ["Qualidade do modelo degrada quando o contexto passa de ~50% da janela; mais contexto não é melhor e custa mais porque todo o histórico é reenviado como input a cada interação", "Desabilite MCP servers não usados (ex.: Postgres MCP em trabalho de front-end): eles desperdiçam tokens e podem confundir o agente", "Quando a sessão sair dos trilhos, inicie nova sessão e peça ao agente para sumarizar o estado para o próximo agente — IA é ótima escrevendo prompts para IA", "Adote o loop pesquisa→plano→implementação: primeiro entenda o sistema (ask mode), depois gere plano com escopo e testes (architect), só então implemente (code mode)", "Um plan file detalhado com comandos de verificação permite usar modelos menores/mais baratos na fase de implementação", "Mantenha agents.md mínimo e always-on (convenções, comandos de build/teste, requisitos de commit) e skills.md para workflows reutilizáveis sob demanda", "Use git local como sua primeira revisão do trabalho do agente, commitando frequentemente antes de abrir PR para colegas", "Para APIs internas de plataforma: use spec OpenAPI/Swagger existente, converta para markdown no repositório, use URL de referência para docs voláteis, ou construa um MCP server próprio para fluxos multi-sistema", "Configure e revise com o tempo as permissões de auto-aprovação do agente (leitura de arquivos dentro/fora do workspace, execução de testes, uso de work trees, agentes paralelos)", "Armin Ronacher reportou ganhar ~30% do dia por saber o que delegar e o que manter — dirigir o trabalho é a diferença entre usar IA e trabalhar com IA", "Uma linha ruim de pesquisa pode custar centenas de linhas de código ruim (Dex Horthy); IA não substitui pensamento, apenas amplifica o pensamento feito ou a falta dele", "Faça uma tarefa por sessão, monitore o 'context meter' e desconfie quando parecer que algo está errado", "O tempo humano nas fases de pesquisa e planejamento é o uso de maior alavancagem; a implementação deve acontecer com o raciocínio duro já feito"]
deep_dive: "medium"
deep_dive_reason: "Densidade razoável de conselhos acionáveis sobre context-engineering e o loop pesquisa→plano→implementação, mas em grande parte consolida boas práticas já difundidas (com trecho promocional do Kilo Code) sem novidade arquitetural ou profundidade em evals/governança."
---

# Agentic Engineering: Working With AI, Not Just Using It — Brendan O'Leary

## Tese
Engenharia agêntica significa deixar de usar IA como autocomplete e passar a trabalhar com agentes como colaboradores juniores rápidos e bem-lidos mas sem julgamento, dirigindo-os por meio de context engineering deliberado (persistir, selecionar, comprimir e isolar contexto) e do loop pesquisa→plano→implementação.

## Conceitos-chave
- Agentic engineering: mudança de 'usar máquinas' para 'trabalhar com máquinas' (Armin Ronacher)
- Mental model do agente como junior developer entusiasmado, bem-lido e 'confiantemente errado', sem contexto de negócio
- Context engineering (Karpathy): arte e ciência de preencher a janela com apenas o necessário para o próximo passo
- Degradação de qualidade quando o contexto passa de ~50% da janela; mais contexto pode deixar o modelo 'mais burro'
- Contexto ruim envenena a saída: tarefas misturadas, comentários desatualizados e tentativas de 'corrigir a rota' reativam padrões negativos
- Quatro práticas de gestão de contexto: persistir fora da janela (scratchpads, memory files), seleção criteriosa, sumarizar/comprimir, isolar por sessão ou agente
- Loop pesquisa→plano→implementação com revisão humana em cada fase antes de codar
- Modos especializados: ask (somente pesquisa/leitura), architect (plano), code (implementação)
- Plan file: passos específicos, comandos de teste para verificação e escopo explícito dentro/fora
- Uso de modelo menor/mais barato na implementação quando o plano está claro
- agents.md como padrão de facto para regras always-on vs skills.md como playbooks sob demanda
- Handoff entre agentes: agente resume a sessão para o próximo agente (IA escrevendo prompts para IA)
- Ajuste de permissões/auto-aprovação por ferramenta e agentes paralelos com work trees
- Git local como primeira revisão do trabalho do agente antes do PR para colegas
- Custo de tokens: todo o histórico é reenviado como input; cada MCP server adiciona tokens ao system prompt

## Ferramentas & pessoas
**Ferramentas:** Kilo Code (kilo.ai), GitHub Copilot, MCP (Model Context Protocol), GitHub MCP, Context7, Postgres MCP, Git, GitLab, VS Code, Balsamiq, Flask, OpenClaw, Kilo Claw, path.lo.ai, Slack

**Pessoas/orgs:** Armin Ronacher (criador do Flask), Andrej Karpathy, Dex Horthy, Kilo Code, GitLab, GitHub

## Claims acionáveis
- Qualidade do modelo degrada quando o contexto passa de ~50% da janela; mais contexto não é melhor e custa mais porque todo o histórico é reenviado como input a cada interação
- Desabilite MCP servers não usados (ex.: Postgres MCP em trabalho de front-end): eles desperdiçam tokens e podem confundir o agente
- Quando a sessão sair dos trilhos, inicie nova sessão e peça ao agente para sumarizar o estado para o próximo agente — IA é ótima escrevendo prompts para IA
- Adote o loop pesquisa→plano→implementação: primeiro entenda o sistema (ask mode), depois gere plano com escopo e testes (architect), só então implemente (code mode)
- Um plan file detalhado com comandos de verificação permite usar modelos menores/mais baratos na fase de implementação
- Mantenha agents.md mínimo e always-on (convenções, comandos de build/teste, requisitos de commit) e skills.md para workflows reutilizáveis sob demanda
- Use git local como sua primeira revisão do trabalho do agente, commitando frequentemente antes de abrir PR para colegas
- Para APIs internas de plataforma: use spec OpenAPI/Swagger existente, converta para markdown no repositório, use URL de referência para docs voláteis, ou construa um MCP server próprio para fluxos multi-sistema
- Configure e revise com o tempo as permissões de auto-aprovação do agente (leitura de arquivos dentro/fora do workspace, execução de testes, uso de work trees, agentes paralelos)
- Armin Ronacher reportou ganhar ~30% do dia por saber o que delegar e o que manter — dirigir o trabalho é a diferença entre usar IA e trabalhar com IA
- Uma linha ruim de pesquisa pode custar centenas de linhas de código ruim (Dex Horthy); IA não substitui pensamento, apenas amplifica o pensamento feito ou a falta dele
- Faça uma tarefa por sessão, monitore o 'context meter' e desconfie quando parecer que algo está errado
- O tempo humano nas fases de pesquisa e planejamento é o uso de maior alavancagem; a implementação deve acontecer com o raciocínio duro já feito

> **Deep dive:** `medium` — Densidade razoável de conselhos acionáveis sobre context-engineering e o loop pesquisa→plano→implementação, mas em grande parte consolida boas práticas já difundidas (com trecho promocional do Kilo Code) sem novidade arquitetural ou profundidade em evals/governança.
