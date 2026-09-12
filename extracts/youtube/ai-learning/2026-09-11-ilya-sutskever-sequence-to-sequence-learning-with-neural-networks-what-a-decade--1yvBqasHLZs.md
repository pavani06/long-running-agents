---
title: "Ilya Sutskever: \"Sequence to sequence learning with neural networks: what a decade\""
type: "extract"
source: "youtube"
video_id: "1yvBqasHLZs"
url: "https://www.youtube.com/watch?v=1yvBqasHLZs"
channel: "seremot"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-ilya-sutskever-sequence-to-sequence-learning-with-neural-networks-what-a-decade--1yvBqasHLZs.txt]]"
tags: ["analise", "agents", "roadmap", "governanca"]
thesis: "Em sua retrospectiva de 10 anos no NeurIPS 2024, Ilya Sutskever argumenta que o conexionismo e a hipótese de scaling impulsionaram a era do pré-treinamento, que inevitablymente terminará por falta de novos dados ('o dado é o combustível fóssil da IA'), sendo sucedida por agentes, dados sintéticos e inference-time compute, culminando em uma superinteligência qualitativamente diferente e intrinsecamente imprevisível."
concepts: ["conexionismo", "hipótese de scaling", "era do pré-treinamento", "modelos autorregressivos", "LSTM (ResNet rotacionada 90°)", "hipótese do deep learning (tarefas humanas em fração de segundo)", "peak data / dados como combustível fóssil", "dados sintéticos", "inference-time compute", "agentes", "imprevisibilidade do raciocínio", "superinteligência", "self-awareness em sistemas de IA", "correlação cérebro-corpo em hominídeos (expoente de scaling diferente)", "generalização out-of-distribution e elevação dos padrões de avaliação", "autocorreção de alucinações via raciocínio", "GPU pipelining (uma camada por GPU)"]
tools: ["LSTM", "GPT-2", "GPT-3", "o1 (OpenAI)", "Bittensor", "Microsoft Word (analogia de autocorrect)"]
people: ["Ilya Sutskever", "Oriol Vinyals", "Quoc Le", "Alec Radford", "Jared Kaplan", "Dario Amodei", "NeurIPS", "Universidade de Toronto"]
claims: ["O pré-treinamento como o conhecemos terminará porque o compute cresce com hardware e algoritmos, mas os dados não — há apenas uma internet e já atingimos o peak data.", "A hipótese de scaling (grande dataset + grande rede neural = sucesso garantido), formulada em 2014, tem sido o motor de todo o progresso atual.", "As três direções pós-pré-treinamento são agentes, dados sintéticos e inference-time compute, como visto no modelo o1.", "Hominídeos exibem um expoente de scaling cérebro-corpo diferente de outros mamíferos, provando que biologia já encontrou um regime de scaling qualitativamente distinto — precedente de que o scaling em IA também pode mudar.", "Quanto mais um sistema raciocina, mais imprevisível ele se torna, análogo a como AIs de xadrez são imprevisíveis para os melhores humanos.", "Sistemas superinteligentes futuros serão genuinamente agênticos, aprenderão de dados limitados e plausivelmente terão self-awareness, sendo qualitativamente diferentes dos modelos atuais.", "Modelos com raciocínio provavelmente conseguirão autocorrigir as próprias alucinações, reduzindo sua frequência.", "Os padrões do que conta como generalização subiram dramaticamente; LLMs generalizam out-of-distribution em algum grau, mas pior que humanos.", "A inspiração biológica no deep learning foi modesta (apenas 'usar neurônios'); insights biológicos mais profundos permanecem possíveis para quem tiver uma percepção especial.", "Pipelining com uma camada por GPU não foi uma decisão sábia de engenharia (rendeu 3.5x em 8 GPUs, mas não é a abordagem correta).", "Uma rede de 10 camadas pode, em princípio, fazer qualquer coisa que algum humano faça em uma fração de segundo — fundamento do deep learning hypothesis original."]
deep_dive: "medium"
deep_dive_reason: "Retrospectiva conceitual com previsões de alto impacto (fim do pré-treinamento, peak data, imprevisibilidade crescente com raciocínio), mas sem densidade de insight arquitetural ou prático acionável em harness, evals, context-engineering ou engenharia de agentes."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-ilya-sutskever-we-re-moving-from-the-age-of-scaling-to-the-age-of-research--aR20FWCCjAs|Ilya Sutskever – We're moving from the age of scaling to the age of research]]", "[[extracts/youtube/ai-learning/2026-09-11-yann-lecun-on-what-comes-after-llms--ngBraLDqzdI|Yann LeCun on What Comes After LLMs]]", "[[extracts/youtube/ai-learning/2026-09-11-jeff-dean-the-1-rule-for-building-in-ai--CxXgV54KzpQ|Jeff Dean: The 1% Rule for Building in AI]]", "[[extracts/youtube/ai-learning/2026-09-11-stanford-cs153-frontier-systems-scale-agi-and-the-future-of-everything--F_7M4Hc-usM|Stanford CS153 Frontier Systems | Scale, AGI, and the Future of Everything]]", "[[extracts/youtube/ai-learning/2026-09-11-stanford-cs153-frontier-systems-anjney-midha-from-amp-pbc-on-frontier-systems--O5PfU_uDhS0|Stanford CS153 Frontier Systems | Anjney Midha from AMP PBC on Frontier Systems]]", "[[extracts/youtube/ai-learning/2026-09-11-yann-lecun-s-1b-bet-against-llms-part-1--kYkIdXwW2AE|Yann LeCun's $1B Bet Against LLMs [Part 1]]]"]
theme: "Estratégias corporativas de agentes"
---

