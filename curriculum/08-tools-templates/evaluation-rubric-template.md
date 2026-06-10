---
title: "Evaluation Rubric Template para KODA"
type: curriculum-template
aliases: []
tags: [curriculo-conteudo, template, avaliacao-de-qualidade, criterios-de-avaliacao, rubrica, calibracao, avaliacao-automatizada, validacao-de-outputs]
relates-to: ["[[curriculum/05-core-concepts/08-evaluation-rubrics|Evaluation Rubrics]]", "[[docs/canonical/eval-tier-stratification|Eval Tier Stratification]]"]
last_updated: 2026-06-10
---
# 🎯 Evaluation Rubric Template para KODA
## Uma ferramenta prática para transformar julgamento de qualidade em critérios claros

**Tempo Estimado:** 120 minutos  
**Nível:** 8 - Tools & Templates  
**Pré-requisito:** `02-nivel-2-practical-patterns/03-rubric-design.md`, Generator/Evaluator, Sprint Contracts e noções de trace reading  
**Status:** ✅ Completo - Template pronto para uso em features KODA  
**Data de Criação:** Maio 2026

---

## 📖 Prólogo: O Dia em Que KODA Precisou de um Juiz Melhor

Imagine uma manhã comum no time KODA.

Carlos, da equipe de growth, chega com uma notícia boa: a campanha de creatina do mês anterior vendeu acima do esperado.

Mas Luiza, do suporte, chega com uma notícia menos boa: vinte e sete clientes abriram atendimento porque receberam mensagens confusas sobre a promoção.

O problema não era falta de esforço.

O Generator tinha produzido mensagens educadas.

O Evaluator tinha aprovado quase tudo.

O catálogo estava correto.

O preço estava correto.

A política de desconto estava documentada.

Mesmo assim, algo escapou.

Uma cliente perguntou se podia combinar cupom de primeira compra com promoção relâmpago.

KODA respondeu com confiança: sim.

O pedido entrou.

O checkout aplicou apenas uma promoção.

A cliente se sentiu enganada.

O suporte explicou a regra real.

A venda virou reclamação.

Quando o time abriu o trace, a frase do Evaluator parecia inocente: qualidade geral aceitável.

Essa frase era o problema.

Qualidade geral não é um critério.

Aceitável não diz o que foi verificado.

Ninguém sabia se o Evaluator tinha checado elegibilidade da promoção, clareza da mensagem, riscos de compliance, tom de suporte ou consistência com o checkout.

Ele tinha aprovado porque a resposta soava boa.

Mas soar bom não basta quando KODA mexe com dinheiro, saúde, confiança e expectativa do cliente.

Foi nesse ponto que a equipe percebeu uma diferença simples.

O arquivo `03-rubric-design.md` ensina por que rubrics importam e como pensar sobre elas.

Este arquivo existe para o momento seguinte.

Você já acredita em rubrics.

Agora precisa escrever uma rubric que outro Engineer consiga aplicar amanhã.

Precisa de uma estrutura que caiba em product recommendation, order processing, customer support e promotion validation.

Precisa de exemplos preenchidos, escalas claras, critérios testáveis e um caminho de calibration.

Não basta dizer ao Evaluator para ser criterioso.

Você precisa entregar a régua.

Você precisa dizer onde começa um score 5, onde termina um score 3, e por que um score 1 bloqueia release.

Uma boa rubric transforma debate subjetivo em decisão visível.

Ela não remove julgamento humano.

Ela torna o julgamento auditável.

KODA não precisa de um Evaluator mais confiante.

KODA precisa de um Evaluator que saiba exatamente o que procurar.

Este template é o instrumento para isso.

---

## 🎯 Objetivos Deste Template

1. Construir uma rubric completa para avaliar outputs de long-running agents com consistência.
2. Definir dimensions, criteria, scoring scale, pesos, exemplos e decisão final.
3. Aplicar a mesma estrutura a textual output e structured output.
4. Conectar a rubric ao padrão Generator/Evaluator sem misturar geração com avaliação.
5. Criar calibration process para reduzir bias e aumentar inter-rater reliability.
6. Dar ao time KODA uma linguagem comum para aprovar, rejeitar e iterar outputs.
7. Fornecer um checklist de qualidade para separar rubric boa de rubric fraca.
8. Mostrar aplicações em product recommendation, order processing, customer support e promotion validation.
9. Complementar `02-nivel-2-practical-patterns/03-rubric-design.md` com uma ferramenta operacional.

Ao final, você terá um modelo pronto para copiar, adaptar e anexar a um sprint contract.

---

## 🧭 Como Este Arquivo Complementa Rubric Design

O arquivo `02-nivel-2-practical-patterns/03-rubric-design.md` é a aula de teoria.

Ele explica por que um Evaluator precisa de critérios mensuráveis.

Ele mostra como intuição vaga vira avaliação confiável.

Ele discute erros comuns, anatomia de rubrics e exemplos conceituais.

Este arquivo é diferente.

Ele é uma ferramenta de trabalho.

Use este template quando você já sabe que precisa de uma rubric e quer escrevê-la sem esquecer partes críticas.

A teoria responde: por que uma rubric funciona.

Este template responde: o que eu escrevo no documento da feature.

A teoria ajuda você a pensar.

Este template ajuda você a produzir.

| Necessidade | Arquivo recomendado | Resultado esperado |
|-------------|---------------------|--------------------|
| Entender conceitos de rubric | `03-rubric-design.md` | Você aprende teoria e princípios |
| Escrever uma rubric para uma feature | Este template | Você sai com documento aplicável |
| Ensinar um novo Evaluator | Ambos | Você combina fundamento e operação |
| Revisar uma rubric existente | Este template | Você encontra lacunas e corrige critérios |

---

## 🧱 Visão Geral da Estrutura

Uma rubric de avaliação para KODA precisa responder seis perguntas.

Primeira: qual output está sendo avaliado.

Segunda: qual contexto o Evaluator deve considerar.

Terceira: quais dimensions medem qualidade.

Quarta: quais criteria definem sucesso em cada dimension.

Quinta: qual scoring scale transforma julgamento em score.

Sexta: qual decision rule converte scores em aprovação, revisão ou rejeição.

Sem essas seis respostas, o Evaluator improvisa.

Improviso parece flexível no começo.

Com volume, vira inconsistência.

Em conversas longas, inconsistência vira risco operacional.

Estrutura recomendada:

1. Identidade da rubric
2. Escopo de uso
3. Input esperado
4. Output avaliado
5. Contexto obrigatório
6. Dimensions de qualidade
7. Criteria por dimension
8. Scoring scale
9. Pesos e decision rule
10. Anchor examples
11. Calibration process
12. Failure handling
13. Trace requirements
14. Quality checklist
15. Owner e ciclo de revisão

---

## 🔁 Lifecycle da Rubric

Use este fluxo sempre que criar ou revisar uma rubric para KODA.

```
┌──────────────────────────────────────────────────────────────┐
│  1. DESIGN                                                   │
│  Definir output, contexto, dimensions, criteria e escala      │
└──────────────────────────────┬───────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│  2. CALIBRATION                                               │
│  Testar com anchor examples e comparar avaliações humanas     │
└──────────────────────────────┬───────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│  3. APPLICATION                                               │
│  Evaluator aplica a rubric em outputs reais do Generator      │
└──────────────────────────────┬───────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│  4. TRACE REVIEW                                              │
│  Time lê aprovações, rejeições, dúvidas e falsos positivos    │
└──────────────────────────────┬───────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│  5. ITERATION                                                 │
│  Ajustar criteria, pesos, examples e decision rule            │
└──────────────────────────────┬───────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│  6. VERSIONING                                                │
│  Registrar versão, motivo da mudança e impacto esperado       │
└──────────────────────────────┴───────────────────────────────┘
```

O ponto mais importante do lifecycle é não tratar rubric como documento morto.

Uma rubric começa como hipótese de qualidade.

Ela melhora quando encontra outputs reais.

Ela fica confiável quando humanos diferentes chegam a scores parecidos usando os mesmos criteria.

Ela vira infraestrutura quando cada mudança deixa trace.

---

## 📊 Estratégias de Avaliação Comparadas

| Estratégia | Consistência | Escalabilidade | Custo inicial | Custo por avaliação | Risco de bias | Auditabilidade | Melhor uso |
|------------|--------------|----------------|---------------|---------------------|---------------|----------------|------------|
| Intuição Humana | Baixa a média | Baixa | Baixo | Alto | Alto | Baixa | Decisões raras com contexto rico |
| Checklist Simples | Média | Média | Baixo | Baixo | Médio | Média | Validações objetivas de presença ou formato |
| Rubrica Estruturada | Alta | Alta | Médio | Médio | Médio baixo | Alta | Qualidade com múltiplas dimensions |
| Avaliação Automatizada | Alta para regras claras | Muito alta | Alto | Muito baixo | Médio | Alta | Campos estruturados, regras fixas, smoke checks |
| Rubric com Human Review | Muito alta | Média | Alto | Alto | Baixo | Muito alta | Casos críticos, saúde, dinheiro, compliance |
| Ensemble de Evaluators | Alta | Média | Alto | Alto | Médio baixo | Alta | Outputs ambíguos com risco de falso positivo |
| Golden Dataset | Alta | Alta | Alto | Baixo | Baixo se bem calibrado | Alta | Regression testing de rubrics e prompts |

A escolha certa depende do risco.

Para uma saudação simples, checklist basta.

Para um pedido com pagamento, promoção e restrição alimentar, rubrica estruturada é o mínimo aceitável.

Para decisões que podem causar dano ao cliente, adicione Human Review ou regras determinísticas antes da aprovação final.

KODA deve preferir Rubrica Estruturada como padrão porque combina clareza, custo aceitável e trace auditável.

---

## 🧩 Template Mestre de Rubric

Esta é a estrutura que você deve copiar para uma feature real.

O conteúdo abaixo já está preenchido com instruções concretas e exemplos de formulação.

Quando criar uma nova rubric, substitua os valores de exemplo por valores específicos da feature e mantenha todos os campos.

Nenhuma seção deve ser apagada sem registrar o motivo no sprint contract.

### Nome da rubric
Use um nome específico, por exemplo `KODA Product Recommendation Message Rubric v1`. O nome deve indicar feature, tipo de output e versão.

Pergunta de verificação: uma pessoa fora da feature conseguiria aplicar este campo sem perguntar ao autor?

### Owner
Defina uma pessoa ou squad responsável, por exemplo `Squad Conversational Commerce`. Owner responde por calibration e revisão.

Pergunta de verificação: uma pessoa fora da feature conseguiria aplicar este campo sem perguntar ao autor?

### Versão
Use versionamento simples, por exemplo `v1.0`, `v1.1`, `v2.0`. Mudança em decision rule costuma exigir versão maior.

Pergunta de verificação: uma pessoa fora da feature conseguiria aplicar este campo sem perguntar ao autor?

### Data de vigência
Registre mês e ano em que a rubric começa a valer, por exemplo `Maio 2026`.

Pergunta de verificação: uma pessoa fora da feature conseguiria aplicar este campo sem perguntar ao autor?

### Feature avaliada
Nomeie a feature KODA específica, por exemplo product recommendation, order processing, customer support ou promotion validation.

Pergunta de verificação: uma pessoa fora da feature conseguiria aplicar este campo sem perguntar ao autor?

### Output avaliado
Descreva o artefato que o Generator produz, como mensagem ao cliente, JSON de pedido, ranking de produtos ou resumo de atendimento.

Pergunta de verificação: uma pessoa fora da feature conseguiria aplicar este campo sem perguntar ao autor?

### Input obrigatório
Liste quais dados o Evaluator precisa receber, como conversa, catálogo, inventory, regras de preço, regras de promoção, perfil do cliente e trace do Generator.

Pergunta de verificação: uma pessoa fora da feature conseguiria aplicar este campo sem perguntar ao autor?

### Contexto obrigatório
Explique quais informações antigas da conversa devem ser consideradas para evitar context amnesia.

Pergunta de verificação: uma pessoa fora da feature conseguiria aplicar este campo sem perguntar ao autor?

### Fora de escopo
Declare o que a rubric não avalia, como performance de API, design visual, disponibilidade do WhatsApp ou estoque real fora do snapshot recebido.

Pergunta de verificação: uma pessoa fora da feature conseguiria aplicar este campo sem perguntar ao autor?

### Dimensions
Liste os eixos de qualidade, por exemplo correctness, completeness, safety, clarity e efficiency.

Pergunta de verificação: uma pessoa fora da feature conseguiria aplicar este campo sem perguntar ao autor?

### Criteria
Para cada dimension, escreva critérios observáveis. Cada critério deve poder ser marcado como atendido, parcialmente atendido ou não atendido.

Pergunta de verificação: uma pessoa fora da feature conseguiria aplicar este campo sem perguntar ao autor?

### Scoring scale
Escolha binary, 3-point, 5-point Likert ou weighted composite. Explique o significado de cada score.

Pergunta de verificação: uma pessoa fora da feature conseguiria aplicar este campo sem perguntar ao autor?

### Pesos
Defina peso por dimension quando nem toda dimension tem a mesma importância.

Pergunta de verificação: uma pessoa fora da feature conseguiria aplicar este campo sem perguntar ao autor?

### Gate criteria
Identifique critérios que bloqueiam aprovação mesmo se o score total for alto, como alergia ignorada, preço incorreto ou JSON inválido.

Pergunta de verificação: uma pessoa fora da feature conseguiria aplicar este campo sem perguntar ao autor?

### Decision rule
Defina regras claras para aprovar, pedir revisão ou rejeitar.

Pergunta de verificação: uma pessoa fora da feature conseguiria aplicar este campo sem perguntar ao autor?

### Anchor examples
Inclua exemplos de score alto, médio e baixo com justificativa.

Pergunta de verificação: uma pessoa fora da feature conseguiria aplicar este campo sem perguntar ao autor?

### Calibration method
Defina como humanos e Evaluators vão comparar scores antes de release.

Pergunta de verificação: uma pessoa fora da feature conseguiria aplicar este campo sem perguntar ao autor?

### Trace requirements
Especifique quais campos devem aparecer no trace para auditoria.

Pergunta de verificação: uma pessoa fora da feature conseguiria aplicar este campo sem perguntar ao autor?

### Failure handling
Diga o que acontece quando a rubric reprova, por exemplo retry do Generator, escalonamento humano ou bloqueio de checkout.

Pergunta de verificação: uma pessoa fora da feature conseguiria aplicar este campo sem perguntar ao autor?

### Review cadence
Defina frequência de revisão, por exemplo semanal durante rollout e mensal após estabilização.

Pergunta de verificação: uma pessoa fora da feature conseguiria aplicar este campo sem perguntar ao autor?

---

## 🧮 Scoring Scales Recomendadas

### Binary pass/fail
Use quando o critério é objetivo.
Exemplo: o JSON é parseable.
Exemplo: o preço apresentado bate com o price snapshot.
Vantagem: rápido e claro.
Risco: não captura qualidade intermediária.
Regra prática: se uma falha pode causar dano ao cliente, transforme em gate criterion além de score ponderado.

### 3-point scale
Use quando você precisa separar ruim, aceitável e bom.
Score 1 significa falha clara.
Score 2 significa atende parcialmente, mas precisa revisão.
Score 3 significa atende bem.
Vantagem: reduz debate excessivo.
Regra prática: se uma falha pode causar dano ao cliente, transforme em gate criterion além de score ponderado.

### 5-point Likert
Use quando quality range importa.
Score 1 significa inaceitável.
Score 2 significa fraco.
Score 3 significa aceitável com ressalvas.
Score 4 significa bom.
Score 5 significa excelente.
Regra prática: se uma falha pode causar dano ao cliente, transforme em gate criterion além de score ponderado.

### Weighted composite
Use quando dimensions têm impacto diferente.
Correctness pode valer 40%.
Safety pode valer 30%.
Clarity pode valer 20%.
Efficiency pode valer 10%.
Regra prática: se uma falha pode causar dano ao cliente, transforme em gate criterion além de score ponderado.

---

## 📐 Estrutura de Dimensions, Criteria e Pesos

### Dimension: Correctness
Definição: mede se o output está factualmente correto contra fontes de verdade.
Exemplos de sinais: preço, estoque, restrição alimentar, regra de promoção, status do pedido.
Critério forte: o Evaluator consegue apontar uma evidência no input ou no trace para justificar o score.
Critério fraco: o Evaluator usa opinião vaga como parece bom, soa natural ou provavelmente está certo.
Peso inicial sugerido: ajuste conforme risco da feature e valide em calibration.

### Dimension: Completeness
Definição: mede se o output inclui tudo que a tarefa exige.
Exemplos de sinais: produto, motivo da recomendação, próximos passos, campos obrigatórios, limitações.
Critério forte: o Evaluator consegue apontar uma evidência no input ou no trace para justificar o score.
Critério fraco: o Evaluator usa opinião vaga como parece bom, soa natural ou provavelmente está certo.
Peso inicial sugerido: ajuste conforme risco da feature e valide em calibration.

### Dimension: Safety
Definição: mede se o output evita dano, promessa indevida e risco operacional.
Exemplos de sinais: alergia, contraindicação, cobrança, privacidade, compliance.
Critério forte: o Evaluator consegue apontar uma evidência no input ou no trace para justificar o score.
Critério fraco: o Evaluator usa opinião vaga como parece bom, soa natural ou provavelmente está certo.
Peso inicial sugerido: ajuste conforme risco da feature e valide em calibration.

### Dimension: Clarity
Definição: mede se o cliente ou sistema entende a resposta sem ambiguidade.
Exemplos de sinais: linguagem simples, tom adequado, separação de opções, instruções claras.
Critério forte: o Evaluator consegue apontar uma evidência no input ou no trace para justificar o score.
Critério fraco: o Evaluator usa opinião vaga como parece bom, soa natural ou provavelmente está certo.
Peso inicial sugerido: ajuste conforme risco da feature e valide em calibration.

### Dimension: Efficiency
Definição: mede se o output resolve a tarefa sem gasto desnecessário.
Exemplos de sinais: mensagem curta quando basta, JSON sem campos extras, menor token footprint.
Critério forte: o Evaluator consegue apontar uma evidência no input ou no trace para justificar o score.
Critério fraco: o Evaluator usa opinião vaga como parece bom, soa natural ou provavelmente está certo.
Peso inicial sugerido: ajuste conforme risco da feature e valide em calibration.

### Dimension: Traceability
Definição: mede se a decisão pode ser auditada depois.
Exemplos de sinais: referências a dados usados, reasons, checks, source ids.
Critério forte: o Evaluator consegue apontar uma evidência no input ou no trace para justificar o score.
Critério fraco: o Evaluator usa opinião vaga como parece bom, soa natural ou provavelmente está certo.
Peso inicial sugerido: ajuste conforme risco da feature e valide em calibration.

### Dimension: Consistency
Definição: mede se o output não contradiz conversa ou state anterior.
Exemplos de sinais: preferências, orçamento, endereço, canal, histórico de reclamações.
Critério forte: o Evaluator consegue apontar uma evidência no input ou no trace para justificar o score.
Critério fraco: o Evaluator usa opinião vaga como parece bom, soa natural ou provavelmente está certo.
Peso inicial sugerido: ajuste conforme risco da feature e valide em calibration.

### Dimension: Recoverability
Definição: mede se o output orienta recuperação quando algo falha.
Exemplos de sinais: pedido de dado faltante, fallback seguro, escalonamento humano.
Critério forte: o Evaluator consegue apontar uma evidência no input ou no trace para justificar o score.
Critério fraco: o Evaluator usa opinião vaga como parece bom, soa natural ou provavelmente está certo.
Peso inicial sugerido: ajuste conforme risco da feature e valide em calibration.

---

## 🧪 Decision Rules Prontas Para Uso

### Aprovação estrita
Aprovar apenas se todos os gate criteria passarem e score total for pelo menos 90%. Use em pagamento, alergia, promoção e dados pessoais.
Exemplo de trace: `decision`, `score_total`, `failed_gates`, `dimension_scores`, `evidence` e `next_action`.

### Aprovação com revisão leve
Aprovar se gates passarem e score total for pelo menos 80%. Revisar outputs entre 70% e 79%. Use em mensagens de recomendação.
Exemplo de trace: `decision`, `score_total`, `failed_gates`, `dimension_scores`, `evidence` e `next_action`.

### Retry automático
Se um critério não crítico falhar, devolver feedback específico ao Generator uma vez. Se falhar de novo, escalar.
Exemplo de trace: `decision`, `score_total`, `failed_gates`, `dimension_scores`, `evidence` e `next_action`.

### Human Review
Se safety ou correctness falhar, não fazer retry cego. Escalar para humano ou regra determinística.
Exemplo de trace: `decision`, `score_total`, `failed_gates`, `dimension_scores`, `evidence` e `next_action`.

### Bloqueio de release
Se uma mudança de prompt reduz inter-rater reliability ou aumenta falsos positivos, bloquear release até calibration nova.
Exemplo de trace: `decision`, `score_total`, `failed_gates`, `dimension_scores`, `evidence` e `next_action`.

---

## 🧾 Modelo de Rubric em Markdown

Use este modelo quando a rubric será lida por humanos em planning, review ou onboarding.

```markdown
# Nome: KODA Feature Output Rubric v1

## Escopo
Avalia o output do Generator para uma feature KODA específica antes de envio ao cliente ou ao sistema downstream.

## Output Avaliado
Mensagem, JSON ou decisão produzida pelo Generator.

## Input Obrigatório
Conversa relevante, state persistido, catálogo, inventory, regras de preço, regras de promoção, trace do Generator e sprint contract.

## Dimensions
| Dimension | Peso | Gate | Critério principal |
|-----------|------|------|--------------------|
| Correctness | 40 | Sim | Output bate com fontes de verdade |
| Safety | 30 | Sim | Output não cria risco ao cliente |
| Completeness | 15 | Não | Output cobre todos os requisitos da tarefa |
| Clarity | 10 | Não | Output é claro para cliente ou sistema |
| Traceability | 5 | Não | Output deixa evidência auditável |

## Scoring Scale
1 significa falha grave.
2 significa falha relevante.
3 significa aceitável com ressalvas.
4 significa bom.
5 significa excelente.

## Decision Rule
Aprovar se todos os gates passarem e score ponderado for pelo menos 4.2 de 5.
Pedir revisão se gates passarem e score ponderado ficar entre 3.6 e 4.19.
Rejeitar se qualquer gate falhar ou score ponderado ficar abaixo de 3.6.
```

---

## 🧾 Modelo de Rubric em JSON

Use este modelo quando o Evaluator será automatizado ou quando a rubric precisa entrar em um harness.

```json
{
  "rubric_id": "koda_feature_output_v1",
  "feature": "product_recommendation",
  "output_type": "customer_message",
  "scale": {
    "type": "five_point_likert",
    "min": 1,
    "max": 5,
    "labels": {
      "1": "falha grave",
      "2": "falha relevante",
      "3": "aceitável com ressalvas",
      "4": "bom",
      "5": "excelente"
    }
  },
  "dimensions": [
    {
      "name": "correctness",
      "weight": 0.4,
      "gate": true,
      "criteria": [
        "produto recomendado existe no catálogo recebido",
        "preço citado bate com price snapshot",
        "restrições do cliente foram respeitadas"
      ]
    },
    {
      "name": "safety",
      "weight": 0.3,
      "gate": true,
      "criteria": [
        "não ignora alergias",
        "não promete resultado médico",
        "não inventa disponibilidade"
      ]
    }
  ],
  "decision_rule": {
    "approve_min_score": 4.2,
    "review_min_score": 3.6,
    "reject_on_gate_failure": true
  }
}
```

