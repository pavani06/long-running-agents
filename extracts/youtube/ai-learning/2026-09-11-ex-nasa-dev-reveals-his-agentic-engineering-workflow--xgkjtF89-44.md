---
title: "Ex-NASA dev reveals his Agentic Engineering Workflow"
type: "extract"
source: "youtube"
video_id: "xgkjtF89-44"
url: "https://www.youtube.com/watch?v=xgkjtF89-44"
channel: "David Ondrej"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-ex-nasa-dev-reveals-his-agentic-engineering-workflow--xgkjtF89-44.txt]]"
tags: ["context-engineering", "evals", "agentic-coding", "spec-driven-development", "12-factor-agents", "token-budgeting", "code-review", "testes-qa", "gate-design", "verification", "decision-discipline", "knowledge-management", "arquitetura", "agent-tooling", "monitoramento"]
thesis: "Agentes de código resolvem problemas muito bem mas não escrevem código manutenível sem o humano no loop — porque o RL não tem um 'oracle' rápido para qualidade de design — então engenheiros devem investir em program design antecipado (produto mensurável, arquitetura, call stack, vertical slices) e em context engineering, em vez de confiar em benchmarks ou em fábricas 'lights-off'."
concepts: ["program design", "context engineering (termo cunhado por Dexter)", "software factory / fábrica de agentes autônomos", "lights-off factory (e sua falência)", "vertical slices / tracer bullets", "oracle problem no reinforcement learning", "slop code e ausência de penalidade por design ruim em benchmarks", "LLM-as-judge (qualidade e equivalência funcional)", "back pressure via outputs mensuráveis (ex.: /goal)", "working backwards: PRD/blog post antes do código", "definição de types e assinaturas de métodos para aprovação humana rápida", "own your context window (12 Factor Agents)", "eficiência de tokens (XML vs JSON) e decisões em sessões de contexto barato", "routing de incidentes e tickets de suporte direto para agentes (acordar com pull request em vez de alerta)", "contexto determinístico via hooks (puxar issues do Sentry sem gastar inferência)", "documentação ADR e /doc/external dentro do codebase", "quiz do agente ao humano para manter domínio do codebase", "teste de testes: rodar testes do modelo contra código pré-patch"]
tools: ["SWE-bench / SWE-bench multilingual", "Codex", "Claude Opus", "GLM 5.2", "Fable / modelos 5.6-6", "Cursor sandbox", "PostHog", "Replay Vision", "Render.com", "Vercel (cron jobs)", "GitHub Actions", "Jira", "Linear", "Sentry", "Mermaid", "Riptide", "Human Layer", "MCP servers", "12 Factor Agents (paper)"]
people: ["Dexter (Dex)", "David Andre", "Calvin French-Owen", "Dylan Mroy (Cloudflare)", "Victor Talin", "Matt PCO", "Jake Nations (Netflix)", "Cognition", "Human Layer", "Cloudflare", "PostHog", "Anthropic", "Amazon"]
claims: ["Se ~30-50% dos incidentes/tarefas puderem ser 'oneshottados' por agentes, a produtividade praticamente dobra — automatize a triagem de incidentes e suporte direto para a fábrica de agentes", "Escreva o PRD/blog post (estilo Amazon working backwards) e mockups HTML antes de qualquer código, definindo como medir sucesso com números de negócio (conversão, receita)", "Faça as decisões de arquitetura e program design (call stack, colocação de arquivos, types e assinaturas) em sessões de contexto barato no início da janela, porque mudar de rumo após milhares de linhas escritas é muito mais caro", "Defina tipos e assinaturas de métodos em blocos fáceis de o humano validar, sem entrar em detalhes de implementação", "Construa em vertical slices ponta a ponta (mock API → front → wiring → migração → lógica → error handling), pois modelos default para construção horizontal sem pontos de teste intermediários e nunca fazem isso sozinhos", "Não adote a fábrica 'lights-off' (não ler código): a experiência de julho/2025 mostrou semanas de miséria debuggando slop code quando um bug excede a capacidade dos modelos", "Mudanças pequenas e previsíveis podem ir direto para produção com base no conhecimento calibrado do comportamento do agente; quando inseguro, revise com um segundo modelo frontier e teste mais", "Cross-review com outro frontier model (ex.: Codex revisando Claude) levanta o piso, mas 'se o modelo soubesse o que é bom código, o escreveria de primeira' — juízes LLM de qualidade só vão até certo ponto", "Benchmarks tipo SWE-bench não penalizam slop: mantenabilidade não tem oracle rápido pois o custo de arquitetura ruim se manifesta em semanas/meses, inviabilizando backpropagation no treino", "Desconfie de benchmarks one-shot; confie mais em benchmarks que entregam um roadmap de ~20 features sequencialmente, sem o modelo conhecer os próximos requisitos", "Truque da Cognition para detectar testes vazios: rodar os testes escritos pelo modelo contra o código pré-patch — se não falharem lá, não testam nada", "Máximo leverage: extrair 'taste' humano em regras explícitas, checagens determinísticas e CI/CD mais robusto (linters, monitoramento de complexidade, regression testing por modo de falha)", "Coloque todo contexto no filesystem (ADRs, /doc/external com setup de provedores/env) e use hooks determinísticos (ex.: puxar últimas 10 issues do Sentry a cada sessão) — isso é 'de graça' em inferência e poupa atenção do modelo", "Trate a janela de contexto como o único primitivo: modele-a como estado do programa, garanta informação correta e completa, e minimize tokens (XML é mais eficiente que JSON)", "Ensine o agente a educar o humano: quizzes sobre o estado do codebase, visualizações HTML e desaceleração proposital quando o humano perde o domínio", "Diferencie regime: pré-PMF pode vibe-code e mover rápido; com clientes enterprise/fintech, invista no pipeline completo de design e verificação"]
deep_dive: "high"
deep_dive_reason: "Densidade alta de insight acionável e arquitetural (program design em 4 estágios, vertical slices, hooks determinísticos, técnicas de benchmark da Cognition) combinada com novidade e relevância direta para harness, context-engineering, evals e governança de fábricas de agentes."
---

