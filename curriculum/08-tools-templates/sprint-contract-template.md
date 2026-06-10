---
title: "Sprint Contract Template"
type: curriculum-template
aliases: ["template sprint", "modelo contrato", "sprint template", "contrato agentes"]
tags: [curriculo-conteudo, template, contratos-de-sprint, acordo-entre-agentes, criterios-de-aceitacao, especificacao-de-entrada, gestao-de-risco, validacao-multietapas]
relates-to: ["[[curriculum/05-core-concepts/04-sprint-contracts|Sprint Contracts]]", "[[curriculum/02-nivel-2-practical-patterns/02-sprint-contracts|Sprint Contracts Lesson]]"]
last_updated: 2026-06-10
---
# 📋 Sprint Contract Template
## Template Completo para Contratos Entre Generator e Evaluator no KODA

**Tempo Estimado:** 120-150 minutos  
**Nível:** 2 - Padrões Práticos / 8 - Tools & Templates  
**Pré-requisito:** Ter completado `01-generator-evaluator-pattern.md` e `02-sprint-contracts.md`  
**Status:** 🟢 TEMPLATE CANÔNICO - Reutilizável em todos os sprints do KODA  
**Data de Criação:** Maio 2026

---

## 📖 Prólogo: O Dia em que Fernando Descobriu que Promessas Implícitas Não Escalam

Quarta-feira, 16h12. Fernando estava olhando para uma thread de atendimento que parecia simples. João, cliente recorrente do KODA, escreveu no WhatsApp: "quero um produto de chocolate, tenho R$ 100 e não posso tomar lactose". Era exatamente o tipo de conversa que o time acreditava dominar.

O módulo de busca encontrou produtos. O módulo de ranking ordenou por margem e avaliação. O módulo de recomendação escreveu uma resposta bonita. O checkout recebeu uma intenção de compra. Tudo parecia funcionar.

Vinte minutos depois, a operação virou caos. O Generator tinha entendido "até R$ 100" como preço antes do frete. O Evaluator validou apenas se havia um produto de chocolate. O módulo de promoção aplicou desconto em um item que não aceitava cupom. O checkout montou um carrinho com um produto que continha traços de lactose.

João percebeu antes de pagar. A mensagem dele foi curta: "KODA, eu falei lactose no começo. Vocês esqueceram?"

O problema não era falta de inteligência. Cada agente individual parecia razoável quando lido isoladamente. O problema era que cada agente estava trabalhando com uma definição diferente de "pronto".

Para o Generator, pronto era encontrar opções plausíveis. Para o Evaluator, pronto era não violar o texto principal da pergunta. Para checkout, pronto era ter SKU, preço e endereço. Para Fernando, pronto significava cliente seguro, restrições respeitadas, explicação auditável e zero surpresa entre módulos.

A reunião de incident review começou com uma pergunta desconfortável: "Onde estava escrito o acordo entre quem gera e quem avalia?" A resposta foi silêncio.

Havia prompts. Havia rubrics. Havia validações. Mas não havia um Contract explícito, negociado e assinado entre Generator e Evaluator antes da execução.

Foi ali que Fernando mudou a regra do KODA: nenhum sprint importante começa sem Sprint Contract. Não uma task description solta. Não uma lista vaga de boas práticas. Um acordo completo sobre input, success criteria, constraints, metrics, failure handling e sign-off.

Este arquivo existe para transformar essa regra em prática reutilizável. Ele é um template completo para desenhar contratos de sprint entre agentes do KODA, com campos, exemplos preenchidos, schemas JSON, checklists, guias de negociação e variações por tipo de sprint.

A conexão com o Nível 2 é direta. No módulo de Generator/Evaluator, você aprendeu que um agente não deve avaliar o próprio trabalho. No módulo de Sprint Contracts, você aprendeu que Generator e Evaluator precisam concordar antes de começar. Este template é a ferramenta operacional para fazer esse acordo acontecer sempre do mesmo jeito.

Ao final, você vai conseguir pegar qualquer feature do KODA, como Discover Products, Process Order ou Promotion Application, e escrever um Contract que reduza ambiguidade, facilite debug, diminua retrabalho e deixe claro quando o sistema deve parar, tentar de novo ou escalar para humano.

### O Incidente de João em Linha do Tempo

```
16:12 Cliente João: "Quero algo de chocolate, tenho R$ 100, sou intolerante à lactose."
16:13 Generator: encontra 6 produtos com sabor chocolate.
16:14 Ranking: ordena por avaliação média e margem comercial.
16:15 Evaluator: aprova porque há produtos de chocolate e preço base menor que R$ 100.
16:17 Promotion Agent: aplica cupom CHOCO10 sem verificar restrição de categoria.
16:19 Checkout Agent: monta carrinho com frete que passa do orçamento combinado.
16:21 João: percebe produto com traços de lactose e questiona confiança do KODA.
16:40 Fernando: identifica que cada agente usou um conceito diferente de sucesso.
17:10 Decisão: todo sprint crítico passa a exigir Contract negociado antes da execução.
```

### O Que Você Vai Aprender

- Transformar requisitos de conversa em **Input Specification** testável.
- Escrever **Success Criteria** que um Evaluator consegue aprovar ou rejeitar sem adivinhar intenção.
- Definir **Constraints** de orçamento, alergias, preferências e regras de negócio sem misturar escopo.
- Escolher **Metrics** que tornam qualidade, custo e confiabilidade visíveis.
- Desenhar **Failure Handling** para falhas reais do KODA, não apenas happy path.
- Conduzir negociação entre Generator e Evaluator sem vagueza, over-promising ou scope creep.
- Reutilizar variações do template para sprints simples, complexos, cross-cutting e recovery.

---

## 🎯 Template Principal: Estrutura do Sprint Contract


Este é o template canônico. Use como blueprint sempre que um Generator precisar produzir algo que um Evaluator vai validar. O template está escrito como documento operacional, não como formulário vazio. Cada campo explica o que deve conter, por que existe, como o Evaluator valida e como aparece em KODA.

### Visão Geral do Contract

```
SPRINT CONTRACT
Nome do sprint: nome operacional estável usado em trace, logs e analytics.
Versão do contract: número semântico do acordo, por exemplo 1.0.0.
Generator responsável: agente ou módulo que produz o output.
Evaluator responsável: agente ou módulo que valida o output.
Janela de execução: limite de tempo, tentativas e token budget.
Estado inicial: contexto persistido, dados do cliente e dados de catálogo.
Estado final esperado: output aprovado, falha classificada ou escalacao humana.
Input Specification: o que entra e quais mudanças são permitidas.
Success Criteria: o que significa pronto em termos testáveis.
Constraints: restrições que nunca podem ser violadas.
Metrics: como medir qualidade, custo, latência e segurança.
Failure Handling: o que fazer quando critérios não podem ser satisfeitos.
Sign-off: confirmação explícita de Generator e Evaluator.
```

### 📥 INPUT SPECIFICATION

**Propósito:** Define o que entra no sprint. Sem input claro, o Generator improvisa e o Evaluator avalia outra coisa.

| Campo | O que escrever | Como o Evaluator valida | Exemplo KODA |
|-------|----------------|-------------------------|-------------|
| `dados_de_entrada` | Tudo que o Generator pode usar como fonte primária: mensagem do cliente, perfil, carrinho, catálogo, estoque, preços, promoções e histórico consentido. | Evaluator verifica se todos os dados citados na saída vieram de fontes declaradas. | Mensagem de João, perfil consentido, catálogo de suplementos, estoque SP, preço vigente e histórico de sabor chocolate. |
| `contexto` | Estado relevante da conversa e do sistema: sprint anterior, decisões já tomadas, restrições persistidas, canal WhatsApp, localização e etapa da jornada. | Evaluator rejeita saída que ignore contexto crítico declarado. | João está em Product Discovery, não iniciou checkout, orçamento informado é R$ 100 e lactose é restrição rígida. |
| `limites` | Fronteiras de tempo, tokens, tentativas, catálogo, jurisdição, canal, quantidade de produtos e ações externas permitidas. | Evaluator compara execução observada contra limites máximos. | Máximo 3 tentativas, 12k tokens, 8 segundos de latência e nenhum envio externo sem aprovação. |
| `mudancas_permitidas` | Regras para lidar com mudança de requisito durante o sprint: ajustar dentro do mesmo contract, renegociar ou abrir recovery sprint. | Evaluator rejeita se o Generator absorver mudança que exigia novo contract. | Mudança de sabor fica no sprint; mudança de categoria de produto abre novo contract. |

#### Regras de Escrita

- `dados_de_entrada` deve ser específico o bastante para que outro agente consiga reproduzir a decisão sem ler a conversa inteira.
- `dados_de_entrada` deve separar fato observado de inferência do Generator.
- `dados_de_entrada` deve deixar claro se a regra é rígida, preferencial ou apenas informativa.
- `contexto` deve ser específico o bastante para que outro agente consiga reproduzir a decisão sem ler a conversa inteira.
- `contexto` deve separar fato observado de inferência do Generator.
- `contexto` deve deixar claro se a regra é rígida, preferencial ou apenas informativa.
- `limites` deve ser específico o bastante para que outro agente consiga reproduzir a decisão sem ler a conversa inteira.
- `limites` deve separar fato observado de inferência do Generator.
- `limites` deve deixar claro se a regra é rígida, preferencial ou apenas informativa.
- `mudancas_permitidas` deve ser específico o bastante para que outro agente consiga reproduzir a decisão sem ler a conversa inteira.
- `mudancas_permitidas` deve separar fato observado de inferência do Generator.
- `mudancas_permitidas` deve deixar claro se a regra é rígida, preferencial ou apenas informativa.

### ✅ SUCCESS CRITERIA / Critérios de Aceitação

**Propósito:** Define o que significa pronto. Critério bom é testável, objetivo e conectado ao risco real do sprint.

| Campo | O que escrever | Como o Evaluator valida | Exemplo KODA |
|-------|----------------|-------------------------|-------------|
| `quantidade_outputs` | Número mínimo, máximo e formato dos resultados. Exemplo: 3 produtos recomendáveis, 1 recomendação final, 1 carrinho validado. | Evaluator conta outputs e rejeita excesso ou falta. | Entregar 3 opções válidas e 1 recomendação principal. |
| `validacoes` | Checagens obrigatórias: orçamento, alergias, estoque, preço, desconto, endereço, elegibilidade e consistência com histórico. | Evaluator executa cada validação como checklist binário ou scoring rubric. | Cada opção passa por orçamento, lactose, estoque e sabor. |
| `padrao_qualidade` | Nível esperado de explicação, ranking, clareza, segurança, tom KODA e rastreabilidade. | Evaluator mede score mínimo e verifica justificativa. | Explicação de 2 frases por produto, ranking por fit score e tom consultivo. |
| `condicao_parada` | Momento em que o Generator deve parar: quando critérios passam, quando tentativas acabam, quando conflito é detectado ou quando humano precisa entrar. | Evaluator rejeita loops longos e outputs forçados após condição de parada. | Parar quando 3 opções válidas atingirem score >= 85 ou quando o catálogo provar impossibilidade. |

#### Regras de Escrita

- `quantidade_outputs` deve ser específico o bastante para que outro agente consiga reproduzir a decisão sem ler a conversa inteira.
- `quantidade_outputs` deve separar fato observado de inferência do Generator.
- `quantidade_outputs` deve deixar claro se a regra é rígida, preferencial ou apenas informativa.
- `validacoes` deve ser específico o bastante para que outro agente consiga reproduzir a decisão sem ler a conversa inteira.
- `validacoes` deve separar fato observado de inferência do Generator.
- `validacoes` deve deixar claro se a regra é rígida, preferencial ou apenas informativa.
- `padrao_qualidade` deve ser específico o bastante para que outro agente consiga reproduzir a decisão sem ler a conversa inteira.
- `padrao_qualidade` deve separar fato observado de inferência do Generator.
- `padrao_qualidade` deve deixar claro se a regra é rígida, preferencial ou apenas informativa.
- `condicao_parada` deve ser específico o bastante para que outro agente consiga reproduzir a decisão sem ler a conversa inteira.
- `condicao_parada` deve separar fato observado de inferência do Generator.
- `condicao_parada` deve deixar claro se a regra é rígida, preferencial ou apenas informativa.

### 🧱 CONSTRAINTS / Restrições

**Propósito:** Define fronteiras que têm prioridade sobre criatividade. Constraints são promessas de segurança e negócio.

| Campo | O que escrever | Como o Evaluator valida | Exemplo KODA |
|-------|----------------|-------------------------|-------------|
| `orcamento` | Valor máximo, moeda, inclusão de frete, descontos e margem de arredondamento permitida. | Evaluator recalcula preço final e rejeita violação. | Preço final com desconto aplicado não pode passar de R$ 100 antes do frete, e resposta deve avisar frete separadamente. |
| `alergias` | Alergias, intolerâncias e ingredientes proibidos: lactose, glúten, amendoim, soja, cafeína ou restrições médicas declaradas. | Evaluator cruza produto contra composição e flags de risco. | Produtos com lactose ou traços declarados de leite são bloqueados. |
| `preferencias` | Sabor, formato, marca, objetivo, nível de treino, textura, forma de pagamento e prazo preferido. | Evaluator diferencia preferência flexível de restrição rígida. | Chocolate tem prioridade alta, mas baunilha pode aparecer apenas se houver menos de 3 chocolates seguros. |
| `regras_negocio` | Políticas comerciais: cupom elegível, estoque mínimo, margem, categorias bloqueadas, LGPD, aprovação humana para exceções. | Evaluator aplica policy engine ou checklist de compliance. | Não recomendar produto fora de estoque nem aplicar cupom fora da categoria elegível. |

#### Regras de Escrita

- `orcamento` deve ser específico o bastante para que outro agente consiga reproduzir a decisão sem ler a conversa inteira.
- `orcamento` deve separar fato observado de inferência do Generator.
- `orcamento` deve deixar claro se a regra é rígida, preferencial ou apenas informativa.
- `alergias` deve ser específico o bastante para que outro agente consiga reproduzir a decisão sem ler a conversa inteira.
- `alergias` deve separar fato observado de inferência do Generator.
- `alergias` deve deixar claro se a regra é rígida, preferencial ou apenas informativa.
- `preferencias` deve ser específico o bastante para que outro agente consiga reproduzir a decisão sem ler a conversa inteira.
- `preferencias` deve separar fato observado de inferência do Generator.
- `preferencias` deve deixar claro se a regra é rígida, preferencial ou apenas informativa.
- `regras_negocio` deve ser específico o bastante para que outro agente consiga reproduzir a decisão sem ler a conversa inteira.
- `regras_negocio` deve separar fato observado de inferência do Generator.
- `regras_negocio` deve deixar claro se a regra é rígida, preferencial ou apenas informativa.

### 📊 METRICS / Métricas

**Propósito:** Define como o sprint será medido depois. Sem metrics, o time não aprende com execução.

| Campo | O que escrever | Como o Evaluator valida | Exemplo KODA |
|-------|----------------|-------------------------|-------------|
| `kpis` | Indicadores principais: taxa de aprovação, taxa de retrabalho, acurácia de restrição, satisfação estimada, conversão e custo por sprint. | Evaluator registra cada KPI no trace. | Approval rate, constraint accuracy, recommendation score, token cost e conversion intent. |
| `thresholds` | Valores mínimos ou máximos aceitáveis: score >= 85, latência <= 8s, token budget <= 12k, zero violação de alergia. | Evaluator compara métrica real contra threshold declarado. | Constraint accuracy 100%, recommendation score >= 85, token cost <= 12k. |
| `medicao` | Fonte e método: logs, trace, JSON output, resposta final, eventos de checkout, feedback do cliente e auditoria humana. | Evaluator exige evidência para cada métrica reportada. | Trace JSON, logs de catálogo, snapshot de preço e resposta final ao cliente. |

#### Regras de Escrita

- `kpis` deve ser específico o bastante para que outro agente consiga reproduzir a decisão sem ler a conversa inteira.
- `kpis` deve separar fato observado de inferência do Generator.
- `kpis` deve deixar claro se a regra é rígida, preferencial ou apenas informativa.
- `thresholds` deve ser específico o bastante para que outro agente consiga reproduzir a decisão sem ler a conversa inteira.
- `thresholds` deve separar fato observado de inferência do Generator.
- `thresholds` deve deixar claro se a regra é rígida, preferencial ou apenas informativa.
- `medicao` deve ser específico o bastante para que outro agente consiga reproduzir a decisão sem ler a conversa inteira.
- `medicao` deve separar fato observado de inferência do Generator.
- `medicao` deve deixar claro se a regra é rígida, preferencial ou apenas informativa.

### ⚠️ FAILURE HANDLING

**Propósito:** Define como falhar corretamente. Um bom Contract não força sucesso falso.

| Campo | O que escrever | Como o Evaluator valida | Exemplo KODA |
|-------|----------------|-------------------------|-------------|
| `cenarios_de_falha` | Falhas previstas: sem estoque, conflito de critérios, dados ausentes, preço desatualizado, cupom inválido, timeout e mudança de requisito. | Evaluator classifica a falha usando lista fechada. | Menos de 3 produtos seguros, preço mudou, catálogo sem lactose indisponível ou João muda para BCAA. |
| `acoes` | Resposta operacional para cada falha: refazer busca, pedir clarificação, relaxar preferência, abrir novo sprint, escalar humano ou encerrar com explicação. | Evaluator verifica se ação corresponde ao cenário. | Pedir relaxamento de preferência, abrir novo sprint ou escalar se houver risco médico. |
| `escalacao` | Quando envolver humano, supervisor, policy owner ou suporte: risco médico, cobrança, reclamação, fraude ou alta incerteza. | Evaluator rejeita automação quando regra exige escalacao. | Humano entra se houver conflito médico, reclamação de segurança ou cobrança irregular. |

