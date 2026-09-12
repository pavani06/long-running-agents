---
title: "Yann LeCun's $1B Bet Against LLMs [Part 1]"
type: "extract"
source: "youtube"
video_id: "kYkIdXwW2AE"
url: "https://www.youtube.com/watch?v=kYkIdXwW2AE"
channel: "Welch Labs"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-yann-lecun-s-1b-bet-against-llms-part-1--kYkIdXwW2AE.txt]]"
tags: ["arquitetura", "analise", "agents", "classification", "state", "model-selection"]
thesis: "Yann LeCun defende que arquiteturas de embedding conjunto preditivo (JEPA) — que preveem representações latentes em vez de pixels ou tokens e fundamentam world models capazes de prever as consequências de ações — são o caminho para IA confiável e eventualmente substituirão os LLMs autorregressivos."
concepts: ["JEPA (Joint Embedding Predictive Architecture)", "world models", "self-supervised learning", "joint embedding architectures", "representation collapse", "contrastive learning", "Barlow Twins (redução de redundância via matriz de correlação cruzada ≈ identidade)", "VICReg", "DINO / DINOv3", "Siamese neural networks", "predição autorregressiva de próximo token", "encoders + predictor em espaço latente (embeddings)", "predição condicionada a ações para controle robótico (V-JEPA 2)", "controle ótimo clássico com modelo aprendido (planejamento por otimização de sequências de ações)", "linear probe para avaliar qualidade de representações", "problema do blur em predição generativa de vídeo (média sob incerteza)", "metáfora do 'bolo' de LeCun: self-supervised > supervisionado > RL"]
tools: ["JEPA", "V-JEPA / V-JEPA 2", "DINO v1/v2/v3", "Barlow Twins", "VICReg", "Siamese networks", "AlexNet", "GPT-1", "GPT-2", "GPT-3", "ChatGPT", "Transformer", "OpenAI Gym / Universe", "ImageNet", "Layworld model (implementação de JEPA citada para a parte 2)"]
people: ["Yann LeCun", "Stéphane Deny", "Horace Barlow", "Ilya Sutskever", "Alec Radford", "OpenAI", "Meta / FAIR Paris", "Google DeepMind", "Bell Labs", "Hudson River Trading", "Welch Labs", "Tesla"]
claims: ["LLMs são ótimos em manipular linguagem mas 'basicamente nada mais'; world models tipo JEPA resolverão problemas diferentes primeiro e eventualmente substituirão LLMs (LeCun)", "Predição generativa de vídeo em nível de pixel falha porque, sob incerteza, o modelo média os desfechos possíveis e produz blur, que se compõe em horizontes longos", "Não é viável enumerar saídas discretas para vídeo: há ~10^15 milhões de frames HD possíveis, tornando a abordagem de vocabulário de tokens inviável", "O que importa no pre-training são as representações internas aprendidas, não a geração em si; next-token prediction é só um proxy que funcionou bem em linguagem", "Barlow Twins evita representation collapse sem exemplos negativos: maximizar correlação dos neurônios correspondentes (diagonal ≈ 1) e minimizar redundância entre neurônios diferentes (off-diagonal ≈ 0)", "Encoder Barlow Twins congelado + linear probe atingiu 73,2% de acurácia no ImageNet vs 59,3% do AlexNet totalmente supervisionado", "DINOv3 (ago/2025) alcançou 88,4% no ImageNet com arquitetura de embedding conjunto, praticamente igualando o estado da arte supervisionado (88,6%)", "Condicionar o predictor do JEPA aos sinais de controle de um braço robótico produz um world model utilizável para planejamento: busca, por otimização, da sequência de ações cujo estado predito coincida com o estado-meta no espaço de embedding", "Sistemas agenticos confiáveis precisam prever as consequências de suas ações antes de executá-las (para cumprir tarefas e garantir guard rails de segurança); a inferência vira busca em vez de mera predição autorregressiva", "Um adolescente aprende a dirigir em ~20 horas, enquanto sistemas nível 2 (ex.: Tesla) usam milhões de horas e não alcançam nível 3-5; a vantagem 'secreta' seria possuir world models pré-aprendidos"]
deep_dive: "medium"
deep_dive_reason: "Há alta densidade de detalhe arquitetural e benchmarks concretos sobre JEPA e aprendizado self-supervised, mas o conteúdo trata principalmente de arquitetura de modelos de ML, com relevância apenas tangencial aos domínios de harness, context-engineering, evals, agent-fleets e governança."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-yann-lecun-on-what-comes-after-llms--ngBraLDqzdI|Yann LeCun on What Comes After LLMs]]", "[[extracts/youtube/ai-learning/2026-09-11-ilya-sutskever-we-re-moving-from-the-age-of-scaling-to-the-age-of-research--aR20FWCCjAs|Ilya Sutskever – We're moving from the age of scaling to the age of research]]", "[[extracts/youtube/ai-learning/2026-09-11-ilya-sutskever-sequence-to-sequence-learning-with-neural-networks-what-a-decade--1yvBqasHLZs|Ilya Sutskever: \"Sequence to sequence learning with neural networks: what a decade\"]]", "[[extracts/youtube/ai-learning/2026-09-11-stanford-cs25-transformers-united-v6-i-from-language-models-to-native-multimodal--NDdc39KYqDU|Stanford CS25: Transformers United V6 I From Language Models to Native Multimodal Intelligence]]", "[[extracts/youtube/ai-learning/2026-09-11-stanford-cs153-frontier-systems-amit-jain-from-luma-ai-on-unified-intelligence-s--6nUl_w5W9Wk|Stanford CS153 Frontier Systems | Amit Jain from Luma AI on Unified Intelligence Systems]]", "[[extracts/youtube/ai-learning/2026-09-11-jeff-dean-the-1-rule-for-building-in-ai--CxXgV54KzpQ|Jeff Dean: The 1% Rule for Building in AI]]", "[[extracts/youtube/ai-learning/2026-09-11-stanford-robotics-seminar-engr319-spring-2026-integrated-learning-and-planning--3W36pd50Wqw|Stanford Robotics Seminar ENGR319 | Spring 2026 | Integrated Learning and Planning]]", "[[extracts/youtube/ai-learning/2026-09-11-did-openai-just-solve-hallucinations--xGO5Q94XXf0|Did OpenAI just solve hallucinations?]]"]
---

# Yann LeCun's $1B Bet Against LLMs [Part 1]

## Tese
Yann LeCun defende que arquiteturas de embedding conjunto preditivo (JEPA) — que preveem representações latentes em vez de pixels ou tokens e fundamentam world models capazes de prever as consequências de ações — são o caminho para IA confiável e eventualmente substituirão os LLMs autorregressivos.

## Conceitos-chave
- JEPA (Joint Embedding Predictive Architecture)
- world models
- self-supervised learning
- joint embedding architectures
- representation collapse
- contrastive learning
- Barlow Twins (redução de redundância via matriz de correlação cruzada ≈ identidade)
- VICReg
- DINO / DINOv3
- Siamese neural networks
- predição autorregressiva de próximo token
- encoders + predictor em espaço latente (embeddings)
- predição condicionada a ações para controle robótico (V-JEPA 2)
- controle ótimo clássico com modelo aprendido (planejamento por otimização de sequências de ações)
- linear probe para avaliar qualidade de representações
- problema do blur em predição generativa de vídeo (média sob incerteza)
- metáfora do 'bolo' de LeCun: self-supervised > supervisionado > RL

## Ferramentas & pessoas
**Ferramentas:** JEPA, V-JEPA / V-JEPA 2, DINO v1/v2/v3, Barlow Twins, VICReg, Siamese networks, AlexNet, GPT-1, GPT-2, GPT-3, ChatGPT, Transformer, OpenAI Gym / Universe, ImageNet, Layworld model (implementação de JEPA citada para a parte 2)

**Pessoas/orgs:** Yann LeCun, Stéphane Deny, Horace Barlow, Ilya Sutskever, Alec Radford, OpenAI, Meta / FAIR Paris, Google DeepMind, Bell Labs, Hudson River Trading, Welch Labs, Tesla

## Claims acionáveis
- LLMs são ótimos em manipular linguagem mas 'basicamente nada mais'; world models tipo JEPA resolverão problemas diferentes primeiro e eventualmente substituirão LLMs (LeCun)
- Predição generativa de vídeo em nível de pixel falha porque, sob incerteza, o modelo média os desfechos possíveis e produz blur, que se compõe em horizontes longos
- Não é viável enumerar saídas discretas para vídeo: há ~10^15 milhões de frames HD possíveis, tornando a abordagem de vocabulário de tokens inviável
- O que importa no pre-training são as representações internas aprendidas, não a geração em si; next-token prediction é só um proxy que funcionou bem em linguagem
- Barlow Twins evita representation collapse sem exemplos negativos: maximizar correlação dos neurônios correspondentes (diagonal ≈ 1) e minimizar redundância entre neurônios diferentes (off-diagonal ≈ 0)
- Encoder Barlow Twins congelado + linear probe atingiu 73,2% de acurácia no ImageNet vs 59,3% do AlexNet totalmente supervisionado
- DINOv3 (ago/2025) alcançou 88,4% no ImageNet com arquitetura de embedding conjunto, praticamente igualando o estado da arte supervisionado (88,6%)
- Condicionar o predictor do JEPA aos sinais de controle de um braço robótico produz um world model utilizável para planejamento: busca, por otimização, da sequência de ações cujo estado predito coincida com o estado-meta no espaço de embedding
- Sistemas agenticos confiáveis precisam prever as consequências de suas ações antes de executá-las (para cumprir tarefas e garantir guard rails de segurança); a inferência vira busca em vez de mera predição autorregressiva
- Um adolescente aprende a dirigir em ~20 horas, enquanto sistemas nível 2 (ex.: Tesla) usam milhões de horas e não alcançam nível 3-5; a vantagem 'secreta' seria possuir world models pré-aprendidos

> **Deep dive:** `medium` — Há alta densidade de detalhe arquitetural e benchmarks concretos sobre JEPA e aprendizado self-supervised, mas o conteúdo trata principalmente de arquitetura de modelos de ML, com relevância apenas tangencial aos domínios de harness, context-engineering, evals, agent-fleets e governança.
