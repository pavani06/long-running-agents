---
title: "How to Understand the Next Wave of AI Before Everyone Else | Tibo Interview"
type: "extract"
source: "youtube"
video_id: "4qjEgPojjzM"
url: "https://www.youtube.com/watch?v=4qjEgPojjzM"
channel: "Matthew Berman"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-how-to-understand-the-next-wave-of-ai-before-everyone-else-tibo-interview--4qjEgPojjzM.txt]]"
tags: ["harness-engineering", "context-engineering", "memory-architecture", "multi-agent", "agent-fleets", "agentic-coding", "agents", "token-budgeting", "runtime", "production", "escalation", "error-handling", "governanca", "investimentos", "stack-tooling", "roadmap", "decision-discipline", "monitoramento"]
thesis: "O líder do ChatGPT/Codex na OpenAI argumenta que a próxima evolução dos agentes exige harnesses que superem limitações atuais (skill files frágeis, memória instável, sub-agentes que quebram a ilusão), com modelos ultra-rápidos deslocando o gargalo de tokens para overhead de tool calls e atenção humana, unificados num único agente 'AGI pessoal' (merge Codex+ChatGPT) alimentado por auto-aperfeiçoamento recursivo aplicado à própria infraestrutura de inferência."
concepts: ["harness de agentes", "AGI pessoal (personal AGI)", "arquitetura de memória e sub-agentes", "skill files", "agentes na nuvem vs laptop como restrição", "gestão de atenção do desenvolvedor", "ultra fast (10-14x tokens/segundo)", "overhead de tool calls como novo gargalo", "paralelismo/concorrência de tarefas de agentes", "automação total vs agente no fluxo", "auto-aperfeiçoamento recursivo aplicado a infraestrutura", "planejamento de capacidade de compute", "eficiência de tokens por geração de modelo", "interface adaptativa à individualidade (merge ChatGPT+Codex)", "voz-first e interações não-textuais", "pausa de RL por segurança/alignment", "minimização de humano-em-loop (aprovação só de ações de alto risco)", "cultura bottoms-up de shipping e autodisrupção", "resets de uso como compensação/goodwill"]
tools: ["ChatGPT", "Codex", "ChatGPT iOS app", "LM chat (Google)", "Luna", "Terra", "Soul", "Ultra Fast", "CUDA kernels", "Dev Day", "Hugging Face (incidente citado)"]
people: ["OpenAI", "Google DeepMind", "Anthropic", "Sam Altman", "Thibault (Tibo)", "Amazon"]
claims: ["Skill files são difíceis de manter ao longo do tempo e a memória atual dos agentes não lembra tudo de forma confiável — áreas maduras para inovação no harness", "Sub-agentes constroem uma pequena rede cuja 'ilusão' de parceiro contínuo quebra em vários pontos da interação", "Modelos futuros precisarão de mais recursos do que um laptop oferece, pois o laptop foi desenhado para restrições humanas (velocidade de digitação/pensamento)", "Com velocidades ultra fast (10-14x), o gargalo migra do gerador de tokens para CPU/tool calls/rede, reduzindo ganho percebido a 3-4x em workflows ricos em tool calls", "A compensação para o gargalo é concorrência: explorar, escrever testes e compilar simultaneamente desloca o bottleneck e aproveita o raciocínio rápido do modelo", "Com modelos rápidos, 3-4 agentes em fluxo contínuo substituem o gerenciamento de 10-15 agentes paralelos lentos que impõe sobrecarga cognitiva de context switching", "Há duas categorias de problema: o agente pessoal no fluxo (reativo e proativo, tailor-made) e a automação total (ex.: otimização de performance via logs de produção, patch automático de regressões e vulnerabilidades com aprovação humana só em ações de alto risco)", "O merge Codex+ChatGPT usa a mesma tecnologia e o mesmo harness: uma interface única que se adapta à individualidade do usuário, técnica ou não, multimodal e voice-first", "Usar os modelos de fronteira para re-engineerar o próprio stack de serving/inferência gerou ganhos significativos — ex.: queda de preço de 80% na Luna e ~60% mais velocidade em 3 meses", "Auto-aperfeiçoamento recursivo está rendendo mais sucesso imediato em infraestrutura crítica (kernels CUDA, inference stack, produtos) do que na fronteira de pesquisa", "A pausa no RL de fronteira serviu para endurecer e alinhar sistemas, com princípios claros definidos pelo time de segurança antes de retomar treinos", "Ultra fast deve ser priorizado para cenários de alto risco (incidentes/outages, incident commander) e a capacidade é majoritariamente reservada para clientes externos, não funcionários", "Eficiência de tokens melhora a cada geração (Soul > Terra; próximo > Soul) e velocidades ultra fast devem virar padrão em 1-2 anos, sempre com um tier premium acima", "Benchmarks não revelam tudo: é preciso brincar com os modelos para descobrir capacidades que mudam o produto (ex.: voz com tool use viabiliza ditado matinal de tarefas)", "Reset de limites de uso é um botão (físico) que o líder pode apertar a qualquer momento, sem escrutínio de marketing/finanças, como compensação e celebração — construindo goodwill mensurável na comunidade"]
deep_dive: "medium"
deep_dive_reason: "Há insight arquitetural real e relativamente novo sobre harness (limites de skill files/memória/sub-agentes), deslocamento de gargalos com tokens ultra-rápidos e auto-aperfeiçoamento recursivo em infraestrutura, mas densidade acionável é diluída por trechos promocionais, anedotas de cultura e conteúdo redundante sobre resets e concorrência."
---

