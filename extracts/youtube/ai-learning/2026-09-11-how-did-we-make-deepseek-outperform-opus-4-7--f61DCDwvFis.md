---
title: "how did we make deepseek outperform opus 4.7?"
type: "extract"
source: "youtube"
video_id: "f61DCDwvFis"
url: "https://www.youtube.com/watch?v=f61DCDwvFis"
channel: "Ahmad Awais"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-how-did-we-make-deepseek-outperform-opus-4-7--f61DCDwvFis.txt]]"
tags: ["harness", "harness-engineering", "error-handling", "agent-tooling", "agentic-coding", "agents", "production", "token-budgeting", "context-engineering", "memory-architecture", "cross-session", "model-selection", "observability"]
thesis: "Falhas de tool-calling em modelos abertos como DeepSeek V4 são essencialmente um problema de harness e não do modelo: um conjunto pequeno, finito e composicional de erros pode ser corrigido deterministicamente por uma camada de 'tool repairs' que devolve o resultado corrigido com uma 'repair note', interrompendo loops de erro, preservando o fluxo da sessão e reduzindo custo."
concepts: ["tool repair harness / tool repairs (reparos determinísticos de tool calls)", "repair note (nota de correção enviada junto ao resultado da ferramenta)", "validação de schema de tool calls com Zod", "conjunto finito e composicional de erros de tool call (null em campo opcional, array-JSON como string, objeto JS vazio como placeholder, nomes de argumentos errados)", "repairs como migrations de banco de dados, indexados por modelo/linguagem/cenário (~56 mil invariantes)", "taste file (taste.md) como camada de aprendizado contínuo de preferências", "scale divergence loop: o taste file encolhe conforme os modelos aprendem o que antes precisava ser ensinado", "extração do 'taste' de um LLM queimando ~1B tokens em ~11 linguagens para catalogar excentricidades sistemáticas", "degradação da qualidade do modelo após repetidas rejeições de validação (até ~56 falhas consecutivas no mesmo call) e em sessões longas", "correlação entre capacidade de inferência sob pressão e aumento da taxa de erros de tool call", "indicador de reparos na UI (reparado 1x, 2x, 3x) para transparência", "aprendizado de preferências humanas a partir de prompts, edições e feedback explícito"]
tools: ["Command Code (cmd/cmdcode)", "DeepSeek V4 Pro", "DeepSeek V4 Flash", "Kimi K2.6 (\"Kimmy\")", "GLM", "Qwen", "MiniMax", "Claude Opus 4.7", "Claude Haiku", "Zod", "Supabase", "Postgres", "OpenCode", "Hermes agent", "Vercel", "GitHub", "Twitter/X"]
people: ["DeepSeek", "Anthropic (Claude)", "Vercel", "Paul (criador do design scale)", "comunidade Twitter/X de engenharia de agentes"]
claims: ["Trate falhas de tool call de modelos abertos como problema de harness, não de modelo: implemente reparos determinísticos em vez de apenas devolver o erro do validador (Zod) ao LLM.", "Os erros de tool call formam um conjunto pequeno, finito e composicional: null em campo opcional, array passado como string JSON, objeto JavaScript vazio como placeholder e nomes de argumentos incorretos (ex.: 'path' em vez de 'file_path', 'old_string' em vez do valor esperado).", "Cada reparo são ~30–100 linhas de código determinístico, versionadas como migrations e selecionáveis por modelo, linguagem e cenário, com ~56 mil invariantes/variações catalogadas.", "Devolver o resultado reparado acompanhado de uma 'repair note' explicando a correção faz o modelo parar de repetir o erro na chamada seguinte; sem a nota, o modelo reenvia o mesmo payload inválido (observado em média 56 vezes).", "Rejeitar tool calls repetidamente degrada a qualidade cognitiva e o output do modelo na sessão; reparar preserva o fluxo e viabiliza sessões de até 12 horas.", "Quando o argumento é ambíguo (ex.: offset de leitura de arquivo), repare com um default razoável e inclua a nota — o modelo se autocorrige no turno seguinte (ex.: queria as últimas linhas de um log).", "Com os reparos ativos, DeepSeek V4 Flash teria desempenho superior ao Claude Haiku a um custo 10–20x menor.", "A taxa de erros de tool call aumenta quando a capacidade de inferência do provedor está sob pressão; a camada de reparos mitiga isso em escala de >1 trilhão de tokens/mês.", "É possível extrair um 'taste file' de um LLM queimando ~1 bilhão de tokens em ~11 linguagens e múltiplos projetos, catalogando falhas sistemáticas (ex.: goroutines em Go, interfaces TypeScript falhando apenas em escala).", "Taste files devem encolher com o tempo: remova automaticamente o que os modelos mais novos já sabem (scale divergence loop).", "Use benchmarks internos e dados agregados de produção (ex.: 10B tokens de erros correlacionados) para descobrir padrões finitos de falha e priorizar reparos."]
deep_dive: "high"
deep_dive_reason: "Densidade alta e acionável de engenharia de harness: taxonomia concreta dos erros de tool call, padrão de migrations determinísticas, mecanismo de repair note com efeito comprovado no comportamento do modelo e dados de produção em escala trilionária — diretamente relevante a harness, error-handling e context-engineering, apesar do viés promocional do produto."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-the-prompting-playbook--G2B0YWuJUgI|The prompting playbook]]", "[[extracts/youtube/ai-learning/2026-09-11-anthropic-workshop-build-agents-that-run-for-hours-ash-prabaker-andrew-wilson--mR-WAvEPRwE|Anthropic Workshop: Build Agents That Run for Hours — Ash Prabaker & Andrew Wilson]]", "[[extracts/youtube/ai-learning/2026-09-11-how-lovable-self-improves-every-hour-benjamin-verbeek-lovable--KA5kPbdkK2E|How Lovable self-improves every hour — Benjamin Verbeek, Lovable]]", "[[extracts/youtube/ai-learning/2026-09-11-build-hour-gpt-5--ITMouQ_EuXI|Build Hour: GPT-5]]", "[[extracts/youtube/ai-learning/2026-09-11-how-the-claude-code-team-uses-claude-code--S-sYlFiGFv8|How the Claude Code team uses Claude Code]]", "[[extracts/youtube/ai-learning/2026-09-11-why-the-harness-matters-more-than-the-model-yc-paper-club--n9xKblqyQ28|Why The Harness Matters More Than The Model | YC Paper Club]]"]
theme: "Processo de Engenharia Agêntica"
---

