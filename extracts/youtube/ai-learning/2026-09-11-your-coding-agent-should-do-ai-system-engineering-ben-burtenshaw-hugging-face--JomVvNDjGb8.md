---
title: "Your Coding Agent Should Do AI System Engineering — Ben Burtenshaw, Hugging Face"
type: "extract"
source: "youtube"
video_id: "JomVvNDjGb8"
url: "https://www.youtube.com/watch?v=JomVvNDjGb8"
channel: "AI Engineer"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-your-coding-agent-should-do-ai-system-engineering-ben-burtenshaw-hugging-face--JomVvNDjGb8.txt]]"
tags: ["agents", "agentic-coding", "agent-tooling", "agent-fleets", "multi-agent", "agent-loop", "context-engineering", "evals", "model-selection", "observability", "telemetry", "monitoramento", "data-platform", "stack-tooling", "state", "verification"]
thesis: "Coding agents já são capazes de resolver os problemas mais difíceis de AI systems engineering — escrever kernels CUDA, fine-tunar LLMs e rodar um laboratório de pesquisa multi-agente — desde que recebam primitives abertos e repositórios padronizados (como o Hugging Face Hub) para distribuição, skills e evals."
concepts: ["kernels CUDA customizados", "eficiência em deep learning: compute, memória e overhead", "gargalo de memória vs compute (H100: ~1 petaflop/s vs 3 TB/s)", "intensidade aritmética / 'manter a GPU aquecida'", "distribuição de kernels via Hub com matriz de compatibilidade (TOML)", "skills como contexto file-based versionável (zero-shot → few-shot)", "benchmark e speedup de kernels por hardware", "auto-research multi-agente (literature scout, planner, workers, reporter)", "filas de hipóteses/jobs e templates de prompt por agente", "Git como estrutura de estado do laboratório (main branch, train original, scores)", "data layer aberto (Parquet) para observabilidade agnóstica", "verificação de experimentos via métrica objetiva (bits per bytes)", "open primitives vs APIs abstraídas como teto de agência"]
tools: ["Hugging Face Hub", "kernels (biblioteca HF)", "Upskill", "Trackio", "Unsloth", "OpenCode", "Codex", "Claude Code", "Gastown", "HF Papers", "HF CLI", "HF Jobs", "nanoGPT", "nano chat", "GPU MODE", "KernelBench", "Flash Attention", "Parquet", "GPT-OSS", "Kimi", "Haiku"]
people: ["Ben (Hugging Face)", "Andrej Karpathy", "Hugging Face", "Unsloth", "GPU MODE", "AMD", "Murvy (colega, HF)"]
claims: ["Agentes já escrevem kernels CUDA válidos e otimizados (hackathons GPU MODE e AMD, paper KernelBench), derrubando a percepção de que kernel-writing é inatingível para agentes", "Em GPUs modernas o gargalo costuma ser memória (bandwidth), não compute; kernels customizados aumentam a intensidade aritmética para 'manter a GPU aquecida'", "A biblioteca kernels da HF permite publicar kernels como repos no Hub (com TOML de hardware/versões CUDA), tornando agentes 'kernel publishers' e habilitando speedups fáceis por compatibilidade de hardware (ex.: 94% de speedup em kernel para Qwen 3 8B em H100)", "Skills são contexto file-based versionável que converte tarefas zero-shot em few-shot, com skills mantidas pelos próprios projetos (mais robustas) e skills experimentais em repo separado (huggingface-skills)", "Upskill gera skills + evals e compara modelos (ex.: GPT-OSS vs Kimi vs Haiku) em acurácia e uso de tokens, permitindo trocar modelo para economizar custo sem perder qualidade", "Fine-tuning zero-shot por agente ('fine-tune Qwen 3 6B neste dataset') já está integrado ao Hub via HF CLI skills, com variante mais barata mantida com Unsloth (frequentemente com créditos gratuitos)", "Auto-lab multi-agente: researcher formula hipóteses via HF Papers CLI, planner mantém fila de jobs, workers implementam patches e disparam HF Jobs, reporter mantém dashboards Trackio — rodando em paralelo por horas", "Trackio é o melhor dashboard para agentes porque expõe data layer aberto (Parquet): agentes podem ler/escrever tabelas livres, gerar Gantt charts customizados e emitir eventos/notificações (ex.: email quando agentes 'saem do controle')", "O estado do laboratório vive no Git (main branch com train original + estrutura de scores) com configurações e templates por sub-agente, implementável em OpenCode, Codex, Claude e Gastown", "Agentes performam melhor com primitives abertos: APIs abstraídas impõem um teto, e o objetivo é 'expor bem' em vez de extrair", "O Hub já possui os fundamentos (storage, tracking, compute) para workloads agênticos, e experimentos verificáveis (treino de modelos, kernels) são os mais fáceis de automatizar em auto-research"]
deep_dive: "high"
deep_dive_reason: "Apresenta arquitetura replicável de agent-fleet (papéis, filas de hipóteses, estado em Git, data layer Parquet) combinada com context-engineering via skills e evals comparativos (Upskill), com novidade real ao distribuir o auto-research do Karpathy em um laboratório multi-agente nativo do Hub."
---

