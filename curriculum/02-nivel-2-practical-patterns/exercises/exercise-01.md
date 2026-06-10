---
title: "Exercício 1: Design a Sprint Contract"
type: curriculum-exercise
nivel: 2
aliases: []
tags: [curriculo-conteudo, nivel-2, exercicio, sprint-contract, contract-design, success-criteria, failure-handling, input-specification, product-comparison, koda-scenario, exercicio-conceitual]
relates-to: ["[[curriculum/02-nivel-2-practical-patterns/01-generator-evaluator-pattern|Generator/Evaluator Pattern]]"]
last_updated: 2026-06-10
---
# 📋 Exercício 1: Design a Sprint Contract
## Nível 2 - Padrões Práticos

**Tempo Estimado:** 30-45 minutos  
**Dificuldade:** ⭐⭐ (Intermediário)  
**Pré-requisito:** Ter lido `02-sprint-contracts.md`  
**Objetivo:** Desenhar um Sprint Contract funcional para um cenário KODA real

---

## 🎯 O Cenário

Você está redesenhando o KODA com Sprint Contracts. O primeiro passo é criar um contract para o sprint **"Product Comparison"**.

### Contexto:

Cliente acabou de receber 5 opções de produtos (do Discover Sprint). Agora quer comparar 3 delas para decidir qual comprar.

```
CLIENTE: "Ok, você me mostrou 5 wheys. Qual é o melhor?"
KODA: "Deixa eu comparar os 3 melhores para você decidir."
```

Esse é o **Product Comparison Sprint**.

---

## 📝 Sua Tarefa

Desenhe um **Sprint Contract completo** para o "Product Comparison" sprint.

Use este template:

```
╔═══════════════════════════════════════════════════════╗
║        SPRINT CONTRACT: [Nome do Sprint]             ║
╠═══════════════════════════════════════════════════════╣
║ GERADOR: [Quem executa]                             ║
║ AVALIADOR: [Quem valida]                            ║
║ DURAÇÃO: [Tempo máximo]                             ║
╠═══════════════════════════════════════════════════════╣
║ 📥 INPUT SPECIFICATION                              ║
║ • [Dado 1]                                          ║
║ • [Dado 2]                                          ║
║ • [Dado 3]                                          ║
╠═══════════════════════════════════════════════════════╣
║ ✅ SUCCESS CRITERIA (TODOS devem passar)             ║
║ • [Critério 1 - testável]                           ║
║ • [Critério 2 - testável]                           ║
║ • [Critério 3 - testável]                           ║
╠═══════════════════════════════════════════════════════╣
║ ⚠️ FAILURE HANDLING                                  ║
║ Se [Situação 1] → [Ação 1]                          ║
║ Se [Situação 2] → [Ação 2]                          ║
║ Se [Situação 3] → [Ação 3]                          ║
╚═══════════════════════════════════════════════════════╝
```

---

## 🤔 Dicas para Pensar

### Para INPUT SPECIFICATION, pergunte a si mesmo:

1. **O que o Client vai fornecer?**
   - 5 produtos já foram encontrados (vêm do Discover Sprint)
   - Cliente tem informações como: orçamento, alergia, preferência

2. **Que contexto está disponível?**
   - Histórico da conversa (alergia, preferências)
   - Dados dos 5 produtos (preço, avaliação, ingredients)

3. **Há limites?**
   - Quanto tempo pode gastar? (30 min de conversa é muito)
   - Quantos tokens pode usar?

---

### Para SUCCESS CRITERIA, pergunte a si mesmo:

1. **Quando você sabe que a comparação foi "boa"?**
   - Só 3 produtos comparados? (não 5)
   - Cada um tem uma dimensão diferente? (preço vs quality vs speed)
   - Cliente conseguiu tomar decisão?

2. **Como você testa se foi sucesso?**
   - "Cliente gostou" é vago. Não é testável.
   - "3 produtos ranqueados por critério X" é testável.

3. **Qual é o padrão de qualidade?**
   - Explicação deve ser clara (e.g., >50 caracteres)
   - Análise deve cobrir 3 dimensões (preço, qualidade, velocidade)

---

### Para FAILURE HANDLING, pergunte a si mesmo:

1. **O que pode dar errado?**
   - Cliente muda de ideia (quer comparar BCAA, não Whey)
   - Um produto saiu do estoque
   - Cliente quer comparar 5 produtos (não 3)

2. **Para cada problema, qual é a ação?**
   - Se cliente muda: Novo contract? Novo sprint?
   - Se saiu estoque: Oferecer alternativa? Voltar para Discover?
   - Se quer 5: Aceitar (mudar contract) ou recusar (manter em 3)?

3. **Há um máximo de tentativas?**
   - Comparação toma tempo. Se falhar 3x, escalar para humano?

---

## ✍️ Como Responder

Escreva seu contract na forma visual (com os boxes) OU em formato texto estruturado.

**Exemplo de resposta bom:**