#### Regras de Escrita

- `cenarios_de_falha` deve ser específico o bastante para que outro agente consiga reproduzir a decisão sem ler a conversa inteira.
- `cenarios_de_falha` deve separar fato observado de inferência do Generator.
- `cenarios_de_falha` deve deixar claro se a regra é rígida, preferencial ou apenas informativa.
- `acoes` deve ser específico o bastante para que outro agente consiga reproduzir a decisão sem ler a conversa inteira.
- `acoes` deve separar fato observado de inferência do Generator.
- `acoes` deve deixar claro se a regra é rígida, preferencial ou apenas informativa.
- `escalacao` deve ser específico o bastante para que outro agente consiga reproduzir a decisão sem ler a conversa inteira.
- `escalacao` deve separar fato observado de inferência do Generator.
- `escalacao` deve deixar claro se a regra é rígida, preferencial ou apenas informativa.

### 🤝 SIGN-OFF / Aprovação

**Propósito:** Confirma que Generator e Evaluator aceitaram o mesmo acordo. Sem sign-off, o sprint não começa.

| Campo | O que escrever | Como o Evaluator valida | Exemplo KODA |
|-------|----------------|-------------------------|-------------|
| `generator_concorda` | Generator declara que entende input, limites, critérios, constraints, métricas e falhas. | Evaluator verifica assinatura lógica antes de aceitar output. | ProductDiscoveryGenerator declara capacidade de buscar, filtrar e explicar 3 opções. |
| `evaluator_concorda` | Evaluator declara que consegue avaliar todos os critérios sem pedir interpretação extra. | Generator não executa enquanto houver critério não avaliável. | ProductQualityEvaluator declara que consegue testar cada critério com dados disponíveis. |
| `registro_de_acordo` | Timestamp, contract_id, versão, checksum do conteúdo e relação com trace_id. | Sistema arquiva o acordo para debug e reuse. | contract_id koda-discover-products-joao-2026-05-28-v1 associado ao trace_id trace-joao-4481. |

#### Regras de Escrita

- `generator_concorda` deve ser específico o bastante para que outro agente consiga reproduzir a decisão sem ler a conversa inteira.
- `generator_concorda` deve separar fato observado de inferência do Generator.
- `generator_concorda` deve deixar claro se a regra é rígida, preferencial ou apenas informativa.
- `evaluator_concorda` deve ser específico o bastante para que outro agente consiga reproduzir a decisão sem ler a conversa inteira.
- `evaluator_concorda` deve separar fato observado de inferência do Generator.
- `evaluator_concorda` deve deixar claro se a regra é rígida, preferencial ou apenas informativa.
- `registro_de_acordo` deve ser específico o bastante para que outro agente consiga reproduzir a decisão sem ler a conversa inteira.
- `registro_de_acordo` deve separar fato observado de inferência do Generator.
- `registro_de_acordo` deve deixar claro se a regra é rígida, preferencial ou apenas informativa.

### Blueprint em JSON do Template Principal

```json
{
  "contract_type": "sprint_contract",
  "contract_version": "1.0.0",
  "system": "KODA",
  "sprint": {
    "name": "Product Discovery",
    "goal": "Encontrar produtos seguros e relevantes para um cliente específico",
    "generator": "ProductDiscoveryGenerator",
    "evaluator": "ProductQualityEvaluator",
    "max_duration_seconds": 480,
    "max_attempts": 3,
    "token_budget": 12000
  },
  "input_specification": {
    "dados_de_entrada": {
      "customer_message": "Quero algo de chocolate ate R$ 100 e sou intolerante a lactose",
      "customer_profile": {
        "customer_id": "customer_joao_1048",
        "name": "Joao",
        "known_restrictions": ["lactose"],
        "known_preferences": ["chocolate"]
      },
      "catalog_snapshot_id": "catalog_sp_2026_05_28_16_00",
      "stock_region": "SP"
    },
    "contexto": {
      "conversation_stage": "discover_products",
      "previous_sprint_id": "conversation-intake-joao-1048",
      "customer_intent": "comprar suplemento seguro dentro do orçamento",
      "hard_constraints_source": "mensagem atual do cliente"
    },
    "limites": {
      "max_products_to_return": 3,
      "max_price_brl": 100,
      "include_shipping_in_budget": false,
      "max_latency_seconds": 8,
      "external_side_effects_allowed": false
    },
    "mudancas_permitidas": {
      "same_sprint": ["troca de sabor", "ajuste de marca preferida"],
      "new_contract_required": ["troca de categoria", "mudanca de restricao medica", "inicio de checkout"],
      "human_escalation_required": ["duvida medica", "reacao alergica", "reclamacao formal"]
    }
  },
  "success_criteria": {
    "quantidade_outputs": {
      "min_options": 3,
      "max_options": 3,
      "final_recommendation_count": 1
    },
    "validacoes": [
      "cada produto tem preco <= 100",
      "cada produto e livre de lactose conforme metadata do catalogo",
      "cada produto esta em estoque na regiao SP",
      "cada produto tem sabor chocolate ou justificativa para excecao"
    ],
    "padrao_qualidade": {
      "minimum_fit_score": 85,
      "explanation_sentences_per_product": 2,
      "tone": "consultivo, claro, seguro"
    },
    "condicao_parada": {
      "success": "3 opcoes validas com score >= 85",
      "failure": "menos de 3 opcoes validas apos 3 tentativas ou conflito de restricoes",
      "renegotiate": "cliente altera categoria ou restricao rigida"
    }
  },
  "constraints": {
    "orcamento": {"currency": "BRL", "max_product_price": 100},
    "alergias": {"blocked_ingredients": ["lactose", "leite", "soro de leite com lactose"]},
    "preferencias": {"flavor": "chocolate", "goal": "suplementacao segura"},
    "regras_negocio": {"must_be_in_stock": true, "coupon_validation_required": true}
  },
  "metrics": {
    "kpis": ["approval_rate", "constraint_accuracy", "fit_score", "token_cost", "latency_seconds"],
    "thresholds": {"constraint_accuracy": 1.0, "fit_score": 85, "token_cost": 12000, "latency_seconds": 8},
    "medicao": ["trace_json", "catalog_snapshot", "price_snapshot", "final_response"]
  },
  "failure_handling": {
    "cenarios_de_falha": [
      {"scenario": "menos_de_3_produtos_validos", "action": "explicar limite e pedir relaxamento de sabor ou orçamento"},
      {"scenario": "risco_de_lactose", "action": "bloquear recomendacao e escalar se houver duvida medica"},
      {"scenario": "preco_desatualizado", "action": "recarregar snapshot e repetir validacao"},
      {"scenario": "mudanca_para_bcaa", "action": "encerrar contract atual e negociar novo Product Discovery Contract"}
    ],
    "escalacao": {"human_required_for": ["risco medico", "cobranca", "fraude", "reclamacao"]}
  },
  "sign_off": {
    "generator_concorda": true,
    "evaluator_concorda": true,
    "signed_at": "2026-05-28T16:12:00-03:00",
    "contract_id": "koda-discover-products-joao-2026-05-28-v1"
  }
}
```

---

## ✅ Exemplo Preenchido para Feature KODA: Discover Products


Este exemplo é completo e executável como referência de design. Ele usa João como cliente realista, orçamento de R$ 100, intolerância à lactose e preferência por chocolate. O objetivo não é apenas recomendar produtos. O objetivo é provar que o Generator e o Evaluator concordam sobre o que uma recomendação segura significa antes de executar.

### Contexto do Cliente

- **Cliente:** João Martins, `customer_joao_1048`.
- **Canal:** WhatsApp.
- **Mensagem atual:** "KODA, quero um suplemento de chocolate, tenho R$ 100 e sou intolerante à lactose."
- **Orçamento:** R$ 100 para o produto, frete apresentado separadamente.
- **Restrição rígida:** intolerância à lactose, incluindo traços declarados de leite.
- **Preferência forte:** sabor chocolate.
- **Preferência flexível:** produto fácil de preparar e bom para rotina pós-treino.
- **Região de estoque:** São Paulo.
- **Estado da jornada:** Product Discovery, antes de checkout.

### Catálogo Realista Usado no Exemplo

| SKU | Produto | Preço | Sabor | Lactose | Estoque SP | Score inicial | Observação |
|-----|---------|-------|-------|---------|------------|---------------|------------|
| KODA-PLANT-CHOCO-500 | Plant Protein Chocolate 500g | R$ 89,90 | Chocolate | Não contém | 42 unidades | 92 | Melhor fit geral |
| KODA-RICE-CHOCO-450 | Rice Protein Chocolate 450g | R$ 74,90 | Chocolate | Não contém | 18 unidades | 88 | Boa opção econômica |
| KODA-PEA-CHOCO-350 | Pea Protein Chocolate 350g | R$ 69,90 | Chocolate | Não contém | 11 unidades | 86 | Textura mais densa |
| KODA-WHEY-ISO-CHOCO | Whey Isolado Chocolate 900g | R$ 99,90 | Pode conter traços | Risco | 25 unidades | 80 | Bloqueado por risco |
| KODA-VEGAN-VANILLA-500 | Plant Protein Baunilha 500g | R$ 84,90 | Baunilha | Não contém | 34 unidades | 81 | Reserva se faltar chocolate |

### Contract Completo

```
╔════════════════════════════════════════════════════════════════════╗
║ SPRINT CONTRACT: Product Discovery para João                      ║
╠════════════════════════════════════════════════════════════════════╣
║ Contract ID: koda-discover-products-joao-2026-05-28-v1            ║
║ Generator: ProductDiscoveryGenerator                              ║
║ Evaluator: ProductQualityEvaluator                                ║
║ Duração máxima: 8 segundos de latência ou 3 tentativas internas    ║
║ Token budget: 12.000 tokens                                       ║
╠════════════════════════════════════════════════════════════════════╣
║ INPUT SPECIFICATION                                                ║
║ - Dados de entrada: mensagem atual de João, perfil consentido,     ║
║   catálogo snapshot catalog_sp_2026_05_28_16_00 e estoque SP.      ║
║ - Contexto: João está em Product Discovery e ainda não iniciou     ║
║   checkout; orçamento é produto até R$ 100, frete separado.        ║
║ - Limites: retornar exatamente 3 opções, sem ação externa,         ║
║   sem reservar estoque e sem aplicar promoção automaticamente.     ║
║ - Mudanças permitidas: troca de sabor fica neste sprint; troca     ║
║   de categoria ou restrição médica exige novo Contract.            ║
╠════════════════════════════════════════════════════════════════════╣
║ SUCCESS CRITERIA                                                   ║
║ - Quantidade outputs: 3 opções válidas e 1 recomendação principal. ║
║ - Validações: preço <= R$ 100, livre de lactose, em estoque SP,    ║
║   sabor chocolate quando disponível, explicação clara.             ║
║ - Padrão qualidade: fit score >= 85, tom consultivo, justificativa ║
║   de 2 frases por produto e ranking por adequação ao João.         ║
║ - Condição parada: parar quando 3 opções válidas forem encontradas ║
║   ou quando catálogo provar impossibilidade após 3 tentativas.     ║
╠════════════════════════════════════════════════════════════════════╣
║ CONSTRAINTS                                                        ║
║ - Orçamento: preço do produto não passa de R$ 100.                 ║
║ - Alergias: qualquer lactose, leite ou traço declarado bloqueia.   ║
║ - Preferências: chocolate é preferência forte; facilidade conta.   ║
║ - Regras negócio: produto precisa estar em estoque e preço precisa ║
║   vir do snapshot vigente.                                         ║
╠════════════════════════════════════════════════════════════════════╣
║ METRICS                                                            ║
║ - KPIs: approval_rate, constraint_accuracy, fit_score, token_cost, ║
║   latency_seconds e conversion_intent.                             ║
║ - Thresholds: constraint_accuracy 100%, score >= 85, latência <= 8s║
║   e token_cost <= 12k.                                             ║
║ - Medição: trace JSON, snapshot de catálogo, snapshot de preço e   ║
║   resposta final enviada ao WhatsApp.                              ║
╠════════════════════════════════════════════════════════════════════╣
║ FAILURE HANDLING                                                   ║
║ - Menos de 3 produtos válidos: explicar limite e perguntar se João ║
║   aceita baunilha ou orçamento maior.                              ║
║ - Risco de lactose: bloquear produto e não mencionar como opção.   ║
║ - Preço mudou: recarregar snapshot e repetir validação.            ║
║ - João muda para BCAA: encerrar este Contract e negociar outro.    ║
║ - Dúvida médica: escalar para humano, sem aconselhamento clínico.  ║
╠════════════════════════════════════════════════════════════════════╣
║ SIGN-OFF                                                           ║
║ - Generator concorda: sim, consegue buscar e explicar 3 opções.    ║
║ - Evaluator concorda: sim, consegue validar todos os critérios.    ║
║ - Status: assinado antes da execução.                              ║
╚════════════════════════════════════════════════════════════════════╝
```

### Resultado Esperado do Generator

```json
{
  "contract_id": "koda-discover-products-joao-2026-05-28-v1",
  "status": "generated_for_evaluation",
  "customer_id": "customer_joao_1048",
  "options": [
    {
      "rank": 1,
      "sku": "KODA-PLANT-CHOCO-500",
      "name": "Plant Protein Chocolate 500g",
      "price_brl": 89.9,
      "lactose_status": "nao_contem",
      "stock_region": "SP",
      "stock_units": 42,
      "fit_score": 92,
      "why_it_fits": "Fica abaixo do orçamento de R$ 100 e respeita a intolerância à lactose. É sabor chocolate e tem boa avaliação para rotina pós-treino."
    },
    {
      "rank": 2,
      "sku": "KODA-RICE-CHOCO-450",
      "name": "Rice Protein Chocolate 450g",
      "price_brl": 74.9,
      "lactose_status": "nao_contem",
      "stock_region": "SP",
      "stock_units": 18,
      "fit_score": 88,
      "why_it_fits": "É a opção mais econômica mantendo sabor chocolate e segurança para lactose. Tem estoque em São Paulo e deixa margem no orçamento do João."
    },
    {
      "rank": 3,
      "sku": "KODA-PEA-CHOCO-350",
      "name": "Pea Protein Chocolate 350g",
      "price_brl": 69.9,
      "lactose_status": "nao_contem",
      "stock_region": "SP",
      "stock_units": 11,
      "fit_score": 86,
      "why_it_fits": "Também respeita orçamento e restrição de lactose. Entra em terceiro porque a textura é mais densa, mas ainda é segura e compatível com chocolate."
    }
  ],
  "final_recommendation": {
    "sku": "KODA-PLANT-CHOCO-500",
    "reason": "melhor equilíbrio entre segurança, sabor chocolate, estoque e score geral"
  },
  "blocked_products": [
    {
      "sku": "KODA-WHEY-ISO-CHOCO",
      "reason": "metadata informa risco de traços de leite ou lactose"
    }
  ]
}
```

### Resultado Esperado do Evaluator

```json
{
  "contract_id": "koda-discover-products-joao-2026-05-28-v1",
  "evaluation_status": "approved",
  "criteria_results": {
    "quantidade_outputs": {"passed": true, "observed": 3},
    "orcamento": {"passed": true, "max_observed_price_brl": 89.9, "limit_brl": 100},
    "lactose": {"passed": true, "blocked_risky_products": ["KODA-WHEY-ISO-CHOCO"]},
    "estoque_sp": {"passed": true, "all_options_in_stock": true},
    "sabor_chocolate": {"passed": true, "all_options_match": true},
    "fit_score": {"passed": true, "minimum_observed": 86, "threshold": 85},
    "explanation_quality": {"passed": true, "all_have_customer_specific_reason": true}
  },
  "metrics": {
    "constraint_accuracy": 1.0,
    "approval_rate_contribution": 1,
    "latency_seconds": 4.6,
    "token_cost": 8420,
    "recommended_fit_score": 92
  },
  "feedback_to_generator": "Aprovado. O produto com risco de lactose foi corretamente bloqueado e as 3 opções respeitam o Contract."
}
```

### Walkthrough de Validação do Caso João

#### Entrada capturada
A mensagem de João contém orçamento, restrição e preferência em uma frase curta; o Contract separa cada elemento em campo próprio.

#### Restrição endurecida
Lactose deixa de ser observação textual e vira constraint rígida com bloqueio de produtos arriscados.

#### Orçamento interpretado
R$ 100 é aplicado ao preço do produto; frete será informado depois para não misturar Product Discovery com Checkout.

#### Catálogo congelado
O snapshot impede que Generator e Evaluator usem preços diferentes durante a mesma execução.

#### Produtos bloqueados
Whey isolado com traços de leite não aparece como opção, mesmo sendo barato e sabor chocolate.

#### Ranking explicado
A opção Plant Protein vence por score, não por margem comercial invisível.

#### Evaluator aprova
A aprovação ocorre porque cada critério tem evidência, não porque a resposta parece bonita.

---

## 📊 Tabela Comparativa de Estratégias de Coordenação


