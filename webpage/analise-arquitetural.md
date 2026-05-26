# Análise de Arquitetura: Página Web Interativa do Currículo KODA

## 1. Resumo Executivo

A recomendação arquitetural é construir uma aplicação estática de página única com um ponto de entrada leve e múltiplos assets estáticos de conteúdo carregados sob demanda. O currículo KODA tem 32 arquivos `.md`/`.txt`, 37.453 linhas e aproximadamente 1,3 MB de conteúdo bruto, além de 34 diagramas Mermaid identificados em `curriculum/06-knowledge-graphs/00-all-diagrams.txt`. Embutir tudo em um único objeto JavaScript dentro de um HTML criaria um problema de inicialização: o navegador teria que baixar, parsear e compilar conteúdo que o usuário talvez nunca abra antes de exibir uma experiência útil.

O modelo proposto preserva a restrição de site estático puro: HTML5, CSS3 e Vanilla JavaScript, sem backend, sem banco de dados e sem build tools. A diferença é que o HTML principal deve funcionar como shell leve, enquanto `assets/content/*.json` ou chunks Markdown/texto estáticos contêm o currículo por nível, módulo ou grupo. Essa abordagem continua entregando todo o conteúdo pelo próprio site, sem links para arquivos Markdown externos na experiência do usuário, mas permite cache, inspeção, substituição de módulos e carregamento assíncrono.

O portal existente em `web/koda_course_portal.html` deve ser tratado como referência de linguagem visual e padrão data-driven, não como base final. Ele já usa arrays de metadados, cards, tabs, progress bars, badges `badge-n1` a `badge-n4`, grids e render functions. Porém, hoje é metadata-only: não contém o conteúdo real, não possui hash routing, sidebar hierárquica, breadcrumbs, busca full-text, persistência real em `localStorage`, dark mode, controle de fonte nem estratégia responsiva completa. A nova arquitetura deve reaproveitar o padrão declarativo, mas substituir a navegação por uma SPA com rotas `#/...`, árvore lateral, renderização de conteúdo ativo, busca assíncrona e Mermaid lazy-rendered.

## 2. Inventário e Dimensionamento

O inventário técnico consolidado aponta 32 arquivos Markdown/texto com conteúdo real, 37.453 linhas e cerca de 1,3 MB bruto. Existem ainda 10 placeholders `.gitkeep` vazios, que não entram no payload de conteúdo. O volume é concentrado: os 10 maiores arquivos somam grande parte do currículo, com destaque para `02-nivel-2-practical-patterns/04-trace-reading.md` com 5.089 linhas, `02-nivel-2-practical-patterns/03-rubric-design.md` com 4.130 linhas e `02-nivel-2-practical-patterns/koda-applications/nivel-2-koda.md` com 3.417 linhas. Esses números tornam inadequado converter, indexar e renderizar tudo no `DOMContentLoaded`.

O currículo se organiza em 4 níveis, 8 conceitos core, exercícios, aplicações KODA, guias, templates, glossário, plano de execução, casos de estudo e knowledge graphs. O `README.md` descreve o programa como 12 semanas, 4 níveis, 8 conceitos core e 35+ diagramas. O `MASTER_PLAN.md` detalha os tempos por nível: Nível 1 com 3-4 horas, Nível 2 com 6-8 horas, Nível 3 com 8-10 horas e Nível 4 contínuo com 10+ horas. O `INDEX.md` adiciona caminhos por perfil: iniciante, pessoa com LLMs, architect, pessoa focada em KODA e consulta rápida.

Os maiores módulos afetam diretamente a experiência de leitura. Um usuário pode abrir apenas `Trace Reading` ou `Rubric Design`, mas se tudo estiver inline no HTML, esses milhares de blocos de texto já terão sido baixados e parseados. A estratégia correta é manter um índice global pequeno com metadados, tempos, tags, relações e rotas, e carregar o corpo textual apenas quando o usuário entra em um módulo, seção, caso de estudo ou diagrama.

Os diagramas Mermaid são administráveis, mas não devem ser renderizados todos de uma vez. A análise identificou 34 diagramas em `00-all-diagrams.txt`: 24 graphs, 10 flowcharts, 30 simples, 4 médios e nenhum complexo. O maior diagrama tem 16 nós, `Complete KODA System Architecture`. A página existente `web/koda_knowledge_graphs_35_diagrams.html` usa import CDN de Mermaid e renderização sequencial; isso prova a viabilidade, mas a nova versão deve trocar renderização total por `IntersectionObserver` com `rootMargin: 200px` para renderizar apenas diagramas próximos do viewport.

Estimativa de payload final para MVP estático: shell HTML abaixo de 30 KB, CSS entre 40 e 80 KB, JavaScript da aplicação entre 80 e 160 KB, manifesto de metadados entre 60 e 150 KB, conteúdo bruto chunked em torno de 1,3 MB antes de compressão, índice de busca entre 300 KB e 1,5 MB dependendo da granularidade e biblioteca, Mermaid via CDN como dependência externa. A primeira carga deve baixar apenas shell, CSS, JS principal, manifesto e rota inicial; o restante deve vir por demanda ou em idle.

