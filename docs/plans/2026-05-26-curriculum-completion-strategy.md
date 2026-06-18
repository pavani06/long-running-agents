---
title: "Estratégia de Execução para Completar o Currículo Long-Running Agents"
type: plan
date: 2026-05-26
tags:
  - curriculo-conteudo
  - governanca
  - stack-tooling
aliases:
  - estratégia conclusão
  - completion strategy
  - GitHub Issues
relates-to:
  - "[[curriculum/MASTER_PLAN|Curriculum Master Plan]]"
  - "[[curriculum/INDEX|Curriculum Index]]"
  - "[[docs/system-of-record|System of Record]]"
  - "[[AGENTS|AGENTS.md]]"
---

# Prompt: Estrategia de Execucao para Completar o Curriculo Long-Running Agents

**Objetivo:** Produzir um plano de execucao utilizando GitHub Issues, Milestones e Projects para completar os ~65 arquivos restantes do curriculo `curriculum/`, organizado por dependencias e prioridades.

---

## Instrucoes para o Agente

Voce deve gerar uma estrategia completa com os seguintes entregaveis:

1. **Configuracao do GitHub Project** — estrutura de colunas, labels padronizadas e milestones
2. **Issues para cada arquivo faltante** — com prioridade, milestone, estimativa e dependencias
3. **Ordem de execucao** — sequencia que respeita dependencias entre niveis e maximiza paralelismo
4. **Guia de conteudo** — template e estilo para cada tipo de arquivo, baseado nos padroes existentes
5. **Scripts de automacao** — comandos `gh` para criar milestones, labels e issues em lote

Ao final, produza um plano executavel. Nao crie os arquivos de curriculo — apenas a estrutura de planejamento no GitHub.

---

## 1. Contexto: Estado Atual do Repositorio

### Projeto

`long-running-agents` — curriculo de 12 semanas sobre construcao de agentes IA que rodam por horas, aplicado ao KODA (agente de venda de suplementos via WhatsApp). O curriculo tem 4 niveis, 8 conceitos core, 35+ diagramas, 12 exercicios e 5 case studies.

### O Que Ja Existe (28 arquivos com conteudo real)

**Documentos-raiz (7/7):** README.md, QUICK_START.md, MASTER_PLAN.md, EXECUTION_PLAN.md, GLOSSARY.md, INDEX.md, DELIVERY-COMPLETE.md

**Nivel 1 — Fundamentos (6 arquivos):**
- `01-nivel-1-fundamentals/01-why-agents-lose-plot.md`
- `01-nivel-1-fundamentals/02-token-budgeting.md`
- `01-nivel-1-fundamentals/03-basic-harness-patterns.md`
- `01-nivel-1-fundamentals/exercises/exercise-01-windowing.md`
- `01-nivel-1-fundamentals/exercises/exercise-02-structured-output.md`
- `01-nivel-1-fundamentals/koda-applications/nivel-1-koda.md`

**Nivel 2 — Padroes Praticos (7 arquivos):**
- `02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md`
- `02-nivel-2-practical-patterns/02-sprint-contracts.md`
- `02-nivel-2-practical-patterns/03-rubric-design.md`
- `02-nivel-2-practical-patterns/04-trace-reading.md`
- `02-nivel-2-practical-patterns/exercises/exercise-01.md`
- `02-nivel-2-practical-patterns/exercises/exercise-03.md`
- `02-nivel-2-practical-patterns/koda-applications/nivel-2-koda.md`

**Case Studies (6 arquivos):**
- `09-case-studies/00-all-case-studies.md`
- `09-case-studies/01-retro-game-maker.md`
- `09-case-studies/02-browser-daw-app.md`
- `09-case-studies/03-koda-product-discovery.md`
- `09-case-studies/04-koda-order-processing.md`
- `09-case-studies/05-koda-fulfillment-workflow.md`

**Knowledge Graphs (1 arquivo com conteudo):**
- `06-knowledge-graphs/00-all-diagrams.txt`

### O Que Falta (~65 arquivos, apenas `.gitkeep` ou ausentes)

