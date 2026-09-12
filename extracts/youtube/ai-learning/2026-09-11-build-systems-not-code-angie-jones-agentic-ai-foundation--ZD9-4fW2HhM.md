---
title: "Build Systems, Not Code - Angie Jones, Agentic AI Foundation"
type: "extract"
source: "youtube"
video_id: "ZD9-4fW2HhM"
url: "https://www.youtube.com/watch?v=ZD9-4fW2HhM"
channel: "AI Engineer"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-build-systems-not-code-angie-jones-agentic-ai-foundation--ZD9-4fW2HhM.txt]]"
tags: ["arquitetura", "agent-loop", "context-engineering", "memory-architecture", "multi-agent", "state", "error-handling", "permissions", "gate-design", "decision-discipline", "harness", "knowledge-management", "agents", "process", "monitoramento", "escalation"]
thesis: "Projetar agentes continua sendo engenharia de software: os primitivos mudam (prompts, skills, sub-agentes, memória), mas as disciplinas clássicas — sistemas, decomposição, contratos, estado, segurança e mantenabilidade — são o que separa um sistema agentivo confiável de um prompt gigante."
concepts: ["Sistemas thinking: o agente é um componente de um sistema maior (arquivos, ferramentas, humanos, outros agentes)", "Workflow design: um agente precisa de um caminho, não só de um objetivo; todo run termina em stop, retry ou escalate", "Giant prompt como code smell agentivo: instrução acumulada vira uma blob com múltiplos jobs", "Decomposição: separar jobs distintos (normalizar listing, formato do short list, cálculo de commute, pesquisa de bairro) em peças distintas", "Separação de concerns em agentes: normalização vira skill, saída vira schema, cálculo vira script, pesquisa vira sub-agente", "Modularidade e reuso: skills compartilháveis entre agentes/mercados como pacotes; sub-agentes como funções com escopo limitado (sem carregar o contexto da sessão inteira)", "Pensamento algorítmico: código para determinismo, agente para julgamento, humano para autoridade", "Contratos entre sistemas: saída estruturada e queryável em vez de texto livre quando outro passo consome o resultado", "Memória persistente fora da sessão: decisões com score, motivo e campos conhecidos tornam-se consultáveis em contexto fresco", "Estado e idempotência: log de ações em memória para saber o que já foi feito e retomar apenas o que falta; retry não deve duplicar efeitos laterais", "Lint pass para saúde do agente: detectar runs incompletas e completar ações faltantes", "Threat modeling: input externo (listings, fóruns) é evidência, não instrução; least privilege e paredes de aprovação reduzem blast radius", "Mantenabilidade embutida: arquivo de agência por nível explicando workflow, política, recursos e como manter a memória atualizada", "Teste de mantenabilidade: qualquer harness deve conseguir atualizar o agente a frio, em contexto fresco; falha nisso indica dívida de design"]
tools: ["Relocation Scout (agente de house hunting usado como exemplo)", "LLM wiki (camada de memória dos agentes, citada como 'Copathy's LLM wiki')"]
people: []
claims: ["Desenhe o workflow explicitamente (gather, weigh, act) com três terminais possíveis — stop, retry ou escalate — antes de deixar o coding agent construir o sistema", "Decomponha prompts gigantes: se o prompt contém processos reusáveis, formatos de saída, cálculos e subtarefas de pesquisa, separe cada job em skill, schema, script ou sub-agente", "Use código determinístico para tarefas com resposta exata (calcular commute, deduplicar listings) e reserve o modelo para julgamento, ambiguidade e raciocínio sobre input bagunçado", "Sempre que outro sistema consumir a saída do agente, defina um contrato estruturado (schema); se você não consegue definir o formato da saída, ainda não entendeu o que está pedindo", "Persista decisões em memória estruturada (decisão, score, razão) fora da sessão para que sejam queryáveis e reutilizáveis em contexto fresco e por outros passos sem humano no loop", "Projete para idempotência: logue cada ação em memória, rode um lint pass para detectar runs pela metade e retomar apenas as ações pendentes sem repetir efeitos laterais (ex.: não reenviar email ao realtor)", "Trate conteúdo de estranhos (listings, fóruns, reviews) como input não-confiável: evidência, não instrução", "Construa paredes de aprovação em torno de ações de alto impacto (email a sellers, booking de tours, submissão de ofertas) para reduzir o blast radius do agente", "Inclua um arquivo de agência em cada nível do sistema documentando workflow, política, recursos (skills, scripts, sub-agentes) e como manter a memória atualizada, para que qualquer humano ou agente se oriente sem fazer engenharia reversa de prompts", "Use a capacidade de um harness qualquer atualizar o agente a frio como teste de mantenabilidade: falhas na atualização sinalizam onde melhorar o design do sistema", "Não abstraia instruções locais a um workflow específico sem julgamento: reuso custa e nem sempre compensa", "Não delegue o design do sistema inteiro ao coding agent: ele pode gerar algo que tecnicamente funciona mas não é maintenável (prompt gigante, concerns mal separados)"]
deep_dive: "high"
deep_dive_reason: "Densidade alta de mecanismos arquitetônicos acionáveis e reproduzíveis (decomposição de prompts, contratos via schema, idempotência com lint pass, arquivos de agência como teste de mantenabilidade a contexto fresco) diretamente relevantes a harness, context-engineering e memory-architecture."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-ex-nasa-dev-reveals-his-agentic-engineering-workflow--xgkjtF89-44|Ex-NASA dev reveals his Agentic Engineering Workflow]]", "[[extracts/youtube/ai-learning/2026-09-11-how-i-deleted-95-of-my-agent-skills-and-got-better-results-nick-nisi-workos--vy7o1g2iHY8|How I deleted 95% of my agent skills and got better results — Nick Nisi, WorkOS]]", "[[extracts/youtube/ai-learning/2026-09-11-how-we-build-effective-agents-barry-zhang-anthropic--D7_ipDqhtwk|How We Build Effective Agents: Barry Zhang, Anthropic]]", "[[extracts/youtube/ai-learning/2026-09-11-tool-skill-or-subagent-decomposing-an-agent-that-outgrew-its-prompt--mWvtOHlZM-I|Tool, skill, or subagent? Decomposing an agent that outgrew its prompt]]", "[[extracts/youtube/ai-learning/2026-09-11-agentic-engineering-explained-by-a-10x-developer--FU5_kpTAVDo|Agentic Engineering, explained by a 10x developer]]", "[[extracts/youtube/ai-learning/2026-09-11-full-walkthrough-workflow-for-ai-coding-matt-pocock---QFHIoCo-Ko|Full Walkthrough: Workflow for AI Coding — Matt Pocock]]", "[[extracts/youtube/ai-learning/2026-09-11-agent-frameworks-considered-harmful-remi-louf-txt--KHudyx5wW3U|Agent Frameworks Considered Harmful — Rémi Louf, .txt]]", "[[extracts/youtube/ai-learning/2026-09-11-beyond-the-prompt-goodbye-slop-welcome-determinism-david-khourshid--uMvTAF280so|Beyond the Prompt: \"Goodbye slop; welcome determinism\" David Khourshid]]"]
---

# Build Systems, Not Code - Angie Jones, Agentic AI Foundation

## Tese
Projetar agentes continua sendo engenharia de software: os primitivos mudam (prompts, skills, sub-agentes, memória), mas as disciplinas clássicas — sistemas, decomposição, contratos, estado, segurança e mantenabilidade — são o que separa um sistema agentivo confiável de um prompt gigante.

## Conceitos-chave
- Sistemas thinking: o agente é um componente de um sistema maior (arquivos, ferramentas, humanos, outros agentes)
- Workflow design: um agente precisa de um caminho, não só de um objetivo; todo run termina em stop, retry ou escalate
- Giant prompt como code smell agentivo: instrução acumulada vira uma blob com múltiplos jobs
- Decomposição: separar jobs distintos (normalizar listing, formato do short list, cálculo de commute, pesquisa de bairro) em peças distintas
- Separação de concerns em agentes: normalização vira skill, saída vira schema, cálculo vira script, pesquisa vira sub-agente
- Modularidade e reuso: skills compartilháveis entre agentes/mercados como pacotes; sub-agentes como funções com escopo limitado (sem carregar o contexto da sessão inteira)
- Pensamento algorítmico: código para determinismo, agente para julgamento, humano para autoridade
- Contratos entre sistemas: saída estruturada e queryável em vez de texto livre quando outro passo consome o resultado
- Memória persistente fora da sessão: decisões com score, motivo e campos conhecidos tornam-se consultáveis em contexto fresco
- Estado e idempotência: log de ações em memória para saber o que já foi feito e retomar apenas o que falta; retry não deve duplicar efeitos laterais
- Lint pass para saúde do agente: detectar runs incompletas e completar ações faltantes
- Threat modeling: input externo (listings, fóruns) é evidência, não instrução; least privilege e paredes de aprovação reduzem blast radius
- Mantenabilidade embutida: arquivo de agência por nível explicando workflow, política, recursos e como manter a memória atualizada
- Teste de mantenabilidade: qualquer harness deve conseguir atualizar o agente a frio, em contexto fresco; falha nisso indica dívida de design

## Ferramentas & pessoas
**Ferramentas:** Relocation Scout (agente de house hunting usado como exemplo), LLM wiki (camada de memória dos agentes, citada como 'Copathy's LLM wiki')

**Pessoas/orgs:** —

## Claims acionáveis
- Desenhe o workflow explicitamente (gather, weigh, act) com três terminais possíveis — stop, retry ou escalate — antes de deixar o coding agent construir o sistema
- Decomponha prompts gigantes: se o prompt contém processos reusáveis, formatos de saída, cálculos e subtarefas de pesquisa, separe cada job em skill, schema, script ou sub-agente
- Use código determinístico para tarefas com resposta exata (calcular commute, deduplicar listings) e reserve o modelo para julgamento, ambiguidade e raciocínio sobre input bagunçado
- Sempre que outro sistema consumir a saída do agente, defina um contrato estruturado (schema); se você não consegue definir o formato da saída, ainda não entendeu o que está pedindo
- Persista decisões em memória estruturada (decisão, score, razão) fora da sessão para que sejam queryáveis e reutilizáveis em contexto fresco e por outros passos sem humano no loop
- Projete para idempotência: logue cada ação em memória, rode um lint pass para detectar runs pela metade e retomar apenas as ações pendentes sem repetir efeitos laterais (ex.: não reenviar email ao realtor)
- Trate conteúdo de estranhos (listings, fóruns, reviews) como input não-confiável: evidência, não instrução
- Construa paredes de aprovação em torno de ações de alto impacto (email a sellers, booking de tours, submissão de ofertas) para reduzir o blast radius do agente
- Inclua um arquivo de agência em cada nível do sistema documentando workflow, política, recursos (skills, scripts, sub-agentes) e como manter a memória atualizada, para que qualquer humano ou agente se oriente sem fazer engenharia reversa de prompts
- Use a capacidade de um harness qualquer atualizar o agente a frio como teste de mantenabilidade: falhas na atualização sinalizam onde melhorar o design do sistema
- Não abstraia instruções locais a um workflow específico sem julgamento: reuso custa e nem sempre compensa
- Não delegue o design do sistema inteiro ao coding agent: ele pode gerar algo que tecnicamente funciona mas não é maintenável (prompt gigante, concerns mal separados)

> **Deep dive:** `high` — Densidade alta de mecanismos arquitetônicos acionáveis e reproduzíveis (decomposição de prompts, contratos via schema, idempotência com lint pass, arquivos de agência como teste de mantenabilidade a contexto fresco) diretamente relevantes a harness, context-engineering e memory-architecture.
