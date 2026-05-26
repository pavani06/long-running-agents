# 🔗 Sistemas Multi-Agente para Arquiteturas Confiaveis
## Como Planner, Generator e Evaluator Transformam Jornadas Longas em Fluxos Auditaveis

**Tempo Estimado:** 120 minutos  
**Nivel:** 3 - Arquitetura Avancada  
**Pre-requisito:** Ter completado `02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md`  
**Status:** 🟢 CRITICO - Base para decompor jornadas complexas do KODA  
**Data de Criacao:** Maio 2026

---

## 📖 Prologo: A Noite em que Um Agente Sozinho Quase Perdeu a Venda

**Cenario Real: quinta-feira, 19h42.**

A academia do bairro tinha acabado de fechar.

Marina saiu cansada, com a garrafa vazia na mochila e uma decisao nova na cabeca: ela queria voltar a treinar com consistencia.

Ela tinha comprado suplementos antes, mas sempre se sentia perdida.

Whey concentrado, whey isolado, creatina, pre-treino, hipercalorico, tabela nutricional, promessa de ganho rapido.

Tudo parecia feito para quem ja entendia do assunto.

Naquela noite, uma amiga indicou o WhatsApp do KODA.

Marina abriu a conversa.

```
19:43 Marina: Oi, estou voltando a treinar e queria ajuda para comprar suplemento.
19:43 KODA: Oi, Marina. Me conta seu objetivo principal e qualquer restricao alimentar.
19:44 Marina: Quero ganhar massa, mas sem engordar muito. Tenho intolerancia a lactose.
```

A primeira resposta foi boa.

O agente unico entendeu o objetivo, perguntou contexto e buscou produtos.

Por alguns minutos, tudo parecia simples.

```
19:46 KODA: Para ganho de massa com intolerancia a lactose, posso olhar whey isolado sem lactose, proteina vegetal e creatina.
19:47 Marina: Tenho ate R$ 220 este mes. Quero algo que dure pelo menos um mes.
19:48 KODA: Entendido. Vou priorizar custo por dose, ausencia de lactose e produtos com boa avaliacao.
```

Marina ficou aliviada.

Ela nao queria falar com um vendedor que empurrasse o produto mais caro.

Queria alguem que acompanhasse a situacao dela.

**Minuto 10:** a conversa cresceu.

```
19:53 Marina: Eu treino 4 vezes por semana.
19:53 Marina: Tambem tomo cafe a tarde, entao nao quero algo que atrapalhe meu sono.
19:54 Marina: Tem alguma coisa com chocolate?
19:55 Marina: E se eu comprar creatina junto, fica melhor?
```

O agente unico tentou responder tudo de uma vez.

Ele misturou descoberta de necessidade, busca de catalogo, comparacao de preco, explicacao nutricional e preparacao de pedido.

A resposta ficou longa.

Parecia completa, mas escondia confusao.

```
19:56 KODA: Recomendo Whey Isolado Chocolate 900g, Creatina Monohidratada 300g e um pre-treino leve sem cafeina.
19:57 Marina: Mas eu falei que tenho R$ 220. Quanto daria tudo?
19:58 KODA: O combo fica R$ 287,90.
19:58 Marina: Entao nao cabe no meu orcamento.
```

A primeira rachadura apareceu.

O agente tinha registrado o orcamento.

Mesmo assim, montou um combo acima do limite.

Ele estava tentando ser util, mas confundiu a meta principal.

**Minuto 18:** Marina continuou, porque queria resolver naquela noite.

```
20:01 Marina: Se eu comprar so um produto agora, qual seria melhor?
20:02 KODA: O whey isolado sem lactose, porque ajuda na proteina diaria.
20:03 Marina: Qual preco?
20:03 KODA: R$ 199,90.
20:04 Marina: Dura um mes?
20:04 KODA: Sim, dura 30 doses.
```

A resposta parecia boa.

Mas a ficha tecnica do produto dizia 24 doses.

O agente unico nao percebeu.

Ele gerou a recomendacao e validou a propria frase com excesso de confianca.

**Minuto 26:** a conversa entrou no territorio que quebra agentes simples.

```
20:09 Marina: Minha amiga falou de uma proteina vegetal de baunilha. Ela e melhor?
20:10 KODA: Sim, pode ser melhor para intolerancia a lactose.
20:10 Marina: Mas eu prefiro chocolate.
20:11 KODA: Temos vegetal baunilha com 20% de desconto.
20:11 Marina: Eu perguntei se e melhor, nao se tem desconto.
```

Agora o problema nao era so preco.

Era atencao.

O agente estava pulando entre criterios: sabor, desconto, restricao alimentar, duracao, estoque e objetivo de treino.

Tudo dentro da mesma context window.

Tudo dentro do mesmo processo mental.

**Minuto 32:** Marina quase desistiu.

```
20:15 Marina: KODA, estou confusa. Qual voce compraria no meu lugar?
20:16 KODA: Eu compraria o Whey Concentrado Chocolate, melhor custo-beneficio.
20:16 Marina: Mas eu tenho intolerancia a lactose.
20:17 KODA: Desculpe, voce tem razao. Vou corrigir.
```

Esse tipo de erro fere a confianca.

Nao e apenas uma resposta errada.

E a sensacao de que o assistente nao estava realmente ouvindo.

**Minuto 38:** a equipe KODA, observando o trace, percebeu o padrao.

O agente unico tinha responsabilidades demais:

1. Entender a jornada emocional da cliente.
2. Coletar restricoes alimentares.
3. Consultar catalogo e estoque.
4. Comparar preco por dose.
5. Explicar trade-offs de produto.
6. Preparar carrinho.
7. Validar se cada etapa respeitava o orcamento.
8. Manter tom humano no WhatsApp.

Nenhuma dessas tarefas e impossivel.

O problema e pedir que uma unica chamada, um unico agente, uma unica trilha de raciocinio faca tudo ao mesmo tempo.

A arquitetura estava criando o erro.

**Minuto 44:** a equipe simulou outra abordagem.

Em vez de um agente unico, a conversa passaria por tres papeis internos.

O Planner decomporia a jornada: descobrir necessidade, filtrar restricoes, comparar opcoes, montar pedido.

O Generator executaria cada etapa planejada, criando respostas e artefatos estruturados.

O Evaluator validaria se a resposta respeitava fatos, orcamento, restricoes e tom.

Marina continuaria vendo um unico KODA no WhatsApp.

