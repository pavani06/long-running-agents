---
title: "Índice Completo de Prompts"
type: prompt
date: 2026-05-26
tags:
  - index
  - curriculo-conteudo
  - stack-tooling
aliases:
  - indice de prompts
  - prompt index
  - todos os prompts
relates-to:
  - "[[prompts/PROMPTS-01-curso-completo|Curso Completo]]"
  - "[[prompts/PROMPTS-02-knowledge-graphs|Knowledge Graphs]]"
  - "[[prompts/PROMPTS-03-exercises|Exercises]]"
  - "[[prompts/PROMPTS-04-case-studies|Case Studies]]"
  - "[[prompts/PROMPT-05-analise-web-interativa|Analise Web Interativa]]"
  - "[[prompts/PROMPTS-06-analise-comparativa-koda-ecommerce|Analise KODA Ecommerce]]"
  - "[[prompts/PROMPTS-07-obsidian-adaptation|Obsidian Adaptation]]"
  - "[[prompts/PROMPTS-08-obsidian-governance|Obsidian Governance]]"
  - "[[prompts/PROMPT_APRESENTACAO_HTML|Apresentacao HTML]]"
  - "[[curriculum/README|Curriculum README]]"
---

# 📝 ÍNDICE COMPLETO DE PROMPTS

**Todos os prompts necessários para gerar o currículo completo**

---

## 📋 Sumário dos Prompts

| # | Nome | Arquivo | Tempo | Outputs |
|---|------|---------|-------|---------|
| 1 | Curso Completo | `PROMPTS-01-curso-completo.md` | 1-2h | 4 níveis completos |
| 2 | Knowledge Graphs | `PROMPTS-02-knowledge-graphs.md` | 1h | 35+ diagramas |
| 3 | Exercícios | `PROMPTS-03-exercises.md` | 2h | 12 exercícios + soluções |
| 4 | Casos de Estudo | `PROMPTS-04-case-studies.md` | 1.5h | 5 casos detalhados |

**Tempo Total para Gerar Tudo:** 5.5-6.5 horas com LLM

---

## 🎯 Como Usar (Passo a Passo)

### **Opção A: Usar Todos os Prompts (Recomendado)**

**Dia 1 - Estrutura Base:**
1. Você já tem os 7 documentos mestres ✅
2. Prepare-se para começar a gerar conteúdo

**Dia 2 - Conteúdo Curricular:**
```bash
# Terminal / Chat com LLM

# Passo 1: Cole PROMPTS-01-curso-completo.md
"Cole o prompt COMPLETO do arquivo PROMPTS-01-curso-completo.md"
→ Tempo: 1-2 horas
→ Output: Todos os 4 níveis do currículo

# Passo 2: Cole PROMPTS-02-knowledge-graphs.md
"Cole o prompt COMPLETO do arquivo PROMPTS-02-knowledge-graphs.md"
→ Tempo: 1 hora
→ Output: 35+ diagramas Mermaid

# Passo 3: Cole PROMPTS-03-exercises.md
"Cole o prompt COMPLETO do arquivo PROMPTS-03-exercises.md"
→ Tempo: 2 horas
→ Output: 12 exercícios com soluções

# Passo 4: Cole PROMPTS-04-case-studies.md
"Cole o prompt COMPLETO do arquivo PROMPTS-04-case-studies.md"
→ Tempo: 1.5 horas
→ Output: 5 casos de estudo
```

**Dia 3 - Organizar e Publicar:**
1. Mova outputs para pastas corretas
2. Configure em GitHub/Notion/MkDocs
3. Compartilhe com equipe

---

### **Opção B: Usar Sequencialmente (Se LLM tem limite de contexto)**

Se seu LLM tem limite de contexto (ex: não consegue processar 1000+ linhas de prompt):

**Semana 1:**
```
SEG: PROMPTS-01 Parte 1 (Nível 1)
TER: PROMPTS-01 Parte 2 (Nível 2)
QUA: PROMPTS-01 Parte 3 (Nível 3)
QUI: PROMPTS-01 Parte 4 (Nível 4)
```

