---
title: "Exercicio 1: Implementar Feature de Recomendacao KODA com Generator/Evaluator"
type: curriculum-exercise
nivel: 4
aliases: []
tags: [curriculo-conteudo, nivel-4, exercicio]
last_updated: 2026-06-10
---
# 🎯 Exercicio 1: Implementar Feature de Recomendacao KODA com Generator/Evaluator
## Nivel 4 — KODA-Especifico — Real-World Feature

**Tempo Estimado:** 90-120 minutos
**Dificuldade:** ⭐⭐⭐⭐ (Avancado)
**Pre-requisito:** Ter completado Nivel 2 (`01-generator-evaluator-pattern.md`, `02-sprint-contracts.md`, `03-rubric-design.md`)
**Objetivo:** Implementar uma feature real do KODA — recomendacao de produto com o padrao Generator/Evaluator — incluindo contrato de feature, rubricas de avaliacao e testes de qualidade

---

## 📖 Prologo: A Feature que Nao Pode Falhar

Voce faz parte do time de engenharia do KODA. O Product Manager acabou de aprovar uma nova feature: **Smart Product Recommendation**.

O KODA atualmente recomenda produtos de forma simples — consulta o catalogo, encontra o mais barato que atende a categoria, e envia. Funciona, mas tem taxa de devolucao de 12% e satisfacao de apenas 68%.

A nova feature promete:

> "KODA analisa o perfil completo do cliente (restricoes alimentares, preferencias, orcamento, historico de compras, objetivo de treino) e recomenda ate 3 produtos ordenados por adequacao, com justificativa clara e verificacao de qualidade antes de enviar ao cliente."

A meta:
- Precisao de recomendacao: 75% → **95%+**
- Taxa de devolucao: 12% → **5%**
- Satisfacao do cliente: 68% → **88%+**

Mas voce sabe que nao basta "pedir para a IA recomendar". Voce precisa de uma arquitetura com Generator/Evaluator, contratos claros, rubricas de qualidade e testes que provem que a feature funciona.

---

## 🎯 O Que Voce Precisa Implementar

### 1. Feature Contract (Contrato da Feature)

Antes de escrever codigo, defina o contrato da feature. O que ela promete entregar? Quais sao as entradas, saidas e garantias?

O contrato deve responder a estas perguntas:
- **Input:** O que o Generator recebe? (perfil do cliente, mensagem, catalogo)
- **Output:** O que e entregue ao cliente? (produtos ranqueados, explicacao)
- **Garantias:** O que SEMPRE sera verdade sobre o output? (respeita restricoes, nao excede orcamento, etc.)
- **Limites:** Quantas recomendacoes? Qual o tamanho maximo da resposta?

Use o template de Sprint Contract que voce aprendeu no Nivel 2.

### 2. Generator Agent (Agente Gerador)

Implemente o `generator_agent()` que recebe o perfil do cliente e o catalogo de produtos e gera recomendacoes candidatas.

O Generator deve:
- Filtrar produtos que atendem restricoes alimentares (lactose, gluten, vegano)
- Respeitar limite de orcamento
- Priorizar sabor preferido quando possivel
- Ranquear por qualidade (rating) dentro dos filtros
- Gerar resposta em formato WhatsApp (curta, humana, util)
- Registrar suposicoes explicitamente
- **NAO se auto-avaliar**

### 3. Evaluator Agent (Agente Avaliador)

Implemente o `evaluator_agent()` que recebe as recomendacoes do Generator e valida contra a rubrica de qualidade.

O Evaluator deve verificar:
- **Restricoes:** Nenhum produto recomendado viola restricao alimentar do cliente
- **Orcamento:** Nenhum produto excede orcamento maximo
- **Estoque:** Produtos recomendados estao em estoque (nao inventar disponibilidade)
- **Coerencia:** Resposta e coerente com o perfil do cliente
- **Qualidade de tom:** Resposta nao pressiona compra, mantem tom humano
- **Contrato:** Output respeita o feature contract

Cada criterio deve ser verificado separadamente com evidencias registradas.

### 4. Feature Orchestrator (Orquestrador)

Implemente o harness que conecta Generator e Evaluator:

```
Cliente envia mensagem
  → Generator cria recomendacoes
    → Evaluator valida
      → Se APROVADO: envia para cliente
      → Se REJEITADO: feedback → Generator tenta novamente (max 2 revisoes)
        → Se ainda rejeitado apos 2 revisoes: fallback seguro
```

