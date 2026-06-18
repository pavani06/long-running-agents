---
title: "Prompt: Análise de Arquitetura para Página Web Interativa do Currículo KODA"
type: prompt
date: 2026-05-26
tags:
  - stack-tooling
  - curriculo-conteudo
aliases:
  - analise web interativa
  - web architecture analysis
  - pagina web curriculo
relates-to:
  - "[[prompts/PROMPTS-00-INDEX|Prompt Index]]"
  - "[[web/koda_course_portal.html|KODA Course Portal]]"
---

# PROMPT: Análise de Arquitetura para Página Web Interativa do Currículo KODA

**Tipo:** Prompt de análise técnica
**Tempo estimado de execução:** 30-45 min (análise) + implementação posterior
**Output esperado:** Documento de análise arquitetural com plano de implementação

---

## CONTEXTO DO PROJETO

Temos um currículo completo sobre "Long-Running Agents para KODA" distribuído em dezenas de arquivos `.md` no diretório `curriculum/`. Já existe um portal HTML inicial em `web/koda_course_portal.html` que é apenas uma casca de navegação — ele referencia os módulos via metadados em JavaScript mas não contém o conteúdo real dos módulos.

Queremos construir uma página web interativa **completa** para hospedar na internet, onde o time possa ler e estudar TODO o conteúdo diretamente no site, sem nenhuma referência ou link para arquivos `.md` externos.

---

## INVENTÁRIO DO CONTEÚDO EXISTENTE

### Estrutura de diretórios (`curriculum/`):

```
curriculum/
├── README.md                          (visão geral do programa)
├── INDEX.md                           (índice executivo com navegação por perfil)
├── MASTER_PLAN.md                     (plano mestre, 568 linhas)
├── QUICK_START.md                     (guia rápido para iniciantes)
├── GLOSSARY.md                        (glossário de termos técnicos)
├── EXECUTION_PLAN.md                  (cronograma de 12 semanas)
├── DELIVERY-COMPLETE.md               (checklist de entrega)
│
├── 01-nivel-1-fundamentals/
│   ├── 01-why-agents-lose-plot.md     (649 linhas, explica 3 problemas fundamentais)
│   ├── 02-token-budgeting.md
│   ├── 03-basic-harness-patterns.md
│   ├── exercises/
│   │   ├── exercise-01.md
│   │   └── exercise-02.md
│   └── koda-applications/
│       └── nivel-1-koda.md
│
├── 02-nivel-2-practical-patterns/
│   ├── 01-generator-evaluator-pattern.md
│   ├── 02-sprint-contracts.md
│   ├── 03-rubric-design.md
│   ├── 04-trace-reading.md
│   ├── exercises/
│   │   ├── exercise-01.md
│   │   ├── exercise-02.md
│   │   └── exercise-03.md
│   └── koda-applications/
│       └── nivel-2-koda.md
│
├── 03-nivel-3-advanced-architecture/
│   ├── exercises/
│   └── koda-applications/
│
├── 04-nivel-4-koda-specific/
│   ├── case-studies/
│   ├── exercises/
│   └── koda-applications/
│
├── 05-core-concepts/                  (8 conceitos, status variado)
├── 06-knowledge-graphs/
│   ├── 00-all-diagrams.txt           (35+ diagramas Mermaid, 1037 linhas)
│   └── detailed-graphs/
├── 07-implementation-guides/
├── 08-tools-templates/
├── 09-case-studies/
│   ├── 00-all-case-studies.md         (1270 linhas, 5 estudos de caso)
│   ├── 01-retro-game-maker.md
│   ├── 02-browser-daw-app.md
│   ├── 03-koda-product-discovery.md
│   ├── 04-koda-order-processing.md
│   └── 05-koda-fulfillment-workflow.md
└── 10-references/
```

### Arquivos web existentes (`web/`):

- `koda_course_portal.html` — Portal interativo com tabs (Visão Geral, Módulos, Knowledge Graphs, Casos de Estudo, Checklist, Progresso, Roadmap). Contém metadados dos módulos no JS mas NÃO contém o conteúdo real. Usa localStorage para progresso.
- `koda_knowledge_graphs_35_diagrams.html` — Página separada com todos os 35 diagramas Mermaid renderizados.
- `mhc_visao_estrategica.html` — Página complementar de visão estratégica.

### Arquivos auxiliares:

- `rawfiles/` — Cópias dos prompts usados para gerar o conteúdo, arquivos de planejamento.
- `prompts/` — Prompts organizados (PROMPTS-00 a PROMPTS-04).

---

## REQUISITOS FUNCIONAIS

### 1. Conteúdo 100% inline

- **NENHUMA** referência a arquivos `.md`. Todo o conteúdo textual dos módulos, exercícios, casos de estudo, glossário, etc. deve estar embedado diretamente no HTML (ou em JSON/JS estático carregado pela página).
- Os diagramas Mermaid devem ser renderizados client-side via `mermaid.js` a partir das definições embedadas.
- Zero dependência de servidor backend. A página deve funcionar como site estático puro (HTML + CSS + JS).

