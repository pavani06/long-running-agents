---
title: "Resumo da Apresentação Anthropic: Building Long-Running Agents"
type: curriculum-reference
aliases: []
tags: [curriculo-conteudo, referencia, fundamentos-de-agentes, sistemas-de-agentes, memoria-externa, avaliacao-separada, coordenacao-de-agentes]
last_updated: 2026-06-10
---
# 🧭 Resumo da Apresentação Anthropic: Building Long-Running Agents
## A origem prática dos padrões que sustentam agentes que trabalham por horas

**Tempo Estimado:** 150 minutos  
**Nível:** Referência transversal para Níveis 1, 2, 3 e 4  
**Pré-requisito:** Ter lido pelo menos `../01-nivel-1-fundamentals/01-why-agents-lose-plot.md`  
**Status:** 🟢 REFERÊNCIA FUNDACIONAL - Fonte conceitual para o currículo inteiro  
**Data de Criação:** Maio 2026

---

## 📖 Prólogo: A Sala Onde o Agente Parou de Ser Mágica

Imagine uma equipe técnica reunida no fim de uma tarde longa. Na tela, uma apresentação da Anthropic. O título promete algo que parece simples: construir agentes que rodam por horas. Mas quem já colocou um agente em produção sabe que essa frase carrega um peso enorme.

No começo, todo agente parece brilhante. Ele responde rápido, segue instruções, entende o pedido, parece lembrar do que acabou de acontecer. Em uma demonstração de cinco minutos, tudo funciona. O cliente pergunta, o agente responde. O líder sorri. A equipe respira aliviada.

Depois vem a realidade.

- A conversa passa de dez minutos para duas horas.
- O agente recebe novos arquivos, novos requisitos, novas restrições e novos conflitos.
- Uma decisão tomada no início precisa ser respeitada no fim.
- Uma promessa feita no sprint anterior precisa continuar valendo no sprint seguinte.
- Um erro pequeno, se não for visto, vira uma cadeia de retrabalho.

A apresentação da Anthropic entra exatamente nesse ponto. Ela não trata agentes como truque de prompt. Trata agentes como sistemas. E sistemas precisam de estado, coordenação, auditoria, checkpoints, papéis separados e uma camada externa que não dependa da memória frágil da conversa.

A ideia central é direta: um agente que precisa trabalhar por horas não pode guardar o mundo apenas dentro da context window. Ele precisa escrever. Precisa ler. Precisa deixar rastros. Precisa dividir trabalho. Precisa ser avaliado por outro processo. Precisa de um harness que transforme uma sequência de chamadas em um fluxo confiável.

Esse é o fio que atravessa todo este currículo. O Nível 1 explica por que agentes perdem o foco. O Nível 2 mostra padrões práticos como Generator/Evaluator, sprint contracts, rubric design e trace reading. O Nível 3 transforma esses padrões em arquitetura, com state persistence, file-based coordination e multi-agent systems. O Nível 4 aplica tudo no KODA, onde conversa longa não é hipótese acadêmica. É venda, suporte, confiança e receita.

Este módulo existe para responder uma pergunta simples: de onde vieram essas ideias?

A resposta curta: elas vêm da prática de construir long-running agents de verdade. A resposta longa está nas próximas seções.

---

## 🎯 Seção 1: Overview da Apresentação

### O que a apresentação cobre

A apresentação da Anthropic sobre long-running agents descreve como construir agentes que continuam úteis quando a tarefa deixa de caber em uma única chamada de modelo. Ela parte de uma observação prática: modelos são poderosos, mas a execução longa quebra quando você espera que o modelo mantenha tudo na própria conversa.

O foco não é apenas aumentar a context window. O foco é desenhar um sistema ao redor do modelo.

A apresentação cobre quatro temas principais:

1. **Limitações de context window:** mesmo janelas grandes têm degradação, custo e ruído.
2. **Externalização de estado:** arquivos, bancos e logs viram fonte de verdade.
3. **Coordenação por artefatos:** agentes colaboram lendo e escrevendo estados explícitos.
4. **Avaliação separada:** um agente que gera não deve ser o único juiz do próprio trabalho.

A mensagem é madura. Ela não vende o agente como uma entidade que simplesmente pensa melhor. Ela mostra que agentes bons dependem de engenharia de sistemas.

### Quem está por trás

O conteúdo é atribuído à Anthropic, a organização que desenvolve Claude e publica guias práticos sobre uso de modelos em sistemas reais. No contexto deste currículo, o valor da apresentação não está em uma frase isolada. Está no conjunto de padrões que ela consolida: context management, state persistence, file-based coordination, harness design, multi-agent orchestration e avaliação externa.

### Por que importa para KODA

KODA não é um chatbot curto. KODA conversa com clientes pelo WhatsApp, ajuda na descoberta de produtos, respeita alergias, lembra preferências, calcula descontos, conduz checkout e precisa manter confiança por conversas longas. Isso faz KODA viver exatamente no território da apresentação.

- **Se KODA esquecer uma restrição alimentar**, a recomendação pode ser perigosa.
- **Se KODA perder o histórico de preferências**, a experiência parece genérica.
- **Se KODA não registrar decisões**, a equipe não consegue debugar falhas.
- **Se KODA se avaliar sozinho**, erros silenciosos chegam ao cliente.
- **Se KODA não tiver file-based coordination**, agentes paralelos podem divergir.

A apresentação importa porque ela explica a mudança de mentalidade: sair de "o modelo vai lembrar" para "o sistema vai registrar".

### Temas-chave

| Tema | Pergunta que responde | Módulo do currículo conectado |
|------|------------------------|-------------------------------|
| context window | Quanto cabe na memória imediata do agente? | `../01-nivel-1-fundamentals/02-token-budgeting.md` |
| harness | Quem conduz o trabalho quando a tarefa dura horas? | `../01-nivel-1-fundamentals/03-basic-harness-patterns.md` |
| Generator/Evaluator | Como separar criação de julgamento? | `../02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md` |
| sprint contracts | Como módulos prometem entregas claras? | `../02-nivel-2-practical-patterns/02-sprint-contracts.md` |
| trace reading | Como entender o que aconteceu depois da falha? | `../02-nivel-2-practical-patterns/04-trace-reading.md` |
| state persistence | Onde fica a memória confiável? | `../03-nivel-3-advanced-architecture/02-state-persistence.md` |
| file-based coordination | Como agentes coordenam sem telepatia? | `../03-nivel-3-advanced-architecture/03-file-based-coordination.md` |

### A tese em uma frase

Long-running agents não ficam confiáveis porque recebem prompts maiores. Eles ficam confiáveis porque trabalham dentro de um sistema que externaliza estado, limita escopo, coordena papéis, registra decisões e avalia resultados.

### Leitura orientada da Seção 1

**Nota 1: Contexto como recurso finito**
Ideia: A apresentação começa da premissa de que atenção do modelo é limitada, mesmo quando a janela parece enorme.
Aplicação em KODA: KODA deve selecionar apenas fatos que mudam a decisão atual, não despejar todo o histórico no prompt.
Pergunta de revisão: qual artefato prova que essa decisão foi respeitada?

**Nota 2: Estado como contrato**
Ideia: Um arquivo persistido transforma uma lembrança frágil em compromisso verificável.
Aplicação em KODA: Alergia, orçamento e endereço precisam estar em estado externo antes de qualquer recomendação.
Pergunta de revisão: qual artefato prova que essa decisão foi respeitada?

**Nota 3: Harness como gerente do trabalho**
Ideia: O modelo não deve decidir sozinho quando tentar de novo, parar ou chamar humano.
Aplicação em KODA: O harness de KODA define limite de retries e política de escalonamento para casos críticos.
Pergunta de revisão: qual artefato prova que essa decisão foi respeitada?

**Nota 4: Avaliação separada**
Ideia: Quem gera uma resposta tem incentivo natural para defendê-la.
Aplicação em KODA: O Evaluator precisa ler o draft com a missão explícita de encontrar erros.
Pergunta de revisão: qual artefato prova que essa decisão foi respeitada?

**Nota 5: Artefatos como memória compartilhada**
Ideia: Agentes não precisam compartilhar memória interna quando compartilham arquivos claros.
Aplicação em KODA: O agente de preço e o agente de logística leem o mesmo `current_order.json`.
Pergunta de revisão: qual artefato prova que essa decisão foi respeitada?

**Nota 6: Logs como narrativa**
Ideia: Um audit_log bom conta a história da decisão sem depender de lembrança humana.
Aplicação em KODA: Depois de uma reclamação, a equipe deve reconstruir a conversa por eventos, não por palpite.
Pergunta de revisão: qual artefato prova que essa decisão foi respeitada?

**Nota 7: Compactação com preservação**
Ideia: Resumir histórico só é seguro quando fatos críticos já foram extraídos.
Aplicação em KODA: Antes de compactar conversa, KODA grava restrições e promessas em campos estruturados.
Pergunta de revisão: qual artefato prova que essa decisão foi respeitada?

**Nota 8: Papéis pequenos**
Ideia: Agentes longos falham menos quando cada chamada tem um papel estreito.
Aplicação em KODA: Uma chamada recomenda, outra valida estoque, outra checa segurança alimentar.
Pergunta de revisão: qual artefato prova que essa decisão foi respeitada?

**Nota 9: Custo como sinal**
Ideia: Quando o prompt cresce sem controle, custo e latência viram sintomas de arquitetura fraca.
Aplicação em KODA: Token budgeting vira parte do design de produto, não otimização tardia.
Pergunta de revisão: qual artefato prova que essa decisão foi respeitada?

**Nota 10: Confiança do cliente**
Ideia: O usuário não vê o harness, mas sente quando ele funciona.
Aplicação em KODA: KODA parece cuidadoso porque suas respostas respeitam decisões antigas.
Pergunta de revisão: qual artefato prova que essa decisão foi respeitada?

**Nota 11: Falha recuperável**
Ideia: Sistemas longos precisam assumir que partes vão falhar.
Aplicação em KODA: Um veredito rejeitado não é desastre. É feedback para nova tentativa.
Pergunta de revisão: qual artefato prova que essa decisão foi respeitada?

**Nota 12: Fonte de verdade única**
Ideia: Se dois arquivos dizem coisas diferentes, o sistema precisa de regra clara.
Aplicação em KODA: O perfil do cliente vence a memória conversacional quando há conflito.
Pergunta de revisão: qual artefato prova que essa decisão foi respeitada?

**Nota 13: Critérios explícitos**
Ideia: Qualidade não melhora quando fica implícita.
Aplicação em KODA: Rubrics de KODA precisam dizer o que significa recomendação segura, útil e clara.
Pergunta de revisão: qual artefato prova que essa decisão foi respeitada?

**Nota 14: Tarefa longa como sequência**
Ideia: O agente não resolve uma tarefa de horas em um pensamento único.
Aplicação em KODA: Cada sprint do checkout produz um artefato aprovado antes do próximo.
Pergunta de revisão: qual artefato prova que essa decisão foi respeitada?

**Nota 15: Humanos no ponto certo**
Ideia: Autonomia não significa ausência de humano.
Aplicação em KODA: KODA chama operador quando veredito envolve risco alimentar, cobrança ou exceção de entrega.
Pergunta de revisão: qual artefato prova que essa decisão foi respeitada?

**Nota 16: Revisão por evidência**
Ideia: A apresentação favorece evidência sobre confiança subjetiva.
Aplicação em KODA: Toda resposta de alto risco precisa ter draft, veredito e log.
Pergunta de revisão: qual artefato prova que essa decisão foi respeitada?

**Nota 17: Sistemas antes de prompts**
Ideia: Prompt bom ajuda, mas não substitui arquitetura.
Aplicação em KODA: A melhoria principal de KODA vem de fluxo, estado e avaliação.
Pergunta de revisão: qual artefato prova que essa decisão foi respeitada?

**Nota 18: Retomada de sessão**
Ideia: Long-running agents precisam continuar depois de interrupção.
Aplicação em KODA: Se o processo reiniciar, KODA recarrega arquivos e segue do último sprint aprovado.
Pergunta de revisão: qual artefato prova que essa decisão foi respeitada?

**Nota 19: Design para debug**
Ideia: Debug não deve depender de ler uma conversa enorme inteira.
Aplicação em KODA: Trace reading aponta o sprint, o agente e o arquivo onde a decisão mudou.
Pergunta de revisão: qual artefato prova que essa decisão foi respeitada?

**Nota 20: Escopo deliberado**
Ideia: Mais agentes não significam mais qualidade se os papéis forem nebulosos.
Aplicação em KODA: KODA só adiciona agente novo quando há fronteira de responsabilidade clara.
Pergunta de revisão: qual artefato prova que essa decisão foi respeitada?

---

## 🧠 Seção 2: Context Windows e Limitações

### A context window não é memória permanente

A context window é o espaço que o modelo consegue ler em uma chamada. Ela parece memória, mas não é memória confiável. É mais parecido com uma mesa de trabalho: você pode colocar papéis nela, mas a mesa tem tamanho limitado, fica bagunçada e precisa deixar espaço para o modelo responder.

Quando a tarefa dura horas, três coisas acontecem ao mesmo tempo:

1. O histórico cresce.
2. O ruído cresce junto com o histórico.
3. O custo de reler tudo cresce a cada nova chamada.

A apresentação enfatiza que aumentar a janela ajuda, mas não resolve o problema arquitetural. Uma janela maior permite adiar a falha. Ela não substitui estado persistido.

### Diagrama: a diferença entre contexto e estado

```text
┌──────────────────────────────────────────────────────────────┐
│                         CONTEXT WINDOW                       │
│                                                              │
│  Mensagens recentes                                          │
│  Resumos                                                     │
│  Instruções do sprint atual                                  │
│  Trechos relevantes de arquivos                              │
│  Espaço para resposta                                        │
│                                                              │
│  Característica: temporária, limitada, cara, sensível a ruído│
└───────────────────────────────┬──────────────────────────────┘
                                │ lê quando precisa
                                ▼
┌──────────────────────────────────────────────────────────────┐
│                       ESTADO EXTERNALIZADO                   │
│                                                              │
│  customer_profile.json                                       │
│  conversation_state.json                                     │
│  sprint_contract.json                                        │
│  generator_draft.json                                        │
│  evaluator_verdict.json                                      │
│  audit_log.jsonl                                             │
│                                                              │
│  Característica: durável, auditável, recuperável, versionado │
└──────────────────────────────────────────────────────────────┘
```

### O problema do context rot

Context rot é a degradação gradual da qualidade quando a janela fica grande, ruidosa ou cheia de informação antiga. O agente ainda pode "ver" o texto, mas deixa de dar o peso correto a ele. Isso é diferente de esquecimento puro. Às vezes a informação está presente, mas enterrada.

```text
Qualidade de decisão
      ▲
100%  │███████████
 90%  │█████████░░
 80%  │███████░░░░
 70%  │█████░░░░░░
 60%  │███░░░░░░░░
 50%  │█░░░░░░░░░░
      └──────────────────────────────►
        10k     80k     200k    1M
        Tokens relevantes e ruído acumulado
```

### Implicações práticas para KODA

Em KODA, context window não pode ser o único lugar onde vivem fatos do cliente. Alergias, orçamento, preferências, histórico de compra, status de pagamento e promessas de entrega precisam estar em arquivos ou bancos.

Exemplo de fato que não deve depender da conversa:

```json
{
  "customer_id": "wa_5511999990000",
  "restrictions": {
    "lactose_intolerant": true,
    "allergic_to": ["amendoim"],
    "gluten_free_required": false
  },
  "preferences": {
    "flavor": "chocolate",
    "budget_max_brl": 180,
    "delivery_preference": "same_day"
  },
  "last_confirmed_at": "2026-05-28T14:12:00Z"
}
```

### O que entra na context window

Nem tudo precisa ser persistido da mesma forma. A apresentação sugere pensar em camadas:

| Tipo de informação | Deve ficar no contexto? | Deve ficar em estado externo? | Motivo |
|--------------------|-------------------------|-------------------------------|--------|
| Mensagem atual do cliente | Sim | Sim, no log | É o gatilho da ação |
| Restrição alimentar | Sim, quando relevante | Sim | É crítica para segurança |
| Lista completa de produtos | Não inteira | Sim, em catálogo | É grande e muda |
| Plano do sprint atual | Sim | Sim | Coordena execução |
| Veredito do Evaluator | Sim, para resposta final | Sim | Explica aprovação ou rejeição |
| Histórico de meses | Só resumo recuperado | Sim | Evita custo e ruído |

### Pseudocódigo de budget de contexto

```python
def montar_contexto_para_koda(mensagem, estado, contrato, limite_tokens):
    contexto = []
    contexto.append(carregar_instrucao_do_harness())
    contexto.append(resumir_estado_critico(estado.customer_profile))
    contexto.append(carregar_contrato_do_sprint(contrato))
    contexto.append(selecionar_trechos_relevantes(estado.audit_log, mensagem))
    contexto.append(mensagem)

    while contar_tokens(contexto) > limite_tokens:
        remover_trecho_menos_relevante(contexto)

    return contexto
```

