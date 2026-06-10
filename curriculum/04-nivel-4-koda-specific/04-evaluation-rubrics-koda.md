---
title: "Evaluation Rubrics para KODA"
type: curriculum-lesson
nivel: 4
aliases: ["rubricas KODA", "avaliação KODA", "KODA evals", "business validation"]
tags: [curriculo-conteudo, nivel-4, koda, rubricas-de-avaliacao, avaliacao-de-qualidade, validacao-negocial, recomendacao-de-produtos, resposta-ao-cliente, negociacao-de-preco, follow-up, calibracao-de-evaluadores, feedback-loop, human-review]
relates-to: ["[[docs/canonical/eval-tier-stratification|Eval Tier Stratification]]", "[[docs/canonical/pain-signal-eval-progression-gate|Pain-Signal Eval Progression Gate]]", "[[curriculum/05-core-concepts/08-evaluation-rubrics|Evaluation Rubrics Concept]]"]
last_updated: 2026-06-10
---
# 📏 Evaluation Rubrics para KODA
## Como transformar qualidade conversacional em decisões auditáveis de negócio

**Tempo Estimado:** 150-180 minutos
**Nível:** 4 - KODA Specific
**Pré-requisitos:** Generator/Evaluator, Sprint Contracts, Rubric Design, Trace Reading e arquitetura operacional do KODA
**Status:** 🟢 CRÍTICO - Gatekeeper de qualidade para recomendações, respostas, negociação e follow-up
**Data de Criação:** Maio 2026
**Pertence a:** `04-nivel-4-koda-specific/`
**Output Esperado:** você sairá capaz de operar rubrics KODA com `rubric_id`, `approval_threshold`, `confidence_score`, `overall_score` e `generation_id` auditáveis.

---

## 📖 Prólogo: A Avaliação Real que Mudou a Operação

Naquela manhã, Fernando não estava revisando uma demo. Ele estava revisando uma conversa que poderia virar uma venda, uma reclamação pública, ou uma perda de confiança. O cliente não queria uma resposta bonita; queria segurança, precisão e respeito ao próprio contexto.

A conversa parecia simples: um pedido de recomendação de suplemento. Mas KODA não é um chatbot genérico. KODA atua em WhatsApp, com histórico longo, preferências acumuladas, restrições alimentares, orçamento, tom de relacionamento e pressão comercial real.

Veja o fluxo que Fernando analisou:

```
09:12 - Cliente: Bom dia, KODA. Quero um suplemento para ganhar massa, mas tenho gastrite e não posso gastar mais de R$ 140.
09:13 - KODA Generator: Fernando viu o draft nascer rápido: uma recomendação simpática, três produtos populares, tom confiante e uma frase final chamando para compra.
09:14 - Fernando: A resposta parecia boa. Parecia humana. Parecia vendável. E era exatamente por isso que era perigosa.
09:15 - Evaluator: O rubric rodou e marcou `overall_score: 0.58`. O produto principal continha alto teor de cafeína. A resposta ignorava gastrite. O tom empurrava compra antes de confirmar restrição médica.
09:16 - Decisão: `REJEITAR_IMEDIATAMENTE`. Não por estilo. Não por preferência subjetiva. Por risco real de negócio e saúde.
```

Sem rubric, alguém poderia dizer: "a resposta está boa, só precisa de ajuste fino". Com rubric, a decisão ficou objetiva: **não publicar**. O Evaluator não julgou se gostou da frase. Ele mediu dimensoes explícitas: precisão de produto, relevância ao contexto, segurança, tom, fechamento e risco.

Essa diferença é o coração deste módulo.

Você já viu no Nível 2 que um Evaluator não pode ser apenas um "sim ou não". Você também viu que self-evaluation colapsa por sycophancy: o mesmo agente que gerou tende a defender a própria geração. No Nível 4, a pergunta muda: **como desenhar rubrics operacionais específicos para KODA, onde cada saída tem impacto comercial e relacional?**

A resposta é: rubrics com criterios mensuraveis, pesos, escalas, exemplos, blockers e decisão auditável. Não basta validar que o JSON está bem formado. `output validation` confirma estrutura. `business validation` confirma se a resposta serve para o cliente, para a operação e para a confiança da marca.

---

## 🎯 O Que Voce Vai Aprender

- ✅ Criar rubrics KODA para quatro famílias críticas: Product Recommendation, Customer Response, Price Negotiation e Follow-Up.
- ✅ Diferenciar output validation de business validation sem misturar rubric scoring com Sprint Contracts.
- ✅ Definir dimensoes, escalas, exemplos, pesos, blockers e decision logic para cada tipo de output.
- ✅ Integrar Generator e Evaluator com draft, verdict, feedback loop, max iterations, escalation e audit log/state files.
- ✅ Usar `rubric_id`, `generation_id`, `approval_threshold`, `confidence_score` e `overall_score` como linguagem operacional comum.
- ✅ Calibrar avaliadores com exemplos bons e ruins, evitando sycophancy e rejeições arbitrárias.
- ✅ Aplicar rubrics a conversas reais de Fernando e clientes no WhatsApp, com diálogo, decisão e próxima ação.

Ao final, você deve conseguir olhar para uma resposta do KODA e explicar, com evidência: **por que aprovar, por que aprovar com ressalvas, por que rejeitar, ou por que rejeitar imediatamente**.

---

## 🔗 Como Este Modulo Se Conecta

| Conceito anterior | Papel neste módulo | Limite que você deve respeitar |
|-------------------|--------------------|--------------------------------|
| Generator/Evaluator | Separa criação de julgamento crítico | Rubric scoring não é self-evaluation |
| Sprint Contracts | Define Input Specification, Success Criteria e Failure Handling do sprint | Sprint Contract é acordo de execução, não substitui rubric |
| Rubric Design | Ensina anatomia geral de rubrics | Aqui o foco é KODA operacional, não teoria genérica |
| Trace Reading | Ajuda a investigar por que uma decisão foi tomada | Trace não corrige sozinho; ele revela evidência |
| State Persistence | Guarda contexto e audit log/state files | Estado persistido não garante qualidade sem avaliação |

Pense assim:

```
Sprint Contract diz: "qual trabalho será feito e quando termina"
Rubric diz:          "quão boa foi a saída e se pode chegar ao cliente"
Trace Reading diz:   "como chegamos nessa decisão"
State Persistence:   "onde guardamos contexto, decisão e evidência"
```

Neste módulo, rubrics são tratados como **gatekeeper de qualidade**, não como documentação bonita. Se o Evaluator aplica uma rubrica e decide `REJEITAR`, o output não deve sair para o cliente sem nova geração ou escalonamento.

---

## 🏗️ Arquitetura de Avaliacao KODA

A arquitetura de avaliação do KODA precisa mostrar explicitamente onde a qualidade é medida. O Generator não decide sozinho. Ele produz um draft. O Evaluator aplica um rubric. O resultado vira score, feedback e decisão.

```
+------------------+      +------------------+      +------------------+
| CUSTOMER CONTEXT | ---> |    Generator     | ---> |  Draft Output    |
| history, budget  |      | creates response |      | generation_id    |
| goals, risks     |      | no self scoring  |      | rubric_id target |
+---------+--------+      +---------+--------+      +---------+--------+
          |                         |                         |
          |                         v                         v
          |              +------------------+      +------------------+
          |              |  State Files     |      |    Evaluator     |
          |              | draft + context  | ---> | applies rubric   |
          |              | audit log        |      | measures quality |
          |              +------------------+      +---------+--------+
          |                                                   |
          |                                                   v
          |                                        +------------------+
          |                                        |  Rubric Score    |
          |                                        | overall_score    |
          |                                        | confidence_score |
          |                                        +---------+--------+
          |                                                   |
          |                                                   v
          |      +------------------+      +------------------+      +------------------+
          +----> | Feedback Loop    | <--- | Decision Engine  | ---> | Customer Output  |
                 | revise or retry  |      | approve/reject   |      | only if approved |
                 +------------------+      +------------------+      +------------------+
```

O caminho feliz é simples: contexto entra, Generator cria, Evaluator mede, score passa do `approval_threshold`, e a resposta vai ao cliente. Mas sistemas reais precisam lidar com falha.

| Decisão | Quando usar | Próxima ação |
|---------|-------------|--------------|
| `APROVAR` | `overall_score` alto, nenhum blocker, `confidence_score` suficiente | Enviar ao cliente e registrar audit log |
| `APROVAR_COM_RESSALVAS` | Pequenas imperfeições sem risco de negócio | Enviar com ajuste automático ou revisão leve |
| `REJEITAR` | Falha corrigível em relevância, tom, completude ou estrutura | Feedback para Generator e nova iteração |
| `REJEITAR_IMEDIATAMENTE` | Risco médico, preço falso, promessa proibida, desrespeito, violação de política | Bloquear envio, escalar para humano ou fluxo seguro |

O Evaluator é gatekeeper. Se ele for fraco, KODA volta ao problema de Nível 1: output bonito, confiança falsa, risco invisível.

---

## 🧭 Estrategias de Coordenacao

Antes de desenhar rubrics, você precisa decidir como Generator, Evaluator, state files e decisão se coordenam. Esta escolha muda latência, auditabilidade e complexidade operacional.

| Estratégia | Como funciona | Pontos fortes | Riscos | Melhor uso no KODA |
|------------|---------------|---------------|--------|--------------------|
| File-based | Generator escreve `draft.json`; Evaluator lê, escreve `verdict.json`; Decision Engine lê ambos | Auditável, simples de debugar, ótimo para long-running agents | Pode ter race condition se não houver locking e versionamento | Conversas longas, avaliação assíncrona, trilha de auditoria |
| In-memory | Objetos passam entre funções no mesmo processo | Baixa latência, menos I/O, simples em requests curtos | Perde evidência se processo cai; difícil reprocessar | Respostas simples de baixo risco e baixa duração |
| API-based | Generator chama serviço Evaluator por HTTP ou RPC | Escala times e linguagens diferentes; contrato claro | Latência de rede, versionamento de schema, autenticação | Avaliação centralizada para múltiplos canais além do WhatsApp |
| Queue-based | Draft entra em fila; Evaluator consome; decisão volta por evento | Resiliente, reprocessável, bom para picos | Mais componentes, eventual consistency, UX precisa lidar com espera | Follow-up em lote, auditoria noturna, campanhas e reavaliações |

Para KODA, a recomendação prática é híbrida: file-based para auditabilidade em conversas complexas, API-based quando o Evaluator virar serviço compartilhado, queue-based para Follow-Up e campanhas, in-memory apenas para saídas triviais de baixo risco.

```
Baixo risco + baixa latência  -> in-memory
Risco médio + precisa debug   -> file-based
Múltiplos produtos/canais     -> API-based
Alto volume assíncrono        -> queue-based
```

---

## 🧬 Anatomia de um Rubric KODA

Um rubric KODA não é uma checklist vaga. Ele é uma especificação operacional que transforma julgamento de qualidade em medição repetível.

Todo rubric deste módulo usa os seguintes componentes:

| Componente | Função | Exemplo |
|------------|--------|---------|
| `rubric_id` | Identificador estável da rubrica | `koda.product_recommendation.v1` |
| `output_type` | Tipo de saída avaliada | `Product Recommendation` |
| `Input Specification` | Dados mínimos que o Evaluator precisa receber | contexto do cliente, catálogo, restrições, draft |
| `dimensions` | Dimensoes avaliadas separadamente | accuracy, relevance, tone, closing |
| `scale` | Escala por dimensão | 0 a 5 com âncoras claras |
| `weights` | Peso de cada dimensão no `overall_score` | accuracy 35%, relevance 25% |
| `blockers` | Falhas que bloqueiam envio mesmo com score alto | preço falso, risco médico, promessa indevida |
| `approval_threshold` | Pontuação mínima para aprovar | 0.82 |
| `confidence_score` | Confiança do Evaluator na própria avaliação | 0.91 |
| `overall_score` | Resultado ponderado final | 0.87 |
| `examples` | Exemplos bons e ruins calibrados | mensagens WhatsApp avaliadas |
| `Failure Handling` | O que fazer quando falha | retry, escalar, pedir dado faltante |

A escala 0-5 usada aqui tem significado fixo:

| Nota | Interpretação operacional |
|------|---------------------------|
| 0 | Violação grave; não pode sair; possível `REJEITAR_IMEDIATAMENTE` |
| 1 | Muito fraco; ignora requisito central ou cria risco |
| 2 | Insuficiente; parcialmente correto, mas com falhas importantes |
| 3 | Aceitável com ressalvas; funciona, mas precisa melhorar |
| 4 | Bom; atende critérios principais com pequenas imperfeições |
| 5 | Excelente; preciso, contextual, seguro, natural e acionável |

Regra central: se um blocker aparece, o `overall_score` não salva a resposta. Uma resposta educada com preço inventado continua sendo rejeitada. Uma negociação respeitosa que promete desconto inexistente continua sendo rejeitada. Um follow-up carinhoso enviado no timing errado continua sendo ruim.

---

### Exemplo de envelope JSON de avaliação

```json
{
  "generation_id": "gen_2026_05_28_091412_fernando_ana",
  "rubric_id": "koda.product_recommendation.v1",
  "output_type": "Product Recommendation",
  "approval_threshold": 0.82,
  "overall_score": 0.58,
  "confidence_score": 0.94,
  "decision": "REJEITAR_IMEDIATAMENTE",
  "dimension_scores": {
    "accuracy": 0.30,
    "relevance": 0.70,
    "tone": 0.80,
    "safety_and_constraints": 0.20,
    "closing": 0.65
  },
  "blockers": [
    "Produto recomendado contém estimulante incompatível com gastrite informada",
    "Resposta empurra compra antes de confirmar restrição de saúde"
  ],
  "feedback_to_generator": [
    "Remover produtos com alto teor de cafeína",
    "Confirmar restrição médica antes de recomendar",
    "Oferecer opção suave e orientar consulta profissional quando houver risco"
  ],
  "audit_log_path": "state/evaluations/gen_2026_05_28_091412_fernando_ana/verdict.json"
}
```

Observe que este JSON não é implementação de produção. Ele é um exemplo operacional de formato: explícito, auditável e legível por humanos. O ponto é ensinar a equipe a pensar em avaliação como artefato de sistema, não como impressão subjetiva.

---

## 🛒 Rubric: Product Recommendation

**`rubric_id`:** `koda.product_recommendation.v1`
**`approval_threshold`:** `0.82`
**Objetivo:** avaliar se uma recomendação de produto é precisa, relevante, segura, personalizada e pronta para virar ação comercial.
**Cenário típico:** cliente pede suplemento com objetivo, restrições e orçamento.

### Input Specification

O Evaluator só deve aplicar este rubric quando recebe dados suficientes. Se o input estiver incompleto, a decisão correta não é fingir confiança; é pedir complemento ou marcar baixa `confidence_score`.

- histórico resumido da conversa com fatos críticos preservados
- mensagem mais recente do cliente
- draft do Generator com `generation_id`
- políticas comerciais e limites atuais aplicáveis
- dados de catálogo, estoque, preço ou agenda quando relevantes
- restrições conhecidas: orçamento, alergias, preferências, opt-out, tom e urgência

### Dimensoes, pesos e criterios mensuraveis

| Dimensão | Peso | O que mede | Nota 5 | Nota 3 | Nota 1 |
|----------|------|------------|--------|--------|--------|
| Accuracy | 30% | Produto existe, preço e estoque estão corretos, atributos batem com catálogo. | atende completamente com evidência | atende parcialmente ou com lacuna pequena | falha no ponto central |
| Relevance | 25% | Produto responde ao objetivo real do cliente, não apenas à palavra-chave. | atende completamente com evidência | atende parcialmente ou com lacuna pequena | falha no ponto central |
| Tone | 15% | Mensagem soa como consultor confiável, não como vendedor agressivo. | atende completamente com evidência | atende parcialmente ou com lacuna pequena | falha no ponto central |
| Safety and Constraints | 20% | Respeita alergias, restrições, contraindicações e limites informados. | atende completamente com evidência | atende parcialmente ou com lacuna pequena | falha no ponto central |
| Actionability | 10% | Próximo passo é claro: escolher sabor, confirmar carrinho ou tirar dúvida. | atende completamente com evidência | atende parcialmente ou com lacuna pequena | falha no ponto central |

### Blockers

- `REJEITAR_IMEDIATAMENTE` quando houver preço inventado.
- `REJEITAR_IMEDIATAMENTE` quando houver produto fora de estoque apresentado como disponível.
- `REJEITAR_IMEDIATAMENTE` quando houver ignorar alergia ou restrição médica.
- `REJEITAR_IMEDIATAMENTE` quando houver prometer resultado físico garantido.
- `REJEITAR_IMEDIATAMENTE` quando houver recomendar item fora do orçamento sem explicar trade-off.

### Exemplo bom

```text
Ana, pelo que você contou - treino de força, orçamento até R$ 140 e gastrite - eu evitaria pré-treinos estimulantes. A melhor opção hoje é o Whey Isolado Neutro 900g por R$ 129,90, em estoque. Ele bate seu objetivo de proteína, cabe no orçamento e tende a ser mais suave. Quer que eu compare com uma opção vegetal também?
```

Por que funciona:
- **Accuracy:** mostra produto existe, preço e estoque estão corretos, atributos batem com catálogo.
- **Relevance:** mostra produto responde ao objetivo real do cliente, não apenas à palavra-chave.
- **Tone:** mostra mensagem soa como consultor confiável, não como vendedor agressivo.
- **Safety and Constraints:** mostra respeita alergias, restrições, contraindicações e limites informados.
- **Actionability:** mostra próximo passo é claro: escolher sabor, confirmar carrinho ou tirar dúvida.

### Exemplo ruim

```text
Compra o Pré-Treino Turbo Max. Ele vai te dar resultado rápido, está bombando e custa só R$ 159,90. Quer fechar?
```

Por que falha:
- Cria risco porque pode envolver preço inventado.
- Cria risco porque pode envolver produto fora de estoque apresentado como disponível.
- Cria risco porque pode envolver ignorar alergia ou restrição médica.

### Diálogo WhatsApp calibrado