| Bloco | Diretorio | Arquivos Faltantes |
|-------|-----------|-------------------|
| A | `03-nivel-3-advanced-architecture/` | 10 (5 conteudo + 3 exercicios + solutions + koda-app) |
| B | `04-nivel-4-koda-specific/` | 11 (5 conteudo + 2 exercicios + solutions + 3 case-studies) |
| C | `05-core-concepts/` | 8 (01 a 08) |
| D | `06-knowledge-graphs/` | ~11 (4 principais + ~7 detailed-graphs) |
| E | `07-implementation-guides/` | 6 (01-setup a 06-playbook) |
| F | `08-tools-templates/` | 6 (tracker, rubrics, templates) |
| G | `10-references/` | 3 (anthropic, timeline, resources) |
| H | Lacunas pontuais | `02-nivel-2/exercises/exercise-02.md`, `FAQ.md`, `solutions/` nos niveis 1 e 2 |

### Estrutura de Diretorios Atual (arvore real do git)

```
curriculum/
├── README.md ✅
├── QUICK_START.md ✅
├── MASTER_PLAN.md ✅
├── EXECUTION_PLAN.md ✅
├── GLOSSARY.md ✅
├── INDEX.md ✅
├── DELIVERY-COMPLETE.md ✅
├── 01-nivel-1-fundamentals/
│   ├── 01-why-agents-lose-plot.md ✅
│   ├── 02-token-budgeting.md ✅
│   ├── 03-basic-harness-patterns.md ✅
│   ├── exercises/
│   │   ├── exercise-01-windowing.md ✅
│   │   ├── exercise-02-structured-output.md ✅
│   │   └── solutions/ ❌ (vazio)
│   └── koda-applications/
│       └── nivel-1-koda.md ✅
├── 02-nivel-2-practical-patterns/
│   ├── 01-generator-evaluator-pattern.md ✅
│   ├── 02-sprint-contracts.md ✅
│   ├── 03-rubric-design.md ✅
│   ├── 04-trace-reading.md ✅
│   ├── exercises/
│   │   ├── exercise-01.md ✅
│   │   ├── exercise-02.md ❌
│   │   ├── exercise-03.md ✅
│   │   └── solutions/ ❌ (vazio)
│   └── koda-applications/
│       └── nivel-2-koda.md ✅
├── 03-nivel-3-advanced-architecture/ ❌ (COMPLETAMENTE VAZIO)
│   ├── exercises/ (.gitkeep)
│   └── koda-applications/ (.gitkeep)
├── 04-nivel-4-koda-specific/ ❌ (COMPLETAMENTE VAZIO)
│   ├── case-studies/ (.gitkeep)
│   ├── exercises/ (.gitkeep)
│   └── koda-applications/ (.gitkeep)
├── 05-core-concepts/ ❌ (COMPLETAMENTE VAZIO)
│   └── .gitkeep
├── 06-knowledge-graphs/
│   ├── 00-all-diagrams.txt ✅
│   └── detailed-graphs/ ❌ (vazio)
├── 07-implementation-guides/ ❌ (COMPLETAMENTE VAZIO)
│   └── .gitkeep
├── 08-tools-templates/ ❌ (COMPLETAMENTE VAZIO)
│   └── .gitkeep
├── 09-case-studies/
│   ├── 00-all-case-studies.md ✅
│   ├── 01-retro-game-maker.md ✅
│   ├── 02-browser-daw-app.md ✅
│   ├── 03-koda-product-discovery.md ✅
│   ├── 04-koda-order-processing.md ✅
│   └── 05-koda-fulfillment-workflow.md ✅
└── 10-references/ ❌ (COMPLETAMENTE VAZIO)
    └── .gitkeep
```

---

## 2. Padroes de Conteudo Existentes (Referencia de Estilo)

### Cabecalho de Modulo de Conteudo

Todo arquivo de conteudo principal segue este template:

```markdown
# [EMOJI] Titulo Principal
## Subtitulo Descritivo

**Tempo Estimado:** XX minutos
**Nivel:** X - Nome do Nivel
**Pre-requisito:** Descricao do que precisa antes
**Status:** [EMOJI] CRITICO - Descricao do impacto
**Data de Criacao:** Maio 2026

---

## [EMOJI] Prologo: [Narrativa Envolvente]

[Paragrafo contextualizando com cenario real do KODA, usando metricas e storytelling]

[Transicao para o conteudo tecnico]
```

### Caracteristicas do Estilo

