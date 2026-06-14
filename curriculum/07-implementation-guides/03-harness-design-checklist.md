---
title: "Checklist de Design de Harness para Agentes Confiáveis"
type: curriculum-guide
aliases: ["checklist harness", "design checklist", "harness design", "guia implementacao"]
tags: [curriculo-conteudo, guia-implementacao, harness, auditoria, qualidade, seguranca, guardrails, persistencia-de-estado, coordenacao-multi-agente, observabilidade]
relates-to: ["[[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]", "[[docs/canonical/stable-harness-prompt|Stable Harness Prompt]]", "[[docs/canonical/error-context-hygiene|Error Context Hygiene]]", "[[docs/canonical/deterministic-tool-dispatch|Deterministic Tool Dispatch]]"]
last_updated: 2026-06-10
---
# 🧪 Checklist de Design de Harness para Agentes Confiáveis
## Como Avaliar Contexto, Contratos, Avaliação, Persistência, Coordenação, Segurança, Evolução e Observabilidade em Sistemas Long-Running

**Tempo Estimado:** 4-6 horas para leitura completa; 2-3 horas por auditoria aplicada  
**Nível:** Guia de Implementação - Integração dos Níveis 1, 2 e 3  
**Pré-requisito:** Ter lido `../01-nivel-1-fundamentals/03-basic-harness-patterns.md`, `../02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md` e `../03-nivel-3-advanced-architecture/05-harness-evolution.md`  
**Status:** 🟢 CRÍTICO - Checklist operacional para revisão de harness antes de produção  
**Data de Criação:** Maio 2026  

---

## 📖 Prólogo: A Reunião em que Fernando Parou o Deploy

Quinta-feira, 18h42.

O time KODA estava a dezoito minutos de liberar uma nova versão do agente de WhatsApp.

A feature parecia simples no resumo executivo: melhorar recomendações de suplementos para clientes recorrentes.

O pull request tinha passado em lint.

Os testes unitários estavam verdes.

O demo para produto tinha sido bonito.

E mesmo assim Fernando Machado pediu para parar.

Não foi uma decisão dramática.

Foi o tipo de pausa que um tech lead experiente faz quando algo parece bom demais para ser verdade.

Ele abriu o trace de uma conversa longa.

Uma cliente chamada Renata tinha conversado com KODA por quase duas horas.

No começo, ela disse que tinha intolerância à lactose.

No meio, comparou preços de whey, creatina e colágeno.

No fim, pediu uma recomendação rápida para fechar a compra antes do treino.

O agente respondeu com confiança, tom humano e ótima formatação.

Mas recomendou um produto com lactose.

O demo não tinha mostrado isso.

O teste unitário não tinha mostrado isso.

O prompt parecia correto.

O modelo parecia inteligente.

A falha estava no harness.

Fernando escreveu oito perguntas no quadro branco.

Elas não eram perguntas sobre modelo.

Eram perguntas sobre engenharia.

Quem decidiu o que fica no contexto?

Onde a restrição de lactose deveria morar: context window, state ou summary?

Qual contrato o Product Discovery prometeu cumprir?

Quem avaliou a recomendação e com qual rubrica?

O estado poderia ser recuperado se o worker caísse?

Dois agentes poderiam alterar o carrinho ao mesmo tempo?

Qual guardrail impediria uma recomendação clinicamente inadequada?

Como o time provaria, depois do incidente, onde a decisão errada entrou?

O silêncio da sala respondeu antes das pessoas.

O sistema tinha componentes bons.

Mas não tinha uma checklist completa de harness.

Tinha pedaços de validação.

Tinha boas intenções.

Tinha logs.

Tinha prompts longos.

Mas não tinha uma forma objetiva de dizer: este harness está pronto para produção.

Esse é o objetivo deste guia.

Você não vai aprender apenas a perguntar se um harness parece bom.

Você vai aprender a verificar se ele cumpre critérios objetivos.

Você vai olhar para contexto, contratos, avaliação, persistência, coordenação, segurança, evolução e observabilidade.

Você vai sair com uma ferramenta prática para revisar KODA, revisar qualquer agente long-running e defender decisões arquiteturais com evidência.

Porque em produção, “parece inteligente” não é suficiente.

Em produção, o harness precisa provar que protege o cliente quando a conversa fica longa, quando o estado fica complexo e quando o modelo está confiante demais.

> **Regra de Fernando:** se você não consegue auditar uma decisão do agente depois do fato, você ainda não tem um harness; você tem uma aposta.

---

## 🎯 O Que Você Vai Aprender

- ✅ Aplicar uma checklist objetiva para avaliar qualidade de harness antes de produção.
- ✅ Distinguir o que pertence à context window, ao state persistente e ao summary comprimido.
- ✅ Escrever e revisar sprint contracts com inputs, outputs, failure handling e versionamento.
- ✅ Desenhar rubrics com pesos, thresholds, blockers e evidência auditável.
- ✅ Avaliar checkpointing, recovery, replayability e escolha entre database e files.
- ✅ Diagnosticar riscos de multi-agent coordination, incluindo lock files, status files e race conditions.
- ✅ Verificar guardrails de input, output, constraints, fallback, budget e formato.
- ✅ Usar o ciclo BUILD/STABILIZE/SIMPLIFY/REMOVE para evoluir harness sem acumular complexidade.
- ✅ Ler traces e exigir observabilidade suficiente para debug, auditoria e melhoria contínua.
- ✅ Aplicar tudo isso ao agente WhatsApp do KODA em um cenário real de vendas de suplementos.

---

## 🧭 Como Usar Esta Checklist

Use este documento em revisões de arquitetura, PR reviews de features críticas, incident reviews e readiness reviews antes de produção.

Não use como checklist estética.

O objetivo não é perguntar “o design está bonito?”.

O objetivo é perguntar “o design tem evidência suficiente para proteger cliente, negócio e time?”.

Cada categoria tem explicação, sinais de bom harness, tabela PASS/FAIL, evidências esperadas e perguntas de auditoria.
Os termos técnicos aparecem no vocabulário usado pelo time: context window, token budgeting, sprint contract, versioning, fallback handler, checkpoint, race condition e trace reading.

Para cada item, marque PASS apenas quando houver artefato verificável.

Se a resposta for “o agente normalmente faz isso”, marque FAIL até existir contrato, teste, trace ou validação objetiva.

Quando um item falhar, registre impacto e dono.

Nem todo harness precisa nota 100 desde o primeiro dia.

Mas todo harness precisa saber quais riscos está aceitando.

### Escala recomendada de aplicação

| Momento | Profundidade | Quem participa | Resultado esperado |
|---------|--------------|----------------|--------------------|
| Design inicial | Completa | Tech lead, dev responsável, produto | Lista de riscos antes da implementação |
| PR review | Focada nos itens alterados | Revisor técnico e autor | Evidência de que a mudança não quebra contratos |
| Pré-produção | Completa | Engenharia, suporte, operações | Go/no-go com critérios objetivos |
| Pós-incidente | Categorias afetadas | Time do incidente | Causa raiz ligada a falha de harness |
| Revisão trimestral | Evolução e observabilidade | Arquitetura e liderança | Decisões de simplificar, manter ou remover |

---

## 🏗️ Arquitetura de Referência: Harness Completo

Um harness completo não é uma camada única. É uma sequência de fronteiras verificáveis ao redor do modelo. O modelo continua sendo importante, mas ele não é obrigado a carregar sozinho memória, contratos, avaliação, recuperação, coordenação e auditoria.

```text
┌────────────────────────────────────────────────────────────────────────────────────┐
│                          MUNDO REAL / CANAIS DE ENTRADA                           │
│        WhatsApp, painel interno, webhooks, catálogo, pagamentos, fulfillment       │
└──────────────────────────────────────────┬─────────────────────────────────────────┘
                                           │
                                           ▼
┌────────────────────────────────────────────────────────────────────────────────────┐
│  1. INPUT VALIDATION & NORMALIZATION                                               │
│  ├─ schema check              ├─ limite de tamanho        ├─ prompt injection guard │
│  └─ normalização de intent    └─ correlation_id           └─ canal e permissões     │
└──────────────────────────────────────────┬─────────────────────────────────────────┘
                                           │
                                           ▼
┌────────────────────────────────────────────────────────────────────────────────────┐
│  2. CONTEXT MANAGEMENT                                                             │
│  ├─ token budget             ├─ history windowing          ├─ compacted summary     │
│  ├─ critical state           ├─ retrieved knowledge        └─ context audit map     │
└──────────────────────────────────────────┬─────────────────────────────────────────┘
                                           │
                                           ▼
┌────────────────────────────────────────────────────────────────────────────────────┐
│  3. SPRINT CONTRACT / PLAN                                                         │
│  ├─ explicit inputs         ├─ success criteria            ├─ failure handling      │
│  ├─ interface boundary      ├─ schema_version              └─ owner e audit refs    │
└──────────────────────────────────────────┬─────────────────────────────────────────┘
                                           │
                                           ▼
┌────────────────────────────────────────────────────────────────────────────────────┐
│  4. MULTI-AGENT EXECUTION                                                          │
│                                                                                    │
│   ┌──────────────┐      ┌────────────────┐      ┌────────────────┐                │
│   │  Planner     │─────▶│   Generator    │─────▶│   Evaluator    │                │
│   │  plan.json   │      │ generation.json│      │ evaluation.json│                │
│   └──────┬───────┘      └───────┬────────┘      └───────┬────────┘                │
│          │                      │                       │                         │
│          ▼                      ▼                       ▼                         │
│   ┌──────────────────────────────────────────────────────────────────────────┐     │
│   │ Coordination Bus: lock files, status files, JSON protocol, atomic writes │     │
│   └──────────────────────────────────────────────────────────────────────────┘     │
└──────────────────────────────────────────┬─────────────────────────────────────────┘
                                           │
                                           ▼
┌────────────────────────────────────────────────────────────────────────────────────┐
│  5. GUARDRAILS & VALIDATION                                                        │
│  ├─ format validator       ├─ constraint checker          ├─ budget guard          │
│  ├─ safety policy          ├─ fallback handler            └─ irreversible action   │
└──────────────────────────────────────────┬─────────────────────────────────────────┘
                                           │
                                           ▼
┌────────────────────────────────────────────────────────────────────────────────────┐
│  6. STATE PERSISTENCE & RECOVERY                                                   │
│  ├─ checkpoints            ├─ state schema                ├─ replay artifacts      │
│  ├─ file/database backend  ├─ retention policy            └─ restore procedure     │
└──────────────────────────────────────────┬─────────────────────────────────────────┘
                                           │
                                           ▼
┌────────────────────────────────────────────────────────────────────────────────────┐
│  7. OBSERVABILITY                                                                  │
│  ├─ trace reading          ├─ audit logs                 ├─ dashboards             │
│  ├─ alerting               ├─ debugging surfaces          └─ incident evidence     │
└──────────────────────────────────────────┬─────────────────────────────────────────┘
                                           │
                                           ▼
┌────────────────────────────────────────────────────────────────────────────────────┐
│  8. OUTPUT / ACTION                                                                │
│        resposta WhatsApp, pedido aprovado, pagamento gerado, fulfillment liberado  │
└────────────────────────────────────────────────────────────────────────────────────┘
```

A checklist a seguir percorre essa arquitetura camada por camada.

---

## 📊 Scorecard de Maturidade do Harness

Use este scorecard para resumir a maturidade do harness depois de aplicar as categorias. A pontuação não substitui a análise. Ela ajuda a comparar evolução ao longo do tempo.

| Dimensão | Nível 1 - Ad hoc | Nível 2 - Básico | Nível 3 - Operacional | Nível 4 - Robusto | Nível 5 - Excelente | Score |
|----------|------------------|------------------|------------------------|-------------------|----------------------|-------|
| Contexto (Context Management) | Depende de prompt e memória implícita | Tem algumas regras manuais | Possui contratos e validações principais | É testado, auditável e recuperável | Mede qualidade, custo e evolução continuamente | 1-5 |
| Contratos (Contracts/Sprint Contracts) | Depende de prompt e memória implícita | Tem algumas regras manuais | Possui contratos e validações principais | É testado, auditável e recuperável | Mede qualidade, custo e evolução continuamente | 1-5 |
| Avaliação (Evaluation/Rubrics) | Depende de prompt e memória implícita | Tem algumas regras manuais | Possui contratos e validações principais | É testado, auditável e recuperável | Mede qualidade, custo e evolução continuamente | 1-5 |
| Persistência (State Persistence) | Depende de prompt e memória implícita | Tem algumas regras manuais | Possui contratos e validações principais | É testado, auditável e recuperável | Mede qualidade, custo e evolução continuamente | 1-5 |
| Coordenação (Multi-Agent Coordination) | Depende de prompt e memória implícita | Tem algumas regras manuais | Possui contratos e validações principais | É testado, auditável e recuperável | Mede qualidade, custo e evolução continuamente | 1-5 |
| Segurança & Guardrails | Depende de prompt e memória implícita | Tem algumas regras manuais | Possui contratos e validações principais | É testado, auditável e recuperável | Mede qualidade, custo e evolução continuamente | 1-5 |
| Evolução (Harness Evolution) | Depende de prompt e memória implícita | Tem algumas regras manuais | Possui contratos e validações principais | É testado, auditável e recuperável | Mede qualidade, custo e evolução continuamente | 1-5 |
| Observabilidade (Traces/Monitoring) | Depende de prompt e memória implícita | Tem algumas regras manuais | Possui contratos e validações principais | É testado, auditável e recuperável | Mede qualidade, custo e evolução continuamente | 1-5 |
| Decisão de Valor (Value Gate) | Toda intenção vira Build por padrão | Existe intenção de questionar valor, mas informal | Há um gate com vocabulário (Build/Experiment/Defer/Stop) e owner nomeado | Gate é aplicado consistentemente, decisões são auditadas | O gate é calibrado com outcomes, o Owner-of-No é um papel institucionalizado | 1-5 |

### Interpretação da pontuação

- **9-17 pontos:** harness experimental. Use apenas em demo, protótipo ou fluxo sem risco comercial.
- **18-27 pontos:** harness inicial. Pode rodar com supervisão humana e baixa autonomia.
- **28-36 pontos:** harness operacional. Aceitável para produção limitada com monitoramento ativo.
- **37-43 pontos:** harness robusto. Adequado para produção em escala com incident response definido.
- **44-45 pontos:** harness excelente. Além de confiável, é evolutivo, auditável e ensina o time a melhorar.

### Regra de bloqueio

Mesmo com score alto, qualquer FAIL crítico em Segurança, Persistência ou Avaliação pode bloquear produção. Score agregado nunca deve esconder risco absoluto.

---

## 🚦 0. Decisão de Valor (Value Decision Gate)

Esta categoria é nova e não existia na checklist original do Fernando. Ela foi adicionada após a análise do [[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis|The Trap SDD Analysis]], que revelou que o harness governa COMO o agente executa mas raramente governa SE o agente deve executar.

### O que um bom harness faz

- Toda intenção que entra no pipeline é classificada em um dos quatro verbos de valor: **Build** (valor claro, construa), **Experiment** (promissor mas incerto, explore com critério de parada), **Defer** (valor possível mas não agora, registre com condição de reativação), **Stop** (não justifica o custo, recuse com alternativa).
- As três perguntas-freio são respondidas e registradas para cada intenção classificada como Build ou Experiment: Quem precisa disso e o que quebra se não existir? Ainda construiríamos se custasse uma semana de engenharia? Quem é o dono de dizer não?
- Existe um Owner-of-No nomeado — papel ou política com autoridade explícita de recusa — para cada domínio do pipeline.
- O gate de valor (entrada) é separado do gate de qualidade (saída): o Manual Brake avalia input, o Evaluator avalia output.
- Recusas e deferrals são registrados com rationale no trace store, não apenas aprovações.
- O time revisa periodicamente as decisões Build/Experiment/Defer/Stop contra outcomes reais para calibrar o julgamento de valor.

### Por que isso importa no KODA

KODA não vive em uma chamada isolada de LLM. Ele vive em conversas que atravessam minutos, horas, preferências, restrições, estoque, preço e confiança.

Quando a dimensão de valor falha, o time constrói features que ninguém pediu, acumula carry debt de artefatos sem owner, e o pipeline de coordenação multi-agente se torna uma máquina de executar trabalho que nunca deveria ter começado.

### Checklist PASS/FAIL

| Item | Critério | PASS | FAIL | Notas |
|------|----------|------|------|-------|
| Classificação de intenção | Toda intenção que entra no pipeline é classificada como Build, Experiment, Defer ou Stop antes da execução. | Existe evidência verificável e atualizada. | Toda intenção vira Build por padrão, sem classificação explícita. | Registre link para artefato, owner e data. |
| Perguntas-freio respondidas | Para cada intenção classificada como Build ou Experiment, as três perguntas-freio têm respostas registradas. | Existe evidência verificável e atualizada. | Features são aprovadas sem que ninguém saiba quem precisa delas ou quem pode dizer não. | Registre link para artefato, owner e data. |
| Owner-of-No designado | Existe um papel ou política com autoridade explícita de recusa para cada domínio do pipeline. | Existe evidência verificável e atualizada. | Ninguém consegue nomear quem tem autoridade para recusar uma feature. | Registre link para artefato, owner e data. |
| Separação value gate / quality gate | O gate de valor (entrada) e o gate de qualidade (saída) são componentes distintos com responsabilidades diferentes. | Existe evidência verificável e atualizada. | O Evaluator é o único gate — não há verificação de valor na entrada. | Registre link para artefato, owner e data. |
| Rationale de recusa registrada | Recusas e deferrals são registrados com rationale no trace store, não apenas aprovações. | Existe evidência verificável e atualizada. | Só se registra o que foi aprovado; recusas desaparecem sem registro. | Registre link para artefato, owner e data. |
| Calibração de julgamento | O time revisa periodicamente decisões de valor contra outcomes reais para calibrar o julgamento. | Existe evidência verificável e atualizada. | Decisões de Build/Stop nunca são revisitadas para aprendizado. | Registre link para artefato, owner e data. |
| Deferred Ledger ativo | As três categorias de dívida (skill, dependence, carry) são monitoradas e revisadas trimestralmente. | Existe evidência verificável e atualizada. | O time só olha para custo de tokens, ignora dívida estrutural. | Registre link para artefato, owner e data. |

### Evidências que um revisor deve pedir

- registro de classificação Build/Experiment/Defer/Stop para as últimas N intenções
- respostas documentadas às três perguntas-freio
- nome do Owner-of-No para cada domínio
- trace de recusa com rationale
- relatório trimestral de calibração de julgamento

### Exemplo de falha típica

❌ O time implementa 12 features em um mês porque "o agente consegue fazer cada uma em 20 minutos". Nenhuma passou pelo Manual Brake. Seis meses depois, 8 features nunca foram usadas — mas consomem tokens de manutenção e superfície de bug.

### Exemplo de desenho melhor

