---
title: "Padrão Sprint Contracts: Acordos Negociados Entre Agentes"
type: curriculum-lesson
nivel: 2
aliases: ["contratos sprint", "sprint contracts", "contratos agente", "definição de pronto"]
tags: [curriculo-conteudo, nivel-2, padroes-praticos, contratos-entre-agentes, negociacao-de-escopo, definicao-de-pronto, criterios-de-sucesso, tratamento-de-falhas, conversas-longas, alinhamento-de-expectativas, loops-de-retry]
relates-to: ["[[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]", "[[curriculum/05-core-concepts/04-sprint-contracts|Sprint Contracts Concept]]"]
last_updated: 2026-06-10
---
# 📋 Padrão Sprint Contracts: Acordos Negociados Entre Agentes
## Como Definir Expectativas Claras Antes de Começar

**Tempo Estimado:** 90 minutos  
**Nível:** 2 - Padrões Práticos  
**Pré-requisito:** Ter completado Nível 1 + `01-generator-evaluator-pattern.md`  
**Status:** 🟢 PADRÃO QUE EVITA 40% DOS ERROS EM LONG-RUNNING AGENTS  
**Data de Criação:** Maio 2026

---

## 📖 Prólogo: A Descoberta que Evitou Desastres

### A Visão que Começou Tudo

Fernando tinha um sonho claro para o KODA:

> *"Não queremos um chatbot que esquece tudo. Queremos um agente que seja como um amigo de confiança — alguém que o cliente pode chamar a qualquer momento e que realmente cresce junto com ele, lembrando suas necessidades, entendendo suas restrições, oferecendo recomendações que mudam vidas."*

Essa visão funcionava **em conversas curtas** (15-30 minutos). Mas quando clientes ligavam para conversa de 2-4 horas? Algo queimava.

### O Desastre de Múltiplas Faces

Vamos seguir **uma conversa real do KODA** que exemplifica o problema:

```
═══════════════════════════════════════════════════════════════
CONVERSA: Cliente procurando suplemento para treino

🕐 14:00 - INÍCIO DO SPRINT 1 (Discover Products)
Cliente: "Oi KODA! Procuro whey protein. Tenho alergia a lactose."
KODA: "Encontrei 3 ótimas opções SEM lactose! 
       1. Whey Isolado (R$ 89,90)
       2. Whey Vegano (R$ 95,00)
       3. Concentrado Plant (R$ 45,00)"
Cliente: "Perfeito! Quero a opção mais barata — a #3."

🕐 14:45 - [45 MINUTOS DEPOIS, MAS AINDA SPRINT 1]
Cliente: "Ah, uma coisa... eu tenho também restrição orçamentária.
         Máximo R$ 50. Você tinha considerado isso?"
KODA: "Verdade! Deixa eu refiltrar...
       Só a opção #3 (R$ 45) se encaixa no orçamento."
Cliente: "Ótimo! E sabor? Prefiro morango."
KODA: "Temos morango! Então: Product #3, Sabor Morango, R$ 45. Pronto!"
       [REGISTRA como RECOMENDAÇÃO FINAL]

🕐 15:45 - [90 MINUTOS DEPOIS - FIM DO SPRINT 1, INICIO SPRINT 2]
         [MUDANÇA IMPORTANTE: Informações críticas ficam "borradas"]
Cliente: "Então quer dizer que já resolvemos tudo? Vou comprar agora?"
KODA: "Claro! Qual produto você quer mesmo?"
Cliente: "O que VOCÊ recomendou!"
KODA: "Recomendo o Whey Isolado (R$ 89,90)!"
       [KODA ESQUECEU da restrição de R$ 50! ❌]
Cliente: "MAS EU FALEI QUE ERA MÁXIMO R$ 50!!!"
KODA: "Ah desculpe, verdade. Então vai o #3 de R$ 45."

🕐 16:30 - [AINDA MAIS TARDE, REQUIREMENTS MUDAM]
Cliente: "Ah... na verdade tive um insight. Meu nutricionista falou 
         que BCAA é melhor que whey para meu objetivo específico.
         Posso mudar?"
KODA: "Claro! Deixa buscar BCAA..."
       [Procura em novo catálogo de BCAA]
KODA: "Encontrei 5 opções! Qual você quer?"
       [PROBLEMA: As 3 recomendações anteriores (Product #1, #2, #3)
        agora são IRRELEVANTES. Temos novo contexto.]
Cliente: "Qual você recomenda?"
KODA: "O BCAA Premium Sabor Morango (R$ 60)!"
Cliente: "MAS VOCÊ FALOU QUE ERA ATÉ R$ 50!!!"
         [SEGUNDO CONFLITO ❌]

═══════════════════════════════════════════════════════════════
```

**Análise:** Três desastres aconteceram:

1. ❌ **Recomendações Contraditórias:** KODA recomendou #3 (R$ 45), depois #1 (R$ 89,90)
2. ❌ **Descontinuidade Entre Sprints:** Quando Sprints mudaram, contexto crítico ("orçamento R$ 50") se perdeu
3. ❌ **Requirements Mudando:** Cliente mudou de Whey para BCAA, e não havia "contrato" sobre como lidar com mudança

### O Insight Estratégico

Fernando percebeu algo crucial: **O problema não era a IA ser ruim. O problema era a arquitetura ser fraca.**

Especificamente: **Não havia contrato claro sobre o que "pronto" significa antes de começar.**

Quando KODA começou o Discover Products Sprint, não havia acordo:
- ✗ "O que entra? Cliente pode mudar requisitos?"
- ✗ "O que significa 'pronto'? 1 recomendação ou 3?"
- ✗ "Se mudarem requisitos, começamos nova busca ou ajustamos a atual?"
- ✗ "Recomendação é 'final' ou pode ser revisada?"

**E se você definisse essas expectativas ANTES de começar?**

### Como Sprint Contracts Resolvem Isso

A solução: **Um "contrato" negociado entre Generator (que busca) e Evaluator (que valida)** sobre o que "pronto" significa.

```
SPRINT CONTRACT: Discover Products

INPUT SPECIFICATION:
✓ Cliente especifica: orçamento, restrições (alergia), preferência de sabor
✓ Se requisitos mudarem DURANTE sprint, reiniciamos com novo contrato

SUCCESS CRITERIA (O que "Pronto" Significa):
✓ 3-5 opções válidas encontradas
✓ TODAS respeitam orçamento máximo
✓ TODAS respeitam restrições (alergia, intolerância)
✓ TODAS têm sabor preferido
✓ Explicação clara de por que cada uma se encaixa

FAILURE HANDLING:
✓ Se cliente muda orçamento: iniciar novo sprint com novo contrato
✓ Se cliente muda tipo de produto (whey→BCAA): novo contrato
✓ Se algo não atender critérios: rejeitar e recomçar
```

**Com esse contrato negociado:**

- ✅ KODA sabe exatamente quando parar (quando 3-5 opções válidas existem)
- ✅ KODA sabe o que "válido" significa (orçamento+alergia+sabor)
- ✅ Se requirements mudarem, há procedimento claro (novo contrato, novo sprint)
- ✅ Recomendações nunca serão contraditórias (ambos concordaram nos critérios primeiro)

### Impacto nos Números

Quando KODA implementou Sprint Contracts (junto com padrões Nível 1):

| Métrica | Antes | Depois | Melhoria |
|---------|-------|--------|----------|
| **Erros em conversas 2h+** | 40% dos outputs tinham inconsistência | 2% | -95% ✅ |
| **Refazimento (recomendações rejeitadas)** | 30% das recomendações precisava refazer | 5% | -83% ✅ |
| **Confiabilidade do cliente** | 85% dos clientes confiava na recomendação | 95% | +12% ✅ |
| **Churn por inconsistência** | 8% dos clientes desistia por confusão | 1% | -87% ✅ |

**Nenhuma mudança no modelo. Apenas na arquitetura — como os agentes colaboram.**

### Diferencial Vs. Generator/Evaluator

Você aprendeu no módulo anterior sobre **Generator/Evaluator**: um agente gera solução, outro valida DEPOIS.

**Sprint Contracts vão além:**

| Aspecto | Generator/Evaluator | Sprint Contract |
|---------|-------------------|-----------------|
| **Quando valida** | DEPOIS da geração | ANTES + DURANTE + DEPOIS |
| **Negociação** | Não há | Sim, explícita |
| **Mudanças mid-sprint** | Problema (Gen já começou) | Tratada (novo contrato) |
| **Comunicação** | Implícita (rubric) | Explícita (acordo) |
| **Escopo de validação** | Output final | Processo inteiro |
| **Melhor para** | Validar qualidade | Garantir alinhamento |

**Sinergia:** Gen/Evaluator + Sprint Contracts = **sistema robusto.**

Gen/Evaluator valida depois. Sprint Contracts previne problemas antes. Juntos? **Quase impossível algo sair errado.**

### O Que Você Vai Aprender Agora

Neste módulo, você vai:

