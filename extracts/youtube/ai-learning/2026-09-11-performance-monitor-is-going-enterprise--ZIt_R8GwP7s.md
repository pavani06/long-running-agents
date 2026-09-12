---
title: "Performance Monitor is Going Enterprise"
type: "extract"
source: "youtube"
video_id: "ZIt_R8GwP7s"
url: "https://www.youtube.com/watch?v=ZIt_R8GwP7s"
channel: "Erik Darling (Erik Darling Data)"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-performance-monitor-is-going-enterprise--ZIt_R8GwP7s.txt]]"
tags: ["monitoramento", "observability", "telemetry", "data-platform", "arquitetura", "production", "stack-tooling", "agentic-coding", "permissions", "process"]
thesis: "Eric Darling está descontinuando o dashboard 'full' de sua ferramenta gratuita de monitoramento de SQL Server e migrando para uma arquitetura de serviço Windows headless que coleta dados continuamente para um backend gratuito Postgres com TimescaleDB, mantendo a versão portátil 'light' e unificando mais código entre os caminhos de visualização."
concepts: ["monitoramento de SQL Server", "serviço Windows headless desacoplado do viewer", "Postgres como backend gratuito", "extensão TimescaleDB para compressão temporal", "compressão COMPRESS/DECOMPRESS de query text, planos e XML de deadlocks", "TOAST e LZ4 no Postgres 18", "unificação de code paths para reduzir bugs duplicados", "segurança baseada em papéis (owner/admin/read-only)", "agent jobs como coletores", "multiusuário no mesmo conjunto de dados", "novas métricas: memory pressure, session stats, latch/spinlock, collection health", "visão de calendário no daily summary", "perfmon collector packs", "confusão de 'um banco por servidor' no modelo antigo"]
tools: ["Darling Data Performance Monitor", "SQL Server", "SQL Server Agent", "PostgreSQL", "TimescaleDB", "HammerDB", "CrystalDiskMark", "GitHub", "Claude (exército de agentes de código)"]
people: ["Eric Darling", "Darling Data", "Kendra Little", "Microsoft"]
claims: ["O dashboard 'full' está sendo descontinuado; a versão 'light' portátil (estilo zip executável) permanece disponível", "O novo coletor é um serviço Windows headless que roda independente de sessão de usuário e continua coletando enquanto a VM estiver ativa, alimentando o Postgres", "O viewer foi completamente desacoplado do serviço de coleta, permitindo múltiplos usuários consultando os mesmos dados simultaneamente", "O backend Postgres com TimescaleDB foi escolhido por ser gratuito e oferecer compressão excelente para dados volumosos como XML de deadlocks e planos de consulta", "É possível trazer sua própria instância Postgres ou provisionar uma nova VM dedicada", "Há três papéis de segurança: owner (tudo), admin (agendas, coletas e alertas) e read-only para visualização sem risco de alterações", "Muito mais do código do viewer agora é compartilhado entre light e a nova versão, reduzindo (mas não eliminando) o problema de corrigir bugs em dois caminhos", "O uso de agentes de IA (Claude) exigia vigilância para que correções fossem aplicadas em ambos os code paths sem descopeamento aleatório", "Novas métricas e visualizações foram promovidas do full: eventos de memory pressure, session stats, latch/spinlock, system events do extended event system_health, health do coletor e daily summary em calendário", "A ferramenta poderia escalar até cerca de 500 servidores, permanecendo totalmente gratuita sem custo por servidor, com doações e contratos de suporte opcionais", "O download está disponível em code.ericdarling.com, na seção performance monitor do repositório GitHub, com release previsto em poucos dias"]
deep_dive: "low"
deep_dive_reason: "Trata-se de um anúncio promocional de roadmap de produto com decisões arquiteturais razoáveis mas convencionais (migração de backend e desacoplamento de serviço), sem densidade de insight sobre harness, context-engineering, evals, agent-fleets ou governança de agentes."
relates-to: []
theme: "Monitoramento Enterprise de SQL Server"
---

# Performance Monitor is Going Enterprise

## Tese
Eric Darling está descontinuando o dashboard 'full' de sua ferramenta gratuita de monitoramento de SQL Server e migrando para uma arquitetura de serviço Windows headless que coleta dados continuamente para um backend gratuito Postgres com TimescaleDB, mantendo a versão portátil 'light' e unificando mais código entre os caminhos de visualização.

## Conceitos-chave
- monitoramento de SQL Server
- serviço Windows headless desacoplado do viewer
- Postgres como backend gratuito
- extensão TimescaleDB para compressão temporal
- compressão COMPRESS/DECOMPRESS de query text, planos e XML de deadlocks
- TOAST e LZ4 no Postgres 18
- unificação de code paths para reduzir bugs duplicados
- segurança baseada em papéis (owner/admin/read-only)
- agent jobs como coletores
- multiusuário no mesmo conjunto de dados
- novas métricas: memory pressure, session stats, latch/spinlock, collection health
- visão de calendário no daily summary
- perfmon collector packs
- confusão de 'um banco por servidor' no modelo antigo

## Ferramentas & pessoas
**Ferramentas:** Darling Data Performance Monitor, SQL Server, SQL Server Agent, PostgreSQL, TimescaleDB, HammerDB, CrystalDiskMark, GitHub, Claude (exército de agentes de código)

**Pessoas/orgs:** Eric Darling, Darling Data, Kendra Little, Microsoft

## Claims acionáveis
- O dashboard 'full' está sendo descontinuado; a versão 'light' portátil (estilo zip executável) permanece disponível
- O novo coletor é um serviço Windows headless que roda independente de sessão de usuário e continua coletando enquanto a VM estiver ativa, alimentando o Postgres
- O viewer foi completamente desacoplado do serviço de coleta, permitindo múltiplos usuários consultando os mesmos dados simultaneamente
- O backend Postgres com TimescaleDB foi escolhido por ser gratuito e oferecer compressão excelente para dados volumosos como XML de deadlocks e planos de consulta
- É possível trazer sua própria instância Postgres ou provisionar uma nova VM dedicada
- Há três papéis de segurança: owner (tudo), admin (agendas, coletas e alertas) e read-only para visualização sem risco de alterações
- Muito mais do código do viewer agora é compartilhado entre light e a nova versão, reduzindo (mas não eliminando) o problema de corrigir bugs em dois caminhos
- O uso de agentes de IA (Claude) exigia vigilância para que correções fossem aplicadas em ambos os code paths sem descopeamento aleatório
- Novas métricas e visualizações foram promovidas do full: eventos de memory pressure, session stats, latch/spinlock, system events do extended event system_health, health do coletor e daily summary em calendário
- A ferramenta poderia escalar até cerca de 500 servidores, permanecendo totalmente gratuita sem custo por servidor, com doações e contratos de suporte opcionais
- O download está disponível em code.ericdarling.com, na seção performance monitor do repositório GitHub, com release previsto em poucos dias

> **Deep dive:** `low` — Trata-se de um anúncio promocional de roadmap de produto com decisões arquiteturais razoáveis mas convencionais (migração de backend e desacoplamento de serviço), sem densidade de insight sobre harness, context-engineering, evals, agent-fleets ou governança de agentes.
