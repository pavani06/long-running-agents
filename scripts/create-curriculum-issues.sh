#!/usr/bin/env bash
# =============================================================================
# create-curriculum-issues.sh
#
# Script de criacao em lote de ~65 issues para completar o curriculo
# Long-Running Agents para KODA.
#
# Uso:
#   chmod +x scripts/create-curriculum-issues.sh
#   ./scripts/create-curriculum-issues.sh
#
# Pre-requisitos:
#   - gh CLI autenticado (gh auth status)
#   - Labels e milestones ja criados (ver setup inicial no plano)
#
# Data: Maio 2026
# Repo: pavani06/long-running-agents
# =============================================================================

set -euo pipefail

REPO="pavani06/long-running-agents"

echo "============================================"
echo " Criando ~65 Issues do Curriculo Long-Running Agents"
echo " Repo: $REPO"
echo "============================================"
echo ""

# ---------------------------------------------------------------------------
# BLOCK A: Nivel 3 — Arquitetura Avancada (12 issues)
# Milestone: "Nivel 3 — Arquitetura Avancada"
# ---------------------------------------------------------------------------
echo ">>> Bloco A — Nivel 3: Arquitetura Avancada (12 issues)"

# A1 — Modulo 01: Multi-Agent Systems
gh issue create \
  --repo "$REPO" \
  --title "[Nivel 3] Criar 01-multi-agent-systems.md — Multi-Agent Systems" \
  --label "curriculum/nivel-3,type/content,priority/high" \
  --milestone "Nivel 3 — Arquitetura Avancada" \
  --body "$(cat <<'ISSUE_EOF'
## Arquivo a Criar
`curriculum/03-nivel-3-advanced-architecture/01-multi-agent-systems.md`

## Descricao do Modulo
Design de sistemas com 3+ agentes coordenados. Cobre o padrao Planner/Generator/Evaluator, canais de comunicacao entre agentes, strategies de coordenacao (sequencial, paralelo, event-driven) e aplicacao no contexto KODA.

## Topicos a Cobrir
- [ ] Arquitetura multi-agente: Planner, Generator, Evaluator
- [ ] Canais de comunicacao entre agentes (files, queues, API)
- [ ] Strategies de coordenacao (sequencial, paralelo, event-driven)
- [ ] Aplicacao KODA: decomposicao do customer journey em agentes

## Requisitos de Conteudo
- [ ] Prologo narrativo com cenario KODA realista
- [ ] Diagrama ASCII da arquitetura 3-agent
- [ ] Tabela comparativa de strategies de coordenacao
- [ ] Secao "Aplicacao KODA"
- [ ] Conexao explicita com padrao Generator/Evaluator do Nivel 2
- [ ] Minimo 800 linhas de conteudo

## Criterios de Aceitacao
- [ ] Arquivo existe no caminho correto
- [ ] Segue template de modulo (cabecalho, prologo, secoes com emojis)
- [ ] Portugues brasileiro com termos tecnicos em ingles
- [ ] Nenhum placeholder "TBD" ou "TODO"

## Dependencias
- Nivel 1 e Nivel 2 concluidos (ja existem)
ISSUE_EOF
)"

echo "  [OK] A1 — 01-multi-agent-systems.md"

# A2 — Modulo 02: State Persistence
gh issue create \
  --repo "$REPO" \
  --title "[Nivel 3] Criar 02-state-persistence.md — State Persistence" \
  --label "curriculum/nivel-3,type/content,priority/high" \
  --milestone "Nivel 3 — Arquitetura Avancada" \
  --body "$(cat <<'ISSUE_EOF'
## Arquivo a Criar
`curriculum/03-nivel-3-advanced-architecture/02-state-persistence.md`

## Descricao do Modulo
Estrategias para persistir estado entre sessoes de agentes. Cobre SQLite, JSON files, checkpointing, recovery strategies e como estado persiste atraves de falhas. Aplicacao KODA: persistindo pedidos, customer state, e progresso de conversas.

## Topicos a Cobrir
- [ ] Por que agentes precisam de persistencia de estado
- [ ] SQLite vs JSON files vs Redis
- [ ] Checkpointing patterns (snapshot, incremental)
- [ ] Recovery strategies (rollback, replay)
- [ ] Aplicacao KODA: customer state machine

## Requisitos de Conteudo
- [ ] Prologo narrativo com cenario KODA (conversa interrompida)
- [ ] Diagrama ASCII de state machine
- [ ] Exemplo de codigo para checkpoint
- [ ] Tabela comparativa de backends de persistencia
- [ ] Minimo 700 linhas

## Criterios de Aceitacao
- [ ] Arquivo existe no caminho correto
- [ ] Segue template de modulo
- [ ] Portugues brasileiro com termos tecnicos em ingles
- [ ] Nenhum placeholder

## Dependencias
- Nivel 1 e Nivel 2 concluidos
ISSUE_EOF
)"

echo "  [OK] A2 — 02-state-persistence.md"

# A3 — Modulo 03: File-Based Coordination
gh issue create \
  --repo "$REPO" \
  --title "[Nivel 3] Criar 03-file-based-coordination.md — File-Based Coordination" \
  --label "curriculum/nivel-3,type/content,priority/high" \
  --milestone "Nivel 3 — Arquitetura Avancada" \
  --body "$(cat <<'ISSUE_EOF'
## Arquivo a Criar
`curriculum/03-nivel-3-advanced-architecture/03-file-based-coordination.md`

## Descricao do Modulo
Coordenacao entre agentes usando sistema de arquivos como barramento de comunicacao. Cobre lock files, status files, JSON protocol entre agentes. Aplicacao KODA: coordenacao entre discovery, pedido e fulfillment.

## Topicos a Cobrir
- [ ] File-based coordination como padrao
- [ ] Lock files e concorrencia
- [ ] Status files e state machines
- [ ] JSON protocol entre agentes
- [ ] Aplicacao KODA: pipeline de pedidos

## Requisitos de Conteudo
- [ ] Prologo narrativo com cenario KODA
- [ ] Diagrama ASCII de pipeline de arquivos
- [ ] Exemplo de codigo para lock file manager
- [ ] Tabela de tipos de arquivo e propositos
- [ ] Minimo 600 linhas

## Criterios de Aceitacao
- [ ] Arquivo existe no caminho correto
- [ ] Segue template de modulo
- [ ] Portugues brasileiro com termos tecnicos em ingles
- [ ] Nenhum placeholder

## Dependencias
- 01-multi-agent-systems.md
ISSUE_EOF
)"

echo "  [OK] A3 — 03-file-based-coordination.md"

# A4 — Modulo 04: Server-Side Compaction
gh issue create \
  --repo "$REPO" \
  --title "[Nivel 3] Criar 04-server-side-compaction.md — Server-Side Compaction" \
  --label "curriculum/nivel-3,type/content,priority/high" \
  --milestone "Nivel 3 — Arquitetura Avancada" \
  --body "$(cat <<'ISSUE_EOF'
## Arquivo a Criar
`curriculum/03-nivel-3-advanced-architecture/04-server-side-compaction.md`

## Descricao do Modulo
Tecnicas de compactacao de contexto no lado do servidor para manter agentes eficientes em sessoes longas. Cobre summarization, chunking, sliding windows server-side. Aplicacao KODA: compactando historico de conversas WhatsApp.

## Topicos a Cobrir
- [ ] Por que compactar no servidor vs cliente
- [ ] Summarization strategies (extractive vs abstractive)
- [ ] Chunking e priorizacao de contexto
- [ ] Sliding windows adaptativos
- [ ] Aplicacao KODA: compactacao de conversas 2h+

## Requisitos de Conteudo
- [ ] Prologo narrativo com cenario KODA (conversa longa)
- [ ] Diagrama ASCII de pipeline de compactacao
- [ ] Metricas: "75% → 98% de retencao de contexto"
- [ ] Tabela comparativa de strategies
- [ ] Minimo 600 linhas

## Criterios de Aceitacao
- [ ] Arquivo existe no caminho correto
- [ ] Segue template de modulo
- [ ] Portugues brasileiro com termos tecnicos em ingles
- [ ] Nenhum placeholder

## Dependencias
- 02-state-persistence.md
ISSUE_EOF
)"

echo "  [OK] A4 — 04-server-side-compaction.md"

# A5 — Modulo 05: Harness Evolution
gh issue create \
  --repo "$REPO" \
  --title "[Nivel 3] Criar 05-harness-evolution.md — Harness Evolution" \
  --label "curriculum/nivel-3,type/content,priority/high" \
  --milestone "Nivel 3 — Arquitetura Avancada" \
  --body "$(cat <<'ISSUE_EOF'
## Arquivo a Criar
`curriculum/03-nivel-3-advanced-architecture/05-harness-evolution.md`

## Descricao do Modulo
Como evoluir o harness de agentes conforme os modelos melhoram. Cobre remocao de scaffolding, simplificacao de patterns, quando e como remover componentes do harness. Aplicacao KODA: roadmap de evolucao do harness atual.

## Topicos a Cobrir
- [ ] Ciclo de vida do harness: build → stabilize → simplify → remove
- [ ] Sinais de que um componente pode ser removido
- [ ] Quando modelos mais fortes mudam o design
- [ ] Estrategia de evolucao incremental

## Requisitos de Conteudo
- [ ] Prologo narrativo com cenario KODA
- [ ] Diagrama ASCII de evolucao em timeline
- [ ] Tabela: "componentes atuais → evolucao planejada"
- [ ] Checklist de remocao de scaffolding
- [ ] Minimo 700 linhas

## Criterios de Aceitacao
- [ ] Arquivo existe no caminho correto
- [ ] Segue template de modulo
- [ ] Portugues brasileiro com termos tecnicos em ingles
- [ ] Nenhum placeholder

## Dependencias
- Modulos 01-04 do Nivel 3
ISSUE_EOF
)"

echo "  [OK] A5 — 05-harness-evolution.md"

# A6 — Exercicio 01: Multi-Agent Design
gh issue create \
  --repo "$REPO" \
  --title "[Exercicio] Criar exercise-01.md — Nivel 3 — Multi-Agent Design" \
  --label "curriculum/nivel-3,curriculum/exercises,type/exercise,priority/medium" \
  --milestone "Nivel 3 — Arquitetura Avancada" \
  --body "$(cat <<'ISSUE_EOF'
## Arquivo a Criar
`curriculum/03-nivel-3-advanced-architecture/exercises/exercise-01.md`

## Topico do Exercicio
Implementar um sistema 3-agent (Planner/Generator/Evaluator) para uma feature do KODA.