✅ Entender os **3 pilares** de um Sprint Contract (Input, Criteria, Failure Handling)  
✅ Aprender o **processo de negociação** entre Generator e Evaluator  
✅ Aplicar a **3 casos reais do KODA** (Discover, Checkout, Long Conversation)  
✅ Desenhar Contracts que **evitam 40% dos erros**  
✅ Implementar um **checklist prático**  
✅ Evitar **5 armadilhas comuns**

E ao final, você terá a mesma superpotência que Fernando tem: **transformar arquitetura em confiabilidade.**

---

## 🎯 O Que É um Sprint Contract?

### Definição Formal

Um **Sprint Contract** é um acordo **explícito, negociado e testável** entre um Generator (agente que executa) e um Evaluator (agente que valida) sobre o que significa "pronto" para um sprint específico.

Diferente de instruções genéricas ("recomende um produto"), um Contract é um **pacto bilateral**:

> **"Generator: Eu vou buscar recomendações se você (Evaluator) concordar que 'pronto' significa: orçamento respeitado, alergias respeitadas, e explicação clara. Correto?"**
>
> **Evaluator: "Concordo com esses critérios. Se você entregar isso, aprovo. Se não, rejeito."**

Quando ambos concordam, o Contract está **selado**. Agora executor e validador têm expectativas iguais.

---

### Os 3 Pilares de um Sprint Contract

Cada Contract tem 3 componentes obrigatórios:

#### 🔹 **Pilar 1: Input Specification**
*O que entra no sprint?*

Define explicitamente:
- Dados de entrada (cliente precisa de X, tem restrição Y)
- Contexto disponível (histórico, catálogo, estado)
- Limites (máximo 30 minutos, máximo 100K tokens)
- O que pode mudar durante (requisitos do cliente podem evoluir? Se sim, como?)

**Exemplo KODA:**
```
INPUT SPECIFICATION - Discover Products Sprint
├─ Cliente especifica: orçamento máximo, restrições (alergia/intolerância)
├─ Histórico disponível: compras anteriores, preferências salvas
├─ Catálogo: produtos em estoque com preços atualizados
├─ Limite de tempo: 30 minutos máximo
└─ Se cliente muda requisito: renegociar contract (novo sprint)
```

#### 🔹 **Pilar 2: Success Criteria**
*O que significa "pronto"?*

Define critérios **testáveis e objetivos**:
- Quantos outputs? (1? 3-5? Todos os que se encaixam?)
- Que validações DEVEM passar? (sem lactose = TRUE?)
- Qual é o padrão de qualidade? (explicação ≥ 50 caracteres?)
- Quando pode parar? (quando encontrou 3 válidas ou após 100 buscas?)

**Exemplo KODA:**
```
SUCCESS CRITERIA - Discover Products Sprint
✓ 3-5 opções válidas encontradas (não menos, não mais)
✓ TODAS respeitam orçamento máximo do cliente
✓ TODAS respeitam restrições (alergia, intolerância)
✓ TODAS têm sabor/forma preferida
✓ Cada uma tem explicação clara (≥50 caracteres)
✓ Ranking ordenado por melhor relação preço/benefício
```

#### 🔹 **Pilar 3: Failure Handling**
*O que fazer se não conseguir?*

Define procedimentos quando algo sai errado:
- Se não encontrou 3 opções válidas? Retornar parcial ou rejeitar?
- Se cliente mudou requisito? Rejeitar contract anterior ou renegociar?
- Se há conflito de critérios? (Ex: orçamento R$ 50 + sabor morango, mas tem 1 opção de R$ 120?)
- Máximo de tentativas antes de fail?

**Exemplo KODA:**
```
FAILURE HANDLING - Discover Products Sprint
├─ Menos de 3 opções válidas encontradas?
│  └─ AÇÃO: Informar cliente e pedir que relaxe requisitos (orçamento ou restrição)
│
├─ Cliente muda requisito (ex: de Whey para BCAA)?
│  └─ AÇÃO: Rejeitar contract anterior, negociar novo contract
│
├─ Conflito de critérios (impossível satisfazer todos)?
│  └─ AÇÃO: Listar o que é impossível, pedir priorização do cliente
│
└─ Após 5 tentativas ainda sem sucesso?
   └─ AÇÃO: Escalar para humano, não force recomendação ruim
```

---

### Analogias para Entender Melhor

#### 📜 **Analogia Jurídica: Contrato Real**

No mundo legal, um contrato entre duas partes tem:
- **Partes:** Você (Generator) e Avaliador (Evaluator)
- **Obrigações:** Generator obriga-se a entregar "pronto". Evaluator obriga-se a validar contra critérios acordados.
- **Consequências:** Se alguém não cumpre, há "breach of contract"
- **Negociação:** Ambos discutem até concordarem nos termos

**Sprint Contract funciona exatamente assim.** Sem esse acordo prévio, é como começar um projeto sem contrato — tudo vago, expectativas diferentes.

#### 👨‍🍳 **Analogia Profissional: Chef & Inspetor de Qualidade**

Num restaurante:

- **Chef (Generator):** "Vou fazer Pasta à Carbonara"
- **Gerente de Qualidade (Evaluator):** "OK, mas deixa claro: o que significa 'Carbonara perfeita'?"
- **Negociação:**
  - Chef: "Guanciale, ovo, queijo pecorino, pimenta preta. Sem creme."
  - Gerente: "E se não tiver Guanciale hoje?"
  - Chef: "Uso bacon de qualidade equivalente, mas aviso ao cliente."
  - Gerente: "Ok, ficamos com isso."

**Agora ambos sabem exatamente o que é 'Carbonara pronta'.** Chef não faz com creme. Gerente não rejeita se usou bacon.

#### 🤖 **Analogia KODA: Vendedor & Gerente de Loja**

- **Vendedor (Generator):** "Vou recomendar 3 produtos para esse cliente"
- **Gerente (Evaluator):** "Que tipos de 'recomendação boa' você quer dizer?"
- **Negociação:**
  - Vendedor: "Produtos que respeitam alergia, orçamento e preferência"
  - Gerente: "E se não tiver opção que respeita todos 3?"
  - Vendedor: "Então retorno parcial — informo o conflito"
  - Gerente: "Aprovado. Isso é 'pronto'."

---

### Sprint Contract vs. Rubric vs. Task Description

Importante não confundir:

| Aspecto | Task Description | Rubric | Sprint Contract |
|---------|------------------|--------|-----------------|
| **O quê?** | "Faça X" | "Avalie por Y" | "Nós concordamos que Z = pronto" |
| **Quem cria?** | Alguém (task) | Evaluator (métricas) | Generator + Evaluator (juntos) |
| **Quem segue?** | Generator | Evaluator | Ambos |
| **Quando é claro?** | DURANTE execução | DURANTE avaliação | ANTES de começar |
| **Muda durante?** | Sim (causa problemas) | Raramente | Não (novo contract se mudar) |
| **Exemplo** | "Encontre 3 produtos" | "Sem lactose? ✓ Orçamento? ✓" | "Pronto quando: 3 produtos encontrados E sem lactose AND orçamento respeitado" |

**Sprint Contract = Task + Rubric + Acordo prévio**

---

### Quando Contract É Necessário (e Quando Não)

#### ✅ **Use Sprint Contract quando:**

- Sprint pode ter múltiplas interpretações de "pronto"
- Mudanças mid-sprint são prováveis (cliente muda de ideia)
- Há risco de refazimento (requirements mal definidos)
- Generator e Evaluator são entidades separadas
- Conversa é longa (4+ horas, múltiplos sprints)
- Há consequências altas de erro (checkout, processamento de pagamento)

#### ⚠️ **Talvez não precisa quando:**

- Sprint muito simples ("Busque 1 produto") - rubric é suficiente
- Generator e Evaluator são a mesma entidade
- Conversa é ultra-curta (<5 minutos)
- Erro tem baixa consequência (sugestão casual)

---

### Lifecycle Completo de um Sprint Contract

```
┌─────────────────────────────────────────────────┐
│ 1. PROPOSAL (Generator propõe)                   │
│    "Vou recomendar 3 produtos se você concordar │
│     que pronto = [Input/Criteria/Failure]"      │
└──────────────────┬──────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────┐
│ 2. NEGOTIATION (Evaluator critica e propõe ajustes)
│    "Aceito, mas adiciona validação de estoque"  │
└──────────────────┬──────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────┐
│ 3. AGREEMENT (Ambos concordam)                  │
│    ✓ Contract assinado (simbolicamente)         │
└──────────────────┬──────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────┐
│ 4. EXECUTION (Generator executa sob Contract)   │
│    Busca produtos, valida contra critérios      │
└──────────────────┬──────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────┐
│ 5. VERIFICATION (Evaluator verifica)            │
│    "Isso atende aos critérios concordados?"     │
│    ✓ Sim → Aprova                              │
│    ✗ Não → Rejeita + feedback                  │
└──────────────────┬──────────────────────────────┘
                   ↓
        ┌─────────────┴──────────────┐
        ↓                            ↓
   ┌──────────────┐          ┌───────────────┐
   │ 6a. SUCCESS  │          │ 6b. FAILURE   │
   │ Entrega sai  │          │ Executa ação  │
   │ (novo sprint)│          │ do Pillar 3   │
   └──────────────┘          └───────────────┘
```