Por tras da interface, porem, haveria uma pequena equipe.

**Minuto 51:** a mesma conversa foi reprocessada.

```
20:26 Planner: Etapa atual e comparacao de duas opcoes sem lactose dentro de R$ 220.
20:26 Generator: Criando resposta com Whey Isolado Chocolate e Proteina Vegetal Baunilha.
20:26 Evaluator: Verificando lactose, preco, doses, preferencia por chocolate e clareza.
20:27 KODA: Marina, no seu caso eu escolheria o Whey Isolado Chocolate agora. Ele respeita sua intolerancia, fica dentro dos R$ 220 e combina com sua preferencia de sabor. A proteina vegetal e segura tambem, mas perde no sabor que voce pediu.
```

A diferenca foi imediata.

O KODA nao ficou mais frio.

Nao virou um fluxo robotico.

Ele ficou mais claro, porque cada responsabilidade tinha um dono.

**Minuto 59:** Marina fechou o pedido.

```
20:35 Marina: Pode fechar o whey isolado chocolate.
20:35 KODA: Posso sim. Vou confirmar estoque, endereco e forma de pagamento antes de finalizar.
20:36 Marina: Entrega em Pinheiros, Sao Paulo.
20:37 KODA: Estoque confirmado em SP. Entrega estimada para amanha. Total R$ 199,90, sem lactose, sabor chocolate. Posso gerar o link de pagamento?
20:38 Marina: Pode.
```

O pedido aconteceu porque a arquitetura segurou a conversa.

Nao foi magia de modelo.

Foi decomposicao, state persistence e avaliacao independente.

Este modulo ensina exatamente isso.

Ao final, voce vai enxergar multi-agent systems nao como moda, mas como uma forma concreta de proteger jornadas longas contra confusao, esquecimento e auto-aprovacao.

---

## 🔗 Conexao com Nivel 2

No Nivel 2, voce aprendeu o padrao Generator/Evaluator em `02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md`.

A ideia central era simples: separar quem cria de quem avalia.

O Generator produz uma solucao.

O Evaluator valida a solucao contra uma rubrica.

Essa separacao reduz sycophancy, aumenta auditabilidade e cria um checkpoint antes da resposta chegar ao cliente.

Multi-agent systems pegam essa mesma ideia e generalizam.

Generator/Evaluator e o caso de 2 agentes do padrao N-agent.

| Nivel | Arquitetura | Pergunta Principal | Resultado |
| --- | --- | --- | --- |
| Nivel 2 | Generator + Evaluator | A resposta gerada esta correta? | Qualidade por verificacao independente |
| Nivel 3 | Planner + Generator + Evaluator | Qual trabalho precisa ser feito, como executar e como validar? | Qualidade por decomposicao completa |
| Nivel 3 expandido | N agentes especializados | Qual parte da jornada cada agente deve possuir? | Escala para customer journeys longos |

A mudanca do Nivel 2 para o Nivel 3 nao contradiz o que voce aprendeu.

Ela preserva o Generator/Evaluator e adiciona uma responsabilidade antes da geracao: planejamento explicito.

Sem Planner, o Generator ainda precisa decidir o que fazer.

Com Planner, o Generator recebe uma tarefa menor, mais clara e mais facil de executar.

No Nivel 2, o fluxo era:

```
Cliente e contexto
    ↓
Generator
    ↓
Evaluator
    ↓
Resposta aprovada
```

No Nivel 3, o fluxo passa a ser:

```
Cliente e contexto
    ↓
Planner
    ↓
Generator
    ↓
Evaluator
    ↓
Resposta aprovada ou novo ciclo
```

A diferenca parece pequena.

Na pratica, ela muda tudo.

O Planner impede que o Generator tente resolver uma jornada inteira sem mapa.

Ele transforma uma conversa baguncada em uma sequencia de etapas observaveis.

O Evaluator continua sendo o gatekeeper aprendido no Nivel 2.

Agora ele tambem valida se o Generator cumpriu o plano, nao apenas se a resposta final parece boa.

Isso cria tres camadas de seguranca:

1. O Planner reduz ambiguidade.
2. O Generator reduz escopo por execucao focada.
3. O Evaluator reduz erro por verificacao independente.

Pense assim: Generator/Evaluator era uma dupla de escritor e editor.

Planner, Generator e Evaluator viram editor-chefe, escritor e revisor tecnico.

O editor-chefe define a pauta.

O escritor escreve.

O revisor tecnico protege o leitor.

Para o KODA, isso significa que uma pergunta como "qual suplemento eu compro?" deixa de ser uma resposta unica.

Ela vira uma pequena jornada:

1. Identificar objetivo.
2. Identificar restricoes.
3. Consultar catalogo.
4. Comparar opcoes.
5. Explicar recomendacao.
6. Validar pedido.
7. Preparar checkout.

Cada etapa pode ter estado, output e criterios proprios.

Essa e a ponte entre o Nivel 2 e o Nivel 3.

---

## 🏗️ Arquitetura Multi-Agente: Planner, Generator, Evaluator

Uma arquitetura multi-agente nao significa colocar varios modelos conversando sem controle.

Essa e a versao caotica.

A versao profissional e um harness que define papeis, contratos, arquivos de estado e criterios de passagem.

Neste modulo, vamos usar a arquitetura base de 3 agentes.

Ela e simples o suficiente para implementar.

Tambem e forte o suficiente para sustentar jornadas reais do KODA.

### Papel 1: Planner

O Planner e responsavel por decompor a tarefa, criar plano operacional e definir criterios de sucesso.

Responsabilidades do Planner:

1. Ler a conversa atual e o state persistido.
2. Identificar o objetivo imediato do cliente.
3. Separar a jornada em etapas pequenas.
4. Definir quais dados faltam.
5. Escolher a proxima acao segura.
6. Registrar criterios de sucesso para o Generator.
7. Registrar criterios de validacao para o Evaluator.

### Papel 2: Generator

O Generator e responsavel por executar cada etapa planejada sem aprovar o proprio trabalho.

Responsabilidades do Generator:

1. Ler o plano do Planner.
2. Executar os passos designados.
3. Consultar ferramentas permitidas, como catalogo, estoque ou calculadora de frete.
4. Produzir output estruturado.
5. Registrar suposicoes explicitamente.
6. Nao aprovar o proprio trabalho.
7. Salvar resultado para o Evaluator.

### Papel 3: Evaluator

O Evaluator e responsavel por validar resultado, proteger cliente e decidir aprovacao ou revisao.

