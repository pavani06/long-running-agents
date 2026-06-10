---
aliases: ["métodos construção", "harness métodos", "construção harness"]
---

# A Arquitetura Invisível: Como Harnesses Evoluem e o Que Torna um Bom Harness de Agentes

**Por que a diferença entre um agente que funciona em demo e um que funciona em produção não está no modelo — está na estrutura que o sustenta.**

---

Em maio de 2026, Fernando Machado entrou na sala de arquitetura do time KODA com um café na mão e uma expressão que misturava ansiedade com excitação. Na mesa, um print do changelog do novo modelo Claude. O time mantinha um harness de 11 componentes que funcionava. Mas Fernando não estava ali para celebrar.

"Vocês leram o changelog de sexta-feira?", perguntou. "Isso muda nossa arquitetura."

O time tinha construído um Context Loader porque o modelo antigo esquecia informações depois de 40 minutos de conversa. O novo modelo mantinha 98% de acurácia em 100K tokens. O Context Loader custava 450ms de latência por turno, 1200 tokens, e 3 horas de manutenção por mês. E prevenia 0.008% dos erros — 12 casos reais em 145 mil turnos.

"O harness certo para o modelo de 6 meses atrás pode ser o harness errado para o modelo de hoje", disse Fernando.

Essa é a história que define a maturidade de um time de agentes: não é sobre construir mais, é sobre saber o que remover.

---

## O Que é um Harness — e Por Que Você Precisa de Um

Um harness é o conjunto de padrões, estruturas e validações que cercam o núcleo do agente — o LLM — para transformar um modelo criativo e não-determinístico em um produto confiável, rastreável e auditável. É a diferença entre ter um bom piloto e ter uma aeronave segura.

Agentes de IA falham em execuções longas por três razões estruturais:

1. **Perda de contexto** — a janela de tokens enche, e o agente "esquece" o que estava fazendo.
2. **Planejamento frágil** — sem decomposição, o agente tenta resolver tudo de uma vez e se perde.
3. **Autoavaliação cega** — o mesmo modelo que gera também avalia, aprovando qualidade ruim como boa.

A solução está nos harnesses: estruturas que gerenciam contexto, decompõem trabalho em etapas menores e separam geração de avaliação.

Muitas pessoas acreditam que a diferença entre um protótipo de agente e um agente em produção é a qualidade do modelo. É o contrário. Empresas que escalaram agentes em produção construíram harnesses sofisticados. Empresas que falharam confiaram que o modelo "faria a coisa certa". A diferença é arquitetura.

---

## Os 5 Padrões Fundamentais de um Bom Harness

### 1. History Windowing — O Contexto Que Importa

Seu agente não precisa carregar 4 horas de conversa inteira no prompt. Em vez de manter toda a conversa, mantenha: as últimas 15-20 mensagens, um resumo comprimido do histórico antigo e metadados críticos que nunca expiram — decisões tomadas, preferências confirmadas, compromissos assumidos.

No KODA, implementar History Windowing reduziu o tempo de resposta em 57% (de 4.2s para 1.8s) e aumentou a satisfação do cliente em conversas longas de 72% para 94%.

**O erro clássico:** descartar o histórico completamente. A solução é extrair decisões e compromissos explicitamente antes de comprimir.

### 2. Structured Generation — Force o Modelo a Ser Previsível

Em vez de deixar o modelo gerar texto livre, force-o a responder em formato estruturado: JSON com campos como `recommendation`, `reasoning`, `confidence` e `risk_flags`. Isso permite validação automática de cada campo antes de chegar ao cliente.

No KODA, a adoção de Structured Generation reduziu a taxa de erro em recomendações de 8.2% para 0.3% e eliminou completamente o retrabalho por respostas ambíguas.

**O erro clássico:** validar só o formato JSON, não as regras de negócio. JSON pode ser válido e ainda recomendar um produto com ingrediente ao qual o cliente é alérgico.

### 3. State Persistence — Memória Que Sobrevive a Falhas

Pedro passou 47 minutos conversando com o KODA, definindo restrições, preferências e um carrinho de R$ 379,60. O servidor reiniciou. Quando Pedro voltou com "deu erro no pagamento, tenta de novo?", o KODA respondeu: "oi, como posso te ajudar?"

