---
title: "Pstack Is Agent Overkill. Use It Anyway!"
type: "extract"
source: "youtube"
video_id: "lUhXa8GiXns"
url: "https://www.youtube.com/watch?v=lUhXa8GiXns"
channel: "Rob Shocks"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-pstack-is-agent-overkill-use-it-anyway--lUhXa8GiXns.txt]]"
tags: ["agent-tooling", "agentic-coding", "multi-agent", "harness", "verification", "testes-qa", "code-review", "context-management", "token-budgeting", "cross-session", "model-selection"]
thesis: "O Pstack de Lauren Tan mostra como um conjunto curado de skills, playbooks e princípios (roteamento por potato mode, arena/swarm paralelo, verificação roteirizada e disciplina do contexto) transforma agentes de codificação em engenheiros seniores de alto custo em tokens, porém muito mais confiáveis, sob a filosofia de que 'a melhor spec é o código'."
concepts: ["potato mode como roteador de skills", "skills vs playbooks vs princípios", "arena: múltiplos modelos competindo no mesmo problema com graft/reject das melhores partes", "swarm: workers paralelos com fatias distintas e agregação em relatório único", "fearless parallelism entre feature branches e worktrees", "TDD-first (testes unitários antes de prosseguir)", "why-skill: arqueologia de decisões via MCPs/CLIs (ADRs)", "recall: retomada de projeto entre sessões escaneando transcripts e MCPs", "interrogate: code review por múltiplos modelos contra os padrões", "create-verification e maintain-verification: scripts que provam comportamento real e são mantidos em sincronia", "unslop: remoção de chavões típicos de IA (delve, crucial, em dashes)", "bro skill: reformulação da última mensagem em linguagem simples", "show me your work: rastreabilidade do pipeline do agente (probe → frame → scaffold → arena → redesign → verificação → auditoria)", "design changes forced by reality: planos quebram ao contato com a implementação", "laziness protocol: deletar código e buscar a menor mudança possível", "redesign from first principles ao adicionar features", "minimizar reader load: menos abstrações e PRs menores", "exhaust the design space: explorar variações antes de commitar o design", "build a lever: automatizar ações manuais repetidas em CLI/script", "guard the context window: delegar a subagentes com janelas próprias reportando ao thread central", "never block the human", "verde nos testes não equivale a prova de funcionamento do artefato real", "ausência deliberada de skill de planejamento (anti spec-driven)", "gerenciador de skills跨 agentes (Molton Base)"]
tools: ["Pstack", "Potato Mode", "Molton Base", "Cursor", "Claude Code", "Codex", "OpenCode", "OpenRouter", "PostHog", "Slack", "Sentry", "Notion", "Linear", "Fable 5.1", "Claude", "GPT", "Grok", "Claude Opus 5", "BMAD", "superpowers", "OpenSpec", "Cadream (geração de vídeo, conforme transcrito)"]
people: ["Lauren Tan", "Netflix", "React core team", "SpaceX", "Cursor", "Theo", "Michael Dener", "Rob Shocks", "Switch Dimension (canal/curso)"]
claims: ["Instale o Pstack no Cursor via /addplugin pstack; para Claude Code, Codex e OpenCode use o port não-oficial de Michael Dener nos marketplaces de plugins", "Potato mode é um roteador que decide qual dos 20+ skills/playbooks invocar primeiro para um prompt", "O Pstack não tem skill de planejamento de propósito — é desenhado para codebases estabelecidos, com a tese de que 'a melhor spec é o código'", "Arena roda 3-4 modelos (ex.: Claude, GPT, Grok, Opus) no mesmo problema e enxerta as melhores partes num commit final, decidindo graft ou reject com base no que os subagentes aprenderam", "Swarm distribui fatias diferentes do problema a workers paralelos e agrega tudo num relatório sem sobreposições (afirmação grande ainda não validada pelo autor do vídeo)", "O why-skill consulta MCPs e CLIs do projeto (PostHog para produto, Slack para discussões, Sentry para logs) para reconstruir o registro de decisões/ADRs de por que algo foi feito", "O recall-skill retoma projetos parados escaneando todos os transcripts e consultando Notion/Linear/PostHog para definir próximos passos", "O interrogate-skill faz 2-3 modelos revisarem o código contra os padrões do projeto, com alto consumo de tokens em troca de máxima qualidade", "O create-verification-skill gera scripts de verificação do comportamento real do app — essencial para agentes não-determinísticos — e o maintain-verification-skill atualiza verificadores que divergiram do desenvolvimento", "O unslop-skill remove frases-sinal de IA (pivotal moment, crucial, delve, em dashes) de textos gerados por agentes", "O bro-skill reexplica a última mensagem do agente em linguagem simples, útil ao operar ~10 agentes em paralelo", "O show me your work expôs o pipeline real: probing de viabilidade, enquadramento de requisitos/constraints, scaffolding, arena, redesign forçado pela realidade, verificação e auditoria — que capturou 3 afirmações alucinadas pelo próprio agente", "Aplique o laziness protocol: ao refatorar, prefira deletar código e buscar a menor mudança que resolve, gerando mais manutenibilidade", "Ao adicionar features, redesenhe from first principles — como se o recurso existisse desde o dia 1 — mesmo que isso remova estruturas existentes", "Minimize reader load: menos abstrações e módulos dispersos para evitar PRs gigantes e disjuntos de agentes", "Exhaust the design space: gere variações concorrentes (design mode) antes de escolher e comitar o design", "Build a lever: converta ações manuais repetidas com o agente em CLI/script reutilizável (ex.: CLI própria sobre a API do OpenRouter com um único API key para texto, imagem, vídeo e voz)", "Guarde o contexto central: offload de fatias a subagentes com janelas próprias que reportam de volta ao thread principal, e nunca bloqueie o humano", "Testes verdes/compilação não provam funcionamento: verifique o artefato real com scripts, computer use ou testes end-to-end", "Benchmark anedótico do autor: Fable 5.1 sem skills concluiu o projeto em ~30min vs ~1h com Pstack, com resultado substancialmente melhor porém muito mais caro — reserve o Pstack para recursos críticos, não para mudanças triviais de UI"]
deep_dive: "medium"
deep_dive_reason: "Há boa densidade de padrões acionáveis e relevantes (arena/swarm, verificação roteirizada, guarda de contexto, retomada cross-session), mas é uma walkthrough de segunda mão de skills de terceiros, com segmentos promocionais (OpenRouter, curso) e afirmações centrais admitidamente não verificadas pelo próprio autor."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-so-i-tried-matt-s-skills--0oXOOlqVu5M|So I tried Matt's skills...]]", "[[extracts/youtube/ai-learning/2026-09-11-how-i-deleted-95-of-my-agent-skills-and-got-better-results-nick-nisi-workos--vy7o1g2iHY8|How I deleted 95% of my agent skills and got better results — Nick Nisi, WorkOS]]", "[[extracts/youtube/ai-learning/2026-09-11-matt-pococks-agentic-engineering-workflow-just-copy-him--nQwJVHCtDDY|Matt Pocock’s Agentic Engineering Workflow (just copy him)]]", "[[extracts/youtube/ai-learning/2026-09-11-i-tried-100-claude-code-skills-these-6-are-the-best--eRS3CmvrOvA|I Tried 100+ Claude Code Skills. These 6 Are The Best]]", "[[extracts/youtube/ai-learning/2026-09-11-my-agentic-engineering-workflow-after-6-775-sessions--c9nRxEy1kUY|My Agentic Engineering Workflow (after 6,775 sessions)]]", "[[extracts/youtube/ai-learning/2026-09-11-full-workshop-setting-yourself-up-for-success-jason-liu-openai-codex--il1c1a2FufU|Full Workshop: Setting Yourself Up for Success —Jason Liu, OpenAI Codex]]"]
---

