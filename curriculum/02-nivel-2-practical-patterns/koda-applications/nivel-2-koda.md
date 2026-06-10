---
title: "KODA em Evolução: Padrões Avançados e Refatoração Arquitetural"
type: curriculum-koda-application
nivel: 2
aliases: []
tags: [curriculo-conteudo, nivel-2, koda]
last_updated: 2026-06-10
---
# 🚀 KODA em Evolução: Padrões Avançados e Refatoração Arquitetural
## De um Agente Bom a um Agente Resiliente - Nível 2 em Ação

**Tempo Estimado:** 120-150 minutos  
**Nível:** 2 - Padrões Práticos  
**Pré-requisitos:** Ter completado Nível 1 (nivel-1-koda.md)  
**Status:** 🟡 CRÍTICO - Transformação arquitetural do KODA  
**Data de Criação:** Maio 2026  

---

## 📖 Prólogo: A Evolução do KODA

**Quinta-feira, 14h30. Uma conversa típica do KODA:**

```
Cliente: "Oi KODA! Estou procurando whey protein, mas sou alérgico a amendoim e 
         prefiro sabor de chocolate."
         
KODA: [0.3s] "Perfeito! Encontrei 3 excelentes opções sem amendoim, todas 
       com chocolate. Qual você prefere?"
       
[Conversa fluida por 2 horas...]

Cliente: "Qual era aquele produto que você recomendou mesmo?"

KODA: [Resposta correta, bem formatada, com link de compra]

Cliente: "Ótimo! Comprei."
```

**Resultado:** ✅ Conversa perfeita. Métrica: 1 venda. Taxa de satisfação: 95%. KODA funcionando.

---

**Mas por trás dos bastidores...**

**Sexta-feira, 10h. Reunião de Fernando com o time de engenharia:**

```
Dev Junior: "Fernando, essa feature de busca de produto está quebrada. 
           Um cliente reclamou que recebeu uma recomendação errada."

Fernando: "Qual é o erro? Os specs estão claros..."

Dev: "Exatamente. Os specs estão lá. A validação de harness está lá. 
     Mas algo saiu errado. Não consigo rastrear o quê."

Fernando: [Silêncio]

Dev: "Eu passei 3 horas lendo os logs. Nada. Tentei debugar a conversa. 
     Os dados estão certos no começo, certos no meio... e de repente, errados.
     Como? Por quê? Não tenho ideia."
```

---

**E aqui está o insight que assustou Fernando:**

Seis meses atrás, o time implementou **Nível 1 com perfeição**:

✅ **Problema 1 (Context Amnesia)** → RESOLVIDO com State Persistence
✅ **Problema 2 (Token Budgeting)** → RESOLVIDO com History Compression
✅ **Problema 3 (Weak Harness)** → RESOLVIDO com Validation Layers

**KODA não quebrava mais.**

Mas Fernando notou algo inquietante:

❌ **Problema 4 (Invisibilidade)** → NOVO
- Specs são "perfeitos". Validações passam. Mas desvios acontecem. E ninguém sabe por quê.
- Quando algo falha, é quase impossível rastrear a causa.
- Você pode melhorar uma feature, mas não consegue prever como outras serão afetadas.

❌ **Problema 5 (Custo & Performance Degradação)** → NOVO
- KODA é **lento**. Cada conversa longa custa tokens. Custa dinheiro. Custa latência.
- Conversas que duravam 5 minutos agora levam 30 segundos extras (invisível para usuário, mas real no custo).
- Sem visibilidade sobre *onde* os tokens estão sendo gastos.

---

### A Verdade que Fernando Percebeu

> *"Nós resolvemos os 3 problemas de Nível 1. KODA não quebra mais. Mas agora temos um novo problema: não conseguimos ver o que está acontecendo. Specs são apenas promessas. Validação é apenas uma checkpoint. Mas entre essas checkpoints? Caos invisível."*

### O Gap de Nível 1 para Nível 2

| Dimensão | Nível 1 | Nível 2 |
|----------|---------|---------|
| **KODA quebra?** | ❌ Não (resolvido) | ✅ Ainda não |
| **Você consegue ver por quê?** | ❌ Não | ✅ Sim (novo) |
| **Você consegue prever falhas?** | ❌ Não | ✅ Sim (novo) |
| **Otimizado para custo?** | ❌ Não | ✅ Sim (novo) |
| **Consegue debugar desvios?** | ❌ Não | ✅ Sim (novo) |

---

## O Que Nível 1 Criou (Sem Querer)

Quando você resolve "não quebrar" com harnesses rígidos e validações severas, você cria um efeito colateral:

**O sistema fica obscuro.** 

Specs definem o "happy path". Validações checam pontos críticos. Mas o que acontece *entre* esses pontos? Como os dados fluem? Onde o tempo é gasto? Quais decisões KODA está tomando em cada etapa?

**Nível 1 não responde isso. Nível 2 vai responder.**

---

## Bem-vindo ao Nível 2

Você não vai desaprender Nível 1. Tudo que aprendeu continua crítico:

- ✅ Context Management (ainda essencial)
- ✅ Token Budgeting (ainda essencial)  
- ✅ Harness Patterns (ainda essencial)

**Mas agora, vamos adicionar 4 novos padrões** que transformam KODA de um agente que "não quebra" para um agente que você **consegue entender, debugar, otimizar e melhorar continuamente**:

1. **Generator/Evaluator** → Para gerar múltiplas opções e escolher a melhor
2. **Sprint Contracts** → Para coordenar módulos sem surpresas
3. **Rubric Design** → Para avaliar qualidade, não apenas passar/falhar
4. **Trace Reading** → Para entender exatamente o que aconteceu

---

## A Jornada de Fernando Continua

Fernando não está reclamando. Está inspirado.

> *"Se Nível 1 nos deu uma fundação sólida, Nível 2 nos dá visibilidade. E com visibilidade, temos controle. Com controle, temos liberdade para inovar sem medo."*

Isso é Nível 2.

---

---

## 🎯 Objetivos Deste Módulo

Ao final deste módulo, você será capaz de:

- ✅ **Dominar os 4 Padrões de Nível 2** (Generator/Evaluator, Sprint Contracts, Rubric Design, Trace Reading) e identificar quando usar cada um para resolver problemas específicos do KODA

- ✅ **Redesenhar Arquitetura do KODA** integrando todos os 4 padrões em um plano coerente, entendendo trade-offs e dependências

- ✅ **Diagnosticar e Otimizar** conversas e features do KODA usando trace reading, rubrics e análise de custo/performance para encontrar gargalos invisíveis

- ✅ **Implementar Padrões em Código** através de 4 exercícios práticos: design um generator/evaluator, escrever rubrics, ler traces reais, e refatorar arquitetura

- ✅ **Comunicar Decisões Técnicas** como um expert, documentando escolhas de design usando os conceitos de Nível 2 e preparando o terreno para Nível 3

---

## 📊 O Que Você Vai Aprender (Roadmap Visual)

```
ENTRADA: Você completou Nível 1
  ↓
SEÇÃO 1: Os 4 Padrões (teoria integrada)
  ↓
SEÇÃO 2-5: Cada padrão em profundidade + aplicação KODA
  ↓
SEÇÃO 6: Refatoração arquitetural (juntando tudo)
  ↓
EXERCÍCIOS: 4 desafios práticos
  ↓
SAÍDA: Você é capaz de entender, planejar, e implementar Nível 2
  ↓
PRÓXIMO: Nível 3 (multi-agent systems)
```

---

---

## 🔄 Parte 1: Os 4 Padrões de Nível 2 - Visão Integrada

### O Paradoxo que Nível 1 Não Resolve

Você implementou Nível 1. KODA não quebra. Validações passam. Histórico é comprimido. Tudo parece perfeito.

Mas há um momento em toda conversa longa onde as coisas ficam... nebulosas.

Você não sabe se:
- KODA está gerando a MELHOR opção, ou apenas uma opção válida
- Os componentes do KODA estão alinhados, ou escondendo surpresas
- Uma recomendação é ÓTIMA ou apenas ACEITÁVEL
- Quando algo falha, por QUE falha

**Nível 2 resolve isso com 4 padrões que trabalham juntos.**

Deixa eu mostrar como, rastreando uma conversa real do KODA:

---

## 🚀 A Jornada: Acompanhando Uma Conversa KODA Completa

### PASSO 1: Cliente Pede, KODA Precisa Gerar Opções
**→ Padrão: Generator/Evaluator**

```
CONVERSA REAL:
Cliente: "Quero um whey protein bom. Sou iniciante na musculação, 
         tenho orçamento de R$ 150, e quero algo fácil de preparar."
```

**O Problema sem o padrão:**
KODA diria: "Recomendo o Whey X por R$ 120." Feito. Uma opção.

Mas e se houvesse 5 opções que encaixam perfeitamente? E se uma é melhor que a outra em dimensões diferentes (preço vs qualidade vs praticidade)?

**O Padrão Generator/Evaluator resolve:**
1. **Generator:** Cria 5 opções diferentes que atendem "iniciante, orçamento até R$ 150, fácil de preparar"
2. **Evaluator:** Avalia cada uma contra critérios de qualidade (custo-benefício, avaliações de clientes, praticidade real)
3. **Resultado:** KODA recomenda a MELHOR opção, não apenas uma opção

> **Por que importa:** Se você gera 5 opções e avalia corretamente, você tem 80% de chance de acertar. Se gera 1 opção, tem 20%. Nível 2 é sobre aumentar probabilidade de acerto.

---

### PASSO 2: Sistema Processa, Módulos Precisam se Coordenar
**→ Padrão: Sprint Contracts**

```
INTERNAMENTE NO KODA:

[Módulo 1: BUSCA]
  "Vou procurar 5 wheys que custam até R$ 150"
  ↓
[Módulo 2: RANKING]
  "Vou ordenar essas 5 por melhor custo-benefício"
  ↓
[Módulo 3: FILTRO]
  "Vou remover qualquer uma que não seja fácil de preparar"
  ↓
[Módulo 4: RECOMENDAÇÃO]
  "Vou apresentar a #1 para o cliente"
```

**O Problema sem o padrão:**
- Busca promete "5 produtos até R$ 150" mas às vezes entrega 3
- Ranking promete "ordenação por qualidade" mas às vezes ordena por preço
- Filtro promete "apenas fácil de preparar" mas às vezes deixa produtos complexos
- Recomendação fica confusa: qual é realmente a #1?

**O Padrão Sprint Contracts resolve:**
Cada módulo **escreve uma "promessa"** (contrato) antes de executar:

```
MÓDULO BUSCA: "Vou entregar exatamente [N] produtos, 
               cada um com {produto_id, preço, categoria}"
               
MÓDULO RANKING: "Recebo [lista de produtos], 
                 entrego [mesma lista, ordenada por score 0-100]"
                 
MÓDULO FILTRO: "Recebo [lista ordenada], 
                entrego [lista filtrada, removendo X, Y, Z]"
                
MÓDULO RECOMENDAÇÃO: "Recebo [lista filtrada], 
                      entrego [1 produto + explicação]"
```

Se um módulo não entregar o que prometeu, o sistema SABE, porque há um contrato. Sem contratos, há caos invisível.

> **Por que importa:** Sprint Contracts transformam "espero que funcione" em "PROMETO que funciona". Isso é Nível 2.

---

### PASSO 3: Avaliar Qualidade da Recomendação
**→ Padrão: Rubric Design**

```
MOMENTO CRÍTICO:
KODA recomendou um whey protein. Mas é uma boa recomendação?

Validação (Nível 1) diz: ✅ Passa (preço < R$ 150, fácil de preparar)

Mas rubric (Nível 2) pergunta: É REALMENTE BOM?
  □ Cliente é iniciante? ✅ Sim
  □ Produto é amigável para iniciantes? ⚠️ Talvez (muitas críticas sobre gosto)
  □ Custo-benefício é excelente? ✅ Sim
  □ Disponibilidade em estoque? ✅ Sim
  □ Tempo de entrega aceitável? ❌ 7 dias (cliente pode achar longo)
  
Score: 4/5 = 80% (Bom, não ótimo)
```

**O Problema sem o padrão:**
Nível 1 diz "válido ou inválido". Preto ou branco. Mas qualidade é cinza.

Você pode ter uma recomendação válida mas ruim. Nível 1 não vê. Nível 2 vê.

**O Padrão Rubric Design resolve:**
Cria um "rubric" (rubrica) que avalia múltiplas dimensões:

```
RUBRIC PARA RECOMENDAÇÃO DE WHEY:

DIMENSÃO 1: Adequação ao Perfil (peso 30%)
  5 pontos: Perfeito para esse cliente
  3 pontos: Bom, mas não ideal
  1 ponto:  Marginal

DIMENSÃO 2: Custo-Benefício (peso 25%)
  5 pontos: Melhor custo-benefício da categoria
  3 pontos: Custo-benefício aceitável
  1 ponto:  Caro para o que oferece

DIMENSÃO 3: Satisfação Esperada (peso 25%)
  5 pontos: 90%+ de clientes satisfeitos
  3 pontos: 70%+ de clientes satisfeitos
  1 ponto:  Menos de 70%

DIMENSÃO 4: Viabilidade (peso 20%)
  5 pontos: Em estoque, entrega em 2 dias
  3 pontos: Em estoque, entrega em 5 dias
  1 ponto:  Fora de estoque ou entrega lenta
```

Resultado: Score 82/100. Recomendação é BOM (não excelente). Você sabe.

> **Por que importa:** Rubrics transformam "passou na validação" em "é realmente bom". Sem eles, você recomenda mediocridade com confiança.

---

### PASSO 4: Algo Deu Errado? Trace Reading Diagnóstica
**→ Padrão: Trace Reading**

```
CENÁRIO REAL:
[3 horas depois]
Cliente: "Ué, o produto chegou, mas o gosto é horrível. Por que você recomendou?"

KODA: [Silêncio constrangido]
```

**O Problema sem o padrão:**
Você não tem ideia por quê. Os specs estão lá. Rubric passava. Validação passava. Onde deu errado?

**O Padrão Trace Reading resolve:**
Você "lê o trace" (o registro completo) de como a recomendação foi gerada:

```
TRACE DA RECOMENDAÇÃO:

[14:32:45] Generator criou 5 opções
  └─ Opção A: Whey X (R$ 120) - score 82/100
  └─ Opção B: Whey Y (R$ 115) - score 79/100
  └─ Opção C: Whey Z (R$ 145) - score 85/100  ← Eleita!
  └─ Opção D: Whey W (R$ 95) - score 71/100
  └─ Opção E: Whey V (R$ 140) - score 77/100

[14:32:48] Evaluator avaliou as 5
  └─ Whey Z: 85/100 (melhor score)
  └─ Rubric passou: ✅ Adequação, ✅ Custo, ⚠️ Satisfação (75%), ✅ Viabilidade

[14:32:50] Recomendação gerada
  └─ "Recomendo Whey Z por R$ 145"

[14:32:51] Sprint Contract validado
  └─ Módulo recomendação entregou conforme prometido ✅
```

