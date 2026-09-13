---
title: "Dinâmica de aprendizado do RLVR"
type: "extract"
source: "x"
status_id: "2080881800877134004"
handle: "tydsh"
url: "https://x.com/tydsh/status/2080881800877134004"
created_at: "2026-07-25T05:04:16.000Z"
extracted: "2026-09-13"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-12-tydsh-a-novel-way-to-do-rl-in-llm-post-training-inspired-by-our-pr--2080881800877134004.json]]"
tags: ["analise", "performance", "verification"]
topic: "Dinâmica de aprendizado do RLVR"
summary: "Paper oferece a primeira caracterização em nível de parâmetro do RLVR: o aprendizado ocorre fora das direções principais do espaço de pesos (drift espectral mínimo, rotação reduzida do subespaço principal), com a aparente esparsidade explicada por uma 'Three-Gate Theory' (âncora KL, geometria do modelo, precisão). Como RL opera em regime de otimização distinto do SFT, reaproveitar PEFT da era SFT (LoRA, sparse fine-tuning) para RL pode ser falho — e otimizar apenas a rotação (vetores singulares) já basta para boa performance."
key_points: ["A esparsidade de updates no RLVR é artefato de superfície: para um modelo pré-treinado fixo, updates se localizam em regiões preferidas de parâmetros, altamente consistentes entre runs e invariantes a datasets e receitas de RL.", "Three-Gate Theory: Gate I (KL Anchor) impõe update restrito por KL; Gate II (Model Geometry) desvia o passo das direções principais para subespaços de baixa curvatura que preservam o espectro; Gate III (Precision) esconde micro-updates fora das regiões preferidas, criando a ilusão de esparsidade.", "RLVR vs SFT: RLVR aprende off-principal com drift espectral mínimo, enquanto SFT mira pesos principais e distorce o espectro — regimes de otimização fundamentalmente distintos.", "Adaptar diretamente métodos PEFT da era SFT (LoRA, sparse fine-tuning avançado) a RL é metodologicamente falho, como mostram os estudos de caso; o caminho proposto são algoritmos RLVR-nativos conscientes da geometria.", "Resultado prático destacado no tweet: otimizar somente os vetores singulares (rotação) das matrizes de peso é suficiente para boa performance em RL pós-treinamento."]
entities: ["RLVR", "SFT", "LoRA", "PEFT", "arXiv", "tydsh"]
content_type: "data"
revisit: "high"
grounded_in: "article"
links: ["https://arxiv.org/abs/2511.08567"]
media: []
relates-to: ["[[extracts/x/bookmarks/2026-09-12-cwolferesearch-getting-ready-to-publish-my-complete-guide-to-rl-for-llms-to--2091570446164733962|RLHF e pós-treinamento de LLMs]]", "[[extracts/x/bookmarks/2026-09-12-cwolferesearch-i-just-published-my-complete-guide-to-reinforcement-learning--2091872097723359673|Guia completo de RL para LLMs]]", "[[extracts/x/bookmarks/2026-09-12-cwolferesearch-this-post-was-initially-a-short-writeup-on-a-few-papers-that--2078915960094761007|World modeling em agentic RL]]", "[[extracts/x/bookmarks/2026-09-12-openhonor-puro-2b-is-open-beyond-the-weights-technical-report-final-in--2093994412770566256|Puro-2B: receita aberta de pré-treinamento barato]]", "[[extracts/x/bookmarks/2026-09-12-0xmortyx-andrej-karpathy-just-broke-the-entire-premise-of-modern-ai-a--2078468804276019504|Agentes como destilação em escala]]", "[[extracts/x/bookmarks/2026-09-12-dair_ai-brilliant-new-paper-from-the-qwen-team-it-provides-insights--2095880318146507139|Ambientes de treino de agentes]]", "[[extracts/x/bookmarks/2026-09-12-_avichawla-why-kv-cache-stores-k-and-v-vectors-but-never-q-a-popular-te--2093962020962083139|KV cache sem Q em LLMs]]", "[[extracts/x/bookmarks/2026-09-12-fazle_karim1-googleresearch-i-wonder-how-it-would-do-on-this-research-of--2094501145536315670|GlucoFM: foundation model para CGM]]", "[[extracts/x/bookmarks/2026-09-12-thenarrator-a-prediction-markets-true-quality-metric-is-repricing-latenc--2082684092768751792|Métrica de qualidade em prediction markets]]", "[[extracts/x/bookmarks/2026-09-12-bradschoenfeld-why-do-some-people-gain-more-muscle-than-others-last-year-i--2096961137031975189|variabilidade individual na hipertrofia]]"]
thin: false
theme: "Tooling agêntico de engenharia"
---

# Dinâmica de aprendizado do RLVR

**@tydsh** · [2080881800877134004](https://x.com/tydsh/status/2080881800877134004) · `data`

## Resumo
Paper oferece a primeira caracterização em nível de parâmetro do RLVR: o aprendizado ocorre fora das direções principais do espaço de pesos (drift espectral mínimo, rotação reduzida do subespaço principal), com a aparente esparsidade explicada por uma 'Three-Gate Theory' (âncora KL, geometria do modelo, precisão). Como RL opera em regime de otimização distinto do SFT, reaproveitar PEFT da era SFT (LoRA, sparse fine-tuning) para RL pode ser falho — e otimizar apenas a rotação (vetores singulares) já basta para boa performance.

## Pontos-chave
- A esparsidade de updates no RLVR é artefato de superfície: para um modelo pré-treinado fixo, updates se localizam em regiões preferidas de parâmetros, altamente consistentes entre runs e invariantes a datasets e receitas de RL.
- Three-Gate Theory: Gate I (KL Anchor) impõe update restrito por KL; Gate II (Model Geometry) desvia o passo das direções principais para subespaços de baixa curvatura que preservam o espectro; Gate III (Precision) esconde micro-updates fora das regiões preferidas, criando a ilusão de esparsidade.
- RLVR vs SFT: RLVR aprende off-principal com drift espectral mínimo, enquanto SFT mira pesos principais e distorce o espectro — regimes de otimização fundamentalmente distintos.
- Adaptar diretamente métodos PEFT da era SFT (LoRA, sparse fine-tuning avançado) a RL é metodologicamente falho, como mostram os estudos de caso; o caminho proposto são algoritmos RLVR-nativos conscientes da geometria.
- Resultado prático destacado no tweet: otimizar somente os vetores singulares (rotação) das matrizes de peso é suficiente para boa performance em RL pós-treinamento.

## Links
- https://arxiv.org/abs/2511.08567

## Entidades
RLVR, SFT, LoRA, PEFT, arXiv, tydsh

> **Revisit:** `high` · **fonte:** `article`