- **Narrativa em primeira pessoa do plural** ("Voce vai aprender", "Imagine KODA")
- **Persona Fernando** — fundador ficticio da KODA, usado como fio narrativo
- **Exemplos concretos** com metricas reais (75% → 98%, "R$0.50 por resposta")
- **Diagramas ASCII** e tabelas comparativas
- **Secoes com emojis** como separadores visuais
- **Profundidade alta** — arquivos de 600 a 3400 linhas
- **Portugues brasileiro** com termos tecnicos em ingles
- **Conexoes explicitas** entre modulos ("Voce aprendeu em Nivel 1 que...")

### Template de Exercicio

```markdown
# [EMOJI] Exercicio N: Titulo

**Nivel:** X - Nome
**Tempo Estimado:** XX-XX minutos
**Dificuldade:** [ESTRELAS] (Nivel)
**Pre-requisito:** Ter lido [arquivo]
**Status:** Hands-On Pratico

---

## [EMOJI] Objetivo

[Lista do que o aluno vai implementar]

## [EMOJI] O Problema Real

[Cenario contextualizado com metricas]

## [EMOJI] Requisitos

### Funcional
- [ ] Item 1
- [ ] Item 2

### Tecnico
- [ ] Item 1
- [ ] Item 2

## [EMOJI] Implementacao

[Codigo Python completo, testes, validacao]

## [EMOJI] Validacao

[Como verificar que funciona, testes esperados]
```

### Template de Aplicacao KODA

```markdown
# [EMOJI] KODA em Acao: [Titulo]
## [Subtitulo]

**Tempo Estimado:** XX-XX minutos
**Nivel:** X - Nome
**Pre-requisitos:** [Lista]
**Status:** [EMOJI] CRITICO - [Descricao]
**Data de Criacao:** Maio 2026

---

## [EMOJI] Prologo: [Narrativa com Fernando/KODA]

[Cenario realista com problema e solucao]

## [EMOJI] Objetivos Deste Modulo

[Lista de objetivos]

## [EMOJI] Parte 1: [Topico]

[Conteudo com codigo, tabelas, exemplos KODA]
```

### Template de Case Study

```markdown
# Estudo de Caso N: Titulo

**Nivel de Complexidade:** Nivel X-Y
**Duracao de Runtime:** X+ horas
**Foco:** Conceitos abordados

---

## Problema
[Descricao]

## Abordagem Inicial (Falha)
[Diagrama ASCII mostrando o que deu errado]

## Solucao: [Nome do Pattern]
[Diagrama ASCII mostrando arquitetura corrigida, fases numeradas]

## [Detalhamento]
[Explicacao de cada componente, codigo quando relevante]

## Resultados
[Metricas comparativas]
```

---

## 3. Estrategia de Priorizacao e Dependencias

### Grafo de Dependencias

```
Nivel 3 (conteudo principal)
  ├── Depende de: Nivel 1, Nivel 2 (ja existem)
  ├── Alimenta: Core Concepts (referencia cruzada)
  └── Paralelo com: Knowledge Graphs (Nivel 3)

Nivel 4 (KODA-especifico)
  ├── Depende de: Nivel 1, Nivel 2, Nivel 3
  ├── Alimenta: Case Studies (KODA-specific)
  └── Paralelo com: Implementation Guides

Core Concepts (05)
  ├── Depende de: Nivel 1, Nivel 2, Nivel 3 (conteudo ja escrito)
  ├── Funcao: Aprofundamento/destilacao
  └── Pode ser escrito em paralelo com Nivel 4

Knowledge Graphs (06)
  ├── Depende de: Core Concepts (para ter o que mapear)
  └── Pode comecar apos cada Core Concept

Implementation Guides (07)
  ├── Depende de: Nivel 3, Nivel 4 (padroes e aplicacao)
  └── Funcao: Guias praticos de implementacao

Tools & Templates (08)
  ├── Independencia: Pode ser criado a qualquer momento
  └── Funcao: Templates reutilizaveis

References (10)
  ├── Independencia: Pode ser criado a qualquer momento
  └── Funcao: Material de consulta externa
```

### Ordem de Execucao Recomendada (Fases)

**Fase 1 — Fundacao Avancada (Bloco A: Nivel 3)**
Arquivos: 10 | Milestone: `curriculum-nivel-3`
Ordem interna: 01 → 02 → 03 → 04 → 05 → exercicios → koda-app

