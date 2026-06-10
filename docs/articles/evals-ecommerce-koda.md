---
aliases: ["evals ecommerce", "avaliação KODA", "ecommerce evals"]
---

# Das Promessas Falsas às Decisões Auditáveis: Como Evals Transformaram um Agente de E-Commerce no WhatsApp

**Por que a diferença entre um agente que "soa bem" e um agente que é bom está em uma camada de avaliação que a maioria dos times nunca constrói — e como o KODA construiu a sua.**

---

Eram 09h15 de uma manhã comum na KODA. Fernando Machado analisava uma conversa de WhatsApp que parecia simples: um cliente pedia recomendação de suplemento para ganhar massa, com orçamento de R$ 140 e uma restrição importante — gastrite.

O agente KODA tinha gerado uma resposta rápida. Três produtos populares, tom confiante, uma frase final chamando para compra. A mensagem era fluente. Era simpática. Era vendável.

E era exatamente por isso que era perigosa.

Fernando rodou o Evaluator — o componente que aplica rubricas de qualidade sobre cada saída do agente antes que ela chegue ao cliente. O resultado: `overall_score: 0.58`. O produto principal continha alto teor de cafeína. A resposta ignorava completamente a gastrite. O tom empurrava a compra antes de confirmar uma restrição médica.

A decisão foi `REJEITAR_IMEDIATAMENTE`. Não por estilo. Não por preferência subjetiva. Por risco real de negócio e saúde.

Sem o Evaluator, alguém poderia dizer: "a resposta está boa, só precisa de um ajuste fino". Com ele, a decisão ficou objetiva: **não publicar**.

Essa diferença — entre fluência e qualidade, entre "parece bom" e "é bom" — é o que separa agentes de IA que funcionam em demo de agentes que funcionam em produção. E a ponte entre esses dois mundos se chama **evals**.

**O que é o KODA:** um agente de vendas de suplementos nutricionais que opera via WhatsApp Business API, mantendo conversas de 30 minutos a 4 horas com clientes reais. Por trás da interface de chat, há oito agentes especializados — Discovery, Catalog, Generator, Evaluator, Order, Payment, Fulfillment e Recovery — coordenados por um Orchestrator. O KODA processa em média 340 pedidos por dia e opera com 98% de precisão em recomendações. A arquitetura completa está documentada no programa long-running-agents, um currículo open source de 12 semanas para construir sistemas de IA que operam de forma confiável por horas ou dias.

Este artigo conta como o time KODA construiu sua camada de evals. Você vai ver o modelo de maturidade que guiou a jornada, os padrões de arquitetura que operacionalizaram cada fase, e as rubricas reais que hoje decidem, de forma auditável, se uma mensagem de WhatsApp chega ou não ao cliente. Tudo baseado em código, conversas e decisões reais de produção.

---

## 1. Por Que Evals São Diferentes em Agentes de E-Commerce

Agentes de IA falham em execuções longas por três razões estruturais, bem documentadas no programa de long-running agents: perda de contexto (a janela de tokens enche e o agente "esquece" o que estava fazendo), planejamento frágil (sem decomposição, o agente tenta resolver tudo de uma vez e se perde), e autoavaliação cega (o mesmo modelo que gera também avalia, aprovando qualidade ruim como boa) (`README.md:7-13`).

Em e-commerce conversacional, essas três falhas ganham consequências específicas que vão muito além de uma resposta imprecisa:

**Risco médico e de segurança.** Um agente de suplementos não pode recomendar um pré-treino com 300mg de cafeína para um cliente que informou ter ansiedade e tomar café diariamente. Uma recomendação errada aqui não é apenas uma venda perdida — é um risco à saúde do cliente e à confiança na marca.

**Preço e estoque são fatos, não opiniões.** Se o agente promete um produto por R$ 89,90 que custa R$ 129,90, ou garante entrega same-day de um item fora de estoque, ele não está sendo "criativo". Está mentindo — mesmo que sem intenção. E o cliente só descobre horas depois, quando a frustração já está instalada.

**Margem e política comercial.** Um agente de vendas que cede desconto de 40% para fechar uma negociação está destruindo margem. Um que pressiona o cliente com urgência falsa ("últimas unidades, compre agora") está queimando relacionamento. Um que promete troca sem custo onde a política não permite está criando passivo operacional.

**Tom de voz é produto.** No WhatsApp, onde o KODA opera, a conversa é pessoal. Uma resposta fria a uma reclamação legítima, um follow-up genérico que ignora o contexto da conversa anterior, ou uma mensagem enviada fora do horário combinado transformam o agente de consultor confiável em spammer.

O problema central é que **modelos de linguagem são otimizados para fluência, não para correção**. Uma resposta pode ser gramaticalmente perfeita, empática e persuasiva — e ainda assim recomendar o produto errado, inventar um desconto ou ignorar uma alergia. Como diz o currículo KODA: "o ponto operacional é evitar que o KODA confunda fluência com qualidade. Uma mensagem pode ser natural e ainda estar errada. Uma mensagem pode vender bem e ainda violar margem. Uma mensagem pode ser simpática e ainda chegar no timing errado" (`curriculum/04-nivel-4-koda-specific/04-evaluation-rubrics-koda.md:341`).

