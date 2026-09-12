---
title: "Stanford AI Club: Jason Wei on 3 Key Ideas in AI in 2025"
type: "extract"
source: "youtube"
video_id: "b6Doq2fz81U"
url: "https://www.youtube.com/watch?v=b6Doq2fz81U"
channel: "Stanford AI Club"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-stanford-ai-club-jason-wei-on-3-key-ideas-in-ai-in-2025--b6Doq2fz81U.txt]]"
tags: ["analise", "analise-estrutural", "classification", "evals", "verification", "macroeconomia", "roadmap"]
thesis: "A navegação da IA em 2025 repousa em três forças: a inteligência torna-se commodity com custo tendendo a zero, o progresso segue a 'Lei do Verificador' (a capacidade de treinar IA numa tarefa é proporcional à facilidade de verificar essa tarefa) e o avanço é 'serrilhado' por tarefa, o que torna improvável um fast takeoff."
concepts: ["Inteligência como commodity (custo de desempenho fixado cai a cada ano)", "Compute adaptativo / escala em tempo de teste como destravador de redução de custo", "Lei do Verificador (assimetria entre gerar e verificar soluções)", "Cinco critérios de verificabilidade: verdade objetiva, velocidade, escalabilidade paralela, baixo ruído, recompensa contínua", "Informação privilegiada (gabaritos, casos de teste) desloca tarefas no plano gerar/verificar", "Borda serrilhada da inteligência: capacidade e taxa de melhoria variam por tarefa", "Rejeição do fast takeoff: auto-melhoria como espectro gradual, não limiar binário", "Heurísticas de previsão de capacidades: tarefa digital, fácil para humanos, dados abundantes", "Geração de dados sintéticos via RL quando existe métrica objetiva única (tática AlphaZero/AlphaEvolve)", "Commoditização pós-fronteira de habilidades e benchmarks", "Valor relativo crescente de informação privada/insider", "Democratização de campos antes fechados por barreias de conhecimento (vibe coding, saúde pessoal)", "Colapso do tempo de recuperação de informação pública entre eras (pré-internet, internet, chatbot, agentes)", "Seleção de problemas onde treino e teste coincidem para contornar generalização"]
tools: ["MMLU", "o1 (OpenAI)", "Deep Research (OpenAI)", "ChatGPT", "OpenAI Operator", "Kosis (base de dados coreana)", "Browse Comp (benchmark)", "AlphaEvolve (DeepMind)", "AlphaZero", "SWE-bench"]
people: ["Jason Wei (palestrante; Meta Super Intelligence Labs, ex-OpenAI, ex-Google Brain)", "Meta Super Intelligence Labs", "OpenAI", "Google Brain", "DeepMind", "Boaz (ex-colega citado)", "Roon (citado sobre conselhos de carreira)", "Danny (ex-colega citado sobre métricas de avaliação)", "Elon Musk (menção ilustrativa)"]
claims: ["O custo para atingir um nível fixo de desempenho (ex.: MMLU) cai a cada ano, empurrando o preço da inteligência para zero.", "Compute adaptativo funciona de fato pela primeira vez na história do deep learning, permitindo baratear tarefas fáceis sem escalar o tamanho do modelo.", "Agentes reduzem para minutos/horas a recuperação de informações públicas que antes levariam semanas (ex.: casamentos em Busan em 1983 via base Kosis, resolvido pelo Operator mas não pelo o3).", "Deep Research resolve cerca de metade do benchmark Browse Comp, enquanto muitos humanos não resolvem as questões em 2 horas.", "Toda tarefa solúvel e facilmente verificável será eventualmente dominada pela IA; os benchmarks existentes são a instância natural dessa lei.", "Verificabilidade é função de cinco propriedades: verdade objetiva, velocidade de verificação, capacidade de verificar milhões de respostas em paralelo, baixo ruído e recompensa contínua.", "Fornecer informação privilegiada (gabaritos, casos de teste como no SWE-bench) desloca tarefas para o quadrante de verificação fácil.", "AlphaEvolve amostra candidatos com LLM, pontua-os e realimenta os melhores como inspiração, escolhendo problemas onde treino e teste coincidem para sidesteppar generalização.", "Fast takeoff é improvável: a auto-melhoria é um espectro por tarefa (de nem acessar o codebase a treinar autonomamente com intervenção humana ocasional), não um evento binário.", "IA avança primeiro em tarefas digitais, fáceis para humanos e com dados abundantes; tarefas físicas ou com dados escassos (encanamento, cabeleireiro, línguas de baixíssimo recurso, tapetes artesanais) ficam para muito depois.", "Com uma métrica objetiva única, RL gera dados sintéticos e resolve benchmarks rapidamente (tática AlphaZero/AlphaEvolve).", "Previsões ilustrativas do palestrante: pesquisa em IA ~2027, produção de filmes ~2029, pesquisa em química depois da pesquisa em IA.", "Oportunidade de negócio: criar formas de medir o que hoje não é medido, habilitando otimização subsequente por IA.", "O valor relativo de informação privada/insider sobe conforme a informação pública se torna instantânea e gratuita.", "Heurísticas simples (digital, dificuldade para humanos, abundância de dados) permitem prever razoavelmente quando a IA dominará uma tarefa."]
deep_dive: "medium"
deep_dive_reason: "Contém frameworks originais e acionáveis (Lei do Verificador, critérios de verificabilidade, heurísticas de previsão por tarefa) com relevância a evals, mas permanece em nível conceitual/estratégico sem profundidade arquitetural em harness, context-engineering ou agent-fleets."
---