**DIAGNÓSTICO:**
Ah! A base de dados de "satisfação" estava defasada. Whey Z tinha 75% de satisfação no mês passado, mas clientes novos acham o gosto ruim. Rubric confiou em dados antigos.

**Ação:** Atualizar base de dados. Próximas recomendações serão melhores.

> **Por que importa:** Sem trace reading, você fica cego. Com ele, você consegue ver exatamente onde o problema está e corrigi-lo.

---

## 🔗 A Integração: Como os 4 Padrões Trabalham Juntos

Agora que você viu cada padrão em ação, vamos entender como eles se **coordenam**:

### O Fluxo Integrado

```
CONVERSA CHEGA
    ↓
[GENERATOR/EVALUATOR]
  Gera 5 opções
  Avalia cada uma
  Escolhe a melhor
    ↓
[SPRINT CONTRACTS]
  Cada módulo promete entregar X
  Coordena sem surpresas
  Valida que promessas foram cumpridas
    ↓
[RUBRIC DESIGN]
  Avalia se a opção escolhida é REALMENTE BOA
  Não apenas "válida", mas "excelente"
  Score final: é seguro recomendar?
    ↓
SE SCORE ≥ 80:
  Recomendação é feita com confiança
    ↓
SE SCORE < 80 ou ALGO DEU ERRADO:
  [TRACE READING]
    Lê o trace completo
    Identifica exatamente onde falhou
    Retroalimenta o sistema
```

### As Dependências Críticas

1. **Generator/Evaluator precisa de Sprint Contracts**
   - Se módulos não forem coordenados, a "melhor opção" pode ser baseada em dados inconsistentes

2. **Sprint Contracts precisa de Rubric Design**
   - Contratos garantem que dados fluem corretamente, mas rubrics garantem que a DECISÃO é boa

3. **Rubric Design precisa de Trace Reading**
   - Rubrics avaliam, mas quando falham, você precisa saber por quê

4. **Trace Reading alimenta tudo**
   - Quando você diagnostica um erro, você ajusta generator, contracts, ou rubrics

### O Círculo Virtuoso

```
Semana 1: Implementa Generator/Evaluator
  → Recomendações melhoram de 60% para 75% de acurácia

Semana 2: Adiciona Sprint Contracts
  → Recomendações melhoram para 80%
  → Tempo de resposta cai 30%

Semana 3: Implementa Rubric Design
  → Recomendações melhoram para 87%
  → Você começa a rejeitar recomendações ruins ANTES de fazer

Semana 4: Adiciona Trace Reading
  → Você diagnostica por quê quando falha
  → Ajusta rubrics, contracts, ou generator
  → Semana 5: Recomendações em 92%
```

**Isso é Nível 2.**

---

## 📊 Diagrama: Os 4 Padrões em Orquestração

```
                    ┌─────────────────────────────────────┐
                    │   CLIENTE FAZ PERGUNTA               │
                    └────────────────┬────────────────────┘
                                     │
                    ┌────────────────▼────────────────────┐
                    │ 1. GENERATOR/EVALUATOR              │
                    │ ├─ Gera 5 opções                    │
                    │ ├─ Avalia cada uma                  │
                    │ └─ Escolhe melhor (75% confiança)   │
                    └────────────────┬────────────────────┘
                                     │
                    ┌────────────────▼────────────────────┐
                    │ 2. SPRINT CONTRACTS                 │
                    │ ├─ Valida coordenação entre módulos │
                    │ ├─ Checa promessas cumpridas        │
                    │ └─ Garante dados consistentes       │
                    └────────────────┬────────────────────┘
                                     │
                    ┌────────────────▼────────────────────┐
                    │ 3. RUBRIC DESIGN                    │
                    │ ├─ Avalia qualidade real (5 dims)   │
                    │ ├─ Score 0-100                      │
                    │ └─ Rejeita se < 75? (configurable)  │
                    └────────┬───────────────────┬────────┘
                             │                   │
                    ✅ SCORE ≥ 75    ❌ SCORE < 75
                             │                   │
                    ┌────────▼────────┐   ┌──────▼─────────────┐
                    │ RECOMENDAÇÃO    │   │ 4. TRACE READING   │
                    │ GERADA COM      │   │ ├─ Lê o trace      │
                    │ CONFIANÇA       │   │ ├─ Identifica erro │
                    │                 │   │ └─ Ajusta sistema  │
                    └─────────────────┘   └────────────────────┘
```

---

## 💼 Caso Real: Recomendação Completa em Nível 2

Vamos ver uma recomendação REAL passando pelos 4 padrões:

### O Contexto
- Cliente: João, 28 anos, iniciante em musculação
- Budget: R$ 150
- Preferência: Whey com bom gosto, fácil de preparar
- Histórico: Comprou proteína em pó antes, não gostou (gosto ruim)

### O Fluxo Completo

**[GENERATOR/EVALUATOR]**
```
Generator cria 5 opções:
1. Whey ISO 100 (R$ 140) - Isolado, menos lactose, 90% pureza
2. Whey Gold Standard (R$ 120) - Concentrado, bom custo-benefício, 80% pureza
3. Whey Vegano (R$ 115) - Vegan, diferente, 85% pureza
4. Whey com Carboidrato (R$ 130) - Pós-treino, energia extra, 75% pureza
5. Whey Sabor (R$ 95) - Concentrado com flavorizantes, gosto melhorado

Evaluator avalia cada uma:
1. Score 78 (ótima qualidade, mas caro)
2. Score 82 (excelente custo-benefício) ← ELEITA
3. Score 71 (qualidade OK, mas vegan pode não encaixar para iniciante)
4. Score 74 (bom para pós-treino, mas iniciante não precisa)
5. Score 68 (gosto melhorado, mas qualidade inferior)
```

**[SPRINT CONTRACTS]**
```
Módulo BUSCA entrega:
  ✅ 5 produtos, cada um com {id, nome, preço, pureza, avaliações}

Módulo RANKING entrega:
  ✅ Mesmos 5, ordenados por score de adequação (78, 82, 71, 74, 68)

Módulo FILTRO entrega:
  ✅ Produtos que "bom gosto" e "fácil de preparar"
  ✅ Remove #3 (vegan, talvez complexo para iniciante)
  ✅ Resultado: [#1, #2, #4, #5]

Módulo RECOMENDAÇÃO entrega:
  ✅ 1 produto (#2: Whey Gold Standard) + explicação clara
```

**[RUBRIC DESIGN]**
```
Rubric avalia #2 (Whey Gold Standard):

DIMENSÃO 1: Adequação ao Perfil (peso 30%)
  Score: 5/5 (Iniciante? ✅ Custo ok? ✅ Gosto? ✅ Fácil? ✅)
  Contribui: 1.5/1.5 pontos

DIMENSÃO 2: Custo-Benefício (peso 25%)
  Score: 5/5 (R$ 120 por 2kg, R$ 60/kg - excelente)
  Contribui: 1.25/1.25 pontos

DIMENSÃO 3: Satisfação Esperada (peso 25%)
  Score: 4/5 (91% de avaliações positivas, alguns mencionam "gosto OK, não excelente")
  Contribui: 1.0/1.25 pontos

DIMENSÃO 4: Viabilidade (peso 20%)
  Score: 5/5 (Em estoque, entrega em 2 dias)
  Contribui: 1.0/1.0 pontos

TOTAL: 4.75/5 = 95/100 ✅ EXCELENTE

Decisão: ✅ Recomendar com confiança
```

**[RECOMENDAÇÃO GERADA]**
```
KODA: "João, baseado no que você me contou, recomendo o **Whey Gold Standard 
(R$ 120)**. É feito para iniciantes como você, tem excelente custo-benefício, 
e 91% dos clientes com perfil similar ao seu ficaram satisfeitos. 
Chega em 2 dias. Quer comprar?"
```

**[TUDO CORRE BEM]**
```
Cliente compra, fica satisfeito. ✅

3 meses depois: Cliente volta
"KODA, você acertou na recomendação anterior. Quer me recomendar outro?"

Trace Reading registra:
  ✅ Recomendação #2 (Whey Gold Standard) → Sucesso
  ✅ Rubric score 95/100 foi validado na prática
  → Confiança no rubric aumenta para futuras recomendações
```

---

## 🎯 Resumo: Por Que Nível 2 é Necessário

| Dimensão | Nível 1 | Nível 2 |
|----------|---------|---------|
| **Gera múltiplas opções?** | ❌ Uma opção | ✅ 5 opções, melhor eleita |
| **Módulos coordenados?** | ⚠️ Esperança | ✅ Sprint Contracts |
| **Valida qualidade?** | ❌ Apenas válido/inválido | ✅ Rubric: 0-100 |
| **Diagnostica problemas?** | ❌ "Não sei por quê" | ✅ Trace Reading |
| **Taxa de acurácia** | ~70% | ~90%+ |
| **Custo otimizado?** | ❌ Não | ✅ Trace → ajustes |
| **Você consegue melhorar continuamente?** | ❌ Cego | ✅ Sim, iterando |

---

---

## 💡 Parte 2: Generator/Evaluator em KODA

### A Conversa que Falhou (Sem o Padrão)

```
CLIENTE: "Oi KODA! Sou iniciante em musculação, tenho R$ 200 de budget.
         Qual whey você recomenda?"

KODA: [Pensa por 2 segundos]
      "Recomendo o Whey Gold Standard. R$ 120, excelente custo-benefício,
       91% de avaliações positivas. Quer comprar?"

CLIENTE: "Só esse? Não tem outras opções?"

KODA: "Bem, tecnicamente tem... mas esse é o melhor."

CLIENTE: "Mas e se eu quisesse algo mais premium? Ou mais barato?
         Ou vegan? Você não consegue mostrar opções?"

KODA: "Não, assim é mais simples. Recomendo esse."

[CLIENTE DESAPONTADO]
"Sinto que você não está me ajudando de verdade. Você está apenas
me empurrando uma opção."
```

---

### O Problema: Uma Opção ≠ A Melhor Opção

**A verdade incômoda sobre recomendações em Nível 1:**

Quando KODA recomenda uma opção única, ele está fazendo uma **aposta**.

```
Se KODA recomenda o Whey Gold Standard como "a melhor" para iniciante:
  - E se cliente quisesse algo vegan? (Whey Gold não é)
  - E se cliente quisesse algo com carbo? (Whey Gold é puro)
  - E se cliente quisesse máxima qualidade? (Há opções melhores)
  - E se cliente quisesse máxima economia? (Há mais baratos)

KODA não sabe. Deu uma resposta. Fim.
```

**Consequências:**
- Taxa de satisfação: ~70% (cliente raramente fica 100% satisfeito com 1 opção)
- Sensação: KODA não "entende" que há trade-offs
- Oportunidade perdida: Cliente sente-se empurrado, não consultado

---

### O Padrão: Generator/Evaluator

**Ideia central:** 

> Em vez de gerar UMA opção e esperar que seja perfeita, gere MÚLTIPLAS opções, avalie CADA uma rigorosamente, e escolha a MELHOR de acordo com critérios explícitos.

**Componentes:**

1. **Generator (Gerador):** 
   - Input: Requisição do cliente ("iniciante, R$ 200, qualquer tipo")
   - Output: 5-7 opções diferentes, cada uma representando um trade-off diferente
   - Foco: Criatividade + cobertura de espaço de opções

2. **Evaluator (Avaliador):**
   - Input: As 5-7 opções
   - Output: Score 0-100 para cada uma (baseado em critérios)
   - Foco: Rigor + consistência

3. **Seletor:**
   - Input: Scores de cada opção
   - Output: A opção com melhor score (ou top-3 para o cliente escolher)

---

### Como Generator Trabalha (Python)

```python
def generator_whey_recommendations(client_profile):
    """
    Input: {
        'budget': 200,
        'level': 'iniciante',
        'preferences': ['sabor bom', 'fácil de preparar'],
        'restrictions': ['sem lactose'],
        'priorities': ['qualidade', 'custo-benefício']
    }
    
    Output: [opção1, opção2, opção3, opção4, opção5]
    """
    
    options = []
    
    # OPÇÃO 1: Premium Quality (maior valor absoluto)
    options.append({
        'id': 'whey_premium',
        'name': 'Whey Isolado Premium',
        'price': 180,
        'purity': 95,
        'taste_rating': 4.8,
        'lactose_free': True,
        'reasoning': 'Máxima qualidade + sem lactose. Valor alto.'
    })
    
    # OPÇÃO 2: Best Value (melhor custo-benefício)
    options.append({
        'id': 'whey_value',
        'name': 'Whey Gold Standard',
        'price': 120,
        'purity': 80,
        'taste_rating': 4.5,
        'lactose_free': False,
        'reasoning': 'Excelente custo-benefício. Popular.'
    })
    
    # OPÇÃO 3: Budget-Friendly (menor preço)
    options.append({
        'id': 'whey_budget',
        'name': 'Whey Concentrado Basic',
        'price': 80,
        'purity': 75,
        'taste_rating': 3.8,
        'lactose_free': False,
        'reasoning': 'Menor preço. Cumpre o básico.'
    })
    
    # OPÇÃO 4: Vegan Alternative
    options.append({
        'id': 'whey_vegan',
        'name': 'Proteína Vegetal Premium',
        'price': 140,
        'purity': 85,
        'taste_rating': 4.2,
        'lactose_free': True,
        'reasoning': 'Alternativa plant-based. Boa qualidade.'
    })
    
    # OPÇÃO 5: Extreme Value (melhor para iniciante)
    options.append({
        'id': 'whey_starter',
        'name': 'Whey Starter Pack',
        'price': 90,
        'purity': 78,
        'taste_rating': 4.6,  # Sabor otimizado para iniciante
        'lactose_free': True,
        'reasoning': 'Design para iniciante. Sabor agradável.'
    })
    
    return options
```

**O que o Generator fez:**
- ✅ Gerou 5 opções DIFERENTES (não 5 variações da mesma coisa)
- ✅ Cada uma representa um trade-off diferente (quality vs cost vs taste vs ethics)
- ✅ Cobriu o espaço de soluções possíveis
- ✅ Cada opção tem "reasoning" (por que esta opção existe)

---

### Como Evaluator Trabalha (Python)