---

## 📝 Exemplo Completo 1: Textual Output de Product Recommendation

Este exemplo avalia uma mensagem que KODA enviaria a uma cliente procurando suplemento.

O foco é textual output.

O Evaluator julga se a mensagem é correta, completa, segura, clara e consistente com a conversa.

### Contexto da conversa
```text
Cliente: Quero um suplemento para começar academia. Tenho intolerância à lactose, orçamento de R$ 150 e prefiro chocolate.
State persistido: cliente evita lactose, nunca comprou creatina, compra pelo WhatsApp, entrega em São Paulo.
Inventory snapshot: Vegan Protein Chocolate 900g, R$ 139,90, em estoque. Whey Concentrado Chocolate 900g, R$ 99,90, contém lactose. Creatina Monohidratada 300g, R$ 89,90, em estoque.
Sprint contract: recomendar uma opção principal e uma alternativa segura, sem prometer resultado médico.
```

### Output do Generator
```text
Para você, eu recomendo o Vegan Protein Chocolate 900g por R$ 139,90. Ele cabe no seu orçamento, está em estoque em São Paulo e evita lactose. Como alternativa, a Creatina Monohidratada 300g por R$ 89,90 pode ajudar sua rotina de treino, mas ela não substitui proteína. Se quiser, eu já deixo o Vegan Protein no carrinho para você confirmar.
```

### Rubric preenchido
| Dimension | Peso | Gate | Score | Justificativa |
|-----------|------|------|-------|---------------|
| Correctness | 40% | Sim | 5/5 | Produto existe no inventory, preço está correto, restrição de lactose foi respeitada e alternativa foi descrita sem confusão. |
| Safety | 25% | Sim | 5/5 | Não promete ganho muscular garantido, não recomenda produto com lactose e não faz afirmação médica. |
| Completeness | 15% | Não | 5/5 | Mensagem traz opção principal, preço, razão, estoque, alternativa e próximo passo. |
| Clarity | 10% | Não | 5/5 | Texto é curto, direto e separa recomendação principal de alternativa. |
| Consistency | 5% | Não | 5/5 | Respeita orçamento, sabor preferido, local de entrega e primeira compra. |
| Traceability | 5% | Não | 4/5 | Justificativa aponta dados principais, mas poderia citar source ids no trace interno. |

### Cálculo
Correctness: 5 x 40% = 2.00
Safety: 5 x 25% = 1.25
Completeness: 5 x 15% = 0.75
Clarity: 5 x 10% = 0.50
Consistency: 5 x 5% = 0.25
Traceability: 4 x 5% = 0.20
Score ponderado final: 4.95 de 5.
Decision: ✅ Aprovado.

### Feedback do Evaluator
```json
{
  "decision": "approve",
  "score": 4.95,
  "failed_gates": [],
  "strengths": [
    "respeita intolerância à lactose",
    "mantém orçamento do cliente",
    "não promete resultado médico"
  ],
  "improvements": [
    "incluir product_id no trace interno para auditoria"
  ]
}
```

### Exemplo de reprovação para comparação
```text
Recomendo o Whey Concentrado Chocolate 900g por R$ 99,90. Ele é barato, gostoso e vai acelerar seus ganhos em poucas semanas.
```

Motivos de reprovação:
* Ignora intolerância à lactose.
* Recomenda produto com contraindicação para a cliente.
* Promete resultado em poucas semanas.
* Não explica alternativa segura.
* Falha em Safety e Correctness, ambos gate criteria.
Decision: ❌ Rejeitado.

---

## 🧾 Exemplo Completo 2: Structured Output de Order Processing

Este exemplo avalia um JSON produzido pelo Generator durante order processing.

O foco é structured output.

A rubric precisa ser mais rígida em schema, tipos, ids, totals e flags de risco.

### Contexto do pedido
```text
Cliente: Ana Silva
Cliente id: cust_12847
Carrinho: Vegan Protein Chocolate 900g, quantidade 1
Preço snapshot: R$ 139,90
Cupom informado: PRIMEIRA10
Regra do cupom: 10% apenas primeira compra, não cumulativo com promoção relâmpago
Cliente é primeira compra: sim
Entrega: São Paulo capital
```

### Output JSON do Generator
```json
{
  "order_id": "ord_draft_8841",
  "customer_id": "cust_12847",
  "status": "ready_for_confirmation",
  "items": [
    {
      "product_id": "prod_vegan_choc_900",
      "name": "Vegan Protein Chocolate 900g",
      "quantity": 1,
      "unit_price_cents": 13990,
      "line_total_cents": 13990
    }
  ],
  "discounts": [
    {
      "code": "PRIMEIRA10",
      "amount_cents": 1399,
      "reason": "primeira compra elegível"
    }
  ],
  "subtotal_cents": 13990,
  "discount_total_cents": 1399,
  "shipping_cents": 1290,
  "grand_total_cents": 13881,
  "requires_human_review": false,
  "risk_flags": [],
  "confirmation_message": "Ana, seu pedido ficou em R$ 138,81 com o cupom PRIMEIRA10 e frete para São Paulo."
}
```

### Rubric preenchido
| Dimension | Peso | Gate | Score | Justificativa |
|-----------|------|------|-------|---------------|
| Schema validity | 20% | Sim | 5/5 | JSON é parseable, usa campos esperados e tipos corretos. |
| Financial correctness | 30% | Sim | 5/5 | Subtotal, desconto, frete e total batem em centavos. |
| Eligibility correctness | 20% | Sim | 5/5 | Cupom é válido porque cliente é primeira compra e não há promoção cumulativa. |
| Operational readiness | 10% | Não | 5/5 | Status indica confirmação antes de fulfillment, sem pular consentimento. |
| Customer clarity | 10% | Não | 4/5 | Mensagem confirma total e cupom, mas poderia separar subtotal e frete. |
| Traceability | 10% | Não | 4/5 | Reason do desconto está clara, faltam rule_id e price_snapshot_id no JSON. |

### Cálculo
Schema validity: 5 x 20% = 1.00
Financial correctness: 5 x 30% = 1.50
Eligibility correctness: 5 x 20% = 1.00
Operational readiness: 5 x 10% = 0.50
Customer clarity: 4 x 10% = 0.40
Traceability: 4 x 10% = 0.40
Score ponderado final: 4.80 de 5.
Decision: ✅ Aprovado com melhoria recomendada de traceability.

### Feedback do Evaluator
```json
{
  "decision": "approve",
  "score": 4.8,
  "failed_gates": [],
  "dimension_scores": {
    "schema_validity": 5,
    "financial_correctness": 5,
    "eligibility_correctness": 5,
    "operational_readiness": 5,
    "customer_clarity": 4,
    "traceability": 4
  },
  "required_action": "send_to_customer_confirmation"
}
```

### Structured output que deve reprovar
```json
{
  "order_id": "ord_draft_8841",
  "customer_id": "cust_12847",
  "status": "approved",
  "items": [
    {
      "product_id": "prod_vegan_choc_900",
      "quantity": 1,
      "unit_price_cents": 13990
    }
  ],
  "discount_total_cents": 2000,
  "grand_total_cents": 11990,
  "requires_human_review": false
}
```

* Falha Financial correctness porque desconto não bate com PRIMEIRA10.
* Falha Schema validity porque faltam subtotal, shipping e line_total.
* Falha Operational readiness porque status aprovado pula confirmação do cliente.
* Falha Traceability porque não registra motivo do desconto.
* Decision final deve ser rejeição mesmo se algum campo parecer útil.

---

## 🛠️ Guia de Calibration

### Passo 1: Selecionar anchor examples
Escolha pelo menos 5 outputs excelentes, 5 medianos e 5 ruins. Inclua casos de alergia, preço, promoção, JSON inválido e tom inadequado.
Critério de saída: existe evidência escrita de que a etapa foi concluída.

### Passo 2: Avaliação independente
Peça para dois humanos e um Evaluator aplicarem a rubric sem conversar antes. Cada avaliador registra score e evidência.
Critério de saída: existe evidência escrita de que a etapa foi concluída.

### Passo 3: Comparar divergências
Agrupe critérios com diferença maior que 1 ponto em escala de 5. Esses critérios estão ambíguos ou mal ancorados.
Critério de saída: existe evidência escrita de que a etapa foi concluída.

### Passo 4: Medir inter-rater reliability
Calcule porcentagem de concordância simples por dimension. Para uso prático no KODA, busque pelo menos 85% em gate criteria antes de release. Em contextos de pesquisa ou auditoria externa, prefira medidas mais robustas como Cohen's Kappa ou Krippendorff's Alpha, que corrigem concordância por acaso.
Critério de saída: existe evidência escrita de que a etapa foi concluída.

### Passo 5: Detectar bias
Verifique se a rubric favorece mensagens mais longas, tom mais formal, produtos de maior margem ou defaults de um modelo específico.
Critério de saída: existe evidência escrita de que a etapa foi concluída.

### Passo 6: Ajustar criteria
Troque opinião por evidência. Cada critério deve apontar para dado no input, regra de negócio ou trecho do output.
Critério de saída: existe evidência escrita de que a etapa foi concluída.

### Passo 7: Adicionar anchor examples
Para cada score confuso, escreva um exemplo concreto de score 1, 3 e 5.
Critério de saída: existe evidência escrita de que a etapa foi concluída.

### Passo 8: Rodar regression set
Aplique a rubric em outputs antigos que causaram incidentes e confirme que seriam reprovados.
- Inclua N+1 long-session fixtures: conversas 10+ turnos com compactação, 11º turno testa continuidade contextual.
- Inclua casos do Production Failure Regression Flywheel: reclamação de usuário, tool misuse, state persistence failure, scoring gap e escaped edge case.
Critério de saída: existe evidência escrita de que a etapa foi concluída.

#### Template de regression eval case

Use este bloco quando uma saída antiga, incidente ou trace diagnosticada precisa virar caso durável de regressão.

```yaml
regression_eval_case:
  case_id: "regression_YYYY_MM_slug_001"
  source:
    incident_id: "support_or_incident_id"
    trace_id: "trace_id_original"
    production_window: "YYYY-MM-DD/YYYY-MM-DD"
  failure_class: "context_loss | tool_misuse | state_persistence | rubric_gap | prompt_regression | pricing_policy | safety_escape | latency_cost"
  input_fixture: "fixtures/evals/<case_id>/input.json"
  state_fixture: "fixtures/evals/<case_id>/state.json"
  output_under_test: "fixtures/evals/<case_id>/baseline_output.json"
  rubric:
    rubric_id: "recommendation_quality_v1"
    expected_label: "reject"
    expected_dimension_failures:
      - "restriction_compliance"
      - "safety"
  expected_behavior: "Uma frase testável sobre a resposta correta."
  prohibited_behavior: "O comportamento antigo que nunca pode voltar."
  suite_tier: "fast | medium | deep"
  owner: "squad-or-person"
  refresh_trigger: "mudança em prompt/model/tool/rubric/context/memory/agent-loop relacionado"
  baseline_result: "fails_on_version_x"
  candidate_requirement: "must_pass_before_merge"
```

Checklist do caso:

- [ ] O caso falha na versão que causou ou permitiu o incidente.
- [ ] O caso passa na correção proposta antes do merge.
- [ ] O expected behavior é verificável sem opinião solta.
- [ ] O owner sabe quando atualizar, deduplicar ou arquivar o caso.
- [ ] O tier escolhido é o mais barato que ainda detecta a regressão.

### Passo 9: Registrar versão
Documente o que mudou, por que mudou e qual métrica deve melhorar.
Critério de saída: existe evidência escrita de que a etapa foi concluída.

### Passo 10: Repetir após rollout
Recalibre com dados reais após a primeira semana de uso.
Critério de saída: existe evidência escrita de que a etapa foi concluída.

---

## ⚖️ Bias Detection em Rubrics

Uma rubric pode parecer objetiva e ainda carregar bias.

O bias pode entrar nos pesos, nos exemplos, nas fontes de verdade e no que você decide chamar de qualidade.

Em KODA, isso aparece de formas práticas.

Uma rubric pode favorecer produtos com margem maior se completeness exigir muita explicação comercial.

Pode punir clientes que escrevem com gírias se clarity for confundida com formalidade.

Pode aprovar mensagens longas demais porque parecem cuidadosas.

Pode rejeitar respostas curtas que eram exatamente o que o cliente precisava.

Por isso, calibration não é luxo.

É parte da segurança operacional.

* A rubric avalia o output ou avalia o estilo pessoal do avaliador?
* A rubric exige tom formal quando o canal WhatsApp pede conversa natural?
* A rubric pune respostas curtas mesmo quando o sprint contract pede brevidade?
* A rubric favorece produtos mais caros sem critério explícito de valor para o cliente?
* A rubric trata ausência de evidência como reprovação ou inventa suposição positiva?
* A rubric separa preferência do cliente de preferência do negócio?
* A rubric usa exemplos com perfis variados de cliente, orçamento e restrição?
* A rubric lida bem com português informal, abreviações e mensagens quebradas?
* A rubric diferencia risco real de desconforto estético?
* A rubric registra quando precisa de Human Review em vez de forçar score automático?

---

## ✅ Rubric Quality Checklist

1. **Escopo claro:** A rubric diz exatamente qual output avalia e qual output não avalia.
2. **Fonte de verdade explícita:** Cada critério importante aponta para catálogo, inventory, price snapshot, policy, conversation state ou sprint contract.
3. **Dimensions separadas:** Correctness não se mistura com Clarity, Safety não se mistura com Completeness.
4. **Criteria observáveis:** O Evaluator consegue justificar score com evidência, não com impressão.
5. **Scoring scale ancorada:** Cada score tem significado concreto, especialmente score mínimo, médio e máximo.
6. **Gate criteria definidos:** Falhas críticas bloqueiam aprovação independentemente do score total.
7. **Pesos proporcionais ao risco:** Safety e correctness pesam mais em features com dinheiro, saúde ou compliance.
8. **Anchor examples incluídos:** A rubric mostra outputs aprovados, revisáveis e rejeitados.
9. **Calibration documentada:** Existe processo para comparar humanos e Evaluator antes de release.
10. **Trace suficiente:** A decisão final deixa score, evidência, falhas e próxima ação.
11. **Linguagem simples:** Um Engineer novo consegue aplicar a rubric sem reunião de uma hora.
12. **Sem critérios duplicados:** Cada critério mede uma coisa só.
13. **Sem critérios ornamentais:** Nenhum critério existe apenas porque parece sofisticado.
14. **Atualização versionada:** Mudanças em pesos, gates ou decision rule têm versão e motivo.
15. **Testada com incidentes reais:** Outputs que já causaram problema são usados como regression examples.
16. **Context degradation cases:** late-failure fixtures estão incluídos no regression set.
17. **Regression flywheel:** incidentes, reclamações, tool misuse e scoring gaps têm template de caso com owner, tier e baseline/candidate.

---

## ❌ Sinais de Rubric Ruim

| Sinal | Exemplo ruim | Correção |
|-------|--------------|----------|
| Critério vago | Avalie se está bom. | Troque por critérios específicos como preço correto, restrição respeitada e próximo passo claro. |
| Escala sem âncora | Score 4 significa bom. | Explique o que diferencia 3, 4 e 5 com exemplos. |
| Tudo tem o mesmo peso | Correctness e tom valem igual em order processing. | Peso deve refletir risco real. |
| Sem gate criteria | Score alto compensa alergia ignorada. | Safety crítica deve bloquear aprovação. |
| Sem fonte de verdade | Evaluator decide se preço parece justo. | Preço deve vir de price snapshot. |
| Sem calibration | Cada pessoa usa a rubric de um jeito. | Rode anchor examples e compare scores. |
| Sem trace | A decisão final diz apenas aprovado. | Registre evidence por dimension. |
| Rubric grande demais | Cinquenta critérios para uma saudação simples. | Use checklist simples quando risco é baixo. |
| Rubric pequena demais | Três critérios para checkout com cupom. | Adicione dimensions financeiras e operacionais. |
| Mistura criação com avaliação | Evaluator sugere produto novo em vez de julgar output. | Mantenha Evaluator como juiz, não Generator paralelo. |

---

## 🚀 Aplicações KODA

KODA é o laboratório perfeito para rubrics porque cada feature combina linguagem natural, regras de negócio e risco operacional.

A mesma estrutura funciona em várias partes do produto.

O que muda é o peso das dimensions e os gate criteria.

### Product Recommendation
Output avaliado: Mensagem recomendando produto ao cliente.
Dimensions principais:
* Correctness: produto existe e está em estoque.
* Safety: respeita alergias e restrições.
* Clarity: explica por que a recomendação faz sentido.
* Consistency: respeita orçamento e preferências.
Gate crítico: Reprovar se recomendar produto incompatível com restrição alimentar.
Decision rule sugerida: aprovar apenas com gates limpos e score ponderado mínimo de 4.2 em escala de 5.
Trace mínimo: input ids, score por dimension, failed gates, evidence e next action.

### Order Processing
Output avaliado: JSON ou decisão de pedido antes de confirmação.
Dimensions principais:
* Schema validity: JSON parseable e completo.
* Financial correctness: total em centavos correto.
* Eligibility correctness: cupom e promoção válidos.
* Operational readiness: status não pula confirmação.
Gate crítico: Reprovar se total, desconto ou status estiver incorreto.
Decision rule sugerida: aprovar apenas com gates limpos e score ponderado mínimo de 4.2 em escala de 5.
Trace mínimo: input ids, score por dimension, failed gates, evidence e next action.

### Customer Support
Output avaliado: Resposta a reclamação, dúvida ou pedido de ajuda.
Dimensions principais:
* Empathy: reconhece frustração sem soar mecânico.
* Resolution: oferece próximo passo concreto.
* Accuracy: não inventa política de troca.
* Safety: escala casos sensíveis.
Gate crítico: Reprovar se culpar cliente ou prometer ação não suportada.
Decision rule sugerida: aprovar apenas com gates limpos e score ponderado mínimo de 4.2 em escala de 5.
Trace mínimo: input ids, score por dimension, failed gates, evidence e next action.

### Promotion Validation
Output avaliado: Decisão sobre aplicar ou negar promoção.
Dimensions principais:
* Rule matching: regra certa foi escolhida.
* Non-stackability: combinações proibidas são bloqueadas.
* Customer explanation: motivo é claro.
* Auditability: rule_id aparece no trace.
Gate crítico: Reprovar se aplicar desconto incompatível com policy.
Decision rule sugerida: aprovar apenas com gates limpos e score ponderado mínimo de 4.2 em escala de 5.
Trace mínimo: input ids, score por dimension, failed gates, evidence e next action.

---

## 🧠 Biblioteca de Dimensions Para Copiar

Esta biblioteca ajuda você a montar uma rubric sem começar do zero.
Ela não substitui julgamento de produto.
Ela dá opções concretas para você escolher conforme o risco da feature.
A regra é simples: escolha poucas dimensions, mas escolha bem.

### Cenário 1: Recomendação inicial para cliente novo
Contexto: cliente chega com objetivo amplo e pouco histórico.
Foco da rubric: priorize clareza, segurança de saúde e compatibilidade com orçamento.
Como usar: selecione as dimensions abaixo que realmente afetam a decisão final neste cenário.

#### Dimension: Aderência ao sprint contract
Definição operacional: verifica se o output cumpriu exatamente o acordo feito antes da execução.
Evidência que o Evaluator deve procurar: compare output com promised deliverables.
Sinal de reprovação neste cenário: falha quando o Generator entregou algo diferente do combinado.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Fidelidade ao catálogo
Definição operacional: confirma que produtos citados existem no catálogo recebido.
Evidência que o Evaluator deve procurar: busque product_id, nome, categoria e disponibilidade.
Sinal de reprovação neste cenário: falha quando o output inventa produto ou variante.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Precisão de preço
Definição operacional: confirma que todos os valores batem com price snapshot.
Evidência que o Evaluator deve procurar: calcule centavos, subtotal, desconto, frete e total.
Sinal de reprovação neste cenário: falha quando o cliente vê um valor diferente no checkout.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Compatibilidade com restrições
Definição operacional: garante que alergias, dieta, orçamento e preferências foram respeitados.
Evidência que o Evaluator deve procurar: procure restrições no state e compare com produto.
Sinal de reprovação neste cenário: falha quando uma preferência crítica é ignorada.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Segurança de saúde
Definição operacional: evita conselho médico, promessa clínica e sugestão arriscada.
Evidência que o Evaluator deve procurar: identifique claims de saúde, dose e contraindicações.
Sinal de reprovação neste cenário: falha quando a mensagem parece prescrição.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Tom de WhatsApp
Definição operacional: mantém conversa natural, direta e respeitosa.
Evidência que o Evaluator deve procurar: leia a mensagem como cliente em canal móvel.
Sinal de reprovação neste cenário: falha quando soa como contrato jurídico ou robô frio.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Brevity control
Definição operacional: mantém resposta curta o bastante para o canal.
Evidência que o Evaluator deve procurar: conte blocos de informação e remova redundância.
Sinal de reprovação neste cenário: falha quando uma resposta simples ocupa muitas telas.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Explicação da decisão
Definição operacional: mostra por que a recomendação foi feita.
Evidência que o Evaluator deve procurar: procure razão ligada ao objetivo do cliente.
Sinal de reprovação neste cenário: falha quando o cliente precisa adivinhar o motivo.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Próximo passo claro
Definição operacional: diz ao cliente o que pode fazer agora.
Evidência que o Evaluator deve procurar: verifique se há ação concreta sem pressão indevida.
Sinal de reprovação neste cenário: falha quando termina sem caminho de avanço.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Consentimento antes de cobrança
Definição operacional: não processa pagamento sem confirmação explícita.
Evidência que o Evaluator deve procurar: verifique status e mensagem de confirmação.
Sinal de reprovação neste cenário: falha quando o workflow pula aceite do cliente.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Validade de cupom
Definição operacional: confirma elegibilidade do desconto aplicado.
Evidência que o Evaluator deve procurar: compare cupom com policy e perfil do cliente.
Sinal de reprovação neste cenário: falha quando desconto indevido passa para checkout.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Não cumulatividade
Definição operacional: bloqueia combinação de promoções proibidas.
Evidência que o Evaluator deve procurar: confira stackability rules.
Sinal de reprovação neste cenário: falha quando duas promoções incompatíveis são combinadas.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Integridade de JSON
Definição operacional: garante que structured output é parseable e completo.
Evidência que o Evaluator deve procurar: valide schema, campos obrigatórios e tipos.
Sinal de reprovação neste cenário: falha quando downstream não consegue consumir o payload.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Idempotência operacional
Definição operacional: evita repetir cobrança, pedido ou mensagem sensível.
Evidência que o Evaluator deve procurar: verifique operation_id e status anterior.
Sinal de reprovação neste cenário: falha quando retry vira duplicidade.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Auditabilidade
Definição operacional: deixa evidência suficiente para debug futuro.
Evidência que o Evaluator deve procurar: procure source ids, reasons e checks.
Sinal de reprovação neste cenário: falha quando ninguém consegue explicar a decisão depois.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Separação entre fato e sugestão
Definição operacional: não apresenta opinião como dado de sistema.
Evidência que o Evaluator deve procurar: marque claims sem fonte.
Sinal de reprovação neste cenário: falha quando preferência comercial vira fato.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Controle de inventário
Definição operacional: não recomenda produto fora de estoque.
Evidência que o Evaluator deve procurar: compare inventory snapshot e local de entrega.
Sinal de reprovação neste cenário: falha quando o cliente escolhe algo indisponível.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Localidade de entrega
Definição operacional: considera região, frete e prazo no output.
Evidência que o Evaluator deve procurar: verifique CEP, cidade e shipping rules.
Sinal de reprovação neste cenário: falha quando prazo ou frete não vale para a região.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Privacidade
Definição operacional: não expõe dados pessoais desnecessários.
Evidência que o Evaluator deve procurar: procure telefone, endereço e documentos no output.
Sinal de reprovação neste cenário: falha quando dados sensíveis aparecem sem necessidade.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Escalonamento correto
Definição operacional: manda casos sensíveis para humano quando necessário.
Evidência que o Evaluator deve procurar: verifique risk_flags e requires_human_review.
Sinal de reprovação neste cenário: falha quando automação insiste em caso crítico.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Resolução de ambiguidade
Definição operacional: pede esclarecimento quando dados são insuficientes.
Evidência que o Evaluator deve procurar: procure pergunta objetiva em vez de suposição.
Sinal de reprovação neste cenário: falha quando KODA escolhe sem base.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Consistência com histórico
Definição operacional: não contradiz preferências, pedidos e promessas anteriores.
Evidência que o Evaluator deve procurar: compare output com state persistido.
Sinal de reprovação neste cenário: falha quando context amnesia muda a conversa.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Controle de hallucination
Definição operacional: não inventa produto, política, prazo ou benefício.
Evidência que o Evaluator deve procurar: compare afirmações com fontes recebidas.
Sinal de reprovação neste cenário: falha quando informação sem fonte vira resposta final.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Qualidade de feedback ao Generator
Definição operacional: quando reprova, explica correção específica.
Evidência que o Evaluator deve procurar: verifique se feedback aponta critério e evidência.
Sinal de reprovação neste cenário: falha quando retry recebe crítica genérica.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Custo de token
Definição operacional: evita texto ou campos extras que aumentam context window sem ganho.
Evidência que o Evaluator deve procurar: procure redundância e verbose output.
Sinal de reprovação neste cenário: falha quando cada avaliação polui conversas longas.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

