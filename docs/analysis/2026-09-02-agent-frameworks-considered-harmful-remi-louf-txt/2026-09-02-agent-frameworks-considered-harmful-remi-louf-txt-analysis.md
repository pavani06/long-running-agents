---
title: "Analise de Conhecimento Nao-Obvio: Agent Frameworks Considered Harmful (Remi Louf, .txt)"
type: analysis
date: 2026-09-02
aliases: ["agent frameworks considered harmful", "Remi Louf agent kernel", "agentes como eventos", "Remi Louf .txt talk", "markdown agents event log"]
tags: [agentes-orquestracao, harness-engineering, context-engineering, error-handling, evals, production]
relates-to: ["[[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent Operating System]]", "[[docs/canonical/structured-generation-constraint-validation-circuit|Structured Generation Constraint Validation Circuit]]", "[[docs/canonical/presence-in-the-loop-metric|Presence in the Loop Metric]]", "[[docs/canonical/centralized-cross-framework-tracing|Centralized Cross-Framework Tracing]]", "[[docs/canonical/epistemic-memory-graph|Epistemic Memory Graph]]", "[[docs/analysis/2026-06-09-12-factor-agents/2026-06-09-12-factor-agents-analysis|Analise 12-Factor Agents]]", "[[docs/analysis/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt-mental-model|Mental Model do Pipeline]]"]
---

# Analise de Conhecimento Nao-Obvio: Agent Frameworks Considered Harmful (Remi Louf, .txt)

> Fonte: Remi Louf (CEO da .txt) — "Agent Frameworks Considered Harmful" (AI Engineer, 2026-08-22, 20:28)
> Transcript: `/home/pavanpavan/raw-knowledge/sources/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt.md`
> Regras: sem marketing, anedotas, historias pessoais, repeticao. A metafora do robô de corte
> foi mantida apenas onde codifica uma taxonomia tecnica.

---

## 1. Frameworks & Models

### 1.1 Taxonomia de modos de interacao humano-agente (presenca como eixo)

O palestrante classifica as interfaces de agent de hoje por quanto de atencao humana exigem,
usando uma escada de metaforas de corte de grama:

| Modo | Interface | Analogia | Atencao exigida |
|---|---|---|---|
| Interativo | TUI no terminal | trator que voce dirige mesmo que "dirija sozinho" | total — voce fica "em cima" |
| Semi-remoto | app mobile ("SSH with vibes") | controle remoto — corrige a trajetoria "de vez em quando" | parcial — voce nao esta ao lado, mas continua pilotando |
| Unattended | background agent | robô de corte autonomo, sem controle remoto | ~zero — trabalha o dia todo sozinho |

A afirmacao nao-obvia: o modo mobile (rodar agentes pelo celular durante uma caminhada,
instruindo sem pensar claramente) e "claramente transitório" — e absurdo como estado final.
O produto prometido e o modo unattended: o agente como processo de fundo que produz o
resultado sem ninguem apontar. Isso converte presenca-no-loop na metrica de maturidade da
interface (ver [[docs/canonical/presence-in-the-loop-metric|Presence in the Loop Metric]]).

### 1.2 O agente como processo: kernel vs. framework

Modelo operacional emprestado de SO, explicitamente contra o modelo de framework:

- **Kernel (runtime)**: agenda processos, isola, faz journaling (log + definicao do agente).
  O agente E um processo — ao kernel nao importa o que ele faz.
- **Userland (definicao do agente)**: o agente vive num arquivo markdown solto numa pasta;
  o runtime o descobre e executa. Um frontend alternativo poderia nao usar markdown nenhum.
- **Frameworks invertem a relacao**: "frameworks just call code — your agents live inside
  their abstractions". O agente deixa de ser um processo isolado do seu sistema e passa a
  ser um plugin dentro das abstracoes de terceiro.

O trabalho do kernel e enunciado como principio de design: **tornar acoes ruins impossiveis,
nao apenas improvaveis** — via duas fronteiras tipadas (ver 2.1).

### 1.3 Sistema de agentes = schedules + eventos (+ nada mais)

A produto inteiro construido em duas semanas e descrito como:

