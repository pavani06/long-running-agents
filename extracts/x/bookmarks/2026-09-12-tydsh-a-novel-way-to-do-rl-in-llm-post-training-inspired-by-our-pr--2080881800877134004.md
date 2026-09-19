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
thin: false
theme: "Confiabilidade e avaliação de agentes"
relates-to: ["[[extracts/x/bookmarks/2026-09-16-googleresearch-introducing-retrieve-for-train-a-framework-that-accelerates--2099951761985601580|Retrieve-for-Train: difusão para retrieval]]", "[[extracts/x/bookmarks/2026-09-14-yifanzhang_-rasbt-https-t-co-tovrlbceki--2099180888684937556|Recurrent Looped Transformer]]", "[[extracts/x/bookmarks/2026-09-12-cwolferesearch-getting-ready-to-publish-my-complete-guide-to-rl-for-llms-to--2091570446164733962|RLHF e pós-treinamento de LLMs]]", "[[extracts/x/bookmarks/2026-09-14-rasbt-reasoning-from-scratch-round-3-this-time-i-cover-generating--2099231450411290900|Verificadores para avaliação e RLVR]]", "[[extracts/x/bookmarks/2026-09-14-orcarouter-yifanzhang-thats-not-really-new-the-interesting-problem-with--2098913996057502068|Observabilidade em modelos com recurrent depth]]", "[[extracts/x/bookmarks/2026-09-12-cwolferesearch-i-just-published-my-complete-guide-to-reinforcement-learning--2091872097723359673|Guia completo de RL para LLMs]]", "[[extracts/x/bookmarks/2026-09-12-_avichawla-why-kv-cache-stores-k-and-v-vectors-but-never-q-a-popular-te--2093962020962083139|KV cache sem Q em LLMs]]", "[[extracts/x/bookmarks/2026-09-12-bradschoenfeld-why-do-some-people-gain-more-muscle-than-others-last-year-i--2096961137031975189|variabilidade individual na hipertrofia]]"]
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
