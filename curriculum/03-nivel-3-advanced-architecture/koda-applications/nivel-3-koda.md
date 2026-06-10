# 🚀 KODA em Arquitetura Avançada: Sistemas que Sobrevivem a Horas, Falhas e Evolução
## Como aplicar Nível 3 ao agente de vendas por WhatsApp da KODA

**Tempo Estimado:** 180-240 minutos  
**Nível:** 3 - Arquitetura Avançada  
**Pré-requisitos:** Ter completado Nível 1, `nivel-1-koda.md`, Nível 2, `nivel-2-koda.md`, e os 5 módulos de Nível 3  
**Status:** 🟢 CRÍTICO  
**Data de Criação:** Maio 2026  

---

## 📖 Prólogo: A Semana em que o KODA Não Quebrou, mas Ainda Falhou

Segunda-feira, 08h10.

Fernando chegou cedo ao escritório da KODA.

Ele abriu o dashboard com uma confiança que não existia seis meses antes.

As métricas pareciam boas.

O uptime estava alto.

As conversas longas já não terminavam em colapso.

O KODA lembrava alergias.

O KODA respeitava orçamento.

O KODA tinha Generator, Evaluator, rubrics e traces.

Nível 1 tinha dado fundação.

Nível 2 tinha dado visibilidade.

Por alguns segundos, Fernando sorriu.

Então chegaram três mensagens no canal de incidentes.

```
08:12 Suporte: Cliente Pedro voltou depois de pagamento com erro.
08:12 Suporte: KODA perdeu o carrinho dele depois do restart de domingo.
08:13 Suporte: Marina recebeu duas confirmações de pedido, com SKUs diferentes.
08:14 Suporte: Cliente Rafael ficou 4h no WhatsApp e KODA resumiu errado a restrição de cafeína.
```

Fernando congelou.

O sistema não tinha caído.

Não havia uma exceção gigante no log.

Nenhum monitor gritava que a API estava fora.

Mesmo assim, três clientes tinham vivido falhas reais.

Pedro tinha montado um carrinho perfeito, mas o servidor reiniciou antes de salvar o estado certo.

Marina tinha uma intenção clara, mas dois agentes tentaram agir ao mesmo tempo.

Rafael tinha explicado suas restrições durante horas, mas a conversa ficou grande demais e o resumo perdeu detalhes críticos.

E o quarto problema apareceu durante a reunião das 10h.

```
Fernando: "O KODA não quebra mais como antes. Isso é bom."

Dev Senior: "Mas agora temos outro tipo de falha."

Fernando: "Sim. Falha de coordenação. Falha de estado. Falha de contexto longo."

Dev Ops: "E falha de arquitetura acumulada. Tem componente que talvez nem precise mais existir."

Fernando: "Então Nível 3 começa aqui."
```

A frase ficou no quadro branco por quase uma hora.

Nível 3 não é sobre fazer o KODA responder bonito.

Isso Nível 1 e Nível 2 já tornaram possível.

Nível 3 é sobre fazer o KODA funcionar como um sistema.

Um sistema com vários agentes internos.

Um sistema que salva estado antes de precisar dele.

Um sistema que coordena trabalho por arquivos, locks e status visível.

Um sistema que compacta contexto sem apagar o que torna o cliente seguro.

Um sistema que tem coragem de remover partes quando o modelo melhora.

Fernando abriu quatro conversas reais e viu o mesmo padrão.

O KODA já não era um chatbot simples.

Era uma pequena operação comercial rodando dentro de uma conversa de WhatsApp.

Tinha Discovery.

Tinha recomendação.

Tinha carrinho.

Tinha pagamento.

Tinha fulfillment.

Tinha suporte pós-venda.

Cada parte tinha contexto, estado e risco.

Quando uma parte falhava, o cliente não via o componente.

O cliente via apenas o KODA.

Por isso, a arquitetura inteira precisava assumir responsabilidade.

Esse módulo é o mapa dessa responsabilidade.

Você vai acompanhar Fernando transformando o KODA de agente resiliente em sistema maduro.

Não com teoria solta.

Com Pedro, Marina, Rafael e outros clientes reais.

Com JSON files.

Com SQLite checkpoints.

Com lock files.

Com compactação server-side.

Com decision records.

E com uma pergunta que fecha o Nível 3:

Se o KODA já está mais forte, o que ainda precisa existir na arquitetura?

---

## 🔍 Diagnóstico Inicial: O que Nível 1 e Nível 2 Não Cobrem

Antes de mergulhar nos 5 padrões, vamos classificar as falhas que Fernando encontrou naquela manhã. Cada falha mapeia para um tipo de problema que Nível 3 resolve:

| Incidente | Cliente | Sintoma | Tipo de falha | Padrão Nível 3 |
|---|---|---|---|---|
| Carrinho perdido após restart | Pedro | KODA esqueceu tudo e perguntou "Como posso ajudar?" | Perda de estado em memória | State persistence |
| Dois pedidos com SKUs diferentes | Marina | Discovery correto, Order leu estado antigo | Conflito entre agentes | File-based coordination + Multi-agent |
| Cafeína sugerida após 4h de conversa | Rafael | Restrição diluída em ruído de conversa longa | Degradação de contexto | Server-side compaction |
| Componentes acumulando latência | Time KODA | Guards rodando sem valor mensurável | Peso morto arquitetural | Harness evolution |

Cada incidente é real. Cada um deles aconteceu apesar de Nível 1 (fundação) e Nível 2 (visibilidade) estarem implementados. A causa raiz de cada um é diferente. A solução de cada um exige um padrão específico de Nível 3.

**Pedro** não perdeu o carrinho porque o prompt estava ruim. Perdeu porque o estado existia apenas em RAM. A solução não é melhorar o texto da resposta — é persistir `cart.json` e `payment_state.json` em SQLite ANTES de gerar o link de pagamento.

**Marina** não recebeu dois pedidos porque o modelo alucinou. Recebeu porque dois agentes leram o mesmo evento e agiram em paralelo sem coordenação. A solução não é treinar o modelo melhor — é implementar `order.lock.json` com TTL e status visível para todos os agentes.

**Rafael** não perdeu a restrição de cafeína porque o Evaluator falhou. Perdeu porque a compactação classificou "evito cafeína" como preferência média e a sumarizou para "cliente tem algumas preferências". A solução não é pedir para o modelo "prestar mais atenção" — é classificar fatos por criticidade ANTES de sumarizar.

**O time KODA** não acumulou complexidade por incompetência. Acumulou porque cada novo incidente gerava um novo guard, e ninguém removia os antigos. A solução não é "ter menos componentes" — é medir custo e valor de cada um e remover com evidência.

Este diagnóstico é o que separa Nível 3 dos níveis anteriores. Nível 1 pergunta "o sistema quebrou?". Nível 2 pergunta "consigo ver por que quebrou?". Nível 3 pergunta "qual camada arquitetural específica falhou, e qual padrão a conserta?".

Com este diagnóstico em mente, vamos aplicar cada padrão ao KODA.

---

## 🎯 Objetivos Deste Módulo

Ao final deste módulo, você será capaz de:

- ✅ **Desenhar uma arquitetura multi-agent para o KODA** com Planner, Generator, Evaluator, Discovery, Order e Fulfillment Agents trabalhando sem confundir responsabilidades.
- ✅ **Persistir estado crítico de conversas KODA** usando SQLite, JSON checkpointing e snapshots recuperáveis para proteger carrinho, preferências, restrições e status de pedido.
- ✅ **Coordenar agentes por arquivos** usando `lock.json`, `status.json`, `manifest.json`, atomic writes e audit trail para impedir pedido duplicado ou decisão baseada em estado antigo.
- ✅ **Compactar conversas de 4+ horas no servidor** mantendo alergias, orçamento, preferências, decisões e promessas, enquanto remove ruído social e repetição.
- ✅ **Evoluir o harness do KODA** com métricas, custos, decision records e remoção segura de componentes que deixaram de agregar valor.
- ✅ **Integrar os 5 padrões de Nível 3** em uma arquitetura única para vendas por WhatsApp, pronta para diagnóstico, recuperação e melhoria contínua.
- ✅ **Praticar decisões arquiteturais reais** por meio de exercícios que simulam incidentes, schema design, token budget, decision records e multi-agent flows.

---

## 🧭 Roadmap Visual do Nível 3 no KODA

```
ENTRADA: KODA já passou por Nível 1 e Nível 2
  |
  v
PARTE 1: Multi-agent systems
  KODA deixa de ser um agente único e vira uma equipe interna
  |
  v
PARTE 2: State persistence
  O estado sobrevive a restart, deploy, timeout e retorno do cliente
  |
  v
PARTE 3: File-based coordination
  Agentes passam a coordenar por arquivos, locks, status e manifest
  |
  v
PARTE 4: Server-side compaction
  Conversas de 4+ horas continuam úteis sem carregar ruído infinito
  |
  v
PARTE 5: Harness evolution
  A arquitetura deixa de acumular peso morto e passa a evoluir com o modelo
  |
  v
PARTE 6: Arquitetura integrada
  Os 5 padrões trabalham juntos no KODA real
  |
  v
SAÍDA: Você consegue projetar, operar e simplificar KODA em escala
```

---

## 🔗 Parte 1: Sistemas Multi-Agente no KODA

### O problema que Fernando enxergou

O primeiro KODA era um agente único.
Ele recebia a mensagem do WhatsApp.
Ele entendia intenção.
Ele consultava catálogo.
Ele comparava produtos.
Ele montava carrinho.
Ele validava segurança.
Ele escrevia a resposta final.
Em conversas curtas, isso parecia suficiente.
Em conversas longas, esse desenho colocava decisões demais dentro de uma única trilha mental.
A falha de Marina no módulo de multi-agent systems mostrou o limite.
Ela tinha orçamento, intolerância à lactose e preferência por chocolate.
O agente único tentou equilibrar tudo de uma vez.
Recomendou combo acima do orçamento.
Depois confundiu proteína vegetal com desconto.
Depois quase voltou para whey concentrado com lactose.
A pergunta deixou de ser: como melhorar o prompt?
A pergunta passou a ser: qual responsabilidade pertence a qual agente?

### Evolução da arquitetura do KODA

| Fase | Desenho | Força | Falha típica no KODA |
| --- | --- | --- | --- |
| Protótipo | Single Agent | Rápido de criar | Mistura descoberta, venda e validação na mesma resposta |
| Nível 1 | Single Agent com harness | Evita erros óbvios | Ainda depende de um raciocínio único |
| Nível 2 | Generator + Evaluator | Melhora qualidade | Ainda não separa toda a jornada comercial |
| Nível 3 | Planner + agentes especializados | Responsabilidades claras | Exige coordenação e estado persistente |

### A equipe interna do KODA

#### Planner Agent

- **Responsabilidade:** divide a jornada em etapas pequenas
- **Exemplo KODA:** decide que Marina está em comparação final, não em descoberta inicial
- **Regra de Nível 3:** se outro agente depende dessa decisão, a saída precisa virar artefato auditável.

#### Discovery Agent

- **Responsabilidade:** extrai intenção, restrições e preferências
- **Exemplo KODA:** registra lactose, orçamento de R$ 220 e preferência por chocolate
- **Regra de Nível 3:** se outro agente depende dessa decisão, a saída precisa virar artefato auditável.

#### Catalog Agent

- **Responsabilidade:** consulta produtos e estoque
- **Exemplo KODA:** busca apenas SKUs sem lactose disponíveis em São Paulo
- **Regra de Nível 3:** se outro agente depende dessa decisão, a saída precisa virar artefato auditável.

#### Generator Agent

- **Responsabilidade:** cria respostas e artefatos comerciais
- **Exemplo KODA:** gera três opções com preço por dose e duração estimada
- **Regra de Nível 3:** se outro agente depende dessa decisão, a saída precisa virar artefato auditável.

#### Evaluator Agent

- **Responsabilidade:** avalia fatos, segurança, tom e contrato
- **Exemplo KODA:** rejeita recomendação que excede orçamento ou contém lactose
- **Regra de Nível 3:** se outro agente depende dessa decisão, a saída precisa virar artefato auditável.

#### Order Agent

- **Responsabilidade:** monta carrinho e pedido
- **Exemplo KODA:** cria order draft com SKU, quantidade, frete e cupom
- **Regra de Nível 3:** se outro agente depende dessa decisão, a saída precisa virar artefato auditável.

#### Fulfillment Agent

- **Responsabilidade:** reserva estoque e prepara entrega
- **Exemplo KODA:** só age depois de evaluation approved
- **Regra de Nível 3:** se outro agente depende dessa decisão, a saída precisa virar artefato auditável.

#### Recovery Agent

- **Responsabilidade:** retoma fluxo após falha
- **Exemplo KODA:** recarrega Pedro do checkpoint de carrinho
- **Regra de Nível 3:** se outro agente depende dessa decisão, a saída precisa virar artefato auditável.

### Como a decomposição muda uma feature real

Feature: recomendação de stack mensal para hipertrofia.

```
Cliente: "Treino 5 vezes por semana, quero ganhar massa, sou intolerante a lactose,
tenho R$ 350, prefiro chocolate e não quero estimulante porque treino à noite."
```

Sem multi-agent, o KODA tenta responder em uma chamada grande.

Com multi-agent, o KODA cria uma fila de responsabilidades.

```
1. Planner define etapas:
   - coletar restrições finais
   - buscar produtos candidatos
   - montar combinações até R$ 350
   - avaliar segurança e custo por dose
   - gerar resposta curta para WhatsApp

2. Discovery Agent extrai fatos:
   - objetivo: hipertrofia
   - frequência: 5x por semana
   - restrição: lactose
   - orçamento: R$ 350
   - sabor preferido: chocolate
   - evitar: estimulantes

3. Catalog Agent busca SKUs:
   - whey isolado sem lactose
   - creatina monohidratada
   - proteína vegetal chocolate
   - multivitamínico sem estimulante

4. Generator Agent cria opções:
   - stack econômico
   - stack balanceado
   - stack premium dentro do orçamento

5. Evaluator Agent rejeita riscos:
   - qualquer produto com lactose
   - qualquer produto acima do orçamento
   - qualquer pré-treino com cafeína

6. Order Agent monta carrinho apenas da opção aprovada.
```


### Pseudocódigo de orquestração multi-agent

```python
def handle_whatsapp_turn(event):
    conversation_id = event["conversation_id"]

    state = load_state(conversation_id)
    plan = planner_agent.plan(
        event=event,
        customer_state=state.customer,
        order_state=state.order,
    )

    write_json(conversation_id, "plan.json", plan)

    if plan.stage == "discovery":
        discovery = discovery_agent.extract(event, state.customer)
        write_json(conversation_id, "discovery.json", discovery)
        return generator_agent.ask_follow_up(discovery)

    if plan.stage == "recommendation":
        candidates = catalog_agent.search(plan.constraints)
        draft = generator_agent.create_recommendation(plan, candidates)
        evaluation = evaluator_agent.check(
            draft=draft,
            customer_state=state.customer,
            policies=KODA_SAFETY_POLICIES,
        )

        write_json(conversation_id, "recommendation_draft.json", draft)
        write_json(conversation_id, "evaluation.json", evaluation)

        if evaluation["decision"] == "approved":
            return generator_agent.render_whatsapp_message(draft)

        return generator_agent.repair_recommendation(draft, evaluation)

    if plan.stage == "order":
        order_draft = order_agent.create_order(plan, state.cart)
        evaluation = evaluator_agent.check_order(order_draft, state.customer)

        if evaluation["decision"] != "approved":
            return generator_agent.explain_order_block(evaluation)

        return fulfillment_agent.reserve_after_approval(order_draft)
```