## Requisitos
- [ ] Cenario realista com problema contextualizado
- [ ] Lista de requisitos funcionais e tecnicos
- [ ] Codigo Python completo (minimo 200 linhas)
- [ ] Secao de validacao com testes esperados
- [ ] Dificuldade: 4 estrelas

## Criterios de Aceitacao
- [ ] Aluno consegue implementar em 60-90 minutos
- [ ] Exercicio testa compreensao, nao apenas copia-cola
- [ ] Solucao incluida em `exercises/solutions/`

## Dependencias
- 01-multi-agent-systems.md deve existir primeiro
ISSUE_EOF
)"

echo "  [OK] A6 — exercise-01.md (Nivel 3)"

# A7 — Exercicio 02: State Persistence Implementation
gh issue create \
  --repo "$REPO" \
  --title "[Exercicio] Criar exercise-02.md — Nivel 3 — State Persistence" \
  --label "curriculum/nivel-3,curriculum/exercises,type/exercise,priority/medium" \
  --milestone "Nivel 3 — Arquitetura Avancada" \
  --body "$(cat <<'ISSUE_EOF'
## Arquivo a Criar
`curriculum/03-nivel-3-advanced-architecture/exercises/exercise-02.md`

## Topico do Exercicio
Implementar checkpointing e recovery de estado para agente KODA usando SQLite.

## Requisitos
- [ ] Cenario realista com problema contextualizado
- [ ] Lista de requisitos funcionais e tecnicos
- [ ] Codigo Python completo (minimo 200 linhas)
- [ ] Secao de validacao com testes de recovery
- [ ] Dificuldade: 4 estrelas

## Criterios de Aceitacao
- [ ] Aluno consegue implementar em 60-90 minutos
- [ ] Exercicio testa compreensao, nao apenas copia-cola
- [ ] Solucao incluida em `exercises/solutions/`

## Dependencias
- 02-state-persistence.md deve existir primeiro
ISSUE_EOF
)"

echo "  [OK] A7 — exercise-02.md (Nivel 3)"

# A8 — Exercicio 03: Harness Evolution Plan
gh issue create \
  --repo "$REPO" \
  --title "[Exercicio] Criar exercise-03.md — Nivel 3 — Harness Evolution" \
  --label "curriculum/nivel-3,curriculum/exercises,type/exercise,priority/medium" \
  --milestone "Nivel 3 — Arquitetura Avancada" \
  --body "$(cat <<'ISSUE_EOF'
## Arquivo a Criar
`curriculum/03-nivel-3-advanced-architecture/exercises/exercise-03.md`

## Topico do Exercicio
Analisar um harness existente do KODA e propor um plano de evolucao com 3 fases.

## Requisitos
- [ ] Cenario realista com harness KODA atual
- [ ] Lista de requisitos funcionais e tecnicos
- [ ] Template de plano de evolucao (3 fases)
- [ ] Secao de validacao com criterios de sucesso por fase
- [ ] Dificuldade: 3 estrelas

## Criterios de Aceitacao
- [ ] Aluno consegue completar em 60-90 minutos
- [ ] Exercicio testa pensamento arquitetonico
- [ ] Solucao incluida em `exercises/solutions/`

## Dependencias
- 05-harness-evolution.md deve existir primeiro
ISSUE_EOF
)"

echo "  [OK] A8 — exercise-03.md (Nivel 3)"

# A9 — Solucao Exercicio 01
gh issue create \
  --repo "$REPO" \
  --title "[Solucao] Criar solution-exercise-01.md — Nivel 3 — Multi-Agent Design" \
  --label "curriculum/nivel-3,curriculum/exercises,type/exercise,priority/low" \
  --milestone "Nivel 3 — Arquitetura Avancada" \
  --body "$(cat <<'ISSUE_EOF'
## Arquivo a Criar
`curriculum/03-nivel-3-advanced-architecture/exercises/solutions/exercise-01-solution.md`

## Descricao
Solucao completa do exercicio de Multi-Agent Design, incluindo codigo Python funcional para o sistema 3-agent Planner/Generator/Evaluator.

## Requisitos
- [ ] Codigo Python completo e funcional
- [ ] Explicacao da arquitetura e decisoes de design
- [ ] Testes que validam o funcionamento
- [ ] Alternativas de implementacao comentadas

## Dependencias
- exercise-01.md deve existir primeiro
ISSUE_EOF
)"

echo "  [OK] A9 — solution-exercise-01.md (Nivel 3)"

# A10 — Solucao Exercicio 02
gh issue create \
  --repo "$REPO" \
  --title "[Solucao] Criar solution-exercise-02.md — Nivel 3 — State Persistence" \
  --label "curriculum/nivel-3,curriculum/exercises,type/exercise,priority/low" \
  --milestone "Nivel 3 — Arquitetura Avancada" \
  --body "$(cat <<'ISSUE_EOF'
## Arquivo a Criar
`curriculum/03-nivel-3-advanced-architecture/exercises/solutions/exercise-02-solution.md`

## Descricao
Solucao completa do exercicio de State Persistence, incluindo codigo Python funcional para checkpointing com SQLite e recovery.

## Requisitos
- [ ] Codigo Python completo e funcional
- [ ] Explicacao das decisoes de persistencia
- [ ] Testes de recovery apos falha simulada

## Dependencias
- exercise-02.md deve existir primeiro
ISSUE_EOF
)"

echo "  [OK] A10 — solution-exercise-02.md (Nivel 3)"

# A11 — Solucao Exercicio 03
gh issue create \
  --repo "$REPO" \
  --title "[Solucao] Criar solution-exercise-03.md — Nivel 3 — Harness Evolution" \
  --label "curriculum/nivel-3,curriculum/exercises,type/exercise,priority/low" \
  --milestone "Nivel 3 — Arquitetura Avancada" \
  --body "$(cat <<'ISSUE_EOF'
## Arquivo a Criar
`curriculum/03-nivel-3-advanced-architecture/exercises/solutions/exercise-03-solution.md`

## Descricao
Solucao completa do exercicio de Harness Evolution, incluindo plano detalhado de evolucao com 3 fases e justificativas.

## Requisitos
- [ ] Plano de evolucao detalhado para 3 fases
- [ ] Justificativas tecnicas para cada remocao/adicao
- [ ] Riscos e mitigacoes por fase

## Dependencias
- exercise-03.md deve existir primeiro
ISSUE_EOF
)"

echo "  [OK] A11 — solution-exercise-03.md (Nivel 3)"

# A12 — KODA Application Nivel 3
gh issue create \
  --repo "$REPO" \
  --title "[KODA App] Criar nivel-3-koda.md — Aplicacao KODA — Nivel 3" \
  --label "curriculum/nivel-3,type/content,priority/medium" \
  --milestone "Nivel 3 — Arquitetura Avancada" \
  --body "$(cat <<'ISSUE_EOF'
## Arquivo a Criar
`curriculum/03-nivel-3-advanced-architecture/koda-applications/nivel-3-koda.md`

## Descricao
Modulo de aplicacao pratica de todos os conceitos do Nivel 3 no contexto KODA. Conecta multi-agent systems, state persistence, file-based coordination, compaction e harness evolution ao agente de vendas WhatsApp.

## Requisitos
- [ ] Prologo narrativo com Fernando enfrentando desafio real
- [ ] Mapeamento de cada modulo do Nivel 3 para feature KODA
- [ ] Exemplos concretos de implementacao no KODA
- [ ] Metricas de impacto esperado

## Criterios de Aceitacao
- [ ] Arquivo existe no caminho correto
- [ ] Segue template de aplicacao KODA (nivel-1-koda.md, nivel-2-koda.md como referencia)
- [ ] Portugues brasileiro com termos tecnicos em ingles

## Dependencias
- Todos os modulos do Nivel 3 concluidos
ISSUE_EOF
)"

echo "  [OK] A12 — nivel-3-koda.md"

echo "  >> Bloco A concluido: 12 issues"
echo ""

# ---------------------------------------------------------------------------
# BLOCK B: Nivel 4 — KODA-Especifico (12 issues)
# Milestone: "Nivel 4 — KODA-Especifico"
# ---------------------------------------------------------------------------
echo ">>> Bloco B — Nivel 4: KODA-Especifico (12 issues)"

# B1 — Modulo 01: KODA Architecture
gh issue create \
  --repo "$REPO" \
  --title "[Nivel 4] Criar 01-koda-architecture.md — Arquitetura KODA" \
  --label "curriculum/nivel-4,type/content,priority/high" \
  --milestone "Nivel 4 — KODA-Especifico" \
  --body "$(cat <<'ISSUE_EOF'
## Arquivo a Criar
`curriculum/04-nivel-4-koda-specific/01-koda-architecture.md`

## Descricao do Modulo
Visao completa da arquitetura do KODA: componentes, fluxo de dados, integracao WhatsApp, pipeline de vendas. Cobre o estado atual da arquitetura e como cada componente se relaciona com os padroes de long-running agents.

## Topicos a Cobrir
- [ ] Visao geral da arquitetura KODA (component diagram)
- [ ] Fluxo de dados: WhatsApp → Agente → ML → Resposta
- [ ] Integracao com WhatsApp Business API
- [ ] Pipeline de vendas: discovery → pedido → fulfillment
- [ ] Estado atual do harness KODA

## Requisitos de Conteudo
- [ ] Prologo narrativo com Fernando apresentando o KODA
- [ ] Diagrama ASCII da arquitetura completa
- [ ] Tabela de componentes e responsabilidades
- [ ] Conexao explicita com padroes dos Niveis 1-3
- [ ] Minimo 1000 linhas

## Criterios de Aceitacao
- [ ] Arquivo existe no caminho correto
- [ ] Segue template de modulo
- [ ] Portugues brasileiro com termos tecnicos em ingles
- [ ] Nenhum placeholder

## Dependencias
- Niveis 1, 2 e 3 concluidos
ISSUE_EOF
)"

echo "  [OK] B1 — 01-koda-architecture.md"

# B2 — Modulo 02: Customer Journey Flows
gh issue create \
  --repo "$REPO" \
  --title "[Nivel 4] Criar 02-customer-journey-flows.md — Customer Journey Flows" \
  --label "curriculum/nivel-4,type/content,priority/high" \
  --milestone "Nivel 4 — KODA-Especifico" \
  --body "$(cat <<'ISSUE_EOF'
## Arquivo a Criar
`curriculum/04-nivel-4-koda-specific/02-customer-journey-flows.md`

## Descricao do Modulo
Mapeamento completo das jornadas de cliente no KODA. Cobre todos os fluxos: primeiro contato, descoberta de produto, negociacao, fechamento, pos-venda. Como os agentes gerenciam cada etapa.

