---
title: "The Multi-Agent Architecture That Actually Ships — Luke Alvoeiro, Factory"
type: "extract"
source: "youtube"
video_id: "ow1we5PzK-o"
url: "https://www.youtube.com/watch?v=ow1we5PzK-o"
channel: "AI Engineer"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-the-multi-agent-architecture-that-actually-ships-luke-alvoeiro-factory--ow1we5PzK-o.txt]]"
tags: ["agent-fleets", "agentes-orquestracao", "agentic-coding", "multi-agent", "harness", "arquitetura", "context-engineering", "evals", "verification", "gate-design", "model-selection", "error-handling", "state", "testes-qa", "token-budgeting", "monitoramento", "production", "process"]
thesis: "O gargalo da engenharia de software deixou de ser inteligência e passou a ser atenção humana, e sistemas multi-agente como as Missions da Factory — combinando delegação, criador-verificador, broadcast e negociação com contratos de validação pré-código, handoffs estruturados e seleção de modelo por papel — podem executar tarefas por dias com supervisão mínima."
concepts: ["Bottleneck de atenção humana vs. inteligência dos modelos", "Taxonomia de cinco frameworks multi-agente: delegação, criador-verificador, comunicação direta, negociação, broadcast", "Arquitetura de três papéis: orquestrador, workers e validadores", "Contrato de validação definido no planejamento antes de qualquer código, com centenas de asserções por feature", "Testes escritos após a implementação confirmam decisões em vez de capturar bugs", "Validação adversarial por design: validadores com contexto fresco que nunca viram o código", "Scrutiny validator (testes, type check, lint, code review por feature) e user testing validator (interage com a aplicação viva via computer use)", "Handoffs estruturados: concluído, pendente, comandos executados, exit codes, issues, aderência a procedimentos", "Autocorreção em fronteiras de milestone", "Execução serial de features com paralelização apenas em operações read-only (busca, pesquisa de APIs)", "Seleção de modelo por papel: raciocínio lento para planejamento, fluidez para implementação, seguimento preciso de instruções para validação", "'Droid whispering': modelar mentalmente como diferentes LLMs interagem e onde falham", "Validação com provedor de modelo diferente para evitar viés de dados de treinamento", "Estrutura compensa modelos não-frontier (open-weight viável com contratos e checkpoints)", "Bitter lesson: orquestração em ~700 linhas de prompts e skills, não state machine hard-coded", "Orquestração dirigida por prompts/skills melhora automaticamente com cada novo modelo", "Mission Control para supervisão assíncrona de missões multidiárias", "Missões como ecossistema de agentes com handoffs estruturados e estado compartilhado", "Missão mais longa: 16 dias, com estimativa de 30 dias"]
tools: ["Goose", "Factory", "Missions", "Mission Control", "Open Droid (Droid)", "git", "AGENTS.md", "Skills", "prompt caching", "computer use"]
people: ["Luke (palestrante)", "Block", "Factory", "Agentic AI Foundation (Linux Foundation)", "Theo (engenheiro do protótipo de Missions)"]
claims: ["Escreva o contrato de validação (asserções de correção) durante o planejamento, antes de qualquer implementação, para evitar que testes apenas confirmem decisões", "Mantenha validadores com contexto fresco e sem exposição ao código para tornar a validação adversarial por design", "Valide comportamento end-to-end, não só código: faça um agente QA subir a aplicação e interagir com ela via computer use", "Execute features serialmente com um único worker ativo e paralelize somente operações read-only; paralelismo total gera conflitos, duplicação e decisões arquiteturais inconsistentes que anulam o ganho de velocidade", "Force handoffs estruturados (comandos, exit codes, issues, pendências) para que o sistema se auto-corrija em fronteiras de milestone", "Escolha deliberadamente qual modelo ocupa cada papel (planejamento, implementação, validação); nenhum provedor é o melhor nos três", "Considere usar um provedor de modelo diferente na validação para eliminar viés de treinamento compartilhado", "Implemente a orquestração como prompts e skills editáveis (~700 linhas), mantendo apenas lógica determinística fina para bookkeeping, para que o sistema melhore com cada lançamento de modelo", "Use prompt caching agressivamente para viabilizar economicamente missões longas", "Contratos de validação e checkpoints de milestone permitem rodar o sistema com sucesso mesmo com modelos open-weight não-frontier", "Instrumente a observação com uma visão dedicada (Mission Control) mostrando progresso, orçamento queimado e resumos de handoff", "Espere que validação quase nunca passe de primeira: crie features de follow-up automaticamente como parte do loop de QA"]
deep_dive: "high"
deep_dive_reason: "Densidade alta de detalhe arquitetural e acionável — taxonomia de padrões multi-agente, contratos de validação pré-implementação, execução serial com paralelismo seletivo, seleção de modelo por papel e orquestração via prompts — com métricas de produção de missões de 16 dias."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-ex-nasa-dev-reveals-his-agentic-engineering-workflow--xgkjtF89-44|Ex-NASA dev reveals his Agentic Engineering Workflow]]", "[[extracts/youtube/ai-learning/2026-09-11-l8-principal-s-agentic-engineering-setup-just-copy-him--8ZgpAXe5V5w|L8 Principal's Agentic Engineering Setup (just copy him)]]", "[[extracts/youtube/ai-learning/2026-09-11-how-i-deleted-95-of-my-agent-skills-and-got-better-results-nick-nisi-workos--vy7o1g2iHY8|How I deleted 95% of my agent skills and got better results — Nick Nisi, WorkOS]]", "[[extracts/youtube/ai-learning/2026-09-11-agentic-engineering-explained-by-a-10x-developer--FU5_kpTAVDo|Agentic Engineering, explained by a 10x developer]]", "[[extracts/youtube/ai-learning/2026-09-11-harness-engineering-is-not-enough-why-software-factories-fail-dex-horthy-humanla--Ib5GBkD555M|Harness Engineering is not Enough: Why Software Factories Fail — Dex Horthy, HumanLayer]]", "[[extracts/youtube/ai-learning/2026-09-11-anthropic-workshop-build-agents-that-run-for-hours-ash-prabaker-andrew-wilson--mR-WAvEPRwE|Anthropic Workshop: Build Agents That Run for Hours — Ash Prabaker & Andrew Wilson]]", "[[extracts/youtube/ai-learning/2026-09-11-bdd-adr-prd-wtf-capturing-decisions-for-humans-and-ai-alike-michal-cichra-safe-i--504PvfXou5Y|BDD, ADR, PRD, WTF: Capturing Decisions for Humans and AI Alike — Michal Cichra, Safe Intelligence]]", "[[extracts/youtube/ai-learning/2026-09-11-how-valkey-uses-ai-agents-without-losing-control-madelyn-olson-aws--SrvKmhJRlKI|How Valkey Uses AI Agents Without Losing Control | Madelyn Olson, AWS]]", "[[extracts/youtube/ai-learning/2026-09-11-why-we-killed-our-multi-agent-pipeline-subbiah-sethuraman-and-abhilash-asokan-zs--u6jJcIFDLE4|Why We Killed Our Multi-Agent Pipeline — Subbiah Sethuraman and Abhilash Asokan, ZS Associates]]", "[[extracts/youtube/ai-learning/2026-09-11-building-closed-loop-evals-for-a-multimodal-agent-at-scale-soumya-gupta-jai-chop--31GUkCBD-Uc|Building Closed-Loop Evals for a Multimodal Agent at Scale — Soumya Gupta & Jai Chopra, Uber]]", "[[extracts/youtube/ai-learning/2026-09-11-hermes-deepseek-4-minimax-2-7-multi-model-coding-on-a-zimaboard---3MPnUGqa68|Hermes + DeepSeek 4 + MiniMax 2.7: Multi-Model Coding on a ZimaBoard]]"]
---

# The Multi-Agent Architecture That Actually Ships — Luke Alvoeiro, Factory

## Tese
O gargalo da engenharia de software deixou de ser inteligência e passou a ser atenção humana, e sistemas multi-agente como as Missions da Factory — combinando delegação, criador-verificador, broadcast e negociação com contratos de validação pré-código, handoffs estruturados e seleção de modelo por papel — podem executar tarefas por dias com supervisão mínima.

## Conceitos-chave
- Bottleneck de atenção humana vs. inteligência dos modelos
- Taxonomia de cinco frameworks multi-agente: delegação, criador-verificador, comunicação direta, negociação, broadcast
- Arquitetura de três papéis: orquestrador, workers e validadores
- Contrato de validação definido no planejamento antes de qualquer código, com centenas de asserções por feature
- Testes escritos após a implementação confirmam decisões em vez de capturar bugs
- Validação adversarial por design: validadores com contexto fresco que nunca viram o código
- Scrutiny validator (testes, type check, lint, code review por feature) e user testing validator (interage com a aplicação viva via computer use)
- Handoffs estruturados: concluído, pendente, comandos executados, exit codes, issues, aderência a procedimentos
- Autocorreção em fronteiras de milestone
- Execução serial de features com paralelização apenas em operações read-only (busca, pesquisa de APIs)
- Seleção de modelo por papel: raciocínio lento para planejamento, fluidez para implementação, seguimento preciso de instruções para validação
- 'Droid whispering': modelar mentalmente como diferentes LLMs interagem e onde falham
- Validação com provedor de modelo diferente para evitar viés de dados de treinamento
- Estrutura compensa modelos não-frontier (open-weight viável com contratos e checkpoints)
- Bitter lesson: orquestração em ~700 linhas de prompts e skills, não state machine hard-coded
- Orquestração dirigida por prompts/skills melhora automaticamente com cada novo modelo
- Mission Control para supervisão assíncrona de missões multidiárias
- Missões como ecossistema de agentes com handoffs estruturados e estado compartilhado
- Missão mais longa: 16 dias, com estimativa de 30 dias

## Ferramentas & pessoas
**Ferramentas:** Goose, Factory, Missions, Mission Control, Open Droid (Droid), git, AGENTS.md, Skills, prompt caching, computer use

**Pessoas/orgs:** Luke (palestrante), Block, Factory, Agentic AI Foundation (Linux Foundation), Theo (engenheiro do protótipo de Missions)

## Claims acionáveis
- Escreva o contrato de validação (asserções de correção) durante o planejamento, antes de qualquer implementação, para evitar que testes apenas confirmem decisões
- Mantenha validadores com contexto fresco e sem exposição ao código para tornar a validação adversarial por design
- Valide comportamento end-to-end, não só código: faça um agente QA subir a aplicação e interagir com ela via computer use
- Execute features serialmente com um único worker ativo e paralelize somente operações read-only; paralelismo total gera conflitos, duplicação e decisões arquiteturais inconsistentes que anulam o ganho de velocidade
- Force handoffs estruturados (comandos, exit codes, issues, pendências) para que o sistema se auto-corrija em fronteiras de milestone
- Escolha deliberadamente qual modelo ocupa cada papel (planejamento, implementação, validação); nenhum provedor é o melhor nos três
- Considere usar um provedor de modelo diferente na validação para eliminar viés de treinamento compartilhado
- Implemente a orquestração como prompts e skills editáveis (~700 linhas), mantendo apenas lógica determinística fina para bookkeeping, para que o sistema melhore com cada lançamento de modelo
- Use prompt caching agressivamente para viabilizar economicamente missões longas
- Contratos de validação e checkpoints de milestone permitem rodar o sistema com sucesso mesmo com modelos open-weight não-frontier
- Instrumente a observação com uma visão dedicada (Mission Control) mostrando progresso, orçamento queimado e resumos de handoff
- Espere que validação quase nunca passe de primeira: crie features de follow-up automaticamente como parte do loop de QA

> **Deep dive:** `high` — Densidade alta de detalhe arquitetural e acionável — taxonomia de padrões multi-agente, contratos de validação pré-implementação, execução serial com paralelismo seletivo, seleção de modelo por papel e orquestração via prompts — com métricas de produção de missões de 16 dias.