| Estratégia | Previsibilidade | Flexibilidade | Custo de Setup | Taxa de Erro | Debugabilidade | Escalabilidade |
|------------|------------------|----------------|----------------|--------------|----------------|----------------|
| Sprint Contracts | Alta, porque input, criteria e failure são acordados antes | Alta, porque cada sprint pode renegociar limites | Médio no começo, baixo após template library | Baixa em sprints críticos; erros viram violações explícitas | Alta, porque trace aponta qual cláusula falhou | Alta, pois templates versionados servem milhares de conversas |
| Self-Validation | Baixa, porque o mesmo agente racionaliza o próprio output | Média, pois um agente improvisa rápido | Baixo | Alta em restrições sutis como lactose, cupom e orçamento | Baixa, porque não há crítico independente | Baixa para conversas longas, pois viés cresce com contexto |
| Generator/Evaluator only | Média, porque há avaliação depois, mas não acordo antes | Média, boa para outputs isolados | Médio | Média; o Evaluator pega erros finais, mas pode não prevenir escopo errado | Média, porque rejeição existe, mas causa pode ser ambígua | Média-alta quando rubrics são fortes |
| Free-form prompts | Muito baixa, depende da interpretação do prompt | Alta demais, frequentemente vira caos | Muito baixo | Alta, especialmente em mudanças mid-sprint | Muito baixa, porque não há estrutura de auditoria | Baixa, pois cada prompt vira exceção |
| Hardcoded rules | Alta para casos previstos | Baixa, regras quebram em cenários novos | Alto quando domínio muda muito | Baixa no happy path, alta fora do script | Média, logs mostram regra, mas não intenção | Média, cresce com custo de manutenção |

### Como Ler a Tabela

- Use **Sprint Contracts** quando o risco de interpretação errada é maior que o custo de escrever o acordo.
- Use **Generator/Evaluator only** quando o output é simples e o escopo não muda durante a execução.
- Evite **Self-Validation** para qualquer coisa com orçamento, alergia, pagamento, estoque ou política comercial.
- Evite **Free-form prompts** em produção; eles são úteis para exploração, não para operação confiável.
- Use **Hardcoded rules** para invariantes de segurança, mas não como substituto de negociação semântica entre agentes.

---

## 🧭 ASCII Architecture Diagram: Lifecycle do Contract


```
+------------------+     +------------------+     +------------------+
|  1. PROPOSE      | --> |  2. NEGOTIATE    | --> |  3. AGREE        |
|  (Generator)     |     |  (Both parties)  |     |  (Signed)        |
+------------------+     +------------------+     +------------------+
                                                          |
                                                          v
+------------------+     +------------------+     +------------------+
|  6. CLOSE        | <-- |  5. VERIFY       | <-- |  4. EXECUTE      |
|  (Archive/Reuse) |     |  (Evaluator)     |     |  (Generator)     |
+------------------+     +------------------+     +------------------+
```

### Leitura Operacional do Diagrama

1. **Propose:** o Generator propõe um Contract que ele acredita conseguir cumprir.
2. **Negotiate:** o Evaluator critica vagueza, falta de validação e risco de escopo.
3. **Agree:** ambos assinam uma versão estável do Contract antes de executar.
4. **Execute:** o Generator produz output seguindo exatamente o acordo.
5. **Verify:** o Evaluator aprova, rejeita ou aciona failure handling com base nas cláusulas.
6. **Close:** o sistema arquiva trace, métricas e lições para reuso do template.

---

## 🔍 Checklist de Validação de Contrato


Use este checklist antes de colocar qualquer Sprint Contract em produção. A regra é simples: se um item crítico falha, o sprint não começa. O custo de renegociar antes é menor que o custo de explicar um erro para o cliente depois.

### Input completeness checks

- [ ] A mensagem atual do cliente foi capturada em texto bruto.
- [ ] O perfil usado tem origem consentida e compatível com LGPD.
- [ ] O catálogo tem snapshot identificável e timestamp.
- [ ] O preço vem de fonte declarada e não de memória do agente.
- [ ] O estoque corresponde à região de entrega relevante.
- [ ] Restrições médicas foram separadas de preferências de sabor.
- [ ] Orçamento indica se inclui frete, cupom e taxas.
- [ ] Histórico de compras foi marcado como contexto, não como verdade absoluta.
- [ ] O sprint anterior foi citado quando influencia a decisão atual.
- [ ] Dados ausentes têm ação definida antes da execução.

### Criteria testability checks

- [ ] Cada success criterion pode ser respondido com aprovado, reprovado ou score numérico.
- [ ] Não há critério baseado apenas em "parece bom".
- [ ] Quantidade mínima e máxima de outputs está explícita.
- [ ] Formato do output é validável por JSON schema ou checklist estável.
- [ ] Critério de qualidade tem threshold mensurável.
- [ ] Condição de parada evita loops infinitos.
- [ ] Critérios de segurança têm prioridade maior que preferência.
- [ ] Evaluator consegue validar sem perguntar intenção ao Generator.
- [ ] Critérios conflitantes têm ordem de precedência.
- [ ] A resposta final ao cliente é parte do que será avaliado.

### Failure handling coverage

- [ ] Existe ação para menos outputs válidos que o mínimo.
- [ ] Existe ação para mudança de requisito durante o sprint.
- [ ] Existe ação para dados de catálogo desatualizados.
- [ ] Existe ação para timeout ou token budget excedido.
- [ ] Existe ação para conflito entre orçamento e restrição.
- [ ] Existe ação para risco médico ou alergia ambígua.
- [ ] Existe ação para cupom inválido ou promoção expirada.
- [ ] Existe ação para estoque insuficiente após seleção.
- [ ] Existe ação para pagamento ou cobrança quando o sprint envolve checkout.
- [ ] Existe critério claro para escalar para humano.

### Boundary conditions

- [ ] O Contract diz o que acontece com exatamente zero produtos válidos.
- [ ] O Contract diz o que acontece com um único produto válido.
- [ ] O Contract diz o que acontece quando há produtos demais.
- [ ] O Contract define arredondamento de preço.
- [ ] O Contract define tratamento de produto com traços de alergênico.
- [ ] O Contract diferencia preferência forte de restrição rígida.
- [ ] O Contract define mudança pequena versus mudança que exige novo sprint.
- [ ] O Contract define região quando estoque varia por localidade.
- [ ] O Contract define como agir se o cliente envia mensagens contraditórias.
- [ ] O Contract define como encerrar sem recomendação ruim.

### Token budget considerations

- [ ] O Contract tem token budget explícito.
- [ ] O Generator sabe quais dados resumir antes de raciocinar.
- [ ] O Evaluator recebe evidência suficiente sem reler conversa inteira.
- [ ] Schemas são compactos e não duplicam catálogo completo quando IDs bastam.
- [ ] Trace registra decisões críticas sem salvar texto irrelevante.
- [ ] Tentativas máximas protegem custo.
- [ ] Critérios são ordenados para falhar rápido em constraints rígidas.
- [ ] O Contract evita pedir explicações longas para produtos rejeitados sem necessidade.
- [ ] O output final é separado do trace técnico.
- [ ] O close step registra custo real para calibrar próximos contracts.

### Cross-sprint consistency

- [ ] O nome do sprint é consistente com a template library.
- [ ] O contract_id aponta para conversa, cliente e versão.
- [ ] A saída do sprint atual é compatível com a entrada do próximo.
- [ ] Constraints rígidas persistem entre Product Discovery e Checkout.
- [ ] Preferências flexíveis são revalidadas quando contexto muda.
- [ ] Métricas usam nomes iguais aos dashboards existentes.
- [ ] Failure codes são reaproveitáveis em trace reading.
- [ ] Mudanças de versão preservam comparação histórica.
- [ ] O Contract não contradiz ADRs ou docs canônicos do KODA.
- [ ] O archive inclui lições para melhorar o template.

### Checklist Estendido por Campo

#### 📥 INPUT SPECIFICATION

- [ ] `dados_de_entrada` tem dono explícito no Generator ou no Evaluator.
- [ ] `dados_de_entrada` pode ser observado no trace sem depender de memória humana.
- [ ] `dados_de_entrada` tem exemplo positivo no contexto do KODA.
- [ ] `dados_de_entrada` tem exemplo negativo que deve ser rejeitado.
- [ ] `dados_de_entrada` não mistura regra rígida com preferência flexível.
- [ ] `dados_de_entrada` tem comportamento definido quando dado está ausente.
- [ ] `dados_de_entrada` pode ser versionado sem quebrar contracts antigos.
- [ ] `dados_de_entrada` é curto o suficiente para caber no prompt do Evaluator.
- [ ] `dados_de_entrada` é específico o suficiente para evitar interpretação livre.
- [ ] `dados_de_entrada` melhora debug quando João reclama de uma recomendação.
- [ ] `contexto` tem dono explícito no Generator ou no Evaluator.
- [ ] `contexto` pode ser observado no trace sem depender de memória humana.
- [ ] `contexto` tem exemplo positivo no contexto do KODA.
- [ ] `contexto` tem exemplo negativo que deve ser rejeitado.
- [ ] `contexto` não mistura regra rígida com preferência flexível.
- [ ] `contexto` tem comportamento definido quando dado está ausente.
- [ ] `contexto` pode ser versionado sem quebrar contracts antigos.
- [ ] `contexto` é curto o suficiente para caber no prompt do Evaluator.
- [ ] `contexto` é específico o suficiente para evitar interpretação livre.
- [ ] `contexto` melhora debug quando João reclama de uma recomendação.
- [ ] `limites` tem dono explícito no Generator ou no Evaluator.
- [ ] `limites` pode ser observado no trace sem depender de memória humana.
- [ ] `limites` tem exemplo positivo no contexto do KODA.
- [ ] `limites` tem exemplo negativo que deve ser rejeitado.
- [ ] `limites` não mistura regra rígida com preferência flexível.
- [ ] `limites` tem comportamento definido quando dado está ausente.
- [ ] `limites` pode ser versionado sem quebrar contracts antigos.
- [ ] `limites` é curto o suficiente para caber no prompt do Evaluator.
- [ ] `limites` é específico o suficiente para evitar interpretação livre.
- [ ] `limites` melhora debug quando João reclama de uma recomendação.
- [ ] `mudancas_permitidas` tem dono explícito no Generator ou no Evaluator.
- [ ] `mudancas_permitidas` pode ser observado no trace sem depender de memória humana.
- [ ] `mudancas_permitidas` tem exemplo positivo no contexto do KODA.
- [ ] `mudancas_permitidas` tem exemplo negativo que deve ser rejeitado.
- [ ] `mudancas_permitidas` não mistura regra rígida com preferência flexível.
- [ ] `mudancas_permitidas` tem comportamento definido quando dado está ausente.
- [ ] `mudancas_permitidas` pode ser versionado sem quebrar contracts antigos.
- [ ] `mudancas_permitidas` é curto o suficiente para caber no prompt do Evaluator.
- [ ] `mudancas_permitidas` é específico o suficiente para evitar interpretação livre.
- [ ] `mudancas_permitidas` melhora debug quando João reclama de uma recomendação.

#### ✅ SUCCESS CRITERIA / Critérios de Aceitação

- [ ] `quantidade_outputs` tem dono explícito no Generator ou no Evaluator.
- [ ] `quantidade_outputs` pode ser observado no trace sem depender de memória humana.
- [ ] `quantidade_outputs` tem exemplo positivo no contexto do KODA.
- [ ] `quantidade_outputs` tem exemplo negativo que deve ser rejeitado.
- [ ] `quantidade_outputs` não mistura regra rígida com preferência flexível.
- [ ] `quantidade_outputs` tem comportamento definido quando dado está ausente.
- [ ] `quantidade_outputs` pode ser versionado sem quebrar contracts antigos.
- [ ] `quantidade_outputs` é curto o suficiente para caber no prompt do Evaluator.
- [ ] `quantidade_outputs` é específico o suficiente para evitar interpretação livre.
- [ ] `quantidade_outputs` melhora debug quando João reclama de uma recomendação.
- [ ] `validacoes` tem dono explícito no Generator ou no Evaluator.
- [ ] `validacoes` pode ser observado no trace sem depender de memória humana.
- [ ] `validacoes` tem exemplo positivo no contexto do KODA.
- [ ] `validacoes` tem exemplo negativo que deve ser rejeitado.
- [ ] `validacoes` não mistura regra rígida com preferência flexível.
- [ ] `validacoes` tem comportamento definido quando dado está ausente.
- [ ] `validacoes` pode ser versionado sem quebrar contracts antigos.
- [ ] `validacoes` é curto o suficiente para caber no prompt do Evaluator.
- [ ] `validacoes` é específico o suficiente para evitar interpretação livre.
- [ ] `validacoes` melhora debug quando João reclama de uma recomendação.
- [ ] `padrao_qualidade` tem dono explícito no Generator ou no Evaluator.
- [ ] `padrao_qualidade` pode ser observado no trace sem depender de memória humana.
- [ ] `padrao_qualidade` tem exemplo positivo no contexto do KODA.
- [ ] `padrao_qualidade` tem exemplo negativo que deve ser rejeitado.
- [ ] `padrao_qualidade` não mistura regra rígida com preferência flexível.
- [ ] `padrao_qualidade` tem comportamento definido quando dado está ausente.
- [ ] `padrao_qualidade` pode ser versionado sem quebrar contracts antigos.
- [ ] `padrao_qualidade` é curto o suficiente para caber no prompt do Evaluator.
- [ ] `padrao_qualidade` é específico o suficiente para evitar interpretação livre.
- [ ] `padrao_qualidade` melhora debug quando João reclama de uma recomendação.
- [ ] `condicao_parada` tem dono explícito no Generator ou no Evaluator.
- [ ] `condicao_parada` pode ser observado no trace sem depender de memória humana.
- [ ] `condicao_parada` tem exemplo positivo no contexto do KODA.
- [ ] `condicao_parada` tem exemplo negativo que deve ser rejeitado.
- [ ] `condicao_parada` não mistura regra rígida com preferência flexível.
- [ ] `condicao_parada` tem comportamento definido quando dado está ausente.
- [ ] `condicao_parada` pode ser versionado sem quebrar contracts antigos.
- [ ] `condicao_parada` é curto o suficiente para caber no prompt do Evaluator.
- [ ] `condicao_parada` é específico o suficiente para evitar interpretação livre.
- [ ] `condicao_parada` melhora debug quando João reclama de uma recomendação.

#### 🧱 CONSTRAINTS / Restrições

- [ ] `orcamento` tem dono explícito no Generator ou no Evaluator.
- [ ] `orcamento` pode ser observado no trace sem depender de memória humana.
- [ ] `orcamento` tem exemplo positivo no contexto do KODA.
- [ ] `orcamento` tem exemplo negativo que deve ser rejeitado.
- [ ] `orcamento` não mistura regra rígida com preferência flexível.
- [ ] `orcamento` tem comportamento definido quando dado está ausente.
- [ ] `orcamento` pode ser versionado sem quebrar contracts antigos.
- [ ] `orcamento` é curto o suficiente para caber no prompt do Evaluator.
- [ ] `orcamento` é específico o suficiente para evitar interpretação livre.
- [ ] `orcamento` melhora debug quando João reclama de uma recomendação.
- [ ] `alergias` tem dono explícito no Generator ou no Evaluator.
- [ ] `alergias` pode ser observado no trace sem depender de memória humana.
- [ ] `alergias` tem exemplo positivo no contexto do KODA.
- [ ] `alergias` tem exemplo negativo que deve ser rejeitado.
- [ ] `alergias` não mistura regra rígida com preferência flexível.
- [ ] `alergias` tem comportamento definido quando dado está ausente.
- [ ] `alergias` pode ser versionado sem quebrar contracts antigos.
- [ ] `alergias` é curto o suficiente para caber no prompt do Evaluator.
- [ ] `alergias` é específico o suficiente para evitar interpretação livre.
- [ ] `alergias` melhora debug quando João reclama de uma recomendação.
- [ ] `preferencias` tem dono explícito no Generator ou no Evaluator.
- [ ] `preferencias` pode ser observado no trace sem depender de memória humana.
- [ ] `preferencias` tem exemplo positivo no contexto do KODA.
- [ ] `preferencias` tem exemplo negativo que deve ser rejeitado.
- [ ] `preferencias` não mistura regra rígida com preferência flexível.
- [ ] `preferencias` tem comportamento definido quando dado está ausente.
- [ ] `preferencias` pode ser versionado sem quebrar contracts antigos.
- [ ] `preferencias` é curto o suficiente para caber no prompt do Evaluator.
- [ ] `preferencias` é específico o suficiente para evitar interpretação livre.
- [ ] `preferencias` melhora debug quando João reclama de uma recomendação.
- [ ] `regras_negocio` tem dono explícito no Generator ou no Evaluator.
- [ ] `regras_negocio` pode ser observado no trace sem depender de memória humana.
- [ ] `regras_negocio` tem exemplo positivo no contexto do KODA.
- [ ] `regras_negocio` tem exemplo negativo que deve ser rejeitado.
- [ ] `regras_negocio` não mistura regra rígida com preferência flexível.
- [ ] `regras_negocio` tem comportamento definido quando dado está ausente.
- [ ] `regras_negocio` pode ser versionado sem quebrar contracts antigos.
- [ ] `regras_negocio` é curto o suficiente para caber no prompt do Evaluator.
- [ ] `regras_negocio` é específico o suficiente para evitar interpretação livre.
- [ ] `regras_negocio` melhora debug quando João reclama de uma recomendação.

#### 📊 METRICS / Métricas