## 3. Arquitetura da Aplicação

### 3.1 Estrutura de Arquivos

A saída recomendada para `webpage/` é uma SPA estática com um HTML de entrada e assets relativos. Nenhum caminho deve ser root-relative, porque GitHub Pages pode servir o site em subpath. A estrutura proposta é:

```text
webpage/
├── index.html
├── sitemap.xml
├── robots.txt
├── assets/
│   ├── css/
│   │   ├── tokens.css
│   │   ├── layout.css
│   │   ├── components.css
│   │   └── content.css
│   ├── js/
│   │   ├── app.js
│   │   ├── router.js
│   │   ├── state.js
│   │   ├── content-loader.js
│   │   ├── markdown-renderer.js
│   │   ├── mermaid-renderer.js
│   │   ├── search.js
│   │   ├── search-worker.js
│   │   └── ui.js
│   ├── data/
│   │   ├── programa.json
│   │   ├── navigation.json
│   │   ├── diagrams.json
│   │   ├── glossary.json
│   │   ├── checklists.json
│   │   └── roadmap.json
│   └── content/
│       ├── nivel-1/
│       │   ├── modules.json
│       │   ├── exercises.json
│       │   └── koda-applications.json
│       ├── nivel-2/
│       │   ├── modules.json
│       │   ├── exercises.json
│       │   └── koda-applications.json
│       ├── nivel-3/
│       │   ├── modules.json
│       │   ├── exercises.json
│       │   └── koda-applications.json
│       ├── nivel-4/
│       │   ├── modules.json
│       │   ├── real-world-exercises.json
│       │   └── case-studies.json
│       ├── core-concepts.json
│       ├── case-studies.json
│       ├── guides.json
│       ├── templates.json
│       └── references.json
```

`index.html` deve conter apenas a estrutura raiz, metadados SEO, links CSS/JS relativos e containers principais. `assets/data/programa.json` é o manifesto canônico de alto nível com título, versão, níveis, módulos, tags, rotas, tempos e referências aos chunks. `assets/content/*` guarda conteúdo textual bruto como Markdown ou texto, não HTML pré-convertido, para manter proximidade com a fonte e evitar build step. `assets/js/markdown-renderer.js` converte somente a seção ativa em HTML no cliente.

Os arquivos `sitemap.xml` e `robots.txt` são estáticos. O sitemap deve listar a URL principal e, se decidido, URLs com fragmentos hash para compartilhamento, sabendo que crawlers podem ignorar fragmentos. Para SEO real, a página principal precisa ter metadados fortes e conteúdo introdutório indexável no shell, enquanto o deep-link por hash atende compartilhamento interno e navegação direta.

### 3.2 Árvore de Componentes

A aplicação deve ser organizada em componentes funcionais de Vanilla JS, não em classes de framework. A árvore conceitual é:

```text
KodaCurriculumApp
├── AppShell
│   ├── TopBar
│   │   ├── MenuToggle
│   │   ├── GlobalSearchInput
│   │   ├── ThemeToggle
│   │   └── FontScaleControl
│   ├── SidebarNavigation
│   │   ├── ProgramTree
│   │   ├── LevelGroup
│   │   ├── ModuleNode
│   │   └── SectionNode
│   ├── MainContentArea
│   │   ├── Breadcrumb
│   │   ├── RouteHeader
│   │   ├── StudyToolbar
│   │   ├── MarkdownContentRenderer
│   │   ├── MermaidDiagramBlock
│   │   └── NextPreviousNavigation
│   └── RightRail
│       ├── ReadingProgress
│       ├── OnPageToc
│       └── RelatedConcepts
├── SearchOverlay
│   ├── SearchFilters
│   ├── ResultList
│   └── HighlightedResultSnippet
├── ProgressDashboard
│   ├── GlobalProgressBar
│   ├── LevelProgressCards
│   └── ChecklistPanel
└── PreferencesLayer
    ├── ThemeState
    ├── FontScaleState
    └── LastRouteState
```

O `SidebarNavigation` substitui as tabs do portal atual como navegação principal. As tabs podem sobreviver apenas como filtros ou views resumidas em páginas de overview. O padrão de cards do portal atual permanece útil para `LevelProgressCards`, cards de casos de estudo, cards de conceitos core e cards de diagramas.

### 3.3 Modelo de Dados (schema do dataset JavaScript)

O schema deve manter a hierarquia exigida `programa > niveis > modulos > secoes`, mas adaptada às decisões de performance: metadados ficam no manifesto global; conteúdo bruto fica em chunks estáticos por módulo/grupo e é carregado sob demanda. O schema conceitual é:

```js
programa = {
  metadados: {
    id: "koda-long-running-agents",
    titulo: "Building Long-Running Agents para KODA",
    subtitulo: "Transformar equipe em especialistas de agentes que rodam por horas",
    versao: "1.0",
    data: "Maio 2026",
    duracao: "12 semanas",
    totalLinhas: 37453,
    tamanhoBrutoAproximado: "1.3MB",
    totalArquivosConteudo: 32,
    totalDiagramas: 34,
    idioma: "pt-BR"
  },
  niveis: [
    {
      id: "n1",
      codigo: "N1",
      titulo: "Conceitos Fundamentais",
      descricao: "Por que agentes falham em tarefas longas",
      tempoEstimado: "3-4 horas",
      cor: "var(--level-n1)",
      rota: "#/niveis/n1",
      criteriosConclusao: [
        "Entendo os 3 motivos pelos quais agentes perdem o foco",
        "Posso explicar context windows e token budgeting",
        "Consigo identificar um padrão de harness em código existente"
      ],
      modulos: [
        {
          id: "n1-01-why-agents-lose-plot",
          numero: "1.1",
          titulo: "Por que agentes perdem o fio",
          descricao: "3 modos de falha: context rot, context anxiety, planning collapse",
          tempo: "45-60 min",
          tipo: "teoria",
          nivel: "N1",
          tags: ["context-management", "harness", "agent-loop"],
          rota: "#/niveis/n1/modulos/why-agents-lose-plot",
          contentRef: "assets/content/nivel-1/modules.json#n1-01-why-agents-lose-plot",
          secoes: [
            {
              id: "n1-01-introducao",
              titulo: "Introdução",
              rota: "#/niveis/n1/modulos/why-agents-lose-plot/secao/introducao",
              anchor: "introducao",
              ordem: 1,
              estimatedWords: 0,
              contentRange: { startHeading: "Introdução", endHeading: "Os 3 modos de falha" }
            }
          ],
          exercicios: [
            {
              id: "n1-exercise-01-windowing",
              titulo: "Windowing",
              tipo: "exercicio",
              rota: "#/exercicios/n1/windowing",
              contentRef: "assets/content/nivel-1/exercises.json#n1-exercise-01-windowing"
            }
          ],
          diagramas: ["ctx-A", "ctx-B"],
          conceitosCore: ["context-management"],
          preRequisitos: [],
          proximoModulo: "n1-02-token-budgeting"
        }
      ]
    }
  ],
  conceitosCore: [
    {
      id: "context-management",
      nome: "Context Management",
      definicao: "Gerenciar o que entra na janela de contexto para maximizar qualidade e minimizar degradação.",
      nivelPrincipal: "N1",
      conexoes: ["state-persistence", "sprint-contracts"],
      prioridade: "alta",
      aplicacaoKoda: "Conversas WhatsApp multi-turn e memória de carrinho",
      contentRef: "assets/content/core-concepts.json#context-management",
      diagramas: ["ctx-A", "ctx-B", "ctx-C"]
    }
  ],
  diagramas: [
    {
      id: "ctx-A",
      titulo: "Hierarchical Connection Graph",
      descricao: "Pré-requisitos, relacionados e dependentes do conceito central",
      nivel: "N1",
      tipo: "graph",
      complexidade: "simples",
      tags: ["context-management", "token-budgeting"],
      mermaidRef: "assets/data/diagrams.json#ctx-A",
      render: { lazy: true, rootMargin: "200px" }
    }
  ],
  casosDeEstudo: [
    {
      id: "retro-game-maker",
      titulo: "Retro Game Maker",
      nivel: "N2-N3",
      descricao: "Caso de harness multi-agente e Generator/Evaluator",
      metricas: [],
      tags: ["generator-evaluator", "sprint-contracts"],
      rota: "#/casos/retro-game-maker",
      contentRef: "assets/content/case-studies.json#retro-game-maker",
      sendMsg: "Prompt sugerido para exploração assistida"
    }
  ],
  checklists: [
    {
      id: "checklist-n1",
      nivel: "N1",
      itens: [
        {
          id: "n1-criterio-3-problemas",
          texto: "Entendo os 3 motivos pelos quais agentes perdem o foco",
          linkedRoutes: ["#/niveis/n1/modulos/why-agents-lose-plot"]
        }
      ]
    }
  ],
  roadmap: {
    duracao: "12 semanas",
    etapas: [
      { id: "semana-1-2", titulo: "Fundação", nivel: "N1", objetivo: "Toda equipe entende o problema" },
      { id: "semana-3-4", titulo: "Padrões Práticos", nivel: "N2", objetivo: "Implementar 1 padrão no KODA" },
      { id: "semana-5-6", titulo: "Arquitetura Avançada", nivel: "N3", objetivo: "Design multi-agent e state persistence" },
      { id: "semana-7-12", titulo: "KODA-Específico", nivel: "N4", objetivo: "Aplicação e mentoria contínua" }
    ]
  },
  glossario: [
    {
      termo: "Harness",
      definicao: "Infraestrutura e padrões que envolvem agentes para fazê-los confiáveis por períodos longos.",
      nivel: "N1",
      verTambem: ["Agent", "State Persistence", "Evaluation Loop"]
    }
  ]
}
```