```
Cliente: Quero ganhar massa, mas tenho gastrite e até R$ 140.
KODA bom: Vou priorizar proteína e evitar estimulantes por causa da gastrite.
KODA ruim: O mais forte é melhor, então pega o pré-treino.
```

### Decision logic

```
if blocker_detected:
  decision = REJEITAR_IMEDIATAMENTE
elif overall_score >= 0.82 and confidence_score >= 0.75:
  decision = APROVAR
elif overall_score >= 0.74 and confidence_score >= 0.70:
  decision = APROVAR_COM_RESSALVAS
else:
  decision = REJEITAR
```

### JSON de avaliação exemplo

```json
{
  "rubric_id": "koda.product_recommendation.v1",
  "generation_id": "gen_koda_product_recommendation_001",
  "approval_threshold": 0.82,
  "overall_score": 0.88,
  "confidence_score": 0.91,
  "decision": "APROVAR",
  "dimension_scores": {
    "accuracy": 0.88,
    "relevance": 0.88,
    "tone": 0.88,
    "safety_and_constraints": 0.88,
    "actionability": 0.88
  },
  "feedback_to_generator": [
    "Manter evidências de contexto na resposta",
    "Preservar tom consultivo e próximo",
    "Registrar decisão no audit log"
  ]
}
```

### Failure Handling

- Se faltar dado crítico, retornar `REJEITAR` com pedido específico de complemento.
- Se houver blocker, retornar `REJEITAR_IMEDIATAMENTE` e impedir envio ao cliente.
- Se houver falha corrigível, devolver feedback curto ao Generator e permitir nova iteração.
- Se a segunda iteração falhar pelo mesmo motivo, escalar para revisão humana ou fluxo seguro.
- Se a avaliação tiver baixa confiança, registrar `confidence_score` baixo e não tratar aprovação como definitiva.

### KODA application

Fernando usa esta rubrica quando KODA transforma busca de catálogo em recomendação final no WhatsApp.

O ponto operacional é evitar que KODA confunda fluência com qualidade. Uma mensagem pode ser natural e ainda estar errada. Uma mensagem pode vender bem e ainda violar margem. Uma mensagem pode ser simpática e ainda chegar no timing errado.

---

## 💬 Rubric: Customer Response

**`rubric_id`:** `koda.customer_response.v1`
**`approval_threshold`:** `0.80`
**Objetivo:** avaliar se uma resposta ao cliente é correta, empática, contextual e resolve a intenção sem confundir.
**Cenário típico:** cliente faz pergunta, reclamação, objeção, pedido de comparação ou dúvida operacional.

### Input Specification

O Evaluator só deve aplicar este rubric quando recebe dados suficientes. Se o input estiver incompleto, a decisão correta não é fingir confiança; é pedir complemento ou marcar baixa `confidence_score`.

- histórico resumido da conversa com fatos críticos preservados
- mensagem mais recente do cliente
- draft do Generator com `generation_id`
- políticas comerciais e limites atuais aplicáveis
- dados de catálogo, estoque, preço ou agenda quando relevantes
- restrições conhecidas: orçamento, alergias, preferências, opt-out, tom e urgência

### Dimensoes, pesos e criterios mensuraveis

| Dimensão | Peso | O que mede | Nota 5 | Nota 3 | Nota 1 |
|----------|------|------------|--------|--------|--------|
| Intent Understanding | 25% | Identifica o que o cliente realmente quer, inclusive emoção e urgência. | atende completamente com evidência | atende parcialmente ou com lacuna pequena | falha no ponto central |
| Factual Correctness | 25% | Não inventa política, prazo, estoque, preço ou benefício. | atende completamente com evidência | atende parcialmente ou com lacuna pequena | falha no ponto central |
| Empathy and Tone | 20% | Responde com respeito, naturalidade e voz KODA. | atende completamente com evidência | atende parcialmente ou com lacuna pequena | falha no ponto central |
| Completeness | 15% | Cobre a pergunta sem excesso e sem deixar lacuna crítica. | atende completamente com evidência | atende parcialmente ou com lacuna pequena | falha no ponto central |
| Next Step Clarity | 15% | Diz claramente o que acontece agora ou pergunta o dado necessário. | atende completamente com evidência | atende parcialmente ou com lacuna pequena | falha no ponto central |

### Blockers

- `REJEITAR_IMEDIATAMENTE` quando houver culpar o cliente.
- `REJEITAR_IMEDIATAMENTE` quando houver inventar política de troca.
- `REJEITAR_IMEDIATAMENTE` quando houver ignorar reclamação explícita.
- `REJEITAR_IMEDIATAMENTE` quando houver responder outra pergunta.
- `REJEITAR_IMEDIATAMENTE` quando houver usar tom frio em momento sensível.

### Exemplo bom

```text
Poxa, Fernando, entendi a frustração. Você recebeu sabor baunilha, mas tinha escolhido chocolate. Vou verificar o pedido agora e te passar a opção mais rápida: troca sem custo ou crédito imediato para novo pedido. Pode me confirmar se o lacre ainda está fechado?
```

Por que funciona:
- **Intent Understanding:** mostra identifica o que o cliente realmente quer, inclusive emoção e urgência.
- **Factual Correctness:** mostra não inventa política, prazo, estoque, preço ou benefício.
- **Empathy and Tone:** mostra responde com respeito, naturalidade e voz koda.
- **Completeness:** mostra cobre a pergunta sem excesso e sem deixar lacuna crítica.
- **Next Step Clarity:** mostra diz claramente o que acontece agora ou pergunta o dado necessário.

### Exemplo ruim

```text
Isso deve ter sido erro seu na hora da compra. Confere o pedido aí e depois me fala.
```

Por que falha:
- Cria risco porque pode envolver culpar o cliente.
- Cria risco porque pode envolver inventar política de troca.
- Cria risco porque pode envolver ignorar reclamação explícita.

### Diálogo WhatsApp calibrado

```
Cliente: Chegou o sabor errado.
KODA bom: Entendi a frustração e vou resolver com troca ou crédito.
KODA ruim: Você deve ter escolhido errado.
```

### Decision logic

```
if blocker_detected:
  decision = REJEITAR_IMEDIATAMENTE
elif overall_score >= 0.80 and confidence_score >= 0.75:
  decision = APROVAR
elif overall_score >= 0.72 and confidence_score >= 0.70:
  decision = APROVAR_COM_RESSALVAS
else:
  decision = REJEITAR
```

### JSON de avaliação exemplo

```json
{
  "rubric_id": "koda.customer_response.v1",
  "generation_id": "gen_koda_customer_response_001",
  "approval_threshold": 0.80,
  "overall_score": 0.88,
  "confidence_score": 0.91,
  "decision": "APROVAR",
  "dimension_scores": {
    "intent_understanding": 0.88,
    "factual_correctness": 0.88,
    "empathy_and_tone": 0.88,
    "completeness": 0.88,
    "next_step_clarity": 0.88
  },
  "feedback_to_generator": [
    "Manter evidências de contexto na resposta",
    "Preservar tom consultivo e próximo",
    "Registrar decisão no audit log"
  ]
}
```

### Failure Handling

- Se faltar dado crítico, retornar `REJEITAR` com pedido específico de complemento.
- Se houver blocker, retornar `REJEITAR_IMEDIATAMENTE` e impedir envio ao cliente.
- Se houver falha corrigível, devolver feedback curto ao Generator e permitir nova iteração.
- Se a segunda iteração falhar pelo mesmo motivo, escalar para revisão humana ou fluxo seguro.
- Se a avaliação tiver baixa confiança, registrar `confidence_score` baixo e não tratar aprovação como definitiva.

### KODA application

Fernando usa esta rubrica para respostas gerais que não são recomendação, negociação ou follow-up.

O ponto operacional é evitar que KODA confunda fluência com qualidade. Uma mensagem pode ser natural e ainda estar errada. Uma mensagem pode vender bem e ainda violar margem. Uma mensagem pode ser simpática e ainda chegar no timing errado.

---

## 🤝 Rubric: Price Negotiation

**`rubric_id`:** `koda.price_negotiation.v1`
**`approval_threshold`:** `0.84`
**Objetivo:** avaliar se uma negociação de preço combina assertividade, respeito, margem e fechamento sem prometer o que não existe.
**Cenário típico:** cliente pede desconto, compara concorrente, ameaça desistir ou solicita condição especial.

### Input Specification

O Evaluator só deve aplicar este rubric quando recebe dados suficientes. Se o input estiver incompleto, a decisão correta não é fingir confiança; é pedir complemento ou marcar baixa `confidence_score`.

- histórico resumido da conversa com fatos críticos preservados
- mensagem mais recente do cliente
- draft do Generator com `generation_id`
- políticas comerciais e limites atuais aplicáveis
- dados de catálogo, estoque, preço ou agenda quando relevantes
- restrições conhecidas: orçamento, alergias, preferências, opt-out, tom e urgência

### Dimensoes, pesos e criterios mensuraveis

| Dimensão | Peso | O que mede | Nota 5 | Nota 3 | Nota 1 |
|----------|------|------------|--------|--------|--------|
| Assertiveness | 20% | Defende valor e limites comerciais sem soar inseguro. | atende completamente com evidência | atende parcialmente ou com lacuna pequena | falha no ponto central |
| Respect | 20% | Reconhece o cliente e mantém relacionamento mesmo ao negar desconto. | atende completamente com evidência | atende parcialmente ou com lacuna pequena | falha no ponto central |
| Commercial Accuracy | 25% | Usa descontos, cupons, frete e condições reais. | atende completamente com evidência | atende parcialmente ou com lacuna pequena | falha no ponto central |
| Value Framing | 20% | Explica benefício e custo-benefício, não apenas preço. | atende completamente com evidência | atende parcialmente ou com lacuna pequena | falha no ponto central |
| Closing | 15% | Conduz para decisão clara sem pressão indevida. | atende completamente com evidência | atende parcialmente ou com lacuna pequena | falha no ponto central |

### Blockers

- `REJEITAR_IMEDIATAMENTE` quando houver prometer desconto não autorizado.
- `REJEITAR_IMEDIATAMENTE` quando houver pressionar com urgência falsa.
- `REJEITAR_IMEDIATAMENTE` quando houver desrespeitar cliente por pedir desconto.
- `REJEITAR_IMEDIATAMENTE` quando houver aceitar preço abaixo da margem configurada.
- `REJEITAR_IMEDIATAMENTE` quando houver ocultar condição relevante.

### Exemplo bom

```text
Entendo, Fernando. Eu não consigo chegar em R$ 90 nesse whey sem quebrar a condição atual, mas consigo manter R$ 119,90 com frete grátis hoje. A diferença é que ele entrega 25g de proteína por dose e dura 30 porções. Se fizer sentido, já deixo no carrinho com essa condição.
```

Por que funciona:
- **Assertiveness:** mostra defende valor e limites comerciais sem soar inseguro.
- **Respect:** mostra reconhece o cliente e mantém relacionamento mesmo ao negar desconto.
- **Commercial Accuracy:** mostra usa descontos, cupons, frete e condições reais.
- **Value Framing:** mostra explica benefício e custo-benefício, não apenas preço.
- **Closing:** mostra conduz para decisão clara sem pressão indevida.

### Exemplo ruim

```text
Fecho por R$ 90 sim, mas só se você comprar agora. Não conta para ninguém.
```

Por que falha:
- Cria risco porque pode envolver prometer desconto não autorizado.
- Cria risco porque pode envolver pressionar com urgência falsa.
- Cria risco porque pode envolver desrespeitar cliente por pedir desconto.

### Diálogo WhatsApp calibrado

```
Cliente: No concorrente está mais barato.
KODA bom: Não inventa desconto; oferece condição real e explica valor.
KODA ruim: Promete desconto secreto sem autorização.
```

### Decision logic

```
if blocker_detected:
  decision = REJEITAR_IMEDIATAMENTE
elif overall_score >= 0.84 and confidence_score >= 0.75:
  decision = APROVAR
elif overall_score >= 0.76 and confidence_score >= 0.70:
  decision = APROVAR_COM_RESSALVAS
else:
  decision = REJEITAR
```

### JSON de avaliação exemplo

```json
{
  "rubric_id": "koda.price_negotiation.v1",
  "generation_id": "gen_koda_price_negotiation_001",
  "approval_threshold": 0.84,
  "overall_score": 0.88,
  "confidence_score": 0.91,
  "decision": "APROVAR",
  "dimension_scores": {
    "assertiveness": 0.88,
    "respect": 0.88,
    "commercial_accuracy": 0.88,
    "value_framing": 0.88,
    "closing": 0.88
  },
  "feedback_to_generator": [
    "Manter evidências de contexto na resposta",
    "Preservar tom consultivo e próximo",
    "Registrar decisão no audit log"
  ]
}
```

### Failure Handling

- Se faltar dado crítico, retornar `REJEITAR` com pedido específico de complemento.
- Se houver blocker, retornar `REJEITAR_IMEDIATAMENTE` e impedir envio ao cliente.
- Se houver falha corrigível, devolver feedback curto ao Generator e permitir nova iteração.
- Se a segunda iteração falhar pelo mesmo motivo, escalar para revisão humana ou fluxo seguro.
- Se a avaliação tiver baixa confiança, registrar `confidence_score` baixo e não tratar aprovação como definitiva.

### KODA application

Fernando usa esta rubrica quando KODA precisa negociar sem destruir margem nem confiança.

O ponto operacional é evitar que KODA confunda fluência com qualidade. Uma mensagem pode ser natural e ainda estar errada. Uma mensagem pode vender bem e ainda violar margem. Uma mensagem pode ser simpática e ainda chegar no timing errado.

---

## ⏰ Rubric: Follow-Up

**`rubric_id`:** `koda.follow_up.v1`
**`approval_threshold`:** `0.78`
**Objetivo:** avaliar se uma mensagem de follow-up chega no timing certo, com personalização suficiente e sem parecer spam.
**Cenário típico:** cliente abandonou carrinho, pediu para lembrar depois, recebeu produto ou está em ciclo de recompra.

### Input Specification

O Evaluator só deve aplicar este rubric quando recebe dados suficientes. Se o input estiver incompleto, a decisão correta não é fingir confiança; é pedir complemento ou marcar baixa `confidence_score`.

- histórico resumido da conversa com fatos críticos preservados
- mensagem mais recente do cliente
- draft do Generator com `generation_id`
- políticas comerciais e limites atuais aplicáveis
- dados de catálogo, estoque, preço ou agenda quando relevantes
- restrições conhecidas: orçamento, alergias, preferências, opt-out, tom e urgência

### Dimensoes, pesos e criterios mensuraveis

| Dimensão | Peso | O que mede | Nota 5 | Nota 3 | Nota 1 |
|----------|------|------------|--------|--------|--------|
| Timing | 25% | Mensagem respeita janela prometida, horário aceitável e momento da jornada. | atende completamente com evidência | atende parcialmente ou com lacuna pequena | falha no ponto central |
| Personalization | 25% | Usa contexto real: produto, objetivo, restrição, conversa anterior. | atende completamente com evidência | atende parcialmente ou com lacuna pequena | falha no ponto central |
| Usefulness | 20% | Traz informação útil, não apenas cobrança para comprar. | atende completamente com evidência | atende parcialmente ou com lacuna pequena | falha no ponto central |
| Consent and Boundaries | 15% | Respeita opt-out, frequência e preferência do cliente. | atende completamente com evidência | atende parcialmente ou com lacuna pequena | falha no ponto central |
| Call to Action | 15% | Próximo passo é leve, claro e opcional. | atende completamente com evidência | atende parcialmente ou com lacuna pequena | falha no ponto central |

### Blockers

- `REJEITAR_IMEDIATAMENTE` quando houver enviar fora da janela combinada.
- `REJEITAR_IMEDIATAMENTE` quando houver ignorar opt-out.
- `REJEITAR_IMEDIATAMENTE` quando houver mandar mensagem genérica em massa.
- `REJEITAR_IMEDIATAMENTE` quando houver pressionar cliente vulnerável.
- `REJEITAR_IMEDIATAMENTE` quando houver repetir follow-up excessivo.

### Exemplo bom

```text
Oi, Ana! Passando como combinado: ontem você ficou entre o Whey Isolado Neutro e a opção vegetal por causa da gastrite. O Neutro ainda está em estoque por R$ 129,90. Quer que eu deixe reservado ou prefere comparar de novo antes de decidir?
```

Por que funciona:
- **Timing:** mostra mensagem respeita janela prometida, horário aceitável e momento da jornada.
- **Personalization:** mostra usa contexto real: produto, objetivo, restrição, conversa anterior.
- **Usefulness:** mostra traz informação útil, não apenas cobrança para comprar.
- **Consent and Boundaries:** mostra respeita opt-out, frequência e preferência do cliente.
- **Call to Action:** mostra próximo passo é leve, claro e opcional.

### Exemplo ruim

```text
E aí, vai comprar ou não? Promo acabando. Responde rápido.
```

Por que falha:
- Cria risco porque pode envolver enviar fora da janela combinada.
- Cria risco porque pode envolver ignorar opt-out.
- Cria risco porque pode envolver mandar mensagem genérica em massa.

### Diálogo WhatsApp calibrado

```
Cliente: Me lembra amanhã do whey sem lactose.
KODA bom: Retoma amanhã com produto e restrição citados.
KODA ruim: Cobra compra com pressão genérica.
```

### Decision logic

```
if blocker_detected:
  decision = REJEITAR_IMEDIATAMENTE
elif overall_score >= 0.78 and confidence_score >= 0.75:
  decision = APROVAR
elif overall_score >= 0.70 and confidence_score >= 0.70:
  decision = APROVAR_COM_RESSALVAS
else:
  decision = REJEITAR
```

### JSON de avaliação exemplo

```json
{
  "rubric_id": "koda.follow_up.v1",
  "generation_id": "gen_koda_follow-up_001",
  "approval_threshold": 0.78,
  "overall_score": 0.88,
  "confidence_score": 0.91,
  "decision": "APROVAR",
  "dimension_scores": {
    "timing": 0.88,
    "personalization": 0.88,
    "usefulness": 0.88,
    "consent_and_boundaries": 0.88,
    "call_to_action": 0.88
  },
  "feedback_to_generator": [
    "Manter evidências de contexto na resposta",
    "Preservar tom consultivo e próximo",
    "Registrar decisão no audit log"
  ]
}
```

