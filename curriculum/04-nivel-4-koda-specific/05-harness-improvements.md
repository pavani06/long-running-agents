# 🛠️ Melhorias de Harness para KODA
## Como transformar diagnóstico em propostas priorizadas, métricas e roadmap de evolução

**Tempo Estimado:** 180 a 240 minutos  
**Nível:** 4 - KODA Específico  
**Pré-requisitos:** Nível 1 completo, Nível 2 completo, Nível 3 completo, leitura dos diagnósticos do mhc-backend  
**Status:** 🟢 CRÍTICO - Módulo de transição entre diagnóstico e plano de melhoria  
**Data de Criação:** Maio 2026  
**Contexto:** Issue #17 - Melhorias de Harness KODA  
**Foco:** propostas de melhoria, não descrição de arquitetura futura como fato atual  

---

## 📌 Como Ler Este Módulo

Este módulo parte de uma realidade específica: o KODA já tem uma base técnica relevante, mas ainda carrega lacunas de harness que afetam coordenação, rastreabilidade, memória longa e evolução arquitetural.

A leitura deve ser prática. Você vai sair com um diagnóstico acionável, uma lista priorizada de propostas, métricas de sucesso, roadmap de implementação e checklists para acompanhar a evolução em fases.

Todas as recomendações aparecem como **propostas de melhoria**. Quando este módulo fala de Planner, Evaluator dedicado, manifest de auditoria ou checkpoint explícito, ele está descrevendo um caminho recomendado, não afirmando que isso já está em produção.

### Fontes Usadas

* `docs/nivel-3-comparacao-mhc-backend.md`
* `docs/analysis/mhc-backend-koda-harness-diagnostic.md`
* `docs/analysis/mhc-backend-koda-nivel-2-diagnostic.md`
* `curriculum/03-nivel-3-advanced-architecture/05-harness-evolution.md`
* `curriculum/03-nivel-3-advanced-architecture/koda-applications/nivel-3-koda.md`
* `curriculum/01-nivel-1-fundamentals/01-why-agents-lose-plot.md`
* `curriculum/02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md`
* `curriculum/02-nivel-2-practical-patterns/koda-applications/nivel-2-koda.md`

### Promessa do Módulo

* Explicar o problema real do harness KODA sem exagerar o que já existe.
* Separar fatos observados de propostas de arquitetura.
* Traduzir gaps em melhorias priorizadas.
* Dar critérios de sucesso por melhoria.
* Criar um roadmap curto, médio e longo.
* Dar um checklist de implementação por fase.
* Manter Fernando e KODA como narrativa guia.

---

## 📖 Prólogo: A Manhã em que o Harness do KODA Parecia Bom, Mas Não Era Suficiente

Terça-feira, 08h07.

Fernando abriu o dashboard do KODA antes da daily.

Os números de superfície pareciam confortáveis.

A API estava respondendo.

O WhatsApp recebia mensagens.

Os logs tinham `orchestrator_turn_trace` com timings por etapa.

O `state_build_trace` mostrava contagens de histórico, carrinho, memórias e cache.

A base usava PostgreSQL, Redis, Prisma, LangGraph, LangChain e tools com schema.

KODA não era um brinquedo.

Mesmo assim, o canal de suporte já tinha três conversas marcadas como risco.

A primeira era de Pedro.

Pedro tinha montado um carrinho em 47 minutos. Escolheu creatina, whey isolado, multivitamínico e uma opção sem estimulantes para treino noturno.

No momento do pagamento, o processo reiniciou.

Quando Pedro voltou, o KODA não retomou com segurança o mesmo estado comercial.

A segunda conversa era de Marina.

Marina pediu a mesma compra em duas mensagens rápidas. O debounce ajudou parte do fluxo, mas a coordenação de pedido ainda dependia de áreas frágeis, incluindo lock em memória no carrinho e race condition documentada em fila de processamento.

O suporte queria saber se dois pedidos poderiam sair com SKUs diferentes.

A resposta honesta era desconfortável: em certas condições, sim, esse tipo de incidente é plausível.

A terceira conversa era de Rafael.

Rafael passou horas conversando sobre treino noturno. No início, disse que evitava cafeína. Depois de muitas mensagens, essa informação competia com ruído social, comparação de sabores, frete, orçamento e dúvidas de uso.

O diagnóstico de Nível 3 registra o risco com clareza: o histórico do WhatsApp é limitado a 60 mensagens e o da API a 20. Sem compactação server-side com criticidade, fatos antigos podem desaparecer ou depender de recall indireto.

Fernando respirou fundo.

O problema não era falta de engenharia.

O problema era que o harness tinha crescido por camadas, não por um plano evolutivo único.

Havia bons sinais: Zod nas tools, logs estruturados, memória semântica, cache Redis, detecção de contradições, idempotência em webhooks e anti-spam gate.

Mas havia gaps claros: KODA ecommerce em produção ainda se comportava como single agent com tools, sem Planner e Evaluator dedicados para decompor a jornada comercial.

Havia traces operacionais, mas não um manifest completo que mostrasse quais inputs, tools e decisões sustentaram cada resposta.

Havia estado persistido em várias tabelas, mas não checkpoints explícitos por etapa crítica de carrinho, pedido e pagamento.

Havia métricas de latência, mas não custo por chamada LLM, tokens por componente, ROI por proteção ou ciclo formal BUILD, STABILIZE, SIMPLIFY, REMOVE.

Na daily, Fernando escreveu no quadro:

```text
KODA tem harness.
KODA precisa de harness governado.
```

A diferença é grande.

Harness existe quando o sistema tem proteções.

Harness governado existe quando o time sabe por que cada proteção existe, quanto custa, qual falha previne, quando deve evoluir e quando pode ser removida.

Esse módulo começa nesse ponto.

Você não vai aprender a construir mais uma camada por reflexo.

Você vai aprender a propor melhorias com evidência.

Você vai diagnosticar onde o KODA está hoje.

Você vai separar gaps críticos de melhorias incrementais.

Você vai desenhar uma arquitetura proposta, deixando claro que é proposta.

Você vai montar roadmap, métricas, checklist e critérios de saída.

E, no fim, vai conseguir responder a pergunta que Fernando fez ao time:

```text
Qual melhoria de harness reduz mais risco real para KODA com o menor custo reversível?
```

---

## 🎯 Objetivos de Aprendizagem

1. Diagnosticar o harness atual do KODA a partir de dados e documentos de análise.
2. Reconhecer a diferença entre single agent com tools e decomposição real Planner, Generator e Evaluator.
3. Explicar por que histórico 60/20 sem compactação crítica cria risco em conversas longas.
4. Definir propostas de checkpoint, trace, manifest e coordination sem vender proposta como fato atual.
5. Priorizar melhorias usando impacto, risco, custo, reversibilidade e dependência.
6. Criar métricas de sucesso para cada melhoria, incluindo qualidade, custo, latência, auditabilidade e ROI.
7. Aplicar o ciclo BUILD, STABILIZE, SIMPLIFY, REMOVE em componentes de harness.
8. Criar um plano de implementação curto, médio e longo para KODA.
9. Usar checklists de fase para evitar implantação frágil.
10. Comunicar melhorias de harness para engenharia, produto, suporte e liderança.

---

## 🔍 Diagnóstico do Harness Atual do KODA


### Síntese Executiva

O diagnóstico consolidado aponta uma situação mista. O `mhc-backend` tem sinais maduros de produção, mas o KODA ecommerce ainda não alcança uma arquitetura de harness Nível 3 completa.

A leitura mais equilibrada é esta:

| Dimensão | Evidência observada | Interpretação |
|---|---|---|
| Estado | PostgreSQL, Redis, Prisma, tabelas de usuário, carrinho, pedido, memórias e contexto | Base persistente forte, mas checkpoints explícitos por decisão ainda faltam |
| Histórico | 60 mensagens no WhatsApp e 20 na API | Janela prática boa, mas truncamento sem compactação crítica gera risco |
| Tools | 20+ tools KODA com schema Zod | Contrato de input forte, mas output e decisão ainda precisam de validação runtime e manifest |
| Roteamento | LangGraph com coach, ecommerce e voturuna, mas ecommerce default em produção | Existe scaffolding multi-agent, mas KODA opera majoritariamente como single agent com tools |
| Traces | `orchestrator_turn_trace` e `state_build_trace` com timings | Boa visibilidade operacional, ainda sem replay completo da decisão |
| Memória | MemoryExtractionService em background com categorias | Boa base, mas não substitui compactação server-side com criticidade |
| Coordenação | Redis locks em alguns fluxos, lock em memória no carrinho, fila com race condition documentada | Coordenação parcial, áreas frágeis para order e cart |
| Evolução | Timings e logs existem, custo e ROI não aparecem como primeira classe | Sem governança formal do harness |

### O que KODA já faz bem

#### Força: Validação de input

Joi, Zod schemas e tools estruturadas reduzem input inválido chegando ao agente.

#### Força: Persistência de domínio

Dados relevantes vivem em PostgreSQL, incluindo usuário, pedidos, memórias e carrinho persistente.

#### Força: Cache operacional

Redis com TTL curto reduz custo de carregar perfil estático.

#### Força: Memory extraction

Um modelo menor extrai fatos em background e salva categorias como preferences, dietary, medical e goals.

#### Força: Idempotência em bordas críticas

Webhooks e mensagens têm deduplicação por identificadores.

#### Força: Timings por etapa

StageTimings permite ver build_state_ms, graph_invoke_ms e outras etapas.

#### Força: Anti-spam

Gate de mensagens proativas limita frequência por dia, hora e tipo.

#### Força: Fast path

Quando só um agente está ativo, o router é pulado e economiza cerca de 800ms.

### Onde o diagnóstico fica mais severo

* **Single agent + tools:** O diagnóstico de comparação Nível 3 registra que o KODA ecommerce em produção funciona como um agente único com prompt grande e tools, não como uma equipe coordenada de Planner, Discovery, Catalog, Generator, Evaluator, Order, Fulfillment e Recovery.
* **Planner ausente:** O campo de status existe, mas a análise aponta retorno constante como navegando em ponto crítico do builder, o que reduz valor de planejamento explícito.
* **Evaluator ausente como agente independente:** Há filtros, regras e prompts, mas não um segundo agente com rubrica formal revisando cada decisão comercial antes do envio.
* **Truncamento sem compactação crítica:** Histórico de 60 ou 20 mensagens ajuda, mas fatos antigos podem sair da janela sem resumo curado por criticidade.
* **Audit manifest ausente:** Logs mostram timings e alguns eventos, mas não uma cadeia completa ligando inputs, tools, outputs e decisão final.
* **Coordenação frágil em áreas específicas:** O carrinho usa `Map` em memória em parte do fluxo e existem riscos de corrida documentados em processamento.
* **Custo invisível:** Sem custo por chamada, tokens por componente e ROI por proteção, o time não sabe quais camadas dão retorno real.

---

## 🧩 Gaps Identificados com Dados de Apoio

### Gap 1: single-agent + tools em vez de decomposição real

**Dado de apoio:** O documento de comparação Nível 3 descreve o grafo efetivo como START para ecommerceAgenteNode para END em produção e classifica a arquitetura como Single Agent com tools.

**Risco para KODA:** O mesmo prompt carrega discovery, recomendação, checkout, segurança, recuperação e escrita de resposta. Isso concentra responsabilidade demais em um único raciocínio.

**Proposta de melhoria:** Criar decomposição gradual com Planner e Evaluator primeiro, mantendo tools existentes e adicionando artefatos auditáveis.

**Perguntas de validação:**

* Qual incidente real esta melhoria previne?
* Qual métrica prova que o risco caiu?
* Qual custo novo ela adiciona?
* Como podemos desligar ou simplificar se não gerar valor?
* Qual evidência precisa entrar em ADR?

### Gap 2: ausência de Planner explícito confiável

**Dado de apoio:** O diagnóstico cita status de conversa sempre retornando navegando em ponto específico, apesar de existirem estados como checkout, pagamento e finalizado.

**Risco para KODA:** Sem plano serializado, cada turno pode reinterpretar a jornada e repetir perguntas, pular etapa ou agir antes da confirmação.

**Proposta de melhoria:** Criar `agent_plan` persistido por turno, com etapa, próxima ação, bloqueios e fontes consultadas.

**Perguntas de validação:**

* Qual incidente real esta melhoria previne?
* Qual métrica prova que o risco caiu?
* Qual custo novo ela adiciona?
* Como podemos desligar ou simplificar se não gerar valor?
* Qual evidência precisa entrar em ADR?

### Gap 3: Evaluator sem independência operacional

**Dado de apoio:** As análises indicam filtros binários, regras de prompt e ProductRecommendationFilter, mas não um Evaluator com scoring 0 a 100 e rubrica multidimensional.

**Risco para KODA:** Recomendações podem ser válidas no mínimo, mas ruins em custo-benefício, satisfação esperada ou viabilidade operacional.

**Proposta de melhoria:** Adicionar evaluator dedicado para recomendação e pedido, com rubrica de adequação, custo-benefício, satisfação e viabilidade.

**Perguntas de validação:**

