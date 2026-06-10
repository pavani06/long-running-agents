---
title: "Sistemas Multi-Agente para Arquiteturas Confiáveis"
type: curriculum-lesson
nivel: 3
aliases: []
tags: [curriculo-conteudo, nivel-3, arquitetura-avancada, sistemas-multiagente, planejamento-geracao-validacao, decomposicao-de-jornada, orquestracao-de-agentes, ownership-de-responsabilidades, coordenacao-sequencial, coordenacao-paralela, orientado-a-eventos, canais-de-comunicacao, auditabilidade]
relates-to: ["[[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]", "[[docs/canonical/multi-model-evaluation-council|Multi-Model Evaluation Council]]", "[[curriculum/05-core-concepts/07-multi-agent-coordination|Multi-Agent Coordination Concept]]"]
last_updated: 2026-06-10
---
# 🔗 Sistemas Multi-Agente para Arquiteturas Confiáveis
## Como Planner, Generator e Evaluator Transformam Jornadas Longas em Fluxos Auditáveis

**Tempo Estimado:** 120 minutos  
**Nível:** 3 - Arquitetura Avançada  
**Pré-requisito:** Ter completado `02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md`  
**Status:** 🟢 CRITICO - Base para decompor jornadas complexas do KODA  
**Data de Criação:** Maio 2026

---

## 📖 Prólogo: A Noite em que Um Agente Sozinho Quase Perdeu a Venda

**Cenário Real: quinta-feira, 19h42.**

A academia do bairro tinha acabado de fechar.

Marina saiu cansada, com a garrafa vazia na mochila e uma decisão nova na cabeça: ela queria voltar a treinar com consistência.

Ela tinha comprado suplementos antes, mas sempre se sentia perdida.

Whey concentrado, whey isolado, creatina, pré-treino, hipercalórico, tabela nutricional, promessa de ganho rápido.

Tudo parecia feito para quem já entendia do assunto.

Naquela noite, uma amiga indicou o WhatsApp do KODA.

Marina abriu a conversa.

```
19:43 Marina: Oi, estou voltando a treinar e queria ajuda para comprar suplemento.
19:43 KODA: Oi, Marina. Me conta seu objetivo principal e qualquer restricao alimentar.
19:44 Marina: Quero ganhar massa, mas sem engordar muito. Tenho intolerancia a lactose.
```

A primeira resposta foi boa.

O agente único entendeu o objetivo, perguntou contexto e buscou produtos.

Por alguns minutos, tudo parecia simples.

```
19:46 KODA: Para ganho de massa com intolerancia a lactose, posso olhar whey isolado sem lactose, proteina vegetal e creatina.
19:47 Marina: Tenho ate R$ 220 este mes. Quero algo que dure pelo menos um mes.
19:48 KODA: Entendido. Vou priorizar custo por dose, ausencia de lactose e produtos com boa avaliacao.
```

Marina ficou aliviada.

Ela não queria falar com um vendedor que empurrasse o produto mais caro.

Queria alguém que acompanhasse a situação dela.

**Minuto 10:** a conversa cresceu.

```
19:53 Marina: Eu treino 4 vezes por semana.
19:53 Marina: Tambem tomo cafe a tarde, entao nao quero algo que atrapalhe meu sono.
19:54 Marina: Tem alguma coisa com chocolate?
19:55 Marina: E se eu comprar creatina junto, fica melhor?
```

O agente único tentou responder tudo de uma vez.

Ele misturou descoberta de necessidade, busca de catálogo, comparação de preço, explicação nutricional e preparação de pedido.

A resposta ficou longa.

Parecia completa, mas escondia confusão.

```
19:56 KODA: Recomendo Whey Isolado Chocolate 900g, Creatina Monohidratada 300g e um pre-treino leve sem cafeina.
19:57 Marina: Mas eu falei que tenho R$ 220. Quanto daria tudo?
19:58 KODA: O combo fica R$ 287,90.
19:58 Marina: Entao nao cabe no meu orcamento.
```

A primeira rachadura apareceu.

O agente tinha registrado o orçamento.

Mesmo assim, montou um combo acima do limite.

Ele estava tentando ser útil, mas confundiu a meta principal.

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

Mas a ficha técnica do produto dizia 24 doses.

O agente único não percebeu.

Ele gerou a recomendação e validou a própria frase com excesso de confiança.