✅ Antes de qualquer feature entrar no pipeline, o Orchestrator aplica o Manual Brake Gate: classifica como Build/Experiment/Defer/Stop, registra as três respostas, e só roteia para execução se a classificação for Build ou Experiment com Owner-of-No aprovando.

### Micro-checklist de revisão rápida

- [ ] Toda intencao que entra no pipeline tem classificacao Build, Experiment, Defer ou Stop registrada?
- [ ] As tres perguntas-freio tem respostas documentadas para intencoes Build e Experiment?
- [ ] Existe um Owner-of-No nomeado para cada dominio com autoridade explicita de recusa?
- [ ] O gate de valor (Manual Brake) e operacionalmente separado do gate de qualidade (Evaluator)?
- [ ] Recusas sao registradas com rationale, nao apenas aprovacoes?
- [ ] O Deferred Ledger (skill debt, dependence debt, carry debt) e revisado trimestralmente?
- [ ] Decisoes de valor passadas sao comparadas com outcomes reais para calibrar julgamento?

### Perguntas de auditoria

- Qual artefato prova que esta regra existe fora da cabeca do agente?
- Qual teste falharia se alguem removesse essa protecao amanha?
- Qual trace mostraria que a protecao foi acionada em producao?
- Quem e o owner desta regra e quando ela foi revisada pela ultima vez?
- Qual e o custo em tokens, latencia ou manutencao desta protecao?
- Qual falha real de cliente esta protecao previne?
- O que acontece quando a protecao rejeita um caso valido?
- O que acontece quando a protecao deixa passar um caso invalido?
- Como um novo dev descobriria essa regra sem perguntar para Fernando?
- A regra esta no lugar certo ou deveria virar contrato, state, rubric ou guardrail?

### Critérios de bloqueio para esta categoria

- Bloqueie produção se features entram no pipeline sem classificação de valor.
- Bloqueie produção se não há Owner-of-No nomeado para decisões de produto.
- Bloqueie produção se o único argumento para construir é "o agente consegue fazer rápido".
- Permita rollout limitado apenas quando o risco estiver documentado, monitorado e reversível.

### Sinais de maturidade crescente

- **Nível 1:** toda intenção vira Build por padrão.
- **Nível 2:** existe intenção de questionar valor, mas é informal e depende de indivíduos corajosos.
- **Nível 3:** há um gate com vocabulário Build/Experiment/Defer/Stop, perguntas-freio, e Owner-of-No nomeado.
- **Nível 4:** o gate é aplicado consistentemente, decisões são auditadas, e o Deferred Ledger é revisado trimestralmente.
- **Nível 5:** o gate é calibrado com outcomes reais, o Owner-of-No é um papel institucionalizado, e o time trata recusas como prática normal de engenharia.

---

## 🧠 1. Contexto (Context Management)

Esta categoria verifica se um harness bom trata contexto como recurso finito, caro e perigoso quando cresce sem curadoria.

### O que um bom harness faz

- A context window tem uma política explícita de entrada, permanência e expiração.
- O token budget reserva espaço para system prompt, estado crítico, histórico recente, tool outputs e resposta final.
- Histórico antigo é comprimido em resumo estruturado, não apenas cortado por tamanho.
- Informações críticas do cliente, como alergias e compromissos comerciais, ficam em state durável e reaparecem no contexto quando necessárias.
- O time consegue explicar por que cada bloco de contexto está presente em uma chamada específica.

### Por que isso importa no KODA

KODA não vive em uma chamada isolada de LLM. Ele vive em conversas que atravessam minutos, horas, preferências, restrições, estoque, preço e confiança.

Quando a dimensão de contexto falha, o cliente não enxerga “um problema técnico”. Ele enxerga uma promessa quebrada.

Fernando ensina o time a procurar a falha antes do incidente: qual evidência existe, qual contrato protege a fronteira e qual trace provará o comportamento depois.

### Checklist PASS/FAIL

| Item | Critério | PASS | FAIL | Notas |
|------|----------|------|------|-------|
| Mapa de fontes de contexto | Existe lista versionada de todas as fontes que entram no prompt: mensagens recentes, summary, state, catálogo, contrato e trace refs. | Existe evidência verificável e atualizada. | Depende de memória, intenção, prompt solto ou comportamento não testado. | Registre link para artefato, owner e data. |
| Janela recente definida | O harness limita a janela recente por número de mensagens ou tokens e registra o corte aplicado em cada turno. | Existe evidência verificável e atualizada. | Depende de memória, intenção, prompt solto ou comportamento não testado. | Registre link para artefato, owner e data. |
| Token budget medido | Cada chamada registra tokens planejados e tokens reais por bloco, com limite máximo antes de chamar o modelo. | Existe evidência verificável e atualizada. | Depende de memória, intenção, prompt solto ou comportamento não testado. | Registre link para artefato, owner e data. |
| Compaction estruturada | Resumos antigos preservam decisões, restrições, pendências, preferências e audit refs em campos separados. | Existe evidência verificável e atualizada. | Depende de memória, intenção, prompt solto ou comportamento não testado. | Registre link para artefato, owner e data. |
| Critério de promoção para state | Há regra objetiva para mover informação do contexto para state durável, como alergia, orçamento confirmado ou endereço. | Existe evidência verificável e atualizada. | Depende de memória, intenção, prompt solto ou comportamento não testado. | Registre link para artefato, owner e data. |
| Separação contexto/state/summary | O documento de arquitetura define o que fica em context window, o que vira state e o que vira summary. | Existe evidência verificável e atualizada. | Depende de memória, intenção, prompt solto ou comportamento não testado. | Registre link para artefato, owner e data. |
| Progressive disclosure por resolver | Skills e runbooks ficam fora do prompt base e são carregados por triggers positivos, exemplos negativos e trigger evals, conforme [[docs/canonical/resolver-based-context-progressive-disclosure|Resolver-Based Context Progressive Disclosure]]. | Existe matriz de triggers, evals e misses revisados. | Instruções crescem em arquivo monolítico sem teste de carregamento. | Registre skill, owner, trigger eval e data. |
| Teste de recall crítico | Existe cenário automatizado em que uma restrição dita cedo é relembrada corretamente após janela longa. | Existe evidência verificável e atualizada. | Depende de memória, intenção, prompt solto ou comportamento não testado. | Registre link para artefato, owner e data. |
| Falha por excesso de tokens | Quando o orçamento estoura, o harness falha antes da chamada ou compacta de forma controlada, nunca corta aleatoriamente. | Existe evidência verificável e atualizada. | Depende de memória, intenção, prompt solto ou comportamento não testado. | Registre link para artefato, owner e data. |

### Evidências que um revisor deve pedir

- trace de prompt com seções nomeadas
- relatório de token usage
- summary JSON de conversa longa
- teste de restrição antiga
- ADR de política de contexto

### Exemplo de falha típica

❌ O harness envia as últimas 200 mensagens porque parece suficiente e só descobre excesso de tokens quando o provedor rejeita a chamada.

### Exemplo de desenho melhor

✅ O harness monta `critical_state`, `history_summary`, `recent_window` e `turn_request` separadamente, calcula tokens por bloco e compacta antes de qualquer chamada.

### X. Stable Harness Prompt (NÃO redutível por compactação)

O que um bom harness faz: o system prompt do harness é a âncora estável da chamada. Compactação reduz history, tool calls e payload, mas NUNCA resume ou trunca o harness prompt. Esse prompt tem budget próprio, versionamento independente e é avaliado separadamente da política de contexto.

Por que importa: se o harness for truncado junto com o payload, o agente perde instruções silenciosamente. O sintoma pode parecer esquecimento de contexto, mas a causa real é perda do contrato operacional que definia papel, ferramentas, segurança e formato.

| Item | Critério | PASS | FAIL | Notas |
|------|----------|------|------|-------|
| Budget separado | System prompt tem budget de tokens separado do payload. | Existe evidência verificável e atualizada. | Prompt e payload disputam o mesmo corte de compactação. | Registre link para artefato, owner e data. |
| Harness não redutível | Política de compactação NUNCA resume ou trunca o harness prompt. | Existe teste ou contrato protegendo a regra. | Compactador trata system prompt como histórico comum. | Registre link para artefato, owner e data. |
| ID versionado | Cada versão do harness prompt tem ID semântico versionado. | Replay e traces registram a versão usada. | Mudanças de prompt não deixam rastro auditável. | Registre link para artefato, owner e data. |
| Evals dedicados | Mudanças no harness prompt são testadas com evals dedicados. | Gate roda antes de rollout. | Prompt muda sem avaliação separada. | Registre link para artefato, owner e data. |
| Replay metadata | Metadata de replay inclui `prompt_version`. | Incidente consegue reconstruir prompt ativo. | Replay depende do prompt atual por acidente. | Registre link para artefato, owner e data. |
| Teste anti-mutação | Existe teste que falha se a compactação mutar o harness. | Teste cobre truncation, summarization e externalização. | Compactação pode alterar instruções sem alerta. | Registre link para artefato, owner e data. |

### Perguntas de auditoria

- Qual artefato prova que esta regra existe fora da cabeça do agente?
- Qual teste falharia se alguém removesse essa proteção amanhã?
- Qual trace mostraria que a proteção foi acionada em produção?
- Quem é o owner desta regra e quando ela foi revisada pela última vez?
- Qual é o custo em tokens, latência ou manutenção desta proteção?
- Qual falha real de cliente esta proteção previne?
- O que acontece quando a proteção rejeita um caso válido?
- O que acontece quando a proteção deixa passar um caso inválido?
- Como um novo dev descobriria essa regra sem perguntar para Fernando?
- A regra está no lugar certo ou deveria virar contrato, state, rubric ou guardrail?

### Micro-checklist de revisão rápida

- [ ] Token budget esta documentado e medido por turno?
- [ ] Blocos `critical_state`, `history_summary`, `recent_window` e `turn_request` aparecem separados no prompt?
- [ ] Resumo antigo preserva decisoes, restricoes, preferencias e pendencias em campos nomeados?
- [ ] Alergias, orcamento e compromissos comerciais foram promovidos para state duravel?
- [ ] Trace registra por que cada fonte entrou ou saiu do contexto?
- [ ] Resolver registra qual skill carregou, qual trigger disparou e qual trigger negativo foi considerado?
- [ ] Teste de conversa longa prova recall de restricao dita no inicio?
- [ ] Corte por excesso de tokens falha antes da chamada ou compacta de forma controlada?
- [ ] Context window exclui dados obsoletos ou conflitantes com o state atual?
- [ ] Owner da politica de contexto e data da ultima revisao estao visiveis?

### Critérios de bloqueio para esta categoria

- Bloqueie produção se a categoria afeta pagamento, saúde, dados pessoais ou promessa de entrega e não há validação objetiva.
- Bloqueie produção se o único argumento for “o modelo costuma acertar”.
- Bloqueie produção se não houver trace suficiente para explicar uma decisão errada depois do fato.
- Permita rollout limitado apenas quando o risco estiver documentado, monitorado e reversível.

### Sinais de maturidade crescente

- **Nível 1:** existe apenas intenção ou prompt informal.
- **Nível 2:** há regra documentada, mas pouca automação.
- **Nível 3:** há contrato, validação e teste principal.
- **Nível 4:** há métricas, replay e revisão periódica.
- **Nível 5:** há evolução contínua com custo, qualidade e remoção controlada.

---

## 📜 2. Contratos (Contracts/Sprint Contracts)

Esta categoria verifica se um harness bom transforma intenção em contrato verificável antes de executar trabalho caro ou irreversível.

### O que um bom harness faz

- Cada etapa declara inputs, outputs, owner, limites e critérios de sucesso antes de rodar.
- Contratos usam schema version e deixam claro quais campos são obrigatórios.
- Failure handling é parte do contrato, não uma reação improvisada depois do erro.
- As fronteiras entre Planner, Generator, Evaluator, Fulfillment e Delivery são explícitas.
- Mudanças de contrato são versionadas e auditáveis.

### Por que isso importa no KODA

KODA não vive em uma chamada isolada de LLM. Ele vive em conversas que atravessam minutos, horas, preferências, restrições, estoque, preço e confiança.

Quando a dimensão de contratos falha, o cliente não enxerga “um problema técnico”. Ele enxerga uma promessa quebrada.

Fernando ensina o time a procurar a falha antes do incidente: qual evidência existe, qual contrato protege a fronteira e qual trace provará o comportamento depois.

### Checklist PASS/FAIL

| Item | Critério | PASS | FAIL | Notas |
|------|----------|------|------|-------|
| Inputs explícitos | Cada contrato lista arquivos, campos e pré-condições obrigatórias para iniciar a etapa. | Existe evidência verificável e atualizada. | Depende de memória, intenção, prompt solto ou comportamento não testado. | Registre link para artefato, owner e data. |
| Outputs verificáveis | Cada output tem schema, campos obrigatórios, tipos esperados e exemplos válidos em documentação ou teste. | Existe evidência verificável e atualizada. | Depende de memória, intenção, prompt solto ou comportamento não testado. | Registre link para artefato, owner e data. |
| Critério de sucesso | O contrato define condição objetiva de conclusão, como `evaluation.decision == approved` e `score >= 85`. | Existe evidência verificável e atualizada. | Depende de memória, intenção, prompt solto ou comportamento não testado. | Registre link para artefato, owner e data. |
| Failure modes declarados | O contrato lista pelo menos erro de input inválido, timeout, output inválido e dependência indisponível. | Existe evidência verificável e atualizada. | Depende de memória, intenção, prompt solto ou comportamento não testado. | Registre link para artefato, owner e data. |
| Versionamento de interface | Todo artefato possui `schema_version` e há regra de compatibilidade entre versões. | Existe evidência verificável e atualizada. | Depende de memória, intenção, prompt solto ou comportamento não testado. | Registre link para artefato, owner e data. |
| Ownership único | Para cada contrato existe um owner responsável por manter schema, rubrica e exemplos. | Existe evidência verificável e atualizada. | Depende de memória, intenção, prompt solto ou comportamento não testado. | Registre link para artefato, owner e data. |
| Boundary test | Há teste que envia input válido mínimo, input inválido e output fora do schema para a fronteira. | Existe evidência verificável e atualizada. | Depende de memória, intenção, prompt solto ou comportamento não testado. | Registre link para artefato, owner e data. |
| Auditoria de alteração | Toda mudança de contrato relevante aponta para ADR, issue ou changelog com motivo e impacto. | Existe evidência verificável e atualizada. | Depende de memória, intenção, prompt solto ou comportamento não testado. | Registre link para artefato, owner e data. |
| Constraint budget gate | O contrato limita constraints a 5-7 itens direcionais, incondicionais e em linguagem de negócio. Constraints de implementação ("usar Redis", "escrever em TypeScript") são reclassificadas como contexto. | Lista tem entre 5 e 7 constraints; cada constraint é direcional e verificável. | Lista tem 12+ itens, mistura constraints reais com preferências de implementação e critérios de qualidade. | Registre a lista de constraints, data de revisão e owner. |
| Constraint classification gate | Cada constraint passa no teste "Saber isso muda como o Builder escreve código?" Items que falham são movidos para failure conditions. | Existe classificação documentada; constraints e failure conditions estão em artefatos separados. | Constraints e failure conditions misturados no mesmo prompt; o Generator recebe critérios de avaliação. | Registre link para a matriz de classificação, owner e data. |

### Evidências que um revisor deve pedir

- sprint_contract.json
- schema JSON
- teste de contrato
- ADR de interface
- trace mostrando contrato assinado

### Exemplo de falha típica

❌ O Order Agent espera que o Discovery Agent entregue produtos, mas ninguém definiu se o preço vem em centavos, reais ou string formatada.

### Exemplo de desenho melhor

✅ O contrato `product_discovery.v2` exige `sku`, `price_cents`, `availability_region`, `dietary_flags` e bloqueia geração se faltar qualquer campo.

### Perguntas de auditoria

- Qual artefato prova que esta regra existe fora da cabeça do agente?
- Qual teste falharia se alguém removesse essa proteção amanhã?
- Qual trace mostraria que a proteção foi acionada em produção?
- Quem é o owner desta regra e quando ela foi revisada pela última vez?
- Qual é o custo em tokens, latência ou manutenção desta proteção?
- Qual falha real de cliente esta proteção previne?
- O que acontece quando a proteção rejeita um caso válido?
- O que acontece quando a proteção deixa passar um caso inválido?
- Como um novo dev descobriria essa regra sem perguntar para Fernando?
- A regra está no lugar certo ou deveria virar contrato, state, rubric ou guardrail?

### Micro-checklist de revisão rápida

- [ ] Todo contrato define inputs, outputs e criterios de sucesso?
- [ ] Campos obrigatorios tem tipos, exemplos validos e schema versionado?
- [ ] Failure modes incluem input invalido, timeout, dependencia indisponivel e output fora do schema?
- [ ] Cada contrato declara owner responsavel pela interface?
- [ ] Boundary test cobre input minimo valido, input invalido e output inesperado?
- [ ] Mudanca de contrato aponta para ADR, issue ou changelog com impacto?
- [ ] Fronteiras entre Planner, Generator, Evaluator, Order e Fulfillment estao explicitas?
- [ ] Criterio de sucesso usa condicao objetiva, como score minimo ou decisao aprovada?
- [ ] Contrato bloqueia execucao quando falta campo critico de catalogo, preco ou restricao?
- [ ] Constraints estao limitadas a 5-7 itens direcionais em linguagem de negocio?
- [ ] Constraints de implementacao foram reclassificadas como contexto ou failure conditions?
- [ ] Cada constraint passa no teste "saber isso muda como o Builder escreve codigo?"?

### Critérios de bloqueio para esta categoria

- Bloqueie produção se a categoria afeta pagamento, saúde, dados pessoais ou promessa de entrega e não há validação objetiva.
- Bloqueie produção se o único argumento for "o modelo costuma acertar".
- Bloqueie produção se não houver trace suficiente para explicar uma decisão errada depois do fato.
- Bloqueie produção se a lista de constraints tem mais de 12 itens sem classificação -- constraint lists infladas escondem especificações de implementação.
- Permita rollout limitado apenas quando o risco estiver documentado, monitorado e reversível.

### Sinais de maturidade crescente

- **Nível 1:** existe apenas intenção ou prompt informal.
- **Nível 2:** há regra documentada, mas pouca automação.
- **Nível 3:** há contrato, validação e teste principal.
- **Nível 4:** há métricas, replay e revisão periódica.
- **Nível 5:** há evolução contínua com custo, qualidade e remoção controlada.

---

## ⚖️ 3. Avaliação (Evaluation/Rubrics)

Esta categoria verifica se um harness bom separa geração de julgamento e transforma qualidade em critérios mensuráveis.

### O que um bom harness faz