* Qual incidente real esta melhoria previne?
* Qual métrica prova que o risco caiu?
* Qual custo novo ela adiciona?
* Como podemos desligar ou simplificar se não gerar valor?
* Qual evidência precisa entrar em ADR?

### Gap 4: histórico 60/20 sem compactação server-side crítica

**Dado de apoio:** ConversationStateBuilder limita histórico a 60 mensagens no WhatsApp e 20 na API. O diagnóstico diz que não há pipeline de compactação com classificação de criticidade.

**Risco para KODA:** Fatos antigos como restrição de cafeína, alergia ou orçamento podem sair da janela e não voltar ao prompt no momento certo.

**Proposta de melhoria:** Criar compactação server-side com classes crítico, importante, útil e ruído, preservando fatos de segurança e decisões comerciais.

**Perguntas de validação:**

* Qual incidente real esta melhoria previne?
* Qual métrica prova que o risco caiu?
* Qual custo novo ela adiciona?
* Como podemos desligar ou simplificar se não gerar valor?
* Qual evidência precisa entrar em ADR?

### Gap 5: traces parciais, sem replay completo

**Dado de apoio:** Há `orchestrator_turn_trace` e `state_build_trace`, mas o diagnóstico de Nível 2 aponta ausência de log estruturado de tool calls, argumentos, resultados e replay da decisão.

**Risco para KODA:** Quando suporte pergunta por que KODA recomendou X e não Y, o time vê latência e contagens, mas não a cadeia de decisão completa.

**Proposta de melhoria:** Criar `turn_manifest` por decisão, com tool calls, inputs, outputs, versões de rubrica, custos e decisão final.

**Perguntas de validação:**

* Qual incidente real esta melhoria previne?
* Qual métrica prova que o risco caiu?
* Qual custo novo ela adiciona?
* Como podemos desligar ou simplificar se não gerar valor?
* Qual evidência precisa entrar em ADR?

### Gap 6: coordenação frágil em carrinho e pedido

**Dado de apoio:** O diagnóstico cita `CartService` com `Map` em memória, locks em memória e race condition documentada em fila. Também reconhece dedup forte em webhooks e mensagens.

**Risco para KODA:** Um restart ou uma corrida em mensagens pode criar carrinho inconsistente, pedido duplicado ou recuperação incompleta.

**Proposta de melhoria:** Mover coordenação crítica para locks duráveis, idempotency key por intenção comercial e checkpoint antes de efeitos externos.

**Perguntas de validação:**

* Qual incidente real esta melhoria previne?
* Qual métrica prova que o risco caiu?
* Qual custo novo ela adiciona?
* Como podemos desligar ou simplificar se não gerar valor?
* Qual evidência precisa entrar em ADR?

### Gap 7: custo, ROI e lifecycle do harness sem primeira classe

**Dado de apoio:** Os documentos citam StageTimings, mas ausência de tracking de custo LLM, tokens, decision records e remoção segura baseada em métrica.

**Risco para KODA:** O harness cresce por reação a incidentes e nunca passa por revisão econômica ou remoção planejada.

**Proposta de melhoria:** Instituir métricas de custo por componente e ciclo BUILD, STABILIZE, SIMPLIFY, REMOVE com ADR por mudança relevante.

**Perguntas de validação:**

* Qual incidente real esta melhoria previne?
* Qual métrica prova que o risco caiu?
* Qual custo novo ela adiciona?
* Como podemos desligar ou simplificar se não gerar valor?
* Qual evidência precisa entrar em ADR?

---

## 🏗️ Diagrama ASCII: Harness Atual vs Harness Proposto


O diagrama abaixo compara o estado diagnosticado com uma proposta incremental. A coluna proposta não deve ser lida como produção atual.

```text
+--------------------------------------------------------------------------------+
| KODA ATUAL DIAGNOSTICADO                                                       |
+--------------------------------------------------------------------------------+
| WhatsApp/API                                                                    |
|      |                                                                          |
|      v                                                                          |
| webhook-unified                                                                 |
|      |                                                                          |
|      v                                                                          |
| OrchestratorAgent                                                               |
|      |                                                                          |
|      +-- ConversationStateBuilder                                              |
|      |      +-- PostgreSQL: user, cart, orders, memories                       |
|      |      +-- Redis: cache curto de perfil                                   |
|      |      +-- History window: 60 WhatsApp / 20 API                           |
|      |      +-- CartService com area em memoria                                |
|      |                                                                          |
|      v                                                                          |
| ecommerceAgenteNode                                                            |
|      |                                                                          |
|      +-- prompt grande + 20+ tools                                             |
|      +-- regras de seguranca no prompt                                         |
|      +-- filtros e tools de catalogo                                           |
|      +-- resposta final                                                        |
|                                                                                 |
| Observabilidade: timings e logs parciais                                       |
| Gap: sem Planner real, sem Evaluator independente, sem manifest completo        |
+--------------------------------------------------------------------------------+

+--------------------------------------------------------------------------------+
| HARNESS PROPOSTO PARA EVOLUCAO GRADUAL                                         |
+--------------------------------------------------------------------------------+
| WhatsApp/API                                                                    |
|      |                                                                          |
|      v                                                                          |
| Ingress + idempotency por intencao comercial                                   |
|      |                                                                          |
|      v                                                                          |
| Turn Controller                                                                 |
|      |                                                                          |
|      +-- load_state_checkpoint                                                 |
|      +-- load_compacted_context                                                |
|      +-- start_turn_manifest                                                   |
|      |                                                                          |
|      v                                                                          |
| Planner                                                                         |
|      | escreve agent_plan                                                       |
|      v                                                                          |
| Discovery / Catalog / Generator                                                |
|      | escrevem artefatos de trabalho                                          |
|      v                                                                          |
| Evaluator                                                                       |
|      | aplica rubrica, contrato e guardrails                                   |
|      v                                                                          |
| Order / Fulfillment                                                            |
|      | usam lock duravel e checkpoint antes de efeito externo                  |
|      v                                                                          |
| Response Renderer                                                               |
|      |                                                                          |
|      v                                                                          |
| close_turn_manifest + metrics + cost + ROI                                     |
|                                                                                 |
| Governanca: BUILD -> STABILIZE -> SIMPLIFY -> REMOVE                           |
+--------------------------------------------------------------------------------+
```

---

## ⚖️ Tabela Comparativa de Estratégias de Coordenação

| Estratégia | Onde encaixa | Força | Limite | Recomendação para KODA |
|---|---|---|---|---|
| Memória local do processo | Cache curto e dados descartáveis | Muito rápida | Some em restart e não coordena múltiplas instâncias | Não usar para carrinho ou pedido como fonte primária |
| Redis lock | Debounce, jobs e exclusão distribuída curta | Boa latência e TTL simples | Precisa política clara em falha | Manter para eventos rápidos e medir falhas fail-open |
| PostgreSQL transacional | Pedido, carrinho, pagamento e idempotência | Durável e auditável | Mais custo de modelagem | Usar como base para estado comercial crítico |
| Arquivo JSON local | Didática, protótipo e workflows locais | Fácil de auditar e ensinar | Não escala sozinho em múltiplas instâncias | Usar como metáfora curricular ou storage controlado |
| Manifest por turno | Auditoria e replay | Liga decisão a inputs e outputs | Exige disciplina de schema | Implementar como artefato persistido |
| Fila por usuário | Ordenação de mensagens | Reduz corrida por cliente | Pode ter race se mal implementada | Revisar race condition antes de order |
| Event sourcing | Reconstituição de estado e auditoria forte | Replay completo | Mais complexo | Avaliar no longo prazo |
| Shadow test | Validar proposta sem afetar cliente | Baixo risco | Custo extra de execução | Usar para Evaluator, compaction e remoção de componentes |

---

## 🚦 Propostas de Melhoria Priorizadas

### P1: Manifest de turno auditável

**Prioridade:** Muito alta

**Por que agora:** Aumenta diagnóstico sem alterar a decisão do agente no primeiro momento.

**Escopo proposto:** Persistir inputs, tool calls, outputs, timings, custos e versão de rubrica por turno.

**Risco de implementação:** Baixo se começar como observabilidade sem mudar comportamento.

**Métrica principal:** 90% dos turnos comerciais com manifest completo em 30 dias.

**Critérios de aceitação da proposta:**

* Pode rodar primeiro em modo observação ou shadow test.
* Não remove proteção existente sem comparação controlada.
* Gera evidência que suporte decisão técnica.
* Tem plano de rollback ou desativação por configuração.
* Tem dono técnico e cadência de revisão.

### P2: Evaluator de recomendação com rubrica 0 a 100

**Prioridade:** Muito alta

**Por que agora:** Ataca o gap de qualidade e reduz self-evaluation collapse em decisões comerciais.

**Escopo proposto:** Avaliar adequação, custo-benefício, satisfação esperada e viabilidade operacional antes de recomendar.

**Risco de implementação:** Médio por custo e latência adicional.

**Métrica principal:** Reduzir recomendações rejeitadas em revisão humana e manter latência dentro do SLA definido.

**Critérios de aceitação da proposta:**

* Pode rodar primeiro em modo observação ou shadow test.
* Não remove proteção existente sem comparação controlada.
* Gera evidência que suporte decisão técnica.
* Tem plano de rollback ou desativação por configuração.
* Tem dono técnico e cadência de revisão.

### P3: Planner leve com `agent_plan` persistido

**Prioridade:** Alta

**Por que agora:** Dá estado explícito de jornada e reduz repetição ou pulo de etapa.

**Escopo proposto:** Registrar etapa, intenção, próxima ação, bloqueio, fontes e validade do plano.

**Risco de implementação:** Médio, porque plano errado pode travar conversa se não houver recuperação.

**Métrica principal:** Aumentar acerto de etapa em amostra auditada e reduzir perguntas repetidas.

**Critérios de aceitação da proposta:**

* Pode rodar primeiro em modo observação ou shadow test.
* Não remove proteção existente sem comparação controlada.
* Gera evidência que suporte decisão técnica.
* Tem plano de rollback ou desativação por configuração.
* Tem dono técnico e cadência de revisão.

### P4: Compactação server-side com criticidade

**Prioridade:** Alta

**Por que agora:** Ataca risco do histórico 60/20 sem depender apenas de recall de memória.

**Escopo proposto:** Classificar fatos como crítico, importante, útil ou ruído antes de resumir.

**Risco de implementação:** Médio por risco de resumo ruim.

**Métrica principal:** Zero perda de fatos críticos em shadow tests de conversas longas.

**Critérios de aceitação da proposta:**

* Pode rodar primeiro em modo observação ou shadow test.
* Não remove proteção existente sem comparação controlada.
* Gera evidência que suporte decisão técnica.
* Tem plano de rollback ou desativação por configuração.
* Tem dono técnico e cadência de revisão.

### P5: Checkpoint comercial antes de efeitos externos

**Prioridade:** Alta

**Por que agora:** Protege carrinho, pedido e pagamento contra restart e corrida.

**Escopo proposto:** Salvar checkpoint de cart, order draft e payment intent antes de gerar link ou reservar estoque.

**Risco de implementação:** Médio por exigir integração com fluxo existente.

**Métrica principal:** 100% dos pedidos com checkpoint recuperável antes de efeito externo.

**Critérios de aceitação da proposta:**

* Pode rodar primeiro em modo observação ou shadow test.
* Não remove proteção existente sem comparação controlada.
* Gera evidência que suporte decisão técnica.
* Tem plano de rollback ou desativação por configuração.
* Tem dono técnico e cadência de revisão.

### P6: Coordenação durável para order

**Prioridade:** Média alta

**Por que agora:** Reduz risco de pedido duplicado ou concorrência em mensagens rápidas.

**Escopo proposto:** Idempotency key por intenção comercial, lock durável e status de processamento visível.

**Risco de implementação:** Médio por impacto em fluxo de checkout.

**Métrica principal:** Nenhum pedido duplicado por corrida em bateria de testes e monitoramento.

**Critérios de aceitação da proposta:**

* Pode rodar primeiro em modo observação ou shadow test.
* Não remove proteção existente sem comparação controlada.
* Gera evidência que suporte decisão técnica.
* Tem plano de rollback ou desativação por configuração.
* Tem dono técnico e cadência de revisão.

### P7: Governança de harness com custo, ROI e ADR

**Prioridade:** Média

**Por que agora:** Impede acumular peso morto conforme modelos e fluxos evoluem.

**Escopo proposto:** Adicionar métricas de token, custo, acionamento, falso positivo e decisão BUILD/STABILIZE/SIMPLIFY/REMOVE.

**Risco de implementação:** Baixo, começa como processo e telemetria.

**Métrica principal:** 100% dos componentes novos de harness com métrica de valor e ADR de entrada.

**Critérios de aceitação da proposta:**

* Pode rodar primeiro em modo observação ou shadow test.
* Não remove proteção existente sem comparação controlada.
* Gera evidência que suporte decisão técnica.
* Tem plano de rollback ou desativação por configuração.
* Tem dono técnico e cadência de revisão.

---

## 🗺️ Roadmap de Implementação

### Curto prazo: 0 a 30 dias

