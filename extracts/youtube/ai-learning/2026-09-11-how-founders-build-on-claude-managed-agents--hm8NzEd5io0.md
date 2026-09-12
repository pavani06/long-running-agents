---
title: "How founders build on Claude Managed Agents"
type: "extract"
source: "youtube"
video_id: "hm8NzEd5io0"
url: "https://www.youtube.com/watch?v=hm8NzEd5io0"
channel: "Claude"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-how-founders-build-on-claude-managed-agents--hm8NzEd5io0.txt]]"
tags: ["harness", "agent-fleets", "agent-loop", "multi-agent", "memory-architecture", "evals", "verification", "model-selection", "decision-discipline", "token-budgeting", "observability", "state", "permissions", "agent-tooling", "monitoramento", "cross-session", "error-handling", "production"]
thesis: "Três startups usam o Claude Managed Agents da Anthropic para enviar recursos de agentes em produção (briefs de reunião com verificação de outcomes, frota de agentes de vendas com memória cross-account, analytics que introspecta codebase em sandbox) em semanas, reservando harness próprio apenas para quando infraestrutura é competência central ou quando custo/UX exigem controle fino."
concepts: ["Outcomes como rubrica iterativa com verificador independente em janela de contexto limpa", "Princípio de abstenção: não mostrar informação em vez de mostrar falso positivo", "Memória em duas dimensões (conta vs cross-conta, usuário vs organização)", "Watchtower: agregação cross-account com escrita de código, tool calling programático e fan-out para agentes por conta", "Aprendizado de conceitos organizacionais a partir de dados sujos via perguntas de clarificação persistidas em memória org-wide", "Build vs buy de harness baseado em competência central e velocidade de aprendizado", "Evals: fase vibes-based antes de stickiness; risco de overfit e de distribuição fora da real do usuário", "Limitação de evals para sistemas stateful com memória viva e chamadas MCP a serviços mutáveis", "Migração de modelos: evitar hiperotimização de prompts a uma família; mitigar novos modos de falha específicos", "Otimização de custo via modelos mais baratos no fan-out e coordenador com modelo frontier", "Sandboxes para acesso seguro a código-fonte com geração de PRs e processos batch noturnos (cron)", "Sonho/'dreaming' de memória: agente supervisor agregando memórias da frota de agentes", "Telemetria fina de atribuição de custo por chamada no harness"]
tools: ["Claude Managed Agents", "Anthropic Claude", "Claude Code", "Opus", "Watchtower", "Salesforce", "LinkedIn", "Slack MCP"]
people: ["Sahaj", "Mihir", "Todd", "Anthropic"]
claims: ["Use um agente verificador independente com janela de contexto limpa, desacoplado do trace de execução, para avaliar o resultado do agente antes de exibi-lo ao usuário", "Transforme critérios de UX (fonte correta, escaneabilidade, ordem quem-porquê-o quê) em rubrica e faça hill-climb contra ela em runtime", "Execute geração e verificação até 24h antes do evento para dar janela longa de iteração e abstenção segura", "Escolha não mostrar informação incorreta em vez de arriscar falso positivo — ajuda quando pode, sem causar dano", "Estruture memória como two-by-two (conta/cross-conta × usuário/org) e mantenha sob controle próprio apenas a parte diferenciadora (memória por conta), delegando o resto à memória gerenciada", "Aprenda conceitos organizacionais perguntando clarificações ao usuário na primeira consulta e persistindo em memória org-wide, evitando configuração inicial", "Para consultas complexas sobre dezenas/centenas de contas: filtre candidatos, escreva código, faça fan-out para agentes independentes por conta e consolide o roll-up", "Compre harness gerenciado quando não for competência central do produto; construa o próprio quando o harness for o produto (ex: assistente de voz contínuo) ou quando controle de custo/UX for habilitador de feature", "Valide stickiness de forma vibes-based primeiro; evals não tornam produto sticky e curar eval set fora da distribuição real do usuário leva a hill-climb inútil", "Construa evals a partir de queries reais de clientes entrevistados para reduzir risco de abstração", "Evals offline para sistemas com estado externo mutável (memória viva, Slack MCP) permanecem problema não resolvido; trajectory evals são o fallback parcial", "Ao migrar modelo, priorize hedging contra modos de falha novos e específicos (ex: tells de escrita de IA, em-dashes) em vez de extrair os últimos 1% via prompt tuning", "Use modelo frontier só no agente coordenador e modelos baratos no fan-out massivo; modo batch/flex poderia cortar 50–75% em workloads agendados com antecedência", "Sandbox todo acesso a código-fonte de clientes: controle ferramentas expostas, dados enviados e ações, com PR como artefato final", "Rode detecção de drift analítico (funil, conversão) em processos batch noturnos via cron, não em tempo real", "Alinhe as rubrics de evals offline com as de outcomes em produção para consistência"]
deep_dive: "high"
deep_dive_reason: "Alta densidade de padrões arquiteturais acionáveis e novos (verificador independente com contexto limpo em outcomes, memória em two-by-two com dreaming cross-frota, fan-out programático, sandboxing de codebase, critérios de build-vs-buy e limites de evals stateful) diretamente relevantes a harness, evals, agent-fleets e governança, apesar do viés promocional do formato roundtable."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-how-to-get-to-production-faster-with-claude-managed-agents--zenIB7XLZxQ|How to get to production faster with Claude Managed Agents]]", "[[extracts/youtube/ai-learning/2026-09-11-how-the-claude-code-team-uses-claude-code--S-sYlFiGFv8|How the Claude Code team uses Claude Code]]", "[[extracts/youtube/ai-learning/2026-09-11-building-with-claude-managed-agents-and-asana-ai-teammates--BrpB-h1e--k|Building with Claude Managed Agents and Asana AI teammates]]", "[[extracts/youtube/ai-learning/2026-09-11-ship-your-first-managed-agent--19HDQ9HppOA|Ship your first Managed Agent]]", "[[extracts/youtube/ai-learning/2026-09-11-loop-engineering-to-graph-engineering--BOOfy3Yshtw|Loop Engineering to Graph Engineering]]", "[[extracts/youtube/ai-learning/2026-09-11-anthropic-s-applied-ai-team-on-the-evolution-of-agentic-surfaces--K0X9QDRkIdg|Anthropic's Applied AI team on the Evolution of Agentic Surfaces]]", "[[extracts/youtube/ai-learning/2026-09-11-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipeline--Uny6LpmjraI|Inside Clay's Eval Stack: 300M Agent Runs, One LangSmith Pipeline]]", "[[extracts/youtube/ai-learning/2026-09-11-build-a-proactive-agent-workflow-with-claude-code--eSP7PLTXNy8|Build a proactive agent workflow with Claude Code]]", "[[extracts/youtube/ai-learning/2026-09-11-how-uber-runs-60-000-ai-agent-tasks-per-week-with-mcp--yVqMxBahjfA|How Uber Runs 60,000 AI Agent Tasks Per Week With MCP]]", "[[extracts/youtube/ai-learning/2026-09-11-getting-started-with-omnigent-the-coding-agent-meta-harness--AyV0hum_hA8|Getting Started with Omnigent | The Coding Agent Meta-Harness]]"]
theme: "Codificação Agêntica com Claude Code"
---

