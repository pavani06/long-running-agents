# Analise de Conhecimento Nao-Obvio: Context Management in Agents (Arize / Alex)

> Fonte: Sally-Ann Delucia, Arize - "How We Solved Context Management in Agents" (AI Engineer, 2026-05-10)
> Extraido: 2026-06-09
> Regras: sem marketing, autopromocao, anedotas, historias pessoais, filler ou repeticao

---

## 1. Frameworks & Models

### 1.1 Context Engineering como Selecao Estrategica

O modelo central da palestra e que context management nao e apenas ficar abaixo do limite de tokens. Context engineering e a disciplina de escolher estrategicamente o que o modelo ve, porque a aplicacao roda sobre esse contexto e a qualidade do produto depende da informacao exposta ao agente (`aggregated-context-management.md:103`, `aggregated-context-management.md:106`, `aggregated-context-management.md:113`, `aggregated-context-management.md:119`).

Componentes do modelo:

- **Lembrar o necessario**: manter os dados que sustentam continuidade conversacional, interpretacao de follow-ups e decisao correta.
- **Esquecer o desnecessario**: remover bulk, duplicatas, resultados intermediarios e partes do historico que nao devem competir por atencao.
- **Recuperar o omitido**: mover informacao removida para um storage acessivel por ferramentas, em vez de confiar que ela desapareceu ou foi comprimida sem perdas.
- **Medir degradacao**: usar evals de sessao longa para descobrir quando a estrategia deixou de preservar informacao suficiente.

A implicacao nao-obvia e que contexto e uma decisao de produto e UX, nao apenas uma tecnica de engenharia: se o agente nao ve os dados corretos, ele responde mal e o usuario abandona o produto (`aggregated-context-management.md:145`, `aggregated-context-management.md:147`, `aggregated-context-management.md:152`, `aggregated-context-management.md:157`).

### 1.2 Separacao Contexto vs. Memoria

A palestra separa dois papeis que costumam ser misturados: contexto e o que o modelo ve agora; memoria e o que sobrevive fora da janela ativa e pode ser recuperado depois (`aggregated-context-management.md:189`, `aggregated-context-management.md:192`, `aggregated-context-management.md:290`, `aggregated-context-management.md:451`).

Componentes do modelo:

- **Active context**: head, tail, system prompt estavel, historico leve e resultado mais recente.
- **Memory store**: meio removido, mensagens antigas, tool calls longos, IDs e previews.
- **Retrieval tool**: mecanismo pelo qual o agente solicita trechos omitidos quando julga que eles importam.
- **Long-term memory ausente**: a memoria descrita ainda e memoria de contexto da conversa, nao memoria persistente cross-session.

O ponto critico e que memoria nao substitui contexto. Ela torna a truncagem recuperavel, mas ainda exige uma politica para decidir o que entra, o que sai e como o agente descobre o que deve buscar.

### 1.3 Agente Analista Constrangido pelos Proprios Dados

Alex expôs um modelo de falha recursiva: o agente analisava traces e spans de agentes, mas essa analise gerava mais span data, aumentava o contexto, batia limites, falhava, tentava de novo com ainda mais dados e repetia o ciclo (`aggregated-context-management.md:161`, `aggregated-context-management.md:170`, `aggregated-context-management.md:173`, `aggregated-context-management.md:183`).

Componentes do modelo:

- **Objeto analisado**: traces, spans, prompts, inputs, metadata, historico e tool calls.
- **Agente analista**: o proprio harness que precisa consumir esses dados para diagnosticar ou otimizar aplicacoes.
- **Loop de crescimento**: cada tentativa de analise cria mais dados para a tentativa seguinte.
- **Restricao operacional**: o sistema que analisa a telemetria fica limitado pela telemetria que precisa analisar.

Esse modelo e especialmente relevante para observability agents: quanto melhor a instrumentacao, maior o risco de o payload de observabilidade virar o gargalo do agente que deveria interpreta-lo.

### 1.4 Context Quality como Propriedade Observavel por Evals

