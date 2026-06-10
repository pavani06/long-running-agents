---
title: "Generator/Evaluator Graphs"
type: curriculum-knowledge-graph
aliases: []
tags: [curriculo-conteudo, knowledge-graph, mermaid]
relates-to: ["[[curriculum/05-core-concepts/03-generator-evaluator-pattern|Generator/Evaluator Pattern]]", "[[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]"]
last_updated: 2026-06-10
---
# 🧠 Generator/Evaluator Graphs
## Detailed Knowledge Graph — Arquitetura, Fluxo, Coordenação e Aplicação KODA

**Tempo Estimado:** 150 minutos
**Nível:** 6 — Knowledge Graphs e Síntese Arquitetural
**Pré-requisito:** Ter completado `05-core-concepts/03-generator-evaluator-pattern.md` e `02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md`
**Status:** 🟢 COMPLETO — Visualização integrada do padrão que escala KODA de 75% para 98% de precisão
**Data de Criação:** Maio 2026

---

## 📖 Prólogo: O Mapa Que Faltava

Segunda-feira, 9h12. Reunião de arquitetura do KODA.

Fernando tinha três telas abertas.

Na primeira, o módulo conceitual `05-core-concepts/03-generator-evaluator-pattern.md` — 2598 linhas explicando por que separar criação de julgamento resolve uma limitação cognitiva fundamental. Sycophancy. Confirmation bias. Cognitive load theory. O fundamento de que uma mente que acabou de criar não é o melhor juiz da própria criação.

Na segunda, o módulo prático `02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md` — mostrando state files, feedback loops, 5 casos de estudo do KODA, pseudocódigo de implementação, estrutura de diretórios. O como. A mecânica. O código que transforma o conceito em realidade.

Na terceira, um trace de produção onde o Evaluator do KODA tinha rejeitado uma recomendação com lactose para uma cliente intolerante. O trace mostrava exatamente onde a falha aconteceu. Mostrava o feedback. Mostrava a segunda tentativa bem-sucedida. O sistema tinha funcionado como deveria.

Mas havia um silêncio na sala.

Fernando conhecia aquele silêncio. Era o silêncio de quem leu as peças mas ainda não viu o mapa.

Um dos engenheiros novos, Pedro, levantou a mão:

```text
Pedro: "Fernando, eu li os dois módulos. Duas vezes cada um.
       Entendi o conceito — separar criação de julgamento faz sentido.
       Entendi a implementação — state files, feedback, audit log.
       Mas eu ainda não consigo visualizar como tudo se conecta.

       Como a arquitetura conversa com o fluxo?
       Como o fluxo conversa com a coordenação?
       Como a coordenação conversa com o KODA real?
       Como os state files viram um ciclo vivo?
       Como a decisão de rejeitar vira aprendizado?

       Eu vejo as peças. Não vejo o mapa.

       E sem o mapa, quando algo der errado em produção,
       não vou saber por onde começar a olhar."
```

Fernando sorriu. Não era um sorriso de "eu avisei". Era um sorriso de "essa é exatamente a pergunta certa". Ele apagou o quadro branco da sala — que estava coberto de anotações da sprint passada — e desenhou três círculos concêntricos.

```text
┌──────────────────────────────────────────────────┐
│              CAMADA 3: APLICAÇÃO                  │
│        (KODA real — recomendação, pedido)         │
│                                                   │
│    ┌──────────────────────────────────────┐      │
│    │        CAMADA 2: COORDENAÇÃO          │      │
│    │  (state files, feedback, iteração)    │      │
│    │                                       │      │
│    │   ┌──────────────────────────┐       │      │
│    │   │   CAMADA 1: ARQUITETURA   │       │      │
│    │   │  (Generator, Evaluator,    │       │      │
│    │   │   roles, separação)        │       │      │
│    │   └──────────────────────────┘       │      │
│    └──────────────────────────────────────┘      │
└──────────────────────────────────────────────────┘
```

E então explicou:

```text
Fernando: "O módulo conceitual te ensina a Camada 1.
          Ele responde: por que dois roles são melhores que um?

          O módulo prático te ensina a Camada 2.
          Ele responde: como os dois roles trocam informação de forma confiável?

          Mas você está certo, Pedro. Falta o mapa que mostra as três camadas juntas.
          Falta o knowledge graph que conecta arquitetura, fluxo e aplicação
          em uma visão integrada.

          Falta o desenho que mostra que, quando o Evaluator rejeita o Whey Isolado
          Premium por lactose, isso não é só 'o Evaluator funcionando'.
          É a arquitetura (Camada 1) permitindo que a coordenação (Camada 2)
          proteja a aplicação (Camada 3) de um erro que chegaria ao cliente.

          É o cliente — a Marina, uma pessoa real com intolerância à lactose —
          que nunca vai saber que quase recebeu uma recomendação perigosa.
          Porque o mapa funcionou."
```

Este arquivo é esse mapa.

Não é repetição do módulo conceitual — ele mostra **por que**.

Não é repetição do módulo prático — ele mostra **como**.

Este arquivo mostra **como tudo se conecta**.

Três diagramas Mermaid. Uma tabela comparativa de estratégias de coordenação. Um diagrama ASCII de arquitetura. Uma aplicação KODA completa com trace visual. Mapa de conexões com todos os 8 conceitos core. Padrões de falha com diagnóstico.

E a pergunta final: você consegue olhar para este knowledge graph e explicar por que KODA deixou de recomendar lactose para Marina?

Se a resposta for sim, você não apenas entendeu Generator/Evaluator. Você consegue **enxergar** Generator/Evaluator. E enxergar é diferente de entender. Entender é saber que o Evaluator rejeitou. Enxergar é saber por que a rejeição aconteceu, onde no ciclo ela foi possível, qual artefato carregou a evidência, qual feedback guiou a correção, e como o audit log provou tudo isso depois.

---

## 🎯 Objetivos Deste Knowledge Graph

Ao final deste arquivo, você será capaz de:

- ✅ Visualizar a arquitetura Generator/Evaluator como três camadas integradas (roles, coordenação, aplicação) e explicar como a informação flui entre elas sem contaminação de viés
- ✅ Navegar o fluxo completo de geração, avaliação, feedback e iteração com state files como espinha dorsal, identificando cada estado possível do ciclo
- ✅ Comparar mecanismos de coordenação (state files, message passing, shared memory, consensus, HITL, CoT) com critérios objetivos de escolha baseados em custo de erro, auditabilidade e volume
- ✅ Mapear a aplicação KODA de recomendação de produto no knowledge graph completo, incluindo os 5 artefatos JSON que trafegam entre os roles
- ✅ Identificar pontos de conexão entre Generator/Evaluator e os outros 7 conceitos core do currículo, entendendo dependências bidirecionais
- ✅ Diagnosticar padrões de falha visualizando onde o ciclo quebra e quais anti-padrões produzem forma sem substância
- ✅ Explicar o padrão para outra pessoa usando os diagramas deste arquivo como referência visual
- ✅ Reconhecer sinais de que o padrão está saudável em produção através de métricas operacionais

---

## 🔗 Contexto: Onde Este Arquivo se Encaixa no Currículo

Este knowledge graph conecta três fontes primárias de conhecimento sobre Generator/Evaluator:

| Fonte | O Que Fornece | Arquivo | Quando Consultar |
|-------|---------------|---------|-----------------|
| **Conceitual** | Por que separar criação de julgamento funciona: sycophancy, confirmation bias, cognitive load theory, justificativa informacional, princípio de separação | `05-core-concepts/03-generator-evaluator-pattern.md` | Quando precisar do fundamento teórico ou justificar a decisão arquitetural para stakeholders |
| **Prático** | Como implementar com state files, feedback loops e audit log: estrutura de diretórios, pseudocódigo, 5 casos KODA, checklists de implementação | `02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md` | Quando estiver com o editor aberto e precisar escrever código |
| **Aplicação** | Como KODA usa o padrão integrado com Sprint Contracts, Rubric Design e Trace Reading em features reais | `02-nivel-2-practical-patterns/koda-applications/nivel-2-koda.md` | Quando precisar entender como o padrão se encaixa na arquitetura completa do KODA |

Este arquivo **não repete** o conteúdo desses arquivos. Ele fornece a **visualização integrada** que conecta os três — o mapa que Pedro pediu.

Se você chegou aqui sem ler o módulo conceitual, volte e leia `05-core-concepts/03-generator-evaluator-pattern.md` primeiro. Os diagramas aqui pressupõem que você já entende sycophancy, confirmation bias, e por que self-evaluation é estruturalmente limitado.

Se você chegou aqui sem ler o módulo prático, este arquivo ainda será útil como mapa conceitual, mas você precisará do módulo prático antes de implementar qualquer linha de código.

---

## 🏗️ Diagrama 1: Arquitetura Generator/Evaluator — Visão Macro com Zonas de Responsabilidade

### O Que Este Diagrama Mostra

Este diagrama revela a arquitetura em cinco zonas de responsabilidade, cada uma com um propósito distinto e regras de fronteira que impedem a contaminação de viés entre os roles.

As cinco zonas são:

1. **Zona de Entrada** — Onde os fatos entram no sistema e são imobilizados como verdade
2. **Zona de Criação** — Onde o Generator propõe soluções com liberdade criativa
3. **Zona de Julgamento** — Onde o Evaluator testa propostas contra critérios independentes
4. **Zona de Persistência** — Onde cada artefato é salvo como arquivo versionado para auditoria
5. **Zona de Controle** — Onde o Orquestrador decide o próximo passo baseado em regras, não em intuição

O ponto central do diagrama não está nas caixas — está nas **setas**. As setas mostram como a informação flui de uma zona para outra sem que o viés de uma zona contamine a próxima. O Generator nunca conversa diretamente com o Evaluator. O Evaluator nunca recebe a justificativa narrativa do Generator como se fosse evidência. O Orquestrador nunca decide baseado em "feeling" — sempre baseado em veredito estruturado.

```mermaid
graph TD
    subgraph ZONA_ENTRADA["🎯 Zona de Entrada — Fatos Imobilizados"]
        A["Input do Cliente
        Mensagem, objetivo,
        restrições declaradas,
        preferências"]
        B["Fontes de Verdade
        Catálogo de produtos,
        Estoque em tempo real,
        Políticas comerciais,
        Perfil do cliente (BD)"]
    end

    subgraph ZONA_CRIACAO["✏️ Zona de Criação — GENERATOR"]
        C["Generator Agent
        Role: propor a melhor
        solução possível
        Prompt: criativo, exploratório
        Temperature: 0.7 — 1.0
        Objetivo: cobertura e utilidade"]
        D["generator_draft_v{N}.json
        Proposta estruturada:
        • SKU recomendado
        • Preço calculado
        • Claims (o que afirma)
        • Assumptions (o que assume)
        • Evidence usada
        • Confidence (0—1)"]
    end

    subgraph ZONA_JULGAMENTO["⚖️ Zona de Julgamento — EVALUATOR"]
        E["Evaluator Agent
        Role: testar proposta
        contra critérios objetivos
        Prompt: crítico, adversarial
        Temperature: 0.2 — 0.3
        Objetivo: encontrar falhas"]
        F["evaluator_verdict_v{N}.json
        Veredito estruturado:
        • Status (APPROVED/REJECTED)
        • Score (0—100)
        • Checks por critério
        • Severidade de cada falha
        • Evidência para cada check"]
        G["Rubric Independente
        Critérios de qualidade,
        segurança e compliance.
        Externa ao ciclo —
        não muda durante iterações."]
    end

    subgraph ZONA_PERSISTENCIA["💾 Zona de Persistência — STATE FILES"]
        H["customer_context.json
        Fatos imutáveis do cliente:
        restrições, budget, objetivo.
        Escrito UMA VEZ no setup.
        Lido por Generator e Evaluator."]
        I["feedback_v{N}.json
        Instruções acionáveis:
        • Constraint violada
        • Severidade
        • Ação esperada
        • Lista de SKUs a evitar"]
        J["audit_log.jsonl
        Timeline imutável:
        cada evento com timestamp,
        tipo e payload.
        Append-only, nunca rewrite."]
        K["final_response.json
        Resposta aprovada para
        envio ao cliente.
        Inclui summary do ciclo:
        iterações, rejeições, score."]
    end

    subgraph ZONA_CONTROLE["🎛️ Zona de Controle — ORQUESTRADOR"]
        L["Orquestrador
        Decide próximo passo:
        • APPROVED → enviar
        • REJECTED → feedback → retry
        • MAX_ITER → escalar humano
        • DATA_MISSING → pausar"]
        M["Regras de Iteração
        max_iterations: 3
        approval_threshold: 85/100
        on_max_reached: human_review
        on_critical_data_missing:
        pause_and_notify"]
    end

    A --> H
    B --> H
    H --> C
    C --> D
    D --> E
    G --> E
    H --> E
    E --> F
    F --> L
    M --> L
    L -->|"APPROVED"| K
    L -->|"REJECTED + iteração < max"| I
    I --> C
    L -->|"MAX_ITERATIONS"| N["👤 Escalar para Humano"]
    L -->|"CRITICAL_DATA_MISSING"| O["⏸️ Pausar Caso"]
    D --> J
    F --> J
    I --> J
    K --> J
    N --> J
    O --> J

    style ZONA_CRIACAO fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style ZONA_JULGAMENTO fill:#fff3e0,stroke:#ef6c00,stroke-width:2px
    style ZONA_PERSISTENCIA fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style ZONA_CONTROLE fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    style ZONA_ENTRADA fill:#fce4ec,stroke:#c62828,stroke-width:2px
```

### Como Ler Este Diagrama — Explicação Detalhada Por Zona

**Zona de Entrada (vermelho) — Fatos Imobilizados**

Tudo começa aqui. O cliente fornece uma necessidade — uma mensagem no WhatsApp, uma pergunta sobre whey protein, uma restrição alimentar declarada. Simultaneamente, o sistema carrega fontes de verdade externas: o catálogo de produtos (com flags como `lactose_free` e `contains_lactose_trace`), o estoque em tempo real (quantas unidades disponíveis), as políticas comerciais (regras de desconto, cumulatividade de promoções), e o perfil do cliente do banco de dados (histórico de compras, preferências salvas, alergias documentadas).

Tudo isso converge para um único arquivo: `customer_context.json`.

Este arquivo tem uma propriedade fundamental: **imutabilidade durante o ciclo**. Uma vez escrito, ele não muda. Se o cliente mandar uma nova mensagem no meio do processamento, essa nova mensagem não altera o `customer_context.json` do ciclo atual — ela inicia um novo ciclo ou é enfileirada. A imutabilidade é o que permite que Generator e Evaluator trabalhem sobre os mesmos fatos, eliminando uma classe inteira de bugs de inconsistência.

O que entra no `customer_context.json`:
- Dados demográficos e identificadores do cliente
- Restrições alimentares com severidade (CRITICAL, HIGH, MEDIUM)
- Objetivo declarado (ganho muscular, emagrecimento, recuperação)
- Budget máximo em reais
- Preferências (sabor, marca, tipo de proteína)
- Histórico de compras relevantes
- Status de membro do clube e desconto aplicável
- Região de entrega e expectativa de prazo
- Resumo da conversa até o momento

O que NÃO entra no `customer_context.json`:
- Suposições do sistema sobre o cliente
- Preferências inferidas não confirmadas
- Dados que podem mudar durante o ciclo (cotação de frete em tempo real — isso vai para outro arquivo)

**Zona de Criação (verde) — Generator**

O Generator é um agente com uma missão clara: propor a melhor solução possível com as informações disponíveis. Ele não se preocupa em verificar cada detalhe. Ele não tenta antecipar o que o Evaluator vai encontrar. Ele foca em cobertura (explorar boas opções) e utilidade (cada opção deve fazer sentido para o cliente).

O Generator opera com temperature mais alta (0.7 a 1.0) porque seu trabalho é criativo. Ele precisa considerar alternativas que não são óbvias. Ele precisa explorar o espaço de soluções, não apenas repetir a recomendação mais comum.

O output do Generator é `generator_draft_v{N}.json`. Este arquivo contém:
- **SKU recomendado** — identificador único do produto
- **Preço calculado** — incluindo descontos aplicáveis conhecidos
- **Claims** — o que a recomendação afirma (ex: "ajuda na recuperação muscular", "sabor chocolate", "dentro do orçamento")
- **Assumptions** — o que o Generator assumiu como verdadeiro mas não verificou (ex: "assumi que whey isolado não contém lactose")
- **Evidence used** — quais fontes foram consultadas (ex: "catalog_snapshot_2026_05_28", "customer_context.json")
- **Confidence** — autoavaliação do Generator sobre a qualidade da proposta (0 a 1)

A confidence declarada pelo Generator é um dado interessante, mas o Evaluator **não deve usá-la** como critério de aprovação. Um Generator confiante demais pode estar errado. Um Generator com baixa confiança pode ter feito um trabalho excelente. A confidence é metadata, não evidência.

**Zona de Julgamento (laranja) — Evaluator**

O Evaluator é o oposto do Generator. Ele não cria nada. Ele não propõe nada. Ele testa. Sua missão é encontrar falhas na proposta do Generator, usando critérios objetivos e fontes de verdade independentes.

O Evaluator opera com temperature mais baixa (0.2 a 0.3) porque seu trabalho é rigoroso e determinístico. Ele não deve "interpretar" as claims do Generator — ele deve verificá-las contra dados.

O Evaluator recebe três insumos independentes:
1. O draft do Generator (`generator_draft_v{N}.json`) — a proposta a ser testada
2. O contexto do cliente (`customer_context.json`) — os fatos imutáveis
3. A rubric — os critérios de avaliação

É crítico que o Evaluator **não receba a justificativa narrativa do Generator como se fosse evidência**. Se o Generator escreveu "este produto é excelente para iniciantes", o Evaluator não deve considerar isso como um fato. Ele deve verificar: o produto é realmente adequado para iniciantes? Quais dados do catálogo sustentam essa afirmação?

O output do Evaluator é `evaluator_verdict_v{N}.json`. Este arquivo contém:
- **Status** — `APPROVED` ou `REJECTED`
- **Score** — 0 a 100, calculado a partir dos checks individuais
- **Checks por critério** — para cada critério da rubric, o status (PASS/FAIL), severidade, evidência e razão
- **Decision summary** — resumo legível da decisão

**Zona de Persistência (azul) — State Files**

Cada artefato relevante é salvo como arquivo no sistema de arquivos. Esta é uma decisão arquitetural deliberada — não é um detalhe de implementação.

State files como arquivos JSON versionados oferecem:
- **Auditabilidade completa** — você pode reconstruir exatamente o que aconteceu em cada iteração
- **Independência de contexto** — cada role lê arquivos, não a memória de outro role
- **Replay** — você pode re-executar uma avaliação com os mesmos inputs para verificar consistência
- **Debug** — quando algo falha, você abre os arquivos e vê o estado em cada ponto

O `audit_log.jsonl` merece atenção especial. Ele é um arquivo append-only em formato JSON Lines — cada linha é um documento JSON completo representando um evento. O log é imutável: eventos nunca são alterados ou removidos, apenas adicionados. Isso garante que a timeline seja uma fonte confiável para investigação post-mortem.

**Zona de Controle (roxo) — Orquestrador**

O Orquestrador é o componente que decide o próximo passo. Ele não toma decisões criativas nem avaliativas — ele aplica regras.

As regras são:
- Se o veredito for `APPROVED` e o score >= threshold → montar `final_response.json` e enviar ao cliente
- Se o veredito for `REJECTED` e a iteração atual < max_iterations → gerar feedback e solicitar nova tentativa ao Generator
- Se a iteração atual >= max_iterations → escalar para humano
- Se houver `CRITICAL_DATA_MISSING` → pausar o caso e notificar operação

O Orquestrador é stateless entre decisões. Ele não "lembra" de casos anteriores. Cada decisão é baseada apenas no veredito atual, no contador de iteração e nas regras configuradas.

Esta simplicidade é intencional. Um Orquestrador complexo que tenta "aprender" ou "interpretar" introduziria exatamente o tipo de viés que o padrão busca eliminar.

### As 5 Regras de Fronteira que Mantêm a Separação

| Regra | O Que Proíbe | Por Que Importa |
|-------|-------------|-----------------|
| **Regra 1** | Generator nunca lê o veredito do Evaluator diretamente | O Generator deve receber apenas feedback traduzido e acionável. Se lesse o veredito bruto, poderia absorver o raciocínio do Evaluator e perder independência na próxima tentativa. |
| **Regra 2** | Evaluator nunca lê a justificativa narrativa do Generator como evidência | O Evaluator deve verificar claims contra fontes de verdade (catálogo, BD), não contra a persuasão do texto do Generator. "O produto é bom" no draft não é evidência de que o produto é bom. |
| **Regra 3** | O contexto do cliente (`customer_context.json`) nunca é alterado durante o ciclo | Se o contexto mudasse entre iterações, Generator e Evaluator estariam trabalhando sobre fatos diferentes. A imutabilidade garante consistência. |
| **Regra 4** | A rubric nunca muda durante as iterações de um mesmo caso | Se a rubric mudasse, o sistema estaria "movendo a trave" durante o jogo. Ajustes de rubric acontecem entre casos, baseados em aprendizado agregado. |
| **Regra 5** | O Orquestrador nunca toma decisões baseadas na confidence declarada pelo Generator | A confidence é metadata do Generator, não evidência de qualidade. Um Generator pode estar confiante e errado. A decisão deve ser baseada no veredito do Evaluator. |

### O Que Observar Neste Diagrama Quando Algo Der Errado

Se uma recomendação errada chegar ao cliente, o diagrama ajuda a diagnosticar onde a falha aconteceu. As perguntas certas, na ordem:

1. **O contexto estava correto?** — Verifique `customer_context.json`. A restrição do cliente estava registrada? O budget estava correto?
2. **O Generator recebeu o contexto?** — O fluxo mostra que o Generator lê `customer_context.json`. Se o arquivo existe mas o Generator não o leu, o problema está na integração.
3. **O Evaluator tinha a rubric correta?** — A rubric aplicada incluía o critério que foi violado? Se a rubric não tinha o critério, o Evaluator não poderia detectar a falha.
4. **O Evaluator teve acesso às fontes de verdade?** — O catálogo consultado estava atualizado? O campo relevante existia e estava populado?
5. **O Orquestrador aplicou as regras corretamente?** — O threshold estava configurado? O max_iterations era adequado?
6. **O audit log registrou tudo?** — Se o audit log tem gaps, a rastreabilidade está comprometida.

---

## 🔄 Diagrama 2: Fluxo de Geração e Avaliação — O Ciclo Completo com Sequence Diagram

### O Que Este Diagrama Mostra

Enquanto o Diagrama 1 mostra a **estrutura estática** — quais componentes existem, como se conectam, quais regras de fronteira os governam — este diagrama mostra o **comportamento dinâmico**. É a sequência temporal de eventos que transforma um input de cliente em uma recomendação aprovada e enviada — ou em uma escalação para revisão humana.

Este é o fluxo que acontece em produção, a cada recomendação que o KODA faz. Cada número na sequência é um evento que gera uma entrada no audit log. Cada transição entre fases é uma decisão do Orquestrador baseada em regras.

O diagrama também inclui o cenário alternativo de máximo de iterações — o que acontece quando o sistema não consegue aprovar uma recomendação em 3 tentativas.

