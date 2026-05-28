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

### Interpretação da pontuação

- **8-15 pontos:** harness experimental. Use apenas em demo, protótipo ou fluxo sem risco comercial.
- **16-24 pontos:** harness inicial. Pode rodar com supervisão humana e baixa autonomia.
- **25-32 pontos:** harness operacional. Aceitável para produção limitada com monitoramento ativo.
- **33-38 pontos:** harness robusto. Adequado para produção em escala com incident response definido.
- **39-40 pontos:** harness excelente. Além de confiável, é evolutivo, auditável e ensina o time a melhorar.

### Regra de bloqueio

Mesmo com score alto, qualquer FAIL crítico em Segurança, Persistência ou Avaliação pode bloquear produção. Score agregado nunca deve esconder risco absoluto.

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

- [ ] Contexto (Context Management): verificação rápida 01 confirma evidência objetiva antes de marcar PASS.
- [ ] Contexto (Context Management): verificação rápida 02 confirma evidência objetiva antes de marcar PASS.
- [ ] Contexto (Context Management): verificação rápida 03 confirma evidência objetiva antes de marcar PASS.
- [ ] Contexto (Context Management): verificação rápida 04 confirma evidência objetiva antes de marcar PASS.
- [ ] Contexto (Context Management): verificação rápida 05 confirma evidência objetiva antes de marcar PASS.
- [ ] Contexto (Context Management): verificação rápida 06 confirma evidência objetiva antes de marcar PASS.
- [ ] Contexto (Context Management): verificação rápida 07 confirma evidência objetiva antes de marcar PASS.
- [ ] Contexto (Context Management): verificação rápida 08 confirma evidência objetiva antes de marcar PASS.
- [ ] Contexto (Context Management): verificação rápida 09 confirma evidência objetiva antes de marcar PASS.
- [ ] Contexto (Context Management): verificação rápida 10 confirma evidência objetiva antes de marcar PASS.
- [ ] Contexto (Context Management): verificação rápida 11 confirma evidência objetiva antes de marcar PASS.
- [ ] Contexto (Context Management): verificação rápida 12 confirma evidência objetiva antes de marcar PASS.
- [ ] Contexto (Context Management): verificação rápida 13 confirma evidência objetiva antes de marcar PASS.
- [ ] Contexto (Context Management): verificação rápida 14 confirma evidência objetiva antes de marcar PASS.
- [ ] Contexto (Context Management): verificação rápida 15 confirma evidência objetiva antes de marcar PASS.
- [ ] Contexto (Context Management): verificação rápida 16 confirma evidência objetiva antes de marcar PASS.
- [ ] Contexto (Context Management): verificação rápida 17 confirma evidência objetiva antes de marcar PASS.
- [ ] Contexto (Context Management): verificação rápida 18 confirma evidência objetiva antes de marcar PASS.

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

- [ ] Contratos (Contracts/Sprint Contracts): verificação rápida 01 confirma evidência objetiva antes de marcar PASS.
- [ ] Contratos (Contracts/Sprint Contracts): verificação rápida 02 confirma evidência objetiva antes de marcar PASS.
- [ ] Contratos (Contracts/Sprint Contracts): verificação rápida 03 confirma evidência objetiva antes de marcar PASS.
- [ ] Contratos (Contracts/Sprint Contracts): verificação rápida 04 confirma evidência objetiva antes de marcar PASS.
- [ ] Contratos (Contracts/Sprint Contracts): verificação rápida 05 confirma evidência objetiva antes de marcar PASS.
- [ ] Contratos (Contracts/Sprint Contracts): verificação rápida 06 confirma evidência objetiva antes de marcar PASS.
- [ ] Contratos (Contracts/Sprint Contracts): verificação rápida 07 confirma evidência objetiva antes de marcar PASS.
- [ ] Contratos (Contracts/Sprint Contracts): verificação rápida 08 confirma evidência objetiva antes de marcar PASS.
- [ ] Contratos (Contracts/Sprint Contracts): verificação rápida 09 confirma evidência objetiva antes de marcar PASS.
- [ ] Contratos (Contracts/Sprint Contracts): verificação rápida 10 confirma evidência objetiva antes de marcar PASS.
- [ ] Contratos (Contracts/Sprint Contracts): verificação rápida 11 confirma evidência objetiva antes de marcar PASS.
- [ ] Contratos (Contracts/Sprint Contracts): verificação rápida 12 confirma evidência objetiva antes de marcar PASS.
- [ ] Contratos (Contracts/Sprint Contracts): verificação rápida 13 confirma evidência objetiva antes de marcar PASS.
- [ ] Contratos (Contracts/Sprint Contracts): verificação rápida 14 confirma evidência objetiva antes de marcar PASS.
- [ ] Contratos (Contracts/Sprint Contracts): verificação rápida 15 confirma evidência objetiva antes de marcar PASS.
- [ ] Contratos (Contracts/Sprint Contracts): verificação rápida 16 confirma evidência objetiva antes de marcar PASS.
- [ ] Contratos (Contracts/Sprint Contracts): verificação rápida 17 confirma evidência objetiva antes de marcar PASS.
- [ ] Contratos (Contracts/Sprint Contracts): verificação rápida 18 confirma evidência objetiva antes de marcar PASS.

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

## ⚖️ 3. Avaliação (Evaluation/Rubrics)

Esta categoria verifica se um harness bom separa geração de julgamento e transforma qualidade em critérios mensuráveis.

### O que um bom harness faz

- Rubrics têm dimensões com pesos, thresholds e blockers explícitos.
- O Evaluator é separado do Generator e não reusa a justificativa do Generator como prova.
- Critérios de aprovação combinam score ponderado com bloqueios absolutos.
- Cada avaliação produz evidência auditável, não apenas uma nota final.
- A rubrica é calibrada com exemplos aprovados, reprovados e limítrofes.

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

- [ ] Avaliação (Evaluation/Rubrics): verificação rápida 01 confirma evidência objetiva antes de marcar PASS.
- [ ] Avaliação (Evaluation/Rubrics): verificação rápida 02 confirma evidência objetiva antes de marcar PASS.
- [ ] Avaliação (Evaluation/Rubrics): verificação rápida 03 confirma evidência objetiva antes de marcar PASS.
- [ ] Avaliação (Evaluation/Rubrics): verificação rápida 04 confirma evidência objetiva antes de marcar PASS.
- [ ] Avaliação (Evaluation/Rubrics): verificação rápida 05 confirma evidência objetiva antes de marcar PASS.
- [ ] Avaliação (Evaluation/Rubrics): verificação rápida 06 confirma evidência objetiva antes de marcar PASS.
- [ ] Avaliação (Evaluation/Rubrics): verificação rápida 07 confirma evidência objetiva antes de marcar PASS.
- [ ] Avaliação (Evaluation/Rubrics): verificação rápida 08 confirma evidência objetiva antes de marcar PASS.
- [ ] Avaliação (Evaluation/Rubrics): verificação rápida 09 confirma evidência objetiva antes de marcar PASS.
- [ ] Avaliação (Evaluation/Rubrics): verificação rápida 10 confirma evidência objetiva antes de marcar PASS.
- [ ] Avaliação (Evaluation/Rubrics): verificação rápida 11 confirma evidência objetiva antes de marcar PASS.
- [ ] Avaliação (Evaluation/Rubrics): verificação rápida 12 confirma evidência objetiva antes de marcar PASS.
- [ ] Avaliação (Evaluation/Rubrics): verificação rápida 13 confirma evidência objetiva antes de marcar PASS.
- [ ] Avaliação (Evaluation/Rubrics): verificação rápida 14 confirma evidência objetiva antes de marcar PASS.
- [ ] Avaliação (Evaluation/Rubrics): verificação rápida 15 confirma evidência objetiva antes de marcar PASS.
- [ ] Avaliação (Evaluation/Rubrics): verificação rápida 16 confirma evidência objetiva antes de marcar PASS.
- [ ] Avaliação (Evaluation/Rubrics): verificação rápida 17 confirma evidência objetiva antes de marcar PASS.
- [ ] Avaliação (Evaluation/Rubrics): verificação rápida 18 confirma evidência objetiva antes de marcar PASS.

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

- [ ] Persistência (State Persistence): verificação rápida 01 confirma evidência objetiva antes de marcar PASS.
- [ ] Persistência (State Persistence): verificação rápida 02 confirma evidência objetiva antes de marcar PASS.
- [ ] Persistência (State Persistence): verificação rápida 03 confirma evidência objetiva antes de marcar PASS.
- [ ] Persistência (State Persistence): verificação rápida 04 confirma evidência objetiva antes de marcar PASS.
- [ ] Persistência (State Persistence): verificação rápida 05 confirma evidência objetiva antes de marcar PASS.
- [ ] Persistência (State Persistence): verificação rápida 06 confirma evidência objetiva antes de marcar PASS.
- [ ] Persistência (State Persistence): verificação rápida 07 confirma evidência objetiva antes de marcar PASS.
- [ ] Persistência (State Persistence): verificação rápida 08 confirma evidência objetiva antes de marcar PASS.
- [ ] Persistência (State Persistence): verificação rápida 09 confirma evidência objetiva antes de marcar PASS.
- [ ] Persistência (State Persistence): verificação rápida 10 confirma evidência objetiva antes de marcar PASS.
- [ ] Persistência (State Persistence): verificação rápida 11 confirma evidência objetiva antes de marcar PASS.
- [ ] Persistência (State Persistence): verificação rápida 12 confirma evidência objetiva antes de marcar PASS.
- [ ] Persistência (State Persistence): verificação rápida 13 confirma evidência objetiva antes de marcar PASS.
- [ ] Persistência (State Persistence): verificação rápida 14 confirma evidência objetiva antes de marcar PASS.
- [ ] Persistência (State Persistence): verificação rápida 15 confirma evidência objetiva antes de marcar PASS.
- [ ] Persistência (State Persistence): verificação rápida 16 confirma evidência objetiva antes de marcar PASS.
- [ ] Persistência (State Persistence): verificação rápida 17 confirma evidência objetiva antes de marcar PASS.
- [ ] Persistência (State Persistence): verificação rápida 18 confirma evidência objetiva antes de marcar PASS.

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