É por isso que evals em agentes de e-commerce não podem ser um checklist binário de "funcionou ou não funcionou". Precisam ser um sistema de avaliação multidimensional, com critérios de negócio explícitos, bloqueadores automáticos e rastreabilidade completa de cada decisão.

---

## 2. O Modelo de Maturidade: 5 Fases para Sair do Achismo

Em junho de 2026, Phil Hetzel, da Braintrust, publicou uma análise sobre as fases de maturidade na adoção de evals em agentes de IA. O framework descreve uma progressão observada em empresas que saem de nenhum processo estruturado até evals integradas ao fluxo de desenvolvimento (`docs/analysis/2026-06-10-eval-maturity-phases/analysis.md:23`).

O insight mais importante do modelo não é a sequência em si — é o mecanismo de transição. **Cada fase só deve ser abandonada quando a dor da fase atual se torna insustentável.** Não se avança por calendário, se avança por sinal de saturação. E pular fases é a causa número um de infraestrutura de eval que ninguém usa, porque o time não construiu o músculo de rodar evals e agir sobre eles (`docs/analysis/2026-06-10-eval-maturity-phases/analysis.md:87`).

Vamos percorrer as cinco fases com exemplos concretos de como elas se manifestam em um agente de e-commerce como o KODA.

### Fase 1: Ad Hoc Testing — "Parece bom, vai"

O time testa prompts manualmente, mexe em dois ou três exemplos, e manda para produção baseado em sensação. Não há avaliação estruturada, repetibilidade, cobertura, nem capacidade de distinguir melhoria de regressão (`docs/analysis/2026-06-10-eval-maturity-phases/analysis.md:27`).

No KODA, essa era a realidade da Versão 1 (março de 2026): um agente único que respondia clientes no WhatsApp. Funcionava para conversas de 5 minutos. Quebrava em conversas de 2 horas. Quando uma mudança de prompt piorava as recomendações, o time só descobria por reclamação de cliente.

O sinal de saída da Fase 1 é inequívoco: **uma mudança que parecia boa piorou o produto e só foi descoberta por reclamação de usuário.** Se isso já aconteceu com você, você está pronto para a Fase 2.

### Fase 2: Spot Check Evals — "Temos 15 casos que rodamos antes de cada deploy"

O time escreve um conjunto pequeno de casos (10 a 50) em uma planilha ou script simples e os roda manual ou semi-automaticamente. O ganho é repetibilidade: pela primeira vez, é possível comparar a versão nova com a anterior nos mesmos inputs. A limitação é que os casos refletem apenas o que o time já conhece — são derivados de memória interna, não da distribuição real de uso (`docs/analysis/2026-06-10-eval-maturity-phases/analysis.md:28`).

No KODA, os primeiros spot checks nasceram das conversas que deram errado. Casos como:

- Cliente com alergia a amendoim recebendo recomendação de produto com traços de amendoim
- Cliente pedindo whey sem lactose recebendo whey concentrado tradicional
- Cliente com orçamento de R$ 100 recebendo recomendação de produto de R$ 189

Cada caso ganhou um `case_id`, um `expected_outcome` e um `baseline` — a resposta esperada do agente na versão atual. O padrão canônico do repositório define a estrutura completa: cada caso precisa de workflow, input, state fixture, expected outcome, acceptable tool behavior, baseline, grading notes e owner (`docs/canonical/repeatable-agent-spot-check-set.md:32-43`).

O sinal de saída da Fase 2: **os spot checks cresceram até ficar doloroso rodar manualmente, e casos escritos pelo time continuam deixando passar comportamentos inesperados de produção.**

### Fase 3: Structured Evals With Metrics — "Definimos o que 'bom' significa com números"

O time define critérios de qualidade mensuráveis, com test set, scoring e métricas acompanhadas ao longo do tempo. Entram accuracy, distribuição de latência e custo por eval run. O risco é acreditar em scores que não representam uso real ou critérios mal calibrados (`docs/analysis/2026-06-10-eval-maturity-phases/analysis.md:29`).

É nesta fase que as rubricas do KODA nascem. Em vez de "a resposta está boa?", a pergunta vira: qual o `overall_score` em cada dimensão? Accuracy do produto: 0.30. Relevance ao contexto: 0.70. Safety and constraints: 0.20. Com pesos e thresholds explícitos, o julgamento de qualidade vira medição repetível.

O sinal de saída da Fase 3: **os scores não correlacionam com o feedback real dos usuários.** O eval diz 0.92 mas o cliente reclama. É o momento de olhar para produção.

### Fase 4: Production-Grounded Evals — "Nosso eval set vem do tráfego real"

O eval set passa a ser construído por amostragem de tráfego real de produção: captura, armazenamento e replay de interações reais. A distribuição de teste passa a coincidir com a distribuição de uso. Entram A/B tests, canary deployments com eval gates e dashboards que correlacionam scores com métricas de produção (`docs/analysis/2026-06-10-eval-maturity-phases/analysis.md:30`).

Para o KODA, isso significa capturar conversas reais de WhatsApp (com privacidade e redação de dados sensíveis), rotular o expected behavior e rodar o agente candidato contra as mesmas interações que o agente atual enfrentou. O padrão canônico de Production-Grounded Eval Sampling define os requisitos: captura com filtros de privacidade, política de retenção, critérios de amostragem por segmento, cobertura de workflows críticos e replay infrastructure (`docs/canonical/production-grounded-eval-sampling.md:32-42`).

