---
title: "Learning Assessment Rubric: Como Medir Compreensão Real dos 8 Core Concepts"
type: curriculum-template
aliases: []
tags: [curriculo-conteudo, template, avaliacao-de-aprendizado, autoavaliacao, dominio-conceitual, mentoria, progresso-pedagogico, medicao-de-compreensao]
relates-to: ["[[curriculum/05-core-concepts/08-evaluation-rubrics|Evaluation Rubrics]]", "[[docs/canonical/eval-tier-stratification|Eval Tier Stratification]]"]
last_updated: 2026-06-10
---
# 📋 Learning Assessment Rubric: Como Medir Compreensão Real dos 8 Core Concepts
## Critérios objetivos, verificáveis e calibrados para auto-avaliação e mentoria no currículo KODA

**Tempo Estimado:** 90-120 minutos (leitura completa + primeira aplicação)
**Nível:** Tools & Templates — aplicável a todos os níveis do currículo
**Pré-requisito:** Familiaridade com os 8 Core Concepts (leitura dos arquivos em `05-core-concepts/`)
**Status:** 🟢 OPERACIONAL — Template para avaliação contínua de aprendizado
**Data de Criação:** Maio 2026

---

## 📖 Prólogo: O Momento em Que Fernando Percebeu Que "Eu Entendi" Não Significava Nada

Era uma sexta-feira, 16h. Fernando estava conduzindo a terceira sessão de mentoria com a equipe de engenharia. O tópico era Context Management — o primeiro core concept do currículo.

Ele perguntou:

> "João, você consegue me explicar por que uma context window de 1 milhão de tokens não resolve todos os problemas de memória de um agente?"

João respondeu na hora:

> "Claro! Porque mesmo com 1 milhão de tokens, o agente precisa priorizar o que fica na janela. Dados críticos como alergias do cliente não podem depender só da janela — precisam de persistência externa. A janela é memória de curto prazo, não arquitetura de memória."

Fernando sorriu. Parecia que João tinha entendido perfeitamente.

Então ele fez a pergunta seguinte:

> "Beleza. Agora me mostra no código do KODA onde você colocaria a camada de persistência para uma conversa que já dura 2 horas."

Silêncio.

João sabia a **teoria**. Conseguia explicar o conceito. Mas quando chegou a hora de **aplicar**, o conhecimento não se traduziu em ação.

Fernando percebeu algo que mudou completamente a forma como ele avaliava aprendizado:

> *"Existe uma diferença entre conseguir repetir um conceito e conseguir usá-lo para tomar decisões. E a maioria das avaliações mede apenas a primeira."*

Naquela noite, ele esboçou o que viria a ser esta rubric. Não era uma prova. Não era um checklist de "viu ou não viu". Era um mapa de profundidade — uma forma de medir **quão fundo** alguém entendeu cada conceito.

### Os 4 Tipos de "Entendi"

Fernando identificou quatro níveis de compreensão que se repetiam em toda a equipe:

**Nível 1: "Entendi a definição"** — A pessoa consegue repetir o que o conceito significa. Sabe a diferença entre context window e state persistence. Consegue explicar por que Generator/Evaluator é melhor que self-evaluation. Mas quando confrontada com um problema real, não sabe por onde começar.

**Nível 2: "Consigo aplicar com ajuda"** — A pessoa já implementou algo parecido, seguindo um exemplo ou template. Se der um código-base e disser "segue esse padrão", ela consegue. Mas se tirar o exemplo, ela trava.

**Nível 3: "Consigo aplicar sozinho e adaptar"** — A pessoa olha para um problema novo, reconhece qual padrão se aplica, e implementa do zero. Consegue explicar **por que** escolheu essa abordagem e não outra. Sabe os trade-offs.

**Nível 4: "Consigo ensinar e evoluir o padrão"** — A pessoa não só aplica como melhora. Olha para um Generator/Evaluator existente e sugere: "aqui dava para paralelizar os evaluators". Ou "esse contrato de sprint está muito rígido, vamos adicionar graceful degradation". Consegue mentorear outros.

Esses quatro níveis — **Básico, Intermediário, Avançado, Expert** — formam a espinha dorsal desta rubric.

### O Que Esta Rubric Não É

Antes de mergulhar nos critérios, é importante deixar claro o que esta rubric **não** é:

- ❌ **Não é uma prova.** Você não "passa" ou "falha". Você identifica em qual nível está para cada conceito.
- ❌ **Não é uma competição.** O objetivo não é chegar a Expert em tudo. Alguns conceitos você usa diariamente (Context Management), outros são especializados (Harness Evolution). É natural ter profundidades diferentes.
- ❌ **Não é imutável.** Conforme o currículo evolui e novos padrões emergem, os critérios devem ser recalibrados.
- ❌ **Não substitui prática.** Esta rubric mede compreensão, mas a verdadeira validação vem de código funcionando em produção.

### O Que Esta Rubric É

- ✅ **Um mapa de profundidade.** Para cada um dos 8 core concepts, você sabe exatamente o que precisa demonstrar para estar em cada nível.
- ✅ **Uma ferramenta de auto-avaliação.** Você pode se avaliar honestamente e saber onde focar seus estudos.
- ✅ **Um guia para mentores.** Mentores usam esta rubric para diagnosticar gaps e sugerir próximos passos.
- ✅ **Um contrato de expectativa.** Equipes sabem o que significa "dominar" um conceito — não é opinião, é critério.
- ✅ **Uma base para crescimento.** Você não fica preso no "será que já sei o suficiente?". Você tem critérios objetivos para responder essa pergunta.

### Mais Cenas Que Moldaram a Rubric

Fernando não chegou a essa conclusão em uma única reunião. A cena com João foi só o ponto de virada.

Na segunda-feira seguinte, ele revisou as notas das semanas anteriores e percebeu um padrão desconfortável.

Três pessoas tinham dito que entendiam Context Management.

Duas tinham dito que dominavam Generator/Evaluator.

Uma tinha se declarado pronta para desenhar Multi-Agent Coordination em produção.

Quando Fernando comparou essas declarações com os PRs reais, a história era diferente.

Marina conseguia explicar sliding window com clareza. Ela até desenhou uma janela móvel no quadro, marcou os tokens antigos saindo, os tokens novos entrando, e explicou por que uma conversa longa não cabia inteira na memória ativa.

Mas no PR dela, a preferência do cliente por produtos sem cafeína continuava apenas no transcript.

Quando a conversa passava de quarenta minutos, a preferência saía da window.

O agente voltava a recomendar pré-treinos com cafeína.

Marina tinha entendido a mecânica da window, mas não tinha entendido a decisão arquitetural: informação crítica precisa mudar de camada.

Esse foi o primeiro aha moment de Fernando.

> "Se a evidência não exige uma decisão real, ela mede vocabulário, não competência."

Depois veio Bruno.

Bruno era rápido. Ele pegava templates, copiava padrões, ajustava nomes e entregava algo que parecia correto.

Em uma tarefa de Generator/Evaluator, ele criou um Generator para recomendações de produtos e um Evaluator que dava score de 1 a 10.

O PR passou nos testes básicos.

Na revisão, Fernando perguntou:

> "O Evaluator sabe algo que o Generator não sabe?"

Bruno abriu o arquivo, leu o prompt, parou, e percebeu que não.

Os dois agentes tinham acesso às mesmas informações, ao mesmo catálogo resumido e às mesmas restrições.

O Evaluator estava só opinando de novo, com outro nome.

Ele parecia crítico, mas não tinha ground truth adicional.

Esse foi o segundo aha moment.

> "Um padrão pode estar presente na forma e ausente na função."

A rubric precisava capturar isso.

Não bastava perguntar se alguém implementou G/E.

Era preciso perguntar se a separação de incentivos existia de verdade.

Era preciso olhar se o Evaluator tinha critérios próprios, dados próprios, thresholds próprios e feedback útil.

Na mesma semana, Aline trouxe um caso de Sprint Contracts.

Ela tinha criado um contrato para o módulo de recomendação.

O schema validava que cada produto tinha `id`, `name`, `price` e `available`.

Tecnicamente, estava correto.

Mas um cliente alérgico a amendoim recebeu uma recomendação de pasta proteica com traços de amendoim.

O contrato tinha validado estrutura.

Não tinha validado semântica.

Aline estava no limite entre Nível 2 e Nível 3.

Ela sabia escrever o contrato.

Ainda não sabia decidir quais garantias importavam para o domínio.

Fernando anotou:

> "Nível 2 valida o shape. Nível 3 valida a promessa."

Essa frase entrou na forma como ele passou a avaliar Sprint Contracts.

Depois veio Diego, que tinha o problema oposto.

Diego se avaliou como Nível 1 em State Persistence porque nunca tinha lido o módulo formal do currículo.

Mas quando Fernando pediu para ele explicar uma migração recente de `customer_context`, Diego descreveu hot state, cold history, schema version, dual read e fallback.

Ele não usava todos os nomes do material.

Mesmo assim, o julgamento arquitetural estava lá.

Diego tinha aprendido pela produção antes de aprender pela teoria.

Esse foi o terceiro aha moment.

> "A rubric não pode punir quem aprendeu pelo caminho prático. Ela precisa reconhecer evidência, não estilo de estudo."

Foi aí que Fernando decidiu separar cada nível por comportamento observável.

Se a pessoa demonstra o comportamento, o nível conta.

Se só fala bonito, não conta.

Se não usa o nome exato, mas toma boas decisões e explica o raciocínio, isso conta.

Na sexta seguinte, a equipe fez uma sessão de debug coletivo.

Um fluxo de pedido same-day estava falhando de forma intermitente.

O agente de estoque confirmava disponibilidade.

O agente de entrega calculava rota.

O agente de pagamento reservava cobrança.

Mesmo assim, alguns pedidos chegavam ao fulfillment com endereço antigo.

A primeira hipótese foi bug no agente de entrega.

A segunda foi falha de cache.

A terceira foi race condition entre dois updates de estado.

Lívia, que se dizia apenas Intermediária em Multi-Agent Coordination, abriu o audit log e reconstruiu a sequência.

Ela percebeu que o orquestrador aceitava resultado de qualquer agente que terminasse por último, mesmo quando o resultado tinha sido calculado sobre uma versão antiga do estado.

Ela não só encontrou o bug.

Ela propôs incluir `state_version` no contrato entre agentes e rejeitar outputs baseados em versão stale.

Fernando olhou para a checklist antiga e percebeu que ela não capturava esse tipo de julgamento.

A pessoa não tinha criado um framework.

Não tinha mentoreado ninguém.

Mas tinha demonstrado Nível 3 com clareza.

A rubric precisava ter espaço para evidências de debug, não só para entregas planejadas.

Outro caso veio de Rafael.

Rafael era confiante, articulado e muito bom em explicar conceitos.

Ele conseguia fazer uma palestra de vinte minutos sobre Harness Evolution.

Falava de thresholds, false positives, monitoring, drift e feedback loop.

Quando Fernando pediu um exemplo de validação que deveria ser removida do harness, Rafael travou.

Ele sempre pensava em adicionar proteções.

Nunca em tirar proteções obsoletas.

Essa lacuna gerava harnesses pesados, lentos e difíceis de manter.

O aha moment foi simples.

> "Evoluir não é só adicionar. Evoluir também é remover o que deixou de pagar aluguel."

A rubric passou a avaliar manutenção, não apenas criação.

Camila trouxe a lição de Evaluation Rubrics.

Ela tinha criado uma rubric bonita, com dimensions, weights e anchors.

A apresentação impressionou todo mundo.

Depois de duas semanas, os scores não batiam com a satisfação dos clientes.

Recomendações com score 90 geravam devolução.

Recomendações com score 72 recebiam elogios.

A rubric media clareza textual melhor do que adequação real ao cliente.

Camila não defendeu a própria criação.

Ela coletou exemplos, comparou score com outcome real, ajustou weights e adicionou uma dimensão de risco contextual.

A nova versão passou a prever melhor os problemas.

Fernando viu ali um comportamento de Nível 3 avançando para Nível 4.

Não era só criar uma rubric.

Era aceitar que a rubric também precisa ser avaliada.

O último caso que entrou na memória da equipe foi o de Pedro.

Pedro era júnior e tinha medo de se expor.

Na auto-avaliação, marcou Nível 1 em quase tudo.

Durante uma sessão prática, recebeu um trace com Planning Collapse.

O agente tinha começado verificando estoque, pulado para pagamento, voltado para endereço, perdido o cupom e finalizado com total errado.

Pedro desenhou os passos em uma folha.

Separou decisão estrutural de execução atômica.

Propôs um plano com checkpoints simples.

Não era perfeito.

Mas era exatamente o comportamento esperado de Nível 2.

Fernando percebeu que a rubric também precisava proteger contra o viés para baixo.

Algumas pessoas superestimam.

Outras subestimam.

Sem evidência, o mentor fica preso à narrativa da pessoa sobre si mesma.

Com evidência, a conversa muda.

A pergunta deixa de ser "você acha que sabe?".

Passa a ser "o que você consegue demonstrar hoje?".

Foi assim que esta rubric ganhou sua forma atual.

Ela nasceu de conversas reais, bugs reais, PRs reais e decisões que custaram tempo da equipe.

Ela não tenta medir inteligência.

Não tenta medir senioridade geral.

Mede algo mais útil para o currículo KODA: a profundidade com que alguém consegue reconhecer, aplicar, adaptar, ensinar e evoluir os 8 core concepts.

Quando usada direito, ela muda a conversa de aprendizado.

O learner para de dizer apenas "entendi".

O mentor para de responder apenas "ótimo".

Os dois passam a perguntar:

> "Qual evidência mostra isso?"

Essa pergunta é desconfortável no começo.

Depois vira liberdade.

Porque quando a evidência aparece, o progresso deixa de ser sensação e vira navegação.

---

## 🎯 O Que Você Vai Encontrar Nesta Rubric

- ✅ **Definição dos 4 níveis de compreensão** com critérios gerais e exemplos concretos
- ✅ **Critérios específicos por conceito** para cada um dos 8 core concepts, com comportamentos observáveis
- ✅ **Diagrama ASCII da arquitetura da rubric** mostrando como conceitos, níveis e avaliação se conectam
- ✅ **Tabela comparativa de estratégias de avaliação** (auto-avaliação, peer review, mentoria, rubric formal)
- ✅ **Checklist de auto-avaliação** para o learner se posicionar em cada conceito
- ✅ **Guia para mentores** com perguntas-gatilho, coleta de evidências e metodologia de scoring
- ✅ **Seção de aplicação KODA** mostrando como usar a rubric no contexto real da equipe
- ✅ **Resumo "O Que Você Aprendeu"** com os pontos essenciais para levar adiante

---

## 🔍 Os 4 Níveis de Compreensão: Definição Geral

Antes de aplicar os critérios a cada conceito, é fundamental entender o que cada nível significa em termos de **comportamento observável**. Estes critérios gerais se aplicam a qualquer um dos 8 core concepts.

### Nível 1: Básico (Conhecimento Declarativo)

**O que caracteriza:** A pessoa consegue definir o conceito, explicar seu propósito e identificar sua importância no contexto de long-running agents. Consegue responder perguntas do tipo "o que é X?" e "por que X existe?".

**Comportamentos observáveis:**
- Define o conceito com terminologia correta (ex: sabe a diferença entre context window e state persistence)
- Explica por que o conceito é relevante para KODA ou agentes long-running
- Identifica o problema que o conceito resolve (ex: "Generator/Evaluator resolve o problema de sycophancy na auto-avaliação")
- Reconhece o conceito quando o vê aplicado (ex: olha para um código e diz "isso aqui é um Sprint Contract")
- Responde perguntas factuais sobre o conceito (ex: "Qual é a diferença entre summarization e compaction?")

**Limitações típicas:**
- Não consegue implementar o conceito do zero sem template
- Não sabe escolher entre variações do conceito para um problema específico
- Consegue explicar "o quê" mas não "como" ou "quando não usar"

**Pergunta-chave que o nível responde:** "Você sabe o que é isso?"

---

### Nível 2: Intermediário (Aplicação Guiada)

**O que caracteriza:** A pessoa consegue aplicar o conceito seguindo padrões estabelecidos, templates ou documentação. Consegue modificar implementações existentes e adaptar exemplos para contextos ligeiramente diferentes.

**Comportamentos observáveis:**
- Implementa o conceito usando templates ou código de referência (ex: cria um Generator/Evaluator a partir do exemplo do módulo)
- Modifica parâmetros de forma consciente (ex: ajusta thresholds de uma rubric baseado em requisitos)
- Debuga problemas básicos em implementações existentes (ex: encontra por que um Sprint Contract está falhando)
- Explica o fluxo de execução de uma implementação do conceito (ex: walkthrough de como state files fluem entre módulos)
- Identifica quando uma aplicação existente do conceito está com defeito (ex: "esse harness não está validando a restrição de lactose")

**Limitações típicas:**
- Depende de exemplos para começar — não consegue implementar do zero em um domínio novo
- Tem dificuldade em combinar múltiplos conceitos simultaneamente
- Escolhe a implementação por familiaridade, não por adequação ao problema

**Pergunta-chave que o nível responde:** "Você consegue aplicar isso com ajuda?"

---

### Nível 3: Avançado (Aplicação Autônoma com Julgamento)

**O que caracteriza:** A pessoa consegue aplicar o conceito de forma independente em contextos novos, fazer trade-offs conscientes entre abordagens, e adaptar o padrão quando a situação exige. O julgamento é tão importante quanto a execução.

**Comportamentos observáveis:**
- Implementa o conceito do zero em um domínio novo sem consultar templates (ex: cria um sistema de Multi-Agent Coordination para um problema que nunca viu antes)
- Compara abordagens diferentes e justifica a escolha com critérios objetivos (ex: "vou usar file-based coordination em vez de message queue porque precisamos de audit trail")
- Adapta o padrão quando a forma canônica não se encaixa (ex: "o Generator/Evaluator clássico é sequencial, mas aqui vou paralelizar os evaluators")
- Antecipa problemas de borda e projeta mitigação (ex: "se o arquivo de estado corromper, tenho um fallback para a versão anterior")
- Explica o conceito para outras pessoas com exemplos originais (não apenas repetindo os do currículo)
- Mede a efetividade da implementação com métricas concretas (ex: "a precisão das recomendações subiu de 75% para 92% após implementar G/E")

**Limitações típicas:**
- Pode não ter visão de como o conceito evolui com mudanças no modelo ou na infraestrutura
- Ainda pensa no conceito como uma "ferramenta" e não como um "princípio arquitetural"

**Pergunta-chave que o nível responde:** "Você consegue aplicar isso sozinho e escolher a abordagem certa?"

---

### Nível 4: Expert (Evolução e Mentoria)

**O que caracteriza:** A pessoa não só domina o conceito como contribui para sua evolução. Consegue identificar limitações fundamentais do padrão, propor melhorias estruturais, mentorear outros engenheiros e adaptar o conceito para contextos radicalmente diferentes.

**Comportamentos observáveis:**
- Propõe melhorias no padrão canônico baseado em experiência de produção (ex: "o Sprint Contract deveria incluir versionamento para backward compatibility")
- Cria variações do padrão para contextos específicos (ex: "para low-latency agents, criei um Evaluator assíncrono que não bloqueia o Generator")
- Diagnostica falhas sutis que outros não veem (ex: identifica que um harness está aprovando outputs porque o threshold foi calibrado com dados enviesados)
- Mentora outros engenheiros com eficácia comprovada (ex: alguém que você mentoreou implementou o conceito corretamente em produção)
- Publica ou documenta aprendizados que avançam o conhecimento da equipe sobre o conceito
- Conecta o conceito com outros em níveis mais altos de abstração (ex: "Context Management + State Persistence + Multi-Agent Coordination formam juntos uma arquitetura de memória distribuída")

**Pergunta-chave que o nível responde:** "Você consegue melhorar o padrão e ensinar outros a usá-lo?"

---

### 📊 Tabela Resumo dos Níveis

