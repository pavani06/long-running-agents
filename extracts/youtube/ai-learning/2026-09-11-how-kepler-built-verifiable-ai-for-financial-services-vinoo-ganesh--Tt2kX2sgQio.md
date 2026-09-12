---
title: "How Kepler Built Verifiable AI for Financial Services — Vinoo Ganesh"
type: "extract"
source: "youtube"
video_id: "Tt2kX2sgQio"
url: "https://www.youtube.com/watch?v=Tt2kX2sgQio"
channel: "AI Engineer"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-how-kepler-built-verifiable-ai-for-financial-services-vinoo-ganesh--Tt2kX2sgQio.txt]]"
tags: ["verification", "arquitetura", "error-handling", "governanca", "tracing", "token-budgeting", "model-selection", "evals", "ontologia", "production"]
thesis: "Produção de trabalho verificável por IA em finanças exige separar a inferência probabilística do LLM de um substrato determinístico que extrai, persiste e calcula todos os números — o modelo apenas referencia e decide, nunca escreve nem computa valores."
concepts: ["proveniência atômica (modelo referencia, sistema determinístico escreve números)", "determinismo de escopo (modelo decide o que computar, nunca computa)", "cadeias de derivação re-jogáveis para números derivados", "citação como auditoria post-hoc vs. verificação determinística", "LLMs como máquinas de probabilidade — impossível 'evaluar' até o determinismo", "verificação como processo no caminho, não como outcome", "AI transformou um problema de escrita em problema de leitura", "decaimento de alfa quando todos leem as mesmas fontes", "deslocamento de culpabilidade como motivo de compra (Bloomberg/FactSet)", "analogia pre-SSL do e-commerce para adoção de IA confiável", "trabalho como prova em código (equivalente a unit tests e code review)", "ontologias verificáveis como próximo marco (visão 2027)", "crítica ao token maxing e otimização de custo tipo Snowflake/Databricks", "generalização do padrão para jurídico e descoberta de fármacos"]
tools: ["Kepler", "Claude", "ChatGPT", "Bloomberg", "FactSet", "Capital IQ", "Daloopa", "Seeking Alpha", "Snowflake", "Databricks", "GLM 5.2", "Opus 4.8", "Hugging Face", "Claude for Science", "XBRL (parsing)"]
people: ["Venu Ganesh", "Kepler", "Palantir", "Citadel", "Anthropic", "SEC", "OCC", "TechCrunch", "NIH", "Harvey", "Lorra", "Susanna"]
claims: ["Evals não tornam um LLM não-determinístico verificável; citações são apenas auditoria após o fato, não validação", "O modelo deve escrever apenas uma referência ao número e nunca manipular o valor; bancos de dados persistem os dados com fidelidade adequada", "Todo número que não passa na checagem determinística independente é removido e nunca chega ao usuário", "Verificação não é ground truth universal: deve codificar as regras ('substantivos e verbos') específicas da firma ou mesa", "Com modelagem de margens/ratios, todos cálculos derivados devem ser registrados em cadeias de derivação que podem ser re-executadas e rebobinadas", "O sistema deve saber explicitamente quais data points pode produzir (de filings estruturados) e quais jamais pode produzir (prosa, tabelas cruas)", "Delegar computação a ferramentas determinísticas é mais barato e mais preciso que usar um modelo de bilhões de parâmetros para operações de um ciclo de CPU", "Fine-tuning para extração a 94% de acurácia é insuficiente para trading — o número errado continua errado nos 6%", "O padrão generaliza: extração determinística de entidades evita citações alucinadas em jurídico (Harvey) e compostos perdidos em NIH", "Clientes querem o analista de IA (automatizar transcrições de earnings calls, V0 de modelos financeiros), não o gestor de portfólio de IA", "A corrida será para otimização de custo (o que a indústria viu com Snowflake/Databricks), não para maximizar tokens", "O produto final verificável (DCF, consolidações) deve carregar sua própria prova: cada número atrelado à fonte individual"]
deep_dive: "high"
deep_dive_reason: "Apresenta uma arquitetura concreta e replicável de três pilares (proveniência atômica, determinismo de escopo, cadeias de derivação) para verificação determinística de agentes — diretamente relevante para harness, governança e tolerância a erro — apesar do tom parcialmente promocional."
---

