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

**Observação arquitetural 1:** O padrão `Generator/Evaluator` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 1: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 1: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 2:** O padrão `file-based coordination` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 2: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 2: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 3:** O padrão `multi-agent patterns` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 3: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 3: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 4:** O padrão `harness design` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 4: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 4: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 5:** O padrão `state persistence` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 5: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 5: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 6:** O padrão `Generator/Evaluator` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 6: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 6: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 7:** O padrão `file-based coordination` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 7: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 7: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 8:** O padrão `multi-agent patterns` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 8: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 8: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 9:** O padrão `harness design` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 9: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 9: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 10:** O padrão `state persistence` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 10: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 10: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 11:** O padrão `Generator/Evaluator` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 11: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 11: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 12:** O padrão `file-based coordination` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 12: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 12: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 13:** O padrão `multi-agent patterns` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 13: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 13: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 14:** O padrão `harness design` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 14: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 14: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 15:** O padrão `state persistence` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 15: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 15: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 16:** O padrão `Generator/Evaluator` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 16: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 16: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 17:** O padrão `file-based coordination` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 17: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 17: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 18:** O padrão `multi-agent patterns` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 18: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 18: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 19:** O padrão `harness design` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 19: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 19: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 20:** O padrão `state persistence` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 20: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 20: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 21:** O padrão `Generator/Evaluator` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 21: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 21: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 22:** O padrão `file-based coordination` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 22: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 22: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 23:** O padrão `multi-agent patterns` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 23: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 23: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 24:** O padrão `harness design` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 24: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 24: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 25:** O padrão `state persistence` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 25: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 25: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 26:** O padrão `Generator/Evaluator` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 26: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 26: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 27:** O padrão `file-based coordination` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 27: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 27: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 28:** O padrão `multi-agent patterns` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 28: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 28: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 29:** O padrão `harness design` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 29: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 29: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 30:** O padrão `state persistence` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 30: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 30: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 31:** O padrão `Generator/Evaluator` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 31: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 31: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 32:** O padrão `file-based coordination` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 32: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 32: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 33:** O padrão `multi-agent patterns` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 33: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 33: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 34:** O padrão `harness design` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 34: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 34: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 35:** O padrão `state persistence` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 35: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 35: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 36:** O padrão `Generator/Evaluator` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 36: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 36: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 37:** O padrão `file-based coordination` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 37: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 37: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 38:** O padrão `multi-agent patterns` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 38: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 38: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 39:** O padrão `harness design` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 39: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 39: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 40:** O padrão `state persistence` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 40: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 40: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 41:** O padrão `Generator/Evaluator` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 41: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 41: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 42:** O padrão `file-based coordination` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 42: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 42: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 43:** O padrão `multi-agent patterns` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 43: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 43: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 44:** O padrão `harness design` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 44: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 44: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 45:** O padrão `state persistence` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 45: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 45: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 46:** O padrão `Generator/Evaluator` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 46: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 46: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 47:** O padrão `file-based coordination` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 47: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 47: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 48:** O padrão `multi-agent patterns` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 48: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 48: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 49:** O padrão `harness design` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 49: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 49: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 50:** O padrão `state persistence` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 50: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 50: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 51:** O padrão `Generator/Evaluator` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 51: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 51: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 52:** O padrão `file-based coordination` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 52: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 52: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 53:** O padrão `multi-agent patterns` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 53: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 53: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 54:** O padrão `harness design` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 54: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 54: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 55:** O padrão `state persistence` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 55: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 55: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 56:** O padrão `Generator/Evaluator` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 56: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 56: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 57:** O padrão `file-based coordination` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 57: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 57: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 58:** O padrão `multi-agent patterns` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 58: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 58: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 59:** O padrão `harness design` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 59: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 59: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 60:** O padrão `state persistence` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 60: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 60: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 61:** O padrão `Generator/Evaluator` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 61: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 61: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 62:** O padrão `file-based coordination` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 62: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 62: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 63:** O padrão `multi-agent patterns` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 63: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 63: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 64:** O padrão `harness design` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 64: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 64: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 65:** O padrão `state persistence` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 65: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 65: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 66:** O padrão `Generator/Evaluator` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 66: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 66: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 67:** O padrão `file-based coordination` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 67: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 67: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 68:** O padrão `multi-agent patterns` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 68: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 68: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 69:** O padrão `harness design` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 69: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 69: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 70:** O padrão `state persistence` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 70: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 70: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 71:** O padrão `Generator/Evaluator` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 71: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 71: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 72:** O padrão `file-based coordination` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 72: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 72: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 73:** O padrão `multi-agent patterns` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 73: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 73: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 74:** O padrão `harness design` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 74: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 74: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 75:** O padrão `state persistence` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 75: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 75: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 76:** O padrão `Generator/Evaluator` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 76: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 76: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 77:** O padrão `file-based coordination` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 77: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 77: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 78:** O padrão `multi-agent patterns` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 78: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 78: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 79:** O padrão `harness design` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 79: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 79: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 80:** O padrão `state persistence` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 80: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 80: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 81:** O padrão `Generator/Evaluator` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 81: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 81: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 82:** O padrão `file-based coordination` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 82: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 82: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 83:** O padrão `multi-agent patterns` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 83: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 83: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 84:** O padrão `harness design` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 84: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 84: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 85:** O padrão `state persistence` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 85: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 85: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 86:** O padrão `Generator/Evaluator` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 86: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 86: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 87:** O padrão `file-based coordination` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 87: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 87: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 88:** O padrão `multi-agent patterns` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 88: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 88: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 89:** O padrão `harness design` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 89: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 89: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 90:** O padrão `state persistence` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 90: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 90: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 91:** O padrão `Generator/Evaluator` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 91: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 91: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 92:** O padrão `file-based coordination` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 92: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 92: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 93:** O padrão `multi-agent patterns` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 93: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 93: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 94:** O padrão `harness design` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 94: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 94: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 95:** O padrão `state persistence` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 95: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 95: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 96:** O padrão `Generator/Evaluator` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 96: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 96: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 97:** O padrão `file-based coordination` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 97: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 97: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 98:** O padrão `multi-agent patterns` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 98: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 98: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 99:** O padrão `harness design` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 99: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 99: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

