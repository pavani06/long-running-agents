---
title: "GPT 6 Astra + Fable 5.1 = GOD MODE"
type: "extract"
source: "youtube"
video_id: "KgKA0A3qlz0"
url: "https://www.youtube.com/watch?v=KgKA0A3qlz0"
channel: "Chase AI"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-gpt-6-astra-fable-5-1-god-mode--KgKA0A3qlz0.txt]]"
tags: ["model-selection", "verification", "multi-agent", "agent-loop", "agentic-coding", "agent-tooling", "token-budgeting", "evals", "stack-tooling"]
thesis: "Em vez de escolher entre modelos de fronteira, deve-se rotear cada tarefa para o modelo com melhor custo-benefício (usando modelos baratos como Luna e Terra para tarefas simples) e estruturar loops adversariais em que um modelo de um fornecedor constrói e o modelo do outro fornecedor avalia o trabalho com contexto limpo."
concepts: ["Roteamento de modelos por custo-benefício e complexidade da tarefa", "Revisão adversarial cruzada entre fornecedores (construtor vs. avaliador)", "Viés de autoavaliação: modelos avaliam o próprio trabalho de forma favorável", "Eficiência de tokens vs. preço por token (custo total por tarefa)", "Instância headless de CLI para delegação entre ferramentas (Claude Code ↔ Codex)", "Sub-agentes de reconhecimento para pesquisa profunda e validação de premissas", "Loop de feedback com salvaguardas contra iteração infinita e queima de tokens", "Contexto limpo/branco para o avaliador evitar idiossincrasias do fornecedor", "Agnosticismo de ferramentas e divisão de investimento em assinaturas", "Pipeline de planejamento antes de execução com veredito aprovado entre modelos"]
tools: ["GPT6 Astra", "Claude Fable 5.1", "Claude Sonnet 5", "Terra", "Luna", "Claude Haiku", "Claude Code", "Codex", "Claudex Loop (skill/GitHub repo)", "Claudex Route (skill)", "Deep Suite (benchmark)", "WhisperFlow (exemplo de projeto a clonar)", "Chase AI Plus (curso)"]
people: ["OpenAI", "Anthropic", "Chase (criador do Claudex Loop / Chase AI Plus)"]
claims: ["Nunca deixe o modelo que constrói ser o mesmo que avalia o trabalho, pois modelos classificam o próprio trabalho de forma excessivamente favorável", "Combine executar com um fornecedor e revisar com outro: ex. Fable 5.1 cria o plano e Astra o revisa com contexto totalmente limpo, iterando até um veredito aprovado", "Use modelos baratos para tarefas simples: Luna custa ~$0.20/M de entrada e ~$1.20/M de saída, praticamente gratuito frente aos modelos de fronteira ($10/M entrada, $50/M saída)", "No benchmark Deep Suite, Terra atinge 70% no esforço máx. a ~$4/tarefa e Luna 67% a ~$0.60, contra Sonnet 5 com 54% a ~$26/tarefa", "Terra é mais cara por token que Sonnet 5, porém mais barata no total por ser mais eficiente em tokens; Luna iguala ou supera o desempenho do Sonnet 5", "Divida o orçamento de assinaturas (ex.: plano 5x da OpenAI + 5x da Anthropic) para experimentar ambos e manter agnosticismo de ferramentas", "A revisão adversarial no estágio de planejamento economiza tokens no longo prazo em comparação a iterar depois de já ter construído", "Use o skill Claudex Route dentro do Claude Code ou Codex: descreva a tarefa e ele recomenda o modelo adequado, podendo despachar para uma instância headless do Codex a partir do Claude Code (e vice-versa)", "O Claudex Loop percorre quatro estágios: reconhecimento com sub-agentes, perguntas de visão ao usuário, revisão adversarial do plano entre Astra e Fable, e execução seguida de revisão cruzada, com salvaguardas contra loops infinitos", "Instale as skills copiando a URL do GitHub do Claudex Loop e apontando Claude Code ou Codex para ela"]
deep_dive: "medium"
deep_dive_reason: "Oferece insights acionáveis sobre roteamento por custo-benefício e revisão adversarial entre fornecedores com dados de benchmark, mas é tutorial-promocional e sem profundidade arquitetural sobre o funcionamento interno das skills."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-claude-fable-5-use-cases-you-must-do-now-or-lose-thousands-in-1-week--lplVBFr0Ndc|Claude Fable 5 Use Cases You Must Do NOW (Or Lose Thousands in 1 Week)]]", "[[extracts/youtube/ai-learning/2026-09-11-l8-principal-s-agentic-engineering-setup-just-copy-him--8ZgpAXe5V5w|L8 Principal's Agentic Engineering Setup (just copy him)]]", "[[extracts/youtube/ai-learning/2026-09-11-boris-cherny-we-cut-80-of-claude-codes-prompt--qyPCVqFUyDo|Boris Cherny: We Cut 80% of Claude Code’s Prompt]]", "[[extracts/youtube/ai-learning/2026-09-11-openai-just-destroyed-ai-coding-codex-2-0--C06FBVXMLCY|OpenAI just destroyed AI coding… Codex 2.0]]", "[[extracts/youtube/ai-learning/2026-09-11-why-the-harness-matters-more-than-the-model-yc-paper-club--n9xKblqyQ28|Why The Harness Matters More Than The Model | YC Paper Club]]", "[[extracts/youtube/ai-learning/2026-09-11-field-guide-to-fable-thariq-shihipar-anthropic--9fubhllmsBU|Field Guide to Fable — Thariq Shihipar, Anthropic]]", "[[extracts/youtube/ai-learning/2026-09-11-build-hour-gpt-5--ITMouQ_EuXI|Build Hour: GPT-5]]", "[[extracts/youtube/ai-learning/2026-09-11-fine-tune-the-biggest-open-source-models-even-with-a-bad-pc--kxstlfc8Lw4|Fine-Tune the biggest open-source models (even with a bad PC)]]"]
---

# GPT 6 Astra + Fable 5.1 = GOD MODE

## Tese
Em vez de escolher entre modelos de fronteira, deve-se rotear cada tarefa para o modelo com melhor custo-benefício (usando modelos baratos como Luna e Terra para tarefas simples) e estruturar loops adversariais em que um modelo de um fornecedor constrói e o modelo do outro fornecedor avalia o trabalho com contexto limpo.

## Conceitos-chave
- Roteamento de modelos por custo-benefício e complexidade da tarefa
- Revisão adversarial cruzada entre fornecedores (construtor vs. avaliador)
- Viés de autoavaliação: modelos avaliam o próprio trabalho de forma favorável
- Eficiência de tokens vs. preço por token (custo total por tarefa)
- Instância headless de CLI para delegação entre ferramentas (Claude Code ↔ Codex)
- Sub-agentes de reconhecimento para pesquisa profunda e validação de premissas
- Loop de feedback com salvaguardas contra iteração infinita e queima de tokens
- Contexto limpo/branco para o avaliador evitar idiossincrasias do fornecedor
- Agnosticismo de ferramentas e divisão de investimento em assinaturas
- Pipeline de planejamento antes de execução com veredito aprovado entre modelos

## Ferramentas & pessoas
**Ferramentas:** GPT6 Astra, Claude Fable 5.1, Claude Sonnet 5, Terra, Luna, Claude Haiku, Claude Code, Codex, Claudex Loop (skill/GitHub repo), Claudex Route (skill), Deep Suite (benchmark), WhisperFlow (exemplo de projeto a clonar), Chase AI Plus (curso)

**Pessoas/orgs:** OpenAI, Anthropic, Chase (criador do Claudex Loop / Chase AI Plus)

## Claims acionáveis
- Nunca deixe o modelo que constrói ser o mesmo que avalia o trabalho, pois modelos classificam o próprio trabalho de forma excessivamente favorável
- Combine executar com um fornecedor e revisar com outro: ex. Fable 5.1 cria o plano e Astra o revisa com contexto totalmente limpo, iterando até um veredito aprovado
- Use modelos baratos para tarefas simples: Luna custa ~$0.20/M de entrada e ~$1.20/M de saída, praticamente gratuito frente aos modelos de fronteira ($10/M entrada, $50/M saída)
- No benchmark Deep Suite, Terra atinge 70% no esforço máx. a ~$4/tarefa e Luna 67% a ~$0.60, contra Sonnet 5 com 54% a ~$26/tarefa
- Terra é mais cara por token que Sonnet 5, porém mais barata no total por ser mais eficiente em tokens; Luna iguala ou supera o desempenho do Sonnet 5
- Divida o orçamento de assinaturas (ex.: plano 5x da OpenAI + 5x da Anthropic) para experimentar ambos e manter agnosticismo de ferramentas
- A revisão adversarial no estágio de planejamento economiza tokens no longo prazo em comparação a iterar depois de já ter construído
- Use o skill Claudex Route dentro do Claude Code ou Codex: descreva a tarefa e ele recomenda o modelo adequado, podendo despachar para uma instância headless do Codex a partir do Claude Code (e vice-versa)
- O Claudex Loop percorre quatro estágios: reconhecimento com sub-agentes, perguntas de visão ao usuário, revisão adversarial do plano entre Astra e Fable, e execução seguida de revisão cruzada, com salvaguardas contra loops infinitos
- Instale as skills copiando a URL do GitHub do Claudex Loop e apontando Claude Code ou Codex para ela

> **Deep dive:** `medium` — Oferece insights acionáveis sobre roteamento por custo-benefício e revisão adversarial entre fornecedores com dados de benchmark, mas é tutorial-promocional e sem profundidade arquitetural sobre o funcionamento interno das skills.