**Minuto 26:** a conversa entrou no território que quebra agentes simples.

```
20:09 Marina: Minha amiga falou de uma proteina vegetal de baunilha. Ela e melhor?
20:10 KODA: Sim, pode ser melhor para intolerancia a lactose.
20:10 Marina: Mas eu prefiro chocolate.
20:11 KODA: Temos vegetal baunilha com 20% de desconto.
20:11 Marina: Eu perguntei se e melhor, nao se tem desconto.
```

Agora o problema não era só preço.

Era atenção.

O agente estava pulando entre critérios: sabor, desconto, restrição alimentar, duração, estoque e objetivo de treino.

Tudo dentro da mesma context window.

Tudo dentro do mesmo processo mental.

**Minuto 32:** Marina quase desistiu.

```
20:15 Marina: KODA, estou confusa. Qual voce compraria no meu lugar?
20:16 KODA: Eu compraria o Whey Concentrado Chocolate, melhor custo-beneficio.
20:16 Marina: Mas eu tenho intolerancia a lactose.
20:17 KODA: Desculpe, voce tem razao. Vou corrigir.
```

Esse tipo de erro fere a confiança.

Não é apenas uma resposta errada.

E a sensação de que o assistente não estava realmente ouvindo.

**Minuto 38:** a equipe KODA, observando o trace, percebeu o padrão.

O agente único tinha responsabilidades demais:

1. Entender a jornada emocional da cliente.
2. Coletar restrições alimentares.
3. Consultar catálogo e estoque.
4. Comparar preço por dose.
5. Explicar trade-offs de produto.
6. Preparar carrinho.
7. Validar se cada etapa respeitava o orçamento.
8. Manter tom humano no WhatsApp.

Nenhuma dessas tarefas é impossível.

O problema é pedir que uma única chamada, um único agente, uma única trilha de raciocínio faça tudo ao mesmo tempo.

A arquitetura estava criando o erro.

**Minuto 44:** a equipe simulou outra abordagem.

Em vez de um agente único, a conversa passaria por três papéis internos.

O Planner decomporia a jornada: descobrir necessidade, filtrar restrições, comparar opções, montar pedido.

O Generator executaria cada etapa planejada, criando respostas e artefatos estruturados.

O Evaluator validaria se a resposta respeitava fatos, orçamento, restrições e tom.

Marina continuaria vendo um único KODA no WhatsApp.

Por trás da interface, porém, haveria uma pequena equipe.

**Minuto 51:** a mesma conversa foi reprocessada.

```
20:26 Planner: Etapa atual e comparacao de duas opcoes sem lactose dentro de R$ 220.
20:26 Generator: Criando resposta com Whey Isolado Chocolate e Proteina Vegetal Baunilha.
20:26 Evaluator: Verificando lactose, preco, doses, preferencia por chocolate e clareza.
20:27 KODA: Marina, no seu caso eu escolheria o Whey Isolado Chocolate agora. Ele respeita sua intolerancia, fica dentro dos R$ 220 e combina com sua preferencia de sabor. A proteina vegetal e segura tambem, mas perde no sabor que voce pediu.
```

A diferença foi imediata.

O KODA não ficou mais frio.

Não virou um fluxo robótico.

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

Não foi magia de modelo.

Foi decomposição, state persistence e avaliação independente.

Este módulo ensina exatamente isso.

Ao final, você vai enxergar multi-agent systems não como moda, mas como uma forma concreta de proteger jornadas longas contra confusão, esquecimento e auto-aprovação.

---

## 🔗 Conexão com Nível 2

No Nível 2, você aprendeu o padrão Generator/Evaluator em `02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md`.

A ideia central era simples: separar quem cria de quem avalia.

O Generator produz uma solução.

O Evaluator valida a solução contra uma rubrica.

Essa separacao reduz sycophancy, aumenta auditabilidade e cria um checkpoint antes da resposta chegar ao cliente.

Multi-agent systems pegam essa mesma ideia e generalizam.

Generator/Evaluator e o caso de 2 agentes do padrão N-agent.

| Nível | Arquitetura | Pergunta Principal | Resultado |
| --- | --- | --- | --- |
| Nível 2 | Generator + Evaluator | A resposta gerada está correta? | Qualidade por verificação independente |
| Nível 3 | Planner + Generator + Evaluator | Qual trabalho precisa ser feito, como executar e como validar? | Qualidade por decomposição completa |
| Nível 3 expandido | N agentes especializados | Qual parte da jornada cada agente deve possuir? | Escala para customer journeys longos |