Como Arize ainda nao possui uma metrica formal de qualidade de contexto nem um budget principiado, long-session evals funcionam como proxy operacional: se a resposta no turno N+1 degrada depois de carregar N turnos, a estrategia de contexto falhou em preservar o que importava (`aggregated-context-management.md:462`, `aggregated-context-management.md:468`, `aggregated-context-management.md:470`, `aggregated-context-management.md:624`).

Componentes do modelo:

- **Carga historica controlada**: carregar uma sequencia anterior de turnos.
- **Pergunta futura**: testar o proximo turno, onde a falha costuma aparecer.
- **Sinal de regressao**: transformar esquecimento tardio em bug reproduzivel.
- **Proxy de qualidade**: avaliar a estrategia de contexto pelo comportamento final do agente, nao pelo tamanho do prompt.

---

## 2. Patterns & Architectures

### 2.1 Smart Truncation: Head + Tail + Memory

**Problema**: um contexto grande demais precisa ser reduzido sem destruir continuidade, referencias de follow-up ou acesso a tool calls importantes.

**Mecanica**:

```
large_context = [head][middle][tail]
active_context = [system_prompt][head][tail][latest_result]
memory_store = [middle + older messages + long tool calls]
retrieval_tool = IDs + location + preview
```

Alex mantem o comeco e o fim, remove o meio para uma memoria recuperavel, preserva o system prompt, mantem o resultado mais recente e permite que o agente busque mensagens ou tool calls omitidos quando precisar (`aggregated-context-management.md:254`, `aggregated-context-management.md:260`, `aggregated-context-management.md:263`, `aggregated-context-management.md:269`, `aggregated-context-management.md:271`, `aggregated-context-management.md:273`, `aggregated-context-management.md:277`).

A escolha de head + tail e nao apenas head preserva dois tipos de ancora: o inicio da estrutura e o estado mais recente. O meio vira memoria porque costuma conter bulk recuperavel, nao necessariamente contexto ativo.

### 2.2 Memory Store com IDs, Posicao e Preview

Na Q&A, a implementacao atual e descrita como dados salvos em banco com IDs. Alex recebe uma ferramenta com todos os IDs, onde no historico deve acessar, quantas mensagens antes e um preview do conteudo (`aggregated-context-management.md:538`, `aggregated-context-management.md:540`, `aggregated-context-management.md:541`, `aggregated-context-management.md:543`, `aggregated-context-management.md:544`).

**Problema**: se o agente pode recuperar qualquer coisa omitida, ele ainda precisa decidir o que buscar sem recolocar tudo no contexto.

**Mecanica**:

- Salvar blobs omitidos fora da janela ativa.
- Representar cada blob por ID estavel.
- Expor metadados de localizacao conversacional.
- Fornecer preview suficiente para escolha, mas pequeno o bastante para nao recriar o problema.
- Recuperar sob demanda somente os trechos que o agente julga relevantes.

O detalhe nao-obvio e que o preview vira uma segunda camada de contexto: pequeno demais e o agente nao sabe o que recuperar; grande demais e a memoria externa volta a poluir a janela ativa.

### 2.3 Long-Session Evals: Load N, Test N+1

**Problema**: bugs de contexto aparecem tarde, depois que usuarios acumulam historico suficiente para estressar truncagem e memoria (`aggregated-context-management.md:311`, `aggregated-context-management.md:316`, `aggregated-context-management.md:321`).

**Mecanica**:

```
1. Carregar 10 turnos de uma conversa realista.
2. Aplicar a estrategia normal de contexto e memoria.
3. Testar a resposta do 11o turno.
4. Falhar o eval quando o agente esquece ou interpreta follow-up como conversa nova.
```

Esse padrao transforma late-session forgetting em teste de regressao, em vez de depender de reporte de usuario ou inspeção manual tardia (`aggregated-context-management.md:322`, `aggregated-context-management.md:332`, `aggregated-context-management.md:333`, `aggregated-context-management.md:335`).

### 2.4 Sub-Agents para Isolar Contextos Pesados

**Problema**: nem todo contexto pertence ao mesmo agente. Search sobre traces pode envolver multiplas queries, centenas de spans e muito raciocinio intermediario, mas o usuario nao precisa carregar tudo isso na conversa principal (`aggregated-context-management.md:343`, `aggregated-context-management.md:344`, `aggregated-context-management.md:351`, `aggregated-context-management.md:355`).

