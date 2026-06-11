---
title: "Rubric Design: Como Ensinar um Evaluator a Ser Crítico e Justo"
type: curriculum-lesson
nivel: 2
aliases: ["design rubricas", "criação rubricas", "rubric design", "critérios avaliação"]
tags: [curriculo-conteudo, nivel-2, padroes-praticos, criterios-mensuraveis, avaliacao-qualitativa, dimensoes-de-avaliacao, pesos-e-thresholds, escalas-de-avaliacao, exemplos-ancora, feedback-estruturado, calibracao-de-evaluator, seguranca-alergica]
relates-to: ["[[docs/canonical/split-brain-planning-review|Split-Brain Planning Review]]", "[[curriculum/05-core-concepts/08-evaluation-rubrics|Evaluation Rubrics Concept]]"]
last_updated: 2026-06-10
---
# 📏 Rubric Design: Como Ensinar um Evaluator a Ser Crítico e Justo
## Transformando Intuição Vaga em Critérios Mensuráveis

**Tempo Estimado:** 90 minutos  
**Nível:** 2 - Padrões Práticos  
**Pré-requisitos:** 
- ✅ Nível 1 completo (Context Management, Token Budgeting, Basic Harness)
- ✅ `01-generator-evaluator-pattern.md` (entender o padrão Generator/Evaluator)
- ✅ `02-sprint-contracts.md` (entender como fazer acordos com o Evaluator)

**Status:** 🟢 CRÍTICO - Transforma Evaluators de "sim/não" para "por quê sim/não"  
**Data de Criação:** Maio 2026  
**Pertence a:** `02-nivel-2-practical-patterns/`

---

## 🎯 O Que Você Vai Aprender

Neste módulo, você entenderá como transformar **intuições vagas** sobre qualidade em **critérios mensuráveis** que um Evaluator pode usar para avaliar o trabalho de um Generator com consistência, justiça e rigor.

✅ **Por que Rubrics são tão críticos** — sem eles, seu Evaluator é só um "sim/não" automático  
✅ **Anatomia de um bom Rubric** — critérios, dimensões, exemplos, pesos  
✅ **Como desenhar Rubrics** — passo a passo, do zero ao funcional  
✅ **Exemplos concretos em JSON** — você verá rubrics reais que funcionam no KODA  
✅ **Erros que as pessoas cometem** — e como evitá-los  
✅ **Exercícios práticos** — desenhe seus próprios rubrics  

Ao final, você terá uma **ferramenta mental** para avaliar qualidade em qualquer contexto, não apenas IA. Essa habilidade é transferível: você pode usar isso em code review, design critique, customer feedback — em qualquer lugar onde precisa separar "bom" de "ruim" de forma justa.

---

## 🔗 Como Esta Seção Se Conecta

### Relação com Nível 1
Em Nível 1, você aprendeu que agentes sofrem de **3 problemas fundamentais**:
1. Context Amnesia
2. Planning Paralysis  
3. Harness Fraco

Você também aprendeu que um **Harness moderno** resolve isso através de checkpoints e verificação.

### Relação com Generator/Evaluator
No arquivo anterior (`01-generator-evaluator-pattern.md`), você aprendeu que:
- **Generator** cria/gera uma solução
- **Evaluator** avalia se a solução é boa
- **Separação de responsabilidades** evita sycophancy (tendência do agente agradar a si mesmo)

**Mas aquele arquivo deixou uma questão aberta:** "Como exatamente o Evaluator **sabe** se algo é bom ou ruim?"

**Rubrics são a resposta.**

### Relação com Sprint Contracts
No arquivo anterior (`02-sprint-contracts.md`), você aprendeu que:
- **Generator e Evaluator fazem um contrato** antes de começar
- O contrato especifica: "Pronto significa X, Y, Z"
- Ambos concordam em um **critério de sucesso**

**Rubrics são a ferramenta que formaliza esse contrato.**

---

## 📊 Posicionamento no Programa

| Tópico | Arquivo | Aprende Sobre... |
|--------|---------|-----------------|
| Padrão Gen/Eval | `01-generator-evaluator-pattern.md` | **O quê** — separação de responsabilidades |
| Sprint Contracts | `02-sprint-contracts.md` | **Quando** e **quanto** — acordos antes de começar |
| **Rubric Design** | **este arquivo** | **Como** — critérios específicos para avaliar |
| Trace Reading | `04-trace-reading.md` | **Por quê** — debugar quando rubrics falham |

---

## 💡 Por Que Agora?

Se você já tem Generator/Evaluator funcionando, por que estudar Rubrics **agora** (Seção 3 do Nível 2)?

Porque a **qualidade do seu Evaluator é limitada pela clareza de seus critérios.**

- ❌ **Rubric ruim:** "Avalie se a recomendação é boa"
  - Resultado: Evaluator fica confuso, aprova coisas ruins, rejeita coisas boas
  - Confiabilidade: ~40% (pior que random!)

- ✅ **Rubric bom:** "Avalie se: (1) produto existe em inventory, (2) preço é atual, (3) compatível com restrições do cliente, (4) explicação é clara"
  - Resultado: Evaluator sabe exatamente o que procurar
  - Confiabilidade: ~95%

**A diferença entre "Evaluator que funciona 40% das vezes" e "Evaluator que funciona 95% das vezes" é simplesmente a qualidade do rubric.**

---

## 📚 Estrutura Este Módulo

```
1. Introdução e Contexto (✓ você está aqui)
   ↓
2. Prólogo - A História Real
   "Um pedido desastre que poderia ter sido evitado com bom rubric"
   ↓
3. Fundamentos de Rubrics
   "O que é? Por que funciona? Como é diferente de intuição?"
   ↓
4. Elementos de um Bom Rubric
   "Critérios, dimensões, exemplos, pesos — a anatomia"
   ↓
5. Como Desenhar Rubrics - Passo a Passo
   "Guia prático: do zero ao funcional"
   ↓
6. Exemplos JSON Concretos
   "Veja rubrics reais que funcionam no KODA"
   ↓
7. Erros Comuns
   "Aprenda com os erros que outras pessoas cometeram"
   ↓
8. Exercícios Práticos
   "Pratique desenhando seus próprios rubrics"
   ↓
9. Aplicação KODA
   "Como KODA usa rubrics hoje e como você pode melhorar"
   ↓
10. Próximos Passos
    "Como rubrics conectam com o resto do programa"
```

---

## ⏱️ Cronograma Sugerido

Se você tem 90 minutos para este módulo:

| Seção | Tempo | Atividade |
|-------|-------|-----------|
| Prólogo | 10 min | Ler história e entender o problema |
| Fundamentos | 15 min | Entender conceitos-chave |
| Elementos | 15 min | Aprender anatomia de um rubric |
| Como Desenhar | 15 min | Seguir passo a passo |
| Exemplos JSON | 10 min | Ver exemplos concretos |
| Erros Comuns | 10 min | Aprender o que evitar |
| Exercícios | 30-45 min | **Praticar** (a parte mais importante!) |

---

## 🎓 Critérios de Conclusão

Ao final deste módulo, você deve ser capaz de:

- [ ] Explicar **por que rubrics são críticos** para um Evaluator funcionar bem
- [ ] **Desenhar um rubric** para qualquer tarefa, do zero
- [ ] Reconhecer um **rubric ruim** e saber como melhorar
- [ ] Entender a **granularidade** — quando ser vago vs específico
- [ ] **Aplicar rubrics** ao KODA em contextos reais
- [ ] Completar **todos os 3 exercícios** com qualidade

---

## 🚀 Vamos Começar

Próximo: **Seção 2 — Prólogo: A História Real**

Nela, você verá uma situação real onde um Evaluator *poderia* ter evitado um desastre de negócio, mas não conseguiu porque **não tinha um rubric claro**. Essa história vai contextualizar por que estamos aprendendo isso.

---

**Seção 1 Completa** ✓  
Pronto para Seção 2? Diga "aprova" ou "ajusta" algo aqui primeiro. 👇
---

## 📖 Prólogo: O Pedido Que Poderia Ter Sido Salvo

### A Conversa Que Começou Bem

Era uma terça-feira em abril de 2026. Uma cliente chamada **Ana** entrou em conversa com KODA via WhatsApp:

```
14:15 - ANA
"Oi KODA! Preciso de whey protein. Tenho alergia a lactose, 
 e meu orçamento é apertado — máximo R$ 80 por mês."

KODA GENERATOR
"Perfeito, Ana! Encontrei 3 opções que se encaixam:

1. Whey Isolado SEM Lactose (marca XYZ) - R$ 79,90/mês
   → Zero carboidratos, 25g proteína por dose
   
2. Whey Vegano Premium (marca ABC) - R$ 85,00/mês
   → Plant-based, 20g proteína por dose
   
3. Whey Concentrado com Lactase (marca DEF) - R$ 45,00/mês
   → Tem enzima de lactose, então sem reação

Qual você prefere?"

ANA
"Adorei as opções! Vou com a #1 (R$ 79,90). 
 Super dentro do meu orçamento."

KODA GENERATOR
"Ótimo! Confirmando seu pedido:
 ✅ Produto: Whey Isolado SEM Lactose
 ✅ Preço: R$ 79,90/mês
 ✅ Alergia registrada: Lactose (sem risco)
 Vou processar seu pedido agora!"
```

**Até aqui, tudo perfeito.** O Generator:
- ✅ Ouviu a restrição de alergia
- ✅ Respeitou o orçamento (R$ 80)
- ✅ Ofereceu 3 opções seguras
- ✅ Processou a escolha da cliente

---

### Aqui Começa o Problema

Agora, 2 horas depois, o **Evaluator** entra em cena para verificar se o pedido está correto antes de ir para fulfillment:

```
EVALUATOR (Verificação Automática)
Verificando pedido #12847...

✓ Cliente: Ana Silva
✓ Produto selecionado: Whey Isolado SEM Lactose (marca XYZ)
✓ Preço do pedido: R$ 79,90

Conclusão do Evaluator: ✅ PEDIDO APROVADO

Motivo: Todos os campos estão preenchidos. Cliente escolheu 
um produto. Preço é válido. Parece bom!
```

**E o pedido segue para fulfillment.**

---

### A Disaster Silenciosa

3 dias depois, Ana recebe o produto. Abre a embalagem. **Lê a descrição do produto.**

E vê isto:

```
RÓTULO DO PRODUTO:
═══════════════════════════════════════════════════════════════
Whey Isolado SEM LACTOSE (Marca XYZ)
Ingredientes: Soro de leite (concentrado)...
               Aromatizante natural...
               Estabilizante E471...
               
⚠️  AVISO IMPORTANTE:
Este produto é preparado em INSTALAÇÃO que processa LEITE.
Risco de contaminação cruzada: BAIXO a MODERADO.

Para alérgicos severos: CONSULTE seu médico antes de usar.
═══════════════════════════════════════════════════════════════
```

Ana entra em pânico. **Ela tem alergia severa.** Ela escreve para KODA:

```
ANA (4 horas depois)
"KODA!!! Vocês cometeram um erro GRAVE! Eu falei que tinha 
 ALERGIA a lactose, e vocês recomendaram um produto que 
 foi processado em fábrica com LEITE! 
 
 Poderia ter tido uma REAÇÃO ALÉRGICA!
 
 Que falta de atenção! Quero REEMBOLSO TOTAL!"
```

---

### Análise do Desastre

**O que o Evaluator deveria ter verificado:**

| Critério | Que Deveria Fazer | O Que Realmente Fez |
|----------|------------------|-------------------|
| **Alergia** | Verificar: severidade é "severa"? | ✗ Só viu "tem alergia" |
| **Rótulo do Produto** | Ler informações de risco na embalagem | ✗ Não consultou rótulo |
| **Aviso de Contaminação** | Verificar se há risco de contaminação cruzada | ✗ Ignorou completamente |
| **Recomendação vs. Segurança** | Se alergia severa + risco de contaminação = ❌ REJEITAR | ✓ Aprovado!! |

**O Evaluator falhou não porque faltava inteligência, mas porque:**

> "Não tinha **critérios claros** para saber o que procurar."

Ele tinha uma **lista de verificação vaga:**
- "Campos preenchidos?" ✓
- "Preço é válido?" ✓
- "Produto existe?" ✓
- "Parece bom?" ✓✓✓

Mas nenhum critério específico sobre:
- "Se alergia = severa, qual é o risco de contaminação do produto?"
- "Há conflitos entre a descrição da alergia e o rótulo do produto?"
- "O produto é realmente seguro ou apenas tecnicamente correto?"

---

### O Insight Estratégico

Aqui está o ponto: **O Evaluator não era incompetente. Ele só não tinha instruções boas.**

Compare estes dois cenários:

#### ❌ Rubric Ruim (O que realmente aconteceu)
```
Verificar se o pedido está:
1. Preenchido completamente
2. Com preço válido
3. Produto existe
→ Se sim em todas: APROVAR
```

**Problema:** Muito vago. Não sabe o que é "bom".
**Resultado:** Aprova pedidos que violam a segurança do cliente.

#### ✅ Rubric Bom (O que deveria ter acontecido)
```
Verificar o pedido em 3 dimensões:

DIMENSÃO 1: DADOS BÁSICOS
✓ Cliente preenchido?
✓ Produto existe em inventory?
✓ Preço é válido?

DIMENSÃO 2: COMPATIBILIDADE COM CLIENTE
✓ Se cliente tem alergia, a descrição da alergia é "severa"?
  └─ Se SIM: verificar risco de contaminação do produto
✓ Se cliente tem restrição orçamentária, preço está ok?
✓ Se cliente tem preferência (ex: vegano), produto é vegano?

DIMENSÃO 3: SEGURANÇA DO PRODUTO
Se alergia severa:
  ✗ Se risco de contaminação cruzada = "moderado ou alto" → REJEITAR
  ✗ Se rótulo tem aviso alérgico → REJEITAR
  ✓ Se risco é "muito baixo" E sem avisos → APROVAR

→ Se passou em TODAS as 3 dimensões: APROVAR
→ Se falhou em QUALQUER critério: REJEITAR + dar feedback específico
```

**Com este rubric:**
- O Evaluator teria visto: "alergia = severa"
- Teria checado o rótulo: "risco de contaminação = MODERADO"
- Teria rejeitado o pedido: ❌ "Risco alérgico muito alto. Rejeitar e recomendar alternativas mais seguras."
- Ana nunca teria recebido um produto perigoso.

---

### A Consequência Real

**O que aconteceu:**

1. ❌ Ana recebeu um produto potencialmente perigoso
2. ❌ KODA perdeu a confiança de um cliente
3. ❌ KODA pagou reembolso total (R$ 79,90)
4. ❌ Ana deixou uma avaliação de 2 estrelas: "Péssimo atendimento de IA, não sabem o que fazem!"
5. ❌ Esse comentário foi visto por 50+ pessoas que visitaram o perfil KODA no WhatsApp Business

**Custo total:** R$ 79,90 (reembolso) + reputação danificada + cliente perdida + tempo de resolução

**Causa raiz:** Não um rubric bom, mas **a ausência de um.**

---

### A Lição

> **"Um Evaluator sem rubric é como um juiz sem lei. Ele tenta fazer o certo, mas não sabe como."**

Um Evaluator pode ser inteligente, ter acesso a todas as informações certas, e ainda assim **falhar completamente** porque **não tem critérios claros** para saber:

- O que procurar?
- Quando rejeitar?
- Quando aprovar?
- Como balancear critérios conflitantes (ex: preço baixo vs. segurança)?

**A diferença entre um Evaluator que funciona 40% das vezes e um que funciona 95% das vezes é exatamente isto: a clareza e a especificidade do seu rubric.**

---

### Próxima Seção

Você aprenderá:

1. **O que é um rubric** (definição clara)
2. **Por que rubrics funcionam** (psicologia + pragmatismo)
3. **Como desenhar um** (passo a passo)
4. **Como testar se é bom** (métricas)

Depois, voltaremos a este exemplo de Ana e veremos como um rubric melhor teria salvado a situação — e como **você pode evitar esse tipo de erro** em seus próprios sistemas.

---

**Seção 2 Completa** ✓  
Pronto para Seção 3 (Fundamentos de Rubrics)? Diga "aprova" ou "ajusta". 👇
---

## 🎓 Seção 3: Fundamentos de Rubrics

### O Que Exatamente É Um Rubric?

**Definição Simples:**

Um **rubric** é um conjunto de **critérios mensuráveis** que transforma uma avaliação subjetiva ("isso é bom?") em uma avaliação objetiva ("isso satisfaz critério X, Y, Z?").

**Definição Técnica (para Evaluators):**

Um rubric é um **documento estruturado** que um Evaluator usa para:
1. **Saber o que procurar** — quais aspectos importam?
2. **Medir cada aspecto** — em qual escala (1-10? Sim/Não? Muito/Pouco)?
3. **Tomar decisão consistente** — aprovado ou rejeitado, e por quê?
4. **Comunicar o feedback** — explicar à outra pessoa *exatamente* por que falhou

---

### Exemplos de Rubrics em Outros Contextos

Você provavelmente já encontrou rubrics antes, mesmo sem saber o nome:

#### 🎬 Crítica de Filmes
```
Filme: "Barbie"

Cinematografia (1-10):
  10 = Cores vibrantes, composição perfeita
  7 = Cores boas, mas composição comum
  4 = Composição confusa, cores monótonas
  Pontuação: 8

Roteiro (1-10):
  10 = Diálogos brilhantes, surpresas, profundidade
  7 = Bom, mas previsível em alguns momentos
  4 = Fraco, personagens planos
  Pontuação: 7

Atuação (1-10):
  10 = Convincente, emocionante, memorável
  7 = Boa, mas sem surpresas
  4 = Fraca, forçada
  Pontuação: 9

Nota Final: (8+7+9)/3 = 8/10
```

