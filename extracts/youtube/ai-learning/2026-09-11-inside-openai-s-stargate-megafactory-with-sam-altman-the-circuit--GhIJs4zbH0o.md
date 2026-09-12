---
title: "Inside OpenAI's Stargate Megafactory with Sam Altman | The Circuit"
type: "extract"
source: "youtube"
video_id: "GhIJs4zbH0o"
url: "https://www.youtube.com/watch?v=GhIJs4zbH0o"
channel: "Bloomberg Originals"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-inside-openai-s-stargate-megafactory-with-sam-altman-the-circuit--GhIJs4zbH0o.txt]]"
tags: ["agents", "investimentos", "macroeconomia", "instituicoes", "analise"]
thesis: "O Stargate — parceria de US$ 500 bilhões entre OpenAI, SoftBank, Oracle e Crusoe para construir em Abilene, Texas, o que seria um dos maiores clusters de computação do mundo (8 edifícios, até 400 mil GPUs, 1,2 GW) — é apresentado como a maior obra de infraestrutura da história da IA, mas permanece cercado de riscos energéticos, financeiros e geopolíticos."
concepts: ["Stargate / Project Ludicrous (site de Abilene)", "AI factories e clusters massivos de GPUs", "Compute como gargalo da escalada de IA", "Elasticidade da demanda por compute (preço 10x menor → 20x uso → 2x compute)", "Densidade energética de racks (130 kW vs 2–4 kW históricos)", "Resfriamento closed-loop e pegada hídrica", "Corrida global por data centers de IA (EUA vs China)", "Eficiência de modelos (impacto DeepSeek) e risco de overbuilding", "Incentivos fiscais municipais para atrair data centers", "Dependência da cadeia de suprimentos de chips (Taiwan/Coreia/Japão/China)", "AGI e agentes como fase seguinte (2025–2026)", "Energia limpa (vento) como fator locacional"]
tools: ["ChatGPT", "GPT-4", "Nvidia Blackwell (GPUs)", "Oracle Cloud Infrastructure", "Microsoft Azure", "DeepSeek (modelo)"]
people: ["OpenAI", "SoftBank", "Oracle", "Crusoe", "Sam Altman", "Masayoshi Son", "Chase Lochmiller", "Larry Ellison", "Nvidia", "Microsoft", "Meta", "Google", "Amazon", "xAI", "TSMC", "Bloomberg (Brody Ford, Shirin Ghaffary)", "Anja Manuel", "Prefeitura de Abilene", "Donald Trump"]
claims: ["Altman argumenta que mesmo IA 10x mais barata elevaria o uso 20x, exigindo ainda 2x mais compute — maior risco é subinvestir que sobre-investir", "Uma pergunta ao ChatGPT consome ~10x a energia de uma busca no Google; racks modernos orçam 130 kW contra 2–4 kW de duas décadas atrás", "O site de Abilene terá 8 edifícios com até 400 mil GPUs Blackwell (50 mil por edifício, instalados pela Oracle), 1.200 acres e 1,2 GW de capacidade — concluído em meados de 2026", "O resfriamento closed-loop de Crusoe exige ~1 milhão de galões de água uma única vez, eliminando consumo hídrico contínuo", "Data centers podem consumir mais de 8% da eletricidade dos EUA até 2035, com metade atendida por renováveis e o resto majoritariamente carvão e gás", "Abilene abriu mão de 85% da receita de property tax para atrair o projeto, que promete entre ~400 e 1.200 empregos locais", "OpenAI registrou prejuízo de US$ 5 bilhões em 2024 e precisou 'emprestar' compute de pesquisa e desacelerar features durante o pico do gerador de imagens (março)", "O episódio DeepSeek não mudou os planos: Altman diz não haver solução radicalmente mais eficiente, apesar de esperar ganhos anuais de eficiência", "Microsoft pausou ou cancelou vários builds de data centers nos EUA e no exterior, alimentando temores de pullback do setor", "SoftBank comprometeu US$ 100 bilhões com intenção de chegar a US$ 500 bilhões, mas Analistas (Bloomberg) ceticismo sobre atingir a cifra total", "A cadeia de suprimentos de chips é global (fab em Taiwan/Coreia/Japão, montagem na China); tarifas de Trump elevam custos e incerteza da construção", "Recomendação geopolítica: onshoring de fabricação avançada de chips (TSMC/CHIPS Act) e distribuir treino/inferência em países aliados (Islândia, Nórdicos, Japão, Cingapura) com energia geotérmica/limpa", "Crusoe pivota de mineração de Bitcoin em poços de petróleo (gás associado flare) para data centers de IA, explorando a agnósticidade locacional e a demanda energética comum a ambos", "Masa Son reconhece erros passados (WeWork) e sustenta a convicção de que AGI mudará 'a vida da humanidade em todos os aspectos'"]
deep_dive: "low"
deep_dive_reason: "Documentário jornalístico/promocional sobre construção de data centers e apostas financeiras, sem densidade de insight acionável ou arquitetural em harness, context-engineering, evals, agent-fleets, governança ou ontologia de agentes."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-the-entire-ai-data-center-explained-from-electricity-to-chatgpt--ckoi0RTEgcY|The Entire AI Data Center Explained — From Electricity to ChatGPT]]", "[[extracts/youtube/ai-learning/2026-09-11-building-the-real-world-infrastructure-for-ai-with-google-cisco-a16z--OsLRf6r5U9E|Building the Real-World Infrastructure for AI, with Google, Cisco & a16z]]", "[[extracts/youtube/ai-learning/2026-09-11-stanford-cs153-frontier-systems-scale-agi-and-the-future-of-everything--F_7M4Hc-usM|Stanford CS153 Frontier Systems | Scale, AGI, and the Future of Everything]]", "[[extracts/youtube/ai-learning/2026-09-11-gpus-tpus-the-economics-of-ai-explained-gavin-baker-interview--cmUo4841KQw|GPUs, TPUs, & The Economics of AI Explained | Gavin Baker Interview]]", "[[extracts/youtube/ai-learning/2026-09-11-stanford-cs153-frontier-systems-anjney-midha-from-amp-pbc-on-frontier-systems--O5PfU_uDhS0|Stanford CS153 Frontier Systems | Anjney Midha from AMP PBC on Frontier Systems]]", "[[extracts/youtube/ai-learning/2026-09-11-stanford-ms-e435-economics-of-the-ai-supercycle-spring-2026-infrasctructure-ente--sRvrXL83N-c|Stanford MS&E435 Economics of the AI Supercycle | Spring 2026 | Infrasctructure, Enterprise AI, SaaS]]"]
theme: "Estratégias corporativas de agentes"
---