| Dimensão | Básico | Intermediário | Avançado | Expert |
|----------|--------|---------------|----------|--------|
| **Tipo de conhecimento** | Declarativo | Procedural guiado | Procedural autônomo | Criativo/evolutivo |
| **Consegue explicar?** | Sim, definição | Sim, fluxo | Sim, com trade-offs | Sim, com limitações e evolução |
| **Consegue implementar?** | Não | Com template | Do zero | Do zero + melhorias |
| **Consegue adaptar?** | Não | Com ajuda | Sozinho | Inova |
| **Consegue avaliar qualidade?** | Não | Com rubrica pronta | Cria rubrica | Evolui rubrica |
| **Consegue ensinar?** | Não | Com material pronto | Com exemplos próprios | Com metodologia |
| **Tempo típico para atingir** | 2-4h de estudo | 1-2 semanas de prática | 1-3 meses de uso real | 6+ meses + produção |
| **Evidência principal** | Explicação oral | Código seguindo padrão | Implementação original | Melhoria do padrão |

---

## 🏗️ Arquitetura da Rubric: Como Tudo se Conecta

```
┌──────────────────────────────────────────────────────────────────────────────────────┐
│                         LEARNING ASSESSMENT RUBRIC ARCHITECTURE                        │
├──────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                       │
│                            ┌─────────────────────────┐                                │
│                            │     QUEM APLICA?         │                                │
│                            │  ┌───────────────────┐   │                                │
│                            │  │ AUTO-AVALIAÇÃO    │   │                                │
│                            │  │ (Learner)         │   │                                │
│                            │  │ MENTOR APPLY      │   │                                │
│                            │  │ (Mentor Guide)    │   │                                │
│                            │  │ PEER REVIEW       │   │                                │
│                            │  │ (Colega)          │   │                                │
│                            │  └───────────────────┘   │                                │
│                            └────────────┬────────────┘                                │
│                                         │                                             │
│                            ┌────────────▼────────────┐                                │
│                            │    4 NÍVEIS DE           │                                │
│                            │    COMPREENSÃO           │                                │
│                            │  ┌────────────────────┐  │                                │
│                            │  │ 1: BÁSICO          │  │  Sabe o que é                 │
│                            │  │ 2: INTERMEDIÁRIO   │  │  Aplica com ajuda             │
│                            │  │ 3: AVANÇADO        │  │  Aplica sozinho, julga        │
│                            │  │ 4: EXPERT          │  │  Evolui, ensina               │
│                            │  └────────────────────┘  │                                │
│                            └────────────┬────────────┘                                │
│                                         │                                             │
│         ┌───────────────────────────────┼───────────────────────────────┐             │
│         │                               │                               │             │
│  ┌──────▼──────┐  ┌──────▼──────┐  ┌────▼────────┐  ┌──────▼──────┐                   │
│  │ CONTEXT     │  │ PLANNING    │  │ GENERATOR/  │  │ SPRINT      │                   │
│  │ MANAGEMENT  │  │ VS EXEC     │  │ EVALUATOR   │  │ CONTRACTS   │                   │
│  │    C1       │  │    C2       │  │    C3       │  │    C4       │                   │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘                   │
│                                                                                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                   │
│  │ STATE       │  │ HARNESS     │  │ MULTI-AGENT │  │ EVALUATION  │                   │
│  │ PERSISTENCE │  │ EVOLUTION   │  │ COORD       │  │ RUBRICS     │                   │
│  │    C5       │  │    C6       │  │    C7       │  │    C8       │                   │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘                   │
│                                         │                                             │
│                            ┌────────────▼────────────┐                                │
│                            │    DECISION GATE          │                                │
│                            │  (conceitual — a decisão  │                                │
│                            │   final é por conceito,   │                                │
│                            │   ver Metodologia de      │                                │
│                            │   Scoring na pg. seguinte)│                                │
│                            │                           │                                │
│                            │  ┌────────────────────┐   │                                │
│                            │  │ Nível alvo atingido │   │                                │
│                            │  │ em cada conceito?   │   │                                │
│                            │  │ SIM → AVANÇA para   │   │                                │
│                            │  │       próximo nível │   │                                │
│                            │  │ NÃO → REFORÇA gaps  │   │                                │
│                            │  │       identificados │   │                                │
│                            │  └────────────────────┘   │                                │
│                            └────────────┬────────────┘                                │
│                                         │                                             │
│                            ┌────────────▼────────────┐                                │
│                            │    EVIDENCE COLLECTION   │                                │
│                            │  ┌────────────────────┐  │                                │
│                            │  │ Explicação oral    │  │                                │
│                            │  │ Código / PR        │  │                                │
│                            │  │ Documentação       │  │                                │
│                            │  │ Trace de debug     │  │                                │
│                            │  │ Mentoria registrada│  │                                │
│                            │  └────────────────────┘  │                                │
│                            └─────────────────────────┘                                │
│                                                                                       │
└──────────────────────────────────────────────────────────────────────────────────────┘
```

---

## ⚖️ Tabela Comparativa: Estratégias de Avaliação

Antes de aplicar a rubric, é útil entender como ela se compara a outras formas de avaliação. Cada estratégia tem seu lugar — a rubric formal é a mais precisa, mas também a mais custosa de configurar.

| Dimensão | Auto-Avaliação | Peer Review | Mentoria 1:1 | Rubric Formal (esta) |
|----------|---------------|-------------|-------------|---------------------|
| **Precisão** | Baixa (viés de confirmação) | Média (depende da experiência do par) | Alta (mentor experiente) | Muito Alta (critérios calibrados) |
| **Consistência** | Baixa (cada um se avalia diferente) | Média (varia entre pares) | Média-Alta (depende do mentor) | Muito Alta (mesmos critérios para todos) |
| **Custo inicial** | Zero | Baixo | Alto (tempo do mentor) | Médio (criar e calibrar a rubric) |
| **Custo por avaliação** | Zero | 30-60 min | 60-90 min | 20-40 min (após setup) |
| **Escalabilidade** | Alta (qualquer número de pessoas) | Média (precisa de pares disponíveis) | Baixa (mentor é gargalo) | Alta (aplicável em larga escala) |
| **Objetividade** | Baixa | Média | Alta | Muito Alta |
| **Auditabilidade** | Baixa (não deixa rastro) | Média (feedback informal) | Alta (notas do mentor) | Muito Alta (critérios + evidências documentadas) |
| **Velocidade de feedback** | Instantânea | 1-3 dias | 1-7 dias (agendamento) | 1-2 dias (após coleta de evidências) |
| **Cobre profundidade?** | Superficial | Média | Alta | Muito Alta (4 níveis calibrados) |
| **Identifica gaps cegos?** | Não (não sabe o que não sabe) | Às vezes | Sim | Sim (níveis explicitam o que falta) |
| **Melhor para...** | Check-in rápido, reflexão inicial | Validação cruzada, segunda opinião | Desenvolvimento acelerado, casos complexos | Avaliação formal, progressão de nível, certificação |

### Quando Usar Cada Estratégia

**Auto-Avaliação:**
- Use no início de cada módulo para estabelecer baseline
- Use após completar um conceito para verificar compreensão inicial
- Combine SEMPRE com pelo menos uma avaliação externa (peer ou mentor)

**Peer Review:**
- Use após implementações práticas (exercícios, código)
- Use quando o mentor não está disponível
- Use para conceitos de Nível 2-3 onde pares têm contexto similar

**Mentoria 1:1:**
- Use para avaliação de progressão entre níveis (ex: Intermediário → Avançado)
- Use quando há gaps identificados que precisam de orientação personalizada
- Use para conceitos de Nível 3-4 onde profundidade é crítica

**Rubric Formal:**
- Use para avaliações trimestrais de progresso no currículo
- Use para decidir se alguém está pronto para o próximo nível do programa
- Use como base para certificação interna de competências

---

## 📊 Critérios por Conceito

Esta é a seção central da rubric. Para cada um dos 8 core concepts do currículo KODA, você encontrará:

- Uma **breve definição** do conceito (para alinhar expectativas)
- **Critérios específicos** para cada um dos 4 níveis de compreensão
- **Comportamentos observáveis** que evidenciam cada nível
- **Armadilhas comuns** — o que as pessoas costumam confundir em cada nível

---

### Conceito 1: Context Management

**Definição:** A disciplina de gerenciar o que um agente "vê" em cada momento de decisão, garantindo que informações críticas estejam disponíveis sem sobrecarregar a janela de contexto. Envolve estratégias como Sliding Window, Summarization, Compaction, Retrieval e State Persistence como camada complementar.

**Por que importa para KODA:** Em conversas de WhatsApp que duram 2+ horas, o agente precisa lembrar alergias, preferências, promessas de entrega e histórico de compras — sem que o contexto cresça até estourar a janela ou degradar a qualidade das respostas.

#### Nível 1 — Básico

**Critérios:**
- Define context window, token e context amnesia com terminologia correta
- Explica por que "janela maior" não resolve todos os problemas de memória
- Lista pelo menos 3 estratégias de context management (ex: summarization, sliding window, state persistence)
- Identifica a diferença entre "informação estar na conversa" e "informação estar disponível para decisão"
- Reconhece os sintomas de context amnesia em uma conversa (ex: agente pergunta algo que cliente já respondeu)

**Evidências aceitáveis:**
- Explicação oral ou escrita correta dos conceitos
- Consegue apontar exemplos de context amnesia em conversas reais do KODA

**Armadilha comum:** Achar que context window grande (1M tokens) elimina a necessidade de estratégias de gerenciamento. Não elimina — apenas adia o problema e pode mascarar má arquitetura.

#### Nível 2 — Intermediário

**Critérios:**
- Implementa pelo menos uma estratégia de context management seguindo template (ex: sliding window com tamanho configurável)
- Configura parâmetros de summarization (ex: frequência de sumarização, tamanho do resumo) com justificativa
- Lê e interpreta arquivos de estado (ex: `customer_context.json`) para entender o que está sendo persistido
- Identifica quando uma informação deveria ser promovida de "conversa" para "estado persistente"
- Debuga problemas básicos: "por que o agente esqueceu a alergia do cliente?"

**Evidências aceitáveis:**
- PR com implementação de sliding window ou summarization seguindo padrão do time
- Correção de um bug de context amnesia com explicação da causa raiz

**Armadilha comum:** Implementar sliding window mas esquecer de promover informações críticas para estado persistente antes que saiam da janela. O sliding window resolve o sintoma (janela cheia), não a causa (informação importante não está segura).

#### Nível 3 — Avançado

**Critérios:**
- Projeta um pipeline de context management com múltiplas camadas (ex: hot context → warm context → cold storage)
- Escolhe entre estratégias (summarization vs compaction vs retrieval) baseado em requisitos do caso de uso
- Implementa priorização de contexto: informações críticas (alergias) têm precedência sobre informações contextuais (histórico de navegação)
- Mede e otimiza a eficiência do context management (ex: "reduzi o uso de tokens em 40% sem perda de precisão")
- Conecta Context Management com State Persistence (C5) — sabe quando cada camada é responsável por qual informação
- Antecipa e mitiga problemas de borda: contexto corrompido, recuperação de estado, migração de formato

**Evidências aceitáveis:**
- Design document de um pipeline de contexto com justificativa para cada camada
- Métricas de antes/depois mostrando melhoria mensurável
- Implementação que sobrevive a cenários de stress (conversa 4h+, múltiplas interrupções)

**Armadilha comum:** Over-engineering. Criar 7 camadas de contexto quando 3 resolveriam. Cada camada adicional introduz latência e pontos de falha. O bom context management é o mais simples que resolve o problema.

#### Nível 4 — Expert

**Critérios:**
- Projeta sistemas de context management que se adaptam dinamicamente ao perfil da conversa (ex: detecta que é uma conversa de compra complexa e expande o hot context)
- Cria ou evolui ferramentas de context management usadas por outros no time
- Mentora engenheiros que passam a implementar context management corretamente
- Publica aprendizados sobre estratégias de contexto que funcionaram (ou falharam) em produção
- Conecta Context Management com Multi-Agent Coordination (C7): como contexto flui entre agentes em um sistema distribuído

**Evidências aceitáveis:**
- Biblioteca interna ou padrão de context management adotado pelo time
- Case study documentado de uma melhoria estrutural no context management do KODA
- Histórico de mentoria com resultados comprovados



#### 📝 Exemplos Concretos por Nível

**Nível 1, Cenário 1:** Durante uma conversa de mentoria, você pergunta ao learner: "O que causa context amnesia?". A resposta menciona o conceito certo, usa os termos principais e conecta com KODA, mas fica no plano explicativo. O learner ainda não propõe mudança em código, não escolhe parâmetros e não aponta onde a decisão entraria no fluxo.

**Nível 1, Cenário 2:** Você mostra um trace curto de conversa longa de WhatsApp com alergias, preferências e orçamento mudando ao longo de duas horas. O learner reconhece o problema, nomeia o conceito C1 corretamente e explica por que ele importa. Quando você pergunta "qual arquivo você mudaria primeiro?", a resposta vira tentativa genérica ou pedido de exemplo pronto.

**Nível 1, Cenário 3:** Em uma sessão de grupo, o learner consegue comparar C1 com um conceito vizinho do currículo. A comparação é conceitualmente correta, mas ele ainda confunde sinais de diagnóstico com decisões de implementação quando o caso fica mais específico.

**Nível 2, Cenário 1:** Você entrega um exemplo funcional do time e pede para o learner adaptar o padrão para conversa longa de WhatsApp com alergias, preferências e orçamento mudando ao longo de duas horas. Ele segue o template, altera os campos certos, roda a validação esperada e explica o fluxo com segurança. Se você remove o template, ele demora para decidir a estrutura inicial.

**Nível 2, Cenário 2:** Você entrega um bug específico e pede para debuggar um sliding window que removeu uma preferência crítica antes de persistir o estado. O learner encontra a falha, corrige sem mudar partes não relacionadas e registra a evidência do comportamento novo. A solução é correta, mas ainda espelha bastante o padrão existente.

**Nível 2, Cenário 3:** Em review, o learner sabe apontar qual critério da rubric foi atendido pelo PR. Ele também sabe dizer o que ainda não demonstrou para Nível 3, principalmente autonomia em domínio novo e justificativa de trade-offs.

**Nível 3, Cenário 1:** Você apresenta um problema novo e pergunta: "Como você projetaria context management para isso?". O learner estrutura a solução sem template, escolhe alternativas com base em risco, latência, custo e qualidade, e explica por que descartou outras opções.

**Nível 3, Cenário 2:** Você pede para projetar hot context, warm context, cold storage e retrieval para conversas de compra complexas. O learner desenha a arquitetura, identifica pontos de falha, define métricas de sucesso e propõe como provar que a mudança melhorou o sistema. A conversa inclui limites da abordagem, não só benefícios.

**Nível 3, Cenário 3:** Durante um incidente, o learner usa trace de conversa, configuração de window, resumo gerado e arquivo `customer_context.json` para reconstruir causa raiz. Ele não para no sintoma. Ele conecta o bug a uma decisão de design e propõe uma correção que reduz a chance de repetição.

**Nível 4, Cenário 1:** O learner propõe um pipeline adaptativo que muda a prioridade do contexto conforme risco, duração e intenção de compra. A proposta não é só uma melhoria local. Ela vira padrão, biblioteca, guia interno ou decisão de arquitetura que outras pessoas conseguem reaplicar.

**Nível 4, Cenário 2:** Em uma sessão de mentoria, o learner guia outra pessoa do diagnóstico até a decisão de implementação. Ele faz perguntas, testa hipóteses, mostra trade-offs e deixa a pessoa capaz de repetir o raciocínio sem depender dele.

**Nível 4, Cenário 3:** O learner revisa a forma como o time avalia C1. Ele identifica critério fraco, evidência enganosa ou métrica que envelheceu, propõe ajuste e acompanha se a nova avaliação prevê melhor o comportamento em produção.

#### 🔬 Como Coletar Evidências

**Para confirmar Nível 1:**
1. Peça uma explicação em voz alta com exemplo próprio de KODA.
2. Mostre um trace simples e peça para o learner nomear o problema.
3. Faça uma pergunta de contraste com outro conceito do currículo.
4. Registre se a resposta usa termos corretos sem depender de frases decoradas.

**Para confirmar Nível 2:**
1. Entregue um template funcional e peça uma adaptação pequena, mas realista.
2. Inclua um bug controlado ligado a context management e observe o caminho de debug.
3. Peça que o learner explique cada mudança feita no PR.
4. Colete o diff, o teste ou a demonstração que prova o novo comportamento.

**Para confirmar Nível 3:**
1. Use um problema que não aparece nos exemplos do currículo.
2. Peça duas alternativas e uma justificativa explícita de escolha.
3. Exija métrica de sucesso, como redução de tokens sem perda de recall de fatos críticos.
4. Revise se a solução trata falhas prováveis, não apenas o happy path.

**Para confirmar Nível 4:**
1. Procure evidência de influência fora do próprio PR do learner.
2. Verifique se outra pessoa ou outro time adotou o padrão proposto.
3. Peça um relato de mentoria com antes, depois e evidência do mentorado.
4. Compare a proposta com dados de produção para ver se ela melhorou a prática do time.

#### 📈 Progressão Típica

A progressão em C1 costuma começar com vocabulário e reconhecimento de sintomas. Depois, o learner ganha confiança adaptando exemplos existentes e corrigindo bugs pequenos. O salto para Avançado acontece quando ele deixa de perguntar "qual template uso?" e passa a perguntar "qual decisão o domínio exige?". O salto para Expert aparece quando a melhoria deixa de ser pessoal e passa a mudar o modo como o time ensina, implementa e mede context management.

---

### Conceito 2: Planning vs Execution Separation

**Definição:** O princípio arquitetural de separar a fase de planejamento (decidir O QUE fazer e em qual ordem) da fase de execução (realmente FAZER cada passo, um de cada vez). Resolve o Planning Collapse — quando um agente tenta planejar e executar simultaneamente e colapsa em confusão, erros em cascata e decisões precipitadas.

**Por que importa para KODA:** Processar um pedido de 12 produtos envolve verificar estoque, validar cupom, calcular frete, confirmar endereço e processar pagamento. Fazer tudo de uma vez gera erros. Separar planejamento de execução leva a precisão de ~80% para ~99.8%.

#### Nível 1 — Básico

**Critérios:**
- Explica a diferença entre "planejar" e "executar" no contexto de agentes
- Descreve o problema de Planning Collapse com exemplos concretos
- Identifica quando um agente está sofrendo de Planning Collapse (ex: interrompe uma tarefa no meio para começar outra)
- Lista os benefícios da separação: clareza, checkpoints, recuperação de falhas, auditabilidade

**Evidências aceitáveis:**
- Explicação oral ou escrita com exemplo próprio (não apenas repetindo o do currículo)
- Consegue apontar Planning Collapse em um trace de conversa real

**Armadilha comum:** Achar que separar planejamento de execução significa "o agente não pode pensar enquanto age". Na prática, o Executor ainda toma micro-decisões — a separação é sobre decisões estruturais (ordem, dependências, checkpoints), não sobre cada ação atômica.

#### Nível 2 — Intermediário

**Critérios:**
- Implementa um fluxo Planner → Executor usando templates (ex: ordem de processamento com checkpoints)
- Escreve um plano em formato estruturado (ex: JSON com passos, dependências e critérios de sucesso)
- Executa um plano passo a passo, verificando cada checkpoint antes de continuar
- Identifica quando um plano falhou em um passo específico e consegue reportar qual passo e por quê
- Modifica planos existentes para adicionar novos passos ou ajustar ordem

**Evidências aceitáveis:**
- Código funcional de um Planner que gera JSON e um Executor que consome esse JSON
- Demonstração de recuperação: plano falha no passo 3, Executor reporta erro claro, não tenta continuar cegamente

**Armadilha comum:** Criar planos excessivamente detalhados que são essencialmente código em linguagem natural. Um bom plano tem o nível certo de abstração — detalhado o suficiente para o Executor não se perder, abstrato o suficiente para o Executor ter espaço para adaptação.

#### Nível 3 — Avançado

**Critérios:**
- Projeta um sistema de planning com múltiplos níveis (plano estratégico → plano tático → passos de execução)
- Implementa replanejamento dinâmico: quando um passo falha, o Planner ajusta o plano em vez de abortar
- Usa Sprint Contracts (C4) como ponte formal entre Planner e Executor
- Conecta Planning/Execution com Generator/Evaluator (C3): o Planner decide o que gerar, o Generator gera, o Evaluator verifica
- Mede o impacto da separação com métricas: antes/depois em precisão, tempo de execução, taxa de erro
- Compara com abordagens alternativas (Chain-of-Thought, ReAct) e justifica quando usar cada uma