A mudança do Nível 2 para o Nível 3 não contradiz o que você aprendeu.

Ela preserva o Generator/Evaluator e adiciona uma responsabilidade antes da geração: planejamento explícito.

Sem Planner, o Generator ainda precisa decidir o que fazer.

Com Planner, o Generator recebe uma tarefa menor, mais clara e mais fácil de executar.

No Nível 2, o fluxo era:

```
Cliente e contexto
    ↓
Generator
    ↓
Evaluator
    ↓
Resposta aprovada
```

No Nível 3, o fluxo passa a ser:

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

A diferença parece pequena.

Na prática, ela muda tudo.

O Planner impede que o Generator tente resolver uma jornada inteira sem mapa.

Ele transforma uma conversa baguncada em uma sequência de etapas observaveis.

O Evaluator continua sendo o gatekeeper aprendido no Nível 2.

Agora ele também valida se o Generator cumpriu o plano, não apenas se a resposta final parece boa.

Isso cria três camadas de segurança:

1. O Planner reduz ambiguidade.
2. O Generator reduz escopo por execução focada.
3. O Evaluator reduz erro por verificação independente.

Pense assim: Generator/Evaluator era uma dupla de escritor e editor.

Planner, Generator e Evaluator viram editor-chefe, escritor e revisor técnico.

O editor-chefe define a pauta.

O escritor escreve.

O revisor técnico protege o leitor.

Para o KODA, isso significa que uma pergunta como "qual suplemento eu compro?" deixa de ser uma resposta única.

Ela vira uma pequena jornada:

1. Identificar objetivo.
2. Identificar restrições.
3. Consultar catálogo.
4. Comparar opções.
5. Explicar recomendação.
6. Validar pedido.
7. Preparar checkout.

Cada etapa pode ter estado, output e critérios proprios.

Essa é a ponte entre o Nível 2 e o Nível 3.

---

## 🏗️ Arquitetura Multi-Agente: Planner, Generator, Evaluator

Uma arquitetura multi-agente não significa colocar vários modelos conversando sem controle.

Essa é a versão caótica.

A versão profissional é um harness que define papéis, contratos, arquivos de estado e critérios de passagem.

Neste módulo, vamos usar a arquitetura base de 3 agentes.

Ela é simples o suficiente para implementar.

Também é forte o suficiente para sustentar jornadas reais do KODA.

### Papel 1: Planner

O Planner é responsável por decompor a tarefa, criar plano operacional e definir critérios de sucesso.

Responsabilidades do Planner:

1. Ler a conversa atual e o state persistido.
2. Identificar o objetivo imediato do cliente.
3. Separar a jornada em etapas pequenas.
4. Definir quais dados faltam.
5. Escolher a próxima ação segura.
6. Registrar critérios de sucesso para o Generator.
7. Registrar critérios de validação para o Evaluator.

### Papel 2: Generator

O Generator é responsável por executar cada etapa planejada sem aprovar o próprio trabalho.

Responsabilidades do Generator:

1. Ler o plano do Planner.
2. Executar os passos designados.
3. Consultar ferramentas permitidas, como catálogo, estoque ou calculadora de frete.
4. Produzir output estruturado.
5. Registrar suposicoes explicitamente.
6. Não aprovar o próprio trabalho.
7. Salvar resultado para o Evaluator.

### Papel 3: Evaluator

O Evaluator é responsável por validar resultado, proteger cliente e decidir aprovação ou revisão.

Responsabilidades do Evaluator:

1. Ler o plano original.
2. Ler o output do Generator.
3. Validar cada criterio da rubrica.
4. Detectar contradicoes com o state persistido.
5. Verificar se ha afirmacoes sem evidência.
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
| Entrada | mensagem do WhatsApp, perfil, histórico resumido | evento de conversa | harness | `conversation_event.json` |
| Planejamento | evento, state, catalog snapshot | plano com etapas e rubrica | Planner | `plan.json` |
| Geracao | plano, ferramentas, dados de catálogo | resposta candidata e evidências | Generator | `generation.json` |
| Avaliação | plano, geração, state | decisão e feedback | Evaluator | `evaluation.json` |
| Entrega | resposta aprovada | mensagem final | harness | `delivery.json` |