A regra principal é não duplicar conteúdo textual. O manifesto guarda título, descrição, tags, rotas e relações. O corpo real fica em `contentRef`, em Markdown bruto. Um `contentCache` em memória evita refetch dentro da mesma sessão; `localStorage` guarda apenas progresso e preferências, nunca currículo nem índice de busca.

### 3.4 Fluxo de Navegação e Roteamento

O roteamento deve ser baseado em hash, por exemplo `#/niveis/n2/modulos/rubric-design`, porque sites estáticos em GitHub Pages não garantem rewrites para history routing. O router observa `hashchange`, interpreta segmentos, valida contra `navigation.json`, atualiza estado ativo e aciona o carregamento de conteúdo da rota.

Fluxo recomendado:

```text
Usuário clica na sidebar ou abre deep link
→ window.location.hash muda
→ router parseia nível/módulo/seção/filtro
→ estado activeRoute é atualizado em memória
→ breadcrumb é derivado do manifesto
→ content-loader busca o chunk se não estiver em cache
→ markdown-renderer converte apenas o conteúdo ativo
→ mermaid-renderer observa blocos visíveis
→ state persiste lastRoute em localStorage
```

As rotas mínimas devem cobrir overview do programa, overview por nível, módulo, seção, exercícios, conceitos core, diagramas, casos de estudo, glossário, busca e progresso. Exemplos de rotas: `#/`, `#/niveis/n1`, `#/niveis/n2/modulos/trace-reading`, `#/conceitos/generator-evaluator`, `#/diagramas/ctx-A`, `#/casos/koda-order-processing`, `#/glossario/context-window`, `#/busca?q=rubric&nivel=N2`.

### 3.5 Gerenciamento de Estado

O estado deve ser simples, explícito e serializável. A aplicação mantém estado em memória e persiste apenas transições significativas em `localStorage` versionado. A chave recomendada é `koda:state:v1`.

Estado em memória:

```js
appState = {
  activeRoute: "#/",
  activeLevel: null,
  activeModule: null,
  activeSection: null,
  navigationTree: null,
  contentCache: new Map(),
  markdownCache: new Map(),
  search: {
    status: "idle",
    indexReady: false,
    query: "",
    filters: { niveis: [], tipos: [], tags: [] },
    results: []
  },
  progress: {
    modules: {},
    sections: {},
    checklists: {}
  },
  preferences: {
    theme: "system",
    fontScale: "medium",
    sidebarCollapsed: false,
    lastRoute: "#/"
  }
}
```

Persistência local:

```js
persistedState = {
  version: 1,
  updatedAt: "ISO-8601",
  progress: {
    modules: {
      "n2-03-rubric-design": { status: "em-progresso", completedAt: null, lastSection: "rubric-dimensions" }
    },
    sections: {
      "n2-03-rubric-design/rubric-dimensions": { completed: true, completedAt: "ISO-8601" }
    },
    checklists: {
      "n2-criterio-generator-evaluator": true
    }
  },
  preferences: {
    theme: "dark",
    fontScale: "large",
    lastRoute: "#/niveis/n2/modulos/rubric-design"
  }
}
```

Gravar no `localStorage` apenas quando o usuário marca módulo/seção como concluído, muda status de progresso, altera tema, ajusta fonte ou navega para uma rota relevante. Evitar writes a cada scroll. O estado é local ao navegador e dispositivo; não há sincronização entre pessoas ou máquinas no MVP.

## 4. Estratégia de Conteúdo

### 4.1 Conversão Markdown → HTML

A decisão recomendada é armazenar conteúdo como Markdown bruto e converter para HTML somente no render da rota ativa. Isso preserva a manutenção próxima aos arquivos fonte, evita um build step e impede parse/render global na inicialização. O conteúdo não deve aparecer como links para `.md` externos na UI: todos os links internos do currículo precisam ser transformados em rotas hash da SPA.

O conversor Markdown precisa suportar cabeçalhos `#` a `####` com anchors, parágrafos, listas ordenadas e não ordenadas, blocos de código, citações, tabelas, negrito, itálico, separadores, links internos e blocos Mermaid. Como não há build tool, a implementação pode ser um parser pequeno e controlado para o subset usado no currículo ou uma biblioteca client-side via CDN se a equipe aceitar uma dependência adicional. A análise favorece parser controlado para MVP de leitura se a restrição de CDN for rígida, e biblioteca madura apenas se a fidelidade Markdown exigir suporte mais amplo.

Regras de transformação:

```text
#, ##, ###, #### → headings com IDs estáveis
parágrafos → blocos de texto com largura máxima de 72ch
listas → listas semânticas preservando aninhamento básico
blocos de código → blocos com classe por linguagem quando declarada
blockquote → callouts editoriais
tabelas → tabelas responsivas com overflow horizontal
links internos para arquivos fonte → rotas hash equivalentes
links externos → links normais com indicação visual discreta
blocos mermaid → placeholders observáveis por IntersectionObserver
```

