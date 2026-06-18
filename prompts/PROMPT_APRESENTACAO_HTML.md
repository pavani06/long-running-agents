---
title: "Prompt: Criar Apresentação Web Interativa — Curso de Agentes de Longa Duração"
type: prompt
date: 2026-05-26
tags:
  - stack-tooling
  - curriculo-conteudo
aliases:
  - apresentacao html prompt
  - web presentation
  - pagina interativa
relates-to:
  - "[[prompts/PROMPTS-00-INDEX|Prompt Index]]"
  - "[[web/koda_course_portal.html|KODA Course Portal]]"
---

# 🎯 PROMPT: Criar Apresentação Web Interativa - Curso de Agentes de Longa Duração

## Como Usar Este Prompt

Cole este prompt **completo** em um LLM (Claude, GPT-4, etc) para gerar um conjunto de páginas HTML profissionais para apresentar seu projeto ao time, segmentado em aulas.

---

## PROMPT COMPLETO (Cole Tudo Isto)

```
Você é um especialista em design web educacional, apresentações técnicas e experiência do usuário. Sua tarefa é criar um conjunto profissional e visualmente atrativo de **páginas HTML** para apresentar um curso sobre **Agentes que Rodam por Longas Durações** (Long-Running Agents), focado na plataforma KODA.

**CONTEXTO DO PROJETO:**
- Nome: "Construindo Agentes Inteligentes para Conversas Longas"
- Público: Time técnico (engenheiros, product managers, líderes)
- Caso de Uso: KODA (agente conversacional para vendas de suplementos via WhatsApp)
- Temas Centrais: Context Management, Generator/Evaluator Patterns, Sprint Contracts, State Persistence, Multi-Agent Systems
- Linguagem: Português (interface) + Code examples em English
- Tons: Profissional + Inspirador + Prático

**ESTRUTURA DO CURSO (4 NÍVEIS):**

Nível 1: FUNDAMENTALS
├─ Por que agentes perdem o contexto ("Three Reasons Agents Lose the Plot")
├─ Token Budgeting e Gerenciamento de Contexto
├─ Padrões básicos de Harness
└─ Aplicações KODA no Nível 1

Nível 2: PRACTICAL PATTERNS
├─ Generator/Evaluator Pattern (Gerador vs Avaliador)
├─ Sprint Contracts (Contratos de Execução)
├─ Design de Rubrics (Critérios de Avaliação)
├─ Trace Reading (Leitura de Rastreamentos)
└─ Aplicações KODA no Nível 2

Nível 3: ADVANCED ARCHITECTURE
├─ Multi-Agent Systems (Sistemas Multi-Agentes)
├─ State Persistence (Persistência de Estado)
├─ File-Based Coordination (Coordenação via Arquivos)
├─ Server-Side Compaction (Compressão de Lado do Servidor)
├─ Harness Evolution (Evolução da Arquitetura)
└─ Aplicações KODA no Nível 3

Nível 4: KODA-SPECIFIC MASTERY
├─ KODA Architecture Deep Dive
├─ Customer Journey Flows (Fluxos de Jornada do Cliente)
├─ Feature Design Patterns (Padrões de Design de Features)
├─ Evaluation Rubrics KODA (Rubrics Específicas para KODA)
├─ Harness Improvements (Melhorias na Arquitetura)
└─ Production Deployment

---

**REQUIREMENTS - ESTRUTURA HTML:**

1. **Home Page / Landing (index.html)**
   - Hero Section com título inspirador
   - Visão geral dos 4 níveis com cards visuais
   - CTA (Call-to-Action): "Começar com Nível 1"
   - Mostrar progresso visual: Nível 1 → 2 → 3 → 4
   - Footer com info do time/projeto

2. **Para Cada Nível (nivel-1.html, nivel-2.html, nivel-3.html, nivel-4.html)**
   
   **Header:**
   - Logo/Title do projeto
   - Breadcrumb navigation (Home > Nível X > Aula Y)
   - Indicador visual de progresso (qual nível está vendo)
   
   **Main Content:**
   - Seção de Overview (5-10 linhas explicando o nível)
   - **Accordion/Tabs com 4 aulas por nível:**
     
     Aula 1: [Conceito A]
     - Descrição (2-3 parágrafos)
     - Diagrama ou ilustração ASCII (se aplicável)
     - "Por que importa" - conexão com KODA
     - Key Takeaways (3-4 pontos de bala)
     - CTA: "Ver Exercício"
     
     Aula 2: [Conceito B]
     - (Mesma estrutura)
     
     Aula 3: [Conceito C]
     - (Mesma estrutura)
     
     Aula 4: [Aplicação Prática KODA]
     - Exemplo real de como este nível se aplica ao KODA
     - Fluxograma/diagrama de fluxo
     - Métricas de impacto
   
   **Right Sidebar (opcional mas recomendado):**
   - Estimated Time (Tempo estimado por aula)
   - Difficulty Indicator (Indicador de dificuldade)
   - Resources (Links para exercícios, PDFs, repos)
   - Next Lesson CTA
   
   **Footer:**
   - Navigation between levels
   - "Voltar ao Home"
   - "Próximo Nível"

3. **Exercícios / Labs (exercises.html)**
   - Lista de todos os exercícios (12 total: 2+3+3+2 por nível)
   - Link para cada exercício
   - Dificuldade, tempo estimado, topics cobertos
   
4. **Knowledge Graphs (graphs.html)**
   - Galeria visual com 35+ diagramas Mermaid
   - Filtros por: Nível, Conceito, Tipo (System, Flow, etc)
   - Visualização interativa (zoom, busca)

5. **Case Studies (case-studies.html)**
   - 5 casos de estudo (2 genéricos + 3 KODA)
   - Cards com: Título, Descrição, Dificuldade, Key Learnings
   - Clique para expandir detalhes

---

**REQUIREMENTS - DESIGN & UX:**

**Visual Design:**
- Paleta de cores profissional (azul + branco + acentos em laranja/verde)
- Typography: Headlines em fonte sans-serif moderna, body em Segoe UI ou similar
- Espaçamento: Generoso (16px mínimo entre seções)
- Ícones: Usar Font Awesome ou Tabler Icons (SVG inline)
- Sem bordes pesados: Cards com subtle shadows
- Mobile-responsive (funciona bem em celular e desktop)

**Componentes Reutilizáveis:**
- Card (title + description + icon + link)
- Badge (para dificuldade, tempo, status)
- Progress Bar (visual do progresso no curso)
- Accordion (expandir/recolher aulas)
- Button (CTA com ícone opcional)
- Breadcrumb Navigation
- Level Indicator (visual mostrando qual nível está)

**Interatividade:**
- Hover effects em cards (sutil, não piscante)
- Smooth transitions (300ms)
- Scroll-to-section animations
- Ícones que mudam ao expandir/recolher
- Indicadores de leitura (progress bar no topo da página)

---

**REQUIREMENTS - CONTEÚDO:**

**Para cada Aula, gere:**

Nível 1:
├─ Aula 1: "Por Que Agentes Perdem o Contexto" (3 razões específicas)
├─ Aula 2: "Token Budgeting: A Moeda do Contexto"
├─ Aula 3: "Padrões Básicos de Harness"
└─ Aula 4: "Fundamentos no KODA: Primeiros Passos"

Nível 2:
├─ Aula 1: "Generator/Evaluator: Separando Ideias de Avaliação"
├─ Aula 2: "Sprint Contracts: Contratos Testáveis"
├─ Aula 3: "Rubric Design: Critérios Claros para Avaliação"
├─ Aula 4: "Aplicando Padrões Práticos no KODA"

Nível 3:
├─ Aula 1: "Multi-Agent Systems: Orquestrando Agentes"
├─ Aula 2: "State Persistence: Preservando Conhecimento"
├─ Aula 3: "Coordenação via Arquivos: Low-Tech, Alta-Eficácia"
├─ Aula 4: "Escalando KODA com Arquitetura Avançada"

Nível 4:
├─ Aula 1: "KODA Deep Dive: Arquitetura em Produção"
├─ Aula 2: "Customer Journey: Do Catálogo à Entrega"
├─ Aula 3: "Feature Design & Deployment Patterns"
└─ Aula 4: "Mastery: KODA em Produção com Impacto"

**Cada Aula deve incluir:**
1. Uma descrição clara (150-200 palavras)
2. Uma analogia ou metáfora (facilita entendimento)
3. Um diagrama ASCII simples ou sugestão de visual
4. Conexão com KODA (como isso se aplica)
5. 3-4 Key Takeaways (bala points)
6. Um CTA (exercício, próxima aula, etc)

---

**REQUIREMENTS - NAVEGAÇÃO:**

**Menu Principal (Header):**
- Home
- Níveis (dropdown mostrando 1, 2, 3, 4)
- Exercícios
- Knowledge Graphs
- Case Studies
- Contato/Info

**Navegação entre Aulas:**
- Botão "Aula Anterior" | Botão "Próxima Aula"
- Breadcrumb mostrando: Home > Nível X > Aula Y
- Quick Jump: Dropdown mostrando todas as aulas do nível

**Visual de Progresso:**
- Barra de progresso no topo (quantas aulas completou)
- Indicador visual do nível atual (Nível 1 ▓▓▓░░░░░░)

---

**REQUIREMENTS - INSPIRAÇÃO & TONE:**

O tone deve refletir:
✅ Confiança técnica (sabemos do que estamos falando)
✅ Acessibilidade (explain it simply, not dumbed down)
✅ Motivação (você pode fazer isto!)
✅ Pragmatismo (examples reais, não teórico)
✅ Comunidade (estamos aprendendo juntos)

**Exemplos de Headlines:**
- "Por Que Seus Agentes Esquecem o Contexto (E Como Evitar)"
- "O Padrão Generator/Evaluator: Separando Pensamento de Ação"
- "Mantendo o Estado: Como Agentes Lembram Conversas Longas"
- "KODA em Produção: De Conversa a Entrega"

---

**TECHNICAL REQUIREMENTS:**

**Stack:**
- HTML5 (semântico)
- CSS3 (modern, sem frameworks se possível, ou use Tailwind se gerar)
- Vanilla JavaScript (interatividade, sem jQuery)
- Pode usar Font Awesome para ícones (link CDN)

**Performance:**
- Minify CSS/JS no final
- Lazy-load images
- Arquivo único de CSS (ou bem poucos)
- Arquivo único de JS (ou bem poucos)

**Accessibility:**
- ARIA labels onde apropriado
- Semantic HTML
- Color contrast 4.5:1 mínimo
- Keyboard navigation funcional

**SEO Basics:**
- Meta tags (title, description, viewport)
- Heading hierarchy (h1, h2, h3)
- Alt text em images/diagrams

---

**OUTPUT ESPERADO:**

Gere os seguintes arquivos HTML (copiáveis, prontos para usar):

1. **index.html** - Home page com overview dos 4 níveis
2. **nivel-1.html** - Nível 1 com 4 aulas
3. **nivel-2.html** - Nível 2 com 4 aulas
4. **nivel-3.html** - Nível 3 com 4 aulas
5. **nivel-4.html** - Nível 4 com 4 aulas
6. **exercises.html** - Lista de todos os 12 exercícios
7. **knowledge-graphs.html** - Galeria de diagramas
8. **case-studies.html** - 5 casos de estudo
9. **styles.css** - Estilos centralizados (reutilizáveis)
10. **script.js** - Interatividade (accordions, navegação, etc)

---

**INSTRUÇÕES FINAIS:**

1. **Comece pelo index.html** - crie a home page inspiradora
2. **Template as aulas** - crie um padrão reutilizável para cada nível
3. **Gere conteúdo inspirador** - use exemplos reais, tons motivacionais
4. **Inclua números/métricas** - "Complete 4 aulas em ~2 horas", etc
5. **Design responsivo** - mobile-first, depois ampliar
6. **Testes de navegação** - todos os links funcionam?
7. **Copiar/Colar Pronto** - usuário deve poder salvar arquivo e abrir direto no browser

---

**BONUS FEATURES (se houver tempo/tokens):**

- Modo escuro (dark mode toggle)
- Print-friendly CSS
- PDF download de cada nível
- Bookmark/Save aulas
- Quiz interativo ao final de cada aula
- Comments/Feedback form

---

**Agora, gere TODOS os arquivos HTML acima. Comece com index.html e styles.css, depois os 4 níveis, depois as páginas de suporte. Cada arquivo deve ser completo, copiável, e funcionante.**
```

