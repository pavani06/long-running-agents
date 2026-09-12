---
title: "RAG is Exploding: 58 NEW RAG Methods in 48 hours"
type: "extract"
source: "youtube"
video_id: "cHVQj7w9TD4"
url: "https://www.youtube.com/watch?v=cHVQj7w9TD4"
channel: "Discover AI"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-rag-is-exploding-58-new-rag-methods-in-48-hours--cHVQj7w9TD4.txt]]"
tags: ["agents", "agent-loop", "agent-fleets", "multi-agent", "evals", "arquitetura", "frameworks", "knowledge-management", "context-engineering", "model-selection", "decision-discipline", "analise"]
thesis: "RAG está sendo reinventado pelo aprendizado por reforço pós-DeepSeek R1, com agentes de busca especializados treinados isoladamente (ex.: S3 com a recompensa 'gain beyond RAG') superando a otimização end-to-end porque a maioria dos ganhos de RAG provém da capacidade de busca, e não do alinhamento da geração."
concepts: ["RAG (Retrieval-Augmented Generation)", "Agentic RAG", "Agentes de busca treinados por reinforcement learning", "Reward function (recompensa de recuperação, de formato, exact match)", "Gain Beyond RAG (GBR) como métrica relativa de recompensa", "Search-R1 (retrieve + generate conjuntos via RL)", "S3 (Search-Select-Surf): searcher desacoplado do gerador", "DeepRetrieval (RL sem dados supervisionados)", "DeepSeek R1-Zero: recompensas rule-based/outcome-driven", "PPO / GRPO / DPO / DAPO / VAPO / GenRM / Luffy (off-policy)", "Interação multi-turn com search engine durante rollouts", "Query augmentation e múltiplas queries paralelas", "Gerador congelado/black-box + searcher treinável (modularidade)", "Domain transfer do agente de busca", "Eficiência de dados de treinamento (~70x menos)", "Process reward vs outcome reward", "Knowledge graph RAG / GraphRAG / LightRAG", "Split RAG com semantic partitioning por tipo", "Self-RAG (distillation/SFT, pré-RL)", "Métricas de recuperação (recall, nDCG) desconectadas da qualidade da resposta final", "Segurança de RAG: extração implícita de conhecimento e jailbreaking"]
tools: ["DeepSeek R1 / R1-Zero", "OpenAI o3 Pro", "Qwen 2.5 (7B e 3B)", "Google Search", "Hugging Face", "LangChain", "MCP (Model Context Protocol)", "A2A (agent-to-agent protocol)", "Volcano Engine RL (verl)", "HybridFlow", "GitHub: DeepRetrieval", "GitHub: Search-R1", "Claude (Anthropic)", "GPT-4.1", "Self-RAG"]
people: ["University of Illinois", "Korea University", "University of Massachusetts", "Google Cloud AI Research", "Google I/O 2025", "Amazon", "OpenAI", "Anthropic", "Chinese University of Hong Kong", "Tencent", "National University of Singapore", "Peking University", "Tsinghua University", "Renmin University of China", "Beijing Academy of Artificial Intelligence", "NTT Corporation", "Alan Turing Institute", "King's College London", "University of Alberta", "Technical University of Vienna", "Kyoto University", "University of Tokyo", "City University of Hong Kong", "NewArk Lab", "UNSW Sydney"]
claims: ["Treinar um searcher LLM dedicado via RL com métricas de recuperação como recompensa (DeepRetrieval) melhora busca de literatura em até 65% sem dados anotados por humanos, apenas trial-and-error", "Search-R1 treina um único modelo para recuperar e gerar com exact match como recompensa: +41% (Qwen2.5-7B) e +20% (3B) sobre baseline RAG, mas acopla busca e geração e exige tuning completo do modelo", "S3 desacopla o agente de busca do gerador congelado (ex.: o3 Pro), tornando o searcher treinado reutilizável com qualquer gerador open-source, proprietário ou quantizado", "S3 atinge desempenho forte em 6 benchmarks gerais e 5 médicos de QA com ~70x menos dados de treinamento que métodos RL concorrentes, reduzindo custo e tempo", "S3 supera Search-R1 em qualidade de busca: a maior parte dos ganhos de RAG vem de melhorar a busca, não de alinhar a geração — searcher-only training bate otimização end-to-end", "A escolha da recompensa molda diretamente a política de busca: métricas semânticas/alinhadas a preferência humana recuperam documentos substantivamente úteis versus otimizar sobreposição frágil de strings", "O loop do searcher S3 filtra queries solúveis por naive RAG e concentra esforço nas perguntas difíceis, decidindo iterativamente se continua buscando (planejamento com métrica de completude)", "GBR permite otimizar o agente contra o seu melhor sistema RAG atual (GraphRAG, SplitRAG, Graph+Agent RAG) como benchmark relativo em vez de um baseline absoluto", "Métricas clássicas de recuperação (recall, nDCG não-normalizado) são desconectadas da qualidade da resposta final; integre recompensa de downstream na avaliação", "A implementação de referência do S3 ainda usa PPO; migrar para DPO/GRPO/DAPO/VAPO ou generative reward models (self-principle critique tuning) é oportunidade direta de melhoria", "Volcano Engine RL está emergindo como biblioteca padrão production-ready para treino RL de LLMs na maioria das publicações recentes asiáticas", "Rollouts multi-turn com search engine habilitam otimização em tempo real sobre dados correntes, sem dados sintéticos, simulação ou dados defasados", "Treinamento searcher-only habilita transferência de domínio: o mesmo searcher serve múltiplos geradores e domínios (geral e médico) sem retrabalho"]
deep_dive: "high"
deep_dive_reason: "Densa em insight arquitetural e acionável — design de recompensa (GBR, exact match vs métricas semânticas), desacoplamento searcher/gerador com números concretos de eficiência (70x menos dados) — combinando novidade (S3, searcher-only training) com relevância direta a evals, agent-fleets e arquitetura de agentes."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-building-production-ready-rag-applications-jerry-liu--TRjq7t2Ms5I|Building Production-Ready RAG Applications: Jerry Liu]]", "[[extracts/youtube/ai-learning/2026-09-11-rag-vs-cag-solving-knowledge-gaps-in-ai-models--HdafI0t3sEY|RAG vs. CAG: Solving Knowledge Gaps in AI Models]]", "[[extracts/youtube/ai-learning/2026-09-11-i-want-llama3-to-perform-10x-with-my-private-knowledge-local-agentic-rag-w-llama--u5Vcrwpzoz8|\"I want Llama3 to perform 10x with my private knowledge\" - Local Agentic RAG w/ llama3]]", "[[extracts/youtube/ai-learning/2026-09-11-i-trained-a-reasoning-language-model-with-rl-on-an-unverifiable-task--kxypcfrkUBI|I trained a Reasoning Language Model with RL on an unverifiable task]]", "[[extracts/youtube/ai-learning/2026-09-11-parallels-parag-agrawal-building-a-new-web-for-ai-agents--fUcnE6pjq5w|Parallel’s Parag Agrawal: Building a New Web for AI Agents]]", "[[extracts/youtube/ai-learning/2026-09-11-research-agent-3-0-build-a-group-of-ai-researchers-here-is-how--AVInhYBUnKs|\"Research agent 3.0 - Build a group of AI researchers\" - Here is how]]"]
---

# RAG is Exploding: 58 NEW RAG Methods in 48 hours

## Tese
RAG está sendo reinventado pelo aprendizado por reforço pós-DeepSeek R1, com agentes de busca especializados treinados isoladamente (ex.: S3 com a recompensa 'gain beyond RAG') superando a otimização end-to-end porque a maioria dos ganhos de RAG provém da capacidade de busca, e não do alinhamento da geração.

## Conceitos-chave
- RAG (Retrieval-Augmented Generation)
- Agentic RAG
- Agentes de busca treinados por reinforcement learning
- Reward function (recompensa de recuperação, de formato, exact match)
- Gain Beyond RAG (GBR) como métrica relativa de recompensa
- Search-R1 (retrieve + generate conjuntos via RL)
- S3 (Search-Select-Surf): searcher desacoplado do gerador
- DeepRetrieval (RL sem dados supervisionados)
- DeepSeek R1-Zero: recompensas rule-based/outcome-driven
- PPO / GRPO / DPO / DAPO / VAPO / GenRM / Luffy (off-policy)
- Interação multi-turn com search engine durante rollouts
- Query augmentation e múltiplas queries paralelas
- Gerador congelado/black-box + searcher treinável (modularidade)
- Domain transfer do agente de busca
- Eficiência de dados de treinamento (~70x menos)
- Process reward vs outcome reward
- Knowledge graph RAG / GraphRAG / LightRAG
- Split RAG com semantic partitioning por tipo
- Self-RAG (distillation/SFT, pré-RL)
- Métricas de recuperação (recall, nDCG) desconectadas da qualidade da resposta final
- Segurança de RAG: extração implícita de conhecimento e jailbreaking

## Ferramentas & pessoas
**Ferramentas:** DeepSeek R1 / R1-Zero, OpenAI o3 Pro, Qwen 2.5 (7B e 3B), Google Search, Hugging Face, LangChain, MCP (Model Context Protocol), A2A (agent-to-agent protocol), Volcano Engine RL (verl), HybridFlow, GitHub: DeepRetrieval, GitHub: Search-R1, Claude (Anthropic), GPT-4.1, Self-RAG

**Pessoas/orgs:** University of Illinois, Korea University, University of Massachusetts, Google Cloud AI Research, Google I/O 2025, Amazon, OpenAI, Anthropic, Chinese University of Hong Kong, Tencent, National University of Singapore, Peking University, Tsinghua University, Renmin University of China, Beijing Academy of Artificial Intelligence, NTT Corporation, Alan Turing Institute, King's College London, University of Alberta, Technical University of Vienna, Kyoto University, University of Tokyo, City University of Hong Kong, NewArk Lab, UNSW Sydney

## Claims acionáveis
- Treinar um searcher LLM dedicado via RL com métricas de recuperação como recompensa (DeepRetrieval) melhora busca de literatura em até 65% sem dados anotados por humanos, apenas trial-and-error
- Search-R1 treina um único modelo para recuperar e gerar com exact match como recompensa: +41% (Qwen2.5-7B) e +20% (3B) sobre baseline RAG, mas acopla busca e geração e exige tuning completo do modelo
- S3 desacopla o agente de busca do gerador congelado (ex.: o3 Pro), tornando o searcher treinado reutilizável com qualquer gerador open-source, proprietário ou quantizado
- S3 atinge desempenho forte em 6 benchmarks gerais e 5 médicos de QA com ~70x menos dados de treinamento que métodos RL concorrentes, reduzindo custo e tempo
- S3 supera Search-R1 em qualidade de busca: a maior parte dos ganhos de RAG vem de melhorar a busca, não de alinhar a geração — searcher-only training bate otimização end-to-end
- A escolha da recompensa molda diretamente a política de busca: métricas semânticas/alinhadas a preferência humana recuperam documentos substantivamente úteis versus otimizar sobreposição frágil de strings
- O loop do searcher S3 filtra queries solúveis por naive RAG e concentra esforço nas perguntas difíceis, decidindo iterativamente se continua buscando (planejamento com métrica de completude)
- GBR permite otimizar o agente contra o seu melhor sistema RAG atual (GraphRAG, SplitRAG, Graph+Agent RAG) como benchmark relativo em vez de um baseline absoluto
- Métricas clássicas de recuperação (recall, nDCG não-normalizado) são desconectadas da qualidade da resposta final; integre recompensa de downstream na avaliação
- A implementação de referência do S3 ainda usa PPO; migrar para DPO/GRPO/DAPO/VAPO ou generative reward models (self-principle critique tuning) é oportunidade direta de melhoria
- Volcano Engine RL está emergindo como biblioteca padrão production-ready para treino RL de LLMs na maioria das publicações recentes asiáticas
- Rollouts multi-turn com search engine habilitam otimização em tempo real sobre dados correntes, sem dados sintéticos, simulação ou dados defasados
- Treinamento searcher-only habilita transferência de domínio: o mesmo searcher serve múltiplos geradores e domínios (geral e médico) sem retrabalho

> **Deep dive:** `high` — Densa em insight arquitetural e acionável — design de recompensa (GBR, exact match vs métricas semânticas), desacoplamento searcher/gerador com números concretos de eficiência (70x menos dados) — combinando novidade (S3, searcher-only training) com relevância direta a evals, agent-fleets e arquitetura de agentes.