- [ ] Coordenação (Multi-Agent Coordination): verificação rápida 01 confirma evidência objetiva antes de marcar PASS.
- [ ] Coordenação (Multi-Agent Coordination): verificação rápida 02 confirma evidência objetiva antes de marcar PASS.
- [ ] Coordenação (Multi-Agent Coordination): verificação rápida 03 confirma evidência objetiva antes de marcar PASS.
- [ ] Coordenação (Multi-Agent Coordination): verificação rápida 04 confirma evidência objetiva antes de marcar PASS.
- [ ] Coordenação (Multi-Agent Coordination): verificação rápida 05 confirma evidência objetiva antes de marcar PASS.
- [ ] Coordenação (Multi-Agent Coordination): verificação rápida 06 confirma evidência objetiva antes de marcar PASS.
- [ ] Coordenação (Multi-Agent Coordination): verificação rápida 07 confirma evidência objetiva antes de marcar PASS.
- [ ] Coordenação (Multi-Agent Coordination): verificação rápida 08 confirma evidência objetiva antes de marcar PASS.
- [ ] Coordenação (Multi-Agent Coordination): verificação rápida 09 confirma evidência objetiva antes de marcar PASS.
- [ ] Coordenação (Multi-Agent Coordination): verificação rápida 10 confirma evidência objetiva antes de marcar PASS.
- [ ] Coordenação (Multi-Agent Coordination): verificação rápida 11 confirma evidência objetiva antes de marcar PASS.
- [ ] Coordenação (Multi-Agent Coordination): verificação rápida 12 confirma evidência objetiva antes de marcar PASS.
- [ ] Coordenação (Multi-Agent Coordination): verificação rápida 13 confirma evidência objetiva antes de marcar PASS.
- [ ] Coordenação (Multi-Agent Coordination): verificação rápida 14 confirma evidência objetiva antes de marcar PASS.
- [ ] Coordenação (Multi-Agent Coordination): verificação rápida 15 confirma evidência objetiva antes de marcar PASS.
- [ ] Coordenação (Multi-Agent Coordination): verificação rápida 16 confirma evidência objetiva antes de marcar PASS.
- [ ] Coordenação (Multi-Agent Coordination): verificação rápida 17 confirma evidência objetiva antes de marcar PASS.
- [ ] Coordenação (Multi-Agent Coordination): verificação rápida 18 confirma evidência objetiva antes de marcar PASS.

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

- [ ] Segurança & Guardrails: verificação rápida 01 confirma evidência objetiva antes de marcar PASS.
- [ ] Segurança & Guardrails: verificação rápida 02 confirma evidência objetiva antes de marcar PASS.
- [ ] Segurança & Guardrails: verificação rápida 03 confirma evidência objetiva antes de marcar PASS.
- [ ] Segurança & Guardrails: verificação rápida 04 confirma evidência objetiva antes de marcar PASS.
- [ ] Segurança & Guardrails: verificação rápida 05 confirma evidência objetiva antes de marcar PASS.
- [ ] Segurança & Guardrails: verificação rápida 06 confirma evidência objetiva antes de marcar PASS.
- [ ] Segurança & Guardrails: verificação rápida 07 confirma evidência objetiva antes de marcar PASS.
- [ ] Segurança & Guardrails: verificação rápida 08 confirma evidência objetiva antes de marcar PASS.
- [ ] Segurança & Guardrails: verificação rápida 09 confirma evidência objetiva antes de marcar PASS.
- [ ] Segurança & Guardrails: verificação rápida 10 confirma evidência objetiva antes de marcar PASS.
- [ ] Segurança & Guardrails: verificação rápida 11 confirma evidência objetiva antes de marcar PASS.
- [ ] Segurança & Guardrails: verificação rápida 12 confirma evidência objetiva antes de marcar PASS.
- [ ] Segurança & Guardrails: verificação rápida 13 confirma evidência objetiva antes de marcar PASS.
- [ ] Segurança & Guardrails: verificação rápida 14 confirma evidência objetiva antes de marcar PASS.
- [ ] Segurança & Guardrails: verificação rápida 15 confirma evidência objetiva antes de marcar PASS.
- [ ] Segurança & Guardrails: verificação rápida 16 confirma evidência objetiva antes de marcar PASS.
- [ ] Segurança & Guardrails: verificação rápida 17 confirma evidência objetiva antes de marcar PASS.
- [ ] Segurança & Guardrails: verificação rápida 18 confirma evidência objetiva antes de marcar PASS.

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

### Micro-checklist de revisão rápida

- [ ] Evolução (Harness Evolution): verificação rápida 01 confirma evidência objetiva antes de marcar PASS.
- [ ] Evolução (Harness Evolution): verificação rápida 02 confirma evidência objetiva antes de marcar PASS.
- [ ] Evolução (Harness Evolution): verificação rápida 03 confirma evidência objetiva antes de marcar PASS.
- [ ] Evolução (Harness Evolution): verificação rápida 04 confirma evidência objetiva antes de marcar PASS.
- [ ] Evolução (Harness Evolution): verificação rápida 05 confirma evidência objetiva antes de marcar PASS.
- [ ] Evolução (Harness Evolution): verificação rápida 06 confirma evidência objetiva antes de marcar PASS.
- [ ] Evolução (Harness Evolution): verificação rápida 07 confirma evidência objetiva antes de marcar PASS.
- [ ] Evolução (Harness Evolution): verificação rápida 08 confirma evidência objetiva antes de marcar PASS.
- [ ] Evolução (Harness Evolution): verificação rápida 09 confirma evidência objetiva antes de marcar PASS.
- [ ] Evolução (Harness Evolution): verificação rápida 10 confirma evidência objetiva antes de marcar PASS.
- [ ] Evolução (Harness Evolution): verificação rápida 11 confirma evidência objetiva antes de marcar PASS.
- [ ] Evolução (Harness Evolution): verificação rápida 12 confirma evidência objetiva antes de marcar PASS.
- [ ] Evolução (Harness Evolution): verificação rápida 13 confirma evidência objetiva antes de marcar PASS.
- [ ] Evolução (Harness Evolution): verificação rápida 14 confirma evidência objetiva antes de marcar PASS.
- [ ] Evolução (Harness Evolution): verificação rápida 15 confirma evidência objetiva antes de marcar PASS.
- [ ] Evolução (Harness Evolution): verificação rápida 16 confirma evidência objetiva antes de marcar PASS.
- [ ] Evolução (Harness Evolution): verificação rápida 17 confirma evidência objetiva antes de marcar PASS.
- [ ] Evolução (Harness Evolution): verificação rápida 18 confirma evidência objetiva antes de marcar PASS.

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

- [ ] Observabilidade (Traces/Monitoring): verificação rápida 01 confirma evidência objetiva antes de marcar PASS.
- [ ] Observabilidade (Traces/Monitoring): verificação rápida 02 confirma evidência objetiva antes de marcar PASS.
- [ ] Observabilidade (Traces/Monitoring): verificação rápida 03 confirma evidência objetiva antes de marcar PASS.
- [ ] Observabilidade (Traces/Monitoring): verificação rápida 04 confirma evidência objetiva antes de marcar PASS.
- [ ] Observabilidade (Traces/Monitoring): verificação rápida 05 confirma evidência objetiva antes de marcar PASS.
- [ ] Observabilidade (Traces/Monitoring): verificação rápida 06 confirma evidência objetiva antes de marcar PASS.
- [ ] Observabilidade (Traces/Monitoring): verificação rápida 07 confirma evidência objetiva antes de marcar PASS.
- [ ] Observabilidade (Traces/Monitoring): verificação rápida 08 confirma evidência objetiva antes de marcar PASS.
- [ ] Observabilidade (Traces/Monitoring): verificação rápida 09 confirma evidência objetiva antes de marcar PASS.
- [ ] Observabilidade (Traces/Monitoring): verificação rápida 10 confirma evidência objetiva antes de marcar PASS.
- [ ] Observabilidade (Traces/Monitoring): verificação rápida 11 confirma evidência objetiva antes de marcar PASS.
- [ ] Observabilidade (Traces/Monitoring): verificação rápida 12 confirma evidência objetiva antes de marcar PASS.
- [ ] Observabilidade (Traces/Monitoring): verificação rápida 13 confirma evidência objetiva antes de marcar PASS.
- [ ] Observabilidade (Traces/Monitoring): verificação rápida 14 confirma evidência objetiva antes de marcar PASS.
- [ ] Observabilidade (Traces/Monitoring): verificação rápida 15 confirma evidência objetiva antes de marcar PASS.
- [ ] Observabilidade (Traces/Monitoring): verificação rápida 16 confirma evidência objetiva antes de marcar PASS.
- [ ] Observabilidade (Traces/Monitoring): verificação rápida 17 confirma evidência objetiva antes de marcar PASS.
- [ ] Observabilidade (Traces/Monitoring): verificação rápida 18 confirma evidência objetiva antes de marcar PASS.

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

### 🧠 Cartões de auditoria - Contexto (Context Management)

#### Cartão 001: Mapa de fontes de contexto - foco em evidência

**Pergunta objetiva:** O harness demonstra que “Existe lista versionada de todas as fontes que entram no prompt: mensagens recentes, summary, state, catálogo, contrato e trace refs.” com foco em evidência?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 002: Mapa de fontes de contexto - foco em teste

**Pergunta objetiva:** O harness demonstra que “Existe lista versionada de todas as fontes que entram no prompt: mensagens recentes, summary, state, catálogo, contrato e trace refs.” com foco em teste?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 003: Mapa de fontes de contexto - foco em trace

**Pergunta objetiva:** O harness demonstra que “Existe lista versionada de todas as fontes que entram no prompt: mensagens recentes, summary, state, catálogo, contrato e trace refs.” com foco em trace?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 004: Mapa de fontes de contexto - foco em owner

**Pergunta objetiva:** O harness demonstra que “Existe lista versionada de todas as fontes que entram no prompt: mensagens recentes, summary, state, catálogo, contrato e trace refs.” com foco em owner?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 005: Janela recente definida - foco em evidência

**Pergunta objetiva:** O harness demonstra que “O harness limita a janela recente por número de mensagens ou tokens e registra o corte aplicado em cada turno.” com foco em evidência?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 006: Janela recente definida - foco em teste

**Pergunta objetiva:** O harness demonstra que “O harness limita a janela recente por número de mensagens ou tokens e registra o corte aplicado em cada turno.” com foco em teste?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 007: Janela recente definida - foco em trace

**Pergunta objetiva:** O harness demonstra que “O harness limita a janela recente por número de mensagens ou tokens e registra o corte aplicado em cada turno.” com foco em trace?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 008: Janela recente definida - foco em owner

**Pergunta objetiva:** O harness demonstra que “O harness limita a janela recente por número de mensagens ou tokens e registra o corte aplicado em cada turno.” com foco em owner?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 009: Token budget medido - foco em evidência

**Pergunta objetiva:** O harness demonstra que “Cada chamada registra tokens planejados e tokens reais por bloco, com limite máximo antes de chamar o modelo.” com foco em evidência?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 010: Token budget medido - foco em teste

**Pergunta objetiva:** O harness demonstra que “Cada chamada registra tokens planejados e tokens reais por bloco, com limite máximo antes de chamar o modelo.” com foco em teste?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 011: Token budget medido - foco em trace

**Pergunta objetiva:** O harness demonstra que “Cada chamada registra tokens planejados e tokens reais por bloco, com limite máximo antes de chamar o modelo.” com foco em trace?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 012: Token budget medido - foco em owner

**Pergunta objetiva:** O harness demonstra que “Cada chamada registra tokens planejados e tokens reais por bloco, com limite máximo antes de chamar o modelo.” com foco em owner?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 013: Compaction estruturada - foco em evidência