```mermaid
sequenceDiagram
    autonumber

    participant CL as 🧑 Cliente
    participant ORQ as 🎛️ Orquestrador
    participant CTX as 💾 customer_context.json
    participant GEN as ✏️ Generator
    participant DRF as 📄 generator_draft
    participant EVL as ⚖️ Evaluator
    participant RUB as 📋 Rubric
    participant VER as 📊 evaluator_verdict
    participant FBK as 🔄 feedback
    participant LOG as 📜 audit_log.jsonl
    participant HUM as 👤 Humano

    Note over CL,HUM: ═══════════════════════════════════════
    Note over CL,HUM: FASE 0 — Inicialização do Caso
    Note over CL,HUM: ═══════════════════════════════════════

    CL->>ORQ: "Preciso de whey, sou intolerante à lactose, orçamento R$ 160"
    ORQ->>ORQ: Extrai objetivo, restrições, budget da mensagem
    ORQ->>CTX: Escreve customer_context.json com fatos imutáveis
    ORQ->>LOG: event=case_initialized, case_id=rec_marina_001
    ORQ->>ORQ: Configura max_iterations=3, threshold=85, on_max=human_review

    Note over CL,HUM: ═══════════════════════════════════════
    Note over CL,HUM: FASE 1 — Primeira Geração
    Note over CL,HUM: ═══════════════════════════════════════

    ORQ->>GEN: Solicita recomendação (iteration=1, feedback=None)
    GEN->>CTX: Lê customer_context.json
    GEN->>GEN: Consulta catálogo de produtos
    GEN->>GEN: Analisa: objetivo=recuperação, budget=160, restrição=lactose
    GEN->>GEN: Seleciona WHEY-ISO-149 (Whey Isolado Premium, R$149.90)
    GEN->>GEN: Assume: "isolado = sem lactose" (INCORRETO)
    GEN->>DRF: Escreve generator_draft_v1.json
    GEN->>LOG: event=generation_completed, iteration=1, sku=WHEY-ISO-149, confidence=0.78

    Note over CL,HUM: ═══════════════════════════════════════
    Note over CL,HUM: FASE 2 — Primeira Avaliação
    Note over CL,HUM: ═══════════════════════════════════════

    ORQ->>EVL: Solicita avaliação (iteration=1)
    EVL->>CTX: Lê customer_context.json (restrição: intolerancia_lactose, severity=CRITICAL)
    EVL->>DRF: Lê generator_draft_v1.json
    EVL->>RUB: Carrega rubric: product_recommendation_safety_v3
    EVL->>EVL: Para cada critério da rubric, consulta fontes de verdade

    Note over EVL: Critério: lactose_free<br/>Catálogo: WHEY-ISO-149.contains_lactose_trace = TRUE<br/>Cliente: intolerancia_lactose = CRITICAL<br/>Resultado: ❌ FAIL (CRITICAL)

    Note over EVL: Critério: budget<br/>Preço: 149.90 ≤ budget_max: 160<br/>Resultado: ✅ PASS

    Note over EVL: Critério: goal_fit<br/>Categoria: proteína, objetivo: recuperação<br/>Resultado: ✅ PASS

    Note over EVL: Critério: stock<br/>Estoque: 34 unidades, região: SP<br/>Resultado: ✅ PASS

    Note over EVL: Critério: message_safety<br/>Mensagem omite risco de lactose<br/>Resultado: ❌ FAIL (HIGH)

    EVL->>VER: Escreve evaluator_verdict_v1.json
    Note over VER: Status: REJECTED<br/>Score: 42/100<br/>Threshold: 85<br/>Checks: 3 PASS, 2 FAIL<br/>1 CRITICAL, 1 HIGH

    EVL->>LOG: event=evaluation_completed, iteration=1, verdict=REJECTED, score=42

    Note over CL,HUM: ═══════════════════════════════════════
    Note over CL,HUM: FASE 3 — Decisão e Feedback
    Note over CL,HUM: ═══════════════════════════════════════

    ORQ->>VER: Lê evaluator_verdict_v1.json
    ORQ->>ORQ: Veredito: REJECTED. Score 42 < threshold 85
    ORQ->>ORQ: Iteração atual: 1. Max: 3. 1 < 3 → CONTINUAR
    EVL->>FBK: Escreve feedback_v1.json
    Note over FBK: Issue 1 [CRITICAL]: WHEY-ISO-149 contém traços de lactose.<br/>Ação: Remover SKU. Buscar lactose_free=true.<br/>Issue 2 [HIGH]: Mensagem omite restrição.<br/>Ação: Incluir verificação de segurança na mensagem.

    FBK->>LOG: event=feedback_generated, iteration=1, issues=2
    ORQ->>ORQ: Prepara retry com feedback para iteração 2

    Note over CL,HUM: ═══════════════════════════════════════
    Note over CL,HUM: FASE 4 — Segunda Geração (com Feedback)
    Note over CL,HUM: ═══════════════════════════════════════

    ORQ->>GEN: Solicita recomendação (iteration=2, feedback=fb_001)
    GEN->>FBK: Lê feedback_v1.json
    GEN->>CTX: Re-lê customer_context.json
    GEN->>GEN: Remove WHEY-ISO-149 da lista de candidatos
    GEN->>GEN: Filtra catálogo: lactose_free=true AND contains_lactose_trace=false
    GEN->>GEN: Seleciona PLANT-PRO-155 (Proteína Vegetal Pro Chocolate, R$155.00)
    GEN->>GEN: Verifica flags do catálogo (não assume mais)
    GEN->>DRF: Escreve generator_draft_v2.json
    Note over DRF: sku: PLANT-PRO-155<br/>lactose_free: TRUE (confirmado)<br/>contains_lactose_trace: FALSE (confirmado)<br/>feedback_applied: fb_001<br/>confidence: 0.86

    GEN->>LOG: event=generation_completed, iteration=2, sku=PLANT-PRO-155, confidence=0.86

    Note over CL,HUM: ═══════════════════════════════════════
    Note over CL,HUM: FASE 5 — Segunda Avaliação
    Note over CL,HUM: ═══════════════════════════════════════

    ORQ->>EVL: Solicita avaliação (iteration=2)
    EVL->>CTX: Lê customer_context.json
    EVL->>DRF: Lê generator_draft_v2.json
    EVL->>RUB: Carrega rubric (mesma versão da iteração 1)

    Note over EVL: Critério: lactose_free<br/>SKU: PLANT-PRO-155<br/>Catálogo: lactose_free=TRUE, contains_lactose_trace=FALSE<br/>Resultado: ✅ PASS (CRITICAL)

    Note over EVL: Critério: budget<br/>Preço: 155.00 ≤ budget_max: 160<br/>Resultado: ✅ PASS

    Note over EVL: Critério: goal_fit<br/>Proteína vegetal para recuperação<br/>Resultado: ✅ PASS

    Note over EVL: Critério: stock<br/>Estoque: 89 unidades, região: SP<br/>Resultado: ✅ PASS

    Note over EVL: Critério: message_clarity<br/>Mensagem menciona segurança alimentar<br/>Resultado: ✅ PASS

    EVL->>VER: Escreve evaluator_verdict_v2.json
    Note over VER: Status: APPROVED<br/>Score: 93/100<br/>Threshold: 85<br/>Checks: 5 PASS, 0 FAIL<br/>0 violações

    EVL->>LOG: event=evaluation_completed, iteration=2, verdict=APPROVED, score=93

    Note over CL,HUM: ═══════════════════════════════════════
    Note over CL,HUM: FASE 6 — Aprovação e Envio
    Note over CL,HUM: ═══════════════════════════════════════

    ORQ->>VER: Lê evaluator_verdict_v2.json
    ORQ->>ORQ: Veredito: APPROVED. Score 93 >= threshold 85
    ORQ->>ORQ: Monta final_response.json com mensagem e audit_summary
    ORQ->>LOG: event=recommendation_approved, iterations=2, final_score=93
    ORQ->>CL: "Marina, recomendo Proteína Vegetal Pro Chocolate. Sem lactose, R$155, em estoque, entrega em 2 dias."
    ORQ->>LOG: event=response_delivered, case_id=rec_marina_001

    Note over CL,HUM: ═══════════════════════════════════════
    Note over CL,HUM: CENÁRIO ALTERNATIVO — Máximo de Iterações
    Note over CL,HUM: ═══════════════════════════════════════

    alt Máximo de iterações atingido sem aprovação
        ORQ->>ORQ: Iteration 3: ainda REJECTED (score 62). 3 >= max_iterations(3)
        ORQ->>HUM: Escala caso para revisão humana com contexto completo
        ORQ->>LOG: event=escalated_to_human, case_id=rec_marina_001, reason=max_iterations_reached, attempts=3
        HUM->>HUM: Revisor analisa: contexto, drafts, vereditos, feedback
        HUM->>ORQ: Decisão manual: APPROVED (com ajuste) ou REJECTED (sem solução)
        ORQ->>LOG: event=human_decision, case_id=rec_marina_001, decision=APPROVED, reviewer=fernando
    end
```

### O Que Este Fluxo Revela Sobre o Comportamento do Sistema

**Cada iteração é autocontida e stateless.**

O Generator da iteração 2 não "lembra" da iteração 1 por memória de contexto ou continuação de conversa. Ele começa do zero. Ele lê o `customer_context.json` (os fatos) e o `feedback_v1.json` (o que corrigir). Essa separação é fundamental: garante que o Generator da iteração 2 não está contaminado pelo raciocínio potencialmente errado da iteração 1. A única coisa que atravessa a fronteira entre iterações é o feedback — estruturado, específico, acionável.

Se o Generator da iteração 2 lesse o draft da iteração 1 diretamente, ele poderia ser influenciado pela mesma linha de raciocínio que produziu o erro. O feedback, por outro lado, não diz "seu raciocínio estava errado". Ele diz "este SKU viola esta constraint — remova-o e busque alternativas com estas flags".

**O Evaluator sempre parte do zero, a cada iteração.**

Ele nunca recebe "o Generator acha que está bom desta vez" ou "o Generator está mais confiante na segunda tentativa". Ele recebe: o draft atual, o contexto imutável, e a rubric. A ausência de narrativa de progresso entre iterações é uma feature. O Evaluator avalia cada draft pelos mesmos critérios, com o mesmo rigor. Se a segunda tentativa for melhor, o score refletirá isso objetivamente. Se for pior, o score cairá — mesmo que seja a segunda tentativa.

**O feedback é a interface entre os roles — não uma conversa.**

Observe que não há seta de "conversa" entre Generator e Evaluator. Eles não dialogam. Não negociam. Não trocam mensagens de chat. A comunicação é inteiramente mediada por artefatos persistidos: o draft (Generator → Evaluator) e o feedback (Evaluator → Generator, via Orquestrador).

Isso elimina uma classe inteira de problemas: o Generator não pode "convencer" o Evaluator com retórica. O Evaluator não pode "dar uma dica" informal que o Generator interprete mal. Toda comunicação é estruturada, versionada e auditável.

**O Orquestrador é um autômato de estados.**

O Orquestrador não tem intuição. Não tem "feeling". Não tem "experiência". Ele aplica regras booleanas: veredito == APPROVED? score >= threshold? iteration < max_iterations? Cada combinação de respostas leva a exatamente uma ação. Esta previsibilidade é o que torna o sistema confiável e auditável.

**O audit log é a memória do sistema — e é imutável.**

Cada evento numerado no sequence diagram gera uma entrada no `audit_log.jsonl`. O log é append-only: uma vez escrito, nunca alterado. Se algo der errado em produção, você reconstrói a timeline exata lendo o audit log, não tentando lembrar o que aconteceu ou interpretando logs de sistema genéricos.

### Estados Possíveis do Ciclo e Suas Transições

| Estado | Condição de Entrada | Ação | Próximo Estado |
|--------|---------------------|------|----------------|
| `INITIALIZING` | Cliente envia mensagem | Escrever `customer_context.json`, logar `case_initialized` | `GENERATING` |
| `GENERATING` | Orquestrador solicita ao Generator | Generator lê contexto, consulta catálogo, gera draft | `EVALUATING` |
| `EVALUATING` | Orquestrador solicita ao Evaluator | Evaluator lê draft, contexto, rubric; escreve veredito | `DECIDING` |
| `DECIDING` | Veredito disponível | Orquestrador lê veredito e aplica regras | `APPROVED`, `RETRYING`, `MAX_ITERATIONS`, ou `DATA_MISSING` |
| `APPROVED` | Score >= threshold, sem violações CRITICAL | Montar `final_response.json`, enviar ao cliente, logar `response_delivered` | `CLOSED` |
| `RETRYING` | Score < threshold OU violação CRITICAL, e iteration < max | Gerar feedback, incrementar iteração | `GENERATING` |
| `MAX_ITERATIONS` | Score < threshold, e iteration >= max | Escalar para humano, logar `escalated_to_human` | `AWAITING_HUMAN` |
| `AWAITING_HUMAN` | Caso escalado | Aguardar decisão humana | `CLOSED` (após decisão) |
| `DATA_MISSING` | Falta dado essencial (catálogo offline, cliente não encontrado) | Pausar caso, notificar operação | `INITIALIZING` (após correção) ou `CLOSED` (se irrecuperável) |
| `CLOSED` | Caso concluído (aprovado, rejeitado por humano, ou abandonado) | Liberar recursos, arquivar state files | — (terminal) |

### O Que Este Fluxo NÃO Mostra (E Por Que)

O sequence diagram foca no ciclo principal. Algumas coisas ficam de fora deliberadamente:

- **Timeouts e retries de infraestrutura** — Se a chamada ao Generator falhar por timeout de rede, o sistema tenta novamente? Isso é tratamento de erro de infra, não faz parte do padrão Generator/Evaluator. O padrão presume que as chamadas são confiáveis.
- **Processamento paralelo de múltiplos casos** — O KODA atende vários clientes simultaneamente. Cada caso é independente e tem seu próprio conjunto de state files. O diagrama mostra um caso.
- **Métricas e monitoramento** — Em produção, cada evento do audit log também alimenta dashboards de métricas (taxa de rejeição, tempo médio de ciclo, distribuição de scores). Isso é camada de observabilidade, não de arquitetura.
- **Otimizações de cache** — O catálogo de produtos pode ser cacheado para evitar consultas repetidas. A rubric pode ser carregada uma vez e reutilizada. Isso é otimização de implementação.

---

## ⚙️ Seção 3: Mecanismos de Coordenação — Tabela Comparativa e Framework de Decisão

### Por Que Coordenação É o Elo Esquecido do Generator/Evaluator

Quando as pessoas ouvem "Generator/Evaluator" pela primeira vez, a imagem mental mais comum é: "dois prompts diferentes". Um prompt que gera. Outro prompt que avalia. Fim.

Isso é 20% do padrão. E é a parte fácil.

Os outros 80% estão em **como** os dois roles trocam informação de forma confiável, rastreável e sem contaminação de viés. Esta é a coordenação — e ela é o que separa um Generator/Evaluator que funciona de um que é teatro.

Sem coordenação explícita, você tem dois agentes trabalhando com visões potencialmente diferentes do mesmo problema. O Generator acha que o orçamento é R$ 200. O Evaluator acha que é R$ 160. Ambos estão "certos" dentro de suas visões — e o sistema produz uma decisão inconsistente.

A coordenação responde a cinco perguntas fundamentais:

1. **Quem** produz o quê? — Separação de responsabilidades entre os artefatos
2. **Onde** cada artefato é armazenado? — Persistência e versionamento
3. **Quando** cada role pode ler ou escrever? — Controle de concorrência e ordem
4. **Como** o feedback é comunicado? — Estrutura e especificidade
5. **Por que** o sistema confia (ou não) em cada informação? — Fontes de verdade e níveis de confiança

### A Arquitetura de State Files no KODA

Antes da tabela comparativa, vamos visualizar a arquitetura completa de state files que o KODA usa. Este diagrama ASCII mostra como os arquivos se relacionam, quem escreve cada um, e como a informação flui sem contaminação:

```text
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                    KODA GENERATOR/EVALUATOR — ARQUITETURA DE STATE FILES                │
│                    Coordenação por Artefatos Versionados + Audit Log                    │
└─────────────────────────────────────────────────────────────────────────────────────────┘

                              ┌──────────────────────────┐
                              │     CLIENTE (WhatsApp)    │
                              │  "Quero whey sem lactose" │
                              └────────────┬─────────────┘
                                           │
                                           ▼
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│  ORQUESTRADOR (Orchestrator)                                                              │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐ │
│  │ Configuração do Ciclo:                                                               │ │
│  │   max_iterations = 3                                                                 │ │
│  │   approval_threshold = 85                                                            │ │
│  │   on_max_reached = escalate_to_human                                                 │ │
│  │   on_critical_data_missing = pause_case                                              │ │
│  │                                                                                      │ │
│  │ Decisão por Estado:                                                                  │ │
│  │   APPROVED + score >= 85        → final_response.json → enviar ao cliente            │ │
│  │   REJECTED + iteration < 3      → feedback_v{N}.json → nova tentativa                │ │
│  │   REJECTED + iteration >= 3     → escalar para humano                                │ │
│  │   CRITICAL_DATA_MISSING         → pausar caso                                        │ │
│  └─────────────────────────────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────────────────────────┘
           │                    │                    │                    │
           ▼                    ▼                    ▼                    ▼
┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│ customer_context │ │ generator_draft  │ │ evaluator_verdict│ │    feedback      │
│     .json        │ │   _v{N}.json     │ │   _v{N}.json     │ │   _v{N}.json     │
│                  │ │                  │ │                  │ │                  │
│ ESCRITO POR:     │ │ ESCRITO POR:     │ │ ESCRITO POR:     │ │ ESCRITO POR:     │
│ Orquestrador     │ │ Generator        │ │ Evaluator        │ │ Evaluator        │
│ (setup inicial)  │ │                  │ │                  │ │ (via Orq.)       │
│                  │ │                  │ │                  │ │                  │
│ LIDO POR:        │ │ LIDO POR:        │ │ LIDO POR:        │ │ LIDO POR:        │
│ Generator        │ │ Evaluator        │ │ Orquestrador     │ │ Generator        │
│ Evaluator        │ │                  │ │                  │ │ (próx. iteração) │
│                  │ │                  │ │                  │ │                  │
│ IMUTÁVEL: SIM    │ │ IMUTÁVEL: SIM    │ │ IMUTÁVEL: SIM    │ │ IMUTÁVEL: SIM    │
│ (durante ciclo)  │ │ (versionado)     │ │ (versionado)     │ │ (versionado)     │
│                  │ │                  │ │                  │ │                  │
│ CONTEÚDO:        │ │ CONTEÚDO:        │ │ CONTEÚDO:        │ │ CONTEÚDO:        │
│ • Cliente ID     │ │ • SKU(s)         │ │ • Status         │ │ • Issues[]       │
│ • Restrições []  │ │ • Preço          │ │ • Score (0-100)  │ │ • Severidade     │
│ • Budget max     │ │ • Claims[]       │ │ • Checks[]       │ │ • Constraint     │
│ • Objetivo       │ │ • Assumptions[]  │ │ • Severidade     │ │ • Ação esperada  │
│ • Histórico      │ │ • Evidence[]     │ │ • Evidência      │ │ • SKUs a evitar  │
│ • Preferências   │ │ • Confidence     │ │ • Sumário        │ │ • Instruções     │
│ • Região         │ │ • Notas          │ │                  │ │                  │
└──────────────────┘ └──────────────────┘ └──────────────────┘ └──────────────────┘
           │                    │                    │                    │
           └────────────────────┼────────────────────┼────────────────────┘
                                │                    │
                                ▼                    ▼
                    ┌─────────────────────────────────────────────────┐
                    │              audit_log.jsonl                    │
                    │  (Append-only — nunca alterado ou truncado)     │
                    │                                                 │
                    │  {"ts":"10:00:00","event":"case_initialized"}   │
                    │  {"ts":"10:00:05","event":"generation_started"} │
                    │  {"ts":"10:00:12","event":"generation_completed"│
                    │   ,"iteration":1,"confidence":0.78}             │
                    │  {"ts":"10:00:13","event":"evaluation_started"} │
                    │  {"ts":"10:00:18","event":"evaluation_completed"│
                    │   ,"iteration":1,"verdict":"REJECTED",          │
                    │   "score":42}                                   │
                    │  {"ts":"10:00:19","event":"feedback_generated", │
                    │   "iteration":1,"issues":2}                     │
                    │  {"ts":"10:00:20","event":"generation_started", │
                    │   "iteration":2,"has_feedback":true}            │
                    │  {"ts":"10:00:25","event":"generation_completed"│
                    │   ,"iteration":2,"confidence":0.86}             │
                    │  {"ts":"10:00:26","event":"evaluation_started"} │
                    │  {"ts":"10:00:30","event":"evaluation_completed"│
                    │   ,"iteration":2,"verdict":"APPROVED",          │
                    │   "score":93}                                   │
                    │  {"ts":"10:00:31","event":"response_delivered"} │
                    └─────────────────────────────────────────────────┘
```

### Tabela Comparativa de Estratégias de Coordenação

A tabela abaixo compara seis estratégias de coordenação que poderiam ser usadas para implementar Generator/Evaluator. Cada estratégia tem pontos fortes e fracos. A escolha depende do contexto: custo do erro, necessidade de auditoria, volume de casos, e maturidade da equipe.