- Rubrics têm dimensões com pesos, thresholds e blockers explícitos.
- O Evaluator é separado do Generator e não reusa a justificativa do Generator como prova.
- Critérios de aprovação combinam score ponderado com bloqueios absolutos.
- Cada avaliação produz evidência auditável, não apenas uma nota final.
- A rubrica é calibrada com exemplos aprovados, reprovados e limítrofes.
- Generator e Evaluator operam com superfícies de informação seladas: o Generator não vê a rubrica nem as failure conditions; o Evaluator não depende da autoavaliação do Generator.
- O harness previne ativamente reward-hacking mantendo métricas de avaliação fora do contexto do Generator.

### Por que isso importa no KODA

KODA não vive em uma chamada isolada de LLM. Ele vive em conversas que atravessam minutos, horas, preferências, restrições, estoque, preço e confiança.

Quando a dimensão de avaliação falha, o cliente não enxerga “um problema técnico”. Ele enxerga uma promessa quebrada.

Fernando ensina o time a procurar a falha antes do incidente: qual evidência existe, qual contrato protege a fronteira e qual trace provará o comportamento depois.

### Checklist PASS/FAIL

| Item | Critério | PASS | FAIL | Notas |
|------|----------|------|------|-------|
| Dimensões definidas | Rubrica lista dimensões nomeadas, como segurança, adequação, completude, consistência e formato. | Existe evidência verificável e atualizada. | Depende de memória, intenção, prompt solto ou comportamento não testado. | Registre link para artefato, owner e data. |
| Pesos somam 100% | Os pesos da rubrica totalizam exatamente 100% e cada peso tem justificativa. | Existe evidência verificável e atualizada. | Depende de memória, intenção, prompt solto ou comportamento não testado. | Registre link para artefato, owner e data. |
| Threshold operacional | Existe nota mínima objetiva para aprovar, como `score >= 85`, e resultado abaixo disso reprova. | Existe evidência verificável e atualizada. | Depende de memória, intenção, prompt solto ou comportamento não testado. | Registre link para artefato, owner e data. |
| Blockers absolutos | Critérios como alergia violada, preço divergente ou pagamento duplicado reprovam mesmo com score alto. | Existe evidência verificável e atualizada. | Depende de memória, intenção, prompt solto ou comportamento não testado. | Registre link para artefato, owner e data. |
| Separação Generator/Evaluator | O Evaluator recebe output e evidências, mas não depende da autoavaliação do Generator. | Existe evidência verificável e atualizada. | Depende de memória, intenção, prompt solto ou comportamento não testado. | Registre link para artefato, owner e data. |
| Evidência por dimensão | Cada nota inclui citação de campo, trace ref ou dado usado para decidir. | Existe evidência verificável e atualizada. | Depende de memória, intenção, prompt solto ou comportamento não testado. | Registre link para artefato, owner e data. |
| Calibração periódica | Há amostra revisada por humano para medir falso positivo e falso negativo da rubrica. | Existe evidência verificável e atualizada. | Depende de memória, intenção, prompt solto ou comportamento não testado. | Registre link para artefato, owner e data. |
| Replay de avaliação | É possível reexecutar a avaliação sobre o mesmo output e obter decisão comparável. | Existe evidência verificável e atualizada. | Depende de memória, intenção, prompt solto ou comportamento não testado. | Registre link para artefato, owner e data. |
| Superfícies de informação seladas | O Generator NÃO recebe rubricas, failure conditions detalhadas, thresholds de aprovação ou exemplos de outputs reprovados. O Evaluator NÃO recebe justificativas do Generator como evidência. | Existe matriz de visibilidade declarando quais artefatos cada agente pode acessar. Os prompts de Generator e Evaluator são construídos a partir de fontes diferentes. | Generator e Evaluator recebem o mesmo prompt com a mesma rubrica. O Generator pode ver os critérios pelos quais será avaliado. | Registre a matriz de visibilidade, versão e owner. |
| Prevenção de reward-hacking | O desenho do harness parte da premissa de que o Generator otimizará para o que consegue ver. Failure conditions que o Generator poderia "gaming" são movidas para a superfície selada do Evaluator. | Existe pelo menos um caso documentado onde uma métrica visível ao Generator foi substituída por uma verificação cega do Evaluator. | O Generator tem acesso a todas as métricas e rubricas; nenhuma verificação é cega. | Registre link para o ADR de compartmentation, owner e data. |

### Evidências que um revisor deve pedir

- rubric.md
- evaluation.json
- calibration set
- trace de Generator/Evaluator
- relatório de false negatives

### Exemplo de falha típica

❌ O sistema pergunta ao mesmo agente se a resposta ficou boa e aceita qualquer “sim, atende ao cliente”.

### Exemplo de desenho melhor

✅ O Generator propõe três SKUs; o Evaluator lê catálogo, restrições e rubric, calcula score por dimensão e rejeita violação de lactose mesmo se preço for ótimo.

### Perguntas de auditoria

- Qual artefato prova que esta regra existe fora da cabeça do agente?
- Qual teste falharia se alguém removesse essa proteção amanhã?
- Qual trace mostraria que a proteção foi acionada em produção?
- Quem é o owner desta regra e quando ela foi revisada pela última vez?
- Qual é o custo em tokens, latência ou manutenção desta proteção?
- Qual falha real de cliente esta proteção previne?
- O que acontece quando a proteção rejeita um caso válido?
- O que acontece quando a proteção deixa passar um caso inválido?
- Como um novo dev descobriria essa regra sem perguntar para Fernando?
- A regra está no lugar certo ou deveria virar contrato, state, rubric ou guardrail?

### Micro-checklist de revisão rápida

- [ ] Rubrica tem dimensoes nomeadas com pesos que somam 100%?
- [ ] Threshold operacional reprova automaticamente abaixo da nota minima?
- [ ] Rubrica tem blocker absoluto para violacoes criticas?
- [ ] Evaluator e separado do Generator e nao aceita autoaprovacao?
- [ ] Cada nota traz evidencia por dimensao, como campo, trace ref ou dado de catalogo?
- [ ] Conjunto de calibracao inclui exemplos aprovados, reprovados e limitrofes?
- [ ] Replay da avaliacao produz decisao comparavel sobre o mesmo output?
- [ ] Falsos positivos e falsos negativos sao revisados por humano em cadencia definida?
- [ ] Score alto nao mascara alergia, preco divergente, estoque ausente ou pagamento duplicado?
- [ ] Generator e Evaluator recebem superfícies de informação diferentes (Generator nao ve a rubrica)?
- [ ] Existe matriz de visibilidade documentando quais artefatos cada agente pode acessar?
- [ ] Failure conditions que poderiam ser "gamificadas" estao na superficie selada do Evaluator?

### Critérios de bloqueio para esta categoria

- Bloqueie produção se a categoria afeta pagamento, saúde, dados pessoais ou promessa de entrega e não há validação objetiva.
- Bloqueie produção se o único argumento for "o modelo costuma acertar".
- Bloqueie produção se não houver trace suficiente para explicar uma decisão errada depois do fato.
- Bloqueie produção se Generator e Evaluator compartilham a mesma superfície de informação sem matriz de visibilidade -- sem compartimentação, o Generator aprende a otimizar para os checks que conhece.
- Permita rollout limitado apenas quando o risco estiver documentado, monitorado e reversível.

### Sinais de maturidade crescente

- **Nível 1:** existe apenas intenção ou prompt informal.
- **Nível 2:** há regra documentada, mas pouca automação.
- **Nível 3:** há contrato, validação e teste principal.
- **Nível 4:** há métricas, replay e revisão periódica.
- **Nível 5:** há evolução contínua com custo, qualidade e remoção controlada.

---

## 💾 4. Persistência (State Persistence)

Esta categoria verifica se um harness bom trata estado como promessa durável ao cliente e como base de replay para engenharia.

### O que um bom harness faz

- Checkpoints existem em cada fronteira crítica da jornada.
- O estado tem schema claro, versão e política de migração.
- Recovery é testado por simulação de crash, não apenas descrito em arquitetura.
- Replay usa artefatos salvos para reproduzir decisão sem depender de memória implícita.
- A escolha entre arquivos, SQLite, Redis ou banco remoto é justificada por volume, concorrência e auditabilidade.

### Por que isso importa no KODA

KODA não vive em uma chamada isolada de LLM. Ele vive em conversas que atravessam minutos, horas, preferências, restrições, estoque, preço e confiança.

Quando a dimensão de persistência falha, o cliente não enxerga “um problema técnico”. Ele enxerga uma promessa quebrada.

Fernando ensina o time a procurar a falha antes do incidente: qual evidência existe, qual contrato protege a fronteira e qual trace provará o comportamento depois.

### Checklist PASS/FAIL

| Item | Critério | PASS | FAIL | Notas |
|------|----------|------|------|-------|
| Checkpoint por fase | Cada fase longa salva checkpoint antes e depois de ações caras ou irreversíveis. | Existe evidência verificável e atualizada. | Depende de memória, intenção, prompt solto ou comportamento não testado. | Registre link para artefato, owner e data. |
| Schema de estado | State files ou tabelas possuem campos obrigatórios, `schema_version`, timestamps e owner. | Existe evidência verificável e atualizada. | Depende de memória, intenção, prompt solto ou comportamento não testado. | Registre link para artefato, owner e data. |
| Recovery testado | Há teste que mata o processo no meio da jornada e verifica retomada a partir do último checkpoint. | Existe evidência verificável e atualizada. | Depende de memória, intenção, prompt solto ou comportamento não testado. | Registre link para artefato, owner e data. |
| Replay determinístico | Um trace salvo contém inputs suficientes para reexecutar Planner, Generator e Evaluator em modo diagnóstico. | Existe evidência verificável e atualizada. | Depende de memória, intenção, prompt solto ou comportamento não testado. | Registre link para artefato, owner e data. |
| Atomic write | Arquivos JSON são escritos em `.tmp` e publicados com rename atômico. | Existe evidência verificável e atualizada. | Depende de memória, intenção, prompt solto ou comportamento não testado. | Registre link para artefato, owner e data. |
| Retenção definida | Existe política de retenção para state, traces e dados pessoais, com justificativa de negócio. | Existe evidência verificável e atualizada. | Depende de memória, intenção, prompt solto ou comportamento não testado. | Registre link para artefato, owner e data. |
| Backups verificáveis | Backup é restaurado periodicamente em ambiente seguro e a restauração é documentada. | Existe evidência verificável e atualizada. | Depende de memória, intenção, prompt solto ou comportamento não testado. | Registre link para artefato, owner e data. |
| Escolha de backend | A arquitetura explica por que usa files, SQLite, Redis ou banco, considerando concorrência, queries e operação. | Existe evidência verificável e atualizada. | Depende de memória, intenção, prompt solto ou comportamento não testado. | Registre link para artefato, owner e data. |

### Evidências que um revisor deve pedir

- session_state.json
- checkpoint log
- replay script
- schema de estado
- relatório de restore

### Exemplo de falha típica

❌ O carrinho do cliente existe apenas na memória do worker e desaparece quando o deploy reinicia o processo.

### Exemplo de desenho melhor

✅ Após cada etapa, KODA salva `preferences.json`, `cart.json`, `evaluation.json` e `status.json`; se cair, retoma pelo último status completo.

### Perguntas de auditoria

- Qual artefato prova que esta regra existe fora da cabeça do agente?
- Qual teste falharia se alguém removesse essa proteção amanhã?
- Qual trace mostraria que a proteção foi acionada em produção?
- Quem é o owner desta regra e quando ela foi revisada pela última vez?
- Qual é o custo em tokens, latência ou manutenção desta proteção?
- Qual falha real de cliente esta proteção previne?
- O que acontece quando a proteção rejeita um caso válido?
- O que acontece quando a proteção deixa passar um caso inválido?
- Como um novo dev descobriria essa regra sem perguntar para Fernando?
- A regra está no lugar certo ou deveria virar contrato, state, rubric ou guardrail?

### Micro-checklist de revisão rápida

- [ ] Estado critico sobrevive a restart do processo?
- [ ] Checkpoints existem antes e depois de acoes caras ou irreversiveis?
- [ ] State schema inclui `schema_version`, timestamps, owner e campos obrigatorios?
- [ ] Recovery foi testado matando o processo no meio da jornada?
- [ ] Replay usa artefatos salvos sem depender de memoria oral do time?
- [ ] Arquivos de estado usam escrita temporaria e rename atomico?
- [ ] Politica de retencao cobre state, traces e dados pessoais?
- [ ] Backup foi restaurado em ambiente seguro e registrado?
- [ ] Escolha entre files, SQLite, Redis ou banco esta justificada por volume e concorrencia?

### Critérios de bloqueio para esta categoria

- Bloqueie produção se a categoria afeta pagamento, saúde, dados pessoais ou promessa de entrega e não há validação objetiva.
- Bloqueie produção se o único argumento for “o modelo costuma acertar”.
- Bloqueie produção se não houver trace suficiente para explicar uma decisão errada depois do fato.
- Permita rollout limitado apenas quando o risco estiver documentado, monitorado e reversível.

### Sinais de maturidade crescente

- **Nível 1:** existe apenas intenção ou prompt informal.
- **Nível 2:** há regra documentada, mas pouca automação.
- **Nível 3:** há contrato, validação e teste principal.
- **Nível 4:** há métricas, replay e revisão periódica.
- **Nível 5:** há evolução contínua com custo, qualidade e remoção controlada.

---

## 🤝 5. Coordenação (Multi-Agent Coordination)

Esta categoria verifica se um harness bom faz agentes colaborarem por protocolo explícito, não por sorte ou timing favorável.

### O que um bom harness faz

- Agentes não escrevem no mesmo recurso sem lock ou transação.
- Status files tornam progresso observável e retomável.
- Protocolos JSON definem quem lê, quem escreve e quando a etapa está liberada.
- Race conditions conhecidas têm testes e mitigação.
- Comunicação entre agentes deixa audit trail suficiente para reconstruir a jornada.

### Por que isso importa no KODA

KODA não vive em uma chamada isolada de LLM. Ele vive em conversas que atravessam minutos, horas, preferências, restrições, estoque, preço e confiança.

Quando a dimensão de coordenação falha, o cliente não enxerga “um problema técnico”. Ele enxerga uma promessa quebrada.

Fernando ensina o time a procurar a falha antes do incidente: qual evidência existe, qual contrato protege a fronteira e qual trace provará o comportamento depois.

### Checklist PASS/FAIL

| Item | Critério | PASS | FAIL | Notas |
|------|----------|------|------|-------|
| Lock para recurso compartilhado | Qualquer escrita em pedido, carrinho, perfil ou estoque usa lock, transação ou fila serializadora. | Existe evidência verificável e atualizada. | Depende de memória, intenção, prompt solto ou comportamento não testado. | Registre link para artefato, owner e data. |
| Status visível | Cada agente publica `pending`, `running`, `completed` ou `failed` com timestamp e motivo. | Existe evidência verificável e atualizada. | Depende de memória, intenção, prompt solto ou comportamento não testado. | Registre link para artefato, owner e data. |
| JSON protocol estável | Mensagens entre agentes seguem schema com `correlation_id`, `agent_id`, `schema_version` e `audit_refs`. | Existe evidência verificável e atualizada. | Depende de memória, intenção, prompt solto ou comportamento não testado. | Registre link para artefato, owner e data. |
| Atomic publish | Outputs finais só aparecem quando completos; leitores ignoram arquivos `.tmp`. | Existe evidência verificável e atualizada. | Depende de memória, intenção, prompt solto ou comportamento não testado. | Registre link para artefato, owner e data. |
| Idempotência | Reprocessar o mesmo evento não cria pedido duplicado nem reserva estoque duas vezes. | Existe evidência verificável e atualizada. | Depende de memória, intenção, prompt solto ou comportamento não testado. | Registre link para artefato, owner e data. |
| Timeout de lock | Locks têm TTL, owner e regra de recuperação para evitar deadlock permanente. | Existe evidência verificável e atualizada. | Depende de memória, intenção, prompt solto ou comportamento não testado. | Registre link para artefato, owner e data. |
| Ordem de execução | Dependências entre agentes são declaradas, por exemplo Fulfillment só roda após Evaluation aprovado. | Existe evidência verificável e atualizada. | Depende de memória, intenção, prompt solto ou comportamento não testado. | Registre link para artefato, owner e data. |
| Teste de concorrência | Há teste que dispara dois agentes sobre o mesmo recurso e verifica ausência de race condition. | Existe evidência verificável e atualizada. | Depende de memória, intenção, prompt solto ou comportamento não testado. | Registre link para artefato, owner e data. |

### Evidências que um revisor deve pedir

- lock.json
- status.json
- protocol schema
- teste concorrente
- trace com correlation_id

### Exemplo de falha típica

❌ Discovery, Order e Fulfillment reagem ao mesmo evento de WhatsApp e cada um altera uma parte do pedido sem ordem global.

### Exemplo de desenho melhor

✅ Discovery escreve `discovery.json`; Order aguarda status completo, adquire `order.lock.json`, escreve draft; Fulfillment aguarda `evaluation.approved`.

### Perguntas de auditoria

- Qual artefato prova que esta regra existe fora da cabeça do agente?
- Qual teste falharia se alguém removesse essa proteção amanhã?
- Qual trace mostraria que a proteção foi acionada em produção?
- Quem é o owner desta regra e quando ela foi revisada pela última vez?
- Qual é o custo em tokens, latência ou manutenção desta proteção?
- Qual falha real de cliente esta proteção previne?
- O que acontece quando a proteção rejeita um caso válido?
- O que acontece quando a proteção deixa passar um caso inválido?
- Como um novo dev descobriria essa regra sem perguntar para Fernando?
- A regra está no lugar certo ou deveria virar contrato, state, rubric ou guardrail?

### Micro-checklist de revisão rápida

- [ ] Lock file, transacao ou fila serializa escrita em carrinho, pedido, perfil ou estoque?
- [ ] Status file publica `pending`, `running`, `completed` ou `failed` com timestamp?
- [ ] JSON protocol define `correlation_id`, `agent_id`, `schema_version` e `audit_refs`?
- [ ] Outputs finais so aparecem depois de escrita completa e atomica?
- [ ] Reprocessamento do mesmo evento e idempotente?
- [ ] Locks tem TTL, owner e regra de recuperacao contra deadlock?
- [ ] Dependencias impedem Fulfillment antes de Evaluation aprovado?
- [ ] Teste concorrente dispara dois agentes sobre o mesmo recurso?
- [ ] Trace mostra ordem real de leitura, escrita e liberacao entre agentes?

### Critérios de bloqueio para esta categoria

- Bloqueie produção se a categoria afeta pagamento, saúde, dados pessoais ou promessa de entrega e não há validação objetiva.
- Bloqueie produção se o único argumento for “o modelo costuma acertar”.
- Bloqueie produção se não houver trace suficiente para explicar uma decisão errada depois do fato.
- Permita rollout limitado apenas quando o risco estiver documentado, monitorado e reversível.

### Sinais de maturidade crescente

- **Nível 1:** existe apenas intenção ou prompt informal.
- **Nível 2:** há regra documentada, mas pouca automação.
- **Nível 3:** há contrato, validação e teste principal.
- **Nível 4:** há métricas, replay e revisão periódica.
- **Nível 5:** há evolução contínua com custo, qualidade e remoção controlada.