**Pergunta objetiva:** O harness demonstra que “Resumos antigos preservam decisões, restrições, pendências, preferências e audit refs em campos separados.” com foco em evidência?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 014: Compaction estruturada - foco em teste

**Pergunta objetiva:** O harness demonstra que “Resumos antigos preservam decisões, restrições, pendências, preferências e audit refs em campos separados.” com foco em teste?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 015: Compaction estruturada - foco em trace

**Pergunta objetiva:** O harness demonstra que “Resumos antigos preservam decisões, restrições, pendências, preferências e audit refs em campos separados.” com foco em trace?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 016: Compaction estruturada - foco em owner

**Pergunta objetiva:** O harness demonstra que “Resumos antigos preservam decisões, restrições, pendências, preferências e audit refs em campos separados.” com foco em owner?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 017: Critério de promoção para state - foco em evidência

**Pergunta objetiva:** O harness demonstra que “Há regra objetiva para mover informação do contexto para state durável, como alergia, orçamento confirmado ou endereço.” com foco em evidência?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 018: Critério de promoção para state - foco em teste

**Pergunta objetiva:** O harness demonstra que “Há regra objetiva para mover informação do contexto para state durável, como alergia, orçamento confirmado ou endereço.” com foco em teste?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 019: Critério de promoção para state - foco em trace

**Pergunta objetiva:** O harness demonstra que “Há regra objetiva para mover informação do contexto para state durável, como alergia, orçamento confirmado ou endereço.” com foco em trace?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 020: Critério de promoção para state - foco em owner

**Pergunta objetiva:** O harness demonstra que “Há regra objetiva para mover informação do contexto para state durável, como alergia, orçamento confirmado ou endereço.” com foco em owner?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 021: Separação contexto/state/summary - foco em evidência

**Pergunta objetiva:** O harness demonstra que “O documento de arquitetura define o que fica em context window, o que vira state e o que vira summary.” com foco em evidência?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 022: Separação contexto/state/summary - foco em teste

**Pergunta objetiva:** O harness demonstra que “O documento de arquitetura define o que fica em context window, o que vira state e o que vira summary.” com foco em teste?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 023: Separação contexto/state/summary - foco em trace

**Pergunta objetiva:** O harness demonstra que “O documento de arquitetura define o que fica em context window, o que vira state e o que vira summary.” com foco em trace?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 024: Separação contexto/state/summary - foco em owner

**Pergunta objetiva:** O harness demonstra que “O documento de arquitetura define o que fica em context window, o que vira state e o que vira summary.” com foco em owner?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 025: Teste de recall crítico - foco em evidência

**Pergunta objetiva:** O harness demonstra que “Existe cenário automatizado em que uma restrição dita cedo é relembrada corretamente após janela longa.” com foco em evidência?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 026: Teste de recall crítico - foco em teste

**Pergunta objetiva:** O harness demonstra que “Existe cenário automatizado em que uma restrição dita cedo é relembrada corretamente após janela longa.” com foco em teste?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 027: Teste de recall crítico - foco em trace

**Pergunta objetiva:** O harness demonstra que “Existe cenário automatizado em que uma restrição dita cedo é relembrada corretamente após janela longa.” com foco em trace?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 028: Teste de recall crítico - foco em owner

**Pergunta objetiva:** O harness demonstra que “Existe cenário automatizado em que uma restrição dita cedo é relembrada corretamente após janela longa.” com foco em owner?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 029: Falha por excesso de tokens - foco em evidência

**Pergunta objetiva:** O harness demonstra que “Quando o orçamento estoura, o harness falha antes da chamada ou compacta de forma controlada, nunca corta aleatoriamente.” com foco em evidência?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 030: Falha por excesso de tokens - foco em teste

**Pergunta objetiva:** O harness demonstra que “Quando o orçamento estoura, o harness falha antes da chamada ou compacta de forma controlada, nunca corta aleatoriamente.” com foco em teste?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 031: Falha por excesso de tokens - foco em trace

**Pergunta objetiva:** O harness demonstra que “Quando o orçamento estoura, o harness falha antes da chamada ou compacta de forma controlada, nunca corta aleatoriamente.” com foco em trace?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 032: Falha por excesso de tokens - foco em owner

**Pergunta objetiva:** O harness demonstra que “Quando o orçamento estoura, o harness falha antes da chamada ou compacta de forma controlada, nunca corta aleatoriamente.” com foco em owner?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

---

### 📜 Cartões de auditoria - Contratos (Contracts/Sprint Contracts)

#### Cartão 033: Inputs explícitos - foco em evidência

**Pergunta objetiva:** O harness demonstra que “Cada contrato lista arquivos, campos e pré-condições obrigatórias para iniciar a etapa.” com foco em evidência?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 034: Inputs explícitos - foco em teste

**Pergunta objetiva:** O harness demonstra que “Cada contrato lista arquivos, campos e pré-condições obrigatórias para iniciar a etapa.” com foco em teste?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 035: Inputs explícitos - foco em trace

**Pergunta objetiva:** O harness demonstra que “Cada contrato lista arquivos, campos e pré-condições obrigatórias para iniciar a etapa.” com foco em trace?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 036: Inputs explícitos - foco em owner

**Pergunta objetiva:** O harness demonstra que “Cada contrato lista arquivos, campos e pré-condições obrigatórias para iniciar a etapa.” com foco em owner?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 037: Outputs verificáveis - foco em evidência

**Pergunta objetiva:** O harness demonstra que “Cada output tem schema, campos obrigatórios, tipos esperados e exemplos válidos em documentação ou teste.” com foco em evidência?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 038: Outputs verificáveis - foco em teste

**Pergunta objetiva:** O harness demonstra que “Cada output tem schema, campos obrigatórios, tipos esperados e exemplos válidos em documentação ou teste.” com foco em teste?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 039: Outputs verificáveis - foco em trace

**Pergunta objetiva:** O harness demonstra que “Cada output tem schema, campos obrigatórios, tipos esperados e exemplos válidos em documentação ou teste.” com foco em trace?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 040: Outputs verificáveis - foco em owner

**Pergunta objetiva:** O harness demonstra que “Cada output tem schema, campos obrigatórios, tipos esperados e exemplos válidos em documentação ou teste.” com foco em owner?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 041: Critério de sucesso - foco em evidência

**Pergunta objetiva:** O harness demonstra que “O contrato define condição objetiva de conclusão, como `evaluation.decision == approved` e `score >= 85`.” com foco em evidência?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 042: Critério de sucesso - foco em teste

**Pergunta objetiva:** O harness demonstra que “O contrato define condição objetiva de conclusão, como `evaluation.decision == approved` e `score >= 85`.” com foco em teste?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 043: Critério de sucesso - foco em trace

**Pergunta objetiva:** O harness demonstra que “O contrato define condição objetiva de conclusão, como `evaluation.decision == approved` e `score >= 85`.” com foco em trace?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 044: Critério de sucesso - foco em owner

**Pergunta objetiva:** O harness demonstra que “O contrato define condição objetiva de conclusão, como `evaluation.decision == approved` e `score >= 85`.” com foco em owner?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 045: Failure modes declarados - foco em evidência

**Pergunta objetiva:** O harness demonstra que “O contrato lista pelo menos erro de input inválido, timeout, output inválido e dependência indisponível.” com foco em evidência?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 046: Failure modes declarados - foco em teste

**Pergunta objetiva:** O harness demonstra que “O contrato lista pelo menos erro de input inválido, timeout, output inválido e dependência indisponível.” com foco em teste?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 047: Failure modes declarados - foco em trace

**Pergunta objetiva:** O harness demonstra que “O contrato lista pelo menos erro de input inválido, timeout, output inválido e dependência indisponível.” com foco em trace?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 048: Failure modes declarados - foco em owner

**Pergunta objetiva:** O harness demonstra que “O contrato lista pelo menos erro de input inválido, timeout, output inválido e dependência indisponível.” com foco em owner?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 049: Versionamento de interface - foco em evidência

**Pergunta objetiva:** O harness demonstra que “Todo artefato possui `schema_version` e há regra de compatibilidade entre versões.” com foco em evidência?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 050: Versionamento de interface - foco em teste

**Pergunta objetiva:** O harness demonstra que “Todo artefato possui `schema_version` e há regra de compatibilidade entre versões.” com foco em teste?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 051: Versionamento de interface - foco em trace

**Pergunta objetiva:** O harness demonstra que “Todo artefato possui `schema_version` e há regra de compatibilidade entre versões.” com foco em trace?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 052: Versionamento de interface - foco em owner

**Pergunta objetiva:** O harness demonstra que “Todo artefato possui `schema_version` e há regra de compatibilidade entre versões.” com foco em owner?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 053: Ownership único - foco em evidência

**Pergunta objetiva:** O harness demonstra que “Para cada contrato existe um owner responsável por manter schema, rubrica e exemplos.” com foco em evidência?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 054: Ownership único - foco em teste

**Pergunta objetiva:** O harness demonstra que “Para cada contrato existe um owner responsável por manter schema, rubrica e exemplos.” com foco em teste?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 055: Ownership único - foco em trace

**Pergunta objetiva:** O harness demonstra que “Para cada contrato existe um owner responsável por manter schema, rubrica e exemplos.” com foco em trace?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 056: Ownership único - foco em owner

**Pergunta objetiva:** O harness demonstra que “Para cada contrato existe um owner responsável por manter schema, rubrica e exemplos.” com foco em owner?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 057: Boundary test - foco em evidência

**Pergunta objetiva:** O harness demonstra que “Há teste que envia input válido mínimo, input inválido e output fora do schema para a fronteira.” com foco em evidência?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 058: Boundary test - foco em teste

**Pergunta objetiva:** O harness demonstra que “Há teste que envia input válido mínimo, input inválido e output fora do schema para a fronteira.” com foco em teste?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 059: Boundary test - foco em trace

**Pergunta objetiva:** O harness demonstra que “Há teste que envia input válido mínimo, input inválido e output fora do schema para a fronteira.” com foco em trace?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 060: Boundary test - foco em owner

**Pergunta objetiva:** O harness demonstra que “Há teste que envia input válido mínimo, input inválido e output fora do schema para a fronteira.” com foco em owner?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 061: Auditoria de alteração - foco em evidência

**Pergunta objetiva:** O harness demonstra que “Toda mudança de contrato relevante aponta para ADR, issue ou changelog com motivo e impacto.” com foco em evidência?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 062: Auditoria de alteração - foco em teste

**Pergunta objetiva:** O harness demonstra que “Toda mudança de contrato relevante aponta para ADR, issue ou changelog com motivo e impacto.” com foco em teste?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 063: Auditoria de alteração - foco em trace

**Pergunta objetiva:** O harness demonstra que “Toda mudança de contrato relevante aponta para ADR, issue ou changelog com motivo e impacto.” com foco em trace?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 064: Auditoria de alteração - foco em owner