```python
def evaluator_score_options(options, client_profile):
    """
    Input: 5 opções + perfil do cliente
    Output: Cada opção com score 0-100
    
    Critérios de avaliação:
    1. Adequação ao Perfil (peso 35%)
    2. Custo-Benefício (peso 30%)
    3. Qualidade Absoluta (peso 20%)
    4. Viabilidade/Estoque (peso 15%)
    """
    
    scored_options = []
    
    for option in options:
        # CRITÉRIO 1: Adequação ao Perfil (35%)
        adequacy_score = 0
        if client_profile['level'] == 'iniciante':
            # Iniciante precisa de sabor bom
            adequacy_score += option['taste_rating'] * 20  # Max 20
            # Iniciante precisa de fácil de preparar
            adequacy_score += 5  # Assume todos são fáceis
            # Restrição: sem lactose
            if option['lactose_free'] and 'sem lactose' in client_profile['restrictions']:
                adequacy_score += 10
        
        adequacy_final = min(adequacy_score, 35)  # Max 35 pontos
        
        # CRITÉRIO 2: Custo-Benefício (30%)
        # Razão: preço vs pureza
        cost_benefit_ratio = option['purity'] / option['price']
        # Normalizar para 0-30
        max_ratio = max([o['purity']/o['price'] for o in options])
        cost_benefit_score = (cost_benefit_ratio / max_ratio) * 30
        
        # CRITÉRIO 3: Qualidade Absoluta (20%)
        # Simplesmente: % de pureza
        quality_score = (option['purity'] / 100) * 20
        
        # CRITÉRIO 4: Viabilidade (15%)
        # Assume todos em estoque, entrega em 2 dias
        viability_score = 15
        
        # TOTAL
        total_score = (adequacy_final + cost_benefit_score + 
                      quality_score + viability_score)
        
        scored_options.append({
            'option': option,
            'breakdown': {
                'adequacy': adequacy_final,
                'cost_benefit': cost_benefit_score,
                'quality': quality_score,
                'viability': viability_score
            },
            'total_score': round(total_score, 1)
        })
    
    # Ordenar por score
    scored_options.sort(key=lambda x: x['total_score'], reverse=True)
    
    return scored_options

# Exemplo de output:
# [
#   {'option': whey_premium, 'total_score': 88.5},
#   {'option': whey_starter, 'total_score': 85.2},
#   {'option': whey_value, 'total_score': 79.3},
#   ...
# ]
```

**O que o Evaluator fez:**
- ✅ Avaliou cada opção contra critérios EXPLÍCITOS
- ✅ Pesou critérios de acordo com importância
- ✅ Gerou scores comparáveis (0-100)
- ✅ Mostrou breakdown (qual critério levantou/baixou o score)

---

### Coordenação: Generator + Evaluator

```
FLUXO:

[1. GENERATOR]
   Cliente: "Quero whey para iniciante, R$ 200"
   ↓
   Generator: "Criei 5 opções (premium, value, budget, vegan, starter)"
   ↓
[2. EVALUATOR]
   Evaluator: "Avaliando as 5..."
   ↓
   Scores: starter=85.2, premium=88.5, value=79.3, vegan=76.1, budget=71.8
   ↓
[3. SELETOR]
   Top-1: Premium (88.5)
   Top-3: [Premium, Starter, Value]
   ↓
[4. RESPOSTA]
   KODA: "Criei 5 opções para você:
         
         🥇 #1 (Minha recomendação): Whey Isolado Premium
            Score: 88.5/100
            Por quê: Máxima qualidade + sem lactose + bom sabor
            Preço: R$ 180
         
         🥈 #2 (Alternativa ótima): Whey Starter Pack
            Score: 85.2/100
            Por quê: Sabor otimizado para iniciante + sem lactose
            Preço: R$ 90
         
         🥉 #3 (Melhor custo-benefício): Whey Gold Standard
            Score: 79.3/100
            Por quê: Excelente valor, muito popular
            Preço: R$ 120
         
         Qual você prefere?"
```

---

### Implementação KODA (Claude API)

```python
from anthropic import Anthropic

client = Anthropic()

def generator_evaluator_pipeline(client_request):
    """
    Pipeline completo: Generator → Evaluator → Resposta
    Usando Claude API com function_calling
    """
    
    # PASSO 1: Generator (Claude com structured_outputs)
    generator_response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1000,
        messages=[{
            "role": "user",
            "content": f"""
            Você é um gerador de opções de produtos.
            Requisição: {client_request}
            
            Gere 5 opções DIFERENTES de whey protein que atendem essa requisição.
            Cada opção deve ter:
            - nome
            - preço
            - pureza (%)
            - avaliação de sabor (1-5)
            - sem lactose? (sim/não)
            - reasoning: por que esta opção existe?
            
            Responda em JSON.
            """
        }],
        temperature=1.0  # Criatividade
    )
    
    options = json.loads(generator_response.content[0].text)
    
    # PASSO 2: Evaluator (Claude com critérios estruturados)
    evaluator_response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1500,
        messages=[
            {
                "role": "user",
                "content": f"""
                Você é um avaliador de qualidade.
                
                Opções para avaliar:
                {json.dumps(options, indent=2)}
                
                Perfil do cliente:
                {client_request}
                
                Avalie cada opção em 4 dimensões:
                1. Adequação ao Perfil (35%)
                2. Custo-Benefício (30%)
                3. Qualidade Absoluta (20%)
                4. Viabilidade (15%)
                
                Para cada opção, retorne:
                - scores por dimensão
                - score total (0-100)
                - justificativa breve
                
                Responda em JSON, ordenado por score decrescente.
                """
            }
        ],
        temperature=0.2  # Rigor
    )
    
    scored_options = json.loads(evaluator_response.content[0].text)
    
    # PASSO 3: Gerar resposta para cliente
    top_3 = scored_options[:3]
    
    response = f"""
    Criei {len(options)} opções para você:
    
    🥇 Top Recomendação: {top_3[0]['name']}
    Score: {top_3[0]['score']}/100
    Justificativa: {top_3[0]['justification']}
    Preço: R$ {top_3[0]['price']}
    
    🥈 Alternativa: {top_3[1]['name']}
    Score: {top_3[1]['score']}/100
    
    🥉 Terceira opção: {top_3[2]['name']}
    Score: {top_3[2]['score']}/100
    
    Qual você prefere?
    """
    
    return response, scored_options

# USO:
resultado = generator_evaluator_pipeline(
    "Iniciante, orçamento R$ 200, sem lactose, bom sabor"
)
```

**Pontos-chave:**
- ✅ Generator usa `temperature=1.0` (criativo, gera opções diferentes)
- ✅ Evaluator usa `temperature=0.2` (rigoroso, scores consistentes)
- ✅ Ambos usam structured_outputs (respostas em JSON)
- ✅ Pipeline é orquestrável (pode adicionar mais passos)

---

### Trade-offs: Custo vs Benefício

**CUSTO:**
- Generator: 1 chamada Claude API (~1500 tokens)
- Evaluator: 1 chamada Claude API (~2000 tokens)
- Total: ~3500 tokens por recomendação
- Comparado com Nível 1 (~500 tokens): **7x mais caro**

**BENEFÍCIO:**
- Taxa de acurácia sobe: 65% → 87%
- Satisfação do cliente: "sinto que você me consultou, não empurrou"
- Custo por venda bem-sucedida: cai em ~60% (mais vendas, custo normalizado)
- Retenção: clientes voltam porque se sentiram consultados

**Resultado:**
```
Cenário Nível 1:
  100 recomendações = 65 vendas = R$ 7.800 (assume R$ 120/venda)
  Custo: 100 * 500 tokens = 50.000 tokens = R$ 2,50

Cenário Nível 2 (Gen/Eval):
  100 recomendações = 87 vendas = R$ 10.440
  Custo: 100 * 3500 tokens = 350.000 tokens = R$ 17,50
  
  Lucro Nível 1: R$ 7.800 - R$ 2,50 = R$ 7.797,50
  Lucro Nível 2: R$ 10.440 - R$ 17,50 = R$ 10.422,50
  
  Delta: +R$ 2.625 (+33% de lucro)
```

---

## 📚 Exercício 1: Generator/Evaluator - Perguntas Conceituais

Responda as perguntas abaixo. Use 2-3 frases por resposta.

**Q1: Por que gerar múltiplas opções e depois avaliar é melhor que "pensar e recomendar uma"?**

[Seu espaço para responder]

---

**Q2: No código do Generator, por que cada opção tem um "reasoning" (justificativa)?**

[Seu espaço para responder]

---

**Q3: Se o Generator criou 5 opções e o Evaluator avaliou todas com scores entre 71-88, o Evaluator deve recomendar APENAS a #1 (score 88) para o cliente?**

[Seu espaço para responder]

---

**Q4: Imagine que o Evaluator rodou 2 vezes (rodada 1 e 2) para as mesmas 5 opções. Na rodada 1, a opção A recebeu score 82. Na rodada 2, score 75. O que isso indica?**

A) O Evaluator está quebrado
B) O Evaluator foi ajustado entre rodadas
C) As opções mudaram
D) Nenhuma das acima

[Sua resposta e justificativa]

---

**Q5: O padrão Generator/Evaluator SEMPRE precisa de 5+ opções? Ou poderia funcionar com 2-3?**

[Seu espaço para responder]

---

**Q6: No caso KODA real, qual é a diferença entre o Evaluator passando uma opção com score 88/100 e a validação de Nível 1 passando um harness check?**

[Seu espaço para responder]

---

**Q7 (Bonus): Se você estivesse implementando Generator/Evaluator no KODA agora, qual seria o MAIOR desafio técnico? (Custo? Latência? Definir critérios? Outro?)**

[Seu espaço para responder]

---

### ✅ Padrão Dominado?

Se conseguiu responder todas com 80%+ de acurácia conceitual, você entendeu Generator/Evaluator.

**Próxima:** Seção 3 - Sprint Contracts (coordenação entre módulos)

---

---

## 📋 Parte 3: Sprint Contracts em KODA

### A Conversa que Falhou (Módulos Desalinhados)

```
INTERNAMENTE NO KODA (Nível 1, sem contratos):

[14:32:45.000] CLIENTE envia requisição
  Input: "Quero whey protein, iniciante, orçamento R$ 200"

[14:32:46.100] MÓDULO A (BUSCA) processa
  Lógica: "Vou buscar todos os wheys até R$ 200"
  Output: [5 produtos com {id, nome, preço}]
  Entrega ao Módulo B

[14:32:46.500] MÓDULO B (RANKING) recebe
  Lógica: "Espera, eu esperava receber {id, nome, preço, avaliacao, marca}"
  Avaliacao? Marca? Não tem!
  Ranking fica quebrado.
  Tenta continuar mesmo assim...
  Output: [5 produtos, ordenados "errado" por falta de dados]

[14:32:47.200] MÓDULO C (FILTRO) recebe
  Lógica: "Espera, esses produtos não têm o campo 'categoria'"
  Queria filtrar por "sem lactose" mas não tem esse campo!
  Pula o filtro silenciosamente.
  Output: [5 produtos, incluindo 1 COM lactose]

[14:32:48.000] MÓDULO D (RECOMENDAÇÃO) recebe
  Dados inconsistentes. Alguns têm campos extras, alguns não.
  Formato variável. Tipos de dados incertos.
  Output: "Recomendo Whey Y" (e era COM lactose, contraindicado)

[14:32:48.500] CLIENTE recebe e FICA INSATISFEITO
  "Por que recomendou algo com lactose se disse que era sem?"
```

**O que aconteceu?**
- Módulo A não "prometeu" que entregaria {id, nome, preço, avaliacao, marca}
- Módulo B não "prometeu" que passaria dados com {categoria}
- Módulo C não "prometeu" validar a restrição "sem lactose"
- Cada módulo fez o que achou que deveria fazer
- Resultado: caos silencioso

---

### O Problema: Módulos Surpresos

**A verdade sobre módulos sem contratos:**

```
Cada módulo tem uma EXPECTATIVA sobre o que vai receber:
  Módulo B espera: {id, nome, preço, avaliacao, marca}
  Mas Módulo A entrega: {id, nome, preço}
  
  → SURPRESA! ❌

Cada módulo tem uma RESPONSABILIDADE sobre o que deve entregar:
  Módulo C deveria garantir: "apenas produtos sem lactose"
  Mas Módulo C tem um BUG e deixa passar 1 com lactose
  
  → SURPRESA! ❌
  
Ninguém sabe disso porque não há "promessa escrita".
```

**Consequências:**
- Bugs silenciosos (sistema "funciona" mas entrega errado)
- Difícil debugar (qual módulo falhou?)
- Mudanças quebram sistema (ajusta Módulo A? Quebra Módulo B)
- Medo de refatorar (não sabe o que vai quebrar)

---

### O Padrão: Sprint Contracts

**Ideia central:**

> Cada módulo **escreve uma promessa** (contrato) que diz: "Se você me der X (input), EU GARANTO que vou entregar Y (output) com essas propriedades Z (garantias)."

**Componentes:**

1. **Input Contract:** "O que eu espero receber"
2. **Output Contract:** "O que eu prometo entregar"
3. **Guarantees:** "Propriedades que sempre vão ser verdade"
4. **Validation:** "Como você verifica que eu cumpri?"

**Exemplo KODA:**

```json
{
  "module": "SEARCH_PRODUCTS",
  
  "input_contract": {
    "type": "object",
    "required": ["budget_max", "restrictions"],
    "properties": {
      "budget_max": {
        "type": "number",
        "description": "Máximo de preço em R$"
      },
      "restrictions": {
        "type": "array",
        "items": {"type": "string"},
        "description": "Ex: ['sem lactose', 'vegan']"
      }
    }
  },
  
  "output_contract": {
    "type": "array",
    "items": {
      "type": "object",
      "required": ["id", "name", "price", "rating", "brand", "category"],
      "properties": {
        "id": {"type": "string"},
        "name": {"type": "string"},
        "price": {"type": "number", "minimum": 0},
        "rating": {"type": "number", "minimum": 0, "maximum": 5},
        "brand": {"type": "string"},
        "category": {"type": "string"},
        "lactose_free": {"type": "boolean"}
      }
    }
  },
  
  "guarantees": [
    "Todos os produtos têm price <= budget_max",
    "Número de produtos retornados >= 3 e <= 10",
    "Todos os campos obrigatórios preenchidos (nunca null)",
    "Sem duplicatas (todos IDs únicos)"
  ]
}
```

**O que o contrato diz:**
- ✅ "Espero receber: {budget_max, restrictions}"
- ✅ "Prometo entregar: array de produtos com {id, name, price, rating, brand, category, ...}"
- ✅ "Garanto que: todos respeitam budget, retorno 3-10 itens, sem nulls, sem duplicatas"

---

### Como Contracts Funcionam (Arquitetura)

```
FLUXO COM CONTRATOS:

[CLIENTE faz requisição]
    ↓
[MÓDULO A - SEARCH]
    Valida: "Requisição atende input_contract?"
    Se não: Rejeita com erro claro
    Se sim: Processa
    Valida: "Meu output atende output_contract?"
    Se não: Lança exceção (nunca entrega algo quebrado)
    Se sim: Entrega
    ↓
[MÓDULO B - RANKING]
    Valida: "Recebido atende input_contract de RANKING?"
    Garante: SEARCH prometeu esses campos? ✅ Sim
    Confia nos dados e processa
    Valida: "Meu output atende output_contract?"
    Entrega
    ↓
[MÓDULO C - FILTRO]
    Valida: "Recebido atende input_contract de FILTRO?"
    Se não: ERRO! SEARCH quebrou seu contrato!
    Falha rápido, não silenciosamente
    ↓
[MÓDULO D - RECOMENDAÇÃO]
    Recebe dados validados
    Confia nos dados
    Entrega recomendação confiável
    ↓
[CLIENTE satisfeito]
```