---

## 🛡️ 6. Segurança & Guardrails

Esta categoria verifica se um harness bom impede que inputs ruins, outputs perigosos e custos descontrolados atravessem fronteiras críticas.

### O que um bom harness faz

- Inputs externos são validados antes de entrar no prompt.
- Outputs são validados por formato, domínio, constraints e segurança antes de chegar ao cliente.
- Fallback handlers são seguros, específicos e rastreáveis.
- Budget guards limitam tokens, iterações, tool calls e tempo total.
- Guardrails falham fechado quando o risco envolve saúde, pagamento, dados pessoais ou promessa comercial.

### Por que isso importa no KODA

KODA não vive em uma chamada isolada de LLM. Ele vive em conversas que atravessam minutos, horas, preferências, restrições, estoque, preço e confiança.

Quando a dimensão de segurança falha, o cliente não enxerga “um problema técnico”. Ele enxerga uma promessa quebrada.

Fernando ensina o time a procurar a falha antes do incidente: qual evidência existe, qual contrato protege a fronteira e qual trace provará o comportamento depois.

### Checklist PASS/FAIL

| Item | Critério | PASS | FAIL | Notas |
|------|----------|------|------|-------|
| Input validation | Mensagens, webhook payloads e tool results passam por schema e limites de tamanho antes de uso. | Existe evidência verificável e atualizada. | Depende de memória, intenção, prompt solto ou comportamento não testado. | Registre link para artefato, owner e data. |
| Output validation | Resposta final é validada contra formato, política comercial, restrições médicas e dados de catálogo. | Existe evidência verificável e atualizada. | Depende de memória, intenção, prompt solto ou comportamento não testado. | Registre link para artefato, owner e data. |
| Constraint checker | Restrições do cliente, como alergia, orçamento e região, são checadas por código ou evaluator independente. | Existe evidência verificável e atualizada. | Depende de memória, intenção, prompt solto ou comportamento não testado. | Registre link para artefato, owner e data. |
| Fallback handler | Cada falha conhecida tem fallback seguro: pedir confirmação, escalar para humano ou pausar a ação. | Existe evidência verificável e atualizada. | Depende de memória, intenção, prompt solto ou comportamento não testado. | Registre link para artefato, owner e data. |
| Budget guard | Há limite explícito para tokens, custo, número de retries, tool calls e duração por turno. | Existe evidência verificável e atualizada. | Depende de memória, intenção, prompt solto ou comportamento não testado. | Registre link para artefato, owner e data. |
| Format validator | JSON, markdown operacional, links e mensagens WhatsApp têm validação objetiva antes do envio. | Existe evidência verificável e atualizada. | Depende de memória, intenção, prompt solto ou comportamento não testado. | Registre link para artefato, owner e data. |
| Proteção contra prompt injection | Conteúdo de cliente e tool output é delimitado e não pode redefinir instruções do sistema. | Existe evidência verificável e atualizada. | Depende de memória, intenção, prompt solto ou comportamento não testado. | Registre link para artefato, owner e data. |
| Bloqueio de ação irreversível | Pagamento, estoque e envio ao cliente exigem aprovação validada antes de execução. | Existe evidência verificável e atualizada. | Depende de memória, intenção, prompt solto ou comportamento não testado. | Registre link para artefato, owner e data. |

### Evidências que um revisor deve pedir

- schemas de entrada
- validator logs
- fallback metrics
- budget dashboard
- security test cases

### Exemplo de falha típica

❌ O agente aceita qualquer texto do WhatsApp, mistura instruções do cliente com system prompt e envia link de pagamento sem validação final.

### Exemplo de desenho melhor

✅ O harness valida payload, normaliza intent, bloqueia prompt injection, gera resposta em JSON, valida constraints e só então renderiza mensagem ao cliente.

### Perguntas de auditoria

- Qual artefato prova que esta regra existe fora da cabeça do agente?
- Qual teste falharia se alguém removesse essa proteção amanhã?
- Qual trace mostraria que a proteção foi acionada em produção?
- Quem é o owner desta regra e quando ela foi revisada pela última vez?
- Qual é o custo em tokens, latência ou manutenção desta proteção?
- Qual falha real de cliente esta proteção previne?
- O que acontece quando a proteção rejeita um caso válido?
- O que acontece quando a proteção deixa passar um caso inválido?
- Como um novo dev descobriria essa regra sem perguntar para Fernando?
- A regra está no lugar certo ou deveria virar contrato, state, rubric ou guardrail?

### Micro-checklist de revisão rápida

- [ ] Input externo passa por schema, limite de tamanho e normalizacao antes do prompt?
- [ ] Output final valida formato, catalogo, politica comercial e restricoes do cliente?
- [ ] Constraint checker bloqueia alergia, orcamento, regiao e estoque incompatíveis?
- [ ] Guardrails falham fechado em acoes irreversiveis?
- [ ] Fallback seguro pede confirmacao, escala para humano ou pausa a acao?
- [ ] Budget guard limita tokens, custo, retries, tool calls e duracao por turno?
- [ ] Prompt injection e delimitada e nao pode redefinir instrucoes de sistema?
- [ ] Pagamento, estoque e envio exigem aprovacao validada antes de executar?
- [ ] Logs mostram qual guardrail aceitou, rejeitou ou acionou fallback?

### Critérios de bloqueio para esta categoria

- Bloqueie produção se a categoria afeta pagamento, saúde, dados pessoais ou promessa de entrega e não há validação objetiva.
- Bloqueie produção se o único argumento for “o modelo costuma acertar”.
- Bloqueie produção se não houver trace suficiente para explicar uma decisão errada depois do fato.
- Permita rollout limitado apenas quando o risco estiver documentado, monitorado e reversível.

### Sinais de maturidade crescente

- **Nível 1:** existe apenas intenção ou prompt informal.
- **Nível 2:** há regra documentada, mas pouca automação.
- **Nível 3:** há contrato, validação e teste principal.
- **Nível 4:** há métricas, replay e revisão periódica.
- **Nível 5:** há evolução contínua com custo, qualidade e remoção controlada.

---

## 🧬 7. Evolução (Harness Evolution)

Esta categoria verifica se um harness bom muda com o modelo, mede o próprio custo e remove proteções que viraram peso morto.

### O que um bom harness faz

- Cada componente tem fase BUILD, STABILIZE, SIMPLIFY ou REMOVE.
- Métricas mostram efetividade real, falsos positivos, custo de tokens, latência e manutenção.
- Critérios de remoção são objetivos e testados por shadow mode ou A/B controlado.
- Rollback está planejado antes de simplificar qualquer guardrail crítico.
- Decisões arquiteturais relevantes são registradas em ADR.

### Por que isso importa no KODA

KODA não vive em uma chamada isolada de LLM. Ele vive em conversas que atravessam minutos, horas, preferências, restrições, estoque, preço e confiança.

Quando a dimensão de evolução falha, o cliente não enxerga “um problema técnico”. Ele enxerga uma promessa quebrada.

Fernando ensina o time a procurar a falha antes do incidente: qual evidência existe, qual contrato protege a fronteira e qual trace provará o comportamento depois.

### Checklist PASS/FAIL

| Item | Critério | PASS | FAIL | Notas |
|------|----------|------|------|-------|
| Fase declarada | Cada componente do harness tem fase atual e data da última revisão. | Existe evidência verificável e atualizada. | Depende de memória, intenção, prompt solto ou comportamento não testado. | Registre link para artefato, owner e data. |
| Métricas de efetividade | Dashboard mostra quantas falhas reais o componente preveniu no período avaliado. | Existe evidência verificável e atualizada. | Depende de memória, intenção, prompt solto ou comportamento não testado. | Registre link para artefato, owner e data. |
| Custo total medido | Tokens, latência, manutenção, complexidade de onboarding e falsos positivos são medidos. | Existe evidência verificável e atualizada. | Depende de memória, intenção, prompt solto ou comportamento não testado. | Registre link para artefato, owner e data. |
| Critério de simplificação | Há limite objetivo, como baixa efetividade por 60 dias e shadow test sem regressão relevante. | Existe evidência verificável e atualizada. | Depende de memória, intenção, prompt solto ou comportamento não testado. | Registre link para artefato, owner e data. |
| Critério de remoção | Remoção exige evidência, plano de rollback e aprovação registrada. | Existe evidência verificável e atualizada. | Depende de memória, intenção, prompt solto ou comportamento não testado. | Registre link para artefato, owner e data. |
| Rollback pronto | Existe feature flag, versão anterior ou procedimento de restauração testado. | Existe evidência verificável e atualizada. | Depende de memória, intenção, prompt solto ou comportamento não testado. | Registre link para artefato, owner e data. |
| ADR ou changelog | Mudanças estruturais têm documento com contexto, decisão, alternativas e consequências. | Existe evidência verificável e atualizada. | Depende de memória, intenção, prompt solto ou comportamento não testado. | Registre link para artefato, owner e data. |
| Revisão periódica | O time revisa componentes após upgrade de modelo ou a cada ciclo trimestral. | Existe evidência verificável e atualizada. | Depende de memória, intenção, prompt solto ou comportamento não testado. | Registre link para artefato, owner e data. |
| Separação invariante vs compensação | Cada componente do harness esta classificado como invariante de dominio ou compensacao de modelo, conforme [[docs/canonical/invariant-compensation-split|Invariant-Compensation Split]]. Compensacoes tem criterio de expiracao documentado. | Existe evidencia verificavel e atualizada. | Nao ha distincao entre o que e permanente e o que e temporario. | Registre link para artefato, owner e data. |
| GC Day semanal | Existe um ritual semanal documentado onde feedback humano de revisao e convertido em guardrails automatizados (lint rules, skills, reviewer prompts), conforme [[docs/canonical/garbage-collection-day-meta-loop|Garbage Collection Day Meta-Loop]]. | Calendario fixo, owner definido, backlog de conversoes visivel. | Padroes de falha sao tratados caso a caso, sem sistematizacao. | Registre link para artefato, owner e data. |
| Classificacao de padroes de falha | Falhas, escapes e misbehaviors sao classificados por taxonomia (context_loss, tool_misuse, rubric_gap, safety_escape, etc.) e convertidos em casos de regressao com tier assignment, conforme [[docs/canonical/failure-pattern-classification-loop|Failure Pattern Classification Loop]]. | Taxonomia documentada, casos vinculados a tiers de eval, deduplicacao ativa. | Cada falha gera um card avulso, sem classificacao ou prevencao sistemica. | Registre link para artefato, owner e data. |
| Documentacao baseada em personas | Conhecimento especializado (front-end, seguranca, UX, produto) vive em documentos NFR por persona, nao apenas em AGENTS.md universal. Agentes herdam as personas relevantes automaticamente, conforme [[docs/canonical/persona-based-documentation|Persona-Based Documentation]]. | Cada especialidade tem dono, documento versionado e dispatch por tipo de tarefa. | Conhecimento de qualidade vive na cabeca dos especialistas ou em comentarios de PR. | Registre link para artefato, owner e data. |

### Evidências que um revisor deve pedir

- dashboard de evolução
- ADR
- shadow test
- feature flag
- relatório BUILD/STABILIZE/SIMPLIFY/REMOVE

### Exemplo de falha típica

❌ O time mantém 11 guardrails criados para um modelo antigo mesmo depois de upgrade que tornou metade deles redundante.

### Exemplo de desenho melhor

✅ Após 90 dias de dados, KODA coloca Context Loader em shadow mode, mede delta de qualidade, simplifica prompt e mantém rollback por feature flag.

### Perguntas de auditoria

- Qual artefato prova que esta regra existe fora da cabeça do agente?
- Qual teste falharia se alguém removesse essa proteção amanhã?
- Qual trace mostraria que a proteção foi acionada em produção?
- Quem é o owner desta regra e quando ela foi revisada pela última vez?
- Qual é o custo em tokens, latência ou manutenção desta proteção?
- Qual falha real de cliente esta proteção previne?
- O que acontece quando a proteção rejeita um caso válido?
- O que acontece quando a proteção deixa passar um caso inválido?
- Como um novo dev descobriria essa regra sem perguntar para Fernando?
- A regra está no lugar certo ou deveria virar contrato, state, rubric ou guardrail?
- O harness prompt tem versionamento independente da política de contexto?
- Mudanças no harness passam pelo mesmo gate de regressão que mudanças de compactação?

### Micro-checklist de revisão rápida

- [ ] Cada componente esta marcado como BUILD, STABILIZE, SIMPLIFY ou REMOVE?
- [ ] Metricas mostram falhas reais prevenidas pelo componente?
- [ ] Tokens, latencia, manutencao e falsos positivos sao medidos?
- [ ] Componentes desnecessarios sao identificados e removidos?
- [ ] Simplificacao exige shadow test ou A/B sem regressao relevante?
- [ ] Remocao de guardrail critico tem rollback e aprovacao registrada?
- [ ] Feature flag ou versao anterior permite restaurar comportamento anterior?
- [ ] Mudanca estrutural tem ADR ou changelog com alternativas e consequencias?
- [ ] Revisao ocorre apos upgrade de modelo ou ciclo trimestral?
- [ ] Cada componente esta classificado como invariante de dominio ou compensacao de modelo?
- [ ] Compensacoes de modelo tem criterio de expiracao e gatilho de reavaliacao?
- [ ] Existe um ritual semanal (GC Day) para converter feedback humano em guardrails automatizados?
- [ ] Falhas e escapes sao classificados por taxonomia e convertidos em casos de regressao?
- [ ] Especialistas mantem documentos NFR por persona, e agentes herdam esse conhecimento automaticamente?
- [ ] O AGENTS.md e complementado por personas especializadas, nao substituido por elas?

### Critérios de bloqueio para esta categoria

- Bloqueie produção se a categoria afeta pagamento, saúde, dados pessoais ou promessa de entrega e não há validação objetiva.
- Bloqueie produção se o único argumento for “o modelo costuma acertar”.
- Bloqueie produção se não houver trace suficiente para explicar uma decisão errada depois do fato.
- Permita rollout limitado apenas quando o risco estiver documentado, monitorado e reversível.

### Sinais de maturidade crescente

- **Nível 1:** existe apenas intenção ou prompt informal.
- **Nível 2:** há regra documentada, mas pouca automação.
- **Nível 3:** há contrato, validação e teste principal.
- **Nível 4:** há métricas, replay e revisão periódica.
- **Nível 5:** há evolução contínua com custo, qualidade e remoção controlada.

---

## 📡 8. Observabilidade (Traces/Monitoring)

Esta categoria verifica se um harness bom permite responder rapidamente o que aconteceu, por que aconteceu e qual decisão deve mudar.

### O que um bom harness faz

- Traces conectam input, contexto, contrato, geração, avaliação, validação, fallback e output final.
- Audit logs registram decisões críticas com `correlation_id` e evidência.
- Dashboards mostram qualidade, custo, latência, falhas e drift de comportamento.
- Alertas disparam por sintomas de negócio e por sinais técnicos.
- Debugging surfaces são legíveis por humanos, não apenas por máquinas.

### Por que isso importa no KODA

KODA não vive em uma chamada isolada de LLM. Ele vive em conversas que atravessam minutos, horas, preferências, restrições, estoque, preço e confiança.

Quando a dimensão de observabilidade falha, o cliente não enxerga “um problema técnico”. Ele enxerga uma promessa quebrada.

Fernando ensina o time a procurar a falha antes do incidente: qual evidência existe, qual contrato protege a fronteira e qual trace provará o comportamento depois.

### Checklist PASS/FAIL

| Item | Critério | PASS | FAIL | Notas |
|------|----------|------|------|-------|
| Trace completo | Cada jornada possui trace com fases, timestamps, agent_id, input refs, output refs e decisão final. | Existe evidência verificável e atualizada. | Depende de memória, intenção, prompt solto ou comportamento não testado. | Registre link para artefato, owner e data. |
| Audit log crítico | Ações sobre pagamento, estoque, dados pessoais e promessa ao cliente entram em audit log imutável. | Existe evidência verificável e atualizada. | Depende de memória, intenção, prompt solto ou comportamento não testado. | Registre link para artefato, owner e data. |
| Dashboard operacional | Há métricas de latência, custo, aprovação de rubrica, fallback rate e error rate por feature. | Existe evidência verificável e atualizada. | Depende de memória, intenção, prompt solto ou comportamento não testado. | Registre link para artefato, owner e data. |
| Alertas acionáveis | Alertas têm threshold, owner, severidade e runbook com primeira ação clara. | Existe evidência verificável e atualizada. | Depende de memória, intenção, prompt solto ou comportamento não testado. | Registre link para artefato, owner e data. |
| Debug por replay | Engenheiro consegue abrir uma pasta ou registro e reproduzir a jornada com os artefatos salvos. | Existe evidência verificável e atualizada. | Depende de memória, intenção, prompt solto ou comportamento não testado. | Registre link para artefato, owner e data. |
| Correlação ponta a ponta | WhatsApp message id, session id, order id e trace id aparecem conectados. | Existe evidência verificável e atualizada. | Depende de memória, intenção, prompt solto ou comportamento não testado. | Registre link para artefato, owner e data. |
| Amostragem de qualidade | Conversas aprovadas também são amostradas para detectar falhas silenciosas. | Existe evidência verificável e atualizada. | Depende de memória, intenção, prompt solto ou comportamento não testado. | Registre link para artefato, owner e data. |
| Leitura de trace treinada | O time possui guia e exemplos de trace reading para incidentes comuns. | Existe evidência verificável e atualizada. | Depende de memória, intenção, prompt solto ou comportamento não testado. | Registre link para artefato, owner e data. |

### Evidências que um revisor deve pedir

- trace folder
- audit log
- dashboard screenshot ou config
- alert rules
- runbook de debugging

### Exemplo de falha típica

❌ Quando um cliente reclama, o time só tem logs soltos e precisa adivinhar qual agente gerou a decisão errada.

### Exemplo de desenho melhor

✅ O trace mostra que o Generator sugeriu SKU incorreto, o Evaluator marcou warning mas threshold permitiu, e o ajuste correto é mudar blocker da rubrica.

### Perguntas de auditoria

- Qual artefato prova que esta regra existe fora da cabeça do agente?
- Qual teste falharia se alguém removesse essa proteção amanhã?
- Qual trace mostraria que a proteção foi acionada em produção?
- Quem é o owner desta regra e quando ela foi revisada pela última vez?
- Qual é o custo em tokens, latência ou manutenção desta proteção?
- Qual falha real de cliente esta proteção previne?
- O que acontece quando a proteção rejeita um caso válido?
- O que acontece quando a proteção deixa passar um caso inválido?
- Como um novo dev descobriria essa regra sem perguntar para Fernando?
- A regra está no lugar certo ou deveria virar contrato, state, rubric ou guardrail?

### Micro-checklist de revisão rápida

