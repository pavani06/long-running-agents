---
title: "The New Code — Sean Grove, OpenAI"
type: "extract"
source: "youtube"
video_id: "8rABwKRsec4"
url: "https://www.youtube.com/watch?v=8rABwKRsec4"
channel: "AI Engineer"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-the-new-code-sean-grove-openai--8rABwKRsec4.txt]]"
tags: ["spec-driven-development", "evals", "governanca", "context-engineering", "verification", "harness", "documentation-publishing", "agents", "process"]
thesis: "A especificação escrita — não o código — é o artefato de maior valor em engenharia de software, e specs em linguagem natural podem se tornar executáveis, testáveis e componíveis como código, alinhando simultaneamente humanos e modelos."
concepts: ["especificação como artefato-fonte vs. código como artefato gerado ('versio­nar o binário e rasgar a fonte')", "código como projeção com perda (lossy projection) da especificação", "comunicação estruturada como gargalo real da engenharia (80–90% do valor)", "vibe coding como comunicação em primeiro lugar", "spec executável: cada cláusula com ID mapeado para prompts desafiadores que servem de critérios de sucesso/evals", "comportamento do modelo desviante da spec = bug (caso sycophancy no update do 4o: rollback, publicação, correção)", "deliberative alignment: spec como material de treino e eval, grader pontuando aderência e reforço dos pesos", "política no contexto (custo de compute de inferência) vs. política nos pesos do modelo ('muscle memory')", "toolchain de specs análogo a compiladores: type checkers para conflitos entre specs de departamentos, linters para ambiguidade, blocking de publicação", "Constituição dos EUA como spec nacional: judicial review como grader, precedente como par input-output/teste unitário", "specs como destino de múltiplas compilações: TypeScript, Rust, servidores, clientes, docs, tutoriais, podcasts", "IDE do futuro como 'clarificador integrado de pensamento' que elimina ambiguidade", "alinhamento de agentes em escala como o domínio que mais carece de especificação"]
tools: ["OpenAI Model Spec (markdown versionado no GitHub)", "Markdown", "Deliberative Alignment (técnica/paper da OpenAI)", "GPT-4o (update com sycophancy)", "TypeScript", "Rust", "V8", "C/compilador, ARM64, x86, WebAssembly (alvos de compilação)", "IDE"]
people: ["Sean (palestrante, OpenAI alignment research)", "OpenAI", "Josh (crédito citado)", "Agente Robustness Team (OpenAI, contratação)"]
claims: ["No próximo feature de IA, comece por uma especificação escrita com intenções, valores e critérios de sucesso explícitos antes de qualquer código", "Dê a cada cláusula da spec um ID e mantenha um arquivo correspondente com prompts desafiadores que funcionam como evals/critérios de sucesso testáveis", "Trate desvio do comportamento do modelo em relação à spec como bug: rollback, publicar análise e corrigir, usando a spec como âncora de confiança", "Aplique deliberative alignment: amostrar o modelo em prompts difíceis, pontuar as respostas contra a spec com um modelo gradeador mais forte e reforçar os pesos — movendo a política do contexto de inferência para os pesos", "Aplique analogia de compilador às specs: 'type checkers' que detectam conflitos entre specs de departamentos e bloqueiam a publicação, e linters que sinalizam linguagem ambígua", "Preserve e versione os prompts/especificações (a fonte) em vez de descartá-los e versionar apenas o código gerado (o binário)", "Compile múltiplos artefatos (código, docs, tutoriais) a partir de uma spec robusta em vez de extrair intenção reversamente do código", "Trate especificação como trabalho central para alinhamento de agentes em escala — 'você nunca disse o que queria, e talvez nunca entendeu plenamente'"]
deep_dive: "high"
deep_dive_reason: "Apresenta mecanismos arquiteturais concretos e replicáveis — cláusulas com IDs mapeadas a evals, pipeline de deliberative alignment que move política do contexto para os pesos, e toolchain de type-checker/linter para specs — com alta densidade de insight acionável diretamente relevante a evals, governança, harness e context-engineering."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-software-fundamentals-matter-more-than-ever-matt-pocock--v4F1gFy-hqg|\"Software Fundamentals Matter More Than Ever\" — Matt Pocock]]", "[[extracts/youtube/ai-learning/2026-09-11-why-the-frontrunners-say-coding-is-solved-but-engineering-is-not--Q7l8YGiMgUw|Why the Frontrunners Say Coding Is Solved BUT Engineering is Not]]", "[[extracts/youtube/ai-learning/2026-09-11-harness-engineering-how-to-build-software-when-humans-steer-agents-execute-ryan--am_oeAoUhew|Harness Engineering: How to Build Software When Humans Steer, Agents Execute — Ryan Lopopolo, OpenAI]]", "[[extracts/youtube/ai-learning/2026-09-11-full-walkthrough-workflow-for-ai-coding-matt-pocock---QFHIoCo-Ko|Full Walkthrough: Workflow for AI Coding — Matt Pocock]]", "[[extracts/youtube/ai-learning/2026-09-11-no-vibes-allowed-solving-hard-problems-in-complex-codebases-dex-horthy-humanlaye--rmvDxxNubIg|No Vibes Allowed: Solving Hard Problems in Complex Codebases – Dex Horthy, HumanLayer]]", "[[extracts/youtube/ai-learning/2026-09-11-fabio-akita-minha-experiencia-com-agile-vibe-coding--U3bZavG8qQY|Fabio Akita: Minha Experiência com Agile Vibe Coding]]"]
theme: "Processo de Engenharia Agêntica"
---