Um agente único pode responder bem em conversas curtas.

Ele falha quando a jornada combina muitos objetivos ao mesmo tempo.

O problema não é falta de inteligência.

O problema é acoplamento de responsabilidades.

Quando o mesmo agente planeja, executa e valida, três riscos aparecem:

1. O plano fica implícito e difícil de debugar.
2. A execução muda o plano sem avisar.
3. A avaliação confirma a própria resposta por sycophancy.

Três agentes reduzem esses riscos por design.

O Planner cria um mapa antes da ação.

O Generator segue o mapa e deixa rastros.

O Evaluator compara resultado contra mapa e fatos.

Essa estrutura também melhora token budget.

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

Esse pseudocodigo mostra o ponto central: agentes não se comunicam por intuicao.

Eles se comunicam por artefatos.

Os arquivos criam memória externa, audit trail e pontos de retomada.

---

## 📡 Canais de Comunicacao entre Agentes

Agentes precisam trocar informação.

A pergunta arquitetural é: por qual canal?

Existem três familias principais para KODA: file-based, message queues e API-based.

A recomendação para este currículo é começar com file-based coordination.

Arquivos JSON em disco são simples, auditáveis e bons para aprendizado.

Eles também são uma excelente base para evoluir depois para Redis, RabbitMQ, REST ou gRPC.

| Canal | Latência | Confiabilidade | Complexidade | Quando Usar |
| --- | --- | --- | --- | --- |
| File-based JSON | Baixa a media | Alta quando escrito de forma atômica | Baixa | Prototipos, curriculum, traces, workflows auditáveis, KODA em fase de desenho |
| Message queues Redis | Muito baixa | Media a alta com retries e ack | Media | Eventos frequentes, multiplos workers, processamento paralelo leve |
| Message queues RabbitMQ | Baixa | Alta com filas duraveis | Alta | Workflows criticos, backpressure, entrega garantida, operacao mais madura |
| API-based REST | Media | Alta se houver idempotencia | Media | Servicos separados, integracao simples entre times, chamadas síncrona |
| API-based gRPC | Baixa | Alta com contratos fortes | Alta | Baixa latência, alto volume, schemas rigidos, comunicação interna |

### Canal 1: File-based Coordination

File-based coordination usa arquivos como contrato entre agentes.

O Planner escreve `plan.json`.

O Generator le `plan.json` e escreve `generation.json`.

O Evaluator le os dois e escreve `evaluation.json`.

Vantagens:

1. Fácil de entender.
2. Fácil de versionar em exemplos.
3. Fácil de debugar com trace reading.
4. Funciona bem em tarefas longas.
5. Cria state persistence naturalmente.

Cuidados:

1. Escrever de forma atômica para evitar arquivo parcial.
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

Message queues entram quando você precisa de paralelismo real ou alto volume.

Redis pode ser suficiente quando a prioridade e velocidade e simplicidade operacional.

RabbitMQ e melhor quando você precisa de roteamento, durabilidade e controle fino de entrega.

Em KODA, filas podem aparecer quando varios Generators trabalham em paralelo:

1. Generator de recomendação.
2. Generator de precificacao.
3. Generator de frete.
4. Generator de risco de restrição alimentar.

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

Ela combina bem quando cada agente é um serviço separado com deploy próprio.

REST e mais simples para times diferentes entenderem.

gRPC e melhor para contratos fortes e baixa latência.

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

Use file-based quando o time ainda está aprendendo o domínio.

Use queues quando o gargalo é throughput ou paralelismo.

Use APIs quando a fronteira entre agentes também é fronteira entre serviços.

Para KODA, uma evolução saudável costuma ser:

1. Começar com arquivos JSON para desenhar contratos.
2. Validar trace reading e rúbricas.
3. Mover partes quentes para filas quando houver volume.
4. Expor APIs quando houver times ou serviços independentes.

---

## 🎯 Estratégias de Coordenação

Canais dizem por onde agentes se comunicam.

Estratégias de coordenação dizem quando e em que ordem eles trabalham.

As três estratégias principais são sequencial, paralelo e event-driven.

