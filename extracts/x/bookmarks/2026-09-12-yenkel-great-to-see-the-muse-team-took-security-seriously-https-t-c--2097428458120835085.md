---
title: "Arquitetura de segurança de agentes pessoais"
type: "extract"
source: "x"
status_id: "2097428458120835085"
handle: "yenkel"
url: "https://x.com/yenkel/status/2097428458120835085"
created_at: "2026-09-08T20:54:47.000Z"
extracted: "2026-09-13"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-12-yenkel-great-to-see-the-muse-team-took-security-seriously-https-t-c--2097428458120835085.json]]"
tags: ["agents", "harness-engineering", "permissions", "arquitetura", "runtime", "escalation", "multi-agent", "production"]
topic: "Arquitetura de segurança de agentes pessoais"
summary: "Post técnico do Meta Superintelligence Labs detalhando como o Muse, agente pessoal autônomo com acesso a inbox, calendário e shell, foi construído assumindo que o agente estará sob ataque: VM isolada por usuário, autoridade de permissões separada e credenciais nunca expostas ao modelo. É a referência concreta de como projetar harness de agente pessoal seguro."
key_points: ["O harness ('Hatch') roda em container systemd-nspawn com root mapeado para usuário sem privilégios no host; serviços sensíveis (classificadores de segurança, authd, workers privsep de conectores) ficam fora da célula de runtime, para que ataques via dados não-confiáveis não desabilitem as proteções", "Sentinel é um agente separado no host e a única autoridade para ações em conectores e egress de rede (avalia L4 e L7, hostname, IP final, método, payload; bloqueia SSRF); Muse propõe ações, mas só Sentinel concede, nega ou escala ao usuário", "Credencial surrogation: o agente só vê tokens substitutos cunhados pelo authd; credenciais reais são inseridas apenas no limite de rede — tornando inútil tentar extrair segredos via prompt injection", "'Tainted egress': rastreamento de fluxo de dados em nível de kernel (eBPF + hooks LSM); requisições limpas e estreitamente delimitadas podem auto-aprovar, processos contaminados por dados do usuário caem no fluxo de aprovação humana com capabilities estritas (one-time, session, task, time-bounded), não sugestões conversacionais", "Least privilege granular: separação leitura/escrita por conector e controles mais finos que escopos OAuth; bug bounty aberto até $300k, incluindo $130k por prompt injection que afete um usuário"]
entities: ["Muse", "Meta Superintelligence Labs", "Tarek Sheasha", "Sentinel", "hatch-authd", "privsep", "systemd-nspawn", "eBPF", "PostgreSQL", "Gmail", "Instagram"]
content_type: "resource"
revisit: "high"
grounded_in: "article"
links: ["https://research.meta.ai/blog/security-and-safety-for-ai-agents-our-approach-with-muse"]
media: ["https://pbs.twimg.com/media/HRuQEBBWsAAJluw.jpg"]
thin: false
relates-to: ["[[extracts/x/bookmarks/2026-09-12-robotbird01-harness-pi-agent-skill-https-t-co-6eqhirel54--2098044628058689738|Arquitetura de plataforma harness empresarial]]", "[[extracts/x/bookmarks/2026-09-12-akshay_pachaar-finally-an-open-source-runtime-security-layer-for-your-agent--2098042808221511836|runtime security layer para agentes]]", "[[extracts/x/bookmarks/2026-09-14-shreyanshpatni_-want-to-build-a-domain-specific-agent-harness-this-is-a-grea--2099180288668750246|Construção de harness para agentes]]", "[[extracts/x/bookmarks/2026-09-12-hackernoon-ai-is-raising-the-baseline-for-software-engineering-this-art--2082839180736889054|AI e plataformas de engenharia]]", "[[extracts/x/bookmarks/2026-09-12-andrewcurran_-a-man-in-australia-asked-his-agent-claude-running-on-opencla--2086567854850384054|agente explora vulnerabilidade em agendamento]]", "[[extracts/x/bookmarks/2026-09-12-kevinwhinnery-the-era-of-the-dumb-token-pipe-is-ending-agent-harness-apis--2098444890602455431|Agent harness APIs como integração]]", "[[extracts/x/bookmarks/2026-09-12-simonw-wow-turns-out-another-openai-agent-swarm-was-busy-spamming-a--2098573718142452055|Ataque de agentes OpenAI ao RubyGems]]", "[[extracts/x/bookmarks/2026-09-12-eric_wallace_-today-we-are-releasing-gpt-5-6-cyber-the-model-is-our-first--2086866306167656901|Lançamento de modelo de cibersegurança]]", "[[extracts/x/bookmarks/2026-09-12-claudedevs-mcp-2026-07-28-is-live-and-it-s-the-largest-update-to-the-pr--2082164248697069935|MCP 2026-07-28 stateless release]]"]
theme: "Tooling e harness de agentes"
---

# Arquitetura de segurança de agentes pessoais

**@yenkel** · [2097428458120835085](https://x.com/yenkel/status/2097428458120835085) · `resource`

## Resumo
Post técnico do Meta Superintelligence Labs detalhando como o Muse, agente pessoal autônomo com acesso a inbox, calendário e shell, foi construído assumindo que o agente estará sob ataque: VM isolada por usuário, autoridade de permissões separada e credenciais nunca expostas ao modelo. É a referência concreta de como projetar harness de agente pessoal seguro.

## Pontos-chave
- O harness ('Hatch') roda em container systemd-nspawn com root mapeado para usuário sem privilégios no host; serviços sensíveis (classificadores de segurança, authd, workers privsep de conectores) ficam fora da célula de runtime, para que ataques via dados não-confiáveis não desabilitem as proteções
- Sentinel é um agente separado no host e a única autoridade para ações em conectores e egress de rede (avalia L4 e L7, hostname, IP final, método, payload; bloqueia SSRF); Muse propõe ações, mas só Sentinel concede, nega ou escala ao usuário
- Credencial surrogation: o agente só vê tokens substitutos cunhados pelo authd; credenciais reais são inseridas apenas no limite de rede — tornando inútil tentar extrair segredos via prompt injection
- 'Tainted egress': rastreamento de fluxo de dados em nível de kernel (eBPF + hooks LSM); requisições limpas e estreitamente delimitadas podem auto-aprovar, processos contaminados por dados do usuário caem no fluxo de aprovação humana com capabilities estritas (one-time, session, task, time-bounded), não sugestões conversacionais
- Least privilege granular: separação leitura/escrita por conector e controles mais finos que escopos OAuth; bug bounty aberto até $300k, incluindo $130k por prompt injection que afete um usuário

## Links
- https://research.meta.ai/blog/security-and-safety-for-ai-agents-our-approach-with-muse

## Entidades
Muse, Meta Superintelligence Labs, Tarek Sheasha, Sentinel, hatch-authd, privsep, systemd-nspawn, eBPF, PostgreSQL, Gmail, Instagram

> **Revisit:** `high` · **fonte:** `article`
