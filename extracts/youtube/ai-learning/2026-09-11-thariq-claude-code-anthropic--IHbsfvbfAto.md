---
title: "Thariq (Claude Code) @ Anthropic"
type: "extract"
source: "youtube"
video_id: "IHbsfvbfAto"
url: "https://www.youtube.com/watch?v=IHbsfvbfAto"
channel: "Greg Kamradt"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-thariq-claude-code-anthropic--IHbsfvbfAto.txt]]"
tags: ["agents", "agentic-coding", "agent-loop", "agent-tooling", "harness", "harness-engineering", "context-engineering", "context-management", "multi-agent", "process", "spec-driven-development", "decision-discipline", "knowledge-management", "stack-tooling"]
thesis: "Existe um 'capability overhang' entre o que os modelos podem fazer e o que realmente utilizamos, e fechá-lo exige dominar a interação humano-agente — fornecer contexto explícito, ferramentas de execução e formatos adequados ao harness, e reduzir ativamente os unknown unknowns do próprio engenheiro."
concepts: ["capability overhang (capacidade não aproveitada)", "unhobbling Claude (destravar o modelo)", "human-agent interaction como nova disciplina", "modelos são cultivados, não desenhados (grown, not designed)", "crescimento de capacidades em 'spiky' (não linear)", "matriz de unknown unknowns (known knowns / unknown knowns / unknown unknowns)", "relação modelo-harness-mundo-usuário", "prompting como skill de alta alavancagem duradoura", "troca de formato (markdown → HTML) como desbloqueio de capacidade", "education porn (consumo passivo de relatórios do modelo)", "grounding de unknown unknowns via visualizações iterativas", "color grading como shader (pixel entra, pixel sai)", "loop spec → entrevista → protótipo com resets", "knowledge work como pasta de código/scripts/dados controlada por um agente", "'não negocie contra si mesmo' / pedir à realidade que revele trade-offs", "entrevistas encadeadas via ask_user_question"]
tools: ["Claude Code", "Claude (modelos)", "Claude Tag (produto multiplayer citado no Q&A)", "ask_user_question (tool do Claude Code)", "plan mode", "Goodfire", "Cursor", "ChatGPT", "ffmpeg", "Remotion", "React", "Figma", "grep", "bash", "git", "Slack"]
people: ["Stark (palestrante, equipe Claude Code)", "Anthropic", "Goodfire", "Eric (Goodfire)", "Y Combinator", "Daisy (equipe Claude Code)", "Matt (criador da skill de entrevista)", "Robbie (audiência)"]
claims: ["Dê ao modelo ferramentas de execução de código em vez de esperar recall puro dos pesos: perguntas que falham no chat (ex.: quais Pokémon terminam em 'aw') são resolvidas em uma linha de grep dentro do Claude Code, e dá para ir além gerando um web app de busca regex.", "Torne o prompt explícito sobre quem você é (nível técnico/familiaridade), o custo do problema (tamanho do codebase, orçamento de compute) e a tática desejada (ex.: 'use subagentes'), pois o modelo não consegue inferir o 'para quê' da pergunta.", "Trate o sistema como modelo + harness + mundo + usuário: o harness pode compensar com memória e contexto adicional (git, Slack), mas cabe ao usuário fornecer propósito e profundidade.", "Modelos melhoram de forma 'spiky' e imprevisível — tool calling, bash e grep venceram a aposta intuitiva em context windows gigantes — então reavalie continuamente suas suposições sobre de onde virá a próxima capacidade.", "Trocar o formato de saída (de markdown para relatórios HTML ricos) desbloqueia capacidades latentes do modelo; não existe ainda ciência para decidir quando trocar ('a pergunta do trilhão de dólares').", "Evolua o uso de ask_user_question em estágios: chamada única → entrevista encadeada com dezenas de perguntas → geração de relatório HTML detalhado do qual o usuário seleciona respostas.", "Para reduzir unknown unknowns, evite 'education porn' (passar os olhos em relatórios do modelo): itere com visualizações interativas, perguntas socráticas e modelos mentais concretos (ex.: color grading ≈ shader; pele e fundo exigem grading diferente por causa da faixa dinâmica do olho humano).", "Descubra o que você quer construir cedo: construa protótipos baratos (mockups HTML, PRs de protótipo) num loop spec → entrevista → protótipo e reinicie incorporando os aprendizados, em vez de descobrir o erro aos 80% da implementação.", "Claude Code edita vídeos ponta a ponta sem editor humano (transcrever clipes, selecionar melhores cortes contra o transcript, cortar 'ums', gerar overlays em React a partir do design system do Figma e compilar) — evidência de que knowledge work está virando uma pasta de código/scripts/dados controlada por um agente.", "Não negocie contra si mesmo: em vez de pré-decidir trade-offs de prioridades, 'faça tudo' e force a realidade a mostrar os trade-offs; ambição insuficiente frequentemente decorre de unknown unknowns não mapeados.", "Palestrante não usa mais plan mode no Claude Code e admite que 'precisamos fazer algo a respeito', sinal de que o formato tradicional de planejamento está sendo substituído pelos loops de entrevista/protótipo."]
deep_dive: "high"
deep_dive_reason: "Apesar do formato conversacional, há densidade alta de insight acionável e novidade vinda de um insider do Claude Code diretamente sobre harness e context-engineering: evolução do ask_user_question, troca markdown→HTML como desbloqueio de capacidade, enquadramento modelo-harness-mundo-usuário e método para grounding de unknown unknowns."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-boris-cherny-we-cut-80-of-claude-codes-prompt--qyPCVqFUyDo|Boris Cherny: We Cut 80% of Claude Code’s Prompt]]", "[[extracts/youtube/ai-learning/2026-09-11-how-the-claude-code-team-uses-claude-code--S-sYlFiGFv8|How the Claude Code team uses Claude Code]]", "[[extracts/youtube/ai-learning/2026-09-11-field-guide-to-fable-thariq-shihipar-anthropic--9fubhllmsBU|Field Guide to Fable — Thariq Shihipar, Anthropic]]", "[[extracts/youtube/ai-learning/2026-09-11-ex-nasa-dev-reveals-his-agentic-engineering-workflow--xgkjtF89-44|Ex-NASA dev reveals his Agentic Engineering Workflow]]", "[[extracts/youtube/ai-learning/2026-09-11-how-we-claude-code--IlqJqcl8ONE|How we Claude Code]]", "[[extracts/youtube/ai-learning/2026-09-11-matt-pococks-agentic-engineering-workflow-just-copy-him--nQwJVHCtDDY|Matt Pocock’s Agentic Engineering Workflow (just copy him)]]", "[[extracts/youtube/ai-learning/2026-09-11-understanding-is-the-new-bottleneck-geoffrey-litt-notion--WkBPX-oDMnA|Understanding is the new bottleneck — Geoffrey Litt, Notion]]", "[[extracts/youtube/ai-learning/2026-09-11-headroom-a-context-optimization-layer-for-llm-applications-tejas-chopra-netflix--UOWSHg18cL0|Headroom: A Context Optimization Layer for LLM Applications - Tejas Chopra, Netflix, Inc.]]"]
theme: "Codificação Agêntica com Claude Code"
---

