---
title: "Every company should have a Brain — Garry Tan, Y Combinator"
type: "extract"
source: "youtube"
video_id: "eBUyTS7SzV4"
url: "https://www.youtube.com/watch?v=eBUyTS7SzV4"
channel: "AI Engineer"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-every-company-should-have-a-brain-garry-tan-y-combinator--eBUyTS7SzV4.txt]]"
tags: ["agents", "agentic-coding", "agent-fleets", "harness", "context-engineering", "memory-architecture", "knowledge-management", "evals", "governanca", "instituicoes", "investimentos", "stack-tooling"]
thesis: "A vantagem de 400x dos engenheiros com agentes não vem dos pesos do modelo, mas de 'wire the work' — tratar harness como uma organização de skill files (funcionários de markdown) alimentada por um company brain curado (biblioteca + bibliotecário) que transforma conhecimento em ativo composto."
concepts: ["skill file como funcionário (uma capacidade, um job escrito com clareza executável)", "tabela de resolução (resolver table) como organograma de roteamento de tarefas", "filing rules como processo interno", "trigger evals como revisões de desempenho dos skills", "workforce feita de markdown: gerenciar agentes é contratar/treinar/gerir", "separação entre espaço latente (gosto, julgamento, intenções vagas) e espaço determinístico (código); bugs nascem do cálculo no lado errado", "estado grande (ex.: arranjo de 800 assentos) não deve viver no context window", "memória de trabalho: 7±2 itens humanos vs ~1M tokens (~3 livros) do agente", "context engineering = decidir quais 'três livros' ficam abertos na mesa do agente", "company brain = biblioteca + bibliotecário; retrieval é o primitivo, curadoria é o produto", "higiene de memória: proveniência em cada fato, checagem de contradições, bibliotecário humano+agente para poda", "hot memory vs cold reference e arbitragem de fatos conflitantes", "'skillify it': nunca fazer trabalho one-off; se pediu duas vezes, você falhou", "model quality é alugado; o brain/compounding library é propriedade", "engenheiros de empresa AI-native mantêm skills e fazem o que os skills ainda não fazem"]
tools: ["Claude / Claude Code (CLAUDE.md)", "Codex", "OpenClaw", "Hermes agent", "GBrain", "Postgres", "TypeScript", "Erlang/Elixir", "Excel", "tests.md", "X (blog posts)"]
people: ["Y Combinator (YC)", "Theo", "Emergence", "Retail", "Startup School / Startup Battlefield"]
claims: ["Mapeie a infraestrutura de agentes para uma organização: skill file = funcionário, resolver table = organograma, filing rules = processo, trigger evals = performance review", "Ao sentar com Claude Code ou Codex você não está escrevendo software, está contratando, treinando e gerenciando uma força de trabalho de markdown", "Tenha cuidado explícito sobre onde a computação acontece: chamadas não determinísticas (julgamento, gosto, intent vago) no espaço latente; tudo mais em código determinístico", "Estado volumoso (arrays multidimensionais, storage) deve ficar fora do context window — o LLM faz só a parte humana", "Context engineering é decidir quais 'três livros' entram na memória de trabalho do agente para cada tarefa", "Retrieval/RAG é o primitivo fácil; o produto é ser digno de retrieval: o que é escrito, como é enriquecido/ligado, o que vira hot memory vs cold reference, e quem arbitra fatos conflitantes", "Trate o company brain como infraestrutura de produção: proveniência por fato, contradição checada quando novo dado colide, e bibliotecário humano+agente dedicado à poda — senão você tem um lixão com ótima busca", "Nunca faça trabalho one-off: ao terminar uma tarefa com output bom, 'skillify' — converta em skill file reutilizável no harness", "Contrate engenheiros cujo trabalho é manter skills e cobrir o que os skills ainda não executam", "O speaker reporta ~400x de output pessoal vs 2013 (~14 linhas lógicas/dia), com piso de 8x mesmo penalizando verbosidade; a diferença 2x vs 100x está na fiação do trabalho, não nos pesos do modelo", "Dados citados: 1/4 do batch W25 da YC tinha codebases 95% gerados por IA (batch mais rápido-crescente e lucrativo da história); 94 empresas YC passaram de $100M de receita; Emercence (Summer 24) 9 dígitos de ARR em 8 meses com 15 pessoas aos $15M; Retail (W24) $60M com ~40 pessoas", "Green field recomendado: camada de memória/company brain e personal AI (a camada deve ser aberta como Linux; GBrain é MIT open source)", "Não é só engenharia: times de mídia, eventos e finanças estão construindo skill files e cron jobs; uma gestora de finanças colapsou ~100 planilhas Excel num app via harness interno", "Use qualquer harness (OpenClaw como 'Ferrari', Codex como 'Honda' que cobre 90%) — os conceitos viajam para qualquer stack"]
deep_dive: "high"
deep_dive_reason: "Densa em insight arquitetural acionável e novedoso — mapeamento harness↔organograma, separação latente/determinístico, higiene de memória com proveniência e contradição — diretamente relevante a harness, context-engineering, memory-architecture e agent-fleets, mesmo carregando tom promocional do GBrain."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-stanford-cs153-frontier-systems-the-ai-native-company-how-one-founder-becomes-a--Lri2LNYtERM|Stanford CS153 Frontier Systems | The AI Native Company: How One Founder Becomes a 1000x Engineer]]", "[[extracts/youtube/ai-learning/2026-09-11-75m-founder-reveals-his-agentic-engineering-setup--QBfXiWvM0qc|$75M founder reveals his Agentic Engineering setup]]", "[[extracts/youtube/ai-learning/2026-09-11-matt-pococks-agentic-engineering-workflow-just-copy-him--nQwJVHCtDDY|Matt Pocock’s Agentic Engineering Workflow (just copy him)]]", "[[extracts/youtube/ai-learning/2026-09-11-the-golden-age-of-ai-engineering-alexander-embiricos-romain-huet-peter-steinberg--pMggiOb18tc|The Golden Age of AI Engineering — Alexander Embiricos & Romain Huet & Peter Steinberger, OpenAI]]", "[[extracts/youtube/ai-learning/2026-09-11-your-company-brain-will-leak-secrets-how-we-stopped-it-for-big-banks-tanmai-gopa--0uC6u0lJJl4|Your company brain will leak secrets: how we stopped it for big banks — Tanmai Gopal, PromptQL]]", "[[extracts/youtube/ai-learning/2026-09-11-full-workshop-setting-yourself-up-for-success-jason-liu-openai-codex--il1c1a2FufU|Full Workshop: Setting Yourself Up for Success —Jason Liu, OpenAI Codex]]", "[[extracts/youtube/ai-learning/2026-09-11-garry-tan-own-your-intelligence--eRrc1pUY5oU|Garry Tan: Own Your Intelligence]]", "[[extracts/youtube/ai-learning/2026-09-11-turn-10-994-notes-into-memory-paul-iusztin-decoding-ai-louis-francois-bouchard-t--ZRM_TfEZcIo|Turn 10,994 Notes Into Memory - Paul Iusztin, Decoding AI & Louis-François Bouchard, Towards AI]]"]
---