* Criar schema do manifest de turno.
* Instrumentar tool calls principais com nome, duração, argumentos redigidos e resultado resumido.
* Adicionar custo estimado por chamada LLM quando o provider expuser tokens.
* Criar amostra de 50 conversas longas para shadow tests de compactação.
* Definir rubrica inicial de recomendação KODA com pesos e threshold.
* Rodar Evaluator em shadow mode para não afetar usuário.
* Documentar ADR da melhoria de manifest e ADR da rubrica inicial.
* Mapear pontos de efeito externo no checkout: criar pedido, link de pagamento, reserva e mensagem final.

**Sinal de saída da fase:**

O time consegue explicar uma decisão comercial lendo manifest, trace parcial e rubrica shadow sem alterar comportamento do usuário.

### Médio prazo: 31 a 90 dias

* Ativar Evaluator para uma fatia controlada de recomendações de menor risco.
* Persistir `agent_plan` em turnos comerciais com etapa e próxima ação.
* Implementar compactação server-side para conversas acima de limite definido.
* Criar checkpoint antes de link de pagamento.
* Substituir dependência de estado em memória em áreas críticas por fonte durável.
* Criar dashboard de taxa de acionamento, latência, custo e rejeição por rubrica.
* Executar simulações de restart durante checkout.
* Treinar suporte para consultar manifest em incidentes selecionados.

**Sinal de saída da fase:**

KODA já usa pelo menos uma melhoria ativa em produção controlada, com métricas de qualidade, custo e rollback claro.

### Longo prazo: 91 a 180 dias

* Evoluir Planner leve para decomposição real de jornada comercial.
* Separar agentes Discovery, Catalog, Evaluator, Order e Recovery quando as métricas justificarem.
* Adicionar replay controlado de decisão para debugging interno.
* Criar ciclo trimestral BUILD, STABILIZE, SIMPLIFY, REMOVE.
* Rodar shadow tests para remoção ou simplificação de guards redundantes.
* Amarrar custo por componente a ROI de incidentes prevenidos.
* Consolidar ADRs em trilha de evolução do harness.
* Definir política de fail-open e fail-closed por tipo de decisão comercial.

**Sinal de saída da fase:**

O harness passa a ser governado por ciclo de vida, com remoção segura e decisões registradas em ADR.

---

## 📏 Métricas de Sucesso por Melhoria

### Métricas para P1: Manifest de turno auditável

| Métrica | Como medir | Por que importa |
|---|---|---|
| Cobertura | Percentual de turnos elegíveis cobertos pela melhoria | Mostra adoção real |
| Qualidade | Taxa de decisões aprovadas em revisão ou rubrica | Mostra efeito no cliente |
| Latência | Delta de p95 antes e depois | Evita melhorar qualidade quebrando UX |
| Custo | Tokens e custo por turno com a melhoria | Permite ROI |
| Auditabilidade | Percentual de incidentes diagnosticáveis sem reprocessar manualmente logs soltos | Reduz tempo de suporte e engenharia |
| Reversibilidade | Tempo para desligar ou contornar a melhoria | Evita aprisionamento arquitetural |

**Threshold inicial sugerido:**

* 95% dos turnos comerciais com manifest válido.
* Menos de 5% de manifests sem tool call principal.
* Consulta de incidente em até 10 minutos usando manifest.

### Métricas para P2: Evaluator de recomendação com rubrica 0 a 100

| Métrica | Como medir | Por que importa |
|---|---|---|
| Cobertura | Percentual de turnos elegíveis cobertos pela melhoria | Mostra adoção real |
| Qualidade | Taxa de decisões aprovadas em revisão ou rubrica | Mostra efeito no cliente |
| Latência | Delta de p95 antes e depois | Evita melhorar qualidade quebrando UX |
| Custo | Tokens e custo por turno com a melhoria | Permite ROI |
| Auditabilidade | Percentual de incidentes diagnosticáveis sem reprocessar manualmente logs soltos | Reduz tempo de suporte e engenharia |
| Reversibilidade | Tempo para desligar ou contornar a melhoria | Evita aprisionamento arquitetural |

**Threshold inicial sugerido:**

* Evaluator em shadow mode com concordância humana acima de 80%.
* Rejeições explicáveis em 95% dos casos.
* Aumento de latência dentro do limite definido pelo time.

### Métricas para P3: Planner leve com `agent_plan` persistido

| Métrica | Como medir | Por que importa |
|---|---|---|
| Cobertura | Percentual de turnos elegíveis cobertos pela melhoria | Mostra adoção real |
| Qualidade | Taxa de decisões aprovadas em revisão ou rubrica | Mostra efeito no cliente |
| Latência | Delta de p95 antes e depois | Evita melhorar qualidade quebrando UX |
| Custo | Tokens e custo por turno com a melhoria | Permite ROI |
| Auditabilidade | Percentual de incidentes diagnosticáveis sem reprocessar manualmente logs soltos | Reduz tempo de suporte e engenharia |
| Reversibilidade | Tempo para desligar ou contornar a melhoria | Evita aprisionamento arquitetural |

**Threshold inicial sugerido:**

* Etapa correta em 85% da amostra auditada.
* Queda de perguntas repetidas em conversas longas.
* Plano inválido recuperado sem bloquear atendimento.

### Métricas para P4: Compactação server-side com criticidade

| Métrica | Como medir | Por que importa |
|---|---|---|
| Cobertura | Percentual de turnos elegíveis cobertos pela melhoria | Mostra adoção real |
| Qualidade | Taxa de decisões aprovadas em revisão ou rubrica | Mostra efeito no cliente |
| Latência | Delta de p95 antes e depois | Evita melhorar qualidade quebrando UX |
| Custo | Tokens e custo por turno com a melhoria | Permite ROI |
| Auditabilidade | Percentual de incidentes diagnosticáveis sem reprocessar manualmente logs soltos | Reduz tempo de suporte e engenharia |
| Reversibilidade | Tempo para desligar ou contornar a melhoria | Evita aprisionamento arquitetural |

**Threshold inicial sugerido:**

* 100% de fatos críticos preservados em suite de conversa longa.
* Resumo com redução de tokens mensurável.
* Nenhum caso de alergia ou restrição rebaixada para preferência genérica.

### Métricas para P5: Checkpoint comercial antes de efeitos externos

| Métrica | Como medir | Por que importa |
|---|---|---|
| Cobertura | Percentual de turnos elegíveis cobertos pela melhoria | Mostra adoção real |
| Qualidade | Taxa de decisões aprovadas em revisão ou rubrica | Mostra efeito no cliente |
| Latência | Delta de p95 antes e depois | Evita melhorar qualidade quebrando UX |
| Custo | Tokens e custo por turno com a melhoria | Permite ROI |
| Auditabilidade | Percentual de incidentes diagnosticáveis sem reprocessar manualmente logs soltos | Reduz tempo de suporte e engenharia |
| Reversibilidade | Tempo para desligar ou contornar a melhoria | Evita aprisionamento arquitetural |

**Threshold inicial sugerido:**

* 100% dos pedidos elegíveis com checkpoint antes de efeito externo.
* Recuperação validada em simulação de restart.
* Zero perda de carrinho em testes de falha controlada.

### Métricas para P6: Coordenação durável para order

| Métrica | Como medir | Por que importa |
|---|---|---|
| Cobertura | Percentual de turnos elegíveis cobertos pela melhoria | Mostra adoção real |
| Qualidade | Taxa de decisões aprovadas em revisão ou rubrica | Mostra efeito no cliente |
| Latência | Delta de p95 antes e depois | Evita melhorar qualidade quebrando UX |
| Custo | Tokens e custo por turno com a melhoria | Permite ROI |
| Auditabilidade | Percentual de incidentes diagnosticáveis sem reprocessar manualmente logs soltos | Reduz tempo de suporte e engenharia |
| Reversibilidade | Tempo para desligar ou contornar a melhoria | Evita aprisionamento arquitetural |

**Threshold inicial sugerido:**

* Zero duplicidade em testes de mensagens simultâneas.
* Lock expirado tratado com recuperação segura.
* Idempotency key registrada em cada pedido elegíveis.

### Métricas para P7: Governança de harness com custo, ROI e ADR

| Métrica | Como medir | Por que importa |
|---|---|---|
| Cobertura | Percentual de turnos elegíveis cobertos pela melhoria | Mostra adoção real |
| Qualidade | Taxa de decisões aprovadas em revisão ou rubrica | Mostra efeito no cliente |
| Latência | Delta de p95 antes e depois | Evita melhorar qualidade quebrando UX |
| Custo | Tokens e custo por turno com a melhoria | Permite ROI |
| Auditabilidade | Percentual de incidentes diagnosticáveis sem reprocessar manualmente logs soltos | Reduz tempo de suporte e engenharia |
| Reversibilidade | Tempo para desligar ou contornar a melhoria | Evita aprisionamento arquitetural |

**Threshold inicial sugerido:**

* 100% dos novos componentes com custo e métrica de valor.
* Revisão trimestral executada.
* Pelo menos uma simplificação decidida com base em dados quando houver evidência.

---

## 📊 Tabela de Impacto das Melhorias

| Proposta | Impacto no cliente | Impacto técnico | Custo esperado | Risco | Primeiro modo de uso |
|---|---|---|---|---|---|
| Manifest de turno | Resolução mais rápida de incidentes | Melhor replay e auditoria | Baixo a médio storage | Baixo | Observação |
| Evaluator com rubrica | Recomendações mais confiáveis | Separação de geração e crítica | LLM extra ou tool extra | Médio | Shadow test |
| Planner leve | Menos repetição e menos pulo de etapa | Plano explícito por turno | Baixo a médio | Médio | Produção parcial |
| Compactação crítica | Menos esquecimento em conversas longas | Resumo curado e menor contexto | Médio | Médio | Shadow test |
| Checkpoint comercial | Recuperação após restart | Estado transacional claro | Médio | Médio | Canary |
| Coordenação durável | Menos duplicidade e inconsistência | Locks e idempotência fortes | Médio | Médio | Canary |
| Governança ROI e ADR | Melhor foco do time em melhorias úteis | Ciclo de vida do harness | Baixo | Baixo | Processo |

---

## ✅ Checklist de Implementação por Fase

### Fase 1: Descoberta e alinhamento

* [ ] Confirmar que cada proposta está ligada a um gap documentado.
* [ ] Separar fato atual de arquitetura proposta.
* [ ] Definir dono técnico por proposta.
* [ ] Definir métrica principal e métrica de segurança.
* [ ] Escolher uma amostra de conversas reais anonimizadas.
* [ ] Criar critérios de rollback antes de alterar comportamento.
* [ ] Registrar ADR inicial quando houver mudança arquitetural.

**Pergunta de controle:**

Se esta fase falhar, o cliente fica protegido e o time sabe como voltar ao comportamento anterior?

### Fase 2: Instrumentação sem mudar comportamento

* [ ] Adicionar manifest em modo observação.
* [ ] Capturar timings já existentes no novo formato.
* [ ] Capturar tool calls com argumentos seguros e resultados resumidos.
* [ ] Registrar custo quando disponível.
* [ ] Comparar manifest com logs atuais.
* [ ] Validar que dados sensíveis não vazam em artefatos.
* [ ] Criar painel mínimo de cobertura e falhas de manifest.

**Pergunta de controle:**

Se esta fase falhar, o cliente fica protegido e o time sabe como voltar ao comportamento anterior?

### Fase 3: Shadow test de qualidade

* [ ] Rodar Evaluator sem bloquear resposta ao usuário.
* [ ] Rodar compaction em paralelo sem substituir contexto ativo.
* [ ] Comparar decisões shadow com decisões atuais.
* [ ] Medir concordância humana em amostra semanal.
* [ ] Registrar falsos positivos e falsos negativos.
* [ ] Ajustar rubrica com evidência, não opinião isolada.
* [ ] Definir threshold para canary.

**Pergunta de controle:**

Se esta fase falhar, o cliente fica protegido e o time sabe como voltar ao comportamento anterior?

### Fase 4: Canary controlado

* [ ] Ativar melhoria em fatia pequena e reversível.
* [ ] Monitorar latência p50, p95 e p99.
* [ ] Monitorar custo por turno.
* [ ] Monitorar rejeições e recuperações.
* [ ] Comparar incidentes contra grupo controle quando possível.
* [ ] Revisar suporte e feedback qualitativo.
* [ ] Decidir expandir, ajustar ou pausar.

**Pergunta de controle:**

Se esta fase falhar, o cliente fica protegido e o time sabe como voltar ao comportamento anterior?

### Fase 5: Produção ampliada

* [ ] Expandir cobertura com limites claros.
* [ ] Atualizar documentação de operação.
* [ ] Treinar suporte e engenharia em leitura de manifest.
* [ ] Criar alerta para regressões da melhoria.
* [ ] Registrar aprendizados em ADR final.
* [ ] Definir data de revisão da melhoria.
* [ ] Planejar etapa STABILIZE.

**Pergunta de controle:**

Se esta fase falhar, o cliente fica protegido e o time sabe como voltar ao comportamento anterior?

### Fase 6: Evolução e remoção segura

* [ ] Medir taxa de acionamento real.
* [ ] Medir falsos positivos.
* [ ] Medir custo mensal.
* [ ] Calcular ROI por trimestre.
* [ ] Rodar shadow test com componente simplificado quando fizer sentido.
* [ ] Mover melhoria para SIMPLIFY se custo superar valor.
* [ ] Remover apenas com evidência, flag e ADR.