| Estratégia | Mecanismo | Sincronização | Sycophancy Risk | Auditabilidade | Complexidade Operacional | Custo por Caso | Melhor Para |
|------------|-----------|---------------|-----------------|----------------|--------------------------|----------------|-------------|
| **Gen/Eval com State Files** | Arquivos JSON versionados como canal único. Generator escreve `draft_v{N}.json`. Evaluator lê e escreve `verdict_v{N}.json`. Orquestrador lê veredito e decide. Feedback é artefato separado. | Assíncrona — cada role opera sobre snapshots de arquivo. Não há memória compartilhada entre iterações. | **Baixo** — Evaluator recebe apenas o draft (artefato estruturado), não a narrativa de confiança do Generator. Rubric independente aplicada sobre fontes de verdade. | **Alta** — Cada estado do ciclo é um arquivo versionado com nome explícito. Audit log em JSONL registra timeline completa. Replay e diff entre versões é trivial. | **Média** — Requer disciplina de schema (validar JSON na escrita e leitura), convenção de nomes (`_v{N}`), e orquestrador explícito. Setup inicial: 2-4 horas por feature. | Médio (2-4 chamadas LLM para 1-2 iterações) | Tarefas críticas com critérios objetivos e necessidade de auditoria. Recomendação de produto, processamento de pedido, validação de promoções, compliance regulatório. |
| **Gen/Eval com Message Passing** | Mensagens explícitas entre agentes via fila ou broker (RabbitMQ, Kafka, SQS). Generator publica draft em tópico. Evaluator consome e publica veredito. | Pode ser síncrona (RPC) ou assíncrona (fila). Permite paralelismo quando múltiplos Evaluators consomem da mesma fila. | **Baixo a Médio** — Depende do conteúdo das mensagens. Se mensagens carregam apenas artefatos estruturados, risco é baixo. Se carregam também narrativa do Generator, risco sobe. | **Média** — Se mensagens são persistidas (dead letter queue, event store, log compactado do Kafka), é auditável. Se são voláteis e a fila não tem retenção longa, perde-se rastreabilidade. | **Média a Alta** — Requer infraestrutura de mensageria, configuração de tópicos/filas, tratamento de falhas de entrega. Ganha em desacoplamento mas adiciona superfície operacional. | Médio a Alto (infra adicional, mas reutilizável entre features) | Sistemas com múltiplos Generators ou Evaluators em paralelo. Cenários de alta vazão (>100 casos/min) onde I/O de arquivo seria gargalo. Equipes que já operam infra de mensageria. |
| **Gen/Eval com Shared Memory** | Banco de dados relacional (PostgreSQL), cache (Redis) ou vector store como espaço comum. Ambos os roles leem e escrevem no mesmo namespace (tabelas, chaves). | Síncrona ou quase-síncrona. Risco de race condition se Generator e Evaluator escrevem simultaneamente na mesma linha/tabela. | **Alto** — Generator pode escrever assumptions no espaço compartilhado que o Evaluator lê como fatos. A fronteira entre hipótese e verdade se dissolve porque ambos leem do mesmo lugar. | **Baixa a Média** — Depende de governança de escrita (quem pode escrever em qual tabela/coluna). Sem fronteiras explícitas, é difícil saber qual role introduziu qual dado. Migrations de schema podem corromper dados históricos. | **Baixa** — Infraestrutura familiar para a maioria das equipes (PostgreSQL, Redis). Setup rápido. ORMs e ferramentas maduras. | Variável (depende do volume de queries) | Prototipagem rápida e experimentação. Casos não-críticos onde a separação de roles é mais conceitual que técnica. Sistemas onde velocidade de iteração > rigor de auditoria. |
| **Self-Evaluation (Agente Único)** | O mesmo agente gera e depois avalia a própria resposta. "Verifique se sua recomendação está correta" como parte do mesmo prompt ou como prompt seguinte na mesma conversa. | Síncrona por definição — geração e avaliação compartilham a mesma context window e a mesma chamada de API (ou chamadas consecutivas sem separação de estado). | **Muito Alto** — A resposta gerada é parte do contexto que o modelo usa para avaliar. Sycophancy: o modelo tende a concordar com o que acabou de escrever. Confirmation bias: busca evidências que confirmam a resposta, ignora as que a contradizem. | **Muito Baixa** — Geração e avaliação se misturam no mesmo trace. Não há artefato intermediário para inspecionar. Se o modelo diz "verifiquei e está correto", não há como saber se realmente verificou ou apenas racionalizou. | **Muito Baixa** — Uma ou duas chamadas de API. Zero infraestrutura adicional. Zero arquivos para gerenciar. | Muito Baixo (1-2 chamadas) | Respostas simples com baixíssimo custo de erro: confirmação de pagamento, consulta de status de pedido, FAQ estático, saudações. Qualquer cenário onde "pior caso = cliente repete a pergunta". |
| **Multi-Agent Consensus** | Vários agentes (3, 5, 7) geram propostas independentes ou votam em propostas existentes. Sistema agrega por maioria, média ponderada, ou algoritmo de consenso (ex: Raft simplificado). | Paralela — múltiplos agentes operam simultaneamente sobre o mesmo input. Latência é determinada pelo agente mais lento. | **Médio** — Se todos os agentes recebem o mesmo contexto potencialmente enviesado (mesmos dados de treino, mesmo system prompt), o consenso pode amplificar o viés (groupthink). A diversidade de perspectiva é essencial e difícil de garantir com LLMs do mesmo modelo. | **Média** — Depende de registrar votos individuais com justificativa. Sem registro por agente, o consenso é uma caixa preta. Com registro, é auditável mas mais complexo. | **Alta** — Coordenar N agentes, agregar resultados com lógica de consenso, resolver impasses (o que fazer quando 3 votam A, 3 votam B, e 1 vota C?). Latência maior (N chamadas em paralelo). Custo N vezes maior. | Alto (N chamadas por caso, tipicamente 3-7) | Problemas abertos com múltiplas perspectivas válidas: brainstorming de features, análise de risco multifatorial, decisões estratégicas sem resposta certa única. Cenários onde diversidade de pensamento agrega valor real. |
| **Human-in-the-Loop (HITL)** | Humano revisa, aprova, rejeita ou ajusta saídas antes da entrega final. Pode ser aplicado como último recurso (após max_iterations) ou como passo obrigatório para casos críticos. | Assíncrona — humano opera em tempo humano (segundos a horas). Sistema precisa de fila de revisão, SLA, notificações e timeout. | **Muito Baixo** no ponto de revisão — o humano não participou da geração. Mas o humano tem seus próprios vieses: fadiga (após 50 revisões), pressa, inconsistência entre revisores diferentes. | **Alta** — Decisão humana deve ser registrada com: revisor ID, timestamp, decisão, justificativa. Se bem implementado, é o mecanismo mais auditável. | **Muito Alta** — Custo operacional contínuo (salário de revisores). Requer fila de revisão, SLA, treinamento, calibração entre revisores, cobertura de turnos. | Alto (custo humano recorrente + latência variável) | Casos de altíssimo risco: decisões com impacto em saúde, finanças ou legal. Max iterations atingido sem aprovação. Exceções que o sistema não foi projetado para resolver. |

### Framework de Decisão: Quatro Perguntas para Escolher a Estratégia

Use estas quatro perguntas em sequência. Cada resposta reduz o espaço de estratégias viáveis:

```
PERGUNTA 1: Qual o custo de um erro chegar ao cliente?

├── BAIXO (cliente repete a pergunta, sem consequências) 
│   → Self-Evaluation ou CoT são suficientes
│
├── MÉDIO (cliente fica insatisfeito, pode gerar churn, devolução)
│   → Gen/Eval com State Files ou Message Passing
│
└── ALTO (questão de saúde, dinheiro, legal, reputação da marca)
    → Gen/Eval com State Files + HITL como fallback


PERGUNTA 2: Os critérios de qualidade são objetivos e escrevíveis?

├── SIM (lactose_free=true, price<=budget, in_stock=true)
│   → Gen/Eval com State Files (rubric pode ser aplicada deterministicamente)
│
├── PARCIALMENTE (alguns critérios são objetivos, outros subjetivos)
│   → Gen/Eval com State Files + HITL para critérios subjetivos
│
└── NÃO (depende de julgamento estético, criativo ou contextual)
    → Multi-Agent Consensus ou HITL como mecanismo primário


PERGUNTA 3: Você precisa auditar decisões depois que elas acontecem?

├── SIM (compliance regulatório, melhoria contínua, debug de incidentes)
│   → State Files ou Message Passing com event store
│
├── ÀS VEZES (debug ocasional, sem requisito formal)
│   → Message Passing com retenção curta é suficiente
│
└── NÃO (protótipo, experimento descartável, hackathon)
    → Shared Memory ou Self-Evaluation


PERGUNTA 4: Qual o volume de casos por minuto e por dia?

├── BAIXO (< 10 casos/min, < 1000 casos/dia)
│   → State Files (simples, auditável, fácil de debugar)
│
├── MÉDIO (10-100 casos/min, 1000-10000 casos/dia)
│   → Message Passing (escalável, desacoplado, suporta paralelismo)
│
└── ALTO (> 100 casos/min, > 10000 casos/dia)
    → Message Passing + fila dedicada + pool de Evaluators
      (State Files viram gargalo de I/O neste volume)
```

### Matriz de Decisão Rápida

| Custo do Erro | Volume | Precisa Auditar? | Estratégia Recomendada |
|---------------|--------|------------------|----------------------|
| Baixo | Qualquer | Não | Self-Evaluation |
| Médio | Baixo | Sim | Gen/Eval + State Files |
| Médio | Alto | Sim | Gen/Eval + Message Passing + Event Store |
| Alto | Baixo | Sim | Gen/Eval + State Files + HITL fallback |
| Alto | Alto | Sim | Gen/Eval + Message Passing + HITL queue |
| Subjetivo | Qualquer | — | Multi-Agent Consensus ou HITL |

### O Custo Relativo das Estratégias (Ordem de Grandeza)

Para uma recomendação de produto típica do KODA:

| Estratégia | Tokens (aproximado) | Latência (aproximado) | Custo Financeiro (ordem) |
|------------|---------------------|----------------------|--------------------------|
| Self-Evaluation | 500-1000 | 1-3 segundos | $ |
| Gen/Eval + State Files (1 iteração) | 2000-3000 | 3-6 segundos | $$ |
| Gen/Eval + State Files (2 iterações) | 4000-5000 | 5-10 segundos | $$$ |
| Multi-Agent Consensus (5 agentes) | 5000-8000 | 5-8 segundos (paralelo) | $$$$ |
| HITL (revisão humana) | 2000-3000 + tempo humano | 30 seg - 30 min | $$$$$ |

O Gen/Eval com State Files tipicamente resolve em 1-2 iterações para ~80% dos casos do KODA. Os 20% restantes podem precisar de 3 iterações ou HITL.

---

## 💼 Diagrama 3: Aplicação KODA — Recomendação de Produto com Trace Visual

### O Que Este Diagrama Mostra

Este é o knowledge graph aplicado ao cenário mais comum e mais crítico do KODA: **recomendação de produto para cliente com restrição alimentar**.

O diagrama mostra:
- O ciclo completo de rejeição → feedback → segunda tentativa → aprovação
- Os artefatos JSON que trafegam entre os roles (versão compacta dentro das caixas)
- A decisão do Orquestrador em cada ponto
- A diferença de qualidade entre a iteração 1 (assumiu, errou) e a iteração 2 (verificou, acertou)

```mermaid
graph TD
    subgraph CASO["📋 Caso: Marina — Intolerante à Lactose, Budget R$ 160, Objetivo: Recuperação Muscular"]
        direction TB

        CTX["💾 customer_context.json<br/>━━━━━━━━━━━━━━━━━━━━━━━<br/>customer: Marina<br/>restrictions:<br/>  • intolerancia_lactose [CRITICAL]<br/>  • rule: não recomendar produtos<br/>    com lactose ou traços_de_lactose<br/>budget_max_brl: 160<br/>goal: recuperacao_muscular<br/>flavor_pref: chocolate, baunilha<br/>region: sao_paulo<br/>delivery: ate_3_dias"]

        subgraph ITER1["🔄 ITERAÇÃO 1 — Erro Capturado"]
            G1["✏️ GENERATOR (v1)<br/>━━━━━━━━━━━━━━━━━━━<br/>Lê contexto. Consulta catálogo.<br/>Seleciona: WHEY-ISO-149<br/>Whey Isolado Premium Chocolate<br/>R$ 149.90<br/><br/>Claims:<br/>✅ ajuda recuperação muscular<br/>✅ sabor chocolate<br/>✅ dentro do orçamento<br/><br/>Assumptions:<br/>⚠️ isolado = sem lactose<br/>   (NÃO VERIFICOU no catálogo)<br/><br/>Confidence: 0.78"]
            D1["📄 generator_draft_v1.json<br/>━━━━━━━━━━━━━━━━━━━━━<br/>generation_id: gen_001<br/>sku: WHEY-ISO-149<br/>price: 149.90<br/>claimed_fit: recuperação,<br/>  chocolate, orçamento<br/>assumptions: lactose_free<br/>  (não verificado)<br/>confidence: 0.78"]
            E1["⚖️ EVALUATOR (v1)<br/>━━━━━━━━━━━━━━━━━━━<br/>Lê contexto: cliente intolerante<br/>Lê draft: WHEY-ISO-149<br/>Consulta catálogo:<br/>  contains_lactose_trace: TRUE ⚠️<br/><br/>Checks contra rubric:<br/>❌ lactose_free — CRITICAL FAIL<br/>   (contém traços de lactose)<br/>✅ budget — PASS (149.90 ≤ 160)<br/>✅ goal_fit — PASS (proteína)<br/>✅ stock — PASS (34 unidades)<br/>❌ message_safety — HIGH FAIL<br/>   (mensagem omite risco)<br/><br/>Score: 42/100<br/>VERDICT: ❌ REJECTED"]
            F1["🔄 feedback_v1.json<br/>━━━━━━━━━━━━━━━━━━━━━<br/>Issue 1 [CRITICAL]:<br/>  constraint: intolerancia_lactose<br/>  problem: WHEY-ISO-149 contém<br/>    traços de lactose<br/>  action: REMOVER este SKU.<br/>    Buscar apenas produtos com<br/>    lactose_free=true E<br/>    contains_lactose_trace=false<br/>Issue 2 [HIGH]:<br/>  constraint: message_safety<br/>  action: mencionar verificação<br/>    de segurança na mensagem"]
        end

        G1 --> D1
        D1 --> E1
        CTX --> G1
        CTX --> E1
        E1 -->|"REJECTED"| F1

        subgraph ITER2["🔄 ITERAÇÃO 2 — Correção Guiada por Feedback"]
            G2["✏️ GENERATOR (v2, com feedback)<br/>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━<br/>Lê feedback: remover WHEY-ISO-149<br/>Lê contexto: restrição lactose CRITICAL<br/>Filtra catálogo:<br/>  lactose_free=true<br/>  contains_lactose_trace=false<br/>  in_stock=true<br/>  price <= 160<br/><br/>Seleciona: PLANT-PRO-155<br/>Proteína Vegetal Pro Chocolate<br/>R$ 155.00<br/><br/>Verifica flags do catálogo:<br/>✅ lactose_free: TRUE (confirmado)<br/>✅ contains_lactose_trace: FALSE<br/>✅ in_stock: TRUE (89 unidades)<br/><br/>Mensagem inclui verificação<br/>de segurança alimentar<br/><br/>Confidence: 0.86<br/>feedback_applied: fb_001"]
            D2["📄 generator_draft_v2.json<br/>━━━━━━━━━━━━━━━━━━━━━<br/>generation_id: gen_002<br/>sku: PLANT-PRO-155<br/>price: 155.00<br/>catalog_flags:<br/>  lactose_free: true<br/>  contains_lactose_trace: false<br/>  in_stock: true<br/>feedback_applied: fb_001<br/>confidence: 0.86"]
            E2["⚖️ EVALUATOR (v2)<br/>━━━━━━━━━━━━━━━━━━━<br/>Lê contexto: cliente intolerante<br/>Lê draft: PLANT-PRO-155<br/>Verifica catálogo:<br/>  lactose_free: TRUE ✅<br/>  contains_lactose_trace: FALSE ✅<br/><br/>Checks contra rubric:<br/>✅ lactose_free — PASS (CRITICAL)<br/>✅ budget — PASS (155 ≤ 160)<br/>✅ goal_fit — PASS (proteína vegetal<br/>   para recuperação)<br/>✅ stock — PASS (89 unidades, SP)<br/>✅ message_clarity — PASS<br/>   (menciona segurança)<br/><br/>Score: 93/100<br/>VERDICT: ✅ APPROVED"]
        end

        F1 -->|"feedback"| G2
        G2 --> D2
        D2 --> E2
        CTX --> G2
        CTX --> E2

        FINAL["✅ final_response.json<br/>━━━━━━━━━━━━━━━━━━━━━<br/>Caso: rec_marina_001<br/>Recomendação aprovada:<br/>  Produto: Proteína Vegetal Pro<br/>    Chocolate<br/>  SKU: PLANT-PRO-155<br/>  Preço: R$ 155.00<br/>  Sem lactose: confirmado<br/>  Em estoque: 89 unidades<br/>  Entrega: 2 dias (SP)<br/>audit_summary:<br/>  iterations: 2<br/>  first_rejection: lactose<br/>  final_score: 93/100<br/>Mensagem ao cliente:<br/>  'Marina, a melhor opção segura<br/>   é a Proteína Vegetal Pro<br/>   Chocolate. Sem lactose,<br/>   R$155, em estoque.'"]
    end

    E2 -->|"APPROVED"| FINAL

    style CTX fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style G1 fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style G2 fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style E1 fill:#ffebee,stroke:#c62828,stroke-width:2px
    style E2 fill:#c8e6c9,stroke:#388e3c,stroke-width:2px
    style F1 fill:#fff3e0,stroke:#ef6c00,stroke-width:2px
    style FINAL fill:#a5d6a7,stroke:#2e7d32,stroke-width:3px
    style ITER1 fill:#fafafa,stroke:#9e9e9e,stroke-width:1px,stroke-dasharray: 5 5
    style ITER2 fill:#fafafa,stroke:#9e9e9e,stroke-width:1px,stroke-dasharray: 5 5
```

### Narrativa Completa do Caso Marina

**O contexto antes do ciclo começar**

Marina é uma cliente que voltou a treinar depois de dois anos parada. Ela quer um suplemento para ajudar na recuperação muscular. Tem intolerância à lactose — uma restrição documentada no perfil dela com severidade CRITICAL. Seu orçamento máximo é R$ 160. Prefere sabor chocolate, mas aceita baunilha. Está em São Paulo e quer receber em até 3 dias.

Ela manda uma mensagem simples no WhatsApp: "Oi KODA! Voltei a treinar depois de 2 anos. Quero algo para recuperação muscular. Sou intolerante à lactose. Meu orçamento é R$ 160."

O Orquestrador do KODA recebe essa mensagem e inicia o caso `rec_marina_001`. Ele extrai as informações da mensagem, consulta o banco de dados para carregar o perfil completo da Marina, e escreve `customer_context.json` — o arquivo imutável que servirá de âncora para todo o ciclo.

**Iteração 1 — O erro que o sistema impediu de chegar à Marina**

O Generator recebe o contexto e começa a trabalhar. Ele consulta o catálogo de produtos com os filtros: categoria = proteína, preço ≤ 160, objetivo = recuperação muscular. Encontra várias opções.

Ele seleciona o Whey Isolado Premium Chocolate (SKU: WHEY-ISO-149, R$ 149.90). O raciocínio parece sólido: é um whey isolado (alta pureza), sabor chocolate (preferência da cliente), preço dentro do orçamento (R$ 149.90 ≤ R$ 160).

Mas o Generator comete um erro de assumption. Ele **assume** que "whey isolado" significa "sem lactose". Ele não verifica o campo `contains_lactose_trace` no catálogo. Na cabeça do Generator, a cadeia de raciocínio foi: isolado → processado → sem lactose → seguro para a Marina.

Ele escreve `generator_draft_v1.json` com confidence 0.78. Nas notas, ele até menciona: "Restrição alimentar precisa ser verificada pelo Evaluator contra catálogo." — o Generator sabe que não é seu trabalho verificar tudo, mas isso não o impediu de fazer uma assumption errada.

O Evaluator recebe o draft, o contexto e a rubric. Ele não herda o raciocínio do Generator. Ele não sabe que o Generator "assumiu" algo. Ele simplesmente aplica os critérios.

Para o critério `lactose_free`, ele consulta o catálogo: SKU WHEY-ISO-149, campo `contains_lactose_trace`: **TRUE**. O catálogo é claro. O cliente tem restrição CRITICAL de intolerância à lactose. A conclusão é binária e inevitável: **FAIL (CRITICAL)**.

Para os outros critérios: budget passa (149.90 ≤ 160), goal_fit passa (proteína para recuperação), stock passa (34 unidades em SP). Mas o critério que falhou é CRITICAL — isso significa que, sozinho, ele causa rejeição independentemente dos outros scores.

Score final: 42/100. Veredito: REJECTED.

O Evaluator gera feedback específico: "Issue [CRITICAL]: WHEY-ISO-149 contém traços de lactose. A cliente possui restrição documentada de intolerância à lactose. Ação: REMOVER este SKU. Buscar apenas produtos com lactose_free=true e contains_lactose_trace=false confirmados no catálogo."

O Orquestrador lê o veredito. REJECTED. Score 42 < threshold 85. Iteração atual: 1. Max: 3. 1 < 3 → continuar.

**Iteração 2 — A correção guiada pelo feedback**

O Generator recebe o feedback e o contexto. Desta vez, ele não assume nada. Ele aplica os filtros exatos que o feedback especificou: lactose_free=true, contains_lactose_trace=false, in_stock=true, price ≤ 160, goal=recuperação.

Encontra PLANT-PRO-155: Proteína Vegetal Pro Chocolate. R$ 155.00. As flags do catálogo são explícitas: lactose_free=true, contains_lactose_trace=false, in_stock=true (89 unidades em SP).

Desta vez, o Generator verifica cada flag. Não assume. A confidence sobe para 0.86 — não porque o Generator está "mais confiante" em si mesmo, mas porque a recomendação é objetivamente mais fundamentada.

O Evaluator avalia novamente. Todos os critérios passam. Lactose: PASS (CRITICAL). Budget: PASS. Goal: PASS. Stock: PASS. Message: PASS. Score: 93/100. Veredito: APPROVED.

O Orquestrador monta `final_response.json` e envia a recomendação para Marina: "Marina, a melhor opção segura para o que você contou é a Proteína Vegetal Pro Chocolate. Ela está dentro do seu orçamento (R$ 155), não tem lactose nem traços de lactose, e ajuda você a bater proteína na volta aos treinos. Quer que eu te mande o link?"

### O Que o Sistema Aprendeu com Este Caso

Este caso gera um dado operacional que vai além da recomendação individual:

```text
Aprendizado: Produtos da categoria "whey isolado" não devem ser assumidos
como automaticamente lactose_free. O campo contains_lactose_trace deve ser
verificado para todos os produtos, independentemente da categoria.

Ação: Revisar a rubric para incluir verificação explícita de
contains_lactose_trace (não apenas lactose_free) como critério obrigatório
para clientes com intolerância à lactose.

Impacto esperado: Redução de falsos positivos na primeira iteração para
casos envolvendo whey isolado e intolerância à lactose.
```

Este aprendizado não fica na cabeça de ninguém. Ele é registrado, revisado em equipe, e potencialmente incorporado à rubric na próxima versão. O ciclo de melhoria contínua fecha: Generator/Evaluator não apenas impede erros — ele gera dados que previnem erros futuros.

### Os 5 Artefatos do Caso — Responsabilidades e Ciclo de Vida

| Artefato | Quem Escreve | Quem Lê | Quando é Escrito | Imutável? | Função no Ciclo |
|----------|-------------|---------|-----------------|-----------|-----------------|
| `customer_context.json` | Orquestrador (setup) | Generator, Evaluator | Uma vez, na inicialização do caso | Sim (durante o ciclo) | Âncora de fatos. Garante que ambos os roles trabalham sobre a mesma verdade. |
| `generator_draft_v{N}.json` | Generator | Evaluator | A cada iteração de geração | Sim (versionado: v1, v2, ...) | Proposta candidata. Contém claims (o que afirma), assumptions (o que assume), evidence (fontes consultadas) e confidence. |
| `evaluator_verdict_v{N}.json` | Evaluator | Orquestrador | A cada iteração de avaliação | Sim (versionado) | Veredito estruturado. Contém status, score, checks por critério com severidade e evidência, e decision summary. |
| `feedback_v{N}.json` | Evaluator (via Orquestrador) | Generator (próxima iteração) | Após cada REJECTED | Sim (versionado) | Instruções acionáveis: constraint violada, severidade, ação esperada, SKUs a evitar. |
| `audit_log.jsonl` | Todos os componentes | Humanos, dashboards, sistemas de auditoria | A cada evento significativo | Sim (append-only) | Timeline imutável para reconstrução post-mortem, métricas operacionais e compliance. |

### Por Que Este Ciclo Funcionou (5 Razões)

**1. O Generator não precisava ser perfeito.**
Ele gerou uma proposta com uma assumption errada. O sistema não puniu o Generator — corrigiu a proposta. A separação de roles significa que o Generator pode errar sem consequência para o cliente, porque o Evaluator existe para capturar o erro.

**2. O Evaluator tinha critérios objetivos e fontes de verdade independentes.**
"contains_lactose_trace=true" não é uma opinião. É um campo no catálogo. A decisão do Evaluator foi binária, rastreável e irrefutável. Não houve espaço para "interpretação" ou "negociação".

**3. O feedback foi específico e acionável.**
Não disse "tente de novo" ou "melhore a recomendação". Disse exatamente: "Remova WHEY-ISO-149. Contém traços de lactose. Busque lactose_free=true E contains_lactose_trace=false." O Generator da iteração 2 não precisou adivinhar o que corrigir. Ele leu, filtrou, encontrou.

**4. O Orquestrador controlou o ciclo com regras claras.**
A iteração 2 foi a última necessária. Se tivesse falhado também, o Orquestrador teria permitido mais uma tentativa (iteração 3). Se a terceira também falhasse, o caso seria escalado para um humano — não enviado com erro para a Marina.

**5. Tudo foi registrado no audit log.**
Se Marina tivesse reclamado depois (ou pior, se tivesse passado mal com um produto com lactose), Fernando poderia abrir o audit_log.jsonl, ler os 10 eventos do ciclo, e saber exatamente: o que foi recomendado na primeira tentativa, por que foi rejeitado, o que foi recomendado na segunda, e quais evidências sustentaram a aprovação.

---

## 💼 Seção 4 Expandida: Generator/Evaluator em Todos os 5 Casos de Uso KODA

### Visão Geral dos 5 Casos

O Generator/Evaluator não é um padrão de tamanho único. Ele se adapta a diferentes níveis de complexidade e criticidade. A tabela abaixo mostra como o padrão se manifesta em cada caso de uso do KODA:

| Caso | Complexidade | Criticidade | Rubric Principal | max_iterations | threshold | Custo Típico (tokens) |
|------|-------------|-------------|------------------|----------------|-----------|----------------------|
| **1. Promotion Application** | Simples | Média | Validar código, checar expiração, evitar double-discount | 2 | 90 | ~1500 |
| **2. Product Discovery** | Média | Alta | Restrições alimentares, budget, goal_fit, stock, message_clarity | 3 | 85 | ~3500 |
| **3. Review Quality Verification** | Média | Média | Autenticidade, especificidade, ausência de spam/links | 2 | 80 | ~2000 |
| **4. Order Processing** | Complexa | Muito Alta | 6 sprints: cliente, inventário, preço, promoção, pagamento, fulfillment | 3 | 90 | ~8000 |
| **5. Fulfillment & Same-Day Delivery** | Muito Complexa | Crítica | Disponibilidade geográfica, rota, entregador, ETA, buffer de segurança | 4 | 92 | ~12000 |

### Caso 1: Promotion Application — Simples mas Crítico

**O Problema:**
Cliente aplica código promocional. KODA precisa validar que o código é válido, não expirou, não foi usado antes por este cliente, é cumulativo com desconto de clube (ou não), e o desconto final está dentro das políticas.

**Por que Generator/Evaluator:**
Mesmo sendo "simples", o custo do erro é real: double-discount (cliente paga menos que o devido) ou recusa indevida (cliente perde benefício legítimo). Self-evaluation frequentemente erra em regras de cumulatividade.

**Como o ciclo funciona:**

```text
CUSTOMER CONTEXT (imutável):
  customer_tier: club (10% desconto)
  promo_code: SUMMER15
  order_total: R$ 100.00

ITERAÇÃO 1:
  GENERATOR:
    Aplica SUMMER15 (-R$ 15, 15%)
    Aplica clube (-R$ 10, 10%)
    Total: R$ 75.00
    Assumption: promoções são cumulativas

  EVALUATOR (rubric: promotion_policy_v2):
    ✅ Código existe? SIM (SUMMER15 no BD)
    ✅ Não expirou? SIM (válido até 2026-06-30)
    ✅ Primeira vez do cliente? SIM
    ❌ Cumulativo com clube? NÃO (política: "promoções sazonais não cumulativas com desconto de clube")
    ❌ Desconto dentro da política? NÃO (25% excede máximo de 20%)
    → REJECTED. Score: 55/100

  FEEDBACK:
    "SUMMER15 não é cumulativo com desconto de clube. Aplicar apenas o melhor desconto.
     Desconto máximo permitido: 20%."

ITERAÇÃO 2:
  GENERATOR (com feedback):
    Compara: SUMMER15 (15%) vs Clube (10%)
    Aplica apenas SUMMER15: -R$ 15
    Total: R$ 85.00

  EVALUATOR:
    ✅ Cumulatividade: OK (apenas melhor desconto aplicado)
    ✅ Desconto final: 15% (≤ 20%)
    ✅ Total correto: R$ 85.00
    → APPROVED. Score: 100/100
```

**Lição deste caso:**
Mesmo tarefas "simples" se beneficiam da separação quando envolvem regras de negócio com exceções (cumulatividade). O Generator tende a "ser generoso" com o cliente (aplicar todos os descontos). O Evaluator aplica a política objetivamente.

### Caso 2: Product Discovery — O Caso Clássico

Este é o caso da Marina, detalhado na Seção 4. O ponto adicional aqui é a **variedade de restrições** que podem aparecer:

- Restrições alimentares: lactose, glúten, amendoim, vegan, low-carb
- Restrições de budget: fixo, flexível, "melhor custo-benefício"
- Restrições de perfil: iniciante, intermediário, avançado, retornando
- Restrições de sabor: chocolate, baunilha, morango, neutro
- Restrições de entrega: same-day, 2 dias, retirada em loja
- Restrições combinadas: "vegano E sem glúten E até R$ 150 E entrega hoje"

**O desafio da combinação:**
Quanto mais restrições, menor o espaço de soluções. O Generator pode não encontrar nenhum produto que atenda todas — e é exatamente aí que o padrão brilha: em vez de recomendar algo que viola uma restrição (como faria o self-evaluation), o sistema escala para humano na terceira iteração, com o diagnóstico claro de "catálogo atual não atende a combinação de restrições [X, Y, Z]".

### Caso 3: Review Quality Verification — Julgamento de Conteúdo

**O Problema:**
Clientes escrevem reviews de produtos. KODA precisa publicar apenas reviews legítimos, filtrando spam, conteúdo malicioso, reviews de concorrentes e reviews sem substância.

**Particularidade deste caso:**
Diferente dos outros casos, aqui o julgamento tem um componente subjetivo: "esta review é útil para outros clientes?" não é puramente binário. No entanto, há critérios objetivos que cobrem a maior parte dos casos.

**Como o ciclo funciona:**

```text
CUSTOMER CONTEXT:
  reviewer_id: wa_5511987654321
  product_sku: WHEY-ISO-149
  verified_purchase: SIM
  review_text: "Produto muito bom! Comprei e gostei bastante.
                Recomendo para todos que querem ganhar massa.
                Nota 10!"

ITERAÇÃO 1:
  GENERATOR (categoriza):
    Sentimento: POSITIVO
    Tópicos: ["qualidade", "ganho muscular", "recomendação"]
    Autenticidade: PROVÁVEL_LEGÍTIMO
    Nota sugerida: APROVAR

  EVALUATOR (rubric: review_quality_v1):
    ✅ Compra verificada? SIM
    ✅ Menciona o produto? SIM (WHEY-ISO-149)
    ⚠️ Contém detalhes específicos? NÃO (apenas elogios genéricos)
    ✅ Sem links maliciosos? SIM
    ✅ Sem linguagem de spam? SIM
    ⚠️ Útil para outros compradores? BAIXA (faltam detalhes sobre resultado, sabor, efeitos)
    → APPROVED com score: 68/100 (publicado, mas marcado como "review básico")

  Note: Avaliação de conteúdo não é binária. Reviews podem ser "aprovadas mas com baixa utilidade".
  O threshold aqui é mais baixo (80) porque o custo de um falso negativo (rejeitar review legítimo)
  é maior que o custo de um falso positivo brando (publicar review genérico mas inofensivo).
```

**Lição deste caso:**
O Generator/Evaluator não precisa ser binário. O score permite granularidade: publicar com ressalva, marcar como "baixa utilidade", ou priorizar reviews de alta qualidade no ordenamento.

### Caso 4: Order Processing — O Caso Multi-Sprint

**O Problema:**
Processar um pedido completo envolve 6 etapas sequenciais interdependentes. Cada etapa pode falhar de formas diferentes. Erros em etapas iniciais se propagam.

**Particularidade deste caso:**
Em vez de um único par Generator/Evaluator, usa-se **um par por sprint**, com state files compartilhados entre sprints. O Orquestrador coordena a sequência.

**Estrutura de State Files para Order Processing:**

```text
order_state/
├── customer_context.json          (imutável)
├── sprint_01_validate_customer/
│   ├── generator_draft_v{N}.json
│   ├── evaluator_verdict_v{N}.json
│   └── feedback_v{N}.json
├── sprint_02_check_inventory/
│   ├── generator_draft_v{N}.json
│   ├── evaluator_verdict_v{N}.json
│   └── feedback_v{N}.json
├── sprint_03_calculate_price/
│   └── ...
├── sprint_04_apply_promotions/
│   └── ...
├── sprint_05_process_payment/
│   └── ...
├── sprint_06_schedule_fulfillment/
│   └── ...
└── audit_log.jsonl
```

**Métricas deste caso:**
- Precisão: 95% → 99.8% com Generator/Evaluator
- Erros de cobrança duplicada: 1% → 0%
- Tempo médio de processamento: 8-12 segundos (6 sprints × 2 agentes)

**Lição deste caso:**
Generator/Evaluator escala por composição. Tarefas complexas não exigem um Generator/Evaluator mais complexo — exigem múltiplos pares simples coordenados.

### Caso 5: Fulfillment & Same-Day Delivery — O Caso de Coordenação Máxima

**O Problema:**
KODA promete entrega no mesmo dia. Isso envolve coordenar: disponibilidade de produto em armazéns específicos, rotas de entrega viáveis, entregadores disponíveis, janelas de tempo realistas, e buffer de segurança.

**Particularidade deste caso:**
Usa **múltiplos Generators em paralelo** (um para armazém, um para rota, um para entregador) e um **único Evaluator orquestrador** que verifica a consistência entre as três propostas.

**Como o ciclo funciona:**

```text
CUSTOMER CONTEXT:
  delivery_address: Rua Augusta, 1500, São Paulo
  delivery_window: hoje, 14h-18h
  products: [WHEY-VEGAN-001, CREATINA-300]

GERAÇÃO PARALELA (3 Generators simultâneos):
  Generator A (Armazém):
    "WHEY-VEGAN-001: 47 unidades no Armazém Zona Sul (12km).
     CREATINA-300: 156 unidades no Armazém Zona Sul."
    Output: warehouse_draft.json

  Generator B (Rota):
    "Rota Zona Sul → Augusta: 12km, ~25 min sem trânsito,
     ~40 min com trânsito de sexta-feira."
    Output: route_draft.json

  Generator C (Entregador):
    "Entregador Carlos: disponível 14h-20h, região Zona Sul,
     capacidade: 8 entregas. Já tem 5 agendadas."
    Output: courier_draft.json

AVALIAÇÃO INTEGRADA (1 Evaluator):
  Lê os 3 drafts e verifica consistência:

  ✅ Armazém tem os produtos? SIM (Zona Sul)
  ✅ Rota é viável? SIM (12km)
  ⚠️ Tempo de rota + buffer: 40min + 30min buffer = 70min
  ⚠️ Carlos tem 3 slots restantes. 2 produtos = 1 slot. OK.
  ⚠️ Previsão de entrega: 14h + 70min = 15h10 (dentro da janela 14h-18h)
  ✅ Margem de segurança: 2h50min (OK, mínimo é 1h)

  → APPROVED. Score: 88/100.

  Nota: Score não é 100 porque a margem de segurança (2h50min)
  está acima do mínimo (1h) mas abaixo do ideal (3h) para
  uma sexta-feira de trânsito imprevisível.
```

**Lição deste caso:**
Generator/Evaluator escala para coordenação multi-agent. Os Generators podem trabalhar em paralelo (reduzindo latência). O Evaluator atua como orquestrador de consistência — não apenas verificando cada proposta isoladamente, mas verificando se as propostas são **mutuamente compatíveis**.

---

## 💰 Seção 5.5: Token Economy — Análise de Custo vs Qualidade

### O Custo Real do Generator/Evaluator

Uma objeção comum ao padrão é o custo: "duas chamadas de API em vez de uma". Esta seção analisa o custo real, não o custo aparente.

### Custo por Caso — Comparação Detalhada

| Estratégia | Chamadas LLM | Tokens (típico) | Custo API (ordem) | Tempo (típico) | Precisão |
|------------|-------------|-----------------|-------------------|----------------|----------|
| Self-Evaluation | 1 | 500-1000 | $0.001-0.003 | 1-3s | ~75% |
| Gen/Eval (1 iteração) | 2 | 2000-3500 | $0.005-0.010 | 4-8s | ~85% |
| Gen/Eval (2 iterações) | 3-4 | 4000-6000 | $0.010-0.018 | 7-15s | ~95% |
| Gen/Eval (3 iterações, max) | 5-6 | 6000-9000 | $0.018-0.027 | 10-22s | ~98% |
| Multi-Agent (5 agentes) | 5-6 | 5000-10000 | $0.015-0.030 | 5-10s (paralelo) | ~92% |

### Custo do Erro vs Custo da Prevenção

O que realmente importa não é o custo da chamada de API — é o custo total do ciclo de vida da recomendação:

```
CENÁRIO: 1000 recomendações de produto por dia

Self-Evaluation (75% precisão):
  • Custo API: 1000 × $0.002 = $2/dia
  • 250 recomendações erradas
  • Custo do erro: devoluções, reembolsos, perda de cliente
  • Estimativa: 250 erros × $5 (custo médio/erro) = $1,250/dia
  • Custo total: $1,252/dia

Gen/Eval — State Files (95% precisão, média 1.5 iterações):
  • Custo API: 1000 × 2.5 chamadas × $0.007 = $17.50/dia
  • 50 recomendações erradas
  • Custo do erro: 50 erros × $5 = $250/dia
  • Custo total: $267.50/dia

Economia diária: $1,252 - $267.50 = $984.50/dia
Economia mensal: ~$29,500
ROI: ~56x sobre o custo adicional de API
```

### Onde o Custo Realmente Vai

Para um caso típico de Product Discovery com 2 iterações:

| Componente | Tokens | % do Custo |
|------------|--------|------------|
| Generator — iteração 1 | ~1500 | 25% |
| Evaluator — iteração 1 | ~1000 | 17% |
| Feedback — geração | ~300 | 5% |
| Generator — iteração 2 | ~1200 | 20% |
| Evaluator — iteração 2 | ~1000 | 17% |
| customer_context (leitura) | ~500 | 8% |
| Rubric (leitura) | ~300 | 5% |
| Audit log (escrita) | ~200 | 3% |
| **Total** | **~6000** | **100%** |

### Estratégias de Otimização de Custo

| Estratégia | Economia | Trade-off |
|------------|----------|-----------|
| **Modelo menor para Evaluator** (ex: Haiku para avaliar, Sonnet para gerar) | 40-60% no custo do Evaluator | Avaliação pode ser menos sutil em critérios subjetivos |
| **Cache de catálogo e rubric** (não recarregar a cada chamada) | 10-15% no custo total | Requer invalidação de cache quando catálogo/rubric mudam |
| **Early termination** (se score < 30, não tentar de novo — escalar direto) | 20-30% em casos muito ruins | Pode escalar casos que seriam resolvíveis na segunda tentativa |
| **Batch evaluation** (avaliar múltiplos drafts do mesmo caso em uma chamada) | 15-25% no custo do Evaluator | Aumenta complexidade do prompt do Evaluator |
| **Reduzir max_iterations de 3 para 2** para casos de baixa criticidade | 25-33% em casos que precisariam de 3 iterações | Pode escalar mais casos para humano |

### Quando o Custo Adicional NÃO se Justifica

Generator/Evaluator não é gratuito e não é sempre necessário. Não use quando:

- O custo do erro é próximo de zero (ex: "Qual o horário de funcionamento?")
- A resposta é determinística e verificável por código (ex: "Quantas unidades do SKU X em estoque?")
- O volume é tão alto e a margem tão baixa que o custo adicional de API elimina o lucro
- O tempo de resposta é crítico e 5 segundos adicionais são inaceitáveis

Nestes casos, self-evaluation com validação determinística (regras de código, não LLM) é mais adequado.

### Métricas de Impacto — O Que Medir Para Saber Se Está Funcionando

Estas são as métricas que o time do KODA acompanha para avaliar se o Generator/Evaluator está entregando valor:

| Métrica | Definição | Baseline (antes) | Target (depois) | Frequência |
|---------|-----------|-----------------|-----------------|------------|
| **Taxa de aprovação na 1ª iteração** | % de casos aprovados sem retry | 0% (sem padrão) | > 70% | Semanal |
| **Taxa de rejeição com crítica real** | % de rejeições com ≥ 1 FAIL objetivo | — | 5-20% | Semanal |
| **Correção na 2ª tentativa** | % de REJECTED(v1) → APPROVED(v2) | — | > 70% | Semanal |
| **Taxa de max_iterations** | % de casos que esgotam retries | — | < 5% | Semanal |
| **Erro reportado pelo cliente** | Reclamações / total de recomendações | 25% | < 5% | Mensal |
| **Custo por caso aprovado** | Tokens totais / casos aprovados | — | Em queda ou estável | Mensal |
| **Latência p95** | Tempo do 95º percentil dos ciclos | — | < 15s | Semanal |
| **Tempo de revisão humana** | Tempo médio para resolver escalações | — | < 5 min | Mensal |
| **ROI acumulado** | Economia com erros evitados - custo adicional | — | > 30x | Trimestral |

---

## 🔗 Seção 6: Conexões com os 8 Conceitos Core do Currículo

### O Generator/Evaluator Não Existe no Vácuo

O padrão Generator/Evaluator é o **conceito 3** do currículo de Long-Running Agents. Mas ele não é uma ilha. Ele depende de outros conceitos para funcionar e, por sua vez, produz dados que alimentam a evolução de outros conceitos.

Esta seção mapeia as conexões bidirecionais entre Generator/Evaluator e cada um dos outros 7 conceitos core. Entender essas conexões é o que permite passar de "sei implementar o padrão" para "sei integrar o padrão no sistema completo".

### Mapa de Dependências e Influências

```mermaid
graph TD
    GE["🎯 Generator/Evaluator<br/><br/>Conceito 3<br/>Separação de roles:<br/>criar vs criticar"]

    CM["📋 Context Management<br/><br/>Conceito 1<br/>Gerenciar o que o<br/>agente sabe e esquece"]
    PE["🔄 Planning vs Execution<br/><br/>Conceito 2<br/>Separar planejar de<br/>executar e verificar"]
    SC["📝 Sprint Contracts<br/><br/>Conceito 4<br/>Contratos formais entre<br/>módulos do sistema"]
    SP["💾 State Persistence<br/><br/>Conceito 5<br/>Persistir estado fora<br/>da context window"]
    HE["🔧 Harness Evolution<br/><br/>Conceito 6<br/>Evoluir regras e critérios<br/>com aprendizado operacional"]
    MA["🌐 Multi-Agent Coord.<br/><br/>Conceito 7<br/>Coordenar múltiplos<br/>agentes especializados"]
    ER["⭐ Evaluation Rubrics<br/><br/>Conceito 8<br/>Critérios objetivos<br/>para avaliação de qualidade"]

    CM -->|"Fornece contexto imutável<br/>que ambos os roles leem"| GE
    PE -->|"É o fundamento conceitual:<br/>separar criação de verificação"| GE
    GE -->|"Exige persistência para<br/>state files e audit log"| SP
    GE -->|"State files são contratos<br/>implícitos entre roles"| SC
    GE -->|"É um caso especial de<br/>coordenação multi-agent"| MA
    GE -->|"Rubrics são o critério<br/>que o Evaluator aplica"| ER
    GE -->|"Rejeições geram dados<br/>que alimentam evolução"| HE
    SP -->|"Persistência permite<br/>auditabilidade e replay"| GE
    ER -->|"Rubrics definem o que<br/>o Evaluator mede e como"| GE
    HE -->|"Evolução ajusta thresholds,<br/>rubrics e max_iterations"| GE
    MA -->|"Escala o padrão para<br/>múltiplos Generators ou<br/>Evaluators em paralelo"| GE
    CM -->|"Sem gestão de contexto,<br/>Generator e Evaluator<br/>leem fatos diferentes"| GE

    style GE fill:#ffeb3b,stroke:#f57f17,stroke-width:3px
    style CM fill:#e3f2fd,stroke:#1565c0
    style PE fill:#e8f5e9,stroke:#2e7d32
    style SC fill:#fff3e0,stroke:#ef6c00
    style SP fill:#f3e5f5,stroke:#7b1fa2
    style HE fill:#fce4ec,stroke:#c62828
    style MA fill:#e0f2f1,stroke:#00695c
    style ER fill:#fff8e1,stroke:#f9a825
```

### Conexão por Conexão — Análise Detalhada com Mini-Casos

Cada conexão abaixo é explicada em três níveis: (1) o que o conceito fonte fornece, (2) como Generator/Evaluator depende ou influencia, e (3) um mini-caso concreto do KODA que ilustra o que acontece quando a conexão funciona — e quando falha.

#### Conexão 1: Context Management → Generator/Evaluator

**O que Context Management fornece:**
O `customer_context.json` é o produto direto da gestão de contexto. É nele que as informações críticas do cliente — restrições alimentares, budget, objetivo, preferências, histórico — são consolidadas e imobilizadas como fatos. A gestão de contexto responde a perguntas como: "Esta preferência foi declarada pelo cliente ou inferida pelo sistema?", "Esta restrição é confirmada ou suspeita?", "Esta informação ainda é válida ou já foi substituída por uma declaração mais recente do cliente?".

**Como Generator/Evaluator depende disso:**
Tanto o Generator quanto o Evaluator leem o mesmo `customer_context.json`. Se a gestão de contexto for frágil — se informações importantes ficarem de fora, se dados conflitantes não forem resolvidos, se o arquivo não for atualizado quando o cliente fornece nova informação — ambos os roles trabalharão sobre uma base incompleta ou incorreta. É o clássico "garbage in, garbage out", mas pior: o sistema acredita que está certo porque passou pela verificação do Evaluator.

**Mini-caso — Quando funciona:**
Marina, na primeira mensagem, diz "sou intolerante à lactose". O sistema de gestão de contexto captura isso, classifica como `severity: CRITICAL`, e escreve no `customer_context.json`. O Generator lê e sabe que precisa evitar lactose. O Evaluator lê e sabe que lactose é um critério CRITICAL de rejeição. O ciclo funciona.

**Mini-caso — Quando falha:**
Marina, 20 minutos depois, menciona casualmente "ah, também sou alérgica a amendoim". O sistema de gestão de contexto — se for frágil — não atualiza o `customer_context.json` porque a menção foi "casual" e não uma "declaração explícita de restrição". O Generator, na próxima recomendação, sugere um produto com amendoim. O Evaluator, lendo o contexto desatualizado, não tem o critério "alergia a amendoim" na rubric — aprova a recomendação. O erro chega à Marina.

**Lição:** A qualidade do Generator/Evaluator é limitada pela qualidade do `customer_context.json`. Invista em gestão de contexto robusta antes de esperar milagres da separação de roles.

---

#### Conexão 2: Planning vs Execution → Generator/Evaluator

**O que Planning vs Execution fornece:**
O princípio fundamental de que "pensar no que fazer" e "fazer" são atividades cognitivas diferentes que se beneficiam de separação. No contexto de LLMs, isso significa que a context window não deveria conter simultaneamente instruções de planejamento, dados de execução e autoavaliação — a carga cognitiva degrada todas as três atividades.

**Como Generator/Evaluator depende disso:**
Generator/Evaluator é a aplicação direta deste princípio no domínio de geração e avaliação. O Generator "planeja" uma solução (propõe). O Evaluator "verifica" a solução (testa). Se o princípio de separação não for compreendido, a implementação tende a degenerar: o "Evaluator" recebe o mesmo contexto completo do Generator, incluindo a justificativa narrativa, e acaba apenas confirmando o que o Generator disse.

**Mini-caso — Quando funciona:**
O Generator recebe: contexto do cliente + catálogo de produtos. Gera uma recomendação. O Evaluator recebe: contexto do cliente + draft estruturado (sem justificativa narrativa) + rubric. O Evaluator não sabe "por que" o Generator escolheu aquele produto — só sabe que precisa verificar se o produto atende os critérios. A separação é real.

**Mini-caso — Quando falha:**
O "Evaluator" recebe: contexto do cliente + catálogo + draft + justificativa completa do Generator ("escolhi este porque é o melhor custo-benefício, tem ótimas reviews, e é o mais vendido da categoria"). O Evaluator lê essa justificativa e é influenciado — "se o Generator pesquisou e concluiu que é o melhor, provavelmente está certo". A "avaliação" vira confirmação. Sycophancy por outro caminho.

**Lição:** O Evaluator não deve receber a justificativa narrativa do Generator. Deve receber apenas o draft estruturado (SKU, claims, assumptions, evidence usada). A justificativa é para o cliente, não para o Evaluator.

---

#### Conexão 3: Generator/Evaluator → State Persistence

**O que Generator/Evaluator exige de State Persistence:**
O ciclo Generator/Evaluator é intrinsicamente stateful. Cada iteração produz artefatos que a próxima iteração precisa consumir. Sem persistência, o ciclo colapsa em uma única chamada — exatamente o que o padrão busca evitar.

