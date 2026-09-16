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
