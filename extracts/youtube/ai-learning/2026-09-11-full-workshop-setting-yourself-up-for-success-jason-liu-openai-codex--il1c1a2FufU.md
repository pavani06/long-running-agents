---
title: "Full Workshop: Setting Yourself Up for Success —Jason Liu, OpenAI Codex"
type: "extract"
source: "youtube"
video_id: "il1c1a2FufU"
url: "https://www.youtube.com/watch?v=il1c1a2FufU"
channel: "AI Engineer"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-full-workshop-setting-yourself-up-for-success-jason-liu-openai-codex--il1c1a2FufU.txt]]"
tags: ["agent-fleets", "agent-loop", "agent-tooling", "context-engineering", "context-management", "cross-session", "escalation", "governanca", "memory-architecture", "model-selection", "monitoramento", "multi-agent", "permissions", "knowledge-management", "state", "verification"]
thesis: "A compaction tornou threads longos e persistentes viáveis, permitindo que threads fixadas do Codex — equipadas com skills auto-editáveis, memory vault em monorepo versionado, appshots e automações de heartbeat — operem como uma frota de teammates (ICs e gerentes) que ingerem contexto, executam trabalho verificável e agem no mundo real em nome do usuário."
concepts: ["compaction viabilizando threads de 5 semanas com centenas de sub-agentes que ainda sabem seu papel", "pinned threads como teammates persistentes renomeados por ID de projeto", "threads que se comunicam entre si (listar, renomear, enviar mensagens) evoluindo para orquestração gerente/IC", "automações de heartbeat que agendam mensagens de volta na mesma thread em vez de criar novas threads", "appshots: screenshot combinado com a árvore de acessibilidade completa do app, expondo IDs de canais e usuários", "skills auto-melhoráveis com permissão para editar o próprio arquivo a cada execução", "plugins como bibliotecas de skills compartilháveis com o time (mindset plugin hero)", "personal memory vault em monorepo versionado em git e revisado via git diff", "chief-of-staff thread como fonte única de verdade diária (morning brief, check de conectores)", "goal com verificador explícito (/goal) e ultra goal com goal.md, plan.md e state.md/worklog editáveis durante a execução", "metadados de roteamento (IDs de Slack, e-mails) no front matter de arquivos de projeto e pessoa para descoberta autônoma de contexto", "o modelo escrevendo os próprios prompts e automações a partir de voice memos bagunçados", "ditado com pedal de pé: falar cerca de 3x mais rápido que digitar", "modos de permissão (ask every / auto review / full auto) e guardrails administrativos organizacionais", "evolução do sandbox de comando único para o computador inteiro, com bordas em nível de máquina e organização", "computer use vs Chrome extension: GUI arbitrária em background vs apenas dentro do Chrome", "remote control do desktop via app iOS com QR code e flag locked use", "personal CRM via skills new person / new project", "write-like-me: destilação de 6 meses de mensagens em style guide pessoal", "três atos do trabalho com IA: trazer contexto, trabalhar, agir no mundo real"]
tools: ["Codex app", "Codex CLI", "Chrome extension", "computer use", "iOS app (remote control)", "AGENTS.md", "MCP", "Slack", "Gmail", "Teams", "Notion", "Linear", "Obsidian", "iMovie", "DocuSign", "Google Drive", "GitHub", "LinkedIn", "Twitter/X", "Statsig", "Playwright", "skillset.sh", "Vercel Skills", "uv", "rich", "Rust", "React", "Chrome", "Safari"]
people: ["Jason (OpenAI)", "Charlie", "Dominic", "Swix", "OpenAI", "Vercel"]
claims: ["Ignore o conselho antigo de iniciar nova thread após ~20 mensagens: fixe uma thread por projeto, renomeie com o ID do projeto e deixe-a delegar a sub-agentes e escrever no memory vault", "Projete automações para agendar mensagens de volta na MESMA thread em vez de criar uma nova thread a cada disparo", "Prefira appshots a screenshots: a árvore de acessibilidade entrega IDs exatos de canais e usuários, colapsando cadeias de múltiplos tool calls em uma única chamada", "Instrua cada skill com uma cláusula permitindo que ela edite o próprio arquivo ao aprender algo novo, tornando-a auto-melhorável", "Versione seu memory vault como repo git e revise o que os agentes alteraram rodando git diff", "Adicione IDs de canais Slack e e-mails no front matter dos arquivos de projeto e de pessoa para que o agente descubra contexto sozinho, eliminando tags manuais", "Use /goal sempre com um verificador explícito; para escopo mutável, coloque o goal em goal.md (ultra goal) acompanhado de plan.md e state.md/worklog para observabilidade de runs longos", "Peça ao próprio modelo para escrever o prompt e a automação a partir de um voice memo bagunçado, pois a saída fica mais in-distribution", "Combine permissões em auto review com um AGENTS.md bem definido e use settings administrativos para bloquear ações perigosas como MCP enviando e-mails externos ou mensagens em Slack externo", "Use modelos spark para tarefas triviais de computer use (ex.: check-in de voo) e modelos maiores para trabalho complexo; latência pesa menos porque o trabalho roda em background", "Crie uma skill write-like-me lendo 6 meses de e-mails e Slack para gerar um style guide pessoal aplicado a toda mensagem que o agente redigir", "Teste uma skill pessoalmente por cerca de 2 meses antes de compartilhar com o time e meça seu impacto pela frequência de uso pelos colegas", "Uma linha no AGENTS.md (ex.: salvar código em /dev e não no monorepo) permite que um único projeto-vault gerencie arquivos fora do diretório do projeto", "Ative a flag locked use em settings > computer use para disparar computer use pelo celular mesmo com o laptop fechado, desde que conectado à tomada", "Quando o modelo não sabe a resposta (ex.: política de privacidade), delegue perguntando diretamente a uma pessoa — a skill delegate"]
deep_dive: "high"
deep_dive_reason: "Alta densidade de detalhe operacional em primeira mão e novidade arquitetural em exactamente as áreas-alvo: fleets de agentes (threads fixadas com heartbeat, mensageria entre threads, split gerente/IC), arquitetura de memória versionada e auditável via git diff, captura de contexto por árvore de acessibilidade, loops goal/verifier editáveis em arquivo e guardrails de governança organizacional."
---