**Evidências aceitáveis:**
- Arquitetura documentada de um sistema multi-fase (planejar → gerar → executar → verificar)
- Métricas mostrando redução de erros em cascata após implementação
- Implementação que lida com falha parcial (passo 3 de 7 falhou, Planner decide se refaz passo 3 ou replaneja passos 4-7)

**Armadilha comum:** Criar um Planner que é essencialmente outro agente complexo, introduzindo os mesmos problemas que deveria resolver. O Planner deve ser mais simples e determinístico que o Executor — se o Planner também sofre de context amnesia, a arquitetura não resolveu nada.

#### Nível 4 — Expert

**Critérios:**
- Projeta sistemas onde o Planner aprende com execuções passadas (ex: "planos para pedidos de 12+ produtos devem incluir verificação de estoque em paralelo")
- Cria padrões de planning reutilizáveis que outros engenheiros adotam
- Mentora outros na arte de separar planejamento de execução sem over-engineering
- Conecta Planning/Execution com Harness Evolution (C6): o harness observa planos que falham e sugere ajustes estruturais

**Evidências aceitáveis:**
- Framework ou biblioteca interna de planning usada por múltiplos times
- Case study de um sistema que evoluiu de single-pass para multi-phase com melhorias documentadas
- Histórico de mentoria com engenheiros que passaram a implementar separação corretamente



#### 📝 Exemplos Concretos por Nível

**Nível 1, Cenário 1:** Durante uma conversa de mentoria, você pergunta ao learner: "Como você reconhece Planning Collapse?". A resposta menciona o conceito certo, usa os termos principais e conecta com KODA, mas fica no plano explicativo. O learner ainda não propõe mudança em código, não escolhe parâmetros e não aponta onde a decisão entraria no fluxo.

**Nível 1, Cenário 2:** Você mostra um trace curto de pedido com estoque, cupom, frete, endereço, pagamento e confirmação final. O learner reconhece o problema, nomeia o conceito C2 corretamente e explica por que ele importa. Quando você pergunta "qual arquivo você mudaria primeiro?", a resposta vira tentativa genérica ou pedido de exemplo pronto.

**Nível 1, Cenário 3:** Em uma sessão de grupo, o learner consegue comparar C2 com um conceito vizinho do currículo. A comparação é conceitualmente correta, mas ele ainda confunde sinais de diagnóstico com decisões de implementação quando o caso fica mais específico.

**Nível 2, Cenário 1:** Você entrega um exemplo funcional do time e pede para o learner adaptar o padrão para pedido com estoque, cupom, frete, endereço, pagamento e confirmação final. Ele segue o template, altera os campos certos, roda a validação esperada e explica o fluxo com segurança. Se você remove o template, ele demora para decidir a estrutura inicial.

**Nível 2, Cenário 2:** Você entrega um bug específico e pede para corrigir um fluxo Planner → Executor onde o Executor continua após um checkpoint falhar. O learner encontra a falha, corrige sem mudar partes não relacionadas e registra a evidência do comportamento novo. A solução é correta, mas ainda espelha bastante o padrão existente.

**Nível 2, Cenário 3:** Em review, o learner sabe apontar qual critério da rubric foi atendido pelo PR. Ele também sabe dizer o que ainda não demonstrou para Nível 3, principalmente autonomia em domínio novo e justificativa de trade-offs.

**Nível 3, Cenário 1:** Você apresenta um problema novo e pergunta: "Como você projetaria planning separado de execution para isso?". O learner estrutura a solução sem template, escolhe alternativas com base em risco, latência, custo e qualidade, e explica por que descartou outras opções.

**Nível 3, Cenário 2:** Você pede para desenhar replanejamento dinâmico quando estoque muda no meio do pedido. O learner desenha a arquitetura, identifica pontos de falha, define métricas de sucesso e propõe como provar que a mudança melhorou o sistema. A conversa inclui limites da abordagem, não só benefícios.

**Nível 3, Cenário 3:** Durante um incidente, o learner usa plano JSON, logs de checkpoints, trace de falha e decisão de replanejamento para reconstruir causa raiz. Ele não para no sintoma. Ele conecta o bug a uma decisão de design e propõe uma correção que reduz a chance de repetição.

**Nível 4, Cenário 1:** O learner cria padrões reutilizáveis de planos com checkpoints e políticas de replanejamento por tipo de fluxo. A proposta não é só uma melhoria local. Ela vira padrão, biblioteca, guia interno ou decisão de arquitetura que outras pessoas conseguem reaplicar.

**Nível 4, Cenário 2:** Em uma sessão de mentoria, o learner guia outra pessoa do diagnóstico até a decisão de implementação. Ele faz perguntas, testa hipóteses, mostra trade-offs e deixa a pessoa capaz de repetir o raciocínio sem depender dele.

**Nível 4, Cenário 3:** O learner revisa a forma como o time avalia C2. Ele identifica critério fraco, evidência enganosa ou métrica que envelheceu, propõe ajuste e acompanha se a nova avaliação prevê melhor o comportamento em produção.

#### 🔬 Como Coletar Evidências

**Para confirmar Nível 1:**
1. Peça uma explicação em voz alta com exemplo próprio de KODA.
2. Mostre um trace simples e peça para o learner nomear o problema.
3. Faça uma pergunta de contraste com outro conceito do currículo.
4. Registre se a resposta usa termos corretos sem depender de frases decoradas.

**Para confirmar Nível 2:**
1. Entregue um template funcional e peça uma adaptação pequena, mas realista.
2. Inclua um bug controlado ligado a planning separado de execution e observe o caminho de debug.
3. Peça que o learner explique cada mudança feita no PR.
4. Colete o diff, o teste ou a demonstração que prova o novo comportamento.

**Para confirmar Nível 3:**
1. Use um problema que não aparece nos exemplos do currículo.
2. Peça duas alternativas e uma justificativa explícita de escolha.
3. Exija métrica de sucesso, como queda em erros em cascata e aumento de conclusão correta de pedidos complexos.
4. Revise se a solução trata falhas prováveis, não apenas o happy path.

**Para confirmar Nível 4:**
1. Procure evidência de influência fora do próprio PR do learner.
2. Verifique se outra pessoa ou outro time adotou o padrão proposto.
3. Peça um relato de mentoria com antes, depois e evidência do mentorado.
4. Compare a proposta com dados de produção para ver se ela melhorou a prática do time.

#### 📈 Progressão Típica

A progressão em C2 costuma começar com vocabulário e reconhecimento de sintomas. Depois, o learner ganha confiança adaptando exemplos existentes e corrigindo bugs pequenos. O salto para Avançado acontece quando ele deixa de perguntar "qual template uso?" e passa a perguntar "qual decisão o domínio exige?". O salto para Expert aparece quando a melhoria deixa de ser pessoal e passa a mudar o modo como o time ensina, implementa e mede planning separado de execution.

---

### Conceito 3: Generator/Evaluator Pattern

**Definição:** O padrão arquitetural que separa a responsabilidade de **gerar** uma solução (Generator) da responsabilidade de **avaliar criticamente** essa solução (Evaluator). Resolve o problema de sycophancy — a tendência de um agente concordar com sua própria resposta e não detectar seus próprios erros.

**Por que importa para KODA:** Recomendações de produtos passaram de 75% para 98% de precisão quando KODA implementou G/E. O Generator cria opções sem se preocupar com perfeição; o Evaluator (independente e crítico) aprova ou rejeita com feedback específico.

#### Nível 1 — Básico

**Critérios:**
- Define o padrão Generator/Evaluator com terminologia correta
- Explica o problema de sycophancy e por que auto-avaliação é inerentemente limitada
- Descreve o fluxo: Generator gera → Evaluator avalia → aprova ou rejeita com feedback
- Identifica quando um sistema está sofrendo de self-evaluation collapse (ex: agente recomenda produto com lactose para cliente intolerante e "confirma" que está correto)
- Lista pelo menos 3 cenários KODA onde G/E é aplicável

**Evidências aceitáveis:**
- Explicação oral ou diagrama do fluxo G/E
- Consegue diferenciar G/E de "fazer dois prompts no mesmo agente"

**Armadilha comum:** Achar que G/E é "rodar o mesmo prompt duas vezes". A diferença fundamental é que Generator e Evaluator têm **incentivos diferentes** — o Generator quer criar, o Evaluator quer encontrar erros. Se os dois têm o mesmo system prompt, não há separação real.

#### Nível 2 — Intermediário

**Critérios:**
- Implementa um par Generator/Evaluator usando arquivos JSON como canal de comunicação
- Escreve uma rubrica simples para o Evaluator aplicar (ex: 5 critérios de verificação)
- Implementa o loop de feedback: Evaluator rejeita → Generator recebe feedback → Generator tenta novamente
- Configura thresholds de aprovação (ex: score ≥ 7.0) e max retries (ex: 3 tentativas)
- Lê e interpreta `evaluator_verdict.json` e `feedback.json` para entender por que algo foi rejeitado

**Evidências aceitáveis:**
- Código funcional de um par G/E que processa recomendações de produtos
- Demonstração do loop de feedback: recomendação com lactose é rejeitada, Generator refaz com produto vegano

**Armadilha comum:** Implementar o Evaluator como uma validação binária (pass/fail) em vez de um score com dimensões. Um Evaluator que só diz "reprovado" sem explicar por que é pouco útil para o Generator aprender.

#### Nível 3 — Avançado

**Critérios:**
- Projeta um sistema G/E com múltiplos Evaluators especializados (ex: um para safety, um para precisão, um para empatia)
- Implementa paralelização: múltiplos Evaluators rodam simultaneamente e consolidam resultados
- Calibra thresholds dinamicamente baseado no tipo de tarefa (ex: recomendação de produto tem threshold 7.0, processamento de pagamento tem threshold 9.0)
- Conecta G/E com Evaluation Rubrics (C8): o Evaluator usa rubrics formais, não critérios ad-hoc
- Mede o impacto do G/E com métricas: precisão, recall, falsos positivos/negativos do Evaluator
- Identifica quando o Evaluator está sendo muito permissivo (aprovando demais) ou muito restritivo (rejeitando demais)

**Evidências aceitáveis:**
- Sistema G/E com múltiplos evaluators e métricas de calibração
- Análise mostrando que o threshold foi ajustado para equilibrar precisão e latência
- Documentação de decisões de design (por que 3 evaluators, por que thresholds diferentes)

**Armadilha comum:** Criar um Evaluator que é essencialmente o Generator com um prompt diferente. O Evaluator precisa de acesso a dados que o Generator não tem (ex: informações nutricionais completas, histórico real de estoque, validação de preços em tempo real). Sem acesso a ground truth, o Evaluator é só outro agente opinando.

#### Nível 4 — Expert

**Critérios:**
- Projeta sistemas G/E adaptativos: o Evaluator aprende com seus próprios erros (ex: se aprovou algo que depois causou devolução, ajusta critérios)
- Cria padrões de G/E reutilizáveis com contratos bem definidos que outros times adotam
- Implementa avaliação cruzada: múltiplos pares G/E avaliam o mesmo input e os resultados são comparados para detectar viés
- Mentora outros engenheiros na arte de separar geração de avaliação
- Conecta G/E com Trace Reading e Harness Evolution: o harness analisa traces de G/E e sugere melhorias

**Evidências aceitáveis:**
- Framework de G/E usado em produção por múltiplos features do KODA
- Sistema de calibração automática de Evaluators com feedback loop de produção
- Case study documentado de evolução do G/E com melhorias mensuráveis



#### 📝 Exemplos Concretos por Nível

**Nível 1, Cenário 1:** Durante uma conversa de mentoria, você pergunta ao learner: "Por que self-evaluation falha em agentes?". A resposta menciona o conceito certo, usa os termos principais e conecta com KODA, mas fica no plano explicativo. O learner ainda não propõe mudança em código, não escolhe parâmetros e não aponta onde a decisão entraria no fluxo.

**Nível 1, Cenário 2:** Você mostra um trace curto de recomendação de produtos para cliente com restrição alimentar, orçamento e preferência de sabor. O learner reconhece o problema, nomeia o conceito C3 corretamente e explica por que ele importa. Quando você pergunta "qual arquivo você mudaria primeiro?", a resposta vira tentativa genérica ou pedido de exemplo pronto.

**Nível 1, Cenário 3:** Em uma sessão de grupo, o learner consegue comparar C3 com um conceito vizinho do currículo. A comparação é conceitualmente correta, mas ele ainda confunde sinais de diagnóstico com decisões de implementação quando o caso fica mais específico.

**Nível 2, Cenário 1:** Você entrega um exemplo funcional do time e pede para o learner adaptar o padrão para recomendação de produtos para cliente com restrição alimentar, orçamento e preferência de sabor. Ele segue o template, altera os campos certos, roda a validação esperada e explica o fluxo com segurança. Se você remove o template, ele demora para decidir a estrutura inicial.

**Nível 2, Cenário 2:** Você entrega um bug específico e pede para implementar loop de feedback quando o Evaluator rejeita uma recomendação com lactose. O learner encontra a falha, corrige sem mudar partes não relacionadas e registra a evidência do comportamento novo. A solução é correta, mas ainda espelha bastante o padrão existente.

**Nível 2, Cenário 3:** Em review, o learner sabe apontar qual critério da rubric foi atendido pelo PR. Ele também sabe dizer o que ainda não demonstrou para Nível 3, principalmente autonomia em domínio novo e justificativa de trade-offs.

**Nível 3, Cenário 1:** Você apresenta um problema novo e pergunta: "Como você projetaria Generator/Evaluator para isso?". O learner estrutura a solução sem template, escolhe alternativas com base em risco, latência, custo e qualidade, e explica por que descartou outras opções.

**Nível 3, Cenário 2:** Você pede para desenhar múltiplos Evaluators para safety, adequação comercial e empatia. O learner desenha a arquitetura, identifica pontos de falha, define métricas de sucesso e propõe como provar que a mudança melhorou o sistema. A conversa inclui limites da abordagem, não só benefícios.

**Nível 3, Cenário 3:** Durante um incidente, o learner usa `candidate_recommendation.json`, `evaluator_verdict.json`, feedback e histórico de retries para reconstruir causa raiz. Ele não para no sintoma. Ele conecta o bug a uma decisão de design e propõe uma correção que reduz a chance de repetição.

**Nível 4, Cenário 1:** O learner propõe calibração contínua de Evaluators com outcomes reais e análise de falsos positivos. A proposta não é só uma melhoria local. Ela vira padrão, biblioteca, guia interno ou decisão de arquitetura que outras pessoas conseguem reaplicar.

**Nível 4, Cenário 2:** Em uma sessão de mentoria, o learner guia outra pessoa do diagnóstico até a decisão de implementação. Ele faz perguntas, testa hipóteses, mostra trade-offs e deixa a pessoa capaz de repetir o raciocínio sem depender dele.

**Nível 4, Cenário 3:** O learner revisa a forma como o time avalia C3. Ele identifica critério fraco, evidência enganosa ou métrica que envelheceu, propõe ajuste e acompanha se a nova avaliação prevê melhor o comportamento em produção.

#### 🔬 Como Coletar Evidências

**Para confirmar Nível 1:**
1. Peça uma explicação em voz alta com exemplo próprio de KODA.
2. Mostre um trace simples e peça para o learner nomear o problema.
3. Faça uma pergunta de contraste com outro conceito do currículo.
4. Registre se a resposta usa termos corretos sem depender de frases decoradas.

**Para confirmar Nível 2:**
1. Entregue um template funcional e peça uma adaptação pequena, mas realista.
2. Inclua um bug controlado ligado a Generator/Evaluator e observe o caminho de debug.
3. Peça que o learner explique cada mudança feita no PR.
4. Colete o diff, o teste ou a demonstração que prova o novo comportamento.

**Para confirmar Nível 3:**
1. Use um problema que não aparece nos exemplos do currículo.
2. Peça duas alternativas e uma justificativa explícita de escolha.
3. Exija métrica de sucesso, como aumento de precisão das recomendações e queda de recomendações inseguras aprovadas.
4. Revise se a solução trata falhas prováveis, não apenas o happy path.

**Para confirmar Nível 4:**
1. Procure evidência de influência fora do próprio PR do learner.
2. Verifique se outra pessoa ou outro time adotou o padrão proposto.
3. Peça um relato de mentoria com antes, depois e evidência do mentorado.
4. Compare a proposta com dados de produção para ver se ela melhorou a prática do time.

#### 📈 Progressão Típica

A progressão em C3 costuma começar com vocabulário e reconhecimento de sintomas. Depois, o learner ganha confiança adaptando exemplos existentes e corrigindo bugs pequenos. O salto para Avançado acontece quando ele deixa de perguntar "qual template uso?" e passa a perguntar "qual decisão o domínio exige?". O salto para Expert aparece quando a melhoria deixa de ser pessoal e passa a mudar o modo como o time ensina, implementa e mede Generator/Evaluator.

---

### Conceito 4: Sprint Contracts

**Definição:** Contratos formais entre módulos ou agentes que especificam exatamente o que cada um espera receber (input contract) e o que promete entregar (output contract), incluindo garantias verificáveis. Eliminam "surpresas" entre módulos e transformam falhas silenciosas em erros ruidosos e rastreáveis.

**Por que importa para KODA:** Quando o módulo de busca entrega produtos sem o campo `lactose_free`, o módulo de recomendação não percebe e recomenda produtos perigosos. Com Sprint Contracts, o módulo de recomendação valida o input e rejeita imediatamente — falha rápido, não silenciosamente.

#### Nível 1 — Básico

**Critérios:**
- Define o que é um Sprint Contract e seus componentes: input contract, output contract, guarantees, validation
- Explica por que contratos previnem "surpresas" entre módulos
- Diferencia contrato de documentação: o contrato é validado em runtime, documentação não
- Identifica cenários onde a falta de contrato causou bugs (ex: "o módulo B esperava receber campo X mas o módulo A não enviava")

**Evidências aceitáveis:**
- Explicação oral com exemplo de input/output contract para um módulo KODA
- Consegue apontar onde um contrato quebrou em um trace de erro

**Armadilha comum:** Confundir contrato com type checking. Type checking (TypeScript, Pydantic) é uma implementação de contrato, mas o contrato é mais amplo — inclui garantias semânticas ("todos os produtos têm preço ≤ budget"), não apenas tipos ("price é number").

#### Nível 2 — Intermediário

**Critérios:**
- Escreve um input contract e output contract para um módulo usando JSON Schema ou Pydantic
- Implementa validação de contrato na entrada e saída de um módulo
- Consegue ler o output contract de um módulo upstream e derivar o input contract do módulo downstream
- Identifica quando um módulo violou seu contrato (ex: prometeu 3-10 produtos, entregou 2)
- Modifica contratos existentes para adicionar novos campos com backward compatibility

**Evidências aceitáveis:**
- Código com classes Pydantic que validam entrada e saída de um módulo KODA
- Teste que demonstra contrato sendo violado e erro sendo lançado claramente

**Armadilha comum:** Contratos muito rígidos que quebram com qualquer mudança. Um bom contrato é específico o suficiente para garantir qualidade, flexível o suficiente para evoluir. Ex: em vez de "exatamente 5 produtos", "entre 3 e 10 produtos".

#### Nível 3 — Avançado

**Critérios:**
- Projeta uma hierarquia de contratos para um pipeline de múltiplos módulos
- Implementa versionamento de contratos para permitir evolução sem quebrar consumidores
- Cria contratos com garantias semânticas complexas (ex: "todos os produtos recomendados são compatíveis com as restrições alimentares do cliente")
- Conecta Sprint Contracts com Planning/Execution (C2): contratos são a ponte formal entre Planner e Executor
- Mede o impacto de contratos: redução de bugs silenciosos, tempo de debug, segurança em refatorações

**Evidências aceitáveis:**
- Sistema com 4+ módulos encadeados, cada um com contratos validados, e um módulo upstream pode mudar sem quebrar downstream
- Documentação de design mostrando a hierarquia de contratos e justificativas

**Armadilha comum:** Contratos que validam estrutura mas não semântica. Um contrato que verifica "price é um número positivo" mas não verifica "price é consistente com a tabela de preços do catálogo" é um contrato fraco.

#### Nível 4 — Expert