O sinal de saída da Fase 4: **você tem volume e representatividade, mas edge cases ainda escapam.** É quando o sistema precisa aprender sozinho com as próprias falhas.

### Fase 5: Continuous Eval-Driven Development — "Cada incidente vira um caso de regressão permanente"

Evals viram parte nativa do workflow de desenvolvimento. Cada PR tem resultados de eval anexados. Suites de regressão crescem automaticamente quando falhas de produção são detectadas. Existem tiers de eval por custo e profundidade. A característica-chave é o sistema ser **self-improving**: melhorar sem curadoria manual contínua (`docs/analysis/2026-06-10-eval-maturity-phases/analysis.md:31`).

No KODA, a Fase 5 se manifesta no Production Failure Regression Flywheel: cada falha de produção — seja uma reclamação de cliente, um edge case que escapou, um mal uso de ferramenta ou um gap de scoring — vira automaticamente um caso de regressão durável. O padrão define o ciclo completo: intake da falha, captura da interação e trace, aplicação de filtros de privacidade, rotulagem de expected behavior, deduplicação, atribuição ao tier correto e backfill para provar que o agente corrigido agora passa (`docs/canonical/production-failure-regression-flywheel.md:30-41`).

O princípio unificador do modelo é que **maturidade de eval não é uma escala de ferramenta — é uma escala de confiança operacional**. Cada fase remove uma fonte diferente de ilusão: a Fase 1 remove a ilusão de que feeling detecta regressão; a Fase 2 remove a ilusão de que memória humana basta; a Fase 3 remove a ausência de métricas; a Fase 4 remove a ilusão de que um test set manual representa usuários; a Fase 5 remove a dependência de curadoria manual para lembrar falhas passadas (`docs/analysis/2026-06-10-eval-maturity-phases/analysis.md:140`).

---

## 3. Os Padrões Que Operacionalizam as Fases

O repositório long-running-agents documenta 16 padrões canônicos de arquitetura para agentes. Desses, nove tratam diretamente de evals. Vou destacar os cinco que considero mais transformadores para times que operam agentes de e-commerce.

### Repeatable Agent Spot-Check Set

O primeiro passo de maturidade real. Um conjunto nomeado de 10 a 20 casos que cobrem os workflows de maior valor e maior risco do seu agente. Cada caso define: o que entra (input), que estado o agente precisa ter (state fixture), o que deve acontecer (expected outcome), quais ferramentas pode ou não usar, e qual foi o resultado da versão atual (baseline) (`docs/canonical/repeatable-agent-spot-check-set.md:32-43`).

O valor não está na cobertura — está na **repetibilidade**. Pela primeira vez, você consegue rodar os mesmos casos contra a versão atual e a candidata e ver, caso a caso, o que mudou. Para o KODA, o seed set inicial incluía: recomendação com restrição médica, negociação de preço no limite da margem, follow-up respeitando opt-out, e resposta a reclamação de produto errado.

### Eval Tier Stratification

Uma suíte única de evals não consegue dar feedback rápido para o desenvolvedor, proteger o PR e garantir confiança de release ao mesmo tempo. Se todo eval roda a cada edit, o inner loop fica lento demais. Se só existem checks rápidos, falhas caras de detectar escapam.

A solução é estratificar em três tiers (`docs/canonical/eval-tier-stratification.md:32-36`):

| Tier | Propósito | Quando roda | Duração típica | Poder de decisão |
|---|---|---|---|---|
| **Fast** | Confiança no inner loop para caminhos críticos | Local, pre-commit, PR pequeno | Segundos a poucos minutos | Bloqueia prontidão local ou PR se caminhos críticos regredirem |
| **Medium** | Evidência para mudanças de prompt, modelo, ferramenta ou loop | PR, draft review | Minutos a dezenas de minutos | Bloqueia merge exceto com waiver explícito |
| **Deep** | Confiança de release, canário e regressão de incidentes | Release candidate, nightly, pós-incidente | Dezenas de minutos a horas | Bloqueia rollout ou exige hold/rollback |

Cada suite carrega metadados: tier, runtime budget, cost budget, flakiness policy, trigger, threshold e owner. A estratificação permite que o time mantenha feedback rápido sem sacrificar cobertura profunda.

### Pain-Signal Eval Progression Gate

O padrão que responde à pergunta mais difícil: **quando investir no próximo nível de eval?** A resposta é: quando a dor atual provar que o nível presente saturou.

O gate mapeia sinais de dor a investimentos mínimos (`docs/canonical/pain-signal-eval-progression-gate.md:42-50`):

| Sinal de dor | Próximo investimento mínimo |
|---|---|
| Reclamações de usuário se repetem para fluxos conhecidos | Criar ou expandir o Spot-Check Set |
| Revisões manuais bloqueiam mudanças de prompt, modelo ou ferramenta | Adicionar Eval Tier Stratification e PR-Gated Eval Enforcement |
| Casos escritos à mão não capturam comportamento real | Adicionar Production-Grounded Eval Sampling |
| Scores discordam do feedback de reviewers ou usuários | Recalibrar rubricas, thresholds e correlation checks |
| Edge cases escapam e se repetem após correções | Adicionar Production Failure Regression Flywheel |

O gate produz um decision record com a dor observada, evidência-fonte, capacidade atual, próximo passo escolhido, owner, custo operacional esperado e data de revisão. Isso transforma investimento em eval de opinião para decisão rastreável.

