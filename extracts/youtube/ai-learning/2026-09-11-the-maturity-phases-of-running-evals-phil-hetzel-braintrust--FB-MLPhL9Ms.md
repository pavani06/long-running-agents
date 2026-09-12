---
title: "The maturity phases of running evals — Phil Hetzel, Braintrust"
type: "extract"
source: "youtube"
video_id: "FB-MLPhL9Ms"
url: "https://www.youtube.com/watch?v=FB-MLPhL9Ms"
channel: "AI Engineer"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-the-maturity-phases-of-running-evals-phil-hetzel-braintrust--FB-MLPhL9Ms.txt]]"
tags: ["evals", "agents", "observability", "tracing", "testes-qa", "verification", "state", "production", "agentic-coding", "error-handling", "token-budgeting", "agent-tooling"]
thesis: "A qualidade de agentes de IA evolui por um continuum de maturidade em evals — da checagem por 'vibes' com anotação humana justificada, escalando via LLM-as-judge e verificações determinísticas, até representar estado de sistemas externos em traces de produção que alimentam um flywheel de melhoria contínua."
concepts: ["Evals não são unit tests: cobertura exaustiva é inviável; comece pelos modos de falha de alto nível definidos por especialistas", "Primitivos de eval: task (agente/prompt sob teste), dataset de exemplos que iniciam a tarefa e scoring functions", "Anotação humana com thumbs up/down mais justificativa obrigatória para extrair conhecimento de domínio escalável depois via LLM-as-judge", "Meta-avaliação: avaliar o próprio LLM juiz contra decisões humanas (saídas discretas permitem dataset de ground truth)", "Verificações determinísticas por código para modos de falha objetivos (excesso de tool calls, excesso de tokens)", "Flywheel de evals: capturar traces de produção, diagnosticar falhas, reinjetar exemplos no ambiente offline e 'rerodar produção' como eval", "Duas categorias de tool calls: context-gathering (injetam dados no LLM) versus CRUD (criam/lêem/atualizam/deletam em sistemas externos)", "Avaliação de trace completo do agente em vez de só a saída final quando há integrações externas", "Encapsular estado de sistemas externos dentro de traces arbitrariamente grandes para viabilizar eval offline", "Consultas de timestamp/versão em vector databases para reproduzir o estado no momento da criação do input", "Mock APIs para aproximar sistemas de produção em evals sem sobrescrever dados reais", "Views de anotação customizadas por domínio em vez de plataformas genéricas de anotação", "Topic modeling em escala para descobrir modos de falha automaticamente em produção", "Evals como defesa (risco reputacional, custo, compliance) e como ofensa (medir ganho de cada tweak)"]
tools: ["Braintrust", "KPMG", "Slalom Consulting", "Databricks", "Cursor", "Claude Code", "Codex", "MCP", "LLM-as-judge", "vector database", "eval provider CLI"]
people: ["Phil Hzel", "Braintrust", "KPMG", "Slalom Consulting"]
claims: ["Comece evals pelos modos de falha indicados por especialistas em vez de tentar cobertura exaustiva estilo unit test", "Exija que anotadores humanos registrem justificativa junto ao thumbs up/down para transferir conhecimento de domínio a um futuro LLM-as-judge", "Avalie os LLM juízes comparando-os às decisões humanas; como suas saídas são discretas, é possível montar ground truth para isso", "Use código determinístico para falhas objetivas como número excessivo de tool calls ou consumo de tokens", "Capture traces de produção ou UAT no dataset de eval e trate eval como rerodar produção, não como rodar testes", "Diferencie tools de context-gathering de tools CRUD no planejamento de evals, pois CRUD exige reproduzir estado externo e proteger dados de produção", "Encapsule o estado dos sistemas externos no próprio trace do agente (que pode ser arbitrariamente grande) para evitar construir infraestrutura de teste dedicada", "Use queries de timestamp/versão no vector database para representar fielmente o estado no momento original da execução", "Construa views de anotação específicas ao domínio do usuário em vez de plataformas genéricas para elevar a qualidade da anotação", "Padrões emergentes: topic modeling em escala para descobrir modos de falha em produção e automação de evals via Claude Code e eval provider CLI"]
deep_dive: "medium"
deep_dive_reason: "Oferece um framework de maturidade de evals com táticas acionáveis (flywheel de traces de produção, encapsulamento de estado externo no trace, meta-avaliação de LLM juízes), mas o tratamento é introdutório, parcialmente promocional e sem profundidade arquitetural ou novidade significativa."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-don-t-ship-skills-without-evals-philipp-schmid-google-deepmind--0vphxNt4wyk|Don't Ship Skills Without Evals — Philipp Schmid, Google DeepMind]]", "[[extracts/youtube/ai-learning/2026-09-11-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipeline--Uny6LpmjraI|Inside Clay's Eval Stack: 300M Agent Runs, One LangSmith Pipeline]]", "[[extracts/youtube/ai-learning/2026-09-11-agentic-evaluations-at-scale-for-everybody-nicholas-kang-michael-aaron-google-de--Ubwb6NzegyA|Agentic Evaluations at Scale, For Everybody — Nicholas Kang & Michael Aaron, Google DeepMind]]", "[[extracts/youtube/ai-learning/2026-09-11-building-and-evaluating-ai-agents-sayash-kapoor-ai-snake-oil--d5EltXhbcfA|Building and evaluating AI Agents — Sayash Kapoor, AI Snake Oil]]", "[[extracts/youtube/ai-learning/2026-09-11-the-production-ai-playbook-deploying-agents-at-enterprise-scale-sandipan-bhaumik--ObTPqBGsEbA|The Production AI Playbook: Deploying Agents at Enterprise Scale — Sandipan Bhaumik, Databricks]]", "[[extracts/youtube/ai-learning/2026-09-11-anthropic-workshop-build-agents-that-run-for-hours-ash-prabaker-andrew-wilson--mR-WAvEPRwE|Anthropic Workshop: Build Agents That Run for Hours — Ash Prabaker & Andrew Wilson]]", "[[extracts/youtube/ai-learning/2026-09-11-building-closed-loop-evals-for-a-multimodal-agent-at-scale-soumya-gupta-jai-chop--31GUkCBD-Uc|Building Closed-Loop Evals for a Multimodal Agent at Scale — Soumya Gupta & Jai Chopra, Uber]]"]
---