### Failure Handling

- Se faltar dado crítico, retornar `REJEITAR` com pedido específico de complemento.
- Se houver blocker, retornar `REJEITAR_IMEDIATAMENTE` e impedir envio ao cliente.
- Se houver falha corrigível, devolver feedback curto ao Generator e permitir nova iteração.
- Se a segunda iteração falhar pelo mesmo motivo, escalar para revisão humana ou fluxo seguro.
- Se a avaliação tiver baixa confiança, registrar `confidence_score` baixo e não tratar aprovação como definitiva.

### KODA application

Fernando usa esta rubrica para manter relacionamento sem transformar KODA em spammer.

O ponto operacional é evitar que KODA confunda fluência com qualidade. Uma mensagem pode ser natural e ainda estar errada. Uma mensagem pode vender bem e ainda violar margem. Uma mensagem pode ser simpática e ainda chegar no timing errado.

---

## 🔁 Integracao com Generator/Evaluator

A integração explícita entre Generator e Evaluator é onde este módulo vira operação. O Generator não recebe a tarefa "faça algo bom". Ele recebe contexto, contrato e tipo de output esperado. O Evaluator não recebe a tarefa "dê sua opinião". Ele recebe rubric, draft, contexto e obrigação de registrar verdict.

### Fluxo operacional

1. **Customer Context:** KODA consolida histórico, preferências, restrições, estado do carrinho, políticas e mensagem atual.
2. **Generator draft:** Generator cria uma resposta com `generation_id`, sem marcar sua própria qualidade.
3. **Evaluator verdict:** Evaluator aplica `rubric_id`, calcula dimensoes, `overall_score` e `confidence_score`.
4. **Decision Engine:** Decisão vira `APROVAR`, `APROVAR_COM_RESSALVAS`, `REJEITAR` ou `REJEITAR_IMEDIATAMENTE`.
5. **Feedback loop:** Se rejeitado, Generator recebe feedback específico e tenta novamente até `max_iterations`.
6. **Escalation:** Falhas repetidas, blockers e baixa confiança vão para humano ou fluxo seguro.
7. **Audit log/state files:** Draft, verdict, decisão e contexto relevante são persistidos para trace reading.

### State files recomendados

```
state/
  conversations/
    customer_ana_2026_05_28/
      context_snapshot.json
      generator_draft_gen_001.json
      evaluator_verdict_gen_001.json
      generator_draft_gen_002.json
      evaluator_verdict_gen_002.json
      decision_log.jsonl
      escalation_note.md
```

### Exemplo de feedback loop com max iterations

```json
{
  "generation_id": "gen_follow_up_4481",
  "rubric_id": "koda.follow_up.v1",
  "max_iterations": 3,
  "iteration": 2,
  "previous_decision": "REJEITAR",
  "feedback_loop": [
    {
      "iteration": 1,
      "decision": "REJEITAR",
      "reason": "Mensagem genérica; não mencionou produto nem timing prometido"
    },
    {
      "iteration": 2,
      "decision": "APROVAR_COM_RESSALVAS",
      "reason": "Personalização adequada; CTA poderia ser mais leve"
    }
  ],
  "escalation_required": false
}
```

### Regras de integração

- Nunca permita que o Generator defina `overall_score` do próprio output.
- Nunca trate `approval_threshold` como decoração; abaixo do threshold a saída não vai direto ao cliente.
- Nunca misture Sprint Contracts com rubric scoring: contrato define escopo, rubric mede qualidade do resultado.
- Nunca confunda output validation com business validation: JSON válido pode conter recomendação ruim.
- Nunca ignore `confidence_score`: baixa confiança exige cuidado mesmo quando `overall_score` parece bom.
- Use `REJEITAR_IMEDIATAMENTE` para risco irreversível, não para preferência de estilo.
- Registre todo verdict em audit log/state files com `generation_id` e `rubric_id`.

---

## 🧪 Calibracao e Quality Validation

Calibração é o processo de garantir que diferentes Evaluators, prompts ou versões do mesmo rubric tomem decisões parecidas diante dos mesmos exemplos. Sem calibração, você troca subjetividade humana por subjetividade automatizada.

### Como calibrar

- **Colete exemplos reais:** Use conversas KODA com autorização operacional e remova dados sensíveis.
- **Separe bons, médios e ruins:** Não treine só com extremos; casos ambíguos revelam falhas de rubric.
- **Atribua score humano inicial:** Fernando ou especialistas marcam dimensoes e justificativa.
- **Rode o Evaluator:** Compare verdict automático com verdict humano.
- **Analise divergências:** Descubra se problema é dimensão vaga, peso errado, blocker ausente ou contexto incompleto.
- **Ajuste rubric:** Mude critérios, exemplos, pesos ou Failure Handling.
- **Congele versão:** Publique `rubric_id` versionado e registre mudanças.

### Quality validation checklist

- [ ] O rubric tem `rubric_id` versionado.
- [ ] O output type está claro e não mistura famílias diferentes.
- [ ] Input Specification lista dados mínimos necessários.
- [ ] Cada dimensão tem peso e descrição mensurável.
- [ ] A escala 0-5 tem âncoras comportamentais claras.
- [ ] Blockers estão explícitos e ligados a decisão.
- [ ] `approval_threshold` está definido e justificado.
- [ ] Exemplos bons e ruins existem para cada família.
- [ ] Failure Handling define retry, escalation e max iterations.
- [ ] O Evaluator registra `overall_score` e `confidence_score`.
- [ ] A decisão final usa `APROVAR`, `APROVAR_COM_RESSALVAS`, `REJEITAR` ou `REJEITAR_IMEDIATAMENTE`.
- [ ] O audit log/state files guarda draft, verdict e contexto essencial.
- [ ] O rubric não substitui Sprint Contracts.
- [ ] O rubric não reduz avaliação a binário vago.
- [ ] A validação cobre business validation, não só output validation.

### Sinais de rubric mal calibrado

- Quase tudo é aprovado com score entre 0.90 e 1.00.
- Quase tudo é rejeitado por detalhes de tom, mesmo sem risco.
- Dois Evaluators aplicando o mesmo rubric discordam em mais de 20% dos casos.
- O feedback para Generator é genérico: "melhore a resposta".
- Blockers aparecem no texto, mas não mudam decisão.
- Casos de alta margem comercial recebem aprovação frouxa demais.
- Casos de reclamação recebem tom frio porque a dimensão de empatia tem peso baixo.

---

## 🚀 Aplicacao KODA

Agora vamos juntar tudo em uma operação real. Imagine que Fernando quer melhorar a qualidade do KODA em quatro pontos do funil: descoberta, atendimento, negociação e recompra.

| Momento da jornada | Output type | Rubric usado | Principal risco | Métrica de sucesso |
|--------------------|-------------|--------------|-----------------|-------------------|
| Descoberta de produto | Product Recommendation | `koda.product_recommendation.v1` | recomendar produto incompatível | queda em reclamações por recomendação errada |
| Dúvida ou reclamação | Customer Response | `koda.customer_response.v1` | resposta fria ou factual errada | aumento de resolução sem humano |
| Objeção de preço | Price Negotiation | `koda.price_negotiation.v1` | desconto falso ou margem destruída | conversão com margem preservada |
| Recontato | Follow-Up | `koda.follow_up.v1` | spam ou timing ruim | resposta positiva ao follow-up |

### Exemplo completo: recomendação rejeitada e corrigida

```
Cliente: KODA, quero algo para energia no treino, mas tenho ansiedade e tomo café todo dia.

Generator v1: Recomendo o Pré-Treino Insano 300mg cafeína. Vai te dar energia máxima.
Evaluator: REJEITAR_IMEDIATAMENTE
Motivo: ignora ansiedade e excesso de estimulante; risco de saúde e confiança.

Generator v2: Pela ansiedade e pelo café diário, eu evitaria pré-treinos fortes com cafeína. Posso te mostrar uma opção sem estimulante para foco e uma opção de carboidrato para energia mais estável?
Evaluator: APROVAR
Motivo: respeita restrição, não promete efeito médico, oferece próximo passo seguro.
```

### Exemplo completo: negociação aprovada com ressalvas

```
Cliente: Se fizer por R$ 100 eu compro agora.

Generator: Eu não consigo chegar em R$ 100 nesse kit, mas consigo aplicar frete grátis e manter R$ 119,90. Ele dura 30 dias e sai por menos de R$ 4 por dose. Quer que eu deixe reservado?
Evaluator: APROVAR_COM_RESSALVAS
Motivo: condição real e respeitosa; poderia explicar validade da condição sem criar urgência falsa.
```

### Exemplo completo: follow-up rejeitado

```
Cliente ontem: Me lembra amanhã à tarde sobre o whey sem lactose.

Generator hoje 08:02: Bom dia! Vai comprar seu produto?
Evaluator: REJEITAR
Motivo: timing errado, sem personalização, tom de cobrança.

Generator corrigido 15:10: Oi, Ana! Passando como combinado sobre o whey sem lactose que você viu ontem. Ele ainda está em estoque por R$ 129,90. Quer que eu compare de novo com a opção vegetal antes de decidir?
Evaluator: APROVAR
```

### Operação semanal de Fernando

- Segunda: revisar 20 casos `REJEITAR_IMEDIATAMENTE` para encontrar blockers recorrentes.
- Terça: calibrar Product Recommendation com catálogo atualizado.
- Quarta: comparar Price Negotiation contra margem real e conversão.
- Quinta: auditar Follow-Up para opt-out, frequência e timing.
- Sexta: publicar versão menor de rubrics se houver ajuste de peso ou exemplo.

---

## 🧩 Playbook Operacional: Product Recommendation

Este playbook transforma a rubrica de Product Recommendation em rotina de operação. O foco é catalogo, restrições, objetivo, orçamento, estoque, preço e explicação.

### Fase 1: checkpoint critico de Product Recommendation

Nesta fase, o Evaluator atua como gatekeeper e procura evidência concreta antes de aceitar a saída. A pergunta não é "soa bem?". A pergunta é "o draft prova que respeitou catalogo, restrições, objetivo, orçamento, estoque, preço e explicação?"

| Checagem | Evidência esperada | Falha comum | Ação |
|----------|--------------------|-------------|------|
| Contexto | O draft usa fatos do cliente, não suposições | Resposta genérica | `REJEITAR` e pedir reescrita contextual |
| Dados | O draft cita apenas dados disponíveis | Inventar preço, prazo ou condição | `REJEITAR_IMEDIATAMENTE` se houver risco |
| Tom | A resposta preserva voz consultiva KODA | Pressão, frieza ou informalidade excessiva | Ajustar com feedback específico |
| Negócio | A resposta protege confiança e margem | Converter a qualquer custo | Escalar se conflito comercial persistir |
| Próximo passo | Cliente sabe o que fazer depois | Fechamento ausente ou agressivo | `APROVAR_COM_RESSALVAS` ou retry |

Exemplo de feedback útil para o Generator:

```text
Reescreva a saída de Product Recommendation preservando o fato crítico do cliente, removendo qualquer afirmação não comprovada e tornando o próximo passo mais claro. Mantenha tom consultivo, sem sycophancy, sem se desculpar em excesso e sem inventar política comercial.
```

Perguntas de calibração:

- O score alto está apoiado em evidência observável ou em impressão subjetiva?
- O `confidence_score` deveria cair porque falta contexto?
- Algum blocker exige `REJEITAR_IMEDIATAMENTE` mesmo com boa escrita?
- A decisão respeita o limite entre output validation e business validation?
- O audit log/state files permite reconstruir por que esta decisão foi tomada?

### Fase 2: checkpoint critico de Product Recommendation

Nesta fase, o Evaluator atua como gatekeeper e procura evidência concreta antes de aceitar a saída. A pergunta não é "soa bem?". A pergunta é "o draft prova que respeitou catalogo, restrições, objetivo, orçamento, estoque, preço e explicação?"

| Checagem | Evidência esperada | Falha comum | Ação |
|----------|--------------------|-------------|------|
| Contexto | O draft usa fatos do cliente, não suposições | Resposta genérica | `REJEITAR` e pedir reescrita contextual |
| Dados | O draft cita apenas dados disponíveis | Inventar preço, prazo ou condição | `REJEITAR_IMEDIATAMENTE` se houver risco |
| Tom | A resposta preserva voz consultiva KODA | Pressão, frieza ou informalidade excessiva | Ajustar com feedback específico |
| Negócio | A resposta protege confiança e margem | Converter a qualquer custo | Escalar se conflito comercial persistir |
| Próximo passo | Cliente sabe o que fazer depois | Fechamento ausente ou agressivo | `APROVAR_COM_RESSALVAS` ou retry |

Exemplo de feedback útil para o Generator:

```text
Reescreva a saída de Product Recommendation preservando o fato crítico do cliente, removendo qualquer afirmação não comprovada e tornando o próximo passo mais claro. Mantenha tom consultivo, sem sycophancy, sem se desculpar em excesso e sem inventar política comercial.
```

Perguntas de calibração:

- O score alto está apoiado em evidência observável ou em impressão subjetiva?
- O `confidence_score` deveria cair porque falta contexto?
- Algum blocker exige `REJEITAR_IMEDIATAMENTE` mesmo com boa escrita?
- A decisão respeita o limite entre output validation e business validation?
- O audit log/state files permite reconstruir por que esta decisão foi tomada?

### Fase 3: checkpoint critico de Product Recommendation

Nesta fase, o Evaluator atua como gatekeeper e procura evidência concreta antes de aceitar a saída. A pergunta não é "soa bem?". A pergunta é "o draft prova que respeitou catalogo, restrições, objetivo, orçamento, estoque, preço e explicação?"

| Checagem | Evidência esperada | Falha comum | Ação |
|----------|--------------------|-------------|------|
| Contexto | O draft usa fatos do cliente, não suposições | Resposta genérica | `REJEITAR` e pedir reescrita contextual |
| Dados | O draft cita apenas dados disponíveis | Inventar preço, prazo ou condição | `REJEITAR_IMEDIATAMENTE` se houver risco |
| Tom | A resposta preserva voz consultiva KODA | Pressão, frieza ou informalidade excessiva | Ajustar com feedback específico |
| Negócio | A resposta protege confiança e margem | Converter a qualquer custo | Escalar se conflito comercial persistir |
| Próximo passo | Cliente sabe o que fazer depois | Fechamento ausente ou agressivo | `APROVAR_COM_RESSALVAS` ou retry |

Exemplo de feedback útil para o Generator:

```text
Reescreva a saída de Product Recommendation preservando o fato crítico do cliente, removendo qualquer afirmação não comprovada e tornando o próximo passo mais claro. Mantenha tom consultivo, sem sycophancy, sem se desculpar em excesso e sem inventar política comercial.
```

Perguntas de calibração:

- O score alto está apoiado em evidência observável ou em impressão subjetiva?
- O `confidence_score` deveria cair porque falta contexto?
- Algum blocker exige `REJEITAR_IMEDIATAMENTE` mesmo com boa escrita?
- A decisão respeita o limite entre output validation e business validation?
- O audit log/state files permite reconstruir por que esta decisão foi tomada?

### Fase 4: checkpoint critico de Product Recommendation

Nesta fase, o Evaluator atua como gatekeeper e procura evidência concreta antes de aceitar a saída. A pergunta não é "soa bem?". A pergunta é "o draft prova que respeitou catalogo, restrições, objetivo, orçamento, estoque, preço e explicação?"

| Checagem | Evidência esperada | Falha comum | Ação |
|----------|--------------------|-------------|------|
| Contexto | O draft usa fatos do cliente, não suposições | Resposta genérica | `REJEITAR` e pedir reescrita contextual |
| Dados | O draft cita apenas dados disponíveis | Inventar preço, prazo ou condição | `REJEITAR_IMEDIATAMENTE` se houver risco |
| Tom | A resposta preserva voz consultiva KODA | Pressão, frieza ou informalidade excessiva | Ajustar com feedback específico |
| Negócio | A resposta protege confiança e margem | Converter a qualquer custo | Escalar se conflito comercial persistir |
| Próximo passo | Cliente sabe o que fazer depois | Fechamento ausente ou agressivo | `APROVAR_COM_RESSALVAS` ou retry |

Exemplo de feedback útil para o Generator:

```text
Reescreva a saída de Product Recommendation preservando o fato crítico do cliente, removendo qualquer afirmação não comprovada e tornando o próximo passo mais claro. Mantenha tom consultivo, sem sycophancy, sem se desculpar em excesso e sem inventar política comercial.
```

Perguntas de calibração:

- O score alto está apoiado em evidência observável ou em impressão subjetiva?
- O `confidence_score` deveria cair porque falta contexto?
- Algum blocker exige `REJEITAR_IMEDIATAMENTE` mesmo com boa escrita?
- A decisão respeita o limite entre output validation e business validation?
- O audit log/state files permite reconstruir por que esta decisão foi tomada?

### Fase 5: checkpoint critico de Product Recommendation

Nesta fase, o Evaluator atua como gatekeeper e procura evidência concreta antes de aceitar a saída. A pergunta não é "soa bem?". A pergunta é "o draft prova que respeitou catalogo, restrições, objetivo, orçamento, estoque, preço e explicação?"

| Checagem | Evidência esperada | Falha comum | Ação |
|----------|--------------------|-------------|------|
| Contexto | O draft usa fatos do cliente, não suposições | Resposta genérica | `REJEITAR` e pedir reescrita contextual |
| Dados | O draft cita apenas dados disponíveis | Inventar preço, prazo ou condição | `REJEITAR_IMEDIATAMENTE` se houver risco |
| Tom | A resposta preserva voz consultiva KODA | Pressão, frieza ou informalidade excessiva | Ajustar com feedback específico |
| Negócio | A resposta protege confiança e margem | Converter a qualquer custo | Escalar se conflito comercial persistir |
| Próximo passo | Cliente sabe o que fazer depois | Fechamento ausente ou agressivo | `APROVAR_COM_RESSALVAS` ou retry |