Sem state persistence, cada falha vira amnésia. Com state persistence, cada falha vira pausa.

Estado deve ser estruturado em campos bem-definidos (preferências, decisões, compromissos), persistido em arquivo ou banco com versionamento, e carregado no início de cada conversa. O cliente não deveria precisar repetir que é alérgico a glúten.

### 4. Fallback & Retry — O Agente Não Pode Simplesmente Morrer

Defina escaladas inteligentes: retry com novo prompt, fallback para recomendação segura, escalada para humano. Sem estratégia de fallback, cada erro vira um ticket manual.

**O erro clássico:** nunca testar o fallback em produção. Fallback não testado é fallback quebrado.

### 5. Guardrails & Constraints — O Que o Modelo Não Pode Fazer

Antes que o modelo gere qualquer resposta, defina constraints claros: budget máximo, produtos disponíveis, prazos realistas. E valide essas constraints em código após a geração — nunca confie apenas no prompt.

---

## Generator/Evaluator: O Padrão Que Muda Tudo

Existe um padrão que merece destaque: separar geração de avaliação. Em vez de um único modelo fazer tudo, divida em dois papéis.

O **Generator** gera múltiplas opções de forma criativa. O **Evaluator** avalia cada opção de forma crítica. O modelo é excelente em gerar ideias, mas não é confiável em avaliar as próprias ideias — é o equivalente a pedir ao mesmo pintor para pintar um quadro e avaliar se ficou bom.

No KODA, o Generator produz 3 recomendações diferentes. O Evaluator pontua cada uma contra uma rubrica (relevância, preço, clareza) e aprova ou rejeita. O resultado: precisão de recomendações subiu de 75% para 98%, e a satisfação do cliente foi de 70% para 88%. O custo adicional foi de apenas 15% em chamadas de API, mas gerou 30% mais receita.

---

## O Ciclo de Vida do Harness: BUILD → STABILIZE → SIMPLIFY → REMOVE

Aqui está a contribuição mais profunda do repositório long-running-agents: harness não é algo que você constrói uma vez. É algo que você gerencia em ciclos.

### Fase 1: BUILD — "Preciso proteger o modelo das próprias fraquezas"

Um novo modelo é integrado. Você ainda não conhece suas limitações em produção real. O mindset é defensivo: crie componentes de validação explícitos, imponha limites rígidos, implemente fallbacks generosos, escreva system prompts longos e detalhados.

O Context Loader original do KODA foi criado nessa fase: 1200 tokens por turno, 450ms de latência, carregando perfil do cliente a cada mensagem, comprimindo histórico, injetando redundância. Na época, com um modelo de 32K tokens que perdia atenção após 40 minutos, cada uma dessas proteções se justificava.

### Fase 2: STABILIZE — "O harness está confiável. Agora posso medir."

Após 60+ dias em produção, você tem dados para avaliar o valor real do componente — não o valor que imaginava quando o criou. Monte um dashboard de efetividade real: quantas falhas o componente realmente preveniu? Quantos falsos positivos gerou? Qual o custo completo?

O Context Loader, após 90 dias, revelou números surpreendentes: 59 prevenções reais em 145 mil turnos (0.04% de efetividade), mas 340 falsos positivos — 28 vezes mais bloqueios incorretos que corretos. O shadow test (50% do tráfego com e sem o componente) mostrou que a diferença de acurácia era de apenas 0.4% — estatisticamente insignificante.

### Fase 3: SIMPLIFY — "O modelo agora consegue lidar com isso"

Um novo modelo cobre a fraqueza que o componente protegia. Ou as métricas mostram ROI negativo. Você não arranca o componente de uma vez. Reduz camada por camada: primeiro remova redundância, depois relaxe constraints, depois consolide funções, e só então remova.

A simplificação do Context Loader foi executada em 3 ondas, cada uma com shadow test de 7-14 dias. Resultado final: 1200 tokens/turno foram para zero (a função essencial foi absorvida pelo History Compactor), 450ms de latência eliminados, e a acurácia caiu apenas 0.2% — dentro da margem de erro.

### Fase 4: REMOVE — "Este componente cumpriu seu propósito"