```
╔═══════════════════════════════════════════════════════╗
║    SPRINT CONTRACT: Product Comparison               ║
╠═══════════════════════════════════════════════════════╣
║ GERADOR: KODA (agent que compara)                   ║
║ AVALIADOR: Quality Gate (valida análise)            ║
║ DURAÇÃO: 15 minutos máximo                          ║
╠═══════════════════════════════════════════════════════╣
║ 📥 INPUT SPECIFICATION                              ║
║ • 5 produtos encontrados (do Discover Sprint)       ║
║ • Cliente especificou: orçamento, restrições        ║
║ • Histórico: alergia/preferência (herdado)          ║
║ • Contexto: Avaliações de clientes, preços atuais  ║
╠═══════════════════════════════════════════════════════╣
║ ✅ SUCCESS CRITERIA                                  ║
║ • EXATAMENTE 3 produtos comparados (não 5, não 2)  ║
║ • Cada produto tem rank (1º, 2º, 3º) claro         ║
║ • Cada análise tem 3 dimensões (preço, qual, vel)  ║
║ • Cada dimensão tem explicação ≥50 caracteres      ║
║ • Recomendação top 1 é clara (por quê é melhor)   ║
╠═══════════════════════════════════════════════════════╣
║ ⚠️ FAILURE HANDLING                                  ║
║ Se cliente quer comparar 5 (não 3):                 ║
║ → "Ok, mas vou comparar os 3 melhores primeiro"    ║
║                                                      ║
║ Se cliente muda tipo (Whey → BCAA):                ║
║ → Rejeitar contract, novo Discover Sprint          ║
║                                                      ║
║ Se 1 produto saiu estoque:                         ║
║ → Oferecer 4º melhor produto como substituição    ║
║                                                      ║
║ Se análise fica vaga/confusa:                       ║
║ → Refazer comparação (máx 2 tentativas)            ║
╚═══════════════════════════════════════════════════════╝
```

---

## 🔍 Como Avaliar Sua Resposta

### ✅ Bom Contract tem:

- [ ] INPUT especifica dados que vão entrar (não é vago)
- [ ] CRITERIA são todos testáveis (têm operadores: ==, >, NOT IN)
- [ ] CRITERIA não são rígidos demais (faixas, não exatos únicos)
- [ ] FAILURE tem 3+ cenários específicos
- [ ] FAILURE tem ação clara para cada cenário
- [ ] Contract é realista (não pede o impossível)

### ❌ Ruim Contract tem:

- ❌ INPUT vago ("contexto do cliente")
- ❌ CRITERIA subjetivo ("análise é boa")
- ❌ CRITERIA rígido demais ("EXATAMENTE 3.000 caracteres")
- ❌ FAILURE vago ("se algo der errado")
- ❌ FAILURE sem ação ("não sei o que fazer")
- ❌ Contract impossível de cumprir

---

## 🎓 Dúvidas Comuns

**P: Quantos critérios de sucesso devo ter?**  
R: 4-7 critérios são ideais. Menos é arriscado, mais é confuso.

**P: Preciso ser específico nos números (e.g., "50 caracteres")?**  
R: Sim! Números específicos são testáveis. "Explicação clara" é vago.

**P: E se meu contract tiver 10 linhas de Failure Handling?**  
R: Tudo bem! Quanto mais específico, melhor. Mas se tem 10+, talvez seja muito rígido.

**P: Posso deixar "DURAÇÃO" como "quanto tempo precisar"?**  
R: Não. Sempre coloque um máximo (15 min, 30 min). Protege contra loops infinitos.

---

## 📊 Rubric de Avaliação

Avalie sua resposta com esta escala:

| Aspecto | Ruim (0-2) | Ok (3-5) | Bom (6-8) | Excelente (9-10) |
|---------|-----------|---------|-----------|-----------------|
| **INPUT** | Vago | Genérico | Específico | Muito específico |
| **CRITERIA** | Subjetivo | Parcial | Testável | Totalmente testável |
| **FAILURE** | Nenhum | 1-2 | 3+ | 5+, específico |
| **Realismo** | Impossível | Difícil | Possível | Realista |
| **Estrutura** | Confuso | Ok | Claro | Muito claro |

**Sua nota:** Some os pontos, máximo 50. Divida por 5 para nota 0-10.

---

## 💡 Próxima Etapa

Depois de completar este exercício:
1. Revise seu contract com um colega (feedback)
2. Vá para **Exercício 2: Build a Harness** — desenhar os passos que acompanham este contract
3. Depois: **Exercício 3: Handle Failure Scenarios** — simular o que acontece quando algo falha

---

## 🎯 Entrega

Quando terminar, você deve ter:
- [ ] 1 Sprint Contract completo (Input + Criteria + Failure)
- [ ] Na forma visual (box) OU texto estruturado
- [ ] Validado contra rubric acima
- [ ] Pronto para compartilhar com time

**Tempo:** 30-45 minutos  
**Próximo:** exercise-02_-_02-nivel-2-practical-patterns.md

---

*Exercício 1 | Nível 2 - Padrões Práticos*

**Boa sorte! Este é o primeiro passo para implementar Sprint Contracts no KODA.** 🚀