### Leitura orientada da Seção 2

**Princípio 1: Fato crítico**
Definição: Informação que muda segurança, dinheiro ou promessa ao cliente.
Ação recomendada: Persistir imediatamente em `customer_context.json`.
Falha que evita: perda de informação crítica dentro da context window.

**Princípio 2: Ruído histórico**
Definição: Mensagem antiga que não muda a decisão atual.
Ação recomendada: Compactar para resumo e remover do prompt ativo.
Falha que evita: perda de informação crítica dentro da context window.

**Princípio 3: Token budget**
Definição: Limite planejado para leitura, ferramentas e resposta.
Ação recomendada: Reservar espaço para veredito e resposta final.
Falha que evita: perda de informação crítica dentro da context window.

**Princípio 4: Recuperação seletiva**
Definição: Trazer só trechos relevantes do histórico.
Ação recomendada: Buscar compras anteriores quando o cliente pede recompra.
Falha que evita: perda de informação crítica dentro da context window.

**Princípio 5: Resumo confiável**
Definição: Resumo que preserva restrições e decisões aprovadas.
Ação recomendada: Separar preferências de fatos confirmados.
Falha que evita: perda de informação crítica dentro da context window.

**Princípio 6: Janela cheia**
Definição: Estado em que o modelo lê muito e decide pior.
Ação recomendada: Cortar exemplos antigos antes de cortar restrições.
Falha que evita: perda de informação crítica dentro da context window.

**Princípio 7: Context rot**
Definição: Degradação por excesso de informação concorrente.
Ação recomendada: Medir quando respostas começam a contradizer o perfil.
Falha que evita: perda de informação crítica dentro da context window.

**Princípio 8: Estado durável**
Definição: Memória que sobrevive a compactação e reinício.
Ação recomendada: Gravar endereço confirmado e método de entrega.
Falha que evita: perda de informação crítica dentro da context window.

**Princípio 9: Estado derivado**
Definição: Informação calculada a partir de dados base.
Ação recomendada: Preço final com descontos deve apontar para regras usadas.
Falha que evita: perda de informação crítica dentro da context window.

**Princípio 10: Estado imutável**
Definição: Registro que não deve ser reescrito sem nova versão.
Ação recomendada: Veredito de uma tentativa fica guardado para replay.
Falha que evita: perda de informação crítica dentro da context window.

**Princípio 11: Estado atual**
Definição: Visão consolidada usada pelo próximo passo.
Ação recomendada: Manter `current_order.json` sincronizado com sprints aprovados.
Falha que evita: perda de informação crítica dentro da context window.

**Princípio 12: Conflito de contexto**
Definição: Quando conversa recente contradiz arquivo persistido.
Ação recomendada: Pedir confirmação antes de sobrescrever alergia ou endereço.
Falha que evita: perda de informação crítica dentro da context window.

**Princípio 13: Memória de cliente**
Definição: Dados de longo prazo que atravessam sessões.
Ação recomendada: Preferências de sabor e histórico de satisfação.
Falha que evita: perda de informação crítica dentro da context window.

**Princípio 14: Memória de tarefa**
Definição: Dados que valem só para o pedido atual.
Ação recomendada: SKU selecionado, cupom aplicado e janela de entrega.
Falha que evita: perda de informação crítica dentro da context window.

**Princípio 15: Memória de avaliação**
Definição: Por que uma resposta foi aprovada ou rejeitada.
Ação recomendada: Guardar `evaluator_verdict_vN.json`.
Falha que evita: perda de informação crítica dentro da context window.

**Princípio 16: Prompt enxuto**
Definição: Prompt que contém o necessário para decidir agora.
Ação recomendada: Context manager monta a visão mínima para o sprint.
Falha que evita: perda de informação crítica dentro da context window.

**Princípio 17: Reidratação**
Definição: Reconstruir contexto a partir de estado externo.
Ação recomendada: Após reinício, KODA relê perfil, pedido e último veredito.
Falha que evita: perda de informação crítica dentro da context window.

**Princípio 18: Custo previsível**
Definição: Gasto controlado por seleção de contexto.
Ação recomendada: Evitar enviar catálogo inteiro em toda mensagem.
Falha que evita: perda de informação crítica dentro da context window.

**Princípio 19: Teste de lembrança**
Definição: Verificar se fatos críticos aparecem sem depender do histórico.
Ação recomendada: Rodar cenário onde conversa antiga é compactada.
Falha que evita: perda de informação crítica dentro da context window.

**Princípio 20: Limite honesto**
Definição: Reconhecer quando a janela não basta.
Ação recomendada: Escalar ou pedir confirmação em vez de adivinhar.
Falha que evita: perda de informação crítica dentro da context window.

---

## 🏗️ Seção 3: Padrões Arquiteturais para Long-Running Agents

### A virada arquitetural

A apresentação mostra que long-running agents precisam de padrões que reduzem carga cognitiva. Em vez de pedir que um único agente entenda, planeje, execute, revise, registre e responda, você separa responsabilidades.

Os três padrões mais conectados ao currículo são Generator/Evaluator, file-based coordination e multi-agent patterns.

### Padrão 1: Generator/Evaluator

O Generator cria uma proposta. O Evaluator verifica a proposta contra critérios explícitos. O Generator não precisa fingir que é juiz. O Evaluator não precisa ser criativo. Cada papel fica claro.

```text
Pedido do cliente
      │
      ▼
┌──────────────────────────┐
│ Generator                │
│ Cria opção ou plano      │
└─────────────┬────────────┘
              │ draft
              ▼
┌──────────────────────────┐
│ Evaluator                │
│ Verifica contra rubric   │
└───────┬───────────┬──────┘
        │ aprovado  │ rejeitado
        ▼           ▼
  Resposta final    Feedback para nova tentativa
```

Conexão direta: veja `../02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md`.

### Padrão 2: file-based coordination

A apresentação destaca que agentes podem coordenar por arquivos. Isso parece simples, mas é poderoso: arquivos viram contrato, memória e trilha de auditoria.

```text
state/
├── customer_context.json
├── current_sprint.json
├── generator_draft_v1.json
├── evaluator_verdict_v1.json
├── feedback_v1.json
└── audit_log.jsonl
```

Esse padrão reduz ambiguidade. O próximo agente não precisa adivinhar o que aconteceu. Ele lê o artefato produzido pelo passo anterior.

### Padrão 3: multi-agent patterns

Multi-agent systems são úteis quando a tarefa tem partes independentes ou papéis que exigem perspectivas diferentes. Em KODA, isso aparece quando um agente cuida de catálogo, outro de preço, outro de logística e outro de avaliação final.

```text
             ┌────────────────────┐
             │ Orchestrator       │
             └─────────┬──────────┘
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ Agente       │ │ Agente       │ │ Agente       │
│ Catálogo     │ │ Preço        │ │ Logística    │
└──────┬───────┘ └──────┬───────┘ └──────┬───────┘
       │                │                │
       └────────────────┼────────────────┘
                        ▼
             ┌────────────────────┐
             │ Evaluator final    │
             └────────────────────┘
```

### Padrão 4: harness design

O harness é o sistema que chama o modelo, passa contexto, controla iterações, lê e escreve arquivos, aplica limites, decide quando parar e registra eventos. Sem harness, o agente fica solto. Com harness, o agente trabalha dentro de uma estrutura confiável.

```json
{
  "harness": {
    "max_iterations": 3,
    "context_budget_tokens": 60000,
    "state_dir": "./state/koda",
    "requires_evaluator": true,
    "audit_log": "audit_log.jsonl",
    "failure_policy": "escalar_para_humano"
  }
}
```

### Padrão 5: estado como fonte de verdade

Se o estado está apenas em mensagens, ele é frágil. Se o estado está em arquivos versionados, ele pode ser lido, testado, compactado, resumido e auditado. Essa é uma das lições mais importantes da apresentação.

### Leitura orientada da Seção 3
A pergunta central desta seção não é "qual padrão devo usar?".
A pergunta melhor é: "qual falha ficaria cara se este atendimento durasse duas horas e passasse por várias decisões?"
Uma arquitetura boa para KODA nasce dessa pergunta.
Ela olha para a conversa como uma sequência de compromissos verificáveis, não como uma resposta grande enviada pelo modelo.
Quando o cliente fala de alergia, orçamento, objetivo, estoque, desconto e prazo, cada uma dessas informações muda o risco do próximo passo.
Por isso a avaliação arquitetural começa antes do código.
Ela começa identificando onde a confiança pode quebrar.
Se a confiança quebra porque o agente esquece uma restrição, o desenho precisa fortalecer estado persistente e context manager.

Se quebra porque o agente recomenda algo e depois se autoaprova, o desenho precisa separar Generator e Evaluator.
Se quebra porque duas etapas escrevem preço ou estoque ao mesmo tempo, o desenho precisa de coordenação por arquivo e decisão do harness.
Se quebra porque ninguém sabe por que uma resposta saiu, o desenho precisa de audit log e artefatos nomeados.
O erro comum é escolher todos os padrões de uma vez para parecer robusto.
Isso cria uma arquitetura pesada, lenta e difícil de operar.
O outro erro é deixar tudo em uma chamada porque o primeiro protótipo respondeu bem.
Isso funciona até a primeira conversa longa, a primeira reclamação ou o primeiro pedido com exceção operacional.

A maturidade está em calibrar o peso do harness ao risco da decisão.
Em KODA, uma dica de produto sem consequência imediata pode começar com um Generator simples e um contexto bem montado.
Uma recomendação com alergia, compra e promessa de entrega precisa de contrato de sprint, Generator especializado, Evaluator independente e registro persistente.
Um checkout com pagamento ou alteração de estoque precisa ainda de locks, idempotência e uma decisão explícita de retry ou escalonamento.
Avaliar arquitetura, então, é seguir o caminho da evidência.
Primeiro, pergunte qual artefato nasce quando a etapa termina.
Depois, pergunte quem pode rejeitar esse artefato.

Em seguida, pergunte quem decide se o sistema tenta de novo, pergunta ao cliente ou chama um humano.
Por fim, pergunte se amanhã alguém conseguiria reconstruir a decisão sem depender da memória do modelo.
Essas quatro perguntas são mais úteis do que uma lista de padrões.
Elas forçam a equipe a conectar design com operação real.
Imagine uma conversa de descoberta de produto com alergia declarada logo no início.
A cliente diz: "Quero algo para recuperação pós-treino, mas tenho alergia a leite e evito soja".
A arquitetura errada trata isso como mais uma frase no histórico.

O Generator lê a conversa, escolhe um whey isolado porque parece adequado para recuperação e escreve uma resposta confiante.
Depois o mesmo modelo faz uma revisão rápida, encontra palavras como "pós-treino" e "proteína" e aprova.
O problema não é falta de inteligência linguística.
O problema é que a restrição de segurança ficou no mesmo plano das preferências comuns.
A arquitetura correta promove a alergia para `customer_context.json` e transforma a recomendação em sprint com contrato.
O contrato diz que nenhum draft pode citar produto com leite, derivados de leite ou soja sem verificação explícita.
O Generator de catálogo filtra produtos compatíveis antes de escrever o texto.

O Generator de recomendação explica tradeoffs entre proteína vegetal, aminoácidos e creatina sem prometer efeito clínico.
O Evaluator de segurança lê o draft sem o viés de quem acabou de escrevê-lo.
Ele rejeita qualquer sugestão que não mostre a compatibilidade com as restrições.
A prova de funcionamento não é a beleza da resposta final.
A prova é a combinação de `sprint_contract.json`, `generator_draft_v1.json`, `evaluator_verdict_v1.json` e uma linha de `audit_log.jsonl` marcando aprovação por restrição.
Quando a cliente volta no dia seguinte, a equipe não precisa perguntar ao modelo o que ele "lembrava".
Ela abre o estado da sessão e vê a decisão preservada.

Esse é o ponto da apresentação aplicado a KODA.
Estado externo não é burocracia.
É o que transforma uma conversa fluida em um processo auditável.
Agora pense no caso em que o cliente pede uma recomendação rápida, sem restrição crítica.
Ele pergunta: "Tenho até R$ 120 e quero algo para começar na academia".
A arquitetura errada também pode ser pesada demais.
Ela aciona cinco agentes, escreve múltiplos arquivos, exige duas avaliações e demora a responder uma pergunta simples.

O cliente percebe lentidão e abandona o atendimento.
A arquitetura correta ainda usa harness, mas reduz o rito.
O context manager pega objetivo, orçamento e histórico mínimo.
O Generator prepara uma resposta com duas opções seguras e uma pergunta de refinamento.
O Evaluator pode ser uma checagem leve de orçamento, estoque e linguagem responsável.
O contrato de sprint cabe em poucas linhas.
A evidência suficiente é o draft aprovado, o veredito curto e o log de que nenhuma restrição crítica estava presente.

Aqui a lição é que padrões são instrumentos, não troféus.
Generator e Evaluator aparecem porque existe risco de recomendação ruim, mas o sistema não precisa simular um comitê para cada mensagem.
A qualidade arquitetural está na proporcionalidade.
O harness deve ser forte o bastante para conter a falha provável e simples o bastante para não virar a própria falha.
Um terceiro exemplo aparece no checkout, onde preço e desconto podem conflitar.
O cliente diz que viu uma promoção de vinte por cento no Instagram.
Ele também tem cupom de primeira compra e frete grátis acima de certo valor.

A arquitetura errada deixa o Generator calcular tudo em texto natural.
Ele tenta ser prestativo, soma descontos incompatíveis, promete frete grátis e só depois consulta uma regra parcial.
Mesmo que o Evaluator perceba algo estranho, já não há artefato claro mostrando qual regra foi aplicada.
A arquitetura correta separa conversa, cálculo e aprovação.
O sprint contract declara que o resultado precisa conter base de preço, desconto aplicado, descontos recusados e motivo da recusa.
O Generator de preço não escreve a mensagem final ao cliente.
Ele escreve `pricing_draft_v1.json` com campos de regra, subtotal, frete, total e validade.

O Evaluator de política comercial compara o draft com a matriz de promoções vigente.
Se dois descontos não podem acumular, ele exige uma nova tentativa com explicação clara.
O Generator de resposta só entra depois do cálculo aprovado.
A coordenação por arquivo evita que a mensagem final corra na frente da verificação.
A prova de funcionamento é uma trilha em que `pricing_draft_v1.json` foi rejeitado, `feedback_v1.json` apontou a incompatibilidade e `pricing_draft_v2.json` saiu aprovado.
Esse caso mostra quando combinar Generator, Evaluator e sprint contracts é indispensável.
Não basta avaliar a frase final.

É preciso avaliar o objeto de decisão que sustenta a frase.
O cliente pode não ver o JSON, mas a operação depende dele.
Sem esse artefato, a equipe só tem uma conversa bonita e um risco financeiro escondido.
O quarto exemplo envolve corrida de estado.
Duas conversas paralelas tentam reservar o último pote de creatina de um lote.
A arquitetura errada mantém estoque em memória de cada execução.
Cada agente lê "1 unidade disponível", ambos respondem que a compra está garantida e o problema só aparece na separação do pedido.

Esse não é um problema de prompt.
É um problema de coordenação.
A arquitetura correta usa arquivo de intenção e decisão transacional controlada pelo harness.
Cada sessão escreve uma intenção de reserva com `session_id`, SKU, quantidade, timestamp e prazo.
O harness verifica se a reserva ainda é válida antes de liberar a resposta.
Uma sessão recebe `stock_reservation_confirmed.json`.
A outra recebe `stock_reservation_rejected.json` com alternativa ou pergunta ao cliente.

O Evaluator de estoque não julga simpatia da mensagem; ele julga consistência entre estoque, reserva e resposta.
A prova de funcionamento é que nunca existem duas reservas aprovadas para a mesma unidade.
O audit log deve mostrar leitura do estoque, tentativa de lock, decisão e saída.
File-based coordination aqui previne uma falha que nenhum texto educado resolveria.
A conversa continua humana, mas a fonte de verdade não é uma lembrança humana do modelo.
O quinto exemplo é fulfillment, onde o pedido já foi comprado e o risco muda de recomendação para promessa operacional.
A cliente comprou suplemento para receber antes de uma viagem.

No meio do processo, uma rota de entrega fica indisponível.
A arquitetura errada usa o mesmo harness da recomendação.
Ele gera uma explicação simpática, sugere novo prazo e registra só a resposta enviada.
Isso parece suficiente até o time de logística perguntar de onde veio o novo compromisso.
A arquitetura correta reconhece que fulfillment tem outra superfície.
O context manager não prioriza sabor ou objetivo nutricional; prioriza pedido, SLA, endereço, transportadora, janela de entrega e histórico de promessas.
O Generator de logística propõe alternativas operacionais, como trocar transportadora, mudar janela ou oferecer retirada.

