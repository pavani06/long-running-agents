---
title: "Padroes Reutilizaveis de Sistemas Agenticos: Agent Frameworks Considered Harmful (Remi Louf, .txt)"
type: analysis
date: 2026-09-02
tags: [agentes-orquestracao, harness-engineering, context-engineering, error-handling, production]
aliases: ["padroes Remi Louf .txt", "agent frameworks patterns", "padroes kernel de agentes", "padroes eventos tipados e content addressing"]
relates-to: ["[[docs/analysis/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt-analysis|Analise Agent Frameworks Considered Harmful]]", "[[docs/analysis/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt-mental-model|Mental Model do Pipeline]]", "[[docs/canonical/structured-generation-constraint-validation-circuit|Structured Generation Constraint Validation Circuit]]", "[[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent Operating System]]", "[[docs/canonical/presence-in-the-loop-metric|Presence in the Loop Metric]]"]
---

# Padroes Reutilizaveis de Sistemas Agenticos: Agent Frameworks Considered Harmful (Remi Louf, .txt)

Modo de extracao: **FILE**. Unica entrada de conhecimento: o arquivo de analise
`2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt-analysis.md` neste mesmo
diretorio, lido na integra. Escopo: apenas padroes aplicaveis a sistemas agenticos;
marketing, anedotas e licoes puramente organizacionais foram excluidos.

## 1. Typed Tool and Event Boundaries

- **name:** Typed Tool and Event Boundaries
- **problem solved:** Acoes invalidas do modelo (chamar tool inexistente, emitir evento fora do schema) atravessam o runtime sem serem barradas; com modelos fracos em structured outputs, ~20% dos eventos eram rejeitados depois de publicados.
- **inputs:**
  - Tool calls emitidos pelo modelo na fronteira agente-ferramentas.
  - Eventos publicados e consumidos na fronteira agente-agentes.
  - Schemas declarados por agente: o que aceita e o que retorna (structured outputs como contrato de saida).
  - Validador no kernel aplicado em ambas as fronteiras.
- **outputs:**
  - Tool calls e eventos garantidamente conformes ao schema, ou rejeitados na fronteira antes de produzir efeito.
  - Contrato de entrada e saida explicito e consultavel por agente.
- **benefits:**
  - Torna acoes ruins impossiveis, nao apenas improvaveis (postura "non-negotiable" do kernel).
  - Elimina a perda de ~20% de eventos invalidos observada antes das fronteiras.
  - Contratos tipados entre agentes substituem convencoes implicitas de payload.
- **limitations:**
  - Custo de schema e validacao em toda fronteira, em toda chamada.
  - Acoplamento a stack de structured outputs do provider.
  - A fronteira rejeita, nao corrige: modelo ruim em structured outputs continua gerando carga rejeitada.

## 2. Content-Addressed Prompt Graph

- **name:** Content-Addressed Prompt Graph
- **problem solved:** E impossivel saber o que efetivamente entrou no contexto do modelo: a sessao de chat nao representa o prompt real (compaction, quirks de provider, thinking traces ocultos); prompts mudam sem rastro; compaction vira manipulacao de strings.
- **inputs:**
  - Partes decompostas do prompt: system prompt, descricao de cada skill, descricao de cada tool, user message.
  - Funcao de hash e armazenamento enderecado por conteudo (estilo git/Nix).
  - Respostas do modelo no mesmo esquema de enderecamento.
- **outputs:**
  - Prompt representado como lista/grafo de hashes antes da renderizacao em texto.
  - Resposta que traca de volta ao prompt exato, e do prompt ao conteudo exato do contexto.
  - Diffs entre runs (qual componente mudou: user message, skill, tool) e replay identico com outro modelo ou modificacao.
  - Compaction como manipulacao de grafo; KV cache management facilitado.
- **benefits:**
  - Debug por reconstrucao exata do input do modelo.
  - Regressao de prompt rastreavel (qual mudanca quebrou o output).
  - Troca de modelo por custo (open-source/local) com avaliacao de se a saida permanece satisfatoria.
  - Auditabilidade em escala: saber exatamente o que aconteceu e porque o agente retornou o que retornou.
- **limitations:**
  - Investimento grande; o proprio autor chama de "deep rabbit hole".
  - Nasceu de uma falha de producao, nao de um plano: exige a dor antes da peca.
  - Exige disciplina de content addressing em toda peca de prompt, sem excecoes.