# Ex-NASA dev reveals his Agentic Engineering Workflow

## Tese
Agentes de código resolvem problemas muito bem mas não escrevem código manutenível sem o humano no loop — porque o RL não tem um 'oracle' rápido para qualidade de design — então engenheiros devem investir em program design antecipado (produto mensurável, arquitetura, call stack, vertical slices) e em context engineering, em vez de confiar em benchmarks ou em fábricas 'lights-off'.

## Conceitos-chave
- program design
- context engineering (termo cunhado por Dexter)
- software factory / fábrica de agentes autônomos
- lights-off factory (e sua falência)
- vertical slices / tracer bullets
- oracle problem no reinforcement learning
- slop code e ausência de penalidade por design ruim em benchmarks
- LLM-as-judge (qualidade e equivalência funcional)
- back pressure via outputs mensuráveis (ex.: /goal)
- working backwards: PRD/blog post antes do código
- definição de types e assinaturas de métodos para aprovação humana rápida
- own your context window (12 Factor Agents)
- eficiência de tokens (XML vs JSON) e decisões em sessões de contexto barato
- routing de incidentes e tickets de suporte direto para agentes (acordar com pull request em vez de alerta)
- contexto determinístico via hooks (puxar issues do Sentry sem gastar inferência)
- documentação ADR e /doc/external dentro do codebase
- quiz do agente ao humano para manter domínio do codebase
- teste de testes: rodar testes do modelo contra código pré-patch

## Ferramentas & pessoas
**Ferramentas:** SWE-bench / SWE-bench multilingual, Codex, Claude Opus, GLM 5.2, Fable / modelos 5.6-6, Cursor sandbox, PostHog, Replay Vision, Render.com, Vercel (cron jobs), GitHub Actions, Jira, Linear, Sentry, Mermaid, Riptide, Human Layer, MCP servers, 12 Factor Agents (paper)

**Pessoas/orgs:** Dexter (Dex), David Andre, Calvin French-Owen, Dylan Mroy (Cloudflare), Victor Talin, Matt PCO, Jake Nations (Netflix), Cognition, Human Layer, Cloudflare, PostHog, Anthropic, Amazon

## Claims acionáveis
- Se ~30-50% dos incidentes/tarefas puderem ser 'oneshottados' por agentes, a produtividade praticamente dobra — automatize a triagem de incidentes e suporte direto para a fábrica de agentes
- Escreva o PRD/blog post (estilo Amazon working backwards) e mockups HTML antes de qualquer código, definindo como medir sucesso com números de negócio (conversão, receita)
- Faça as decisões de arquitetura e program design (call stack, colocação de arquivos, types e assinaturas) em sessões de contexto barato no início da janela, porque mudar de rumo após milhares de linhas escritas é muito mais caro
- Defina tipos e assinaturas de métodos em blocos fáceis de o humano validar, sem entrar em detalhes de implementação
- Construa em vertical slices ponta a ponta (mock API → front → wiring → migração → lógica → error handling), pois modelos default para construção horizontal sem pontos de teste intermediários e nunca fazem isso sozinhos
- Não adote a fábrica 'lights-off' (não ler código): a experiência de julho/2025 mostrou semanas de miséria debuggando slop code quando um bug excede a capacidade dos modelos
- Mudanças pequenas e previsíveis podem ir direto para produção com base no conhecimento calibrado do comportamento do agente; quando inseguro, revise com um segundo modelo frontier e teste mais
- Cross-review com outro frontier model (ex.: Codex revisando Claude) levanta o piso, mas 'se o modelo soubesse o que é bom código, o escreveria de primeira' — juízes LLM de qualidade só vão até certo ponto
- Benchmarks tipo SWE-bench não penalizam slop: mantenabilidade não tem oracle rápido pois o custo de arquitetura ruim se manifesta em semanas/meses, inviabilizando backpropagation no treino
- Desconfie de benchmarks one-shot; confie mais em benchmarks que entregam um roadmap de ~20 features sequencialmente, sem o modelo conhecer os próximos requisitos
- Truque da Cognition para detectar testes vazios: rodar os testes escritos pelo modelo contra o código pré-patch — se não falharem lá, não testam nada
- Máximo leverage: extrair 'taste' humano em regras explícitas, checagens determinísticas e CI/CD mais robusto (linters, monitoramento de complexidade, regression testing por modo de falha)
- Coloque todo contexto no filesystem (ADRs, /doc/external com setup de provedores/env) e use hooks determinísticos (ex.: puxar últimas 10 issues do Sentry a cada sessão) — isso é 'de graça' em inferência e poupa atenção do modelo
- Trate a janela de contexto como o único primitivo: modele-a como estado do programa, garanta informação correta e completa, e minimize tokens (XML é mais eficiente que JSON)
- Ensine o agente a educar o humano: quizzes sobre o estado do codebase, visualizações HTML e desaceleração proposital quando o humano perde o domínio
- Diferencie regime: pré-PMF pode vibe-code e mover rápido; com clientes enterprise/fintech, invista no pipeline completo de design e verificação

> **Deep dive:** `high` — Densidade alta de insight acionável e arquitetural (program design em 4 estágios, vertical slices, hooks determinísticos, técnicas de benchmark da Cognition) combinada com novidade e relevância direta para harness, context-engineering, evals e governança de fábricas de agentes.