O Evaluator verifica SLA, custo, autorização comercial e clareza para o cliente.
O sprint contract exige que toda promessa contenha fonte operacional.
A resposta final só sai depois que `fulfillment_plan_v1.json` e `evaluator_verdict_v1.json` concordam.
A prova de funcionamento é uma trace que liga a mudança de rota à nova promessa.
Se o cliente reclamar, a equipe vê que KODA não inventou prazo.
Ele leu um evento de fulfillment, gerou opções, avaliou regras e respondeu dentro do limite autorizado.
Esses exemplos também mostram que o harness não é igual em todos os domínios.

No domínio de recomendação, o ponto crítico é compatibilidade entre necessidade, restrição e catálogo.
No checkout, o ponto crítico é consistência entre preço, desconto, frete, pagamento e autorização.
No fulfillment, o ponto crítico é promessa operacional rastreável.
Usar o mesmo rubric para os três cria falsos positivos.
Uma resposta pode ser perfeita em tom e perigosa em preço.
Outra pode ser correta em estoque e incompleta em segurança alimentar.
Outra pode ser clara para o cliente e impossível para a transportadora.

Por isso a avaliação arquitetural deve perguntar qual rubric representa o risco daquela etapa.
A apresentação fala de padrões gerais; KODA precisa traduzi-los em critérios concretos.
Para recomendação, critérios típicos incluem restrições, objetivo, orçamento, estoque e linguagem responsável.
Para checkout, entram cálculo, política comercial, idempotência, confirmação de pagamento e reversibilidade.
Para fulfillment, entram SLA, endereço, transportadora, comunicação de exceção e escalonamento humano.
A arquitetura está madura quando esses critérios aparecem antes do prompt final.
Eles precisam estar no contrato, no evaluator e no log.

Outro sinal de maturidade é a existência de caminhos de rejeição.
Arquiteturas geradas por entusiasmo costumam desenhar apenas o caminho feliz.
O cliente fala, o Generator responde, o Evaluator aprova, o pedido segue.
Mas KODA vive nos caminhos imperfeitos.
O produto compatível está sem estoque.
O desconto prometido não combina com a regra vigente.
O endereço não aceita entrega rápida.

O cliente muda a restrição no meio da conversa.
O pagamento aparece duplicado.
A arquitetura precisa mostrar o que acontece nesses momentos.
Se não há `feedback_v1.json`, retry controlado ou escalonamento, a rejeição vira improviso.
E improviso em conversa longa vira perda de confiança.
Ao revisar uma proposta de arquitetura, procure também por fronteiras de papel.
O Generator deve produzir uma hipótese útil, não aprovar a própria hipótese.

O Evaluator deve aplicar critérios, não reescrever a resposta por gosto pessoal.
O context manager deve selecionar fatos, não decidir política comercial.
O harness deve coordenar chamadas, arquivos, limites e decisão final.
Quando esses papéis se misturam, o sistema ainda pode funcionar em demonstração.
Ele apenas fica difícil de explicar no incidente.
A fronteira mais importante é entre persuasão e verdade.
KODA precisa vender, mas não pode vender ao custo de ignorar restrição ou prometer operação inexistente.

O Generator tende a otimizar fluidez, acolhimento e fechamento.
O Evaluator precisa segurar o limite do que é seguro, permitido e comprovado.
Essa tensão é saudável.
Ela é o motivo de separar agentes.
Uma arquitetura sem tensão vira monólogo.
Uma arquitetura com tensão bem registrada vira sistema confiável.
Também vale avaliar como a arquitetura lida com tempo.

Uma conversa de duas horas não é apenas uma conversa grande.
Ela muda de fase.
Começa com descoberta, passa por comparação, vira decisão, entra em checkout e pode terminar em fulfillment.
Cada fase tem fatos que expiram e fatos que permanecem.
Preferência de sabor pode mudar.
Alergia não deve sumir.
Preço promocional pode ter validade curta.

Pagamento aprovado deve ser tratado como evento forte.
A arquitetura correta marca essas diferenças no estado.
Sem isso, o context manager não sabe o que compactar nem o que preservar.
A pergunta de revisão é simples: se a janela de contexto precisasse ser reconstruída agora, quais fatos voltariam e por quê?
Se a resposta depende de "o modelo vai saber", o desenho ainda é frágil.
O último critério é observabilidade.
Não basta ter arquivos; eles precisam contar uma história legível.
`customer_context.json` mostra quem é o cliente e quais restrições comandam a conversa.

`conversation_summary.md` mostra o que foi decidido sem carregar todo o ruído.
`sprint_contract.json` mostra o compromisso da próxima etapa.
`generator_draft_v1.json` mostra a hipótese construída.
`evaluator_verdict_v1.json` mostra por que a hipótese foi aceita ou rejeitada.
`feedback_v1.json` mostra como corrigir sem recomeçar às cegas.
`audit_log.jsonl` costura esses eventos em ordem.
Quando esses artefatos existem, a equipe consegue aprender com falhas.

Quando não existem, a equipe só discute prints de conversa.
A revisão arquitetural deve terminar com um teste de replay.
Escolha uma sessão realista, apague a memória mental do time e tente reconstruir a decisão só pelos artefatos.
Se vocês conseguem explicar o que o cliente disse, o que KODA entendeu, o que gerou, o que avaliou e por que respondeu, o desenho está no caminho certo.
Se falta uma peça, a arquitetura ainda depende demais da boa vontade do modelo.
Esse é o modo prático de usar os padrões da apresentação.
Não pergunte se KODA "tem Generator/Evaluator" como item de checklist.
Pergunte qual decisão o Generator assume, qual risco o Evaluator cobre e qual arquivo prova que o harness respeitou ambos.
Não pergunte se existe state persistence.
Pergunte qual fato crítico sobreviveria a uma compactação agressiva, a uma troca de modelo e a uma investigação no dia seguinte.
Não pergunte se há file-based coordination.
Pergunte qual corrida, duplicidade ou perda de contexto ela impede.
Quando as respostas são concretas, a arquitetura deixa de ser desenho bonito.
Ela vira uma máquina de preservar confiança em conversas longas.
E confiança, para KODA, é o produto real.

Uma revisão final pode usar uma sessão fictícia, mas precisa ser implacável.
Escolha uma conversa com pelo menos uma restrição, uma mudança de decisão e uma exceção operacional.
Peça para a arquitetura mostrar onde cada fato nasce.
Peça para mostrar onde cada fato pode ser corrigido.
Peça para mostrar onde cada fato deixa de ser válido.
Se o desenho não sabe expirar uma promoção, ele confundirá preço antigo com promessa atual.
Se não sabe proteger uma alergia, ele tratará segurança como preferência.
Se não sabe registrar uma rejeição, ele repetirá o mesmo erro com mais confiança.
A equipe deve sair da revisão com um mapa de riscos, não com uma sensação vaga de robustez.
O mapa diz quais decisões exigem veredito independente.
Diz quais arquivos precisam existir antes da resposta final.
Diz quais eventos autorizam retry e quais exigem humano.
Diz quais fatos entram sempre no contexto, mesmo quando a conversa é compactada.
Esse mapa também ajuda produto e operação a conversarem.
Produto enxerga onde a experiência precisa ser rápida.
Operação enxerga onde uma promessa precisa de fonte.
Engenharia enxerga onde o harness deve impor limite.
Atendimento enxerga onde pode explicar uma decisão ao cliente sem inventar bastidores.
Quando esses grupos discordam, a discordância deve aparecer no sprint contract.
É melhor discutir antes se KODA pode oferecer retirada em loja do que descobrir durante uma reclamação.
Também é melhor declarar que uma etapa não precisa de Evaluator pesado do que fingir que todo fluxo tem o mesmo risco.
A boa arquitetura não elimina julgamento humano.
Ela coloca o julgamento nos lugares certos.
Ela deixa o modelo gerar onde linguagem ajuda.
Ela deixa o Evaluator bloquear onde risco exige frieza.
Ela deixa o harness decidir onde processo precisa vencer improviso.
Ela deixa arquivos sustentarem memória quando a conversa fica longa.
No fim, a pergunta de aprovação é prática: alguém consegue operar, auditar e melhorar KODA a partir desse desenho?
Se a resposta for sim, os padrões foram absorvidos.
Se a resposta for não, ainda estamos olhando para nomes bonitos sem consequência operacional.

---

## 📊 Seção 4: Comparativo de Estratégias de Coordenação

A apresentação não diz que toda tarefa precisa da estratégia mais pesada. O desenho certo depende de custo, latência, risco e necessidade de auditoria. A tabela abaixo compara escolhas típicas.

| Strategy | Confiabilidade | Latência | Custo por Tarefa | Escalabilidade | Auditabilidade | Complexidade | Melhor Caso de Uso |
|----------|-----------------|----------|------------------|----------------|-----------------|--------------|--------------------|
| Single agent | Baixa em tarefas longas, média em tarefas curtas | Baixa | Baixo | Limitada pela context window | Baixa | Baixa | Respostas simples, perguntas diretas, ações reversíveis |
| Generator/Evaluator | Alta quando rubric é clara | Média | Médio | Boa para tarefas com qualidade mensurável | Alta | Média | Recomendações, revisão de respostas, validação de pedidos |
| Multi-agent | Alta quando papéis são bem separados | Média a alta | Alto | Alta para trabalho paralelo | Média a alta | Alta | Catálogo, preço, logística e suporte trabalhando juntos |
| Human-in-the-loop | Muito alta em decisões críticas | Alta | Alto | Limitada por disponibilidade humana | Muito alta | Média | Pagamento suspeito, alergia crítica, exceção operacional |
| File-based coordination | Alta para continuidade e replay | Média | Baixo a médio | Alta quando arquivos são versionados | Muito alta | Média | Sprints longos, retomada de sessão, debug e auditoria |
| Event-driven | Alta para sistemas distribuídos maduros | Baixa a média | Médio | Muito alta | Alta se eventos forem persistidos | Alta | Workflows assíncronos, fulfillment, notificações e retries |
| Orchestrator central | Alta quando o harness é bem testado | Média | Médio | Alta com filas e limites | Alta | Alta | Coordenação de sprints, retries, políticas e escalonamento |
| Rubric gate | Alta para qualidade explícita | Média | Médio | Boa se rubrics forem reutilizáveis | Alta | Média | Aprovar conteúdo, ranking, recomendação e resposta final |

### Como ler a tabela

A coluna mais importante não é custo. É risco. Se uma falha custa pouco, um single agent pode ser suficiente. Se uma falha custa confiança, dinheiro ou segurança, a arquitetura precisa de checkpoints.

### Guia de decisão rápido

1. Use single agent quando a tarefa for curta, reversível e barata.
2. Use Generator/Evaluator quando qualidade for mais importante que velocidade.
3. Use multi-agent quando partes da tarefa exigirem conhecimento ou dados diferentes.
4. Use human-in-the-loop quando o risco não puder ser delegado apenas ao modelo.
5. Use file-based coordination quando precisar de continuidade, replay e debug.
6. Use event-driven quando a tarefa tiver esperas, callbacks e efeitos externos.

### Leitura orientada da Seção 4

A tabela de estratégias não é uma escada onde a opção mais sofisticada sempre vence.

Ela é uma ferramenta para decidir qual risco você está comprando quando escolhe simplicidade, velocidade, auditabilidade ou controle humano.

Em KODA, essa escolha aparece em momentos muito concretos: o cliente muda de ideia, o catálogo muda no meio da conversa, uma regra comercial entra em conflito com outra, uma alergia aparece tarde, ou uma confirmação de pagamento demora.

A pergunta útil não é "qual estratégia parece mais elegante?".

A pergunta útil é: "se isso der errado, que tipo de dano acontece e qual arquitetura me permite perceber, explicar e recuperar?".

Os três cenários abaixo treinam essa leitura.

Eles partem das oito estratégias da tabela: `single agent`, `Generator/Evaluator`, `multi-agent`, `human-in-the-loop`, `file-based coordination`, `event-driven`, `orchestrator central` e `rubric gate`.

O objetivo não é decorar nomes.

O objetivo é reconhecer o formato do problema antes de escolher o padrão.

#### Cenário A: recomendação rápida que vira decisão de segurança

Imagine uma cliente nova chegando pelo WhatsApp às 10h13.

Ela pergunta: "Vocês têm proteína sabor baunilha?".

Nesse primeiro instante, a tarefa parece pequena.

KODA só precisa responder se existe produto no catálogo, talvez com duas opções e faixa de preço.

A escolha errada seria começar com a arquitetura mais pesada: abrir múltiplos agentes, gerar drafts versionados, pedir avaliação completa e acionar operador humano.

Isso adiciona latência antes de existir risco real.

O cliente percebe demora para uma pergunta simples.

A equipe gasta custo de modelo sem ganhar qualidade proporcional.

Aqui, `single agent` pode ser suficiente se a ação for curta, reversível e sem promessa crítica.

A resposta pode dizer que há opções de baunilha e perguntar se a cliente tem alguma restrição alimentar ou faixa de preço.

Mas o cenário muda quando a cliente responde: "Tenho alergia a amendoim e preciso de algo sem traços".

A partir desse ponto, continuar com `single agent` vira escolha frágil.

A conversa deixou de ser apenas descoberta de produto.

Agora existe risco de segurança alimentar.

A decisão correta passa a combinar `state persistence`, `Generator/Evaluator` e `rubric gate`.

O fato crítico precisa sair da conversa e entrar em `customer_context.json`.

O Generator pode propor produtos candidatos.

O Evaluator deve checar cada SKU contra campos de alergênicos, avisos de contaminação cruzada e disponibilidade real.

O `rubric gate` torna explícito que uma recomendação só passa se a pontuação de segurança for máxima.

Se o catálogo não tiver dado suficiente sobre traços de amendoim, a estratégia correta deixa de ser automatizar a recomendação.

Nesse ponto, `human-in-the-loop` é a proteção madura.

A resposta de KODA deve reconhecer o limite: "Para não arriscar sua segurança, vou confirmar essa informação antes de indicar".

O erro comum é tratar alergia como mais uma preferência.

Preferência de sabor pode ser negociada.

Alergia não pode.

Preferência aceita ranking.

Alergia exige veto.

Preferência pode ser resolvida com resposta rápida.

Alergia precisa de evidência.

O artefato esperado para esse cenário não é apenas uma mensagem bonita.

É uma sequência: `customer_context.json` com a restrição, `generator_draft_v1.json` com candidatos, `evaluator_verdict_v1.json` com checagem de alergênicos e uma linha em `audit_log.jsonl` registrando aprovação ou escalonamento.

A estratégia certa, portanto, não é uma só desde o começo.

Ela muda conforme o risco muda.

A maturidade arquitetural está em permitir essa troca sem improviso.

O harness precisa perceber que a conversa saiu de descoberta simples para decisão crítica.

Se a equipe não consegue apontar onde essa transição acontece, a tabela ainda não virou prática.

#### Cenário B: carrinho em andamento com endereço alterado no último minuto

Agora imagine um cliente recorrente que já escolheu dois produtos.

Ele colocou creatina e multivitamínico no carrinho.

KODA calculou frete para o endereço salvo em São Paulo.

O cliente então diz: "Na verdade manda para Campinas, estou na casa da minha mãe hoje".

A escolha errada é deixar o mesmo agente recalcular tudo em memória e responder rápido demais.

Parece eficiente, mas mistura três responsabilidades: entender a mudança, recalcular logística e preservar rastreabilidade do pedido.

Se o valor de frete mudar, se o prazo de entrega mudar ou se uma promoção dependia da região, a equipe precisa saber qual dado causou a mudança.

Aqui, `file-based coordination` deixa de ser detalhe técnico.

Ele vira mecanismo de confiança.

O endereço anterior deve continuar registrado como histórico.

O endereço novo deve aparecer em `current_order.json` ou artefato equivalente, com timestamp e origem conversacional.

O cálculo de frete deve ler esse arquivo, não uma lembrança solta da última mensagem.

Se a entrega depende de callback de transportadora, `event-driven` entra naturalmente.

O workflow pode emitir `address_changed`, depois esperar `shipping_quote_received`, depois atualizar `order_totals_recomputed`.

Forçar tudo em uma chamada síncrona aumenta a chance de promessa quebrada.

A estratégia correta combina `orchestrator central`, `file-based coordination` e, quando há espera externa, `event-driven`.

O orchestrator define a ordem: bloquear confirmação final, recalcular frete, revalidar prazo, revalidar total, pedir aceite do cliente.

Ele também impede que KODA confirme pagamento enquanto o pedido está em estado intermediário.

O erro comum é escolher `multi-agent` só porque existem várias partes.

Multi-agent pode ajudar se catálogo, preço e logística forem domínios realmente separados.

