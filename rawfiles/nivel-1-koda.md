# 🎯 KODA em Ação: Aplicando Conceitos de Nível 1
## Da Teoria à Prática - Long-Running Agents no Mundo Real do KODA

**Tempo Estimado:** 30-45 minutos  
**Nível:** 1 - Conceitos Fundamentais  
**Pré-requisitos:** Ter completado os 3 módulos de Nível 1  
**Status:** 🟢 CRÍTICO - Bridge entre teoria e prática KODA  
**Data de Criação:** Maio 2026  

---

## 📖 Prólogo: A Jornada de KODA

Você conheceu Fernando, o fundador da KODA. Ele não apenas construiu um sistema de recomendação de produtos - ele construiu um **agente que precisa estar sempre conectado com seus clientes**, conversando naturalmente por horas, entendendo necessidades complexas, mantendo histórico de preferências, e gerando recomendações que mudam vidas de pessoas.

Quando Fernando começou, ele tinha uma visão clara:

> *"Queremos que KODA seja como um amigo de confiança que o cliente pode chamar no WhatsApp a qualquer momento. Não um chatbot que esquece tudo após 5 minutos. Um verdadeiro agente que cresce junto com o cliente."*

Mas havia um problema. Os agentes de IA naturalmente **perdem o foco**. Eles esquecem. Ficam lentos. Fazem recomendações contraditórias. Aprovam pedidos errados.

Foi quando Fernando percebeu: **"Os 3 problemas de Nível 1 não são apenas teóricos. Eles estão acontecendo AGORA no KODA, afetando clientes reais."**

Este módulo é sobre **como você vai resolver isso**. Como vai transformar teoria em ação. Como vai fazer KODA ser mais confiável, rápido e eficiente.

---

## 🎯 Objetivos Deste Módulo

Ao final, você será capaz de:

- ✅ **Diagnosticar** qual dos 3 problemas de Nível 1 está afetando uma conversa KODA
- ✅ **Aplicar** padrões de token budgeting em features reais do KODA
- ✅ **Desenhar** um harness básico para uma feature do KODA
- ✅ **Avaliar** uma conversa KODA e propor melhorias simples
- ✅ **Documentar** decisões de design usando conceitos de Nível 1

---

## 🔍 Parte 1: Diagnosticando os 3 Problemas no KODA Real

### Cenário: Uma Conversa de 2 Horas que Deu Errado

Vamos analisar uma conversa real do KODA (simplificada). Você consegue identificar os 3 problemas?

```
======================== CONVERSA KODA ========================

14:30 - Cliente: "Oi KODA! Procuro suplemento para ganhar massa muscular."
        KODA: "Ótimo! Vou ajudar. Você tem alguma alergia ou restrição?"

14:31 - Cliente: "Sou intolerante à lactose, alérgico a amendoim, e prefiro sabor de chocolate"
        KODA: [Registra] ✓ Entendido. Buscando produtos...
        KODA: "Encontrei 3 ótimas opções sem lactose e sem amendoim:
               1. Whey Isolado Chocolate - R$ 89,90
               2. Whey Vegano Chocolate - R$ 95,00  
               3. BCAA Chocolate - R$ 45,00
               Qual você prefere?"

14:35 - Cliente: "Legal! E qual tem melhor relação preço/benefício?"
        KODA: "Recomendo o BCAA por R$ 45. Melhor custo-benefício!"
        Cliente: "Blz, anoto aqui..."

[Conversa continua com dúvidas sobre frete, estoque, promoções...]

15:45 - [1 hora e 15 minutos depois]
        Cliente: "Então, qual produto você tinha recomendado mesmo?"
        KODA: "Recomendo o Whey Isolado Chocolate - R$ 89,90!"
        Cliente: "Mas você não tinha dito que era caro e que o BCAA era melhor?"
        KODA: "Ah, verdade, desculpe. O BCAA é melhor. Compra o BCAA."

16:15 - [30 minutos depois]
        Cliente: "Uma última dúvida: esse produto que você recomendou é mesmo sem lactose?"
        KODA: "Sim, é sem lactose!"
        [Mas na verdade era COM lactose - KODA já tinha esquecido da alergia]
        
        Cliente compra, recebe, sofre reação alérgica. 😞

16:45 - [Reclamação]
        Cliente: "KODA, você me recomendou um produto COM lactose???"
        KODA: "Desculpe, houve um erro. Vou verificar..."
```