- [ ] Trace permite reconstruir decisao sem reencenar o incidente?
- [ ] Cada jornada conecta input, contexto, contrato, geracao, avaliacao, guardrail e output?
- [ ] Audit log registra pagamento, estoque, dados pessoais e promessa ao cliente?
- [ ] Dashboard mostra latencia, custo, score de rubrica, fallback rate e error rate?
- [ ] Alertas tem threshold, severidade, owner e runbook com primeira acao?
- [ ] Replay de debug abre artefatos salvos e reproduz a jornada?
- [ ] WhatsApp message id, session id, order id e trace id aparecem correlacionados?
- [ ] Conversas aprovadas tambem sao amostradas para detectar falhas silenciosas?
- [ ] Guia de trace reading esta disponivel para incidentes comuns?

### Critérios de bloqueio para esta categoria

- Bloqueie produção se a categoria afeta pagamento, saúde, dados pessoais ou promessa de entrega e não há validação objetiva.
- Bloqueie produção se o único argumento for “o modelo costuma acertar”.
- Bloqueie produção se não houver trace suficiente para explicar uma decisão errada depois do fato.
- Permita rollout limitado apenas quando o risco estiver documentado, monitorado e reversível.

### Sinais de maturidade crescente

- **Nível 1:** existe apenas intenção ou prompt informal.
- **Nível 2:** há regra documentada, mas pouca automação.
- **Nível 3:** há contrato, validação e teste principal.
- **Nível 4:** há métricas, replay e revisão periódica.
- **Nível 5:** há evolução contínua com custo, qualidade e remoção controlada.

---

## 🔀 Tabela Comparativa de Estratégias de Coordenação

Coordenação não é apenas escolha técnica. Ela define como agentes compartilham verdade, como falhas são recuperadas e como o time debuga incidentes.

| Estratégia | Latência | Consistência | Complexidade | Failure modes comuns | Melhor uso |
|------------|----------|--------------|--------------|----------------------|------------|
| File-based coordination | Baixa a média; depende de disco e polling | Boa com lock file e atomic rename | Baixa | Arquivo parcial, lock preso, leitor processando versão antiga | Pipelines auditáveis, aprendizado, traces humanos |
| Message queue | Baixa; boa para eventos assíncronos | Boa com idempotência e ack correto | Média | Mensagem duplicada, ordering parcial, poison message | Alto volume, workers independentes, retries controlados |
| Database transaction | Baixa em queries simples; pode subir com lock contention | Forte quando usa transação ACID | Média | Deadlock, migração de schema ruim, `SQLITE_BUSY` ou lock prolongado | Estado relacional, pedidos, carrinhos, checkpoints |
| API orchestration síncrona | Média a alta; depende de rede e cadeia de chamadas | Variável; forte apenas com contrato e timeout | Média a alta | Timeout em cascata, retry duplicado, acoplamento forte | Integração com serviços externos e fronteiras bem definidas |
| Shared memory/cache | Muito baixa | Fraca sem persistência e locking externo | Baixa no começo, alta em produção | Perda em restart, estado invisível, race condition silenciosa | Cache temporário, nunca como fonte de verdade crítica |

### Como escolher

- Comece com file-based coordination quando auditabilidade e simplicidade são mais importantes que throughput.
- Use database transaction quando múltiplas entidades precisam mudar juntas ou quando queries de estado são frequentes.
- Use message queue quando há alto volume, retries independentes e workers desacoplados.
- Use API orchestration quando a fronteira é um serviço externo com contrato claro.
- Evite shared memory como fonte de verdade para jornada longa, porque ela falha exatamente quando o processo reinicia.

---

## 🧪 Exemplos Concretos: Bom Harness vs Harness Ruim

Os exemplos abaixo são pequenos de propósito. Em code review, falhas de harness aparecem em detalhes que parecem inocentes.

### Exemplo 1: Contexto sem orçamento vs contexto com token budget

❌ Harness ruim: envia tudo e torce para caber.

```python
def build_prompt(customer_message, full_history, catalog):
    return f"""
    Você é KODA, agente de vendas.
    Histórico completo: {full_history}
    Catálogo completo: {catalog}
    Cliente agora: {customer_message}
    Responda da melhor forma.
    """
```

Problemas objetivos:

- Não há token budget.
- Não há separação entre histórico recente e summary.
- Não há garantia de que alergias e compromissos comerciais sobrevivem ao corte.
- Não há trace mostrando por que cada bloco entrou no prompt.

✅ Bom harness: monta contexto por blocos auditáveis.

```python
def build_context(request, state, summaries, token_budget):
    blocks = [
        ContextBlock("critical_state", state.critical_customer_constraints),
        ContextBlock("active_contract", request.sprint_contract),
        ContextBlock("history_summary", summaries.current),
        ContextBlock("recent_window", request.recent_messages[-20:]),
        ContextBlock("turn_request", request.customer_message),
    ]
    planned = allocate_tokens(blocks, token_budget)
    if planned.total > token_budget.max_input_tokens:
        planned = compact_noncritical_blocks(planned)
    record_context_trace(request.trace_id, planned)
    return render_prompt(planned)
```

Melhorias objetivas:

- Cada bloco tem nome e motivo.
- O budget é calculado antes da chamada.
- Dados críticos ficam separados de histórico conversacional.
- O trace permite auditar o contexto usado em uma decisão.

### Exemplo 2: Avaliação subjetiva vs rubric com blockers

❌ Harness ruim: autoavaliação subjetiva.

```json
{
  "generator_prompt": "Recomende um suplemento e verifique se sua resposta está boa.",
  "acceptance_rule": "Se o agente disser que está bom, enviar para o cliente."
}
```

Problemas objetivos:

- Generator e Evaluator são a mesma entidade.
- Não há pesos ou thresholds.
- Não há blocker absoluto para alergia, estoque ou preço divergente.
- Não há evidência por dimensão.

✅ Bom harness: avaliação independente e bloqueios absolutos.

```json
{
  "rubric_version": "product_recommendation.v3",
  "threshold": 85,
  "dimensions": [
    {"name": "adequacao_ao_objetivo", "weight": 30},
    {"name": "restricoes_do_cliente", "weight": 30},
    {"name": "preco_e_estoque", "weight": 25},
    {"name": "clareza_da_mensagem", "weight": 15}
  ],
  "blockers": [
    "produto viola alergia ou restricao alimentar",
    "preco difere do catalogo atual",
    "produto fora de estoque na regiao prometida"
  ],
  "generator_can_self_approve": false
}
```

Melhorias objetivas:

- A decisão depende de score e blockers.
- O Evaluator tem função separada.
- A rubrica é versionada.
- A aprovação pode ser auditada depois.

### Exemplo 3: Coordenação sem lock vs status e atomic write

❌ Harness ruim: dois agentes escrevem no mesmo estado.

```python
def update_cart(session_id, item):
    cart = read_json(f"state/{session_id}/cart.json")
    cart["items"].append(item)
    write_json(f"state/{session_id}/cart.json", cart)
```

✅ Bom harness: lock, arquivo temporário e publicação atômica.

```python
def update_cart(session_id, item, agent_id):
    with acquire_lock(f"state/{session_id}/cart.lock.json", owner=agent_id, ttl_seconds=30):
        cart_path = f"state/{session_id}/cart.json"
        cart = read_json(cart_path)
        if item["sku"] not in [existing["sku"] for existing in cart["items"]]:
            cart["items"].append(item)
        cart["updated_by"] = agent_id
        atomic_write_json(cart_path, cart)
        write_json(f"state/{session_id}/cart.status.json", {"status": "completed", "agent_id": agent_id})
```

---

## 🚀 Aplicação no KODA: Usando a Checklist no Agente de WhatsApp

### História do problema

Fernando recebe um alerta de suporte: três clientes reclamaram que KODA recomendou produtos incompatíveis com restrições alimentares.

Nenhum caso gerou incidente médico, mas todos geraram perda de confiança.

O time abre os logs e encontra mensagens bonitas, educadas e aparentemente coerentes.

O problema não é tom de voz.

O problema é que KODA trata restrição alimentar como detalhe conversacional, não como constraint de sistema.

Em uma conversa curta, isso raramente falha.

Em uma conversa de duas horas, com comparações, carrinho, cupom e entrega, a restrição se perde entre blocos de contexto.

Além disso, o Evaluator usa uma rubrica genérica de “boa recomendação” e não tem blocker absoluto para alergia.

Fulfillment lê o pedido antes de a avaliação final terminar.

O dashboard mostra latência e volume, mas não mostra taxa de recomendações bloqueadas por restrição.

Esse é o tipo de problema que parece uma falha de prompt, mas é falha de harness.

### Como a checklist resolve

- **Contexto:** move alergias e restrições de conversa para `critical_state`, sempre injetado no prompt e no Evaluator.
- **Contratos:** exige que Product Discovery entregue `dietary_flags` e `contraindications` por SKU.
- **Avaliação:** adiciona blocker absoluto para qualquer recomendação que viole restrição confirmada.
- **Persistência:** salva restrições no perfil do cliente e checkpoint do carrinho antes de pagamento.
- **Coordenação:** impede Fulfillment de reservar estoque antes de `evaluation.decision == approved`.
- **Segurança & Guardrails:** valida resposta final antes do WhatsApp e exige confirmação quando há ambiguidade alimentar.
- **Evolução:** mede quantos bloqueios reais ocorrem para ajustar custo do guardrail sem removê-lo cedo demais.
- **Observabilidade:** cria dashboard de restrições detectadas, violações bloqueadas e falsos positivos.

### Exemplo de implementação

```json
{
  "session_id": "wa_2026_05_28_renata",
  "critical_state": {
    "customer_id": "cust_renata",
    "dietary_restrictions": [
      {
        "type": "intolerancia_lactose",
        "source_message_id": "wamid.001",
        "confidence": "confirmed",
        "expires": "never_for_session"
      }
    ],
    "budget_brl": {"max": 220, "source_message_id": "wamid.014"}
  },
  "sprint_contract": {
    "contract_id": "product_recommendation.v3",
    "inputs_required": ["critical_state", "catalog_snapshot", "recent_window"],
    "success_criteria": [
      "recommendation.score >= 85",
      "evaluation.decision == approved",
      "no_blockers_triggered"
    ]
  },
  "evaluation": {
    "rubric_version": "koda_recommendation_safety.v2",
    "blockers": [
      {
        "name": "violates_confirmed_dietary_restriction",
        "result": "pass",
        "evidence": "SKU vegan_protein_42 has lactose_free=true"
      }
    ]
  }
}
```

### Impacto esperado

- Redução de recomendações incompatíveis com restrição alimentar.
- Menos retrabalho de suporte porque o trace mostra onde cada decisão foi tomada.
- Maior confiança do cliente em conversas longas.
- Menor risco de pedido incorreto chegar ao Fulfillment.
- Melhor onboarding para novos devs, porque as regras estão em contratos e rubrics, não apenas em prompts.

### Checklist KODA específica

- [ ] Cliente informou alergia, intolerância ou restrição alimentar? Então o dado aparece em `critical_state`.
- [ ] O Product Discovery retorna `dietary_flags` para cada SKU recomendado.
- [ ] O Evaluator possui blocker absoluto para violação de restrição confirmada.
- [ ] O Order Agent só cria pedido após avaliação aprovada.
- [ ] O Fulfillment Agent só reserva estoque após pedido aprovado e idempotente.
- [ ] A mensagem WhatsApp final cita a restrição quando ela influenciou a recomendação.
- [ ] O trace conecta WhatsApp message id, recommendation id, evaluation id e order id.
- [ ] O dashboard mede taxa de bloqueio por restrição e falsos positivos revisados por humano.
- [ ] O loop de operação lê artifacts reais, sugere próximo trabalho e registra feedback em memória operacional, conforme [[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent Operating System]].
- [ ] Todo workflow recorrente promovido a skill passou por tests, evals, resolver trigger, check-resolvable, smoke test e schema, conforme [[docs/canonical/skill-resolver-skillify-capability-pipeline|Skillify Pipeline]].

---

## 🧾 Roteiro de Auditoria em 90 Minutos

Quando o time estiver com pouco tempo, use este roteiro. Ele não substitui a leitura completa, mas força as perguntas que mais capturam risco.

- **Minutos 0-10:** Definir feature, jornada, risco máximo e artefatos disponíveis.
- **Minutos 10-20:** Ler contexto montado para uma chamada real e verificar token budget.
- **Minutos 20-30:** Ler sprint contract e confirmar inputs, outputs, success criteria e failure modes.
- **Minutos 30-40:** Ler rubric e procurar thresholds, weights, blockers e evidência por dimensão.
- **Minutos 40-50:** Abrir state/checkpoints e simular onde a jornada retomaria após crash.
- **Minutos 50-60:** Verificar coordenação: locks, status files, idempotência e ordem de execução.
- **Minutos 60-70:** Revisar guardrails: input, output, constraints, budget e fallback.
- **Minutos 70-80:** Abrir trace real e tentar explicar uma decisão do início ao fim.
- **Minutos 80-90:** Atribuir score, registrar FAILs, decidir go/no-go e donos.

### Resultado mínimo da auditoria

- Lista de PASS/FAIL por categoria.
- Pelo menos uma evidência por PASS importante.
- Dono e data para cada FAIL.
- Decisão explícita de produção: aprovado, aprovado com monitoramento, rollout limitado ou bloqueado.
- Riscos aceitos por produto e engenharia, não escondidos no texto do PR.

---

## 🔗 Vínculos com Módulos do Currículo

| Tema deste guia | Módulo relacionado | Como usar junto |
|-----------------|--------------------|-----------------|
| Fundação de harness | `../01-nivel-1-fundamentals/03-basic-harness-patterns.md` | Releia para entender por que o harness existe ao redor do modelo. |
| Falhas de contexto | `../01-nivel-1-fundamentals/01-why-agents-lose-plot.md` | Use para explicar Context Amnesia e degradação em conversas longas. |
| Token budget | `../01-nivel-1-fundamentals/02-token-budgeting.md` | Use antes de revisar context windows e compaction. |
| Generator/Evaluator | `../02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md` | Use para aprofundar separação entre criação e avaliação. |
| Sprint Contracts | `../02-nivel-2-practical-patterns/02-sprint-contracts.md` | Use para desenhar interfaces e critérios de sucesso. |
| Rubric Design | `../02-nivel-2-practical-patterns/03-rubric-design.md` | Use para transformar qualidade em pesos, thresholds e blockers. |
| Trace Reading | `../02-nivel-2-practical-patterns/04-trace-reading.md` | Use para treinar leitura de evidências após incidentes. |
| State Persistence | `../03-nivel-3-advanced-architecture/02-state-persistence.md` | Use para recovery, checkpoints, replay e backend de estado. |
| File-Based Coordination | `../03-nivel-3-advanced-architecture/03-file-based-coordination.md` | Use para lock files, status files, JSON protocol e atomic writes. |
| Harness Evolution | `../03-nivel-3-advanced-architecture/05-harness-evolution.md` | Use para BUILD/STABILIZE/SIMPLIFY/REMOVE e remoção segura. |
| Aplicações KODA Nível 2 | `../02-nivel-2-practical-patterns/koda-applications/nivel-2-koda.md` | Use para conectar padrões práticos à jornada real do KODA. |
| LLM as Fuzzy Compiler | [[docs/canonical/llm-as-fuzzy-compiler|LLM as Fuzzy Compiler]] | Use para classificar componentes como invariante vs compensacao e decidir o que sobrevive a upgrades de modelo. |
| Garbage Collection Day | [[docs/canonical/garbage-collection-day-meta-loop|Garbage Collection Day Meta-Loop]] | Use para implementar o ritual semanal de conversao de feedback humano em guardrails. |
| Failure Pattern Classification | [[docs/canonical/failure-pattern-classification-loop|Failure Pattern Classification Loop]] | Use para classificar falhas por taxonomia e converter em casos de regressao. |
| Persona-Based Documentation | [[docs/canonical/persona-based-documentation|Persona-Based Documentation]] | Use para estruturar documentos NFR por especialidade e multiplicar conhecimento entre agentes. |

---

## 🎓 O Que Você Aprendeu

Você agora tem uma forma objetiva de avaliar harness quality. O ponto central é simples: um agente confiável não depende apenas de um modelo forte. Ele depende de fronteiras, contratos, avaliações, estado, coordenação, guardrails, evolução e observabilidade.

### Takeaways principais

- Contexto é orçamento, não depósito infinito.
- State durável é onde ficam compromissos que não podem ser esquecidos.
- Summary é uma representação comprimida, não fonte de verdade para dados críticos.
- Sprint contract transforma intenção em promessa verificável.
- Rubric boa tem pesos, thresholds, blockers e evidência por dimensão.
- Generator não deve aprovar o próprio trabalho quando há risco real.
- Checkpoint não é detalhe operacional; é respeito ao tempo do cliente.
- Coordenação multi-agent precisa de protocolo, lock, status e idempotência.
- Guardrails bons falham fechado em saúde, pagamento, dados pessoais e promessa comercial.
- Harness evolution impede que proteções antigas virem complexidade morta.
- Observabilidade boa permite explicar uma decisão sem reencenar o incidente inteiro.
- KODA precisa de harness porque vendas via WhatsApp misturam conversa humana com ações de negócio irreversíveis.

### Self-check

- [ ] Consigo explicar a diferença entre context window, state e summary.
- [ ] Consigo apontar onde um sprint contract começa e termina.
- [ ] Consigo revisar uma rubrica e identificar se falta blocker absoluto.
- [ ] Consigo verificar se um estado pode ser recuperado após crash.
- [ ] Consigo encontrar risco de race condition em um fluxo multi-agent.
- [ ] Consigo diferenciar fallback seguro de retry cego.
- [ ] Consigo decidir quando um componente de harness está em BUILD, STABILIZE, SIMPLIFY ou REMOVE.
- [ ] Consigo abrir um trace e reconstruir a decisão final do agente.
- [ ] Consigo aplicar a checklist ao KODA sem depender de opinião subjetiva.
- [ ] Consigo registrar FAILs como riscos concretos, com owner e evidência necessária.

---

## 📚 Apêndice A: Cartões de Auditoria Detalhados

Use estes cartões durante uma revisão real. Cada cartão força uma pergunta objetiva, uma evidência e uma decisão. Eles existem para evitar que a checklist vire conversa abstrata.

Em vez de quatro cartões mecanicamente iguais por foco, cada categoria agora tem cartões substantivos que combinam evidência, teste, trace e ownership quando isso muda a decisão de auditoria.

### 🧠 Cartões de auditoria - Contexto (Context Management)

#### Cartão A1: Fontes de contexto e orçamento por chamada

**Pergunta objetiva:** A chamada mostra exatamente quais fontes entraram no prompt e quanto do token budget cada bloco consumiu?

**Evidência aceitável:**
- trace de prompt com secoes nomeadas para system, critical_state, history_summary, recent_window, catalogo e turn_request
- relatorio de tokens planejados e reais por bloco
- politica versionada de entrada, permanencia e expiracao de contexto
- exemplo de chamada longa do KODA com corte ou compactacao registrado