O render deve gerar uma tabela de conteúdos local para o módulo ativo, alimentar o breadcrumb, atualizar o título da rota e registrar seções para leitura contínua. Para módulos grandes, como `trace-reading` e `rubric-design`, a renderização inicial deve permitir skeleton/loading e, se necessário, quebrar a conversão por seções para não monopolizar o main thread.

### 4.2 Embedding de Diagramas Mermaid

Os diagramas devem ser armazenados como definições Mermaid estáticas em `assets/data/diagrams.json`, com título, descrição contextual, tags, nível, tipo, complexidade e código. A experiência deve oferecer expandir/colapsar, zoom e, se desejado, copiar código Mermaid. A página existente de knowledge graphs já demonstra o uso de `mermaid@11` via CDN, `mermaid.initialize({ startOnLoad: false })` e renderização manual; o problema é que ela renderiza todos os diagramas sequencialmente.

A nova estratégia:

```text
Conteúdo ativo inclui placeholders para diagramas
→ mermaid-renderer registra placeholders com IntersectionObserver
→ quando placeholder entra perto do viewport, carrega Mermaid se ainda não carregou
→ chama mermaid.run ou mermaid.render apenas para aquele nó
→ marca data-rendered=true
→ remove o nó do observer
```

Cuidados específicos: não renderizar Mermaid dentro de containers `display: none`, aguardar fontes quando necessário, escapar caracteres em código exibido, tratar subgraphs e `style` directives preservando sintaxe original, manter scroll horizontal em telas pequenas, evitar re-render em alternância de tabs ocultas e reprocessar apenas se troca de tema exigir novo tema Mermaid.

### 4.3 Lazy Loading e Performance

A performance depende de três regras: não carregar todo conteúdo na largada, não converter todo Markdown na largada e não indexar busca no main thread na largada. O first paint deve precisar apenas de `index.html`, CSS crítico, JS principal, manifesto de navegação e, opcionalmente, o conteúdo da rota inicial. O restante deve ser acionado por navegação, foco de busca ou `requestIdleCallback`.

Padrões recomendados:

```text
contentCache Map
→ fetch relativo do chunk quando rota exige
→ guarda resposta bruta em memória
→ markdownCache Map por contentId + versão
→ renderiza HTML ativo
→ descarta DOM antigo ao trocar rota
```

Para busca, carregar o mecanismo após `requestIdleCallback` ou no primeiro foco do campo de busca. O índice deve ser construído em Web Worker, dividido por grupos, para não travar a leitura. Para conteúdo grande, preferir índice por seção ou por módulo com snippets pré-computáveis nos chunks. Nunca armazenar o índice em `localStorage`; ele pode ser reconstruído ou buscado como asset cacheável.

Pitfalls que a implementação deve evitar: parse/convert/index/render de todo currículo no `DOMContentLoaded`, caminhos root-relative em GitHub Pages, histórico via `pushState`, Mermaid em containers escondidos, service worker no MVP, busca síncrona no main thread e gravação do currículo em `localStorage`.

## 5. Design de Interface

### 5.1 Layout Principal (desktop e mobile)

O layout deve ser mobile-first com CSS Grid para macroestrutura e Flexbox para alinhamentos locais. A leitura é o centro do produto, então o conteúdo textual deve ter largura máxima aproximada de `72ch`, boa altura de linha e controles de leitura visíveis, sem competir com a navegação.

Breakpoints recomendados:

```text
Base mobile: 1 coluna, top bar fixa, sidebar off-canvas, conteúdo full-width
>= 640px: layout tablet com navegação colapsável e cards em 2 colunas quando útil
>= 960px: sidebar fixa + área de conteúdo + right rail opcional
>= 1200px: sidebar, conteúdo 72ch e rail para TOC/progresso
```

No desktop, a tela deve ter sidebar hierárquica à esquerda, conteúdo no centro e rail direito para sumário da página, progresso de leitura e próximos passos. No mobile, sidebar vira menu hamburger, breadcrumb fica compacto, busca pode abrir overlay e diagramas precisam overflow horizontal ou modo zoom.

### 5.2 Sistema de Cores e Temas

O portal atual já define cores por nível: N1 verde, N2 azul, N3 âmbar/marrom, N4 vermelho e Knowledge Graph roxo. A nova UI deve transformar isso em tokens estáveis e expandir para dark mode.

Tokens recomendados:

```text
--level-n1, --level-n1-bg, --level-n1-strong
--level-n2, --level-n2-bg, --level-n2-strong
--level-n3, --level-n3-bg, --level-n3-strong
--level-n4, --level-n4-bg, --level-n4-strong
--kg, --kg-bg, --kg-strong
--surface-1, --surface-2, --surface-3
--text-1, --text-2, --text-muted
--border-subtle, --border-strong
--focus-ring
```

