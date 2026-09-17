---
title: "How Decagon Runs 90% of Its Agents on Open-Source Models"
type: "extract"
source: "youtube"
video_id: "cO1f2wOxSH4"
url: "https://www.youtube.com/watch?v=cO1f2wOxSH4"
channel: "a16z"
extracted: "2026-09-17"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-17-how-decagon-runs-90-of-its-agents-on-open-source-models--cO1f2wOxSH4.txt]]"
tags: ["agents", "agent-tooling", "model-selection", "evals", "multi-agent", "testes-qa", "monitoramento", "observability", "governanca", "process", "production", "context-engineering", "token-budgeting", "knowledge-management"]
thesis: "A Decagon sustenta que empresas de camada de aplicação sobrevivem aos labs porque modelos open-source menores fine-tuned para tarefas estreitas superam modelos frontier (melhores, mais baratos e mais rápidos ao mesmo tempo), e o fosso duradouro é uma plataforma 'glass box' que captura lógica de negócio, evals e governança para tornar agentes implantáveis no enterprise."
concepts: ["Trade-off custo × inteligência × latência como eixo de seleção de modelos", "Falsa dicotomia custo vs qualidade: modelos pequenos fine-tuned superam frontier na tarefa específica", "Fine-tuning por caso de uso vs. ensino de procedimentos in-context", "AOPs (Agent Operating Procedures) escritas em texto simples em vez de código", "Fábrica de modelos (Decagon Labs) com treinamento e depreciação contínuos", "Evals bespoke medindo outcome fim-a-fim do sistema de modelos vs. loss curves", "Meta-agente (Duet) que gera procedimentos, ferramentas, testes, simulações e monitora conversas", "Autopilot: revisão de milhões de conversas, detecção de tendências e criação de variantes do modelo primário", "Glass box vs. black box na implantação enterprise", "Forward-deployed engineers como fase transitória a ser productizada", "Implantabilidade enterprise como moat: permissões, guardrails, colaboração em massa, compliance e integrações legadas", "Conversa como unidade de output; tokens por conversa crescendo com mais chamadas e checks paralelos", "Convergência labs ↔ camada de aplicação; application companies como 'labs verticais'", "Sales-led product development", "Build vs. buy em infraestrutura de treinamento de modelos"]
tools: ["Decagon", "Duet", "Duet Autopilot", "Decagon Labs", "Sierra", "Palantir", "OpenAI", "Anthropic", "Thinking Machines", "Kimi K3", "Claude Code", "a16z"]
people: ["Jesse Zhang (Decagon)", "Asha (Decagon)", "Shyam Sankar (Palantir)", "Decagon", "Sierra", "Palantir", "OpenAI", "Anthropic", "a16z"]
claims: ["Fine-tune modelos pequenos open-source para tarefas estreitas: na tarefa específica eles superam modelos frontier sendo mais baratos e mais rápidos — o trade-off custo/qualidade é falso", "Reserve modelos frontier para tarefas amplas e exploratórias (ex.: Autopilot revisando milhões de conversas e testando variantes do modelo primário)", "Construa evals próprios que meçam o outcome de cliente do sistema inteiro (modelos atuando em conjunto), não loss curves nem benchmarks públicos", "Fine-tune para o caso de uso, nunca para procedimentos do cliente: procedimentos mudam com frequência e devem ser ensinados in-context", "Espere que a fatia de inferência open-source no enterprise caia antes de subir: novos use cases nascem em APIs frontier e migram para open-source apenas quando solidificam em produção em escala", "Productize todo trabalho forward-deployed no core product (os próximos 10 clientes devem receber de graça), senão você está construindo consultoria disfarçada", "Automatize o harness com um meta-agente: geração de AOPs, integrações, testes, simulações, monitoramento de conversas e drafts de melhoria — viável apenas com modelos de raciocínio recentes", "Escreva procedimentos do agente em texto simples (AOPs) em vez de código para reduzir custo de iteração e dependência de engenharia", "Prioritize velocidade de iteração do cliente (glass box) sobre serviço FD black box: um cliente migrou da Sierra de 3 journeys/ano para 7 journeys em um mês", "Trate implantabilidade enterprise como moat: permissões para impedir ações catastróficas, colaboração de centenas de especialistas no comportamento do agente, testes regulatórios e extração de insights de milhões de conversas", "Em fase de crescimento otimize latência e qualidade e aceite custo como side benefit; tokens por conversa tendem a subir com mais chamadas, checks e paralelismo", "Opere uma fábrica de modelos: treine modelos novos continuamente e deprecie antigos conforme o frontier open-source avança, comprimindo o ciclo release→fine-tune", "Build vs. buy: construa internamente o que for acoplado aos seus evals e outcomes; compre o que for commodity (rotulagem de dados, medição de diversidade de datasets)"]
deep_dive: "high"
deep_dive_reason: "Densidade alta de detalhes acionáveis e arquiteturais (estratégia de open-source fine-tuned em 90% do fluxo, evals atrelados a outcomes, meta-agente Duet automatizando o harness de procedimentos/testes/monitoramento, governança e permissões para enterprise) com novidade e relevância direta a evals, harness e governança de agentes."
---