---

### 🔎 Diagnóstico Detalhado

#### **Problema 1: Context Amnesia** ❌
- **Manifesto em:** KODA esqueceu que o cliente era intolerante à lactose
- **Por quê?** Conversas longas (90+ minutos) fazem informações críticas "envelhecerem" no contexto
- **Token perspective:** A alergia foi mencionada nos primeiros 30 tokens da conversa. 90 minutos depois, está em 45.000+ tokens atrás. Quando KODA processa a pergunta final, essas informações estão "borradas"

#### **Problema 2: Token Budgeting Inadequado** 💸
- **Manifesto em:** Respostas ficam mais curtas/genéricas conforme a conversa avança
- **Por quê?** O token budget foi gasto mantendo histórico completo. Não há espaço reservado para "pensar bem"
- **Números reais:**
  - Minuto 15: KODA tem 150K tokens livres (Sonnet 4.6) → Respostas longas, pensadas
  - Minuto 75: KODA tem 50K tokens livres → Respostas mais curtas, menos contexto considerado
  - Minuto 105: KODA tem 20K tokens livres → Respostas genéricas, esquece detalhes

#### **Problema 3: Padrões de Harness Fraco** 🏗️
- **Manifesto em:** KODA não tem mecanismo para verificar recomendações contra dados críticos do cliente
- **Por quê?** Não há "harness" que force KODA a revisar alergia antes de confirmar produto
- **O que falta:** Um padrão simples que diga: "Antes de finalizar qualquer recomendação, SEMPRE veja se o cliente tem alergias"

---

### ✅ Como Seria Com Nível 1 Aplicado

Se Fernando e seu time tivessem aplicado os conceitos de Nível 1:

```
PROBLEMA 1 → SOLUÇÃO: Separar informações críticas
- Alergia é "Estado Crítico", não fica submersa no histórico
- KODA mantém lista separada: [alergia: lactose], [alergia: amendoim]
- Antes de recomendar, consulta SEMPRE essa lista

PROBLEMA 2 → SOLUÇÃO: Token Budgeting Agressivo
- Reserve sempre 20K tokens de buffer para "pensar bem" em decisões críticas
- Comprima histórico após 45 minutos: sumarize as primeiras 30 minutos em 2-3 frases
- Resultado: Mesmo após 105 minutos, KODA tem espaço para pensar

PROBLEMA 3 → SOLUÇÃO: Harness Pattern Simples
- Antes de recomendar um produto:
  1. Verificar alergia e restrições do cliente
  2. Validar que o produto NÃO tem essas restrições
  3. Então recomendar
- Sem isso, não há recomendação. Simples assim.
```

---

## 💡 Parte 2: Aplicando Token Budgeting ao KODA

### O Orçamento Típico do KODA

**Contexto:** Uma conversa de cliente em uma terça-feira à noite.

```
CONTEXTO TOTAL (Claude Sonnet 4.6): 200.000 tokens

COMPOSIÇÃO TÍPICA DA CONVERSA:

1. SYSTEM PROMPT (Instruções para KODA)
   - Persona: "Você é KODA, um assistente..."
   - Regras: "Sempre considere alergia, sempre seja simpático..."
   - Tamanho: ~3.000 tokens

2. HISTÓRICO DE CONVERSA (Acumula com o tempo)
   - Minuto 15: ~5.000 tokens
   - Minuto 45: ~15.000 tokens
   - Minuto 75: ~25.000 tokens
   - Minuto 105: ~35.000 tokens

3. ESTADO DO CLIENTE (Informações estruturadas)
   - Perfil: nome, histórico de compras, preferências
   - Tamanho: ~2.000 tokens

4. CONTEXTO DE PRODUTO (Catálogo, promoções)
   - Produtos que podem interessar ao cliente
   - Tamanho: ~5.000 tokens

5. BUFFER PARA RESPOSTA (Para o modelo gerar resposta de qualidade)
   - Tamanho mínimo necessário: ~10.000 tokens

────────────────────────────────────────────
TOTAL NECESSÁRIO: 3.000 + 35.000 + 2.000 + 5.000 + 10.000 = 55.000 tokens
DISPONÍVEL: 200.000 tokens
SOBRA: 145.000 tokens ✓ Ainda temos espaço!
```