**Mecanica**:

```
Antes:
[main agent: chat history + heavy data + search + intermediate reasoning]

Depois:
[main agent: chat history + light context]
        -> delegate -> [sub-agent: heavy data + search + intermediate reasoning]
        <- result ---
```

O main agent mantem historico e contexto leve; sub-agents ficam com os dados pesados e devolvem apenas resultados sintetizados para a conversa principal (`aggregated-context-management.md:369`, `aggregated-context-management.md:371`, `aggregated-context-management.md:376`, `aggregated-context-management.md:380`, `aggregated-context-management.md:383`).

O padrao nao e apenas paralelismo ou especializacao. Ele e particionamento de janelas de contexto: cada sub-agent recebe seu proprio espaco de trabalho e impede que raciocinio intermediario contamine o chat principal.

### 2.5 Main Conversation como Superficie Leve de UX

Alex observou que usuarios tendem a permanecer em um unico chat enquanto navegam entre paginas do produto (`aggregated-context-management.md:299`, `aggregated-context-management.md:309`, `aggregated-context-management.md:439`). A arquitetura resultante trata a conversa principal como superficie de continuidade do usuario, nao como local para todo o trabalho computacional.

**Problema**: o usuario quer continuidade, mas a implementacao precisa manter a janela principal pequena.

**Mecanica**:

- A conversa principal conserva o fio conversacional e os resultados finais.
- Dados volumosos ficam em memoria externa ou sub-agents.
- Search, trace analysis e operacoes data-intensive retornam outputs compactos.
- Se necessario, o main agent recupera memoria ou delega novamente.

Esse desenho separa continuidade de UX de completude de dados. O usuario ve uma conversa continua, mas o sistema evita um contexto monolitico.

### 2.6 Iterative Context Strategy Loop

A estrategia apresentada nao foi descoberta de primeira. O loop operacional foi: naive truncation, falha de continuidade; summarization, falha de controle; smart truncation + memory, estabilidade temporaria; long-session evals, descoberta de degradacao tardia; sub-agents, particionamento de trabalho pesado; pesquisa atual em long-term memory e metricas (`aggregated-context-management.md:202`, `aggregated-context-management.md:235`, `aggregated-context-management.md:254`, `aggregated-context-management.md:322`, `aggregated-context-management.md:363`, `aggregated-context-management.md:429`, `aggregated-context-management.md:462`).

**Problema**: uma unica tecnica de compaction nao resolve todos os regimes de crescimento de contexto.

**Mecanica**:

- Comecar por tecnicas simples e observar onde quebram.
- Transformar falhas em evals reproduziveis.
- Mover bulk de contexto para memoria ou sub-agents.
- Reavaliar quando o comportamento real de uso muda.

---

## 3. Operational Lessons

### 3.1 Over-Truncation Quebra Raciocinio Antes de Quebrar Execucao

Truncar apenas o comeco parece funcionar em tarefas simples, mas follow-ups passam a parecer novas conversas. O agente responde ao primeiro pedido e perde a referencia quando o usuario pergunta sobre um item mencionado antes (`aggregated-context-management.md:203`, `aggregated-context-management.md:214`, `aggregated-context-management.md:219`, `aggregated-context-management.md:226`).

Licao: uma estrategia pode passar em casos single-turn e ainda falhar no uso real multi-turn. Testar apenas a primeira resposta superestima qualidade.

### 3.2 Summarization Falhou por Falta de Controle, Nao por Falta de Compressao

Resumo por LLM parecia a solucao obvia, mas foi inconsistente porque deixava o proprio modelo decidir o que importava (`aggregated-context-management.md:235`, `aggregated-context-management.md:244`, `aggregated-context-management.md:246`, `aggregated-context-management.md:249`).

Licao: compressao sem politica de importancia e lossy de um jeito dificil de auditar. O problema nao e apenas reduzir tokens; e preservar as partes certas com mecanismo de recuperacao.

### 3.3 Uso Real Altera o Regime de Contexto

Alex comecou vendo conversas com menos de 10 turnos e depois usuarios chegaram a 20+ turnos enquanto atravessavam o produto (`aggregated-context-management.md:431`, `aggregated-context-management.md:434`, `aggregated-context-management.md:437`, `aggregated-context-management.md:439`).