**Critérios:**
- Projeta sistemas onde contratos são gerados ou evoluídos automaticamente a partir de traces de execução
- Cria padrões de contrato reutilizáveis que capturam conhecimento de domínio (ex: "Contract for KODA Product Recommendations")
- Implementa monitoramento de violações de contrato em produção com alertas
- Mentora outros engenheiros em design de contratos efetivos
- Conecta Sprint Contracts com Harness Evolution (C6): o harness analisa violações de contrato e sugere ajustes

**Evidências aceitáveis:**
- Sistema de contratos auto-evolutivos ou biblioteca de contratos padrão do time
- Dashboards de saúde de contratos em produção
- Histórico de mentoria com resultados



#### 📝 Exemplos Concretos por Nível

**Nível 1, Cenário 1:** Durante uma conversa de mentoria, você pergunta ao learner: "Qual diferença entre contrato, documentação e type checking?". A resposta menciona o conceito certo, usa os termos principais e conecta com KODA, mas fica no plano explicativo. O learner ainda não propõe mudança em código, não escolhe parâmetros e não aponta onde a decisão entraria no fluxo.

**Nível 1, Cenário 2:** Você mostra um trace curto de pipeline onde busca, recomendação, pagamento e fulfillment trocam dados estruturados. O learner reconhece o problema, nomeia o conceito C4 corretamente e explica por que ele importa. Quando você pergunta "qual arquivo você mudaria primeiro?", a resposta vira tentativa genérica ou pedido de exemplo pronto.

**Nível 1, Cenário 3:** Em uma sessão de grupo, o learner consegue comparar C4 com um conceito vizinho do currículo. A comparação é conceitualmente correta, mas ele ainda confunde sinais de diagnóstico com decisões de implementação quando o caso fica mais específico.

**Nível 2, Cenário 1:** Você entrega um exemplo funcional do time e pede para o learner adaptar o padrão para pipeline onde busca, recomendação, pagamento e fulfillment trocam dados estruturados. Ele segue o template, altera os campos certos, roda a validação esperada e explica o fluxo com segurança. Se você remove o template, ele demora para decidir a estrutura inicial.

**Nível 2, Cenário 2:** Você entrega um bug específico e pede para adicionar validação de input e output contract em um módulo que recebe produtos incompletos. O learner encontra a falha, corrige sem mudar partes não relacionadas e registra a evidência do comportamento novo. A solução é correta, mas ainda espelha bastante o padrão existente.

**Nível 2, Cenário 3:** Em review, o learner sabe apontar qual critério da rubric foi atendido pelo PR. Ele também sabe dizer o que ainda não demonstrou para Nível 3, principalmente autonomia em domínio novo e justificativa de trade-offs.

**Nível 3, Cenário 1:** Você apresenta um problema novo e pergunta: "Como você projetaria Sprint Contracts para isso?". O learner estrutura a solução sem template, escolhe alternativas com base em risco, latência, custo e qualidade, e explica por que descartou outras opções.

**Nível 3, Cenário 2:** Você pede para versionar contratos sem quebrar consumidores downstream durante mudança de schema. O learner desenha a arquitetura, identifica pontos de falha, define métricas de sucesso e propõe como provar que a mudança melhorou o sistema. A conversa inclui limites da abordagem, não só benefícios.

**Nível 3, Cenário 3:** Durante um incidente, o learner usa schema, teste de violação, erro lançado e changelog de versão do contrato para reconstruir causa raiz. Ele não para no sintoma. Ele conecta o bug a uma decisão de design e propõe uma correção que reduz a chance de repetição.

**Nível 4, Cenário 1:** O learner cria uma biblioteca de contratos de domínio com garantias semânticas para recomendações KODA. A proposta não é só uma melhoria local. Ela vira padrão, biblioteca, guia interno ou decisão de arquitetura que outras pessoas conseguem reaplicar.

**Nível 4, Cenário 2:** Em uma sessão de mentoria, o learner guia outra pessoa do diagnóstico até a decisão de implementação. Ele faz perguntas, testa hipóteses, mostra trade-offs e deixa a pessoa capaz de repetir o raciocínio sem depender dele.

**Nível 4, Cenário 3:** O learner revisa a forma como o time avalia C4. Ele identifica critério fraco, evidência enganosa ou métrica que envelheceu, propõe ajuste e acompanha se a nova avaliação prevê melhor o comportamento em produção.

#### 🔬 Como Coletar Evidências

**Para confirmar Nível 1:**
1. Peça uma explicação em voz alta com exemplo próprio de KODA.
2. Mostre um trace simples e peça para o learner nomear o problema.
3. Faça uma pergunta de contraste com outro conceito do currículo.
4. Registre se a resposta usa termos corretos sem depender de frases decoradas.

**Para confirmar Nível 2:**
1. Entregue um template funcional e peça uma adaptação pequena, mas realista.
2. Inclua um bug controlado ligado a Sprint Contracts e observe o caminho de debug.
3. Peça que o learner explique cada mudança feita no PR.
4. Colete o diff, o teste ou a demonstração que prova o novo comportamento.

**Para confirmar Nível 3:**
1. Use um problema que não aparece nos exemplos do currículo.
2. Peça duas alternativas e uma justificativa explícita de escolha.
3. Exija métrica de sucesso, como redução de bugs silenciosos entre módulos e tempo médio de debug.
4. Revise se a solução trata falhas prováveis, não apenas o happy path.

**Para confirmar Nível 4:**
1. Procure evidência de influência fora do próprio PR do learner.
2. Verifique se outra pessoa ou outro time adotou o padrão proposto.
3. Peça um relato de mentoria com antes, depois e evidência do mentorado.
4. Compare a proposta com dados de produção para ver se ela melhorou a prática do time.

#### 📈 Progressão Típica

A progressão em C4 costuma começar com vocabulário e reconhecimento de sintomas. Depois, o learner ganha confiança adaptando exemplos existentes e corrigindo bugs pequenos. O salto para Avançado acontece quando ele deixa de perguntar "qual template uso?" e passa a perguntar "qual decisão o domínio exige?". O salto para Expert aparece quando a melhoria deixa de ser pessoal e passa a mudar o modo como o time ensina, implementa e mede Sprint Contracts.

---

### Conceito 5: State Persistence

**Definição:** A prática de armazenar informações críticas fora da context window do agente — em arquivos, bancos de dados ou sistemas de cache — garantindo que dados essenciais sobrevivam a conversas longas, reinicializações e mudanças de contexto. Complementa Context Management (C1) provendo uma camada de memória de longo prazo.

**Por que importa para KODA:** Alergias de clientes, preferências de sabor, histórico de compras e promessas de entrega não podem depender apenas da memória de curto prazo do agente. Se KODA "esquece" que o cliente é alérgico a amendoim, as consequências vão além de uma venda perdida — são riscos à saúde.

#### Nível 1 — Básico

**Critérios:**
- Define state persistence e diferencia de context window
- Explica por que "guardar tudo na conversa" não é suficiente para agentes long-running
- Identifica que tipos de dados devem ser persistidos (alergias, preferências, promessas, estado de pedidos)
- Reconhece o padrão de leitura de estado no início de uma interação e escrita no final
- Lista formatos comuns de persistência (JSON, SQLite, Redis) e seus trade-offs básicos

**Evidências aceitáveis:**
- Explicação com exemplo: "se o cliente diz que é alérgico a glúten no minuto 5, como garantir que KODA lembre no minuto 120?"
- Consegue identificar em um trace quando o estado deveria ter sido lido mas não foi

**Armadilha comum:** Achar que state persistence é "salvar a conversa inteira". State persistence é sobre extrair e armazenar informações **estruturadas e semanticamente relevantes**, não sobre backup bruto de mensagens.

#### Nível 2 — Intermediário

**Critérios:**
- Implementa leitura e escrita de estado usando arquivos JSON (ex: `customer_context.json`)
- Projeta um schema de estado simples com campos relevantes (ex: alergias, orçamento, preferências)
- Implementa atualização de estado: novos campos são adicionados sem perder dados existentes
- Conecta state persistence com Context Management: o estado persistido é injetado no contexto do agente no início de cada interação
- Debuga problemas de estado: "por que o agente usou o orçamento antigo em vez do novo?"

**Evidências aceitáveis:**
- Código que lê `customer_context.json`, processa uma interação, e atualiza o arquivo com novos dados
- Demonstração de que o agente "lembra" de informação persistida mesmo após reinicialização

**Armadilha comum:** Persistir estado mas não versionar. Se o formato do estado muda (ex: adiciona campo `dietary_preferences`), código antigo quebra ao ler o novo formato. Versionamento de schema é essencial.

#### Nível 3 — Avançado

**Critérios:**
- Projeta uma arquitetura de estado em múltiplas camadas: hot state (sessão atual), warm state (últimas N sessões), cold state (histórico completo)
- Implementa estratégias de invalidação de estado: quando uma informação expira? (ex: promoção válida até data X)
- Gerencia conflitos de estado: o que acontece quando duas interações concorrentes tentam atualizar o mesmo campo?
- Conecta State Persistence com Multi-Agent Coordination (C7): como estado é compartilhado e sincronizado entre agentes
- Mede a efetividade: latência de leitura/escrita, taxa de cache hit, consistência de estado

**Evidências aceitáveis:**
- Arquitetura documentada de camadas de estado com políticas de expiração e conflito
- Sistema que sobrevive a condições de borda: escrita concorrente, corrupção de arquivo, migração de schema

**Armadilha comum:** Tratar estado como cache simples. Estado persistente é fonte de verdade — se o cache e o estado divergem, o estado vence. Confundir os dois leva a bugs sutis onde o agente age baseado em dados stale.

#### Nível 4 — Expert

**Critérios:**
- Projeta sistemas de estado distribuído onde múltiplos agentes leem e escrevem com garantias de consistência
- Implementa estratégias de migração de estado sem downtime (ex: old schema → new schema com leitura dual-write)
- Cria padrões de state persistence reutilizáveis que capturam decisões de design (ex: "KODA State Contract")
- Mentora outros engenheiros em design de persistência para agentes
- Conecta State Persistence com Harness Evolution (C6): o harness monitora saúde do estado e sugere otimizações

**Evidências aceitáveis:**
- Sistema de estado em produção com 99.9%+ de disponibilidade e zero corrupção de dados
- Biblioteca interna de padrões de persistência
- Case study de migração de schema sem impacto para clientes



#### 📝 Exemplos Concretos por Nível

**Nível 1, Cenário 1:** Durante uma conversa de mentoria, você pergunta ao learner: "O que deve sair da conversa e virar estado persistente?". A resposta menciona o conceito certo, usa os termos principais e conecta com KODA, mas fica no plano explicativo. O learner ainda não propõe mudança em código, não escolhe parâmetros e não aponta onde a decisão entraria no fluxo.

**Nível 1, Cenário 2:** Você mostra um trace curto de cliente retorna depois de reinício do agente e espera que alergias, orçamento e promessas sejam lembradas. O learner reconhece o problema, nomeia o conceito C5 corretamente e explica por que ele importa. Quando você pergunta "qual arquivo você mudaria primeiro?", a resposta vira tentativa genérica ou pedido de exemplo pronto.

**Nível 1, Cenário 3:** Em uma sessão de grupo, o learner consegue comparar C5 com um conceito vizinho do currículo. A comparação é conceitualmente correta, mas ele ainda confunde sinais de diagnóstico com decisões de implementação quando o caso fica mais específico.

**Nível 2, Cenário 1:** Você entrega um exemplo funcional do time e pede para o learner adaptar o padrão para cliente retorna depois de reinício do agente e espera que alergias, orçamento e promessas sejam lembradas. Ele segue o template, altera os campos certos, roda a validação esperada e explica o fluxo com segurança. Se você remove o template, ele demora para decidir a estrutura inicial.

**Nível 2, Cenário 2:** Você entrega um bug específico e pede para corrigir leitura e escrita de `customer_context.json` sem perder campos existentes. O learner encontra a falha, corrige sem mudar partes não relacionadas e registra a evidência do comportamento novo. A solução é correta, mas ainda espelha bastante o padrão existente.

**Nível 2, Cenário 3:** Em review, o learner sabe apontar qual critério da rubric foi atendido pelo PR. Ele também sabe dizer o que ainda não demonstrou para Nível 3, principalmente autonomia em domínio novo e justificativa de trade-offs.

**Nível 3, Cenário 1:** Você apresenta um problema novo e pergunta: "Como você projetaria state persistence para isso?". O learner estrutura a solução sem template, escolhe alternativas com base em risco, latência, custo e qualidade, e explica por que descartou outras opções.

**Nível 3, Cenário 2:** Você pede para desenhar hot state, warm state e cold state com expiração e resolução de conflitos. O learner desenha a arquitetura, identifica pontos de falha, define métricas de sucesso e propõe como provar que a mudança melhorou o sistema. A conversa inclui limites da abordagem, não só benefícios.

**Nível 3, Cenário 3:** Durante um incidente, o learner usa arquivo de estado, schema versionado, logs de migração e trace de recuperação para reconstruir causa raiz. Ele não para no sintoma. Ele conecta o bug a uma decisão de design e propõe uma correção que reduz a chance de repetição.

**Nível 4, Cenário 1:** O learner planeja migração de schema sem downtime com dual read, dual write e validação de consistência. A proposta não é só uma melhoria local. Ela vira padrão, biblioteca, guia interno ou decisão de arquitetura que outras pessoas conseguem reaplicar.

**Nível 4, Cenário 2:** Em uma sessão de mentoria, o learner guia outra pessoa do diagnóstico até a decisão de implementação. Ele faz perguntas, testa hipóteses, mostra trade-offs e deixa a pessoa capaz de repetir o raciocínio sem depender dele.

**Nível 4, Cenário 3:** O learner revisa a forma como o time avalia C5. Ele identifica critério fraco, evidência enganosa ou métrica que envelheceu, propõe ajuste e acompanha se a nova avaliação prevê melhor o comportamento em produção.

#### 🔬 Como Coletar Evidências

**Para confirmar Nível 1:**
1. Peça uma explicação em voz alta com exemplo próprio de KODA.
2. Mostre um trace simples e peça para o learner nomear o problema.
3. Faça uma pergunta de contraste com outro conceito do currículo.
4. Registre se a resposta usa termos corretos sem depender de frases decoradas.

**Para confirmar Nível 2:**
1. Entregue um template funcional e peça uma adaptação pequena, mas realista.
2. Inclua um bug controlado ligado a state persistence e observe o caminho de debug.
3. Peça que o learner explique cada mudança feita no PR.
4. Colete o diff, o teste ou a demonstração que prova o novo comportamento.

**Para confirmar Nível 3:**
1. Use um problema que não aparece nos exemplos do currículo.
2. Peça duas alternativas e uma justificativa explícita de escolha.
3. Exija métrica de sucesso, como consistência de estado, latência de leitura e ausência de dados críticos perdidos.
4. Revise se a solução trata falhas prováveis, não apenas o happy path.

**Para confirmar Nível 4:**
1. Procure evidência de influência fora do próprio PR do learner.
2. Verifique se outra pessoa ou outro time adotou o padrão proposto.
3. Peça um relato de mentoria com antes, depois e evidência do mentorado.
4. Compare a proposta com dados de produção para ver se ela melhorou a prática do time.

#### 📈 Progressão Típica

A progressão em C5 costuma começar com vocabulário e reconhecimento de sintomas. Depois, o learner ganha confiança adaptando exemplos existentes e corrigindo bugs pequenos. O salto para Avançado acontece quando ele deixa de perguntar "qual template uso?" e passa a perguntar "qual decisão o domínio exige?". O salto para Expert aparece quando a melhoria deixa de ser pessoal e passa a mudar o modo como o time ensina, implementa e mede state persistence.

---

### Conceito 6: Harness Evolution

**Definição:** A disciplina de projetar, monitorar e evoluir o "harness" — o conjunto de validações, checkpoints, contratos e guardrails que envolvem um agente e garantem que ele opere dentro de limites seguros e eficazes. O harness não é estático; ele evolui conforme o agente encontra novos cenários, novos modelos são lançados e os requisitos de negócio mudam.

**Por que importa para KODA:** Um harness que validava 5 critérios em janeiro pode precisar validar 15 em junho, quando novos produtos, novas restrições regulatórias e novos padrões de qualidade são introduzidos. Sem evolução consciente, o harness se torna obsoleto e o agente opera sem guardrails efetivos.

#### Nível 1 — Básico

**Critérios:**
- Define o que é um harness no contexto de agentes long-running
- Explica a diferença entre "agente funcionando" e "agente operando com harness"
- Lista os componentes típicos de um harness: validações, checkpoints, contratos, limites de retry, timeouts
- Identifica o que acontece quando um harness está ausente ou fraco (ex: agente recomenda produto indisponível)
- Entende que harness não é código do agente — é código ao redor do agente

**Evidências aceitáveis:**
- Explicação com exemplo: "se o KODA recomendar um produto, o harness verifica se o produto existe, está em estoque e respeita restrições"
- Consegue apontar onde um harness falhou em um trace de incidente

**Armadilha comum:** Achar que o harness é "o prompt do sistema". O harness inclui o prompt, mas também inclui validações pós-geração, checkpoints de estado, limites de segurança e monitoramento. O prompt é um componente do harness, não o harness inteiro.

#### Nível 2 — Intermediário

**Critérios:**
- Modifica um harness existente para adicionar uma nova validação (ex: "agora precisamos verificar se o produto é adequado para gestantes")
- Ajusta thresholds e limites do harness (ex: aumentar max_retries de 3 para 5 para um caso específico)
- Monitora a saúde do harness: quantas validações estão passando/falhando? Onde estão os gargalos?
- Identifica quando uma validação do harness está gerando falsos positivos (rejeitando coisas boas)
- Documenta mudanças no harness com justificativa

**Evidências aceitáveis:**
- PR que adiciona uma validação ao harness com testes que demonstram o novo comportamento
- Relatório de saúde do harness mostrando taxas de aprovação/rejeição

**Armadilha comum:** Adicionar validações sem remover as obsoletas. Com o tempo, o harness acumula "sedimento" — validações que já não fazem sentido mas ninguém removeu. Isso aumenta latência e falsos positivos.

#### Nível 3 — Avançado

**Critérios:**
- Projeta uma estratégia de evolução de harness: como decidir quando adicionar, modificar ou remover validações
- Implementa A/B testing de harness: duas versões do harness rodam em paralelo e métricas determinam qual é melhor
- Conecta Harness Evolution com Trace Reading: analisa traces para identificar padrões de falha que o harness deveria capturar
- Conecta com Evaluation Rubrics (C8): o harness usa rubrics para avaliar outputs, e as rubrics evoluem com o harness
- Mede o impacto de mudanças no harness: "após adicionar validação de restrições alimentares, reclamações caíram 40%"

**Evidências aceitáveis:**
- Documento de estratégia de evolução do harness com critérios de decisão
- Resultados de A/B test mostrando melhoria mensurável após evolução do harness
- Sistema onde o harness evoluiu 3+ vezes com melhorias documentadas em cada iteração

**Armadilha comum:** Evoluir o harness reativamente (após incidentes) em vez de proativamente (analisando tendências). Um harness que só muda depois que algo quebra está sempre um passo atrás dos problemas.

#### Nível 4 — Expert

**Critérios:**
- Projeta harnesses que se auto-calibram: o harness ajusta seus próprios thresholds baseado em feedback de produção
- Cria um framework de harness evolution usado por múltiplos times
- Implementa detecção automática de "harness drift" — quando o harness está se tornando menos efetivo
- Mentora outros engenheiros em design e evolução de harnesses
- Publica padrões e aprendizados sobre evolução de harness que influenciam a arquitetura do KODA

**Evidências aceitáveis:**
- Framework de harness auto-evolutivo ou biblioteca de componentes de harness
- Sistema de detecção de harness drift com alertas
- Case study de evolução de harness que resultou em melhoria significativa e sustentada



#### 📝 Exemplos Concretos por Nível

**Nível 1, Cenário 1:** Durante uma conversa de mentoria, você pergunta ao learner: "O que faz parte do harness além do prompt?". A resposta menciona o conceito certo, usa os termos principais e conecta com KODA, mas fica no plano explicativo. O learner ainda não propõe mudança em código, não escolhe parâmetros e não aponta onde a decisão entraria no fluxo.

**Nível 1, Cenário 2:** Você mostra um trace curto de harness de recomendação que precisa acompanhar catálogo novo, regras novas e mudança no modelo. O learner reconhece o problema, nomeia o conceito C6 corretamente e explica por que ele importa. Quando você pergunta "qual arquivo você mudaria primeiro?", a resposta vira tentativa genérica ou pedido de exemplo pronto.

