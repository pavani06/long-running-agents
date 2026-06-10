---
title: "Estudo de Caso 3 (KODA): Product Discovery"
type: curriculum-case-study
aliases: []
tags: [curriculo-conteudo, caso-de-estudo, recomendacao-de-produtos, validacao-de-recomendacoes, inventario-em-tempo-real, whatsapp, avaliacao-com-rubrica]
last_updated: 2026-06-10
---
# Estudo de Caso 3 (KODA): Product Discovery

**Nível de Complexidade:** Nível 2–3  
**Foco:** Generator/Evaluator para qualidade de recomendação  
**Contexto:** Vendas via WhatsApp de suplementos esportivos

---

## Problema

O KODA precisa recomendar produtos que simultaneamente:

1. Correspondam à necessidade real do cliente  
2. Estejam em estoque no momento da conversa  
3. Ofereçam valor genuíno (preço, promoção, adequação)  
4. Sejam apresentados com clareza e persuasão

**Cenário real:** Cliente envia no WhatsApp: *"Estou treinando para uma maratona e preciso de nutrição"*

Com um agente único, 25% das recomendações tinham algum problema — produto fora de estoque, preço desatualizado, ou escolha inadequada para o nível do atleta.

---

## Solução: Generator/Evaluator com Rubrica

GENERATOR (Recomendador de Produtos)

│

├─ Input: Contexto do cliente (treino de maratona)

├─ Processo:

│   ├─ Consulta base de produtos via API

│   ├─ Filtra por categoria (nutrição esportiva)

│   ├─ Cruza com nível do cliente (amador/avançado)

│   ├─ Verifica estoque em tempo real

│   └─ Aplica promoções ativas do clube

│

├─ Output: 3 recomendações estruturadas

│   Exemplo: "Mix de carbo-loading \- 5kg \- R$175 (era R$250)"

│            "Gel energético isotônico \- pack 24 \- R$89"

│            "Proteína de recuperação \- 2kg \- R$199"

│

└─ Sem verificação própria — confia no Evaluator

EVALUATOR (QA de Recomendações)

│

├─ Verifica cada recomendação do Generator:

│   ├─ Produto existe? (valida SKU na base)

│   ├─ Preço correto? (checa promoção em tempo real)

│   ├─ Em estoque? (confirma inventário atual)

│   ├─ Relevante para o objetivo? (avalia coerência)

│   └─ O cliente ficaria satisfeito? (assessment de valor)

│

├─ Rubrica de avaliação:

│   ├─ Relevância para o objetivo: 8/10 ✓

│   ├─ Valor percebido do preço: 9/10 ✓

│   ├─ Clareza da explicação: 7/10 (pode melhorar)

│   └─ Score geral: 8/10 → Aprovado

│

└─ Se problema encontrado: Devolve ao Generator com feedback específico

SPRINT CONTRACT

"O Generator recomendará produtos que:

  1\. Apoiem diretamente o objetivo declarado

  2\. Estejam em estoque agora (verificação ao vivo)

  3\. Tenham preço com margem de ±5% do valor promocional atual

  4\. Incluam explicação clara do motivo da recomendação

  

  O Evaluator verificará os 4 critérios antes de aprovar.

  Itens reprovados retornam ao Generator com feedback específico."

---

## Arquitetura de Dados

recommendation-state/

│

├── customer\_context.json

│   {

│     "customer\_id": "wa\_5511999999999",

│     "goal": "marathon\_training",

│     "level": "intermediate",

│     "club\_member": true,

│     "purchase\_history": \["whey\_protein", "creatine"\]

│   }

│

├── generator\_draft.json

│   {

│     "recommendations": \[

│       {

│         "sku": "CARBO-001",

│         "name": "Mix Carbo-Loading 5kg",

│         "price": 175.00,

│         "promo\_price": 175.00,

│         "rationale": "Alta densidade energética para long runs"

│       }

│     \],

│     "draft\_timestamp": "2026-05-23T10:30:00Z"

│   }

│

└── evaluator\_verdict.json

    {

      "verdict": "approved",

      "scores": {"relevance": 8, "price": 9, "clarity": 7},

      "overall": 8,

      "notes": "Aumentar explicação sobre timing de consumo"

    }

---

## Resultados

ANTES (Agente Único):

├─ Tempo de resposta: 2–5 minutos

├─ Precisão: 75% (às vezes estoque errado)

├─ Qualidade: Variada (algumas recomendações mediocres)

└─ Satisfação do cliente: 70%

DEPOIS (Generator/Evaluator):

├─ Tempo de resposta: 3–5 minutos (overhead pequeno)

├─ Precisão: 98% (Evaluator captura problemas)

├─ Qualidade: 92% (rubrica garante padrão)

└─ Satisfação do cliente: 88%

---

## Métricas de Impacto

Melhorias operacionais:

├─ Precisão de estoque: 75% → 98%

├─ Recomendações erradas: 20% → 2%

├─ Satisfação do cliente: 70% → 88%

├─ Taxa de recompra: 35% → 52%

└─ Taxa de devolução: 15% → 6%

Impacto financeiro:

├─ Custo adicional: \+15% (2 chamadas de API ao invés de 1\)

├─ Latência adicionada: \+1–2 segundos

├─ Impacto na receita: \+52% recompras \= \+30% receita

└─ ROI: 2x custo → 30x benefício

O trade-off é claro: pagar 15% a mais em custo de modelo para obter 30x de retorno em receita recorrente.

---

## Padrões-Chave Utilizados

1. **Generator/Evaluator:** Separação entre geração e verificação de qualidade  
2. **Rubric Design:** Grades objetivos e subjetivos com pesos claros  
3. **Sprint Contracts:** Define explicitamente o que "boa recomendação" significa  
4. **Trace Reading:** Debug estruturado quando recomendações falham  
5. **Real-time Verification:** Evaluator sempre consulta inventário ao vivo

---

## Lições Aprendidas

1. **Separação funciona:** O Evaluator captura erros que o Generator ignora  
2. **Rubricas habilitam escala:** Critérios claros \= qualidade consistente sem supervisão humana  
3. **Pequeno custo, grande benefício:** \+15% custo → \+30% receita  
4. **Confiança via verificação:** Clientes confiam em recomendações verificadas  
5. **Padrões são universais:** O mesmo padrão Generator/Evaluator serve para múltiplas features

---

---