## 3. Append-Only Causal Event Log

- **name:** Append-Only Causal Event Log
- **problem solved:** Trabalho perdido entre passos e debugging impossivel com multiplos agentes; "mesmo com 3-4 agentes voce ja tem major debugging headaches".
- **inputs:**
  - Eventos publicados por todos os agentes e processos do sistema.
  - Ligacoes causais registradas no momento do evento (qual evento disparou qual evento).
  - Tabela unica append-only como destino obrigatorio.
- **outputs:**
  - Log unico, queryavel, imutavel ("o log e a memoria do sistema; nada e perdido, tudo e observado").
  - Cadeia causal navegavel de qualquer falha de volta ao gatilho.
- **benefits:**
  - Elimina trabalho perdido: tudo salvo para sempre.
  - Debug viavel: da falha de volta ao gatilho pela cadeia causal.
  - Substrato para topologia emergente (padrao 4) e para auditoria.
- **limitations:**
  - Volume de armazenamento cresce sem remocao.
  - Exige disciplina de publicacao: valor do log depende de todo evento ser publicado.
  - Causalidade precisa ser capturada no momento do evento; reconstrucao posterior nao e confiavel.

## 4. Emergent Event Topology

- **name:** Emergent Event Topology
- **problem solved:** Grafos de agentes definidos em codigo (o que frameworks vendem) criam arestas para manter e restringem contribuicao a quem codifica.
- **inputs:**
  - Agentes que apenas publicam e assinam eventos tipados.
  - Schemas de eventos publicos e conhecidos.
  - Log de eventos como registro do que aconteceu.
- **outputs:**
  - Topologia que emerge do que o log diz que aconteceu; nenhuma aresta declarada em codigo.
  - Fan-in e fan-out gratuitos; extensao do sistema por drop de novo arquivo de agente conhecendo os eventos existentes.
- **benefits:**
  - Zero arestas para manter.
  - Extensao sem codar; pipeline real de producao (voice note, transcritor, daily brief, Slack) rodando nesse modelo.
  - Contribuicao desacoplada do codigo da orquestracao.
- **limitations:**
  - Nenhuma visao global declarada: a topologia so existe no log.
  - Descoberta depende de conhecer os eventos existentes.
  - Debug depende integralmente do log causal (padrao 3).

## 5. Agent as Declarative File

- **name:** Agent as Declarative File
- **problem solved:** Editar prompt dentro de codigo de framework ("passei todo o tempo editando o prompt dentro do codigo") e restringir criacao de agentes a engenheiros.
- **inputs:**
  - Arquivo markdown/YAML solto numa pasta com a definicao do agente (prompt, ferramentas, eventos aceitos/retornados, schedule).
  - Runtime que escaneia a pasta e carrega definicoes.
- **outputs:**
  - Agente descoberto e executado; o agente "magicamente aparece".
  - Definicao versionavel no git, diffavel, reviewavel em PR.
- **benefits:**
  - Onboarding de agente = drop de arquivo.
  - Contribuicao por nao-codificadores: 20 agentes em producao em um mes, "contribuidos nao apenas por gente tecnica".
  - Frontend alternativo poderia nem usar markdown: o formato e da userland, nao do kernel.
- **limitations:**
  - YAML/markdown e menos expressivo que codigo ("YAML e odiado").
  - Dependencia do runtime que consome o formato.
  - Capacidade de agentes limitada ao que o formato declarativo expressa.

## 6. Agent Kernel Runtime

- **name:** Agent Kernel Runtime
- **problem solved:** Frameworks invertem a relacao de posse: "frameworks just call code; your agents live inside their abstractions"; o agente deixa de ser processo isolado do seu sistema e vira plugin de terceiro.
- **inputs:**
  - Definicoes declarativas de agentes (userland).
  - Scheduler de processos, isolamento por processo, journaling (log + definicao do agente).
  - Fronteiras tipadas de tool calls e eventos.
- **outputs:**
  - Runtime que agenda processos, isola execucao e registra journal; ao kernel nao importa o que o agente faz.
  - O agente como processo de primeiro classe do sistema do usuario.
- **benefits:**
  - Inverte a relacao do framework: as abstracoes de terceiro nao posedm o agente.
  - Reutiliza responsabilidades classicas de SO (agendamento, isolamento, journaling) em vez de reinventa-las.
  - Permite trocar o frontend de definicao sem trocar o kernel.