Mas, neste cenário, o problema principal não é paralelismo.

O problema principal é consistência de estado.

Se três agentes trabalham sobre versões diferentes do endereço, a arquitetura piorou.

Antes de multiplicar agentes, você precisa de uma fonte de verdade.

Só depois faz sentido especializar papéis.

Um `rubric gate` também pode ser útil, mas ele não substitui a coordenação.

A rubric final deve checar se o endereço usado no cálculo de frete é o mesmo endereço confirmado pelo cliente.

Ela deve checar se o total apresentado inclui o frete novo.

Ela deve checar se a mensagem final não promete prazo antigo.

Esse gate é a última barreira, não o sistema inteiro.

A evidência esperada para o cenário é concreta.

Você quer ver `audit_log.jsonl` com eventos de mudança de endereço, `shipping_quote_v2.json` apontando para o novo CEP e `final_response.json` citando o prazo atualizado.

Se amanhã o cliente disser "vocês prometeram entrega hoje", a equipe não deve reler 80 mensagens tentando lembrar.

Ela deve reconstruir o fluxo por artefatos.

A estratégia certa é aquela que permite reprocessar a decisão sem depender da memória do modelo.

#### Cenário C: promoção de campanha conflita com regra de margem

Considere uma campanha de fim de mês.

O cliente pergunta por um combo de whey, creatina e coqueteleira.

Ele tem um cupom de 20% enviado por marketing.

Ao mesmo tempo, existe uma regra interna: certos SKUs com margem baixa não podem acumular desconto com frete grátis.

A escolha errada é tratar isso como recomendação comum e deixar o Generator decidir uma oferta "atraente".

O Generator tende a otimizar a satisfação imediata do cliente.

Ele pode montar um combo excelente do ponto de vista comercial aparente, mas inválido do ponto de vista de regra.

Também é errado acionar humano em todo conflito de desconto.

Isso protege a empresa, mas destrói escala se o caso for frequente e codificável.

Aqui, a primeira pergunta é: a regra está expressa em artefato verificável?

Se a regra vive apenas na cabeça de alguém, `human-in-the-loop` é necessário até que a regra seja formalizada.

Se a regra está em arquivo ou serviço confiável, KODA pode automatizar com `Generator/Evaluator`, `rubric gate` e talvez `multi-agent`.

O agente de preço calcula combinações possíveis.

O agente de catálogo confirma elegibilidade dos SKUs.

O Evaluator aplica a rubric comercial: cupom válido, margem respeitada, frete permitido, mensagem sem promessa ambígua.

O `rubric gate` é decisivo porque qualidade aqui não é só clareza textual.

Qualidade é conformidade com política comercial.

A resposta final deve explicar a alternativa sem parecer arbitrária.

Por exemplo: "Consigo aplicar o cupom no combo, mas ele não acumula com frete grátis para este SKU. A melhor opção dentro da regra fica em R$ X com entrega Y".

O erro comum é escolher `event-driven` porque há vários eventos comerciais.

Nem todo conflito precisa de arquitetura orientada a eventos.

Se a decisão acontece dentro de uma única conversa, com dados disponíveis agora, `event-driven` pode ser excesso.

Ele passa a fazer sentido se o preço depende de aprovação assíncrona, atualização de ERP ou callback de gateway.

Também é comum escolher `orchestrator central` e achar que isso resolve a política.

O orchestrator conduz o fluxo, mas não sabe sozinho o que é desconto válido.

A política precisa estar em regras, rubrics ou serviços que o Evaluator consiga consultar.

A evidência esperada é uma trilha que mostre a origem do preço.

`pricing_decision_v1.json` deve listar cupom, regra de acúmulo, SKUs afetados e total.

`evaluator_verdict_v1.json` deve dizer por que a combinação foi aprovada ou rejeitada.

`audit_log.jsonl` deve registrar o evento `discount_conflict_resolved`.

Se a equipe só tem a mensagem final enviada ao cliente, ela não tem auditoria suficiente.

Neste cenário, a estratégia correta não é a mais simples nem a mais pesada.

É a composição mínima que separa geração de oferta, validação de política e explicação ao cliente.

A tabela da Seção 4 deve ser lida assim: cada estratégia cobre uma falha dominante.

`single agent` cobre velocidade em risco baixo.

`Generator/Evaluator` cobre qualidade verificável.

`multi-agent` cobre divisão real de domínio.

`human-in-the-loop` cobre risco que não deve ser delegado.

`file-based coordination` cobre continuidade e replay.

`event-driven` cobre espera e efeitos externos.

`orchestrator central` cobre fluxo, limite e retry.

`rubric gate` cobre aprovação explícita antes da resposta final.

Quando você escolhe uma estratégia, diga qual falha ela está prevenindo.

Se você não consegue responder, provavelmente está escolhendo pelo nome, não pelo problema.

O exercício prático é pegar uma feature real de KODA e escrever três frases antes de implementar.

Primeira: "A falha mais cara aqui seria...".

Segunda: "O artefato que provaria a decisão correta é...".

Terceira: "A estratégia mínima que produz esse artefato é...".

Essas três frases evitam tanto engenharia insuficiente quanto arquitetura teatral.

Elas mantêm a decisão ligada ao cliente, ao risco e à evidência.


---

## 🗺️ Seção 5: Diagrama ASCII da Arquitetura Completa

Abaixo está uma visão textual da arquitetura de um long-running agent system inspirado pela apresentação. O objetivo é mostrar todos os elementos exigidos: entrada do usuário, context manager, state persistence layer, Generator agents, Evaluator agents, file-based coordination, orchestrator, harness, output e feedback loops.

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                         CLIENTE OU USUÁRIO                                  │
│                 WhatsApp, painel interno, API, operador humano              │
└───────────────────────────────────┬─────────────────────────────────────────┘
                                    │ mensagem, intenção, arquivo, evento
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         ORCHESTRATOR / HARNESS                              │
│                                                                             │
│  Responsabilidades:                                                         │
│  1. Receber entrada                                                         │
│  2. Carregar estado externo                                                 │
│  3. Montar context window                                                   │
│  4. Definir sprint contract                                                 │
│  5. Chamar Generator agents                                                 │
│  6. Chamar Evaluator agents                                                 │
│  7. Decidir retry, aprovação ou escalonamento humano                        │
│  8. Registrar audit_log                                                     │
└───────────────┬───────────────────────────────────────────────┬─────────────┘
                │                                               │
                │ lê e escreve                                  │ monta contexto
                ▼                                               ▼
┌─────────────────────────────────────────────┐       ┌───────────────────────┐
│       FILE-BASED COORDINATION               │       │ CONTEXT MANAGER       │
│                                             │       │                       │
│  state/session_123/                         │       │  Seleciona fatos      │
│  ├── customer_context.json                  │       │  Compacta histórico   │
│  ├── conversation_summary.md                │       │  Aplica token budget  │
│  ├── sprint_contract.json                   │       │  Remove ruído         │
│  ├── generator_draft_v1.json                │       │  Mantém instruções    │
│  ├── evaluator_verdict_v1.json              │       │  Prepara prompt       │
│  ├── feedback_v1.json                       │       │                       │
│  └── audit_log.jsonl                        │       └───────────┬───────────┘
│                                             │                   │
│  Fonte de verdade para agentes              │                   │ contexto
└──────────────┬──────────────────────────────┘                   ▼
               │                                         ┌────────────────────┐
               │                                         │ CONTEXT WINDOW     │
               │                                         │                    │
               │                                         │ Instrução do papel │
               │                                         │ Estado resumido    │
               │                                         │ Sprint contract    │
               │                                         │ Dados relevantes   │
               │                                         │ Espaço de resposta │
               │                                         └────────┬───────────┘
               │                                                  │
               │                                                  ▼
               │                           ┌──────────────────────────────────┐
               │                           │ GENERATOR AGENTS                 │
               │                           │                                  │
               │                           │ ┌────────────┐ ┌──────────────┐ │
               │                           │ │ Catálogo   │ │ Recomendação │ │
               │                           │ └─────┬──────┘ └──────┬───────┘ │
               │                           │       │               │         │
               │                           │ ┌─────▼──────┐ ┌──────▼───────┐ │
               │                           │ │ Preço      │ │ Logística    │ │
               │                           │ └─────┬──────┘ └──────┬───────┘ │
               │                           └───────┼───────────────┼─────────┘
               │                                   │ drafts        │
               │                                   ▼               ▼
               │                         generator_draft_v1.json   │
               │                                   │               │
               │                                   └───────┬───────┘
               │                                           │
               │                                           ▼
               │                           ┌──────────────────────────────────┐
               │                           │ EVALUATOR AGENTS                 │
               │                           │                                  │
               │                           │ ┌────────────┐ ┌──────────────┐ │
               │                           │ │ Rubric     │ │ Segurança    │ │
               │                           │ └─────┬──────┘ └──────┬───────┘ │
               │                           │       │               │         │
               │                           │ ┌─────▼──────┐ ┌──────▼───────┐ │
               │                           │ │ Estoque    │ │ Coerência    │ │
               │                           │ └─────┬──────┘ └──────┬───────┘ │
               │                           └───────┼───────────────┼─────────┘
               │                                   │ vereditos     │
               │                                   ▼               ▼
               │                         evaluator_verdict_v1.json │
               │                                           │
               │                                           ▼
               │                           ┌──────────────────────────────────┐
               │                           │ DECISION GATE                    │
               │                           │                                  │
               │                           │ Se aprovado: preparar resposta   │
               │                           │ Se rejeitado: escrever feedback  │
               │                           │ Se risco alto: chamar humano     │
               │                           └───────────┬───────────┬──────────┘
               │                                       │           │
               │ aprovado                              │           │ rejeitado
               │                                       ▼           ▼
               │                          ┌────────────────┐ ┌───────────────┐
               │                          │ OUTPUT FINAL   │ │ FEEDBACK LOOP │
               │                          │ Resposta       │ │ feedback_v1   │
               │                          │ Confirmação    │ │ retry         │
               │                          │ Ação externa   │ │ novo sprint   │
               │                          └───────┬────────┘ └───────┬───────┘
               │                                  │                  │
               │                                  ▼                  │
               │                       ┌────────────────────┐        │
               │                       │ CLIENTE RECEBE     │        │
               │                       │ resposta aprovada  │        │
               │                       └────────────────────┘        │
               │                                                     │
               └─────────────────────────────────────────────────────┘
                         audit_log registra cada transição