# How Decagon Runs 90% of Its Agents on Open-Source Models

## Tese
A Decagon sustenta que empresas de camada de aplicação sobrevivem aos labs porque modelos open-source menores fine-tuned para tarefas estreitas superam modelos frontier (melhores, mais baratos e mais rápidos ao mesmo tempo), e o fosso duradouro é uma plataforma 'glass box' que captura lógica de negócio, evals e governança para tornar agentes implantáveis no enterprise.

## Conceitos-chave
- Trade-off custo × inteligência × latência como eixo de seleção de modelos
- Falsa dicotomia custo vs qualidade: modelos pequenos fine-tuned superam frontier na tarefa específica
- Fine-tuning por caso de uso vs. ensino de procedimentos in-context
- AOPs (Agent Operating Procedures) escritas em texto simples em vez de código
- Fábrica de modelos (Decagon Labs) com treinamento e depreciação contínuos
- Evals bespoke medindo outcome fim-a-fim do sistema de modelos vs. loss curves
- Meta-agente (Duet) que gera procedimentos, ferramentas, testes, simulações e monitora conversas
- Autopilot: revisão de milhões de conversas, detecção de tendências e criação de variantes do modelo primário
- Glass box vs. black box na implantação enterprise
- Forward-deployed engineers como fase transitória a ser productizada
- Implantabilidade enterprise como moat: permissões, guardrails, colaboração em massa, compliance e integrações legadas
- Conversa como unidade de output; tokens por conversa crescendo com mais chamadas e checks paralelos
- Convergência labs ↔ camada de aplicação; application companies como 'labs verticais'
- Sales-led product development
- Build vs. buy em infraestrutura de treinamento de modelos

## Ferramentas & pessoas
**Ferramentas:** Decagon, Duet, Duet Autopilot, Decagon Labs, Sierra, Palantir, OpenAI, Anthropic, Thinking Machines, Kimi K3, Claude Code, a16z

**Pessoas/orgs:** Jesse Zhang (Decagon), Asha (Decagon), Shyam Sankar (Palantir), Decagon, Sierra, Palantir, OpenAI, Anthropic, a16z

## Claims acionáveis
- Fine-tune modelos pequenos open-source para tarefas estreitas: na tarefa específica eles superam modelos frontier sendo mais baratos e mais rápidos — o trade-off custo/qualidade é falso
- Reserve modelos frontier para tarefas amplas e exploratórias (ex.: Autopilot revisando milhões de conversas e testando variantes do modelo primário)
- Construa evals próprios que meçam o outcome de cliente do sistema inteiro (modelos atuando em conjunto), não loss curves nem benchmarks públicos
- Fine-tune para o caso de uso, nunca para procedimentos do cliente: procedimentos mudam com frequência e devem ser ensinados in-context
- Espere que a fatia de inferência open-source no enterprise caia antes de subir: novos use cases nascem em APIs frontier e migram para open-source apenas quando solidificam em produção em escala
- Productize todo trabalho forward-deployed no core product (os próximos 10 clientes devem receber de graça), senão você está construindo consultoria disfarçada
- Automatize o harness com um meta-agente: geração de AOPs, integrações, testes, simulações, monitoramento de conversas e drafts de melhoria — viável apenas com modelos de raciocínio recentes
- Escreva procedimentos do agente em texto simples (AOPs) em vez de código para reduzir custo de iteração e dependência de engenharia
- Prioritize velocidade de iteração do cliente (glass box) sobre serviço FD black box: um cliente migrou da Sierra de 3 journeys/ano para 7 journeys em um mês
- Trate implantabilidade enterprise como moat: permissões para impedir ações catastróficas, colaboração de centenas de especialistas no comportamento do agente, testes regulatórios e extração de insights de milhões de conversas
- Em fase de crescimento otimize latência e qualidade e aceite custo como side benefit; tokens por conversa tendem a subir com mais chamadas, checks e paralelismo
- Opere uma fábrica de modelos: treine modelos novos continuamente e deprecie antigos conforme o frontier open-source avança, comprimindo o ciclo release→fine-tune
- Build vs. buy: construa internamente o que for acoplado aos seus evals e outcomes; compre o que for commodity (rotulagem de dados, medição de diversidade de datasets)

> **Deep dive:** `high` — Densidade alta de detalhes acionáveis e arquiteturais (estratégia de open-source fine-tuned em 90% do fluxo, evals atrelados a outcomes, meta-agente Duet automatizando o harness de procedimentos/testes/monitoramento, governança e permissões para enterprise) com novidade e relevância direta a evals, harness e governança de agentes.