```
arquivo markdown por agente  +  cron (quando)  +  eventos tipados (por que)
```

- O cron cobre a dimensao **"quando"** (pontos no tempo: market watch todo dia de manha).
- Eventos cobrem a dimensao **"porque isso aconteceu"** (nova nota de voz, novo email,
  entrada nova no CRM, PR aberto/mergeado). Cron e explicitamente insuficiente: e so um
  ponto no tempo, nao reatividade.
- Nao ha camada de orquestracao adicional: "isso e a interface — voce nao escreve codigo,
  e esse e o produto inteiro ate agora".

### 1.4 O chat e uma mentira: modelo de proveniencia do prompt

Diagnostico do porque depurar agentes e tao dificil: o que voce ve na sessao de chat do
TUI **nao e o que o modelo viu**. Tres causas nomeadas:

1. **Compaction** — o contexto renderizado difere do enviado.
2. **Quirks de provider** — detalhes de montagem nao expostos.
3. **Thinking traces ocultos** — nem OpenAI nem Anthropic compartilham o raciocinio
   interno; voce "tem uma ideia" do que entrou, nunca a certeza.

Consequencia de design: um runtime de agentes precisa de um mecanismo proprio de
proveniencia exata do contexto (resolvido via content addressing, ver 2.2).

### 1.5 Runtime como divida paga por falha (accrual por erro)

O runtime nao foi desenhado antecipadamente; cada modo de falha real de producao gerou
exatamente uma peca do runtime, na ordem em que a falha apareceu:

| Falha observada | Peca do runtime que nasceu dela |
|---|---|
| Nota de voz sumiu | log append-only (tudo salvo para sempre) |
| Brief postado 2x no Slack | fila propriamente dita (contagem de tentativas, dedup) |
| Prompt destroido sem regressao rastreavel | sistema content-addressed de prompts |

Principio: "paguei a divida conforme ela aparecia" — alternativa explicita ao design
upfront de runtime, e com eles de "nothing new under the sun": orquestrar agentes e
"good old software orchestration".

---

## 2. Patterns & Architectures

### 2.1 Fronteiras tipadas: tool calls tipados + eventos tipados entre agentes

- **Problema**: acoes invalidas de modelo (chamar tool inexistente, emitir evento com schema
  errado) — na pratica ~20% dos eventos eram rejeitados quando o modelo era ruim em
  structured outputs.
- **Mechanismo**: duas fronteiras com o mundo externo, ambas validadas por schema:
  1. **Typed tool calls** — fronteira agente ↔ ferramentas.
  2. **Typed events** — fronteira agente ↔ agentes; cada agente declara o que **aceita** e
     o que **retorna** (structured outputs como contrato de saida).
- **Postura**: "non-negotiable" — o kernel existe para tornar essas acoes ruins
  *impossiveis*, nao improvaveis. Compara com
  [[docs/canonical/structured-generation-constraint-validation-circuit|Structured Generation Constraint Validation Circuit]].

### 2.2 Prompt content-addressed: prompt como grafo de hashes (estilo git/Nix)

- **Problema**: impossivel saber o que efetivamente entrou no contexto do modelo (1.4);
  prompts mudam sem rastro; compaction exige manipular strings.
- **Mechanismo**:
  1. O prompt e decomposto em partes: system prompt, descricao de cada skill, descricao de
     cada tool, user message.
  2. Cada parte e armazenada e enderecada por **hash** (content addressing — git, Nix,
     build systems: "nothing new").
  3. Antes de renderizar texto, o prompt e representado como **lista/grafo de hashes**.
  4. A resposta do modelo e armazenada no mesmo esquema; logo toda resposta traca de volta
     ao prompt exato, e do prompt ao conteudo exato do contexto.
