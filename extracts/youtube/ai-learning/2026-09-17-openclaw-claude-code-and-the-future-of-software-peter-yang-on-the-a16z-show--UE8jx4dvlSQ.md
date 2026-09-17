---
title: "OpenClaw, Claude Code, and the Future of Software | Peter Yang on The a16z Show"
type: "extract"
source: "youtube"
video_id: "UE8jx4dvlSQ"
url: "https://www.youtube.com/watch?v=UE8jx4dvlSQ"
channel: "a16z"
extracted: "2026-09-17"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-17-openclaw-claude-code-and-the-future-of-software-peter-yang-on-the-a16z-show--UE8jx4dvlSQ.txt]]"
tags: ["agents", "agent-loop", "agentic-coding", "agent-tooling", "agent-context", "memory-architecture", "context-management", "model-selection", "harness", "stack-tooling", "arquitetura", "investimentos", "analise", "macroeconomia"]
thesis: "Agentes de código (OpenClaw, Claude Code, Codex) estão virando o substrato de todo trabalho do conhecimento, encolhendo equipes e apps transacionais enquanto emerge um novo stack de agentes (identidade, pagamentos, CLI vs MCP) que invalida o playbook antigo de software e gestão."
concepts: ["'Coding will eat all knowledge work' (extensão de 'software will eat the world')", "stack de agentes: identidade, pagamentos, marketing, CLI vs MCP", "definição de agente como 'modelo que usa ferramentas em loop'", "arquitetura de memória em camadas (memory.md padrão fraca vs 3 camadas + busca QMD)", "agents.md como instrução de comportamento persistente", "agentes esquecem as próprias skills e precisam de lembretes/capability lists", "canais múltiplos no Telegram com contextos separados (sem memória cross-channel confirmada)", "recompensas de agenda variável (analogia slot machine / feed social) em coding agents", "ferramentas de pensar vs ferramentas de fazer (IDE migrando de execução para exploração)", "workflow 80/20: agente gera os primeiros 80%, humano refina os últimos 20%", "construir naive, pedir retroespectiva ao agente e refazer do ponto inicial", "vibe coding substituindo SaaS por ferramentas internas em startups AI-native", "automação de 100% de uma função vs ganho dramático parcial de produtividade", "enquadramento do compridor: software caro vs mão de obra barata", "monetização consumer: disposição a pagar + receita de consumo (tokens) + custos de inferência forçando cobrança desde o dia 1", "interfaces duplas: API/MCP para agentes + interface de consumo (feed + log de ações)", "ritmo fast-and-slow: hill-climb rápido com agentes, desaceleração para o próximo máximo local", "empresas pequenas (times de produto de 2-3 pessoas + agentes) vs OKR meetings", "negociação agente-a-agente removendo emoção", "agente pessoal em hardware dedicado (Mac Mini) com email próprio e permissões granulares (leitura de email/calendário, escrita em docs selecionados)", "apps orientados a tarefa morrem primeiro; apps de entretenimento sobrevivem mais; Slack sobrevive como interface com agentes"]
tools: ["OpenClaw", "Claude Code", "Codex", "ChatGPT", "Claude (integração Chrome)", "Telegram", "Twilio", "Mercury (MCP de banco)", "Google Docs", "Mac Mini", "QMD search tool (de Toby)", "Figma", "Lovable", "Replit", "Slack", "Calendly", "Excel", "PowerPoint", "Decagon", "Happy Robot", "Sierra", "Pencil.dev"]
people: ["Peter Yang", "Peter Steinberger", "Boris Cherny", "Satya Nadella", "Marc Andreessen (referência implícita)", "Gary (provável Gary Tan)", "a16z / a16z Speedrun", "OpenAI", "Anthropic", "Roblox", "Credit Karma", "Google"]
claims: ["A memória padrão do OpenClaw (memory.md atualizado por dia) é fraca; instalar memória de 3 camadas com busca QMD (~2GB) melhora a recall, e adicionar em agents.md a instrução 'revise toda a memória antes de responder' reduz o esquecimento", "Agentes esquecem que possuem certas skills (ex.: atualizar Google Docs); liste capacidades nos arquivos do agente e reforce verbalmente", "Use Codex para construir algo sério (pensa mais, mais preciso, mas quebra o flow state com pausas longas) e Claude Code para vibing (mais falante, assume mais, mantém fluxo)", "Claude Code vence hoje por features de harness — colar screenshot diretamente, voz, integração com Claude no Chrome — enquanto Codex tem modelo melhor mas harness pior", "Coding agents têm recompensas de agenda variável (qualidade e tempo variáveis), mesma propriedade psicológica de cassino dos feeds sociais — considerar no design", "Apps de conclusão de tarefa (ex.: Calendly) perdem uso para agentes antes de apps de entretenimento; substituição de SaaS por ferramentas internas só compensa com vibe coders dedicados", "Nunca comece do zero: faça o agente gerar os primeiros 80% (texto, slides, docs) e refine manualmente os 20% finais", "Use o agente como ferramenta de pensamento: construa uma versão naive, peça a lista do que ele faria diferente, e refaça do ponto inicial", "Empresas de AI se dividem em dois baldes: lift dramático em parte do job (ex.: phone screen de recrutamento) vs 100% de automação da função (Decagon/Happy Robot/Sierra em suporte) — o segundo é raro; compradores precificam o primeiro como software caro e o segundo como mão de obra barata", "Produtos consumer de AI devem adotar monetização direta (assinatura + consumo por token) viabilizada pela disposição a pagar e pelos custos de inferência", "Produtos futuros precisam de interface dupla: API/MCP para agentes transacionais + interface de consumo com feed e log do que o agente executou", "Cadência de trabalho: use agentes para subir rápido a colina até o máximo local, depois desacelere/random walk para achar o próximo insight; planejamento anual não funciona mais", "Estruture o agente pessoal em hardware dedicado com email próprio, acesso de leitura a email/calendário, escrita apenas em docs selecionados, e canais Telegram separados (público para demos vs privado para trabalho)", "Integração Twilio permite chamadas telefônicas ao vivo com o agente — viável mas com latência ruim", "Menos jobs não é o cenário provável: muda o formato da economia (mais empresas pequenas/solopreneurs), com ambição humana sem teto sustentando demanda de trabalho"]
deep_dive: "medium"
deep_dive_reason: "Conversa casual com nuggets acionáveis (memória em camadas, trade-offs Codex vs Claude Code como modelo vs harness, buckets de automação, interfaces API+consumo), mas sem densidade arquitetural profunda, evals nem novidade técnica significativa."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-head-of-claude-code-on-the-future-of-work-and-productivity--kRgdkOw82F0|Head of Claude Code on the future of work and productivity]]", "[[extracts/youtube/ai-learning/2026-09-11-the-future-of-ai-agents-with-andrew-ng-interrupt-26--OaRhpwz_TGM|The Future of AI Agents with Andrew Ng | Interrupt 26]]", "[[extracts/youtube/ai-learning/2026-09-11-loop-engineering-to-graph-engineering--BOOfy3Yshtw|Loop Engineering to Graph Engineering]]", "[[extracts/youtube/ai-learning/2026-09-11-from-coding-to-knowledge-work-agents-karan-vaidya-composio--xxfMT-bPEmU|From coding to Knowledge work agents — Karan Vaidya, Composio]]", "[[extracts/youtube/ai-learning/2026-09-11-agentic-engineering-explained-by-a-10x-developer--FU5_kpTAVDo|Agentic Engineering, explained by a 10x developer]]", "[[extracts/youtube/ai-learning/2026-09-11-fabio-akita-minha-experiencia-com-agile-vibe-coding--U3bZavG8qQY|Fabio Akita: Minha Experiência com Agile Vibe Coding]]", "[[extracts/youtube/ai-learning/2026-09-15-building-ambitious-software-jonathan-kelley-dioxus-labs-cognition--H7vFrcNWXzs|Building ambitious software — Jonathan Kelley, Dioxus Labs & Cognition]]", "[[extracts/youtube/ai-learning/2026-09-11-why-enterprise-ai-adoption-is-slower-than-you-think-aaron-levie-box-harrison-cha--agSRMrhNTf4|Why Enterprise AI Adoption Is Slower Than You Think — Aaron Levie (Box) + Harrison Chase]]", "[[extracts/youtube/ai-learning/2026-09-11-everything-we-knew-about-software-has-changed-theo-browne-t3dotgg--xUnRQ9vLXxo|Everything we knew about software has changed — Theo Browne, @t3dotgg ​]]"]
theme: "Agentic Coding com Evals"
---

