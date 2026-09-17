---
title: "Skill de segurança da Cloudflare"
type: "extract"
source: "x"
status_id: "2099560068362441009"
handle: "mstrYoda_"
url: "https://x.com/mstrYoda_/status/2099560068362441009"
created_at: "2026-09-14T18:05:02.000Z"
extracted: "2026-09-17"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-17-mstryoda_-cloudflare-ai-agentlar-icin-security-skill-yaynlams-direkt-y--2099560068362441009.json]]"
tags: ["agents", "agent-tooling", "multi-agent", "harness", "verification", "code-review"]
topic: "Skill de segurança da Cloudflare"
summary: "Cloudflare lançou o security-audit-skill, um skill para coding agents que os transforma em auditores de segurança via pipeline de 6 fases com hunters e verifiers isolados; é o ponto de partida single-repo do harness de descoberta de vulnerabilidades da empresa, instalável com npx skills add."
key_points: ["Pipeline de auditoria em 6 fases: reconhecimento (architecture.md + coverage-ledger.json), caça guiada por cobertura com hunters isolados e coverage critics, validação adversarial (verifier fresco tenta disprovar cada candidato), saída estruturada (findings.json validado contra report-schema.json), verificação independente de registros e relatório target-neutral.", "Disciplina de verdicts: confirmed exige source trace completo e resultado observado delimitado; needs_validation carrega o fato não resolvido exato e sem severidade; rejected registra candidato disprovado. Severidade exige impacto (likelihood × impact); gaps de defense-in-depth são hardening notes, não vulnerabilidades.", "Execuções múltiplas são aditivas e stateful: o skill reusa ledgers e findings anteriores para mirar gaps, revalidar código alterado e carregar evidência de fonte atual; em testes, uma única run achou ~metade das vulnerabilidades que runs repetidas acharam no total.", "Exige sandbox enforced pelo SO (rede externa desabilitada, ambiente allowlisted, limits de recursos, writes só em scratch paths) para executar código do alvo; sem isso, leads permanecem como needs_validation em vez de serem executados.", "Documentação modular por classe de ataque: memory-safety/binary, prompt-injection e agent/tool para alvos LLM, protocolos HTTP/auth, client-side, supply chain/release, cloud/IaC, RPC/messaging, resource exhaustion, data isolation e desktop/mobile IPC."]
entities: ["Cloudflare", "security-audit-skill", "Skills CLI", "Node.js", "GitHub"]
content_type: "tool"
revisit: "high"
grounded_in: "article"
thin: false
links: ["https://github.com/cloudflare/security-audit-skill"]
media: []
relates-to: ["[[extracts/x/bookmarks/2026-09-12-poteto-pstack-now-includes-2-skills-i-recommend-everyone-use-or-cop--2082874054483255805|Skill de verificação para agentes]]", "[[extracts/x/bookmarks/2026-09-12-thsottiaux-more-opensource-goodness-we-have-just-released-a-cli-and-typ--2082241164850364555|Codex Security CLI e SDK]]", "[[extracts/x/bookmarks/2026-09-12-steipete-hit-a-new-record-with-our-autoreview-skill-66-rounds-on-a-gn--2080899298838098034|Autoreview: code review multi-engine]]", "[[extracts/x/bookmarks/2026-09-14-cyrilxbt-every-department-installable-developers-superpowers-https-t--2098652326248493447|Superpowers: metodologia para coding agents]]", "[[extracts/x/bookmarks/2026-09-12-mattpocockuk-mattpocock-skills-v1-2-is-out-we-re-now-the-19th-most-starre--2084985277102031137|Lançamento mattpocock/skills v1.2]]", "[[extracts/x/bookmarks/2026-09-12-openai-we-quietly-released-the-open-source-codex-security-cli-but-h--2082263717916586117|Codex Security CLI open-source]]", "[[extracts/x/bookmarks/2026-09-12-pythonhub-tencent-opensource-ai-red-teaming-platform-a-full-stack-ai-r--2092420578875527174|Plataforma open-source de AI red teaming]]", "[[extracts/x/bookmarks/2026-09-12-eric_wallace_-today-we-are-releasing-gpt-5-6-cyber-the-model-is-our-first--2086866306167656901|Lançamento de modelo de cibersegurança]]", "[[extracts/x/bookmarks/2026-09-16-thehackersnews-attackers-stole-a-metr-api-key-and-used-it-for-three-weeks-c--2094713437930787192|Vazamento de chave API da METR]]"]
theme: "Claude Code e Coding Agêntico"
---

# Skill de segurança da Cloudflare

**@mstrYoda_** · [2099560068362441009](https://x.com/mstrYoda_/status/2099560068362441009) · `tool`

## Resumo
Cloudflare lançou o security-audit-skill, um skill para coding agents que os transforma em auditores de segurança via pipeline de 6 fases com hunters e verifiers isolados; é o ponto de partida single-repo do harness de descoberta de vulnerabilidades da empresa, instalável com npx skills add.

## Pontos-chave
- Pipeline de auditoria em 6 fases: reconhecimento (architecture.md + coverage-ledger.json), caça guiada por cobertura com hunters isolados e coverage critics, validação adversarial (verifier fresco tenta disprovar cada candidato), saída estruturada (findings.json validado contra report-schema.json), verificação independente de registros e relatório target-neutral.
- Disciplina de verdicts: confirmed exige source trace completo e resultado observado delimitado; needs_validation carrega o fato não resolvido exato e sem severidade; rejected registra candidato disprovado. Severidade exige impacto (likelihood × impact); gaps de defense-in-depth são hardening notes, não vulnerabilidades.
- Execuções múltiplas são aditivas e stateful: o skill reusa ledgers e findings anteriores para mirar gaps, revalidar código alterado e carregar evidência de fonte atual; em testes, uma única run achou ~metade das vulnerabilidades que runs repetidas acharam no total.
- Exige sandbox enforced pelo SO (rede externa desabilitada, ambiente allowlisted, limits de recursos, writes só em scratch paths) para executar código do alvo; sem isso, leads permanecem como needs_validation em vez de serem executados.
- Documentação modular por classe de ataque: memory-safety/binary, prompt-injection e agent/tool para alvos LLM, protocolos HTTP/auth, client-side, supply chain/release, cloud/IaC, RPC/messaging, resource exhaustion, data isolation e desktop/mobile IPC.

## Links
- https://github.com/cloudflare/security-audit-skill

## Entidades
Cloudflare, security-audit-skill, Skills CLI, Node.js, GitHub

> **Revisit:** `high` · **fonte:** `article`