**Pergunta objetiva:** O harness demonstra que “Toda mudança de contrato relevante aponta para ADR, issue ou changelog com motivo e impacto.” com foco em owner?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

---

### ⚖️ Cartões de auditoria - Avaliação (Evaluation/Rubrics)

#### Cartão 065: Dimensões definidas - foco em evidência

**Pergunta objetiva:** O harness demonstra que “Rubrica lista dimensões nomeadas, como segurança, adequação, completude, consistência e formato.” com foco em evidência?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 066: Dimensões definidas - foco em teste

**Pergunta objetiva:** O harness demonstra que “Rubrica lista dimensões nomeadas, como segurança, adequação, completude, consistência e formato.” com foco em teste?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 067: Dimensões definidas - foco em trace

**Pergunta objetiva:** O harness demonstra que “Rubrica lista dimensões nomeadas, como segurança, adequação, completude, consistência e formato.” com foco em trace?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 068: Dimensões definidas - foco em owner

**Pergunta objetiva:** O harness demonstra que “Rubrica lista dimensões nomeadas, como segurança, adequação, completude, consistência e formato.” com foco em owner?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 069: Pesos somam 100% - foco em evidência

**Pergunta objetiva:** O harness demonstra que “Os pesos da rubrica totalizam exatamente 100% e cada peso tem justificativa.” com foco em evidência?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 070: Pesos somam 100% - foco em teste

**Pergunta objetiva:** O harness demonstra que “Os pesos da rubrica totalizam exatamente 100% e cada peso tem justificativa.” com foco em teste?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 071: Pesos somam 100% - foco em trace

**Pergunta objetiva:** O harness demonstra que “Os pesos da rubrica totalizam exatamente 100% e cada peso tem justificativa.” com foco em trace?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 072: Pesos somam 100% - foco em owner

**Pergunta objetiva:** O harness demonstra que “Os pesos da rubrica totalizam exatamente 100% e cada peso tem justificativa.” com foco em owner?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 073: Threshold operacional - foco em evidência

**Pergunta objetiva:** O harness demonstra que “Existe nota mínima objetiva para aprovar, como `score >= 85`, e resultado abaixo disso reprova.” com foco em evidência?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 074: Threshold operacional - foco em teste

**Pergunta objetiva:** O harness demonstra que “Existe nota mínima objetiva para aprovar, como `score >= 85`, e resultado abaixo disso reprova.” com foco em teste?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 075: Threshold operacional - foco em trace

**Pergunta objetiva:** O harness demonstra que “Existe nota mínima objetiva para aprovar, como `score >= 85`, e resultado abaixo disso reprova.” com foco em trace?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 076: Threshold operacional - foco em owner

**Pergunta objetiva:** O harness demonstra que “Existe nota mínima objetiva para aprovar, como `score >= 85`, e resultado abaixo disso reprova.” com foco em owner?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 077: Blockers absolutos - foco em evidência

**Pergunta objetiva:** O harness demonstra que “Critérios como alergia violada, preço divergente ou pagamento duplicado reprovam mesmo com score alto.” com foco em evidência?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 078: Blockers absolutos - foco em teste

**Pergunta objetiva:** O harness demonstra que “Critérios como alergia violada, preço divergente ou pagamento duplicado reprovam mesmo com score alto.” com foco em teste?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 079: Blockers absolutos - foco em trace

**Pergunta objetiva:** O harness demonstra que “Critérios como alergia violada, preço divergente ou pagamento duplicado reprovam mesmo com score alto.” com foco em trace?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 080: Blockers absolutos - foco em owner

**Pergunta objetiva:** O harness demonstra que “Critérios como alergia violada, preço divergente ou pagamento duplicado reprovam mesmo com score alto.” com foco em owner?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 081: Separação Generator/Evaluator - foco em evidência

**Pergunta objetiva:** O harness demonstra que “O Evaluator recebe output e evidências, mas não depende da autoavaliação do Generator.” com foco em evidência?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 082: Separação Generator/Evaluator - foco em teste

**Pergunta objetiva:** O harness demonstra que “O Evaluator recebe output e evidências, mas não depende da autoavaliação do Generator.” com foco em teste?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 083: Separação Generator/Evaluator - foco em trace

**Pergunta objetiva:** O harness demonstra que “O Evaluator recebe output e evidências, mas não depende da autoavaliação do Generator.” com foco em trace?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 084: Separação Generator/Evaluator - foco em owner

**Pergunta objetiva:** O harness demonstra que “O Evaluator recebe output e evidências, mas não depende da autoavaliação do Generator.” com foco em owner?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 085: Evidência por dimensão - foco em evidência

**Pergunta objetiva:** O harness demonstra que “Cada nota inclui citação de campo, trace ref ou dado usado para decidir.” com foco em evidência?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 086: Evidência por dimensão - foco em teste

**Pergunta objetiva:** O harness demonstra que “Cada nota inclui citação de campo, trace ref ou dado usado para decidir.” com foco em teste?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 087: Evidência por dimensão - foco em trace

**Pergunta objetiva:** O harness demonstra que “Cada nota inclui citação de campo, trace ref ou dado usado para decidir.” com foco em trace?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 088: Evidência por dimensão - foco em owner

**Pergunta objetiva:** O harness demonstra que “Cada nota inclui citação de campo, trace ref ou dado usado para decidir.” com foco em owner?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 089: Calibração periódica - foco em evidência

**Pergunta objetiva:** O harness demonstra que “Há amostra revisada por humano para medir falso positivo e falso negativo da rubrica.” com foco em evidência?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 090: Calibração periódica - foco em teste

**Pergunta objetiva:** O harness demonstra que “Há amostra revisada por humano para medir falso positivo e falso negativo da rubrica.” com foco em teste?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 091: Calibração periódica - foco em trace

**Pergunta objetiva:** O harness demonstra que “Há amostra revisada por humano para medir falso positivo e falso negativo da rubrica.” com foco em trace?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 092: Calibração periódica - foco em owner

**Pergunta objetiva:** O harness demonstra que “Há amostra revisada por humano para medir falso positivo e falso negativo da rubrica.” com foco em owner?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 093: Replay de avaliação - foco em evidência

**Pergunta objetiva:** O harness demonstra que “É possível reexecutar a avaliação sobre o mesmo output e obter decisão comparável.” com foco em evidência?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 094: Replay de avaliação - foco em teste

**Pergunta objetiva:** O harness demonstra que “É possível reexecutar a avaliação sobre o mesmo output e obter decisão comparável.” com foco em teste?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 095: Replay de avaliação - foco em trace

**Pergunta objetiva:** O harness demonstra que “É possível reexecutar a avaliação sobre o mesmo output e obter decisão comparável.” com foco em trace?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 096: Replay de avaliação - foco em owner

**Pergunta objetiva:** O harness demonstra que “É possível reexecutar a avaliação sobre o mesmo output e obter decisão comparável.” com foco em owner?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

---

### 💾 Cartões de auditoria - Persistência (State Persistence)

#### Cartão 097: Checkpoint por fase - foco em evidência

**Pergunta objetiva:** O harness demonstra que “Cada fase longa salva checkpoint antes e depois de ações caras ou irreversíveis.” com foco em evidência?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 098: Checkpoint por fase - foco em teste

**Pergunta objetiva:** O harness demonstra que “Cada fase longa salva checkpoint antes e depois de ações caras ou irreversíveis.” com foco em teste?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 099: Checkpoint por fase - foco em trace

**Pergunta objetiva:** O harness demonstra que “Cada fase longa salva checkpoint antes e depois de ações caras ou irreversíveis.” com foco em trace?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 100: Checkpoint por fase - foco em owner

**Pergunta objetiva:** O harness demonstra que “Cada fase longa salva checkpoint antes e depois de ações caras ou irreversíveis.” com foco em owner?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 101: Schema de estado - foco em evidência

**Pergunta objetiva:** O harness demonstra que “State files ou tabelas possuem campos obrigatórios, `schema_version`, timestamps e owner.” com foco em evidência?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 102: Schema de estado - foco em teste

**Pergunta objetiva:** O harness demonstra que “State files ou tabelas possuem campos obrigatórios, `schema_version`, timestamps e owner.” com foco em teste?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 103: Schema de estado - foco em trace

**Pergunta objetiva:** O harness demonstra que “State files ou tabelas possuem campos obrigatórios, `schema_version`, timestamps e owner.” com foco em trace?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 104: Schema de estado - foco em owner

**Pergunta objetiva:** O harness demonstra que “State files ou tabelas possuem campos obrigatórios, `schema_version`, timestamps e owner.” com foco em owner?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 105: Recovery testado - foco em evidência

**Pergunta objetiva:** O harness demonstra que “Há teste que mata o processo no meio da jornada e verifica retomada a partir do último checkpoint.” com foco em evidência?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 106: Recovery testado - foco em teste

**Pergunta objetiva:** O harness demonstra que “Há teste que mata o processo no meio da jornada e verifica retomada a partir do último checkpoint.” com foco em teste?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 107: Recovery testado - foco em trace

**Pergunta objetiva:** O harness demonstra que “Há teste que mata o processo no meio da jornada e verifica retomada a partir do último checkpoint.” com foco em trace?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 108: Recovery testado - foco em owner

**Pergunta objetiva:** O harness demonstra que “Há teste que mata o processo no meio da jornada e verifica retomada a partir do último checkpoint.” com foco em owner?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 109: Replay determinístico - foco em evidência

**Pergunta objetiva:** O harness demonstra que “Um trace salvo contém inputs suficientes para reexecutar Planner, Generator e Evaluator em modo diagnóstico.” com foco em evidência?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 110: Replay determinístico - foco em teste

**Pergunta objetiva:** O harness demonstra que “Um trace salvo contém inputs suficientes para reexecutar Planner, Generator e Evaluator em modo diagnóstico.” com foco em teste?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 111: Replay determinístico - foco em trace

**Pergunta objetiva:** O harness demonstra que “Um trace salvo contém inputs suficientes para reexecutar Planner, Generator e Evaluator em modo diagnóstico.” com foco em trace?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 112: Replay determinístico - foco em owner

**Pergunta objetiva:** O harness demonstra que “Um trace salvo contém inputs suficientes para reexecutar Planner, Generator e Evaluator em modo diagnóstico.” com foco em owner?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 113: Atomic write - foco em evidência

**Pergunta objetiva:** O harness demonstra que “Arquivos JSON são escritos em `.tmp` e publicados com rename atômico.” com foco em evidência?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 114: Atomic write - foco em teste

**Pergunta objetiva:** O harness demonstra que “Arquivos JSON são escritos em `.tmp` e publicados com rename atômico.” com foco em teste?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 115: Atomic write - foco em trace

**Pergunta objetiva:** O harness demonstra que “Arquivos JSON são escritos em `.tmp` e publicados com rename atômico.” com foco em trace?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 116: Atomic write - foco em owner

