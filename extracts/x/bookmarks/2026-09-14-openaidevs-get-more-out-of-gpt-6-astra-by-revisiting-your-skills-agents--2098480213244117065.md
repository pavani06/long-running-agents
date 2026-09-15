---
title: "Instruções e skills para GPT-6 Astra"
type: "extract"
source: "x"
status_id: "2098480213244117065"
handle: "OpenAIDevs"
url: "https://x.com/OpenAIDevs/status/2098480213244117065"
created_at: "2026-09-11T18:34:05.000Z"
extracted: "2026-09-15"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-14-openaidevs-get-more-out-of-gpt-6-astra-by-revisiting-your-skills-agents--2098480213244117065.json]]"
tags: ["agent-context", "context-engineering", "context-management", "agent-tooling", "repo-as-context", "agentic-coding"]
topic: "Instruções e skills para GPT-6 Astra"
summary: "Guia da OpenAI sobre revisar skills, AGENTS.md e prompts ao migrar para GPT-6 Astra: modelos mais capazes exigem menos scaffolding, e instruções antigas (descrições longas, leituras obrigatórias, cercas de segurança) agora atrapalham. Vale salvar como checklist de manutenção de contexto de agentes."
key_points: ["Descrições de skills devem ser curtas e específicas: com muitas skills, o Codex trunca as descrições, e textos longos ou contraditórios levam o modelo a carregar orientações inúteis para a tarefa.", "Use progressive disclosure: faça do documento raiz da skill um roteador mínimo que aponta para docs e scripts de apoio, poupando contexto e evitando compaction prematura.", "Remova do AGENTS.md instruções obsoletas: exigir leitura de docs/mapa do repo antes de cada edição queima contexto, e pedir para rodar testes é redundante — Astra faz isso sozinho; em vez disso, conceda permissão explícita para workflows seguros (ex.: suite de testes local com fixtures descartáveis).", "Linguagem restritiva escrita para modelos menos alinhados pode fazer Astra parar cedo demais: atualize fronteiras de decisão e defina 'pronto' antes de começar (implementar, inspecionar, corrigir), incluindo onde o modelo deve continuar ou parar.", "Um novo modelo é oportunidade de limpeza — e a própria auditoria das instruções pode ser delegada ao agente com base nos critérios do artigo."]
entities: ["OpenAI", "GPT-6 Astra", "Codex", "AGENTS.md", "$skill-creator", "GPT-5.6 Sol", "Luna"]
content_type: "resource"
revisit: "high"
grounded_in: "article"
thin: false
links: ["https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra"]
media: []
---

# Instruções e skills para GPT-6 Astra

**@OpenAIDevs** · [2098480213244117065](https://x.com/OpenAIDevs/status/2098480213244117065) · `resource`

## Resumo
Guia da OpenAI sobre revisar skills, AGENTS.md e prompts ao migrar para GPT-6 Astra: modelos mais capazes exigem menos scaffolding, e instruções antigas (descrições longas, leituras obrigatórias, cercas de segurança) agora atrapalham. Vale salvar como checklist de manutenção de contexto de agentes.

## Pontos-chave
- Descrições de skills devem ser curtas e específicas: com muitas skills, o Codex trunca as descrições, e textos longos ou contraditórios levam o modelo a carregar orientações inúteis para a tarefa.
- Use progressive disclosure: faça do documento raiz da skill um roteador mínimo que aponta para docs e scripts de apoio, poupando contexto e evitando compaction prematura.
- Remova do AGENTS.md instruções obsoletas: exigir leitura de docs/mapa do repo antes de cada edição queima contexto, e pedir para rodar testes é redundante — Astra faz isso sozinho; em vez disso, conceda permissão explícita para workflows seguros (ex.: suite de testes local com fixtures descartáveis).
- Linguagem restritiva escrita para modelos menos alinhados pode fazer Astra parar cedo demais: atualize fronteiras de decisão e defina 'pronto' antes de começar (implementar, inspecionar, corrigir), incluindo onde o modelo deve continuar ou parar.
- Um novo modelo é oportunidade de limpeza — e a própria auditoria das instruções pode ser delegada ao agente com base nos critérios do artigo.

## Links
- https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra

## Entidades
OpenAI, GPT-6 Astra, Codex, AGENTS.md, $skill-creator, GPT-5.6 Sol, Luna

> **Revisit:** `high` · **fonte:** `article`
