# 🎯 Padrões de Design de Features: Como Estender o KODA com Confiança
## Templates, Contratos e Padrões para Novas Funcionalidades

**Tempo Estimado:** 150-180 minutos  
**Nível:** 4 - KODA-Específico  
**Pré-requisito:** Ter completado Níveis 1-3: fundamentos, padrões práticos e arquitetura avançada  
**Status:** 🟢 CRÍTICO - Guia de implementação para novas features KODA  
**Data de Criação:** Maio 2026

---

## 📖 Prólogo: A Feature Que Parecia Pequena
Segunda-feira, 9h12. Fernando chegou na sala de engenharia com um café na mão e uma pergunta simples no rosto.
A equipe queria lançar uma nova feature: recomendações de combos personalizados no WhatsApp.
Na descrição do produto, parecia pequeno.
Na reunião de planejamento, parecia pequeno.
No primeiro ticket, parecia quase trivial.
“Quando o cliente compra whey, KODA sugere creatina junto”, alguém disse.
Todo mundo assentiu, porque KODA já recomendava produtos.
KODA já conhecia o catálogo.
KODA já tinha Generator/Evaluator.
KODA já usava Sprint Contract nas etapas críticas.
KODA já persistia estado fora da context window.
Então a feature deveria ser apenas uma regra a mais, certo?
Fernando não respondeu na hora.
Ele abriu um trace antigo de uma conversa de duas horas.
O cliente começou pedindo algo para ganhar massa.
Depois mencionou intolerância à lactose.
Depois disse que treinava à noite.
Depois perguntou sobre frete.
Depois pediu desconto.
Depois quase desistiu por causa do orçamento.
Depois voltou porque lembrou que tinha cupom.
E só no final aceitou comprar.
Naquela conversa, a recomendação parecia uma frase simples.
Mas por baixo dela existiam dezenas de decisões pequenas.
Qual dado do cliente é confiável?
Qual preferência é recente?
Qual restrição é permanente?
Qual produto está em estoque agora?
Qual desconto pode ser combinado?
Qual sugestão parece ajuda e qual parece pressão de venda?
Qual mensagem respeita o momento emocional do cliente?
Qual resposta mantém a confiança construída durante horas?
A nova feature de combo não era apenas uma regra.
Era uma nova peça entrando em um pipeline vivo.
E peças novas, quando entram sem design, quebram coisas antigas.
O primeiro protótipo provou isso em menos de uma tarde.
KODA recomendou creatina para um cliente que havia dito ter orientação médica para evitar creatina.
KODA ofereceu upsell para um cliente que estava reclamando de preço.
KODA repetiu a mesma sugestão três vezes porque o estado da feature não registrava que a oferta já havia sido feita.
KODA gerou uma explicação boa, mas o Evaluator avaliou o draft errado porque o feature output não tinha feature_run_id.
Nada disso era um bug isolado.
Era ausência de um padrão de design para features.
Fernando então desenhou três caixas no quadro.
A primeira caixa dizia: Contract.
A segunda caixa dizia: Generator.
A terceira caixa dizia: Evaluator.
“Uma feature KODA madura”, ele disse, “não é uma função. É um acordo operacional entre essas três partes.”
A sala ficou quieta.
Ele continuou.
“O Contract define o que entra, o que sai, o que nunca pode ser violado e como validamos.”
“O Generator produz a melhor tentativa dentro desse contrato.”
“O Evaluator decide se essa tentativa merece entrar na conversa real com o cliente.”
“Se qualquer uma dessas três partes estiver implícita, a feature vira dívida técnica.”
Essa foi a virada.
A equipe parou de perguntar qual código escrever primeiro.
Começou a perguntar qual contrato a feature assinaria com o pipeline do KODA.
Começou a perguntar qual trace um engenheiro leria quando algo desse errado.
Começou a perguntar qual rubric protegeria o cliente, o negócio e a confiança.
E a feature de combo deixou de ser uma gambiarra em prompt.
Virou um módulo auditável, testável e coordenado.
Este módulo existe para te levar exatamente até esse ponto.
Você já aprendeu por que agentes perdem o foco.
Você já aprendeu a separar Generator e Evaluator.
Você já aprendeu a coordenar múltiplos agentes, persistir estado e ler traces.
Agora você vai transformar tudo isso em um jeito consistente de desenhar features KODA.
Não features que funcionam apenas no demo.
Features que sobrevivem a conversas longas, clientes ambíguos, token budget apertado e pressão real de vendas.
Esse é o salto do Nível 4.

---

## 🔍 Conexão com os Níveis 1-3
Feature Design Patterns não substituem os Níveis 1, 2 e 3; eles os consolidam em uma disciplina prática de implementação.
No Nível 1, você aprendeu por que context window, token budget e harness fraco derrubam agentes em conversas longas.
No Nível 2, você aprendeu Generator/Evaluator, Sprint Contract, rubric e trace reading como mecanismos de rigor operacional.
No Nível 3, você aprendeu state persistence, file-based coordination, multi-agent coordination e harness evolution.
No Nível 4, cada conceito vira uma pergunta concreta antes de criar uma feature nova.

| Nível | Conceito | Pergunta que a feature precisa responder |
|-------|----------|-------------------------------------------|
| Nível 1 | Context Amnesia | Quais fatos críticos saem da context window e entram em state persistence? |
| Nível 1 | Token Budgeting | Quanto contexto a feature consome e qual evidência pode ser compactada? |
| Nível 1 | Planning vs. Execution Collapse | Onde separamos decisão, geração, validação e commit? |
| Nível 1 | Self-Evaluation Collapse | Qual Evaluator independente impede o Generator de se aprovar? |
| Nível 2 | Generator/Evaluator | O que o Generator cria e o que o Evaluator reprova? |
| Nível 2 | Sprint Contract | Que promessa cada etapa faz para a próxima etapa? |
| Nível 2 | Rubric Design | Como medimos qualidade além de validade estrutural? |
| Nível 2 | Trace Reading | Qual evidência ficará disponível quando uma decisão for questionada? |
| Nível 3 | Multi-agent coordination | Quais agentes colaboram e quem tem autoridade final? |
| Nível 3 | State persistence | Que estado a feature lê, grava, expira e protege? |
| Nível 3 | File-based coordination | Quais artefatos auditáveis atravessam o pipeline? |
| Nível 3 | Harness evolution | Como a feature evolui sem quebrar contratos antigos ativos? |

A ponte central é simples e poderosa: uma feature KODA é uma unidade de comportamento e também uma unidade de coordenação.
Ela conversa com catálogo, estoque, perfil do cliente, histórico, descontos, fulfillment, WhatsApp e avaliação de qualidade.
Se você desenha apenas o prompt, desenha uma fração da feature.
Se você desenha Contract, Generator, Evaluator, trace, state e integração, desenha a feature inteira.

---

## 🎯 Anatomia de uma Feature KODA
Uma feature KODA é uma capacidade operacional que participa da conversa com o cliente e do pipeline interno de decisão.
Ela pode ser grande, como processamento de pedido, ou pequena, como sugerir coqueteleira depois de whey.
O tamanho importa menos que o risco: se influencia o que o cliente compra, quanto paga, quando recebe ou se confia no KODA, precisa de design explícito.

A arquitetura mínima tem três partes:
1. **Contract:** a promessa verificável da feature.
2. **Generator:** o componente que produz a proposta da feature.
3. **Evaluator:** o componente que decide se a proposta é segura, boa e compatível com o contexto.

### Contract: A Promessa Verificável
- **Identidade:** nome estável, versão, owner, escopo e business goal.
- **Input contract:** campos obrigatórios que eliminam adivinhação do Generator.
- **Output contract:** estrutura que o pipeline seguinte pode consumir sem surpresa.
- **Guarantees:** propriedades que sempre devem ser verdade quando a feature aprova um output.
- **Constraints:** limites que a feature jamais pode ultrapassar, mesmo quando conversão parece atraente.
- **Validation rules:** regras executáveis ou revisáveis que transformam contrato em gate real.
- **Rubric:** critérios de qualidade que dizem se o output é bom, não apenas válido.
- **Trace schema:** eventos que precisam ser registrados para debugging, replay e auditoria.
- **Token budget:** limite de tokens e política de compaction quando a conversa cresce.
- **State policy:** o que a feature lê, grava, expira e compartilha com outras features.

O Contract é o antídoto contra ambiguidade.
Ele impede que a feature dependa de bom senso do modelo quando deveria depender de dados explícitos.
Ele também impede que o pipeline aceite outputs convincentes, mas incompletos.

#### Perguntas que um Contract precisa responder
1. Qual intenção do cliente ativa a feature?
2. Qual estágio da jornada bloqueia a feature?
3. Quais campos vêm de state persistence?
4. Quais campos vêm do catálogo fresco?
5. Quais campos vêm do último trace segment?
6. Qual evidência precisa acompanhar cada recomendação?
7. Qual informação não pode ser colocada na mensagem final por privacidade?
8. Qual regra comercial tem prioridade sobre conversão?
9. Qual regra de segurança tem prioridade sobre regra comercial?
10. Qual state update só pode ocorrer após aprovação?
11. Qual erro exige NEEDS_HUMAN_REVIEW?
12. Qual dado ausente força abstinência?
13. Qual output deve ser idempotente?
14. Qual evento precisa aparecer no trace?
15. Qual métrica provará que a feature ficou melhor?

### Generator: A Melhor Tentativa Dentro do Contrato
O Generator cria a proposta, mas não a aprova.
Essa separação é intencional porque evita o Self-Evaluation Collapse.
Quando o Generator tenta gerar e se validar, ele tende a racionalizar falhas em vez de expor incerteza.

- Lê o input contract já validado antes de chamar modelo ou lógica determinística.
- Carrega somente contexto necessário para respeitar token budget.
- Usa intenção atual, estado persistido e dados atuais do catálogo.
- Gera output estruturado, com IDs estáveis e justificativas curtas.
- Expõe incertezas em campos próprios, não em texto ambíguo.
- Nunca envia mensagem ao cliente diretamente quando a feature exige avaliação.
- Nunca modifica estado final antes de aprovação do Evaluator.
- Nunca inventa campos fora do output contract.
- Nunca ignora constraints para melhorar conversão.
- Registra trace de entrada, decisão, output gerado e evidence usada.

Pense no Generator como um engenheiro propondo um pull request.
Ele deve fazer o melhor trabalho possível, mas o merge depende de revisão.

#### Pseudocódigo do Generator
```json
{
  "generator_run": {
    "feature_run_id": "feat_2026_05_28_001",
    "feature_name": "koda.product_recommendation",
    "validated_input": "feature_input_v1.json",
    "token_budget": {"max_context_tokens": 6000, "reserved_output_tokens": 900},
    "strategy": "gerar ate 3 produtos compatíveis, explicar trade-offs e expor incertezas",
    "output": "feature_proposal_v1.json",
    "trace_event": "feature_generation_completed"
  }
}
```

