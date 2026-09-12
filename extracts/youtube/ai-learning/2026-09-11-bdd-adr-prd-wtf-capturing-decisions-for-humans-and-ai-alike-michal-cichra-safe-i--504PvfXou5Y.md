---
title: "BDD, ADR, PRD, WTF: Capturing Decisions for Humans and AI Alike — Michal Cichra, Safe Intelligence"
type: "extract"
source: "youtube"
video_id: "504PvfXou5Y"
url: "https://www.youtube.com/watch?v=504PvfXou5Y"
channel: "AI Engineer"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-bdd-adr-prd-wtf-capturing-decisions-for-humans-and-ai-alike-michal-cichra-safe-i--504PvfXou5Y.txt]]"
tags: ["spec-driven-development", "harness", "agent-loop", "context-engineering", "context-management", "testes-qa", "code-review", "knowledge-management", "gate-design", "arquitetura", "agent-tooling", "decision-discipline", "verification", "process"]
thesis: "Capturar decisões em documentos legíveis e executáveis (ADR, PRD, BDD/Cucumber, design systems) e reforçá-las automaticamente com um harness de git hooks, CI, linters e skills mantém humanos e agentes consistentes ao longo de sessões longas."
concepts: ["ADR (Architecture Decision Record): registra o porquê e como enforce a decisão", "PRD (Product Requirements Document): documento leve com problema, objetivo e jornada do usuário", "BDD (Behavior-Driven Development) como especificações legíveis e executáveis", "Cucumber e o fechamento do ciclo que o spec-driven development deixa aberto", "Analogia dos macacos: humanos e LLMs sofrem de contexto limitado e perda de memória", "Design system e pattern library com regras explícitas (ex.: um único botão primário por página)", "Harness de reforço: git hooks + CI + linters executando as mesmas tarefas", "Skills como foco do loop genérico do agente (ADR, PRD, UI, testes)", "Enforcement de arquitetura via linting de imports entre módulos", "Prevenção estrutural de N+1 queries proibindo acesso ao banco em templates e na suíte e2e", "Compactação de contexto como rotina suportável (20-50 compacts por sessão)", "Code review deslocado de estilo para conceitos de alto nível"]
tools: ["Cucumber", "Git hooks", "CI (integração contínua)", "Linters", "Code coverage / seleção de testes por mudança de arquivos", "Spec 27 (produto da Safe Intelligence para testar agentes)", "Design system / pattern library com previews e snippets"]
people: ["Mikuel (palestrante)", "Safe Intelligence", "Microsoft", "Red Hat"]
claims: ["ADRs devem registrar por que uma decisão existe e como é enforce (ex.: separação em camadas reforçada por linting de imports) para que o agente encontre a razão e como corrigir violações", "BDD com Cucumber valida se o produto realmente adere à spec, fechando a lacuna do spec-driven development cujos documentos markdown não são verificados", "Design systems e pattern libraries com regras, componentes, previews e snippets continuam sendo o caminho para UIs consistentes geradas por agentes", "Reviews de código não devem mais discutir estilo: regras mecânicas (formatação, tipos, duplicação, arquitetura) são automatizadas em git hooks espelhados no CI, pegando agentes que tentem pular tarefas", "'O que você não consegue encontrar, não consegue enforce': proibir via linting que a suíte BDD e2e e templates acessem módulos de banco elimina N+1 queries por prevenção e não por correção repetida", "O loop do agente é genérico (trabalhar, commitar, receber feedback, ler o documento linkado, iterar); skills diferentes mudam o foco do loop sem mudar o loop (UI itera no navegador pulando checks; test skill roda só testes relevantes via cobertura e arquivos alterados)", "Sessões com 20-50 compactações de contexto funcionam porque o importante sobrevive e o agente re-busca informações quando precisa; o objetivo é autonomia multi-hora sob regras definidas", "PRDs leves servem tanto para agentes quanto para humanos que esquecerão o porquê de uma feature semanas depois"]
deep_dive: "high"
deep_dive_reason: "Apresenta densidade alta de práticas acionáveis e arquiteturais (ADRs enforce via linting de imports, BDD/Cucumber como validação executável de specs, harness com git hooks espelhados no CI, skills focando o loop, dados reais de compactação de contexto), com novidade em reaplicar técnicas clássicas a loops de agentes e relevância direta a harness, context-engineering e spec-driven development."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-ex-nasa-dev-reveals-his-agentic-engineering-workflow--xgkjtF89-44|Ex-NASA dev reveals his Agentic Engineering Workflow]]", "[[extracts/youtube/ai-learning/2026-09-11-no-vibes-allowed-solving-hard-problems-in-complex-codebases-dex-horthy-humanlaye--rmvDxxNubIg|No Vibes Allowed: Solving Hard Problems in Complex Codebases – Dex Horthy, HumanLayer]]", "[[extracts/youtube/ai-learning/2026-09-11-ryan-lopopolo-harness-engineering-how-to-build-software-when-humans-steer-and-ag--c8bE0cj7vHY|Ryan Lopopolo - Harness Engineering: How to Build Software When Humans Steer and Agents Execute]]", "[[extracts/youtube/ai-learning/2026-09-11-full-walkthrough-workflow-for-ai-coding-matt-pocock---QFHIoCo-Ko|Full Walkthrough: Workflow for AI Coding — Matt Pocock]]", "[[extracts/youtube/ai-learning/2026-09-11-the-multi-agent-architecture-that-actually-ships-luke-alvoeiro-factory--ow1we5PzK-o|The Multi-Agent Architecture That Actually Ships — Luke Alvoeiro, Factory]]", "[[extracts/youtube/ai-learning/2026-09-11-how-i-deleted-95-of-my-agent-skills-and-got-better-results-nick-nisi-workos--vy7o1g2iHY8|How I deleted 95% of my agent skills and got better results — Nick Nisi, WorkOS]]", "[[extracts/youtube/ai-learning/2026-09-11-the-end-of-the-static-screen-architecting-intent-driven-ux-gus-iwanaga-commercet--QrMcNe2jjt8|The End of the Static Screen: Architecting Intent-Driven UX — Gus Iwanaga, commercetools]]", "[[extracts/youtube/ai-learning/2026-09-11-i-stopped-using-grill-me-for-coding-heres-what-i-use-instead--6BB6exR8Zd8|I stopped using /grill-me for coding. Here’s what I use instead:]]"]
---

