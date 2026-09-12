---
title: "CI/CD Is Dead, Agents Need Continuous Compute and Computers — Hugo Santos and Madison Faulkner"
type: "extract"
source: "youtube"
video_id: "VktrqzQgytY"
url: "https://www.youtube.com/watch?v=VktrqzQgytY"
channel: "AI Engineer"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-ci-cd-is-dead-agents-need-continuous-compute-and-computers-hugo-santos-and-madis--VktrqzQgytY.txt]]"
tags: ["agentic-coding", "agent-loop", "harness", "arquitetura", "code-review", "governanca", "state", "evals", "verification", "multi-agent", "agent-fleets", "stack-tooling", "testes-qa", "gate-design", "escalation", "memory-architecture", "runtime"]
thesis: "O desenvolvimento agêntico quebra as premissas de escala humana do CI/CD, exigindo uma arquitetura de 'continuous compute' em que a validação (builds/tests e agentes avaliadores) roda continuamente dentro do loop do agente, o merge se torna um problema de serialização/ledger com filas de premerge, e humanos aprovam apenas intenção-versus-resultado."
concepts: ["continuous compute como substituto do CI/CD", "agentes monolíticos evoluindo para microsserviços de agentes", "PR como unidade de trabalho desenhada para revisão humana com feedback demorado", "latência humana mascarando a lentidão das máquinas de validação", "repositório git como ledger e merge como problema de serialização/lock de banco de dados de alta performance", "time-to-merge como métrica crítica conforme a taxa de mudança aumenta", "intenção e plano codificados como spec alimentando o loop de um agent harness", "validação interna contínua usando os ativos do repositório (build/test) a cada iteração", "validação externa por agentes especializados (LLM de segurança, LLM de conformidade de API)", "fila de premerge com reconciliação para garantir serializabilidade entre agentes paralelos", "agrupamento semântico de múltiplas mudanças de agentes em unidades aprováveis por humanos", "ambientes stateful com memória/estado quente para eliminar cold starts no loop", "multiverse: agentes ramificando e trabalhando a partir de múltiplos commits simultaneamente", "invariantes (checkout bem conhecido, compliance) aplicados continuamente em vez de fase separada", "governança elevada ao harness e coordenação saindo do CI", "cache como camada de orquestração via codesign hardware/software, com ingress shaping, rate limiting, identidade agêntica e retries em escala"]
tools: ["Namespace", "GitHub / GitHub Actions", "GitHub Copilot", "HashiCorp", "Claude Code", "Amp", "Cursor", "Factory", "Linear", "Slack", "Git"]
people: ["Madison (NEA)", "Hugo Santos (Namespace)", "Mitchell Hashimoto (HashiCorp)", "NEA", "Google", "Meta AI", "fal", "Zed", "Ramp"]
claims: ["Com agentes, o volume de 'PRs' cresce cerca de 4x e torna a revisão humana de cada diff impossível; a validação precisa migrar para o loop interno", "Trate o repositório git como um ledger e o merge como problema de serialização com lock curto; minimize o time-to-merge porque a taxa de mudanças explode", "Comece o fluxo por intenção/plano codificado em spec (ticket Linear, Slack) alimentando um harness agêntico (Claude Code, Amp, Cursor, Factory), em vez de fluxo PR-first", "Force checkout de commit bem conhecido e validação com os ativos do repositório (build+test) em cada iteração, mantendo invariantes de compliance de forma contínua", "Builds e tests precisam rodar em segundos/minutos — não 15-45 minutos — pois atrasam todo o loop; use ambientes stateful e caches quentes para nunca recomeçar do zero", "Substitua revisores humanos por agentes avaliadores especializados (segurança, conformidade de API) que devolvem feedback dentro do loop", "Introduza uma fila de premerge com processo de reconciliação para garantir serializabilidade quando muitos agentes paralelos tocam as mesmas partes do código", "Mode a aprovação externa como intenção-versus-resultado (vídeo do funcionamento, output do agente de segurança), agrupando semanticamente múltiplos diffs em vez de revisar commit a commit", "Planeje para o 'multiverse': agentes trabalhando ramificados de múltiplos commits simultaneamente, com aumento consequente de uso de recursos computacionais", "Acelere o CI existente inserindo uma camada de cache/orquestração sobre GitHub Actions (codesign hardware/software), com ingress shaping, rate limiting, identidade agêntica e retries em escala", "CI não desaparece: deixa de ser fase separada e passa a aplicação contínua de invariantes dentro do loop; a governança sobe para o harness"]
deep_dive: "high"
deep_dive_reason: "Densa em insight arquitetural acionável e novidade (merge como ledger/serialização, fila de premerge, validação contínua no loop, multiverse de commits) diretamente relevante a harness, evals, agent-fleets e governança, apesar do leve viés promocional da Namespace."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-the-pipeline-is-dead-iris-ten-teije-sky-valley-ambient-computing--bRnoEpoK5m4|The Pipeline Is Dead - Iris ten Teije, Sky Valley Ambient Computing]]", "[[extracts/youtube/ai-learning/2026-09-11-agentic-engineering-explained-by-a-10x-developer--FU5_kpTAVDo|Agentic Engineering, explained by a 10x developer]]", "[[extracts/youtube/ai-learning/2026-09-11-agent-frameworks-considered-harmful-remi-louf-txt--KHudyx5wW3U|Agent Frameworks Considered Harmful — Rémi Louf, .txt]]", "[[extracts/youtube/ai-learning/2026-09-11-loop-engineering-to-graph-engineering--BOOfy3Yshtw|Loop Engineering to Graph Engineering]]", "[[extracts/youtube/ai-learning/2026-09-11-from-coding-to-knowledge-work-agents-karan-vaidya-composio--xxfMT-bPEmU|From coding to Knowledge work agents — Karan Vaidya, Composio]]", "[[extracts/youtube/ai-learning/2026-09-11-no-vibes-allowed-solving-hard-problems-in-complex-codebases-dex-horthy-humanlaye--rmvDxxNubIg|No Vibes Allowed: Solving Hard Problems in Complex Codebases – Dex Horthy, HumanLayer]]"]
theme: "Engenharia de Agentes Confiáveis"
---

