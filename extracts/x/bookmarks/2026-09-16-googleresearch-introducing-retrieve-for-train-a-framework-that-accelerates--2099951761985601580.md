---
title: "Retrieve-for-Train: difusão para retrieval"
type: "extract"
source: "x"
status_id: "2099951761985601580"
handle: "GoogleResearch"
url: "https://x.com/GoogleResearch/status/2099951761985601580"
created_at: "2026-09-15T20:01:29.000Z"
extracted: "2026-09-16"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-16-googleresearch-introducing-retrieve-for-train-a-framework-that-accelerates--2099951761985601580.json]]"
tags: ["frameworks", "performance", "evals", "arquitetura"]
topic: "Retrieve-for-Train: difusão para retrieval"
summary: "Google Research apresenta Retrieve-for-Train: usa RL offline uma única vez para compilar comportamentos de query fan-out alinhados a recompensa e destilar isso num modelo de difusão de 53.9M parâmetros, substituindo a inferência autorregressiva cara do LLM por geração single-pass de slates de busca em nível especialista. Vale salvar como padrão arquitetural de 'RL como transdutor de objetivo' + destilação para difusão, com speedup de 12-20x e latência sub-segundo."
key_points: ["Zero-shot LLMs para decomposição de query sofrem de paraphrastic collapse (sub-queries quase sinônimas, ex. 'bohemian festival fashion' vs 'clothes') e gargalo de latência autorregressiva — ~50 segundos em batches grandes de contexto — incompatível com barra de busca em produção.", "Pipeline em 3 etapas: (1) fan-out LM (Gemma3-4B/Qwen3-4B) treinado via RL com recompensa de propriedades set-level; (2) o LM congelado sintetiza pares (query → target-set) offline, sem labels humanos; (3) um difusor de 53.9M parâmetros aprende a mapear query embedding direto para o conjunto completo de target embeddings em uma passada não-autorregressiva.", "Recompensa composta de três pilares que agem como contra-âncoras mútuas: groundedness (distância ao manifold do banco), diversity (Vendi Score sobre o conjunto) e alignment ao prompt original — sem o termo de diversidade, o modelo faz reward hacking com strings degeneradas ('line ending line ending') ou parafrases repetitivas; treino com Soft-GRPO (GRPO + PPO soft).", "Resultado: supera single-query search, zero-shot expansion e Best-of-N otimizado em dois regimes (abstract retrieval e composicional fracamente supervisionado), nos domínios moda (CLIP) e playlists musicais (MuLan), com 12-20x de speedup sobre abordagens autorregressivas.", "Insight central transferível: RL como 'transdutor de objetivo' one-time em vez de motor de inferência online — desacoplar o custo de exploração dirigida por recompensa do modelo deployado, viabilizando propriedades set-level não-decomponíveis (diversidade, complementaridade) sem custo de tokens de raciocínio em tempo de teste."]
entities: ["Google Research", "Retrieve-for-Train", "ICML 2026", "Gemma3-4B", "Qwen3-4B", "CLIP", "MuLan", "Vendi Score", "Soft-GRPO", "Pengcheng Jiang", "Judith Yue Li"]
content_type: "announcement"
revisit: "high"
grounded_in: "article"
thin: false
links: ["https://goo.gle/4xuV3lB"]
media: ["https://pbs.twimg.com/media/HSSGbEDasAApYsC.jpg"]
relates-to: ["[[extracts/x/bookmarks/2026-09-12-tydsh-a-novel-way-to-do-rl-in-llm-post-training-inspired-by-our-pr--2080881800877134004|Dinâmica de aprendizado do RLVR]]", "[[extracts/x/bookmarks/2026-09-14-yifanzhang_-rasbt-https-t-co-tovrlbceki--2099180888684937556|Recurrent Looped Transformer]]", "[[extracts/x/bookmarks/2026-09-12-googleresearch-introducing-toolgrad-an-efficient-framework-for-generating-t--2098183830968705163|ToolGrad: geração de datasets de tool-use]]", "[[extracts/x/bookmarks/2026-09-12-openhonor-puro-2b-is-open-beyond-the-weights-technical-report-final-in--2093994412770566256|Puro-2B: receita aberta de pré-treinamento barato]]", "[[extracts/x/bookmarks/2026-09-18-completeskeptic-extraordinary-claims-require-extraordinary-evidence-so-check--2099925690682630371|Modelos estruturados para automação]]", "[[extracts/x/bookmarks/2026-09-12-cwolferesearch-getting-ready-to-publish-my-complete-guide-to-rl-for-llms-to--2091570446164733962|RLHF e pós-treinamento de LLMs]]", "[[extracts/x/bookmarks/2026-09-12-googleresearch-introducing-timesfm-3-a-state-of-the-art-time-series-foundat--2094483372718580066|TimesFM-3: forecasting multivariado]]", "[[extracts/x/bookmarks/2026-09-12-cwolferesearch-i-just-published-my-complete-guide-to-reinforcement-learning--2091872097723359673|Guia completo de RL para LLMs]]", "[[extracts/x/bookmarks/2026-09-12-mtslive-xiaoyin-qu-breaks-down-deepseek-s-cheap-inference-philosophy--2085525434385695137|Economia de treinamento DeepSeek]]", "[[extracts/x/bookmarks/2026-09-19-eriksreinfelds-omg-togethercompute-i-love-you-this-is-time-to-first-token-f--2100218519636037929|Benchmark TTFT DeepSeek v4.1 Flash]]", "[[extracts/x/bookmarks/2026-09-12-fazle_karim1-googleresearch-i-wonder-how-it-would-do-on-this-research-of--2094501145536315670|GlucoFM: foundation model para CGM]]"]
theme: "Treinamento de modelos e atletas"
---