# BDD, ADR, PRD, WTF: Capturing Decisions for Humans and AI Alike — Michal Cichra, Safe Intelligence

## Tese
Capturar decisões em documentos legíveis e executáveis (ADR, PRD, BDD/Cucumber, design systems) e reforçá-las automaticamente com um harness de git hooks, CI, linters e skills mantém humanos e agentes consistentes ao longo de sessões longas.

## Conceitos-chave
- ADR (Architecture Decision Record): registra o porquê e como enforce a decisão
- PRD (Product Requirements Document): documento leve com problema, objetivo e jornada do usuário
- BDD (Behavior-Driven Development) como especificações legíveis e executáveis
- Cucumber e o fechamento do ciclo que o spec-driven development deixa aberto
- Analogia dos macacos: humanos e LLMs sofrem de contexto limitado e perda de memória
- Design system e pattern library com regras explícitas (ex.: um único botão primário por página)
- Harness de reforço: git hooks + CI + linters executando as mesmas tarefas
- Skills como foco do loop genérico do agente (ADR, PRD, UI, testes)
- Enforcement de arquitetura via linting de imports entre módulos
- Prevenção estrutural de N+1 queries proibindo acesso ao banco em templates e na suíte e2e
- Compactação de contexto como rotina suportável (20-50 compacts por sessão)
- Code review deslocado de estilo para conceitos de alto nível

## Ferramentas & pessoas
**Ferramentas:** Cucumber, Git hooks, CI (integração contínua), Linters, Code coverage / seleção de testes por mudança de arquivos, Spec 27 (produto da Safe Intelligence para testar agentes), Design system / pattern library com previews e snippets

**Pessoas/orgs:** Mikuel (palestrante), Safe Intelligence, Microsoft, Red Hat

## Claims acionáveis
- ADRs devem registrar por que uma decisão existe e como é enforce (ex.: separação em camadas reforçada por linting de imports) para que o agente encontre a razão e como corrigir violações
- BDD com Cucumber valida se o produto realmente adere à spec, fechando a lacuna do spec-driven development cujos documentos markdown não são verificados
- Design systems e pattern libraries com regras, componentes, previews e snippets continuam sendo o caminho para UIs consistentes geradas por agentes
- Reviews de código não devem mais discutir estilo: regras mecânicas (formatação, tipos, duplicação, arquitetura) são automatizadas em git hooks espelhados no CI, pegando agentes que tentem pular tarefas
- 'O que você não consegue encontrar, não consegue enforce': proibir via linting que a suíte BDD e2e e templates acessem módulos de banco elimina N+1 queries por prevenção e não por correção repetida
- O loop do agente é genérico (trabalhar, commitar, receber feedback, ler o documento linkado, iterar); skills diferentes mudam o foco do loop sem mudar o loop (UI itera no navegador pulando checks; test skill roda só testes relevantes via cobertura e arquivos alterados)
- Sessões com 20-50 compactações de contexto funcionam porque o importante sobrevive e o agente re-busca informações quando precisa; o objetivo é autonomia multi-hora sob regras definidas
- PRDs leves servem tanto para agentes quanto para humanos que esquecerão o porquê de uma feature semanas depois

> **Deep dive:** `high` — Apresenta densidade alta de práticas acionáveis e arquiteturais (ADRs enforce via linting de imports, BDD/Cucumber como validação executável de specs, harness com git hooks espelhados no CI, skills focando o loop, dados reais de compactação de contexto), com novidade em reaplicar técnicas clássicas a loops de agentes e relevância direta a harness, context-engineering e spec-driven development.