### 🚨 O Problema: Conversas Muito Longas

Mas e se a conversa durar **3-4 horas** (não é raro em fintech)?

```
CENÁRIO PESSIMISTA (Conversa de 4 horas):

1. SYSTEM PROMPT: 3.000 tokens
2. HISTÓRICO COMPLETO: ~50.000 tokens (4 horas = muitas trocas)
3. ESTADO DO CLIENTE: 2.000 tokens
4. CONTEXTO DE PRODUTO: 5.000 tokens (precisa buscar produtos atualizados)
5. BUFFER PARA RESPOSTA: 10.000 tokens (mínimo)

TOTAL: 70.000 tokens

MAS ESPERA... O que acontece se o cliente pede para comparar com produtos de ontem?
- Você precisa de histórico de produtos antigos: +8.000 tokens
- Você precisa de histórico de conversa anterior: +15.000 tokens
- Você quer que KODA "pense" sobre a melhor comparação: precisa de mais buffer

NOVO TOTAL: ~100.000 tokens
SOBRA: 100.000 tokens ← Ainda OK, mas apertado
```

### 💰 Estratégia de Budget do KODA

A equipe KODA implementa esta estratégia (você precisa conhecer):

#### **Nível 1: Conversas até 2 horas** ✓
**Budget:** 
- Manter histórico completo: SIM
- Buffer de resposta: 15.000 tokens
- Estado do cliente: Sempre atualizado
- **Resultado:** Performance perfeita

#### **Nível 2: Conversas de 2-4 horas** ⚠️
**Budget:**
- Comprimir histórico antigo em 5-7 resumos
- Buffer de resposta: Reduzir para 12.000 tokens
- Estado do cliente: Cache separado (não no histórico)
- **Resultado:** Performance boa, sem degradação

#### **Nível 3: Conversas 4+ horas** 🚨
**Budget:**
- Mover conversa para múltiplos "sprints" (Nível 2 topic)
- Ou: Resumir agressivamente e fazer "reset contextual"
- Buffer: 10.000 tokens (mínimo crítico)
- **Resultado:** Funciona, mas requer padrões avançados

---

### 📊 Exercício: Calcule o Budget de Uma Feature KODA

**Cenário:** Feature "Consultor de Promoção" - Cliente ligou para KODA perguntar sobre promoções válidas hoje.

```
System Prompt: 2.000 tokens
Histórico: (Assumir 20 minutos de conversa) ~7.000 tokens
Promoções atuais (catálogo): 4.000 tokens
Pedidos recentes do cliente: 3.000 tokens
Buffer para resposta: ? tokens [VOCÊ DECIDE]
────────────────────────────
Total necessário: ?

Usando Claude Sonnet 4.6 (200.000 tokens totais):
TOKENS SOBRA: 200.000 - (?) = ?

PERGUNTA: Esse budget é suficiente para conversa de 2 horas?
```

**Resposta no final do módulo** ↓

---

## 🏗️ Parte 3: Padrões de Harness no KODA

### O Que É um Harness no KODA?

Um **harness** é um padrão estruturado que garante que KODA execute uma tarefa corretamente, mesmo sob pressão de contexto grande.

É como um **"railguard"** - impede que KODA saia do trilho, mesmo que esteja "cansado" (contexto grande).

### Exemplo 1: Harness para "Recomendação de Produto"

**Sem Harness** (O que vimos acima - deu errado):
```
Cliente: "Qual produto você recomenda?"
KODA: [Pensa sobre tudo que o cliente falou]
KODA: "Recomendo X!"
```

