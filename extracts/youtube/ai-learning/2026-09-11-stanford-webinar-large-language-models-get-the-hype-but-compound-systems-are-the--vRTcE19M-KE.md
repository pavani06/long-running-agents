---
title: "Stanford Webinar - Large Language Models Get the Hype, but Compound Systems Are the Future of AI"
type: "extract"
source: "youtube"
video_id: "vRTcE19M-KE"
url: "https://www.youtube.com/watch?v=vRTcE19M-KE"
channel: "Stanford Online"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-stanford-webinar-large-language-models-get-the-hype-but-compound-systems-are-the--vRTcE19M-KE.txt]]"
tags: ["arquitetura", "context-engineering", "evals", "model-selection", "governanca", "frameworks", "agent-tooling", "multi-agent", "agents", "analise"]
thesis: "O presente e o futuro da IA são sistemas compostos (prompt + modelo + método de amostragem + ferramentas), não modelos isolados — logo, engenharia, avaliação e regulação devem ser orientadas a sistemas completos."
concepts: ["sistemas de IA compostos (compound AI systems)", "sistema mínimo: prompt + modelo + método de amostragem", "amostragem para geração (decodificação gulosa, top-p, beam search, diversidade de tokens, gramáticas/JSON válido, temperatura adaptativa)", "majority completion / múltiplos caminhos de raciocínio com voto majoritário", "in-context learning (origens em GPT-2 e GPT-3)", "sensibilidade dos modelos à formatação do prompt (diferenças de até 80 pontos por dois-pontos)", "prompt como 'binário compilado' acoplado ao modelo específico", "lições clássicas de IA: design modular, otimização orientada a dados, arquiteturas genéricas", "programação de modelos de linguagem vs. prompt engineering (DSPy)", "bootstrapped few-shot optimization de instruções e demonstrações", "modelos pequenos em sistemas inteligentes vs. modelos grandes em sistemas simples", "trade-offs de latência e custo (18ms vs. 750ms)", "eras de escala: treino não supervisionado, instruct fine-tuning, compute de inferência, escala de sistemas", "regulação de sistemas vs. regulação por tamanho de modelo (SB-1047)", "leaderboards deveriam avaliar sistemas, não modelos", "guardrails: identificação como não-humano e restrições de login/redes sociais", "ReAct e agentes como ponte para uso de ferramentas"]
tools: ["DSPy", "PyTorch", "Torch", "Theano", "Chainer", "GPT-2", "GPT-3", "GPT-4", "GPT-4o", "GPT-4o mini", "o1 (mencionado como '4o1')", "Llama 2-7b", "Llama2-13b", "code-davinci-002", "Turbo (GPT-3.5-turbo)", "PaLM", "Gemini", "ChatGPT", "Apple Intelligence", "Google Search", "Hugging Face leaderboard", "Chatbot Arena", "HELM", "EchoPrompt (artigo)"]
people: ["Christopher Potts", "Petra Parikova", "UC Berkeley", "University of Washington (U-dub)", "OpenAI", "Sam Altman", "Google", "Gavin Newsom", "Stanford", "Theory Ventures", "Hugging Face", "Apple", "Radford et al."]
claims: ["Avalie sempre pares modelo+prompt (e a estratégia de amostragem), nunca o modelo isolado — diferenças triviais de formatação do prompt podem alterar a performance em até 80 pontos", "Um modelo pequeno embutido em um sistema inteligente supera um modelo grande em um sistema simplista, mesmo em acurácia bruta e sobretudo em custo, latência, segurança e privacidade", "Ao trocar de modelo (ex.: GPT-4 para 4o), conte com uma nova rodada completa de engenharia de prompt: prompts são acoplados ao modelo como binários compilados", "Prefira otimização orientada a dados (ex.: bootstrapped few-shot no DSPy) a prompts escritos à mão — prompts bootstrapados superaram chain-of-thought escrito por humanos nos experimentos citados", "77% do uso corporativo de modelos ocorre em escala ≤13B de parâmetros; latências ~18ms são confortáveis, acima de ~50ms (até 750ms) geram custos e dores operacionais", "Amostragem é decisão de design altamente consequente: escolha conscientemente entre decodificação gulosa, top-p, beam search, restrições gramaticais/JSON, temperatura adaptativa e estratégias de maioria sobre múltiplos caminhos de raciocínio", "Regulação deve incidir sobre sistemas inteiros, não sobre limiares de tamanho/custo de treinamento — o veto de Newsom à SB-1047 reconheceu que sistemas com modelos pequenos podem ser tão ou mais perigosos", "Reoriente benchmarks/leaderboards para avaliar sistemas completos (prompt+modelo+amostragem+ferramentas), não artefatos de modelo isolados", "Guardrails propostos: exigir que sistemas de IA se identifiquem como não-humanos e restringir capacidades de login em sites e atuação livre em redes sociais", "Predição: a próxima era transformadora de escala será 'scaling de sistemas' — dar a bons modelos (inclusive pequenos) acesso produtivo a muitas ferramentas coordenadas"]
deep_dive: "high"
deep_dive_reason: "Densa em insights acionáveis e arquiteturais sobre context-engineering (acoplamento prompt-modelo), evals (avaliar sistemas, não modelos), model-selection e governança, com dados concretos e o argumento central da tese de sistemas compostos."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-stanford-cs153-frontier-systems-anjney-midha-from-amp-pbc-on-frontier-systems--O5PfU_uDhS0|Stanford CS153 Frontier Systems | Anjney Midha from AMP PBC on Frontier Systems]]", "[[extracts/youtube/ai-learning/2026-09-11-stanford-cs153-frontier-systems-scale-agi-and-the-future-of-everything--F_7M4Hc-usM|Stanford CS153 Frontier Systems | Scale, AGI, and the Future of Everything]]", "[[extracts/youtube/ai-learning/2026-09-11-stanford-cs153-frontier-systems-amit-jain-from-luma-ai-on-unified-intelligence-s--6nUl_w5W9Wk|Stanford CS153 Frontier Systems | Amit Jain from Luma AI on Unified Intelligence Systems]]", "[[extracts/youtube/ai-learning/2026-09-11-jeff-dean-the-1-rule-for-building-in-ai--CxXgV54KzpQ|Jeff Dean: The 1% Rule for Building in AI]]", "[[extracts/youtube/ai-learning/2026-09-11-stanford-cs153-frontier-systems-mati-staniszewski-from-elevenlabs-on-the-future--vfF011ko89o|Stanford CS153 Frontier Systems | Mati Staniszewski from ElevenLabs on The Future of Voice Systems]]", "[[extracts/youtube/ai-learning/2026-09-11-how-to-understand-the-next-wave-of-ai-before-everyone-else-tibo-interview--4qjEgPojjzM|How to Understand the Next Wave of AI Before Everyone Else | Tibo Interview]]", "[[extracts/youtube/ai-learning/2026-09-11-stanford-cs25-transformers-united-v6-i-from-language-models-to-native-multimodal--NDdc39KYqDU|Stanford CS25: Transformers United V6 I From Language Models to Native Multimodal Intelligence]]", "[[extracts/youtube/ai-learning/2026-09-11-stanford-robotics-seminar-engr319-spring-2026-integrated-learning-and-planning--3W36pd50Wqw|Stanford Robotics Seminar ENGR319 | Spring 2026 | Integrated Learning and Planning]]", "[[extracts/youtube/ai-learning/2026-09-11-stanford-cs230-autumn-2025-lecture-1-introduction-to-deep-learning--_NLHFoVNlbg|Stanford CS230 | Autumn 2025 | Lecture 1: Introduction to Deep Learning]]", "[[extracts/youtube/ai-learning/2026-09-11-foundation-ai-a-especializacao-dos-modelos-dicionario-do-programador--AKoBE4gKaXQ|Foundation AI (A Especialização dos Modelos) // Dicionário do Programador]]", "[[extracts/youtube/ai-learning/2026-09-11-stanford-cs336-language-modeling-from-scratch-spring-2026-lecture-13-data-source---qm0ln33G24|Stanford CS336 Language Modeling from Scratch | Spring 2026 | Lecture 13: Data (Sources, Datasets)]]"]
---

# Stanford Webinar - Large Language Models Get the Hype, but Compound Systems Are the Future of AI

## Tese
O presente e o futuro da IA são sistemas compostos (prompt + modelo + método de amostragem + ferramentas), não modelos isolados — logo, engenharia, avaliação e regulação devem ser orientadas a sistemas completos.

## Conceitos-chave
- sistemas de IA compostos (compound AI systems)
- sistema mínimo: prompt + modelo + método de amostragem
- amostragem para geração (decodificação gulosa, top-p, beam search, diversidade de tokens, gramáticas/JSON válido, temperatura adaptativa)
- majority completion / múltiplos caminhos de raciocínio com voto majoritário
- in-context learning (origens em GPT-2 e GPT-3)
- sensibilidade dos modelos à formatação do prompt (diferenças de até 80 pontos por dois-pontos)
- prompt como 'binário compilado' acoplado ao modelo específico
- lições clássicas de IA: design modular, otimização orientada a dados, arquiteturas genéricas
- programação de modelos de linguagem vs. prompt engineering (DSPy)
- bootstrapped few-shot optimization de instruções e demonstrações
- modelos pequenos em sistemas inteligentes vs. modelos grandes em sistemas simples
- trade-offs de latência e custo (18ms vs. 750ms)
- eras de escala: treino não supervisionado, instruct fine-tuning, compute de inferência, escala de sistemas
- regulação de sistemas vs. regulação por tamanho de modelo (SB-1047)
- leaderboards deveriam avaliar sistemas, não modelos
- guardrails: identificação como não-humano e restrições de login/redes sociais
- ReAct e agentes como ponte para uso de ferramentas

## Ferramentas & pessoas
**Ferramentas:** DSPy, PyTorch, Torch, Theano, Chainer, GPT-2, GPT-3, GPT-4, GPT-4o, GPT-4o mini, o1 (mencionado como '4o1'), Llama 2-7b, Llama2-13b, code-davinci-002, Turbo (GPT-3.5-turbo), PaLM, Gemini, ChatGPT, Apple Intelligence, Google Search, Hugging Face leaderboard, Chatbot Arena, HELM, EchoPrompt (artigo)

**Pessoas/orgs:** Christopher Potts, Petra Parikova, UC Berkeley, University of Washington (U-dub), OpenAI, Sam Altman, Google, Gavin Newsom, Stanford, Theory Ventures, Hugging Face, Apple, Radford et al.

## Claims acionáveis
- Avalie sempre pares modelo+prompt (e a estratégia de amostragem), nunca o modelo isolado — diferenças triviais de formatação do prompt podem alterar a performance em até 80 pontos
- Um modelo pequeno embutido em um sistema inteligente supera um modelo grande em um sistema simplista, mesmo em acurácia bruta e sobretudo em custo, latência, segurança e privacidade
- Ao trocar de modelo (ex.: GPT-4 para 4o), conte com uma nova rodada completa de engenharia de prompt: prompts são acoplados ao modelo como binários compilados
- Prefira otimização orientada a dados (ex.: bootstrapped few-shot no DSPy) a prompts escritos à mão — prompts bootstrapados superaram chain-of-thought escrito por humanos nos experimentos citados
- 77% do uso corporativo de modelos ocorre em escala ≤13B de parâmetros; latências ~18ms são confortáveis, acima de ~50ms (até 750ms) geram custos e dores operacionais
- Amostragem é decisão de design altamente consequente: escolha conscientemente entre decodificação gulosa, top-p, beam search, restrições gramaticais/JSON, temperatura adaptativa e estratégias de maioria sobre múltiplos caminhos de raciocínio
- Regulação deve incidir sobre sistemas inteiros, não sobre limiares de tamanho/custo de treinamento — o veto de Newsom à SB-1047 reconheceu que sistemas com modelos pequenos podem ser tão ou mais perigosos
- Reoriente benchmarks/leaderboards para avaliar sistemas completos (prompt+modelo+amostragem+ferramentas), não artefatos de modelo isolados
- Guardrails propostos: exigir que sistemas de IA se identifiquem como não-humanos e restringir capacidades de login em sites e atuação livre em redes sociais
- Predição: a próxima era transformadora de escala será 'scaling de sistemas' — dar a bons modelos (inclusive pequenos) acesso produtivo a muitas ferramentas coordenadas

> **Deep dive:** `high` — Densa em insights acionáveis e arquiteturais sobre context-engineering (acoplamento prompt-modelo), evals (avaliar sistemas, não modelos), model-selection e governança, com dados concretos e o argumento central da tese de sistemas compostos.
