---
title: "9 Things People Get Wrong With My /grill-* skills"
type: "extract"
source: "youtube"
video_id: "UzMNBN6xLLA"
url: "https://www.youtube.com/watch?v=UzMNBN6xLLA"
channel: "Matt Pocock"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-9-things-people-get-wrong-with-my-grill-skills--UzMNBN6xLLA.txt]]"
tags: ["agentic-coding", "context-engineering", "context-management", "cross-session", "model-selection", "token-budgeting", "decision-discipline", "spec-driven-development", "agent-tooling", "process"]
thesis: "Sessões de 'grilling' (interrogatório contínuo pelo agente até entendimento compartilhado) só funcionam quando o engenheiro gerencia ativamente a fidelidade das perguntas, o escopo, o orçamento de contexto, a capacidade do modelo e o paralelismo de sessões — o skill auxilia, mas não substitui a habilidade de planejar do usuário."
concepts: ["low-fidelity vs high-fidelity questions (taxonomia de Shape Up)", "perguntas grilláveis vs ungrilláveis", "prototyping handoff (handoff para sessão de protótipo e retorno ao grilling)", "sizing de escopo", "'dumb zone' do modelo (~120K tokens onde a atenção degrada)", "postura passiva vs ativa diante do agente (conversa, não entrevista)", "conhecimento contextual vs paramétrico do modelo", "artefato de handoff (PRD) para preservar decisões", "sessões de grilling paralelas para throughput", "entendimento compartilhado como objetivo do grilling", "construir sobre fundação validada vs planejar longamente no futuro"]
tools: ["grill me (skill)", "grill with docs (skill)", "handoff (skill)", "2 PRD (skill de geração de PRD)", "sessão de prototyping", "Gstack (repo de Gary Tan, citado em comparação de stars)", "Slack (analogia para threads paralelas)"]
people: ["Ryan Singer (autor de Shape Up)", "Gary Tan", "criador das skills grill me / grill with docs (palestrante, não nomeado)", "AI Coding for Real Engineers (cohort do palestrante)"]
claims: ["Separe perguntas de baixa fidelidade (resolvíveis por Q&A) das de alta fidelidade (que exigem ver/prototipar); apenas as primeiras são 'grilláveis' em sessão de grilling.", "Ao encontrar pergunta ungrillável sobre 'feel', faça handoff para uma sessão de prototyping, resolva lá e traga os aprendizados de volta à sessão de grilling original.", "Escopo grande demais esconde perguntas de alta fidelidade e empurra a sessão para a 'dumb zone' (~120K tokens em modelos SOTA); escolha escopos menores ou peça ao agente para decompor o escopo em sub-escopos grilláveis individualmente.", "Seja ativo no grilling: dirija a conversa, controle o escopo e o ritmo; passividade leva a bombardeio de perguntas (ex.: 200+ perguntas) e explosão de escopo.", "Evite também o excesso de atividade: não prolongue indefinidamente o grilling em perguntas de baixa fidelidade quando o que falta é ver código funcionando.", "Preserve o contexto valioso gerado no grilling: implemente na mesma sessão se houver orçamento de contexto restante, ou gere um artefato de handoff (ex.: PRD via skill 2 PRD); nunca limpe o contexto e gere o PRD numa janela nova, desperdiçando as decisões tomadas.", "Use modelos frontier/capazes para grilling, pois a fase depende de conhecimento paramétrico para levantar questões e sugestões não óbvias; modelos menores bastam para implementação, que é majoritariamente contextual (plano detalhado + arquivos do codebase).", "Rode 2 sessões de grilling em paralelas (até 3 se uma executa tarefa longa como research) alternando entre elas, dobrando o throughput de planejamento.", "Construa sobre algo já validado e alinhado em vez de agendar dias de tarefas futuras sem fundação sólida, o que tende a produzir resultados ruins.", "O grilling é uma habilidade treinável: com prática, aumenta-se a capacidade de lidar com mais paralelismo (2 a 4 sessões)."]
deep_dive: "medium"
deep_dive_reason: "Contém heurísticas acionáveis e relevantes a context-engineering e model-selection (fidelidade de perguntas, dumb zone ~120K, handoff/PRD, paralelismo), mas é conteúdo instrucional de nível workflow com trechos promocionais e repetitivos, sem profundidade arquitetural em harness, evals ou agent-fleets."
---

