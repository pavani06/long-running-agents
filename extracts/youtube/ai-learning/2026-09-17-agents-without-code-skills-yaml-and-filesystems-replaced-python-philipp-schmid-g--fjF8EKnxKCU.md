---
title: "Agents Without Code: Skills, YAML, and Filesystems Replaced Python — Philipp Schmid, Google DeepMind"
type: "extract"
source: "youtube"
video_id: "fjF8EKnxKCU"
url: "https://www.youtube.com/watch?v=fjF8EKnxKCU"
channel: "AI Engineer"
extracted: "2026-09-17"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-17-agents-without-code-skills-yaml-and-filesystems-replaced-python-philipp-schmid-g--fjF8EKnxKCU.txt]]"
tags: ["agents", "agent-loop", "agent-tooling", "agentic-coding", "arquitetura", "frameworks", "harness-engineering", "context-engineering", "context-management", "memory-architecture", "cross-session", "permissions", "documentation-as-code", "code-review", "evals", "verification", "runtime", "state"]
thesis: "Conforme os modelos melhoram, o código de orquestração de agentes (loops Python, roteamento de ferramentas, schemas JSON) colapsa em arquivos declarativos (AGENTS.md, skills.md) executados em harnesses remotos com sandbox gerenciado pela plataforma — 'arquivos substituindo Python'."
concepts: ["Agente = LLM rodando ferramentas em loop até alcançar um objetivo (definição de Simon)", "Evolução em três camadas: loop Python cru → framework de agentes → agente remoto baseado em arquivos", "API baseada em steps tipados (user, reasoning, function call, function result) em vez de histórico por turnos", "Sandbox em nuvem isolado e hospedado com bash, sistema de arquivos e fontes configuráveis (repo GitHub, GCS, arquivos inline)", "Proxy de rede que injeta credenciais nas requisições do sandbox para que o agente nunca veja os tokens", "Allowlist de domínios para restringir acesso de rede do agente", "Compaction automática de contexto e estado de sessão server-side", "Agentes como arquivos: AGENTS.md para instruções, skills.md para capacidades", "Agentes escrevem seus próprios arquivos de memória/preferências para reuso entre sessões", "Externalização de contexto e handoffs para arquivos em sessões longas", "Ferramentas gerais e atômicas (bash, CLI, filesystem) substituem ferramentas customizadas estreitas", "Anti-padrão: harness que fica mais complexo conforme o modelo melhora indica overengineering", "Build to delete: escrever código assumindo que ele será removido com a evolução dos modelos"]
tools: ["Gemini Interactions API", "Google ADK (Agent Development Kit)", "Agente remoto Anti-Gravity (Gemini API)", "Harness do AntiGravity IDE", "Agents API (IDs de agentes customizados)", "GitHub CLI", "Ferramenta Google Search", "Cloud sandbox hospedado (parâmetro environment)", "GCS buckets", "AI Studio"]
people: ["Google / Gemini", "Simon (autor da definição de agente citada)", "Cursor", "Manus", "LangChain", "Worsel (conforme transcrição)"]
claims: ["Cursor substituiu cerca de 12.000 linhas de TypeScript por ~200 linhas de arquivos de agente para orquestração de git worktrees", "Manus refatorou seu harness 5 vezes em 6 meses no último ano", "LangChain rearquitetou o Open Deep Research 3 vezes em um ano", "Worsel removeu 80% de suas ferramentas e obteve menos passos, respostas mais rápidas e melhor acurácia", "Se seu harness fica mais complexo à medida que o modelo melhora, você provavelmente está superengenheirando o harness", "A Interactions API usa steps tipados em vez de turnos, eliminando o abuso do role de usuário para devolver resultados de funções e do ambiente", "O proxy de rede do sandbox injeta credenciais on-the-fly nas chamadas de saída, e o acesso a domínios pode ser restringido (em branco = bloqueado; padrão = tudo liberado)", "Frameworks como ADK eliminam boilerplate gerando schemas JSON a partir das assinaturas das funções, mas o desenvolvedor ainda possui o plumbing Python das ferramentas", "Com o agente remoto, estender capacidades significa adicionar arquivos (skills.md, CLI no ambiente) sem mudar código, e uma única chamada de API executa todo o loop server-side", "O desenvolvedor deve focar no que é seu: instruções de domínio, workflows, evals, ferramentas limpas e verificação de resultados — não em reescrever infraestrutura", "Pare de microgerenciar caminhos de execução: forneça ferramentas gerais e deixe o modelo explorar, raciocinar e descobrir a solução"]
deep_dive: "high"
deep_dive_reason: "Alta densidade de insight arquitetural acionável (deleção de orquestração, harness vs. capacidade do modelo, arquivos como configuração, sandbox com injeção de credenciais, API por steps) com evidências da indústria e relevância direta a harness, context-engineering, evals e permissões."
---