# How founders build on Claude Managed Agents

## Tese
Três startups usam o Claude Managed Agents da Anthropic para enviar recursos de agentes em produção (briefs de reunião com verificação de outcomes, frota de agentes de vendas com memória cross-account, analytics que introspecta codebase em sandbox) em semanas, reservando harness próprio apenas para quando infraestrutura é competência central ou quando custo/UX exigem controle fino.

## Conceitos-chave
- Outcomes como rubrica iterativa com verificador independente em janela de contexto limpa
- Princípio de abstenção: não mostrar informação em vez de mostrar falso positivo
- Memória em duas dimensões (conta vs cross-conta, usuário vs organização)
- Watchtower: agregação cross-account com escrita de código, tool calling programático e fan-out para agentes por conta
- Aprendizado de conceitos organizacionais a partir de dados sujos via perguntas de clarificação persistidas em memória org-wide
- Build vs buy de harness baseado em competência central e velocidade de aprendizado
- Evals: fase vibes-based antes de stickiness; risco de overfit e de distribuição fora da real do usuário
- Limitação de evals para sistemas stateful com memória viva e chamadas MCP a serviços mutáveis
- Migração de modelos: evitar hiperotimização de prompts a uma família; mitigar novos modos de falha específicos
- Otimização de custo via modelos mais baratos no fan-out e coordenador com modelo frontier
- Sandboxes para acesso seguro a código-fonte com geração de PRs e processos batch noturnos (cron)
- Sonho/'dreaming' de memória: agente supervisor agregando memórias da frota de agentes
- Telemetria fina de atribuição de custo por chamada no harness