---

### Implementação KODA (Python com Pydantic)

```python
from pydantic import BaseModel, validator, Field
from typing import List, Optional
import json

# DEFINIR CONTRATOS COMO CLASSES PYDANTIC

class SearchProductsInput(BaseModel):
    """Input Contract para SEARCH"""
    budget_max: float = Field(..., gt=0, description="Máximo de preço")
    restrictions: List[str] = Field(
        default=[],
        description="Restrições (sem lactose, vegan, etc)"
    )
    level: str = Field(..., description="Iniciante/Intermediário/Avançado")

    @validator('budget_max')
    def budget_must_be_reasonable(cls, v):
        if v < 50 or v > 1000:
            raise ValueError('Budget deve estar entre R$ 50 e R$ 1000')
        return v


class ProductOutput(BaseModel):
    """Estrutura de CADA PRODUTO no output"""
    id: str
    name: str
    price: float = Field(..., ge=0)
    rating: float = Field(..., ge=0, le=5)
    brand: str
    category: str
    lactose_free: bool
    vegan: bool
    availability_days: int = Field(..., ge=1, le=30)
    
    @validator('price')
    def price_positive(cls, v):
        if v <= 0:
            raise ValueError('Preço deve ser positivo')
        return v


class SearchProductsOutput(BaseModel):
    """Output Contract para SEARCH"""
    products: List[ProductOutput] = Field(
        ...,
        min_items=3,
        max_items=10,
        description="3-10 produtos"
    )
    
    @validator('products')
    def no_duplicates(cls, v):
        ids = [p.id for p in v]
        if len(ids) != len(set(ids)):
            raise ValueError('Não pode haver produtos duplicados')
        return v
    
    @validator('products')
    def all_within_budget(cls, v, values):
        # Acesso ao budget_max da input (se tiver)
        # Aqui simplificado: apenas exemplo
        return v


# IMPLEMENTAR O MÓDULO SEARCH

class SearchModule:
    """Módulo que respeita contrato"""
    
    def execute(self, input_request: dict) -> dict:
        """
        1. Valida input contra contrato
        2. Processa
        3. Valida output contra contrato
        4. Retorna garantindo que contrato foi cumprido
        """
        
        # PASSO 1: Validar Input
        try:
            validated_input = SearchProductsInput(**input_request)
            print("✅ Input válido contra contrato")
        except ValueError as e:
            print(f"❌ Input INVÁLIDO: {e}")
            raise
        
        # PASSO 2: Processar
        raw_products = self._search_database(
            budget=validated_input.budget_max,
            restrictions=validated_input.restrictions
        )
        
        # PASSO 3: Validar Output
        try:
            output = SearchProductsOutput(products=raw_products)
            print(f"✅ Output válido contra contrato ({len(output.products)} produtos)")
        except ValueError as e:
            print(f"❌ Output INVÁLIDO: {e}")
            print("  → Módulo SEARCH não cumpriu seu contrato!")
            raise
        
        # PASSO 4: Retornar (garantindo que contrato foi cumprido)
        return output.dict()
    
    def _search_database(self, budget, restrictions):
        """Implementação real (simplificada)"""
        # Busca 5 produtos
        products = [
            ProductOutput(
                id="whey_1",
                name="Whey Gold Standard",
                price=120,
                rating=4.5,
                brand="Gold Nutrition",
                category="Whey Concentrado",
                lactose_free=False,
                vegan=False,
                availability_days=2
            ),
            ProductOutput(
                id="whey_2",
                name="Whey Isolado Premium",
                price=180,
                rating=4.8,
                brand="Premium Proteins",
                category="Whey Isolado",
                lactose_free=True,
                vegan=False,
                availability_days=2
            ),
            # ... 3 mais
        ]
        return products


# USO:

search = SearchModule()

# Input que respeita contrato
valid_input = {
    'budget_max': 200,
    'restrictions': ['sem lactose'],
    'level': 'iniciante'
}

result = search.execute(valid_input)
# ✅ Garantia: output respeita contrato SearchProductsOutput

# Input que NÃO respeita contrato
invalid_input = {
    'budget_max': 10000,  # Fora do range [50, 1000]
    'restrictions': 'sem lactose',  # Deveria ser array
    'level': 'iniciante'
}

result = search.execute(invalid_input)
# ❌ Erro claro: "Input INVÁLIDO: Budget deve estar entre R$ 50 e R$ 1000"
```

**Pontos-chave:**
- ✅ Input e Output são **classes Pydantic** (contratos!)
- ✅ Validação acontece em DOIS lugares: entrada e saída
- ✅ Se contrato quebra, erro é CLARO e RASTREÁVEL
- ✅ Módulo nunca entrega algo que não promete
- ✅ Módulos podem confiar nos dados que recebem

---

### Validação de Contratos (Checklist)

Quando um módulo recebe dados de outro, ele valida:

```python
def ranking_module_validate_input(products_from_search):
    """
    RANKING espera receber output de SEARCH.
    Valida se atende o contrato SearchProductsOutput.
    """
    
    # Validação 1: Estrutura
    assert isinstance(products_from_search, list), \
        "❌ Esperava array, recebi: " + str(type(products_from_search))
    
    assert len(products_from_search) >= 3, \
        f"❌ Esperava 3-10 produtos, recebi: {len(products_from_search)}"
    
    # Validação 2: Campos obrigatórios
    required_fields = ['id', 'name', 'price', 'rating', 'brand', 'category']
    for product in products_from_search:
        for field in required_fields:
            assert field in product, \
                f"❌ Campo obrigatório '{field}' faltando em: {product}"
            assert product[field] is not None, \
                f"❌ Campo '{field}' é null em: {product['id']}"
    
    # Validação 3: Tipos e ranges
    for product in products_from_search:
        assert isinstance(product['price'], (int, float)), \
            f"❌ 'price' deve ser número, é {type(product['price'])}"
        assert 0 <= product['rating'] <= 5, \
            f"❌ 'rating' deve estar entre 0-5, é {product['rating']}"
    
    # Validação 4: Sem duplicatas
    ids = [p['id'] for p in products_from_search]
    assert len(ids) == len(set(ids)), \
        "❌ Há produtos duplicados nos IDs"
    
    print("✅ Input de SEARCH atende contrato SearchProductsOutput")
    return True
```

**O benefício:**
Se SEARCH entrega algo errado, RANKING **SABE IMEDIATAMENTE** e falha rápido, em vez de produzir um ranking silenciosamente quebrado.

---

### Trade-offs: Overhead vs Confiabilidade

**CUSTO:**
- Escrever contratos (JSONSchema/Pydantic): ~2 horas por módulo
- Validação em entrada/saída: ~5-10% overhead de latência
- Manutenção: se contrato muda, precisa atualizar validações

**BENEFÍCIO:**
- Bugs silenciosos: reduz em ~85%
- Tempo de debug: reduz em ~70% (sabe exatamente o módulo que falhou)
- Segurança refatoração: pode mudar Módulo A sem medo de quebrar Módulo B
- Confiança: você SABE que dados entre módulos são válidos

**Resultado:**
```
Sem Contracts:
  Bug silencioso aparece 3 dias depois em produção
  Leva 8 horas para debugar qual módulo falhou
  Custo: 8h dev + possível perda de cliente

Com Contracts:
  Erro aparece DURANTE TESTE (antes de produção)
  Sabe exatamente qual módulo falhou
  Custo: 2h setup + 0,5h debug quando acontece algo inesperado
  Economia: ~7 horas por incidente
```

---

## 📚 Exercício 2: Sprint Contracts - Perguntas Conceituais

**Q1: Por que contratos precisam existir TANTO na entrada quanto na saída de um módulo?**

[Seu espaço para responder]

---

**Q2: No exemplo KODA, o contrato de SEARCH promete "Número de produtos retornados >= 3 e <= 10". Por que não prometer sempre exatamente 5?**

[Seu espaço para responder]

---

**Q3: Se você está implementando um novo módulo FILTRO que recebe output de SEARCH, qual é o primeiro passo antes de escrever uma linha de código?**

A) Escrever o input_contract baseado no output_contract de SEARCH
B) Implementar a lógica de filtro
C) Começar a testar

[Sua resposta com justificativa]

---

**Q4: No código Pydantic mostrado, a validação de input acontece dentro do método `execute()`. Por que não deixar a validação implícita (só ao criarto objeto SearchProductsInput)?**

[Seu espaço para responder]

---

**Q5: Você está mudando SEARCH para também retornar um campo novo: "availability_in_store" (disponível em loja física?). Quais módulos precisam ser atualizados para não quebrar?**

[Seu espaço para responder]

---

**Q6: O contrato é uma "promessa". Mas o que acontece se um módulo recebe dados válidos contra seu input_contract, processa, mas por BUG INTERNO, entrega algo que não respeita seu output_contract?**

[Seu espaço para responder]

---

**Q7 (Bonus): Em um sistema com 10 módulos encadeados (A → B → C → ... → J), qual é a vantagem de ter contratos comparado a "cada um faz o que achar melhor"?**

[Seu espaço para responder]

---

### ✅ Padrão Dominado?

Se conseguiu responder com 80%+ de clareza sobre input/output/validação, você entendeu Sprint Contracts.

**Próxima:** Seção 4 - Rubric Design (avaliar qualidade, não apenas validar)

---

---

## ⭐ Parte 4: Rubric Design em KODA

### A Conversa que Falhou (Validação Passou, Mas foi Ruim)

```
CENÁRIO:

CLIENTE: "Oi KODA, quero whey para iniciante, R$ 100"

KODA: [Processa com Generator/Evaluator]
      Gera 5 opções
      Evaluator score cada uma
      Eleita: Whey Budget Basic (R$ 85)
      
      [Com Nível 1, só faz validação]
      ✅ Preço <= R$ 100? Sim (R$ 85)
      ✅ Fácil de preparar? Sim
      ✅ Categoria existe? Sim
      [PASSA NA VALIDAÇÃO]
      
KODA: "Recomendo Whey Budget Basic, R$ 85. Ótimo preço!"

CLIENTE: [3 dias depois recebe produto]
         Abre a embalagem. Gosto HORRÍVEL.
         Avalia 1 estrela. Pede reembolso.

KODA: [Silêncio constrangido]
```

**O que aconteceu?**
- ✅ Validação passou (preço certo, categoria certa, em estoque)
- ❌ Mas recomendação foi RUIM (gosto horrível, apenas 2.5 de avaliação)

**Nível 1 não vê isso. Nível 2 (com Rubric) teria rejeitado a recomendação.**

---

### O Problema: Validação ≠ Qualidade

**A diferença crítica:**

```
VALIDAÇÃO (Nível 1):
  "Essa recomendação é VÁLIDA?"
  ✅ Sim ou ❌ Não
  Resposta binária.

QUALIDADE (Nível 2 com Rubric):
  "Essa recomendação é ÓTIMA?"
  Score: 35/100 (Ruim), 75/100 (Bom), 92/100 (Excelente)
  Resposta em escala.
```

**Exemplo KODA:**

```
Whey Budget Basic:
  ✅ Preço <= R$ 100? Sim (VALIDA)
  ✅ Sem lactose? Sim (VALIDA)
  ✅ Em estoque? Sim (VALIDA)
  
  Validação: ✅ PASSA
  
  Mas rubric avalia:
  • Gosto (avaliações de clientes): 2.5/5 ⚠️ RUIM
  • Adequação para iniciante: 3/5 ⚠️ FRACO
  • Custo-benefício: 4/5 ✅ BOM
  • Disponibilidade: 5/5 ✅ BOM
  
  Score Rubric: 56/100 ❌ REJEITA
```

---

### O Padrão: Rubric Design

**Ideia central:**

> Um Rubric é um **scoring system multi-dimensional** que avalia qualidade em MÚLTIPLAS DIMENSÕES (não apenas passa/falha), com pesos, critérios explícitos, e um score final que diz se é seguro recomendar.

**Componentes:**

1. **Dimensões:** "O que vou avaliar?" (gosto, qualidade, preço, disponibilidade)
2. **Escala:** "Como vou medir?" (1-5, 0-100, etc)
3. **Pesos:** "Quanto cada dimensão importa?" (30%, 25%, 25%, 20%)
4. **Threshold:** "A partir de que score eu rejeito?" (< 70 = rejeita)

---

### Como Rubric Funciona (Python)