# Stanford AI Club: Jason Wei on 3 Key Ideas in AI in 2025

## Tese
A navegação da IA em 2025 repousa em três forças: a inteligência torna-se commodity com custo tendendo a zero, o progresso segue a 'Lei do Verificador' (a capacidade de treinar IA numa tarefa é proporcional à facilidade de verificar essa tarefa) e o avanço é 'serrilhado' por tarefa, o que torna improvável um fast takeoff.

## Conceitos-chave
- Inteligência como commodity (custo de desempenho fixado cai a cada ano)
- Compute adaptativo / escala em tempo de teste como destravador de redução de custo
- Lei do Verificador (assimetria entre gerar e verificar soluções)
- Cinco critérios de verificabilidade: verdade objetiva, velocidade, escalabilidade paralela, baixo ruído, recompensa contínua
- Informação privilegiada (gabaritos, casos de teste) desloca tarefas no plano gerar/verificar
- Borda serrilhada da inteligência: capacidade e taxa de melhoria variam por tarefa
- Rejeição do fast takeoff: auto-melhoria como espectro gradual, não limiar binário
- Heurísticas de previsão de capacidades: tarefa digital, fácil para humanos, dados abundantes
- Geração de dados sintéticos via RL quando existe métrica objetiva única (tática AlphaZero/AlphaEvolve)
- Commoditização pós-fronteira de habilidades e benchmarks
- Valor relativo crescente de informação privada/insider
- Democratização de campos antes fechados por barreias de conhecimento (vibe coding, saúde pessoal)
- Colapso do tempo de recuperação de informação pública entre eras (pré-internet, internet, chatbot, agentes)
- Seleção de problemas onde treino e teste coincidem para contornar generalização

## Ferramentas & pessoas
**Ferramentas:** MMLU, o1 (OpenAI), Deep Research (OpenAI), ChatGPT, OpenAI Operator, Kosis (base de dados coreana), Browse Comp (benchmark), AlphaEvolve (DeepMind), AlphaZero, SWE-bench

**Pessoas/orgs:** Jason Wei (palestrante; Meta Super Intelligence Labs, ex-OpenAI, ex-Google Brain), Meta Super Intelligence Labs, OpenAI, Google Brain, DeepMind, Boaz (ex-colega citado), Roon (citado sobre conselhos de carreira), Danny (ex-colega citado sobre métricas de avaliação), Elon Musk (menção ilustrativa)

## Claims acionáveis
- O custo para atingir um nível fixo de desempenho (ex.: MMLU) cai a cada ano, empurrando o preço da inteligência para zero.
- Compute adaptativo funciona de fato pela primeira vez na história do deep learning, permitindo baratear tarefas fáceis sem escalar o tamanho do modelo.
- Agentes reduzem para minutos/horas a recuperação de informações públicas que antes levariam semanas (ex.: casamentos em Busan em 1983 via base Kosis, resolvido pelo Operator mas não pelo o3).
- Deep Research resolve cerca de metade do benchmark Browse Comp, enquanto muitos humanos não resolvem as questões em 2 horas.
- Toda tarefa solúvel e facilmente verificável será eventualmente dominada pela IA; os benchmarks existentes são a instância natural dessa lei.
- Verificabilidade é função de cinco propriedades: verdade objetiva, velocidade de verificação, capacidade de verificar milhões de respostas em paralelo, baixo ruído e recompensa contínua.
- Fornecer informação privilegiada (gabaritos, casos de teste como no SWE-bench) desloca tarefas para o quadrante de verificação fácil.
- AlphaEvolve amostra candidatos com LLM, pontua-os e realimenta os melhores como inspiração, escolhendo problemas onde treino e teste coincidem para sidesteppar generalização.
- Fast takeoff é improvável: a auto-melhoria é um espectro por tarefa (de nem acessar o codebase a treinar autonomamente com intervenção humana ocasional), não um evento binário.
- IA avança primeiro em tarefas digitais, fáceis para humanos e com dados abundantes; tarefas físicas ou com dados escassos (encanamento, cabeleireiro, línguas de baixíssimo recurso, tapetes artesanais) ficam para muito depois.
- Com uma métrica objetiva única, RL gera dados sintéticos e resolve benchmarks rapidamente (tática AlphaZero/AlphaEvolve).
- Previsões ilustrativas do palestrante: pesquisa em IA ~2027, produção de filmes ~2029, pesquisa em química depois da pesquisa em IA.
- Oportunidade de negócio: criar formas de medir o que hoje não é medido, habilitando otimização subsequente por IA.
- O valor relativo de informação privada/insider sobe conforme a informação pública se torna instantânea e gratuita.
- Heurísticas simples (digital, dificuldade para humanos, abundância de dados) permitem prever razoavelmente quando a IA dominará uma tarefa.

> **Deep dive:** `medium` — Contém frameworks originais e acionáveis (Lei do Verificador, critérios de verificabilidade, heurísticas de previsão por tarefa) com relevância a evals, mas permanece em nível conceitual/estratégico sem profundidade arquitetural em harness, context-engineering ou agent-fleets.
