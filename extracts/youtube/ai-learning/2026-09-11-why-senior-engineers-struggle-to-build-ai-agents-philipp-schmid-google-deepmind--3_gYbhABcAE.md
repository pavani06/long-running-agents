---
title: "Why (Senior) Engineers Struggle to Build AI Agents — Philipp Schmid, Google DeepMind"
type: "extract"
source: "youtube"
video_id: "3_gYbhABcAE"
url: "https://www.youtube.com/watch?v=3_gYbhABcAE"
channel: "AI Engineer"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-why-senior-engineers-struggle-to-build-ai-agents-philipp-schmid-google-deepmind--3_gYbhABcAE.txt]]"
tags: ["agents", "agent-loop", "agent-tooling", "context-engineering", "error-handling", "evals", "tracing", "state", "process", "production"]
thesis: "Engenheiros lutam para construir agentes porque aplicam práticas de software determinístico (estruturas de dados rígidas, fluxos predefinidos, retentes do zero, testes unitários, APIs para humanos) em vez de práticas agent-nativas: texto como estado, delegação de controle, erros como input, evals e ferramentas auto-documentadas."
concepts: ["texto como novo estado (semantic meaning vs data structures)", "delegar controle (dispatcher vs traffic controller)", "definir objetivo em vez de passos exatos", "erros como inputs normais (padrão error-or-value do Go)", "preservar contexto/compute em agentes de longa duração (não reiniciar o fluxo)", "transição de unit/integration tests para evals", "não-determinismo e taxa de sucesso estatística", "resultados subjetivos e LLM-as-judge ou especialista humano", "tracing e avaliação por outcome em vez de passos idênticos", "APIs/tools agent-ready com interfaces semânticas e auto-documentadas", "agentes só veem schemas, docstrings e tool definitions, não o código", "iterative loop de prompt/tool adjustment", "trust but verify", "design for recovery", "build to delete / software é descartável / bitter lesson", "personalização e memória baseada em preferência textual (ex.: Celsius vs Fahrenheit)", "aprovação de planos com feedback semântico livre em vez de flags accept/deny"]
tools: ["Gemini", "Gemini API", "Deep Research (agente de deep research)"]
people: ["Phillip (speaker, DeepMind)", "Google", "DeepMind"]
claims: ["Substitua gates binários (accept/deny) por gates textuais: aprove o plano do agente e ao mesmo tempo forneça restrições semânticas adicionais, eliminando idas-e-voltas de fluxo", "Não force o modelo em um workflow fixo de passo 1, passo 2; defina o objetivo e deixe o agente escolher o caminho", "Trate erros como inputs do modelo: alimente a falha de volta com workarounds e verificações para continuar o fluxo em vez de reiniciar tudo e perder compute/contexto acumulado", "Meça agentes por evals de taxa de sucesso (ex.: quantas de N execuções passam), não por asserts determinísticos de entrada A → saída C", "Como outputs são subjetivos, use LLM-as-judge ou especialistas humanos para qualificar resultados e avalie o outcome final, tolerando número variável de passos e tokens por execução", "Só leve agentes a produção quando a taxa de sucesso for confiável; 1 acerto em 10 é flaky demais", "Reescreva APIs/tools para agentes: docstrings e schemas semânticos completos (o que é o ID, o que acontece em falha) porque o agente não tem o contexto de quem construiu a API", "Sempre rastreie (trace) o que o agente faz, mas grade no resultado final", "Projete para recuperação: em agentes de longa duração coisas estranhas vão acontecer e o sistema deve se recuperar", "Construa para deletar: software de agentes é descartável e será reconstruído muitas vezes com modelos melhores"]
deep_dive: "medium"
deep_dive_reason: "Palestra introdutória com cinco princípios práticos acionáveis sobre estado, erros e evals, mas de alto nível e sem novidade arquitetural ou detalhes de implementação para quem já acompanha o campo."
---

# Why (Senior) Engineers Struggle to Build AI Agents — Philipp Schmid, Google DeepMind

## Tese
Engenheiros lutam para construir agentes porque aplicam práticas de software determinístico (estruturas de dados rígidas, fluxos predefinidos, retentes do zero, testes unitários, APIs para humanos) em vez de práticas agent-nativas: texto como estado, delegação de controle, erros como input, evals e ferramentas auto-documentadas.

## Conceitos-chave
- texto como novo estado (semantic meaning vs data structures)
- delegar controle (dispatcher vs traffic controller)
- definir objetivo em vez de passos exatos
- erros como inputs normais (padrão error-or-value do Go)
- preservar contexto/compute em agentes de longa duração (não reiniciar o fluxo)
- transição de unit/integration tests para evals
- não-determinismo e taxa de sucesso estatística
- resultados subjetivos e LLM-as-judge ou especialista humano
- tracing e avaliação por outcome em vez de passos idênticos
- APIs/tools agent-ready com interfaces semânticas e auto-documentadas
- agentes só veem schemas, docstrings e tool definitions, não o código
- iterative loop de prompt/tool adjustment
- trust but verify
- design for recovery
- build to delete / software é descartável / bitter lesson
- personalização e memória baseada em preferência textual (ex.: Celsius vs Fahrenheit)
- aprovação de planos com feedback semântico livre em vez de flags accept/deny

## Ferramentas & pessoas
**Ferramentas:** Gemini, Gemini API, Deep Research (agente de deep research)

**Pessoas/orgs:** Phillip (speaker, DeepMind), Google, DeepMind

## Claims acionáveis
- Substitua gates binários (accept/deny) por gates textuais: aprove o plano do agente e ao mesmo tempo forneça restrições semânticas adicionais, eliminando idas-e-voltas de fluxo
- Não force o modelo em um workflow fixo de passo 1, passo 2; defina o objetivo e deixe o agente escolher o caminho
- Trate erros como inputs do modelo: alimente a falha de volta com workarounds e verificações para continuar o fluxo em vez de reiniciar tudo e perder compute/contexto acumulado
- Meça agentes por evals de taxa de sucesso (ex.: quantas de N execuções passam), não por asserts determinísticos de entrada A → saída C
- Como outputs são subjetivos, use LLM-as-judge ou especialistas humanos para qualificar resultados e avalie o outcome final, tolerando número variável de passos e tokens por execução
- Só leve agentes a produção quando a taxa de sucesso for confiável; 1 acerto em 10 é flaky demais
- Reescreva APIs/tools para agentes: docstrings e schemas semânticos completos (o que é o ID, o que acontece em falha) porque o agente não tem o contexto de quem construiu a API
- Sempre rastreie (trace) o que o agente faz, mas grade no resultado final
- Projete para recuperação: em agentes de longa duração coisas estranhas vão acontecer e o sistema deve se recuperar
- Construa para deletar: software de agentes é descartável e será reconstruído muitas vezes com modelos melhores

> **Deep dive:** `medium` — Palestra introdutória com cinco princípios práticos acionáveis sobre estado, erros e evals, mas de alto nível e sem novidade arquitetural ou detalhes de implementação para quem já acompanha o campo.