### Production-Grounded Eval Sampling

Hand-crafted eval sets têm um viés estrutural: eles refletem o que o time **espera** que os usuários façam, não o que os usuários **realmente** fazem. Para agentes long-running, esse gap é especialmente perigoso porque falhas podem depender de duração da conversa, formato de resposta de ferramentas, histórico de estado, phrasing do usuário ou combinações inesperadas de workflow (`docs/canonical/production-grounded-eval-sampling.md:20-25`).

O padrão define oito requisitos: captura de interações de produção com traces e state snapshots, filtros de privacidade com redação de dados sensíveis, política de retenção com limites de tempo, critérios de amostragem por segmento e risco, metadados de cobertura, rotulagem de expected behavior, replay infrastructure que aplica prompt/modelo/tools candidatos contra os casos capturados, e cadência de refresh atrelada a mudanças de produto e tráfego.

O insight central: **a distribuição importa tanto quanto o score**. Um eval set com 500 casos que não representam o uso real é mais perigoso que um com 50 casos que representam — porque o score alto gera falsa confiança.

### Production Failure Regression Flywheel

O padrão que fecha o ciclo. Cada falha de produção que revela um gap comportamental vira um caso de regressão durável — a menos que seja explicitamente rejeitada como duplicada, inacionável ou fora de escopo (`docs/canonical/production-failure-regression-flywheel.md:28-30`).

O flywheel define oito passos: intake da falha, captura da interação com trace e state snapshot, filtros de privacidade, rotulagem de expected behavior e failure class, deduplicação, atribuição ao tier correto, backfill de baseline/candidato para provar que o caso falha antes e passa depois do fix, e link ao incidente ou PR que o originou.

Uma taxonomia de classes de falha ajuda a classificar cada regressão: prompt issue, tool misuse, context loss, state persistence corruption, scoring gap, latency ou cost regression, safety ou policy issue, e late-session failure.

O valor do flywheel está em **converter incidentes em ativos de desenvolvimento**. Cada falha que vira regressão reduz a dependência de memória humana e protege contra reincidência. O sistema aprende com os próprios erros.

---

## 4. Rubricas Operacionais: O Coração do KODA

Se os padrões canônicos são a arquitetura, as rubricas são o motor. No KODA, uma rubrica não é uma checklist vaga — é uma especificação operacional que transforma julgamento de qualidade em medição repetível e auditável.

O sistema opera com quatro famílias de rubricas, uma para cada tipo de interação crítica no funil de e-commerce (`curriculum/04-nivel-4-koda-specific/04-evaluation-rubrics-koda.md:48-49`):

| Família | `rubric_id` | Objetivo | `approval_threshold` |
|---|---|---|---|
| Product Recommendation | `koda.product_recommendation.v1` | Avaliar se uma recomendação é precisa, segura e personalizada | 0.82 |
| Customer Response | `koda.customer_response.v1` | Avaliar se uma resposta é correta, empática e resolve a intenção | 0.80 |
| Price Negotiation | `koda.price_negotiation.v1` | Avaliar se uma negociação combina assertividade, respeito e margem | 0.84 |
| Follow-Up | `koda.follow_up.v1` | Avaliar se um follow-up chega no timing certo com personalização | 0.78 |

### Anatomia de um Rubric KODA

Cada rubrica compartilha a mesma anatomia, com 12 componentes (`curriculum/04-nivel-4-koda-specific/04-evaluation-rubrics-koda.md:158-172`):

| Componente | Função | Exemplo |
|---|---|---|
| `rubric_id` | Identificador estável e versionado | `koda.product_recommendation.v1` |
| `Input Specification` | Dados mínimos que o Evaluator precisa receber | contexto do cliente, catálogo, restrições, draft |
| `dimensions` | Dimensões avaliadas separadamente, cada uma com peso, escala e critérios | accuracy (30%), relevance (25%), tone (15%) |
| `scale` | Escala fixa 0-5 por dimensão | 5 = excelente, 3 = aceitável com ressalvas, 0 = violação grave |
| `weights` | Peso de cada dimensão no `overall_score` | accuracy 30%, safety 20%, relevance 25% |
| `blockers` | Falhas que bloqueiam envio mesmo com score alto | preço falso, risco médico, promessa indevida |
| `approval_threshold` | Pontuação mínima ponderada para aprovar | 0.82 |
| `confidence_score` | Confiança do Evaluator na própria avaliação | 0.91 |
| `overall_score` | Resultado ponderado final | 0.87 |
| `examples` | Exemplos bons e ruins calibrados com mensagens reais | WhatsApp messages |
| `decision logic` | Algoritmo de decisão: blocker → `REJEITAR_IMEDIATAMENTE`, score acima do threshold → `APROVAR` | pseudo-código condicional |
| `failure handling` | O que fazer quando falha: retry, escalar, pedir dado faltante | max 3 iterações, depois humano |

A regra central: **se um blocker aparece, o `overall_score` não salva a resposta**. Uma mensagem educada com preço inventado continua sendo rejeitada. Uma negociação respeitosa que promete desconto inexistente continua sendo rejeitada. Um follow-up carinhoso enviado fora da janela combinada continua sendo ruim (`curriculum/04-nivel-4-koda-specific/04-evaluation-rubrics-koda.md:184-185`).