### Evaluator: O Gatekeeper da Confiança
O Evaluator recebe o output do Generator, o contract e evidências adicionais.
Seu trabalho não é ser simpático; seu trabalho é proteger cliente, negócio e integridade do pipeline.

- Confirma que o output respeita o output contract.
- Confirma que guarantees continuam verdadeiras depois da geração.
- Confirma que constraints não foram violadas.
- Aplica rubric de qualidade com score e justificativa.
- Compara a proposta com restrições persistidas do cliente.
- Verifica se dados atuais de estoque, preço e promoção foram usados.
- Detecta repetição de ofertas já recusadas.
- Detecta linguagem agressiva, insegura ou desalinhada com WhatsApp.
- Retorna APPROVED, REJECTED ou NEEDS_HUMAN_REVIEW com razão específica.
- Escreve feedback que o Generator consegue usar em retry.

Um bom Evaluator é específico.
Ele não diz “a recomendação está ruim”.
Ele diz “produto WHEY-ISO-001 viola customer.restrictions.lactose_free_required e deve ser removido”.

#### Pseudocódigo do Evaluator
```json
{
  "evaluation": {
    "feature_run_id": "feat_2026_05_28_001",
    "verdict": "REJECTED",
    "rejection_code": "RESTRICTION_CONFLICT",
    "rubric_scores": {
      "safety": 2,
      "goal_fit": 4,
      "budget_fit": 5,
      "clarity": 4
    },
    "feedback_for_generator": "Remova WHEY-ISO-001 porque o cliente exige sem lactose e o snapshot marca lactose_free=false.",
    "trace_event": "feature_evaluation_completed"
  }
}
```

### O Ciclo Completo
1. Pipeline identifica que a feature pode ser aplicável.
2. Contract valida se há input suficiente.
3. Generator cria uma proposta estruturada.
4. Evaluator avalia proposta contra contract, constraints e rubric.
5. Se aprovado, pipeline materializa a ação.
6. Se rejeitado, Generator recebe feedback ou a feature se abstém.
7. Trace registra cada decisão com IDs correlacionáveis.
8. State persistence grava somente o estado aprovado e necessário.

### Estados Operacionais da Feature
| Estado | Significado | Ação do Pipeline |
|--------|-------------|------------------|
| `NOT_APPLICABLE` | A feature não deve rodar nesse contexto. | Segue fluxo principal sem chamar Generator. |
| `CANDIDATE` | A feature pode rodar, mas ainda não gerou proposta. | Valida input contract e reserva token budget. |
| `PROPOSED` | Generator criou uma proposta ainda não aprovada. | Chama Evaluator com proposta e evidência. |
| `APPROVED` | Evaluator aprovou e pipeline pode usar output. | Envia mensagem, aplica ação ou persiste update. |
| `REJECTED` | Evaluator rejeitou a proposta. | Esconde proposta do cliente e registra feedback. |
| `DEFERRED` | A feature é útil, mas deve esperar momento melhor. | Agenda rechecagem após mudança de jornada. |
| `HUMAN_REVIEW` | Risco exige humano antes de agir. | Escala com trace, evidence e motivo claro. |

### Como a Anatomia Resolve os Três Problemas Fundamentais
- **Context Amnesia:** Contract declara quais fatos precisam vir de state persistence e quais summaries entram na context window.
- **Planning vs. Execution Collapse:** Generator cria proposta e Evaluator valida; planejamento, geração e aprovação não ficam misturados.
- **Self-Evaluation Collapse:** Evaluator independente impede que o Generator aprove seu próprio output convincente, porém errado.

- Checklist de anatomia 01: A feature tem nome, versão e owner claros.
- Checklist de anatomia 02: O input contract lista campos obrigatórios e fontes.
- Checklist de anatomia 03: O output contract é estruturado e tem IDs estáveis.
- Checklist de anatomia 04: As guarantees são testáveis em unit test e trace.
- Checklist de anatomia 05: As constraints protegem segurança e confiança acima de conversão.
- Checklist de anatomia 06: O Generator não envia mensagem final sem aprovação quando há risco.
- Checklist de anatomia 07: O Evaluator tem rubric explícita.
- Checklist de anatomia 08: O trace permite reconstruir a decisão em ordem cronológica.
- Checklist de anatomia 09: A state policy define o que persistir e o que expirar.
- Checklist de anatomia 10: O token budget está documentado e testado.

---

## 📋 Template de Feature Contract
A seguir está um template completo de feature contract para KODA.
Ele é escrito em JSON-like pseudocode para ser fácil de adaptar para TypeScript, Python, JSON Schema ou Pydantic.
O importante não é a sintaxe exata; o importante é que cada campo tenha função operacional clara.

### Template Base
```json
{
  "feature_contract": {
    "feature_name": "koda.feature_name",
    "feature_version": "1.0.0",
    "owner": "koda-commerce-or-growth",
    "business_goal": "Explicar a melhoria real entregue ao cliente e ao negócio.",
    "customer_promise": "Explicar o que o cliente pode confiar que KODA fará.",
    "activation_policy": {
      "when_to_run": [
        "A intenção atual do cliente pede esta capacidade.",
        "O estágio da jornada permite esta intervenção.",
        "Os dados obrigatórios estão frescos e completos."
      ],
      "when_not_to_run": [
        "Cliente demonstrou frustração recente.",
        "Dados obrigatórios estão ausentes ou antigos.",
        "Feature já rodou nesta conversa e foi recusada."
      ]
    },
    "input_contract": {
      "required": [
        "conversation_id",
        "customer_profile",
        "journey_state",
        "catalog_snapshot",
        "latest_customer_intent"
      ],
      "properties": {
        "conversation_id": {"type": "string", "must_be_stable": true},
        "customer_profile": {"type": "object", "source": "state_persistence"},
        "journey_state": {"type": "object", "source": "server_state"},
        "catalog_snapshot": {"type": "object", "source": "fresh_catalog_read"},
        "latest_customer_intent": {"type": "object", "source": "latest_trace_segment"}
      }
    },
    "output_contract": {
      "required": [
        "feature_run_id",
        "status",
        "candidate_action",
        "customer_message_draft",
        "evidence",
        "state_updates"
      ],
      "properties": {
        "feature_run_id": {"type": "string", "format": "stable_unique_id"},
        "status": {"type": "enum", "values": ["PROPOSED", "ABSTAINED"]},
        "candidate_action": {"type": "object", "description": "Ação que pipeline pode executar se aprovada."},
        "customer_message_draft": {"type": "string", "max_whatsapp_lines": 8},
        "evidence": {"type": "array", "description": "Fatos usados para justificar a proposta."},
        "state_updates": {"type": "object", "description": "Mudanças persistidas somente após aprovação."}
      }
    },
    "guarantees": [
      "A feature nunca recomenda produto fora de estoque.",
      "A feature nunca viola restrições alimentares persistidas.",
      "A feature sempre inclui evidence suficiente para o Evaluator auditar.",
      "A feature nunca grava state_updates antes de aprovação."
    ],
    "constraints": [
      "Não pressionar cliente que demonstrou objeção de preço.",
      "Não oferecer item contraindicado por saúde ou restrição dietética.",
      "Não repetir a mesma oferta recusada na mesma conversa.",
      "Não exceder token budget definido para a etapa."
    ],
    "validation_rules": [
      "Validar input antes de chamar Generator.",
      "Validar output antes de chamar Evaluator.",
      "Validar rubric antes de enviar mensagem ao cliente.",
      "Validar state_updates antes de persistir."
    ],
    "evaluation_rubric": {
      "safety": {"weight": 0.30, "minimum": 5},
      "relevance": {"weight": 0.25, "minimum": 4},
      "commercial_fit": {"weight": 0.15, "minimum": 3},
      "conversation_timing": {"weight": 0.15, "minimum": 3},
      "clarity": {"weight": 0.15, "minimum": 4}
    },
    "trace_events": [
      "feature_activation_checked",
      "feature_input_validated",
      "feature_generation_completed",
      "feature_evaluation_completed",
      "feature_output_committed"
    ]
  }
}
```

### Input Contract: Quatro Classes de Fatos
| Classe | Exemplos | Regra KODA |
|--------|----------|------------|
| Fatos permanentes do cliente | Alergias, restrições, preferências duráveis, histórico de compras. | Vêm de state persistence e vencem qualquer palpite do modelo. |
| Fatos transitórios da conversa | Objeções recentes, intenção atual, humor, urgência e canal. | Vêm do trace recente e expiram quando a jornada muda. |
| Fatos comerciais atuais | Preço, estoque, promoções, margem e regras de combo. | Vêm de snapshot fresco e carregam timestamp. |
| Fatos técnicos do pipeline | conversation_id, trace_id, feature_run_id e token budget restante. | Vêm do harness e são obrigatórios para auditoria. |

- Regra de input 01: Se um dado influencia segurança, preço, estoque ou confiança, ele entra no input contract.
- Regra de input 02: Se uma restrição do cliente está persistida, ela tem prioridade sobre intenção momentânea.
- Regra de input 03: Se o catálogo está antigo, a feature abstém em vez de inventar disponibilidade.
- Regra de input 04: Se a intenção atual está ambígua, o Generator deve pedir esclarecimento ou gerar ABSTAINED.
- Regra de input 05: Se o orçamento não foi informado, a feature pode recomendar faixa moderada, mas precisa marcar price_uncertainty.
- Regra de input 06: Se a feature depende de histórico sensível, a mensagem final não deve expor esse histórico sem necessidade.
- Regra de input 07: Se há conflito entre conversa recente e estado persistido, o Evaluator precisa receber ambos.
- Regra de input 08: Se token budget restante é baixo, a feature usa summary aprovado, não histórico bruto.
- Regra de input 09: Se o cliente recusou uma oferta, offer_history precisa estar no input.
- Regra de input 10: Se a feature pode afetar checkout, journey_state.current_stage é obrigatório.

### Output Contract: O Que o Pipeline Pode Esperar
- **`feature_run_id`:** ID único correlacionando Generator, Evaluator, trace e state update.
- **`status`:** PROPOSED, ABSTAINED, REJECTED ou APPROVED dependendo do ponto do fluxo.
- **`candidate_action`:** Ação que o pipeline executaria: recomendar, ofertar, lembrar, escalar ou perguntar.
- **`customer_message_draft`:** Mensagem curta, natural e compatível com WhatsApp.
- **`evidence`:** Lista de fatos usados, com fonte e timestamp quando relevante.
- **`risk_flags`:** Possíveis riscos que o Evaluator deve olhar com cuidado.
- **`state_updates`:** Mudanças persistidas se a feature for aprovada.
- **`next_allowed_actions`:** Próximos passos permitidos para o pipeline.