**Nível 1, Cenário 3:** Em uma sessão de grupo, o learner consegue comparar C6 com um conceito vizinho do currículo. A comparação é conceitualmente correta, mas ele ainda confunde sinais de diagnóstico com decisões de implementação quando o caso fica mais específico.

**Nível 2, Cenário 1:** Você entrega um exemplo funcional do time e pede para o learner adaptar o padrão para harness de recomendação que precisa acompanhar catálogo novo, regras novas e mudança no modelo. Ele segue o template, altera os campos certos, roda a validação esperada e explica o fluxo com segurança. Se você remove o template, ele demora para decidir a estrutura inicial.

**Nível 2, Cenário 2:** Você entrega um bug específico e pede para adicionar uma validação nova e medir se ela gera falsos positivos. O learner encontra a falha, corrige sem mudar partes não relacionadas e registra a evidência do comportamento novo. A solução é correta, mas ainda espelha bastante o padrão existente.

**Nível 2, Cenário 3:** Em review, o learner sabe apontar qual critério da rubric foi atendido pelo PR. Ele também sabe dizer o que ainda não demonstrou para Nível 3, principalmente autonomia em domínio novo e justificativa de trade-offs.

**Nível 3, Cenário 1:** Você apresenta um problema novo e pergunta: "Como você projetaria harness evolution para isso?". O learner estrutura a solução sem template, escolhe alternativas com base em risco, latência, custo e qualidade, e explica por que descartou outras opções.

**Nível 3, Cenário 2:** Você pede para planejar quando adicionar, alterar ou remover validações com base em traces e métricas. O learner desenha a arquitetura, identifica pontos de falha, define métricas de sucesso e propõe como provar que a mudança melhorou o sistema. A conversa inclui limites da abordagem, não só benefícios.

**Nível 3, Cenário 3:** Durante um incidente, o learner usa configuração do harness, relatório de aprovação, amostras rejeitadas e decisão de mudança para reconstruir causa raiz. Ele não para no sintoma. Ele conecta o bug a uma decisão de design e propõe uma correção que reduz a chance de repetição.

**Nível 4, Cenário 1:** O learner cria detecção de harness drift e processo de recalibração usado por múltiplos times. A proposta não é só uma melhoria local. Ela vira padrão, biblioteca, guia interno ou decisão de arquitetura que outras pessoas conseguem reaplicar.

**Nível 4, Cenário 2:** Em uma sessão de mentoria, o learner guia outra pessoa do diagnóstico até a decisão de implementação. Ele faz perguntas, testa hipóteses, mostra trade-offs e deixa a pessoa capaz de repetir o raciocínio sem depender dele.

**Nível 4, Cenário 3:** O learner revisa a forma como o time avalia C6. Ele identifica critério fraco, evidência enganosa ou métrica que envelheceu, propõe ajuste e acompanha se a nova avaliação prevê melhor o comportamento em produção.

#### 🔬 Como Coletar Evidências

**Para confirmar Nível 1:**
1. Peça uma explicação em voz alta com exemplo próprio de KODA.
2. Mostre um trace simples e peça para o learner nomear o problema.
3. Faça uma pergunta de contraste com outro conceito do currículo.
4. Registre se a resposta usa termos corretos sem depender de frases decoradas.

**Para confirmar Nível 2:**
1. Entregue um template funcional e peça uma adaptação pequena, mas realista.
2. Inclua um bug controlado ligado a harness evolution e observe o caminho de debug.
3. Peça que o learner explique cada mudança feita no PR.
4. Colete o diff, o teste ou a demonstração que prova o novo comportamento.

**Para confirmar Nível 3:**
1. Use um problema que não aparece nos exemplos do currículo.
2. Peça duas alternativas e uma justificativa explícita de escolha.
3. Exija métrica de sucesso, como queda de incidentes capturados tarde e estabilidade da taxa de rejeição útil.
4. Revise se a solução trata falhas prováveis, não apenas o happy path.

**Para confirmar Nível 4:**
1. Procure evidência de influência fora do próprio PR do learner.
2. Verifique se outra pessoa ou outro time adotou o padrão proposto.
3. Peça um relato de mentoria com antes, depois e evidência do mentorado.
4. Compare a proposta com dados de produção para ver se ela melhorou a prática do time.

#### 📈 Progressão Típica

A progressão em C6 costuma começar com vocabulário e reconhecimento de sintomas. Depois, o learner ganha confiança adaptando exemplos existentes e corrigindo bugs pequenos. O salto para Avançado acontece quando ele deixa de perguntar "qual template uso?" e passa a perguntar "qual decisão o domínio exige?". O salto para Expert aparece quando a melhoria deixa de ser pessoal e passa a mudar o modo como o time ensina, implementa e mede harness evolution.

---

### Conceito 7: Multi-Agent Coordination

**Definição:** A disciplina de projetar sistemas onde múltiplos agentes colaboram para resolver problemas que um agente sozinho não consegue — ou não consegue com qualidade suficiente. Envolve topologias de comunicação (pipeline, star, mesh), protocolos de coordenação (file-based, message-based, orchestrated) e estratégias de resolução de conflitos entre agentes.

**Por que importa para KODA:** Um pedido complexo pode envolver um agente de busca de produtos, um de validação de estoque, um de cálculo de frete e um de processamento de pagamento. Coordená-los sem que pisem no trabalho uns dos outros é o que separa um sistema que escala de um que colapsa.

#### Nível 1 — Básico

**Critérios:**
- Define multi-agent coordination e explica por que agentes únicos têm limites
- Lista pelo menos 2 topologias de coordenação (ex: pipeline sequencial, orquestrador central)
- Explica a diferença entre coordenação por arquivos, mensagens e orquestração
- Identifica cenários KODA onde múltiplos agentes são necessários (ex: fulfillment same-day)
- Entende os riscos de coordenação: race conditions, deadlocks, agentes "fantasmas"

**Evidências aceitáveis:**
- Explicação com exemplo: "para processar um pedido com same-day delivery, um agente busca estoque, outro calcula rota, outro aloca entregador, e um quarto orquestra"
- Consegue desenhar um diagrama simples de coordenação entre 3 agentes

**Armadilha comum:** Achar que multi-agent é só "rodar vários agentes ao mesmo tempo". A complexidade está na coordenação — como eles compartilham estado, como resolvem conflitos, como garantem que o trabalho de um não invalida o do outro.

#### Nível 2 — Intermediário

**Critérios:**
- Implementa coordenação simples entre 2 agentes usando arquivos como canal (ex: Agent A escreve resultado em JSON, Agent B lê e processa)
- Implementa um orquestrador básico que dispara agentes em sequência e coleta resultados
- Lida com falha de um agente: o que acontece se Agent B falha? O orquestrador detecta e retry?
- Usa audit log (JSONL) para rastrear o fluxo de coordenação
- Identifica gargalos de coordenação: onde o pipeline está serializado desnecessariamente?

**Evidências aceitáveis:**
- Sistema com 2-3 agentes coordenados via arquivos que completa uma tarefa de ponta a ponta
- Audit log mostrando o fluxo completo com timestamps

**Armadilha comum:** Coordenação sequencial desnecessária. Se o Agent B não depende do resultado do Agent A, eles deveriam rodar em paralelo. Coordenação sequencial onde paralelismo é possível é desperdício de latência.

#### Nível 3 — Avançado

**Critérios:**
- Projeta topologias de coordenação adequadas ao problema: escolhe entre pipeline, star, mesh ou híbrida com justificativa
- Implementa coordenação com paralelismo: múltiplos agentes rodam simultaneamente e um coletor agrega resultados
- Projeta estratégias de failure handling: retry, fallback, graceful degradation, circuit breaker
- Conecta Multi-Agent Coordination com State Persistence (C5): como estado é compartilhado entre agentes sem conflitos
- Conecta com Generator/Evaluator (C3): múltiplos Generators podem alimentar um Evaluator central
- Mede eficiência: tempo total vs tempo de cada agente, overhead de coordenação, taxa de conflitos

**Evidências aceitáveis:**
- Sistema multi-agente com 4+ agentes, paralelismo onde apropriado, e estratégia de failure handling
- Documentação de design justificando a topologia escolhida com trade-offs

**Armadilha comum:** Over-engineering de coordenação. Para 3 agentes que rodam em sequência, file-based coordination é suficiente. Implementar um message broker (Redis, RabbitMQ) para esse caso é complexidade desnecessária.

#### Nível 4 — Expert

**Critérios:**
- Projeta sistemas onde a topologia de coordenação se adapta dinamicamente à carga (ex: em horário de pico, mais agentes de busca são spawnados)
- Cria padrões de coordenação reutilizáveis: "KODA Order Processing Topology", "KODA Fulfillment Mesh"
- Implementa coordenação com garantias de consistência (ex: exactly-once processing)
- Mentora outros engenheiros em design de sistemas multi-agente
- Conecta Multi-Agent Coordination com Harness Evolution (C6): o harness monitora a saúde da coordenação

**Evidências aceitáveis:**
- Framework de coordenação multi-agente usado em produção
- Sistema que escala dinamicamente com carga sem intervenção manual
- Case study de evolução de coordenação com métricas de melhoria



#### 📝 Exemplos Concretos por Nível

**Nível 1, Cenário 1:** Durante uma conversa de mentoria, você pergunta ao learner: "Por que rodar vários agentes não basta?". A resposta menciona o conceito certo, usa os termos principais e conecta com KODA, mas fica no plano explicativo. O learner ainda não propõe mudança em código, não escolhe parâmetros e não aponta onde a decisão entraria no fluxo.

**Nível 1, Cenário 2:** Você mostra um trace curto de pedido same-day com agentes de estoque, rota, pagamento, atendimento e orquestração. O learner reconhece o problema, nomeia o conceito C7 corretamente e explica por que ele importa. Quando você pergunta "qual arquivo você mudaria primeiro?", a resposta vira tentativa genérica ou pedido de exemplo pronto.

**Nível 1, Cenário 3:** Em uma sessão de grupo, o learner consegue comparar C7 com um conceito vizinho do currículo. A comparação é conceitualmente correta, mas ele ainda confunde sinais de diagnóstico com decisões de implementação quando o caso fica mais específico.

**Nível 2, Cenário 1:** Você entrega um exemplo funcional do time e pede para o learner adaptar o padrão para pedido same-day com agentes de estoque, rota, pagamento, atendimento e orquestração. Ele segue o template, altera os campos certos, roda a validação esperada e explica o fluxo com segurança. Se você remove o template, ele demora para decidir a estrutura inicial.

**Nível 2, Cenário 2:** Você entrega um bug específico e pede para debuggar coordenação por arquivos onde Agent B lê resultado parcial de Agent A. O learner encontra a falha, corrige sem mudar partes não relacionadas e registra a evidência do comportamento novo. A solução é correta, mas ainda espelha bastante o padrão existente.

**Nível 2, Cenário 3:** Em review, o learner sabe apontar qual critério da rubric foi atendido pelo PR. Ele também sabe dizer o que ainda não demonstrou para Nível 3, principalmente autonomia em domínio novo e justificativa de trade-offs.

**Nível 3, Cenário 1:** Você apresenta um problema novo e pergunta: "Como você projetaria multi-agent coordination para isso?". O learner estrutura a solução sem template, escolhe alternativas com base em risco, latência, custo e qualidade, e explica por que descartou outras opções.

**Nível 3, Cenário 2:** Você pede para escolher topologia pipeline, star, mesh ou híbrida com paralelismo seguro. O learner desenha a arquitetura, identifica pontos de falha, define métricas de sucesso e propõe como provar que a mudança melhorou o sistema. A conversa inclui limites da abordagem, não só benefícios.

**Nível 3, Cenário 3:** Durante um incidente, o learner usa audit log JSONL, arquivos de handoff, estado compartilhado e diagrama de topologia para reconstruir causa raiz. Ele não para no sintoma. Ele conecta o bug a uma decisão de design e propõe uma correção que reduz a chance de repetição.

**Nível 4, Cenário 1:** O learner propõe coordenação adaptativa com garantias de consistência e monitoramento de conflitos. A proposta não é só uma melhoria local. Ela vira padrão, biblioteca, guia interno ou decisão de arquitetura que outras pessoas conseguem reaplicar.

**Nível 4, Cenário 2:** Em uma sessão de mentoria, o learner guia outra pessoa do diagnóstico até a decisão de implementação. Ele faz perguntas, testa hipóteses, mostra trade-offs e deixa a pessoa capaz de repetir o raciocínio sem depender dele.

**Nível 4, Cenário 3:** O learner revisa a forma como o time avalia C7. Ele identifica critério fraco, evidência enganosa ou métrica que envelheceu, propõe ajuste e acompanha se a nova avaliação prevê melhor o comportamento em produção.

#### 🔬 Como Coletar Evidências

**Para confirmar Nível 1:**
1. Peça uma explicação em voz alta com exemplo próprio de KODA.
2. Mostre um trace simples e peça para o learner nomear o problema.
3. Faça uma pergunta de contraste com outro conceito do currículo.
4. Registre se a resposta usa termos corretos sem depender de frases decoradas.

**Para confirmar Nível 2:**
1. Entregue um template funcional e peça uma adaptação pequena, mas realista.
2. Inclua um bug controlado ligado a multi-agent coordination e observe o caminho de debug.
3. Peça que o learner explique cada mudança feita no PR.
4. Colete o diff, o teste ou a demonstração que prova o novo comportamento.

**Para confirmar Nível 3:**
1. Use um problema que não aparece nos exemplos do currículo.
2. Peça duas alternativas e uma justificativa explícita de escolha.
3. Exija métrica de sucesso, como redução de overhead de coordenação e queda de conflitos entre agentes.
4. Revise se a solução trata falhas prováveis, não apenas o happy path.

**Para confirmar Nível 4:**
1. Procure evidência de influência fora do próprio PR do learner.
2. Verifique se outra pessoa ou outro time adotou o padrão proposto.
3. Peça um relato de mentoria com antes, depois e evidência do mentorado.
4. Compare a proposta com dados de produção para ver se ela melhorou a prática do time.

#### 📈 Progressão Típica

A progressão em C7 costuma começar com vocabulário e reconhecimento de sintomas. Depois, o learner ganha confiança adaptando exemplos existentes e corrigindo bugs pequenos. O salto para Avançado acontece quando ele deixa de perguntar "qual template uso?" e passa a perguntar "qual decisão o domínio exige?". O salto para Expert aparece quando a melhoria deixa de ser pessoal e passa a mudar o modo como o time ensina, implementa e mede multi-agent coordination.

---

### Conceito 8: Evaluation Rubrics

**Definição:** A disciplina de criar critérios estruturados, ponderados e calibrados para avaliar a qualidade de outputs de agentes em múltiplas dimensões simultaneamente. Diferente de validação binária (pass/fail), rubrics capturam nuances de qualidade — um output pode ser "válido mas ruim" ou "tecnicamente correto mas inadequado para o cliente".

**Por que importa para KODA:** Uma recomendação pode passar em todas as validações (produto existe, preço ok, em estoque) e ainda assim ser ruim (não considera preferência de sabor, ignora restrição alimentar, sugere produto com histórico de devoluções). Rubrics detectam o que validações não veem.

#### Nível 1 — Básico

**Critérios:**
- Define o que é uma evaluation rubric e diferencia de validação binária (pass/fail)
- Lista os componentes de uma rubric: dimensions, weights, scoring levels, thresholds, anchors, evidence rules
- Explica por que "passou na validação" não significa "é uma boa recomendação"
- Identifica exemplos de outputs que passam validação mas falhariam em uma rubric (ex: recomendar whey com lactose para intolerante)
- Entende que rubrics medem qualidade em um espectro, não em binário

**Evidências aceitáveis:**
- Explicação com exemplo: "um output pode ter score 72/100 — é válido, mas abaixo do threshold de qualidade"
- Consegue diferenciar "válido" de "bom" em exemplos concretos

**Armadilha comum:** Criar rubrics que são essencialmente checklists de validação com scores. Uma rubric de verdade avalia dimensões que validação binária não alcança: adequação ao cliente, clareza da explicação, empatia, segurança contextual.

#### Nível 2 — Intermediário

**Critérios:**
- Cria uma rubric com 3-5 dimensions, weights e scoring levels (1-5) para um caso KODA
- Define anchors: descrições concretas do que significa cada nível de score (ex: "score 5 em lactose_free = produto é certificado sem lactose; score 1 = produto contém lactose")
- Aplica a rubric em outputs reais e obtém scores consistentes (aplicando duas vezes, scores similares)
- Ajusta weights baseado em prioridades de negócio (ex: safety weight sobe para 40% em recomendações para alérgicos)
- Usa a rubric como parte de um Evaluator no padrão Generator/Evaluator

**Evidências aceitáveis:**
- Rubric documentada com dimensions, weights, levels e anchors para recomendação de produtos KODA
- Demonstração de aplicação consistente (scores similares em avaliações repetidas)

**Armadilha comum:** Rubrics com weights arbitrários ("35% para adequação porque parece certo"). Bons weights são calibrados com dados: quantas recomendações ruins foram causadas por falha em cada dimensão? As dimensões que mais causam falhas deveriam ter weights maiores.

#### Nível 3 — Avançado

**Critérios:**
- Projeta rubrics com calibração baseada em dados: analisa histórico de falhas para determinar weights
- Cria rubrics adaptativas: thresholds diferentes para contextos diferentes (ex: threshold 8.0 para produtos alimentícios, 6.0 para acessórios)
- Conecta Evaluation Rubrics com Trace Reading: usa traces para identificar dimensões que a rubric atual não cobre
- Implementa revisão de rubrics: periodicamente, compara scores da rubric com outcomes reais (satisfação do cliente, devoluções) e ajusta
- Mede a efetividade da rubric: correlação entre score da rubric e satisfação real do cliente

**Evidências aceitáveis:**
- Rubric com weights calibrados por dados históricos e justificativa documentada
- Análise de correlação entre scores da rubric e outcomes reais
- Histórico de evolução da rubric com melhorias documentadas

**Armadilha comum:** Rubrics que se tornam obsoletas porque o domínio mudou. Uma rubric calibrada para produtos de janeiro pode não funcionar em junho se o catálogo, as preferências dos clientes ou as regulamentações mudaram.

#### Nível 4 — Expert

**Critérios:**
- Projeta sistemas de rubrics auto-calibráveis que ajustam weights e thresholds baseado em feedback contínuo de produção
- Cria um framework de criação de rubrics usado por múltiplos times
- Implementa métricas de saúde da rubric: "esta rubric está detectando problemas? Está gerando falsos positivos?"
- Mentora outros engenheiros em design de rubrics efetivas
- Conecta Evaluation Rubrics com Harness Evolution (C6): o harness usa múltiplas rubrics e evolui quais rubrics aplicar baseado no contexto

**Evidências aceitáveis:**
- Framework de rubrics com calibração automática
- Sistema de monitoramento de saúde de rubrics em produção
- Case study de evolução de rubric que resultou em melhoria significativa na qualidade



#### 📝 Exemplos Concretos por Nível

**Nível 1, Cenário 1:** Durante uma conversa de mentoria, você pergunta ao learner: "Por que válido não significa bom?". A resposta menciona o conceito certo, usa os termos principais e conecta com KODA, mas fica no plano explicativo. O learner ainda não propõe mudança em código, não escolhe parâmetros e não aponta onde a decisão entraria no fluxo.

**Nível 1, Cenário 2:** Você mostra um trace curto de avaliação de recomendações que passam validação técnica, mas podem ser ruins para o cliente. O learner reconhece o problema, nomeia o conceito C8 corretamente e explica por que ele importa. Quando você pergunta "qual arquivo você mudaria primeiro?", a resposta vira tentativa genérica ou pedido de exemplo pronto.

**Nível 1, Cenário 3:** Em uma sessão de grupo, o learner consegue comparar C8 com um conceito vizinho do currículo. A comparação é conceitualmente correta, mas ele ainda confunde sinais de diagnóstico com decisões de implementação quando o caso fica mais específico.

**Nível 2, Cenário 1:** Você entrega um exemplo funcional do time e pede para o learner adaptar o padrão para avaliação de recomendações que passam validação técnica, mas podem ser ruins para o cliente. Ele segue o template, altera os campos certos, roda a validação esperada e explica o fluxo com segurança. Se você remove o template, ele demora para decidir a estrutura inicial.

