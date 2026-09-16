---
title: "Fábrica de software agêntica da OpenAI"
type: "extract"
source: "x"
status_id: "2099945497377091902"
handle: "GergelyOrosz"
url: "https://x.com/GergelyOrosz/status/2099945497377091902"
created_at: "2026-09-15T19:36:36.000Z"
extracted: "2026-09-16"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-16-gergelyorosz-here-s-what-openai-s-agentic-software-factory-looks-like-tod--2099945497377091902.json]]"
tags: ["agentic-coding", "agents", "harness-engineering", "code-review", "performance", "production", "observability", "analise"]
topic: "Fábrica de software agêntica da OpenAI"
summary: "Reportagem interna baseada em entrevistas com 7 líderes de engenharia da OpenAI sobre como o Codex virou o harness de toda a empresa: adoção de ~90% por não-engenheiros em meses, morte gradual de IDEs e PRs tradicionais, e loops agênticos automatizados como a Perf Factory corrigindo produção. Vale salvar como retrato concreto de como engenharia de software se reorganiza em torno de agentes."
key_points: ["Codex e ChatGPT Work tomaram conta da OpenAI sem mandato: orgs não-engenharia (finanças, legal, recrutamento) saltaram de ~0% para 90% de adoção em 4 meses; o /goal e melhor manejo de tarefas longas (threads que rodam por dias) foram gatilhos do salto de 60% para 90%.", "Perf Factory: loop agêntico automatizado que monitora produção e dispara agentes Codex para corrigir problemas de performance sem intervenção humana — exemplo central da 'software factory' com múltiplos feedback loops agênticos.", "PRs por engenheiro crescem em curva de hockey stick: ~10x de carga em ~6 meses em partes do pipeline build-test-deploy (vs. 2-3 anos em empresas típicas), forçando repensar CI/CD, observabilidade e code review; revisões agênticas multi-lentes (ex.: infra + segurança em todo change) e um agente que acompanha o deploy até produção e constrói os próprios dashboards de monitoramento.", "Uso de IDE cai desde janeiro: a aposta do app Codex (entre terminal e IDE, sem forkar VS Code, apesar do Antigravity) validou-se; ferramentas internas artesanais são substituídas pelo Codex, que passa a ser preferido até para debugging, e eficiência do harness vira fator crítico.", "Adoção acelerada por plugins/skills específicos por papel e time ('não se entrega uma caixa vazia'), e especialistas de domínio embedados nos times de engenharia do ChatGPT Work para canalizar 'gosto' onde os modelos já superam os devs; dependência total é tamanha que mensagens humanas alertam o time antes dos alertas automatizados em outages."]
entities: ["OpenAI", "Codex", "ChatGPT Work", "Perf Factory", "Gergely Orosz", "The Pulse", "Venkat Venkataramani", "Sulman Choudhry", "Andrew Ambrosino", "Joe Gershenson", "Akshay Nathan", "Ahmed Ibrahim", "Steve Coffey", "Ramp Inspect AI", "Antigravity", "VS Code"]
content_type: "resource"
revisit: "high"
grounded_in: "article"
thin: false
links: ["https://newsletter.pragmaticengineer.com/p/openai-software-factory"]
media: ["https://pbs.twimg.com/media/HSSBIdfWEAAbXl8.jpg"]
---

# Fábrica de software agêntica da OpenAI

**@GergelyOrosz** · [2099945497377091902](https://x.com/GergelyOrosz/status/2099945497377091902) · `resource`

## Resumo
Reportagem interna baseada em entrevistas com 7 líderes de engenharia da OpenAI sobre como o Codex virou o harness de toda a empresa: adoção de ~90% por não-engenheiros em meses, morte gradual de IDEs e PRs tradicionais, e loops agênticos automatizados como a Perf Factory corrigindo produção. Vale salvar como retrato concreto de como engenharia de software se reorganiza em torno de agentes.

## Pontos-chave
- Codex e ChatGPT Work tomaram conta da OpenAI sem mandato: orgs não-engenharia (finanças, legal, recrutamento) saltaram de ~0% para 90% de adoção em 4 meses; o /goal e melhor manejo de tarefas longas (threads que rodam por dias) foram gatilhos do salto de 60% para 90%.
- Perf Factory: loop agêntico automatizado que monitora produção e dispara agentes Codex para corrigir problemas de performance sem intervenção humana — exemplo central da 'software factory' com múltiplos feedback loops agênticos.
- PRs por engenheiro crescem em curva de hockey stick: ~10x de carga em ~6 meses em partes do pipeline build-test-deploy (vs. 2-3 anos em empresas típicas), forçando repensar CI/CD, observabilidade e code review; revisões agênticas multi-lentes (ex.: infra + segurança em todo change) e um agente que acompanha o deploy até produção e constrói os próprios dashboards de monitoramento.
- Uso de IDE cai desde janeiro: a aposta do app Codex (entre terminal e IDE, sem forkar VS Code, apesar do Antigravity) validou-se; ferramentas internas artesanais são substituídas pelo Codex, que passa a ser preferido até para debugging, e eficiência do harness vira fator crítico.
- Adoção acelerada por plugins/skills específicos por papel e time ('não se entrega uma caixa vazia'), e especialistas de domínio embedados nos times de engenharia do ChatGPT Work para canalizar 'gosto' onde os modelos já superam os devs; dependência total é tamanha que mensagens humanas alertam o time antes dos alertas automatizados em outages.

## Links
- https://newsletter.pragmaticengineer.com/p/openai-software-factory

## Entidades
OpenAI, Codex, ChatGPT Work, Perf Factory, Gergely Orosz, The Pulse, Venkat Venkataramani, Sulman Choudhry, Andrew Ambrosino, Joe Gershenson, Akshay Nathan, Ahmed Ibrahim, Steve Coffey, Ramp Inspect AI, Antigravity, VS Code

> **Revisit:** `high` · **fonte:** `article`