# Ilya Sutskever: "Sequence to sequence learning with neural networks: what a decade"

## Tese
Em sua retrospectiva de 10 anos no NeurIPS 2024, Ilya Sutskever argumenta que o conexionismo e a hipótese de scaling impulsionaram a era do pré-treinamento, que inevitablymente terminará por falta de novos dados ('o dado é o combustível fóssil da IA'), sendo sucedida por agentes, dados sintéticos e inference-time compute, culminando em uma superinteligência qualitativamente diferente e intrinsecamente imprevisível.

## Conceitos-chave
- conexionismo
- hipótese de scaling
- era do pré-treinamento
- modelos autorregressivos
- LSTM (ResNet rotacionada 90°)
- hipótese do deep learning (tarefas humanas em fração de segundo)
- peak data / dados como combustível fóssil
- dados sintéticos
- inference-time compute
- agentes
- imprevisibilidade do raciocínio
- superinteligência
- self-awareness em sistemas de IA
- correlação cérebro-corpo em hominídeos (expoente de scaling diferente)
- generalização out-of-distribution e elevação dos padrões de avaliação
- autocorreção de alucinações via raciocínio
- GPU pipelining (uma camada por GPU)

## Ferramentas & pessoas
**Ferramentas:** LSTM, GPT-2, GPT-3, o1 (OpenAI), Bittensor, Microsoft Word (analogia de autocorrect)

**Pessoas/orgs:** Ilya Sutskever, Oriol Vinyals, Quoc Le, Alec Radford, Jared Kaplan, Dario Amodei, NeurIPS, Universidade de Toronto

## Claims acionáveis
- O pré-treinamento como o conhecemos terminará porque o compute cresce com hardware e algoritmos, mas os dados não — há apenas uma internet e já atingimos o peak data.
- A hipótese de scaling (grande dataset + grande rede neural = sucesso garantido), formulada em 2014, tem sido o motor de todo o progresso atual.
- As três direções pós-pré-treinamento são agentes, dados sintéticos e inference-time compute, como visto no modelo o1.
- Hominídeos exibem um expoente de scaling cérebro-corpo diferente de outros mamíferos, provando que biologia já encontrou um regime de scaling qualitativamente distinto — precedente de que o scaling em IA também pode mudar.
- Quanto mais um sistema raciocina, mais imprevisível ele se torna, análogo a como AIs de xadrez são imprevisíveis para os melhores humanos.
- Sistemas superinteligentes futuros serão genuinamente agênticos, aprenderão de dados limitados e plausivelmente terão self-awareness, sendo qualitativamente diferentes dos modelos atuais.
- Modelos com raciocínio provavelmente conseguirão autocorrigir as próprias alucinações, reduzindo sua frequência.
- Os padrões do que conta como generalização subiram dramaticamente; LLMs generalizam out-of-distribution em algum grau, mas pior que humanos.
- A inspiração biológica no deep learning foi modesta (apenas 'usar neurônios'); insights biológicos mais profundos permanecem possíveis para quem tiver uma percepção especial.
- Pipelining com uma camada por GPU não foi uma decisão sábia de engenharia (rendeu 3.5x em 8 GPUs, mas não é a abordagem correta).
- Uma rede de 10 camadas pode, em princípio, fazer qualquer coisa que algum humano faça em uma fração de segundo — fundamento do deep learning hypothesis original.

> **Deep dive:** `medium` — Retrospectiva conceitual com previsões de alto impacto (fim do pré-treinamento, peak data, imprevisibilidade crescente com raciocínio), mas sem densidade de insight arquitetural ou prático acionável em harness, evals, context-engineering ou engenharia de agentes.