**Semana 2:**
```
SEG: PROMPTS-02 Parte 1 (Conceitos 1-3)
TER: PROMPTS-02 Parte 2 (Conceitos 4-8)
QUA: PROMPTS-02 Parte 3 (Mega-graphs)
QUI: PROMPTS-02 Parte 4 (Especializados)
```

**Semana 3:**
```
SEG: PROMPTS-03 Nível 1
TER: PROMPTS-03 Nível 2
QUA: PROMPTS-03 Nível 3
QUI: PROMPTS-03 Nível 4
```

**Semana 4:**
```
SEG-TER: PROMPTS-04 Casos genéricos
QUA-QUI: PROMPTS-04 Casos KODA
```

---

### **Opção C: Priorizado (Se Tempo é Limitado)**

Se você tem pouco tempo, faça APENAS:

**Essencial (3 horas):**
1. PROMPTS-01 (Conteúdo dos 4 níveis)
2. PROMPTS-03 (Exercícios)

**Importante (adicional 2 horas):**
3. PROMPTS-02 (Knowledge Graphs)

**Bônus (adicional 1.5 horas):**
4. PROMPTS-04 (Case Studies)

---

## 📄 Descrição Detalhada de Cada Prompt

### **PROMPTS-01: Curso Completo**

**O que gera:**
- ✅ Estrutura dos 4 níveis completa
- ✅ Conteúdo de cada nível (Nível 1-4)
- ✅ Conceitos core (Context Management, Generator/Evaluator, etc)
- ✅ Deep dives para cada padrão
- ✅ Exemplos práticos de KODA
- ✅ Guias de implementação

**Arquivos a salvar:**
```
01-nivel-1-fundamentals/
├── 01-why-agents-lose-plot.md
├── 02-token-budgeting.md
├── 03-basic-harness-patterns.md
└── koda-applications/nivel-1-koda.md

02-nivel-2-practical-patterns/
├── 01-generator-evaluator-pattern.md
├── 02-sprint-contracts.md
├── 03-rubric-design.md
├── 04-trace-reading.md
└── koda-applications/nivel-2-koda.md

03-nivel-3-advanced-architecture/
├── 01-multi-agent-systems.md
├── 02-state-persistence.md
├── 03-file-based-coordination.md
├── 04-server-side-compaction.md
├── 05-harness-evolution.md
└── koda-applications/nivel-3-koda.md

04-nivel-4-koda-specific/
├── 01-koda-architecture.md
├── 02-customer-journey-flows.md
├── 03-feature-design-patterns.md
├── 04-evaluation-rubrics-koda.md
└── 05-harness-improvements.md
```

**Tempo:** 1-2 horas
**Tamanho esperado:** ~12,000 linhas
**Complexidade:** Alta (precisa entender todas as nuances)

---

### **PROMPTS-02: Knowledge Graphs**

**O que gera:**
- ✅ 3 diagramas para cada 1 dos 8 conceitos core
- ✅ 3 mega-graphs (ecosystem, features, progression)
- ✅ Problem-solution graphs
- ✅ Generator/Evaluator patterns detalhados
- ✅ Harness evolution timeline
- ✅ Multi-agent coordination visual

**Total:** 35+ diagramas Mermaid

**Arquivos a salvar:**
```
06-knowledge-graphs/
├── 01-core-concepts/
│   ├── 01-context-management.md
│   ├── 02-planning-execution.md
│   ├── 03-generator-evaluator.md
│   ├── 04-sprint-contracts.md
│   ├── 05-state-persistence.md
│   ├── 06-harness-evolution.md
│   ├── 07-multi-agent.md
│   └── 08-evaluation-rubrics.md
│
├── 02-mega-graphs/
│   ├── ecosystem.md
│   ├── koda-features.md
│   └── learning-progression.md
│
├── 03-problem-solutions/
│   └── three-reasons-agents-lose-plot.md
│
├── 04-patterns/
│   ├── generator-evaluator-detailed.md
│   ├── harness-evolution.md
│   └── multi-agent-coordination.md
│
└── 05-complete-systems/
    └── koda-complete-architecture.md
```

