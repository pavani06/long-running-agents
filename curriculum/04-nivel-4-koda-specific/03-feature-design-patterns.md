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

### Caderno de Revisão Avançada
As linhas abaixo consolidam decisões de design que aparecem repetidamente quando o time cria features KODA em produção.
Cada item é uma pergunta ou regra que pode ser usada em review técnico real.
- Revisão avançada 01 — **Contract:** verifique se cada campo obrigatório tem fonte explícita e freshness definida.
- Revisão avançada 02 — **Contract:** rejeite contratos que dependem de texto livre quando o pipeline precisa de campo estruturado.
- Revisão avançada 03 — **Contract:** mantenha business_goal curto para evitar feature com objetivo difuso.
- Revisão avançada 04 — **Input:** separe preferência durável de preferência momentânea para evitar recomendações antigas.
- Revisão avançada 05 — **Input:** exija catalog_snapshot fresco quando preço ou estoque aparecerem na mensagem.
- Revisão avançada 06 — **Input:** inclua journey_state para impedir growth action durante suporte.
- Revisão avançada 07 — **Input:** inclua offer_history em qualquer feature que possa repetir sugestão.
- Revisão avançada 08 — **Input:** inclua risk_register quando suplemento, saúde ou restrição alimentar estiverem em jogo.
- Revisão avançada 09 — **Output:** mantenha customer_message_draft separado de candidate_action.
- Revisão avançada 10 — **Output:** inclua evidence com fonte para cada claim comercial.
- Revisão avançada 11 — **Output:** inclua risk_flags mesmo quando Generator acha que está seguro.
- Revisão avançada 12 — **Output:** inclua state_updates propostos, mas não persista antes de approval.
- Revisão avançada 13 — **Generator:** limite candidatos antes de chamar modelo para respeitar token budget.
- Revisão avançada 14 — **Generator:** gere alternativas com trade-offs diferentes, não variações superficiais.
- Revisão avançada 15 — **Generator:** registre incerteza como dado estruturado.
- Revisão avançada 16 — **Generator:** nunca transforme falta de dado em afirmação confiante.
- Revisão avançada 17 — **Evaluator:** trate safety como hard gate, não apenas peso de score.
- Revisão avançada 18 — **Evaluator:** retorne rejection_code estável para métricas e dashboards.
- Revisão avançada 19 — **Evaluator:** escreva feedback acionável para retry.
- Revisão avançada 20 — **Evaluator:** diferencie REJECTED de DEFERRED para não descartar oportunidade boa fora de hora.
- Revisão avançada 21 — **Rubric:** calibre pesos com conversas reais e revisão humana.
- Revisão avançada 22 — **Rubric:** mantenha mínimos por dimensão para evitar média mascarando falha grave.
- Revisão avançada 23 — **Rubric:** revise thresholds quando rejection_rate sobe sem melhora em qualidade.
- Revisão avançada 24 — **Rubric:** registre score e justificativa para permitir auditoria posterior.
- Revisão avançada 25 — **Trace:** grave feature_run_id em cada evento relacionado.
- Revisão avançada 26 — **Trace:** registre input hash para proteger privacidade e manter replay possível.
- Revisão avançada 27 — **Trace:** registre primeiro erro, não apenas erro final.
- Revisão avançada 28 — **Trace:** mantenha timestamps suficientes para debugar latência.
- Revisão avançada 29 — **State:** persista apenas decisões aprovadas e fatos duráveis.
- Revisão avançada 30 — **State:** expire fatos transitórios como objeção momentânea quando a jornada mudar.
### Biblioteca de Cenários de Treino
- Cenário de treino 001: Cliente pede whey barato, mas tem intolerância à lactose. Resultado esperado: Product Recommendation deve escolher produto sem lactose e dentro do orçamento.
- Cenário de treino 002: Cliente quer checkout rápido depois de comparar três marcas. Resultado esperado: Upsell deve ficar DEFERRED para não atrasar decisão.
- Cenário de treino 003: Cliente reclama que entrega anterior atrasou. Resultado esperado: Feature comercial deve ceder lugar para suporte e confiança.
- Cenário de treino 004: Cliente aceita produto premium e pergunta se precisa de mais alguma coisa. Resultado esperado: Upsell pode sugerir complemento relevante com tom consultivo.
- Cenário de treino 005: Cliente cita orientação médica contra estimulantes. Resultado esperado: Safety Guard bloqueia pré-treino estimulante e sugere alternativa segura.
- Cenário de treino 006: Cliente abandona carrinho e volta no dia seguinte. Resultado esperado: Reengagement confirma disponibilidade sem pressão.
- Cenário de treino 007: Cliente usa cupom e clube ao mesmo tempo. Resultado esperado: Feature de desconto valida cumulatividade antes de exibir preço.
- Cenário de treino 008: Cliente troca orçamento no meio da conversa. Resultado esperado: State distingue preferência recente de orçamento antigo.
- Cenário de treino 009: Catálogo fica indisponível por alguns segundos. Resultado esperado: Feature abstém e KODA comunica que vai verificar antes de recomendar.
- Cenário de treino 010: Evaluator rejeita três tentativas seguidas. Resultado esperado: Pipeline escala para humano com trace e rejection codes.
- Cenário de treino 011: Cliente pede whey barato, mas tem intolerância à lactose. Resultado esperado: Product Recommendation deve escolher produto sem lactose e dentro do orçamento.
- Cenário de treino 012: Cliente quer checkout rápido depois de comparar três marcas. Resultado esperado: Upsell deve ficar DEFERRED para não atrasar decisão.
- Cenário de treino 013: Cliente reclama que entrega anterior atrasou. Resultado esperado: Feature comercial deve ceder lugar para suporte e confiança.
- Cenário de treino 014: Cliente aceita produto premium e pergunta se precisa de mais alguma coisa. Resultado esperado: Upsell pode sugerir complemento relevante com tom consultivo.
- Cenário de treino 015: Cliente cita orientação médica contra estimulantes. Resultado esperado: Safety Guard bloqueia pré-treino estimulante e sugere alternativa segura.
- Cenário de treino 016: Cliente abandona carrinho e volta no dia seguinte. Resultado esperado: Reengagement confirma disponibilidade sem pressão.
- Cenário de treino 017: Cliente usa cupom e clube ao mesmo tempo. Resultado esperado: Feature de desconto valida cumulatividade antes de exibir preço.
- Cenário de treino 018: Cliente troca orçamento no meio da conversa. Resultado esperado: State distingue preferência recente de orçamento antigo.
- Cenário de treino 019: Catálogo fica indisponível por alguns segundos. Resultado esperado: Feature abstém e KODA comunica que vai verificar antes de recomendar.
- Cenário de treino 020: Evaluator rejeita três tentativas seguidas. Resultado esperado: Pipeline escala para humano com trace e rejection codes.
- Cenário de treino 021: Cliente pede whey barato, mas tem intolerância à lactose. Resultado esperado: Product Recommendation deve escolher produto sem lactose e dentro do orçamento.
- Cenário de treino 022: Cliente quer checkout rápido depois de comparar três marcas. Resultado esperado: Upsell deve ficar DEFERRED para não atrasar decisão.
- Cenário de treino 023: Cliente reclama que entrega anterior atrasou. Resultado esperado: Feature comercial deve ceder lugar para suporte e confiança.
- Cenário de treino 024: Cliente aceita produto premium e pergunta se precisa de mais alguma coisa. Resultado esperado: Upsell pode sugerir complemento relevante com tom consultivo.
- Cenário de treino 025: Cliente cita orientação médica contra estimulantes. Resultado esperado: Safety Guard bloqueia pré-treino estimulante e sugere alternativa segura.
- Cenário de treino 026: Cliente abandona carrinho e volta no dia seguinte. Resultado esperado: Reengagement confirma disponibilidade sem pressão.
- Cenário de treino 027: Cliente usa cupom e clube ao mesmo tempo. Resultado esperado: Feature de desconto valida cumulatividade antes de exibir preço.
- Cenário de treino 028: Cliente troca orçamento no meio da conversa. Resultado esperado: State distingue preferência recente de orçamento antigo.
- Cenário de treino 029: Catálogo fica indisponível por alguns segundos. Resultado esperado: Feature abstém e KODA comunica que vai verificar antes de recomendar.
- Cenário de treino 030: Evaluator rejeita três tentativas seguidas. Resultado esperado: Pipeline escala para humano com trace e rejection codes.
- Cenário de treino 031: Cliente pede whey barato, mas tem intolerância à lactose. Resultado esperado: Product Recommendation deve escolher produto sem lactose e dentro do orçamento.
- Cenário de treino 032: Cliente quer checkout rápido depois de comparar três marcas. Resultado esperado: Upsell deve ficar DEFERRED para não atrasar decisão.
- Cenário de treino 033: Cliente reclama que entrega anterior atrasou. Resultado esperado: Feature comercial deve ceder lugar para suporte e confiança.
- Cenário de treino 034: Cliente aceita produto premium e pergunta se precisa de mais alguma coisa. Resultado esperado: Upsell pode sugerir complemento relevante com tom consultivo.
- Cenário de treino 035: Cliente cita orientação médica contra estimulantes. Resultado esperado: Safety Guard bloqueia pré-treino estimulante e sugere alternativa segura.
- Cenário de treino 036: Cliente abandona carrinho e volta no dia seguinte. Resultado esperado: Reengagement confirma disponibilidade sem pressão.
- Cenário de treino 037: Cliente usa cupom e clube ao mesmo tempo. Resultado esperado: Feature de desconto valida cumulatividade antes de exibir preço.
- Cenário de treino 038: Cliente troca orçamento no meio da conversa. Resultado esperado: State distingue preferência recente de orçamento antigo.
- Cenário de treino 039: Catálogo fica indisponível por alguns segundos. Resultado esperado: Feature abstém e KODA comunica que vai verificar antes de recomendar.
- Cenário de treino 040: Evaluator rejeita três tentativas seguidas. Resultado esperado: Pipeline escala para humano com trace e rejection codes.
- Cenário de treino 041: Cliente pede whey barato, mas tem intolerância à lactose. Resultado esperado: Product Recommendation deve escolher produto sem lactose e dentro do orçamento.
- Cenário de treino 042: Cliente quer checkout rápido depois de comparar três marcas. Resultado esperado: Upsell deve ficar DEFERRED para não atrasar decisão.
- Cenário de treino 043: Cliente reclama que entrega anterior atrasou. Resultado esperado: Feature comercial deve ceder lugar para suporte e confiança.
- Cenário de treino 044: Cliente aceita produto premium e pergunta se precisa de mais alguma coisa. Resultado esperado: Upsell pode sugerir complemento relevante com tom consultivo.
- Cenário de treino 045: Cliente cita orientação médica contra estimulantes. Resultado esperado: Safety Guard bloqueia pré-treino estimulante e sugere alternativa segura.
- Cenário de treino 046: Cliente abandona carrinho e volta no dia seguinte. Resultado esperado: Reengagement confirma disponibilidade sem pressão.
- Cenário de treino 047: Cliente usa cupom e clube ao mesmo tempo. Resultado esperado: Feature de desconto valida cumulatividade antes de exibir preço.
- Cenário de treino 048: Cliente troca orçamento no meio da conversa. Resultado esperado: State distingue preferência recente de orçamento antigo.
- Cenário de treino 049: Catálogo fica indisponível por alguns segundos. Resultado esperado: Feature abstém e KODA comunica que vai verificar antes de recomendar.
- Cenário de treino 050: Evaluator rejeita três tentativas seguidas. Resultado esperado: Pipeline escala para humano com trace e rejection codes.
- Cenário de treino 051: Cliente pede whey barato, mas tem intolerância à lactose. Resultado esperado: Product Recommendation deve escolher produto sem lactose e dentro do orçamento.
- Cenário de treino 052: Cliente quer checkout rápido depois de comparar três marcas. Resultado esperado: Upsell deve ficar DEFERRED para não atrasar decisão.
- Cenário de treino 053: Cliente reclama que entrega anterior atrasou. Resultado esperado: Feature comercial deve ceder lugar para suporte e confiança.
- Cenário de treino 054: Cliente aceita produto premium e pergunta se precisa de mais alguma coisa. Resultado esperado: Upsell pode sugerir complemento relevante com tom consultivo.
- Cenário de treino 055: Cliente cita orientação médica contra estimulantes. Resultado esperado: Safety Guard bloqueia pré-treino estimulante e sugere alternativa segura.
- Cenário de treino 056: Cliente abandona carrinho e volta no dia seguinte. Resultado esperado: Reengagement confirma disponibilidade sem pressão.
- Cenário de treino 057: Cliente usa cupom e clube ao mesmo tempo. Resultado esperado: Feature de desconto valida cumulatividade antes de exibir preço.
- Cenário de treino 058: Cliente troca orçamento no meio da conversa. Resultado esperado: State distingue preferência recente de orçamento antigo.
- Cenário de treino 059: Catálogo fica indisponível por alguns segundos. Resultado esperado: Feature abstém e KODA comunica que vai verificar antes de recomendar.
- Cenário de treino 060: Evaluator rejeita três tentativas seguidas. Resultado esperado: Pipeline escala para humano com trace e rejection codes.
- Cenário de treino 061: Cliente pede whey barato, mas tem intolerância à lactose. Resultado esperado: Product Recommendation deve escolher produto sem lactose e dentro do orçamento.
- Cenário de treino 062: Cliente quer checkout rápido depois de comparar três marcas. Resultado esperado: Upsell deve ficar DEFERRED para não atrasar decisão.
- Cenário de treino 063: Cliente reclama que entrega anterior atrasou. Resultado esperado: Feature comercial deve ceder lugar para suporte e confiança.
- Cenário de treino 064: Cliente aceita produto premium e pergunta se precisa de mais alguma coisa. Resultado esperado: Upsell pode sugerir complemento relevante com tom consultivo.
- Cenário de treino 065: Cliente cita orientação médica contra estimulantes. Resultado esperado: Safety Guard bloqueia pré-treino estimulante e sugere alternativa segura.
- Cenário de treino 066: Cliente abandona carrinho e volta no dia seguinte. Resultado esperado: Reengagement confirma disponibilidade sem pressão.
- Cenário de treino 067: Cliente usa cupom e clube ao mesmo tempo. Resultado esperado: Feature de desconto valida cumulatividade antes de exibir preço.
- Cenário de treino 068: Cliente troca orçamento no meio da conversa. Resultado esperado: State distingue preferência recente de orçamento antigo.
- Cenário de treino 069: Catálogo fica indisponível por alguns segundos. Resultado esperado: Feature abstém e KODA comunica que vai verificar antes de recomendar.
- Cenário de treino 070: Evaluator rejeita três tentativas seguidas. Resultado esperado: Pipeline escala para humano com trace e rejection codes.
- Cenário de treino 071: Cliente pede whey barato, mas tem intolerância à lactose. Resultado esperado: Product Recommendation deve escolher produto sem lactose e dentro do orçamento.
- Cenário de treino 072: Cliente quer checkout rápido depois de comparar três marcas. Resultado esperado: Upsell deve ficar DEFERRED para não atrasar decisão.
- Cenário de treino 073: Cliente reclama que entrega anterior atrasou. Resultado esperado: Feature comercial deve ceder lugar para suporte e confiança.
- Cenário de treino 074: Cliente aceita produto premium e pergunta se precisa de mais alguma coisa. Resultado esperado: Upsell pode sugerir complemento relevante com tom consultivo.
- Cenário de treino 075: Cliente cita orientação médica contra estimulantes. Resultado esperado: Safety Guard bloqueia pré-treino estimulante e sugere alternativa segura.
- Cenário de treino 076: Cliente abandona carrinho e volta no dia seguinte. Resultado esperado: Reengagement confirma disponibilidade sem pressão.
- Cenário de treino 077: Cliente usa cupom e clube ao mesmo tempo. Resultado esperado: Feature de desconto valida cumulatividade antes de exibir preço.
- Cenário de treino 078: Cliente troca orçamento no meio da conversa. Resultado esperado: State distingue preferência recente de orçamento antigo.
- Cenário de treino 079: Catálogo fica indisponível por alguns segundos. Resultado esperado: Feature abstém e KODA comunica que vai verificar antes de recomendar.
- Cenário de treino 080: Evaluator rejeita três tentativas seguidas. Resultado esperado: Pipeline escala para humano com trace e rejection codes.
- Cenário de treino 081: Cliente pede whey barato, mas tem intolerância à lactose. Resultado esperado: Product Recommendation deve escolher produto sem lactose e dentro do orçamento.
- Cenário de treino 082: Cliente quer checkout rápido depois de comparar três marcas. Resultado esperado: Upsell deve ficar DEFERRED para não atrasar decisão.
- Cenário de treino 083: Cliente reclama que entrega anterior atrasou. Resultado esperado: Feature comercial deve ceder lugar para suporte e confiança.
- Cenário de treino 084: Cliente aceita produto premium e pergunta se precisa de mais alguma coisa. Resultado esperado: Upsell pode sugerir complemento relevante com tom consultivo.
- Cenário de treino 085: Cliente cita orientação médica contra estimulantes. Resultado esperado: Safety Guard bloqueia pré-treino estimulante e sugere alternativa segura.
- Cenário de treino 086: Cliente abandona carrinho e volta no dia seguinte. Resultado esperado: Reengagement confirma disponibilidade sem pressão.
- Cenário de treino 087: Cliente usa cupom e clube ao mesmo tempo. Resultado esperado: Feature de desconto valida cumulatividade antes de exibir preço.
- Cenário de treino 088: Cliente troca orçamento no meio da conversa. Resultado esperado: State distingue preferência recente de orçamento antigo.
- Cenário de treino 089: Catálogo fica indisponível por alguns segundos. Resultado esperado: Feature abstém e KODA comunica que vai verificar antes de recomendar.
- Cenário de treino 090: Evaluator rejeita três tentativas seguidas. Resultado esperado: Pipeline escala para humano com trace e rejection codes.
- Cenário de treino 091: Cliente pede whey barato, mas tem intolerância à lactose. Resultado esperado: Product Recommendation deve escolher produto sem lactose e dentro do orçamento.
- Cenário de treino 092: Cliente quer checkout rápido depois de comparar três marcas. Resultado esperado: Upsell deve ficar DEFERRED para não atrasar decisão.
- Cenário de treino 093: Cliente reclama que entrega anterior atrasou. Resultado esperado: Feature comercial deve ceder lugar para suporte e confiança.
- Cenário de treino 094: Cliente aceita produto premium e pergunta se precisa de mais alguma coisa. Resultado esperado: Upsell pode sugerir complemento relevante com tom consultivo.
- Cenário de treino 095: Cliente cita orientação médica contra estimulantes. Resultado esperado: Safety Guard bloqueia pré-treino estimulante e sugere alternativa segura.
- Cenário de treino 096: Cliente abandona carrinho e volta no dia seguinte. Resultado esperado: Reengagement confirma disponibilidade sem pressão.
- Cenário de treino 097: Cliente usa cupom e clube ao mesmo tempo. Resultado esperado: Feature de desconto valida cumulatividade antes de exibir preço.
- Cenário de treino 098: Cliente troca orçamento no meio da conversa. Resultado esperado: State distingue preferência recente de orçamento antigo.
- Cenário de treino 099: Catálogo fica indisponível por alguns segundos. Resultado esperado: Feature abstém e KODA comunica que vai verificar antes de recomendar.
- Cenário de treino 100: Evaluator rejeita três tentativas seguidas. Resultado esperado: Pipeline escala para humano com trace e rejection codes.
- Cenário de treino 101: Cliente pede whey barato, mas tem intolerância à lactose. Resultado esperado: Product Recommendation deve escolher produto sem lactose e dentro do orçamento.
- Cenário de treino 102: Cliente quer checkout rápido depois de comparar três marcas. Resultado esperado: Upsell deve ficar DEFERRED para não atrasar decisão.
- Cenário de treino 103: Cliente reclama que entrega anterior atrasou. Resultado esperado: Feature comercial deve ceder lugar para suporte e confiança.
- Cenário de treino 104: Cliente aceita produto premium e pergunta se precisa de mais alguma coisa. Resultado esperado: Upsell pode sugerir complemento relevante com tom consultivo.
- Cenário de treino 105: Cliente cita orientação médica contra estimulantes. Resultado esperado: Safety Guard bloqueia pré-treino estimulante e sugere alternativa segura.
- Cenário de treino 106: Cliente abandona carrinho e volta no dia seguinte. Resultado esperado: Reengagement confirma disponibilidade sem pressão.
- Cenário de treino 107: Cliente usa cupom e clube ao mesmo tempo. Resultado esperado: Feature de desconto valida cumulatividade antes de exibir preço.
- Cenário de treino 108: Cliente troca orçamento no meio da conversa. Resultado esperado: State distingue preferência recente de orçamento antigo.
- Cenário de treino 109: Catálogo fica indisponível por alguns segundos. Resultado esperado: Feature abstém e KODA comunica que vai verificar antes de recomendar.
- Cenário de treino 110: Evaluator rejeita três tentativas seguidas. Resultado esperado: Pipeline escala para humano com trace e rejection codes.
- Cenário de treino 111: Cliente pede whey barato, mas tem intolerância à lactose. Resultado esperado: Product Recommendation deve escolher produto sem lactose e dentro do orçamento.
- Cenário de treino 112: Cliente quer checkout rápido depois de comparar três marcas. Resultado esperado: Upsell deve ficar DEFERRED para não atrasar decisão.
- Cenário de treino 113: Cliente reclama que entrega anterior atrasou. Resultado esperado: Feature comercial deve ceder lugar para suporte e confiança.
- Cenário de treino 114: Cliente aceita produto premium e pergunta se precisa de mais alguma coisa. Resultado esperado: Upsell pode sugerir complemento relevante com tom consultivo.
- Cenário de treino 115: Cliente cita orientação médica contra estimulantes. Resultado esperado: Safety Guard bloqueia pré-treino estimulante e sugere alternativa segura.
- Cenário de treino 116: Cliente abandona carrinho e volta no dia seguinte. Resultado esperado: Reengagement confirma disponibilidade sem pressão.
- Cenário de treino 117: Cliente usa cupom e clube ao mesmo tempo. Resultado esperado: Feature de desconto valida cumulatividade antes de exibir preço.
- Cenário de treino 118: Cliente troca orçamento no meio da conversa. Resultado esperado: State distingue preferência recente de orçamento antigo.
- Cenário de treino 119: Catálogo fica indisponível por alguns segundos. Resultado esperado: Feature abstém e KODA comunica que vai verificar antes de recomendar.
- Cenário de treino 120: Evaluator rejeita três tentativas seguidas. Resultado esperado: Pipeline escala para humano com trace e rejection codes.
### Rubrics de Referência por Feature
- Rubric referência 01: **Product Recommendation** usa safety 35%, goal_fit 25%, budget_fit 15%, clarity 15%, choice_quality 10%.
- Rubric referência 02: **Contextual Upsell** usa timing 25%, relevance 25%, trust_preservation 25%, commercial_value 15%, clarity 10%.
- Rubric referência 03: **Cart Reengagement** usa usefulness 30%, timing 25%, freshness 20%, tone 15%, actionability 10%.
- Rubric referência 04: **Safety Guard** usa safety 60%, clarity 20%, escalation_quality 10%, empathy 10%.
- Rubric referência 05: **Discount Explanation** usa price_accuracy 40%, policy_fit 25%, clarity 20%, fairness 15%.
- Rubric referência 06: **Fulfillment Promise** usa eta_accuracy 35%, inventory_confidence 25%, partner_availability 20%, customer_clarity 20%.
- Rubric referência 07: **Product Recommendation** usa safety 35%, goal_fit 25%, budget_fit 15%, clarity 15%, choice_quality 10%.
- Rubric referência 08: **Contextual Upsell** usa timing 25%, relevance 25%, trust_preservation 25%, commercial_value 15%, clarity 10%.
- Rubric referência 09: **Cart Reengagement** usa usefulness 30%, timing 25%, freshness 20%, tone 15%, actionability 10%.
- Rubric referência 10: **Safety Guard** usa safety 60%, clarity 20%, escalation_quality 10%, empathy 10%.
- Rubric referência 11: **Discount Explanation** usa price_accuracy 40%, policy_fit 25%, clarity 20%, fairness 15%.
- Rubric referência 12: **Fulfillment Promise** usa eta_accuracy 35%, inventory_confidence 25%, partner_availability 20%, customer_clarity 20%.
- Rubric referência 13: **Product Recommendation** usa safety 35%, goal_fit 25%, budget_fit 15%, clarity 15%, choice_quality 10%.
- Rubric referência 14: **Contextual Upsell** usa timing 25%, relevance 25%, trust_preservation 25%, commercial_value 15%, clarity 10%.
- Rubric referência 15: **Cart Reengagement** usa usefulness 30%, timing 25%, freshness 20%, tone 15%, actionability 10%.
- Rubric referência 16: **Safety Guard** usa safety 60%, clarity 20%, escalation_quality 10%, empathy 10%.
- Rubric referência 17: **Discount Explanation** usa price_accuracy 40%, policy_fit 25%, clarity 20%, fairness 15%.
- Rubric referência 18: **Fulfillment Promise** usa eta_accuracy 35%, inventory_confidence 25%, partner_availability 20%, customer_clarity 20%.
- Rubric referência 19: **Product Recommendation** usa safety 35%, goal_fit 25%, budget_fit 15%, clarity 15%, choice_quality 10%.
- Rubric referência 20: **Contextual Upsell** usa timing 25%, relevance 25%, trust_preservation 25%, commercial_value 15%, clarity 10%.
- Rubric referência 21: **Cart Reengagement** usa usefulness 30%, timing 25%, freshness 20%, tone 15%, actionability 10%.
- Rubric referência 22: **Safety Guard** usa safety 60%, clarity 20%, escalation_quality 10%, empathy 10%.
- Rubric referência 23: **Discount Explanation** usa price_accuracy 40%, policy_fit 25%, clarity 20%, fairness 15%.
- Rubric referência 24: **Fulfillment Promise** usa eta_accuracy 35%, inventory_confidence 25%, partner_availability 20%, customer_clarity 20%.
- Rubric referência 25: **Product Recommendation** usa safety 35%, goal_fit 25%, budget_fit 15%, clarity 15%, choice_quality 10%.
- Rubric referência 26: **Contextual Upsell** usa timing 25%, relevance 25%, trust_preservation 25%, commercial_value 15%, clarity 10%.
- Rubric referência 27: **Cart Reengagement** usa usefulness 30%, timing 25%, freshness 20%, tone 15%, actionability 10%.
- Rubric referência 28: **Safety Guard** usa safety 60%, clarity 20%, escalation_quality 10%, empathy 10%.
- Rubric referência 29: **Discount Explanation** usa price_accuracy 40%, policy_fit 25%, clarity 20%, fairness 15%.
- Rubric referência 30: **Fulfillment Promise** usa eta_accuracy 35%, inventory_confidence 25%, partner_availability 20%, customer_clarity 20%.
- Rubric referência 31: **Product Recommendation** usa safety 35%, goal_fit 25%, budget_fit 15%, clarity 15%, choice_quality 10%.
- Rubric referência 32: **Contextual Upsell** usa timing 25%, relevance 25%, trust_preservation 25%, commercial_value 15%, clarity 10%.
- Rubric referência 33: **Cart Reengagement** usa usefulness 30%, timing 25%, freshness 20%, tone 15%, actionability 10%.
- Rubric referência 34: **Safety Guard** usa safety 60%, clarity 20%, escalation_quality 10%, empathy 10%.
- Rubric referência 35: **Discount Explanation** usa price_accuracy 40%, policy_fit 25%, clarity 20%, fairness 15%.
- Rubric referência 36: **Fulfillment Promise** usa eta_accuracy 35%, inventory_confidence 25%, partner_availability 20%, customer_clarity 20%.
- Rubric referência 37: **Product Recommendation** usa safety 35%, goal_fit 25%, budget_fit 15%, clarity 15%, choice_quality 10%.
- Rubric referência 38: **Contextual Upsell** usa timing 25%, relevance 25%, trust_preservation 25%, commercial_value 15%, clarity 10%.
- Rubric referência 39: **Cart Reengagement** usa usefulness 30%, timing 25%, freshness 20%, tone 15%, actionability 10%.
- Rubric referência 40: **Safety Guard** usa safety 60%, clarity 20%, escalation_quality 10%, empathy 10%.
- Rubric referência 41: **Discount Explanation** usa price_accuracy 40%, policy_fit 25%, clarity 20%, fairness 15%.
- Rubric referência 42: **Fulfillment Promise** usa eta_accuracy 35%, inventory_confidence 25%, partner_availability 20%, customer_clarity 20%.
- Rubric referência 43: **Product Recommendation** usa safety 35%, goal_fit 25%, budget_fit 15%, clarity 15%, choice_quality 10%.
- Rubric referência 44: **Contextual Upsell** usa timing 25%, relevance 25%, trust_preservation 25%, commercial_value 15%, clarity 10%.
- Rubric referência 45: **Cart Reengagement** usa usefulness 30%, timing 25%, freshness 20%, tone 15%, actionability 10%.
- Rubric referência 46: **Safety Guard** usa safety 60%, clarity 20%, escalation_quality 10%, empathy 10%.
- Rubric referência 47: **Discount Explanation** usa price_accuracy 40%, policy_fit 25%, clarity 20%, fairness 15%.
- Rubric referência 48: **Fulfillment Promise** usa eta_accuracy 35%, inventory_confidence 25%, partner_availability 20%, customer_clarity 20%.
- Rubric referência 49: **Product Recommendation** usa safety 35%, goal_fit 25%, budget_fit 15%, clarity 15%, choice_quality 10%.
- Rubric referência 50: **Contextual Upsell** usa timing 25%, relevance 25%, trust_preservation 25%, commercial_value 15%, clarity 10%.
- Rubric referência 51: **Cart Reengagement** usa usefulness 30%, timing 25%, freshness 20%, tone 15%, actionability 10%.
- Rubric referência 52: **Safety Guard** usa safety 60%, clarity 20%, escalation_quality 10%, empathy 10%.
- Rubric referência 53: **Discount Explanation** usa price_accuracy 40%, policy_fit 25%, clarity 20%, fairness 15%.
- Rubric referência 54: **Fulfillment Promise** usa eta_accuracy 35%, inventory_confidence 25%, partner_availability 20%, customer_clarity 20%.
- Rubric referência 55: **Product Recommendation** usa safety 35%, goal_fit 25%, budget_fit 15%, clarity 15%, choice_quality 10%.
- Rubric referência 56: **Contextual Upsell** usa timing 25%, relevance 25%, trust_preservation 25%, commercial_value 15%, clarity 10%.
- Rubric referência 57: **Cart Reengagement** usa usefulness 30%, timing 25%, freshness 20%, tone 15%, actionability 10%.
- Rubric referência 58: **Safety Guard** usa safety 60%, clarity 20%, escalation_quality 10%, empathy 10%.
- Rubric referência 59: **Discount Explanation** usa price_accuracy 40%, policy_fit 25%, clarity 20%, fairness 15%.
- Rubric referência 60: **Fulfillment Promise** usa eta_accuracy 35%, inventory_confidence 25%, partner_availability 20%, customer_clarity 20%.
### Anti-Patterns que Quebram Features KODA
- Anti-pattern 01: **Prompt-only feature** — parece rápida, mas não tem contract, trace nem state policy.
- Anti-pattern 02: **Evaluator decorativo** — aprova quase tudo e não protege contra self-evaluation collapse.
- Anti-pattern 03: **Contract sem tests** — documenta promessa que ninguém verifica.
- Anti-pattern 04: **State update otimista** — grava ação antes do Evaluator aprovar.
- Anti-pattern 05: **Trace raso** — registra resultado final, mas não registra decisão intermediária.
- Anti-pattern 06: **Rubric média-cega** — média alta esconde falha crítica em safety.
- Anti-pattern 07: **Upsell insistente** — aumenta attach_rate no curto prazo e destrói trust no longo prazo.
- Anti-pattern 08: **Token budget infinito** — copia catálogo inteiro e degrada resposta em conversa longa.
- Anti-pattern 09: **Fallback silencioso** — troca produto rejeitado sem registrar motivo.
- Anti-pattern 10: **Feature sem owner** — ninguém responde quando incidente aparece.
- Anti-pattern 11: **Prompt-only feature** — parece rápida, mas não tem contract, trace nem state policy.
- Anti-pattern 12: **Evaluator decorativo** — aprova quase tudo e não protege contra self-evaluation collapse.
- Anti-pattern 13: **Contract sem tests** — documenta promessa que ninguém verifica.
- Anti-pattern 14: **State update otimista** — grava ação antes do Evaluator aprovar.
- Anti-pattern 15: **Trace raso** — registra resultado final, mas não registra decisão intermediária.
- Anti-pattern 16: **Rubric média-cega** — média alta esconde falha crítica em safety.
- Anti-pattern 17: **Upsell insistente** — aumenta attach_rate no curto prazo e destrói trust no longo prazo.
- Anti-pattern 18: **Token budget infinito** — copia catálogo inteiro e degrada resposta em conversa longa.
- Anti-pattern 19: **Fallback silencioso** — troca produto rejeitado sem registrar motivo.
- Anti-pattern 20: **Feature sem owner** — ninguém responde quando incidente aparece.
- Anti-pattern 21: **Prompt-only feature** — parece rápida, mas não tem contract, trace nem state policy.
- Anti-pattern 22: **Evaluator decorativo** — aprova quase tudo e não protege contra self-evaluation collapse.
- Anti-pattern 23: **Contract sem tests** — documenta promessa que ninguém verifica.
- Anti-pattern 24: **State update otimista** — grava ação antes do Evaluator aprovar.
- Anti-pattern 25: **Trace raso** — registra resultado final, mas não registra decisão intermediária.
- Anti-pattern 26: **Rubric média-cega** — média alta esconde falha crítica em safety.
- Anti-pattern 27: **Upsell insistente** — aumenta attach_rate no curto prazo e destrói trust no longo prazo.
- Anti-pattern 28: **Token budget infinito** — copia catálogo inteiro e degrada resposta em conversa longa.
- Anti-pattern 29: **Fallback silencioso** — troca produto rejeitado sem registrar motivo.
- Anti-pattern 30: **Feature sem owner** — ninguém responde quando incidente aparece.
- Anti-pattern 31: **Prompt-only feature** — parece rápida, mas não tem contract, trace nem state policy.
- Anti-pattern 32: **Evaluator decorativo** — aprova quase tudo e não protege contra self-evaluation collapse.
- Anti-pattern 33: **Contract sem tests** — documenta promessa que ninguém verifica.
- Anti-pattern 34: **State update otimista** — grava ação antes do Evaluator aprovar.
- Anti-pattern 35: **Trace raso** — registra resultado final, mas não registra decisão intermediária.
- Anti-pattern 36: **Rubric média-cega** — média alta esconde falha crítica em safety.
- Anti-pattern 37: **Upsell insistente** — aumenta attach_rate no curto prazo e destrói trust no longo prazo.
- Anti-pattern 38: **Token budget infinito** — copia catálogo inteiro e degrada resposta em conversa longa.
- Anti-pattern 39: **Fallback silencioso** — troca produto rejeitado sem registrar motivo.
- Anti-pattern 40: **Feature sem owner** — ninguém responde quando incidente aparece.
- Anti-pattern 41: **Prompt-only feature** — parece rápida, mas não tem contract, trace nem state policy.
- Anti-pattern 42: **Evaluator decorativo** — aprova quase tudo e não protege contra self-evaluation collapse.
- Anti-pattern 43: **Contract sem tests** — documenta promessa que ninguém verifica.
- Anti-pattern 44: **State update otimista** — grava ação antes do Evaluator aprovar.
- Anti-pattern 45: **Trace raso** — registra resultado final, mas não registra decisão intermediária.
- Anti-pattern 46: **Rubric média-cega** — média alta esconde falha crítica em safety.
- Anti-pattern 47: **Upsell insistente** — aumenta attach_rate no curto prazo e destrói trust no longo prazo.
- Anti-pattern 48: **Token budget infinito** — copia catálogo inteiro e degrada resposta em conversa longa.
- Anti-pattern 49: **Fallback silencioso** — troca produto rejeitado sem registrar motivo.
- Anti-pattern 50: **Feature sem owner** — ninguém responde quando incidente aparece.
- Anti-pattern 51: **Prompt-only feature** — parece rápida, mas não tem contract, trace nem state policy.
- Anti-pattern 52: **Evaluator decorativo** — aprova quase tudo e não protege contra self-evaluation collapse.
- Anti-pattern 53: **Contract sem tests** — documenta promessa que ninguém verifica.
- Anti-pattern 54: **State update otimista** — grava ação antes do Evaluator aprovar.
- Anti-pattern 55: **Trace raso** — registra resultado final, mas não registra decisão intermediária.
- Anti-pattern 56: **Rubric média-cega** — média alta esconde falha crítica em safety.
- Anti-pattern 57: **Upsell insistente** — aumenta attach_rate no curto prazo e destrói trust no longo prazo.
- Anti-pattern 58: **Token budget infinito** — copia catálogo inteiro e degrada resposta em conversa longa.
- Anti-pattern 59: **Fallback silencioso** — troca produto rejeitado sem registrar motivo.
- Anti-pattern 60: **Feature sem owner** — ninguém responde quando incidente aparece.
- Anti-pattern 61: **Prompt-only feature** — parece rápida, mas não tem contract, trace nem state policy.
- Anti-pattern 62: **Evaluator decorativo** — aprova quase tudo e não protege contra self-evaluation collapse.
- Anti-pattern 63: **Contract sem tests** — documenta promessa que ninguém verifica.
- Anti-pattern 64: **State update otimista** — grava ação antes do Evaluator aprovar.
- Anti-pattern 65: **Trace raso** — registra resultado final, mas não registra decisão intermediária.
- Anti-pattern 66: **Rubric média-cega** — média alta esconde falha crítica em safety.
- Anti-pattern 67: **Upsell insistente** — aumenta attach_rate no curto prazo e destrói trust no longo prazo.
- Anti-pattern 68: **Token budget infinito** — copia catálogo inteiro e degrada resposta em conversa longa.
- Anti-pattern 69: **Fallback silencioso** — troca produto rejeitado sem registrar motivo.
- Anti-pattern 70: **Feature sem owner** — ninguém responde quando incidente aparece.
- Anti-pattern 71: **Prompt-only feature** — parece rápida, mas não tem contract, trace nem state policy.
- Anti-pattern 72: **Evaluator decorativo** — aprova quase tudo e não protege contra self-evaluation collapse.
- Anti-pattern 73: **Contract sem tests** — documenta promessa que ninguém verifica.
- Anti-pattern 74: **State update otimista** — grava ação antes do Evaluator aprovar.
- Anti-pattern 75: **Trace raso** — registra resultado final, mas não registra decisão intermediária.
- Anti-pattern 76: **Rubric média-cega** — média alta esconde falha crítica em safety.
- Anti-pattern 77: **Upsell insistente** — aumenta attach_rate no curto prazo e destrói trust no longo prazo.
- Anti-pattern 78: **Token budget infinito** — copia catálogo inteiro e degrada resposta em conversa longa.
- Anti-pattern 79: **Fallback silencioso** — troca produto rejeitado sem registrar motivo.
- Anti-pattern 80: **Feature sem owner** — ninguém responde quando incidente aparece.
- Anti-pattern 81: **Prompt-only feature** — parece rápida, mas não tem contract, trace nem state policy.
- Anti-pattern 82: **Evaluator decorativo** — aprova quase tudo e não protege contra self-evaluation collapse.
- Anti-pattern 83: **Contract sem tests** — documenta promessa que ninguém verifica.
- Anti-pattern 84: **State update otimista** — grava ação antes do Evaluator aprovar.
- Anti-pattern 85: **Trace raso** — registra resultado final, mas não registra decisão intermediária.
- Anti-pattern 86: **Rubric média-cega** — média alta esconde falha crítica em safety.
- Anti-pattern 87: **Upsell insistente** — aumenta attach_rate no curto prazo e destrói trust no longo prazo.
- Anti-pattern 88: **Token budget infinito** — copia catálogo inteiro e degrada resposta em conversa longa.
- Anti-pattern 89: **Fallback silencioso** — troca produto rejeitado sem registrar motivo.
- Anti-pattern 90: **Feature sem owner** — ninguém responde quando incidente aparece.
### Checklist de Readiness para Produção
- Readiness 001: Feature flag criada e documentada.
- Readiness 002: Rollback testado em staging.
- Readiness 003: Dashboard com approval_rate, rejection_rate e complaint_rate.
- Readiness 004: Alertas definidos para violation de safety.
- Readiness 005: Trace replay validado em pelo menos dez conversas simuladas.
- Readiness 006: Rubric revisada por engenharia e produto.
- Readiness 007: Suporte treinado para ler rejection_code básico.
- Readiness 008: Owner definido para incidentes.
- Readiness 009: Canary inicial limitado a público de baixo risco.
- Readiness 010: Decision log atualizado com trade-offs aceitos.
- Readiness 011: Feature flag criada e documentada.
- Readiness 012: Rollback testado em staging.
- Readiness 013: Dashboard com approval_rate, rejection_rate e complaint_rate.
- Readiness 014: Alertas definidos para violation de safety.
- Readiness 015: Trace replay validado em pelo menos dez conversas simuladas.
- Readiness 016: Rubric revisada por engenharia e produto.
- Readiness 017: Suporte treinado para ler rejection_code básico.
- Readiness 018: Owner definido para incidentes.
- Readiness 019: Canary inicial limitado a público de baixo risco.
- Readiness 020: Decision log atualizado com trade-offs aceitos.
- Readiness 021: Feature flag criada e documentada.
- Readiness 022: Rollback testado em staging.
- Readiness 023: Dashboard com approval_rate, rejection_rate e complaint_rate.
- Readiness 024: Alertas definidos para violation de safety.
- Readiness 025: Trace replay validado em pelo menos dez conversas simuladas.
- Readiness 026: Rubric revisada por engenharia e produto.
- Readiness 027: Suporte treinado para ler rejection_code básico.
- Readiness 028: Owner definido para incidentes.
- Readiness 029: Canary inicial limitado a público de baixo risco.
- Readiness 030: Decision log atualizado com trade-offs aceitos.
- Readiness 031: Feature flag criada e documentada.
- Readiness 032: Rollback testado em staging.
- Readiness 033: Dashboard com approval_rate, rejection_rate e complaint_rate.
- Readiness 034: Alertas definidos para violation de safety.
- Readiness 035: Trace replay validado em pelo menos dez conversas simuladas.
- Readiness 036: Rubric revisada por engenharia e produto.
- Readiness 037: Suporte treinado para ler rejection_code básico.
- Readiness 038: Owner definido para incidentes.
- Readiness 039: Canary inicial limitado a público de baixo risco.
- Readiness 040: Decision log atualizado com trade-offs aceitos.
- Readiness 041: Feature flag criada e documentada.
- Readiness 042: Rollback testado em staging.
- Readiness 043: Dashboard com approval_rate, rejection_rate e complaint_rate.
- Readiness 044: Alertas definidos para violation de safety.
- Readiness 045: Trace replay validado em pelo menos dez conversas simuladas.
- Readiness 046: Rubric revisada por engenharia e produto.
- Readiness 047: Suporte treinado para ler rejection_code básico.
- Readiness 048: Owner definido para incidentes.
- Readiness 049: Canary inicial limitado a público de baixo risco.
- Readiness 050: Decision log atualizado com trade-offs aceitos.
- Readiness 051: Feature flag criada e documentada.
- Readiness 052: Rollback testado em staging.
- Readiness 053: Dashboard com approval_rate, rejection_rate e complaint_rate.
- Readiness 054: Alertas definidos para violation de safety.
- Readiness 055: Trace replay validado em pelo menos dez conversas simuladas.
- Readiness 056: Rubric revisada por engenharia e produto.
- Readiness 057: Suporte treinado para ler rejection_code básico.
- Readiness 058: Owner definido para incidentes.
- Readiness 059: Canary inicial limitado a público de baixo risco.
- Readiness 060: Decision log atualizado com trade-offs aceitos.
- Readiness 061: Feature flag criada e documentada.
- Readiness 062: Rollback testado em staging.
- Readiness 063: Dashboard com approval_rate, rejection_rate e complaint_rate.
- Readiness 064: Alertas definidos para violation de safety.
- Readiness 065: Trace replay validado em pelo menos dez conversas simuladas.
- Readiness 066: Rubric revisada por engenharia e produto.
- Readiness 067: Suporte treinado para ler rejection_code básico.
- Readiness 068: Owner definido para incidentes.
- Readiness 069: Canary inicial limitado a público de baixo risco.
- Readiness 070: Decision log atualizado com trade-offs aceitos.
- Readiness 071: Feature flag criada e documentada.
- Readiness 072: Rollback testado em staging.
- Readiness 073: Dashboard com approval_rate, rejection_rate e complaint_rate.
- Readiness 074: Alertas definidos para violation de safety.
- Readiness 075: Trace replay validado em pelo menos dez conversas simuladas.
- Readiness 076: Rubric revisada por engenharia e produto.
- Readiness 077: Suporte treinado para ler rejection_code básico.
- Readiness 078: Owner definido para incidentes.
- Readiness 079: Canary inicial limitado a público de baixo risco.
- Readiness 080: Decision log atualizado com trade-offs aceitos.
- Readiness 081: Feature flag criada e documentada.
- Readiness 082: Rollback testado em staging.
- Readiness 083: Dashboard com approval_rate, rejection_rate e complaint_rate.
- Readiness 084: Alertas definidos para violation de safety.
- Readiness 085: Trace replay validado em pelo menos dez conversas simuladas.
- Readiness 086: Rubric revisada por engenharia e produto.
- Readiness 087: Suporte treinado para ler rejection_code básico.
- Readiness 088: Owner definido para incidentes.
- Readiness 089: Canary inicial limitado a público de baixo risco.
- Readiness 090: Decision log atualizado com trade-offs aceitos.
- Readiness 091: Feature flag criada e documentada.
- Readiness 092: Rollback testado em staging.
- Readiness 093: Dashboard com approval_rate, rejection_rate e complaint_rate.
- Readiness 094: Alertas definidos para violation de safety.
- Readiness 095: Trace replay validado em pelo menos dez conversas simuladas.
- Readiness 096: Rubric revisada por engenharia e produto.
- Readiness 097: Suporte treinado para ler rejection_code básico.
- Readiness 098: Owner definido para incidentes.
- Readiness 099: Canary inicial limitado a público de baixo risco.
- Readiness 100: Decision log atualizado com trade-offs aceitos.
### Mini-Glossário Operacional
- **feature contract:** contrato versionado que define promessa operacional da feature.
- **input contract:** estrutura de dados que a feature exige para rodar sem adivinhar.
- **output contract:** estrutura que a feature promete entregar ao pipeline seguinte.
- **Generator:** componente que cria proposta dentro do contrato.
- **Evaluator:** componente que avalia proposta contra contract, constraints e rubric.
- **rubric:** sistema de pontuação multi-dimensional para qualidade.
- **trace:** registro estruturado de eventos e decisões.
- **pipeline:** sequência de etapas que transforma mensagem do cliente em ação segura.
- **context window:** limite de tokens disponível para o modelo processar de uma vez.
- **token budget:** orçamento explícito de tokens para input, geração, avaliação e resposta.
- **harness:** estrutura de suporte que guia, valida e observa o agente.
- **Sprint Contract:** promessa entre etapas ou módulos em um ciclo de execução.
---

