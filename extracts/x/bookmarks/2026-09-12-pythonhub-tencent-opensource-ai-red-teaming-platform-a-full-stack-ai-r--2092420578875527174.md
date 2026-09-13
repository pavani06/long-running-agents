---
title: "Plataforma open-source de AI red teaming"
type: "extract"
source: "x"
status_id: "2092420578875527174"
handle: "PythonHub"
url: "https://x.com/PythonHub/status/2092420578875527174"
created_at: "2026-08-26T01:15:15.000Z"
extracted: "2026-09-13"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-12-pythonhub-tencent-opensource-ai-red-teaming-platform-a-full-stack-ai-r--2092420578875527174.json]]"
tags: ["agents", "agent-tooling", "evals", "testes-qa", "monitoramento"]
topic: "Plataforma open-source de AI red teaming"
summary: "A.I.G (AI-Infra-Guard), do Tencent Zhuque Lab, é uma plataforma open-source (Apache 2.0) de red teaming de IA que escaneia agentes, servidores MCP, skills, infraestrutura de IA e avalia jailbreaks de LLMs. Vale salvar como ferramenta concreta de segurança para ecossistemas de agentes, com CLIs integráveis em CI/CD e framework de plugins extensível."
key_points: ["Cinco módulos principais: ClawScan (segurança OpenClaw), Agent Scan (fluxos de agentes em Dify e Coze), MCP Server & Skills scan (14 categorias de risco), AI Infra scan (100+ componentes como vLLM, Ollama, ComfyUI, n8n, Triton; 2000+ CVEs) e Jailbreak Evaluation com ataques multi-turn (Many-Shot, PAIR, GOAT, ActorAttack).", "Skill-Scan CLI integrável em pipelines CI/CD usa a taxonomia SkillTrustBench T01–T09 (hijacking de instrução, memory poisoning, execução remota de payload, escalada de privilégio, dependências inseguras); melhor F1 de 0.9848 com Claude Opus 4.6.", "API Checker faz fingerprinting de modelos, detecção de envenenamento de LLM/API (substituição de modelo e backdoor via múltiplas sondas black-box) e auditoria de relays; versão v4.6.0+ expandiu cobertura para GLM, Gemini, Gemma e DeepSeek.", "Deploy via Docker (web UI na porta 8088) e framework de plugins extensível (fingerprints YAML, regras de vulnerabilidade, datasets de jailbreak via PR); atenção: sem mecanismo de autenticação — apenas uso interno, nunca exposto em rede pública.", "Desenvolvido pelo Tencent Zhuque Lab (fundado em 2019), com vulnerabilidades corrigidas e reconhecimento público por NVIDIA, Google, Microsoft e comunidades como Linux e Hugging Face; existe versão Pro por convite para contribuidores."]
entities: ["Tencent", "Tencent Zhuque Lab", "A.I.G (AI-Infra-Guard)", "SkillTrustBench", "OpenClaw", "ClawHub", "Dify", "Coze", "vLLM", "Ollama", "ComfyUI", "n8n", "Triton Inference Server", "Docker", "Claude Opus 4.6", "DeepSeek"]
content_type: "tool"
revisit: "high"
grounded_in: "article"
links: ["https://github.com/tencent/AI-Infra-Guard"]
media: []
---

# Plataforma open-source de AI red teaming

**@PythonHub** · [2092420578875527174](https://x.com/PythonHub/status/2092420578875527174) · `tool`

## Resumo
A.I.G (AI-Infra-Guard), do Tencent Zhuque Lab, é uma plataforma open-source (Apache 2.0) de red teaming de IA que escaneia agentes, servidores MCP, skills, infraestrutura de IA e avalia jailbreaks de LLMs. Vale salvar como ferramenta concreta de segurança para ecossistemas de agentes, com CLIs integráveis em CI/CD e framework de plugins extensível.

## Pontos-chave
- Cinco módulos principais: ClawScan (segurança OpenClaw), Agent Scan (fluxos de agentes em Dify e Coze), MCP Server & Skills scan (14 categorias de risco), AI Infra scan (100+ componentes como vLLM, Ollama, ComfyUI, n8n, Triton; 2000+ CVEs) e Jailbreak Evaluation com ataques multi-turn (Many-Shot, PAIR, GOAT, ActorAttack).
- Skill-Scan CLI integrável em pipelines CI/CD usa a taxonomia SkillTrustBench T01–T09 (hijacking de instrução, memory poisoning, execução remota de payload, escalada de privilégio, dependências inseguras); melhor F1 de 0.9848 com Claude Opus 4.6.
- API Checker faz fingerprinting de modelos, detecção de envenenamento de LLM/API (substituição de modelo e backdoor via múltiplas sondas black-box) e auditoria de relays; versão v4.6.0+ expandiu cobertura para GLM, Gemini, Gemma e DeepSeek.
- Deploy via Docker (web UI na porta 8088) e framework de plugins extensível (fingerprints YAML, regras de vulnerabilidade, datasets de jailbreak via PR); atenção: sem mecanismo de autenticação — apenas uso interno, nunca exposto em rede pública.
- Desenvolvido pelo Tencent Zhuque Lab (fundado em 2019), com vulnerabilidades corrigidas e reconhecimento público por NVIDIA, Google, Microsoft e comunidades como Linux e Hugging Face; existe versão Pro por convite para contribuidores.

## Links
- https://github.com/tencent/AI-Infra-Guard

## Entidades
Tencent, Tencent Zhuque Lab, A.I.G (AI-Infra-Guard), SkillTrustBench, OpenClaw, ClawHub, Dify, Coze, vLLM, Ollama, ComfyUI, n8n, Triton Inference Server, Docker, Claude Opus 4.6, DeepSeek

> **Revisit:** `high` · **fonte:** `article`