# The New Code — Sean Grove, OpenAI

## Tese
A especificação escrita — não o código — é o artefato de maior valor em engenharia de software, e specs em linguagem natural podem se tornar executáveis, testáveis e componíveis como código, alinhando simultaneamente humanos e modelos.

## Conceitos-chave
- especificação como artefato-fonte vs. código como artefato gerado ('versio­nar o binário e rasgar a fonte')
- código como projeção com perda (lossy projection) da especificação
- comunicação estruturada como gargalo real da engenharia (80–90% do valor)
- vibe coding como comunicação em primeiro lugar
- spec executável: cada cláusula com ID mapeado para prompts desafiadores que servem de critérios de sucesso/evals
- comportamento do modelo desviante da spec = bug (caso sycophancy no update do 4o: rollback, publicação, correção)
- deliberative alignment: spec como material de treino e eval, grader pontuando aderência e reforço dos pesos
- política no contexto (custo de compute de inferência) vs. política nos pesos do modelo ('muscle memory')
- toolchain de specs análogo a compiladores: type checkers para conflitos entre specs de departamentos, linters para ambiguidade, blocking de publicação
- Constituição dos EUA como spec nacional: judicial review como grader, precedente como par input-output/teste unitário
- specs como destino de múltiplas compilações: TypeScript, Rust, servidores, clientes, docs, tutoriais, podcasts
- IDE do futuro como 'clarificador integrado de pensamento' que elimina ambiguidade
- alinhamento de agentes em escala como o domínio que mais carece de especificação

## Ferramentas & pessoas
**Ferramentas:** OpenAI Model Spec (markdown versionado no GitHub), Markdown, Deliberative Alignment (técnica/paper da OpenAI), GPT-4o (update com sycophancy), TypeScript, Rust, V8, C/compilador, ARM64, x86, WebAssembly (alvos de compilação), IDE

**Pessoas/orgs:** Sean (palestrante, OpenAI alignment research), OpenAI, Josh (crédito citado), Agente Robustness Team (OpenAI, contratação)

## Claims acionáveis
- No próximo feature de IA, comece por uma especificação escrita com intenções, valores e critérios de sucesso explícitos antes de qualquer código
- Dê a cada cláusula da spec um ID e mantenha um arquivo correspondente com prompts desafiadores que funcionam como evals/critérios de sucesso testáveis
- Trate desvio do comportamento do modelo em relação à spec como bug: rollback, publicar análise e corrigir, usando a spec como âncora de confiança
- Aplique deliberative alignment: amostrar o modelo em prompts difíceis, pontuar as respostas contra a spec com um modelo gradeador mais forte e reforçar os pesos — movendo a política do contexto de inferência para os pesos
- Aplique analogia de compilador às specs: 'type checkers' que detectam conflitos entre specs de departamentos e bloqueiam a publicação, e linters que sinalizam linguagem ambígua
- Preserve e versione os prompts/especificações (a fonte) em vez de descartá-los e versionar apenas o código gerado (o binário)
- Compile múltiplos artefatos (código, docs, tutoriais) a partir de uma spec robusta em vez de extrair intenção reversamente do código
- Trate especificação como trabalho central para alinhamento de agentes em escala — 'você nunca disse o que queria, e talvez nunca entendeu plenamente'

> **Deep dive:** `high` — Apresenta mecanismos arquiteturais concretos e replicáveis — cláusulas com IDs mapeadas a evals, pipeline de deliberative alignment que move política do contexto para os pesos, e toolchain de type-checker/linter para specs — com alta densidade de insight acionável diretamente relevante a evals, governança, harness e context-engineering.