# Every company should have a Brain — Garry Tan, Y Combinator

## Tese
A vantagem de 400x dos engenheiros com agentes não vem dos pesos do modelo, mas de 'wire the work' — tratar harness como uma organização de skill files (funcionários de markdown) alimentada por um company brain curado (biblioteca + bibliotecário) que transforma conhecimento em ativo composto.

## Conceitos-chave
- skill file como funcionário (uma capacidade, um job escrito com clareza executável)
- tabela de resolução (resolver table) como organograma de roteamento de tarefas
- filing rules como processo interno
- trigger evals como revisões de desempenho dos skills
- workforce feita de markdown: gerenciar agentes é contratar/treinar/gerir
- separação entre espaço latente (gosto, julgamento, intenções vagas) e espaço determinístico (código); bugs nascem do cálculo no lado errado
- estado grande (ex.: arranjo de 800 assentos) não deve viver no context window
- memória de trabalho: 7±2 itens humanos vs ~1M tokens (~3 livros) do agente
- context engineering = decidir quais 'três livros' ficam abertos na mesa do agente
- company brain = biblioteca + bibliotecário; retrieval é o primitivo, curadoria é o produto
- higiene de memória: proveniência em cada fato, checagem de contradições, bibliotecário humano+agente para poda
- hot memory vs cold reference e arbitragem de fatos conflitantes
- 'skillify it': nunca fazer trabalho one-off; se pediu duas vezes, você falhou
- model quality é alugado; o brain/compounding library é propriedade
- engenheiros de empresa AI-native mantêm skills e fazem o que os skills ainda não fazem

