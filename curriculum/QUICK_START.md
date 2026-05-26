# 🚀 QUICK START: Seu Caminho para Long-Running Agents

**⏱️ Tempo Estimado:** 45 minutos (este guia + introdução)

Se você chegou aqui e quer começar **AGORA**, este é seu guia.

---

## 📍 Onde Você Está?

Escolha uma opção:

### 🆕 "Sou novo e nunca ouvi falar disso"
**→ Comece aqui (Seção: Comece com o Básico)**

### 📚 "Tenho experiência com LLMs"
**→ Vá para Nível 2 (Seção: Pule para Prático)**

### 🏗️ "Trabalho em arquitetura"
**→ Vá para Nível 3 (Seção: Vá Direto para Avançado)**

### 🎯 "Trabalho em KODA"
**→ Vá para Nível 4 (Seção: KODA-Específico)**

---

## ✅ Comece com o Básico (Nível 1: 3-4 horas)

### O Problema em 2 Minutos

Os agentes de IA podem fazer coisas incríveis, mas **perdem o foco** quando executam por horas:

1. **Não conseguem manter estado** → Esquecem contexto após 30 minutos
2. **Não sabem planejar** → Tentam fazer tudo de uma vez
3. **Não conseguem se avaliar** → Aprovam trabalho ruim como bom

**KODA enfrenta isso:** Quando um cliente conversa com KODA por 2+ horas descobrindo produtos e fazendo pedido, como o KODA mantém a coerência?

### Solução em 1 Parágrafo

Use **harnesses** (estruturas de suporte) que:
- Gerenciam contexto e memória
- Decompõem trabalho em etapas menores
- Separam "geração" de "avaliação" para melhor julgamento

**E é exatamente isso que aprenderemos.**

### Ler Primeiro (15 minutos)

Leia **nesta ordem**:

1. `01-nivel-1-fundamentals/01-why-agents-lose-plot.md`
   - Por que o problema existe
   - Como KODA é afetado

2. `01-nivel-1-fundamentals/02-token-budgeting.md`
   - Como gerenciar tokens/contexto
   - Conceito fundamental para tudo

3. `01-nivel-1-fundamentals/03-basic-harness-patterns.md`
   - Padrões básicos que funcionam
   - Exemplos práticos

### Fazer Exercícios (30 minutos)

Faça os 2 exercícios:
- `01-nivel-1-fundamentals/exercises/exercise-01.md`
- `01-nivel-1-fundamentals/exercises/exercise-02.md`

**Espere:** Esses são fáceis? São para consolidar conceitos, não para desafiar.

### Verificar Aprendizado (5 minutos)

Responda sim/não:

- [ ] Consigo explicar os 3 problemas em uma frase cada?
- [ ] Entendo o que é um context window?
- [ ] Posso descrever um padrão básico de harness?
- [ ] Fiz os 2 exercícios?
- [ ] Posso aplicar a Nível 1 ao KODA?

Se **sim em todas**, você está pronto para Nível 2!

---

## 🎯 Pule para Prático (Nível 2: 6-8 horas)

### Para Quem?

Você já:
- Entende LLMs e prompting
- Sabe o que é context window
- Trabalhou com múltiplos agentes antes

### O que Aprender (Nível 2)

4 padrões práticos que mudam o jogo:

| Padrão | Problema que Resolve | Tempo |
|--------|---------------------|-------|
| **Generator/Evaluator** | Agent não consegue se avaliar | 90 min |
| **Sprint Contracts** | Ambiguidade sobre "pronto" | 90 min |
| **Rubric Design** | Subjetividade em qualidade | 90 min |
| **Trace Reading** | Debugar agent behavior | 90 min |

### Sequência Recomendada

```
Dia 1:
├─ Generator/Evaluator (90 min)
├─ Sprint Contracts (90 min)

Dia 2:
├─ Rubric Design (90 min)
├─ Trace Reading (90 min)

Dia 3:
├─ 3 Exercícios práticos (120 min)
├─ Aplicação KODA (60 min)
```

### Onde Está Tudo?