```

### Como o diagrama deve ser usado

Use este diagrama como checklist de arquitetura. Se algum componente não existe, você precisa saber por quê. Nem toda feature precisa de tudo, mas toda feature de alto risco precisa justificar qualquer ausência.

### Leitura orientada da Seção 5
O diagrama deve ser lido como uma conversa atravessando fronteiras de responsabilidade.
A primeira caixa, `CLIENTE OU USUÁRIO`, representa a entrada pelo WhatsApp, por um painel interno, por uma API ou por um operador humano.
Em KODA, isso mapeia para o ponto em que uma mensagem, um evento de pedido ou uma intervenção operacional vira entrada de sessão.
O arquivo que costuma refletir essa chegada é `audit_log.jsonl`, porque a primeira coisa verificável não é a resposta, mas o fato de que um evento entrou.
Essa caixa previne uma falha simples: tratar mensagem de cliente, webhook de pagamento e ajuste manual como se fossem o mesmo tipo de estímulo.
Para verificar se está funcionando, pegue uma sessão e confirme que cada entrada relevante aparece no log com origem, horário e identificador.
Depois a entrada sobe para `ORCHESTRATOR / HARNESS`.

Esse é o cérebro operacional, não o cérebro semântico.
Ele decide quando carregar estado, montar contexto, definir contrato, chamar Generator, chamar Evaluator, aprovar, tentar novamente ou escalar.
No material de KODA, essa responsabilidade aparece nos exemplos de harness que controlam `max_iterations`, `context_budget_tokens`, `state_dir`, `requires_evaluator` e `failure_policy`.
O harness previne a falha de deixar o modelo improvisar processo.
Quando ele funciona, a trace mostra transições explícitas: entrada recebida, estado carregado, contrato criado, draft gerado, veredito avaliado e saída liberada.
Se uma resposta final apareceu sem esses passos mínimos, o diagrama foi pulado.
À esquerda do harness está `FILE-BASED COORDINATION`.

No desenho, ela aparece como `state/session_123/` com arquivos nomeados.
Em KODA, esse diretório é a fonte de verdade da sessão, mesmo quando a conversa parece natural para o cliente.
`customer_context.json` concentra fatos duráveis como alergias, objetivo, orçamento, endereço e preferências confirmadas.
`conversation_summary.md` guarda a memória compactada para que o context manager não dependa de todo o histórico bruto.
`sprint_contract.json` declara o que a próxima etapa precisa fazer e quais critérios bloqueiam a saída.
`generator_draft_v1.json` preserva a hipótese do agente gerador antes de virar mensagem.
`evaluator_verdict_v1.json` registra a avaliação independente.

`feedback_v1.json` explica como corrigir quando o draft falha.
`audit_log.jsonl` amarra tudo em ordem temporal.
Essa camada previne perda de memória, disputa entre etapas e investigação sem prova.
A verificação prática é abrir a pasta de uma sessão complexa e reconstruir a resposta final sem perguntar nada ao modelo.
Se a reconstrução exige adivinhação, algum arquivo está fraco ou ausente.
À direita do diretório aparece o `CONTEXT MANAGER`.
Ele não é um resumidor genérico.

Ele escolhe quais fatos entram na janela do modelo para aquela etapa específica.
Em uma recomendação, ele prioriza restrições, objetivo, orçamento, catálogo relevante e histórico de preferências.
Em checkout, ele prioriza carrinho, regras de desconto, endereço, frete, pagamento e confirmações pendentes.
Em fulfillment, ele prioriza pedido, SLA, transportadora, rota e promessas já feitas.
O componente mapeia para a chamada que lê `customer_context.json`, `conversation_summary.md` e o contrato atual antes de montar o prompt.
A falha que ele previne é context rot: a janela fica cheia de conversa agradável e esquece o fato perigoso.
Para verificar, compare uma context window real com o estado persistido e pergunte se alergias, orçamento e compromissos aparecem com prioridade correta.

O bloco `CONTEXT WINDOW` é o pacote que o modelo efetivamente vê.
Ele contém instrução de papel, estado resumido, sprint contract, dados relevantes e espaço de resposta.
Em KODA, essa montagem precisa ser menor que o orçamento definido pelo harness e específica ao papel chamado.
Um Generator de preço não precisa ler toda a explicação nutricional do cliente.
Um Evaluator de segurança precisa ler restrições e draft, mesmo que não precise de toda a conversa de simpatia.
A falha evitada aqui é confundir memória disponível com memória útil.
A verificação é observar se o prompt muda de acordo com a etapa, em vez de carregar sempre o mesmo pacote gigante.

No centro do fluxo estão os `GENERATOR AGENTS`.
O diagrama nomeia Catálogo, Recomendação, Preço e Logística porque KODA não vende apenas texto; ele coordena decisões diferentes.
O Generator de Catálogo encontra candidatos compatíveis com estoque e restrições.
O Generator de Recomendação transforma candidatos em orientação compreensível para o cliente.
O Generator de Preço calcula ou prepara a estrutura de desconto, subtotal, frete e total.
O Generator de Logística propõe entrega, retirada, troca de rota ou comunicação de atraso.
Todos escrevem drafts, não decisões finais.

O arquivo concreto é `generator_draft_v1.json` ou uma variação nomeada por etapa, como `pricing_draft_v1.json` ou `fulfillment_plan_v1.json`.
Essa separação previne a falha de misturar criatividade, cálculo e aprovação na mesma resposta.
Para verificar, leia o draft e confirme que ele contém a hipótese completa, mas ainda não foi enviado ao cliente.
Depois vêm os `EVALUATOR AGENTS`.
O diagrama mostra Rubric, Segurança, Estoque e Coerência.
Em KODA, o Evaluator de Rubric aplica critérios como restrição respeitada, objetivo atendido, clareza e orçamento.
O Evaluator de Segurança bloqueia alergias ignoradas, promessas clínicas indevidas e recomendações incompatíveis.

O Evaluator de Estoque confere disponibilidade, reserva e validade de dados operacionais.
O Evaluator de Coerência procura contradições com histórico, preço, prazo e compromissos anteriores.
O arquivo de saída é `evaluator_verdict_v1.json`, com aprovação, rejeição, critérios e razões.
A falha prevenida é self-evaluation collapse: o mesmo agente que vendeu a ideia não deve ser o juiz final.
Para verificar, procure pelo menos uma sessão rejeitada e veja se o feedback levou a uma tentativa melhor, não apenas a uma aprovação automática.
O `DECISION GATE` é onde o harness transforma veredito em ação.
Se aprovado, ele prepara resposta.

Se rejeitado, ele grava feedback e decide retry.
Se o risco for alto, chama humano.
Em KODA, esse ponto é crítico porque evita que uma resposta parcialmente correta escape por simpatia.
A falha prevenida é saída prematura.
A verificação é observar se existe diferença clara entre `approved`, `rejected`, `retry_requested` e `human_escalation` no log.
`OUTPUT FINAL` é a única parte que o cliente vê, mas não deve ser a única parte que a equipe entende.
Ele pode ser uma resposta, uma confirmação ou uma ação externa.

Em KODA, a saída precisa carregar a decisão aprovada sem expor a mecânica interna.
O cliente recebe linguagem simples: recomendação, pergunta, confirmação, aviso de indisponibilidade ou proposta de alternativa.
A falha prevenida é enviar texto bonito que não corresponde ao estado aprovado.
Para verificar, compare a mensagem final com o draft aprovado e confirme que nenhuma promessa nova entrou depois do Evaluator.
Ao lado da saída aparece o `FEEDBACK LOOP`.
Ele não é uma desculpa para repetir indefinidamente.
Ele é o mecanismo controlado para corrigir o draft quando o Evaluator encontra falha.

Em KODA, isso aparece como `feedback_v1.json`, novo sprint ou retry limitado pelo harness.
A falha prevenida é shotgun debugging dentro da conversa, quando o agente tenta consertar sem saber o que quebrou.
Para verificar, uma trace de retry deve mostrar motivo específico, alteração específica e nova avaliação.
Se o segundo draft não responde ao feedback, o loop está girando sem aprender.
Por fim, a seta que volta ao cliente fecha o ciclo.
O cliente não precisa conhecer `customer_context.json`, `sprint_contract.json` ou `evaluator_verdict_v1.json`.
Mas a experiência dele depende desses arquivos existirem.

A arquitetura é saudável quando a conversa parece leve na superfície e rigorosa por baixo.
O melhor uso do diagrama é escolher uma mensagem real e seguir cada seta.
A mensagem entrou por qual canal?
Qual estado foi carregado?
Qual contexto foi montado?
Qual Generator escreveu o draft?
Qual Evaluator julgou o risco?
Qual decisão liberou a resposta?
Qual artefato provaria tudo isso amanhã?
Quando a equipe consegue responder sem improvisar, o diagrama deixou de ser ilustração e virou ferramenta de operação.

Há uma forma simples de testar o diagrama em revisão de arquitetura.
Pegue uma conversa de descoberta, uma de checkout e uma de fulfillment.
Para cada uma, escreva o nome do arquivo que deveria mudar em cada caixa.
Na entrada, espere evento bruto e identificação de sessão.
No harness, espere decisão de etapa e limites de execução.
No context manager, espere seleção de fatos e orçamento de tokens.
Na coordenação por arquivo, espere estado persistido antes de qualquer resposta crítica.
Nos Generators, espere hipótese estruturada, não mensagem já enviada.
Nos Evaluators, espere critérios com veredito, não opinião genérica.
No decision gate, espere uma decisão de aprovar, rejeitar, tentar de novo ou escalar.
Na saída, espere somente conteúdo que já passou pelo gate.
No feedback loop, espere correção rastreável e limite de repetição.
Se algum componente não deixa evidência, ele pode até existir no código, mas não existe operacionalmente.
Essa distinção evita arquitetura de slide.
KODA precisa de arquitetura que apareça quando algo dá errado.
Quando uma recomendação ignora alergia, o diagrama aponta para context manager, catálogo e Evaluator de segurança.
Quando um desconto sai errado, aponta para Generator de preço, política comercial e decision gate.
Quando uma rota muda, aponta para fulfillment plan, SLA e resposta aprovada.
Quando um cliente reclama, aponta para audit log e evidência de promessa.
Cada caixa deve reduzir uma classe de erro.
Entrada reduz ambiguidade de origem.
Harness reduz improviso de processo.
Estado reduz esquecimento.
Context manager reduz ruído.
Generator reduz mistura de papéis.
Evaluator reduz autoaprovação.
Decision gate reduz saída prematura.
Output reduz vazamento de bastidor.
Feedback loop reduz repetição cega.
Essa leitura também mostra onde simplificar.
Uma pergunta informativa pode usar poucos arquivos e veredito leve.
Uma compra confirmada precisa de mais controle.
Uma exceção logística precisa de fonte operacional.
O diagrama não manda usar tudo sempre.
Ele obriga a justificar o que foi omitido.
Essa justificativa deve ser escrita no contrato ou na decisão de arquitetura.
Assim, quando KODA evoluir, a equipe saberá se está removendo peso desnecessário ou retirando uma proteção essencial.
A melhor verificação é pedir replay para alguém que não participou da implementação.
Se essa pessoa seguir os arquivos e entender a sessão, o desenho está ensinando o sistema a ser legível.
Se ela precisar entrevistar quem escreveu o código, o diagrama ainda não virou prática.

---

## 🧪 Seção 6: Aplicação KODA

### O caso concreto: recomendação com restrição crítica

Cliente: "Quero whey para ganhar massa, mas sou intolerante à lactose e tenho até R$ 180."

Sem os padrões da apresentação, KODA pode acertar por sorte. Com os padrões, KODA acerta por estrutura.

### Estado inicial

```json
{
  "session_id": "koda_session_2026_05_28_001",
  "customer": {
    "id": "wa_5511987654321",
    "name": "João",
    "goal": "ganho_muscular",
    "budget_max_brl": 180,
    "restrictions": [
      "sem_lactose"
    ],
    "preferred_flavor": "chocolate"
  },
  "conversation": {
    "current_intent": "product_discovery",
    "status": "needs_recommendation"
  }
}
```

### Sprint contract

```json
{
  "sprint_id": "recommendation_sprint_001",
  "objective": "gerar recomendacao segura para cliente com restricao alimentar",
  "input_contract": {
    "requires": [
      "customer.goal",
      "customer.budget_max_brl",
      "customer.restrictions"
    ]
  },
  "output_contract": {
    "requires": [
      "recommendations",
      "safety_checks",
      "final_message"
    ]
  },
  "guarantees": [
    "nenhum produto viola restricao alimentar",
    "todos os produtos existem no catalogo",
    "todos os produtos estao dentro do budget",
    "resposta final cita a razao da recomendacao"
  ]
}
```

### Pseudocódigo do harness

```python
def executar_recomendacao_koda(session_id):
    estado = read_json(f"state/{session_id}/customer_context.json")
    contrato = read_json(f"state/{session_id}/sprint_contract.json")

    for tentativa in range(1, 4):
        contexto = montar_contexto(estado, contrato, tentativa)
        draft = chamar_generator(contexto)
        write_json(f"state/{session_id}/generator_draft_v{tentativa}.json", draft)

        veredito = chamar_evaluator(estado, contrato, draft)
        write_json(f"state/{session_id}/evaluator_verdict_v{tentativa}.json", veredito)

        append_jsonl("audit_log.jsonl", {
            "event": "evaluation_completed",
            "attempt": tentativa,
            "verdict": veredito["status"]
        })

        if veredito["status"] == "APPROVED":
            resposta = montar_resposta_final(draft, veredito)
            write_json(f"state/{session_id}/final_response.json", resposta)
            return resposta

        feedback = gerar_feedback_para_generator(veredito)
        write_json(f"state/{session_id}/feedback_v{tentativa}.json", feedback)

    return escalar_para_humano(session_id)
```

### Draft do Generator

```json
{
  "generation_id": "gen_001",
  "recommendations": [
    {
      "sku": "WHEY-VEGANO-CHOC-001",
      "name": "Whey Vegano Chocolate",
      "price_brl": 149.9,
      "reason": "proteina adequada para ganho muscular, sabor chocolate, sem lactose",
      "confidence": 0.86
    },
    {
      "sku": "CREATINA-MONO-300",
      "name": "Creatina Monohidratada 300g",
      "price_brl": 79.9,
      "reason": "complemento seguro para ganho muscular, sem lactose",
      "confidence": 0.78
    }
  ],
  "notes_for_evaluator": [
    "verificar estoque",
    "confirmar marcacao sem_lactose no catalogo",
    "validar preco atual"
  ]
}
```

### Veredito do Evaluator

```json
{
  "verdict_id": "eval_001",
  "status": "APPROVED",
  "rubric_scores": {
    "restriction_safety": 10,
    "catalog_validity": 10,
    "budget_fit": 10,
    "goal_match": 9,
    "message_clarity": 8
  },
  "overall_score": 94,
  "approval_threshold": 85,
  "notes": "Todos os produtos respeitam restricao sem_lactose e cabem no budget informado."
}
```

### Resposta final

```text
João, para o seu objetivo de ganhar massa sem lactose e dentro de R$ 180, minha recomendação principal é o Whey Vegano Chocolate. Ele respeita sua restrição, está dentro do orçamento e combina com sua preferência por chocolate. Também deixei a creatina como complemento seguro se você quiser melhorar o resultado do treino.
```

### O que mudou

| Antes | Depois |
|-------|--------|
| Conversa era a memória principal | Arquivos são a fonte de verdade |
| Agente tentava gerar e avaliar | Generator e Evaluator têm papéis separados |
| Erro era difícil de rastrear | audit_log mostra cada transição |
| Resposta dependia de confiança do modelo | Resposta depende de rubric e veredito |
| Recuperação era improvisada | Retry e escalonamento são políticas do harness |

### Leitura orientada da Seção 6
A melhor forma de aprender esta seção é seguir sessões inteiras, não frases isoladas. KODA parece simples quando responde uma pergunta, mas fica interessante quando precisa preservar contexto, tomar decisões e explicar o próprio caminho. Os casos abaixo mostram como a arquitetura se comporta quando a conversa encontra situações típicas de comércio real. Cada caso deve ser lido como uma trace narrada. A pergunta não é apenas "qual resposta KODA enviou?". A pergunta é "quais arquivos mudaram, quais agentes participaram, qual rubric aprovou e o que ficaria visível em uma auditoria?".

#### Caso de descoberta de produto com alergia alimentar

A cliente Mariana chega pelo WhatsApp depois de ver um anúncio de recuperação pós-treino.
Ela diz que treina à noite, sente muita dor muscular no dia seguinte e quer algo prático para tomar no trabalho.
Na mesma mensagem, quase como detalhe, ela avisa que tem alergia a leite e evita soja por recomendação médica.
O fluxo começa no entry point, que registra a mensagem em `audit_log.jsonl` com origem `whatsapp` e cria ou atualiza a pasta `state/session_mariana_001/`.
O context manager lê a mensagem bruta, separa preferências de restrições e grava a restrição em `customer_context.json` como fato crítico.
O resumo da conversa ainda é curto, mas `conversation_summary.md` já marca que alergia e evitação de soja não podem ser compactadas fora do contexto.
O harness cria um sprint contract específico para descoberta segura.
O contrato não pede simplesmente "recomende um produto".
Ele pede uma opção compatível, uma pergunta de confirmação se o catálogo estiver ambíguo e nenhuma promessa terapêutica.
O Generator de Catálogo consulta candidatos sem leite e sem soja.
O Generator de Recomendação recebe apenas candidatos compatíveis e prepara um draft que compara proteína vegetal de ervilha com creatina, explicando uso geral sem diagnóstico.
O Evaluator de Segurança verifica alergênicos, linguagem médica e consistência com orçamento se ele já tiver sido informado.
O Evaluator de Coerência procura contradições: não pode citar whey comum, não pode sugerir produto com traços de leite sem aviso, não pode ignorar a preferência de praticidade.
Um estado intermediário poderia aparecer assim:

```json
{
  "session_id": "session_mariana_001",
  "stage": "product_discovery",
  "customer_context": {
    "goal": "recuperacao_pos_treino",
    "hard_restrictions": ["alergia_leite", "evita_soja"],
    "usage_context": "tomar_no_trabalho"
  },
  "sprint_contract": {
    "must_exclude": ["derivados_de_leite", "soja"],
    "must_include": ["pergunta_de_confirmacao", "justificativa_simples"],
    "blocked_claims": ["promessa_clinica", "tratamento_de_dor"]
  }
}

```

A resposta aprovada não precisa mostrar toda essa estrutura.
Ela pode dizer que, pela restrição, KODA vai priorizar opções vegetais sem leite e sem soja, confirmar tolerância a ervilha e perguntar se Mariana prefere cápsula, pó ou sachê.
O artefato que prova o funcionamento é `evaluator_verdict_v1.json` aprovando critérios de segurança antes da mensagem final.
Se a trace mostrar que o Generator recomendou primeiro e a restrição só apareceu na resposta final, o fluxo está invertido.
O correto é a restrição controlar a geração, não apenas enfeitar a explicação.
Nesse caso, a rubric de aprovação exige quatro pontos.
Restrições críticas devem estar refletidas no filtro de catálogo.
A linguagem deve evitar promessa médica.
A recomendação precisa explicar por que opções comuns foram excluídas.
A próxima pergunta deve reduzir incerteza sem empurrar compra prematura.
Quando esses critérios aparecem no veredito, a equipe pode confiar que a resposta não foi sorte.
Ela foi consequência do desenho.

#### Caso de checkout com descontos conflitantes

Rafael já escolheu creatina, multivitamínico e uma proteína vegetal. Ele diz que tem cupom de primeira compra e também quer usar a promoção de vinte por cento vista no Instagram. O problema não é persuadir Rafael a finalizar. O problema é não prometer uma combinação comercial que a empresa não sustenta. O entry point registra a intenção de checkout e o harness muda o estágio da sessão para `checkout_pricing`. O context manager carrega carrinho, endereço, histórico de cupons e regras comerciais relevantes. O arquivo `cart_state.json` preserva SKUs, quantidades e preços base. O arquivo `promotion_context.json` registra cupom informado, campanha mencionada e elegibilidade conhecida. O sprint contract diz que nenhum total final pode ser enviado sem listar desconto aplicado, descontos recusados e motivo.
O Generator de Preço cria `pricing_draft_v1.json`.
Nesse primeiro draft, ele pode descobrir que a promoção de Instagram não acumula com cupom de primeira compra.
Se ele errar e acumular ambos, o Evaluator de Política Comercial rejeita.
O feedback não diz apenas "corrija o preço".
Ele aponta qual regra foi violada e pede nova tentativa escolhendo a melhor opção para o cliente.
A segunda tentativa calcula o total com a promoção mais vantajosa e prepara uma explicação transparente.
Um trecho de transição de estado poderia ser:

```json
{
  "stage": "checkout_pricing",
  "pricing_attempt": 2,
  "cart_total_brl": 286.70,
  "discounts_requested": ["primeira_compra", "instagram_20"],
  "discount_applied": {
    "code": "instagram_20",
    "amount_brl": 57.34,
    "reason": "maior_beneficio_e_nao_acumulavel"
  },
  "discounts_declined": [
    {
      "code": "primeira_compra",
      "reason": "regra_nao_acumula_com_campanha_percentual"
    }
  ],
  "approved_total_brl": 229.36
}

```

O Evaluator de Coerência compara a mensagem final com o JSON de preço aprovado.
Ele bloqueia qualquer frase que sugira que Rafael recebeu os dois descontos.
O Evaluator de Clareza verifica se a explicação não soa punitiva.
A resposta final pode dizer que KODA aplicou automaticamente a melhor promoção disponível e deixou claro por que o outro cupom ficou reservado para uma compra futura, se essa for a política.
A trace esperada mostra `pricing_draft_v1.json` rejeitado, `feedback_v1.json` com regra comercial, `pricing_draft_v2.json` aprovado e `audit_log.jsonl` registrando a decisão.
Esse caso ensina que checkout exige harness diferente de recomendação.
Na recomendação, o risco central é compatibilidade e segurança.
No checkout, o risco central é uma promessa econômica incorreta.
A rubric precisa refletir cálculo, política, transparência, idempotência e ausência de nova promessa depois da aprovação.
Se a equipe só revisar o texto final, talvez ache a resposta excelente.
Se revisar a trace, saberá se o total tem fundamento.

#### Caso de processamento de pedido com ruptura de estoque no meio da conversa

Luana está comprando duas unidades de creatina porque quer aproveitar frete grátis. No início da conversa, o catálogo indicava estoque disponível. Enquanto ela confirma endereço e forma de pagamento, outro pedido consome a última unidade do mesmo lote. A arquitetura frágil seguiria com a memória antiga de estoque e deixaria a ruptura aparecer no backoffice. A arquitetura correta trata estoque como estado mutável e exige revalidação antes da confirmação final. O entry point recebe a confirmação de Luana e o harness abre sprint de `order_processing`.
O context manager carrega `customer_context.json`, `cart_state.json`, `conversation_summary.md` e o último evento de estoque.
Antes de chamar o Generator de resposta, o harness chama a verificação operacional e grava `stock_check_v2.json`.
Esse arquivo mostra que só existe uma unidade disponível.
O Generator de Pedido não deve inventar solução.
Ele deve propor alternativas: comprar uma unidade agora, trocar por SKU equivalente, aguardar reposição ou remover item para recalcular frete.
O Evaluator de Estoque bloqueia qualquer resposta que mantenha duas unidades como confirmadas.
O Evaluator de Experiência verifica se a mensagem reconhece o inconveniente e oferece escolhas reais.
A transição de estado ficaria assim:

```json
{
  "stage": "order_processing",
  "inventory_event": {
    "sku": "creatina_mono_300g",
    "requested_quantity": 2,
    "available_quantity": 1,
    "event_source": "stock_check_before_confirmation"
  },
  "cart_revision": {
    "status": "requires_customer_choice",
    "options": ["confirmar_1_unidade", "substituir_sku", "aguardar_reposicao"]
  },
  "customer_message_allowed": false
}