# Your Coding Agent Should Do AI System Engineering — Ben Burtenshaw, Hugging Face

## Tese
Coding agents já são capazes de resolver os problemas mais difíceis de AI systems engineering — escrever kernels CUDA, fine-tunar LLMs e rodar um laboratório de pesquisa multi-agente — desde que recebam primitives abertos e repositórios padronizados (como o Hugging Face Hub) para distribuição, skills e evals.

## Conceitos-chave
- kernels CUDA customizados
- eficiência em deep learning: compute, memória e overhead
- gargalo de memória vs compute (H100: ~1 petaflop/s vs 3 TB/s)
- intensidade aritmética / 'manter a GPU aquecida'
- distribuição de kernels via Hub com matriz de compatibilidade (TOML)
- skills como contexto file-based versionável (zero-shot → few-shot)
- benchmark e speedup de kernels por hardware
- auto-research multi-agente (literature scout, planner, workers, reporter)
- filas de hipóteses/jobs e templates de prompt por agente
- Git como estrutura de estado do laboratório (main branch, train original, scores)
- data layer aberto (Parquet) para observabilidade agnóstica
- verificação de experimentos via métrica objetiva (bits per bytes)
- open primitives vs APIs abstraídas como teto de agência

## Ferramentas & pessoas
**Ferramentas:** Hugging Face Hub, kernels (biblioteca HF), Upskill, Trackio, Unsloth, OpenCode, Codex, Claude Code, Gastown, HF Papers, HF CLI, HF Jobs, nanoGPT, nano chat, GPU MODE, KernelBench, Flash Attention, Parquet, GPT-OSS, Kimi, Haiku

**Pessoas/orgs:** Ben (Hugging Face), Andrej Karpathy, Hugging Face, Unsloth, GPU MODE, AMD, Murvy (colega, HF)

## Claims acionáveis
- Agentes já escrevem kernels CUDA válidos e otimizados (hackathons GPU MODE e AMD, paper KernelBench), derrubando a percepção de que kernel-writing é inatingível para agentes
- Em GPUs modernas o gargalo costuma ser memória (bandwidth), não compute; kernels customizados aumentam a intensidade aritmética para 'manter a GPU aquecida'
- A biblioteca kernels da HF permite publicar kernels como repos no Hub (com TOML de hardware/versões CUDA), tornando agentes 'kernel publishers' e habilitando speedups fáceis por compatibilidade de hardware (ex.: 94% de speedup em kernel para Qwen 3 8B em H100)
- Skills são contexto file-based versionável que converte tarefas zero-shot em few-shot, com skills mantidas pelos próprios projetos (mais robustas) e skills experimentais em repo separado (huggingface-skills)
- Upskill gera skills + evals e compara modelos (ex.: GPT-OSS vs Kimi vs Haiku) em acurácia e uso de tokens, permitindo trocar modelo para economizar custo sem perder qualidade
- Fine-tuning zero-shot por agente ('fine-tune Qwen 3 6B neste dataset') já está integrado ao Hub via HF CLI skills, com variante mais barata mantida com Unsloth (frequentemente com créditos gratuitos)
- Auto-lab multi-agente: researcher formula hipóteses via HF Papers CLI, planner mantém fila de jobs, workers implementam patches e disparam HF Jobs, reporter mantém dashboards Trackio — rodando em paralelo por horas
- Trackio é o melhor dashboard para agentes porque expõe data layer aberto (Parquet): agentes podem ler/escrever tabelas livres, gerar Gantt charts customizados e emitir eventos/notificações (ex.: email quando agentes 'saem do controle')
- O estado do laboratório vive no Git (main branch com train original + estrutura de scores) com configurações e templates por sub-agente, implementável em OpenCode, Codex, Claude e Gastown
- Agentes performam melhor com primitives abertos: APIs abstraídas impõem um teto, e o objetivo é 'expor bem' em vez de extrair
- O Hub já possui os fundamentos (storage, tracking, compute) para workloads agênticos, e experimentos verificáveis (treino de modelos, kernels) são os mais fáceis de automatizar em auto-research

> **Deep dive:** `high` — Apresenta arquitetura replicável de agent-fleet (papéis, filas de hipóteses, estado em Git, data layer Parquet) combinada com context-engineering via skills e evals comparativos (Upskill), com novidade real ao distribuir o auto-research do Karpathy em um laboratório multi-agente nativo do Hub.
