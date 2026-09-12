---
title: "Why Your Enterprise Tech Stack Isn’t Ready for AI Agents — Christopher Lovejoy & Saul Howard"
type: "extract"
source: "youtube"
video_id: "mav15aW9lLM"
url: "https://www.youtube.com/watch?v=mav15aW9lLM"
channel: "AI Engineer"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-why-your-enterprise-tech-stack-isnt-ready-for-ai-agents-christopher-lovejoy-saul--mav15aW9lLM.txt]]"
tags: ["arquitetura", "context-engineering", "data-platform", "escalation", "evals", "governanca", "observability", "permissions", "production", "state", "agents"]
thesis: "Stacks corporativos não estão prontos para agentes de IA em setores regulados, e é preciso construir sobre primitivas arquiteturais — ledger imutável de eventos, object storage de dados sensíveis com zero trust, equivalência humano-agente — para que auditoria, escalonamento e evals emerjam como propriedades de primeira classe em vez de remendos sobre um POC."
concepts: ["POC-to-production gap em enterprise", "audit trail vs. log de desenvolvedor", "event sourcing / transaction log imutável", "projeções efêmeras computadas do event log", "schema-driven object storage", "PHI (protected health information)", "RBAC para humanos e agentes", "zero trust com bearer tokens", "prompt injection / lethal trifecta", "escalonamento dinâmico para humanos", "equivalência humano-agente", "definição compartilhada de contexto mapeada para prompt ou UI", "evals privacy-preserving por replay do ledger", "comparação humano vs. agente como eval", "drift de dados offline vs. produção", "arquitetura como escolha do que deve ser simples", "restrições de produção como princípios arquiteturais"]
tools: ["Datadog", "Epic", "Salesforce"]
people: ["Christopher Lovejoy (Anthropic)", "Saul (Anterior)", "Anthropic", "Anterior"]
claims: ["Modele a auditoria como um event log append-only imutável e unificado, para que a auditabilidade caia naturalmente do paradigma de armazenamento (fonte única de verdade, replay de qualquer ponto no tempo).", "Aceite o trade-off do event sourcing: escritas triviais, leituras mais custosas, mitigáveis com caching e snapshots; views são projeções efêmeras recomputáveis quando a interpretação muda.", "Armazene dados sensíveis (PHI) em blobs imutáveis com schema em object storage, mantendo nos eventos apenas referências, permitindo debug e observabilidade sem expor os dados sensíveis.", "Aplique zero trust no object storage: agentes portam bearer tokens e acessam dados só no ponto de uso, impedindo fluxo livre de dados e mitigando a trifeta letal do prompt injection.", "Trate humanos e LLMs como agentes equivalentes na plataforma: qualquer ação executável pelo LLM pode ser escalonada a um humano, e passos downstream são agnósticos a quem executou.", "Defina métodos sobre um contexto compartilhado que renderizem tanto em prompt (LLM) quanto em UI (humano), resolvendo a diferença de processamento de contexto entre humanos e modelos.", "Derive evals dos primitivos sem bolt-on: replay do ledger para isolar efeitos de mudanças de prompt/modelo/código; comparar desempenho humano vs. agente na mesma tarefa; rodar evals dentro do ambiente do cliente sem expor dados sensíveis.", "Não leve o POC de alta acurácia para produção acrescentando requisitos corporativos por cima; comece pelas restrições de produção como princípios arquiteturais e reconstrua a acurácia do POC sobre os novos primitivos.", "Reutilize padrões provados em finanças, defesa e big tech (ex.: transaction log) combinando-os de formas novas para agentes, em vez de inventar tudo do zero."]
deep_dive: "high"
deep_dive_reason: "Alta densidade de primitivas arquiteturais acionáveis com trade-offs explícitos (event sourcing, object storage com zero trust, equivalência humano-agente, evals emergentes por replay), diretamente relevantes a harness, governança, evals e engenharia de contexto em produção."
---

# Why Your Enterprise Tech Stack Isn’t Ready for AI Agents — Christopher Lovejoy & Saul Howard

## Tese
Stacks corporativos não estão prontos para agentes de IA em setores regulados, e é preciso construir sobre primitivas arquiteturais — ledger imutável de eventos, object storage de dados sensíveis com zero trust, equivalência humano-agente — para que auditoria, escalonamento e evals emerjam como propriedades de primeira classe em vez de remendos sobre um POC.

## Conceitos-chave
- POC-to-production gap em enterprise
- audit trail vs. log de desenvolvedor
- event sourcing / transaction log imutável
- projeções efêmeras computadas do event log
- schema-driven object storage
- PHI (protected health information)
- RBAC para humanos e agentes
- zero trust com bearer tokens
- prompt injection / lethal trifecta
- escalonamento dinâmico para humanos
- equivalência humano-agente
- definição compartilhada de contexto mapeada para prompt ou UI
- evals privacy-preserving por replay do ledger
- comparação humano vs. agente como eval
- drift de dados offline vs. produção
- arquitetura como escolha do que deve ser simples
- restrições de produção como princípios arquiteturais

## Ferramentas & pessoas
**Ferramentas:** Datadog, Epic, Salesforce

**Pessoas/orgs:** Christopher Lovejoy (Anthropic), Saul (Anterior), Anthropic, Anterior

## Claims acionáveis
- Modele a auditoria como um event log append-only imutável e unificado, para que a auditabilidade caia naturalmente do paradigma de armazenamento (fonte única de verdade, replay de qualquer ponto no tempo).
- Aceite o trade-off do event sourcing: escritas triviais, leituras mais custosas, mitigáveis com caching e snapshots; views são projeções efêmeras recomputáveis quando a interpretação muda.
- Armazene dados sensíveis (PHI) em blobs imutáveis com schema em object storage, mantendo nos eventos apenas referências, permitindo debug e observabilidade sem expor os dados sensíveis.
- Aplique zero trust no object storage: agentes portam bearer tokens e acessam dados só no ponto de uso, impedindo fluxo livre de dados e mitigando a trifeta letal do prompt injection.
- Trate humanos e LLMs como agentes equivalentes na plataforma: qualquer ação executável pelo LLM pode ser escalonada a um humano, e passos downstream são agnósticos a quem executou.
- Defina métodos sobre um contexto compartilhado que renderizem tanto em prompt (LLM) quanto em UI (humano), resolvendo a diferença de processamento de contexto entre humanos e modelos.
- Derive evals dos primitivos sem bolt-on: replay do ledger para isolar efeitos de mudanças de prompt/modelo/código; comparar desempenho humano vs. agente na mesma tarefa; rodar evals dentro do ambiente do cliente sem expor dados sensíveis.
- Não leve o POC de alta acurácia para produção acrescentando requisitos corporativos por cima; comece pelas restrições de produção como princípios arquiteturais e reconstrua a acurácia do POC sobre os novos primitivos.
- Reutilize padrões provados em finanças, defesa e big tech (ex.: transaction log) combinando-os de formas novas para agentes, em vez de inventar tudo do zero.

> **Deep dive:** `high` — Alta densidade de primitivas arquiteturais acionáveis com trade-offs explícitos (event sourcing, object storage com zero trust, equivalência humano-agente, evals emergentes por replay), diretamente relevantes a harness, governança, evals e engenharia de contexto em produção.