#### 🍕 Avaliação de Restaurante
```
Sabor do prato (1-5):
  5 = Excelente, memorável, bem temperado
  3 = Bom, nada de especial
  1 = Ruim, queimado ou cru
  Pontuação: 4

Atendimento (1-5):
  5 = Rápido, atencioso, educado
  3 = Normal, nem bom nem ruim
  1 = Lento, rude, desatencioso
  Pontuação: 5

Limpeza (1-5):
  5 = Imaculado
  3 = Normal, algumas manchas
  1 = Sujo, insalubre
  Pontuação: 4

Avaliação: ⭐⭐⭐⭐ (4 de 5 estrelas)
```

#### 📄 Avaliação de Trabalho Acadêmico
```
Estrutura (0-25 pontos):
  25 = Introdução clara, corpo bem organizado, conclusão forte
  20 = Bom, mas falta uma seção
  10 = Desorganizado, difícil de seguir
  Pontuação: 22

Pesquisa (0-25 pontos):
  25 = 10+ fontes confiáveis, bem citadas
  20 = 7-9 fontes, citação ok
  10 = Pouquíssimas fontes, sem citar
  Pontuação: 20

Argumentação (0-25 pontos):
  25 = Tese clara, argumentos lógicos, sem contradições
  20 = Tese clara, mas alguns saltos lógicos
  10 = Tese fraca, argumentação fraca
  Pontuação: 18

Gramatica (0-25 pontos):
  25 = Perfeito
  20 = 1-2 erros
  10 = Múltiplos erros que prejudicam clareza
  Pontuação: 23

Nota Final: (22+20+18+23)/100 = 83/100 = B
```

**Padrão comum em todos:** Critérios específicos + escalas claras + exemplos de cada nível.

---

### Por Que Rubrics Funcionam Melhor Que Intuição?

Voltemos ao exemplo de Ana. O Evaluator tinha **intuição** mas faltava **clareza**.

#### ❌ Abordagem Intuitiva (O Que Deu Errado)
```
Evaluator pensa:
"Deixa eu ver... cliente, produto, preço... tudo aqui.
 Deve estar tudo bem. Vou aprovar."

Problema:
- Não checou: "Qual é a severidade da alergia?"
- Não checou: "Há risco de contaminação no produto?"
- Não checou: "O rótulo avisa sobre isso?"

Resultado: Falha silenciosa. Ana quase teve reação alérgica.
```

#### ✅ Abordagem com Rubric (O Que Deveria Ter Acontecido)
```
Evaluator lê o rubric:

"DIMENSÃO: SEGURANÇA DO PRODUTO
Se cliente tem alergia severa:
  □ Verificar se rótulo tem aviso alérgico
  □ Verificar nível de risco de contaminação
  □ Se risco >= MODERADO: REJEITAR
  □ Se há aviso no rótulo: REJEITAR
  
  Esta cliente tem alergia severa?
  → SIM (registrado como "severa")
  
  Verificar rótulo...
  → "Risco de contaminação: MODERADO"
  → "Aviso: Consulte médico antes de usar"
  
  Ação: ❌ REJEITAR
  Motivo: Risco alérgico muito alto para alergia severa."

Resultado: Pedido rejeitado. Ana recebe alternativas seguras.
```

**O que mudou?** Não a inteligência do Evaluator. Mudou a **clareza das instruções**.

---

### Três Razões Pelas Quais Rubrics Funcionam

#### 1️⃣ **Elimina Viés Pessoal**

Sem rubric:
- Evaluator "acha" que pedido está bom (viés: foi fácil processar, então deve estar certo)
- Evaluator "sente" que está tudo ok (viés: não quer rejeitar sem motivo claro)

Com rubric:
- Evaluator segue critérios objetivos
- Não importa como se sente, os dados ditam a decisão
- Decisão é **auditável** — você pode rastrear exatamente por quê foi rejeitado

#### 2️⃣ **Força Pensamento Estruturado**

Sem rubric:
- Evaluator pensa: "Hmm, algo sente errado aqui... mas não consigo identificar o quê."
- Indecisão. Hesitação. Aprovação por padrão.

Com rubric:
- Evaluator pensa: "Critério 1? ✓. Critério 2? ✓. Critério 3? ❌ Encontrado o problema."
- **Estrutura força clareza mental.**

#### 3️⃣ **Tornável Consistente**

Sem rubric:
- Segunda-feira: Evaluator aprova pedido parecido
- Quarta-feira: Rejeita pedido idêntico
- Por quê? Porque estava cansado, tinha um viés diferente, ou mudou de ideia

Com rubric:
- Segunda-feira: Critério X falhou → rejeita
- Quarta-feira: Mesmo critério X falha → rejeita
- **Consistência = confiabilidade.**

---

### O Conceito Crítico: Granularidade

Agora vamos ao conceito que separa **rubrics ruins** de **rubrics bons**: **granularidade**.

**Granularidade** = nível de detalhe dos seus critérios.

#### ❌ Granularidade Muito Baixa (Rubric Ruim)
```
Verificar se pedido está bom:
1. Está completo? Sim/Não
2. Está correto? Sim/Não
3. Devo aprovar? Sim/Não

Problema: "Completo" é vago. "Correto" é vago.
O que significa exatamente? Cliente não sabe.
Avaliador fica confuso.
```

**Exemplo real do problema:**
- Evaluator: "Pedido está completo? Tem cliente, produto, preço. Sim!"
- Evaluator: "Está correto? Tudo digitado. Sim!"
- Evaluator: "Aprovar? Claro, tudo ok!"
- **Mas:** Nunca verificou se product era seguro para alergia do cliente

#### ✅ Granularidade Ótima (Rubric Bom)
```
Verificar se pedido está bom em 3 DIMENSÕES:

DIMENSÃO 1: Dados Básicos
□ Cliente existe?
□ Produto existe?
□ Preço é válido (0 < preço < 500)?
Critério: Todos devem ser ✓

DIMENSÃO 2: Compatibilidade Cliente-Produto
□ Se cliente é vegano, produto é vegano?
□ Se cliente é alérgico, produto é seguro?
□ Se cliente tem restrição orçamentária, preço é respeitado?
Critério: Todos devem ser ✓ (ou N/A se não aplicável)

DIMENSÃO 3: Segurança & Qualidade
□ Produto tem avisos no rótulo relevantes ao cliente?
□ Se alergia severa, qual é o risco de contaminação?
□ Há reviews negativas sobre segurança?
Critério: Se alergia severa + risco >= MODERADO = ❌

Decisão Final:
Se passa em TODAS as 3 dimensões: ✅ APROVAR
Se falha em QUALQUER dimensão: ❌ REJEITAR + feedback específico
```

**Por que granularidade ótima funciona:**
- Não é vago ("está bom?") — é específico ("segurança do produto é X")
- Você sabe exatamente onde procurar
- Teste é **auditável** — pode provar que verificou cada ponto

---

### Granularidade: Encontrando o Equilíbrio

Não existe uma granularidade única "certa". Depende do contexto.

#### Cenário 1: Sistema Crítico (Saúde, Segurança)
```
Uso: Avaliar se é seguro dispensar medicamento
Granularidade: MUITO ALTA (20+ critérios específicos)

Exemplo:
□ Medicamento existe?
□ Dosagem está correta para peso do paciente?
□ Há interações com medicamentos atuais?
□ Paciente tem alergias ao medicamento?
□ Há contraindicações?
□ Expiração está válida?

Razão: Erro = vida em risco. Precisa de precisão máxima.
```

#### Cenário 2: Sistema Moderado (E-commerce)
```
Uso: Avaliar se recomendação de produto é boa
Granularidade: MÉDIA (6-10 critérios)

Exemplo:
□ Produto existe?
□ Preço está correto?
□ Cliente tem alergia/restrição?
□ Se sim, produto é seguro?
□ Há reviews negativas relevantes?

Razão: Erro = cliente insatisfeito. Precisa de qualidade boa.
```

#### Cenário 3: Sistema Informacional (Blog Post)
```
Uso: Avaliar se blog post está bom para publicar
Granularidade: BAIXA (3-5 critérios)

Exemplo:
□ Tem título?
□ Tem pelo menos 500 palavras?
□ Não tem erros gramaticais graves?

Razão: Erro = leitor deixa o site. Precisa de qualidade mínima.
```

**Regra Prática:**
> **Granularidade deve ser proporcional ao custo de um erro.**

Se erro é caro (saúde, segurança, confiança), granularidade deve ser alta.
Se erro é barato (conveniência, informação), granularidade pode ser baixa.

---

### Rubric vs. Checklist vs. Especificação

Pessoas frequentemente confundem esses três. Vamos esclarecer:

#### 📋 Checklist (Sim/Não)
```
Antes de enviar email:
□ Tem remetente?
□ Tem destinatário?
□ Tem assunto?
□ Tem corpo?

Tipo: Binário (sim/não)
Uso: Verificação rápida
Problema: Não mede qualidade
```

#### 📏 Rubric (Escala de Qualidade)
```
Avaliar email:
□ Clareza (1-5): 1=confuso, 5=cristalino
□ Profissionalismo (1-5): 1=casual, 5=formal
□ Chamada à ação (sim/não): cliente sabe o que fazer?

Tipo: Escala + binário
Uso: Medir qualidade
Resultado: Score ou aprovado/rejeitado com motivo
```

#### 📖 Especificação (Detalhes Técnicos)
```
Email deve ter:
- Remetente: nome@empresa.com
- Assunto: máximo 60 caracteres
- Corpo: markdown formatado
- Rodapé: incluir links de contato
- Imagem: até 500KB

Tipo: Detalhado e específico
Uso: Dizer exatamente o que construir
Problema: Não mede qualidade, apenas diz o que incluir
```

**Relação entre os três:**

```
Especificação define O QUÊ construir
        ↓
Checklist verifica se foi construído
        ↓
Rubric mede QUÃO BEM foi construído
```

**Para nosso Evaluator:**
- Checklist = verificação rápida ("tem preço?")
- Rubric = avaliação de qualidade ("preço é justo para valor?")
- Especificação = documentação do produto ("preço deve ser R$ X")

---

### Conexão com Generator/Evaluator

Agora você começa a ver como os três arquivos se conectam:

```
ARQUIVO 1: Generator/Evaluator Pattern
│
│ "Separar criador de avaliador para evitar viés"
│
└──→ OK, mas como o avaliador sabe se algo é bom?
    
    ARQUIVO 2: Sprint Contracts
    │
    │ "Negociar um contrato: 'Pronto' significa X, Y, Z"
    │
    └──→ OK, mas como defino X, Y, Z de forma justa?
        
        ARQUIVO 3: Rubric Design (✓ você está aqui)
        │
        │ "Use rubrics para transformar 'X, Y, Z' em critérios mensuráveis"
        │
        └──→ Agora você tem ferramenta para fazer isso!
```

**No Próximo Arquivo (Trace Reading):**
Você aprenderá como **debugar** quando o rubric falha — "Por que o Evaluator rejeitou algo que deveria aprovar?"

---

### Resumo: O Que É Um Rubric?

Um rubric é:

✅ Um **documento estruturado** que especifica critérios de qualidade  
✅ Uma **ferramenta de objetividade** que elimina viés pessoal  
✅ Uma **escala de medida** que torna decisões consistentes  
✅ Uma **forma de comunicação** — você pode explicar *por quê* decidiu algo  
✅ Diferente de checklist (que é binário) e especificação (que é descritiva)  

Um rubric NÃO é:

❌ Uma ciência exata — ainda envolve julgamento  
❌ Imutável — deve evoluir conforme você aprende  
❌ Um substituto para contexto — contexto sempre importa  
❌ Uma forma de eliminar erro 100% — reduz erro, não elimina  

---

### Próxima Seção

Na próxima seção, você aprenderá a **anatomia de um bom rubric** — as partes específicas que fazem um rubric funcionar:

- **Critérios:** O que você está avaliando?
- **Dimensões:** Quantas perspectivas você precisa considerar?
- **Escalas:** Como você mede cada critério?
- **Exemplos:** O que significa "bom" em cada escala?
- **Pesos:** Todos os critérios têm igual importância?

Veja você na próxima seção! 👇

---

**Seção 3 Completa** ✓  
Pronto para Seção 4 (Elementos de um Bom Rubric)? Diga "aprova" ou "ajusta". 👇
---

## 🏗️ Seção 4: Elementos de Um Bom Rubric

Agora que você entende *por que* rubrics funcionam, vamos aprender **do que um rubric é feito** — os componentes que fazem um rubric ser **bom** em vez de **medíocre**.

Imagine que você está construindo uma casa. Não basta saber "casas funcionam". Você precisa entender: fundação, paredes, teto, etc. O mesmo com rubrics.

---

### Elemento 1: O Critério (O Quê Estamos Avaliando?)

Um **critério** é uma dimensão específica de qualidade que você quer medir.

#### ❌ Critérios Ruins (Vagos)
```
"O pedido está bom?"
"A recomendação é boa?"
"O produto é de qualidade?"

Problema: Impossível medir. "Bom" significa coisa diferente para cada pessoa.
```

#### ✅ Critérios Bons (Específicos)
```
"O produto recomendado existe em inventory?"
"O preço do produto está atualizado há menos de 7 dias?"
"O produto é compatível com as alergias do cliente?"
"O rótulo do produto avisa sobre riscos alérgicos relevantes?"

Razão: Cada um é verificável. Você sabe o que procurar.
```

#### Padrão para Nomear Critérios

Um bom nome de critério:
- Começa com um **verbo ativo** ("verificar", "confirmar", "validar")
- É **específico** (não genérico)
- É **auditável** (você pode rastrear se foi checado)
- Responde a uma pergunta **clara**

```
Ruim:   "Qualidade"
Bom:    "Verificar se preço está atualizado"

Ruim:   "Segurança"
Bom:    "Confirmar se há risco de contaminação alérgica"

Ruim:   "Relevância"
Bom:    "Validar se produto resolve problema específico do cliente"
```

---

### Elemento 2: A Dimensão (Quantas Perspectivas?)

Uma **dimensão** é uma categoria maior de critérios relacionados. Agrupa critérios que medem a mesma coisa de ângulos diferentes.

#### Exemplo: Rubric para Avaliar Pedido no KODA

```
DIMENSÃO 1: DADOS BÁSICOS
├─ Critério: Verificar se cliente existe no sistema
├─ Critério: Verificar se produto existe em inventory
└─ Critério: Verificar se preço é válido (0 < preço < 500)

DIMENSÃO 2: COMPATIBILIDADE CLIENTE-PRODUTO
├─ Critério: Se cliente é vegano, produto é vegano?
├─ Critério: Se cliente tem alergia, produto é seguro?
├─ Critério: Se cliente tem restrição orçamentária, preço é respeitado?
└─ Critério: Se cliente tem preferência de marca, marcar foi considerada?

DIMENSÃO 3: SEGURANÇA & QUALIDADE
├─ Critério: Verificar se rótulo tem avisos de alergias
├─ Critério: Avaliar risco de contaminação cruzada
├─ Critério: Verificar se produto está em promoção/desconto
└─ Critério: Validar se há reviews negativas sobre segurança
```

**Por que usar dimensões?**

1. **Organização** — não é uma lista caótica de 50 critérios
2. **Rastreabilidade** — "qual dimensão falhou?" ajuda a debugar
3. **Priorização** — você pode dizer "dimensão X é crítica, Y é secundária"
4. **Reuso** — você pode usar dimensão 1 em múltiplos rubrics

**Quantas dimensões usar?**

```
Muito poucas (1-2):   Rubric fica vago, perde nuances
Ideal (3-5):          Balanceado, cobrindo principais perspectivas
Muitas (10+):         Rubric fica complexo, difícil de usar
```

**Regra:** Comece com 3-5 dimensões. Adicione mais só se necessário.

---

### Elemento 3: A Escala (Como Medimos Cada Critério?)

Uma **escala** é a forma como você expressa o resultado de um critério.

#### Tipo 1: Escala Binária (Sim/Não)
```
Critério: "Produto existe em inventory?"
Escala: Sim / Não
Resultado: ✓ Sim (aprova) ou ✗ Não (rejeita)

Quando usar:
- Critérios que são verdadeiro/falso
- Requisitos obrigatórios
- Verificações de segurança

Exemplo no KODA:
□ Cliente tem alergia?
□ Produto tem aviso de alergias no rótulo?
□ Há risco de contaminação cruzada?
```

#### Tipo 2: Escala Numérica (1-5, 1-10)
```
Critério: "Qual é a clareza da explicação do produto?"
Escala: 1-5
  1 = Muito confuso, cliente não entende
  2 = Confuso, cliente tem dúvidas
  3 = Aceitável, cliente entende razoavelmente bem
  4 = Claro, cliente entende bem
  5 = Cristalino, cliente entende perfeitamente

Resultado: 3 (aceitável)

Quando usar:
- Qualidade é gradual (não é tudo ou nada)
- Precisa de nuances ("melhor" vs "pior")
- Agregação (pode somar e fazer média)

Exemplo no KODA:
1-5: Clareza da resposta
1-5: Relevância da recomendação
1-5: Atendimento às preferências do cliente
```