---

### Quem Negocia o Contract?

**Padrão ideal:**

- **Generator:** Propõe contract ("Vou fazer X se você concordar que pronto é Y")
- **Evaluator:** Critica e sugere ajustes ("Concordo com Y, mas adiciona Z")
- **Ambos:** Chegam a acordo ("OK, ficamos com Y + Z")

**Quem tem o poder?**
- Generator propõe baseado em capabilities ("Consigo fazer isso? Quanto custa em tokens?")
- Evaluator tem **veto** ("Não aceito critério vago")

Quando ambos têm incentivos alinhados (sucesso = sucesso para os dois), negociação é rápida.

---

### Estrutura Visual Recomendada

Quando você vai escrever um Contract, use essa structure:

```
╔═══════════════════════════════════════════════════╗
║        SPRINT CONTRACT: [Nome do Sprint]         ║
╠═══════════════════════════════════════════════════╣
║ GERADOR: [Quem vai executar]                     ║
║ AVALIADOR: [Quem vai validar]                    ║
║ DURAÇÃO: [Tempo máximo]                          ║
╠═══════════════════════════════════════════════════╣
║ 📥 INPUT SPECIFICATION                           ║
║ • [O que entra]                                  ║
║ • [Contexto disponível]                          ║
║ • [Limites]                                      ║
╠═══════════════════════════════════════════════════╣
║ ✅ SUCCESS CRITERIA                              ║
║ • [Critério 1 - testável]                        ║
║ • [Critério 2 - testável]                        ║
║ • [Critério 3 - testável]                        ║
╠═══════════════════════════════════════════════════╣
║ ⚠️ FAILURE HANDLING                              ║
║ Se [Situação A] → [Ação]                         ║
║ Se [Situação B] → [Ação]                         ║
║ Se [Situação C] → [Ação]                         ║
╚═══════════════════════════════════════════════════╝
```

---

### Exemplo Simples: "Recommend 1 Product"

Vamos ver um micro-contract bem simples:

```
╔═══════════════════════════════════════════════════╗
║    SPRINT CONTRACT: Recommend 1 Product          ║
╠═══════════════════════════════════════════════════╣
║ GERADOR: KODA (agent que recomenda)             ║
║ AVALIADOR: Quality Gate (valida recomendação)   ║
║ DURAÇÃO: 2 minutos máximo                       ║
╠═══════════════════════════════════════════════════╣
║ 📥 INPUT SPECIFICATION                           ║
║ • Cliente especificou: orçamento, restrição     ║
║ • Histórico de compras: acessível                ║
║ • Catálogo: produtos em estoque                  ║
╠═══════════════════════════════════════════════════╣
║ ✅ SUCCESS CRITERIA                              ║
║ • 1 produto selecionado                          ║
║ • Respeita orçamento? TRUE                       ║
║ • Respeita restrição? TRUE                       ║
║ • Tem explicação (≥20 chars)? TRUE               ║
╠═══════════════════════════════════════════════════╣
║ ⚠️ FAILURE HANDLING                              ║
║ Se (orçamento ∩ restrição = ∅) → Informar cliente
║ Se explicação é vaga → Rejeitar, refazer        ║
║ Se timed out (>2min) → Retornar None, escalar   ║
╚═══════════════════════════════════════════════════╝
```

---

### Conexão com Nível 1

Você aprendeu em Nível 1 sobre 3 problemas fundamentais:

**Sprint Contract resolve:**

- ✅ **Context Amnesia:** Especificação clara (Pilar 1) reduz risco de esquecer requisitos
- ✅ **Token Budgeting:** Duração máxima definida (Pilar 1: limite de tempo)
- ✅ **Weak Harness:** Success Criteria (Pilar 2) É o harness. Define exatamente o que validar

Sprint Contracts são uma **aplicação prática dos padrões de Nível 1.**

---

### Diferença de Harness

**Harness** (Nível 1): Padrão estruturado que força uma sequência específica.

Exemplo: "Antes de recomendar, sempre verificar alergia. Sempre."

```
HARNESS:
1. Check alergia
2. Filter produtos
3. Validar produtos vs alergia
4. Recomendar
```

**Sprint Contract:** Acordo sobre expectativas do que "pronto" significa.

```
CONTRACT:
"Pronto quando: alergia foi checada E
 produtos foram filtrados E
 recomendação foi validada"
```

**A diferença?** Harness é **padrão de execução**. Contract é **acordo sobre resultado**.

**Usados juntos:** Contract define "o quê pronto é" (Success Criteria). Harness define "como chegar lá".

---

### Contracts Como Templates Reutilizáveis

Um Contract não precisa ser único para cada conversa.

Você pode criar **templates**:

```
TEMPLATE: Product Recommendation Contract
├─ INPUT: Customer specifies (budget, restrictions)
├─ CRITERIA: 3-5 valid options, all meet constraints
└─ FAILURE: If <3 options, ask customer to relax

INSTÂNCIAS:
├─ Conversa #1 com Cliente A: Use template + budget=50
├─ Conversa #2 com Cliente B: Use template + budget=200
├─ Conversa #3 com Cliente C: Use template + budget=75
```

Todos usam o mesmo **structure** (template), mas com **parâmetros diferentes** (budget).

Isso é escalável e eficiente.

---

### Escalabilidade: De 1 Contract para 10.000

**Cenário:** KODA está crescendo. Você tem:
- 1 tipo de Generator (KODA agent)
- 1 tipo de Evaluator (Quality Gate)
- Mas 10.000 conversas simultâneas

**Pergunta:** Precisa de 10.000 contracts diferentes?

**Resposta:** Não! Você usa **templates**:

```
TEMPLATE LIBRARY:
├─ Product Recommendation (template #1)
├─ Order Checkout (template #2)
├─ Delivery Tracking (template #3)
└─ Complaint Resolution (template #4)

CADA CONVERSA:
├─ Conversa #1: Usa Template #1 (Product)
├─ Conversa #2: Usa Template #1 (Product)
├─ Conversa #3: Usa Template #2 (Checkout)
├─ Conversa #4: Usa Template #1 (Product)
└─ Conversa #5: Usa Template #3 (Delivery)
```

**Benefício:** 4 templates bem-pensados servem 10.000 conversas.

Mudanças globais? Atualiza o template uma vez, todas as 10.000 conversas afetadas.

---

### Resumo: O Que É um Sprint Contract?

**Em 1 frase:**
Um Sprint Contract é um acordo negociado, explícito e testável entre Generator e Evaluator sobre exatamente o que "pronto" significa.

**Em 3 pilares:**
1. 📥 **Input:** O que entra
2. ✅ **Criteria:** O que significa pronto
3. ⚠️ **Failure:** O que fazer se falhar

**Em 1 benefício:**
Evita surpresas, refazimento, e inconsistências — transformando expectativas vagas em consenso claro.

---

## 🔄 Sprint vs. Loop vs. Harness: Entendendo os Relacionamentos

Três conceitos que trabalham juntos. Vamos clarificar cada um e como se relacionam.

---

### 📌 Definições Fundamentais

#### **Sprint: O Átomo do Trabalho**

Um **Sprint** é uma unidade discreta e bem-definida de trabalho:
- **Duração:** 30-120 minutos de execução do agente
- **Escopo:** Uma tarefa específica com contract claro
- **Entrada:** Dados bem-definidos
- **Saída:** Resultado (sucesso ou falha específica)
- **Padrão:** Pode ser repetido múltiplas vezes com inputs diferentes

**Características:**
- ✅ Tem início e fim definidos
- ✅ Contract negocia "pronto" antes de começar
- ✅ Resultado é testável (passou nos critérios? Sim/Não)
- ✅ Independente (não depende do resultado de outro sprint)

**Exemplo KODA - Discover Products Sprint:**
```
INPUT: Cliente quer whey protein, orçamento R$ 100, sem lactose
↓
SPRINT EXECUTA (Duração: 5 minutos)
↓
OUTPUT: 3 opções válidas encontradas ✓
```

#### **Loop: A Molécula da Repetição**

Um **Loop** é um ciclo que contém um ou mais Sprints, repetindo até satisfazer uma condição:
- **Quando ativa:** Quando resultado do sprint não é "perfeito"
- **Iterações:** 2-5 tentativas típicas (máximo configurável)
- **Condição de saída:** Sucesso OU máximo de tentativas atingido
- **Custo:** Sprint × N iterações

**Características:**
- ✅ Contém sprints dentro dele
- ✅ Repete enquanto condição não é satisfeita
- ✅ Cada iteração aprende da anterior
- ✅ Gasta mais tokens (múltiplas execuções)

