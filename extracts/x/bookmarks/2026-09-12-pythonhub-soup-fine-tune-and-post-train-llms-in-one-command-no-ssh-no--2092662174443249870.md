---
title: "Ferramenta CLI de fine-tuning de LLMs"
type: "extract"
source: "x"
status_id: "2092662174443249870"
handle: "PythonHub"
url: "https://x.com/PythonHub/status/2092662174443249870"
created_at: "2026-08-26T17:15:16.000Z"
extracted: "2026-09-13"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-12-pythonhub-soup-fine-tune-and-post-train-llms-in-one-command-no-ssh-no--2092662174443249870.json]]"
tags: ["stack-tooling", "frameworks", "performance", "verification"]
topic: "Ferramenta CLI de fine-tuning de LLMs"
summary: "Soup (soup-cli) é uma ferramenta open-source que reduz o fine-tuning e post-training de LLMs a um YAML + um comando (`soup train`), sem SSH e com auto-detecção de GPU, batch e quantização. Destaque para layer streaming (beta) que treina um modelo 8B em GPU de 4 GB de forma bit-exata, e um changelog recente focado em correção de configuração silenciosamente ignorada."
key_points: ["Layer streaming (opt-in, beta) mantém o base model congelado fora da VRAM e alimenta a GPU camada a camada: Llama-3.1-8B + NF4 atingiu 119,6 tok/s com pico de 3,32 GB em RTX 3050 Laptop 4 GB, bit-exato vs execução residente e reproduzido em H100 com o mesmo pico de VRAM.", "v0.75.0 endurece a validação de config: chave desconhecida (typo como 'quantizaton') agora falha o load (exit 1 / ValueError) em vez de ser descartada silenciosamente; antes uma configuração validada podia simplesmente não ser aplicada durante o run.", "Backend MLX passou a honrar 6 opções de treino que eram validadas e depois descartadas (train_on_responses_only, scheduler, weight_decay, etc.); 24 dos 32 nomes de otimizador sem equivalente MLX agora são recusados por nome em vez de virar AdamW silenciosamente.", "Cobre SFT/DPO/GRPO/PPO/KTO/ORPO/SimPO/IPO, PEFT zoo (DoRA, LoRA+, rsLoRA, VeRA, PiSSA), export GGUF/ONNX para Ollama/llama.cpp, servidor OpenAI-compatible, Web UI com métricas ao vivo, eval-gated training e templates de compliance (HIPAA/SOC2/EU-AI-Act).", "Guia de VRAM (QLoRA 4-bit): 8 GB ~7B, 16 GB ~14B, 24 GB ~34B, 48 GB ~70B; funciona com qualquer modelo HF que carregue via AutoModelForCausalLM, com 100+ receitas prontas."]
entities: ["Soup / soup-cli", "Llama-3.1-8B-Instruct", "MLX", "HuggingFace Hub", "PyTorch / transformers / TRL / peft", "Ollama", "llama.cpp", "GSPO (arXiv:2507.18071)"]
content_type: "tool"
revisit: "medium"
grounded_in: "article"
links: ["https://github.com/MakazhanAlpamys/Soup"]
media: []
thin: false
theme: "Confiabilidade e avaliação de agentes"
relates-to: ["[[extracts/x/bookmarks/2026-09-12-openhonor-puro-2b-is-open-beyond-the-weights-technical-report-final-in--2093994412770566256|Puro-2B: receita aberta de pré-treinamento barato]]", "[[extracts/x/bookmarks/2026-09-18-completeskeptic-extraordinary-claims-require-extraordinary-evidence-so-check--2099925690682630371|Modelos estruturados para automação]]", "[[extracts/x/bookmarks/2026-09-12-googleresearch-introducing-toolgrad-an-efficient-framework-for-generating-t--2098183830968705163|ToolGrad: geração de datasets de tool-use]]", "[[extracts/x/bookmarks/2026-09-12-cwolferesearch-getting-ready-to-publish-my-complete-guide-to-rl-for-llms-to--2091570446164733962|RLHF e pós-treinamento de LLMs]]", "[[extracts/x/bookmarks/2026-09-12-agentnativedev-so-perplexity-wrote-its-own-inference-engine-it-is-called-li--2098111913695551626|Engine de inferência Lily da Perplexity]]", "[[extracts/x/bookmarks/2026-09-15-suraj_sharma14-as-an-ai-infrastructure-engineer-you-must-build-these-projec--2099113368942465438|Projetos de infraestrutura de inferência]]"]
---

# Ferramenta CLI de fine-tuning de LLMs

**@PythonHub** · [2092662174443249870](https://x.com/PythonHub/status/2092662174443249870) · `tool`

## Resumo
Soup (soup-cli) é uma ferramenta open-source que reduz o fine-tuning e post-training de LLMs a um YAML + um comando (`soup train`), sem SSH e com auto-detecção de GPU, batch e quantização. Destaque para layer streaming (beta) que treina um modelo 8B em GPU de 4 GB de forma bit-exata, e um changelog recente focado em correção de configuração silenciosamente ignorada.

## Pontos-chave
- Layer streaming (opt-in, beta) mantém o base model congelado fora da VRAM e alimenta a GPU camada a camada: Llama-3.1-8B + NF4 atingiu 119,6 tok/s com pico de 3,32 GB em RTX 3050 Laptop 4 GB, bit-exato vs execução residente e reproduzido em H100 com o mesmo pico de VRAM.
- v0.75.0 endurece a validação de config: chave desconhecida (typo como 'quantizaton') agora falha o load (exit 1 / ValueError) em vez de ser descartada silenciosamente; antes uma configuração validada podia simplesmente não ser aplicada durante o run.
- Backend MLX passou a honrar 6 opções de treino que eram validadas e depois descartadas (train_on_responses_only, scheduler, weight_decay, etc.); 24 dos 32 nomes de otimizador sem equivalente MLX agora são recusados por nome em vez de virar AdamW silenciosamente.
- Cobre SFT/DPO/GRPO/PPO/KTO/ORPO/SimPO/IPO, PEFT zoo (DoRA, LoRA+, rsLoRA, VeRA, PiSSA), export GGUF/ONNX para Ollama/llama.cpp, servidor OpenAI-compatible, Web UI com métricas ao vivo, eval-gated training e templates de compliance (HIPAA/SOC2/EU-AI-Act).
- Guia de VRAM (QLoRA 4-bit): 8 GB ~7B, 16 GB ~14B, 24 GB ~34B, 48 GB ~70B; funciona com qualquer modelo HF que carregue via AutoModelForCausalLM, com 100+ receitas prontas.

## Links
- https://github.com/MakazhanAlpamys/Soup

## Entidades
Soup / soup-cli, Llama-3.1-8B-Instruct, MLX, HuggingFace Hub, PyTorch / transformers / TRL / peft, Ollama, llama.cpp, GSPO (arXiv:2507.18071)

> **Revisit:** `medium` · **fonte:** `article`