Exemplo de feedback útil para o Generator:

```text
Reescreva a saída de Product Recommendation preservando o fato crítico do cliente, removendo qualquer afirmação não comprovada e tornando o próximo passo mais claro. Mantenha tom consultivo, sem sycophancy, sem se desculpar em excesso e sem inventar política comercial.
```

Perguntas de calibração:

- O score alto está apoiado em evidência observável ou em impressão subjetiva?
- O `confidence_score` deveria cair porque falta contexto?
- Algum blocker exige `REJEITAR_IMEDIATAMENTE` mesmo com boa escrita?
- A decisão respeita o limite entre output validation e business validation?
- O audit log/state files permite reconstruir por que esta decisão foi tomada?

### Fase 6: checkpoint critico de Product Recommendation

Nesta fase, o Evaluator atua como gatekeeper e procura evidência concreta antes de aceitar a saída. A pergunta não é "soa bem?". A pergunta é "o draft prova que respeitou catalogo, restrições, objetivo, orçamento, estoque, preço e explicação?"

| Checagem | Evidência esperada | Falha comum | Ação |
|----------|--------------------|-------------|------|
| Contexto | O draft usa fatos do cliente, não suposições | Resposta genérica | `REJEITAR` e pedir reescrita contextual |
| Dados | O draft cita apenas dados disponíveis | Inventar preço, prazo ou condição | `REJEITAR_IMEDIATAMENTE` se houver risco |
| Tom | A resposta preserva voz consultiva KODA | Pressão, frieza ou informalidade excessiva | Ajustar com feedback específico |
| Negócio | A resposta protege confiança e margem | Converter a qualquer custo | Escalar se conflito comercial persistir |
| Próximo passo | Cliente sabe o que fazer depois | Fechamento ausente ou agressivo | `APROVAR_COM_RESSALVAS` ou retry |

Exemplo de feedback útil para o Generator:

```text
Reescreva a saída de Product Recommendation preservando o fato crítico do cliente, removendo qualquer afirmação não comprovada e tornando o próximo passo mais claro. Mantenha tom consultivo, sem sycophancy, sem se desculpar em excesso e sem inventar política comercial.
```

Perguntas de calibração:

- O score alto está apoiado em evidência observável ou em impressão subjetiva?
- O `confidence_score` deveria cair porque falta contexto?
- Algum blocker exige `REJEITAR_IMEDIATAMENTE` mesmo com boa escrita?
- A decisão respeita o limite entre output validation e business validation?
- O audit log/state files permite reconstruir por que esta decisão foi tomada?

### Fase 7: checkpoint critico de Product Recommendation

Nesta fase, o Evaluator atua como gatekeeper e procura evidência concreta antes de aceitar a saída. A pergunta não é "soa bem?". A pergunta é "o draft prova que respeitou catalogo, restrições, objetivo, orçamento, estoque, preço e explicação?"

| Checagem | Evidência esperada | Falha comum | Ação |
|----------|--------------------|-------------|------|
| Contexto | O draft usa fatos do cliente, não suposições | Resposta genérica | `REJEITAR` e pedir reescrita contextual |
| Dados | O draft cita apenas dados disponíveis | Inventar preço, prazo ou condição | `REJEITAR_IMEDIATAMENTE` se houver risco |
| Tom | A resposta preserva voz consultiva KODA | Pressão, frieza ou informalidade excessiva | Ajustar com feedback específico |
| Negócio | A resposta protege confiança e margem | Converter a qualquer custo | Escalar se conflito comercial persistir |
| Próximo passo | Cliente sabe o que fazer depois | Fechamento ausente ou agressivo | `APROVAR_COM_RESSALVAS` ou retry |

Exemplo de feedback útil para o Generator:

```text
Reescreva a saída de Product Recommendation preservando o fato crítico do cliente, removendo qualquer afirmação não comprovada e tornando o próximo passo mais claro. Mantenha tom consultivo, sem sycophancy, sem se desculpar em excesso e sem inventar política comercial.
```

Perguntas de calibração:

- O score alto está apoiado em evidência observável ou em impressão subjetiva?
- O `confidence_score` deveria cair porque falta contexto?
- Algum blocker exige `REJEITAR_IMEDIATAMENTE` mesmo com boa escrita?
- A decisão respeita o limite entre output validation e business validation?
- O audit log/state files permite reconstruir por que esta decisão foi tomada?

### Fase 8: checkpoint critico de Product Recommendation

Nesta fase, o Evaluator atua como gatekeeper e procura evidência concreta antes de aceitar a saída. A pergunta não é "soa bem?". A pergunta é "o draft prova que respeitou catalogo, restrições, objetivo, orçamento, estoque, preço e explicação?"

| Checagem | Evidência esperada | Falha comum | Ação |
|----------|--------------------|-------------|------|
| Contexto | O draft usa fatos do cliente, não suposições | Resposta genérica | `REJEITAR` e pedir reescrita contextual |
| Dados | O draft cita apenas dados disponíveis | Inventar preço, prazo ou condição | `REJEITAR_IMEDIATAMENTE` se houver risco |
| Tom | A resposta preserva voz consultiva KODA | Pressão, frieza ou informalidade excessiva | Ajustar com feedback específico |
| Negócio | A resposta protege confiança e margem | Converter a qualquer custo | Escalar se conflito comercial persistir |
| Próximo passo | Cliente sabe o que fazer depois | Fechamento ausente ou agressivo | `APROVAR_COM_RESSALVAS` ou retry |

Exemplo de feedback útil para o Generator:

```text
Reescreva a saída de Product Recommendation preservando o fato crítico do cliente, removendo qualquer afirmação não comprovada e tornando o próximo passo mais claro. Mantenha tom consultivo, sem sycophancy, sem se desculpar em excesso e sem inventar política comercial.
```

Perguntas de calibração:

- O score alto está apoiado em evidência observável ou em impressão subjetiva?
- O `confidence_score` deveria cair porque falta contexto?
- Algum blocker exige `REJEITAR_IMEDIATAMENTE` mesmo com boa escrita?
- A decisão respeita o limite entre output validation e business validation?
- O audit log/state files permite reconstruir por que esta decisão foi tomada?

### Fase 9: checkpoint critico de Product Recommendation

Nesta fase, o Evaluator atua como gatekeeper e procura evidência concreta antes de aceitar a saída. A pergunta não é "soa bem?". A pergunta é "o draft prova que respeitou catalogo, restrições, objetivo, orçamento, estoque, preço e explicação?"

| Checagem | Evidência esperada | Falha comum | Ação |
|----------|--------------------|-------------|------|
| Contexto | O draft usa fatos do cliente, não suposições | Resposta genérica | `REJEITAR` e pedir reescrita contextual |
| Dados | O draft cita apenas dados disponíveis | Inventar preço, prazo ou condição | `REJEITAR_IMEDIATAMENTE` se houver risco |
| Tom | A resposta preserva voz consultiva KODA | Pressão, frieza ou informalidade excessiva | Ajustar com feedback específico |
| Negócio | A resposta protege confiança e margem | Converter a qualquer custo | Escalar se conflito comercial persistir |
| Próximo passo | Cliente sabe o que fazer depois | Fechamento ausente ou agressivo | `APROVAR_COM_RESSALVAS` ou retry |

Exemplo de feedback útil para o Generator:

```text
Reescreva a saída de Product Recommendation preservando o fato crítico do cliente, removendo qualquer afirmação não comprovada e tornando o próximo passo mais claro. Mantenha tom consultivo, sem sycophancy, sem se desculpar em excesso e sem inventar política comercial.
```

Perguntas de calibração:

- O score alto está apoiado em evidência observável ou em impressão subjetiva?
- O `confidence_score` deveria cair porque falta contexto?
- Algum blocker exige `REJEITAR_IMEDIATAMENTE` mesmo com boa escrita?
- A decisão respeita o limite entre output validation e business validation?
- O audit log/state files permite reconstruir por que esta decisão foi tomada?

### Fase 10: checkpoint critico de Product Recommendation

Nesta fase, o Evaluator atua como gatekeeper e procura evidência concreta antes de aceitar a saída. A pergunta não é "soa bem?". A pergunta é "o draft prova que respeitou catalogo, restrições, objetivo, orçamento, estoque, preço e explicação?"

| Checagem | Evidência esperada | Falha comum | Ação |
|----------|--------------------|-------------|------|
| Contexto | O draft usa fatos do cliente, não suposições | Resposta genérica | `REJEITAR` e pedir reescrita contextual |
| Dados | O draft cita apenas dados disponíveis | Inventar preço, prazo ou condição | `REJEITAR_IMEDIATAMENTE` se houver risco |
| Tom | A resposta preserva voz consultiva KODA | Pressão, frieza ou informalidade excessiva | Ajustar com feedback específico |
| Negócio | A resposta protege confiança e margem | Converter a qualquer custo | Escalar se conflito comercial persistir |
| Próximo passo | Cliente sabe o que fazer depois | Fechamento ausente ou agressivo | `APROVAR_COM_RESSALVAS` ou retry |

Exemplo de feedback útil para o Generator:

```text
Reescreva a saída de Product Recommendation preservando o fato crítico do cliente, removendo qualquer afirmação não comprovada e tornando o próximo passo mais claro. Mantenha tom consultivo, sem sycophancy, sem se desculpar em excesso e sem inventar política comercial.
```

Perguntas de calibração:

- O score alto está apoiado em evidência observável ou em impressão subjetiva?
- O `confidence_score` deveria cair porque falta contexto?
- Algum blocker exige `REJEITAR_IMEDIATAMENTE` mesmo com boa escrita?
- A decisão respeita o limite entre output validation e business validation?
- O audit log/state files permite reconstruir por que esta decisão foi tomada?

---

## 🧩 Playbook Operacional: Customer Response

Este playbook transforma a rubrica de Customer Response em rotina de operação. O foco é intenção, emoção, fato operacional, completude e próximo passo.

### Fase 1: checkpoint critico de Customer Response

Nesta fase, o Evaluator atua como gatekeeper e procura evidência concreta antes de aceitar a saída. A pergunta não é "soa bem?". A pergunta é "o draft prova que respeitou intenção, emoção, fato operacional, completude e próximo passo?"

| Checagem | Evidência esperada | Falha comum | Ação |
|----------|--------------------|-------------|------|
| Contexto | O draft usa fatos do cliente, não suposições | Resposta genérica | `REJEITAR` e pedir reescrita contextual |
| Dados | O draft cita apenas dados disponíveis | Inventar preço, prazo ou condição | `REJEITAR_IMEDIATAMENTE` se houver risco |
| Tom | A resposta preserva voz consultiva KODA | Pressão, frieza ou informalidade excessiva | Ajustar com feedback específico |
| Negócio | A resposta protege confiança e margem | Converter a qualquer custo | Escalar se conflito comercial persistir |
| Próximo passo | Cliente sabe o que fazer depois | Fechamento ausente ou agressivo | `APROVAR_COM_RESSALVAS` ou retry |

Exemplo de feedback útil para o Generator:

```text
Reescreva a saída de Customer Response preservando o fato crítico do cliente, removendo qualquer afirmação não comprovada e tornando o próximo passo mais claro. Mantenha tom consultivo, sem sycophancy, sem se desculpar em excesso e sem inventar política comercial.
```

Perguntas de calibração:

- O score alto está apoiado em evidência observável ou em impressão subjetiva?
- O `confidence_score` deveria cair porque falta contexto?
- Algum blocker exige `REJEITAR_IMEDIATAMENTE` mesmo com boa escrita?
- A decisão respeita o limite entre output validation e business validation?
- O audit log/state files permite reconstruir por que esta decisão foi tomada?

### Fase 2: checkpoint critico de Customer Response

Nesta fase, o Evaluator atua como gatekeeper e procura evidência concreta antes de aceitar a saída. A pergunta não é "soa bem?". A pergunta é "o draft prova que respeitou intenção, emoção, fato operacional, completude e próximo passo?"

| Checagem | Evidência esperada | Falha comum | Ação |
|----------|--------------------|-------------|------|
| Contexto | O draft usa fatos do cliente, não suposições | Resposta genérica | `REJEITAR` e pedir reescrita contextual |
| Dados | O draft cita apenas dados disponíveis | Inventar preço, prazo ou condição | `REJEITAR_IMEDIATAMENTE` se houver risco |
| Tom | A resposta preserva voz consultiva KODA | Pressão, frieza ou informalidade excessiva | Ajustar com feedback específico |
| Negócio | A resposta protege confiança e margem | Converter a qualquer custo | Escalar se conflito comercial persistir |
| Próximo passo | Cliente sabe o que fazer depois | Fechamento ausente ou agressivo | `APROVAR_COM_RESSALVAS` ou retry |

Exemplo de feedback útil para o Generator:

```text
Reescreva a saída de Customer Response preservando o fato crítico do cliente, removendo qualquer afirmação não comprovada e tornando o próximo passo mais claro. Mantenha tom consultivo, sem sycophancy, sem se desculpar em excesso e sem inventar política comercial.
```

Perguntas de calibração:

- O score alto está apoiado em evidência observável ou em impressão subjetiva?
- O `confidence_score` deveria cair porque falta contexto?
- Algum blocker exige `REJEITAR_IMEDIATAMENTE` mesmo com boa escrita?
- A decisão respeita o limite entre output validation e business validation?
- O audit log/state files permite reconstruir por que esta decisão foi tomada?

### Fase 3: checkpoint critico de Customer Response

Nesta fase, o Evaluator atua como gatekeeper e procura evidência concreta antes de aceitar a saída. A pergunta não é "soa bem?". A pergunta é "o draft prova que respeitou intenção, emoção, fato operacional, completude e próximo passo?"

| Checagem | Evidência esperada | Falha comum | Ação |
|----------|--------------------|-------------|------|
| Contexto | O draft usa fatos do cliente, não suposições | Resposta genérica | `REJEITAR` e pedir reescrita contextual |
| Dados | O draft cita apenas dados disponíveis | Inventar preço, prazo ou condição | `REJEITAR_IMEDIATAMENTE` se houver risco |
| Tom | A resposta preserva voz consultiva KODA | Pressão, frieza ou informalidade excessiva | Ajustar com feedback específico |
| Negócio | A resposta protege confiança e margem | Converter a qualquer custo | Escalar se conflito comercial persistir |
| Próximo passo | Cliente sabe o que fazer depois | Fechamento ausente ou agressivo | `APROVAR_COM_RESSALVAS` ou retry |

Exemplo de feedback útil para o Generator:

```text
Reescreva a saída de Customer Response preservando o fato crítico do cliente, removendo qualquer afirmação não comprovada e tornando o próximo passo mais claro. Mantenha tom consultivo, sem sycophancy, sem se desculpar em excesso e sem inventar política comercial.
```

Perguntas de calibração:

- O score alto está apoiado em evidência observável ou em impressão subjetiva?
- O `confidence_score` deveria cair porque falta contexto?
- Algum blocker exige `REJEITAR_IMEDIATAMENTE` mesmo com boa escrita?
- A decisão respeita o limite entre output validation e business validation?
- O audit log/state files permite reconstruir por que esta decisão foi tomada?

### Fase 4: checkpoint critico de Customer Response

Nesta fase, o Evaluator atua como gatekeeper e procura evidência concreta antes de aceitar a saída. A pergunta não é "soa bem?". A pergunta é "o draft prova que respeitou intenção, emoção, fato operacional, completude e próximo passo?"

| Checagem | Evidência esperada | Falha comum | Ação |
|----------|--------------------|-------------|------|
| Contexto | O draft usa fatos do cliente, não suposições | Resposta genérica | `REJEITAR` e pedir reescrita contextual |
| Dados | O draft cita apenas dados disponíveis | Inventar preço, prazo ou condição | `REJEITAR_IMEDIATAMENTE` se houver risco |
| Tom | A resposta preserva voz consultiva KODA | Pressão, frieza ou informalidade excessiva | Ajustar com feedback específico |
| Negócio | A resposta protege confiança e margem | Converter a qualquer custo | Escalar se conflito comercial persistir |
| Próximo passo | Cliente sabe o que fazer depois | Fechamento ausente ou agressivo | `APROVAR_COM_RESSALVAS` ou retry |

Exemplo de feedback útil para o Generator:

```text
Reescreva a saída de Customer Response preservando o fato crítico do cliente, removendo qualquer afirmação não comprovada e tornando o próximo passo mais claro. Mantenha tom consultivo, sem sycophancy, sem se desculpar em excesso e sem inventar política comercial.
```

Perguntas de calibração:

- O score alto está apoiado em evidência observável ou em impressão subjetiva?
- O `confidence_score` deveria cair porque falta contexto?
- Algum blocker exige `REJEITAR_IMEDIATAMENTE` mesmo com boa escrita?
- A decisão respeita o limite entre output validation e business validation?
- O audit log/state files permite reconstruir por que esta decisão foi tomada?

### Fase 5: checkpoint critico de Customer Response

Nesta fase, o Evaluator atua como gatekeeper e procura evidência concreta antes de aceitar a saída. A pergunta não é "soa bem?". A pergunta é "o draft prova que respeitou intenção, emoção, fato operacional, completude e próximo passo?"

| Checagem | Evidência esperada | Falha comum | Ação |
|----------|--------------------|-------------|------|
| Contexto | O draft usa fatos do cliente, não suposições | Resposta genérica | `REJEITAR` e pedir reescrita contextual |
| Dados | O draft cita apenas dados disponíveis | Inventar preço, prazo ou condição | `REJEITAR_IMEDIATAMENTE` se houver risco |
| Tom | A resposta preserva voz consultiva KODA | Pressão, frieza ou informalidade excessiva | Ajustar com feedback específico |
| Negócio | A resposta protege confiança e margem | Converter a qualquer custo | Escalar se conflito comercial persistir |
| Próximo passo | Cliente sabe o que fazer depois | Fechamento ausente ou agressivo | `APROVAR_COM_RESSALVAS` ou retry |

Exemplo de feedback útil para o Generator:

```text
Reescreva a saída de Customer Response preservando o fato crítico do cliente, removendo qualquer afirmação não comprovada e tornando o próximo passo mais claro. Mantenha tom consultivo, sem sycophancy, sem se desculpar em excesso e sem inventar política comercial.
```

Perguntas de calibração:

- O score alto está apoiado em evidência observável ou em impressão subjetiva?
- O `confidence_score` deveria cair porque falta contexto?
- Algum blocker exige `REJEITAR_IMEDIATAMENTE` mesmo com boa escrita?
- A decisão respeita o limite entre output validation e business validation?
- O audit log/state files permite reconstruir por que esta decisão foi tomada?

### Fase 6: checkpoint critico de Customer Response

Nesta fase, o Evaluator atua como gatekeeper e procura evidência concreta antes de aceitar a saída. A pergunta não é "soa bem?". A pergunta é "o draft prova que respeitou intenção, emoção, fato operacional, completude e próximo passo?"

| Checagem | Evidência esperada | Falha comum | Ação |
|----------|--------------------|-------------|------|
| Contexto | O draft usa fatos do cliente, não suposições | Resposta genérica | `REJEITAR` e pedir reescrita contextual |
| Dados | O draft cita apenas dados disponíveis | Inventar preço, prazo ou condição | `REJEITAR_IMEDIATAMENTE` se houver risco |
| Tom | A resposta preserva voz consultiva KODA | Pressão, frieza ou informalidade excessiva | Ajustar com feedback específico |
| Negócio | A resposta protege confiança e margem | Converter a qualquer custo | Escalar se conflito comercial persistir |
| Próximo passo | Cliente sabe o que fazer depois | Fechamento ausente ou agressivo | `APROVAR_COM_RESSALVAS` ou retry |

Exemplo de feedback útil para o Generator:

```text
Reescreva a saída de Customer Response preservando o fato crítico do cliente, removendo qualquer afirmação não comprovada e tornando o próximo passo mais claro. Mantenha tom consultivo, sem sycophancy, sem se desculpar em excesso e sem inventar política comercial.
```

Perguntas de calibração:

- O score alto está apoiado em evidência observável ou em impressão subjetiva?
- O `confidence_score` deveria cair porque falta contexto?
- Algum blocker exige `REJEITAR_IMEDIATAMENTE` mesmo com boa escrita?
- A decisão respeita o limite entre output validation e business validation?
- O audit log/state files permite reconstruir por que esta decisão foi tomada?

### Fase 7: checkpoint critico de Customer Response

Nesta fase, o Evaluator atua como gatekeeper e procura evidência concreta antes de aceitar a saída. A pergunta não é "soa bem?". A pergunta é "o draft prova que respeitou intenção, emoção, fato operacional, completude e próximo passo?"

| Checagem | Evidência esperada | Falha comum | Ação |
|----------|--------------------|-------------|------|
| Contexto | O draft usa fatos do cliente, não suposições | Resposta genérica | `REJEITAR` e pedir reescrita contextual |
| Dados | O draft cita apenas dados disponíveis | Inventar preço, prazo ou condição | `REJEITAR_IMEDIATAMENTE` se houver risco |
| Tom | A resposta preserva voz consultiva KODA | Pressão, frieza ou informalidade excessiva | Ajustar com feedback específico |
| Negócio | A resposta protege confiança e margem | Converter a qualquer custo | Escalar se conflito comercial persistir |
| Próximo passo | Cliente sabe o que fazer depois | Fechamento ausente ou agressivo | `APROVAR_COM_RESSALVAS` ou retry |

Exemplo de feedback útil para o Generator:

```text
Reescreva a saída de Customer Response preservando o fato crítico do cliente, removendo qualquer afirmação não comprovada e tornando o próximo passo mais claro. Mantenha tom consultivo, sem sycophancy, sem se desculpar em excesso e sem inventar política comercial.
```

Perguntas de calibração:

- O score alto está apoiado em evidência observável ou em impressão subjetiva?
- O `confidence_score` deveria cair porque falta contexto?
- Algum blocker exige `REJEITAR_IMEDIATAMENTE` mesmo com boa escrita?
- A decisão respeita o limite entre output validation e business validation?
- O audit log/state files permite reconstruir por que esta decisão foi tomada?

### Fase 8: checkpoint critico de Customer Response

Nesta fase, o Evaluator atua como gatekeeper e procura evidência concreta antes de aceitar a saída. A pergunta não é "soa bem?". A pergunta é "o draft prova que respeitou intenção, emoção, fato operacional, completude e próximo passo?"

| Checagem | Evidência esperada | Falha comum | Ação |
|----------|--------------------|-------------|------|
| Contexto | O draft usa fatos do cliente, não suposições | Resposta genérica | `REJEITAR` e pedir reescrita contextual |
| Dados | O draft cita apenas dados disponíveis | Inventar preço, prazo ou condição | `REJEITAR_IMEDIATAMENTE` se houver risco |
| Tom | A resposta preserva voz consultiva KODA | Pressão, frieza ou informalidade excessiva | Ajustar com feedback específico |
| Negócio | A resposta protege confiança e margem | Converter a qualquer custo | Escalar se conflito comercial persistir |
| Próximo passo | Cliente sabe o que fazer depois | Fechamento ausente ou agressivo | `APROVAR_COM_RESSALVAS` ou retry |

Exemplo de feedback útil para o Generator:

```text
Reescreva a saída de Customer Response preservando o fato crítico do cliente, removendo qualquer afirmação não comprovada e tornando o próximo passo mais claro. Mantenha tom consultivo, sem sycophancy, sem se desculpar em excesso e sem inventar política comercial.
```

Perguntas de calibração:

- O score alto está apoiado em evidência observável ou em impressão subjetiva?
- O `confidence_score` deveria cair porque falta contexto?
- Algum blocker exige `REJEITAR_IMEDIATAMENTE` mesmo com boa escrita?
- A decisão respeita o limite entre output validation e business validation?
- O audit log/state files permite reconstruir por que esta decisão foi tomada?

### Fase 9: checkpoint critico de Customer Response

Nesta fase, o Evaluator atua como gatekeeper e procura evidência concreta antes de aceitar a saída. A pergunta não é "soa bem?". A pergunta é "o draft prova que respeitou intenção, emoção, fato operacional, completude e próximo passo?"

| Checagem | Evidência esperada | Falha comum | Ação |
|----------|--------------------|-------------|------|
| Contexto | O draft usa fatos do cliente, não suposições | Resposta genérica | `REJEITAR` e pedir reescrita contextual |
| Dados | O draft cita apenas dados disponíveis | Inventar preço, prazo ou condição | `REJEITAR_IMEDIATAMENTE` se houver risco |
| Tom | A resposta preserva voz consultiva KODA | Pressão, frieza ou informalidade excessiva | Ajustar com feedback específico |
| Negócio | A resposta protege confiança e margem | Converter a qualquer custo | Escalar se conflito comercial persistir |
| Próximo passo | Cliente sabe o que fazer depois | Fechamento ausente ou agressivo | `APROVAR_COM_RESSALVAS` ou retry |

Exemplo de feedback útil para o Generator:

```text
Reescreva a saída de Customer Response preservando o fato crítico do cliente, removendo qualquer afirmação não comprovada e tornando o próximo passo mais claro. Mantenha tom consultivo, sem sycophancy, sem se desculpar em excesso e sem inventar política comercial.
```

Perguntas de calibração:

- O score alto está apoiado em evidência observável ou em impressão subjetiva?
- O `confidence_score` deveria cair porque falta contexto?
- Algum blocker exige `REJEITAR_IMEDIATAMENTE` mesmo com boa escrita?
- A decisão respeita o limite entre output validation e business validation?
- O audit log/state files permite reconstruir por que esta decisão foi tomada?

### Fase 10: checkpoint critico de Customer Response

Nesta fase, o Evaluator atua como gatekeeper e procura evidência concreta antes de aceitar a saída. A pergunta não é "soa bem?". A pergunta é "o draft prova que respeitou intenção, emoção, fato operacional, completude e próximo passo?"

| Checagem | Evidência esperada | Falha comum | Ação |
|----------|--------------------|-------------|------|
| Contexto | O draft usa fatos do cliente, não suposições | Resposta genérica | `REJEITAR` e pedir reescrita contextual |
| Dados | O draft cita apenas dados disponíveis | Inventar preço, prazo ou condição | `REJEITAR_IMEDIATAMENTE` se houver risco |
| Tom | A resposta preserva voz consultiva KODA | Pressão, frieza ou informalidade excessiva | Ajustar com feedback específico |
| Negócio | A resposta protege confiança e margem | Converter a qualquer custo | Escalar se conflito comercial persistir |
| Próximo passo | Cliente sabe o que fazer depois | Fechamento ausente ou agressivo | `APROVAR_COM_RESSALVAS` ou retry |

Exemplo de feedback útil para o Generator:

```text
Reescreva a saída de Customer Response preservando o fato crítico do cliente, removendo qualquer afirmação não comprovada e tornando o próximo passo mais claro. Mantenha tom consultivo, sem sycophancy, sem se desculpar em excesso e sem inventar política comercial.
```

Perguntas de calibração:

- O score alto está apoiado em evidência observável ou em impressão subjetiva?
- O `confidence_score` deveria cair porque falta contexto?
- Algum blocker exige `REJEITAR_IMEDIATAMENTE` mesmo com boa escrita?
- A decisão respeita o limite entre output validation e business validation?
- O audit log/state files permite reconstruir por que esta decisão foi tomada?

---

## 🧩 Playbook Operacional: Price Negotiation

Este playbook transforma a rubrica de Price Negotiation em rotina de operação. O foco é limite comercial, margem, respeito, valor percebido e fechamento.

### Fase 1: checkpoint critico de Price Negotiation

Nesta fase, o Evaluator atua como gatekeeper e procura evidência concreta antes de aceitar a saída. A pergunta não é "soa bem?". A pergunta é "o draft prova que respeitou limite comercial, margem, respeito, valor percebido e fechamento?"

| Checagem | Evidência esperada | Falha comum | Ação |
|----------|--------------------|-------------|------|
| Contexto | O draft usa fatos do cliente, não suposições | Resposta genérica | `REJEITAR` e pedir reescrita contextual |
| Dados | O draft cita apenas dados disponíveis | Inventar preço, prazo ou condição | `REJEITAR_IMEDIATAMENTE` se houver risco |
| Tom | A resposta preserva voz consultiva KODA | Pressão, frieza ou informalidade excessiva | Ajustar com feedback específico |
| Negócio | A resposta protege confiança e margem | Converter a qualquer custo | Escalar se conflito comercial persistir |
| Próximo passo | Cliente sabe o que fazer depois | Fechamento ausente ou agressivo | `APROVAR_COM_RESSALVAS` ou retry |

Exemplo de feedback útil para o Generator:

```text
Reescreva a saída de Price Negotiation preservando o fato crítico do cliente, removendo qualquer afirmação não comprovada e tornando o próximo passo mais claro. Mantenha tom consultivo, sem sycophancy, sem se desculpar em excesso e sem inventar política comercial.
```

Perguntas de calibração:

- O score alto está apoiado em evidência observável ou em impressão subjetiva?
- O `confidence_score` deveria cair porque falta contexto?
- Algum blocker exige `REJEITAR_IMEDIATAMENTE` mesmo com boa escrita?
- A decisão respeita o limite entre output validation e business validation?
- O audit log/state files permite reconstruir por que esta decisão foi tomada?

### Fase 2: checkpoint critico de Price Negotiation

Nesta fase, o Evaluator atua como gatekeeper e procura evidência concreta antes de aceitar a saída. A pergunta não é "soa bem?". A pergunta é "o draft prova que respeitou limite comercial, margem, respeito, valor percebido e fechamento?"

| Checagem | Evidência esperada | Falha comum | Ação |
|----------|--------------------|-------------|------|
| Contexto | O draft usa fatos do cliente, não suposições | Resposta genérica | `REJEITAR` e pedir reescrita contextual |
| Dados | O draft cita apenas dados disponíveis | Inventar preço, prazo ou condição | `REJEITAR_IMEDIATAMENTE` se houver risco |
| Tom | A resposta preserva voz consultiva KODA | Pressão, frieza ou informalidade excessiva | Ajustar com feedback específico |
| Negócio | A resposta protege confiança e margem | Converter a qualquer custo | Escalar se conflito comercial persistir |
| Próximo passo | Cliente sabe o que fazer depois | Fechamento ausente ou agressivo | `APROVAR_COM_RESSALVAS` ou retry |

Exemplo de feedback útil para o Generator:

```text
Reescreva a saída de Price Negotiation preservando o fato crítico do cliente, removendo qualquer afirmação não comprovada e tornando o próximo passo mais claro. Mantenha tom consultivo, sem sycophancy, sem se desculpar em excesso e sem inventar política comercial.
```

Perguntas de calibração:

- O score alto está apoiado em evidência observável ou em impressão subjetiva?
- O `confidence_score` deveria cair porque falta contexto?
- Algum blocker exige `REJEITAR_IMEDIATAMENTE` mesmo com boa escrita?
- A decisão respeita o limite entre output validation e business validation?
- O audit log/state files permite reconstruir por que esta decisão foi tomada?

### Fase 3: checkpoint critico de Price Negotiation

Nesta fase, o Evaluator atua como gatekeeper e procura evidência concreta antes de aceitar a saída. A pergunta não é "soa bem?". A pergunta é "o draft prova que respeitou limite comercial, margem, respeito, valor percebido e fechamento?"

| Checagem | Evidência esperada | Falha comum | Ação |
|----------|--------------------|-------------|------|
| Contexto | O draft usa fatos do cliente, não suposições | Resposta genérica | `REJEITAR` e pedir reescrita contextual |
| Dados | O draft cita apenas dados disponíveis | Inventar preço, prazo ou condição | `REJEITAR_IMEDIATAMENTE` se houver risco |
| Tom | A resposta preserva voz consultiva KODA | Pressão, frieza ou informalidade excessiva | Ajustar com feedback específico |
| Negócio | A resposta protege confiança e margem | Converter a qualquer custo | Escalar se conflito comercial persistir |
| Próximo passo | Cliente sabe o que fazer depois | Fechamento ausente ou agressivo | `APROVAR_COM_RESSALVAS` ou retry |

Exemplo de feedback útil para o Generator:

```text
Reescreva a saída de Price Negotiation preservando o fato crítico do cliente, removendo qualquer afirmação não comprovada e tornando o próximo passo mais claro. Mantenha tom consultivo, sem sycophancy, sem se desculpar em excesso e sem inventar política comercial.
```

Perguntas de calibração:

- O score alto está apoiado em evidência observável ou em impressão subjetiva?
- O `confidence_score` deveria cair porque falta contexto?
- Algum blocker exige `REJEITAR_IMEDIATAMENTE` mesmo com boa escrita?
- A decisão respeita o limite entre output validation e business validation?
- O audit log/state files permite reconstruir por que esta decisão foi tomada?

### Fase 4: checkpoint critico de Price Negotiation

Nesta fase, o Evaluator atua como gatekeeper e procura evidência concreta antes de aceitar a saída. A pergunta não é "soa bem?". A pergunta é "o draft prova que respeitou limite comercial, margem, respeito, valor percebido e fechamento?"

| Checagem | Evidência esperada | Falha comum | Ação |
|----------|--------------------|-------------|------|
| Contexto | O draft usa fatos do cliente, não suposições | Resposta genérica | `REJEITAR` e pedir reescrita contextual |
| Dados | O draft cita apenas dados disponíveis | Inventar preço, prazo ou condição | `REJEITAR_IMEDIATAMENTE` se houver risco |
| Tom | A resposta preserva voz consultiva KODA | Pressão, frieza ou informalidade excessiva | Ajustar com feedback específico |
| Negócio | A resposta protege confiança e margem | Converter a qualquer custo | Escalar se conflito comercial persistir |
| Próximo passo | Cliente sabe o que fazer depois | Fechamento ausente ou agressivo | `APROVAR_COM_RESSALVAS` ou retry |

Exemplo de feedback útil para o Generator:

```text
Reescreva a saída de Price Negotiation preservando o fato crítico do cliente, removendo qualquer afirmação não comprovada e tornando o próximo passo mais claro. Mantenha tom consultivo, sem sycophancy, sem se desculpar em excesso e sem inventar política comercial.
```

Perguntas de calibração:

- O score alto está apoiado em evidência observável ou em impressão subjetiva?
- O `confidence_score` deveria cair porque falta contexto?
- Algum blocker exige `REJEITAR_IMEDIATAMENTE` mesmo com boa escrita?
- A decisão respeita o limite entre output validation e business validation?
- O audit log/state files permite reconstruir por que esta decisão foi tomada?

### Fase 5: checkpoint critico de Price Negotiation

Nesta fase, o Evaluator atua como gatekeeper e procura evidência concreta antes de aceitar a saída. A pergunta não é "soa bem?". A pergunta é "o draft prova que respeitou limite comercial, margem, respeito, valor percebido e fechamento?"

| Checagem | Evidência esperada | Falha comum | Ação |
|----------|--------------------|-------------|------|
| Contexto | O draft usa fatos do cliente, não suposições | Resposta genérica | `REJEITAR` e pedir reescrita contextual |
| Dados | O draft cita apenas dados disponíveis | Inventar preço, prazo ou condição | `REJEITAR_IMEDIATAMENTE` se houver risco |
| Tom | A resposta preserva voz consultiva KODA | Pressão, frieza ou informalidade excessiva | Ajustar com feedback específico |
| Negócio | A resposta protege confiança e margem | Converter a qualquer custo | Escalar se conflito comercial persistir |
| Próximo passo | Cliente sabe o que fazer depois | Fechamento ausente ou agressivo | `APROVAR_COM_RESSALVAS` ou retry |

Exemplo de feedback útil para o Generator:

```text
Reescreva a saída de Price Negotiation preservando o fato crítico do cliente, removendo qualquer afirmação não comprovada e tornando o próximo passo mais claro. Mantenha tom consultivo, sem sycophancy, sem se desculpar em excesso e sem inventar política comercial.
```

Perguntas de calibração:

- O score alto está apoiado em evidência observável ou em impressão subjetiva?
- O `confidence_score` deveria cair porque falta contexto?
- Algum blocker exige `REJEITAR_IMEDIATAMENTE` mesmo com boa escrita?
- A decisão respeita o limite entre output validation e business validation?
- O audit log/state files permite reconstruir por que esta decisão foi tomada?

### Fase 6: checkpoint critico de Price Negotiation

Nesta fase, o Evaluator atua como gatekeeper e procura evidência concreta antes de aceitar a saída. A pergunta não é "soa bem?". A pergunta é "o draft prova que respeitou limite comercial, margem, respeito, valor percebido e fechamento?"

| Checagem | Evidência esperada | Falha comum | Ação |
|----------|--------------------|-------------|------|
| Contexto | O draft usa fatos do cliente, não suposições | Resposta genérica | `REJEITAR` e pedir reescrita contextual |
| Dados | O draft cita apenas dados disponíveis | Inventar preço, prazo ou condição | `REJEITAR_IMEDIATAMENTE` se houver risco |
| Tom | A resposta preserva voz consultiva KODA | Pressão, frieza ou informalidade excessiva | Ajustar com feedback específico |
| Negócio | A resposta protege confiança e margem | Converter a qualquer custo | Escalar se conflito comercial persistir |
| Próximo passo | Cliente sabe o que fazer depois | Fechamento ausente ou agressivo | `APROVAR_COM_RESSALVAS` ou retry |

Exemplo de feedback útil para o Generator:

```text
Reescreva a saída de Price Negotiation preservando o fato crítico do cliente, removendo qualquer afirmação não comprovada e tornando o próximo passo mais claro. Mantenha tom consultivo, sem sycophancy, sem se desculpar em excesso e sem inventar política comercial.
```

Perguntas de calibração:

- O score alto está apoiado em evidência observável ou em impressão subjetiva?
- O `confidence_score` deveria cair porque falta contexto?
- Algum blocker exige `REJEITAR_IMEDIATAMENTE` mesmo com boa escrita?
- A decisão respeita o limite entre output validation e business validation?
- O audit log/state files permite reconstruir por que esta decisão foi tomada?

### Fase 7: checkpoint critico de Price Negotiation

Nesta fase, o Evaluator atua como gatekeeper e procura evidência concreta antes de aceitar a saída. A pergunta não é "soa bem?". A pergunta é "o draft prova que respeitou limite comercial, margem, respeito, valor percebido e fechamento?"

| Checagem | Evidência esperada | Falha comum | Ação |
|----------|--------------------|-------------|------|
| Contexto | O draft usa fatos do cliente, não suposições | Resposta genérica | `REJEITAR` e pedir reescrita contextual |
| Dados | O draft cita apenas dados disponíveis | Inventar preço, prazo ou condição | `REJEITAR_IMEDIATAMENTE` se houver risco |
| Tom | A resposta preserva voz consultiva KODA | Pressão, frieza ou informalidade excessiva | Ajustar com feedback específico |
| Negócio | A resposta protege confiança e margem | Converter a qualquer custo | Escalar se conflito comercial persistir |
| Próximo passo | Cliente sabe o que fazer depois | Fechamento ausente ou agressivo | `APROVAR_COM_RESSALVAS` ou retry |

Exemplo de feedback útil para o Generator:

```text
Reescreva a saída de Price Negotiation preservando o fato crítico do cliente, removendo qualquer afirmação não comprovada e tornando o próximo passo mais claro. Mantenha tom consultivo, sem sycophancy, sem se desculpar em excesso e sem inventar política comercial.
```

Perguntas de calibração:

- O score alto está apoiado em evidência observável ou em impressão subjetiva?
- O `confidence_score` deveria cair porque falta contexto?
- Algum blocker exige `REJEITAR_IMEDIATAMENTE` mesmo com boa escrita?
- A decisão respeita o limite entre output validation e business validation?
- O audit log/state files permite reconstruir por que esta decisão foi tomada?

### Fase 8: checkpoint critico de Price Negotiation

Nesta fase, o Evaluator atua como gatekeeper e procura evidência concreta antes de aceitar a saída. A pergunta não é "soa bem?". A pergunta é "o draft prova que respeitou limite comercial, margem, respeito, valor percebido e fechamento?"

| Checagem | Evidência esperada | Falha comum | Ação |
|----------|--------------------|-------------|------|
| Contexto | O draft usa fatos do cliente, não suposições | Resposta genérica | `REJEITAR` e pedir reescrita contextual |
| Dados | O draft cita apenas dados disponíveis | Inventar preço, prazo ou condição | `REJEITAR_IMEDIATAMENTE` se houver risco |
| Tom | A resposta preserva voz consultiva KODA | Pressão, frieza ou informalidade excessiva | Ajustar com feedback específico |
| Negócio | A resposta protege confiança e margem | Converter a qualquer custo | Escalar se conflito comercial persistir |
| Próximo passo | Cliente sabe o que fazer depois | Fechamento ausente ou agressivo | `APROVAR_COM_RESSALVAS` ou retry |

Exemplo de feedback útil para o Generator:

```text
Reescreva a saída de Price Negotiation preservando o fato crítico do cliente, removendo qualquer afirmação não comprovada e tornando o próximo passo mais claro. Mantenha tom consultivo, sem sycophancy, sem se desculpar em excesso e sem inventar política comercial.
```

Perguntas de calibração:

- O score alto está apoiado em evidência observável ou em impressão subjetiva?
- O `confidence_score` deveria cair porque falta contexto?
- Algum blocker exige `REJEITAR_IMEDIATAMENTE` mesmo com boa escrita?
- A decisão respeita o limite entre output validation e business validation?
- O audit log/state files permite reconstruir por que esta decisão foi tomada?

### Fase 9: checkpoint critico de Price Negotiation

Nesta fase, o Evaluator atua como gatekeeper e procura evidência concreta antes de aceitar a saída. A pergunta não é "soa bem?". A pergunta é "o draft prova que respeitou limite comercial, margem, respeito, valor percebido e fechamento?"

| Checagem | Evidência esperada | Falha comum | Ação |
|----------|--------------------|-------------|------|
| Contexto | O draft usa fatos do cliente, não suposições | Resposta genérica | `REJEITAR` e pedir reescrita contextual |
| Dados | O draft cita apenas dados disponíveis | Inventar preço, prazo ou condição | `REJEITAR_IMEDIATAMENTE` se houver risco |
| Tom | A resposta preserva voz consultiva KODA | Pressão, frieza ou informalidade excessiva | Ajustar com feedback específico |
| Negócio | A resposta protege confiança e margem | Converter a qualquer custo | Escalar se conflito comercial persistir |
| Próximo passo | Cliente sabe o que fazer depois | Fechamento ausente ou agressivo | `APROVAR_COM_RESSALVAS` ou retry |

Exemplo de feedback útil para o Generator:

```text
Reescreva a saída de Price Negotiation preservando o fato crítico do cliente, removendo qualquer afirmação não comprovada e tornando o próximo passo mais claro. Mantenha tom consultivo, sem sycophancy, sem se desculpar em excesso e sem inventar política comercial.
```

Perguntas de calibração:

- O score alto está apoiado em evidência observável ou em impressão subjetiva?
- O `confidence_score` deveria cair porque falta contexto?
- Algum blocker exige `REJEITAR_IMEDIATAMENTE` mesmo com boa escrita?
- A decisão respeita o limite entre output validation e business validation?
- O audit log/state files permite reconstruir por que esta decisão foi tomada?

### Fase 10: checkpoint critico de Price Negotiation

Nesta fase, o Evaluator atua como gatekeeper e procura evidência concreta antes de aceitar a saída. A pergunta não é "soa bem?". A pergunta é "o draft prova que respeitou limite comercial, margem, respeito, valor percebido e fechamento?"

| Checagem | Evidência esperada | Falha comum | Ação |
|----------|--------------------|-------------|------|
| Contexto | O draft usa fatos do cliente, não suposições | Resposta genérica | `REJEITAR` e pedir reescrita contextual |
| Dados | O draft cita apenas dados disponíveis | Inventar preço, prazo ou condição | `REJEITAR_IMEDIATAMENTE` se houver risco |
| Tom | A resposta preserva voz consultiva KODA | Pressão, frieza ou informalidade excessiva | Ajustar com feedback específico |
| Negócio | A resposta protege confiança e margem | Converter a qualquer custo | Escalar se conflito comercial persistir |
| Próximo passo | Cliente sabe o que fazer depois | Fechamento ausente ou agressivo | `APROVAR_COM_RESSALVAS` ou retry |

Exemplo de feedback útil para o Generator:

```text
Reescreva a saída de Price Negotiation preservando o fato crítico do cliente, removendo qualquer afirmação não comprovada e tornando o próximo passo mais claro. Mantenha tom consultivo, sem sycophancy, sem se desculpar em excesso e sem inventar política comercial.
```

Perguntas de calibração:

- O score alto está apoiado em evidência observável ou em impressão subjetiva?
- O `confidence_score` deveria cair porque falta contexto?
- Algum blocker exige `REJEITAR_IMEDIATAMENTE` mesmo com boa escrita?
- A decisão respeita o limite entre output validation e business validation?
- O audit log/state files permite reconstruir por que esta decisão foi tomada?

---

## 🧩 Playbook Operacional: Follow-Up

Este playbook transforma a rubrica de Follow-Up em rotina de operação. O foco é timing, consentimento, personalização, utilidade e CTA leve.

### Fase 1: checkpoint critico de Follow-Up

Nesta fase, o Evaluator atua como gatekeeper e procura evidência concreta antes de aceitar a saída. A pergunta não é "soa bem?". A pergunta é "o draft prova que respeitou timing, consentimento, personalização, utilidade e CTA leve?"

| Checagem | Evidência esperada | Falha comum | Ação |
|----------|--------------------|-------------|------|
| Contexto | O draft usa fatos do cliente, não suposições | Resposta genérica | `REJEITAR` e pedir reescrita contextual |
| Dados | O draft cita apenas dados disponíveis | Inventar preço, prazo ou condição | `REJEITAR_IMEDIATAMENTE` se houver risco |
| Tom | A resposta preserva voz consultiva KODA | Pressão, frieza ou informalidade excessiva | Ajustar com feedback específico |
| Negócio | A resposta protege confiança e margem | Converter a qualquer custo | Escalar se conflito comercial persistir |
| Próximo passo | Cliente sabe o que fazer depois | Fechamento ausente ou agressivo | `APROVAR_COM_RESSALVAS` ou retry |

Exemplo de feedback útil para o Generator:

```text
Reescreva a saída de Follow-Up preservando o fato crítico do cliente, removendo qualquer afirmação não comprovada e tornando o próximo passo mais claro. Mantenha tom consultivo, sem sycophancy, sem se desculpar em excesso e sem inventar política comercial.
```

Perguntas de calibração:

- O score alto está apoiado em evidência observável ou em impressão subjetiva?
- O `confidence_score` deveria cair porque falta contexto?
- Algum blocker exige `REJEITAR_IMEDIATAMENTE` mesmo com boa escrita?
- A decisão respeita o limite entre output validation e business validation?
- O audit log/state files permite reconstruir por que esta decisão foi tomada?

### Fase 2: checkpoint critico de Follow-Up

Nesta fase, o Evaluator atua como gatekeeper e procura evidência concreta antes de aceitar a saída. A pergunta não é "soa bem?". A pergunta é "o draft prova que respeitou timing, consentimento, personalização, utilidade e CTA leve?"

| Checagem | Evidência esperada | Falha comum | Ação |
|----------|--------------------|-------------|------|
| Contexto | O draft usa fatos do cliente, não suposições | Resposta genérica | `REJEITAR` e pedir reescrita contextual |
| Dados | O draft cita apenas dados disponíveis | Inventar preço, prazo ou condição | `REJEITAR_IMEDIATAMENTE` se houver risco |
| Tom | A resposta preserva voz consultiva KODA | Pressão, frieza ou informalidade excessiva | Ajustar com feedback específico |
| Negócio | A resposta protege confiança e margem | Converter a qualquer custo | Escalar se conflito comercial persistir |
| Próximo passo | Cliente sabe o que fazer depois | Fechamento ausente ou agressivo | `APROVAR_COM_RESSALVAS` ou retry |

Exemplo de feedback útil para o Generator:

```text
Reescreva a saída de Follow-Up preservando o fato crítico do cliente, removendo qualquer afirmação não comprovada e tornando o próximo passo mais claro. Mantenha tom consultivo, sem sycophancy, sem se desculpar em excesso e sem inventar política comercial.
```

Perguntas de calibração:

- O score alto está apoiado em evidência observável ou em impressão subjetiva?
- O `confidence_score` deveria cair porque falta contexto?
- Algum blocker exige `REJEITAR_IMEDIATAMENTE` mesmo com boa escrita?
- A decisão respeita o limite entre output validation e business validation?
- O audit log/state files permite reconstruir por que esta decisão foi tomada?

### Fase 3: checkpoint critico de Follow-Up

Nesta fase, o Evaluator atua como gatekeeper e procura evidência concreta antes de aceitar a saída. A pergunta não é "soa bem?". A pergunta é "o draft prova que respeitou timing, consentimento, personalização, utilidade e CTA leve?"

| Checagem | Evidência esperada | Falha comum | Ação |
|----------|--------------------|-------------|------|
| Contexto | O draft usa fatos do cliente, não suposições | Resposta genérica | `REJEITAR` e pedir reescrita contextual |
| Dados | O draft cita apenas dados disponíveis | Inventar preço, prazo ou condição | `REJEITAR_IMEDIATAMENTE` se houver risco |
| Tom | A resposta preserva voz consultiva KODA | Pressão, frieza ou informalidade excessiva | Ajustar com feedback específico |
| Negócio | A resposta protege confiança e margem | Converter a qualquer custo | Escalar se conflito comercial persistir |
| Próximo passo | Cliente sabe o que fazer depois | Fechamento ausente ou agressivo | `APROVAR_COM_RESSALVAS` ou retry |

Exemplo de feedback útil para o Generator:

```text
Reescreva a saída de Follow-Up preservando o fato crítico do cliente, removendo qualquer afirmação não comprovada e tornando o próximo passo mais claro. Mantenha tom consultivo, sem sycophancy, sem se desculpar em excesso e sem inventar política comercial.
```

Perguntas de calibração:

- O score alto está apoiado em evidência observável ou em impressão subjetiva?
- O `confidence_score` deveria cair porque falta contexto?
- Algum blocker exige `REJEITAR_IMEDIATAMENTE` mesmo com boa escrita?
- A decisão respeita o limite entre output validation e business validation?
- O audit log/state files permite reconstruir por que esta decisão foi tomada?

### Fase 4: checkpoint critico de Follow-Up

Nesta fase, o Evaluator atua como gatekeeper e procura evidência concreta antes de aceitar a saída. A pergunta não é "soa bem?". A pergunta é "o draft prova que respeitou timing, consentimento, personalização, utilidade e CTA leve?"

| Checagem | Evidência esperada | Falha comum | Ação |
|----------|--------------------|-------------|------|
| Contexto | O draft usa fatos do cliente, não suposições | Resposta genérica | `REJEITAR` e pedir reescrita contextual |
| Dados | O draft cita apenas dados disponíveis | Inventar preço, prazo ou condição | `REJEITAR_IMEDIATAMENTE` se houver risco |
| Tom | A resposta preserva voz consultiva KODA | Pressão, frieza ou informalidade excessiva | Ajustar com feedback específico |
| Negócio | A resposta protege confiança e margem | Converter a qualquer custo | Escalar se conflito comercial persistir |
| Próximo passo | Cliente sabe o que fazer depois | Fechamento ausente ou agressivo | `APROVAR_COM_RESSALVAS` ou retry |

Exemplo de feedback útil para o Generator:

```text
Reescreva a saída de Follow-Up preservando o fato crítico do cliente, removendo qualquer afirmação não comprovada e tornando o próximo passo mais claro. Mantenha tom consultivo, sem sycophancy, sem se desculpar em excesso e sem inventar política comercial.
```

Perguntas de calibração:

- O score alto está apoiado em evidência observável ou em impressão subjetiva?
- O `confidence_score` deveria cair porque falta contexto?
- Algum blocker exige `REJEITAR_IMEDIATAMENTE` mesmo com boa escrita?
- A decisão respeita o limite entre output validation e business validation?
- O audit log/state files permite reconstruir por que esta decisão foi tomada?

### Fase 5: checkpoint critico de Follow-Up

Nesta fase, o Evaluator atua como gatekeeper e procura evidência concreta antes de aceitar a saída. A pergunta não é "soa bem?". A pergunta é "o draft prova que respeitou timing, consentimento, personalização, utilidade e CTA leve?"

| Checagem | Evidência esperada | Falha comum | Ação |
|----------|--------------------|-------------|------|
| Contexto | O draft usa fatos do cliente, não suposições | Resposta genérica | `REJEITAR` e pedir reescrita contextual |
| Dados | O draft cita apenas dados disponíveis | Inventar preço, prazo ou condição | `REJEITAR_IMEDIATAMENTE` se houver risco |
| Tom | A resposta preserva voz consultiva KODA | Pressão, frieza ou informalidade excessiva | Ajustar com feedback específico |
| Negócio | A resposta protege confiança e margem | Converter a qualquer custo | Escalar se conflito comercial persistir |
| Próximo passo | Cliente sabe o que fazer depois | Fechamento ausente ou agressivo | `APROVAR_COM_RESSALVAS` ou retry |

Exemplo de feedback útil para o Generator:

```text
Reescreva a saída de Follow-Up preservando o fato crítico do cliente, removendo qualquer afirmação não comprovada e tornando o próximo passo mais claro. Mantenha tom consultivo, sem sycophancy, sem se desculpar em excesso e sem inventar política comercial.
```

Perguntas de calibração:

- O score alto está apoiado em evidência observável ou em impressão subjetiva?
- O `confidence_score` deveria cair porque falta contexto?
- Algum blocker exige `REJEITAR_IMEDIATAMENTE` mesmo com boa escrita?
- A decisão respeita o limite entre output validation e business validation?
- O audit log/state files permite reconstruir por que esta decisão foi tomada?