```

O campo `customer_message_allowed` muda para `true` apenas depois que o draft passa pela avaliação.
Isso impede a resposta apressada que confirma pedido incompleto.
A trace deve mostrar a ruptura como evento separado da conversa.
Ela também deve mostrar que o sprint contract mudou: a meta deixou de ser "confirmar pedido" e virou "explicar ruptura e coletar escolha".
Esse detalhe importa porque muitos agentes longos falham ao insistir no plano antigo.
O plano antigo era finalizar.
O estado novo exige renegociar.
A rubric aplicável inclui estoque atualizado, não confirmação indevida, alternativas concretas, recalculo se houver mudança e tom de responsabilidade.
Se Luana escolher uma unidade, o próximo sprint recalcula frete e total.
Se ela escolher substituição, o Generator de Catálogo volta ao fluxo com restrições de equivalência.
Se ela aguardar reposição, fulfillment não deve receber promessa de despacho imediato.
O estado persistente impede que uma escolha parcial se perca entre etapas.
Sem arquivo, o agente teria que lembrar de uma conversa emocional e operacionalmente complexa.
Com arquivo, cada etapa herda a decisão correta.

#### Caso de fulfillment com mudança de rota

Pedro comprou um combo para receber antes de uma prova de ciclismo no sábado. O pedido já está pago e separado. Na sexta de manhã, a transportadora informa bloqueio em uma rota por evento local. O risco agora não é escolher produto, nem calcular desconto. O risco é prometer uma entrega que logística não consegue cumprir. O webhook operacional entra como evento no mesmo sistema de sessão. O harness cria sprint de `fulfillment_exception` e marca que há promessa anterior de entrega antes da prova. O context manager carrega `order_state.json`, `fulfillment_plan_v1.json`, `customer_context.json` e `conversation_summary.md`.
Ele também carrega o evento novo em `route_update.json`.
O Generator de Logística propõe três caminhos: trocar transportadora com custo adicional autorizado, oferecer retirada em ponto parceiro ou avisar novo prazo com compensação comercial.
O Evaluator de SLA verifica se cada alternativa cabe no horário.
O Evaluator de Política Comercial verifica se a compensação sugerida está autorizada.
O Evaluator de Comunicação verifica se a resposta assume responsabilidade sem culpar terceiros de forma vaga.
Um estado aprovado poderia ser:

```json
{
  "stage": "fulfillment_exception",
  "order_id": "pedido_78421",
  "route_update": {
    "carrier": "rota_sul_express",
    "original_eta": "sexta_18h",
    "risk": "bloqueio_evento_local",
    "new_eta_if_unchanged": "segunda_12h"
  },
  "approved_options": [
    {
      "type": "carrier_switch",
      "eta": "sabado_09h",
      "customer_cost_brl": 0,
      "requires_confirmation": true
    },
    {
      "type": "pickup_point",
      "eta": "sexta_17h30",
      "requires_confirmation": true
    }
  ]
}

```

A resposta final deve oferecer escolhas, não anunciar unilateralmente uma solução.
Ela pode dizer que KODA identificou risco na rota original e já separou duas alternativas para manter a entrega antes da prova.
O cliente escolhe trocar transportadora ou retirar no ponto parceiro.
Depois da escolha, o harness abre novo sprint para executar a alternativa e registrar confirmação.
A trace mostra que KODA não improvisou prazo.
Ela mostra evento de rota, opções geradas, critérios avaliados, decisão aguardando confirmação e resposta final.
O arquivo que prova funcionamento é `fulfillment_plan_v2.json` acompanhado de `evaluator_verdict_v1.json`.
A rubric deste caso inclui SLA, fonte operacional, autorização de custo, clareza, confirmação do cliente e atualização de promessa.
Se qualquer promessa nova aparece apenas no texto final, a arquitetura falhou.
Fulfillment é o lugar onde a distância entre linguagem e operação fica perigosa.
O harness precisa manter essa distância visível.

#### Caso de investigação de reclamação pós-compra

Camila volta três dias depois irritada.
Ela diz que KODA prometeu entrega na terça, mas o pedido chegou na quinta e o sabor veio diferente do combinado.
Esse é o tipo de situação em que uma conversa longa precisa ser auditável.
A arquitetura errada pediria desculpas de forma genérica e talvez oferecesse cupom sem entender a causa.
A arquitetura correta abre sprint de investigação.
O entry point registra a reclamação e o harness muda o estágio para `post_purchase_investigation`.
O context manager não deve carregar apenas a mensagem atual.
Ele precisa reunir `conversation_summary.md`, `order_state.json`, `fulfillment_plan_v1.json`, `approved_response_log.json`, eventos de expedição e qualquer alteração de SKU.
O Generator de Investigação monta uma hipótese factual: qual sabor foi pedido, qual sabor foi separado, qual promessa de data foi aprovada e qual evento atrasou a entrega.
Ele não escreve pedido de desculpa final ainda.
Ele escreve `complaint_investigation_v1.json`.
O Evaluator de Evidência verifica se cada afirmação tem fonte.
O Evaluator de Responsabilidade bloqueia linguagem defensiva quando a trace mostra erro interno.
O Evaluator de Política de Resolução verifica se troca, reembolso parcial ou cupom estão dentro das regras.
Um trecho de investigação poderia ser:

```json
{
  "stage": "post_purchase_investigation",
  "complaint": ["atraso_entrega", "sabor_incorreto"],
  "evidence": {
    "promised_eta": {
      "value": "terca_20h",
      "source": "approved_response_log.json#msg_018"
    },
    "actual_delivery": {
      "value": "quinta_14h10",
      "source": "carrier_event_2026_05_30.json"
    },
    "flavor_ordered": {
      "value": "chocolate",
      "source": "cart_state.json"
    },
    "flavor_shipped": {
      "value": "baunilha",
      "source": "packing_event_442.json"
    }
  },
  "resolution_options": ["troca_sem_custo", "reembolso_frete", "cupom_reparacao"]
}

```

A resposta aprovada deve reconhecer fatos específicos.
Ela não deve dizer "sentimos muito pelo ocorrido" e parar ali.
Ela deve dizer que a promessa registrada era terça, que a entrega ocorreu quinta e que houve divergência entre sabor pedido e separado.
Depois deve oferecer resolução concreta dentro da política.
A trace esperada mostra leitura de evidências, investigação gerada, avaliação de fonte, opção de resolução aprovada e mensagem enviada.
Esse caso fecha o ciclo de long-running agents.
A utilidade dos arquivos criados em recomendação, checkout e fulfillment aparece quando há reclamação.
Se a equipe não registrou promessa, não consegue saber se Camila tem razão.
Se registrou apenas texto livre, perde tempo interpretando.
Se registrou estado estruturado, a resolução pode ser rápida e justa.
A rubric inclui completude de evidência, ausência de invenção, reconhecimento proporcional, política de reparação e preservação de confiança.
O Generator ajuda a organizar a história.
O Evaluator impede que a história vire narrativa conveniente.
O harness decide se a resposta pode sair ou se precisa de humano, especialmente quando há custo ou risco jurídico.

#### Caso de retorno para recompra com memória compactada

Um último caso mostra por que a persistência não serve apenas para incidentes.
Bruno comprou proteína vegetal há dois meses, gostou do sabor, mas achou o pacote grande demais para levar ao trabalho.
Agora ele volta pedindo "algo parecido, só que mais prático".
A conversa antiga não cabe inteira na janela e nem deveria caber.
O context manager lê `customer_context.json` e `conversation_summary.md` para recuperar fatos duráveis: prefere chocolate, evita lactose, valorizou praticidade e reclamou do tamanho da embalagem.
O Generator de Recomendação não precisa reabrir todo o histórico.
Ele propõe sachês ou embalagem menor, mantendo restrições e explicando que a sugestão vem da preferência anterior.
O Evaluator de Coerência verifica se a memória usada é sustentada por arquivo e não por suposição.
A transição pode ser curta:

```json
{
  "stage": "returning_customer_recommendation",
  "memory_loaded": [
    "restricao_sem_lactose",
    "preferencia_chocolate",
    "reclamacao_embalagem_grande",
    "uso_no_trabalho"
  ],
  "recommendation_strategy": "similaridade_com_melhor_praticidade",
  "requires_new_budget_question": true
}

```

A resposta final reconhece continuidade sem assustar o cliente.
Ela pode dizer: "Da última vez você preferiu chocolate e comentou que queria algo mais fácil de levar; posso te mostrar duas opções sem lactose em porções menores".
A trace prova que KODA lembrou por arquivo, não por magia.
A rubric pede uso correto de memória, pergunta de orçamento atual, estoque vigente e cuidado para não fingir intimidade excessiva.
Esse caso diferencia memória útil de acúmulo de histórico.
Long-running agents bons não carregam tudo.
Eles carregam o que ainda muda a decisão.
Ao comparar os seis casos, aparece um padrão comum.
Toda sessão começa com entrada registrada.
Todo risco relevante vira estado explícito.
Toda etapa crítica ganha sprint contract.
Todo draft importante é avaliado por papel independente.
Toda decisão aprovada deixa rastro.
Mas os detalhes mudam conforme o domínio.
Alergia exige segurança e filtro de catálogo.
Desconto exige política comercial e cálculo.
Ruptura de estoque exige revalidação e escolha do cliente.
Rota alterada exige SLA e fonte operacional.
Reclamação exige evidência e reparação.
Recompra exige memória compactada e atualidade.
Essa é a lição prática da seção.
A arquitetura não existe para multiplicar arquivos.
Ela existe para que KODA consiga explicar, corrigir e sustentar decisões quando a conversa deixa de ser simples.
---

## 🔗 Seção 7: Conexões com o Currículo

A apresentação da Anthropic funciona como mapa de origem para o currículo. Cada nível pega uma parte da tese e transforma em prática.

### Nível 1: Fundamentos

- [Por Que Agentes Perdem o Foco?](../01-nivel-1-fundamentals/01-why-agents-lose-plot.md) explica os problemas que a apresentação assume como ponto de partida.
- [Token Budgeting](../01-nivel-1-fundamentals/02-token-budgeting.md) aprofunda o custo de usar context window como memória.
- [Basic Harness Patterns](../01-nivel-1-fundamentals/03-basic-harness-patterns.md) mostra a primeira camada de controle ao redor do modelo.
- [Aplicações KODA Nível 1](../01-nivel-1-fundamentals/koda-applications/nivel-1-koda.md) traduz as falhas de contexto para conversas reais de venda.

### Nível 2: Padrões práticos

- [Generator/Evaluator Pattern](../02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md) é a aplicação mais direta da separação entre criação e avaliação.
- [Sprint Contracts](../02-nivel-2-practical-patterns/02-sprint-contracts.md) formaliza promessas entre etapas.
- [Rubric Design](../02-nivel-2-practical-patterns/03-rubric-design.md) transforma qualidade em critérios verificáveis.
- [Trace Reading](../02-nivel-2-practical-patterns/04-trace-reading.md) ensina a ler os rastros que o harness registra.
- [Aplicações KODA Nível 2](../02-nivel-2-practical-patterns/koda-applications/nivel-2-koda.md) mostra como esses padrões mudam o comportamento do produto.

### Nível 3: Arquitetura avançada

- [Multi-Agent Systems](../03-nivel-3-advanced-architecture/01-multi-agent-systems.md) expande a coordenação entre papéis especializados.
- [State Persistence](../03-nivel-3-advanced-architecture/02-state-persistence.md) aprofunda a fonte de verdade fora da context window.
- [File-Based Coordination](../03-nivel-3-advanced-architecture/03-file-based-coordination.md) implementa a coordenação por artefatos que a apresentação defende.
- [Server-Side Compaction](../03-nivel-3-advanced-architecture/04-server-side-compaction.md) mostra como compactar sem perder fatos críticos.
- [Harness Evolution](../03-nivel-3-advanced-architecture/05-harness-evolution.md) mostra como o harness cresce conforme risco e complexidade aumentam.

### Nível 4: KODA específico

- [KODA Architecture](../04-nivel-4-koda-specific/01-koda-architecture.md) aplica os blocos da apresentação ao produto real.
- [Customer Journey Flows](../04-nivel-4-koda-specific/02-customer-journey-flows.md) mostra onde estado precisa atravessar etapas da conversa.
- [Feature Design Patterns](../04-nivel-4-koda-specific/03-feature-design-patterns.md) ajuda a escolher padrões por feature.
- [Evaluation Rubrics KODA](../04-nivel-4-koda-specific/04-evaluation-rubrics-koda.md) adapta rubric design para riscos específicos de venda de suplementos.
- [Harness Improvements](../04-nivel-4-koda-specific/05-harness-improvements.md) mostra como evoluir o sistema sem quebrar confiança.

### Mapa conceitual

```text
Apresentação Anthropic
      │
      ├── context window limitada
      │       └── Nível 1: token budgeting e context management
      │
      ├── estado externo
      │       └── Nível 3: state persistence
      │
      ├── coordenação por arquivos
      │       └── Nível 3: file-based coordination
      │
      ├── papéis separados
      │       └── Nível 2: Generator/Evaluator
      │
      ├── controle por harness
      │       └── Níveis 1, 3 e 4: harness patterns e evolution
      │
      └── avaliação e auditoria
              └── Nível 2: rubric design e trace reading