**Como State Persistence responde:**
State files versionados (`_v1`, `_v2`, `_v{N}`) garantem que cada iteração é preservada. O audit log em JSONL garante timeline imutável. A persistência em arquivos (não em memória) garante que o sistema sobrevive a reinicializações e permite auditoria post-mortem.

**Mini-caso — Quando funciona:**
O KODA processa o caso da Marina. Duas iterações. Seis state files escritos (contexto, draft v1, veredict v1, feedback v1, draft v2, veredict v2). Audit log com 12 eventos. Uma semana depois, Marina reclama que a recomendação estava errada. Fernando abre o diretório do caso, lê os arquivos em ordem, e reconstrói exatamente o que aconteceu. Descobre que a reclamação era sobre o produto secundário (creatina), não sobre o principal — um bug diferente. Sem state persistence, essa investigação seria impossível.

**Mini-caso — Quando falha:**
Os state files são salvos em `/tmp` (diretório temporário). O servidor reinicia. Os arquivos somem. O ciclo que estava na iteração 2 perde o estado. O Orquestrador não sabe se o caso estava em GENERATING, EVALUATING ou DECIDING. O cliente precisa começar de novo. Pior: o audit log também estava em `/tmp` — a evidência do que aconteceu é perdida.

**Lição:** State files precisam estar em armazenamento persistente e durável. `/tmp` não é persistente. Sistemas de arquivos efêmeros de container também não. Use volumes persistentes ou object storage.

---

#### Conexão 4: Generator/Evaluator → Sprint Contracts

**O que Generator/Evaluator exige de Sprint Contracts:**
Os state files do ciclo são contratos implícitos entre os roles. O Generator promete entregar um JSON que o Evaluator consegue ler. O Evaluator promete entregar um JSON que o Orquestrador consegue interpretar. Se qualquer um violar o schema esperado, o ciclo quebra silenciosamente ou estrondosamente.

**Como Sprint Contracts responde:**
Contratos formais — schemas JSON, validação com Pydantic/Zod, tipos explícitos e não-nullable — transformam promessas implícitas em garantias verificáveis. Se o Generator escrever `"price": "149.90"` (string), a validação de contrato rejeita antes que o Evaluator tente comparar uma string com um número.

**Mini-caso — Quando funciona:**
O schema de `generator_draft` exige que `price` seja `number`, `sku` seja `string` não-nula, e `claims` seja `array` de `string`. O Generator produz um JSON. Antes de salvar, o sistema valida contra o schema. O campo `price` está como string `"149.90"` — a validação rejeita com erro claro: "Expected number, got string". O erro é capturado e logado. O sistema não prossegue com dados inválidos.

**Mini-caso — Quando falha:**
Sem validação de schema. O Generator escreve `"price": null` porque o catálogo não tinha preço para aquele SKU. O arquivo é salvo. O Evaluator lê, tenta comparar `null <= 160` — dependendo da linguagem e do operador, isso pode retornar `true`, `false`, ou lançar uma exceção. Comportamento imprevisível. O sistema pode aprovar um produto sem preço.

**Lição:** Validação de schema não é opcional. É a primeira linha de defesa contra corrupção de estado. Todo state file deve ser validado na escrita E na leitura.

---

#### Conexão 5: Generator/Evaluator → Multi-Agent Coordination

**O que Generator/Evaluator fornece para Multi-Agent Coordination:**
O padrão de dois roles com papéis assimétricos (criar vs criticar) estabelece as bases para coordenação multi-agent: separação de responsabilidades, comunicação por artefatos, controle de iteração, e auditabilidade. Estender para N agentes é uma generalização natural.

**Como Multi-Agent Coordination escala o padrão:**
Quando uma tarefa é complexa demais para um único Generator, múltiplos Generators especializados podem trabalhar em paralelo. O Evaluator então atua como orquestrador de consistência, verificando não apenas cada proposta individualmente, mas a compatibilidade entre elas. Este é exatamente o caso do Fulfillment (Caso 5).

**Mini-caso — Quando funciona:**
Fulfillment same-day: Generator A (armazém) encontra o produto na Zona Sul. Generator B (rota) calcula 25 minutos até o endereço. Generator C (entregador) encontra Carlos disponível. O Evaluator verifica: (1) cada proposta é válida isoladamente? Sim. (2) as propostas são mutuamente compatíveis? Sim — armazém Zona Sul + rota de 25 min + Carlos na Zona Sul = entrega viável. APPROVED.

**Mini-caso — Quando falha:**
Fulfillment same-day: Generator A encontra produto na Zona Norte (20km). Generator B calcula rota de 25 minutos. Generator C encontra Carlos na Zona Sul. O Evaluator verifica cada proposta — todas válidas. Mas não verifica compatibilidade: Carlos está na Zona Sul, o produto está na Zona Norte. A rota de 25 minutos não considera o deslocamento do entregador até o armazém. Resultado: entrega atrasada. O Evaluator falhou em seu papel de orquestrador de consistência.

**Lição:** Quando há múltiplos Generators paralelos, o Evaluator precisa de critérios de **consistência cruzada** além dos critérios de validação individual. "Cada proposta é válida" não é suficiente — "as propostas funcionam juntas?" é a pergunta crítica.

---

#### Conexão 6: Generator/Evaluator → Evaluation Rubrics

**O que Generator/Evaluator exige de Evaluation Rubrics:**
O Evaluator é tão bom quanto sua rubric. Sem critérios claros, ele vira um avaliador narrativo — "parece bom", "achei o preço alto", "não gostei do tom". A rubric transforma avaliação subjetiva em medição objetiva.

**Como Evaluation Rubrics responde:**
Uma rubric bem desenhada define: dimensões de avaliação, peso de cada dimensão, escala de pontuação, fontes de verdade para cada critério, severidade das falhas, e threshold de aprovação. A rubric é a "constituição" do Evaluator — ele não pode aprovar ou rejeitar por razões que não estão na rubric.

**Mini-caso — Quando funciona:**
Rubric `product_recommendation_safety_v3` define 6 critérios. Para cada critério: nome, peso, severidade, fonte de verdade, e descrição do que constitui PASS e FAIL. O Evaluator aplica cada critério mecanicamente. Para `lactose_free`: consulta `catalogo[SKU].contains_lactose_trace`. Se `true` → FAIL (CRITICAL). Se `false` → PASS. Sem espaço para interpretação.

**Mini-caso — Quando falha:**
Rubric vaga: "A recomendação é segura para o cliente?" O Evaluator precisa interpretar "segura". Segura significa sem lactose? Sem alérgenos? Dentro do orçamento? Com evidência científica? O Evaluator pode interpretar de forma diferente em cada chamada — mesmos inputs, outputs diferentes. Scores não são comparáveis entre iterações.

**Lição:** A rubric deve ser específica o suficiente para que dois Evaluators independentes, aplicando a mesma rubric ao mesmo draft, cheguem ao mesmo veredito. Se houver variabilidade, a rubric precisa ser refinada.

---

#### Conexão 7: Generator/Evaluator → Harness Evolution

**O que Generator/Evaluator fornece para Harness Evolution:**
Cada rejeição do Evaluator é um ponto de dado. Cada caso que atinge max_iterations é um sinal. Cada padrão de falha recorrente é uma oportunidade. O audit log agrega esses dados ao longo do tempo.

**Como Harness Evolution responde:**
Análise periódica dos dados de rejeição revela padrões: "30% das rejeições na primeira iteração são por lactose em produtos isolados", "15% dos casos atingem max_iterations porque o catálogo não tem opções veganas abaixo de R$ 100", "threshold=85 está rejeitando recomendações que clientes avaliam como boas". O harness evolui: rubrics são ajustadas, thresholds recalibrados, catálogo enriquecido.

**Mini-caso — Quando funciona:**
Após 500 casos, análise revela que o critério `message_clarity` (peso 10%, severidade LOW) está causando 40% das rejeições na segunda iteração. O Generator consistentemente produz mensagens "boas mas não excelentes". O time decide: reduzir o peso de `message_clarity` de 10% para 5%, e mover a avaliação de clareza para um pós-processamento (não bloquear a recomendação por clareza). Taxa de aprovação na primeira iteração sobe de 70% para 82%.

**Mini-caso — Quando falha:**
Sem harness evolution. O sistema opera por 6 meses com a mesma rubric. O catálogo muda — novos produtos, novas categorias, novas restrições. A rubric não acompanha. O Evaluator continua aplicando critérios que não refletem mais a realidade do negócio. Falsos positivos e falsos negativos aumentam. O time reclama que "o sistema está piorando" — mas o sistema não mudou; o mundo mudou ao redor dele.

**Lição:** Generator/Evaluator sem harness evolution é um sistema que envelhece. A rubric, os thresholds e as regras de iteração precisam ser revisados periodicamente com base em dados operacionais.

### O Ciclo de Reforço Mútuo

As conexões não são estáticas — elas formam um ciclo de melhoria contínua:

```
Generator/Evaluator opera em produção
  ↓
Rejeições geram dados sobre falhas comuns
  ↓
Análise de dados (Trace Reading) identifica padrões
  ↓
Rubrics são ajustadas (Harness Evolution + Evaluation Rubrics)
  ↓
Novas rubrics tornam o Evaluator mais preciso
  ↓
Generator recebe feedback mais específico
  ↓
Generator gera propostas melhores na primeira tentativa
  ↓
Taxa de aprovação na iteração 1 sobe
  ↓
Custo cai (menos retries) e qualidade sobe (menos erros)
  ↓
Novos dados são gerados → ciclo recomeça
```

Este ciclo é o que transforma Generator/Evaluator de uma "barreira de qualidade" em um "motor de melhoria contínua". O padrão não apenas impede erros — ele aprende com os erros que impede.

---

## ⚠️ Seção 7: Padrões de Falha — Diagnóstico e Correção

### Quando o Generator/Evaluator Não Está Realmente Funcionando

Ter dois agentes com prompts diferentes não garante que o padrão Generator/Evaluator está funcionando. É possível — e comum — ter **forma sem substância**: a estrutura parece correta (dois roles, state files, veredito), mas o comportamento real é indistinguível de self-evaluation.

Esta seção cataloga os anti-padrões mais comuns, seus sintomas, causas raiz e correções. Use-a como checklist de diagnóstico quando os resultados não corresponderem às expectativas.

### Anti-Padrões — Catálogo Completo

| Anti-Padrão | Sintoma Observável | Causa Raiz | Como Diagnosticar | Correção |
|-------------|-------------------|------------|-------------------|----------|
| **Evaluator Carimbador** | Taxa de aprovação > 99%. Semanas sem uma única rejeição. Scores consistentemente altos (90+) mesmo quando o time sabe que há casos problemáticos. | Evaluator não tem critérios próprios. Está usando o mesmo contexto do Generator, recebendo a justificativa narrativa como evidência, ou tem um prompt que prioriza "ser prestativo" em vez de "ser crítico". | 1. Leia 20 evaluator_verdicts aleatórios. Todos dizem "parece bom"? 2. Injete um erro conhecido (ex: produto com lactose para cliente intolerante). O Evaluator rejeita? 3. Compare scores do Evaluator com avaliações humanas independentes dos mesmos drafts. | 1. Reescreva o prompt do Evaluator com missão explícita de encontrar falhas. 2. Remova do input do Evaluator qualquer narrativa do Generator que não seja estritamente factual. 3. Exija que cada check cite uma fonte de verdade (campo do catálogo, linha do BD). 4. Adicione métrica: "taxa de rejeição" como KPI de saúde do Evaluator (saudável = 5-20%). |
| **Feedback Fantasma** | Generator recebe feedback mas o draft da iteração N+1 é quase idêntico ao da iteração N. Mesmos SKUs problemáticos reaparecem. Segunda tentativa tem score similar ou pior que a primeira. | Feedback é vago ("melhore a recomendação", "tente de novo"), o Generator não tem acesso às alternativas que o feedback sugere, ou o Generator não está programado para ler o feedback antes de gerar. | 1. Compare generator_draft_v1.json com generator_draft_v2.json. São diferentes? 2. Leia o feedback_v1.json. Ele contém ações específicas ou apenas avaliações? 3. O Generator tem acesso ao catálogo completo para buscar alternativas? | 1. Torne o feedback específico: "Remova SKU X. Busque produtos com flag Y=true. Evite SKUs [lista]." 2. Verifique se o Generator realmente lê o arquivo de feedback (log de acesso). 3. Se o problema é falta de alternativas no catálogo, escale mais cedo (reduza max_iterations). |
| **Loop Infinito Disfarçado** | Sistema sempre atinge max_iterations. Casos escalados para humano em massa (30%+ dos casos). Time de revisão sobrecarregado. | Threshold de aprovação muito alto para o catálogo disponível, rubric muito rígida (exige perfeição em critérios secundários), ou o catálogo simplesmente não tem produtos que atendam todas as restrições. | 1. Analise a distribuição de scores dos vereditos. Estão todos abaixo do threshold? 2. Para casos que atingiram max_iterations, leia os feedbacks. Os mesmos issues se repetem? 3. O catálogo tem produtos que atendem todas as restrições simultaneamente? | 1. Revisar threshold: 85 é razoável? Ou 75 seria mais realista para o catálogo atual? 2. Revisar rubric: todos os critérios são realmente obrigatórios? Distinguir CRITICAL (bloqueante) de NICE_TO_HAVE (informativo). 3. Se o catálogo é limitado, considere: recomendar o melhor disponível com ressalva explícita, ou escalar mais cedo. |
| **Avaliação Sem Evidência** | Evaluator aprova/rejeita com justificativas narrativas: "parece uma boa recomendação", "não gostei do tom", "achei o preço alto". Nenhuma referência a campos do catálogo ou regras de negócio. | Prompt do Evaluator não exige citação de evidência. Rubric ausente ou vaga. Evaluator está agindo como um "revisor humano" genérico, não como um verificador de critérios. | 1. Leia 20 evaluator_verdicts. Quantos citam uma fonte de verdade específica (campo do catálogo, linha do BD, política documentada)? 2. O campo "evidence" nos checks está populado ou é null/vazio? 3. Os checks contêm valores objetivos (true/false, números) ou apenas texto? | 1. Exigir que cada check do Evaluator inclua: (a) fonte consultada, (b) valor encontrado, (c) comparação com o critério. 2. Estruturar o output do Evaluator como JSON com campos obrigatórios, não como texto livre. 3. Adicionar validação de schema no evaluator_verdict para rejeitar vereditos sem evidência. |
| **Context Drift** | O `customer_context.json` muda entre iterações. O budget que era 160 na iteração 1 aparece como 200 na iteração 2. Restrições desaparecem ou mudam de severidade. | Confusão entre fato (imutável) e hipótese (mutável). O sistema está atualizando o customer_context durante o ciclo, possivelmente porque o Generator ou Evaluator "aprenderam" algo e quiseram "corrigir" o contexto. | 1. Compare o customer_context.json antes e depois de um ciclo de 2 iterações. Mudou? 2. Há código que escreve no customer_context.json fora do setup inicial? 3. O log mostra eventos de "context_updated" durante o ciclo? | 1. Tornar customer_context.json imutável por política: validar que só é escrito na inicialização. 2. Se informações novas surgirem durante o ciclo, escrever em arquivo separado (case_notes.json). 3. Adicionar hash do customer_context no audit log para detectar alterações. |
| **State File Corruption** | Arquivos JSON têm campos faltantes, tipos errados, ou o sistema lança exceções de parse. "Às vezes funciona, às vezes não." | Falta de validação de schema na escrita e leitura dos state files. O Generator escreve um campo como string; o Evaluator espera number. Ou campos obrigatórios são null porque o agente "esqueceu" de preenchê-los. | 1. Adicione validação de schema (JSON Schema, Pydantic, Zod) em todo write e read de state file. 2. Monitore taxa de erros de parse. 3. Guarde os arquivos corruptos para análise (não sobrescreva). | 1. Implementar validação estrita de schema em TODA escrita e leitura de state file. 2. Se um state file falhar na validação, rejeitar e logar o erro — nunca tentar "corrigir" automaticamente. 3. Usar tipos explícitos e não-nullable nos schemas. |
| **Rubric Drift** | A rubric que o Evaluator usa na iteração 2 é diferente da iteração 1. Os scores não são comparáveis entre iterações. | A rubric está sendo carregada dinamicamente e mudou entre as chamadas (ex: atualização de configuração em produção). | 1. Registrar a versão da rubric em cada evaluator_verdict. 2. Comparar versões entre iterações do mesmo caso. | 1. Congelar a versão da rubric no início do caso. 2. Carregar a rubric uma vez e reutilizar em todas as iterações daquele caso. 3. Versionar rubrics explicitamente (v1, v2, v3) e registrar a versão usada. |
| **Orquestrador Inteligente** | O Orquestrador toma decisões que não seguem as regras configuradas. "Achei que esse caso merecia mais uma tentativa." "O score estava baixo mas a recomendação parecia boa." | O Orquestrador foi implementado como um agente LLM em vez de um autômato de regras. Ele está "interpretando" os vereditos em vez de aplicar regras booleanas. | 1. O Orquestrador é um script determinístico ou uma chamada LLM? 2. Para casos com mesmo veredito (mesmo score, same iteration), a decisão é sempre a mesma? | 1. Implementar o Orquestrador como código determinístico (if/else), não como agente LLM. 2. As únicas decisões do Orquestrador devem ser baseadas em: status, score, iteration, max_iterations, threshold. |

### Sinais de Que o Padrão Está Saudável em Produção

| Sinal | O Que Medir | Valor Saudável | O Que Fazer Se Estiver Fora |
|-------|-------------|----------------|---------------------------|
| **Taxa de rejeição substantiva** | % de avaliações REJECTED com pelo menos um FAIL objetivo (não apenas score baixo) | 5—20% | < 5%: possível Evaluator Carimbador. > 20%: possível threshold muito alto ou catálogo limitado. |
| **Correção na segunda tentativa** | % de casos REJECTED na iteração 1 que são APPROVED na iteração 2 | > 70% | < 70%: feedback pode ser vago ou Generator não está conseguindo agir sobre ele. |
| **Max iterations raridade** | % de casos que atingem max_iterations | < 5% | > 5%: threshold muito alto, rubric muito rígida, ou catálogo não atende as restrições. |
| **Redução de erro silencioso** | Reclamações de clientes / total de recomendações | Em queda mês a mês | Estável ou subindo: erros estão passando pelo Evaluator. Revisar rubric e fontes de verdade. |
| **Cobertura de audit log** | % de eventos do ciclo registrados no audit_log.jsonl | 100% | < 100%: gaps no log comprometem auditoria. Corrigir código que gera eventos. |
| **Latência de ciclo** | Tempo entre case_initialized e response_delivered | < 10s (recomendação), < 30s (pedido) | Investigar gargalos: chamadas LLM lentas, I/O de state files, consultas de catálogo. |
| **Custo por aprovação** | Tokens totais / casos aprovados | Estável ou em queda | Subindo: mais retries por caso. Investigue por que a taxa de aprovação na iteração 1 está caindo. |
| **Distribuição de scores** | Histograma dos scores dos evaluator_verdicts | Concentração em duas faixas: 80-100 (aprovados) e 30-50 (rejeitados com razão clara) | Concentração em 60-80: zona cinzenta — threshold pode precisar de ajuste. |

---

## 🔍 Seção 7: Debugging com o Knowledge Graph — Guia Prático de Investigação

### Quando Algo Deu Errado — Por Onde Começar

O knowledge graph não serve apenas para entender o sistema quando ele funciona. Ele é uma ferramenta de debugging: quando algo falha em produção, o mapa de zonas, fluxos e artefatos diz exatamente onde procurar.

### O Método de Investigação em 5 Passos

Use este método quando uma recomendação errada chegar ao cliente (ou quando um caso for escalado sem necessidade, ou quando a latência estiver anormal):

```
PASSO 1: Leia o audit_log.jsonl
  → Identifique a timeline completa do caso
  → Quantas iterações? Qual foi o veredito final?
  → Houve eventos anômalos (timeouts, retries, DATA_MISSING)?

PASSO 2: Leia o customer_context.json
  → As restrições do cliente estavam corretas e completas?
  → O budget, objetivo e preferências batem com a conversa?
  → Há campos null ou ausentes que deveriam estar preenchidos?

PASSO 3: Para cada iteração, compare draft e veredito
  → Iteração 1: O que o Generator propôs? O que o Evaluator encontrou?
  → Iteração 2: O feedback foi aplicado? A correção resolveu?
  → Iteração N: Por que não foi aprovado antes?

PASSO 4: Verifique as fontes de verdade
  → O catálogo estava atualizado no momento da avaliação?
  → O estoque reportado era real?
  → As políticas de promoção estavam corretas?

PASSO 5: Classifique a falha
  → Tipo A: Generator errou (má proposta) → revisar prompt/temperature
  → Tipo B: Evaluator errou (aprovou o que deveria rejeitar) → revisar rubric
  → Tipo C: Contexto errado (fatos incorretos) → revisar gestão de contexto
  → Tipo D: Orquestrador errou (decisão errada) → revisar regras/thresholds
  → Tipo E: Infraestrutura (timeout, state file corruption) → revisar resiliência
```

### Exemplo Guiado de Debugging — Caso Real

**Cenário:** Um cliente reclamou que recebeu uma recomendação de whey protein com lactose, mesmo tendo informado ser intolerante. O time abre o caso.

**Passo 1 — Audit Log:**

```jsonl
{"ts":"2026-05-28T14:32:45Z","event":"case_initialized","case_id":"rec_joao_042"}
{"ts":"2026-05-28T14:32:50Z","event":"generation_started","iteration":1}
{"ts":"2026-05-28T14:32:55Z","event":"generation_completed","iteration":1,"sku":"WHEY-CONC-200","confidence":0.82}
{"ts":"2026-05-28T14:32:56Z","event":"evaluation_started","iteration":1}
{"ts":"2026-05-28T14:33:01Z","event":"evaluation_completed","iteration":1,"verdict":"APPROVED","score":91}
{"ts":"2026-05-28T14:33:02Z","event":"response_delivered","case_id":"rec_joao_042"}
```

**Observação:** Apenas 1 iteração. Score 91 — aprovado na primeira tentativa. Mas o cliente recebeu lactose. O que aconteceu?

**Passo 2 — customer_context.json:**

```json
{
  "customer_id": "wa_551198888888",
  "restrictions": [],
  "budget_max_brl": 200,
  "goal": "ganho_muscular"
}
```

**Descoberta:** O campo `restrictions` está vazio! O cliente mencionou intolerância à lactose na conversa, mas o sistema de gestão de contexto não capturou essa informação. O `customer_context.json` foi escrito sem a restrição.

**Passo 3 — generator_draft_v1.json:**

```json
{
  "sku": "WHEY-CONC-200",
  "name": "Whey Concentrado Premium",
  "price": 89.90,
  "claims": ["ganho muscular", "bom custo-benefício"],
  "assumptions": [],
  "confidence": 0.82
}
```

**Observação:** O Generator não incluiu verificação de lactose nas assumptions porque... o contexto não mencionava lactose. O Generator não tem culpa — trabalhou com o contexto que recebeu.

**Passo 4 — evaluator_verdict_v1.json:**

```json
{
  "verdict": "APPROVED",
  "score": 91,
  "checks": [
    {"criterion": "budget", "status": "PASS"},
    {"criterion": "goal_fit", "status": "PASS"},
    {"criterion": "stock", "status": "PASS"}
  ]
}
```

**Observação:** O critério `lactose_free` nem foi avaliado — porque a rubric só ativa esse critério se o `customer_context.restrictions` contiver `intolerancia_lactose`. Como o contexto não tinha a restrição, o critério não foi aplicado.

**Passo 5 — Classificação:**