**Pergunta de controle:**

Se esta fase falhar, o cliente fica protegido e o time sabe como voltar ao comportamento anterior?

---

## 🧪 Playbook de Shadow Test

### Passo 1: Definir hipótese

Exemplo: um Evaluator com rubrica reduz recomendações inadequadas sem aumentar demais a latência.

**Evidência mínima:**

* Registro do input usado.
* Registro do output baseline.
* Registro do output proposto.
* Decisão comparativa.
* Observação sobre custo e risco.

### Passo 2: Selecionar amostra

Usar conversas reais anonimizadas com variedade de objetivos, restrições, orçamento e etapa de jornada.

**Evidência mínima:**

* Registro do input usado.
* Registro do output baseline.
* Registro do output proposto.
* Decisão comparativa.
* Observação sobre custo e risco.

### Passo 3: Rodar caminho atual

Preservar output atual como baseline.

**Evidência mínima:**

* Registro do input usado.
* Registro do output baseline.
* Registro do output proposto.
* Decisão comparativa.
* Observação sobre custo e risco.

### Passo 4: Rodar caminho proposto

Executar melhoria sem afetar resposta ao cliente.

**Evidência mínima:**

* Registro do input usado.
* Registro do output baseline.
* Registro do output proposto.
* Decisão comparativa.
* Observação sobre custo e risco.

### Passo 5: Comparar decisão

Registrar quando o caminho proposto aprova, rejeita ou pede reparo.

**Evidência mínima:**

* Registro do input usado.
* Registro do output baseline.
* Registro do output proposto.
* Decisão comparativa.
* Observação sobre custo e risco.

### Passo 6: Revisar com humanos

Amostra semanal revisada por engenharia, produto ou suporte.

**Evidência mínima:**

* Registro do input usado.
* Registro do output baseline.
* Registro do output proposto.
* Decisão comparativa.
* Observação sobre custo e risco.

### Passo 7: Medir custo

Tokens, latência, storage e horas de análise.

**Evidência mínima:**

* Registro do input usado.
* Registro do output baseline.
* Registro do output proposto.
* Decisão comparativa.
* Observação sobre custo e risco.

### Passo 8: Decidir próximo passo

Promover para canary, ajustar rubrica ou encerrar proposta.

**Evidência mínima:**

* Registro do input usado.
* Registro do output baseline.
* Registro do output proposto.
* Decisão comparativa.
* Observação sobre custo e risco.

---

## 🧠 Aplicação KODA: Como Fernando Priorizaria as Melhorias


Fernando não começa perguntando qual arquitetura parece mais elegante.

Ele começa com cinco perguntas simples:

* Qual falha real queremos reduzir primeiro?
* Qual melhoria gera evidência mesmo se ainda não mudar comportamento?
* Qual mudança tem menor risco de prejudicar cliente?
* Qual proposta cria base para as próximas?
* Qual componente precisa nascer com data de revisão?

A resposta mais provável é começar por manifest de turno, Evaluator em shadow mode e mapeamento de checkpoint comercial. Essas três frentes criam visibilidade, reduzem self-evaluation e protegem efeitos externos sem exigir reescrever o agente por completo.

### Decisão proposta de Fernando

```text
Semana 1: manifest e rubrica shadow.
Semana 2: tool_call_trace e amostra de revisão humana.
Semana 3: checkpoint antes de pagamento em teste controlado.
Semana 4: decisão de canary com dados.
```

---

## 🧭 Cartões de Cenário KODA

### Cenário 1: Pedro

**Problema:** carrinho perdido depois de restart.

**Melhoria proposta:** checkpoint comercial.

**Resultado esperado:** cart checkpoint recuperável antes de pagamento.

**Passo a passo recomendado:**

1. Criar checkpoint para o ponto em que Pedro falha: carrinho perdido depois de restart.
2. Gerar idempotency key por intenção comercial antes de link, reserva ou retry.
3. Persistir carrinho, order draft, etapa atual e próxima ação antes de efeito externo.
4. Acionar Recovery agent quando houver restart, retry ou retorno sem estado em memória.
5. Comparar checkpoint recuperado com estoque, preço e pedido durável antes de responder.
6. Validar com simulação de restart que o resultado esperado se mantém: cart checkpoint recuperável antes de pagamento.
7. Retomar a conversa com Pedro sem pedir de novo dados já confirmados.

**Métrica de sucesso:**

* 100% dos fluxos de Pedro têm checkpoint antes do efeito externo relevante.
* Restart simulado recupera carrinho, pedido e etapa sem depender de memória local.
* Idempotency key impede pedido, pagamento ou retry duplicado na mesma intenção.
* Pedro retoma o fluxo com o resultado esperado: cart checkpoint recuperável antes de pagamento.

### Cenário 2: Marina

**Problema:** duas mensagens rápidas pedindo o mesmo item.

**Melhoria proposta:** coordenação durável.

**Resultado esperado:** idempotency key por intenção de compra.

**Passo a passo recomendado:**

1. Derivar idempotency key da intenção de Marina, considerando o problema: duas mensagens rápidas pedindo o mesmo item.
2. Abrir lock durável por cliente e intenção antes de alterar carrinho ou pedido.
3. Registrar dedup log com evento aceito, evento repetido, sequência e decisão.
4. Processar conflitos mantendo a intenção mais recente sem sobrescrever estado novo.
5. Liberar o lock só depois de persistir estado, manifest e resposta planejada.
6. Testar mensagens simultâneas, duplicadas e fora de ordem para o mesmo cliente.
7. Responder a Marina com uma única decisão consistente: idempotency key por intenção de compra.

**Métrica de sucesso:**

* Zero pedidos duplicados ou carrinhos divergentes em testes simultâneos.
* Dedup log mostra qual evento venceu, qual foi reaproveitado e por quê.
* Lock durável protege retry, fila atrasada e concorrência entre workers.
* Marina não recebe respostas conflitantes sobre a mesma intenção comercial.

### Cenário 3: Rafael

**Problema:** restrição de cafeína dita no início de conversa longa.

**Melhoria proposta:** compactação crítica.

**Resultado esperado:** fato crítico preservado fora da janela 60/20.

**Passo a passo recomendado:**

1. Classificar o fato central de Rafael por criticidade a partir de: restrição de cafeína dita no início de conversa longa.
2. Salvar fonte, trecho, timestamp e classe fora da janela 60/20.
3. Rodar compactação em shadow test antes de substituir o contexto ativo.
4. Comparar resposta baseline com resposta que usa `critical_summary`.
5. Medir retenção do fato em conversas longas, ruidosas e com mudança de assunto.
6. Bloquear recomendação ou decisão que contradiga fato crítico preservado.
7. Responder a Rafael mantendo o fato preservado no resultado: fato crítico preservado fora da janela 60/20.

**Métrica de sucesso:**

* 100% dos fatos críticos da amostra sobrevivem fora da janela 60/20.
* Shadow test mostra retenção maior sem aumento excessivo de tokens.
* Nenhuma restrição crítica é rebaixada para preferência ou ruído.
* Rafael não precisa repetir o fato para receber: fato crítico preservado fora da janela 60/20.

### Cenário 4: Bianca

**Problema:** cupom aplicado em categoria incorreta.

**Melhoria proposta:** Evaluator com rubrica.

**Resultado esperado:** pedido rejeitado antes de gerar link.

**Passo a passo recomendado:**

1. Definir dimensões de rubrica para a melhoria proposta: Evaluator com rubrica.
2. Adicionar critérios específicos para o problema de Bianca: cupom aplicado em categoria incorreta.
3. Rodar o Evaluator em shadow test contra a resposta atual do KODA.
4. Calibrar score e threshold com revisão humana de engenharia, produto ou suporte.
5. Registrar no manifest score, veredito, dimensão reprovada e instrução de reparo.
6. Ativar canary apenas quando latência, custo e falso bloqueio ficarem dentro do limite.
7. Enviar resposta aprovada que alcance o resultado esperado: pedido rejeitado antes de gerar link.

**Métrica de sucesso:**

* Revisão humana concorda com o veredito para Bianca acima do threshold definido.
* Falsos positivos e falsos negativos da rubrica são medidos por dimensão.
* Canary mantém latência e custo dentro do limite aceito pelo time.
* A decisão final evita o problema original e entrega: pedido rejeitado antes de gerar link.

### Cenário 5: Lucas

**Problema:** compra recorrente sem querer reabrir discovery.

**Melhoria proposta:** Planner leve.

**Resultado esperado:** etapa reconhecida como recompra.

**Passo a passo recomendado:**

1. Criar `agent_plan` com stage, intenção e próxima ação para Lucas.
2. Detectar a etapa correta a partir do problema: compra recorrente sem querer reabrir discovery.
3. Persistir bloqueios, fontes consultadas e validade do plano no turno.
4. Definir `expires_at` para evitar plano velho quando a conversa mudar.
5. Medir stage accuracy contra revisão humana da amostra relevante.
6. Registrar no manifest por que o plano pediu confirmação, pulou etapa ou avançou.
7. Responder a Lucas seguindo o plano até alcançar: etapa reconhecida como recompra.

**Métrica de sucesso:**

* Stage correto aparece em pelo menos 85% da amostra auditada.
* Planos vencidos expiram sem travar ou contaminar a próxima intenção.
* Perguntas repetidas e pulos de etapa caem no fluxo observado.
* Lucas recebe resposta compatível com a etapa real da jornada.

### Cenário 6: Ana

**Problema:** preferência por baunilha confundida com restrição médica.

**Melhoria proposta:** manifest de decisão.

**Resultado esperado:** suporte vê origem da classificação.

**Passo a passo recomendado:**

1. Definir no `turn_manifest` os campos necessários para explicar: preferência por baunilha confundida com restrição médica.
2. Registrar fonte, classe do fato, tool calls, versão de política e decisão final.
3. Logar classificação e motivo sem expor dado sensível no artefato de suporte.
4. Criar endpoint de suporte para consultar o turno sem reprocessar logs soltos.
5. Medir tempo de diagnóstico de incidentes antes e depois do manifest.
6. Registrar correção humana quando a classificação ou fonte escolhida estiver errada.
7. Permitir que suporte explique a Ana como o KODA chegou a: suporte vê origem da classificação.

**Métrica de sucesso:**

* Manifest mostra fonte, classificação e decisão final do turno auditado.
* Suporte diagnostica o incidente em menos de 10 minutos usando o endpoint.
* Campos sensíveis aparecem mascarados ou referenciados por identificador seguro.
* A explicação para Ana não depende de leitura manual de logs soltos.

### Cenário 7: João

**Problema:** pedido corporativo misturado com compra pessoal.

**Melhoria proposta:** Planner leve.

**Resultado esperado:** jornada B2B separada da jornada pessoa física.

**Passo a passo recomendado:**

1. Criar `agent_plan` com stage, intenção e próxima ação para João.
2. Detectar a etapa correta a partir do problema: pedido corporativo misturado com compra pessoal.
3. Persistir bloqueios, fontes consultadas e validade do plano no turno.
4. Definir `expires_at` para evitar plano velho quando a conversa mudar.
5. Medir stage accuracy contra revisão humana da amostra relevante.
6. Registrar no manifest por que o plano pediu confirmação, pulou etapa ou avançou.
7. Responder a João seguindo o plano até alcançar: jornada B2B separada da jornada pessoa física.

**Métrica de sucesso:**

* Stage correto aparece em pelo menos 85% da amostra auditada.
* Planos vencidos expiram sem travar ou contaminar a próxima intenção.
* Perguntas repetidas e pulos de etapa caem no fluxo observado.
* João recebe resposta compatível com a etapa real da jornada.

### Cenário 8: Nina

**Problema:** sabor indisponível trocado sem confirmação.

**Melhoria proposta:** Evaluator e Catalog.

**Resultado esperado:** SKU validado antes da resposta.

**Passo a passo recomendado:**

1. Consultar catálogo e estoque em tempo real para tratar: sabor indisponível trocado sem confirmação.
2. Validar SKU, variação, preço e disponibilidade antes de aprovar a resposta.
3. Aplicar Evaluator para bloquear troca silenciosa ou compra inviável.
4. Registrar no manifest SKU pedido, SKU validado, fonte de estoque e veredito.
5. Pedir confirmação quando a alternativa não for exatamente o item solicitado.
6. Rechecar estoque antes de criar order draft ou link de pagamento.
7. Responder a Nina apenas com SKU válido e decisão alinhada a: SKU validado antes da resposta.

**Métrica de sucesso:**

* 100% das respostas auditadas têm SKU validado antes de aprovação.
* Estoque é checado antes da recomendação e rechecado antes do order draft.
* Evaluator rejeita troca silenciosa, item indisponível ou compra inviável.
* Nina não recebe link nem sugestão final para SKU inválido.

### Cenário 9: Caio

**Problema:** comparação por preço por dose.

**Melhoria proposta:** rubrica de custo-benefício.

**Resultado esperado:** score considera dose e duração.

**Passo a passo recomendado:**