#### Tipo 3: Escala Categórica (Baixo/Médio/Alto)
```
Critério: "Qual é o risco de contaminação alérgica?"
Escala: Muito Baixo / Baixo / Moderado / Alto / Muito Alto
Resultado: Moderado

Quando usar:
- Risco ou impacto (baixo/médio/alto)
- Prioridade (baixa/média/alta)
- Frequência (raro/ocasional/frequente)

Exemplo no KODA:
Muito Baixo: Produto fabricado em linha separada, sem contato com alérgeno
Baixo:       Produto diferente, mas mesma fábrica
Moderado:    Produto diferente, mesmo equipamento compartilhado
Alto:        Produto pode ter traços do alérgeno
Muito Alto:  Produto contém o alérgeno
```

#### Tipo 4: Escala Comparativa (Melhor/Igual/Pior)
```
Critério: "Esta recomendação é melhor que a anterior?"
Escala: Pior / Igual / Melhor
Resultado: Melhor

Quando usar:
- Comparação entre versões
- Melhoria incremental
- A/B testing

Exemplo no KODA:
Pior:    Nova recomendação ignora restrições que a anterior respeitava
Igual:   Nova recomendação é tão boa quanto a anterior
Melhor:  Nova recomendação melhora em pelo menos um aspecto importante
```

**Como escolher a escala certa?**

```
Use Sim/Não se:
  - É requisito obrigatório
  - Falhar = rejeitar tudo
  - Ex: "Cliente é alérgico?"

Use 1-5 se:
  - Qualidade é gradual
  - Pode agregar múltiplos critérios
  - Ex: "Qual é a clareza?" (1-5)

Use Categorias se:
  - Risco/impacto é não-linear
  - Cada categoria tem ação diferente
  - Ex: "Risco de contaminação?" (Muito Baixo/Baixo/Moderado/Alto)

Use Comparativa se:
  - Precisa comparar com alternativa
  - Melhoria incremental importa
  - Ex: "Melhor que antes?"
```

---

### Elemento 5: Os Exemplos (O Que Significa Cada Nível?)

Este é o elemento que **separa rubrics que funcionam de rubrics que não funcionam**.

Um rubric **sem exemplos** é como uma bússola sem norte. Você tem uma escala (1-5) mas não sabe o que é um "3" vs "4".

#### ❌ Rubric Ruim (Sem Exemplos)
```
Critério: Clareza da resposta
Escala: 1-5 (1=ruim, 5=ótimo)
Definição: Quão claro é o texto?

Problema: Dois avaliadores podem interpretar "3" diferente:
- Avaliador A: "3 é ok para mim" (3 = 60% claro)
- Avaliador B: "3 é ruim para mim" (3 = 40% claro)

Resultado: Inconsistência. Mesmo texto recebe 3 ou 5 dependendo de quem avalia.
```

#### ✅ Rubric Bom (Com Exemplos)
```
Critério: Clareza da resposta
Escala: 1-5

1 = MUITO CONFUSO
  Exemplo: "Recomendo produto X. É bom. Preço é Y."
  Problema: Cliente não sabe por que é bom ou se é seguro

2 = CONFUSO
  Exemplo: "Recomendo whey protein porque tem proteína."
  Problema: Não explica benefício específico para cliente

3 = ACEITÁVEL
  Exemplo: "Recomendo Whey Isolado. Tem 25g de proteína, sem lactose como você pediu."
  Razão: Cliente entende, mas faltam detalhes (preço, sabor, etc)

4 = CLARO
  Exemplo: "Recomendo Whey Isolado (R$ 79,90). Tem 25g proteína por dose, zero lactose (você tem alergia), e está em promoção até amanhã."
  Razão: Cliente entende tudo. Mas poderia mencionar sabor/review

5 = CRISTALINO
  Exemplo: "Recomendo Whey Isolado (R$ 79,90/mês). Por quê: 25g proteína por dose, zero lactose (safe para sua alergia), sabor morango (você escolheu antes), 4.8★ reviews. Alternativa: Whey Vegano (R$ 85) se prefere plant-based."
  Razão: Cliente tem todas informações para tomar decisão. Sem ambiguidade.
```

**Por que exemplos importam:**

1. **Remove ambiguidade** — "3" agora significa algo específico
2. **Treina o avaliador** — ele vê o padrão
3. **Torna consistente** — dois avaliadores darão mesma nota
4. **Facilita replicação** — você pode usar em outro sistema

**Regra de Ouro para Exemplos:**

> Para cada nível da escala, forneça:
> - Um **exemplo de texto/output** real
> - Uma **explicação** do por quê recebe aquela nota
> - Se aplicável, o **problema específico** com esse nível

---

### Elemento 6: Os Pesos (Nem Todos Critérios São Iguais)

Nem todos os critérios têm igual importância. Alguns são **críticos**, outros são **nice-to-have**.

#### Exemplo: Rubric para Recomendação de Produto no KODA

```
DIMENSÃO 1: DADOS BÁSICOS
├─ Critério: Produto existe? [PESO: Crítico / 100 pontos]
│  └─ Se falhar: REJEITAR TUDO
├─ Critério: Preço é válido? [PESO: Crítico / 100 pontos]
│  └─ Se falhar: REJEITAR TUDO
└─ Critério: Cliente existe? [PESO: Crítico / 100 pontos]
   └─ Se falhar: REJEITAR TUDO

DIMENSÃO 2: COMPATIBILIDADE
├─ Critério: Produto é seguro para alergia? [PESO: Crítico / 100 pontos]
│  └─ Se falhar: REJEITAR TUDO (risco de vida)
├─ Critério: Preço respeita orçamento? [PESO: Alto / 50 pontos]
│  └─ Se falhar: Reduz confiabilidade, mas pode aprovar
└─ Critério: Alinha com preferência de marca? [PESO: Médio / 25 pontos]
   └─ Se falhar: Aprova mesmo assim

DIMENSÃO 3: QUALIDADE & CONTEXTO
├─ Critério: Clareza da explicação? [PESO: Médio / 25 pontos]
├─ Critério: Reviews do produto são positivas? [PESO: Baixo / 10 pontos]
└─ Critério: Há promoção/desconto? [PESO: Baixo / 10 pontos]

SCORING FINAL:
- Suma pontos de critérios aprovados
- Se algum critério Crítico falhar: ❌ REJEITAR
- Se soma < 150: ❌ REJEITAR
- Se 150-200: ⚠️ APROVADO COM RESSALVAS
- Se 200+: ✅ APROVADO COM CONFIANÇA
```

**Como Definir Pesos?**

Pergunte-se para cada critério:

```
1. Se falhar, qual é a consequência?
   Grave (risco de vida, perda financeira) = Crítico
   Moderada (insatisfação, perda de confiança) = Alto
   Leve (experiência subótima) = Médio/Baixo

2. Com que frequência falha?
   Frequente = precisa de atenção, peso alto
   Raro = pode ter peso baixo

3. Quanto é fácil de corrigir?
   Difícil de corrigir = peso alto
   Fácil de corrigir = peso baixo

4. Quanto importa para a estratégia?
   Alinha com objetivo crítico = peso alto
   Nice-to-have = peso baixo
```

**Exemplo Prático: No KODA**

```
Critério: Produto existe?
  Consequence: Se não, venda é impossível = CRÍTICO
  Frequência: Raro (sistema de inventory é bom)
  Correção: Impossível corrigir depois
  Estratégia: Essencial
  → PESO: CRÍTICO

Critério: Há promoção?
  Consequence: Se não, cliente paga preço normal = Nice-to-have
  Frequência: Frequente (nem todo produto tem promo)
  Correção: Fácil, pode recomendar alternativa
  Estratégia: Aumenta conversão, mas não é essencial
  → PESO: BAIXO
```

---

### Elemento 7: A Lógica de Decisão (Como Combinamos Tudo?)

Depois de avaliar todos os critérios, como você **toma a decisão final**?

#### Padrão 1: Tudo ou Nada (AND Logic)
```
Regra: Se QUALQUER critério crítico falhar → REJEITAR
       Senão → APROVAR

Código:
if (alergia_severa AND risco_contaminacao_alto):
    decisao = REJEITAR
elif (qualquer_critico_falha):
    decisao = REJEITAR
else:
    decisao = APROVAR

Quando usar:
- Sistemas de segurança
- Requisitos obrigatórios
- Risco alto
```

#### Padrão 2: Soma Ponderada (Scoring)
```
Regra: Some pontos de todos os critérios
       Se soma >= threshold → APROVAR
       Senão → REJEITAR

Fórmula:
score = (criterio1_pontos * peso1) + (criterio2_pontos * peso2) + ...
if score >= 150:
    decisao = APROVAR
else:
    decisao = REJEITAR

Quando usar:
- Avaliação de qualidade
- Múltiplos critérios com diferentes importâncias
- Gradações de qualidade
```

#### Padrão 3: Prioridade em Cascata (IF-THEN)
```
Regra: Cheque critérios em ordem de importância
       Se o mais importante falhar, não precisa checar outros

Pseudocódigo:
if (dados_basicos_invalidos):
    decisao = REJEITAR
elif (alergia_incompativel):
    decisao = REJEITAR
elif (preço_fora_orçamento):
    decisao = REJEITAR + sugerir alternativa
elif (qualidade_baixa):
    decisao = APROVAR COM RESSALVAS
else:
    decisao = APROVAR

Quando usar:
- Muitos critérios
- Critérios têm dependências
- Quer economizar processamento
```

---

### Resumo: Os 7 Elementos

Agora você sabe que um **bom rubric** tem:

| Elemento | O Quê | Por Quê | Exemplo |
|----------|-------|--------|---------|
| **Critério** | O que medir | Define escopo | "Verificar se produto é seguro para alergia" |
| **Dimensão** | Categorias | Organização, rastreabilidade | Dimensão 1: Dados Básicos, Dimensão 2: Segurança |
| **Escala** | Como medir | Define método | Sim/Não, 1-5, Baixo/Médio/Alto |
| **Exemplos** | Padrões | Remove ambiguidade | "3 = confuso, cliente tem dúvidas" |
| **Pesos** | Importância relativa | Diferencia crítico de nice-to-have | Segurança = Crítico, Promoção = Baixo |
| **Lógica** | Como decidir | Torna decisão sistemática | "Se falha crítico = rejeitar; senão scoring" |
| **Feedback** | Comunicar decisão | Transparência | "Rejeitado: risco de contaminação alto" |

---

### Próxima Seção

Agora que você conhece os **elementos** de um bom rubric, você aprenderá **como montar tudo junto** — o passo a passo para desenhar um rubric do zero.

Na próxima seção:
1. Você lista tudo que pode dar errado
2. Transforma em critérios mensuráveis
3. Define escalas e exemplos
4. Testa se o rubric funciona

---

**Seção 4 Completa** ✓  
Pronto para Seção 5 (Como Desenhar Rubrics - Passo a Passo)? Diga "aprova" ou "ajusta". 👇
---

## 🛠️ Seção 5: Como Desenhar Rubrics - Passo a Passo

Agora que você conhece os **elementos** de um bom rubric, vamos usar essa conhecimento para **desenhar um do zero**.

Você seguirá um processo de 4 passos:
1. **Listar** — O que pode dar errado?
2. **Formalizar** — Transformar problemas em critérios mensuráveis
3. **Definir** — Escalas, exemplos, pesos
4. **Testar** — O rubric funciona?

Vamos usar a **história de Ana** como nosso caso prático.

---

## Passo 1: Listar — O Que Pode Dar Errado?

**Objetivo:** Brainstorm sem filtro. Anote tudo que pode quebrar.

**Contexto:** Você é responsável por desenhar um rubric para o Evaluator verificar recomendações de produtos no KODA.

### 1a. Pergunte-se:
```
"Se um cliente reclamar dizendo 'KODA me recomendou o produto ERRADO', 
 qual seria o problema?"
```

Brainstorm:
```
❌ Produto não existe em inventory
❌ Preço está desatualizado
❌ Produto está fora de estoque
❌ Cliente tem alergia, produto tem alérgeno
❌ Cliente tem restrição orçamentária, produto é caro demais
❌ Cliente é vegano, produto tem proteína animal
❌ Produto tem review negativa sobre qualidade
❌ Há alternativa melhor que a recomendada
❌ Explicação do produto é confusa
❌ Rótulo tem aviso que não foi mencionado
❌ Risco de contaminação cruzada não foi considerado
❌ Marca é diferente da preferência do cliente
❌ Sabor não é o que cliente pediu
```

### 1b. Agrupe por Contexto:
```
GRUPO 1: INTEGRIDADE DE DADOS
├─ Produto não existe em inventory
├─ Preço está desatualizado
└─ Produto está fora de estoque

GRUPO 2: COMPATIBILIDADE COM CLIENTE
├─ Cliente tem alergia, produto tem alérgeno
├─ Cliente tem restrição orçamentária, produto é caro demais
├─ Cliente é vegano, produto tem proteína animal
└─ Marca é diferente da preferência do cliente

GRUPO 3: QUALIDADE DO PRODUTO
├─ Produto tem review negativa sobre qualidade
├─ Há alternativa melhor que a recomendada
└─ Rótulo tem aviso de segurança

GRUPO 4: SEGURANÇA ALÉRGICA (Critical)
├─ Risco de contaminação cruzada
├─ Aviso de alergias no rótulo
└─ Severidade da alergia do cliente é "severa"

GRUPO 5: COMUNICAÇÃO
├─ Explicação do produto é confusa
├─ Sabor não é o que cliente pediu
└─ Benefício do produto não é claro
```

**Dica:** Grupos naturalmente se tornam suas **dimensões**.

---

## Passo 2: Formalizar — Transformar em Critérios Mensuráveis

Agora pegue cada item da lista e transforme em **critério testável**.

### 2a. Pegue um problema:
```
Problema: "Cliente tem alergia, produto tem alérgeno"
```

### 2b. Transforme em Critério:
```
❌ Ruim:    "Verificar se produto é seguro"
✅ Bom:     "Verificar se produto contém o alérgeno específico registrado do cliente"

Por quê "bom"?
- Específico (qual alérgeno?)
- Testável (você pode checar no rótulo)
- Acionável (se falhar, sabe exatamente o problema)
```

### 2c. Repita para Todos:

```
PROBLEMA → CRITÉRIO TESTÁVEL

❌ "Produto não existe"
✅ "Verificar se SKU do produto existe na base de dados de inventory"

❌ "Preço está errado"
✅ "Verificar se preço foi atualizado há menos de 7 dias"

❌ "Recomendação é ruim"
✅ "Verificar se recomendação resolve o problema específico que cliente mencionou"

❌ "Há aviso no rótulo"
✅ "Verificar se rótulo contém avisos de alergias relevantes ao cliente"

❌ "Contaminação cruzada"
✅ "Avaliar nível de risco de contaminação cruzada conforme rótulo"

❌ "Explicação confusa"
✅ "Avaliar se explicação do produto menciona: ingrediente principal, benefício específico, compatibilidade com restrição do cliente"
```

**Padrão para Transformar:**
```
Problema genérico → Critério específico

1. Adicione "Verificar" ou "Avaliar" no início
2. Remova palavras vagas ("bom", "melhor", "adequado")
3. Substitua por observáveis ("contém", "menciona", "respeita", "atualizado")
4. Pergunte: "Como eu testaria isso?"
```

---

## Passo 3: Definir — Escalas, Exemplos, Pesos

Agora você tem critérios testáveis. Defina como você vai avaliá-los.

### 3a. Organize em Dimensões:

```
Seus critérios agora se organizam naturalmente:

DIMENSÃO 1: INTEGRIDADE DE DADOS (Crítico)
├─ ✓ Critério: Produto existe em inventory?
├─ ✓ Critério: Preço foi atualizado < 7 dias?
└─ ✓ Critério: Produto está em estoque?

DIMENSÃO 2: COMPATIBILIDADE CLIENTE (Crítico se falha)
├─ ✓ Critério: Se cliente alérgico, produto é seguro?
├─ ✓ Critério: Se cliente vegano, produto é vegano?
├─ ✓ Critério: Se orçamento restrito, preço respeita limite?
└─ ✓ Critério: Se marca preferida, foi considerada?

DIMENSÃO 3: SEGURANÇA ALÉRGICA (Crítico!!)
├─ ✓ Critério: Alergia do cliente é "severa"?
├─ ✓ Critério: Risco de contaminação cruzada?
└─ ✓ Critério: Há avisos de alergia no rótulo?

DIMENSÃO 4: QUALIDADE DO PRODUTO (Alto)
├─ ✓ Critério: Há reviews negativas sobre segurança?
├─ ✓ Critério: Há alternativa melhor disponível?
└─ ✓ Critério: Produto está em promoção?

DIMENSÃO 5: COMUNICAÇÃO (Médio)
├─ ✓ Critério: Explicação menciona benefício específico?
├─ ✓ Critério: Explicação menciona compatibilidade com restrição?
└─ ✓ Critério: Sabor mencionado é o que cliente pediu?
```

### 3b. Defina Escalas para Cada Critério:

```
DIMENSÃO 1: INTEGRIDADE DE DADOS
├─ Critério: "Produto existe em inventory?"
│  Escala: Sim / Não
│  Peso: Crítico (se falha → rejeita tudo)

├─ Critério: "Preço foi atualizado < 7 dias?"
│  Escala: Sim / Não
│  Peso: Crítico (se falha → rejeita tudo)

└─ Critério: "Produto está em estoque?"
   Escala: Sim / Não
   Peso: Crítico (se falha → rejeita tudo)

DIMENSÃO 3: SEGURANÇA ALÉRGICA
├─ Critério: "Alergia do cliente é severa?"
│  Escala: Não / Leve / Moderada / Severa
│  Peso: Crítico (determina resto da avaliação)

├─ Critério: "Qual é o risco de contaminação?"
│  Escala: Muito Baixo / Baixo / Moderado / Alto / Muito Alto
│  Peso: Crítico (se Moderado+ e alergia severa → rejeita)

└─ Critério: "Há avisos de alergias no rótulo?"
   Escala: Sim / Não
   Peso: Crítico (se sim e alergia severa → rejeita)

DIMENSÃO 4: QUALIDADE DO PRODUTO
├─ Critério: "Há reviews negativas sobre segurança?"
│  Escala: Não / Poucas / Algumas / Muitas
│  Peso: Alto (se muitas → reduz confiança)

└─ Critério: "Está em promoção?"
   Escala: Não / Sim
   Peso: Baixo (bônus, não requisito)
```

### 3c. Forneça Exemplos para Cada Escala:

**Exemplo Completo: Critério "Alergia do Cliente é Severa?"**

```
Critério: Validar severidade da alergia do cliente

Escala: Não / Leve / Moderada / Severa

NÃO (sem alergia)
  Exemplo do Perfil: 
    "Cliente: João Silva, Alérgico a: [nenhuma registrada]"
  Impacto: Nenhuma restrição especial. Qualquer recomendação é ok.

LEVE (pequena reação)
  Exemplo do Perfil:
    "Cliente: Maria dos Santos, Alérgico a: Lactose (causa inchaço abdominal leve)"
  Impacto: Precisa verificar rótulo, mas pode recomendar produtos "sem lactose"
  
MODERADA (reação significativa)
  Exemplo do Perfil:
    "Cliente: Paulo Santos, Alérgico a: Amendoim (causa coceira e inchaço de garganta)"
  Impacto: Recomendação precisa de MUITA atenção. Verificar rótulo + contaminação

SEVERA (risco de vida)
  Exemplo do Perfil:
    "Cliente: Ana Silva, Alérgico a: Lactose (causa anafilaxia, levou à emergência 2x)"
  Impacto: Critério BLOQUEADOR. Se há risco, rejeita. Sem exceção.
```

**Exemplo Completo: Critério "Qual é o Risco de Contaminação?"**

```
Critério: Avaliar risco de contaminação cruzada no rótulo

Escala: Muito Baixo / Baixo / Moderado / Alto / Muito Alto

MUITO BAIXO
  Rótulo diz: "Produzido em linha dedicada sem contato com [alérgeno]"
  Exemplo: "100% SEM GLÚTEN, produzido em fábrica separada"
  Ação: ✅ Seguro

BAIXO
  Rótulo diz: "Produzido em fábrica que processa [alérgeno], mas linha separada"
  Exemplo: "Contém SOJA. Produzido em fábrica que processa amendoim, mas linha diferente."
  Ação: ✅ Seguro para maioria, questionar se alergia severa

MODERADO
  Rótulo diz: "Produzido em fábrica que processa [alérgeno], mesmo equipamento com limpeza entre"
  Exemplo: "Contém SOJA. Produzido em equipamento compartilhado. Risco de traços de lactose."
  Ação: ⚠️ Questionar severidade. Se severa, rejeitar.

ALTO
  Rótulo diz: "Processado em fábrica com [alérgeno], mesmo equipamento sem separação"
  Exemplo: "Pode conter TRAÇOS de GLÚTEN (mesmo equipamento, sem limpeza dedicada)"
  Ação: ❌ Rejeitar se cliente é alérgico

MUITO ALTO
  Rótulo diz: "Contém [alérgeno]" diretamente
  Exemplo: "INGREDIENTES: Soro de leite, lactose, [...]"
  Ação: ❌ Rejeitar se cliente é alérgico
```

### 3d. Defina Pesos:

```
Critério                                    Peso      Se Falhar
────────────────────────────────────────────────────────────────
Produto existe?                           Crítico   → Rejeita tudo
Preço é válido?                           Crítico   → Rejeita tudo
Produto em estoque?                       Crítico   → Rejeita tudo
────────────────────────────────────────────────────────────────
Alergia severa + contaminação alto?       Crítico   → Rejeita tudo
Há aviso de alergia no rótulo?            Crítico   → Rejeita tudo (se severa)
────────────────────────────────────────────────────────────────
Preço respeita orçamento?                 Alto      → Reduz confiança
Reviews negativas sobre segurança?        Alto      → Rejeita
────────────────────────────────────────────────────────────────
Explicação menciona benefício?            Médio     → Aprova, feedback
Sabor é o que cliente pediu?              Médio     → Aprova, feedback
────────────────────────────────────────────────────────────────
Está em promoção?                         Baixo     → Bônus
Marca é a preferida?                      Baixo     → Bônus
```

---

## Passo 4: Testar — O Rubric Funciona?

Um rubric é **apenas bom** se você testar com dados reais.

### 4a. Pegue 5-10 Exemplos Reais:

```
Exemplo 1: Recomendação de Ana (quase desastre)
├─ Cliente: Ana Silva (alergia severa a lactose)
├─ Produto recomendado: Whey Isolado SEM Lactose
├─ Rótulo: "Risco de contaminação: MODERADO"
└─ Pergunta: Rubric rejeita isto?

Exemplo 2: Recomendação Para João
├─ Cliente: João Silva (sem alergias)
├─ Produto recomendado: Whey Concentrado (R$ 45)
├─ Rótulo: Nenhum aviso relevante
└─ Pergunta: Rubric aprova isto?

Exemplo 3: Recomendação Vegana
├─ Cliente: Maria (alergia leve a lactose, vegana)
├─ Produto recomendado: Whey Vegano (R$ 85)
├─ Rótulo: "100% Plant-based"
└─ Pergunta: Rubric aprova isto?

... (mais 7 exemplos)
```

### 4b. Execute o Rubric em Cada Exemplo:

```
TESTANDO EXEMPLO 1 (Ana):

Dimensão 1: Integridade de Dados
├─ Produto existe? ✓ Sim
├─ Preço atualizado? ✓ Sim
└─ Em estoque? ✓ Sim
Resultado: ✅ Passou

Dimensão 2: Compatibilidade Cliente
├─ Cliente alérgico? ✓ Sim (severa)
├─ Produto é seguro? ? Precisa avaliar...
└─ Preço ok? ✓ Sim
Resultado: ? Depende de segurança

Dimensão 3: SEGURANÇA ALÉRGICA (Crítico!)
├─ Alergia severa? ✓ SIM
├─ Risco contaminação? ✓ MODERADO (no rótulo)
└─ Há aviso? ✓ SIM (no rótulo)
Resultado: ❌ FALHOU (Crítico!)

DECISÃO FINAL: ❌ REJEITAR
Motivo: Risco de contaminação MODERADO + alergia SEVERA = desastre potencial
```

### 4c. Verifique os Resultados:

```
Esperado vs Realidade:

Exemplo 1 (Ana - deve REJEITAR)
  Esperado: ❌ REJEITAR
  Rubric diz: ❌ REJEITAR
  Resultado: ✅ CORRETO

Exemplo 2 (João - deve APROVAR)
  Esperado: ✅ APROVAR
  Rubric diz: ✅ APROVAR
  Resultado: ✅ CORRETO

Exemplo 3 (Maria - deve APROVAR)
  Esperado: ✅ APROVAR
  Rubric diz: ✅ APROVAR
  Resultado: ✅ CORRETO

... (resto dos exemplos)

TAXA DE ACERTO: 9/10 (90%)
```

### 4d. Se Taxa de Acerto < 80%, Ajuste:

```
Se rubric errou em Exemplo X:
1. Por quê errou?
2. Qual dimensão falhou?
3. Como ajustar critério ou escala?

Exemplo:
Rubric REJEITOU quando deveria APROVAR
→ Porque escalou risco de contaminação errado
→ Dimensão 3 (Segurança) está muito rígida
→ Ajuste: Adicione exceção "se alergia leve, risco moderado é ok"

Teste de novo
→ Taxa de acerto: 9/10 → 10/10
→ ✅ Pronto!
```

---

## Checklist Rápido: Você Desenhou Um Rubric Bom?

Antes de usar seu rubric em produção, verifique:

```
ESTRUTURA
□ Tem 3-5 dimensões? (não 1, não 20)
□ Cada dimensão tem 2-5 critérios?
□ Critérios são testáveis (não vagos)?

ESCALAS & EXEMPLOS
□ Cada critério tem escala clara?
□ Cada nível tem exemplo concreto?
□ Exemplos fazem sentido com domínio (KODA)?

PESOS
□ Há criterios "Críticos" (bloqueadores)?
□ Há critérios "Alto", "Médio", "Baixo"?
□ Pesos refletem realidade (segurança > promoção)?

LÓGICA
□ Regra de decisão é clara?
□ Se A falha, o que acontece?
□ Dois avaliadores chegam à mesma conclusão?

TESTES
□ Testou com 5-10 exemplos reais?
□ Taxa de acerto >= 80%?
□ Erros fazem sentido ou são bugs do rubric?
```

---

## Template de Rubric em Branco

Aqui está um template que você pode copiar para seu próprio rubric:

```
# Rubric: [Nome]
## Contexto
O que estamos avaliando? Por quê?

## Dimensão 1: [Nome]
### Critério 1.1: [Pergunta testável?]
- **Escala:** [Sim/Não] ou [1-5] ou [Baixo/Médio/Alto]
- **Peso:** [Crítico/Alto/Médio/Baixo]
- **Nível 1 (Pior):** [Exemplo]
- **Nível 2:** [Exemplo]
- **Nível 3 (Melhor):** [Exemplo]

### Critério 1.2: ...

## Dimensão 2: [Nome]
### Critério 2.1: ...

## Lógica de Decisão
Se falha critério crítico X → REJEITAR
Se falha critério alto Y → Reduz confiança
Se passa tudo → APROVAR

## Testes
Testado com X exemplos, taxa de acerto: Y%
```

---

## Resumo: O Processo em 4 Passos

```
PASSO 1: LISTAR
"O que pode dar errado?"
Brainstorm sem filtro
↓
PASSO 2: FORMALIZAR
Transforme problemas em critérios testáveis
"Verificar se X"
↓
PASSO 3: DEFINIR
Escalas, exemplos, pesos
"1-5, com exemplo para cada nível"
↓
PASSO 4: TESTAR
Teste com dados reais
"Taxa de acerto >= 80%"
```

---

**Seção 5 Completa** ✓  
Pronto para Seção 6 (Exemplos JSON Concretos)? Diga "aprova" ou "ajusta". 👇
---

## 💾 Seção 6: Exemplos JSON Concretos

Agora que você sabe **como desenhar** um rubric, veja rubrics **reais** em formato JSON que você pode usar, modificar ou servir como template.

Você verá:
1. **Rubric Genérico:** Avaliar qualidade de recomendação de produto
2. **Rubric KODA Específico:** Validar se pedido é seguro para processar
3. **Rubric Simples:** Avaliar clareza de resposta

Cada um é **100% funcional** — você pode copiar, colar e usar.

---

## Exemplo 1: Rubric Genérico - Qualidade de Recomendação

Este rubric funciona para qualquer sistema que recomenda produtos.

```json
{
  "rubric_id": "eval-product-recommendation-v1",
  "rubric_name": "Avaliação de Qualidade de Recomendação de Produto",
  "version": "1.0",
  "last_updated": "2026-05-20",
  "context": "Usado por Evaluator para validar recomendações geradas pelo Generator antes de enviar ao cliente",
  
  "decision_logic": "Se falha QUALQUER critério crítico → REJEITAR. Senão, soma pontos. Se >= 150 → APROVAR.",
  
  "dimensions": [
    {
      "dimension_id": "dim_basic_data",
      "dimension_name": "Integridade de Dados Básicos",
      "weight": "critical",
      "description": "O produto existe e é válido?",
      "criteria": [
        {
          "criterion_id": "crit_product_exists",
          "criterion_name": "Produto existe em inventory?",
          "scale_type": "binary",
          "weight": "critical",
          "points": 100,
          "pass_condition": "true",
          "examples": {
            "pass": {
              "scenario": "SKU 'WHEY-ISOLADO-XYZ-250G' encontrado no banco de dados de inventory",
              "result": "✅ PASS"
            },
            "fail": {
              "scenario": "SKU 'WHEY-INEXISTENTE-999' não existe em nenhuma base de dados",
              "result": "❌ FAIL → REJEITAR TUDO"
            }
          }
        },
        {
          "criterion_id": "crit_price_valid",
          "criterion_name": "Preço é válido (0 < preço < 500)?",
          "scale_type": "binary",
          "weight": "critical",
          "points": 100,
          "pass_condition": "price > 0 AND price < 500",
          "examples": {
            "pass": {
              "scenario": "Produto recomendado: Whey Isolado, Preço: R$ 79,90",
              "result": "✅ PASS"
            },
            "fail": {
              "scenario": "Produto recomendado: Whey Premium, Preço: R$ 0 ou R$ 999",
              "result": "❌ FAIL → REJEITAR TUDO"
            }
          }
        },
        {
          "criterion_id": "crit_in_stock",
          "criterion_name": "Produto está em estoque?",
          "scale_type": "binary",
          "weight": "critical",
          "points": 100,
          "pass_condition": "stock_quantity > 0",
          "examples": {
            "pass": {
              "scenario": "Whey Isolado: 150 unidades em estoque",
              "result": "✅ PASS"
            },
            "fail": {
              "scenario": "Whey Isolado: 0 unidades em estoque",
              "result": "❌ FAIL → REJEITAR TUDO"
            }
          }
        }
      ]
    },
    {
      "dimension_id": "dim_compatibility",
      "dimension_name": "Compatibilidade Cliente-Produto",
      "weight": "critical",
      "description": "O produto é seguro e adequado para este cliente específico?",
      "criteria": [
        {
          "criterion_id": "crit_allergen_safety",
          "criterion_name": "Se cliente tem alergia registrada, produto é seguro?",
          "scale_type": "categorical",
          "scale_options": ["N/A (sem alergia)", "safe", "unsafe"],
          "weight": "critical",
          "points_if_pass": 100,
          "points_if_fail": 0,
          "fail_action": "REJEITAR_TUDO",
          "examples": {
            "n_a": {
              "scenario": "Cliente: João Silva, Alergias: [nenhuma registrada]",
              "result": "N/A → Pula este critério"
            },
            "pass": {
              "scenario": "Cliente: Ana Silva, Alergia: Lactose (severa), Produto: Whey Isolado SEM Lactose (rótulo: risco muito baixo)",
              "result": "✅ SAFE"
            },
            "fail": {
              "scenario": "Cliente: Ana Silva, Alergia: Lactose (severa), Produto: Whey Isolado (rótulo: risco moderado de contaminação)",
              "result": "❌ UNSAFE → REJEITAR TUDO"
            }
          }
        },
        {
          "criterion_id": "crit_budget_respect",
          "criterion_name": "Se cliente tem limite orçamentário, preço é respeitado?",
          "scale_type": "binary",
          "weight": "high",
          "points": 50,
          "examples": {
            "pass": {
              "scenario": "Cliente: Orçamento R$ 80/mês, Recomendação: R$ 79,90",
              "result": "✅ PASS"
            },
            "fail": {
              "scenario": "Cliente: Orçamento R$ 80/mês, Recomendação: R$ 85,00",
              "result": "❌ FAIL → Reduz confiança"
            }
          }
        }
      ]
    },
    {
      "dimension_id": "dim_quality",
      "dimension_name": "Qualidade & Contexto",
      "weight": "high",
      "description": "Quão boa é essa recomendação comparada com outras opções?",
      "criteria": [
        {
          "criterion_id": "crit_reviews_safety",
          "criterion_name": "Há reviews negativas sobre segurança?",
          "scale_type": "categorical",
          "scale_options": ["no_reviews", "positive_only", "some_negative", "many_negative"],
          "weight": "high",
          "points": {
            "no_reviews": 40,
            "positive_only": 40,
            "some_negative": 15,
            "many_negative": 0
          },
          "examples": {
            "positive": {
              "scenario": "Whey Isolado XYZ: 500 reviews, 4.8★, nenhuma menção de reação alérgica",
              "result": "✅ Positive or no reviews → +40 pontos"
            },
            "some_negative": {
              "scenario": "Whey Isolado ABC: 300 reviews, 4.2★, 5 reviews mencionam 'alergia'",
              "result": "⚠️ Some negative → +15 pontos"
            },
            "many_negative": {
              "scenario": "Whey Isolado DEF: 200 reviews, 2.1★, 80+ reviews mencionam problemas alérgicos",
              "result": "❌ Many negative → +0 pontos, pode rejeitar"
            }
          }
        },
        {
          "criterion_id": "crit_explanation_quality",
          "criterion_name": "Explicação menciona: (a) benefício específico, (b) compatibilidade com restrição?",
          "scale_type": "numeric",
          "scale_range": [1, 5],
          "weight": "medium",
          "points_per_level": 10,
          "examples": {
            "1": {
              "text": "Recomendo Whey Isolado.",
              "reason": "Muito vago, sem contexto",
              "points": 0
            },
            "2": {
              "text": "Recomendo Whey Isolado porque tem proteína.",
              "reason": "Genérico, não específico ao cliente",
              "points": 10
            },
            "3": {
              "text": "Recomendo Whey Isolado porque tem 25g proteína por dose e é sem lactose como você pediu.",
              "reason": "Menciona benefício + compatibilidade, mas faltam detalhes",
              "points": 20
            },
            "4": {
              "text": "Recomendo Whey Isolado (R$ 79,90). Tem 25g proteína, zero lactose (você tem alergia), e 4.8★ em reviews.",
              "reason": "Claro, contextualizad, faltam só alternativas",
              "points": 30
            },
            "5": {
              "text": "Recomendo Whey Isolado (R$ 79,90/mês). Por quê: (1) 25g proteína por dose, (2) ZERO lactose (você tem alergia severa), (3) Fabricado em linha dedicada, sem risco de contaminação, (4) 4.8★ em 500+ reviews, (5) Sabor morango (seu preferido). Alternativa: Whey Vegano (R$ 85) se prefere plant-based.",
              "reason": "Cristalino, todos detalhes, contexto completo",
              "points": 40
            }
          }
        }
      ]
    }
  ],
  
  "decision_rules": {
    "rule_1": {
      "condition": "Qualquer critério Crítico falha",
      "action": "REJEITAR",
      "feedback": "Rejeitado porque: [motivo específico do critério que falhou]"
    },
    "rule_2": {
      "condition": "Todos critérios Críticos passam, mas soma de pontos < 150",
      "action": "REJEITAR",
      "feedback": "Rejeitado porque qualidade geral é baixa (score: X/300)"
    },
    "rule_3": {
      "condition": "Soma entre 150-200 pontos",
      "action": "APROVAR_COM_RESSALVAS",
      "feedback": "Aprovado, mas com ressalvas: [detalhes de critérios que poderiam melhorar]"
    },
    "rule_4": {
      "condition": "Soma >= 200 pontos",
      "action": "APROVAR",
      "feedback": "Aprovado com confiança"
    }
  },
  
  "max_points": 300,
  "approval_threshold": 150,
  "high_confidence_threshold": 200
}
```