- Regra de output 01: Todo output que pode chegar ao cliente precisa ser rastreável até evidence concreta.
- Regra de output 02: Todo output que altera estado precisa declarar state_updates separadamente da mensagem.
- Regra de output 03: Todo output com produto precisa carregar SKU, preço, estoque e origem do snapshot.
- Regra de output 04: Todo output com desconto precisa carregar regra comercial aplicada.
- Regra de output 05: Todo output com uncertainty precisa expor uncertainty para o Evaluator.
- Regra de output 06: Todo output aprovado precisa ser idempotente para evitar cobrança ou oferta duplicada.
- Regra de output 07: Todo output rejeitado fica fora da conversa com o cliente.
- Regra de output 08: Todo output de WhatsApp precisa caber em leitura rápida no celular.
- Regra de output 09: Todo output precisa respeitar constraints mesmo quando o Generator achou alternativa persuasiva.
- Regra de output 10: Todo output precisa preservar feature_version para comparar incidentes entre versões.

### Guarantees e Constraints
Guarantees dizem o que sempre será verdade quando a feature aprova um output.
Constraints dizem o que a feature nunca pode fazer, mesmo que pareça útil para conversão.
- Guarantee 1: Garantia de segurança alimentar: restrições persistidas vencem qualquer objetivo comercial.
- Guarantee 2: Garantia de estoque: produto recomendado precisa estar disponível no snapshot usado.
- Guarantee 3: Garantia de preço: valor exibido precisa bater com regra de desconto aplicada.
- Guarantee 4: Garantia de não repetição: oferta recusada não reaparece sem mudança real de contexto.
- Guarantee 5: Garantia de rastreabilidade: toda ação tem trace_id e feature_run_id.
- Guarantee 6: Garantia de linguagem: mensagem final deve soar como ajuda, não pressão.
- Guarantee 7: Garantia de abstinência: se dados críticos faltam, feature não age.
- Guarantee 8: Garantia de state: apenas decisões aprovadas geram state update permanente.
- Constraint 1: Não recomendar suplemento contraindicado por saúde.
- Constraint 2: Não inventar disponibilidade, preço ou benefício clínico.
- Constraint 3: Não prometer entrega sem confirmação do fulfillment pipeline.
- Constraint 4: Não usar histórico sensível em mensagem sem necessidade.
- Constraint 5: Não ultrapassar token budget sem compaction segura.
- Constraint 6: Não esconder incerteza do Evaluator.
- Constraint 7: Não converter uma rejeição do Evaluator em texto suavizado para o cliente.
- Constraint 8: Não transformar silêncio do cliente em consentimento de compra.

### Validation Rules
- Regra de validação 01: Input deve conter conversation_id, customer_id, journey_state e latest_customer_intent.
- Regra de validação 02: Input deve carregar restrições críticas do cliente a partir de state persistence.
- Regra de validação 03: Catálogo deve ter timestamp recente para estoque e preço.
- Regra de validação 04: Generator deve retornar JSON parseável ou status ABSTAINED com razão.
- Regra de validação 05: Output deve ter feature_run_id único.
- Regra de validação 06: Output não pode conter produto sem SKU válido.
- Regra de validação 07: Mensagem não pode exceder oito linhas de WhatsApp para features de venda.
- Regra de validação 08: Evidence deve citar a fonte de cada fato crítico.
- Regra de validação 09: Evaluator deve produzir verdict explícito.
- Regra de validação 10: State update só pode ocorrer depois de verdict APPROVED.
- Regra de validação 11: Offer history deve impedir repetição de proposta recusada.
- Regra de validação 12: Token budget deve reservar espaço para resposta final e feedback de retry.
- Regra de validação 13: Rubric deve ter pesos somando 1.0.
- Regra de validação 14: Rubric deve reprovar automaticamente violações de safety.
- Regra de validação 15: Feature version precisa aparecer nos eventos de trace.

### Exemplo Preenchido: Product Recommendation
Este contrato cobre a feature que recomenda produtos principais para um cliente com intenção de compra.
A feature é crítica porque uma recomendação errada pode gerar devolução, risco de saúde e perda de confiança.
```json
{
  "feature_contract": {
    "feature_name": "koda.product_recommendation",
    "feature_version": "1.0.0",
    "owner": "koda-commerce-core",
    "business_goal": "Ajudar o cliente a escolher o suplemento mais adequado com segurança e confiança.",
    "customer_promise": "KODA só recomenda produtos compatíveis com objetivo, restrições, orçamento e disponibilidade real.",
    "activation_policy": {
      "when_to_run": [
        "latest_customer_intent.category == product_discovery",
        "cliente expressa objetivo como ganho_muscular, emagrecimento, energia ou recuperacao",
        "catalog_snapshot.available_products_count >= 1"
      ],
      "when_not_to_run": [
        "cliente tem restricao de seguranca sem mapeamento no catalogo",
        "cliente esta perguntando sobre reembolso, reclamacao ou suporte",
        "stock freshness is older than accepted_inventory_ttl"
      ]
    },
    "input_contract": {
      "required": [
        "conversation_id",
        "customer_profile.restrictions",
        "customer_profile.budget_range",
        "customer_profile.goal",
        "catalog_snapshot.products",
        "journey_state.current_stage"
      ],
      "properties": {
        "customer_profile.restrictions": {"type": "array", "examples": ["sem_lactose", "sem_gluten"]},
        "customer_profile.goal": {"type": "enum", "values": ["ganho_muscular", "emagrecimento", "energia", "recuperacao"]},
        "catalog_snapshot.products": {"type": "array", "min_items": 1},
        "journey_state.current_stage": {"type": "enum", "values": ["descoberta", "comparacao", "decisao"]}
      }
    },
    "output_contract": {
      "required": ["feature_run_id", "status", "recommended_products", "customer_message_draft", "evidence", "risk_flags"],
      "properties": {
        "recommended_products": {
          "type": "array",
          "min_items": 1,
          "max_items": 3,
          "item_required": ["sku", "name", "price", "why_this_customer", "restriction_checks"]
        },
        "customer_message_draft": {"type": "string", "tone": "consultivo e direto"},
        "risk_flags": {"type": "array", "allowed": ["restriction_sensitive", "price_sensitive", "stock_low"]}
      }
    },
    "guarantees": [
      "Nenhum produto recomendado viola customer_profile.restrictions.",
      "Todo produto recomendado existe no catalog_snapshot usado.",
      "Todo preço exibido vem do mesmo snapshot avaliado.",
      "A recomendação explica por que o produto combina com o objetivo do cliente."
    ],
    "constraints": [
      "Não recomendar produto fora do orçamento sem explicar alternativa.",
      "Não usar alegações médicas não autorizadas.",
      "Não recomendar mais de 3 produtos na primeira resposta para evitar overload."
    ],
    "evaluation_rubric": {
      "safety": {"weight": 0.35, "minimum_score": 5},
      "goal_fit": {"weight": 0.25, "minimum_score": 4},
      "budget_fit": {"weight": 0.15, "minimum_score": 3},
      "clarity": {"weight": 0.15, "minimum_score": 4},
      "choice_quality": {"weight": 0.10, "minimum_score": 4}
    }
  }
}
```

#### Product Recommendation: Deep Dive Operacional
- **Entrada crítica:** restrições alimentares e objetivo do cliente precisam vir de state persistence, não da memória do chat.
- **Snapshot crítico:** preço e estoque precisam vir do mesmo catalog_snapshot para evitar recomendar item que mudou durante a conversa.
- **Evidence crítica:** cada produto precisa explicar por que combina com objetivo, orçamento e restrições.
- **Rubric crítica:** safety reprova automaticamente; goal_fit diferencia “produto válido” de “produto bom”.
- **Trace crítico:** feature_run_id conecta recomendação, avaliação e mensagem enviada.

### Exemplo Preenchido: Upsell
Este contrato cobre a feature que sugere um complemento, como creatina, coqueteleira ou combo de recuperação.
Upsell é delicado porque pode aumentar receita ou destruir confiança.
O contrato precisa proteger timing, relevância e tom.
```json
{
  "feature_contract": {
    "feature_name": "koda.contextual_upsell",
    "feature_version": "1.0.0",
    "owner": "koda-growth",
    "business_goal": "Aumentar valor do pedido oferecendo complementos realmente úteis.",
    "customer_promise": "KODA só sugere complemento quando ele melhora o resultado do cliente e respeita o momento da conversa.",
    "activation_policy": {
      "when_to_run": [
        "cliente aceitou ou considerou fortemente um produto principal",
        "journey_state.current_stage in [decisao, checkout_pre_confirmation]",
        "existe ao menos um add_on compativel em estoque"
      ],
      "when_not_to_run": [
        "cliente expressou objecao de preco nos ultimos 5 turnos",
        "cliente ja recusou upsell nesta conversa",
        "produto principal ainda nao foi selecionado",
        "add_on cria conflito de seguranca ou restricao alimentar"
      ]
    },
    "input_contract": {
      "required": [
        "selected_primary_product",
        "customer_profile.restrictions",
        "customer_profile.price_sensitivity",
        "journey_state.last_objection",
        "catalog_snapshot.add_on_candidates",
        "offer_history"
      ],
      "properties": {
        "selected_primary_product": {"type": "object", "required": ["sku", "category", "price"]},
        "customer_profile.price_sensitivity": {"type": "enum", "values": ["low", "medium", "high", "unknown"]},
        "journey_state.last_objection": {"type": "object", "nullable": true},
        "offer_history": {"type": "array", "description": "Ofertas já feitas e resposta do cliente."}
      }
    },
    "output_contract": {
      "required": ["feature_run_id", "status", "upsell_candidate", "customer_message_draft", "evidence", "state_updates"],
      "properties": {
        "upsell_candidate": {
          "type": "object",
          "required": ["sku", "name", "price", "relation_to_primary_product", "why_now"]
        },
        "customer_message_draft": {"type": "string", "max_whatsapp_lines": 4},
        "state_updates": {"type": "object", "required": ["offer_history_append"]}
      }
    },
    "guarantees": [
      "A feature não roda depois de objeção de preço recente.",
      "A feature não repete o mesmo upsell recusado.",
      "O complemento tem relação clara com o produto principal.",
      "O complemento está em estoque e tem preço atual."
    ],
    "constraints": [
      "Não usar linguagem de pressão como ultima chance sem campanha real.",
      "Não sugerir suplemento com contraindicação conhecida.",
      "Não atrasar checkout para insistir em upsell.",
      "Não apresentar mais de uma sugestão de upsell por turno."
    ],
    "evaluation_rubric": {
      "timing": {"weight": 0.25, "minimum_score": 4},
      "relevance": {"weight": 0.25, "minimum_score": 4},
      "trust_preservation": {"weight": 0.25, "minimum_score": 5},
      "commercial_value": {"weight": 0.15, "minimum_score": 3},
      "message_clarity": {"weight": 0.10, "minimum_score": 4}
    }
  }
}
```