Resumo do cenário: se muitas dimensions parecem críticas, divida a feature em rubrics menores.

### Cenário 2: Recomendação para cliente com alergia
Contexto: cliente informa restrição alimentar crítica.
Foco da rubric: priorize safety, restrições e gate de produto incompatível.
Como usar: selecione as dimensions abaixo que realmente afetam a decisão final neste cenário.

#### Dimension: Aderência ao sprint contract
Definição operacional: verifica se o output cumpriu exatamente o acordo feito antes da execução.
Evidência que o Evaluator deve procurar: compare output com promised deliverables.
Sinal de reprovação neste cenário: falha quando o Generator entregou algo diferente do combinado.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Fidelidade ao catálogo
Definição operacional: confirma que produtos citados existem no catálogo recebido.
Evidência que o Evaluator deve procurar: busque product_id, nome, categoria e disponibilidade.
Sinal de reprovação neste cenário: falha quando o output inventa produto ou variante.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Precisão de preço
Definição operacional: confirma que todos os valores batem com price snapshot.
Evidência que o Evaluator deve procurar: calcule centavos, subtotal, desconto, frete e total.
Sinal de reprovação neste cenário: falha quando o cliente vê um valor diferente no checkout.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Compatibilidade com restrições
Definição operacional: garante que alergias, dieta, orçamento e preferências foram respeitados.
Evidência que o Evaluator deve procurar: procure restrições no state e compare com produto.
Sinal de reprovação neste cenário: falha quando uma preferência crítica é ignorada.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Segurança de saúde
Definição operacional: evita conselho médico, promessa clínica e sugestão arriscada.
Evidência que o Evaluator deve procurar: identifique claims de saúde, dose e contraindicações.
Sinal de reprovação neste cenário: falha quando a mensagem parece prescrição.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Tom de WhatsApp
Definição operacional: mantém conversa natural, direta e respeitosa.
Evidência que o Evaluator deve procurar: leia a mensagem como cliente em canal móvel.
Sinal de reprovação neste cenário: falha quando soa como contrato jurídico ou robô frio.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Brevity control
Definição operacional: mantém resposta curta o bastante para o canal.
Evidência que o Evaluator deve procurar: conte blocos de informação e remova redundância.
Sinal de reprovação neste cenário: falha quando uma resposta simples ocupa muitas telas.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Explicação da decisão
Definição operacional: mostra por que a recomendação foi feita.
Evidência que o Evaluator deve procurar: procure razão ligada ao objetivo do cliente.
Sinal de reprovação neste cenário: falha quando o cliente precisa adivinhar o motivo.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Próximo passo claro
Definição operacional: diz ao cliente o que pode fazer agora.
Evidência que o Evaluator deve procurar: verifique se há ação concreta sem pressão indevida.
Sinal de reprovação neste cenário: falha quando termina sem caminho de avanço.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Consentimento antes de cobrança
Definição operacional: não processa pagamento sem confirmação explícita.
Evidência que o Evaluator deve procurar: verifique status e mensagem de confirmação.
Sinal de reprovação neste cenário: falha quando o workflow pula aceite do cliente.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Validade de cupom
Definição operacional: confirma elegibilidade do desconto aplicado.
Evidência que o Evaluator deve procurar: compare cupom com policy e perfil do cliente.
Sinal de reprovação neste cenário: falha quando desconto indevido passa para checkout.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Não cumulatividade
Definição operacional: bloqueia combinação de promoções proibidas.
Evidência que o Evaluator deve procurar: confira stackability rules.
Sinal de reprovação neste cenário: falha quando duas promoções incompatíveis são combinadas.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Integridade de JSON
Definição operacional: garante que structured output é parseable e completo.
Evidência que o Evaluator deve procurar: valide schema, campos obrigatórios e tipos.
Sinal de reprovação neste cenário: falha quando downstream não consegue consumir o payload.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Idempotência operacional
Definição operacional: evita repetir cobrança, pedido ou mensagem sensível.
Evidência que o Evaluator deve procurar: verifique operation_id e status anterior.
Sinal de reprovação neste cenário: falha quando retry vira duplicidade.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Auditabilidade
Definição operacional: deixa evidência suficiente para debug futuro.
Evidência que o Evaluator deve procurar: procure source ids, reasons e checks.
Sinal de reprovação neste cenário: falha quando ninguém consegue explicar a decisão depois.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Separação entre fato e sugestão
Definição operacional: não apresenta opinião como dado de sistema.
Evidência que o Evaluator deve procurar: marque claims sem fonte.
Sinal de reprovação neste cenário: falha quando preferência comercial vira fato.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Controle de inventário
Definição operacional: não recomenda produto fora de estoque.
Evidência que o Evaluator deve procurar: compare inventory snapshot e local de entrega.
Sinal de reprovação neste cenário: falha quando o cliente escolhe algo indisponível.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Localidade de entrega
Definição operacional: considera região, frete e prazo no output.
Evidência que o Evaluator deve procurar: verifique CEP, cidade e shipping rules.
Sinal de reprovação neste cenário: falha quando prazo ou frete não vale para a região.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Privacidade
Definição operacional: não expõe dados pessoais desnecessários.
Evidência que o Evaluator deve procurar: procure telefone, endereço e documentos no output.
Sinal de reprovação neste cenário: falha quando dados sensíveis aparecem sem necessidade.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Escalonamento correto
Definição operacional: manda casos sensíveis para humano quando necessário.
Evidência que o Evaluator deve procurar: verifique risk_flags e requires_human_review.
Sinal de reprovação neste cenário: falha quando automação insiste em caso crítico.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Resolução de ambiguidade
Definição operacional: pede esclarecimento quando dados são insuficientes.
Evidência que o Evaluator deve procurar: procure pergunta objetiva em vez de suposição.
Sinal de reprovação neste cenário: falha quando KODA escolhe sem base.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Consistência com histórico
Definição operacional: não contradiz preferências, pedidos e promessas anteriores.
Evidência que o Evaluator deve procurar: compare output com state persistido.
Sinal de reprovação neste cenário: falha quando context amnesia muda a conversa.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Controle de hallucination
Definição operacional: não inventa produto, política, prazo ou benefício.
Evidência que o Evaluator deve procurar: compare afirmações com fontes recebidas.
Sinal de reprovação neste cenário: falha quando informação sem fonte vira resposta final.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Qualidade de feedback ao Generator
Definição operacional: quando reprova, explica correção específica.
Evidência que o Evaluator deve procurar: verifique se feedback aponta critério e evidência.
Sinal de reprovação neste cenário: falha quando retry recebe crítica genérica.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Custo de token
Definição operacional: evita texto ou campos extras que aumentam context window sem ganho.
Evidência que o Evaluator deve procurar: procure redundância e verbose output.
Sinal de reprovação neste cenário: falha quando cada avaliação polui conversas longas.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

Resumo do cenário: se muitas dimensions parecem críticas, divida a feature em rubrics menores.

### Cenário 3: Comparação entre três produtos
Contexto: cliente quer decidir entre opções parecidas.
Foco da rubric: priorize explicação da decisão, fidelidade ao catálogo e tom de WhatsApp.
Como usar: selecione as dimensions abaixo que realmente afetam a decisão final neste cenário.

#### Dimension: Aderência ao sprint contract
Definição operacional: verifica se o output cumpriu exatamente o acordo feito antes da execução.
Evidência que o Evaluator deve procurar: compare output com promised deliverables.
Sinal de reprovação neste cenário: falha quando o Generator entregou algo diferente do combinado.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Fidelidade ao catálogo
Definição operacional: confirma que produtos citados existem no catálogo recebido.
Evidência que o Evaluator deve procurar: busque product_id, nome, categoria e disponibilidade.
Sinal de reprovação neste cenário: falha quando o output inventa produto ou variante.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Precisão de preço
Definição operacional: confirma que todos os valores batem com price snapshot.
Evidência que o Evaluator deve procurar: calcule centavos, subtotal, desconto, frete e total.
Sinal de reprovação neste cenário: falha quando o cliente vê um valor diferente no checkout.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Compatibilidade com restrições
Definição operacional: garante que alergias, dieta, orçamento e preferências foram respeitados.
Evidência que o Evaluator deve procurar: procure restrições no state e compare com produto.
Sinal de reprovação neste cenário: falha quando uma preferência crítica é ignorada.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Segurança de saúde
Definição operacional: evita conselho médico, promessa clínica e sugestão arriscada.
Evidência que o Evaluator deve procurar: identifique claims de saúde, dose e contraindicações.
Sinal de reprovação neste cenário: falha quando a mensagem parece prescrição.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Tom de WhatsApp
Definição operacional: mantém conversa natural, direta e respeitosa.
Evidência que o Evaluator deve procurar: leia a mensagem como cliente em canal móvel.
Sinal de reprovação neste cenário: falha quando soa como contrato jurídico ou robô frio.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Brevity control
Definição operacional: mantém resposta curta o bastante para o canal.
Evidência que o Evaluator deve procurar: conte blocos de informação e remova redundância.
Sinal de reprovação neste cenário: falha quando uma resposta simples ocupa muitas telas.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Explicação da decisão
Definição operacional: mostra por que a recomendação foi feita.
Evidência que o Evaluator deve procurar: procure razão ligada ao objetivo do cliente.
Sinal de reprovação neste cenário: falha quando o cliente precisa adivinhar o motivo.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Próximo passo claro
Definição operacional: diz ao cliente o que pode fazer agora.
Evidência que o Evaluator deve procurar: verifique se há ação concreta sem pressão indevida.
Sinal de reprovação neste cenário: falha quando termina sem caminho de avanço.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Consentimento antes de cobrança
Definição operacional: não processa pagamento sem confirmação explícita.
Evidência que o Evaluator deve procurar: verifique status e mensagem de confirmação.
Sinal de reprovação neste cenário: falha quando o workflow pula aceite do cliente.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Validade de cupom
Definição operacional: confirma elegibilidade do desconto aplicado.
Evidência que o Evaluator deve procurar: compare cupom com policy e perfil do cliente.
Sinal de reprovação neste cenário: falha quando desconto indevido passa para checkout.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Não cumulatividade
Definição operacional: bloqueia combinação de promoções proibidas.
Evidência que o Evaluator deve procurar: confira stackability rules.
Sinal de reprovação neste cenário: falha quando duas promoções incompatíveis são combinadas.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Integridade de JSON
Definição operacional: garante que structured output é parseable e completo.
Evidência que o Evaluator deve procurar: valide schema, campos obrigatórios e tipos.
Sinal de reprovação neste cenário: falha quando downstream não consegue consumir o payload.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Idempotência operacional
Definição operacional: evita repetir cobrança, pedido ou mensagem sensível.
Evidência que o Evaluator deve procurar: verifique operation_id e status anterior.
Sinal de reprovação neste cenário: falha quando retry vira duplicidade.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Auditabilidade
Definição operacional: deixa evidência suficiente para debug futuro.
Evidência que o Evaluator deve procurar: procure source ids, reasons e checks.
Sinal de reprovação neste cenário: falha quando ninguém consegue explicar a decisão depois.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Separação entre fato e sugestão
Definição operacional: não apresenta opinião como dado de sistema.
Evidência que o Evaluator deve procurar: marque claims sem fonte.
Sinal de reprovação neste cenário: falha quando preferência comercial vira fato.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Controle de inventário
Definição operacional: não recomenda produto fora de estoque.
Evidência que o Evaluator deve procurar: compare inventory snapshot e local de entrega.
Sinal de reprovação neste cenário: falha quando o cliente escolhe algo indisponível.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Localidade de entrega
Definição operacional: considera região, frete e prazo no output.
Evidência que o Evaluator deve procurar: verifique CEP, cidade e shipping rules.
Sinal de reprovação neste cenário: falha quando prazo ou frete não vale para a região.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Privacidade
Definição operacional: não expõe dados pessoais desnecessários.
Evidência que o Evaluator deve procurar: procure telefone, endereço e documentos no output.
Sinal de reprovação neste cenário: falha quando dados sensíveis aparecem sem necessidade.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Escalonamento correto
Definição operacional: manda casos sensíveis para humano quando necessário.
Evidência que o Evaluator deve procurar: verifique risk_flags e requires_human_review.
Sinal de reprovação neste cenário: falha quando automação insiste em caso crítico.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Resolução de ambiguidade
Definição operacional: pede esclarecimento quando dados são insuficientes.
Evidência que o Evaluator deve procurar: procure pergunta objetiva em vez de suposição.
Sinal de reprovação neste cenário: falha quando KODA escolhe sem base.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Consistência com histórico
Definição operacional: não contradiz preferências, pedidos e promessas anteriores.
Evidência que o Evaluator deve procurar: compare output com state persistido.
Sinal de reprovação neste cenário: falha quando context amnesia muda a conversa.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Controle de hallucination
Definição operacional: não inventa produto, política, prazo ou benefício.
Evidência que o Evaluator deve procurar: compare afirmações com fontes recebidas.
Sinal de reprovação neste cenário: falha quando informação sem fonte vira resposta final.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Qualidade de feedback ao Generator
Definição operacional: quando reprova, explica correção específica.
Evidência que o Evaluator deve procurar: verifique se feedback aponta critério e evidência.
Sinal de reprovação neste cenário: falha quando retry recebe crítica genérica.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Custo de token
Definição operacional: evita texto ou campos extras que aumentam context window sem ganho.
Evidência que o Evaluator deve procurar: procure redundância e verbose output.
Sinal de reprovação neste cenário: falha quando cada avaliação polui conversas longas.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

Resumo do cenário: se muitas dimensions parecem críticas, divida a feature em rubrics menores.

### Cenário 4: Carrinho antes de confirmação
Contexto: KODA monta pedido e precisa pedir aceite.
Foco da rubric: priorize consentimento, preço e operational readiness.
Como usar: selecione as dimensions abaixo que realmente afetam a decisão final neste cenário.

#### Dimension: Aderência ao sprint contract
Definição operacional: verifica se o output cumpriu exatamente o acordo feito antes da execução.
Evidência que o Evaluator deve procurar: compare output com promised deliverables.
Sinal de reprovação neste cenário: falha quando o Generator entregou algo diferente do combinado.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Fidelidade ao catálogo
Definição operacional: confirma que produtos citados existem no catálogo recebido.
Evidência que o Evaluator deve procurar: busque product_id, nome, categoria e disponibilidade.
Sinal de reprovação neste cenário: falha quando o output inventa produto ou variante.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Precisão de preço
Definição operacional: confirma que todos os valores batem com price snapshot.
Evidência que o Evaluator deve procurar: calcule centavos, subtotal, desconto, frete e total.
Sinal de reprovação neste cenário: falha quando o cliente vê um valor diferente no checkout.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Compatibilidade com restrições
Definição operacional: garante que alergias, dieta, orçamento e preferências foram respeitados.
Evidência que o Evaluator deve procurar: procure restrições no state e compare com produto.
Sinal de reprovação neste cenário: falha quando uma preferência crítica é ignorada.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Segurança de saúde
Definição operacional: evita conselho médico, promessa clínica e sugestão arriscada.
Evidência que o Evaluator deve procurar: identifique claims de saúde, dose e contraindicações.
Sinal de reprovação neste cenário: falha quando a mensagem parece prescrição.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Tom de WhatsApp
Definição operacional: mantém conversa natural, direta e respeitosa.
Evidência que o Evaluator deve procurar: leia a mensagem como cliente em canal móvel.
Sinal de reprovação neste cenário: falha quando soa como contrato jurídico ou robô frio.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Brevity control
Definição operacional: mantém resposta curta o bastante para o canal.
Evidência que o Evaluator deve procurar: conte blocos de informação e remova redundância.
Sinal de reprovação neste cenário: falha quando uma resposta simples ocupa muitas telas.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Explicação da decisão
Definição operacional: mostra por que a recomendação foi feita.
Evidência que o Evaluator deve procurar: procure razão ligada ao objetivo do cliente.
Sinal de reprovação neste cenário: falha quando o cliente precisa adivinhar o motivo.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Próximo passo claro
Definição operacional: diz ao cliente o que pode fazer agora.
Evidência que o Evaluator deve procurar: verifique se há ação concreta sem pressão indevida.
Sinal de reprovação neste cenário: falha quando termina sem caminho de avanço.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Consentimento antes de cobrança
Definição operacional: não processa pagamento sem confirmação explícita.
Evidência que o Evaluator deve procurar: verifique status e mensagem de confirmação.
Sinal de reprovação neste cenário: falha quando o workflow pula aceite do cliente.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Validade de cupom
Definição operacional: confirma elegibilidade do desconto aplicado.
Evidência que o Evaluator deve procurar: compare cupom com policy e perfil do cliente.
Sinal de reprovação neste cenário: falha quando desconto indevido passa para checkout.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Não cumulatividade
Definição operacional: bloqueia combinação de promoções proibidas.
Evidência que o Evaluator deve procurar: confira stackability rules.
Sinal de reprovação neste cenário: falha quando duas promoções incompatíveis são combinadas.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Integridade de JSON
Definição operacional: garante que structured output é parseable e completo.
Evidência que o Evaluator deve procurar: valide schema, campos obrigatórios e tipos.
Sinal de reprovação neste cenário: falha quando downstream não consegue consumir o payload.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Idempotência operacional
Definição operacional: evita repetir cobrança, pedido ou mensagem sensível.
Evidência que o Evaluator deve procurar: verifique operation_id e status anterior.
Sinal de reprovação neste cenário: falha quando retry vira duplicidade.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Auditabilidade
Definição operacional: deixa evidência suficiente para debug futuro.
Evidência que o Evaluator deve procurar: procure source ids, reasons e checks.
Sinal de reprovação neste cenário: falha quando ninguém consegue explicar a decisão depois.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Separação entre fato e sugestão
Definição operacional: não apresenta opinião como dado de sistema.
Evidência que o Evaluator deve procurar: marque claims sem fonte.
Sinal de reprovação neste cenário: falha quando preferência comercial vira fato.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Controle de inventário
Definição operacional: não recomenda produto fora de estoque.
Evidência que o Evaluator deve procurar: compare inventory snapshot e local de entrega.
Sinal de reprovação neste cenário: falha quando o cliente escolhe algo indisponível.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Localidade de entrega
Definição operacional: considera região, frete e prazo no output.
Evidência que o Evaluator deve procurar: verifique CEP, cidade e shipping rules.
Sinal de reprovação neste cenário: falha quando prazo ou frete não vale para a região.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Privacidade
Definição operacional: não expõe dados pessoais desnecessários.
Evidência que o Evaluator deve procurar: procure telefone, endereço e documentos no output.
Sinal de reprovação neste cenário: falha quando dados sensíveis aparecem sem necessidade.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Escalonamento correto
Definição operacional: manda casos sensíveis para humano quando necessário.
Evidência que o Evaluator deve procurar: verifique risk_flags e requires_human_review.
Sinal de reprovação neste cenário: falha quando automação insiste em caso crítico.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Resolução de ambiguidade
Definição operacional: pede esclarecimento quando dados são insuficientes.
Evidência que o Evaluator deve procurar: procure pergunta objetiva em vez de suposição.
Sinal de reprovação neste cenário: falha quando KODA escolhe sem base.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Consistência com histórico
Definição operacional: não contradiz preferências, pedidos e promessas anteriores.
Evidência que o Evaluator deve procurar: compare output com state persistido.
Sinal de reprovação neste cenário: falha quando context amnesia muda a conversa.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Controle de hallucination
Definição operacional: não inventa produto, política, prazo ou benefício.
Evidência que o Evaluator deve procurar: compare afirmações com fontes recebidas.
Sinal de reprovação neste cenário: falha quando informação sem fonte vira resposta final.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Qualidade de feedback ao Generator
Definição operacional: quando reprova, explica correção específica.
Evidência que o Evaluator deve procurar: verifique se feedback aponta critério e evidência.
Sinal de reprovação neste cenário: falha quando retry recebe crítica genérica.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Custo de token
Definição operacional: evita texto ou campos extras que aumentam context window sem ganho.
Evidência que o Evaluator deve procurar: procure redundância e verbose output.
Sinal de reprovação neste cenário: falha quando cada avaliação polui conversas longas.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

Resumo do cenário: se muitas dimensions parecem críticas, divida a feature em rubrics menores.

### Cenário 5: Aplicação de cupom de primeira compra
Contexto: cliente informa cupom no meio da conversa.
Foco da rubric: priorize validade de cupom, não cumulatividade e traceability.
Como usar: selecione as dimensions abaixo que realmente afetam a decisão final neste cenário.