| Estratégia | Fluxo | Vantagens | Desvantagens | Caso de Uso KODA |
| --- | --- | --- | --- | --- |
| Sequencial | Planner para Generator para Evaluator | Simples, auditável, fácil de debugar | Menor velocidade, cada etapa espera a anterior | Recomendação com risco alimentar ou fechamento de pedido |
| Paralelo | Planner cria subtarefas e vários Generators executam ao mesmo tempo | Reduz latência, explora alternativas, escala comparações | Exige agregação, risco de resultados inconsistentes | Comparar produtos, frete, estoque e promoções em paralelo |
| Event-driven | Agentes reagem a mudanças no state | Bom para jornadas longas, desacopla componentes, permite retomada | Mais difícil de observar, precisa governança de eventos | Atualização de estoque, abandono de carrinho, pagamento aprovado |

### Estratégia 1: Sequencial

Sequencial define uma forma específica de coordenar agentes em KODA.

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
3. A resposta depende de uma ordem lógica.
4. O time ainda está estabilizando os contratos.

### Estratégia 2: Paralelo

Paralelo define uma forma específica de coordenar agentes em KODA.

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

1. As subtarefas são independentes.
2. Latência importa.
3. Você precisa comparar alternativas.
4. Existe um bom Evaluator para reconciliar resultados.

### Estratégia 3: Event-driven

Event-driven define uma forma específica de coordenar agentes em KODA.

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
4. Você precisa retomar workflows sem depender da context window.

Regras praticas de coordenação:

1. Comece sequencial para aprender os contratos.
2. Paralelize apenas tarefas independentes.
3. Use event-driven para jornadas que continuam fora do turno atual.
4. Nunca deixe dois agentes escreverem o mesmo campo sem regra de ownership.
5. Sempre registre quem escreveu cada decisão.
6. Sempre permita replay do trace.
7. Trate state como fonte de verdade, não a memória temporaria do modelo.

---

## 🎓 Aplicação KODA: Decomposição do Customer Journey em Agentes

Agora vamos aplicar tudo ao KODA.

A pergunta não é "quantos agentes podemos criar?".

A pergunta correta é "quais responsabilidades precisam de ownership separado?".

Para uma jornada de compra completa, podemos decompor em cinco agentes de domínio.

Eles ainda podem usar internamente Planner, Generator e Evaluator.

Mas, no nível de customer journey, cada um possui uma parte clara da experiência.

| Agente | Responsabilidade | Input | Output | Estratégia de Coordenação |
| --- | --- | --- | --- | --- |
| Welcome Agent | Receber cliente, identificar intenção inicial, criar tom de conversa | primeira mensagem, perfil existente | saudação e pergunta de descoberta | Sequencial |
| Discovery Agent | Coletar objetivo, restrições, orçamento e preferências | respostas do cliente, histórico | `customer_needs.json` | Sequencial |
| Recommendation Agent | Gerar e comparar opções de produto | necessidades, catálogo, estoque | `recommendation_set.json` | Paralelo com avaliação |
| Order Agent | Montar carrinho, validar preço, cupom, endereço e pagamento | produto escolhido, perfil, endereço | `order_draft.json` | Sequencial |
| Fulfillment Agent | Confirmar entrega, status e pos-venda | pedido pago, estoque, transportadora | `fulfillment_plan.json` | Event-driven |

### Agente 1: Welcome Agent

Responsabilidade: abrir a conversa sem pressa e sem tentar vender cedo demais.

Input:

1. Mensagem inicial do WhatsApp.
2. Nome do cliente quando disponível.
3. Sinais de cliente recorrente.

Output:

1. Saudacao curta.
2. Identificação de intenção.
3. Handoff para Discovery Agent.

Coordination strategy: sequencial.

### Agente 2: Discovery Agent

Responsabilidade: transformar conversa aberta em dados estruturados.

Input:

1. Objetivo do cliente.
2. Restrições alimentares.
3. Orçamento.
4. Preferencias de sabor.
5. Frequencia de treino.

Output:

1. `customer_needs.json`.
2. Lista de dados faltantes.
3. Nível de confiança.

Coordination strategy: sequencial.

### Agente 3: Recommendation Agent

Responsabilidade: transformar necessidades em recomendação explicavel.

Input:

1. `customer_needs.json`.
2. `catalog_snapshot.json`.
3. `inventory_snapshot.json`.
4. Promocoes ativas.

Output:

1. `recommendation_set.json`.
2. Justificativa de produto principal.
3. Alternativa segura.
4. Alertas de restrição.

Coordination strategy: paralelo com Evaluator central.

### Agente 4: Order Agent

Responsabilidade: transformar escolha em pedido validado.