**Nível 2, Cenário 2:** Você pede para o learner criar uma rubric para avaliação de recomendações KODA do zero, fornecendo os critérios de negócio (adequação ao cliente, safety, custo-benefício). O learner define 4 dimensions com weights consistentes, escreve anchors para cada nível de score, estabelece um threshold de aprovação e consegue aplicar a rubric em 5 exemplos reais obtendo scores consistentes entre aplicações repetidas. A rubric funciona, mas segue de perto o formato ensinado no módulo.

**Nível 2, Cenário 3:** Em review, o learner sabe apontar qual critério da rubric foi atendido pelo PR. Ele também sabe dizer o que ainda não demonstrou para Nível 3, principalmente autonomia em domínio novo e justificativa de trade-offs.

**Nível 3, Cenário 1:** Você apresenta um problema novo e pergunta: "Como você projetaria evaluation rubrics para isso?". O learner estrutura a solução sem template, escolhe alternativas com base em risco, latência, custo e qualidade, e explica por que descartou outras opções.

**Nível 3, Cenário 2:** Você pede para calibrar weights usando histórico de devoluções, reclamações e satisfação. O learner desenha a arquitetura, identifica pontos de falha, define métricas de sucesso e propõe como provar que a mudança melhorou o sistema. A conversa inclui limites da abordagem, não só benefícios.

**Nível 3, Cenário 3:** Durante um incidente, o learner usa rubric versionada, amostras avaliadas, distribuição de scores e outcome real para reconstruir causa raiz. Ele não para no sintoma. Ele conecta o bug a uma decisão de design e propõe uma correção que reduz a chance de repetição.

**Nível 4, Cenário 1:** O learner cria sistema de saúde da rubric que detecta drift, falsos positivos e baixa correlação com outcomes. A proposta não é só uma melhoria local. Ela vira padrão, biblioteca, guia interno ou decisão de arquitetura que outras pessoas conseguem reaplicar.

**Nível 4, Cenário 2:** Em uma sessão de mentoria, o learner guia outra pessoa do diagnóstico até a decisão de implementação. Ele faz perguntas, testa hipóteses, mostra trade-offs e deixa a pessoa capaz de repetir o raciocínio sem depender dele.

**Nível 4, Cenário 3:** O learner revisa a forma como o time avalia C8. Ele identifica critério fraco, evidência enganosa ou métrica que envelheceu, propõe ajuste e acompanha se a nova avaliação prevê melhor o comportamento em produção.

#### 🔬 Como Coletar Evidências

**Para confirmar Nível 1:**
1. Peça uma explicação em voz alta com exemplo próprio de KODA.
2. Mostre um trace simples e peça para o learner nomear o problema.
3. Faça uma pergunta de contraste com outro conceito do currículo.
4. Registre se a resposta usa termos corretos sem depender de frases decoradas.

**Para confirmar Nível 2:**
1. Entregue um template funcional e peça uma adaptação pequena, mas realista.
2. Inclua um bug controlado ligado a evaluation rubrics e observe o caminho de debug.
3. Peça que o learner explique cada mudança feita no PR.
4. Colete o diff, o teste ou a demonstração que prova o novo comportamento.

**Para confirmar Nível 3:**
1. Use um problema que não aparece nos exemplos do currículo.
2. Peça duas alternativas e uma justificativa explícita de escolha.
3. Exija métrica de sucesso, como correlação entre score da rubric e satisfação, devolução ou incidente real.
4. Revise se a solução trata falhas prováveis, não apenas o happy path.

**Para confirmar Nível 4:**
1. Procure evidência de influência fora do próprio PR do learner.
2. Verifique se outra pessoa ou outro time adotou o padrão proposto.
3. Peça um relato de mentoria com antes, depois e evidência do mentorado.
4. Compare a proposta com dados de produção para ver se ela melhorou a prática do time.

#### 📈 Progressão Típica

A progressão em C8 costuma começar com vocabulário e reconhecimento de sintomas. Depois, o learner ganha confiança adaptando exemplos existentes e corrigindo bugs pequenos. O salto para Avançado acontece quando ele deixa de perguntar "qual template uso?" e passa a perguntar "qual decisão o domínio exige?". O salto para Expert aparece quando a melhoria deixa de ser pessoal e passa a mudar o modo como o time ensina, implementa e mede evaluation rubrics.

---

## ✅ Checklist de Auto-Avaliação

Use esta checklist para se posicionar em cada conceito. Para cada afirmação, marque se é **verdadeira para você hoje**. Seja honesto — esta é uma ferramenta de crescimento, não de julgamento.

### Como usar

1. Para cada conceito, leia as afirmações do Nível 1 ao 4
2. Marque `[x]` nas afirmações que são **consistentemente verdadeiras** sobre sua capacidade atual
3. Esta checklist é uma **ferramenta de triagem inicial** — o nível sugerido é uma estimativa. A determinação definitiva requer validação com mentor usando os critérios detalhados na seção "Critérios por Conceito" e as perguntas-gatilho do "Guia para Mentores"
4. Como triagem: considere seu nível provisório como o mais alto onde você marcou **todas** as afirmações. Se houver dúvida entre dois níveis, assuma o mais baixo até validar com evidências externas
5. Afirmações parcialmente verdadeiras contam como não marcadas — o critério é consistência

### Context Management (C1)

- [ ] **N1:** Consigo explicar o que é context window e por que ela tem limites
- [ ] **N1:** Sei listar pelo menos 3 estratégias de context management
- [ ] **N1:** Consigo identificar context amnesia em uma conversa real
- [ ] **N2:** Já implementei sliding window ou summarization seguindo um template
- [ ] **N2:** Consigo debuggar por que um agente "esqueceu" uma informação
- [ ] **N2:** Sei quando promover informação de "conversa" para "estado persistente"
- [ ] **N3:** Já projetei um pipeline de contexto com múltiplas camadas do zero
- [ ] **N3:** Consigo medir e otimizar eficiência de contexto (ex: reduzi tokens em X%)
- [ ] **N3:** Sei escolher entre estratégias baseado em requisitos, não em familiaridade
- [ ] **N4:** Já criei ou evolui uma ferramenta de context management usada por outros
- [ ] **N4:** Já mentorei alguém que passou a implementar context management corretamente
- [ ] **N4:** Publiquei aprendizados ou padrões sobre contexto que influenciaram o time

**Meu nível atual em C1:** [___]

**Perguntas de Reflexão:**
1. Qual foi a última informação crítica que você viu sair da context window sem virar estado?
1. Quando você escolheria summarization em vez de retrieval, e por quê?
1. Que métrica provaria que seu context management melhorou sem esconder perda de qualidade?
1. Que parte do seu pipeline atual depende de memória implícita demais?

---

### Planning vs Execution Separation (C2)

- [ ] **N1:** Consigo explicar a diferença entre planejar e executar em agentes
- [ ] **N1:** Sei descrever Planning Collapse com exemplos próprios
- [ ] **N1:** Identifico quando um agente está sofrendo de Planning Collapse
- [ ] **N2:** Já implementei um fluxo Planner → Executor com checkpoints
- [ ] **N2:** Consigo escrever um plano estruturado (JSON com passos e dependências)
- [ ] **N2:** Sei reportar exatamente qual passo falhou e por quê
- [ ] **N3:** Já projetei um sistema com replanejamento dinâmico
- [ ] **N3:** Uso Sprint Contracts como ponte entre Planner e Executor
- [ ] **N3:** Consigo comparar Planejamento/Execução com Chain-of-Thought e ReAct
- [ ] **N4:** Criei padrões de planning reutilizáveis adotados pelo time
- [ ] **N4:** Já mentorei alguém em separação de planejamento e execução
- [ ] **N4:** Conectei Planning/Execution com Harness Evolution em produção

**Meu nível atual em C2:** [___]

**Perguntas de Reflexão:**
1. Em qual fluxo recente o agente tentou planejar e executar ao mesmo tempo?
1. Que checkpoint teria evitado a falha mais cedo?
1. Quando replanejar é melhor do que abortar?
1. Que decisão deve ficar no Planner e qual deve ficar no Executor?

---

### Generator/Evaluator Pattern (C3)

- [ ] **N1:** Consigo definir o padrão G/E e explicar o problema de sycophancy
- [ ] **N1:** Sei descrever o fluxo: Generator → Evaluator → aprova/rejeita → feedback
- [ ] **N1:** Identifico self-evaluation collapse em exemplos reais
- [ ] **N2:** Já implementei um par G/E usando arquivos JSON como comunicação
- [ ] **N2:** Escrevi uma rubrica simples para o Evaluator aplicar
- [ ] **N2:** Implementei loop de feedback com retry
- [ ] **N3:** Já projetei G/E com múltiplos Evaluators especializados
- [ ] **N3:** Calibrei thresholds dinamicamente baseado no tipo de tarefa
- [ ] **N3:** Meço impacto do G/E com métricas (precisão, recall, falsos positivos)
- [ ] **N4:** Criei padrões de G/E reutilizáveis adotados por outros times
- [ ] **N4:** Implementei G/E adaptativo que aprende com erros
- [ ] **N4:** Já mentorei alguém que passou a implementar G/E corretamente

**Meu nível atual em C3:** [___]

**Perguntas de Reflexão:**
1. O Evaluator que você criou sabe algo que o Generator não sabe?
1. Seu feedback ajuda o Generator a melhorar ou só reprova?
1. Que falso positivo do Evaluator seria perigoso em KODA?
1. Quando múltiplos Evaluators pagam o custo extra?

---

### Sprint Contracts (C4)

- [ ] **N1:** Consigo definir input contract, output contract, guarantees e validation
- [ ] **N1:** Sei explicar por que contratos previnem falhas silenciosas
- [ ] **N1:** Diferencio contrato (validado em runtime) de documentação (não validada)
- [ ] **N2:** Já escrevi contratos usando JSON Schema ou Pydantic
- [ ] **N2:** Implementei validação de contrato na entrada e saída de um módulo
- [ ] **N2:** Consigo derivar input contract de módulo downstream do output contract upstream
- [ ] **N3:** Projetei hierarquia de contratos para pipeline multi-módulo
- [ ] **N3:** Implementei versionamento de contratos para backward compatibility
- [ ] **N3:** Meço impacto de contratos (redução de bugs, tempo de debug)
- [ ] **N4:** Criei padrões de contrato reutilizáveis com conhecimento de domínio
- [ ] **N4:** Implementei monitoramento de violações de contrato em produção
- [ ] **N4:** Já mentorei alguém em design de contratos efetivos

**Meu nível atual em C4:** [___]

**Perguntas de Reflexão:**
1. Seu contrato valida semântica ou apenas formato?
1. Que mudança de schema quebraria consumidores hoje?
1. Qual garantia do domínio deveria virar validação em runtime?
1. Como você saberia que um contrato está rígido demais?

---

### State Persistence (C5)

- [ ] **N1:** Consigo definir state persistence e diferenciar de context window
- [ ] **N1:** Sei explicar por que "guardar tudo na conversa" não é suficiente
- [ ] **N1:** Identifico que tipos de dados devem ser persistidos
- [ ] **N2:** Já implementei leitura/escrita de estado com arquivos JSON
- [ ] **N2:** Projetei um schema de estado simples com campos relevantes
- [ ] **N2:** Conectei state persistence com context management na prática
- [ ] **N3:** Projetei arquitetura de estado em múltiplas camadas (hot/warm/cold)
- [ ] **N3:** Implementei estratégias de invalidação e conflito de estado
- [ ] **N3:** Meço efetividade da persistência (latência, cache hit, consistência)
- [ ] **N4:** Projetei sistema de estado distribuído com garantias de consistência
- [ ] **N4:** Implementei migração de schema sem downtime
- [ ] **N4:** Já mentorei alguém em design de persistência para agentes

**Meu nível atual em C5:** [___]

**Perguntas de Reflexão:**
1. Que dado do cliente precisa sobreviver a reinício do agente?
1. Qual campo do estado pode expirar e qual não pode?
1. Como você resolveria duas escritas concorrentes no mesmo perfil?
1. Que migração de schema exigiria plano antes do merge?

---

### Harness Evolution (C6)

- [ ] **N1:** Consigo definir o que é um harness e seus componentes
- [ ] **N1:** Sei diferenciar "código do agente" de "código ao redor do agente"
- [ ] **N1:** Identifico o que acontece quando um harness está ausente
- [ ] **N2:** Já modifiquei um harness existente para adicionar validação
- [ ] **N2:** Ajustei thresholds e limites do harness com justificativa
- [ ] **N2:** Monitorei saúde do harness (taxas de aprovação/rejeição)
- [ ] **N3:** Projetei estratégia de evolução de harness com critérios de decisão
- [ ] **N3:** Implementei A/B testing de harness
- [ ] **N3:** Conectei Harness Evolution com Trace Reading para identificar gaps
- [ ] **N4:** Projetei harness que se auto-calibra baseado em feedback de produção
- [ ] **N4:** Criei framework de harness evolution usado por múltiplos times
- [ ] **N4:** Implementei detecção automática de harness drift

**Meu nível atual em C6:** [___]

**Perguntas de Reflexão:**
1. Que validação do harness atual talvez esteja obsoleta?
1. Qual incidente recente poderia ter sido capturado antes?
1. Como você distingue falso positivo útil de ruído?
1. Que sinal indicaria harness drift?

---

### Multi-Agent Coordination (C7)

- [ ] **N1:** Consigo definir multi-agent coordination e seus benefícios
- [ ] **N1:** Sei listar topologias (pipeline, star, mesh) e canais (arquivos, mensagens)
- [ ] **N1:** Entendo riscos: race conditions, deadlocks, agentes fantasmas
- [ ] **N2:** Já implementei coordenação entre 2+ agentes via arquivos
- [ ] **N2:** Implementei orquestrador básico com coleta de resultados
- [ ] **N2:** Lidei com falha de um agente no pipeline
- [ ] **N3:** Projetei topologia de coordenação com justificativa de escolha
- [ ] **N3:** Implementei paralelismo onde agentes independentes rodam juntos
- [ ] **N3:** Projetei estratégia de failure handling (retry, fallback, circuit breaker)
- [ ] **N4:** Projetei sistema onde topologia se adapta dinamicamente à carga
- [ ] **N4:** Criei padrões de coordenação reutilizáveis
- [ ] **N4:** Implementei coordenação com garantias de consistência (exactly-once)

**Meu nível atual em C7:** [___]

**Perguntas de Reflexão:**
1. Quais agentes realmente precisam rodar em sequência?
1. Onde existe risco de race condition no fluxo atual?
1. Que estado compartilhado precisa de versionamento?
1. Qual parte da coordenação você mediria primeiro?

---

### Evaluation Rubrics (C8)

- [ ] **N1:** Consigo definir rubric e diferenciar de validação binária
- [ ] **N1:** Sei listar componentes: dimensions, weights, levels, thresholds, anchors
- [ ] **N1:** Entendo que qualidade é um espectro, não binário
- [ ] **N2:** Já criei uma rubric com 3-5 dimensions, weights e anchors
- [ ] **N2:** Apliquei a rubric e obtive scores consistentes
- [ ] **N2:** Usei a rubric como parte de um Evaluator no padrão G/E
- [ ] **N3:** Calibrei weights de rubric baseado em dados históricos
- [ ] **N3:** Criei rubrics adaptativas com thresholds por contexto
- [ ] **N3:** Meço correlação entre scores da rubric e outcomes reais
- [ ] **N4:** Projetei sistema de rubrics auto-calibráveis
- [ ] **N4:** Criei framework de criação de rubrics usado por múltiplos times
- [ ] **N4:** Implementei métricas de saúde da rubric em produção

**Meu nível atual em C8:** [___]

**Perguntas de Reflexão:**
1. Que dimensão da sua rubric tem weight baseado em evidência, não opinião?
1. Qual output válido, mas ruim, sua rubric precisa detectar?
1. Como você testaria consistência entre avaliadores?
1. Que outcome real deveria correlacionar com o score?

---

### Matriz Resumo de Auto-Avaliação

| Conceito | Nível Atual | Nível Alvo | Gap? | Ação Prioritária |
|----------|------------|------------|------|-----------------|
| C1: Context Management | [___] | [___] | | |
| C2: Planning vs Execution | [___] | [___] | | |
| C3: Generator/Evaluator | [___] | [___] | | |
| C4: Sprint Contracts | [___] | [___] | | |
| C5: State Persistence | [___] | [___] | | |
| C6: Harness Evolution | [___] | [___] | | |
| C7: Multi-Agent Coordination | [___] | [___] | | |
| C8: Evaluation Rubrics | [___] | [___] | | |

**Preencha o "Nível Alvo" baseado em:**
- Seu cargo atual (ex: engenheiro júnior → alvo Intermediário na maioria; sênior → alvo Avançado)
- Relevância do conceito para seu trabalho diário (ex: se você trabalha com infraestrutura, C5 e C7 são prioridade)
- Plano de carreira (ex: quer ser arquiteto → precisa Avançado em todos)

---

## 👥 Guia para Mentores

Esta seção é para quem vai aplicar a rubric avaliando outras pessoas — mentores, tech leads, engenheiros seniores. Avaliar profundidade de compreensão requer mais do que ler a checklist; requer saber **como perguntar**, **o que observar** e **como coletar evidências**.

### Princípios da Mentoria com Rubric

**1. A rubric é um ponto de partida, não uma sentença.**
O objetivo não é "aprovar" ou "reprovar". É identificar com precisão onde a pessoa está e qual o próximo passo. Um diagnóstico de "Nível 2 em C3" não é um veredito — é um mapa.

**2. Evidência supera auto-avaliação.**
A auto-avaliação do learner é um input valioso, mas tende ao viés (para cima ou para baixo). Sempre colete evidências independentes: código, explicações, decisões de design, debug sessions.

**3. Uma conversa revela mais que um formulário.**
A diferença entre Nível 1 (sabe definir) e Nível 2 (sabe aplicar) frequentemente só aparece quando você pede: "Me mostra como você faria isso no código." Faça perguntas de follow-up.

**4. Progresso não é linear.**
Alguém pode estar em Nível 3 em Context Management (porque usa todo dia) e Nível 1 em Harness Evolution (porque nunca precisou). Isso é normal. A rubric não espera uniformidade.

**5. O nível certo depende do contexto.**
Nem todo mundo precisa ser Expert em tudo. Um engenheiro de produto focado em features pode mirar Nível 3 nos conceitos que usa diariamente e Nível 2 nos demais. Um arquiteto precisa de Nível 3-4 em todos.

---

### Perguntas-Gatilho por Nível

Use estas perguntas para provocar evidências de compreensão. Adapte ao conceito específico.

#### Para verificar Nível 1 (Básico)

- "Me explica [conceito] como se eu fosse um engenheiro novo no time."
- "Qual problema [conceito] resolve? O que acontece se você não usar?"
- "Me dá um exemplo do KODA onde [conceito] faria diferença."
- "Qual é a diferença entre [conceito] e [conceito relacionado]?"

**Sinais de Nível 1 sólido:** Respostas corretas, usa terminologia adequada, consegue dar exemplos (mesmo que sejam os do currículo). Não espera profundidade — espera clareza.

**Sinais de alerta:** Respostas vagas ("é tipo uma forma de melhorar as coisas"), confusão entre conceitos relacionados, não consegue dar exemplo concreto.

#### Para verificar Nível 2 (Intermediário)

- "Aqui está um código/base. Me mostra onde você aplicaria [conceito]."
- "Esse módulo está com [problema]. Como você debuga usando [conceito]?"
- "Se eu pedisse para você modificar esse [componente] para adicionar [requisito], o que mudaria?"
- "Me explica o que esse código está fazendo, passo a passo."

**Sinais de Nível 2 sólido:** Consegue navegar código existente, identifica o padrão, faz modificações corretas, explica o fluxo. Pode precisar consultar documentação ou exemplos — isso é esperado.

**Sinais de alerta:** Não sabe por onde começar sem instruções muito específicas, faz modificações que quebram o padrão, não consegue explicar o fluxo de execução.

#### Para verificar Nível 3 (Avançado)

