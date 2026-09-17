---
title: "If we want them to do Knowledge Work, design them as Knowledge Agents — Benjamin Clavié, Mixedbread"
type: "extract"
source: "youtube"
video_id: "O84lhGc1OOI"
url: "https://www.youtube.com/watch?v=O84lhGc1OOI"
channel: "AI Engineer"
extracted: "2026-09-17"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-17-if-we-want-them-to-do-knowledge-work-design-them-as-knowledge-agents-benjamin-cl--O84lhGc1OOI.txt]]"
tags: ["agents", "multi-agent", "agentes-orquestracao", "context-engineering", "knowledge-management", "evals", "stack-tooling", "agent-tooling", "token-budgeting", "harness", "analise", "arquitetura"]
thesis: "Agentes de IA devem ser projetados como 'agentes de conhecimento' — espelhando o design secular do trabalho intelectual humano (ferramentas de recuperação otimizadas + orquestração hierárquica com sub-agentes) — e não como agentes de código, pois conhecimento não-código é contextual, ambíguo e orientado por intenção, exigindo busca multimodal otimizada e decomposição de tarefas."
concepts: ["Agentes de conhecimento vs. agentes de código", "Trabalho do conhecimento: entrada é informação, saída é julgamento/decisão acionável", "Definição topológica: se precisa de busca, é um problema de conhecimento", "Código tem pistas duráveis e superfície grep-ável; conhecimento não-código é contextual e orientado por intenção", "Tarefas de programação são estreitas e pré-decompostas; conhecimento real exige decomposição autônoma", "Loop único de auto-otimização: novo conhecimento → novas ferramentas → novos fluxos e papéis → novos trabalhadores do conhecimento", "Ferramentas não são neutras: determinam se a tarefa é escalável e barata", "Otimização de baselines: existem centenas de variantes de BM25", "Harness híbrido (léxico + semântico)", "Busca multimodal direta sobre PDFs vs. OCR", "Padrão orquestrador + sub-agentes pesquisadores que retornam memos", "Oracle gap: lacuna entre documentos perfeitos e o sistema de busca", "Co-design de ferramentas com agentes: múltiplos primitivos de recuperação (grep, BM25, busca semântica)", "Contexto como recurso finito"]
tools: ["BM25", "grep", "RAG", "Claude Code", "Codex", "BrowseComp Plus", "MQA (benchmark Hugging Face/Snowflake)", "Gemini 3", "Mixbread search (busca multimodal)", "OCR", "Google", "Sistema Dewey", "Pinakes (catálogo da Biblioteca de Alexandria)"]
people: ["Ben Clavié (palestrante)", "Mixbread", "Hugging Face", "Snowflake", "Google", "Biblioteca de Alexandria"]
claims: ["Otimize sempre seus baselines: BM25 mal otimizado rende ~60% de acurácia no BrowseComp Plus, enquanto BM25 otimizado chega a 70-80%", "Um harness híbrido atinge ~98% no BrowseComp Plus com ~20% menos chamadas de ferramenta, gastando ~5% do custo do baseline não otimizado — a qualidade da ferramenta decide se o workflow vale a pena", "No MQA, humanos e Gemini 3 atingem o mesmo teto usando BM25: sem ferramenta melhor, nem humanos com buscas ilimitadas extraem a informação certa — a ferramenta define o limite, não o agente", "Substituir OCR por busca multimodal nativa sobre PDFs (tabelas, visão) dá um salto grande de acurácia em tarefas corporativas", "Arquitetura de orquestrador que decompõe o problema, escreve queries e despacha sub-agentes pesquisadores reduziu o oracle gap de ~10 para ~6 pontos (~40% menos erros) no MQA", "Agentes de código parecem capazes porque as tarefas de programação são estreitas e o usuário já fez a decomposição; conhecimento real exige que o próprio agente decomponha a intenção", "Treine o harness/modelo para conhecer múltiplos primitivos de busca (grep, BM25, semântica): agentes tendem a escrever queries grep/BM25 por viés dos dados de treino, mesmo quando é impossível 'greppear' um PDF", "Mesmo com contexto de 100 milhões de tokens, custo e volume de dados tornam janelas gigantes inviáveis; prefira orquestração de busca e decomposição de tarefas", "Adote ferramentas novas para quebrar tetos de desempenho (orquestração + ferramenta), não como melhorias marginais neutras", "Aprenda com indústrias maduras de conhecimento (jurídica, médica, acadêmica) para desenhar arquiteturas de agentes, pois nenhuma delas se parece com programação"]
deep_dive: "high"
deep_dive_reason: "Alta densidade de insight arquitetural acionável com dados de benchmarks (BrowseComp Plus, MQA), um padrão concreto de orquestrador+pesquisadores com métrica de oracle gap e diretrizes de co-design de ferramentas, diretamente relevante a harness, evals, context-engineering e orquestração multi-agente."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-from-coding-to-knowledge-work-agents-karan-vaidya-composio--xxfMT-bPEmU|From coding to Knowledge work agents — Karan Vaidya, Composio]]", "[[extracts/youtube/ai-learning/2026-09-11-agentic-engineering-working-with-ai-not-just-using-it-brendan-o-leary--BEKc4P87XKo|Agentic Engineering: Working With AI, Not Just Using It — Brendan O'Leary]]", "[[extracts/youtube/ai-learning/2026-09-11-ex-nasa-dev-reveals-his-agentic-engineering-workflow--xgkjtF89-44|Ex-NASA dev reveals his Agentic Engineering Workflow]]", "[[extracts/youtube/ai-learning/2026-09-11-why-enterprise-ai-adoption-is-slower-than-you-think-aaron-levie-box-harrison-cha--agSRMrhNTf4|Why Enterprise AI Adoption Is Slower Than You Think — Aaron Levie (Box) + Harrison Chase]]", "[[extracts/youtube/ai-learning/2026-09-15-your-agents-lack-context-here-s-how-to-fix-you-re-absolutely-right-brandon-wasel--KcVkq5L-0f0|Your agents lack context: Here's how to fix \"You're absolutely right!\" — Brandon Waselnuk, Unblocked]]", "[[extracts/youtube/ai-learning/2026-09-11-the-future-of-ai-agents-with-andrew-ng-interrupt-26--OaRhpwz_TGM|The Future of AI Agents with Andrew Ng | Interrupt 26]]", "[[extracts/youtube/ai-learning/2026-09-11-why-agentic-systems-need-ontologies-frank-coyle-uc-berkeley--Sir59K8ZDPU|Why Agentic Systems Need Ontologies — Frank Coyle, UC Berkeley]]", "[[extracts/youtube/ai-learning/2026-09-11-google-s-okf-the-new-way-to-structure-your-knowledge-for-agents--MY9F9K7wWX4|Google's OKF - The New Way to Structure Your Knowledge for Agents]]", "[[extracts/youtube/ai-learning/2026-09-11-ontology-in-ai-the-hidden-skill-that-makes-architecture-and-your-career-work--J0hj0ms2ddo|Ontology in AI: The Hidden Skill That Makes Architecture and Your Career Work]]"]
theme: "Agentic Coding com Evals"
---

# If we want them to do Knowledge Work, design them as Knowledge Agents — Benjamin Clavié, Mixedbread

## Tese
Agentes de IA devem ser projetados como 'agentes de conhecimento' — espelhando o design secular do trabalho intelectual humano (ferramentas de recuperação otimizadas + orquestração hierárquica com sub-agentes) — e não como agentes de código, pois conhecimento não-código é contextual, ambíguo e orientado por intenção, exigindo busca multimodal otimizada e decomposição de tarefas.

## Conceitos-chave
- Agentes de conhecimento vs. agentes de código
- Trabalho do conhecimento: entrada é informação, saída é julgamento/decisão acionável
- Definição topológica: se precisa de busca, é um problema de conhecimento
- Código tem pistas duráveis e superfície grep-ável; conhecimento não-código é contextual e orientado por intenção
- Tarefas de programação são estreitas e pré-decompostas; conhecimento real exige decomposição autônoma
- Loop único de auto-otimização: novo conhecimento → novas ferramentas → novos fluxos e papéis → novos trabalhadores do conhecimento
- Ferramentas não são neutras: determinam se a tarefa é escalável e barata
- Otimização de baselines: existem centenas de variantes de BM25
- Harness híbrido (léxico + semântico)
- Busca multimodal direta sobre PDFs vs. OCR
- Padrão orquestrador + sub-agentes pesquisadores que retornam memos
- Oracle gap: lacuna entre documentos perfeitos e o sistema de busca
- Co-design de ferramentas com agentes: múltiplos primitivos de recuperação (grep, BM25, busca semântica)
- Contexto como recurso finito

## Ferramentas & pessoas
**Ferramentas:** BM25, grep, RAG, Claude Code, Codex, BrowseComp Plus, MQA (benchmark Hugging Face/Snowflake), Gemini 3, Mixbread search (busca multimodal), OCR, Google, Sistema Dewey, Pinakes (catálogo da Biblioteca de Alexandria)

**Pessoas/orgs:** Ben Clavié (palestrante), Mixbread, Hugging Face, Snowflake, Google, Biblioteca de Alexandria

## Claims acionáveis
- Otimize sempre seus baselines: BM25 mal otimizado rende ~60% de acurácia no BrowseComp Plus, enquanto BM25 otimizado chega a 70-80%
- Um harness híbrido atinge ~98% no BrowseComp Plus com ~20% menos chamadas de ferramenta, gastando ~5% do custo do baseline não otimizado — a qualidade da ferramenta decide se o workflow vale a pena
- No MQA, humanos e Gemini 3 atingem o mesmo teto usando BM25: sem ferramenta melhor, nem humanos com buscas ilimitadas extraem a informação certa — a ferramenta define o limite, não o agente
- Substituir OCR por busca multimodal nativa sobre PDFs (tabelas, visão) dá um salto grande de acurácia em tarefas corporativas
- Arquitetura de orquestrador que decompõe o problema, escreve queries e despacha sub-agentes pesquisadores reduziu o oracle gap de ~10 para ~6 pontos (~40% menos erros) no MQA
- Agentes de código parecem capazes porque as tarefas de programação são estreitas e o usuário já fez a decomposição; conhecimento real exige que o próprio agente decomponha a intenção
- Treine o harness/modelo para conhecer múltiplos primitivos de busca (grep, BM25, semântica): agentes tendem a escrever queries grep/BM25 por viés dos dados de treino, mesmo quando é impossível 'greppear' um PDF
- Mesmo com contexto de 100 milhões de tokens, custo e volume de dados tornam janelas gigantes inviáveis; prefira orquestração de busca e decomposição de tarefas
- Adote ferramentas novas para quebrar tetos de desempenho (orquestração + ferramenta), não como melhorias marginais neutras
- Aprenda com indústrias maduras de conhecimento (jurídica, médica, acadêmica) para desenhar arquiteturas de agentes, pois nenhuma delas se parece com programação

> **Deep dive:** `high` — Alta densidade de insight arquitetural acionável com dados de benchmarks (BrowseComp Plus, MQA), um padrão concreto de orquestrador+pesquisadores com métrica de oracle gap e diretrizes de co-design de ferramentas, diretamente relevante a harness, evals, context-engineering e orquestração multi-agente.