Input:

1. Produto escolhido.
2. Endereco.
3. Estoque regional.
4. Preço atual.
5. Cupom ou promoção.

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
2. Mensagem de confirmação.
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

O que está arquitetura evita:

1. O Welcome Agent não tenta recomendar cedo demais.
2. O Discovery Agent não inventa produto.
3. O Recommendation Agent não ignora restrição alimentar.
4. O Order Agent não promete entrega antes de validar estoque.
5. O Fulfillment Agent não depende da memória do chat para saber o que foi comprado.
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

Esse fluxo parece mais longo que um agente único.

Mas ele reduz retrabalho.

Ele reduz pedidos errados.

Ele reduz respostas contraditorias.

E, principalmente, permite que a equipe entenda exatamente o que aconteceu.

---

## ⚠️ Quando NÃO Usar Multi-Agente

Multi-agent systems não são resposta para tudo.

A arquitetura adiciona overhead.

Ela cria mais arquivos, mais contratos, mais pontos de falha e mais latência.

Use quando o benefício supera esse custo.

Não use multi-agente quando:

1. A tarefa cabe em uma resposta simples.
2. O erro tem baixo custo.
3. Não há critérios claros de avaliação.
4. O time ainda não sabe manter state persistence básica.
5. A latência precisa ser mínima e a resposta não exige verificação.
6. O fluxo ainda muda todos os dias e contratos seriam desperdício.
7. O problema real é catálogo ruim, não arquitetura.

Exemplos em KODA onde um agente único basta:

1. "Qual o horario de atendimento?"
2. "Meu pedido já foi enviado?" quando o status vem direto do sistema.
3. "Vocês entregam em São Paulo?"
4. "Como falo com suporte humano?"

Exemplos onde multi-agente faz sentido:

1. Recomendação com alergias, orçamento e preferências.
2. Pedido com múltiplos produtos, cupom, estoque regional e frete.
3. Jornada que continua depois do pagamento.
4. Recuperação de carrinho abandonado com histórico sensível.
5. Comparação de kits com custo por dose e restrições alimentares.

A regra prática:

Se você não consegue explicar o benefício de cada agente, ele provavelmente não deveria existir.

Cada agente precisa ter ownership claro.

Cada handoff precisa ter um contrato.

Cada contrato precisa ser verificável.

### Sinais de Overengineering

1. Agentes com nomes bonitos, mas responsabilidades sobrepostas.
2. Muitos eventos para uma tarefa que caberia em uma função.
3. Evaluator que apenas repete "parece bom".
4. Planner que cria planos genericos sem critérios concretos.
5. State files enormes que ninguem le.
6. Latência piorando sem aumento mensuravel de qualidade.
7. Debug mais dificil do que antes.

Quando esses sinais aparecem, simplifique.

Multi-agente bom parece inevitável depois que você entende o fluxo.

Multi-agente ruim parece teatro.

### Perguntas de Design Antes de Criar Mais Um Agente

1. Qual decisão esse agente possui que nenhum outro agente possui?
2. Qual arquivo de entrada ele le?
3. Qual arquivo de saida ele escreve?
4. Qual criterio permite dizer que ele terminou?
5. Qual falha ele previne?
6. Qual latência ele adiciona?
7. Qual custo de token budget ele consome?
8. Como o Evaluator verifica seu trabalho?
9. Como o trace mostra sua decisão depois de uma reclamacao?
10. O cliente perceberia piora se esse agente fosse removido?
11. O time consegue explicar seu papel em uma frase?
12. O agente reduz complexidade ou apenas muda complexidade de lugar?
13. Existe state persistence suficiente para ele retomar a tarefa?
14. Existe rubrica concreta para seu output?
15. Ele precisa ser síncrono ou poderia reagir a evento?
16. Ele precisa consultar ferramenta externa?
17. Ele escreve dados sensiveis que exigem cuidado?
18. Ele depende de informação que pode ficar desatualizada?
19. Ele tem fallback seguro se a avaliação reprovar?
20. Ele melhora qualidade de forma mensuravel?

---

## 🎯 Key Takeaways

1. Generator/Evaluator do Nível 2 e o caso de 2 agentes do padrão N-agent.

2. A arquitetura Planner, Generator e Evaluator separa planejamento, execução e validação.

3. O Planner reduz ambiguidade antes da geração, criando etapas e critérios de sucesso.