## Ferramentas & pessoas
**Ferramentas:** Claude Managed Agents, Anthropic Claude, Claude Code, Opus, Watchtower, Salesforce, LinkedIn, Slack MCP

**Pessoas/orgs:** Sahaj, Mihir, Todd, Anthropic

## Claims acionáveis
- Use um agente verificador independente com janela de contexto limpa, desacoplado do trace de execução, para avaliar o resultado do agente antes de exibi-lo ao usuário
- Transforme critérios de UX (fonte correta, escaneabilidade, ordem quem-porquê-o quê) em rubrica e faça hill-climb contra ela em runtime
- Execute geração e verificação até 24h antes do evento para dar janela longa de iteração e abstenção segura
- Escolha não mostrar informação incorreta em vez de arriscar falso positivo — ajuda quando pode, sem causar dano
- Estruture memória como two-by-two (conta/cross-conta × usuário/org) e mantenha sob controle próprio apenas a parte diferenciadora (memória por conta), delegando o resto à memória gerenciada
- Aprenda conceitos organizacionais perguntando clarificações ao usuário na primeira consulta e persistindo em memória org-wide, evitando configuração inicial
- Para consultas complexas sobre dezenas/centenas de contas: filtre candidatos, escreva código, faça fan-out para agentes independentes por conta e consolide o roll-up
- Compre harness gerenciado quando não for competência central do produto; construa o próprio quando o harness for o produto (ex: assistente de voz contínuo) ou quando controle de custo/UX for habilitador de feature
- Valide stickiness de forma vibes-based primeiro; evals não tornam produto sticky e curar eval set fora da distribuição real do usuário leva a hill-climb inútil
- Construa evals a partir de queries reais de clientes entrevistados para reduzir risco de abstração
- Evals offline para sistemas com estado externo mutável (memória viva, Slack MCP) permanecem problema não resolvido; trajectory evals são o fallback parcial
- Ao migrar modelo, priorize hedging contra modos de falha novos e específicos (ex: tells de escrita de IA, em-dashes) em vez de extrair os últimos 1% via prompt tuning
- Use modelo frontier só no agente coordenador e modelos baratos no fan-out massivo; modo batch/flex poderia cortar 50–75% em workloads agendados com antecedência
- Sandbox todo acesso a código-fonte de clientes: controle ferramentas expostas, dados enviados e ações, com PR como artefato final
- Rode detecção de drift analítico (funil, conversão) em processos batch noturnos via cron, não em tempo real
- Alinhe as rubrics de evals offline com as de outcomes em produção para consistência

> **Deep dive:** `high` — Alta densidade de padrões arquiteturais acionáveis e novos (verificador independente com contexto limpo em outcomes, memória em two-by-two com dreaming cross-frota, fan-out programático, sandboxing de codebase, critérios de build-vs-buy e limites de evals stateful) diretamente relevantes a harness, evals, agent-fleets e governança, apesar do viés promocional do formato roundtable.