#### Upsell: Deep Dive Operacional
- **Timing:** o cliente precisa estar perto de decisão, não no meio de objeção.
- **Relevância:** o complemento precisa melhorar uso do produto principal, não apenas aumentar carrinho.
- **Confiança:** a mensagem deve dar opção simples de recusar sem culpa.
- **Estado:** offer_history precisa registrar oferta feita, resposta do cliente e motivo de rejeição.
- **Fallback:** quando timing falha, a feature deve DEFERRED, não REJECTED, porque pode rodar depois.

### Micro-Checklist para Revisar um Feature Contract
- Revisão 01: Nome, versão e owner aparecem em contrato, trace e dashboard.
- Revisão 02: Input contract declara fontes, não apenas nomes de campos.
- Revisão 03: Output contract separa mensagem, ação e state update.
- Revisão 04: Guarantees são verificáveis em testes automatizados.
- Revisão 05: Constraints protegem cliente antes de proteger conversão.
- Revisão 06: Rubric tem pesos, mínimos e decisão de reprovação clara.
- Revisão 07: Trace events permitem replay da decisão.
- Revisão 08: Token budget reserva espaço para Evaluator e retry.
- Revisão 09: State policy define expiração de dados temporários.
- Revisão 10: Feature sabe abstêr quando falta dado crítico.

---

## 🔗 Integração com Pipeline Existente
Uma feature KODA não vive sozinha.
Ela entra em um pipeline que já parseia intenção, consulta estado, busca catálogo, calcula preço, avalia qualidade, envia WhatsApp e persiste decisões.
A integração correta evita três classes de incidente: feature rodando no momento errado, feature usando dados antigos e feature gravando estado que ninguém consegue explicar.

### Pipeline Base do KODA
```
CLIENTE WHATSAPP
    ↓
INTENT PARSER
    ↓
STATE LOADER  ← lê customer_profile, offer_history, journey_state
    ↓
FEATURE ROUTER ← decide quais features viram candidates
    ↓
FEATURE CONTRACT VALIDATION
    ↓
GENERATOR
    ↓
OUTPUT CONTRACT VALIDATION
    ↓
EVALUATOR + RUBRIC
    ↓
PIPELINE DECISION
    ↓
MESSAGE COMPOSER
    ↓
STATE COMMIT + TRACE COMMIT
    ↓
CLIENTE RECEBE RESPOSTA
```

### Onde a Feature Entra
- **Intent Parser:** classifica a intenção sem decidir a feature final.
- **State Loader:** carrega fatos persistidos que a feature não pode esquecer.
- **Feature Router:** transforma intenção e jornada em lista de candidates.
- **Contract Validation:** bloqueia candidate sem input suficiente.
- **Generator:** gera proposta estruturada dentro do output contract.
- **Output Validation:** bloqueia JSON incompleto antes de avaliação semântica.
- **Evaluator:** aplica guarantees, constraints e rubric.
- **Decision Merger:** resolve conflito entre features aprovadas.
- **Message Composer:** transforma ação aprovada em texto WhatsApp sem perder evidence.
- **State Commit:** persiste somente decisões aprovadas e trace correlacionado.

### Feature Router
O Feature Router é a etapa que decide quais features podem tentar atuar em uma conversa.
Ele não deve chamar diretamente o Generator sem passar pelo contract.
Ele deve produzir uma lista pequena de candidates, porque chamar features demais desperdiça token budget e aumenta conflito.
```json
{
  "feature_candidates": [
    {
      "feature_name": "koda.product_recommendation",
      "reason": "cliente pediu sugestao de suplemento",
      "priority": 90
    },
    {
      "feature_name": "koda.contextual_upsell",
      "reason": "produto principal selecionado e cliente sem objecao recente",
      "priority": 50
    }
  ],
  "router_trace_event": "feature_activation_checked"
}
```

### Decision Merger
Quando múltiplas features aprovam ações, KODA precisa decidir o que vai para o cliente agora.
Sem Decision Merger, Product Recommendation e Upsell podem competir no mesmo turno.
A regra é: uma resposta de WhatsApp deve parecer uma conversa humana, não um relatório de features.

- Regra de merge 01: Safety overrides sempre vencem growth actions.
- Regra de merge 02: Suporte e reclamação vencem venda.
- Regra de merge 03: Checkout confirmation vence upsell quando cliente já demonstrou decisão.
- Regra de merge 04: Uma mensagem deve carregar no máximo uma ação comercial primária.
- Regra de merge 05: Features aprovadas, mas não usadas, devem virar DEFERRED com motivo no trace.
- Regra de merge 06: Features com mesma prioridade usam journey_stage para desempate.
- Regra de merge 07: Feature que exigiu HUMAN_REVIEW bloqueia ações irreversíveis.
- Regra de merge 08: Feature que usa estado antigo perde para feature com snapshot fresco.

### Integração com State Persistence
- **customer_profile:** restrições, preferências duráveis, histórico e consentimentos.
- **journey_state:** fase atual, intenção dominante, últimas objeções e próximo passo esperado.
- **offer_history:** ofertas feitas, recusas, aceitações, timestamp e feature_version.
- **feature_memory:** resumos compactados de decisões aprovadas que precisam sobreviver à compaction.
- **risk_register:** marcadores de segurança, saúde, preço e fulfillment que exigem cuidado.

### Integração com Token Budget
Feature nova sempre disputa context window com histórico, estado, catálogo, rubrics e resposta final.
Por isso, cada feature precisa ter orçamento explícito.
```json
{
  "token_budget_policy": {
    "feature_name": "koda.product_recommendation",
    "max_input_tokens": 4500,
    "max_generator_output_tokens": 900,
    "max_evaluator_tokens": 1100,
    "reserved_customer_response_tokens": 500,
    "compaction_strategy": "usar customer_profile_summary + catalog_top_candidates"
  }
}
```

### Trace de Integração
- **`feature_activation_checked`:** Router decidiu se a feature era candidata.
- **`feature_input_validated`:** Contract confirmou input suficiente.
- **`feature_generation_started`:** Generator começou com token budget reservado.
- **`feature_generation_completed`:** Generator escreveu proposta e evidence.
- **`feature_output_validated`:** Output contract passou antes do Evaluator.
- **`feature_evaluation_completed`:** Evaluator escreveu verdict e scores.
- **`feature_merge_decided`:** Decision Merger escolheu ação final.
- **`feature_state_committed`:** State update aprovado foi persistido.
- **`feature_message_sent`:** Mensagem final foi enviada ao cliente.

### Falhas de Integração Mais Comuns
- **Feature roda cedo demais:** Router ignora journey_state e ativa upsell no começo da descoberta.
- **Feature usa dado antigo:** Catalog snapshot não tem freshness check e preço muda antes do envio.
- **Feature duplica mensagem:** Message Composer recebe duas ações comerciais e concatena as duas.
- **Feature grava antes da aprovação:** State update acontece logo após Generator e permanece mesmo com Evaluator rejeitando.
- **Feature perde rastreabilidade:** Output não tem feature_run_id e trace não conecta geração com resposta final.
- **Feature consome token budget demais:** Generator recebe catálogo inteiro em vez de candidatos filtrados.
- **Feature conflita com suporte:** Cliente reclama de entrega, mas Growth feature tenta vender combo.

---

## 🧪 Testes e Validação de Nova Feature
Testing de feature KODA não é apenas verificar se uma função retorna JSON.
Você precisa provar que a feature respeita contrato, integra com pipeline, funciona na jornada e mantém qualidade sob avaliação.
Use quatro camadas: unit tests, integration tests, acceptance criteria e evaluation rubrics.

### Camada 1: Unit Tests de Contract
Unit tests validam regras pequenas e determinísticas.
- **`input_required_fields`:** falha quando conversation_id, customer_profile ou catalog_snapshot estão ausentes.
- **`restriction_source`:** falha quando restrições críticas vêm apenas da mensagem e não de state persistence.
- **`output_has_feature_run_id`:** falha quando proposta não carrega ID correlacionável.
- **`sku_validation`:** falha quando produto recomendado não existe no catalog_snapshot.
- **`price_snapshot_consistency`:** falha quando preço exibido vem de snapshot diferente do avaliado.
- **`state_update_after_approval`:** falha quando state_updates aparecem como commit antes do verdict.
- **`rubric_weights_sum`:** falha quando pesos da rubric não somam 1.0.
- **`message_length`:** falha quando WhatsApp draft excede limite de linhas.
- **`offer_history_block`:** falha quando upsell recusado reaparece sem mudança de contexto.
- **`token_budget_limit`:** falha quando input montado excede max_input_tokens.

#### Exemplo de Unit Test em Pseudocódigo
```json
{
  "test_name": "rejects_product_with_restricted_ingredient",
  "given": {
    "customer_profile": {"restrictions": ["sem_lactose"]},
    "catalog_snapshot": {"products": [{"sku": "WHEY-001", "lactose_free": false}]}
  },
  "when": {
    "generator_output": {"recommended_products": [{"sku": "WHEY-001"}]}
  },
  "then": {
    "evaluator_verdict": "REJECTED",
    "rejection_code": "RESTRICTION_CONFLICT"
  }
}
```

### Camada 2: Integration Tests com Pipeline
Integration tests validam se a feature conversa corretamente com Router, State Loader, Generator, Evaluator, Message Composer e State Commit.
- **`router_to_contract`:** Router ativa Product Recommendation apenas quando intenção é product_discovery.
- **`contract_to_generator`:** Generator só recebe input validado e token budget reservado.
- **`generator_to_evaluator`:** Evaluator recebe output completo, evidence e versão do contract.
- **`evaluator_to_merger`:** Decision Merger recebe verdict e não usa proposta rejeitada.
- **`merger_to_message`:** Message Composer gera uma resposta natural com uma ação principal.
- **`message_to_state`:** State Commit persiste apenas decisões aprovadas.
- **`state_to_next_turn`:** Próximo turno carrega offer_history e não repete oferta recusada.
- **`trace_replay`:** Trace permite reconstruir a decisão de ponta a ponta.

### Camada 3: Acceptance Criteria
Acceptance criteria descrevem o comportamento observável pelo cliente e pelo time de operação.
- Critério de aceite 01: Cliente com restrição sem lactose nunca recebe recomendação com lactose.
- Critério de aceite 02: Cliente que demonstrou objeção de preço não recebe upsell no mesmo bloco de conversa.
- Critério de aceite 03: Cliente recebe no máximo três opções principais na primeira recomendação.
- Critério de aceite 04: Cliente recebe explicação curta do motivo da recomendação.
- Critério de aceite 05: Cliente pode recusar upsell sem sofrer insistência no próximo turno.
- Critério de aceite 06: Produto recomendado está em estoque no momento da resposta.
- Critério de aceite 07: Preço exibido bate com o preço usado pelo Evaluator.
- Critério de aceite 08: Trace da conversa mostra Contract, Generator, Evaluator e Decision Merger.
- Critério de aceite 09: Feature abstém quando dado crítico está ausente.
- Critério de aceite 10: Feature escala para humano quando risco de saúde não é mapeável pelo catálogo.