**Exemplo KODA - Retry Loop (se Discover falhar):**
```
LOOP: "Encontrar 3 opções, máximo 3 tentativas"
├─ ITERAÇÃO 1: Sprint (procura com critérios rigorosos)
│  └─ Resultado: Encontrou 2 opções (não é 3) ❌
│
├─ ITERAÇÃO 2: Sprint (relaxa orçamento em 10%)
│  └─ Resultado: Encontrou 3 opções ✓
│
└─ SAÍDA: Sucesso na iteração 2
```

#### **Harness: O Padrão da Estrutura**

Um **Harness** é um padrão estruturado que governa COMO algo é executado:
- **O quê governa:** Sequência de passos, validações, checkpoints
- **Por quê existe:** Garante consistência mesmo sob pressão
- **Aplica a:** Sprints (como executar) e Loops (padrão de retry)
- **Não é:** Uma unidade de trabalho, mas um padrão para executar unidades

**Características:**
- ✅ Define sequência obrigatória
- ✅ Define validações em cada passo
- ✅ Força rigor (não permite "pular passos")
- ✅ Reutilizável (mesmo harness para múltiplos sprints)

**Exemplo KODA - Harness para Recomendação:**
```
HARNESS: Product Recommendation Pattern
1. CHECK RESTRIÇÕES (alergia, intolerância) → valida
2. FILTER CATÁLOGO (apenas produtos válidos) → valida
3. RANK POR CRITÉRIOS (preço, avaliação) → valida
4. VALIDATE RANKING (topo atende criteria?) → valida
5. COMMUNICATE (explicar por quê cada uma) → valida
[Sem pular passos. Sempre.]
```

---

### 🔗 Como Se Relacionam: A Hierarquia

```
┌─────────────────────────────────────────┐
│           LOOP (Repetição)              │
│  ┌───────────────────────────────────┐  │
│  │   SPRINT 1 (Tentativa 1)          │  │
│  │  ┌─────────────────────────────┐  │  │
│  │  │  HARNESS (Padrão de exec)   │  │  │
│  │  │  ✓ Passo 1                   │  │  │
│  │  │  ✓ Passo 2                   │  │  │
│  │  │  ✓ Passo 3                   │  │  │
│  │  └─────────────────────────────┘  │  │
│  │  Resultado: Falhou ❌              │  │
│  └────────────┬──────────────────────┘  │
│               ↓                          │
│  ┌───────────────────────────────────┐  │
│  │   SPRINT 2 (Tentativa 2)          │  │
│  │  ┌─────────────────────────────┐  │  │
│  │  │  HARNESS (Mesmo padrão)     │  │  │
│  │  │  ✓ Passo 1                   │  │  │
│  │  │  ✓ Passo 2                   │  │  │
│  │  │  ✓ Passo 3                   │  │  │
│  │  └─────────────────────────────┘  │  │
│  │  Resultado: Sucesso ✓              │  │
│  └───────────────────────────────────┘  │
│  LOOP TERMINA (sucesso)                 │
└─────────────────────────────────────────┘
```

**Leitura da hierarquia:**
- **Loop contém Sprints** — Sprint é unidade discreta dentro do loop
- **Sprint usa Harness** — Harness governa como sprint executa
- **Contract define Sprint** — Sprint Contract diz quando o sprint é "pronto"

---

### 📊 Tabela Comparativa

| Aspecto | Sprint | Loop | Harness |
|---------|--------|------|---------|
| **É uma unidade de trabalho?** | ✅ Sim | ❌ Não (contém unidades) | ❌ Não (padrão) |
| **Tem início e fim?** | ✅ Sim | ✅ Sim | ❌ Não (padrão contínuo) |
| **Pode falhar?** | ✅ Sim (parte do design) | ✅ Sim (max tentativas) | ❌ Não (padrão imutável) |
| **Pode repetir?** | ✅ Sim (em loops) | ✅ Sim (iterações) | ✅ Sim (múltiplas execuções) |
| **Tem contract?** | ✅ Sim | ❌ Não | ❌ Não |
| **Quando usar** | Tarefa discreta | Quando retry é necessário | Padrão crítico |
| **Custo** | X tokens | X * N tokens | Incluído no custo do sprint |
| **Exemplo KODA** | Discover 1x | Descobrir com 3 tentativas | Validação de restrições |

---

### 🎯 Quando Usar Cada Um

#### ✅ **Use SPRINT quando:**
- Tarefa tem escopo claro e definido
- Requisitos são estáveis (não vão mudar)
- Resultado é "sucesso ou falha específica"
- Conversa tem duração curta (<30 minutos)
- Generator e Evaluator concordam no contract

**Exemplo:** "Busque 3 produtos para esse cliente" (uma vez)

#### ✅ **Use LOOP quando:**
- Sprint pode falhar e você quer retry
- Você pode "relaxar" requisitos entre tentativas
- Há margem para aprendizado (iteração 2 usa feedback de iteração 1)
- Você quer máximo de tentativas (proteção contra loops infinitos)
- Falha total é aceitável (após N tentativas, falha e escala)

**Exemplo:** "Busque 3 produtos, e se não conseguir, relaxe orçamento e tente de novo (máx 3 vezes)"

#### ✅ **Use HARNESS quando:**
- Padrão deve ser executado SEMPRE igual
- Há validações críticas em cada passo
- Erro é inaceitável (segurança, conformidade, qualidade)
- Padrão será reutilizado muitas vezes
- Quer garantir consistência sob pressão (contexto grande, tokens baixos)

**Exemplo:** "Sempre valide restrição ANTES de recomendar. Sem exceções."

---

### 📖 Narrativas: De Teoria a Prática KODA

#### **Narrativa 1: Customer Journey Simples (Sprint Único)**

```
Cliente chega ao KODA, quer comprar whey protein.

🕐 14:00 - INÍCIO
└─ SPRINT: Discover Products
   ├─ INPUT: Orçamento R$ 100, sem lactose, sabor chocolate
   ├─ HARNESS: Validar restrição → filtrar → rankear → comunicar
   ├─ OUTPUT: 3 opções (Whey Isolado, Whey Vegano, Concentrado)
   └─ Resultado: Sucesso ✓

🕐 14:15 - PRÓXIMO SPRINT
└─ SPRINT: Process Order
   ├─ INPUT: Cliente escolheu Whey Isolado
   ├─ HARNESS: Validar endereço → confirmar itens → processar pagamento
   ├─ OUTPUT: Pedido confirmado #12345
   └─ Resultado: Sucesso ✓

🕐 14:30 - FIM
Conversa: 30 minutos, 0 loops, 2 sprints sequenciais
```

**Por que não usou Loop aqui?** Tudo correu bem. Nenhum sprint falhou.

---

#### **Narrativa 2: Conversa Complexa com Retry (Sprint + Loop)**

```
Cliente procura BCAA com critérios muito restritivos.

🕐 14:00 - SPRINT 1 com LOOP
└─ LOOP: "Encontrar 3 opções, máximo 3 tentativas"
   │
   ├─ ITERAÇÃO 1 - SPRINT: Discover com critérios rigorosos
   │  ├─ INPUT: Orçamento R$ 50, sem glúten, sem soja, sabor morango
   │  ├─ OUTPUT: Encontrou 1 opção (não é 3) ❌
   │  └─ AÇÃO: Relaxa orçamento → R$ 75
   │
   ├─ ITERAÇÃO 2 - SPRINT: Discover com orçamento relaxado
   │  ├─ INPUT: Orçamento R$ 75, sem glúten, sem soja, sabor morango
   │  ├─ OUTPUT: Encontrou 2 opções (não é 3) ❌
   │  └─ AÇÃO: Remove restrição soja
   │
   ├─ ITERAÇÃO 3 - SPRINT: Discover com ambos relaxados
   │  ├─ INPUT: Orçamento R$ 75, sem glúten, sabor morango
   │  ├─ OUTPUT: Encontrou 3 opções ✓
   │  └─ AÇÃO: LOOP termina (sucesso)
   │
   └─ Resultado final: Sucesso após 3 iterações

🕐 14:20 - PRÓXIMO SPRINT (sem loop)
└─ SPRINT: Process Order (simples, sem retry)
   ├─ OUTPUT: Pedido confirmado
   └─ Resultado: Sucesso ✓

🕐 14:35 - FIM
Conversa: 35 minutos, 1 loop (3 iterações), 2 sprints sequenciais
```

**Por que usou Loop?** Cliente tinha requisitos que talvez não tivessem solução exata. Loop permitiu iteração inteligente.

---

#### **Narrativa 3: Conversa Longa (Múltiplos Sprints em Sequence)**

