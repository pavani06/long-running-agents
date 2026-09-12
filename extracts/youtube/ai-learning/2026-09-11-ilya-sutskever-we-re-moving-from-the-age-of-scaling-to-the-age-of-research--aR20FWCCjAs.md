---
title: "Ilya Sutskever – We're moving from the age of scaling to the age of research"
type: "extract"
source: "youtube"
video_id: "aR20FWCCjAs"
url: "https://www.youtube.com/watch?v=aR20FWCCjAs"
channel: "Dwarkesh Patel"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-ilya-sutskever-we-re-moving-from-the-age-of-scaling-to-the-age-of-research--aR20FWCCjAs.txt]]"
tags: ["analise", "evals", "governanca", "investimentos", "macroeconomia", "instituicoes", "roadmap"]
thesis: "Ilya Sutskever argumenta que os modelos generalizam dramaticamente pior que humanos, que a desconexão entre evals e impacto real decorre de ambientes de RL derivados dos próprios evals, e que o campo saiu da era do scaling e voltou a uma era de pesquisa focada em continual learning, value functions e alinhamento."
concepts: ["desconexão entre desempenho em evals e impacto econômico real", "ambientes de RL inspirados em evals (reward hacking por pesquisadores)", "generalização limitada e analogia dos dois estudantes (10.000h vs 100h com 'it')", "pre-training (treinar em tudo) vs RL (escolher ambientes específicos)", "value function como sinal de recompensa intermediário no RL", "emoções como value function humano hardcoded pela evolução", "eras do ML: pesquisa (2012-2020), scaling (2020-2025), retorno à pesquisa com grande compute", "sample efficiency e robustez superiores dos humanos", "continual learning e aprendizado no trabalho ('superinteligente de 15 anos')", "straight shot superintelligence vs release gradual", "'communicate the AI' vs comunicar a ideia de IA", "fusão de aprendizados entre instâncias de um modelo (merge de mentes)", "alinhamento com vida senciente vs vida humana apenas", "capping do poder da superinteligência", "how language shapes thought (termos como 'AGI' e 'scaling')"]
tools: ["o1", "DeepSeek R1", "GPT-3", "AlexNet", "Transformer", "ResNet", "Gemini", "Linux"]
people: ["Ilya Sutskever", "SSI (Safe Superintelligence)", "OpenAI", "Anthropic", "Google", "Stanford", "DeepSeek", "Yann LeCun", "Garry Kasparov"]
claims: ["Ambientes de RL derivados de evals explicam parte da desconexão entre pontuação em evals e desempenho real; avalie se há vazamento entre treino e teste", "Empilhar mais diversidade de ambientes de RL não resolve a generalização sozinha; é preciso transferir aprendizado de um domínio para outro", "Value functions tornam RL mais eficiente ao fornecer recompensa intermediária antes do fim do episódio, mas tudo que se faz com elas pode ser feito sem, apenas mais devagar", "Ideias de pesquisa de fronteira historicamente não exigiram compute máximo: AlexNet usou 2 GPUs e o Transformer 8-64 GPUs", "Grande parte do financiamento dos grandes labs é alocada a inference e produtos, reduzindo a vantagem real de compute dedicado a pesquisa", "Deploy incremental e antecipado de IA é necessário porque é impossível 'sentir' a AGI sem vê-la em operação", "Superintelligença deveria ser definida como capacidade de aprender qualquer trabalho (continual learning), não um sistema acabado que já sabe tudo", "Previsões: concorrentes passarão a colaborar em segurança de IA, empresas ficarão mais cautelosas quando a IA parecer poderosa, e governos/público agirão quando o poder ficar visível", "Limitar (capping) o poder da superintelligença mais poderosa seria materialmente útil para segurança", "Alinhar IA à vida senciente pode ser mais fácil do que à vida humana apenas, pois a própria IA será senciente e em número trilionesimal", "Superhuman em competições de código não implica melhor gosto/juízo sobre codebases reais; segurar dois bugs alternados em vibe coding evidencia falha estranha do RL atual"]
deep_dive: "medium"
deep_dive_reason: "Há insights conceituais relevantes sobre evals, generalização, value functions e governança de superinteligência, mas o conteúdo é majoritariamente conversacional e especulativo, sem densidade arquitetural implementável para harness de agentes."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-ilya-sutskever-sequence-to-sequence-learning-with-neural-networks-what-a-decade--1yvBqasHLZs|Ilya Sutskever: \"Sequence to sequence learning with neural networks: what a decade\"]]", "[[extracts/youtube/ai-learning/2026-09-11-stanford-cs153-frontier-systems-scale-agi-and-the-future-of-everything--F_7M4Hc-usM|Stanford CS153 Frontier Systems | Scale, AGI, and the Future of Everything]]", "[[extracts/youtube/ai-learning/2026-09-11-yann-lecun-on-what-comes-after-llms--ngBraLDqzdI|Yann LeCun on What Comes After LLMs]]", "[[extracts/youtube/ai-learning/2026-09-11-stanford-cs153-frontier-systems-anjney-midha-from-amp-pbc-on-frontier-systems--O5PfU_uDhS0|Stanford CS153 Frontier Systems | Anjney Midha from AMP PBC on Frontier Systems]]", "[[extracts/youtube/ai-learning/2026-09-11-how-to-understand-the-next-wave-of-ai-before-everyone-else-tibo-interview--4qjEgPojjzM|How to Understand the Next Wave of AI Before Everyone Else | Tibo Interview]]", "[[extracts/youtube/ai-learning/2026-09-11-jeff-dean-the-1-rule-for-building-in-ai--CxXgV54KzpQ|Jeff Dean: The 1% Rule for Building in AI]]", "[[extracts/youtube/ai-learning/2026-09-11-stanford-ai-club-jason-wei-on-3-key-ideas-in-ai-in-2025--b6Doq2fz81U|Stanford AI Club: Jason Wei on 3 Key Ideas in AI in 2025]]", "[[extracts/youtube/ai-learning/2026-09-11-yann-lecun-s-1b-bet-against-llms-part-1--kYkIdXwW2AE|Yann LeCun's $1B Bet Against LLMs [Part 1]]]", "[[extracts/youtube/ai-learning/2026-09-11-the-thinking-game-full-documentary-tribeca-film-festival-official-selection--d95J8yzvjbQ|The Thinking Game | Full documentary | Tribeca Film Festival official selection]]", "[[extracts/youtube/ai-learning/2026-09-11-did-openai-just-solve-hallucinations--xGO5Q94XXf0|Did OpenAI just solve hallucinations?]]"]
---