# OpenClaw, Claude Code, and the Future of Software | Peter Yang on The a16z Show

## Tese
Agentes de código (OpenClaw, Claude Code, Codex) estão virando o substrato de todo trabalho do conhecimento, encolhendo equipes e apps transacionais enquanto emerge um novo stack de agentes (identidade, pagamentos, CLI vs MCP) que invalida o playbook antigo de software e gestão.

## Conceitos-chave
- 'Coding will eat all knowledge work' (extensão de 'software will eat the world')
- stack de agentes: identidade, pagamentos, marketing, CLI vs MCP
- definição de agente como 'modelo que usa ferramentas em loop'
- arquitetura de memória em camadas (memory.md padrão fraca vs 3 camadas + busca QMD)
- agents.md como instrução de comportamento persistente
- agentes esquecem as próprias skills e precisam de lembretes/capability lists
- canais múltiplos no Telegram com contextos separados (sem memória cross-channel confirmada)
- recompensas de agenda variável (analogia slot machine / feed social) em coding agents
- ferramentas de pensar vs ferramentas de fazer (IDE migrando de execução para exploração)
- workflow 80/20: agente gera os primeiros 80%, humano refina os últimos 20%
- construir naive, pedir retroespectiva ao agente e refazer do ponto inicial
- vibe coding substituindo SaaS por ferramentas internas em startups AI-native
- automação de 100% de uma função vs ganho dramático parcial de produtividade
- enquadramento do compridor: software caro vs mão de obra barata
- monetização consumer: disposição a pagar + receita de consumo (tokens) + custos de inferência forçando cobrança desde o dia 1
- interfaces duplas: API/MCP para agentes + interface de consumo (feed + log de ações)
- ritmo fast-and-slow: hill-climb rápido com agentes, desaceleração para o próximo máximo local
- empresas pequenas (times de produto de 2-3 pessoas + agentes) vs OKR meetings
- negociação agente-a-agente removendo emoção
- agente pessoal em hardware dedicado (Mac Mini) com email próprio e permissões granulares (leitura de email/calendário, escrita em docs selecionados)
- apps orientados a tarefa morrem primeiro; apps de entretenimento sobrevivem mais; Slack sobrevive como interface com agentes

