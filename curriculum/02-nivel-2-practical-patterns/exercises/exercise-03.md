---
title: "Exercício 3: Handle Failure Scenarios"
type: curriculum-exercise
nivel: 2
aliases: []
tags: [curriculo-conteudo, nivel-2, exercicio]
last_updated: 2026-06-10
---
# ⚠️ Exercício 3: Handle Failure Scenarios
## Nível 2 - Padrões Práticos

**Tempo Estimado:** 45-60 minutos  
**Dificuldade:** ⭐⭐⭐⭐ (Avançado)  
**Pré-requisito:** Ter completado Exercício 1 + 2  
**Objetivo:** Simular falhas reais e descrever como Contract + Harness lidam com elas

---

## 🎯 O Contexto

Você tem:
- ✅ Sprint Contract (Exercício 1) — Define "pronto"
- ✅ Harness (Exercício 2) — Força sequência segura

Agora: **O que acontece quando as coisas dão errado?**

Você vai simular 3 cenários reais de falha e descrever como sistema responde.

---

## 📝 Sua Tarefa

Escolha **3 failure scenarios** do mundo real do KODA e descreva:

1. **O que falha** (situação específica)
2. **Em qual passo do Harness detecta** (Passo 1? 2? 3?)
3. **O que o Harness faz** (ação imediata)
4. **Como o Contract ajuda** (evita disaster)
5. **Como KODA comunica ao cliente** (transparência)
6. **Resultado final** (sucesso parcial, refazimento, escala?)

### Template para Cada Cenário:

```
═══════════════════════════════════════════════════════
FAILURE SCENARIO #N: [Nome Descritivo]
═══════════════════════════════════════════════════════

🎬 O CENÁRIO:
[Descreva a situação específica que causa falha]

❌ O QUE FALHA:
[Qual é a falha exata? Qual condição fica FALSE?]

🔍 ONDE DETECTA (No Harness):
[Em qual passo do Harness isso é detectado?
 Ex: "PASSO 2: CHECK AVAILABILITY - Falha na validação"]

⚡ AÇÃO IMEDIATA (Do Harness):
[O que Harness faz imediatamente?
 Ex: "Remove produto de estoque fora, substitui com 4º"]

💬 COMO COMUNICA (Com Cliente):
[Exatamente o que KODA diz ao cliente?]

📋 COMO CONTRACT AJUDA:
[Como o Contract do Exercício 1 evita disaster?
 Ex: "Success Criteria diz 3 produtos, não 2.
      Se tentar com 2, Contract rejeitaria"]

✅ RESULTADO FINAL:
[O que acontece? Sucesso? Refazimento? Escala?
 Ex: "Sucesso com produto substituído"
     ou "Refazimento (2ª tentativa)"
     ou "Escalado para humano"]

IMPACTO PARA CLIENTE:
[Como cliente se sente? Segurança? Confusão?]
```

---

## 🎓 Cenários Potenciais

Escolha 3 destes (ou crie seus próprios):

### Opção A: Alergia Problema
```
Cliente é intolerante a lactose.
Um dos 3 produtos comparados TEM LACTOSE.
(Dados de Discover estavam desatualizados)
```

### Opção B: Produto Saiu do Estoque
```
Cliente viu 5 opções em Discover (15 minutos atrás).
Agora em Comparison, 1 deles já saiu do estoque.
(Estoque em tempo real mudou)
```

### Opção C: Preço Mudou
```
Cliente viu Whey por R$ 89 em Discover.
Agora em Comparison, preço subiu para R$ 95.
(Promoção expirou nos últimos 10 minutos)
```

### Opção D: Cliente Muda de Ideia
```
Contract diz: "Compare 3 produtos"
Cliente: "Ah, na verdade quero comparar 5"
```

### Opção E: Análise Fica Muito Complexa
```
Harness tenta comparar 3 produtos em 5 dimensões cada.
Resultado: Texto gigante e confuso.
Cliente não consegue entender.
```

### Opção F: Avaliações Desatualizadas
```
Um produto tinha 4.8 stars em Discover.
Agora em Comparison, é 3.2 stars (clientes deixaram reviews ruins).
```

### Opção G: Não Tem 3 Produtos Válidos
```
Cliente quer Whey, sem lactose, R$ 50.
Harness filtra: acha só 1 opção válida.
Impossível comparar 3.
```