# how did we make deepseek outperform opus 4.7?

## Tese
Falhas de tool-calling em modelos abertos como DeepSeek V4 são essencialmente um problema de harness e não do modelo: um conjunto pequeno, finito e composicional de erros pode ser corrigido deterministicamente por uma camada de 'tool repairs' que devolve o resultado corrigido com uma 'repair note', interrompendo loops de erro, preservando o fluxo da sessão e reduzindo custo.

## Conceitos-chave
- tool repair harness / tool repairs (reparos determinísticos de tool calls)
- repair note (nota de correção enviada junto ao resultado da ferramenta)
- validação de schema de tool calls com Zod
- conjunto finito e composicional de erros de tool call (null em campo opcional, array-JSON como string, objeto JS vazio como placeholder, nomes de argumentos errados)
- repairs como migrations de banco de dados, indexados por modelo/linguagem/cenário (~56 mil invariantes)
- taste file (taste.md) como camada de aprendizado contínuo de preferências
- scale divergence loop: o taste file encolhe conforme os modelos aprendem o que antes precisava ser ensinado
- extração do 'taste' de um LLM queimando ~1B tokens em ~11 linguagens para catalogar excentricidades sistemáticas
- degradação da qualidade do modelo após repetidas rejeições de validação (até ~56 falhas consecutivas no mesmo call) e em sessões longas
- correlação entre capacidade de inferência sob pressão e aumento da taxa de erros de tool call
- indicador de reparos na UI (reparado 1x, 2x, 3x) para transparência
- aprendizado de preferências humanas a partir de prompts, edições e feedback explícito

## Ferramentas & pessoas
**Ferramentas:** Command Code (cmd/cmdcode), DeepSeek V4 Pro, DeepSeek V4 Flash, Kimi K2.6 ("Kimmy"), GLM, Qwen, MiniMax, Claude Opus 4.7, Claude Haiku, Zod, Supabase, Postgres, OpenCode, Hermes agent, Vercel, GitHub, Twitter/X

**Pessoas/orgs:** DeepSeek, Anthropic (Claude), Vercel, Paul (criador do design scale), comunidade Twitter/X de engenharia de agentes

## Claims acionáveis
- Trate falhas de tool call de modelos abertos como problema de harness, não de modelo: implemente reparos determinísticos em vez de apenas devolver o erro do validador (Zod) ao LLM.
- Os erros de tool call formam um conjunto pequeno, finito e composicional: null em campo opcional, array passado como string JSON, objeto JavaScript vazio como placeholder e nomes de argumentos incorretos (ex.: 'path' em vez de 'file_path', 'old_string' em vez do valor esperado).
- Cada reparo são ~30–100 linhas de código determinístico, versionadas como migrations e selecionáveis por modelo, linguagem e cenário, com ~56 mil invariantes/variações catalogadas.
- Devolver o resultado reparado acompanhado de uma 'repair note' explicando a correção faz o modelo parar de repetir o erro na chamada seguinte; sem a nota, o modelo reenvia o mesmo payload inválido (observado em média 56 vezes).
- Rejeitar tool calls repetidamente degrada a qualidade cognitiva e o output do modelo na sessão; reparar preserva o fluxo e viabiliza sessões de até 12 horas.
- Quando o argumento é ambíguo (ex.: offset de leitura de arquivo), repare com um default razoável e inclua a nota — o modelo se autocorrige no turno seguinte (ex.: queria as últimas linhas de um log).
- Com os reparos ativos, DeepSeek V4 Flash teria desempenho superior ao Claude Haiku a um custo 10–20x menor.
- A taxa de erros de tool call aumenta quando a capacidade de inferência do provedor está sob pressão; a camada de reparos mitiga isso em escala de >1 trilhão de tokens/mês.
- É possível extrair um 'taste file' de um LLM queimando ~1 bilhão de tokens em ~11 linguagens e múltiplos projetos, catalogando falhas sistemáticas (ex.: goroutines em Go, interfaces TypeScript falhando apenas em escala).
- Taste files devem encolher com o tempo: remova automaticamente o que os modelos mais novos já sabem (scale divergence loop).
- Use benchmarks internos e dados agregados de produção (ex.: 10B tokens de erros correlacionados) para descobrir padrões finitos de falha e priorizar reparos.

> **Deep dive:** `high` — Densidade alta e acionável de engenharia de harness: taxonomia concreta dos erros de tool call, padrão de migrations determinísticas, mecanismo de repair note com efeito comprovado no comportamento do modelo e dados de produção em escala trilionária — diretamente relevante a harness, error-handling e context-engineering, apesar do viés promocional do produto.
