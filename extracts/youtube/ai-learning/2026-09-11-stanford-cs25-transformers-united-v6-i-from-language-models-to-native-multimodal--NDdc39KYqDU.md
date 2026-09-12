---
title: "Stanford CS25: Transformers United V6 I From Language Models to Native Multimodal Intelligence"
type: "extract"
source: "youtube"
video_id: "NDdc39KYqDU"
url: "https://www.youtube.com/watch?v=NDdc39KYqDU"
channel: "Stanford Online"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-stanford-cs25-transformers-united-v6-i-from-language-models-to-native-multimodal--NDdc39KYqDU.txt]]"
tags: ["arquitetura", "analise-estrutural", "roadmap"]
thesis: "Modelos de linguagem nativamente multimodais podem ser construídos estendendo o paradigma de tokenização e geração autorregressiva dos LLMs a todas as modalidades, mas essa transferência é assimétrica e incompleta — sobretudo na unificação de entendimento e geração e na inteligência para o mundo físico."
concepts: ["Tokenização cross-modal: patchify de imagens, transformadas de áudio e vídeo como sequência de frames", "Dois tipos de modelo: entrada multimodal com saída apenas textual (Gemini, Qwen, Kimi) vs. modelos Omni com saída multimodal (GPT-4o)", "Chameleon: discretização de imagens via VQ-VAE com codebook aprendido e treinamento entrelaçado texto+imagem do zero", "Transfusion: autorregressão para texto combinada com difusão para imagens em um único transformer (atenção causal no texto, bidirecional na imagem)", "Mixture of Transformers (MoT): conjuntos de parâmetros por modalidade (projeções QKV e FFN separadas) com roteamento determinístico por token e atenção conjunta", "Dilema das duas codificações: representações eficientes para geração (VAE) são ineficientes para entendimento de imagem, motivando dois codificadores nos modelos state-of-the-art", "Transferência assimétrica: melhor entendimento melhora fortemente a geração, mas treinar geração não melhora o entendimento", "Puzzle de Sergey Levine: next-token prediction gera capacidades emergentes em linguagem, mas next-frame prediction não fortalece modelos de vídeo na mesma medida", "Hipótese explicativa: linguagem é abstração comprimida da cognição humana, enquanto imagem/vídeo são dados sensoriais passivos com loss landscape mais complicada e redundância entre frames", "Planejamento textual antes de gerar imagem (thinking before generation) melhora detalhe e reduz alucinação", "Treinamento assíncrono de modalidades: congelar o modelo de texto e treinar apenas o conjunto novo de parâmetros para geração de imagem/fala", "Modelos vision-language-action em robótica reutilizando arquitetura estilo MoT com parâmetros dedicados a vetores de ação", "Leis de escala multimodais exatas ainda subexploradas (comportamento de power law observado apenas na tendência geral)", "Princípio de alinhar outras modalidades sobre o texto, e não renderizar texto como imagem (OCR), para preservar capacidades agentic/reasoning", "JEPA e representações semânticas/orientadas a objeto para entendimento físico-espacial do mundo real"]
tools: ["ChatGPT", "Claude Code", "Codex", "Gemini", "Qwen", "Kimi", "GPT-4o", "Chameleon", "Transfusion", "VQ-VAE", "SigLIP", "BAGEL", "Mixture of Transformers (MoT)", "Mixture of Experts", "JEPA"]
people: ["Victoria Lin", "Thinking Machines Lab", "Meta AI", "Salesforce AI Research", "University of Washington", "Sergey Levine (UC Berkeley)", "Physical Intelligence", "CS25 (série de palestras)"]
claims: ["Tokenize todas as modalidades em tokens (densos ou discretos) e treine com objetivo autorregressivo unificado para transferir prompting, instrução, planejamento e raciocínio dos LLMs para o multimodal", "Evite discretização VQ-VAE quando entendimento de imagem é prioridade: ela causa perda significativa de informação frente a codificadores contínuos como SigLIP", "Use arquitetura Transfusion (AR no texto + difusão bidirecional na imagem) para gerar imagens de melhor qualidade com muito menos orçamento de tokens", "Adote parâmetros separados por modalidade (MoT) com roteamento determinístico e atenção conjunta para melhorar substancialmente a geração não-textual sem sacrificar desempenho de texto", "Estenda um LLM existente com nova modalidade congelando o texto e treinando apenas o conjunto adicional de parâmetros (treinamento assíncrono), em vez de fine-tuning completo", "Aloque mais experts ao texto do que à imagem: geração de imagem escala mais devagar com o número de experts", "Permita que o modelo gere raciocínio/trilha de pensamento em texto antes de produzir a imagem para obter mais detalhe e menos alucinação", "Planeje usar dois codificadores de imagem (um para entendimento, outro para geração) até que a unificação de representação amadureça", "Não conte com treino de geração de vídeo/imagem para melhorar conhecimento geral ou entendimento — a transferência inversa não foi observada empiricamente", "Prefira alinhar modalidades sobre o texto em vez de renderizar texto como imagem (OCR-ificado), que tende a ser menos eficiente para escalar capacidades de raciocínio", "A derivação de leis de escala multimodais exatas é um problema aberto e oportunidade concreta de pesquisa", "Use modelos de linguagem multimodal como backbone para action prediction em robótica em vez de treinar do zero, aproveitando a transferência positiva do conhecimento de mundo"]
deep_dive: "medium"
deep_dive_reason: "Palestra densa em arquitetura de modelos (Chameleon, Transfusion, MoT, BAGEL) com insights acionáveis de treinamento e escalabilidade, mas recapitula trabalho publicado sobre fundações de modelos e tem aplicação direta limitada a harness, context-engineering, evals ou agent-fleets."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-stanford-cs153-frontier-systems-amit-jain-from-luma-ai-on-unified-intelligence-s--6nUl_w5W9Wk|Stanford CS153 Frontier Systems | Amit Jain from Luma AI on Unified Intelligence Systems]]", "[[extracts/youtube/ai-learning/2026-09-11-yann-lecun-on-what-comes-after-llms--ngBraLDqzdI|Yann LeCun on What Comes After LLMs]]", "[[extracts/youtube/ai-learning/2026-09-11-yann-lecun-s-1b-bet-against-llms-part-1--kYkIdXwW2AE|Yann LeCun's $1B Bet Against LLMs [Part 1]]]", "[[extracts/youtube/ai-learning/2026-09-11-stanford-webinar-large-language-models-get-the-hype-but-compound-systems-are-the--vRTcE19M-KE|Stanford Webinar - Large Language Models Get the Hype, but Compound Systems Are the Future of AI]]", "[[extracts/youtube/ai-learning/2026-09-11-stanford-robotics-seminar-engr319-spring-2026-integrated-learning-and-planning--3W36pd50Wqw|Stanford Robotics Seminar ENGR319 | Spring 2026 | Integrated Learning and Planning]]", "[[extracts/youtube/ai-learning/2026-09-11-creating-agents-that-co-create-karina-nguyen-openai--1XvN5EBDnDw|Creating Agents that Co-Create — Karina Nguyen, OpenAI]]", "[[extracts/youtube/ai-learning/2026-09-11-intro-to-fine-tuning-large-language-models--H-oCV5brtU4|Intro to Fine-Tuning Large Language Models]]", "[[extracts/youtube/ai-learning/2026-09-11-stanford-cs336-language-modeling-from-scratch-spring-2026-lecture-10-inference--EfM546A79aM|Stanford CS336 Language Modeling from Scratch | Spring 2026 | Lecture 10: Inference]]", "[[extracts/youtube/ai-learning/2026-09-11-let-s-build-gpt-from-scratch-in-code-spelled-out--kCc8FmEb1nY|Let's build GPT: from scratch, in code, spelled out.]]"]
theme: "Fundamentos e Arquitetura de LLMs"
---