---

## ✍️ Como Responder

### Exemplo Completo: Failure Scenario - Alergia Problema

```
═══════════════════════════════════════════════════════
FAILURE SCENARIO #1: Alergia Descoberta No Último Minuto
═══════════════════════════════════════════════════════

🎬 O CENÁRIO:
Cliente é intolerante a lactose. Em Discover (há 10 minutos),
KODA recomendou 5 opções com rótulo "sem lactose".
Agora em Comparison, Cliente quer comparar Whey Isolado vs Whey Vegano.

No meio da análise, descobre-se que os dados de Discover estavam desatualizados.
Whey Isolado agora TEM LACTOSE (fabricante mudou fórmula ontem).

❌ O QUE FALHA:
Validação "Whey Isolado TEM LACTOSE?" == TRUE
Esperado: FALSE
Isso viola o Harness: "PASSO 1: VALIDATE RESTRICTIONS"

🔍 ONDE DETECTA:
PASSO 1 do Harness: VALIDATE RESTRICTIONS
├─ Validação: "Este produto TEM {cliente.alergia}?" == FALSE
├─ Resultado: Whey Isolado TEM LACTOSE
└─ FALHA DETECTADA!

⚡ AÇÃO IMEDIATA:
Harness para imediatamente (não continua para Passo 2, 3, 4, 5).
Remove Whey Isolado da lista de comparação.
Substitui com 4º melhor produto (Whey Concentrado).
Refaz análise com 3 produtos válidos.

💬 COMO COMUNICA:
KODA: "Espera! Detectei que Whey Isolado foi reformulado e agora tem lactose.
        Você é intolerante, então vou substituir por Whey Concentrado.
        Deixa eu refazer a comparação com produtos 100% seguros para você."

📋 COMO CONTRACT AJUDA:
CONTRACT especifica no FAILURE HANDLING:
"Se alergia falha: Rejeitar análise, refazer com produtos válidos"

Sem contract, KODA poderia:
❌ Continuar com 2 produtos (violaria critério "3-5 opções")
❌ Forçar Whey Isolado mesmo com alergia (risco!)
❌ Não comunicar (cliente fica confuso)

COM CONTRACT:
✅ Rejeita análise errada
✅ Refaz com produtos válidos
✅ Mantém 3 opções

✅ RESULTADO FINAL:
Refazimento (2ª tentativa)
├─ Passo 1: Whey Vegano (SEM lactose) ✓
├─ Passo 1: Whey Concentrado (SEM lactose) ✓
├─ Passo 1: BCAA (SEM lactose) ✓
└─ Passo 2-5: Análise procede normalmente

IMPACTO PARA CLIENTE:
✅ Segurança: Nunca sofre reação alérgica
✅ Confiança: KODA "cuida" dele, detecta problema
✅ Sem fricção: Refazimento é transparente
✅ Satisfação: +1 para "KODA é confiável"
```

---

## 🔍 Como Avaliar Sua Resposta

### ✅ Bom Failure Scenario tem:

- [ ] Cenário específico (não genérico)
- [ ] Descreve exatamente qual condição falha
- [ ] Identifica em qual Passo do Harness detecta
- [ ] Ação do Harness é clara e imediata
- [ ] Comunicação é específica (não vaga)
- [ ] Explica como Contract evita disaster
- [ ] Resultado é realista
- [ ] Impacto para cliente é claro

### ❌ Ruim Failure Scenario tem:

- ❌ Genérico ("algo dá errado")
- ❌ Não especifica o que falha
- ❌ Não identifica passo Harness
- ❌ Ação vaga ("refazer")
- ❌ Comunicação vaga
- ❌ Não menciona Contract
- ❌ Resultado vago

---

## 💡 Análise Mais Profunda

Quando descrever cada cenário, responda também:

**1. Frequência:** Isso é comum ou raro?
```
COMUM: Estoque muda a cada minuto
RARO: Alergia descobre no último minuto
```

**2. Severidade:** Qual é o dano se não detectar?
```
CRÍTICA: Cliente sofre reação alérgica (saúde)
MÉDIA: Cliente fica confuso (frustração)
BAIXA: Cliente vê análise menos boa (satisfação)
```

**3. Custo de Detecção:** Quanto custa validar?
```
BARATO: 1 query de estoque (+50 tokens)
CARO: Re-validar alergia em BD (+500 tokens)
GRATUITO: Já temos info em memória
```