Responsabilidades do Evaluator:

1. Ler o plano original.
2. Ler o output do Generator.
3. Validar cada criterio da rubrica.
4. Detectar contradicoes com o state persistido.
5. Verificar se ha afirmacoes sem evidencia.
6. Aprovar, rejeitar ou pedir revisao.
7. Registrar feedback especifico.

```json
{
  "conversation_id": "wa_2026_05_26_marina",
  "current_goal": "recomendar um produto principal dentro do orcamento",
  "known_constraints": {
    "budget_brl": 220,
    "dietary_restrictions": ["intolerancia_lactose"],
    "preferred_flavor": "chocolate",
    "training_frequency": "4x_semana"
  },
  "plan": [
    {
      "step_id": "s1",
      "task": "filtrar produtos sem lactose abaixo de R$ 220",
      "owner": "generator",
      "success_criteria": ["produto existe", "preco <= 220", "sem lactose"]
    },
    {
      "step_id": "s2",
      "task": "comparar ate duas alternativas por custo por dose",
      "owner": "generator",
      "success_criteria": ["maximo 2 opcoes", "explicar trade-off", "nao exceder orcamento"]
    },
    {
      "step_id": "s3",
      "task": "preparar resposta curta para WhatsApp",
      "owner": "generator",
      "success_criteria": ["tom humano", "sem jargao excessivo", "pergunta final clara"]
    }
  ],
  "evaluation_rubric": [
    "respeita restricao de lactose",
    "respeita orcamento",
    "nao inventa estoque",
    "explica recomendacao sem pressionar compra"
  ]
}
```

```json
{
  "conversation_id": "wa_2026_05_26_marina",
  "step_id": "s3",
  "generated_at": "2026-05-26T20:27:12-03:00",
  "candidate_response": "Marina, no seu caso eu escolheria o Whey Isolado Chocolate agora. Ele respeita sua intolerancia, fica dentro dos R$ 220 e combina com sua preferencia de sabor. A proteina vegetal tambem e segura, mas perde no sabor que voce pediu. Posso confirmar estoque em SP?",
  "products_considered": [
    {
      "sku": "WHEY-ISO-CHOC-900",
      "name": "Whey Isolado Chocolate 900g",
      "price_brl": 199.9,
      "servings": 24,
      "lactose_free": true
    },
    {
      "sku": "PROT-VEG-BAUN-750",
      "name": "Proteina Vegetal Baunilha 750g",
      "price_brl": 179.9,
      "servings": 25,
      "lactose_free": true
    }
  ],
  "assumptions": [
    "cliente prefere chocolate quando opcoes sao equivalentes",
    "cliente quer escolher um produto agora, nao montar combo"
  ]
}
```

```json
{
  "conversation_id": "wa_2026_05_26_marina",
  "evaluated_step_id": "s3",
  "status": "approved",
  "checked_at": "2026-05-26T20:27:18-03:00",
  "rubric_results": [
    { "criterion": "respeita restricao de lactose", "passed": true, "evidence": "ambos os produtos marcados como lactose_free" },
    { "criterion": "respeita orcamento", "passed": true, "evidence": "produto recomendado custa R$ 199,90" },
    { "criterion": "nao inventa estoque", "passed": true, "evidence": "resposta pede confirmacao de estoque antes de afirmar disponibilidade" },
    { "criterion": "tom humano", "passed": true, "evidence": "resposta curta, direta e sem pressao" }
  ],
  "customer_visible_response": "Marina, no seu caso eu escolheria o Whey Isolado Chocolate agora. Ele respeita sua intolerancia, fica dentro dos R$ 220 e combina com sua preferencia de sabor. A proteina vegetal tambem e segura, mas perde no sabor que voce pediu. Posso confirmar estoque em SP?"
}
```

### Diagrama da Arquitetura

```
┌────────────────────────────────────────────────────────────────────┐
│                         WhatsApp Cliente                           │
│        mensagem, historico resumido, preferencias, pedido           │
└───────────────────────────────┬────────────────────────────────────┘
                                │
                                ▼
┌────────────────────────────────────────────────────────────────────┐
│                         State Store                                │
│  conversation.json │ customer_profile.json │ catalog_snapshot.json  │
└───────────────────────────────┬────────────────────────────────────┘
                                │
                                ▼
┌────────────────────────────────────────────────────────────────────┐
│                              Planner                               │
│  decompoe tarefa │ define etapas │ cria criterios de sucesso        │
└───────────────────────────────┬────────────────────────────────────┘
                                │ plan.json
                                ▼
┌────────────────────────────────────────────────────────────────────┐
│                             Generator                              │
│  executa etapa │ consulta ferramentas │ gera resposta candidata      │
└───────────────────────────────┬────────────────────────────────────┘
                                │ generation.json
                                ▼
┌────────────────────────────────────────────────────────────────────┐
│                             Evaluator                              │
│  valida rubrica │ checa fatos │ aprova, rejeita ou pede revisao     │
└───────────────┬───────────────────────────────────┬────────────────┘
                │ approved                          │ rejected
                ▼                                   ▼
┌──────────────────────────────┐       ┌─────────────────────────────┐
│ Resposta para o cliente       │       │ Feedback para novo ciclo     │
│ enviada pelo KODA             │       │ Planner ou Generator         │
└──────────────────────────────┘       └─────────────────────────────┘
```

### Data Flow Entre Agentes

| Etapa | Input | Output | Dono | Persistencia |
| --- | --- | --- | --- | --- |
| Entrada | mensagem do WhatsApp, perfil, historico resumido | evento de conversa | harness | `conversation_event.json` |
| Planejamento | evento, state, catalog snapshot | plano com etapas e rubrica | Planner | `plan.json` |
| Geracao | plano, ferramentas, dados de catalogo | resposta candidata e evidencias | Generator | `generation.json` |
| Avaliacao | plano, geracao, state | decisao e feedback | Evaluator | `evaluation.json` |
| Entrega | resposta aprovada | mensagem final | harness | `delivery.json` |

Um agente unico pode responder bem em conversas curtas.

Ele falha quando a jornada combina muitos objetivos ao mesmo tempo.

O problema nao e falta de inteligencia.

O problema e acoplamento de responsabilidades.

Quando o mesmo agente planeja, executa e valida, tres riscos aparecem:

1. O plano fica implicito e dificil de debugar.
2. A execucao muda o plano sem avisar.
3. A avaliacao confirma a propria resposta por sycophancy.

