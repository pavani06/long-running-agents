---
title: "Getting Started with Omnigent | The Coding Agent Meta-Harness"
type: "extract"
source: "youtube"
video_id: "AyV0hum_hA8"
url: "https://www.youtube.com/watch?v=AyV0hum_hA8"
channel: "Ram Vegiraju"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-getting-started-with-omnigent-the-coding-agent-meta-harness--AyV0hum_hA8.txt]]"
tags: ["agentic-coding", "harness", "harness-engineering", "agent-fleets", "agentes-orquestracao", "multi-agent", "gate-design", "permissions", "governanca", "token-budgeting", "monitoramento", "stack-tooling", "agent-tooling", "production"]
thesis: "O vídeo apresenta o Omni, um 'meta-harness' (supervisor de agentes) lançado no Data and AI Summit pela Databricks, que consolida múltiplos harnesses de coding (Claude Code, OpenAI Agents SDK, etc.) num único workflow em YAML com guardrails de custo, limites de tool calls e aprovação humana, além de compartilhamento de sessões para colaboração em equipe."
concepts: ["Agentic coding em escala (de protótipo a produção)", "Meta-harness / agente supervisor orquestrando sub-harnesses", "Orquestração declarativa via arquivos YAML como fonte da verdade", "Roteamento de saídas de um harness como entrada de outro sem copy-paste manual", "Guardrails e políticas: orçamento, limite de chamadas de ferramentas, human-in-the-loop", "Governança e controle de custo de modelos via gateway", "Compartilhamento de sessões ao vivo por URL para colaboração", "UI unificada com terminal e chat para múltiplos agentes", "Cadeia sequencial de sub-agentes (ex.: coder depois de revisão de código, marketer gerando documentação/descrição)"]
tools: ["Omni (meta-harness)", "Claude Code", "OpenAI Agents SDK", "Codex", "Gemini API", "Databricks Unity AI Gateway (Foundation Models API)", "Claude SDK", "GPT-4o", "Streamlit", "Notion", "YAML"]
people: ["Matei Zaharia (CTO da Databricks, citado como 'Mate')", "Databricks", "OpenAI", "Anthropic (Claude)"]
claims: ["Defina o orquestrador/supervisor e cada sub-agente em arquivos YAML separados, com executor, prompt de sistema e seção de guardrails como fonte da verdade da configuração", "O supervisor decide qual sub-harness usar por caso de uso e alimenta automaticamente a saída de um harness como entrada de outro, eliminando copy-paste manual entre terminais", "Configure políticas de budget com alarmes (ex.: disparar quando custo do sub-agente exceder 5 dólares) e limites máximos de tool calls por sessão (ex.: 12 chamadas)", "Imponha portões de human-in-the-loop exigindo aprovação do usuário antes de ações sensíveis como criação/escrita de arquivos ou ferramentas baseadas em SO", "Aplique guardrails tanto no orquestrador quanto em cada sub-agente, com granularidade configurável, para parar harnesses improdutivos e evitar estouro de custos", "Roteie os modelos de fundação por trás dos harnesses pelo Databricks Unity AI Gateway para obter governança e rastreio de custo", "Compartilhe a URL da sessão ativa com o time para observar em tempo real o que cada agente está gerando", "Instale o Omni e execute 'omni run' via CLI para subir uma UI com acesso simultâneo a terminal e chat, com agentes e configuração do orquestrador delimitados claramente", "Padrão de exemplo: sub-agente coder via Claude Code para geração de código e sub-agente marketer via OpenAI Agents SDK (GPT-4o) para documentação/descrições, encadeados sequencialmente pelo supervisor"]
deep_dive: "medium"
deep_dive_reason: "É uma introdução 101 com detalhes acionáveis reais (estrutura YAML, políticas de budget/tool calls, HITL, gateway de governança), mas sem profundidade arquitetural ou novidade conceitual além do que a ferramenta expõe, com tom parcialmente promocional."
---

# Getting Started with Omnigent | The Coding Agent Meta-Harness

## Tese
O vídeo apresenta o Omni, um 'meta-harness' (supervisor de agentes) lançado no Data and AI Summit pela Databricks, que consolida múltiplos harnesses de coding (Claude Code, OpenAI Agents SDK, etc.) num único workflow em YAML com guardrails de custo, limites de tool calls e aprovação humana, além de compartilhamento de sessões para colaboração em equipe.

## Conceitos-chave
- Agentic coding em escala (de protótipo a produção)
- Meta-harness / agente supervisor orquestrando sub-harnesses
- Orquestração declarativa via arquivos YAML como fonte da verdade
- Roteamento de saídas de um harness como entrada de outro sem copy-paste manual
- Guardrails e políticas: orçamento, limite de chamadas de ferramentas, human-in-the-loop
- Governança e controle de custo de modelos via gateway
- Compartilhamento de sessões ao vivo por URL para colaboração
- UI unificada com terminal e chat para múltiplos agentes
- Cadeia sequencial de sub-agentes (ex.: coder depois de revisão de código, marketer gerando documentação/descrição)

## Ferramentas & pessoas
**Ferramentas:** Omni (meta-harness), Claude Code, OpenAI Agents SDK, Codex, Gemini API, Databricks Unity AI Gateway (Foundation Models API), Claude SDK, GPT-4o, Streamlit, Notion, YAML

**Pessoas/orgs:** Matei Zaharia (CTO da Databricks, citado como 'Mate'), Databricks, OpenAI, Anthropic (Claude)

## Claims acionáveis
- Defina o orquestrador/supervisor e cada sub-agente em arquivos YAML separados, com executor, prompt de sistema e seção de guardrails como fonte da verdade da configuração
- O supervisor decide qual sub-harness usar por caso de uso e alimenta automaticamente a saída de um harness como entrada de outro, eliminando copy-paste manual entre terminais
- Configure políticas de budget com alarmes (ex.: disparar quando custo do sub-agente exceder 5 dólares) e limites máximos de tool calls por sessão (ex.: 12 chamadas)
- Imponha portões de human-in-the-loop exigindo aprovação do usuário antes de ações sensíveis como criação/escrita de arquivos ou ferramentas baseadas em SO
- Aplique guardrails tanto no orquestrador quanto em cada sub-agente, com granularidade configurável, para parar harnesses improdutivos e evitar estouro de custos
- Roteie os modelos de fundação por trás dos harnesses pelo Databricks Unity AI Gateway para obter governança e rastreio de custo
- Compartilhe a URL da sessão ativa com o time para observar em tempo real o que cada agente está gerando
- Instale o Omni e execute 'omni run' via CLI para subir uma UI com acesso simultâneo a terminal e chat, com agentes e configuração do orquestrador delimitados claramente
- Padrão de exemplo: sub-agente coder via Claude Code para geração de código e sub-agente marketer via OpenAI Agents SDK (GPT-4o) para documentação/descrições, encadeados sequencialmente pelo supervisor

> **Deep dive:** `medium` — É uma introdução 101 com detalhes acionáveis reais (estrutura YAML, políticas de budget/tool calls, HITL, gateway de governança), mas sem profundidade arquitetural ou novidade conceitual além do que a ferramenta expõe, com tom parcialmente promocional.