# Pstack Is Agent Overkill. Use It Anyway!

## Tese
O Pstack de Lauren Tan mostra como um conjunto curado de skills, playbooks e princípios (roteamento por potato mode, arena/swarm paralelo, verificação roteirizada e disciplina do contexto) transforma agentes de codificação em engenheiros seniores de alto custo em tokens, porém muito mais confiáveis, sob a filosofia de que 'a melhor spec é o código'.

## Conceitos-chave
- potato mode como roteador de skills
- skills vs playbooks vs princípios
- arena: múltiplos modelos competindo no mesmo problema com graft/reject das melhores partes
- swarm: workers paralelos com fatias distintas e agregação em relatório único
- fearless parallelism entre feature branches e worktrees
- TDD-first (testes unitários antes de prosseguir)
- why-skill: arqueologia de decisões via MCPs/CLIs (ADRs)
- recall: retomada de projeto entre sessões escaneando transcripts e MCPs
- interrogate: code review por múltiplos modelos contra os padrões
- create-verification e maintain-verification: scripts que provam comportamento real e são mantidos em sincronia
- unslop: remoção de chavões típicos de IA (delve, crucial, em dashes)
- bro skill: reformulação da última mensagem em linguagem simples
- show me your work: rastreabilidade do pipeline do agente (probe → frame → scaffold → arena → redesign → verificação → auditoria)
- design changes forced by reality: planos quebram ao contato com a implementação
- laziness protocol: deletar código e buscar a menor mudança possível
- redesign from first principles ao adicionar features
- minimizar reader load: menos abstrações e PRs menores
- exhaust the design space: explorar variações antes de commitar o design
- build a lever: automatizar ações manuais repetidas em CLI/script
- guard the context window: delegar a subagentes com janelas próprias reportando ao thread central
- never block the human
- verde nos testes não equivale a prova de funcionamento do artefato real
- ausência deliberada de skill de planejamento (anti spec-driven)
- gerenciador de skills跨 agentes (Molton Base)