**Fase 2 — Aplicacao KODA (Bloco B: Nivel 4)**
Arquivos: 11 | Milestone: `curriculum-nivel-4`
Ordem interna: 01 → 02 → 03 → 04 → 05 → exercicios → case-studies

**Fase 3 — Conceitos Core + Knowledge Graphs (Blocos C + D)**
Arquivos: 19 | Milestone: `curriculum-core-concepts`
Ordem: Core Concepts 01-08 em sequencia, depois Knowledge Graphs

**Fase 4 — Guias e Templates (Blocos E + F)**
Arquivos: 12 | Milestone: `curriculum-guides-templates`
Ordem: Guias primeiro, Templates depois (podem ser paralelos)

**Fase 5 — Referencias e Lacunas (Blocos G + H)**
Arquivos: 6 | Milestone: `curriculum-references`
Ordem: Qualquer ordem, todos independentes

---

## 4. Configuracao do GitHub

### Labels

Crie as seguintes labels no repositorio:

| Label | Cor | Descricao |
|-------|-----|-----------|
| `curriculum/nivel-3` | `#d73a4a` | Conteudo do Nivel 3 — Arquitetura Avancada |
| `curriculum/nivel-4` | `#a2eeef` | Conteudo do Nivel 4 — KODA-Especifico |
| `curriculum/core-concepts` | `#0e8a16` | Conceitos Core (05-core-concepts) |
| `curriculum/knowledge-graphs` | `#5319e7` | Knowledge Graphs (06) |
| `curriculum/guides` | `#fbca04` | Implementation Guides (07) |
| `curriculum/templates` | `#d4c5f9` | Tools & Templates (08) |
| `curriculum/references` | `#b60205` | References (10) |
| `curriculum/exercises` | `#0052cc` | Exercicios e solucoes |
| `curriculum/gap` | `#f9d0c4` | Lacunas em diretorios existentes |
| `type/content` | `#c5def5` | Criacao de arquivo de conteudo |
| `type/exercise` | `#bfdadc` | Criacao de exercicio |
| `type/template` | `#fef2c0` | Criacao de template |
| `priority/high` | `#d93f0b` | Bloqueia fases seguintes |
| `priority/medium` | `#fbca04` | Importante, mas nao bloqueante |
| `priority/low` | `#0e8a16` | Nice to have |

### Milestones

| Milestone | Descricao | Arquivos |
|-----------|-----------|----------|
| `curriculum-nivel-3` | 10 arquivos do Nivel 3 — Arquitetura Avancada | Bloco A |
| `curriculum-nivel-4` | 11 arquivos do Nivel 4 — KODA-Especifico | Bloco B |
| `curriculum-core-concepts` | 8 conceitos core + diagramas | Bloco C + D (inicio) |
| `curriculum-knowledge-graphs` | 11 Knowledge Graphs | Bloco D (completo) |
| `curriculum-guides` | 6 guias de implementacao | Bloco E |
| `curriculum-templates` | 6 templates | Bloco F |
| `curriculum-references` | 3 referencias + lacunas | Bloco G + H |

### GitHub Project (Kanban)

Colunas do board:

```
📋 Backlog         → 🏗️ In Progress    → 👁️ Review         → ✅ Done
   (priorizado)        (1 issue por vez)    (peer review)       (merged)
```

---

## 5. Templates de Issue por Tipo

### Template: Conteudo Principal (Nivel 3 e 4)

```markdown
---
title: "[Nivel X] Criar [Numero]-[slug].md — [Titulo do Modulo]"
labels: ["curriculum/nivel-X", "type/content", "priority/high"]
milestone: "curriculum-nivel-X"
---

## Arquivo a Criar

`curriculum/0X-nivel-X-[nome]/[numero]-[slug].md`

## Descricao do Modulo

[2-3 frases sobre o que este modulo cobre, extraidas do MASTER_PLAN.md]

## Topicos a Cobrir

- [ ] Topico 1
- [ ] Topico 2
- [ ] Topico 3

## Requisitos de Conteudo

- [ ] Prologo narrativo com cenario KODA realista
- [ ] Metricas e dados concretos (ex: "75% → 98%")
- [ ] Tabelas comparativas onde relevante
- [ ] Diagramas ASCII de arquitetura/fluxo
- [ ] Conexao explicita com modulos anteriores
- [ ] Secao "O Que Voce Aprendeu" ao final
- [ ] Minimo 600 linhas de conteudo

## Criterios de Aceitacao

- [ ] Arquivo existe no caminho correto
- [ ] Segue template de modulo (cabecalho, prologo, secoes)
- [ ] Portugues brasileiro com termos tecnicos em ingles
- [ ] Referencias cruzadas com outros modulos funcionam
- [ ] Nenhum placeholder "TBD" ou "TODO"

## Dependencias

- Nivel 1 e Nivel 2 concluidos (ja existem)
```