# The maturity phases of running evals — Phil Hetzel, Braintrust

## Tese
A qualidade de agentes de IA evolui por um continuum de maturidade em evals — da checagem por 'vibes' com anotação humana justificada, escalando via LLM-as-judge e verificações determinísticas, até representar estado de sistemas externos em traces de produção que alimentam um flywheel de melhoria contínua.

## Conceitos-chave
- Evals não são unit tests: cobertura exaustiva é inviável; comece pelos modos de falha de alto nível definidos por especialistas
- Primitivos de eval: task (agente/prompt sob teste), dataset de exemplos que iniciam a tarefa e scoring functions
- Anotação humana com thumbs up/down mais justificativa obrigatória para extrair conhecimento de domínio escalável depois via LLM-as-judge
- Meta-avaliação: avaliar o próprio LLM juiz contra decisões humanas (saídas discretas permitem dataset de ground truth)
- Verificações determinísticas por código para modos de falha objetivos (excesso de tool calls, excesso de tokens)
- Flywheel de evals: capturar traces de produção, diagnosticar falhas, reinjetar exemplos no ambiente offline e 'rerodar produção' como eval
- Duas categorias de tool calls: context-gathering (injetam dados no LLM) versus CRUD (criam/lêem/atualizam/deletam em sistemas externos)
- Avaliação de trace completo do agente em vez de só a saída final quando há integrações externas
- Encapsular estado de sistemas externos dentro de traces arbitrariamente grandes para viabilizar eval offline
- Consultas de timestamp/versão em vector databases para reproduzir o estado no momento da criação do input
- Mock APIs para aproximar sistemas de produção em evals sem sobrescrever dados reais
- Views de anotação customizadas por domínio em vez de plataformas genéricas de anotação
- Topic modeling em escala para descobrir modos de falha automaticamente em produção
- Evals como defesa (risco reputacional, custo, compliance) e como ofensa (medir ganho de cada tweak)

## Ferramentas & pessoas
**Ferramentas:** Braintrust, KPMG, Slalom Consulting, Databricks, Cursor, Claude Code, Codex, MCP, LLM-as-judge, vector database, eval provider CLI

**Pessoas/orgs:** Phil Hzel, Braintrust, KPMG, Slalom Consulting

## Claims acionáveis
- Comece evals pelos modos de falha indicados por especialistas em vez de tentar cobertura exaustiva estilo unit test
- Exija que anotadores humanos registrem justificativa junto ao thumbs up/down para transferir conhecimento de domínio a um futuro LLM-as-judge
- Avalie os LLM juízes comparando-os às decisões humanas; como suas saídas são discretas, é possível montar ground truth para isso
- Use código determinístico para falhas objetivas como número excessivo de tool calls ou consumo de tokens
- Capture traces de produção ou UAT no dataset de eval e trate eval como rerodar produção, não como rodar testes
- Diferencie tools de context-gathering de tools CRUD no planejamento de evals, pois CRUD exige reproduzir estado externo e proteger dados de produção
- Encapsule o estado dos sistemas externos no próprio trace do agente (que pode ser arbitrariamente grande) para evitar construir infraestrutura de teste dedicada
- Use queries de timestamp/versão no vector database para representar fielmente o estado no momento original da execução
- Construa views de anotação específicas ao domínio do usuário em vez de plataformas genéricas para elevar a qualidade da anotação
- Padrões emergentes: topic modeling em escala para descobrir modos de falha em produção e automação de evals via Claude Code e eval provider CLI

> **Deep dive:** `medium` — Oferece um framework de maturidade de evals com táticas acionáveis (flywheel de traces de produção, encapsulamento de estado externo no trace, meta-avaliação de LLM juízes), mas o tratamento é introdutório, parcialmente promocional e sem profundidade arquitetural ou novidade significativa.
