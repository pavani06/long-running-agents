---
title: "GPUs, TPUs, & The Economics of AI Explained | Gavin Baker Interview"
type: "extract"
source: "youtube"
video_id: "cmUo4841KQw"
url: "https://www.youtube.com/watch?v=cmUo4841KQw"
channel: "Invest Like The Best"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-gpus-tpus-the-economics-of-ai-explained-gavin-baker-interview--cmUo4841KQw.txt]]"
tags: ["investimentos", "model-selection", "verification", "context-engineering", "evals", "stack-tooling", "agents", "analise", "monitoramento"]
thesis: "Gavin Baker argumenta que o Gemini 3 confirmou que as leis de scaling de pré-treinamento continuam válidas, que o reasoning (RLVR + test-time compute) bridou o hiato de compute até Blackwell e ativou um flywheel de dados nos labs de fronteira, e que a economia de custo por token reorganizará a vantagem competitiva (Google, Nvidia, xAI, ASICs) em 2026."
concepts: ["Leis de scaling de pré-treinamento como observação empírica precisa mas teoricamente inexplicada (analogia aos egípcios e o Sol)", "RLVR: reinforcement learning com recompensas verificáveis — 'com IA, tudo que você pode verificar, você pode automatizar'", "Test-time compute como segunda nova lei de scaling, multiplicativa com pré-treino e RLVR", "Coerência de cluster (~200k GPUs Hopper como limite prático) como gargalo de pré-treinamento", "Flywheel de dados (produto→usuários→dados→melhor produto) agora começando a girar nos labs de fronteira via reasoning", "Checkpoints internos mais avançados usados para treinar o próximo modelo — defasagem composta para quem não os tem", "Produção de tokens a baixo custo como nova vantagem estratégica decisiva (inédita na história do tech investing)", "Janelas de contexto muito longas + KV cache offload como caminho para utilidade de agentes (segurar todo o contexto corporativo)", "Mudança necessária de inteligência → utilidade: execução consistente e confiável de tarefas longas", "Edge AI (modelo podado rodando grátis no telefone a 30–60 tokens/s) como principal bear case para demanda de compute em nuvem", "ROI de IA: treinamento não gera retorno direto, inferência gera — risco de 'air gap' de ROIC no ciclo de capex", "Variação de uptime de clusters GPU (30% vs 90%) como diferencial competitivo decisivo", "'Taste' dos pesquisadores: intuição para escolher quais experimentos caros rodar em clusters de grande escala", "Levar ~3 gerações para construir um ASIC competitivo; só TPU e Trainium provavelmente sobreviverão"]
tools: ["Gemini 3 / Gemini Ultra", "Grok / Super Grok", "ChatGPT", "Nvidia Hopper", "Nvidia Blackwell (GB200, GB300)", "Nvidia Rubin", "Google TPU (v6, v7, v8, v9)", "AMD MI355 / MI450", "Amazon Trainium / Graviton / Nitro", "Broadcom (backend de ASIC, SerDes)", "MediaTek", "ARC AGI (benchmark)", "METR task-length evaluation", "X (Twitter)", "PyTorch / JAX", "Tesla Optimus"]
people: ["Gavin Baker", "Andrej Karpathy", "Jensen Huang", "Elon Musk", "Mark Zuckerberg", "Yann LeCun", "Lisa Su", "Eric Vishria", "Jeff Bezos", "Patrick O'Shaughnessy", "David George (a16z)", "OpenAI", "Anthropic", "Google DeepMind", "xAI", "Meta", "Microsoft", "Amazon", "Apple", "Nvidia", "Broadcom", "TSMC", "CH Robinson", "Iconiq"]
claims: ["Pague pelo tier máximo (~US$200/mês) para avaliar modelos; conclusões baseadas no free tier subestimam gravemente a capacidade real", "Siga de perto as 500–1000 pessoas na fronteira (muitas na China) no X — tudo em IA é downstream delas; leia tudo de Karpathy no mínimo três vezes", "Gemini 3 confirmou que as leis de scaling de pré-treinamento permanecem intactas; as três leis (pré-treino, RLVR, test-time compute) são multiplicativas", "Aplique RLVR a funções verificáveis: contabilidade (balanço fecha), vendas (conversão), suporte (escalação) — qualquer função com resultado certo/errado é automatizável", "O reasoning 'salvou' a IA ao sustentar progresso durante o hiato de ~18 meses entre Hopper e Blackwell/nova geração de TPU", "Os primeiros modelos treinados em Blackwell saem no início de 2026, provavelmente do xAI, que constrói data centers mais rápido e ajuda a depurar a plataforma para todos", "GB300 é drop-in compatível com racks GB200; quem for verticalmente integrado vira produtor de tokens de menor custo, mudando o cálculo estratégico do Google (margem negativa de -30% deixa de ser racional)", "Reasoning ativou o flywheel de dados nos labs de fronteira: feedback de usuários vira recompensa verificável que realimenta o modelo, transformando a dinâmica competitiva", "Cada lab usa internamente um checkpoint mais avançado para treinar o próximo modelo; não ter o checkpoint mais recente gera atraso composto quase impossível de recuperar", "Uptime de cluster é diferencial decisivo: competir com 30% de uptime contra alguém com 90% é não competir", "Janelas de contexto muito longas (com KV cache offload) podem resolver boa parte das limitações atuais, segurando Slack, Outlook e manuais da empresa inteira no contexto", "Edge AI — modelo podado tipo Gemini 5/Grok 4 rodando grátis a 30–60 tokens/s no telefone em ~3 anos (estratégia da Apple como distribuidora) — é o bear case mais plausível além da quebra das scaling laws", "Treinamento não gera ROI direto; inferência gera — monitorar queda de ROIC durante o pico de capex em Blackwell (Meta já imprimiu trimestre com ROIC em queda)", "ROIC dos maiores gastadores públicos de GPUs subiu após o ramp; CH Robinson (100% das cotações de frete em segundos vs 60% em 15–45 min, ação +20%) é o primeiro exemplo quantitativo Fortune 500 fora do setor de tech", "Construir um ASIC competitivo leva no mínimo 3 gerações; por economia, TPU e Trainium tenderão inevitavelmente à ferramentaria própria (client-owned tooling)", "Empresas para-empresa com forte cultura interna de experimentação tecnológica (ex.: melhores bancos de investimento, CH Robinson) adotarão IA antes e melhor que pares conservadores", "VCs montando holding companies para aplicar IA em negócios tradicionais não vencerão o private equity no próprio jogo deste"]
deep_dive: "medium"
deep_dive_reason: "Há densidade considerável de insights técnicos e estratégicos (scaling laws multiplicativas, RLVR, checkpoints internos, flywheel de dados, contexto longo para agentes), mas o conteúdo permanece na camada de análise de investimento sem profundidade arquitetural acionável em harness, evals, context-engineering ou governança."
---