**4. Alternativa sem Harness:** O que acontecia antes?
```
SEM HARNESS: 60% de chance Cliente sofria reação
COM HARNESS: 0% de chance (Passo 1 bloqueia)
```

---

## 🎓 Dúvidas Comuns

**P: Preciso escolher exatamente os 3 do menu acima?**  
R: Não! Escolha ou crie seus próprios. O importante é que sejam REAIS.

**P: E se um cenário envolve múltiplas falhas?**  
R: Tudo bem! Descreva em ordem como Harness detecta/lida com cada uma.
```
Exemplo:
1. Alergia falha em Passo 1
2. Estoque falha em Passo 2
3. Preço é ok
→ Qual detecta primeiro? Passo 1 (alergia)
   Harness pára lá, refaz.
```

**P: Meu cenário é muito simples/complexo?**  
R: Sem problema! Simples é fácil entender. Complexo testa compreensão profunda.

---

## 📊 Rubric de Avaliação

| Aspecto | Ruim (0-2) | Ok (3-5) | Bom (6-8) | Excelente (9-10) |
|---------|-----------|---------|-----------|-----------------|
| **Especificidade** | Genérico | Parcial | Específico | Muito específico |
| **Detecção** | Vaga | Mencionado | Passo claro | Passo + validação |
| **Ação** | Nenhuma | Vaga | Clara | Muito clara |
| **Comunicação** | Nenhuma | Genérica | Específica | Diálogo real |
| **Contract** | Não menciona | Menciona | Explica | Conecta tudo |
| **Resultado** | Vago | Ok | Claro | Muito claro |
| **Impacto Cliente** | Não trata | Mencionado | Claro | Muito claro |

**Sua nota por cenário:** Some e divida por 7.  
**Nota final:** Média dos 3 cenários.

---

## 🎁 Bônus: Implementar Failure Handling

Se quiser bonus points, implemente o failure handling em pseudo-código:

```python
def harness_product_comparison_with_failures(products, restrictions):
    """
    Harness com tratamento de falhas
    """
    
    try:
        # PASSO 1: VALIDATE RESTRICTIONS
        valid_products = []
        for product in products:
            if not product.has_restriction(restrictions):
                valid_products.append(product)
        
        if len(valid_products) < 3:
            # FAILURE HANDLING: Menos de 3 válidos
            log("FAILURE: Menos de 3 produtos sem alergia")
            return FAILURE_ACTION_1("Informar cliente, oferecer alternativa")
        
        # PASSO 2: CHECK AVAILABILITY
        available_products = []
        for product in valid_products[:3]:
            if product.stock > 0:
                available_products.append(product)
        
        if len(available_products) < 3:
            # FAILURE HANDLING: Estoque insuficiente
            log("FAILURE: Menos de 3 em estoque")
            substitute = find_4th_best_product()
            available_products.append(substitute)
        
        # Continue com PASSO 3, 4, 5...
        # Similar structure para cada possível falha
        
    except Exception as e:
        log(f"FAILURE: {e}")
        return ESCALATE_TO_HUMAN()
```

---

## 🎯 Próxima Etapa

Depois de completar este exercício:
1. Você completou todos os 3 exercícios! 🎉
2. Próximo: Implemente em KODA real
3. Meça impacto (antes/depois)

---

## ✍️ Entrega

Quando terminar, você deve ter:
- [ ] 3 Failure Scenarios descritos completamente
- [ ] Cada um com O QUÊ/ONDE/AÇÃO/COMUNICAÇÃO/CONTRACT/RESULTADO
- [ ] Específicos e realistas (não genéricos)
- [ ] (Bônus) Pseudo-código do failure handling

**Tempo:** 45-60 minutos  
**Pronto para:** Implementação real no KODA

---

## 🏆 Você Completou os 3 Exercícios!

Parabéns! Você agora pode:

✅ **Exercício 1:** Desenhar um Sprint Contract  
✅ **Exercício 2:** Desenhar um Harness que o garante  
✅ **Exercício 3:** Simular e lidar com falhas reais  

**Próximo:** Implemente isso no KODA e meça o impacto!

---

*Exercício 3 | Nível 2 - Padrões Práticos*

**Você é um expert em Sprint Contracts! 🚀**