Tres agentes reduzem esses riscos por design.

O Planner cria um mapa antes da acao.

O Generator segue o mapa e deixa rastros.

O Evaluator compara resultado contra mapa e fatos.

Essa estrutura tambem melhora token budget.

Cada agente recebe apenas o contexto necessario para sua etapa.

Resultado: menos context rot, mais clareza e mais state persistence.

### Pseudocodigo de Orquestracao

```python
from pathlib import Path
import json

STATE_DIR = Path("state/conversations/wa_2026_05_26_marina")

def write_json(name, payload):
    path = STATE_DIR / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2))
    return path

def read_json(name):
    return json.loads((STATE_DIR / name).read_text())

def run_customer_turn(message):
    event = {
        "message": message,
        "channel": "whatsapp",
        "received_at": "2026-05-26T20:26:03-03:00"
    }
    write_json("conversation_event.json", event)

    plan = planner_agent(
        event=event,
        profile=read_json("customer_profile.json"),
        conversation=read_json("conversation_summary.json")
    )
    write_json("plan.json", plan)

    generation = generator_agent(
        plan=plan,
        catalog=read_json("catalog_snapshot.json")
    )
    write_json("generation.json", generation)

    evaluation = evaluator_agent(
        plan=plan,
        generation=generation,
        profile=read_json("customer_profile.json")
    )
    write_json("evaluation.json", evaluation)

    if evaluation["status"] == "approved":
        return evaluation["customer_visible_response"]

    revision = generator_agent(
        plan=plan,
        catalog=read_json("catalog_snapshot.json"),
        evaluator_feedback=evaluation["feedback"]
    )
    write_json("generation_revision.json", revision)

    final_evaluation = evaluator_agent(
        plan=plan,
        generation=revision,
        profile=read_json("customer_profile.json")
    )
    write_json("evaluation_final.json", final_evaluation)

    if final_evaluation["status"] != "approved":
        return "Quero confirmar um detalhe antes de te responder com seguranca."

    return final_evaluation["customer_visible_response"]
```

Esse pseudocodigo mostra o ponto central: agentes nao se comunicam por intuicao.

Eles se comunicam por artefatos.

Os arquivos criam memoria externa, audit trail e pontos de retomada.

---

## 📡 Canais de Comunicacao entre Agentes

Agentes precisam trocar informacao.

A pergunta arquitetural e: por qual canal?

Existem tres familias principais para KODA: file-based, message queues e API-based.

A recomendacao para este curriculo e comecar com file-based coordination.

Arquivos JSON em disco sao simples, auditaveis e bons para aprendizado.

Eles tambem sao uma excelente base para evoluir depois para Redis, RabbitMQ, REST ou gRPC.

| Canal | Latencia | Confiabilidade | Complexidade | Quando Usar |
| --- | --- | --- | --- | --- |
| File-based JSON | Baixa a media | Alta quando escrito de forma atomica | Baixa | Prototipos, curriculum, traces, workflows auditaveis, KODA em fase de desenho |
| Message queues Redis | Muito baixa | Media a alta com retries e ack | Media | Eventos frequentes, multiplos workers, processamento paralelo leve |
| Message queues RabbitMQ | Baixa | Alta com filas duraveis | Alta | Workflows criticos, backpressure, entrega garantida, operacao mais madura |
| API-based REST | Media | Alta se houver idempotencia | Media | Servicos separados, integracao simples entre times, chamadas sincrona |
| API-based gRPC | Baixa | Alta com contratos fortes | Alta | Baixa latencia, alto volume, schemas rigidos, comunicacao interna |

### Canal 1: File-based Coordination

File-based coordination usa arquivos como contrato entre agentes.

O Planner escreve `plan.json`.

O Generator le `plan.json` e escreve `generation.json`.

O Evaluator le os dois e escreve `evaluation.json`.

Vantagens:

1. Facil de entender.
2. Facil de versionar em exemplos.
3. Facil de debugar com trace reading.
4. Funciona bem em tarefas longas.
5. Cria state persistence naturalmente.

Cuidados:

1. Escrever de forma atomica para evitar arquivo parcial.
2. Usar nomes previsiveis.
3. Incluir `schema_version`.
4. Registrar timestamps.
5. Evitar segredos nos arquivos.

```
state/
└── conversations/
    └── wa_2026_05_26_marina/
        ├── conversation_event.json
        ├── customer_profile.json
        ├── conversation_summary.json
        ├── catalog_snapshot.json
        ├── plan.json
        ├── generation.json
        ├── evaluation.json
        └── delivery.json
```

Exemplo de `conversation_event.json`:

```json
{
  "schema_version": "1.0",
  "conversation_id": "wa_2026_05_26_marina",
  "turn_id": "turn_020",
  "channel": "whatsapp",
  "received_at": "2026-05-26T20:26:03-03:00",
  "customer_message": "Qual voce compraria no meu lugar?",
  "known_context_refs": [
    "customer_profile.json",
    "conversation_summary.json",
    "catalog_snapshot.json"
  ]
}
```

Exemplo de `customer_profile.json`:

```json
{
  "schema_version": "1.0",
  "customer_id": "cust_marina_4821",
  "name": "Marina",
  "dietary_restrictions": ["intolerancia_lactose"],
  "preferences": {
    "flavor": "chocolate",
    "budget_brl": 220,
    "training_goal": "ganho_de_massa_com_controle_de_peso",
    "training_frequency": "4x_semana"
  },
  "risk_notes": [
    "nao recomendar produtos com lactose",
    "nao recomendar estimulantes perto da noite"
  ]
}
```

Exemplo de `delivery.json`:

```json
{
  "schema_version": "1.0",
  "conversation_id": "wa_2026_05_26_marina",
  "turn_id": "turn_020",
  "sent_at": "2026-05-26T20:27:21-03:00",
  "approved_by": "evaluator",
  "message": "Marina, no seu caso eu escolheria o Whey Isolado Chocolate agora. Ele respeita sua intolerancia, fica dentro dos R$ 220 e combina com sua preferencia de sabor. Posso confirmar estoque em SP?",
  "audit_refs": ["plan.json", "generation.json", "evaluation.json"]
}
```

### Canal 2: Message Queues

Message queues entram quando voce precisa de paralelismo real ou alto volume.

Redis pode ser suficiente quando a prioridade e velocidade e simplicidade operacional.

RabbitMQ e melhor quando voce precisa de roteamento, durabilidade e controle fino de entrega.

