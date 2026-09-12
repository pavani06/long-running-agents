---
title: "Matt Pocock’s Agentic Engineering Workflow (just copy him)"
type: "extract"
source: "youtube"
video_id: "nQwJVHCtDDY"
url: "https://www.youtube.com/watch?v=nQwJVHCtDDY"
channel: "David Ondrej"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-matt-pococks-agentic-engineering-workflow-just-copy-him--nQwJVHCtDDY.txt]]"
tags: ["harness-engineering", "context-engineering", "agent-tooling", "agentic-coding", "agent-loop", "multi-agent", "agent-fleets", "model-selection", "token-budgeting", "arquitetura", "knowledge-management", "curriculo-conteudo", "memory-architecture", "state", "process", "code-review", "stack-tooling"]
thesis: "A IA já absorveu a programação tática, então o diferencial dos desenvolvedores está em dominar a programação estratégica e investir no harness (prompts, skills, ambiente e arquitetura do codebase) tanto quanto no modelo — pois suas próprias habilidades são o teto do multiplicador que a IA entrega."
concepts: ["harness vs. modelo (metáfora do motor vs. chassi de F1; split 50/50)", "programação tática vs. estratégica (A Philosophy of Software Design)", "skills procedurais (invocadas pelo usuário) vs. abilities (invocadas pelo modelo)", "vazamento de descrições de skills no contexto; flag disable model invocation", "skills stateful vs. stateless (estado persistido no workspace)", "conhecimento, habilidades e sabedoria (sabedoria só se adquire fazendo no contexto real)", "zona de desenvolvimento proximal e quizzes para storage strength no teach skill", "mission.md, learning record e lições em HTML; conhecimento como grafo percorrido em caminho linear", "trabalho AFK vs. human-in-the-loop", "filas (queues/backlog) em vez de loops agênticos infinitos", "sandboxing de agentes e paralelização (frota infinita de programadores táticos)", "otimização de token spend via codebase fácil de mudar (permite modelos mais baratos)", "bitter lesson (compute cru supera otimizações pontuais)", "cron jobs de revisão de segurança e sistemas self-improving", "suas habilidades são o teto do que a IA pode fazer", "política de esperar ~1 mês antes de adotar um novo modelo", "delegação eficaz: escopo claro, interfaces entre módulos, bons testes, documentação mínima direcionadora"]
tools: ["Claude Code", "Claude Opus 4.8 (medium effort)", "Claude Opus 4.5", "Fable", "Cursor", "Sand Castle", "Docker", "Podman", "GitHub Actions", "Vercel Sandboxes", "npx skills add (CLI de skills)", "teach skill", "grill me skill", "PRD skill", "superpowers (repo de skills)", "Whisper Flow", "SerpApi", "Tailscale", "Replit", "Lovable", "Codex", "Pro Git (livro)", "Twitter/X API"]
people: ["Matt Pocock", "David (entrevistador)", "John Ousterhout", "Geoffrey Huntley", "Peter Steinberger", "Obra (repo superpowers)", "Anthropic", "OpenAI", "Vercel", "GitHub", "SerpApi (patrocinador)"]
claims: ["Trate modelo e harness como 50/50 e otimize o que você controla: prompts, skills, ambiente de execução e qualidade do codebase", "Para otimizar gasto de tokens, torne o codebase fácil de mudar — arquitetura melhor permite usar modelos mais baratos com menos tokens 'batendo a cabeça na parede'", "Prefira skills procedurais (invocadas por você) para manter o controle e não delegar seu pensamento; reserve abilities para padrões que o modelo deve invocar sozinho, como coding standards", "Use 'disable model invocation: true' em skills procedurais para que suas descrições não vazem no contexto — 100 skills com abilities = 100 descrições no contexto", "Antes de implementar, rode um skill tipo 'grill me' (entrevistador adversário de ~5 frases) como substituto do plan mode até atingir entendimento compartilhado", "Espere cerca de um mês após o lançamento de um novo modelo antes de adotá-lo, pesando custo, latência e disponibilidade", "Rode agentes dentro de sandboxes (Docker/Podman via Sand Castle) para evitar ações destrutivas e paralelizar vários agentes, inclusive remotos (Vercel sandboxes) trazendo os commits de volta", "Configure revisão por agente em PRs via GitHub Actions usando um prompt de revisão versionado localmente", "Adote trabalho AFK: remova-se do loop de permissões para multiplicar sua saída e revise os resultados depois", "Pense em filas (backlog com labels de triage, ex.: 'agent implement') em vez de loops infinitos; o item sai da fila quando o PR é mergeado", "Rode cron jobs diários de revisão de segurança cobrindo partes diferentes do repo com modelos baratos, em vez de depender do modelo mais novo para achar bugs profundos", "Quando a IA encontra um bug profundo, investigue por que ele existia e crie um sistema/skill/processo que previna recorrência ('se roubam sua bike, compre um cadeado')", "Delegue a programação tática e mantenha a estratégica: desenhe as partes difíceis antecipadamente, escope bem as tarefas, cuide das interfaces entre módulos, dos testes e de documentação mínima que aponte a IA ao lugar certo", "Transforme pedagogia em skill stateful: capture a missão em mission.md, mantenha learning record, gere cheat sheets e lições em HTML com quizzes personalizados ao setup local do aluno", "Procedralize seu trabalho em skills compartilhadas com o time (ex.: como fazer bons planos) para elevar o piso de todos", "Upskill a si mesmo: sêniores ganham ~10x com IA enquanto juniores ganham pouco, então seu domínio define o teto do multiplicador", "Use ditado (ex.: Whisper Flow) como habilidade overpowered para acelerar a entrada e saída de tokens do seu cérebro"]
deep_dive: "high"
deep_dive_reason: "Densidade alta de detalhes arquiteturais acionáveis e relativamente novos — taxonomia procedural vs. ability com vazamento de contexto controlável, agentes AFK em sandbox orquestrados via GitHub Actions, e 'filas não loops' — diretamente relevantes a harness, context-engineering e agent-fleets, ainda que centrado em opinião de um único praticante."
---