- "Você nunca viu esse problema antes. Como decidiria se [conceito] se aplica? O que consideraria?"
- "Quais são os trade-offs de usar [abordagem A] vs [abordagem B] para esse caso?"
- "Esse sistema está com [problema sutil]. O que você investigaria primeiro?"
- "Se eu pedisse para você desenhar [sistema] do zero usando [conceito], qual seria sua arquitetura?"
- "Como você mediria se sua implementação de [conceito] está funcionando bem?"

**Sinais de Nível 3 sólido:** Considera múltiplas abordagens, justifica escolhas com critérios (não preferência), antecipa problemas de borda, menciona métricas. Consegue desenhar arquitetura no quadro branco.

**Sinais de alerta:** Escolhe abordagem por familiaridade, não consegue articular trade-offs, não pensa em cenários de falha, foca em "funciona" em vez de "funciona bem".

#### Para verificar Nível 4 (Expert)

- "O que você mudaria em [conceito] se pudesse redesigná-lo para o KODA de 2027?"
- "Me conta de uma vez que [conceito] falhou em produção e o que você aprendeu."
- "Como você ensinaria [conceito] para alguém que está chegando agora no time?"
- "Que padrões ou ferramentas você criou que outros no time usam para [conceito]?"

**Sinais de Nível 4 sólido:** Tem opiniões fundamentadas sobre limitações do conceito, já contribuiu para evolução do padrão, consegue ensinar com metodologia (não apenas "mostrar como faz"), tem exemplos de produção.

**Sinais de alerta:** Respostas puramente teóricas sem experiência de produção, não consegue citar exemplos de melhoria que fez, ensino é "mostrar código" sem explicar princípios.

---

### Coleta de Evidências

Para cada conceito e nível, colete evidências de múltiplas fontes. Uma única evidência forte pode ser suficiente; múltiplas evidências fracas não somam para uma forte.

#### Tipos de Evidência (em ordem de força)

1. **Código em produção** — Implementação real, usada por clientes, com métricas de sucesso. Evidência mais forte.
2. **Pull Request com review** — Código que passou por revisão e foi aprovado por pares.
3. **Design document** — Documento de arquitetura ou decisão técnica com justificativa.
4. **Debug session** — Sessão onde a pessoa diagnosticou e resolveu um problema relacionado ao conceito.
5. **Explicação oral com follow-up** — Conversa onde a pessoa explica e responde perguntas de profundidade.
6. **Exercício prático** — Tarefa designada para demonstrar o conceito.
7. **Auto-avaliação** — Input do learner sobre seu próprio nível. Evidência mais fraca (viés), mas contextualiza as demais.

#### Matriz de Evidências por Nível

| Nível | Evidência Mínima Necessária | Evidência Ideal |
|-------|---------------------------|-----------------|
| Básico | Explicação oral correta + 1 exemplo | Explicação + identificação em código real |
| Intermediário | 1 PR com implementação seguindo padrão | PR + debug session + explicação do fluxo |
| Avançado | Design doc + implementação original + métricas | Design doc + código em produção + A/B test |
| Expert | Framework/ferramenta criada + mentoria comprovada + case study | Framework + múltiplos mentorados + publicação interna |

---

### Metodologia de Scoring

Quando você precisa tomar uma decisão formal (ex: "Fulano está pronto para o Nível 3?"), use esta metodologia:

**Passo 1: Colete evidências para o nível alvo.**
Para cada conceito relevante, colete pelo menos 2 evidências do tipo apropriado para o nível sendo avaliado (ver matriz acima).

**Passo 2: Avalie cada conceito independentemente.**
Não faça média entre conceitos. Alguém pode ser Nível 4 em C1 e Nível 1 em C6 — isso não "faz média" para Nível 2.5. Cada conceito é avaliado separadamente.

**Passo 3: Aplique a regra de consistência.**
O nível em um conceito é o nível mais alto onde a pessoa demonstra **consistentemente** os comportamentos descritos. "Uma vez eu fiz algo de Nível 3" não faz a pessoa ser Nível 3 — precisa ser reproduzível.

**Passo 4: Identifique gaps e recomende ações.**
Para cada conceito abaixo do nível alvo, identifique o gap específico e recomende:
- Que módulo do currículo revisitar
- Que tipo de prática fazer (exercício, implementação, mentoria)
- Que evidência coletar na próxima avaliação

**Passo 5: Documente a decisão.**
Registre: data, conceitos avaliados, nível determinado para cada um, evidências coletadas, gaps identificados e recomendações. Isso cria uma trilha de crescimento ao longo do tempo.

---

### Exemplo de Aplicação da Mentoria

**Cenário:** Mentora Ana avaliando o engenheiro Carlos no conceito C3 (Generator/Evaluator). Carlos se auto-avaliou como Nível 3.

**Evidências coletadas por Ana:**
1. Carlos explicou G/E corretamente, incluindo sycophancy e fluxo de feedback (N1 ✅)
2. Carlos mostrou um PR onde implementou G/E para recomendação de produtos seguindo o template do time (N2 ✅)
3. Ana perguntou: "Se eu pedisse para você implementar G/E para um domínio novo, como validação de reviews, como faria?" Carlos hesitou, disse que precisaria consultar o template de produto e adaptar. (N3 ❓ — depende de template)
4. Ana perguntou: "Quando você usaria 1 Evaluator vs 3 Evaluators especializados?" Carlos respondeu: "Depende da criticidade — para pagamento usaria 3, para recomendação 1 basta. Mas confesso que nunca implementei com múltiplos evaluators." (N3 ⚠️ — conhece a teoria mas não implementou)

**Diagnóstico de Ana:** Carlos está sólido em N2. Tem conhecimento teórico de N3 mas não demonstrou aplicação autônoma. A dependência de template e a falta de experiência com evaluators múltiplos sugerem que N3 ainda não está consolidado.

**Recomendação:** Nível atual: **Intermediário (N2)**. Para alcançar N3: implementar G/E para um domínio novo sem consultar templates existentes, e experimentar com múltiplos evaluators em um projeto real.

### Cenários Detalhados de Aplicação da Rubric

#### Cenário A: Learner superestima o próprio nível

**Contexto:** Júlia é engenheira plena e se auto-avalia como Nível 4 em Generator/Evaluator. Ela liderou um PR recente que adicionou um Evaluator a um fluxo de recomendação e sente que domina o padrão.

**Como o mentor conduz:** O mentor começa validando a experiência real. Ele não corrige a auto-avaliação de imediato. Em vez disso, pede evidências alinhadas ao Nível 4: padrões reutilizáveis, mentoria, evolução do padrão, impacto em outros times e melhoria estrutural.

**Perguntas usadas:**
1. "Quem além de você usa esse padrão hoje?"
2. "Que parte do G/E você mudou em relação ao template original?"
3. "Você já mentoreou alguém até a pessoa implementar G/E sem sua ajuda?"
4. "Que métrica mostra que sua abordagem é melhor que a anterior?"

**Evidências encontradas:** Júlia tem um PR bom, com Evaluator funcional e feedback loop. Ela ajustou threshold, escreveu testes e explicou sycophancy com clareza. Mas o padrão ainda é local ao feature, não foi adotado por outros, não há mentoria comprovada e a métrica de melhoria cobre só aquele fluxo.

**Diagnóstico:** Nível 3 em C3, não Nível 4. Ela aplica de forma autônoma, faz trade-offs e mede impacto. Ainda não demonstrou evolução do padrão nem influência sustentada no time.

**Feedback recomendado:** "Sua auto-avaliação capturou uma competência real. Você não está em N2, está claramente em N3. O que falta para N4 não é mais um PR. É transformar o que você aprendeu em padrão reutilizável, orientar outra pessoa e provar adoção fora do seu feature."

**Próxima evidência sugerida:** Júlia deve extrair o G/E para um template interno, aplicar em outro domínio com outro engenheiro e registrar antes/depois de precisão, tempo de debug e taxa de rejeição útil.

#### Cenário B: Learner subestima o próprio nível por impostor syndrome

**Contexto:** Pedro é júnior e marca Nível 1 em Planning vs Execution. Ele diz: "eu só segui o que o time já fazia". O mentor viu, porém, que Pedro resolveu um bug em um fluxo de pedido que misturava validação de cupom, estoque e pagamento.

**Como o mentor conduz:** O mentor não tenta convencer Pedro com elogios genéricos. Ele reconstrói a evidência passo a passo e pergunta o que Pedro fez em cada momento. O objetivo é separar humildade saudável de subestimação imprecisa.

**Perguntas usadas:**
1. "Qual era o plano original do agente?"
2. "Onde a execução saiu do plano?"
3. "Que checkpoint você adicionou?"
4. "O que teria acontecido se o Executor continuasse depois da falha?"

**Evidências encontradas:** Pedro identificou Planning Collapse em trace real, separou passos estruturais de ações atômicas, adicionou checkpoint antes do pagamento e impediu continuação após falha de estoque. Ele não desenhou um sistema novo, mas aplicou o padrão com ajuda limitada.

**Diagnóstico:** Nível 2 em C2. A auto-avaliação N1 estava baixa demais porque Pedro associou competência apenas a criar arquitetura do zero. A rubric mostra que adaptar um padrão e corrigir bug real já conta para Intermediário.

**Feedback recomendado:** "Você não precisa se declarar Avançado. Mas também não precisa apagar evidência. Neste conceito, você já demonstrou aplicação guiada. Seu próximo passo é pegar um caso novo e desenhar o plano antes de ver o template."

**Próxima evidência sugerida:** Pedro deve receber um fluxo novo, criar plano JSON com dependências e checkpoints, executar em pair com mentor e registrar onde precisou de ajuda.

#### Cenário C: Learner está entre níveis e a decisão não é óbvia

**Contexto:** Renata se avalia como Nível 3 em Sprint Contracts. Ela escreveu contratos com JSON Schema, adicionou testes e já fez versionamento simples. Em entrevista, demonstra boa noção de garantias semânticas, mas ainda consulta exemplos para estruturar pipelines maiores.

**Como o mentor conduz:** O mentor trata a avaliação como decisão de evidência, não como debate. Ele pergunta quais comportamentos de N3 aparecem consistentemente e quais aparecem só em teoria ou em casos pequenos.

**Perguntas usadas:**
1. "Mostre um contrato onde você validou uma garantia semântica, não só estrutura."
2. "Como você versionaria esse contrato se o módulo downstream estivesse uma versão atrás?"
3. "Qual métrica melhorou depois dos contratos?"
4. "Você consegue desenhar a hierarquia de contratos para quatro módulos sem consultar o exemplo?"

**Evidências encontradas:** Renata demonstra N2 completo e parte de N3. Ela tem um contrato com garantia semântica simples e já lidou com backward compatibility. Ainda não tem design de pipeline com múltiplos módulos, nem métrica clara de impacto, nem autonomia consistente fora dos exemplos.

**Diagnóstico:** Nível 2 forte, em transição para N3. A regra de consistência evita promover cedo demais, mas o mentor registra os comportamentos de N3 já observados para orientar a próxima prática.

**Feedback recomendado:** "Você está mais perto de N3 do que de N2 inicial. A decisão de hoje fica em N2 porque N3 precisa aparecer de forma repetível em contexto novo. Vamos escolher uma tarefa que gere exatamente essa evidência."

**Próxima evidência sugerida:** Renata deve desenhar contratos para um pipeline de quatro módulos, incluir versionamento, validar pelo menos uma garantia semântica por módulo e medir se o tempo de debug caiu em incidentes simulados.

### Como Decidir Quando a Pessoa Está Entre Níveis

1. Use o nível mais alto onde há consistência, não o pico isolado.
2. Registre comportamentos parciais do próximo nível para não apagar progresso.
3. Prefira "N2 forte, em transição para N3" a uma promoção frágil.
4. Defina uma evidência próxima que resolva a ambiguidade.
5. Reavalie em prazo curto quando a pessoa está claramente na fronteira.
6. Explique a decisão com exemplos concretos, não com impressão pessoal.
7. Separe confiança da pessoa de competência demonstrada.
8. Separe humildade da pessoa de falta real de evidência.

---

## 🚀 Aplicação KODA: Como Usar Esta Rubric na Prática

Esta seção conecta a rubric com o contexto real da equipe KODA — como integrá-la ao fluxo de desenvolvimento, mentoria e crescimento.

### Integração com o Programa de 12 Semanas

| Semana | Marco do Programa | Como usar a Rubric |
|--------|------------------|-------------------|
| Semana 1 | Início do Nível 1 | Auto-avaliação inicial em todos os 8 conceitos (baseline) |
| Semana 2 | Fim do Nível 1 | Reavaliar C1 (Context Management) — esperado N1→N2 |
| Semana 4 | Fim do Nível 2 | Reavaliar C2, C3, C4, C8 — esperado N1→N2 ou N2→N3 |
| Semana 6 | Fim do Nível 3 | Reavaliar C5, C6, C7 — esperado progresso para N2/N3 |
| Semana 8 | Meio do Nível 4 | Peer review usando a rubric nos conceitos aplicados em features KODA |
| Semana 12 | Conclusão | Avaliação formal completa com mentor para todos os 8 conceitos |

---

### Papéis e Responsabilidades

**Learner (quem está aprendendo):**
- Fazer auto-avaliação honesta no início de cada nível
- Coletar evidências do próprio progresso (PRs, docs, métricas)
- Identificar gaps e pedir ajuda direcionada ("preciso melhorar em C4, especialmente versionamento de contratos")
- Não esperar a avaliação formal para agir nos gaps

**Mentor (quem avalia e orienta):**
- Aplicar a rubric em avaliações formais (a cada 4-6 semanas)
- Usar perguntas-gatilho para verificar profundidade real
- Coletar evidências independentes (código, design docs, observação)
- Dar feedback específico: "você está em N2 em C3 porque X, para chegar a N3 precisa demonstrar Y"
- Manter registro de progresso para cada mentorado

**Tech Lead / Gestor:**
- Definir níveis-alvo por cargo (ver tabela abaixo)
- Garantir que o tempo de mentoria está alocado
- Usar dados agregados da rubric para identificar gaps na equipe (ex: "80% do time está abaixo de N2 em C7 — precisamos de workshop de Multi-Agent Coordination")
- Não usar a rubric para avaliação de desempenho puro — é ferramenta de desenvolvimento, não de punição

---

### Níveis-Alvo Sugeridos por Cargo

| Cargo | C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 |
|-------|----|----|----|----|----|----|----|----|
| **Estagiário / Jr** (0-2 anos) | N2 | N1 | N1 | N1 | N1 | N1 | N1 | N1 |
| **Pleno** (2-5 anos) | N3 | N2 | N2 | N2 | N2 | N1 | N1 | N2 |
| **Sênior** (5-8 anos) | N3 | N3 | N3 | N3 | N3 | N2 | N2 | N3 |
| **Staff / Tech Lead** | N4 | N3 | N3 | N3 | N3 | N3 | N3 | N3 |
| **Arquiteto / Principal** | N4 | N4 | N4 | N4 | N4 | N4 | N4 | N4 |

Estes são guias, não regras rígidas. Um engenheiro pleno que trabalha intensivamente com multi-agent systems pode mirar N3 em C7 antes do esperado. Um sênior focado em produto pode ficar em N2 em C6 indefinidamente se não for relevante para seu trabalho.

---

### Exemplo de Ciclo de Avaliação KODA

**Semana 1 — Auto-avaliação inicial:**
```
Carlos (Pleno, 3 anos):
C1: N2 | C2: N1 | C3: N1 | C4: N1 | C5: N2 | C6: N1 | C7: N1 | C8: N1

Diagnóstico: Sólido em Context Management e State Persistence (já trabalhava com isso).
Gaps grandes nos padrões de Nível 2 (C2, C3, C4, C8).
```

**Semana 4 — Reavaliação após Nível 2:**
```
Carlos:
C1: N3 ⬆ | C2: N2 ⬆ | C3: N2 ⬆ | C4: N2 ⬆ | C5: N2 | C6: N1 | C7: N1 | C8: N2 ⬆

Diagnóstico: Excelente progresso! C1 atingiu N3 (nível alvo para pleno). C2-C4-C8 no N2 conforme esperado.
Próximo foco: solidificar N2 nos padrões e começar N3 em C3 e C8.
```

**Semana 8 — Peer Review:**
```
Carlos:
C3: N3 ⬆ (implementou G/E para feature nova de revisão de pedidos, com múltiplos evaluators)
C8: N2 (rubrics ainda seguem template, não calibradas com dados)
C5: N3 ⬆ (projetou migração de schema de customer_context)

Diagnóstico: C3 atingiu N3 antes do esperado — Carlos está acelerando.
C8 ainda em N2 — recomendação: liderar calibração de uma rubric com dados históricos.
```

### Métricas de Adoção

A rubric só cumpre seu papel se mudar comportamento. Não basta existir no repositório, ser citada em onboarding ou aparecer em uma apresentação. A equipe precisa usar a rubric para tomar decisões de estudo, mentoria, PR review e evolução do currículo.

#### Métricas de Uso

1. **Taxa de auto-avaliação inicial:** Percentual de learners que preencheram os 8 conceitos na primeira semana do programa.
2. **Taxa de reavaliação:** Percentual de learners que atualizaram a checklist após cada marco do currículo.
3. **Cobertura por conceito:** Quantos conceitos têm evidência registrada por learner, não apenas nível declarado.
4. **Frequência de mentoria com rubric:** Quantas sessões 1:1 usam perguntas-gatilho e registram diagnóstico por conceito.
5. **PRs vinculados a evidência:** Quantos PRs de currículo ou KODA são citados como prova de N2, N3 ou N4.
6. **Tempo até feedback:** Tempo entre entrega de evidência e retorno do mentor.
7. **Reavaliações com mudança de nível:** Percentual de avaliações que resultam em avanço, ajuste para baixo ou confirmação com nova evidência.

#### Métricas de Qualidade da Avaliação

1. **Concordância mentor versus peer:** Dois avaliadores chegam ao mesmo nível usando as mesmas evidências?
2. **Taxa de diagnósticos revertidos:** Quantas decisões de nível precisaram ser corrigidas depois por falta de evidência?
3. **Precisão das recomendações:** As ações sugeridas pelo mentor geram a evidência esperada na avaliação seguinte?
4. **Clareza dos gaps:** Learners conseguem explicar qual comportamento falta para o próximo nível?
5. **Distribuição saudável de níveis:** A equipe tem variação coerente por cargo e área, sem todo mundo marcado artificialmente no mesmo nível.
6. **Evidência por decisão:** Cada nível registrado tem pelo menos uma evidência forte ou duas evidências complementares?
7. **Uso de casos reais:** Avaliações usam traces, PRs e design docs reais em vez de conversas puramente teóricas?

#### Métricas de Impacto no Aprendizado

1. **Tempo de progressão por conceito:** Quantas semanas, em média, a pessoa leva para sair de N1 para N2 e de N2 para N3.
2. **Gaps sistêmicos detectados:** Conceitos onde mais de 40% do time fica abaixo do nível alvo.
3. **Workshops disparados por dados:** Quantos treinamentos foram criados por evidência agregada da rubric.
4. **Melhoria pós-workshop:** Diferença de nível ou evidência antes e depois de uma intervenção.
5. **Retenção de competência:** A pessoa mantém o nível em nova avaliação três meses depois?
6. **Transferência para produção:** Competências avaliadas aparecem em PRs reais de KODA?
7. **Redução de incidentes relacionados:** Gaps trabalhados pela rubric reduzem bugs de contexto, contratos, harness ou coordenação?

#### Sinais de Que a Rubric Está Sendo Usada Bem

1. Learners chegam ao 1:1 dizendo "preciso de evidência para C4 N3", não apenas "quero melhorar".
2. Mentores discordam de auto-avaliações com respeito e base em evidência.
3. PR reviews citam critérios específicos da rubric quando avaliam qualidade de implementação.
4. Tech leads conseguem planejar workshops com base em gaps agregados.
5. A equipe aceita que níveis mudem quando novas evidências aparecem.
6. Critérios da rubric são ajustados quando deixam de prever desempenho real.
7. Pessoas usam a rubric para pedir ajuda antes de falhar em produção.

#### Sinais de Adoção Superficial

1. Todo mundo marca níveis altos sem anexar evidências.
2. Mentores copiam a auto-avaliação sem entrevista ou análise de código.
3. A rubric aparece só no início do programa e desaparece nas semanas seguintes.
4. Ninguém registra decisões difíceis entre níveis.
5. Os mesmos gaps aparecem trimestre após trimestre sem ação.
6. A equipe usa a rubric como ranking, não como mapa de crescimento.
7. Critérios antigos continuam valendo mesmo depois de mudanças no KODA ou nos modelos.