Em KODA, filas podem aparecer quando varios Generators trabalham em paralelo:

1. Generator de recomendacao.
2. Generator de precificacao.
3. Generator de frete.
4. Generator de risco de restricao alimentar.

Cada worker consome um evento e publica resultado.

O Evaluator espera todos os resultados antes de aprovar a resposta final.

```json
{
  "event_type": "generator.requested",
  "conversation_id": "wa_2026_05_26_marina",
  "task_id": "compare_products",
  "required_outputs": ["product_options", "price_per_serving", "constraint_warnings"],
  "reply_to": "koda.generator.results",
  "created_at": "2026-05-26T20:26:04-03:00"
}
```

### Canal 3: API-based Communication

API-based communication usa chamadas REST ou gRPC entre servicos.

Ela combina bem quando cada agente e um servico separado com deploy proprio.

REST e mais simples para times diferentes entenderem.

gRPC e melhor para contratos fortes e baixa latencia.

```json
{
  "method": "POST",
  "path": "/agents/planner/plan",
  "body": {
    "conversation_id": "wa_2026_05_26_marina",
    "turn_id": "turn_020",
    "state_refs": ["customer_profile", "conversation_summary", "catalog_snapshot"]
  },
  "response": {
    "plan_id": "plan_020",
    "status": "created",
    "plan_ref": "state/conversations/wa_2026_05_26_marina/plan.json"
  }
}
```

### Como Escolher o Canal

Use file-based quando o time ainda esta aprendendo o dominio.

Use queues quando o gargalo e throughput ou paralelismo.

Use APIs quando a fronteira entre agentes tambem e fronteira entre servicos.

Para KODA, uma evolucao saudavel costuma ser:

1. Comecar com arquivos JSON para desenhar contratos.
2. Validar trace reading e rubricas.
3. Mover partes quentes para filas quando houver volume.
4. Expor APIs quando houver times ou servicos independentes.

---

## 🎯 Strategies de Coordenacao

Canais dizem por onde agentes se comunicam.

Strategies de coordenacao dizem quando e em que ordem eles trabalham.

As tres strategies principais sao sequencial, paralelo e event-driven.

| Estrategia | Fluxo | Vantagens | Desvantagens | Caso de Uso KODA |
| --- | --- | --- | --- | --- |
| Sequencial | Planner para Generator para Evaluator | Simples, auditavel, facil de debugar | Menor velocidade, cada etapa espera a anterior | Recomendacao com risco alimentar ou fechamento de pedido |
| Paralelo | Planner cria subtarefas e varios Generators executam ao mesmo tempo | Reduz latencia, explora alternativas, escala comparacoes | Exige agregacao, risco de resultados inconsistentes | Comparar produtos, frete, estoque e promocoes em paralelo |
| Event-driven | Agentes reagem a mudancas no state | Bom para jornadas longas, desacopla componentes, permite retomada | Mais dificil de observar, precisa governanca de eventos | Atualizacao de estoque, abandono de carrinho, pagamento aprovado |

### Estrategia 1: Sequencial

Sequencial define uma forma especifica de coordenar agentes em KODA.

```
┌──────────┐     plan.json      ┌────────────┐   generation.json   ┌────────────┐
│ Planner  │ ─────────────────▶ │ Generator  │ ─────────────────▶ │ Evaluator  │
└──────────┘                    └────────────┘                     └─────┬──────┘
                                                                        │
                                                                        ▼
                                                              ┌──────────────────┐
                                                              │ WhatsApp Response │
                                                              └──────────────────┘
```

Use quando:

1. O erro custa caro.
2. A jornada precisa de audit trail claro.
3. A resposta depende de uma ordem logica.
4. O time ainda esta estabilizando os contratos.

### Estrategia 2: Paralelo

Paralelo define uma forma especifica de coordenar agentes em KODA.

```
                            ┌────────────────────┐
                            │      Planner       │
                            └─────────┬──────────┘
                                      │
             ┌────────────────────────┼────────────────────────┐
             ▼                        ▼                        ▼
┌────────────────────┐   ┌────────────────────┐   ┌────────────────────┐
│ Product Generator  │   │  Price Generator   │   │ Freight Generator  │
└─────────┬──────────┘   └─────────┬──────────┘   └─────────┬──────────┘
          │                        │                        │
          └────────────────────────┼────────────────────────┘
                                   ▼
                         ┌────────────────────┐
                         │     Evaluator      │
                         └─────────┬──────────┘
                                   ▼
                         ┌────────────────────┐
                         │ Resposta Aprovada  │
                         └────────────────────┘
```

Use quando:

1. As subtarefas sao independentes.
2. Latencia importa.
3. Voce precisa comparar alternativas.
4. Existe um bom Evaluator para reconciliar resultados.

### Estrategia 3: Event-driven

Event-driven define uma forma especifica de coordenar agentes em KODA.

```
┌────────────────────┐
│  State Change       │
│  cart.updated       │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐       ┌────────────────────┐
│ Event Bus           │──────▶│ Recommendation     │
│ watches changes     │       │ Agent              │
└─────────┬──────────┘       └────────────────────┘
          │
          ▼
┌────────────────────┐       ┌────────────────────┐
│ Order Agent         │──────▶│ Fulfillment Agent  │
│ reacts to checkout  │       │ reacts to paid     │
└────────────────────┘       └────────────────────┘
```

Use quando:

1. A jornada dura horas ou dias.
2. Eventos externos mudam o estado, como pagamento aprovado.
3. Nem tudo acontece dentro da conversa do WhatsApp.
4. Voce precisa retomar workflows sem depender da context window.

Regras praticas de coordenacao:

1. Comece sequencial para aprender os contratos.
2. Paralelize apenas tarefas independentes.
3. Use event-driven para jornadas que continuam fora do turno atual.
4. Nunca deixe dois agentes escreverem o mesmo campo sem regra de ownership.
5. Sempre registre quem escreveu cada decisao.
6. Sempre permita replay do trace.
7. Trate state como fonte de verdade, nao a memoria temporaria do modelo.

---

## 🎓 Aplicacao KODA: Decomposicao do Customer Journey em Agentes

Agora vamos aplicar tudo ao KODA.

A pergunta nao e "quantos agentes podemos criar?".

A pergunta correta e "quais responsabilidades precisam de ownership separado?".

Para uma jornada de compra completa, podemos decompor em cinco agentes de dominio.