### Exemplo concreto: agentes por feature KODA

| Feature KODA | Agentes principais | Exemplo concreto |
| --- | --- | --- |
| Product Discovery | Discovery + Catalog + Evaluator | KODA pergunta objetivo, restrição, sabor e orçamento antes de recomendar |
| Stack Builder | Planner + Catalog + Generator + Evaluator | KODA monta combo mensal com whey, creatina e vitaminas sem passar do budget |
| Cart Recovery | Recovery + Order + Generator | KODA retoma Pedro no carrinho depois de restart |
| Payment Retry | Order + Fulfillment + Evaluator | KODA não cria pedido duplicado depois de erro no gateway |
| Post-sale Support | Fulfillment + Generator + Evaluator | KODA explica entrega sem inventar prazo |

### Cartões de aplicação multi-agent

#### Caso multi-agent 1: Marina

- **Momento da conversa:** comparação final entre whey isolado e proteína vegetal.
- **Planner decide:** qual etapa comercial está ativa e qual etapa deve esperar.
- **Generator produz:** uma resposta curta para WhatsApp e um artefato estruturado.
- **Evaluator verifica:** fatos críticos, tom, orçamento, estoque e restrições.
- **Guardrail específico:** não repetir descoberta inicial.
- **Resultado esperado:** o cliente vê um único KODA, mas a decisão veio de uma equipe interna coordenada.

#### Caso multi-agent 2: Pedro

- **Momento da conversa:** recuperação de carrinho depois de pagamento falho.
- **Planner decide:** qual etapa comercial está ativa e qual etapa deve esperar.
- **Generator produz:** uma resposta curta para WhatsApp e um artefato estruturado.
- **Evaluator verifica:** fatos críticos, tom, orçamento, estoque e restrições.
- **Guardrail específico:** não montar carrinho do zero.
- **Resultado esperado:** o cliente vê um único KODA, mas a decisão veio de uma equipe interna coordenada.

#### Caso multi-agent 3: Rafael

- **Momento da conversa:** stack sem cafeína para treino noturno.
- **Planner decide:** qual etapa comercial está ativa e qual etapa deve esperar.
- **Generator produz:** uma resposta curta para WhatsApp e um artefato estruturado.
- **Evaluator verifica:** fatos críticos, tom, orçamento, estoque e restrições.
- **Guardrail específico:** não sugerir pré-treino estimulante.
- **Resultado esperado:** o cliente vê um único KODA, mas a decisão veio de uma equipe interna coordenada.

#### Caso multi-agent 4: Bianca

- **Momento da conversa:** pedido com cupom e frete grátis.
- **Planner decide:** qual etapa comercial está ativa e qual etapa deve esperar.
- **Generator produz:** uma resposta curta para WhatsApp e um artefato estruturado.
- **Evaluator verifica:** fatos críticos, tom, orçamento, estoque e restrições.
- **Guardrail específico:** não aplicar cupom fora da regra.
- **Resultado esperado:** o cliente vê um único KODA, mas a decisão veio de uma equipe interna coordenada.

#### Caso multi-agent 5: Lucas

- **Momento da conversa:** compra recorrente de creatina.
- **Planner decide:** qual etapa comercial está ativa e qual etapa deve esperar.
- **Generator produz:** uma resposta curta para WhatsApp e um artefato estruturado.
- **Evaluator verifica:** fatos críticos, tom, orçamento, estoque e restrições.
- **Guardrail específico:** não reabrir consultoria completa.
- **Resultado esperado:** o cliente vê um único KODA, mas a decisão veio de uma equipe interna coordenada.

#### Caso multi-agent 6: Ana

- **Momento da conversa:** restrição a glúten e preferência por baunilha.
- **Planner decide:** qual etapa comercial está ativa e qual etapa deve esperar.
- **Generator produz:** uma resposta curta para WhatsApp e um artefato estruturado.
- **Evaluator verifica:** fatos críticos, tom, orçamento, estoque e restrições.
- **Guardrail específico:** não tratar sabor como alergia.
- **Resultado esperado:** o cliente vê um único KODA, mas a decisão veio de uma equipe interna coordenada.

#### Caso multi-agent 7: João

- **Momento da conversa:** pedido corporativo para academia.
- **Planner decide:** qual etapa comercial está ativa e qual etapa deve esperar.
- **Generator produz:** uma resposta curta para WhatsApp e um artefato estruturado.
- **Evaluator verifica:** fatos críticos, tom, orçamento, estoque e restrições.
- **Guardrail específico:** não misturar cliente pessoa física com B2B.
- **Resultado esperado:** o cliente vê um único KODA, mas a decisão veio de uma equipe interna coordenada.

#### Caso multi-agent 8: Nina

- **Momento da conversa:** troca de produto por sabor indisponível.
- **Planner decide:** qual etapa comercial está ativa e qual etapa deve esperar.
- **Generator produz:** uma resposta curta para WhatsApp e um artefato estruturado.
- **Evaluator verifica:** fatos críticos, tom, orçamento, estoque e restrições.
- **Guardrail específico:** não confirmar SKU sem estoque.
- **Resultado esperado:** o cliente vê um único KODA, mas a decisão veio de uma equipe interna coordenada.

#### Caso multi-agent 9: Caio

- **Momento da conversa:** comparação por preço por dose.
- **Planner decide:** qual etapa comercial está ativa e qual etapa deve esperar.
- **Generator produz:** uma resposta curta para WhatsApp e um artefato estruturado.
- **Evaluator verifica:** fatos críticos, tom, orçamento, estoque e restrições.
- **Guardrail específico:** não escolher só preço total.
- **Resultado esperado:** o cliente vê um único KODA, mas a decisão veio de uma equipe interna coordenada.

#### Caso multi-agent 10: Lara

- **Momento da conversa:** suporte pós-venda com atraso de entrega.
- **Planner decide:** qual etapa comercial está ativa e qual etapa deve esperar.
- **Generator produz:** uma resposta curta para WhatsApp e um artefato estruturado.
- **Evaluator verifica:** fatos críticos, tom, orçamento, estoque e restrições.
- **Guardrail específico:** não prometer nova data sem Fulfillment.
- **Resultado esperado:** o cliente vê um único KODA, mas a decisão veio de uma equipe interna coordenada.

#### Caso multi-agent 11: Otávio

- **Momento da conversa:** carrinho com dois endereços possíveis.
- **Planner decide:** qual etapa comercial está ativa e qual etapa deve esperar.
- **Generator produz:** uma resposta curta para WhatsApp e um artefato estruturado.
- **Evaluator verifica:** fatos críticos, tom, orçamento, estoque e restrições.
- **Guardrail específico:** não fechar antes de confirmar endereço.
- **Resultado esperado:** o cliente vê um único KODA, mas a decisão veio de uma equipe interna coordenada.

#### Caso multi-agent 12: Sofia

- **Momento da conversa:** cliente indecisa que pede opinião pessoal.
- **Planner decide:** qual etapa comercial está ativa e qual etapa deve esperar.
- **Generator produz:** uma resposta curta para WhatsApp e um artefato estruturado.
- **Evaluator verifica:** fatos críticos, tom, orçamento, estoque e restrições.
- **Guardrail específico:** não esconder trade-offs importantes.
- **Resultado esperado:** o cliente vê um único KODA, mas a decisão veio de uma equipe interna coordenada.

### KODA Walkthrough: Marina fecha compra com agentes coordenados

Vamos rastrear o fluxo completo de uma compra real no KODA Nível 3, do WhatsApp até a confirmação:

**00:00 — Marina envia mensagem:**
```
"Quero fechar o whey isolado chocolate sem lactose. Entrega em Pinheiros."
```

**00:01 — Ingress Layer:**
- Recebe webhook do WhatsApp.
- Cria `conversation_event.json` com idempotency key: `evt_marina_20260526_001`.
- Encaminha para o Planner.

**00:02 — Planner Agent:**
- Lê `customer_profile.json` de Marina: intolerância à lactose, orçamento R$ 220, preferência chocolate.
- Decide etapa: `order_confirmation` (não discovery inicial).
- Escreve `plan.json`: `{"stage": "order_confirmation", "customer_id": "wa_5511998765432", "intent": "comprar whey isolado chocolate"}`.

**00:03 — Discovery Agent:**
- Confirma intenção: comprar whey isolado, chocolate, sem lactose, Pinheiros.
- Atualiza `discovery.json` com intenção confirmada.

**00:04 — Catalog Agent:**
- Consulta SKU `WHEY-ISO-CHOC-001` no inventário.
- Verifica: em estoque (32 unidades em SP), preço R$ 199,90.
- Escreve `catalog_results.json`: `{"sku": "WHEY-ISO-CHOC-001", "price": 199.90, "stock_sp": 32, "lactose_free": true, "flavor": "chocolate"}`.

**00:05 — Order Agent:**
- Adquire `order.lock.json` com TTL de 30s.
- Lê `discovery.json`, `catalog_results.json` e `customer_profile.json`.
- Monta `order_draft.json`: 1x WHEY-ISO-CHOC-001, R$ 199,90, frete grátis, entrega Pinheiros.
- Libera `order.lock.json`.

**00:06 — Evaluator:**
- Lê `order_draft.json` e `customer_profile.json`.
- Verifica: SKU sem lactose? ✅ Produto em estoque? ✅ Preço < R$ 220? ✅ Entrega em Pinheiros viável? ✅
- Score: 9.2/10. Verdict: APPROVED.
- Escreve `evaluator_verdict.json`.

**00:07 — Generator:**
- Recebe veredict aprovado.
- Gera resposta para WhatsApp: "Marina, seu Whey Isolado Chocolate (R$ 199,90) está confirmado. Entrega amanhã em Pinheiros. Link de pagamento: [link]"

**00:08 — KODA envia resposta.**
- `manifest.json` é escrito listando todos os artefatos usados: `[plan.json, customer_profile.json, discovery.json, catalog_results.json, order_draft.json, evaluator_verdict.json]`.
- Cliente vê: uma resposta curta e útil no WhatsApp.

**Por que isso funciona:**
- Se o servidor reiniciar entre 00:05 e 00:06, o estado está em `order_draft.json` e pode ser recuperado.
- Se outro evento de Marina chegar simultaneamente, o `order.lock.json` impede processamento paralelo.
- Se o suporte precisar explicar a resposta, o `manifest.json` mostra exatamente quais arquivos foram usados.
- Se a conversa durar 4h, a compactação preserva a decisão de compra e remove o ruído.

Este é o KODA Nível 3 em operação. Não é mágica — é arquitetura.

---

## 💾 Parte 2: Persistência de Estado no KODA

### A história do carrinho de Pedro

Pedro passou 47 minutos montando uma compra.
Ele tinha restrição a glúten.
Ele tinha orçamento de R$ 380.
Ele escolheu whey isolado, creatina, pré-treino sem cafeína e multivitamínico.
O KODA chegou ao link de pagamento.
O servidor reiniciou.
O processo voltou sem memória.
Pedro escreveu: deu erro no pagamento, tenta de novo?
O KODA respondeu como se fosse a primeira mensagem.
Essa falha não era de prompt.
Era falta de state persistence.
Persistência de estado é a promessa de que o tempo do cliente não desaparece quando o processo morre.

### O que precisa sobreviver no KODA

- **`customer_profile.json`:** nome, restrições, objetivos, preferências e riscos de segurança.
- **`conversation_summary.json`:** resumo curado dos turnos relevantes.
- **`cart.json`:** itens, quantidades, preço travado, cupom e frete.
- **`order_state.json`:** status do pedido, pagamento, reserva e entrega.
- **`agent_plan.json`:** etapa atual e próxima ação esperada.
- **`audit_manifest.json`:** lista de artefatos que sustentam a decisão enviada ao cliente.

### SQLite para estado transacional

```sql
CREATE TABLE conversations (
    conversation_id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL,
    current_stage TEXT NOT NULL,
    last_event_id TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE customer_facts (
    fact_id TEXT PRIMARY KEY,
    conversation_id TEXT NOT NULL,
    fact_type TEXT NOT NULL,
    fact_value TEXT NOT NULL,
    confidence REAL NOT NULL,
    source_event_id TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE cart_items (
    cart_item_id TEXT PRIMARY KEY,
    conversation_id TEXT NOT NULL,
    sku TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price_cents INTEGER NOT NULL,
    safety_status TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE order_checkpoints (
    checkpoint_id TEXT PRIMARY KEY,
    conversation_id TEXT NOT NULL,
    checkpoint_type TEXT NOT NULL,
    payload_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);
```

### JSON checkpoint para conversa WhatsApp

```json
{
  "conversation_id": "wa_2026_05_26_pedro_001",
  "customer_id": "customer_pedro",
  "checkpoint_type": "cart_ready_for_payment",
  "created_at": "2026-05-26T21:03:42Z",
  "customer_context": {
    "name": "Pedro",
    "constraints": ["sem gluten"],
    "budget_cents": 38000,
    "delivery_city": "Sao Paulo",
    "delivery_neighborhood": "Vila Mariana"
  },
  "cart": {
    "items": [
      {"sku": "WHEY-ISO-BAUN-900", "name": "Whey Isolado Baunilha 900g", "price_cents": 18990},
      {"sku": "CREA-MONO-300", "name": "Creatina Monohidratada 300g", "price_cents": 5990},
      {"sku": "PRE-NOCAF-150", "name": "Pre-treino Sem Cafeina 150g", "price_cents": 7990},
      {"sku": "MULTI-60", "name": "Multivitaminico 60 caps", "price_cents": 4990}
    ],
    "total_cents": 37960,
    "freight_cents": 0,
    "payment_link_status": "generated"
  },
  "resume_prompt": "Pedro estava finalizando pagamento do carrinho aprovado. Nao reiniciar discovery.",
  "next_safe_action": "reissue_payment_link"
}
```

### Padrão de checkpoint por etapa

| Etapa KODA | Checkpoint | Quando salvar | Recuperação |
| --- | --- | --- | --- |
| Discovery | preferences_captured | Depois de extrair restrições | Retomar perguntando apenas lacunas |
| Recommendation | recommendation_approved | Depois do Evaluator aprovar | Reexibir opção aprovada sem recalcular tudo |
| Cart | cart_ready_for_payment | Antes de gerar link | Reemitir link ou confirmar carrinho |
| Payment | payment_pending | Depois de chamar gateway | Consultar status antes de criar outro pedido |
| Fulfillment | stock_reserved | Depois de reserva | Evitar reserva duplicada |

### Pseudocódigo de checkpointing

```python
def save_checkpoint(conversation_id, checkpoint_type, payload):
    checkpoint = {
        "conversation_id": conversation_id,
        "checkpoint_type": checkpoint_type,
        "payload": payload,
        "created_at": now_iso(),
        "schema_version": "koda-state-v3",
    }

    db.insert_order_checkpoint(checkpoint)
    write_json_atomic(
        f"state/{conversation_id}/{checkpoint_type}.json",
        checkpoint,
    )


def recover_conversation(conversation_id):
    latest = db.load_latest_checkpoint(conversation_id)

    if latest.checkpoint_type == "cart_ready_for_payment":
        return {
            "message": "Pedro, encontrei seu carrinho aprovado. Posso gerar um novo link de pagamento?",
            "next_action": "reissue_payment_link",
        }

    if latest.checkpoint_type == "recommendation_approved":
        return {
            "message": "Retomando de onde paramos: a recomendacao aprovada continua valida.",
            "next_action": "confirm_cart",
        }

    return {
        "message": "Vou retomar sua conversa com base no ultimo estado salvo.",
        "next_action": latest.payload["next_safe_action"],
    }
```