**Pergunta objetiva:** O harness demonstra que “Arquivos JSON são escritos em `.tmp` e publicados com rename atômico.” com foco em owner?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 117: Retenção definida - foco em evidência

**Pergunta objetiva:** O harness demonstra que “Existe política de retenção para state, traces e dados pessoais, com justificativa de negócio.” com foco em evidência?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 118: Retenção definida - foco em teste

**Pergunta objetiva:** O harness demonstra que “Existe política de retenção para state, traces e dados pessoais, com justificativa de negócio.” com foco em teste?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 119: Retenção definida - foco em trace

**Pergunta objetiva:** O harness demonstra que “Existe política de retenção para state, traces e dados pessoais, com justificativa de negócio.” com foco em trace?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 120: Retenção definida - foco em owner

**Pergunta objetiva:** O harness demonstra que “Existe política de retenção para state, traces e dados pessoais, com justificativa de negócio.” com foco em owner?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 121: Backups verificáveis - foco em evidência

**Pergunta objetiva:** O harness demonstra que “Backup é restaurado periodicamente em ambiente seguro e a restauração é documentada.” com foco em evidência?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 122: Backups verificáveis - foco em teste

**Pergunta objetiva:** O harness demonstra que “Backup é restaurado periodicamente em ambiente seguro e a restauração é documentada.” com foco em teste?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 123: Backups verificáveis - foco em trace

**Pergunta objetiva:** O harness demonstra que “Backup é restaurado periodicamente em ambiente seguro e a restauração é documentada.” com foco em trace?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 124: Backups verificáveis - foco em owner

**Pergunta objetiva:** O harness demonstra que “Backup é restaurado periodicamente em ambiente seguro e a restauração é documentada.” com foco em owner?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 125: Escolha de backend - foco em evidência

**Pergunta objetiva:** O harness demonstra que “A arquitetura explica por que usa files, SQLite, Redis ou banco, considerando concorrência, queries e operação.” com foco em evidência?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 126: Escolha de backend - foco em teste

**Pergunta objetiva:** O harness demonstra que “A arquitetura explica por que usa files, SQLite, Redis ou banco, considerando concorrência, queries e operação.” com foco em teste?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 127: Escolha de backend - foco em trace

**Pergunta objetiva:** O harness demonstra que “A arquitetura explica por que usa files, SQLite, Redis ou banco, considerando concorrência, queries e operação.” com foco em trace?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 128: Escolha de backend - foco em owner

**Pergunta objetiva:** O harness demonstra que “A arquitetura explica por que usa files, SQLite, Redis ou banco, considerando concorrência, queries e operação.” com foco em owner?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

---

### 🤝 Cartões de auditoria - Coordenação (Multi-Agent Coordination)

#### Cartão 129: Lock para recurso compartilhado - foco em evidência

**Pergunta objetiva:** O harness demonstra que “Qualquer escrita em pedido, carrinho, perfil ou estoque usa lock, transação ou fila serializadora.” com foco em evidência?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 130: Lock para recurso compartilhado - foco em teste

**Pergunta objetiva:** O harness demonstra que “Qualquer escrita em pedido, carrinho, perfil ou estoque usa lock, transação ou fila serializadora.” com foco em teste?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 131: Lock para recurso compartilhado - foco em trace

**Pergunta objetiva:** O harness demonstra que “Qualquer escrita em pedido, carrinho, perfil ou estoque usa lock, transação ou fila serializadora.” com foco em trace?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 132: Lock para recurso compartilhado - foco em owner

**Pergunta objetiva:** O harness demonstra que “Qualquer escrita em pedido, carrinho, perfil ou estoque usa lock, transação ou fila serializadora.” com foco em owner?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 133: Status visível - foco em evidência

**Pergunta objetiva:** O harness demonstra que “Cada agente publica `pending`, `running`, `completed` ou `failed` com timestamp e motivo.” com foco em evidência?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 134: Status visível - foco em teste

**Pergunta objetiva:** O harness demonstra que “Cada agente publica `pending`, `running`, `completed` ou `failed` com timestamp e motivo.” com foco em teste?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 135: Status visível - foco em trace

**Pergunta objetiva:** O harness demonstra que “Cada agente publica `pending`, `running`, `completed` ou `failed` com timestamp e motivo.” com foco em trace?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 136: Status visível - foco em owner

**Pergunta objetiva:** O harness demonstra que “Cada agente publica `pending`, `running`, `completed` ou `failed` com timestamp e motivo.” com foco em owner?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 137: JSON protocol estável - foco em evidência

**Pergunta objetiva:** O harness demonstra que “Mensagens entre agentes seguem schema com `correlation_id`, `agent_id`, `schema_version` e `audit_refs`.” com foco em evidência?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 138: JSON protocol estável - foco em teste

**Pergunta objetiva:** O harness demonstra que “Mensagens entre agentes seguem schema com `correlation_id`, `agent_id`, `schema_version` e `audit_refs`.” com foco em teste?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 139: JSON protocol estável - foco em trace

**Pergunta objetiva:** O harness demonstra que “Mensagens entre agentes seguem schema com `correlation_id`, `agent_id`, `schema_version` e `audit_refs`.” com foco em trace?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 140: JSON protocol estável - foco em owner

**Pergunta objetiva:** O harness demonstra que “Mensagens entre agentes seguem schema com `correlation_id`, `agent_id`, `schema_version` e `audit_refs`.” com foco em owner?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 141: Atomic publish - foco em evidência

**Pergunta objetiva:** O harness demonstra que “Outputs finais só aparecem quando completos; leitores ignoram arquivos `.tmp`.” com foco em evidência?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 142: Atomic publish - foco em teste

**Pergunta objetiva:** O harness demonstra que “Outputs finais só aparecem quando completos; leitores ignoram arquivos `.tmp`.” com foco em teste?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 143: Atomic publish - foco em trace

**Pergunta objetiva:** O harness demonstra que “Outputs finais só aparecem quando completos; leitores ignoram arquivos `.tmp`.” com foco em trace?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 144: Atomic publish - foco em owner

**Pergunta objetiva:** O harness demonstra que “Outputs finais só aparecem quando completos; leitores ignoram arquivos `.tmp`.” com foco em owner?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 145: Idempotência - foco em evidência

**Pergunta objetiva:** O harness demonstra que “Reprocessar o mesmo evento não cria pedido duplicado nem reserva estoque duas vezes.” com foco em evidência?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 146: Idempotência - foco em teste

**Pergunta objetiva:** O harness demonstra que “Reprocessar o mesmo evento não cria pedido duplicado nem reserva estoque duas vezes.” com foco em teste?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 147: Idempotência - foco em trace

**Pergunta objetiva:** O harness demonstra que “Reprocessar o mesmo evento não cria pedido duplicado nem reserva estoque duas vezes.” com foco em trace?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 148: Idempotência - foco em owner

**Pergunta objetiva:** O harness demonstra que “Reprocessar o mesmo evento não cria pedido duplicado nem reserva estoque duas vezes.” com foco em owner?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 149: Timeout de lock - foco em evidência

**Pergunta objetiva:** O harness demonstra que “Locks têm TTL, owner e regra de recuperação para evitar deadlock permanente.” com foco em evidência?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 150: Timeout de lock - foco em teste

**Pergunta objetiva:** O harness demonstra que “Locks têm TTL, owner e regra de recuperação para evitar deadlock permanente.” com foco em teste?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 151: Timeout de lock - foco em trace

**Pergunta objetiva:** O harness demonstra que “Locks têm TTL, owner e regra de recuperação para evitar deadlock permanente.” com foco em trace?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 152: Timeout de lock - foco em owner

**Pergunta objetiva:** O harness demonstra que “Locks têm TTL, owner e regra de recuperação para evitar deadlock permanente.” com foco em owner?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 153: Ordem de execução - foco em evidência

**Pergunta objetiva:** O harness demonstra que “Dependências entre agentes são declaradas, por exemplo Fulfillment só roda após Evaluation aprovado.” com foco em evidência?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 154: Ordem de execução - foco em teste

**Pergunta objetiva:** O harness demonstra que “Dependências entre agentes são declaradas, por exemplo Fulfillment só roda após Evaluation aprovado.” com foco em teste?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 155: Ordem de execução - foco em trace

**Pergunta objetiva:** O harness demonstra que “Dependências entre agentes são declaradas, por exemplo Fulfillment só roda após Evaluation aprovado.” com foco em trace?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 156: Ordem de execução - foco em owner

**Pergunta objetiva:** O harness demonstra que “Dependências entre agentes são declaradas, por exemplo Fulfillment só roda após Evaluation aprovado.” com foco em owner?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 157: Teste de concorrência - foco em evidência

**Pergunta objetiva:** O harness demonstra que “Há teste que dispara dois agentes sobre o mesmo recurso e verifica ausência de race condition.” com foco em evidência?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 158: Teste de concorrência - foco em teste

**Pergunta objetiva:** O harness demonstra que “Há teste que dispara dois agentes sobre o mesmo recurso e verifica ausência de race condition.” com foco em teste?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 159: Teste de concorrência - foco em trace

**Pergunta objetiva:** O harness demonstra que “Há teste que dispara dois agentes sobre o mesmo recurso e verifica ausência de race condition.” com foco em trace?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 160: Teste de concorrência - foco em owner

**Pergunta objetiva:** O harness demonstra que “Há teste que dispara dois agentes sobre o mesmo recurso e verifica ausência de race condition.” com foco em owner?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

---

### 🛡️ Cartões de auditoria - Segurança & Guardrails

#### Cartão 161: Input validation - foco em evidência

**Pergunta objetiva:** O harness demonstra que “Mensagens, webhook payloads e tool results passam por schema e limites de tamanho antes de uso.” com foco em evidência?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 162: Input validation - foco em teste

**Pergunta objetiva:** O harness demonstra que “Mensagens, webhook payloads e tool results passam por schema e limites de tamanho antes de uso.” com foco em teste?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 163: Input validation - foco em trace

**Pergunta objetiva:** O harness demonstra que “Mensagens, webhook payloads e tool results passam por schema e limites de tamanho antes de uso.” com foco em trace?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 164: Input validation - foco em owner

**Pergunta objetiva:** O harness demonstra que “Mensagens, webhook payloads e tool results passam por schema e limites de tamanho antes de uso.” com foco em owner?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 165: Output validation - foco em evidência

**Pergunta objetiva:** O harness demonstra que “Resposta final é validada contra formato, política comercial, restrições médicas e dados de catálogo.” com foco em evidência?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 166: Output validation - foco em teste

**Pergunta objetiva:** O harness demonstra que “Resposta final é validada contra formato, política comercial, restrições médicas e dados de catálogo.” com foco em teste?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 167: Output validation - foco em trace

**Pergunta objetiva:** O harness demonstra que “Resposta final é validada contra formato, política comercial, restrições médicas e dados de catálogo.” com foco em trace?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 168: Output validation - foco em owner

