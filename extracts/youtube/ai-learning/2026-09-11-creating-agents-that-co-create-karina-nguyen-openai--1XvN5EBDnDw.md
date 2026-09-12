---
title: "Creating Agents that Co-Create — Karina Nguyen, OpenAI"
type: "extract"
source: "youtube"
video_id: "1XvN5EBDnDw"
url: "https://www.youtube.com/watch?v=1XvN5EBDnDw"
channel: "AI Engineer"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-creating-agents-that-co-create-karina-nguyen-openai--1XvN5EBDnDw.txt]]"
tags: ["agents", "multi-agent", "context-management", "verification", "evals", "agentic-coding", "roadmap"]
thesis: "Dois paradigmas de escala — pre-training via next-token prediction e reinforcement learning sobre chain-of-thought — desbloquearam uma nova classe de pesquisa de produto, cujo próximo estágio é transformar agentes em co-inovadores por meio de colaboração criativa humano-IA."
concepts: ["next-token prediction como máquina de construção de mundo", "pre-training e scaling de compute", "post-training com RLHF/RLAIF", "scaling de reinforcement learning sobre chain-of-thought (o1)", "test-time compute", "interação streaming dos pensamentos do modelo", "agentes com ferramentas reais (browsing, busca, computer use) em horizonte longo", "co-inovadores: raciocínio + tool use + long context + criatividade", "destilação de modelos de raciocínio para modelos rápidos", "geração sintética de dados e ambientes de RL", "familiar form factor para capacidades desconhecidas (100K context via upload de arquivos)", "composição modular de features de produto", "síncrono vs. assíncrono na conclusão de tarefas", "confiança como gargalo, resolvida por affordances de verificação/edição e feedback em tempo real", "teammate virtual em organizações (Claude no Slack)", "multiplayer e multi-agent no mesmo artefato (Canvas)", "tutores personalizados multimodais", "criação invisível de software para todos", "acesso à internet via 'lente do modelo' em vez de links", "canvas em branco que se auto-molda à intenção do usuário", "co-direção criativa com modelos", "faithfulness do chain-of-thought como problema aberto", "escrita criativa e coerência de enredo como problema difícil de pre-training e avaliação"]
tools: ["ChatGPT", "Claude", "Canvas", "ChatGPT Tasks", "Claude in Slack", "GitHub Copilot", "Cursor", "o1", "GPT-4o", "RLHF", "RLAIF", "chain-of-thought", "computer use", "browsing/search", "canvas como pair programmer e data scientist"]
people: ["Karina (pesquisadora, ex-Anthropic, OpenAI)", "OpenAI", "Anthropic", "GitHub", "Slack"]
claims: ["Tarefas como matemática e escrita criativa exigem mais compute/test-time compute porque next-token prediction puro não captura raciocínio computacional denso nem coerência de enredo de longo prazo", "Medir a faithfulness do chain-of-thought e a qualidade de escrita criativa permanece um problema aberto de avaliação", "Para iteração rápida de produto, destile modelos de raciocínio complexos em modelos menores/mais rápidos e use-os para gerar dados sintéticos e novos ambientes de RL", "Ao lançar capacidades desconhecidas (ex.: contexto de 100K), encontre o form factor mais familiar possível (upload de arquivos) para adoção", "Projete features de produto para composição modular, para que escalem conforme a capacidade dos modelos cresce", "O gargalo para tarefas assíncronas de longo prazo (10 horas de pesquisa/código) é confiança; resolva dando aos humanos affordances para verificar, editar e dar feedback em tempo real nos outputs", "Interfaces como Canvas escalam de co-editor para multiplayer e multi-agent, adicionando agentes críticos/editores ao mesmo documento", "Streaming de resumos dos pensamentos do modelo reduz o custo de espera em novos paradigmas de interação de raciocínio", "Modele novos produtos como novas classes de tarefas: simule usuários sinteticamente e treine RL condicionado a perfis de usuário", "O acesso à internet tende a migrar de cliques em links para respostas personalizadas e multimodais mediadas por modelos"]
deep_dive: "medium"
deep_dive_reason: "A palestra traz lições de design de produto acionáveis e algumas intuições sobre scaling, mas permanece em nível alto, sem densidade arquitetural em harness, evals, governança ou engenharia de contexto que justificasse o tier alto."
---

