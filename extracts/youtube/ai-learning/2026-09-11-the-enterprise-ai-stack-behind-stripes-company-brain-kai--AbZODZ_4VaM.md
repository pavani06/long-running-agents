---
title: "The enterprise AI stack behind Stripe’s company brain “Kai”"
type: "extract"
source: "youtube"
video_id: "AbZODZ_4VaM"
url: "https://www.youtube.com/watch?v=AbZODZ_4VaM"
channel: "How I AI"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-the-enterprise-ai-stack-behind-stripes-company-brain-kai--AbZODZ_4VaM.txt]]"
tags: ["agents", "harness", "harness-engineering", "context-engineering", "context-management", "governanca", "permissions", "gate-design", "escalation", "evals", "telemetry", "observability", "data-platform", "token-budgeting", "model-selection", "agent-tooling", "runtime", "knowledge-management", "production", "process"]
thesis: "Stripe construiu o Kai, um agente interno único para toda a empresa, cujo diferencial central é governança — 'projetos' como camada de escopo para modelos, tokens, políticas de ferramentas e human-in-the-loop, combinada com uma plataforma de skills com telemetria e ciclo de vida, rodando sobre infraestrutura de dados pré-endurecida."
concepts: ["governança como razão primária para construir um agente interno em vez de adotar ferramentas prontas", "projetos como unidade de governança: modelo padrão, restrição de modelos caros, orçamento de tokens, conectores e políticas de ferramentas definidos pelo DRI do espaço", "tool policies com human-in-the-loop aplicado apenas a ferramentas sensíveis por workflow", "motor de contexto personalizado com controle de acesso pelo usuário final (opt-in para Drive, Slack, DMs, revogável por sessão)", "org chart e projetos do usuário como sinal forte de intenção", "sandbox seguro por sessão na nuvem com ferramentas controladas de entrada, execução e saída de dados", "roteamento e recuperação de skills em escala (~2000 skills, sem hierarquia natural de repositório)", "lifecycle de skills: telemetria de invocação, promoção/demote entre workflows, depreciação, sugestões automáticas de melhoria", "quantidade de skills como facet de qualidade (poluição de contexto degrada resultados)", "triagem de 3 camadas para agentes de dados: artefatos existentes → analytics layer abençoada → data catalog com query própria", "resiliência do warehouse a queries de alto volume (agentes fazem brute force por padrão)", "identidade agêntica na infraestrutura para priorização e load shedding", "iteração multi-turn de artefatos compartilhados (centenas de turns ao longo de semanas, eficiência de tokens)", "'light apps' de last-mile data criadas por não-engenheiros via agente com sandbox", "alavancagem de investimentos pré-IA em DevX, data platform e analytics layers", "rollout enxuto: V0 com 1,5 pessoas em 2 semanas, piloto, demo company-wide, core team <10 pessoas para 10k+ usuários semanais"]
tools: ["Kai (agente interno do Stripe)", "Hubble (camada de query de dados do Stripe)", "Trino", "Google Drive", "Slack", "Google Calendar", "Gemini", "Cursor", "Lovable", "minions (ferramenta interna do Stripe)", "DX", "Hyper Agent"]
people: ["Sherrod", "Claire", "Anupam", "Ilia", "Stripe", "DX", "Hyper Agent"]
claims: ["Trate a construção de um agente interno primariamente como problema de governança, não de acesso a IA.", "Use 'projetos' como camada de configuração e governança: modelo padrão, modelos bloqueados por custo, budget de tokens, conectores e políticas de ferramentas definidos por poucos especialistas (DRI) para todos do projeto.", "Configure human-in-the-loop apenas para ferramentas sensíveis dentro da política do projeto; aplicar a toda sessão gera fricção que induz humanos a contornos inseguros.", "Projete agentes de dados com fallback em cascata: dashboards/relatórios existentes → analytics layer com métricas-chave → catálogo de dados com query própria, para evitar queries e tabelas erradas.", "Endureça o data warehouse contra queries de alto volume porque agentes fazem brute force quando em dúvida; agentes multiplicam a amplitude de todos os modos de falha existentes.", "Investimentos pré-IA em DevX, data platform e analytics layers são a principal alavancagem de eficácia de agentes — 'dobre o tamanho do time de DevX e do time de dados'.", "Dê a cada sessão um sandbox seguro na nuvem com ferramentas controladas de entrada/saída de dados para que não-engenheiros possam executar código gerado pelo agente com segurança.", "Prefira iterar sobre artefatos compartilhados em conversas multi-turn em vez de regenerá-los, por eficiência de tokens e para tratar o agente como colaborador.", "Transforme sessões em skills reutilizáveis via skill-creator, em spec aberta portável entre harnesses, com editor tipo IDE, descrição e gatilhos de uso gerados automaticamente.", "Opere a biblioteca de skills com telemetria: promova skills de alto uso ao workflow geral, delegue as de cauda longa e deprecione skills não invocadas (ex.: aviso após 30 dias, arquivamento e exclusão).", "Trate quantidade de skills como problema de qualidade: contexto não relacionado degrada os resultados do modelo.", "Adote identidade agêntica na infraestrutura (quem é o agente e qual caso de uso) para suportar priorização e load shedding.", "Deixe o usuário final controlar quanto contexto pessoal (Drive, Slack, DMs) o agente ingere, sessão a sessão.", "Valide rápido com um V0 barato (1,5 pessoas, 2 semanas) e um demo company-wide para disparar adoção; um core team de <10 pessoas pode servir 10k+ usuários semanais com apoio de coding agents e infraestrutura existente."]
deep_dive: "high"
deep_dive_reason: "Alta densidade de decisões arquiteturais acionáveis e relativamente novas (projetos como camada de governança com model routing e tool policies, roteamento e lifecycle de ~2000 skills com telemetria, triagem em cascata para agentes de dados sobre warehouse resiliente), diretamente relevantes a harness, context-engineering, evals e governança de agentes em produção."
---