**Pergunta objetiva:** O harness demonstra que “Resposta final é validada contra formato, política comercial, restrições médicas e dados de catálogo.” com foco em owner?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 169: Constraint checker - foco em evidência

**Pergunta objetiva:** O harness demonstra que “Restrições do cliente, como alergia, orçamento e região, são checadas por código ou evaluator independente.” com foco em evidência?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 170: Constraint checker - foco em teste

**Pergunta objetiva:** O harness demonstra que “Restrições do cliente, como alergia, orçamento e região, são checadas por código ou evaluator independente.” com foco em teste?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 171: Constraint checker - foco em trace

**Pergunta objetiva:** O harness demonstra que “Restrições do cliente, como alergia, orçamento e região, são checadas por código ou evaluator independente.” com foco em trace?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 172: Constraint checker - foco em owner

**Pergunta objetiva:** O harness demonstra que “Restrições do cliente, como alergia, orçamento e região, são checadas por código ou evaluator independente.” com foco em owner?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 173: Fallback handler - foco em evidência

**Pergunta objetiva:** O harness demonstra que “Cada falha conhecida tem fallback seguro: pedir confirmação, escalar para humano ou pausar a ação.” com foco em evidência?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 174: Fallback handler - foco em teste

**Pergunta objetiva:** O harness demonstra que “Cada falha conhecida tem fallback seguro: pedir confirmação, escalar para humano ou pausar a ação.” com foco em teste?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 175: Fallback handler - foco em trace

**Pergunta objetiva:** O harness demonstra que “Cada falha conhecida tem fallback seguro: pedir confirmação, escalar para humano ou pausar a ação.” com foco em trace?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 176: Fallback handler - foco em owner

**Pergunta objetiva:** O harness demonstra que “Cada falha conhecida tem fallback seguro: pedir confirmação, escalar para humano ou pausar a ação.” com foco em owner?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 177: Budget guard - foco em evidência

**Pergunta objetiva:** O harness demonstra que “Há limite explícito para tokens, custo, número de retries, tool calls e duração por turno.” com foco em evidência?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 178: Budget guard - foco em teste

**Pergunta objetiva:** O harness demonstra que “Há limite explícito para tokens, custo, número de retries, tool calls e duração por turno.” com foco em teste?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 179: Budget guard - foco em trace

**Pergunta objetiva:** O harness demonstra que “Há limite explícito para tokens, custo, número de retries, tool calls e duração por turno.” com foco em trace?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 180: Budget guard - foco em owner

**Pergunta objetiva:** O harness demonstra que “Há limite explícito para tokens, custo, número de retries, tool calls e duração por turno.” com foco em owner?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 181: Format validator - foco em evidência

**Pergunta objetiva:** O harness demonstra que “JSON, markdown operacional, links e mensagens WhatsApp têm validação objetiva antes do envio.” com foco em evidência?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 182: Format validator - foco em teste

**Pergunta objetiva:** O harness demonstra que “JSON, markdown operacional, links e mensagens WhatsApp têm validação objetiva antes do envio.” com foco em teste?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 183: Format validator - foco em trace

**Pergunta objetiva:** O harness demonstra que “JSON, markdown operacional, links e mensagens WhatsApp têm validação objetiva antes do envio.” com foco em trace?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 184: Format validator - foco em owner

**Pergunta objetiva:** O harness demonstra que “JSON, markdown operacional, links e mensagens WhatsApp têm validação objetiva antes do envio.” com foco em owner?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 185: Proteção contra prompt injection - foco em evidência

**Pergunta objetiva:** O harness demonstra que “Conteúdo de cliente e tool output é delimitado e não pode redefinir instruções do sistema.” com foco em evidência?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 186: Proteção contra prompt injection - foco em teste

**Pergunta objetiva:** O harness demonstra que “Conteúdo de cliente e tool output é delimitado e não pode redefinir instruções do sistema.” com foco em teste?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 187: Proteção contra prompt injection - foco em trace

**Pergunta objetiva:** O harness demonstra que “Conteúdo de cliente e tool output é delimitado e não pode redefinir instruções do sistema.” com foco em trace?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 188: Proteção contra prompt injection - foco em owner

**Pergunta objetiva:** O harness demonstra que “Conteúdo de cliente e tool output é delimitado e não pode redefinir instruções do sistema.” com foco em owner?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 189: Bloqueio de ação irreversível - foco em evidência

**Pergunta objetiva:** O harness demonstra que “Pagamento, estoque e envio ao cliente exigem aprovação validada antes de execução.” com foco em evidência?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 190: Bloqueio de ação irreversível - foco em teste

**Pergunta objetiva:** O harness demonstra que “Pagamento, estoque e envio ao cliente exigem aprovação validada antes de execução.” com foco em teste?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 191: Bloqueio de ação irreversível - foco em trace

**Pergunta objetiva:** O harness demonstra que “Pagamento, estoque e envio ao cliente exigem aprovação validada antes de execução.” com foco em trace?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 192: Bloqueio de ação irreversível - foco em owner

**Pergunta objetiva:** O harness demonstra que “Pagamento, estoque e envio ao cliente exigem aprovação validada antes de execução.” com foco em owner?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

---

### 🧬 Cartões de auditoria - Evolução (Harness Evolution)

#### Cartão 193: Fase declarada - foco em evidência

**Pergunta objetiva:** O harness demonstra que “Cada componente do harness tem fase atual e data da última revisão.” com foco em evidência?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 194: Fase declarada - foco em teste

**Pergunta objetiva:** O harness demonstra que “Cada componente do harness tem fase atual e data da última revisão.” com foco em teste?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 195: Fase declarada - foco em trace

**Pergunta objetiva:** O harness demonstra que “Cada componente do harness tem fase atual e data da última revisão.” com foco em trace?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 196: Fase declarada - foco em owner

**Pergunta objetiva:** O harness demonstra que “Cada componente do harness tem fase atual e data da última revisão.” com foco em owner?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 197: Métricas de efetividade - foco em evidência

**Pergunta objetiva:** O harness demonstra que “Dashboard mostra quantas falhas reais o componente preveniu no período avaliado.” com foco em evidência?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 198: Métricas de efetividade - foco em teste

**Pergunta objetiva:** O harness demonstra que “Dashboard mostra quantas falhas reais o componente preveniu no período avaliado.” com foco em teste?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 199: Métricas de efetividade - foco em trace

**Pergunta objetiva:** O harness demonstra que “Dashboard mostra quantas falhas reais o componente preveniu no período avaliado.” com foco em trace?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 200: Métricas de efetividade - foco em owner

**Pergunta objetiva:** O harness demonstra que “Dashboard mostra quantas falhas reais o componente preveniu no período avaliado.” com foco em owner?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 201: Custo total medido - foco em evidência

**Pergunta objetiva:** O harness demonstra que “Tokens, latência, manutenção, complexidade de onboarding e falsos positivos são medidos.” com foco em evidência?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 202: Custo total medido - foco em teste

**Pergunta objetiva:** O harness demonstra que “Tokens, latência, manutenção, complexidade de onboarding e falsos positivos são medidos.” com foco em teste?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 203: Custo total medido - foco em trace

**Pergunta objetiva:** O harness demonstra que “Tokens, latência, manutenção, complexidade de onboarding e falsos positivos são medidos.” com foco em trace?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 204: Custo total medido - foco em owner

**Pergunta objetiva:** O harness demonstra que “Tokens, latência, manutenção, complexidade de onboarding e falsos positivos são medidos.” com foco em owner?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 205: Critério de simplificação - foco em evidência

**Pergunta objetiva:** O harness demonstra que “Há limite objetivo, como baixa efetividade por 60 dias e shadow test sem regressão relevante.” com foco em evidência?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 206: Critério de simplificação - foco em teste

**Pergunta objetiva:** O harness demonstra que “Há limite objetivo, como baixa efetividade por 60 dias e shadow test sem regressão relevante.” com foco em teste?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 207: Critério de simplificação - foco em trace

**Pergunta objetiva:** O harness demonstra que “Há limite objetivo, como baixa efetividade por 60 dias e shadow test sem regressão relevante.” com foco em trace?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 208: Critério de simplificação - foco em owner

**Pergunta objetiva:** O harness demonstra que “Há limite objetivo, como baixa efetividade por 60 dias e shadow test sem regressão relevante.” com foco em owner?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 209: Critério de remoção - foco em evidência

**Pergunta objetiva:** O harness demonstra que “Remoção exige evidência, plano de rollback e aprovação registrada.” com foco em evidência?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 210: Critério de remoção - foco em teste

**Pergunta objetiva:** O harness demonstra que “Remoção exige evidência, plano de rollback e aprovação registrada.” com foco em teste?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 211: Critério de remoção - foco em trace

**Pergunta objetiva:** O harness demonstra que “Remoção exige evidência, plano de rollback e aprovação registrada.” com foco em trace?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 212: Critério de remoção - foco em owner

**Pergunta objetiva:** O harness demonstra que “Remoção exige evidência, plano de rollback e aprovação registrada.” com foco em owner?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 213: Rollback pronto - foco em evidência

**Pergunta objetiva:** O harness demonstra que “Existe feature flag, versão anterior ou procedimento de restauração testado.” com foco em evidência?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 214: Rollback pronto - foco em teste

**Pergunta objetiva:** O harness demonstra que “Existe feature flag, versão anterior ou procedimento de restauração testado.” com foco em teste?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 215: Rollback pronto - foco em trace

**Pergunta objetiva:** O harness demonstra que “Existe feature flag, versão anterior ou procedimento de restauração testado.” com foco em trace?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 216: Rollback pronto - foco em owner

**Pergunta objetiva:** O harness demonstra que “Existe feature flag, versão anterior ou procedimento de restauração testado.” com foco em owner?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 217: ADR ou changelog - foco em evidência

**Pergunta objetiva:** O harness demonstra que “Mudanças estruturais têm documento com contexto, decisão, alternativas e consequências.” com foco em evidência?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 218: ADR ou changelog - foco em teste

**Pergunta objetiva:** O harness demonstra que “Mudanças estruturais têm documento com contexto, decisão, alternativas e consequências.” com foco em teste?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 219: ADR ou changelog - foco em trace

**Pergunta objetiva:** O harness demonstra que “Mudanças estruturais têm documento com contexto, decisão, alternativas e consequências.” com foco em trace?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 220: ADR ou changelog - foco em owner

**Pergunta objetiva:** O harness demonstra que “Mudanças estruturais têm documento com contexto, decisão, alternativas e consequências.” com foco em owner?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 221: Revisão periódica - foco em evidência

**Pergunta objetiva:** O harness demonstra que “O time revisa componentes após upgrade de modelo ou a cada ciclo trimestral.” com foco em evidência?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 222: Revisão periódica - foco em teste

**Pergunta objetiva:** O harness demonstra que “O time revisa componentes após upgrade de modelo ou a cada ciclo trimestral.” com foco em teste?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 223: Revisão periódica - foco em trace