## Topicos a Cobrir
- [ ] Jornada completa: awareness → consideration → decision → retention
- [ ] State machine por etapa
- [ ] Transicoes e condicoes de guarda
- [ ] Tratamento de excecoes e desvios
- [ ] Metricas por etapa (taxa de conversao, drop-off)

## Requisitos de Conteudo
- [ ] Prologo narrativo com jornada real de cliente
- [ ] Diagrama ASCII de state machine completa
- [ ] Tabela de metricas por etapa
- [ ] Exemplo de dialogo WhatsApp real
- [ ] Minimo 800 linhas

## Criterios de Aceitacao
- [ ] Arquivo existe no caminho correto
- [ ] Segue template de modulo
- [ ] Portugues brasileiro com termos tecnicos em ingles
- [ ] Nenhum placeholder

## Dependencias
- 01-koda-architecture.md
ISSUE_EOF
)"

echo "  [OK] B2 — 02-customer-journey-flows.md"

# B3 — Modulo 03: Feature Design Patterns
gh issue create \
  --repo "$REPO" \
  --title "[Nivel 4] Criar 03-feature-design-patterns.md — Feature Design Patterns" \
  --label "curriculum/nivel-4,type/content,priority/high" \
  --milestone "Nivel 4 — KODA-Especifico" \
  --body "$(cat <<'ISSUE_EOF'
## Arquivo a Criar
`curriculum/04-nivel-4-koda-specific/03-feature-design-patterns.md`

## Descricao do Modulo
Padroes de design para novas features no KODA. Cobre como estender o agente com novas capacidades mantendo qualidade. Templates de contrato de feature, checklist de implementacao e padroes de integracao.

## Topicos a Cobrir
- [ ] Anatomia de uma feature KODA (contract, generator, evaluator)
- [ ] Feature contract template
- [ ] Integracao com pipeline existente
- [ ] Testing e validacao de nova feature
- [ ] Exemplos: recomendacao de produto, upsell, follow-up

## Requisitos de Conteudo
- [ ] Prologo narrativo com nova feature sendo implementada
- [ ] Diagrama ASCII de integracao de feature
- [ ] Template de contrato preenchido com exemplo
- [ ] Checklist de implementacao
- [ ] Minimo 700 linhas

## Criterios de Aceitacao
- [ ] Arquivo existe no caminho correto
- [ ] Segue template de modulo
- [ ] Portugues brasileiro com termos tecnicos em ingles
- [ ] Nenhum placeholder

## Dependencias
- 01-koda-architecture.md, 02-customer-journey-flows.md
ISSUE_EOF
)"

echo "  [OK] B3 — 03-feature-design-patterns.md"

# B4 — Modulo 04: Evaluation Rubrics KODA
gh issue create \
  --repo "$REPO" \
  --title "[Nivel 4] Criar 04-evaluation-rubrics-koda.md — Evaluation Rubrics para KODA" \
  --label "curriculum/nivel-4,type/content,priority/high" \
  --milestone "Nivel 4 — KODA-Especifico" \
  --body "$(cat <<'ISSUE_EOF'
## Arquivo a Criar
`curriculum/04-nivel-4-koda-specific/04-evaluation-rubrics-koda.md`

## Descricao do Modulo
Rubrics de avaliacao especificas para outputs do KODA. Cobre criterios de qualidade para recomendacoes de produto, respostas a clientes, negociacao de preco e follow-ups. Integracao com generator/evaluator pattern.

## Topicos a Cobrir
- [ ] Criterios de qualidade para cada tipo de output KODA
- [ ] Rubric de recomendacao de produto (precisao, relevancia, tom)
- [ ] Rubric de negociacao (assertividade, respeito, fechamento)
- [ ] Rubric de follow-up (timing, personalizacao)
- [ ] Integracao com evaluator agent

## Requisitos de Conteudo
- [ ] Prologo narrativo com avaliacao de qualidade real
- [ ] Tabelas de rubrics para cada tipo de output
- [ ] Exemplos de outputs bons vs ruins
- [ ] Checklist de validacao de qualidade
- [ ] Minimo 700 linhas

## Criterios de Aceitacao
- [ ] Arquivo existe no caminho correto
- [ ] Segue template de modulo
- [ ] Portugues brasileiro com termos tecnicos em ingles
- [ ] Nenhum placeholder

## Dependencias
- 02-nivel-2-practical-patterns/03-rubric-design.md
ISSUE_EOF
)"

echo "  [OK] B4 — 04-evaluation-rubrics-koda.md"

# B5 — Modulo 05: Harness Improvements
gh issue create \
  --repo "$REPO" \
  --title "[Nivel 4] Criar 05-harness-improvements.md — Melhorias de Harness KODA" \
  --label "curriculum/nivel-4,type/content,priority/high" \
  --milestone "Nivel 4 — KODA-Especifico" \
  --body "$(cat <<'ISSUE_EOF'
## Arquivo a Criar
`curriculum/04-nivel-4-koda-specific/05-harness-improvements.md`

## Descricao do Modulo
Plano concreto de melhorias para o harness do KODA baseado nos padroes aprendidos. Cobre diagnostico do harness atual, gaps identificados, propostas de melhoria com justificativas e roadmap de implementacao.

## Topicos a Cobrir
- [ ] Diagnostico do harness atual do KODA
- [ ] Gaps identificados (com dados de suporte)
- [ ] Propostas de melhoria priorizadas
- [ ] Roadmap de implementacao (curto, medio, longo prazo)
- [ ] Metricas de sucesso para cada melhoria

## Requisitos de Conteudo
- [ ] Prologo narrativo com problema real identificado
- [ ] Diagrama ASCII do harness atual vs proposto
- [ ] Tabela de melhorias com impacto estimado
- [ ] Checklist de implementacao por fase
- [ ] Minimo 800 linhas

## Criterios de Aceitacao
- [ ] Arquivo existe no caminho correto
- [ ] Segue template de modulo
- [ ] Portugues brasileiro com termos tecnicos em ingles
- [ ] Nenhum placeholder

## Dependencias
- 05-harness-evolution.md (Nivel 3), 01-koda-architecture.md
ISSUE_EOF
)"

echo "  [OK] B5 — 05-harness-improvements.md"

# B6 — Exercicio 01: Real-World KODA Feature
gh issue create \
  --repo "$REPO" \
  --title "[Exercicio] Criar exercise-01.md — Nivel 4 — Real-World KODA Feature" \
  --label "curriculum/nivel-4,curriculum/exercises,type/exercise,priority/medium" \
  --milestone "Nivel 4 — KODA-Especifico" \
  --body "$(cat <<'ISSUE_EOF'
## Arquivo a Criar
`curriculum/04-nivel-4-koda-specific/real-world-exercises/exercise-01.md`

## Topico do Exercicio
Implementar uma feature completa de recomendacao de produto no KODA usando generator/evaluator pattern.

## Requisitos
- [ ] Cenario realista com contexto KODA
- [ ] Especificacao de feature contract
- [ ] Codigo Python do generator e evaluator
- [ ] Testes de qualidade com rubrics
- [ ] Dificuldade: 5 estrelas

## Criterios de Aceitacao
- [ ] Aluno consegue implementar em 90-120 minutos
- [ ] Feature integra com pipeline KODA existente
- [ ] Solucao incluida em `real-world-exercises/solutions/`

## Dependencias
- 03-feature-design-patterns.md, 04-evaluation-rubrics-koda.md
ISSUE_EOF
)"

echo "  [OK] B6 — exercise-01.md (Nivel 4)"

# B7 — Exercicio 02: Full Customer Journey
gh issue create \
  --repo "$REPO" \
  --title "[Exercicio] Criar exercise-02.md — Nivel 4 — Full Customer Journey" \
  --label "curriculum/nivel-4,curriculum/exercises,type/exercise,priority/medium" \
  --milestone "Nivel 4 — KODA-Especifico" \
  --body "$(cat <<'ISSUE_EOF'
## Arquivo a Criar
`curriculum/04-nivel-4-koda-specific/real-world-exercises/exercise-02.md`

## Topico do Exercicio
Implementar uma jornada completa de cliente no KODA com agentes coordenados: discovery → recomendacao → pedido → pos-venda.

## Requisitos
- [ ] Cenario realista com jornada completa
- [ ] Multi-agent coordination com file-based ou state persistence
- [ ] Codigo Python do pipeline completo
- [ ] Avaliacao com rubrics
- [ ] Dificuldade: 5 estrelas

## Criterios de Aceitacao
- [ ] Aluno consegue implementar em 120-180 minutos
- [ ] Pipeline cobre todas as etapas da jornada
- [ ] Solucao incluida em `real-world-exercises/solutions/`

## Dependencias
- 02-customer-journey-flows.md, 01-koda-architecture.md
ISSUE_EOF
)"

echo "  [OK] B7 — exercise-02.md (Nivel 4)"

# B8 — Solucao Exercicio 01 Nivel 4
gh issue create \
  --repo "$REPO" \
  --title "[Solucao] Criar solution-exercise-01.md — Nivel 4 — KODA Feature" \
  --label "curriculum/nivel-4,curriculum/exercises,type/exercise,priority/low" \
  --milestone "Nivel 4 — KODA-Especifico" \
  --body "$(cat <<'ISSUE_EOF'
## Arquivo a Criar
`curriculum/04-nivel-4-koda-specific/real-world-exercises/solutions/exercise-01-solution.md`

## Descricao
Solucao completa do exercicio de feature KODA: recomendacao de produto com generator/evaluator.

## Requisitos
- [ ] Codigo Python completo e funcional
- [ ] Feature contract preenchido
- [ ] Rubrics de avaliacao aplicadas
- [ ] Testes validando qualidade

## Dependencias
- real-world-exercises/exercise-01.md
ISSUE_EOF
)"

echo "  [OK] B8 — solution-exercise-01.md (Nivel 4)"

# B9 — Solucao Exercicio 02 Nivel 4
gh issue create \
  --repo "$REPO" \
  --title "[Solucao] Criar solution-exercise-02.md — Nivel 4 — Full Journey" \
  --label "curriculum/nivel-4,curriculum/exercises,type/exercise,priority/low" \
  --milestone "Nivel 4 — KODA-Especifico" \
  --body "$(cat <<'ISSUE_EOF'
## Arquivo a Criar
`curriculum/04-nivel-4-koda-specific/real-world-exercises/solutions/exercise-02-solution.md`

## Descricao
Solucao completa do exercicio de jornada completa: pipeline multi-agent para customer journey KODA.

## Requisitos
- [ ] Codigo Python do pipeline completo
- [ ] Coordenacao entre agentes documentada
- [ ] Avaliacao de qualidade por etapa