# Full Workshop: Setting Yourself Up for Success —Jason Liu, OpenAI Codex

## Tese
A compaction tornou threads longos e persistentes viáveis, permitindo que threads fixadas do Codex — equipadas com skills auto-editáveis, memory vault em monorepo versionado, appshots e automações de heartbeat — operem como uma frota de teammates (ICs e gerentes) que ingerem contexto, executam trabalho verificável e agem no mundo real em nome do usuário.

## Conceitos-chave
- compaction viabilizando threads de 5 semanas com centenas de sub-agentes que ainda sabem seu papel
- pinned threads como teammates persistentes renomeados por ID de projeto
- threads que se comunicam entre si (listar, renomear, enviar mensagens) evoluindo para orquestração gerente/IC
- automações de heartbeat que agendam mensagens de volta na mesma thread em vez de criar novas threads
- appshots: screenshot combinado com a árvore de acessibilidade completa do app, expondo IDs de canais e usuários
- skills auto-melhoráveis com permissão para editar o próprio arquivo a cada execução
- plugins como bibliotecas de skills compartilháveis com o time (mindset plugin hero)
- personal memory vault em monorepo versionado em git e revisado via git diff
- chief-of-staff thread como fonte única de verdade diária (morning brief, check de conectores)
- goal com verificador explícito (/goal) e ultra goal com goal.md, plan.md e state.md/worklog editáveis durante a execução
- metadados de roteamento (IDs de Slack, e-mails) no front matter de arquivos de projeto e pessoa para descoberta autônoma de contexto
- o modelo escrevendo os próprios prompts e automações a partir de voice memos bagunçados
- ditado com pedal de pé: falar cerca de 3x mais rápido que digitar
- modos de permissão (ask every / auto review / full auto) e guardrails administrativos organizacionais
- evolução do sandbox de comando único para o computador inteiro, com bordas em nível de máquina e organização
- computer use vs Chrome extension: GUI arbitrária em background vs apenas dentro do Chrome
- remote control do desktop via app iOS com QR code e flag locked use
- personal CRM via skills new person / new project
- write-like-me: destilação de 6 meses de mensagens em style guide pessoal
- três atos do trabalho com IA: trazer contexto, trabalhar, agir no mundo real