**Pergunta objetiva:** O harness demonstra que “O time revisa componentes após upgrade de modelo ou a cada ciclo trimestral.” com foco em trace?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 224: Revisão periódica - foco em owner

**Pergunta objetiva:** O harness demonstra que “O time revisa componentes após upgrade de modelo ou a cada ciclo trimestral.” com foco em owner?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

---

### 📡 Cartões de auditoria - Observabilidade (Traces/Monitoring)

#### Cartão 225: Trace completo - foco em evidência

**Pergunta objetiva:** O harness demonstra que “Cada jornada possui trace com fases, timestamps, agent_id, input refs, output refs e decisão final.” com foco em evidência?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 226: Trace completo - foco em teste

**Pergunta objetiva:** O harness demonstra que “Cada jornada possui trace com fases, timestamps, agent_id, input refs, output refs e decisão final.” com foco em teste?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 227: Trace completo - foco em trace

**Pergunta objetiva:** O harness demonstra que “Cada jornada possui trace com fases, timestamps, agent_id, input refs, output refs e decisão final.” com foco em trace?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 228: Trace completo - foco em owner

**Pergunta objetiva:** O harness demonstra que “Cada jornada possui trace com fases, timestamps, agent_id, input refs, output refs e decisão final.” com foco em owner?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 229: Audit log crítico - foco em evidência

**Pergunta objetiva:** O harness demonstra que “Ações sobre pagamento, estoque, dados pessoais e promessa ao cliente entram em audit log imutável.” com foco em evidência?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 230: Audit log crítico - foco em teste

**Pergunta objetiva:** O harness demonstra que “Ações sobre pagamento, estoque, dados pessoais e promessa ao cliente entram em audit log imutável.” com foco em teste?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 231: Audit log crítico - foco em trace

**Pergunta objetiva:** O harness demonstra que “Ações sobre pagamento, estoque, dados pessoais e promessa ao cliente entram em audit log imutável.” com foco em trace?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 232: Audit log crítico - foco em owner

**Pergunta objetiva:** O harness demonstra que “Ações sobre pagamento, estoque, dados pessoais e promessa ao cliente entram em audit log imutável.” com foco em owner?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 233: Dashboard operacional - foco em evidência

**Pergunta objetiva:** O harness demonstra que “Há métricas de latência, custo, aprovação de rubrica, fallback rate e error rate por feature.” com foco em evidência?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 234: Dashboard operacional - foco em teste

**Pergunta objetiva:** O harness demonstra que “Há métricas de latência, custo, aprovação de rubrica, fallback rate e error rate por feature.” com foco em teste?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 235: Dashboard operacional - foco em trace

**Pergunta objetiva:** O harness demonstra que “Há métricas de latência, custo, aprovação de rubrica, fallback rate e error rate por feature.” com foco em trace?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 236: Dashboard operacional - foco em owner

**Pergunta objetiva:** O harness demonstra que “Há métricas de latência, custo, aprovação de rubrica, fallback rate e error rate por feature.” com foco em owner?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 237: Alertas acionáveis - foco em evidência

**Pergunta objetiva:** O harness demonstra que “Alertas têm threshold, owner, severidade e runbook com primeira ação clara.” com foco em evidência?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 238: Alertas acionáveis - foco em teste

**Pergunta objetiva:** O harness demonstra que “Alertas têm threshold, owner, severidade e runbook com primeira ação clara.” com foco em teste?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 239: Alertas acionáveis - foco em trace

**Pergunta objetiva:** O harness demonstra que “Alertas têm threshold, owner, severidade e runbook com primeira ação clara.” com foco em trace?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 240: Alertas acionáveis - foco em owner

**Pergunta objetiva:** O harness demonstra que “Alertas têm threshold, owner, severidade e runbook com primeira ação clara.” com foco em owner?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 241: Debug por replay - foco em evidência

**Pergunta objetiva:** O harness demonstra que “Engenheiro consegue abrir uma pasta ou registro e reproduzir a jornada com os artefatos salvos.” com foco em evidência?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 242: Debug por replay - foco em teste

**Pergunta objetiva:** O harness demonstra que “Engenheiro consegue abrir uma pasta ou registro e reproduzir a jornada com os artefatos salvos.” com foco em teste?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 243: Debug por replay - foco em trace

**Pergunta objetiva:** O harness demonstra que “Engenheiro consegue abrir uma pasta ou registro e reproduzir a jornada com os artefatos salvos.” com foco em trace?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 244: Debug por replay - foco em owner

**Pergunta objetiva:** O harness demonstra que “Engenheiro consegue abrir uma pasta ou registro e reproduzir a jornada com os artefatos salvos.” com foco em owner?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 245: Correlação ponta a ponta - foco em evidência

**Pergunta objetiva:** O harness demonstra que “WhatsApp message id, session id, order id e trace id aparecem conectados.” com foco em evidência?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 246: Correlação ponta a ponta - foco em teste

**Pergunta objetiva:** O harness demonstra que “WhatsApp message id, session id, order id e trace id aparecem conectados.” com foco em teste?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 247: Correlação ponta a ponta - foco em trace

**Pergunta objetiva:** O harness demonstra que “WhatsApp message id, session id, order id e trace id aparecem conectados.” com foco em trace?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 248: Correlação ponta a ponta - foco em owner

**Pergunta objetiva:** O harness demonstra que “WhatsApp message id, session id, order id e trace id aparecem conectados.” com foco em owner?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 249: Amostragem de qualidade - foco em evidência

**Pergunta objetiva:** O harness demonstra que “Conversas aprovadas também são amostradas para detectar falhas silenciosas.” com foco em evidência?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 250: Amostragem de qualidade - foco em teste

**Pergunta objetiva:** O harness demonstra que “Conversas aprovadas também são amostradas para detectar falhas silenciosas.” com foco em teste?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 251: Amostragem de qualidade - foco em trace

**Pergunta objetiva:** O harness demonstra que “Conversas aprovadas também são amostradas para detectar falhas silenciosas.” com foco em trace?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 252: Amostragem de qualidade - foco em owner

**Pergunta objetiva:** O harness demonstra que “Conversas aprovadas também são amostradas para detectar falhas silenciosas.” com foco em owner?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 253: Leitura de trace treinada - foco em evidência

**Pergunta objetiva:** O harness demonstra que “O time possui guia e exemplos de trace reading para incidentes comuns.” com foco em evidência?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 254: Leitura de trace treinada - foco em teste

**Pergunta objetiva:** O harness demonstra que “O time possui guia e exemplos de trace reading para incidentes comuns.” com foco em teste?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 255: Leitura de trace treinada - foco em trace

**Pergunta objetiva:** O harness demonstra que “O time possui guia e exemplos de trace reading para incidentes comuns.” com foco em trace?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

#### Cartão 256: Leitura de trace treinada - foco em owner

**Pergunta objetiva:** O harness demonstra que “O time possui guia e exemplos de trace reading para incidentes comuns.” com foco em owner?

**Evidência aceitável:** artefato versionado, teste executável, trace real, dashboard, schema, ADR ou log de auditoria que possa ser revisado por outra pessoa.

**PASS:** uma pessoa nova no time consegue localizar a evidência, entender a regra e reproduzir a verificação sem pedir contexto oral.

**FAIL:** a resposta depende de memória do autor, comportamento esperado do modelo, print solto, comentário em chat ou “sempre funcionou assim”.

**Ação recomendada:** criar ou atualizar o artefato mínimo que torna a regra verificável antes de aumentar autonomia do agente.

---

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
- Qual métrica mudaria se Avaliação (Evaluation/Rubrics) fosse removido ou enfraquecido?
- Qual incidente passado de KODA teria sido prevenido por Avaliação (Evaluation/Rubrics) neste nível?
- Qual custo adicional este nível adiciona em tokens, latência, manutenção ou onboarding?
- Qual evidência faria Fernando aceitar este nível como suficiente para a próxima release?

#### Nível 2

- O que provaria que Avaliação (Evaluation/Rubrics) está no nível 2 neste harness?
- Qual métrica mudaria se Avaliação (Evaluation/Rubrics) fosse removido ou enfraquecido?
- Qual incidente passado de KODA teria sido prevenido por Avaliação (Evaluation/Rubrics) neste nível?
- Qual custo adicional este nível adiciona em tokens, latência, manutenção ou onboarding?
- Qual evidência faria Fernando aceitar este nível como suficiente para a próxima release?

#### Nível 3

- O que provaria que Avaliação (Evaluation/Rubrics) está no nível 3 neste harness?
- Qual métrica mudaria se Avaliação (Evaluation/Rubrics) fosse removido ou enfraquecido?
- Qual incidente passado de KODA teria sido prevenido por Avaliação (Evaluation/Rubrics) neste nível?
- Qual custo adicional este nível adiciona em tokens, latência, manutenção ou onboarding?
- Qual evidência faria Fernando aceitar este nível como suficiente para a próxima release?

#### Nível 4

- O que provaria que Avaliação (Evaluation/Rubrics) está no nível 4 neste harness?
- Qual métrica mudaria se Avaliação (Evaluation/Rubrics) fosse removido ou enfraquecido?
- Qual incidente passado de KODA teria sido prevenido por Avaliação (Evaluation/Rubrics) neste nível?
- Qual custo adicional este nível adiciona em tokens, latência, manutenção ou onboarding?
- Qual evidência faria Fernando aceitar este nível como suficiente para a próxima release?

#### Nível 5

- O que provaria que Avaliação (Evaluation/Rubrics) está no nível 5 neste harness?
- Qual métrica mudaria se Avaliação (Evaluation/Rubrics) fosse removido ou enfraquecido?
- Qual incidente passado de KODA teria sido prevenido por Avaliação (Evaluation/Rubrics) neste nível?
- Qual custo adicional este nível adiciona em tokens, latência, manutenção ou onboarding?
- Qual evidência faria Fernando aceitar este nível como suficiente para a próxima release?

### 💾 Persistência (State Persistence)

#### Nível 1

- O que provaria que Persistência (State Persistence) está no nível 1 neste harness?
- Qual métrica mudaria se Persistência (State Persistence) fosse removido ou enfraquecido?
- Qual incidente passado de KODA teria sido prevenido por Persistência (State Persistence) neste nível?
- Qual custo adicional este nível adiciona em tokens, latência, manutenção ou onboarding?
- Qual evidência faria Fernando aceitar este nível como suficiente para a próxima release?

#### Nível 2

- O que provaria que Persistência (State Persistence) está no nível 2 neste harness?
- Qual métrica mudaria se Persistência (State Persistence) fosse removido ou enfraquecido?
- Qual incidente passado de KODA teria sido prevenido por Persistência (State Persistence) neste nível?
- Qual custo adicional este nível adiciona em tokens, latência, manutenção ou onboarding?
- Qual evidência faria Fernando aceitar este nível como suficiente para a próxima release?

#### Nível 3