# How to Understand the Next Wave of AI Before Everyone Else | Tibo Interview

## Tese
O líder do ChatGPT/Codex na OpenAI argumenta que a próxima evolução dos agentes exige harnesses que superem limitações atuais (skill files frágeis, memória instável, sub-agentes que quebram a ilusão), com modelos ultra-rápidos deslocando o gargalo de tokens para overhead de tool calls e atenção humana, unificados num único agente 'AGI pessoal' (merge Codex+ChatGPT) alimentado por auto-aperfeiçoamento recursivo aplicado à própria infraestrutura de inferência.

## Conceitos-chave
- harness de agentes
- AGI pessoal (personal AGI)
- arquitetura de memória e sub-agentes
- skill files
- agentes na nuvem vs laptop como restrição
- gestão de atenção do desenvolvedor
- ultra fast (10-14x tokens/segundo)
- overhead de tool calls como novo gargalo
- paralelismo/concorrência de tarefas de agentes
- automação total vs agente no fluxo
- auto-aperfeiçoamento recursivo aplicado a infraestrutura
- planejamento de capacidade de compute
- eficiência de tokens por geração de modelo
- interface adaptativa à individualidade (merge ChatGPT+Codex)
- voz-first e interações não-textuais
- pausa de RL por segurança/alignment
- minimização de humano-em-loop (aprovação só de ações de alto risco)
- cultura bottoms-up de shipping e autodisrupção
- resets de uso como compensação/goodwill

## Ferramentas & pessoas
**Ferramentas:** ChatGPT, Codex, ChatGPT iOS app, LM chat (Google), Luna, Terra, Soul, Ultra Fast, CUDA kernels, Dev Day, Hugging Face (incidente citado)

**Pessoas/orgs:** OpenAI, Google DeepMind, Anthropic, Sam Altman, Thibault (Tibo), Amazon

## Claims acionáveis
- Skill files são difíceis de manter ao longo do tempo e a memória atual dos agentes não lembra tudo de forma confiável — áreas maduras para inovação no harness
- Sub-agentes constroem uma pequena rede cuja 'ilusão' de parceiro contínuo quebra em vários pontos da interação
- Modelos futuros precisarão de mais recursos do que um laptop oferece, pois o laptop foi desenhado para restrições humanas (velocidade de digitação/pensamento)
- Com velocidades ultra fast (10-14x), o gargalo migra do gerador de tokens para CPU/tool calls/rede, reduzindo ganho percebido a 3-4x em workflows ricos em tool calls
- A compensação para o gargalo é concorrência: explorar, escrever testes e compilar simultaneamente desloca o bottleneck e aproveita o raciocínio rápido do modelo
- Com modelos rápidos, 3-4 agentes em fluxo contínuo substituem o gerenciamento de 10-15 agentes paralelos lentos que impõe sobrecarga cognitiva de context switching
- Há duas categorias de problema: o agente pessoal no fluxo (reativo e proativo, tailor-made) e a automação total (ex.: otimização de performance via logs de produção, patch automático de regressões e vulnerabilidades com aprovação humana só em ações de alto risco)
- O merge Codex+ChatGPT usa a mesma tecnologia e o mesmo harness: uma interface única que se adapta à individualidade do usuário, técnica ou não, multimodal e voice-first
- Usar os modelos de fronteira para re-engineerar o próprio stack de serving/inferência gerou ganhos significativos — ex.: queda de preço de 80% na Luna e ~60% mais velocidade em 3 meses
- Auto-aperfeiçoamento recursivo está rendendo mais sucesso imediato em infraestrutura crítica (kernels CUDA, inference stack, produtos) do que na fronteira de pesquisa
- A pausa no RL de fronteira serviu para endurecer e alinhar sistemas, com princípios claros definidos pelo time de segurança antes de retomar treinos
- Ultra fast deve ser priorizado para cenários de alto risco (incidentes/outages, incident commander) e a capacidade é majoritariamente reservada para clientes externos, não funcionários
- Eficiência de tokens melhora a cada geração (Soul > Terra; próximo > Soul) e velocidades ultra fast devem virar padrão em 1-2 anos, sempre com um tier premium acima
- Benchmarks não revelam tudo: é preciso brincar com os modelos para descobrir capacidades que mudam o produto (ex.: voz com tool use viabiliza ditado matinal de tarefas)
- Reset de limites de uso é um botão (físico) que o líder pode apertar a qualquer momento, sem escrutínio de marketing/finanças, como compensação e celebração — construindo goodwill mensurável na comunidade

> **Deep dive:** `medium` — Há insight arquitetural real e relativamente novo sobre harness (limites de skill files/memória/sub-agentes), deslocamento de gargalos com tokens ultra-rápidos e auto-aperfeiçoamento recursivo em infraestrutura, mas densidade acionável é diluída por trechos promocionais, anedotas de cultura e conteúdo redundante sobre resets e concorrência.