```

### Leitura orientada da Seção 7

Use esta seção como um roteiro de estudo, não como uma lista para marcar mecanicamente.

A apresentação da Anthropic é a origem conceitual; os módulos do currículo são as ferramentas que transformam essa origem em decisões de produto.

Se você está lendo com pressa, escolha o caminho pelo problema que precisa resolver agora.

Se você está formando base, siga a progressão dos níveis.

Se você está revisando uma feature de KODA, comece pelo ponto onde a feature pode falhar.

A regra prática é simples: leia primeiro o módulo que reduz o risco mais próximo do cliente.

**Se você quer entender por que KODA perde confiança em conversas longas, leia `../01-nivel-1-fundamentals/01-why-agents-lose-plot.md` primeiro.**

Esse módulo dá a história que torna o resto do currículo óbvio.

Ele mostra como amnésia de contexto, colapso de planejamento e autoavaliação fraca aparecem como uma experiência ruim para o cliente.

Leia com uma conversa real em mente e marque onde KODA poderia esquecer alergia, orçamento ou promessa de entrega.

**Se você quer reduzir custo e ruído antes de mexer na arquitetura, leia `../01-nivel-1-fundamentals/02-token-budgeting.md`.**

Esse material importa quando a equipe acha que resolverá tudo aumentando a context window.

Ele ensina a decidir o que entra no prompt ativo e o que deve virar estado externo.

Use esse módulo antes de discutir modelos maiores, porque muitas falhas são seleção ruim de contexto, não falta de capacidade.

**Se você quer construir o primeiro controle ao redor do modelo, leia `../01-nivel-1-fundamentals/03-basic-harness-patterns.md`.**

Esse é o ponto onde o agente deixa de ser uma chamada isolada e passa a trabalhar dentro de um fluxo.

Ele ajuda a responder quem decide retry, quem limita iterações e quem registra o que aconteceu.

Leia antes de implementar qualquer feature que possa precisar continuar depois de erro parcial.

**Se você quer impedir que recomendação ruim chegue ao cliente, leia `../02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md`.**

Esse módulo é a ponte mais direta entre a apresentação e KODA.

Ele separa quem propõe de quem julga, o que é essencial quando há alergia, preço ou regra comercial.

Leia com um exemplo concreto: um draft de recomendação e um veredito que precisa poder reprovar sem pedir desculpas ao Generator.

**Se você quer tornar entregas entre etapas menos ambíguas, leia `../02-nivel-2-practical-patterns/02-sprint-contracts.md`.**

Sprint contracts importam quando uma feature tem mais de um passo e cada passo depende do anterior.

Eles evitam que logística receba pedido incompleto, que preço calcule sobre SKU errado ou que resposta final ignore veredito.

Leia antes de dividir trabalho entre agentes ou módulos, porque contrato fraco multiplica confusão.

**Se você quer transformar qualidade em critério discutível, leia `../02-nivel-2-practical-patterns/03-rubric-design.md`.**

Rubrics são o antídoto contra avaliações vagas como "parece bom".

Esse módulo mostra como traduzir segurança, utilidade, clareza e conformidade em critérios que podem ser aplicados repetidamente.

Leia quando a equipe discorda sobre o que significa uma resposta aprovada.

**Se você quer diagnosticar incidentes sem depender de lembrança humana, leia `../02-nivel-2-practical-patterns/04-trace-reading.md`.**

Trace reading é onde logs, drafts, vereditos e contratos viram narrativa.

Ele importa depois de qualquer falha que o cliente percebeu como contradição, cobrança errada ou promessa quebrada.

Leia com um incidente real aberto e tente reconstruir a decisão sem consultar quem estava online no momento.

**Se você quer separar domínios de trabalho sem criar confusão, leia `../03-nivel-3-advanced-architecture/01-multi-agent-systems.md`.**

Multi-agent só ajuda quando cada agente tem fronteira real.

Esse módulo ensina a diferenciar especialização útil de duplicação cara.

Leia antes de criar agentes para catálogo, preço, logística e suporte, porque nomes diferentes não garantem responsabilidades diferentes.

**Se você quer parar de usar conversa como banco de dados, leia `../03-nivel-3-advanced-architecture/02-state-persistence.md`.**

State persistence é a base para retomada, auditoria e compactação segura.

Ele mostra que fatos críticos precisam sobreviver a reinício, resumo e troca de modelo.

Leia quando a equipe identificar qualquer dado de cliente que hoje vive apenas no histórico do WhatsApp.

**Se você quer coordenar agentes por evidência, leia `../03-nivel-3-advanced-architecture/03-file-based-coordination.md`.**

Esse módulo torna prática a tese de que arquivos podem ser memória compartilhada.

Ele importa quando um agente precisa continuar o trabalho de outro sem receber uma explicação verbal ou prompt gigante.

Leia antes de desenhar diretórios `state/`, versionamento de drafts e nomes de artefatos.

**Se você quer compactar conversas sem apagar decisões importantes, leia `../03-nivel-3-advanced-architecture/04-server-side-compaction.md`.**

Compaction mal feita transforma histórico longo em resumo enganoso.

Esse módulo mostra como preservar fatos críticos antes de reduzir texto.

Leia quando KODA começar a usar resumos automáticos ou quando custo de contexto estiver pressionando a operação.

**Se você quer evoluir o sistema sem reescrever tudo de uma vez, leia `../03-nivel-3-advanced-architecture/05-harness-evolution.md`.**

Harness evolution ajuda a planejar maturidade incremental.

Ele mostra quando adicionar gates, filas, retries, políticas e escalonamento.

Leia quando uma feature simples começa a acumular exceções e o harness atual já não explica o fluxo.

**Se você quer aplicar os padrões ao produto real, leia `../04-nivel-4-koda-specific/01-koda-architecture.md`.**

Esse módulo junta o vocabulário do currículo com as fronteiras reais de KODA.

Ele importa para decidir onde ficam estado, agentes, avaliações, integrações e logs no produto.

Leia antes de propor mudança estrutural, porque ele impede soluções genéricas demais.

**Se você quer entender onde a conversa muda de fase, leia `../04-nivel-4-koda-specific/02-customer-journey-flows.md`.**

Customer journey flows ajudam a localizar transições perigosas: descoberta, comparação, carrinho, checkout, entrega e suporte.

Cada transição muda o tipo de estado que precisa ser preservado.

Leia quando uma falha parecer "pequena", mas tiver ocorrido justamente na passagem entre duas fases.

**Se você quer escolher padrão por feature, leia `../04-nivel-4-koda-specific/03-feature-design-patterns.md`.**

Esse módulo conecta problemas de produto a escolhas de arquitetura.

Ele ajuda a decidir se uma feature precisa de single agent, Generator/Evaluator, multi-agent, eventos ou humano.

Leia junto com a tabela da Seção 4 para não confundir sofisticação com adequação.

**Se você quer avaliar riscos específicos de suplemento e venda, leia `../04-nivel-4-koda-specific/04-evaluation-rubrics-koda.md`.**

Rubrics genéricas não bastam quando há alergia, composição nutricional, estoque, preço e promessa de entrega.

Esse módulo adapta avaliação para o domínio do KODA.

Leia antes de aprovar respostas que envolvem saúde, dinheiro ou expectativa operacional do cliente.

**Se você quer priorizar melhorias do harness, leia `../04-nivel-4-koda-specific/05-harness-improvements.md`.**

Esse é o material para transformar diagnóstico em roadmap.

Ele ajuda a escolher a próxima melhoria sem tentar resolver todo o sistema em uma sprint.

Leia depois de trace reading, porque melhoria boa nasce de falha observada, não de arquitetura imaginada.

Uma sequência segura para iniciantes é: problema, token budget, harness básico, Generator/Evaluator, rubrics e trace reading.

Uma sequência segura para arquitetos é: state persistence, file-based coordination, multi-agent systems, server-side compaction e harness evolution.

Uma sequência segura para quem está mexendo em KODA agora é: arquitetura KODA, customer journey, feature design, rubrics KODA e melhorias de harness.

Não pule direto para Nível 4 se a equipe ainda não consegue explicar Nível 1.

Não fique presa no Nível 1 se já existe incidente real exigindo trace reading.

O currículo é uma caixa de ferramentas.

A apresentação da Anthropic explica por que as ferramentas existem.

A leitura orientada serve para escolher a ferramenta certa antes que a próxima conversa longa exponha a mesma falha outra vez.


---

## ✅ Seção 8: O Que Você Aprendeu

Esta seção resume os aprendizados centrais. Ela é longa de propósito: serve como revisão para quem vai usar a apresentação como referência antes de desenhar uma feature nova.

### Resumo em 12 ideias

1. Long-running agents são sistemas, não apenas prompts longos.
2. A context window ajuda, mas não substitui state persistence.
3. Fatos críticos precisam viver fora da conversa.
4. File-based coordination dá memória, contrato e auditoria.
5. Generator/Evaluator separa criação de julgamento.
6. Multi-agent patterns funcionam quando papéis têm fronteiras claras.
7. O harness é quem controla iteração, limite, retry e escalonamento.
8. Rubrics transformam qualidade em critérios explícitos.
9. Trace reading transforma falha em diagnóstico.
10. Human-in-the-loop continua necessário em riscos altos.
11. KODA precisa dessas ideias porque conversa longa é parte do produto.
12. A arquitetura certa reduz erros sem depender de esperança no modelo.

### Key Takeaways com aplicação

### Takeaway 1: State persistence para fatos críticos
**Ideia:** Memória confiável não é aquilo que o modelo viu; é aquilo que o sistema consegue reler, auditar e usar depois de reinício.
**Prática:** Extraia fatos que mudam segurança, dinheiro ou promessa e grave em estado externo antes de continuar a conversa.
**Aplicação em KODA:** quando uma cliente informa "tenho alergia a amendoim" durante a escolha de whey, KODA deve persistir a restrição antes de consultar produtos ou montar recomendação.
**Evidência esperada:** `state/koda_session_*/customer_context.json` contém `allergies: ["amendoim"]` e `audit_log.jsonl` registra `customer_restriction_confirmed` com timestamp.
**Pergunta de revisão:** se a conversa for compactada logo depois dessa mensagem, qual arquivo garante que a alergia ainda bloqueia produtos com risco?

Para revisar esse takeaway, não olhe primeiro para a resposta final.

Olhe para o estado que a resposta final leu.

Se a informação crítica só aparece no histórico textual, KODA ainda está confiando demais na context window.

A resposta pode parecer correta hoje e falhar amanhã quando o histórico mudar de forma.

O teste mínimo é reiniciar a sessão e verificar se a recomendação continua respeitando a restrição.


Um bom sinal de maturidade é conseguir apagar as mensagens intermediárias e ainda reconstruir a decisão pelos arquivos.

Se isso não for possível, o sistema ainda usa conversa como muleta operacional.

No caso de alergia, essa muleta é perigosa porque a falha não aparece como bug técnico; aparece como recomendação insegura.

Por isso a revisão deve começar pelo estado persistido e só depois olhar a resposta ao cliente.

### Takeaway 2: File-based coordination entre papéis
**Ideia:** Agentes coordenam melhor quando deixam artefatos pequenos, nomeados e versionados, em vez de depender de explicação escondida no prompt.
**Prática:** Faça cada etapa escrever um arquivo que a próxima etapa possa ler sem ambiguidade.
**Aplicação em KODA:** quando o agente de catálogo seleciona três SKUs e o agente de preço calcula o total, o preço deve ler `catalog_candidates_v1.json`, não uma frase solta da conversa.
**Evidência esperada:** `state/koda_session_*/catalog_candidates_v1.json`, `pricing_quote_v1.json` e `audit_log.jsonl` com `artifact_written` para cada transição.
**Pergunta de revisão:** se o total apresentado estiver errado, qual arquivo mostra se o erro veio do catálogo ou do cálculo de preço?

Esse padrão é simples, mas muda a cultura de debug.

Em vez de perguntar "o que o agente estava pensando?", a equipe pergunta "qual artefato ele produziu?".

Essa troca é essencial para long-running agents.

Pensamento não versionado desaparece.

Arquivo versionado pode ser comparado, testado e reaproveitado.


A coordenação por arquivos também ajuda quando a equipe precisa comparar versões.

Se `pricing_quote_v1.json` e `pricing_quote_v2.json` divergem, a diferença precisa estar explicada por evento ou entrada nova.

Essa disciplina reduz discussões subjetivas sobre "o que KODA quis dizer".

O arquivo mostra o que KODA realmente entregou para a próxima etapa.

### Takeaway 3: Generator/Evaluator para recomendações arriscadas
**Ideia:** Criar uma boa resposta e encontrar falhas nessa resposta são trabalhos diferentes.
**Prática:** Deixe o Generator propor e dê ao Evaluator permissão explícita para reprovar por segurança, orçamento, estoque ou clareza.
**Aplicação em KODA:** quando o cliente pede suplemento para ganho muscular mas informa intolerância à lactose, o Generator sugere opções e o Evaluator veta qualquer SKU com lactose ou marcação incompleta.
**Evidência esperada:** `generator_draft_v1.json` lista os produtos candidatos e `evaluator_verdict_v1.json` traz `restriction_safety: 10` ou rejeição com motivo específico.
**Pergunta de revisão:** o Evaluator consegue reprovar uma recomendação que parece comercialmente boa, mas viola a restrição alimentar?

O ganho não está apenas em ter dois nomes no fluxo.

O ganho está em criar tensão produtiva.

O Generator tenta ajudar o cliente.

O Evaluator tenta proteger o cliente e o negócio.

Quando os dois papéis são claros, a resposta final deixa de depender de autoconfiança do modelo.


O Evaluator precisa ter acesso aos mesmos fatos críticos que o Generator usou, mas com uma missão diferente.

Ele não está tentando vender; está tentando encontrar o erro antes do cliente.

Em KODA, isso muda a conversa interna da equipe: a melhor resposta não é a mais persuasiva, é a mais segura entre as persuasivas.

Quando o veredito reprova, o feedback precisa ser específico o suficiente para gerar uma segunda tentativa melhor.

### Takeaway 4: Harness como condutor do fluxo
**Ideia:** O modelo não deve decidir sozinho quando tentar de novo, quando parar, quando escalar ou qual artefato gravar.
**Prática:** Centralize limites, retries, políticas de escalonamento e escrita de logs no harness.
**Aplicação em KODA:** quando o Evaluator reprova duas vezes uma recomendação por estoque desatualizado, o harness deve interromper novas tentativas e acionar operador ou fluxo de catálogo.
**Evidência esperada:** `harness_run.json` contém `max_attempts: 2`, `stop_reason: evaluator_rejected_stock` e `audit_log.jsonl` registra `human_escalation_requested`.
**Pergunta de revisão:** quem impede o Generator de continuar tentando indefinidamente depois de reprovações repetidas?

Sem harness, autonomia vira improviso.

Com harness, autonomia vira processo.

Essa diferença aparece principalmente quando algo dá errado.

O happy path pode funcionar mesmo com arquitetura fraca.

O harness mostra seu valor quando há rejeição, timeout, conflito ou falta de dado.


O harness também é onde a experiência do cliente fica consistente.

Sem ele, duas conversas parecidas podem ter políticas diferentes de retry, timeout e escalonamento.

Com ele, KODA mantém o mesmo comportamento operacional mesmo quando o conteúdo da conversa muda.

Isso é importante para suporte, porque a equipe consegue explicar não só a resposta, mas o processo que levou até ela.

### Takeaway 5: Rubric gate antes da resposta final
**Ideia:** Qualidade precisa passar por critérios visíveis antes de virar mensagem para o cliente.
**Prática:** Transforme requisitos de segurança, preço, estoque, clareza e política comercial em gate de aprovação.
**Aplicação em KODA:** quando dois descontos conflitam no checkout, a resposta final só deve sair se a rubric confirmar regra de acúmulo, total final e explicação ao cliente.
**Evidência esperada:** `rubric_discount_checkout_v1.json` define critérios e `evaluator_verdict_v1.json` registra `discount_policy_compliance: approved`.
**Pergunta de revisão:** qual critério impediria KODA de prometer frete grátis junto com cupom que não acumula?

Rubric boa não é lista genérica de boas intenções.

Ela precisa pegar erros reais do domínio.

No KODA, isso significa tratar saúde, dinheiro e promessa operacional como critérios separados.

Uma resposta clara, mas comercialmente inválida, deve reprovar.

Uma resposta correta, mas ambígua para o cliente, também deve reprovar.


Um gate bem desenhado deve ser chato de propósito.

Ele impede que entusiasmo comercial passe por cima de regra operacional.

Se a equipe sentir vontade de contornar a rubric para mandar uma resposta mais rápida, esse é justamente o momento de revisar o risco.

Velocidade que pula critério crítico costuma reaparecer como retrabalho, reembolso ou perda de confiança.

### Takeaway 6: Trace reading para incidentes
**Ideia:** Debug de agente longo é reconstrução de história, não caça a uma linha isolada.
**Prática:** Leia entrada, estado, contrato, draft, veredito, feedback e resposta final em ordem temporal.
**Aplicação em KODA:** quando um cliente reclama que KODA prometeu entrega no mesmo dia mas o pedido chegou depois, trace reading deve mostrar onde o prazo antigo foi mantido.
**Evidência esperada:** `audit_log.jsonl` contém eventos `address_changed`, `shipping_quote_received`, `final_response_sent` e o arquivo `shipping_quote_v2.json` mostra o prazo usado.
**Pergunta de revisão:** a equipe consegue explicar a promessa de entrega sem reler toda a conversa do WhatsApp?

Trace reading também treina melhoria de produto.

Ele mostra se a falha veio de contexto, estado, política, avaliação ou mensagem final.

Sem essa separação, a equipe tende a culpar "o modelo".

Com trace, a falha ganha endereço.

E falha com endereço pode virar correção concreta.


O trace precisa ser legível para alguém que não participou da conversa.

Essa pessoa deve conseguir responder: qual foi a entrada, qual estado estava vigente, qual decisão foi tomada e por que foi aprovada.

Se a explicação depende de perguntar ao operador que estava online, o trace ainda não cumpre seu papel.

O objetivo é transformar incidente em aprendizado reproduzível.

### Takeaway 7: Context management com seleção deliberada
**Ideia:** Contexto bom não é contexto máximo; é contexto suficiente para a decisão atual.
**Prática:** Monte prompts com fatos críticos, contrato do sprint e trechos relevantes, deixando ruído histórico fora da chamada.
**Aplicação em KODA:** quando o catálogo é atualizado durante uma conversa, KODA deve trazer apenas os SKUs ainda candidatos e a mudança relevante, não despejar o catálogo inteiro no prompt.
**Evidência esperada:** `context_snapshot_v3.md` mostra os campos carregados e `metrics/context_tokens` registra redução após remover histórico irrelevante.
**Pergunta de revisão:** qual fato foi incluído porque muda a decisão, e qual texto foi deixado fora porque só aumentaria ruído?

Esse takeaway evita uma reação comum: resolver esquecimento com prompt maior.

Prompt maior pode adiar a falha, mas também aumenta custo e confusão.

O objetivo é construir uma mesa de trabalho limpa.

A mesa precisa ter os documentos certos.

Não precisa ter todo o arquivo morto da empresa.


Context management também protege o tom da conversa.

Quando o prompt carrega histórico demais, KODA pode responder a uma pergunta simples como se estivesse encerrando um caso complexo.

Quando carrega pouco demais, perde restrições e promessas.

A habilidade está em montar a visão mínima que preserva decisão correta e resposta natural.

### Takeaway 8: Multi-agent apenas com fronteiras reais
**Ideia:** Vários agentes ajudam quando cada um possui responsabilidade distinta e artefato próprio.
**Prática:** Separe papéis por domínio, dado e critério de sucesso; não crie agentes diferentes para fazer a mesma revisão genérica.
**Aplicação em KODA:** quando um pedido envolve disponibilidade regional, preço promocional e restrição alimentar, agentes de logística, preço e segurança podem trabalhar sobre o mesmo `current_order.json` com outputs separados.
**Evidência esperada:** `logistics_check_v1.json`, `pricing_decision_v1.json` e `safety_verdict_v1.json` existem e são referenciados por `final_evaluator_verdict.json`.
**Pergunta de revisão:** cada agente produz uma evidência que outro agente não produziria melhor?

Multi-agent sem coordenação aumenta ruído.

Multi-agent com artefatos claros reduz ambiguidade.

A diferença está na fronteira.

Se dois agentes podem trocar de nome sem mudar o resultado, a arquitetura está teatral.

Se cada agente tem dado, saída e falha própria, a divisão faz sentido.


A fronteira entre agentes deve aparecer em nomes de arquivos, não apenas no diagrama.

Se logística escreve `logistics_check_v1.json`, preço escreve `pricing_decision_v1.json` e segurança escreve `safety_verdict_v1.json`, a equipe sabe onde procurar.

Se todos escrevem no mesmo resumo genérico, o ganho de especialização desaparece.

A coordenação precisa sobreviver ao primeiro incidente real.

### Takeaway 9: Human-in-the-loop como proteção explícita
**Ideia:** Autonomia responsável inclui saber quando parar e pedir confirmação humana.
**Prática:** Defina critérios de escalonamento para risco alimentar, cobrança suspeita, exceção operacional e dado ausente crítico.
**Aplicação em KODA:** quando o catálogo não informa se um produto tem traços de amendoim e a cliente declarou alergia severa, KODA deve escalar em vez de inferir segurança.
**Evidência esperada:** `human_review_request_v1.json` contém motivo `missing_allergen_trace_data` e `audit_log.jsonl` registra `response_blocked_for_safety`.
**Pergunta de revisão:** qual condição impede KODA de responder automaticamente mesmo quando o cliente pede rapidez?

Human-in-the-loop não é fracasso de automação.

É parte do desenho de confiança.

O cliente prefere uma pausa honesta a uma recomendação arriscada.

A empresa também prefere um caso escalado a um incidente de saúde ou cobrança.

O importante é que o escalonamento seja regra, não improviso.


Escalonar para humano também precisa ser confortável para o cliente.

KODA deve explicar que está protegendo uma decisão sensível, não simplesmente travando.

A mensagem pode ser curta, mas precisa preservar confiança: "vou confirmar esse dado antes de indicar".

Esse tom mostra que a arquitetura não é só interna; ela aparece como cuidado percebido.

### Takeaway 10 - Event-driven para esperas externas
**Ideia:** Quando o fluxo depende de callbacks, filas ou sistemas externos, a conversa não deve fingir que tudo é síncrono.
**Prática:** Modele eventos persistidos para mudanças de endereço, pagamento, estoque, transporte e notificações.
**Aplicação em KODA:** quando um cliente muda o endereço depois de montar o carrinho, KODA emite `address_changed`, aguarda nova cotação e só depois libera confirmação de pagamento.
**Evidência esperada:** `events/order_events.jsonl` contém `address_changed`, `shipping_quote_requested`, `shipping_quote_received` e `checkout_unblocked`.
**Pergunta de revisão:** qual evento prova que o checkout ficou bloqueado enquanto o frete novo não chegava?

Event-driven não é necessário para todo fluxo.

Ele aparece quando existe espera real fora do modelo.

Transportadora, gateway de pagamento e ERP não obedecem ao ritmo da conversa.

Persistir eventos permite retomar o trabalho quando a resposta externa chega.

Também evita prometer ao cliente algo que ainda está pendente.


Eventos são especialmente úteis quando o cliente continua falando enquanto o sistema espera.

KODA pode responder dúvidas gerais, mas não deve avançar checkout bloqueado por cotação pendente.

Essa separação entre conversa ativa e workflow pendente evita misturar simpatia com promessa operacional.

O audit_log precisa mostrar claramente quando o fluxo ficou bloqueado e quando foi liberado.

### Takeaway 11 - Sprint contracts para continuidade
**Ideia:** Cada etapa longa precisa declarar entrada, saída e garantia antes de executar.
**Prática:** Escreva contratos pequenos que digam quais dados são obrigatórios e qual artefato será produzido.
**Aplicação em KODA:** quando o cliente escolhe produto, cupom e endereço, o sprint de checkout deve exigir SKU confirmado, regra de desconto aplicada e cotação de frete válida antes de gerar link de pagamento.
**Evidência esperada:** `sprint_contract_checkout_v1.json` lista `required_inputs` e `final_response.json` referencia o contrato aprovado.
**Pergunta de revisão:** qual campo obrigatório bloquearia o checkout se o endereço ainda estivesse incompleto?

Sprint contract reduz surpresa entre módulos.

Ele também facilita retry.

Se uma tentativa falha, a equipe sabe qual garantia não foi cumprida.

Sem contrato, cada etapa inventa seu próprio significado de "pronto".

Em agente longo, "pronto" precisa ser verificável.


O contrato deve ser pequeno o bastante para ser lido e rígido o bastante para bloquear erro.

Se ele vira documento longo demais, ninguém respeita; se vira frase vaga, não protege nada.

Em KODA, um bom contrato de checkout diz exatamente quais campos impedem avançar.

Essa clareza torna falhas menos dramáticas, porque o sistema sabe parar antes de prometer.

### Takeaway 12 - Escolha arquitetural por risco
**Ideia:** A melhor estratégia é a menor composição que cobre a falha dominante do cenário.
**Prática:** Antes de implementar, nomeie a falha mais cara, o artefato que provaria a decisão e o padrão que produz esse artefato.
**Aplicação em KODA:** quando um cliente pede troca de produto após pagamento aprovado, a falha dominante é inconsistência entre pedido, estoque e cobrança, não apenas resposta textual ruim.
**Evidência esperada:** `order_change_decision_v1.json` registra produto antigo, produto novo, status de pagamento, ajuste de valor e aprovação em `evaluator_verdict_v1.json`.
**Pergunta de revisão:** a estratégia escolhida permite explicar a troca sem depender da memória de quem atendeu o caso?

Esse takeaway fecha a apresentação.

Long-running agents não ficam confiáveis por excesso de padrão.

Eles ficam confiáveis quando cada padrão resolve uma falha concreta.

Em KODA, a arquitetura deve sempre voltar ao cliente: segurança, preço, prazo, continuidade e clareza.

Se o padrão não melhora uma dessas dimensões, talvez ele ainda não seja necessário.



A escolha por risco também evita copiar arquitetura de uma feature para outra sem pensar.

Uma pergunta simples de catálogo não merece o mesmo fluxo de uma troca pós-pagamento.

Por outro lado, uma decisão de saúde não deve ser tratada como pergunta simples só porque o cliente escreveu em uma frase curta.

O tamanho da mensagem não mede o risco; o impacto da falha mede.

---

## 🚀 Seção 9: Próximos Passos

Depois de ler esta referência, escolha o próximo material de acordo com sua necessidade.

### Se você quer entender o problema

1. Leia [Por Que Agentes Perdem o Foco?](../01-nivel-1-fundamentals/01-why-agents-lose-plot.md).
2. Leia [Token Budgeting](../01-nivel-1-fundamentals/02-token-budgeting.md).
3. Releia o prólogo deste módulo e escreva um exemplo real do seu produto.

### Se você quer implementar o primeiro padrão

1. Leia [Generator/Evaluator Pattern](../02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md).
2. Escolha uma feature KODA de baixo risco.
3. Crie `generator_draft.json` e `evaluator_verdict.json` para essa feature.
4. Defina uma rubric simples com 5 critérios.

### Se você quer desenhar arquitetura

1. Leia [State Persistence](../03-nivel-3-advanced-architecture/02-state-persistence.md).
2. Leia [File-Based Coordination](../03-nivel-3-advanced-architecture/03-file-based-coordination.md).
3. Desenhe onde cada artefato fica no diretório `state/`.
4. Defina quais arquivos são imutáveis e quais são versionados.

### Se você quer aplicar no KODA

1. Leia [KODA Architecture](../04-nivel-4-koda-specific/01-koda-architecture.md).
2. Leia [Evaluation Rubrics KODA](../04-nivel-4-koda-specific/04-evaluation-rubrics-koda.md).
3. Pegue uma conversa real e marque onde cada decisão deveria ter sido persistida.
4. Escreva um trace manual antes de automatizar.

### Sequência recomendada de estudo

```text
Esta referência
   ↓