### 5. Testes de Qualidade

Escreva testes que validem:

- `test_recomendacao_caminho_feliz` — perfil tipico, recomendacao aprovada
- `test_respeita_orcamento` — nunca recomenda produto fora do orcamento
- `test_respeita_restricao_lactose` — nunca recomenda produto com lactose para cliente intolerante
- `test_respeita_restricao_gluten` — nunca recomenda produto com gluten para cliente celiaco
- `test_fallback_sem_produtos` — fallback seguro quando nenhum produto atende
- `test_prioriza_sabor_preferido` — prioriza sabor declarado pelo cliente
- `test_audit_trail` — todos os arquivos JSON tem campos obrigatorios
- `test_feature_contract` — output do Generator respeita o feature contract

---

## 📋 Requisitos Tecnicos

### Formato de Entrega

Sua solucao deve ser entregue em um arquivo Python executavel que, ao rodar `python exercise-01-solution.py`, execute todos os testes e mostre `✅ TODOS OS TESTES PASSARAM!`.

### Estrutura de Dados

Use o catalogo de produtos simulado abaixo:

```python
PRODUCT_CATALOG = [
    Product(sku="WHEY-CONC-CHOC-1000", name="Whey Concentrado Chocolate 1kg", category="whey", price_brl=89.90, servings=30, lactose_free=False, gluten_free=True, in_stock=True, rating=4.5),
    Product(sku="WHEY-ISO-CHOC-900", name="Whey Isolado Chocolate 900g", category="whey", price_brl=139.90, servings=27, lactose_free=True, gluten_free=True, in_stock=True, rating=4.7),
    Product(sku="WHEY-VEG-BAUN-750", name="Proteina Vegetal Baunilha 750g", category="whey_vegano", price_brl=99.90, servings=25, lactose_free=True, gluten_free=True, in_stock=True, rating=4.3),
    Product(sku="PROT-VEG-CHOC-750", name="Proteina Vegetal Chocolate 750g", category="whey_vegano", price_brl=119.90, servings=25, lactose_free=True, gluten_free=True, in_stock=True, rating=4.6),
    Product(sku="CREA-MONO-300", name="Creatina Monohidratada 300g", category="creatina", price_brl=69.90, servings=60, lactose_free=True, gluten_free=True, in_stock=True, rating=4.8),
    Product(sku="CREA-MICRO-250", name="Creatina Micronizada 250g", category="creatina", price_brl=74.90, servings=50, lactose_free=True, gluten_free=True, in_stock=True, rating=4.6),
    Product(sku="PRE-TREINO-CAFE-300", name="Pre-Treino Cafeina 300g", category="pre_treino", price_brl=79.90, servings=30, lactose_free=True, gluten_free=True, in_stock=False, rating=4.4),
    Product(sku="BCAA-PO-200", name="BCAA em Po 200g", category="bcaa", price_brl=59.90, servings=40, lactose_free=True, gluten_free=True, in_stock=True, rating=4.1),
]
```

### O que NAO fazer

- ❌ Nao use chamadas LLM reais (use heuristica para manter deterministico e testavel)
- ❌ Nao invente estoque ou disponibilidade
- ❌ Nao use `as any`, `@ts-ignore`, ou equivalentes
- ❌ Nao deixe criterios de avaliacao vagos ("resposta boa")
- ❌ Nao misture responsabilidades de Generator e Evaluator no mesmo agente

---

## 🏆 Criterios de Aceitacao

Sua solucao sera considerada completa quando:

- [ ] `python exercise-01-solution.py` executa sem erros
- [ ] Todos os 8 cenarios de teste passam
- [ ] Generator nao avalia o proprio trabalho (separacao clara)
- [ ] Evaluator registra evidencias para cada criterio reprovado
- [ ] Feature contract esta documentado e o codigo o respeita
- [ ] Fallback seguro funciona quando nenhum produto atende
- [ ] Codigo e legivel, com funcoes pequenas e responsabilidades unicas

---

## 📚 Material de Referencia

Antes de comecar, revise:
- `02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md` — o padrao em detalhes
- `02-nivel-2-practical-patterns/02-sprint-contracts.md` — como escrever contratos
- `02-nivel-2-practical-patterns/03-rubric-design.md` — como criar rubricas de qualidade
- `04-nivel-4-koda-specific/03-feature-design-patterns.md` — como features KODA sao desenhadas

---

**Voce ja sabe o que fazer. O KODA confia em voce. Implemente com qualidade.**