# Ilya Sutskever – We're moving from the age of scaling to the age of research

## Tese
Ilya Sutskever argumenta que os modelos generalizam dramaticamente pior que humanos, que a desconexão entre evals e impacto real decorre de ambientes de RL derivados dos próprios evals, e que o campo saiu da era do scaling e voltou a uma era de pesquisa focada em continual learning, value functions e alinhamento.

## Conceitos-chave
- desconexão entre desempenho em evals e impacto econômico real
- ambientes de RL inspirados em evals (reward hacking por pesquisadores)
- generalização limitada e analogia dos dois estudantes (10.000h vs 100h com 'it')
- pre-training (treinar em tudo) vs RL (escolher ambientes específicos)
- value function como sinal de recompensa intermediário no RL
- emoções como value function humano hardcoded pela evolução
- eras do ML: pesquisa (2012-2020), scaling (2020-2025), retorno à pesquisa com grande compute
- sample efficiency e robustez superiores dos humanos
- continual learning e aprendizado no trabalho ('superinteligente de 15 anos')
- straight shot superintelligence vs release gradual
- 'communicate the AI' vs comunicar a ideia de IA
- fusão de aprendizados entre instâncias de um modelo (merge de mentes)
- alinhamento com vida senciente vs vida humana apenas
- capping do poder da superinteligência
- how language shapes thought (termos como 'AGI' e 'scaling')

## Ferramentas & pessoas
**Ferramentas:** o1, DeepSeek R1, GPT-3, AlexNet, Transformer, ResNet, Gemini, Linux

**Pessoas/orgs:** Ilya Sutskever, SSI (Safe Superintelligence), OpenAI, Anthropic, Google, Stanford, DeepSeek, Yann LeCun, Garry Kasparov

## Claims acionáveis
- Ambientes de RL derivados de evals explicam parte da desconexão entre pontuação em evals e desempenho real; avalie se há vazamento entre treino e teste
- Empilhar mais diversidade de ambientes de RL não resolve a generalização sozinha; é preciso transferir aprendizado de um domínio para outro
- Value functions tornam RL mais eficiente ao fornecer recompensa intermediária antes do fim do episódio, mas tudo que se faz com elas pode ser feito sem, apenas mais devagar
- Ideias de pesquisa de fronteira historicamente não exigiram compute máximo: AlexNet usou 2 GPUs e o Transformer 8-64 GPUs
- Grande parte do financiamento dos grandes labs é alocada a inference e produtos, reduzindo a vantagem real de compute dedicado a pesquisa
- Deploy incremental e antecipado de IA é necessário porque é impossível 'sentir' a AGI sem vê-la em operação
- Superintelligença deveria ser definida como capacidade de aprender qualquer trabalho (continual learning), não um sistema acabado que já sabe tudo
- Previsões: concorrentes passarão a colaborar em segurança de IA, empresas ficarão mais cautelosas quando a IA parecer poderosa, e governos/público agirão quando o poder ficar visível
- Limitar (capping) o poder da superintelligença mais poderosa seria materialmente útil para segurança
- Alinhar IA à vida senciente pode ser mais fácil do que à vida humana apenas, pois a própria IA será senciente e em número trilionesimal
- Superhuman em competições de código não implica melhor gosto/juízo sobre codebases reais; segurar dois bugs alternados em vibe coding evidencia falha estranha do RL atual

> **Deep dive:** `medium` — Há insights conceituais relevantes sobre evals, generalização, value functions e governança de superinteligência, mas o conteúdo é majoritariamente conversacional e especulativo, sem densidade arquitetural implementável para harness de agentes.