- [ ] `kpis` tem dono explícito no Generator ou no Evaluator.
- [ ] `kpis` pode ser observado no trace sem depender de memória humana.
- [ ] `kpis` tem exemplo positivo no contexto do KODA.
- [ ] `kpis` tem exemplo negativo que deve ser rejeitado.
- [ ] `kpis` não mistura regra rígida com preferência flexível.
- [ ] `kpis` tem comportamento definido quando dado está ausente.
- [ ] `kpis` pode ser versionado sem quebrar contracts antigos.
- [ ] `kpis` é curto o suficiente para caber no prompt do Evaluator.
- [ ] `kpis` é específico o suficiente para evitar interpretação livre.
- [ ] `kpis` melhora debug quando João reclama de uma recomendação.
- [ ] `thresholds` tem dono explícito no Generator ou no Evaluator.
- [ ] `thresholds` pode ser observado no trace sem depender de memória humana.
- [ ] `thresholds` tem exemplo positivo no contexto do KODA.
- [ ] `thresholds` tem exemplo negativo que deve ser rejeitado.
- [ ] `thresholds` não mistura regra rígida com preferência flexível.
- [ ] `thresholds` tem comportamento definido quando dado está ausente.
- [ ] `thresholds` pode ser versionado sem quebrar contracts antigos.
- [ ] `thresholds` é curto o suficiente para caber no prompt do Evaluator.
- [ ] `thresholds` é específico o suficiente para evitar interpretação livre.
- [ ] `thresholds` melhora debug quando João reclama de uma recomendação.
- [ ] `medicao` tem dono explícito no Generator ou no Evaluator.
- [ ] `medicao` pode ser observado no trace sem depender de memória humana.
- [ ] `medicao` tem exemplo positivo no contexto do KODA.
- [ ] `medicao` tem exemplo negativo que deve ser rejeitado.
- [ ] `medicao` não mistura regra rígida com preferência flexível.
- [ ] `medicao` tem comportamento definido quando dado está ausente.
- [ ] `medicao` pode ser versionado sem quebrar contracts antigos.
- [ ] `medicao` é curto o suficiente para caber no prompt do Evaluator.
- [ ] `medicao` é específico o suficiente para evitar interpretação livre.
- [ ] `medicao` melhora debug quando João reclama de uma recomendação.

#### ⚠️ FAILURE HANDLING

- [ ] `cenarios_de_falha` tem dono explícito no Generator ou no Evaluator.
- [ ] `cenarios_de_falha` pode ser observado no trace sem depender de memória humana.
- [ ] `cenarios_de_falha` tem exemplo positivo no contexto do KODA.
- [ ] `cenarios_de_falha` tem exemplo negativo que deve ser rejeitado.
- [ ] `cenarios_de_falha` não mistura regra rígida com preferência flexível.
- [ ] `cenarios_de_falha` tem comportamento definido quando dado está ausente.
- [ ] `cenarios_de_falha` pode ser versionado sem quebrar contracts antigos.
- [ ] `cenarios_de_falha` é curto o suficiente para caber no prompt do Evaluator.
- [ ] `cenarios_de_falha` é específico o suficiente para evitar interpretação livre.
- [ ] `cenarios_de_falha` melhora debug quando João reclama de uma recomendação.
- [ ] `acoes` tem dono explícito no Generator ou no Evaluator.
- [ ] `acoes` pode ser observado no trace sem depender de memória humana.
- [ ] `acoes` tem exemplo positivo no contexto do KODA.
- [ ] `acoes` tem exemplo negativo que deve ser rejeitado.
- [ ] `acoes` não mistura regra rígida com preferência flexível.
- [ ] `acoes` tem comportamento definido quando dado está ausente.
- [ ] `acoes` pode ser versionado sem quebrar contracts antigos.
- [ ] `acoes` é curto o suficiente para caber no prompt do Evaluator.
- [ ] `acoes` é específico o suficiente para evitar interpretação livre.
- [ ] `acoes` melhora debug quando João reclama de uma recomendação.
- [ ] `escalacao` tem dono explícito no Generator ou no Evaluator.
- [ ] `escalacao` pode ser observado no trace sem depender de memória humana.
- [ ] `escalacao` tem exemplo positivo no contexto do KODA.
- [ ] `escalacao` tem exemplo negativo que deve ser rejeitado.
- [ ] `escalacao` não mistura regra rígida com preferência flexível.
- [ ] `escalacao` tem comportamento definido quando dado está ausente.
- [ ] `escalacao` pode ser versionado sem quebrar contracts antigos.
- [ ] `escalacao` é curto o suficiente para caber no prompt do Evaluator.
- [ ] `escalacao` é específico o suficiente para evitar interpretação livre.
- [ ] `escalacao` melhora debug quando João reclama de uma recomendação.

#### 🤝 SIGN-OFF / Aprovação

- [ ] `generator_concorda` tem dono explícito no Generator ou no Evaluator.
- [ ] `generator_concorda` pode ser observado no trace sem depender de memória humana.
- [ ] `generator_concorda` tem exemplo positivo no contexto do KODA.
- [ ] `generator_concorda` tem exemplo negativo que deve ser rejeitado.
- [ ] `generator_concorda` não mistura regra rígida com preferência flexível.
- [ ] `generator_concorda` tem comportamento definido quando dado está ausente.
- [ ] `generator_concorda` pode ser versionado sem quebrar contracts antigos.
- [ ] `generator_concorda` é curto o suficiente para caber no prompt do Evaluator.
- [ ] `generator_concorda` é específico o suficiente para evitar interpretação livre.
- [ ] `generator_concorda` melhora debug quando João reclama de uma recomendação.
- [ ] `evaluator_concorda` tem dono explícito no Generator ou no Evaluator.
- [ ] `evaluator_concorda` pode ser observado no trace sem depender de memória humana.
- [ ] `evaluator_concorda` tem exemplo positivo no contexto do KODA.
- [ ] `evaluator_concorda` tem exemplo negativo que deve ser rejeitado.
- [ ] `evaluator_concorda` não mistura regra rígida com preferência flexível.
- [ ] `evaluator_concorda` tem comportamento definido quando dado está ausente.
- [ ] `evaluator_concorda` pode ser versionado sem quebrar contracts antigos.
- [ ] `evaluator_concorda` é curto o suficiente para caber no prompt do Evaluator.
- [ ] `evaluator_concorda` é específico o suficiente para evitar interpretação livre.
- [ ] `evaluator_concorda` melhora debug quando João reclama de uma recomendação.
- [ ] `registro_de_acordo` tem dono explícito no Generator ou no Evaluator.
- [ ] `registro_de_acordo` pode ser observado no trace sem depender de memória humana.
- [ ] `registro_de_acordo` tem exemplo positivo no contexto do KODA.
- [ ] `registro_de_acordo` tem exemplo negativo que deve ser rejeitado.
- [ ] `registro_de_acordo` não mistura regra rígida com preferência flexível.
- [ ] `registro_de_acordo` tem comportamento definido quando dado está ausente.
- [ ] `registro_de_acordo` pode ser versionado sem quebrar contracts antigos.
- [ ] `registro_de_acordo` é curto o suficiente para caber no prompt do Evaluator.
- [ ] `registro_de_acordo` é específico o suficiente para evitar interpretação livre.
- [ ] `registro_de_acordo` melhora debug quando João reclama de uma recomendação.

---

## 🤝 Guia de Negociação de Contrato


Negociação não é burocracia. É o mecanismo que impede Generator e Evaluator de começarem com expectativas diferentes. Em KODA, a negociação deve ser curta, explícita e registrada no trace.

### Phase 1: Generator proposes

- Apresentar o objetivo do sprint em uma frase operacional.
- Listar dados que pretende usar e fontes correspondentes.
- Declarar limites de execução, tentativas e token budget.
- Propor quantidade de outputs e formato de resposta.
- Separar constraints rígidas de preferências negociáveis.
- Declarar falhas que consegue detectar sem ajuda humana.
- Explicar o que será arquivado no trace.
- Pedir crítica explícita do Evaluator antes de executar.

### Phase 2: Evaluator critiques

- Questionar qualquer critério que não seja testável.
- Pedir fonte para preço, estoque, alergia e promoção.
- Empurrar de volta quando o Generator promete mais do que consegue medir.
- Exigir failure handling para catálogo vazio, conflito e mudança de requisito.
- Verificar se o Contract separa Product Discovery de Checkout.
- Checar se token budget permite avaliar evidências, não apenas resposta final.
- Adicionar threshold quando o critério usa palavra qualitativa.
- Vetar execução quando uma restrição médica estiver ambígua.

### Phase 3: Both converge

- Transformar termos vagos em thresholds.
- Trocar escopo por confiabilidade quando necessário.
- Aceitar outputs parciais apenas se failure handling explicar ao cliente.
- Registrar critérios que ficaram fora do sprint atual.
- Confirmar ordem de precedência entre segurança, orçamento e preferência.
- Assinar contract_id e versão.
- Executar apenas após ambos confirmarem que conseguem cumprir seus papéis.
- Arquivar pontos de negociação para melhorar próximo template.

### Anti-patterns em Negociação

| Anti-pattern | Por que quebra | Correção prática |
|--------------|----------------|------------------|
| Critério vago | "Recomendar um produto bom" não é avaliável; troque por score, constraints e evidência. | Reescrever cláusula com dado, threshold, dono e ação observável. |
| Over-promising | Generator promete considerar todo histórico, todo catálogo e todas as promoções sem token budget compatível. | Reescrever cláusula com dado, threshold, dono e ação observável. |
| Scope creep | Durante Product Discovery, alguém adiciona checkout, frete, cupom e pagamento no mesmo sprint. | Reescrever cláusula com dado, threshold, dono e ação observável. |
| Evaluator passivo | Evaluator aceita critérios só porque o Generator parece confiante. | Reescrever cláusula com dado, threshold, dono e ação observável. |
| Falha sem dono | O Contract diz que algo pode falhar, mas não diz quem age nem como responder ao cliente. | Reescrever cláusula com dado, threshold, dono e ação observável. |
| Mudança silenciosa | Cliente muda de whey para BCAA e o Generator adapta sem renegociar. | Reescrever cláusula com dado, threshold, dono e ação observável. |
| Métrica decorativa | KPI é citado, mas não há fonte de medição no trace. | Reescrever cláusula com dado, threshold, dono e ação observável. |
| Sign-off automático | Sistema marca contract como assinado sem confirmação lógica dos dois papéis. | Reescrever cláusula com dado, threshold, dono e ação observável. |

### Exemplo de Diálogo entre Generator e Evaluator

```
Generator: Quero executar Product Discovery para João. Vou retornar 3 produtos de chocolate até R$ 100.
Evaluator: Até R$ 100 inclui frete ou apenas preço do produto?
Generator: Apenas preço do produto. Vou avisar que frete será calculado no checkout.
Evaluator: A restrição de lactose é rígida ou preferência?
Generator: Rígida. Produtos com lactose ou traços declarados serão bloqueados.
Evaluator: Como você lida se só houver 2 chocolates seguros?
Generator: Retorno falha parcial, explico a João e pergunto se ele aceita baunilha segura ou orçamento maior.
Evaluator: Não chame isso de sucesso. Classifique como menos_de_3_produtos_validos.
Generator: Concordo. Success exige exatamente 3 opções; menos que isso aciona failure handling.
Evaluator: Qual score mínimo?
Generator: 85 para cada opção. A recomendação principal precisa ter maior fit score.
Evaluator: Quais fontes de evidência?
Generator: Snapshot de catálogo, estoque SP, preço vigente e metadata de ingredientes.
Evaluator: Com esses ajustes, consigo validar. Assino o Contract.
Generator: Também assino. Executando sob contract_id koda-discover-products-joao-2026-05-28-v1.
```

---

## 🚀 Aplicação KODA: Casos de Uso


### Discover Products Sprint

**Problema:** Cliente informa objetivo, orçamento, alergia e preferência; KODA precisa encontrar produtos seguros sem pular para checkout.

**Contract design:**
- Input contém mensagem, perfil, catálogo, preço e estoque.
- Success exige 3 opções válidas e 1 recomendação principal.
- Constraints priorizam alergia e orçamento antes de sabor.
- Failure handling pede relaxamento de preferência se catálogo for insuficiente.

**Evaluation:**
- Evaluator recalcula preço.
- Evaluator bloqueia produtos com lactose.
- Evaluator confirma estoque regional.
- Evaluator verifica explicação individual.

**Metrics:**
- constraint_accuracy 100%
- fit_score >= 85
- latency <= 8s
- token_cost <= 12k
- rework_rate <= 5%

#### Mini Contract Operacional

```
SPRINT: Discover Products Sprint
PROBLEMA: Cliente informa objetivo, orçamento, alergia e preferência; KODA precisa encontrar produtos seguros sem pular para checkout.
DESIGN: Input contém mensagem, perfil, catálogo, preço e estoque.
DESIGN: Success exige 3 opções válidas e 1 recomendação principal.
DESIGN: Constraints priorizam alergia e orçamento antes de sabor.
DESIGN: Failure handling pede relaxamento de preferência se catálogo for insuficiente.
EVALUATION: Evaluator recalcula preço.
EVALUATION: Evaluator bloqueia produtos com lactose.
EVALUATION: Evaluator confirma estoque regional.
EVALUATION: Evaluator verifica explicação individual.
METRIC: constraint_accuracy 100%
METRIC: fit_score >= 85
METRIC: latency <= 8s
METRIC: token_cost <= 12k
METRIC: rework_rate <= 5%
SIGN-OFF: Generator e Evaluator concordam antes de executar.
```

### Process Order Sprint

**Problema:** Cliente escolhe produto e quer comprar; KODA precisa montar carrinho, validar preço, endereço, frete, pagamento e confirmação sem cobrança indevida.

**Contract design:**
- Input contém SKU aprovado, quantidade, endereço, forma de pagamento e consentimento para avançar.
- Success exige carrinho válido, preço final explicado e confirmação explícita antes de pagamento.
- Constraints bloqueiam cobrança sem confirmação e impedem substituição silenciosa de produto.
- Failure handling separa estoque acabou, endereço inválido, pagamento recusado e preço mudou.

**Evaluation:**
- Evaluator compara SKU com Product Discovery aprovado.
- Evaluator verifica soma de itens, desconto, frete e total.
- Evaluator checa consentimento textual para pagamento.
- Evaluator exige mensagem final com resumo claro.

**Metrics:**
- payment_error_rate 0%
- cart_total_accuracy 100%
- human_escalation_for_payment_dispute 100%
- latency <= 12s
- checkout_completion_rate

#### Mini Contract Operacional

```
SPRINT: Process Order Sprint
PROBLEMA: Cliente escolhe produto e quer comprar; KODA precisa montar carrinho, validar preço, endereço, frete, pagamento e confirmação sem cobrança indevida.
DESIGN: Input contém SKU aprovado, quantidade, endereço, forma de pagamento e consentimento para avançar.
DESIGN: Success exige carrinho válido, preço final explicado e confirmação explícita antes de pagamento.
DESIGN: Constraints bloqueiam cobrança sem confirmação e impedem substituição silenciosa de produto.
DESIGN: Failure handling separa estoque acabou, endereço inválido, pagamento recusado e preço mudou.
EVALUATION: Evaluator compara SKU com Product Discovery aprovado.
EVALUATION: Evaluator verifica soma de itens, desconto, frete e total.
EVALUATION: Evaluator checa consentimento textual para pagamento.
EVALUATION: Evaluator exige mensagem final com resumo claro.
METRIC: payment_error_rate 0%
METRIC: cart_total_accuracy 100%
METRIC: human_escalation_for_payment_dispute 100%
METRIC: latency <= 12s
METRIC: checkout_completion_rate
SIGN-OFF: Generator e Evaluator concordam antes de executar.
```

### Promotion Application Sprint

**Problema:** Cliente menciona cupom ou promoção; KODA precisa aplicar desconto apenas quando regras comerciais permitem.

**Contract design:**
- Input contém código do cupom, SKU, categoria, data, região e customer segment.
- Success exige elegibilidade comprovada, desconto calculado e explicação de motivo quando cupom não vale.
- Constraints impedem desconto cumulativo não permitido e aplicação em categoria bloqueada.
- Failure handling orienta alternativa comercial quando cupom expira ou não se aplica.

**Evaluation:**
- Evaluator consulta regra de promoção versionada.
- Evaluator recalcula preço antes e depois do desconto.
- Evaluator verifica se cupom foi aplicado uma única vez.
- Evaluator bloqueia cupom quando produto já está em preço mínimo.

**Metrics:**
- discount_accuracy 100%
- policy_violation_rate 0%
- customer_explanation_score >= 90
- promotion_margin_guardrail_passed
- manual_override_rate <= 2%

#### Mini Contract Operacional

```
SPRINT: Promotion Application Sprint
PROBLEMA: Cliente menciona cupom ou promoção; KODA precisa aplicar desconto apenas quando regras comerciais permitem.
DESIGN: Input contém código do cupom, SKU, categoria, data, região e customer segment.
DESIGN: Success exige elegibilidade comprovada, desconto calculado e explicação de motivo quando cupom não vale.
DESIGN: Constraints impedem desconto cumulativo não permitido e aplicação em categoria bloqueada.
DESIGN: Failure handling orienta alternativa comercial quando cupom expira ou não se aplica.
EVALUATION: Evaluator consulta regra de promoção versionada.
EVALUATION: Evaluator recalcula preço antes e depois do desconto.
EVALUATION: Evaluator verifica se cupom foi aplicado uma única vez.
EVALUATION: Evaluator bloqueia cupom quando produto já está em preço mínimo.
METRIC: discount_accuracy 100%
METRIC: policy_violation_rate 0%
METRIC: customer_explanation_score >= 90
METRIC: promotion_margin_guardrail_passed
METRIC: manual_override_rate <= 2%
SIGN-OFF: Generator e Evaluator concordam antes de executar.
```

---

## 📋 Variações do Template por Tipo de Sprint