```python
from dataclasses import dataclass
from typing import List, Dict
import json

@dataclass
class RubricDimension:
    """Uma dimensão do rubric"""
    name: str
    weight: float  # 0.0 a 1.0 (ex: 0.30 = 30%)
    max_score: float  # Máximo possível (ex: 5.0)
    threshold: float  # Mínimo aceitável (ex: 3.0)
    description: str


class ProductRubric:
    """Rubric para avaliar qualidade de recomendação de whey"""
    
    def __init__(self):
        self.dimensions = [
            RubricDimension(
                name="Taste Quality",
                weight=0.35,  # 35% do peso
                max_score=5.0,
                threshold=3.0,
                description="Avaliação de gosto por clientes (1-5 stars)"
            ),
            RubricDimension(
                name="Beginner Friendliness",
                weight=0.25,  # 25%
                max_score=5.0,
                threshold=3.0,
                description="Quão fácil é para iniciante usar (1-5)"
            ),
            RubricDimension(
                name="Cost Benefit",
                weight=0.25,  # 25%
                max_score=5.0,
                threshold=2.5,
                description="Custo vs valor entregue (1-5)"
            ),
            RubricDimension(
                name="Availability",
                weight=0.15,  # 15%
                max_score=5.0,
                threshold=4.0,
                description="Estoque + entrega rápida (1-5)"
            ),
        ]
        
        # Validar que pesos somam 1.0
        total_weight = sum(d.weight for d in self.dimensions)
        assert abs(total_weight - 1.0) < 0.01, \
            f"Pesos devem somar 1.0, somaram {total_weight}"
    
    def evaluate_product(self, product: dict) -> dict:
        """
        Avalia um produto contra o rubric.
        
        Input: {
            'id': 'whey_1',
            'name': 'Whey X',
            'taste_rating': 2.5,  # 1-5
            'beginner_friendly': 3.0,  # 1-5
            'cost_benefit_score': 4.0,  # 1-5
            'availability_score': 5.0,  # 1-5
        }
        
        Output: {
            'product_id': 'whey_1',
            'dimension_scores': {...},
            'final_score': 75.3,
            'recommendation': 'ACCEPT' or 'REJECT',
            'reasoning': '...'
        }
        """
        
        scores = {}
        weighted_sum = 0
        
        # Avaliar cada dimensão
        for dim in self.dimensions:
            # Pegar score da dimensão
            field_name = dim.name.lower().replace(' ', '_')
            if field_name + '_score' in product:
                raw_score = product[field_name + '_score']
            elif field_name + '_rating' in product:
                raw_score = product[field_name + '_rating']
            else:
                raw_score = 0
                print(f"⚠️ Campo '{field_name}' não encontrado em produto")
            
            # Checar threshold
            passes_threshold = raw_score >= dim.threshold
            
            # Normalizar score para 0-100
            normalized_score = (raw_score / dim.max_score) * 100
            
            # Aplicar peso
            weighted_score = normalized_score * dim.weight
            weighted_sum += weighted_score
            
            scores[dim.name] = {
                'raw_score': raw_score,
                'normalized': round(normalized_score, 1),
                'weight': dim.weight,
                'weighted_contribution': round(weighted_score, 1),
                'passes_threshold': passes_threshold
            }
        
        # Score final (0-100)
        final_score = round(weighted_sum, 1)
        
        # Decisão: rejeitar se QUALQUER dimensão cai abaixo do threshold
        all_pass_threshold = all(
            scores[dim.name]['passes_threshold'] 
            for dim in self.dimensions
        )
        
        # OU rejeitar se score final < 70
        recommendation = 'ACCEPT' if (all_pass_threshold and final_score >= 70) else 'REJECT'
        
        # Montar reasoning
        failures = [
            f"{dim.name} ({scores[dim.name]['raw_score']}/{dim.max_score})"
            for dim in self.dimensions
            if not scores[dim.name]['passes_threshold']
        ]
        
        if failures:
            reasoning = f"Rejeitado: {', '.join(failures)} ficaram abaixo do threshold"
        elif final_score < 70:
            reasoning = f"Rejeitado: score final {final_score} abaixo de 70"
        else:
            reasoning = f"Aceito: todas as dimensões passaram, score {final_score}"
        
        return {
            'product_id': product.get('id', 'unknown'),
            'product_name': product.get('name', 'unknown'),
            'dimension_scores': scores,
            'final_score': final_score,
            'recommendation': recommendation,
            'reasoning': reasoning
        }


# USO:

rubric = ProductRubric()

# Produto 1: Whey Budget (o que falhou antes)
product_1 = {
    'id': 'whey_budget',
    'name': 'Whey Budget Basic',
    'taste_rating': 2.5,  # RUIM
    'beginner_friendly_score': 3.0,
    'cost_benefit_score': 4.0,
    'availability_score': 5.0
}

result_1 = rubric.evaluate_product(product_1)
print(json.dumps(result_1, indent=2))

# Output:
# {
#   "product_id": "whey_budget",
#   "product_name": "Whey Budget Basic",
#   "final_score": 68.5,
#   "recommendation": "REJECT",
#   "reasoning": "Rejeitado: Taste Quality (2.5/5) ficou abaixo do threshold"
# }
# ❌ REJEITA PORQUE GOSTO RUIM


# Produto 2: Whey Premium (deve passar)
product_2 = {
    'id': 'whey_premium',
    'name': 'Whey Premium',
    'taste_rating': 4.8,  # BOM
    'beginner_friendly_score': 4.5,
    'cost_benefit_score': 4.0,
    'availability_score': 5.0
}

result_2 = rubric.evaluate_product(product_2)
print(json.dumps(result_2, indent=2))

# Output:
# {
#   "product_id": "whey_premium",
#   "product_name": "Whey Premium",
#   "final_score": 87.3,
#   "recommendation": "ACCEPT",
#   "reasoning": "Aceito: todas as dimensões passaram, score 87.3"
# }
# ✅ ACEITA
```

**Pontos-chave:**
- ✅ Cada dimensão tem weight (35%, 25%, 25%, 15%)
- ✅ Cada dimensão tem threshold (mínimo aceitável)
- ✅ Score final é média ponderada
- ✅ Rejeita se qualquer dimensão falha threshold OU score < 70
- ✅ Reasoning explica EXATAMENTE por que aceitou/rejeitou

---

### Rubrics em Produção (KODA)

```
FLUXO:

[Generator/Evaluator gera 5 opções, eleita: Whey X]
    ↓
[Sprint Contracts: dados são validados ✅]
    ↓
[Rubric avalia qualidade de Whey X]
    taste_rating: 2.5 ❌ (abaixo de 3.0)
    beginner_friendly: 3.0 ✅
    cost_benefit: 4.0 ✅
    availability: 5.0 ✅
    
    final_score: 68.5 ❌ (abaixo de 70)
    
    REJEITA!
    ↓
[Se top-1 é rejeitado, tenta top-2]
    Whey Y score: 76 ✅ ACEITA!
    ↓
[Recomenda Whey Y ao cliente]
```

**Benefício:**
- Sem rubric: recomenda Whey X (ruim) → cliente insatisfeito
- Com rubric: rejeita Whey X, recomenda Whey Y (bom) → cliente satisfeito

---

### Trade-offs: Precisão vs Simplicidade

**CUSTO:**
- Definir rubric: ~3-5 horas (pensar dimensões, pesos, thresholds)
- Implementar avaliação: ~2 horas
- Manutenção: ajustar pesos/thresholds com feedback real

**BENEFÍCIO:**
- Taxa de rejeição de recomendações ruins: ~80% (evita cliente insatisfeito)
- Satisfação esperada: sobe de 75% para 92%
- Feedback para melhoria: você sabe exatamente por que rejeitou algo

---

## 📚 Exercício 3: Rubric Design - Perguntas Conceituais

**Q1: No rubric mostrado, "Taste Quality" tem peso 35% e threshold 3.0. Por que não é weight 50% e threshold 5.0 (máximo)?**

[Seu espaço para responder]

---

**Q2: Se um produto passa em TODAS as dimensões (todas com score > threshold), mas o score final é 65/100, ele deve ser aceito ou rejeitado?**

[Seu espaço para responder]

---

**Q3: Você está criando um rubric para "Recomendação de Creatina". Quais dimensões você incluiria? (Nomeie 4-5)**

[Seu espaço para responder]

---

**Q4: Por que o código rejeita se "QUALQUER dimensão cai abaixo do threshold"? Por que não dar uma segunda chance (ex: baixa em gosto, mas alta em custo)?**

[Seu espaço para responder]

---

**Q5: Se você está rodando rubric e notou que muitas recomendações estão sendo rejeitadas (>70%), qual seria o primeiro ajuste: aumentar weights, aumentar thresholds, ou mudar dimensões?**

[Seu espaço para responder]

---

**Q6: Qual é a diferença entre "Generator/Evaluator score" (88/100) e "Rubric score" (75/100) para o mesmo produto?**

[Seu espaço para responder]

---

**Q7 (Bonus): Em produção, como você coletaria feedback para saber se os pesos/thresholds do rubric estão corretos?**

[Seu espaço para responder]

---

### ✅ Padrão Dominado?

Se conseguiu explicar pesos, thresholds e por que rejeita, você entendeu Rubric Design.

**Próxima:** Seção 5 - Trace Reading (diagnosticar quando dá errado)

---

---

## 🔍 Parte 5: Trace Reading em KODA

### A Reclamação (Quando Algo Deu Errado)

```
[3 DIAS DEPOIS DE UMA RECOMENDAÇÃO]

CLIENTE: "KODA, vocês me recomendaram uma proteína que achei HORRÍVEL.
         Gosto ruim, bateu com minha alergia, e agora tenho que devolver.
         Explica aí por que você recomendou errado!"

KODA: [Silêncio... como explicar?]
      "Desculpe, houve um erro. Não sei exatamente onde."
```

---

### O Problema: Invisibilidade

**A verdade sobre sistemas complexos:**

```
Quando algo dá errado, você tem 3 opções:

1. ❌ "Não sei por quê" (Nível 0)
   Ruim para confiança, ruim para melhoria, ruim para retenção

2. ⚠️ "Acho que foi o módulo X" (Nível 1)
   Especulação. Você investe 5 horas investigando o módulo errado.

3. ✅ "Sei exatamente onde e por quê" (Nível 2 com Trace Reading)
   Você abre o log, vê a sequência de decisões, identifica o erro em 10 min.
```

**Trace Reading** é a habilidade de **ler um trace** (registro completo do que aconteceu) e diagnósticar o problema.

---

### O Padrão: Trace Reading

**Ideia central:**

> Todo componente de KODA **registra** o que fez (input recebido, decisões tomadas, output produzido). Um Trace é a sequência COMPLETA desses registros. Quando algo falha, você "lê o trace" passo a passo para encontrar onde deu errado.

**Componentes:**

1. **Logging:** "O que cada módulo registra"
2. **Sequência:** "A ordem dos eventos com timestamps"
3. **Detalhe:** "O que você pode extrair de cada passo"
4. **Diagnóstico:** "Como ler e encontrar o problema"

---

### Como Ler um Trace (Exemplo Real)

**Cenário:** Cliente reclamou que recebeu whey COM lactose mas tinha dito que era intolerante.

```json
[TRACE COMPLETO DA RECOMENDAÇÃO ERRADA]

{
  "conversation_id": "conv_12345",
  "timestamp": "2026-05-26T14:32:00Z",
  "events": [
    
    {
      "step": 1,
      "module": "PARSE_REQUEST",
      "timestamp": "14:32:00.000",
      "input": {
        "message": "Quero whey, sou intolerante à lactose"
      },
      "output": {
        "budget": null,
        "restrictions": ["sem lactose"],
        "level": null
      },
      "decision": "Extraído restrição: sem lactose",
      "status": "✅ OK"
    },
    
    {
      "step": 2,
      "module": "GENERATOR",
      "timestamp": "14:32:01.500",
      "input": {
        "budget": null,
        "restrictions": ["sem lactose"],
        "level": null
      },
      "output": {
        "options": [
          {
            "id": "whey_1",
            "name": "Whey Isolado",
            "lactose_free": true
          },
          {
            "id": "whey_2",
            "name": "Whey Gold",
            "lactose_free": false  ← ⚠️ PROBLEMA AQUI
          },
          {
            "id": "whey_3",
            "name": "Whey Vegan",
            "lactose_free": true
          },
          {
            "id": "whey_4",
            "name": "Whey Budget",
            "lactose_free": false  ← ⚠️ E AQUI
          },
          {
            "id": "whey_5",
            "name": "Whey Starter",
            "lactose_free": true
          }
        ]
      },
      "decision": "Gerou 5 opções (mas 2 têm lactose!)",
      "status": "⚠️ PROBLEMA: Filtro de restrição não funcionou"
    },
    
    {
      "step": 3,
      "module": "EVALUATOR",
      "timestamp": "14:32:02.800",
      "input": {
        "options": "[whey_1, whey_2, whey_3, whey_4, whey_5]"
      },
      "output": {
        "scores": [
          {"id": "whey_1", "score": 78},
          {"id": "whey_2", "score": 82},  ← Eleita (tem lactose!)
          {"id": "whey_3", "score": 75},
          {"id": "whey_4", "score": 71},
          {"id": "whey_5", "score": 74}
        ]
      },
      "decision": "Whey_2 tem maior score, eleita",
      "status": "⚠️ PROBLEMA: Evaluator não validou restrição"
    },
    
    {
      "step": 4,
      "module": "CONTRACTS_VALIDATION",
      "timestamp": "14:32:03.200",
      "input": {
        "selected_product": {"id": "whey_2", "lactose_free": false}
      },
      "check": "Produto deve ter lactose_free=true (por restrição)",
      "actual": "lactose_free=false",
      "status": "❌ FALHA NO CONTRATO"
    },
    
    {
      "step": 5,
      "module": "RUBRIC_EVALUATION",
      "timestamp": "14:32:03.500",
      "input": {
        "product": {"id": "whey_2", "name": "Whey Gold", "lactose_free": false}
      },
      "rubric_check": "Verificar segurança (restrições do cliente)",
      "client_restrictions": ["sem lactose"],
      "product_properties": {"lactose_free": false},
      "match": false,
      "status": "❌ REJEITADO (incompatível com restrição)"
    },
    
    {
      "step": 6,
      "module": "FALLBACK",
      "timestamp": "14:32:03.800",
      "decision": "Whey_2 rejeitado, tenta Whey_3",
      "fallback_product": {"id": "whey_3", "name": "Whey Vegan", "lactose_free": true},
      "status": "✅ Whey_3 passou em todas as validações"
    },
    
    {
      "step": 7,
      "module": "RECOMMENDATION",
      "timestamp": "14:32:04.000",
      "output": "Recomendo Whey Vegan por R$ 140",
      "status": "✅ ENVIADO PARA CLIENTE"
    }
  ]
}
```

---

### Como Diagnosticar o Problema (Trace Reading)

**Lendo o trace acima:**

```
1. Parse: ✅ Extraiu corretamente "sem lactose"

2. Generator: ❌ PROBLEMA AQUI!
   Gerou 5 opções, mas NÃO filtrou por restrição
   Deveria ter gerado APENAS: [whey_1, whey_3, whey_5]
   Gerou: [whey_1, whey_2, whey_3, whey_4, whey_5]

3. Evaluator: ⚠️ Elegeu whey_2 (lactose=true)
   Mas não é culpa do Evaluator
   Generator deveria ter filtrado antes

4. Contracts Validation: ✅ Pegou o erro!
   "lactose_free deve ser true"
   whey_2 tem false → FALHA

5. Rubric: ✅ Também pegou!
   "Incompatível com restrição do cliente"

6. Fallback: ✅ Ajustou para whey_3

7. Final: ✅ Cliente recebeu whey_3 (correto)
```

**Diagnóstico Final:**

> **CULPADO:** Generator (não filtrou restrição)
> **SALVOU:** Sprint Contracts + Rubric (detectaram e rejeitaram)
> **AÇÃO:** Corrigir o Generator para SEMPRE filtrar restrições

---

### Implementação KODA (Python)