#### Dimension: Aderência ao sprint contract
Definição operacional: verifica se o output cumpriu exatamente o acordo feito antes da execução.
Evidência que o Evaluator deve procurar: compare output com promised deliverables.
Sinal de reprovação neste cenário: falha quando o Generator entregou algo diferente do combinado.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Fidelidade ao catálogo
Definição operacional: confirma que produtos citados existem no catálogo recebido.
Evidência que o Evaluator deve procurar: busque product_id, nome, categoria e disponibilidade.
Sinal de reprovação neste cenário: falha quando o output inventa produto ou variante.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Precisão de preço
Definição operacional: confirma que todos os valores batem com price snapshot.
Evidência que o Evaluator deve procurar: calcule centavos, subtotal, desconto, frete e total.
Sinal de reprovação neste cenário: falha quando o cliente vê um valor diferente no checkout.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Compatibilidade com restrições
Definição operacional: garante que alergias, dieta, orçamento e preferências foram respeitados.
Evidência que o Evaluator deve procurar: procure restrições no state e compare com produto.
Sinal de reprovação neste cenário: falha quando uma preferência crítica é ignorada.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Segurança de saúde
Definição operacional: evita conselho médico, promessa clínica e sugestão arriscada.
Evidência que o Evaluator deve procurar: identifique claims de saúde, dose e contraindicações.
Sinal de reprovação neste cenário: falha quando a mensagem parece prescrição.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Tom de WhatsApp
Definição operacional: mantém conversa natural, direta e respeitosa.
Evidência que o Evaluator deve procurar: leia a mensagem como cliente em canal móvel.
Sinal de reprovação neste cenário: falha quando soa como contrato jurídico ou robô frio.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Brevity control
Definição operacional: mantém resposta curta o bastante para o canal.
Evidência que o Evaluator deve procurar: conte blocos de informação e remova redundância.
Sinal de reprovação neste cenário: falha quando uma resposta simples ocupa muitas telas.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Explicação da decisão
Definição operacional: mostra por que a recomendação foi feita.
Evidência que o Evaluator deve procurar: procure razão ligada ao objetivo do cliente.
Sinal de reprovação neste cenário: falha quando o cliente precisa adivinhar o motivo.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Próximo passo claro
Definição operacional: diz ao cliente o que pode fazer agora.
Evidência que o Evaluator deve procurar: verifique se há ação concreta sem pressão indevida.
Sinal de reprovação neste cenário: falha quando termina sem caminho de avanço.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Consentimento antes de cobrança
Definição operacional: não processa pagamento sem confirmação explícita.
Evidência que o Evaluator deve procurar: verifique status e mensagem de confirmação.
Sinal de reprovação neste cenário: falha quando o workflow pula aceite do cliente.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Validade de cupom
Definição operacional: confirma elegibilidade do desconto aplicado.
Evidência que o Evaluator deve procurar: compare cupom com policy e perfil do cliente.
Sinal de reprovação neste cenário: falha quando desconto indevido passa para checkout.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Não cumulatividade
Definição operacional: bloqueia combinação de promoções proibidas.
Evidência que o Evaluator deve procurar: confira stackability rules.
Sinal de reprovação neste cenário: falha quando duas promoções incompatíveis são combinadas.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Integridade de JSON
Definição operacional: garante que structured output é parseable e completo.
Evidência que o Evaluator deve procurar: valide schema, campos obrigatórios e tipos.
Sinal de reprovação neste cenário: falha quando downstream não consegue consumir o payload.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Idempotência operacional
Definição operacional: evita repetir cobrança, pedido ou mensagem sensível.
Evidência que o Evaluator deve procurar: verifique operation_id e status anterior.
Sinal de reprovação neste cenário: falha quando retry vira duplicidade.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Auditabilidade
Definição operacional: deixa evidência suficiente para debug futuro.
Evidência que o Evaluator deve procurar: procure source ids, reasons e checks.
Sinal de reprovação neste cenário: falha quando ninguém consegue explicar a decisão depois.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Separação entre fato e sugestão
Definição operacional: não apresenta opinião como dado de sistema.
Evidência que o Evaluator deve procurar: marque claims sem fonte.
Sinal de reprovação neste cenário: falha quando preferência comercial vira fato.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Controle de inventário
Definição operacional: não recomenda produto fora de estoque.
Evidência que o Evaluator deve procurar: compare inventory snapshot e local de entrega.
Sinal de reprovação neste cenário: falha quando o cliente escolhe algo indisponível.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Localidade de entrega
Definição operacional: considera região, frete e prazo no output.
Evidência que o Evaluator deve procurar: verifique CEP, cidade e shipping rules.
Sinal de reprovação neste cenário: falha quando prazo ou frete não vale para a região.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Privacidade
Definição operacional: não expõe dados pessoais desnecessários.
Evidência que o Evaluator deve procurar: procure telefone, endereço e documentos no output.
Sinal de reprovação neste cenário: falha quando dados sensíveis aparecem sem necessidade.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Escalonamento correto
Definição operacional: manda casos sensíveis para humano quando necessário.
Evidência que o Evaluator deve procurar: verifique risk_flags e requires_human_review.
Sinal de reprovação neste cenário: falha quando automação insiste em caso crítico.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Resolução de ambiguidade
Definição operacional: pede esclarecimento quando dados são insuficientes.
Evidência que o Evaluator deve procurar: procure pergunta objetiva em vez de suposição.
Sinal de reprovação neste cenário: falha quando KODA escolhe sem base.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Consistência com histórico
Definição operacional: não contradiz preferências, pedidos e promessas anteriores.
Evidência que o Evaluator deve procurar: compare output com state persistido.
Sinal de reprovação neste cenário: falha quando context amnesia muda a conversa.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Controle de hallucination
Definição operacional: não inventa produto, política, prazo ou benefício.
Evidência que o Evaluator deve procurar: compare afirmações com fontes recebidas.
Sinal de reprovação neste cenário: falha quando informação sem fonte vira resposta final.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Qualidade de feedback ao Generator
Definição operacional: quando reprova, explica correção específica.
Evidência que o Evaluator deve procurar: verifique se feedback aponta critério e evidência.
Sinal de reprovação neste cenário: falha quando retry recebe crítica genérica.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Custo de token
Definição operacional: evita texto ou campos extras que aumentam context window sem ganho.
Evidência que o Evaluator deve procurar: procure redundância e verbose output.
Sinal de reprovação neste cenário: falha quando cada avaliação polui conversas longas.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

Resumo do cenário: se muitas dimensions parecem críticas, divida a feature em rubrics menores.

### Cenário 6: Promoção relâmpago com estoque baixo
Contexto: campanha ativa tem limite de inventory.
Foco da rubric: priorize inventory, preço e mensagem sem promessa indevida.
Como usar: selecione as dimensions abaixo que realmente afetam a decisão final neste cenário.

#### Dimension: Aderência ao sprint contract
Definição operacional: verifica se o output cumpriu exatamente o acordo feito antes da execução.
Evidência que o Evaluator deve procurar: compare output com promised deliverables.
Sinal de reprovação neste cenário: falha quando o Generator entregou algo diferente do combinado.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Fidelidade ao catálogo
Definição operacional: confirma que produtos citados existem no catálogo recebido.
Evidência que o Evaluator deve procurar: busque product_id, nome, categoria e disponibilidade.
Sinal de reprovação neste cenário: falha quando o output inventa produto ou variante.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Precisão de preço
Definição operacional: confirma que todos os valores batem com price snapshot.
Evidência que o Evaluator deve procurar: calcule centavos, subtotal, desconto, frete e total.
Sinal de reprovação neste cenário: falha quando o cliente vê um valor diferente no checkout.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Compatibilidade com restrições
Definição operacional: garante que alergias, dieta, orçamento e preferências foram respeitados.
Evidência que o Evaluator deve procurar: procure restrições no state e compare com produto.
Sinal de reprovação neste cenário: falha quando uma preferência crítica é ignorada.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Segurança de saúde
Definição operacional: evita conselho médico, promessa clínica e sugestão arriscada.
Evidência que o Evaluator deve procurar: identifique claims de saúde, dose e contraindicações.
Sinal de reprovação neste cenário: falha quando a mensagem parece prescrição.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Tom de WhatsApp
Definição operacional: mantém conversa natural, direta e respeitosa.
Evidência que o Evaluator deve procurar: leia a mensagem como cliente em canal móvel.
Sinal de reprovação neste cenário: falha quando soa como contrato jurídico ou robô frio.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Brevity control
Definição operacional: mantém resposta curta o bastante para o canal.
Evidência que o Evaluator deve procurar: conte blocos de informação e remova redundância.
Sinal de reprovação neste cenário: falha quando uma resposta simples ocupa muitas telas.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Explicação da decisão
Definição operacional: mostra por que a recomendação foi feita.
Evidência que o Evaluator deve procurar: procure razão ligada ao objetivo do cliente.
Sinal de reprovação neste cenário: falha quando o cliente precisa adivinhar o motivo.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Próximo passo claro
Definição operacional: diz ao cliente o que pode fazer agora.
Evidência que o Evaluator deve procurar: verifique se há ação concreta sem pressão indevida.
Sinal de reprovação neste cenário: falha quando termina sem caminho de avanço.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Consentimento antes de cobrança
Definição operacional: não processa pagamento sem confirmação explícita.
Evidência que o Evaluator deve procurar: verifique status e mensagem de confirmação.
Sinal de reprovação neste cenário: falha quando o workflow pula aceite do cliente.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Validade de cupom
Definição operacional: confirma elegibilidade do desconto aplicado.
Evidência que o Evaluator deve procurar: compare cupom com policy e perfil do cliente.
Sinal de reprovação neste cenário: falha quando desconto indevido passa para checkout.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Não cumulatividade
Definição operacional: bloqueia combinação de promoções proibidas.
Evidência que o Evaluator deve procurar: confira stackability rules.
Sinal de reprovação neste cenário: falha quando duas promoções incompatíveis são combinadas.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Integridade de JSON
Definição operacional: garante que structured output é parseable e completo.
Evidência que o Evaluator deve procurar: valide schema, campos obrigatórios e tipos.
Sinal de reprovação neste cenário: falha quando downstream não consegue consumir o payload.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Idempotência operacional
Definição operacional: evita repetir cobrança, pedido ou mensagem sensível.
Evidência que o Evaluator deve procurar: verifique operation_id e status anterior.
Sinal de reprovação neste cenário: falha quando retry vira duplicidade.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Auditabilidade
Definição operacional: deixa evidência suficiente para debug futuro.
Evidência que o Evaluator deve procurar: procure source ids, reasons e checks.
Sinal de reprovação neste cenário: falha quando ninguém consegue explicar a decisão depois.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Separação entre fato e sugestão
Definição operacional: não apresenta opinião como dado de sistema.
Evidência que o Evaluator deve procurar: marque claims sem fonte.
Sinal de reprovação neste cenário: falha quando preferência comercial vira fato.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Controle de inventário
Definição operacional: não recomenda produto fora de estoque.
Evidência que o Evaluator deve procurar: compare inventory snapshot e local de entrega.
Sinal de reprovação neste cenário: falha quando o cliente escolhe algo indisponível.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Localidade de entrega
Definição operacional: considera região, frete e prazo no output.
Evidência que o Evaluator deve procurar: verifique CEP, cidade e shipping rules.
Sinal de reprovação neste cenário: falha quando prazo ou frete não vale para a região.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Privacidade
Definição operacional: não expõe dados pessoais desnecessários.
Evidência que o Evaluator deve procurar: procure telefone, endereço e documentos no output.
Sinal de reprovação neste cenário: falha quando dados sensíveis aparecem sem necessidade.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Escalonamento correto
Definição operacional: manda casos sensíveis para humano quando necessário.
Evidência que o Evaluator deve procurar: verifique risk_flags e requires_human_review.
Sinal de reprovação neste cenário: falha quando automação insiste em caso crítico.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Resolução de ambiguidade
Definição operacional: pede esclarecimento quando dados são insuficientes.
Evidência que o Evaluator deve procurar: procure pergunta objetiva em vez de suposição.
Sinal de reprovação neste cenário: falha quando KODA escolhe sem base.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Consistência com histórico
Definição operacional: não contradiz preferências, pedidos e promessas anteriores.
Evidência que o Evaluator deve procurar: compare output com state persistido.
Sinal de reprovação neste cenário: falha quando context amnesia muda a conversa.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Controle de hallucination
Definição operacional: não inventa produto, política, prazo ou benefício.
Evidência que o Evaluator deve procurar: compare afirmações com fontes recebidas.
Sinal de reprovação neste cenário: falha quando informação sem fonte vira resposta final.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Qualidade de feedback ao Generator
Definição operacional: quando reprova, explica correção específica.
Evidência que o Evaluator deve procurar: verifique se feedback aponta critério e evidência.
Sinal de reprovação neste cenário: falha quando retry recebe crítica genérica.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Custo de token
Definição operacional: evita texto ou campos extras que aumentam context window sem ganho.
Evidência que o Evaluator deve procurar: procure redundância e verbose output.
Sinal de reprovação neste cenário: falha quando cada avaliação polui conversas longas.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

Resumo do cenário: se muitas dimensions parecem críticas, divida a feature em rubrics menores.

### Cenário 7: Pedido com retry após falha de pagamento
Contexto: workflow precisa tentar novamente sem duplicar cobrança.
Foco da rubric: priorize idempotência, consentimento e trace.
Como usar: selecione as dimensions abaixo que realmente afetam a decisão final neste cenário.

#### Dimension: Aderência ao sprint contract
Definição operacional: verifica se o output cumpriu exatamente o acordo feito antes da execução.
Evidência que o Evaluator deve procurar: compare output com promised deliverables.
Sinal de reprovação neste cenário: falha quando o Generator entregou algo diferente do combinado.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Fidelidade ao catálogo
Definição operacional: confirma que produtos citados existem no catálogo recebido.
Evidência que o Evaluator deve procurar: busque product_id, nome, categoria e disponibilidade.
Sinal de reprovação neste cenário: falha quando o output inventa produto ou variante.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Precisão de preço
Definição operacional: confirma que todos os valores batem com price snapshot.
Evidência que o Evaluator deve procurar: calcule centavos, subtotal, desconto, frete e total.
Sinal de reprovação neste cenário: falha quando o cliente vê um valor diferente no checkout.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Compatibilidade com restrições
Definição operacional: garante que alergias, dieta, orçamento e preferências foram respeitados.
Evidência que o Evaluator deve procurar: procure restrições no state e compare com produto.
Sinal de reprovação neste cenário: falha quando uma preferência crítica é ignorada.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Segurança de saúde
Definição operacional: evita conselho médico, promessa clínica e sugestão arriscada.
Evidência que o Evaluator deve procurar: identifique claims de saúde, dose e contraindicações.
Sinal de reprovação neste cenário: falha quando a mensagem parece prescrição.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Tom de WhatsApp
Definição operacional: mantém conversa natural, direta e respeitosa.
Evidência que o Evaluator deve procurar: leia a mensagem como cliente em canal móvel.
Sinal de reprovação neste cenário: falha quando soa como contrato jurídico ou robô frio.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Brevity control
Definição operacional: mantém resposta curta o bastante para o canal.
Evidência que o Evaluator deve procurar: conte blocos de informação e remova redundância.
Sinal de reprovação neste cenário: falha quando uma resposta simples ocupa muitas telas.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Explicação da decisão
Definição operacional: mostra por que a recomendação foi feita.
Evidência que o Evaluator deve procurar: procure razão ligada ao objetivo do cliente.
Sinal de reprovação neste cenário: falha quando o cliente precisa adivinhar o motivo.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Próximo passo claro
Definição operacional: diz ao cliente o que pode fazer agora.
Evidência que o Evaluator deve procurar: verifique se há ação concreta sem pressão indevida.
Sinal de reprovação neste cenário: falha quando termina sem caminho de avanço.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Consentimento antes de cobrança
Definição operacional: não processa pagamento sem confirmação explícita.
Evidência que o Evaluator deve procurar: verifique status e mensagem de confirmação.
Sinal de reprovação neste cenário: falha quando o workflow pula aceite do cliente.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Validade de cupom
Definição operacional: confirma elegibilidade do desconto aplicado.
Evidência que o Evaluator deve procurar: compare cupom com policy e perfil do cliente.
Sinal de reprovação neste cenário: falha quando desconto indevido passa para checkout.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Não cumulatividade
Definição operacional: bloqueia combinação de promoções proibidas.
Evidência que o Evaluator deve procurar: confira stackability rules.
Sinal de reprovação neste cenário: falha quando duas promoções incompatíveis são combinadas.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Integridade de JSON
Definição operacional: garante que structured output é parseable e completo.
Evidência que o Evaluator deve procurar: valide schema, campos obrigatórios e tipos.
Sinal de reprovação neste cenário: falha quando downstream não consegue consumir o payload.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Idempotência operacional
Definição operacional: evita repetir cobrança, pedido ou mensagem sensível.
Evidência que o Evaluator deve procurar: verifique operation_id e status anterior.
Sinal de reprovação neste cenário: falha quando retry vira duplicidade.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Auditabilidade
Definição operacional: deixa evidência suficiente para debug futuro.
Evidência que o Evaluator deve procurar: procure source ids, reasons e checks.
Sinal de reprovação neste cenário: falha quando ninguém consegue explicar a decisão depois.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Separação entre fato e sugestão
Definição operacional: não apresenta opinião como dado de sistema.
Evidência que o Evaluator deve procurar: marque claims sem fonte.
Sinal de reprovação neste cenário: falha quando preferência comercial vira fato.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Controle de inventário
Definição operacional: não recomenda produto fora de estoque.
Evidência que o Evaluator deve procurar: compare inventory snapshot e local de entrega.
Sinal de reprovação neste cenário: falha quando o cliente escolhe algo indisponível.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Localidade de entrega
Definição operacional: considera região, frete e prazo no output.
Evidência que o Evaluator deve procurar: verifique CEP, cidade e shipping rules.
Sinal de reprovação neste cenário: falha quando prazo ou frete não vale para a região.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Privacidade
Definição operacional: não expõe dados pessoais desnecessários.
Evidência que o Evaluator deve procurar: procure telefone, endereço e documentos no output.
Sinal de reprovação neste cenário: falha quando dados sensíveis aparecem sem necessidade.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Escalonamento correto
Definição operacional: manda casos sensíveis para humano quando necessário.
Evidência que o Evaluator deve procurar: verifique risk_flags e requires_human_review.
Sinal de reprovação neste cenário: falha quando automação insiste em caso crítico.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Resolução de ambiguidade
Definição operacional: pede esclarecimento quando dados são insuficientes.
Evidência que o Evaluator deve procurar: procure pergunta objetiva em vez de suposição.
Sinal de reprovação neste cenário: falha quando KODA escolhe sem base.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Consistência com histórico
Definição operacional: não contradiz preferências, pedidos e promessas anteriores.
Evidência que o Evaluator deve procurar: compare output com state persistido.
Sinal de reprovação neste cenário: falha quando context amnesia muda a conversa.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Controle de hallucination
Definição operacional: não inventa produto, política, prazo ou benefício.
Evidência que o Evaluator deve procurar: compare afirmações com fontes recebidas.
Sinal de reprovação neste cenário: falha quando informação sem fonte vira resposta final.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Qualidade de feedback ao Generator
Definição operacional: quando reprova, explica correção específica.
Evidência que o Evaluator deve procurar: verifique se feedback aponta critério e evidência.
Sinal de reprovação neste cenário: falha quando retry recebe crítica genérica.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Custo de token
Definição operacional: evita texto ou campos extras que aumentam context window sem ganho.
Evidência que o Evaluator deve procurar: procure redundância e verbose output.
Sinal de reprovação neste cenário: falha quando cada avaliação polui conversas longas.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

Resumo do cenário: se muitas dimensions parecem críticas, divida a feature em rubrics menores.

### Cenário 8: Suporte para entrega atrasada
Contexto: cliente está frustrado e precisa de resposta prática.
Foco da rubric: priorize empathy, resolução e escalonamento.
Como usar: selecione as dimensions abaixo que realmente afetam a decisão final neste cenário.

#### Dimension: Aderência ao sprint contract
Definição operacional: verifica se o output cumpriu exatamente o acordo feito antes da execução.
Evidência que o Evaluator deve procurar: compare output com promised deliverables.
Sinal de reprovação neste cenário: falha quando o Generator entregou algo diferente do combinado.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Fidelidade ao catálogo
Definição operacional: confirma que produtos citados existem no catálogo recebido.
Evidência que o Evaluator deve procurar: busque product_id, nome, categoria e disponibilidade.
Sinal de reprovação neste cenário: falha quando o output inventa produto ou variante.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Precisão de preço
Definição operacional: confirma que todos os valores batem com price snapshot.
Evidência que o Evaluator deve procurar: calcule centavos, subtotal, desconto, frete e total.
Sinal de reprovação neste cenário: falha quando o cliente vê um valor diferente no checkout.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Compatibilidade com restrições
Definição operacional: garante que alergias, dieta, orçamento e preferências foram respeitados.
Evidência que o Evaluator deve procurar: procure restrições no state e compare com produto.
Sinal de reprovação neste cenário: falha quando uma preferência crítica é ignorada.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Segurança de saúde
Definição operacional: evita conselho médico, promessa clínica e sugestão arriscada.
Evidência que o Evaluator deve procurar: identifique claims de saúde, dose e contraindicações.
Sinal de reprovação neste cenário: falha quando a mensagem parece prescrição.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Tom de WhatsApp
Definição operacional: mantém conversa natural, direta e respeitosa.
Evidência que o Evaluator deve procurar: leia a mensagem como cliente em canal móvel.
Sinal de reprovação neste cenário: falha quando soa como contrato jurídico ou robô frio.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Brevity control
Definição operacional: mantém resposta curta o bastante para o canal.
Evidência que o Evaluator deve procurar: conte blocos de informação e remova redundância.
Sinal de reprovação neste cenário: falha quando uma resposta simples ocupa muitas telas.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Explicação da decisão
Definição operacional: mostra por que a recomendação foi feita.
Evidência que o Evaluator deve procurar: procure razão ligada ao objetivo do cliente.
Sinal de reprovação neste cenário: falha quando o cliente precisa adivinhar o motivo.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Próximo passo claro
Definição operacional: diz ao cliente o que pode fazer agora.
Evidência que o Evaluator deve procurar: verifique se há ação concreta sem pressão indevida.
Sinal de reprovação neste cenário: falha quando termina sem caminho de avanço.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Consentimento antes de cobrança
Definição operacional: não processa pagamento sem confirmação explícita.
Evidência que o Evaluator deve procurar: verifique status e mensagem de confirmação.
Sinal de reprovação neste cenário: falha quando o workflow pula aceite do cliente.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Validade de cupom
Definição operacional: confirma elegibilidade do desconto aplicado.
Evidência que o Evaluator deve procurar: compare cupom com policy e perfil do cliente.
Sinal de reprovação neste cenário: falha quando desconto indevido passa para checkout.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Não cumulatividade
Definição operacional: bloqueia combinação de promoções proibidas.
Evidência que o Evaluator deve procurar: confira stackability rules.
Sinal de reprovação neste cenário: falha quando duas promoções incompatíveis são combinadas.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Integridade de JSON
Definição operacional: garante que structured output é parseable e completo.
Evidência que o Evaluator deve procurar: valide schema, campos obrigatórios e tipos.
Sinal de reprovação neste cenário: falha quando downstream não consegue consumir o payload.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Idempotência operacional
Definição operacional: evita repetir cobrança, pedido ou mensagem sensível.
Evidência que o Evaluator deve procurar: verifique operation_id e status anterior.
Sinal de reprovação neste cenário: falha quando retry vira duplicidade.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Auditabilidade
Definição operacional: deixa evidência suficiente para debug futuro.
Evidência que o Evaluator deve procurar: procure source ids, reasons e checks.
Sinal de reprovação neste cenário: falha quando ninguém consegue explicar a decisão depois.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Separação entre fato e sugestão
Definição operacional: não apresenta opinião como dado de sistema.
Evidência que o Evaluator deve procurar: marque claims sem fonte.
Sinal de reprovação neste cenário: falha quando preferência comercial vira fato.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Controle de inventário
Definição operacional: não recomenda produto fora de estoque.
Evidência que o Evaluator deve procurar: compare inventory snapshot e local de entrega.
Sinal de reprovação neste cenário: falha quando o cliente escolhe algo indisponível.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Localidade de entrega
Definição operacional: considera região, frete e prazo no output.
Evidência que o Evaluator deve procurar: verifique CEP, cidade e shipping rules.
Sinal de reprovação neste cenário: falha quando prazo ou frete não vale para a região.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Privacidade
Definição operacional: não expõe dados pessoais desnecessários.
Evidência que o Evaluator deve procurar: procure telefone, endereço e documentos no output.
Sinal de reprovação neste cenário: falha quando dados sensíveis aparecem sem necessidade.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Escalonamento correto
Definição operacional: manda casos sensíveis para humano quando necessário.
Evidência que o Evaluator deve procurar: verifique risk_flags e requires_human_review.
Sinal de reprovação neste cenário: falha quando automação insiste em caso crítico.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Resolução de ambiguidade
Definição operacional: pede esclarecimento quando dados são insuficientes.
Evidência que o Evaluator deve procurar: procure pergunta objetiva em vez de suposição.
Sinal de reprovação neste cenário: falha quando KODA escolhe sem base.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Consistência com histórico
Definição operacional: não contradiz preferências, pedidos e promessas anteriores.
Evidência que o Evaluator deve procurar: compare output com state persistido.
Sinal de reprovação neste cenário: falha quando context amnesia muda a conversa.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Controle de hallucination
Definição operacional: não inventa produto, política, prazo ou benefício.
Evidência que o Evaluator deve procurar: compare afirmações com fontes recebidas.
Sinal de reprovação neste cenário: falha quando informação sem fonte vira resposta final.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Qualidade de feedback ao Generator
Definição operacional: quando reprova, explica correção específica.
Evidência que o Evaluator deve procurar: verifique se feedback aponta critério e evidência.
Sinal de reprovação neste cenário: falha quando retry recebe crítica genérica.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Custo de token
Definição operacional: evita texto ou campos extras que aumentam context window sem ganho.
Evidência que o Evaluator deve procurar: procure redundância e verbose output.
Sinal de reprovação neste cenário: falha quando cada avaliação polui conversas longas.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