### Camada 4: Evaluation Rubrics
Rubric avalia qualidade em escala, não apenas validade binária.
| Dimensão | Peso | Mínimo | O que mede | Falha crítica |
|----------|------|--------|------------|---------------|
| Safety | 35% | 5/5 | Compatibilidade com restrições e saúde. | Produto viola restrição persistida. |
| Goal Fit | 20% | 4/5 | Aderência ao objetivo declarado. | Produto não ajuda objetivo principal. |
| Budget Fit | 15% | 3/5 | Respeito ao orçamento e sensibilidade de preço. | Sugestão ignora objeção recente de preço. |
| Timing | 15% | 4/5 | Momento certo na jornada. | Upsell antes de produto principal escolhido. |
| Clarity | 15% | 4/5 | Mensagem curta, honesta e acionável. | Mensagem confusa ou com promessa exagerada. |

#### Rubric Verdict JSON
```json
{
  "rubric_result": {
    "feature_run_id": "feat_2026_05_28_001",
    "dimension_scores": {
      "safety": 5,
      "goal_fit": 4,
      "budget_fit": 4,
      "timing": 5,
      "clarity": 4
    },
    "weighted_score": 4.45,
    "verdict": "APPROVED",
    "notes": "Proposta segura, relevante e adequada ao momento da jornada."
  }
}
```

### Matriz de Testes por Risco
| Risco | Teste mínimo | Teste de regressão | Métrica monitorada |
|-------|--------------|--------------------|--------------------|
| Restrição alimentar | Unit test de restriction conflict. | Cenários sem lactose, sem glúten e alergia a amendoim. | Taxa de violation zero. |
| Preço errado | Snapshot consistency test. | Promoção, cupom, clube e combo. | Diferença entre preço exibido e cobrado. |
| Upsell agressivo | Acceptance test com objeção de preço. | Conversas com frustração, recusa e silêncio. | Reclamações por pressão comercial. |
| Repetição | Offer history unit test. | Recusa seguida de novos turnos. | Ofertas repetidas por conversa. |
| Token budget | Input assembly test. | Conversas longas com catálogo grande. | Taxa de compaction segura. |
| Trace incompleto | Trace replay test. | Falhas em Generator e Evaluator. | Incidentes sem causa rastreável. |

### Banco de Cenários para QA
- Cenário QA 01: **Cliente iniciante sem restrição** — Feature deve recomendar opção simples, explicar preparo e evitar overload.
- Cenário QA 02: **Cliente com intolerância à lactose** — Feature deve filtrar qualquer produto com lactose e mostrar evidence de compatibilidade.
- Cenário QA 03: **Cliente com orçamento baixo** — Feature deve priorizar custo-benefício e evitar upsell imediato.
- Cenário QA 04: **Cliente reclamando de entrega** — Feature comercial deve abstêr e suporte deve vencer no Decision Merger.
- Cenário QA 05: **Cliente aceitou whey premium** — Upsell pode sugerir coqueteleira se timing e preço forem bons.
- Cenário QA 06: **Cliente recusou creatina** — Offer history bloqueia nova oferta de creatina nesta conversa.
- Cenário QA 07: **Catálogo sem estoque** — Product Recommendation abstém ou oferece perguntar quando houver reposição.
- Cenário QA 08: **Snapshot antigo** — Contract Validation falha e força refresh antes de gerar.
- Cenário QA 09: **Restrição de saúde ambígua** — Feature escala para humano em vez de recomendar.
- Cenário QA 10: **Conversa com token budget baixo** — Feature usa summary aprovado e mantém evidence mínima.

### Sinais de Que a Validação Está Boa
- Erros aparecem em staging antes de chegar ao cliente.
- Rejeições do Evaluator são específicas o suficiente para retry útil.
- Trace de falha mostra primeiro módulo culpado em menos de cinco minutos.
- Acceptance tests descrevem experiência do cliente, não apenas estrutura de JSON.
- Rubric reprova casos que humanos também reprovariam.
- Métricas de produção mostram queda de erro silencioso sem aumento absurdo de latência.
---

## 📚 Exemplos Práticos
A melhor forma de aprender Feature Design Patterns é acompanhar features reais do KODA do começo ao fim.
Os exemplos abaixo misturam theory, contract, Generator, Evaluator, trace e decisão de produto.
### Exemplo 1: Product Recommendation para Cliente Iniciante
**Contexto:** Cliente diz: “Comecei academia agora, quero ganhar massa, tenho até R$ 160 e prefiro algo fácil de preparar.”
**Feature:** `koda.product_recommendation`
**Generator:** Gera três opções: whey starter, proteína vegetal e creatina como complemento secundário.
**Evaluator:** Reprova qualquer item fora do orçamento, com preparo complexo ou baixo fit para iniciante.
**Decisão:** Recomenda whey starter como opção principal e menciona creatina apenas como futuro complemento.
**Lição:** Nem toda opção tecnicamente boa é boa para o estágio do cliente.
```json
{
  "example_feature": "koda.product_recommendation",
  "contract_status": "input_validated",
  "generator_status": "proposal_created",
  "evaluator_status": "verdict_recorded",
  "trace_status": "replayable",
  "customer_visible_behavior": "mensagem curta, segura e alinhada ao momento"
}
```

### Exemplo 2: Upsell Sensível a Objeção de Preço
**Contexto:** Cliente escolhe whey de R$ 149, mas disse há dois turnos: “estou tentando gastar pouco este mês”.
**Feature:** `koda.contextual_upsell`
**Generator:** Sugere coqueteleira de R$ 29 como complemento útil.
**Evaluator:** Rejeita por timing porque customer_profile.price_sensitivity está high e last_objection é price.
**Decisão:** Feature fica DEFERRED; KODA segue para checkout sem pressão.
**Lição:** Upsell bom fora de hora vira quebra de confiança.
```json
{
  "example_feature": "koda.contextual_upsell",
  "contract_status": "input_validated",
  "generator_status": "proposal_created",
  "evaluator_status": "verdict_recorded",
  "trace_status": "replayable",
  "customer_visible_behavior": "mensagem curta, segura e alinhada ao momento"
}
```

### Exemplo 3: Reengagement Depois de Carrinho Abandonado
**Contexto:** Cliente montou carrinho, sumiu por 18 horas e voltou perguntando se o produto ainda está disponível.
**Feature:** `koda.cart_reengagement`
**Generator:** Cria mensagem curta confirmando estoque e retomando a decisão anterior.
**Evaluator:** Verifica se preço e estoque mudaram, se a mensagem não soa insistente e se o carrinho ainda é válido.
**Decisão:** Envia resposta: “Ainda está disponível, e posso retomar seu carrinho por aqui se quiser.”
**Lição:** Reengagement precisa ser útil, não perseguição comercial.
```json
{
  "example_feature": "koda.cart_reengagement",
  "contract_status": "input_validated",
  "generator_status": "proposal_created",
  "evaluator_status": "verdict_recorded",
  "trace_status": "replayable",
  "customer_visible_behavior": "mensagem curta, segura e alinhada ao momento"
}
```

### Exemplo 4: Safety Guard em Recomendação Contraindicada
**Contexto:** Cliente menciona orientação médica para evitar estimulantes e pede pré-treino forte.
**Feature:** `koda.safety_guard`
**Generator:** Gera alternativa sem estimulante e sugestão de falar com profissional de saúde.
**Evaluator:** Aprova a recusa segura e bloqueia produtos com cafeína alta.
**Decisão:** KODA explica que não vai recomendar estimulante nesse contexto e oferece alternativa segura.
**Lição:** Às vezes a melhor feature de venda é não vender.
```json
{
  "example_feature": "koda.safety_guard",
  "contract_status": "input_validated",
  "generator_status": "proposal_created",
  "evaluator_status": "verdict_recorded",
  "trace_status": "replayable",
  "customer_visible_behavior": "mensagem curta, segura e alinhada ao momento"
}
```

### 🎬 Simulação de Trace: Product Recommendation
- `14:32:00.000` **intent_parser:** Cliente pede whey para ganhar massa.
- `14:32:00.120` **state_loader:** Carrega restrição sem lactose e budget R$ 160.
- `14:32:00.300` **feature_router:** Ativa koda.product_recommendation com prioridade 90.
- `14:32:00.430` **contract_validation:** Input válido; catálogo fresco há 18 segundos.
- `14:32:01.200` **generator:** Gera três produtos candidatos com evidence.
- `14:32:01.480` **output_validation:** feature_run_id e SKUs válidos.
- `14:32:02.100` **evaluator:** Rejeita WHEY-ISO-002 por lactose; aprova WHEY-VEGAN-010.
- `14:32:02.300` **decision_merger:** Escolhe uma recomendação e adia upsell.
- `14:32:02.500` **message_composer:** Cria resposta WhatsApp com duas linhas principais.
- `14:32:02.650` **state_commit:** Persiste recommendation_made e evidence hash.

### Padrões que Aparecem nos Exemplos
- Contract impede dados ausentes de chegarem ao Generator.
- Generator produz proposta, não decisão final.
- Evaluator protege safety, timing e qualidade.
- Sprint Contract mantém módulos vizinhos alinhados.
- Rubric transforma “parece bom” em score auditável.
- Trace Reading permite explicar cada decisão depois.
- State persistence impede repetição e esquecimento.
- Token budget força summaries enxutos em conversas longas.
---

