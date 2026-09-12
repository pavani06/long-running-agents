---
title: "Jeff Dean: The 1% Rule for Building in AI"
type: "extract"
source: "youtube"
video_id: "CxXgV54KzpQ"
url: "https://www.youtube.com/watch?v=CxXgV54KzpQ"
channel: "Y Combinator"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-jeff-dean-the-1-rule-for-building-in-ai--CxXgV54KzpQ.txt]]"
tags: ["agents", "agent-fleets", "agent-loop", "agent-tooling", "agentic-coding", "multi-agent", "context-engineering", "harness", "evals", "spec-driven-development", "model-selection", "arquitetura", "runtime", "decision-discipline", "verification", "knowledge-management", "error-handling"]
thesis: "Jeff Dean defende que o futuro próximo dos sistemas de IA está menos nos modelos gerais e mais no que os rodeia — context engineering com skills e harnesses, hardware especializado de inferência de baixa latência e baixa energia, e avaliadores rápidos que viabilizam loops automatizados de experimentação capazes de rodar por dias ou semanas — com a habilidade escassa sendo o 'gosto' para especificar e selecionar o que as frotas de agentes devem fazer."
concepts: ["context engineering", "skills para modelos (diretrizes de uso de ferramentas)", "harness de agentes", "orquestração multi-agente com agente avaliador", "inference-time compute / busca sobre abordagens plausíveis", "degradação fora-da-distribuição em agentes de longa duração", "napkin math (cálculos de guardanapo)", "especialização de hardware para inferência", "eficiência energética por operação (1 picojoule vs ~1000x para mover dados)", "batching e epochs como problema de IO/dados, não de modelo", "compressão como proxy de compreensão", "avaliadores surrogate neurais (aproximações de simuladores caros)", "loop automatizado de experimentação (método científico acelerado)", "auto-melhoramento recursivo de ML", "distilação de modelos (teacher para student)", "tradução de código entre linguagens como spec perfeita", "taste / seleção de problemas como habilidade escassa", "confiabilidade construída sobre componentes não-confiáveis (replicação, Reed-Solomon, transistores com erros)", "microbenchmarks e auto-melhoria de performance de código"]
tools: ["TPU", "MapReduce", "BigTable", "TensorFlow", "Google Search", "Gemini", "Gemini Flash / Gemini Pro", "AlphaFold", "AlphaChip", "AlphaEvolve", "Python", "Go", "biblioteca interna de microbenchmarks do Google", "documento 'Performance Hints' (Jeff Dean e Sanjay, ~30 páginas, público)", "simulador de teoria do funcional da densidade (DFT)", "arXiv"]
people: ["Jeff Dean", "Sanjay Ghemawat", "Geoffrey Hinton", "Oriol Vinyals (transcrito como 'Oral Fin')", "Google", "Google DeepMind", "AI Ascent (evento)"]
claims: ["Agentes apoiados em modelos altamente capazes já conseguem executar por dias ou semanas em tarefas complexas, como reimplementar software em outra linguagem com melhores propriedades de segurança ou performance", "Latência de inferência é o gargalo para popularizar agentes; hardware especializado pode entregar melhorias de até ~50x em latência", "O TPU, especializado em álgebra linear densa de baixa precisão, foi 30-80x mais eficiente energeticamente e 20-30x mais rápido em latência que CPUs/GPUs da época", "Mover dados custa ~1000x mais energia que computar, o que obriga batching de tokens/exemplos e molda decisões de treino (batching, epochs) e de inferência", "Context engineering é acessível a qualquer pessoa com acesso a uma API: observe onde o modelo falha e escreva skills/guidelines que codificam a abordagem humana para mantê-lo no caminho que ele domina", "Para agentes de longa duração, rode múltiplos agentes com abordagens diferentes e use um modelo/agente avaliador com inference-time compute para descartar trajetórias que saem dos trilhos", "No ambiente interno do Google, skills que ensinam agentes a usar ferramentas proprietárias (busca de logs, code review, medição de performance) tornam agentes úteis sem retreino do modelo", "Um skill escrito por Jeff e Sanjay ensina o agente a rodar microbenchmarks, alterar código, medir ganhos e iterar, replicando o loop humano de otimização de performance", "O documento público 'Performance Hints', resumido e dado ao modelo, melhora o raciocínio deste sobre performance de código", "Ao escolher problema de startup, prefira domínios onde o modelo geral acerta 0-1% das vezes; sucesso parcial (~20%) indica que o modelo de fronteira absorverá a capacidade em 6-12 meses", "Vantagens duráveis vêm de dados que o modelo geral não acessa (ex.: organização de informações pessoais do usuário) ou de modelos de nicho baratos de treinar e altamente acurados (padrão AlphaFold, materiais, design de chips)", "Gerenciar frotas de 50-100 agentes exige design docs/specs nítidos; especificação clara importa mais com agentes do que com humanos, pois o agente infere o que você quis dizer", "Tradução de código entre linguagens (ex.: Python para Go) com tradução dos testes e comparação comportamental até eliminarem-se diferenças é hoje um dos usos mais eficazes de agentes de coding", "A habilidade escassa quando todos rodam centenas de agentes será o taste de escolher o que pedir; treine-o listando previsões de 12 meses e auditando depois quais se materializaram", "Aproximações neurais de avaliadores caros (ex.: 300.000x mais rápido que simulação DFT, quase tão acuradas) transformam a velocidade dos loops experimentais em ciência e ML", "Distilação — paper rejeitado por 'improvável impacto significativo' — é hoje técnica central, usada para gerar Gemini Flash a partir do Pro; rejeição não prediz impacto", "Pensamento de primeira ordem: questione pressupostos de projeto (ex.: transistores com 20 erros/dia com redundância em nível superior) e busque soluções 1-2 ordens de magnitude melhores em vez de otimizar a abordagem atual"]
deep_dive: "high"
deep_dive_reason: "Alta densidade de insight acionável de um praticante de fronteira sobre harnesses, skills, busca multi-agente com avaliadores, specs para frotas de agentes e avaliadores surrogate, com detalhes internos do Google e heurísticas concretas de seleção de problemas que raramente aparecem em público."
---

