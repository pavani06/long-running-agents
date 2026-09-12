---
title: "Everything We Got Wrong About Research-Plan-Implement -  Dexter Horthy"
type: "extract"
source: "youtube"
video_id: "YwZR6tc7qYg"
url: "https://www.youtube.com/watch?v=YwZR6tc7qYg"
channel: "AAIF Live"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-everything-we-got-wrong-about-research-plan-implement-dexter-horthy--YwZR6tc7qYg.txt]]"
tags: ["agentic-coding", "agents", "context-engineering", "context-management", "harness-engineering", "decision-discipline", "verification", "code-review", "12-factor-agents", "spec-driven-development", "process", "token-budgeting", "gate-design"]
thesis: "Dex (HumanLayer) revisa publicamente a metodologia RPI, substituindo-a pelo pipeline CRISPY (perguntas, pesquisa, design, esboço, plano, implementação) que fatia o prompt monolítico de planejamento em estágios menores com janelas de contexto separadas, orçamento de instruções e artefatos curtos de alinhamento humano-agente, defendendo que engenheiros devem continuar lendo o código e nunca terceirizar o pensamento."
concepts: ["Research Plan Implement (RPI) e seus fracassos identificados", "CRISPY (Questions, Research, Design, Structure/Outline, Plan, Implement)", "Orçamento de instruções (LLMs de fronteira seguem consistentemente só ~150-200 instruções)", "Zona burra da janela de contexto (degradação média em torno de ~40%)", "Pesquisa objetiva sem expor o ticket (fatos vs opiniões) via janelas de contexto separadas", "Query planning aplicado a leitura de codebases por LLMs", "'Do not outsource the thinking'", "Design discussion (~200 linhas) como artefato de alinhamento humano-agente", "Structure outline como 'C header file' (assinaturas e tipos, ~2 páginas vs plano de 8)", "Planos verticais com checkpoints testáveis vs planos horizontais por camada", "Usar control flow de código em vez de prompts para control flow", "Classificação de entrada para rotear a prompts pequenos e focados", "Persistir artefatos em markdown estático em vez de depender de compaction", "Alvo de 2-3x de velocidade com qualidade quase humana vs 10x com slop"]
tools: ["Claude Code", "Claude Opus 4.5", "CLAUDE.md", "MCP", "12 Factor Agents (paper)", "Prompts RPI open source (comandos research-codebase e create-plan)", "CRISPY", "TLA+ / TLA++", "GPT-7 (mencionado hipoteticamente)", "IDE da HumanLayer (em construção)"]
people: ["Dex (HumanLayer)", "Eigor", "Jake (Netflix)", "Kyle (cofundador da HumanLayer)", "Jeff", "Matt PCO", "Drew Brun", "Demetrios (organizador)", "Beads (projeto OSS)", "OpenClaw e Pete (mantenedor)", "Sean Grove", "StrongDM (mencionado em pergunta)", "Databricks"]
claims: ["Mantenha cada prompt abaixo de ~40 instruções; LLMs de fronteira seguem consistentemente apenas 150-200 instruções no total, então prompts de 85 instruções mais CLAUDE.md, ferramentas e MCPs estouram o orçamento", "Esconde deterministicamente o ticket do contexto que gera a pesquisa: uma janela formula perguntas e outra janela fresca, sem saber o objetivo, escreve a pesquisa para manter fatos objetivos em vez de opiniões", "Não use prompts para control flow se puder usar control flow real: classifique a entrada e alimente prompts menores e focados com poucas instruções e ações", "Não leia planos longos; revise o design discussion (~200 linhas) e o structure outline (~2 páginas) antes da implementação e faça a revisão profunda no código final", "Leia o código de produção: tentar não ler por seis meses obrigou a rasgar e substituir grandes partes do sistema, e quem mantém código usado por usuários não pode aceitar slop", "Prefira planos verticais (fatias ponta a ponta com checkpoints de teste a cada 200-400 linhas) a planos horizontais por camada (DB, serviços, API, frontend) que geram milhares de linhas sem nada testável", "Mantenha o uso da janela de contexto abaixo de ~40% (a 'zona burra') e considere encerrar a sessão por volta de 60%; resultados degradam quanto mais contexto é usado", "Persista tudo que importa em artefatos markdown estáticos para retomar sessões sem depender da qualidade de autocompactação ou compactação manual", "Excesso de MCPs/ferramentas enche a janela de contexto com instruções irrelevantes e degrada a aderência do modelo às suas instruções", "Mirar 2-3x de velocidade mantendo qualidade quase humana gera melhores resultados de negócio que 10x com slop e retrabalho", "Envie design discussions ao code owner antes de implementar para interceptar decisões ruins num documento de 200 linhas e reduzir retrabalho em code review", "Se a ferramenta exige 'palavras mágicas' ou horas de treino para bons resultados, a ferramenta está errada — conserte-a em vez de culpar o usuário"]
deep_dive: "high"
deep_dive_reason: "Alta densidade de insight arquitetural e acionável diretamente relevante a harness e context engineering — orçamento de instruções, separação determinística de contextos, limiares da zona burra, artefatos de alinhamento e planos verticais — com novidade genuína (revisão pública do RPI para CRISPY) e impacto comprovado em produção."
---