# Thariq (Claude Code) @ Anthropic

## Tese
Existe um 'capability overhang' entre o que os modelos podem fazer e o que realmente utilizamos, e fechá-lo exige dominar a interação humano-agente — fornecer contexto explícito, ferramentas de execução e formatos adequados ao harness, e reduzir ativamente os unknown unknowns do próprio engenheiro.

## Conceitos-chave
- capability overhang (capacidade não aproveitada)
- unhobbling Claude (destravar o modelo)
- human-agent interaction como nova disciplina
- modelos são cultivados, não desenhados (grown, not designed)
- crescimento de capacidades em 'spiky' (não linear)
- matriz de unknown unknowns (known knowns / unknown knowns / unknown unknowns)
- relação modelo-harness-mundo-usuário
- prompting como skill de alta alavancagem duradoura
- troca de formato (markdown → HTML) como desbloqueio de capacidade
- education porn (consumo passivo de relatórios do modelo)
- grounding de unknown unknowns via visualizações iterativas
- color grading como shader (pixel entra, pixel sai)
- loop spec → entrevista → protótipo com resets
- knowledge work como pasta de código/scripts/dados controlada por um agente
- 'não negocie contra si mesmo' / pedir à realidade que revele trade-offs
- entrevistas encadeadas via ask_user_question