### Template: Exercicio

```markdown
---
title: "[Exercicio] Criar exercise-0X.md — Nivel X — [Topico]"
labels: ["curriculum/nivel-X", "curriculum/exercises", "type/exercise", "priority/medium"]
milestone: "curriculum-nivel-X"
---

## Arquivo a Criar

`curriculum/0X-nivel-X-[nome]/exercises/exercise-0X.md`

## Topico do Exercicio

[Qual conceito/pratica este exercicio avalia]

## Requisitos

- [ ] Cenario realista com problema contextualizado
- [ ] Lista de requisitos funcionais e tecnicos
- [ ] Codigo Python completo (minimo 200 linhas)
- [ ] Secao de validacao com testes esperados
- [ ] Dificuldade claramente indicada (1-5 estrelas)

## Criterios de Aceitacao

- [ ] Aluno consegue implementar em 60-90 minutos
- [ ] Exercicio testa compreensao, nao apenas copia-cola
- [ ] Solucao incluida em `solutions/`

## Dependencias

- Modulo de conteudo correspondente deve existir primeiro
```

### Template: Core Concept

```markdown
---
title: "[Core Concept] Criar 0X-[slug].md — [Nome do Conceito]"
labels: ["curriculum/core-concepts", "type/content", "priority/medium"]
milestone: "curriculum-core-concepts"
---

## Arquivo a Criar

`curriculum/05-core-concepts/0X-[slug].md`

## Conceito

[Nome do conceito e descricao de 1 frase]

## Requisitos

- [ ] Explicacao profunda (3-5 secoes)
- [ ] 3 diagramas Mermaid (conceito, fluxo, aplicacao)
- [ ] Aplicacao pratica no KODA
- [ ] Checklist de implementacao
- [ ] Referencias cruzadas com modulos dos niveis

## Criterios de Aceitacao

- [ ] Conceito explicado em profundidade (nao apenas resumo)
- [ ] Diagramas Mermaid renderizam corretamente
- [ ] Conexao KODA pratica e concreta

## Dependencias

- Modulo(s) de nivel correspondente devem existir
```

### Template: Knowledge Graph

```markdown
---
title: "[Knowledge Graph] Criar [arquivo].md — [Nome do Grafo]"
labels: ["curriculum/knowledge-graphs", "type/content", "priority/low"]
milestone: "curriculum-knowledge-graphs"
---

## Arquivo a Criar

`curriculum/06-knowledge-graphs/[arquivo].md`

## Diagrama(s) a Incluir

- [ ] Diagrama Mermaid principal (conceito/ecossistema)
- [ ] Diagrama de fluxo (processo)
- [ ] Diagrama de aplicacao KODA

## Criterios de Aceitacao

- [ ] Diagramas Mermaid renderizam corretamente
- [ ] Conexoes entre conceitos visualmente claras
- [ ] Consistente com 00-all-diagrams.txt

## Dependencias

- Core Concept correspondente deve existir
```

---

## 6. Comandos `gh` para Setup Inicial

Execute estes comandos para configurar o GitHub Project, Labels e Milestones. Substitua `owner/repo` pelo repositorio real.

### Criar Labels

```bash
# Labels de curriculo
gh label create "curriculum/nivel-3" --color d73a4a --description "Conteudo do Nivel 3"
gh label create "curriculum/nivel-4" --color a2eeef --description "Conteudo do Nivel 4"
gh label create "curriculum/core-concepts" --color 0e8a16 --description "Core Concepts"
gh label create "curriculum/knowledge-graphs" --color 5319e7 --description "Knowledge Graphs"
gh label create "curriculum/guides" --color fbca04 --description "Implementation Guides"
gh label create "curriculum/templates" --color d4c5f9 --description "Tools & Templates"
gh label create "curriculum/references" --color b60205 --description "References"
gh label create "curriculum/exercises" --color 0052cc --description "Exercicios e solucoes"
gh label create "curriculum/gap" --color f9d0c4 --description "Lacunas em diretorios existentes"

# Labels de tipo
gh label create "type/content" --color c5def5 --description "Arquivo de conteudo principal"
gh label create "type/exercise" --color bfdadc --description "Exercicio pratico"
gh label create "type/template" --color fef2c0 --description "Template reutilizavel"

# Labels de prioridade
gh label create "priority/high" --color d93f0b --description "Bloqueia fases seguintes"
gh label create "priority/medium" --color fbca04 --description "Importante, nao bloqueante"
gh label create "priority/low" --color 0e8a16 --description "Nice to have"
```