**Observação arquitetural 100:** O padrão `state persistence` reduz uma falha específica de agentes longos. Ele transforma comportamento implícito em artefato verificável.
Como revisar em KODA 100: procure a fronteira do papel. Quem gera? Quem avalia? Quem registra? Quem decide retry? Se a mesma chamada faz tudo, o risco volta.
Sinal de maturidade 100: depois de uma falha, a equipe consegue apontar um arquivo, um veredito, um contrato ou uma linha de audit_log que explica o ocorrido.

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

**Elemento 1:** `Client/User entry point` precisa ter uma responsabilidade clara. Quando dois elementos fazem a mesma coisa, o debug fica confuso.
Checagem KODA 1: identifique qual arquivo muda quando `Client/User entry point` executa. Se nenhum arquivo muda, pergunte como a equipe fará replay depois.

**Elemento 2:** `Context manager` precisa ter uma responsabilidade clara. Quando dois elementos fazem a mesma coisa, o debug fica confuso.
Checagem KODA 2: identifique qual arquivo muda quando `Context manager` executa. Se nenhum arquivo muda, pergunte como a equipe fará replay depois.

**Elemento 3:** `state persistence layer` precisa ter uma responsabilidade clara. Quando dois elementos fazem a mesma coisa, o debug fica confuso.
Checagem KODA 3: identifique qual arquivo muda quando `state persistence layer` executa. Se nenhum arquivo muda, pergunte como a equipe fará replay depois.

**Elemento 4:** `Generator agents` precisa ter uma responsabilidade clara. Quando dois elementos fazem a mesma coisa, o debug fica confuso.
Checagem KODA 4: identifique qual arquivo muda quando `Generator agents` executa. Se nenhum arquivo muda, pergunte como a equipe fará replay depois.

**Elemento 5:** `Evaluator agents` precisa ter uma responsabilidade clara. Quando dois elementos fazem a mesma coisa, o debug fica confuso.
Checagem KODA 5: identifique qual arquivo muda quando `Evaluator agents` executa. Se nenhum arquivo muda, pergunte como a equipe fará replay depois.

**Elemento 6:** `file-based coordination` precisa ter uma responsabilidade clara. Quando dois elementos fazem a mesma coisa, o debug fica confuso.
Checagem KODA 6: identifique qual arquivo muda quando `file-based coordination` executa. Se nenhum arquivo muda, pergunte como a equipe fará replay depois.

**Elemento 7:** `Orchestrator / harness` precisa ter uma responsabilidade clara. Quando dois elementos fazem a mesma coisa, o debug fica confuso.
Checagem KODA 7: identifique qual arquivo muda quando `Orchestrator / harness` executa. Se nenhum arquivo muda, pergunte como a equipe fará replay depois.

**Elemento 8:** `Output/response` precisa ter uma responsabilidade clara. Quando dois elementos fazem a mesma coisa, o debug fica confuso.
Checagem KODA 8: identifique qual arquivo muda quando `Output/response` executa. Se nenhum arquivo muda, pergunte como a equipe fará replay depois.

**Elemento 9:** `feedback loops` precisa ter uma responsabilidade clara. Quando dois elementos fazem a mesma coisa, o debug fica confuso.
Checagem KODA 9: identifique qual arquivo muda quando `feedback loops` executa. Se nenhum arquivo muda, pergunte como a equipe fará replay depois.