1. Definir dimensões de rubrica para a melhoria proposta: rubrica de custo-benefício.
2. Adicionar critérios específicos para o problema de Caio: comparação por preço por dose.
3. Rodar o Evaluator em shadow test contra a resposta atual do KODA.
4. Calibrar score e threshold com revisão humana de engenharia, produto ou suporte.
5. Registrar no manifest score, veredito, dimensão reprovada e instrução de reparo.
6. Ativar canary apenas quando latência, custo e falso bloqueio ficarem dentro do limite.
7. Enviar resposta aprovada que alcance o resultado esperado: score considera dose e duração.

**Métrica de sucesso:**

* Revisão humana concorda com o veredito para Caio acima do threshold definido.
* Falsos positivos e falsos negativos da rubrica são medidos por dimensão.
* Canary mantém latência e custo dentro do limite aceito pelo time.
* A decisão final evita o problema original e entrega: score considera dose e duração.

### Cenário 10: Lara

**Problema:** atraso de entrega com promessa indevida.

**Melhoria proposta:** Fulfillment + Evaluator proposto.

**Resultado esperado:** resposta não inventa data.

**Passo a passo recomendado:**

1. Definir dimensões de rubrica para a melhoria proposta: Fulfillment + Evaluator proposto.
2. Adicionar critérios específicos para o problema de Lara: atraso de entrega com promessa indevida.
3. Rodar o Evaluator em shadow test contra a resposta atual do KODA.
4. Calibrar score e threshold com revisão humana de engenharia, produto ou suporte.
5. Registrar no manifest score, veredito, dimensão reprovada e instrução de reparo.
6. Ativar canary apenas quando latência, custo e falso bloqueio ficarem dentro do limite.
7. Enviar resposta aprovada que alcance o resultado esperado: resposta não inventa data.

**Métrica de sucesso:**

* Revisão humana concorda com o veredito para Lara acima do threshold definido.
* Falsos positivos e falsos negativos da rubrica são medidos por dimensão.
* Canary mantém latência e custo dentro do limite aceito pelo time.
* A decisão final evita o problema original e entrega: resposta não inventa data.

### Cenário 11: Otávio

**Problema:** dois endereços possíveis no checkout.

**Melhoria proposta:** Planner e checkpoint.

**Resultado esperado:** pedido bloqueado até endereço escolhido.

**Passo a passo recomendado:**

1. Criar checkpoint de checkout para o problema de Otávio: dois endereços possíveis no checkout.
2. Gerar idempotency key para fechar pedido somente depois da escolha pendente.
3. Usar `agent_plan` para marcar a etapa bloqueada até a confirmação obrigatória.
4. Persistir alternativas, bloqueio atual e próxima pergunta antes de criar order draft.
5. Acionar Recovery agent se houver restart durante a escolha ou confirmação.
6. Simular restart e validar que o sistema volta para: pedido bloqueado até endereço escolhido.
7. Pedir a confirmação de Otávio antes de qualquer link de pagamento.

**Métrica de sucesso:**

* Nenhum pedido avança sem a confirmação registrada no checkpoint.
* O `agent_plan` mostra a etapa bloqueada e expira se a conversa mudar.
* Restart simulado retoma a pergunta correta, não um link prematuro.
* Otávio recebe fluxo coerente para resolver: dois endereços possíveis no checkout.

### Cenário 12: Sofia

**Problema:** cliente indecisa pede opinião pessoal.

**Melhoria proposta:** Generator + Evaluator.

**Resultado esperado:** trade-offs claros sem excesso de confiança.

**Passo a passo recomendado:**

1. Definir dimensões de rubrica para a melhoria proposta: Generator + Evaluator.
2. Adicionar critérios específicos para o problema de Sofia: cliente indecisa pede opinião pessoal.
3. Rodar o Evaluator em shadow test contra a resposta atual do KODA.
4. Calibrar score e threshold com revisão humana de engenharia, produto ou suporte.
5. Registrar no manifest score, veredito, dimensão reprovada e instrução de reparo.
6. Ativar canary apenas quando latência, custo e falso bloqueio ficarem dentro do limite.
7. Enviar resposta aprovada que alcance o resultado esperado: trade-offs claros sem excesso de confiança.

**Métrica de sucesso:**

* Revisão humana concorda com o veredito para Sofia acima do threshold definido.
* Falsos positivos e falsos negativos da rubrica são medidos por dimensão.
* Canary mantém latência e custo dentro do limite aceito pelo time.
* A decisão final evita o problema original e entrega: trade-offs claros sem excesso de confiança.

### Cenário 13: Bruno

**Problema:** mensagem curta muda quantidade depois do carrinho.

**Melhoria proposta:** coordination.

**Resultado esperado:** lock evita conflito entre atualizar e fechar.

**Passo a passo recomendado:**

1. Derivar idempotency key da intenção de Bruno, considerando o problema: mensagem curta muda quantidade depois do carrinho.
2. Abrir lock durável por cliente e intenção antes de alterar carrinho ou pedido.
3. Registrar dedup log com evento aceito, evento repetido, sequência e decisão.
4. Processar conflitos mantendo a intenção mais recente sem sobrescrever estado novo.
5. Liberar o lock só depois de persistir estado, manifest e resposta planejada.
6. Testar mensagens simultâneas, duplicadas e fora de ordem para o mesmo cliente.
7. Responder a Bruno com uma única decisão consistente: lock evita conflito entre atualizar e fechar.

**Métrica de sucesso:**

* Zero pedidos duplicados ou carrinhos divergentes em testes simultâneos.
* Dedup log mostra qual evento venceu, qual foi reaproveitado e por quê.
* Lock durável protege retry, fila atrasada e concorrência entre workers.
* Bruno não recebe respostas conflitantes sobre a mesma intenção comercial.

### Cenário 14: Camila

**Problema:** cliente menciona alergia após recomendação inicial.

**Melhoria proposta:** compaction + evaluator.

**Resultado esperado:** nova restrição invalida recomendação anterior.

**Passo a passo recomendado:**

1. Classificar a nova informação de Camila como fato crítico quando ela muda segurança ou recomendação.
2. Salvar fonte e severidade fora da janela 60/20 imediatamente.
3. Rodar Evaluator para invalidar recomendação anterior incompatível.
4. Executar shadow test com restrições que aparecem tarde na conversa.
5. Medir retenção do fato e taxa de reparo da recomendação antiga.
6. Registrar no manifest a recomendação anterior, a restrição nova e o reparo.
7. Responder a Camila pausando a decisão antiga e buscando: nova restrição invalida recomendação anterior.

**Métrica de sucesso:**

* Restrição nova invalida recomendação anterior em todos os testes críticos.
* Resumo crítico mantém a informação ativa fora da janela de histórico bruto.
* Evaluator bloqueia produto incompatível antes de nova sugestão.
* Camila recebe uma recomendação reparada, não continuidade insegura.

### Cenário 15: Diego

**Problema:** pagamento falha e cliente tenta de novo.

**Melhoria proposta:** checkpoint e recovery.

**Resultado esperado:** mesmo order draft é recuperado.

**Passo a passo recomendado:**

1. Criar checkpoint para o ponto em que Diego falha: pagamento falha e cliente tenta de novo.
2. Gerar idempotency key por intenção comercial antes de link, reserva ou retry.
3. Persistir carrinho, order draft, etapa atual e próxima ação antes de efeito externo.
4. Acionar Recovery agent quando houver restart, retry ou retorno sem estado em memória.
5. Comparar checkpoint recuperado com estoque, preço e pedido durável antes de responder.
6. Validar com simulação de restart que o resultado esperado se mantém: mesmo order draft é recuperado.
7. Retomar a conversa com Diego sem pedir de novo dados já confirmados.

**Métrica de sucesso:**

* 100% dos fluxos de Diego têm checkpoint antes do efeito externo relevante.
* Restart simulado recupera carrinho, pedido e etapa sem depender de memória local.
* Idempotency key impede pedido, pagamento ou retry duplicado na mesma intenção.
* Diego retoma o fluxo com o resultado esperado: mesmo order draft é recuperado.

### Cenário 16: Elisa

**Problema:** memória antiga contradiz preferência nova.

**Melhoria proposta:** manifest + memory policy.

**Resultado esperado:** decisão mostra qual fonte venceu.

**Passo a passo recomendado:**

1. Definir no `turn_manifest` os campos necessários para explicar: memória antiga contradiz preferência nova.
2. Registrar fonte, classe do fato, tool calls, versão de política e decisão final.
3. Logar classificação e motivo sem expor dado sensível no artefato de suporte.
4. Criar endpoint de suporte para consultar o turno sem reprocessar logs soltos.
5. Medir tempo de diagnóstico de incidentes antes e depois do manifest.
6. Registrar correção humana quando a classificação ou fonte escolhida estiver errada.
7. Permitir que suporte explique a Elisa como o KODA chegou a: decisão mostra qual fonte venceu.

**Métrica de sucesso:**

* Manifest mostra fonte, classificação e decisão final do turno auditado.
* Suporte diagnostica o incidente em menos de 10 minutos usando o endpoint.
* Campos sensíveis aparecem mascarados ou referenciados por identificador seguro.
* A explicação para Elisa não depende de leitura manual de logs soltos.

### Cenário 17: Felipe

**Problema:** estoque muda entre recomendação e compra.

**Melhoria proposta:** Catalog + Evaluator.

**Resultado esperado:** viabilidade reavaliada antes do link.

**Passo a passo recomendado:**

1. Consultar catálogo e estoque em tempo real para tratar: estoque muda entre recomendação e compra.
2. Validar SKU, variação, preço e disponibilidade antes de aprovar a resposta.
3. Aplicar Evaluator para bloquear troca silenciosa ou compra inviável.
4. Registrar no manifest SKU pedido, SKU validado, fonte de estoque e veredito.
5. Pedir confirmação quando a alternativa não for exatamente o item solicitado.
6. Rechecar estoque antes de criar order draft ou link de pagamento.
7. Responder a Felipe apenas com SKU válido e decisão alinhada a: viabilidade reavaliada antes do link.

**Métrica de sucesso:**

* 100% das respostas auditadas têm SKU validado antes de aprovação.
* Estoque é checado antes da recomendação e rechecado antes do order draft.
* Evaluator rejeita troca silenciosa, item indisponível ou compra inviável.
* Felipe não recebe link nem sugestão final para SKU inválido.

### Cenário 18: Gabriela

**Problema:** orçamento máximo aparece em áudio transcrito.

**Melhoria proposta:** Planner + compaction.

**Resultado esperado:** budget vira fato importante.

**Passo a passo recomendado:**

1. Criar `agent_plan` com stage ligado ao problema de Gabriela: orçamento máximo aparece em áudio transcrito.
2. Classificar o fato extraído como importante ou crítico conforme impacto comercial.
3. Salvar o fato também em resumo durável quando a conversa passar da janela 60/20.
4. Definir `expires_at` para o plano quando objetivo, budget ou restrição mudarem.
5. Medir stage accuracy e retenção do fato em amostra de áudio ou texto longo.
6. Rodar shadow test comparando decisão com e sem plano mais resumo.
7. Responder a Gabriela usando o plano e o fato preservado para obter: budget vira fato importante.

**Métrica de sucesso:**

* `agent_plan` registra stage, intenção e próxima ação sem perder o fato importante.
* Resumo durável preserva o fato quando a conversa sai da janela 60/20.
* Stage accuracy melhora na amostra auditada de conversas longas.
* Gabriela recebe recomendação compatível com o fato informado.

### Cenário 19: Henrique

**Problema:** cliente usa gíria e intenção fica ambígua.

**Melhoria proposta:** Planner leve.

**Resultado esperado:** plano pede confirmação em vez de agir.

**Passo a passo recomendado:**

1. Criar `agent_plan` com stage, intenção e próxima ação para Henrique.
2. Detectar a etapa correta a partir do problema: cliente usa gíria e intenção fica ambígua.
3. Persistir bloqueios, fontes consultadas e validade do plano no turno.
4. Definir `expires_at` para evitar plano velho quando a conversa mudar.
5. Medir stage accuracy contra revisão humana da amostra relevante.
6. Registrar no manifest por que o plano pediu confirmação, pulou etapa ou avançou.
7. Responder a Henrique seguindo o plano até alcançar: plano pede confirmação em vez de agir.

**Métrica de sucesso:**

* Stage correto aparece em pelo menos 85% da amostra auditada.
* Planos vencidos expiram sem travar ou contaminar a próxima intenção.
* Perguntas repetidas e pulos de etapa caem no fluxo observado.
* Henrique recebe resposta compatível com a etapa real da jornada.

### Cenário 20: Isabela

**Problema:** cliente volta 12 horas depois.

**Melhoria proposta:** checkpoint e summary.

**Resultado esperado:** KODA retoma etapa correta.

**Passo a passo recomendado:**

1. Criar checkpoint para o ponto em que Isabela falha: cliente volta 12 horas depois.
2. Gerar idempotency key por intenção comercial antes de link, reserva ou retry.
3. Persistir carrinho, order draft, etapa atual e próxima ação antes de efeito externo.
4. Acionar Recovery agent quando houver restart, retry ou retorno sem estado em memória.
5. Comparar checkpoint recuperado com estoque, preço e pedido durável antes de responder.
6. Validar com simulação de restart que o resultado esperado se mantém: KODA retoma etapa correta.
7. Retomar a conversa com Isabela sem pedir de novo dados já confirmados.