### Criar Milestones

```bash
gh milestone create "curriculum-nivel-3" --title "Nivel 3 — Arquitetura Avancada" \
  --description "10 arquivos: 5 modulos + 3 exercicios + solutions + koda-app"

gh milestone create "curriculum-nivel-4" --title "Nivel 4 — KODA-Especifico" \
  --description "11 arquivos: 5 modulos + 2 exercicios + solutions + 3 case-studies"

gh milestone create "curriculum-core-concepts" --title "Core Concepts — 8 Conceitos" \
  --description "8 arquivos de conceitos em profundidade"

gh milestone create "curriculum-knowledge-graphs" --title "Knowledge Graphs — 35+ Diagramas" \
  --description "11 arquivos de diagramas Mermaid"

gh milestone create "curriculum-guides" --title "Implementation Guides" \
  --description "6 guias praticos de implementacao"

gh milestone create "curriculum-templates" --title "Tools & Templates" \
  --description "6 templates reutilizaveis"

gh milestone create "curriculum-references" --title "References & Lacunas" \
  --description "3 referencias + FAQ + exercise-02 Nivel 2 + solutions"
```

### Criar Issues em Lote (exemplo para Nivel 3)

```bash
# Exemplo: criar uma issue para o primeiro modulo do Nivel 3
gh issue create \
  --title "[Nivel 3] Criar 01-multi-agent-systems.md — Multi-Agent Systems" \
  --body "$(cat <<'EOF'
## Arquivo a Criar
`curriculum/03-nivel-3-advanced-architecture/01-multi-agent-systems.md`

## Descricao
Design de sistemas com 3+ agentes coordenados. Cobre o padrao Planner/Generator/Evaluator, canais de comunicacao entre agentes, strategies de coordenacao (sequencial, paralelo, event-driven) e aplicacao no contexto KODA.

## Criterios de Aceitacao
- [ ] Prologo narrativo com cenario KODA
- [ ] Diagrama ASCII da arquitetura 3-agent
- [ ] Tabela comparativa de strategies de coordenacao
- [ ] Secao de aplicacao KODA
- [ ] Minimo 800 linhas
EOF
)" \
  --label "curriculum/nivel-3,type/content,priority/high" \
  --milestone "curriculum-nivel-3"
```

---

## 7. Checklist de Verificacao Final

Ao concluir a execucao de todas as fases, verifique:

- [ ] `curriculum/README.md` referencia corretamente todos os arquivos criados
- [ ] `curriculum/INDEX.md` lista todos os novos arquivos
- [ ] `curriculum/MASTER_PLAN.md` tem tabelas de status atualizadas (⏳ → ✅)
- [ ] Nao existem mais diretorios apenas com `.gitkeep`
- [ ] Links cruzados entre arquivos funcionam (ex: "Veja 05-core-concepts/01-context-management.md")
- [ ] Todos os diagramas Mermaid renderizam
- [ ] `git status` mostra apenas arquivos novos/modificados do curriculo
- [ ] Nenhum placeholder "TBD", "TODO", "em construcao"

---

## 8. Entregaveis Esperados

Ao executar esta estrategia, voce deve produzir:

1. **GitHub Project board** configurado com colunas de kanban
2. **~65 issues** criadas e atribuidas aos milestones corretos
3. **Labels e milestones** criados conforme especificado
4. **Script de criacao em lote** (`scripts/create-curriculum-issues.sh`) para criar todas as issues de uma vez
5. **Relatorio de cobertura** mostrando que cada arquivo do MASTER_PLAN tem uma issue correspondente

---

*Prompt para Estrategia de Execucao | Curriculum Long-Running Agents | v1.0 | Maio 2026*