## 🏗️ Diagrama de Arquitetura
O diagrama abaixo mostra onde uma feature nova entra no pipeline KODA e como Contract, Generator e Evaluator se conectam.
```
┌──────────────────────────────────────────────────────────────────────────────┐
│                           CLIENTE NO WHATSAPP                               │
└────────────────────────────────────┬─────────────────────────────────────────┘
                                     │
                                     ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ INTENT PARSER                                                                │
│ Extrai intenção atual, urgência, objeções e sinais de jornada                │
└────────────────────────────────────┬─────────────────────────────────────────┘
                                     │
                                     ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ STATE LOADER                                                                 │
│ customer_profile + journey_state + offer_history + risk_register             │
└────────────────────────────────────┬─────────────────────────────────────────┘
                                     │
                                     ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ FEATURE ROUTER                                                               │
│ Escolhe candidates: product_recommendation, upsell, safety_guard             │
└────────────────────────────────────┬─────────────────────────────────────────┘
                                     │
             ┌───────────────────────┴────────────────────────┐
             │                                                │
             ▼                                                ▼
┌──────────────────────────────┐              ┌──────────────────────────────┐
│ FEATURE CONTRACT             │              │ CATALOG / PRICE / STOCK      │
│ input/output/guarantees      │◄────────────►│ snapshot fresco e auditável  │
│ validation rules             │              │                              │
└──────────────┬───────────────┘              └──────────────────────────────┘
               │
               ▼
┌──────────────────────────────┐
│ GENERATOR                    │
│ Cria proposta estruturada    │
│ Não aprova a si mesmo        │
└──────────────┬───────────────┘
               │ feature_proposal.json
               ▼
┌──────────────────────────────┐
│ OUTPUT CONTRACT VALIDATION   │
│ Verifica formato e evidence  │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ EVALUATOR + RUBRIC           │
│ Safety, relevance, timing    │
│ Verdict: APPROVED/REJECTED   │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ DECISION MERGER              │
│ Resolve conflitos entre      │
│ features aprovadas           │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ MESSAGE COMPOSER             │
│ Transforma ação em WhatsApp  │
│ curto, humano e rastreável   │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ STATE + TRACE COMMIT         │
│ Persiste decisão aprovada    │
│ e eventos para replay        │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ CLIENTE RECEBE RESPOSTA      │
└──────────────────────────────┘
```
Leitura do diagrama: a feature só fala com o cliente depois de contract validation, generation, output validation, evaluation, merge e commit.
Esse caminho parece longo, mas evita o tipo de erro que destrói confiança em segundos.

---

## 📊 Tabela Comparativa
| Estrategia | Quando Usar | Vantagens | Desvantagens | Exemplo KODA |
|------------|-------------|-----------|---------------|--------------|
| Regra determinística simples | Campo e decisão são objetivos. | Baixa latência, baixo custo, fácil testar. | Pouca flexibilidade e fraca para linguagem natural. | Bloquear upsell se last_objection.type == price. |
| Feature Contract isolado | Feature pequena precisa entrar com segurança. | Define input/output e evita surpresa no pipeline. | Não resolve qualidade sem Evaluator robusto. | Validar recomendação de produto antes de gerar texto. |
| Generator/Evaluator | Qualidade importa e erros custam confiança. | Reduz self-evaluation, cria feedback loop e melhora precisão. | Mais tokens, maior latência e mais tracing. | Recomendar whey para cliente com restrições. |
| Sprint Contract entre módulos | Vários módulos encadeados dependem de formato estável. | Debug mais rápido e falha cedo. | Exige manutenção quando contratos evoluem. | Busca entrega produtos para ranking e filtro. |
| Rubric multi-dimensional | Validade não basta; qualidade precisa de score. | Captura nuances como timing, clareza e trust. | Pesos exigem calibração com dados reais. | Avaliar se upsell soa útil ou pressionador. |
| Trace-first design | Feature crítica precisa ser auditável em produção. | Permite replay, RCA e melhoria contínua. | Aumenta volume de logs e disciplina operacional. | Investigar por que produto errado foi recomendado. |
| Multi-agent coordination | Feature exige especialistas paralelos. | Escala análise complexa e reduz gargalo cognitivo. | Coordenação e conflitos ficam mais difíceis. | Fulfillment com estoque, rota e entregador. |
| Human review gate | Risco de saúde, financeiro ou reputacional é alto. | Protege cliente e empresa em zonas cinzas. | Aumenta tempo e custo operacional. | Cliente cita condição médica não mapeada. |

---

## 🚀 Aplicação KODA
Agora vamos transformar o padrão em prática de engenharia para o KODA real.
Imagine que o time quer lançar “Combo Inteligente”, uma feature que recomenda um bundle quando o cliente escolhe um produto principal.
A pergunta ruim seria: “Qual prompt faz KODA vender mais combo?”
A pergunta boa é: “Qual feature contract permite vender combo sem quebrar confiança, safety e jornada?”

### Passo 1: Definir o Escopo
- Combo Inteligente sugere um bundle de no máximo dois itens complementares.
- A feature roda somente depois de produto principal selecionado.
- A feature não roda se houve objeção de preço recente.
- A feature não roda se qualquer complemento conflita com restrição persistida.
- A feature precisa gerar evidence de relação entre principal e complemento.
- A feature precisa registrar oferta em offer_history após aprovação.
- A feature precisa permitir recusa simples sem insistência.
- A feature precisa ser desligável por feature flag.
### Passo 2: Escrever Contract Antes do Generator
Antes de escrever prompt, Fernando pede ao time: “mostrem o input contract”.
Se a equipe não sabe quais campos entram, ainda não entende a feature.
```json
{
  "combo_inteligente_input": {
    "required": [
      "selected_primary_product.sku",
      "selected_primary_product.category",
      "customer_profile.restrictions",
      "customer_profile.price_sensitivity",
      "journey_state.last_objection",
      "catalog_snapshot.compatible_addons",
      "offer_history"
    ]
  }
}
```
### Passo 3: Definir Generator
O Generator não recebe catálogo inteiro.
Ele recebe candidatos filtrados pelo pipeline para respeitar token budget.
Ele deve criar no máximo dois bundles e explicar o trade-off de cada um.
### Passo 4: Definir Evaluator
O Evaluator avalia safety, relevância, timing, clareza e preservação de confiança.
Ele rejeita automaticamente se price_sensitivity é high e last_objection é price.
Ele rejeita automaticamente se o complemento já foi recusado.
### Passo 5: Integrar com Decision Merger
Se Product Recommendation e Combo Inteligente aprovam ações no mesmo turno, Decision Merger decide o que aparece.
Geralmente a recomendação principal aparece agora e o combo fica DEFERRED para o momento de checkout.
### Passo 6: Medir Resultado
- **`attach_rate`:** Percentual de pedidos com complemento aceito.
- **`upsell_complaint_rate`:** Reclamações de pressão comercial por 1000 conversas.
- **`rejection_rate`:** Percentual de propostas rejeitadas pelo Evaluator.
- **`repeat_offer_rate`:** Taxa de repetição indevida de oferta.
- **`incremental_margin`:** Margem incremental sem aumento de churn.
- **`trace_completeness`:** Percentual de decisões com replay completo.
### Playbook de Deploy
1. Rodar contract tests com cenários de restrição, preço e recusa.
2. Rodar integration tests com Decision Merger e State Commit.
3. Executar avaliação offline em conversas históricas anonimizadas.
4. Liberar para 5% das conversas elegíveis com feature flag.
5. Monitorar rejection_rate e upsell_complaint_rate por 48 horas.
6. Aumentar para 25% se métricas ficarem dentro dos limites.
7. Revisar traces de rejeição para calibrar rubric.
8. Expandir gradualmente e documentar decisão em ADR ou decision log.
### Como Fernando Revisaria o PR
- Fernando pergunta: Onde está o feature contract versionado?
- Fernando pergunta: Qual unit test prova que restrição alimentar vence conversão?
- Fernando pergunta: Qual integration test prova que state update só ocorre após APPROVED?
- Fernando pergunta: Qual trace mostra uma oferta rejeitada e não enviada?
- Fernando pergunta: Qual rubric score reprova timing ruim?
- Fernando pergunta: Qual métrica detecta pressão comercial?
- Fernando pergunta: Como desligar a feature sem quebrar o pipeline?
- Fernando pergunta: Como a feature se comporta com token budget baixo?
### Erros que Fernando Não Aceitaria
- Prompt que menciona restrições, mas contract não exige restrições no input.
- Generator escrevendo direto em offer_history antes de avaliação.
- Evaluator com verdict genérico e sem rejection_code.
- Rubric sem mínimo de trust_preservation.
- Trace sem feature_run_id.
- Mensagem de upsell que impede checkout fluido.
- Feature que não abstém quando catálogo está antigo.
- Testes que validam apenas happy path.
### Resultado Esperado
Quando a aplicação está correta, Combo Inteligente aumenta receita sem aumentar sensação de pressão.
O cliente sente que KODA ajudou, não que empurrou produto.
O time consegue abrir trace e explicar por que o combo apareceu, por que não apareceu ou por que foi adiado.
Essa é a diferença entre uma feature de growth comum e uma feature KODA madura.

---

## 🎓 O Que Você Aprendeu
1. Uma feature KODA não é apenas prompt; é Contract, Generator, Evaluator, trace, state e integração.
2. Contract define a promessa verificável da feature para o pipeline.
3. Input contract impede que o Generator adivinhe fatos críticos.
4. Output contract impede que módulos seguintes recebam formatos instáveis.
5. Guarantees dizem o que sempre deve ser verdade quando a feature aprova output.
6. Constraints dizem o que a feature nunca pode fazer, mesmo com pressão de conversão.
7. Generator cria proposta, mas não aprova a própria proposta.
8. Evaluator protege cliente, negócio e pipeline contra outputs convincentes e errados.
9. Rubric mede qualidade em múltiplas dimensões, não apenas validade binária.
10. Trace permite reconstruir decisões quando cliente, suporte ou engenharia questionam comportamento.
11. State persistence impede repetição, esquecimento e conflito entre conversas longas.
12. Token budget precisa ser definido por feature para evitar context window saturada.
13. Feature Router decide candidates, mas Contract decide se a feature pode rodar.
14. Decision Merger evita que várias features falem ao mesmo tempo com o cliente.
15. Upsell precisa de timing e trust_preservation, não apenas relevância comercial.
16. Product Recommendation exige safety como dimensão dominante da rubric.
17. Acceptance criteria devem descrever experiência real do cliente.
18. Unit tests protegem regras de contrato e validações determinísticas.
19. Integration tests provam que a feature atravessa o pipeline sem quebrar estado.
20. Evaluation rubrics ajudam a calibrar qualidade antes e depois do deploy.
21. HUMAN_REVIEW é uma decisão madura quando risco passa do limite automatizável.
22. Feature flag e canary deploy reduzem risco de lançamento.
23. Métricas precisam incluir confiança, reclamação e erro silencioso, não apenas conversão.
24. Feature madura sabe abstêr quando falta dado crítico.
25. Fernando revisaria primeiro contrato, testes, trace e failure modes antes de elogiar a mensagem final.

---

## ❓ Perguntas Frequentes
### P: Toda feature KODA precisa de Generator/Evaluator?
R: Não. Regras determinísticas simples podem ser suficientes quando decisão é objetiva e risco é baixo. Use Generator/Evaluator quando há linguagem natural, múltiplas opções, trade-offs ou custo alto de erro.

### P: Feature Contract é a mesma coisa que Sprint Contract?
R: Não. Feature Contract descreve a promessa de uma capacidade de produto. Sprint Contract descreve a promessa entre etapas ou módulos. Eles se conectam, mas têm escopos diferentes.

