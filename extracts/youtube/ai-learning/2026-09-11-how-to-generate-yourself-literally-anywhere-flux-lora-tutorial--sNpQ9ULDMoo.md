---
title: "How To Generate Yourself LITERALLY Anywhere - Flux LoRA Tutorial"
type: "extract"
source: "youtube"
video_id: "sNpQ9ULDMoo"
url: "https://www.youtube.com/watch?v=sNpQ9ULDMoo"
channel: "100x Engineers"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-how-to-generate-yourself-literally-anywhere-flux-lora-tutorial--sNpQ9ULDMoo.txt]]"
tags: ["process", "stack-tooling", "model-selection", "governanca"]
thesis: "É possível gerar imagens fotorrealistas do próprio rosto (headshots de LinkedIn, posts de redes sociais, campanhas) treinando um LoRA sobre o modelo Flux Dev na plataforma Replicate, usando apenas 20-25 fotos pessoais, por cerca de US$2-4 e 15-30 minutos de treinamento."
concepts: ["LoRA (Low-Rank Adaptation)", "fine-tuning de modelos de difusão de imagem", "dataset de imagens faciais (variedade de ângulos e iluminação)", "trigger word como marcador de recuperação do dataset", "steps de treinamento (2000)", "inferência com modelo treinado", "arquivos de pesos .safetensors", "tokens de acesso da Hugging Face", "consentimento e ética no treinamento de rostos", "treinamento de LoRA em estilos/marcas (ex.: personagem de publicidade)"]
tools: ["Replicate", "FLUX.1-dev (Flux Dev LoRA trainer)", "Black Forest Labs", "Hugging Face", "Stable Diffusion (menção comparativa)", "Midjourney (menção comparativa)", "iPhone (captura do dataset)"]
people: ["Shev (apresentador)", "100x Engineers / AI Labs by 100x", "Amul (experimento com a 'Amul girl')"]
claims: ["20 a 25 fotos de alta resolução, tiradas de ângulos e condições de iluminação variados, são suficientes para treinar o LoRA no próprio rosto", "Definir steps em 2000 é um ponto ideal; não é necessário alterar learning rate nem LoRA rank", "Treinar um LoRA no Replicate custa cerca de US$2-4 (₹200-250) e cada imagem gerada custa poucos centavos", "O treinamento leva de 15 a 30 minutos, dependendo do tamanho do dataset compactado em zip", "A trigger word (ex.: 'boson') no prompt faz o modelo recalls o dataset treinado, funcionando como marcador de identificação", "O token da Hugging Face é exibido apenas uma vez na criação e deve ser copiado imediatamente; caso contrário é preciso gerar um novo", "Os pesos treinados ficam disponíveis no Hugging Face como arquivos .safetensors e podem ser usados fora do Replicate, em qualquer plataforma", "Os valores default do modelo de inferência (aspect ratio, número de outputs até 4, força do prompt/LoRA) já são adequados para a maioria dos casos de uso", "Treinar modelos no rosto de outra pessoa sem consentimento explícito pode gerar problemas legais e éticos sérios", "LoRAs também podem ser treinados em estilos visuais e personagens de marca (ex.: anúncios da Amul) para gerar campanhas similares"]
deep_dive: "low"
deep_dive_reason: "Tutorial introdutório passo a passo de fine-tuning de imagem com forte caráter promocional, sem densidade arquitetural nem relevância para harness, context-engineering, evals, agent-fleets ou ontologia de agentes."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-fine-tune-the-biggest-open-source-models-even-with-a-bad-pc--kxstlfc8Lw4|Fine-Tune the biggest open-source models (even with a bad PC)]]", "[[extracts/youtube/ai-learning/2026-09-11-create-anything-with-nano-banana-pro-heres-how--2VktR2fAmF0|Create Anything with Nano Banana Pro, Here’s How]]", "[[extracts/youtube/ai-learning/2026-09-11-stanford-cs153-frontier-systems-amit-jain-from-luma-ai-on-unified-intelligence-s--6nUl_w5W9Wk|Stanford CS153 Frontier Systems | Amit Jain from Luma AI on Unified Intelligence Systems]]", "[[extracts/youtube/ai-learning/2026-09-11-sora-da-openai-e-lancada-primeiras-impressoes-das-funcoes--TBmcvEmPXJ4|SORA da OPENAI é LANÇADA! PRIMEIRAS IMPRESSÕES das FUNÇÕES 🤯]]"]
theme: "Stack de IA e Prompting"
---

# How To Generate Yourself LITERALLY Anywhere - Flux LoRA Tutorial

## Tese
É possível gerar imagens fotorrealistas do próprio rosto (headshots de LinkedIn, posts de redes sociais, campanhas) treinando um LoRA sobre o modelo Flux Dev na plataforma Replicate, usando apenas 20-25 fotos pessoais, por cerca de US$2-4 e 15-30 minutos de treinamento.

## Conceitos-chave
- LoRA (Low-Rank Adaptation)
- fine-tuning de modelos de difusão de imagem
- dataset de imagens faciais (variedade de ângulos e iluminação)
- trigger word como marcador de recuperação do dataset
- steps de treinamento (2000)
- inferência com modelo treinado
- arquivos de pesos .safetensors
- tokens de acesso da Hugging Face
- consentimento e ética no treinamento de rostos
- treinamento de LoRA em estilos/marcas (ex.: personagem de publicidade)

## Ferramentas & pessoas
**Ferramentas:** Replicate, FLUX.1-dev (Flux Dev LoRA trainer), Black Forest Labs, Hugging Face, Stable Diffusion (menção comparativa), Midjourney (menção comparativa), iPhone (captura do dataset)

**Pessoas/orgs:** Shev (apresentador), 100x Engineers / AI Labs by 100x, Amul (experimento com a 'Amul girl')

## Claims acionáveis
- 20 a 25 fotos de alta resolução, tiradas de ângulos e condições de iluminação variados, são suficientes para treinar o LoRA no próprio rosto
- Definir steps em 2000 é um ponto ideal; não é necessário alterar learning rate nem LoRA rank
- Treinar um LoRA no Replicate custa cerca de US$2-4 (₹200-250) e cada imagem gerada custa poucos centavos
- O treinamento leva de 15 a 30 minutos, dependendo do tamanho do dataset compactado em zip
- A trigger word (ex.: 'boson') no prompt faz o modelo recalls o dataset treinado, funcionando como marcador de identificação
- O token da Hugging Face é exibido apenas uma vez na criação e deve ser copiado imediatamente; caso contrário é preciso gerar um novo
- Os pesos treinados ficam disponíveis no Hugging Face como arquivos .safetensors e podem ser usados fora do Replicate, em qualquer plataforma
- Os valores default do modelo de inferência (aspect ratio, número de outputs até 4, força do prompt/LoRA) já são adequados para a maioria dos casos de uso
- Treinar modelos no rosto de outra pessoa sem consentimento explícito pode gerar problemas legais e éticos sérios
- LoRAs também podem ser treinados em estilos visuais e personagens de marca (ex.: anúncios da Amul) para gerar campanhas similares

> **Deep dive:** `low` — Tutorial introdutório passo a passo de fine-tuning de imagem com forte caráter promocional, sem densidade arquitetural nem relevância para harness, context-engineering, evals, agent-fleets ou ontologia de agentes.