**Tempo:** 1 hora
**Tamanho esperado:** ~5,000 linhas (código Mermaid)
**Complexidade:** Média (visual, mas requer pensamento estrutural)

---

### **PROMPTS-03: Exercícios**

**O que gera:**
- ✅ 2 exercícios Nível 1 (1 hora)
- ✅ 3 exercícios Nível 2 (3 horas)
- ✅ 3 exercícios Nível 3 (4 horas)
- ✅ 2 exercícios Nível 4 (4 horas)
- ✅ Soluções completas para todos

**Total:** 12 exercícios com soluções

**Arquivos a salvar:**
```
01-nivel-1-fundamentals/exercises/
├── exercise-01.md
├── exercise-02.md
└── solutions/
    ├── exercise-01-solution.md
    └── exercise-02-solution.md

02-nivel-2-practical-patterns/exercises/
├── exercise-01.md
├── exercise-02.md
├── exercise-03.md
└── solutions/
    ├── exercise-01-solution.md
    ├── exercise-02-solution.md
    └── exercise-03-solution.md

[E assim para Nível 3-4...]
```

**Tempo:** 2 horas
**Tamanho esperado:** ~3,000 linhas
**Complexidade:** Média-Alta (requer criatividade pedagógica)

---

### **PROMPTS-04: Casos de Estudo**

**O que gera:**
- ✅ Retro Game Maker (genérico, Nível 2-3)
- ✅ Browser DAW (genérico, Nível 3-4)
- ✅ KODA Product Discovery (KODA-específico)
- ✅ KODA Order Processing (KODA-específico)
- ✅ KODA Fulfillment (KODA-específico)

**Total:** 5 casos de estudo detalhados

**Arquivos a salvar:**
```
09-case-studies/
├── retro-game-maker.md
├── browser-daw-app.md
├── koda-product-discovery.md
├── koda-order-processing.md
└── koda-fulfillment-workflow.md
```

**Tempo:** 1.5 horas
**Tamanho esperado:** ~4,000 linhas
**Complexidade:** Média (requer entender padrões em contexto real)

---

## 🔄 Fluxo Recomendado

### **Semana 1: Preparação**
- [x] Baixar 7 documentos mestres
- [x] Copiar para repositório
- [x] Estrutura de pastas criada
- [x] Baixar 4 prompts

### **Semana 2: Conteúdo**
- [ ] Executar PROMPTS-01 (1-2h)
- [ ] Executar PROMPTS-02 (1h)
- [ ] Organizar outputs nas pastas
- [ ] Testar links

### **Semana 3: Exercícios e Casos**
- [ ] Executar PROMPTS-03 (2h)
- [ ] Executar PROMPTS-04 (1.5h)
- [ ] Finalizar documentação
- [ ] Review de qualidade

### **Semana 4: Publicação**
- [ ] Configurar em GitHub/Notion/MkDocs
- [ ] Testes finais
- [ ] Compartilhar com equipe
- [ ] Kickoff do programa

---

## 💡 Dicas para Usar os Prompts

### **1. Antes de Colar o Prompt**
- [ ] Certifique-se que o LLM tem contexto suficiente
- [ ] Prepare pasta onde vai salvar output
- [ ] Tenha arquivo de referência à mão (pdf da Anthropic)
- [ ] Bloqueie ~2 horas de tempo ininterrupto

### **2. Ao Colar o Prompt**
- [ ] Cole o prompt INTEIRO (não parta em pedaços)
- [ ] Deixe o LLM pensar (não apresse)
- [ ] Monitore outputs
- [ ] Salve tudo em arquivo .md

### **3. Depois de Gerar**
- [ ] Revise a qualidade
- [ ] Corrija erros óbvios
- [ ] Organize em pastas
- [ ] Teste links cruzados
- [ ] Valide formatação