**Elemento 10:** `Client/User entry point` precisa ter uma responsabilidade clara. Quando dois elementos fazem a mesma coisa, o debug fica confuso.
Checagem KODA 10: identifique qual arquivo muda quando `Client/User entry point` executa. Se nenhum arquivo muda, pergunte como a equipe fará replay depois.

**Elemento 11:** `Context manager` precisa ter uma responsabilidade clara. Quando dois elementos fazem a mesma coisa, o debug fica confuso.
Checagem KODA 11: identifique qual arquivo muda quando `Context manager` executa. Se nenhum arquivo muda, pergunte como a equipe fará replay depois.

**Elemento 12:** `state persistence layer` precisa ter uma responsabilidade clara. Quando dois elementos fazem a mesma coisa, o debug fica confuso.
Checagem KODA 12: identifique qual arquivo muda quando `state persistence layer` executa. Se nenhum arquivo muda, pergunte como a equipe fará replay depois.

**Elemento 13:** `Generator agents` precisa ter uma responsabilidade clara. Quando dois elementos fazem a mesma coisa, o debug fica confuso.
Checagem KODA 13: identifique qual arquivo muda quando `Generator agents` executa. Se nenhum arquivo muda, pergunte como a equipe fará replay depois.

**Elemento 14:** `Evaluator agents` precisa ter uma responsabilidade clara. Quando dois elementos fazem a mesma coisa, o debug fica confuso.
Checagem KODA 14: identifique qual arquivo muda quando `Evaluator agents` executa. Se nenhum arquivo muda, pergunte como a equipe fará replay depois.

**Elemento 15:** `file-based coordination` precisa ter uma responsabilidade clara. Quando dois elementos fazem a mesma coisa, o debug fica confuso.
Checagem KODA 15: identifique qual arquivo muda quando `file-based coordination` executa. Se nenhum arquivo muda, pergunte como a equipe fará replay depois.

**Elemento 16:** `Orchestrator / harness` precisa ter uma responsabilidade clara. Quando dois elementos fazem a mesma coisa, o debug fica confuso.
Checagem KODA 16: identifique qual arquivo muda quando `Orchestrator / harness` executa. Se nenhum arquivo muda, pergunte como a equipe fará replay depois.

**Elemento 17:** `Output/response` precisa ter uma responsabilidade clara. Quando dois elementos fazem a mesma coisa, o debug fica confuso.
Checagem KODA 17: identifique qual arquivo muda quando `Output/response` executa. Se nenhum arquivo muda, pergunte como a equipe fará replay depois.

**Elemento 18:** `feedback loops` precisa ter uma responsabilidade clara. Quando dois elementos fazem a mesma coisa, o debug fica confuso.
Checagem KODA 18: identifique qual arquivo muda quando `feedback loops` executa. Se nenhum arquivo muda, pergunte como a equipe fará replay depois.

**Elemento 19:** `Client/User entry point` precisa ter uma responsabilidade clara. Quando dois elementos fazem a mesma coisa, o debug fica confuso.
Checagem KODA 19: identifique qual arquivo muda quando `Client/User entry point` executa. Se nenhum arquivo muda, pergunte como a equipe fará replay depois.

**Elemento 20:** `Context manager` precisa ter uma responsabilidade clara. Quando dois elementos fazem a mesma coisa, o debug fica confuso.
Checagem KODA 20: identifique qual arquivo muda quando `Context manager` executa. Se nenhum arquivo muda, pergunte como a equipe fará replay depois.

**Elemento 21:** `state persistence layer` precisa ter uma responsabilidade clara. Quando dois elementos fazem a mesma coisa, o debug fica confuso.
Checagem KODA 21: identifique qual arquivo muda quando `state persistence layer` executa. Se nenhum arquivo muda, pergunte como a equipe fará replay depois.

**Elemento 22:** `Generator agents` precisa ter uma responsabilidade clara. Quando dois elementos fazem a mesma coisa, o debug fica confuso.
Checagem KODA 22: identifique qual arquivo muda quando `Generator agents` executa. Se nenhum arquivo muda, pergunte como a equipe fará replay depois.

**Elemento 23:** `Evaluator agents` precisa ter uma responsabilidade clara. Quando dois elementos fazem a mesma coisa, o debug fica confuso.
Checagem KODA 23: identifique qual arquivo muda quando `Evaluator agents` executa. Se nenhum arquivo muda, pergunte como a equipe fará replay depois.

**Elemento 24:** `file-based coordination` precisa ter uma responsabilidade clara. Quando dois elementos fazem a mesma coisa, o debug fica confuso.
Checagem KODA 24: identifique qual arquivo muda quando `file-based coordination` executa. Se nenhum arquivo muda, pergunte como a equipe fará replay depois.