### Fase 6: checkpoint critico de Follow-Up

Nesta fase, o Evaluator atua como gatekeeper e procura evidência concreta antes de aceitar a saída. A pergunta não é "soa bem?". A pergunta é "o draft prova que respeitou timing, consentimento, personalização, utilidade e CTA leve?"

| Checagem | Evidência esperada | Falha comum | Ação |
|----------|--------------------|-------------|------|
| Contexto | O draft usa fatos do cliente, não suposições | Resposta genérica | `REJEITAR` e pedir reescrita contextual |
| Dados | O draft cita apenas dados disponíveis | Inventar preço, prazo ou condição | `REJEITAR_IMEDIATAMENTE` se houver risco |
| Tom | A resposta preserva voz consultiva KODA | Pressão, frieza ou informalidade excessiva | Ajustar com feedback específico |
| Negócio | A resposta protege confiança e margem | Converter a qualquer custo | Escalar se conflito comercial persistir |
| Próximo passo | Cliente sabe o que fazer depois | Fechamento ausente ou agressivo | `APROVAR_COM_RESSALVAS` ou retry |

Exemplo de feedback útil para o Generator:

```text
Reescreva a saída de Follow-Up preservando o fato crítico do cliente, removendo qualquer afirmação não comprovada e tornando o próximo passo mais claro. Mantenha tom consultivo, sem sycophancy, sem se desculpar em excesso e sem inventar política comercial.
```

Perguntas de calibração:

- O score alto está apoiado em evidência observável ou em impressão subjetiva?
- O `confidence_score` deveria cair porque falta contexto?
- Algum blocker exige `REJEITAR_IMEDIATAMENTE` mesmo com boa escrita?
- A decisão respeita o limite entre output validation e business validation?
- O audit log/state files permite reconstruir por que esta decisão foi tomada?

### Fase 7: checkpoint critico de Follow-Up

Nesta fase, o Evaluator atua como gatekeeper e procura evidência concreta antes de aceitar a saída. A pergunta não é "soa bem?". A pergunta é "o draft prova que respeitou timing, consentimento, personalização, utilidade e CTA leve?"

| Checagem | Evidência esperada | Falha comum | Ação |
|----------|--------------------|-------------|------|
| Contexto | O draft usa fatos do cliente, não suposições | Resposta genérica | `REJEITAR` e pedir reescrita contextual |
| Dados | O draft cita apenas dados disponíveis | Inventar preço, prazo ou condição | `REJEITAR_IMEDIATAMENTE` se houver risco |
| Tom | A resposta preserva voz consultiva KODA | Pressão, frieza ou informalidade excessiva | Ajustar com feedback específico |
| Negócio | A resposta protege confiança e margem | Converter a qualquer custo | Escalar se conflito comercial persistir |
| Próximo passo | Cliente sabe o que fazer depois | Fechamento ausente ou agressivo | `APROVAR_COM_RESSALVAS` ou retry |

Exemplo de feedback útil para o Generator:

```text
Reescreva a saída de Follow-Up preservando o fato crítico do cliente, removendo qualquer afirmação não comprovada e tornando o próximo passo mais claro. Mantenha tom consultivo, sem sycophancy, sem se desculpar em excesso e sem inventar política comercial.
```

Perguntas de calibração:

- O score alto está apoiado em evidência observável ou em impressão subjetiva?
- O `confidence_score` deveria cair porque falta contexto?
- Algum blocker exige `REJEITAR_IMEDIATAMENTE` mesmo com boa escrita?
- A decisão respeita o limite entre output validation e business validation?
- O audit log/state files permite reconstruir por que esta decisão foi tomada?

### Fase 8: checkpoint critico de Follow-Up

Nesta fase, o Evaluator atua como gatekeeper e procura evidência concreta antes de aceitar a saída. A pergunta não é "soa bem?". A pergunta é "o draft prova que respeitou timing, consentimento, personalização, utilidade e CTA leve?"

| Checagem | Evidência esperada | Falha comum | Ação |
|----------|--------------------|-------------|------|
| Contexto | O draft usa fatos do cliente, não suposições | Resposta genérica | `REJEITAR` e pedir reescrita contextual |
| Dados | O draft cita apenas dados disponíveis | Inventar preço, prazo ou condição | `REJEITAR_IMEDIATAMENTE` se houver risco |
| Tom | A resposta preserva voz consultiva KODA | Pressão, frieza ou informalidade excessiva | Ajustar com feedback específico |
| Negócio | A resposta protege confiança e margem | Converter a qualquer custo | Escalar se conflito comercial persistir |
| Próximo passo | Cliente sabe o que fazer depois | Fechamento ausente ou agressivo | `APROVAR_COM_RESSALVAS` ou retry |

Exemplo de feedback útil para o Generator:

```text
Reescreva a saída de Follow-Up preservando o fato crítico do cliente, removendo qualquer afirmação não comprovada e tornando o próximo passo mais claro. Mantenha tom consultivo, sem sycophancy, sem se desculpar em excesso e sem inventar política comercial.
```

Perguntas de calibração:

- O score alto está apoiado em evidência observável ou em impressão subjetiva?
- O `confidence_score` deveria cair porque falta contexto?
- Algum blocker exige `REJEITAR_IMEDIATAMENTE` mesmo com boa escrita?
- A decisão respeita o limite entre output validation e business validation?
- O audit log/state files permite reconstruir por que esta decisão foi tomada?

### Fase 9: checkpoint critico de Follow-Up

Nesta fase, o Evaluator atua como gatekeeper e procura evidência concreta antes de aceitar a saída. A pergunta não é "soa bem?". A pergunta é "o draft prova que respeitou timing, consentimento, personalização, utilidade e CTA leve?"

| Checagem | Evidência esperada | Falha comum | Ação |
|----------|--------------------|-------------|------|
| Contexto | O draft usa fatos do cliente, não suposições | Resposta genérica | `REJEITAR` e pedir reescrita contextual |
| Dados | O draft cita apenas dados disponíveis | Inventar preço, prazo ou condição | `REJEITAR_IMEDIATAMENTE` se houver risco |
| Tom | A resposta preserva voz consultiva KODA | Pressão, frieza ou informalidade excessiva | Ajustar com feedback específico |
| Negócio | A resposta protege confiança e margem | Converter a qualquer custo | Escalar se conflito comercial persistir |
| Próximo passo | Cliente sabe o que fazer depois | Fechamento ausente ou agressivo | `APROVAR_COM_RESSALVAS` ou retry |

Exemplo de feedback útil para o Generator:

```text
Reescreva a saída de Follow-Up preservando o fato crítico do cliente, removendo qualquer afirmação não comprovada e tornando o próximo passo mais claro. Mantenha tom consultivo, sem sycophancy, sem se desculpar em excesso e sem inventar política comercial.
```

Perguntas de calibração:

- O score alto está apoiado em evidência observável ou em impressão subjetiva?
- O `confidence_score` deveria cair porque falta contexto?
- Algum blocker exige `REJEITAR_IMEDIATAMENTE` mesmo com boa escrita?
- A decisão respeita o limite entre output validation e business validation?
- O audit log/state files permite reconstruir por que esta decisão foi tomada?

### Fase 10: checkpoint critico de Follow-Up

Nesta fase, o Evaluator atua como gatekeeper e procura evidência concreta antes de aceitar a saída. A pergunta não é "soa bem?". A pergunta é "o draft prova que respeitou timing, consentimento, personalização, utilidade e CTA leve?"

| Checagem | Evidência esperada | Falha comum | Ação |
|----------|--------------------|-------------|------|
| Contexto | O draft usa fatos do cliente, não suposições | Resposta genérica | `REJEITAR` e pedir reescrita contextual |
| Dados | O draft cita apenas dados disponíveis | Inventar preço, prazo ou condição | `REJEITAR_IMEDIATAMENTE` se houver risco |
| Tom | A resposta preserva voz consultiva KODA | Pressão, frieza ou informalidade excessiva | Ajustar com feedback específico |
| Negócio | A resposta protege confiança e margem | Converter a qualquer custo | Escalar se conflito comercial persistir |
| Próximo passo | Cliente sabe o que fazer depois | Fechamento ausente ou agressivo | `APROVAR_COM_RESSALVAS` ou retry |

Exemplo de feedback útil para o Generator:

```text
Reescreva a saída de Follow-Up preservando o fato crítico do cliente, removendo qualquer afirmação não comprovada e tornando o próximo passo mais claro. Mantenha tom consultivo, sem sycophancy, sem se desculpar em excesso e sem inventar política comercial.
```

Perguntas de calibração:

- O score alto está apoiado em evidência observável ou em impressão subjetiva?
- O `confidence_score` deveria cair porque falta contexto?
- Algum blocker exige `REJEITAR_IMEDIATAMENTE` mesmo com boa escrita?
- A decisão respeita o limite entre output validation e business validation?
- O audit log/state files permite reconstruir por que esta decisão foi tomada?

---

## ✅ Checklist de Validacao de Qualidade

- [ ] Existe rubric separado para Product Recommendation, Customer Response, Price Negotiation e Follow-Up.
- [ ] Cada rubric tem dimensoes, escalas, exemplos, pesos e blockers.
- [ ] Cada família tem pelo menos um exemplo bom e um exemplo ruim.
- [ ] Product Recommendation avalia accuracy, relevance e tone, além de restrições e ação.
- [ ] Price Negotiation avalia assertiveness, respect e closing, além de margem e valor.
- [ ] Follow-Up avalia timing e personalization, além de consentimento e utilidade.
- [ ] Customer Response avalia intenção, factualidade, empatia, completude e próximo passo.
- [ ] Generator/Evaluator estão separados; não há rubric scoring por self-evaluation.
- [ ] Feedback loop define max iterations antes de escalation.
- [ ] `rubric_id` e `generation_id` aparecem em todo verdict.
- [ ] `approval_threshold`, `overall_score` e `confidence_score` são registrados.
- [ ] As decisões usam vocabulário operacional consistente.
- [ ] Blockers são mais fortes que score ponderado.
- [ ] O módulo deixa claro que Sprint Contracts são separados de rubric scoring.
- [ ] O módulo deixa claro que output validation não basta sem business validation.
- [ ] A arquitetura mostra Customer Context -> Generator -> Evaluator -> Rubric Score -> feedback/decision.
- [ ] A tabela de estratégias compara file-based, in-memory, API-based e queue-based.
- [ ] A seção Aplicacao KODA conecta rubrics à rotina de Fernando.
- [ ] A calibração inclui comparação com julgamento humano e ajuste versionado.
- [ ] Não há lacunas nem espaços para preencher depois.

---

## 🎓 O Que Voce Aprendeu

- Rubrics KODA são instrumentos operacionais de decisão, não enfeites de prompt.
- O Evaluator precisa ser gatekeeper independente para reduzir sycophancy.
- Product Recommendation exige precisão, relevância, tom, segurança e ação.
- Customer Response exige compreensão de intenção, fatos corretos, empatia, completude e próximo passo.
- Price Negotiation exige assertiveness, respect, closing, margem e valor percebido.
- Follow-Up exige timing, personalization, consentimento, utilidade e CTA leve.
- `REJEITAR_IMEDIATAMENTE` existe para blockers de risco, não para gosto pessoal.
- `APROVAR_COM_RESSALVAS` permite pragmatismo quando a falha é pequena e segura.
- `overall_score` mede qualidade ponderada; `confidence_score` mede confiança na avaliação.
- `rubric_id` e `generation_id` tornam decisões rastreáveis.
- Output validation confirma forma; business validation confirma valor e segurança.
- Sprint Contracts continuam separados: eles alinham escopo, enquanto rubrics medem qualidade.
- Calibração transforma rubrics de intenção boa em ferramenta confiável.
- Audit log/state files permitem trace reading e melhoria contínua.

Se você consegue explicar esses pontos com exemplos reais de WhatsApp, você não está apenas lendo sobre rubrics. Você está pronto para operar qualidade em KODA.

---

## 🚶 Proximos Passos

1. Escolha 20 conversas reais de cada família e classifique manualmente com os rubrics deste módulo.
1. Compare decisões humanas com decisões do Evaluator e registre divergências.
1. Ajuste pesos apenas quando houver evidência, não por intuição isolada.
1. Crie fixtures de calibração para Product Recommendation, Customer Response, Price Negotiation e Follow-Up.
1. Implemente audit log/state files antes de aumentar automação.
1. Defina política de escalation para blockers e baixa confiança.
1. Revise rubrics sempre que catálogo, política comercial ou tom de marca mudar.

A maturidade de KODA não aparece quando tudo dá certo. Ela aparece quando um draft ruim é barrado antes de chegar ao cliente, quando um desconto falso não passa, quando um follow-up não vira spam e quando Fernando consegue abrir o audit log e entender exatamente por que o sistema decidiu o que decidiu.

---

## 📄 Metadata de Fechamento

| Campo | Valor |
|-------|-------|
| Módulo | `04-evaluation-rubrics-koda.md` |
| Nível | 4 - KODA Specific |
| Famílias cobertas | Product Recommendation, Customer Response, Price Negotiation, Follow-Up |
| Padrões integrados | Generator/Evaluator, Rubric Design, Trace Reading, State Persistence |
| Decisões suportadas | `APROVAR`, `APROVAR_COM_RESSALVAS`, `REJEITAR`, `REJEITAR_IMEDIATAMENTE` |
| Artefatos | `rubric_id`, `generation_id`, `approval_threshold`, `overall_score`, `confidence_score`, audit log/state files |
| Autor operacional | Equipe KODA com exemplos narrativos de Fernando |
| Versão curricular | Maio 2026 |

**Resumo final:** KODA não precisa apenas responder. KODA precisa responder bem, responder com segurança, responder com negócio em mente e deixar evidência de por que aquela resposta passou pelo gatekeeper. Rubrics são a ponte entre intenção de qualidade e qualidade auditável.

## 📚 Catalogo de Casos de Calibracao KODA

Esta seção final oferece casos curtos para workshops. Cada caso é concreto, avaliável e ligado às quatro famílias. Use como banco inicial para treinar humanos e Evaluators.

### Caso de calibracao 001: Product Recommendation

- **Situação:** Cliente quer hipertrofia, orçamento controlado, restrição alimentar e dúvida sobre sabor.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar se o produto recomendado existe, cabe no orçamento e respeita restrição.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 002: Customer Response

- **Situação:** Cliente relata entrega incorreta, frustração e urgência para resolver antes de viagem.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar empatia, política real e próximo passo operacional.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 003: Price Negotiation

- **Situação:** Cliente compara preço com concorrente e pede condição abaixo da margem.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar assertividade, respeito, valor e fechamento sem desconto falso.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 004: Follow-Up

- **Situação:** Cliente pediu lembrete em horário específico sobre produto sem lactose.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar timing, personalização, consentimento e CTA leve.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 005: Product Recommendation

- **Situação:** Cliente quer hipertrofia, orçamento controlado, restrição alimentar e dúvida sobre sabor.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar se o produto recomendado existe, cabe no orçamento e respeita restrição.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 006: Customer Response

- **Situação:** Cliente relata entrega incorreta, frustração e urgência para resolver antes de viagem.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar empatia, política real e próximo passo operacional.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 007: Price Negotiation

- **Situação:** Cliente compara preço com concorrente e pede condição abaixo da margem.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar assertividade, respeito, valor e fechamento sem desconto falso.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 008: Follow-Up

- **Situação:** Cliente pediu lembrete em horário específico sobre produto sem lactose.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar timing, personalização, consentimento e CTA leve.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 009: Product Recommendation

- **Situação:** Cliente quer hipertrofia, orçamento controlado, restrição alimentar e dúvida sobre sabor.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar se o produto recomendado existe, cabe no orçamento e respeita restrição.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 010: Customer Response

- **Situação:** Cliente relata entrega incorreta, frustração e urgência para resolver antes de viagem.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar empatia, política real e próximo passo operacional.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 011: Price Negotiation

- **Situação:** Cliente compara preço com concorrente e pede condição abaixo da margem.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar assertividade, respeito, valor e fechamento sem desconto falso.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 012: Follow-Up

- **Situação:** Cliente pediu lembrete em horário específico sobre produto sem lactose.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar timing, personalização, consentimento e CTA leve.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 013: Product Recommendation

- **Situação:** Cliente quer hipertrofia, orçamento controlado, restrição alimentar e dúvida sobre sabor.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar se o produto recomendado existe, cabe no orçamento e respeita restrição.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 014: Customer Response

- **Situação:** Cliente relata entrega incorreta, frustração e urgência para resolver antes de viagem.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar empatia, política real e próximo passo operacional.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 015: Price Negotiation

- **Situação:** Cliente compara preço com concorrente e pede condição abaixo da margem.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar assertividade, respeito, valor e fechamento sem desconto falso.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 016: Follow-Up

- **Situação:** Cliente pediu lembrete em horário específico sobre produto sem lactose.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar timing, personalização, consentimento e CTA leve.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 017: Product Recommendation

- **Situação:** Cliente quer hipertrofia, orçamento controlado, restrição alimentar e dúvida sobre sabor.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar se o produto recomendado existe, cabe no orçamento e respeita restrição.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 018: Customer Response

- **Situação:** Cliente relata entrega incorreta, frustração e urgência para resolver antes de viagem.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar empatia, política real e próximo passo operacional.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 019: Price Negotiation

- **Situação:** Cliente compara preço com concorrente e pede condição abaixo da margem.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar assertividade, respeito, valor e fechamento sem desconto falso.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 020: Follow-Up

- **Situação:** Cliente pediu lembrete em horário específico sobre produto sem lactose.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar timing, personalização, consentimento e CTA leve.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 021: Product Recommendation

- **Situação:** Cliente quer hipertrofia, orçamento controlado, restrição alimentar e dúvida sobre sabor.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar se o produto recomendado existe, cabe no orçamento e respeita restrição.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 022: Customer Response

- **Situação:** Cliente relata entrega incorreta, frustração e urgência para resolver antes de viagem.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar empatia, política real e próximo passo operacional.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 023: Price Negotiation