### P: Posso começar pelo prompt e escrever o contract depois?
R: Em features críticas, isso inverte a ordem correta. O contract define o espaço seguro de atuação; o prompt é apenas uma implementação possível dentro desse espaço.

### P: O que fazer quando Evaluator rejeita quase tudo?
R: Leia os traces, veja quais dimensões falham e separe três hipóteses: Generator ruim, rubric rígida demais ou input contract incompleto. Ajuste com dados, não com intuição isolada.

### P: Como preservar Portuguese Brazilian e English technical terms?
R: Use português brasileiro para explicação, tom e narrativa. Preserve termos como context window, token budget, harness, Generator, Evaluator, Sprint Contract, rubric, trace, pipeline e feature contract quando eles são conceitos técnicos.

### P: Quando usar HUMAN_REVIEW?
R: Use quando a decisão envolve saúde, risco financeiro alto, dados contraditórios, política comercial ambígua ou qualquer situação em que uma resposta automática errada seria pior que uma demora honesta.

### P: Como saber se a feature está pronta para produção?
R: Ela está pronta quando contract tests passam, integration tests passam, acceptance criteria são demonstráveis, rubrics estão calibradas, traces são replayable e métricas de canary não mostram regressão de confiança.

---

## ✅ Checkpoint
Use este checkpoint como self-assessment antes de desenhar ou revisar uma feature KODA.
- [ ] Consigo explicar a diferença entre feature, prompt e pipeline step.
- [ ] Consigo escrever um feature contract com input contract, output contract, guarantees e validation rules.
- [ ] Consigo explicar por que Generator não deve aprovar a si mesmo.
- [ ] Consigo desenhar um Evaluator com verdict específico e feedback útil.
- [ ] Consigo definir rubric com pesos, mínimos e falhas críticas.
- [ ] Consigo mostrar onde a feature entra no pipeline existente.
- [ ] Consigo identificar quais state updates só ocorrem após APPROVED.
- [ ] Consigo planejar unit tests para regras determinísticas.
- [ ] Consigo planejar integration tests de ponta a ponta.
- [ ] Consigo escrever acceptance criteria observáveis pelo cliente.
- [ ] Consigo ler um trace e identificar falha de Contract, Generator, Evaluator ou Merge.
- [ ] Consigo decidir quando usar DEFERRED em vez de REJECTED.
- [ ] Consigo proteger token budget sem remover evidence crítica.
- [ ] Consigo explicar como a feature preserva confiança, não apenas conversão.
- [ ] Consigo revisar uma feature nova como Fernando revisaria.

Se marcou menos de 12 itens, volte às seções de Anatomia, Feature Contract Template e Testing.
Se marcou 12 ou mais, você já tem base para participar de design review de features KODA.
Se marcou tudo, você está pronto para liderar a criação de um padrão interno de feature design.

---

## 🔗 Próximos Passos
### Próximo Arquivo: `04-evaluation-rubrics-koda.md`
Agora que você sabe desenhar features, o próximo passo é aprofundar rubrics específicas do KODA.
Você vai aprender a calibrar safety, relevance, trust_preservation, commercial_fit e conversation_timing com exemplos de produção.

### Aplicação Prática Imediata
1. Escolha uma feature atual do KODA que gera dúvida ou incidente.
2. Escreva o feature contract antes de mexer em prompt.
3. Mapeie input sources e state updates.
4. Escreva pelo menos cinco unit tests de contract.
5. Escreva dois integration tests atravessando pipeline completo.
6. Defina rubric inicial com pesos e mínimos.
7. Rode avaliação offline em conversas históricas.
8. Faça review com alguém que não participou do design.
9. Libere com feature flag e canary pequeno.
10. Revise traces de rejeição antes de aumentar rollout.

### Leituras Recomendadas no Programa
- `01-nivel-1-fundamentals/01-why-agents-lose-plot.md` para revisitar os problemas fundamentais.
- `02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md` para reforçar separação de criação e avaliação.
- `02-nivel-2-practical-patterns/02-sprint-contracts.md` para aprofundar contratos entre módulos.
- `02-nivel-2-practical-patterns/03-rubric-design.md` para calibragem de qualidade.
- `03-nivel-3-advanced-architecture/02-state-persistence.md` para persistência de decisões.
- `03-nivel-3-advanced-architecture/03-file-based-coordination.md` para artefatos auditáveis.

---

## 💭 Reflexão Final
Fernando costuma dizer que a diferença entre um agente impressionante e um agente confiável aparece quando a conversa fica longa.
No começo, quase qualquer demo parece inteligente.
Depois de cinquenta mensagens, o sistema começa a revelar sua arquitetura real.
Ele lembra ou esquece?
Ele separa geração de avaliação ou racionaliza os próprios erros?
Ele respeita contratos ou improvisa formatos?
Ele deixa trace ou obriga engenharia a adivinhar?
Feature Design Patterns são a resposta disciplinada a essas perguntas.
Eles tiram KODA do território da esperança e colocam no território da engenharia.
Uma feature desenhada assim pode errar, mas erra de forma rastreável.
Pode ser rejeitada, mas rejeita antes de machucar a confiança do cliente.
Pode evoluir, mas evolui sem quebrar o pipeline inteiro.
Esse é o tipo de maturidade que transforma um agente de vendas em um sistema operacional de relacionamento.
E esse é o tipo de engenharia que Fernando espera de um time que trabalha com long-running agents.
Não desenhe apenas a resposta bonita.
Desenhe a promessa, a geração, a avaliação, o trace e o aprendizado.
Quando fizer isso, KODA não vai apenas vender melhor.
KODA vai merecer confiança.

---

---

### Aprofundamento: Design de Contracts para Features Complexas
Nem toda feature é independente. Algumas features precisam coordenar múltiplos passos — como um checkout completo que envolve validação de estoque, cálculo de frete, aplicação de desconto e processamento de pagamento. Para esses casos, o contrato precisa evoluir.

#### Contratos com Dependências

Quando uma feature depende do output de outra, o contrato deve declarar explicitamente:

```json
{
  "feature_contract": {
    "feature_name": "checkout_completo",
    "dependencies": {
      "requires": [
        {"feature": "product_recommendation", "output_field": "recommendations", "min_version": "2.3.0"},
        {"feature": "customer_context_loader", "output_field": "customer_context", "min_version": "1.0.0"}
      ],
      "optional": [
        {"feature": "upsell", "output_field": "suggestions"}
      ]
    }
  }
}
```

Isso permite que o Feature Router valide não apenas o input da feature atual, mas também que todas as dependências foram satisfeitas antes da execução.

#### Contratos com Timeouts e Degradação

Features que dependem de APIs externas precisam de contratos que especifiquem comportamento sob falha:

- **Timeout:** Se o catálogo não responder em 2 segundos, usar cache da última hora
- **Degradação:** Se o serviço de frete estiver indisponível, exibir "frete a calcular" em vez de bloquear o checkout
- **Fallback:** Se o Evaluator rejeitar 3 vezes, usar uma regra determinística como fallback

O contrato deve declarar esses modos de operação:

```json
{
  "resilience_contract": {
    "timeout_ms": 2000,
    "degraded_mode": {
      "condition": "catalog_api_timeout",
      "behavior": "use_cached_catalog",
      "max_cache_age_seconds": 3600,
      "client_message": "Estou verificando a disponibilidade mais recente..."
    },
    "fallback_mode": {
      "condition": "evaluator_rejected_3x",
      "behavior": "use_deterministic_rule",
      "rule": "recommend_top_selling_in_category"
    }
  }
}
```

### Catálogo de Decisões de Design para Review Técnico

Quando o time revisa um Feature Contract, estas são as perguntas que Fernando faz:

**Sobre o Input Contract:**
- Todo campo obrigatório tem uma fonte de dados conhecida que existe em produção?
- Campos opcionais têm defaults seguros ou a feature trata ausência explicitamente?
- Dados sensíveis (saúde, financeiro) têm validação extra de frescor?
- O input contract é compatível com o output contract do módulo upstream?

**Sobre o Output Contract:**
- Todo campo garantido como "never_null" realmente nunca pode ser null?
- O formato do output é consumível pelo próximo módulo sem adaptação?
- Métricas de latência e token budget são realistas para o modelo em uso?
- O output inclui metadados suficientes para tracing (timestamp, version, generator_id)?

**Sobre o Evaluator e Rubric:**
- A dimensão de safety tem peso suficiente para bloquear recomendações perigosas?
- O threshold de aprovação foi calibrado com dados reais ou é um número arbitrário?
- Os códigos de rejeição são específicos o bastante para o Generator aprender com eles?
- Existe um caso documentado onde HUMAN_REVIEW é a resposta correta?

**Sobre Integração:**
- A feature modifica estado persistente? Se sim, apenas após APPROVED?
- A feature concorre com outras features pelo mesmo recurso (ex: token budget)?
- O trace cobre o ciclo completo: input → generator → evaluator → verdict?
- O rollback é possível sem corromper o estado de outras features?

### Anti-Patterns que Quebram Features KODA

Em produção, o time KODA já encontrou estes anti-patterns repetidamente. Evite-os:

**Anti-Pattern 1: Contract After Code**
O desenvolvedor implementa a feature inteira e só depois escreve o contrato — adaptando o contrato para justificar o que já foi feito. Resultado: contrato não protege nada, apenas documenta o que já existe.

**Correção:** Escreva o contrato primeiro. Revise com o time. Só então implemente.

**Anti-Pattern 2: Evaluator Que Sempre Aprova**
O Evaluator foi escrito pelo mesmo desenvolvedor que escreveu o Generator. Ele "confia" no Generator e aprova 99% dos outputs. Resultado: sycophancy por procuração.

**Correção:** O Evaluator deve ser escrito ou revisado por alguém que NÃO implementou o Generator. Ou use um rubric com dimensões objetivas que forçam verificação.

**Anti-Pattern 3: Feature Monolítica**
Uma única feature faz recomendação, upsell, aplica desconto E agenda follow-up. Resultado: impossível testar, impossível debugar, impossível desligar parcialmente.

**Correção:** Uma feature = uma responsabilidade. Se precisa de 4 capacidades, crie 4 features com contratos independentes.

**Anti-Pattern 4: Contrato Implícito**
"O módulo de recomendação sempre retorna entre 1 e 5 produtos" — mas isso não está escrito em lugar nenhum. Um dia, alguém muda e retorna 10. O pipeline quebra silenciosamente.

**Correção:** Toda expectativa entre módulos deve ser um contrato explícito, versionado e validado.

**Anti-Pattern 5: Testes Só do Happy Path**
Os testes cobrem apenas o cenário ideal: cliente com orçamento folgado, sem restrições, catálogo cheio. Primeiro cliente real com restrição de lactose quebra tudo.

