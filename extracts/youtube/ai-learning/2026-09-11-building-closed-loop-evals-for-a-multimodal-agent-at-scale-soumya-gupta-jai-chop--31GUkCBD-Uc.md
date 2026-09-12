---
title: "Building Closed-Loop Evals for a Multimodal Agent at Scale — Soumya Gupta & Jai Chopra, Uber"
type: "extract"
source: "youtube"
video_id: "31GUkCBD-Uc"
url: "https://www.youtube.com/watch?v=31GUkCBD-Uc"
channel: "AI Engineer"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-building-closed-loop-evals-for-a-multimodal-agent-at-scale-soumya-gupta-jai-chop--31GUkCBD-Uc.txt]]"
tags: ["evals", "agents", "multi-agent", "agent-loop", "gate-design", "observability", "tracing", "monitoramento", "verification", "error-handling", "production", "arquitetura", "model-selection", "decision-discipline"]
thesis: "A Uber Eats opera um sistema multiagente de produção para aprimoramento de fotos de merchants cuja confiabilidade vem de um design orientado por evals — gates por estágio, golden dataset alinhado a labels humanos e um loop de autotuning totalmente automatizado (diagnoser + reflect/synthesize) que corrige drift continuamente sem humano no loop."
concepts: ["agente de roteamento (enhance vs. skip) com saída estruturada de LLM multimodal", "matriz de confusão e precision/recall como eval do router (métrica guardrail: recall)", "matriz N×N para roteamento multirramo com trade-off de custo/latência entre modelos", "golden dataset com labels humanos e diretrizes objetivas para reduzir viés dos labelers", "autotuning de config via sub-agentes reflect (remove ruído, acha problemas sistêmicos) e synthesize (reescreve config, faz benchmark, registra nova versão)", "agente diagnóstico que generaliza múltiplos loops de feedback e roteia a otimização para o agente certo", "pass@K como métrica do loop de edição com auto-correção via feedback do QA", "avaliação por comparação pairwise (input vs. output) com rubrica alinhada a product design, policy e legal", "rubrica de qualidade: faithfulness, completeness, naturalness, realism (saída yes/no/unsure)", "modelo Swiss cheese de gates redundantes de QA antes de publicar", "reward hacking em edição de imagem (oversteering para edição genérica conservadora)", "fragilidades de frontier models (coerência de objetos, plausibilidade física) vazando para o caso aplicado", "logging-first: JSON plano de toda a orquestração, legível por times técnicos e não técnicos", "drift contínuo: modelo estático offline não sobrevive em produção; amostragem regular de dados reais vs. labels humanos", "loops de feedback: model loop, dogfooding (thumbs up/down + texto livre) e métricas de produção fatiadas por geo/dispositivo/tipo de prato"]
tools: ["Uber Eats", "Arize", "agent config store", "modelos frontier de edição de imagem"]
people: ["Uber", "Jay", "Sam (Sia)", "Arize"]
claims: ["Comece pelo logging antes de qualquer otimização: um JSON plano único para toda a orquestração permite diagnóstico caso a caso e análise agregada por qualquer pessoa do time", "Trate labels humanos como golden source of truth e construa dataset representativo (geos, tipos de prato, qualidade de imagem) com diretrizes objetivas para eliminar ruído dos labelers", "Use recall como métrica guardrail do router para garantir que nenhuma imagem ruim passe pelo sistema", "Amostre dados de produção em cadência regular e compare com labels humanos para detectar drift; um modelo estático treinado offline não funciona em produção", "Implemente o autotuning como sistema fechado sem humano no loop: agente de diagnóstico localiza o problema, sub-agentes reflect/synthesize reescrevem a config, benchmark contra o golden dataset e registro automático da nova versão — com observabilidade, guardrails e rollback rápido embutidos", "Meça loops de auto-correção de edição com pass@K: a taxa de aprovação deve crescer com as iterações conforme o feedback do QA entra", "Defina 'melhor imagem' via comparação pairwise com rubrica alinhada entre product design, policy e legal antes de codificar em evals", "Aplique o modelo Swiss cheese: redundância deliberada de gates de QA reduz a probabilidade de falha chegar à produção", "Monitore reward hacking: após rejeição de uma edição criativa, o agente pode oversteerar para edições genéricas e conservadoras sem melhoria real", "Use verificação multimodal: quando o modelo não consegue confirmar o conteúdo (ex.: contar 8 wontons), retorne 'unsure' e rejeite em produção", "Problemas de frontier models (coerência de objetos, plausibilidade física) vazam para o caso aplicado; coordene com os times dos modelos", "Roteie imagens para modelos menores e de menor latência quando o trade-off custo/qualidade for aceitável, avaliando com matriz de confusão N×N", "Generalize a ingestão de feedback com um diagnoser que recebe qualquer fonte (dogfooding, métricas de produção, labels) e roteia a correção para o agente específico", "Fatie métricas de produção (conversão, add-to-cart) por geo, dispositivo e tipo de prato para identificar e afinar ganhos por segmento"]
deep_dive: "high"
deep_dive_reason: "Alta densidade de insight arquitetural acionável e novel (loop de autotuning fechado com reflect/synthesize, abstração do diagnoser, pass@K, gates redundantes tipo Swiss cheese, exemplos de reward hacking) diretamente aplicável a harness, evals e operação de agentes em produção."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-the-art-of-loop-engineering-how-to-build-agents-that-improve-over-time--jPPiZ22DY3g|The Art of Loop Engineering: How to Build Agents That Improve Over Time]]", "[[extracts/youtube/ai-learning/2026-09-11-the-production-ai-playbook-deploying-agents-at-enterprise-scale-sandipan-bhaumik--ObTPqBGsEbA|The Production AI Playbook: Deploying Agents at Enterprise Scale — Sandipan Bhaumik, Databricks]]", "[[extracts/youtube/ai-learning/2026-09-11-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipeline--Uny6LpmjraI|Inside Clay's Eval Stack: 300M Agent Runs, One LangSmith Pipeline]]", "[[extracts/youtube/ai-learning/2026-09-11-the-maturity-phases-of-running-evals-phil-hetzel-braintrust--FB-MLPhL9Ms|The maturity phases of running evals — Phil Hetzel, Braintrust]]", "[[extracts/youtube/ai-learning/2026-09-11-the-multi-agent-architecture-that-actually-ships-luke-alvoeiro-factory--ow1we5PzK-o|The Multi-Agent Architecture That Actually Ships — Luke Alvoeiro, Factory]]", "[[extracts/youtube/ai-learning/2026-09-11-scaling-agents-for-gen-ai-products-anju-kambadur-bloomberg-head-of-ai-engineerin--b2GqTDWtg6s|Scaling Agents for Gen AI Products - Anju Kambadur, Bloomberg Head of AI Engineering]]", "[[extracts/youtube/ai-learning/2026-09-11-building-production-ready-rag-applications-jerry-liu--TRjq7t2Ms5I|Building Production-Ready RAG Applications: Jerry Liu]]"]
---

# Building Closed-Loop Evals for a Multimodal Agent at Scale — Soumya Gupta & Jai Chopra, Uber

## Tese
A Uber Eats opera um sistema multiagente de produção para aprimoramento de fotos de merchants cuja confiabilidade vem de um design orientado por evals — gates por estágio, golden dataset alinhado a labels humanos e um loop de autotuning totalmente automatizado (diagnoser + reflect/synthesize) que corrige drift continuamente sem humano no loop.

## Conceitos-chave
- agente de roteamento (enhance vs. skip) com saída estruturada de LLM multimodal
- matriz de confusão e precision/recall como eval do router (métrica guardrail: recall)
- matriz N×N para roteamento multirramo com trade-off de custo/latência entre modelos
- golden dataset com labels humanos e diretrizes objetivas para reduzir viés dos labelers
- autotuning de config via sub-agentes reflect (remove ruído, acha problemas sistêmicos) e synthesize (reescreve config, faz benchmark, registra nova versão)
- agente diagnóstico que generaliza múltiplos loops de feedback e roteia a otimização para o agente certo
- pass@K como métrica do loop de edição com auto-correção via feedback do QA
- avaliação por comparação pairwise (input vs. output) com rubrica alinhada a product design, policy e legal
- rubrica de qualidade: faithfulness, completeness, naturalness, realism (saída yes/no/unsure)
- modelo Swiss cheese de gates redundantes de QA antes de publicar
- reward hacking em edição de imagem (oversteering para edição genérica conservadora)
- fragilidades de frontier models (coerência de objetos, plausibilidade física) vazando para o caso aplicado
- logging-first: JSON plano de toda a orquestração, legível por times técnicos e não técnicos
- drift contínuo: modelo estático offline não sobrevive em produção; amostragem regular de dados reais vs. labels humanos
- loops de feedback: model loop, dogfooding (thumbs up/down + texto livre) e métricas de produção fatiadas por geo/dispositivo/tipo de prato

## Ferramentas & pessoas
**Ferramentas:** Uber Eats, Arize, agent config store, modelos frontier de edição de imagem

**Pessoas/orgs:** Uber, Jay, Sam (Sia), Arize

## Claims acionáveis
- Comece pelo logging antes de qualquer otimização: um JSON plano único para toda a orquestração permite diagnóstico caso a caso e análise agregada por qualquer pessoa do time
- Trate labels humanos como golden source of truth e construa dataset representativo (geos, tipos de prato, qualidade de imagem) com diretrizes objetivas para eliminar ruído dos labelers
- Use recall como métrica guardrail do router para garantir que nenhuma imagem ruim passe pelo sistema
- Amostre dados de produção em cadência regular e compare com labels humanos para detectar drift; um modelo estático treinado offline não funciona em produção
- Implemente o autotuning como sistema fechado sem humano no loop: agente de diagnóstico localiza o problema, sub-agentes reflect/synthesize reescrevem a config, benchmark contra o golden dataset e registro automático da nova versão — com observabilidade, guardrails e rollback rápido embutidos
- Meça loops de auto-correção de edição com pass@K: a taxa de aprovação deve crescer com as iterações conforme o feedback do QA entra
- Defina 'melhor imagem' via comparação pairwise com rubrica alinhada entre product design, policy e legal antes de codificar em evals
- Aplique o modelo Swiss cheese: redundância deliberada de gates de QA reduz a probabilidade de falha chegar à produção
- Monitore reward hacking: após rejeição de uma edição criativa, o agente pode oversteerar para edições genéricas e conservadoras sem melhoria real
- Use verificação multimodal: quando o modelo não consegue confirmar o conteúdo (ex.: contar 8 wontons), retorne 'unsure' e rejeite em produção
- Problemas de frontier models (coerência de objetos, plausibilidade física) vazam para o caso aplicado; coordene com os times dos modelos
- Roteie imagens para modelos menores e de menor latência quando o trade-off custo/qualidade for aceitável, avaliando com matriz de confusão N×N
- Generalize a ingestão de feedback com um diagnoser que recebe qualquer fonte (dogfooding, métricas de produção, labels) e roteia a correção para o agente específico
- Fatie métricas de produção (conversão, add-to-cart) por geo, dispositivo e tipo de prato para identificar e afinar ganhos por segmento

> **Deep dive:** `high` — Alta densidade de insight arquitetural acionável e novel (loop de autotuning fechado com reflect/synthesize, abstração do diagnoser, pass@K, gates redundantes tipo Swiss cheese, exemplos de reward hacking) diretamente aplicável a harness, evals e operação de agentes em produção.