## Dependencias
- real-world-exercises/exercise-02.md
ISSUE_EOF
)"

echo "  [OK] B9 — solution-exercise-02.md (Nivel 4)"

# B10 — Case Study 01: KODA Feature Launch
gh issue create \
  --repo "$REPO" \
  --title "[Case Study] Criar case-study-01.md — Nivel 4 — KODA Feature Launch" \
  --label "curriculum/nivel-4,type/content,priority/medium" \
  --milestone "Nivel 4 — KODA-Especifico" \
  --body "$(cat <<'ISSUE_EOF'
## Arquivo a Criar
`curriculum/04-nivel-4-koda-specific/case-studies/case-study-01.md`

## Descricao
Case study de lancamento de uma nova feature no KODA usando padroes de long-running agents. Cobre o processo completo: diagnostico, design, implementacao, validacao e resultados.

## Requisitos
- [ ] Contexto do problema e metricas iniciais
- [ ] Abordagem inicial e falhas encontradas
- [ ] Solucao final com padroes aplicados
- [ ] Diagrama ASCII da arquitetura
- [ ] Metricas comparativas (antes vs depois)
- [ ] Licoes aprendidas

## Criterios de Aceitacao
- [ ] Arquivo existe no caminho correto
- [ ] Segue template de case study
- [ ] Minimo 600 linhas

## Dependencias
- Nivel 4 modulos 01-05
ISSUE_EOF
)"

echo "  [OK] B10 — case-study-01.md (Nivel 4)"

# B11 — Case Study 02: KODA Scale-Up
gh issue create \
  --repo "$REPO" \
  --title "[Case Study] Criar case-study-02.md — Nivel 4 — KODA Scale-Up" \
  --label "curriculum/nivel-4,type/content,priority/medium" \
  --milestone "Nivel 4 — KODA-Especifico" \
  --body "$(cat <<'ISSUE_EOF'
## Arquivo a Criar
`curriculum/04-nivel-4-koda-specific/case-studies/case-study-02.md`

## Descricao
Case study de escalamento do KODA de 100 para 10.000 conversas/dia. Cobre desafios de escala, evolucao do harness e estrategias de otimizacao.

## Requisitos
- [ ] Contexto do desafio de escala
- [ ] Abordagem inicial e gargalos encontrados
- [ ] Solucao com multi-agent e compaction
- [ ] Diagrama ASCII da arquitetura escalada
- [ ] Metricas comparativas
- [ ] Licoes aprendidas

## Criterios de Aceitacao
- [ ] Arquivo existe no caminho correto
- [ ] Segue template de case study
- [ ] Minimo 600 linhas

## Dependencias
- Nivel 4 modulos 01-05
ISSUE_EOF
)"

echo "  [OK] B11 — case-study-02.md (Nivel 4)"

# B12 — Case Study 03: KODA Continuous Improvement
gh issue create \
  --repo "$REPO" \
  --title "[Case Study] Criar case-study-03.md — Nivel 4 — KODA Continuous Improvement" \
  --label "curriculum/nivel-4,type/content,priority/medium" \
  --milestone "Nivel 4 — KODA-Especifico" \
  --body "$(cat <<'ISSUE_EOF'
## Arquivo a Criar
`curriculum/04-nivel-4-koda-specific/case-studies/case-study-03.md`

## Descricao
Case study de melhoria continua do KODA ao longo de 6 meses. Cobre ciclos de feedback, evolucao de rubrics e como o harness foi simplificado conforme modelos melhoraram.

## Requisitos
- [ ] Timeline de 6 meses de melhorias
- [ ] Abordagem inicial e metricas
- [ ] Ciclos de feedback e ajustes
- [ ] Diagrama ASCII da evolucao do harness
- [ ] Metricas comparativas por trimestre
- [ ] Licoes aprendidas

## Criterios de Aceitacao
- [ ] Arquivo existe no caminho correto
- [ ] Segue template de case study
- [ ] Minimo 600 linhas

## Dependencias
- 05-harness-improvements.md
ISSUE_EOF
)"

echo "  [OK] B12 — case-study-03.md (Nivel 4)"

echo "  >> Bloco B concluido: 12 issues"
echo ""

# ---------------------------------------------------------------------------
# BLOCK C: Core Concepts (8 issues)
# Milestone: "Core Concepts — 8 Conceitos"
# ---------------------------------------------------------------------------
echo ">>> Bloco C — Core Concepts (8 issues)"

gh issue create --repo "$REPO" \
  --title "[Core Concept] Criar 01-context-management.md — Context Management" \
  --label "curriculum/core-concepts,type/content,priority/medium" \
  --milestone "Core Concepts — 8 Conceitos" \
  --body "$(cat <<'ISSUE_EOF'
## Arquivo a Criar
`curriculum/05-core-concepts/01-context-management.md`

## Conceito
Context Management: como agentes gerenciam informacao por periodos longos sem perder o foco.

## Requisitos
- [ ] Explicacao profunda (3-5 secoes)
- [ ] 3 diagramas Mermaid (conceito, fluxo, aplicacao KODA)
- [ ] Aplicacao pratica no KODA (conversas WhatsApp 2h+)
- [ ] Checklist de implementacao
- [ ] Referencias cruzadas com Nivel 1

## Criterios de Aceitacao
- [ ] Conceito explicado em profundidade
- [ ] Diagramas Mermaid renderizam corretamente
- [ ] Conexao KODA pratica e concreta

## Dependencias
- Nivel 1 concluido
ISSUE_EOF
)" && echo "  [OK] C1 — 01-context-management.md"

gh issue create --repo "$REPO" \
  --title "[Core Concept] Criar 02-planning-execution-separation.md — Planning vs Execution" \
  --label "curriculum/core-concepts,type/content,priority/medium" \
  --milestone "Core Concepts — 8 Conceitos" \
  --body "$(cat <<'ISSUE_EOF'
## Arquivo a Criar
`curriculum/05-core-concepts/02-planning-execution-separation.md`

## Conceito
Planning vs Execution Separation: por que separar planejamento de execucao melhora qualidade e confiabilidade dos agentes.

## Requisitos
- [ ] Explicacao profunda (3-5 secoes)
- [ ] 3 diagramas Mermaid (conceito, fluxo, aplicacao KODA)
- [ ] Aplicacao pratica no KODA (Planner decide, Generator executa)
- [ ] Checklist de implementacao
- [ ] Referencias cruzadas com Nivel 2

## Criterios de Aceitacao
- [ ] Conceito explicado em profundidade
- [ ] Diagramas Mermaid renderizam corretamente
- [ ] Conexao KODA pratica

## Dependencias
- Nivel 2 concluido
ISSUE_EOF
)" && echo "  [OK] C2 — 02-planning-execution-separation.md"

gh issue create --repo "$REPO" \
  --title "[Core Concept] Criar 03-generator-evaluator-pattern.md — Generator/Evaluator" \
  --label "curriculum/core-concepts,type/content,priority/medium" \
  --milestone "Core Concepts — 8 Conceitos" \
  --body "$(cat <<'ISSUE_EOF'
## Arquivo a Criar
`curriculum/05-core-concepts/03-generator-evaluator-pattern.md`

## Conceito
Generator/Evaluator Pattern: separacao entre geracao de output e avaliacao de qualidade para melhor julgamento.

## Requisitos
- [ ] Explicacao profunda (3-5 secoes)
- [ ] 3 diagramas Mermaid (conceito, fluxo, aplicacao KODA)
- [ ] Aplicacao pratica no KODA (recomendacao de produto)
- [ ] Checklist de implementacao
- [ ] Referencias cruzadas com Nivel 2

## Criterios de Aceitacao
- [ ] Conceito explicado em profundidade
- [ ] Diagramas Mermaid renderizam corretamente
- [ ] Conexao KODA pratica

## Dependencias
- Nivel 2 concluido
ISSUE_EOF
)" && echo "  [OK] C3 — 03-generator-evaluator-pattern.md"

gh issue create --repo "$REPO" \
  --title "[Core Concept] Criar 04-sprint-contracts.md — Sprint Contracts" \
  --label "curriculum/core-concepts,type/content,priority/medium" \
  --milestone "Core Concepts — 8 Conceitos" \
  --body "$(cat <<'ISSUE_EOF'
## Arquivo a Criar
`curriculum/05-core-concepts/04-sprint-contracts.md`

## Conceito
Sprint Contracts: como definir contratos claros com criterios testaveis para agentes.

## Requisitos
- [ ] Explicacao profunda (3-5 secoes)
- [ ] 3 diagramas Mermaid (conceito, fluxo, aplicacao KODA)
- [ ] Aplicacao pratica no KODA (contrato de feature)
- [ ] Checklist de implementacao
- [ ] Referencias cruzadas com Nivel 2

## Criterios de Aceitacao
- [ ] Conceito explicado em profundidade
- [ ] Diagramas Mermaid renderizam corretamente
- [ ] Conexao KODA pratica

## Dependencias
- Nivel 2 concluido
ISSUE_EOF
)" && echo "  [OK] C4 — 04-sprint-contracts.md"

gh issue create --repo "$REPO" \
  --title "[Core Concept] Criar 05-state-persistence.md — State Persistence" \
  --label "curriculum/core-concepts,type/content,priority/medium" \
  --milestone "Core Concepts — 8 Conceitos" \
  --body "$(cat <<'ISSUE_EOF'
## Arquivo a Criar
`curriculum/05-core-concepts/05-state-persistence.md`

## Conceito
State Persistence: estrategias para persistir estado entre sessoes e apos falhas.

## Requisitos
- [ ] Explicacao profunda (3-5 secoes)
- [ ] 3 diagramas Mermaid (conceito, fluxo, aplicacao KODA)
- [ ] Aplicacao pratica no KODA (customer state machine)
- [ ] Checklist de implementacao
- [ ] Referencias cruzadas com Nivel 3

## Criterios de Aceitacao
- [ ] Conceito explicado em profundidade
- [ ] Diagramas Mermaid renderizam corretamente
- [ ] Conexao KODA pratica

## Dependencias
- Nivel 3 concluido
ISSUE_EOF
)" && echo "  [OK] C5 — 05-state-persistence.md"

gh issue create --repo "$REPO" \
  --title "[Core Concept] Criar 06-harness-evolution.md — Harness Evolution" \
  --label "curriculum/core-concepts,type/content,priority/medium" \
  --milestone "Core Concepts — 8 Conceitos" \
  --body "$(cat <<'ISSUE_EOF'
## Arquivo a Criar
`curriculum/05-core-concepts/06-harness-evolution.md`