- **O que sai de graca desse unico primitivo**:
  - **Debug**: reconstrucao exata do input do modelo.
  - **Diffs entre runs**: funcao que mostra quais componentes mudaram entre duas runs
    (user message? skill trocada? tool trocada?) e quais eram continuacao da mesma sessao.
  - **Replay**: reconstruir a request do grafo e reenviar identica — com outro modelo,
    outra request, ou modificada. Caso de uso relatado: trocar por modelos open-source ao
    ver o custo subir, e avaliar se a saida permanece satisfatoria.
  - **Compaction como manipulacao de grafo**, nao de strings.
  - **KV cache management** "indiretamente" mais facil.
  - **Auditabilidade em escala** — apontada como a principal vantagem: saber exatamente o
    que aconteceu com o agente e porque ele retornou o que retornou.

### 2.3 Log append-only com causalidade (event sourcing de agentes)

- **Problema**: trabalho perdido e debugging impossivel — "mesmo com 3-4 agentes voce ja
  tem major debugging headaches".
- **Mechanismo**: uma unica tabela append-only de eventos; todo evento e publicado la;
  eventos sao **causalmente ligados** (qual evento disparou qual evento); tudo e queryavel.
  "O log e a memoria do sistema — nada e perdido, tudo e observado."
- A cadeia causal e o que torna a navegacao de debug viavel: da falha de volta ao gatilho.

### 2.4 Topologia emergente por eventos (em vez de grafos em codigo)

- **Problema**: frameworks vendem grafos de agentes definidos em codigo — arestas para
  manter, contribuicao restrita a quem codifica.
- **Mechanismo**: agentes apenas **publicam e assinam eventos tipados**; nao existem arestas
  declaradas. "A topologia emerge do que o log diz que aconteceu." Fan-in e fan-out saem
  de graca; estender o sistema = dropar um novo arquivo markdown conhecendo os eventos
  existentes — sem codar.
- **Pipeline real descrito** (producao, funcionando):
  ```
  voice note dropada → evento → agente transcritor (aceita nota, retorna notas duraveis
  + emite voice-note-processed) → agente daily-brief (consome saida do cron + notas) →
  produz o brief → evento slack.message.post → processo assinante posta no Slack
  ```

### 2.5 Agente-como-arquivo markdown (contribuicao sem codigo)

- **Problema**: editar prompt dentro de codigo de framework — "passei todo o tempo editando
  o prompt dentro do codigo".
- **Mechanismo**: definicao do agente e um arquivo (markdown/YAML) solto numa pasta; o
  runtime o carrega e o agente "magicamente aparece". Versionavel no git, diffavel,
  reviewavel em PR.
- **Efeito organizacional medido**: apos um mes de deploy interno, 20 agentes em producao —
  "contribuidos nao apenas por gente tecnica".

---

## 3. Operational Lessons

| Licao | Contexto |
|---|---|
| Background agents bem executados sao "magicos" | brief matinal gerado sozinho, "provavelmente melhor do que faria manualmente" — o valor realizavel da promessa original |
| As dificuldades sao "good old engineering problems" | nada novo sob o sol em orquestracao de agentes; e orquestracao de software classica (filas, logs, retries, versionamento) |
| Modelos open-source ja sao suficientes para essa workload | substituiu todas as APIs terceiras; roda modelo local ate no laptop — "bom o suficiente para o que faco com isso" (para coding, desconhecido) |
| Observabilidade revela custo rapido | "quando voce tem observabilidade, percebe que o custo sobe muito rapido" — motivacao direta para replay com modelos mais baratos |
| A categoria de infra esta indefinida: build antes de buy | tentar algumas coisas antes de construir; construir primeiro para "saber exatamente o que precisa e as limitacoes do que existe" — vantagem peculiar para tech CEO de empresa pequena (fazer sem tirar engenheiros da linha) |
| Framework builders: "eat your own dog food" | "as vezes e bem claro que quem constroi agent orchestration frameworks nao usa o proprio produto" |
| Primeira versao em ~1 dia com Codex | "fui de trampa" — usou o agente para escrever o sistema; o resto da semana foi gasto nos modos de falha e no runtime |
| Imersao dedicada muda trajetoria | duas semanas de imersao pratica mudaram a trajetoria da empresa — contra o modo "so pensando no next thing" |

---

## 4. Tradeoffs