Eles ainda podem usar internamente Planner, Generator e Evaluator.

Mas, no nivel de customer journey, cada um possui uma parte clara da experiencia.

| Agente | Responsabilidade | Input | Output | Strategy de Coordenacao |
| --- | --- | --- | --- | --- |
| Welcome Agent | Receber cliente, identificar intencao inicial, criar tom de conversa | primeira mensagem, perfil existente | saudacao e pergunta de descoberta | Sequencial |
| Discovery Agent | Coletar objetivo, restricoes, orcamento e preferencias | respostas do cliente, historico | `customer_needs.json` | Sequencial |
| Recommendation Agent | Gerar e comparar opcoes de produto | necessidades, catalogo, estoque | `recommendation_set.json` | Paralelo com avaliacao |
| Order Agent | Montar carrinho, validar preco, cupom, endereco e pagamento | produto escolhido, perfil, endereco | `order_draft.json` | Sequencial |
| Fulfillment Agent | Confirmar entrega, status e pos-venda | pedido pago, estoque, transportadora | `fulfillment_plan.json` | Event-driven |

### Agente 1: Welcome Agent

Responsabilidade: abrir a conversa sem pressa e sem tentar vender cedo demais.

Input:

1. Mensagem inicial do WhatsApp.
2. Nome do cliente quando disponivel.
3. Sinais de cliente recorrente.

Output:

1. Saudacao curta.
2. Identificacao de intencao.
3. Handoff para Discovery Agent.

Coordination strategy: sequencial.

### Agente 2: Discovery Agent

Responsabilidade: transformar conversa aberta em dados estruturados.

Input:

1. Objetivo do cliente.
2. Restricoes alimentares.
3. Orcamento.
4. Preferencias de sabor.
5. Frequencia de treino.

Output:

1. `customer_needs.json`.
2. Lista de dados faltantes.
3. Nivel de confianca.

Coordination strategy: sequencial.

### Agente 3: Recommendation Agent

Responsabilidade: transformar necessidades em recomendacao explicavel.

Input:

1. `customer_needs.json`.
2. `catalog_snapshot.json`.
3. `inventory_snapshot.json`.
4. Promocoes ativas.

Output:

1. `recommendation_set.json`.
2. Justificativa de produto principal.
3. Alternativa segura.
4. Alertas de restricao.

Coordination strategy: paralelo com Evaluator central.

### Agente 4: Order Agent

Responsabilidade: transformar escolha em pedido validado.

Input:

1. Produto escolhido.
2. Endereco.
3. Estoque regional.
4. Preco atual.
5. Cupom ou promocao.

Output:

1. `order_draft.json`.
2. Resumo de pedido.
3. Link de pagamento quando aprovado.

Coordination strategy: sequencial.

### Agente 5: Fulfillment Agent

Responsabilidade: cuidar do que acontece depois da compra.

Input:

1. Pedido pago.
2. Estoque reservado.
3. Transportadora.
4. Preferencias de notificacao.

Output:

1. `fulfillment_plan.json`.
2. Mensagem de confirmacao.
3. Eventos de acompanhamento.

Coordination strategy: event-driven.

Exemplo de `customer_needs.json`:

```json
{
  "schema_version": "1.0",
  "conversation_id": "wa_2026_05_26_marina",
  "captured_by": "discovery_agent",
  "customer_goal": "ganhar massa com controle de peso",
  "budget_brl": 220,
  "restrictions": ["intolerancia_lactose"],
  "preferences": {
    "flavor": "chocolate",
    "avoid": ["estimulantes_noite"],
    "duration_expectation": "aproximadamente_um_mes"
  },
  "confidence": "high",
  "missing_information": ["endereco_para_frete"]
}
```

Exemplo de `recommendation_set.json`:

```json
{
  "schema_version": "1.0",
  "conversation_id": "wa_2026_05_26_marina",
  "captured_by": "recommendation_agent",
  "primary_recommendation": {
    "sku": "WHEY-ISO-CHOC-900",
    "name": "Whey Isolado Chocolate 900g",
    "price_brl": 199.9,
    "why": ["sem lactose", "sabor preferido", "dentro do orcamento", "bom encaixe para meta de proteina"]
  },
  "alternative": {
    "sku": "PROT-VEG-BAUN-750",
    "name": "Proteina Vegetal Baunilha 750g",
    "price_brl": 179.9,
    "why_not_primary": "segura para lactose, mas nao atende preferencia de chocolate"
  },
  "warnings": []
}
```

Exemplo de `order_draft.json`:

```json
{
  "schema_version": "1.0",
  "conversation_id": "wa_2026_05_26_marina",
  "captured_by": "order_agent",
  "items": [
    { "sku": "WHEY-ISO-CHOC-900", "quantity": 1, "unit_price_brl": 199.9 }
  ],
  "shipping": {
    "city": "Sao Paulo",
    "neighborhood": "Pinheiros",
    "estimated_delivery": "2026-05-27"
  },
  "total_brl": 199.9,
  "requires_customer_confirmation": true
}
```

Exemplo de `fulfillment_plan.json`:

```json
{
  "schema_version": "1.0",
  "conversation_id": "wa_2026_05_26_marina",
  "captured_by": "fulfillment_agent",
  "order_id": "ord_78291",
  "payment_status": "paid",
  "delivery_events": [
    { "event": "order_confirmed", "message_at": "2026-05-26T20:42:00-03:00" },
    { "event": "out_for_delivery", "message_at": "2026-05-27T09:00:00-03:00" },
    { "event": "delivered", "message_at": "2026-05-27T18:00:00-03:00" }
  ],
  "post_purchase_note": "perguntar em 14 dias se o produto esta funcionando bem"
}
```

### Conversa End-to-End com Handoffs