---

## Exemplo 2: Rubric KODA Específico - Validação de Pedido

Este rubric é usado **especificamente no KODA** para validar pedidos antes de enviar para fulfillment.

```json
{
  "rubric_id": "koda-order-validation-v2",
  "rubric_name": "Validação de Pedido Seguro - KODA",
  "version": "2.0",
  "context": "Usado por Evaluator para validar se pedido é seguro para processar (especialmente alergias)",
  "use_cases": ["Processamento de pedido após recomendação", "Validação antes de fulfillment"],
  
  "dimensions": [
    {
      "dimension_id": "dim_allergic_safety",
      "dimension_name": "🚨 SEGURANÇA ALÉRGICA (Bloqueador)",
      "weight": "critical_blocker",
      "description": "Se algum critério aqui falha, REJEITA tudo",
      "failure_mode": "REJECT_ALL_NO_EXCEPTIONS",
      "criteria": [
        {
          "criterion_id": "koda_allergy_severity",
          "criterion_name": "Qual é a severidade da alergia registrada?",
          "scale_type": "categorical",
          "scale_options": ["none", "mild", "moderate", "severe"],
          "weight": "critical",
          "determines_rest_of_evaluation": true,
          "examples": {
            "none": {
              "profile": "Cliente: João, Alérgicos a: [nenhuma]",
              "impact": "Sem restrições especiais",
              "rest_of_eval": "Normal"
            },
            "mild": {
              "profile": "Cliente: Maria, Alérgicos a: Lactose (causa inchaço abdominal leve)",
              "impact": "Verificar rótulo, mas produtos 'sem lactose' são ok",
              "rest_of_eval": "Moderadamente rigoroso"
            },
            "moderate": {
              "profile": "Cliente: Paulo, Alérgicos a: Amendoim (causa coceira de garganta)",
              "impact": "Muito rigoroso. Verificar contaminação cruzada.",
              "rest_of_eval": "Altamente rigoroso"
            },
            "severe": {
              "profile": "Cliente: Ana, Alérgicos a: Lactose (anafilaxia, ida à emergência 2x)",
              "impact": "BLOQUEADOR. Qualquer risco = rejeita.",
              "rest_of_eval": "MÁXIMO RIGOR - ZERO RISCO"
            }
          }
        },
        {
          "criterion_id": "koda_contamination_risk",
          "criterion_name": "Se alergia severa: qual é o risco de contaminação cruzada?",
          "condition": "only_if_severity == 'severe'",
          "scale_type": "categorical",
          "scale_options": ["very_low", "low", "moderate", "high", "very_high"],
          "weight": "critical_blocker",
          "pass_condition": "very_low OR low",
          "fail_condition": "moderate OR high OR very_high",
          "examples": {
            "very_low": {
              "label_text": "Produzido em linha dedicada sem contato com [alérgeno]",
              "example": "100% SEM LACTOSE, produzido em fábrica separada",
              "action": "✅ PASS - Seguro"
            },
            "low": {
              "label_text": "Produzido em fábrica que processa [alérgeno], linha separada com limpeza",
              "example": "Contém SOJA. Fábrica processa amendoim, mas linha diferente.",
              "action": "⚠️ Avaliar com cliente alérgico severo antes"
            },
            "moderate": {
              "label_text": "Equipamento compartilhado com limpeza entre ciclos",
              "example": "Pode conter TRAÇOS de lactose (equipamento compartilhado)",
              "action": "❌ FAIL se alergia severa - REJEITAR"
            },
            "high": {
              "label_text": "Equipamento compartilhado, sem separação clara",
              "example": "Processado em equipamento que também processa leite",
              "action": "❌ FAIL - REJEITAR"
            },
            "very_high": {
              "label_text": "Contém alérgeno diretamente",
              "example": "INGREDIENTES: Soro de leite, lactose, ...",
              "action": "❌ FAIL - REJEITAR IMEDIATAMENTE"
            }
          }
        },
        {
          "criterion_id": "koda_allergen_warning",
          "criterion_name": "Rótulo tem aviso de alergia relevante ao cliente?",
          "scale_type": "binary",
          "weight": "critical",
          "pass_condition": false,
          "fail_action": "REJEITAR",
          "examples": {
            "pass": {
              "scenario": "Rótulo: [sem avisos de lactose para cliente alérgico a lactose]",
              "result": "✅ PASS - Seguro"
            },
            "fail": {
              "scenario": "Rótulo: '⚠️ AVISO: Consulte seu médico antes de usar (alergia)'",
              "result": "❌ FAIL - REJEITAR se alergia severa"
            }
          }
        }
      ]
    },
    {
      "dimension_id": "dim_order_completeness",
      "dimension_name": "Completude do Pedido",
      "weight": "critical",
      "criteria": [
        {
          "criterion_id": "koda_client_valid",
          "criterion_name": "Cliente existe e é válido no sistema?",
          "scale_type": "binary",
          "weight": "critical",
          "examples": {
            "pass": {
              "scenario": "Cliente: Ana Silva (ID: 12847, historicamente válido)",
              "result": "✅ PASS"
            },
            "fail": {
              "scenario": "Cliente: ID inválido ou não encontrado",
              "result": "❌ FAIL - REJEITAR"
            }
          }
        },
        {
          "criterion_id": "koda_product_quantity",
          "criterion_name": "Produto + quantidade estão especificados?",
          "scale_type": "binary",
          "examples": {
            "pass": {
              "scenario": "Pedido: 1x Whey Isolado (250g)",
              "result": "✅ PASS"
            },
            "fail": {
              "scenario": "Pedido: [Produto em branco] ou [quantidade = 0]",
              "result": "❌ FAIL - REJEITAR"
            }
          }
        },
        {
          "criterion_id": "koda_delivery_address",
          "criterion_name": "Endereço de entrega é válido?",
          "scale_type": "binary",
          "examples": {
            "pass": {
              "scenario": "Endereço: Rua X, 123, São Paulo, SP, 01234-567",
              "result": "✅ PASS"
            },
            "fail": {
              "scenario": "Endereço: [em branco] ou [só número inválido]",
              "result": "❌ FAIL - REJEITAR"
            }
          }
        }
      ]
    },
    {
      "dimension_id": "dim_business_logic",
      "dimension_name": "Lógica de Negócio",
      "weight": "high",
      "criteria": [
        {
          "criterion_id": "koda_budget_respected",
          "criterion_name": "Se cliente tem limite orçamentário mensal, é respeitado?",
          "scale_type": "binary",
          "weight": "high",
          "examples": {
            "pass": {
              "scenario": "Cliente: Orçamento R$ 80/mês, Pedido: R$ 79,90",
              "result": "✅ PASS"
            },
            "fail": {
              "scenario": "Cliente: Orçamento R$ 80/mês, Pedido: R$ 99,90",
              "result": "⚠️ WARN - Notificar cliente, mas pode processar"
            }
          }
        },
        {
          "criterion_id": "koda_dietary_preference",
          "criterion_name": "Se cliente é vegano, produto é vegano?",
          "scale_type": "binary",
          "condition": "only_if_dietary_pref == 'vegan'",
          "weight": "high",
          "examples": {
            "pass": {
              "scenario": "Cliente: Vegano, Produto: Whey Vegano",
              "result": "✅ PASS"
            },
            "fail": {
              "scenario": "Cliente: Vegano, Produto: Whey Concentrado (tem leite)",
              "result": "❌ FAIL - REJEITAR"
            }
          }
        }
      ]
    }
  ],
  
  "decision_rules": {
    "blocker_rule": {
      "description": "Se QUALQUER critério em 'dim_allergic_safety' falha",
      "action": "REJEITAR_IMEDIATAMENTE",
      "reason": "Risco de segurança para cliente"
    },
    "completeness_rule": {
      "description": "Se QUALQUER critério em 'dim_order_completeness' falha",
      "action": "REJEITAR",
      "reason": "Pedido não pode ser processado sem informações"
    },
    "business_rule": {
      "description": "Se critério em 'dim_business_logic' falha",
      "action": "AVISAR_E_CONFIRMAR",
      "reason": "Possível conflito com preferência do cliente, mas pode prosseguir"
    }
  }
}
```

---

## Exemplo 3: Rubric Simples - Avaliar Clareza de Resposta

Às vezes você não precisa de algo complexo. Aqui está um rubric bem simples e direto.

```json
{
  "rubric_id": "clarity-evaluation-v1",
  "rubric_name": "Avaliar Clareza de Resposta",
  "version": "1.0",
  "context": "Avaliação simples de quão clara é a resposta do Generator",
  
  "single_dimension": {
    "criterion_id": "clarity_score",
    "criterion_name": "Qual é o nível de clareza?",
    "scale_type": "numeric",
    "scale_range": [1, 5],
    "scale_step": 1,
    
    "levels": [
      {
        "level": 1,
        "label": "Muito Confuso",
        "description": "Cliente definitivamente não entende",
        "example_response": "Whey bom. Compra.",
        "score": 0,
        "action": "REJEITAR"
      },
      {
        "level": 2,
        "label": "Confuso",
        "description": "Cliente tem dúvidas",
        "example_response": "Recomendo whey porque tem proteína.",
        "score": 10,
        "action": "REJEITAR"
      },
      {
        "level": 3,
        "label": "Aceitável",
        "description": "Cliente entende, mas faltam detalhes",
        "example_response": "Recomendo Whey Isolado. Tem 25g proteína, sem lactose.",
        "score": 20,
        "action": "APROVAR_COM_RESSALVAS"
      },
      {
        "level": 4,
        "label": "Claro",
        "description": "Cliente entende bem",
        "example_response": "Recomendo Whey Isolado (R$ 79,90). 25g proteína, zero lactose (você tem alergia), 4.8★ em reviews.",
        "score": 30,
        "action": "APROVAR"
      },
      {
        "level": 5,
        "label": "Cristalino",
        "description": "Cliente tem TODAS informações para decidir",
        "example_response": "Recomendo Whey Isolado (R$ 79,90/mês). Por quê: (1) 25g proteína, (2) ZERO lactose (safe para sua alergia), (3) Fabricado em linha dedicada, (4) 4.8★, (5) Sabor morango (seu preferido). Alternativa: Vegano (R$ 85).",
        "score": 40,
        "action": "APROVAR"
      }
    ]
  },
  
  "decision_rules": {
    "threshold_reject": {
      "condition": "score < 10",
      "action": "REJEITAR"
    },
    "threshold_warn": {
      "condition": "score >= 10 AND score < 20",
      "action": "APROVAR_COM_RESSALVAS"
    },
    "threshold_approve": {
      "condition": "score >= 20",
      "action": "APROVAR"
    }
  }
}
```

---

## Como Usar Esses JSONs

### Cenário 1: Você é Desenvolvedor

```python
import json

# Carregue o rubric
with open('rubric_product_recommendation.json') as f:
    rubric = json.load(f)

# Use em seu Evaluator
def evaluate_recommendation(recommendation, rubric):
    score = 0
    failures = []
    
    for dimension in rubric['dimensions']:
        for criterion in dimension['criteria']:
            result = check_criterion(recommendation, criterion)
            
            if criterion['weight'] == 'critical' and not result:
                return {
                    'decision': 'REJECT',
                    'reason': f"Critério crítico falhou: {criterion['criterion_name']}"
                }
            
            if result:
                score += criterion['points']
            else:
                failures.append(criterion['criterion_name'])
    
    # Aplique lógica de decisão
    if score >= rubric['approval_threshold']:
        return {'decision': 'APPROVE', 'score': score}
    else:
        return {'decision': 'REJECT', 'reason': f"Score baixo: {score}/{rubric['max_points']}"}
```

### Cenário 2: Você é Product Manager

1. Copie um dos JSONs acima
2. Modifique critérios para seu caso de uso
3. Compartilhe com seu Evaluator (seja humano ou IA)
4. Use para avaliar outputs

### Cenário 3: Você é Pesquisador

1. Use o JSON como baseline
2. Execute em seus dados
3. Calcule taxa de acerto
4. Publ publique resultados com o rubric anexado (para reprodutibilidade)

---

## Checklist: Antes de Usar em Produção

```
□ Testei com 10+ exemplos reais?
□ Taxa de acerto >= 80%?
□ Critérios críticos estão realmente críticos?
□ Exemplos fazem sentido no domínio?
□ Decidi: Vou usar Sim/Não, 1-5, ou Categorias?
□ Dois avaliadores chegam à mesma conclusão?
□ Documentei por que cada critério está aqui?
□ Planejei como evoluir o rubric com novo feedback?
```

---

## Próxima Seção

Na próxima seção, você aprenderá os **erros comuns** que as pessoas cometem ao desenhar rubrics — e como evitá-los.

---

**Seção 6 Completa** ✓  
Pronto para Seção 7 (Erros Comuns ao Desenhar Rubrics)? Diga "aprova" ou "ajusta". 👇
---

## ⚠️ Seção 7: Erros Comuns ao Desenhar Rubrics

Você agora sabe **como desenhar um rubric bom**. Mas aprender vendo o que **funciona** é apenas metade. A outra metade é aprender o que **não funciona**.

Nesta seção, você verá os **5 erros mais comuns** que as pessoas cometem — e como corrigi-los.

---

## Erro 1: Critérios Muito Vagos

### ❌ O Problema

Você especifica um critério tão genérico que dois avaliadores interpreta diferentes.

```
RUBRIC RUIM:
Critério: "A recomendação é boa?"
Escala: Sim / Não

Problema:
- Avaliador A: "Boa = funciona para cliente" (aprova)
- Avaliador B: "Boa = perfeita, sem nada para melhorar" (rejeita)
- Mesmo recomendação: aprovada por A, rejeitada por B

Resultado: Inconsistência. Caos.
```

### ✅ A Solução

Seja **específico**. Transforme adjetivos em observáveis.

```
RUBRIC BOM:
Critério: "Recomendação menciona pelo menos 3 destes: 
           (a) benefício específico, 
           (b) compatibilidade com restrição do cliente, 
           (c) preço, 
           (d) reviews, 
           (e) alternativa?"
Escala: Sim / Não

Prova:
- Avaliador A: "Menciona benefício, preço, reviews. Sim."
- Avaliador B: "Menciona benefício, preço, reviews. Sim."
- Mesma decisão ✓
```

### 🔍 Como Reconhecer Este Erro

Pergunte-se:
```
"Se dois avaliadores olham este critério, eles chegam à MESMA conclusão?"

Se resposta = "talvez", seu critério é vago.
Se resposta = "provavelmente não", definitivamente vago.

Se resposta = "100% sim", está bom!
```

---

## Erro 2: Critérios Não-Mensuráveis

### ❌ O Problema

Você especifica algo que **não pode ser testado** de forma objetiva.

```
RUBRIC RUIM:
Critério: "O produto é 'confiável'"
Escala: Sim / Não

Problema:
- O que significa "confiável"?
- Como você testa isto?
- Você verifica: reviews? preço? marca? tudo junto?
- Impossível responder. Critério é inútil.

Resultado: Avaliador fica bloqueado.
```

### ✅ A Solução

Transforme abstrações em observáveis. Procure por evidência.

```
RUBRIC BOM:
Critério: "Produto atende a critérios de confiabilidade:
           □ Reviews médias >= 4.0 de 5
           □ Número de reviews >= 50
           □ Nenhuma reclamação sobre alergia nos últimos 6 meses"
Escala: Sim (atende todos) / Não

Por que bom?
- Cada subcritério é verificável
- Avaliador sabe exatamente o que procurar
- Não há interpretação subjetiva
```

### 🔍 Como Reconhecer Este Erro

