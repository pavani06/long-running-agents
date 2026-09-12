---
title: "Don't Ship Skills Without Evals — Philipp Schmid, Google DeepMind"
type: "extract"
source: "youtube"
video_id: "0vphxNt4wyk"
url: "https://www.youtube.com/watch?v=0vphxNt4wyk"
channel: "AI Engineer"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-don-t-ship-skills-without-evals-philipp-schmid-google-deepmind--0vphxNt4wyk.txt]]"
tags: ["evals", "harness-engineering", "agent-tooling", "agentic-coding", "context-engineering", "token-budgeting", "testes-qa", "verification", "agents"]
thesis: "Não coloque skills em produção sem evals: agentes são não-determinísticos, e somente uma suíte de avaliação (casos positivos/negativos, ablação com/sem skill, múltiplos trials e regressão a cada mudança) revela se a skill ajuda, prejudica ou já pode ser aposentada."
concepts: ["skills como pasta com SKILL.md e assets adicionais", "progressive disclosure em 3 camadas (descrição, corpo da skill, arquivos de referência)", "capability skills (temporárias, aposentáveis) vs preference skills (duráveis, específicas do domínio)", "model-invoked vs user-invoked skills", "descrição da skill como custo fixo de contexto pago em toda invocação do modelo", "no-ops (instruções que não alteram o comportamento do agente)", "eval harness mínimo: JSON/YAML de casos + script Python rodando o coding agent", "regex asserts baratos vs LLM-as-judge com rubric", "estrutura de caso de teste: prompt, language, should_trigger, expected_checks", "ablation testing (rodar evals com e sem a skill carregada)", "isolated runs em workspaces limpos para evitar que o agente trapaceie buscando contexto externo", "múltiplos trials (3-6) por caso para medir confiabilidade", "teste cross-harness (diferentes harnesses comportam-se diferente)", "regressão contínua: eval roda a cada diff na skill e bloqueia merge sem melhoria", "aposentadoria de skills conforme os modelos melhoram, mantendo o eval para detectar degradação", "diretivas em vez de ensaios; outcomes e não paths", "não confundir agentes que usamos (com contexto do engenheiro) vs agentes que construímos (usuário final não conhece skills)"]
tools: ["SkillBench (benchmark, versão 1.1)", "Gemini API", "Gemini Interactions API", "Gemini CLI", "Gemini 3 / 3.1 / 3.5", "Gemini 2.0", "Claude Code", "Antigravity", "Cursor", "Codex", "GitHub", "repositório de skills de Matt", "TypeScript", "Python", "AWS", "Google Cloud", "Azure"]
people: ["Phillip (palestrante, Google DeepMind)", "Google DeepMind", "Matt (educador de IA, autor da skill de remoção de no-ops)"]
claims: ["SkillBench indexou mais de 50.000 skills do GitHub e quase nenhuma tinha evals; a maioria era escrita por IA e não testada", "SkillBench 1.1 mostra que skills melhoram o desempenho em média ~15% em cerca de 100 tarefas de coding e produtividade", "Skills escritas por humanos superam as geradas por IA; skills geradas por IA podem impactar a performance negativamente", "Arquivos SKILL.md devem ficar abaixo de 500 linhas", "A descrição da skill é custo permanente (~100-200 tokens) pago em cada chamada do modelo; deve ser enxuta e cobrir why/how/when, incluindo casos negativos", "Cerca de 50% das falhas ocorrem porque a skill não foi acionada corretamente devido a descrição fraca ou prompt raso do usuário", "Google DeepMind criou 117 casos de teste para a skill da Gemini Interactions API e elevou a geração de código válido com modelos recentes a quase 90%", "Workflows determinísticos passo-a-passo devem ser scripts, não skills; skills devem definir objetivos e restrições, deixando liberdade ao modelo", "Inicie com 10-20 prompts de eval (5 de caminho feliz, 5 negativos) e inclua traces reais de produção quando disponíveis", "Rode evals em ambientes isolados porque coding agents 'trapaceiam' buscando chats/execuções anteriores para obter o contexto sem usar a skill", "Rode 3-6 trials por caso para medir confiabilidade dado o não-determinismo dos agentes", "Teste a skill em múltiplos harnesses (ex: Claude Code, Cursor, Antigravity, Codex) pois harness e modelo afetam o desempenho", "No DeepMind, toda skill interna tem evals que rodam a cada mudança; o diff só é mergeado se melhorar os testes", "Aposente skills executando evals com e sem a skill; se o modelo atinge a performance sem acioná-la, remova-a para economizar tokens e manutenção", "Mantenha o eval mesmo após aposentar a skill, para detectar degradação e reintroduzi-la se necessário", "Remover no-ops pode não mudar a performance do eval mas economiza custo de tokens"]
deep_dive: "high"
deep_dive_reason: "Densidade alta de orientação arquitetural e acionável sobre evals e harness para skills (estrutura de casos, asserts vs LLM-as-judge, ablação, regressão, aposentadoria), com dados concretos do SkillBench e prática interna do DeepMind, diretamente relevante a harness, evals e context-engineering."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-the-maturity-phases-of-running-evals-phil-hetzel-braintrust--FB-MLPhL9Ms|The maturity phases of running evals — Phil Hetzel, Braintrust]]", "[[extracts/youtube/ai-learning/2026-09-11-building-great-agent-skills-the-missing-manual--UNzCG3lw6O0|Building Great Agent Skills: The Missing Manual]]", "[[extracts/youtube/ai-learning/2026-09-11-so-i-tried-matt-s-skills--0oXOOlqVu5M|So I tried Matt's skills...]]", "[[extracts/youtube/ai-learning/2026-09-11-matt-pococks-agentic-engineering-workflow-just-copy-him--nQwJVHCtDDY|Matt Pocock’s Agentic Engineering Workflow (just copy him)]]", "[[extracts/youtube/ai-learning/2026-09-11-how-i-deleted-95-of-my-agent-skills-and-got-better-results-nick-nisi-workos--vy7o1g2iHY8|How I deleted 95% of my agent skills and got better results — Nick Nisi, WorkOS]]", "[[extracts/youtube/ai-learning/2026-09-11-building-and-evaluating-ai-agents-sayash-kapoor-ai-snake-oil--d5EltXhbcfA|Building and evaluating AI Agents — Sayash Kapoor, AI Snake Oil]]", "[[extracts/youtube/ai-learning/2026-09-11-agentic-evaluations-at-scale-for-everybody-nicholas-kang-michael-aaron-google-de--Ubwb6NzegyA|Agentic Evaluations at Scale, For Everybody — Nicholas Kang & Michael Aaron, Google DeepMind]]"]
theme: "Skills e conhecimento para agentes"
---

# Don't Ship Skills Without Evals — Philipp Schmid, Google DeepMind

## Tese
Não coloque skills em produção sem evals: agentes são não-determinísticos, e somente uma suíte de avaliação (casos positivos/negativos, ablação com/sem skill, múltiplos trials e regressão a cada mudança) revela se a skill ajuda, prejudica ou já pode ser aposentada.

## Conceitos-chave
- skills como pasta com SKILL.md e assets adicionais
- progressive disclosure em 3 camadas (descrição, corpo da skill, arquivos de referência)
- capability skills (temporárias, aposentáveis) vs preference skills (duráveis, específicas do domínio)
- model-invoked vs user-invoked skills
- descrição da skill como custo fixo de contexto pago em toda invocação do modelo
- no-ops (instruções que não alteram o comportamento do agente)
- eval harness mínimo: JSON/YAML de casos + script Python rodando o coding agent
- regex asserts baratos vs LLM-as-judge com rubric
- estrutura de caso de teste: prompt, language, should_trigger, expected_checks
- ablation testing (rodar evals com e sem a skill carregada)
- isolated runs em workspaces limpos para evitar que o agente trapaceie buscando contexto externo
- múltiplos trials (3-6) por caso para medir confiabilidade
- teste cross-harness (diferentes harnesses comportam-se diferente)
- regressão contínua: eval roda a cada diff na skill e bloqueia merge sem melhoria
- aposentadoria de skills conforme os modelos melhoram, mantendo o eval para detectar degradação
- diretivas em vez de ensaios; outcomes e não paths
- não confundir agentes que usamos (com contexto do engenheiro) vs agentes que construímos (usuário final não conhece skills)

## Ferramentas & pessoas
**Ferramentas:** SkillBench (benchmark, versão 1.1), Gemini API, Gemini Interactions API, Gemini CLI, Gemini 3 / 3.1 / 3.5, Gemini 2.0, Claude Code, Antigravity, Cursor, Codex, GitHub, repositório de skills de Matt, TypeScript, Python, AWS, Google Cloud, Azure

**Pessoas/orgs:** Phillip (palestrante, Google DeepMind), Google DeepMind, Matt (educador de IA, autor da skill de remoção de no-ops)

## Claims acionáveis
- SkillBench indexou mais de 50.000 skills do GitHub e quase nenhuma tinha evals; a maioria era escrita por IA e não testada
- SkillBench 1.1 mostra que skills melhoram o desempenho em média ~15% em cerca de 100 tarefas de coding e produtividade
- Skills escritas por humanos superam as geradas por IA; skills geradas por IA podem impactar a performance negativamente
- Arquivos SKILL.md devem ficar abaixo de 500 linhas
- A descrição da skill é custo permanente (~100-200 tokens) pago em cada chamada do modelo; deve ser enxuta e cobrir why/how/when, incluindo casos negativos
- Cerca de 50% das falhas ocorrem porque a skill não foi acionada corretamente devido a descrição fraca ou prompt raso do usuário
- Google DeepMind criou 117 casos de teste para a skill da Gemini Interactions API e elevou a geração de código válido com modelos recentes a quase 90%
- Workflows determinísticos passo-a-passo devem ser scripts, não skills; skills devem definir objetivos e restrições, deixando liberdade ao modelo
- Inicie com 10-20 prompts de eval (5 de caminho feliz, 5 negativos) e inclua traces reais de produção quando disponíveis
- Rode evals em ambientes isolados porque coding agents 'trapaceiam' buscando chats/execuções anteriores para obter o contexto sem usar a skill
- Rode 3-6 trials por caso para medir confiabilidade dado o não-determinismo dos agentes
- Teste a skill em múltiplos harnesses (ex: Claude Code, Cursor, Antigravity, Codex) pois harness e modelo afetam o desempenho
- No DeepMind, toda skill interna tem evals que rodam a cada mudança; o diff só é mergeado se melhorar os testes
- Aposente skills executando evals com e sem a skill; se o modelo atinge a performance sem acioná-la, remova-a para economizar tokens e manutenção
- Mantenha o eval mesmo após aposentar a skill, para detectar degradação e reintroduzi-la se necessário
- Remover no-ops pode não mudar a performance do eval mas economiza custo de tokens

> **Deep dive:** `high` — Densidade alta de orientação arquitetural e acionável sobre evals e harness para skills (estrutura de casos, asserts vs LLM-as-judge, ablação, regressão, aposentadoria), com dados concretos do SkillBench e prática interna do DeepMind, diretamente relevante a harness, evals e context-engineering.