# The enterprise AI stack behind Stripe’s company brain “Kai”

## Tese
Stripe construiu o Kai, um agente interno único para toda a empresa, cujo diferencial central é governança — 'projetos' como camada de escopo para modelos, tokens, políticas de ferramentas e human-in-the-loop, combinada com uma plataforma de skills com telemetria e ciclo de vida, rodando sobre infraestrutura de dados pré-endurecida.

## Conceitos-chave
- governança como razão primária para construir um agente interno em vez de adotar ferramentas prontas
- projetos como unidade de governança: modelo padrão, restrição de modelos caros, orçamento de tokens, conectores e políticas de ferramentas definidos pelo DRI do espaço
- tool policies com human-in-the-loop aplicado apenas a ferramentas sensíveis por workflow
- motor de contexto personalizado com controle de acesso pelo usuário final (opt-in para Drive, Slack, DMs, revogável por sessão)
- org chart e projetos do usuário como sinal forte de intenção
- sandbox seguro por sessão na nuvem com ferramentas controladas de entrada, execução e saída de dados
- roteamento e recuperação de skills em escala (~2000 skills, sem hierarquia natural de repositório)
- lifecycle de skills: telemetria de invocação, promoção/demote entre workflows, depreciação, sugestões automáticas de melhoria
- quantidade de skills como facet de qualidade (poluição de contexto degrada resultados)
- triagem de 3 camadas para agentes de dados: artefatos existentes → analytics layer abençoada → data catalog com query própria
- resiliência do warehouse a queries de alto volume (agentes fazem brute force por padrão)
- identidade agêntica na infraestrutura para priorização e load shedding
- iteração multi-turn de artefatos compartilhados (centenas de turns ao longo de semanas, eficiência de tokens)
- 'light apps' de last-mile data criadas por não-engenheiros via agente com sandbox
- alavancagem de investimentos pré-IA em DevX, data platform e analytics layers
- rollout enxuto: V0 com 1,5 pessoas em 2 semanas, piloto, demo company-wide, core team <10 pessoas para 10k+ usuários semanais

## Ferramentas & pessoas
**Ferramentas:** Kai (agente interno do Stripe), Hubble (camada de query de dados do Stripe), Trino, Google Drive, Slack, Google Calendar, Gemini, Cursor, Lovable, minions (ferramenta interna do Stripe), DX, Hyper Agent

**Pessoas/orgs:** Sherrod, Claire, Anupam, Ilia, Stripe, DX, Hyper Agent

## Claims acionáveis
- Trate a construção de um agente interno primariamente como problema de governança, não de acesso a IA.
- Use 'projetos' como camada de configuração e governança: modelo padrão, modelos bloqueados por custo, budget de tokens, conectores e políticas de ferramentas definidos por poucos especialistas (DRI) para todos do projeto.
- Configure human-in-the-loop apenas para ferramentas sensíveis dentro da política do projeto; aplicar a toda sessão gera fricção que induz humanos a contornos inseguros.
- Projete agentes de dados com fallback em cascata: dashboards/relatórios existentes → analytics layer com métricas-chave → catálogo de dados com query própria, para evitar queries e tabelas erradas.
- Endureça o data warehouse contra queries de alto volume porque agentes fazem brute force quando em dúvida; agentes multiplicam a amplitude de todos os modos de falha existentes.
- Investimentos pré-IA em DevX, data platform e analytics layers são a principal alavancagem de eficácia de agentes — 'dobre o tamanho do time de DevX e do time de dados'.
- Dê a cada sessão um sandbox seguro na nuvem com ferramentas controladas de entrada/saída de dados para que não-engenheiros possam executar código gerado pelo agente com segurança.
- Prefira iterar sobre artefatos compartilhados em conversas multi-turn em vez de regenerá-los, por eficiência de tokens e para tratar o agente como colaborador.
- Transforme sessões em skills reutilizáveis via skill-creator, em spec aberta portável entre harnesses, com editor tipo IDE, descrição e gatilhos de uso gerados automaticamente.
- Opere a biblioteca de skills com telemetria: promova skills de alto uso ao workflow geral, delegue as de cauda longa e deprecione skills não invocadas (ex.: aviso após 30 dias, arquivamento e exclusão).
- Trate quantidade de skills como problema de qualidade: contexto não relacionado degrada os resultados do modelo.
- Adote identidade agêntica na infraestrutura (quem é o agente e qual caso de uso) para suportar priorização e load shedding.
- Deixe o usuário final controlar quanto contexto pessoal (Drive, Slack, DMs) o agente ingere, sessão a sessão.
- Valide rápido com um V0 barato (1,5 pessoas, 2 semanas) e um demo company-wide para disparar adoção; um core team de <10 pessoas pode servir 10k+ usuários semanais com apoio de coding agents e infraestrutura existente.

> **Deep dive:** `high` — Alta densidade de decisões arquiteturais acionáveis e relativamente novas (projetos como camada de governança com model routing e tool policies, roteamento e lifecycle de ~2000 skills com telemetria, triagem em cascata para agentes de dados sobre warehouse resiliente), diretamente relevantes a harness, context-engineering, evals e governança de agentes em produção.
