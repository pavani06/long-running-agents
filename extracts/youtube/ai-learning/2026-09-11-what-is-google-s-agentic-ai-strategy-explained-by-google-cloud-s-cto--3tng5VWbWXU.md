---
title: "What is Google's Agentic AI Strategy? (Explained by Google Cloud's CTO)"
type: "extract"
source: "youtube"
video_id: "3tng5VWbWXU"
url: "https://www.youtube.com/watch?v=3tng5VWbWXU"
channel: "CXOTalk"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-what-is-google-s-agentic-ai-strategy-explained-by-google-cloud-s-cto--3tng5VWbWXU.txt]]"
tags: ["agents", "agent-fleets", "agentes-orquestracao", "arquitetura", "context-engineering", "evals", "gate-design", "governanca", "multi-agent", "observability", "telemetry", "decision-discipline", "knowledge-management", "data-platform", "model-selection", "roadmap", "process", "stack-tooling"]
thesis: "Will Grannis, CTO do Google Cloud, defende que o sucesso de agentes empresariais depende de contexto explícito (processos documentados), avaliações multi-etapa com IA-como-juiz, governança integrada (consolidada na pilha Gemini Enterprise) e diferenciação via grounding dos modelos de fronteira em dados proprietários de domínio."
concepts: ["Agentes como terceira onda de automação (intenção → execução de tarefas)", "Racionalização de workflows agênticos (agentic workflow rationalization)", "IA-como-juiz / IA-como-crítico para avaliar conclusão de tarefas", "Avaliação em múltiplas etapas do pipeline (física, inventário, critérios de marca)", "Telemetria recursiva: mais agentes geram mais dados de comportamento para refinar agentes", "Espectro agente-de-tarefa vs. agente-de-papel (role-based)", "Human-in-the-loop proporcional ao risco (stakes) do workflow", "Regras organizacionais implícitas vs. instruções explícitas para agentes", "Grounding de modelos de fronteira com dados e linguagem de domínio proprietários", "Setores regulados têm vantagem inicial por documentação prévia de SOPs", "UI efêmera: o modelo gera a interface ad hoc", "Protocolos de interoperabilidade: MCP, A2A, Agent Payment Protocol", "Alinhamento agente-tarefa em escala (dezenas a milhares de agentes)", "Multimodalidade como futuro da interação (imagem, vídeo, voz, câmera)", "Gate de decisão incremental: prosseguir / mudar / parar", "Shadow IT e cultura de experimentação como motores de adoção", "Liderança modelando o uso (CEO vibe coding)"]
tools: ["Gemini Enterprise", "Gemini 2.5 Pro", "Gemini Flash", "Veo", "Imagen", "Nano Banana", "Gemini CLI", "Gemini Live API", "BigQuery", "MCP", "A2A", "Agent Payment Protocol (AP2)", "Computer use", "ServiceNow", "Oracle", "Salesforce", "Jira", "Confluence", "SharePoint", "Workday", "Harvey AI"]
people: ["Will Grannis (CTO Google Cloud)", "Google Cloud", "Google Public Sector", "Michael Krigsman (CXO Talk)", "Highmark Health", "Harvey AI", "Emeritus", "Sundar Pichai", "State of Wisconsin", "Anthony Scriffino", "Stephanie Satsos (Workday)", "Arcelon Khan", "Justin Kavanaaugh", "Kenroy Benedict", "Greg Walters", "Elizabeth Shaw"]
claims: ["Selecione problemas com dados, contexto e SOPs documentados antes de implantar agentes — inventariar e escolher metodicamente ('racionalização de workflows agênticos')", "Setores regulados (financeiro, saúde, setor público) atingem valor mais rápido porque já têm processos de negócio documentados", "Projete IA-como-juiz desde o início: agentes produzem tarefas mais rápido do que humanos conseguem aprovar", "Arquitete avaliações em múltiplos pontos do pipeline (ex.: 4 gates — leis da física, correspondência de inventário, critérios de marca, sensibilidade de cluster) e torne-as instruções explícitas ao agente avaliador", "Agentes geram trilhas de telemetria e logs em escala muito maior que workflows manuais — use esse 'escape' para analisar e refinar comportamentos recursivamente", "Decida human-in-the-loop pelo custo do erro: segurança de transporte exige humano; geração em massa de vídeos de marca não", "Quebre workflows agênticos longos em passos atômicos e mensuráveis, com decisão explícita de prosseguir/mudar/parar em cada gate", "A vantagem competitiva não está no modelo (acessível a todos), mas em combiná-lo com dados, linguagem e IP de domínio próprio de forma segura", "Documente regras e normas ocultas da organização: agentes não fazem saltos lógicos não explícitos, e falhas de software revelam normas implícitas", "Fomente experimentação bottom-up (shadow IT) com equipes pequenas e escassas — ex.: Gemini CLI cresceu de time pequeno e scrappy", "Comece imediatamente a construir workflows agênticos: a curva de aprendizado (MCP, computer use, orquestração) leva mais tempo do que se espera", "Pequenas empresas devem usar integrações de IA nativas do provedor de nuvem (ex.: inferência embutida no BigQuery) em vez de soluções bolt-on", "Configure expectativas realistas: primeiras iterações terão qualidade baixa; o valor vem da iteração rápida", "Líderes devem modelar o uso prático (construir agentes em linguagem natural na plataforma) para sinalizar compromisso", "Meça e seja transparente em cada passo para combater o hype; subestimamos a profundidade e superestimamos a velocidade das mudanças", "Casos: Highmark Health (~60 mil usuários em agente de conhecimento interno), telco britânica (suporte multimodal ao vivo via câmera), Wisconsin (benefícios de desemprego de semanas para horas), banco (pesquisa de dias para minutos)"]
deep_dive: "high"
deep_dive_reason: "Alta densidade de insight acionável e arquitetural diretamente relevante a evals (pipeline de 4 gates com IA-como-juiz), context-engineering (SOPs e regras implícitas), gate-design, telemetria recursiva em fleets de agentes, governança e protocolos emergentes (MCP/A2A/AP2), com novidade concreta apesar do viés promocional da plataforma Gemini Enterprise."
---