# CI/CD Is Dead, Agents Need Continuous Compute and Computers — Hugo Santos and Madison Faulkner

## Tese
O desenvolvimento agêntico quebra as premissas de escala humana do CI/CD, exigindo uma arquitetura de 'continuous compute' em que a validação (builds/tests e agentes avaliadores) roda continuamente dentro do loop do agente, o merge se torna um problema de serialização/ledger com filas de premerge, e humanos aprovam apenas intenção-versus-resultado.

## Conceitos-chave
- continuous compute como substituto do CI/CD
- agentes monolíticos evoluindo para microsserviços de agentes
- PR como unidade de trabalho desenhada para revisão humana com feedback demorado
- latência humana mascarando a lentidão das máquinas de validação
- repositório git como ledger e merge como problema de serialização/lock de banco de dados de alta performance
- time-to-merge como métrica crítica conforme a taxa de mudança aumenta
- intenção e plano codificados como spec alimentando o loop de um agent harness
- validação interna contínua usando os ativos do repositório (build/test) a cada iteração
- validação externa por agentes especializados (LLM de segurança, LLM de conformidade de API)
- fila de premerge com reconciliação para garantir serializabilidade entre agentes paralelos
- agrupamento semântico de múltiplas mudanças de agentes em unidades aprováveis por humanos
- ambientes stateful com memória/estado quente para eliminar cold starts no loop
- multiverse: agentes ramificando e trabalhando a partir de múltiplos commits simultaneamente
- invariantes (checkout bem conhecido, compliance) aplicados continuamente em vez de fase separada
- governança elevada ao harness e coordenação saindo do CI
- cache como camada de orquestração via codesign hardware/software, com ingress shaping, rate limiting, identidade agêntica e retries em escala

## Ferramentas & pessoas
**Ferramentas:** Namespace, GitHub / GitHub Actions, GitHub Copilot, HashiCorp, Claude Code, Amp, Cursor, Factory, Linear, Slack, Git

**Pessoas/orgs:** Madison (NEA), Hugo Santos (Namespace), Mitchell Hashimoto (HashiCorp), NEA, Google, Meta AI, fal, Zed, Ramp

## Claims acionáveis
- Com agentes, o volume de 'PRs' cresce cerca de 4x e torna a revisão humana de cada diff impossível; a validação precisa migrar para o loop interno
- Trate o repositório git como um ledger e o merge como problema de serialização com lock curto; minimize o time-to-merge porque a taxa de mudanças explode
- Comece o fluxo por intenção/plano codificado em spec (ticket Linear, Slack) alimentando um harness agêntico (Claude Code, Amp, Cursor, Factory), em vez de fluxo PR-first
- Force checkout de commit bem conhecido e validação com os ativos do repositório (build+test) em cada iteração, mantendo invariantes de compliance de forma contínua
- Builds e tests precisam rodar em segundos/minutos — não 15-45 minutos — pois atrasam todo o loop; use ambientes stateful e caches quentes para nunca recomeçar do zero
- Substitua revisores humanos por agentes avaliadores especializados (segurança, conformidade de API) que devolvem feedback dentro do loop
- Introduza uma fila de premerge com processo de reconciliação para garantir serializabilidade quando muitos agentes paralelos tocam as mesmas partes do código
- Mode a aprovação externa como intenção-versus-resultado (vídeo do funcionamento, output do agente de segurança), agrupando semanticamente múltiplos diffs em vez de revisar commit a commit
- Planeje para o 'multiverse': agentes trabalhando ramificados de múltiplos commits simultaneamente, com aumento consequente de uso de recursos computacionais
- Acelere o CI existente inserindo uma camada de cache/orquestração sobre GitHub Actions (codesign hardware/software), com ingress shaping, rate limiting, identidade agêntica e retries em escala
- CI não desaparece: deixa de ser fase separada e passa a aplicação contínua de invariantes dentro do loop; a governança sobe para o harness

> **Deep dive:** `high` — Densa em insight arquitetural acionável e novidade (merge como ledger/serialização, fila de premerge, validação contínua no loop, multiverse de commits) diretamente relevante a harness, evals, agent-fleets e governança, apesar do leve viés promocional da Namespace.