### 2. Navegação interativa

- Estrutura hierárquica: Programa > Nível (1-4) > Módulo > Seção.
- Navegação lateral (sidebar) com árvore expansível de todos os conteúdos.
- Breadcrumb para orientação de localização.
- Busca full-text em todo o conteúdo com highlights.
- Filtros por nível (N1-N4), tipo de conteúdo (teoria, exercício, caso de estudo, diagrama), e tags (conceitos core: Context Management, Generator/Evaluator, etc.).
- Modo de leitura contínua: poder ler um módulo inteiro como página única com scroll.

### 3. Funcionalidades de estudo

- **Progresso por módulo**: marcar módulos como "não iniciado", "em progresso", "concluído". Persistir em localStorage.
- **Checklist por nível**: baseado nos checklists já definidos no `INDEX.md` e `MASTER_PLAN.md`.
- **Modo escuro/claro** com toggle.
- **Ajuste de fonte** (pequeno/médio/grande).
- **Tempo estimado de leitura** visível em cada módulo.
- **Indicador de progresso visual** (barra de progresso por nível e global).

### 4. Renderização de diagramas

- Todos os 35+ diagramas Mermaid definidos em `06-knowledge-graphs/00-all-diagrams.txt` devem ser renderizados client-side.
- Cada diagrama deve ter:
  - Título e descrição contextual
  - Tags de conceitos conectados
  - Indicador de nível relevante (N1-N4)
  - Botão para expandir/colapsar
  - Opção de zoom

### 5. Responsividade

- Funcionar em desktop, tablet e mobile.
- Sidebar colapsável em mobile (hamburger menu).
- Diagramas com scroll horizontal em telas pequenas.

### 6. SEO e compartilhamento