# Jeff Dean: The 1% Rule for Building in AI

## Tese
Jeff Dean defende que o futuro próximo dos sistemas de IA está menos nos modelos gerais e mais no que os rodeia — context engineering com skills e harnesses, hardware especializado de inferência de baixa latência e baixa energia, e avaliadores rápidos que viabilizam loops automatizados de experimentação capazes de rodar por dias ou semanas — com a habilidade escassa sendo o 'gosto' para especificar e selecionar o que as frotas de agentes devem fazer.

## Conceitos-chave
- context engineering
- skills para modelos (diretrizes de uso de ferramentas)
- harness de agentes
- orquestração multi-agente com agente avaliador
- inference-time compute / busca sobre abordagens plausíveis
- degradação fora-da-distribuição em agentes de longa duração
- napkin math (cálculos de guardanapo)
- especialização de hardware para inferência
- eficiência energética por operação (1 picojoule vs ~1000x para mover dados)
- batching e epochs como problema de IO/dados, não de modelo
- compressão como proxy de compreensão
- avaliadores surrogate neurais (aproximações de simuladores caros)
- loop automatizado de experimentação (método científico acelerado)
- auto-melhoramento recursivo de ML
- distilação de modelos (teacher para student)
- tradução de código entre linguagens como spec perfeita
- taste / seleção de problemas como habilidade escassa
- confiabilidade construída sobre componentes não-confiáveis (replicação, Reed-Solomon, transistores com erros)
- microbenchmarks e auto-melhoria de performance de código