## Conceito
Harness Evolution: como evoluir scaffolding de agentes conforme modelos melhoram.

## Requisitos
- [ ] Explicacao profunda (3-5 secoes)
- [ ] 3 diagramas Mermaid (conceito, fluxo, aplicacao KODA)
- [ ] Aplicacao pratica no KODA (roadmap de evolucao)
- [ ] Checklist de implementacao
- [ ] Referencias cruzadas com Nivel 3

## Criterios de Aceitacao
- [ ] Conceito explicado em profundidade
- [ ] Diagramas Mermaid renderizam corretamente
- [ ] Conexao KODA pratica

## Dependencias
- Nivel 3 concluido
ISSUE_EOF
)" && echo "  [OK] C6 — 06-harness-evolution.md"

gh issue create --repo "$REPO" \
  --title "[Core Concept] Criar 07-multi-agent-coordination.md — Multi-Agent Coordination" \
  --label "curriculum/core-concepts,type/content,priority/medium" \
  --milestone "Core Concepts — 8 Conceitos" \
  --body "$(cat <<'ISSUE_EOF'
## Arquivo a Criar
`curriculum/05-core-concepts/07-multi-agent-coordination.md`

## Conceito
Multi-Agent Coordination: como coordenar 3+ agentes para tarefas complexas.

## Requisitos
- [ ] Explicacao profunda (3-5 secoes)
- [ ] 3 diagramas Mermaid (conceito, fluxo, aplicacao KODA)
- [ ] Aplicacao pratica no KODA (customer journey pipeline)
- [ ] Checklist de implementacao
- [ ] Referencias cruzadas com Nivel 3

## Criterios de Aceitacao
- [ ] Conceito explicado em profundidade
- [ ] Diagramas Mermaid renderizam corretamente
- [ ] Conexao KODA pratica

## Dependencias
- Nivel 3 concluido
ISSUE_EOF
)" && echo "  [OK] C7 — 07-multi-agent-coordination.md"

gh issue create --repo "$REPO" \
  --title "[Core Concept] Criar 08-evaluation-rubrics.md — Evaluation Rubrics" \
  --label "curriculum/core-concepts,type/content,priority/medium" \
  --milestone "Core Concepts — 8 Conceitos" \
  --body "$(cat <<'ISSUE_EOF'
## Arquivo a Criar
`curriculum/05-core-concepts/08-evaluation-rubrics.md`

## Conceito
Evaluation Rubrics: como criar criterios de avaliacao objetivos para outputs de agentes.

## Requisitos
- [ ] Explicacao profunda (3-5 secoes)
- [ ] 3 diagramas Mermaid (conceito, fluxo, aplicacao KODA)
- [ ] Aplicacao pratica no KODA (rubrics de recomendacao)
- [ ] Checklist de implementacao
- [ ] Referencias cruzadas com Nivel 2

## Criterios de Aceitacao
- [ ] Conceito explicado em profundidade
- [ ] Diagramas Mermaid renderizam corretamente
- [ ] Conexao KODA pratica

## Dependencias
- Nivel 2 concluido
ISSUE_EOF
)" && echo "  [OK] C8 — 08-evaluation-rubrics.md"

echo "  >> Bloco C concluido: 8 issues"
echo ""

# ---------------------------------------------------------------------------
# BLOCK D: Knowledge Graphs (11 issues)
# Milestone: "Knowledge Graphs — 35+ Diagramas"
# ---------------------------------------------------------------------------
echo ">>> Bloco D — Knowledge Graphs (11 issues)"

gh issue create --repo "$REPO" \
  --title "[Knowledge Graph] Criar 01-concept-ecosystem.md — Concept Ecosystem" \
  --label "curriculum/knowledge-graphs,type/content,priority/low" \
  --milestone "Knowledge Graphs — 35+ Diagramas" \
  --body "$(cat <<'ISSUE_EOF'
## Arquivo a Criar
`curriculum/06-knowledge-graphs/01-concept-ecosystem.md`

## Diagrama(s) a Incluir
- [ ] Diagrama Mermaid principal: ecossistema completo de conceitos
- [ ] Diagrama de fluxo: como conceitos se relacionam
- [ ] Diagrama de aplicacao KODA: mapeamento features ↔ conceitos

## Criterios de Aceitacao
- [ ] Diagramas Mermaid renderizam corretamente
- [ ] Conexoes entre conceitos visualmente claras
- [ ] Consistente com 00-all-diagrams.txt

## Dependencias
- Core Concepts 01-08
ISSUE_EOF
)" && echo "  [OK] D1 — 01-concept-ecosystem.md"

gh issue create --repo "$REPO" \
  --title "[Knowledge Graph] Criar 02-koda-feature-dependencies.md — KODA Feature Dependencies" \
  --label "curriculum/knowledge-graphs,type/content,priority/low" \
  --milestone "Knowledge Graphs — 35+ Diagramas" \
  --body "$(cat <<'ISSUE_EOF'
## Arquivo a Criar
`curriculum/06-knowledge-graphs/02-koda-feature-dependencies.md`

## Diagrama(s) a Incluir
- [ ] Diagrama Mermaid principal: features KODA e conceitos que as sustentam
- [ ] Diagrama de dependencias entre features
- [ ] Diagrama de risco: features mais impactadas por mudancas de conceito

## Criterios de Aceitacao
- [ ] Diagramas Mermaid renderizam corretamente
- [ ] Conexoes feature↔conceito visualmente claras
- [ ] Consistente com Nivel 4

## Dependencias
- Nivel 4 modulos principais
ISSUE_EOF
)" && echo "  [OK] D2 — 02-koda-feature-dependencies.md"

gh issue create --repo "$REPO" \
  --title "[Knowledge Graph] Criar 03-learning-progression.md — Learning Progression" \
  --label "curriculum/knowledge-graphs,type/content,priority/low" \
  --milestone "Knowledge Graphs — 35+ Diagramas" \
  --body "$(cat <<'ISSUE_EOF'
## Arquivo a Criar
`curriculum/06-knowledge-graphs/03-learning-progression.md`

## Diagrama(s) a Incluir
- [ ] Diagrama Mermaid principal: progressao de aprendizado Nivel 1→4
- [ ] Diagrama de pre-requisitos por topico
- [ ] Diagrama de caminhos alternativos (fast-track, standard, deep-dive)

## Criterios de Aceitacao
- [ ] Diagramas Mermaid renderizam corretamente
- [ ] Ordem de aprendizado visualmente clara
- [ ] Consistente com MASTER_PLAN.md

## Dependencias
- MASTER_PLAN.md
ISSUE_EOF
)" && echo "  [OK] D3 — 03-learning-progression.md"

gh issue create --repo "$REPO" \
  --title "[Knowledge Graph] Criar 04-problem-solution-mapping.md — Problem-Solution Mapping" \
  --label "curriculum/knowledge-graphs,type/content,priority/low" \
  --milestone "Knowledge Graphs — 35+ Diagramas" \
  --body "$(cat <<'ISSUE_EOF'
## Arquivo a Criar
`curriculum/06-knowledge-graphs/04-problem-solution-mapping.md`

## Diagrama(s) a Incluir
- [ ] Diagrama Mermaid principal: problemas comuns → solucoes (padroes)
- [ ] Diagrama de severidade: impacto de cada problema
- [ ] Diagrama de aplicacao: problemas KODA especificos e solucoes

## Criterios de Aceitacao
- [ ] Diagramas Mermaid renderizam corretamente
- [ ] Mapeamento problema→solucao visualmente claro
- [ ] Consistente com case studies

## Dependencias
- Case studies, Niveis 1-4
ISSUE_EOF
)" && echo "  [OK] D4 — 04-problem-solution-mapping.md"

# D5-D11: Detailed Graphs para cada Core Concept
gh issue create --repo "$REPO" \
  --title "[Knowledge Graph] Criar context-management-graphs.md — Detailed Graph: Context Management" \
  --label "curriculum/knowledge-graphs,type/content,priority/low" \
  --milestone "Knowledge Graphs — 35+ Diagramas" \
  --body "$(cat <<'ISSUE_EOF'
## Arquivo a Criar
`curriculum/06-knowledge-graphs/detailed-graphs/context-management-graphs.md`

## Diagrama(s) a Incluir
- [ ] Diagrama Mermaid: arquitetura de context management
- [ ] Diagrama Mermaid: fluxo de compactacao e windowing
- [ ] Diagrama Mermaid: aplicacao KODA (conversa 2h+)

## Criterios de Aceitacao
- [ ] Diagramas Mermaid renderizam corretamente
- [ ] Conexoes com 05-core-concepts/01-context-management.md
- [ ] Consistente com 00-all-diagrams.txt

## Dependencias
- 05-core-concepts/01-context-management.md
ISSUE_EOF
)" && echo "  [OK] D5 — context-management-graphs.md"

gh issue create --repo "$REPO" \
  --title "[Knowledge Graph] Criar planning-execution-graphs.md — Detailed Graph: Planning vs Execution" \
  --label "curriculum/knowledge-graphs,type/content,priority/low" \
  --milestone "Knowledge Graphs — 35+ Diagramas" \
  --body "$(cat <<'ISSUE_EOF'
## Arquivo a Criar
`curriculum/06-knowledge-graphs/detailed-graphs/planning-execution-graphs.md`

## Diagrama(s) a Incluir
- [ ] Diagrama Mermaid: separacao Planner/Executor
- [ ] Diagrama Mermaid: fluxo de decisao e delegacao
- [ ] Diagrama Mermaid: aplicacao KODA (feature planning)

## Criterios de Aceitacao
- [ ] Diagramas Mermaid renderizam corretamente
- [ ] Conexoes com 05-core-concepts/02-planning-execution-separation.md

## Dependencias
- 05-core-concepts/02-planning-execution-separation.md
ISSUE_EOF
)" && echo "  [OK] D6 — planning-execution-graphs.md"

gh issue create --repo "$REPO" \
  --title "[Knowledge Graph] Criar generator-evaluator-graphs.md — Detailed Graph: Generator/Evaluator" \
  --label "curriculum/knowledge-graphs,type/content,priority/low" \
  --milestone "Knowledge Graphs — 35+ Diagramas" \
  --body "$(cat <<'ISSUE_EOF'
## Arquivo a Criar
`curriculum/06-knowledge-graphs/detailed-graphs/generator-evaluator-graphs.md`

## Diagrama(s) a Incluir
- [ ] Diagrama Mermaid: arquitetura Generator/Evaluator
- [ ] Diagrama Mermaid: fluxo de geracao e avaliacao
- [ ] Diagrama Mermaid: aplicacao KODA (recomendacao de produto)