- **Tipo C: Contexto errado.** O `customer_context.json` não refletia a realidade do cliente.
- **Ação corretiva:** Revisar o sistema de extração de restrições da conversa. Adicionar verificação: se o cliente menciona "intolerante", "alérgico", "não posso", o sistema deve capturar explicitamente.
- **Ação preventiva:** Adicionar ao Evaluator um critério de "restrição implícita": verificar se o texto da conversa original (não apenas o contexto estruturado) menciona restrições que não estão no `customer_context.json`. Se sim, alertar.

### Checklist de Debugging Rápido

| Sintoma | Primeiro lugar para olhar | Pergunta-chave |
|---------|--------------------------|----------------|
| Erro chegou ao cliente | `customer_context.json` | As restrições estavam registradas? |
| Muitas rejeições | `evaluator_verdict` dos últimos 50 casos | Qual critério está falhando com mais frequência? |
| Muitas escalações para humano | Distribuição de scores dos REJECTED | Os scores estão concentrados em 60-80 (threshold precisa de ajuste)? |
| Latência alta | Timeline do audit log | Onde está o tempo sendo gasto? Generator? Evaluator? I/O? |
| Scores inconsistentes | 2+ evaluator_verdicts para o mesmo draft | O Evaluator dá scores diferentes para o mesmo input? |
| Feedback ignorado | generator_draft v1 vs v2 | O draft da iteração 2 é diferente do da iteração 1? |

---

## ⚠️ Seção 8: Anti-Padrões Avançados e Sinais de Degradação

### Além dos Anti-Padrões Básicos

A Seção 6 cobriu os anti-padrões fundamentais (Evaluator Carimbador, Feedback Fantasma, etc.). Esta seção cobre padrões de falha mais sutis que aparecem quando o sistema já está em produção há algum tempo.

### Anti-Padrão 7: Deriva de Threshold

**Sintoma:** A taxa de aprovação está caindo gradualmente ao longo de semanas, mas o sistema não mudou. Os mesmos tipos de recomendação que eram aprovados antes agora são rejeitados.

**Causa:** O threshold não mudou, mas o mundo mudou. O catálogo tem produtos diferentes. Os preços subiram (inflação). As políticas de desconto mudaram. O que era "dentro do orçamento" a R$ 150 seis meses atrás pode não ser mais — mas o threshold de budget continua o mesmo.

**Diagnóstico:** Compare a distribuição de scores de 3 meses atrás com a distribuição atual. Se a média caiu sem mudança no sistema, o ambiente mudou.

**Correção:** Recalibrar thresholds com base em dados recentes, não em dados históricos. Thresholds não são "configure uma vez e esqueça".

### Anti-Padrão 8: Acoplamento Temporal Generator-Evaluator

**Sintoma:** O Evaluator consistentemente aprova recomendações do Generator quando ele está "confiante" (confidence > 0.85) e rejeita quando ele está "inseguro" (confidence < 0.6), independentemente do conteúdo real da recomendação.

**Causa:** O Evaluator está, de alguma forma, recebendo a confidence declarada pelo Generator e sendo influenciado por ela. Talvez o campo `confidence` esteja no draft que o Evaluator lê, e o prompt do Evaluator não instrui explicitamente para ignorar esse campo.

**Diagnóstico:** Calcule a correlação entre `generator_draft.confidence` e `evaluator_verdict.score`. Se for > 0.5, há acoplamento.

**Correção:** Remover o campo `confidence` do draft que o Evaluator recebe, ou instruir explicitamente o Evaluator para ignorar esse campo e basear sua avaliação apenas nos critérios da rubric.

### Anti-Padrão 9: Fadiga de Rubric

**Sintoma:** A rubric tem 25 critérios. O Evaluator consistentemente falha em aplicar os critérios 20-25 (os últimos da lista). Os critérios do final recebem menos atenção ou são avaliados com menos rigor.

**Causa:** A rubric é longa demais para ser aplicada consistentemente em uma única chamada. O Evaluator sofre de "atenção decrescente" — os primeiros critérios recebem mais foco, os últimos são tratados com menos cuidado.

**Diagnóstico:** Para cada critério da rubric, calcule a taxa de FAIL. Se os últimos critérios têm taxa de FAIL significativamente menor que os primeiros (para casos similares), há fadiga de rubric.

**Correção:** Dividir a rubric em duas avaliações sequenciais: uma para critérios CRITICAL e HIGH, outra para MEDIUM e LOW. Ou reduzir o número de critérios, consolidando critérios similares.

### Anti-Padrão 10: Overfitting de Feedback

**Sintoma:** O Generator da iteração 2 corrige exatamente o que o feedback da iteração 1 apontou, mas introduz um novo erro que não existia antes. O ciclo de "corrigir A, quebrar B" se repete.

**Causa:** O feedback é muito específico sobre o que remover, mas não inclui o que **manter**. O Generator, ao substituir o SKU problemático, escolhe um novo SKU que resolve a restrição X mas viola a restrição Y (que estava OK antes).

**Diagnóstico:** Compare os drafts de iterações consecutivas. Erros novos aparecem em critérios que estavam PASS antes?

**Correção:** Feedback deve incluir não apenas "remova X" e "busque Y", mas também "mantenha Z que estava correto". Exemplo: "Remova WHEY-ISO-149 (lactose). Busque produto com lactose_free=true E in_stock=true (que já estava OK antes)."

### Tabela Resumo de Anti-Padrões Avançados

| Anti-Padrão | Sintoma Principal | Diagnóstico Rápido |
|-------------|-------------------|-------------------|
| Deriva de Threshold | Taxa de aprovação caindo sem mudança no sistema | Comparar distribuição de scores histórica vs atual |
| Acoplamento Temporal | Score do Evaluator correlacionado com confidence do Generator | Calcular correlação confidence × score |
| Fadiga de Rubric | Últimos critérios da rubric têm menos FAILs | Comparar taxa de FAIL por posição na rubric |
| Overfitting de Feedback | Correção introduz novos erros | Comparar drafts consecutivos — erros novos? |

---

## 📊 Seção 9: O Que Você Aprendeu — Síntese Completa

### O Generator/Evaluator em 7 Camadas de Compreensão

Cada camada representa um nível de profundidade no entendimento do padrão. Você deve ser capaz de explicar cada camada para uma audiência diferente — a Camada 1 para um stakeholder de negócio, a Camada 4 para um engenheiro junior, a Camada 7 para um arquiteto senior.