**Métrica de sucesso:**

* 100% dos fluxos de Isabela têm checkpoint antes do efeito externo relevante.
* Restart simulado recupera carrinho, pedido e etapa sem depender de memória local.
* Idempotency key impede pedido, pagamento ou retry duplicado na mesma intenção.
* Isabela retoma o fluxo com o resultado esperado: KODA retoma etapa correta.

### Cenário 21: Júlia

**Problema:** produto premium recomendado fora do budget.

**Melhoria proposta:** rubrica.

**Resultado esperado:** score derruba custo-benefício.

**Passo a passo recomendado:**

1. Definir dimensões de rubrica para a melhoria proposta: rubrica.
2. Adicionar critérios específicos para o problema de Júlia: produto premium recomendado fora do budget.
3. Rodar o Evaluator em shadow test contra a resposta atual do KODA.
4. Calibrar score e threshold com revisão humana de engenharia, produto ou suporte.
5. Registrar no manifest score, veredito, dimensão reprovada e instrução de reparo.
6. Ativar canary apenas quando latência, custo e falso bloqueio ficarem dentro do limite.
7. Enviar resposta aprovada que alcance o resultado esperado: score derruba custo-benefício.

**Métrica de sucesso:**

* Revisão humana concorda com o veredito para Júlia acima do threshold definido.
* Falsos positivos e falsos negativos da rubrica são medidos por dimensão.
* Canary mantém latência e custo dentro do limite aceito pelo time.
* A decisão final evita o problema original e entrega: score derruba custo-benefício.

### Cenário 22: Kleber

**Problema:** cliente pede item fora de catálogo.

**Melhoria proposta:** Catalog + manifest.

**Resultado esperado:** resposta mostra busca sem inventar SKU.

**Passo a passo recomendado:**

1. Consultar catálogo em tempo real para confirmar o caso de Kleber: cliente pede item fora de catálogo.
2. Validar SKU antes de aprovar qualquer resposta ou alternativa.
3. Registrar no manifest termos buscados, filtros, resultado vazio e fonte.
4. Oferecer alternativa só depois de checar categoria compatível e estoque.
5. Rechecar disponibilidade antes de criar order draft para a alternativa.
6. Expor ao suporte a busca feita para diagnosticar incidentes de catálogo.
7. Responder a Kleber sem inventar SKU e com resultado claro: resposta mostra busca sem inventar SKU.

**Métrica de sucesso:**

* Zero respostas inventam SKU para item fora de catálogo.
* Manifest mostra busca, filtros e resultado do catálogo.
* Alternativas oferecidas têm SKU válido e estoque checado.
* Kleber entende o limite do catálogo sem receber promessa falsa.

### Cenário 23: Letícia

**Problema:** restrição médica é informada de forma casual.

**Melhoria proposta:** compactação crítica.

**Resultado esperado:** classificação preserva segurança.

**Passo a passo recomendado:**

1. Classificar o fato central de Letícia por criticidade a partir de: restrição médica é informada de forma casual.
2. Salvar fonte, trecho, timestamp e classe fora da janela 60/20.
3. Rodar compactação em shadow test antes de substituir o contexto ativo.
4. Comparar resposta baseline com resposta que usa `critical_summary`.
5. Medir retenção do fato em conversas longas, ruidosas e com mudança de assunto.
6. Bloquear recomendação ou decisão que contradiga fato crítico preservado.
7. Responder a Letícia mantendo o fato preservado no resultado: classificação preserva segurança.

**Métrica de sucesso:**

* 100% dos fatos críticos da amostra sobrevivem fora da janela 60/20.
* Shadow test mostra retenção maior sem aumento excessivo de tokens.
* Nenhuma restrição crítica é rebaixada para preferência ou ruído.
* Letícia não precisa repetir o fato para receber: classificação preserva segurança.

### Cenário 24: Marcelo

**Problema:** pedido com frete e retirada local.

**Melhoria proposta:** Planner.

**Resultado esperado:** etapa logística separada da etapa de pagamento.

**Passo a passo recomendado:**

1. Criar `agent_plan` com stage, intenção e próxima ação para Marcelo.
2. Detectar a etapa correta a partir do problema: pedido com frete e retirada local.
3. Persistir bloqueios, fontes consultadas e validade do plano no turno.
4. Definir `expires_at` para evitar plano velho quando a conversa mudar.
5. Medir stage accuracy contra revisão humana da amostra relevante.
6. Registrar no manifest por que o plano pediu confirmação, pulou etapa ou avançou.
7. Responder a Marcelo seguindo o plano até alcançar: etapa logística separada da etapa de pagamento.

**Métrica de sucesso:**

* Stage correto aparece em pelo menos 85% da amostra auditada.
* Planos vencidos expiram sem travar ou contaminar a próxima intenção.
* Perguntas repetidas e pulos de etapa caem no fluxo observado.
* Marcelo recebe resposta compatível com a etapa real da jornada.

### Cenário 25: Natália

**Problema:** cliente pergunta por produto visto antes.

**Melhoria proposta:** manifest + shownProducts.

**Resultado esperado:** KODA sabe qual item foi mostrado.

**Passo a passo recomendado:**

1. Definir no `turn_manifest` os campos necessários para explicar: cliente pergunta por produto visto antes.
2. Registrar fonte, classe do fato, tool calls, versão de política e decisão final.
3. Logar classificação e motivo sem expor dado sensível no artefato de suporte.
4. Criar endpoint de suporte para consultar o turno sem reprocessar logs soltos.
5. Medir tempo de diagnóstico de incidentes antes e depois do manifest.
6. Registrar correção humana quando a classificação ou fonte escolhida estiver errada.
7. Permitir que suporte explique a Natália como o KODA chegou a: KODA sabe qual item foi mostrado.

**Métrica de sucesso:**

* Manifest mostra fonte, classificação e decisão final do turno auditado.
* Suporte diagnostica o incidente em menos de 10 minutos usando o endpoint.
* Campos sensíveis aparecem mascarados ou referenciados por identificador seguro.
* A explicação para Natália não depende de leitura manual de logs soltos.

### Cenário 26: Paulo

**Problema:** cliente muda objetivo de emagrecer para hipertrofia.

**Melhoria proposta:** Planner e memory policy.

**Resultado esperado:** plano invalida recomendação anterior.

**Passo a passo recomendado:**

1. Criar `agent_plan` com stage, intenção e próxima ação para Paulo.
2. Detectar a etapa correta a partir do problema: cliente muda objetivo de emagrecer para hipertrofia.
3. Persistir bloqueios, fontes consultadas e validade do plano no turno.
4. Definir `expires_at` para evitar plano velho quando a conversa mudar.
5. Medir stage accuracy contra revisão humana da amostra relevante.
6. Registrar no manifest por que o plano pediu confirmação, pulou etapa ou avançou.
7. Responder a Paulo seguindo o plano até alcançar: plano invalida recomendação anterior.

**Métrica de sucesso:**

* Stage correto aparece em pelo menos 85% da amostra auditada.
* Planos vencidos expiram sem travar ou contaminar a próxima intenção.
* Perguntas repetidas e pulos de etapa caem no fluxo observado.
* Paulo recebe resposta compatível com a etapa real da jornada.

### Cenário 27: Renata

**Problema:** suporte precisa explicar recomendação passada.

**Melhoria proposta:** manifest.

**Resultado esperado:** trace mostra fontes e rubrica.

**Passo a passo recomendado:**

1. Definir no `turn_manifest` os campos necessários para explicar: suporte precisa explicar recomendação passada.
2. Registrar fonte, classe do fato, tool calls, versão de política e decisão final.
3. Logar classificação e motivo sem expor dado sensível no artefato de suporte.
4. Criar endpoint de suporte para consultar o turno sem reprocessar logs soltos.
5. Medir tempo de diagnóstico de incidentes antes e depois do manifest.
6. Registrar correção humana quando a classificação ou fonte escolhida estiver errada.
7. Permitir que suporte explique a Renata como o KODA chegou a: trace mostra fontes e rubrica.

**Métrica de sucesso:**

* Manifest mostra fonte, classificação e decisão final do turno auditado.
* Suporte diagnostica o incidente em menos de 10 minutos usando o endpoint.
* Campos sensíveis aparecem mascarados ou referenciados por identificador seguro.
* A explicação para Renata não depende de leitura manual de logs soltos.

### Cenário 28: Samuel

**Problema:** mensagens chegam fora de ordem.

**Melhoria proposta:** coordination.

**Resultado esperado:** evento antigo não sobrescreve estado novo.

**Passo a passo recomendado:**

1. Derivar idempotency key da intenção de Samuel, considerando o problema: mensagens chegam fora de ordem.
2. Abrir lock durável por cliente e intenção antes de alterar carrinho ou pedido.
3. Registrar dedup log com evento aceito, evento repetido, sequência e decisão.
4. Processar conflitos mantendo a intenção mais recente sem sobrescrever estado novo.
5. Liberar o lock só depois de persistir estado, manifest e resposta planejada.
6. Testar mensagens simultâneas, duplicadas e fora de ordem para o mesmo cliente.
7. Responder a Samuel com uma única decisão consistente: evento antigo não sobrescreve estado novo.

**Métrica de sucesso:**

* Zero pedidos duplicados ou carrinhos divergentes em testes simultâneos.
* Dedup log mostra qual evento venceu, qual foi reaproveitado e por quê.
* Lock durável protege retry, fila atrasada e concorrência entre workers.
* Samuel não recebe respostas conflitantes sobre a mesma intenção comercial.

### Cenário 29: Tatiane

**Problema:** cliente pede comparação honesta.

**Melhoria proposta:** Generator/Evaluator.

**Resultado esperado:** KODA mostra melhor opção e trade-offs.

**Passo a passo recomendado:**

1. Definir dimensões de rubrica para a melhoria proposta: Generator/Evaluator.
2. Adicionar critérios específicos para o problema de Tatiane: cliente pede comparação honesta.
3. Rodar o Evaluator em shadow test contra a resposta atual do KODA.
4. Calibrar score e threshold com revisão humana de engenharia, produto ou suporte.
5. Registrar no manifest score, veredito, dimensão reprovada e instrução de reparo.
6. Ativar canary apenas quando latência, custo e falso bloqueio ficarem dentro do limite.
7. Enviar resposta aprovada que alcance o resultado esperado: KODA mostra melhor opção e trade-offs.

**Métrica de sucesso:**

* Revisão humana concorda com o veredito para Tatiane acima do threshold definido.
* Falsos positivos e falsos negativos da rubrica são medidos por dimensão.
* Canary mantém latência e custo dentro do limite aceito pelo time.
* A decisão final evita o problema original e entrega: KODA mostra melhor opção e trade-offs.

### Cenário 30: Vinícius

**Problema:** cliente tenta comprar item sem estoque.

**Melhoria proposta:** Evaluator.

**Resultado esperado:** pedido bloqueado antes do pagamento.

**Passo a passo recomendado:**

1. Definir dimensões de rubrica para a melhoria proposta: Evaluator.
2. Adicionar critérios específicos para o problema de Vinícius: cliente tenta comprar item sem estoque.
3. Rodar o Evaluator em shadow test contra a resposta atual do KODA.
4. Calibrar score e threshold com revisão humana de engenharia, produto ou suporte.
5. Registrar no manifest score, veredito, dimensão reprovada e instrução de reparo.
6. Ativar canary apenas quando latência, custo e falso bloqueio ficarem dentro do limite.
7. Enviar resposta aprovada que alcance o resultado esperado: pedido bloqueado antes do pagamento.

**Métrica de sucesso:**

* Revisão humana concorda com o veredito para Vinícius acima do threshold definido.
* Falsos positivos e falsos negativos da rubrica são medidos por dimensão.
* Canary mantém latência e custo dentro do limite aceito pelo time.
* A decisão final evita o problema original e entrega: pedido bloqueado antes do pagamento.

---

## 🧱 Modelos de Artefatos Propostos

### `turn_manifest`

**Uso proposto:**

Reconstruir uma decisão do KODA sem depender de leitura manual de logs soltos.

**Campos mínimos:**

* `turn_id`
* `user_id_hash`
* `channel`
* `started_at`
* `agent_route`
* `tools_called`
* `timings`
* `token_cost`
* `decision_summary`
* `artifact_refs`

**Regra de segurança:**

Campos sensíveis devem ser mascarados, resumidos ou referenciados por identificador seguro quando o artefato for usado para debugging.

### `agent_plan`

**Uso proposto:**

Evitar que cada turno reinterprete do zero a etapa da jornada.

**Campos mínimos:**

* `plan_id`
* `turn_id`
* `stage`
* `intent`
* `next_action`
* `blocked_by`
* `expires_at`
* `source_refs`

**Regra de segurança:**

Campos sensíveis devem ser mascarados, resumidos ou referenciados por identificador seguro quando o artefato for usado para debugging.

### `recommendation_evaluation`

**Uso proposto:**

Separar recomendação gerada de recomendação aprovada.

**Campos mínimos:**