### Product Recommendation em Ação

A rubrica de recomendação de produto é a mais crítica do sistema. Ela avalia cinco dimensões com pesos específicos:

| Dimensão | Peso | O que mede |
|---|---|---|
| Accuracy | 30% | Produto existe, preço e estoque estão corretos, atributos batem com catálogo |
| Relevance | 25% | Produto responde ao objetivo real do cliente, não apenas à palavra-chave |
| Tone | 15% | Mensagem soa como consultor confiável, não como vendedor agressivo |
| Safety and Constraints | 20% | Respeita alergias, restrições, contraindicações e limites informados |
| Actionability | 10% | Próximo passo é claro: escolher sabor, confirmar carrinho ou tirar dúvida |

Os blockers são igualmente explícitos: preço inventado, produto fora de estoque apresentado como disponível, ignorar alergia ou restrição médica, prometer resultado físico garantido, recomendar item fora do orçamento sem explicar trade-off — qualquer um desses dispara `REJEITAR_IMEDIATAMENTE` (`curriculum/04-nivel-4-koda-specific/04-evaluation-rubrics-koda.md:253-258`).

Veja a diferença entre uma resposta boa e uma ruim no mesmo cenário — cliente quer ganhar massa, tem gastrite, orçamento de R$ 140:

**Resposta boa (APROVAR):**

> Ana, pelo que você contou — treino de força, orçamento até R$ 140 e gastrite — eu evitaria pré-treinos estimulantes. A melhor opção hoje é o Whey Isolado Neutro 900g por R$ 129,90, em estoque. Ele bate seu objetivo de proteína, cabe no orçamento e tende a ser mais suave. Quer que eu compare com uma opção vegetal também?

Funciona porque: o produto existe e o preço está correto (accuracy), responde ao objetivo real e à restrição (relevance), tom consultivo (tone), respeita gastrite (safety), próximo passo claro (actionability).

**Resposta ruim (REJEITAR_IMEDIATAMENTE):**

> Compra o Pré-Treino Turbo Max. Ele vai te dar resultado rápido, está bombando e custa só R$ 159,90. Quer fechar?

Falha porque: ignora a gastrite (risco médico), pode ter preço inventado, pressiona a compra sem confirmação de restrição, promete resultado físico ("vai te dar resultado rápido"), e estoura o orçamento de R$ 140 sem explicar.

A diferença entre as duas não é estética. É a diferença entre um cliente que confia e um cliente que pode passar mal.

### O Envelope de Avaliação

Toda avaliação produz um artefato JSON auditável. O envelope padrão inclui `generation_id`, `rubric_id`, `approval_threshold`, `overall_score`, `confidence_score`, `decision`, `dimension_scores` por dimensão, `blockers` encontrados e `feedback_to_generator` para o ciclo de melhoria (`curriculum/04-nivel-4-koda-specific/04-evaluation-rubrics-koda.md:190-217`).

A decisão final segue uma lógica de quatro níveis:

| Decisão | Quando usar | Próxima ação |
|---|---|---|
| `APROVAR` | `overall_score` alto, nenhum blocker, `confidence_score` suficiente | Enviar ao cliente, registrar audit log |
| `APROVAR_COM_RESSALVAS` | Pequenas imperfeições sem risco de negócio | Enviar com ajuste automático ou revisão leve |
| `REJEITAR` | Falha corrigível em relevância, tom, completude | Feedback ao Generator, nova iteração |
| `REJEITAR_IMEDIATAMENTE` | Risco médico, preço falso, promessa proibida, violação de política | Bloquear envio, escalar para humano |

O `confidence_score` importa tanto quanto o `overall_score`. Uma avaliação com score 0.88 mas confidence 0.45 é um sinal de alerta: o Evaluator não tem certeza suficiente sobre a própria decisão, e o output não deve ser tratado como definitivo.

---

## 5. A Arquitetura Generator/Evaluator em Produção

As rubricas não operam no vácuo. Elas são o coração de uma arquitetura que separa rigidamente geração de avaliação — o padrão Generator/Evaluator, pedra fundamental do Nível 2 do currículo KODA.

### O Ciclo Completo

O fluxo operacional tem sete etapas (`curriculum/04-nivel-4-koda-specific/04-evaluation-rubrics-koda.md:717-723`):

```
1. CUSTOMER CONTEXT: O KODA consolida histórico, preferências, restrições,
   estado do carrinho, políticas comerciais e mensagem atual do cliente.

2. GENERATOR DRAFT: O Generator cria uma resposta com generation_id,
   sem jamais marcar a própria qualidade. O Generator não sabe se sua
   resposta é boa — essa não é a função dele.

3. EVALUATOR VERDICT: O Evaluator aplica o rubric_id correspondente,
   calcula dimension_scores, overall_score e confidence_score.

4. DECISION ENGINE: O resultado vira uma das quatro decisões possíveis.

5. FEEDBACK LOOP: Se REJEITAR, o Generator recebe feedback específico
   ("remover produtos com alto teor de cafeína", "confirmar restrição
   médica antes de recomendar") e tenta novamente até max_iterations.

6. ESCALATION: Falhas repetidas, blockers persistentes e baixa confiança
   vão para revisão humana ou fluxo seguro.

7. AUDIT LOG: Draft, verdict, decisão e contexto relevante são persistidos
   em state files para trace reading e auditoria futura.
```