Resumo do cenário: se muitas dimensions parecem críticas, divida a feature em rubrics menores.

### Cenário 9: Suporte para troca de produto
Contexto: cliente recebeu produto incorreto ou mudou de ideia.
Foco da rubric: priorize política correta, privacidade e próximo passo claro.
Como usar: selecione as dimensions abaixo que realmente afetam a decisão final neste cenário.

#### Dimension: Aderência ao sprint contract
Definição operacional: verifica se o output cumpriu exatamente o acordo feito antes da execução.
Evidência que o Evaluator deve procurar: compare output com promised deliverables.
Sinal de reprovação neste cenário: falha quando o Generator entregou algo diferente do combinado.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Fidelidade ao catálogo
Definição operacional: confirma que produtos citados existem no catálogo recebido.
Evidência que o Evaluator deve procurar: busque product_id, nome, categoria e disponibilidade.
Sinal de reprovação neste cenário: falha quando o output inventa produto ou variante.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Precisão de preço
Definição operacional: confirma que todos os valores batem com price snapshot.
Evidência que o Evaluator deve procurar: calcule centavos, subtotal, desconto, frete e total.
Sinal de reprovação neste cenário: falha quando o cliente vê um valor diferente no checkout.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Compatibilidade com restrições
Definição operacional: garante que alergias, dieta, orçamento e preferências foram respeitados.
Evidência que o Evaluator deve procurar: procure restrições no state e compare com produto.
Sinal de reprovação neste cenário: falha quando uma preferência crítica é ignorada.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Segurança de saúde
Definição operacional: evita conselho médico, promessa clínica e sugestão arriscada.
Evidência que o Evaluator deve procurar: identifique claims de saúde, dose e contraindicações.
Sinal de reprovação neste cenário: falha quando a mensagem parece prescrição.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Tom de WhatsApp
Definição operacional: mantém conversa natural, direta e respeitosa.
Evidência que o Evaluator deve procurar: leia a mensagem como cliente em canal móvel.
Sinal de reprovação neste cenário: falha quando soa como contrato jurídico ou robô frio.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Brevity control
Definição operacional: mantém resposta curta o bastante para o canal.
Evidência que o Evaluator deve procurar: conte blocos de informação e remova redundância.
Sinal de reprovação neste cenário: falha quando uma resposta simples ocupa muitas telas.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Explicação da decisão
Definição operacional: mostra por que a recomendação foi feita.
Evidência que o Evaluator deve procurar: procure razão ligada ao objetivo do cliente.
Sinal de reprovação neste cenário: falha quando o cliente precisa adivinhar o motivo.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Próximo passo claro
Definição operacional: diz ao cliente o que pode fazer agora.
Evidência que o Evaluator deve procurar: verifique se há ação concreta sem pressão indevida.
Sinal de reprovação neste cenário: falha quando termina sem caminho de avanço.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Consentimento antes de cobrança
Definição operacional: não processa pagamento sem confirmação explícita.
Evidência que o Evaluator deve procurar: verifique status e mensagem de confirmação.
Sinal de reprovação neste cenário: falha quando o workflow pula aceite do cliente.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Validade de cupom
Definição operacional: confirma elegibilidade do desconto aplicado.
Evidência que o Evaluator deve procurar: compare cupom com policy e perfil do cliente.
Sinal de reprovação neste cenário: falha quando desconto indevido passa para checkout.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Não cumulatividade
Definição operacional: bloqueia combinação de promoções proibidas.
Evidência que o Evaluator deve procurar: confira stackability rules.
Sinal de reprovação neste cenário: falha quando duas promoções incompatíveis são combinadas.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Integridade de JSON
Definição operacional: garante que structured output é parseable e completo.
Evidência que o Evaluator deve procurar: valide schema, campos obrigatórios e tipos.
Sinal de reprovação neste cenário: falha quando downstream não consegue consumir o payload.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Idempotência operacional
Definição operacional: evita repetir cobrança, pedido ou mensagem sensível.
Evidência que o Evaluator deve procurar: verifique operation_id e status anterior.
Sinal de reprovação neste cenário: falha quando retry vira duplicidade.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Auditabilidade
Definição operacional: deixa evidência suficiente para debug futuro.
Evidência que o Evaluator deve procurar: procure source ids, reasons e checks.
Sinal de reprovação neste cenário: falha quando ninguém consegue explicar a decisão depois.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Separação entre fato e sugestão
Definição operacional: não apresenta opinião como dado de sistema.
Evidência que o Evaluator deve procurar: marque claims sem fonte.
Sinal de reprovação neste cenário: falha quando preferência comercial vira fato.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Controle de inventário
Definição operacional: não recomenda produto fora de estoque.
Evidência que o Evaluator deve procurar: compare inventory snapshot e local de entrega.
Sinal de reprovação neste cenário: falha quando o cliente escolhe algo indisponível.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Localidade de entrega
Definição operacional: considera região, frete e prazo no output.
Evidência que o Evaluator deve procurar: verifique CEP, cidade e shipping rules.
Sinal de reprovação neste cenário: falha quando prazo ou frete não vale para a região.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Privacidade
Definição operacional: não expõe dados pessoais desnecessários.
Evidência que o Evaluator deve procurar: procure telefone, endereço e documentos no output.
Sinal de reprovação neste cenário: falha quando dados sensíveis aparecem sem necessidade.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Escalonamento correto
Definição operacional: manda casos sensíveis para humano quando necessário.
Evidência que o Evaluator deve procurar: verifique risk_flags e requires_human_review.
Sinal de reprovação neste cenário: falha quando automação insiste em caso crítico.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Resolução de ambiguidade
Definição operacional: pede esclarecimento quando dados são insuficientes.
Evidência que o Evaluator deve procurar: procure pergunta objetiva em vez de suposição.
Sinal de reprovação neste cenário: falha quando KODA escolhe sem base.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Consistência com histórico
Definição operacional: não contradiz preferências, pedidos e promessas anteriores.
Evidência que o Evaluator deve procurar: compare output com state persistido.
Sinal de reprovação neste cenário: falha quando context amnesia muda a conversa.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Controle de hallucination
Definição operacional: não inventa produto, política, prazo ou benefício.
Evidência que o Evaluator deve procurar: compare afirmações com fontes recebidas.
Sinal de reprovação neste cenário: falha quando informação sem fonte vira resposta final.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Qualidade de feedback ao Generator
Definição operacional: quando reprova, explica correção específica.
Evidência que o Evaluator deve procurar: verifique se feedback aponta critério e evidência.
Sinal de reprovação neste cenário: falha quando retry recebe crítica genérica.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Custo de token
Definição operacional: evita texto ou campos extras que aumentam context window sem ganho.
Evidência que o Evaluator deve procurar: procure redundância e verbose output.
Sinal de reprovação neste cenário: falha quando cada avaliação polui conversas longas.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

Resumo do cenário: se muitas dimensions parecem críticas, divida a feature em rubrics menores.

### Cenário 10: Resumo de conversa longa
Contexto: KODA precisa compactar contexto sem perder fatos críticos.
Foco da rubric: priorize consistência, restrições e auditabilidade.
Como usar: selecione as dimensions abaixo que realmente afetam a decisão final neste cenário.

#### Dimension: Aderência ao sprint contract
Definição operacional: verifica se o output cumpriu exatamente o acordo feito antes da execução.
Evidência que o Evaluator deve procurar: compare output com promised deliverables.
Sinal de reprovação neste cenário: falha quando o Generator entregou algo diferente do combinado.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Fidelidade ao catálogo
Definição operacional: confirma que produtos citados existem no catálogo recebido.
Evidência que o Evaluator deve procurar: busque product_id, nome, categoria e disponibilidade.
Sinal de reprovação neste cenário: falha quando o output inventa produto ou variante.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Precisão de preço
Definição operacional: confirma que todos os valores batem com price snapshot.
Evidência que o Evaluator deve procurar: calcule centavos, subtotal, desconto, frete e total.
Sinal de reprovação neste cenário: falha quando o cliente vê um valor diferente no checkout.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Compatibilidade com restrições
Definição operacional: garante que alergias, dieta, orçamento e preferências foram respeitados.
Evidência que o Evaluator deve procurar: procure restrições no state e compare com produto.
Sinal de reprovação neste cenário: falha quando uma preferência crítica é ignorada.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Segurança de saúde
Definição operacional: evita conselho médico, promessa clínica e sugestão arriscada.
Evidência que o Evaluator deve procurar: identifique claims de saúde, dose e contraindicações.
Sinal de reprovação neste cenário: falha quando a mensagem parece prescrição.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Tom de WhatsApp
Definição operacional: mantém conversa natural, direta e respeitosa.
Evidência que o Evaluator deve procurar: leia a mensagem como cliente em canal móvel.
Sinal de reprovação neste cenário: falha quando soa como contrato jurídico ou robô frio.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Brevity control
Definição operacional: mantém resposta curta o bastante para o canal.
Evidência que o Evaluator deve procurar: conte blocos de informação e remova redundância.
Sinal de reprovação neste cenário: falha quando uma resposta simples ocupa muitas telas.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Explicação da decisão
Definição operacional: mostra por que a recomendação foi feita.
Evidência que o Evaluator deve procurar: procure razão ligada ao objetivo do cliente.
Sinal de reprovação neste cenário: falha quando o cliente precisa adivinhar o motivo.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Próximo passo claro
Definição operacional: diz ao cliente o que pode fazer agora.
Evidência que o Evaluator deve procurar: verifique se há ação concreta sem pressão indevida.
Sinal de reprovação neste cenário: falha quando termina sem caminho de avanço.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Consentimento antes de cobrança
Definição operacional: não processa pagamento sem confirmação explícita.
Evidência que o Evaluator deve procurar: verifique status e mensagem de confirmação.
Sinal de reprovação neste cenário: falha quando o workflow pula aceite do cliente.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Validade de cupom
Definição operacional: confirma elegibilidade do desconto aplicado.
Evidência que o Evaluator deve procurar: compare cupom com policy e perfil do cliente.
Sinal de reprovação neste cenário: falha quando desconto indevido passa para checkout.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Não cumulatividade
Definição operacional: bloqueia combinação de promoções proibidas.
Evidência que o Evaluator deve procurar: confira stackability rules.
Sinal de reprovação neste cenário: falha quando duas promoções incompatíveis são combinadas.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Integridade de JSON
Definição operacional: garante que structured output é parseable e completo.
Evidência que o Evaluator deve procurar: valide schema, campos obrigatórios e tipos.
Sinal de reprovação neste cenário: falha quando downstream não consegue consumir o payload.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Idempotência operacional
Definição operacional: evita repetir cobrança, pedido ou mensagem sensível.
Evidência que o Evaluator deve procurar: verifique operation_id e status anterior.
Sinal de reprovação neste cenário: falha quando retry vira duplicidade.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Auditabilidade
Definição operacional: deixa evidência suficiente para debug futuro.
Evidência que o Evaluator deve procurar: procure source ids, reasons e checks.
Sinal de reprovação neste cenário: falha quando ninguém consegue explicar a decisão depois.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Separação entre fato e sugestão
Definição operacional: não apresenta opinião como dado de sistema.
Evidência que o Evaluator deve procurar: marque claims sem fonte.
Sinal de reprovação neste cenário: falha quando preferência comercial vira fato.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Controle de inventário
Definição operacional: não recomenda produto fora de estoque.
Evidência que o Evaluator deve procurar: compare inventory snapshot e local de entrega.
Sinal de reprovação neste cenário: falha quando o cliente escolhe algo indisponível.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Localidade de entrega
Definição operacional: considera região, frete e prazo no output.
Evidência que o Evaluator deve procurar: verifique CEP, cidade e shipping rules.
Sinal de reprovação neste cenário: falha quando prazo ou frete não vale para a região.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Privacidade
Definição operacional: não expõe dados pessoais desnecessários.
Evidência que o Evaluator deve procurar: procure telefone, endereço e documentos no output.
Sinal de reprovação neste cenário: falha quando dados sensíveis aparecem sem necessidade.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Escalonamento correto
Definição operacional: manda casos sensíveis para humano quando necessário.
Evidência que o Evaluator deve procurar: verifique risk_flags e requires_human_review.
Sinal de reprovação neste cenário: falha quando automação insiste em caso crítico.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Resolução de ambiguidade
Definição operacional: pede esclarecimento quando dados são insuficientes.
Evidência que o Evaluator deve procurar: procure pergunta objetiva em vez de suposição.
Sinal de reprovação neste cenário: falha quando KODA escolhe sem base.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Consistência com histórico
Definição operacional: não contradiz preferências, pedidos e promessas anteriores.
Evidência que o Evaluator deve procurar: compare output com state persistido.
Sinal de reprovação neste cenário: falha quando context amnesia muda a conversa.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Controle de hallucination
Definição operacional: não inventa produto, política, prazo ou benefício.
Evidência que o Evaluator deve procurar: compare afirmações com fontes recebidas.
Sinal de reprovação neste cenário: falha quando informação sem fonte vira resposta final.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Qualidade de feedback ao Generator
Definição operacional: quando reprova, explica correção específica.
Evidência que o Evaluator deve procurar: verifique se feedback aponta critério e evidência.
Sinal de reprovação neste cenário: falha quando retry recebe crítica genérica.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Custo de token
Definição operacional: evita texto ou campos extras que aumentam context window sem ganho.
Evidência que o Evaluator deve procurar: procure redundância e verbose output.
Sinal de reprovação neste cenário: falha quando cada avaliação polui conversas longas.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

Resumo do cenário: se muitas dimensions parecem críticas, divida a feature em rubrics menores.

### Cenário 11: Handoff para humano
Contexto: automação decide que precisa escalar atendimento.
Foco da rubric: priorize risk_flags, resumo fiel e dados mínimos necessários.
Como usar: selecione as dimensions abaixo que realmente afetam a decisão final neste cenário.

#### Dimension: Aderência ao sprint contract
Definição operacional: verifica se o output cumpriu exatamente o acordo feito antes da execução.
Evidência que o Evaluator deve procurar: compare output com promised deliverables.
Sinal de reprovação neste cenário: falha quando o Generator entregou algo diferente do combinado.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Fidelidade ao catálogo
Definição operacional: confirma que produtos citados existem no catálogo recebido.
Evidência que o Evaluator deve procurar: busque product_id, nome, categoria e disponibilidade.
Sinal de reprovação neste cenário: falha quando o output inventa produto ou variante.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Precisão de preço
Definição operacional: confirma que todos os valores batem com price snapshot.
Evidência que o Evaluator deve procurar: calcule centavos, subtotal, desconto, frete e total.
Sinal de reprovação neste cenário: falha quando o cliente vê um valor diferente no checkout.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Compatibilidade com restrições
Definição operacional: garante que alergias, dieta, orçamento e preferências foram respeitados.
Evidência que o Evaluator deve procurar: procure restrições no state e compare com produto.
Sinal de reprovação neste cenário: falha quando uma preferência crítica é ignorada.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Segurança de saúde
Definição operacional: evita conselho médico, promessa clínica e sugestão arriscada.
Evidência que o Evaluator deve procurar: identifique claims de saúde, dose e contraindicações.
Sinal de reprovação neste cenário: falha quando a mensagem parece prescrição.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Tom de WhatsApp
Definição operacional: mantém conversa natural, direta e respeitosa.
Evidência que o Evaluator deve procurar: leia a mensagem como cliente em canal móvel.
Sinal de reprovação neste cenário: falha quando soa como contrato jurídico ou robô frio.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Brevity control
Definição operacional: mantém resposta curta o bastante para o canal.
Evidência que o Evaluator deve procurar: conte blocos de informação e remova redundância.
Sinal de reprovação neste cenário: falha quando uma resposta simples ocupa muitas telas.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Explicação da decisão
Definição operacional: mostra por que a recomendação foi feita.
Evidência que o Evaluator deve procurar: procure razão ligada ao objetivo do cliente.
Sinal de reprovação neste cenário: falha quando o cliente precisa adivinhar o motivo.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Próximo passo claro
Definição operacional: diz ao cliente o que pode fazer agora.
Evidência que o Evaluator deve procurar: verifique se há ação concreta sem pressão indevida.
Sinal de reprovação neste cenário: falha quando termina sem caminho de avanço.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Consentimento antes de cobrança
Definição operacional: não processa pagamento sem confirmação explícita.
Evidência que o Evaluator deve procurar: verifique status e mensagem de confirmação.
Sinal de reprovação neste cenário: falha quando o workflow pula aceite do cliente.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Validade de cupom
Definição operacional: confirma elegibilidade do desconto aplicado.
Evidência que o Evaluator deve procurar: compare cupom com policy e perfil do cliente.
Sinal de reprovação neste cenário: falha quando desconto indevido passa para checkout.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Não cumulatividade
Definição operacional: bloqueia combinação de promoções proibidas.
Evidência que o Evaluator deve procurar: confira stackability rules.
Sinal de reprovação neste cenário: falha quando duas promoções incompatíveis são combinadas.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Integridade de JSON
Definição operacional: garante que structured output é parseable e completo.
Evidência que o Evaluator deve procurar: valide schema, campos obrigatórios e tipos.
Sinal de reprovação neste cenário: falha quando downstream não consegue consumir o payload.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Idempotência operacional
Definição operacional: evita repetir cobrança, pedido ou mensagem sensível.
Evidência que o Evaluator deve procurar: verifique operation_id e status anterior.
Sinal de reprovação neste cenário: falha quando retry vira duplicidade.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Auditabilidade
Definição operacional: deixa evidência suficiente para debug futuro.
Evidência que o Evaluator deve procurar: procure source ids, reasons e checks.
Sinal de reprovação neste cenário: falha quando ninguém consegue explicar a decisão depois.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Separação entre fato e sugestão
Definição operacional: não apresenta opinião como dado de sistema.
Evidência que o Evaluator deve procurar: marque claims sem fonte.
Sinal de reprovação neste cenário: falha quando preferência comercial vira fato.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Controle de inventário
Definição operacional: não recomenda produto fora de estoque.
Evidência que o Evaluator deve procurar: compare inventory snapshot e local de entrega.
Sinal de reprovação neste cenário: falha quando o cliente escolhe algo indisponível.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Localidade de entrega
Definição operacional: considera região, frete e prazo no output.
Evidência que o Evaluator deve procurar: verifique CEP, cidade e shipping rules.
Sinal de reprovação neste cenário: falha quando prazo ou frete não vale para a região.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Privacidade
Definição operacional: não expõe dados pessoais desnecessários.
Evidência que o Evaluator deve procurar: procure telefone, endereço e documentos no output.
Sinal de reprovação neste cenário: falha quando dados sensíveis aparecem sem necessidade.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Escalonamento correto
Definição operacional: manda casos sensíveis para humano quando necessário.
Evidência que o Evaluator deve procurar: verifique risk_flags e requires_human_review.
Sinal de reprovação neste cenário: falha quando automação insiste em caso crítico.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Resolução de ambiguidade
Definição operacional: pede esclarecimento quando dados são insuficientes.
Evidência que o Evaluator deve procurar: procure pergunta objetiva em vez de suposição.
Sinal de reprovação neste cenário: falha quando KODA escolhe sem base.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Consistência com histórico
Definição operacional: não contradiz preferências, pedidos e promessas anteriores.
Evidência que o Evaluator deve procurar: compare output com state persistido.
Sinal de reprovação neste cenário: falha quando context amnesia muda a conversa.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Controle de hallucination
Definição operacional: não inventa produto, política, prazo ou benefício.
Evidência que o Evaluator deve procurar: compare afirmações com fontes recebidas.
Sinal de reprovação neste cenário: falha quando informação sem fonte vira resposta final.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Qualidade de feedback ao Generator
Definição operacional: quando reprova, explica correção específica.
Evidência que o Evaluator deve procurar: verifique se feedback aponta critério e evidência.
Sinal de reprovação neste cenário: falha quando retry recebe crítica genérica.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Custo de token
Definição operacional: evita texto ou campos extras que aumentam context window sem ganho.
Evidência que o Evaluator deve procurar: procure redundância e verbose output.
Sinal de reprovação neste cenário: falha quando cada avaliação polui conversas longas.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

Resumo do cenário: se muitas dimensions parecem críticas, divida a feature em rubrics menores.

### Cenário 12: Validação de endereço
Contexto: cliente informa CEP e complemento em mensagens separadas.
Foco da rubric: priorize completude, privacidade e localidade de entrega.
Como usar: selecione as dimensions abaixo que realmente afetam a decisão final neste cenário.