Pergunte-se:
```
"Se dou este critério para um desenvolvedor, ele consegue codificar uma verificação automática?"

Se "sim" → mensurável ✓
Se "não, faltam detalhes" → ajuste
Se "não, conceito é abstrato" → refaça do zero
```

**Exemplo de refazer do zero:**

```
ANTES (abstrato):
"Qualidade do produto é alta"

DEPOIS (mensurável):
"Produto tem nota >= 4.0 e nenhuma reclamação em Q3 2026"
```

---

## Erro 3: Falta de Exemplos

### ❌ O Problema

Você define uma escala, mas não mostra **o que significa cada nível**.

```
RUBRIC RUIM:
Critério: "Clareza da explicação"
Escala: 1-5 (1=ruim, 5=ótimo)

Problema:
- O que é "3"? É 60% claro ou 40%?
- Avaliador A: "Razoável, vou dar 3"
- Avaliador B: "Muito confuso, vou dar 3"
- Mesma nota, significados diferentes

Resultado: Não é possível agregar resultados.
```

### ✅ A Solução

Para **cada nível** da escala, forneça um **exemplo concreto**.

```
RUBRIC BOM:
Critério: "Clareza da explicação"
Escala: 1-5

1 = MUITO CONFUSO
  Exemplo: "Compra whey."
  Problema: Cliente não entende nada

2 = CONFUSO
  Exemplo: "Whey tem proteína."
  Problema: Muito genérico, sem contexto

3 = ACEITÁVEL
  Exemplo: "Whey Isolado, 25g proteína, sem lactose."
  Problema: Claro, mas faltam detalhes

4 = CLARO
  Exemplo: "Whey Isolado, R$ 79,90, 25g, sem lactose, 4.8★."
  Problema: Bom, mas sem alternativas

5 = CRISTALINO
  Exemplo: "Whey Isolado (R$ 79,90). Por quê: 25g, zero lactose (sua alergia), 4.8★ (500 reviews), sabor morango. Alternativa: Vegano (R$ 85)."
  Problema: Nenhum (completo)

Resultado: Quando avaliar, você compara com exemplos, não com "intuição"
```

### 🔍 Como Reconhecer Este Erro

```
"Se alguém recebe apenas escala (1-5) e nenhum exemplo, 
 consegue saber o que significa cada número?"

Se "sim, é óbvio" → provavelmente ok
Se "não, precisaria de exemplos" → ERRO! Adicione exemplos
```

---

## Erro 4: Pesos Desbalanceados

### ❌ O Problema

Todos os critérios têm peso igual, mesmo que alguns sejam muito mais importantes.

```
RUBRIC RUIM:
Critério A: "Preço é válido?" (Crítico) - Peso: 10 pontos
Critério B: "Está em promoção?" (Nice-to-have) - Peso: 10 pontos
Critério C: "Risco de alergia?" (Crítico) - Peso: 10 pontos

Problema:
- Um erro em "está em promoção" = mesma penalidade que "risco de alergia"
- Cliente pode receber produto perigoso porque faltou promoção
- Decisão é ridicula

Resultado: Rubric não reflete realidade de negócio
```

### ✅ A Solução

Diferencie critérios por **custo de falhar**.

```
RUBRIC BOM:
Critério A: "Preço é válido?" (Crítico) - Peso: Bloqueador
Critério B: "Está em promoção?" (Nice-to-have) - Peso: 5 pontos
Critério C: "Risco de alergia?" (Crítico) - Peso: Bloqueador

Se falha Bloqueador → REJEITA TUDO (sem contar pontos)
Se falha 5 pontos → Reduz score

Decisão:
Se passa bloqueadores + score >= 80 → APROVAR
Se falha qualquer bloqueador → REJEITAR
```

### 🔍 Como Reconhecer Este Erro

Pergunte-se:

```
"Se este critério falha, qual é a consequência?"

Grave (risco de vida, perda financeira, dano legal)? 
  → Crítico/Bloqueador

Moderada (insatisfação, perda de confiança)?
  → Alto peso

Leve (experiência subótima)?
  → Médio/Baixo peso
```

---

## Erro 5: Lógica de Decisão Confusa

### ❌ O Problema

Você tem critérios e exemplos, mas a **regra final é ambígua**.

```
RUBRIC RUIM:
Dimensão 1: Dados Básicos (varios critérios)
Dimensão 2: Qualidade (varios critérios)
Dimensão 3: Segurança (varios critérios)

"Se tudo está ok, aprovar. Se algo falhar, avaliar."

Problema:
- O que é "tudo está ok"?
- Quantos critérios podem falhar antes de rejeitar?
- É AND (todos precisam passar) ou OR (qualquer um passa)?
- Avaliador fica confuso

Resultado: Cada avaliador implementa lógica diferente
```

### ✅ A Solução

Seja **explícito** sobre a lógica de decisão.

```
RUBRIC BOM:
Lógica de Decisão (deixar MUITO clara):

1. SE qualquer critério em "Segurança" = FALHA
   ENTÃO REJEITAR imediatamente (sem avaliar resto)

2. SE qualquer critério em "Dados Básicos" = FALHA
   ENTÃO REJEITAR (sem avaliar resto)

3. SE todos critérios em "Dados Básicos" E "Segurança" = PASSA
   ENTÃO avaliar "Qualidade"

4. SE score de Qualidade >= 150
   ENTÃO APROVAR

5. SENÃO REJEITAR

Implementação:
```python
if security_checks_fail():
    return REJECT
elif basic_data_checks_fail():
    return REJECT
elif quality_score() >= 150:
    return APPROVE
else:
    return REJECT
```

Não há ambiguidade. Código é direto.
```

### 🔍 Como Reconhecer Este Erro

```
"Se eu fosse um desenvolvedor, conseguiria codificar este rubric em 10 minutos?"

Se "sim" → lógica está clara ✓
Se "não, teria que fazer perguntas" → ERRO! Deixe mais explícito
```

---

## Erro 6: Rubric Muito Longo ou Muito Curto

### ❌ O Problema: Muito Longo

```
RUBRIC GIGANTE:
50 critérios em 10 dimensões
1000 linhas de documentação
15 escalas diferentes

Problema:
- Avaliador demora 30 min por avaliação
- Muito complexo, fácil fazer erro
- Impossível manter/atualizar
- Taxa de erro aumenta

Resultado: Rubric é inútil porque ninguém o usa
```

### ❌ O Problema: Muito Curto

```
RUBRIC MINIMALISTA:
"Está bom? Sim/Não"

Problema:
- Nenhuma granularidade
- Nenhum feedback útil
- Não captura nuances
- Avaliador tem que adivinhar

Resultado: Rubric é inútil porque não fornece qualidade
```

### ✅ A Solução: O Equilíbrio

```
Recomendação:
- 3-5 dimensões ✓
- 2-5 critérios por dimensão ✓
- Total: 6-25 critérios (não 1, não 100)
- Tempo de avaliação: 5-15 minutos (não 1 min, não 1 hora)

Teste:
Se um avaliador conseguir fazer avaliação em < 15 min com consistência,
rubric está bem-tamanho.

Se demora > 30 min, está muito longo.
Se consegue fazer em < 2 min, está muito curto.
```

---

## Erro 7: Rubric Desconectado da Realidade

### ❌ O Problema

Você desenhou rubric bonito, mas **não reflete o que realmente importa** no negócio.

```
RUBRIC DESCONECTADO:
Critério: "Sabor do produto é inovador?"
Critério: "Embalagem tem design moderno?"
Critério: "Marca é conhecida?"

Mas no KODA, o que realmente importa:
- Produto é seguro para alergia?
- Preço é justo?
- Cliente vai usar mesmo?

Resultado: Rubric avalia coisas erradas. Garbage in, garbage out.
```

### ✅ A Solução

Sempre comece com **business impact**.

```
RUBRIC CONECTADO:
1. Brainstorm: "O que causa cliente infeliz ou danifica KODA?"
   → Alergia não respeitada
   → Preço enganoso
   → Produto não chega
   → Explicação confusa

2. Desenhe critérios para evitar isto

3. Resultado: Rubric que realmente protege negócio
```

### 🔍 Como Reconhecer Este Erro

```
"Se este rubric fosse perfeito (100% de acurácia), 
 o cliente ficaria mais feliz?"

Se "sim" → conectado à realidade ✓
Se "não, porque X realmente importa mais" → refaça
```

---

## Checklist: Evite Estes 7 Erros

Antes de usar seu rubric, verifique:

```
CRITÉRIOS
□ Cada critério é específico ou vago?
□ Cada critério é testável ou abstrato?
□ Dois avaliadores chegam à mesma conclusão?

EXEMPLOS
□ Cada nível tem exemplo concreto?
□ Exemplos fazem sentido no domínio?
□ Avaliador consegue comparar com exemplo?

PESOS
□ Pesos refletem importância real?
□ Há critérios "Críticos" que deveriam ser?
□ Há critérios "Baixo" que poderiam ser removidos?

LÓGICA
□ Regra de decisão é codificável?
□ Há ambiguidade na lógica?
□ Seria fácil de manter/atualizar?

TAMANHO
□ Rubric tem 3-5 dimensões?
□ Rubric tem 6-25 critérios?
□ Avaliação leva 5-15 minutos?

REALIDADE
□ Critérios refletem o que realmente importa?
□ Se rubric fosse perfeito, negócio melhoraria?
□ Testei com exemplos reais?
```

---

## Resumo: Os 7 Erros

| Erro | Sintoma | Solução |
|------|---------|--------|
| **1. Vago** | Dois avaliadores discordam | Seja específico |
| **2. Não-mensurável** | "Como testo isto?" | Transforme em observáveis |
| **3. Sem exemplos** | "O que é '3'?" | Forneça exemplos para cada nível |
| **4. Pesos errados** | Promoção = alergia | Diferencie por custo de falhar |
| **5. Lógica confusa** | "É AND ou OR?" | Seja explícito, codificável |
| **6. Tamanho errado** | Avaliador demora 1h | Mantenha 3-5 dimensões |
| **7. Desconectado** | Avalia coisas irrelevantes | Conecte à business impact |

---

**Seção 7 Completa** ✓  
Pronto para Seção 8 (Exercícios Práticos)? Diga "aprova" ou "ajusta". 👇
---

## 🏋️ Seção 8: Exercícios Práticos

Agora é sua vez. Nesta seção, você fará **3 exercícios práticos** que cobrem:

1. **Exercício 1 (Fácil):** Identificar e corrigir um rubric ruim
2. **Exercício 2 (Médio):** Desenhar um rubric do zero
3. **Exercício 3 (Difícil):** Usar um rubric para avaliar outputs reais

**Tempo:** 45-60 minutos total (15 min por exercício + soluções)

---

## 🏋️ Exercício 1: Identificar e Corrigir um Rubric Ruim

### Contexto

Você é consultor de um e-commerce de roupas. Um colega desenhou este rubric para avaliar se recomendações de roupa são boas. **Ele está cheio de erros.**

### O Rubric Ruim

```json
{
  "rubric_name": "Recomendação de Roupa",
  "criteria": [
    {
      "criterion": "Roupa é boa?",
      "scale": "Sim/Não"
    },
    {
      "criterion": "Cliente quer comprar?",
      "scale": "Sim/Não"
    },
    {
      "criterion": "Preço está ok",
      "scale": "1-10"
    },
    {
      "criterion": "Design é bonito",
      "scale": "Sim/Não",
      "weight": "10 pontos"
    },
    {
      "criterion": "Material é de qualidade",
      "scale": "Sim/Não",
      "weight": "10 pontos"
    }
  ],
  "decision_rule": "Se passa em 3 de 5, aprovar"
}
```

### Sua Tarefa

Identifique **pelo menos 5 erros** neste rubric e rescreva-o melhor.

**Dicas:**
- Procure por critérios vagos
- Procure por falta de exemplos
- Procure por problemas de peso/escala
- Procure por lógica confusa

### Espaço para Sua Resposta

```
ERROS IDENTIFICADOS:

1. [Descreva o erro]
   Localização: [qual critério]
   Por quê é erro: [explicação]
   Como corrigir: [sua solução]

2. [Próximo erro]
   ...

RUBRIC REVISADO:
[Cole seu rubric melhorado aqui]
```

---

## 🏋️ Exercício 2: Desenhar um Rubric do Zero

### Contexto

Você trabalha na **Plataforma de Hiring de Desenvolvedores**. Seu sistema usa um Evaluator para verificar se entrevistas técnicas foram feitas corretamente:

- **Candidato:** Desenvolvedor em Python
- **Tarefa na Entrevista:** "Implemente uma função que calcula fibonacci com memoização"
- **Tempo:** 30 minutos
- **Seu Trabalho:** Desenhar rubric para Evaluator avaliar se solução do candidato é boa

### Informações sobre o Contexto

```
O que pode dar errado em uma solução:
- Código não compila/roda
- Solução é lenta (não usa memoização)
- Código é ilegível
- Faltam testes
- Código tem bugs
- Não atende requisitos (ex: não memoiza)
- Candidato copiou código pronto
```

### Sua Tarefa

Desenhe um rubric completo para avaliar se solução de fibonacci é boa. 

**Deve incluir:**
1. 3-5 dimensões
2. 2-5 critérios por dimensão
3. Escalas claras (Sim/Não, 1-5, Categorias)
4. Exemplos para cada nível
5. Lógica de decisão clara

**Formato:** Use JSON ou Markdown estruturado

### Espaço para Sua Resposta

```
# Rubric: Avaliação de Solução Fibonacci

## Dimensão 1: [Nome]
### Critério 1.1: [Pergunta?]
- Escala: [tipo]
- Exemplos:
  - Nível 1: [exemplo]
  - Nível 2: [exemplo]
  - Nível 3: [exemplo]

## Dimensão 2: ...

## Lógica de Decisão:
[Descreva como combina dimensões]

## Testes:
Testado com X exemplos, taxa de acerto: Y%
```

---

## 🏋️ Exercício 3: Usar um Rubric para Avaliar Outputs Reais

### Contexto

Agora você tem dados reais. Um Generator criou 3 recomendações de produto no KODA. Você precisa usar o **Rubric KODA do Exemplo 2 (Seção 6)** para avaliar qual é aprovado e qual é rejeitado.

### Os Dados

#### Recomendação 1: Cliente Carlos

```
Cliente Profile:
- Nome: Carlos Silva
- Alergias: Nenhuma registrada
- Orçamento: R$ 100/mês
- Preferências: Sabor chocolate
- Histórico: Compra Whey Isolado XYZ há 6 meses

Generator Recomendou:
"Recomendo Whey Isolado XYZ (mesmo que você compra). 
 Preço: R$ 89,90/mês
 Por quê: 25g proteína, sabor chocolate, 4.9★ em 1000+ reviews"

Informações do Produto:
- SKU: WHEY-ISO-XYZ-250G
- Preço: R$ 89,90 (atualizado hoje)
- Em estoque: Sim (500 unidades)
- Rótulo: Nenhum aviso de alergias
- Reviews: 4.9★ (1200 reviews, nenhuma menção de problema)
- Severidade da Alergia do Cliente: N/A (sem alergia)
```

#### Recomendação 2: Cliente Diana

```
Cliente Profile:
- Nome: Diana Costa
- Alergias: Lactose (SEVERA - levou à anafilaxia)
- Orçamento: R$ 80/mês
- Preferências: Vegano
- Histórico: Compra produtos veganos, recusa qualquer coisa com lactose

Generator Recomendou:
"Recomendo Whey Vegano Premium (R$ 85). 
 Tem 20g proteína, 100% plant-based, sem lactose."

Informações do Produto:
- SKU: WHEY-VEG-PREM-250G
- Preço: R$ 85,00
- Em estoque: Sim (200 unidades)
- Rótulo: "100% Plant-based, ZERO animais. Produzido em fábrica que processa leite (risco muito baixo)"
- Reviews: 4.6★ (300 reviews, sem menção de reação alérgica)
- Severidade da Alergia do Cliente: SEVERA
- Risco de Contaminação: Muito Baixo (conforme rótulo)
```

#### Recomendação 3: Cliente Elisa

```
Cliente Profile:
- Nome: Elisa Santos
- Alergias: Amendoim (SEVERA - causa anafilaxia)
- Orçamento: R$ 60/mês
- Preferências: Vegano
- Histórico: Muito cautelosa com alérgenos

Generator Recomendou:
"Recomendo Whey Vegano Standard (R$ 55). 
 Bom custo-benefício, sem alérgenos."

Informações do Produto:
- SKU: WHEY-VEG-STD-250G
- Preço: R$ 55,00
- Em estoque: Sim (100 unidades)
- Rótulo: "AVISO: Este produto é processado em equipamento compartilhado com amendoim. Risco de traços = MODERADO. Consulte seu médico."
- Reviews: 3.8★ (150 reviews)
- Severidade da Alergia do Cliente: SEVERA (amendoim)
- Risco de Contaminação: MODERADO (conforme rótulo)
```

### Sua Tarefa

Para **cada uma das 3 recomendações**, execute o Rubric KODA (Seção 6, Exemplo 2) e decida:

1. **APROVAR** ou **REJEITAR**
2. **Por quê** (qual critério passou/falhou)
3. **Feedback** para o Generator

### Espaço para Sua Resposta

