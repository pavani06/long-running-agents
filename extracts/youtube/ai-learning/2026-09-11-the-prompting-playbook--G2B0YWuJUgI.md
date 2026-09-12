---
title: "The prompting playbook"
type: "extract"
source: "youtube"
video_id: "G2B0YWuJUgI"
url: "https://www.youtube.com/watch?v=G2B0YWuJUgI"
channel: "Claude"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-the-prompting-playbook--G2B0YWuJUgI.txt]]"
tags: ["evals", "context-engineering", "harness", "agent-loop", "model-selection", "token-budgeting", "escalation", "verification", "agent-tooling", "testes-qa", "production", "error-handling", "process", "runtime"]
thesis: "Depurar prompts com uma eval suite (caso de controle, edge cases e limites de capacidade), corrigindo um modo de falha por vez com higiene estrutural, mudanças no harness e decomposição em loops agentivos (generate-evaluate-repair), é o caminho prático para manter prompts em produção e construir agentes novos com trade-off controlado de tokens e latência."
concepts: ["eval suite com control case, edge cases e limites de capacidade (escalonar/recusar)", "higiene de prompt: XML tags separando role, guidelines, policy, tone e data", "output contract: formato de saída, stop sequences e structured outputs", "overfitting a patches defensivos criados para modelos anteriores", "retenção indevida de informação (withholding) como inverso da alucinação", "'instructions don't add capability' — dar ferramenta em vez de exigir cálculo correto", "instruções com os dois lados do trade-off (custo vs benefício)", "generate-evaluate-repair loop com três prompts especializados", "julgamento programático (função Python) vs LLM judge", "soft constraints injetadas em runtime no prompt de avaliação", "adaptive thinking e orçamento de tokens/latência", "seleção de modelo (Sonnet 4.6 vs Opus 4.7)", "version control de prompts com registro do motivo das mudanças defensivas"]
tools: ["Claude", "Anthropic API", "Opus 4.7", "Sonnet 4.6", "adaptive thinking", "structured outputs", "stop sequences", "XML tags", "calculate_proration (tool de exemplo)", "LLM judge", "função Python de verificação de violações", "version control"]
people: ["Margot Vanlar", "Anthropic", "Meridian Mobile (telco fictícia)"]
claims: ["Construa a eval suite antes de migrar um prompt para um novo modelo, cobrindo um caso de controle inambíguo, edge cases onde o modelo já falhou e limites de capacidade (quando escalar para humano ou recusar).", "Se ao ler o prompt você não distingue guidelines de policy e de data, o modelo também não conseguirá — separe as seções com XML tags e descrição clara do papel.", "Instruções defensivas introduzidas como patch para modelos antigos (ex.: 'nunca dê detalhes do plano errado, aponte para a URL') tornam-se redundantes e fazem o modelo reter informação que possui; reescreva apontando a fonte correta de verdade no contexto.", "Use version control para registrar a razão de cada mudança defensiva no prompt, permitindo reverter efeitos indesejados ao migrar de modelo.", "Instruções não adicionam capacidade: para cálculos, defina um tool (schema + implementação na API) em vez de pedir que o modelo 'sempre calcule corretamente'.", "Apresente os dois lados dos trade-offs nas instruções (ex.: escalonar custa US$8, mas errar gera reembolso e perda de confiança), pois modelos mais inteligentes ponderam melhor trade-offs explícitos.", "Garanta consistência de saída no harness com stop sequences na chamada de API e, para schemas complexos como JSONs aninhados, use structured outputs.", "Para regras duras, prefira um checker programático (função Python que conta violações) ao LLM judge; reserve o juiz LLM para restrições moles definidas em runtime.", "Resultados medidos: Sonnet 4.6 com prompt simples falha todos os casos; Opus 4.7 reduz violações mas ainda falha; Opus 4.7 com adaptive thinking passa tudo triplicando tokens e latência (~100s); o loop generate-evaluate-repair com três prompts simples passa todos os casos com menos tokens e menor latência.", "Prefira decompor um agente novo em múltiplos prompts especializados (gerar/avaliar/reparar) em vez de um prompt monolítico que tenta fazer tudo.", "Restrições moles (ex.: 'Harry não gosta de trabalhar com Sally', 'terceiro turno na quarta') podem ser injetadas no prompt de avaliação em runtime sem alterar o checker programático.", "Bônus de output format: pedir JSON estruturado no prompt evita erros de parsing downstream mesmo antes de configurar structured outputs."]
deep_dive: "high"
deep_dive_reason: "Densidade alta de técnicas acionáveis sobre evals, mudanças no harness (stop sequences, tools) e decomposição agêntica generate-evaluate-repair, com comparações quantitativas de modelos, tokens e latência diretamente relevantes a harness e avaliação de agentes."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-state-of-the-art-prompting-for-ai-agents--DL82mGde6wo|State-Of-The-Art Prompting For AI Agents]]", "[[extracts/youtube/ai-learning/2026-09-11-ai-prompt-engineering-a-deep-dive--T9aRN5JkmL8|AI prompt engineering: A deep dive]]", "[[extracts/youtube/ai-learning/2026-09-11-prompting-101-code-w-claude--ysPbXH0LpIE|Prompting 101 | Code w/ Claude]]", "[[extracts/youtube/ai-learning/2026-09-11-next-level-prompts-10-mins-into-advanced-prompting--69bH4IHZivs|\"Next Level Prompts?\" - 10 mins into advanced prompting]]", "[[extracts/youtube/ai-learning/2026-09-11-master-the-perfect-chatgpt-prompt-formula-in-just-8-minutes--jC4v5AS4RIM|Master the Perfect ChatGPT Prompt Formula (in just 8 minutes)!]]", "[[extracts/youtube/ai-learning/2026-09-11-boris-cherny-we-cut-80-of-claude-codes-prompt--qyPCVqFUyDo|Boris Cherny: We Cut 80% of Claude Code’s Prompt]]", "[[extracts/youtube/ai-learning/2026-09-11-the-best-chatgpt-prompt-i-ve-ever-created-i-spent-2-months-curating-this-prompt--ABCqfaTjNd4|The best ChatGPT Prompt I've ever created - I spent 2 months curating this prompt to write prompts]]", "[[extracts/youtube/ai-learning/2026-09-11-build-hour-gpt-5--ITMouQ_EuXI|Build Hour: GPT-5]]", "[[extracts/youtube/ai-learning/2026-09-11-beyond-the-prompt-goodbye-slop-welcome-determinism-david-khourshid--uMvTAF280so|Beyond the Prompt: \"Goodbye slop; welcome determinism\" David Khourshid]]", "[[extracts/youtube/ai-learning/2026-09-11-how-did-we-make-deepseek-outperform-opus-4-7--f61DCDwvFis|how did we make deepseek outperform opus 4.7?]]"]
theme: "Stack de IA e Prompting"
---

# The prompting playbook

## Tese
Depurar prompts com uma eval suite (caso de controle, edge cases e limites de capacidade), corrigindo um modo de falha por vez com higiene estrutural, mudanças no harness e decomposição em loops agentivos (generate-evaluate-repair), é o caminho prático para manter prompts em produção e construir agentes novos com trade-off controlado de tokens e latência.

## Conceitos-chave
- eval suite com control case, edge cases e limites de capacidade (escalonar/recusar)
- higiene de prompt: XML tags separando role, guidelines, policy, tone e data
- output contract: formato de saída, stop sequences e structured outputs
- overfitting a patches defensivos criados para modelos anteriores
- retenção indevida de informação (withholding) como inverso da alucinação
- 'instructions don't add capability' — dar ferramenta em vez de exigir cálculo correto
- instruções com os dois lados do trade-off (custo vs benefício)
- generate-evaluate-repair loop com três prompts especializados
- julgamento programático (função Python) vs LLM judge
- soft constraints injetadas em runtime no prompt de avaliação
- adaptive thinking e orçamento de tokens/latência
- seleção de modelo (Sonnet 4.6 vs Opus 4.7)
- version control de prompts com registro do motivo das mudanças defensivas

## Ferramentas & pessoas
**Ferramentas:** Claude, Anthropic API, Opus 4.7, Sonnet 4.6, adaptive thinking, structured outputs, stop sequences, XML tags, calculate_proration (tool de exemplo), LLM judge, função Python de verificação de violações, version control

**Pessoas/orgs:** Margot Vanlar, Anthropic, Meridian Mobile (telco fictícia)

## Claims acionáveis
- Construa a eval suite antes de migrar um prompt para um novo modelo, cobrindo um caso de controle inambíguo, edge cases onde o modelo já falhou e limites de capacidade (quando escalar para humano ou recusar).
- Se ao ler o prompt você não distingue guidelines de policy e de data, o modelo também não conseguirá — separe as seções com XML tags e descrição clara do papel.
- Instruções defensivas introduzidas como patch para modelos antigos (ex.: 'nunca dê detalhes do plano errado, aponte para a URL') tornam-se redundantes e fazem o modelo reter informação que possui; reescreva apontando a fonte correta de verdade no contexto.
- Use version control para registrar a razão de cada mudança defensiva no prompt, permitindo reverter efeitos indesejados ao migrar de modelo.
- Instruções não adicionam capacidade: para cálculos, defina um tool (schema + implementação na API) em vez de pedir que o modelo 'sempre calcule corretamente'.
- Apresente os dois lados dos trade-offs nas instruções (ex.: escalonar custa US$8, mas errar gera reembolso e perda de confiança), pois modelos mais inteligentes ponderam melhor trade-offs explícitos.
- Garanta consistência de saída no harness com stop sequences na chamada de API e, para schemas complexos como JSONs aninhados, use structured outputs.
- Para regras duras, prefira um checker programático (função Python que conta violações) ao LLM judge; reserve o juiz LLM para restrições moles definidas em runtime.
- Resultados medidos: Sonnet 4.6 com prompt simples falha todos os casos; Opus 4.7 reduz violações mas ainda falha; Opus 4.7 com adaptive thinking passa tudo triplicando tokens e latência (~100s); o loop generate-evaluate-repair com três prompts simples passa todos os casos com menos tokens e menor latência.
- Prefira decompor um agente novo em múltiplos prompts especializados (gerar/avaliar/reparar) em vez de um prompt monolítico que tenta fazer tudo.
- Restrições moles (ex.: 'Harry não gosta de trabalhar com Sally', 'terceiro turno na quarta') podem ser injetadas no prompt de avaliação em runtime sem alterar o checker programático.
- Bônus de output format: pedir JSON estruturado no prompt evita erros de parsing downstream mesmo antes de configurar structured outputs.

> **Deep dive:** `high` — Densidade alta de técnicas acionáveis sobre evals, mudanças no harness (stop sequences, tools) e decomposição agêntica generate-evaluate-repair, com comparações quantitativas de modelos, tokens e latência diretamente relevantes a harness e avaliação de agentes.