```python
from datetime import datetime
import json
from typing import List, Dict, Any

class TraceLogger:
    """Sistema que registra cada passo da recomendação"""
    
    def __init__(self, conversation_id: str):
        self.conversation_id = conversation_id
        self.events: List[Dict[str, Any]] = []
        self.step_counter = 0
    
    def log_step(
        self,
        module: str,
        input_data: Dict,
        output_data: Dict,
        decision: str,
        status: str
    ):
        """Registra um passo no trace"""
        self.step_counter += 1
        
        event = {
            "step": self.step_counter,
            "module": module,
            "timestamp": datetime.now().isoformat(),
            "input": input_data,
            "output": output_data,
            "decision": decision,
            "status": status
        }
        
        self.events.append(event)
    
    def get_trace(self) -> str:
        """Retorna trace completo em JSON"""
        return json.dumps({
            "conversation_id": self.conversation_id,
            "trace": self.events
        }, indent=2)
    
    def find_problem(self) -> Dict[str, Any]:
        """Analisa trace para encontrar problema"""
        
        # Procurar por status de erro
        failures = [
            event for event in self.events
            if "❌" in event.get("status", "") or "⚠️" in event.get("status", "")
        ]
        
        if not failures:
            return {
                "problem_found": False,
                "summary": "Nenhum erro detectado no trace"
            }
        
        # Encontrar PRIMEIRO erro
        first_failure = failures[0]
        
        return {
            "problem_found": True,
            "first_failure_at_step": first_failure["step"],
            "module": first_failure["module"],
            "decision": first_failure["decision"],
            "status": first_failure["status"],
            "recommendation": f"Investigar módulo {first_failure['module']}",
            "subsequent_failures": len(failures) - 1
        }


# USO EM KODA:

def generate_with_logging(client_request, trace_logger):
    """Generator com logging"""
    
    options = [
        {"id": "whey_1", "lactose_free": True},
        {"id": "whey_2", "lactose_free": False},  # BUG: não filtrou
        {"id": "whey_3", "lactose_free": True},
    ]
    
    trace_logger.log_step(
        module="GENERATOR",
        input_data={"restrictions": client_request["restrictions"]},
        output_data={"options": options},
        decision="Gerou opções",
        status="⚠️ PROBLEMA: Não filtrou restrições"
    )
    
    return options


def evaluate_with_logging(options, trace_logger):
    """Evaluator com logging"""
    
    scores = [
        {"id": "whey_1", "score": 78},
        {"id": "whey_2", "score": 82},  # Eleita
        {"id": "whey_3", "score": 75},
    ]
    
    trace_logger.log_step(
        module="EVALUATOR",
        input_data={"options": options},
        output_data={"scores": scores},
        decision="Whey_2 tem maior score",
        status="⚠️ PROBLEMA: Não validou restrição"
    )
    
    return scores


def validate_contracts_with_logging(selected, restrictions, trace_logger):
    """Contracts validation com logging"""
    
    is_valid = (selected["lactose_free"] == True) if "sem lactose" in restrictions else True
    
    trace_logger.log_step(
        module="CONTRACTS_VALIDATION",
        input_data={"product": selected, "restrictions": restrictions},
        output_data={"valid": is_valid},
        decision=f"Validar se {selected['id']} respeita restrições",
        status="✅ OK" if is_valid else "❌ FALHA"
    )
    
    return is_valid


# FLUXO COMPLETO:

trace = TraceLogger("conv_12345")

# Step 1: Generator
options = generate_with_logging(
    {"restrictions": ["sem lactose"]},
    trace
)

# Step 2: Evaluator
scores = evaluate_with_logging(options, trace)
selected_id = scores[0]["id"]  # whey_2 tem maior score
selected = next(o for o in options if o["id"] == selected_id)

# Step 3: Contracts
valid = validate_contracts_with_logging(
    selected,
    ["sem lactose"],
    trace
)

# Step 4: Analisar trace
print(trace.get_trace())
# ↑ Mostra JSON com todos os passos

problem = trace.find_problem()
print(json.dumps(problem, indent=2))
# ↑ Output:
# {
#   "problem_found": true,
#   "first_failure_at_step": 1,
#   "module": "GENERATOR",
#   "recommendation": "Investigar módulo GENERATOR"
# }
```

**Pontos-chave:**
- ✅ Cada módulo registra seu input, output, decisão, status
- ✅ Trace é JSON estruturado (fácil de analisar)
- ✅ `find_problem()` identifica ONDE falhou (primeiro erro)
- ✅ Você consegue reconstruir toda a sequência de decisões

---

### Trace Reading em Produção

**Quando cliente reclama:**

```
CLIENTE: "Por que vocês recomendaram whey com lactose?"

ENGINEERING:
1. Pega conversation_id da conversa
2. Carrega trace do banco de dados
3. Executa trace.find_problem()
4. Descobre: Generator não filtrou restrição
5. Responde ao cliente:
   "Desculpe, nosso gerador teve um bug em 26-05-2026.
    Já corrigimos. Você pode devolver o produto gratuitamente."
```

**Benefício:**
- Antes: "Não sei por quê" (confere confiança)
- Depois: "Identificamos a causa, corrigimos, não acontece mais" (restaura confiança)

---

### Trade-offs: Custo de Logging vs Visibilidade

**CUSTO:**
- Implementar logging em cada módulo: ~3 horas
- Storage de traces: ~1 KB por conversa (10K conversas = 10 MB/dia)
- Análise de traces: ferramentas (Datadog, ELK, Splunk) = custo

**BENEFÍCIO:**
- Tempo para debugar: 8 horas → 10 minutos (80x mais rápido!)
- Confiança do cliente: quando explica problema, cliente acredita
- Melhoria contínua: descobre padrões de erro (Generator falha 40% das vezes?)

---

## 📚 Exercício 4: Trace Reading - Perguntas Conceituais

**Q1: No trace mostrado, qual módulo foi o "culpado" do erro? E qual módulo "salvou" a situação?**

[Seu espaço para responder]

---

**Q2: Se você tivesse acesso ao trace ANTES de enviar a recomendação para o cliente, qual seria a ação correta?**

[Seu espaço para responder]

---

**Q3: Por que é importante registrar NÃO APENAS o resultado (output) de cada módulo, mas também a DECISÃO que levou a esse resultado?**

[Seu espaço para responder]

---

**Q4: Você está lendo um trace e vê: Generator ✅, Evaluator ✅, Contracts ❌, Rubric ❌. O que isso significa?**

[Seu espaço para responder]

---

**Q5: Em um sistema com 50.000 conversas por dia, como você buscaria por "todas as conversas onde Generator falhou"?**

[Seu espaço para responder]

---

**Q6: O trace registra que Generator gerou 5 opções, mas Evaluator só recebeu 4. O que isso indica?**

[Seu espaço para responder]

---

**Q7 (Bonus): Qual é a diferença entre "logging para debugging" (o que você faz em desenvolvimento) e "trace logging para diagnóstico" (o que você faz em produção)?**

[Seu espaço para responder]

---

### ✅ Padrão Dominado?

Se conseguiu explicar o fluxo do trace e identificar culpados/salvadores, você entendeu Trace Reading.

**Próxima:** Seção 6 - Refatoração Arquitetural (juntando TUDO!)

---

---

## 🛠️ Parte 6: Refatoração Arquitetural - Redesenhando o KODA

### O Estado Atual (Nível 1)

```
ARQUITETURA KODA - NÍVEL 1:

┌─────────────────────────────────────────────┐
│           CLIENTE CONVERSA COM KODA         │
└──────────────┬──────────────────────────────┘
               │
        ┌──────▼──────┐
        │ REQUEST     │
        │ PARSING     │
        └──────┬──────┘
               │
        ┌──────▼──────────────────┐
        │ SEARCH PRODUCTS          │
        │ (Query no banco)         │
        │ Output: 1 produto        │
        └──────┬──────────────────┘
               │
        ┌──────▼──────────────────┐
        │ HARNESS VALIDATION       │
        │ (Nível 1: Specs)         │
        │ ✅ Passa/❌ Falha         │
        └──────┬──────────────────┘
               │
        ┌──────▼──────────────────┐
        │ RECOMMENDATION           │
        │ (Se passou harness)      │
        │ Output: 1 opção          │
        └──────┬──────────────────┘
               │
               ▼
        [CLIENTE RECEBE]
```

**Características Nível 1:**
- ✅ Não quebra (validação harness)
- ✅ Gerencia contexto (token budgeting)
- ❌ Gera UMA opção (não escolhe a melhor)
- ❌ Módulos sem coordenação (Sprint Contracts)
- ❌ Avalia apenas válido/inválido (sem Rubric)
- ❌ Invisível (sem Trace Reading)

**Métricas Nível 1:**
```
Taxa de acurácia: 65%
Satisfação do cliente: 72%
Taxa de erro silencioso: 8%
Custo por recomendação: R$ 0.03 (tokens)
Tempo para debugar problema: ~8 horas
Retenção de cliente: 68%
```

---

### Visão Futura (Nível 2)

```
ARQUITETURA KODA - NÍVEL 2:

┌─────────────────────────────────────────────────┐
│         CLIENTE CONVERSA COM KODA               │
└──────────────┬──────────────────────────────────┘
               │
        ┌──────▼──────┐
        │ REQUEST     │
        │ PARSING     │ → [Trace Logger]
        └──────┬──────┘
               │
    ┌──────────┴──────────┐
    │                     │
┌───▼──────────────┐  ┌──▼─────────────────┐
│ GENERATOR        │  │ STATE PERSISTENCE  │
│ (Gera 5 opções) │  │ (Histórico, dados) │
│ Contract: Out   │  │ Contract: Get/Set  │
└───┬──────────────┘  └────────────────────┘
    │
    │ [Sprint Contract validation]
    │
┌───▼───────────────────────────────────┐
│ EVALUATOR (Score cada opção)           │
│ Usa: Purity, Rating, Cost-Benefit      │
│ Contract: {options} → {scores}         │
└───┬───────────────────────────────────┘
    │
    │ [Sprint Contract validation]
    │
┌───▼──────────────────────────────────┐
│ RUBRIC EVALUATION (Qualidade)         │
│ Dimensions: Taste, Safety, Value      │
│ Score: 0-100, Threshold: 70           │
│ Accept/Reject                         │
└───┬──────────────────────────────────┘
    │
    ├─ If Rejected: Try next option
    │ (Fallback loop)
    │
    │ [All validations]
    │
┌───▼──────────────────────────────────┐
│ RECOMMENDATION                        │
│ Top-1 (score >= 70) ou Top-3 options │
│ Output: {product, score, reasoning}  │
└───┬──────────────────────────────────┘
    │
    │ [Trace Logger: Registra tudo]
    │
    ▼
[CLIENTE RECEBE]
```

**Características Nível 2:**
- ✅ Não quebra (Nível 1 + Contracts + Rubric)
- ✅ Gera MÚLTIPLAS opções (Generator/Evaluator)
- ✅ Módulos coordenados (Sprint Contracts)
- ✅ Avalia QUALIDADE (Rubric Design)
- ✅ Visível (Trace Reading)
- ✅ Recuperação automática (Fallback quando rejeita)

**Métricas Nível 2:**
```
Taxa de acurácia: 87% (+22 pontos!)
Satisfação do cliente: 91% (+19 pontos!)
Taxa de erro silencioso: 1% (-7 pontos!)
Custo por recomendação: R$ 0.09 (3x, mas 30% mais vendas)
Tempo para debugar: 15 minutos (-480 minutos!)
Retenção de cliente: 85% (+17 pontos!)
```

---

### Jornada de Transformação: Passo a Passo

**SEMANA 1-2: Implementar Generator/Evaluator**

```
FASE 1.1: Design (2 dias)
  □ Definir "dimensões de diferença" (quality vs cost vs ethics)
  □ Desenhar contrato Generator Input/Output
  □ Desenhar contrato Evaluator Input/Output
  □ Validar com time que faz sentido

FASE 1.2: Implementação (3 dias)
  □ Generator: Código que gera 5 opções diferentes
  □ Evaluator: Código que avalia cada uma com critérios
  □ Teste: Que output é determinístico?

FASE 1.3: Validação (2 dias)
  □ Rodar em ambiente de staging
  □ Taxa de acurácia sobe: 65% → 75%
  □ Satisfação sobe: 72% → 78%
  □ Deploy em produção

RESULTADO: KODA agora gera múltiplas opções!
```

**SEMANA 3: Implementar Sprint Contracts**

```
FASE 2.1: Mapeamento (1 dia)
  □ Listar todos os módulos KODA
  □ Para cada um: definir input_contract + output_contract
  □ Documentar em Pydantic classes

FASE 2.2: Validação (2 dias)
  □ Adicionar validação de entrada em cada módulo
  □ Adicionar validação de saída em cada módulo
  □ Testar: "Se Generator entrega errado, TODOS os módulos sabem"

FASE 2.3: Debugging (2 dias)
  □ Bugs aparecem durante testes (bom!)
  □ Fix um por um
  □ Deploy

RESULTADO: Módulos estão sincronizados!
```

**SEMANA 4: Implementar Rubric Design**

```
FASE 3.1: Design Rubric (2 dias)
  □ Definir dimensões (Taste, Quality, Value, Availability)
  □ Definir pesos (35%, 25%, 25%, 15%)
  □ Definir thresholds (mínimo aceitável por dimensão)
  □ Definir score final mínimo (70)

FASE 3.2: Implementação (2 dias)
  □ Código Pydantic para cada dimensão
  □ Score calculation (weighted average)
  □ Accept/Reject logic
  □ Fallback: se top-1 rejeitado, tenta top-2

FASE 3.3: Validação (1 dia)
  □ Teste em staging
  □ Taxa de rejeição esperada: ~20%
  □ Deploy

RESULTADO: KODA só recomenda produtos "bons"!
```

**SEMANA 5: Implementar Trace Reading**

```
FASE 4.1: Infraestrutura (2 dias)
  □ Criar TraceLogger class
  □ Adicionar logging em cada módulo
  □ Estrutura JSON para traces
  □ Storage em banco de dados (ou file system)

FASE 4.2: Análise (2 dias)
  □ Criar função find_problem() para analisar traces
  □ Criar dashboards para visualizar padrões de erro
  □ Documentar como ler traces

FASE 4.3: Validação (1 dia)
  □ Testar: consegue encontrar problema em trace?
  □ Deploy

RESULTADO: Quando algo falha, você SABE onde!
```

---

### Cronograma Integrado (5 Semanas)

```
SEMANA  │ Mon    │ Tue    │ Wed    │ Thu    │ Fri    │ STATUS
────────┼────────┼────────┼────────┼────────┼────────┼─────────────
1       │ Gen/E  │ Gen/E  │ Gen/E  │ Gen/E  │ Gen/E  │ ⚙️ RODANDO
        │ Design │ Impl 1 │ Impl 2 │ Test   │ Deploy │
────────┼────────┼────────┼────────┼────────┼────────┼─────────────
2       │ Gen/E  │ Sprint │ Sprint │ Sprint │ Deploy │ ⚙️ RODANDO
        │ Polish │ Design │ Impl   │ Test   │        │
────────┼────────┼────────┼────────┼────────┼────────┼─────────────
3       │ Sprint │ Rubric │ Rubric │ Rubric │ Deploy │ ⚙️ RODANDO
        │ Refine │ Design │ Impl   │ Test   │        │
────────┼────────┼────────┼────────┼────────┼────────┼─────────────
4       │ Trace  │ Trace  │ Trace  │ Trace  │ Deploy │ ⚙️ RODANDO
        │ Design │ Impl   │ Impl   │ Test   │        │
────────┼────────┼────────┼────────┼────────┼────────┼─────────────
5       │ Integr │ Integr │ Integr │ Integr │ Deploy │ ✅ COMPLETO
        │ Teste  │ Teste  │ Teste  │ Teste  │        │

TOTAL: 5 semanas para transformação completa!
```

---

### Métricas: Antes vs Depois