**Com Harness** (O padrão correto):
```
Cliente: "Qual produto você recomenda?"
KODA executa o HARNESS:

ETAPA 1 - VALIDAR RESTRIÇÕES
  ✓ Cliente tem alergia a lactose? → SIM, lembrar
  ✓ Cliente tem alergia a amendoim? → NÃO
  ✓ Cliente quer sabor chocolate? → SIM, lembrar
  
ETAPA 2 - BUSCAR PRODUTOS VÁLIDOS
  ✓ Filtrar catálogo: [sem lactose, sem amendoim, chocolate]
  ✓ Resultado: 3 produtos válidos
  
ETAPA 3 - RANQUEAR POR CRITÉRIOS
  ✓ Qual tem melhor relação preço/benefício?
  ✓ Qual tem melhor avaliação?
  ✓ Qual está em promoção?
  
ETAPA 4 - VALIDAR RECOMENDAÇÃO
  ✓ Produto recomendado NÃO tem lactose? ✓ SIM
  ✓ Produto recomendado NÃO tem amendoim? ✓ SIM
  ✓ Produto recomendado é chocolate? ✓ SIM
  
ETAPA 5 - COMUNICAR
  "Recomendo o Whey Isolado Chocolate porque:
   - Não tem lactose (você é intolerante)
   - Não tem amendoim (você é alérgico)
   - Sabor chocolate (sua preferência)
   - Melhor custo-benefício (R$ 89,90)"
```

**Por que funciona?**
1. Força KODA a lembrar restrições (Problema 1 ✓)
2. Usa pouco token (cada etapa é simples) (Problema 2 ✓)
3. Valida antes de recomendar (Problema 3 ✓)

---

### Exemplo 2: Harness para "Checkout com Validação"

**Cenário:** Cliente está pronto para pagar. Precisa validar dados.

```
HARNESS: Checkout Seguro

ETAPA 1 - CONFIRMAR ENDEREÇO
  "Confirma seu endereço? [Mostrar endereço do perfil]"
  
ETAPA 2 - CONFIRMAR ITENS
  "Estes são os itens que vai levar?"
  [Listar tudo que foi recomendado]
  
ETAPA 3 - CONFIRMAR RESTRIÇÕES
  "Nenhum desses itens tem lactose? Nenhum tem amendoim?"
  [Cliente confirma]
  
ETAPA 4 - CONFIRMAR PREÇO FINAL
  "Subtotal: R$ X | Frete: R$ Y | Total: R$ Z. OK?"
  
ETAPA 5 - PROCESSAR PAGAMENTO
  "Processando... ✓ Pedido confirmado!"
```

**Resultado:** Mesmo que KODA esteja "cansado" após 2 horas de conversa, o harness força que execute 5 validações antes de processar.

---

### 🎯 Princípios de um Bom Harness

1. **Simplicidade:** Cada etapa deve ser um padrão simples (validar, buscar, ranquear)
2. **Validação:** Deve sempre validar antes de agir (especialmente em dados críticos)
3. **Comunicação:** Deve ser claro ao cliente o que está acontecendo
4. **Recuperação:** Se algo der errado, deve perguntar ao cliente, não assumir
5. **Token-eficiência:** Não deve gastar muitos tokens por etapa

---

## 📋 Parte 4: Documentando Decisões de Design

### Template: Decision Record para KODA

Quando você propõe uma mudança no KODA, deve documentar assim:

```markdown
# Decision Record: [Nome da Feature]

**Data:** [Data]
**Autor:** [Seu Nome]
**Status:** [Proposta / Implementando / Implementado]

## 🎯 Problema

[Descrever qual dos 3 problemas de Nível 1 esta decision resolve]

Exemplo:
"Cliente com intolerância à lactose estava recebendo recomendações 
COM lactose em conversas longas. Problema 1 (Context Amnesia)."

## 💡 Solução Proposta

[Descrever a solução com padrões de Nível 1]

Exemplo:
"Implementar Harness de Validação de Restrições:
- Manter lista separada de [alergia/restrição] fora do histórico
- Antes de recomendar produto, validar contra essa lista
- Padrão: CHECK → FILTER → RECOMMEND → VALIDATE → COMMUNICATE"

## 📊 Token Impact

[Calcular impacto em token budget]

Exemplo:
"Adicionar validação: +500 tokens por recomendação
Ganho de eficiência (sem retrabalho): -2.000 tokens
Impacto líquido: -1.500 tokens por conversa ✓"

## ✅ Critérios de Sucesso

[Como você vai saber se funciona?]

- [ ] Taxa de erros de alergia reduz para 0%
- [ ] Conversas de 2h+ mantêm performance
- [ ] Tempo de resposta não aumenta

## 🔗 Referência a Nível 1

Conceitos usados:
- ☑ Context Management (Problema 1)
- ☑ Token Budgeting (Problema 2)
- ☑ Basic Harness Patterns (Problema 3)
```

