---
title: "Recurrent Looped Transformer"
type: "extract"
source: "x"
status_id: "2099180888684937556"
handle: "yifanzhang_"
url: "https://x.com/yifanzhang_/status/2099180888684937556"
created_at: "2026-09-13T16:58:19.000Z"
extracted: "2026-09-15"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-14-yifanzhang_-rasbt-https-t-co-tovrlbceki--2099180888684937556.json]]"
tags: ["arquitetura", "memory-architecture", "state", "runtime", "performance"]
topic: "Recurrent Looped Transformer"
summary: "Tech report de Yifan Zhang sobre o RLT, arquitetura que carrega computação latente entre todos os tokens (prompt e resposta) via encoder causal com memória KV global + decoder recorrente com SWA e feedback do estado oculto anterior. Resultados sintéticos de state tracking (79K parâmetros) mostram generalização de comprimento superior a Transformers padrão, embora com decaimento além do comprimento de treino."
key_points: ["Arquitetura: encoder causal constrói memória KV global lida por cross-attention apenas até a posição atual; decoder recorrente combina SWA local com feedback do último hidden state — o caminho computacional atravessa t·L_D blocos após t tokens com custo fixo por token ('profundidade infinita' temporal, não computação infinita por token).", "Co-design modelo–algoritmo de RL: pretraining, SFT, sampling e replay de RL on-policy usam a mesma transição de estado completa (recorrência do prompt + caches SWA), com BPTT total através de outputs recorrentes, KV do decoder e memória do encoder; desanexar qualquer deles é aproximação de gradiente.", "Configuração concreta: 48 camadas de encoder + 48 de decoder com pesos compartilhados; blocos do decoder fazem cross-attention extra sobre a memória do encoder, então contagens iguais de camadas não implicam FLOPs iguais.", "Prova de conceito sintética (state tracking, ~79K params, 3 seeds): RLT atinge ~100% no comprimento de treino (32 ops) vs ~72% do Transformer em parity, e mantém vantagem em 2× e 4× o comprimento (60.8% vs ~48% em parity; chance = 50%).", "Caveats explícitos: melhorias de raciocínio em larga escala, speedups de hardware e scaling de RL são metas de pesquisa, não resultados medidos; em five-state transitions a 128 ops o RLT cai para 20.7%, próximo do acaso (20%)."]
entities: ["Yifan Zhang", "Aradhye Agarwal", "Sebastian Raschka (@rasbt)", "Recurrent Looped Transformer (RLT)", "GitHub: yifanzhang-pro/recurrent-looped-tranformer"]
content_type: "resource"
revisit: "high"
grounded_in: "article"
thin: false
links: ["https://github.com/yifanzhang-pro/recurrent-looped-tranformer#independent-proof-of-concept"]
media: []
---

# Recurrent Looped Transformer

**@yifanzhang_** · [2099180888684937556](https://x.com/yifanzhang_/status/2099180888684937556) · `resource`

## Resumo
Tech report de Yifan Zhang sobre o RLT, arquitetura que carrega computação latente entre todos os tokens (prompt e resposta) via encoder causal com memória KV global + decoder recorrente com SWA e feedback do estado oculto anterior. Resultados sintéticos de state tracking (79K parâmetros) mostram generalização de comprimento superior a Transformers padrão, embora com decaimento além do comprimento de treino.

## Pontos-chave
- Arquitetura: encoder causal constrói memória KV global lida por cross-attention apenas até a posição atual; decoder recorrente combina SWA local com feedback do último hidden state — o caminho computacional atravessa t·L_D blocos após t tokens com custo fixo por token ('profundidade infinita' temporal, não computação infinita por token).
- Co-design modelo–algoritmo de RL: pretraining, SFT, sampling e replay de RL on-policy usam a mesma transição de estado completa (recorrência do prompt + caches SWA), com BPTT total através de outputs recorrentes, KV do decoder e memória do encoder; desanexar qualquer deles é aproximação de gradiente.
- Configuração concreta: 48 camadas de encoder + 48 de decoder com pesos compartilhados; blocos do decoder fazem cross-attention extra sobre a memória do encoder, então contagens iguais de camadas não implicam FLOPs iguais.
- Prova de conceito sintética (state tracking, ~79K params, 3 seeds): RLT atinge ~100% no comprimento de treino (32 ops) vs ~72% do Transformer em parity, e mantém vantagem em 2× e 4× o comprimento (60.8% vs ~48% em parity; chance = 50%).
- Caveats explícitos: melhorias de raciocínio em larga escala, speedups de hardware e scaling de RL são metas de pesquisa, não resultados medidos; em five-state transitions a 128 ops o RLT cai para 20.7%, próximo do acaso (20%).

## Links
- https://github.com/yifanzhang-pro/recurrent-looped-tranformer#independent-proof-of-concept

## Entidades
Yifan Zhang, Aradhye Agarwal, Sebastian Raschka (@rasbt), Recurrent Looped Transformer (RLT), GitHub: yifanzhang-pro/recurrent-looped-tranformer

> **Revisit:** `high` · **fonte:** `article`