# Agents Without Code: Skills, YAML, and Filesystems Replaced Python — Philipp Schmid, Google DeepMind

## Tese
Conforme os modelos melhoram, o código de orquestração de agentes (loops Python, roteamento de ferramentas, schemas JSON) colapsa em arquivos declarativos (AGENTS.md, skills.md) executados em harnesses remotos com sandbox gerenciado pela plataforma — 'arquivos substituindo Python'.

## Conceitos-chave
- Agente = LLM rodando ferramentas em loop até alcançar um objetivo (definição de Simon)
- Evolução em três camadas: loop Python cru → framework de agentes → agente remoto baseado em arquivos
- API baseada em steps tipados (user, reasoning, function call, function result) em vez de histórico por turnos
- Sandbox em nuvem isolado e hospedado com bash, sistema de arquivos e fontes configuráveis (repo GitHub, GCS, arquivos inline)
- Proxy de rede que injeta credenciais nas requisições do sandbox para que o agente nunca veja os tokens
- Allowlist de domínios para restringir acesso de rede do agente
- Compaction automática de contexto e estado de sessão server-side
- Agentes como arquivos: AGENTS.md para instruções, skills.md para capacidades
- Agentes escrevem seus próprios arquivos de memória/preferências para reuso entre sessões
- Externalização de contexto e handoffs para arquivos em sessões longas
- Ferramentas gerais e atômicas (bash, CLI, filesystem) substituem ferramentas customizadas estreitas
- Anti-padrão: harness que fica mais complexo conforme o modelo melhora indica overengineering
- Build to delete: escrever código assumindo que ele será removido com a evolução dos modelos

## Ferramentas & pessoas
**Ferramentas:** Gemini Interactions API, Google ADK (Agent Development Kit), Agente remoto Anti-Gravity (Gemini API), Harness do AntiGravity IDE, Agents API (IDs de agentes customizados), GitHub CLI, Ferramenta Google Search, Cloud sandbox hospedado (parâmetro environment), GCS buckets, AI Studio

**Pessoas/orgs:** Google / Gemini, Simon (autor da definição de agente citada), Cursor, Manus, LangChain, Worsel (conforme transcrição)

## Claims acionáveis
- Cursor substituiu cerca de 12.000 linhas de TypeScript por ~200 linhas de arquivos de agente para orquestração de git worktrees
- Manus refatorou seu harness 5 vezes em 6 meses no último ano
- LangChain rearquitetou o Open Deep Research 3 vezes em um ano
- Worsel removeu 80% de suas ferramentas e obteve menos passos, respostas mais rápidas e melhor acurácia
- Se seu harness fica mais complexo à medida que o modelo melhora, você provavelmente está superengenheirando o harness
- A Interactions API usa steps tipados em vez de turnos, eliminando o abuso do role de usuário para devolver resultados de funções e do ambiente
- O proxy de rede do sandbox injeta credenciais on-the-fly nas chamadas de saída, e o acesso a domínios pode ser restringido (em branco = bloqueado; padrão = tudo liberado)
- Frameworks como ADK eliminam boilerplate gerando schemas JSON a partir das assinaturas das funções, mas o desenvolvedor ainda possui o plumbing Python das ferramentas
- Com o agente remoto, estender capacidades significa adicionar arquivos (skills.md, CLI no ambiente) sem mudar código, e uma única chamada de API executa todo o loop server-side
- O desenvolvedor deve focar no que é seu: instruções de domínio, workflows, evals, ferramentas limpas e verificação de resultados — não em reescrever infraestrutura
- Pare de microgerenciar caminhos de execução: forneça ferramentas gerais e deixe o modelo explorar, raciocinar e descobrir a solução

> **Deep dive:** `high` — Alta densidade de insight arquitetural acionável (deleção de orquestração, harness vs. capacidade do modelo, arquivos como configuração, sandbox com injeção de credenciais, API por steps) com evidências da indústria e relevância direta a harness, context-engineering, evals e permissões.