Dark mode deve ser aplicado por atributo no documento, por exemplo `data-theme="dark"`, respeitando `prefers-color-scheme` quando o usuário não escolheu manualmente. O tema escolhido entra em `localStorage`. A implementação não deve depender das variáveis do ambiente onde os HTMLs atuais foram colados; precisa definir seus próprios tokens em `webpage/assets/css/tokens.css`.

### 5.3 Componentes de Navegação

Componentes essenciais: sidebar expansível, breadcrumb, busca global, filtros, sumário local, next/previous, cards de nível, cards de módulo e navegação por perfil. O `INDEX.md` é fonte direta para entradas como “sou novo”, “conheço LLMs”, “sou architect”, “trabalho em KODA” e “preciso de resposta rápida”.

O sidebar deve seguir a hierarquia:

```text
Programa
├── Comece aqui
├── Nível 1: Conceitos Fundamentais
│   ├── Módulos
│   ├── Exercícios
│   └── Aplicação KODA
├── Nível 2: Padrões Práticos
├── Nível 3: Arquitetura Avançada
├── Nível 4: KODA-Específico
├── Conceitos Core
├── Knowledge Graphs
├── Casos de Estudo
├── Guias e Templates
├── Glossário
└── Progresso
```

Breadcrumb deve ser derivado da rota, não duplicado manualmente. Exemplo: `Programa > Nível 2 > Rubric Design > Dimensões de Rubric`. A busca global deve abrir em overlay no mobile e como painel no desktop. Filtros por nível, tipo de conteúdo e tags devem compartilhar estado com a URL para deep-linking de resultados.

### 5.4 Componentes de Estudo

Funcionalidades de estudo necessárias: status por módulo (`não iniciado`, `em progresso`, `concluído`), checklist por nível, barra de progresso por nível e global, tempo estimado de leitura, modo leitura contínua, ajuste de fonte, tema claro/escuro e retorno à última rota.

O tempo de leitura deve usar metadados quando existirem no `MASTER_PLAN.md` e estimativa por palavras/linhas quando o módulo não tiver tempo explícito. Para preservar honestidade, mostrar como “tempo estimado” e permitir granularidade por módulo. O progresso visual deve usar os totais reais por nível do manifesto, não os totais hardcoded do portal atual.

Componentes derivados do portal atual que devem ser mantidos em versão evoluída: `level-card`, `module-item`, `progress-bar`, `badge-n1` a `badge-n4`, `kg-card`, `case-card`, `check-item` e `roadmap-item`. Componentes novos: `breadcrumb`, `sidebar-tree`, `search-overlay`, `reading-toolbar`, `font-scale-control`, `theme-toggle`, `content-toc`, `mermaid-viewer` e `route-loading-state`.

## 6. Funcionalidades Interativas

### 6.1 Busca Full-Text

Para 37.453 linhas de conteúdo técnico bilíngue, a recomendação é usar FlexSearch para busca full-text, com Fuse.js reservado apenas se a busca ficar restrita a título/tag/navegação. FlexSearch oferece ranking melhor e suporte adequado a múltiplos campos. A contrapartida é mais peso e complexidade de indexação, por isso deve ser carregado tardiamente e rodar em Web Worker.

Modelo de indexação:

```text
Documento indexável
├── id
├── route
├── title
├── level
├── type
├── tags
├── headings
├── bodyText
└── snippets
```

Fluxo:

```text
Usuário foca busca ou browser fica idle
→ carrega search.js e search-worker.js
→ worker busca chunks indexáveis ou índice estático
→ cria índice por campos title, tags, headings e bodyText
→ UI envia query + filtros ao worker
→ worker retorna IDs, score e snippets
→ UI renderiza resultados com highlights
→ clique atualiza hash route
```

Há uma tensão com a restrição original “apenas CDN para mermaid.js”. Se essa restrição for absoluta, a alternativa é uma busca local simples com tokenização própria e índice invertido em JSON estático, mas isso reduz ranking e qualidade de resultados. Como a decisão arquitetural consolidada recomenda FlexSearch, o plano assume FlexSearch como dependência estática client-side sem npm e sem build step.

### 6.2 Progresso e Checkpoints

O progresso deve ser local e versionado. Estados por módulo: `nao-iniciado`, `em-progresso`, `concluido`. O estado `em-progresso` pode ser automático quando usuário abre uma seção ou manual quando clica “marcar em progresso”. O estado `concluido` deve ser ação explícita para evitar falsos positivos por scroll acidental.

Checklists devem vir do `MASTER_PLAN.md` e do `INDEX.md`. Exemplos reais: Nível 1 exige entender os 3 motivos pelos quais agentes perdem o foco, explicar context windows e token budgeting, identificar padrão de harness e completar exercícios. Nível 2 exige desenhar Generator/Evaluator, escrever Sprint Contracts, criar rubrics, ler traces e aplicar padrões ao KODA. Nível 3 exige desenhar sistema 3+ agentes, coordenação baseada em arquivo, harness evolution e apoio a decisões arquiteturais. Nível 4 exige diagnosticar traces reais do KODA, propor melhorias, implementar feature, criar rubrics e participar de decisões arquiteturais.