```
19:43 Marina: Oi, estou voltando a treinar e queria ajuda para comprar suplemento.
19:43 Welcome Agent: identifica intencao de compra assistida.
19:43 KODA: Oi, Marina. Te ajudo sim. Qual e seu objetivo principal e tem alguma restricao alimentar?

19:44 Marina: Quero ganhar massa, mas sem engordar muito. Tenho intolerancia a lactose.
19:44 Discovery Agent: registra objetivo e restricao critica.
19:44 KODA: Perfeito. Vou evitar produtos com lactose. Voce tem um orcamento para este mes?

19:47 Marina: Tenho ate R$ 220 e prefiro chocolate.
19:47 Discovery Agent: atualiza budget e preferencia.
19:47 Recommendation Agent: inicia busca por produtos sem lactose, chocolate, ate R$ 220.
19:48 KODA: Com esse limite, vou comparar opcoes seguras e te explicar a melhor sem empurrar combo.

19:53 Marina: Eu treino 4 vezes por semana e nao quero algo que atrapalhe meu sono.
19:53 Discovery Agent: registra frequencia e evita estimulantes.
19:54 Recommendation Agent: remove pre-treinos com estimulantes da consideracao atual.

20:01 Marina: Se eu comprar so um produto agora, qual seria melhor?
20:01 Planner: define etapa como recomendacao de produto unico.
20:01 Generator: compara whey isolado e proteina vegetal.
20:01 Evaluator: valida lactose, preco, sabor e duracao.
20:02 KODA: Eu escolheria o Whey Isolado Chocolate agora. Ele fica dentro dos R$ 220, respeita sua intolerancia e combina com seu sabor preferido.

20:09 Marina: Pode confirmar se entrega em Pinheiros?
20:09 Order Agent: solicita frete e estoque regional.
20:10 Evaluator: impede promessa antes de estoque confirmado.
20:10 KODA: Vou confirmar estoque em SP antes de prometer o prazo. Um instante.

20:12 Order Agent: estoque confirmado.
20:12 Fulfillment Agent: calcula previsao de entrega para dia seguinte.
20:13 KODA: Estoque confirmado em SP. Entrega estimada para amanha em Pinheiros. Total R$ 199,90. Posso gerar o link de pagamento?

20:14 Marina: Pode.
20:14 Order Agent: gera pedido pendente de pagamento.
20:14 Evaluator: valida resumo antes do link.
20:15 KODA: Aqui esta o resumo: Whey Isolado Chocolate 900g, sem lactose, R$ 199,90, entrega estimada para amanha em Pinheiros. Vou te enviar o link seguro de pagamento.

20:18 Marina: Paguei.
20:18 Fulfillment Agent: recebe evento payment.approved.
20:18 KODA: Pagamento aprovado. Pedido confirmado. Amanha te aviso quando sair para entrega.
```

Snapshot `handoff_discovery.json` durante a jornada:

```json
{
  "stage": "discovery_complete",
  "next_agent": "recommendation_agent",
  "handoff_reason": "necessidades suficientes para recomendar produto unico",
  "customer_state": {
    "goal": "ganho_de_massa",
    "budget_brl": 220,
    "restrictions": ["intolerancia_lactose"],
    "preferred_flavor": "chocolate",
    "avoid": ["estimulantes_noite"]
  }
}
```

Snapshot `handoff_recommendation.json` durante a jornada:

```json
{
  "stage": "recommendation_approved",
  "next_agent": "order_agent",
  "handoff_reason": "cliente aceitou produto principal",
  "selected_product": {
    "sku": "WHEY-ISO-CHOC-900",
    "price_brl": 199.9,
    "safety_flags": ["lactose_free"]
  },
  "evaluator_decision": {
    "status": "approved",
    "notes": ["orcamento respeitado", "preferencia de sabor respeitada", "sem promessa de estoque antes da confirmacao"]
  }
}
```

Snapshot `handoff_payment.json` durante a jornada:

```json
{
  "stage": "payment_approved",
  "next_agent": "fulfillment_agent",
  "order": {
    "order_id": "ord_78291",
    "payment_status": "paid",
    "delivery_city": "Sao Paulo",
    "delivery_neighborhood": "Pinheiros",
    "estimated_delivery": "2026-05-27"
  },
  "customer_message_needed": "confirmacao curta e proximo update"
}
```

O que esta arquitetura evita:

1. O Welcome Agent nao tenta recomendar cedo demais.
2. O Discovery Agent nao inventa produto.
3. O Recommendation Agent nao ignora restricao alimentar.
4. O Order Agent nao promete entrega antes de validar estoque.
5. O Fulfillment Agent nao depende da memoria do chat para saber o que foi comprado.
6. O Evaluator cria checkpoints entre decisoes sensiveis.
7. O state store permite replay se o cliente reclamar.

```
01_inbound_message.json
    ↓ Welcome Agent
02_welcome_response.json
    ↓ Discovery Agent
03_customer_needs.json
    ↓ Recommendation Agent
04_recommendation_set.json
    ↓ Evaluator
05_recommendation_evaluation.json
    ↓ Order Agent
06_order_draft.json
    ↓ Evaluator
07_order_evaluation.json
    ↓ Payment Event
08_payment_approved.json
    ↓ Fulfillment Agent
09_fulfillment_plan.json
```

Esse fluxo parece mais longo que um agente unico.

Mas ele reduz retrabalho.

Ele reduz pedidos errados.

Ele reduz respostas contraditorias.

E, principalmente, permite que a equipe entenda exatamente o que aconteceu.

---

## ⚠️ Quando NAO Usar Multi-Agente

Multi-agent systems nao sao resposta para tudo.

A arquitetura adiciona overhead.

Ela cria mais arquivos, mais contratos, mais pontos de falha e mais latencia.

Use quando o beneficio supera esse custo.

Nao use multi-agente quando:

1. A tarefa cabe em uma resposta simples.
2. O erro tem baixo custo.
3. Nao ha criterios claros de avaliacao.
4. O time ainda nao sabe manter state persistence basica.
5. A latencia precisa ser minima e a resposta nao exige verificacao.
6. O fluxo ainda muda todos os dias e contratos seriam desperdicio.
7. O problema real e catalogo ruim, nao arquitetura.

Exemplos em KODA onde um agente unico basta:

1. "Qual o horario de atendimento?"
2. "Meu pedido ja foi enviado?" quando o status vem direto do sistema.
3. "Vocês entregam em Sao Paulo?"
4. "Como falo com suporte humano?"

Exemplos onde multi-agente faz sentido:

1. Recomendacao com alergias, orcamento e preferencias.
2. Pedido com multiplos produtos, cupom, estoque regional e frete.
3. Jornada que continua depois do pagamento.
4. Recuperacao de carrinho abandonado com historico sensivel.
5. Comparacao de kits com custo por dose e restricoes alimentares.

A regra pratica:

Se voce nao consegue explicar o beneficio de cada agente, ele provavelmente nao deveria existir.

Cada agente precisa ter ownership claro.

Cada handoff precisa ter um contrato.

Cada contrato precisa ser verificavel.

### Sinais de Overengineering