# Everything We Got Wrong About Research-Plan-Implement -  Dexter Horthy

## Tese
Dex (HumanLayer) revisa publicamente a metodologia RPI, substituindo-a pelo pipeline CRISPY (perguntas, pesquisa, design, esboço, plano, implementação) que fatia o prompt monolítico de planejamento em estágios menores com janelas de contexto separadas, orçamento de instruções e artefatos curtos de alinhamento humano-agente, defendendo que engenheiros devem continuar lendo o código e nunca terceirizar o pensamento.

## Conceitos-chave
- Research Plan Implement (RPI) e seus fracassos identificados
- CRISPY (Questions, Research, Design, Structure/Outline, Plan, Implement)
- Orçamento de instruções (LLMs de fronteira seguem consistentemente só ~150-200 instruções)
- Zona burra da janela de contexto (degradação média em torno de ~40%)
- Pesquisa objetiva sem expor o ticket (fatos vs opiniões) via janelas de contexto separadas
- Query planning aplicado a leitura de codebases por LLMs
- 'Do not outsource the thinking'
- Design discussion (~200 linhas) como artefato de alinhamento humano-agente
- Structure outline como 'C header file' (assinaturas e tipos, ~2 páginas vs plano de 8)
- Planos verticais com checkpoints testáveis vs planos horizontais por camada
- Usar control flow de código em vez de prompts para control flow
- Classificação de entrada para rotear a prompts pequenos e focados
- Persistir artefatos em markdown estático em vez de depender de compaction
- Alvo de 2-3x de velocidade com qualidade quase humana vs 10x com slop

## Ferramentas & pessoas
**Ferramentas:** Claude Code, Claude Opus 4.5, CLAUDE.md, MCP, 12 Factor Agents (paper), Prompts RPI open source (comandos research-codebase e create-plan), CRISPY, TLA+ / TLA++, GPT-7 (mencionado hipoteticamente), IDE da HumanLayer (em construção)

**Pessoas/orgs:** Dex (HumanLayer), Eigor, Jake (Netflix), Kyle (cofundador da HumanLayer), Jeff, Matt PCO, Drew Brun, Demetrios (organizador), Beads (projeto OSS), OpenClaw e Pete (mantenedor), Sean Grove, StrongDM (mencionado em pergunta), Databricks

## Claims acionáveis
- Mantenha cada prompt abaixo de ~40 instruções; LLMs de fronteira seguem consistentemente apenas 150-200 instruções no total, então prompts de 85 instruções mais CLAUDE.md, ferramentas e MCPs estouram o orçamento
- Esconde deterministicamente o ticket do contexto que gera a pesquisa: uma janela formula perguntas e outra janela fresca, sem saber o objetivo, escreve a pesquisa para manter fatos objetivos em vez de opiniões
- Não use prompts para control flow se puder usar control flow real: classifique a entrada e alimente prompts menores e focados com poucas instruções e ações
- Não leia planos longos; revise o design discussion (~200 linhas) e o structure outline (~2 páginas) antes da implementação e faça a revisão profunda no código final
- Leia o código de produção: tentar não ler por seis meses obrigou a rasgar e substituir grandes partes do sistema, e quem mantém código usado por usuários não pode aceitar slop
- Prefira planos verticais (fatias ponta a ponta com checkpoints de teste a cada 200-400 linhas) a planos horizontais por camada (DB, serviços, API, frontend) que geram milhares de linhas sem nada testável
- Mantenha o uso da janela de contexto abaixo de ~40% (a 'zona burra') e considere encerrar a sessão por volta de 60%; resultados degradam quanto mais contexto é usado
- Persista tudo que importa em artefatos markdown estáticos para retomar sessões sem depender da qualidade de autocompactação ou compactação manual
- Excesso de MCPs/ferramentas enche a janela de contexto com instruções irrelevantes e degrada a aderência do modelo às suas instruções
- Mirar 2-3x de velocidade mantendo qualidade quase humana gera melhores resultados de negócio que 10x com slop e retrabalho
- Envie design discussions ao code owner antes de implementar para interceptar decisões ruins num documento de 200 linhas e reduzir retrabalho em code review
- Se a ferramenta exige 'palavras mágicas' ou horas de treino para bons resultados, a ferramenta está errada — conserte-a em vez de culpar o usuário

> **Deep dive:** `high` — Alta densidade de insight arquitetural e acionável diretamente relevante a harness e context engineering — orçamento de instruções, separação determinística de contextos, limiares da zona burra, artefatos de alinhamento e planos verticais — com novidade genuína (revisão pública do RPI para CRISPY) e impacto comprovado em produção.
