---
title: "L8 Principal's Agentic Engineering Setup (just copy him)"
type: "extract"
source: "youtube"
video_id: "8ZgpAXe5V5w"
url: "https://www.youtube.com/watch?v=8ZgpAXe5V5w"
channel: "David Ondrej"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-l8-principal-s-agentic-engineering-setup-just-copy-him--8ZgpAXe5V5w.txt]]"
tags: ["agent-fleets", "agents", "agentic-coding", "agent-tooling", "agentes-orquestracao", "multi-agent", "harness", "harness-engineering", "code-review", "verification", "testes-qa", "escalation", "gate-design", "decision-discipline", "model-selection", "token-budgeting", "evals", "context-engineering", "stack-tooling", "runtime", "cross-session", "telemetry", "process"]
thesis: "Um ex-engenheiro de Meta/Microsoft/Atlassian opera uma frota de agentes por meio de um coordenador ('first mate') que roteia modelos, delega tarefas e só escala ao humano decisões ambíguas, com um pipeline adversarial de verificação ('no mistakes') tornando a revisão de código gerado por IA escalável."
concepts: ["Orquestração first mate/crewmates (agente coordenador que gerencia todas as sessões paralelas)", "Regras de roteamento por agente/modelo/reasoning effort escritas em arquivo editável", "Escalonamento ao humano apenas em decisões ambíguas ou com implicação de produto (gate design)", "Encapsular passos determinísticos em scripts bash para economizar tokens", "Software auto-modificável: agente edita seu próprio agents.md e scripts para contornar bugs", "Pipeline de validação 'no mistakes': extração de intenção da sessão do agente, rebase, revisão adversarial, autofix vs escalonamento, testes, documentação, PR e babysitting de CI", "Extração de intent do transcript da sessão que gerou a mudança como requisitos verdadeiros", "Curva inteligência vs custo: modelos menos inteligentes com reasoning alto desperdiçam ciclos", "Ultra não é nível de raciocínio, mas prompt que faz fan-out agressivo de subagentes", "Modo 'brain dump': humano despeja pensamentos e o coordenador resolve o resto", "Multiplexador de terminal que entende estado de agentes (working/waiting)", "Sessão de terminal remota e persistente acessível via SSH do celular", "Software self-modifying e self-healing (bug report -> fix -> PR -> review sem humano)", "Orçamento de quota como gargalo e demanda por modo lento-barato para tarefas em background", "Artefatos HTML interativos (whiteboard) para revisão colaborativa de design e trade-offs", "Confiança progressiva: delegação construída por observação e otimização de roteamento"]
tools: ["Westermy", "Herder", "tmux", "Zellij", "Emacs", "Mac Mini", "SSH", "First Mate", "No Mistakes", "Baby Menu", "Lavish", "Excalidraw", "Claude Code", "Codex CLI", "Codex app", "Cursor", "GitHub Copilot", "Pi (harness)", "OpenCode", "Grok CLI", "Grok 4.5", "GPT-5.6 (Soul/Luna/Terra)", "Claude Fable", "Claude Sonnet 5", "GPT-3.5", "GPT-4", "Sonnet 3.5 v2", "DeepU benchmark", "CodeRabbit", "Home Assistant", "X API", "OpenRouter", "Kimi K2.7 Code", "Treehouse (projeto)", "HighBit (harness para crianças)", "GitHub", "GitLab"]
people: ["Kun", "David", "Meta", "Microsoft", "Atlassian", "Anthropic", "OpenAI", "Mark Zuckerberg", "xAI/Grok"]
claims: ["Mova passos determinísticos do fluxo do agente para scripts bash no diretório de trabalho: economiza tokens e permite que o agente os modifique para contornar bugs, tornando o sistema praticamente instoppável", "Extraia a intenção original do transcript da sessão de agente que produziu a mudança e use como requisitos de referência na revisão de código", "Defina regras explícitas de escalonamento: autofix para bugs óbvios, escalonamento ao humano quando a correção muda comportamento de produto", "Mantenha o agente coordenador livre: ele deve delegar verificações a crewmates para nunca bloquear o canal de conversa com o humano", "Roteie por tarefa: GPT-5.6 Soul xhigh como coordenador, Fable para design complexo, Luna apenas quando latência importa (ex.: home assistant)", "Evite 'ultra': é um prompt que dispara fan-out de subagentes (cada um ultra) e queima quota rapidamente; prefira Soul com reasoning ajustável a Terra", "Modelos menos inteligentes com reasoning máximo desperdiçam ciclos (Sonnet 5 max fica mais caro que Fable no benchmark); ajuste reasoning à inteligência do modelo", "Concentre o tempo humano apenas em decisões ambíguas e em modo brain dump no coordenador; delegue todo o resto", "Aplique pipeline pesado de validação somente em código de produção; pule em demos e mudezas triviais com julgamento manual", "Revise com GPT desde a 5.5: é o melhor detector de edge cases raros; documentação desatualizada é o segundo maior capturador (63% de ~1000 mudanças em 59 repos continham erros)", "Escolha harness por ecossistema: Claude Code para Anthropic, Pi para GPT (customizável via plugins), Grock CLI dá acesso grátis à X API", "Use artefatos HTML interativos (Lavish/Excalidraw) para visualizar hierarquias, trade-offs e pontos de decisão em revisões de design", "Trackeie estatísticas do pipeline (mudanças, erros por etapa, repos) como telemetry para calibrar qualidade e custo", "Existe demanda de mercado por tiers acima de US$ 200 e por um modo lento e barato para tarefas em background; API pricing é inviável para indivíduos (>US$ 10k/mês)", "Softwares devem enviar experiência razoável out-of-box e permitir auto-modificação via conversa com agentes, incluindo loops self-healing de bug a PR sem intervenção humana"]
deep_dive: "high"
deep_dive_reason: "Densidade alta de padrões arquiteturais acionáveis e novados (coordenador first mate, gates de escalonamento, pipeline adversarial com extração de intent, scripts auto-modificáveis, roteamento por reasoning effort) diretamente relevantes a harness, agent-fleets e verification."
---