```
## RECOMENDAÇÃO 1: Carlos

### Dimensão 1: Segurança Alérgica
- Alergia severa? [SIM/NÃO/N/A]
- Risco de contaminação? [resultado]
- Há aviso de alergias? [SIM/NÃO]
- Resultado desta dimensão: [PASSOU/FALHOU]

### Dimensão 2: Completude do Pedido
[Avalie cada critério]
- Resultado desta dimensão: [PASSOU/FALHOU]

### Dimensão 3: Lógica de Negócio
[Avalie cada critério]
- Resultado desta dimensão: [PASSOU/FALHOU]

### DECISÃO FINAL:
[APROVAR / REJEITAR]

### MOTIVO:
[Explicação clara]

### FEEDBACK PARA GENERATOR:
[O que melhorar, se aplicável]

---

## RECOMENDAÇÃO 2: Diana
[Repita para Diana]

---

## RECOMENDAÇÃO 3: Elisa
[Repita para Elisa]
```

---

## 📋 Como Verificar Suas Respostas

### Exercício 1: Checklist de Erros

Você deveria ter identificado algo como:

```
✓ Critério "Roupa é boa?" é vago (o que significa "boa"?)
✓ Falta exemplos para cada nível
✓ Pesos de "Design" e "Material" são iguais (deveriam ser diferentes?)
✓ Lógica "3 de 5" é confusa (qual 3? se falha crítico?)
✓ Escala inconsistente (alguns Sim/Não, alguns 1-10)
```

### Exercício 2: Checklist de Rubric Bom

Seu rubric deveria ter:

```
✓ 3-5 dimensões (ex: Corretude, Performance, Legibilidade, Testes, Originalidade)
✓ Cada dimensão tem 2-5 critérios testáveis
✓ Cada critério tem escala clara com exemplos
✓ Lógica de decisão clara (ex: "Se falha Corretude → rejeita")
✓ Peso diferenciado (Corretude é crítico, Originalidade é médio)
```

### Exercício 3: Checklist de Decisões

Você deveria ter concluído:

```
Recomendação 1 (Carlos): ✅ APROVAR
  Motivo: Sem alergia, preço ok, produto existe, reviews boas
  
Recomendação 2 (Diana): ✅ APROVAR
  Motivo: Alergia severa, mas risco contaminação muito baixo
  
Recomendação 3 (Elisa): ❌ REJEITAR
  Motivo: Alergia severa + risco contaminação MODERADO
         = bloqueador automático no rubric
```

**Se suas respostas foram diferentes, por quê? Releia o rubric e veja se entendeu a lógica de decisão.**

---

## Dicas para Completar os Exercícios

### Dica 1: Não Precisa Ser Perfeito
Ninguém desenha rubric perfeito na primeira vez. O importante é:
- Tentar
- Aprender com erros
- Iterar

### Dica 2: Use Exemplos Reais
Se estiver em dúvida sobre como especificar algo, procure um **exemplo real** daquilo que você quer medir. Escreva o exemplo, depois defina o critério ao redor.

### Dica 3: Teste com Dados Reais
Só saiba se seu rubric funciona quando testar com dados reais. Use Exercício 3 para isto.

### Dica 4: Pense em Consequências
Sempre pergunte: "Se meu rubric aprovar isto errado, qual é a consequência?" Isto ajuda a priorizar pesos.

---

## Próxima Etapa

Depois de completar os 3 exercícios:

1. **Revise suas respostas** contra checklist acima
2. **Identifique o que errou** e entenda por quê
3. **Refaça o exercício** com melhorias
4. Se taxa de acerto >= 80%, você está pronto! 🎉

---

## Resumo dos Exercícios

| Exercício | O Quê | Tempo | Difículdade |
|-----------|-------|-------|-------------|
| 1 | Identificar erros em rubric existente | 15 min | Fácil |
| 2 | Desenhar rubric do zero | 20 min | Médio |
| 3 | Usar rubric para avaliar dados reais | 25 min | Difícil |

**Total:** ~60 minutos

---

**Seção 8 Completa** ✓  
Pronto para Seção 9 (Aplicação KODA)? Diga "aprova" ou "ajusta". 👇
---

## 🎯 Seção 9: Aplicação KODA

Agora que você entende **como desenhar rubrics**, vamos aplicar isto ao **KODA especificamente**.

Você aprenderá:
1. Como KODA usa rubrics **hoje**
2. Exemplos reais de rubrics que **funcionam**
3. Onde KODA **pode melhorar**
4. Checklist para desenhar novos rubrics KODA

---

## 1. Como KODA Usa Rubrics Hoje

### Cenário: Recomendação de Produto

```
FLUXO ATUAL DO KODA:

Cliente: "Oi KODA, procuro whey protein sem lactose."

1. GENERATOR (Gerador)
   └─ Processa contexto do cliente
   └─ Busca produtos compatíveis
   └─ Cria recomendação
   └─ Output: "Recomendo Whey Isolado XYZ..."

2. EVALUATOR (Avaliador) ← Aqui Usamos Rubric!
   ├─ Recebe a recomendação
   ├─ Aplica rubric de "Qualidade de Recomendação"
   ├─ Verifica: alergia segura? preço ok? explicação clara?
   ├─ Resultado: ✅ APROVAR ou ❌ REJEITAR
   └─ Se rejeitar: feedback para Generator tentar novamente

3. CLIENTE
   └─ Recebe recomendação (se aprovada)
   └─ Decide: compra ou pede alternativa
```

### Rubric Atual do KODA (Versão 1.0)

```json
{
  "rubric_id": "koda-product-recommendation-v1",
  "rubric_name": "Recomendação de Produto - KODA v1.0",
  "dimensions": [
    {
      "dimension_id": "safety",
      "dimension_name": "Segurança (Crítico)",
      "criteria": [
        {
          "criterion": "Se cliente tem alergia severa, risco de contaminação está em nível aceitável?",
          "weight": "blocker"
        },
        {
          "criterion": "Rótulo do produto avisa sobre alérgenos relevantes?",
          "weight": "blocker"
        }
      ]
    },
    {
      "dimension_id": "business",
      "dimension_name": "Lógica de Negócio",
      "criteria": [
        {
          "criterion": "Preço está dentro do orçamento do cliente?",
          "weight": "high"
        },
        {
          "criterion": "Se cliente é vegano, produto é vegano?",
          "weight": "high"
        }
      ]
    },
    {
      "dimension_id": "quality",
      "dimension_name": "Qualidade",
      "criteria": [
        {
          "criterion": "Explicação menciona: (a) benefício, (b) compatibilidade, (c) preço?",
          "weight": "medium"
        },
        {
          "criterion": "Há menção de reviews/ratings do produto?",
          "weight": "low"
        }
      ]
    }
  ]
}
```

**Taxa de Sucesso com este Rubric:**
- 95% de clientes satisfeitos ✓
- 1% de reclamações sobre alergia (down from 3%) ✓
- 2% de devolução por insatisfação ✓
- 2% desconhecido/sem feedback

---

## 2. Exemplos Reais de Rubrics que Funcionam no KODA

### Exemplo 1: Recomendação para Cliente Alérgico Severo

**Caso:** Ana Silva (alergia lactose severa, anafilaxia)

```
RUBRIC ESPECIALIZADO: "Alergia Severa - Protocolo de Segurança"

Pré-Requisito: Apenas se cliente tem alergia severa

Critérios Críticos:
├─ Alergia está marcada como "SEVERA" no sistema?
├─ Produto rótulo NÃO contém o alérgeno?
├─ Risco de contaminação < MODERADO?
└─ Há aviso de anafilaxia no histórico do cliente?

Se QUALQUER falha → REJEITAR (sem exceção)

Resultado para Ana:
"Whey Vegano Premium aprovado porque:
 - Zero lactose (direto no ingrediente)
 - Fabricado em linha dedicada
 - Reviews: nenhuma menção de reação alérgica
 - Preço: R$ 85 (dentro do orçamento)"
```

### Exemplo 2: Recomendação para Cliente First-Time Buyer

**Caso:** João Silva (novo no KODA, sem histórico)

```
RUBRIC ESPECIALIZADO: "First-Time Buyer - Confiança Extra"

Pré-Requisito: Apenas se primeira compra no KODA

Critérios Aumentados:
├─ Produto tem reviews >= 4.0★?
├─ Número de reviews >= 100?
├─ Explicação é MUITO clara (não só aceitável)?
├─ Preço não é premium (para reduzir risco)?
└─ Há menção de "satisfação garantida"?

Peso Aumentado:
"Explicação clara" agora vale mais pontos
(porque primeiro-comprador é mais sensível)

Resultado para João:
"Recomendo Whey Isolado XYZ (R$ 79,90)
 Por quê:
 - 25g proteína por dose
 - 4.9★ em 1200+ reviews (muito confiável)
 - Sabor vanilla (nosso best-seller)
 - Satisfação garantida ou dinheiro de volta
 - Milhares de clientes fizeram primeira compra com este
 
 Como usar: 1 scoop em 200ml leite ou água
 Quando: Pós-treino ou café da manhã"
```

### Exemplo 3: Recomendação com Alternativas

**Caso:** Maria Costa (orçamento apertado, muitas opções)

```
RUBRIC ESPECIALIZADO: "Múltiplas Opções - Recomendação com Comparativa"

Pré-Requisito: Quando há 3+ produtos viáveis

Critérios:
├─ Todos os produtos são seguros para cliente?
├─ Estão ordenados por relevância (1ª opção é a melhor)?
├─ Cada alternativa tem motivo claro de por que diferente?
├─ Preço está marcado para cada uma?
└─ Impacto/benefício está claro para cada nível de preço?

Resultado para Maria:
"3 opções, ordenadas por relevância:

1. MELHOR CUSTO-BENEFÍCIO: Whey Concentrado (R$ 45)
   - Bom: Barato, 20g proteína
   - Limite: Mais carboidratos

2. MELHOR QUALIDADE: Whey Isolado (R$ 79,90)
   - Bom: 25g proteína, filtrado
   - Gasto extra: +R$ 35

3. PREMIUM (se orçamento liberar): Whey Vegano (R$ 99)
   - Bom: Plant-based, ótimo para sostenibilidade
   - Gasto extra: +R$ 54

Recomendação: Comece com #1. Se quiser melhor qualidade depois, upgrade para #2."
```

---

## 3. Onde KODA Pode Melhorar

Embora KODA tenha bons rubrics, há oportunidades:

### Problema 1: Rubric Não Adapta por Contexto do Cliente

**Situação Atual:**
Mesmo rubric para todos os clientes

**Solução:**
Rubrics especializados por tipo de cliente

```
if cliente.alergia_severa:
    use rubric_alergia_severa_v1
elif cliente.is_first_purchase:
    use rubric_first_time_buyer_v1
elif cliente.preferencias_multiplas:
    use rubric_multiplas_opcoes_v1
else:
    use rubric_standard_v1
```

**Impacto esperado:**
Taxa de satisfação: 95% → 98%

### Problema 2: Rubric Não Considera Histórico do Cliente

**Situação Atual:**
Avalia recomendação isolada

**Solução:**
Rubric que compara com histórico

```
criterion = "É melhoria vs última compra do cliente?"

Se cliente comprou Whey Concentrado (R$ 45) 5x,
e agora recomendamos Isolado (R$ 79,90):
  ✓ Pergunte: Por quê é melhoria? (ingrediente novo? cliente pediu upgrade?)
  ✓ Se sim, aprova
  ✓ Se não, propõe alternativa similar
```

**Impacto esperado:**
Reduz clientes comprando "produto errado", aumenta retenção

### Problema 3: Rubric Não Aprende com Feedback

**Situação Atual:**
Rubric é estático

**Solução:**
Rubric que evolui com feedback

```
# Cada rejeição do cliente:
client_feedback = "Este produto causou reação alérgica"
→ Sistema marca: "Este produto deve ser BANNIDO para alérgicos"
→ Rubric futuro: "Se alérgico a X, BLOQUEIA produto Y"
→ Taxa de erro diminui

# Cada aprovação entusiasta:
client_feedback = "Adorei! Melhor que esperava"
→ Sistema marca: "Cliente gostou acima da expectativa"
→ Rubric futuro: "Produtos com padrão similar têm 90% de aprovação"
```

**Impacto esperado:**
Rubric melhora a cada 100 avaliações

---

## 4. Checklist para Desenhar Novo Rubric no KODA

Se você está desenhando um novo rubric para KODA (nova feature, novo tipo de cliente), use este checklist:

### Phase 1: Scoping (Antes de Desenhar)

```
□ Qual é o problema que este rubric resolve?
  (ex: "Muitos clientes alérgicos recebem produtos perigosos")

□ Qual é o impacto de erro?
  (ex: "Risco de vida → Crítico")

□ Quantas avaliações por dia?
  (ex: "500 recomendações/dia")

□ Há clientes específicos que precisa suportar?
  (ex: "Alérgicos severos, veganos, orçamento baixo")

□ Qual é o target de taxa de sucesso?
  (ex: "95% de aprovação com < 2% de erro crítico")
```

### Phase 2: Design (Desenhando)

```
□ Identifiquei 3-5 dimensões?
□ Cada dimensão tem 2-5 critérios?
□ Critérios são testáveis?
□ Há exemplos para cada nível?
□ Lógica de decisão é clara?
□ Há bloqueadores (critérios críticos)?
```

### Phase 3: Testing (Testando)

```
□ Testei com 10+ exemplos reais de KODA?
□ Taxa de acerto >= 80%?
□ Erros fazem sentido (ou são bugs do rubric)?
□ Dois avaliadores (humano + IA) chegam mesma conclusão?
□ Tempo de avaliação < 15 min?
```

### Phase 4: Deployment (Lançando)

```
□ Documentei o rubric em JSON?
□ Treinei Evaluator (se humano) no novo rubric?
□ Tenho plano para evoluir rubric com feedback?
□ Alertas estão configurados se taxa de erro sobe?
□ Plano de rollback se der problema?
```

### Phase 5: Monitoring (Mantendo)

```
□ Rastreiando taxa de sucesso diário?
□ Coletando feedback dos clientes?
□ Revisando erros semanalmente?
□ Atualizando rubric com novos padrões?
□ Versioning correto (v1.0 → v1.1 → v2.0)?
```

---

## 5. Rubric Novo: Processamento de Pedido Seguro

Como exemplo de "novo rubric que você poderia desenhar", aqui está um rubric para uma feature futura do KODA:

```
NOVO FEATURE: "Processamento de Pedido com Proteção Dupla"

Hoje: Recomendação → Cliente aprova → Fulfillment

Novo: Recomendação → Cliente aprova → Evaluator valida → Fulfillment

RUBRIC PARA ESTA NOVA FEATURE:
```

```json
{
  "rubric_id": "koda-order-processing-v1",
  "rubric_name": "Validação de Pedido com Proteção Dupla",
  "version": "1.0",
  "target_success_rate": "99.5%",
  "target_critical_error_rate": "< 0.1%",
  
  "dimensions": [
    {
      "dimension_name": "Integridade do Pedido",
      "weight": "critical",
      "criteria": [
        {
          "criterion": "Cliente, Produto, Endereço estão válidos?",
          "scale": "binary",
          "weight": "blocker"
        }
      ]
    },
    {
      "dimension_name": "Segurança Alérgica (Validação Dupla)",
      "weight": "critical",
      "description": "Verify alergia DUAS vezes (Generator + Evaluator)",
      "criteria": [
        {
          "criterion": "Alergia registrada no perfil?",
          "scale": "binary"
        },
        {
          "criterion": "Produto contém alérgeno?",
          "scale": "binary"
        },
        {
          "criterion": "Cliente confirmou 'estou ciente de risco'?",
          "scale": "binary",
          "weight": "blocker_if_risk_present"
        }
      ]
    },
    {
      "dimension_name": "Conformidade de Negócio",
      "criteria": [
        {
          "criterion": "Preço não aumentou desde recomendação?",
          "scale": "binary"
        },
        {
          "criterion": "Produto ainda em estoque?",
          "scale": "binary"
        }
      ]
    }
  ]
}
```

---

## Resumo: Rubrics no KODA

| Aspecto | Status Hoje | Oportunidade |
|---------|------------|--------------|
| **Rubrics para Recomendação** | ✅ Existe, funciona bem | Melhorar com contexto do cliente |
| **Rubrics para Alergia Severa** | ✅ Existe, crítico | Adicionar feedback loop |
| **Rubrics para Múltiplas Opções** | ⚠️ Básico | Expandir com comparação |
| **Rubrics para Pedido** | ❌ Não existe | Criar (nova feature) |
| **Rubrics que Aprendem** | ❌ Não existe | Implementar (evolução) |

---

## Próxima Seção

Na próxima e final seção (Seção 10), você aprenderá:
1. Como rubrics conectam com Trace Reading
2. Próximos passos na sua jornada de Nível 2
3. Como apresentar/documentar seus rubrics

---

**Seção 9 Completa** ✓  
Pronto para Seção 10 (Próximos Passos - Final)? Diga "aprova" ou "ajusta". 👇
---

## 🚀 Seção 10: Próximos Passos

Parabéns! Você completou o módulo **Rubric Design**. Agora você sabe:

✅ Por que rubrics são críticos para Evaluators  
✅ Como desenhar rubrics bons (7 elementos)  
✅ Como evitar erros comuns  
✅ Como aplicar ao KODA  

Mas há mais a aprender. Nesta seção final, você verá:

1. **Como rubrics conectam** com o próximo arquivo (Trace Reading)
2. **Próximos passos** na jornada de Nível 2
3. **Critérios de conclusão** — você está realmente pronto?
4. **Reflexão final** — o que isto significa para você

---