- **limitations:**
  - Manutencao do runtime proprio (tradeoff build vs buy com infra de agentes ainda indefinida).
  - O kernel so e completo com as demais pecas: log causal, content addressing, fila com dedup.
  - Menor velocidade inicial que adotar framework pronto.

## 7. Cron plus Typed Events Orchestration Surface

- **name:** Cron plus Typed Events Orchestration Surface
- **problem solved:** Camadas adicionais de orquestracao (grafos em codigo, workflows de framework) para expressar quando um agente roda e porque ele rodou.
- **inputs:**
  - Cron: a dimensao "quando" (pontos no tempo; ex.: market watch todo dia de manha).
  - Eventos tipados: a dimensao "porque isso aconteceu" (nova nota de voz, novo email, entrada no CRM, PR aberto/mergeado).
  - Arquivos declarativos de agente que declaram schedules e assinaturas.
- **outputs:**
  - Sistema de agentes completo sem camada de orquestracao adicional: "isso e a interface; voce nao escreve codigo, e esse e o produto inteiro".
  - Reatividade a mudancas do mundo externo, nao apenas a pontos no tempo.
- **benefits:**
  - Duas primitivas baratas substituem a camada de framework inteira.
  - "Good old software orchestration": nada novo sob o sol, filas e eventos classicos.
  - Interface declarativa em vez de codigo de orquestracao.
- **limitations:**
  - Cron isolado e explicitamente insuficiente: e so um ponto no tempo, nao reatividade.
  - A composicao dos dois eixos depende de eventos tipados (padrao 1) para nao virar spaghetti de payloads.
  - Sem visao declarada do conjunto: o que existe so aparece no log.

## 8. Failure-Accrued Runtime Growth

- **name:** Failure-Accrued Runtime Growth
- **problem solved:** Design upfront de runtime produz pecas especulativas sem justificativa observada; a alternativa e pagar a divida conforme ela aparece.
- **inputs:**
  - Sistema rodando em producao real.
  - Falhas observadas e registradas: nota de voz sumiu, brief postado 2x no Slack, prompt destruido sem regressao rastreavel.
  - Mapa 1:1 falha, peca.
- **outputs:**
  - Peca minima de runtime adicionada por falha, na ordem em que a falha apareceu: log append-only (trabalho perdido), fila com contagem de tentativas e dedup (entrega duplicada), prompts content-addressed (regressao irreproduzivel).
  - Runtime como sedimento das falhas, nao design anterior a elas.
- **benefits:**
  - Nada especulativo: cada peca tem uma justificativa observada em producao.
  - Contraponto pragmatico ao design upfront de "agent operating systems".
  - Primeira versao funcional rapida (~1 dia); o resto do tempo vai para modos de falha e runtime.
- **limitations:**
  - O sistema quebra em producao primeiro: as falhas sao o metodo, nao o acidente.
  - Exige observabilidade e producao real rodando para gerar as falhas que justificam as pecas.
  - Custo de estabilidade durante o acrescimo.

## 9. Presence-in-the-Loop Interface Ladder

- **name:** Presence-in-the-Loop Interface Ladder
- **problem solved:** Medir maturidade de interface de agente por capacidade do modelo esconde o gargalo real: quanta atencao humana a interface exige.
- **inputs:**
  - Inventario de interfaces de agente (TUI interativa, app mobile semi-remota, background agent unattended).
  - Avaliacao de atencao exigida por modo (total, parcial, ~zero).
  - Meta de produto de reduzir presenca humana.
- **outputs:**
  - Classificacao em escada: interativo (atencao total), semi-remoto ("SSH with vibes", atencao parcial), unattended (~zero).
  - Decisao direcional: o produto prometido e o modo unattended; o modo mobile e "claramente transitorio".
- **benefits:**
  - Presenca-no-loop como metrica de maturidade da interface, independente do modelo.
  - Identifica o absurdo de pilotar agentes pelo celular como sintoma de interface transitoria.
  - Direciona investimento para remover o humano do loop, nao para aumentar capacidade do modelo.
- **limitations:**
  - Taxonomia de produto, nao mecanismo: nao implementa nada por si.
  - O degrau unattended exige todos os demais padroes (log, fronteiras tipadas, replay) para ser seguro.
  - Unattended reduz presenca a ~zero, nao a zero: falhas ainda escalam para humanos.