## Ferramentas & pessoas
**Ferramentas:** TPU, MapReduce, BigTable, TensorFlow, Google Search, Gemini, Gemini Flash / Gemini Pro, AlphaFold, AlphaChip, AlphaEvolve, Python, Go, biblioteca interna de microbenchmarks do Google, documento 'Performance Hints' (Jeff Dean e Sanjay, ~30 páginas, público), simulador de teoria do funcional da densidade (DFT), arXiv

**Pessoas/orgs:** Jeff Dean, Sanjay Ghemawat, Geoffrey Hinton, Oriol Vinyals (transcrito como 'Oral Fin'), Google, Google DeepMind, AI Ascent (evento)

## Claims acionáveis
- Agentes apoiados em modelos altamente capazes já conseguem executar por dias ou semanas em tarefas complexas, como reimplementar software em outra linguagem com melhores propriedades de segurança ou performance
- Latência de inferência é o gargalo para popularizar agentes; hardware especializado pode entregar melhorias de até ~50x em latência
- O TPU, especializado em álgebra linear densa de baixa precisão, foi 30-80x mais eficiente energeticamente e 20-30x mais rápido em latência que CPUs/GPUs da época
- Mover dados custa ~1000x mais energia que computar, o que obriga batching de tokens/exemplos e molda decisões de treino (batching, epochs) e de inferência
- Context engineering é acessível a qualquer pessoa com acesso a uma API: observe onde o modelo falha e escreva skills/guidelines que codificam a abordagem humana para mantê-lo no caminho que ele domina
- Para agentes de longa duração, rode múltiplos agentes com abordagens diferentes e use um modelo/agente avaliador com inference-time compute para descartar trajetórias que saem dos trilhos
- No ambiente interno do Google, skills que ensinam agentes a usar ferramentas proprietárias (busca de logs, code review, medição de performance) tornam agentes úteis sem retreino do modelo
- Um skill escrito por Jeff e Sanjay ensina o agente a rodar microbenchmarks, alterar código, medir ganhos e iterar, replicando o loop humano de otimização de performance
- O documento público 'Performance Hints', resumido e dado ao modelo, melhora o raciocínio deste sobre performance de código
- Ao escolher problema de startup, prefira domínios onde o modelo geral acerta 0-1% das vezes; sucesso parcial (~20%) indica que o modelo de fronteira absorverá a capacidade em 6-12 meses
- Vantagens duráveis vêm de dados que o modelo geral não acessa (ex.: organização de informações pessoais do usuário) ou de modelos de nicho baratos de treinar e altamente acurados (padrão AlphaFold, materiais, design de chips)
- Gerenciar frotas de 50-100 agentes exige design docs/specs nítidos; especificação clara importa mais com agentes do que com humanos, pois o agente infere o que você quis dizer
- Tradução de código entre linguagens (ex.: Python para Go) com tradução dos testes e comparação comportamental até eliminarem-se diferenças é hoje um dos usos mais eficazes de agentes de coding
- A habilidade escassa quando todos rodam centenas de agentes será o taste de escolher o que pedir; treine-o listando previsões de 12 meses e auditando depois quais se materializaram
- Aproximações neurais de avaliadores caros (ex.: 300.000x mais rápido que simulação DFT, quase tão acuradas) transformam a velocidade dos loops experimentais em ciência e ML
- Distilação — paper rejeitado por 'improvável impacto significativo' — é hoje técnica central, usada para gerar Gemini Flash a partir do Pro; rejeição não prediz impacto
- Pensamento de primeira ordem: questione pressupostos de projeto (ex.: transistores com 20 erros/dia com redundância em nível superior) e busque soluções 1-2 ordens de magnitude melhores em vez de otimizar a abordagem atual

> **Deep dive:** `high` — Alta densidade de insight acionável de um praticante de fronteira sobre harnesses, skills, busca multi-agente com avaliadores, specs para frotas de agentes e avaliadores surrogate, com detalhes internos do Google e heurísticas concretas de seleção de problemas que raramente aparecem em público.