**Elemento 25:** `Orchestrator / harness` precisa ter uma responsabilidade clara. Quando dois elementos fazem a mesma coisa, o debug fica confuso.
Checagem KODA 25: identifique qual arquivo muda quando `Orchestrator / harness` executa. Se nenhum arquivo muda, pergunte como a equipe fará replay depois.

**Elemento 26:** `Output/response` precisa ter uma responsabilidade clara. Quando dois elementos fazem a mesma coisa, o debug fica confuso.
Checagem KODA 26: identifique qual arquivo muda quando `Output/response` executa. Se nenhum arquivo muda, pergunte como a equipe fará replay depois.

**Elemento 27:** `feedback loops` precisa ter uma responsabilidade clara. Quando dois elementos fazem a mesma coisa, o debug fica confuso.
Checagem KODA 27: identifique qual arquivo muda quando `feedback loops` executa. Se nenhum arquivo muda, pergunte como a equipe fará replay depois.

**Elemento 28:** `Client/User entry point` precisa ter uma responsabilidade clara. Quando dois elementos fazem a mesma coisa, o debug fica confuso.
Checagem KODA 28: identifique qual arquivo muda quando `Client/User entry point` executa. Se nenhum arquivo muda, pergunte como a equipe fará replay depois.

**Elemento 29:** `Context manager` precisa ter uma responsabilidade clara. Quando dois elementos fazem a mesma coisa, o debug fica confuso.
Checagem KODA 29: identifique qual arquivo muda quando `Context manager` executa. Se nenhum arquivo muda, pergunte como a equipe fará replay depois.

**Elemento 30:** `state persistence layer` precisa ter uma responsabilidade clara. Quando dois elementos fazem a mesma coisa, o debug fica confuso.
Checagem KODA 30: identifique qual arquivo muda quando `state persistence layer` executa. Se nenhum arquivo muda, pergunte como a equipe fará replay depois.

**Elemento 31:** `Generator agents` precisa ter uma responsabilidade clara. Quando dois elementos fazem a mesma coisa, o debug fica confuso.
Checagem KODA 31: identifique qual arquivo muda quando `Generator agents` executa. Se nenhum arquivo muda, pergunte como a equipe fará replay depois.

**Elemento 32:** `Evaluator agents` precisa ter uma responsabilidade clara. Quando dois elementos fazem a mesma coisa, o debug fica confuso.
Checagem KODA 32: identifique qual arquivo muda quando `Evaluator agents` executa. Se nenhum arquivo muda, pergunte como a equipe fará replay depois.

**Elemento 33:** `file-based coordination` precisa ter uma responsabilidade clara. Quando dois elementos fazem a mesma coisa, o debug fica confuso.
Checagem KODA 33: identifique qual arquivo muda quando `file-based coordination` executa. Se nenhum arquivo muda, pergunte como a equipe fará replay depois.

**Elemento 34:** `Orchestrator / harness` precisa ter uma responsabilidade clara. Quando dois elementos fazem a mesma coisa, o debug fica confuso.
Checagem KODA 34: identifique qual arquivo muda quando `Orchestrator / harness` executa. Se nenhum arquivo muda, pergunte como a equipe fará replay depois.

**Elemento 35:** `Output/response` precisa ter uma responsabilidade clara. Quando dois elementos fazem a mesma coisa, o debug fica confuso.
Checagem KODA 35: identifique qual arquivo muda quando `Output/response` executa. Se nenhum arquivo muda, pergunte como a equipe fará replay depois.

**Elemento 36:** `feedback loops` precisa ter uma responsabilidade clara. Quando dois elementos fazem a mesma coisa, o debug fica confuso.
Checagem KODA 36: identifique qual arquivo muda quando `feedback loops` executa. Se nenhum arquivo muda, pergunte como a equipe fará replay depois.

**Elemento 37:** `Client/User entry point` precisa ter uma responsabilidade clara. Quando dois elementos fazem a mesma coisa, o debug fica confuso.
Checagem KODA 37: identifique qual arquivo muda quando `Client/User entry point` executa. Se nenhum arquivo muda, pergunte como a equipe fará replay depois.

**Elemento 38:** `Context manager` precisa ter uma responsabilidade clara. Quando dois elementos fazem a mesma coisa, o debug fica confuso.
Checagem KODA 38: identifique qual arquivo muda quando `Context manager` executa. Se nenhum arquivo muda, pergunte como a equipe fará replay depois.

**Elemento 39:** `state persistence layer` precisa ter uma responsabilidade clara. Quando dois elementos fazem a mesma coisa, o debug fica confuso.
Checagem KODA 39: identifique qual arquivo muda quando `state persistence layer` executa. Se nenhum arquivo muda, pergunte como a equipe fará replay depois.