#### Dimension: Aderência ao sprint contract
Definição operacional: verifica se o output cumpriu exatamente o acordo feito antes da execução.
Evidência que o Evaluator deve procurar: compare output com promised deliverables.
Sinal de reprovação neste cenário: falha quando o Generator entregou algo diferente do combinado.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Fidelidade ao catálogo
Definição operacional: confirma que produtos citados existem no catálogo recebido.
Evidência que o Evaluator deve procurar: busque product_id, nome, categoria e disponibilidade.
Sinal de reprovação neste cenário: falha quando o output inventa produto ou variante.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Precisão de preço
Definição operacional: confirma que todos os valores batem com price snapshot.
Evidência que o Evaluator deve procurar: calcule centavos, subtotal, desconto, frete e total.
Sinal de reprovação neste cenário: falha quando o cliente vê um valor diferente no checkout.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Compatibilidade com restrições
Definição operacional: garante que alergias, dieta, orçamento e preferências foram respeitados.
Evidência que o Evaluator deve procurar: procure restrições no state e compare com produto.
Sinal de reprovação neste cenário: falha quando uma preferência crítica é ignorada.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Segurança de saúde
Definição operacional: evita conselho médico, promessa clínica e sugestão arriscada.
Evidência que o Evaluator deve procurar: identifique claims de saúde, dose e contraindicações.
Sinal de reprovação neste cenário: falha quando a mensagem parece prescrição.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Tom de WhatsApp
Definição operacional: mantém conversa natural, direta e respeitosa.
Evidência que o Evaluator deve procurar: leia a mensagem como cliente em canal móvel.
Sinal de reprovação neste cenário: falha quando soa como contrato jurídico ou robô frio.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Brevity control
Definição operacional: mantém resposta curta o bastante para o canal.
Evidência que o Evaluator deve procurar: conte blocos de informação e remova redundância.
Sinal de reprovação neste cenário: falha quando uma resposta simples ocupa muitas telas.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Explicação da decisão
Definição operacional: mostra por que a recomendação foi feita.
Evidência que o Evaluator deve procurar: procure razão ligada ao objetivo do cliente.
Sinal de reprovação neste cenário: falha quando o cliente precisa adivinhar o motivo.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Próximo passo claro
Definição operacional: diz ao cliente o que pode fazer agora.
Evidência que o Evaluator deve procurar: verifique se há ação concreta sem pressão indevida.
Sinal de reprovação neste cenário: falha quando termina sem caminho de avanço.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Consentimento antes de cobrança
Definição operacional: não processa pagamento sem confirmação explícita.
Evidência que o Evaluator deve procurar: verifique status e mensagem de confirmação.
Sinal de reprovação neste cenário: falha quando o workflow pula aceite do cliente.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Validade de cupom
Definição operacional: confirma elegibilidade do desconto aplicado.
Evidência que o Evaluator deve procurar: compare cupom com policy e perfil do cliente.
Sinal de reprovação neste cenário: falha quando desconto indevido passa para checkout.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Não cumulatividade
Definição operacional: bloqueia combinação de promoções proibidas.
Evidência que o Evaluator deve procurar: confira stackability rules.
Sinal de reprovação neste cenário: falha quando duas promoções incompatíveis são combinadas.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Integridade de JSON
Definição operacional: garante que structured output é parseable e completo.
Evidência que o Evaluator deve procurar: valide schema, campos obrigatórios e tipos.
Sinal de reprovação neste cenário: falha quando downstream não consegue consumir o payload.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Idempotência operacional
Definição operacional: evita repetir cobrança, pedido ou mensagem sensível.
Evidência que o Evaluator deve procurar: verifique operation_id e status anterior.
Sinal de reprovação neste cenário: falha quando retry vira duplicidade.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Auditabilidade
Definição operacional: deixa evidência suficiente para debug futuro.
Evidência que o Evaluator deve procurar: procure source ids, reasons e checks.
Sinal de reprovação neste cenário: falha quando ninguém consegue explicar a decisão depois.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Separação entre fato e sugestão
Definição operacional: não apresenta opinião como dado de sistema.
Evidência que o Evaluator deve procurar: marque claims sem fonte.
Sinal de reprovação neste cenário: falha quando preferência comercial vira fato.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Controle de inventário
Definição operacional: não recomenda produto fora de estoque.
Evidência que o Evaluator deve procurar: compare inventory snapshot e local de entrega.
Sinal de reprovação neste cenário: falha quando o cliente escolhe algo indisponível.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Localidade de entrega
Definição operacional: considera região, frete e prazo no output.
Evidência que o Evaluator deve procurar: verifique CEP, cidade e shipping rules.
Sinal de reprovação neste cenário: falha quando prazo ou frete não vale para a região.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Privacidade
Definição operacional: não expõe dados pessoais desnecessários.
Evidência que o Evaluator deve procurar: procure telefone, endereço e documentos no output.
Sinal de reprovação neste cenário: falha quando dados sensíveis aparecem sem necessidade.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Escalonamento correto
Definição operacional: manda casos sensíveis para humano quando necessário.
Evidência que o Evaluator deve procurar: verifique risk_flags e requires_human_review.
Sinal de reprovação neste cenário: falha quando automação insiste em caso crítico.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Resolução de ambiguidade
Definição operacional: pede esclarecimento quando dados são insuficientes.
Evidência que o Evaluator deve procurar: procure pergunta objetiva em vez de suposição.
Sinal de reprovação neste cenário: falha quando KODA escolhe sem base.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Consistência com histórico
Definição operacional: não contradiz preferências, pedidos e promessas anteriores.
Evidência que o Evaluator deve procurar: compare output com state persistido.
Sinal de reprovação neste cenário: falha quando context amnesia muda a conversa.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Controle de hallucination
Definição operacional: não inventa produto, política, prazo ou benefício.
Evidência que o Evaluator deve procurar: compare afirmações com fontes recebidas.
Sinal de reprovação neste cenário: falha quando informação sem fonte vira resposta final.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Qualidade de feedback ao Generator
Definição operacional: quando reprova, explica correção específica.
Evidência que o Evaluator deve procurar: verifique se feedback aponta critério e evidência.
Sinal de reprovação neste cenário: falha quando retry recebe crítica genérica.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Custo de token
Definição operacional: evita texto ou campos extras que aumentam context window sem ganho.
Evidência que o Evaluator deve procurar: procure redundância e verbose output.
Sinal de reprovação neste cenário: falha quando cada avaliação polui conversas longas.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

Resumo do cenário: se muitas dimensions parecem críticas, divida a feature em rubrics menores.

### Cenário 13: Ranking interno de produtos
Contexto: Generator produz lista ordenada para Evaluator escolher.
Foco da rubric: priorize critério de ranking, catálogo e bias comercial.
Como usar: selecione as dimensions abaixo que realmente afetam a decisão final neste cenário.

#### Dimension: Aderência ao sprint contract
Definição operacional: verifica se o output cumpriu exatamente o acordo feito antes da execução.
Evidência que o Evaluator deve procurar: compare output com promised deliverables.
Sinal de reprovação neste cenário: falha quando o Generator entregou algo diferente do combinado.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Fidelidade ao catálogo
Definição operacional: confirma que produtos citados existem no catálogo recebido.
Evidência que o Evaluator deve procurar: busque product_id, nome, categoria e disponibilidade.
Sinal de reprovação neste cenário: falha quando o output inventa produto ou variante.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Precisão de preço
Definição operacional: confirma que todos os valores batem com price snapshot.
Evidência que o Evaluator deve procurar: calcule centavos, subtotal, desconto, frete e total.
Sinal de reprovação neste cenário: falha quando o cliente vê um valor diferente no checkout.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Compatibilidade com restrições
Definição operacional: garante que alergias, dieta, orçamento e preferências foram respeitados.
Evidência que o Evaluator deve procurar: procure restrições no state e compare com produto.
Sinal de reprovação neste cenário: falha quando uma preferência crítica é ignorada.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Segurança de saúde
Definição operacional: evita conselho médico, promessa clínica e sugestão arriscada.
Evidência que o Evaluator deve procurar: identifique claims de saúde, dose e contraindicações.
Sinal de reprovação neste cenário: falha quando a mensagem parece prescrição.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Tom de WhatsApp
Definição operacional: mantém conversa natural, direta e respeitosa.
Evidência que o Evaluator deve procurar: leia a mensagem como cliente em canal móvel.
Sinal de reprovação neste cenário: falha quando soa como contrato jurídico ou robô frio.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Brevity control
Definição operacional: mantém resposta curta o bastante para o canal.
Evidência que o Evaluator deve procurar: conte blocos de informação e remova redundância.
Sinal de reprovação neste cenário: falha quando uma resposta simples ocupa muitas telas.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Explicação da decisão
Definição operacional: mostra por que a recomendação foi feita.
Evidência que o Evaluator deve procurar: procure razão ligada ao objetivo do cliente.
Sinal de reprovação neste cenário: falha quando o cliente precisa adivinhar o motivo.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Próximo passo claro
Definição operacional: diz ao cliente o que pode fazer agora.
Evidência que o Evaluator deve procurar: verifique se há ação concreta sem pressão indevida.
Sinal de reprovação neste cenário: falha quando termina sem caminho de avanço.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Consentimento antes de cobrança
Definição operacional: não processa pagamento sem confirmação explícita.
Evidência que o Evaluator deve procurar: verifique status e mensagem de confirmação.
Sinal de reprovação neste cenário: falha quando o workflow pula aceite do cliente.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Validade de cupom
Definição operacional: confirma elegibilidade do desconto aplicado.
Evidência que o Evaluator deve procurar: compare cupom com policy e perfil do cliente.
Sinal de reprovação neste cenário: falha quando desconto indevido passa para checkout.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Não cumulatividade
Definição operacional: bloqueia combinação de promoções proibidas.
Evidência que o Evaluator deve procurar: confira stackability rules.
Sinal de reprovação neste cenário: falha quando duas promoções incompatíveis são combinadas.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Integridade de JSON
Definição operacional: garante que structured output é parseable e completo.
Evidência que o Evaluator deve procurar: valide schema, campos obrigatórios e tipos.
Sinal de reprovação neste cenário: falha quando downstream não consegue consumir o payload.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Idempotência operacional
Definição operacional: evita repetir cobrança, pedido ou mensagem sensível.
Evidência que o Evaluator deve procurar: verifique operation_id e status anterior.
Sinal de reprovação neste cenário: falha quando retry vira duplicidade.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Auditabilidade
Definição operacional: deixa evidência suficiente para debug futuro.
Evidência que o Evaluator deve procurar: procure source ids, reasons e checks.
Sinal de reprovação neste cenário: falha quando ninguém consegue explicar a decisão depois.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Separação entre fato e sugestão
Definição operacional: não apresenta opinião como dado de sistema.
Evidência que o Evaluator deve procurar: marque claims sem fonte.
Sinal de reprovação neste cenário: falha quando preferência comercial vira fato.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Controle de inventário
Definição operacional: não recomenda produto fora de estoque.
Evidência que o Evaluator deve procurar: compare inventory snapshot e local de entrega.
Sinal de reprovação neste cenário: falha quando o cliente escolhe algo indisponível.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Localidade de entrega
Definição operacional: considera região, frete e prazo no output.
Evidência que o Evaluator deve procurar: verifique CEP, cidade e shipping rules.
Sinal de reprovação neste cenário: falha quando prazo ou frete não vale para a região.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Privacidade
Definição operacional: não expõe dados pessoais desnecessários.
Evidência que o Evaluator deve procurar: procure telefone, endereço e documentos no output.
Sinal de reprovação neste cenário: falha quando dados sensíveis aparecem sem necessidade.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Escalonamento correto
Definição operacional: manda casos sensíveis para humano quando necessário.
Evidência que o Evaluator deve procurar: verifique risk_flags e requires_human_review.
Sinal de reprovação neste cenário: falha quando automação insiste em caso crítico.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Resolução de ambiguidade
Definição operacional: pede esclarecimento quando dados são insuficientes.
Evidência que o Evaluator deve procurar: procure pergunta objetiva em vez de suposição.
Sinal de reprovação neste cenário: falha quando KODA escolhe sem base.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Consistência com histórico
Definição operacional: não contradiz preferências, pedidos e promessas anteriores.
Evidência que o Evaluator deve procurar: compare output com state persistido.
Sinal de reprovação neste cenário: falha quando context amnesia muda a conversa.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Controle de hallucination
Definição operacional: não inventa produto, política, prazo ou benefício.
Evidência que o Evaluator deve procurar: compare afirmações com fontes recebidas.
Sinal de reprovação neste cenário: falha quando informação sem fonte vira resposta final.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Qualidade de feedback ao Generator
Definição operacional: quando reprova, explica correção específica.
Evidência que o Evaluator deve procurar: verifique se feedback aponta critério e evidência.
Sinal de reprovação neste cenário: falha quando retry recebe crítica genérica.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Custo de token
Definição operacional: evita texto ou campos extras que aumentam context window sem ganho.
Evidência que o Evaluator deve procurar: procure redundância e verbose output.
Sinal de reprovação neste cenário: falha quando cada avaliação polui conversas longas.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

Resumo do cenário: se muitas dimensions parecem críticas, divida a feature em rubrics menores.

### Cenário 14: Mensagem de recuperação após erro
Contexto: KODA reconhece falha e precisa reconstruir confiança.
Foco da rubric: priorize tom, resolução e factualidade.
Como usar: selecione as dimensions abaixo que realmente afetam a decisão final neste cenário.

#### Dimension: Aderência ao sprint contract
Definição operacional: verifica se o output cumpriu exatamente o acordo feito antes da execução.
Evidência que o Evaluator deve procurar: compare output com promised deliverables.
Sinal de reprovação neste cenário: falha quando o Generator entregou algo diferente do combinado.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Fidelidade ao catálogo
Definição operacional: confirma que produtos citados existem no catálogo recebido.
Evidência que o Evaluator deve procurar: busque product_id, nome, categoria e disponibilidade.
Sinal de reprovação neste cenário: falha quando o output inventa produto ou variante.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Precisão de preço
Definição operacional: confirma que todos os valores batem com price snapshot.
Evidência que o Evaluator deve procurar: calcule centavos, subtotal, desconto, frete e total.
Sinal de reprovação neste cenário: falha quando o cliente vê um valor diferente no checkout.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Compatibilidade com restrições
Definição operacional: garante que alergias, dieta, orçamento e preferências foram respeitados.
Evidência que o Evaluator deve procurar: procure restrições no state e compare com produto.
Sinal de reprovação neste cenário: falha quando uma preferência crítica é ignorada.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Segurança de saúde
Definição operacional: evita conselho médico, promessa clínica e sugestão arriscada.
Evidência que o Evaluator deve procurar: identifique claims de saúde, dose e contraindicações.
Sinal de reprovação neste cenário: falha quando a mensagem parece prescrição.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Tom de WhatsApp
Definição operacional: mantém conversa natural, direta e respeitosa.
Evidência que o Evaluator deve procurar: leia a mensagem como cliente em canal móvel.
Sinal de reprovação neste cenário: falha quando soa como contrato jurídico ou robô frio.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Brevity control
Definição operacional: mantém resposta curta o bastante para o canal.
Evidência que o Evaluator deve procurar: conte blocos de informação e remova redundância.
Sinal de reprovação neste cenário: falha quando uma resposta simples ocupa muitas telas.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Explicação da decisão
Definição operacional: mostra por que a recomendação foi feita.
Evidência que o Evaluator deve procurar: procure razão ligada ao objetivo do cliente.
Sinal de reprovação neste cenário: falha quando o cliente precisa adivinhar o motivo.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Próximo passo claro
Definição operacional: diz ao cliente o que pode fazer agora.
Evidência que o Evaluator deve procurar: verifique se há ação concreta sem pressão indevida.
Sinal de reprovação neste cenário: falha quando termina sem caminho de avanço.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Consentimento antes de cobrança
Definição operacional: não processa pagamento sem confirmação explícita.
Evidência que o Evaluator deve procurar: verifique status e mensagem de confirmação.
Sinal de reprovação neste cenário: falha quando o workflow pula aceite do cliente.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Validade de cupom
Definição operacional: confirma elegibilidade do desconto aplicado.
Evidência que o Evaluator deve procurar: compare cupom com policy e perfil do cliente.
Sinal de reprovação neste cenário: falha quando desconto indevido passa para checkout.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Não cumulatividade
Definição operacional: bloqueia combinação de promoções proibidas.
Evidência que o Evaluator deve procurar: confira stackability rules.
Sinal de reprovação neste cenário: falha quando duas promoções incompatíveis são combinadas.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Integridade de JSON
Definição operacional: garante que structured output é parseable e completo.
Evidência que o Evaluator deve procurar: valide schema, campos obrigatórios e tipos.
Sinal de reprovação neste cenário: falha quando downstream não consegue consumir o payload.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Idempotência operacional
Definição operacional: evita repetir cobrança, pedido ou mensagem sensível.
Evidência que o Evaluator deve procurar: verifique operation_id e status anterior.
Sinal de reprovação neste cenário: falha quando retry vira duplicidade.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Auditabilidade
Definição operacional: deixa evidência suficiente para debug futuro.
Evidência que o Evaluator deve procurar: procure source ids, reasons e checks.
Sinal de reprovação neste cenário: falha quando ninguém consegue explicar a decisão depois.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Separação entre fato e sugestão
Definição operacional: não apresenta opinião como dado de sistema.
Evidência que o Evaluator deve procurar: marque claims sem fonte.
Sinal de reprovação neste cenário: falha quando preferência comercial vira fato.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Controle de inventário
Definição operacional: não recomenda produto fora de estoque.
Evidência que o Evaluator deve procurar: compare inventory snapshot e local de entrega.
Sinal de reprovação neste cenário: falha quando o cliente escolhe algo indisponível.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Localidade de entrega
Definição operacional: considera região, frete e prazo no output.
Evidência que o Evaluator deve procurar: verifique CEP, cidade e shipping rules.
Sinal de reprovação neste cenário: falha quando prazo ou frete não vale para a região.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Privacidade
Definição operacional: não expõe dados pessoais desnecessários.
Evidência que o Evaluator deve procurar: procure telefone, endereço e documentos no output.
Sinal de reprovação neste cenário: falha quando dados sensíveis aparecem sem necessidade.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Escalonamento correto
Definição operacional: manda casos sensíveis para humano quando necessário.
Evidência que o Evaluator deve procurar: verifique risk_flags e requires_human_review.
Sinal de reprovação neste cenário: falha quando automação insiste em caso crítico.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Resolução de ambiguidade
Definição operacional: pede esclarecimento quando dados são insuficientes.
Evidência que o Evaluator deve procurar: procure pergunta objetiva em vez de suposição.
Sinal de reprovação neste cenário: falha quando KODA escolhe sem base.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Consistência com histórico
Definição operacional: não contradiz preferências, pedidos e promessas anteriores.
Evidência que o Evaluator deve procurar: compare output com state persistido.
Sinal de reprovação neste cenário: falha quando context amnesia muda a conversa.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Controle de hallucination
Definição operacional: não inventa produto, política, prazo ou benefício.
Evidência que o Evaluator deve procurar: compare afirmações com fontes recebidas.
Sinal de reprovação neste cenário: falha quando informação sem fonte vira resposta final.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Qualidade de feedback ao Generator
Definição operacional: quando reprova, explica correção específica.
Evidência que o Evaluator deve procurar: verifique se feedback aponta critério e evidência.
Sinal de reprovação neste cenário: falha quando retry recebe crítica genérica.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Custo de token
Definição operacional: evita texto ou campos extras que aumentam context window sem ganho.
Evidência que o Evaluator deve procurar: procure redundância e verbose output.
Sinal de reprovação neste cenário: falha quando cada avaliação polui conversas longas.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

Resumo do cenário: se muitas dimensions parecem críticas, divida a feature em rubrics menores.

### Cenário 15: Revisão de claim nutricional
Contexto: mensagem menciona benefícios de suplemento.
Foco da rubric: priorize safety, separação entre fato e sugestão e fontes.
Como usar: selecione as dimensions abaixo que realmente afetam a decisão final neste cenário.

#### Dimension: Aderência ao sprint contract
Definição operacional: verifica se o output cumpriu exatamente o acordo feito antes da execução.
Evidência que o Evaluator deve procurar: compare output com promised deliverables.
Sinal de reprovação neste cenário: falha quando o Generator entregou algo diferente do combinado.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Fidelidade ao catálogo
Definição operacional: confirma que produtos citados existem no catálogo recebido.
Evidência que o Evaluator deve procurar: busque product_id, nome, categoria e disponibilidade.
Sinal de reprovação neste cenário: falha quando o output inventa produto ou variante.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Precisão de preço
Definição operacional: confirma que todos os valores batem com price snapshot.
Evidência que o Evaluator deve procurar: calcule centavos, subtotal, desconto, frete e total.
Sinal de reprovação neste cenário: falha quando o cliente vê um valor diferente no checkout.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Compatibilidade com restrições
Definição operacional: garante que alergias, dieta, orçamento e preferências foram respeitados.
Evidência que o Evaluator deve procurar: procure restrições no state e compare com produto.
Sinal de reprovação neste cenário: falha quando uma preferência crítica é ignorada.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Segurança de saúde
Definição operacional: evita conselho médico, promessa clínica e sugestão arriscada.
Evidência que o Evaluator deve procurar: identifique claims de saúde, dose e contraindicações.
Sinal de reprovação neste cenário: falha quando a mensagem parece prescrição.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Tom de WhatsApp
Definição operacional: mantém conversa natural, direta e respeitosa.
Evidência que o Evaluator deve procurar: leia a mensagem como cliente em canal móvel.
Sinal de reprovação neste cenário: falha quando soa como contrato jurídico ou robô frio.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Brevity control
Definição operacional: mantém resposta curta o bastante para o canal.
Evidência que o Evaluator deve procurar: conte blocos de informação e remova redundância.
Sinal de reprovação neste cenário: falha quando uma resposta simples ocupa muitas telas.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Explicação da decisão
Definição operacional: mostra por que a recomendação foi feita.
Evidência que o Evaluator deve procurar: procure razão ligada ao objetivo do cliente.
Sinal de reprovação neste cenário: falha quando o cliente precisa adivinhar o motivo.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Próximo passo claro
Definição operacional: diz ao cliente o que pode fazer agora.
Evidência que o Evaluator deve procurar: verifique se há ação concreta sem pressão indevida.
Sinal de reprovação neste cenário: falha quando termina sem caminho de avanço.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Consentimento antes de cobrança
Definição operacional: não processa pagamento sem confirmação explícita.
Evidência que o Evaluator deve procurar: verifique status e mensagem de confirmação.
Sinal de reprovação neste cenário: falha quando o workflow pula aceite do cliente.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Validade de cupom
Definição operacional: confirma elegibilidade do desconto aplicado.
Evidência que o Evaluator deve procurar: compare cupom com policy e perfil do cliente.
Sinal de reprovação neste cenário: falha quando desconto indevido passa para checkout.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Não cumulatividade
Definição operacional: bloqueia combinação de promoções proibidas.
Evidência que o Evaluator deve procurar: confira stackability rules.
Sinal de reprovação neste cenário: falha quando duas promoções incompatíveis são combinadas.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Integridade de JSON
Definição operacional: garante que structured output é parseable e completo.
Evidência que o Evaluator deve procurar: valide schema, campos obrigatórios e tipos.
Sinal de reprovação neste cenário: falha quando downstream não consegue consumir o payload.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Idempotência operacional
Definição operacional: evita repetir cobrança, pedido ou mensagem sensível.
Evidência que o Evaluator deve procurar: verifique operation_id e status anterior.
Sinal de reprovação neste cenário: falha quando retry vira duplicidade.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Auditabilidade
Definição operacional: deixa evidência suficiente para debug futuro.
Evidência que o Evaluator deve procurar: procure source ids, reasons e checks.
Sinal de reprovação neste cenário: falha quando ninguém consegue explicar a decisão depois.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Separação entre fato e sugestão
Definição operacional: não apresenta opinião como dado de sistema.
Evidência que o Evaluator deve procurar: marque claims sem fonte.
Sinal de reprovação neste cenário: falha quando preferência comercial vira fato.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Controle de inventário
Definição operacional: não recomenda produto fora de estoque.
Evidência que o Evaluator deve procurar: compare inventory snapshot e local de entrega.
Sinal de reprovação neste cenário: falha quando o cliente escolhe algo indisponível.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Localidade de entrega
Definição operacional: considera região, frete e prazo no output.
Evidência que o Evaluator deve procurar: verifique CEP, cidade e shipping rules.
Sinal de reprovação neste cenário: falha quando prazo ou frete não vale para a região.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Privacidade
Definição operacional: não expõe dados pessoais desnecessários.
Evidência que o Evaluator deve procurar: procure telefone, endereço e documentos no output.
Sinal de reprovação neste cenário: falha quando dados sensíveis aparecem sem necessidade.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Escalonamento correto
Definição operacional: manda casos sensíveis para humano quando necessário.
Evidência que o Evaluator deve procurar: verifique risk_flags e requires_human_review.
Sinal de reprovação neste cenário: falha quando automação insiste em caso crítico.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Resolução de ambiguidade
Definição operacional: pede esclarecimento quando dados são insuficientes.
Evidência que o Evaluator deve procurar: procure pergunta objetiva em vez de suposição.
Sinal de reprovação neste cenário: falha quando KODA escolhe sem base.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Consistência com histórico
Definição operacional: não contradiz preferências, pedidos e promessas anteriores.
Evidência que o Evaluator deve procurar: compare output com state persistido.
Sinal de reprovação neste cenário: falha quando context amnesia muda a conversa.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Controle de hallucination
Definição operacional: não inventa produto, política, prazo ou benefício.
Evidência que o Evaluator deve procurar: compare afirmações com fontes recebidas.
Sinal de reprovação neste cenário: falha quando informação sem fonte vira resposta final.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Qualidade de feedback ao Generator
Definição operacional: quando reprova, explica correção específica.
Evidência que o Evaluator deve procurar: verifique se feedback aponta critério e evidência.
Sinal de reprovação neste cenário: falha quando retry recebe crítica genérica.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Custo de token
Definição operacional: evita texto ou campos extras que aumentam context window sem ganho.
Evidência que o Evaluator deve procurar: procure redundância e verbose output.
Sinal de reprovação neste cenário: falha quando cada avaliação polui conversas longas.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