# 9 Things People Get Wrong With My /grill-* skills

## Tese
Sessões de 'grilling' (interrogatório contínuo pelo agente até entendimento compartilhado) só funcionam quando o engenheiro gerencia ativamente a fidelidade das perguntas, o escopo, o orçamento de contexto, a capacidade do modelo e o paralelismo de sessões — o skill auxilia, mas não substitui a habilidade de planejar do usuário.

## Conceitos-chave
- low-fidelity vs high-fidelity questions (taxonomia de Shape Up)
- perguntas grilláveis vs ungrilláveis
- prototyping handoff (handoff para sessão de protótipo e retorno ao grilling)
- sizing de escopo
- 'dumb zone' do modelo (~120K tokens onde a atenção degrada)
- postura passiva vs ativa diante do agente (conversa, não entrevista)
- conhecimento contextual vs paramétrico do modelo
- artefato de handoff (PRD) para preservar decisões
- sessões de grilling paralelas para throughput
- entendimento compartilhado como objetivo do grilling
- construir sobre fundação validada vs planejar longamente no futuro

## Ferramentas & pessoas
**Ferramentas:** grill me (skill), grill with docs (skill), handoff (skill), 2 PRD (skill de geração de PRD), sessão de prototyping, Gstack (repo de Gary Tan, citado em comparação de stars), Slack (analogia para threads paralelas)

**Pessoas/orgs:** Ryan Singer (autor de Shape Up), Gary Tan, criador das skills grill me / grill with docs (palestrante, não nomeado), AI Coding for Real Engineers (cohort do palestrante)

## Claims acionáveis
- Separe perguntas de baixa fidelidade (resolvíveis por Q&A) das de alta fidelidade (que exigem ver/prototipar); apenas as primeiras são 'grilláveis' em sessão de grilling.
- Ao encontrar pergunta ungrillável sobre 'feel', faça handoff para uma sessão de prototyping, resolva lá e traga os aprendizados de volta à sessão de grilling original.
- Escopo grande demais esconde perguntas de alta fidelidade e empurra a sessão para a 'dumb zone' (~120K tokens em modelos SOTA); escolha escopos menores ou peça ao agente para decompor o escopo em sub-escopos grilláveis individualmente.
- Seja ativo no grilling: dirija a conversa, controle o escopo e o ritmo; passividade leva a bombardeio de perguntas (ex.: 200+ perguntas) e explosão de escopo.
- Evite também o excesso de atividade: não prolongue indefinidamente o grilling em perguntas de baixa fidelidade quando o que falta é ver código funcionando.
- Preserve o contexto valioso gerado no grilling: implemente na mesma sessão se houver orçamento de contexto restante, ou gere um artefato de handoff (ex.: PRD via skill 2 PRD); nunca limpe o contexto e gere o PRD numa janela nova, desperdiçando as decisões tomadas.
- Use modelos frontier/capazes para grilling, pois a fase depende de conhecimento paramétrico para levantar questões e sugestões não óbvias; modelos menores bastam para implementação, que é majoritariamente contextual (plano detalhado + arquivos do codebase).
- Rode 2 sessões de grilling em paralelas (até 3 se uma executa tarefa longa como research) alternando entre elas, dobrando o throughput de planejamento.
- Construa sobre algo já validado e alinhado em vez de agendar dias de tarefas futuras sem fundação sólida, o que tende a produzir resultados ruins.
- O grilling é uma habilidade treinável: com prática, aumenta-se a capacidade de lidar com mais paralelismo (2 a 4 sessões).

> **Deep dive:** `medium` — Contém heurísticas acionáveis e relevantes a context-engineering e model-selection (fidelidade de perguntas, dumb zone ~120K, handoff/PRD, paralelismo), mas é conteúdo instrucional de nível workflow com trechos promocionais e repetitivos, sem profundidade arquitetural em harness, evals ou agent-fleets.