- **Situação:** Cliente compara preço com concorrente e pede condição abaixo da margem.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar assertividade, respeito, valor e fechamento sem desconto falso.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 024: Follow-Up

- **Situação:** Cliente pediu lembrete em horário específico sobre produto sem lactose.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar timing, personalização, consentimento e CTA leve.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 025: Product Recommendation

- **Situação:** Cliente quer hipertrofia, orçamento controlado, restrição alimentar e dúvida sobre sabor.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar se o produto recomendado existe, cabe no orçamento e respeita restrição.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 026: Customer Response

- **Situação:** Cliente relata entrega incorreta, frustração e urgência para resolver antes de viagem.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar empatia, política real e próximo passo operacional.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 027: Price Negotiation

- **Situação:** Cliente compara preço com concorrente e pede condição abaixo da margem.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar assertividade, respeito, valor e fechamento sem desconto falso.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 028: Follow-Up

- **Situação:** Cliente pediu lembrete em horário específico sobre produto sem lactose.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar timing, personalização, consentimento e CTA leve.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 029: Product Recommendation

- **Situação:** Cliente quer hipertrofia, orçamento controlado, restrição alimentar e dúvida sobre sabor.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar se o produto recomendado existe, cabe no orçamento e respeita restrição.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 030: Customer Response

- **Situação:** Cliente relata entrega incorreta, frustração e urgência para resolver antes de viagem.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar empatia, política real e próximo passo operacional.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 031: Price Negotiation

- **Situação:** Cliente compara preço com concorrente e pede condição abaixo da margem.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar assertividade, respeito, valor e fechamento sem desconto falso.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 032: Follow-Up

- **Situação:** Cliente pediu lembrete em horário específico sobre produto sem lactose.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar timing, personalização, consentimento e CTA leve.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 033: Product Recommendation

- **Situação:** Cliente quer hipertrofia, orçamento controlado, restrição alimentar e dúvida sobre sabor.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar se o produto recomendado existe, cabe no orçamento e respeita restrição.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 034: Customer Response

- **Situação:** Cliente relata entrega incorreta, frustração e urgência para resolver antes de viagem.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar empatia, política real e próximo passo operacional.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 035: Price Negotiation

- **Situação:** Cliente compara preço com concorrente e pede condição abaixo da margem.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar assertividade, respeito, valor e fechamento sem desconto falso.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 036: Follow-Up

- **Situação:** Cliente pediu lembrete em horário específico sobre produto sem lactose.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar timing, personalização, consentimento e CTA leve.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 037: Product Recommendation

- **Situação:** Cliente quer hipertrofia, orçamento controlado, restrição alimentar e dúvida sobre sabor.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar se o produto recomendado existe, cabe no orçamento e respeita restrição.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 038: Customer Response

- **Situação:** Cliente relata entrega incorreta, frustração e urgência para resolver antes de viagem.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar empatia, política real e próximo passo operacional.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 039: Price Negotiation

- **Situação:** Cliente compara preço com concorrente e pede condição abaixo da margem.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar assertividade, respeito, valor e fechamento sem desconto falso.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 040: Follow-Up

- **Situação:** Cliente pediu lembrete em horário específico sobre produto sem lactose.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar timing, personalização, consentimento e CTA leve.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 041: Product Recommendation

- **Situação:** Cliente quer hipertrofia, orçamento controlado, restrição alimentar e dúvida sobre sabor.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar se o produto recomendado existe, cabe no orçamento e respeita restrição.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 042: Customer Response

- **Situação:** Cliente relata entrega incorreta, frustração e urgência para resolver antes de viagem.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar empatia, política real e próximo passo operacional.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 043: Price Negotiation

- **Situação:** Cliente compara preço com concorrente e pede condição abaixo da margem.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar assertividade, respeito, valor e fechamento sem desconto falso.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 044: Follow-Up

- **Situação:** Cliente pediu lembrete em horário específico sobre produto sem lactose.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar timing, personalização, consentimento e CTA leve.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 045: Product Recommendation

- **Situação:** Cliente quer hipertrofia, orçamento controlado, restrição alimentar e dúvida sobre sabor.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar se o produto recomendado existe, cabe no orçamento e respeita restrição.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 046: Customer Response

- **Situação:** Cliente relata entrega incorreta, frustração e urgência para resolver antes de viagem.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar empatia, política real e próximo passo operacional.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 047: Price Negotiation

- **Situação:** Cliente compara preço com concorrente e pede condição abaixo da margem.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar assertividade, respeito, valor e fechamento sem desconto falso.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 048: Follow-Up

- **Situação:** Cliente pediu lembrete em horário específico sobre produto sem lactose.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar timing, personalização, consentimento e CTA leve.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 049: Product Recommendation

- **Situação:** Cliente quer hipertrofia, orçamento controlado, restrição alimentar e dúvida sobre sabor.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar se o produto recomendado existe, cabe no orçamento e respeita restrição.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 050: Customer Response

- **Situação:** Cliente relata entrega incorreta, frustração e urgência para resolver antes de viagem.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar empatia, política real e próximo passo operacional.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 051: Price Negotiation

- **Situação:** Cliente compara preço com concorrente e pede condição abaixo da margem.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar assertividade, respeito, valor e fechamento sem desconto falso.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 052: Follow-Up

- **Situação:** Cliente pediu lembrete em horário específico sobre produto sem lactose.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar timing, personalização, consentimento e CTA leve.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 053: Product Recommendation

- **Situação:** Cliente quer hipertrofia, orçamento controlado, restrição alimentar e dúvida sobre sabor.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar se o produto recomendado existe, cabe no orçamento e respeita restrição.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 054: Customer Response

- **Situação:** Cliente relata entrega incorreta, frustração e urgência para resolver antes de viagem.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar empatia, política real e próximo passo operacional.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 055: Price Negotiation

- **Situação:** Cliente compara preço com concorrente e pede condição abaixo da margem.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar assertividade, respeito, valor e fechamento sem desconto falso.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 056: Follow-Up

- **Situação:** Cliente pediu lembrete em horário específico sobre produto sem lactose.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar timing, personalização, consentimento e CTA leve.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 057: Product Recommendation

- **Situação:** Cliente quer hipertrofia, orçamento controlado, restrição alimentar e dúvida sobre sabor.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar se o produto recomendado existe, cabe no orçamento e respeita restrição.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 058: Customer Response

- **Situação:** Cliente relata entrega incorreta, frustração e urgência para resolver antes de viagem.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar empatia, política real e próximo passo operacional.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 059: Price Negotiation

- **Situação:** Cliente compara preço com concorrente e pede condição abaixo da margem.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar assertividade, respeito, valor e fechamento sem desconto falso.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 060: Follow-Up

- **Situação:** Cliente pediu lembrete em horário específico sobre produto sem lactose.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar timing, personalização, consentimento e CTA leve.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 061: Product Recommendation

- **Situação:** Cliente quer hipertrofia, orçamento controlado, restrição alimentar e dúvida sobre sabor.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar se o produto recomendado existe, cabe no orçamento e respeita restrição.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 062: Customer Response

- **Situação:** Cliente relata entrega incorreta, frustração e urgência para resolver antes de viagem.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar empatia, política real e próximo passo operacional.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 063: Price Negotiation

- **Situação:** Cliente compara preço com concorrente e pede condição abaixo da margem.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar assertividade, respeito, valor e fechamento sem desconto falso.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 064: Follow-Up

- **Situação:** Cliente pediu lembrete em horário específico sobre produto sem lactose.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar timing, personalização, consentimento e CTA leve.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 065: Product Recommendation

- **Situação:** Cliente quer hipertrofia, orçamento controlado, restrição alimentar e dúvida sobre sabor.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar se o produto recomendado existe, cabe no orçamento e respeita restrição.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 066: Customer Response

- **Situação:** Cliente relata entrega incorreta, frustração e urgência para resolver antes de viagem.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar empatia, política real e próximo passo operacional.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 067: Price Negotiation

- **Situação:** Cliente compara preço com concorrente e pede condição abaixo da margem.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar assertividade, respeito, valor e fechamento sem desconto falso.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 068: Follow-Up

- **Situação:** Cliente pediu lembrete em horário específico sobre produto sem lactose.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar timing, personalização, consentimento e CTA leve.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 069: Product Recommendation

- **Situação:** Cliente quer hipertrofia, orçamento controlado, restrição alimentar e dúvida sobre sabor.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar se o produto recomendado existe, cabe no orçamento e respeita restrição.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 070: Customer Response

- **Situação:** Cliente relata entrega incorreta, frustração e urgência para resolver antes de viagem.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar empatia, política real e próximo passo operacional.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 071: Price Negotiation

- **Situação:** Cliente compara preço com concorrente e pede condição abaixo da margem.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar assertividade, respeito, valor e fechamento sem desconto falso.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 072: Follow-Up

- **Situação:** Cliente pediu lembrete em horário específico sobre produto sem lactose.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar timing, personalização, consentimento e CTA leve.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 073: Product Recommendation

- **Situação:** Cliente quer hipertrofia, orçamento controlado, restrição alimentar e dúvida sobre sabor.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar se o produto recomendado existe, cabe no orçamento e respeita restrição.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 074: Customer Response

- **Situação:** Cliente relata entrega incorreta, frustração e urgência para resolver antes de viagem.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar empatia, política real e próximo passo operacional.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 075: Price Negotiation

- **Situação:** Cliente compara preço com concorrente e pede condição abaixo da margem.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar assertividade, respeito, valor e fechamento sem desconto falso.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 076: Follow-Up

- **Situação:** Cliente pediu lembrete em horário específico sobre produto sem lactose.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar timing, personalização, consentimento e CTA leve.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 077: Product Recommendation

- **Situação:** Cliente quer hipertrofia, orçamento controlado, restrição alimentar e dúvida sobre sabor.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar se o produto recomendado existe, cabe no orçamento e respeita restrição.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 078: Customer Response

- **Situação:** Cliente relata entrega incorreta, frustração e urgência para resolver antes de viagem.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar empatia, política real e próximo passo operacional.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 079: Price Negotiation

- **Situação:** Cliente compara preço com concorrente e pede condição abaixo da margem.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar assertividade, respeito, valor e fechamento sem desconto falso.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 080: Follow-Up

- **Situação:** Cliente pediu lembrete em horário específico sobre produto sem lactose.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar timing, personalização, consentimento e CTA leve.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 081: Product Recommendation

- **Situação:** Cliente quer hipertrofia, orçamento controlado, restrição alimentar e dúvida sobre sabor.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar se o produto recomendado existe, cabe no orçamento e respeita restrição.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 082: Customer Response

- **Situação:** Cliente relata entrega incorreta, frustração e urgência para resolver antes de viagem.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar empatia, política real e próximo passo operacional.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 083: Price Negotiation

- **Situação:** Cliente compara preço com concorrente e pede condição abaixo da margem.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar assertividade, respeito, valor e fechamento sem desconto falso.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 084: Follow-Up

- **Situação:** Cliente pediu lembrete em horário específico sobre produto sem lactose.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar timing, personalização, consentimento e CTA leve.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 085: Product Recommendation

- **Situação:** Cliente quer hipertrofia, orçamento controlado, restrição alimentar e dúvida sobre sabor.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar se o produto recomendado existe, cabe no orçamento e respeita restrição.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 086: Customer Response

- **Situação:** Cliente relata entrega incorreta, frustração e urgência para resolver antes de viagem.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar empatia, política real e próximo passo operacional.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 087: Price Negotiation

- **Situação:** Cliente compara preço com concorrente e pede condição abaixo da margem.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar assertividade, respeito, valor e fechamento sem desconto falso.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 088: Follow-Up

- **Situação:** Cliente pediu lembrete em horário específico sobre produto sem lactose.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar timing, personalização, consentimento e CTA leve.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 089: Product Recommendation

- **Situação:** Cliente quer hipertrofia, orçamento controlado, restrição alimentar e dúvida sobre sabor.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar se o produto recomendado existe, cabe no orçamento e respeita restrição.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 090: Customer Response

- **Situação:** Cliente relata entrega incorreta, frustração e urgência para resolver antes de viagem.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar empatia, política real e próximo passo operacional.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 091: Price Negotiation

- **Situação:** Cliente compara preço com concorrente e pede condição abaixo da margem.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar assertividade, respeito, valor e fechamento sem desconto falso.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 092: Follow-Up

- **Situação:** Cliente pediu lembrete em horário específico sobre produto sem lactose.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar timing, personalização, consentimento e CTA leve.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 093: Product Recommendation

- **Situação:** Cliente quer hipertrofia, orçamento controlado, restrição alimentar e dúvida sobre sabor.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar se o produto recomendado existe, cabe no orçamento e respeita restrição.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 094: Customer Response

- **Situação:** Cliente relata entrega incorreta, frustração e urgência para resolver antes de viagem.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar empatia, política real e próximo passo operacional.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 095: Price Negotiation

- **Situação:** Cliente compara preço com concorrente e pede condição abaixo da margem.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar assertividade, respeito, valor e fechamento sem desconto falso.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 096: Follow-Up

- **Situação:** Cliente pediu lembrete em horário específico sobre produto sem lactose.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar timing, personalização, consentimento e CTA leve.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 097: Product Recommendation

- **Situação:** Cliente quer hipertrofia, orçamento controlado, restrição alimentar e dúvida sobre sabor.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar se o produto recomendado existe, cabe no orçamento e respeita restrição.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 098: Customer Response

- **Situação:** Cliente relata entrega incorreta, frustração e urgência para resolver antes de viagem.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar empatia, política real e próximo passo operacional.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 099: Price Negotiation

- **Situação:** Cliente compara preço com concorrente e pede condição abaixo da margem.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar assertividade, respeito, valor e fechamento sem desconto falso.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 100: Follow-Up

- **Situação:** Cliente pediu lembrete em horário específico sobre produto sem lactose.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar timing, personalização, consentimento e CTA leve.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 101: Product Recommendation

- **Situação:** Cliente quer hipertrofia, orçamento controlado, restrição alimentar e dúvida sobre sabor.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar se o produto recomendado existe, cabe no orçamento e respeita restrição.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 102: Customer Response

- **Situação:** Cliente relata entrega incorreta, frustração e urgência para resolver antes de viagem.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar empatia, política real e próximo passo operacional.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 103: Price Negotiation

- **Situação:** Cliente compara preço com concorrente e pede condição abaixo da margem.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar assertividade, respeito, valor e fechamento sem desconto falso.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 104: Follow-Up

- **Situação:** Cliente pediu lembrete em horário específico sobre produto sem lactose.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar timing, personalização, consentimento e CTA leve.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 105: Product Recommendation

- **Situação:** Cliente quer hipertrofia, orçamento controlado, restrição alimentar e dúvida sobre sabor.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar se o produto recomendado existe, cabe no orçamento e respeita restrição.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 106: Customer Response

- **Situação:** Cliente relata entrega incorreta, frustração e urgência para resolver antes de viagem.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar empatia, política real e próximo passo operacional.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 107: Price Negotiation

- **Situação:** Cliente compara preço com concorrente e pede condição abaixo da margem.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar assertividade, respeito, valor e fechamento sem desconto falso.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 108: Follow-Up

- **Situação:** Cliente pediu lembrete em horário específico sobre produto sem lactose.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar timing, personalização, consentimento e CTA leve.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 109: Product Recommendation

- **Situação:** Cliente quer hipertrofia, orçamento controlado, restrição alimentar e dúvida sobre sabor.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar se o produto recomendado existe, cabe no orçamento e respeita restrição.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 110: Customer Response

- **Situação:** Cliente relata entrega incorreta, frustração e urgência para resolver antes de viagem.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar empatia, política real e próximo passo operacional.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 111: Price Negotiation

- **Situação:** Cliente compara preço com concorrente e pede condição abaixo da margem.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar assertividade, respeito, valor e fechamento sem desconto falso.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 112: Follow-Up

- **Situação:** Cliente pediu lembrete em horário específico sobre produto sem lactose.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar timing, personalização, consentimento e CTA leve.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 113: Product Recommendation

- **Situação:** Cliente quer hipertrofia, orçamento controlado, restrição alimentar e dúvida sobre sabor.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar se o produto recomendado existe, cabe no orçamento e respeita restrição.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 114: Customer Response

- **Situação:** Cliente relata entrega incorreta, frustração e urgência para resolver antes de viagem.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar empatia, política real e próximo passo operacional.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 115: Price Negotiation

- **Situação:** Cliente compara preço com concorrente e pede condição abaixo da margem.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar assertividade, respeito, valor e fechamento sem desconto falso.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 116: Follow-Up

- **Situação:** Cliente pediu lembrete em horário específico sobre produto sem lactose.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar timing, personalização, consentimento e CTA leve.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 117: Product Recommendation

- **Situação:** Cliente quer hipertrofia, orçamento controlado, restrição alimentar e dúvida sobre sabor.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar se o produto recomendado existe, cabe no orçamento e respeita restrição.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 118: Customer Response

- **Situação:** Cliente relata entrega incorreta, frustração e urgência para resolver antes de viagem.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar empatia, política real e próximo passo operacional.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 119: Price Negotiation

- **Situação:** Cliente compara preço com concorrente e pede condição abaixo da margem.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar assertividade, respeito, valor e fechamento sem desconto falso.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?

### Caso de calibracao 120: Follow-Up

- **Situação:** Cliente pediu lembrete em horário específico sobre produto sem lactose.
- **Draft provável:** KODA tenta responder rápido e pode esquecer uma restrição crítica ou exagerar no fechamento.
- **Evidência exigida:** Verificar timing, personalização, consentimento e CTA leve.
- **Decisão esperada se a evidência faltar:** `REJEITAR`.
- **Decisão esperada se houver risco direto:** `REJEITAR_IMEDIATAMENTE`.
- **Sinal de aprovação:** resposta contextual, factual, segura, com próximo passo claro e auditável.
- **Pergunta para o avaliador:** qual dimensão recebeu menor nota e qual feedback específico corrige a próxima geração?
