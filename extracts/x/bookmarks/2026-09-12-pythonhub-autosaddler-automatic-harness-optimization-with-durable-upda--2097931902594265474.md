---
title: "Otimização automática de agent harness"
type: "extract"
source: "x"
status_id: "2097931902594265474"
handle: "PythonHub"
url: "https://x.com/PythonHub/status/2097931902594265474"
created_at: "2026-09-10T06:15:17.000Z"
extracted: "2026-09-13"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-12-pythonhub-autosaddler-automatic-harness-optimization-with-durable-upda--2097931902594265474.json]]"
tags: ["agents", "agent-tooling", "agent-loop", "harness", "harness-engineering", "evals", "tracing"]
topic: "Otimização automática de agent harness"
summary: "AutoSaddler (Microsoft) melhora automaticamente harnesses de agentes LLM diagnosticando traces de execução e aplicando patches estruturados em prompts, ferramentas e middleware, com ganhos de +9 a +10 pp de Pass@1 em GAIA2, SWE-Bench Pro e Terminal-Bench 2.0. Código aberto (MIT) com engine V2 durável e plugin-based."
key_points: ["Ganhos reportados: GAIA2 53.0→62.0 (+9.0 pp, ReAct default), SWE-Bench Pro 37.3→46.9 (+9.6 pp, SWE-agent) e Terminal-Bench 2.0 40.0→50.0 (+10.0 pp, Terminus 2).", "Otimiza o harness completo — prompts, definições/implementações de ferramentas, middleware hooks e lógica do agent loop — via taxonomia explícita de patches Capability vs Steering, em vez de edição irrestrita.", "Ciclo com três sessões: Diagnosis-Patch (causa-raiz em traces e no codebase), Reflection (classifica fixed/regressed/still-failing e registra lições) e Evolution (sintetiza candidatos pelo EvoDAG); candidatos são verificados em treino e gateados no split de desenvolvimento.", "Execução durável: eventos append-only, provenance imutável, estado resumível, candidatos content-addressed; config fail-closed que só reusa run ID com inputs byte-identical, e suporte a fork de checkpoints.", "V2 é plugin-based (scenario plugins para pares harness/benchmark, ex.: fake e Meta-ARE/GAIA2) com providers fake, Anthropic Claude Agent SDK, GitHub Copilot SDK e Codex CLI; V1 retido para reprodução do paper (arXiv 2608.23041)."]
entities: ["AutoSaddler", "Microsoft", "GAIA2", "SWE-Bench Pro", "Terminal-Bench 2.0", "SWE-agent", "Terminus 2", "Meta-ARE", "EvoDAG", "Anthropic Claude Agent SDK", "GitHub Copilot SDK", "Codex CLI", "gpt-4.1-mini", "claude-opus-4-6", "arXiv"]
content_type: "tool"
revisit: "high"
grounded_in: "article"
links: ["https://github.com/microsoft/AutoSaddler"]
media: []
thin: false
relates-to: ["[[extracts/x/bookmarks/2026-09-12-sumanth_077-bytedance-dropped-a-banger-paper-on-self-evolving-agent-harn--2098053941800100294|HarnessDev: self-evolving agent harnesses]]", "[[extracts/x/bookmarks/2026-09-12-dair_ai-harness-of-harness-exciting-new-research-on-coding-agents-th--2095172426925801608|Harness-of-Harness: agentes de código autônomos]]", "[[extracts/x/bookmarks/2026-09-12-omarsar0-find-the-whole-collection-here-https-t-co-hskmmhjf1l--2097449134202503657|Harness engineering evolução curada]]", "[[extracts/x/bookmarks/2026-09-12-svpino-the-frontieragent-framework-is-here-star-the-repo-https-t-co--2098489264749334565|FrontierAgent: runtime de agentes e evals]]", "[[extracts/x/bookmarks/2026-09-19-omarsar0-build-your-own-harness-folks-this-is-absolute-banger-paper-f--2101074795643494546|SoL-Pi: harness de agente auto-evolutivo]]", "[[extracts/x/bookmarks/2026-09-14-shreyanshpatni_-want-to-build-a-domain-specific-agent-harness-this-is-a-grea--2099180288668750246|Construção de harness para agentes]]", "[[extracts/x/bookmarks/2026-09-12-dabit3-fusion-is-the-most-efficient-frontier-harness-for-gpt-6-astr--2098557144580735156|Harness Fusion para modelos frontier]]", "[[extracts/x/bookmarks/2026-09-12-maxforai-nvidia-harness-sol-pi-nvlabs-sol-pi-scaling-auto-research-lo--2098050525279478059|NVIDIA open-sources SoL-Pi agent harness]]"]
theme: "Agentes autônomos de engenharia"
---

# Otimização automática de agent harness

**@PythonHub** · [2097931902594265474](https://x.com/PythonHub/status/2097931902594265474) · `tool`

## Resumo
AutoSaddler (Microsoft) melhora automaticamente harnesses de agentes LLM diagnosticando traces de execução e aplicando patches estruturados em prompts, ferramentas e middleware, com ganhos de +9 a +10 pp de Pass@1 em GAIA2, SWE-Bench Pro e Terminal-Bench 2.0. Código aberto (MIT) com engine V2 durável e plugin-based.

## Pontos-chave
- Ganhos reportados: GAIA2 53.0→62.0 (+9.0 pp, ReAct default), SWE-Bench Pro 37.3→46.9 (+9.6 pp, SWE-agent) e Terminal-Bench 2.0 40.0→50.0 (+10.0 pp, Terminus 2).
- Otimiza o harness completo — prompts, definições/implementações de ferramentas, middleware hooks e lógica do agent loop — via taxonomia explícita de patches Capability vs Steering, em vez de edição irrestrita.
- Ciclo com três sessões: Diagnosis-Patch (causa-raiz em traces e no codebase), Reflection (classifica fixed/regressed/still-failing e registra lições) e Evolution (sintetiza candidatos pelo EvoDAG); candidatos são verificados em treino e gateados no split de desenvolvimento.
- Execução durável: eventos append-only, provenance imutável, estado resumível, candidatos content-addressed; config fail-closed que só reusa run ID com inputs byte-identical, e suporte a fork de checkpoints.
- V2 é plugin-based (scenario plugins para pares harness/benchmark, ex.: fake e Meta-ARE/GAIA2) com providers fake, Anthropic Claude Agent SDK, GitHub Copilot SDK e Codex CLI; V1 retido para reprodução do paper (arXiv 2608.23041).

## Links
- https://github.com/microsoft/AutoSaddler

## Entidades
AutoSaddler, Microsoft, GAIA2, SWE-Bench Pro, Terminal-Bench 2.0, SWE-agent, Terminus 2, Meta-ARE, EvoDAG, Anthropic Claude Agent SDK, GitHub Copilot SDK, Codex CLI, gpt-4.1-mini, claude-opus-4-6, arXiv

> **Revisit:** `high` · **fonte:** `article`