```
02-nivel-2-practical-patterns/
├── 01-generator-evaluator-pattern.md ⭐ COMECE AQUI
├── 02-sprint-contracts.md
├── 03-rubric-design.md
├── 04-trace-reading.md
├── exercises/
│   ├── exercise-01.md (generator/evaluator)
│   ├── exercise-02.md (sprint contracts)
│   ├── exercise-03.md (rubric design)
│   └── solutions/ (respostas)
└── koda-applications/
    └── nivel-2-koda.md (como aplica ao KODA)
```

### Checkpoint de Aprendizado

Teste-se:

- [ ] Posso desenhar um pair generator/evaluator do zero?
- [ ] Consigo escrever um sprint contract com critérios?
- [ ] Posso criar uma rubric para um problema específico?
- [ ] Consigo ler um agent trace e encontrar divergências?
- [ ] Posso propor generator/evaluator para 1 feature KODA?

Se **sim**, você está pronto para Nível 3!

---

## 🏗️ Vá Direto para Avançado (Nível 3: 8-10 horas)

### Para Quem?

Você é um architect ou engenheiro sênior que:
- Já entende generator/evaluator
- Trabalha com sistemas complexos
- Precisa desenhar multi-agent systems

### O que Aprender (Nível 3)

Construir sistemas sofisticados:

| Tópico | Resultado |
|--------|-----------|
| **Multi-Agent Systems** | Design sistema com 3+ agentes coordenados |
| **State Persistence** | Manter estado através de horas |
| **File-Based Coordination** | Agentes conversam via arquivos |
| **Harness Evolution** | Remover scaffolding quando modelo melhora |

### Sequência Recomendada

```
Dia 1-2:
├─ Multi-Agent Systems (90 min)
├─ State Persistence (90 min)

Dia 3:
├─ File-Based Coordination (90 min)
├─ Server-Side Compaction (60 min)

Dia 4:
├─ Harness Evolution (90 min)
├─ 3 Exercícios (150 min)
```

### Onde Está Tudo?

```
03-nivel-3-advanced-architecture/
├── 01-multi-agent-systems.md ⭐ COMECE AQUI
├── 02-state-persistence.md
├── 03-file-based-coordination.md
├── 04-server-side-compaction.md
├── 05-harness-evolution.md
├── exercises/
│   ├── exercise-01.md (design 3-agent system)
│   ├── exercise-02.md (implement state persistence)
│   ├── exercise-03.md (harness evolution)
│   └── solutions/
└── koda-applications/
    └── nivel-3-koda.md
```

### Checkpoint de Aprendizado

- [ ] Posso desenhar arquitetura Planner/Generator/Evaluator?
- [ ] Entendo trade-offs de diferentes estratégias de estado?
- [ ] Posso desenhar sistema de coordenação baseado em arquivo?
- [ ] Consigo identificar quando remover componentes de harness?
- [ ] Posso proposar multi-agent design para KODA?

Se **sim**, você está pronto para Nível 4!

---

## 🎯 KODA-Específico (Nível 4: Contínuo)

### Para Quem?

Você trabalha em KODA ou vai usar padrões **aplicados em produção**.

### O que Aprender

```
04-nivel-4-koda-specific/
├── 01-koda-architecture.md
├── 02-customer-journey-flows.md
├── 03-feature-design-patterns.md
├── 04-evaluation-rubrics-koda.md
├── 05-harness-improvements.md
├── real-world-exercises/
│   ├── exercise-01.md
│   ├── exercise-02.md
│   └── solutions/
└── case-studies/
    ├── case-study-01.md
    ├── case-study-02.md
    └── case-study-03.md
```

### Próximos Passos

1. Leia arquitetura atual do KODA
2. Identifique 1-2 features para refatorar
3. Desenhe generator/evaluator para elas
4. Implemente e meça resultado
5. Documente aprendizados

---

## 📚 Recursos por Caso de Uso

### "Quero entender KODA"
1. Leia `04-nivel-4-koda-specific/01-koda-architecture.md`
2. Leia case studies em `09-case-studies/koda-*.md`
3. Faça real-world exercises em `04-nivel-4-koda-specific/real-world-exercises/`