# Inside OpenAI's Stargate Megafactory with Sam Altman | The Circuit

## Tese
O Stargate — parceria de US$ 500 bilhões entre OpenAI, SoftBank, Oracle e Crusoe para construir em Abilene, Texas, o que seria um dos maiores clusters de computação do mundo (8 edifícios, até 400 mil GPUs, 1,2 GW) — é apresentado como a maior obra de infraestrutura da história da IA, mas permanece cercado de riscos energéticos, financeiros e geopolíticos.

## Conceitos-chave
- Stargate / Project Ludicrous (site de Abilene)
- AI factories e clusters massivos de GPUs
- Compute como gargalo da escalada de IA
- Elasticidade da demanda por compute (preço 10x menor → 20x uso → 2x compute)
- Densidade energética de racks (130 kW vs 2–4 kW históricos)
- Resfriamento closed-loop e pegada hídrica
- Corrida global por data centers de IA (EUA vs China)
- Eficiência de modelos (impacto DeepSeek) e risco de overbuilding
- Incentivos fiscais municipais para atrair data centers
- Dependência da cadeia de suprimentos de chips (Taiwan/Coreia/Japão/China)
- AGI e agentes como fase seguinte (2025–2026)
- Energia limpa (vento) como fator locacional

## Ferramentas & pessoas
**Ferramentas:** ChatGPT, GPT-4, Nvidia Blackwell (GPUs), Oracle Cloud Infrastructure, Microsoft Azure, DeepSeek (modelo)

**Pessoas/orgs:** OpenAI, SoftBank, Oracle, Crusoe, Sam Altman, Masayoshi Son, Chase Lochmiller, Larry Ellison, Nvidia, Microsoft, Meta, Google, Amazon, xAI, TSMC, Bloomberg (Brody Ford, Shirin Ghaffary), Anja Manuel, Prefeitura de Abilene, Donald Trump

## Claims acionáveis
- Altman argumenta que mesmo IA 10x mais barata elevaria o uso 20x, exigindo ainda 2x mais compute — maior risco é subinvestir que sobre-investir
- Uma pergunta ao ChatGPT consome ~10x a energia de uma busca no Google; racks modernos orçam 130 kW contra 2–4 kW de duas décadas atrás
- O site de Abilene terá 8 edifícios com até 400 mil GPUs Blackwell (50 mil por edifício, instalados pela Oracle), 1.200 acres e 1,2 GW de capacidade — concluído em meados de 2026
- O resfriamento closed-loop de Crusoe exige ~1 milhão de galões de água uma única vez, eliminando consumo hídrico contínuo
- Data centers podem consumir mais de 8% da eletricidade dos EUA até 2035, com metade atendida por renováveis e o resto majoritariamente carvão e gás
- Abilene abriu mão de 85% da receita de property tax para atrair o projeto, que promete entre ~400 e 1.200 empregos locais
- OpenAI registrou prejuízo de US$ 5 bilhões em 2024 e precisou 'emprestar' compute de pesquisa e desacelerar features durante o pico do gerador de imagens (março)
- O episódio DeepSeek não mudou os planos: Altman diz não haver solução radicalmente mais eficiente, apesar de esperar ganhos anuais de eficiência
- Microsoft pausou ou cancelou vários builds de data centers nos EUA e no exterior, alimentando temores de pullback do setor
- SoftBank comprometeu US$ 100 bilhões com intenção de chegar a US$ 500 bilhões, mas Analistas (Bloomberg) ceticismo sobre atingir a cifra total
- A cadeia de suprimentos de chips é global (fab em Taiwan/Coreia/Japão, montagem na China); tarifas de Trump elevam custos e incerteza da construção
- Recomendação geopolítica: onshoring de fabricação avançada de chips (TSMC/CHIPS Act) e distribuir treino/inferência em países aliados (Islândia, Nórdicos, Japão, Cingapura) com energia geotérmica/limpa
- Crusoe pivota de mineração de Bitcoin em poços de petróleo (gás associado flare) para data centers de IA, explorando a agnósticidade locacional e a demanda energética comum a ambos
- Masa Son reconhece erros passados (WeWork) e sustenta a convicção de que AGI mudará 'a vida da humanidade em todos os aspectos'

> **Deep dive:** `low` — Documentário jornalístico/promocional sobre construção de data centers e apostas financeiras, sem densidade de insight acionável ou arquitetural em harness, context-engineering, evals, agent-fleets, governança ou ontologia de agentes.