### Simple Sprint (single validation, quick)

Usado quando o risco é baixo e o output é pequeno, como confirmar disponibilidade de um SKU.

**Estrutura recomendada:**
- Input mínimo com SKU e região.
- Success binário: disponível ou indisponível.
- Constraints limitadas a estoque e preço vigente.
- Failure handling simples: pedir alternativa ou avisar indisponibilidade.

**Quando usar:**
- Consulta de estoque.
- Validação de preço atual.
- Confirmação de prazo estimado sem compra.
- Resposta curta com baixo risco.

### Complex Sprint (multiple validations, retry)

Usado quando há várias validações e até 3 tentativas, como Discover Products com alergia e orçamento.

**Estrutura recomendada:**
- Input completo com catálogo e perfil.
- Success com múltiplos critérios e score.
- Constraints rígidas priorizadas.
- Failure handling cobre retry, renegociação e escalacao.

**Quando usar:**
- Recomendação com múltiplas restrições.
- Comparação de produtos.
- Montagem de bundle.
- Escolha de plano ou assinatura.

### Cross-cutting Sprint (affects multiple modules)

Usado quando o sprint atravessa descoberta, carrinho, promoção e mensagens.

**Estrutura recomendada:**
- Input inclui contratos anteriores.
- Success exige compatibilidade entre módulos.
- Constraints incluem política global.
- Failure handling protege consistência cross-sprint.

**Quando usar:**
- Mudança de política promocional.
- Sincronização entre descoberta e checkout.
- Alteração de regra de frete.
- Atualização que afeta múltiplos agents.

### Recovery Sprint (error handling)

Usado quando algo falhou e KODA precisa corrigir sem piorar confiança.

**Estrutura recomendada:**
- Input inclui trace da falha e estado seguro.
- Success exige diagnóstico, correção e comunicação honesta.
- Constraints bloqueiam cobrança, recomendação ou promessa nova sem validação.
- Failure handling escala rápido se risco persistir.

**Quando usar:**
- Produto recomendado violou regra.
- Pagamento falhou.
- Cliente reclamou de inconsistência.
- Trace mostra divergência entre Contract e execução.

---

## 🧩 Catálogo Detalhado de Cláusulas Reutilizáveis


As cláusulas abaixo podem ser copiadas para contracts reais do KODA. Elas estão organizadas por campo e escritas em linguagem operacional para Generator e Evaluator.

### Cláusulas para `dados_de_entrada`

#### 1. mensagem do cliente
- Cláusula recomendada: Para `dados_de_entrada`, o Contract declara explicitamente como `mensagem do cliente` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `mensagem do cliente` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `mensagem do cliente` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `mensagem do cliente` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `mensagem do cliente` em campo, threshold, lista permitida ou failure code antes de executar.

#### 2. perfil consentido
- Cláusula recomendada: Para `dados_de_entrada`, o Contract declara explicitamente como `perfil consentido` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `perfil consentido` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `perfil consentido` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `perfil consentido` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `perfil consentido` em campo, threshold, lista permitida ou failure code antes de executar.

#### 3. catálogo snapshot
- Cláusula recomendada: Para `dados_de_entrada`, o Contract declara explicitamente como `catálogo snapshot` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `catálogo snapshot` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `catálogo snapshot` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `catálogo snapshot` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `catálogo snapshot` em campo, threshold, lista permitida ou failure code antes de executar.

#### 4. estoque regional
- Cláusula recomendada: Para `dados_de_entrada`, o Contract declara explicitamente como `estoque regional` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `estoque regional` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `estoque regional` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `estoque regional` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `estoque regional` em campo, threshold, lista permitida ou failure code antes de executar.

#### 5. preço vigente
- Cláusula recomendada: Para `dados_de_entrada`, o Contract declara explicitamente como `preço vigente` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `preço vigente` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `preço vigente` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `preço vigente` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `preço vigente` em campo, threshold, lista permitida ou failure code antes de executar.

#### 6. histórico de compras
- Cláusula recomendada: Para `dados_de_entrada`, o Contract declara explicitamente como `histórico de compras` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `histórico de compras` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `histórico de compras` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `histórico de compras` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `histórico de compras` em campo, threshold, lista permitida ou failure code antes de executar.

#### 7. carrinho atual
- Cláusula recomendada: Para `dados_de_entrada`, o Contract declara explicitamente como `carrinho atual` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `carrinho atual` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `carrinho atual` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `carrinho atual` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `carrinho atual` em campo, threshold, lista permitida ou failure code antes de executar.

#### 8. cupom informado
- Cláusula recomendada: Para `dados_de_entrada`, o Contract declara explicitamente como `cupom informado` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `cupom informado` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `cupom informado` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `cupom informado` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `cupom informado` em campo, threshold, lista permitida ou failure code antes de executar.

#### 9. endereço parcial
- Cláusula recomendada: Para `dados_de_entrada`, o Contract declara explicitamente como `endereço parcial` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `endereço parcial` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `endereço parcial` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `endereço parcial` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `endereço parcial` em campo, threshold, lista permitida ou failure code antes de executar.

#### 10. objetivo declarado
- Cláusula recomendada: Para `dados_de_entrada`, o Contract declara explicitamente como `objetivo declarado` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `objetivo declarado` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `objetivo declarado` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `objetivo declarado` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `objetivo declarado` em campo, threshold, lista permitida ou failure code antes de executar.

### Cláusulas para `contexto`

#### 1. etapa da jornada
- Cláusula recomendada: Para `contexto`, o Contract declara explicitamente como `etapa da jornada` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `etapa da jornada` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `etapa da jornada` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `etapa da jornada` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `etapa da jornada` em campo, threshold, lista permitida ou failure code antes de executar.

#### 2. sprint anterior
- Cláusula recomendada: Para `contexto`, o Contract declara explicitamente como `sprint anterior` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `sprint anterior` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `sprint anterior` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `sprint anterior` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `sprint anterior` em campo, threshold, lista permitida ou failure code antes de executar.

#### 3. decisão já aprovada
- Cláusula recomendada: Para `contexto`, o Contract declara explicitamente como `decisão já aprovada` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `decisão já aprovada` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `decisão já aprovada` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `decisão já aprovada` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `decisão já aprovada` em campo, threshold, lista permitida ou failure code antes de executar.

#### 4. restrição persistida
- Cláusula recomendada: Para `contexto`, o Contract declara explicitamente como `restrição persistida` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `restrição persistida` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `restrição persistida` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `restrição persistida` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `restrição persistida` em campo, threshold, lista permitida ou failure code antes de executar.

#### 5. canal WhatsApp
- Cláusula recomendada: Para `contexto`, o Contract declara explicitamente como `canal WhatsApp` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `canal WhatsApp` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `canal WhatsApp` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `canal WhatsApp` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `canal WhatsApp` em campo, threshold, lista permitida ou failure code antes de executar.

#### 6. região de entrega
- Cláusula recomendada: Para `contexto`, o Contract declara explicitamente como `região de entrega` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `região de entrega` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `região de entrega` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `região de entrega` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `região de entrega` em campo, threshold, lista permitida ou failure code antes de executar.

#### 7. tempo de conversa
- Cláusula recomendada: Para `contexto`, o Contract declara explicitamente como `tempo de conversa` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `tempo de conversa` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `tempo de conversa` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `tempo de conversa` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `tempo de conversa` em campo, threshold, lista permitida ou failure code antes de executar.

#### 8. estado emocional do cliente
- Cláusula recomendada: Para `contexto`, o Contract declara explicitamente como `estado emocional do cliente` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `estado emocional do cliente` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `estado emocional do cliente` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `estado emocional do cliente` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `estado emocional do cliente` em campo, threshold, lista permitida ou failure code antes de executar.

#### 9. origem da recomendação
- Cláusula recomendada: Para `contexto`, o Contract declara explicitamente como `origem da recomendação` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `origem da recomendação` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `origem da recomendação` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `origem da recomendação` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `origem da recomendação` em campo, threshold, lista permitida ou failure code antes de executar.

#### 10. status do checkout
- Cláusula recomendada: Para `contexto`, o Contract declara explicitamente como `status do checkout` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `status do checkout` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `status do checkout` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `status do checkout` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `status do checkout` em campo, threshold, lista permitida ou failure code antes de executar.

### Cláusulas para `limites`

#### 1. tempo máximo
- Cláusula recomendada: Para `limites`, o Contract declara explicitamente como `tempo máximo` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `tempo máximo` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `tempo máximo` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `tempo máximo` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `tempo máximo` em campo, threshold, lista permitida ou failure code antes de executar.

#### 2. token budget
- Cláusula recomendada: Para `limites`, o Contract declara explicitamente como `token budget` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `token budget` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `token budget` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `token budget` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `token budget` em campo, threshold, lista permitida ou failure code antes de executar.

#### 3. tentativas
- Cláusula recomendada: Para `limites`, o Contract declara explicitamente como `tentativas` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `tentativas` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `tentativas` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `tentativas` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `tentativas` em campo, threshold, lista permitida ou failure code antes de executar.

#### 4. quantidade de produtos
- Cláusula recomendada: Para `limites`, o Contract declara explicitamente como `quantidade de produtos` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `quantidade de produtos` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `quantidade de produtos` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `quantidade de produtos` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `quantidade de produtos` em campo, threshold, lista permitida ou failure code antes de executar.

#### 5. ações externas
- Cláusula recomendada: Para `limites`, o Contract declara explicitamente como `ações externas` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `ações externas` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `ações externas` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `ações externas` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `ações externas` em campo, threshold, lista permitida ou failure code antes de executar.

#### 6. uso de ferramenta
- Cláusula recomendada: Para `limites`, o Contract declara explicitamente como `uso de ferramenta` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `uso de ferramenta` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `uso de ferramenta` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `uso de ferramenta` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `uso de ferramenta` em campo, threshold, lista permitida ou failure code antes de executar.

#### 7. janela de catálogo
- Cláusula recomendada: Para `limites`, o Contract declara explicitamente como `janela de catálogo` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `janela de catálogo` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `janela de catálogo` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `janela de catálogo` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `janela de catálogo` em campo, threshold, lista permitida ou failure code antes de executar.

#### 8. escopo comercial
- Cláusula recomendada: Para `limites`, o Contract declara explicitamente como `escopo comercial` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `escopo comercial` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `escopo comercial` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `escopo comercial` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `escopo comercial` em campo, threshold, lista permitida ou failure code antes de executar.

#### 9. limite de desconto
- Cláusula recomendada: Para `limites`, o Contract declara explicitamente como `limite de desconto` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `limite de desconto` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `limite de desconto` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `limite de desconto` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `limite de desconto` em campo, threshold, lista permitida ou failure code antes de executar.

#### 10. limite de autonomia
- Cláusula recomendada: Para `limites`, o Contract declara explicitamente como `limite de autonomia` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `limite de autonomia` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `limite de autonomia` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `limite de autonomia` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `limite de autonomia` em campo, threshold, lista permitida ou failure code antes de executar.

### Cláusulas para `mudancas_permitidas`

#### 1. troca de sabor
- Cláusula recomendada: Para `mudancas_permitidas`, o Contract declara explicitamente como `troca de sabor` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `troca de sabor` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `troca de sabor` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `troca de sabor` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `troca de sabor` em campo, threshold, lista permitida ou failure code antes de executar.

#### 2. troca de marca
- Cláusula recomendada: Para `mudancas_permitidas`, o Contract declara explicitamente como `troca de marca` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `troca de marca` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `troca de marca` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `troca de marca` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `troca de marca` em campo, threshold, lista permitida ou failure code antes de executar.

#### 3. ajuste de orçamento
- Cláusula recomendada: Para `mudancas_permitidas`, o Contract declara explicitamente como `ajuste de orçamento` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `ajuste de orçamento` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `ajuste de orçamento` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `ajuste de orçamento` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `ajuste de orçamento` em campo, threshold, lista permitida ou failure code antes de executar.

#### 4. mudança de categoria
- Cláusula recomendada: Para `mudancas_permitidas`, o Contract declara explicitamente como `mudança de categoria` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `mudança de categoria` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `mudança de categoria` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `mudança de categoria` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `mudança de categoria` em campo, threshold, lista permitida ou failure code antes de executar.

#### 5. nova alergia
- Cláusula recomendada: Para `mudancas_permitidas`, o Contract declara explicitamente como `nova alergia` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `nova alergia` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `nova alergia` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `nova alergia` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `nova alergia` em campo, threshold, lista permitida ou failure code antes de executar.

#### 6. entrada em checkout
- Cláusula recomendada: Para `mudancas_permitidas`, o Contract declara explicitamente como `entrada em checkout` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `entrada em checkout` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `entrada em checkout` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `entrada em checkout` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `entrada em checkout` em campo, threshold, lista permitida ou failure code antes de executar.

#### 7. cancelamento
- Cláusula recomendada: Para `mudancas_permitidas`, o Contract declara explicitamente como `cancelamento` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `cancelamento` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `cancelamento` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `cancelamento` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `cancelamento` em campo, threshold, lista permitida ou failure code antes de executar.

#### 8. pedido de comparação
- Cláusula recomendada: Para `mudancas_permitidas`, o Contract declara explicitamente como `pedido de comparação` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `pedido de comparação` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `pedido de comparação` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `pedido de comparação` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `pedido de comparação` em campo, threshold, lista permitida ou failure code antes de executar.

#### 9. pedido de humano
- Cláusula recomendada: Para `mudancas_permitidas`, o Contract declara explicitamente como `pedido de humano` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `pedido de humano` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `pedido de humano` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `pedido de humano` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `pedido de humano` em campo, threshold, lista permitida ou failure code antes de executar.

#### 10. adição de cupom
- Cláusula recomendada: Para `mudancas_permitidas`, o Contract declara explicitamente como `adição de cupom` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `adição de cupom` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `adição de cupom` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `adição de cupom` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `adição de cupom` em campo, threshold, lista permitida ou failure code antes de executar.

### Cláusulas para `quantidade_outputs`

#### 1. uma recomendação final
- Cláusula recomendada: Para `quantidade_outputs`, o Contract declara explicitamente como `uma recomendação final` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `uma recomendação final` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `uma recomendação final` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `uma recomendação final` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `uma recomendação final` em campo, threshold, lista permitida ou failure code antes de executar.

#### 2. três opções válidas
- Cláusula recomendada: Para `quantidade_outputs`, o Contract declara explicitamente como `três opções válidas` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `três opções válidas` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `três opções válidas` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `três opções válidas` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `três opções válidas` em campo, threshold, lista permitida ou failure code antes de executar.

#### 3. cinco comparações
- Cláusula recomendada: Para `quantidade_outputs`, o Contract declara explicitamente como `cinco comparações` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `cinco comparações` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `cinco comparações` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `cinco comparações` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `cinco comparações` em campo, threshold, lista permitida ou failure code antes de executar.

#### 4. um carrinho
- Cláusula recomendada: Para `quantidade_outputs`, o Contract declara explicitamente como `um carrinho` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `um carrinho` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `um carrinho` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `um carrinho` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `um carrinho` em campo, threshold, lista permitida ou failure code antes de executar.

#### 5. uma explicação
- Cláusula recomendada: Para `quantidade_outputs`, o Contract declara explicitamente como `uma explicação` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `uma explicação` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `uma explicação` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `uma explicação` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `uma explicação` em campo, threshold, lista permitida ou failure code antes de executar.

#### 6. uma falha classificada
- Cláusula recomendada: Para `quantidade_outputs`, o Contract declara explicitamente como `uma falha classificada` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `uma falha classificada` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `uma falha classificada` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `uma falha classificada` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `uma falha classificada` em campo, threshold, lista permitida ou failure code antes de executar.

#### 7. um pedido de clarificação
- Cláusula recomendada: Para `quantidade_outputs`, o Contract declara explicitamente como `um pedido de clarificação` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `um pedido de clarificação` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `um pedido de clarificação` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `um pedido de clarificação` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `um pedido de clarificação` em campo, threshold, lista permitida ou failure code antes de executar.

#### 8. um trace resumido
- Cláusula recomendada: Para `quantidade_outputs`, o Contract declara explicitamente como `um trace resumido` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `um trace resumido` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `um trace resumido` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `um trace resumido` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `um trace resumido` em campo, threshold, lista permitida ou failure code antes de executar.

#### 9. um score
- Cláusula recomendada: Para `quantidade_outputs`, o Contract declara explicitamente como `um score` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `um score` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `um score` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `um score` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `um score` em campo, threshold, lista permitida ou failure code antes de executar.

#### 10. uma decisão de escalacao
- Cláusula recomendada: Para `quantidade_outputs`, o Contract declara explicitamente como `uma decisão de escalacao` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `uma decisão de escalacao` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `uma decisão de escalacao` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `uma decisão de escalacao` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `uma decisão de escalacao` em campo, threshold, lista permitida ou failure code antes de executar.

### Cláusulas para `validacoes`

#### 1. orçamento
- Cláusula recomendada: Para `validacoes`, o Contract declara explicitamente como `orçamento` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `orçamento` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `orçamento` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `orçamento` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `orçamento` em campo, threshold, lista permitida ou failure code antes de executar.

#### 2. lactose
- Cláusula recomendada: Para `validacoes`, o Contract declara explicitamente como `lactose` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `lactose` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `lactose` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `lactose` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `lactose` em campo, threshold, lista permitida ou failure code antes de executar.

#### 3. glúten
- Cláusula recomendada: Para `validacoes`, o Contract declara explicitamente como `glúten` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `glúten` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `glúten` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `glúten` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `glúten` em campo, threshold, lista permitida ou failure code antes de executar.

