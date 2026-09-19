---
title: "auditoria de segurança multi-agente"
type: "extract"
source: "x"
status_id: "2100557033829261738"
handle: "trending_repos"
url: "https://x.com/trending_repos/status/2100557033829261738"
created_at: "2026-09-17T12:06:37.000Z"
extracted: "2026-09-19"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-18-trending_repos-trending-repository-of-the-day-security-audit-skill-a-coding--2100557033829261738.json]]"
tags: ["agents", "multi-agent", "harness-engineering", "verification", "evals", "agent-tooling", "production"]
topic: "auditoria de segurança multi-agente"
summary: "Cloudflare open-sourcou o security-audit-skill, uma skill que transforma um coding agent em auditor de segurança via seis fases (reconhecimento, caça guiada por cobertura, validação adversarial, saída estruturada, verificação independente e relatório); é o ponto de partida do harness de descoberta de vulnerabilidades que a empresa usa em escala. Denso e diretamente instalável com npx skills, é uma referência de orquestração de agentes com verificação adversarial."
key_points: ["Fluxo de seis fases: reconhecimento mapeia arquitetura e fronteiras de confiança (architecture.md, coverage-ledger.json); caça distribui hunters isolados por unidades do ledger com coverage critics apontando lacunas; validação adversarial usa verificador novo que tenta desprovar cada candidato; saída estruturada em findings.json com três verdictos distintos (confirmed, needs_validation, rejected) validados por schema.", "Princípio central de adversarialidade: o agente que verifica um finding nunca é o que o encontrou; severity exige impacto (likelihood × impacto, não desvio de checklist); gaps de defense-in-depth são hardening notes, não vulnerabilidades.", "Execuções múltiplas são aditivas: o skill reaproveita ledgers e findings anteriores para mirar lacunas e revalidar código alterado — em testes, uma única rodada achou ~metade das vulnerabilidades que rodadas repetidas acharam no total.", "Segurança operacional: execução de código do alvo exige sandbox enforced pelo OS (rede externa desabilitada, ambiente allowlist, limites de recursos, escrita só em scratch); sem isso, leads ficam em needs_validation em vez de serem executados.", "Inclui validadores zero-dependency (validate-findings.cjs, validate-coverage-ledger.cjs) rodados em checkpoints das fases, e bibliotecas de prompts por classe de ataque (web/auth, memory-safety/binário, prompt-injection/LLM, supply chain, cloud/IaC, client-side, exaustão de recursos, isolamento de dados, IPC local)."]
entities: ["Cloudflare", "security-audit-skill", "Skills CLI", "Node.js"]
content_type: "tool"
revisit: "high"
grounded_in: "article"
thin: false
links: ["https://github.com/cloudflare/security-audit-skill"]
media: []
---

# auditoria de segurança multi-agente

**@trending_repos** · [2100557033829261738](https://x.com/trending_repos/status/2100557033829261738) · `tool`

## Resumo
Cloudflare open-sourcou o security-audit-skill, uma skill que transforma um coding agent em auditor de segurança via seis fases (reconhecimento, caça guiada por cobertura, validação adversarial, saída estruturada, verificação independente e relatório); é o ponto de partida do harness de descoberta de vulnerabilidades que a empresa usa em escala. Denso e diretamente instalável com npx skills, é uma referência de orquestração de agentes com verificação adversarial.

## Pontos-chave
- Fluxo de seis fases: reconhecimento mapeia arquitetura e fronteiras de confiança (architecture.md, coverage-ledger.json); caça distribui hunters isolados por unidades do ledger com coverage critics apontando lacunas; validação adversarial usa verificador novo que tenta desprovar cada candidato; saída estruturada em findings.json com três verdictos distintos (confirmed, needs_validation, rejected) validados por schema.
- Princípio central de adversarialidade: o agente que verifica um finding nunca é o que o encontrou; severity exige impacto (likelihood × impacto, não desvio de checklist); gaps de defense-in-depth são hardening notes, não vulnerabilidades.
- Execuções múltiplas são aditivas: o skill reaproveita ledgers e findings anteriores para mirar lacunas e revalidar código alterado — em testes, uma única rodada achou ~metade das vulnerabilidades que rodadas repetidas acharam no total.
- Segurança operacional: execução de código do alvo exige sandbox enforced pelo OS (rede externa desabilitada, ambiente allowlist, limites de recursos, escrita só em scratch); sem isso, leads ficam em needs_validation em vez de serem executados.
- Inclui validadores zero-dependency (validate-findings.cjs, validate-coverage-ledger.cjs) rodados em checkpoints das fases, e bibliotecas de prompts por classe de ataque (web/auth, memory-safety/binário, prompt-injection/LLM, supply chain, cloud/IaC, client-side, exaustão de recursos, isolamento de dados, IPC local).

## Links
- https://github.com/cloudflare/security-audit-skill

## Entidades
Cloudflare, security-audit-skill, Skills CLI, Node.js

> **Revisit:** `high` · **fonte:** `article`