Nível 1: por que agentes falham
   ↓
Nível 2: padrões práticos
   ↓
Nível 3: arquitetura avançada
   ↓
Nível 4: KODA em produção
```

---

## ❓ Perguntas Frequentes

### P: Se a context window é muito grande, ainda preciso de state persistence?
**R:** Sim. Uma janela grande permite ler mais, mas não garante auditoria, replay, retomada amanhã ou custo previsível. Estado externo resolve outro problema.

### P: File-based coordination não é simples demais?
**R:** É simples no melhor sentido. Arquivos são fáceis de ler, versionar, testar e auditar. Para muitos long-running agents, essa simplicidade é vantagem.

### P: Quando Generator/Evaluator vale o custo extra?
**R:** Vale quando erro custa confiança, dinheiro, segurança ou retrabalho. Recomendação de produto com restrição alimentar é um caso claro.

### P: Multi-agent sempre melhora o sistema?
**R:** Não. Multi-agent melhora quando os papéis têm fronteiras reais. Se todos os agentes fazem a mesma coisa, você só adicionou custo e ruído.

### P: O harness é parte do agente?
**R:** Sim, no sentido de produto. O modelo gera texto e decisões, mas o harness controla fluxo, estado, retry, logs, limites e integração.

### P: Human-in-the-loop contradiz autonomia?
**R:** Não. Autonomia boa sabe quando parar. Escalar casos críticos é parte de uma arquitetura responsável.

### P: Como sei se minha rubric está boa?
**R:** Ela é boa quando pega erros reais, explica rejeições e produz decisões consistentes entre rodadas parecidas.

### P: Trace reading é só olhar logs?
**R:** Não. É reconstruir a história da decisão a partir de artefatos, entradas, saídas, contratos e vereditos.

---

## 🚀 Checkpoint: Você Consegue Aplicar?

Antes de fechar este módulo, marque os itens que você consegue explicar sem consultar as seções acima.

- [ ] Consigo explicar por que context window não é memória permanente.
- [ ] Consigo diferenciar contexto temporário de estado persistido.
- [ ] Consigo desenhar um fluxo Generator/Evaluator simples.
- [ ] Consigo explicar por que file-based coordination ajuda no debug.
- [ ] Consigo escolher entre single agent, Generator/Evaluator e multi-agent.
- [ ] Consigo apontar onde o harness entra na arquitetura.
- [ ] Consigo escrever um exemplo de `customer_context.json` para KODA.
- [ ] Consigo escrever um exemplo de `evaluator_verdict.json`.
- [ ] Consigo ler a tabela de estratégias e escolher uma opção para uma feature real.
- [ ] Consigo conectar a apresentação aos módulos de Nível 1.
- [ ] Consigo conectar a apresentação aos módulos de Nível 2.
- [ ] Consigo conectar a apresentação aos módulos de Nível 3.
- [ ] Consigo conectar a apresentação aos módulos de Nível 4.
- [ ] Consigo explicar quando human-in-the-loop é obrigatório.
- [ ] Consigo explicar por que trace reading reduz tempo de debug.

### Autoavaliação prática

Responda em voz alta ou em um documento curto:

1. Qual é a menor feature do KODA que merece Generator/Evaluator?
2. Qual fato crítico de cliente hoje está vivendo apenas em conversa?
3. Qual arquivo você criaria primeiro para tornar esse fato persistente?
4. Qual rubric impediria uma recomendação ruim de chegar ao cliente?
5. Qual evento precisa aparecer no audit_log para permitir replay?

Se você travou em mais de duas respostas, volte para as Seções 2, 3 e 6.

---

## 📚 Referências & Próximas Leituras

### Dentro deste currículo

- [Nível 1: Por Que Agentes Perdem o Foco?](../01-nivel-1-fundamentals/01-why-agents-lose-plot.md)
- [Nível 1: Token Budgeting](../01-nivel-1-fundamentals/02-token-budgeting.md)
- [Nível 1: Basic Harness Patterns](../01-nivel-1-fundamentals/03-basic-harness-patterns.md)
- [Nível 2: Generator/Evaluator Pattern](../02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md)
- [Nível 2: Sprint Contracts](../02-nivel-2-practical-patterns/02-sprint-contracts.md)
- [Nível 2: Rubric Design](../02-nivel-2-practical-patterns/03-rubric-design.md)
- [Nível 2: Trace Reading](../02-nivel-2-practical-patterns/04-trace-reading.md)
- [Nível 3: Multi-Agent Systems](../03-nivel-3-advanced-architecture/01-multi-agent-systems.md)
- [Nível 3: State Persistence](../03-nivel-3-advanced-architecture/02-state-persistence.md)
- [Nível 3: File-Based Coordination](../03-nivel-3-advanced-architecture/03-file-based-coordination.md)
- [Nível 3: Server-Side Compaction](../03-nivel-3-advanced-architecture/04-server-side-compaction.md)
- [Nível 3: Harness Evolution](../03-nivel-3-advanced-architecture/05-harness-evolution.md)
- [Nível 4: KODA Architecture](../04-nivel-4-koda-specific/01-koda-architecture.md)
- [Nível 4: Customer Journey Flows](../04-nivel-4-koda-specific/02-customer-journey-flows.md)
- [Nível 4: Feature Design Patterns](../04-nivel-4-koda-specific/03-feature-design-patterns.md)
- [Nível 4: Evaluation Rubrics KODA](../04-nivel-4-koda-specific/04-evaluation-rubrics-koda.md)
- [Nível 4: Harness Improvements](../04-nivel-4-koda-specific/05-harness-improvements.md)

### Fora deste currículo

- Anthropic: apresentação sobre construir agents que rodam por horas.
- Anthropic documentation sobre context windows, tool use e agent patterns.
- Materiais sobre sistemas distribuídos, event sourcing e auditoria de workflows.
- Papers e artigos sobre multi-agent systems e avaliação de LLMs.

---

## 💭 Reflexão Final

A apresentação da Anthropic é valiosa porque tira long-running agents do campo da intuição. Ela mostra que o problema não é pedir ao modelo para ser mais cuidadoso. O problema é desenhar um sistema onde cuidado não dependa de sorte.

Um agente que trabalha por horas precisa lembrar sem confiar apenas na context window. Precisa planejar sem misturar tudo em uma chamada. Precisa gerar sem ser juiz do próprio trabalho. Precisa deixar rastros para que humanos consigam entender o que aconteceu. Precisa de um harness que transforme intenção em processo.

KODA é o exemplo vivo dessa tese. Cada conversa longa com cliente é uma pequena prova de arquitetura. Se KODA lembra restrições, respeita orçamento, explica recomendações, registra decisões e aprende com traces, o cliente sente confiança. Se KODA depende apenas de uma conversa enorme e de um modelo confiante, a falha é questão de tempo.

A boa notícia é que os padrões não são misteriosos. Eles são concretos: arquivos JSON, rubrics, contracts, logs, Generator, Evaluator, context manager, orchestrator e feedback loops. O desafio é disciplina. Escrever estado quando parece mais rápido manter tudo no prompt. Criar rubric quando parece mais fácil confiar na resposta. Ler trace quando parece mais confortável culpar o modelo.

Esse currículo existe para treinar essa disciplina.

Quando você construir a próxima feature do KODA, não pergunte apenas: "o agente consegue responder?"

Pergunte: "o sistema consegue continuar correto depois de duas horas, três retries, uma compactação de histórico e uma falha parcial?"

Essa é a pergunta que separa uma demonstração bonita de um long-running agent confiável.

---

## 📋 Metadata

| Campo | Valor |
|-------|-------|
| **Arquivo** | anthropic-presentation-summary.md |
| **Diretório** | curriculum/10-references/ |
| **Nível** | Referência transversal |
| **Tempo** | 150 minutos |
| **Status** | ✅ Completo |
| **Fonte resumida** | Apresentação Anthropic sobre building long-running agents |
| **Conecta com** | Níveis 1, 2, 3 e 4 |
| **Conceitos centrais** | context window, state persistence, file-based coordination, Generator/Evaluator, harness, multi-agent orchestration, rubric design, trace reading |
| **Próximo** | ../01-nivel-1-fundamentals/01-why-agents-lose-plot.md |
| **Atualizado** | Maio 2026 |

*Escrito para servir como referência de origem conceitual do currículo KODA Long-Running Agents.*