### Exemplo Real: Decision Record para Feature de KODA

```markdown
# Decision Record: Alergia-First Architecture para Recomendações

**Data:** Maio 2026
**Autor:** Time KODA
**Status:** Implementado

## 🎯 Problema

Customer relatou reação alérgica a produto recomendado por KODA após 105 minutos
de conversa. Root cause: Context Amnesia (Problema 1 - Nível 1).

Alergia foi mencionada no início da conversa (~500 tokens), recomendação aconteceu
no final (~35.000 tokens depois). Em conversas longas, informação crítica fica
"borrada" no contexto.

## 💡 Solução Proposta

Implementar "Camada de Restrições Separada":

1. **Separar dados críticos do histórico:**
   - Crie dicionário estruturado: {alergias: [...], restrições: [...]}
   - NUNCA misture isso com histórico de conversa
   - Atualize em tempo real conforme cliente fala

2. **Padrão de Recomendação (Harness):**
   ```
   RECOMMENDED_PRODUCT = filter(catalog, restrictions=client.restrictions)
   for product in RECOMMENDED_PRODUCT:
     validate(product.ingredients NOT IN client.restrictions)
     if valid: recommend(product)
     else: skip()
   ```

3. **Token Budget:**
   - Manter restrições separadas: +1.000 tokens (one-time)
   - Filtro de validação: +300 tokens por recomendação
   - Economia de retrabalho: -2.000 tokens por conversa
   - **Impacto: -700 tokens por conversa média**

## ✅ Resultados (6 semanas)

- Taxa de erros de alergia: 2.1% → 0.0% ✓
- Tempo de recomendação: 3.2s → 2.8s ✓
- Satisfação do cliente: 4.2 → 4.7 / 5.0 ✓
- Conversas 2h+: Performance mantida ✓

## 🔗 Referência a Nível 1

- ✅ Context Management: Resolvido com separação de camadas
- ✅ Token Budgeting: Budget negativo = melhora de eficiência
- ✅ Basic Harness: Pattern de validação aplicado
```

---

## ✍️ Parte 5: Exercícios Práticos

### Exercício 1: Diagnóstico de Conversa Quebrada

**Você recebeu esta trace de um cliente insatisfeito:**

```
14:00 - Cliente: "Oi KODA! Procuro BCAA para treinar melhor"
        KODA: "Ótimo! Vou encontrar a melhor opção para você."

14:02 - Cliente: "Tenho restrição orçamentária - máximo R$ 50"
        KODA: "Entendido! Filtrando produtos até R$ 50..."

14:05 - Cliente: "E prefiro sabor morango ou abacaxi"
        KODA: "Perfeito! Mostro você as melhores opções..."

[Conversa continua por 1h15min com dúvidas sobre frete, promoção, etc.]

15:20 - Cliente: "Certo, vou comprar! Qual era o produto que você recomendou?"
        KODA: "Recomendo o BCAA Premium Morango - R$ 120!"
        Cliente: "MAS VOCÊ FALOU QUE ERA ATÉ R$ 50!!!"
```

**Suas tarefas:**

1. **Identifique qual dos 3 problemas aconteceu** (ou múltiplos?)
   - Problema 1: Context Amnesia? 
   - Problema 2: Token Budget?
   - Problema 3: Harness fraco?

2. **Explique o mecanismo técnico**
   - Por que KODA "esqueceu" o budget de R$ 50?

3. **Proponha um Harness**
   - Como estruturar a recomendação para nunca mais acontecer?

**Sua resposta:**

```
[Escreva aqui suas análises]
```

---

### Exercício 2: Calcule o Budget (Continuação)

Voltando ao exercício anterior sobre "Consultor de Promoção":

```
System Prompt: 2.000 tokens
Histórico: (20 minutos de conversa) ~7.000 tokens
Promoções atuais: 4.000 tokens
Pedidos recentes do cliente: 3.000 tokens
Buffer para resposta: ??? ← VOCÊ DEFINE

Contexto disponível: 200.000 tokens (Sonnet 4.6)
```

**Questão 1:** Qual é o buffer mínimo que você alocaria?
- [ ] 5.000 tokens
- [ ] 10.000 tokens
- [ ] 15.000 tokens
- [ ] 20.000 tokens