## Criterios de Aceitacao
- [ ] Diagramas Mermaid renderizam corretamente
- [ ] Conexoes com 05-core-concepts/03-generator-evaluator-pattern.md

## Dependencias
- 05-core-concepts/03-generator-evaluator-pattern.md
ISSUE_EOF
)" && echo "  [OK] D7 — generator-evaluator-graphs.md"

gh issue create --repo "$REPO" \
  --title "[Knowledge Graph] Criar sprint-contracts-graphs.md — Detailed Graph: Sprint Contracts" \
  --label "curriculum/knowledge-graphs,type/content,priority/low" \
  --milestone "Knowledge Graphs — 35+ Diagramas" \
  --body "$(cat <<'ISSUE_EOF'
## Arquivo a Criar
`curriculum/06-knowledge-graphs/detailed-graphs/sprint-contracts-graphs.md`

## Diagrama(s) a Incluir
- [ ] Diagrama Mermaid: estrutura de sprint contract
- [ ] Diagrama Mermaid: fluxo de validacao de contrato
- [ ] Diagrama Mermaid: aplicacao KODA (feature contract)

## Criterios de Aceitacao
- [ ] Diagramas Mermaid renderizam corretamente
- [ ] Conexoes com 05-core-concepts/04-sprint-contracts.md

## Dependencias
- 05-core-concepts/04-sprint-contracts.md
ISSUE_EOF
)" && echo "  [OK] D8 — sprint-contracts-graphs.md"

gh issue create --repo "$REPO" \
  --title "[Knowledge Graph] Criar state-persistence-graphs.md — Detailed Graph: State Persistence" \
  --label "curriculum/knowledge-graphs,type/content,priority/low" \
  --milestone "Knowledge Graphs — 35+ Diagramas" \
  --body "$(cat <<'ISSUE_EOF'
## Arquivo a Criar
`curriculum/06-knowledge-graphs/detailed-graphs/state-persistence-graphs.md`

## Diagrama(s) a Incluir
- [ ] Diagrama Mermaid: arquitetura de persistencia
- [ ] Diagrama Mermaid: fluxo de checkpoint e recovery
- [ ] Diagrama Mermaid: aplicacao KODA (customer state)

## Criterios de Aceitacao
- [ ] Diagramas Mermaid renderizam corretamente
- [ ] Conexoes com 05-core-concepts/05-state-persistence.md

## Dependencias
- 05-core-concepts/05-state-persistence.md
ISSUE_EOF
)" && echo "  [OK] D9 — state-persistence-graphs.md"

gh issue create --repo "$REPO" \
  --title "[Knowledge Graph] Criar harness-evolution-graphs.md — Detailed Graph: Harness Evolution" \
  --label "curriculum/knowledge-graphs,type/content,priority/low" \
  --milestone "Knowledge Graphs — 35+ Diagramas" \
  --body "$(cat <<'ISSUE_EOF'
## Arquivo a Criar
`curriculum/06-knowledge-graphs/detailed-graphs/harness-evolution-graphs.md`

## Diagrama(s) a Incluir
- [ ] Diagrama Mermaid: ciclo de vida do harness
- [ ] Diagrama Mermaid: timeline de evolucao
- [ ] Diagrama Mermaid: aplicacao KODA (roadmap)

## Criterios de Aceitacao
- [ ] Diagramas Mermaid renderizam corretamente
- [ ] Conexoes com 05-core-concepts/06-harness-evolution.md

## Dependencias
- 05-core-concepts/06-harness-evolution.md
ISSUE_EOF
)" && echo "  [OK] D10 — harness-evolution-graphs.md"

gh issue create --repo "$REPO" \
  --title "[Knowledge Graph] Criar multi-agent-coordination-graphs.md — Detailed Graph: Multi-Agent" \
  --label "curriculum/knowledge-graphs,type/content,priority/low" \
  --milestone "Knowledge Graphs — 35+ Diagramas" \
  --body "$(cat <<'ISSUE_EOF'
## Arquivo a Criar
`curriculum/06-knowledge-graphs/detailed-graphs/multi-agent-coordination-graphs.md`

## Diagrama(s) a Incluir
- [ ] Diagrama Mermaid: arquitetura multi-agent
- [ ] Diagrama Mermaid: fluxo de coordenacao
- [ ] Diagrama Mermaid: aplicacao KODA (customer journey pipeline)

## Criterios de Aceitacao
- [ ] Diagramas Mermaid renderizam corretamente
- [ ] Conexoes com 05-core-concepts/07-multi-agent-coordination.md

## Dependencias
- 05-core-concepts/07-multi-agent-coordination.md
ISSUE_EOF
)" && echo "  [OK] D11 — multi-agent-coordination-graphs.md"

gh issue create --repo "$REPO" \
  --title "[Knowledge Graph] Criar evaluation-rubrics-graphs.md — Detailed Graph: Evaluation Rubrics" \
  --label "curriculum/knowledge-graphs,type/content,priority/low" \
  --milestone "Knowledge Graphs — 35+ Diagramas" \
  --body "$(cat <<'ISSUE_EOF'
## Arquivo a Criar
`curriculum/06-knowledge-graphs/detailed-graphs/evaluation-rubrics-graphs.md`

## Diagrama(s) a Incluir
- [ ] Diagrama Mermaid: estrutura de rubric
- [ ] Diagrama Mermaid: fluxo de avaliacao
- [ ] Diagrama Mermaid: aplicacao KODA (rubrics de qualidade)

## Criterios de Aceitacao
- [ ] Diagramas Mermaid renderizam corretamente
- [ ] Conexoes com 05-core-concepts/08-evaluation-rubrics.md

## Dependencias
- 05-core-concepts/08-evaluation-rubrics.md
ISSUE_EOF
)" && echo "  [OK] D12 — evaluation-rubrics-graphs.md"

echo "  >> Bloco D concluido: 12 issues"
echo ""

# ---------------------------------------------------------------------------
# BLOCK E: Implementation Guides (6 issues)
# Milestone: "Implementation Guides"
# ---------------------------------------------------------------------------
echo ">>> Bloco E — Implementation Guides (6 issues)"

gh issue create --repo "$REPO" \
  --title "[Guia] Criar 01-setup-guide.md — Setup Guide" \
  --label "curriculum/guides,type/content,priority/medium" \
  --milestone "Implementation Guides" \
  --body "$(cat <<'ISSUE_EOF'
## Arquivo a Criar
`curriculum/07-implementation-guides/01-setup-guide.md`

## Descricao
Guia completo de setup para lideres: como estruturar o repositorio, configurar ferramentas, preparar ambiente de desenvolvimento para long-running agents.

## Requisitos
- [ ] Estrutura de repositorio recomendada
- [ ] Dependencias e requisitos de sistema
- [ ] Configuracao de ambiente (Python, APIs, ferramentas)
- [ ] Primeiro agente funcional (hello world)
- [ ] Checklist de verificacao de setup

## Criterios de Aceitacao
- [ ] Guia auto-contido (leitor consegue seguir sem ajuda externa)
- [ ] Exemplos de codigo funcionais
- [ ] Portugues brasileiro

## Dependencias
- Nenhuma (independente)
ISSUE_EOF
)" && echo "  [OK] E1 — 01-setup-guide.md"

gh issue create --repo "$REPO" \
  --title "[Guia] Criar 02-team-progression-guide.md — Team Progression Guide" \
  --label "curriculum/guides,type/content,priority/medium" \
  --milestone "Implementation Guides" \
  --body "$(cat <<'ISSUE_EOF'
## Arquivo a Criar
`curriculum/07-implementation-guides/02-team-progression-guide.md`

## Descricao
Guia para lideres sobre como escalar o aprendizado da equipe: roadmap, checkpoints, metricas de progresso e estrategias de mentoring.

## Requisitos
- [ ] Roadmap de progressao por nivel
- [ ] Checkpoints e criterios de avanco
- [ ] Metricas de progresso da equipe
- [ ] Estrategias de mentoring e pair programming
- [ ] Templates de avaliacao

## Criterios de Aceitacao
- [ ] Guia completo e acionavel para lideres
- [ ] Metricas claras e mensuraveis
- [ ] Portugues brasileiro

## Dependencias
- EXECUTION_PLAN.md
ISSUE_EOF
)" && echo "  [OK] E2 — 02-team-progression-guide.md"

gh issue create --repo "$REPO" \
  --title "[Guia] Criar 03-harness-design-checklist.md — Harness Design Checklist" \
  --label "curriculum/guides,type/content,priority/medium" \
  --milestone "Implementation Guides" \
  --body "$(cat <<'ISSUE_EOF'
## Arquivo a Criar
`curriculum/07-implementation-guides/03-harness-design-checklist.md`

## Descricao
Checklist abrangente para avaliar a qualidade de um harness de agente. Cobre todos os aspectos: contexto, contratos, avaliacao, persistencia e evolucao.

## Requisitos
- [ ] Checklist por categoria (contexto, contratos, avaliacao, etc)
- [ ] Criterios de PASS/FAIL por item
- [ ] Exemplos de harness bom vs ruim
- [ ] Scorecard de maturidade do harness
- [ ] Vinculos com modulos do curriculo

## Criterios de Aceitacao
- [ ] Checklist completo e acionavel
- [ ] Criterios objetivos (nao subjetivos)
- [ ] Portugues brasileiro

## Dependencias
- Niveis 1-3
ISSUE_EOF
)" && echo "  [OK] E3 — 03-harness-design-checklist.md"

gh issue create --repo "$REPO" \
  --title "[Guia] Criar 04-evaluation-rubric-template.md — Evaluation Rubric Template" \
  --label "curriculum/guides,type/template,priority/medium" \
  --milestone "Implementation Guides" \
  --body "$(cat <<'ISSUE_EOF'
## Arquivo a Criar
`curriculum/07-implementation-guides/04-evaluation-rubric-template.md`

## Descricao
Template e guia para criar rubrics de avaliacao de qualidade para outputs de agentes. Inclui exemplos preenchidos para diferentes tipos de output.

## Requisitos
- [ ] Template de rubric (dimensoes, criterios, scores)
- [ ] Guia de como adaptar para diferentes dominios
- [ ] 3 exemplos preenchidos (recomendacao, texto, codigo)
- [ ] Checklist de validacao de rubric

## Criterios de Aceitacao
- [ ] Template reutilizavel e adaptavel
- [ ] Exemplos claros e didaticos
- [ ] Portugues brasileiro

## Dependencias
- 02-nivel-2-practical-patterns/03-rubric-design.md
ISSUE_EOF
)" && echo "  [OK] E4 — 04-evaluation-rubric-template.md"