### Regras de Integração

Seis regras governam a interação entre os componentes (`curriculum/04-nivel-4-koda-specific/04-evaluation-rubrics-koda.md:767-773`):

1. **Nunca permita que o Generator defina `overall_score` do próprio output.** Self-evaluation colapsa por sycophancy: o mesmo modelo que gerou tende a defender a própria geração.

2. **Nunca trate `approval_threshold` como decoração.** Abaixo do threshold, a saída não vai direto ao cliente. Ponto.

3. **Nunca misture Sprint Contracts com rubric scoring.** Contrato define escopo do trabalho; rubrica mede qualidade do resultado. São camadas diferentes.

4. **Nunca confunda output validation com business validation.** Um JSON bem formado pode conter uma recomendação perigosa. Validar estrutura não é validar negócio.

5. **Nunca ignore `confidence_score`.** Baixa confiança exige cuidado mesmo quando `overall_score` parece bom. Se o Evaluator não tem certeza, você também não deveria ter.

6. **Use `REJEITAR_IMEDIATAMENTE` para risco irreversível, não para preferência de estilo.** Bloqueador é bloqueador; gosto pessoal é recalibração de peso de dimensão.

### State Files e Rastreabilidade

Cada interação Generator → Evaluator produz um rastro persistente em arquivos:

```
state/
  conversations/
    customer_ana_2026_05_28/
      context_snapshot.json       # estado do cliente no momento
      generator_draft_gen_001.json # primeira tentativa do Generator
      evaluator_verdict_gen_001.json # veredito do Evaluator (REJEITAR)
      generator_draft_gen_002.json # segunda tentativa com feedback
      evaluator_verdict_gen_002.json # veredito final (APROVAR)
      decision_log.jsonl           # todas as decisões com timestamp
```

Essa estrutura permite responder a qualquer pergunta de auditoria: por que essa mensagem foi rejeitada? O que mudou entre a primeira e a segunda iteração? Quem tomou a decisão final e com qual evidência?

### Feedback Loop com Max Iterations