| Decisao | Beneficio | Custo |
|---|---|---|
| Markdown/YAML em vez de codigo de framework | versionavel, diffavel, review em PR; contribuicao por nao-codificadores; onboarding de agente = drop de arquivo | YAML e odiado; menos expressividade que codigo; dependencia do runtime que o consome |
| Eventos em vez de grafos em codigo | zero arestas para manter; fan-in/fan-out gratis; topologia emergente; extensivel por quem conhece os eventos | nenhuma visao global declarada — a topologia so existe "no que o log diz que aconteceu"; descoberta depende de conhecer os eventos existentes |
| Content addressing de prompts (git/Nix style) | diffs entre runs, replay com outro modelo, compaction como grafo, KV cache, auditabilidade total | "deep rabbit hole" — investimento grande; nasceu de uma falha, nao de um plano |
| Fronteiras tipadas obrigatorias (tools + eventos) | acoes ruins impossiveis (nao so improvaveis); elimina ~20% de eventos invalidos | custo de schema/validacao em toda fronteira; acoplamento a stack de structured outputs |
| Build antes de buy (infra unsettled) | conhecimento exato das proprias necessidades e dos limites do mercado | tempo do CEO/engineering; manutencao do runtime proprio |
| Divida paga por falha (sem design upfront de runtime) | cada peca do runtime tem uma justificativa observada; nada especulativo | o sistema quebra em producao primeiro — as falhas sao o metodo, nao o acidente |

---

## 5. Failure Patterns

| Padrao | Causa | Mitigacao |
|---|---|---|
| Entrega duplicada (brief postado 2x no Slack) | sem fila: multiplas tentativas sem contagem, sem dedup | fila com contagem de tentativas e semantica de entrega |
| Trabalho perdido (nota de voz sumiu) | nada persistido entre passos | log append-only — "tudo salvo para sempre" |
| Regressao irreproduzivel (market brief virou lixo apos semana de tweaks de prompt) | prompts alterados sem versionamento; impossivel lembrar qual mudanca quebrou | content addressing de prompts + diff entre runs |
| Eventos invalidos (~20% rejeitados) | modelo fraco em structured outputs emitindo payload fora do schema | fronteiras tipadas com validacao (tornar imposssivel, nao improvavel) |
| Opacidade de debug (nao saber o que o modelo viu) | chat UI nao representa o contexto real: compaction, quirks, thinking traces ocultos | grafo de hashes do prompt — resposta traca ate o input exato |
| Dor de custo ao observar | telemetria revela burn de API subindo rapido | replay do grafo com modelos open-source/locais |

Padrao transversal: cada falha de producao mapeou 1:1 para uma peca do runtime — o
runtime e o sedimento das falhas, nao um design anterior a elas.

---

## 6. Synthesis

O titulo fala de frameworks, mas a tese real e de **dissolucao de camada**: quando o
runtime assume as responsabilidades classicas de um kernel (agendamento, isolamento,
journaling) e a definicao do agente vira um arquivo declarativo, a "camada de framework"
perde razao de existir — o que frameworks empacotam como grafo em codigo reaparece como
duas primitivas baratas (cron e evento tipado) mais um log. A segunda tese, nao nomeada
pelo autor mas central: **um unico primitivo — o evento content-addressed e causalmente
encadeado — e a origem de quase todo o resto**. Debug, diffs, replay, compaction, KV
cache, auditabilidade e ate a viabilidade de trocar modelo por custo derivam do mesmo
grafo de hashes; nenhuma dessas capacidades foi construida isoladamente. Terceira tese
implicita: a escada de maturidade do produto e medida em **atencao humana removida**
(TUI → celular → unattended), nao em capacidade do modelo — a interface e o gargalo
transitorio, e o "absurdo" de pilotar agentes pelo celular durante uma caminhada e o
sintoma. Por fim, o metodo e tao importante quanto a arquitetura: o runtime foi
**acrescido por falha**, cada componente com uma justificativa observada em producao —
um contraponto pragmatico ao design upfront de "agent operating systems", e eco direto
do [[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent Operating System]]
e da instrumentacao de
[[docs/canonical/centralized-cross-framework-tracing|Centralized Cross-Framework Tracing]],
com proveniencia de grafo parente do
[[docs/canonical/epistemic-memory-graph|Epistemic Memory Graph]].