#### 4. amendoim
- Cláusula recomendada: Para `validacoes`, o Contract declara explicitamente como `amendoim` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `amendoim` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `amendoim` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `amendoim` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `amendoim` em campo, threshold, lista permitida ou failure code antes de executar.

#### 5. estoque
- Cláusula recomendada: Para `validacoes`, o Contract declara explicitamente como `estoque` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `estoque` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `estoque` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `estoque` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `estoque` em campo, threshold, lista permitida ou failure code antes de executar.

#### 6. preço
- Cláusula recomendada: Para `validacoes`, o Contract declara explicitamente como `preço` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `preço` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `preço` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `preço` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `preço` em campo, threshold, lista permitida ou failure code antes de executar.

#### 7. cupom
- Cláusula recomendada: Para `validacoes`, o Contract declara explicitamente como `cupom` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `cupom` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `cupom` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `cupom` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `cupom` em campo, threshold, lista permitida ou failure code antes de executar.

#### 8. frete
- Cláusula recomendada: Para `validacoes`, o Contract declara explicitamente como `frete` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `frete` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `frete` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `frete` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `frete` em campo, threshold, lista permitida ou failure code antes de executar.

#### 9. pagamento
- Cláusula recomendada: Para `validacoes`, o Contract declara explicitamente como `pagamento` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `pagamento` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `pagamento` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `pagamento` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `pagamento` em campo, threshold, lista permitida ou failure code antes de executar.

#### 10. consentimento
- Cláusula recomendada: Para `validacoes`, o Contract declara explicitamente como `consentimento` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `consentimento` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `consentimento` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `consentimento` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `consentimento` em campo, threshold, lista permitida ou failure code antes de executar.

### Cláusulas para `padrao_qualidade`

#### 1. clareza
- Cláusula recomendada: Para `padrao_qualidade`, o Contract declara explicitamente como `clareza` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `clareza` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `clareza` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `clareza` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `clareza` em campo, threshold, lista permitida ou failure code antes de executar.

#### 2. tom consultivo
- Cláusula recomendada: Para `padrao_qualidade`, o Contract declara explicitamente como `tom consultivo` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `tom consultivo` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `tom consultivo` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `tom consultivo` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `tom consultivo` em campo, threshold, lista permitida ou failure code antes de executar.

#### 3. explicação específica
- Cláusula recomendada: Para `padrao_qualidade`, o Contract declara explicitamente como `explicação específica` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `explicação específica` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `explicação específica` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `explicação específica` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `explicação específica` em campo, threshold, lista permitida ou failure code antes de executar.

#### 4. ranking justificado
- Cláusula recomendada: Para `padrao_qualidade`, o Contract declara explicitamente como `ranking justificado` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `ranking justificado` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `ranking justificado` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `ranking justificado` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `ranking justificado` em campo, threshold, lista permitida ou failure code antes de executar.

#### 5. sem alucinação
- Cláusula recomendada: Para `padrao_qualidade`, o Contract declara explicitamente como `sem alucinação` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `sem alucinação` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `sem alucinação` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `sem alucinação` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `sem alucinação` em campo, threshold, lista permitida ou failure code antes de executar.

#### 6. sem pressão comercial
- Cláusula recomendada: Para `padrao_qualidade`, o Contract declara explicitamente como `sem pressão comercial` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `sem pressão comercial` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `sem pressão comercial` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `sem pressão comercial` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `sem pressão comercial` em campo, threshold, lista permitida ou failure code antes de executar.

#### 7. resposta curta
- Cláusula recomendada: Para `padrao_qualidade`, o Contract declara explicitamente como `resposta curta` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `resposta curta` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `resposta curta` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `resposta curta` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `resposta curta` em campo, threshold, lista permitida ou failure code antes de executar.

#### 8. evidência rastreável
- Cláusula recomendada: Para `padrao_qualidade`, o Contract declara explicitamente como `evidência rastreável` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `evidência rastreável` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `evidência rastreável` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `evidência rastreável` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `evidência rastreável` em campo, threshold, lista permitida ou failure code antes de executar.

#### 9. linguagem segura
- Cláusula recomendada: Para `padrao_qualidade`, o Contract declara explicitamente como `linguagem segura` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `linguagem segura` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `linguagem segura` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `linguagem segura` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `linguagem segura` em campo, threshold, lista permitida ou failure code antes de executar.

#### 10. próximo passo claro
- Cláusula recomendada: Para `padrao_qualidade`, o Contract declara explicitamente como `próximo passo claro` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `próximo passo claro` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `próximo passo claro` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `próximo passo claro` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `próximo passo claro` em campo, threshold, lista permitida ou failure code antes de executar.

### Cláusulas para `condicao_parada`

#### 1. critérios passam
- Cláusula recomendada: Para `condicao_parada`, o Contract declara explicitamente como `critérios passam` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `critérios passam` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `critérios passam` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `critérios passam` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `critérios passam` em campo, threshold, lista permitida ou failure code antes de executar.

#### 2. tentativas acabam
- Cláusula recomendada: Para `condicao_parada`, o Contract declara explicitamente como `tentativas acabam` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `tentativas acabam` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `tentativas acabam` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `tentativas acabam` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `tentativas acabam` em campo, threshold, lista permitida ou failure code antes de executar.

#### 3. conflito detectado
- Cláusula recomendada: Para `condicao_parada`, o Contract declara explicitamente como `conflito detectado` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `conflito detectado` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `conflito detectado` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `conflito detectado` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `conflito detectado` em campo, threshold, lista permitida ou failure code antes de executar.

#### 4. cliente muda escopo
- Cláusula recomendada: Para `condicao_parada`, o Contract declara explicitamente como `cliente muda escopo` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `cliente muda escopo` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `cliente muda escopo` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `cliente muda escopo` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `cliente muda escopo` em campo, threshold, lista permitida ou failure code antes de executar.

#### 5. risco médico aparece
- Cláusula recomendada: Para `condicao_parada`, o Contract declara explicitamente como `risco médico aparece` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `risco médico aparece` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `risco médico aparece` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `risco médico aparece` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `risco médico aparece` em campo, threshold, lista permitida ou failure code antes de executar.

#### 6. catálogo insuficiente
- Cláusula recomendada: Para `condicao_parada`, o Contract declara explicitamente como `catálogo insuficiente` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `catálogo insuficiente` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `catálogo insuficiente` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `catálogo insuficiente` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `catálogo insuficiente` em campo, threshold, lista permitida ou failure code antes de executar.

#### 7. pagamento exige humano
- Cláusula recomendada: Para `condicao_parada`, o Contract declara explicitamente como `pagamento exige humano` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `pagamento exige humano` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `pagamento exige humano` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `pagamento exige humano` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `pagamento exige humano` em campo, threshold, lista permitida ou failure code antes de executar.

#### 8. token budget atinge limite
- Cláusula recomendada: Para `condicao_parada`, o Contract declara explicitamente como `token budget atinge limite` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `token budget atinge limite` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `token budget atinge limite` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `token budget atinge limite` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `token budget atinge limite` em campo, threshold, lista permitida ou failure code antes de executar.

#### 9. latência excede limite
- Cláusula recomendada: Para `condicao_parada`, o Contract declara explicitamente como `latência excede limite` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `latência excede limite` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `latência excede limite` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `latência excede limite` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `latência excede limite` em campo, threshold, lista permitida ou failure code antes de executar.

#### 10. dados críticos ausentes
- Cláusula recomendada: Para `condicao_parada`, o Contract declara explicitamente como `dados críticos ausentes` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `dados críticos ausentes` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `dados críticos ausentes` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `dados críticos ausentes` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `dados críticos ausentes` em campo, threshold, lista permitida ou failure code antes de executar.

### Cláusulas para `orcamento`

#### 1. preço do produto
- Cláusula recomendada: Para `orcamento`, o Contract declara explicitamente como `preço do produto` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `preço do produto` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `preço do produto` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `preço do produto` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `preço do produto` em campo, threshold, lista permitida ou failure code antes de executar.

#### 2. frete separado
- Cláusula recomendada: Para `orcamento`, o Contract declara explicitamente como `frete separado` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `frete separado` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `frete separado` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `frete separado` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `frete separado` em campo, threshold, lista permitida ou failure code antes de executar.

#### 3. cupom aplicado
- Cláusula recomendada: Para `orcamento`, o Contract declara explicitamente como `cupom aplicado` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `cupom aplicado` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `cupom aplicado` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `cupom aplicado` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `cupom aplicado` em campo, threshold, lista permitida ou failure code antes de executar.

#### 4. imposto
- Cláusula recomendada: Para `orcamento`, o Contract declara explicitamente como `imposto` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `imposto` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `imposto` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `imposto` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `imposto` em campo, threshold, lista permitida ou failure code antes de executar.

#### 5. parcelamento
- Cláusula recomendada: Para `orcamento`, o Contract declara explicitamente como `parcelamento` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `parcelamento` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `parcelamento` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `parcelamento` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `parcelamento` em campo, threshold, lista permitida ou failure code antes de executar.

#### 6. arredondamento
- Cláusula recomendada: Para `orcamento`, o Contract declara explicitamente como `arredondamento` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `arredondamento` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `arredondamento` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `arredondamento` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `arredondamento` em campo, threshold, lista permitida ou failure code antes de executar.

#### 7. moeda BRL
- Cláusula recomendada: Para `orcamento`, o Contract declara explicitamente como `moeda BRL` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `moeda BRL` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `moeda BRL` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `moeda BRL` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `moeda BRL` em campo, threshold, lista permitida ou failure code antes de executar.

#### 8. margem de centavos
- Cláusula recomendada: Para `orcamento`, o Contract declara explicitamente como `margem de centavos` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `margem de centavos` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `margem de centavos` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `margem de centavos` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `margem de centavos` em campo, threshold, lista permitida ou failure code antes de executar.

#### 9. limite máximo
- Cláusula recomendada: Para `orcamento`, o Contract declara explicitamente como `limite máximo` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `limite máximo` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `limite máximo` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `limite máximo` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `limite máximo` em campo, threshold, lista permitida ou failure code antes de executar.

#### 10. comunicação ao cliente
- Cláusula recomendada: Para `orcamento`, o Contract declara explicitamente como `comunicação ao cliente` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `comunicação ao cliente` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `comunicação ao cliente` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `comunicação ao cliente` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `comunicação ao cliente` em campo, threshold, lista permitida ou failure code antes de executar.

### Cláusulas para `alergias`

#### 1. lactose
- Cláusula recomendada: Para `alergias`, o Contract declara explicitamente como `lactose` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `lactose` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `lactose` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `lactose` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `lactose` em campo, threshold, lista permitida ou failure code antes de executar.

#### 2. glúten
- Cláusula recomendada: Para `alergias`, o Contract declara explicitamente como `glúten` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `glúten` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `glúten` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `glúten` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `glúten` em campo, threshold, lista permitida ou failure code antes de executar.

#### 3. amendoim
- Cláusula recomendada: Para `alergias`, o Contract declara explicitamente como `amendoim` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `amendoim` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `amendoim` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `amendoim` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `amendoim` em campo, threshold, lista permitida ou failure code antes de executar.

#### 4. soja
- Cláusula recomendada: Para `alergias`, o Contract declara explicitamente como `soja` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `soja` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `soja` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `soja` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `soja` em campo, threshold, lista permitida ou failure code antes de executar.

#### 5. cafeína
- Cláusula recomendada: Para `alergias`, o Contract declara explicitamente como `cafeína` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `cafeína` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `cafeína` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `cafeína` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `cafeína` em campo, threshold, lista permitida ou failure code antes de executar.

#### 6. corante
- Cláusula recomendada: Para `alergias`, o Contract declara explicitamente como `corante` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `corante` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `corante` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `corante` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `corante` em campo, threshold, lista permitida ou failure code antes de executar.

#### 7. adoçante
- Cláusula recomendada: Para `alergias`, o Contract declara explicitamente como `adoçante` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `adoçante` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `adoçante` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `adoçante` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `adoçante` em campo, threshold, lista permitida ou failure code antes de executar.

#### 8. traços
- Cláusula recomendada: Para `alergias`, o Contract declara explicitamente como `traços` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `traços` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `traços` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `traços` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `traços` em campo, threshold, lista permitida ou failure code antes de executar.

#### 9. contaminação cruzada
- Cláusula recomendada: Para `alergias`, o Contract declara explicitamente como `contaminação cruzada` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `contaminação cruzada` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `contaminação cruzada` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `contaminação cruzada` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `contaminação cruzada` em campo, threshold, lista permitida ou failure code antes de executar.

#### 10. dúvida médica
- Cláusula recomendada: Para `alergias`, o Contract declara explicitamente como `dúvida médica` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `dúvida médica` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `dúvida médica` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `dúvida médica` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `dúvida médica` em campo, threshold, lista permitida ou failure code antes de executar.

### Cláusulas para `preferencias`

#### 1. chocolate
- Cláusula recomendada: Para `preferencias`, o Contract declara explicitamente como `chocolate` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `chocolate` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `chocolate` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `chocolate` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `chocolate` em campo, threshold, lista permitida ou failure code antes de executar.

#### 2. baunilha
- Cláusula recomendada: Para `preferencias`, o Contract declara explicitamente como `baunilha` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `baunilha` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `baunilha` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `baunilha` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `baunilha` em campo, threshold, lista permitida ou failure code antes de executar.

#### 3. sem sabor
- Cláusula recomendada: Para `preferencias`, o Contract declara explicitamente como `sem sabor` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `sem sabor` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `sem sabor` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `sem sabor` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `sem sabor` em campo, threshold, lista permitida ou failure code antes de executar.

#### 4. marca preferida
- Cláusula recomendada: Para `preferencias`, o Contract declara explicitamente como `marca preferida` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `marca preferida` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `marca preferida` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `marca preferida` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `marca preferida` em campo, threshold, lista permitida ou failure code antes de executar.

#### 5. textura
- Cláusula recomendada: Para `preferencias`, o Contract declara explicitamente como `textura` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `textura` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `textura` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `textura` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `textura` em campo, threshold, lista permitida ou failure code antes de executar.

#### 6. tipo de treino
- Cláusula recomendada: Para `preferencias`, o Contract declara explicitamente como `tipo de treino` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `tipo de treino` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `tipo de treino` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `tipo de treino` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `tipo de treino` em campo, threshold, lista permitida ou failure code antes de executar.

#### 7. praticidade
- Cláusula recomendada: Para `preferencias`, o Contract declara explicitamente como `praticidade` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `praticidade` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `praticidade` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `praticidade` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `praticidade` em campo, threshold, lista permitida ou failure code antes de executar.

#### 8. prazo
- Cláusula recomendada: Para `preferencias`, o Contract declara explicitamente como `prazo` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `prazo` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `prazo` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `prazo` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `prazo` em campo, threshold, lista permitida ou failure code antes de executar.

#### 9. forma de pagamento
- Cláusula recomendada: Para `preferencias`, o Contract declara explicitamente como `forma de pagamento` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `forma de pagamento` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `forma de pagamento` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `forma de pagamento` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `forma de pagamento` em campo, threshold, lista permitida ou failure code antes de executar.

#### 10. sustentabilidade
- Cláusula recomendada: Para `preferencias`, o Contract declara explicitamente como `sustentabilidade` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `sustentabilidade` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `sustentabilidade` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `sustentabilidade` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `sustentabilidade` em campo, threshold, lista permitida ou failure code antes de executar.

### Cláusulas para `regras_negocio`

#### 1. estoque mínimo
- Cláusula recomendada: Para `regras_negocio`, o Contract declara explicitamente como `estoque mínimo` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `estoque mínimo` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `estoque mínimo` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `estoque mínimo` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `estoque mínimo` em campo, threshold, lista permitida ou failure code antes de executar.

#### 2. categoria elegível
- Cláusula recomendada: Para `regras_negocio`, o Contract declara explicitamente como `categoria elegível` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `categoria elegível` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `categoria elegível` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `categoria elegível` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `categoria elegível` em campo, threshold, lista permitida ou failure code antes de executar.

#### 3. cupom único
- Cláusula recomendada: Para `regras_negocio`, o Contract declara explicitamente como `cupom único` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `cupom único` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `cupom único` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `cupom único` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `cupom único` em campo, threshold, lista permitida ou failure code antes de executar.

#### 4. preço mínimo
- Cláusula recomendada: Para `regras_negocio`, o Contract declara explicitamente como `preço mínimo` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `preço mínimo` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `preço mínimo` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `preço mínimo` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `preço mínimo` em campo, threshold, lista permitida ou failure code antes de executar.

#### 5. margem
- Cláusula recomendada: Para `regras_negocio`, o Contract declara explicitamente como `margem` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `margem` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `margem` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `margem` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `margem` em campo, threshold, lista permitida ou failure code antes de executar.

#### 6. LGPD
- Cláusula recomendada: Para `regras_negocio`, o Contract declara explicitamente como `LGPD` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `LGPD` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `LGPD` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `LGPD` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `LGPD` em campo, threshold, lista permitida ou failure code antes de executar.

#### 7. sem conselho médico
- Cláusula recomendada: Para `regras_negocio`, o Contract declara explicitamente como `sem conselho médico` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `sem conselho médico` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `sem conselho médico` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `sem conselho médico` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `sem conselho médico` em campo, threshold, lista permitida ou failure code antes de executar.

#### 8. sem cobrança sem consentimento
- Cláusula recomendada: Para `regras_negocio`, o Contract declara explicitamente como `sem cobrança sem consentimento` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `sem cobrança sem consentimento` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `sem cobrança sem consentimento` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `sem cobrança sem consentimento` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `sem cobrança sem consentimento` em campo, threshold, lista permitida ou failure code antes de executar.