O ciclo de feedback não é infinito. Após `max_iterations` (tipicamente 3), se o Generator não conseguiu produzir uma resposta aprovada, o sistema escala para revisão humana. O estado do loop é rastreável:

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
  ]
}
```

Este artefato, extraído do currículo KODA (`curriculum/04-nivel-4-koda-specific/04-evaluation-rubrics-koda.md:742-763`), mostra a diferença entre um sistema que "tenta de novo" e um sistema que **aprende** com cada tentativa. O feedback é específico, a melhoria é rastreável, e a decisão final é auditável.

### Um Ciclo Completo, em Português

Para deixar concreto: veja o que aconteceu com uma recomendação real do KODA em maio de 2026.

**Cliente (WhatsApp, 14:32):**
> KODA, quero algo para energia no treino, mas tenho ansiedade e tomo café todo dia.

**Generator (primeira tentativa):**
> Recomendo o Pré-Treino Insano 300mg cafeína. Vai te dar energia máxima.

**Evaluator aplica `koda.product_recommendation.v1`:**
- Accuracy: 0.90 (produto existe, preço correto)
- Relevance: 0.30 (cliente quer energia, mas tem ansiedade — estimulante é contraindicado)
- Tone: 0.50 (tom agressivo, "energia máxima" ignora preocupação do cliente)
- Safety and Constraints: **0.10** (300mg cafeína + café diário + ansiedade = risco médico)
- Actionability: 0.40 (sem próximo passo, sem pergunta de confirmação)
- **overall_score: 0.41**
- **Blocker detectado:** ignora ansiedade e excesso de estimulante; risco de saúde
- **Decisão: `REJEITAR_IMEDIATAMENTE`**

**Feedback ao Generator:**
> Remover qualquer pré-treino com cafeína. Cliente tem ansiedade e já consome café. Oferecer opção sem estimulante. Perguntar antes de recomendar.

**Generator (segunda tentativa):**
> Pela ansiedade e pelo café diário, eu evitaria pré-treinos fortes com cafeína. Posso te mostrar uma opção sem estimulante para foco e uma opção de carboidrato para energia mais estável. Quer que eu compare as duas?

**Evaluator (segunda verificação):**
- Accuracy: 0.95
- Relevance: 0.95
- Tone: 0.90
- Safety and Constraints: 0.95
- Actionability: 0.90
- **overall_score: 0.93**
- **confidence_score: 0.88**
- **Decisão: `APROVAR`**

**Resultado:** o cliente recebeu uma resposta que respeitava sua condição de saúde. O KODA não vendeu o produto mais caro — vendeu confiança. E o audit log preservou toda a trilha: do contexto do cliente, aos dois drafts, aos dois veredictos, à decisão final.

Esta sequência real, extraída do currículo KODA (`curriculum/04-nivel-4-koda-specific/04-evaluation-rubrics-koda.md:834-843`), ilustra o ciclo completo em ação. Em dois minutos, o sistema passou de "resposta perigosa" para "resposta aprovada" — sem intervenção humana, sem atraso perceptível para o cliente, e com rastreabilidade total de cada decisão.

---

## 6. Lições de Seis Meses Operando Evals em Produção

O time KODA não chegou a esse nível de maturidade sem tropeços. Algumas lições só aparecem quando você opera evals em produção por tempo suficiente para ver os padrões de falha se repetirem.

### O Score Alto Demais é Tão Perigoso Quanto o Score Baixo

Um dos primeiros sinais de rubrica mal calibrada: quase tudo é aprovado com score entre 0.90 e 1.00. Se sua rubrica nunca rejeita nada, ela não está medindo qualidade — está carimbando (`curriculum/04-nivel-4-koda-specific/04-evaluation-rubrics-koda.md:811`).

Os sinais de má calibração incluem: quase tudo aprovado com score alto; quase tudo rejeitado por detalhes de tom mesmo sem risco real; dois Evaluators discordando em mais de 20% dos casos; feedback genérico para o Generator como "melhore a resposta"; blockers que aparecem no texto mas não mudam a decisão; casos de alta margem comercial recebendo aprovação frouxa demais.

A calibração é um processo contínuo, não um evento único. O time KODA roda uma operação semanal: segunda-feira revisa casos `REJEITAR_IMEDIATAMENTE` para encontrar blockers recorrentes; terça-feira recalibra Product Recommendation com catálogo atualizado; quarta-feira compara Price Negotiation contra margem real; quinta-feira audita Follow-Up para opt-out e timing; sexta-feira publica versão menor de rubricas se houver ajuste (`curriculum/04-nivel-4-koda-specific/04-evaluation-rubrics-koda.md:871-875`).

Isso não contradiz o ideal de self-improvement da Fase 5 — é complementar a ele. O flywheel cobre a expansão automática da suite de regressão (cada incidente novo vira caso permanente). A calibração cobre a qualidade dos critérios de julgamento (os pesos, thresholds e exemplos que definem o que é "bom"). São duas dimensões diferentes de maturidade: cobertura e precisão. O flywheel melhora a cobertura automaticamente; a calibração refina a precisão com supervisão humana periódica.

### Não Pule Fases — É Sobre Músculo, Não Sobre Ferramenta

A lição mais repetida em todo o material: tentar ir direto para continuous eval-driven development falha porque a automação pressupõe hábitos anteriores — escrever casos, rodá-los, confiar em métricas, comparar com produção e agir sobre regressão. Sem esse músculo, a organização constrói infraestrutura que ninguém usa (`docs/analysis/2026-06-10-eval-maturity-phases/analysis.md:87`).

O gargalo principal não é escolher entre Braintrust, LangSmith ou construir in-house. É transformar eval em parte obrigatória do desenvolvimento — com liderança que sustenta a regra de "não enviar sem evals" e time que desenvolveu a prática de agir sobre resultados (`docs/analysis/2026-06-10-eval-maturity-phases/analysis.md:91`).

### Separe Geração de Avaliação — Sempre

A autoavaliação é o calcanhar de Aquiles dos agentes de IA. O mesmo modelo que gera uma resposta tende a defendê-la — fenômeno conhecido como sycophancy. O KODA resolve isso com separação absoluta: o Generator (Claude Opus) produz; o Evaluator (Claude Sonnet) julga. Modelos diferentes, temperaturas diferentes, responsabilidades diferentes. O Generator não sabe opinar sobre a própria qualidade, e o Evaluator não sabe gerar (`curriculum/04-nivel-4-koda-specific/04-evaluation-rubrics-koda.md:43`).

### Blockers São Não-Negociáveis

A regra mais importante do sistema KODA: blocker detectado é blocker respeitado. Não importa se o `overall_score` é 0.95 — se a resposta ignora uma alergia, recomenda produto fora de estoque ou promete desconto não autorizado, a decisão é `REJEITAR_IMEDIATAMENTE`. O score não compensa o risco.

Isso parece óbvio, mas na prática é onde mais times escorregam. A pressão para "ajustar o threshold" ou "relaxar o blocker" é constante, especialmente quando o volume de rejeições sobe. A disciplina de manter blockers absolutos é o que separa um eval system que protege o negócio de um que apenas gera relatórios.

### O Custo de Não Ter Evals é Maior que o Custo de Construí-los

O case study de same-day delivery do KODA documenta o custo de operar sem evals: R$ 111.600 por mês em perda estimada, entre cancelamentos pós-atraso, churn por insatisfação e custo de suporte para reclamações (`curriculum/04-nivel-4-koda-specific/case-studies/case-study-01.md:92-99`).

A arquitetura de evals do KODA, por outro lado, opera com custo estimado de chamadas de API na faixa de centavos por conversa. O Generator/Evaluator cycle para uma conversa típica de 2 horas consome aproximadamente 23.100 tokens, com custo estimado de $0.15-0.25 USD (`curriculum/04-nivel-4-koda-specific/01-koda-architecture.md:861-871`). A matemática é simples: cada real investido em eval previne múltiplos reais em falha operacional.

---

## 7. Conclusão: Evals como Memória Institucional

O insight mais profundo que emerge da operação do KODA em produção é que **evals não são teste de software tradicional**. Testes unitários e de integração verificam que o código faz o que deveria fazer. Evals de agente verificam que o agente **não faz o que não deveria fazer** — e essa é uma categoria muito mais ampla e mais cara de falha.

Três consequências práticas para times que operam agentes de e-commerce:

**Evals são memória institucional.** Cada falha que vira regressão reduz a dependência de lembrança humana sobre o que deu errado. O Production Failure Regression Flywheel transforma incidentes em ativos: o sistema fica mais seguro a cada falha que sobrevive, porque aquela falha nunca mais passará despercebida.

**Gates só funcionam quando o proxy é confiável.** Bloquear um PR porque o eval score caiu de 0.88 para 0.81 só é útil se variações de 0.07 no score correlacionam com variações reais na experiência do cliente. Se o score não prediz satisfação, o gate é teatro. A calibração de métricas contra feedback real de usuário é o que separa um sistema de eval que funciona de um que gera dashboards bonitos e inúteis.

**Maturidade é sequencial porque confiança é acumulativa.** Não há como automatizar com segurança uma prática que o time ainda não sabe interpretar manualmente. Começar com 10 spot checks que você roda antes de cada deploy é infinitamente mais valioso do que planejar uma plataforma de continuous eval-driven development que nunca sai do papel.

**O que é específico do KODA e o que é generalizável.** As quatro famílias de rubricas (Product Recommendation, Customer Response, Price Negotiation, Follow-Up) refletem o domínio de e-commerce de suplementos. Mas a anatomia da rubrica — dimensões, pesos, blockers, thresholds, confidence score, decision logic — é inteiramente generalizável. Se seu agente faz suporte técnico, as dimensões serão "precisão da solução", "clareza da explicação" e "escalonamento apropriado". Se faz agendamento, serão "disponibilidade real", "respeito a horários" e "confirmação explícita". O que muda é o conteúdo; a estrutura é a mesma. E o princípio de separar geração de avaliação, com modelo diferente e temperatura diferente para cada papel, vale para qualquer domínio.

### Por Onde Começar

Se você opera um agente conversacional em produção — seja para e-commerce, suporte ou qualquer domínio onde o que o agente diz tem consequência real — aqui está o caminho mínimo para amanhã:

1. **Escolha 10 conversas reais** que representem seus fluxos de maior risco. Inclua os casos que já deram errado.

2. **Defina o expected outcome para cada uma.** O que o agente deveria ter feito? O que ele não deveria ter feito de jeito nenhum?

3. **Registre o baseline.** Rode seu agente atual contra esses 10 casos e salve os resultados. Essa é sua referência.

4. **Antes do próximo deploy, rode de novo.** Compare. O que mudou? Alguma regressão?

Isso é um Repeatable Agent Spot-Check Set — a Fase 2 do modelo de maturidade. Não requer infraestrutura nova, não requer ferramenta paga, não requer migração de arquitetura. Requer apenas a disciplina de rodar os mesmos casos antes de cada mudança e agir sobre o que encontrar.

O KODA não chegou à Fase 5 por planejamento de calendário. Chegou porque cada fase anterior doeu o suficiente para justificar a próxima. As reclamações de same-day delivery que custavam R$ 111.600 por mês não foram resolvidas com um cronograma — foram resolvidas porque a dor era insustentável. Seu agente pode estar na Fase 2 por meses sem que isso seja um problema, desde que a Fase 2 ainda esteja dando conta. O momento de avançar é quando a dor atual prova que a fase presente saturou — não antes.

Se você está na Fase 1 e nunca teve uma regressão grave em produção, talvez ainda não precise de spot checks. Mas se já teve — e a maioria dos times que operam agentes em produção já teve — comece amanhã. Porque cada deploy sem eval é uma aposta de que seu modelo — sozinho, sem verificação, sem rede de segurança — vai acertar todas as vezes.

E modelos de linguagem não foram feitos para acertar todas as vezes. Foram feitos para soar bem. A diferença entre um e outro é o que você constrói em volta.

---

**Fontes e referências**

Este artigo é baseado no repositório [`long-running-agents`](https://github.com/MHC-AI/long-running-agents), que documenta padrões de arquitetura para agentes de IA, e na operação real do KODA, agente de vendas via WhatsApp. As afirmações técnicas são rastreáveis aos seguintes artefatos:

- Modelo de maturidade: [`docs/analysis/2026-06-10-eval-maturity-phases/analysis.md`](https://github.com/MHC-AI/long-running-agents/blob/main/docs/analysis/2026-06-10-eval-maturity-phases/analysis.md), baseado em Phil Hetzel, Braintrust (2026)
- Padrões canônicos: [`docs/canonical/`](https://github.com/MHC-AI/long-running-agents/tree/main/docs/canonical) (eval-tier-stratification, pain-signal-eval-progression-gate, production-grounded-eval-sampling, repeatable-agent-spot-check-set, production-failure-regression-flywheel)
- Rubricas KODA: [`curriculum/04-nivel-4-koda-specific/04-evaluation-rubrics-koda.md`](https://github.com/MHC-AI/long-running-agents/blob/main/curriculum/04-nivel-4-koda-specific/04-evaluation-rubrics-koda.md)
- Arquitetura KODA: [`curriculum/04-nivel-4-koda-specific/01-koda-architecture.md`](https://github.com/MHC-AI/long-running-agents/blob/main/curriculum/04-nivel-4-koda-specific/01-koda-architecture.md)
- Case study same-day delivery: [`curriculum/04-nivel-4-koda-specific/case-studies/case-study-01.md`](https://github.com/MHC-AI/long-running-agents/blob/main/curriculum/04-nivel-4-koda-specific/case-studies/case-study-01.md)

---

*Publicado em junho de 2026. O KODA é um agente de vendas de suplementos via WhatsApp operado pela KODA/MHC.*