### "Quero desenhar um feature novo"
1. Leia `04-nivel-4-koda-specific/03-feature-design-patterns.md`
2. Estude `09-case-studies/`
3. Use templates em `08-tools-templates/sprint-contract-template.md`

### "Tenho um problema e preciso de solução"
1. Vá para `GLOSSARY.md` e procure o termo relacionado
2. Vá para `FAQ.md` e veja se está lá
3. Procure nos `09-case-studies/`

### "Quero visualizar conceitos"
1. Acesse `06-knowledge-graphs/`
2. Veja Knowledge Graphs dos conceitos relacionados

---

## 🎓 Checklists Rápidos

### Meu Primeiro Dia

- [ ] Abri este arquivo (você está aqui!)
- [ ] Li MASTER_PLAN.md
- [ ] Escolhi meu caminho (Nível 1/2/3/4)
- [ ] Li a introdução do meu nível
- [ ] Marquei calendário para estudar

**Tempo:** 30 minutos

### Minha Primeira Semana

- [ ] Completei leitura principal de meu nível
- [ ] Fiz todos os exercícios
- [ ] Respondi afirmativamente aos checkpoints
- [ ] Compartilhei uma coisa que aprendi com alguém
- [ ] Preparei perguntas para revisão

**Tempo:** 4-10 horas

### Meu Primeiro Mês

- [ ] Completei meu nível e passei para o próximo
- [ ] Apliquei 1 padrão em código real
- [ ] Documentei meu aprendizado
- [ ] Mentarei someone em meu nível anterior
- [ ] Propus 1 melhoria para KODA

**Tempo:** Contínuo

---

## ❓ Perguntas Frequentes Rápidas

### P: Por onde começo?
**R:** Responda: Sou novo em tudo? → Nível 1. Conheço LLMs? → Nível 2. Sou architect? → Nível 3. Trabalho em KODA? → Nível 4.

### P: Quanto tempo leva?
**R:** Nível 1 (4h), Nível 2 (8h), Nível 3 (10h), Nível 4 (contínuo). Total: 30+ horas ao longo de 12 semanas.

### P: Posso pular níveis?
**R:** Se você domina Nível N-1, sim. Use checkpoints para testar.

### P: E se não entender?
**R:** Normal! Volte para leitura anterior, releia, faça exercícios novamente, pergunte. Ver `FAQ.md`.

### P: Isso é para KODA?
**R:** Sim e não. Padrões são genéricos (Nível 1-3), aplicação é KODA (Nível 4).

---

## 🔗 Próximas Leituras

Após QUICK_START:

**Para Nível 1:**
→ Abra `01-nivel-1-fundamentals/01-why-agents-lose-plot.md`

**Para Nível 2:**
→ Abra `02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md`

**Para Nível 3:**
→ Abra `03-nivel-3-advanced-architecture/01-multi-agent-systems.md`

**Para Nível 4:**
→ Abra `04-nivel-4-koda-specific/01-koda-architecture.md`

---

## 💡 Dicas de Ouro

1. **Não aprenda tudo de uma vez.** Leia um tópico, faça exercícios, durma, volte.

2. **Leia as traces!** Melhor forma de aprender é ver um agent real em ação.

3. **Compartilhe aprendizado.** Ensinar é a melhor forma de consolidar.

4. **Volte frequentemente.** Cada nível ilumina o anterior com nova compreensão.

5. **KODA é seu laboratório.** Use padrões em KODA para entendimento real.

---

## 🎯 Seu Checklist Agora

- [ ] Entendi que escolho meu caminho por nível
- [ ] Identifiquei meu nível inicial
- [ ] Marquei tempo no calendário para começar
- [ ] Abri o arquivo recomendado do meu nível
- [ ] Salvei este arquivo para referência rápida

**Se marcou todas?** 

### Você está pronto! 🚀

Abra seu arquivo de início e comece. A equipe está aqui se precisar.

---

*Quick Start | 45 minutos para começar | v1.0*