```
Cliente conversa por 3 horas. Precisa de múltiplos "resetar".

🕐 14:00 - SPRINT 1: Discover Products
└─ Duração: 15 minutos
   └─ Resultado: 3 opções de Whey encontradas ✓

🕐 14:30 - SPRINT 2: Comparison (comparar opcoes)
└─ Duração: 20 minutos
   └─ Resultado: "Whey Isolado é melhor custo-benefício" ✓

🕐 15:00 - SPRINT 3: Questions About Delivery
└─ Duração: 15 minutos
   └─ Resultado: "Frete R$ 15, chegaria em 2 dias" ✓

[Cliente sai para almoço]

🕐 17:00 - [Voltou 2 horas depois]

🕐 17:00 - SPRINT 4: Rediscover (cliente mudou de ideia)
└─ INPUT: "Agora quero BCAA, não mais Whey"
└─ Duração: 20 minutos
   └─ Resultado: 3 opções de BCAA encontradas ✓
   └─ NOTE: Sprint 4 é NOVO, com novo contract
           Não usa histórico de Sprint 1 (que era Whey)

🕐 17:30 - SPRINT 5: Process Order (novo produto)
└─ INPUT: Cliente escolheu BCAA Chocolate
└─ Duração: 15 minutos
   └─ Resultado: Pedido confirmado ✓

🕐 17:45 - FIM
Conversa: ~3.5 horas, 5 sprints, 0 loops
```

**Por que multiple sprints?** Conversa era longa. Cada 30 minutos = novo "contexto fresco" (novo sprint com seu próprio contract). Isso evita Context Amnesia.

---

### 🏗️ Exemplo Completo KODA: Discover + Checkout com Harness

Vamos ver um exemplo que usa **Sprint + Harness** juntos:

```
╔════════════════════════════════════════════════════════╗
║  EXEMPLO: DISCOVER PRODUCTS COM HARNESS               ║
╚════════════════════════════════════════════════════════╝

SPRINT CONTRACT: Discover Products
┌────────────────────────────────────────────────────────┐
│ 📥 INPUT:                                              │
│ • Cliente: "Quero whey protein"                        │
│ • Restrição: Sem lactose                              │
│ • Orçamento: Máximo R$ 100                            │
│                                                        │
│ ✅ SUCCESS CRITERIA:                                   │
│ • 3-5 opções válidas encontradas                      │
│ • Todas respeitam orçamento E restrição               │
│ • Cada uma tem explicação clara                       │
│                                                        │
│ ⚠️ FAILURE HANDLING:                                   │
│ • Se <3 opções: informar cliente, sugerir relaxar     │
└────────────────────────────────────────────────────────┘

EXECUÇÃO USANDO HARNESS:

┌─ PASSO 1: CHECK RESTRIÇÕES (Harness Obrigatório)
│  ├─ Cliente tem alergia a lactose? SIM
│  ├─ Salvar em memória: [restrição: sem_lactose]
│  └─ ✓ Validado
│
├─ PASSO 2: BUSCAR CATÁLOGO (Harness Obrigatório)
│  ├─ Query: "produtos proteína AND sem_lactose AND preço ≤ 100"
│  ├─ Resultado: 8 produtos válidos
│  └─ ✓ Validado
│
├─ PASSO 3: RANKEAR (Harness Obrigatório)
│  ├─ Critério 1: Melhor avaliação (reviews)
│  ├─ Critério 2: Melhor preço
│  ├─ Top 5: [Whey Isolado R$89, Whey Vegano R$95, ...]
│  └─ ✓ Validado
│
├─ PASSO 4: VALIDAR RECOMENDAÇÃO (Harness Obrigatório)
│  ├─ Top 3 tem sem lactose? SIM (checkar contra restrição salva)
│  ├─ Top 3 está dentro orçamento? SIM
│  └─ ✓ Validado (não passa, rejeita tudo)
│
└─ PASSO 5: COMUNICAR
   ├─ "Encontrei 3 opções. Todas respeitam sua restrição e orçamento:"
   ├─ "1. Whey Isolado (R$ 89) - Melhor isolado do mercado"
   ├─ "2. Whey Vegano (R$ 95) - 100% plant-based"
   ├─ "3. Concentrado Chocolate (R$ 75) - Melhor preço"
   └─ ✓ Pronto segundo contract!

RESULTADO: Sprint Completou com Sucesso ✓
```

**O que o Harness garante?** Mesmo que KODA estivesse "cansado" (contexto grande), o Harness FORÇA a validação de restrição em cada passo. Impossível "esquecer" a alergia.

---

### 💾 Implicações de Tokens

Um detalhe importante para entender o custo:

```
SPRINT: Busque 3 produtos
└─ Custo: ~2.000 tokens (search + rank + validate)

LOOP (3 iterações) com SPRINT repetido:
├─ Iteração 1: Sprint (~2.000 tokens)
├─ Iteração 2: Sprint (~2.000 tokens) + feedback de iteração 1 (+500 tokens)
├─ Iteração 3: Sprint (~2.000 tokens) + feedback de iterações 1-2 (+1.000 tokens)
└─ Total: ~7.500 tokens (vs 2.000 se fosse sucesso na primeira)

HARNESS (padrão repetido):
└─ Custo: Incluído no sprint. Padrão em si não custa mais.
   (Mas garante menos refazimento, então economiza tokens no longo prazo)
```

**Implicação:** Loops são caros. Use quando necessário, mas proteja com `máximo de tentativas`.

---

### 🎁 Nesting: Padrões Dentro de Padrões

Você pode aninhar conceitos:

```
CONVERSA LONGA (3+ horas)
└─ LOOP (Retry de conversas)
   ├─ SPRINT 1 (Discover)
   │  └─ HARNESS (Validação de restrições)
   │
   ├─ SPRINT 2 (Comparison)
   │  └─ HARNESS (Validação de comparação)
   │
   └─ SPRINT 3 (Checkout)
      └─ HARNESS (Validação de pagamento)
```

**Leitura:**
- Loop contém múltiplos Sprints (sequencial, não repetição)
- Cada Sprint usa seu Harness
- Cada Harness garante validações específicas

---

### 🔗 Conexão a Generator/Evaluator

Lembra do padrão anterior? Aqui está como se conecta:

```
GENERATOR = Sprint (executa uma vez)
EVALUATOR = Harness (padrão de validação)
LOOP = Retry mechanism (se generator falha, tenta novamente)

FLUXO:
1. Generator propõe Sprint Contract
2. Evaluator usa Harness para validar
3. Se falha: LOOP começa (retry)
4. Se passa: Sprint termina, próximo sprint inicia
```

**Sinergia:** Generator/Evaluator define QUEM valida. Sprint/Loop/Harness define COMO e QUANTAS VEZES.

---

### ⚠️ Anti-Padrão: O Que Não Fazer

**"Faça um Loop SEM SPRINT definido"**

```
❌ ANTI-PADRÃO: Conversa sem estrutura
└─ Loop: "Recomende produtos até cliente ficar feliz"
   ├─ Iteração 1: Recomenda
   ├─ Iteração 2: Recomenda novamente
   ├─ Iteração 3: Recomenda mais uma vez
   ├─ Iteração 4: ...
   ├─ Iteração 47: ...
   └─ Resultado: CAOS

PROBLEMA:
• Sem Sprint definido = sem contract = sem "pronto" claro
• Sem "pronto" definido = loop pode rodar para sempre
• Cliente nunca sabe quando terminou
• Tokens sendo gastos à toa
```

**Por que é ruim?** Loops PRECISAM de Sprint bem-definido para saber quando parar.

---

### ✅ Recomendação para KODA

Baseado em tudo acima, aqui está o **padrão ideal para KODA**:

```
PARA CONVERSAS CURTAS (< 30 minutos):
├─ 1-3 Sprints sequenciais
├─ Cada sprint tem seu contract
├─ Loop só se retry é necessário
└─ Harness em padrões críticos (restrições, pagamento)

PARA CONVERSAS LONGAS (30+ minutos):
├─ Múltiplos sprints sequenciais (1 a cada 20-30 minutos)
├─ Cada sprint reseta contexto (novo contract)
├─ Loop para retry em sprints críticos
├─ Harness em TODOS os sprints (consistência)
└─ Benefício: Evita Context Amnesia, mantém tokens saudáveis

CHECKLIST KODA:
✓ Sprint tem contract explícito?
✓ Contract tem Input + Criteria + Failure?
✓ Harness está definido para padrão crítico?
✓ Loop tem máximo de tentativas?
✓ Cada sprint é independente (não depende de anterior)?
```

---

### 🎓 Próximos Passos: Exercícios Técnicos

Na próxima seção (exercícios), você vai:

✅ **Exercício 1:** Desenhar um Sprint Contract para "Discover Products" (com Input/Criteria/Failure)  
✅ **Exercício 2:** Desenhar o Harness que valida esse Sprint (passos sequenciais)  
✅ **Exercício 3:** Desenhar um Loop que faz retry se Sprint falha (com máximo tentativas)  
✅ **Exercício 4:** Combinar tudo em um exemplo de conversa longa (Sprint → Loop → Harness)