# Stanford CS25: Transformers United V6 I From Language Models to Native Multimodal Intelligence

## Tese
Modelos de linguagem nativamente multimodais podem ser construídos estendendo o paradigma de tokenização e geração autorregressiva dos LLMs a todas as modalidades, mas essa transferência é assimétrica e incompleta — sobretudo na unificação de entendimento e geração e na inteligência para o mundo físico.

## Conceitos-chave
- Tokenização cross-modal: patchify de imagens, transformadas de áudio e vídeo como sequência de frames
- Dois tipos de modelo: entrada multimodal com saída apenas textual (Gemini, Qwen, Kimi) vs. modelos Omni com saída multimodal (GPT-4o)
- Chameleon: discretização de imagens via VQ-VAE com codebook aprendido e treinamento entrelaçado texto+imagem do zero
- Transfusion: autorregressão para texto combinada com difusão para imagens em um único transformer (atenção causal no texto, bidirecional na imagem)
- Mixture of Transformers (MoT): conjuntos de parâmetros por modalidade (projeções QKV e FFN separadas) com roteamento determinístico por token e atenção conjunta
- Dilema das duas codificações: representações eficientes para geração (VAE) são ineficientes para entendimento de imagem, motivando dois codificadores nos modelos state-of-the-art
- Transferência assimétrica: melhor entendimento melhora fortemente a geração, mas treinar geração não melhora o entendimento
- Puzzle de Sergey Levine: next-token prediction gera capacidades emergentes em linguagem, mas next-frame prediction não fortalece modelos de vídeo na mesma medida
- Hipótese explicativa: linguagem é abstração comprimida da cognição humana, enquanto imagem/vídeo são dados sensoriais passivos com loss landscape mais complicada e redundância entre frames
- Planejamento textual antes de gerar imagem (thinking before generation) melhora detalhe e reduz alucinação
- Treinamento assíncrono de modalidades: congelar o modelo de texto e treinar apenas o conjunto novo de parâmetros para geração de imagem/fala
- Modelos vision-language-action em robótica reutilizando arquitetura estilo MoT com parâmetros dedicados a vetores de ação
- Leis de escala multimodais exatas ainda subexploradas (comportamento de power law observado apenas na tendência geral)
- Princípio de alinhar outras modalidades sobre o texto, e não renderizar texto como imagem (OCR), para preservar capacidades agentic/reasoning
- JEPA e representações semânticas/orientadas a objeto para entendimento físico-espacial do mundo real