**Elemento 40:** `Generator agents` precisa ter uma responsabilidade clara. Quando dois elementos fazem a mesma coisa, o debug fica confuso.
Checagem KODA 40: identifique qual arquivo muda quando `Generator agents` executa. Se nenhum arquivo muda, pergunte como a equipe fará replay depois.

**Elemento 41:** `Evaluator agents` precisa ter uma responsabilidade clara. Quando dois elementos fazem a mesma coisa, o debug fica confuso.
Checagem KODA 41: identifique qual arquivo muda quando `Evaluator agents` executa. Se nenhum arquivo muda, pergunte como a equipe fará replay depois.

**Elemento 42:** `file-based coordination` precisa ter uma responsabilidade clara. Quando dois elementos fazem a mesma coisa, o debug fica confuso.
Checagem KODA 42: identifique qual arquivo muda quando `file-based coordination` executa. Se nenhum arquivo muda, pergunte como a equipe fará replay depois.

**Elemento 43:** `Orchestrator / harness` precisa ter uma responsabilidade clara. Quando dois elementos fazem a mesma coisa, o debug fica confuso.
Checagem KODA 43: identifique qual arquivo muda quando `Orchestrator / harness` executa. Se nenhum arquivo muda, pergunte como a equipe fará replay depois.

**Elemento 44:** `Output/response` precisa ter uma responsabilidade clara. Quando dois elementos fazem a mesma coisa, o debug fica confuso.
Checagem KODA 44: identifique qual arquivo muda quando `Output/response` executa. Se nenhum arquivo muda, pergunte como a equipe fará replay depois.

**Elemento 45:** `feedback loops` precisa ter uma responsabilidade clara. Quando dois elementos fazem a mesma coisa, o debug fica confuso.
Checagem KODA 45: identifique qual arquivo muda quando `feedback loops` executa. Se nenhum arquivo muda, pergunte como a equipe fará replay depois.

**Elemento 46:** `Client/User entry point` precisa ter uma responsabilidade clara. Quando dois elementos fazem a mesma coisa, o debug fica confuso.
Checagem KODA 46: identifique qual arquivo muda quando `Client/User entry point` executa. Se nenhum arquivo muda, pergunte como a equipe fará replay depois.

**Elemento 47:** `Context manager` precisa ter uma responsabilidade clara. Quando dois elementos fazem a mesma coisa, o debug fica confuso.
Checagem KODA 47: identifique qual arquivo muda quando `Context manager` executa. Se nenhum arquivo muda, pergunte como a equipe fará replay depois.

**Elemento 48:** `state persistence layer` precisa ter uma responsabilidade clara. Quando dois elementos fazem a mesma coisa, o debug fica confuso.
Checagem KODA 48: identifique qual arquivo muda quando `state persistence layer` executa. Se nenhum arquivo muda, pergunte como a equipe fará replay depois.

**Elemento 49:** `Generator agents` precisa ter uma responsabilidade clara. Quando dois elementos fazem a mesma coisa, o debug fica confuso.
Checagem KODA 49: identifique qual arquivo muda quando `Generator agents` executa. Se nenhum arquivo muda, pergunte como a equipe fará replay depois.

**Elemento 50:** `Evaluator agents` precisa ter uma responsabilidade clara. Quando dois elementos fazem a mesma coisa, o debug fica confuso.
Checagem KODA 50: identifique qual arquivo muda quando `Evaluator agents` executa. Se nenhum arquivo muda, pergunte como a equipe fará replay depois.

**Elemento 51:** `file-based coordination` precisa ter uma responsabilidade clara. Quando dois elementos fazem a mesma coisa, o debug fica confuso.
Checagem KODA 51: identifique qual arquivo muda quando `file-based coordination` executa. Se nenhum arquivo muda, pergunte como a equipe fará replay depois.

**Elemento 52:** `Orchestrator / harness` precisa ter uma responsabilidade clara. Quando dois elementos fazem a mesma coisa, o debug fica confuso.
Checagem KODA 52: identifique qual arquivo muda quando `Orchestrator / harness` executa. Se nenhum arquivo muda, pergunte como a equipe fará replay depois.

**Elemento 53:** `Output/response` precisa ter uma responsabilidade clara. Quando dois elementos fazem a mesma coisa, o debug fica confuso.
Checagem KODA 53: identifique qual arquivo muda quando `Output/response` executa. Se nenhum arquivo muda, pergunte como a equipe fará replay depois.

**Elemento 54:** `feedback loops` precisa ter uma responsabilidade clara. Quando dois elementos fazem a mesma coisa, o debug fica confuso.
Checagem KODA 54: identifique qual arquivo muda quando `feedback loops` executa. Se nenhum arquivo muda, pergunte como a equipe fará replay depois.