**PASS:** o revisor localiza uma chamada real, confere fontes e tokens por bloco, e entende por que cada bloco entrou sem depender de explicacao oral.

**FAIL:** o prompt aparece como texto unico, historico completo ou colecao de mensagens sem budget, sem fonte e sem motivo auditavel.

**Verificação em 30 segundos:**
- Abra um trace real de conversa longa.
- Confira se `critical_state` aparece separado de historico recente.
- Compare tokens planejados contra tokens reais.
- Procure registro de bloco removido, compactado ou mantido.
- Confirme que catalogo e contrato entram por referencia versionada.
- Verifique se o limite e aplicado antes da chamada ao modelo.

**Perguntas de follow-up quando houver dúvida:**
- Qual informacao critica ficaria fora se o historico crescesse mais 30 minutos?
- Qual teste falha quando alguem remove a medicao de tokens?
- Quem revisa a politica quando o modelo ou limite de contexto muda?
- A regra pertence ao contexto ou deveria virar state duravel?

**Ação recomendada:** registre o menor artefato verificável que transforma a resposta em PASS ou declare risco aceito com owner e data.

#### Cartão A2: Recall de restricoes e compactacao segura

**Pergunta objetiva:** Uma restricao dita cedo pelo cliente sobrevive a resumo, corte de janela e turnos posteriores?

**Evidência aceitável:**
- teste automatizado de conversa longa com alergia, orcamento ou preferencia declarada no inicio
- summary JSON com campos separados para restricoes, decisoes, preferencias e pendencias
- state duravel apontando source_message_id da restricao
- trace do Evaluator recebendo a restricao no momento da recomendacao

**PASS:** a restricao antiga reaparece em state, prompt e avaliacao quando afeta a decisao, e o teste mostra falha se ela for esquecida.

**FAIL:** a restricao existe apenas em historico bruto, resumo narrativo ou memoria do agente, sem teste que proteja contra esquecimento.

**Verificação em 30 segundos:**
- Busque uma restricao alimentar no inicio do trace.
- Verifique se ela foi promovida para `critical_state`.
- Abra o summary e confira campo dedicado, nao texto solto.
- Confirme que o Evaluator usa a mesma restricao.
- Execute mentalmente o que acontece se a janela recente nao inclui a mensagem original.
- Cheque se ha owner para politica de promocao para state.

**Perguntas de follow-up quando houver dúvida:**
- A compactacao preserva a evidencia original ou apenas a conclusao?
- O que acontece quando summary e state entram em conflito?
- Qual alerta indica perda de recall critico em producao?
- Qual custo adicional essa protecao adiciona?

**Ação recomendada:** registre o menor artefato verificável que transforma a resposta em PASS ou declare risco aceito com owner e data.

---

### 📜 Cartões de auditoria - Contratos (Contracts/Sprint Contracts)

#### Cartão A3: Interface contratual executavel

**Pergunta objetiva:** Cada etapa declara inputs, outputs, schema_version e criterios de sucesso antes de executar trabalho caro?

**Evidência aceitável:**
- sprint_contract.json ou documento equivalente versionado
- schema de input e output com campos obrigatorios, tipos e exemplos
- teste de contrato cobrindo input minimo valido e input invalido
- trace mostrando o contrato usado por Planner, Generator ou Evaluator

**PASS:** um revisor consegue validar a fronteira sem ler codigo interno e encontra criterio objetivo para iniciar e concluir a etapa.

**FAIL:** a etapa depende de combinacao informal de prompt, comentario em PR ou conhecimento do autor sobre campos esperados.

**Verificação em 30 segundos:**
- Abra o contrato da feature revisada.
- Marque inputs obrigatorios e pre-condicoes.
- Marque outputs, tipos e exemplos.
- Confira `schema_version` e owner.
- Procure criterio de sucesso objetivo.
- Confirme que teste falha com campo critico ausente.

**Perguntas de follow-up quando houver dúvida:**
- Qual consumidor quebra se este output mudar?
- O contrato define unidade de preco, moeda e disponibilidade?
- Como uma versao antiga e rejeitada ou migrada?
- A fronteira esta no contrato certo ou vazou para prompt?

**Ação recomendada:** registre o menor artefato verificável que transforma a resposta em PASS ou declare risco aceito com owner e data.

#### Cartão A4: Falha e mudanca de contrato controladas

**Pergunta objetiva:** O contrato explica como falhar, recuperar e auditar alteracoes de interface?

**Evidência aceitável:**
- lista de failure modes para input invalido, timeout, dependencia indisponivel e output fora do schema
- fallback ou stop condition por modo de falha
- ADR, issue ou changelog para mudanca relevante de contrato
- trace ou log registrando contrato rejeitado e motivo

**PASS:** a falha prevista produz estado seguro, mensagem auditavel e dono claro; mudancas de contrato tem motivo e impacto registrados.

**FAIL:** falhas sao tratadas por retry cego, excecao generica ou conversa oral, e mudancas de campo nao deixam rastro.

**Verificação em 30 segundos:**
- Leia a secao de failure handling.
- Procure timeout e dependencia externa indisponivel.
- Verifique se output fora do schema bloqueia a etapa.
- Confira owner de manutencao do contrato.
- Ache uma mudanca recente e seu motivo.
- Confirme que o trace registra rejeicao de contrato.

**Perguntas de follow-up quando houver dúvida:**
- O que acontece se Product Discovery entrega preco em string?
- Quem aprova quebra de compatibilidade?
- A falha pausa a jornada ou deixa Fulfillment continuar?
- Qual cliente seria afetado por aceitar output parcial?

**Ação recomendada:** registre o menor artefato verificável que transforma a resposta em PASS ou declare risco aceito com owner e data.

---

### ⚖️ Cartões de auditoria - Avaliação (Evaluation/Rubrics)

#### Cartão A5: Rubrica com dimensoes, pesos e blockers

**Pergunta objetiva:** A decisao de qualidade combina score ponderado com blockers absolutos para riscos criticos?

**Evidência aceitável:**
- rubric.md ou JSON com dimensoes nomeadas e pesos que somam 100%
- threshold operacional explicito
- blockers para alergia, preco divergente, estoque ausente, pagamento duplicado ou acao insegura
- evaluation.json real com score por dimensao

**PASS:** a avaliacao reprova automaticamente uma violacao critica mesmo quando o score agregado e alto.

**FAIL:** a avaliacao usa nota unica, julgamento subjetivo ou autoaprovacao do Generator sem blockers verificaveis.

**Verificação em 30 segundos:**
- Some os pesos da rubrica.
- Confirme threshold minimo.
- Procure lista de blockers absolutos.
- Abra uma avaliacao real.
- Verifique score por dimensao.
- Simule violacao de alergia com score alto.

**Perguntas de follow-up quando houver dúvida:**
- Qual blocker teria evitado o incidente da Renata?
- O score agregado pode mascarar risco de saude ou pagamento?
- Quem calibrou os pesos?
- Qual evidencia sustenta cada dimensao?

**Ação recomendada:** registre o menor artefato verificável que transforma a resposta em PASS ou declare risco aceito com owner e data.

#### Cartão A6: Independencia, evidencia e calibracao do Evaluator

**Pergunta objetiva:** O Evaluator julga com evidencias externas ao Generator e e calibrado contra exemplos reais?

**Evidência aceitável:**
- trace separando Generator e Evaluator
- evaluation.json com citacao de campo, trace ref ou dado de catalogo por dimensao
- calibration set com casos aprovados, reprovados e limitrofes
- relatorio de falsos positivos e falsos negativos revisado por humano

**PASS:** o Evaluator recebe output e evidencias, produz justificativa auditavel por dimensao e tem calibracao periodica documentada.

**FAIL:** o Generator aprova o proprio trabalho ou o Evaluator aceita justificativa do Generator como prova suficiente.

**Verificação em 30 segundos:**
- Confira se Generator e Evaluator sao etapas separadas.
- Abra evidencias usadas em uma nota.
- Veja se ha exemplos limitrofes.
- Procure revisao humana de falso negativo.
- Confirme replay de avaliacao.
- Compare decisao atual com rubrica versionada.

**Perguntas de follow-up quando houver dúvida:**
- A avaliacao e reproduzivel sobre o mesmo output?
- Que caso aprovado virou incidente depois?
- O Evaluator acessa catalogo atual ou apenas texto gerado?
- Qual dimensao mais diverge da revisao humana?

**Ação recomendada:** registre o menor artefato verificável que transforma a resposta em PASS ou declare risco aceito com owner e data.

---

### 💾 Cartões de auditoria - Persistência (State Persistence)

#### Cartão A7: Checkpoint, schema e recovery real

**Pergunta objetiva:** O estado critico fica salvo em formato versionado e a jornada retoma corretamente apos crash?

**Evidência aceitável:**
- state files ou tabelas com `schema_version`, timestamps, owner e campos obrigatorios
- checkpoint log antes e depois de acoes caras ou irreversiveis
- teste que mata o processo e retoma do ultimo checkpoint
- procedimento de restore documentado

**PASS:** o revisor consegue identificar ultimo checkpoint valido e demonstrar como o processo retoma sem perder carrinho, restricoes ou avaliacao.

**FAIL:** estado critico vive apenas em memoria, variavel de worker ou historico conversacional sem recovery testado.

**Verificação em 30 segundos:**
- Abra um state real de sessao.
- Confira schema_version e timestamps.
- Localize checkpoint antes de pagamento ou estoque.
- Leia o teste de crash.
- Verifique owner do schema.
- Confirme que restart nao apaga carrinho ou restricao.

**Perguntas de follow-up quando houver dúvida:**
- Qual campo minimo permite retomar a jornada?
- O que acontece se o deploy reinicia entre avaliacao e pedido?
- Quem migra schema antigo?
- Qual dado pessoal deve expirar?

**Ação recomendada:** registre o menor artefato verificável que transforma a resposta em PASS ou declare risco aceito com owner e data.

#### Cartão A8: Replay, atomicidade e backend escolhido

**Pergunta objetiva:** Os artefatos persistidos permitem replay auditavel e escrita segura sob falha parcial?

**Evidência aceitável:**
- replay script ou modo diagnostico com inputs salvos
- trace com refs para plan, generation, evaluation, status e outputs
- implementacao ou padrao documentado de write `.tmp` seguido de rename atomico
- ADR justificando files, SQLite, Redis ou banco remoto por volume, concorrencia e auditabilidade

**PASS:** uma decisao pode ser reconstruida com artefatos salvos e nenhum leitor consome estado parcial.

**FAIL:** replay exige memoria do time, logs soltos ou reexecucao manual; arquivos podem ficar parcialmente escritos.

**Verificação em 30 segundos:**
- Abra pasta de trace de uma sessao.
- Siga refs ate cada artefato persistido.
- Confirme escrita atomica no padrao usado.
- Verifique se leitores ignoram `.tmp`.
- Leia justificativa do backend.
- Procure evidencia de restore ou replay recente.

**Perguntas de follow-up quando houver dúvida:**
- O backend suporta concorrencia atual?
- Que artefato falta para reproduzir uma decisao?
- Como detectar arquivo parcial?
- Backup foi restaurado ou apenas configurado?

**Ação recomendada:** registre o menor artefato verificável que transforma a resposta em PASS ou declare risco aceito com owner e data.

---

### 🤝 Cartões de auditoria - Coordenação (Multi-Agent Coordination)

#### Cartão A9: Escrita compartilhada sem race condition

**Pergunta objetiva:** Agentes que alteram carrinho, pedido, perfil ou estoque usam lock, transacao ou fila serializadora?

**Evidência aceitável:**
- lock.json com owner, recurso, timestamp e TTL
- teste concorrente disparando dois agentes sobre o mesmo recurso
- codigo ou documento de atomic publish
- trace mostrando aquisicao, escrita e liberacao do lock

**PASS:** duas execucoes concorrentes preservam consistencia e o trace mostra qual agente escreveu primeiro.

**FAIL:** agentes escrevem no mesmo arquivo, pedido ou carrinho por timing favoravel sem bloqueio verificavel.

**Verificação em 30 segundos:**
- Identifique recurso compartilhado.
- Procure lock, transacao ou fila.
- Confira TTL e owner.
- Abra teste concorrente.
- Verifique idempotencia do reprocessamento.
- Confirme que output final nao aparece parcial.

**Perguntas de follow-up quando houver dúvida:**
- Qual race condition duplicaria pedido?
- O lock preso tem recuperacao segura?
- Reprocessar webhook duplica estoque reservado?
- O teste falha sem lock?

**Ação recomendada:** registre o menor artefato verificável que transforma a resposta em PASS ou declare risco aceito com owner e data.

#### Cartão A10: Protocolo, status e ordem entre agentes

**Pergunta objetiva:** A colaboracao multi-agent segue protocolo explicito de status, dependencias e ids correlacionados?

**Evidência aceitável:**
- status files com `pending`, `running`, `completed` ou `failed` e motivo
- schema de protocolo com `correlation_id`, `agent_id`, `schema_version` e `audit_refs`
- grafo ou contrato de dependencias entre Planner, Generator, Evaluator, Order e Fulfillment
- trace ponta a ponta mostrando ordem real

**PASS:** um novo dev consegue prever quem pode ler, escrever e prosseguir em cada fase, e o trace confirma a ordem executada.

**FAIL:** agentes descobrem progresso por polling informal, nomes de arquivo soltos ou suposicao de que outro agente ja terminou.

**Verificação em 30 segundos:**
- Abra o status atual da jornada.
- Confira timestamps e motivo de falha.
- Leia schema do protocolo JSON.
- Verifique dependencia Fulfillment apos avaliacao aprovada.
- Siga correlation_id em todo trace.
- Procure audit refs nos handoffs.

**Perguntas de follow-up quando houver dúvida:**
- Quem decide que a etapa esta completa?
- O que impede Fulfillment antes de Evaluation?
- Como um agente reage a status `failed`?
- O protocolo mudou sem versionamento?

**Ação recomendada:** registre o menor artefato verificável que transforma a resposta em PASS ou declare risco aceito com owner e data.

---

### 🛡️ Cartões de auditoria - Segurança & Guardrails

#### Cartão A11: Validacao de entrada, saida e constraints

**Pergunta objetiva:** Dados externos e respostas finais passam por validacao objetiva antes de influenciar prompt ou cliente?

**Evidência aceitável:**
- schemas de webhook, mensagem e tool result
- validator logs de input e output
- constraint checker para alergia, orcamento, regiao, estoque e catalogo
- casos de teste de prompt injection e output invalido

**PASS:** inputs invalidos sao rejeitados antes do prompt e outputs perigosos sao bloqueados antes do WhatsApp ou acao externa.

**FAIL:** cliente, tool output ou texto gerado entram sem delimitacao e a resposta final depende de bom comportamento do modelo.

**Verificação em 30 segundos:**
- Abra schema de entrada.
- Confira limite de tamanho.
- Procure delimitacao de conteudo nao confiavel.
- Veja validacao contra catalogo.
- Confirme checker de restricoes do cliente.
- Leia log de uma rejeicao real.

**Perguntas de follow-up quando houver dúvida:**
- O cliente pode redefinir instrucao de sistema?
- Produto fora de estoque passa pela validacao?
- A mensagem final cita dado medico sem checagem?
- Qual teste cobre prompt injection?

**Ação recomendada:** registre o menor artefato verificável que transforma a resposta em PASS ou declare risco aceito com owner e data.

#### Cartão A12: Falha fechada, fallback e acoes irreversiveis

**Pergunta objetiva:** Guardrails bloqueiam ou pausam quando o risco envolve pagamento, dados pessoais, saude, estoque ou promessa comercial?

**Evidência aceitável:**
- policy de guardrails com fail-closed para riscos criticos
- fallback handlers especificos para confirmacao, humano ou pausa
- budget guard para tokens, retries, tool calls e duracao
- audit log de aprovacao antes de pagamento, estoque ou envio ao cliente

**PASS:** acoes irreversiveis so executam depois de aprovacao validada; falhas conhecidas entram em fallback seguro e rastreavel.

**FAIL:** o harness tenta de novo cegamente, envia resposta parcial ou executa pagamento/estoque sem aprovacao final.

**Verificação em 30 segundos:**
- Procure regra fail-closed.
- Abra fallback de restricao ambigua.
- Confira limites de budget.
- Verifique aprovacao antes de pagamento.
- Leia audit log de acao irreversivel.
- Confirme owner de cada guardrail critico.

**Perguntas de follow-up quando houver dúvida:**
- Fallback informa risco ao cliente ou esconde incerteza?
- Retry pode multiplicar pagamento?
- Budget guard para a jornada toda existe?
- Qual guardrail falharia se removido amanha?

**Ação recomendada:** registre o menor artefato verificável que transforma a resposta em PASS ou declare risco aceito com owner e data.

---

### 🧬 Cartões de auditoria - Evolução (Harness Evolution)

#### Cartão A13: Fase, efetividade e custo do componente

**Pergunta objetiva:** Cada protecao do harness tem fase declarada, metricas de efetividade e custo operacional medido?

**Evidência aceitável:**
- inventario de componentes com BUILD, STABILIZE, SIMPLIFY ou REMOVE
- dashboard de falhas reais prevenidas, falsos positivos e falsos negativos
- medicao de tokens, latencia, manutencao e onboarding
- owner e data da ultima revisao

**PASS:** o time sabe quais componentes ainda estao provando valor, quais custam caro e quais precisam estabilizar ou simplificar.

**FAIL:** componentes antigos continuam por inercia, sem metricas de beneficio, custo ou dono atual.

**Verificação em 30 segundos:**
- Abra inventario de harness.
- Confira fase atual.
- Veja metrica de falha prevenida.
- Compare custo de tokens e latencia.
- Procure owner e ultima revisao.
- Identifique componente sem uso recente.

**Perguntas de follow-up quando houver dúvida:**
- Qual componente virou peso morto apos upgrade de modelo?
- O custo de onboarding justifica a protecao?
- Que metrica cairia se removermos este nivel?
- Quem decide transicao de fase?

**Ação recomendada:** registre o menor artefato verificável que transforma a resposta em PASS ou declare risco aceito com owner e data.

#### Cartão A14: Simplificacao, remocao e rollback seguro

**Pergunta objetiva:** Simplificar ou remover uma protecao exige evidencia, experimento controlado e volta segura?

**Evidência aceitável:**
- criterio de simplificacao com periodo minimo e shadow test ou A/B controlado
- plano de rollback por feature flag, versao anterior ou procedimento testado
- ADR ou changelog explicando contexto, alternativas e consequencias
- aprovacao registrada para remover guardrail critico

**PASS:** a remocao so ocorre depois de evidencia comparativa e pode ser revertida rapidamente sem perder auditabilidade.

**FAIL:** o time remove guardrail porque parece redundante, sem shadow mode, sem rollback e sem registro de risco aceito.