### Catálogo de Decisões de Design para Review Técnico
Esta seção substitui intuição por perguntas concretas que um time pode usar em design review de features KODA.
- Decisão de review 001: **Contract** — confirme que o contrato tem nome, versão, owner e business_goal testável durante descoberta de produto; isso evita restrição alimentar ignorada, porque sem identidade estável, incidentes ficam impossíveis de agrupar.
- Decisão de review 002: **Input contract** — confirme que cada campo obrigatório tem source explícito durante comparação de marcas; isso evita preço desatualizado, porque sem source, o Generator começa a adivinhar.
- Decisão de review 003: **Output contract** — confirme que mensagem, ação e state_updates estão separados durante decisão de compra; isso evita estoque antigo, porque sem separação, proposta rejeitada pode vazar para o cliente.
- Decisão de review 004: **Guarantees** — confirme que cada guarantee pode virar teste ou trace check durante checkout; isso evita upsell agressivo, porque garantia não verificável vira slogan.
- Decisão de review 005: **Constraints** — confirme que constraints de safety vencem objetivos comerciais durante pós-compra; isso evita oferta repetida, porque conversão não compensa quebra de confiança.
- Decisão de review 006: **Generator** — confirme que o Generator não envia resposta final sozinho durante reclamação de entrega; isso evita trace incompleto, porque self-evaluation collapse volta quando geração e aprovação se misturam.
- Decisão de review 007: **Evaluator** — confirme que rejection_code é específico e estável durante reengagement; isso evita state update prematuro, porque sem código, dashboard e retry ficam cegos.
- Decisão de review 008: **Rubric** — confirme que safety tem hard gate quando há restrição crítica durante aplicação de cupom; isso evita rubric leniente, porque média ponderada não pode esconder risco de saúde.
- Decisão de review 009: **Trace** — confirme que feature_run_id aparece em todos os eventos durante pedido com restrição alimentar; isso evita token budget estourado, porque sem correlação, replay vira caça ao tesouro.
- Decisão de review 010: **State** — confirme que apenas APPROVED gera commit durável durante pedido com orçamento apertado; isso evita mensagem confusa, porque estado otimista cria repetição e contradição.
- Decisão de review 011: **Token budget** — confirme que catálogo foi pré-filtrado antes do modelo durante descoberta de produto; isso evita restrição alimentar ignorada, porque catálogo bruto consome context window sem melhorar decisão.
- Decisão de review 012: **Router** — confirme que candidates são poucos e justificados durante comparação de marcas; isso evita preço desatualizado, porque features demais competem por atenção e latência.
- Decisão de review 013: **Decision Merger** — confirme que só uma ação comercial primária chega ao WhatsApp durante decisão de compra; isso evita estoque antigo, porque mensagem com múltiplas vendas parece spam.
- Decisão de review 014: **Message Composer** — confirme que texto final preserva evidence sem expor dados sensíveis durante checkout; isso evita upsell agressivo, porque clareza não pode violar privacidade.
- Decisão de review 015: **Testing** — confirme que há unit, integration, acceptance e evaluation tests durante pós-compra; isso evita oferta repetida, porque uma camada sozinha não cobre feature KODA real.
- Decisão de review 016: **Contract** — confirme que o contrato tem nome, versão, owner e business_goal testável durante reclamação de entrega; isso evita trace incompleto, porque sem identidade estável, incidentes ficam impossíveis de agrupar.
- Decisão de review 017: **Input contract** — confirme que cada campo obrigatório tem source explícito durante reengagement; isso evita state update prematuro, porque sem source, o Generator começa a adivinhar.
- Decisão de review 018: **Output contract** — confirme que mensagem, ação e state_updates estão separados durante aplicação de cupom; isso evita rubric leniente, porque sem separação, proposta rejeitada pode vazar para o cliente.
- Decisão de review 019: **Guarantees** — confirme que cada guarantee pode virar teste ou trace check durante pedido com restrição alimentar; isso evita token budget estourado, porque garantia não verificável vira slogan.
- Decisão de review 020: **Constraints** — confirme que constraints de safety vencem objetivos comerciais durante pedido com orçamento apertado; isso evita mensagem confusa, porque conversão não compensa quebra de confiança.
- Decisão de review 021: **Generator** — confirme que o Generator não envia resposta final sozinho durante descoberta de produto; isso evita restrição alimentar ignorada, porque self-evaluation collapse volta quando geração e aprovação se misturam.
- Decisão de review 022: **Evaluator** — confirme que rejection_code é específico e estável durante comparação de marcas; isso evita preço desatualizado, porque sem código, dashboard e retry ficam cegos.
- Decisão de review 023: **Rubric** — confirme que safety tem hard gate quando há restrição crítica durante decisão de compra; isso evita estoque antigo, porque média ponderada não pode esconder risco de saúde.
- Decisão de review 024: **Trace** — confirme que feature_run_id aparece em todos os eventos durante checkout; isso evita upsell agressivo, porque sem correlação, replay vira caça ao tesouro.
- Decisão de review 025: **State** — confirme que apenas APPROVED gera commit durável durante pós-compra; isso evita oferta repetida, porque estado otimista cria repetição e contradição.
- Decisão de review 026: **Token budget** — confirme que catálogo foi pré-filtrado antes do modelo durante reclamação de entrega; isso evita trace incompleto, porque catálogo bruto consome context window sem melhorar decisão.
- Decisão de review 027: **Router** — confirme que candidates são poucos e justificados durante reengagement; isso evita state update prematuro, porque features demais competem por atenção e latência.
- Decisão de review 028: **Decision Merger** — confirme que só uma ação comercial primária chega ao WhatsApp durante aplicação de cupom; isso evita rubric leniente, porque mensagem com múltiplas vendas parece spam.
- Decisão de review 029: **Message Composer** — confirme que texto final preserva evidence sem expor dados sensíveis durante pedido com restrição alimentar; isso evita token budget estourado, porque clareza não pode violar privacidade.
- Decisão de review 030: **Testing** — confirme que há unit, integration, acceptance e evaluation tests durante pedido com orçamento apertado; isso evita mensagem confusa, porque uma camada sozinha não cobre feature KODA real.
- Decisão de review 031: **Contract** — confirme que o contrato tem nome, versão, owner e business_goal testável durante descoberta de produto; isso evita restrição alimentar ignorada, porque sem identidade estável, incidentes ficam impossíveis de agrupar.
- Decisão de review 032: **Input contract** — confirme que cada campo obrigatório tem source explícito durante comparação de marcas; isso evita preço desatualizado, porque sem source, o Generator começa a adivinhar.
- Decisão de review 033: **Output contract** — confirme que mensagem, ação e state_updates estão separados durante decisão de compra; isso evita estoque antigo, porque sem separação, proposta rejeitada pode vazar para o cliente.
- Decisão de review 034: **Guarantees** — confirme que cada guarantee pode virar teste ou trace check durante checkout; isso evita upsell agressivo, porque garantia não verificável vira slogan.
- Decisão de review 035: **Constraints** — confirme que constraints de safety vencem objetivos comerciais durante pós-compra; isso evita oferta repetida, porque conversão não compensa quebra de confiança.
- Decisão de review 036: **Generator** — confirme que o Generator não envia resposta final sozinho durante reclamação de entrega; isso evita trace incompleto, porque self-evaluation collapse volta quando geração e aprovação se misturam.
- Decisão de review 037: **Evaluator** — confirme que rejection_code é específico e estável durante reengagement; isso evita state update prematuro, porque sem código, dashboard e retry ficam cegos.
- Decisão de review 038: **Rubric** — confirme que safety tem hard gate quando há restrição crítica durante aplicação de cupom; isso evita rubric leniente, porque média ponderada não pode esconder risco de saúde.
- Decisão de review 039: **Trace** — confirme que feature_run_id aparece em todos os eventos durante pedido com restrição alimentar; isso evita token budget estourado, porque sem correlação, replay vira caça ao tesouro.
- Decisão de review 040: **State** — confirme que apenas APPROVED gera commit durável durante pedido com orçamento apertado; isso evita mensagem confusa, porque estado otimista cria repetição e contradição.
- Decisão de review 041: **Token budget** — confirme que catálogo foi pré-filtrado antes do modelo durante descoberta de produto; isso evita restrição alimentar ignorada, porque catálogo bruto consome context window sem melhorar decisão.
- Decisão de review 042: **Router** — confirme que candidates são poucos e justificados durante comparação de marcas; isso evita preço desatualizado, porque features demais competem por atenção e latência.
- Decisão de review 043: **Decision Merger** — confirme que só uma ação comercial primária chega ao WhatsApp durante decisão de compra; isso evita estoque antigo, porque mensagem com múltiplas vendas parece spam.
- Decisão de review 044: **Message Composer** — confirme que texto final preserva evidence sem expor dados sensíveis durante checkout; isso evita upsell agressivo, porque clareza não pode violar privacidade.
- Decisão de review 045: **Testing** — confirme que há unit, integration, acceptance e evaluation tests durante pós-compra; isso evita oferta repetida, porque uma camada sozinha não cobre feature KODA real.
- Decisão de review 046: **Contract** — confirme que o contrato tem nome, versão, owner e business_goal testável durante reclamação de entrega; isso evita trace incompleto, porque sem identidade estável, incidentes ficam impossíveis de agrupar.
- Decisão de review 047: **Input contract** — confirme que cada campo obrigatório tem source explícito durante reengagement; isso evita state update prematuro, porque sem source, o Generator começa a adivinhar.
- Decisão de review 048: **Output contract** — confirme que mensagem, ação e state_updates estão separados durante aplicação de cupom; isso evita rubric leniente, porque sem separação, proposta rejeitada pode vazar para o cliente.
- Decisão de review 049: **Guarantees** — confirme que cada guarantee pode virar teste ou trace check durante pedido com restrição alimentar; isso evita token budget estourado, porque garantia não verificável vira slogan.
- Decisão de review 050: **Constraints** — confirme que constraints de safety vencem objetivos comerciais durante pedido com orçamento apertado; isso evita mensagem confusa, porque conversão não compensa quebra de confiança.
- Decisão de review 051: **Generator** — confirme que o Generator não envia resposta final sozinho durante descoberta de produto; isso evita restrição alimentar ignorada, porque self-evaluation collapse volta quando geração e aprovação se misturam.
- Decisão de review 052: **Evaluator** — confirme que rejection_code é específico e estável durante comparação de marcas; isso evita preço desatualizado, porque sem código, dashboard e retry ficam cegos.
- Decisão de review 053: **Rubric** — confirme que safety tem hard gate quando há restrição crítica durante decisão de compra; isso evita estoque antigo, porque média ponderada não pode esconder risco de saúde.
- Decisão de review 054: **Trace** — confirme que feature_run_id aparece em todos os eventos durante checkout; isso evita upsell agressivo, porque sem correlação, replay vira caça ao tesouro.
- Decisão de review 055: **State** — confirme que apenas APPROVED gera commit durável durante pós-compra; isso evita oferta repetida, porque estado otimista cria repetição e contradição.
- Decisão de review 056: **Token budget** — confirme que catálogo foi pré-filtrado antes do modelo durante reclamação de entrega; isso evita trace incompleto, porque catálogo bruto consome context window sem melhorar decisão.
- Decisão de review 057: **Router** — confirme que candidates são poucos e justificados durante reengagement; isso evita state update prematuro, porque features demais competem por atenção e latência.
- Decisão de review 058: **Decision Merger** — confirme que só uma ação comercial primária chega ao WhatsApp durante aplicação de cupom; isso evita rubric leniente, porque mensagem com múltiplas vendas parece spam.
- Decisão de review 059: **Message Composer** — confirme que texto final preserva evidence sem expor dados sensíveis durante pedido com restrição alimentar; isso evita token budget estourado, porque clareza não pode violar privacidade.
- Decisão de review 060: **Testing** — confirme que há unit, integration, acceptance e evaluation tests durante pedido com orçamento apertado; isso evita mensagem confusa, porque uma camada sozinha não cobre feature KODA real.
- Decisão de review 061: **Contract** — confirme que o contrato tem nome, versão, owner e business_goal testável durante descoberta de produto; isso evita restrição alimentar ignorada, porque sem identidade estável, incidentes ficam impossíveis de agrupar.
- Decisão de review 062: **Input contract** — confirme que cada campo obrigatório tem source explícito durante comparação de marcas; isso evita preço desatualizado, porque sem source, o Generator começa a adivinhar.
- Decisão de review 063: **Output contract** — confirme que mensagem, ação e state_updates estão separados durante decisão de compra; isso evita estoque antigo, porque sem separação, proposta rejeitada pode vazar para o cliente.
- Decisão de review 064: **Guarantees** — confirme que cada guarantee pode virar teste ou trace check durante checkout; isso evita upsell agressivo, porque garantia não verificável vira slogan.
- Decisão de review 065: **Constraints** — confirme que constraints de safety vencem objetivos comerciais durante pós-compra; isso evita oferta repetida, porque conversão não compensa quebra de confiança.
- Decisão de review 066: **Generator** — confirme que o Generator não envia resposta final sozinho durante reclamação de entrega; isso evita trace incompleto, porque self-evaluation collapse volta quando geração e aprovação se misturam.
- Decisão de review 067: **Evaluator** — confirme que rejection_code é específico e estável durante reengagement; isso evita state update prematuro, porque sem código, dashboard e retry ficam cegos.
- Decisão de review 068: **Rubric** — confirme que safety tem hard gate quando há restrição crítica durante aplicação de cupom; isso evita rubric leniente, porque média ponderada não pode esconder risco de saúde.
- Decisão de review 069: **Trace** — confirme que feature_run_id aparece em todos os eventos durante pedido com restrição alimentar; isso evita token budget estourado, porque sem correlação, replay vira caça ao tesouro.
- Decisão de review 070: **State** — confirme que apenas APPROVED gera commit durável durante pedido com orçamento apertado; isso evita mensagem confusa, porque estado otimista cria repetição e contradição.
- Decisão de review 071: **Token budget** — confirme que catálogo foi pré-filtrado antes do modelo durante descoberta de produto; isso evita restrição alimentar ignorada, porque catálogo bruto consome context window sem melhorar decisão.
- Decisão de review 072: **Router** — confirme que candidates são poucos e justificados durante comparação de marcas; isso evita preço desatualizado, porque features demais competem por atenção e latência.
- Decisão de review 073: **Decision Merger** — confirme que só uma ação comercial primária chega ao WhatsApp durante decisão de compra; isso evita estoque antigo, porque mensagem com múltiplas vendas parece spam.
- Decisão de review 074: **Message Composer** — confirme que texto final preserva evidence sem expor dados sensíveis durante checkout; isso evita upsell agressivo, porque clareza não pode violar privacidade.
- Decisão de review 075: **Testing** — confirme que há unit, integration, acceptance e evaluation tests durante pós-compra; isso evita oferta repetida, porque uma camada sozinha não cobre feature KODA real.
- Decisão de review 076: **Contract** — confirme que o contrato tem nome, versão, owner e business_goal testável durante reclamação de entrega; isso evita trace incompleto, porque sem identidade estável, incidentes ficam impossíveis de agrupar.
- Decisão de review 077: **Input contract** — confirme que cada campo obrigatório tem source explícito durante reengagement; isso evita state update prematuro, porque sem source, o Generator começa a adivinhar.
- Decisão de review 078: **Output contract** — confirme que mensagem, ação e state_updates estão separados durante aplicação de cupom; isso evita rubric leniente, porque sem separação, proposta rejeitada pode vazar para o cliente.
- Decisão de review 079: **Guarantees** — confirme que cada guarantee pode virar teste ou trace check durante pedido com restrição alimentar; isso evita token budget estourado, porque garantia não verificável vira slogan.
- Decisão de review 080: **Constraints** — confirme que constraints de safety vencem objetivos comerciais durante pedido com orçamento apertado; isso evita mensagem confusa, porque conversão não compensa quebra de confiança.
- Decisão de review 081: **Generator** — confirme que o Generator não envia resposta final sozinho durante descoberta de produto; isso evita restrição alimentar ignorada, porque self-evaluation collapse volta quando geração e aprovação se misturam.
- Decisão de review 082: **Evaluator** — confirme que rejection_code é específico e estável durante comparação de marcas; isso evita preço desatualizado, porque sem código, dashboard e retry ficam cegos.
- Decisão de review 083: **Rubric** — confirme que safety tem hard gate quando há restrição crítica durante decisão de compra; isso evita estoque antigo, porque média ponderada não pode esconder risco de saúde.
- Decisão de review 084: **Trace** — confirme que feature_run_id aparece em todos os eventos durante checkout; isso evita upsell agressivo, porque sem correlação, replay vira caça ao tesouro.
- Decisão de review 085: **State** — confirme que apenas APPROVED gera commit durável durante pós-compra; isso evita oferta repetida, porque estado otimista cria repetição e contradição.
- Decisão de review 086: **Token budget** — confirme que catálogo foi pré-filtrado antes do modelo durante reclamação de entrega; isso evita trace incompleto, porque catálogo bruto consome context window sem melhorar decisão.
- Decisão de review 087: **Router** — confirme que candidates são poucos e justificados durante reengagement; isso evita state update prematuro, porque features demais competem por atenção e latência.
- Decisão de review 088: **Decision Merger** — confirme que só uma ação comercial primária chega ao WhatsApp durante aplicação de cupom; isso evita rubric leniente, porque mensagem com múltiplas vendas parece spam.
- Decisão de review 089: **Message Composer** — confirme que texto final preserva evidence sem expor dados sensíveis durante pedido com restrição alimentar; isso evita token budget estourado, porque clareza não pode violar privacidade.
- Decisão de review 090: **Testing** — confirme que há unit, integration, acceptance e evaluation tests durante pedido com orçamento apertado; isso evita mensagem confusa, porque uma camada sozinha não cobre feature KODA real.
- Decisão de review 091: **Contract** — confirme que o contrato tem nome, versão, owner e business_goal testável durante descoberta de produto; isso evita restrição alimentar ignorada, porque sem identidade estável, incidentes ficam impossíveis de agrupar.
- Decisão de review 092: **Input contract** — confirme que cada campo obrigatório tem source explícito durante comparação de marcas; isso evita preço desatualizado, porque sem source, o Generator começa a adivinhar.
- Decisão de review 093: **Output contract** — confirme que mensagem, ação e state_updates estão separados durante decisão de compra; isso evita estoque antigo, porque sem separação, proposta rejeitada pode vazar para o cliente.
- Decisão de review 094: **Guarantees** — confirme que cada guarantee pode virar teste ou trace check durante checkout; isso evita upsell agressivo, porque garantia não verificável vira slogan.
- Decisão de review 095: **Constraints** — confirme que constraints de safety vencem objetivos comerciais durante pós-compra; isso evita oferta repetida, porque conversão não compensa quebra de confiança.
- Decisão de review 096: **Generator** — confirme que o Generator não envia resposta final sozinho durante reclamação de entrega; isso evita trace incompleto, porque self-evaluation collapse volta quando geração e aprovação se misturam.
- Decisão de review 097: **Evaluator** — confirme que rejection_code é específico e estável durante reengagement; isso evita state update prematuro, porque sem código, dashboard e retry ficam cegos.
- Decisão de review 098: **Rubric** — confirme que safety tem hard gate quando há restrição crítica durante aplicação de cupom; isso evita rubric leniente, porque média ponderada não pode esconder risco de saúde.
- Decisão de review 099: **Trace** — confirme que feature_run_id aparece em todos os eventos durante pedido com restrição alimentar; isso evita token budget estourado, porque sem correlação, replay vira caça ao tesouro.
- Decisão de review 100: **State** — confirme que apenas APPROVED gera commit durável durante pedido com orçamento apertado; isso evita mensagem confusa, porque estado otimista cria repetição e contradição.
- Decisão de review 101: **Token budget** — confirme que catálogo foi pré-filtrado antes do modelo durante descoberta de produto; isso evita restrição alimentar ignorada, porque catálogo bruto consome context window sem melhorar decisão.
- Decisão de review 102: **Router** — confirme que candidates são poucos e justificados durante comparação de marcas; isso evita preço desatualizado, porque features demais competem por atenção e latência.
- Decisão de review 103: **Decision Merger** — confirme que só uma ação comercial primária chega ao WhatsApp durante decisão de compra; isso evita estoque antigo, porque mensagem com múltiplas vendas parece spam.
- Decisão de review 104: **Message Composer** — confirme que texto final preserva evidence sem expor dados sensíveis durante checkout; isso evita upsell agressivo, porque clareza não pode violar privacidade.
- Decisão de review 105: **Testing** — confirme que há unit, integration, acceptance e evaluation tests durante pós-compra; isso evita oferta repetida, porque uma camada sozinha não cobre feature KODA real.
- Decisão de review 106: **Contract** — confirme que o contrato tem nome, versão, owner e business_goal testável durante reclamação de entrega; isso evita trace incompleto, porque sem identidade estável, incidentes ficam impossíveis de agrupar.
- Decisão de review 107: **Input contract** — confirme que cada campo obrigatório tem source explícito durante reengagement; isso evita state update prematuro, porque sem source, o Generator começa a adivinhar.
- Decisão de review 108: **Output contract** — confirme que mensagem, ação e state_updates estão separados durante aplicação de cupom; isso evita rubric leniente, porque sem separação, proposta rejeitada pode vazar para o cliente.
- Decisão de review 109: **Guarantees** — confirme que cada guarantee pode virar teste ou trace check durante pedido com restrição alimentar; isso evita token budget estourado, porque garantia não verificável vira slogan.
- Decisão de review 110: **Constraints** — confirme que constraints de safety vencem objetivos comerciais durante pedido com orçamento apertado; isso evita mensagem confusa, porque conversão não compensa quebra de confiança.
- Decisão de review 111: **Generator** — confirme que o Generator não envia resposta final sozinho durante descoberta de produto; isso evita restrição alimentar ignorada, porque self-evaluation collapse volta quando geração e aprovação se misturam.
- Decisão de review 112: **Evaluator** — confirme que rejection_code é específico e estável durante comparação de marcas; isso evita preço desatualizado, porque sem código, dashboard e retry ficam cegos.
- Decisão de review 113: **Rubric** — confirme que safety tem hard gate quando há restrição crítica durante decisão de compra; isso evita estoque antigo, porque média ponderada não pode esconder risco de saúde.
- Decisão de review 114: **Trace** — confirme que feature_run_id aparece em todos os eventos durante checkout; isso evita upsell agressivo, porque sem correlação, replay vira caça ao tesouro.
- Decisão de review 115: **State** — confirme que apenas APPROVED gera commit durável durante pós-compra; isso evita oferta repetida, porque estado otimista cria repetição e contradição.
- Decisão de review 116: **Token budget** — confirme que catálogo foi pré-filtrado antes do modelo durante reclamação de entrega; isso evita trace incompleto, porque catálogo bruto consome context window sem melhorar decisão.
- Decisão de review 117: **Router** — confirme que candidates são poucos e justificados durante reengagement; isso evita state update prematuro, porque features demais competem por atenção e latência.
- Decisão de review 118: **Decision Merger** — confirme que só uma ação comercial primária chega ao WhatsApp durante aplicação de cupom; isso evita rubric leniente, porque mensagem com múltiplas vendas parece spam.
- Decisão de review 119: **Message Composer** — confirme que texto final preserva evidence sem expor dados sensíveis durante pedido com restrição alimentar; isso evita token budget estourado, porque clareza não pode violar privacidade.
- Decisão de review 120: **Testing** — confirme que há unit, integration, acceptance e evaluation tests durante pedido com orçamento apertado; isso evita mensagem confusa, porque uma camada sozinha não cobre feature KODA real.
- Decisão de review 121: **Contract** — confirme que o contrato tem nome, versão, owner e business_goal testável durante descoberta de produto; isso evita restrição alimentar ignorada, porque sem identidade estável, incidentes ficam impossíveis de agrupar.
- Decisão de review 122: **Input contract** — confirme que cada campo obrigatório tem source explícito durante comparação de marcas; isso evita preço desatualizado, porque sem source, o Generator começa a adivinhar.
- Decisão de review 123: **Output contract** — confirme que mensagem, ação e state_updates estão separados durante decisão de compra; isso evita estoque antigo, porque sem separação, proposta rejeitada pode vazar para o cliente.
- Decisão de review 124: **Guarantees** — confirme que cada guarantee pode virar teste ou trace check durante checkout; isso evita upsell agressivo, porque garantia não verificável vira slogan.
- Decisão de review 125: **Constraints** — confirme que constraints de safety vencem objetivos comerciais durante pós-compra; isso evita oferta repetida, porque conversão não compensa quebra de confiança.
- Decisão de review 126: **Generator** — confirme que o Generator não envia resposta final sozinho durante reclamação de entrega; isso evita trace incompleto, porque self-evaluation collapse volta quando geração e aprovação se misturam.
- Decisão de review 127: **Evaluator** — confirme que rejection_code é específico e estável durante reengagement; isso evita state update prematuro, porque sem código, dashboard e retry ficam cegos.
- Decisão de review 128: **Rubric** — confirme que safety tem hard gate quando há restrição crítica durante aplicação de cupom; isso evita rubric leniente, porque média ponderada não pode esconder risco de saúde.
- Decisão de review 129: **Trace** — confirme que feature_run_id aparece em todos os eventos durante pedido com restrição alimentar; isso evita token budget estourado, porque sem correlação, replay vira caça ao tesouro.
- Decisão de review 130: **State** — confirme que apenas APPROVED gera commit durável durante pedido com orçamento apertado; isso evita mensagem confusa, porque estado otimista cria repetição e contradição.
- Decisão de review 131: **Token budget** — confirme que catálogo foi pré-filtrado antes do modelo durante descoberta de produto; isso evita restrição alimentar ignorada, porque catálogo bruto consome context window sem melhorar decisão.
- Decisão de review 132: **Router** — confirme que candidates são poucos e justificados durante comparação de marcas; isso evita preço desatualizado, porque features demais competem por atenção e latência.
- Decisão de review 133: **Decision Merger** — confirme que só uma ação comercial primária chega ao WhatsApp durante decisão de compra; isso evita estoque antigo, porque mensagem com múltiplas vendas parece spam.
- Decisão de review 134: **Message Composer** — confirme que texto final preserva evidence sem expor dados sensíveis durante checkout; isso evita upsell agressivo, porque clareza não pode violar privacidade.
- Decisão de review 135: **Testing** — confirme que há unit, integration, acceptance e evaluation tests durante pós-compra; isso evita oferta repetida, porque uma camada sozinha não cobre feature KODA real.
- Decisão de review 136: **Contract** — confirme que o contrato tem nome, versão, owner e business_goal testável durante reclamação de entrega; isso evita trace incompleto, porque sem identidade estável, incidentes ficam impossíveis de agrupar.
- Decisão de review 137: **Input contract** — confirme que cada campo obrigatório tem source explícito durante reengagement; isso evita state update prematuro, porque sem source, o Generator começa a adivinhar.
- Decisão de review 138: **Output contract** — confirme que mensagem, ação e state_updates estão separados durante aplicação de cupom; isso evita rubric leniente, porque sem separação, proposta rejeitada pode vazar para o cliente.
- Decisão de review 139: **Guarantees** — confirme que cada guarantee pode virar teste ou trace check durante pedido com restrição alimentar; isso evita token budget estourado, porque garantia não verificável vira slogan.
- Decisão de review 140: **Constraints** — confirme que constraints de safety vencem objetivos comerciais durante pedido com orçamento apertado; isso evita mensagem confusa, porque conversão não compensa quebra de confiança.
- Decisão de review 141: **Generator** — confirme que o Generator não envia resposta final sozinho durante descoberta de produto; isso evita restrição alimentar ignorada, porque self-evaluation collapse volta quando geração e aprovação se misturam.
- Decisão de review 142: **Evaluator** — confirme que rejection_code é específico e estável durante comparação de marcas; isso evita preço desatualizado, porque sem código, dashboard e retry ficam cegos.
- Decisão de review 143: **Rubric** — confirme que safety tem hard gate quando há restrição crítica durante decisão de compra; isso evita estoque antigo, porque média ponderada não pode esconder risco de saúde.
- Decisão de review 144: **Trace** — confirme que feature_run_id aparece em todos os eventos durante checkout; isso evita upsell agressivo, porque sem correlação, replay vira caça ao tesouro.
- Decisão de review 145: **State** — confirme que apenas APPROVED gera commit durável durante pós-compra; isso evita oferta repetida, porque estado otimista cria repetição e contradição.
- Decisão de review 146: **Token budget** — confirme que catálogo foi pré-filtrado antes do modelo durante reclamação de entrega; isso evita trace incompleto, porque catálogo bruto consome context window sem melhorar decisão.
- Decisão de review 147: **Router** — confirme que candidates são poucos e justificados durante reengagement; isso evita state update prematuro, porque features demais competem por atenção e latência.
- Decisão de review 148: **Decision Merger** — confirme que só uma ação comercial primária chega ao WhatsApp durante aplicação de cupom; isso evita rubric leniente, porque mensagem com múltiplas vendas parece spam.
- Decisão de review 149: **Message Composer** — confirme que texto final preserva evidence sem expor dados sensíveis durante pedido com restrição alimentar; isso evita token budget estourado, porque clareza não pode violar privacidade.
- Decisão de review 150: **Testing** — confirme que há unit, integration, acceptance e evaluation tests durante pedido com orçamento apertado; isso evita mensagem confusa, porque uma camada sozinha não cobre feature KODA real.
- Decisão de review 151: **Contract** — confirme que o contrato tem nome, versão, owner e business_goal testável durante descoberta de produto; isso evita restrição alimentar ignorada, porque sem identidade estável, incidentes ficam impossíveis de agrupar.
- Decisão de review 152: **Input contract** — confirme que cada campo obrigatório tem source explícito durante comparação de marcas; isso evita preço desatualizado, porque sem source, o Generator começa a adivinhar.
- Decisão de review 153: **Output contract** — confirme que mensagem, ação e state_updates estão separados durante decisão de compra; isso evita estoque antigo, porque sem separação, proposta rejeitada pode vazar para o cliente.
- Decisão de review 154: **Guarantees** — confirme que cada guarantee pode virar teste ou trace check durante checkout; isso evita upsell agressivo, porque garantia não verificável vira slogan.
- Decisão de review 155: **Constraints** — confirme que constraints de safety vencem objetivos comerciais durante pós-compra; isso evita oferta repetida, porque conversão não compensa quebra de confiança.
- Decisão de review 156: **Generator** — confirme que o Generator não envia resposta final sozinho durante reclamação de entrega; isso evita trace incompleto, porque self-evaluation collapse volta quando geração e aprovação se misturam.
- Decisão de review 157: **Evaluator** — confirme que rejection_code é específico e estável durante reengagement; isso evita state update prematuro, porque sem código, dashboard e retry ficam cegos.
- Decisão de review 158: **Rubric** — confirme que safety tem hard gate quando há restrição crítica durante aplicação de cupom; isso evita rubric leniente, porque média ponderada não pode esconder risco de saúde.
- Decisão de review 159: **Trace** — confirme que feature_run_id aparece em todos os eventos durante pedido com restrição alimentar; isso evita token budget estourado, porque sem correlação, replay vira caça ao tesouro.
- Decisão de review 160: **State** — confirme que apenas APPROVED gera commit durável durante pedido com orçamento apertado; isso evita mensagem confusa, porque estado otimista cria repetição e contradição.
- Decisão de review 161: **Token budget** — confirme que catálogo foi pré-filtrado antes do modelo durante descoberta de produto; isso evita restrição alimentar ignorada, porque catálogo bruto consome context window sem melhorar decisão.
- Decisão de review 162: **Router** — confirme que candidates são poucos e justificados durante comparação de marcas; isso evita preço desatualizado, porque features demais competem por atenção e latência.
- Decisão de review 163: **Decision Merger** — confirme que só uma ação comercial primária chega ao WhatsApp durante decisão de compra; isso evita estoque antigo, porque mensagem com múltiplas vendas parece spam.
- Decisão de review 164: **Message Composer** — confirme que texto final preserva evidence sem expor dados sensíveis durante checkout; isso evita upsell agressivo, porque clareza não pode violar privacidade.
- Decisão de review 165: **Testing** — confirme que há unit, integration, acceptance e evaluation tests durante pós-compra; isso evita oferta repetida, porque uma camada sozinha não cobre feature KODA real.
- Decisão de review 166: **Contract** — confirme que o contrato tem nome, versão, owner e business_goal testável durante reclamação de entrega; isso evita trace incompleto, porque sem identidade estável, incidentes ficam impossíveis de agrupar.
- Decisão de review 167: **Input contract** — confirme que cada campo obrigatório tem source explícito durante reengagement; isso evita state update prematuro, porque sem source, o Generator começa a adivinhar.
- Decisão de review 168: **Output contract** — confirme que mensagem, ação e state_updates estão separados durante aplicação de cupom; isso evita rubric leniente, porque sem separação, proposta rejeitada pode vazar para o cliente.
- Decisão de review 169: **Guarantees** — confirme que cada guarantee pode virar teste ou trace check durante pedido com restrição alimentar; isso evita token budget estourado, porque garantia não verificável vira slogan.
- Decisão de review 170: **Constraints** — confirme que constraints de safety vencem objetivos comerciais durante pedido com orçamento apertado; isso evita mensagem confusa, porque conversão não compensa quebra de confiança.
- Decisão de review 171: **Generator** — confirme que o Generator não envia resposta final sozinho durante descoberta de produto; isso evita restrição alimentar ignorada, porque self-evaluation collapse volta quando geração e aprovação se misturam.
- Decisão de review 172: **Evaluator** — confirme que rejection_code é específico e estável durante comparação de marcas; isso evita preço desatualizado, porque sem código, dashboard e retry ficam cegos.
- Decisão de review 173: **Rubric** — confirme que safety tem hard gate quando há restrição crítica durante decisão de compra; isso evita estoque antigo, porque média ponderada não pode esconder risco de saúde.
- Decisão de review 174: **Trace** — confirme que feature_run_id aparece em todos os eventos durante checkout; isso evita upsell agressivo, porque sem correlação, replay vira caça ao tesouro.
- Decisão de review 175: **State** — confirme que apenas APPROVED gera commit durável durante pós-compra; isso evita oferta repetida, porque estado otimista cria repetição e contradição.
- Decisão de review 176: **Token budget** — confirme que catálogo foi pré-filtrado antes do modelo durante reclamação de entrega; isso evita trace incompleto, porque catálogo bruto consome context window sem melhorar decisão.
- Decisão de review 177: **Router** — confirme que candidates são poucos e justificados durante reengagement; isso evita state update prematuro, porque features demais competem por atenção e latência.
- Decisão de review 178: **Decision Merger** — confirme que só uma ação comercial primária chega ao WhatsApp durante aplicação de cupom; isso evita rubric leniente, porque mensagem com múltiplas vendas parece spam.
- Decisão de review 179: **Message Composer** — confirme que texto final preserva evidence sem expor dados sensíveis durante pedido com restrição alimentar; isso evita token budget estourado, porque clareza não pode violar privacidade.
- Decisão de review 180: **Testing** — confirme que há unit, integration, acceptance e evaluation tests durante pedido com orçamento apertado; isso evita mensagem confusa, porque uma camada sozinha não cobre feature KODA real.
- Decisão de review 181: **Contract** — confirme que o contrato tem nome, versão, owner e business_goal testável durante descoberta de produto; isso evita restrição alimentar ignorada, porque sem identidade estável, incidentes ficam impossíveis de agrupar.
- Decisão de review 182: **Input contract** — confirme que cada campo obrigatório tem source explícito durante comparação de marcas; isso evita preço desatualizado, porque sem source, o Generator começa a adivinhar.
- Decisão de review 183: **Output contract** — confirme que mensagem, ação e state_updates estão separados durante decisão de compra; isso evita estoque antigo, porque sem separação, proposta rejeitada pode vazar para o cliente.
- Decisão de review 184: **Guarantees** — confirme que cada guarantee pode virar teste ou trace check durante checkout; isso evita upsell agressivo, porque garantia não verificável vira slogan.
- Decisão de review 185: **Constraints** — confirme que constraints de safety vencem objetivos comerciais durante pós-compra; isso evita oferta repetida, porque conversão não compensa quebra de confiança.
- Decisão de review 186: **Generator** — confirme que o Generator não envia resposta final sozinho durante reclamação de entrega; isso evita trace incompleto, porque self-evaluation collapse volta quando geração e aprovação se misturam.
- Decisão de review 187: **Evaluator** — confirme que rejection_code é específico e estável durante reengagement; isso evita state update prematuro, porque sem código, dashboard e retry ficam cegos.
- Decisão de review 188: **Rubric** — confirme que safety tem hard gate quando há restrição crítica durante aplicação de cupom; isso evita rubric leniente, porque média ponderada não pode esconder risco de saúde.
- Decisão de review 189: **Trace** — confirme que feature_run_id aparece em todos os eventos durante pedido com restrição alimentar; isso evita token budget estourado, porque sem correlação, replay vira caça ao tesouro.
- Decisão de review 190: **State** — confirme que apenas APPROVED gera commit durável durante pedido com orçamento apertado; isso evita mensagem confusa, porque estado otimista cria repetição e contradição.
- Decisão de review 191: **Token budget** — confirme que catálogo foi pré-filtrado antes do modelo durante descoberta de produto; isso evita restrição alimentar ignorada, porque catálogo bruto consome context window sem melhorar decisão.
- Decisão de review 192: **Router** — confirme que candidates são poucos e justificados durante comparação de marcas; isso evita preço desatualizado, porque features demais competem por atenção e latência.
- Decisão de review 193: **Decision Merger** — confirme que só uma ação comercial primária chega ao WhatsApp durante decisão de compra; isso evita estoque antigo, porque mensagem com múltiplas vendas parece spam.
- Decisão de review 194: **Message Composer** — confirme que texto final preserva evidence sem expor dados sensíveis durante checkout; isso evita upsell agressivo, porque clareza não pode violar privacidade.
- Decisão de review 195: **Testing** — confirme que há unit, integration, acceptance e evaluation tests durante pós-compra; isso evita oferta repetida, porque uma camada sozinha não cobre feature KODA real.
- Decisão de review 196: **Contract** — confirme que o contrato tem nome, versão, owner e business_goal testável durante reclamação de entrega; isso evita trace incompleto, porque sem identidade estável, incidentes ficam impossíveis de agrupar.
- Decisão de review 197: **Input contract** — confirme que cada campo obrigatório tem source explícito durante reengagement; isso evita state update prematuro, porque sem source, o Generator começa a adivinhar.
- Decisão de review 198: **Output contract** — confirme que mensagem, ação e state_updates estão separados durante aplicação de cupom; isso evita rubric leniente, porque sem separação, proposta rejeitada pode vazar para o cliente.
- Decisão de review 199: **Guarantees** — confirme que cada guarantee pode virar teste ou trace check durante pedido com restrição alimentar; isso evita token budget estourado, porque garantia não verificável vira slogan.
- Decisão de review 200: **Constraints** — confirme que constraints de safety vencem objetivos comerciais durante pedido com orçamento apertado; isso evita mensagem confusa, porque conversão não compensa quebra de confiança.
- Decisão de review 201: **Generator** — confirme que o Generator não envia resposta final sozinho durante descoberta de produto; isso evita restrição alimentar ignorada, porque self-evaluation collapse volta quando geração e aprovação se misturam.
- Decisão de review 202: **Evaluator** — confirme que rejection_code é específico e estável durante comparação de marcas; isso evita preço desatualizado, porque sem código, dashboard e retry ficam cegos.
- Decisão de review 203: **Rubric** — confirme que safety tem hard gate quando há restrição crítica durante decisão de compra; isso evita estoque antigo, porque média ponderada não pode esconder risco de saúde.
- Decisão de review 204: **Trace** — confirme que feature_run_id aparece em todos os eventos durante checkout; isso evita upsell agressivo, porque sem correlação, replay vira caça ao tesouro.
- Decisão de review 205: **State** — confirme que apenas APPROVED gera commit durável durante pós-compra; isso evita oferta repetida, porque estado otimista cria repetição e contradição.
- Decisão de review 206: **Token budget** — confirme que catálogo foi pré-filtrado antes do modelo durante reclamação de entrega; isso evita trace incompleto, porque catálogo bruto consome context window sem melhorar decisão.
- Decisão de review 207: **Router** — confirme que candidates são poucos e justificados durante reengagement; isso evita state update prematuro, porque features demais competem por atenção e latência.
- Decisão de review 208: **Decision Merger** — confirme que só uma ação comercial primária chega ao WhatsApp durante aplicação de cupom; isso evita rubric leniente, porque mensagem com múltiplas vendas parece spam.
- Decisão de review 209: **Message Composer** — confirme que texto final preserva evidence sem expor dados sensíveis durante pedido com restrição alimentar; isso evita token budget estourado, porque clareza não pode violar privacidade.
- Decisão de review 210: **Testing** — confirme que há unit, integration, acceptance e evaluation tests durante pedido com orçamento apertado; isso evita mensagem confusa, porque uma camada sozinha não cobre feature KODA real.
- Decisão de review 211: **Contract** — confirme que o contrato tem nome, versão, owner e business_goal testável durante descoberta de produto; isso evita restrição alimentar ignorada, porque sem identidade estável, incidentes ficam impossíveis de agrupar.
- Decisão de review 212: **Input contract** — confirme que cada campo obrigatório tem source explícito durante comparação de marcas; isso evita preço desatualizado, porque sem source, o Generator começa a adivinhar.
- Decisão de review 213: **Output contract** — confirme que mensagem, ação e state_updates estão separados durante decisão de compra; isso evita estoque antigo, porque sem separação, proposta rejeitada pode vazar para o cliente.
- Decisão de review 214: **Guarantees** — confirme que cada guarantee pode virar teste ou trace check durante checkout; isso evita upsell agressivo, porque garantia não verificável vira slogan.
- Decisão de review 215: **Constraints** — confirme que constraints de safety vencem objetivos comerciais durante pós-compra; isso evita oferta repetida, porque conversão não compensa quebra de confiança.
- Decisão de review 216: **Generator** — confirme que o Generator não envia resposta final sozinho durante reclamação de entrega; isso evita trace incompleto, porque self-evaluation collapse volta quando geração e aprovação se misturam.
- Decisão de review 217: **Evaluator** — confirme que rejection_code é específico e estável durante reengagement; isso evita state update prematuro, porque sem código, dashboard e retry ficam cegos.
- Decisão de review 218: **Rubric** — confirme que safety tem hard gate quando há restrição crítica durante aplicação de cupom; isso evita rubric leniente, porque média ponderada não pode esconder risco de saúde.
- Decisão de review 219: **Trace** — confirme que feature_run_id aparece em todos os eventos durante pedido com restrição alimentar; isso evita token budget estourado, porque sem correlação, replay vira caça ao tesouro.
- Decisão de review 220: **State** — confirme que apenas APPROVED gera commit durável durante pedido com orçamento apertado; isso evita mensagem confusa, porque estado otimista cria repetição e contradição.
### Casos de Borda que Devem Entrar no Banco de QA
- Caso de borda 001: **Cliente declara sem lactose no início e esquece de repetir depois**. Feature foco: `product_recommendation`. Resultado esperado: state persistence deve manter restrição e Evaluator deve bloquear lactose.
- Caso de borda 002: **Cliente muda orçamento de R$ 200 para R$ 120 no meio da conversa**. Feature foco: `contextual_upsell`. Resultado esperado: latest_customer_intent deve atualizar budget transitório e trace deve registrar mudança.
- Caso de borda 003: **Cliente aceita whey, mas recusa creatina explicitamente**. Feature foco: `discount_explanation`. Resultado esperado: offer_history deve bloquear novo upsell de creatina nesta conversa.
- Caso de borda 004: **Cliente pergunta por entrega antes de escolher produto**. Feature foco: `fulfillment_promise`. Resultado esperado: fulfillment feature deve responder disponibilidade geral sem prometer ETA específico.
- Caso de borda 005: **Cliente reclama de cobrança duplicada**. Feature foco: `safety_guard`. Resultado esperado: support intent deve vencer features comerciais no Decision Merger.
- Caso de borda 006: **Catálogo retorna produto sem campo lactose_free**. Feature foco: `product_recommendation`. Resultado esperado: Product Recommendation deve abstêr ou escalar em vez de assumir seguro.
- Caso de borda 007: **Cupom do cliente não é cumulativo com clube**. Feature foco: `contextual_upsell`. Resultado esperado: Discount feature deve aplicar melhor desconto válido e explicar sem confusão.
- Caso de borda 008: **Generator produz três opções, mas uma não tem evidence**. Feature foco: `discount_explanation`. Resultado esperado: Output contract validation deve falhar antes do Evaluator.
- Caso de borda 009: **Evaluator rejeita top-1 por timing ruim**. Feature foco: `fulfillment_promise`. Resultado esperado: Decision Merger deve tentar top-2 ou DEFERRED, nunca enviar top-1.
- Caso de borda 010: **Trace commit falha depois de mensagem pronta**. Feature foco: `safety_guard`. Resultado esperado: pipeline deve impedir envio se ação crítica não é auditável.
- Caso de borda 011: **Cliente declara sem lactose no início e esquece de repetir depois**. Feature foco: `product_recommendation`. Resultado esperado: state persistence deve manter restrição e Evaluator deve bloquear lactose.
- Caso de borda 012: **Cliente muda orçamento de R$ 200 para R$ 120 no meio da conversa**. Feature foco: `contextual_upsell`. Resultado esperado: latest_customer_intent deve atualizar budget transitório e trace deve registrar mudança.
- Caso de borda 013: **Cliente aceita whey, mas recusa creatina explicitamente**. Feature foco: `discount_explanation`. Resultado esperado: offer_history deve bloquear novo upsell de creatina nesta conversa.
- Caso de borda 014: **Cliente pergunta por entrega antes de escolher produto**. Feature foco: `fulfillment_promise`. Resultado esperado: fulfillment feature deve responder disponibilidade geral sem prometer ETA específico.
- Caso de borda 015: **Cliente reclama de cobrança duplicada**. Feature foco: `safety_guard`. Resultado esperado: support intent deve vencer features comerciais no Decision Merger.
- Caso de borda 016: **Catálogo retorna produto sem campo lactose_free**. Feature foco: `product_recommendation`. Resultado esperado: Product Recommendation deve abstêr ou escalar em vez de assumir seguro.
- Caso de borda 017: **Cupom do cliente não é cumulativo com clube**. Feature foco: `contextual_upsell`. Resultado esperado: Discount feature deve aplicar melhor desconto válido e explicar sem confusão.
- Caso de borda 018: **Generator produz três opções, mas uma não tem evidence**. Feature foco: `discount_explanation`. Resultado esperado: Output contract validation deve falhar antes do Evaluator.
- Caso de borda 019: **Evaluator rejeita top-1 por timing ruim**. Feature foco: `fulfillment_promise`. Resultado esperado: Decision Merger deve tentar top-2 ou DEFERRED, nunca enviar top-1.
- Caso de borda 020: **Trace commit falha depois de mensagem pronta**. Feature foco: `safety_guard`. Resultado esperado: pipeline deve impedir envio se ação crítica não é auditável.
- Caso de borda 021: **Cliente declara sem lactose no início e esquece de repetir depois**. Feature foco: `product_recommendation`. Resultado esperado: state persistence deve manter restrição e Evaluator deve bloquear lactose.
- Caso de borda 022: **Cliente muda orçamento de R$ 200 para R$ 120 no meio da conversa**. Feature foco: `contextual_upsell`. Resultado esperado: latest_customer_intent deve atualizar budget transitório e trace deve registrar mudança.
- Caso de borda 023: **Cliente aceita whey, mas recusa creatina explicitamente**. Feature foco: `discount_explanation`. Resultado esperado: offer_history deve bloquear novo upsell de creatina nesta conversa.
- Caso de borda 024: **Cliente pergunta por entrega antes de escolher produto**. Feature foco: `fulfillment_promise`. Resultado esperado: fulfillment feature deve responder disponibilidade geral sem prometer ETA específico.
- Caso de borda 025: **Cliente reclama de cobrança duplicada**. Feature foco: `safety_guard`. Resultado esperado: support intent deve vencer features comerciais no Decision Merger.
- Caso de borda 026: **Catálogo retorna produto sem campo lactose_free**. Feature foco: `product_recommendation`. Resultado esperado: Product Recommendation deve abstêr ou escalar em vez de assumir seguro.
- Caso de borda 027: **Cupom do cliente não é cumulativo com clube**. Feature foco: `contextual_upsell`. Resultado esperado: Discount feature deve aplicar melhor desconto válido e explicar sem confusão.
- Caso de borda 028: **Generator produz três opções, mas uma não tem evidence**. Feature foco: `discount_explanation`. Resultado esperado: Output contract validation deve falhar antes do Evaluator.
- Caso de borda 029: **Evaluator rejeita top-1 por timing ruim**. Feature foco: `fulfillment_promise`. Resultado esperado: Decision Merger deve tentar top-2 ou DEFERRED, nunca enviar top-1.
- Caso de borda 030: **Trace commit falha depois de mensagem pronta**. Feature foco: `safety_guard`. Resultado esperado: pipeline deve impedir envio se ação crítica não é auditável.
- Caso de borda 031: **Cliente declara sem lactose no início e esquece de repetir depois**. Feature foco: `product_recommendation`. Resultado esperado: state persistence deve manter restrição e Evaluator deve bloquear lactose.
- Caso de borda 032: **Cliente muda orçamento de R$ 200 para R$ 120 no meio da conversa**. Feature foco: `contextual_upsell`. Resultado esperado: latest_customer_intent deve atualizar budget transitório e trace deve registrar mudança.
- Caso de borda 033: **Cliente aceita whey, mas recusa creatina explicitamente**. Feature foco: `discount_explanation`. Resultado esperado: offer_history deve bloquear novo upsell de creatina nesta conversa.
- Caso de borda 034: **Cliente pergunta por entrega antes de escolher produto**. Feature foco: `fulfillment_promise`. Resultado esperado: fulfillment feature deve responder disponibilidade geral sem prometer ETA específico.
- Caso de borda 035: **Cliente reclama de cobrança duplicada**. Feature foco: `safety_guard`. Resultado esperado: support intent deve vencer features comerciais no Decision Merger.
- Caso de borda 036: **Catálogo retorna produto sem campo lactose_free**. Feature foco: `product_recommendation`. Resultado esperado: Product Recommendation deve abstêr ou escalar em vez de assumir seguro.
- Caso de borda 037: **Cupom do cliente não é cumulativo com clube**. Feature foco: `contextual_upsell`. Resultado esperado: Discount feature deve aplicar melhor desconto válido e explicar sem confusão.
- Caso de borda 038: **Generator produz três opções, mas uma não tem evidence**. Feature foco: `discount_explanation`. Resultado esperado: Output contract validation deve falhar antes do Evaluator.
- Caso de borda 039: **Evaluator rejeita top-1 por timing ruim**. Feature foco: `fulfillment_promise`. Resultado esperado: Decision Merger deve tentar top-2 ou DEFERRED, nunca enviar top-1.
- Caso de borda 040: **Trace commit falha depois de mensagem pronta**. Feature foco: `safety_guard`. Resultado esperado: pipeline deve impedir envio se ação crítica não é auditável.
- Caso de borda 041: **Cliente declara sem lactose no início e esquece de repetir depois**. Feature foco: `product_recommendation`. Resultado esperado: state persistence deve manter restrição e Evaluator deve bloquear lactose.
- Caso de borda 042: **Cliente muda orçamento de R$ 200 para R$ 120 no meio da conversa**. Feature foco: `contextual_upsell`. Resultado esperado: latest_customer_intent deve atualizar budget transitório e trace deve registrar mudança.
- Caso de borda 043: **Cliente aceita whey, mas recusa creatina explicitamente**. Feature foco: `discount_explanation`. Resultado esperado: offer_history deve bloquear novo upsell de creatina nesta conversa.
- Caso de borda 044: **Cliente pergunta por entrega antes de escolher produto**. Feature foco: `fulfillment_promise`. Resultado esperado: fulfillment feature deve responder disponibilidade geral sem prometer ETA específico.
- Caso de borda 045: **Cliente reclama de cobrança duplicada**. Feature foco: `safety_guard`. Resultado esperado: support intent deve vencer features comerciais no Decision Merger.
- Caso de borda 046: **Catálogo retorna produto sem campo lactose_free**. Feature foco: `product_recommendation`. Resultado esperado: Product Recommendation deve abstêr ou escalar em vez de assumir seguro.
- Caso de borda 047: **Cupom do cliente não é cumulativo com clube**. Feature foco: `contextual_upsell`. Resultado esperado: Discount feature deve aplicar melhor desconto válido e explicar sem confusão.
- Caso de borda 048: **Generator produz três opções, mas uma não tem evidence**. Feature foco: `discount_explanation`. Resultado esperado: Output contract validation deve falhar antes do Evaluator.
- Caso de borda 049: **Evaluator rejeita top-1 por timing ruim**. Feature foco: `fulfillment_promise`. Resultado esperado: Decision Merger deve tentar top-2 ou DEFERRED, nunca enviar top-1.
- Caso de borda 050: **Trace commit falha depois de mensagem pronta**. Feature foco: `safety_guard`. Resultado esperado: pipeline deve impedir envio se ação crítica não é auditável.
- Caso de borda 051: **Cliente declara sem lactose no início e esquece de repetir depois**. Feature foco: `product_recommendation`. Resultado esperado: state persistence deve manter restrição e Evaluator deve bloquear lactose.
- Caso de borda 052: **Cliente muda orçamento de R$ 200 para R$ 120 no meio da conversa**. Feature foco: `contextual_upsell`. Resultado esperado: latest_customer_intent deve atualizar budget transitório e trace deve registrar mudança.
- Caso de borda 053: **Cliente aceita whey, mas recusa creatina explicitamente**. Feature foco: `discount_explanation`. Resultado esperado: offer_history deve bloquear novo upsell de creatina nesta conversa.
- Caso de borda 054: **Cliente pergunta por entrega antes de escolher produto**. Feature foco: `fulfillment_promise`. Resultado esperado: fulfillment feature deve responder disponibilidade geral sem prometer ETA específico.
- Caso de borda 055: **Cliente reclama de cobrança duplicada**. Feature foco: `safety_guard`. Resultado esperado: support intent deve vencer features comerciais no Decision Merger.
- Caso de borda 056: **Catálogo retorna produto sem campo lactose_free**. Feature foco: `product_recommendation`. Resultado esperado: Product Recommendation deve abstêr ou escalar em vez de assumir seguro.
- Caso de borda 057: **Cupom do cliente não é cumulativo com clube**. Feature foco: `contextual_upsell`. Resultado esperado: Discount feature deve aplicar melhor desconto válido e explicar sem confusão.
- Caso de borda 058: **Generator produz três opções, mas uma não tem evidence**. Feature foco: `discount_explanation`. Resultado esperado: Output contract validation deve falhar antes do Evaluator.
- Caso de borda 059: **Evaluator rejeita top-1 por timing ruim**. Feature foco: `fulfillment_promise`. Resultado esperado: Decision Merger deve tentar top-2 ou DEFERRED, nunca enviar top-1.
- Caso de borda 060: **Trace commit falha depois de mensagem pronta**. Feature foco: `safety_guard`. Resultado esperado: pipeline deve impedir envio se ação crítica não é auditável.
- Caso de borda 061: **Cliente declara sem lactose no início e esquece de repetir depois**. Feature foco: `product_recommendation`. Resultado esperado: state persistence deve manter restrição e Evaluator deve bloquear lactose.
- Caso de borda 062: **Cliente muda orçamento de R$ 200 para R$ 120 no meio da conversa**. Feature foco: `contextual_upsell`. Resultado esperado: latest_customer_intent deve atualizar budget transitório e trace deve registrar mudança.
- Caso de borda 063: **Cliente aceita whey, mas recusa creatina explicitamente**. Feature foco: `discount_explanation`. Resultado esperado: offer_history deve bloquear novo upsell de creatina nesta conversa.
- Caso de borda 064: **Cliente pergunta por entrega antes de escolher produto**. Feature foco: `fulfillment_promise`. Resultado esperado: fulfillment feature deve responder disponibilidade geral sem prometer ETA específico.
- Caso de borda 065: **Cliente reclama de cobrança duplicada**. Feature foco: `safety_guard`. Resultado esperado: support intent deve vencer features comerciais no Decision Merger.
- Caso de borda 066: **Catálogo retorna produto sem campo lactose_free**. Feature foco: `product_recommendation`. Resultado esperado: Product Recommendation deve abstêr ou escalar em vez de assumir seguro.
- Caso de borda 067: **Cupom do cliente não é cumulativo com clube**. Feature foco: `contextual_upsell`. Resultado esperado: Discount feature deve aplicar melhor desconto válido e explicar sem confusão.
- Caso de borda 068: **Generator produz três opções, mas uma não tem evidence**. Feature foco: `discount_explanation`. Resultado esperado: Output contract validation deve falhar antes do Evaluator.
- Caso de borda 069: **Evaluator rejeita top-1 por timing ruim**. Feature foco: `fulfillment_promise`. Resultado esperado: Decision Merger deve tentar top-2 ou DEFERRED, nunca enviar top-1.
- Caso de borda 070: **Trace commit falha depois de mensagem pronta**. Feature foco: `safety_guard`. Resultado esperado: pipeline deve impedir envio se ação crítica não é auditável.
- Caso de borda 071: **Cliente declara sem lactose no início e esquece de repetir depois**. Feature foco: `product_recommendation`. Resultado esperado: state persistence deve manter restrição e Evaluator deve bloquear lactose.
- Caso de borda 072: **Cliente muda orçamento de R$ 200 para R$ 120 no meio da conversa**. Feature foco: `contextual_upsell`. Resultado esperado: latest_customer_intent deve atualizar budget transitório e trace deve registrar mudança.
- Caso de borda 073: **Cliente aceita whey, mas recusa creatina explicitamente**. Feature foco: `discount_explanation`. Resultado esperado: offer_history deve bloquear novo upsell de creatina nesta conversa.
- Caso de borda 074: **Cliente pergunta por entrega antes de escolher produto**. Feature foco: `fulfillment_promise`. Resultado esperado: fulfillment feature deve responder disponibilidade geral sem prometer ETA específico.
- Caso de borda 075: **Cliente reclama de cobrança duplicada**. Feature foco: `safety_guard`. Resultado esperado: support intent deve vencer features comerciais no Decision Merger.
- Caso de borda 076: **Catálogo retorna produto sem campo lactose_free**. Feature foco: `product_recommendation`. Resultado esperado: Product Recommendation deve abstêr ou escalar em vez de assumir seguro.
- Caso de borda 077: **Cupom do cliente não é cumulativo com clube**. Feature foco: `contextual_upsell`. Resultado esperado: Discount feature deve aplicar melhor desconto válido e explicar sem confusão.
- Caso de borda 078: **Generator produz três opções, mas uma não tem evidence**. Feature foco: `discount_explanation`. Resultado esperado: Output contract validation deve falhar antes do Evaluator.
- Caso de borda 079: **Evaluator rejeita top-1 por timing ruim**. Feature foco: `fulfillment_promise`. Resultado esperado: Decision Merger deve tentar top-2 ou DEFERRED, nunca enviar top-1.
- Caso de borda 080: **Trace commit falha depois de mensagem pronta**. Feature foco: `safety_guard`. Resultado esperado: pipeline deve impedir envio se ação crítica não é auditável.
- Caso de borda 081: **Cliente declara sem lactose no início e esquece de repetir depois**. Feature foco: `product_recommendation`. Resultado esperado: state persistence deve manter restrição e Evaluator deve bloquear lactose.
- Caso de borda 082: **Cliente muda orçamento de R$ 200 para R$ 120 no meio da conversa**. Feature foco: `contextual_upsell`. Resultado esperado: latest_customer_intent deve atualizar budget transitório e trace deve registrar mudança.
- Caso de borda 083: **Cliente aceita whey, mas recusa creatina explicitamente**. Feature foco: `discount_explanation`. Resultado esperado: offer_history deve bloquear novo upsell de creatina nesta conversa.
- Caso de borda 084: **Cliente pergunta por entrega antes de escolher produto**. Feature foco: `fulfillment_promise`. Resultado esperado: fulfillment feature deve responder disponibilidade geral sem prometer ETA específico.
- Caso de borda 085: **Cliente reclama de cobrança duplicada**. Feature foco: `safety_guard`. Resultado esperado: support intent deve vencer features comerciais no Decision Merger.
- Caso de borda 086: **Catálogo retorna produto sem campo lactose_free**. Feature foco: `product_recommendation`. Resultado esperado: Product Recommendation deve abstêr ou escalar em vez de assumir seguro.
- Caso de borda 087: **Cupom do cliente não é cumulativo com clube**. Feature foco: `contextual_upsell`. Resultado esperado: Discount feature deve aplicar melhor desconto válido e explicar sem confusão.
- Caso de borda 088: **Generator produz três opções, mas uma não tem evidence**. Feature foco: `discount_explanation`. Resultado esperado: Output contract validation deve falhar antes do Evaluator.
- Caso de borda 089: **Evaluator rejeita top-1 por timing ruim**. Feature foco: `fulfillment_promise`. Resultado esperado: Decision Merger deve tentar top-2 ou DEFERRED, nunca enviar top-1.
- Caso de borda 090: **Trace commit falha depois de mensagem pronta**. Feature foco: `safety_guard`. Resultado esperado: pipeline deve impedir envio se ação crítica não é auditável.
- Caso de borda 091: **Cliente declara sem lactose no início e esquece de repetir depois**. Feature foco: `product_recommendation`. Resultado esperado: state persistence deve manter restrição e Evaluator deve bloquear lactose.
- Caso de borda 092: **Cliente muda orçamento de R$ 200 para R$ 120 no meio da conversa**. Feature foco: `contextual_upsell`. Resultado esperado: latest_customer_intent deve atualizar budget transitório e trace deve registrar mudança.
- Caso de borda 093: **Cliente aceita whey, mas recusa creatina explicitamente**. Feature foco: `discount_explanation`. Resultado esperado: offer_history deve bloquear novo upsell de creatina nesta conversa.
- Caso de borda 094: **Cliente pergunta por entrega antes de escolher produto**. Feature foco: `fulfillment_promise`. Resultado esperado: fulfillment feature deve responder disponibilidade geral sem prometer ETA específico.
- Caso de borda 095: **Cliente reclama de cobrança duplicada**. Feature foco: `safety_guard`. Resultado esperado: support intent deve vencer features comerciais no Decision Merger.
- Caso de borda 096: **Catálogo retorna produto sem campo lactose_free**. Feature foco: `product_recommendation`. Resultado esperado: Product Recommendation deve abstêr ou escalar em vez de assumir seguro.
- Caso de borda 097: **Cupom do cliente não é cumulativo com clube**. Feature foco: `contextual_upsell`. Resultado esperado: Discount feature deve aplicar melhor desconto válido e explicar sem confusão.
- Caso de borda 098: **Generator produz três opções, mas uma não tem evidence**. Feature foco: `discount_explanation`. Resultado esperado: Output contract validation deve falhar antes do Evaluator.
- Caso de borda 099: **Evaluator rejeita top-1 por timing ruim**. Feature foco: `fulfillment_promise`. Resultado esperado: Decision Merger deve tentar top-2 ou DEFERRED, nunca enviar top-1.
- Caso de borda 100: **Trace commit falha depois de mensagem pronta**. Feature foco: `safety_guard`. Resultado esperado: pipeline deve impedir envio se ação crítica não é auditável.
- Caso de borda 101: **Cliente declara sem lactose no início e esquece de repetir depois**. Feature foco: `product_recommendation`. Resultado esperado: state persistence deve manter restrição e Evaluator deve bloquear lactose.
- Caso de borda 102: **Cliente muda orçamento de R$ 200 para R$ 120 no meio da conversa**. Feature foco: `contextual_upsell`. Resultado esperado: latest_customer_intent deve atualizar budget transitório e trace deve registrar mudança.
- Caso de borda 103: **Cliente aceita whey, mas recusa creatina explicitamente**. Feature foco: `discount_explanation`. Resultado esperado: offer_history deve bloquear novo upsell de creatina nesta conversa.
- Caso de borda 104: **Cliente pergunta por entrega antes de escolher produto**. Feature foco: `fulfillment_promise`. Resultado esperado: fulfillment feature deve responder disponibilidade geral sem prometer ETA específico.
- Caso de borda 105: **Cliente reclama de cobrança duplicada**. Feature foco: `safety_guard`. Resultado esperado: support intent deve vencer features comerciais no Decision Merger.
- Caso de borda 106: **Catálogo retorna produto sem campo lactose_free**. Feature foco: `product_recommendation`. Resultado esperado: Product Recommendation deve abstêr ou escalar em vez de assumir seguro.
- Caso de borda 107: **Cupom do cliente não é cumulativo com clube**. Feature foco: `contextual_upsell`. Resultado esperado: Discount feature deve aplicar melhor desconto válido e explicar sem confusão.
- Caso de borda 108: **Generator produz três opções, mas uma não tem evidence**. Feature foco: `discount_explanation`. Resultado esperado: Output contract validation deve falhar antes do Evaluator.
- Caso de borda 109: **Evaluator rejeita top-1 por timing ruim**. Feature foco: `fulfillment_promise`. Resultado esperado: Decision Merger deve tentar top-2 ou DEFERRED, nunca enviar top-1.
- Caso de borda 110: **Trace commit falha depois de mensagem pronta**. Feature foco: `safety_guard`. Resultado esperado: pipeline deve impedir envio se ação crítica não é auditável.
- Caso de borda 111: **Cliente declara sem lactose no início e esquece de repetir depois**. Feature foco: `product_recommendation`. Resultado esperado: state persistence deve manter restrição e Evaluator deve bloquear lactose.
- Caso de borda 112: **Cliente muda orçamento de R$ 200 para R$ 120 no meio da conversa**. Feature foco: `contextual_upsell`. Resultado esperado: latest_customer_intent deve atualizar budget transitório e trace deve registrar mudança.
- Caso de borda 113: **Cliente aceita whey, mas recusa creatina explicitamente**. Feature foco: `discount_explanation`. Resultado esperado: offer_history deve bloquear novo upsell de creatina nesta conversa.
- Caso de borda 114: **Cliente pergunta por entrega antes de escolher produto**. Feature foco: `fulfillment_promise`. Resultado esperado: fulfillment feature deve responder disponibilidade geral sem prometer ETA específico.
- Caso de borda 115: **Cliente reclama de cobrança duplicada**. Feature foco: `safety_guard`. Resultado esperado: support intent deve vencer features comerciais no Decision Merger.
- Caso de borda 116: **Catálogo retorna produto sem campo lactose_free**. Feature foco: `product_recommendation`. Resultado esperado: Product Recommendation deve abstêr ou escalar em vez de assumir seguro.
- Caso de borda 117: **Cupom do cliente não é cumulativo com clube**. Feature foco: `contextual_upsell`. Resultado esperado: Discount feature deve aplicar melhor desconto válido e explicar sem confusão.
- Caso de borda 118: **Generator produz três opções, mas uma não tem evidence**. Feature foco: `discount_explanation`. Resultado esperado: Output contract validation deve falhar antes do Evaluator.
- Caso de borda 119: **Evaluator rejeita top-1 por timing ruim**. Feature foco: `fulfillment_promise`. Resultado esperado: Decision Merger deve tentar top-2 ou DEFERRED, nunca enviar top-1.
- Caso de borda 120: **Trace commit falha depois de mensagem pronta**. Feature foco: `safety_guard`. Resultado esperado: pipeline deve impedir envio se ação crítica não é auditável.
- Caso de borda 121: **Cliente declara sem lactose no início e esquece de repetir depois**. Feature foco: `product_recommendation`. Resultado esperado: state persistence deve manter restrição e Evaluator deve bloquear lactose.
- Caso de borda 122: **Cliente muda orçamento de R$ 200 para R$ 120 no meio da conversa**. Feature foco: `contextual_upsell`. Resultado esperado: latest_customer_intent deve atualizar budget transitório e trace deve registrar mudança.
- Caso de borda 123: **Cliente aceita whey, mas recusa creatina explicitamente**. Feature foco: `discount_explanation`. Resultado esperado: offer_history deve bloquear novo upsell de creatina nesta conversa.
- Caso de borda 124: **Cliente pergunta por entrega antes de escolher produto**. Feature foco: `fulfillment_promise`. Resultado esperado: fulfillment feature deve responder disponibilidade geral sem prometer ETA específico.
- Caso de borda 125: **Cliente reclama de cobrança duplicada**. Feature foco: `safety_guard`. Resultado esperado: support intent deve vencer features comerciais no Decision Merger.
- Caso de borda 126: **Catálogo retorna produto sem campo lactose_free**. Feature foco: `product_recommendation`. Resultado esperado: Product Recommendation deve abstêr ou escalar em vez de assumir seguro.
- Caso de borda 127: **Cupom do cliente não é cumulativo com clube**. Feature foco: `contextual_upsell`. Resultado esperado: Discount feature deve aplicar melhor desconto válido e explicar sem confusão.
- Caso de borda 128: **Generator produz três opções, mas uma não tem evidence**. Feature foco: `discount_explanation`. Resultado esperado: Output contract validation deve falhar antes do Evaluator.
- Caso de borda 129: **Evaluator rejeita top-1 por timing ruim**. Feature foco: `fulfillment_promise`. Resultado esperado: Decision Merger deve tentar top-2 ou DEFERRED, nunca enviar top-1.
- Caso de borda 130: **Trace commit falha depois de mensagem pronta**. Feature foco: `safety_guard`. Resultado esperado: pipeline deve impedir envio se ação crítica não é auditável.
- Caso de borda 131: **Cliente declara sem lactose no início e esquece de repetir depois**. Feature foco: `product_recommendation`. Resultado esperado: state persistence deve manter restrição e Evaluator deve bloquear lactose.
- Caso de borda 132: **Cliente muda orçamento de R$ 200 para R$ 120 no meio da conversa**. Feature foco: `contextual_upsell`. Resultado esperado: latest_customer_intent deve atualizar budget transitório e trace deve registrar mudança.
- Caso de borda 133: **Cliente aceita whey, mas recusa creatina explicitamente**. Feature foco: `discount_explanation`. Resultado esperado: offer_history deve bloquear novo upsell de creatina nesta conversa.
- Caso de borda 134: **Cliente pergunta por entrega antes de escolher produto**. Feature foco: `fulfillment_promise`. Resultado esperado: fulfillment feature deve responder disponibilidade geral sem prometer ETA específico.
- Caso de borda 135: **Cliente reclama de cobrança duplicada**. Feature foco: `safety_guard`. Resultado esperado: support intent deve vencer features comerciais no Decision Merger.
- Caso de borda 136: **Catálogo retorna produto sem campo lactose_free**. Feature foco: `product_recommendation`. Resultado esperado: Product Recommendation deve abstêr ou escalar em vez de assumir seguro.
- Caso de borda 137: **Cupom do cliente não é cumulativo com clube**. Feature foco: `contextual_upsell`. Resultado esperado: Discount feature deve aplicar melhor desconto válido e explicar sem confusão.
- Caso de borda 138: **Generator produz três opções, mas uma não tem evidence**. Feature foco: `discount_explanation`. Resultado esperado: Output contract validation deve falhar antes do Evaluator.
- Caso de borda 139: **Evaluator rejeita top-1 por timing ruim**. Feature foco: `fulfillment_promise`. Resultado esperado: Decision Merger deve tentar top-2 ou DEFERRED, nunca enviar top-1.
- Caso de borda 140: **Trace commit falha depois de mensagem pronta**. Feature foco: `safety_guard`. Resultado esperado: pipeline deve impedir envio se ação crítica não é auditável.
- Caso de borda 141: **Cliente declara sem lactose no início e esquece de repetir depois**. Feature foco: `product_recommendation`. Resultado esperado: state persistence deve manter restrição e Evaluator deve bloquear lactose.
- Caso de borda 142: **Cliente muda orçamento de R$ 200 para R$ 120 no meio da conversa**. Feature foco: `contextual_upsell`. Resultado esperado: latest_customer_intent deve atualizar budget transitório e trace deve registrar mudança.
- Caso de borda 143: **Cliente aceita whey, mas recusa creatina explicitamente**. Feature foco: `discount_explanation`. Resultado esperado: offer_history deve bloquear novo upsell de creatina nesta conversa.
- Caso de borda 144: **Cliente pergunta por entrega antes de escolher produto**. Feature foco: `fulfillment_promise`. Resultado esperado: fulfillment feature deve responder disponibilidade geral sem prometer ETA específico.
- Caso de borda 145: **Cliente reclama de cobrança duplicada**. Feature foco: `safety_guard`. Resultado esperado: support intent deve vencer features comerciais no Decision Merger.
- Caso de borda 146: **Catálogo retorna produto sem campo lactose_free**. Feature foco: `product_recommendation`. Resultado esperado: Product Recommendation deve abstêr ou escalar em vez de assumir seguro.
- Caso de borda 147: **Cupom do cliente não é cumulativo com clube**. Feature foco: `contextual_upsell`. Resultado esperado: Discount feature deve aplicar melhor desconto válido e explicar sem confusão.
- Caso de borda 148: **Generator produz três opções, mas uma não tem evidence**. Feature foco: `discount_explanation`. Resultado esperado: Output contract validation deve falhar antes do Evaluator.
- Caso de borda 149: **Evaluator rejeita top-1 por timing ruim**. Feature foco: `fulfillment_promise`. Resultado esperado: Decision Merger deve tentar top-2 ou DEFERRED, nunca enviar top-1.
- Caso de borda 150: **Trace commit falha depois de mensagem pronta**. Feature foco: `safety_guard`. Resultado esperado: pipeline deve impedir envio se ação crítica não é auditável.
- Caso de borda 151: **Cliente declara sem lactose no início e esquece de repetir depois**. Feature foco: `product_recommendation`. Resultado esperado: state persistence deve manter restrição e Evaluator deve bloquear lactose.
- Caso de borda 152: **Cliente muda orçamento de R$ 200 para R$ 120 no meio da conversa**. Feature foco: `contextual_upsell`. Resultado esperado: latest_customer_intent deve atualizar budget transitório e trace deve registrar mudança.
- Caso de borda 153: **Cliente aceita whey, mas recusa creatina explicitamente**. Feature foco: `discount_explanation`. Resultado esperado: offer_history deve bloquear novo upsell de creatina nesta conversa.
- Caso de borda 154: **Cliente pergunta por entrega antes de escolher produto**. Feature foco: `fulfillment_promise`. Resultado esperado: fulfillment feature deve responder disponibilidade geral sem prometer ETA específico.
- Caso de borda 155: **Cliente reclama de cobrança duplicada**. Feature foco: `safety_guard`. Resultado esperado: support intent deve vencer features comerciais no Decision Merger.
- Caso de borda 156: **Catálogo retorna produto sem campo lactose_free**. Feature foco: `product_recommendation`. Resultado esperado: Product Recommendation deve abstêr ou escalar em vez de assumir seguro.
- Caso de borda 157: **Cupom do cliente não é cumulativo com clube**. Feature foco: `contextual_upsell`. Resultado esperado: Discount feature deve aplicar melhor desconto válido e explicar sem confusão.
- Caso de borda 158: **Generator produz três opções, mas uma não tem evidence**. Feature foco: `discount_explanation`. Resultado esperado: Output contract validation deve falhar antes do Evaluator.
- Caso de borda 159: **Evaluator rejeita top-1 por timing ruim**. Feature foco: `fulfillment_promise`. Resultado esperado: Decision Merger deve tentar top-2 ou DEFERRED, nunca enviar top-1.
- Caso de borda 160: **Trace commit falha depois de mensagem pronta**. Feature foco: `safety_guard`. Resultado esperado: pipeline deve impedir envio se ação crítica não é auditável.
- Caso de borda 161: **Cliente declara sem lactose no início e esquece de repetir depois**. Feature foco: `product_recommendation`. Resultado esperado: state persistence deve manter restrição e Evaluator deve bloquear lactose.
- Caso de borda 162: **Cliente muda orçamento de R$ 200 para R$ 120 no meio da conversa**. Feature foco: `contextual_upsell`. Resultado esperado: latest_customer_intent deve atualizar budget transitório e trace deve registrar mudança.
- Caso de borda 163: **Cliente aceita whey, mas recusa creatina explicitamente**. Feature foco: `discount_explanation`. Resultado esperado: offer_history deve bloquear novo upsell de creatina nesta conversa.
- Caso de borda 164: **Cliente pergunta por entrega antes de escolher produto**. Feature foco: `fulfillment_promise`. Resultado esperado: fulfillment feature deve responder disponibilidade geral sem prometer ETA específico.
- Caso de borda 165: **Cliente reclama de cobrança duplicada**. Feature foco: `safety_guard`. Resultado esperado: support intent deve vencer features comerciais no Decision Merger.
- Caso de borda 166: **Catálogo retorna produto sem campo lactose_free**. Feature foco: `product_recommendation`. Resultado esperado: Product Recommendation deve abstêr ou escalar em vez de assumir seguro.
- Caso de borda 167: **Cupom do cliente não é cumulativo com clube**. Feature foco: `contextual_upsell`. Resultado esperado: Discount feature deve aplicar melhor desconto válido e explicar sem confusão.
- Caso de borda 168: **Generator produz três opções, mas uma não tem evidence**. Feature foco: `discount_explanation`. Resultado esperado: Output contract validation deve falhar antes do Evaluator.
- Caso de borda 169: **Evaluator rejeita top-1 por timing ruim**. Feature foco: `fulfillment_promise`. Resultado esperado: Decision Merger deve tentar top-2 ou DEFERRED, nunca enviar top-1.
- Caso de borda 170: **Trace commit falha depois de mensagem pronta**. Feature foco: `safety_guard`. Resultado esperado: pipeline deve impedir envio se ação crítica não é auditável.
- Caso de borda 171: **Cliente declara sem lactose no início e esquece de repetir depois**. Feature foco: `product_recommendation`. Resultado esperado: state persistence deve manter restrição e Evaluator deve bloquear lactose.
- Caso de borda 172: **Cliente muda orçamento de R$ 200 para R$ 120 no meio da conversa**. Feature foco: `contextual_upsell`. Resultado esperado: latest_customer_intent deve atualizar budget transitório e trace deve registrar mudança.
- Caso de borda 173: **Cliente aceita whey, mas recusa creatina explicitamente**. Feature foco: `discount_explanation`. Resultado esperado: offer_history deve bloquear novo upsell de creatina nesta conversa.
- Caso de borda 174: **Cliente pergunta por entrega antes de escolher produto**. Feature foco: `fulfillment_promise`. Resultado esperado: fulfillment feature deve responder disponibilidade geral sem prometer ETA específico.
- Caso de borda 175: **Cliente reclama de cobrança duplicada**. Feature foco: `safety_guard`. Resultado esperado: support intent deve vencer features comerciais no Decision Merger.
- Caso de borda 176: **Catálogo retorna produto sem campo lactose_free**. Feature foco: `product_recommendation`. Resultado esperado: Product Recommendation deve abstêr ou escalar em vez de assumir seguro.
- Caso de borda 177: **Cupom do cliente não é cumulativo com clube**. Feature foco: `contextual_upsell`. Resultado esperado: Discount feature deve aplicar melhor desconto válido e explicar sem confusão.
- Caso de borda 178: **Generator produz três opções, mas uma não tem evidence**. Feature foco: `discount_explanation`. Resultado esperado: Output contract validation deve falhar antes do Evaluator.
- Caso de borda 179: **Evaluator rejeita top-1 por timing ruim**. Feature foco: `fulfillment_promise`. Resultado esperado: Decision Merger deve tentar top-2 ou DEFERRED, nunca enviar top-1.
- Caso de borda 180: **Trace commit falha depois de mensagem pronta**. Feature foco: `safety_guard`. Resultado esperado: pipeline deve impedir envio se ação crítica não é auditável.
- Caso de borda 181: **Cliente declara sem lactose no início e esquece de repetir depois**. Feature foco: `product_recommendation`. Resultado esperado: state persistence deve manter restrição e Evaluator deve bloquear lactose.
- Caso de borda 182: **Cliente muda orçamento de R$ 200 para R$ 120 no meio da conversa**. Feature foco: `contextual_upsell`. Resultado esperado: latest_customer_intent deve atualizar budget transitório e trace deve registrar mudança.
- Caso de borda 183: **Cliente aceita whey, mas recusa creatina explicitamente**. Feature foco: `discount_explanation`. Resultado esperado: offer_history deve bloquear novo upsell de creatina nesta conversa.
- Caso de borda 184: **Cliente pergunta por entrega antes de escolher produto**. Feature foco: `fulfillment_promise`. Resultado esperado: fulfillment feature deve responder disponibilidade geral sem prometer ETA específico.
- Caso de borda 185: **Cliente reclama de cobrança duplicada**. Feature foco: `safety_guard`. Resultado esperado: support intent deve vencer features comerciais no Decision Merger.
- Caso de borda 186: **Catálogo retorna produto sem campo lactose_free**. Feature foco: `product_recommendation`. Resultado esperado: Product Recommendation deve abstêr ou escalar em vez de assumir seguro.
- Caso de borda 187: **Cupom do cliente não é cumulativo com clube**. Feature foco: `contextual_upsell`. Resultado esperado: Discount feature deve aplicar melhor desconto válido e explicar sem confusão.
- Caso de borda 188: **Generator produz três opções, mas uma não tem evidence**. Feature foco: `discount_explanation`. Resultado esperado: Output contract validation deve falhar antes do Evaluator.
- Caso de borda 189: **Evaluator rejeita top-1 por timing ruim**. Feature foco: `fulfillment_promise`. Resultado esperado: Decision Merger deve tentar top-2 ou DEFERRED, nunca enviar top-1.
- Caso de borda 190: **Trace commit falha depois de mensagem pronta**. Feature foco: `safety_guard`. Resultado esperado: pipeline deve impedir envio se ação crítica não é auditável.
- Caso de borda 191: **Cliente declara sem lactose no início e esquece de repetir depois**. Feature foco: `product_recommendation`. Resultado esperado: state persistence deve manter restrição e Evaluator deve bloquear lactose.
- Caso de borda 192: **Cliente muda orçamento de R$ 200 para R$ 120 no meio da conversa**. Feature foco: `contextual_upsell`. Resultado esperado: latest_customer_intent deve atualizar budget transitório e trace deve registrar mudança.
- Caso de borda 193: **Cliente aceita whey, mas recusa creatina explicitamente**. Feature foco: `discount_explanation`. Resultado esperado: offer_history deve bloquear novo upsell de creatina nesta conversa.
- Caso de borda 194: **Cliente pergunta por entrega antes de escolher produto**. Feature foco: `fulfillment_promise`. Resultado esperado: fulfillment feature deve responder disponibilidade geral sem prometer ETA específico.
- Caso de borda 195: **Cliente reclama de cobrança duplicada**. Feature foco: `safety_guard`. Resultado esperado: support intent deve vencer features comerciais no Decision Merger.
- Caso de borda 196: **Catálogo retorna produto sem campo lactose_free**. Feature foco: `product_recommendation`. Resultado esperado: Product Recommendation deve abstêr ou escalar em vez de assumir seguro.
- Caso de borda 197: **Cupom do cliente não é cumulativo com clube**. Feature foco: `contextual_upsell`. Resultado esperado: Discount feature deve aplicar melhor desconto válido e explicar sem confusão.
- Caso de borda 198: **Generator produz três opções, mas uma não tem evidence**. Feature foco: `discount_explanation`. Resultado esperado: Output contract validation deve falhar antes do Evaluator.
- Caso de borda 199: **Evaluator rejeita top-1 por timing ruim**. Feature foco: `fulfillment_promise`. Resultado esperado: Decision Merger deve tentar top-2 ou DEFERRED, nunca enviar top-1.
- Caso de borda 200: **Trace commit falha depois de mensagem pronta**. Feature foco: `safety_guard`. Resultado esperado: pipeline deve impedir envio se ação crítica não é auditável.
- Caso de borda 201: **Cliente declara sem lactose no início e esquece de repetir depois**. Feature foco: `product_recommendation`. Resultado esperado: state persistence deve manter restrição e Evaluator deve bloquear lactose.
- Caso de borda 202: **Cliente muda orçamento de R$ 200 para R$ 120 no meio da conversa**. Feature foco: `contextual_upsell`. Resultado esperado: latest_customer_intent deve atualizar budget transitório e trace deve registrar mudança.
- Caso de borda 203: **Cliente aceita whey, mas recusa creatina explicitamente**. Feature foco: `discount_explanation`. Resultado esperado: offer_history deve bloquear novo upsell de creatina nesta conversa.
- Caso de borda 204: **Cliente pergunta por entrega antes de escolher produto**. Feature foco: `fulfillment_promise`. Resultado esperado: fulfillment feature deve responder disponibilidade geral sem prometer ETA específico.
- Caso de borda 205: **Cliente reclama de cobrança duplicada**. Feature foco: `safety_guard`. Resultado esperado: support intent deve vencer features comerciais no Decision Merger.
- Caso de borda 206: **Catálogo retorna produto sem campo lactose_free**. Feature foco: `product_recommendation`. Resultado esperado: Product Recommendation deve abstêr ou escalar em vez de assumir seguro.
- Caso de borda 207: **Cupom do cliente não é cumulativo com clube**. Feature foco: `contextual_upsell`. Resultado esperado: Discount feature deve aplicar melhor desconto válido e explicar sem confusão.
- Caso de borda 208: **Generator produz três opções, mas uma não tem evidence**. Feature foco: `discount_explanation`. Resultado esperado: Output contract validation deve falhar antes do Evaluator.
- Caso de borda 209: **Evaluator rejeita top-1 por timing ruim**. Feature foco: `fulfillment_promise`. Resultado esperado: Decision Merger deve tentar top-2 ou DEFERRED, nunca enviar top-1.
- Caso de borda 210: **Trace commit falha depois de mensagem pronta**. Feature foco: `safety_guard`. Resultado esperado: pipeline deve impedir envio se ação crítica não é auditável.
- Caso de borda 211: **Cliente declara sem lactose no início e esquece de repetir depois**. Feature foco: `product_recommendation`. Resultado esperado: state persistence deve manter restrição e Evaluator deve bloquear lactose.
- Caso de borda 212: **Cliente muda orçamento de R$ 200 para R$ 120 no meio da conversa**. Feature foco: `contextual_upsell`. Resultado esperado: latest_customer_intent deve atualizar budget transitório e trace deve registrar mudança.
- Caso de borda 213: **Cliente aceita whey, mas recusa creatina explicitamente**. Feature foco: `discount_explanation`. Resultado esperado: offer_history deve bloquear novo upsell de creatina nesta conversa.
- Caso de borda 214: **Cliente pergunta por entrega antes de escolher produto**. Feature foco: `fulfillment_promise`. Resultado esperado: fulfillment feature deve responder disponibilidade geral sem prometer ETA específico.
- Caso de borda 215: **Cliente reclama de cobrança duplicada**. Feature foco: `safety_guard`. Resultado esperado: support intent deve vencer features comerciais no Decision Merger.
- Caso de borda 216: **Catálogo retorna produto sem campo lactose_free**. Feature foco: `product_recommendation`. Resultado esperado: Product Recommendation deve abstêr ou escalar em vez de assumir seguro.
- Caso de borda 217: **Cupom do cliente não é cumulativo com clube**. Feature foco: `contextual_upsell`. Resultado esperado: Discount feature deve aplicar melhor desconto válido e explicar sem confusão.
- Caso de borda 218: **Generator produz três opções, mas uma não tem evidence**. Feature foco: `discount_explanation`. Resultado esperado: Output contract validation deve falhar antes do Evaluator.
- Caso de borda 219: **Evaluator rejeita top-1 por timing ruim**. Feature foco: `fulfillment_promise`. Resultado esperado: Decision Merger deve tentar top-2 ou DEFERRED, nunca enviar top-1.
- Caso de borda 220: **Trace commit falha depois de mensagem pronta**. Feature foco: `safety_guard`. Resultado esperado: pipeline deve impedir envio se ação crítica não é auditável.
### Frases de Feedback Úteis do Evaluator
- Feedback Evaluator 001: `RESTRICTION_CONFLICT` — Remova o SKU porque ele viola uma restrição persistida do cliente.
- Feedback Evaluator 002: `STALE_CATALOG_SNAPSHOT` — Atualize o catalog_snapshot antes de gerar nova proposta.
- Feedback Evaluator 003: `PRICE_OBJECTION_RECENT` — Adie o upsell porque houve objeção de preço nos últimos turnos.
- Feedback Evaluator 004: `MISSING_EVIDENCE` — Inclua evidence para cada claim sobre preço, estoque ou compatibilidade.
- Feedback Evaluator 005: `MESSAGE_TOO_LONG` — Reduza a mensagem para caber em leitura rápida de WhatsApp.
- Feedback Evaluator 006: `REPEATED_OFFER` — Não repita oferta recusada sem mudança objetiva de contexto.
- Feedback Evaluator 007: `UNMAPPED_HEALTH_RISK` — Escale para humano porque a condição informada não está mapeada no catálogo.
- Feedback Evaluator 008: `LOW_GOAL_FIT` — Substitua o produto por opção mais alinhada ao objetivo declarado.
- Feedback Evaluator 009: `WEAK_TIMING` — Marque DEFERRED e tente novamente após avanço na jornada.
- Feedback Evaluator 010: `STATE_COMMIT_RISK` — Separe state_updates propostos de commits aprovados.
- Feedback Evaluator 011: `RESTRICTION_CONFLICT` — Remova o SKU porque ele viola uma restrição persistida do cliente.
- Feedback Evaluator 012: `STALE_CATALOG_SNAPSHOT` — Atualize o catalog_snapshot antes de gerar nova proposta.
- Feedback Evaluator 013: `PRICE_OBJECTION_RECENT` — Adie o upsell porque houve objeção de preço nos últimos turnos.
- Feedback Evaluator 014: `MISSING_EVIDENCE` — Inclua evidence para cada claim sobre preço, estoque ou compatibilidade.
- Feedback Evaluator 015: `MESSAGE_TOO_LONG` — Reduza a mensagem para caber em leitura rápida de WhatsApp.
- Feedback Evaluator 016: `REPEATED_OFFER` — Não repita oferta recusada sem mudança objetiva de contexto.
- Feedback Evaluator 017: `UNMAPPED_HEALTH_RISK` — Escale para humano porque a condição informada não está mapeada no catálogo.
- Feedback Evaluator 018: `LOW_GOAL_FIT` — Substitua o produto por opção mais alinhada ao objetivo declarado.
- Feedback Evaluator 019: `WEAK_TIMING` — Marque DEFERRED e tente novamente após avanço na jornada.
- Feedback Evaluator 020: `STATE_COMMIT_RISK` — Separe state_updates propostos de commits aprovados.
- Feedback Evaluator 021: `RESTRICTION_CONFLICT` — Remova o SKU porque ele viola uma restrição persistida do cliente.
- Feedback Evaluator 022: `STALE_CATALOG_SNAPSHOT` — Atualize o catalog_snapshot antes de gerar nova proposta.
- Feedback Evaluator 023: `PRICE_OBJECTION_RECENT` — Adie o upsell porque houve objeção de preço nos últimos turnos.
- Feedback Evaluator 024: `MISSING_EVIDENCE` — Inclua evidence para cada claim sobre preço, estoque ou compatibilidade.
- Feedback Evaluator 025: `MESSAGE_TOO_LONG` — Reduza a mensagem para caber em leitura rápida de WhatsApp.
- Feedback Evaluator 026: `REPEATED_OFFER` — Não repita oferta recusada sem mudança objetiva de contexto.
- Feedback Evaluator 027: `UNMAPPED_HEALTH_RISK` — Escale para humano porque a condição informada não está mapeada no catálogo.
- Feedback Evaluator 028: `LOW_GOAL_FIT` — Substitua o produto por opção mais alinhada ao objetivo declarado.
- Feedback Evaluator 029: `WEAK_TIMING` — Marque DEFERRED e tente novamente após avanço na jornada.
- Feedback Evaluator 030: `STATE_COMMIT_RISK` — Separe state_updates propostos de commits aprovados.
- Feedback Evaluator 031: `RESTRICTION_CONFLICT` — Remova o SKU porque ele viola uma restrição persistida do cliente.
- Feedback Evaluator 032: `STALE_CATALOG_SNAPSHOT` — Atualize o catalog_snapshot antes de gerar nova proposta.
- Feedback Evaluator 033: `PRICE_OBJECTION_RECENT` — Adie o upsell porque houve objeção de preço nos últimos turnos.
- Feedback Evaluator 034: `MISSING_EVIDENCE` — Inclua evidence para cada claim sobre preço, estoque ou compatibilidade.
- Feedback Evaluator 035: `MESSAGE_TOO_LONG` — Reduza a mensagem para caber em leitura rápida de WhatsApp.
- Feedback Evaluator 036: `REPEATED_OFFER` — Não repita oferta recusada sem mudança objetiva de contexto.
- Feedback Evaluator 037: `UNMAPPED_HEALTH_RISK` — Escale para humano porque a condição informada não está mapeada no catálogo.
- Feedback Evaluator 038: `LOW_GOAL_FIT` — Substitua o produto por opção mais alinhada ao objetivo declarado.
- Feedback Evaluator 039: `WEAK_TIMING` — Marque DEFERRED e tente novamente após avanço na jornada.
- Feedback Evaluator 040: `STATE_COMMIT_RISK` — Separe state_updates propostos de commits aprovados.
- Feedback Evaluator 041: `RESTRICTION_CONFLICT` — Remova o SKU porque ele viola uma restrição persistida do cliente.
- Feedback Evaluator 042: `STALE_CATALOG_SNAPSHOT` — Atualize o catalog_snapshot antes de gerar nova proposta.
- Feedback Evaluator 043: `PRICE_OBJECTION_RECENT` — Adie o upsell porque houve objeção de preço nos últimos turnos.
- Feedback Evaluator 044: `MISSING_EVIDENCE` — Inclua evidence para cada claim sobre preço, estoque ou compatibilidade.
- Feedback Evaluator 045: `MESSAGE_TOO_LONG` — Reduza a mensagem para caber em leitura rápida de WhatsApp.
- Feedback Evaluator 046: `REPEATED_OFFER` — Não repita oferta recusada sem mudança objetiva de contexto.
- Feedback Evaluator 047: `UNMAPPED_HEALTH_RISK` — Escale para humano porque a condição informada não está mapeada no catálogo.
- Feedback Evaluator 048: `LOW_GOAL_FIT` — Substitua o produto por opção mais alinhada ao objetivo declarado.
- Feedback Evaluator 049: `WEAK_TIMING` — Marque DEFERRED e tente novamente após avanço na jornada.
- Feedback Evaluator 050: `STATE_COMMIT_RISK` — Separe state_updates propostos de commits aprovados.
- Feedback Evaluator 051: `RESTRICTION_CONFLICT` — Remova o SKU porque ele viola uma restrição persistida do cliente.
- Feedback Evaluator 052: `STALE_CATALOG_SNAPSHOT` — Atualize o catalog_snapshot antes de gerar nova proposta.
- Feedback Evaluator 053: `PRICE_OBJECTION_RECENT` — Adie o upsell porque houve objeção de preço nos últimos turnos.
- Feedback Evaluator 054: `MISSING_EVIDENCE` — Inclua evidence para cada claim sobre preço, estoque ou compatibilidade.
- Feedback Evaluator 055: `MESSAGE_TOO_LONG` — Reduza a mensagem para caber em leitura rápida de WhatsApp.
- Feedback Evaluator 056: `REPEATED_OFFER` — Não repita oferta recusada sem mudança objetiva de contexto.
- Feedback Evaluator 057: `UNMAPPED_HEALTH_RISK` — Escale para humano porque a condição informada não está mapeada no catálogo.
- Feedback Evaluator 058: `LOW_GOAL_FIT` — Substitua o produto por opção mais alinhada ao objetivo declarado.
- Feedback Evaluator 059: `WEAK_TIMING` — Marque DEFERRED e tente novamente após avanço na jornada.
- Feedback Evaluator 060: `STATE_COMMIT_RISK` — Separe state_updates propostos de commits aprovados.
- Feedback Evaluator 061: `RESTRICTION_CONFLICT` — Remova o SKU porque ele viola uma restrição persistida do cliente.
- Feedback Evaluator 062: `STALE_CATALOG_SNAPSHOT` — Atualize o catalog_snapshot antes de gerar nova proposta.
- Feedback Evaluator 063: `PRICE_OBJECTION_RECENT` — Adie o upsell porque houve objeção de preço nos últimos turnos.
- Feedback Evaluator 064: `MISSING_EVIDENCE` — Inclua evidence para cada claim sobre preço, estoque ou compatibilidade.
- Feedback Evaluator 065: `MESSAGE_TOO_LONG` — Reduza a mensagem para caber em leitura rápida de WhatsApp.
- Feedback Evaluator 066: `REPEATED_OFFER` — Não repita oferta recusada sem mudança objetiva de contexto.
- Feedback Evaluator 067: `UNMAPPED_HEALTH_RISK` — Escale para humano porque a condição informada não está mapeada no catálogo.
- Feedback Evaluator 068: `LOW_GOAL_FIT` — Substitua o produto por opção mais alinhada ao objetivo declarado.
- Feedback Evaluator 069: `WEAK_TIMING` — Marque DEFERRED e tente novamente após avanço na jornada.
- Feedback Evaluator 070: `STATE_COMMIT_RISK` — Separe state_updates propostos de commits aprovados.
- Feedback Evaluator 071: `RESTRICTION_CONFLICT` — Remova o SKU porque ele viola uma restrição persistida do cliente.
- Feedback Evaluator 072: `STALE_CATALOG_SNAPSHOT` — Atualize o catalog_snapshot antes de gerar nova proposta.
- Feedback Evaluator 073: `PRICE_OBJECTION_RECENT` — Adie o upsell porque houve objeção de preço nos últimos turnos.
- Feedback Evaluator 074: `MISSING_EVIDENCE` — Inclua evidence para cada claim sobre preço, estoque ou compatibilidade.
- Feedback Evaluator 075: `MESSAGE_TOO_LONG` — Reduza a mensagem para caber em leitura rápida de WhatsApp.
- Feedback Evaluator 076: `REPEATED_OFFER` — Não repita oferta recusada sem mudança objetiva de contexto.
- Feedback Evaluator 077: `UNMAPPED_HEALTH_RISK` — Escale para humano porque a condição informada não está mapeada no catálogo.
- Feedback Evaluator 078: `LOW_GOAL_FIT` — Substitua o produto por opção mais alinhada ao objetivo declarado.
- Feedback Evaluator 079: `WEAK_TIMING` — Marque DEFERRED e tente novamente após avanço na jornada.
- Feedback Evaluator 080: `STATE_COMMIT_RISK` — Separe state_updates propostos de commits aprovados.
- Feedback Evaluator 081: `RESTRICTION_CONFLICT` — Remova o SKU porque ele viola uma restrição persistida do cliente.
- Feedback Evaluator 082: `STALE_CATALOG_SNAPSHOT` — Atualize o catalog_snapshot antes de gerar nova proposta.
- Feedback Evaluator 083: `PRICE_OBJECTION_RECENT` — Adie o upsell porque houve objeção de preço nos últimos turnos.
- Feedback Evaluator 084: `MISSING_EVIDENCE` — Inclua evidence para cada claim sobre preço, estoque ou compatibilidade.
- Feedback Evaluator 085: `MESSAGE_TOO_LONG` — Reduza a mensagem para caber em leitura rápida de WhatsApp.
- Feedback Evaluator 086: `REPEATED_OFFER` — Não repita oferta recusada sem mudança objetiva de contexto.
- Feedback Evaluator 087: `UNMAPPED_HEALTH_RISK` — Escale para humano porque a condição informada não está mapeada no catálogo.
- Feedback Evaluator 088: `LOW_GOAL_FIT` — Substitua o produto por opção mais alinhada ao objetivo declarado.
- Feedback Evaluator 089: `WEAK_TIMING` — Marque DEFERRED e tente novamente após avanço na jornada.
- Feedback Evaluator 090: `STATE_COMMIT_RISK` — Separe state_updates propostos de commits aprovados.
- Feedback Evaluator 091: `RESTRICTION_CONFLICT` — Remova o SKU porque ele viola uma restrição persistida do cliente.
- Feedback Evaluator 092: `STALE_CATALOG_SNAPSHOT` — Atualize o catalog_snapshot antes de gerar nova proposta.
- Feedback Evaluator 093: `PRICE_OBJECTION_RECENT` — Adie o upsell porque houve objeção de preço nos últimos turnos.
- Feedback Evaluator 094: `MISSING_EVIDENCE` — Inclua evidence para cada claim sobre preço, estoque ou compatibilidade.
- Feedback Evaluator 095: `MESSAGE_TOO_LONG` — Reduza a mensagem para caber em leitura rápida de WhatsApp.
- Feedback Evaluator 096: `REPEATED_OFFER` — Não repita oferta recusada sem mudança objetiva de contexto.
- Feedback Evaluator 097: `UNMAPPED_HEALTH_RISK` — Escale para humano porque a condição informada não está mapeada no catálogo.
- Feedback Evaluator 098: `LOW_GOAL_FIT` — Substitua o produto por opção mais alinhada ao objetivo declarado.
- Feedback Evaluator 099: `WEAK_TIMING` — Marque DEFERRED e tente novamente após avanço na jornada.
- Feedback Evaluator 100: `STATE_COMMIT_RISK` — Separe state_updates propostos de commits aprovados.
- Feedback Evaluator 101: `RESTRICTION_CONFLICT` — Remova o SKU porque ele viola uma restrição persistida do cliente.
- Feedback Evaluator 102: `STALE_CATALOG_SNAPSHOT` — Atualize o catalog_snapshot antes de gerar nova proposta.
- Feedback Evaluator 103: `PRICE_OBJECTION_RECENT` — Adie o upsell porque houve objeção de preço nos últimos turnos.
- Feedback Evaluator 104: `MISSING_EVIDENCE` — Inclua evidence para cada claim sobre preço, estoque ou compatibilidade.
- Feedback Evaluator 105: `MESSAGE_TOO_LONG` — Reduza a mensagem para caber em leitura rápida de WhatsApp.
- Feedback Evaluator 106: `REPEATED_OFFER` — Não repita oferta recusada sem mudança objetiva de contexto.
- Feedback Evaluator 107: `UNMAPPED_HEALTH_RISK` — Escale para humano porque a condição informada não está mapeada no catálogo.
- Feedback Evaluator 108: `LOW_GOAL_FIT` — Substitua o produto por opção mais alinhada ao objetivo declarado.
- Feedback Evaluator 109: `WEAK_TIMING` — Marque DEFERRED e tente novamente após avanço na jornada.
- Feedback Evaluator 110: `STATE_COMMIT_RISK` — Separe state_updates propostos de commits aprovados.
- Feedback Evaluator 111: `RESTRICTION_CONFLICT` — Remova o SKU porque ele viola uma restrição persistida do cliente.
- Feedback Evaluator 112: `STALE_CATALOG_SNAPSHOT` — Atualize o catalog_snapshot antes de gerar nova proposta.
- Feedback Evaluator 113: `PRICE_OBJECTION_RECENT` — Adie o upsell porque houve objeção de preço nos últimos turnos.
- Feedback Evaluator 114: `MISSING_EVIDENCE` — Inclua evidence para cada claim sobre preço, estoque ou compatibilidade.
- Feedback Evaluator 115: `MESSAGE_TOO_LONG` — Reduza a mensagem para caber em leitura rápida de WhatsApp.
- Feedback Evaluator 116: `REPEATED_OFFER` — Não repita oferta recusada sem mudança objetiva de contexto.
- Feedback Evaluator 117: `UNMAPPED_HEALTH_RISK` — Escale para humano porque a condição informada não está mapeada no catálogo.
- Feedback Evaluator 118: `LOW_GOAL_FIT` — Substitua o produto por opção mais alinhada ao objetivo declarado.
- Feedback Evaluator 119: `WEAK_TIMING` — Marque DEFERRED e tente novamente após avanço na jornada.
- Feedback Evaluator 120: `STATE_COMMIT_RISK` — Separe state_updates propostos de commits aprovados.
- Feedback Evaluator 121: `RESTRICTION_CONFLICT` — Remova o SKU porque ele viola uma restrição persistida do cliente.
- Feedback Evaluator 122: `STALE_CATALOG_SNAPSHOT` — Atualize o catalog_snapshot antes de gerar nova proposta.
- Feedback Evaluator 123: `PRICE_OBJECTION_RECENT` — Adie o upsell porque houve objeção de preço nos últimos turnos.
- Feedback Evaluator 124: `MISSING_EVIDENCE` — Inclua evidence para cada claim sobre preço, estoque ou compatibilidade.
- Feedback Evaluator 125: `MESSAGE_TOO_LONG` — Reduza a mensagem para caber em leitura rápida de WhatsApp.
- Feedback Evaluator 126: `REPEATED_OFFER` — Não repita oferta recusada sem mudança objetiva de contexto.
- Feedback Evaluator 127: `UNMAPPED_HEALTH_RISK` — Escale para humano porque a condição informada não está mapeada no catálogo.
- Feedback Evaluator 128: `LOW_GOAL_FIT` — Substitua o produto por opção mais alinhada ao objetivo declarado.
- Feedback Evaluator 129: `WEAK_TIMING` — Marque DEFERRED e tente novamente após avanço na jornada.
- Feedback Evaluator 130: `STATE_COMMIT_RISK` — Separe state_updates propostos de commits aprovados.
- Feedback Evaluator 131: `RESTRICTION_CONFLICT` — Remova o SKU porque ele viola uma restrição persistida do cliente.
- Feedback Evaluator 132: `STALE_CATALOG_SNAPSHOT` — Atualize o catalog_snapshot antes de gerar nova proposta.
- Feedback Evaluator 133: `PRICE_OBJECTION_RECENT` — Adie o upsell porque houve objeção de preço nos últimos turnos.
- Feedback Evaluator 134: `MISSING_EVIDENCE` — Inclua evidence para cada claim sobre preço, estoque ou compatibilidade.
- Feedback Evaluator 135: `MESSAGE_TOO_LONG` — Reduza a mensagem para caber em leitura rápida de WhatsApp.
- Feedback Evaluator 136: `REPEATED_OFFER` — Não repita oferta recusada sem mudança objetiva de contexto.
- Feedback Evaluator 137: `UNMAPPED_HEALTH_RISK` — Escale para humano porque a condição informada não está mapeada no catálogo.
- Feedback Evaluator 138: `LOW_GOAL_FIT` — Substitua o produto por opção mais alinhada ao objetivo declarado.
- Feedback Evaluator 139: `WEAK_TIMING` — Marque DEFERRED e tente novamente após avanço na jornada.
- Feedback Evaluator 140: `STATE_COMMIT_RISK` — Separe state_updates propostos de commits aprovados.
### Métricas de Produção por Feature
- Métrica 001: **Product Recommendation** acompanha `recommendation_accuracy`; mede se produto recomendado foi aceito sem devolução ou reclamação.
- Métrica 002: **Product Recommendation** acompanha `restriction_violation_rate`; deve permanecer em zero para restrições críticas.
- Métrica 003: **Contextual Upsell** acompanha `attach_rate`; mede aceitação de complemento sem confundir com pressão comercial.
- Métrica 004: **Contextual Upsell** acompanha `upsell_complaint_rate`; alerta quando growth começa a ferir confiança.
- Métrica 005: **Discount Explanation** acompanha `price_mismatch_rate`; mede diferença entre preço explicado e preço cobrado.
- Métrica 006: **Fulfillment Promise** acompanha `eta_accuracy`; mede promessa de entrega contra entrega real.
- Métrica 007: **Safety Guard** acompanha `human_review_rate`; mede quantos casos ambíguos exigiram humano.
- Métrica 008: **Cart Reengagement** acompanha `helpful_return_rate`; mede retorno útil sem sensação de perseguição.
- Métrica 009: **All Features** acompanha `trace_completeness`; mede decisões com replay possível.
- Métrica 010: **All Features** acompanha `first_pass_approval_rate`; mede qualidade inicial do Generator.
- Métrica 011: **Product Recommendation** acompanha `recommendation_accuracy`; mede se produto recomendado foi aceito sem devolução ou reclamação.
- Métrica 012: **Product Recommendation** acompanha `restriction_violation_rate`; deve permanecer em zero para restrições críticas.
- Métrica 013: **Contextual Upsell** acompanha `attach_rate`; mede aceitação de complemento sem confundir com pressão comercial.
- Métrica 014: **Contextual Upsell** acompanha `upsell_complaint_rate`; alerta quando growth começa a ferir confiança.
- Métrica 015: **Discount Explanation** acompanha `price_mismatch_rate`; mede diferença entre preço explicado e preço cobrado.
- Métrica 016: **Fulfillment Promise** acompanha `eta_accuracy`; mede promessa de entrega contra entrega real.
- Métrica 017: **Safety Guard** acompanha `human_review_rate`; mede quantos casos ambíguos exigiram humano.
- Métrica 018: **Cart Reengagement** acompanha `helpful_return_rate`; mede retorno útil sem sensação de perseguição.
- Métrica 019: **All Features** acompanha `trace_completeness`; mede decisões com replay possível.
- Métrica 020: **All Features** acompanha `first_pass_approval_rate`; mede qualidade inicial do Generator.
- Métrica 021: **Product Recommendation** acompanha `recommendation_accuracy`; mede se produto recomendado foi aceito sem devolução ou reclamação.
- Métrica 022: **Product Recommendation** acompanha `restriction_violation_rate`; deve permanecer em zero para restrições críticas.
- Métrica 023: **Contextual Upsell** acompanha `attach_rate`; mede aceitação de complemento sem confundir com pressão comercial.
- Métrica 024: **Contextual Upsell** acompanha `upsell_complaint_rate`; alerta quando growth começa a ferir confiança.
- Métrica 025: **Discount Explanation** acompanha `price_mismatch_rate`; mede diferença entre preço explicado e preço cobrado.
- Métrica 026: **Fulfillment Promise** acompanha `eta_accuracy`; mede promessa de entrega contra entrega real.
- Métrica 027: **Safety Guard** acompanha `human_review_rate`; mede quantos casos ambíguos exigiram humano.
- Métrica 028: **Cart Reengagement** acompanha `helpful_return_rate`; mede retorno útil sem sensação de perseguição.
- Métrica 029: **All Features** acompanha `trace_completeness`; mede decisões com replay possível.
- Métrica 030: **All Features** acompanha `first_pass_approval_rate`; mede qualidade inicial do Generator.
- Métrica 031: **Product Recommendation** acompanha `recommendation_accuracy`; mede se produto recomendado foi aceito sem devolução ou reclamação.
- Métrica 032: **Product Recommendation** acompanha `restriction_violation_rate`; deve permanecer em zero para restrições críticas.
- Métrica 033: **Contextual Upsell** acompanha `attach_rate`; mede aceitação de complemento sem confundir com pressão comercial.
- Métrica 034: **Contextual Upsell** acompanha `upsell_complaint_rate`; alerta quando growth começa a ferir confiança.
- Métrica 035: **Discount Explanation** acompanha `price_mismatch_rate`; mede diferença entre preço explicado e preço cobrado.
- Métrica 036: **Fulfillment Promise** acompanha `eta_accuracy`; mede promessa de entrega contra entrega real.
- Métrica 037: **Safety Guard** acompanha `human_review_rate`; mede quantos casos ambíguos exigiram humano.
- Métrica 038: **Cart Reengagement** acompanha `helpful_return_rate`; mede retorno útil sem sensação de perseguição.
- Métrica 039: **All Features** acompanha `trace_completeness`; mede decisões com replay possível.
- Métrica 040: **All Features** acompanha `first_pass_approval_rate`; mede qualidade inicial do Generator.
- Métrica 041: **Product Recommendation** acompanha `recommendation_accuracy`; mede se produto recomendado foi aceito sem devolução ou reclamação.
- Métrica 042: **Product Recommendation** acompanha `restriction_violation_rate`; deve permanecer em zero para restrições críticas.
- Métrica 043: **Contextual Upsell** acompanha `attach_rate`; mede aceitação de complemento sem confundir com pressão comercial.
- Métrica 044: **Contextual Upsell** acompanha `upsell_complaint_rate`; alerta quando growth começa a ferir confiança.
- Métrica 045: **Discount Explanation** acompanha `price_mismatch_rate`; mede diferença entre preço explicado e preço cobrado.
- Métrica 046: **Fulfillment Promise** acompanha `eta_accuracy`; mede promessa de entrega contra entrega real.
- Métrica 047: **Safety Guard** acompanha `human_review_rate`; mede quantos casos ambíguos exigiram humano.
- Métrica 048: **Cart Reengagement** acompanha `helpful_return_rate`; mede retorno útil sem sensação de perseguição.
- Métrica 049: **All Features** acompanha `trace_completeness`; mede decisões com replay possível.
- Métrica 050: **All Features** acompanha `first_pass_approval_rate`; mede qualidade inicial do Generator.
- Métrica 051: **Product Recommendation** acompanha `recommendation_accuracy`; mede se produto recomendado foi aceito sem devolução ou reclamação.
- Métrica 052: **Product Recommendation** acompanha `restriction_violation_rate`; deve permanecer em zero para restrições críticas.
- Métrica 053: **Contextual Upsell** acompanha `attach_rate`; mede aceitação de complemento sem confundir com pressão comercial.
- Métrica 054: **Contextual Upsell** acompanha `upsell_complaint_rate`; alerta quando growth começa a ferir confiança.
- Métrica 055: **Discount Explanation** acompanha `price_mismatch_rate`; mede diferença entre preço explicado e preço cobrado.
- Métrica 056: **Fulfillment Promise** acompanha `eta_accuracy`; mede promessa de entrega contra entrega real.
- Métrica 057: **Safety Guard** acompanha `human_review_rate`; mede quantos casos ambíguos exigiram humano.
- Métrica 058: **Cart Reengagement** acompanha `helpful_return_rate`; mede retorno útil sem sensação de perseguição.
- Métrica 059: **All Features** acompanha `trace_completeness`; mede decisões com replay possível.
- Métrica 060: **All Features** acompanha `first_pass_approval_rate`; mede qualidade inicial do Generator.
- Métrica 061: **Product Recommendation** acompanha `recommendation_accuracy`; mede se produto recomendado foi aceito sem devolução ou reclamação.
- Métrica 062: **Product Recommendation** acompanha `restriction_violation_rate`; deve permanecer em zero para restrições críticas.
- Métrica 063: **Contextual Upsell** acompanha `attach_rate`; mede aceitação de complemento sem confundir com pressão comercial.
- Métrica 064: **Contextual Upsell** acompanha `upsell_complaint_rate`; alerta quando growth começa a ferir confiança.
- Métrica 065: **Discount Explanation** acompanha `price_mismatch_rate`; mede diferença entre preço explicado e preço cobrado.
- Métrica 066: **Fulfillment Promise** acompanha `eta_accuracy`; mede promessa de entrega contra entrega real.
- Métrica 067: **Safety Guard** acompanha `human_review_rate`; mede quantos casos ambíguos exigiram humano.
- Métrica 068: **Cart Reengagement** acompanha `helpful_return_rate`; mede retorno útil sem sensação de perseguição.
- Métrica 069: **All Features** acompanha `trace_completeness`; mede decisões com replay possível.
- Métrica 070: **All Features** acompanha `first_pass_approval_rate`; mede qualidade inicial do Generator.
- Métrica 071: **Product Recommendation** acompanha `recommendation_accuracy`; mede se produto recomendado foi aceito sem devolução ou reclamação.
- Métrica 072: **Product Recommendation** acompanha `restriction_violation_rate`; deve permanecer em zero para restrições críticas.
- Métrica 073: **Contextual Upsell** acompanha `attach_rate`; mede aceitação de complemento sem confundir com pressão comercial.
- Métrica 074: **Contextual Upsell** acompanha `upsell_complaint_rate`; alerta quando growth começa a ferir confiança.
- Métrica 075: **Discount Explanation** acompanha `price_mismatch_rate`; mede diferença entre preço explicado e preço cobrado.
- Métrica 076: **Fulfillment Promise** acompanha `eta_accuracy`; mede promessa de entrega contra entrega real.
- Métrica 077: **Safety Guard** acompanha `human_review_rate`; mede quantos casos ambíguos exigiram humano.
- Métrica 078: **Cart Reengagement** acompanha `helpful_return_rate`; mede retorno útil sem sensação de perseguição.
- Métrica 079: **All Features** acompanha `trace_completeness`; mede decisões com replay possível.
- Métrica 080: **All Features** acompanha `first_pass_approval_rate`; mede qualidade inicial do Generator.
- Métrica 081: **Product Recommendation** acompanha `recommendation_accuracy`; mede se produto recomendado foi aceito sem devolução ou reclamação.
- Métrica 082: **Product Recommendation** acompanha `restriction_violation_rate`; deve permanecer em zero para restrições críticas.
- Métrica 083: **Contextual Upsell** acompanha `attach_rate`; mede aceitação de complemento sem confundir com pressão comercial.
- Métrica 084: **Contextual Upsell** acompanha `upsell_complaint_rate`; alerta quando growth começa a ferir confiança.
- Métrica 085: **Discount Explanation** acompanha `price_mismatch_rate`; mede diferença entre preço explicado e preço cobrado.
- Métrica 086: **Fulfillment Promise** acompanha `eta_accuracy`; mede promessa de entrega contra entrega real.
- Métrica 087: **Safety Guard** acompanha `human_review_rate`; mede quantos casos ambíguos exigiram humano.
- Métrica 088: **Cart Reengagement** acompanha `helpful_return_rate`; mede retorno útil sem sensação de perseguição.
- Métrica 089: **All Features** acompanha `trace_completeness`; mede decisões com replay possível.
- Métrica 090: **All Features** acompanha `first_pass_approval_rate`; mede qualidade inicial do Generator.
- Métrica 091: **Product Recommendation** acompanha `recommendation_accuracy`; mede se produto recomendado foi aceito sem devolução ou reclamação.
- Métrica 092: **Product Recommendation** acompanha `restriction_violation_rate`; deve permanecer em zero para restrições críticas.
- Métrica 093: **Contextual Upsell** acompanha `attach_rate`; mede aceitação de complemento sem confundir com pressão comercial.
- Métrica 094: **Contextual Upsell** acompanha `upsell_complaint_rate`; alerta quando growth começa a ferir confiança.
- Métrica 095: **Discount Explanation** acompanha `price_mismatch_rate`; mede diferença entre preço explicado e preço cobrado.
- Métrica 096: **Fulfillment Promise** acompanha `eta_accuracy`; mede promessa de entrega contra entrega real.
- Métrica 097: **Safety Guard** acompanha `human_review_rate`; mede quantos casos ambíguos exigiram humano.
- Métrica 098: **Cart Reengagement** acompanha `helpful_return_rate`; mede retorno útil sem sensação de perseguição.
- Métrica 099: **All Features** acompanha `trace_completeness`; mede decisões com replay possível.
- Métrica 100: **All Features** acompanha `first_pass_approval_rate`; mede qualidade inicial do Generator.
- Métrica 101: **Product Recommendation** acompanha `recommendation_accuracy`; mede se produto recomendado foi aceito sem devolução ou reclamação.
- Métrica 102: **Product Recommendation** acompanha `restriction_violation_rate`; deve permanecer em zero para restrições críticas.
- Métrica 103: **Contextual Upsell** acompanha `attach_rate`; mede aceitação de complemento sem confundir com pressão comercial.
- Métrica 104: **Contextual Upsell** acompanha `upsell_complaint_rate`; alerta quando growth começa a ferir confiança.
- Métrica 105: **Discount Explanation** acompanha `price_mismatch_rate`; mede diferença entre preço explicado e preço cobrado.
- Métrica 106: **Fulfillment Promise** acompanha `eta_accuracy`; mede promessa de entrega contra entrega real.
- Métrica 107: **Safety Guard** acompanha `human_review_rate`; mede quantos casos ambíguos exigiram humano.
- Métrica 108: **Cart Reengagement** acompanha `helpful_return_rate`; mede retorno útil sem sensação de perseguição.
- Métrica 109: **All Features** acompanha `trace_completeness`; mede decisões com replay possível.
- Métrica 110: **All Features** acompanha `first_pass_approval_rate`; mede qualidade inicial do Generator.
- Métrica 111: **Product Recommendation** acompanha `recommendation_accuracy`; mede se produto recomendado foi aceito sem devolução ou reclamação.
- Métrica 112: **Product Recommendation** acompanha `restriction_violation_rate`; deve permanecer em zero para restrições críticas.
- Métrica 113: **Contextual Upsell** acompanha `attach_rate`; mede aceitação de complemento sem confundir com pressão comercial.
- Métrica 114: **Contextual Upsell** acompanha `upsell_complaint_rate`; alerta quando growth começa a ferir confiança.
- Métrica 115: **Discount Explanation** acompanha `price_mismatch_rate`; mede diferença entre preço explicado e preço cobrado.
- Métrica 116: **Fulfillment Promise** acompanha `eta_accuracy`; mede promessa de entrega contra entrega real.
- Métrica 117: **Safety Guard** acompanha `human_review_rate`; mede quantos casos ambíguos exigiram humano.
- Métrica 118: **Cart Reengagement** acompanha `helpful_return_rate`; mede retorno útil sem sensação de perseguição.
- Métrica 119: **All Features** acompanha `trace_completeness`; mede decisões com replay possível.
- Métrica 120: **All Features** acompanha `first_pass_approval_rate`; mede qualidade inicial do Generator.
- Métrica 121: **Product Recommendation** acompanha `recommendation_accuracy`; mede se produto recomendado foi aceito sem devolução ou reclamação.
- Métrica 122: **Product Recommendation** acompanha `restriction_violation_rate`; deve permanecer em zero para restrições críticas.
- Métrica 123: **Contextual Upsell** acompanha `attach_rate`; mede aceitação de complemento sem confundir com pressão comercial.
- Métrica 124: **Contextual Upsell** acompanha `upsell_complaint_rate`; alerta quando growth começa a ferir confiança.
- Métrica 125: **Discount Explanation** acompanha `price_mismatch_rate`; mede diferença entre preço explicado e preço cobrado.
- Métrica 126: **Fulfillment Promise** acompanha `eta_accuracy`; mede promessa de entrega contra entrega real.
- Métrica 127: **Safety Guard** acompanha `human_review_rate`; mede quantos casos ambíguos exigiram humano.
- Métrica 128: **Cart Reengagement** acompanha `helpful_return_rate`; mede retorno útil sem sensação de perseguição.
- Métrica 129: **All Features** acompanha `trace_completeness`; mede decisões com replay possível.
- Métrica 130: **All Features** acompanha `first_pass_approval_rate`; mede qualidade inicial do Generator.
- Métrica 131: **Product Recommendation** acompanha `recommendation_accuracy`; mede se produto recomendado foi aceito sem devolução ou reclamação.
- Métrica 132: **Product Recommendation** acompanha `restriction_violation_rate`; deve permanecer em zero para restrições críticas.
- Métrica 133: **Contextual Upsell** acompanha `attach_rate`; mede aceitação de complemento sem confundir com pressão comercial.
- Métrica 134: **Contextual Upsell** acompanha `upsell_complaint_rate`; alerta quando growth começa a ferir confiança.
- Métrica 135: **Discount Explanation** acompanha `price_mismatch_rate`; mede diferença entre preço explicado e preço cobrado.
- Métrica 136: **Fulfillment Promise** acompanha `eta_accuracy`; mede promessa de entrega contra entrega real.
- Métrica 137: **Safety Guard** acompanha `human_review_rate`; mede quantos casos ambíguos exigiram humano.
- Métrica 138: **Cart Reengagement** acompanha `helpful_return_rate`; mede retorno útil sem sensação de perseguição.
- Métrica 139: **All Features** acompanha `trace_completeness`; mede decisões com replay possível.
- Métrica 140: **All Features** acompanha `first_pass_approval_rate`; mede qualidade inicial do Generator.
### Critérios de Prontidão para Aprovar uma Feature
- Prontidão 001: confirme que feature flag existe, foi testada e tem owner operacional.
- Prontidão 002: confirme que rollback foi ensaiado sem depender de deploy manual arriscado.
- Prontidão 003: confirme que contract tests cobrem ausência de campos obrigatórios.
- Prontidão 004: confirme que integration tests atravessam Router, Contract, Generator, Evaluator e Commit.
- Prontidão 005: confirme que acceptance tests descrevem comportamento percebido pelo cliente.
- Prontidão 006: confirme que rubric foi revisada por engenharia e produto.
- Prontidão 007: confirme que traces de rejeição são legíveis por alguém fora do time autor.
- Prontidão 008: confirme que dashboard mostra approval_rate, rejection_rate, latency e complaint_rate.
- Prontidão 009: confirme que canary inicial limita exposição de clientes de alto risco.
- Prontidão 010: confirme que decision log registra trade-offs aceitos antes do rollout.
- Prontidão 011: confirme que feature flag existe, foi testada e tem owner operacional.
- Prontidão 012: confirme que rollback foi ensaiado sem depender de deploy manual arriscado.
- Prontidão 013: confirme que contract tests cobrem ausência de campos obrigatórios.
- Prontidão 014: confirme que integration tests atravessam Router, Contract, Generator, Evaluator e Commit.
- Prontidão 015: confirme que acceptance tests descrevem comportamento percebido pelo cliente.
- Prontidão 016: confirme que rubric foi revisada por engenharia e produto.
- Prontidão 017: confirme que traces de rejeição são legíveis por alguém fora do time autor.
- Prontidão 018: confirme que dashboard mostra approval_rate, rejection_rate, latency e complaint_rate.
- Prontidão 019: confirme que canary inicial limita exposição de clientes de alto risco.
- Prontidão 020: confirme que decision log registra trade-offs aceitos antes do rollout.
- Prontidão 021: confirme que feature flag existe, foi testada e tem owner operacional.
- Prontidão 022: confirme que rollback foi ensaiado sem depender de deploy manual arriscado.
- Prontidão 023: confirme que contract tests cobrem ausência de campos obrigatórios.
- Prontidão 024: confirme que integration tests atravessam Router, Contract, Generator, Evaluator e Commit.
- Prontidão 025: confirme que acceptance tests descrevem comportamento percebido pelo cliente.
- Prontidão 026: confirme que rubric foi revisada por engenharia e produto.
- Prontidão 027: confirme que traces de rejeição são legíveis por alguém fora do time autor.
- Prontidão 028: confirme que dashboard mostra approval_rate, rejection_rate, latency e complaint_rate.
- Prontidão 029: confirme que canary inicial limita exposição de clientes de alto risco.
- Prontidão 030: confirme que decision log registra trade-offs aceitos antes do rollout.
- Prontidão 031: confirme que feature flag existe, foi testada e tem owner operacional.
- Prontidão 032: confirme que rollback foi ensaiado sem depender de deploy manual arriscado.
- Prontidão 033: confirme que contract tests cobrem ausência de campos obrigatórios.
- Prontidão 034: confirme que integration tests atravessam Router, Contract, Generator, Evaluator e Commit.
- Prontidão 035: confirme que acceptance tests descrevem comportamento percebido pelo cliente.
- Prontidão 036: confirme que rubric foi revisada por engenharia e produto.
- Prontidão 037: confirme que traces de rejeição são legíveis por alguém fora do time autor.
- Prontidão 038: confirme que dashboard mostra approval_rate, rejection_rate, latency e complaint_rate.
- Prontidão 039: confirme que canary inicial limita exposição de clientes de alto risco.
- Prontidão 040: confirme que decision log registra trade-offs aceitos antes do rollout.
- Prontidão 041: confirme que feature flag existe, foi testada e tem owner operacional.
- Prontidão 042: confirme que rollback foi ensaiado sem depender de deploy manual arriscado.
- Prontidão 043: confirme que contract tests cobrem ausência de campos obrigatórios.
- Prontidão 044: confirme que integration tests atravessam Router, Contract, Generator, Evaluator e Commit.
- Prontidão 045: confirme que acceptance tests descrevem comportamento percebido pelo cliente.
- Prontidão 046: confirme que rubric foi revisada por engenharia e produto.
- Prontidão 047: confirme que traces de rejeição são legíveis por alguém fora do time autor.
- Prontidão 048: confirme que dashboard mostra approval_rate, rejection_rate, latency e complaint_rate.
- Prontidão 049: confirme que canary inicial limita exposição de clientes de alto risco.
- Prontidão 050: confirme que decision log registra trade-offs aceitos antes do rollout.
- Prontidão 051: confirme que feature flag existe, foi testada e tem owner operacional.
- Prontidão 052: confirme que rollback foi ensaiado sem depender de deploy manual arriscado.
- Prontidão 053: confirme que contract tests cobrem ausência de campos obrigatórios.
- Prontidão 054: confirme que integration tests atravessam Router, Contract, Generator, Evaluator e Commit.
- Prontidão 055: confirme que acceptance tests descrevem comportamento percebido pelo cliente.
- Prontidão 056: confirme que rubric foi revisada por engenharia e produto.
- Prontidão 057: confirme que traces de rejeição são legíveis por alguém fora do time autor.
- Prontidão 058: confirme que dashboard mostra approval_rate, rejection_rate, latency e complaint_rate.
- Prontidão 059: confirme que canary inicial limita exposição de clientes de alto risco.
- Prontidão 060: confirme que decision log registra trade-offs aceitos antes do rollout.
- Prontidão 061: confirme que feature flag existe, foi testada e tem owner operacional.
- Prontidão 062: confirme que rollback foi ensaiado sem depender de deploy manual arriscado.
- Prontidão 063: confirme que contract tests cobrem ausência de campos obrigatórios.
- Prontidão 064: confirme que integration tests atravessam Router, Contract, Generator, Evaluator e Commit.
- Prontidão 065: confirme que acceptance tests descrevem comportamento percebido pelo cliente.
- Prontidão 066: confirme que rubric foi revisada por engenharia e produto.
- Prontidão 067: confirme que traces de rejeição são legíveis por alguém fora do time autor.
- Prontidão 068: confirme que dashboard mostra approval_rate, rejection_rate, latency e complaint_rate.
- Prontidão 069: confirme que canary inicial limita exposição de clientes de alto risco.
- Prontidão 070: confirme que decision log registra trade-offs aceitos antes do rollout.
- Prontidão 071: confirme que feature flag existe, foi testada e tem owner operacional.
- Prontidão 072: confirme que rollback foi ensaiado sem depender de deploy manual arriscado.
- Prontidão 073: confirme que contract tests cobrem ausência de campos obrigatórios.
- Prontidão 074: confirme que integration tests atravessam Router, Contract, Generator, Evaluator e Commit.
- Prontidão 075: confirme que acceptance tests descrevem comportamento percebido pelo cliente.
- Prontidão 076: confirme que rubric foi revisada por engenharia e produto.
- Prontidão 077: confirme que traces de rejeição são legíveis por alguém fora do time autor.
- Prontidão 078: confirme que dashboard mostra approval_rate, rejection_rate, latency e complaint_rate.
- Prontidão 079: confirme que canary inicial limita exposição de clientes de alto risco.
- Prontidão 080: confirme que decision log registra trade-offs aceitos antes do rollout.
- Prontidão 081: confirme que feature flag existe, foi testada e tem owner operacional.
- Prontidão 082: confirme que rollback foi ensaiado sem depender de deploy manual arriscado.
- Prontidão 083: confirme que contract tests cobrem ausência de campos obrigatórios.
- Prontidão 084: confirme que integration tests atravessam Router, Contract, Generator, Evaluator e Commit.
- Prontidão 085: confirme que acceptance tests descrevem comportamento percebido pelo cliente.
- Prontidão 086: confirme que rubric foi revisada por engenharia e produto.
- Prontidão 087: confirme que traces de rejeição são legíveis por alguém fora do time autor.
- Prontidão 088: confirme que dashboard mostra approval_rate, rejection_rate, latency e complaint_rate.
- Prontidão 089: confirme que canary inicial limita exposição de clientes de alto risco.
- Prontidão 090: confirme que decision log registra trade-offs aceitos antes do rollout.
- Prontidão 091: confirme que feature flag existe, foi testada e tem owner operacional.
- Prontidão 092: confirme que rollback foi ensaiado sem depender de deploy manual arriscado.
- Prontidão 093: confirme que contract tests cobrem ausência de campos obrigatórios.
- Prontidão 094: confirme que integration tests atravessam Router, Contract, Generator, Evaluator e Commit.
- Prontidão 095: confirme que acceptance tests descrevem comportamento percebido pelo cliente.
- Prontidão 096: confirme que rubric foi revisada por engenharia e produto.
- Prontidão 097: confirme que traces de rejeição são legíveis por alguém fora do time autor.
- Prontidão 098: confirme que dashboard mostra approval_rate, rejection_rate, latency e complaint_rate.
- Prontidão 099: confirme que canary inicial limita exposição de clientes de alto risco.
- Prontidão 100: confirme que decision log registra trade-offs aceitos antes do rollout.
- Prontidão 101: confirme que feature flag existe, foi testada e tem owner operacional.
- Prontidão 102: confirme que rollback foi ensaiado sem depender de deploy manual arriscado.
- Prontidão 103: confirme que contract tests cobrem ausência de campos obrigatórios.
- Prontidão 104: confirme que integration tests atravessam Router, Contract, Generator, Evaluator e Commit.
- Prontidão 105: confirme que acceptance tests descrevem comportamento percebido pelo cliente.
- Prontidão 106: confirme que rubric foi revisada por engenharia e produto.
- Prontidão 107: confirme que traces de rejeição são legíveis por alguém fora do time autor.
- Prontidão 108: confirme que dashboard mostra approval_rate, rejection_rate, latency e complaint_rate.
- Prontidão 109: confirme que canary inicial limita exposição de clientes de alto risco.
- Prontidão 110: confirme que decision log registra trade-offs aceitos antes do rollout.
- Prontidão 111: confirme que feature flag existe, foi testada e tem owner operacional.
- Prontidão 112: confirme que rollback foi ensaiado sem depender de deploy manual arriscado.
- Prontidão 113: confirme que contract tests cobrem ausência de campos obrigatórios.
- Prontidão 114: confirme que integration tests atravessam Router, Contract, Generator, Evaluator e Commit.
- Prontidão 115: confirme que acceptance tests descrevem comportamento percebido pelo cliente.
- Prontidão 116: confirme que rubric foi revisada por engenharia e produto.
- Prontidão 117: confirme que traces de rejeição são legíveis por alguém fora do time autor.
- Prontidão 118: confirme que dashboard mostra approval_rate, rejection_rate, latency e complaint_rate.
- Prontidão 119: confirme que canary inicial limita exposição de clientes de alto risco.
- Prontidão 120: confirme que decision log registra trade-offs aceitos antes do rollout.
- Prontidão 121: confirme que feature flag existe, foi testada e tem owner operacional.
- Prontidão 122: confirme que rollback foi ensaiado sem depender de deploy manual arriscado.
- Prontidão 123: confirme que contract tests cobrem ausência de campos obrigatórios.
- Prontidão 124: confirme que integration tests atravessam Router, Contract, Generator, Evaluator e Commit.
- Prontidão 125: confirme que acceptance tests descrevem comportamento percebido pelo cliente.
- Prontidão 126: confirme que rubric foi revisada por engenharia e produto.
- Prontidão 127: confirme que traces de rejeição são legíveis por alguém fora do time autor.
- Prontidão 128: confirme que dashboard mostra approval_rate, rejection_rate, latency e complaint_rate.
- Prontidão 129: confirme que canary inicial limita exposição de clientes de alto risco.
- Prontidão 130: confirme que decision log registra trade-offs aceitos antes do rollout.
- Prontidão 131: confirme que feature flag existe, foi testada e tem owner operacional.
- Prontidão 132: confirme que rollback foi ensaiado sem depender de deploy manual arriscado.
- Prontidão 133: confirme que contract tests cobrem ausência de campos obrigatórios.
- Prontidão 134: confirme que integration tests atravessam Router, Contract, Generator, Evaluator e Commit.
- Prontidão 135: confirme que acceptance tests descrevem comportamento percebido pelo cliente.
- Prontidão 136: confirme que rubric foi revisada por engenharia e produto.
- Prontidão 137: confirme que traces de rejeição são legíveis por alguém fora do time autor.
- Prontidão 138: confirme que dashboard mostra approval_rate, rejection_rate, latency e complaint_rate.
- Prontidão 139: confirme que canary inicial limita exposição de clientes de alto risco.
- Prontidão 140: confirme que decision log registra trade-offs aceitos antes do rollout.
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
