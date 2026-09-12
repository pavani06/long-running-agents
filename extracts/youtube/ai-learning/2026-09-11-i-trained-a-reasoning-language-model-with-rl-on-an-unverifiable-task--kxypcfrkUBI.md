---
title: "I trained a Reasoning Language Model with RL on an unverifiable task"
type: "extract"
source: "youtube"
video_id: "kxypcfrkUBI"
url: "https://www.youtube.com/watch?v=kxypcfrkUBI"
channel: "Neural Breakdown with AVB"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-i-trained-a-reasoning-language-model-with-rl-on-an-unverifiable-task--kxypcfrkUBI.txt]]"
tags: ["evals", "verification", "harness", "gate-design", "model-selection", "error-handling", "analise", "process"]
thesis: "Um SLM de 135M parâmetros pode aprender a raciocinar em domínios não verificáveis combinando recompensas heurísticas verificáveis (formato, schema, gate de comprimento) com um reward model leve de equivalência de respostas (22M, all-MiniLM) sob GRPO, defendendo-se ativamente contra reward hacking via redesenho iterativo da reward function e avaliação com juiz externo."
concepts: ["GRPO (Group Relative Policy Optimization)", "Pipeline de post-training: CPT, SFT, DPO, RL", "Ambientes verificáveis (RLVR) vs não verificáveis", "Reward models: autoregressivo (Bradley-Terry), juiz externo, answer equivalence model", "Limitações de F1 (word overlap) e BERTScore (embeddings contextuais)", "Reward hacking e Lei de Goodhart (proxy vs intenção)", "Termo de KL divergence como âncora ao modelo de referência", "Normalização de vantagens por grupo (média vs desvio padrão)", "Credit assignment implícito do GRPO entre tokens", "Geração de confounds procedurais (troca de entidades, inversão de números, antônimos de verbos)", "Spearman rank correlation vs MSE para seleção de reward model", "Viés de comprimento e decoupling comprimento-qualidade", "Warm-up SFT em dataset de reasoning antes do RL", "Temperatura (~0.5) para fabricar variância entre rollouts do grupo", "Schema matching reward para outputs estruturados (JSON, listas, triplas)"]
tools: ["GRPO", "all-MiniLM (22M parâmetros)", "DeepSeek V4 Flash (juiz)", "Qwen 0.8B", "Hugging Face", "GitHub"]
people: ["DeepSeek", "Qwen", "Hugging Face", "Goodhart", "Bradley-Terry"]
claims: ["Combine recompensas heurísticas verificáveis (formato, tipo de dado, gate de comprimento) com um reward model neural de equivalência de respostas, em vez de depender de apenas um dos dois", "Modelos de answer equivalence exigem apenas tríades (prompt, resposta, ground truth), permitindo usar qualquer dataset supervisionado e um modelo muito menor que um reward model autoregressivo", "Gere confounds de treino proceduralmente: inverta números, troque entidades nomeadas, inverta verbos (score 3/5), embaralhe respostas entre prompts (score 1/5) e inclua matches exatos (score 5/5) para calibrar o reward model", "Descongele a maioria das camadas do encoder (5 de 6 no MiniLM): camadas inferiores congeladas colapsam entradas quase idênticas em embeddings indistinguíveis, cegando o modelo para diferenças factuais finas", "Desacople comprimento de qualidade reescrevendo respostas ruins em excelentes mantendo-as longas, eliminando viés de 'curto é bom'", "Selecione o reward model por MSE contra scores do juiz, não por rank correlation — correlação alta pode mascarar scores absolutamente inúteis para GRPO", "Use temperatura ~0.5 nos rollouts: alta demais gera gibberish com recompensas zeradas, baixa demais elimina a variância intra-grupo que o GRPO precisa", "Faça um warm-up SFT em um dataset pequeno de reasoning (~20k linhas) antes do RL, para que o modelo emita trace de raciocínio que o RL possa amplificar", "Substitua penalidade linear de comprimento por um gate (penalizar só se 2x maior/menor que o alvo): componentes constantes no grupo contribuem zero ao gradiente e rampas lineares são o caminho mais fácil para o otimizador hackear", "Desligue a normalização por desvio padrão das vantagens quando ela estiver mutando as diferenças de recompensa entre rollouts e enfraquecendo o sinal de gradiente", "Descarte o termo de KL divergence quando o policy inicial é muito ruim, permitindo que o modelo hill-climbe a reward function", "Adicione uma recompensa verificável de schema matching ao lado da neural, senão o policy abandona JSON/listas porque prosa maximiza overlap de keywords no reward model", "Avalie os runs com um juiz externo mais forte (ex.: DeepSeek) em vez da própria reward function, para detectar reward hacking (ex.: frases-âncora como 'the passage defines')", "Resultado: o SLM de 135M empatou/superou por pouco o Qwen 0.8B no domínio estreito, com um reward model de 22M treinado em ~20k exemplos"]
deep_dive: "high"
deep_dive_reason: "Densidade alta de insight acionável e arquitetural (loop iterativo de engenharia de reward model com confounds, contramedidas concretas de reward hacking, tuning fino de GRPO como gate de comprimento e normalização de vantagens) diretamente relevante a evals, verification e gate-design, com novidade prática rara documentada abertamente."
---