1. Agentes com nomes bonitos, mas responsabilidades sobrepostas.
2. Muitos eventos para uma tarefa que caberia em uma funcao.
3. Evaluator que apenas repete "parece bom".
4. Planner que cria planos genericos sem criterios concretos.
5. State files enormes que ninguem le.
6. Latencia piorando sem aumento mensuravel de qualidade.
7. Debug mais dificil do que antes.

Quando esses sinais aparecem, simplifique.

Multi-agente bom parece inevitavel depois que voce entende o fluxo.

Multi-agente ruim parece teatro.

### Perguntas de Design Antes de Criar Mais Um Agente

1. Qual decisao esse agente possui que nenhum outro agente possui?
2. Qual arquivo de entrada ele le?
3. Qual arquivo de saida ele escreve?
4. Qual criterio permite dizer que ele terminou?
5. Qual falha ele previne?
6. Qual latencia ele adiciona?
7. Qual custo de token budget ele consome?
8. Como o Evaluator verifica seu trabalho?
9. Como o trace mostra sua decisao depois de uma reclamacao?
10. O cliente perceberia piora se esse agente fosse removido?
11. O time consegue explicar seu papel em uma frase?
12. O agente reduz complexidade ou apenas muda complexidade de lugar?
13. Existe state persistence suficiente para ele retomar a tarefa?
14. Existe rubrica concreta para seu output?
15. Ele precisa ser sincrono ou poderia reagir a evento?
16. Ele precisa consultar ferramenta externa?
17. Ele escreve dados sensiveis que exigem cuidado?
18. Ele depende de informacao que pode ficar desatualizada?
19. Ele tem fallback seguro se a avaliacao reprovar?
20. Ele melhora qualidade de forma mensuravel?

---

## 🎯 Key Takeaways

1. Generator/Evaluator do Nivel 2 e o caso de 2 agentes do padrao N-agent.

2. A arquitetura Planner, Generator e Evaluator separa planejamento, execucao e validacao.

3. O Planner reduz ambiguidade antes da geracao, criando etapas e criterios de sucesso.

4. O Generator executa melhor quando recebe uma tarefa pequena e um contrato claro.

5. O Evaluator continua sendo o gatekeeper contra sycophancy, contradicoes e erro factual.

6. File-based coordination com JSON e o caminho mais simples para aprender, auditar e evoluir.

7. Multi-agent systems devem ser usados quando a jornada exige ownership separado, nao porque parecem avancados.

---

## 🚀 Checkpoint: O Que Voce Aprendeu

- [ ] Consigo explicar por que Generator/Evaluator e o caso de 2 agentes do padrao N-agent.

- [ ] Consigo diferenciar Planner, Generator e Evaluator sem misturar responsabilidades.

- [ ] Consigo desenhar o fluxo Planner para Generator para Evaluator com state files.

- [ ] Consigo escolher entre file-based, queue-based e API-based communication.

- [ ] Consigo comparar strategies sequencial, paralelo e event-driven.

- [ ] Consigo decompor uma customer journey do KODA em agentes com input e output claros.

- [ ] Consigo identificar quando multi-agente seria overkill.

- [ ] Consigo escrever um `plan.json` com criterios de sucesso verificaveis.

- [ ] Consigo escrever um `generation.json` com evidencias e suposicoes.

- [ ] Consigo escrever um `evaluation.json` que aprova ou rejeita com feedback especifico.

- [ ] Consigo explicar por que state persistence protege jornadas longas contra context rot.

- [ ] Consigo revisar um trace e descobrir qual agente tomou qual decisao.

---

## 📚 Referencias & Proximas Leituras

- `curriculum/02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md` para revisar a base Generator/Evaluator.

- `curriculum/02-nivel-2-practical-patterns/koda-applications/nivel-2-koda.md` para ver como KODA evolui de padroes praticos para arquitetura.

- `curriculum/03-nivel-3-advanced-architecture/02-state-persistence.md` para aprofundar como estado externo sustenta agentes longos.

- `curriculum/03-nivel-3-advanced-architecture/03-file-based-coordination.md` para estudar contratos por arquivos JSON.

- `curriculum/03-nivel-3-advanced-architecture/05-harness-evolution.md` para entender como o harness cresce sem virar caos.

- `curriculum/04-nivel-4-koda-specific/02-customer-journey-flows.md` para aplicar esses conceitos em jornadas completas do KODA.

- `curriculum/02-nivel-2-practical-patterns/03-rubric-design.md` para fortalecer os criterios usados pelo Evaluator.

- Papers e posts sobre multi-agent orchestration em LLM applications.

- Documentacao de Redis Streams quando o fluxo exigir filas leves.

- Documentacao de RabbitMQ quando o fluxo exigir entrega duravel e backpressure.

- Guias de REST e gRPC para contratos entre servicos internos.

---

## 💭 Reflexao Final

Um bom sistema multi-agente nao tenta parecer inteligente.

Ele tenta ser confiavel.

Essa diferenca muda a arquitetura.

Quando Marina pediu ajuda, ela nao queria saber quantos agentes existiam por tras do KODA.

Ela queria ser ouvida.

Queria que sua intolerancia fosse respeitada.

Queria que o orcamento importasse.

Queria uma recomendacao clara, segura e humana.

A melhor arquitetura e aquela que torna isso repetivel.

Planner, Generator e Evaluator nao sao personagens decorativos.

Sao uma forma de dividir responsabilidade para proteger a experiencia do cliente.

O Planner da direcao.

O Generator cria valor.

O Evaluator protege qualidade.

O state store guarda memoria.

O harness mantem todos honestos.

Quando esses elementos trabalham juntos, KODA deixa de ser apenas um chatbot bom em respostas curtas.

Ele se torna um sistema capaz de acompanhar uma pessoa por uma jornada inteira.

Esse e o salto do Nivel 3.

Nao e adicionar agentes por ambicao tecnica.

E criar uma arquitetura onde cada decisao importante tem dono, evidencia e validacao.

Esse e o tipo de sistema que clientes sentem, mesmo sem ver.

---

## 📋 Metadata

| Campo | Valor |
| --- | --- |
| Arquivo | `curriculum/03-nivel-3-advanced-architecture/01-multi-agent-systems.md` |
| Nivel | 3 - Arquitetura Avancada |
| Tempo | 120 minutos |
| Status | Completo |
| Proximo | `curriculum/03-nivel-3-advanced-architecture/02-state-persistence.md` |
| Atualizado | Maio 2026 |