Esses exercícios estarão em **arquivo separado** (`exercise-01_-_02-nivel-2-practical-patterns.md`) com exemplos detalhados e código pseudo-Python.

---

### 📌 Resumo: Sprint vs. Loop vs. Harness

**Sprint:**
- Unidade discreta de trabalho (30-120 minutos)
- Tem contract definido antes de começar
- Sucesso/Falha testável

**Loop:**
- Ciclo que contém sprints repetidos
- Ativa quando sprint falha e retry é necessário
- Protegido com máximo de tentativas

**Harness:**
- Padrão estruturado de execução
- Define sequência obrigatória + validações
- Reutilizável em múltiplos sprints

**Juntos:** Sprint com Harness + Loop como fallback = sistema robusto e escalável.

---

## 🤝 O Processo de Negociação do Contract

### Fase 1: Generator Propõe

[TO BE WRITTEN]

### Fase 2: Evaluator Negocia

[TO BE WRITTEN]

### Fase 3: Ambos Concordam

[TO BE WRITTEN]

### Fluxo Completo com Exemplo

[TO BE WRITTEN]

---

## 💼 Caso 1: Discover Products Sprint — O Caminho Feliz com Proteção

### O Cenário

Cliente chega ao KODA:
```
🕐 14:00
Cliente: "Oi KODA! Procuro whey protein. Tenho alergia a lactose, 
         orçamento máximo R$ 100, e prefiro sabor chocolate."
KODA: "Perfeito! Deixa eu buscar as melhores opções para você."
```

Cliente tem **requisitos claros**. Nada ambíguo. Isso é ideal para um Sprint bem-definido.

### Sprint Contract: Discover Products

```
╔════════════════════════════════════════════════════════╗
║      SPRINT CONTRACT: Discover Products               ║
╠════════════════════════════════════════════════════════╣
║ GERADOR: KODA (agent que recomenda)                  ║
║ AVALIADOR: Quality Gate (valida contra contract)     ║
║ DURAÇÃO: 15 minutos máximo                           ║
╠════════════════════════════════════════════════════════╣
║ 📥 INPUT SPECIFICATION                               ║
║ • Cliente especifica: orçamento máximo (R$ 100)      ║
║ • Cliente especifica: alergia/intolerância (lactose) ║
║ • Cliente especifica: preferência (sabor chocolate)  ║
║ • Contexto: Catálogo com 150+ produtos em estoque   ║
║ • Limite: Máximo 15 minutos de busca                 ║
║ • Change during: Se cliente muda requisito → novo    ║
║   sprint, novo contract                              ║
╠════════════════════════════════════════════════════════╣
║ ✅ SUCCESS CRITERIA (TODOS devem passar)              ║
║ • 3-5 opções válidas encontradas (não menos, não mais)
║ • TODAS respeitam orçamento máximo (R$ ≤ 100)        ║
║ • TODAS respeitam alergia (sem lactose = TRUE)       ║
║ • TODAS têm sabor chocolate (preferência = TRUE)     ║
║ • Cada opção tem explicação clara (≥ 50 caracteres)  ║
║ • Ranking: Melhor relação preço/benefício no topo   ║
╠════════════════════════════════════════════════════════╣
║ ⚠️ FAILURE HANDLING                                   ║
║ Se <3 opções: Informar cliente                       ║
║ Se cliente muda requisito: Novo contract             ║
║ Se alergia foi esquecida: Harness detecta            ║
╚════════════════════════════════════════════════════════╝
```

### Como o Cliente Experimenta (POV Cliente)

```
Cliente sente: Segurança, clareza, recomendação confiável.
Não vê: O Harness validando alergia 2x nos bastidores.
Resultado: "KODA entende minhas necessidades e cuida."
```

### Customer Effort Score

**Sem Contract:** 6.2/10 (cliente precisa confirmar restrição)  
**Com Contract:** 8.9/10 (confiança na recomendação)  
**Melhoria:** +43%

### Failure Scenario: Cliente Muda de Ideia Mid-Sprint

```
🕐 14:02 - [KODA em plena busca de Whey]

Cliente: "Ah espera... minha nutricionista falou que BCAA é melhor. 
         Posso mudar?"

KODA: "Claro! Mas deixa eu começar nova busca com esse novo requisito.
       Novo contrato, novo sprint."

[Contract anterior é REJEITADO]
[Novo Sprint: Discover BCAA]

🕐 14:07 - KODA: "Encontrei 3 BCAA de boa qualidade..."
```

**Por que funciona?** Contract deixou claro: "Se requisito muda, novo contract". Nenhuma confusão.

### Error Recovery: Alergia Esquecida

```
HARNESS valida alergia em 2 passos:
1. Passo 1 (início): Extrair e salvar
2. Passo 4 (validação final): Re-validar contra top 3 produtos

Se algum produto TEM lactose → Rejeita tudo, refaz busca.
Máximo 2 tentativas, depois escala para humano.
```

### Métricas Antes/Depois

| Métrica | Sem Contract | Com Contract | Melhoria |
|---------|-------------|------------|----------|
| **Taxa de erro de alergia** | 2.1% | 0.05% | -97% ✅ |
| **Refazimento** | 8% | 1% | -87% ✅ |
| **Customer Effort** | 6.2/10 | 8.9/10 | +43% ✅ |

---

## 🛒 Caso 2: Process Order Sprint — Múltiplas Validações, Zero Erros

### O Cenário

Cliente escolheu Whey Isolado em Discover. Agora quer finalizar compra.

```
🕐 14:05
Cliente: "Como faço para comprar?"
KODA: "Vou confirmar informações antes de processar."
```

Checkout é **crítico** — dinheiro envolvido, zero margem de erro.

### Sprint Contract: Process Order (Detalhado com 5 Passos)

```
╔════════════════════════════════════════════════════════════════╗
║         SPRINT CONTRACT: Process Order (Checkout)             ║
╠════════════════════════════════════════════════════════════════╣
║ GERADOR: KODA                 AVALIADOR: Payment Gateway      ║
║ DURAÇÃO: 10 minutos máximo (crítico)                          ║
╠════════════════════════════════════════════════════════════════╣
║ ✅ SUCCESS CRITERIA (SEQUÊNCIA OBRIGATÓRIA)                   ║
║                                                               ║
║ ✓ PASSO 1: CONFIRM ADDRESS                                   ║
║   └─ Endereço não nulo AND válido? TRUE                      ║
║                                                               ║
║ ✓ PASSO 2: CONFIRM ITEMS & ESTOQUE                           ║
║   └─ Produto em estoque? TRUE                                ║
║   └─ Preço atual = preço escolhido? TRUE                     ║
║                                                               ║
║ ✓ PASSO 3: RE-VALIDATE RESTRIÇÕES (CRÍTICO!)                 ║
║   └─ Produto tem alergia? FALSO (sem lactose = TRUE)         ║
║   └─ Se falhar aqui: NÃO processa pagamento                  ║
║                                                               ║
║ ✓ PASSO 4: CALCULATE TOTAL                                   ║
║   └─ Total = (preço × qtd) + frete                           ║
║                                                               ║
║ ✓ PASSO 5: FINAL CONFIRMATION & PAYMENT                      ║
║   └─ Pagamento sucesso? Pedido criado ✓                      ║
║                                                               ║
║ Nota: Se qualquer passo falha, REJEITA tudo.                 ║
╚════════════════════════════════════════════════════════════════╝
```

### Como o Cliente Experimenta (POV Cliente)

```
🕐 14:05 - KODA: "Seu endereço ainda é Rua X, Apt 123?"
         Cliente: "Sim!"

🕐 14:06 - KODA: "Você quer 1x Whey Isolado (R$ 89)?"
         Cliente: "Isso!"

🕐 14:07 - KODA: "Este produto é SEM lactose, certo? Você tinha alergia."
         Cliente: "Verdade, obrigado!"

🕐 14:08 - KODA: "Total: R$ 89 + Frete R$ 15 = R$ 104. Confirma?"
         Cliente: "Confirmo!"

🕐 14:09 - KODA: "Processando... ✓ Sucesso! Pedido #78234 confirmado."
```

**Cliente sente:** Segurança absoluta. Nenhuma surpresa.

### Failure Scenarios: 3 Desastres Evitados

#### **Scenario A: Produto Saiu do Estoque**

```
Passo 2 valida: "Este whey ainda tem estoque?"
Resultado: NÃO (saiu do estoque)

SEM CONTRACT: Processaria mesmo assim (chargeback)
COM CONTRACT: "Ops! Produto saiu. Quer alternativa?"

[Novo Discover Sprint com tipo de produto = Whey similar]
```

#### **Scenario B: Preço Mudou (Promoção Expirou)**

```
Passo 4 calcula: "Whey era R$ 89, agora está R$ 95?"

SEM CONTRACT: Cobraria sem avisar (cliente se sente trapaceado)
COM CONTRACT: "Preço subiu para R$ 95. Ainda quer?"

Cliente pode recusar sem problema.
```

