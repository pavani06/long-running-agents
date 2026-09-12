---
title: "How the Claude Code team uses Claude Code"
type: "extract"
source: "youtube"
video_id: "S-sYlFiGFv8"
url: "https://www.youtube.com/watch?v=S-sYlFiGFv8"
channel: "Claude"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-how-the-claude-code-team-uses-claude-code--S-sYlFiGFv8.txt]]"
tags: ["harness", "harness-engineering", "agent-loop", "agentic-coding", "agents", "multi-agent", "code-review", "shadow-review", "verification", "testes-qa", "memory-architecture", "cross-session", "monitoramento", "observability", "telemetry", "process", "production"]
thesis: "A equipe do Claude Code descreve a evolução de um ano do trabalho de supervisionar transcripts e chamadas de ferramenta para delegar objetivos a agentes Slack-nativos (Claude Tag), tratando recursos do harness como scaffolding temporário para falhas do modelo atual e adotando workflows onde o próprio agente escreve código determinístico para orquestrar sub-agentes em fan-out, com verificação e feedback como primitivas centrais."
concepts: ["delegação em nível de objetivo vs. supervisão de transcript", "harness como scaffolding temporário para modos de falha do modelo", "compressão do shelf-life da tecnologia (anos para ~2 meses)", "todo-lists como scaffolding de longo-horizonte ultrapassado por memory states", "ferramenta ask-user evoluindo para artifacts interativos", "quebra da fronteira de sessão (prompt um nível acima da sessão)", "loops e rotinas em containers hospedados", "fan-out + revisão adversarial multi-perspectiva como test-time compute", "filtragem estilo MapReduce da saída do fan-out para consumo humano", "mistura de código determinístico e comportamento agentic na orquestração", "desacoplamento da UI do transcript (monólogo interno invisível)", "primitivas de verificação, code review e feedback", "self-hosting: Claude Tag construindo Claude Tag", "instrumentação com eventos para monitoramento e melhoria de funil"]
tools: ["Claude Code", "Claude Tag", "Slack", "TUI", "desktop app", "Claude Code on the web (containers hospedados)", "remote hosted developer boxes", "artifacts (HTML com diagramas/mockups)", "code review bot", "GitHub issues", "Sonnet 3.5", "PowerPoint"]
people: ["Boris", "Sid", "Robert", "equipe Claude Code / Anthropic"]
claims: ["Trate recursos do harness como cobertura temporária para modos de falha do modelo atual e esteja pronto para removê-los quando os modelos melhorarem (ex.: todo-lists deixaram de ser necessários).", "Comprime-se o shelf-life: a tecnologia muda por baixo do produto a cada ~2 meses, então equilibre construir na fronteira com entregar valor para usuários atuais.", "Delegue em nível de objetivo em vez de supervisionar cada tool call: 70-80% do trabalho da equipe agora flui pelo agente Slack-nativo, com TUI apenas para refinamento.", "Deixe o agente resolver nitpicks de code review autonomamente e redirecione revisores humanos para contexto arquitetural (estrutura de APIs, fronteiras de serviço) que o agente não internalizou.", "Para achar bugs, faça fan-out massivo seguido de revisão adversarial de cada bug sob três perspectivas/opiniões para filtrar falsos positivos antes de escalar ao humano.", "Saídas de fan-out devem ser coalescidas/filtradas de volta (estilo MapReduce) para consumo humano; confiança se constrói jogando test-time compute no problema.", "Prefira workflows onde o agente escreve código determinístico (ex.: for loops) para orquestrar sub-agentes: garantia de aplicação uniforme aumenta a confiança versus comportamento puramente LLM.", "Claude é bom em criar os próprios harnesses: determina topologia do fan-out, encadeia saídas entre níveis de agentes e resume o resultado final.", "Mova o agente do laptop local para boxes hospedados e depois para containers na nuvem para habilitar loops e rotinas contínuas (ex.: diariamente triar feedback em buckets de importância e corrigir os de alta confiança).", "Desacoplar a UI do transcript (mensagens via tool, monólogo interno oculto com link para o transcript completo) é libertador e força a 'deixar o Claude cozinhar', validando que os modelos já suportam supervisão mínima.", "Instrumente ferramentas internas com eventos/telemetria para que o agente monitore uso, notifique sobre feedback e proponha melhorias de funil em nível superior.", "Use primitivas de verificação em PRs gerados por agentes: testes automáticos e screenshots do resultado para construir confiança sem abrir o ambiente.", "Garanta que o dev loop e o ambiente de desenvolvimento sejam triviais para o próprio agente usar, especialmente em software complexo e integrado (o produto construindo a si mesmo).", "Substitua interações ad hoc (ferramenta ask-user pós-planejamento) por artifacts interativos que fazem perguntas com diagramas e mockups.", "À medida que o escopo das tarefas cresce, as ferramentas que o modelo precisa para se manter coerente mudam de forma — redesenhe o toolkit por nível de tarefa."]
deep_dive: "high"
deep_dive_reason: "Densidade alta de insight acionável e arquitetural direto de quem constrói o harness (scaffolding temporário, fan-out adversarial, orquestração determinística por código do agente, desacoplamento UI/transcript, loops em rotinas), com novidade e relevância direta a harness-engineering, verification e agent-fleets."
---

