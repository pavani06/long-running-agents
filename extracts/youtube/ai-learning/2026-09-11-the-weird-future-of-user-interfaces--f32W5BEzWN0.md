---
title: "The Weird Future Of User Interfaces"
type: "extract"
source: "youtube"
video_id: "f32W5BEzWN0"
url: "https://www.youtube.com/watch?v=f32W5BEzWN0"
channel: "Enrico Tartarotti"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-the-weird-future-of-user-interfaces--f32W5BEzWN0.txt]]"
tags: ["agents", "analise", "arquitetura", "agent-tooling", "stack-tooling", "process"]
thesis: "O futuro da interação não é chatbots substituindo UI, mas a coexistência de três camadas: UI tradicional com manipulação direta para tarefas simples, agentes para tarefas complexas, e generative UI — interfaces geradas pela IA sob demanda — para o meio da curva de complexidade onde está a maioria do uso real."
concepts: ["Manipulação direta como superpoder da GUI (afordância visível de todas as ações)", "Distribuição normal da complexidade das tarefas (o meio é onde está o valor)", "Generative UI nível 1: visualizações geradas on-the-spot", "Generative UI nível 2: UI base fixa com peças generativas", "Generative UI nível 3: o produto inteiro é generativo, as regras são o produto", "Mudança do design de telas para o design de regras e UI kits (blocos de Lego)", "Produtos headless e CLIs voltados a agentes, não humanos", "Adoção orgânica de coding agents por não-engenheiros", "Manipulação indireta via agentes vs manipulação direta via GUI"]
tools: ["Starbucks app", "Starbucks plugin para ChatGPT", "Humane Pin", "Rabbit", "Siri", "Alexa", "Google Home", "Meta AI (botão no WhatsApp)", "Microsoft Copilot key", "Claude Code", "Codex", "VS Code", "Remotion", "Blender", "After Effects", "Linear", "PostHog", "Salesforce (versão headless)", "Notion CLI", "Google CLI", "Google Flights (AI mode)", "Lovable", "Flask"]
people: ["Microsoft", "Humane", "Meta", "Google", "Salesforce", "Notion", "Linear", "PostHog", "Anthropic (Claude)", "Airbnb", "Brian Chesky", "Xerox PARC", "Figma"]
claims: ["Chatbots e dispositivos de voz falharam ao tentar substituir GUI para tarefas simples, habituais e de baixa complexidade, onde a manipulação direta é superior", "Coding tools como Claude Code e Codex se espalham organicamente entre não-engenheiros para automações cotidianas (impostos, organização de arquivos, edição de vídeo), sinal de mudança radical de comportamento", "Produtos SaaS estão se adaptando a agentes lançando versões headless e CLIs dedicados (Salesforce, Notion, Google), abandonando décadas de investimento em UI", "Acima de um limiar de complexidade, a GUI deixa de ser ativo e vira problema (menus, submenus, painéis), tornando agentes a interface preferencial", "Generative UI nível 2 muda o papel de designers e engenheiros: eles passam a desenhar regras e componentes (UI kit) que a IA combina, não telas fixas", "Airbnb testou interfaces de booking baseadas em chat, descartou por não funcionar, e lançou um AI lab dedicado a modelos para generative UI", "Google anunciou que a busca passará a gerar mini-apps com generative UI para visualizar tópicos complexos", "A lentidão atual da geração de UI on-the-spot é transitória, assim como o load de páginas web era aceito no passado", "A estratégia correta por produto é segmentar: UI tradicional onde for melhor, agentes para o trabalho repetitivo, generative UI para breakdowns específicos no meio da complexidade"]
deep_dive: "medium"
deep_dive_reason: "O vídeo oferece um framework estruturado e acionável (3 níveis de generative UI, espectro de complexidade, design de regras em vez de telas) com novidade real para arquitetura de produto, mas é análise popular de UX com segmento promocional e sem densidade técnica em harness, evals, context-engineering ou governança."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-ai-interfaces-of-the-future-design-review--DBhSfROq3wU|AI Interfaces Of The Future | Design Review]]", "[[extracts/youtube/ai-learning/2026-09-11-seeing-the-future-from-ai-companions-to-personal-software---KfrrWRl3FA|Seeing The Future from AI Companions to Personal Software]]", "[[extracts/youtube/ai-learning/2026-09-11-beyond-components-designing-generative-ui-for-mcp-apps-ruben-casas-postman--hCMrEfPG2Yg|Beyond Components: Designing Generative UI for MCP Apps — Ruben Casas, Postman]]", "[[extracts/youtube/ai-learning/2026-09-11-the-end-of-the-static-screen-architecting-intent-driven-ux-gus-iwanaga-commercet--QrMcNe2jjt8|The End of the Static Screen: Architecting Intent-Driven UX — Gus Iwanaga, commercetools]]", "[[extracts/youtube/ai-learning/2026-09-11-agentic-ai-how-bots-came-for-our-workflows-and-drudgery-ft-working-it--e85AxYW0Qyk|Agentic AI - how bots came for our workflows and drudgery | FT Working It]]", "[[extracts/youtube/ai-learning/2026-09-11-ex-uber-dev-explains-his-multi-agent-workflow--utb7zYbK10c|Ex-Uber dev explains his Multi-Agent Workflow]]"]
---

