---
title: "Active Graph Agent Runtime (BabyAGI 4) — Yohei Nakajima, Untapped Capital"
type: "extract"
source: "youtube"
video_id: "khVX_BUnEwU"
url: "https://www.youtube.com/watch?v=khVX_BUnEwU"
channel: "AI Engineer"
extracted: "2026-09-17"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-17-active-graph-agent-runtime-babyagi-4-yohei-nakajima-untapped-capital--khVX_BUnEwU.txt]]"
tags: ["agents", "arquitetura", "runtime", "harness-engineering", "agent-loop", "context-engineering", "context-management", "state", "memory-architecture", "gate-design", "governanca", "permissions", "evals", "verification", "observability", "multi-agent", "frameworks", "agentic-coding", "tracing"]
thesis: "Yohei Nakajima propõe o Active Graph, um runtime de grafo event-sourced onde agentes são construídos em torno de um log de eventos imutável e tipado (em vez do LLM), tornando replays, rollbacks, forks, auditoria e auto-melhoria nativos."
concepts: ["Runtime de grafo event-sourced para agentes auditáveis", "Log imutável e tipado como ground truth (\"o log é o agente\")", "Abordagem log-cêntrica vs LLM-cêntrica", "Flatten de 'o que o agente faz' e 'como o agente muda' em um único log", "Behaviors: reagem a mudanças no grafo e emitem eventos", "Relation behaviors em arestas (ex.: unblock)", "LLMs não conversam diretamente; comunicam-se via estado compartilhado", "Inspiração em Blackboard architecture (anos 70/80) e Kafka (microworkers)", "Policies: controlam como o grafo pode ser modificado (human-in-the-loop, checagem de contradição)", "Proposed patch antes de aprovar mudanças", "Views: context management programático como query de grafo", "Packs: bundles modulares de schemas de objetos, tools, behaviors e pack policy", "Replays, rollbacks e forks nativos", "Log como memória estruturada (não vector RAG puro)", "Self-improvement loops com gates estáticos, sandbox e verificação de resultado", "Fork de si mesmo para propor mudança + avaliar antes de aceitar", "Rastreamento do que não funcionou (não só do que funcionou)", "World model experiencial vs world model preditivo (priors)", "Analogia com hipocampo: log de eventos imutável que projeta estado e realimenta priors via replay/sono", "Hipótese de que o harness não desaparece conforme modelos melhoram", "Identidade do agente derivada do seu próprio log", "Agente debugging via query no event DB em vez de session logs"]
tools: ["Active Graph", "BabyAGI (9 iterações)", "Instagraph", "Claude Code", "Replit", "Kaggle", "LongMemEval", "arXiv (papers 'The Log is the Agent' e 'Regimes')", "babyagi wiki (GitHub)"]
people: ["Yohei Nakajima", "Untapped Capital", "BabyAGI"]
claims: ["Construir em torno do log dá replays, rollbacks e forks nativamente, eliminando a necessidade de reiniciar runs longos do zero (ex.: API key falhou na questão 350 e o run retomou da 353)", "Usar o log estruturado como memória (embeddar query, buscar mensagens relevantes, pegar contexto antes/depois) performou bem no LongMemEval sem ingestão semântica, extração de fatos ou entidades", "LLMs comunicando-se apenas via estado compartilhado permite reconstruir harnesses comuns (ex.: ReAct agent) sobre o runtime", "Self-modification controlada por classificação de falha + permissão de editar partes específicas do agente + gates (patch proposta, checagem estática, sandbox, verificação de impacto) gerou melhora modesta mas estatisticamente significativa no LongMemEval, aceitando ~4-5 patches em loops de 8-13 iterações", "Policies que exigem experimentos antes de aceitar mudanças fazem o agente rastrear e lembrar o que não funcionou, ao contrário de agentes 'yolo'", "No Kaggle Pokemon, ~80 passes com gates (200 jogos simulados, win rate + Wilson score) aceitaram ~20-30 mudanças e melhoraram o score gradualmente", "Hipótese: AI arqueta melhor esse estilo de agente porque Blackboard/Kafka têm décadas de discussão no training data, enquanto agentes LLM têm só ~3 anos", "Packs funcionam modulares entre repositórios sem trabalho extra (descoberto pelo próprio agente lab)", "O ActiveGraph Lab lê blogs/repos, propõe experimentos, achou um bug no próprio código, escreveu o PR e o merge foi aceito", "Debugging mudou de session logs para queries no event DB porque tudo está logado de forma limpa e tipada", "Hipótese de pesquisa: agentes de longa duração precisam de world model experiencial além do preditivo, e o harness não desaparecerá conforme os modelos melhoram", "Recomendação prática: pedir ao seu coding agent que procure 'active graph' e construa algo para testar o runtime"]
deep_dive: "high"
deep_dive_reason: "Apresenta arquitetura nova e densa em mecanismos acionáveis (log imutável tipado, behaviors, policies, views, packs) com validação experimental em harness engineering, governança, evals e self-improvement, diretamente relevante aos critérios de novidade e densidade."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-agent-frameworks-considered-harmful-remi-louf-txt--KHudyx5wW3U|Agent Frameworks Considered Harmful — Rémi Louf, .txt]]", "[[extracts/youtube/ai-learning/2026-09-11-deep-agents-explained--GbzEDgcuGJU|Deep Agents Explained]]", "[[extracts/youtube/ai-learning/2026-09-11-introducing-managed-deep-agents-interrupt-26--LdQpoK2TzSo|Introducing Managed Deep Agents | Interrupt 26]]", "[[extracts/youtube/ai-learning/2026-09-11-the-best-ai-agents-need-less-code-than-you-think--YqjR4vQwbTc|The best AI agents need less code than you think]]", "[[extracts/youtube/ai-learning/2026-09-11-anthropic-s-applied-ai-team-on-the-evolution-of-agentic-surfaces--K0X9QDRkIdg|Anthropic's Applied AI team on the Evolution of Agentic Surfaces]]", "[[extracts/youtube/ai-learning/2026-09-13-github-top-trending-tool-just-fixed-the-ai-agents-biggest-problem--cyIWQHYoUg8|Github Top Trending Tool Just Fixed The AI Agent’s Biggest Problem]]", "[[extracts/youtube/ai-learning/2026-09-11-why-your-agents-need-decision-traces-not-just-documents-zach-blumenfeld-neo4j--B9h9ovW5H9U|Why your agents need decision traces, not just documents — Zach Blumenfeld, Neo4j]]"]
theme: "Deep Agents e Orquestração de Subagentes"
---

# Active Graph Agent Runtime (BabyAGI 4) — Yohei Nakajima, Untapped Capital

## Tese
Yohei Nakajima propõe o Active Graph, um runtime de grafo event-sourced onde agentes são construídos em torno de um log de eventos imutável e tipado (em vez do LLM), tornando replays, rollbacks, forks, auditoria e auto-melhoria nativos.

## Conceitos-chave
- Runtime de grafo event-sourced para agentes auditáveis
- Log imutável e tipado como ground truth ("o log é o agente")
- Abordagem log-cêntrica vs LLM-cêntrica
- Flatten de 'o que o agente faz' e 'como o agente muda' em um único log
- Behaviors: reagem a mudanças no grafo e emitem eventos
- Relation behaviors em arestas (ex.: unblock)
- LLMs não conversam diretamente; comunicam-se via estado compartilhado
- Inspiração em Blackboard architecture (anos 70/80) e Kafka (microworkers)
- Policies: controlam como o grafo pode ser modificado (human-in-the-loop, checagem de contradição)
- Proposed patch antes de aprovar mudanças
- Views: context management programático como query de grafo
- Packs: bundles modulares de schemas de objetos, tools, behaviors e pack policy
- Replays, rollbacks e forks nativos
- Log como memória estruturada (não vector RAG puro)
- Self-improvement loops com gates estáticos, sandbox e verificação de resultado
- Fork de si mesmo para propor mudança + avaliar antes de aceitar
- Rastreamento do que não funcionou (não só do que funcionou)
- World model experiencial vs world model preditivo (priors)
- Analogia com hipocampo: log de eventos imutável que projeta estado e realimenta priors via replay/sono
- Hipótese de que o harness não desaparece conforme modelos melhoram
- Identidade do agente derivada do seu próprio log
- Agente debugging via query no event DB em vez de session logs

## Ferramentas & pessoas
**Ferramentas:** Active Graph, BabyAGI (9 iterações), Instagraph, Claude Code, Replit, Kaggle, LongMemEval, arXiv (papers 'The Log is the Agent' e 'Regimes'), babyagi wiki (GitHub)

**Pessoas/orgs:** Yohei Nakajima, Untapped Capital, BabyAGI

## Claims acionáveis
- Construir em torno do log dá replays, rollbacks e forks nativamente, eliminando a necessidade de reiniciar runs longos do zero (ex.: API key falhou na questão 350 e o run retomou da 353)
- Usar o log estruturado como memória (embeddar query, buscar mensagens relevantes, pegar contexto antes/depois) performou bem no LongMemEval sem ingestão semântica, extração de fatos ou entidades
- LLMs comunicando-se apenas via estado compartilhado permite reconstruir harnesses comuns (ex.: ReAct agent) sobre o runtime
- Self-modification controlada por classificação de falha + permissão de editar partes específicas do agente + gates (patch proposta, checagem estática, sandbox, verificação de impacto) gerou melhora modesta mas estatisticamente significativa no LongMemEval, aceitando ~4-5 patches em loops de 8-13 iterações
- Policies que exigem experimentos antes de aceitar mudanças fazem o agente rastrear e lembrar o que não funcionou, ao contrário de agentes 'yolo'
- No Kaggle Pokemon, ~80 passes com gates (200 jogos simulados, win rate + Wilson score) aceitaram ~20-30 mudanças e melhoraram o score gradualmente
- Hipótese: AI arqueta melhor esse estilo de agente porque Blackboard/Kafka têm décadas de discussão no training data, enquanto agentes LLM têm só ~3 anos
- Packs funcionam modulares entre repositórios sem trabalho extra (descoberto pelo próprio agente lab)
- O ActiveGraph Lab lê blogs/repos, propõe experimentos, achou um bug no próprio código, escreveu o PR e o merge foi aceito
- Debugging mudou de session logs para queries no event DB porque tudo está logado de forma limpa e tipada
- Hipótese de pesquisa: agentes de longa duração precisam de world model experiencial além do preditivo, e o harness não desaparecerá conforme os modelos melhoram
- Recomendação prática: pedir ao seu coding agent que procure 'active graph' e construa algo para testar o runtime

> **Deep dive:** `high` — Apresenta arquitetura nova e densa em mecanismos acionáveis (log imutável tipado, behaviors, policies, views, packs) com validação experimental em harness engineering, governança, evals e self-improvement, diretamente relevante aos critérios de novidade e densidade.