**Elemento 55:** `Client/User entry point` precisa ter uma responsabilidade clara. Quando dois elementos fazem a mesma coisa, o debug fica confuso.
Checagem KODA 55: identifique qual arquivo muda quando `Client/User entry point` executa. Se nenhum arquivo muda, pergunte como a equipe fará replay depois.

**Elemento 56:** `Context manager` precisa ter uma responsabilidade clara. Quando dois elementos fazem a mesma coisa, o debug fica confuso.
Checagem KODA 56: identifique qual arquivo muda quando `Context manager` executa. Se nenhum arquivo muda, pergunte como a equipe fará replay depois.

**Elemento 57:** `state persistence layer` precisa ter uma responsabilidade clara. Quando dois elementos fazem a mesma coisa, o debug fica confuso.
Checagem KODA 57: identifique qual arquivo muda quando `state persistence layer` executa. Se nenhum arquivo muda, pergunte como a equipe fará replay depois.

**Elemento 58:** `Generator agents` precisa ter uma responsabilidade clara. Quando dois elementos fazem a mesma coisa, o debug fica confuso.
Checagem KODA 58: identifique qual arquivo muda quando `Generator agents` executa. Se nenhum arquivo muda, pergunte como a equipe fará replay depois.

**Elemento 59:** `Evaluator agents` precisa ter uma responsabilidade clara. Quando dois elementos fazem a mesma coisa, o debug fica confuso.
Checagem KODA 59: identifique qual arquivo muda quando `Evaluator agents` executa. Se nenhum arquivo muda, pergunte como a equipe fará replay depois.

**Elemento 60:** `file-based coordination` precisa ter uma responsabilidade clara. Quando dois elementos fazem a mesma coisa, o debug fica confuso.
Checagem KODA 60: identifique qual arquivo muda quando `file-based coordination` executa. Se nenhum arquivo muda, pergunte como a equipe fará replay depois.

**Elemento 61:** `Orchestrator / harness` precisa ter uma responsabilidade clara. Quando dois elementos fazem a mesma coisa, o debug fica confuso.
Checagem KODA 61: identifique qual arquivo muda quando `Orchestrator / harness` executa. Se nenhum arquivo muda, pergunte como a equipe fará replay depois.

**Elemento 62:** `Output/response` precisa ter uma responsabilidade clara. Quando dois elementos fazem a mesma coisa, o debug fica confuso.
Checagem KODA 62: identifique qual arquivo muda quando `Output/response` executa. Se nenhum arquivo muda, pergunte como a equipe fará replay depois.

**Elemento 63:** `feedback loops` precisa ter uma responsabilidade clara. Quando dois elementos fazem a mesma coisa, o debug fica confuso.
Checagem KODA 63: identifique qual arquivo muda quando `feedback loops` executa. Se nenhum arquivo muda, pergunte como a equipe fará replay depois.

**Elemento 64:** `Client/User entry point` precisa ter uma responsabilidade clara. Quando dois elementos fazem a mesma coisa, o debug fica confuso.
Checagem KODA 64: identifique qual arquivo muda quando `Client/User entry point` executa. Se nenhum arquivo muda, pergunte como a equipe fará replay depois.

**Elemento 65:** `Context manager` precisa ter uma responsabilidade clara. Quando dois elementos fazem a mesma coisa, o debug fica confuso.
Checagem KODA 65: identifique qual arquivo muda quando `Context manager` executa. Se nenhum arquivo muda, pergunte como a equipe fará replay depois.

**Elemento 66:** `state persistence layer` precisa ter uma responsabilidade clara. Quando dois elementos fazem a mesma coisa, o debug fica confuso.
Checagem KODA 66: identifique qual arquivo muda quando `state persistence layer` executa. Se nenhum arquivo muda, pergunte como a equipe fará replay depois.

**Elemento 67:** `Generator agents` precisa ter uma responsabilidade clara. Quando dois elementos fazem a mesma coisa, o debug fica confuso.
Checagem KODA 67: identifique qual arquivo muda quando `Generator agents` executa. Se nenhum arquivo muda, pergunte como a equipe fará replay depois.

**Elemento 68:** `Evaluator agents` precisa ter uma responsabilidade clara. Quando dois elementos fazem a mesma coisa, o debug fica confuso.
Checagem KODA 68: identifique qual arquivo muda quando `Evaluator agents` executa. Se nenhum arquivo muda, pergunte como a equipe fará replay depois.

**Elemento 69:** `file-based coordination` precisa ter uma responsabilidade clara. Quando dois elementos fazem a mesma coisa, o debug fica confuso.
Checagem KODA 69: identifique qual arquivo muda quando `file-based coordination` executa. Se nenhum arquivo muda, pergunte como a equipe fará replay depois.