## Ferramentas & pessoas
**Ferramentas:** Codex app, Codex CLI, Chrome extension, computer use, iOS app (remote control), AGENTS.md, MCP, Slack, Gmail, Teams, Notion, Linear, Obsidian, iMovie, DocuSign, Google Drive, GitHub, LinkedIn, Twitter/X, Statsig, Playwright, skillset.sh, Vercel Skills, uv, rich, Rust, React, Chrome, Safari

**Pessoas/orgs:** Jason (OpenAI), Charlie, Dominic, Swix, OpenAI, Vercel

## Claims acionáveis
- Ignore o conselho antigo de iniciar nova thread após ~20 mensagens: fixe uma thread por projeto, renomeie com o ID do projeto e deixe-a delegar a sub-agentes e escrever no memory vault
- Projete automações para agendar mensagens de volta na MESMA thread em vez de criar uma nova thread a cada disparo
- Prefira appshots a screenshots: a árvore de acessibilidade entrega IDs exatos de canais e usuários, colapsando cadeias de múltiplos tool calls em uma única chamada
- Instrua cada skill com uma cláusula permitindo que ela edite o próprio arquivo ao aprender algo novo, tornando-a auto-melhorável
- Versione seu memory vault como repo git e revise o que os agentes alteraram rodando git diff
- Adicione IDs de canais Slack e e-mails no front matter dos arquivos de projeto e de pessoa para que o agente descubra contexto sozinho, eliminando tags manuais
- Use /goal sempre com um verificador explícito; para escopo mutável, coloque o goal em goal.md (ultra goal) acompanhado de plan.md e state.md/worklog para observabilidade de runs longos
- Peça ao próprio modelo para escrever o prompt e a automação a partir de um voice memo bagunçado, pois a saída fica mais in-distribution
- Combine permissões em auto review com um AGENTS.md bem definido e use settings administrativos para bloquear ações perigosas como MCP enviando e-mails externos ou mensagens em Slack externo
- Use modelos spark para tarefas triviais de computer use (ex.: check-in de voo) e modelos maiores para trabalho complexo; latência pesa menos porque o trabalho roda em background
- Crie uma skill write-like-me lendo 6 meses de e-mails e Slack para gerar um style guide pessoal aplicado a toda mensagem que o agente redigir
- Teste uma skill pessoalmente por cerca de 2 meses antes de compartilhar com o time e meça seu impacto pela frequência de uso pelos colegas
- Uma linha no AGENTS.md (ex.: salvar código em /dev e não no monorepo) permite que um único projeto-vault gerencie arquivos fora do diretório do projeto
- Ative a flag locked use em settings > computer use para disparar computer use pelo celular mesmo com o laptop fechado, desde que conectado à tomada
- Quando o modelo não sabe a resposta (ex.: política de privacidade), delegue perguntando diretamente a uma pessoa — a skill delegate

> **Deep dive:** `high` — Alta densidade de detalhe operacional em primeira mão e novidade arquitetural em exactamente as áreas-alvo: fleets de agentes (threads fixadas com heartbeat, mensageria entre threads, split gerente/IC), arquitetura de memória versionada e auditável via git diff, captura de contexto por árvore de acessibilidade, loops goal/verifier editáveis em arquivo e guardrails de governança organizacional.