# GPUs, TPUs, & The Economics of AI Explained | Gavin Baker Interview

## Tese
Gavin Baker argumenta que o Gemini 3 confirmou que as leis de scaling de pré-treinamento continuam válidas, que o reasoning (RLVR + test-time compute) bridou o hiato de compute até Blackwell e ativou um flywheel de dados nos labs de fronteira, e que a economia de custo por token reorganizará a vantagem competitiva (Google, Nvidia, xAI, ASICs) em 2026.

## Conceitos-chave
- Leis de scaling de pré-treinamento como observação empírica precisa mas teoricamente inexplicada (analogia aos egípcios e o Sol)
- RLVR: reinforcement learning com recompensas verificáveis — 'com IA, tudo que você pode verificar, você pode automatizar'
- Test-time compute como segunda nova lei de scaling, multiplicativa com pré-treino e RLVR
- Coerência de cluster (~200k GPUs Hopper como limite prático) como gargalo de pré-treinamento
- Flywheel de dados (produto→usuários→dados→melhor produto) agora começando a girar nos labs de fronteira via reasoning
- Checkpoints internos mais avançados usados para treinar o próximo modelo — defasagem composta para quem não os tem
- Produção de tokens a baixo custo como nova vantagem estratégica decisiva (inédita na história do tech investing)
- Janelas de contexto muito longas + KV cache offload como caminho para utilidade de agentes (segurar todo o contexto corporativo)
- Mudança necessária de inteligência → utilidade: execução consistente e confiável de tarefas longas
- Edge AI (modelo podado rodando grátis no telefone a 30–60 tokens/s) como principal bear case para demanda de compute em nuvem
- ROI de IA: treinamento não gera retorno direto, inferência gera — risco de 'air gap' de ROIC no ciclo de capex
- Variação de uptime de clusters GPU (30% vs 90%) como diferencial competitivo decisivo
- 'Taste' dos pesquisadores: intuição para escolher quais experimentos caros rodar em clusters de grande escala
- Levar ~3 gerações para construir um ASIC competitivo; só TPU e Trainium provavelmente sobreviverão

