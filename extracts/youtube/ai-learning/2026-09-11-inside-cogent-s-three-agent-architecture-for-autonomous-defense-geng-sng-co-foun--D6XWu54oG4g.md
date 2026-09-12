---
title: "Inside Cogent's three-agent architecture for autonomous defense | Geng Sng (Co-founder, Cogent)"
type: "extract"
source: "youtube"
video_id: "D6XWu54oG4g"
url: "https://www.youtube.com/watch?v=D6XWu54oG4g"
channel: "LangChain"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-inside-cogent-s-three-agent-architecture-for-autonomous-defense-geng-sng-co-foun--D6XWu54oG4g.txt]]"
tags: ["agents", "agent-fleets", "arquitetura", "context-engineering", "context-management", "data-platform", "evals", "gate-design", "governanca", "harness", "harness-engineering", "memory-architecture", "model-selection", "multi-agent", "observability", "ontologia", "permissions", "production", "verification", "monitoramento", "testes-qa"]
thesis: "Defesa cibernômica autônoma em velocidade de máquina torna-se viável combinando uma plataforma de dados agêntica (grafo de contexto com ontologia híbrida materializada sobre um data lake) com uma escada graduada de confiança/autonomia, sandboxes com permissões em camadas e um sistema de evals em dois níveis usando uma frota de juízes LLM que chega à paridade ambiental com o agente avaliado."
concepts: ["Mean time to exploit comprimido (de ~2,5 anos para minutos)", "Agentic data lake ('agent lake')", "Context farm / 'supply side agents'", "Grafo de contexto materializado sobre data lake (S3), sem graph database", "Ontologia híbrida: propriedades estruturais fixas + atributos derivados por agentes", "Enriquecimento em múltiplas passadas (primeira lossy para topologia, demais focadas)", "Context artifacts com provenance", "Escada de confiança: read-only, auto-routing de tickets, auto validation, automação total", "Vulnerability chaining e impacto em produção como bloqueio real da automação", "Sandbox com permissões em camadas e policy engine para elevação de acesso", "Ações de escrita executadas fora do sandbox de forma determinística", "Três tipos de agentes: interativos, background e coding agents", "Fase de planejamento profunda com testes que short-circuitam a execução (one-shotting)", "Hot vs. cold context (distinção por uso ativo, não por tempo)", "Sub-agentes para paralelização e side-tasks fora do caminho crítico", "Frota de LLMs como juízes: de adversarial simples até paridade ambiental (agent-as-judge)", "Métrica 'fail-safe recover' como sinal de bug de prompt", "Evals offline (golden labels, análise de traces) vs. online (amostragem, detecção de drift/incidentes)", "Entry points de contexto (produto, Slack, Teams, tickets) e feedback loop com o usuário", "Monitoramento de drift de modelos, prompts e comportamentos", "Explainability e front-ends agênticos (gráficos gerados pelo agente)"]
tools: ["Cogent (plataforma de cyber defense autônoma)", "S3 (data lake)", "Spark", "Jupyter notebooks", "MCP", "Claude / Opus (Anthropic)", "OpenAI (modelos com trusted access para cyber)", "LangSmith", "Claude Code / Codex (harnesses citados)", "Slack / Teams", "CMDB / SharePoint / Google Drive (fontes de contexto)", "Mozilla (alvo de zero-days por modelo frontier)"]
people: ["Gang Singh (cofundador e CTO da Cogent)", "Anthropic", "OpenAI", "Mozilla", "LangChain / LangSmith (podcast Max Agency)"]
claims: ["Mean time to exploit caiu de ~2,5 anos para minutos devido a digital sprawl e modelos frontier encontrando zero-days (ex.: ~500 turns em ambiente Mozilla).", "Para alto write throughput (bilhões de eventos/dia), evite graph databases: armazene em data lake (S3) e materialize grafos customizados por caso de uso.", "Fixe apenas as propriedades estruturais da ontologia (assinaturas para resolução de entidades) e deixe agentes criarem atributos derivados on the fly (ex.: internet exposure).", "A primeira passada de enriquecimento deve ser lossy para pintar a topologia; passadas seguintes respondem perguntas focadas com agentes.", "Onboarding de confiança em degraus: read-only com aprovação humana, depois auto-routing de tickets, depois auto validação em dev/staging, e por fim automação total em fatias de baixo blast radius.", "~80% do attack surface corporativo típico está em dev/staging: uma fatia enorme é automatizável se isolada corretamente.", "O bloqueio real da automação não é aplicar o patch, mas saber o impacto da aplicação em produção.", "Rode agentes em sandboxes read-only com policy engine para elevação de acesso; ações de escrita saem do sandbox de forma determinística, então alucinação nunca vira write.", "Para agentes interativos, invista em planejamento profundo com testes que short-circuitam a execução: planejar bem permite one-shotting em 1-2 loops.", "Sem constraint de latência, agentes background de longa duração destravam o potencial máximo de raciocínio, com retries e tarefas longas.", "Use sub-agentes apenas para tarefas decomponíveis/paralelizáveis e side-tasks fora do caminho crítico; sequência pura pede orquestração externa, não sub-agente.", "Construa frota de juízes LLM em níveis: do adversarial simples até juízes com paridade ambiental completa com o agente avaliado (agent-as-judge).", "Rastreie a métrica fail-safe recover: alta frequência correlaciona com erros de prompt, distinguindo problema difícil de bug introduzido por você.", "Online evals: amostre com distribuição representativa e use como detector de incidentes/drift; deixe a carga de correção para os evals offline (golden labels e traces).", "Diferencie hot context (ativamente usado: sessão, compaction, changelogs) de cold context (arquivado com índice/sumário), ambos plugados ao knowledge graph, uma distinção por uso e não por tempo.", "Multiplique entry points de captura de contexto (produto, Slack, Teams, tickets): quanto mais pontos, mais viva e em tempo real a camada de contexto.", "Construa supply side agents que extraem decisões e contexto dos sistemas organizacionais sem depender de engajamento direto do usuário.", "Usuários confiam demais em agentes após bons resultados e esquecem que tarefas nunca vistas falharão; a responsabilidade pela segurança é do fornecedor da ferramenta.", "Monitore drift de modelos, prompts e comportamentos (ex.: novos ativos pós-M&A) e feche o loop pedindo decisão ao usuário quando o contexto é inédito.", "Perguntas de dados difíceis que levavam de 4 horas a semanas podem sair em 3-4 minutos via text-to-SQL e modelagem de schema pelo agente."]
deep_dive: "high"
deep_dive_reason: "Alta densidade de decisões arquiteturais acionáveis e novas (sandbox com permissões em camadas e writes fora da caixa, escada de confiança, hot/cold context definido por uso, juízes LLM com paridade ambiental, ontologia híbrida sobre data lake, métrica fail-safe recover) diretamente relevantes a harness, context-engineering, evals, agent-fleets e governança."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-why-more-context-makes-your-agent-dumber-and-what-to-do-about-it-nupur-sharma-qo--EcqMYoIV57A|Why More Context Makes Your Agent Dumber and What to Do About It — Nupur Sharma, Qodo]]", "[[extracts/youtube/ai-learning/2026-09-11-scaling-agents-for-gen-ai-products-anju-kambadur-bloomberg-head-of-ai-engineerin--b2GqTDWtg6s|Scaling Agents for Gen AI Products - Anju Kambadur, Bloomberg Head of AI Engineering]]", "[[extracts/youtube/ai-learning/2026-09-11-anthropic-s-applied-ai-team-on-the-evolution-of-agentic-surfaces--K0X9QDRkIdg|Anthropic's Applied AI team on the Evolution of Agentic Surfaces]]", "[[extracts/youtube/ai-learning/2026-09-11-agentic-engineering-explained-by-a-10x-developer--FU5_kpTAVDo|Agentic Engineering, explained by a 10x developer]]", "[[extracts/youtube/ai-learning/2026-09-11-agent-frameworks-considered-harmful-remi-louf-txt--KHudyx5wW3U|Agent Frameworks Considered Harmful — Rémi Louf, .txt]]", "[[extracts/youtube/ai-learning/2026-09-11-l8-principal-s-agentic-engineering-setup-just-copy-him--8ZgpAXe5V5w|L8 Principal's Agentic Engineering Setup (just copy him)]]", "[[extracts/youtube/ai-learning/2026-09-11-context-graphs-for-explainable-decision-aware-ai-agents-andreas-kollegger-zaid-z--abvQEhvRI_c|Context Graphs for Explainable, Decision-Aware AI Agents — Andreas Kollegger & Zaid Zaim, Neo4j]]"]
theme: "Arquiteturas de Deep Agents"
---