```
╔════════════════════════════════════════════════════════════════╗
║                 COMPARATIVO NÍVEL 1 vs 2                       ║
╠═════════════════════════════╦═════════════════╦════════════════╣
║ MÉTRICA                     ║ NÍVEL 1         ║ NÍVEL 2        ║
╠═════════════════════════════╬═════════════════╬════════════════╣
║ Taxa de Acurácia            ║ 65%             ║ 87%   (+22pp)  ║
║ Satisfação do Cliente       ║ 72%             ║ 91%   (+19pp)  ║
║ Taxa de Erro Silencioso     ║ 8%              ║ 1%    (-7pp)   ║
║ Custo por Recomendação      ║ R$ 0.03         ║ R$ 0.09 (3x)   ║
║ Tempo para Debugar          ║ 480 min (8h)    ║ 15 min (-97%)  ║
║ Retenção de Cliente         ║ 68%             ║ 85%   (+17pp)  ║
║ Rejections da Rubric        ║ N/A             ║ ~20%           ║
║ Fallback Success Rate       ║ N/A             ║ 85%            ║
╠═════════════════════════════╬═════════════════╬════════════════╣
║ IMPACTO FINANCEIRO (100 recomendações)                         ║
╠═════════════════════════════╬═════════════════╬════════════════╣
║ Recomendações Aceitas       ║ 100             ║ 100            ║
║ Conversões (taxa acurácia)  ║ 65 vendas       ║ 87 vendas      ║
║ Receita (R$ 120/venda)      ║ R$ 7.800        ║ R$ 10.440      ║
║ Custo (tokens)              ║ R$ 3.00         ║ R$ 9.00        ║
║ Lucro Líquido               ║ R$ 7.797        ║ R$ 10.431      ║
║ Delta                       ║ —               ║ +34% lucro! 💰 ║
╚═════════════════════════════╩═════════════════╩════════════════╝
```

**Insight:** O custo 3x é mais que compensado pelas 22 vendas adicionais (34% mais lucro).

---

### Trade-offs e Decisões de Design

**DECISÃO 1: Generator cria 5 opções ou 3?**

```
OPÇÃO A: 5 opções
  ✅ Cobertura maior do espaço de soluções
  ✅ Mais chances de passar na Rubric
  ❌ Custo 2x maior (5 vs 3 opções)
  
OPÇÃO B: 3 opções
  ✅ Custo menor
  ✅ Mais rápido
  ❌ Menos cobertura, pode rejeitar todas na Rubric

ESCOLHA: 5 opções (custo vale a pena pelo resultado)
```

---

**DECISÃO 2: Rubric rejeita se 1 dimensão falha OU só se score final < 70?**

```
OPÇÃO A: Rejeita se QUALQUER dimensão < threshold
  ✅ Segurança: não recomenda se gosto é ruim (mesmo que preço seja bom)
  ❌ Pode rejeitar demais (muitas rejeições)
  
OPÇÃO B: Rejeita só se score final < 70
  ✅ Flexibilidade: permite trade-off (baixo gosto, alto custo-benefício)
  ❌ Insegurança: pode recomendar algo ruim em uma dimensão

ESCOLHA: Opção A (segurança > flexibilidade, cliente importa mais)
```

---

**DECISÃO 3: Rastrear TUDO ou apenas erros?**

```
OPÇÃO A: Rastrear TUDO (10 KB por conversa)
  ✅ Visibilidade total
  ✅ Consegue reconstruir qualquer decisão
  ❌ Armazena muitos dados (caro)
  
OPÇÃO B: Rastrear só erros e checkpoints principais (1 KB)
  ✅ Menos dados
  ✅ Mais rápido
  ❌ Menos visibilidade quando algo inesperado acontece

ESCOLHA: Opção A (armazenamento é barato, visibilidade é cara)
```

---

**DECISÃO 4: Deploy tudo de uma vez ou incrementalmente?**

```
OPÇÃO A: Big Bang (tudo de uma vez)
  ✅ Rápido (1 deploy)
  ❌ Risco alto (se quebra, sistema todo cai)
  
OPÇÃO B: Incrementalmente (Gen/Eval → Contracts → Rubric → Trace)
  ✅ Risco baixo (descobre problemas cedo)
  ✅ Canary deploy (roda 10% do traffic primeiro)
  ❌ Mais lento (5 semanas)

ESCOLHA: Opção B (risco é mais importante que velocidade em produção)
```

---

### Implementação Completa: Pseudocódigo

```python
class KODAv2:
    """KODA Nível 2 - Completo"""
    
    def __init__(self):
        self.generator = Generator()
        self.evaluator = Evaluator()
        self.rubric = ProductRubric()
        self.trace_logger = TraceLogger()
        self.state_manager = StateManager()
        self.contracts_validator = ContractsValidator()
    
    def recommend(self, client_request: dict) -> dict:
        """
        Pipeline completo de recomendação (Nível 2)
        """
        
        conversation_id = client_request['conversation_id']
        trace = TraceLogger(conversation_id)
        
        # STEP 1: Parse request
        parsed = self._parse_request(client_request, trace)
        
        # STEP 2: Load client state
        client_state = self.state_manager.get(client_request['client_id'])
        
        # STEP 3: Generator (with Sprint Contract validation)
        options = self.generator.execute(parsed, trace)
        self.contracts_validator.validate_generator_output(options)
        
        # STEP 4: Evaluator (with Sprint Contract)
        scored_options = self.evaluator.execute(options, trace)
        self.contracts_validator.validate_evaluator_output(scored_options)
        
        # STEP 5: Rubric (try to find acceptable recommendation)
        recommendation = None
        for option in scored_options:  # Loop from top score
            rubric_result = self.rubric.evaluate_product(option['product'], trace)
            
            if rubric_result['recommendation'] == 'ACCEPT':
                recommendation = {
                    'product': option['product'],
                    'evaluator_score': option['score'],
                    'rubric_score': rubric_result['final_score'],
                    'reasoning': rubric_result['reasoning']
                }
                break  # Found acceptable recommendation
        
        # STEP 6: Fallback (if all rejected, use best available with warning)
        if not recommendation:
            best_option = scored_options[0]
            recommendation = {
                'product': best_option['product'],
                'warning': 'No option passed quality threshold. Offering best available.',
                'evaluator_score': best_option['score']
            }
        
        # STEP 7: Trace (register everything)
        trace.log_step(
            module="RECOMMENDATION",
            input_data={"options": len(options)},
            output_data=recommendation,
            decision="Selected best acceptable option",
            status="✅ OK"
        )
        
        # STEP 8: Return response
        return {
            'recommendation': recommendation,
            'trace_id': conversation_id,
            'trace': trace.get_trace()
        }
```

---

## 📚 Exercício 5: Refatoração Arquitetural - Perguntas sobre Escolhas

**Q1: Por que implementar na ordem Generator/Evaluator → Contracts → Rubric → Trace (e não de uma vez)?**

[Seu espaço para responder]

---

**Q2: Na métrica "Custo por Recomendação", KODA Nível 2 custa 3x mais (R$ 0.09 vs R$ 0.03). Mas o lucro sobe 34%. Como isso é possível?**

[Seu espaço para responder]

---

**Q3: O Exercício da Seção 4 mostrou que Rubric rejeitou "Whey Budget Basic" (score 68.5). Em produção, o que KODA faz quando top-1 é rejeitado?**

[Seu espaço para responder]

---

**Q4: No cronograma, cada semana tem um deploy. Qual seria o risco de fazer UM deploy grande (5 semanas de code) vs 5 deploys pequenos?**

[Seu espaço para responder]

---

**Q5: A taxa de erro silencioso cai de 8% para 1%. O que "erro silencioso" significa?**

[Seu espaço para responder]

---

**Q6: Você está em produção, rodando Nível 2. Um cliente reclama: "Vocês me recomendaram errado NOVAMENTE!" Qual é o PRIMEIRO passo que você toma?**

[Seu espaço para responder]

---

**Q7 (Bonus): Se você tivesse que escolher APENAS 1 dos 4 padrões para implementar primeiro (Gen/Eval, Contracts, Rubric, Trace), qual seria e por quê?**

[Seu espaço para responder]

---

### ✅ Padrão Dominado?

Se conseguiu explicar cronograma, trade-offs e impacto financeiro, você entendeu Refatoração Arquitetural.

**Próxima:** Exercises consolidation e próximos passos!

---

---

## 📚 Exercícios Práticos

### Exercício 1: Design um Generator/Evaluator para Busca de Produtos

[To be written]

### Exercício 2: Escrever Rubric para Validação de Pedidos

[To be written]

### Exercício 3: Ler e Diagnosticar um Trace de Conversa Quebrada

[To be written]

### Exercício 4: Refatorar a Arquitetura KODA (Desafio Avançado)

[To be written]

---

## 🎓 Checklist de Implementação (Semanas 3-4)

### Para Você, como Integrante do Time KODA em Nível 2

#### **Semana 3: Generator/Evaluator + Sprint Contracts**

- [ ] **Leitura (2h)**
  - [ ] Leia `01-generator-evaluator-pattern.md` completamente
  - [ ] Leia `02-sprint-contracts.md` completamente
  - [ ] Entenda como os 2 padrões interagem

- [ ] **Exercises (3h)**
  - [ ] Complete Exercício 1 (Design Gen/Eval para feature KODA)
  - [ ] Complete Exercício 2 (Escrever contratos em Pydantic)
  - [ ] Review suas respostas contra apêndice

- [ ] **Micro-Projeto (4h)**
  - [ ] Escolha UMA feature atual do KODA
  - [ ] Desenhe como implementaria Gen/Eval + Contracts
  - [ ] Estime custo (tokens) e benefício (acurácia)
  - [ ] Apresente ao time

- [ ] **Checklist de Entendimento**
  - [ ] Consigo explicar por que gerar múltiplas opções?
  - [ ] Consigo escrever um contrato Pydantic para um módulo?
  - [ ] Consigo identificar quando Sprint Contracts está quebrado?
  - [ ] Entendo trade-off custo vs benefício?

**Checkpoint Semana 3:**
- ✅ Ambos padrões entendidos em profundidade
- ✅ Código Pydantic funcional
- ✅ Micro-projeto apresentado

---

#### **Semana 4: Rubric Design + Trace Reading**

- [ ] **Leitura (2h)**
  - [ ] Leia `03-rubric-design.md` completamente
  - [ ] Leia `04-trace-reading.md` completamente
  - [ ] Entenda como Rubric + Trace trabalham juntos

- [ ] **Exercises (3h)**
  - [ ] Complete Exercício 3 (Criar Rubric para recomendação KODA)
  - [ ] Complete Exercício 4 (Ler trace real e encontrar problema)
  - [ ] Review suas respostas contra apêndice

- [ ] **Micro-Projeto Avançado (5h)**
  - [ ] Pegue uma conversa KODA real que falhou (ou simule)
  - [ ] Gere o trace completo (simule se não tiver)
  - [ ] Rode `find_problem()` para diagnosticar
  - [ ] Apresente: "A culpa foi do módulo X porque..."

- [ ] **Design Rubric para KODA (3h)**
  - [ ] Defina 4-5 dimensões para recomendação
  - [ ] Defina pesos (somam 100%)
  - [ ] Defina thresholds e score mínimo
  - [ ] Documente em JSON

- [ ] **Checklist de Entendimento**
  - [ ] Consigo criar um Rubric do zero?
  - [ ] Consigo explicar por que Rubric != Validação?
  - [ ] Consigo ler um trace JSON e encontrar o erro?
  - [ ] Entendo como Trace Reading melhora confiança do cliente?

**Checkpoint Semana 4:**
- ✅ Ambos padrões entendidos
- ✅ Rubric desenhado e documentado
- ✅ Capaz de ler e diagnosticar traces
- ✅ Micro-projeto avançado apresentado

---

#### **Final: Integração Completa (Opcional, Semana 5)**

Se tempo permitir:

- [ ] Implementar os 4 padrões em UMA feature do KODA
- [ ] Comparar antes (Nível 1) vs depois (Nível 2)
- [ ] Coletar métricas de melhoria
- [ ] Documentar em Decision Record
- [ ] Apresentar case study ao time

---

## 🔗 Mapeando Para Nível 3

### O Que Você Aprendeu em Nível 2 ✓

- ✅ **Generator/Evaluator:** Como gerar múltiplas opções e escolher a melhor
- ✅ **Sprint Contracts:** Como coordenar módulos com "promessas"
- ✅ **Rubric Design:** Como avaliar qualidade em múltiplas dimensões
- ✅ **Trace Reading:** Como diagnosticar problemas e aprender com falhas
- ✅ **Refatoração Arquitetural:** Como planejar e implementar transformação
- ✅ **Trade-offs:** Entender custo vs benefício, risco vs velocidade

---

### O Que Vem em Nível 3 (Preview) 🔜

Nível 3 é sobre **arquitetura distribuída** com múltiplos agentes:

1. **Multi-Agent Systems**
   - Não um KODA monolítico, mas múltiplos agentes especializados
   - Ex: Agent Busca, Agent Ranking, Agent Validação, cada um rodando independentemente
   - Como eles se comunicam? Fila de mensagens? Eventos? Contratos?

2. **State Persistence Avançada**
   - Não apenas histórico de conversa, mas estado compartilhado entre agentes
   - Como sincronizar estado sem conflitos?
   - Consistency vs Availability (CAP theorem)

3. **Harness Evolution**
   - Quando Claude 4.7 sair (melhor modelo), como você aproveita?
   - Seus harnesses antigos ainda funcionam?
   - Como evoluir harnesses gracefully?

4. **File-Based Coordination**
   - Agentes coordenam lendo/escrevendo arquivos (não API chamadas)
   - Por que isso é mais simples que REST APIs
   - Quando usar vs quando não usar

5. **Advanced Rubric Systems**
   - Rubrics que aprendem com feedback
   - Meta-rubrics (avaliar se sua rubric está boa)
   - Dynamic thresholds (ajustar conforme dados reais)

---

### Preparação Para Nível 3

Antes de começar Nível 3, você precisa:

- [ ] Ter implementado pelo menos 1 padrão de Nível 2 em KODA real
- [ ] Ser capaz de ler e entender traces de conversas complexas
- [ ] Entender por que arquitetura distribuída é difícil (e necessária)
- [ ] Estar pronto para pensar em termos de "agentes", não "módulos"

---

## 📊 Resumo Visual: Os 4 Padrões em Ação