gh issue create --repo "$REPO" \
  --title "[Guia] Criar 05-trace-analysis-guide.md — Trace Analysis Guide" \
  --label "curriculum/guides,type/content,priority/medium" \
  --milestone "Implementation Guides" \
  --body "$(cat <<'ISSUE_EOF'
## Arquivo a Criar
`curriculum/07-implementation-guides/05-trace-analysis-guide.md`

## Descricao
Guia completo de como ler, interpretar e diagnosticar problemas em agent traces. Cobre padrões comuns de falha e como identifica-los.

## Requisitos
- [ ] Anatomia de um agent trace
- [ ] Padroes comuns de falha (loop, perda de contexto, ma qualidade)
- [ ] Tecnicas de diagnostico
- [ ] Exemplos de traces reais comentados
- [ ] Checklist de troubleshooting

## Criterios de Aceitacao
- [ ] Guia pratico e acionavel
- [ ] Exemplos reais de traces
- [ ] Portugues brasileiro

## Dependencias
- 02-nivel-2-practical-patterns/04-trace-reading.md
ISSUE_EOF
)" && echo "  [OK] E5 — 05-trace-analysis-guide.md"

gh issue create --repo "$REPO" \
  --title "[Guia] Criar 06-harness-evolution-playbook.md — Harness Evolution Playbook" \
  --label "curriculum/guides,type/content,priority/medium" \
  --milestone "Implementation Guides" \
  --body "$(cat <<'ISSUE_EOF'
## Arquivo a Criar
`curriculum/07-implementation-guides/06-harness-evolution-playbook.md`

## Descricao
Playbook passo-a-passo para evoluir um harness de agente. Cobre diagnostico, planejamento, execucao e validacao de cada fase de evolucao.

## Requisitos
- [ ] Fase 1: Diagnostico (o que remover/melhorar)
- [ ] Fase 2: Planejamento (roadmap, riscos)
- [ ] Fase 3: Execucao (passo-a-passo)
- [ ] Fase 4: Validacao (metricas, rollback)
- [ ] Templates de documentacao por fase

## Criterios de Aceitacao
- [ ] Playbook completo e sequencial
- [ ] Decisoes justificadas com dados
- [ ] Portugues brasileiro

## Dependencias
- 03-nivel-3-advanced-architecture/05-harness-evolution.md
ISSUE_EOF
)" && echo "  [OK] E6 — 06-harness-evolution-playbook.md"

echo "  >> Bloco E concluido: 6 issues"
echo ""

# ---------------------------------------------------------------------------
# BLOCK F: Tools & Templates (6 issues)
# Milestone: "Tools & Templates"
# ---------------------------------------------------------------------------
echo ">>> Bloco F — Tools & Templates (6 issues)"

gh issue create --repo "$REPO" \
  --title "[Template] Criar team-progress-tracker.md — Team Progress Tracker" \
  --label "curriculum/templates,type/template,priority/medium" \
  --milestone "Tools & Templates" \
  --body "$(cat <<'ISSUE_EOF'
## Arquivo a Criar
`curriculum/08-tools-templates/team-progress-tracker.md`

## Descricao
Template interativo para rastrear progresso individual e da equipe no curriculo. Inclui tabelas, graficos de progresso e checklists.

## Requisitos
- [ ] Tabela de progresso por membro
- [ ] Indicadores visuais de status (Nivel, Exercicios, Case Studies)
- [ ] Secao de metricas da equipe
- [ ] Instrucoes de uso

## Criterios de Aceitacao
- [ ] Template funcional e auto-explicativo
- [ ] Facil de adaptar para qualquer tamanho de equipe
- [ ] Portugues brasileiro

## Dependencias
- Nenhuma (independente)
ISSUE_EOF
)" && echo "  [OK] F1 — team-progress-tracker.md"

gh issue create --repo "$REPO" \
  --title "[Template] Criar learning-assessment-rubric.md — Learning Assessment Rubric" \
  --label "curriculum/templates,type/template,priority/medium" \
  --milestone "Tools & Templates" \
  --body "$(cat <<'ISSUE_EOF'
## Arquivo a Criar
`curriculum/08-tools-templates/learning-assessment-rubric.md`

## Descricao
Rubric para avaliar compreensao de conceitos do curriculo. Cobre todos os 8 core concepts com criterios por nivel de profundidade.

## Requisitos
- [ ] Criterios de avaliacao por conceito
- [ ] Niveis de compreensao (basico, intermediario, avancado, expert)
- [ ] Checklist de auto-avaliacao
- [ ] Guia para mentores aplicarem a rubric

## Criterios de Aceitacao
- [ ] Rubric completa para todos os 8 conceitos
- [ ] Criterios objetivos e verificaveis
- [ ] Portugues brasileiro

## Dependencias
- 05-core-concepts/
ISSUE_EOF
)" && echo "  [OK] F2 — learning-assessment-rubric.md"

gh issue create --repo "$REPO" \
  --title "[Template] Criar knowledge-graph-template.md — Knowledge Graph Template" \
  --label "curriculum/templates,type/template,priority/low" \
  --milestone "Tools & Templates" \
  --body "$(cat <<'ISSUE_EOF'
## Arquivo a Criar
`curriculum/08-tools-templates/knowledge-graph-template.md`

## Descricao
Template para criar novos Knowledge Graphs no padrao Mermaid. Inclui estrutura de 3 diagramas por conceito e guia de estilo.

## Requisitos
- [ ] Template de 3 diagramas Mermaid
- [ ] Guia de estilo visual (cores, formas, conectores)
- [ ] Exemplo preenchido
- [ ] Checklist de qualidade do diagrama

## Criterios de Aceitacao
- [ ] Template facil de usar e adaptar
- [ ] Diagramas exemplo renderizam corretamente
- [ ] Portugues brasileiro

## Dependencias
- 06-knowledge-graphs/
ISSUE_EOF
)" && echo "  [OK] F3 — knowledge-graph-template.md"

gh issue create --repo "$REPO" \
  --title "[Template] Criar sprint-contract-template.md — Sprint Contract Template" \
  --label "curriculum/templates,type/template,priority/medium" \
  --milestone "Tools & Templates" \
  --body "$(cat <<'ISSUE_EOF'
## Arquivo a Criar
`curriculum/08-tools-templates/sprint-contract-template.md`

## Descricao
Template para definir contratos entre generator e evaluator. Inclui secoes de objetivo, criterios de aceitacao, restricoes e metricas.

## Requisitos
- [ ] Estrutura de contrato (objetivo, criterios, restricoes)
- [ ] Exemplo preenchido para feature KODA
- [ ] Checklist de validacao de contrato
- [ ] Guia de negociacao de contrato

## Criterios de Aceitacao
- [ ] Template pronto para uso em features reais
- [ ] Exemplo concreto e didatico
- [ ] Portugues brasileiro

## Dependencias
- 02-nivel-2-practical-patterns/02-sprint-contracts.md
ISSUE_EOF
)" && echo "  [OK] F4 — sprint-contract-template.md"

gh issue create --repo "$REPO" \
  --title "[Template] Criar evaluation-rubric-template.md — Evaluation Rubric Template" \
  --label "curriculum/templates,type/template,priority/medium" \
  --milestone "Tools & Templates" \
  --body "$(cat <<'ISSUE_EOF'
## Arquivo a Criar
`curriculum/08-tools-templates/evaluation-rubric-template.md`

## Descricao
Template generico para criar rubrics de avaliacao. Inclui dimensoes, criterios, escala de pontuacao e exemplos para diferentes dominios.

## Requisitos
- [ ] Estrutura de rubric (dimensoes, criterios, scores)
- [ ] 2 exemplos preenchidos (output textual, output estruturado)
- [ ] Guia de calibracao de rubric
- [ ] Checklist de qualidade da rubric

## Criterios de Aceitacao
- [ ] Template adaptavel a qualquer dominio
- [ ] Exemplos claros e didaticos
- [ ] Portugues brasileiro

## Dependencias
- 02-nivel-2-practical-patterns/03-rubric-design.md
ISSUE_EOF
)" && echo "  [OK] F5 — evaluation-rubric-template.md"

gh issue create --repo "$REPO" \
  --title "[Template] Criar architecture-decision-record-template.md — ADR Template" \
  --label "curriculum/templates,type/template,priority/low" \
  --milestone "Tools & Templates" \
  --body "$(cat <<'ISSUE_EOF'
## Arquivo a Criar
`curriculum/08-tools-templates/architecture-decision-record-template.md`

## Descricao
Template de Architecture Decision Record (ADR) para documentar decisoes arquiteturais em projetos de long-running agents.

## Requisitos
- [ ] Estrutura ADR (titulo, status, contexto, decisao, consequencias)
- [ ] Exemplo preenchido (decisao real do KODA)
- [ ] Guia de quando criar um ADR
- [ ] Checklist de completude

## Criterios de Aceitacao
- [ ] Template segue formato ADR padrao
- [ ] Exemplo concreto e relevante
- [ ] Portugues brasileiro

## Dependencias
- Nenhuma (independente)
ISSUE_EOF
)" && echo "  [OK] F6 — architecture-decision-record-template.md"

echo "  >> Bloco F concluido: 6 issues"
echo ""

# ---------------------------------------------------------------------------
# BLOCK G: References (3 issues)
# Milestone: "References & Lacunas"
# ---------------------------------------------------------------------------
echo ">>> Bloco G — References (3 issues)"

gh issue create --repo "$REPO" \
  --title "[Referencia] Criar anthropic-presentation-summary.md — Anthropic Presentation Summary" \
  --label "curriculum/references,type/content,priority/low" \
  --milestone "References & Lacunas" \
  --body "$(cat <<'ISSUE_EOF'
## Arquivo a Criar
`curriculum/10-references/anthropic-presentation-summary.md`

## Descricao
Resumo da apresentacao da Anthropic sobre long-running agents. Cobre os principais pontos, padroes apresentados e insights tecnicos.

## Requisitos
- [ ] Resumo estruturado da apresentacao
- [ ] Principais padroes e insights
- [ ] Conexoes com o curriculo (links para modulos relevantes)
- [ ] Notas e observacoes pessoais

## Criterios de Aceitacao
- [ ] Resumo claro e conciso
- [ ] Links funcionais para modulos do curriculo
- [ ] Portugues brasileiro

## Dependencias
- Nenhuma (independente)
ISSUE_EOF
)" && echo "  [OK] G1 — anthropic-presentation-summary.md"

gh issue create --repo "$REPO" \
  --title "[Referencia] Criar model-capability-timeline.md — Model Capability Timeline" \
  --label "curriculum/references,type/content,priority/low" \
  --milestone "References & Lacunas" \
  --body "$(cat <<'ISSUE_EOF'