## 1. Como Rubrics Conectam com Trace Reading

Você agora entende como rubrics **funcionam** quando tudo está bem. Mas e quando algo **dá errado**?

### Cenário: Um Rubric Falha

```
Situação:
Você criou um rubric para avaliar recomendações de produto.
Taxa de acerto: 95% (ótimo!)

Mas depois aparece este caso:
├─ Cliente: Alérgico a lactose (severa)
├─ Produto recomendado: "Whey Vegano Premium"
├─ Seu rubric disse: ✅ APROVAR
├─ Cliente recebeu: ❌ Reação alérgica!!
└─ Seu rubric: FALHOU

Pergunta Crítica:
"POR QUÊ meu rubric aprovou algo perigoso?"
"Onde estava o erro de lógica?"
"Como evitar isto novamente?"

Resposta: Trace Reading
```

### Trace Reading é o Próximo Arquivo

O arquivo `04-trace-reading.md` (Nível 2) ensina você a:

1. **Ler o trace** — log detalhado de cada passo que o Evaluator tomou
2. **Debugar o rubric** — encontrar exatamente onde falhou
3. **Melhorar o rubric** — adicionar caso de teste para evitar repetição

```
PADRÃO:
Rubric Design (você está aqui) → Cria critérios
                ↓
            Trace Reading → Debuga quando falha
                ↓
        Iteration Loop → Melhora rubric continuamente
```

### Exemplo Prático: Debugando Falha de Rubric

```
Seu rubric falhou em Ana (alergia severa)

TRACE READING:
1. Qual foi o passo 1 do Evaluator?
   "Verificar se alergia severa → SIM"
   ✓ Correto

2. Qual foi o passo 2?
   "Verificar risco de contaminação → 'Muito Baixo'"
   ✗ ERRO AQUI! Deveria ser "Baixo", não "Muito Baixo"
   
3. Por quê o erro?
   "Rótulo dizia 'fábrica que processa lactose, risco muito baixo'"
   Avaliador interpretou "fábrica que processa" = "fábrica dedicada"
   
4. Como corrigir?
   Adicionar critério mais específico:
   "Se rótulo menciona 'processado em equipamento compartilhado'
    → risco é BAIXO, não 'muito baixo'"

RESULTADO:
Rubric v1.0 → Rubric v1.1 (com novo critério)
Taxa de erro: 5% → 1%
```

**Lição:** Rubrics não são estáticos. Evoluem com feedback. Trace Reading é como você aprende.

---

## 2. Próximos Passos na Jornada Nível 2

### Tópicos Restantes do Nível 2

```
Nível 2: Padrões Práticos

✅ Tópico 1: Generator/Evaluator Pattern (já completou)
✅ Tópico 2: Sprint Contracts (já completou)
✅ Tópico 3: Rubric Design (VOCÊ ESTÁ AQUI)

→ Tópico 4: Trace Reading (próximo)

Depois:
Exercícios Nível 2 (3 exercícios práticos)
Aplicação KODA Nível 2 (como tudo se junta)
```

### Recomendação: Sequência de Aprendizado

```
HOJE:
□ Complete exercícios da Seção 8
□ Revise exemplos JSON da Seção 6
□ Crie seu próprio rubric (Exercício 2)

AMANHÃ:
□ Leia Trace Reading (04-trace-reading-pattern.md)
□ Entenda como debugar rubrics
□ Comece Exercício 3 do Nível 2

SEMANA PRÓXIMA:
□ Complete todos os exercícios
□ Implemente seu primeiro rubric real em KODA
□ Revise com time, colete feedback
```

### Roadmap Nível 2 → Nível 3

```
Nível 2 (4 semanas):
└─ Você domina: Padrões que melhoram confiabilidade
   └─ Generator/Evaluator
   └─ Sprint Contracts
   └─ Rubric Design ← VOCÊ ESTÁ AQUI
   └─ Trace Reading

Nível 3 (6 semanas):
└─ Você domina: Arquitetura avançada
   └─ Multi-Agent Systems
   └─ State Persistence
   └─ File-Based Coordination
   └─ Server-Side Compaction
   └─ Harness Evolution

Nível 4 (Contínuo):
└─ Você domina: KODA específico
   └─ Customer Journey Flows
   └─ Feature Design Patterns
   └─ Rubrics para KODA
   └─ Melhorias de Harness
```

---

## 3. Critérios de Conclusão — Você Está Realmente Pronto?

Antes de passar para Trace Reading, verifique:

### Conhecimento Conceitual

```
□ Posso explicar por que rubrics são críticos para Evaluators?
  (resposta esperada: "Sem rubric, avaliação é inconsistente/vaga")

□ Entendo os 7 elementos de um bom rubric?
  (resposta: "Critério, Dimensão, Escala, Exemplos, Pesos, Lógica, Feedback")

□ Posso reconhecer um rubric ruim?
  (teste: veja um rubric vago → consiga identificar o erro)

□ Entendo como rubrics conectam com Generator/Evaluator?
  (resposta: "Generator cria, Evaluator avalia usando rubric")
```

### Prática Prática

```
□ Completei Exercício 1 (Identificar erros)?
  Taxa de acerto: >= 80% em erros identificados?

□ Completei Exercício 2 (Desenhar do zero)?
  Meu rubric tem: 3-5 dimensões, exemplos claros, lógica testável?

□ Completei Exercício 3 (Usar rubric em dados reais)?
  Minhas decisões sobre Ana, Diana, Elisa fazem sentido?
  (Carlos: APROVAR, Diana: APROVAR, Elisa: REJEITAR)
```

### Mentalidade

```
□ Entendi que rubrics são ferramentas, não verdades absolutas?
  (mindset: "rubrics melhoram, mas não eliminam erro 100%")

□ Posso iterar e melhorar rubrics com feedback?
  (mindset: "v1.0 é começo, não final")

□ Vejo rubrics como forma de comunicação (não só avaliação)?
  (mindset: "rubric diz ao Generator EXATAMENTE o que espero")
```

### Aplicação KODA

```
□ Consigo desenhar rubric para novo caso de uso KODA?
  (ex: "Validação de Pedido com Proteção Dupla")

□ Entendo onde KODA pode melhorar rubrics?
  (ex: "Adaptar por contexto do cliente")

□ Posso listar 3 oportunidades de novo rubric no KODA?
  (ex: "Rubric para detecção de fraude", etc)
```

---

## 4. Como Documentar e Apresentar Seus Rubrics

Quando você desenhar um rubric novo (em KODA ou em outro contexto), você precisará **documentar e apresentar**.

### Template de Documentação

```markdown
# Rubric: [Nome Claro]

## Contexto
O que estamos avaliando? Por quê?
Qual é o problema que resolve?

## Quick Facts
- **Tempo de Avaliação:** 5-15 min
- **Taxa de Sucesso Target:** 95%+
- **Versão:** 1.0
- **Data:** 2026-05-25
- **Criador:** [Seu Nome]

## Dimensões & Critérios
[JSON ou tabela com estrutura]

## Exemplos
[3-5 exemplos reais de aprovação/rejeição]

## Lógica de Decisão
[Pseudocódigo ou descrição clara]

## Testing Results
Testado com X exemplos, taxa de acerto: Y%

## Checklist para Usar
Antes de aplicar este rubric:
□ Item 1
□ Item 2

## Próximos Passos
Como melhorar este rubric?
Feedback esperado?
```

### Apresentação em Reunião de Time

```
ESTRUTURA (20 minutos):

1. PROBLEMA (3 min)
   "Por que precisamos deste rubric?"
   Exemplo: "25% de pedidos rejeitados injustamente"

2. SOLUÇÃO (5 min)
   "Como funciona?"
   Mostre 1-2 exemplos de aprovação/rejeição

3. IMPACTO (3 min)
   "Qual é o impacto esperado?"
   Exemplo: "Taxa de erro: 5% → 1%"

4. DETALHE (5 min)
   "Quais são os critérios?"
   Tabela resumida

5. PERGUNTAS (4 min)
   Abra para discussão
```

---

## 5. Sua Jornada Até Agora

### Reflexão Pessoal

Vamos recapitular onde você começou e aonde chegou:

```
SEMANA 1-2 (Nível 1):
Você aprendeu: "Agentes falham por 3 razões principais"
Mindset: "Isto é um problema? Como resolver?"

SEMANA 3 (Generator/Evaluator):
Você aprendeu: "Separar criador de avaliador evita viés"
Mindset: "Preciso de checkpoints, não self-evaluation"

SEMANA 4 (Sprint Contracts):
Você aprendeu: "Contratos deixam expectativas claras"
Mindset: "Antes de começar, todos devem concordar no sucesso"

SEMANA 5 (Rubric Design - AGORA):
Você aprendeu: "Critérios claros tornam avaliação consistente"
Mindset: "Não é sobre intuição, é sobre sistema"

SEMANA 6 (Trace Reading - PRÓXIMA):
Você aprenderá: "Quando falhar, você debugará com precisão"
Mindset: "Erro é feedback, não fracasso"
```

### O Que Você Agora Pode Fazer

```
Antes deste módulo:
- Você criava rubrics vagos (talvez sem perceber)
- Avaliação era inconsistente
- Quando algo falha, era difícil debugar

Depois deste módulo:
✅ Você desenha rubrics estruturados com 7 elementos claros
✅ Avaliação é consistente entre avaliadores
✅ Quando falha, você consegue debugar (Trace Reading)
✅ Você melhora rubrics iterativamente com feedback
✅ Você consegue comunicar critérios ao time
✅ Você reconhece e evita 7 erros comuns
```

---

## 6. Mensagem Final: Por Que Isto Importa

### Para KODA

Rubrics transformaram KODA de um sistema que causa reações alérgicas para um sistema que as **previne**.

De 75% de recomendações corretas para 98%.

Isto é a diferença entre um produto que **mata** alguém e um produto que **salva** vidas (literalmente — alguns clientes têm alergias anafiláticas).

### Para Você

Você agora tem uma **ferramenta mental** transferível:

- **E-commerce?** Rubric para avaliar recomendações
- **Hiring?** Rubric para avaliar candidatos
- **Code Review?** Rubric para avaliar qualidade
- **Pesquisa?** Rubric para avaliar papers

Qualquer lugar onde precisa fazer avaliação justa e consistente, rubrics funcionam.

### Para o Mundo

LLMs são poderosos, mas falhos. Rubrics são o **guardrail** que transforma LLMs de "*às vezes funcionam*" em "*funcionam de forma confiável 95% das vezes*".

Isto é como você escala IA de "interessante demos" para "produtos que salvam vidas".

---

## 7. Checklist Final: Está Pronto para Próxima Seção?

Antes de começar `04-trace-reading.md`, verifique:

```
CONHECIMENTO
□ Entendo os 7 elementos de um rubric
□ Consigo desenhar rubric com 3-5 dimensões
□ Consigo reconhecer rubric vago
□ Entendo por que rubrics evitam sycophancy

PRÁTICA
□ Completei Exercício 1, 2, 3
□ Taxa de acerto >= 80% em minhas respostas
□ Consegui desenhar um rubric funcional do zero

APLICAÇÃO
□ Tenho exemplo real no KODA que gostaria de melhorar
□ Posso listar 3 critérios para novo rubric
□ Entendo como rubric conecta com Generator/Evaluator

MENTALIDADE
□ Vejo rubric como ferramenta, não verdade absoluta
□ Estou pronto para debugar quando falhar (Trace Reading)
□ Tenho curiosidade de entender POR QUÊ algo falhou
```

Se respondeu SIM a todos → **Você está pronto!** 🎉

Se respondeu NÃO a alguns → **Revise aquela seção** (não há pressa)

---

## 8. Próximos 7 Dias: Seu Roadmap

```
DIA 1 (Hoje):
□ Complete este módulo
□ Revise as 10 seções
□ Faça os 3 exercícios

DIA 2:
□ Crie seu próprio rubric (novo caso de uso)
□ Teste com 5 exemplos
□ Revise com um colega

DIA 3:
□ Comece Trace Reading
□ Entenda lógica de debugging
□ Prepare para próxima módulo

DIA 4-5:
□ Trabalhe em implementação real no KODA
□ Collect feedback do time
□ Iterate e melhore

DIA 6-7:
□ Complete exercícios integrados de Nível 2
□ Prepare para Nível 3
□ Celebre progresso!
```

---

## Recursos Adicionais

### Se Tiver Dúvidas

```
"Como X?" ou "Por quê Y?" → Revise a seção relevante
"Exemplo específico" → Veja Seção 6 (JSON concretos)
"Erro no meu rubric" → Use Seção 7 (Erros Comuns)
"Aplicar ao KODA" → Veja Seção 9 (Aplicação KODA)
```

### Se Quiser Ir Além

```
"Quero rubric ainda mais sofisticado" → Veja Nível 3
"Quero aplicar ao meu negócio" → Crie novo rubric, teste, itere
"Quero entender LLM behavior" → Veja Trace Reading (próximo)
```

### Comunidade

Compartilhe seu rubric com o time:
- "Criei rubric para X, feedback?"
- "Teste este rubric com seus dados"
- "Encontrei erro no padrão, aqui está a melhoria"

---

## Além do Evaluator: A Meta-Rubrica de Classificação de Falhas

Tudo que voce aprendeu sobre rubricas para avaliar outputs de agente se aplica em um nivel acima: **avaliar o proprio harness**. O padrao [[docs/canonical/failure-pattern-classification-loop|Failure Pattern Classification Loop]] estende o conceito de rubrica para classificar falhas recorrentes e converte-las em melhorias sistematicas.

### A Taxonomia como Rubrica do Harness

Assim como uma rubrica de avaliacao tem dimensoes (seguranca, adequacao, clareza), a taxonomia de falhas do harness classifica cada escape ou misbehavior em categorias acionaveis:

| Categoria | O que detecta | Exemplo KODA | Acao tipica |
|---|---|---|---|
| `context_loss` | Agente esqueceu informacao dita antes | Cliente disse que e alergico a lactose no inicio, KODA recomenda whey com lactose na hora 3 | Caso N+1 no tier medium |
| `tool_misuse` | Agente usou ferramenta errada ou com parametros errados | Aplicou cupom vencido porque nao validou `expires_at` | Nova lint rule ou constraint no tool schema |
| `rubric_gap` | Evaluator aprovou algo que deveria ter rejeitado | Score 90 em recomendacao com produto fora de estoque | Adicionar blocker `in_stock` na rubrica |
| `safety_escape` | Output violou regra de seguranca ou saude | Token JWT armazenado em `localStorage` | Nova regra no Security Persona + lint rule |
| `prompt_regression` | Mudanca de prompt causou degradacao | Novo prompt de checkout reduziu taxa de conversao | Rollback + teste A/B antes do proximo deploy |
| `state_persistence` | Estado foi perdido ou corrompido | Carrinho desapareceu apos restart do worker | Checkpoint adicional + teste de recovery |
| `pricing_policy` | Preco, desconto ou cupom aplicado incorretamente | Desconto de 30%% aplicado quando maximo era 15%% | Blocker na rubrica de promo + shadow test |
| `latency_cost` | Componente adicionou latencia ou custo desproporcional | Context Loader: 450ms/turno para 0.008%% de efetividade | Diagnostico de ROI → SIMPLIFY ou REMOVE |

### O Ciclo: Observar → Classificar → Converter → Verificar

```
FALHA ESCAPA EM PRODUCAO
        │
        ▼
┌──────────────────┐
│ 1. OBSERVAR      │  Ticket de suporte, alerta, rejeicao do Evaluator, GC Day
│    Coletar        │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ 2. CLASSIFICAR   │  Aplicar taxonomia: context_loss? tool_misuse? rubric_gap?
│    Taxonomia      │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ 3. CONVERTER      │  Criar caso de regressao, lint rule, atualizacao de skill,
│    Em guardrail   │  ajuste de reviewer prompt, ou novo blocker de rubrica
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ 4. VERIFICAR      │  Caso falha na versao antiga? Passa na candidate?
│    Backfill proof │  Esta na registry de evals? Cobertura documentada?
└──────────────────┘
```

Este ciclo e o que transforma "o time aprendeu com o incidente" em "o harness aprendeu com o incidente". A diferenca e que o harness nao esquece.

**Checklist -- Voce esta classificando falhas sistematicamente?**
- [ ] Toda falha em producao recebe uma categoria da taxonomia?
- [ ] Categorias recorrentes (3+ ocorrencias) geram uma acao de harness, nao apenas um card de correcao?
- [ ] Casos de regressao tem tier assignment (fast/medium/deep) e gate documentado?
- [ ] Casos duplicados sao consolidados (manter um canonico, vincular evidencias)?
- [ ] Casos sem falha por 2+ ciclos sao promovidos a archive com justificativa?

---

## Última Mensagem

> "Um rubric não é perfeição. É clareza."
> 
> Não espera eliminar erro. Espera tornar erro **explícito e corrigível**.
> 
> Com rubric bem feito, você sabe EXATAMENTE onde falhou e como melhorar.
> 
> Sem rubric, você fica confuso, esperando que "algo funcione".
> 
> Escolha clareza. ✨

---

## Parabéns! 🎉

Você completou **Rubric Design — Nível 2, Tópico 3**.

Próximo: **Trace Reading (04-trace-reading.md)**

---

**Seção 10 Completa** ✓ **Módulo Completo** ✓  

🚀 **Pronto para Trace Reading?** Abra `04-trace-reading.md` e continue!

---

*Módulo Completo: Rubric Design | v1.0 | Maio 2026*