## Ferramentas & pessoas
**Ferramentas:** Claude / Claude Code (CLAUDE.md), Codex, OpenClaw, Hermes agent, GBrain, Postgres, TypeScript, Erlang/Elixir, Excel, tests.md, X (blog posts)

**Pessoas/orgs:** Y Combinator (YC), Theo, Emergence, Retail, Startup School / Startup Battlefield

## Claims acionáveis
- Mapeie a infraestrutura de agentes para uma organização: skill file = funcionário, resolver table = organograma, filing rules = processo, trigger evals = performance review
- Ao sentar com Claude Code ou Codex você não está escrevendo software, está contratando, treinando e gerenciando uma força de trabalho de markdown
- Tenha cuidado explícito sobre onde a computação acontece: chamadas não determinísticas (julgamento, gosto, intent vago) no espaço latente; tudo mais em código determinístico
- Estado volumoso (arrays multidimensionais, storage) deve ficar fora do context window — o LLM faz só a parte humana
- Context engineering é decidir quais 'três livros' entram na memória de trabalho do agente para cada tarefa
- Retrieval/RAG é o primitivo fácil; o produto é ser digno de retrieval: o que é escrito, como é enriquecido/ligado, o que vira hot memory vs cold reference, e quem arbitra fatos conflitantes
- Trate o company brain como infraestrutura de produção: proveniência por fato, contradição checada quando novo dado colide, e bibliotecário humano+agente dedicado à poda — senão você tem um lixão com ótima busca
- Nunca faça trabalho one-off: ao terminar uma tarefa com output bom, 'skillify' — converta em skill file reutilizável no harness
- Contrate engenheiros cujo trabalho é manter skills e cobrir o que os skills ainda não executam
- O speaker reporta ~400x de output pessoal vs 2013 (~14 linhas lógicas/dia), com piso de 8x mesmo penalizando verbosidade; a diferença 2x vs 100x está na fiação do trabalho, não nos pesos do modelo
- Dados citados: 1/4 do batch W25 da YC tinha codebases 95% gerados por IA (batch mais rápido-crescente e lucrativo da história); 94 empresas YC passaram de $100M de receita; Emercence (Summer 24) 9 dígitos de ARR em 8 meses com 15 pessoas aos $15M; Retail (W24) $60M com ~40 pessoas
- Green field recomendado: camada de memória/company brain e personal AI (a camada deve ser aberta como Linux; GBrain é MIT open source)
- Não é só engenharia: times de mídia, eventos e finanças estão construindo skill files e cron jobs; uma gestora de finanças colapsou ~100 planilhas Excel num app via harness interno
- Use qualquer harness (OpenClaw como 'Ferrari', Codex como 'Honda' que cobre 90%) — os conceitos viajam para qualquer stack

> **Deep dive:** `high` — Densa em insight arquitetural acionável e novedoso — mapeamento harness↔organograma, separação latente/determinístico, higiene de memória com proveniência e contradição — diretamente relevante a harness, context-engineering, memory-architecture e agent-fleets, mesmo carregando tom promocional do GBrain.