#### 9. política de troca
- Cláusula recomendada: Para `regras_negocio`, o Contract declara explicitamente como `política de troca` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `política de troca` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `política de troca` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `política de troca` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `política de troca` em campo, threshold, lista permitida ou failure code antes de executar.

#### 10. janela de entrega
- Cláusula recomendada: Para `regras_negocio`, o Contract declara explicitamente como `janela de entrega` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `janela de entrega` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `janela de entrega` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `janela de entrega` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `janela de entrega` em campo, threshold, lista permitida ou failure code antes de executar.

### Cláusulas para `kpis`

#### 1. approval rate
- Cláusula recomendada: Para `kpis`, o Contract declara explicitamente como `approval rate` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `approval rate` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `approval rate` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `approval rate` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `approval rate` em campo, threshold, lista permitida ou failure code antes de executar.

#### 2. rework rate
- Cláusula recomendada: Para `kpis`, o Contract declara explicitamente como `rework rate` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `rework rate` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `rework rate` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `rework rate` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `rework rate` em campo, threshold, lista permitida ou failure code antes de executar.

#### 3. constraint accuracy
- Cláusula recomendada: Para `kpis`, o Contract declara explicitamente como `constraint accuracy` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `constraint accuracy` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `constraint accuracy` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `constraint accuracy` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `constraint accuracy` em campo, threshold, lista permitida ou failure code antes de executar.

#### 4. fit score
- Cláusula recomendada: Para `kpis`, o Contract declara explicitamente como `fit score` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `fit score` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `fit score` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `fit score` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `fit score` em campo, threshold, lista permitida ou failure code antes de executar.

#### 5. latency
- Cláusula recomendada: Para `kpis`, o Contract declara explicitamente como `latency` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `latency` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `latency` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `latency` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `latency` em campo, threshold, lista permitida ou failure code antes de executar.

#### 6. token cost
- Cláusula recomendada: Para `kpis`, o Contract declara explicitamente como `token cost` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `token cost` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `token cost` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `token cost` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `token cost` em campo, threshold, lista permitida ou failure code antes de executar.

#### 7. conversion intent
- Cláusula recomendada: Para `kpis`, o Contract declara explicitamente como `conversion intent` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `conversion intent` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `conversion intent` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `conversion intent` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `conversion intent` em campo, threshold, lista permitida ou failure code antes de executar.

#### 8. escalation rate
- Cláusula recomendada: Para `kpis`, o Contract declara explicitamente como `escalation rate` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `escalation rate` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `escalation rate` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `escalation rate` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `escalation rate` em campo, threshold, lista permitida ou failure code antes de executar.

#### 9. policy violation rate
- Cláusula recomendada: Para `kpis`, o Contract declara explicitamente como `policy violation rate` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `policy violation rate` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `policy violation rate` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `policy violation rate` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `policy violation rate` em campo, threshold, lista permitida ou failure code antes de executar.

#### 10. customer trust score
- Cláusula recomendada: Para `kpis`, o Contract declara explicitamente como `customer trust score` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `customer trust score` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `customer trust score` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `customer trust score` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `customer trust score` em campo, threshold, lista permitida ou failure code antes de executar.

### Cláusulas para `thresholds`

#### 1. score mínimo
- Cláusula recomendada: Para `thresholds`, o Contract declara explicitamente como `score mínimo` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `score mínimo` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `score mínimo` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `score mínimo` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `score mínimo` em campo, threshold, lista permitida ou failure code antes de executar.

#### 2. latência máxima
- Cláusula recomendada: Para `thresholds`, o Contract declara explicitamente como `latência máxima` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `latência máxima` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `latência máxima` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `latência máxima` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `latência máxima` em campo, threshold, lista permitida ou failure code antes de executar.

#### 3. custo máximo
- Cláusula recomendada: Para `thresholds`, o Contract declara explicitamente como `custo máximo` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `custo máximo` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `custo máximo` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `custo máximo` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `custo máximo` em campo, threshold, lista permitida ou failure code antes de executar.

#### 4. erro zero em alergia
- Cláusula recomendada: Para `thresholds`, o Contract declara explicitamente como `erro zero em alergia` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `erro zero em alergia` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `erro zero em alergia` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `erro zero em alergia` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `erro zero em alergia` em campo, threshold, lista permitida ou failure code antes de executar.

#### 5. erro zero em cobrança
- Cláusula recomendada: Para `thresholds`, o Contract declara explicitamente como `erro zero em cobrança` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `erro zero em cobrança` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `erro zero em cobrança` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `erro zero em cobrança` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `erro zero em cobrança` em campo, threshold, lista permitida ou failure code antes de executar.

#### 6. retrabalho máximo
- Cláusula recomendada: Para `thresholds`, o Contract declara explicitamente como `retrabalho máximo` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `retrabalho máximo` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `retrabalho máximo` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `retrabalho máximo` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `retrabalho máximo` em campo, threshold, lista permitida ou failure code antes de executar.

#### 7. confiança mínima
- Cláusula recomendada: Para `thresholds`, o Contract declara explicitamente como `confiança mínima` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `confiança mínima` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `confiança mínima` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `confiança mínima` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `confiança mínima` em campo, threshold, lista permitida ou failure code antes de executar.

#### 8. estoque mínimo
- Cláusula recomendada: Para `thresholds`, o Contract declara explicitamente como `estoque mínimo` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `estoque mínimo` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `estoque mínimo` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `estoque mínimo` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `estoque mínimo` em campo, threshold, lista permitida ou failure code antes de executar.

#### 9. desconto máximo
- Cláusula recomendada: Para `thresholds`, o Contract declara explicitamente como `desconto máximo` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `desconto máximo` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `desconto máximo` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `desconto máximo` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `desconto máximo` em campo, threshold, lista permitida ou failure code antes de executar.

#### 10. tentativas máximas
- Cláusula recomendada: Para `thresholds`, o Contract declara explicitamente como `tentativas máximas` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `tentativas máximas` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `tentativas máximas` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `tentativas máximas` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `tentativas máximas` em campo, threshold, lista permitida ou failure code antes de executar.

### Cláusulas para `medicao`

#### 1. trace JSON
- Cláusula recomendada: Para `medicao`, o Contract declara explicitamente como `trace JSON` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `trace JSON` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `trace JSON` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `trace JSON` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `trace JSON` em campo, threshold, lista permitida ou failure code antes de executar.

#### 2. snapshot de catálogo
- Cláusula recomendada: Para `medicao`, o Contract declara explicitamente como `snapshot de catálogo` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `snapshot de catálogo` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `snapshot de catálogo` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `snapshot de catálogo` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `snapshot de catálogo` em campo, threshold, lista permitida ou failure code antes de executar.

#### 3. log de preço
- Cláusula recomendada: Para `medicao`, o Contract declara explicitamente como `log de preço` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `log de preço` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `log de preço` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `log de preço` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `log de preço` em campo, threshold, lista permitida ou failure code antes de executar.

#### 4. evento de checkout
- Cláusula recomendada: Para `medicao`, o Contract declara explicitamente como `evento de checkout` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `evento de checkout` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `evento de checkout` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `evento de checkout` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `evento de checkout` em campo, threshold, lista permitida ou failure code antes de executar.

#### 5. resposta final
- Cláusula recomendada: Para `medicao`, o Contract declara explicitamente como `resposta final` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `resposta final` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `resposta final` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `resposta final` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `resposta final` em campo, threshold, lista permitida ou failure code antes de executar.

#### 6. feedback do cliente
- Cláusula recomendada: Para `medicao`, o Contract declara explicitamente como `feedback do cliente` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `feedback do cliente` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `feedback do cliente` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `feedback do cliente` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `feedback do cliente` em campo, threshold, lista permitida ou failure code antes de executar.

#### 7. rubric score
- Cláusula recomendada: Para `medicao`, o Contract declara explicitamente como `rubric score` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `rubric score` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `rubric score` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `rubric score` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `rubric score` em campo, threshold, lista permitida ou failure code antes de executar.

#### 8. audit log
- Cláusula recomendada: Para `medicao`, o Contract declara explicitamente como `audit log` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `audit log` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `audit log` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `audit log` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `audit log` em campo, threshold, lista permitida ou failure code antes de executar.

#### 9. policy engine
- Cláusula recomendada: Para `medicao`, o Contract declara explicitamente como `policy engine` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `policy engine` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `policy engine` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `policy engine` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `policy engine` em campo, threshold, lista permitida ou failure code antes de executar.

#### 10. dashboard semanal
- Cláusula recomendada: Para `medicao`, o Contract declara explicitamente como `dashboard semanal` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `dashboard semanal` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `dashboard semanal` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `dashboard semanal` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `dashboard semanal` em campo, threshold, lista permitida ou failure code antes de executar.

### Cláusulas para `cenarios_de_falha`

#### 1. sem estoque
- Cláusula recomendada: Para `cenarios_de_falha`, o Contract declara explicitamente como `sem estoque` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `sem estoque` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `sem estoque` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `sem estoque` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `sem estoque` em campo, threshold, lista permitida ou failure code antes de executar.

#### 2. catálogo vazio
- Cláusula recomendada: Para `cenarios_de_falha`, o Contract declara explicitamente como `catálogo vazio` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `catálogo vazio` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `catálogo vazio` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `catálogo vazio` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `catálogo vazio` em campo, threshold, lista permitida ou failure code antes de executar.

#### 3. preço muda
- Cláusula recomendada: Para `cenarios_de_falha`, o Contract declara explicitamente como `preço muda` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `preço muda` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `preço muda` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `preço muda` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `preço muda` em campo, threshold, lista permitida ou failure code antes de executar.

#### 4. cupom inválido
- Cláusula recomendada: Para `cenarios_de_falha`, o Contract declara explicitamente como `cupom inválido` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `cupom inválido` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `cupom inválido` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `cupom inválido` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `cupom inválido` em campo, threshold, lista permitida ou failure code antes de executar.

#### 5. pagamento recusado
- Cláusula recomendada: Para `cenarios_de_falha`, o Contract declara explicitamente como `pagamento recusado` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `pagamento recusado` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `pagamento recusado` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `pagamento recusado` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `pagamento recusado` em campo, threshold, lista permitida ou failure code antes de executar.

#### 6. endereço inválido
- Cláusula recomendada: Para `cenarios_de_falha`, o Contract declara explicitamente como `endereço inválido` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `endereço inválido` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `endereço inválido` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `endereço inválido` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `endereço inválido` em campo, threshold, lista permitida ou failure code antes de executar.

#### 7. alergia ambígua
- Cláusula recomendada: Para `cenarios_de_falha`, o Contract declara explicitamente como `alergia ambígua` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `alergia ambígua` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `alergia ambígua` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `alergia ambígua` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `alergia ambígua` em campo, threshold, lista permitida ou failure code antes de executar.

#### 8. mudança de categoria
- Cláusula recomendada: Para `cenarios_de_falha`, o Contract declara explicitamente como `mudança de categoria` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `mudança de categoria` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `mudança de categoria` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `mudança de categoria` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `mudança de categoria` em campo, threshold, lista permitida ou failure code antes de executar.

#### 9. timeout
- Cláusula recomendada: Para `cenarios_de_falha`, o Contract declara explicitamente como `timeout` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `timeout` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `timeout` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `timeout` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `timeout` em campo, threshold, lista permitida ou failure code antes de executar.

#### 10. contradição do cliente
- Cláusula recomendada: Para `cenarios_de_falha`, o Contract declara explicitamente como `contradição do cliente` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `contradição do cliente` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `contradição do cliente` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `contradição do cliente` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `contradição do cliente` em campo, threshold, lista permitida ou failure code antes de executar.

### Cláusulas para `acoes`

#### 1. repetir busca
- Cláusula recomendada: Para `acoes`, o Contract declara explicitamente como `repetir busca` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `repetir busca` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `repetir busca` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `repetir busca` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `repetir busca` em campo, threshold, lista permitida ou failure code antes de executar.

#### 2. pedir clarificação
- Cláusula recomendada: Para `acoes`, o Contract declara explicitamente como `pedir clarificação` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `pedir clarificação` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `pedir clarificação` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `pedir clarificação` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `pedir clarificação` em campo, threshold, lista permitida ou failure code antes de executar.

#### 3. relaxar preferência
- Cláusula recomendada: Para `acoes`, o Contract declara explicitamente como `relaxar preferência` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `relaxar preferência` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `relaxar preferência` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `relaxar preferência` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `relaxar preferência` em campo, threshold, lista permitida ou failure code antes de executar.

#### 4. abrir novo sprint
- Cláusula recomendada: Para `acoes`, o Contract declara explicitamente como `abrir novo sprint` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `abrir novo sprint` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `abrir novo sprint` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `abrir novo sprint` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `abrir novo sprint` em campo, threshold, lista permitida ou failure code antes de executar.

#### 5. escalar humano
- Cláusula recomendada: Para `acoes`, o Contract declara explicitamente como `escalar humano` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `escalar humano` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `escalar humano` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `escalar humano` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `escalar humano` em campo, threshold, lista permitida ou failure code antes de executar.

#### 6. bloquear produto
- Cláusula recomendada: Para `acoes`, o Contract declara explicitamente como `bloquear produto` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `bloquear produto` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `bloquear produto` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `bloquear produto` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `bloquear produto` em campo, threshold, lista permitida ou failure code antes de executar.

#### 7. recarregar snapshot
- Cláusula recomendada: Para `acoes`, o Contract declara explicitamente como `recarregar snapshot` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `recarregar snapshot` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `recarregar snapshot` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `recarregar snapshot` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `recarregar snapshot` em campo, threshold, lista permitida ou failure code antes de executar.

#### 8. explicar impossibilidade
- Cláusula recomendada: Para `acoes`, o Contract declara explicitamente como `explicar impossibilidade` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `explicar impossibilidade` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `explicar impossibilidade` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `explicar impossibilidade` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `explicar impossibilidade` em campo, threshold, lista permitida ou failure code antes de executar.

#### 9. cancelar checkout
- Cláusula recomendada: Para `acoes`, o Contract declara explicitamente como `cancelar checkout` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `cancelar checkout` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `cancelar checkout` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `cancelar checkout` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `cancelar checkout` em campo, threshold, lista permitida ou failure code antes de executar.

#### 10. arquivar falha
- Cláusula recomendada: Para `acoes`, o Contract declara explicitamente como `arquivar falha` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `arquivar falha` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `arquivar falha` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `arquivar falha` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `arquivar falha` em campo, threshold, lista permitida ou failure code antes de executar.

### Cláusulas para `escalacao`

#### 1. risco médico
- Cláusula recomendada: Para `escalacao`, o Contract declara explicitamente como `risco médico` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `risco médico` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `risco médico` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `risco médico` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `risco médico` em campo, threshold, lista permitida ou failure code antes de executar.

#### 2. cobrança
- Cláusula recomendada: Para `escalacao`, o Contract declara explicitamente como `cobrança` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `cobrança` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `cobrança` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `cobrança` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `cobrança` em campo, threshold, lista permitida ou failure code antes de executar.

#### 3. fraude
- Cláusula recomendada: Para `escalacao`, o Contract declara explicitamente como `fraude` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `fraude` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `fraude` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `fraude` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `fraude` em campo, threshold, lista permitida ou failure code antes de executar.

#### 4. cliente irritado
- Cláusula recomendada: Para `escalacao`, o Contract declara explicitamente como `cliente irritado` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `cliente irritado` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `cliente irritado` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `cliente irritado` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `cliente irritado` em campo, threshold, lista permitida ou failure code antes de executar.

#### 5. falha repetida
- Cláusula recomendada: Para `escalacao`, o Contract declara explicitamente como `falha repetida` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `falha repetida` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `falha repetida` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `falha repetida` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `falha repetida` em campo, threshold, lista permitida ou failure code antes de executar.

#### 6. policy conflict
- Cláusula recomendada: Para `escalacao`, o Contract declara explicitamente como `policy conflict` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `policy conflict` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `policy conflict` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `policy conflict` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `policy conflict` em campo, threshold, lista permitida ou failure code antes de executar.

#### 7. dados ausentes críticos
- Cláusula recomendada: Para `escalacao`, o Contract declara explicitamente como `dados ausentes críticos` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `dados ausentes críticos` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `dados ausentes críticos` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `dados ausentes críticos` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `dados ausentes críticos` em campo, threshold, lista permitida ou failure code antes de executar.

#### 8. valor alto
- Cláusula recomendada: Para `escalacao`, o Contract declara explicitamente como `valor alto` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `valor alto` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `valor alto` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `valor alto` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `valor alto` em campo, threshold, lista permitida ou failure code antes de executar.

#### 9. reclamação formal
- Cláusula recomendada: Para `escalacao`, o Contract declara explicitamente como `reclamação formal` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `reclamação formal` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `reclamação formal` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `reclamação formal` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `reclamação formal` em campo, threshold, lista permitida ou failure code antes de executar.

#### 10. incidente de confiança
- Cláusula recomendada: Para `escalacao`, o Contract declara explicitamente como `incidente de confiança` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `incidente de confiança` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `incidente de confiança` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `incidente de confiança` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `incidente de confiança` em campo, threshold, lista permitida ou failure code antes de executar.

### Cláusulas para `generator_concorda`

#### 1. capacidade de buscar
- Cláusula recomendada: Para `generator_concorda`, o Contract declara explicitamente como `capacidade de buscar` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `capacidade de buscar` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `capacidade de buscar` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `capacidade de buscar` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `capacidade de buscar` em campo, threshold, lista permitida ou failure code antes de executar.