### Estruturas de estado por feature

#### Schema 1: Descoberta de produto

- **Campos que não podem sumir:** restrições, objetivos, preferências de sabor, orçamento, frequência de treino.
- **Momento de salvar:** antes de KODA prometer algo ao cliente.
- **Momento de recarregar:** início de cada turno, depois de restart, depois de timeout e antes de pagamento.
- **Exemplo de risco:** se esse estado sumir, KODA repete pergunta já respondida ou cria decisão incoerente.

#### Schema 2: Comparação de produtos

- **Campos que não podem sumir:** lista candidata, critérios de ranking, score por produto, motivo de rejeição.
- **Momento de salvar:** antes de KODA prometer algo ao cliente.
- **Momento de recarregar:** início de cada turno, depois de restart, depois de timeout e antes de pagamento.
- **Exemplo de risco:** se esse estado sumir, KODA repete pergunta já respondida ou cria decisão incoerente.

#### Schema 3: Carrinho

- **Campos que não podem sumir:** SKUs, quantidades, preço travado, cupom, frete, prazo e status de aprovação.
- **Momento de salvar:** antes de KODA prometer algo ao cliente.
- **Momento de recarregar:** início de cada turno, depois de restart, depois de timeout e antes de pagamento.
- **Exemplo de risco:** se esse estado sumir, KODA repete pergunta já respondida ou cria decisão incoerente.

#### Schema 4: Pagamento

- **Campos que não podem sumir:** payment_intent_id, status, link gerado, tentativa atual e idempotency key.
- **Momento de salvar:** antes de KODA prometer algo ao cliente.
- **Momento de recarregar:** início de cada turno, depois de restart, depois de timeout e antes de pagamento.
- **Exemplo de risco:** se esse estado sumir, KODA repete pergunta já respondida ou cria decisão incoerente.

#### Schema 5: Entrega

- **Campos que não podem sumir:** reserva de estoque, endereço, transportadora, janela prometida e status de rastreio.
- **Momento de salvar:** antes de KODA prometer algo ao cliente.
- **Momento de recarregar:** início de cada turno, depois de restart, depois de timeout e antes de pagamento.
- **Exemplo de risco:** se esse estado sumir, KODA repete pergunta já respondida ou cria decisão incoerente.

#### Schema 6: Suporte pós-venda

- **Campos que não podem sumir:** pedido relacionado, motivo do contato, promessa feita e próxima ação.
- **Momento de salvar:** antes de KODA prometer algo ao cliente.
- **Momento de recarregar:** início de cada turno, depois de restart, depois de timeout e antes de pagamento.
- **Exemplo de risco:** se esse estado sumir, KODA repete pergunta já respondida ou cria decisão incoerente.

### Cartões de persistência por cliente

#### Caso de persistência 1: Marina

- **Estado crítico:** comparação final entre whey isolado e proteína vegetal.
- **Arquivo principal:** `customer_profile.json` mais `order_state.json` quando houver intenção de compra.
- **Banco:** SQLite guarda índice por `conversation_id`, `customer_id` e `current_stage`.
- **Checkpoint mínimo:** salvar antes de resposta com preço, prazo, SKU ou pagamento.
- **Falha evitada:** não repetir descoberta inicial.
- **Resposta de recuperação:** KODA retoma com contexto específico, não com saudação genérica.

#### Caso de persistência 2: Pedro

- **Estado crítico:** recuperação de carrinho depois de pagamento falho.
- **Arquivo principal:** `customer_profile.json` mais `order_state.json` quando houver intenção de compra.
- **Banco:** SQLite guarda índice por `conversation_id`, `customer_id` e `current_stage`.
- **Checkpoint mínimo:** salvar antes de resposta com preço, prazo, SKU ou pagamento.
- **Falha evitada:** não montar carrinho do zero.
- **Resposta de recuperação:** KODA retoma com contexto específico, não com saudação genérica.

#### Caso de persistência 3: Rafael

- **Estado crítico:** stack sem cafeína para treino noturno.
- **Arquivo principal:** `customer_profile.json` mais `order_state.json` quando houver intenção de compra.
- **Banco:** SQLite guarda índice por `conversation_id`, `customer_id` e `current_stage`.
- **Checkpoint mínimo:** salvar antes de resposta com preço, prazo, SKU ou pagamento.
- **Falha evitada:** não sugerir pré-treino estimulante.
- **Resposta de recuperação:** KODA retoma com contexto específico, não com saudação genérica.

#### Caso de persistência 4: Bianca

- **Estado crítico:** pedido com cupom e frete grátis.
- **Arquivo principal:** `customer_profile.json` mais `order_state.json` quando houver intenção de compra.
- **Banco:** SQLite guarda índice por `conversation_id`, `customer_id` e `current_stage`.
- **Checkpoint mínimo:** salvar antes de resposta com preço, prazo, SKU ou pagamento.
- **Falha evitada:** não aplicar cupom fora da regra.
- **Resposta de recuperação:** KODA retoma com contexto específico, não com saudação genérica.

#### Caso de persistência 5: Lucas

- **Estado crítico:** compra recorrente de creatina.
- **Arquivo principal:** `customer_profile.json` mais `order_state.json` quando houver intenção de compra.
- **Banco:** SQLite guarda índice por `conversation_id`, `customer_id` e `current_stage`.
- **Checkpoint mínimo:** salvar antes de resposta com preço, prazo, SKU ou pagamento.
- **Falha evitada:** não reabrir consultoria completa.
- **Resposta de recuperação:** KODA retoma com contexto específico, não com saudação genérica.

#### Caso de persistência 6: Ana

- **Estado crítico:** restrição a glúten e preferência por baunilha.
- **Arquivo principal:** `customer_profile.json` mais `order_state.json` quando houver intenção de compra.
- **Banco:** SQLite guarda índice por `conversation_id`, `customer_id` e `current_stage`.
- **Checkpoint mínimo:** salvar antes de resposta com preço, prazo, SKU ou pagamento.
- **Falha evitada:** não tratar sabor como alergia.
- **Resposta de recuperação:** KODA retoma com contexto específico, não com saudação genérica.

#### Caso de persistência 7: João

- **Estado crítico:** pedido corporativo para academia.
- **Arquivo principal:** `customer_profile.json` mais `order_state.json` quando houver intenção de compra.
- **Banco:** SQLite guarda índice por `conversation_id`, `customer_id` e `current_stage`.
- **Checkpoint mínimo:** salvar antes de resposta com preço, prazo, SKU ou pagamento.
- **Falha evitada:** não misturar cliente pessoa física com B2B.
- **Resposta de recuperação:** KODA retoma com contexto específico, não com saudação genérica.

#### Caso de persistência 8: Nina

- **Estado crítico:** troca de produto por sabor indisponível.
- **Arquivo principal:** `customer_profile.json` mais `order_state.json` quando houver intenção de compra.
- **Banco:** SQLite guarda índice por `conversation_id`, `customer_id` e `current_stage`.
- **Checkpoint mínimo:** salvar antes de resposta com preço, prazo, SKU ou pagamento.
- **Falha evitada:** não confirmar SKU sem estoque.
- **Resposta de recuperação:** KODA retoma com contexto específico, não com saudação genérica.

#### Caso de persistência 9: Caio

- **Estado crítico:** comparação por preço por dose.
- **Arquivo principal:** `customer_profile.json` mais `order_state.json` quando houver intenção de compra.
- **Banco:** SQLite guarda índice por `conversation_id`, `customer_id` e `current_stage`.
- **Checkpoint mínimo:** salvar antes de resposta com preço, prazo, SKU ou pagamento.
- **Falha evitada:** não escolher só preço total.
- **Resposta de recuperação:** KODA retoma com contexto específico, não com saudação genérica.

#### Caso de persistência 10: Lara

- **Estado crítico:** suporte pós-venda com atraso de entrega.
- **Arquivo principal:** `customer_profile.json` mais `order_state.json` quando houver intenção de compra.
- **Banco:** SQLite guarda índice por `conversation_id`, `customer_id` e `current_stage`.
- **Checkpoint mínimo:** salvar antes de resposta com preço, prazo, SKU ou pagamento.
- **Falha evitada:** não prometer nova data sem Fulfillment.
- **Resposta de recuperação:** KODA retoma com contexto específico, não com saudação genérica.

#### Caso de persistência 11: Otávio

- **Estado crítico:** carrinho com dois endereços possíveis.
- **Arquivo principal:** `customer_profile.json` mais `order_state.json` quando houver intenção de compra.
- **Banco:** SQLite guarda índice por `conversation_id`, `customer_id` e `current_stage`.
- **Checkpoint mínimo:** salvar antes de resposta com preço, prazo, SKU ou pagamento.
- **Falha evitada:** não fechar antes de confirmar endereço.
- **Resposta de recuperação:** KODA retoma com contexto específico, não com saudação genérica.

#### Caso de persistência 12: Sofia

- **Estado crítico:** cliente indecisa que pede opinião pessoal.
- **Arquivo principal:** `customer_profile.json` mais `order_state.json` quando houver intenção de compra.
- **Banco:** SQLite guarda índice por `conversation_id`, `customer_id` e `current_stage`.
- **Checkpoint mínimo:** salvar antes de resposta com preço, prazo, SKU ou pagamento.
- **Falha evitada:** não esconder trade-offs importantes.
- **Resposta de recuperação:** KODA retoma com contexto específico, não com saudação genérica.

### KODA Walkthrough: Pedro perde o carrinho — e recupera

Este é o cenário que abriu o módulo. Vamos ver como a state persistence de Nível 3 transforma um desastre em uma pausa de 15 segundos.

**Antes (sem Nível 3):**
```
21:03 Pedro: "Pode finalizar. Gera o link."
21:03 KODA: gera link de pagamento (MAS NÃO SALVA NADA)
21:04 Servidor: reinicia (deploy de rotina)
21:04 Pedro: "Deu erro no pagamento. Tenta de novo?"
21:04 KODA: "Oi! Como posso te ajudar?"
       [Pedro perdeu 47 minutos. Carrinho, perfil, restrições — tudo sumiu.]
```

**Depois (com Nível 3):**

**21:02 — KODA monta carrinho de Pedro:**
- Whey Isolado Baunilha 900g — R$ 189,90
- Creatina Monohidratada 300g — R$ 59,90
- Pré-treino Sem Cafeína 150g — R$ 79,90
- Multivitamínico 60 caps — R$ 49,90
- Frete grátis ( acima de R$ 300)
- Total: R$ 379,60

**21:02:30 — Checkpoint ANTES do link:**
```sql
-- SQLite: salva carrinho completo
INSERT INTO customer_cart (customer_id, cart_json, created_at)
VALUES ('wa_5511998765432', '{"items": [...4 itens...], "total": 379.60}', '2026-05-26T21:02:30Z');

-- JSON: snapshot do estado de pagamento
-- payment_checkpoint.json:
{
  "customer_id": "wa_5511998765432",
  "stage": "payment_pending",
  "cart_total": 379.60,
  "checkpoint_time": "2026-05-26T21:02:30Z"
}
```

**21:03 — Gera link e salva estado de pagamento:**
```sql
INSERT INTO payment_state (transaction_id, customer_id, status, link, created_at)
VALUES ('tx_pedro_20260526_001', 'wa_5511998765432', 'link_generated', 'https://pay.koda.com/tx_pedro_001', '2026-05-26T21:03:00Z');
```

**21:04 — Servidor reinicia.**

**21:04:02 — Recovery Agent detecta restart:**
1. Consulta SQLite: `SELECT * FROM payment_state WHERE customer_id = 'wa_5511998765432' ORDER BY created_at DESC LIMIT 1`.
2. Encontra transação `tx_pedro_20260526_001` com status `link_generated`.
3. Reidrata `customer_profile.json` (restrições de Pedro).
4. Reidrata `customer_cart` (carrinho com 4 itens).

**21:04:03 — Pedro pergunta:**
```
Pedro: "Deu erro no pagamento. Tenta de novo?"
```

**KODA (menos de 1s depois):**
```
"Pedro, seu carrinho ainda está salvo:
- Whey Isolado Baunilha 900g (R$ 189,90)
- Creatina Monohidratada 300g (R$ 59,90)
- Pré-treino Sem Cafeína 150g (R$ 79,90)
- Multivitamínico 60 caps (R$ 49,90)
Total: R$ 379,60 com frete grátis.

O link anterior pode ter expirado. Gerar um novo?"
```

**Resultado:** Pedro nem percebeu que o servidor reiniciou. O KODA lembrou de tudo. 47 minutos de conversa não foram perdidos.

**O que tornou isso possível:**
1. **Checkpoint ANTES de ação irreversível** — salvar estado antes de gerar link, não depois.
2. **Recovery Agent** — um agente dedicado a detectar estado órfão após restart.
3. **SQLite + JSON** — SQLite para queries (último estado do cliente) e JSON para snapshots auditáveis.
4. **Idempotency** — transaction_id garante que o mesmo link não seja gerado duas vezes.

A diferença entre perder o cliente e manter o cliente foram 3 queries e 15 segundos de recovery.

---

## 🗂️ Parte 3: Coordenação Baseada em Arquivos no KODA

### O incidente de Marina

Marina pediu para fechar o whey isolado chocolate sem lactose.
O Discovery Agent entendeu corretamente.
O Order Agent leu estado antigo.
O Fulfillment Agent reservou um SKU antes da aprovação.
O Delivery worker preparou mensagem final rápido demais.
Cada agente parecia útil.
O sistema inteiro ficou errado.
File-based coordination resolve esse tipo de falha criando um lugar comum para combinar trabalho.
O file system vira coordination bus.
Não porque arquivos são mágicos.
Porque arquivos são visíveis, auditáveis, simples de inspecionar e fáceis de retomar depois de falha.

### Protocolo mínimo de arquivos

| Arquivo | Quem escreve | Quem lê | Função no KODA |
| --- | --- | --- | --- |
| conversation_event.json | WhatsApp ingress | Discovery, Planner | Evento bruto com idempotency key |
| discovery.json | Discovery Agent | Planner, Order, Evaluator | Intenção, restrições e preferências |
| order.lock.json | Order Agent | Todos os agentes de pedido | Impede dois pedidos simultâneos |
| order_draft.json | Order Agent | Evaluator, Fulfillment | Pedido proposto antes de aprovação |
| evaluation.json | Evaluator Agent | Fulfillment, Generator | Decisão final de segurança e qualidade |
| status.json | Cada agente | Orchestrator, Recovery | Progresso visível de cada etapa |
| manifest.json | Orchestrator | Auditoria e suporte | Lista de artefatos usados na resposta |

### `lock.json` para impedir pedido duplo

```json
{
  "lock_name": "order_creation",
  "conversation_id": "wa_marina_2026_05_26",
  "owner_agent": "order_agent",
  "owner_run_id": "run_8421",
  "acquired_at": "2026-05-26T21:12:08Z",
  "expires_at": "2026-05-26T21:14:08Z",
  "protected_resource": "order_draft",
  "reason": "creating order draft for approved discovery intent"
}
```

### `status.json` para progresso visível

```json
{
  "conversation_id": "wa_marina_2026_05_26",
  "stage": "order_evaluation",
  "status": "running",
  "started_at": "2026-05-26T21:12:14Z",
  "updated_at": "2026-05-26T21:12:18Z",
  "required_inputs": ["discovery.json", "order_draft.json"],
  "expected_outputs": ["evaluation.json"],
  "blocked_by": [],
  "visible_to_support": true
}
```