## Ferramentas & pessoas
**Ferramentas:** Gemini 3 / Gemini Ultra, Grok / Super Grok, ChatGPT, Nvidia Hopper, Nvidia Blackwell (GB200, GB300), Nvidia Rubin, Google TPU (v6, v7, v8, v9), AMD MI355 / MI450, Amazon Trainium / Graviton / Nitro, Broadcom (backend de ASIC, SerDes), MediaTek, ARC AGI (benchmark), METR task-length evaluation, X (Twitter), PyTorch / JAX, Tesla Optimus

**Pessoas/orgs:** Gavin Baker, Andrej Karpathy, Jensen Huang, Elon Musk, Mark Zuckerberg, Yann LeCun, Lisa Su, Eric Vishria, Jeff Bezos, Patrick O'Shaughnessy, David George (a16z), OpenAI, Anthropic, Google DeepMind, xAI, Meta, Microsoft, Amazon, Apple, Nvidia, Broadcom, TSMC, CH Robinson, Iconiq

## Claims acionáveis
- Pague pelo tier máximo (~US$200/mês) para avaliar modelos; conclusões baseadas no free tier subestimam gravemente a capacidade real
- Siga de perto as 500–1000 pessoas na fronteira (muitas na China) no X — tudo em IA é downstream delas; leia tudo de Karpathy no mínimo três vezes
- Gemini 3 confirmou que as leis de scaling de pré-treinamento permanecem intactas; as três leis (pré-treino, RLVR, test-time compute) são multiplicativas
- Aplique RLVR a funções verificáveis: contabilidade (balanço fecha), vendas (conversão), suporte (escalação) — qualquer função com resultado certo/errado é automatizável
- O reasoning 'salvou' a IA ao sustentar progresso durante o hiato de ~18 meses entre Hopper e Blackwell/nova geração de TPU
- Os primeiros modelos treinados em Blackwell saem no início de 2026, provavelmente do xAI, que constrói data centers mais rápido e ajuda a depurar a plataforma para todos
- GB300 é drop-in compatível com racks GB200; quem for verticalmente integrado vira produtor de tokens de menor custo, mudando o cálculo estratégico do Google (margem negativa de -30% deixa de ser racional)
- Reasoning ativou o flywheel de dados nos labs de fronteira: feedback de usuários vira recompensa verificável que realimenta o modelo, transformando a dinâmica competitiva
- Cada lab usa internamente um checkpoint mais avançado para treinar o próximo modelo; não ter o checkpoint mais recente gera atraso composto quase impossível de recuperar
- Uptime de cluster é diferencial decisivo: competir com 30% de uptime contra alguém com 90% é não competir
- Janelas de contexto muito longas (com KV cache offload) podem resolver boa parte das limitações atuais, segurando Slack, Outlook e manuais da empresa inteira no contexto
- Edge AI — modelo podado tipo Gemini 5/Grok 4 rodando grátis a 30–60 tokens/s no telefone em ~3 anos (estratégia da Apple como distribuidora) — é o bear case mais plausível além da quebra das scaling laws
- Treinamento não gera ROI direto; inferência gera — monitorar queda de ROIC durante o pico de capex em Blackwell (Meta já imprimiu trimestre com ROIC em queda)
- ROIC dos maiores gastadores públicos de GPUs subiu após o ramp; CH Robinson (100% das cotações de frete em segundos vs 60% em 15–45 min, ação +20%) é o primeiro exemplo quantitativo Fortune 500 fora do setor de tech
- Construir um ASIC competitivo leva no mínimo 3 gerações; por economia, TPU e Trainium tenderão inevitavelmente à ferramentaria própria (client-owned tooling)
- Empresas para-empresa com forte cultura interna de experimentação tecnológica (ex.: melhores bancos de investimento, CH Robinson) adotarão IA antes e melhor que pares conservadores
- VCs montando holding companies para aplicar IA em negócios tradicionais não vencerão o private equity no próprio jogo deste

> **Deep dive:** `medium` — Há densidade considerável de insights técnicos e estratégicos (scaling laws multiplicativas, RLVR, checkpoints internos, flywheel de dados, contexto longo para agentes), mas o conteúdo permanece na camada de análise de investimento sem profundidade arquitetural acionável em harness, evals, context-engineering ou governança.