# Inside Cogent's three-agent architecture for autonomous defense | Geng Sng (Co-founder, Cogent)

## Tese
Defesa cibernômica autônoma em velocidade de máquina torna-se viável combinando uma plataforma de dados agêntica (grafo de contexto com ontologia híbrida materializada sobre um data lake) com uma escada graduada de confiança/autonomia, sandboxes com permissões em camadas e um sistema de evals em dois níveis usando uma frota de juízes LLM que chega à paridade ambiental com o agente avaliado.

## Conceitos-chave
- Mean time to exploit comprimido (de ~2,5 anos para minutos)
- Agentic data lake ('agent lake')
- Context farm / 'supply side agents'
- Grafo de contexto materializado sobre data lake (S3), sem graph database
- Ontologia híbrida: propriedades estruturais fixas + atributos derivados por agentes
- Enriquecimento em múltiplas passadas (primeira lossy para topologia, demais focadas)
- Context artifacts com provenance
- Escada de confiança: read-only, auto-routing de tickets, auto validation, automação total
- Vulnerability chaining e impacto em produção como bloqueio real da automação
- Sandbox com permissões em camadas e policy engine para elevação de acesso
- Ações de escrita executadas fora do sandbox de forma determinística
- Três tipos de agentes: interativos, background e coding agents
- Fase de planejamento profunda com testes que short-circuitam a execução (one-shotting)
- Hot vs. cold context (distinção por uso ativo, não por tempo)
- Sub-agentes para paralelização e side-tasks fora do caminho crítico
- Frota de LLMs como juízes: de adversarial simples até paridade ambiental (agent-as-judge)
- Métrica 'fail-safe recover' como sinal de bug de prompt
- Evals offline (golden labels, análise de traces) vs. online (amostragem, detecção de drift/incidentes)
- Entry points de contexto (produto, Slack, Teams, tickets) e feedback loop com o usuário
- Monitoramento de drift de modelos, prompts e comportamentos
- Explainability e front-ends agênticos (gráficos gerados pelo agente)