Licao: uma estrategia validada no regime inicial de uso pode degradar quando o produto fica mais util. Mais sucesso do agente gera sessoes mais longas, que por sua vez tornam contexto mais dificil.

### 3.4 Sub-Agents Viraram o Padrao Recorrente para Contexto Extremo

Mesmo depois de smart truncation, prompts e inputs muito grandes ainda batem limites de provider, especialmente quando clientes querem que Alex analise system prompts, mensagens, historico e traces de seus proprios agentes (`aggregated-context-management.md:408`, `aggregated-context-management.md:411`, `aggregated-context-management.md:413`, `aggregated-context-management.md:417`). O padrao recorrente foi continuar quebrando trabalho em sub-agents e deixar partes diferentes manejarem contextos diferentes (`aggregated-context-management.md:421`, `aggregated-context-management.md:423`).

Licao: quando o payload e intrinsecamente grande, compaction local nao basta. A arquitetura precisa dividir ownership de contexto.

### 3.5 Context Management Precisa de Produto, Evals e Observabilidade Juntos

Arize trata contexto como problema de UX, usa evals para sinal de degradacao e usa o caso de trace/span analysis como motivacao operacional (`aggregated-context-management.md:145`, `aggregated-context-management.md:322`, `aggregated-context-management.md:470`, `aggregated-context-management.md:497`).

Licao: contexto nao pode ser otimizado apenas por heuristicas internas de token. Ele precisa ser conectado a comportamento de usuario, falhas observadas e regressao automatizada.

### 3.6 Long-Term Memory Surge Quando Usuarios Esperam Continuidade Cross-Session

A memoria atual de Alex recupera contexto omitido da conversa, mas nao resolve referencias a assuntos discutidos em chats anteriores. Essa dor cresce quando usuarios querem iniciar novo chat sem perder continuidade (`aggregated-context-management.md:447`, `aggregated-context-management.md:449`, `aggregated-context-management.md:452`, `aggregated-context-management.md:453`, `aggregated-context-management.md:455`, `aggregated-context-management.md:457`).

Licao: ha uma fronteira clara entre memory store de truncagem e memoria de produto. A primeira salva tokens omitidos; a segunda sustenta identidade, preferencias e historico entre sessoes.

---

## 4. Tradeoffs

| Decisao | Beneficio | Custo |
|---|---|---|
| Naive truncation first-only | Implementacao simples e reducao imediata de tokens | Perde continuidade; follow-ups parecem conversas novas; raciocinio multi-turn quebra |
| Summarization completa | Compressao agressiva em linguagem natural | Sem controle confiavel sobre o que sobrevive; inconsistente para analise de traces |
| Smart truncation head + tail + memory | Preserva ancoras e torna o meio recuperavel; mantem contexto ativo pequeno | Ainda heuristico; exige storage, IDs, previews e tool de recuperacao |
| Preservar system prompt durante truncagem | Mantem instrucoes do harness estaveis enquanto bulk sai do contexto | Reduz menos tokens do que truncar tudo uniformemente; exige separar prompt de payload |
| Memory store sob demanda | Evita recolocar todo o historico no prompt; da controle ao agente | Depende de bons metadados e previews; recuperacao errada ainda causa perda de contexto |
| Long-session evals N+1 | Torna falhas tardias reproduziveis antes de reporte de usuario | Cobre apenas cenarios modelados; nao substitui metrica formal de context quality |
| Sub-agents para heavy data | Mantem conversa principal leve e isola raciocinio intermediario | Mais complexidade de delegacao, composicao de resultados e coordenacao entre contextos |
| Heuristica first-100/last-100 | Simples, previsivel e funcionou por meses | Sem budget principiado; pode preservar bytes errados quando estrutura do payload muda |
| Foco atual em long-term memory antes de cache optimization | Ataca a principal dor reportada por usuarios | Adia sofisticacao em cache invalidation e eficiencia de contexto |

---

## 5. Failure Patterns