```
                    CLIENTE FAZ PERGUNTA
                           ↓
        ┌──────────────────────────────────────┐
        │   1. GENERATOR/EVALUATOR              │
        │   ├─ Gera 5 opções diferentes        │
        │   ├─ Avalia cada uma (0-100)         │
        │   └─ Eleita: opção com melhor score  │
        │   Resultado: Opção #2 (score 82/100) │
        └──────────────┬───────────────────────┘
                       ↓
        ┌──────────────────────────────────────┐
        │   2. SPRINT CONTRACTS                 │
        │   ├─ Valida: recebi o que esperava?  │
        │   ├─ Cheque: dados têm todos campos? │
        │   ├─ Síncrono: módulos alinhados?    │
        │   └─ ✅ Tudo certo, prossiga         │
        └──────────────┬───────────────────────┘
                       ↓
        ┌──────────────────────────────────────┐
        │   3. RUBRIC DESIGN                    │
        │   ├─ Dimensão 1 (Gosto): 4.5/5       │
        │   ├─ Dimensão 2 (Qualidade): 4.0/5   │
        │   ├─ Dimensão 3 (Custo): 4.5/5       │
        │   ├─ Dimensão 4 (Disponibilidade): 5/5
        │   └─ Score Final: 87/100 ✅ ACEITA   │
        └──────────────┬───────────────────────┘
                       ↓
        ┌──────────────────────────────────────┐
        │   4. TRACE LOGGING                    │
        │   ├─ Step 1: Generator ✅            │
        │   ├─ Step 2: Evaluator ✅            │
        │   ├─ Step 3: Contracts ✅            │
        │   ├─ Step 4: Rubric ✅               │
        │   └─ JSON trace completo salvo       │
        └──────────────┬───────────────────────┘
                       ↓
                 RECOMENDAÇÃO
               (Confiável, visível,
                auditável, melhorável)
```

---

## 🚀 Próximos Passos

### Imediatamente (Esta Semana)

1. **Escolha UMA feature do KODA** que você quer melhorar
   - Busca de produtos?
   - Validação de pedido?
   - Recomendação de promoção?
   - Outra?

2. **Colete 3-5 conversas** onde essa feature falhou
   - Se não tiver dados reais, simule conversas

3. **Crie um Decision Record**
   ```
   Título: "Implementar Gen/Eval para Feature X"
   Problema: "Taxa de acurácia é 65%, clientes insatisfeitos"
   Solução: "Implementar Generator/Evaluator + Sprint Contracts"
   Estimativa: "3 semanas"
   Impacto: "Acurácia sobe para 85%"
   ```

---

### Próximas 2 Semanas

1. **Designar owner** para cada padrão (pode ser você!)
   - Owner de Generator/Evaluator
   - Owner de Sprint Contracts
   - Owner de Rubric Design
   - Owner de Trace Reading

2. **Fazer design** de como implementar
   - Desenhar arquitetura
   - Escrever contratos (Pydantic)
   - Definir rubric
   - Planejar logging

3. **Apresentar ao time**
   - "Aqui está o plano para Nível 2"
   - "Aqui estão os 4 padrões que vamos implementar"
   - "Aqui está o impacto esperado"

---

### Próximas 5 Semanas

1. **Semana 1-2:** Implementar Gen/Eval + Contracts
2. **Semana 3:** Implementar Rubric Design
3. **Semana 4:** Implementar Trace Reading
4. **Semana 5:** Integração, testes, deploy
5. **Semana 6:** Coletar métricas, celebrar! 🎉

---

### Antes de Nível 3

1. Você deve ter **uma feature completamente Nível 2**
2. Deve saber **ler traces** de conversas reais
3. Deve entender **trade-offs** entre padrões
4. Deve estar pronto para pensar em **múltiplos agentes**

---

## ✨ Palavras Finais

Quando você começou Nível 1, aprendeu que agentes perdem o foco. Você resolveu isso com **contexto**, **budgeting** e **harnesses**.

Agora, em Nível 2, você descobriu que não quebrar não é suficiente. Você precisa ser **visível**, **inteligente** e **confiável**.

**Generator/Evaluator** faz você inteligente (múltiplas opções, melhor escolhida).

**Sprint Contracts** faz você confiável (módulos sincronizados, sem surpresas).

**Rubric Design** faz você confiável (rejeita recomendações ruins, aceita boas).

**Trace Reading** faz você visível (quando algo falha, você SABE onde).

Juntos, esses 4 padrões transformam KODA de um agente que "funciona" para um agente que você consegue **entender**, **melhorar** e **confiar**.

Isso é Nível 2.

Fernando viu isso acontecer e percebeu: **a diferença entre um agente que sobrevive e um agente que prospera não é o modelo, é a arquitetura.**

Você está pronto. Agora, **implemente**.

---

## 📎 Apêndice: Respostas Comentadas dos Exercícios

### Exercício 1: Generator/Evaluator - Respostas

**Q1: Por que múltiplas opções vs uma?**
- Resposta esperada: "Uma opção assume que você sabe o que é melhor. Múltiplas exploram trade-offs diferentes (qualidade vs preço vs ética). Aumenta chance de acerto."

**Q2: Por que cada opção tem reasoning?**
- Resposta esperada: "Para você entender por que essa opção foi gerada. Sem reasoning, é só um output. Com reasoning, você aprende a intenção do generator."

**Q3: Recomendar APENAS top-1?**
- Resposta esperada: "Não! Você pode mostrar top-3 para o cliente escolher. Ou rejeitar top-1 se falhar rubric, usar top-2. Múltiplas opções dão flexibilidade."

**Q4: Evaluator rodou 2x com scores diferentes?**
- Resposta esperada: "Indica que o Evaluator foi ajustado, ou os dados mudaram, ou há inconsistência. Deve rodar determinístico (temperature=0.2)."

**Q5: Generator sempre precisa 5+ opções?**
- Resposta esperada: "Não, depende do problema. Recomendação pode ser 5. Mas para decisão binária (sim/não), 2-3 bastam. Balancear exploração vs custo."

**Q6: Diferença entre Evaluator score (88) e Validação (pass)?**
- Resposta esperada: "Validação é binário (sim/não). Evaluator é numérico (0-100), diferencia qualidade relativa. Evaluator é mais útil."

**Q7 Bonus: Maior desafio técnico?**
- Resposta esperada: "Custo (3x mais caro). Ou: Definir critérios consistentes para evaluation. Ou: Garantir que evaluator é determinístico."

---

### Exercício 2: Sprint Contracts - Respostas

**Q1: Por que input E output contracts?**
- Resposta esperada: "Input valida que recebi dados certos (evita garbage in). Output valida que cumpri minha promessa (evita garbage out). Juntas, garantem data integrity."

**Q2: Por que 3-10 produtos, não exatamente 5?**
- Resposta esperada: "Porque nem sempre há 5 produtos disponíveis. 3-10 é o range realista. Mas sempre >= 3 (para ter opção) e <= 10 (pra não sobrecarregar cliente)."

**Q3: Primeiro passo ao implementar FILTRO?**
- Resposta esperada: "Resposta A - Escrever input_contract baseado no output_contract de SEARCH. Você precisa saber o contrato anterior antes de escrever seu código."

**Q4: Por que validar no método vs implícito no Pydantic?**
- Resposta esperada: "Para ter controle e logging. Você quer saber QUANDO falhou, não só "erro genérico". Com try/except explícito, você pode fazer logging, rastreamento, etc."

**Q5: Qual módulo quebra se SEARCH muda?**
- Resposta esperada: "RANKING (recebe output de SEARCH). Se SEARCH add novo campo, RANKING precisa se adaptar. Ou: todos que leêm output de SEARCH precisam ser atualizados."

**Q6: Se receive válido, processa, mas entrega inválido?**
- Resposta esperada: "É um BUG INTERNO do módulo. Contrato deve falhar (exceção lançada). Melhor falhar rápido do que entrega silenciosamente errado."

**Q7 Bonus: 10 módulos encadeados, vantagem de contracts?**
- Resposta esperada: "Isolação de mudanças. Se módulo 5 muda, só módulo 6 é afetado (via contrato). Sem contracts, mudança em 5 pode afetar 6,7,8,9,10."

---

### Exercício 3: Rubric Design - Respostas

**Q1: Por que peso 35% para gosto, não 50%?**
- Resposta esperada: "Porque iniciante precisa de múltiplas dimensões. Gosto é importante (35%), mas qualidade (20%) e custo (25%) também. Balanceamento é crucial."

**Q2: Passa todas dimensões mas score < 70?**
- Resposta esperada: "Rejeitado. Score final é o "health check" da recomendação inteira. Se individual pass mas agregado falha, há inconsistência. Rejeita para ser seguro."

**Q3: Dimensões para Creatina?**
- Resposta esperada: Exemplos: Pureza, Solubilidade, Preço, Timing (pré/pós treino), Segurança (sem contaminantes). Você nomeia 4-5 relevantes."

**Q4: Por que rejeita se QUALQUER dimensão falha threshold?**
- Resposta esperada: "Segurança. Se gosto é horrível (2/5), não compensa preço baixo. Protege contra "trade-off ruim". Você pode relaxar isso se quiser flexibilidade."

**Q5: Muitas rejeições (>70%), primeiro ajuste?**
- Resposta esperada: "Aumentar thresholds dimensionais, NÃO o score final. Ou: revisar dimensões (talvez uma está muito rigorosa). Weights são "secundários", thresholds são "primários"."

**Q6: Diferença entre Evaluator score e Rubric score?**
- Resposta esperada: "Evaluator score (88) é 'quanto KODA acha que é bom baseado em dados'. Rubric score (75) é 'quantoé realmente bom contra critérios multi-dimensionais'. Rubric é o ground truth."

**Q7 Bonus: Como validar pesos/thresholds em produção?**
- Resposta esperada: "Coletar feedback do cliente real. Se aceitou, ficou satisfeito? Se rejeitou, era mesmo ruim? Iterar pesos/thresholds baseado em feedback."

---

### Exercício 4: Trace Reading - Respostas

**Q1: Culpado + Salvador?**
- Resposta esperada: "Culpado: GENERATOR (não filtrou restrição). Salvador: CONTRACTS + RUBRIC (detectaram e rejeitaram antes de enviar)."

**Q2: Ação se tivesse acesso ao trace ANTES?**
- Resposta esperada: "Não enviar a recomendação. Usar fallback (top-2). Ou rejuntar mensagem: 'Desculpe, nossa melhor opção não atende suas restrições. Que tal essa?'"

**Q3: Por que registrar DECISÃO além de resultado?**
- Resposta esperada: "Porque resultado sem decisão é misterioso. Você vê 'output X' mas não sabe por quê. Decisão deixa explícito o raciocínio de cada passo."

**Q4: Gen ✅, Eval ✅, Contracts ❌, Rubric ❌?**
- Resposta esperada: "Generator e Evaluator rodaram bem, mas Contracts falhou (dados inconsistentes). Rubric também falhou (porque recebeu dados ruins). Culpado: Generator ou Evaluator quebrou contrato."

**Q5: Como buscar "todas as conversas onde Generator falhou" em 50K/dia?**
- Resposta esperada: "Banco de dados com índice em 'step.module' + 'status'. Query: SELECT traces WHERE traces[1].status LIKE '%Generator%FAIL%'. Precisa infra (Elasticsearch, BigQuery)."

**Q6: Generator gerou 5, Evaluator recebeu 4?**
- Resposta esperada: "Alguém removeu 1 opção entre eles (filtro silencioso, erro de serialização, etc). Trace deveria mostrar em qual passo. Investigate o módulo intermediário."

**Q7 Bonus: Logging para debug vs Trace para diagnóstico?**
- Resposta esperada: "Debug logging: você escreve manualmente durante desenvolvimento ('print aqui', 'print ali'). Trace logging: estruturado, automático, em produção, para diagnosticar problemas do cliente real."

---

### Exercício 5: Refatoração - Respostas

**Q1: Por que sequencial, não tudo de uma vez?**
- Resposta esperada: "Risco. Se Gen/Eval quebra tudo, você desativa e volta. Sequencial permite canary deploy (10% traffic), validar antes de 100%. Velocidade < segurança em produção."

**Q2: Custo 3x, mas lucro sobe 34%?**
- Resposta esperada: "Taxa de acurácia sobe 65% → 87% (22 vendas adicionais em 100). Custo extra: R$ 6 (3500 tokens * 100). Receita extra: R$ 2.640 (22 * 120). Lucro: 2.640 - 6 = 2.634 (+34%)."

**Q3: Quando top-1 é rejeitado?**
- Resposta esperada: "Tenta top-2. Se top-2 também rejeitado, tenta top-3. Se nenhum passa, usa fallback (recomenda best available com warning)."

**Q4: Risco: 1 deploy grande vs 5 pequenos?**
- Resposta esperada: "1 grande: risco alto (se quebra, sistema todo cai por 8 horas). 5 pequenos: risco baixo (quebra só 1 componente, rollback rápido). Pequenos são melhores."

**Q5: O que é 'erro silencioso'?**
- Resposta esperada: "Recomendação errada que o sistema acha estar certa. Cliente recebe e fica insatisfeito. Em Nível 1, acontece 8% das vezes (invisível). Em Nível 2, Rubric rejeita antes."

**Q6: Primeiro passo se cliente reclama?**
- Resposta esperada: "Pegar conversation_id. Carregar trace. Rodar find_problem(). Descobrir exatamente qual módulo falhou. Responder ao cliente com humildade: 'Achamos o bug no módulo X, corrigimos.'"

**Q7 Bonus: Qual padrão implementar PRIMEIRO?**
- Resposta esperada: "Trace Reading. Porque sem visibilidade, você não sabe o que está quebrado. Com traces, você consegue debugar Gen/Eval/Contracts/Rubric. Visibilidade é foundational."

---

## 📖 Leitura Complementar

### Dentro do Projeto

- `01-generator-evaluator-pattern.md` - Teoria completa de Gen/Eval
- `02-sprint-contracts.md` - Contratos em profundidade
- `03-rubric-design.md` - Design de rubrics avançados
- `04-trace-reading.md` - Diagnóstico em produção
- `case-studies.md` - Retro Game Maker (case study completo)
- `GLOSSARY.md` - Definições de todos os termos

### Antes de Nível 3

- Releia `nivel-1-koda.md` (contexto dos 3 problemas de Nível 1)
- Estude `PROMPTS-02-knowledge-graphs.md` (visualizações dos 4 padrões)
- Prepare-se para `PROMPTS-04-case-studies.md` (casos reais)

### Comunidade

- Slack: #long-running-agents (dúvidas técnicas)
- Retrospectiva semanal: toda sexta, 16h
- Mentoring: Nível 2 mentoram Nível 1

---

**Você completou Nível 2: Padrões Avançados! 🎉**

Agora você é capaz de:
- ✅ Gerar múltiplas opções e avaliar
- ✅ Coordenar módulos com contratos
- ✅ Avaliar qualidade em múltiplas dimensões
- ✅ Diagnosticar problemas completos
- ✅ Planejar refatoração arquitetural
- ✅ Implementar transformação em produção

**Tempo estimado:** 150 minutos de leitura + 10 horas de exercícios = 11.5 horas total

**Pronto para Nível 3?** Abra `PROMPTS-03-exercises.md` para os exercícios de Nível 3, ou espere pela seção `nivel-3-koda.md`! 🚀

---

*Documento: KODA Applications Level 2 | FutanBear Technical Team | Maio 2026*
*Versão: 1.0 | Autores: Fernando + Team | Status: Production Ready*

---

**Você está começando Nível 2: Padrões Avançados! 🎉**

*Documento: KODA Applications Level 2 | FutanBear Technical Team | Maio 2026*