## Ferramentas & pessoas
**Ferramentas:** Cogent (plataforma de cyber defense autônoma), S3 (data lake), Spark, Jupyter notebooks, MCP, Claude / Opus (Anthropic), OpenAI (modelos com trusted access para cyber), LangSmith, Claude Code / Codex (harnesses citados), Slack / Teams, CMDB / SharePoint / Google Drive (fontes de contexto), Mozilla (alvo de zero-days por modelo frontier)

**Pessoas/orgs:** Gang Singh (cofundador e CTO da Cogent), Anthropic, OpenAI, Mozilla, LangChain / LangSmith (podcast Max Agency)

## Claims acionáveis
- Mean time to exploit caiu de ~2,5 anos para minutos devido a digital sprawl e modelos frontier encontrando zero-days (ex.: ~500 turns em ambiente Mozilla).
- Para alto write throughput (bilhões de eventos/dia), evite graph databases: armazene em data lake (S3) e materialize grafos customizados por caso de uso.
- Fixe apenas as propriedades estruturais da ontologia (assinaturas para resolução de entidades) e deixe agentes criarem atributos derivados on the fly (ex.: internet exposure).
- A primeira passada de enriquecimento deve ser lossy para pintar a topologia; passadas seguintes respondem perguntas focadas com agentes.
- Onboarding de confiança em degraus: read-only com aprovação humana, depois auto-routing de tickets, depois auto validação em dev/staging, e por fim automação total em fatias de baixo blast radius.
- ~80% do attack surface corporativo típico está em dev/staging: uma fatia enorme é automatizável se isolada corretamente.
- O bloqueio real da automação não é aplicar o patch, mas saber o impacto da aplicação em produção.
- Rode agentes em sandboxes read-only com policy engine para elevação de acesso; ações de escrita saem do sandbox de forma determinística, então alucinação nunca vira write.
- Para agentes interativos, invista em planejamento profundo com testes que short-circuitam a execução: planejar bem permite one-shotting em 1-2 loops.
- Sem constraint de latência, agentes background de longa duração destravam o potencial máximo de raciocínio, com retries e tarefas longas.
- Use sub-agentes apenas para tarefas decomponíveis/paralelizáveis e side-tasks fora do caminho crítico; sequência pura pede orquestração externa, não sub-agente.
- Construa frota de juízes LLM em níveis: do adversarial simples até juízes com paridade ambiental completa com o agente avaliado (agent-as-judge).
- Rastreie a métrica fail-safe recover: alta frequência correlaciona com erros de prompt, distinguindo problema difícil de bug introduzido por você.
- Online evals: amostre com distribuição representativa e use como detector de incidentes/drift; deixe a carga de correção para os evals offline (golden labels e traces).
- Diferencie hot context (ativamente usado: sessão, compaction, changelogs) de cold context (arquivado com índice/sumário), ambos plugados ao knowledge graph, uma distinção por uso e não por tempo.
- Multiplique entry points de captura de contexto (produto, Slack, Teams, tickets): quanto mais pontos, mais viva e em tempo real a camada de contexto.
- Construa supply side agents que extraem decisões e contexto dos sistemas organizacionais sem depender de engajamento direto do usuário.
- Usuários confiam demais em agentes após bons resultados e esquecem que tarefas nunca vistas falharão; a responsabilidade pela segurança é do fornecedor da ferramenta.
- Monitore drift de modelos, prompts e comportamentos (ex.: novos ativos pós-M&A) e feche o loop pedindo decisão ao usuário quando o contexto é inédito.
- Perguntas de dados difíceis que levavam de 4 horas a semanas podem sair em 3-4 minutos via text-to-SQL e modelagem de schema pelo agente.

> **Deep dive:** `high` — Alta densidade de decisões arquiteturais acionáveis e novas (sandbox com permissões em camadas e writes fora da caixa, escada de confiança, hot/cold context definido por uso, juízes LLM com paridade ambiental, ontologia híbrida sobre data lake, métrica fail-safe recover) diretamente relevantes a harness, context-engineering, evals, agent-fleets e governança.