## Ferramentas & pessoas
**Ferramentas:** Pstack, Potato Mode, Molton Base, Cursor, Claude Code, Codex, OpenCode, OpenRouter, PostHog, Slack, Sentry, Notion, Linear, Fable 5.1, Claude, GPT, Grok, Claude Opus 5, BMAD, superpowers, OpenSpec, Cadream (geração de vídeo, conforme transcrito)

**Pessoas/orgs:** Lauren Tan, Netflix, React core team, SpaceX, Cursor, Theo, Michael Dener, Rob Shocks, Switch Dimension (canal/curso)

## Claims acionáveis
- Instale o Pstack no Cursor via /addplugin pstack; para Claude Code, Codex e OpenCode use o port não-oficial de Michael Dener nos marketplaces de plugins
- Potato mode é um roteador que decide qual dos 20+ skills/playbooks invocar primeiro para um prompt
- O Pstack não tem skill de planejamento de propósito — é desenhado para codebases estabelecidos, com a tese de que 'a melhor spec é o código'
- Arena roda 3-4 modelos (ex.: Claude, GPT, Grok, Opus) no mesmo problema e enxerta as melhores partes num commit final, decidindo graft ou reject com base no que os subagentes aprenderam
- Swarm distribui fatias diferentes do problema a workers paralelos e agrega tudo num relatório sem sobreposições (afirmação grande ainda não validada pelo autor do vídeo)
- O why-skill consulta MCPs e CLIs do projeto (PostHog para produto, Slack para discussões, Sentry para logs) para reconstruir o registro de decisões/ADRs de por que algo foi feito
- O recall-skill retoma projetos parados escaneando todos os transcripts e consultando Notion/Linear/PostHog para definir próximos passos
- O interrogate-skill faz 2-3 modelos revisarem o código contra os padrões do projeto, com alto consumo de tokens em troca de máxima qualidade
- O create-verification-skill gera scripts de verificação do comportamento real do app — essencial para agentes não-determinísticos — e o maintain-verification-skill atualiza verificadores que divergiram do desenvolvimento
- O unslop-skill remove frases-sinal de IA (pivotal moment, crucial, delve, em dashes) de textos gerados por agentes
- O bro-skill reexplica a última mensagem do agente em linguagem simples, útil ao operar ~10 agentes em paralelo
- O show me your work expôs o pipeline real: probing de viabilidade, enquadramento de requisitos/constraints, scaffolding, arena, redesign forçado pela realidade, verificação e auditoria — que capturou 3 afirmações alucinadas pelo próprio agente
- Aplique o laziness protocol: ao refatorar, prefira deletar código e buscar a menor mudança que resolve, gerando mais manutenibilidade
- Ao adicionar features, redesenhe from first principles — como se o recurso existisse desde o dia 1 — mesmo que isso remova estruturas existentes
- Minimize reader load: menos abstrações e módulos dispersos para evitar PRs gigantes e disjuntos de agentes
- Exhaust the design space: gere variações concorrentes (design mode) antes de escolher e comitar o design
- Build a lever: converta ações manuais repetidas com o agente em CLI/script reutilizável (ex.: CLI própria sobre a API do OpenRouter com um único API key para texto, imagem, vídeo e voz)
- Guarde o contexto central: offload de fatias a subagentes com janelas próprias que reportam de volta ao thread principal, e nunca bloqueie o humano
- Testes verdes/compilação não provam funcionamento: verifique o artefato real com scripts, computer use ou testes end-to-end
- Benchmark anedótico do autor: Fable 5.1 sem skills concluiu o projeto em ~30min vs ~1h com Pstack, com resultado substancialmente melhor porém muito mais caro — reserve o Pstack para recursos críticos, não para mudanças triviais de UI

> **Deep dive:** `medium` — Há boa densidade de padrões acionáveis e relevantes (arena/swarm, verificação roteirizada, guarda de contexto, retomada cross-session), mas é uma walkthrough de segunda mão de skills de terceiros, com segmentos promocionais (OpenRouter, curso) e afirmações centrais admitidamente não verificadas pelo próprio autor.