#### Ritmo Recomendado de Medição

1. **Semanal:** Verificar se novas evidências foram registradas e se feedback está dentro do prazo.
2. **Mensal:** Agregar gaps por conceito, cargo e squad.
3. **Trimestral:** Recalibrar níveis-alvo, critérios ambíguos e exemplos de evidência.
4. **Após incidentes relevantes:** Mapear se o incidente revela gap de conceito, gap de rubric ou gap de aplicação.
5. **Após mudança grande de modelo ou arquitetura:** Revisar se os critérios continuam representando a prática real.

#### Exemplo de Dashboard Simples

| Métrica | Meta Saudável | Sinal de Atenção |
|---------|---------------|------------------|
| Auto-avaliação inicial | 95%+ na semana 1 | Menos de 80% |
| Evidência por nível declarado | 1+ evidência forte | Nível sem evidência |
| Feedback de mentor | Até 5 dias úteis | Mais de 10 dias |
| Concordância entre avaliadores | 80%+ | Menos de 60% |
| Gaps sistêmicos tratados | Ação em até 30 dias | Gap repetido por trimestre |
| Recalibração da rubric | A cada 3 meses | Mais de 6 meses sem revisão |

O dashboard não precisa ser complexo. Uma planilha versionada já é suficiente no começo. O ponto é manter visível se a rubric está gerando melhores decisões de aprendizado.

---


## 🔧 Calibração e Manutenção da Rubric

Uma rubric boa envelhece. Isso não é defeito. É sinal de que o currículo, o KODA, os modelos e a equipe estão mudando. O risco real não é precisar recalibrar. O risco é continuar usando critérios antigos como se ainda fossem verdadeiros.

### Quando Recalibrar

Recalibre a rubric em ciclos planejados e também quando eventos específicos mostrarem que os critérios perderam aderência.

#### Recalibração Planejada

1. **A cada 3 meses:** Revisão padrão para comparar critérios com prática atual.
2. **Ao fim de cada turma do currículo:** Ajustar exemplos, evidências e perguntas que geraram confusão.
3. **Após fechamento de ciclo de performance técnica:** Usar dados agregados sem transformar a rubric em ranking individual.
4. **Antes de onboarding grande:** Garantir que novos learners não recebam exemplos obsoletos.
5. **Após revisão dos core concepts:** Sincronizar a rubric com mudanças nos materiais de `05-core-concepts/`.

#### Recalibração por Evento

1. Novo modelo muda limites de context window, tool use ou comportamento de planning.
2. Arquitetura do KODA muda o papel de algum conceito.
3. Incidente de produção revela gap que a rubric não capturava.
4. Mentores discordam com frequência sobre o mesmo critério.
5. Learners passam na avaliação, mas falham repetidamente em tarefas reais.
6. Critério de Nível 4 vira prática comum de Nível 3 por maturidade do time.
7. Ferramenta interna automatiza uma habilidade que antes exigia julgamento manual.

### Como Recalibrar sem Quebrar Confiança

1. **Declare o motivo da revisão.** Explique se a mudança veio de dados, incidente, feedback ou evolução técnica.
2. **Separe critério de pessoa.** Recalibrar não significa dizer que avaliações antigas eram falsas. Significa que o mapa mudou.
3. **Preserve histórico.** Não reescreva avaliações passadas como se tivessem usado critérios novos.
4. **Teste em amostras reais.** Antes de publicar, aplique os critérios novos em 3 a 5 casos conhecidos.
5. **Compare decisões.** Veja onde a versão nova muda o nível e confirme se a mudança faz sentido.
6. **Comunique impacto.** Diga quais conceitos mudaram, quais níveis foram afetados e que evidência nova será esperada.
7. **Dê período de transição.** Para decisões formais, permita que learners coletem nova evidência antes de rebaixar nível.

### Como Detectar Critérios Desatualizados

Critérios desatualizados raramente anunciam que falharam. Eles aparecem como pequenas distorções na prática.

#### Sinais nos Learners

1. Muitos learners atingem N3 no papel, mas precisam de ajuda constante em tarefas novas.
2. Learners dizem "não sei como provar isso" para um critério que deveria ser observável.
3. Pessoas com boa produção real ficam presas em N1 ou N2 porque o critério exige terminologia específica demais.
4. A auto-avaliação vira exercício de memorização, não de reflexão.
5. O mesmo conceito gera dúvidas repetidas apesar de mentoria clara.

#### Sinais nos Mentores

1. Mentores diferentes dão níveis diferentes para a mesma evidência.
2. A entrevista precisa de muitas exceções verbais para funcionar.
3. O mentor ignora parte da rubric porque "na prática não é bem assim".
4. Critérios de Expert dependem de feitos raros demais para o contexto atual.
5. Critérios de Intermediário ficaram fáceis demais porque o time criou templates fortes.

#### Sinais no Produto

1. Incidentes acontecem em áreas onde a equipe parecia bem avaliada.
2. Métricas de qualidade não melhoram apesar de níveis declarados subirem.
3. Novos features usam padrões que a rubric não menciona.
4. Ferramentas internas mudaram o trabalho, mas a avaliação continua manual e antiga.
5. Mudanças de catálogo, política ou modelo alteram o risco de decisões técnicas.

### Estratégia de Versionamento

A rubric deve ter versionamento simples, rastreável e fácil de consultar.

#### Formato de Versão

Use `vMAJOR.MINOR.PATCH`.

1. **MAJOR:** Mudança que altera significado de nível ou critério central.
2. **MINOR:** Novo exemplo, nova evidência, nova seção ou ajuste de calibração sem mudar o sentido principal.
3. **PATCH:** Correção de texto, clareza, link ou inconsistência pequena.

#### Exemplos de Mudança

1. `v1.1.0`: Adiciona exemplos concretos por nível para todos os conceitos.
2. `v1.2.0`: Inclui métricas de adoção e processo de recalibração.
3. `v2.0.0`: Redefine Nível 3 de Context Management após nova arquitetura de memória no KODA.
4. `v1.2.1`: Corrige wording de um critério ambíguo em Sprint Contracts.

#### Registro de Mudanças

Cada revisão deve registrar:

1. Data da mudança.
2. Pessoa ou grupo responsável.
3. Seções alteradas.
4. Motivo da mudança.
5. Impacto esperado nas avaliações.
6. Evidências usadas para justificar a alteração.
7. Prazo recomendado para próxima revisão.

### Feedback Loop com Mentores e Learners

A rubric precisa ouvir quem aplica e quem é avaliado. Sem esse loop, ela vira documento bonito e pouco verdadeiro.

#### Input dos Mentores

Colete feedback dos mentores sobre:

1. Perguntas que geraram respostas úteis.
2. Perguntas que viraram conversa vaga.
3. Critérios difíceis de observar.
4. Evidências que foram fortes, mas não estavam previstas.
5. Diferenças frequentes entre auto-avaliação e avaliação externa.
6. Conceitos onde a decisão entre níveis foi mais difícil.
7. Casos em que a rubric ajudou a evitar julgamento subjetivo.

#### Input dos Learners

Colete feedback dos learners sobre:

1. Critérios que ficaram claros.
2. Critérios que pareceram abstratos demais.
3. Gaps que a rubric ajudou a enxergar.
4. Gaps que continuaram confusos mesmo depois da mentoria.
5. Evidências que eles conseguiram coletar com facilidade.
6. Evidências que pareciam impossíveis no trabalho atual.
7. Perguntas de reflexão que mudaram sua forma de estudar.

#### Rituais Recomendados

1. **Retro mensal de mentores:** 45 minutos para discutir decisões difíceis e calibrar interpretação.
2. **Pesquisa curta com learners:** 5 perguntas após cada avaliação formal.
3. **Review trimestral de evidências:** Amostrar avaliações reais e verificar consistência.
4. **Sessão de calibration cases:** Todos avaliam o mesmo caso e comparam decisões.
5. **Backlog de melhorias da rubric:** Cada sugestão vira item com dono, motivo e decisão.

### Como Tratar Discordâncias

Discordância não é falha. Discordância é sinal de que o critério precisa de mais precisão ou de que a evidência está incompleta.

1. Se mentor e learner discordam, volte para evidência observável.
2. Se dois mentores discordam, peça que cada um cite qual linha da rubric sustenta a decisão.
3. Se a linha permite duas leituras razoáveis, abra item de recalibração.
4. Se a evidência é insuficiente, mantenha o nível mais baixo consistente e defina nova coleta.
5. Se a pessoa demonstra parte do próximo nível, registre como transição.
6. Se a discordância envolve impacto de carreira, use segundo avaliador.

### Critérios Para Aceitar Mudanças na Rubric

Uma mudança deve ser aceita quando melhora precisão, clareza ou aderência à prática real.

1. A mudança resolve ambiguidade observada em avaliações reais.
2. A mudança alinha a rubric com arquitetura atual do KODA.
3. A mudança torna evidência mais verificável.
4. A mudança reduz subjetividade entre mentores.
5. A mudança preserva a progressão dos 4 níveis.
6. A mudança não transforma a rubric em checklist mecânico.
7. A mudança mantém foco em comportamento demonstrável.

### O Que Não Fazer na Manutenção

1. Não ajustar critério para justificar uma decisão individual já tomada.
2. Não criar Nível 5 informal.
3. Não transformar Nível 4 em requisito para todo mundo.
4. Não remover critérios difíceis só porque exigem mentoria.
5. Não aceitar exemplos que medem só vocabulário.
6. Não mudar a rubric sem registrar motivo.
7. Não misturar avaliação de aprendizado com punição de performance.

### Exemplo de Recalibração Completa

**Problema detectado:** Três learners foram marcados como Nível 3 em Evaluation Rubrics porque criaram rubrics com dimensions e weights. Em produção, as rubrics não previram satisfação real do cliente.

**Análise:** O critério antigo enfatizava criação da rubric, mas não exigia correlação com outcomes ou revisão pós-uso. Isso permitia N3 sem evidência de calibração real.

**Mudança proposta:** Adicionar a N3 a exigência de comparar scores com outcomes reais e registrar ajustes de weights. Manter criação de rubric como N2 forte.

**Teste da mudança:** Aplicar a nova leitura a cinco rubrics existentes. Duas continuam N3. Três passam a N2 forte em transição para N3.

**Comunicação:** Informar que ninguém "perdeu competência". O critério ficou mais preciso sobre o que significa calibrar com dados.

**Próxima evidência:** Cada owner de rubric deve coletar 20 casos avaliados, comparar score com outcome e propor ajuste documentado.

---

## 📊 O Que Você Aprendeu

### Os 8 Conceitos e Como Avaliá-los

1. **Context Management (C1):** Você aprendeu a medir profundidade em estratégias de gerenciamento de contexto, de "sei o que é sliding window" (Básico) até "criei um pipeline adaptativo usado pelo time" (Expert).

2. **Planning vs Execution (C2):** Você aprendeu a diferenciar "entendo o problema de Planning Collapse" de "projetei sistemas com separação que reduziram erros em cascata".

3. **Generator/Evaluator (C3):** Você aprendeu a ver além da definição do padrão — de "sei que sycophancy existe" a "criei G/E adaptativo com múltiplos evaluators que aprende com erros".

4. **Sprint Contracts (C4):** Você aprendeu que contratos não são type checking — são garantias semânticas validadas em runtime, e a diferença entre implementar um contrato simples e projetar hierarquias versionadas.

5. **State Persistence (C5):** Você aprendeu que estado não é cache — é fonte de verdade, e a progressão de "salvar um JSON" até "arquitetura de estado distribuído com migração zero-downtime".

6. **Harness Evolution (C6):** Você aprendeu que harness não é estático — evolui com o sistema, e a diferença entre "adicionar uma validação" e "projetar um sistema de harness auto-calibrável".

7. **Multi-Agent Coordination (C7):** Você aprendeu que coordenar agentes não é só "rodar vários ao mesmo tempo" — é sobre topologias, protocolos, failure handling e adaptação dinâmica.

8. **Evaluation Rubrics (C8):** Você aprendeu que qualidade é um espectro — rubrics capturam o que validação binária não vê, e a jornada de "criar uma rubric simples" até "framework de rubrics auto-calibráveis".

### O Meta-Aprendizado

Além dos conceitos individuais, esta rubric ensina algo mais profundo:

**A diferença entre "saber sobre" e "saber fazer".**

O currículo KODA não existe para que você acumule definições. Existe para que você construa sistemas de agentes que funcionam em produção, por horas, com confiabilidade. A rubric existe para que você — e seus mentores — saibam exatamente onde você está nessa jornada.

**Os 4 níveis não são uma escada — são um mapa.**

Você não "sobe" de Básico para Expert uniformemente em todos os conceitos. Você se move em profundidade nos conceitos que são relevantes para seu trabalho e seu crescimento. O importante não é o nível — é a direção.

**Avaliação não é julgamento — é navegação.**

Saber que você está em N2 em C4 não é um veredito sobre sua capacidade. É um farol dizendo: "você está aqui, o porto fica ali, e este é o caminho".

### Takeaways Detalhados Para Levar Para a Prática

**1. Definição não basta.** Se a pessoa só consegue explicar o conceito em termos gerais, ela está no começo da jornada. Isso é válido e importante, mas não deve ser confundido com capacidade de implementação.

**2. Aplicação guiada tem valor próprio.** Nível 2 não é fracasso. É a fase em que templates, exemplos e padrões do time transformam teoria em prática. Muitos bugs reais são resolvidos por pessoas em N2 sólido.

**3. Autonomia aparece em contexto novo.** Para confirmar N3, mude o domínio, retire o template e peça justificativa. Se a pessoa mantém qualidade, explica trade-offs e define métricas, a compreensão ficou transferível.

**4. Expert é influência, não ego.** Nível 4 não significa falar mais bonito. Significa melhorar o padrão, ensinar outras pessoas e criar ferramentas ou critérios que sobrevivem fora da cabeça de quem criou.

**5. Evidência precisa ser proporcional ao nível.** Uma explicação oral pode confirmar N1. Um PR seguindo template pode confirmar N2. N3 pede design, implementação autônoma e métrica. N4 pede adoção, mentoria ou evolução do padrão.

**6. Cada conceito tem sua própria profundidade.** Uma pessoa pode ser Expert em Context Management e Básica em Harness Evolution. Isso não é contradição. É o retrato normal de uma equipe real.

**7. Armadilhas comuns são parte da avaliação.** Saber a definição, mas cair na armadilha, indica que a compreensão ainda não está estável. A rubric mostra essas armadilhas para que mentor e learner saibam onde testar.

**8. A melhor pergunta é concreta.** "Você entende State Persistence?" gera resposta vaga. "O cliente informou alergia no minuto 5, o agente reiniciou no minuto 80, onde essa informação deveria estar?" gera evidência.

**9. Métricas protegem contra impressão.** Se uma mudança diz melhorar context management, procure recall de fatos críticos, uso de tokens, latência e incidentes. Se uma rubric diz medir qualidade, compare score com outcome real.

**10. Recalibração mantém a rubric verdadeira.** Conforme KODA evolui, alguns critérios ficam fáceis, outros ficam irrelevantes e outros precisam nascer. A rubric deve acompanhar a prática, não congelar a prática.

### Como Esta Rubric Deve Mudar Seu Próximo 1:1

Antes, uma conversa de mentoria podia terminar com frases como "você está indo bem" ou "precisa estudar mais". Depois desta rubric, a conversa deve terminar com algo mais específico.

O mentor deve conseguir dizer: "Você está em N2 forte em C3 porque implementou G/E com template, escreveu feedback útil e debugou um retry. Para chegar a N3, falta implementar em domínio novo e medir falsos positivos do Evaluator."

O learner deve conseguir responder: "Então minha próxima evidência é um G/E sem template, com dois Evaluators e análise de precisão."

Essa clareza muda a energia da mentoria. A pessoa sai com um próximo passo, não com uma sensação vaga.

### Como Esta Rubric Deve Mudar Seu Próximo PR

Um PR também pode carregar evidência de aprendizado. A descrição pode dizer qual conceito está sendo demonstrado, qual nível a mudança tenta evidenciar e qual critério específico foi atendido.

Exemplo: "Este PR demonstra C4 N2 porque adiciona input/output contract com validação em runtime e teste de violação clara. Ainda não demonstra C4 N3 porque não inclui hierarquia de contratos nem versionamento."

Esse tipo de descrição ajuda reviewers. Também evita inflar o nível. O próprio autor aprende a separar o que provou do que ainda não provou.

### Como Esta Rubric Deve Mudar o Planejamento do Time

Quando os dados forem agregados, a equipe deve enxergar padrões.

Se quase todo mundo está em N1 em Multi-Agent Coordination, talvez não seja problema individual. Talvez o currículo precise de mais exercícios práticos ou o time precise de um workshop com traces reais.

Se muitos estão em N2 em Evaluation Rubrics, mas ninguém chega a N3, talvez faltem dados de outcomes para calibrar weights. O bloqueio não é estudo. É acesso a evidência.

Se pessoas seniores têm N3 em vários conceitos, mas N1 em Harness Evolution, talvez o KODA ainda não tenha dado oportunidades reais de manutenção de harness. Nesse caso, o plano de crescimento precisa criar essas oportunidades.

### O Resumo Operacional

1. Use a checklist para começar, não para terminar.
2. Use perguntas-gatilho para abrir a conversa.
3. Use evidências para fechar a decisão.
4. Use gaps para escolher a próxima prática.
5. Use métricas para saber se a prática melhorou o produto.
6. Use recalibração para manter a rubric honesta.
7. Use mentoria para transformar critério em crescimento.

Se você lembrar de apenas uma coisa, lembre disto: compreensão real deixa rastro. Ela aparece em código, decisão, debug, design, métrica, ensino e melhoria do padrão. A função desta rubric é tornar esse rastro visível.

### Último Check Antes de Usar

1. Escolha um conceito, não todos de uma vez.
2. Escolha uma evidência real, não uma intenção.
3. Escolha uma pergunta que force decisão, não memória.
4. Escolha um próximo passo pequeno o bastante para acontecer nesta semana.
5. Volte para a rubric quando a evidência mudar.

---

## 🔗 Próximos Passos

### Se você é um Learner:
1. Preencha a checklist de auto-avaliação para estabelecer sua baseline
2. Compare com os níveis-alvo sugeridos para seu cargo
3. Identifique os 2-3 conceitos com maior gap e priorize-os
4. Agende uma conversa com seu mentor para validar a auto-avaliação

### Se você é um Mentor:
1. Leia a seção "Guia para Mentores" com atenção
2. Prepare perguntas-gatilho para seus próximos 1:1s
3. Comece a coletar evidências para seus mentorados
4. Use a matriz de níveis-alvo para calibrar expectativas

### Se você é Tech Lead / Gestor:
1. Defina níveis-alvo oficiais para cada cargo na sua equipe
2. Incorpore a rubric ao ciclo de desenvolvimento (onboarding, check-ins, progressão)
3. Agregue dados da equipe para identificar gaps sistêmicos
4. Planeje workshops ou mentorias focadas nos conceitos com gaps maiores

---

## 📋 Metadata

| Campo | Valor |
|-------|-------|
| **Arquivo** | learning-assessment-rubric.md |
| **Pertence a** | 08-tools-templates |
| **Tipo** | Template operacional de avaliação |
| **Cobertura** | 8 core concepts × 4 níveis = 32 critérios |
| **Status** | ✅ Completo |
| **Aplicável a** | Todos os níveis do currículo (1-4) |
| **Revisão recomendada** | A cada 3 meses ou após mudanças significativas no currículo |
| **Atualizado** | Maio 2026 |
| **Próximo template relacionado** | `evaluation-rubric-template.md` (para rubricas de output de agentes) |

---

*Esta rubric é um organismo vivo. Conforme o currículo evolui, novos padrões emergem e a equipe acumula experiência de produção, os critérios devem ser recalibrados. A versão atual reflete o estado da arte em Maio de 2026. Se você identificar um critério que não captura bem a realidade, proponha uma melhoria. A rubric só é útil se for verdadeira.*

---

**Template criado para o currículo KODA Long-Running Agents.**
**Issue: #52 | Arquivo: [[curriculum/08-tools-templates/learning-assessment-rubric|Learning Assessment Rubric]]**
