---
title: "DevTools para engenharia agêntica"
type: "extract"
source: "x"
status_id: "2098398242727940442"
handle: "akshay_pachaar"
url: "https://x.com/akshay_pachaar/status/2098398242727940442"
created_at: "2026-09-11T13:08:22.000Z"
extracted: "2026-09-13"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-12-akshay_pachaar-karpathys-agentic-engineering-finally-has-proper-devtools-wh--2098398242727940442.json]]"
tags: ["agents", "agent-tooling", "observability", "tracing", "monitoramento"]
topic: "DevTools para engenharia agêntica"
summary: "Tweet anunciando DevTools da CopilotKit para debugar agentes, com o argumento central de que falhas em agentes raramente são só culpa do modelo: podem ser ferramentas quebradas, conexões perdidas, mudanças de interface ou problemas anteriores na conversa. Vale salvar como referência de que debugging de agentes exige observabilidade de todo o harness, não apenas do LLM."
key_points: ["Quando um agente para de funcionar, o modelo é apenas uma das causas possíveis — diagnóstico deve cobrir todo o sistema, não só o prompt/modelo", "Causas alternativas comuns: falha de tool, perda de conexão, interface externa que mudou sem aviso, ou contexto corrompido mais cedo na conversa", "CopilotKit lançou DevTools específicos para 'Agentic Engineering' (termo popularizado por Karpathy), sugerindo maturação do ecossistema de tooling para depuração de agentes"]
entities: ["Andrej Karpathy", "CopilotKit"]
content_type: "announcement"
revisit: "medium"
grounded_in: "tweet"
links: []
media: ["https://pbs.twimg.com/amplify_video_thumb/2098398218006806529/img/SCJfvJI5lg455Xnq.jpg"]
thin: false
theme: "Agentes para engenharia de código"
relates-to: ["[[extracts/x/bookmarks/2026-09-16-ctatedev-introducing-vercel-labs-tools-for-devs-in-the-ai-era-agent-b--2099621387732140540|Vercel Labs ferramentas IA]]", "[[extracts/x/bookmarks/2026-09-16-gergelyorosz-here-s-what-openai-s-agentic-software-factory-looks-like-tod--2099945497377091902|Fábrica de software agêntica da OpenAI]]", "[[extracts/x/bookmarks/2026-09-12-hackernoon-ai-is-raising-the-baseline-for-software-engineering-this-art--2082839180736889054|AI e plataformas de engenharia]]", "[[extracts/x/bookmarks/2026-09-12-clare_liguori-i-just-published-a-manifesto-for-all-the-developers-out-ther--2097836812958097915|frontier engineering com agentes de IA]]", "[[extracts/x/bookmarks/2026-09-12-anatolikopadze-anthropic-engineer-you-re-not-supposed-to-prompt-claude-you--2080286550005358977|Sistemas que se auto-promptam em agentes]]", "[[extracts/x/bookmarks/2026-09-12-mattpocockuk-atpaawej-1-learn-to-read-code-2-learn-to-use-the-terminal-3--2097611379763007870|Habilidades fundamentais para devs na era de agentes]]", "[[extracts/x/bookmarks/2026-09-12-marwan_3atef-datadog-put-agent-observability-in-your-coding-agent-and-the--2097986925088903355|Datadog Agent Observability para coding agents]]", "[[extracts/x/bookmarks/2026-09-12-dair_ai-an-anatomy-of-cli-coding-agent-trajectories-bookmark-it-when--2076699431207154069|análise de trajetórias de agentes de código]]", "[[extracts/x/bookmarks/2026-09-17-langchain-voice-agents-are-becoming-a-bigger-part-of-customer-and-oper--2099845326928515142|Evals de voice agents em produção]]", "[[extracts/x/bookmarks/2026-09-15-shadcn-introducing-shadcn-lint-an-agent-first-linter-for-tailwind-d--2099534231114314145|shadcn/lint, linter agent-first para Tailwind]]", "[[extracts/x/bookmarks/2026-09-17-_avichawla-layers-of-observability-in-ai-systems-explained-visually-if--2100139401842250163|Camadas de observabilidade em sistemas de IA]]", "[[extracts/x/bookmarks/2026-09-12-marwan_3atef-google-cloud-put-data-agent-kit-in-the-ide-and-the-pitch-is--2097976275373531523|Data Agent Kit no IDE]]", "[[extracts/x/bookmarks/2026-09-17-chromiumdev-10-000-installs-and-counting-we-created-modern-web-guidance--2100291127005856239|Web guidance para agentes]]", "[[extracts/x/bookmarks/2026-09-15-sumanth_077-microsoft-open-sourced-an-ai-engineer-coach-ai-engineer-coac--2098785284745990298|Microsoft AI Engineer Coach]]", "[[extracts/x/bookmarks/2026-09-12-dair_ai-the-bitter-lesson-of-tool-calling-tool-calling-is-a-design-c--2086846794840019178|Comparação de métodos de tool calling]]", "[[extracts/x/bookmarks/2026-09-16-langchain-new-in-our-langsmith-essentials-course-a-capstone-weve-added--2099875992139415786|Capstone no curso LangSmith Essentials]]", "[[extracts/x/bookmarks/2026-09-12-thsottiaux-hi-astra-users-a-reset-and-a-quick-update-on-quality-issues--2098612714704891959|Correções de qualidade no Astra]]"]
---

# DevTools para engenharia agêntica

**@akshay_pachaar** · [2098398242727940442](https://x.com/akshay_pachaar/status/2098398242727940442) · `announcement`

## Resumo
Tweet anunciando DevTools da CopilotKit para debugar agentes, com o argumento central de que falhas em agentes raramente são só culpa do modelo: podem ser ferramentas quebradas, conexões perdidas, mudanças de interface ou problemas anteriores na conversa. Vale salvar como referência de que debugging de agentes exige observabilidade de todo o harness, não apenas do LLM.

## Pontos-chave
- Quando um agente para de funcionar, o modelo é apenas uma das causas possíveis — diagnóstico deve cobrir todo o sistema, não só o prompt/modelo
- Causas alternativas comuns: falha de tool, perda de conexão, interface externa que mudou sem aviso, ou contexto corrompido mais cedo na conversa
- CopilotKit lançou DevTools específicos para 'Agentic Engineering' (termo popularizado por Karpathy), sugerindo maturação do ecossistema de tooling para depuração de agentes

## Entidades
Andrej Karpathy, CopilotKit

> **Revisit:** `medium` · **fonte:** `tweet`
