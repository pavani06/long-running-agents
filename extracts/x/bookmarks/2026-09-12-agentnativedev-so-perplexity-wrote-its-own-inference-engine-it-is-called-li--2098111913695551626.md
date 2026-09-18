---
title: "Engine de inferência Lily da Perplexity"
type: "extract"
source: "x"
status_id: "2098111913695551626"
handle: "agentnativedev"
url: "https://x.com/agentnativedev/status/2098111913695551626"
created_at: "2026-09-10T18:10:35.000Z"
extracted: "2026-09-13"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-12-agentnativedev-so-perplexity-wrote-its-own-inference-engine-it-is-called-li--2098111913695551626.json]]"
tags: ["performance", "runtime", "stack-tooling"]
topic: "Engine de inferência Lily da Perplexity"
summary: "Perplexity escreveu e open-sourcou (Apache-2.0, 2 de setembro) o Lily, seu próprio engine de inferência hiper-especializado em exatamente um modelo (Qwen3.6–35B-A3B) e uma família de hardware (Apple Silicon). Vale salvar como exemplo notável de otimização por especialização extrema na camada de runtime de LLM."
key_points: ["Perplexity desenvolveu internamente um engine de inferência próprio, chamado Lily, em vez de depender de runtimes existentes", "A especialização é radical: otimizado para exatamente um modelo (Qwen3.6–35B-A3B) e exatamente uma família de hardware (Apple Silicon)", "Foi open-sourcido em 2 de setembro sob licença Apache-2.0, permitindo uso e estudo público", "O caso ilustra o trade-off de abrir mão de generalidade em troca de desempenho máximo no par modelo/hardware"]
entities: ["Perplexity", "Lily", "Qwen3.6-35B-A3B", "Apple Silicon", "Apache-2.0"]
content_type: "announcement"
revisit: "medium"
grounded_in: "tweet"
links: []
media: ["https://pbs.twimg.com/media/HR39pEOa0AAvEFR.png"]
thin: false
theme: "IA, execução e vencedores"
relates-to: ["[[extracts/x/bookmarks/2026-09-12-aravsrinivas-we-re-open-sourcing-lily-perplexity-s-local-inference-engine--2095264908762140823|Perplexity Lily inferência local]]", "[[extracts/x/bookmarks/2026-09-14-andrewchen-vitostrokov-agreed-but-i-think-theres-two-issues-you-really--2099279190491353442|Apple M5 Ultra vs Nvidia para IA]]", "[[extracts/x/bookmarks/2026-09-14-andrewchen-current-homelab-setup-for-local-ai-experimentation-hermes-bo--2099247007454142644|Homelab para experimentação de IA local]]", "[[extracts/x/bookmarks/2026-09-18-completeskeptic-extraordinary-claims-require-extraordinary-evidence-so-check--2099925690682630371|Modelos estruturados para automação]]", "[[extracts/x/bookmarks/2026-09-12-skeptrune-sharing-a-map-of-the-most-important-skills-for-inference-eng--2098087369224405122|mapa de habilidades de inference engineering]]", "[[extracts/x/bookmarks/2026-09-15-suraj_sharma14-as-an-ai-infrastructure-engineer-you-must-build-these-projec--2099113368942465438|Projetos de infraestrutura de inferência]]", "[[extracts/x/bookmarks/2026-09-12-pythonhub-soup-fine-tune-and-post-train-llms-in-one-command-no-ssh-no--2092662174443249870|Ferramenta CLI de fine-tuning de LLMs]]", "[[extracts/x/bookmarks/2026-09-12-mtslive-xiaoyin-qu-breaks-down-deepseek-s-cheap-inference-philosophy--2085525434385695137|Economia de treinamento DeepSeek]]"]
---

# Engine de inferência Lily da Perplexity

**@agentnativedev** · [2098111913695551626](https://x.com/agentnativedev/status/2098111913695551626) · `announcement`

## Resumo
Perplexity escreveu e open-sourcou (Apache-2.0, 2 de setembro) o Lily, seu próprio engine de inferência hiper-especializado em exatamente um modelo (Qwen3.6–35B-A3B) e uma família de hardware (Apple Silicon). Vale salvar como exemplo notável de otimização por especialização extrema na camada de runtime de LLM.

## Pontos-chave
- Perplexity desenvolveu internamente um engine de inferência próprio, chamado Lily, em vez de depender de runtimes existentes
- A especialização é radical: otimizado para exatamente um modelo (Qwen3.6–35B-A3B) e exatamente uma família de hardware (Apple Silicon)
- Foi open-sourcido em 2 de setembro sob licença Apache-2.0, permitindo uso e estudo público
- O caso ilustra o trade-off de abrir mão de generalidade em troca de desempenho máximo no par modelo/hardware

## Entidades
Perplexity, Lily, Qwen3.6-35B-A3B, Apple Silicon, Apache-2.0

> **Revisit:** `medium` · **fonte:** `tweet`