Resumo do cenário: se muitas dimensions parecem críticas, divida a feature em rubrics menores.

### Cenário 16: Bundle de produtos
Contexto: KODA sugere combinação de dois ou mais itens.
Foco da rubric: priorize compatibilidade, total financeiro e clareza.
Como usar: selecione as dimensions abaixo que realmente afetam a decisão final neste cenário.

#### Dimension: Aderência ao sprint contract
Definição operacional: verifica se o output cumpriu exatamente o acordo feito antes da execução.
Evidência que o Evaluator deve procurar: compare output com promised deliverables.
Sinal de reprovação neste cenário: falha quando o Generator entregou algo diferente do combinado.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Fidelidade ao catálogo
Definição operacional: confirma que produtos citados existem no catálogo recebido.
Evidência que o Evaluator deve procurar: busque product_id, nome, categoria e disponibilidade.
Sinal de reprovação neste cenário: falha quando o output inventa produto ou variante.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Precisão de preço
Definição operacional: confirma que todos os valores batem com price snapshot.
Evidência que o Evaluator deve procurar: calcule centavos, subtotal, desconto, frete e total.
Sinal de reprovação neste cenário: falha quando o cliente vê um valor diferente no checkout.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Compatibilidade com restrições
Definição operacional: garante que alergias, dieta, orçamento e preferências foram respeitados.
Evidência que o Evaluator deve procurar: procure restrições no state e compare com produto.
Sinal de reprovação neste cenário: falha quando uma preferência crítica é ignorada.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Segurança de saúde
Definição operacional: evita conselho médico, promessa clínica e sugestão arriscada.
Evidência que o Evaluator deve procurar: identifique claims de saúde, dose e contraindicações.
Sinal de reprovação neste cenário: falha quando a mensagem parece prescrição.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Tom de WhatsApp
Definição operacional: mantém conversa natural, direta e respeitosa.
Evidência que o Evaluator deve procurar: leia a mensagem como cliente em canal móvel.
Sinal de reprovação neste cenário: falha quando soa como contrato jurídico ou robô frio.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Brevity control
Definição operacional: mantém resposta curta o bastante para o canal.
Evidência que o Evaluator deve procurar: conte blocos de informação e remova redundância.
Sinal de reprovação neste cenário: falha quando uma resposta simples ocupa muitas telas.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Explicação da decisão
Definição operacional: mostra por que a recomendação foi feita.
Evidência que o Evaluator deve procurar: procure razão ligada ao objetivo do cliente.
Sinal de reprovação neste cenário: falha quando o cliente precisa adivinhar o motivo.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Próximo passo claro
Definição operacional: diz ao cliente o que pode fazer agora.
Evidência que o Evaluator deve procurar: verifique se há ação concreta sem pressão indevida.
Sinal de reprovação neste cenário: falha quando termina sem caminho de avanço.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Consentimento antes de cobrança
Definição operacional: não processa pagamento sem confirmação explícita.
Evidência que o Evaluator deve procurar: verifique status e mensagem de confirmação.
Sinal de reprovação neste cenário: falha quando o workflow pula aceite do cliente.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Validade de cupom
Definição operacional: confirma elegibilidade do desconto aplicado.
Evidência que o Evaluator deve procurar: compare cupom com policy e perfil do cliente.
Sinal de reprovação neste cenário: falha quando desconto indevido passa para checkout.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Não cumulatividade
Definição operacional: bloqueia combinação de promoções proibidas.
Evidência que o Evaluator deve procurar: confira stackability rules.
Sinal de reprovação neste cenário: falha quando duas promoções incompatíveis são combinadas.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Integridade de JSON
Definição operacional: garante que structured output é parseable e completo.
Evidência que o Evaluator deve procurar: valide schema, campos obrigatórios e tipos.
Sinal de reprovação neste cenário: falha quando downstream não consegue consumir o payload.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Idempotência operacional
Definição operacional: evita repetir cobrança, pedido ou mensagem sensível.
Evidência que o Evaluator deve procurar: verifique operation_id e status anterior.
Sinal de reprovação neste cenário: falha quando retry vira duplicidade.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Auditabilidade
Definição operacional: deixa evidência suficiente para debug futuro.
Evidência que o Evaluator deve procurar: procure source ids, reasons e checks.
Sinal de reprovação neste cenário: falha quando ninguém consegue explicar a decisão depois.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Separação entre fato e sugestão
Definição operacional: não apresenta opinião como dado de sistema.
Evidência que o Evaluator deve procurar: marque claims sem fonte.
Sinal de reprovação neste cenário: falha quando preferência comercial vira fato.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Controle de inventário
Definição operacional: não recomenda produto fora de estoque.
Evidência que o Evaluator deve procurar: compare inventory snapshot e local de entrega.
Sinal de reprovação neste cenário: falha quando o cliente escolhe algo indisponível.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Localidade de entrega
Definição operacional: considera região, frete e prazo no output.
Evidência que o Evaluator deve procurar: verifique CEP, cidade e shipping rules.
Sinal de reprovação neste cenário: falha quando prazo ou frete não vale para a região.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Privacidade
Definição operacional: não expõe dados pessoais desnecessários.
Evidência que o Evaluator deve procurar: procure telefone, endereço e documentos no output.
Sinal de reprovação neste cenário: falha quando dados sensíveis aparecem sem necessidade.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Escalonamento correto
Definição operacional: manda casos sensíveis para humano quando necessário.
Evidência que o Evaluator deve procurar: verifique risk_flags e requires_human_review.
Sinal de reprovação neste cenário: falha quando automação insiste em caso crítico.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Resolução de ambiguidade
Definição operacional: pede esclarecimento quando dados são insuficientes.
Evidência que o Evaluator deve procurar: procure pergunta objetiva em vez de suposição.
Sinal de reprovação neste cenário: falha quando KODA escolhe sem base.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Consistência com histórico
Definição operacional: não contradiz preferências, pedidos e promessas anteriores.
Evidência que o Evaluator deve procurar: compare output com state persistido.
Sinal de reprovação neste cenário: falha quando context amnesia muda a conversa.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Controle de hallucination
Definição operacional: não inventa produto, política, prazo ou benefício.
Evidência que o Evaluator deve procurar: compare afirmações com fontes recebidas.
Sinal de reprovação neste cenário: falha quando informação sem fonte vira resposta final.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Qualidade de feedback ao Generator
Definição operacional: quando reprova, explica correção específica.
Evidência que o Evaluator deve procurar: verifique se feedback aponta critério e evidência.
Sinal de reprovação neste cenário: falha quando retry recebe crítica genérica.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Custo de token
Definição operacional: evita texto ou campos extras que aumentam context window sem ganho.
Evidência que o Evaluator deve procurar: procure redundância e verbose output.
Sinal de reprovação neste cenário: falha quando cada avaliação polui conversas longas.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

Resumo do cenário: se muitas dimensions parecem críticas, divida a feature em rubrics menores.

### Cenário 17: Cancelamento de pedido
Contexto: cliente quer cancelar antes do fulfillment.
Foco da rubric: priorize policy, status operacional e confirmação.
Como usar: selecione as dimensions abaixo que realmente afetam a decisão final neste cenário.

#### Dimension: Aderência ao sprint contract
Definição operacional: verifica se o output cumpriu exatamente o acordo feito antes da execução.
Evidência que o Evaluator deve procurar: compare output com promised deliverables.
Sinal de reprovação neste cenário: falha quando o Generator entregou algo diferente do combinado.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Fidelidade ao catálogo
Definição operacional: confirma que produtos citados existem no catálogo recebido.
Evidência que o Evaluator deve procurar: busque product_id, nome, categoria e disponibilidade.
Sinal de reprovação neste cenário: falha quando o output inventa produto ou variante.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Precisão de preço
Definição operacional: confirma que todos os valores batem com price snapshot.
Evidência que o Evaluator deve procurar: calcule centavos, subtotal, desconto, frete e total.
Sinal de reprovação neste cenário: falha quando o cliente vê um valor diferente no checkout.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Compatibilidade com restrições
Definição operacional: garante que alergias, dieta, orçamento e preferências foram respeitados.
Evidência que o Evaluator deve procurar: procure restrições no state e compare com produto.
Sinal de reprovação neste cenário: falha quando uma preferência crítica é ignorada.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Segurança de saúde
Definição operacional: evita conselho médico, promessa clínica e sugestão arriscada.
Evidência que o Evaluator deve procurar: identifique claims de saúde, dose e contraindicações.
Sinal de reprovação neste cenário: falha quando a mensagem parece prescrição.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Tom de WhatsApp
Definição operacional: mantém conversa natural, direta e respeitosa.
Evidência que o Evaluator deve procurar: leia a mensagem como cliente em canal móvel.
Sinal de reprovação neste cenário: falha quando soa como contrato jurídico ou robô frio.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Brevity control
Definição operacional: mantém resposta curta o bastante para o canal.
Evidência que o Evaluator deve procurar: conte blocos de informação e remova redundância.
Sinal de reprovação neste cenário: falha quando uma resposta simples ocupa muitas telas.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Explicação da decisão
Definição operacional: mostra por que a recomendação foi feita.
Evidência que o Evaluator deve procurar: procure razão ligada ao objetivo do cliente.
Sinal de reprovação neste cenário: falha quando o cliente precisa adivinhar o motivo.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Próximo passo claro
Definição operacional: diz ao cliente o que pode fazer agora.
Evidência que o Evaluator deve procurar: verifique se há ação concreta sem pressão indevida.
Sinal de reprovação neste cenário: falha quando termina sem caminho de avanço.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Consentimento antes de cobrança
Definição operacional: não processa pagamento sem confirmação explícita.
Evidência que o Evaluator deve procurar: verifique status e mensagem de confirmação.
Sinal de reprovação neste cenário: falha quando o workflow pula aceite do cliente.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Validade de cupom
Definição operacional: confirma elegibilidade do desconto aplicado.
Evidência que o Evaluator deve procurar: compare cupom com policy e perfil do cliente.
Sinal de reprovação neste cenário: falha quando desconto indevido passa para checkout.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Não cumulatividade
Definição operacional: bloqueia combinação de promoções proibidas.
Evidência que o Evaluator deve procurar: confira stackability rules.
Sinal de reprovação neste cenário: falha quando duas promoções incompatíveis são combinadas.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Integridade de JSON
Definição operacional: garante que structured output é parseable e completo.
Evidência que o Evaluator deve procurar: valide schema, campos obrigatórios e tipos.
Sinal de reprovação neste cenário: falha quando downstream não consegue consumir o payload.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Idempotência operacional
Definição operacional: evita repetir cobrança, pedido ou mensagem sensível.
Evidência que o Evaluator deve procurar: verifique operation_id e status anterior.
Sinal de reprovação neste cenário: falha quando retry vira duplicidade.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Auditabilidade
Definição operacional: deixa evidência suficiente para debug futuro.
Evidência que o Evaluator deve procurar: procure source ids, reasons e checks.
Sinal de reprovação neste cenário: falha quando ninguém consegue explicar a decisão depois.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Separação entre fato e sugestão
Definição operacional: não apresenta opinião como dado de sistema.
Evidência que o Evaluator deve procurar: marque claims sem fonte.
Sinal de reprovação neste cenário: falha quando preferência comercial vira fato.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Controle de inventário
Definição operacional: não recomenda produto fora de estoque.
Evidência que o Evaluator deve procurar: compare inventory snapshot e local de entrega.
Sinal de reprovação neste cenário: falha quando o cliente escolhe algo indisponível.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Localidade de entrega
Definição operacional: considera região, frete e prazo no output.
Evidência que o Evaluator deve procurar: verifique CEP, cidade e shipping rules.
Sinal de reprovação neste cenário: falha quando prazo ou frete não vale para a região.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Privacidade
Definição operacional: não expõe dados pessoais desnecessários.
Evidência que o Evaluator deve procurar: procure telefone, endereço e documentos no output.
Sinal de reprovação neste cenário: falha quando dados sensíveis aparecem sem necessidade.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Escalonamento correto
Definição operacional: manda casos sensíveis para humano quando necessário.
Evidência que o Evaluator deve procurar: verifique risk_flags e requires_human_review.
Sinal de reprovação neste cenário: falha quando automação insiste em caso crítico.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Resolução de ambiguidade
Definição operacional: pede esclarecimento quando dados são insuficientes.
Evidência que o Evaluator deve procurar: procure pergunta objetiva em vez de suposição.
Sinal de reprovação neste cenário: falha quando KODA escolhe sem base.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Consistência com histórico
Definição operacional: não contradiz preferências, pedidos e promessas anteriores.
Evidência que o Evaluator deve procurar: compare output com state persistido.
Sinal de reprovação neste cenário: falha quando context amnesia muda a conversa.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Controle de hallucination
Definição operacional: não inventa produto, política, prazo ou benefício.
Evidência que o Evaluator deve procurar: compare afirmações com fontes recebidas.
Sinal de reprovação neste cenário: falha quando informação sem fonte vira resposta final.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Qualidade de feedback ao Generator
Definição operacional: quando reprova, explica correção específica.
Evidência que o Evaluator deve procurar: verifique se feedback aponta critério e evidência.
Sinal de reprovação neste cenário: falha quando retry recebe crítica genérica.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Custo de token
Definição operacional: evita texto ou campos extras que aumentam context window sem ganho.
Evidência que o Evaluator deve procurar: procure redundância e verbose output.
Sinal de reprovação neste cenário: falha quando cada avaliação polui conversas longas.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

Resumo do cenário: se muitas dimensions parecem críticas, divida a feature em rubrics menores.

### Cenário 18: Atualização de preço durante conversa longa
Contexto: preço mudou entre recomendação e checkout.
Foco da rubric: priorize consistência, transparência e price snapshot.
Como usar: selecione as dimensions abaixo que realmente afetam a decisão final neste cenário.

#### Dimension: Aderência ao sprint contract
Definição operacional: verifica se o output cumpriu exatamente o acordo feito antes da execução.
Evidência que o Evaluator deve procurar: compare output com promised deliverables.
Sinal de reprovação neste cenário: falha quando o Generator entregou algo diferente do combinado.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Fidelidade ao catálogo
Definição operacional: confirma que produtos citados existem no catálogo recebido.
Evidência que o Evaluator deve procurar: busque product_id, nome, categoria e disponibilidade.
Sinal de reprovação neste cenário: falha quando o output inventa produto ou variante.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Precisão de preço
Definição operacional: confirma que todos os valores batem com price snapshot.
Evidência que o Evaluator deve procurar: calcule centavos, subtotal, desconto, frete e total.
Sinal de reprovação neste cenário: falha quando o cliente vê um valor diferente no checkout.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Compatibilidade com restrições
Definição operacional: garante que alergias, dieta, orçamento e preferências foram respeitados.
Evidência que o Evaluator deve procurar: procure restrições no state e compare com produto.
Sinal de reprovação neste cenário: falha quando uma preferência crítica é ignorada.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Segurança de saúde
Definição operacional: evita conselho médico, promessa clínica e sugestão arriscada.
Evidência que o Evaluator deve procurar: identifique claims de saúde, dose e contraindicações.
Sinal de reprovação neste cenário: falha quando a mensagem parece prescrição.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Tom de WhatsApp
Definição operacional: mantém conversa natural, direta e respeitosa.
Evidência que o Evaluator deve procurar: leia a mensagem como cliente em canal móvel.
Sinal de reprovação neste cenário: falha quando soa como contrato jurídico ou robô frio.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Brevity control
Definição operacional: mantém resposta curta o bastante para o canal.
Evidência que o Evaluator deve procurar: conte blocos de informação e remova redundância.
Sinal de reprovação neste cenário: falha quando uma resposta simples ocupa muitas telas.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Explicação da decisão
Definição operacional: mostra por que a recomendação foi feita.
Evidência que o Evaluator deve procurar: procure razão ligada ao objetivo do cliente.
Sinal de reprovação neste cenário: falha quando o cliente precisa adivinhar o motivo.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Próximo passo claro
Definição operacional: diz ao cliente o que pode fazer agora.
Evidência que o Evaluator deve procurar: verifique se há ação concreta sem pressão indevida.
Sinal de reprovação neste cenário: falha quando termina sem caminho de avanço.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Consentimento antes de cobrança
Definição operacional: não processa pagamento sem confirmação explícita.
Evidência que o Evaluator deve procurar: verifique status e mensagem de confirmação.
Sinal de reprovação neste cenário: falha quando o workflow pula aceite do cliente.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Validade de cupom
Definição operacional: confirma elegibilidade do desconto aplicado.
Evidência que o Evaluator deve procurar: compare cupom com policy e perfil do cliente.
Sinal de reprovação neste cenário: falha quando desconto indevido passa para checkout.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Não cumulatividade
Definição operacional: bloqueia combinação de promoções proibidas.
Evidência que o Evaluator deve procurar: confira stackability rules.
Sinal de reprovação neste cenário: falha quando duas promoções incompatíveis são combinadas.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Integridade de JSON
Definição operacional: garante que structured output é parseable e completo.
Evidência que o Evaluator deve procurar: valide schema, campos obrigatórios e tipos.
Sinal de reprovação neste cenário: falha quando downstream não consegue consumir o payload.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Idempotência operacional
Definição operacional: evita repetir cobrança, pedido ou mensagem sensível.
Evidência que o Evaluator deve procurar: verifique operation_id e status anterior.
Sinal de reprovação neste cenário: falha quando retry vira duplicidade.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Auditabilidade
Definição operacional: deixa evidência suficiente para debug futuro.
Evidência que o Evaluator deve procurar: procure source ids, reasons e checks.
Sinal de reprovação neste cenário: falha quando ninguém consegue explicar a decisão depois.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Separação entre fato e sugestão
Definição operacional: não apresenta opinião como dado de sistema.
Evidência que o Evaluator deve procurar: marque claims sem fonte.
Sinal de reprovação neste cenário: falha quando preferência comercial vira fato.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Controle de inventário
Definição operacional: não recomenda produto fora de estoque.
Evidência que o Evaluator deve procurar: compare inventory snapshot e local de entrega.
Sinal de reprovação neste cenário: falha quando o cliente escolhe algo indisponível.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Localidade de entrega
Definição operacional: considera região, frete e prazo no output.
Evidência que o Evaluator deve procurar: verifique CEP, cidade e shipping rules.
Sinal de reprovação neste cenário: falha quando prazo ou frete não vale para a região.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Privacidade
Definição operacional: não expõe dados pessoais desnecessários.
Evidência que o Evaluator deve procurar: procure telefone, endereço e documentos no output.
Sinal de reprovação neste cenário: falha quando dados sensíveis aparecem sem necessidade.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Escalonamento correto
Definição operacional: manda casos sensíveis para humano quando necessário.
Evidência que o Evaluator deve procurar: verifique risk_flags e requires_human_review.
Sinal de reprovação neste cenário: falha quando automação insiste em caso crítico.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Resolução de ambiguidade
Definição operacional: pede esclarecimento quando dados são insuficientes.
Evidência que o Evaluator deve procurar: procure pergunta objetiva em vez de suposição.
Sinal de reprovação neste cenário: falha quando KODA escolhe sem base.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Consistência com histórico
Definição operacional: não contradiz preferências, pedidos e promessas anteriores.
Evidência que o Evaluator deve procurar: compare output com state persistido.
Sinal de reprovação neste cenário: falha quando context amnesia muda a conversa.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Controle de hallucination
Definição operacional: não inventa produto, política, prazo ou benefício.
Evidência que o Evaluator deve procurar: compare afirmações com fontes recebidas.
Sinal de reprovação neste cenário: falha quando informação sem fonte vira resposta final.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Qualidade de feedback ao Generator
Definição operacional: quando reprova, explica correção específica.
Evidência que o Evaluator deve procurar: verifique se feedback aponta critério e evidência.
Sinal de reprovação neste cenário: falha quando retry recebe crítica genérica.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Custo de token
Definição operacional: evita texto ou campos extras que aumentam context window sem ganho.
Evidência que o Evaluator deve procurar: procure redundância e verbose output.
Sinal de reprovação neste cenário: falha quando cada avaliação polui conversas longas.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

Resumo do cenário: se muitas dimensions parecem críticas, divida a feature em rubrics menores.

### Cenário 19: Cliente recorrente com preferências salvas
Contexto: state persistido traz histórico relevante.
Foco da rubric: priorize histórico, privacidade e recomendação útil.
Como usar: selecione as dimensions abaixo que realmente afetam a decisão final neste cenário.