- O que provaria que Persistência (State Persistence) está no nível 3 neste harness?
- Qual métrica mudaria se Persistência (State Persistence) fosse removido ou enfraquecido?
- Qual incidente passado de KODA teria sido prevenido por Persistência (State Persistence) neste nível?
- Qual custo adicional este nível adiciona em tokens, latência, manutenção ou onboarding?
- Qual evidência faria Fernando aceitar este nível como suficiente para a próxima release?

#### Nível 4

- O que provaria que Persistência (State Persistence) está no nível 4 neste harness?
- Qual métrica mudaria se Persistência (State Persistence) fosse removido ou enfraquecido?
- Qual incidente passado de KODA teria sido prevenido por Persistência (State Persistence) neste nível?
- Qual custo adicional este nível adiciona em tokens, latência, manutenção ou onboarding?
- Qual evidência faria Fernando aceitar este nível como suficiente para a próxima release?

#### Nível 5

- O que provaria que Persistência (State Persistence) está no nível 5 neste harness?
- Qual métrica mudaria se Persistência (State Persistence) fosse removido ou enfraquecido?
- Qual incidente passado de KODA teria sido prevenido por Persistência (State Persistence) neste nível?
- Qual custo adicional este nível adiciona em tokens, latência, manutenção ou onboarding?
- Qual evidência faria Fernando aceitar este nível como suficiente para a próxima release?

### 🤝 Coordenação (Multi-Agent Coordination)

#### Nível 1

- O que provaria que Coordenação (Multi-Agent Coordination) está no nível 1 neste harness?
- Qual métrica mudaria se Coordenação (Multi-Agent Coordination) fosse removido ou enfraquecido?
- Qual incidente passado de KODA teria sido prevenido por Coordenação (Multi-Agent Coordination) neste nível?
- Qual custo adicional este nível adiciona em tokens, latência, manutenção ou onboarding?
- Qual evidência faria Fernando aceitar este nível como suficiente para a próxima release?

#### Nível 2

- O que provaria que Coordenação (Multi-Agent Coordination) está no nível 2 neste harness?
- Qual métrica mudaria se Coordenação (Multi-Agent Coordination) fosse removido ou enfraquecido?
- Qual incidente passado de KODA teria sido prevenido por Coordenação (Multi-Agent Coordination) neste nível?
- Qual custo adicional este nível adiciona em tokens, latência, manutenção ou onboarding?
- Qual evidência faria Fernando aceitar este nível como suficiente para a próxima release?

#### Nível 3

- O que provaria que Coordenação (Multi-Agent Coordination) está no nível 3 neste harness?
- Qual métrica mudaria se Coordenação (Multi-Agent Coordination) fosse removido ou enfraquecido?
- Qual incidente passado de KODA teria sido prevenido por Coordenação (Multi-Agent Coordination) neste nível?
- Qual custo adicional este nível adiciona em tokens, latência, manutenção ou onboarding?
- Qual evidência faria Fernando aceitar este nível como suficiente para a próxima release?

#### Nível 4

- O que provaria que Coordenação (Multi-Agent Coordination) está no nível 4 neste harness?
- Qual métrica mudaria se Coordenação (Multi-Agent Coordination) fosse removido ou enfraquecido?
- Qual incidente passado de KODA teria sido prevenido por Coordenação (Multi-Agent Coordination) neste nível?
- Qual custo adicional este nível adiciona em tokens, latência, manutenção ou onboarding?
- Qual evidência faria Fernando aceitar este nível como suficiente para a próxima release?

#### Nível 5

- O que provaria que Coordenação (Multi-Agent Coordination) está no nível 5 neste harness?
- Qual métrica mudaria se Coordenação (Multi-Agent Coordination) fosse removido ou enfraquecido?
- Qual incidente passado de KODA teria sido prevenido por Coordenação (Multi-Agent Coordination) neste nível?
- Qual custo adicional este nível adiciona em tokens, latência, manutenção ou onboarding?
- Qual evidência faria Fernando aceitar este nível como suficiente para a próxima release?

### 🛡️ Segurança & Guardrails

#### Nível 1

- O que provaria que Segurança & Guardrails está no nível 1 neste harness?
- Qual métrica mudaria se Segurança & Guardrails fosse removido ou enfraquecido?
- Qual incidente passado de KODA teria sido prevenido por Segurança & Guardrails neste nível?
- Qual custo adicional este nível adiciona em tokens, latência, manutenção ou onboarding?
- Qual evidência faria Fernando aceitar este nível como suficiente para a próxima release?

#### Nível 2

- O que provaria que Segurança & Guardrails está no nível 2 neste harness?
- Qual métrica mudaria se Segurança & Guardrails fosse removido ou enfraquecido?
- Qual incidente passado de KODA teria sido prevenido por Segurança & Guardrails neste nível?
- Qual custo adicional este nível adiciona em tokens, latência, manutenção ou onboarding?
- Qual evidência faria Fernando aceitar este nível como suficiente para a próxima release?

#### Nível 3

- O que provaria que Segurança & Guardrails está no nível 3 neste harness?
- Qual métrica mudaria se Segurança & Guardrails fosse removido ou enfraquecido?
- Qual incidente passado de KODA teria sido prevenido por Segurança & Guardrails neste nível?
- Qual custo adicional este nível adiciona em tokens, latência, manutenção ou onboarding?
- Qual evidência faria Fernando aceitar este nível como suficiente para a próxima release?

#### Nível 4

- O que provaria que Segurança & Guardrails está no nível 4 neste harness?
- Qual métrica mudaria se Segurança & Guardrails fosse removido ou enfraquecido?
- Qual incidente passado de KODA teria sido prevenido por Segurança & Guardrails neste nível?
- Qual custo adicional este nível adiciona em tokens, latência, manutenção ou onboarding?
- Qual evidência faria Fernando aceitar este nível como suficiente para a próxima release?

#### Nível 5

- O que provaria que Segurança & Guardrails está no nível 5 neste harness?
- Qual métrica mudaria se Segurança & Guardrails fosse removido ou enfraquecido?
- Qual incidente passado de KODA teria sido prevenido por Segurança & Guardrails neste nível?
- Qual custo adicional este nível adiciona em tokens, latência, manutenção ou onboarding?
- Qual evidência faria Fernando aceitar este nível como suficiente para a próxima release?

### 🧬 Evolução (Harness Evolution)

#### Nível 1

- O que provaria que Evolução (Harness Evolution) está no nível 1 neste harness?
- Qual métrica mudaria se Evolução (Harness Evolution) fosse removido ou enfraquecido?
- Qual incidente passado de KODA teria sido prevenido por Evolução (Harness Evolution) neste nível?
- Qual custo adicional este nível adiciona em tokens, latência, manutenção ou onboarding?
- Qual evidência faria Fernando aceitar este nível como suficiente para a próxima release?

#### Nível 2

- O que provaria que Evolução (Harness Evolution) está no nível 2 neste harness?
- Qual métrica mudaria se Evolução (Harness Evolution) fosse removido ou enfraquecido?
- Qual incidente passado de KODA teria sido prevenido por Evolução (Harness Evolution) neste nível?
- Qual custo adicional este nível adiciona em tokens, latência, manutenção ou onboarding?
- Qual evidência faria Fernando aceitar este nível como suficiente para a próxima release?

#### Nível 3

- O que provaria que Evolução (Harness Evolution) está no nível 3 neste harness?
- Qual métrica mudaria se Evolução (Harness Evolution) fosse removido ou enfraquecido?
- Qual incidente passado de KODA teria sido prevenido por Evolução (Harness Evolution) neste nível?
- Qual custo adicional este nível adiciona em tokens, latência, manutenção ou onboarding?
- Qual evidência faria Fernando aceitar este nível como suficiente para a próxima release?

#### Nível 4

- O que provaria que Evolução (Harness Evolution) está no nível 4 neste harness?
- Qual métrica mudaria se Evolução (Harness Evolution) fosse removido ou enfraquecido?
- Qual incidente passado de KODA teria sido prevenido por Evolução (Harness Evolution) neste nível?
- Qual custo adicional este nível adiciona em tokens, latência, manutenção ou onboarding?
- Qual evidência faria Fernando aceitar este nível como suficiente para a próxima release?

#### Nível 5

- O que provaria que Evolução (Harness Evolution) está no nível 5 neste harness?
- Qual métrica mudaria se Evolução (Harness Evolution) fosse removido ou enfraquecido?
- Qual incidente passado de KODA teria sido prevenido por Evolução (Harness Evolution) neste nível?
- Qual custo adicional este nível adiciona em tokens, latência, manutenção ou onboarding?
- Qual evidência faria Fernando aceitar este nível como suficiente para a próxima release?

### 📡 Observabilidade (Traces/Monitoring)

#### Nível 1

- O que provaria que Observabilidade (Traces/Monitoring) está no nível 1 neste harness?
- Qual métrica mudaria se Observabilidade (Traces/Monitoring) fosse removido ou enfraquecido?
- Qual incidente passado de KODA teria sido prevenido por Observabilidade (Traces/Monitoring) neste nível?
- Qual custo adicional este nível adiciona em tokens, latência, manutenção ou onboarding?
- Qual evidência faria Fernando aceitar este nível como suficiente para a próxima release?

#### Nível 2

- O que provaria que Observabilidade (Traces/Monitoring) está no nível 2 neste harness?
- Qual métrica mudaria se Observabilidade (Traces/Monitoring) fosse removido ou enfraquecido?
- Qual incidente passado de KODA teria sido prevenido por Observabilidade (Traces/Monitoring) neste nível?
- Qual custo adicional este nível adiciona em tokens, latência, manutenção ou onboarding?
- Qual evidência faria Fernando aceitar este nível como suficiente para a próxima release?

#### Nível 3

- O que provaria que Observabilidade (Traces/Monitoring) está no nível 3 neste harness?
- Qual métrica mudaria se Observabilidade (Traces/Monitoring) fosse removido ou enfraquecido?
- Qual incidente passado de KODA teria sido prevenido por Observabilidade (Traces/Monitoring) neste nível?
- Qual custo adicional este nível adiciona em tokens, latência, manutenção ou onboarding?
- Qual evidência faria Fernando aceitar este nível como suficiente para a próxima release?

#### Nível 4

- O que provaria que Observabilidade (Traces/Monitoring) está no nível 4 neste harness?
- Qual métrica mudaria se Observabilidade (Traces/Monitoring) fosse removido ou enfraquecido?
- Qual incidente passado de KODA teria sido prevenido por Observabilidade (Traces/Monitoring) neste nível?
- Qual custo adicional este nível adiciona em tokens, latência, manutenção ou onboarding?
- Qual evidência faria Fernando aceitar este nível como suficiente para a próxima release?

#### Nível 5

- O que provaria que Observabilidade (Traces/Monitoring) está no nível 5 neste harness?
- Qual métrica mudaria se Observabilidade (Traces/Monitoring) fosse removido ou enfraquecido?
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