# What is Google's Agentic AI Strategy? (Explained by Google Cloud's CTO)

## Tese
Will Grannis, CTO do Google Cloud, defende que o sucesso de agentes empresariais depende de contexto explícito (processos documentados), avaliações multi-etapa com IA-como-juiz, governança integrada (consolidada na pilha Gemini Enterprise) e diferenciação via grounding dos modelos de fronteira em dados proprietários de domínio.

## Conceitos-chave
- Agentes como terceira onda de automação (intenção → execução de tarefas)
- Racionalização de workflows agênticos (agentic workflow rationalization)
- IA-como-juiz / IA-como-crítico para avaliar conclusão de tarefas
- Avaliação em múltiplas etapas do pipeline (física, inventário, critérios de marca)
- Telemetria recursiva: mais agentes geram mais dados de comportamento para refinar agentes
- Espectro agente-de-tarefa vs. agente-de-papel (role-based)
- Human-in-the-loop proporcional ao risco (stakes) do workflow
- Regras organizacionais implícitas vs. instruções explícitas para agentes
- Grounding de modelos de fronteira com dados e linguagem de domínio proprietários
- Setores regulados têm vantagem inicial por documentação prévia de SOPs
- UI efêmera: o modelo gera a interface ad hoc
- Protocolos de interoperabilidade: MCP, A2A, Agent Payment Protocol
- Alinhamento agente-tarefa em escala (dezenas a milhares de agentes)
- Multimodalidade como futuro da interação (imagem, vídeo, voz, câmera)
- Gate de decisão incremental: prosseguir / mudar / parar
- Shadow IT e cultura de experimentação como motores de adoção
- Liderança modelando o uso (CEO vibe coding)

## Ferramentas & pessoas
**Ferramentas:** Gemini Enterprise, Gemini 2.5 Pro, Gemini Flash, Veo, Imagen, Nano Banana, Gemini CLI, Gemini Live API, BigQuery, MCP, A2A, Agent Payment Protocol (AP2), Computer use, ServiceNow, Oracle, Salesforce, Jira, Confluence, SharePoint, Workday, Harvey AI

**Pessoas/orgs:** Will Grannis (CTO Google Cloud), Google Cloud, Google Public Sector, Michael Krigsman (CXO Talk), Highmark Health, Harvey AI, Emeritus, Sundar Pichai, State of Wisconsin, Anthony Scriffino, Stephanie Satsos (Workday), Arcelon Khan, Justin Kavanaaugh, Kenroy Benedict, Greg Walters, Elizabeth Shaw

## Claims acionáveis
- Selecione problemas com dados, contexto e SOPs documentados antes de implantar agentes — inventariar e escolher metodicamente ('racionalização de workflows agênticos')
- Setores regulados (financeiro, saúde, setor público) atingem valor mais rápido porque já têm processos de negócio documentados
- Projete IA-como-juiz desde o início: agentes produzem tarefas mais rápido do que humanos conseguem aprovar
- Arquitete avaliações em múltiplos pontos do pipeline (ex.: 4 gates — leis da física, correspondência de inventário, critérios de marca, sensibilidade de cluster) e torne-as instruções explícitas ao agente avaliador
- Agentes geram trilhas de telemetria e logs em escala muito maior que workflows manuais — use esse 'escape' para analisar e refinar comportamentos recursivamente
- Decida human-in-the-loop pelo custo do erro: segurança de transporte exige humano; geração em massa de vídeos de marca não
- Quebre workflows agênticos longos em passos atômicos e mensuráveis, com decisão explícita de prosseguir/mudar/parar em cada gate
- A vantagem competitiva não está no modelo (acessível a todos), mas em combiná-lo com dados, linguagem e IP de domínio próprio de forma segura
- Documente regras e normas ocultas da organização: agentes não fazem saltos lógicos não explícitos, e falhas de software revelam normas implícitas
- Fomente experimentação bottom-up (shadow IT) com equipes pequenas e escassas — ex.: Gemini CLI cresceu de time pequeno e scrappy
- Comece imediatamente a construir workflows agênticos: a curva de aprendizado (MCP, computer use, orquestração) leva mais tempo do que se espera
- Pequenas empresas devem usar integrações de IA nativas do provedor de nuvem (ex.: inferência embutida no BigQuery) em vez de soluções bolt-on
- Configure expectativas realistas: primeiras iterações terão qualidade baixa; o valor vem da iteração rápida
- Líderes devem modelar o uso prático (construir agentes em linguagem natural na plataforma) para sinalizar compromisso
- Meça e seja transparente em cada passo para combater o hype; subestimamos a profundidade e superestimamos a velocidade das mudanças
- Casos: Highmark Health (~60 mil usuários em agente de conhecimento interno), telco britânica (suporte multimodal ao vivo via câmera), Wisconsin (benefícios de desemprego de semanas para horas), banco (pesquisa de dias para minutos)

> **Deep dive:** `high` — Alta densidade de insight acionável e arquitetural diretamente relevante a evals (pipeline de 4 gates com IA-como-juiz), context-engineering (SOPs e regras implícitas), gate-design, telemetria recursiva em fleets de agentes, governança e protocolos emergentes (MCP/A2A/AP2), com novidade concreta apesar do viés promocional da plataforma Gemini Enterprise.