# How the Claude Code team uses Claude Code

## Tese
A equipe do Claude Code descreve a evolução de um ano do trabalho de supervisionar transcripts e chamadas de ferramenta para delegar objetivos a agentes Slack-nativos (Claude Tag), tratando recursos do harness como scaffolding temporário para falhas do modelo atual e adotando workflows onde o próprio agente escreve código determinístico para orquestrar sub-agentes em fan-out, com verificação e feedback como primitivas centrais.

## Conceitos-chave
- delegação em nível de objetivo vs. supervisão de transcript
- harness como scaffolding temporário para modos de falha do modelo
- compressão do shelf-life da tecnologia (anos para ~2 meses)
- todo-lists como scaffolding de longo-horizonte ultrapassado por memory states
- ferramenta ask-user evoluindo para artifacts interativos
- quebra da fronteira de sessão (prompt um nível acima da sessão)
- loops e rotinas em containers hospedados
- fan-out + revisão adversarial multi-perspectiva como test-time compute
- filtragem estilo MapReduce da saída do fan-out para consumo humano
- mistura de código determinístico e comportamento agentic na orquestração
- desacoplamento da UI do transcript (monólogo interno invisível)
- primitivas de verificação, code review e feedback
- self-hosting: Claude Tag construindo Claude Tag
- instrumentação com eventos para monitoramento e melhoria de funil

## Ferramentas & pessoas
**Ferramentas:** Claude Code, Claude Tag, Slack, TUI, desktop app, Claude Code on the web (containers hospedados), remote hosted developer boxes, artifacts (HTML com diagramas/mockups), code review bot, GitHub issues, Sonnet 3.5, PowerPoint

**Pessoas/orgs:** Boris, Sid, Robert, equipe Claude Code / Anthropic

## Claims acionáveis
- Trate recursos do harness como cobertura temporária para modos de falha do modelo atual e esteja pronto para removê-los quando os modelos melhorarem (ex.: todo-lists deixaram de ser necessários).
- Comprime-se o shelf-life: a tecnologia muda por baixo do produto a cada ~2 meses, então equilibre construir na fronteira com entregar valor para usuários atuais.
- Delegue em nível de objetivo em vez de supervisionar cada tool call: 70-80% do trabalho da equipe agora flui pelo agente Slack-nativo, com TUI apenas para refinamento.
- Deixe o agente resolver nitpicks de code review autonomamente e redirecione revisores humanos para contexto arquitetural (estrutura de APIs, fronteiras de serviço) que o agente não internalizou.
- Para achar bugs, faça fan-out massivo seguido de revisão adversarial de cada bug sob três perspectivas/opiniões para filtrar falsos positivos antes de escalar ao humano.
- Saídas de fan-out devem ser coalescidas/filtradas de volta (estilo MapReduce) para consumo humano; confiança se constrói jogando test-time compute no problema.
- Prefira workflows onde o agente escreve código determinístico (ex.: for loops) para orquestrar sub-agentes: garantia de aplicação uniforme aumenta a confiança versus comportamento puramente LLM.
- Claude é bom em criar os próprios harnesses: determina topologia do fan-out, encadeia saídas entre níveis de agentes e resume o resultado final.
- Mova o agente do laptop local para boxes hospedados e depois para containers na nuvem para habilitar loops e rotinas contínuas (ex.: diariamente triar feedback em buckets de importância e corrigir os de alta confiança).
- Desacoplar a UI do transcript (mensagens via tool, monólogo interno oculto com link para o transcript completo) é libertador e força a 'deixar o Claude cozinhar', validando que os modelos já suportam supervisão mínima.
- Instrumente ferramentas internas com eventos/telemetria para que o agente monitore uso, notifique sobre feedback e proponha melhorias de funil em nível superior.
- Use primitivas de verificação em PRs gerados por agentes: testes automáticos e screenshots do resultado para construir confiança sem abrir o ambiente.
- Garanta que o dev loop e o ambiente de desenvolvimento sejam triviais para o próprio agente usar, especialmente em software complexo e integrado (o produto construindo a si mesmo).
- Substitua interações ad hoc (ferramenta ask-user pós-planejamento) por artifacts interativos que fazem perguntas com diagramas e mockups.
- À medida que o escopo das tarefas cresce, as ferramentas que o modelo precisa para se manter coerente mudam de forma — redesenhe o toolkit por nível de tarefa.

> **Deep dive:** `high` — Densidade alta de insight acionável e arquitetural direto de quem constrói o harness (scaffolding temporário, fan-out adversarial, orquestração determinística por código do agente, desacoplamento UI/transcript, loops em rotinas), com novidade e relevância direta a harness-engineering, verification e agent-fleets.