**Verificação em 30 segundos:**
- Leia criterio de remocao.
- Verifique resultado de shadow test.
- Confirme feature flag ou rollback.
- Abra ADR da mudanca.
- Procure aprovacao para guardrail critico.
- Cheque monitoramento pos-remocao.

**Perguntas de follow-up quando houver dúvida:**
- Qual regressao o shadow mode detectaria?
- Quem pode reativar a protecao?
- A remocao muda contrato ou rubrica?
- Qual alerta acompanha o rollout?

**Ação recomendada:** registre o menor artefato verificável que transforma a resposta em PASS ou declare risco aceito com owner e data.

---

### 📡 Cartões de auditoria - Observabilidade (Traces/Monitoring)

#### Cartão A15: Trace reconstrutivel de ponta a ponta

**Pergunta objetiva:** O trace permite explicar o que aconteceu, por que aconteceu e qual fronteira decidiu?

**Evidência aceitável:**
- trace com fases, timestamps, agent_id, input refs, output refs e decisao final
- correlacao entre WhatsApp message id, session id, order id e trace id
- refs para contexto, contrato, geracao, avaliacao, guardrail, fallback e output
- exemplo de incidente reconstruido sem reencenar a jornada

**PASS:** um revisor reconstrói a decisao final abrindo artefatos e refs, sem depender de memoria do autor ou rerun do modelo.

**FAIL:** logs sao soltos, incompletos ou centrados em texto do modelo, sem conectar entrada, avaliacao, validacao e acao final.

**Verificação em 30 segundos:**
- Abra trace de uma jornada real.
- Siga correlation_id entre sistemas.
- Localize contexto usado na chamada.
- Abra contrato e avaliacao referenciados.
- Confira guardrail ou fallback acionado.
- Explique a decisao final em uma frase.

**Perguntas de follow-up quando houver dúvida:**
- Qual parte do trace aponta a causa raiz?
- O incidente pode ser debugado sem repetir chamada ao modelo?
- A decisao errada veio de contexto, rubrica ou guardrail?
- Qual artefato faltaria em auditoria externa?

**Ação recomendada:** registre o menor artefato verificável que transforma a resposta em PASS ou declare risco aceito com owner e data.

#### Cartão A16: Monitoramento acionavel e aprendizagem operacional

**Pergunta objetiva:** Dashboards, alertas e amostragem mostram qualidade, custo, risco e drift de comportamento?

**Evidência aceitável:**
- dashboard com latencia, custo, aprovacao de rubrica, fallback rate, error rate e metricas de negocio
- alert rules com threshold, severidade, owner e runbook
- audit log imutavel para pagamento, estoque, dados pessoais e promessa ao cliente
- amostragem de conversas aprovadas e guia de trace reading para o time

**PASS:** alertas orientam primeira acao, dashboards mostram sintomas tecnicos e de negocio, e amostras aprovadas detectam falhas silenciosas.

**FAIL:** observabilidade mede apenas volume e latencia, sem qualidade, guardrails, owner de alerta ou aprendizado pos-incidente.

**Verificação em 30 segundos:**
- Abra dashboard da feature.
- Veja fallback rate e score de rubrica.
- Confira alerta com owner.
- Leia runbook da primeira acao.
- Procure amostra de conversas aprovadas.
- Verifique guia de trace reading.

**Perguntas de follow-up quando houver dúvida:**
- Qual alerta teria pego recomendacao com lactose?
- Quem acorda quando fallback sobe?
- Dashboards separam falha tecnica de risco ao cliente?
- Como findings viram melhoria de rubrica ou contrato?

**Ação recomendada:** registre o menor artefato verificável que transforma a resposta em PASS ou declare risco aceito com owner e data.

---

### Matriz complementar de evidências para os cartões

Use esta matriz para registrar achados sem recriar cartões duplicados. Ela mantém a revisão objetiva: sinais de risco, campos mínimos de evidência e decisão esperada por categoria.

#### Contexto - sinais de risco que mudam a decisão

- Fonte ausente no prompt apesar de estar no contrato ativo.
- Token budget calculado depois da chamada ao modelo.
- Resumo narrativo misturando restricao critica com conversa casual.
- State e summary discordando sobre alergia, orcamento ou endereco.
- Trace sem motivo para remover bloco antigo.
- Catalogo inteiro enviado sem recorte por necessidade.
- Janela recente cortada por quantidade fixa sem registro de tokens.
- Owner da politica de contexto inexistente ou desatualizado.
- Teste de conversa longa sem restricao dita no inicio.
- Critical_state montado, mas nao entregue ao Evaluator.
- Mensagem antiga usada como verdade mesmo depois de correcao do cliente.
- Compactacao que perde source_message_id da evidencia original.

#### Contexto - campos mínimos para registrar PASS ou FAIL

- trace_id da chamada revisada
- budget planejado e budget real por bloco
- lista de fontes aceitas no prompt
- regra de promocao para state duravel
- teste que falha quando restricao antiga some
- owner da politica de contexto
- data da ultima revisao do limite de contexto
- exemplo de bloco compactado com motivo
- campo do state que guarda restricao critica
- acao tomada quando o budget estoura

#### Contexto - decisão de auditoria

- Marque PASS somente quando a evidência existir fora da conversa oral.
- Marque FAIL quando o comportamento depender de intenção, prompt solto ou sorte operacional.
- Marque RISCO ACEITO apenas com owner, impacto, prazo e monitoramento explícitos.
- Reabra o cartão se a evidência estiver certa, mas estiver no lugar arquitetural errado.

#### Contratos - sinais de risco que mudam a decisão

- Campo obrigatorio usado por consumidor mas ausente do schema.
- Preco sem unidade clara, como centavos, reais ou string formatada.
- Contrato sem success criteria objetivo.
- Output parcial aceito como se fosse completo.
- Falha de dependencia tratada como retry infinito.
- Mudanca de schema sem versionamento ou changelog.
- Owner de contrato confundido com owner do codigo.
- Boundary test cobrindo apenas caminho feliz.
- Planner e Generator compartilhando suposicoes nao documentadas.
- Fulfillment consumindo contrato antes de avaliacao aprovada.
- Exemplo valido desatualizado em relacao ao schema atual.
- Contrato permitindo campo livre onde deveria haver enum.

#### Contratos - campos mínimos para registrar PASS ou FAIL

- contract_id e schema_version
- inputs obrigatorios e pre-condicoes
- outputs obrigatorios e exemplos validos
- criterio de conclusao da etapa
- failure modes explicitamente listados
- teste de input invalido
- teste de output fora do schema
- owner da interface
- issue ou ADR de mudanca recente
- consumidor principal do contrato

#### Contratos - decisão de auditoria

- Marque PASS somente quando a evidência existir fora da conversa oral.
- Marque FAIL quando o comportamento depender de intenção, prompt solto ou sorte operacional.
- Marque RISCO ACEITO apenas com owner, impacto, prazo e monitoramento explícitos.
- Reabra o cartão se a evidência estiver certa, mas estiver no lugar arquitetural errado.

#### Avaliação - sinais de risco que mudam a decisão

- Score unico sem dimensoes auditaveis.
- Pesos que nao somam 100%.
- Blocker critico descrito em texto, mas nao implementado na decisao.
- Generator julgando o proprio output.
- Evaluator aceitando justificativa do Generator como evidencia.
- Alergia tratada como penalidade leve em vez de reprovação absoluta.
- Rubrica sem exemplos limitrofes.
- Calibracao feita uma vez e esquecida.
- Replay impossivel porque evidencias nao foram salvas.
- Falso negativo sem dono para ajuste de rubrica.
- Threshold alterado sem impacto medido.
- Output aprovado sem citar dado de catalogo usado na nota.

#### Avaliação - campos mínimos para registrar PASS ou FAIL

- rubric_version aplicada
- dimensoes e pesos
- threshold minimo
- lista de blockers absolutos
- evaluation_id do caso revisado
- evidencia por dimensao
- separacao entre Generator e Evaluator
- calibration set usado
- resultado de replay
- ultimo falso negativo revisado

#### Avaliação - decisão de auditoria

- Marque PASS somente quando a evidência existir fora da conversa oral.
- Marque FAIL quando o comportamento depender de intenção, prompt solto ou sorte operacional.
- Marque RISCO ACEITO apenas com owner, impacto, prazo e monitoramento explícitos.
- Reabra o cartão se a evidência estiver certa, mas estiver no lugar arquitetural errado.

#### Persistência - sinais de risco que mudam a decisão

- Carrinho mantido apenas em memoria de worker.
- Checkpoint salvo depois de acao irreversivel, nao antes.
- State sem schema_version ou timestamp.
- Recovery descrito em arquitetura, mas nunca testado.
- Replay dependendo de logs soltos sem inputs originais.
- Arquivo JSON escrito diretamente sem publicacao atomica.
- Backup configurado, mas restauracao nunca ensaiada.
- Dados pessoais sem retencao definida.
- Backend escolhido por conveniencia sem discutir concorrencia.
- State antigo lido sem migracao ou rejeicao clara.
- Checkpoint parcial consumido por agente seguinte.
- Trace sem refs para artefatos persistidos.

#### Persistência - campos mínimos para registrar PASS ou FAIL

- state schema e versao
- ultimo checkpoint valido
- acao cara ou irreversivel protegida
- resultado de teste de crash
- procedimento de restore
- padrao de escrita atomica
- politica de retencao
- justificativa do backend
- artefatos minimos para replay
- owner de migracao de schema

#### Persistência - decisão de auditoria

- Marque PASS somente quando a evidência existir fora da conversa oral.
- Marque FAIL quando o comportamento depender de intenção, prompt solto ou sorte operacional.
- Marque RISCO ACEITO apenas com owner, impacto, prazo e monitoramento explícitos.
- Reabra o cartão se a evidência estiver certa, mas estiver no lugar arquitetural errado.

#### Coordenação - sinais de risco que mudam a decisão

- Dois agentes escrevendo no mesmo recurso sem lock.
- Status file sem timestamp ou motivo de falha.
- Mensagem JSON sem correlation_id.
- Leitor consumindo arquivo temporario ou parcial.
- Webhook reprocessado criando pedido duplicado.
- Lock sem TTL prendendo jornada indefinidamente.
- Dependencia entre agentes documentada, mas nao aplicada.
- Teste concorrente inexistente para carrinho ou estoque.
- Agent_id ausente no audit trail.
- Status completed escrito antes de output final estar pronto.
- Protocolo alterado sem schema_version.
- Fallback de deadlock exigindo intervencao manual nao registrada.

#### Coordenação - campos mínimos para registrar PASS ou FAIL

- recurso compartilhado revisado
- lock ou transacao usada
- TTL e owner do lock
- status atual da etapa
- schema do protocolo JSON
- correlation_id ponta a ponta
- teste de concorrencia
- regra de idempotencia
- ordem entre agentes
- trace de aquisicao e liberacao

#### Coordenação - decisão de auditoria

- Marque PASS somente quando a evidência existir fora da conversa oral.
- Marque FAIL quando o comportamento depender de intenção, prompt solto ou sorte operacional.
- Marque RISCO ACEITO apenas com owner, impacto, prazo e monitoramento explícitos.
- Reabra o cartão se a evidência estiver certa, mas estiver no lugar arquitetural errado.

#### Segurança & Guardrails - sinais de risco que mudam a decisão

- Webhook aceito sem schema ou limite de tamanho.
- Tool output misturado ao prompt sem delimitacao.
- Resposta final enviada sem checagem de catalogo.
- Alergia, regiao ou estoque tratados apenas por prompt.
- Fallback generico dizendo para tentar novamente.
- Guardrail critico falhando aberto por conveniencia.
- Budget guard por chamada, mas nao por jornada inteira.
- Prompt injection sem teste regressivo.
- Pagamento executado antes de aprovacao validada.
- Log de rejeicao sem motivo acionavel.
- Retry duplicando acao externa.
- Politica comercial atualizada sem atualizar validator.

#### Segurança & Guardrails - campos mínimos para registrar PASS ou FAIL

- schema de entrada
- validator de output
- constraint checker aplicado
- policy fail-closed
- fallback especifico
- budget maximo por turno e jornada
- teste de prompt injection
- aprovacao antes de acao irreversivel
- audit log de bloqueio
- owner de cada guardrail critico

#### Segurança & Guardrails - decisão de auditoria

- Marque PASS somente quando a evidência existir fora da conversa oral.
- Marque FAIL quando o comportamento depender de intenção, prompt solto ou sorte operacional.
- Marque RISCO ACEITO apenas com owner, impacto, prazo e monitoramento explícitos.
- Reabra o cartão se a evidência estiver certa, mas estiver no lugar arquitetural errado.

#### Evolução - sinais de risco que mudam a decisão

- Componente sem fase BUILD, STABILIZE, SIMPLIFY ou REMOVE.
- Guardrail mantido sem medir falhas prevenidas.
- Custo de token crescendo sem decisao explicita.
- Falso positivo alto sem plano de ajuste.
- Componente criado para modelo antigo ainda obrigatorio.
- Remocao proposta sem shadow test.
- Rollback mencionado, mas nao testado.
- ADR ausente para mudanca estrutural.
- Revisao trimestral pulada apos upgrade de modelo.
- Owner antigo ainda listado para componente critico.
- Simplificacao confundida com apagar evidencia.
- Metrica de sucesso sem baseline anterior.

#### Evolução - campos mínimos para registrar PASS ou FAIL

- fase atual do componente
- data da ultima revisao
- falhas reais prevenidas
- tokens e latencia adicionados
- falsos positivos e falsos negativos
- criterio de simplificacao
- resultado de shadow test
- plano de rollback
- ADR ou changelog
- owner da proxima decisao

#### Evolução - decisão de auditoria

- Marque PASS somente quando a evidência existir fora da conversa oral.
- Marque FAIL quando o comportamento depender de intenção, prompt solto ou sorte operacional.
- Marque RISCO ACEITO apenas com owner, impacto, prazo e monitoramento explícitos.
- Reabra o cartão se a evidência estiver certa, mas estiver no lugar arquitetural errado.

#### Observabilidade - sinais de risco que mudam a decisão

- Trace sem input refs ou output refs.
- Logs que mostram texto final, mas nao decisao intermediaria.
- Audit log ausente para promessa comercial.
- Dashboard medindo volume sem qualidade.
- Alerta sem owner ou runbook.
- Replay impossivel por falta de artefatos.
- WhatsApp id desconectado de order id.
- Conversas aprovadas nunca amostradas.
- Trace reading conhecido por uma pessoa apenas.
- Incidente reencenado manualmente em vez de reconstruido.
- Fallback rate agregado sem separar por feature.
- Metricas tecnicas sem sintoma de negocio associado.

#### Observabilidade - campos mínimos para registrar PASS ou FAIL

- trace_id e correlation_id
- fases com timestamps
- input refs e output refs
- audit log de acao critica
- dashboard de qualidade e custo
- alerta com owner e severidade
- runbook da primeira acao
- artefatos de replay
- amostragem de aprovados
- link para guia de trace reading

#### Observabilidade - decisão de auditoria

- Marque PASS somente quando a evidência existir fora da conversa oral.
- Marque FAIL quando o comportamento depender de intenção, prompt solto ou sorte operacional.
- Marque RISCO ACEITO apenas com owner, impacto, prazo e monitoramento explícitos.
- Reabra o cartão se a evidência estiver certa, mas estiver no lugar arquitetural errado.

### Protocolo de fechamento dos cartões de auditoria

Use este protocolo depois de revisar os cartões de uma categoria.

- Confirme que o PASS aponta para artefato, nao para opiniao.
- Confirme que o FAIL descreve impacto ao cliente ou ao time.
- Confirme que cada risco aceito tem owner unico.
- Confirme que cada owner tem prazo de revisao.
- Confirme que cada evidencia pode ser aberta por uma pessoa nova.
- Confirme que prints soltos nao substituem trace, teste ou contrato.
- Confirme que logs sem correlation_id nao contam como audit trail completo.
- Confirme que teste manual sem roteiro nao conta como recovery test.
- Confirme que dashboard sem threshold nao conta como alerta acionavel.
- Confirme que fallback generico nao conta como protecao de seguranca.
- Confirme que retry cego nao conta como failure handling.
- Confirme que schema sem exemplo valido nao conta como contrato completo.
- Confirme que exemplo valido sem teste nao protege regressao.
- Confirme que owner antigo nao conta como ownership atual.
- Confirme que ADR proposta nao conta como decisao aceita.
- Confirme que shadow test tem baseline antes de autorizar remocao.
- Confirme que rollout limitado define limite, duracao e criterio de parada.
- Confirme que monitoramento cobre sintoma tecnico e sintoma de negocio.
- Confirme que a decisao final registra aprovado, bloqueado ou risco aceito.
- Confirme que o proximo revisor saberia repetir a mesma verificacao.
- Registre links para contratos, traces, testes, dashboards e ADRs usados.
- Registre a versao do modelo quando ela afetar avaliacao ou contexto.
- Registre a versao da rubrica quando ela afetar aprovacao.
- Registre a versao do schema quando ela afetar handoff entre agentes.
- Registre a janela de tempo analisada quando usar metricas.
- Registre amostras analisadas quando usar evidência estatistica.
- Registre excecoes aprovadas por produto ou engenharia.
- Registre qualquer conflito entre score agregado e blocker absoluto.
- Registre qualquer falta de evidência como FAIL, nao como pendencia neutra.
- Registre quando a protecao esta no lugar errado e precisa migrar de camada.
- Use o menor artefato suficiente para fechar o gap, sem criar processo extra.
- Reavalie a categoria quando o artefato minimo ficar pronto.

## 📚 Apêndice B: Perguntas de Calibração por Nível de Maturidade

### 🧠 Contexto (Context Management)

#### Nível 1

- O que provaria que Contexto (Context Management) está no nível 1 neste harness?
- Qual métrica mudaria se Contexto (Context Management) fosse removido ou enfraquecido?
- Qual incidente passado de KODA teria sido prevenido por Contexto (Context Management) neste nível?
- Qual custo adicional este nível adiciona em tokens, latência, manutenção ou onboarding?
- Qual evidência faria Fernando aceitar este nível como suficiente para a próxima release?

#### Nível 2

- O que provaria que Contexto (Context Management) está no nível 2 neste harness?
- Qual métrica mudaria se Contexto (Context Management) fosse removido ou enfraquecido?
- Qual incidente passado de KODA teria sido prevenido por Contexto (Context Management) neste nível?
- Qual custo adicional este nível adiciona em tokens, latência, manutenção ou onboarding?
- Qual evidência faria Fernando aceitar este nível como suficiente para a próxima release?

#### Nível 3

- O que provaria que Contexto (Context Management) está no nível 3 neste harness?
- Qual métrica mudaria se Contexto (Context Management) fosse removido ou enfraquecido?
- Qual incidente passado de KODA teria sido prevenido por Contexto (Context Management) neste nível?
- Qual custo adicional este nível adiciona em tokens, latência, manutenção ou onboarding?
- Qual evidência faria Fernando aceitar este nível como suficiente para a próxima release?