O Budget Guard, primeiro componente removido do KODA, monitorava o consumo de tokens e truncava conversas ao atingir 80% da janela de 32K. Com a migração para um modelo de 200K tokens, o limite nunca era atingido. Zero disparos em 180 dias. Zero regressões após remoção.

O código não foi deletado — foi arquivado em `archive/components/budget-guard-v1/` com README documentando por que existiu, por que foi removido e que modelo justificou a remoção. Feature flag permite reativação em minutos se necessário.

---

## O Paradoxo do Harness

O harness existe para dar confiança. Mas se você nunca o revisa, ele se torna a própria fonte de fragilidade que deveria prevenir.

Cada componente desnecessário significa mais superfície para bugs, mais latência entre o cliente perguntar e o sistema responder, mais tokens gastos, mais complexidade para novos desenvolvedores entenderem, mais arquivos de estado para manter.

A pergunta não é "funciona?". A pergunta é **"ainda é necessário?"**

Em sistemas tradicionais (APIs REST, bancos de dados), a peça central evolui lentamente. Em sistemas de agentes de IA, a peça central evolui a cada 3-6 meses. Um harness desenhado para o modelo de 6 meses atrás não é proteção — é peso morto.

---

## Os 4 Componentes do Loop de Controle

Extraído da talk "12-Factor Agents" (Dex Horthy, AI Engineer 2025) e adaptado no repositório: o agente deve ser decomposto em exatamente quatro partes que você possui diretamente, sem delegar a um framework.

**1. Prompt.** As instruções que o modelo recebe a cada turno. Você possui o texto e o versiona como código. Ponto de intervenção: avaliar variantes de prompt contra evals, fazer A/B testing.

**2. Context Builder.** O que o modelo vê além do prompt: histórico, memória, resultados de ferramentas, estado de negócio. Você constrói cada token deliberadamente. Ponto de intervenção: sumarizar histórico antigo, injetar contexto fresco, comprimir resultados verbosos.

**3. Switch Statement (Dispatch).** O roteador determinístico que mapeia JSON de saída do modelo para código de handler. Você possui o mapeamento. Ponto de intervenção: circuit-break de chamadas caras, audit-log de cada dispatch.

**4. Loop.** O while/for que executa os turnos do agente. Você controla contagem de iterações, condições de saída e o que acontece entre iterações. Pontos de intervenção: break, summarize mid-loop, LM-as-judge, human approval gate, force terminate.

Se você possui o loop, você pode injetar operações arbitrárias nele sem que o framework saiba ou precise saber. O loop deixa de ser uma caixa-preta do runtime para ser código de aplicação comum.

---

## Context Engineering: A Disciplina Unificadora

Se há um princípio unificador que atravessa todos os padrões do repositório, é este: **context engineering é a disciplina central**. Prompt, memória, RAG, histórico — tudo se resume a como colocar os tokens certos no modelo. O harness existe para servir o contexto, não o contrário.

Isso implica decisões concretas de arquitetura:

**Head-Tail Context Truncation.** Quando o contexto estoura, preserve a cabeça (objetivo original, system prompt) e a cauda (estado atual, último resultado). Mova o meio para memória externa com handles de recuperação: ID estável, localização na conversa, preview do conteúdo.

**Addressable Memory Catalog.** Memória externa sem catálogo é inútil. Cada item omitido precisa de `id`, `location`, `preview` e `fetch` para o agente decidir o que recuperar. O preview é uma segunda camada de contexto: pequeno demais e o agente não sabe o que buscar; grande demais e a memória externa volta a poluir a janela ativa.

**Stable Harness Prompt.** A redução de contexto deve remover payload, histórico antigo e tool calls longas — nunca as instruções do harness que definem papel, política, contratos de ferramenta, limites de segurança e formato de resposta. O harness prompt é um bloco de primeira classe com budget e versão próprios.

**Error Context Hygiene.** Erros acumulados no context window são uma das causas principais de "spiral out" — o agente começa a alucinar sobre erros passados, tenta corrigir problemas já resolvidos, ou entra em loop de retry porque o contexto está poluído com informação de falha. A regra: quando um tool call falha e um subsequente é bem-sucedido, limpe todos os erros pendentes e resuma em uma linha.

---

## O Que Nunca Remover: Invariantes Arquiteturais

Algumas proteções são permanentes — sua presença não depende da qualidade do modelo, mas da natureza do domínio:

- **Segurança do cliente.** Alergias, contraindicações, dados sensíveis exigem validação independente do modelo.
- **Decisões irreversíveis.** Cobrança, envio de pedido, alteração de dados precisam de checkpoint humano ou de sistema.
- **Fallback de disponibilidade.** O modelo pode ficar offline. Retry e fila de mensagens protegem contra falha do serviço, não do modelo.
- **Evaluator como gatekeeper.** Sycophancy é um problema estrutural de LLMs, não de qualidade de modelo. Mesmo modelos excelentes podem ser sycophantic.
- **State Persistence.** Sem estado persistente, não há auditabilidade, debugging ou recuperação de falhas.

Todo o resto é candidato a revisão trimestral.

---

## Métodos de Construção: O Que Fazer na Prática

O repositório fornece um playbook completo para implementar esses conceitos:

### O Ritmo Trimestral

A evolução do harness não é um projeto com começo, meio e fim. É um processo contínuo integrado ao ritmo do time: review & plan na semana 1 (analisar changelog do modelo, revisar métricas, classificar cada componente), implement nas semanas 2-3 (feature flags, shadow tests, remoções documentadas), observe nas semanas 4-12 (monitorar, coletar dados, não fazer novas mudanças).

### One In, One Out

Sempre que um componente novo é adicionado ao harness, um existente deve ser marcado para investigação de remoção no próximo ciclo. Isso evita que o harness cresça indefinidamente.

### Decida com ROI, Não com Intuição

```
ROI = (Erros Prevenidos × Custo Médio do Erro) / (Custo Operacional do Componente)
```

Se o ROI for menor que 1x por dois trimestres consecutivos, o componente é candidato a remoção.

### Feature Flags, Shadow Tests, Canary Deploy

Nunca remova em big bang. Uma remoção por vez. Feature flag independente para cada componente. Shadow test de 14+ dias. Canary em 5% → 25% → 100%. Período de observação de 14 dias entre remoções.

### Documente Tudo

Para cada componente removido, escreva um ADR com: data da decisão, métricas que justificaram, processo de validação, resultado pós-remoção. Código vai para `archive/components/<nome>/` com README. Seis meses depois, quando alguém perguntar "por que não temos Budget Guard?", o ADR responde.

---

## Do Pesado ao Essencial: O KODA em Três Momentos

A mesma jornada de cliente — "Quero um whey protein vegano, sem glúten, até R$ 150" — processada em três momentos diferentes da evolução:

**Dezembro 2025 (Harness Pesado — 11 componentes):** 4000ms de latência, 3200 tokens, 9 componentes acionados, R$ 0,048 por turno.

**Junho 2026 (Harness em Simplificação — 8 componentes):** 1500ms (-62%), 1500 tokens (-53%), 4 componentes acionados, R$ 0,022 (-54%). Mesma acurácia.

**Setembro 2026 (Harness Essencial — 6 componentes):** 1300ms (-67%), 1200 tokens (-62%), 3-4 componentes acionados, R$ 0,018 (-62%). Mesma acurácia.

A qualidade da recomendação não mudou. Mas o sistema ficou 3x mais rápido, 2.6x mais barato e com metade dos componentes para manter.

---

## A Lição Final

Construir um harness é um ato de humildade — você reconhece que o modelo tem fraquezas e cria proteções. Evoluir um harness é um ato de confiança — você reconhece que o modelo melhorou e que é hora de seguir em frente com uma arquitetura mais leve.

O destino de toda boa arquitetura de agentes não é crescer para sempre. É **evoluir para o essencial**.

Bons arquitetos constroem sistemas que funcionam. Grandes arquitetos constroem sistemas que **continuam simples** conforme evoluem.

---

*Este artigo é uma síntese do repositório [long-running-agents](https://github.com/futanbear/long-running-agents), um programa curricular de 12 semanas sobre construção de sistemas de IA que operam de forma confiável por horas, dias ou pelo tempo que a tarefa exigir. O conteúdo é baseado em 16 padrões canônicos ativos de arquitetura, diagnósticos de produção do sistema KODA, análises derivadas das talks "12-Factor Agents" (Dex Horthy) e "How We Solved Context Management in Agents" (Arize), e 5 estudos de caso reais.*