# Creating Agents that Co-Create — Karina Nguyen, OpenAI

## Tese
Dois paradigmas de escala — pre-training via next-token prediction e reinforcement learning sobre chain-of-thought — desbloquearam uma nova classe de pesquisa de produto, cujo próximo estágio é transformar agentes em co-inovadores por meio de colaboração criativa humano-IA.

## Conceitos-chave
- next-token prediction como máquina de construção de mundo
- pre-training e scaling de compute
- post-training com RLHF/RLAIF
- scaling de reinforcement learning sobre chain-of-thought (o1)
- test-time compute
- interação streaming dos pensamentos do modelo
- agentes com ferramentas reais (browsing, busca, computer use) em horizonte longo
- co-inovadores: raciocínio + tool use + long context + criatividade
- destilação de modelos de raciocínio para modelos rápidos
- geração sintética de dados e ambientes de RL
- familiar form factor para capacidades desconhecidas (100K context via upload de arquivos)
- composição modular de features de produto
- síncrono vs. assíncrono na conclusão de tarefas
- confiança como gargalo, resolvida por affordances de verificação/edição e feedback em tempo real
- teammate virtual em organizações (Claude no Slack)
- multiplayer e multi-agent no mesmo artefato (Canvas)
- tutores personalizados multimodais
- criação invisível de software para todos
- acesso à internet via 'lente do modelo' em vez de links
- canvas em branco que se auto-molda à intenção do usuário
- co-direção criativa com modelos
- faithfulness do chain-of-thought como problema aberto
- escrita criativa e coerência de enredo como problema difícil de pre-training e avaliação

## Ferramentas & pessoas
**Ferramentas:** ChatGPT, Claude, Canvas, ChatGPT Tasks, Claude in Slack, GitHub Copilot, Cursor, o1, GPT-4o, RLHF, RLAIF, chain-of-thought, computer use, browsing/search, canvas como pair programmer e data scientist

**Pessoas/orgs:** Karina (pesquisadora, ex-Anthropic, OpenAI), OpenAI, Anthropic, GitHub, Slack

## Claims acionáveis
- Tarefas como matemática e escrita criativa exigem mais compute/test-time compute porque next-token prediction puro não captura raciocínio computacional denso nem coerência de enredo de longo prazo
- Medir a faithfulness do chain-of-thought e a qualidade de escrita criativa permanece um problema aberto de avaliação
- Para iteração rápida de produto, destile modelos de raciocínio complexos em modelos menores/mais rápidos e use-os para gerar dados sintéticos e novos ambientes de RL
- Ao lançar capacidades desconhecidas (ex.: contexto de 100K), encontre o form factor mais familiar possível (upload de arquivos) para adoção
- Projete features de produto para composição modular, para que escalem conforme a capacidade dos modelos cresce
- O gargalo para tarefas assíncronas de longo prazo (10 horas de pesquisa/código) é confiança; resolva dando aos humanos affordances para verificar, editar e dar feedback em tempo real nos outputs
- Interfaces como Canvas escalam de co-editor para multiplayer e multi-agent, adicionando agentes críticos/editores ao mesmo documento
- Streaming de resumos dos pensamentos do modelo reduz o custo de espera em novos paradigmas de interação de raciocínio
- Modele novos produtos como novas classes de tarefas: simule usuários sinteticamente e treine RL condicionado a perfis de usuário
- O acesso à internet tende a migrar de cliques em links para respostas personalizadas e multimodais mediadas por modelos

> **Deep dive:** `medium` — A palestra traz lições de design de produto acionáveis e algumas intuições sobre scaling, mas permanece em nível alto, sem densidade arquitetural em harness, evals, governança ou engenharia de contexto que justificasse o tier alto.