## Arquivo a Criar
`curriculum/10-references/model-capability-timeline.md`

## Descricao
Timeline da evolucao das capacidades dos modelos de LLM e como cada avanco impacta o design de long-running agents.

## Requisitos
- [ ] Timeline visual (tabela ou ASCII art)
- [ ] Marcos principais (context windows, reasoning, tool use)
- [ ] Impacto de cada marco no design de agentes
- [ ] Projecoes futuras

## Criterios de Aceitacao
- [ ] Timeline clara e informativa
- [ ] Conexoes com evolucao do harness
- [ ] Portugues brasileiro

## Dependencias
- Nenhuma (independente)
ISSUE_EOF
)" && echo "  [OK] G2 — model-capability-timeline.md"

gh issue create --repo "$REPO" \
  --title "[Referencia] Criar additional-resources.md — Additional Resources" \
  --label "curriculum/references,type/content,priority/low" \
  --milestone "References & Lacunas" \
  --body "$(cat <<'ISSUE_EOF'
## Arquivo a Criar
`curriculum/10-references/additional-resources.md`

## Descricao
Lista curada de recursos adicionais: papers, blog posts, videos, repositorios e ferramentas relacionadas a long-running agents.

## Requisitos
- [ ] Papers academicos relevantes
- [ ] Blog posts e artigos tecnicos
- [ ] Videos e palestras
- [ ] Repositorios open-source de referencia
- [ ] Ferramentas e bibliotecas uteis

## Criterios de Aceitacao
- [ ] Lista organizada por categoria
- [ ] Links funcionais
- [ ] Breve descricao de cada recurso
- [ ] Portugues brasileiro

## Dependencias
- Nenhuma (independente)
ISSUE_EOF
)" && echo "  [OK] G3 — additional-resources.md"

echo "  >> Bloco G concluido: 3 issues"
echo ""

# ---------------------------------------------------------------------------
# BLOCK H: Gaps / Lacunas (7 issues)
# Milestone: "References & Lacunas"
# ---------------------------------------------------------------------------
echo ">>> Bloco H — Lacunas / Gaps (7 issues)"

# H1 — FAQ.md
gh issue create --repo "$REPO" \
  --title "[Gap] Criar FAQ.md — Perguntas Frequentes" \
  --label "curriculum/gap,type/content,priority/medium" \
  --milestone "References & Lacunas" \
  --body "$(cat <<'ISSUE_EOF'
## Arquivo a Criar
`curriculum/FAQ.md`

## Descricao
Documento de perguntas frequentes sobre o curriculo. Cobre duvidas comuns de participantes, lideres e mentores.

## Requisitos
- [ ] Secao para participantes (duvidas sobre o curriculo)
- [ ] Secao para lideres (duvidas sobre implementacao)
- [ ] Secao para mentores (duvidas sobre avaliacao)
- [ ] Secao tecnica (duvidas sobre conceitos)
- [ ] Minimo 15 perguntas respondidas

## Criterios de Aceitacao
- [ ] Perguntas baseadas em duvidas reais
- [ ] Respostas claras e diretas
- [ ] Links para modulos relevantes
- [ ] Portugues brasileiro

## Dependencias
- Nenhuma (pode ser criado a qualquer momento)
ISSUE_EOF
)" && echo "  [OK] H1 — FAQ.md"

# H2 — Exercise 02 Nivel 2 (missing)
gh issue create --repo "$REPO" \
  --title "[Gap] Criar exercise-02.md — Nivel 2 — Sprint Contracts Exercise" \
  --label "curriculum/gap,curriculum/exercises,type/exercise,priority/high" \
  --milestone "References & Lacunas" \
  --body "$(cat <<'ISSUE_EOF'
## Arquivo a Criar
`curriculum/02-nivel-2-practical-patterns/exercises/exercise-02.md`

## Topico do Exercicio
Criar sprint contracts para uma feature do KODA e validar com generator/evaluator.

## Requisitos
- [ ] Cenario realista com feature KODA a ser contratada
- [ ] Lista de requisitos funcionais e tecnicos
- [ ] Codigo Python do contrato e validacao (minimo 200 linhas)
- [ ] Secao de validacao com criterios de aceitacao
- [ ] Dificuldade: 3 estrelas

## Criterios de Aceitacao
- [ ] Aluno consegue implementar em 60-90 minutos
- [ ] Exercicio completa a trilogia de exercicios do Nivel 2 (01, 02, 03)
- [ ] Solucao incluida em `exercises/solutions/`

## Dependencias
- 02-nivel-2-practical-patterns/02-sprint-contracts.md
ISSUE_EOF
)" && echo "  [OK] H2 — exercise-02.md (Nivel 2)"

# H3 — Solucao Exercise 01 Nivel 1
gh issue create --repo "$REPO" \
  --title "[Gap] Criar solution-exercise-01.md — Nivel 1 — Windowing" \
  --label "curriculum/gap,curriculum/exercises,type/exercise,priority/low" \
  --milestone "References & Lacunas" \
  --body "$(cat <<'ISSUE_EOF'
## Arquivo a Criar
`curriculum/01-nivel-1-fundamentals/exercises/solutions/exercise-01-solution.md`

## Descricao
Solucao do exercicio de windowing do Nivel 1. Implementacao de sliding window para gerenciamento de contexto.

## Requisitos
- [ ] Codigo Python funcional
- [ ] Explicacao da estrategia de windowing
- [ ] Testes de retencao de contexto

## Dependencias
- 01-nivel-1-fundamentals/exercises/exercise-01-windowing.md
ISSUE_EOF
)" && echo "  [OK] H3 — solution-exercise-01.md (Nivel 1)"

# H4 — Solucao Exercise 02 Nivel 1
gh issue create --repo "$REPO" \
  --title "[Gap] Criar solution-exercise-02.md — Nivel 1 — Structured Output" \
  --label "curriculum/gap,curriculum/exercises,type/exercise,priority/low" \
  --milestone "References & Lacunas" \
  --body "$(cat <<'ISSUE_EOF'
## Arquivo a Criar
`curriculum/01-nivel-1-fundamentals/exercises/solutions/exercise-02-solution.md`

## Descricao
Solucao do exercicio de structured output do Nivel 1. Implementacao de formatos estruturados (JSON, XML) para outputs de agente.

## Requisitos
- [ ] Codigo Python funcional
- [ ] Explicacao dos formatos e quando usar cada um
- [ ] Testes de parsing e validacao

## Dependencias
- 01-nivel-1-fundamentals/exercises/exercise-02-structured-output.md
ISSUE_EOF
)" && echo "  [OK] H4 — solution-exercise-02.md (Nivel 1)"

# H5 — Solucao Exercise 01 Nivel 2
gh issue create --repo "$REPO" \
  --title "[Gap] Criar solution-exercise-01.md — Nivel 2 — Generator/Evaluator" \
  --label "curriculum/gap,curriculum/exercises,type/exercise,priority/low" \
  --milestone "References & Lacunas" \
  --body "$(cat <<'ISSUE_EOF'
## Arquivo a Criar
`curriculum/02-nivel-2-practical-patterns/exercises/solutions/exercise-01-solution.md`

## Descricao
Solucao do exercicio de Generator/Evaluator do Nivel 2. Implementacao completa do padrao para uma feature simples.

## Requisitos
- [ ] Codigo Python do generator
- [ ] Codigo Python do evaluator
- [ ] Integracao generator↔evaluator
- [ ] Testes de qualidade

## Dependencias
- 02-nivel-2-practical-patterns/exercises/exercise-01.md
ISSUE_EOF
)" && echo "  [OK] H5 — solution-exercise-01.md (Nivel 2)"

# H6 — Solucao Exercise 02 Nivel 2
gh issue create --repo "$REPO" \
  --title "[Gap] Criar solution-exercise-02.md — Nivel 2 — Sprint Contracts" \
  --label "curriculum/gap,curriculum/exercises,type/exercise,priority/low" \
  --milestone "References & Lacunas" \
  --body "$(cat <<'ISSUE_EOF'
## Arquivo a Criar
`curriculum/02-nivel-2-practical-patterns/exercises/solutions/exercise-02-solution.md`

## Descricao
Solucao do exercicio de Sprint Contracts do Nivel 2. Contratos preenchidos e validados.

## Requisitos
- [ ] Contratos preenchidos para a feature
- [ ] Codigo de validacao de contrato
- [ ] Testes de conformidade

## Dependencias
- 02-nivel-2-practical-patterns/exercises/exercise-02.md (a ser criado)
ISSUE_EOF
)" && echo "  [OK] H6 — solution-exercise-02.md (Nivel 2)"

# H7 — Solucao Exercise 03 Nivel 2
gh issue create --repo "$REPO" \
  --title "[Gap] Criar solution-exercise-03.md — Nivel 2 — Rubric Design" \
  --label "curriculum/gap,curriculum/exercises,type/exercise,priority/low" \
  --milestone "References & Lacunas" \
  --body "$(cat <<'ISSUE_EOF'
## Arquivo a Criar
`curriculum/02-nivel-2-practical-patterns/exercises/solutions/exercise-03-solution.md`

## Descricao
Solucao do exercicio de Rubric Design do Nivel 2. Rubrics completas para avaliacao de outputs.

## Requisitos
- [ ] Rubrics preenchidas para diferentes tipos de output
- [ ] Explicacao dos criterios e pesos
- [ ] Exemplos de aplicacao das rubrics

## Dependencias
- 02-nivel-2-practical-patterns/exercises/exercise-03.md
ISSUE_EOF
)" && echo "  [OK] H7 — solution-exercise-03.md (Nivel 2)"

echo "  >> Bloco H concluido: 7 issues"
echo ""

# ---------------------------------------------------------------------------
# Resumo Final
# ---------------------------------------------------------------------------
echo "============================================"
echo " CRIACAO CONCLUIDA!"
echo "============================================"
echo ""
echo "Resumo por bloco:"
echo "  Bloco A (Nivel 3):            12 issues"
echo "  Bloco B (Nivel 4):            12 issues"
echo "  Bloco C (Core Concepts):       8 issues"
echo "  Bloco D (Knowledge Graphs):   12 issues"
echo "  Bloco E (Implementation Guides): 6 issues"
echo "  Bloco F (Tools & Templates):   6 issues"
echo "  Bloco G (References):          3 issues"
echo "  Bloco H (Lacunas/Gaps):        7 issues"
echo "  -------------------------------------------"
echo "  TOTAL:                        66 issues"
echo ""
echo "Verifique em: https://github.com/pavani06/long-running-agents/issues"
echo ""
