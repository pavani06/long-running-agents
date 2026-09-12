---
title: "The Golden Age of AI Engineering — Alexander Embiricos & Romain Huet & Peter Steinberger, OpenAI"
type: "extract"
source: "youtube"
video_id: "pMggiOb18tc"
url: "https://www.youtube.com/watch?v=pMggiOb18tc"
channel: "AI Engineer"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-the-golden-age-of-ai-engineering-alexander-embiricos-romain-huet-peter-steinberg--pMggiOb18tc.txt]]"
tags: ["agents", "agent-fleets", "agent-loop", "agentic-coding", "agent-tooling", "harness", "harness-engineering", "context-engineering", "context-management", "multi-agent", "cross-session", "decision-discipline", "token-budgeting", "model-selection", "stack-tooling", "runtime", "roadmap", "arquitetura", "escalation"]
thesis: "A engenharia está sendo devolvida às suas raízes por engenheiros de IA que, em vez de assistir agentes escrever código, gerenciam loops persistentes de agentes (manager-delegation-triggers) sobre uma stack aberta e em camadas, onde a atenção humana — e não tokens ou compute — é o gargalo decisivo."
concepts: ["AI engineers eating the world / retorno às raízes da engenharia", "duas modalidades de produto: chat subestimado + UI colaborativa hands-on", "agente conectado ao 'porquê' antes do código e ao review/deploy depois", "stack aberta em camadas (API, harness, apps server, plugins)", "API-first: novas capacidades entram na Responses API antes do produto", "compaction server-side para tarefas longas", "coordination: uma thread cria e dirige projetos", "triggers/automação que acordam o mesmo manager", "contexto persistente + delegação + triggers = o loop", "evolução: scheduler/roteador/memória humano -> gerenciar 10 direct reports -> manage the manager", "gargalos em sequência: tokens -> compute -> atenção humana", "inner execution loop (agente) vs outer loop (direção e decisões humanas)", "value maxing vs token maxing", "eficiência de custo em tiers de modelo", "velocidade extrema habilitando múltiplas abordagens paralelas e seleção da melhor", "unificação local/cloud: o agente escolhe o ambiente", "test boxes: rodar testes em máquina separada", "manager longevo não preso a laptop/app; acessível via Slack/texto", "modelos avançam mais rápido que harnesses e organizações", "agent triando issues contra goals/notes/vision do projeto"]
tools: ["Codex", "Codex app", "Codex CLI", "Codex Cloud", "Codex for iOS", "Codex Monitor", "Codex image gen", "Responses API", "AGENTS.md", "Codex harness (open source)", "Codex apps server (open source)", "plugins browser use e computer use", "GPT 5.6 series (preview)", "GPT 5.6 'terra'", "GPT 5.6 'Luna'", "GPT 5.6 'SUL'", "GPT 5.5", "GPT 5.3 Codex Spark", "Cerebras", "Terminal Bench", "opencode", "openclaw (OpenClaw gateway/nodes)", "pi", "droid", "Xcode", "JetBrains", "VS Code", "Slack", "VNC", "GitHub"]
people: ["OpenAI", "Raman (speaker)", "Alexander (speaker)", "Peter Steinberger ('claw father')", "Theo", "Paul Salt", "Tuma (Dimilian)", "opencode team", "Cerebras"]
claims: ["Conecte o agente ao motivo do trabalho (antes do código) e ao review/deploy (depois) para que ele comece e 'aterrisse' muito mais trabalho", "Construa sobre as mesmas primitivas que a OpenAI usa: novas capacidades como compaction são incorporadas primeiro na Responses API", "Fork o harness open-source do Codex como implementação de referência; os modelos não são hardcoded e podem ser trocados por modelos abertos mantendo o agent loop", "Use o apps server open-source para construir clientes próprios autenticando com a assinatura existente do Codex (como Tuma fez com o Codex Monitor)", "Torne loops longos confiáveis combinando compaction server-side, coordination e triggers — contexto persistente, delegação e gatilhos", "Elimine o gargalo de compute rodando testes em máquinas separadas (test boxes) enquanto múltiplos threads rodam em paralelo", "Pare de assistir o agente gerar código: modelos recentes entendem intenção bem o suficiente; revise artefatos (PR, issue, diff, vídeo, build rodando via VNC) uma única vez", "Deixe o manager triar issues contra goals/notes/vision do projeto antes de criar workers; separe o agente worker do agente reviewer", "Posicione o humano no outer loop (direção e decisões) e os agentes no inner execution loop", "Com ~750 tokens/s, rode 5-6 abordagens paralelas e escolha a melhor no tempo de uma única resposta lenta", "Escolha tier de modelo por custo-eficiência (ex.: 'terra' com inteligência do 5.5 pela metade do custo; 'Luna' a $1/M input, $6/M output)", "Um manager longevo deve ser alcançável de qualquer lugar (Slack, texto) e mover trabalho entre hosts/cloud/local, não ficar preso como sessão dentro de um app", "Modelos estão avançando mais rápido que harnesses e organizações; projetar esses loops é o próximo problema de engenharia", "Use automação para acordar o manager periodicamente (ex.: chief of staff a cada 10 minutos coordenando trabalho no GitHub, criando threads para steering)"]
deep_dive: "high"
deep_dive_reason: "Apesar da metade promocional de lançamentos, a palestra entrega densidade alta e novidade acionável sobre harness (stack aberta em camadas, API-first), agent-fleets (manager-worker-reviewer com contexto persistente, delegação e triggers) e alocação de atenção humana como gargalo arquitetural."
---