### `manifest.json` para audit trail

```json
{
  "conversation_id": "wa_marina_2026_05_26",
  "customer_message_id": "wamid_001",
  "response_message_id": "wamid_002",
  "decision": "ask_payment_confirmation",
  "audit_refs": [
    "conversation_event.json",
    "discovery.json",
    "order_draft.json",
    "evaluation.json",
    "final_response.txt"
  ],
  "critical_facts_used": [
    "intolerancia_lactose",
    "budget_22000_cents",
    "preferred_flavor_chocolate",
    "delivery_neighborhood_pinheiros"
  ]
}
```

### Atomic write no fluxo KODA

```python
def write_json_atomic(path, payload):
    temp_path = path + ".tmp"
    write_json(temp_path, payload)
    fsync(temp_path)
    rename(temp_path, path)


def create_order_draft(conversation_id, draft):
    with acquire_lock(f"runs/{conversation_id}/order.lock.json"):
        write_json_atomic(
            f"runs/{conversation_id}/order_draft.json",
            draft,
        )
        write_json_atomic(
            f"runs/{conversation_id}/status.json",
            {"stage": "order_draft", "status": "completed"},
        )
```

### Como o fluxo impede a venda duplicada

```
ANTES:
WhatsApp event chega
  -> Discovery processa
  -> Order processa ao mesmo tempo
  -> Fulfillment reserva cedo demais
  -> Cliente recebe pedido errado

DEPOIS:
WhatsApp event vira conversation_event.json
  -> Discovery escreve discovery.json
  -> status.json marca discovery completed
  -> Order tenta order.lock.json
  -> Order escreve order_draft.json.tmp
  -> atomic rename publica order_draft.json
  -> Evaluator aprova ou rejeita
  -> Fulfillment só roda com evaluation approved
  -> manifest.json registra tudo que sustentou a resposta
```

### Cartões de coordenação por feature

#### Caso de coordenação 1: Criação de pedido

- **Mecanismo principal:** lock em `order.lock.json`.
- **Risco evitado:** dois Order Agents criando o mesmo pedido.
- **Arquivo de status:** mostra se a etapa está `pending`, `running`, `completed`, `failed` ou `blocked`.
- **Audit trail:** `manifest.json` lista inputs e outputs usados na mensagem ao cliente.
- **Critério de sucesso:** qualquer pessoa do suporte consegue reconstruir a decisão sem perguntar ao modelo.

#### Caso de coordenação 2: Reserva de estoque

- **Mecanismo principal:** status `evaluation approved` obrigatório.
- **Risco evitado:** Fulfillment reservar SKU rejeitado.
- **Arquivo de status:** mostra se a etapa está `pending`, `running`, `completed`, `failed` ou `blocked`.
- **Audit trail:** `manifest.json` lista inputs e outputs usados na mensagem ao cliente.
- **Critério de sucesso:** qualquer pessoa do suporte consegue reconstruir a decisão sem perguntar ao modelo.

#### Caso de coordenação 3: Cupom promocional

- **Mecanismo principal:** manifest com regra de cupom usada.
- **Risco evitado:** suporte não conseguir explicar desconto.
- **Arquivo de status:** mostra se a etapa está `pending`, `running`, `completed`, `failed` ou `blocked`.
- **Audit trail:** `manifest.json` lista inputs e outputs usados na mensagem ao cliente.
- **Critério de sucesso:** qualquer pessoa do suporte consegue reconstruir a decisão sem perguntar ao modelo.

#### Caso de coordenação 4: Troca de sabor

- **Mecanismo principal:** arquivo `replacement_options.json`.
- **Risco evitado:** Generator oferecer SKU sem estoque.
- **Arquivo de status:** mostra se a etapa está `pending`, `running`, `completed`, `failed` ou `blocked`.
- **Audit trail:** `manifest.json` lista inputs e outputs usados na mensagem ao cliente.
- **Critério de sucesso:** qualquer pessoa do suporte consegue reconstruir a decisão sem perguntar ao modelo.

#### Caso de coordenação 5: Pagamento reemitido

- **Mecanismo principal:** idempotency key no `payment_state.json`.
- **Risco evitado:** cliente receber dois links para pedidos diferentes.
- **Arquivo de status:** mostra se a etapa está `pending`, `running`, `completed`, `failed` ou `blocked`.
- **Audit trail:** `manifest.json` lista inputs e outputs usados na mensagem ao cliente.
- **Critério de sucesso:** qualquer pessoa do suporte consegue reconstruir a decisão sem perguntar ao modelo.

#### Caso de coordenação 6: Entrega expressa

- **Mecanismo principal:** lock em `delivery_quote.lock.json`.
- **Risco evitado:** duas cotações conflitantes aparecerem.
- **Arquivo de status:** mostra se a etapa está `pending`, `running`, `completed`, `failed` ou `blocked`.
- **Audit trail:** `manifest.json` lista inputs e outputs usados na mensagem ao cliente.
- **Critério de sucesso:** qualquer pessoa do suporte consegue reconstruir a decisão sem perguntar ao modelo.

#### Caso de coordenação 7: Recomendação recorrente

- **Mecanismo principal:** status por etapa de renovação.
- **Risco evitado:** KODA pular validação de restrição antiga.
- **Arquivo de status:** mostra se a etapa está `pending`, `running`, `completed`, `failed` ou `blocked`.
- **Audit trail:** `manifest.json` lista inputs e outputs usados na mensagem ao cliente.
- **Critério de sucesso:** qualquer pessoa do suporte consegue reconstruir a decisão sem perguntar ao modelo.

#### Caso de coordenação 8: Suporte pós-venda

- **Mecanismo principal:** manifest apontando pedido original.
- **Risco evitado:** atendente investigar conversa errada.
- **Arquivo de status:** mostra se a etapa está `pending`, `running`, `completed`, `failed` ou `blocked`.
- **Audit trail:** `manifest.json` lista inputs e outputs usados na mensagem ao cliente.
- **Critério de sucesso:** qualquer pessoa do suporte consegue reconstruir a decisão sem perguntar ao modelo.

#### Caso de coordenação 9: Produto em pré-venda

- **Mecanismo principal:** arquivo `availability_policy.json`.
- **Risco evitado:** KODA prometer entrega impossível.
- **Arquivo de status:** mostra se a etapa está `pending`, `running`, `completed`, `failed` ou `blocked`.
- **Audit trail:** `manifest.json` lista inputs e outputs usados na mensagem ao cliente.
- **Critério de sucesso:** qualquer pessoa do suporte consegue reconstruir a decisão sem perguntar ao modelo.

#### Caso de coordenação 10: Pedido B2B

- **Mecanismo principal:** lock por conta corporativa.
- **Risco evitado:** dois vendedores internos mexerem no mesmo orçamento.
- **Arquivo de status:** mostra se a etapa está `pending`, `running`, `completed`, `failed` ou `blocked`.
- **Audit trail:** `manifest.json` lista inputs e outputs usados na mensagem ao cliente.
- **Critério de sucesso:** qualquer pessoa do suporte consegue reconstruir a decisão sem perguntar ao modelo.

### KODA Walkthrough: Rafael e a conversa de 4 horas que não perdeu a cafeína

Rafael passou 4 horas no WhatsApp com o KODA. Ele detalhou sua rotina de treino, restrições alimentares, preferências de sabor, orçamento. No minuto 15, ele disse: "evito cafeína, atrapalha meu sono". Quatro horas depois, o KODA não deveria recomendar um pré-treino com 200mg de cafeína.

**Sem Compaction (Nível 1 e 2):**
- Histórico bruto: 120.000 tokens.
- O fato "evito cafeína" está em 3 tokens no meio de 120.000.
- O Generator recebe 120K tokens de contexto e precisa encontrar esses 3 tokens relevantes.
- Resultado: frequentemente perde. Recomenda pré-treino com cafeína.

**Com Compaction (Nível 3):**

**Passo 1: Extrair fatos do histórico bruto (4 horas de conversa).**
```json
{
  "extracted_facts": [
    {
      "type": "critical_restriction",
      "fact": "evitar cafeína",
      "reason": "atrapalha o sono",
      "mentioned_at": "00:15:00",
      "severity": "health",
      "priority": "critical"
    },
    {
      "type": "budget",
      "fact": "orçamento máximo R$ 350",
      "mentioned_at": "00:22:00",
      "priority": "critical"
    },
    {
      "type": "goal",
      "fact": "hipertrofia, treino 5x/semana",
      "mentioned_at": "00:05:00",
      "priority": "high"
    },
    {
      "type": "preference",
      "fact": "prefere whey isolado a concentrado",
      "mentioned_at": "01:30:00",
      "priority": "medium"
    },
    {
      "type": "social",
      "fact": "conversa sobre o tempo em SP",
      "mentioned_at": "02:10:00",
      "priority": "low"
    }
  ],
  "total_raw_tokens": 120000,
  "extracted_critical_tokens": 1800,
  "extracted_high_tokens": 3000,
  "extracted_medium_tokens": 5000
}
```

**Passo 2: Construir compacted_context.json.**
```json
{
  "compacted_context": {
    "critical_facts": [
      "CLIENTE DEVE EVITAR CAFEÍNA — atrapalha o sono (mencionado 00:15)",
      "Orçamento máximo: R$ 350",
      "Intolerante à lactose"
    ],
    "high_priority": [
      "Objetivo: hipertrofia, treino 5x/semana",
      "Prefere produtos com boa avaliação (4.5+)"
    ],
    "medium_priority": [
      "Prefere whey isolado a concentrado",
      "Sabor preferido: chocolate, mas aceita baunilha"
    ],
    "conversation_summary": "Rafael é um atleta experiente buscando stack completo para hipertrofia. Discutiu 8 produtos, comparou preços, tem restrições claras de cafeína e lactose. Está pronto para decidir após 4h de consulta."
  },
  "compacted_token_count": 9800,
  "raw_token_count": 120000,
  "compression_ratio": "12.2:1",
  "validated_against": "customer_profile.json",
  "validation_passed": true
}
```

**Passo 3: Validar compacted_context contra customer_profile.json.**
O Compaction Validator compara cada critical_fact extraído com a fonte de verdade (`customer_profile.json`). Se houver divergência (ex: orçamento sumarizado como R$ 420 mas o perfil diz R$ 350), o resumo é rejeitado e refeito.

**Passo 4: Generator recebe 9.800 tokens (em vez de 120.000).**
Com apenas os fatos relevantes, o Generator:
- Vê claramente "EVITAR CAFEÍNA" como critical_fact.
- Não recomenda pré-treino com cafeína.
- Tem 110.200 tokens livres para raciocinar com qualidade.
- Resposta é precisa e rápida.

**O que mudou:**
- De 120K tokens de ruído para 9.8K tokens de sinal.
- Fato crítico (cafeína) não está mais diluído — está em destaque como critical_fact.
- Validação cruzada com `customer_profile.json` garante que o resumo não contradiz o estado persistido.
- Economia de ~110K tokens por conversa longa = redução significativa de custo operacional.

**Regra de ouro da compactação no KODA:** fatos que afetam SAÚDE (alergias, restrições médicas), DINHEIRO (orçamento, preço acordado) ou CONFIANÇA (promessas de prazo, garantias) são sempre critical. Nunca são sumarizados. São injetados literalmente no contexto de todo agente downstream.

---

## 🗜️ Parte 4: Compactação Server-Side no KODA

### Conversas de 4 horas não são raridade

Um cliente que compra suplemento pela primeira vez pode conversar por 20 minutos.
Um cliente experiente pode comparar marcas por 90 minutos.
Um cliente com restrições médicas pode passar a manhã inteira perguntando detalhes.
Rafael fez isso.
Ele treinava havia três anos.
Tinha intolerância à lactose e glúten.
Treinava à noite.
Queria evitar cafeína.
Comparou 12 produtos.
Falou de marcas antigas.
Perguntou sobre interações entre suplementos.
Depois de 4 horas, pediu uma decisão final.
O KODA sabia muita coisa.
Mas o contexto tinha ruído demais.
Server-side compaction nasce para guardar o que importa e reduzir o resto.

### Classificação de prioridade para KODA

| Prioridade | Exemplo KODA | Ação de compactação |
| --- | --- | --- |
| Crítica | alergia a amendoim, intolerância à lactose, orçamento máximo, endereço de entrega | preservar como fato estruturado e repetir em contexto ativo |
| Alta | produto favorito, objetivo de treino, frequência semanal, pedido em andamento | sumarizar com fonte e timestamp |
| Média | preferência de sabor, marca que cliente já usou, sensibilidade a preço | manter em resumo curto |
| Baixa | small talk sobre cachorro, piadas, repetição de agradecimento | descartar ou comprimir em nota social mínima |
| Transitória | pergunta já respondida sobre uma promoção expirada | remover do contexto ativo depois de registrar decisão |

### Antes e depois do token budget

```
CENÁRIO: Rafael conversa por 4h15

ANTES DA COMPACTAÇÃO:
System prompt KODA                         3.500 tokens
Histórico completo WhatsApp              132.000 tokens
Catálogo relevante                         8.000 tokens
Traces de recomendação                    14.000 tokens
Carrinho e estado                          4.000 tokens
Buffer de resposta                        12.000 tokens
-------------------------------------------------------
Total                                    173.500 tokens
Risco: alto, porque ruído social compete com restrições críticas

DEPOIS DA COMPACTAÇÃO SERVER-SIDE:
System prompt KODA                         3.500 tokens
Resumo crítico da conversa                 6.500 tokens
Fatos estruturados do cliente              2.000 tokens
Catálogo relevante                         8.000 tokens
Traces resumidos                           3.500 tokens
Carrinho e estado                          4.000 tokens
Buffer de resposta                        18.000 tokens
-------------------------------------------------------
Total                                     45.500 tokens
Economia                                  128.000 tokens
Risco: menor, porque fatos críticos ficam explícitos
```

### Pipeline de compactação

```
1. Ingestão
   Ler mensagens completas, state files e audit manifest

2. Segmentação
   Separar conversa por intenção: discovery, comparação, carrinho, pagamento, suporte

3. Extração crítica
   Puxar alergias, orçamento, endereço, SKUs, promessas, decisões e rejeições

4. Sumarização por etapa
   Criar resumo curto com timestamp e fonte

5. Validação
   Evaluator compara resumo com fatos persistidos

6. Publicação
   Escrever compacted_context.json e atualizar manifest

7. Injeção
   Próxima chamada do KODA recebe apenas o contexto útil
```

### Exemplo de `compacted_context.json`

```json
{
  "conversation_id": "wa_rafael_2026_05_26",
  "compaction_version": "koda-compaction-v3",
  "source_window": {
    "start": "2026-05-26T09:00:00Z",
    "end": "2026-05-26T13:15:00Z",
    "raw_tokens": 132000,
    "compacted_tokens": 6500
  },
  "critical_facts": [
    {"type": "restriction", "value": "intolerancia a lactose", "source": "msg_004"},
    {"type": "restriction", "value": "intolerancia a gluten", "source": "msg_004"},
    {"type": "avoid", "value": "cafeina", "source": "msg_079"},
    {"type": "budget", "value": "ate R$ 420", "source": "msg_112"}
  ],
  "active_decision": "comparar stack sem lactose, sem gluten e sem cafeina para treino noturno",
  "discarded_noise_summary": "Conversa social sobre rotina, cachorro e atrasos foi removida sem impacto comercial.",
  "validator_result": "approved"
}
```