## Ferramentas & pessoas
**Ferramentas:** Claude Code, Claude (modelos), Claude Tag (produto multiplayer citado no Q&A), ask_user_question (tool do Claude Code), plan mode, Goodfire, Cursor, ChatGPT, ffmpeg, Remotion, React, Figma, grep, bash, git, Slack

**Pessoas/orgs:** Stark (palestrante, equipe Claude Code), Anthropic, Goodfire, Eric (Goodfire), Y Combinator, Daisy (equipe Claude Code), Matt (criador da skill de entrevista), Robbie (audiência)

## Claims acionáveis
- Dê ao modelo ferramentas de execução de código em vez de esperar recall puro dos pesos: perguntas que falham no chat (ex.: quais Pokémon terminam em 'aw') são resolvidas em uma linha de grep dentro do Claude Code, e dá para ir além gerando um web app de busca regex.
- Torne o prompt explícito sobre quem você é (nível técnico/familiaridade), o custo do problema (tamanho do codebase, orçamento de compute) e a tática desejada (ex.: 'use subagentes'), pois o modelo não consegue inferir o 'para quê' da pergunta.
- Trate o sistema como modelo + harness + mundo + usuário: o harness pode compensar com memória e contexto adicional (git, Slack), mas cabe ao usuário fornecer propósito e profundidade.
- Modelos melhoram de forma 'spiky' e imprevisível — tool calling, bash e grep venceram a aposta intuitiva em context windows gigantes — então reavalie continuamente suas suposições sobre de onde virá a próxima capacidade.
- Trocar o formato de saída (de markdown para relatórios HTML ricos) desbloqueia capacidades latentes do modelo; não existe ainda ciência para decidir quando trocar ('a pergunta do trilhão de dólares').
- Evolua o uso de ask_user_question em estágios: chamada única → entrevista encadeada com dezenas de perguntas → geração de relatório HTML detalhado do qual o usuário seleciona respostas.
- Para reduzir unknown unknowns, evite 'education porn' (passar os olhos em relatórios do modelo): itere com visualizações interativas, perguntas socráticas e modelos mentais concretos (ex.: color grading ≈ shader; pele e fundo exigem grading diferente por causa da faixa dinâmica do olho humano).
- Descubra o que você quer construir cedo: construa protótipos baratos (mockups HTML, PRs de protótipo) num loop spec → entrevista → protótipo e reinicie incorporando os aprendizados, em vez de descobrir o erro aos 80% da implementação.
- Claude Code edita vídeos ponta a ponta sem editor humano (transcrever clipes, selecionar melhores cortes contra o transcript, cortar 'ums', gerar overlays em React a partir do design system do Figma e compilar) — evidência de que knowledge work está virando uma pasta de código/scripts/dados controlada por um agente.
- Não negocie contra si mesmo: em vez de pré-decidir trade-offs de prioridades, 'faça tudo' e force a realidade a mostrar os trade-offs; ambição insuficiente frequentemente decorre de unknown unknowns não mapeados.
- Palestrante não usa mais plan mode no Claude Code e admite que 'precisamos fazer algo a respeito', sinal de que o formato tradicional de planejamento está sendo substituído pelos loops de entrevista/protótipo.

> **Deep dive:** `high` — Apesar do formato conversacional, há densidade alta de insight acionável e novidade vinda de um insider do Claude Code diretamente sobre harness e context-engineering: evolução do ask_user_question, troca markdown→HTML como desbloqueio de capacidade, enquadramento modelo-harness-mundo-usuário e método para grounding de unknown unknowns.