Persistência deve ocorrer em eventos significativos:

```text
markModuleStatus(moduleId, status)
toggleChecklistItem(itemId)
markSectionComplete(sectionId)
setTheme(theme)
setFontScale(scale)
saveLastRoute(route)
```

Não persistir o conteúdo do currículo, HTML renderizado, Mermaid SVG, índice de busca ou resultados. Esses dados pertencem ao cache HTTP do browser e ao cache em memória da sessão.

### 6.3 Filtros e Ordenação

Filtros mínimos: nível (`N1`, `N2`, `N3`, `N4`), tipo (`teoria`, `exercicio`, `caso-de-estudo`, `diagrama`, `conceito`, `guia`, `template`, `glossario`), tags de conceitos core e status de progresso. Ordenações mínimas: ordem curricular, tempo estimado, nível, relevância de busca e status de progresso.

Tags core devem refletir o vocabulário real do currículo: `context-management`, `planning-execution-separation`, `generator-evaluator`, `sprint-contracts`, `state-persistence`, `harness-evolution`, `multi-agent-coordination`, `evaluation-rubrics`, além de tags operacionais como `trace-reading`, `token-budgeting`, `koda-architecture`, `order-processing`, `fulfillment` e `product-discovery`.

Os filtros devem ser refletidos no hash quando afetam compartilhamento, por exemplo `#/busca?q=trace&nivel=N2&tipo=teoria` ou `#/diagramas?tag=generator-evaluator`. Para filtros temporários de uma lista local, o estado em memória basta.

## 7. Plano de Implementação

Sequência recomendada, com esforço estimado:

| Etapa | Entrega | Esforço |
|---|---|---:|
| 1 | Inventário final automatizado dos arquivos, rotas e metadados | 0,5-1 dia |
| 2 | Definir `programa.json`, `navigation.json`, `diagrams.json`, checklists e roadmap | 1-1,5 dia |
| 3 | Criar shell SPA estático em `webpage/index.html` com CSS base e tokens | 1 dia |
| 4 | Implementar router hash, parse de rotas e breadcrumb | 1 dia |
| 5 | Implementar sidebar hierárquica, cards de overview e navegação por perfil | 1-1,5 dia |
| 6 | Criar chunks de conteúdo estático por nível/grupo | 1-2 dias |
| 7 | Implementar `content-loader` com cache em memória e loading states | 0,5-1 dia |
| 8 | Implementar conversão Markdown subset e transformação de links internos em rotas | 2-3 dias |
| 9 | Implementar render de conteúdo ativo, TOC local, next/previous e leitura contínua | 1,5-2 dias |
| 10 | Implementar Mermaid lazy-render com `IntersectionObserver` e zoom | 1-1,5 dia |
| 11 | Implementar estado versionado em `localStorage`: progresso, tema, fonte e última rota | 1 dia |
| 12 | Implementar dashboard de progresso e checklists por nível | 1-1,5 dia |
| 13 | Implementar busca full-text com worker e FlexSearch ou índice próprio | 2-4 dias |
| 14 | Implementar filtros por nível, tipo, tag e status | 1 dia |
| 15 | Refinar responsividade mobile/tablet/desktop e acessibilidade de foco | 1,5-2 dias |
| 16 | Adicionar SEO: metadados, Open Graph, `sitemap.xml`, `robots.txt` e títulos por rota | 0,5-1 dia |
| 17 | QA de conteúdo: rotas quebradas, links internos, módulos grandes e diagramas | 2-3 dias |
| 18 | Performance pass: first load, busca, render de módulos grandes e Mermaid | 1-2 dias |

Estimativa total: 21 a 32 dias-pessoa para uma versão completa e polida. Um MVP útil com shell, navegação, conteúdo sob demanda, Markdown básico, progresso local e Mermaid lazy pode sair em 8 a 12 dias-pessoa, deixando busca avançada, filtros finos e refinamentos de SEO para a segunda iteração.

Riscos e mitigadores:

| Risco | Impacto | Mitigação |
|---|---|---|
| Markdown real usa padrões não cobertos pelo parser | Conteúdo quebrado ou mal formatado | Começar parser pelo subset observado e rodar QA em todos os chunks |
| Busca trava main thread | UX ruim em máquinas fracas | Worker obrigatório, inicialização em idle e índice por grupos |
| Módulos de 4-5 mil linhas demoram a renderizar | Rota parece congelada | Loading state, conversão por seção e cache de HTML ativo |
| Mermaid falha em subgraphs ou style directives | Diagramas invisíveis | Preservar código original, capturar erro por diagrama e manter fallback textual |
| GitHub Pages com subpath quebra assets | Site não carrega | Usar somente caminhos relativos e hash routing |
| SEO de deep links hash é limitado | Baixa indexação de módulos internos | Metadados fortes no shell, sitemap principal e compartilhamento interno via hash |
| Dependência FlexSearch conflita com restrição de CDN | Bloqueio de aprovação | Decidir explicitamente: aceitar CDN estático ou usar índice próprio com ranking simples |