# L8 Principal's Agentic Engineering Setup (just copy him)

## Tese
Um ex-engenheiro de Meta/Microsoft/Atlassian opera uma frota de agentes por meio de um coordenador ('first mate') que roteia modelos, delega tarefas e só escala ao humano decisões ambíguas, com um pipeline adversarial de verificação ('no mistakes') tornando a revisão de código gerado por IA escalável.

## Conceitos-chave
- Orquestração first mate/crewmates (agente coordenador que gerencia todas as sessões paralelas)
- Regras de roteamento por agente/modelo/reasoning effort escritas em arquivo editável
- Escalonamento ao humano apenas em decisões ambíguas ou com implicação de produto (gate design)
- Encapsular passos determinísticos em scripts bash para economizar tokens
- Software auto-modificável: agente edita seu próprio agents.md e scripts para contornar bugs
- Pipeline de validação 'no mistakes': extração de intenção da sessão do agente, rebase, revisão adversarial, autofix vs escalonamento, testes, documentação, PR e babysitting de CI
- Extração de intent do transcript da sessão que gerou a mudança como requisitos verdadeiros
- Curva inteligência vs custo: modelos menos inteligentes com reasoning alto desperdiçam ciclos
- Ultra não é nível de raciocínio, mas prompt que faz fan-out agressivo de subagentes
- Modo 'brain dump': humano despeja pensamentos e o coordenador resolve o resto
- Multiplexador de terminal que entende estado de agentes (working/waiting)
- Sessão de terminal remota e persistente acessível via SSH do celular
- Software self-modifying e self-healing (bug report -> fix -> PR -> review sem humano)
- Orçamento de quota como gargalo e demanda por modo lento-barato para tarefas em background
- Artefatos HTML interativos (whiteboard) para revisão colaborativa de design e trade-offs
- Confiança progressiva: delegação construída por observação e otimização de roteamento

## Ferramentas & pessoas
**Ferramentas:** Westermy, Herder, tmux, Zellij, Emacs, Mac Mini, SSH, First Mate, No Mistakes, Baby Menu, Lavish, Excalidraw, Claude Code, Codex CLI, Codex app, Cursor, GitHub Copilot, Pi (harness), OpenCode, Grok CLI, Grok 4.5, GPT-5.6 (Soul/Luna/Terra), Claude Fable, Claude Sonnet 5, GPT-3.5, GPT-4, Sonnet 3.5 v2, DeepU benchmark, CodeRabbit, Home Assistant, X API, OpenRouter, Kimi K2.7 Code, Treehouse (projeto), HighBit (harness para crianças), GitHub, GitLab

**Pessoas/orgs:** Kun, David, Meta, Microsoft, Atlassian, Anthropic, OpenAI, Mark Zuckerberg, xAI/Grok

## Claims acionáveis
- Mova passos determinísticos do fluxo do agente para scripts bash no diretório de trabalho: economiza tokens e permite que o agente os modifique para contornar bugs, tornando o sistema praticamente instoppável
- Extraia a intenção original do transcript da sessão de agente que produziu a mudança e use como requisitos de referência na revisão de código
- Defina regras explícitas de escalonamento: autofix para bugs óbvios, escalonamento ao humano quando a correção muda comportamento de produto
- Mantenha o agente coordenador livre: ele deve delegar verificações a crewmates para nunca bloquear o canal de conversa com o humano
- Roteie por tarefa: GPT-5.6 Soul xhigh como coordenador, Fable para design complexo, Luna apenas quando latência importa (ex.: home assistant)
- Evite 'ultra': é um prompt que dispara fan-out de subagentes (cada um ultra) e queima quota rapidamente; prefira Soul com reasoning ajustável a Terra
- Modelos menos inteligentes com reasoning máximo desperdiçam ciclos (Sonnet 5 max fica mais caro que Fable no benchmark); ajuste reasoning à inteligência do modelo
- Concentre o tempo humano apenas em decisões ambíguas e em modo brain dump no coordenador; delegue todo o resto
- Aplique pipeline pesado de validação somente em código de produção; pule em demos e mudezas triviais com julgamento manual
- Revise com GPT desde a 5.5: é o melhor detector de edge cases raros; documentação desatualizada é o segundo maior capturador (63% de ~1000 mudanças em 59 repos continham erros)
- Escolha harness por ecossistema: Claude Code para Anthropic, Pi para GPT (customizável via plugins), Grock CLI dá acesso grátis à X API
- Use artefatos HTML interativos (Lavish/Excalidraw) para visualizar hierarquias, trade-offs e pontos de decisão em revisões de design
- Trackeie estatísticas do pipeline (mudanças, erros por etapa, repos) como telemetry para calibrar qualidade e custo
- Existe demanda de mercado por tiers acima de US$ 200 e por um modo lento e barato para tarefas em background; API pricing é inviável para indivíduos (>US$ 10k/mês)
- Softwares devem enviar experiência razoável out-of-box e permitir auto-modificação via conversa com agentes, incluindo loops self-healing de bug a PR sem intervenção humana

> **Deep dive:** `high` — Densidade alta de padrões arquiteturais acionáveis e novados (coordenador first mate, gates de escalonamento, pipeline adversarial com extração de intent, scripts auto-modificáveis, roteamento por reasoning effort) diretamente relevantes a harness, agent-fleets e verification.