### Estratégias de sumarização para KODA

#### Extractive summary

- **Como funciona:** copiar frases críticas exatas.
- **Exemplo KODA:** alergia a amendoim deve manter wording forte.
- **Regra:** se impacta segurança, preço, prazo ou confiança, não vira ruído.

#### Abstractive summary

- **Como funciona:** reescrever trechos longos em resumo fiel.
- **Exemplo KODA:** comparação de 12 marcas vira critérios finais.
- **Regra:** se impacta segurança, preço, prazo ou confiança, não vira ruído.

#### Structured facts

- **Como funciona:** salvar fatos em campos fixos.
- **Exemplo KODA:** budget, restrições, objetivo e endereço.
- **Regra:** se impacta segurança, preço, prazo ou confiança, não vira ruído.

#### Decision summary

- **Como funciona:** guardar decisão e motivo.
- **Exemplo KODA:** por que whey concentrado foi rejeitado.
- **Regra:** se impacta segurança, preço, prazo ou confiança, não vira ruído.

#### Promise ledger

- **Como funciona:** guardar promessa feita ao cliente.
- **Exemplo KODA:** entrega amanhã só se Fulfillment confirmou.
- **Regra:** se impacta segurança, preço, prazo ou confiança, não vira ruído.

### Cartões de compactação por momento da conversa

#### Janela 1: 0 a 30 minutos

- **Estratégia:** manter histórico completo.
- **Motivo KODA:** cliente ainda está construindo contexto.
- **Fatos nunca descartados:** alergias, restrições, orçamento, endereço, pedido e promessas.
- **Ruído candidato:** repetição de agradecimento, small talk e perguntas já resolvidas.
- **Métrica:** retenção de fatos críticos deve ficar acima de 99%.

#### Janela 2: 30 a 90 minutos

- **Estratégia:** sumarizar discovery antigo.
- **Motivo KODA:** preferências já viraram fatos estruturados.
- **Fatos nunca descartados:** alergias, restrições, orçamento, endereço, pedido e promessas.
- **Ruído candidato:** repetição de agradecimento, small talk e perguntas já resolvidas.
- **Métrica:** retenção de fatos críticos deve ficar acima de 99%.

#### Janela 3: 90 a 180 minutos

- **Estratégia:** compactar comparações rejeitadas.
- **Motivo KODA:** KODA precisa das razões, não de cada frase.
- **Fatos nunca descartados:** alergias, restrições, orçamento, endereço, pedido e promessas.
- **Ruído candidato:** repetição de agradecimento, small talk e perguntas já resolvidas.
- **Métrica:** retenção de fatos críticos deve ficar acima de 99%.

#### Janela 4: 180 a 300 minutos

- **Estratégia:** usar compacted_context como fonte primária.
- **Motivo KODA:** histórico bruto só entra sob demanda.
- **Fatos nunca descartados:** alergias, restrições, orçamento, endereço, pedido e promessas.
- **Ruído candidato:** repetição de agradecimento, small talk e perguntas já resolvidas.
- **Métrica:** retenção de fatos críticos deve ficar acima de 99%.

#### Janela 5: Pagamento

- **Estratégia:** preservar estado exato sem sumarizar valores.
- **Motivo KODA:** preço, SKU e frete precisam ser literais.
- **Fatos nunca descartados:** alergias, restrições, orçamento, endereço, pedido e promessas.
- **Ruído candidato:** repetição de agradecimento, small talk e perguntas já resolvidas.
- **Métrica:** retenção de fatos críticos deve ficar acima de 99%.

#### Janela 6: Pós-venda

- **Estratégia:** manter promise ledger.
- **Motivo KODA:** suporte precisa saber o que KODA prometeu.
- **Fatos nunca descartados:** alergias, restrições, orçamento, endereço, pedido e promessas.
- **Ruído candidato:** repetição de agradecimento, small talk e perguntas já resolvidas.
- **Métrica:** retenção de fatos críticos deve ficar acima de 99%.

---

## 🧬 Parte 5: Evolução de Harness no KODA

### O dia em que Fernando quis remover metade do código

O time KODA tinha orgulho da arquitetura v2.8.
Havia Context Loader.
Havia Planning Agent.
Havia Generator Agent.
Havia Evaluator Agent.
Havia Validation Layer.
Havia Budget Guard.
Havia Format Validator.
Havia Fallback Handler.
Havia History Compaction Layer.
Tudo tinha sido criado por um motivo real.
Mas o modelo mudou.
A janela de contexto cresceu.
O instruction following melhorou.
A autocorreção ficou mais forte.
Fernando perguntou a frase que ninguém queria encarar.
Isso ainda é necessário?

### Framework: ainda é necessário?

1. Qual falha concreta esse componente previne hoje?
2. Quantas vezes ele preveniu a falha nos últimos 90 dias?
3. Qual é o custo em tokens por turno?
4. Qual é o custo em latência por turno?
5. Qual é o custo de manutenção por mês?
6. Ele gera falso positivo que bloqueia venda correta?
7. O modelo atual já executa essa capacidade com qualidade suficiente?
8. Existe teste A/B ou replay que prove que remover é seguro?
9. Se removermos, qual rollback é possível em menos de 15 minutos?

### Análise de custo por componente

| Componente | Custo mensal | Falhas prevenidas | Risco de remover | Decisão KODA |
| --- | --- | --- | --- | --- |
| Context Loader antigo | 5.4M tokens + 450ms por turno | 12 em 145k turns | Médio | Reduzir para modo seletivo |
| Format Validator rígido | 120ms por turno | 3 falhas reais | Baixo | Remover em canary |
| Budget Guard | 80ms por turno | 41 conversas salvas | Alto | Manter |
| Evaluator de alergia | 900 tokens por recomendação | 18 incidentes evitados | Muito alto | Manter sempre |
| Fallback genérico | Complexidade operacional | 0 usos em 60 dias | Baixo | Remover depois de replay |

### Decision Record de evolução

```
# KODA-ADR-017: Reduzir Context Loader para modo seletivo

## Contexto
O Context Loader foi criado quando conversas acima de 40 minutos perdiam fatos críticos.
O modelo atual mantém melhor contexto e state persistence já salva fatos críticos.

## Evidência
Nos últimos 90 dias, o componente preveniu 12 falhas em 145.000 turns.
Ele adicionou 450ms por turno e 5.4M tokens por mês.
Gerou 340 falsos positivos, muitos em recomendação simples.

## Decisão
Manter Context Loader apenas para conversas acima de 90 minutos,
clientes com restrição crítica ou pedidos em pagamento.

## Plano de segurança
Rodar replay de 1.000 conversas.
Ativar canary para 10% do tráfego por 7 dias.
Rollback por flag `context_loader_mode=always`.

## Métricas de sucesso
Latência p95 reduzida em pelo menos 250ms.
Zero aumento em incidentes de alergia, orçamento ou pedido duplicado.
Redução de pelo menos 30% nos tokens do harness.
```

### Quando remover e quando manter

| Decisão | Quando usar | Exemplo KODA |
| --- | --- | --- |
| Remover | componente tem baixo uso real, alto custo e rollback simples | Format Validator duplicado pelo schema do Order Agent |
| Reduzir | componente ajuda em casos raros, mas não precisa rodar sempre | Context Loader só para conversas longas ou restrições críticas |
| Manter | componente protege segurança, dinheiro ou confiança | Evaluator de alergia antes de qualquer recomendação |
| Reescrever | componente ainda é necessário, mas o desenho antigo está pesado | Compaction Layer que mistura summary e audit trail |

### Cartões de evolução de harness

#### Evolução 1: Context Loader

- **Evidência observada:** modelo novo mantém 100K tokens com boa acurácia.
- **Ação proposta:** ativar só em conversas longas.
- **Experimento:** replay de conversas reais anonimizadas antes de canary.
- **Métrica de segurança:** nenhum aumento em incidente crítico.
- **Critério de reversão:** qualquer regressão em alergia, orçamento, pagamento ou entrega.

#### Evolução 2: Trace Layer verboso

- **Evidência observada:** auditoria nativa melhorou.
- **Ação proposta:** reduzir detalhes de baixo valor.
- **Experimento:** replay de conversas reais anonimizadas antes de canary.
- **Métrica de segurança:** nenhum aumento em incidente crítico.
- **Critério de reversão:** qualquer regressão em alergia, orçamento, pagamento ou entrega.

#### Evolução 3: Rubric duplicada

- **Evidência observada:** Evaluator e rubric checam o mesmo campo.
- **Ação proposta:** fundir verificações iguais.
- **Experimento:** replay de conversas reais anonimizadas antes de canary.
- **Métrica de segurança:** nenhum aumento em incidente crítico.
- **Critério de reversão:** qualquer regressão em alergia, orçamento, pagamento ou entrega.

#### Evolução 4: Fallback genérico

- **Evidência observada:** quase nunca usado.
- **Ação proposta:** trocar por fallback específico de feature.
- **Experimento:** replay de conversas reais anonimizadas antes de canary.
- **Métrica de segurança:** nenhum aumento em incidente crítico.
- **Critério de reversão:** qualquer regressão em alergia, orçamento, pagamento ou entrega.

#### Evolução 5: Prompt de segurança longo

- **Evidência observada:** políticas agora estão em JSON estruturado.
- **Ação proposta:** encurtar system prompt.
- **Experimento:** replay de conversas reais anonimizadas antes de canary.
- **Métrica de segurança:** nenhum aumento em incidente crítico.
- **Critério de reversão:** qualquer regressão em alergia, orçamento, pagamento ou entrega.

#### Evolução 6: Revalidação de catálogo

- **Evidência observada:** cache já tem versionamento forte.
- **Ação proposta:** validar apenas no checkout.
- **Experimento:** replay de conversas reais anonimizadas antes de canary.
- **Métrica de segurança:** nenhum aumento em incidente crítico.
- **Critério de reversão:** qualquer regressão em alergia, orçamento, pagamento ou entrega.

#### Evolução 7: Guard de preço

- **Evidência observada:** erro de preço ainda afeta dinheiro.
- **Ação proposta:** manter sem redução.
- **Experimento:** replay de conversas reais anonimizadas antes de canary.
- **Métrica de segurança:** nenhum aumento em incidente crítico.
- **Critério de reversão:** qualquer regressão em alergia, orçamento, pagamento ou entrega.

#### Evolução 8: Guard de alergia

- **Evidência observada:** erro afeta saúde e confiança.
- **Ação proposta:** manter e testar sempre.
- **Experimento:** replay de conversas reais anonimizadas antes de canary.
- **Métrica de segurança:** nenhum aumento em incidente crítico.
- **Critério de reversão:** qualquer regressão em alergia, orçamento, pagamento ou entrega.

### Padrão: corpus de eval amostrado de produção

O replay de conversas reais anonimizadas deixa de ser uma atividade genérica e vira um artefato nomeado: `production_sampled_eval_corpus`. Esse corpus é a ponte entre Harness Evolution e produção. Ele garante que uma remoção, simplificação ou troca de modelo seja testada contra casos que clientes reais já geraram, com privacidade e labels explícitos.

Um corpus válido para KODA registra:

| Campo | Por que existe | Exemplo |
|---|---|---|
| `case_id` | Permite repetir o mesmo caso em PRs futuros | `koda_prod_replay_rafael_caffeine_001` |
| Fonte | Liga fixture redigida ao trace/ticket original sem expor PII | `support_ticket_2026_05_118` |
| Cobertura | Mostra qual risco o caso representa | conversa longa, checkout, alergia, cupom, suporte |
| Redação | Prova que telefone, endereço e dados sensíveis foram removidos | `redaction_reviewed: true` |
| Label esperado | Define comportamento correto antes de rodar candidate | rejeitar pré-treino com cafeína |
| Baseline | Preserva resultado da versão atual | `prompt.koda.v3: pass` |
| Candidate | Registra resultado da mudança | `prompt.koda.v4: pass` |
| Retenção | Evita manter dado bruto por tempo indefinido | fixture redigida revisada mensalmente |

```yaml
production_sampled_eval_corpus:
  corpus_id: "koda_prod_sampled_eval_2026_05"
  owner: "conversational-core"
  selection_policy:
    source: "conversas reais anonimizadas"
    minimum_cases:
      long_context: 20
      checkout_payment: 20
      dietary_restriction: 20
      support_complaint: 10
  case_requirements:
    - case_id
    - expected_behavior
    - prohibited_behavior
    - state_fixture
    - baseline_result
    - redaction_status
  replay_before_canary: true
```

Nos cartões de evolução, a frase "replay de conversas reais anonimizadas antes de canary" deve ser lida como: selecionar casos para esse corpus, salvar baseline/candidate, rodar o tier adequado e anexar o relatório ao ADR ou PR de mudança.

---

## 🏗️ Parte 6: Arquitetura Integrada

### Os 5 padrões trabalhando juntos

```
                              WHATSAPP CLIENTE
                                     |
                                     v
+--------------------------------------------------------------------------+
|                            KODA INGRESS LAYER                            |
|  recebe mensagem, atribui event_id, salva conversation_event.json          |
+--------------------------------------------------------------------------+
                                     |
                                     v
+---------------------------+     +-----------------------------+
|      STATE PERSISTENCE    |<--->|       FILE COORDINATION     |
| SQLite checkpoints        |     | lock.json                   |
| customer_profile.json     |     | status.json                 |
| cart.json                 |     | manifest.json               |
| order_state.json          |     | atomic writes               |
+---------------------------+     +-----------------------------+
            |                                      |
            v                                      v
+--------------------------------------------------------------------------+
|                         MULTI-AGENT ORCHESTRATION                        |
|                                                                          |
|  +----------+   +-----------+   +----------+   +-----------+              |
|  | Planner  |-->| Discovery |-->| Catalog  |-->| Generator |              |
|  +----------+   +-----------+   +----------+   +-----------+              |
|        |              |              |              |                     |
|        v              v              v              v                     |
|  +----------+   +-----------+   +----------+   +-----------+              |
|  |Evaluator |-->|  Order    |-->|Fulfillment|->| Recovery  |              |
|  +----------+   +-----------+   +----------+   +-----------+              |
|                                                                          |
+--------------------------------------------------------------------------+
                                     |
                                     v
+--------------------------------------------------------------------------+
|                       SERVER-SIDE COMPACTION ENGINE                       |
| segmenta histórico, extrai fatos críticos, sumariza ruído, valida resumo  |
+--------------------------------------------------------------------------+
                                     |
                                     v
+--------------------------------------------------------------------------+
|                         HARNESS EVOLUTION LOOP                            |
| mede custo, replay, canary, ADR, remove ou simplifica componentes          |
+--------------------------------------------------------------------------+
                                     |
                                     v
                              RESPOSTA KODA NO WHATSAPP
```

### Estratégias de coordenação

| Strategy | Latency | Fault Tolerance | Auditability | KODA Fit |
| --- | --- | --- | --- | --- |
| Centralized orchestrator | Média, uma fila principal decide tudo | Boa se o orquestrador persistir estado | Alta, decisões ficam em um lugar | Ótimo para checkout e pagamento |
| Distributed agents | Baixa em tarefas paralelas | Variável, depende de locks e retry | Média se cada agente escreve manifest | Bom para discovery e enriquecimento de catálogo |
| Hybrid | Balanceada, centraliza o crítico e distribui o paralelo | Alta, porque estado crítico tem dono | Alta, porque manifest unifica a trilha | Melhor encaixe para KODA Nível 3 |

### Como os padrões se compõem