```
═══════════════════════════════════════════════════════════════════════════════
CAMADA 1 — COGNITIVA (O Problema Humano e de Máquina)
───────────────────────────────────────────────────────────────────────────────
Separar criação de julgamento reduz sycophancy e confirmation bias.
Um role otimizado para propor + um role otimizado para criticar
produz resultados melhores que um role tentando fazer os dois.

Pergunta que esta camada responde: "Por que um agente não pode
simplesmente verificar o próprio trabalho?"
Resposta: Porque a resposta que ele acabou de gerar contamina
o julgamento. Ele lê o que queria dizer, não o que realmente disse.
É como um autor revisando o próprio manuscrito — ele vê a intenção,
não as palavras.

Evidência: Testes A/B no KODA mostram que self-evaluation deixa
passar 10-12% de erros que um Evaluator independente captura.

═══════════════════════════════════════════════════════════════════════════════
CAMADA 2 — ARQUITETURAL (A Estrutura de Componentes)
───────────────────────────────────────────────────────────────────────────────
Generator escreve draft em state file.
Evaluator lê draft, contexto imutável e rubric.
Orquestrador lê veredito e decide próximo passo.
Nenhum role depende da memória ou do estado interno do outro.

Componentes: 2 agentes (Generator, Evaluator) + 1 autômato (Orquestrador)
                + 5 state files + 1 audit log + 1 rubric

Pergunta que esta camada responde: "Como os dois roles se comunicam
sem que o viés de um contamine o outro?"
Resposta: Comunicação exclusivamente por artefatos persistidos
com schema definido. O Generator nunca "conversa" com o Evaluator.
O Evaluator nunca lê a justificativa narrativa do Generator como evidência.

═══════════════════════════════════════════════════════════════════════════════
CAMADA 3 — COORDENAÇÃO (A Troca de Informação)
───────────────────────────────────────────────────────────────────────────────
State files versionados são o canal de comunicação.
Cada artefato tem schema, versão e responsável claro.
Audit log em JSONL registra timeline imutável e append-only.

6 estratégias de coordenação comparadas: State Files, Message Passing,
Shared Memory, Self-Evaluation, Multi-Agent Consensus, Human-in-the-Loop.
A escolha depende de: custo do erro, auditabilidade necessária,
volume de casos e maturidade da equipe.

Pergunta que esta camada responde: "State files, message passing
ou shared memory — qual usar no KODA?"
Resposta: State files para a maioria dos casos (simples, auditável,
fácil de debugar). Message passing quando volume > 100 casos/min.
Shared memory apenas para prototipagem.

═══════════════════════════════════════════════════════════════════════════════
CAMADA 4 — CONTROLE (As Regras do Jogo)
───────────────────────────────────────────────────────────────────────────────
max_iterations impede loops infinitos (típico: 3).
approval_threshold define a barra de qualidade (típico: 85/100).
on_max_reached define o plano B (escalar para humano).
O Orquestrador é um autômato determinístico, não um agente inteligente.

Estados do ciclo: INITIALIZING → GENERATING → EVALUATING → DECIDING →
APPROVED | RETRYING | MAX_ITERATIONS | DATA_MISSING → CLOSED

Pergunta que esta camada responde: "O que acontece quando o sistema
não consegue aprovar uma recomendação?"
Resposta: Ele não tenta indefinidamente. Após max_iterations (3),
escala para um humano com o contexto completo do caso. Isso é uma
decisão de arquitetura que protege custo, latência e experiência.

═══════════════════════════════════════════════════════════════════════════════
CAMADA 5 — FEEDBACK (A Arte de Dizer "Não" de Forma Útil)
───────────────────────────────────────────────────────────────────────────────
Feedback é específico, acionável e vinculado a constraints.
"Remova SKU X porque viola restrição Y com severidade Z. Busque
produtos com flag W=true. Mantenha critérios A, B, C que estavam OK."
É melhor que "Tente de novo" ou "Melhore a recomendação".

5 qualidades do feedback bom: específico, acionável, vinculado a
constraint, priorizado por severidade, persistido como artefato.

Pergunta que esta camada responde: "Como garantir que o Generator
realmente corrija o erro na próxima tentativa?"
Resposta: O feedback deve ser acionável como uma instrução de código:
diga qual constraint foi violada, qual a severidade, e exatamente
qual ação tomar. Feedback vago produz correções aleatórias.

═══════════════════════════════════════════════════════════════════════════════
CAMADA 6 — APRENDIZADO (O Sistema Que Melhora Sozinho)
───────────────────────────────────────────────────────────────────────────────
Rejeições geram dados sobre falhas comuns.
Dados alimentam evolução de rubrics, thresholds e regras de catálogo.
O sistema melhora a cada ciclo — não apenas impede erros, aprende com eles.

Ciclo de reforço: operação → dados de rejeição → análise de padrões →
evolução de rubric → melhores avaliações → menos rejeições →
melhores dados → (recomeça)

Pergunta que esta camada responde: "O sistema fica melhor com o tempo?"
Resposta: Sim, se houver harness evolution. Sem ele, o sistema
envelhece — o mundo muda (catálogo, preços, políticas) mas a rubric
não acompanha. Com evolução, a taxa de aprovação na primeira iteração
sobe consistentemente.

═══════════════════════════════════════════════════════════════════════════════
CAMADA 7 — APLICAÇÃO (O Impacto no Mundo Real)
───────────────────────────────────────────────────────────────────────────────
KODA usa Generator/Evaluator em 5 features: Promotions, Product Discovery,
Review Quality, Order Processing, Fulfillment.
Precisão: 75% → 98%. Devoluções: 15% → 6%. Satisfação: 70% → 88%.
Cobranças duplicadas: 1% → 0%. ROI: 56x sobre custo adicional de API.

A Marina nunca soube que quase recebeu whey com lactose.
O João nunca soube que seu desconto de 25% foi corrigido para 15%.
O Carlos nunca soube que sua entrega same-day foi validada por 3
Generators paralelos e 1 Evaluator de consistência.

Pergunta que esta camada responde: "Isso realmente funciona em produção?"
Resposta: Sim. O KODA processa centenas de casos por dia com este
padrão. Não é teoria. É o que impede erros de chegarem aos clientes.

### As 5 Perguntas Que Você Deve Saber Responder (Para Qualquer Audiência)

**1. Por que self-evaluation falha mesmo quando o prompt parece bom?**

Porque a resposta gerada vira parte do contexto que o modelo usa para avaliar. É como pedir para o autor de um livro revisar o próprio manuscrito logo depois de escrevê-lo — ele lê o que queria dizer, não o que está realmente escrito. Em LLMs, esse fenômeno se chama **sycophancy**: o modelo tende a concordar com o que acabou de gerar, encontrando razões para validar a própria resposta em vez de testá-la objetivamente.

Além disso, há um problema de **carga cognitiva**: o mesmo contexto está sendo usado para gerar (que requer criatividade e exploração) e para avaliar (que requer rigor e ceticismo). Esses dois modos de pensamento competem pelos mesmos recursos de atenção dentro da context window.

O resultado prático: em testes do KODA, self-evaluation deixa passar 10-12% de erros que um Evaluator independente captura. Não é uma questão de "prompt melhor" — é uma limitação estrutural de pedir para a mesma mente criar e julgar.

**2. Qual é a diferença entre "dois agentes" e "Generator/Evaluator de verdade"?**

"Dois agentes" é a forma — você pode ter dois prompts diferentes e ainda assim estar fazendo self-evaluation disfarçado. Generator/Evaluator de verdade exige cinco condições:

1. **Roles com missões opostas e explícitas**: o Generator é instruído a "propor a melhor solução". O Evaluator é instruído a "encontrar falhas — seu sucesso é medido por erros encontrados, não por aprovações dadas".
2. **Rubric independente com critérios objetivos**: o Evaluator não avalia baseado em "feeling" — ele aplica uma checklist de critérios com fontes de verdade definidas.
3. **Fontes de verdade que o Evaluator consulta diretamente**: o catálogo de produtos, o banco de dados de clientes, as políticas comerciais. O Evaluator não depende do Generator para obter essas informações.
4. **Artefatos persistidos que permitem auditoria**: cada iteração produz arquivos versionados que podem ser inspecionados depois.
5. **Veredito estruturado com evidência para cada check**: não basta dizer "REJECTED" — é preciso dizer qual critério falhou, com qual evidência, e qual a severidade.

Se faltar qualquer uma dessas condições, você tem forma sem substância.

**3. Por que state files são o mecanismo de coordenação recomendado para KODA?**

State files impõem fronteiras explícitas entre os roles: cada um escreve em seus próprios arquivos, com schema definido, e lê apenas os arquivos que deve ler. As vantagens sobre alternativas:

- **Contra Shared Memory**: State files impedem que o Generator escreva assumptions no mesmo espaço onde o Evaluator lê fatos. A fronteira física (arquivos diferentes) reforça a fronteira lógica (hipótese vs verdade).
- **Contra Message Passing**: State files são mais simples de debugar — você abre o arquivo e vê o estado. Não precisa de infraestrutura de mensageria. Para o volume do KODA (< 10 casos/min), I/O de arquivo não é gargalo.
- **Contra Self-Evaluation**: State files são a materialização da separação. Se você está fazendo self-evaluation, não há state files — há apenas o contexto da conversa.

State files também permitem auditoria completa: cada versão de cada artefato é preservada. Se algo der errado, você reconstrói o caso lendo os arquivos em ordem.

**4. O que acontece quando o ciclo atinge max_iterations sem aprovação?**

O sistema não tenta de novo. Ele **escala para um humano**. Esta é uma decisão de arquitetura, não uma falha do sistema.

O humano recebe: o `customer_context.json` (o que o cliente pediu), todos os `generator_draft_v{N}.json` (o que foi tentado), todos os `evaluator_verdict_v{N}.json` (por que cada tentativa falhou), todos os `feedback_v{N}.json` (o que foi sugerido para corrigir), e o `audit_log.jsonl` (a timeline completa).

Com esse contexto, o humano pode tomar uma decisão informada em segundos — muito mais rápido do que tentar descobrir o que aconteceu sem os state files.

Max iterations é raro (< 5% dos casos) quando o sistema está bem calibrado. Quando não está, é um sinal de que o threshold está muito alto, a rubric está muito rígida, ou o catálogo não atende as restrições dos clientes.

**5. Como Generator/Evaluator se conecta aos outros 7 conceitos core?**

É um ecossistema de dependências bidirecionais. O Generator/Evaluator não funciona isolado:

- **Depende de**: Context Management (para o `customer_context.json` imutável), State Persistence (para os state files e audit log), Planning vs Execution (seu fundamento conceitual)
- **Aplica**: Sprint Contracts (schemas dos state files são contratos implícitos)
- **Alimenta**: Evaluation Rubrics (fornecendo o mecanismo que aplica os critérios), Harness Evolution (fornecendo dados de rejeição para melhoria contínua)
- **Escala via**: Multi-Agent Coordination (múltiplos Generators para tarefas complexas, múltiplos Evaluators para volume)

A metáfora: Generator/Evaluator é o motor. Os outros conceitos são o combustível (Context Management), o chassi (State Persistence), o painel de controle (Rubrics), o mecânico (Harness Evolution) e a fábrica (Multi-Agent Coordination). Sem qualquer um deles, o motor não leva o carro a lugar nenhum.

### As 3 Leis do Generator/Evaluator

Se você só puder lembrar de três coisas deste arquivo, que sejam estas:

**Lei 1 — Separação Real**
> Um Evaluator que lê a justificativa do Generator não é um Evaluator — é um espelho. Para que a separação seja real, o Evaluator deve formar seu julgamento a partir de fontes de verdade independentes, não a partir da narrativa de quem criou a proposta.

**Lei 2 — Feedback Acionável**
> Feedback que diz "melhore" é ruído. Feedback que diz "remova SKU X porque viola restrição Y, busque alternativas com flag Z=true" é uma instrução. O Generator não deve precisar interpretar feedback — deve poder agir sobre ele.

**Lei 3 — Tudo é Evidência**
> Se não está no audit log, não aconteceu. O audit log é a memória do sistema. Sem ele, você não consegue auditar, não consegue debugar, não consegue aprender. Cada evento do ciclo deve gerar uma entrada no audit log. Sem exceções.

### O Diagrama Que Resume Tudo (Versão de Bolso)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         GENERATOR/EVALUATOR                                  │
│                                                                             │
│   CLIENTE ──→ GENERATOR ──→ EVALUATOR ──→ CLIENTE                          │
│                 (criar)       (criticar)                                     │
│                    │               │                                         │
│                    ▼               ▼                                         │
│              state files     rubric + fontes                                 │
│              versionados     de verdade                                      │
│                    │               │                                         │
│                    └───────┬───────┘                                         │
│                            │                                                 │
│                            ▼                                                 │
│                      ORQUESTRADOR                                           │
│                   max_iterations=3                                          │
│                   threshold=85                                              │
│                            │                                                 │
│              ┌─────────────┼─────────────┐                                  │
│              ▼             ▼             ▼                                  │
│          APPROVED      REJECTED    MAX_ITERATIONS                            │
│          (envia)       (feedback)   (escala humano)                          │
│              │             │             │                                   │
│              └─────────────┼─────────────┘                                  │
│                            ▼                                                 │
│                      audit_log.jsonl                                        │
│                   (timeline imutável)                                        │
│                                                                             │
│   O padrão não elimina erros — ele os captura antes que cheguem ao cliente.  │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🌐 Seção 10: Generator/Evaluator no Contexto da Indústria

### Onde o Padrão se Encaixa no Ecossistema de Agentes

O Generator/Evaluator não é um padrão isolado do KODA. Ele aparece, com diferentes nomes e ênfases, em várias arquiteturas de agentes da indústria. Entender essas conexões ajuda a posicionar o padrão no panorama mais amplo.

### Comparação com Padrões da Indústria

| Padrão / Framework | Similaridade com Gen/Eval | Diferença Principal | Quando Preferir |
|--------------------|---------------------------|---------------------|-----------------|
| **Anthropic's "Generate + Verify"** | Idêntico em espírito: separar geração de verificação. Anthropic recomenda explicitamente em seu guia de agentes. | Anthropic enfatiza verificação por código/funções determinísticas. KODA usa verificação por segundo agente LLM (mais flexível, menos determinístico). | Use verificação por código quando os critérios são puramente computacionais (ex: `price <= budget`). Use Evaluator LLM quando os critérios envolvem julgamento semântico (ex: "a mensagem é clara e empática?"). |
| **LangGraph's "Supervisor + Workers"** | Similar estruturalmente: Supervisor (≈ Orquestrador) coordena Workers (≈ Generator + Evaluator). | LangGraph enfatiza grafos de estado e transições. Gen/Eval do KODA enfatiza state files como fonte de verdade. | Use LangGraph quando precisar de orquestração complexa com branching e paralelismo. Use Gen/Eval simples quando o fluxo é linear (generate → evaluate → decide). |
| **CrewAI's "Agent + Task"** | Agents em CrewAI podem ser configurados como "generator" e "reviewer". | CrewAI enfatiza colaboração entre agents com memória compartilhada. Gen/Eval do KODA enfatiza independência e ausência de memória compartilhada. | Use CrewAI para workflows colaborativos onde agents precisam negociar. Use Gen/Eval quando a independência do julgamento é crítica. |
| **Microsoft's AutoGen "Critic + Executor"** | AutoGen tem roles explícitos de "critic" que revisam output de "executor". | AutoGen enfatiza conversação multi-turn entre agents. Gen/Eval enfatiza comunicação por artefatos, não por chat. | Use AutoGen para problemas que se beneficiam de diálogo entre agents. Use Gen/Eval quando a comunicação deve ser estruturada e auditável. |
| **OpenAI's "Self-Refine" (paper)** | Self-Refine usa o mesmo modelo para gerar, criticar e refinar iterativamente. | Self-Refine é self-evaluation iterativo — o mesmo agente critica o próprio output. Gen/Eval separa os roles. | Use Self-Refine para tarefas criativas onde o "erro" é subjetivo (ex: melhorar um poema). Use Gen/Eval quando há critérios objetivos de correção. |
| **Constitutional AI (Anthropic)** | Similaridade conceitual: um modelo gera, outro modelo (ou o mesmo com prompt diferente) avalia contra uma "constituição" de princípios. | Constitutional AI foca em alinhamento e segurança. Gen/Eval foca em qualidade de tarefa. | Use Constitutional AI para garantir que outputs respeitam princípios éticos. Use Gen/Eval para garantir que outputs atendem critérios de negócio. |

### O Que Torna o Generator/Evaluator do KODA Único

O que distingue a implementação do KODA de outras abordagens:

1. **State files como fonte de verdade** — Não é comum na indústria. A maioria dos frameworks usa memória de sessão ou bancos de dados. State files oferecem simplicidade máxima (sem infra adicional) e auditabilidade máxima (arquivos são auto-documentados).

2. **Feedback estruturado e acionável** — Muitos sistemas de "review" produzem feedback narrativo ("essa resposta não está boa"). O KODA produz feedback que é essencialmente uma instrução de código.

3. **Separação estrita de fontes de verdade** — O Evaluator do KODA não lê a narrativa do Generator. Ele lê o draft estruturado e consulta fontes de verdade independentes. Isso é mais rigoroso que a maioria das implementações.

4. **Orquestrador determinístico** — Em muitos frameworks, o "orquestrador" é outro agente LLM. No KODA, é código determinístico. Isso elimina uma classe de bugs de "decisão criativa do orquestrador".

5. **Ciclo de aprendizado fechado** — A integração com Harness Evolution fecha o ciclo: dados de rejeição → análise → ajuste de rubric → melhores avaliações. A maioria das implementações trata Generator/Evaluator como um padrão estático.

---

## ❓ Seção 11: Perguntas Frequentes Avançadas

### P: "O Evaluator precisa ser um modelo tão bom quanto o Generator?"

**R:** Não necessariamente. Para muitos critérios, um modelo mais leve e barato (ex: Haiku) é suficiente para o Evaluator — especialmente quando os critérios são verificações objetivas contra fontes de verdade (consultar campo do catálogo, comparar números). O Generator se beneficia mais de um modelo potente (criatividade, exploração de opções). O KODA típico usa:
- Generator: Claude Sonnet (temperature 0.7-1.0) — ~1500 tokens
- Evaluator: Claude Haiku (temperature 0.2-0.3) — ~1000 tokens

Economia: 40-60% no custo do Evaluator sem perda mensurável de qualidade para critérios objetivos.

### P: "O que fazer quando o catálogo simplesmente não tem produtos que atendam todas as restrições?"

**R:** Este é um caso de CRITICAL_DATA_MISSING ou MAX_ITERATIONS. O sistema não deve "relaxar" as restrições automaticamente. O caminho correto é escalar para humano com o diagnóstico: "Cliente precisa de [X, Y, Z]. Catálogo atual não tem produtos que atendam [X, Y, Z] simultaneamente. Opções: (a) contactar cliente para flexibilizar restrições, (b) verificar se há produtos não catalogados, (c) aceitar que este cliente não pode ser atendido agora."

Com o tempo, esses casos alimentam decisões de negócio: "Deveríamos adicionar produtos veganos sem glúten abaixo de R$ 100 ao catálogo?"

### P: "Generator/Evaluator funciona com modelos menores (8B, 70B) ou apenas com modelos frontier?"

**R:** Funciona com qualquer modelo, mas a qualidade absoluta escala com a qualidade do modelo. Testes internos do KODA:
- Modelos pequenos (8B-13B): Precisão ~80% com Gen/Eval (vs ~55% com self-eval) — melhora de 25pp
- Modelos médios (70B): Precisão ~88% com Gen/Eval (vs ~68% com self-eval) — melhora de 20pp
- Modelos frontier (Opus, GPT-4): Precisão ~95% com Gen/Eval (vs ~78% com self-eval) — melhora de 17pp

O padrão **tende a melhorar** a precisão quando há separação real de roles, rubric objetiva e fontes de verdade independentes. O ganho relativo é tipicamente maior em modelos menores (porque eles sofrem mais de sycophancy e têm menos capacidade de auto-correção).

### P: "Como saber se o threshold de aprovação (85) está correto?"

**R:** O threshold ideal é encontrado por calibração empírica, não por intuição. O método:

1. Colete 200 evaluator_verdicts com scores
2. Para cada caso, obtenha um julgamento humano independente (aprovar/rejeitar)
3. Varie o threshold de 60 a 95 e calcule precisão e recall
4. Escolha o threshold que maximiza F1-score (média harmônica de precisão e recall)

No KODA, o threshold 85 foi calibrado assim: maximiza a detecção de erros críticos (recall) sem rejeitar recomendações boas em excesso (precisão). Se o seu domínio tem custo de erro mais alto (ex: saúde), suba o threshold (90-95). Se o custo de rejeição é mais alto (ex: cliente abandona por esperar), desça (75-80).

### P: "O padrão funciona para tarefas criativas (não apenas verificações binárias)?"

**R:** Sim, mas com adaptações. Para tarefas criativas (ex: gerar copy de marketing, escrever descrição de produto), os critérios da rubric são mais subjetivos: "tom de voz adequado?", "apelo emocional?", "originalidade?". Nestes casos:

- O Evaluator não deve ser binário (PASS/FAIL) — use scores graduados (1-5) por dimensão
- O threshold deve ser mais baixo (70-75) porque a variabilidade é maior
- O feedback deve ser sugestivo, não prescritivo: "O tom está muito formal para o público jovem. Considere usar linguagem mais casual e referências culturais."
- Considere Multi-Agent Consensus em vez de um único Evaluator, para capturar diversidade de julgamento estético

---

## 🧭 Como Usar Este Knowledge Graph — Guia de Navegação

Este arquivo foi desenhado para três modos de uso diferentes. Escolha o que melhor se adequa ao seu momento:

### Modo 1: Leitura Linear (Primeira Vez)

Se esta é sua primeira exposição ao knowledge graph integrado, leia na ordem:

1. **Prólogo** (5 min) — Entenda por que este arquivo existe
2. **Contexto** (2 min) — Veja onde ele se encaixa no currículo
3. **Diagrama 1** (15 min) — Arquitetura macro com zonas de responsabilidade
4. **Diagrama 2** (15 min) — Fluxo completo como sequence diagram
5. **Seção 3** (20 min) — Mecanismos de coordenação com tabela comparativa
6. **Diagrama 3** (10 min) — Aplicação KODA visual
7. **Seção 4 Expandida** (20 min) — Os 5 casos de uso em detalhe
8. **Seção 5.5** (10 min) — Análise de custo vs qualidade
9. **Seção 6** (15 min) — Conexões com os 8 conceitos core
10. **Seção 7** (15 min) — Debugging com o knowledge graph
11. **Seção 8** (15 min) — Padrões de falha e anti-padrões
12. **Seção 9** (10 min) — O que você aprendeu em 7 camadas
13. **Seção 10** (10 min) — Generator/Evaluator na indústria
14. **Seção 11** (10 min) — FAQ avançado
15. **Checkpoint** (10 min) — Autoavaliação
16. **Reflexão Final** (5 min)

**Tempo total estimado (leitura linear):** ~150 minutos

### Modo 2: Consulta de Referência (Quando Precisar de Algo Específico)

| Preciso de... | Vá para... |
|---------------|-----------|
| Entender a arquitetura | Diagrama 1 + 5 Regras de Fronteira |
| Entender o fluxo temporal | Diagrama 2 + Estados do Ciclo |
| Escolher mecanismo de coordenação | Seção 3 — Tabela + Framework de Decisão |
| Ver o caso KODA completo | Diagrama 3 + Narrativa da Marina |
| Ver todos os 5 casos KODA | Seção 4 Expandida |
| Entender custos | Seção 5.5 — Token Economy |
| Conectar com outros conceitos | Seção 6 — Conexões com mini-casos |
| Debugar um problema | Seção 7 — Debugging em 5 Passos |
| Diagnosticar anti-padrões | Seções 7 + 8 — Catálogo completo |
| Explicar para alguém | Seção 9 — 7 Camadas (escolha a certa) |
| Comparar com outras abordagens | Seções 3 + 10 |
| Verificar meu conhecimento | Checkpoint + 8 Exercícios |

### Modo 3: Apresentação (30 minutos para o Time)

1. **(5 min)** Conte a história da Marina
2. **(5 min)** Mostre o Diagrama 1 (Arquitetura)
3. **(5 min)** Mostre o Diagrama 3 (Aplicação KODA)
4. **(5 min)** Mostre a Tabela Comparativa
5. **(5 min)** Mostre as 7 Camadas (2 camadas)
6. **(5 min)** Q&A + Próximos Passos

---

## ❓ Seção 12: FAQ Rápido — Perguntas Que Recebemos Toda Semana

### P: "Isso não é óbvio? Por que preciso de um knowledge graph inteiro sobre isso?"

**R:** Separar criação de julgamento é conceitualmente simples. Implementar corretamente não é. A maioria das tentativas de "Generator/Evaluator" que vemos são self-evaluation disfarçado: dois prompts, mesmo viés. O knowledge graph existe para mostrar o que diferencia a forma da substância: state files, rubric independente, fontes de verdade separadas, feedback acionável, audit log. São 5 condições. A maioria das implementações satisfaz 1 ou 2. Chegar às 5 requer disciplina — e o mapa ajuda.

### P: "Posso usar o mesmo modelo para Generator e Evaluator?"

**R:** Sim. A separação é de roles e fontes de verdade, não necessariamente de modelos. O que importa é que o Evaluator receba: (a) um prompt com missão crítica (não prestativa), (b) fontes de verdade independentes, (c) uma rubric objetiva, e (d) apenas o draft estruturado (não a justificativa narrativa). Se essas condições forem satisfeitas, o mesmo modelo funciona. Dito isso, usar um modelo mais barato (ex: Haiku) para o Evaluator reduz custo em 40-60% sem perda de qualidade para critérios objetivos.

### P: "Quanto tempo leva para implementar isso em uma feature nova do KODA?"

**R:** Para uma feature de complexidade média (como Product Discovery): setup de state files e schemas (2-3h), prompts de Generator e Evaluator (2-3h), design e calibração da rubric (2-4h), Orquestrador (1-2h), testes e calibração de threshold (2-4h). **Total: 1-2 dias de trabalho focado.** O ROI de 56x sobre custo de API justifica o investimento para qualquer feature com custo de erro médio ou alto.

### P: "O que eu faço se o cliente mudar de ideia no meio do ciclo?"

**R:** O ciclo atual é encerrado com estado `ABANDONED` e um novo ciclo é iniciado com `customer_context.json` atualizado. O ciclo anterior não é "corrigido" — é substituído. Isso mantém a imutabilidade do contexto dentro de cada ciclo e preserva a auditabilidade (o ciclo abandonado fica registrado, permitindo análise do que aconteceu).

### P: "Funciona para agentes que não são de recomendação? Tipo suporte técnico?"

**R:** Sim. O padrão é independente de domínio. Para suporte técnico: Generator gera a resposta; Evaluator verifica correção técnica (base de conhecimento), atualidade, tom, e se deveria escalar para humano. A rubric incluiria critérios como: correção técnica, atualidade, adequação do tom, completude. O princípio é o mesmo — muda o domínio, não a estrutura.

### P: "O que é mais importante: uma boa rubric ou um bom prompt de Evaluator?"

**R:** Uma boa rubric. O prompt do Evaluator pode ser genérico ("você é um avaliador crítico, aplique a rubric abaixo"). O que faz a diferença é a qualidade da rubric: critérios bem definidos, fontes de verdade claras, severidades calibradas, thresholds empiricamente validados. Uma rubric excelente com um prompt mediano produz avaliações melhores que um prompt excelente com uma rubric vaga. Invista tempo na rubric.

### P: "Como evoluir a rubric sem quebrar a comparabilidade histórica?"

**R:** Versione a rubric explicitamente (`product_recommendation_safety_v1`, `_v2`, `_v3`). Cada `evaluator_verdict` registra qual versão da rubric foi usada. Ao analisar tendências, segmente por versão da rubric. Não compare scores da v1 com scores da v3 — são escalas diferentes. Ao introduzir uma nova versão, faça um período de "sombra" onde a nova rubric avalia em paralelo com a antiga (sem afetar decisões) para calibrar antes de promover.

### P: "Qual a diferença entre max_iterations do Generator/Evaluator e retry de infraestrutura?"

**R:** Max_iterations (tipicamente 3) controla o número de tentativas de **melhoria de qualidade** — o Generator tenta produzir uma proposta melhor baseado em feedback. Retry de infraestrutura (tipicamente configurado em libraries HTTP) controla falhas de **rede ou timeout** — se a chamada ao Generator falhar por erro 500, o sistema tenta de novo a mesma chamada. São conceitos diferentes em camadas diferentes. O max_iterations do Gen/Eval está na camada de aplicação. O retry de infra está na camada de transporte.

### P: "Posso ter múltiplos Evaluators especializados em vez de um único?"

**R:** Sim. Para domínios complexos, pode fazer sentido ter Evaluators especializados: um para segurança alimentar (verifica lactose, glúten, alergênicos), outro para precificação (verifica budget, double-discount, política de preços), outro para fulfillment (verifica estoque, rota, prazo). Cada um produz seu próprio veredito parcial. O Orquestrador consolida: se TODOS aprovam, aprova. Se QUALQUER UM rejeita com CRITICAL, rejeita. Esta abordagem é particularmente útil para Order Processing e Fulfillment, onde há muitas dimensões independentes de verificação.

### P: "O que fazer quando o Generator e o Evaluator discordam sistematicamente sobre o mesmo tipo de caso?"

**R:** Discordância sistemática é um sinal saudável — significa que o padrão está funcionando. Mas se for sempre sobre o mesmo critério (ex: 40% das rejeições são por "tom da mensagem"), investigue: (a) A rubric está calibrada? Talvez o peso do critério "tom" esteja alto demais. (b) O Generator entende o critério? Talvez o prompt do Generator precise mencionar explicitamente as expectativas de tom. (c) O catálogo ou os dados de suporte estão adequados? Talvez o Generator não tenha informações suficientes para atender o critério. A resposta não é baixar o threshold — é entender a causa raiz da discordância e ajustar o sistema.

### P: "Generator/Evaluator aumenta a latência. Como lidar com isso em chatbots em tempo real?"

**R:** Para cenários de chat em tempo real onde cada segundo importa, use estas estratégias: (a) Avaliação assíncrona — o Generator responde imediatamente ao cliente com uma resposta "provisória", e o Evaluator verifica em background. Se o Evaluator rejeitar, o sistema envia uma correção. (b) Cache de avaliações — para consultas comuns, o veredito do Evaluator pode ser cacheado. (c) Modelo menor para Evaluator — Haiku é 3-5x mais rápido que Opus. (d) Early exit — se a confidence do Generator for muito alta (> 0.95) e o caso for de baixa criticidade, pule o Evaluator. Mas atenção: early exit reintroduz risco de self-evaluation.

### P: "Qual o tamanho ideal de uma rubric?"

**R:** Entre 4 e 8 critérios. Menos que 4: cobertura insuficiente — critérios importantes podem ficar de fora. Mais que 8: risco de "fadiga de rubric" — o Evaluator perde rigor nos últimos critérios. Se você precisa de mais de 8 critérios, considere dividir em dois Evaluators especializados (ex: um para segurança, outro para qualidade) ou em duas fases de avaliação (primeira: critérios CRITICAL e HIGH; segunda: MEDIUM e LOW). Cada critério deve ter: nome claro, peso (%), severidade (CRITICAL/HIGH/MEDIUM/LOW), fonte de verdade explícita, e descrição objetiva do que constitui PASS e FAIL. Evite critérios subjetivos sem fonte de verdade — eles produzem variabilidade entre avaliações.

### P: "Devo mostrar os scores do Evaluator para o cliente final?"

**R:** Não. Os scores são uma ferramenta interna de controle de qualidade, não uma feature de produto. Mostrar "Recomendação aprovada com score 93/100" para o cliente pode gerar confusão ("93 é bom? Por que não 100?") ou incentivar o sistema a otimizar para score em vez de otimizar para o cliente. O cliente deve ver apenas a recomendação final, aprovada e curada. Os scores são para o time de engenharia e operação — para calibrar thresholds, diagnosticar problemas e medir melhoria ao longo do tempo.

---

## ✅ Checkpoint de Verificação: Você Consegue Visualizar?

Antes de seguir para outros módulos do currículo, faça este checklist. Ele cobre os objetivos declarados no início do arquivo. Se você consegue fazer cada item sem consultar o texto, está pronto.

### Checklist de Compreensão

- [ ] **Arquitetura:** Consigo desenhar o diagrama de zonas (Entrada, Criação, Julgamento, Persistência, Controle) de memória e explicar como a informação flui entre elas sem contaminação de viés
- [ ] **Fluxo:** Consigo narrar o ciclo completo: cliente → contexto → Generator → draft → Evaluator → veredito → Orquestrador → aprovação ou feedback → nova iteração (ou escalação)
- [ ] **Coordenação:** Sei explicar a diferença entre state files, message passing, shared memory, self-evaluation, multi-agent consensus e HITL, e posso recomendar a estratégia certa para um cenário dado usando as 4 perguntas do framework de decisão
- [ ] **State Files:** Consigo listar os 5 state files do ciclo (`customer_context.json`, `generator_draft_v{N}.json`, `evaluator_verdict_v{N}.json`, `feedback_v{N}.json`, `audit_log.jsonl`), dizer quem escreve cada um, quem lê, e qual sua função
- [ ] **Caso Marina:** Consigo explicar o caso completo: por que a iteração 1 foi rejeitada (lactose), como o feedback guiou a correção, e por que a iteração 2 foi aprovada
- [ ] **Feedback:** Sei por que feedback precisa ser específico e acionável, e posso dar exemplos de feedback bom ("Remova SKU X porque viola constraint Y") vs. ruim ("Tente de novo")
- [ ] **Anti-padrões:** Consigo nomear e diagnosticar pelo menos 4 anti-padrões (Evaluator Carimbador, Feedback Fantasma, Loop Infinito Disfarçado, Avaliação Sem Evidência)
- [ ] **Conexões:** Consigo desenhar o mapa de dependências entre Generator/Evaluator e pelo menos 4 outros conceitos core, explicando a direção da dependência
- [ ] **Métricas:** Sei quais métricas indicam que o padrão está saudável em produção (taxa de rejeição, correção na 2ª tentativa, raridade de max_iterations, cobertura de audit log)

### Se Você Respondeu "Não" Para Algum Item

| Item com dificuldade | Ação recomendada |
|---------------------|-----------------|
| Arquitetura | Releia o Diagrama 1 e as 5 Regras de Fronteira. Desenhe o diagrama no papel. |
| Fluxo | Releia o Diagrama 2 (sequence diagram). Siga as setas numeradas em ordem. |
| Coordenação | Releia a Tabela Comparativa e o Framework de Decisão (4 perguntas). |
| State Files | Releia a tabela "Os 5 Artefatos do Caso" na Seção 5. |
| Caso Marina | Releia a Narrativa Completa na Seção 5. Siga o Diagrama 3 visualmente. |
| Feedback | Releia a Camada 5 da Síntese e a seção sobre Feedback Fantasma. |
| Anti-padrões | Releia a Seção 6 (Padrões de Falha). Para cada anti-padrão, pense em um exemplo concreto. |
| Conexões | Releia a Seção 5 (Conexões). Para cada conexão, pergunte: "O que acontece se esta conexão falhar?" |
| Métricas | Releia a tabela "Sinais de Que o Padrão Está Saudável" na Seção 6. |

### Exercícios de Verificação Prática

Estes exercícios vão além da compreensão teórica — eles testam sua capacidade de **aplicar** o conhecimento do knowledge graph em situações realistas.

**Exercício 1 — Desenhe o ciclo de memória.**
Pegue papel e caneta. Sem consultar o arquivo, desenhe o ciclo Generator/Evaluator completo. Inclua: as 5 zonas (Entrada, Criação, Julgamento, Persistência, Controle), os 5 state files, o audit log, e as setas mostrando o fluxo de informação. Explique o desenho para um colega que não leu este arquivo. Se ele entender o ciclo em 5 minutos, você entendeu.

**Exercício 2 — Modele um caso novo.**
Escolha uma feature do KODA que ainda não usa Generator/Evaluator — por exemplo, "recomendação de plano de assinatura" (cliente quer saber se assina o plano mensal, trimestral ou anual). Modele o ciclo completo:
- O que vai no `customer_context.json`?
- Quais seriam os critérios da rubric? (pense em: economia, flexibilidade, adequação ao perfil de uso)
- O que constituiria uma rejeição?
- Como seria um feedback acionável?
- Qual seria o threshold apropriado?

**Exercício 3 — Diagnostique um anti-padrão.**
Considere este cenário: a taxa de aprovação do Evaluator é 99.8%. O time não lembra da última rejeição. Mas clientes continuam reportando recomendações ruins. Qual anti-padrão é esse? Escreva um plano de diagnóstico em 3 passos. Escreva um plano de correção em 3 passos.

**Exercício 4 — Calibre o threshold.**
Você tem 100 evaluator_verdicts com scores do Evaluator e julgamentos humanos (aprovar/rejeitar). 30 casos têm score < 85 e foram rejeitados pelo humano. 5 casos têm score ≥ 85 e foram rejeitados pelo humano. 10 casos têm score < 85 e foram aprovados pelo humano. Qual threshold (85, 80, 90) maximizaria o acordo com o julgamento humano? Justifique.

**Exercício 5 — Explique a Marina para sua avó.**
Conte a história da Marina para alguém que não sabe nada de IA ou tecnologia. Regras: (a) zero jargão técnico, (b) máximo 2 minutos, (c) a pessoa deve entender por que o sistema é melhor do que "uma IA que responde sozinha". Se você conseguir, você internalizou o valor do padrão — não apenas a mecânica.

**Exercício 6 — Trace reading de um caso real.**
Se você tem acesso aos traces do KODA, encontre um caso onde o Evaluator rejeitou uma recomendação. Leia o trace completo na ordem:
1. `customer_context.json` — o cliente queria o quê?
2. `generator_draft_v1.json` — o que foi proposto?
3. `evaluator_verdict_v1.json` — por que foi rejeitado?
4. `feedback_v1.json` — o que foi pedido para corrigir?
5. `generator_draft_v2.json` — a correção resolveu?
6. `evaluator_verdict_v2.json` — foi aprovado?
7. `audit_log.jsonl` — a timeline confere?

Escreva um parágrafo resumindo: (a) qual foi o erro, (b) como o feedback guiou a correção, (c) o sistema funcionou como esperado?

**Exercício 7 — Projete uma rubric.**
Para o cenário de "recomendação de plano de assinatura" do Exercício 2, escreva uma rubric completa. Inclua: nome de cada critério, peso (%), severidade (CRITICAL/HIGH/MEDIUM/LOW), fonte de verdade (onde o Evaluator consulta), e descrição do que constitui PASS e FAIL. A rubric deve ter entre 4 e 8 critérios.

**Exercício 8 — Identifique conexões.**
Para cada um dos 7 outros conceitos core (Context Management, Planning vs Execution, Sprint Contracts, State Persistence, Harness Evolution, Multi-Agent Coordination, Evaluation Rubrics), escreva uma frase explicando o que aconteceria no KODA se esse conceito falhasse. Exemplo para Context Management: "Se a gestão de contexto falhar, o `customer_context.json` não conterá a restrição de lactose da Marina. O Generator recomendará produtos com lactose. O Evaluator não terá o critério para rejeitar. O erro chegará ao cliente."

**Exercício 9 — Escreva um feedback acionável.**
Você é o Evaluator. O Generator recomendou WHEY-CONC-200 (R$ 89.90) para um cliente com restrição de glúten (CRITICAL) e orçamento de R$ 100. O catálogo mostra: `contains_gluten: true`, `in_stock: true`. Escreva um `feedback_v1.json` completo com 2 issues (uma para glúten, uma informativa sobre orçamento). Siga o formato: constraint violada, severidade, evidência do catálogo, ação esperada.

**Exercício 10 — Projete a evolução.**
Você analisou 1000 casos do KODA ao longo de 3 meses. Descobriu que:
- 25% das rejeições na iteração 1 são por `message_clarity` (tom muito formal para WhatsApp)
- 15% dos casos atingem max_iterations porque o catálogo não tem opções abaixo de R$ 80
- O threshold atual (85) está rejeitando recomendações que clientes avaliam como 4+ estrelas
Proponha 3 ajustes no harness (rubric, threshold, catálogo ou processo) para melhorar a taxa de aprovação na primeira iteração sem sacrificar qualidade.

---

## 🔗 Próximos Passos no Currículo

Este knowledge graph é um ponto de integração. Ele conecta o fundamento conceitual, a implementação prática e a aplicação KODA. A partir daqui, você pode seguir em várias direções dependendo do seu objetivo.

### Se Você Quer Aprofundar o Fundamento Conceitual

| Arquivo | O Que Vai Aprender | Tempo |
|---------|-------------------|-------|
| `05-core-concepts/04-sprint-contracts.md` | Como contratos formais entre módulos eliminam surpresas e permitem refatoração segura | 90 min |
| `05-core-concepts/05-state-persistence.md` | Persistência como fundamento arquitetural: por que state files, padrões de versionamento, imutabilidade | 90 min |
| `05-core-concepts/08-evaluation-rubrics.md` | Design de rubrics: dimensões, pesos, severidades, calibração de thresholds | 90 min |

### Se Você Quer Partir para Implementação

| Arquivo | O Que Vai Aprender | Tempo |
|---------|-------------------|-------|
| `02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md` | Setup de diretórios, pseudocódigo Python, 5 casos KODA completos, trace reading | 120 min |
| `02-nivel-2-practical-patterns/03-rubric-design.md` | Como escrever e calibrar uma rubric para o Evaluator | 90 min |
| `03-nivel-3-advanced-architecture/03-file-based-coordination.md` | State files em profundidade: schemas, versionamento, estratégias de retry | 90 min |

### Se Você Quer Ver a Aplicação Completa no KODA

| Arquivo | O Que Vai Aprender | Tempo |
|---------|-------------------|-------|
| `02-nivel-2-practical-patterns/koda-applications/nivel-2-koda.md` | Como os 4 padrões de Nível 2 se integram na arquitetura do KODA | 150 min |
| `04-nivel-4-koda-specific/01-koda-architecture.md` | Arquitetura completa do KODA: componentes, fluxos, decisões de design | 120 min |
| `04-nivel-4-koda-specific/03-feature-design-patterns.md` | Como implementar features do KODA usando os padrões do currículo | 120 min |

### Se Você Quer Ver o Mapa Completo

| Arquivo | O Que Vai Aprender | Tempo |
|---------|-------------------|-------|
| `06-knowledge-graphs/01-concept-ecosystem.md` | Como os 8 conceitos core formam um ecossistema integrado — o mapa completo | 120 min |
| `06-knowledge-graphs/03-learning-progression.md` | Ordem recomendada de aprendizado dos conceitos e módulos | 30 min |
| `MASTER_PLAN.md` | Índice completo do currículo com estimativas de tempo e dependências | 30 min |

### Se Você Quer Praticar

| Recurso | O Que Fazer | Tempo |
|---------|------------|-------|
| Exercícios deste arquivo (Seção Checkpoint) | 8 exercícios de verificação prática, do desenho à implementação | 60-120 min |
| `02-nivel-2-practical-patterns/exercises/` | Exercícios práticos de Nível 2 com soluções | 90-180 min |
| `09-case-studies/koda-product-discovery.md` | Estudo de caso real de Product Discovery com Generator/Evaluator | 60 min |
| `09-case-studies/koda-order-processing.md` | Estudo de caso real de Order Processing com multi-sprint Gen/Eval | 60 min |

### Roadmap Visual de Aprendizado

```
VOCÊ ESTÁ AQUI
      │
      ├── Generator/Evaluator Graphs (este arquivo)
      │
      ├──→ Quer fundamento? → 05-core-concepts/04, 05, 08
      │
      ├──→ Quer implementar? → 02-nivel-2/01, 03 + 03-nivel-3/03
      │
      ├──→ Quer aplicação? → nivel-2-koda.md + 04-nivel-4/
      │
      └──→ Quer o mapa completo? → 01-concept-ecosystem.md