* `evaluation_id`
* `candidate_ids`
* `rubric_version`
* `scores`
* `threshold`
* `verdict`
* `repair_instruction`

**Regra de segurança:**

Campos sensíveis devem ser mascarados, resumidos ou referenciados por identificador seguro quando o artefato for usado para debugging.

### `critical_summary`

**Uso proposto:**

Preservar fatos que não podem ser perdidos quando o histórico bruto é truncado.

**Campos mínimos:**

* `conversation_id`
* `critical_facts`
* `important_facts`
* `useful_context`
* `noise_removed`
* `source_message_refs`

**Regra de segurança:**

Campos sensíveis devem ser mascarados, resumidos ou referenciados por identificador seguro quando o artefato for usado para debugging.

### `order_checkpoint`

**Uso proposto:**

Permitir recuperação segura antes e depois de efeitos externos de checkout.

**Campos mínimos:**

* `checkout_id`
* `cart_items`
* `price_snapshot`
* `shipping_snapshot`
* `payment_state`
* `idempotency_key`
* `status`

**Regra de segurança:**

Campos sensíveis devem ser mascarados, resumidos ou referenciados por identificador seguro quando o artefato for usado para debugging.

---

## 🔁 Ciclo BUILD, STABILIZE, SIMPLIFY, REMOVE no KODA

### BUILD

Criar proteção quando há risco conhecido e pouca evidência de produção.

**Aplicações em KODA:**

* Adicionar manifest mínimo.
* Rodar Evaluator em shadow mode.
* Criar checkpoint antes de pagamento.

**Critério para avançar:**

A proteção existe, é reversível e já mede o básico.

### STABILIZE

Medir se a proteção funciona, quanto custa e quantos incidentes evita.

**Aplicações em KODA:**

* Medir taxa de acionamento.
* Medir falsos positivos.
* Revisar amostra humana.

**Critério para avançar:**

A proteção tem 60 dias ou amostra suficiente de dados para decisão.

### SIMPLIFY

Reduzir redundância quando a proteção provou valor mas ficou pesada.

**Aplicações em KODA:**

* Consolidar campos repetidos.
* Reduzir prompts de avaliação.
* Mover checks determinísticos para código.

**Critério para avançar:**

A versão simples mantém proteção essencial com menos custo.

### REMOVE

Desligar componente quando evidência mostra custo maior que valor.

**Aplicações em KODA:**

* Rodar shadow sem componente.
* Usar feature flag.
* Registrar ADR de remoção.

**Critério para avançar:**

A remoção foi testada, documentada e monitorada sem regressão relevante.

---

## 🧾 Rubrica de Priorização

| Critério | Peso | Pergunta | Escala |
|---|---:|---|---|
| Redução de risco crítico | 30% | Evita perda de pedido, recomendação insegura ou duplicidade? | 1 a 5 |
| Base para outras melhorias | 20% | Desbloqueia Planner, Evaluator, checkpoint ou trace? | 1 a 5 |
| Reversibilidade | 15% | Pode ser desligada sem migração dolorosa? | 1 a 5 |
| Custo de implementação | 15% | Cabe em ciclos pequenos? | 1 a 5 invertido |
| Clareza de métrica | 10% | Sabemos medir sucesso? | 1 a 5 |
| Impacto no cliente | 10% | O cliente percebe menos erro ou menos repetição? | 1 a 5 |

### Exemplo de pontuação inicial

| Proposta | Risco | Base | Reversível | Custo | Métrica | Cliente | Leitura |
|---|---:|---:|---:|---:|---:|---:|---|
| Manifest de turno | 4 | 5 | 5 | 4 | 5 | 3 | Começa primeiro |
| Evaluator shadow | 5 | 4 | 5 | 3 | 4 | 5 | Começa junto com manifest |
| Checkpoint comercial | 5 | 4 | 3 | 3 | 5 | 5 | Começa após mapear efeito externo |
| Planner leve | 4 | 4 | 4 | 3 | 4 | 4 | Começa depois de manifest |
| Compaction crítica | 4 | 3 | 4 | 3 | 4 | 4 | Requer suite de conversa longa |

---

## 🧪 Exercícios Práticos

### Exercício 1: Leia um incidente como arquiteto

Pegue um caso de carrinho perdido e classifique se a causa provável é estado, coordenação, contexto, avaliação ou custo invisível.

**Entrega esperada:**

* Uma decisão escrita em até 10 linhas.
* Uma métrica de sucesso.
* Um risco de implementação.
* Um próximo passo reversível.

### Exercício 2: Escreva um manifest mínimo

Defina campos para reconstruir uma recomendação sem expor dados sensíveis.

**Entrega esperada:**

* Uma decisão escrita em até 10 linhas.
* Uma métrica de sucesso.
* Um risco de implementação.
* Um próximo passo reversível.

### Exercício 3: Crie uma rubrica de recomendação

Use quatro dimensões com pesos e threshold de aprovação.

**Entrega esperada:**

* Uma decisão escrita em até 10 linhas.
* Uma métrica de sucesso.
* Um risco de implementação.
* Um próximo passo reversível.

### Exercício 4: Desenhe um checkpoint de checkout

Liste quais dados precisam existir antes de gerar link de pagamento.

**Entrega esperada:**

* Uma decisão escrita em até 10 linhas.
* Uma métrica de sucesso.
* Um risco de implementação.
* Um próximo passo reversível.

### Exercício 5: Planeje um shadow test

Defina baseline, caminho proposto, amostra, métrica e decisão de saída.

**Entrega esperada:**

* Uma decisão escrita em até 10 linhas.
* Uma métrica de sucesso.
* Um risco de implementação.
* Um próximo passo reversível.

### Exercício 6: Calcule ROI de uma proteção

Compare custo mensal com incidentes evitados e falsos positivos.

**Entrega esperada:**

* Uma decisão escrita em até 10 linhas.
* Uma métrica de sucesso.
* Um risco de implementação.
* Um próximo passo reversível.

---

## 🧯 Anti-Padrões a Evitar

### Chamar proposta de produção

Dizer que Planner, Evaluator ou manifest completo já existem quando são propostas distorce a decisão.

**Correção:**

Defina contrato, métrica, dono e ciclo de revisão antes de promover a mudança.

### Adicionar agente sem contrato

Mais agentes sem artefatos auditáveis aumentam confusão.

**Correção:**

Defina contrato, métrica, dono e ciclo de revisão antes de promover a mudança.

### Medir só latência

Latência é importante, mas qualidade, custo, ROI e incidentes também importam.

**Correção:**

Defina contrato, métrica, dono e ciclo de revisão antes de promover a mudança.

### Usar compactação sem criticidade

Resumo genérico pode apagar exatamente o fato que deveria proteger.

**Correção:**

Defina contrato, métrica, dono e ciclo de revisão antes de promover a mudança.

### Confiar em lock em memória para pedido

Memória local é útil para cache, não para coordenação comercial crítica.

**Correção:**

Defina contrato, métrica, dono e ciclo de revisão antes de promover a mudança.

### Criar guard sem data de revisão

Proteção sem revisão vira peso arquitetural.

**Correção:**

Defina contrato, métrica, dono e ciclo de revisão antes de promover a mudança.

### Rejeitar fail-open e fail-closed como dogmas

Cada fluxo precisa de política própria. Recomendações podem fail-closed, extração de memória pode fail-open.

**Correção:**

Defina contrato, métrica, dono e ciclo de revisão antes de promover a mudança.

---

## 🧩 Como Comunicar para Cada Público

### Engenharia

Falar em contratos, checkpoints, idempotência, trace e rollback.

**Mensagem curta sugerida:**

Estamos propondo melhorias de harness para tornar o KODA mais auditável, mais seguro em decisões comerciais e mais fácil de evoluir com métricas claras.

### Produto

Falar em menos repetição, mais confiança, menos incidentes e melhor recomendação.

**Mensagem curta sugerida:**

Estamos propondo melhorias de harness para tornar o KODA mais auditável, mais seguro em decisões comerciais e mais fácil de evoluir com métricas claras.

### Suporte

Falar em manifest consultável e explicação rápida de decisões passadas.

**Mensagem curta sugerida:**

Estamos propondo melhorias de harness para tornar o KODA mais auditável, mais seguro em decisões comerciais e mais fácil de evoluir com métricas claras.

### Liderança

Falar em risco reduzido, custo visível, ROI e roadmap incremental.

**Mensagem curta sugerida:**

Estamos propondo melhorias de harness para tornar o KODA mais auditável, mais seguro em decisões comerciais e mais fácil de evoluir com métricas claras.

### Dados e analytics

Falar em eventos padronizados, amostras, comparação e cohorts.

**Mensagem curta sugerida:**

Estamos propondo melhorias de harness para tornar o KODA mais auditável, mais seguro em decisões comerciais e mais fácil de evoluir com métricas claras.

---

## 🧠 KODA Application: Walkthrough Completo de Uma Melhoria

### 00:00

Cliente pergunta por whey sem lactose até R$ 220.

### 00:01

Ingress registra evento e idempotency key.

### 00:02

State loader recupera perfil, histórico recente, memórias e resumo crítico.

### 00:03

Planner proposto define etapa como recomendação, não checkout.

### 00:04

Catalog tool busca candidatos compatíveis.

### 00:05

Generator cria opções com trade-offs.

### 00:06

Evaluator shadow pontua adequação, custo-benefício, satisfação e viabilidade.

### 00:07

Manifest registra candidatos, tools, scores, timings e custo.

### 00:08

KODA envia resposta atual se shadow ainda não estiver ativo.

### 00:09

Revisão humana compara resposta enviada com resposta proposta.

### 00:10

Métrica semanal decide se a rubrica está pronta para canary.

### Resultado esperado do walkthrough

* O cliente recebe recomendação mais confiável quando a melhoria for ativada.
* O time consegue explicar por que a recomendação venceu.
* O custo adicional é visível antes de virar padrão.
* A melhoria pode ser pausada se a rubrica gerar falsos positivos.

---

## 🧾 Checklist Final de Prontidão

* [ ] O documento de proposta separa fatos atuais de arquitetura proposta.
* [ ] Cada melhoria tem dono técnico.
* [ ] Cada melhoria tem métrica principal.
* [ ] Cada melhoria tem métrica de segurança.
* [ ] Cada melhoria tem modo de uso inicial reversível.
* [ ] Cada melhoria tem critério de rollback.
* [ ] Mudanças com impacto arquitetural têm ADR.
* [ ] Dados sensíveis em traces e manifests são protegidos.
* [ ] Suporte sabe consultar evidência quando houver incidente.
* [ ] Produto entende trade-off de latência e qualidade.
* [ ] Liderança entende custo e ROI.
* [ ] Existe data de revisão após STABILIZE.

---

## 🧭 O Que Voce Aprendeu

* KODA já tem uma base forte de produção, mas ainda precisa de harness governado.
* Single agent com tools não é o mesmo que decomposição real com Planner, Generator e Evaluator.
* Histórico 60/20 ajuda, mas não substitui compactação crítica em conversas longas.
* Trace operacional mostra tempo, mas manifest de decisão mostra causa.
* Carrinho, pedido e pagamento precisam de checkpoint antes de efeitos externos.
* Coordenação crítica não deve depender de memória local.
* Evaluator com rubrica reduz o risco de self-evaluation collapse.
* Roadmap bom começa com observabilidade e shadow test antes de mudar comportamento.
* Métricas de custo, ROI e falsos positivos evitam harness pesado demais.
* O ciclo BUILD, STABILIZE, SIMPLIFY, REMOVE transforma proteção em disciplina evolutiva.

---

## 🏁 Fechamento: A Decisão Madura

No fim da semana, Fernando voltou ao quadro branco.

A frase inicial ainda estava lá:

```text
KODA tem harness.
KODA precisa de harness governado.
```

Agora o time tinha algo melhor que ansiedade arquitetural.

Tinha prioridades.

Tinha métricas.

Tinha roadmap.

Tinha um jeito de testar sem colocar cliente em risco.

Tinha uma linguagem comum para falar com suporte, produto, liderança e engenharia.

A melhoria mais importante não era adicionar mais um agente imediatamente.

Era criar evidência para saber qual agente, qual checkpoint, qual manifest e qual rubrica realmente reduzem risco.

Essa é a maturidade do Nível 4.

Não é apenas saber construir harness.

É saber melhorar o harness certo, na ordem certa, com a prova certa.

Quando KODA chega nesse ponto, cada conversa longa deixa de ser uma aposta na memória do modelo.

Ela vira um workflow auditável, recuperável, mensurável e evolutivo.

Esse é o objetivo.
---

## 📚 Anexo: Cartões de Implementação por Semana

### Cartão 1: Manifest em KODA

**Foco:** auditoria de decisão.

**Quando usar:**

* Quando uma conversa real expõe risco ligado a este tema.
* Quando a proposta pode ser testada sem afetar cada usuário.
* Quando a métrica de sucesso pode ser observada em uma semana.

**Passos práticos:**

1. Escolher uma amostra de conversas KODA relevantes.
2. Definir a hipótese de melhoria em uma frase.
3. Rodar a mudança em observação ou shadow quando possível.
4. Medir qualidade, custo, latência e auditabilidade.
5. Registrar decisão curta com evidência.
6. Decidir continuar, ajustar, pausar ou simplificar.