#### Multi-agent systems

- **Papel no KODA:** divide responsabilidades.
- **Falha se faltar:** sem isso, um único agente mistura descoberta, pedido e validação.
- **Integração:** publica artefatos que os outros padrões conseguem ler, validar e auditar.

#### State persistence

- **Papel no KODA:** mantém progresso fora da memória.
- **Falha se faltar:** sem isso, restart apaga carrinho e decisões.
- **Integração:** publica artefatos que os outros padrões conseguem ler, validar e auditar.

#### File-based coordination

- **Papel no KODA:** ordena trabalho entre agentes.
- **Falha se faltar:** sem isso, dois agentes criam verdades diferentes.
- **Integração:** publica artefatos que os outros padrões conseguem ler, validar e auditar.

#### Server-side compaction

- **Papel no KODA:** mantém contexto útil em sessões longas.
- **Falha se faltar:** sem isso, fatos críticos se diluem em ruído.
- **Integração:** publica artefatos que os outros padrões conseguem ler, validar e auditar.

#### Harness evolution

- **Papel no KODA:** remove peso morto com segurança.
- **Falha se faltar:** sem isso, a arquitetura fica lenta e cara.
- **Integração:** publica artefatos que os outros padrões conseguem ler, validar e auditar.

### Fluxo completo: Marina fecha compra

```
1. Marina escreve no WhatsApp:
   "Quero fechar o whey isolado chocolate sem lactose para Pinheiros."

2. Ingress salva conversation_event.json com idempotency key.

3. State Persistence carrega customer_profile.json:
   - intolerância a lactose
   - orçamento R$ 220
   - preferência chocolate
   - endereço provável Pinheiros

4. Planner define etapa:
   - order confirmation
   - não discovery inicial

5. Discovery atualiza intenção:
   - comprar whey isolado chocolate
   - confirmar entrega em Pinheiros

6. Order Agent tenta adquirir order.lock.json.

7. Order Agent escreve order_draft.json com atomic write.

8. Evaluator lê discovery.json e order_draft.json.

9. Evaluator aprova porque:
   - SKU é sem lactose
   - preço R$ 199,90 fica abaixo de R$ 220
   - estoque SP disponível
   - entrega em Pinheiros possível

10. Fulfillment reserva estoque depois da aprovação.

11. Generator cria resposta curta para WhatsApp.

12. manifest.json lista os artefatos usados.

13. Compaction Engine marca esse trecho como decisão crítica.

14. Harness Evolution registra métricas de latência e custo do fluxo.
```

### Matriz de composição por feature KODA

A tabela abaixo mostra como cada padrão de Nível 3 contribui para as features reais do KODA.

| Feature KODA | Multi-agent | State persistence | File coordination | Compaction | Harness evolution |
|---|---|---|---|---|---|
| Product Discovery | Discovery + Catalog + Generator | `customer_profile.json`, `discovery.json` | `discovery.lock.json`, `status.json` | Preserva restrições, remove conversa social | Mede custo do Catalog Agent vs acurácia |
| Cart Recovery | Recovery Agent reidrata estado | `cart.json`, SQLite checkpoint de pagamento | `recovery.lock.json` impede dupla recuperação | Mantém decisão de compra, remove histórico antigo | ADR sobre manter Recovery Agent dedicado |
| Order Confirmation | Order + Evaluator em sequência | `order_draft.json`, `order_state.json` | `order.lock.json` com TTL, atomic write | Preserva itens, preço e restrições no resumo | Mede latência do lock vs incidentes de pedido duplo |
| Payment Retry | Order Agent consulta estado salvo | `payment_state.json`, `payment_checkpoint.sqlite` | `payment.lock.json` por transaction_id | Preserva link, status e transaction_id | Canary para remover retry manual se recovery automático cobre 99% |
| Allergy Safety Check | Evaluator valida contra `customer_profile.json` | Tabela `customer_restrictions` no SQLite | `safety_check.status.json` com timestamp | Alergia é prioridade máxima, nunca sumarizada | Mede falsos positivos do checker vs alergias prevenidas |
| Fulfillment Tracking | Fulfillment Agent pós-aprovação | `fulfillment.json`, `delivery_promise.json` | `fulfillment.lock.json` por pedido | Preserva tracking e promessa de entrega | Remove Fulfillment Agent se Order Agent já cobre a etapa |
| Long Consultation (4h+) | Planner redefine etapas a cada fase | Checkpoint de fase salva resumo validado | `phase.status.json` marca progresso | Extrai fatos críticos, sumariza ruído, valida contra estado | Mede se o custo do Planner se paga em conversas acima de 2h |

Cada feature real do KODA pode ser lida como a combinação específica desses padrões. A resposta ao cliente nasce de artefatos auditáveis, não de improviso. O `manifest.json` de cada resposta lista exatamente quais arquivos e agentes participaram daquela decisão.

---

## 🧪 Parte 7: Exercícios Práticos

### Exercício 1: Diagnose uma falha de coordenação

**Cenário KODA:** Marina recebeu confirmação de whey concentrado, apesar de ter intolerância à lactose.

**Sua tarefa:**

1. Identifique quais agentes participaram.
2. Liste quais arquivos deveriam existir.
3. Explique qual lock faltou ou foi ignorado.
4. Escreva a resposta que KODA deve enviar ao cliente depois da correção.

**Critério de sucesso:**

- A resposta precisa citar artefatos concretos do KODA.
- A decisão precisa proteger cliente, dinheiro e confiança.
- O desenho precisa ser recuperável depois de falha.
- O exercício não deve depender de memória implícita do modelo.

**Resposta esperada em alto nível:**

- Você deve mostrar fluxo, estado, coordenação, validação e métrica.
- Se houver trade-off, documente por que aceitou esse custo.
- Se houver risco de segurança ou saúde, mantenha guard explícito.

### Exercício 2: Desenhe um schema de persistência

**Cenário KODA:** Pedro perdeu o carrinho depois de restart durante pagamento.

**Sua tarefa:**

1. Defina tabelas SQLite mínimas.
2. Defina `cart.json` e `payment_state.json`.
3. Explique a ordem de checkpoint.
4. Escreva a mensagem de recuperação.

**Critério de sucesso:**

- A resposta precisa citar artefatos concretos do KODA.
- A decisão precisa proteger cliente, dinheiro e confiança.
- O desenho precisa ser recuperável depois de falha.
- O exercício não deve depender de memória implícita do modelo.

**Resposta esperada em alto nível:**

- Você deve mostrar fluxo, estado, coordenação, validação e métrica.
- Se houver trade-off, documente por que aceitou esse custo.
- Se houver risco de segurança ou saúde, mantenha guard explícito.

### Exercício 3: Calcule token budget com compactação

**Cenário KODA:** Rafael conversou por 4h15 e precisa de decisão final.

**Sua tarefa:**

1. Estime tokens antes de compactar.
2. Classifique fatos críticos, altos, médios e baixos.
3. Calcule tokens depois de compactar.
4. Defina critério de validação do resumo.

**Critério de sucesso:**

- A resposta precisa citar artefatos concretos do KODA.
- A decisão precisa proteger cliente, dinheiro e confiança.
- O desenho precisa ser recuperável depois de falha.
- O exercício não deve depender de memória implícita do modelo.

**Resposta esperada em alto nível:**

- Você deve mostrar fluxo, estado, coordenação, validação e métrica.
- Se houver trade-off, documente por que aceitou esse custo.
- Se houver risco de segurança ou saúde, mantenha guard explícito.

### Exercício 4: Escreva um decision record de harness evolution

**Cenário KODA:** O time quer remover Format Validator duplicado.

**Sua tarefa:**

1. Liste evidências necessárias.
2. Defina experimento replay.
3. Defina canary e rollback.
4. Declare métricas de sucesso.

**Critério de sucesso:**

- A resposta precisa citar artefatos concretos do KODA.
- A decisão precisa proteger cliente, dinheiro e confiança.
- O desenho precisa ser recuperável depois de falha.
- O exercício não deve depender de memória implícita do modelo.

**Resposta esperada em alto nível:**

- Você deve mostrar fluxo, estado, coordenação, validação e métrica.
- Se houver trade-off, documente por que aceitou esse custo.
- Se houver risco de segurança ou saúde, mantenha guard explícito.

### Exercício 5: Desenhe um fluxo multi-agent

**Cenário KODA:** Bianca quer montar stack mensal com cupom, frete grátis e restrição a glúten.

**Sua tarefa:**

1. Escolha agentes envolvidos.
2. Defina outputs de cada agente.
3. Defina arquivos de coordenação.
4. Explique como Evaluator aprova ou rejeita.

**Critério de sucesso:**

- A resposta precisa citar artefatos concretos do KODA.
- A decisão precisa proteger cliente, dinheiro e confiança.
- O desenho precisa ser recuperável depois de falha.
- O exercício não deve depender de memória implícita do modelo.

**Resposta esperada em alto nível:**

- Você deve mostrar fluxo, estado, coordenação, validação e métrica.
- Se houver trade-off, documente por que aceitou esse custo.
- Se houver risco de segurança ou saúde, mantenha guard explícito.

### Gabarito orientativo resumido

#### Exercício 1: direção de solução (coordenação)

- Identifique os agentes: Discovery (registrou lactose), Order (leu estado antigo), Evaluator (validou contra estado incorreto).
- Arquivos ausentes: `profile.lock.json` (ninguém adquiriu lock antes de ler `customer_profile.json`).
- Correção: Order Agent deve adquirir `profile.lock.json` antes de ler perfil. Evaluator deve comparar timestamp do perfil com timestamp da resposta no manifest.
- Métrica: redução de recomendações inseguras para zero em 30 dias.

#### Exercício 2: direção de solução (persistência)

- Tabelas SQLite: `customer_cart` (cart_id, customer_id, items_json, created_at, updated_at), `payment_checkpoint` (tx_id, cart_id, status, link, created_at).
- Arquivos: `cart.json` (itens, preços, descontos), `payment_state.json` (transaction_id, status, link, attempts).
- Ordem: salvar `cart.json` → gerar link → salvar `payment_state.json` → só então responder ao cliente.
- Mensagem de recuperação: "Pedro, seu carrinho com Whey Isolado, Creatina e Multivitamínico ainda está salvo. Quer retomar de onde paramos?"
- Métrica: recovery_time_p95 abaixo de 30s. Zero carrinhos perdidos após restart.

#### Exercício 3: direção de solução (token budget com compactação)

- Baseline 6h: ~120K tokens (histórico bruto) + 5K (perfil) + 3K (catálogo) = 128K tokens.
- Classificação: fatos críticos (alergia=life, orçamento=money, promessa=trust) usam 2K tokens. Fatos altos (preferências, objetivos) usam 3K. Médios (comparações feitas) usam 5K. Baixos/ruído (small talk) descartados.
- Compaction target: 10K tokens de fatos + 5K de resumo de conversa = 15K em vez de 120K.
- Economia: 105K tokens (87% de redução). Espaço liberado para o Generator raciocinar com qualidade.
- Métrica: retenção de fatos críticos acima de 99% em amostragem de 100 conversas de 6h+.

#### Exercício 4: direção de solução (ADR de harness evolution)

- Componente questionado: Context Loader (injeta `customer_profile.json` a cada turno).
- Custo medido: 450ms de latência, 1200 tokens por turno, R$ 0,003 por turno. Em 100K turns/mês: R$ 300/mês.
- Valor medido: preveniu 12 falhas reais em 145K turns nos últimos 90 dias (0.008% de prevenção). Gerou 340 falsos positivos (alarme sem risco real).
- Replay: rodou 50 conversas com e sem Context Loader. Resultado: diferença de acurácia de 0.3% (dentro da margem de erro).
- Decisão: REMOVER. Rollback por feature flag `context_loader_enabled`. Canary por 7 dias.
- Métrica pós-remoção: acurácia de recomendação não caiu. Latência p95 caiu 380ms.

#### Exercício 5: direção de solução (fluxo multi-agent)

- Agentes: Planner → Discovery → Catalog → Generator → Evaluator → Order → Fulfillment.
- Outputs: `discovery.json` (intenção, restrição glúten, preferências), `catalog_results.json` (SKUs filtrados), `generator_draft.json` (stack proposto), `evaluator_verdict.json` (aprova/rejeita cada item contra glúten e orçamento), `order_draft.json` (pedido final), `fulfillment.json` (tracking).
- Arquivos de coordenação: `discovery.lock.json` → `catalog.lock.json` → `order.lock.json` → `fulfillment.lock.json`. `status.json` marca etapa atual. `manifest.json` lista todos os artefatos usados na resposta final.
- Evaluator: verifica cada SKU contra `customer_profile.json` restrições (glúten). Verifica total contra orçamento. Verifica se cupom foi aplicado corretamente (sem double-discount). Se score < 7.5, rejeita com feedback específico.
- Métrica: acurácia de stack recomendado (todos os itens atendem restrições e orçamento).

---

## 📅 Parte 8: Checklist de Implementação

### Plano semana a semana

### Semana 1: Mapear fluxos críticos

- [ ] listar features KODA com risco de cliente
- [ ] coletar 20 conversas longas
- [ ] marcar falhas de coordenação, estado e contexto
- [ ] Documentar evidência em `docs/evidence/` ou no trace interno do KODA
- [ ] Validar com pelo menos uma conversa real anonimizada

### Semana 2: Introduzir artefatos multi-agent

- [ ] definir Planner, Discovery, Generator, Evaluator, Order e Fulfillment
- [ ] escrever contratos de input e output
- [ ] rodar replay offline
- [ ] Documentar evidência em `docs/evidence/` ou no trace interno do KODA
- [ ] Validar com pelo menos uma conversa real anonimizada

### Semana 3: Implementar state persistence mínima

- [ ] criar tabelas SQLite
- [ ] criar checkpoints JSON
- [ ] testar restart no meio do carrinho
- [ ] Documentar evidência em `docs/evidence/` ou no trace interno do KODA
- [ ] Validar com pelo menos uma conversa real anonimizada

### Semana 4: Adicionar file-based coordination

- [ ] implementar lock files
- [ ] status files e manifest
- [ ] testar pedido duplicado e atomic write
- [ ] Documentar evidência em `docs/evidence/` ou no trace interno do KODA
- [ ] Validar com pelo menos uma conversa real anonimizada

### Semana 5: Ativar compaction server-side

- [ ] classificar fatos por prioridade
- [ ] criar compacted_context.json
- [ ] validar retenção de fatos críticos
- [ ] Documentar evidência em `docs/evidence/` ou no trace interno do KODA
- [ ] Validar com pelo menos uma conversa real anonimizada

### Semana 6: Fechar harness evolution loop

- [ ] medir custo por componente
- [ ] criar ADRs
- [ ] rodar canary para simplificação segura
- [ ] Documentar evidência em `docs/evidence/` ou no trace interno do KODA
- [ ] Validar com pelo menos uma conversa real anonimizada

### Semana 7: Integrar observabilidade

- [ ] dashboards por agente
- [ ] métricas de recovery
- [ ] alerta para locks expirados
- [ ] Documentar evidência em `docs/evidence/` ou no trace interno do KODA
- [ ] Validar com pelo menos uma conversa real anonimizada

### Semana 8: Treinar suporte e engenharia

- [ ] playbook de incidente
- [ ] leitura de manifest
- [ ] procedimento de resposta ao cliente
- [ ] Documentar evidência em `docs/evidence/` ou no trace interno do KODA
- [ ] Validar com pelo menos uma conversa real anonimizada

### Checklist por padrão