## Ferramentas & pessoas
**Ferramentas:** ChatGPT, Claude Code, Codex, Gemini, Qwen, Kimi, GPT-4o, Chameleon, Transfusion, VQ-VAE, SigLIP, BAGEL, Mixture of Transformers (MoT), Mixture of Experts, JEPA

**Pessoas/orgs:** Victoria Lin, Thinking Machines Lab, Meta AI, Salesforce AI Research, University of Washington, Sergey Levine (UC Berkeley), Physical Intelligence, CS25 (série de palestras)

## Claims acionáveis
- Tokenize todas as modalidades em tokens (densos ou discretos) e treine com objetivo autorregressivo unificado para transferir prompting, instrução, planejamento e raciocínio dos LLMs para o multimodal
- Evite discretização VQ-VAE quando entendimento de imagem é prioridade: ela causa perda significativa de informação frente a codificadores contínuos como SigLIP
- Use arquitetura Transfusion (AR no texto + difusão bidirecional na imagem) para gerar imagens de melhor qualidade com muito menos orçamento de tokens
- Adote parâmetros separados por modalidade (MoT) com roteamento determinístico e atenção conjunta para melhorar substancialmente a geração não-textual sem sacrificar desempenho de texto
- Estenda um LLM existente com nova modalidade congelando o texto e treinando apenas o conjunto adicional de parâmetros (treinamento assíncrono), em vez de fine-tuning completo
- Aloque mais experts ao texto do que à imagem: geração de imagem escala mais devagar com o número de experts
- Permita que o modelo gere raciocínio/trilha de pensamento em texto antes de produzir a imagem para obter mais detalhe e menos alucinação
- Planeje usar dois codificadores de imagem (um para entendimento, outro para geração) até que a unificação de representação amadureça
- Não conte com treino de geração de vídeo/imagem para melhorar conhecimento geral ou entendimento — a transferência inversa não foi observada empiricamente
- Prefira alinhar modalidades sobre o texto em vez de renderizar texto como imagem (OCR-ificado), que tende a ser menos eficiente para escalar capacidades de raciocínio
- A derivação de leis de escala multimodais exatas é um problema aberto e oportunidade concreta de pesquisa
- Use modelos de linguagem multimodal como backbone para action prediction em robótica em vez de treinar do zero, aproveitando a transferência positiva do conhecimento de mundo

> **Deep dive:** `medium` — Palestra densa em arquitetura de modelos (Chameleon, Transfusion, MoT, BAGEL) com insights acionáveis de treinamento e escalabilidade, mas recapitula trabalho publicado sobre fundações de modelos e tem aplicação direta limitada a harness, context-engineering, evals ou agent-fleets.