**Elemento 70:** `Orchestrator / harness` precisa ter uma responsabilidade clara. Quando dois elementos fazem a mesma coisa, o debug fica confuso.
Checagem KODA 70: identifique qual arquivo muda quando `Orchestrator / harness` executa. Se nenhum arquivo muda, pergunte como a equipe fará replay depois.

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

**Cenário KODA 1:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 1: `state/session_id/artifact_001.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 1: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 1: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 2:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 2: `state/session_id/artifact_002.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 2: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 2: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 3:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 3: `state/session_id/artifact_003.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 3: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 3: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 4:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 4: `state/session_id/artifact_004.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 4: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 4: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 5:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 5: `state/session_id/artifact_005.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 5: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 5: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 6:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 6: `state/session_id/artifact_006.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 6: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 6: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 7:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 7: `state/session_id/artifact_007.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 7: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 7: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 8:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 8: `state/session_id/artifact_008.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 8: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 8: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 9:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 9: `state/session_id/artifact_009.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 9: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 9: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 10:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 10: `state/session_id/artifact_010.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 10: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 10: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 11:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 11: `state/session_id/artifact_011.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 11: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 11: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 12:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 12: `state/session_id/artifact_012.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 12: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 12: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 13:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 13: `state/session_id/artifact_013.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 13: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 13: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 14:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 14: `state/session_id/artifact_014.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 14: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 14: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 15:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 15: `state/session_id/artifact_015.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 15: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 15: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 16:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 16: `state/session_id/artifact_016.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 16: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 16: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 17:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 17: `state/session_id/artifact_017.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 17: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 17: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 18:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 18: `state/session_id/artifact_018.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 18: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 18: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 19:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 19: `state/session_id/artifact_019.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 19: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 19: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 20:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 20: `state/session_id/artifact_020.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 20: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 20: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 21:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 21: `state/session_id/artifact_021.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 21: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 21: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 22:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 22: `state/session_id/artifact_022.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 22: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 22: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 23:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 23: `state/session_id/artifact_023.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 23: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 23: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 24:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 24: `state/session_id/artifact_024.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 24: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 24: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 25:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 25: `state/session_id/artifact_025.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 25: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 25: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 26:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 26: `state/session_id/artifact_026.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 26: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 26: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 27:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 27: `state/session_id/artifact_027.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 27: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 27: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 28:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 28: `state/session_id/artifact_028.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 28: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 28: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 29:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 29: `state/session_id/artifact_029.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 29: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 29: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 30:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 30: `state/session_id/artifact_030.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 30: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 30: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 31:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 31: `state/session_id/artifact_031.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 31: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 31: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 32:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 32: `state/session_id/artifact_032.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 32: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 32: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 33:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 33: `state/session_id/artifact_033.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 33: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 33: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 34:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 34: `state/session_id/artifact_034.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 34: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 34: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 35:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 35: `state/session_id/artifact_035.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 35: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 35: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 36:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 36: `state/session_id/artifact_036.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 36: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 36: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 37:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 37: `state/session_id/artifact_037.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 37: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 37: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 38:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 38: `state/session_id/artifact_038.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 38: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 38: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 39:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 39: `state/session_id/artifact_039.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 39: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 39: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 40:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 40: `state/session_id/artifact_040.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 40: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 40: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 41:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 41: `state/session_id/artifact_041.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 41: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 41: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 42:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 42: `state/session_id/artifact_042.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 42: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 42: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 43:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 43: `state/session_id/artifact_043.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 43: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 43: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 44:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 44: `state/session_id/artifact_044.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 44: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 44: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 45:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 45: `state/session_id/artifact_045.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 45: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 45: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 46:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 46: `state/session_id/artifact_046.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 46: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 46: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 47:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 47: `state/session_id/artifact_047.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 47: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 47: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 48:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 48: `state/session_id/artifact_048.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 48: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 48: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 49:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 49: `state/session_id/artifact_049.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 49: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 49: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 50:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 50: `state/session_id/artifact_050.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 50: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 50: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 51:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 51: `state/session_id/artifact_051.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 51: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 51: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 52:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 52: `state/session_id/artifact_052.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 52: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 52: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 53:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 53: `state/session_id/artifact_053.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 53: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 53: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 54:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 54: `state/session_id/artifact_054.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 54: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 54: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 55:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 55: `state/session_id/artifact_055.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 55: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 55: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 56:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 56: `state/session_id/artifact_056.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 56: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 56: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 57:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 57: `state/session_id/artifact_057.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 57: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 57: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 58:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 58: `state/session_id/artifact_058.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 58: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 58: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 59:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 59: `state/session_id/artifact_059.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 59: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 59: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 60:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 60: `state/session_id/artifact_060.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 60: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 60: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 61:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 61: `state/session_id/artifact_061.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 61: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 61: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 62:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 62: `state/session_id/artifact_062.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 62: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 62: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 63:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 63: `state/session_id/artifact_063.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 63: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 63: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 64:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 64: `state/session_id/artifact_064.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 64: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 64: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 65:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 65: `state/session_id/artifact_065.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 65: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 65: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 66:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 66: `state/session_id/artifact_066.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 66: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 66: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 67:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 67: `state/session_id/artifact_067.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 67: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 67: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 68:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 68: `state/session_id/artifact_068.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 68: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 68: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 69:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 69: `state/session_id/artifact_069.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 69: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 69: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 70:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 70: `state/session_id/artifact_070.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 70: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 70: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 71:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 71: `state/session_id/artifact_071.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 71: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 71: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 72:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 72: `state/session_id/artifact_072.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 72: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 72: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 73:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 73: `state/session_id/artifact_073.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 73: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 73: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 74:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 74: `state/session_id/artifact_074.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 74: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 74: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 75:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 75: `state/session_id/artifact_075.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 75: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 75: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 76:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 76: `state/session_id/artifact_076.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 76: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 76: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 77:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 77: `state/session_id/artifact_077.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 77: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 77: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 78:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 78: `state/session_id/artifact_078.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 78: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 78: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 79:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 79: `state/session_id/artifact_079.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 79: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 79: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 80:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 80: `state/session_id/artifact_080.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 80: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 80: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 81:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 81: `state/session_id/artifact_081.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 81: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 81: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 82:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 82: `state/session_id/artifact_082.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 82: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 82: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 83:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 83: `state/session_id/artifact_083.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 83: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 83: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 84:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 84: `state/session_id/artifact_084.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 84: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 84: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 85:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 85: `state/session_id/artifact_085.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 85: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 85: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 86:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 86: `state/session_id/artifact_086.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 86: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 86: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 87:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 87: `state/session_id/artifact_087.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 87: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 87: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 88:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 88: `state/session_id/artifact_088.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 88: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 88: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 89:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 89: `state/session_id/artifact_089.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 89: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 89: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 90:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 90: `state/session_id/artifact_090.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 90: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 90: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 91:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 91: `state/session_id/artifact_091.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 91: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 91: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 92:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 92: `state/session_id/artifact_092.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 92: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 92: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 93:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 93: `state/session_id/artifact_093.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 93: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 93: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 94:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 94: `state/session_id/artifact_094.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 94: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 94: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 95:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 95: `state/session_id/artifact_095.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 95: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 95: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 96:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 96: `state/session_id/artifact_096.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 96: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 96: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 97:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 97: `state/session_id/artifact_097.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 97: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 97: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 98:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 98: `state/session_id/artifact_098.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 98: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 98: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 99:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 99: `state/session_id/artifact_099.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 99: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 99: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 100:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 100: `state/session_id/artifact_100.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 100: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 100: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 101:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 101: `state/session_id/artifact_101.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 101: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 101: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 102:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 102: `state/session_id/artifact_102.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 102: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 102: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 103:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 103: `state/session_id/artifact_103.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 103: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 103: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 104:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 104: `state/session_id/artifact_104.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 104: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 104: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 105:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 105: `state/session_id/artifact_105.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 105: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 105: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 106:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 106: `state/session_id/artifact_106.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 106: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 106: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 107:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 107: `state/session_id/artifact_107.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 107: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 107: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 108:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 108: `state/session_id/artifact_108.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 108: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 108: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 109:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 109: `state/session_id/artifact_109.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 109: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 109: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 110:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 110: `state/session_id/artifact_110.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 110: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 110: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 111:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 111: `state/session_id/artifact_111.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 111: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 111: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 112:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 112: `state/session_id/artifact_112.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 112: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 112: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 113:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 113: `state/session_id/artifact_113.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 113: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 113: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 114:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 114: `state/session_id/artifact_114.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 114: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 114: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 115:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 115: `state/session_id/artifact_115.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 115: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 115: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 116:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 116: `state/session_id/artifact_116.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 116: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 116: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 117:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 117: `state/session_id/artifact_117.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 117: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 117: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 118:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 118: `state/session_id/artifact_118.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 118: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 118: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 119:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 119: `state/session_id/artifact_119.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 119: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 119: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

**Cenário KODA 120:** Quando uma conversa passa por recomendação, preço e entrega, cada etapa deve escrever seu resultado antes da próxima começar.
Arquivo esperado 120: `state/session_id/artifact_120.json` representa uma decisão verificável, como produto escolhido, desconto aplicado ou veredito de segurança.
Pergunta de revisão 120: se o cliente reclamar amanhã, qual artefato mostra por que KODA respondeu daquele jeito?
Critério de aprovação 120: a resposta só deve sair quando o Evaluator confirmar que o draft respeita restrições, orçamento, estoque e clareza.

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