### **4. Se Encontrar Problemas**
- **Prompt truncado?** → Cole novamente
- **Qualidade baixa?** → Refine prompt com feedback
- **Incompleto?** → Peça ao LLM continuar
- **Erros técnicos?** → Corrija manualmente

---

## 📊 Resumo de Geração

| Prompt | Outputs | Tempo | Status |
|--------|---------|-------|--------|
| PROMPTS-01 | 4 níveis | 1-2h | ⏳ TBD |
| PROMPTS-02 | 35+ diagramas | 1h | ⏳ TBD |
| PROMPTS-03 | 12 exercícios | 2h | ⏳ TBD |
| PROMPTS-04 | 5 case studies | 1.5h | ⏳ TBD |
| **TOTAL** | **~35k linhas** | **5.5-6.5h** | ⏳ TBD |

---

## 🚀 Próximos Passos Exatos

### **Agora (Próximos 30 minutos):**
1. Abra seu LLM favorito (Claude, GPT-4, etc)
2. Abra `PROMPTS-01-curso-completo.md`
3. **Cole TUDO o que está entre os ``` markers```
4. Espere resposta (10-30 minutos)

### **Depois:**
1. Salve resposta em arquivo .md
2. Organize em pastas `01-nivel-1-fundamentals/`, etc
3. Repita para PROMPTS-02, PROMPTS-03, PROMPTS-04

### **Resultado Final:**
✅ Currículo completo de 35,000+ linhas  
✅ 4 níveis totalmente documentados  
✅ 12 exercícios com soluções  
✅ 35+ diagramas Mermaid  
✅ 5 casos de estudo  
✅ Pronto para compartilhar com equipe!

---

## ✅ Checklist Final

- [ ] Todos os 4 prompts salvos em .md
- [ ] Repositório criado e estrutura de pastas pronta
- [ ] LLM escolhido (Claude, GPT-4, etc)
- [ ] 5.5-6.5 horas bloqueadas no calendário
- [ ] PDF da Anthropic à mão para referência
- [ ] Pasta de outputs pronta para salvar arquivos

**Quando tudo isto estiver feito:**
→ Cole `PROMPTS-01-curso-completo.md` em seu LLM e comece! 🚀

---

## 📞 Perguntas Frequentes sobre Prompts

**P: Qual LLM devo usar?**
R: Claude (melhor para código), GPT-4 (rápido), ou Gemini (bom custo). Recomendamos Claude para melhor qualidade.

**P: Preciso executar os 4 prompts?**
R: Para programa completo, sim. Mas se tiver tempo limitado, execute no mínimo PROMPTS-01 e PROMPTS-03.

**P: Posso modificar os prompts?**
R: Sim! Os prompts são templates. Customizar para seu contexto específico pode melhorar resultados.

**P: Quanto vai custar?**
R: Com Claude API: ~$5-10 para gerar tudo. Com GPT-4: ~$10-20. Vale muito a pena pelos 35,000+ linhas geradas.

**P: E se o LLM parar no meio?**
R: Peça ao LLM continuar. Exemplo: "Continue gerando o resto dos exercícios do Nível 2"

**P: Como garanto qualidade dos outputs?**
R: Revise outputs, corrija erros óbvios, teste links. Refine prompt se qualidade for baixa.

---

## 🎓 Estrutura Final (Depois de Gerar Tudo)

```
koda-long-running-agents/
├── 📄 Documentos Mestres (7 arquivos)
├── 📚 4 Níveis Completos (17 arquivos de conteúdo)
├── 🧠 8 Conceitos Core (8 arquivos)
├── 📊 Knowledge Graphs (15+ arquivos)
├── 🛠️ Implementação (12 arquivos)
├── 📖 Casos de Estudo (5 arquivos)
├── 💻 Exercícios (12 arquivos + 12 soluções)
└── 📚 Referências (3 arquivos)

TOTAL: ~100+ arquivos, ~35,000 linhas
```

---

*Índice de Prompts | Complete Generation Guide | v1.0*

**Pronto para começar? Abra o primeiro prompt e cole no seu LLM! 🚀**