# The Golden Age of AI Engineering — Alexander Embiricos & Romain Huet & Peter Steinberger, OpenAI

## Tese
A engenharia está sendo devolvida às suas raízes por engenheiros de IA que, em vez de assistir agentes escrever código, gerenciam loops persistentes de agentes (manager-delegation-triggers) sobre uma stack aberta e em camadas, onde a atenção humana — e não tokens ou compute — é o gargalo decisivo.

## Conceitos-chave
- AI engineers eating the world / retorno às raízes da engenharia
- duas modalidades de produto: chat subestimado + UI colaborativa hands-on
- agente conectado ao 'porquê' antes do código e ao review/deploy depois
- stack aberta em camadas (API, harness, apps server, plugins)
- API-first: novas capacidades entram na Responses API antes do produto
- compaction server-side para tarefas longas
- coordination: uma thread cria e dirige projetos
- triggers/automação que acordam o mesmo manager
- contexto persistente + delegação + triggers = o loop
- evolução: scheduler/roteador/memória humano -> gerenciar 10 direct reports -> manage the manager
- gargalos em sequência: tokens -> compute -> atenção humana
- inner execution loop (agente) vs outer loop (direção e decisões humanas)
- value maxing vs token maxing
- eficiência de custo em tiers de modelo
- velocidade extrema habilitando múltiplas abordagens paralelas e seleção da melhor
- unificação local/cloud: o agente escolhe o ambiente
- test boxes: rodar testes em máquina separada
- manager longevo não preso a laptop/app; acessível via Slack/texto
- modelos avançam mais rápido que harnesses e organizações
- agent triando issues contra goals/notes/vision do projeto

## Ferramentas & pessoas
**Ferramentas:** Codex, Codex app, Codex CLI, Codex Cloud, Codex for iOS, Codex Monitor, Codex image gen, Responses API, AGENTS.md, Codex harness (open source), Codex apps server (open source), plugins browser use e computer use, GPT 5.6 series (preview), GPT 5.6 'terra', GPT 5.6 'Luna', GPT 5.6 'SUL', GPT 5.5, GPT 5.3 Codex Spark, Cerebras, Terminal Bench, opencode, openclaw (OpenClaw gateway/nodes), pi, droid, Xcode, JetBrains, VS Code, Slack, VNC, GitHub

**Pessoas/orgs:** OpenAI, Raman (speaker), Alexander (speaker), Peter Steinberger ('claw father'), Theo, Paul Salt, Tuma (Dimilian), opencode team, Cerebras

## Claims acionáveis
- Conecte o agente ao motivo do trabalho (antes do código) e ao review/deploy (depois) para que ele comece e 'aterrisse' muito mais trabalho
- Construa sobre as mesmas primitivas que a OpenAI usa: novas capacidades como compaction são incorporadas primeiro na Responses API
- Fork o harness open-source do Codex como implementação de referência; os modelos não são hardcoded e podem ser trocados por modelos abertos mantendo o agent loop
- Use o apps server open-source para construir clientes próprios autenticando com a assinatura existente do Codex (como Tuma fez com o Codex Monitor)
- Torne loops longos confiáveis combinando compaction server-side, coordination e triggers — contexto persistente, delegação e gatilhos
- Elimine o gargalo de compute rodando testes em máquinas separadas (test boxes) enquanto múltiplos threads rodam em paralelo
- Pare de assistir o agente gerar código: modelos recentes entendem intenção bem o suficiente; revise artefatos (PR, issue, diff, vídeo, build rodando via VNC) uma única vez
- Deixe o manager triar issues contra goals/notes/vision do projeto antes de criar workers; separe o agente worker do agente reviewer
- Posicione o humano no outer loop (direção e decisões) e os agentes no inner execution loop
- Com ~750 tokens/s, rode 5-6 abordagens paralelas e escolha a melhor no tempo de uma única resposta lenta
- Escolha tier de modelo por custo-eficiência (ex.: 'terra' com inteligência do 5.5 pela metade do custo; 'Luna' a $1/M input, $6/M output)
- Um manager longevo deve ser alcançável de qualquer lugar (Slack, texto) e mover trabalho entre hosts/cloud/local, não ficar preso como sessão dentro de um app
- Modelos estão avançando mais rápido que harnesses e organizações; projetar esses loops é o próximo problema de engenharia
- Use automação para acordar o manager periodicamente (ex.: chief of staff a cada 10 minutos coordenando trabalho no GitHub, criando threads para steering)

> **Deep dive:** `high` — Apesar da metade promocional de lançamentos, a palestra entrega densidade alta e novidade acionável sobre harness (stack aberta em camadas, API-first), agent-fleets (manager-worker-reviewer com contexto persistente, delegação e triggers) e alocação de atenção humana como gargalo arquitetural.