## Ferramentas & pessoas
**Ferramentas:** OpenClaw, Claude Code, Codex, ChatGPT, Claude (integração Chrome), Telegram, Twilio, Mercury (MCP de banco), Google Docs, Mac Mini, QMD search tool (de Toby), Figma, Lovable, Replit, Slack, Calendly, Excel, PowerPoint, Decagon, Happy Robot, Sierra, Pencil.dev

**Pessoas/orgs:** Peter Yang, Peter Steinberger, Boris Cherny, Satya Nadella, Marc Andreessen (referência implícita), Gary (provável Gary Tan), a16z / a16z Speedrun, OpenAI, Anthropic, Roblox, Credit Karma, Google

## Claims acionáveis
- A memória padrão do OpenClaw (memory.md atualizado por dia) é fraca; instalar memória de 3 camadas com busca QMD (~2GB) melhora a recall, e adicionar em agents.md a instrução 'revise toda a memória antes de responder' reduz o esquecimento
- Agentes esquecem que possuem certas skills (ex.: atualizar Google Docs); liste capacidades nos arquivos do agente e reforce verbalmente
- Use Codex para construir algo sério (pensa mais, mais preciso, mas quebra o flow state com pausas longas) e Claude Code para vibing (mais falante, assume mais, mantém fluxo)
- Claude Code vence hoje por features de harness — colar screenshot diretamente, voz, integração com Claude no Chrome — enquanto Codex tem modelo melhor mas harness pior
- Coding agents têm recompensas de agenda variável (qualidade e tempo variáveis), mesma propriedade psicológica de cassino dos feeds sociais — considerar no design
- Apps de conclusão de tarefa (ex.: Calendly) perdem uso para agentes antes de apps de entretenimento; substituição de SaaS por ferramentas internas só compensa com vibe coders dedicados
- Nunca comece do zero: faça o agente gerar os primeiros 80% (texto, slides, docs) e refine manualmente os 20% finais
- Use o agente como ferramenta de pensamento: construa uma versão naive, peça a lista do que ele faria diferente, e refaça do ponto inicial
- Empresas de AI se dividem em dois baldes: lift dramático em parte do job (ex.: phone screen de recrutamento) vs 100% de automação da função (Decagon/Happy Robot/Sierra em suporte) — o segundo é raro; compradores precificam o primeiro como software caro e o segundo como mão de obra barata
- Produtos consumer de AI devem adotar monetização direta (assinatura + consumo por token) viabilizada pela disposição a pagar e pelos custos de inferência
- Produtos futuros precisam de interface dupla: API/MCP para agentes transacionais + interface de consumo com feed e log do que o agente executou
- Cadência de trabalho: use agentes para subir rápido a colina até o máximo local, depois desacelere/random walk para achar o próximo insight; planejamento anual não funciona mais
- Estruture o agente pessoal em hardware dedicado com email próprio, acesso de leitura a email/calendário, escrita apenas em docs selecionados, e canais Telegram separados (público para demos vs privado para trabalho)
- Integração Twilio permite chamadas telefônicas ao vivo com o agente — viável mas com latência ruim
- Menos jobs não é o cenário provável: muda o formato da economia (mais empresas pequenas/solopreneurs), com ambição humana sem teto sustentando demanda de trabalho

> **Deep dive:** `medium` — Conversa casual com nuggets acionáveis (memória em camadas, trade-offs Codex vs Claude Code como modelo vs harness, buckets de automação, interfaces API+consumo), mas sem densidade arquitetural profunda, evals nem novidade técnica significativa.