**Correção:** Os test_scenarios no contrato devem incluir: happy path, edge cases, falhas de dependência, dados ausentes, e o pior cenário razoável.

**Anti-Pattern 6: Métrica Única de Sucesso**
"O sucesso da feature é medido por taxa de conversão." Resultado: feature otimiza para vender a qualquer custo, inclusive recomendando produtos inadequados.

**Correção:** Toda feature deve ter métricas balanceadas: conversão, satisfação, reclamação, taxa de devolução e trust_score.

**Anti-Pattern 7: Deploy sem Shadow Mode**
Feature nova vai direto para produção com clientes reais. Primeiro bug acontece com um cliente VIP.

**Correção:** Shadow mode por 24-48h. Feature executa, gera traces, mas output não chega ao cliente. Só ative após métricas estáveis.

### Casos de Borda que Todo Feature Contract Deve Cobrir

Antes de aprovar um Feature Contract para produção, verifique se estes cenários estão cobertos:

**Cenário 1: Cliente Muda de Ideia no Meio da Conversa**
Cliente começa pedindo whey, depois decide que quer vegan, depois pergunta sobre preço. O estado da feature deve refletir a intenção MAIS RECENTE, não a primeira.

**Cenário 2: Dados de Catálogo Desatualizados**
O Generator recomenda um produto que estava em estoque há 10 minutos, mas agora está esgotado. O Evaluator deve verificar estoque EM TEMPO REAL, não confiar no cache do Generator.

**Cenário 3: Restrição Não Documentada**
Cliente nunca disse que é alérgico, mas o histórico de compras mostra que só compra produtos sem glúten. A feature deve inferir restrições implícitas? (Resposta: apenas se o contract explicitamente permitir inferência com confidence threshold.)

**Cenário 4: Duas Features Conflitantes**
Upsell sugere um produto, mas Safety Guard detecta que o cliente mencionou uma condição médica que contraindica esse produto. O Decision Merger deve priorizar Safety Guard sobre Upsell — e o contrato de Upsell deve declarar que respeita veto de Safety.

**Cenário 5: Token Budget Estourado**
A conversa já consumiu 80% da context window. A feature deve ser capaz de operar em modo reduzido (ex: 1 recomendação em vez de 5, menos explicação).

**Cenário 6: Cliente Pede para Não Receber Sugestões**
"Para de me oferecer coisas, só quero comprar isso." A feature NÃO deve insistir. Deve registrar a preferência e silenciar por um período configurável.

**Cenário 7: Rollback de Funcionalidade**
Uma feature em produção começa a causar reclamações. O feature flag permite desligá-la em segundos, não em horas. O contrato deve especificar o comportamento do sistema quando a feature é desligada (ex: pipeline pula a feature, sem efeitos colaterais).

### Debugging e Troubleshooting de Features em Produção

Quando uma feature falha em produção, o trace é seu melhor amigo. Mas você precisa saber LER o trace.

#### Anatomia de um Trace de Feature

```
[2026-05-28 14:32:45.100] ROUTER: customer_id=wa_55119..., intent=product_recommendation
[2026-05-28 14:32:45.150] CONTRACT_FEAT-001: input validated ✅
[2026-05-28 14:32:45.200] GENERATOR_FEAT-001: started (model=claude-sonnet-4-6, temp=0.7)
[2026-05-28 14:32:46.800] GENERATOR_FEAT-001: completed (tokens=847, candidates=8)
[2026-05-28 14:32:46.850] CONTRACT_FEAT-001: output schema validated ✅
[2026-05-28 14:32:46.900] EVALUATOR_FEAT-001: started (rubric_version=2.3)
[2026-05-28 14:32:47.600] EVALUATOR_FEAT-001: verdict=REJECTED, score=3.2
[2026-05-28 14:32:47.610] EVALUATOR_FEAT-001: issue=LACTOSE_VIOLATION (rec #1), severity=CRITICAL
[2026-05-28 14:32:47.620] EVALUATOR_FEAT-001: issue=OVER_BUDGET (rec #3), severity=MEDIUM
[2026-05-28 14:32:47.630] FEEDBACK: sent to generator (2 issues)
[2026-05-28 14:32:47.700] GENERATOR_FEAT-001: retry #2 started
[2026-05-28 14:32:48.900] GENERATOR_FEAT-001: completed (tokens=623, candidates=4)
[2026-05-28 14:32:49.500] EVALUATOR_FEAT-001: verdict=APPROVED, score=8.7 ✅
[2026-05-28 14:32:49.510] MERGER: feature output merged into response
```

#### Checklist de Debug

Quando a feature falha, investigue nesta ordem:

1. **O input era válido?** Verifique `CONTRACT_FEAT-xxx: input validated` — se falhou aqui, o problema está no módulo upstream.
2. **O Generator produziu output?** Verifique `GENERATOR_FEAT-xxx: completed` — se não, é falha de API ou timeout.
3. **O output passou na validação de schema?** Verifique `CONTRACT_FEAT-xxx: output schema validated` — se falhou, o Generator não respeitou o contrato.
4. **O Evaluator aprovou ou rejeitou?** Verifique `EVALUATOR_FEAT-xxx: verdict` — se REJECTED, leia as issues.
5. **As issues fazem sentido?** Se o Evaluator rejeitou por um motivo que parece errado, o problema pode estar no rubric (muito severo) ou nos dados do Evaluator (desatualizados).
6. **O retry funcionou?** Se a segunda tentativa foi aprovada, o feedback loop funcionou — mas investigue por que a primeira falhou.
7. **O merger integrou corretamente?** Verifique se o output da feature não conflitou com outras features.

### Workflow de Time para Feature Design

O time KODA desenvolveu um processo que funciona:

#### Semana -2: Discovery
- Product Manager descreve o problema de negócio (não a solução)
- Time de engenharia faz spike técnico: é viável?
- Identificar dependências e riscos

#### Semana -1: Contract Design
- 1-2 engenheiros escrevem o Feature Contract (apenas o JSON, sem código)
- Review com todo o time: contrato faz sentido? Cobrimos edge cases?
- Product Manager valida: os test_scenarios refletem o que o cliente deve experimentar?

#### Semana 1: Implementação
- Generator e Evaluator implementados em paralelo (por devs diferentes, idealmente)
- Testes de contract escritos primeiro (TDD)
- Testes de integração em seguida

#### Semana 2: Shadow + Deploy
- Feature em shadow mode por 48h
- Métricas revisadas diariamente
- Se approval_rate >= 80% e zero CRITICAL issues, ativar para 10% dos clientes (canary)
- Após 72h de canary sem regressão, ativar para 100%

#### Semana 3+: Monitoramento Contínuo
- Dashboard com approval_rate, latency p50/p99, rejection_reasons
- Alerta se approval_rate cair abaixo de 70%
- Retrospectiva após 30 dias: a feature entregou o valor esperado?

### Evolução de Features: Quando Refatorar vs. Reescrever

Features evoluem. Mas COMO evoluem faz diferença:

#### Quando Refatorar (Manter o FEAT-ID)

- O contrato principal não muda (mesmos input/output garantidos)
- A mudança é interna (otimização do Generator, ajuste de rubric)
- Os módulos downstream não precisam ser alterados
- Os testes existentes continuam válidos

Exemplo: Ajustar o peso da dimensão "safety" de 0.25 para 0.30 no rubric.

#### Quando Versionar (Manter FEAT-ID, Incrementar Versão)

- O output contract ganha campos NOVOS (não quebra consumidores existentes)
- Garantias são adicionadas (não removidas)
- Changelog documenta a evolução

Exemplo: Adicionar campo `confidence_interval` ao output, mantendo todos os campos anteriores.

#### Quando Criar Nova Feature (Novo FEAT-ID)

- O input contract muda de forma incompatível
- Uma garantia existente é removida
- O comportamento fundamental da feature muda
- Módulos downstream precisariam ser reescritos

Exemplo: Transformar "Product Recommendation" de recomendação única para recomendação comparativa com explicação de trade-offs.

**Regra de Ouro:** Se você está mudando o que a feature PROMETE, está criando uma feature nova. Se está mudando COMO ela entrega a promessa, está refatorando.

### Playbook de Resposta a Incidentes

Quando uma feature causa um incidente em produção:

1. **Contenção (0-5 min):** Desligar a feature via feature flag. Zero hesitação.
2. **Diagnóstico (5-30 min):** Ler os traces das últimas decisões da feature. Identificar o padrão de falha.
3. **Comunicação (30-60 min):** Reportar ao time: qual feature, qual falha, quantos clientes afetados, ação tomada.
4. **Correção (1-4 horas):** Corrigir o contrato, generator ou evaluator. Testar contra o cenário que causou o incidente.
5. **Reativação Controlada (4-24 horas):** Shadow mode → canary 1% → canary 10% → 100%.
6. **Postmortem (24-72 horas):** Documentar: o que aconteceu, por que não foi detectado antes, o que muda no processo para evitar recorrência.

NUNCA:
- Corrigir em produção sem passar pelo ciclo de teste
- Reativar sem shadow mode
- Culpar o modelo ("a IA alucinou") — se a feature deixou passar, o contrato ou evaluator falhou

### Mini-Glossário Aplicado
- **feature contract:** contrato versionado que define promessa operacional da feature no contexto do KODA.
- **input contract:** estrutura de dados exigida antes de uma feature rodar no contexto do KODA.
- **output contract:** estrutura que o pipeline pode consumir sem surpresa no contexto do KODA.
- **Generator:** componente que cria proposta e expõe evidence no contexto do KODA.
- **Evaluator:** componente que aprova, rejeita ou escala proposta no contexto do KODA.
- **rubric:** sistema de pontuação multi-dimensional para qualidade no contexto do KODA.
- **trace:** registro estruturado para replay de decisão no contexto do KODA.
- **pipeline:** sequência que transforma mensagem em ação segura no contexto do KODA.
- **context window:** limite de tokens processado pelo modelo no contexto do KODA.
- **token budget:** orçamento de tokens para input, generation, evaluation e resposta no contexto do KODA.
- **harness:** estrutura que guia e valida o agente no contexto do KODA.
- **Sprint Contract:** promessa entre módulos durante execução no contexto do KODA.
## 📋 Metadados
| Campo | Valor |
|-------|-------|
| **Arquivo** | 03-feature-design-patterns.md |
| **Nível** | 4 - KODA-Específico |
| **Tempo** | 150-180 minutos |
| **Status** | ✅ Completo |
| **Pré-requisito** | Níveis 1-3 completos |
| **Próximo** | 04-evaluation-rubrics-koda.md |
| **Crítica para** | Implementação segura de novas features KODA |
| **Atualizado** | Maio 2026 |
| **Personagem guia** | Fernando |
| **Conceitos preservados em inglês** | context window, token budget, harness, Generator, Evaluator, Sprint Contract, rubric, trace, pipeline, feature contract |