- Meta tags adequadas (title, description, og:image).
- Cada módulo/seção deve ter URL própria via hash (#nivel-1/modulo-1) para deep-linking.
- Sitemap XML para search engines.

---

## REQUISITOS TÉCNICOS

### Stack

- **HTML5 + CSS3 + Vanilla JavaScript** (sem frameworks, para deploy mínimo).
- **mermaid.js** (CDN) para renderização de diagramas.
- **localStorage** para persistência de progresso e preferências.
- **Nenhum build step**: o arquivo HTML final deve ser auto-contido e deployável diretamente.
- **Nenhuma dependência de npm/node**: apenas CDN para mermaid.js.

### Performance

- Conteúdo carregado sob demanda (lazy loading de seções) para não travar o browser com 5000+ linhas de texto de uma vez.
- Diagramas Mermaid renderizados apenas quando a seção correspondente se torna visível (IntersectionObserver).
- Minificação do HTML final para reduzir tamanho de download.

### Estrutura de dados embedada

O conteúdo deve ser estruturado em um grande objeto JavaScript com a seguinte hierarquia:

```
programa
├── metadados (título, versão, data)
├── niveis[]
│   ├── id, titulo, descricao, tempoEstimado, cor
│   └── modulos[]
│       ├── id, titulo, descricao, tempo, tags[]
│       ├── secoes[] (conteúdo textual em Markdown convertido para HTML)
│       └── exercicios[] (se existirem)
├── conceitosCore[]
│   ├── id, nome, definicao, conexoes[], prioridade, aplicacaoKoda
│   └── diagramas[] (definições Mermaid embedadas)
├── casosDeEstudo[]
│   ├── titulo, nivel, descricao, metricas[], conteudo (HTML)
│   └── sendMsg (prompt sugerido para exploração)
├── checklists[] (por nível)
├── roadmap (12 semanas)
└── glossario[] (termo -> definição)
```

### Conversão de Markdown para HTML

Todo o conteúdo `.md` deve ser convertido para HTML e embedado. Regras:
- Cabeçalhos (`#`, `##`, `###`, `####`) → tags `<h1>`-`<h4>` com âncoras.
- Parágrafos → `<p>`.
- Listas (`-`, `*`, `1.`) → `<ul>`, `<ol>`, `<li>`.
- Blocos de código (``` ```) → `<pre><code>` com syntax highlighting via classes CSS.
- Citações (`>`) → `<blockquote>`.
- Tabelas → `<table>`, `<thead>`, `<tbody>`.
- Negrito (`**texto**`) → `<strong>`.
- Itálico (`*texto*`) → `<em>`.
- Links internos devem ser convertidos para navegação SPA (hash-based), não links para arquivos `.md`.
- Emojis e ícones Unicode devem ser preservados.
- Quebras de linha e separadores (`---`) devem ser convertidos adequadamente.

---

## ENTREGÁVEIS DA ANÁLISE

### 1. Documento de Arquitetura

Responda estas perguntas no documento de análise:

#### Estratégia de conteúdo
- Qual o volume total estimado de conteúdo (linhas, caracteres, KB)?
- É viável um único HTML ou o conteúdo deve ser dividido em múltiplos arquivos HTML?
- Qual a melhor estratégia para embedar o conteúdo: tudo inline no HTML vs. arquivos JSON separados vs. chunks carregados sob demanda?
- Como estruturar o objeto de dados JavaScript para minimizar duplicação e maximizar performance?

#### Estrutura de componentes
- Quais componentes de UI são necessários? Desenhe a árvore de componentes.
- Como organizar o CSS? Variáveis CSS? Metodologia (BEM, utility-first)?
- Como o sistema de navegação (sidebar + breadcrumb + busca) se relaciona com o estado da aplicação?

#### Fluxo de dados
- Como o estado da aplicação (nível atual, módulo atual, progresso, preferências) é gerenciado?
- Como a busca full-text funciona sem backend?
- Como o roteamento baseado em hash funciona para deep-linking?

#### Estratégia de renderização
- Como os diagramas Mermaid são carregados e renderizados sem bloquear a página?
- Como o lazy loading de conteúdo funciona? Quais seções são críticas para o first paint?
- Como garantir que a página não trave ao carregar 35+ diagramas?

#### Deploy e hosting
- Onde hospedar? (GitHub Pages, Netlify, Vercel, Cloudflare Pages)
- Qual o tamanho final estimado do artefato?
- Estratégia de cache e CDN.

### 2. Plano de Implementação

- Sequência de passos para construir a página (ordem lógica de desenvolvimento).
- Estimativa de esforço por etapa.
- Riscos e mitigadores identificados.

### 3. Protótipo de Estrutura

- Esqueleto da árvore de componentes em pseudocódigo.
- Esboço da estrutura do objeto de dados (schema do grande dataset JavaScript).
- Mockup da estrutura HTML (elementos principais, sem conteúdo real).

---

## RESTRIÇÕES

1. **NÃO** gerar a página completa nesta análise. O objetivo é planejar, não implementar.
2. **NÃO** propor soluções que exijam servidor backend, banco de dados, ou build tools (webpack, vite, etc.).
3. **NÃO** referenciar arquivos `.md` em links ou imports — todo conteúdo deve ser inline.
4. **NÃO** usar frameworks React, Vue, Angular, Svelte, etc. Vanilla JS apenas.
5. **NÃO** inventar conteúdo que não existe — usar apenas o que está nos diretórios `curriculum/`, `rawfiles/`, e `web/`.
6. **NÃO** apagar ou modificar os arquivos `.md` existentes — eles são a fonte de verdade.

---

## REFERÊNCIAS PARA CONSULTA

Antes de começar a análise, leia estes arquivos para entender o escopo completo:

1. `curriculum/README.md` — Visão geral do programa e estrutura
2. `curriculum/INDEX.md` — Índice executivo com todos os caminhos de navegação
3. `curriculum/MASTER_PLAN.md` — Plano mestre com estrutura completa
4. `web/koda_course_portal.html` — Portal existente (referência de UI e metadados)
5. `curriculum/01-nivel-1-fundamentals/01-why-agents-lose-plot.md` — Exemplo de módulo de conteúdo real (649 linhas)
6. `curriculum/09-case-studies/00-all-case-studies.md` — Exemplo de caso de estudo (1270 linhas)
7. `curriculum/06-knowledge-graphs/00-all-diagrams.txt` — Exemplo de diagramas Mermaid (1037 linhas)
8. `curriculum/GLOSSARY.md` — Glossário de termos

---

## FORMATO DE SAÍDA

Entregue o documento de análise em Markdown, estruturado nestas seções:

```markdown
# Análise de Arquitetura: Página Web Interativa do Currículo KODA

## 1. Resumo Executivo
(2-3 parágrafos sobre a abordagem recomendada)

## 2. Inventário e Dimensionamento
(volume de conteúdo, estimativas de tamanho)

## 3. Arquitetura da Aplicação
### 3.1 Estrutura de Arquivos
### 3.2 Árvore de Componentes
### 3.3 Modelo de Dados (schema do dataset JavaScript)
### 3.4 Fluxo de Navegação e Roteamento
### 3.5 Gerenciamento de Estado

## 4. Estratégia de Conteúdo
### 4.1 Conversão Markdown → HTML
### 4.2 Embedding de Diagramas Mermaid
### 4.3 Lazy Loading e Performance

## 5. Design de Interface
### 5.1 Layout Principal (desktop e mobile)
### 5.2 Sistema de Cores e Temas
### 5.3 Componentes de Navegação
### 5.4 Componentes de Estudo

## 6. Funcionalidades Interativas
### 6.1 Busca Full-Text
### 6.2 Progresso e Checkpoints
### 6.3 Filtros e Ordenação

## 7. Plano de Implementação
(sequência de passos, estimativas, riscos)

## 8. Hosting e Deploy

## 9. Decisões em Aberto
(perguntas que precisam de resposta antes da implementação)
```