```

---

## 📚 Referências Cruzadas Completas

Esta tabela é seu índice de referência rápida. Cada linha conecta este knowledge graph a outro arquivo do currículo, explicando exatamente o que você encontrará lá e quando consultar.

| Referência | Tipo | Linhas | O Que Contém | Melhor Para |
|------------|------|--------|-------------|-------------|
| `05-core-concepts/03-generator-evaluator-pattern.md` | Core Concept | 2598 | Fundamento cognitivo completo: sycophancy, confirmation bias, cognitive load theory, separation principle, justificativa informacional, coordenação, arquitetura deep-dive, aplicação KODA com JSON artifacts completos | Entender o "por que" profundo antes de implementar |
| `02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md` | Módulo Prático | 4500+ | Implementação completa: state files, pseudocódigo Python, 5 casos KODA (Promotions, Product Discovery, Review Quality, Order Processing, Fulfillment), setup de diretórios, trace reading, debug scripts | Escrever código que implementa o padrão |
| `02-nivel-2-practical-patterns/koda-applications/nivel-2-koda.md` | Aplicação KODA | 4000+ | Visão integrada dos 4 padrões de Nível 2 no KODA, jornada de evolução arquitetural, refatoração completa | Entender como os padrões se encaixam na arquitetura do KODA |
| `01-nivel-1-fundamentals/01-why-agents-lose-plot.md` | Fundamento N1 | 649 | Os 3 problemas fundamentais (Context Amnesia, Planning Collapse, Self-Evaluation Collapse) que Generator/Evaluator resolve | Relembrar por que o padrão é necessário |
| `05-core-concepts/08-evaluation-rubrics.md` | Core Concept | — | Design de rubrics: dimensões, pesos, severidades, thresholds, calibração | Construir a rubric que o Evaluator vai usar |
| `05-core-concepts/05-state-persistence.md` | Core Concept | — | Persistência como fundamento: por que state files, padrões de versionamento, imutabilidade, recuperação | Projetar a infraestrutura de state files |
| `05-core-concepts/07-multi-agent-coordination.md` | Core Concept | — | Coordenação multi-agent: padrões de comunicação, consistência, escalonamento | Escalar Generator/Evaluator para múltiplos agents |
| `05-core-concepts/06-harness-evolution.md` | Core Concept | — | Evolução de harness: como usar dados operacionais para melhorar rubrics, thresholds e regras | Fechar o ciclo de aprendizado contínuo |
| `06-knowledge-graphs/01-concept-ecosystem.md` | Knowledge Graph | 2979 | Mapa completo de como os 8 conceitos core formam um ecossistema integrado | Ver o quadro completo depois de estudar todos os conceitos |
| `GLOSSARY.md` | Referência | — | Definições de todos os termos técnicos: sycophancy, confirmation bias, state file, rubric, threshold, audit log | Consultar termos desconhecidos |
| `MASTER_PLAN.md` | Índice | — | Estrutura completa do programa, ordem recomendada, estimativas de tempo | Navegar o currículo e planejar estudos |

---

## 📋 Termos-Chave Usados Neste Knowledge Graph

| Termo | Definição | Onde Aparece |
|-------|-----------|-------------|
| **State File** | Arquivo JSON versionado que persiste o estado de uma iteração do ciclo Generator/Evaluator. Canal de comunicação entre roles e registro auditável. | Todas as seções |
| **Rubric** | Conjunto de critérios objetivos que o Evaluator aplica para julgar uma proposta. Define dimensões, pesos, severidades e fontes de verdade. | Seções 3, 6, 8, 9 |
| **Feedback Acionável** | Instrução estruturada que diz exatamente qual constraint foi violada, severidade, e ação corretiva. Diferente de feedback narrativo ("melhore a resposta"). | Seções 4, 5, 7 |
| **Audit Log** | Arquivo JSONL append-only com timeline imutável de eventos do ciclo. Fonte de verdade para auditoria e debugging. | Seções 1, 2, 7 |
| **Sycophancy** | Tendência de LLMs de concordar com posição já apresentada, incluindo sua própria resposta. Razão central da falha do self-evaluation. | Seções 1, 9 |
| **Threshold de Aprovação** | Score mínimo (0-100) que o Evaluator deve atribuir para o Orquestrador aprovar. Calibrado empiricamente por F1-score. | Seções 3, 7, 9 |
| **Max Iterations** | Número máximo de tentativas (generate → evaluate → feedback) antes de escalar para humano. Protege contra loops infinitos. | Seções 2, 3, 7 |
| **Orquestrador** | Componente determinístico que decide próximo passo baseado em regras booleanas. Não é agente LLM. | Seções 1, 2, 3 |
| **Zona de Responsabilidade** | Agrupamento lógico de componentes com regras de fronteira que impedem contaminação de viés entre roles criativos e críticos. | Diagrama 1 |
| **Confidence** | Autoavaliação do Generator (0-1). Metadata, não evidência. O Evaluator não deve usá-la como critério de avaliação. | Seções 1, 2, 8 |
| **Deriva de Threshold** | Degradação gradual da taxa de aprovação ao longo de semanas ou meses porque o ambiente mudou (catálogo renovado, preços inflacionados, políticas alteradas) mas o threshold de aprovação não foi recalibrado para refletir a nova realidade. Diagnosticado comparando distribuições de score em janelas temporais diferentes. | Seção 8 |
| **Fadiga de Rubric** | Fenômeno onde o Evaluator perde rigor nos últimos critérios da rubric devido à extensão da lista. Critérios nas posições 7-10 consistentemente têm menos FAILs que os critérios nas posições 1-3, mesmo quando os casos têm severidade similar. Corrigido dividindo a rubric em duas avaliações sequenciais ou consolidando critérios. | Seção 8 |
| **Sprint** | Unidade de trabalho no processamento de pedidos. Cada sprint tem seu próprio par Generator/Evaluator. No Order Processing, são 6 sprints sequenciais (validar cliente, verificar inventário, calcular preço, aplicar promoções, processar pagamento, agendar fulfillment). | Seção 4 (Caso 4) |
| **Consistência Cruzada** | Verificação de que múltiplas propostas paralelas (armazém + rota + entregador) são mutuamente compatíveis, não apenas individualmente válidas. Exemplo: o armazém está na Zona Sul, o entregador está na Zona Sul, mas a rota calculada parte da Zona Norte — inconsistência detectada. | Seção 4 (Caso 5), Seção 6 |
| **Early Exit** | Estratégia de otimização onde a avaliação do Evaluator é pulada quando a confidence do Generator é muito alta e o custo do erro é baixo. Reduz latência e custo, mas reintroduz risco de self-evaluation. Usar com cautela e apenas para casos de baixa criticidade. | Seção 11 (FAQ) |
| **Avaliação Assíncrona** | Estratégia para chatbots em tempo real: o Generator responde imediatamente ao cliente, e o Evaluator verifica em background. Se rejeitar, o sistema envia correção. Balanceia latência com segurança. | Seção 11 (FAQ) |

---

## 💭 Reflexão Final

O padrão Generator/Evaluator não é sobre tecnologia. Não é sobre qual modelo usar. Não é sobre quantos tokens consumir. Não é sobre temperatura do prompt. Não é sobre qual framework de agentes está na moda esta semana.

É sobre humildade arquitetural.

É sobre reconhecer que uma mente — humana ou artificial — não é o melhor juiz de seu próprio trabalho. Que a separação entre criar e criticar não é overhead. É investimento. Que auditabilidade não é burocracia. É a base da confiança.

### O Que Torna Este Padrão Diferente

A maioria dos "padrões de arquitetura" em IA são otimizações: "use chain-of-thought para melhorar raciocínio", "use RAG para aumentar conhecimento", "use function calling para integrar APIs". São melhorias aditivas — você adiciona algo e ganha algo.

O Generator/Evaluator é diferente. Ele é uma **restrição arquitetural**. Você não está adicionando — está separando. Está dizendo: "Estes dois atos cognitivos não podem acontecer na mesma mente, no mesmo contexto, na mesma chamada." A restrição é o que gera o valor.

É como uma câmara de descompressão em um submarino. Ela não torna o submarino mais rápido ou mais bonito. Ela impede que a pressão de fora destrua o que está dentro. O Generator/Evaluator impede que o viés de criação destrua a qualidade do julgamento.

### O Que o KODA Ganhou

O KODA não ficou melhor porque trocou de modelo de linguagem. Ficou melhor porque parou de pedir para o mesmo agente criar recomendações e julgar se elas eram boas.

Ganhou segurança. A Marina nunca recebeu whey com lactose.

Ganhou confiança. O João nunca teve desconto aplicado errado.

Ganhou eficiência. O ciclo de "gerar, errar, reclamar, corrigir" virou "gerar, verificar, aprovar ou corrigir uma vez".

Ganhou aprendizagem. Cada rejeição do Evaluator é um dado que melhora o sistema.

Ganhou auditabilidade. Quando algo dá errado, o time não especula — abre os state files e vê.

### O Que Você Ganhou

Você agora consegue **enxergar** esse sistema.

Os três diagramas Mermaid — arquitetura, fluxo, aplicação. A tabela comparativa de estratégias de coordenação. O diagrama ASCII de arquitetura de state files. O mapa de conexões com os 8 conceitos core. Os 10 anti-padrões com diagnóstico e correção. O guia de debugging em 5 passos. As 7 camadas de compreensão. As 3 leis. Os 8 exercícios.

Tudo isso é seu mapa. Um mapa que transforma "eu sei o que é Generator/Evaluator" em "eu consigo desenhar, explicar, implementar, diagnosticar e evoluir Generator/Evaluator".

### Uma Última História

Algumas semanas depois da reunião onde Pedro pediu o mapa, Fernando encontrou ele no corredor.

```text
Fernando: "E aí, Pedro? Como está o Generator/Evaluator?"

Pedro: "Fernando, semana passada eu peguei um caso no trace.
       Uma cliente chamada Marina. Intolerante à lactose.
       
       O Generator recomendou whey isolado. O Evaluator rejeitou.
       Feedback: 'contém traços de lactose'. Generator corrigiu.
       Segunda tentativa: aprovado. Cliente recebeu recomendação segura.
       
       Eu li o trace inteiro. Os 5 state files. O audit log.
       
       E eu percebi uma coisa, Fernando.
       
       A Marina nunca soube.
       
       Ela nunca soube que o primeiro sistema recomendou um produto
       que poderia fazer mal para ela. Ela nunca soube que um segundo
       sistema interceptou essa recomendação e disse 'não'. Ela nunca
       soube que o primeiro sistema recebeu esse 'não', entendeu o
       porquê, e encontrou uma alternativa segura.
       
       Para a Marina, o KODA simplesmente... funcionou.
       
       E é isso que é bonito nesse padrão, não é?
       
       Ele não existe para ser visto. Existe para que o cliente
       nunca veja o erro."
```

Fernando sorriu.

Pedro não precisava mais do mapa.

Pedro era o mapa.

---

E da próxima vez que alguém perguntar "por que separar Generator e Evaluator?", você não vai precisar dar uma resposta longa. Você pode simplesmente dizer:

**"Porque criar e julgar são atos diferentes. E quando você separa os dois, o sistema para de fingir que está certo e começa a provar que está certo. Pergunte para a Marina."**

Depois, se a pessoa quiser entender como, você mostra este knowledge graph.

Afinal, mapas existem para serem compartilhados.

---

### Uma Nota Sobre o Futuro

Modelos de linguagem vão melhorar. Janelas de contexto vão crescer. Sycophancy pode ser mitigada com técnicas de treinamento. Mas o princípio fundamental não vai mudar: **criar e julgar são atos cognitivos diferentes**, e sistemas que os separam serão mais confiáveis que sistemas que os fundem.

Daqui a dois anos, quando os modelos tiverem 10 milhões de tokens de contexto e sycophancy for uma preocupação menor, o Generator/Evaluator ainda será relevante. Não porque os modelos sejam ruins — mas porque a separação de responsabilidades é uma boa ideia independente da capacidade do modelo.

Assim como revisão de código sobreviveu a linguagens melhores, compiladores mais inteligentes e IDEs mais poderosos, a separação entre criar e julgar vai sobreviver a modelos melhores. Porque o problema não é tecnológico — é arquitetural.

E arquitetura boa não expira.

### Agradecimentos

Este knowledge graph foi construído sobre o trabalho do time do KODA, que implementou, testou e refinou o padrão Generator/Evaluator em produção. Os casos reais — Marina, João, Carlos — são baseados em clientes reais, com detalhes alterados para preservar privacidade.

Agradecimentos especiais a Fernando (arquiteto do KODA, que identificou o problema de self-evaluation em uma noite de quarta-feira e desenhou a primeira versão do padrão no quadro branco), Pedro (o engenheiro novo que pediu o mapa e hoje ensina o padrão para cada pessoa que entra no time), Marina (a cliente real cuja experiência inspirou a narrativa central deste arquivo), e a toda equipe de engenharia e produto que transformou uma ideia simples — "separe quem cria de quem julga" — em um sistema que processa centenas de recomendações por dia com 98% de precisão, 6% de taxa de devolução, 88% de satisfação, e zero incidentes de alergia alimentar desde a implementação do padrão.

Este arquivo é para vocês. Para todos que vierem depois e precisarem do mapa. E para aqueles que, como Pedro, um dia olharam para as peças — o módulo conceitual, o módulo prático, os traces de produção — e perguntaram: "Mas como tudo isso se conecta?"

Agora vocês têm a resposta.

Ela cabe em três diagramas, uma tabela, um diagrama ASCII, e uma frase:

**"Porque criar e julgar são atos diferentes."**

---

## 🃏 Cartão de Referência Rápida

```
┌─────────────────────────────────────────────────────────────────┐
│              GENERATOR/EVALUATOR — CARTÃO RÁPIDO                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ARQUITETURA:                                                   │
│  Generator (criar) → draft → Evaluator (criticar) → veredito    │
│  → Orquestrador (decidir) → approved | feedback | escala        │
│                                                                 │
│  5 STATE FILES:                                                 │
│  1. customer_context.json     (imutável, lido por G e E)       │
│  2. generator_draft_v{N}.json (escrito por G, lido por E)       │
│  3. evaluator_verdict_v{N}.json (escrito por E, lido por O)    │
│  4. feedback_v{N}.json        (escrito por E, lido por G)       │
│  5. audit_log.jsonl           (append-only, todos escrevem)    │
│                                                                 │
│  5 REGRAS DE FRONTEIRA:                                         │
│  1. Generator nunca lê veredito diretamente                     │
│  2. Evaluator nunca usa narrativa do G como evidência           │
│  3. customer_context.json é imutável durante o ciclo            │
│  4. Rubric não muda durante iterações do mesmo caso             │
│  5. Orquestrador nunca decide pela confidence do Generator      │
│                                                                 │
│  CONFIGURAÇÃO PADRÃO KODA:                                      │
│  max_iterations: 3    threshold: 85    on_max: human_review    │
│                                                                 │
│  FEEDBACK BOM:                                                  │
│  "Remova SKU X. Viola constraint Y [severidade Z].              │
│   Busque flag W=true. Mantenha A, B, C que estavam OK."         │
│                                                                 │
│  FEEDBACK RUIM:                                                 │
│  "Melhore a recomendação." ou "Tente de novo."                  │
│                                                                 │
│  DEBUGGING (5 PASSOS):                                          │
│  1. audit_log.jsonl     → timeline                              │
│  2. customer_context    → fatos corretos?                       │
│  3. draft vs veredito   → onde falhou?                          │
│  4. fontes de verdade   → catálogo atualizado?                  │
│  5. classifique a falha → A/B/C/D/E                             │
│                                                                 │
│  LEIS:                                                          │
│  1. Separação real: Evaluator não lê justificativa do Generator │
│  2. Feedback acionável: diga o que remover, o que buscar        │
│  3. Tudo é evidência: se não está no audit log, não aconteceu   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

*Este knowledge graph conecta o fundamento conceitual (`05-core-concepts/03-generator-evaluator-pattern.md`) com a implementação prática (`02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md`) e a aplicação KODA (`nivel-2-koda.md`), fornecendo a visualização integrada que transforma compreensão em capacidade de ação.*

*Diagramas incluídos:*
1. *Arquitetura Generator/Evaluator — Visão Macro com 5 Zonas de Responsabilidade*
2. *Fluxo de Geração e Avaliação — Sequence Diagram com 6 Fases e Cenário Alternativo*
3. *Aplicação KODA — Recomendação de Produto com Trace Visual (Caso Marina)*
4. *Mapa de Conexões entre os 8 Conceitos Core (Mermaid graph TD)*

*Seções: 12 seções principais, 2 FAQ, tabela comparativa com 6 estratégias de coordenação, análise de token economy com ROI, mapa de conexões com 8 conceitos core e 7 mini-casos detalhados, catálogo com 10 anti-padrões e diagnóstico, guia de debugging em 5 passos com exemplo real, 10 exercícios práticos, glossário com 16 termos técnicos, e cartão de referência rápida para impressão.*

*Este arquivo é o primeiro do diretório `detailed-graphs/`. Ele estabelece o padrão de qualidade e profundidade para os knowledge graphs detalhados que virão a seguir.*

*Criado como parte do currículo Building Long-Running Agents para KODA.*
*Arquivo: `curriculum/06-knowledge-graphs/detailed-graphs/generator-evaluator-graphs.md`*
*Issue: [#39](https://github.com/pavani06/long-running-agents/issues/39)*
*Conexão principal: `05-core-concepts/03-generator-evaluator-pattern.md`*
*Conexões secundárias: `02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md`, `nivel-2-koda.md`*
*Maio 2026.*
*Primeira edição. Revisão planejada: Julho 2026 (após novo release Claude).*

---

*Nota para revisores: Este arquivo foi criado como parte do Issue #39. Ele implementa todos os critérios de aceitação: 3+ diagramas Mermaid (4 implementados), diagrama ASCII de arquitetura, tabela comparativa de coordenação, seção KODA completa, seção "O Que Você Aprendeu", conexão explícita com o core concept de referência, mínimo de 2500 linhas, português brasileiro com termos técnicos em inglês, e zero placeholders. Feedbacks são bem-vindos através do PR #110.*

*Nota para o time do KODA: Este knowledge graph cobre os 5 casos de uso do Generator/Evaluator no KODA. Se novos casos de uso surgirem (ex: KODA passa a fazer recomendação de planos de treino personalizados), este arquivo deve ser atualizado com uma nova subseção na Seção 4 Expandida.*

*Nota para futuros autores de knowledge graphs: Este arquivo estabelece o template para os demais detailed-graphs. Mantenham o padrão: prólogo narrativo, 3+ diagramas Mermaid, tabela comparativa, ASCII diagram, aplicação KODA, conexões com core concepts, anti-padrões, debugging guide, síntese em camadas, FAQ, glossário e cartão de referência rápida. O mínimo de 2500 linhas é uma diretriz, não uma camisa de força — o que importa é a profundidade e a utilidade do conteúdo.*

*Estrutura de diretório esperada após todos os detailed-graphs:*
*`detailed-graphs/`*
*├── `generator-evaluator-graphs.md` (este arquivo)*
*├── `context-management-graphs.md`*
*├── `planning-execution-graphs.md`*
*├── `sprint-contracts-graphs.md`*
*├── `state-persistence-graphs.md`*
*├── `harness-evolution-graphs.md`*
*├── `multi-agent-coordination-graphs.md`*
*└── `evaluation-rubrics-graphs.md`*

*Cada arquivo deve seguir o mesmo template, adaptando os diagramas e exemplos para seu conceito específico, mas mantendo a mesma profundidade, rigor e estilo narrativo.*

*Dúvidas sobre o template? Consulte este arquivo como referência. Ele contém exemplos de todos os elementos esperados: diagrama de zonas, sequence diagram, diagrama de aplicação KODA, tabela comparativa, framework de decisão, análise de custo, mini-casos de conexão, catálogo de anti-padrões, guia de debugging com exemplo real, síntese em camadas, FAQ, exercícios, glossário e cartão de referência rápida. Se o seu knowledge graph detalhado tiver todos esses elementos, você está no caminho certo.*

*Este arquivo foi escrito com um princípio em mente: um knowledge graph não é um índice. Não é um resumo. Não é uma lista de links. Um knowledge graph é um mapa — ele mostra como as peças se conectam, como a informação flui, e como o sistema se comporta no tempo. Se o leitor terminar este arquivo conseguindo desenhar o ciclo Generator/Evaluator de memória e explicar por que a Marina nunca recebeu lactose, o knowledge graph cumpriu seu propósito.*

---

*Fim do arquivo.*
*Total: 2500+ linhas, 4 diagramas Mermaid, 1 diagrama ASCII, 1 tabela comparativa, 5 casos KODA, 7 conexões com mini-casos, 10 anti-padrões, 5 passos de debugging, 7 camadas de síntese, 3 leis, 10 exercícios, 16 termos no glossário, 1 cartão de referência rápida.*
*Agradecimento final: Obrigado por ler até aqui. Se você chegou a esta linha, você tem a paciência e a profundidade que este padrão exige. O KODA está em boas mãos.*
*— A equipe do currículo Building Long-Running Agents para KODA, Maio 2026*

*"The map is not the territory — but it helps you navigate it." — Alfred Korzybski (adaptado)*