# The Weird Future Of User Interfaces

## Tese
O futuro da interação não é chatbots substituindo UI, mas a coexistência de três camadas: UI tradicional com manipulação direta para tarefas simples, agentes para tarefas complexas, e generative UI — interfaces geradas pela IA sob demanda — para o meio da curva de complexidade onde está a maioria do uso real.

## Conceitos-chave
- Manipulação direta como superpoder da GUI (afordância visível de todas as ações)
- Distribuição normal da complexidade das tarefas (o meio é onde está o valor)
- Generative UI nível 1: visualizações geradas on-the-spot
- Generative UI nível 2: UI base fixa com peças generativas
- Generative UI nível 3: o produto inteiro é generativo, as regras são o produto
- Mudança do design de telas para o design de regras e UI kits (blocos de Lego)
- Produtos headless e CLIs voltados a agentes, não humanos
- Adoção orgânica de coding agents por não-engenheiros
- Manipulação indireta via agentes vs manipulação direta via GUI

## Ferramentas & pessoas
**Ferramentas:** Starbucks app, Starbucks plugin para ChatGPT, Humane Pin, Rabbit, Siri, Alexa, Google Home, Meta AI (botão no WhatsApp), Microsoft Copilot key, Claude Code, Codex, VS Code, Remotion, Blender, After Effects, Linear, PostHog, Salesforce (versão headless), Notion CLI, Google CLI, Google Flights (AI mode), Lovable, Flask

**Pessoas/orgs:** Microsoft, Humane, Meta, Google, Salesforce, Notion, Linear, PostHog, Anthropic (Claude), Airbnb, Brian Chesky, Xerox PARC, Figma

## Claims acionáveis
- Chatbots e dispositivos de voz falharam ao tentar substituir GUI para tarefas simples, habituais e de baixa complexidade, onde a manipulação direta é superior
- Coding tools como Claude Code e Codex se espalham organicamente entre não-engenheiros para automações cotidianas (impostos, organização de arquivos, edição de vídeo), sinal de mudança radical de comportamento
- Produtos SaaS estão se adaptando a agentes lançando versões headless e CLIs dedicados (Salesforce, Notion, Google), abandonando décadas de investimento em UI
- Acima de um limiar de complexidade, a GUI deixa de ser ativo e vira problema (menus, submenus, painéis), tornando agentes a interface preferencial
- Generative UI nível 2 muda o papel de designers e engenheiros: eles passam a desenhar regras e componentes (UI kit) que a IA combina, não telas fixas
- Airbnb testou interfaces de booking baseadas em chat, descartou por não funcionar, e lançou um AI lab dedicado a modelos para generative UI
- Google anunciou que a busca passará a gerar mini-apps com generative UI para visualizar tópicos complexos
- A lentidão atual da geração de UI on-the-spot é transitória, assim como o load de páginas web era aceito no passado
- A estratégia correta por produto é segmentar: UI tradicional onde for melhor, agentes para o trabalho repetitivo, generative UI para breakdowns específicos no meio da complexidade

> **Deep dive:** `medium` — O vídeo oferece um framework estruturado e acionável (3 níveis de generative UI, espectro de complexidade, design de regras em vez de telas) com novidade real para arquitetura de produto, mas é análise popular de UX com segmento promocional e sem densidade técnica em harness, evals, context-engineering ou governança.