#### 2. capacidade de filtrar
- Cláusula recomendada: Para `generator_concorda`, o Contract declara explicitamente como `capacidade de filtrar` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `capacidade de filtrar` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `capacidade de filtrar` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `capacidade de filtrar` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `capacidade de filtrar` em campo, threshold, lista permitida ou failure code antes de executar.

#### 3. capacidade de explicar
- Cláusula recomendada: Para `generator_concorda`, o Contract declara explicitamente como `capacidade de explicar` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `capacidade de explicar` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `capacidade de explicar` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `capacidade de explicar` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `capacidade de explicar` em campo, threshold, lista permitida ou failure code antes de executar.

#### 4. respeito ao budget
- Cláusula recomendada: Para `generator_concorda`, o Contract declara explicitamente como `respeito ao budget` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `respeito ao budget` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `respeito ao budget` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `respeito ao budget` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `respeito ao budget` em campo, threshold, lista permitida ou failure code antes de executar.

#### 5. sem ação externa
- Cláusula recomendada: Para `generator_concorda`, o Contract declara explicitamente como `sem ação externa` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `sem ação externa` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `sem ação externa` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `sem ação externa` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `sem ação externa` em campo, threshold, lista permitida ou failure code antes de executar.

#### 6. trace completo
- Cláusula recomendada: Para `generator_concorda`, o Contract declara explicitamente como `trace completo` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `trace completo` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `trace completo` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `trace completo` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `trace completo` em campo, threshold, lista permitida ou failure code antes de executar.

#### 7. falha honesta
- Cláusula recomendada: Para `generator_concorda`, o Contract declara explicitamente como `falha honesta` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `falha honesta` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `falha honesta` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `falha honesta` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `falha honesta` em campo, threshold, lista permitida ou failure code antes de executar.

#### 8. sem improviso
- Cláusula recomendada: Para `generator_concorda`, o Contract declara explicitamente como `sem improviso` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `sem improviso` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `sem improviso` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `sem improviso` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `sem improviso` em campo, threshold, lista permitida ou failure code antes de executar.

#### 9. versão correta
- Cláusula recomendada: Para `generator_concorda`, o Contract declara explicitamente como `versão correta` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `versão correta` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `versão correta` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `versão correta` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `versão correta` em campo, threshold, lista permitida ou failure code antes de executar.

#### 10. pronto para execução
- Cláusula recomendada: Para `generator_concorda`, o Contract declara explicitamente como `pronto para execução` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `pronto para execução` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `pronto para execução` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `pronto para execução` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `pronto para execução` em campo, threshold, lista permitida ou failure code antes de executar.

### Cláusulas para `evaluator_concorda`

#### 1. critérios testáveis
- Cláusula recomendada: Para `evaluator_concorda`, o Contract declara explicitamente como `critérios testáveis` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `critérios testáveis` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `critérios testáveis` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `critérios testáveis` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `critérios testáveis` em campo, threshold, lista permitida ou failure code antes de executar.

#### 2. fontes disponíveis
- Cláusula recomendada: Para `evaluator_concorda`, o Contract declara explicitamente como `fontes disponíveis` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `fontes disponíveis` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `fontes disponíveis` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `fontes disponíveis` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `fontes disponíveis` em campo, threshold, lista permitida ou failure code antes de executar.

#### 3. thresholds claros
- Cláusula recomendada: Para `evaluator_concorda`, o Contract declara explicitamente como `thresholds claros` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `thresholds claros` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `thresholds claros` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `thresholds claros` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `thresholds claros` em campo, threshold, lista permitida ou failure code antes de executar.

#### 4. falhas classificáveis
- Cláusula recomendada: Para `evaluator_concorda`, o Contract declara explicitamente como `falhas classificáveis` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `falhas classificáveis` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `falhas classificáveis` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `falhas classificáveis` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `falhas classificáveis` em campo, threshold, lista permitida ou failure code antes de executar.

#### 5. schema validável
- Cláusula recomendada: Para `evaluator_concorda`, o Contract declara explicitamente como `schema validável` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `schema validável` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `schema validável` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `schema validável` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `schema validável` em campo, threshold, lista permitida ou failure code antes de executar.

#### 6. constraints priorizadas
- Cláusula recomendada: Para `evaluator_concorda`, o Contract declara explicitamente como `constraints priorizadas` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `constraints priorizadas` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `constraints priorizadas` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `constraints priorizadas` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `constraints priorizadas` em campo, threshold, lista permitida ou failure code antes de executar.

#### 7. métricas observáveis
- Cláusula recomendada: Para `evaluator_concorda`, o Contract declara explicitamente como `métricas observáveis` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `métricas observáveis` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `métricas observáveis` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `métricas observáveis` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `métricas observáveis` em campo, threshold, lista permitida ou failure code antes de executar.

#### 8. veto preservado
- Cláusula recomendada: Para `evaluator_concorda`, o Contract declara explicitamente como `veto preservado` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `veto preservado` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `veto preservado` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `veto preservado` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `veto preservado` em campo, threshold, lista permitida ou failure code antes de executar.

#### 9. sign-off registrado
- Cláusula recomendada: Para `evaluator_concorda`, o Contract declara explicitamente como `sign-off registrado` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `sign-off registrado` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `sign-off registrado` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `sign-off registrado` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `sign-off registrado` em campo, threshold, lista permitida ou failure code antes de executar.

#### 10. pronto para verificar
- Cláusula recomendada: Para `evaluator_concorda`, o Contract declara explicitamente como `pronto para verificar` influencia o sprint e qual evidência o Evaluator deve observar.
- Exemplo KODA: Em uma conversa como a de João, `pronto para verificar` precisa aparecer no trace quando altera recomendação, bloqueio, preço ou escalacao.
- Validação: O Evaluator aprova apenas se `pronto para verificar` estiver coerente com Input Specification, Success Criteria e Constraints.
- Falha comum: O Generator trata `pronto para verificar` como detalhe narrativo e não como dado operacional verificável.
- Correção: Converter `pronto para verificar` em campo, threshold, lista permitida ou failure code antes de executar.

---

## 🧪 Cenários de Teste para Qualquer Sprint Contract


### Cenário 1: João mantém orçamento R$ 100, mas aceita outro sabor

**Comportamento esperado:** Preferência muda, constraint não muda; mesmo sprint pode continuar.

**Perguntas de validação:**
- O Contract diferencia restrição rígida de preferência flexível?
- O Generator sabe se deve continuar, renegociar ou escalar?
- O Evaluator tem evidência suficiente para aprovar ou rejeitar?
- A resposta ao cliente preserva confiança sem inventar disponibilidade?
- O trace permite explicar a decisão em incident review?

### Cenário 2: João muda de whey para BCAA

**Comportamento esperado:** Categoria muda; novo Contract obrigatório.

**Perguntas de validação:**
- O Contract diferencia restrição rígida de preferência flexível?
- O Generator sabe se deve continuar, renegociar ou escalar?
- O Evaluator tem evidência suficiente para aprovar ou rejeitar?
- A resposta ao cliente preserva confiança sem inventar disponibilidade?
- O trace permite explicar a decisão em incident review?

### Cenário 3: Catálogo retorna apenas dois produtos sem lactose

**Comportamento esperado:** Falha parcial; pedir relaxamento de sabor ou orçamento.

**Perguntas de validação:**
- O Contract diferencia restrição rígida de preferência flexível?
- O Generator sabe se deve continuar, renegociar ou escalar?
- O Evaluator tem evidência suficiente para aprovar ou rejeitar?
- A resposta ao cliente preserva confiança sem inventar disponibilidade?
- O trace permite explicar a decisão em incident review?

### Cenário 4: Produto seguro fica fora de estoque no meio do sprint

**Comportamento esperado:** Recarregar snapshot e reavaliar sem prometer item indisponível.

**Perguntas de validação:**
- O Contract diferencia restrição rígida de preferência flexível?
- O Generator sabe se deve continuar, renegociar ou escalar?
- O Evaluator tem evidência suficiente para aprovar ou rejeitar?
- A resposta ao cliente preserva confiança sem inventar disponibilidade?
- O trace permite explicar a decisão em incident review?

### Cenário 5: Cupom reduz preço abaixo de R$ 100, mas categoria não permite desconto

**Comportamento esperado:** Promotion Application rejeita cupom; não mascarar como preço válido.

**Perguntas de validação:**
- O Contract diferencia restrição rígida de preferência flexível?
- O Generator sabe se deve continuar, renegociar ou escalar?
- O Evaluator tem evidência suficiente para aprovar ou rejeitar?
- A resposta ao cliente preserva confiança sem inventar disponibilidade?
- O trace permite explicar a decisão em incident review?

### Cenário 6: Cliente diz "tanto faz lactose" após ter informado intolerância

**Comportamento esperado:** Restrição médica persistida exige clarificação ou humano; não relaxar automaticamente.

**Perguntas de validação:**
- O Contract diferencia restrição rígida de preferência flexível?
- O Generator sabe se deve continuar, renegociar ou escalar?
- O Evaluator tem evidência suficiente para aprovar ou rejeitar?
- A resposta ao cliente preserva confiança sem inventar disponibilidade?
- O trace permite explicar a decisão em incident review?

### Cenário 7: Preço aparece como R$ 99,999 no sistema

**Comportamento esperado:** Aplicar regra de arredondamento antes de validar orçamento.

**Perguntas de validação:**
- O Contract diferencia restrição rígida de preferência flexível?
- O Generator sabe se deve continuar, renegociar ou escalar?
- O Evaluator tem evidência suficiente para aprovar ou rejeitar?
- A resposta ao cliente preserva confiança sem inventar disponibilidade?
- O trace permite explicar a decisão em incident review?

### Cenário 8: Evaluator não consegue acessar metadata de ingredientes

**Comportamento esperado:** Falhar seguro e não recomendar produto com risco.

**Perguntas de validação:**
- O Contract diferencia restrição rígida de preferência flexível?
- O Generator sabe se deve continuar, renegociar ou escalar?
- O Evaluator tem evidência suficiente para aprovar ou rejeitar?
- A resposta ao cliente preserva confiança sem inventar disponibilidade?
- O trace permite explicar a decisão em incident review?

### Cenário 9: Generator excede token budget tentando explicar tudo

**Comportamento esperado:** Parar, resumir evidência e evitar output caro sem ganho de qualidade.

**Perguntas de validação:**
- O Contract diferencia restrição rígida de preferência flexível?
- O Generator sabe se deve continuar, renegociar ou escalar?
- O Evaluator tem evidência suficiente para aprovar ou rejeitar?
- A resposta ao cliente preserva confiança sem inventar disponibilidade?
- O trace permite explicar a decisão em incident review?

### Cenário 10: Trace não registra contract_id

**Comportamento esperado:** Rejeitar execução como não auditável.

**Perguntas de validação:**
- O Contract diferencia restrição rígida de preferência flexível?
- O Generator sabe se deve continuar, renegociar ou escalar?
- O Evaluator tem evidência suficiente para aprovar ou rejeitar?
- A resposta ao cliente preserva confiança sem inventar disponibilidade?
- O trace permite explicar a decisão em incident review?

---

## 🧾 Schemas JSON Operacionais


Os schemas abaixo mostram como representar o Contract em forma legível por máquina. Eles não substituem a explicação humana; eles garantem que o harness consiga validar estrutura antes de executar.

### Schema Resumido de Contract

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "KODA Sprint Contract",
  "type": "object",
  "required": [
    "contract_id",
    "contract_version",
    "sprint",
    "input_specification",
    "success_criteria",
    "constraints",
    "metrics",
    "failure_handling",
    "sign_off"
  ],
  "properties": {
    "contract_id": {"type": "string", "minLength": 12},
    "contract_version": {"type": "string", "pattern": "^[0-9]+\\.[0-9]+\\.[0-9]+$"},
    "sprint": {
      "type": "object",
      "required": ["name", "generator", "evaluator", "token_budget", "max_attempts"],
      "properties": {
        "name": {"type": "string"},
        "generator": {"type": "string"},
        "evaluator": {"type": "string"},
        "token_budget": {"type": "integer", "minimum": 1000},
        "max_attempts": {"type": "integer", "minimum": 1, "maximum": 5}
      }
    },
    "input_specification": {"type": "object"},
    "success_criteria": {"type": "object"},
    "constraints": {"type": "object"},
    "metrics": {"type": "object"},
    "failure_handling": {"type": "object"},
    "sign_off": {
      "type": "object",
      "required": ["generator_concorda", "evaluator_concorda", "signed_at"],
      "properties": {
        "generator_concorda": {"type": "boolean", "const": true},
        "evaluator_concorda": {"type": "boolean", "const": true},
        "signed_at": {"type": "string"}
      }
    }
  }
}
```

### Event Log de Lifecycle

```json
[
  {"step": "PROPOSE", "actor": "ProductDiscoveryGenerator", "event": "contract_proposed", "contract_id": "koda-discover-products-joao-2026-05-28-v1"},
  {"step": "NEGOTIATE", "actor": "ProductQualityEvaluator", "event": "added_lactose_trace_requirement", "severity": "critical"},
  {"step": "AGREE", "actor": "both", "event": "contract_signed", "version": "1.0.0"},
  {"step": "EXECUTE", "actor": "ProductDiscoveryGenerator", "event": "three_options_generated", "token_cost": 8420},
  {"step": "VERIFY", "actor": "ProductQualityEvaluator", "event": "contract_approved", "fit_score": 92},
  {"step": "CLOSE", "actor": "ContractArchive", "event": "contract_archived_for_reuse", "template": "complex_product_discovery"}
]
```

---

## 🎓 O Que Você Aprendeu


Sprint Contracts parecem documentação, mas funcionam como arquitetura. Eles mudam o comportamento do sistema porque obrigam agentes a concordarem sobre input, critérios, constraints, métricas, falhas e aprovação antes da execução.

### Key takeaways

1. Um Sprint Contract é um acordo explícito e testável entre Generator e Evaluator, não uma task description bonita.
2. Input Specification reduz Context Amnesia porque transforma informações críticas em campos rastreáveis.
3. Success Criteria precisam ser verificáveis; se o Evaluator não consegue testar, o critério ainda está vago.
4. Constraints protegem cliente e negócio; alergias, orçamento e cobrança têm prioridade sobre criatividade.
5. Metrics tornam aprendizado possível, porque mostram custo, qualidade, retrabalho e confiança ao longo do tempo.
6. Failure Handling é parte do design, não plano secundário; falhar com segurança é melhor que forçar sucesso falso.
7. Sign-off evita execução desalinhada e cria base auditável para trace reading, incident review e template reuse.

### Self-assessment checkpoint

- [ ] Consigo explicar a diferença entre Generator/Evaluator e Sprint Contract.
- [ ] Consigo escrever Input Specification sem misturar contexto com constraints.
- [ ] Consigo transformar "produto bom" em critérios testáveis.
- [ ] Consigo definir o que acontece quando não há produto seguro para João.
- [ ] Consigo desenhar um Contract de checkout sem permitir cobrança sem consentimento.
- [ ] Consigo identificar quando mudança de requisito exige novo Contract.
- [ ] Consigo apontar quais métricas provam que o sprint funcionou.
- [ ] Consigo revisar um Contract e encontrar vagueza antes da execução.

### Conexão com Próximos Módulos

- **Rubric Design:** usa os critérios do Contract para avaliar qualidade com score, pesos e thresholds.
- **Trace Reading:** usa contract_id, failure codes e event logs para descobrir onde a execução desviou.
- **State Persistence:** mantém constraints e decisões aprovadas entre sprints longos.
- **Multi-Agent Systems:** escala Contracts para múltiplos Generators, Evaluators e coordinators.
- **Harness Evolution:** ajusta templates com base em falhas reais, métricas e incident reviews.

### Pro tip

> Um Contract bom não tenta prever cada frase do cliente. Ele define como o sistema decide quando continuar, quando parar, quando renegociar e quando proteger o cliente mesmo que isso reduza conversão no curto prazo.

---

## 📚 Referências & Próximos Passos


- `curriculum/01-nivel-1-fundamentals/01-why-agents-lose-plot.md` para entender os problemas fundamentais que Contracts ajudam a controlar.
- `curriculum/02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md` para dominar separação entre geração e avaliação.
- `curriculum/02-nivel-2-practical-patterns/02-sprint-contracts.md` para teoria completa do padrão.
- `curriculum/02-nivel-2-practical-patterns/03-rubric-design.md` para transformar criteria em avaliação de qualidade.
- `curriculum/02-nivel-2-practical-patterns/04-trace-reading.md` para debugar violações de Contract.
- `curriculum/09-case-studies/03-koda-product-discovery.md` para estudar Product Discovery em profundidade.
- `curriculum/09-case-studies/04-koda-order-processing.md` para estudar Process Order multi-step.

### Próximos Passos Práticos

1. Escolha uma conversa real do KODA com recomendação de produto.
2. Escreva o Contract usando este template antes de olhar a resposta final.
3. Peça para um Evaluator revisar apenas o Contract e apontar vagueza.
4. Execute o Generator com contract_id registrado no trace.
5. Compare output final contra Success Criteria e Failure Handling.
6. Arquive métricas e ajuste o template quando encontrar uma cláusula fraca.

### Frase Final

Quando Fernando diz que KODA precisa ser um amigo de confiança, ele não está pedindo respostas mais bonitas. Ele está pedindo arquitetura que cumpra promessas. Sprint Contracts são o lugar onde essas promessas ficam explícitas.

---

**Fim do template.** Este arquivo é completo para uso como referência de Sprint Contracts no KODA e deve ser versionado junto com a biblioteca operacional de templates.