**Questão 2:** Se a conversa durar 2 horas (não 20 min), qual é o novo cálculo?
```
System Prompt: 2.000 tokens
Histórico: (120 minutos de conversa) ~40.000 tokens
Promoções atuais: 4.000 tokens
Pedidos recentes do cliente: 3.000 tokens
Buffer para resposta: ???

Total necessário: ???
Está OK com 200.000? SIM / NÃO
Se NÃO, qual estratégia usar? 
```

---

### Exercício 3: Design Your Own Harness

**Sua missão:** KODA precisa validar pedidos antes de enviar para processamento.

Crie um Harness que força KODA a validar 5 pontos críticos antes de marcar o pedido como "confirmado".

**Template:**

```
# Harness: Order Validation

ETAPA 1: [Seu ponto 1]
  [ ] Validação específica aqui
  
ETAPA 2: [Seu ponto 2]
  [ ] Validação específica aqui
  
ETAPA 3: [Seu ponto 3]
  [ ] Validação específica aqui
  
ETAPA 4: [Seu ponto 4]
  [ ] Validação específica aqui
  
ETAPA 5: [Seu ponto 5]
  [ ] Validação específica aqui

RESULTADO FINAL:
Se todas as 5 etapas forem ✓, marca como "confirmado"
Se qualquer uma for ✗, pede clarificação ao cliente
```

---

## 🎓 Parte 6: Checklist de Implementação

### Para Você, como Integrante do Time KODA

Se você foi designado para melhorar uma feature do KODA, use este checklist:

#### **Semana 1: Diagnóstico**
- [ ] Identifiquei qual dos 3 problemas essa feature tem
- [ ] Coletei traces de conversas que falharam
- [ ] Calculei o token budget atual da feature
- [ ] Documentei em um Decision Record

#### **Semana 2: Design**
- [ ] Desenhei um Harness para resolver o problema
- [ ] Validei que o Harness não quebra o token budget
- [ ] Documentei cada etapa do Harness
- [ ] Propus testes para validar

#### **Semana 3: Implementação**
- [ ] Implementei o Harness no código
- [ ] Testei com conversas reais do KODA
- [ ] Validei que conversas de 2h+ funcionam
- [ ] Documentei qualquer variação do design

#### **Semana 4: Validação**
- [ ] Coletei métricas de sucesso
- [ ] Comparei antes/depois
- [ ] Documentei lições aprendidas
- [ ] Atualizei o Decision Record com resultados

---

## 🔗 Parte 7: Mapeando Para os Próximos Níveis

### O Que Você Aprendeu em Nível 1 ✓
- Os 3 problemas fundamentais de long-running agents
- Como calcular e gerenciar token budgets
- Padrões básicos de Harness

### O Que Vem em Nível 2 (Preview) 🔜
- **Generator/Evaluator Pattern:** Como KODA pode gerar múltiplas opções e avaliá-las
- **Sprint Contracts:** Como definir "promessas" entre componentes de KODA
- **Rubric Design:** Como avaliar se uma recomendação é "boa"
- **Trace Reading:** Como ler logs do KODA e entender por que algo falhou

### Aplicação em Nível 2 para KODA
Você aprenderá a:
- Gerar 3 recomendações de produto e deixar KODA escolher a melhor
- Definir contratos entre "módulo de busca" e "módulo de ranking"
- Criar rubrics que avaliam se uma recomendação é segura (sem alergias, etc.)
- Ler traces quando algo der errado e identificar exatamente aonde

---

## 📚 Resumo Visual: Os 3 Problemas e Soluções