#### Multi-agent systems

- [ ] Cada agente tem responsabilidade única
- [ ] Planner define etapa atual
- [ ] Evaluator é independente do Generator
- [ ] Cliente continua vendo um único KODA

#### State persistence

- [ ] Todo pedido tem checkpoint antes de pagamento
- [ ] Estado crítico está em SQLite ou JSON
- [ ] Recovery Agent sabe retomar por checkpoint
- [ ] Restart em ambiente de teste não perde carrinho

#### File-based coordination

- [ ] Arquivos são escritos com atomic rename
- [ ] Locks têm owner, expiration e reason
- [ ] Status é visível para suporte
- [ ] Manifest liga resposta final aos artefatos

#### Server-side compaction

- [ ] Fatos críticos são extraídos antes de sumarizar
- [ ] Resumo é validado contra estado persistido
- [ ] Token budget antes e depois é registrado
- [ ] Conversas de 6+ horas mantêm restrições

#### Harness evolution

- [ ] Cada componente tem custo medido
- [ ] Cada remoção tem ADR
- [ ] Replay precede canary
- [ ] Rollback por flag existe antes da mudança

### Sinais de que a implementação está pronta

- ✅ Um restart no meio do pagamento de Pedro não perde carrinho.
- ✅ Dois agentes não conseguem criar pedido para Marina ao mesmo tempo.
- ✅ Uma conversa de 4 horas com Rafael preserva lactose, glúten, cafeína e orçamento.
- ✅ O suporte consegue abrir `manifest.json` e explicar por que KODA respondeu algo.
- ✅ Fernando consegue apontar um componente do harness e ver custo, valor e decisão atual.

### Anti-padrões comuns na implantação do Nível 3

Evite estes erros que times cometem ao aplicar os 5 padrões pela primeira vez:

**Anti-padrão 1: Agentes demais cedo demais.** Criar Discovery, Catalog, Order, Fulfillment, Recovery e Support Agent antes de ter um Planner maduro e state persistence funcional. Sem Planner, os agentes não sabem de quem é a vez. Sem estado, cada agente recria trabalho.

**Anti-padrão 2: Locks sem TTL.** Adquirir lock sem configurar `expires_at`. Se o processo morrer, o lock fica eterno e o recurso trava. Todo lock deve ter expiration curta (5-30s para pedidos, 60s para carrinho) e um Recovery Agent que saiba expirar locks órfãos.

**Anti-padrão 3: Compaction antes de classificar fatos.** Rodar sumarização sem antes extrair fatos críticos e marcá-los como prioridade máxima. O resumo fica bom de ler, mas perde alergia, orçamento ou promessa. A ordem correta é: extrair → classificar → sumarizar → validar contra estado persistido.

**Anti-padrão 4: Remover harness sem replay.** Ver que o modelo novo é melhor e remover o guard imediatamente. Semanas depois, um bug de borda aparece em produção e ninguém lembra que o guard prevenia exatamente aquele cenário. Sempre rode replay com 50+ conversas antes de remover.

**Anti-padrão 5: Manifest gerado só quando dá tempo.** Tratar `manifest.json` como feature opcional ou de debugging. Quando o suporte precisa explicar uma decisão, o manifest não existe. Manifest deve ser obrigatório para toda resposta que afeta dinheiro, saúde, prazo ou confiança do cliente.

**Anti-padrão 6: Checkpoint só no final.** Salvar estado apenas quando a conversa termina. Se o servidor reinicia no meio, perde-se tudo. Checkpoint deve ser incremental: após cada decisão importante (restrição registrada, carrinho montado, pagamento iniciado).

Estes anti-padrões são comuns porque parecem "otimizações" ou "simplificações" na hora de implementar. Mas cada um deles já causou incidentes reais no KODA. A disciplina do Nível 3 existe para prevenir exatamente esses cenários.

---

## 📊 Parte 9: Métricas de Impacto Esperado

### Métricas por padrão

| Padrão | Métrica principal | Baseline provável | Meta Nível 3 | Impacto KODA |
| --- | --- | --- | --- | --- |
| Multi-agent | Acurácia de recomendação validada | 82% | 92%+ | Menos respostas que ignoram restrição ou orçamento |
| Multi-agent | Auditabilidade por decisão | 35% | 95%+ | Suporte reconstrói decisões sem adivinhar |
| State persistence | Recovery time após restart | 5 a 20 min ou perda total | menos de 30s | Cliente retoma carrinho sem recomeçar |
| State persistence | Perda de estado crítico | 1 a 3% das conversas longas | 0.1% ou menos | Menos abandono por esquecimento |
| File coordination | Pedidos duplicados por 10k pedidos | 8 a 15 | 0 a 1 | Menos estorno e suporte manual |
| File coordination | Trace completeness | 50% | 98%+ | Cada resposta tem manifest auditável |
| Compaction | Economia de tokens em 4h+ | 0% | 60% a 75% | Custo menor e resposta mais focada |
| Compaction | Retenção de fatos críticos em 6h+ | 85% a 92% | 99%+ | Alergias e orçamento não somem |
| Harness evolution | Redução de latência p95 | 0ms | 250ms a 600ms | WhatsApp parece mais rápido |
| Harness evolution | Redução de complexidade | 11 componentes ativos | 6 a 8 com valor provado | Menos manutenção e onboarding mais fácil |

### Como medir sem se enganar

- Meça por conversa, não apenas por chamada de LLM.
- Separe conversas curtas de conversas com 2h, 4h e 6h.
- Registre quando o cliente forneceu o fato crítico e quando KODA usou esse fato.
- Compare custo do harness com incidentes realmente prevenidos.
- Use replay de conversas reais anonimizadas antes de confiar em canary.
- Para segurança, trate falso negativo como mais grave que falso positivo.

### Métricas por persona de cliente

| Persona | Métrica | Exemplo KODA |
| --- | --- | --- |
| Cliente iniciante | tempo até primeira recomendação segura | KODA pergunta restrições antes de produto |
| Cliente avançado | qualidade de comparação por critério | KODA mantém preço por dose, pureza e objetivo |
| Cliente com alergia | zero recomendação insegura | Evaluator bloqueia produto incompatível |
| Cliente em pagamento | taxa de recuperação após erro | Payment Retry consulta estado antes de gerar outro link |
| Cliente pós-venda | rastreabilidade de promessa | manifest mostra prazo prometido e fonte |

### Dashboard mínimo

```
KODA Nivel 3 Dashboard

Multi-agent
  - planner_stage_accuracy
  - evaluator_rejection_rate
  - generator_repair_success_rate

State persistence
  - checkpoint_write_success_rate
  - recovery_time_p95
  - lost_cart_incidents

File coordination
  - lock_contention_rate
  - expired_lock_count
  - manifest_completeness_rate

Compaction
  - raw_tokens_per_long_conversation
  - compacted_tokens_per_long_conversation
  - critical_fact_retention_rate

Harness evolution
  - harness_tokens_per_turn
  - harness_latency_p95
  - component_prevention_rate
  - false_positive_rate
```

### Expectativa realista de impacto

#### Primeiro mês

- **Impacto esperado:** mais visibilidade que economia.
- **Exemplo KODA:** o time descobre onde o KODA falha de verdade.
- **Sinal de maturidade:** o time toma decisões por evidência, não por sensação.

#### Segundo mês

- **Impacto esperado:** menos incidentes de pedido e recuperação melhor.
- **Exemplo KODA:** Pedro não perde carrinho e Marina não recebe pedido duplicado.
- **Sinal de maturidade:** o time toma decisões por evidência, não por sensação.

#### Terceiro mês

- **Impacto esperado:** custo começa a cair com compaction e harness evolution.
- **Exemplo KODA:** Fernando remove peso morto com segurança.
- **Sinal de maturidade:** o time toma decisões por evidência, não por sensação.

#### Depois de seis meses

- **Impacto esperado:** arquitetura vira prática operacional.
- **Exemplo KODA:** novas features já nascem com estado, manifest e métricas.
- **Sinal de maturidade:** o time toma decisões por evidência, não por sensação.

---

### 📚 Caderno de Referência Rápida para Implementação KODA

Use esta seção durante design reviews, incident reviews e planejamento de features.

### Referência: Multi-agent systems

- **Pergunta de review:** Quem decide?
- **Resposta KODA:** Planner define etapa. Evaluator aprova risco. Order cria pedido. Fulfillment executa depois de aprovação.
- **Evidência mínima:** trace, checkpoint, manifest ou métrica de produção.

### Referência: State persistence

- **Pergunta de review:** O que precisa sobreviver?
- **Resposta KODA:** Perfil, restrição, orçamento, carrinho, pagamento, promessa e etapa atual.
- **Evidência mínima:** trace, checkpoint, manifest ou métrica de produção.

### Referência: File-based coordination

- **Pergunta de review:** Como impedir corrida?
- **Resposta KODA:** Locks por recurso, status por etapa, atomic write e manifest por resposta.
- **Evidência mínima:** trace, checkpoint, manifest ou métrica de produção.

### Referência: Server-side compaction

- **Pergunta de review:** O que merece continuar no contexto?
- **Resposta KODA:** Fatos críticos, decisões, promessas e razões de rejeição.
- **Evidência mínima:** trace, checkpoint, manifest ou métrica de produção.

### Referência: Harness evolution

- **Pergunta de review:** O que pode sair?
- **Resposta KODA:** Componentes com baixo valor medido, alto custo e rollback seguro.
- **Evidência mínima:** trace, checkpoint, manifest ou métrica de produção.

### Guia rápido de revisão por cenário KODA

Use esta tabela durante design reviews e incident reviews para verificar cobertura dos 5 padrões.

| Cenário KODA | Multi-agent | State persistence | File coordination | Compaction | Harness evolution |
|---|---|---|---|---|---|
| Cliente pede whey sem lactose | Discovery registra restrição; Evaluator valida | `customer_profile.json` persiste alergia | `safety_check.status.json` antes de responder | Alergia é prioridade máxima, nunca sumarizada | Mede falsos positivos do safety checker |
| Cliente volta após erro de pagamento | Recovery Agent reidrata estado | `cart.json`, `payment_state.json`, SQLite checkpoint | `payment.lock.json` por transaction_id | Preserva link, status, valor; remove duplicatas | ADR sobre manter Recovery Agent dedicado |
| Cliente troca endereço no último minuto | Order Agent atualiza `order_draft.json` | `delivery_address.json` com versão | `order.lock.json` com TTL curto | Preserva novo endereço, invalida rota antiga | Mede latência do lock vs incidentes de entrega errada |
| Cliente compara duas marcas por preço/dose | Catalog Agent retorna tabela; Generator cria comparação | Cache de comparação em `comparison_cache.json` | `catalog.lock.json` evita leitura desatualizada | Preserva critérios de comparação, remove produtos descartados | Mede custo do Catalog Agent vs acurácia de preço vivo |
| Cliente tem alergia crítica a amendoim | Evaluator com rubrica de segurança reforçada | Tabela `critical_restrictions` com flag de severidade | `safety_check.lock.json` com prioridade sobre outros locks | Alergia crítica NUNCA é sumarizada, sempre injetada | Mede falsos negativos (risco de vida) com tolerância zero |
| Cliente quer entrega amanhã em Pinheiros | Fulfillment Agent valida viabilidade | `delivery_promise.json` com ETA e restrições | `fulfillment.lock.json` por pedido | Preserva promessa de prazo, remove alternativas descartadas | Remove Fulfillment Agent se Order já cobre o cenário |
| Cliente reclama de atraso | Support Agent lê manifest | `manifest.json` + `delivery_promise.json` originais | `support.lock.json` para evitar respostas conflitantes | Preserva promessa original e timeline de eventos | ADR para decidir entre Support Agent dedicado vs Recovery Agent |
| Cliente pede renovação mensal automática | Subscription Agent em background | `subscription.json` com renewal_date e status | `subscription.lock.json` com TTL de 24h | Preserva preferências e data; remove histórico de renovações passadas | Mede custo do Subscription Agent vs churn evitado |
| Cliente pede nota fiscal para empresa | Order Agent gera NF a partir do estado final | `invoice.json` com dados fiscais do pedido | `invoice.lock.json` por pedido | Preserva dados fiscais; remove rascunhos de cálculo | Mede se NF deveria ser feature do Order Agent ou agente separado |

---

### 🧩 Catálogo de Decisões Arquiteturais do KODA Nível 3

Decisões recorrentes que o time enfrenta ao aplicar os 5 padrões no KODA. Cada linha é uma decisão que merece documentação explícita (ADR, comment no código ou registro no trace).

| Decisão | Gatilho | Resposta KODA | Quem decide | Artefato |
|---|---|---|---|---|
| Alergia registrada no começo da conversa | Cliente menciona restrição | Persistir como fato crítico e injetar em toda recomendação | Discovery → SQLite | `customer_profile.json` |
| Orçamento muda no meio da jornada | Cliente redefine limite | Criar checkpoint, invalidar recomendações acima do novo teto | Planner → Order | `budget_checkpoint.json` |
| Cliente some e volta após 2 dias | Session expirada ou cliente retoma | Reidratar estado do último checkpoint, resumir conversa anterior | Recovery Agent | `recovery_context.json` |
| Pagamento falha no gateway | Timeout ou recusa da adquirente | Manter transaction_id, não gerar link novo sem confirmação do cliente | Order Agent | `payment_state.json` |
| Produto sai de estoque durante checkout | Inventário atualizado entre etapas | Remover do carrinho, sugerir alternativas, notificar Planner | Catalog → Order | `stock_event.json` |
| Dois cupons aplicáveis ao mesmo carrinho | Cliente tem cupom + promo ativa | Aplicar maior desconto, registrar o outro como não aplicado | Order → Evaluator | `coupon_resolution.json` |
| Harness bloqueia venda correta | Falso positivo do safety checker | Registrar no dashboard do componente, revisar threshold | Evaluator | `false_positive_event.jsonl` |
| Dois eventos WhatsApp chegam fora de ordem | Latência de rede ou retry do webhook | Ordenar por timestamp e idempotency key antes de processar | Ingress Layer | `event_queue.json` |
| Suporte precisa explicar resposta ao cliente | Reclamação ou dúvida pós-venda | Abrir `manifest.json`, rastrear agentes e arquivos envolvidos | Support Agent | `manifest.json` |
| Modelo novo melhora instruction following | Lançamento de API com capacidades melhores | Rodar replay com conversas antigas, medir diferença, propor ADR | Harness Evolution | `model_upgrade_adr.md` |

### 🧪 Banco de Incidentes Simulados para Treino KODA

Use estes incidentes para treinar leitura de arquitetura sem depender de abstrações. Cada incidente simula uma falha que os 5 padrões de Nível 3 deveriam prevenir ou diagnosticar.

#### INC-001: Marina recebeu SKU com lactose

- **Sintoma:** Marina, intolerante à lactose, recebeu recomendação de whey concentrado com lactose.
- **Causa:** Discovery registrou restrição corretamente, mas Order Agent leu `customer_profile.json` em versão antiga (antes da atualização da restrição). Evaluator validou contra estado desatualizado.
- **Arquivos para abrir:** `manifest.json` da resposta → `status.json` da etapa Order → `customer_profile.json` para verificar versão.
- **Padrão exposto:** File-based coordination (falta de lock e atomic read no estado compartilhado).
- **Correção:** Order Agent deve adquirir `profile.lock.json` antes de ler `customer_profile.json`. Evaluator deve comparar timestamp do perfil com timestamp da resposta.

#### INC-002: Pedro perdeu carrinho depois de deploy