#### **Scenario C: Produto TEM Alergia (CRÍTICO!)**

```
Passo 3 valida: "Whey tem lactose? SIM (dados defasados)"

SEM CONTRACT: Processaria pagamento. Cliente sofre reação alérgica.
COM CONTRACT: "ALERTA: Produto contém lactose! Abortar!"

[Escala para humano. Cliente salvo.]
```

**Salvou uma vida. Não é dramático — é realidade.**

### Error Recovery

```
Erro em Passo 1 (endereço): Pedir confirmação novamente
Erro em Passo 2 (estoque): Oferecer alternativa (novo Discover)
Erro em Passo 3 (alergia): NUNCA processar. Escalar.
Erro em Passo 4 (preço): Refazer cálculo
Erro em Passo 5 (pagamento): Máximo 2 tentativas, depois avisar
```

### Métricas Antes/Depois

| Métrica | Sem Contract | Com Contract | Melhoria |
|---------|-------------|------------|----------|
| **Erros em checkout** | 5.2% | 0.1% | -98% ✅ |
| **Chargebacks** | 2.1% | 0.05% | -97% ✅ |
| **Refund rate** | 8% | 0.3% | -96% ✅ |
| **Customer Effort** | 4.1/10 | 9.2/10 | +124% ✅ |

---

## 🔄 Caso 3: Long Conversation Split — Dividindo 4 Horas em Sprints

### O Cenário

Cliente conversa por **3.5 horas** (descobre, compara, faz perguntas, volta 2h depois, muda de ideia, compra).

```
🕐 14:00 - Cliente: "Oi KODA! Procuro suplemento ideal para mim"
🕐 15:30 - [Conversa intensa: descoberta + comparação]
🕐 16:30 - [Cliente sai para almoço]
🕐 18:30 - [Cliente volta. Quer BCAA, não Whey]
🕐 19:00 - [Finaliza compra]
🕐 19:15 - Fim (3h 15min de conversa)
```

**Total: 5 sprints, múltiplas mudanças, nenhum erro.**

### Como Dividir em Sprints: O Segredo

**NÃO:** 1 sprint gigante de 3.5 horas (contexto >100K tokens)  
**SIM:** 5 sprints pequenos (~20K tokens cada)

```
SPRINT 1 (Discover Whey): 0-30 min
├─ Contract: Encontrar 5 opções
├─ Output: 5 opções + estado salvo
└─ Tokens: 15K (confortável)

SPRINT 2 (Comparison): 30-60 min
├─ Input: 5 opções de Sprint 1 + estado cliente
├─ Contract: Comparar 3 melhores
├─ Output: Recomendação top 1
└─ Tokens: 12K (histórico limpo)

[Cliente faz perguntas, 20 min]

SPRINT 3 (Questions): 60-90 min
├─ Contract: Responder sobre delivery/garantia
├─ Output: "Frete R$ 15, chegaria em 2 dias"
└─ Tokens: 10K (simples)

[Cliente sai, volta 2h depois]

SPRINT 4 (Rediscover): 150-170 min
├─ Input: Cliente quer BCAA (produto DIFERENTE!)
├─ Contract: Encontrar 3 BCAA válidos
├─ Output: 3 opções de BCAA
├─ [Alergia a lactose é HERDADA de Sprint 1]
└─ Tokens: 14K (novo start, mas com restrição herdada)

SPRINT 5 (Checkout): 170-180 min
├─ Contract: Processar pagamento (BCAA)
├─ Output: Pedido confirmado
└─ Tokens: 12K (simples checkout)

TOTAL: ~63K tokens gastos, distribuído.
SEM SPRINTS: ~100K+ tokens gastos (possível timeout).
ECONOMIA: ~37K tokens (37% de eficiência)
```

### Cada Sprint Tem Seu Próprio Contract

**SPRINT 1:** Descobrir 5 wheys válidos  
**SPRINT 2:** Comparar as 3 melhores  
**SPRINT 3:** Responder dúvidas específicas  
**SPRINT 4:** Descobrir 3 BCaas (novo produto!)  
**SPRINT 5:** Processar pagamento (com alergia herdada)

Cada contract é **independente**, mas **alergia é herdada**.

### How Client Experiences (POV Cliente)

```
Cliente sente: "Uma conversa fluida e natural de 3.5 horas"

Cliente NÃO vê: 
└─ Que história foi dividida em 5 sprints
└─ Que contexto foi resetado entre sprints
└─ Que tokens foram economizados
└─ Que alergia foi re-validada

Cliente SÓ vê:
└─ Recomendações consistentes
└─ Conversa que flui
└─ Nenhuma fricção
└─ Segurança (alergia sempre lembrada)

Customer Effort Score: 9.1/10 (excelente, sem perceber divisão)
```

### Context Management: O Que Passa, O Que Reseta

#### **O QUE PASSA** (Herdado entre Sprints)

```
✓ Alergia/restrições críticas ("sem lactose")
✓ Identificação do cliente (nome, email)
✓ Preferências explícitas ("gosta de chocolate")
```

#### **O QUE RESETA** (Novo Sprint, Contexto Limpo)

```
✗ Produtos específicos de sprint anterior
  └─ Sprint 1: "Whey #1, #2, #3"
     Sprint 4: "Esquece whey. BCAA agora."

✗ Histórico conversacional detalhado
  └─ Sprint 1: "Cliente perguntou se tem carboidrato extra"
     Sprint 4: Não importa mais, novo contexto

✗ Tokens gastos em sprint anterior
  └─ Sprint 1: Gasta 15K
     Sprint 4: Começa com 14K (histórico sumarizado = +2K)
     └─ Economia: 13K tokens!
```

**Estratégia:** Crítico passa. Tudo mais limpa-se.

### Failure Scenarios: 2 Desastres Evitados

#### **Failure 1: Sprint 4 Esquece Alergia**

```
Cliente volta 2h depois, quer BCAA.

SEM SPRINTS:
└─ Contexto de 2h atrás está "borrado"
   └─ KODA não lembra de alergia
   └─ Recomenda BCAA com LACTOSE
   └─ Cliente sofre reação

COM SPRINTS + CONTRACT:
├─ Sprint 4 contract especifica: "Alergia lactose (herdada)"
├─ Harness valida: "Este BCAA tem lactose? NÃO ✓"
└─ Seguro!
```

#### **Failure 2: Timeout After 3.5 Hours**

```
SEM SPRINTS:
└─ 1 contexto de 3.5h = 80K+ tokens
   └─ Espaço restante: 30K (apertado!)
   └─ Timeout possível

COM SPRINTS:
└─ Sprint 1-5 distribuído: ~63K tokens total
   └─ Cada sprint tem espaço confortável
   └─ Nunca timeout!
```

### Token Implications: O Verdadeiro Poder

```
SEM SPRINTS (contexto contínuo):
🕐 14:00 (inicio): 20K tokens livres ✓
🕐 15:00 (90 min): 15K tokens livres ⚠️
🕐 17:00 (180 min): 5K tokens livres 🚨 (aperrado!)
→ Qualidade degrada conforme conversa avança

COM SPRINTS (contexto resetado):
🕐 14:00 Sprint 1: 25K tokens livres ✓
🕐 14:45 Sprint 2: 20K tokens livres ✓ (histórico limpo)
🕐 15:30 Sprint 3: 20K tokens livres ✓ (histórico limpo)
🕐 18:30 Sprint 4: 18K tokens livres ✓ (novo start)
🕐 19:00 Sprint 5: 22K tokens livres ✓ (simples)
→ Qualidade consistente por toda conversa!
```

### Error Recovery: Quando Falha

```
Sprint 1 falha (não encontrou): Cliente relaxa requisitos
Sprint 4 falha (BCAA com alergia): Volta para Whey
Sprint 5 falha (pagamento recusado): Retry ou novo método
```

**Pattern:** Erro em sprint → Retry dessa sprint ou volta para anterior. Nunca força.

### Métricas Antes/Depois

| Métrica | Sem Sprints | Com Sprints | Melhoria |
|---------|----------|---------|----------|
| **Consistência em 4h** | 75% | 98% | +31% ✅ |
| **Alergia esquecida** | 3.2% | 0.05% | -94% ✅ |
| **Timeout rate** | 4% | 0% | -100% ✅ |
| **Token efficiency** | Desperdiça 40K | Economiza 40K | +50% ✅ |
| **Customer Effort** | 7.2/10 | 9.4/10 | +31% ✅ |

---

## 📊 Comparação Cross-Case: O Harness Aparece em Tudo

**Observação importante:** O mesmo Harness (validar alergia) aparece nos 3 casos, mas em contextos diferentes.

```
CASO 1 (Discover):
└─ Harness: Validar alergia ANTES de recomendar

CASO 2 (Checkout):
└─ Harness: Re-validar alergia ANTES de processar pagamento (Passo 3)
   └─ Camada final de segurança

CASO 3 (Long Conversation):
└─ Harness: Alergia é herdada entre sprints
   └─ Cada novo sprint recebe restrição crítica
```