---

## 📋 Como Usar Este Prompt

### **Passo 1: Preparação**
1. Abra seu LLM favorito (Claude, GPT-4, Gemini, etc)
2. Abra este arquivo (`PROMPT_APRESENTACAO_HTML.md`)
3. Copie TUDO o que está entre os três ` ``` ` (marca de código)

### **Passo 2: Cole e Execute**
1. Cole no seu LLM
2. Deixe processar (tipicamente 10-30 minutos)
3. Monitore o progresso

### **Passo 3: Salve os Outputs**
1. Copie cada arquivo HTML gerado
2. Salve com nome exato (index.html, nivel-1.html, etc)
3. Salve também styles.css e script.js na mesma pasta

### **Passo 4: Abra no Browser**
1. Coloque todos os arquivos (`.html`, `.css`, `.js`) na mesma pasta
2. Abra `index.html` em seu navegador
3. Teste a navegação, responsividade, interatividade

---

## 🎨 Personalizações Opcionais

Se quiser customizar ainda mais o prompt antes de colar, você pode:

### **Aumentar/Diminuir Complexidade**
- **Mais simples:** Remova "BONUS FEATURES" e "Accessibility"
- **Mais avançado:** Adicione "Adicione um mini-quiz ao final de cada aula" ou "Crie um sistema de badges/achievements"

### **Mudar Paleta de Cores**
Adicione à seção "Visual Design":
```
Paleta de Cores Específica:
- Primary: #0066CC (azul)
- Secondary: #FF6B35 (laranja)
- Background: #F8F9FA (cinza claro)
- Text: #1F2937 (cinza escuro)
- Success: #10B981 (verde)
- Warning: #F59E0B (âmbar)
```

### **Adicionar Seu Logo**
Adicione à seção "Technical Requirements":
```
Logo/Branding:
- Adicione logo da FutanBear em todas as pages (header)
- Favico (pequeno ícone no abr)
- Colores devem refletir brand guidelines
```

### **Modificar Estrutura de Aulas**
Se seus 4 níveis têm uma estrutura diferente, edite a seção "ESTRUTURA DO CURSO" antes de colar.

---

## ✅ Checklist Antes de Colar

- [ ] Você tem acesso a um LLM (Claude, GPT-4, etc)
- [ ] Tem 30+ minutos disponíveis
- [ ] Sabe onde vai salvar os arquivos HTML
- [ ] Tem um editor de texto básico (VS Code, Notepad++, etc)
- [ ] Sabe como abrir arquivos HTML no navegador

---

## 📞 Troubleshooting

| Problema | Solução |
|----------|---------|
| LLM parou no meio | Peça para continuar: "Continue gerando do ponto onde parou" |
| HTML não abre | Verifique se todos os arquivos (.html, .css, .js) estão na mesma pasta |
| Estilos não aparecem | Verifique se o caminho para `styles.css` está correto (deve ser `<link rel="stylesheet" href="styles.css">`) |
| Links não funcionam | Use caminhos relativos: `<a href="nivel-1.html">` não `<a href="/nivel-1.html">` |
| Responsividade quebrada | Verifique se o `<meta name="viewport">` está em cada HTML |

---

## 🚀 Próximos Passos

Depois que os HTMLs forem gerados:

1. **Hospede online** (GitHub Pages, Vercel, Netlify - todos gratuitos)
2. **Compartilhe link** com seu time via Slack/Email
3. **Colete feedback** - adicione uma seção de comentários
4. **Iterate** - refine baseado em feedback do time
5. **Integre com outros recursos** - links para exercícios, PDFs, repos

---

## 💡 Dicas Extras

✅ **Se quiser versão mais visual:** Peça ao LLM para incluir diagramas SVG inline em vez de ASCII
✅ **Se quiser versão mais leve:** Remova a seção de Knowledge Graphs e Case Studies (crie pages separadas depois)
✅ **Se quiser versão interativa avançada:** Peça para incluir localStorage para "salvar progresso do usuário"
✅ **Se quiser em Inglês:** Mude "Linguagem: Português" para "Linguagem: English"

---

*Prompt de Apresentação HTML | v1.0 | Pronto para usar!*

**Está pronto? Cole o prompt acima em seu LLM e comece! 🚀**