- **Sintoma:** Pedro montou carrinho com 4 itens (R$ 379,60). Deploy de rotina reiniciou o servidor. KODA esqueceu tudo e perguntou "Como posso ajudar?"
- **Causa:** Estado do carrinho existia apenas em memória do processo. Nenhum checkpoint em SQLite ou JSON foi salvo antes do link de pagamento.
- **Arquivos para abrir:** `payment_state.json` (deveria existir, não existe) → log de deploy para confirmar timestamp.
- **Padrão exposto:** State persistence (ausência de checkpoint antes de operação irreversível).
- **Correção:** Salvar `cart.json` e `payment_checkpoint.sqlite` ANTES de gerar link de pagamento. Recovery Agent deve detectar checkpoint órfão após restart e reidratar conversa.

#### INC-003: Rafael teve cafeína sugerida no fim de 4h

- **Sintoma:** Rafael passou 4h no WhatsApp detalhando rotina, restrições e preferências. No minuto 15 ele disse "evito cafeína, atrapalha meu sono". No final, KODA sugeriu pré-treino com 200mg de cafeína.
- **Causa:** Compaction classificou "evito cafeína" como preferência média (nível 3) e a sumarizou para "cliente tem algumas preferências de fórmula". O fato crítico foi diluído.
- **Arquivos para abrir:** `compacted_context.json` → `customer_profile.json` (fato original) → `manifest.json` da recomendação final.
- **Padrão exposto:** Server-side compaction (classificação incorreta de prioridade de fato).
- **Correção:** "Evitar cafeína" deve ser classificado como critical_fact, não preference. Compaction validator deve comparar fatos críticos extraídos com estado persistido antes de liberar o resumo.

#### INC-004: Lock ficou preso e bloqueou checkout

- **Sintoma:** Cliente tentou finalizar compra por 15 minutos. KODA respondia "Aguarde, estamos processando". O lock de pedido nunca foi liberado.
- **Causa:** Order Agent adquiriu `order.lock.json`, mas o processo que detinha o lock crashou antes de liberar. Lock não tinha TTL configurado.
- **Arquivos para abrir:** `order.lock.json` (verificar owner, timestamp, TTL) → `status.json` do pedido.
- **Padrão exposto:** File-based coordination (lock sem expiration).
- **Correção:** Todo lock deve ter `expires_at`. Recovery Agent deve expirar locks com mais de 60s e fazer rollback seguro do estado do pedido.

#### INC-005: Harness adicionou 900ms em conversa simples

- **Sintoma:** Cliente perguntou "Tem whey de chocolate?" e KODA levou 1.4s para responder "Sim, temos 3 opções". 900ms foram gastos em guards que não agregaram valor.
- **Causa:** Safety checker, budget guard, format validator e context loader rodavam em TODA mensagem, inclusive perguntas triviais. Nenhum componente tinha métrica de custo por chamada.
- **Arquivos para abrir:** Trace de latência da resposta → dashboard de custo por componente.
- **Padrão exposto:** Harness evolution (componentes sem medição de valor).
- **Correção:** Classificar mensagens por risco. Para perguntas triviais (risco baixo), pular budget guard e format validator. Medir latência e falsos positivos de cada componente. Criar ADR para remover guards que não previnem falhas reais.

#### INC-006: Resumo de 6h inverteu orçamento do cliente

- **Sintoma:** Após 6h de consulta, o resumo dizia "orçamento máximo: R$ 420". Mas o cliente tinha reduzido de R$ 420 para R$ 300 na hora 3 da conversa. KODA recomendou produtos acima do novo limite.
- **Causa:** Compaction preservou o primeiro valor de orçamento (timestamp mais antigo) e ignorou a atualização. O `compacted_context.json` não foi validado contra `customer_profile.json` antes de injetar no prompt do Generator.
- **Arquivos para abrir:** `compacted_context.json` (comparar versão do orçamento) → `customer_profile.json` (timestamp da última atualização).
- **Padrão exposto:** Server-side compaction + State persistence (falta de validação cruzada entre camadas).
- **Correção:** Compaction engine deve sempre comparar fatos extraídos com `customer_profile.json` (fonte de verdade). Orçamento é critical_fact e deve vencer qualquer versão sumarizada.

### 🧾 Templates de Review de Arquitetura para o KODA

Use estes templates durante design reviews e incident reviews. Cada template cobre um padrão do Nível 3.

**Review de Agente (Multi-agent):**
1. Qual é a responsabilidade única deste agente?
2. Qual arquivo ele lê? Qual arquivo ele escreve?
3. Quem valida sua saída? O que acontece se a validação falhar?
4. Como outro agente descobre que este agente terminou? (status file, event, callback)
5. Como este agente falha de modo seguro? (sem corromper estado compartilhado)

**Review de Estado (State persistence):**
1. Qual dado não pode sumir se o processo reiniciar?
2. Onde ele é salvo? (SQLite, JSON, ambos)
3. Quando ele é atualizado? (antes ou depois de cada etapa?)
4. Como é recuperado depois de restart? (qual agente reidrata?)
5. Qual versão de schema está em uso? (migration existe?)

**Review de Coordenação (File-based coordination):**
1. Qual recurso compartilhado existe? (carrinho, perfil, pedido)
2. Qual lock protege esse recurso? Qual TTL?
3. Qual status prova progresso? (etapa atual visível para todos os agentes)
4. Qual manifest explica a decisão final?
5. Qual cleanup existe para lock expirado?

**Review de Compactação (Server-side compaction):**
1. Quais fatos são críticos? (alergia, orçamento, promessa)
2. Como você classifica cada fato? (critical, high, medium, low)
3. Qual resumo foi gerado? Como foi validado?
4. Quanto token foi economizado vs baseline?
5. Qual fato crítico foi checado por amostragem após compactação?

**Review de Evolução (Harness evolution):**
1. Qual componente está sendo questionado? Por quê?
2. Qual custo medido ele tem? (latência, tokens, manutenção)
3. Qual falha real ele previne? (com evidência de produção)
4. Qual replay foi rodado? Qual resultado?
5. Qual rollback por flag existe antes da remoção?

## ✨ O Que Você Aprendeu

### 1. KODA precisa virar uma equipe interna

Um agente único pode parecer simples, mas conversas comerciais longas exigem Planner, Discovery, Generator, Evaluator, Order, Fulfillment e Recovery com responsabilidades claras.

### 2. Estado precisa sobreviver ao processo

Pedro não deveria perder 47 minutos porque um servidor reiniciou. SQLite, JSON checkpoints e recovery transforms falhas técnicas em pausas quase invisíveis.

### 3. Coordenação precisa ser explícita

Marina não deveria receber dois pedidos porque agentes correram em paralelo. Lock files, status files, atomic writes e manifest tornam o fluxo seguro e auditável.

### 4. Contexto longo precisa ser destilado

Rafael não precisa que KODA carregue cada piada da manhã inteira. Ele precisa que alergias, orçamento, decisões e promessas sigam vivos em 6+ horas de conversa.

### 5. Harness bom também envelhece

O componente que salvou o KODA seis meses atrás pode virar latência, custo e complexidade hoje. Harness evolution pergunta, mede e remove com segurança.

### 6. Os padrões só funcionam juntos

Multi-agent sem estado perde progresso. Estado sem coordenação cria conflito. Coordenação sem compactação degrada em conversas longas. Compactação sem evolução vira mais uma camada eterna.

### Key Takeaways no estilo KODA

- ✅ Se um agente precisa confiar em outro, a saída precisa existir fora da context window.
- ✅ Se um cliente já investiu tempo, o KODA deve tratar esse tempo como estado valioso.
- ✅ Se dois agentes podem tocar no mesmo pedido, precisa haver lock.
- ✅ Se uma conversa passa de 4 horas, o histórico bruto deixa de ser memória e vira ruído.
- ✅ Se um harness não prova valor em produção, ele precisa ser reduzido, reescrito ou removido.
- ✅ Se a decisão afeta saúde, dinheiro, prazo ou confiança, ela precisa de audit trail.
- ✅ Se suporte não consegue explicar a resposta do KODA, a arquitetura ainda não está pronta.

### A maturidade chega quando o time para de adivinhar

Nível 1 respondeu "o sistema quebrou?".
Nível 2 respondeu "consigo ver por que quebrou?".
Nível 3 responde "qual camada falhou, qual arquivo prova, e qual padrão conserta?".

Quando o time de Fernando começou este programa, cada incidente gerava horas de debugging e semanas de "vamos melhorar o prompt". Hoje, cada incidente começa com a abertura do `manifest.json`. Em 2 minutos, o time sabe qual agente decidiu o quê, com base em quais arquivos, validado por qual Evaluator.

Isso não é tecnologia. É disciplina. E você agora a tem.

### A frase que fecha Nível 3

> KODA não é confiável porque responde bem em uma chamada. KODA é confiável quando sobrevive a horas de conversa, falhas de processo, agentes paralelos, contexto grande e mudanças de modelo sem trair a confiança do cliente.

### O checklist mental do arquiteto Nível 3

Antes de sair deste módulo, memorize estas perguntas. Elas são o que separa um time que opera o KODA de um time que entende o KODA:

**Quando uma conversa começa:**
1. Quem decide a etapa atual? (Planner)
2. O estado da conversa sobrevive a um restart? (State persistence)
3. Se dois agentes tocarem no mesmo recurso, quem ganha? (File coordination)

**Quando uma conversa passa de 2 horas:**
4. O que é essencial manter no contexto? (Compaction — fatos críticos)
5. O que posso sumarizar sem perder segurança? (Compaction — classificação)
6. O resumo foi validado contra o estado persistido? (Compaction — validação cruzada)

**Quando a conversa termina:**
7. Consigo explicar cada decisão do KODA? (Manifest)
8. Se o cliente voltar amanhã, o KODA lembra? (Recovery)
9. Se o modelo melhorar, qual componente posso remover? (Harness evolution)

**Quando algo falha:**
10. Qual arquivo eu abro primeiro? (`manifest.json`)
11. Qual arquivo mostra o estado no momento da falha? (`status.json`)
12. Qual agente deveria ter bloqueado o erro? (Rastrear pelo manifest)
13. O que precisa mudar: prompt, estado, coordenação ou compactação?

Este checklist não é teórico. É o protocolo que o time do Fernando usa em toda revisão de incidente. Funcionou para Marina, Pedro, Rafael e centenas de outros clientes.

### O que Nível 3 muda na prática diária do time

| Antes do Nível 3 | Depois do Nível 3 |
|---|---|
| "O KODA respondeu errado, vamos ajustar o prompt" | "Vamos abrir o manifest e entender qual agente decidiu o quê" |
| "O servidor reiniciou, cliente perdeu tudo" | "Recovery Agent reidratou o estado, cliente nem percebeu" |
| "Dois pedidos foram gerados, como?" | "Lock não foi adquirido. Vamos ver o `order.lock.json`" |
| "Conversa de 5h, KODA esqueceu a alergia" | "Compaction preservou o fato crítico, alergia está no `compacted_context.json`" |
| "Temos 11 componentes, impossível manter" | "ADR #47: removemos 3 componentes com evidência de replay" |
| "Não sei por que o KODA recomendou isso" | "`manifest.json` linha 4: Generator usou `catalog_results.json` v2, aprovado pelo Evaluator com score 8.7" |

A diferença não está no modelo de linguagem. Está na disciplina arquitetural.

### Uma nota sobre responsabilidade

Fernando costuma dizer que Nível 3 é o ponto onde o time para de "torcer para o agente acertar" e passa a "exigir que o sistema prove que acertou".

Isso muda tudo.

Muda como você escreve código.
Muda como você revisa PR.
Muda como você responde a incidente.
Muda como você planeja feature nova.

Nível 1 deu fundação. Nível 2 deu visibilidade. Nível 3 dá responsabilidade.

Responsabilidade de que cada arquivo, cada lock, cada checkpoint e cada componente do harness existe por uma razão mensurável. E se essa razão deixar de existir, o componente sai.

Esse é o KODA que Fernando imaginou quando abriu a empresa.

Não um chatbot que responde bem.
Um sistema que honra o tempo, o dinheiro e a confiança de cada cliente que abre o WhatsApp.

Você agora sabe construir esse sistema.

---

## 🚀 Próximos Passos

### Imediatamente

1. Escolha uma conversa KODA longa com falha real ou simulada.
2. Reconstrua a jornada com os 5 padrões de Nível 3.
3. Liste quais artefatos deveriam existir em cada etapa.
4. Calcule quais fatos críticos precisavam sobreviver a compaction.
5. Escreva uma decisão de harness evolution para um componente existente.

### Na próxima semana

1. Implementar um checkpoint de carrinho para uma feature KODA.
2. Criar um `manifest.json` para uma resposta de recomendação.
3. Rodar replay de uma conversa com Marina, Pedro ou Rafael.
4. Medir token budget antes e depois de compactação.
5. Abrir um ADR para manter, reduzir ou remover um componente do harness.

### Ponte para Nível 4

Nível 3 ensinou arquitetura avançada aplicada ao KODA.
Nível 4 será mais específico.
Você vai sair do padrão geral e entrar no desenho próprio do produto KODA.
A pergunta muda.
Não será apenas: como sistemas multi-agent funcionam?
Será: qual é a arquitetura exata do KODA para jornadas de venda, checkout, fulfillment e suporte?
Nível 4 transforma este módulo em decisões de produto e implementação real.

### Leitura recomendada antes do Nível 4

- `04-nivel-4-koda-specific/01-koda-architecture.md`
- `04-nivel-4-koda-specific/02-customer-journey-flows.md`
- `04-nivel-4-koda-specific/03-feature-design-patterns.md`
- `04-nivel-4-koda-specific/04-evaluation-rubrics-koda.md`
- `04-nivel-4-koda-specific/05-harness-improvements.md`

---

## 📎 Metadata

| Campo | Valor |
| --- | --- |
| Arquivo | `curriculum/03-nivel-3-advanced-architecture/koda-applications/nivel-3-koda.md` |
| Documento | KODA Applications Level 3 |
| Programa | Building Long-Running Agents para KODA |
| Nível | 3 - Arquitetura Avançada |
| Tópicos conectados | Multi-agent systems, State persistence, File-based coordination, Server-side compaction, Harness evolution |
| Personagens e cenários | Fernando, Marina, Pedro, Rafael e clientes KODA de WhatsApp |
| Status | Production Ready para estudo curricular |
| Data | Maio 2026 |
| Equipe | FutanBear Technical Team |

Este documento representa a conclusão do Nível 3 do programa Building Long-Running Agents para KODA. Ele conecta sistemas multi-agente, persistência de estado, coordenação por arquivos, compactação server-side e evolução de harness ao agente de vendas WhatsApp da KODA.

Os padrões aqui documentados foram validados em incidentes reais, conversas de produção e decisões de arquitetura do time KODA ao longo de 2025-2026. Eles representam o estado da arte em agentes long-running aplicados a e-commerce conversacional.

Para dúvidas sobre aplicação prática, consulte os módulos individuais do Nível 3 em `curriculum/03-nivel-3-advanced-architecture/`. Para aprofundamento em features específicas do KODA, prossiga para o Nível 4.

*Documento: KODA Applications Level 3 | FutanBear Technical Team | Maio 2026*
*Versão: 1.0 | Autores: Fernando + Team | Status: Production Ready*
*Revisão: Primeira edição — cobre todos os 5 módulos do Nível 3 aplicados ao KODA*

---

*Fim do módulo. O KODA está mais forte. Você também.*