```
┌─────────────────────────────────────────────────────────────┐
│ PROBLEMA 1: Context Amnesia                                 │
├─────────────────────────────────────────────────────────────┤
│ ❌ O que acontece: KODA esquece informações antigas         │
│ 🔍 Causa: Contexto muito grande, informação fica borrada   │
│ ✅ Solução Nível 1: Separar dados críticos do histórico     │
│ 🎯 Exemplo KODA: Alergia em camada separada, não no chat   │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ PROBLEMA 2: Token Budgeting                                 │
├─────────────────────────────────────────────────────────────┤
│ ❌ O que acontece: Respostas ficam lentas/genéricas         │
│ 🔍 Causa: Tokens gastos, pouco espaço para "pensar bem"   │
│ ✅ Solução Nível 1: Planejar alocação de tokens            │
│ 🎯 Exemplo KODA: Reservar sempre 15K tokens de buffer      │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ PROBLEMA 3: Weak Harness Patterns                           │
├─────────────────────────────────────────────────────────────┤
│ ❌ O que acontece: Erros catastróficos (alergias, preços)  │
│ 🔍 Causa: KODA sem estrutura, aprova tudo que pensa       │
│ ✅ Solução Nível 1: Padrões com validação em cada etapa   │
│ 🎯 Exemplo KODA: 5-step validation antes de recomendar    │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Próximos Passos

### Imediatamente (Esta Semana)
1. Escolha **UMA feature do KODA** que você quer melhorar
2. Colete **3-5 conversas** que falharam
3. Identifique qual dos 3 problemas cada uma tem
4. Crie um **Decision Record**

### Próxima Semana
1. Desenhe um **Harness** para resolver o problema
2. Calcule o **impacto em tokens**
3. Propus as mudanças para o time
4. Comece a implementação

### Antes de Nível 2
1. Você deve ter **uma feature** parcialmente melhorada
2. Deve saber **ler traces** do KODA
3. Deve entender **seu token budget** intimamente
4. Pronto para aprender **Generator/Evaluator**

---

## ✨ Palavras Finais: Respeito à Jornada

Quando Fernando começou a KODA, ele não conhecia esses 3 problemas. Ele descobriu porque **observou seus agentes falhando no mundo real**. Isso é coragem.

Você, agora, tem vantagem: **você conhece os problemas antes de implementar**.

Cada feature que você melhorar no KODA usando essas ideias **não é apenas um bug fix**. É você honrando a visão de Fernando de criar um agente que **nunca abandona seus clientes**, que **lembra de alergias**, que **faz recomendações que salvam tempo**.

Como Fernando aprecia: **simplicidade que resolve problemas complexos**.

Você está pronto. Vamos?

---

## 📎 Apêndice: Respostas dos Exercícios

### Exercício 2: Resposta do Budget de Promoção

```
System Prompt: 2.000 tokens
Histórico (20 min): 7.000 tokens
Promoções: 4.000 tokens
Pedidos recentes: 3.000 tokens
────────────────────────────
Subtotal: 16.000 tokens

Buffer recomendado: 15.000 tokens
[Por quê? Deixar espaço para KODA "pensar" sobre melhor promoção]

TOTAL: 31.000 tokens
DISPONÍVEL: 200.000 tokens
SOBRA: 169.000 tokens ✓ Excelente!

────────────────────────────

SE CONVERSA DURAR 2 HORAS:

System Prompt: 2.000 tokens
Histórico (120 min): ~40.000 tokens
Promoções: 4.000 tokens
Pedidos: 3.000 tokens
────────────────────────────
Subtotal: 49.000 tokens

Buffer necessário: 15.000 tokens
TOTAL: 64.000 tokens
DISPONÍVEL: 200.000 tokens
SOBRA: 136.000 tokens ✓ Ainda excelente!

CONCLUSÃO: Mesmo em 2 horas, o budget está OK.
Mas se fosse 4+ horas, você precisaria comprimir histórico (Nível 2).
```

---

## 📖 Leitura Complementar

- **Volta a Nível 1:**
  - `01-why-agents-lose-plot.md` - Entender os 3 problemas em profundidade
  - `02-token-budgeting.md` - Aprender token budgeting matematicamente
  - `03-basic-harness-patterns.md` - Ver exemplos de Harness

- **Prepare para Nível 2:**
  - Leia `QUICK_START.md` da seção Nível 2
  - Estude `generator-evaluator-pattern.md`

---

**Você completou Nível 1: Aplicações KODA! 🎉**

Agora você pode:
- ✅ Diagnosticar problemas em conversas do KODA
- ✅ Calcular tokens budgets reais
- ✅ Desenhar Harnesses simples
- ✅ Documentar decisões como um expert

**Tempo estimado:** 45 minutos (ou mais se fizer os exercícios profundamente)

**Pronto para Nível 2?** Abra `PROMPTS-02-knowledge-graphs.md` ou passe direto para os exercícios de Nível 2! 🚀

---

*Documento: KODA Applications Level 1 | FutanBear Technical Team | Maio 2026*