Ordem de validação por etapa: primeiro conteúdo e roteamento com 3 módulos pequenos, depois 1 módulo grande, depois diagramas, depois progresso local, depois busca, depois responsividade. Não esperar o fim para testar os maiores arquivos.

## 8. Hosting e Deploy

Hospedagem recomendada para MVP: GitHub Pages, porque o artefato é estático, sem backend e compatível com hash routing. Netlify, Vercel e Cloudflare Pages também funcionam, mas adicionam recursos que o MVP não precisa. Como a aplicação não depende de rewrites, qualquer host estático serve.

Regras de deploy:

```text
Usar caminhos relativos em todos os assets
Usar hash routing para deep links
Não depender de headers customizados
Não usar service worker no MVP
Não exigir build step
Versionar assets por nome ou query simples se necessário
```

Estratégia de cache: `index.html` deve ser pequeno e atualizado com frequência; assets de conteúdo e dados podem ser cacheados pelo browser/CDN como arquivos estáticos. Se não houver controle de headers, versionar arquivos ou manifests com campo `version` resolve invalidation básica. Conteúdo chunked permite que alterações em Nível 2, por exemplo, não invalidem todo o currículo.

SEO e compartilhamento:

```text
title: KODA Training Center | Long-Running Agents Curriculum
description: Programa de 12 semanas sobre construção de agentes de longa duração para KODA, com 4 níveis, conceitos core, exercícios, estudos de caso e knowledge graphs.
lang: pt-BR
og:title, og:description, og:type, og:image
twitter:card
canonical apontando para a raiz publicada
sitemap.xml com URL principal e, se aprovado, entradas hash documentais
robots.txt permitindo indexação
```

Deep-linking por hash atende compartilhamento direto de módulos e seções, por exemplo `#/niveis/n3/modulos/state-persistence`. Ao carregar um hash, o app deve resolver rota, carregar chunk, renderizar conteúdo e rolar para seção se houver anchor. Para crawlers tradicionais, hashes podem não ser indexados como páginas separadas; portanto, o objetivo realista de SEO no MVP é indexar bem a landing do currículo e permitir compartilhamento interno confiável de rotas.

Tamanho final estimado: 1,8 a 4 MB de assets próprios não comprimidos dependendo do índice de busca e da duplicação de snippets. Com cache e carregamento sob demanda, o first load deve ficar muito menor: shell + CSS + JS + manifesto, idealmente abaixo de 400 KB próprios antes de bibliotecas CDN. Mermaid e FlexSearch, se usados via CDN, entram como custos externos carregados apenas quando necessários ou em idle.

## 9. Decisões em Aberto

1. FlexSearch é permitido como dependência client-side via CDN/asset estático, apesar da restrição inicial mencionar apenas Mermaid via CDN? A recomendação técnica é sim, porque o volume de 37.453 linhas precisa de ranking real, mas essa exceção deve ser explicitamente aprovada.

2. O conteúdo deve ser armazenado nos chunks como Markdown bruto ou texto com seções já segmentadas? A recomendação é Markdown bruto com metadados de seções, mas segmentar por seção pode melhorar módulos grandes como `trace-reading` e `rubric-design`.

3. O conversor Markdown deve ser parser próprio limitado ao subset do currículo ou biblioteca client-side madura? Parser próprio reduz dependência; biblioteca melhora fidelidade. A decisão depende do quanto o conteúdo usa tabelas, listas aninhadas e blocos especiais.

4. O sitemap deve listar apenas a landing canônica ou também hashes de módulos para documentação interna? Hash URLs são úteis para pessoas, mas têm valor limitado para crawlers. A decisão depende se SEO público ou compartilhamento interno é prioridade.

5. O MVP deve incluir busca full-text desde a primeira versão ou começar com busca por título/tag e entregar FlexSearch na segunda iteração? Para uso real do currículo inteiro, full-text é altamente recomendada; para reduzir risco, pode entrar após navegação e renderização estarem estáveis.

6. O conteúdo dos arquivos `rawfiles/` deve entrar no site ou permanecer fora do currículo interativo? O prompt permite usar conteúdo de `curriculum/`, `rawfiles/` e `web/`, mas o inventário funcional atual está centrado em `curriculum/`. Incluir `rawfiles/` pode aumentar escopo e confundir a experiência de estudo.

7. O controle de progresso é individual/local ou haverá futuramente progresso de equipe? A arquitetura MVP assume localStorage por navegador. Progresso de equipe exigiria backend ou integração externa e está fora das restrições atuais.

8. A página deve manter a estética compacta do portal atual ou adotar a linguagem editorial mais robusta de `mhc_visao_estrategica.html`? A recomendação é combinar: navegação e badges do portal KODA, com padrões editoriais de leitura, tabelas, timeline e scrollspy inspirados na visão estratégica.