4. O Generator executa melhor quando recebe uma tarefa pequena e um contrato claro.

5. O Evaluator continua sendo o gatekeeper contra sycophancy, contradições e erro factual.

6. File-based coordination com JSON é o caminho mais simples para aprender, auditar e evoluir.

7. Multi-agent systems devem ser usados quando a jornada exige ownership separado, não porque parecem avançados.

---

## 🚀 Checkpoint: O Que Você Aprendeu

- [ ] Consigo explicar por que Generator/Evaluator e o caso de 2 agentes do padrão N-agent.

- [ ] Consigo diferenciar Planner, Generator e Evaluator sem misturar responsabilidades.

- [ ] Consigo desenhar o fluxo Planner para Generator para Evaluator com state files.

- [ ] Consigo escolher entre file-based, queue-based e API-based communication.

- [ ] Consigo comparar estratégias sequencial, paralelo e event-driven.

- [ ] Consigo decompor uma customer journey do KODA em agentes com input e output claros.

- [ ] Consigo identificar quando multi-agente seria overkill.

- [ ] Consigo escrever um `plan.json` com critérios de sucesso verificáveis.

- [ ] Consigo escrever um `generation.json` com evidências e suposições.

- [ ] Consigo escrever um `evaluation.json` que aprova ou rejeita com feedback específico.

- [ ] Consigo explicar por que state persistence protege jornadas longas contra context rot.

- [ ] Consigo revisar um trace e descobrir qual agente tomou qual decisão.

---

## 📚 Referências & Próximas Leituras

- `curriculum/02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md` para revisar a base Generator/Evaluator.

- `curriculum/02-nivel-2-practical-patterns/koda-applications/nivel-2-koda.md` para ver como KODA evolui de padrões práticos para arquitetura.

- `curriculum/03-nivel-3-advanced-architecture/02-state-persistence.md` para aprofundar como estado externo sustenta agentes longos.

- `curriculum/03-nivel-3-advanced-architecture/03-file-based-coordination.md` para estudar contratos por arquivos JSON.

- `curriculum/03-nivel-3-advanced-architecture/05-harness-evolution.md` para entender como o harness cresce sem virar caos.

- `curriculum/04-nivel-4-koda-specific/02-customer-journey-flows.md` para aplicar esses conceitos em jornadas completas do KODA.

- `curriculum/02-nivel-2-practical-patterns/03-rubric-design.md` para fortalecer os critérios usados pelo Evaluator.

- Papers e posts sobre multi-agent orchestration em LLM applications.

- Documentação de Redis Streams quando o fluxo exigir filas leves.

- Documentação de RabbitMQ quando o fluxo exigir entrega durável e backpressure.

- Guias de REST e gRPC para contratos entre serviços internos.

---

## 💭 Reflexão Final

Um bom sistema multi-agente não tenta parecer inteligente.

Ele tenta ser confiável.

Essa diferença muda a arquitetura.

Quando Marina pediu ajuda, ela não queria saber quantos agentes existiam por trás do KODA.

Ela queria ser ouvida.

Queria que sua intolerância fosse respeitada.

Queria que o orçamento importasse.

Queria uma recomendação clara, segura e humana.

A melhor arquitetura é aquela que torna isso repetível.

Planner, Generator e Evaluator não são personagens decorativos.

São uma forma de dividir responsabilidade para proteger a experiência do cliente.

O Planner dá direção.

O Generator cria valor.

O Evaluator protege qualidade.

O state store guarda memória.

O harness mantém todos honestos.

Quando esses elementos trabalham juntos, KODA deixa de ser apenas um chatbot bom em respostas curtas.

Ele se torna um sistema capaz de acompanhar uma pessoa por uma jornada inteira.

Esse é o salto do Nível 3.

Não é adicionar agentes por ambição técnica.

E criar uma arquitetura onde cada decisão importante tem dono, evidência e validação.

Esse é o tipo de sistema que clientes sentem, mesmo sem ver.

---

## 📋 Metadata

| Campo | Valor |
| --- | --- |
| Arquivo | `curriculum/03-nivel-3-advanced-architecture/01-multi-agent-systems.md` |
| Nível | 3 - Arquitetura Avançada |
| Tempo | 120 minutos |
| Status | Completo |
| Próximo | `curriculum/03-nivel-3-advanced-architecture/02-state-persistence.md` |
| Atualizado | Maio 2026 |