# Retrieve-for-Train: difusão para retrieval

**@GoogleResearch** · [2099951761985601580](https://x.com/GoogleResearch/status/2099951761985601580) · `announcement`

## Resumo
Google Research apresenta Retrieve-for-Train: usa RL offline uma única vez para compilar comportamentos de query fan-out alinhados a recompensa e destilar isso num modelo de difusão de 53.9M parâmetros, substituindo a inferência autorregressiva cara do LLM por geração single-pass de slates de busca em nível especialista. Vale salvar como padrão arquitetural de 'RL como transdutor de objetivo' + destilação para difusão, com speedup de 12-20x e latência sub-segundo.

## Pontos-chave
- Zero-shot LLMs para decomposição de query sofrem de paraphrastic collapse (sub-queries quase sinônimas, ex. 'bohemian festival fashion' vs 'clothes') e gargalo de latência autorregressiva — ~50 segundos em batches grandes de contexto — incompatível com barra de busca em produção.
- Pipeline em 3 etapas: (1) fan-out LM (Gemma3-4B/Qwen3-4B) treinado via RL com recompensa de propriedades set-level; (2) o LM congelado sintetiza pares (query → target-set) offline, sem labels humanos; (3) um difusor de 53.9M parâmetros aprende a mapear query embedding direto para o conjunto completo de target embeddings em uma passada não-autorregressiva.
- Recompensa composta de três pilares que agem como contra-âncoras mútuas: groundedness (distância ao manifold do banco), diversity (Vendi Score sobre o conjunto) e alignment ao prompt original — sem o termo de diversidade, o modelo faz reward hacking com strings degeneradas ('line ending line ending') ou parafrases repetitivas; treino com Soft-GRPO (GRPO + PPO soft).
- Resultado: supera single-query search, zero-shot expansion e Best-of-N otimizado em dois regimes (abstract retrieval e composicional fracamente supervisionado), nos domínios moda (CLIP) e playlists musicais (MuLan), com 12-20x de speedup sobre abordagens autorregressivas.
- Insight central transferível: RL como 'transdutor de objetivo' one-time em vez de motor de inferência online — desacoplar o custo de exploração dirigida por recompensa do modelo deployado, viabilizando propriedades set-level não-decomponíveis (diversidade, complementaridade) sem custo de tokens de raciocínio em tempo de teste.

## Links
- https://goo.gle/4xuV3lB

## Entidades
Google Research, Retrieve-for-Train, ICML 2026, Gemma3-4B, Qwen3-4B, CLIP, MuLan, Vendi Score, Soft-GRPO, Pengcheng Jiang, Judith Yue Li

> **Revisit:** `high` · **fonte:** `article`