#### Nível 4

- O que provaria que Contexto (Context Management) está no nível 4 neste harness?
- Qual métrica mudaria se Contexto (Context Management) fosse removido ou enfraquecido?
- Qual incidente passado de KODA teria sido prevenido por Contexto (Context Management) neste nível?
- Qual custo adicional este nível adiciona em tokens, latência, manutenção ou onboarding?
- Qual evidência faria Fernando aceitar este nível como suficiente para a próxima release?

#### Nível 5

- O que provaria que Contexto (Context Management) está no nível 5 neste harness?
- Qual métrica mudaria se Contexto (Context Management) fosse removido ou enfraquecido?
- Qual incidente passado de KODA teria sido prevenido por Contexto (Context Management) neste nível?
- Qual custo adicional este nível adiciona em tokens, latência, manutenção ou onboarding?
- Qual evidência faria Fernando aceitar este nível como suficiente para a próxima release?

### 📜 Contratos (Contracts/Sprint Contracts)

#### Nível 1

- O que provaria que Contratos (Contracts/Sprint Contracts) está no nível 1 neste harness?
- Qual métrica mudaria se Contratos (Contracts/Sprint Contracts) fosse removido ou enfraquecido?
- Qual incidente passado de KODA teria sido prevenido por Contratos (Contracts/Sprint Contracts) neste nível?
- Qual custo adicional este nível adiciona em tokens, latência, manutenção ou onboarding?
- Qual evidência faria Fernando aceitar este nível como suficiente para a próxima release?

#### Nível 2

- O que provaria que Contratos (Contracts/Sprint Contracts) está no nível 2 neste harness?
- Qual métrica mudaria se Contratos (Contracts/Sprint Contracts) fosse removido ou enfraquecido?
- Qual incidente passado de KODA teria sido prevenido por Contratos (Contracts/Sprint Contracts) neste nível?
- Qual custo adicional este nível adiciona em tokens, latência, manutenção ou onboarding?
- Qual evidência faria Fernando aceitar este nível como suficiente para a próxima release?

#### Nível 3

- O que provaria que Contratos (Contracts/Sprint Contracts) está no nível 3 neste harness?
- Qual métrica mudaria se Contratos (Contracts/Sprint Contracts) fosse removido ou enfraquecido?
- Qual incidente passado de KODA teria sido prevenido por Contratos (Contracts/Sprint Contracts) neste nível?
- Qual custo adicional este nível adiciona em tokens, latência, manutenção ou onboarding?
- Qual evidência faria Fernando aceitar este nível como suficiente para a próxima release?

#### Nível 4

- O que provaria que Contratos (Contracts/Sprint Contracts) está no nível 4 neste harness?
- Qual métrica mudaria se Contratos (Contracts/Sprint Contracts) fosse removido ou enfraquecido?
- Qual incidente passado de KODA teria sido prevenido por Contratos (Contracts/Sprint Contracts) neste nível?
- Qual custo adicional este nível adiciona em tokens, latência, manutenção ou onboarding?
- Qual evidência faria Fernando aceitar este nível como suficiente para a próxima release?

#### Nível 5

- O que provaria que Contratos (Contracts/Sprint Contracts) está no nível 5 neste harness?
- Qual métrica mudaria se Contratos (Contracts/Sprint Contracts) fosse removido ou enfraquecido?
- Qual incidente passado de KODA teria sido prevenido por Contratos (Contracts/Sprint Contracts) neste nível?
- Qual custo adicional este nível adiciona em tokens, latência, manutenção ou onboarding?
- Qual evidência faria Fernando aceitar este nível como suficiente para a próxima release?

### ⚖️ Avaliação (Evaluation/Rubrics)

#### Nível 1

- O que provaria que Avaliação (Evaluation/Rubrics) está no nível 1 neste harness?
- Qual métrica mudaria se Avaliação (Evaluation/Rubrics) fosse removida ou enfraquecida?
- Qual incidente passado de KODA teria sido prevenido por Avaliação (Evaluation/Rubrics) neste nível?
- Qual custo adicional este nível adiciona em tokens, latência, manutenção ou onboarding?
- Qual evidência faria Fernando aceitar este nível como suficiente para a próxima release?

#### Nível 2

- O que provaria que Avaliação (Evaluation/Rubrics) está no nível 2 neste harness?
- Qual métrica mudaria se Avaliação (Evaluation/Rubrics) fosse removida ou enfraquecida?
- Qual incidente passado de KODA teria sido prevenido por Avaliação (Evaluation/Rubrics) neste nível?
- Qual custo adicional este nível adiciona em tokens, latência, manutenção ou onboarding?
- Qual evidência faria Fernando aceitar este nível como suficiente para a próxima release?

#### Nível 3

- O que provaria que Avaliação (Evaluation/Rubrics) está no nível 3 neste harness?
- Qual métrica mudaria se Avaliação (Evaluation/Rubrics) fosse removida ou enfraquecida?
- Qual incidente passado de KODA teria sido prevenido por Avaliação (Evaluation/Rubrics) neste nível?
- Qual custo adicional este nível adiciona em tokens, latência, manutenção ou onboarding?
- Qual evidência faria Fernando aceitar este nível como suficiente para a próxima release?

#### Nível 4

- O que provaria que Avaliação (Evaluation/Rubrics) está no nível 4 neste harness?
- Qual métrica mudaria se Avaliação (Evaluation/Rubrics) fosse removida ou enfraquecida?
- Qual incidente passado de KODA teria sido prevenido por Avaliação (Evaluation/Rubrics) neste nível?
- Qual custo adicional este nível adiciona em tokens, latência, manutenção ou onboarding?
- Qual evidência faria Fernando aceitar este nível como suficiente para a próxima release?

#### Nível 5

- O que provaria que Avaliação (Evaluation/Rubrics) está no nível 5 neste harness?
- Qual métrica mudaria se Avaliação (Evaluation/Rubrics) fosse removida ou enfraquecida?
- Qual incidente passado de KODA teria sido prevenido por Avaliação (Evaluation/Rubrics) neste nível?
- Qual custo adicional este nível adiciona em tokens, latência, manutenção ou onboarding?
- Qual evidência faria Fernando aceitar este nível como suficiente para a próxima release?

### 💾 Persistência (State Persistence)

#### Nível 1

- O que provaria que Persistência (State Persistence) está no nível 1 neste harness?
- Qual métrica mudaria se Persistência (State Persistence) fosse removida ou enfraquecida?
- Qual incidente passado de KODA teria sido prevenido por Persistência (State Persistence) neste nível?
- Qual custo adicional este nível adiciona em tokens, latência, manutenção ou onboarding?
- Qual evidência faria Fernando aceitar este nível como suficiente para a próxima release?

#### Nível 2

- O que provaria que Persistência (State Persistence) está no nível 2 neste harness?
- Qual métrica mudaria se Persistência (State Persistence) fosse removida ou enfraquecida?
- Qual incidente passado de KODA teria sido prevenido por Persistência (State Persistence) neste nível?
- Qual custo adicional este nível adiciona em tokens, latência, manutenção ou onboarding?
- Qual evidência faria Fernando aceitar este nível como suficiente para a próxima release?

#### Nível 3

- O que provaria que Persistência (State Persistence) está no nível 3 neste harness?
- Qual métrica mudaria se Persistência (State Persistence) fosse removida ou enfraquecida?
- Qual incidente passado de KODA teria sido prevenido por Persistência (State Persistence) neste nível?
- Qual custo adicional este nível adiciona em tokens, latência, manutenção ou onboarding?
- Qual evidência faria Fernando aceitar este nível como suficiente para a próxima release?

#### Nível 4

- O que provaria que Persistência (State Persistence) está no nível 4 neste harness?
- Qual métrica mudaria se Persistência (State Persistence) fosse removida ou enfraquecida?
- Qual incidente passado de KODA teria sido prevenido por Persistência (State Persistence) neste nível?
- Qual custo adicional este nível adiciona em tokens, latência, manutenção ou onboarding?
- Qual evidência faria Fernando aceitar este nível como suficiente para a próxima release?

#### Nível 5

- O que provaria que Persistência (State Persistence) está no nível 5 neste harness?
- Qual métrica mudaria se Persistência (State Persistence) fosse removida ou enfraquecida?
- Qual incidente passado de KODA teria sido prevenido por Persistência (State Persistence) neste nível?
- Qual custo adicional este nível adiciona em tokens, latência, manutenção ou onboarding?
- Qual evidência faria Fernando aceitar este nível como suficiente para a próxima release?

### 🤝 Coordenação (Multi-Agent Coordination)

#### Nível 1

- O que provaria que Coordenação (Multi-Agent Coordination) está no nível 1 neste harness?
- Qual métrica mudaria se Coordenação (Multi-Agent Coordination) fosse removida ou enfraquecida?
- Qual incidente passado de KODA teria sido prevenido por Coordenação (Multi-Agent Coordination) neste nível?
- Qual custo adicional este nível adiciona em tokens, latência, manutenção ou onboarding?
- Qual evidência faria Fernando aceitar este nível como suficiente para a próxima release?

#### Nível 2

- O que provaria que Coordenação (Multi-Agent Coordination) está no nível 2 neste harness?
- Qual métrica mudaria se Coordenação (Multi-Agent Coordination) fosse removida ou enfraquecida?
- Qual incidente passado de KODA teria sido prevenido por Coordenação (Multi-Agent Coordination) neste nível?
- Qual custo adicional este nível adiciona em tokens, latência, manutenção ou onboarding?
- Qual evidência faria Fernando aceitar este nível como suficiente para a próxima release?

#### Nível 3

- O que provaria que Coordenação (Multi-Agent Coordination) está no nível 3 neste harness?
- Qual métrica mudaria se Coordenação (Multi-Agent Coordination) fosse removida ou enfraquecida?
- Qual incidente passado de KODA teria sido prevenido por Coordenação (Multi-Agent Coordination) neste nível?
- Qual custo adicional este nível adiciona em tokens, latência, manutenção ou onboarding?
- Qual evidência faria Fernando aceitar este nível como suficiente para a próxima release?

#### Nível 4

- O que provaria que Coordenação (Multi-Agent Coordination) está no nível 4 neste harness?
- Qual métrica mudaria se Coordenação (Multi-Agent Coordination) fosse removida ou enfraquecida?
- Qual incidente passado de KODA teria sido prevenido por Coordenação (Multi-Agent Coordination) neste nível?
- Qual custo adicional este nível adiciona em tokens, latência, manutenção ou onboarding?
- Qual evidência faria Fernando aceitar este nível como suficiente para a próxima release?

#### Nível 5

- O que provaria que Coordenação (Multi-Agent Coordination) está no nível 5 neste harness?
- Qual métrica mudaria se Coordenação (Multi-Agent Coordination) fosse removida ou enfraquecida?
- Qual incidente passado de KODA teria sido prevenido por Coordenação (Multi-Agent Coordination) neste nível?
- Qual custo adicional este nível adiciona em tokens, latência, manutenção ou onboarding?
- Qual evidência faria Fernando aceitar este nível como suficiente para a próxima release?

### 🛡️ Segurança & Guardrails

#### Nível 1

- O que provaria que Segurança & Guardrails está no nível 1 neste harness?
- Qual métrica mudaria se Segurança & Guardrails fosse removida ou enfraquecida?
- Qual incidente passado de KODA teria sido prevenido por Segurança & Guardrails neste nível?
- Qual custo adicional este nível adiciona em tokens, latência, manutenção ou onboarding?
- Qual evidência faria Fernando aceitar este nível como suficiente para a próxima release?

#### Nível 2

- O que provaria que Segurança & Guardrails está no nível 2 neste harness?
- Qual métrica mudaria se Segurança & Guardrails fosse removida ou enfraquecida?
- Qual incidente passado de KODA teria sido prevenido por Segurança & Guardrails neste nível?
- Qual custo adicional este nível adiciona em tokens, latência, manutenção ou onboarding?
- Qual evidência faria Fernando aceitar este nível como suficiente para a próxima release?

#### Nível 3

- O que provaria que Segurança & Guardrails está no nível 3 neste harness?
- Qual métrica mudaria se Segurança & Guardrails fosse removida ou enfraquecida?
- Qual incidente passado de KODA teria sido prevenido por Segurança & Guardrails neste nível?
- Qual custo adicional este nível adiciona em tokens, latência, manutenção ou onboarding?
- Qual evidência faria Fernando aceitar este nível como suficiente para a próxima release?

#### Nível 4

- O que provaria que Segurança & Guardrails está no nível 4 neste harness?
- Qual métrica mudaria se Segurança & Guardrails fosse removida ou enfraquecida?
- Qual incidente passado de KODA teria sido prevenido por Segurança & Guardrails neste nível?
- Qual custo adicional este nível adiciona em tokens, latência, manutenção ou onboarding?
- Qual evidência faria Fernando aceitar este nível como suficiente para a próxima release?

#### Nível 5

- O que provaria que Segurança & Guardrails está no nível 5 neste harness?
- Qual métrica mudaria se Segurança & Guardrails fosse removida ou enfraquecida?
- Qual incidente passado de KODA teria sido prevenido por Segurança & Guardrails neste nível?
- Qual custo adicional este nível adiciona em tokens, latência, manutenção ou onboarding?
- Qual evidência faria Fernando aceitar este nível como suficiente para a próxima release?

### 🧬 Evolução (Harness Evolution)

#### Nível 1

- O que provaria que Evolução (Harness Evolution) está no nível 1 neste harness?
- Qual métrica mudaria se Evolução (Harness Evolution) fosse removida ou enfraquecida?
- Qual incidente passado de KODA teria sido prevenido por Evolução (Harness Evolution) neste nível?
- Qual custo adicional este nível adiciona em tokens, latência, manutenção ou onboarding?
- Qual evidência faria Fernando aceitar este nível como suficiente para a próxima release?

#### Nível 2

- O que provaria que Evolução (Harness Evolution) está no nível 2 neste harness?
- Qual métrica mudaria se Evolução (Harness Evolution) fosse removida ou enfraquecida?
- Qual incidente passado de KODA teria sido prevenido por Evolução (Harness Evolution) neste nível?
- Qual custo adicional este nível adiciona em tokens, latência, manutenção ou onboarding?
- Qual evidência faria Fernando aceitar este nível como suficiente para a próxima release?

#### Nível 3

- O que provaria que Evolução (Harness Evolution) está no nível 3 neste harness?
- Qual métrica mudaria se Evolução (Harness Evolution) fosse removida ou enfraquecida?
- Qual incidente passado de KODA teria sido prevenido por Evolução (Harness Evolution) neste nível?
- Qual custo adicional este nível adiciona em tokens, latência, manutenção ou onboarding?
- Qual evidência faria Fernando aceitar este nível como suficiente para a próxima release?

#### Nível 4

- O que provaria que Evolução (Harness Evolution) está no nível 4 neste harness?
- Qual métrica mudaria se Evolução (Harness Evolution) fosse removida ou enfraquecida?
- Qual incidente passado de KODA teria sido prevenido por Evolução (Harness Evolution) neste nível?
- Qual custo adicional este nível adiciona em tokens, latência, manutenção ou onboarding?
- Qual evidência faria Fernando aceitar este nível como suficiente para a próxima release?

#### Nível 5

- O que provaria que Evolução (Harness Evolution) está no nível 5 neste harness?
- Qual métrica mudaria se Evolução (Harness Evolution) fosse removida ou enfraquecida?
- Qual incidente passado de KODA teria sido prevenido por Evolução (Harness Evolution) neste nível?
- Qual custo adicional este nível adiciona em tokens, latência, manutenção ou onboarding?
- Qual evidência faria Fernando aceitar este nível como suficiente para a próxima release?

### 📡 Observabilidade (Traces/Monitoring)

#### Nível 1

- O que provaria que Observabilidade (Traces/Monitoring) está no nível 1 neste harness?
- Qual métrica mudaria se Observabilidade (Traces/Monitoring) fosse removida ou enfraquecida?
- Qual incidente passado de KODA teria sido prevenido por Observabilidade (Traces/Monitoring) neste nível?
- Qual custo adicional este nível adiciona em tokens, latência, manutenção ou onboarding?
- Qual evidência faria Fernando aceitar este nível como suficiente para a próxima release?

#### Nível 2

- O que provaria que Observabilidade (Traces/Monitoring) está no nível 2 neste harness?
- Qual métrica mudaria se Observabilidade (Traces/Monitoring) fosse removida ou enfraquecida?
- Qual incidente passado de KODA teria sido prevenido por Observabilidade (Traces/Monitoring) neste nível?
- Qual custo adicional este nível adiciona em tokens, latência, manutenção ou onboarding?
- Qual evidência faria Fernando aceitar este nível como suficiente para a próxima release?

#### Nível 3

- O que provaria que Observabilidade (Traces/Monitoring) está no nível 3 neste harness?
- Qual métrica mudaria se Observabilidade (Traces/Monitoring) fosse removida ou enfraquecida?
- Qual incidente passado de KODA teria sido prevenido por Observabilidade (Traces/Monitoring) neste nível?
- Qual custo adicional este nível adiciona em tokens, latência, manutenção ou onboarding?
- Qual evidência faria Fernando aceitar este nível como suficiente para a próxima release?

#### Nível 4

- O que provaria que Observabilidade (Traces/Monitoring) está no nível 4 neste harness?
- Qual métrica mudaria se Observabilidade (Traces/Monitoring) fosse removida ou enfraquecida?
- Qual incidente passado de KODA teria sido prevenido por Observabilidade (Traces/Monitoring) neste nível?
- Qual custo adicional este nível adiciona em tokens, latência, manutenção ou onboarding?
- Qual evidência faria Fernando aceitar este nível como suficiente para a próxima release?

#### Nível 5

- O que provaria que Observabilidade (Traces/Monitoring) está no nível 5 neste harness?
- Qual métrica mudaria se Observabilidade (Traces/Monitoring) fosse removida ou enfraquecida?
- Qual incidente passado de KODA teria sido prevenido por Observabilidade (Traces/Monitoring) neste nível?
- Qual custo adicional este nível adiciona em tokens, latência, manutenção ou onboarding?
- Qual evidência faria Fernando aceitar este nível como suficiente para a próxima release?

---

## 📎 Metadata

| Campo | Valor |
|-------|-------|
| Título | Checklist de Design de Harness para Agentes Confiáveis |
| Tipo | Implementation Guide |
| Público | Engenharia, tech leads, reviewers, produto técnico |
| Projeto de referência | KODA - agente de vendas de suplementos via WhatsApp |
| Issue | #47 |
| Idioma | Português brasileiro com technical terms em inglês |
| Versão | 1.0 |
| Criado em | Maio 2026 |
| Status | Completo para uso em auditorias de harness |

*Este guia integra padrões dos Níveis 1, 2 e 3 do currículo de Long-Running Agents.*

*Use como documento vivo: cada auditoria real deve melhorar critérios, evidências e exemplos.*