1. **Vicious context loop**: o agente analisa dados de agente, gera mais spans, aumenta o contexto, falha por limite e tenta novamente com ainda mais dados. Causa: telemetria e payload de analise competem pela mesma janela. Mitigacao: smart truncation, memoria externa e sub-agents (`aggregated-context-management.md:170`, `aggregated-context-management.md:174`, `aggregated-context-management.md:183`).
2. **First-only truncation**: manter so o inicio do blob faz tarefas simples passarem, mas follow-ups perdem referencia. Causa: estado recente e relacoes conversacionais somem. Mitigacao: preservar head + tail e mover middle para memoria (`aggregated-context-management.md:203`, `aggregated-context-management.md:219`, `aggregated-context-management.md:260`).
3. **Lossy summarization drift**: resumo por LLM remove ou altera detalhes importantes sem criterio auditavel. Causa: o summarizer decide importancia sozinho. Mitigacao: trocar resumo opaco por truncagem recuperavel e storage externo (`aggregated-context-management.md:244`, `aggregated-context-management.md:247`, `aggregated-context-management.md:587`).
4. **Late-session forgetting**: estrategia parece boa no inicio, mas falha depois de conversas longas. Causa: usuarios nao reiniciam chats e contexto acumulado degrada continuidade. Mitigacao: long-session evals carregando N turnos e testando N+1 (`aggregated-context-management.md:299`, `aggregated-context-management.md:316`, `aggregated-context-management.md:332`).
5. **Monolithic heavy search context**: chat history, dados pesados, search e raciocinio intermediario ficam no mesmo agente. Causa: falta de separacao entre conversa principal e tarefa data-intensive. Mitigacao: sub-agents com contexto proprio e retorno de resultado compacto (`aggregated-context-management.md:371`, `aggregated-context-management.md:376`, `aggregated-context-management.md:380`).
6. **Provider-limit collision**: prompts ou inputs enormes ainda quebram mesmo com estrategia de contexto. Causa: clientes pedem analise de system prompts, mensagens, historico e traces completos. Mitigacao: particionar trabalho em sub-agents e reduzir o que retorna ao main agent (`aggregated-context-management.md:408`, `aggregated-context-management.md:411`, `aggregated-context-management.md:421`).
7. **Context heuristic blind spot**: first-100/last-100 funciona ate a distribuicao do payload mudar. Causa: ausencia de budget principiado e metricas claras de context quality. Mitigacao: evals como proxy, pesquisa de metricas e revisao periodica da heuristica (`aggregated-context-management.md:462`, `aggregated-context-management.md:468`, `aggregated-context-management.md:470`).
8. **Conversation memory mistaken for long-term memory**: recuperar meio omitido dentro de uma sessao nao resolve referencias entre chats. Causa: memoria de truncagem e memoria persistente tem objetivos diferentes. Mitigacao: adicionar long-term memory separada da memory store de contexto (`aggregated-context-management.md:447`, `aggregated-context-management.md:452`, `aggregated-context-management.md:459`).

---

## 6. Synthesis

O principio unificador e que contexto deve ser tratado como uma arquitetura de alocacao de atencao, nao como um buffer de tokens. A conversa principal, a memoria externa, os sub-agents e os evals formam um sistema unico para decidir onde cada informacao vive, quando ela entra no prompt e como descobrir que a decisao falhou.

A contribuicao mais forte da fonte nao e o detalhe first-100/last-100, que a propria Arize reconhece como heuristico. A contribuicao e a composicao: manter ancoras no contexto ativo, tornar bulk recuperavel por ID e preview, testar degradacao no turno seguinte e mover tarefas data-intensive para agentes com janelas separadas. Essa composicao transforma context management de uma funcao utilitaria em uma propriedade do harness.

Tres insights cross-cutting emergem:

- **Contexto bom e contextual, nao maximo**: mais tokens podem piorar o produto quando competem com a informacao que deveria guiar o proximo passo.
- **Memoria util precisa ser enderecavel**: guardar o meio omitido so ajuda se o agente tiver IDs, localizacao e previews suficientes para decidir o que recuperar.
- **Sessoes longas sao teste de produto**: quanto mais util o agente fica, mais tempo usuarios permanecem na conversa, e mais cedo a arquitetura de contexto vira o limitador real.