# How Kepler Built Verifiable AI for Financial Services — Vinoo Ganesh

## Tese
Produção de trabalho verificável por IA em finanças exige separar a inferência probabilística do LLM de um substrato determinístico que extrai, persiste e calcula todos os números — o modelo apenas referencia e decide, nunca escreve nem computa valores.

## Conceitos-chave
- proveniência atômica (modelo referencia, sistema determinístico escreve números)
- determinismo de escopo (modelo decide o que computar, nunca computa)
- cadeias de derivação re-jogáveis para números derivados
- citação como auditoria post-hoc vs. verificação determinística
- LLMs como máquinas de probabilidade — impossível 'evaluar' até o determinismo
- verificação como processo no caminho, não como outcome
- AI transformou um problema de escrita em problema de leitura
- decaimento de alfa quando todos leem as mesmas fontes
- deslocamento de culpabilidade como motivo de compra (Bloomberg/FactSet)
- analogia pre-SSL do e-commerce para adoção de IA confiável
- trabalho como prova em código (equivalente a unit tests e code review)
- ontologias verificáveis como próximo marco (visão 2027)
- crítica ao token maxing e otimização de custo tipo Snowflake/Databricks
- generalização do padrão para jurídico e descoberta de fármacos

## Ferramentas & pessoas
**Ferramentas:** Kepler, Claude, ChatGPT, Bloomberg, FactSet, Capital IQ, Daloopa, Seeking Alpha, Snowflake, Databricks, GLM 5.2, Opus 4.8, Hugging Face, Claude for Science, XBRL (parsing)

**Pessoas/orgs:** Venu Ganesh, Kepler, Palantir, Citadel, Anthropic, SEC, OCC, TechCrunch, NIH, Harvey, Lorra, Susanna

## Claims acionáveis
- Evals não tornam um LLM não-determinístico verificável; citações são apenas auditoria após o fato, não validação
- O modelo deve escrever apenas uma referência ao número e nunca manipular o valor; bancos de dados persistem os dados com fidelidade adequada
- Todo número que não passa na checagem determinística independente é removido e nunca chega ao usuário
- Verificação não é ground truth universal: deve codificar as regras ('substantivos e verbos') específicas da firma ou mesa
- Com modelagem de margens/ratios, todos cálculos derivados devem ser registrados em cadeias de derivação que podem ser re-executadas e rebobinadas
- O sistema deve saber explicitamente quais data points pode produzir (de filings estruturados) e quais jamais pode produzir (prosa, tabelas cruas)
- Delegar computação a ferramentas determinísticas é mais barato e mais preciso que usar um modelo de bilhões de parâmetros para operações de um ciclo de CPU
- Fine-tuning para extração a 94% de acurácia é insuficiente para trading — o número errado continua errado nos 6%
- O padrão generaliza: extração determinística de entidades evita citações alucinadas em jurídico (Harvey) e compostos perdidos em NIH
- Clientes querem o analista de IA (automatizar transcrições de earnings calls, V0 de modelos financeiros), não o gestor de portfólio de IA
- A corrida será para otimização de custo (o que a indústria viu com Snowflake/Databricks), não para maximizar tokens
- O produto final verificável (DCF, consolidações) deve carregar sua própria prova: cada número atrelado à fonte individual

> **Deep dive:** `high` — Apresenta uma arquitetura concreta e replicável de três pilares (proveniência atômica, determinismo de escopo, cadeias de derivação) para verificação determinística de agentes — diretamente relevante para harness, governança e tolerância a erro — apesar do tom parcialmente promocional.