**Pattern:** Mesmo harness, 3 lugares diferentes. **Reutilização = consistência + eficiência.**

---

## 📊 Métricas & Trade-Offs

### Quando Sprint Contracts Ajudam

✅ **Use quando:**
- Requisitos podem mudar mid-sprint
- Há risco de refazimento (ambiguidade)
- Conversa será longa (30+ minutos)
- Há consequências altas de erro (pagamento, alergia)
- Multiple stakeholders (Generator + Evaluator separados)
- Padrão será reutilizado (template)

❌ **NÃO use quando:**
- Sprint é ultra-simples (<5 minutos, resultado óbvio)
- Não há ambiguidade (cliente sabe exatamente o quê quer)
- Erro tem baixa consequência (sugestão casual)
- Generator e Evaluator são a mesma coisa

### Trade-Offs Importantes

| Trade-off | Benefício | Custo | Quando Usar |
|-----------|-----------|------|-----------|
| **Complexidade** | Clareza absoluta | Setup inicial (+5 min) | Conversas 30+ min |
| **Token overhead** | Validações robustas | +500 tokens por sprint | Quando alergia/pagamento |
| **Negociação** | Consenso prévio | Tempo de agreement | Multi-stakeholder |
| **Rigidez** | Nenhuma surpresa | Difícil mudar mid-sprint | Quando mudança é cara |
| **Escalabilidade** | Não explode com volume | Templates bem feitos | 1.000+ conversas |

**Recomendação:** Benefício >> Custo. Use.

### Comparação com Generator/Evaluator Simples

| Aspecto | Gen/Eval Simples | + Sprint Contracts | Ganho |
|---------|-----------------|-------------------|-------|
| **Quando valida** | Depois (output) | Antes + durante + depois | Previne vs corrige |
| **Taxa de erro** | 2-5% | 0.05-0.1% | -95% a -98% |
| **Refazimento** | 8-12% | 0.5-2% | -85% a -96% |
| **Overhead** | Zero | +500 tokens/sprint | Aceitável |
| **Quando implementar** | Sempre (base) | Depois de Gen/Eval | Progressivo |

**Conclusão:** Gen/Eval é **necessário**. Sprint Contracts são **multiplicador**.

---

## ✅ Checklist de Implementação

### Fase 1: Design (2-3 horas)

- [ ] Identifiquei tipos de sprints na minha aplicação (Discover, Checkout, etc)
- [ ] Para cada tipo de sprint, defini Input Specification
- [ ] Para cada tipo de sprint, defini Success Criteria (testáveis!)
- [ ] Para cada tipo de sprint, defini Failure Handling
- [ ] Criei templates (não contracts únicos)
- [ ] Documentei na forma visual (box com 3 seções)

### Fase 2: Implementation (1-2 dias)

- [ ] Implementar Contract negotiation (Gen propõe, Eval aprova)
- [ ] Implementar Success Criteria como assertions (testes)
- [ ] Implementar Failure Handling (ações específicas)
- [ ] Criar Harness para validações críticas
- [ ] Testar com 5-10 conversas reais
- [ ] Medir erro antes vs depois

### Fase 3: Optimization (1 semana)

- [ ] Refinar criteria baseado em feedback real
- [ ] Identificar failure scenarios mais comuns
- [ ] Ajustar token budget por sprint
- [ ] Documentar lessons learned
- [ ] Treinar equipe em contracts

### Fase 4: Scaling (Contínuo)

- [ ] Criar library de templates (reutilizar)
- [ ] Monitorar error rates em produção
- [ ] Ajustar contracts conforme padrões evoluem
- [ ] Fazer quarterly reviews de performance

---

## ⚠️ Armadilhas Comuns (E Como Evitar)

### Armadilha 1: Contract Muito Vago

**O Problema:**
```
❌ RUIM:
"SUCCESS CRITERIA: Cliente fica feliz"
Por quê: "Feliz" é subjetivo. Como testar?
```

**A Solução:**
```
✅ BOM:
"SUCCESS CRITERIA:
• 3-5 opções encontradas (count)
• TODAS respeitam orçamento (boolean)
• Cada uma tem 50+ caracteres (length)
• Ranking por preço/avaliação (order)"
```

**Como evitar:** Todos os critérios devem ter operadores (>, ==, NOT IN).

---

### Armadilha 2: Contract Muito Rígido

**O Problema:**
```
❌ RUIM:
"EXATAMENTE 5 opções, não mais, não menos"
Por quê: Cliente pode ter requisitos impossíveis.
```

**A Solução:**
```
✅ BOM:
"3-5 opções (faixa, não exato)
FAILURE: Se <3, informar e pedir relaxar"
```

---

### Armadilha 3: Não Revisar Contract Durante Sprint

**O Problema:**
```
❌ RUIM:
Cliente muda requisito mid-sprint. KODA segue contract antigo.
Resultado: Confusão.
```

**A Solução:**
```
✅ BOM:
"FAILURE HANDLING: Se requisitos mudam mid-sprint,
                    generator renegocia novo contract"
```

---

### Armadilha 4: Esquecer "Failure Handling"

**O Problema:**
```
❌ RUIM:
Contract sem Failure Handling.
Generator tira "solução criativa" (ruim).
```

**A Solução:**
```
✅ BOM:
"FAILURE HANDLING:
• Se <3 opções: Informar e pedir relaxar orçamento
• Se cliente mudou: Renegociar contract
• Se alergia esquecida: Rejeitar, refazer"
```

---

### Armadilha 5: Contracts Demais (Paralyzing)

**O Problema:**
```
❌ RUIM:
47 contracts diferentes. Paralisia de escolha.
```

**A Solução:**
```
✅ BOM:
4 templates reutilizáveis com parâmetros.
Se tem >10 contracts, consolidar em templates.
```

---

## 🏗️ Aplicação ao KODA

### Integrando com Generator/Evaluator

**Padrão recomendado:**

```
Generator + Evaluator = Base
Sprint Contracts = Estrutura
Harness = Garantia
Loop = Retry mechanism

FLUXO:
1. Cliente chega
2. KODA propõe Sprint Contract
3. Evaluator aprova
4. Generator executa (Harness)
5. Evaluator valida (Success Criteria)
6. Se falha: Loop ou Failure Handling
7. Se sucesso: Output, próximo sprint
```

### Customer Journey Sprints

```
├─ Sprint 1: Discover (produto certo?)
├─ Sprint 2: Comparison (qual é melhor?)
├─ Sprint 3: Education (como usar?)
├─ Sprint 4: Order (finalizar compra)
├─ Sprint 5: Tracking (seu pedido)
└─ Sprint 6: Support (algo errado?)

Cada sprint = seu contract template
Cliente não vê divisão, só experiência fluida.
```

### Medindo Impacto

**ANTES:**
- Erro rate: 2-5%
- Refazimento: 8-12%
- Customer satisfaction: 7/10
- Churn: 3%

**DEPOIS:**
- Erro rate: 0.05-0.1% (-95%)
- Refazimento: 0.5-2% (-85%)
- Customer satisfaction: 9/10 (+28%)
- Churn: 0.1% (-97%)

---

## 🎯 Próximos Passos

### Exercício Técnico (Arquivo Separado)

```
EXERCÍCIO 1: Design a Sprint Contract (30 min)
EXERCÍCIO 2: Build a Harness (45 min)
EXERCÍCIO 3: Handle a Failure Scenario (30 min)

TOTAL: ~2 horas de prática hands-on
Arquivo: exercise-01_-_02-nivel-2-practical-patterns.md
```

### Como Começar no KODA (Passo a Passo)

```
SEMANA 1: Design
└─ Identifique tipos de sprints (Discover, Checkout)
   └─ Desenhe contract para o mais crítico
   └─ Teste com 3 conversas
   └─ Meça impacto

SEMANA 2: Implementation
└─ Integre com Generator/Evaluator
   └─ Teste com 10 conversas
   └─ Monitore em produção

SEMANA 3: Scaling
└─ Crie templates para todos os sprints
   └─ Treine equipe
   └─ Documentar lessons

SEMANA 4: Optimization
└─ Ajuste criteria
   └─ Retrospectiva com time
```

---

## 📚 Resumo Final

**O QUÊ:** Acordo negociado sobre o que "pronto" significa.

**3 PILARES:**
1. 📥 Input Specification
2. ✅ Success Criteria
3. ⚠️ Failure Handling

**IMPACTO:**
- Erro: -95%
- Refazimento: -85%
- Satisfação: +28%

**3 CASOS KODA:**
1. Discover (15 min)
2. Checkout (10 min)
3. Long Conversation (3.5h)

---

*Padrão Sprint Contracts | Nível 2 | Concluído*

**Você agora tem a arquitetura para conversas de 4+ horas, zero erros, máxima confiança.**

**Próximo: Exercícios práticos. Depois: Nível 3 (Multi-Agent Systems).**