# I trained a Reasoning Language Model with RL on an unverifiable task

## Tese
Um SLM de 135M parâmetros pode aprender a raciocinar em domínios não verificáveis combinando recompensas heurísticas verificáveis (formato, schema, gate de comprimento) com um reward model leve de equivalência de respostas (22M, all-MiniLM) sob GRPO, defendendo-se ativamente contra reward hacking via redesenho iterativo da reward function e avaliação com juiz externo.

## Conceitos-chave
- GRPO (Group Relative Policy Optimization)
- Pipeline de post-training: CPT, SFT, DPO, RL
- Ambientes verificáveis (RLVR) vs não verificáveis
- Reward models: autoregressivo (Bradley-Terry), juiz externo, answer equivalence model
- Limitações de F1 (word overlap) e BERTScore (embeddings contextuais)
- Reward hacking e Lei de Goodhart (proxy vs intenção)
- Termo de KL divergence como âncora ao modelo de referência
- Normalização de vantagens por grupo (média vs desvio padrão)
- Credit assignment implícito do GRPO entre tokens
- Geração de confounds procedurais (troca de entidades, inversão de números, antônimos de verbos)
- Spearman rank correlation vs MSE para seleção de reward model
- Viés de comprimento e decoupling comprimento-qualidade
- Warm-up SFT em dataset de reasoning antes do RL
- Temperatura (~0.5) para fabricar variância entre rollouts do grupo
- Schema matching reward para outputs estruturados (JSON, listas, triplas)

## Ferramentas & pessoas
**Ferramentas:** GRPO, all-MiniLM (22M parâmetros), DeepSeek V4 Flash (juiz), Qwen 0.8B, Hugging Face, GitHub

**Pessoas/orgs:** DeepSeek, Qwen, Hugging Face, Goodhart, Bradley-Terry

## Claims acionáveis
- Combine recompensas heurísticas verificáveis (formato, tipo de dado, gate de comprimento) com um reward model neural de equivalência de respostas, em vez de depender de apenas um dos dois
- Modelos de answer equivalence exigem apenas tríades (prompt, resposta, ground truth), permitindo usar qualquer dataset supervisionado e um modelo muito menor que um reward model autoregressivo
- Gere confounds de treino proceduralmente: inverta números, troque entidades nomeadas, inverta verbos (score 3/5), embaralhe respostas entre prompts (score 1/5) e inclua matches exatos (score 5/5) para calibrar o reward model
- Descongele a maioria das camadas do encoder (5 de 6 no MiniLM): camadas inferiores congeladas colapsam entradas quase idênticas em embeddings indistinguíveis, cegando o modelo para diferenças factuais finas
- Desacople comprimento de qualidade reescrevendo respostas ruins em excelentes mantendo-as longas, eliminando viés de 'curto é bom'
- Selecione o reward model por MSE contra scores do juiz, não por rank correlation — correlação alta pode mascarar scores absolutamente inúteis para GRPO
- Use temperatura ~0.5 nos rollouts: alta demais gera gibberish com recompensas zeradas, baixa demais elimina a variância intra-grupo que o GRPO precisa
- Faça um warm-up SFT em um dataset pequeno de reasoning (~20k linhas) antes do RL, para que o modelo emita trace de raciocínio que o RL possa amplificar
- Substitua penalidade linear de comprimento por um gate (penalizar só se 2x maior/menor que o alvo): componentes constantes no grupo contribuem zero ao gradiente e rampas lineares são o caminho mais fácil para o otimizador hackear
- Desligue a normalização por desvio padrão das vantagens quando ela estiver mutando as diferenças de recompensa entre rollouts e enfraquecendo o sinal de gradiente
- Descarte o termo de KL divergence quando o policy inicial é muito ruim, permitindo que o modelo hill-climbe a reward function
- Adicione uma recompensa verificável de schema matching ao lado da neural, senão o policy abandona JSON/listas porque prosa maximiza overlap de keywords no reward model
- Avalie os runs com um juiz externo mais forte (ex.: DeepSeek) em vez da própria reward function, para detectar reward hacking (ex.: frases-âncora como 'the passage defines')
- Resultado: o SLM de 135M empatou/superou por pouco o Qwen 0.8B no domínio estreito, com um reward model de 22M treinado em ~20k exemplos

> **Deep dive:** `high` — Densidade alta de insight acionável e arquitetural (loop iterativo de engenharia de reward model com confounds, contramedidas concretas de reward hacking, tuning fino de GRPO como gate de comprimento e normalização de vantagens) diretamente relevante a evals, verification e gate-design, com novidade prática rara documentada abertamente.