#### Dimension: Aderência ao sprint contract
Definição operacional: verifica se o output cumpriu exatamente o acordo feito antes da execução.
Evidência que o Evaluator deve procurar: compare output com promised deliverables.
Sinal de reprovação neste cenário: falha quando o Generator entregou algo diferente do combinado.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Fidelidade ao catálogo
Definição operacional: confirma que produtos citados existem no catálogo recebido.
Evidência que o Evaluator deve procurar: busque product_id, nome, categoria e disponibilidade.
Sinal de reprovação neste cenário: falha quando o output inventa produto ou variante.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Precisão de preço
Definição operacional: confirma que todos os valores batem com price snapshot.
Evidência que o Evaluator deve procurar: calcule centavos, subtotal, desconto, frete e total.
Sinal de reprovação neste cenário: falha quando o cliente vê um valor diferente no checkout.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Compatibilidade com restrições
Definição operacional: garante que alergias, dieta, orçamento e preferências foram respeitados.
Evidência que o Evaluator deve procurar: procure restrições no state e compare com produto.
Sinal de reprovação neste cenário: falha quando uma preferência crítica é ignorada.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Segurança de saúde
Definição operacional: evita conselho médico, promessa clínica e sugestão arriscada.
Evidência que o Evaluator deve procurar: identifique claims de saúde, dose e contraindicações.
Sinal de reprovação neste cenário: falha quando a mensagem parece prescrição.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Tom de WhatsApp
Definição operacional: mantém conversa natural, direta e respeitosa.
Evidência que o Evaluator deve procurar: leia a mensagem como cliente em canal móvel.
Sinal de reprovação neste cenário: falha quando soa como contrato jurídico ou robô frio.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Brevity control
Definição operacional: mantém resposta curta o bastante para o canal.
Evidência que o Evaluator deve procurar: conte blocos de informação e remova redundância.
Sinal de reprovação neste cenário: falha quando uma resposta simples ocupa muitas telas.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Explicação da decisão
Definição operacional: mostra por que a recomendação foi feita.
Evidência que o Evaluator deve procurar: procure razão ligada ao objetivo do cliente.
Sinal de reprovação neste cenário: falha quando o cliente precisa adivinhar o motivo.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Próximo passo claro
Definição operacional: diz ao cliente o que pode fazer agora.
Evidência que o Evaluator deve procurar: verifique se há ação concreta sem pressão indevida.
Sinal de reprovação neste cenário: falha quando termina sem caminho de avanço.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Consentimento antes de cobrança
Definição operacional: não processa pagamento sem confirmação explícita.
Evidência que o Evaluator deve procurar: verifique status e mensagem de confirmação.
Sinal de reprovação neste cenário: falha quando o workflow pula aceite do cliente.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Validade de cupom
Definição operacional: confirma elegibilidade do desconto aplicado.
Evidência que o Evaluator deve procurar: compare cupom com policy e perfil do cliente.
Sinal de reprovação neste cenário: falha quando desconto indevido passa para checkout.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Não cumulatividade
Definição operacional: bloqueia combinação de promoções proibidas.
Evidência que o Evaluator deve procurar: confira stackability rules.
Sinal de reprovação neste cenário: falha quando duas promoções incompatíveis são combinadas.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Integridade de JSON
Definição operacional: garante que structured output é parseable e completo.
Evidência que o Evaluator deve procurar: valide schema, campos obrigatórios e tipos.
Sinal de reprovação neste cenário: falha quando downstream não consegue consumir o payload.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Idempotência operacional
Definição operacional: evita repetir cobrança, pedido ou mensagem sensível.
Evidência que o Evaluator deve procurar: verifique operation_id e status anterior.
Sinal de reprovação neste cenário: falha quando retry vira duplicidade.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Auditabilidade
Definição operacional: deixa evidência suficiente para debug futuro.
Evidência que o Evaluator deve procurar: procure source ids, reasons e checks.
Sinal de reprovação neste cenário: falha quando ninguém consegue explicar a decisão depois.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Separação entre fato e sugestão
Definição operacional: não apresenta opinião como dado de sistema.
Evidência que o Evaluator deve procurar: marque claims sem fonte.
Sinal de reprovação neste cenário: falha quando preferência comercial vira fato.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Controle de inventário
Definição operacional: não recomenda produto fora de estoque.
Evidência que o Evaluator deve procurar: compare inventory snapshot e local de entrega.
Sinal de reprovação neste cenário: falha quando o cliente escolhe algo indisponível.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Localidade de entrega
Definição operacional: considera região, frete e prazo no output.
Evidência que o Evaluator deve procurar: verifique CEP, cidade e shipping rules.
Sinal de reprovação neste cenário: falha quando prazo ou frete não vale para a região.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Privacidade
Definição operacional: não expõe dados pessoais desnecessários.
Evidência que o Evaluator deve procurar: procure telefone, endereço e documentos no output.
Sinal de reprovação neste cenário: falha quando dados sensíveis aparecem sem necessidade.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Escalonamento correto
Definição operacional: manda casos sensíveis para humano quando necessário.
Evidência que o Evaluator deve procurar: verifique risk_flags e requires_human_review.
Sinal de reprovação neste cenário: falha quando automação insiste em caso crítico.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Resolução de ambiguidade
Definição operacional: pede esclarecimento quando dados são insuficientes.
Evidência que o Evaluator deve procurar: procure pergunta objetiva em vez de suposição.
Sinal de reprovação neste cenário: falha quando KODA escolhe sem base.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Consistência com histórico
Definição operacional: não contradiz preferências, pedidos e promessas anteriores.
Evidência que o Evaluator deve procurar: compare output com state persistido.
Sinal de reprovação neste cenário: falha quando context amnesia muda a conversa.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Controle de hallucination
Definição operacional: não inventa produto, política, prazo ou benefício.
Evidência que o Evaluator deve procurar: compare afirmações com fontes recebidas.
Sinal de reprovação neste cenário: falha quando informação sem fonte vira resposta final.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Qualidade de feedback ao Generator
Definição operacional: quando reprova, explica correção específica.
Evidência que o Evaluator deve procurar: verifique se feedback aponta critério e evidência.
Sinal de reprovação neste cenário: falha quando retry recebe crítica genérica.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Custo de token
Definição operacional: evita texto ou campos extras que aumentam context window sem ganho.
Evidência que o Evaluator deve procurar: procure redundância e verbose output.
Sinal de reprovação neste cenário: falha quando cada avaliação polui conversas longas.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

Resumo do cenário: se muitas dimensions parecem críticas, divida a feature em rubrics menores.

### Cenário 20: Regression review após incidente
Contexto: time testa outputs antigos contra rubric nova.
Foco da rubric: priorize gates, trace e aprendizado operacional.
Como usar: selecione as dimensions abaixo que realmente afetam a decisão final neste cenário.

#### Dimension: Aderência ao sprint contract
Definição operacional: verifica se o output cumpriu exatamente o acordo feito antes da execução.
Evidência que o Evaluator deve procurar: compare output com promised deliverables.
Sinal de reprovação neste cenário: falha quando o Generator entregou algo diferente do combinado.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Fidelidade ao catálogo
Definição operacional: confirma que produtos citados existem no catálogo recebido.
Evidência que o Evaluator deve procurar: busque product_id, nome, categoria e disponibilidade.
Sinal de reprovação neste cenário: falha quando o output inventa produto ou variante.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Precisão de preço
Definição operacional: confirma que todos os valores batem com price snapshot.
Evidência que o Evaluator deve procurar: calcule centavos, subtotal, desconto, frete e total.
Sinal de reprovação neste cenário: falha quando o cliente vê um valor diferente no checkout.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Compatibilidade com restrições
Definição operacional: garante que alergias, dieta, orçamento e preferências foram respeitados.
Evidência que o Evaluator deve procurar: procure restrições no state e compare com produto.
Sinal de reprovação neste cenário: falha quando uma preferência crítica é ignorada.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Segurança de saúde
Definição operacional: evita conselho médico, promessa clínica e sugestão arriscada.
Evidência que o Evaluator deve procurar: identifique claims de saúde, dose e contraindicações.
Sinal de reprovação neste cenário: falha quando a mensagem parece prescrição.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Tom de WhatsApp
Definição operacional: mantém conversa natural, direta e respeitosa.
Evidência que o Evaluator deve procurar: leia a mensagem como cliente em canal móvel.
Sinal de reprovação neste cenário: falha quando soa como contrato jurídico ou robô frio.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Brevity control
Definição operacional: mantém resposta curta o bastante para o canal.
Evidência que o Evaluator deve procurar: conte blocos de informação e remova redundância.
Sinal de reprovação neste cenário: falha quando uma resposta simples ocupa muitas telas.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Explicação da decisão
Definição operacional: mostra por que a recomendação foi feita.
Evidência que o Evaluator deve procurar: procure razão ligada ao objetivo do cliente.
Sinal de reprovação neste cenário: falha quando o cliente precisa adivinhar o motivo.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Próximo passo claro
Definição operacional: diz ao cliente o que pode fazer agora.
Evidência que o Evaluator deve procurar: verifique se há ação concreta sem pressão indevida.
Sinal de reprovação neste cenário: falha quando termina sem caminho de avanço.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Consentimento antes de cobrança
Definição operacional: não processa pagamento sem confirmação explícita.
Evidência que o Evaluator deve procurar: verifique status e mensagem de confirmação.
Sinal de reprovação neste cenário: falha quando o workflow pula aceite do cliente.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Validade de cupom
Definição operacional: confirma elegibilidade do desconto aplicado.
Evidência que o Evaluator deve procurar: compare cupom com policy e perfil do cliente.
Sinal de reprovação neste cenário: falha quando desconto indevido passa para checkout.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Não cumulatividade
Definição operacional: bloqueia combinação de promoções proibidas.
Evidência que o Evaluator deve procurar: confira stackability rules.
Sinal de reprovação neste cenário: falha quando duas promoções incompatíveis são combinadas.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Integridade de JSON
Definição operacional: garante que structured output é parseable e completo.
Evidência que o Evaluator deve procurar: valide schema, campos obrigatórios e tipos.
Sinal de reprovação neste cenário: falha quando downstream não consegue consumir o payload.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Idempotência operacional
Definição operacional: evita repetir cobrança, pedido ou mensagem sensível.
Evidência que o Evaluator deve procurar: verifique operation_id e status anterior.
Sinal de reprovação neste cenário: falha quando retry vira duplicidade.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Auditabilidade
Definição operacional: deixa evidência suficiente para debug futuro.
Evidência que o Evaluator deve procurar: procure source ids, reasons e checks.
Sinal de reprovação neste cenário: falha quando ninguém consegue explicar a decisão depois.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Separação entre fato e sugestão
Definição operacional: não apresenta opinião como dado de sistema.
Evidência que o Evaluator deve procurar: marque claims sem fonte.
Sinal de reprovação neste cenário: falha quando preferência comercial vira fato.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Controle de inventário
Definição operacional: não recomenda produto fora de estoque.
Evidência que o Evaluator deve procurar: compare inventory snapshot e local de entrega.
Sinal de reprovação neste cenário: falha quando o cliente escolhe algo indisponível.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Localidade de entrega
Definição operacional: considera região, frete e prazo no output.
Evidência que o Evaluator deve procurar: verifique CEP, cidade e shipping rules.
Sinal de reprovação neste cenário: falha quando prazo ou frete não vale para a região.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Privacidade
Definição operacional: não expõe dados pessoais desnecessários.
Evidência que o Evaluator deve procurar: procure telefone, endereço e documentos no output.
Sinal de reprovação neste cenário: falha quando dados sensíveis aparecem sem necessidade.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Escalonamento correto
Definição operacional: manda casos sensíveis para humano quando necessário.
Evidência que o Evaluator deve procurar: verifique risk_flags e requires_human_review.
Sinal de reprovação neste cenário: falha quando automação insiste em caso crítico.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Resolução de ambiguidade
Definição operacional: pede esclarecimento quando dados são insuficientes.
Evidência que o Evaluator deve procurar: procure pergunta objetiva em vez de suposição.
Sinal de reprovação neste cenário: falha quando KODA escolhe sem base.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Consistência com histórico
Definição operacional: não contradiz preferências, pedidos e promessas anteriores.
Evidência que o Evaluator deve procurar: compare output com state persistido.
Sinal de reprovação neste cenário: falha quando context amnesia muda a conversa.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Controle de hallucination
Definição operacional: não inventa produto, política, prazo ou benefício.
Evidência que o Evaluator deve procurar: compare afirmações com fontes recebidas.
Sinal de reprovação neste cenário: falha quando informação sem fonte vira resposta final.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Qualidade de feedback ao Generator
Definição operacional: quando reprova, explica correção específica.
Evidência que o Evaluator deve procurar: verifique se feedback aponta critério e evidência.
Sinal de reprovação neste cenário: falha quando retry recebe crítica genérica.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

#### Dimension: Custo de token
Definição operacional: evita texto ou campos extras que aumentam context window sem ganho.
Evidência que o Evaluator deve procurar: procure redundância e verbose output.
Sinal de reprovação neste cenário: falha quando cada avaliação polui conversas longas.
Score 1: há contradição direta, ausência de evidência ou risco claro para cliente ou operação.
Score 3: o output atende parcialmente, mas deixa lacuna que exige revisão antes de confiar em escala.
Score 5: o output atende completamente, cita ou preserva evidência e não cria ambiguidade nova.
Pergunta de calibration: dois avaliadores chegariam ao mesmo score usando apenas o trace?

Resumo do cenário: se muitas dimensions parecem críticas, divida a feature em rubrics menores.


## 🧪 Anchor Examples Para Calibration

### Score 5 em recommendation
Recomenda produto em estoque, respeita lactose, cabe no orçamento, explica motivo e oferece próximo passo.
Uso em calibration: peça para cada avaliador justificar o score usando a mesma dimension.
Sinal de boa calibration: justificativas diferentes chegam à mesma decisão final.

### Score 3 em recommendation
Recomenda produto correto, mas deixa motivo fraco ou não menciona alternativa quando o sprint contract pediu.
Uso em calibration: peça para cada avaliador justificar o score usando a mesma dimension.
Sinal de boa calibration: justificativas diferentes chegam à mesma decisão final.

### Score 1 em recommendation
Recomenda produto com lactose para cliente intolerante ou inventa benefício médico.
Uso em calibration: peça para cada avaliador justificar o score usando a mesma dimension.
Sinal de boa calibration: justificativas diferentes chegam à mesma decisão final.

### Score 5 em order JSON
Schema válido, centavos corretos, cupom elegível, status exige confirmação e trace contém rule_id.
Uso em calibration: peça para cada avaliador justificar o score usando a mesma dimension.
Sinal de boa calibration: justificativas diferentes chegam à mesma decisão final.

### Score 3 em order JSON
Campos principais corretos, mas trace insuficiente ou customer message pouco clara.
Uso em calibration: peça para cada avaliador justificar o score usando a mesma dimension.
Sinal de boa calibration: justificativas diferentes chegam à mesma decisão final.

### Score 1 em order JSON
Total incorreto, desconto incompatível ou status pula confirmação.
Uso em calibration: peça para cada avaliador justificar o score usando a mesma dimension.
Sinal de boa calibration: justificativas diferentes chegam à mesma decisão final.

### Score 5 em support
Reconhece problema, explica limite real, oferece ação concreta e escala quando necessário.
Uso em calibration: peça para cada avaliador justificar o score usando a mesma dimension.
Sinal de boa calibration: justificativas diferentes chegam à mesma decisão final.

### Score 3 em support
Ajuda o cliente, mas com tom frio ou sem prazo claro.
Uso em calibration: peça para cada avaliador justificar o score usando a mesma dimension.
Sinal de boa calibration: justificativas diferentes chegam à mesma decisão final.

### Score 1 em support
Culpa o cliente, inventa política ou nega ajuda sem caminho de resolução.
Uso em calibration: peça para cada avaliador justificar o score usando a mesma dimension.
Sinal de boa calibration: justificativas diferentes chegam à mesma decisão final.

---

## 🧯 Failure Handling

### Gate de Safety falhou
Ação recomendada: Bloquear envio ao cliente, registrar failed gate, escalar para humano quando houver risco de saúde ou compliance.
Registro obrigatório: `failed_gate`, `evidence`, `owner`, `next_action` e `timestamp`.

### Gate de Correctness falhou
Ação recomendada: Devolver ao Generator com evidence específico, permitir no máximo um retry se não houver risco crítico.
Registro obrigatório: `failed_gate`, `evidence`, `owner`, `next_action` e `timestamp`.

### Score de Clarity baixo
Ação recomendada: Pedir rewrite do Generator com restrição de brevidade e exemplos do que ficou ambíguo.
Registro obrigatório: `failed_gate`, `evidence`, `owner`, `next_action` e `timestamp`.

### Traceability baixo
Ação recomendada: Não bloquear cliente se output é seguro, mas abrir task de melhoria do trace antes do próximo rollout.
Registro obrigatório: `failed_gate`, `evidence`, `owner`, `next_action` e `timestamp`.

### Inter-rater reliability baixa
Ação recomendada: Pausar rollout da rubric, revisar anchors e simplificar criteria ambíguos.
Registro obrigatório: `failed_gate`, `evidence`, `owner`, `next_action` e `timestamp`.

### Evaluator discordou de regra determinística
Ação recomendada: Regra determinística vence, trace marca conflito para análise humana.
Registro obrigatório: `failed_gate`, `evidence`, `owner`, `next_action` e `timestamp`.

---

## 🔍 Trace Requirements

| Campo de trace | Por que existe |
|----------------|----------------|
| `rubric_id` | Identifica qual rubric foi aplicada. |
| `rubric_version` | Permite comparar mudanças de avaliação ao longo do tempo. |
| `input_refs` | Lista conversation_id, state_snapshot_id, catalog_snapshot_id e price_snapshot_id. |
| `output_ref` | Aponta para mensagem, JSON ou decisão avaliada. |
| `dimension_scores` | Registra score por dimension. |
| `criteria_evidence` | Mostra evidência usada para cada score importante. |
| `failed_gates` | Lista gates que falharam. |
| `decision` | Indica approve, revise, reject ou escalate. |
| `feedback_to_generator` | Traz correções específicas quando houver retry. |
| `human_override` | Registra se humano alterou decisão e por quê. |

---

## 🧑‍🏫 Como Ensinar Este Template ao Time

1. Ler o prólogo em grupo e pedir que cada pessoa identifique onde o Evaluator falhou.
2. Abrir `03-rubric-design.md` para revisar dimensions, criteria e scoring scale.
3. Escolher uma feature real do KODA que gerou dúvida na última sprint.
4. Preencher a identidade da rubric em conjunto.
5. Definir três gate criteria que jamais podem ser compensados por score alto.
6. Criar dois anchor examples aprovados e dois rejeitados.
7. Rodar uma calibration curta com três avaliadores.
8. Comparar divergências e ajustar termos vagos.
9. Anexar a rubric ao sprint contract da próxima implementação.
10. Revisar traces depois da primeira semana de uso.

---

## 🧩 Mini Rubrics Prontas Para Adaptação

### Mensagem curta de estoque
Scoring scale sugerida: 3-point scale.
Decision rule sugerida: reprovar se qualquer critério crítico receber score 1.
Criteria:
* Produto citado existe.
* Disponibilidade bate com inventory.
* Mensagem não inventa prazo.
* Próximo passo é claro.
Trace mínimo: score por critério, evidence e decisão final.

### Resumo de conversa longa
Scoring scale sugerida: 3-point scale.
Decision rule sugerida: reprovar se qualquer critério crítico receber score 1.
Criteria:
* Inclui decisões importantes.
* Preserva restrições do cliente.
* Remove ruído sem apagar contexto crítico.
* Indica incertezas.
Trace mínimo: score por critério, evidence e decisão final.

### Resposta de troca ou devolução
Scoring scale sugerida: 3-point scale.
Decision rule sugerida: reprovar se qualquer critério crítico receber score 1.
Criteria:
* Política aplicada corretamente.
* Tom empático.
* Próximo passo acionável.
* Escala exceções.
Trace mínimo: score por critério, evidence e decisão final.

### Validação de endereço
Scoring scale sugerida: 3-point scale.
Decision rule sugerida: reprovar se qualquer critério crítico receber score 1.
Criteria:
* Campos obrigatórios presentes.
* CEP compatível com cidade.
* Frete calculável.
* Não expõe dados além do necessário.
Trace mínimo: score por critério, evidence e decisão final.

### Ranking de produtos
Scoring scale sugerida: 3-point scale.
Decision rule sugerida: reprovar se qualquer critério crítico receber score 1.
Criteria:
* Todos produtos elegíveis.
* Critério de ranking explícito.
* Empate resolvido de forma estável.
* Sem favorecimento sem evidência.
Trace mínimo: score por critério, evidence e decisão final.

---

## 🎓 O Que Você Aprendeu

* Uma rubric é uma régua operacional, não uma opinião bonita.
* Dimensions definem o que medir.
* Criteria definem o que conta como bom dentro de cada dimension.
* Scoring scale define como transformar julgamento em número ou decisão.
* Gate criteria impedem que falhas críticas sejam compensadas por pontos em áreas menos importantes.
* Anchor examples ajudam humanos e Evaluators a calibrar expectativas.
* Calibration aumenta fairness, consistência e inter-rater reliability.
* Traceability transforma aprovação em decisão auditável.
* KODA precisa de rubrics diferentes para product recommendation, order processing, customer support e promotion validation.
* Este template complementa `03-rubric-design.md` ao transformar teoria em ferramenta preenchível.

### Checkpoint: Você Aprendeu?
1. Você consegue explicar a diferença entre dimension e criterion sem olhar o texto?
2. Você consegue apontar três gate criteria para uma feature de checkout?
3. Você consegue escrever uma scoring scale de 5 pontos com âncoras concretas?
4. Você consegue dizer quando usar binary scale em vez de weighted composite?
5. Você consegue calibrar uma rubric usando anchor examples?
6. Você consegue identificar bias em uma rubric que favorece mensagens longas?
7. Você consegue avaliar uma mensagem de product recommendation com evidence?
8. Você consegue avaliar um JSON de order processing sem depender de opinião?
9. Você consegue definir trace fields mínimos para auditoria?
10. Você consegue revisar uma rubric ruim e deixá-la aplicável por outro Engineer?

Se você respondeu sim para pelo menos oito perguntas, está pronto para usar este template em uma sprint real.
Se respondeu não para alguma pergunta crítica, volte ao trecho correspondente e pratique com um output real do KODA.

---

## 🚀 Próximos Passos

1. Escolha uma feature KODA com risco real de qualidade.
2. Leia o sprint contract da feature antes de escrever a rubric.
3. Copie a estrutura mestre deste arquivo.
4. Defina output avaliado, input obrigatório e contexto obrigatório.
5. Escolha dimensions com base no risco da feature.
6. Escreva criteria observáveis para cada dimension.
7. Defina gate criteria para falhas que não podem passar.
8. Escolha scoring scale e pesos.
9. Crie anchor examples aprovados, revisáveis e rejeitados.
10. Rode calibration com pelo menos dois humanos e um Evaluator.
11. Anexe a rubric ao harness ou ao documento da sprint.
12. Revise traces reais após rollout.

---

## 📚 Referências Internas

* `curriculum/02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md` para entender separação entre Generator e Evaluator.
* `curriculum/02-nivel-2-practical-patterns/02-sprint-contracts.md` para conectar rubric a contrato de execução.
* `curriculum/02-nivel-2-practical-patterns/03-rubric-design.md` para teoria completa de rubrics.
* `curriculum/02-nivel-2-practical-patterns/04-trace-reading.md` para auditar decisões depois da avaliação.
* `curriculum/02-nivel-2-practical-patterns/koda-applications/nivel-2-koda.md` para ver os padrões aplicados ao KODA.

---

## 📄 Metadata

| Campo | Valor |
|-------|-------|
| **Arquivo** | evaluation-rubric-template.md |
| **Nível** | 8 - Tools & Templates |
| **Tempo** | 120 minutos |
| **Status** | ✅ Completo |
| **Atualizado** | Maio 2026 |