# Matt Pocock’s Agentic Engineering Workflow (just copy him)

## Tese
A IA já absorveu a programação tática, então o diferencial dos desenvolvedores está em dominar a programação estratégica e investir no harness (prompts, skills, ambiente e arquitetura do codebase) tanto quanto no modelo — pois suas próprias habilidades são o teto do multiplicador que a IA entrega.

## Conceitos-chave
- harness vs. modelo (metáfora do motor vs. chassi de F1; split 50/50)
- programação tática vs. estratégica (A Philosophy of Software Design)
- skills procedurais (invocadas pelo usuário) vs. abilities (invocadas pelo modelo)
- vazamento de descrições de skills no contexto; flag disable model invocation
- skills stateful vs. stateless (estado persistido no workspace)
- conhecimento, habilidades e sabedoria (sabedoria só se adquire fazendo no contexto real)
- zona de desenvolvimento proximal e quizzes para storage strength no teach skill
- mission.md, learning record e lições em HTML; conhecimento como grafo percorrido em caminho linear
- trabalho AFK vs. human-in-the-loop
- filas (queues/backlog) em vez de loops agênticos infinitos
- sandboxing de agentes e paralelização (frota infinita de programadores táticos)
- otimização de token spend via codebase fácil de mudar (permite modelos mais baratos)
- bitter lesson (compute cru supera otimizações pontuais)
- cron jobs de revisão de segurança e sistemas self-improving
- suas habilidades são o teto do que a IA pode fazer
- política de esperar ~1 mês antes de adotar um novo modelo
- delegação eficaz: escopo claro, interfaces entre módulos, bons testes, documentação mínima direcionadora

## Ferramentas & pessoas
**Ferramentas:** Claude Code, Claude Opus 4.8 (medium effort), Claude Opus 4.5, Fable, Cursor, Sand Castle, Docker, Podman, GitHub Actions, Vercel Sandboxes, npx skills add (CLI de skills), teach skill, grill me skill, PRD skill, superpowers (repo de skills), Whisper Flow, SerpApi, Tailscale, Replit, Lovable, Codex, Pro Git (livro), Twitter/X API

**Pessoas/orgs:** Matt Pocock, David (entrevistador), John Ousterhout, Geoffrey Huntley, Peter Steinberger, Obra (repo superpowers), Anthropic, OpenAI, Vercel, GitHub, SerpApi (patrocinador)

## Claims acionáveis
- Trate modelo e harness como 50/50 e otimize o que você controla: prompts, skills, ambiente de execução e qualidade do codebase
- Para otimizar gasto de tokens, torne o codebase fácil de mudar — arquitetura melhor permite usar modelos mais baratos com menos tokens 'batendo a cabeça na parede'
- Prefira skills procedurais (invocadas por você) para manter o controle e não delegar seu pensamento; reserve abilities para padrões que o modelo deve invocar sozinho, como coding standards
- Use 'disable model invocation: true' em skills procedurais para que suas descrições não vazem no contexto — 100 skills com abilities = 100 descrições no contexto
- Antes de implementar, rode um skill tipo 'grill me' (entrevistador adversário de ~5 frases) como substituto do plan mode até atingir entendimento compartilhado
- Espere cerca de um mês após o lançamento de um novo modelo antes de adotá-lo, pesando custo, latência e disponibilidade
- Rode agentes dentro de sandboxes (Docker/Podman via Sand Castle) para evitar ações destrutivas e paralelizar vários agentes, inclusive remotos (Vercel sandboxes) trazendo os commits de volta
- Configure revisão por agente em PRs via GitHub Actions usando um prompt de revisão versionado localmente
- Adote trabalho AFK: remova-se do loop de permissões para multiplicar sua saída e revise os resultados depois
- Pense em filas (backlog com labels de triage, ex.: 'agent implement') em vez de loops infinitos; o item sai da fila quando o PR é mergeado
- Rode cron jobs diários de revisão de segurança cobrindo partes diferentes do repo com modelos baratos, em vez de depender do modelo mais novo para achar bugs profundos
- Quando a IA encontra um bug profundo, investigue por que ele existia e crie um sistema/skill/processo que previna recorrência ('se roubam sua bike, compre um cadeado')
- Delegue a programação tática e mantenha a estratégica: desenhe as partes difíceis antecipadamente, escope bem as tarefas, cuide das interfaces entre módulos, dos testes e de documentação mínima que aponte a IA ao lugar certo
- Transforme pedagogia em skill stateful: capture a missão em mission.md, mantenha learning record, gere cheat sheets e lições em HTML com quizzes personalizados ao setup local do aluno
- Procedralize seu trabalho em skills compartilhadas com o time (ex.: como fazer bons planos) para elevar o piso de todos
- Upskill a si mesmo: sêniores ganham ~10x com IA enquanto juniores ganham pouco, então seu domínio define o teto do multiplicador
- Use ditado (ex.: Whisper Flow) como habilidade overpowered para acelerar a entrada e saída de tokens do seu cérebro

> **Deep dive:** `high` — Densidade alta de detalhes arquiteturais acionáveis e relativamente novos — taxonomia procedural vs. ability com vazamento de contexto controlável, agentes AFK em sandbox orquestrados via GitHub Actions, e 'filas não loops' — diretamente relevantes a harness, context-engineering e agent-fleets, ainda que centrado em opinião de um único praticante.