**Sinal de sucesso:**

O time consegue explicar a decisão com dados e não apenas com sensação de que a arquitetura ficou melhor.

**Sinal de alerta:**

A melhoria aumenta componentes, latência ou custo sem mostrar queda mensurável de risco.

### Cartão 2: Evaluator em KODA

**Foco:** qualidade da recomendação.

**Quando usar:**

* Quando uma conversa real expõe risco ligado a este tema.
* Quando a proposta pode ser testada sem afetar cada usuário.
* Quando a métrica de sucesso pode ser observada em uma semana.

**Passos práticos:**

1. Escolher uma amostra de conversas KODA relevantes.
2. Definir a hipótese de melhoria em uma frase.
3. Rodar a mudança em observação ou shadow quando possível.
4. Medir qualidade, custo, latência e auditabilidade.
5. Registrar decisão curta com evidência.
6. Decidir continuar, ajustar, pausar ou simplificar.

**Sinal de sucesso:**

O time consegue explicar a decisão com dados e não apenas com sensação de que a arquitetura ficou melhor.

**Sinal de alerta:**

A melhoria aumenta componentes, latência ou custo sem mostrar queda mensurável de risco.

### Cartão 3: Planner em KODA

**Foco:** clareza de etapa.

**Quando usar:**

* Quando uma conversa real expõe risco ligado a este tema.
* Quando a proposta pode ser testada sem afetar cada usuário.
* Quando a métrica de sucesso pode ser observada em uma semana.

**Passos práticos:**

1. Escolher uma amostra de conversas KODA relevantes.
2. Definir a hipótese de melhoria em uma frase.
3. Rodar a mudança em observação ou shadow quando possível.
4. Medir qualidade, custo, latência e auditabilidade.
5. Registrar decisão curta com evidência.
6. Decidir continuar, ajustar, pausar ou simplificar.

**Sinal de sucesso:**

O time consegue explicar a decisão com dados e não apenas com sensação de que a arquitetura ficou melhor.

**Sinal de alerta:**

A melhoria aumenta componentes, latência ou custo sem mostrar queda mensurável de risco.

### Cartão 4: Compaction em KODA

**Foco:** memória longa segura.

**Quando usar:**

* Quando uma conversa real expõe risco ligado a este tema.
* Quando a proposta pode ser testada sem afetar cada usuário.
* Quando a métrica de sucesso pode ser observada em uma semana.

**Passos práticos:**

1. Escolher uma amostra de conversas KODA relevantes.
2. Definir a hipótese de melhoria em uma frase.
3. Rodar a mudança em observação ou shadow quando possível.
4. Medir qualidade, custo, latência e auditabilidade.
5. Registrar decisão curta com evidência.
6. Decidir continuar, ajustar, pausar ou simplificar.

**Sinal de sucesso:**

O time consegue explicar a decisão com dados e não apenas com sensação de que a arquitetura ficou melhor.

**Sinal de alerta:**

A melhoria aumenta componentes, latência ou custo sem mostrar queda mensurável de risco.

### Cartão 5: Checkpoint em KODA

**Foco:** recuperação de checkout.

**Quando usar:**

* Quando uma conversa real expõe risco ligado a este tema.
* Quando a proposta pode ser testada sem afetar cada usuário.
* Quando a métrica de sucesso pode ser observada em uma semana.

**Passos práticos:**

1. Escolher uma amostra de conversas KODA relevantes.
2. Definir a hipótese de melhoria em uma frase.
3. Rodar a mudança em observação ou shadow quando possível.
4. Medir qualidade, custo, latência e auditabilidade.
5. Registrar decisão curta com evidência.
6. Decidir continuar, ajustar, pausar ou simplificar.

**Sinal de sucesso:**

O time consegue explicar a decisão com dados e não apenas com sensação de que a arquitetura ficou melhor.

**Sinal de alerta:**

A melhoria aumenta componentes, latência ou custo sem mostrar queda mensurável de risco.

### Cartão 6: Coordination em KODA

**Foco:** concorrência e idempotência.

**Quando usar:**

* Quando uma conversa real expõe risco ligado a este tema.
* Quando a proposta pode ser testada sem afetar cada usuário.
* Quando a métrica de sucesso pode ser observada em uma semana.

**Passos práticos:**

1. Escolher uma amostra de conversas KODA relevantes.
2. Definir a hipótese de melhoria em uma frase.
3. Rodar a mudança em observação ou shadow quando possível.
4. Medir qualidade, custo, latência e auditabilidade.
5. Registrar decisão curta com evidência.
6. Decidir continuar, ajustar, pausar ou simplificar.

**Sinal de sucesso:**

O time consegue explicar a decisão com dados e não apenas com sensação de que a arquitetura ficou melhor.

**Sinal de alerta:**

A melhoria aumenta componentes, latência ou custo sem mostrar queda mensurável de risco.

### Cartão 7: ROI em KODA

**Foco:** governança de custo.

**Quando usar:**

* Quando uma conversa real expõe risco ligado a este tema.
* Quando a proposta pode ser testada sem afetar cada usuário.
* Quando a métrica de sucesso pode ser observada em uma semana.

**Passos práticos:**

1. Escolher uma amostra de conversas KODA relevantes.
2. Definir a hipótese de melhoria em uma frase.
3. Rodar a mudança em observação ou shadow quando possível.
4. Medir qualidade, custo, latência e auditabilidade.
5. Registrar decisão curta com evidência.
6. Decidir continuar, ajustar, pausar ou simplificar.

**Sinal de sucesso:**

O time consegue explicar a decisão com dados e não apenas com sensação de que a arquitetura ficou melhor.

**Sinal de alerta:**

A melhoria aumenta componentes, latência ou custo sem mostrar queda mensurável de risco.

### Cartão 8: ADR em KODA

**Foco:** decisão arquitetural registrada.

**Quando usar:**

* Quando uma conversa real expõe risco ligado a este tema.
* Quando a proposta pode ser testada sem afetar cada usuário.
* Quando a métrica de sucesso pode ser observada em uma semana.

**Passos práticos:**

1. Escolher uma amostra de conversas KODA relevantes.
2. Definir a hipótese de melhoria em uma frase.
3. Rodar a mudança em observação ou shadow quando possível.
4. Medir qualidade, custo, latência e auditabilidade.
5. Registrar decisão curta com evidência.
6. Decidir continuar, ajustar, pausar ou simplificar.

**Sinal de sucesso:**

O time consegue explicar a decisão com dados e não apenas com sensação de que a arquitetura ficou melhor.

**Sinal de alerta:**

A melhoria aumenta componentes, latência ou custo sem mostrar queda mensurável de risco.

### Cartão 9: Manifest em STABILIZE

**Foco:** medir se a auditoria de decisão virou rotina confiável.

**Quando usar:**

* Quando o manifest já cobre a maior parte dos turnos comerciais.
* Quando suporte começou a usar o artefato em incidentes reais.
* Quando o custo de storage e consulta já aparece no painel semanal.

**Passos práticos:**

1. Medir cobertura de manifest por tipo de turno, canal e agente.
2. Separar incidentes diagnosticados com manifest de incidentes que ainda exigiram log manual.
3. Revisar campos vazios, dados sensíveis mascarados e falhas de schema.
4. Comparar tempo de diagnóstico antes e depois do endpoint de suporte.
5. Marcar campos raramente usados como candidatos a SIMPLIFY.
6. Registrar evidência em ADR de estabilização ou ajuste.

**Sinal de sucesso:**

Suporte explica decisões comerciais recorrentes pelo manifest, com menor tempo de diagnóstico e sem vazamento de dados sensíveis.

**Sinal de alerta:**

O manifest cresce em campos e storage, mas os incidentes continuam exigindo leitura manual de logs.

### Cartão 10: Evaluator em STABILIZE

**Foco:** provar que a rubrica melhora qualidade sem custo descontrolado.

**Quando usar:**

* Quando o Evaluator saiu de shadow test para canary controlado.
* Quando há amostra humana suficiente para medir concordância.
* Quando latência e custo por avaliação já são visíveis.

**Passos práticos:**

1. Medir aprovação, rejeição, repair e falso positivo por dimensão da rubrica.
2. Comparar recomendações com e sem Evaluator em grupo controle.
3. Revisar semanalmente divergências entre Evaluator e revisão humana.
4. Ajustar pesos só quando a amostra mostrar erro consistente.
5. Identificar dimensões redundantes para SIMPLIFY.
6. Definir gatilho de REMOVE para dimensões sem impacto por ciclo completo.

**Sinal de sucesso:**

A rubrica reduz recomendações inadequadas sem ultrapassar o limite de latência, custo ou falso bloqueio definido pelo time.

**Sinal de alerta:**

O Evaluator rejeita muito, explica pouco ou aumenta latência sem melhorar a revisão humana.

### Cartão 11: Planner em SIMPLIFY

**Foco:** manter clareza de etapa sem transformar plano em burocracia.

**Quando usar:**

* Quando `agent_plan` já está ativo em recompras, checkout ou jornadas ambíguas.
* Quando algumas etapas têm baixo uso ou baixa precisão.
* Quando o time consegue medir stage accuracy por amostra.

**Passos práticos:**

1. Medir acerto de stage por tipo de conversa e por transição de jornada.
2. Listar campos do `agent_plan` que raramente mudam a decisão do turno.
3. Encerrar stages duplicados que produzem a mesma próxima ação.
4. Ajustar `expires_at` para reduzir planos velhos que travam conversa.
5. Rodar shadow test com schema menor antes de remover campo.
6. Registrar no ADR quais campos ficaram, quais saíram e por quê.

**Sinal de sucesso:**

O plano fica menor e mais previsível, mantendo ou elevando acerto de etapa e reduzindo perguntas repetidas.

**Sinal de alerta:**

A simplificação remove contexto que evitava pulo de etapa ou ação sem confirmação.

### Cartão 12: Compaction em SIMPLIFY

**Foco:** preservar fatos críticos com menos tokens e menos resumo desnecessário.

**Quando usar:**

* Quando compactação crítica já preserva restrições em conversas longas.
* Quando custo de tokens ou storage começa a subir sem ganho proporcional.
* Quando classes de criticidade têm baixa diferença prática.

**Passos práticos:**

1. Medir retenção de fatos críticos fora da janela 60/20.
2. Comparar tokens do contexto antes e depois de cada política de resumo.
3. Separar fatos críticos, importantes e ruído por taxa real de uso em decisão.
4. Testar schema de resumo menor em shadow test com conversas longas.
5. Remover categorias que não mudam recomendação, segurança ou suporte.
6. Registrar evidência de retenção e economia antes de ampliar a simplificação.

**Sinal de sucesso:**

O contexto fica mais barato e curto sem perder restrições, alergias, orçamento ou decisões comerciais relevantes.

**Sinal de alerta:**

A redução de resumo economiza tokens, mas volta a causar esquecimento de fatos críticos.

### Cartão 13: Checkpoint em REMOVE

**Foco:** saber quando um checkpoint extra deixou de proteger risco real.

**Quando usar:**

* Quando checkpoints comerciais já estão estáveis em checkout e pagamento.
* Quando um checkpoint específico quase nunca é usado na recuperação.
* Quando outro estado durável passou a cobrir a mesma falha com evidência.

**Passos práticos:**

1. Medir taxa de criação, recuperação real e recuperação falsa por tipo de checkpoint.
2. Simular restart sem o checkpoint candidato usando replay ou shadow test.
3. Comparar perdas de carrinho, duplicidade e tempo de recuperação com e sem ele.
4. Manter feature flag para desligamento gradual por grupo de baixo risco.
5. Definir rollback se qualquer métrica de recuperação piorar.
6. Registrar ADR de remoção com evidência, janela observada e plano de volta.

**Sinal de sucesso:**

O checkpoint removido não aumenta perda de carrinho, duplicidade, retry de pagamento ou tempo de recuperação.

**Sinal de alerta:**

A taxa de uso parece baixa porque o incidente é raro, mas o impacto do único caso ainda é alto.

### Cartão 14: Coordination em REMOVE

**Foco:** remover locks ou dedup redundantes sem reabrir corrida comercial.

**Quando usar:**

* Quando locks duráveis e idempotency keys já têm métricas por intenção.
* Quando duas camadas de dedup registram sempre a mesma decisão.
* Quando testes simultâneos cobrem mensagens duplicadas, atrasadas e fora de ordem.

**Passos práticos:**

1. Medir conflitos reais, lock timeout, dedup hit e evento reaproveitado por semana.
2. Identificar camada de coordenação que nunca decide diferente da camada anterior.
3. Rodar teste simultâneo com a camada candidata desligada em ambiente controlado.
4. Validar que pedidos duplicados, carrinho antigo e evento fora de ordem continuam bloqueados.
5. Desligar por feature flag em canary pequeno e observar métricas de corrida.
6. Registrar ADR de remoção ou manter a camada se o risco voltar a aparecer.

**Sinal de sucesso:**

A remoção reduz custo ou complexidade sem criar pedido duplicado, overwrite de estado ou resposta fora de ordem.

**Sinal de alerta:**

A camada parecia redundante em média, mas era a única proteção em retry, atraso de fila ou restart.
