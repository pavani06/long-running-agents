# 📈 Case Study 2: KODA Scale-Up — De 100 para 10.000 Conversas por Dia
## Como a Arquitetura Multi-Agent, Compaction e Coordenação Baseada em Arquivos Transformaram um Protótipo Frágil em uma Plataforma de Produção Resiliente

**Tempo Estimado:** 120 minutos
**Nível:** 4 — KODA-Específico
**Pré-requisitos:** Ter completado Nível 1 (Fundamentos), Nível 2 (Padrões Práticos) e Nível 3 (Arquitetura Avançada)
**Status:** 🟢 COMPLETO — Estudo de caso de escala real
**Data de Criação:** Maio 2026
**Dependências:** Módulos Nível 4 — 01 a 05 (`01-koda-architecture.md`, `02-customer-journey-flows.md`, `03-feature-design-patterns.md`, `04-evaluation-rubrics-koda.md`, `05-harness-improvements.md`)

---

## 📖 Prólogo: A Segunda-Feira Que Mudou Tudo

**Segunda-feira, 08h47. O escritório da KODA estava mais silencioso que o normal.**

Fernando chegou cedo. Mais cedo que o habitual. Na noite anterior, ele tinha recebido uma mensagem do CEO que o deixou inquieto:

> *"Fernando, o time de marketing quer lançar a campanha nacional na sexta-feira. Projeção: 4.000 novos clientes nos primeiros 7 dias. O KODA aguenta?"*

Fernando leu a mensagem três vezes.

O KODA estava funcionando bem — para os padrões atuais. Lidava com cerca de **100 conversas por dia**, com uma equipe pequena monitorando. O sistema tinha seus momentos de brilhantismo e seus momentos de frustração, mas no geral... funcionava.

Mas 4.000 novos clientes em 7 dias? Isso significaria, potencialmente, **10.000 conversas por dia**. Um fator de 100x.

**100x.**

Fernando fechou os olhos e visualizou o cenário:

```
Sexta-feira, 09h00. Campanha vai ao ar.

09h01 — 50 mensagens simultâneas no WhatsApp
09h05 — 200 mensagens. O KODA começa a responder.
09h15 — 500 mensagens. O sistema ainda está respondendo, mas...
09h30 — 1.200 mensagens. A latência sobe. Algumas respostas demoram 30 segundos.
10h00 — 2.800 mensagens. O banco de dados de estado começa a ter conflitos.
11h00 — 4.200 mensagens. Três conversas travam completamente. Agentes entram em loop.
12h00 — 5.800 mensagens. O sistema de monitoramento mostra 23% de erro.
14h00 — Clientes reclamam publicamente no Twitter: "KODA não responde", "pedido sumiu".
18h00 — CEO chama Fernando para uma reunião de emergência.
```

Fernando abriu os olhos. Aquilo não podia acontecer.

Ele pegou o quadro branco e escreveu uma única frase:

> **"Como escalar KODA de 100 para 10.000 conversas/dia sem perder qualidade, confiabilidade e sanidade da equipe?"**

Essa é a história de como eles conseguiram.

---

### O Que Estava em Jogo

Antes de mergulhar na solução, é importante entender o que significava "escalar" para a KODA. Não era apenas "colocar mais servidores". Era sobre:

1. **Qualidade:** Cada conversa precisava manter a mesma qualidade de recomendação, independentemente do volume. Um erro em 100 conversas/dia = 1 cliente insatisfeito. Um erro em 10.000 conversas/dia = 100 clientes insatisfeitos.

2. **Latência:** Clientes no WhatsApp esperam respostas em segundos, não minutos. A 100 conversas/dia, havia margem. A 10.000/dia, cada milissegundo importava.

3. **Consistência de Estado:** Cada conversa do KODA gerenciava estado — dados do cliente, carrinho, preferências, histórico. Com 100 conversas, era gerenciável. Com 10.000, o volume de state files se tornaria um problema de I/O.

4. **Custo:** Cada chamada de API custava dinheiro. Escalar 100x poderia significar custo 100x — a menos que a arquitetura fosse inteligente sobre quando e como chamar o modelo.

5. **Operação:** A equipe não podia escalar 100x. Monitoramento manual de 100 conversas era possível. Monitoramento de 10.000 exigia automação total.

**Este case study documenta a jornada completa — os erros, as descobertas, as decisões arquiteturais e as lições que você pode aplicar aos seus próprios sistemas.**

---

### Conexão com os Módulos Anteriores

Este case study assume que você já domina:

- **Nível 1:** Os 3 problemas fundamentais (Context Amnesia, Planning Collapse, Self-Evaluation) de `01-why-agents-lose-plot.md`
- **Nível 2:** Generator/Evaluator (`01-generator-evaluator-pattern.md`), Sprint Contracts (`02-sprint-contracts.md`), Trace Reading (`04-trace-reading.md`)
- **Nível 3:** Multi-Agent Systems (`01-multi-agent-systems.md`), State Persistence (`02-state-persistence.md`), File-Based Coordination (`03-file-based-coordination.md`), Server-Side Compaction (`04-server-side-compaction.md`)
- **Nível 4:** Arquitetura KODA (`01-koda-architecture.md`), Customer Journeys (`02-customer-journey-flows.md`), Feature Patterns (`03-feature-design-patterns.md`), Harness Improvements (`05-harness-improvements.md`)

Se você ainda não domina esses conceitos, este case study fará menos sentido. Recomendamos voltar aos módulos relevantes antes de continuar.

---

### O Que Você Vai Aprender Neste Case Study

✅ Como identificar gargalos de escala ANTES que eles quebrem o sistema
✅ Como evoluir de um agente monolítico para uma arquitetura multi-agent distribuída
✅ Como implementar compaction inteligente para reduzir custo de API em 60%+
✅ Como usar coordenação baseada em arquivos para orquestrar dezenas de agentes simultâneos
✅ Como projetar métricas de escala que preveem problemas antes dos clientes sentirem
✅ Como pensar em escala desde o dia 1 — mesmo que você só tenha 100 conversas/dia

---

## 🔍 Seção 1: Contexto do Desafio de Escala

### 1.1 O Ponto de Partida: KODA v1.0 (Março 2026)

O KODA nasceu como um agente único. Era elegante na sua simplicidade:

```
┌──────────────────────────────────────────────────────┐
│                    KODA v1.0                          │
│                                                       │
│  ┌─────────┐     ┌──────────┐     ┌──────────────┐  │
│  │WhatsApp │────▶│  KODA    │────▶│   Cliente    │  │
│  │ Message │     │  Agent   │     │   Resposta    │  │
│  └─────────┘     └────┬─────┘     └──────────────┘  │
│                        │                              │
│                        ▼                              │
│               ┌────────────────┐                      │
│               │  State Files   │                      │
│               │  (JSON local)  │                      │
│               └────────────────┘                      │
│                                                       │
│  Capacidade: ~100 conversas/dia                       │
│  Agentes: 1 por conversa                              │
│  Coordenação: Nenhuma (monolítico)                    │
│  Latência Média: 2-5 segundos                         │
│  Taxa de Erro: ~5%                                    │
│  Custo/Conversa: ~$0.30                               │
└──────────────────────────────────────────────────────┘
```

**O que funcionava bem:**

- **Simplicidade:** Um agente, uma responsabilidade. Fácil de entender, fácil de debugar.
- **Latência baixa para volume baixo:** Com 100 conversas/dia, as chamadas de API eram sequenciais e raramente competiam por recursos.
- **State simples:** Cada conversa gerava um arquivo JSON (`state/customer_123.json`) com o histórico e contexto. Funcionava para 100 arquivos.
- **Custo previsível:** $0.30/conversa × 100 conversas = $30/dia = $900/mês. Sustentável.

**O que já mostrava sinais de alerta:**

- **Picos de latência:** Quando 5+ conversas aconteciam simultaneamente, o sistema começava a engasgar. O agente único tinha que processar cada uma sequencialmente.
- **State file corruption:** Com múltiplas conversas do mesmo cliente (ex: cliente abandona carrinho e volta depois), o arquivo de estado às vezes era sobrescrito com dados parciais.
- **Zero auditabilidade:** Quando algo dava errado, a única forma de debugar era ler o log bruto. Não havia trace files, não havia separation of concerns.
- **Escalabilidade zero:** Para aumentar capacidade, era preciso duplicar toda a stack. Não havia como escalar componentes individuais.

Fernando documentou esses problemas em março e começou a planejar a v2.0. Mas a campanha de marketing acelerou tudo.

---

### 1.2 O Gatilho: A Campanha Nacional

**Contexto de negócio:**

A KODA tinha fechado uma parceria com uma rede de academias. A campanha ofereceria:
- 20% de desconto na primeira compra via KODA
- Recomendação personalizada de suplementos
- Entrega same-day em São Paulo

**Projeções do time de marketing:**

```
Dia 1 (Sexta-feira):   2.000 - 3.000 novos clientes
Dia 2 (Sábado):        3.000 - 5.000 novos clientes
Dia 3 (Domingo):       2.000 - 3.000 novos clientes
Dia 4-7 (Seg-Qui):     1.000 - 2.000/dia

Total projetado: 8.000 - 15.000 novos clientes na primeira semana
```

**Tradução para carga do sistema:**

Cada novo cliente gera, em média:
- 1 conversa de descoberta (15-30 minutos, 20-40 mensagens)
- 1 conversa de recomendação (5-15 minutos, 10-20 mensagens)
- 1 conversa de fechamento/pedido (5-10 minutos, 5-15 mensagens)
- Possíveis follow-ups (suporte pós-venda, tracking de entrega)

**Total estimado por cliente:** 2-4 interações com o KODA, ~35-75 mensagens.

**Carga diária projetada:**

```
Cenário Conservador (8.000 clientes):
  Dia 1: 2.000 clientes × 2.5 interações = 5.000 conversas/dia
  Dia 2: 3.000 clientes × 2.5 interações = 7.500 conversas/dia
  Pico: ~7.500 conversas/dia

Cenário Agressivo (15.000 clientes):
  Dia 1: 3.000 clientes × 3 interações = 9.000 conversas/dia
  Dia 2: 5.000 clientes × 3 interações = 15.000 conversas/dia
  Pico: ~15.000 conversas/dia
```

**O gap:**
- Capacidade atual: **100 conversas/dia**
- Necessidade projetada: **5.000 - 15.000 conversas/dia**
- **Gap: 50x a 150x**

Isso não era um problema de "adicionar mais servidores". Era um problema de **rearquitetura fundamental**.

---

### 1.3 O Diagnóstico Inicial: Por Que o KODA v1.0 Não Escalava

Fernando reuniu o time técnico para uma sessão de diagnóstico. Em 4 horas, eles mapearam **7 gargalos críticos**:

#### Gargalo #1: Agente Monolítico (CPU-Bound)

```
┌─────────────────────────────────────────────┐
│         KODA v1.0 - Single Agent             │
│                                               │
│  Cada conversa = 1 agente dedicado            │
│  Agente processa TUDO sequencialmente:        │
│                                               │
│  Receber msg → Entender intenção →            │
│  Buscar produtos → Avaliar contexto →         │
│  Gerar resposta → Validar resposta →          │
│  Enviar ao cliente                            │
│                                               │
│  Tudo no mesmo contexto, mesma chamada.       │
│  Sem paralelismo. Sem especialização.         │
└─────────────────────────────────────────────┘
```

**Problema:** O agente único era CPU-bound no modelo de linguagem. Cada mensagem exigia uma chamada completa ao LLM, que processava o histórico inteiro da conversa + busca de produtos + geração de resposta. Com 10.000 conversas/dia, isso significaria potencialmente **100.000+ chamadas de API/dia**, cada uma processando contextos cada vez maiores.

#### Gargalo #2: Context Window Explosion

```
Crescimento de Contexto por Conversa (tokens):

Minuto 0:   500 tokens (system prompt + contexto inicial)
Minuto 5:   2.000 tokens (+ primeiras interações)
Minuto 15:  8.000 tokens (+ descoberta de necessidades)
Minuto 30:  18.000 tokens (+ recomendação + objeções)
Minuto 45:  35.000 tokens (+ negociação + fechamento)
Minuto 60:  55.000 tokens (+ pós-venda + follow-up)

Custo por chamada (Claude Opus, ~$15/1M tokens input):
  Minuto 0:  $0.008
  Minuto 60: $0.83  (103x mais caro!)
```

**Problema:** O custo por conversa não era linear — era exponencial em relação ao tempo. Conversas longas custavam 100x mais que conversas curtas, embora o valor de negócio fosse similar.

#### Gargalo #3: I/O de State Files

```
Com 100 conversas/dia:
  state/customer_001.json
  state/customer_002.json
  ...
  state/customer_100.json

Total: ~100 arquivos. Tempo de acesso: <1ms por arquivo.
I/O total: ~100 leituras/escritas por dia.

Com 10.000 conversas/dia:
  state/customer_0001.json
  state/customer_0002.json
  ...
  state/customer_9999.json

Total: ~10.000 arquivos. Tempo de acesso: 5-15ms por arquivo (com contenção).
I/O total: ~50.000 leituras/escritas por dia.
```

**Problema:** O sistema de arquivos não foi projetado para 10.000 pequenas leituras/escritas concorrentes. Mesmo com SSD, a contenção de I/O começaria a degradar performance quando múltiplos agentes tentassem ler/escrever o mesmo diretório simultaneamente.

#### Gargalo #4: Ausência de Fila e Priorização

No KODA v1.0, todas as mensagens eram tratadas com a mesma prioridade:

```
Mensagem "Oi, quero comprar" → mesma prioridade que "Qual o horário de funcionamento?"
```

**Problema:** Sem um sistema de filas com priorização, mensagens de alto valor (intenção de compra) competiam com mensagens de baixo valor (dúvidas simples). Em alto volume, isso significava que clientes prontos para comprar podiam esperar atrás de clientes tirando dúvidas triviais.

#### Gargalo #5: Sem Separação de Responsabilidades

```
KODA v1.0 - Todas as responsabilidades em um agente:

┌─────────────────────────────────────────────┐
│                AGENTE ÚNICO                  │
│                                               │
│  🧠 Entender intenção do cliente              │
│  🔍 Buscar produtos no catálogo               │
│  ⚖️  Avaliar restrições (alergia, orçamento)  │
│  💰 Calcular preço com descontos              │
│  ✅ Validar se recomendação é segura          │
│  📝 Gerar resposta em português natural       │
│  📊 Atualizar estado da conversa              │
│  🔄 Lidar com objeções e follow-ups           │
└─────────────────────────────────────────────┘
```

**Problema:** Um agente fazendo tudo significa que qualquer erro em qualquer etapa contamina todo o fluxo. Além disso, é impossível otimizar partes individuais do pipeline independentemente.

#### Gargalo #6: Ausência de Compaction

O KODA v1.0 enviava o **histórico completo da conversa** em cada chamada ao LLM:

```
Chamada #1:  [system prompt] + [msg1]
Chamada #2:  [system prompt] + [msg1, msg2]
Chamada #3:  [system prompt] + [msg1, msg2, msg3]
...
Chamada #50: [system prompt] + [msg1, msg2, ..., msg50]
```

**Problema:** O custo e a latência cresciam linearmente com o tamanho da conversa. Para 10.000 conversas/dia, muitas das quais durariam 30-60 minutos, o custo acumulado seria proibitivo.

#### Gargalo #7: Monitoramento Manual

A equipe monitorava o KODA manualmente:
- Um operador olhava o dashboard a cada 30 minutos
- Se visse algo estranho, investigava manualmente
- Não havia alertas automáticos
- Não havia métricas de escala (apenas "está funcionando" ou "não está")

**Problema:** Com 10.000 conversas/dia, monitoramento manual seria impossível. A equipe precisava de um sistema de observabilidade que escalasse automaticamente.

---

### 1.4 O Framework de Decisão: O Que Mudar, O Que Manter

Antes de sair redesenhando tudo, Fernando estabeleceu um framework de decisão:

| Componente | Manter? | Motivo |
|---|---|---|
| WhatsApp Business API | ✅ Sim | Interface estável, não era o gargalo |
| Catálogo de Produtos (MongoDB) | ✅ Sim | Consultas rápidas, índices adequados |
| Sistema de Pagamento | ✅ Sim | Terceirizado, escala independentemente |
| Agente Único | ❌ Não | Gargalo #1, #5 |
| State Files (JSON local) | ⚠️ Parcial | Gargalo #3, mas conceito de state é correto |
| Estrutura de Prompt | ⚠️ Parcial | Gargalo #2, #6 |
| Sistema de Monitoramento | ❌ Não | Gargalo #7 |
| Sem Fila/Priorização | ❌ Não | Gargalo #4 |

**Decisão estratégica:** Não reescrever do zero. Evoluir a arquitetura incrementalmente, mantendo o que funciona e redesenhando apenas os componentes gargalos.

---

## 🔧 Seção 2: Abordagem Inicial e Gargalos Encontrados

### 2.1 A Primeira Tentativa: Escala Horizontal Ingênua

O primeiro instinto da equipe foi o mais óbvio: **"Vamos apenas rodar mais instâncias do KODA."**

```
Arquitetura Tentativa #1 — Escala Horizontal Ingênua:

┌──────────────────────────────────────────────────────┐
│                     Load Balancer                     │
│                                                       │
│         ┌─────────┬─────────┬─────────┐              │
│         │         │         │         │              │
│    ┌────▼───┐ ┌──▼─────┐ ┌─▼──────┐ ┌▼────────┐    │
│    │ KODA   │ │ KODA   │ │ KODA   │ │ KODA    │    │
│    │ Inst 1 │ │ Inst 2 │ │ Inst 3 │ │ Inst N  │    │
│    └────┬───┘ └──┬─────┘ └─┬──────┘ └┬────────┘    │
│         │        │         │         │              │
│         └────────┼─────────┼─────────┘              │
│                  │         │                         │
│          ┌───────▼─────────▼───────┐                │
│          │   State Files (NFS)     │                │
│          │   /mnt/shared/state/    │                │
│          └─────────────────────────┘                │
└──────────────────────────────────────────────────────┘
```

**O que aconteceu na prática:**

A equipe subiu 10 instâncias do KODA em máquinas diferentes, todas apontando para um NFS compartilhado para os state files. O resultado foi... **catastrófico**.

```
Dia 1 do Teste de Carga (500 conversas simultâneas):

Hora 0:  Todas as 10 instâncias sobem. Tudo parece normal.
Hora 1:  Primeiros sinais de latência. Respostas demoram 8-12 segundos.
Hora 2:  State corruption detectado. Duas instâncias leram o mesmo
         arquivo simultaneamente e sobrescreveram com dados parciais.
Hora 3:  NFS começa a throttling. 500+ operações de I/O por segundo.
Hora 4:  Três instâncias crasham com "file lock contention".
Hora 5:  Equipe desliga o teste. 47% das conversas tiveram erro.
```

**Os 3 problemas fatais da abordagem ingênua:**

1. **Race Conditions em State Files:**
   ```
   Instância A lê customer_123.json (versão 1)
   Instância B lê customer_123.json (versão 1) — simultaneamente
   Instância A escreve customer_123.json (versão 2)
   Instância B escreve customer_123.json (versão 2') — SOBRESCREVE versão 2!
   
   Resultado: Dados da Instância A são perdidos.
   ```

2. **NFS não foi feito para alta concorrência de pequenos arquivos:**
   - NFS funciona bem para arquivos grandes e poucas operações
   - 10.000 pequenos JSONs com leitura/escrita frequente = pesadelo de metadata
   - Latência de operações de arquivo saltou de <1ms para 50-200ms

3. **Sem coordenação entre instâncias:**
   - Cada instância era independente e não sabia da existência das outras
   - Duas instâncias podiam responder à mesma mensagem do cliente
   - Não havia como garantir que um cliente sempre fosse atendido pela mesma instância (sticky session)

**Lição #1:** Escala horizontal não é mágica. Sem coordenação e isolamento de estado, mais instâncias significam mais problemas, não menos.

---

### 2.2 A Segunda Tentativa: Redis como State Store

Depois do fiasco com NFS, a equipe tentou substituir state files por Redis:

```
Arquitetura Tentativa #2 — Redis State Store:

┌──────────────────────────────────────────────────────┐
│                     Load Balancer                     │
│                                                       │
│    ┌────▼───┐ ┌──▼─────┐ ┌─▼──────┐ ┌▼────────┐    │
│    │ KODA   │ │ KODA   │ │ KODA   │ │ KODA    │    │
│    │ Inst 1 │ │ Inst 2 │ │ Inst 3 │ │ Inst N  │    │
│    └────┬───┘ └──┬─────┘ └─┬──────┘ └┬────────┘    │
│         │        │         │         │              │
│         └────────┼─────────┼─────────┘              │
│                  │                                   │
│          ┌───────▼──────────┐                        │
│          │   Redis Cluster  │                        │
│          │   (state store)  │                        │
│          └──────────────────┘                        │
└──────────────────────────────────────────────────────┘
```

**O que aconteceu:**

Redis resolveu o problema de race conditions — operações atômicas garantiam que não houvesse sobrescrita de dados. A latência de leitura/escrita caiu para <1ms consistente.

**Mas novos problemas surgiram:**

1. **Custo de Memória Explodiu:**
   ```
   Cada conversa ativa: ~50KB de estado (JSON serializado)
   10.000 conversas simultâneas: 500MB
   + Cache de produto: 200MB
   + Sessões de usuário: 100MB
   + Overhead Redis: 200MB
   
   Total Redis: ~1GB para operação normal
   Pico de campanha: ~3-5GB
   
   Custo Redis gerenciado (AWS ElastiCache): ~$200-400/mês para 5GB
   ```

2. **Estado Virou Caixa-Preta:**
   - Antes, dava para abrir `state/customer_123.json` e ver exatamente o que estava acontecendo
   - Com Redis, era preciso usar `redis-cli` e decodificar JSON manualmente
   - Debugging ficou significativamente mais difícil

3. **Sem Persistência de Longo Prazo:**
   - Redis é primariamente um cache em memória
   - Se o cluster caísse, todo o estado de conversas ativas seria perdido
   - Clientes teriam que reiniciar conversas do zero

4. **Problema de Escala do Próprio LLM:**
   - Redis resolveu o gargalo de I/O, mas não resolveu o gargalo principal: **cada instância ainda rodava um agente monolítico que processava a conversa inteira a cada chamada**
   - O custo de API continuava crescendo linearmente com o volume

**Lição #2:** Trocar a tecnologia de armazenamento resolveu um sintoma, não a causa raiz. O problema fundamental era arquitetural: **um agente fazendo tudo não escala, independentemente de onde o estado é guardado.**

---

### 2.3 A Terceira Tentativa: Agent Pooling

A terceira abordagem foi mais sofisticada: em vez de um agente por conversa, criar um pool de agentes especializados:

```
Arquitetura Tentativa #3 — Agent Pooling:

┌──────────────────────────────────────────────────────┐
│                   Message Queue                       │
│                 (Redis Pub/Sub)                       │
│                                                       │
│    ┌──────────────────────────────────────┐          │
│    │          AGENT POOL                  │          │
│    │                                      │          │
│    │  ┌────────┐ ┌────────┐ ┌────────┐  │          │
│    │  │Intent  │ │Product │ │Pricing │  │          │
│    │  │Agent 1 │ │Agent 1 │ │Agent 1 │  │          │
│    │  │Agent 2 │ │Agent 2 │ │Agent 2 │  │          │
│    │  │Agent 3 │ │ ...    │ │ ...    │  │          │
│    │  └────────┘ └────────┘ └────────┘  │          │
│    │                                      │          │
│    │  ┌────────┐ ┌────────┐ ┌────────┐  │          │
│    │  │Validat │ │Respons │ │State   │  │          │
│    │  │Agent 1 │ │Agent 1 │ │Agent 1 │  │          │
│    │  │Agent 2 │ │Agent 2 │ │Agent 2 │  │          │
│    │  └────────┘ └────────┘ └────────┘  │          │
│    └──────────────────────────────────────┘          │
└──────────────────────────────────────────────────────┘
```

**O que funcionou:**

- ✅ Especialização reduziu o tamanho do prompt de cada agente
- ✅ Paralelismo real: múltiplos agentes processavam diferentes aspectos simultaneamente
- ✅ Isolamento de falhas: se o Pricing Agent falhasse, o Intent Agent continuava funcionando

**O que quebrou:**

1. **Orquestração virou um pesadelo:**
   ```
   Fluxo de uma mensagem simples:
   
   1. Intent Agent: "É uma pergunta sobre preço"
   2. Product Agent: "Preciso saber qual produto"
   3. State Agent: "Cliente estava vendo Whey Isolado"
   4. Pricing Agent: "Preço: R$ 89,90"
   5. Validation Agent: "Preço está correto? Sim"
   6. Response Agent: "Gera resposta final"
   
   Cada etapa: 1 chamada de API.
   Total: 6 chamadas para UMA mensagem.
   Latência: 6 × 2s = 12 segundos. Inaceitável.
   ```

2. **Coordenação de contexto virou exponencial:**
   - Cada agente precisava de contexto diferente
   - Intent Agent precisava da mensagem do cliente
   - Product Agent precisava do catálogo + intenção
   - Pricing Agent precisava do produto + cliente
   - Passar contexto entre agentes gerava ainda mais chamadas de API

3. **Debugging impossível:**
   - Quando algo dava errado, eram 6 agentes para investigar
   - Qual deles errou? Em qual ordem? Com qual input?
   - A equipe passava mais tempo debugando do que desenvolvendo

**Lição #3:** Especialização sem coordenação adequada cria mais problemas do que resolve. O segredo não está em ter muitos agentes, mas em ter **o número certo de agentes com as interfaces certas**.

---

### 2.4 A Virada: Madrugada de Quinta-Feira

Depois de três tentativas fracassadas, a campanha estava a 36 horas de distância. O time estava exausto. Fernando estava considerando adiar o lançamento.

Foi quando Júlia, a engenheira mais sênior do time, chegou com um café e uma ideia:

> *"Nós estamos tentando resolver o problema errado. Não é sobre quantos agentes. Não é sobre onde guardar estado. É sobre **como o trabalho flui através do sistema**."*

Ela desenhou no quadro:

```
O PROBLEMA REAL:

KODA v1.0 processava conversas como um FUNIL:
  Entrada → Processamento → Saída
  
Mas com 10.000 conversas, isso se torna um CANO:
  ═══════════════════════════╗
  ║  10.000 conversas        ║  → Tudo passa pelo mesmo caminho
  ║  simultâneas             ║  → Gargalo em qualquer ponto
  ═══════════════════════════╝

Precisamos transformar isso em uma REDE:
  
  ┌─────┐     ┌─────┐     ┌─────┐
  │ INT │────▶│ PROD│────▶│ PRICE│
  └──┬──┘     └──┬──┘     └──┬──┘
     │            │            │
     └────────────┼────────────┘
                  │
             ┌────▼────┐
             │ EVAL    │  ← Checkpoint de qualidade
             └────┬────┘
                  │
             ┌────▼────┐
             │ RESP    │
             └─────────┘
  
  Com:
  - Cada nó é independente e escalável
  - Entre nós: filas com prioridade
  - Estado: arquivos versionados (não Redis)
  - Checkpoints: avaliação antes de avançar
```

Aquela madrugada mudou tudo. A equipe passou as próximas 30 horas implementando o que chamaram de **Arquitetura em Rede com Coordenação por Arquivos**.

---

## 🏗️ Seção 3: A Solução Multi-Agent

### 3.1 O Design Final: Arquitetura em Rede com 4 Camadas

Depois de iterar sobre o design de Júlia, a arquitetura final do KODA Scale-Up emergiu com 4 camadas:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    KODA SCALE-UP ARCHITECTURE v2.0                          │
│                    (Suporta 10.000+ conversas/dia)                          │
│                                                                              │
│  CAMADA 1: INGESTÃO & ROTEAMENTO                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                      │   │
│  │  WhatsApp ──▶ API Gateway ──▶ Message Queue ──▶ Intent Router        │   │
│  │               (rate limit)     (Redis Streams)    (classificador)    │   │
│  │                                                                      │   │
│  │  Função: Receber, autenticar, enfileirar, classificar intenção       │   │
│  │  Escala: Horizontal (N instâncias de API Gateway)                    │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                         │
│                                    ▼                                         │
│  CAMADA 2: PROCESSAMENTO (MULTI-AGENT)                                      │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                      │   │
│  │  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐        │   │
│  │  │ Planner  │──▶│Discovery │──▶│Generator │──▶│Evaluator │        │   │
│  │  │ Agent    │   │Agent     │   │Agent     │   │Agent     │        │   │
│  │  └──────────┘   └──────────┘   └──────────┘   └──────────┘        │   │
│  │       │               │               │               │             │   │
│  │       └───────────────┼───────────────┼───────────────┘             │   │
│  │                       │               │                              │   │
│  │              ┌────────▼───────────────▼────────┐                     │   │
│  │              │     COORDINATION LAYER          │                     │   │
│  │              │  (File-Based + Lock Manager)    │                     │   │
│  │              └─────────────────────────────────┘                     │   │
│  │                                                                      │   │
│  │  Cada agente é um pool de workers independentes                      │   │
│  │  Comunicação entre agentes via state files versionados               │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                         │
│                                    ▼                                         │
│  CAMADA 3: PERSISTÊNCIA & ESTADO                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                      │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │   │
│  │  │ State Store  │  │ Trace Store  │  │ Metric Store │              │   │
│  │  │ (Versioned   │  │ (Append-only │  │ (Time-series │              │   │
│  │  │  JSON Files) │  │  JSONL Logs) │  │  Database)   │              │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘              │   │
│  │                                                                      │   │
│  │  + Compaction Engine (background, assíncrono)                        │   │
│  │  + Snapshot Manager (checkpoints a cada N interações)                │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                         │
│                                    ▼                                         │
│  CAMADA 4: OBSERVABILIDADE & CONTROLE                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                      │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐           │   │
│  │  │Dashboard │  │ Alerting │  │Auto-Scale│  │Audit Log │           │   │
│  │  │(Real-time│  │(Threshold│  │(K8s HPA) │  │(Complian │           │   │
│  │  │ metrics) │  │ alerts)  │  │          │  │ ce)      │           │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘           │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 3.2 Camada 1: Ingestão e Roteamento Inteligente

**Problema resolvido:** Gargalo #4 (ausência de fila e priorização)

A Camada 1 é a porta de entrada. Toda mensagem do WhatsApp passa por três estágios:

#### Estágio 1: API Gateway com Rate Limiting

```
┌─────────────────────────────────────────┐
│            API Gateway                    │
│                                           │
│  WhatsApp Webhook ──▶ Valida assinatura   │
│                       ──▶ Rate limit check │
│                       ──▶ Enfileira msg    │
│                                           │
│  Rate Limit Config:                       │
│  - 100 msg/segundo por tenant             │
│  - 10 msg/segundo por cliente             │
│  - Burst: 200 msg/segundo (rajada)        │
│                                           │
│  Se exceder: HTTP 429 + retry-after       │
└─────────────────────────────────────────┘
```

**Por que isso importa:** Sem rate limiting, um pico de mensagens poderia derrubar todo o sistema. O API Gateway age como um "amortecedor" que protege as camadas internas.

#### Estágio 2: Message Queue (Redis Streams)

```
┌─────────────────────────────────────────────────┐
│              Redis Streams                        │
│                                                   │
│  Stream: "koda:messages"                          │
│  ┌─────────────────────────────────────────────┐ │
│  │ ID       │ Customer │ Intent    │ Priority   │ │
│  ├──────────┼──────────┼───────────┼────────────┤ │
│  │ 001-0    │ cust_123 │ purchase  │ HIGH       │ │
│  │ 001-1    │ cust_456 │ question  │ LOW        │ │
│  │ 001-2    │ cust_789 │ complaint │ CRITICAL   │ │
│  │ ...      │ ...      │ ...       │ ...        │ │
│  └─────────────────────────────────────────────┘ │
│                                                   │
│  Consumer Groups (paralelismo):                   │
│  - Group "planner": 5 consumers                   │
│  - Group "discovery": 8 consumers                 │
│  - Group "generator": 10 consumers                │
│  - Group "evaluator": 5 consumers                 │
└─────────────────────────────────────────────────┘
```

**Por que Redis Streams em vez de RabbitMQ/Kafka?**

- **Simplicidade:** Redis já estava na stack (usado para cache). Adicionar Streams não introduziu nova dependência.
- **Latência:** Redis opera em memória. Latência de enfileiramento: <1ms.
- **Consumer Groups:** Suporta múltiplos consumidores lendo da mesma stream em paralelo. A entrega é at-least-once — o consumidor deve usar o campo ID da mensagem para implementar idempotência e evitar processamento duplicado.
- **Persistência:** Streams são persistidos em disco (AOF), não apenas em memória.

#### Estágio 3: Intent Router (Classificador de Intenção)

```
┌─────────────────────────────────────────────────┐
│              Intent Router                        │
│                                                   │
│  Input: Mensagem do cliente (texto)               │
│  Output: Classificação + Prioridade               │
│                                                   │
│  ┌─────────────────────────────────────────────┐ │
│  │ Mensagem                │ Intenção  │ Prior. │ │
│  ├─────────────────────────┼───────────┼────────┤ │
│  │ "Quero comprar whey"    │ purchase  │ HIGH   │ │
│  │ "Vcs entregam hoje?"    │ question  │ MEDIUM │ │
│  │ "Meu pedido não chegou" │ complaint │ CRIT   │ │
│  │ "Obrigado, gostei!"     │ feedback  │ LOW    │ │
│  │ "Quanto custa o frete?" │ question  │ MEDIUM │ │
│  │ "Cancelar meu pedido"   │ cancel    │ CRIT   │ │
│  └─────────────────────────────────────────────┘ │
│                                                   │
│  Modelo: Claude Haiku (rápido, barato)             │
│  Latência: ~200ms                                  │
│  Custo: ~$0.0005/classificação                     │
└─────────────────────────────────────────────────┘
```

**Decisão de design importante:** O Intent Router usa um modelo **leve e barato** (Haiku, não Opus). A classificação de intenção é uma tarefa simples que não exige o modelo mais poderoso. Essa decisão economizou ~$0.01 por mensagem — o que em 10.000 conversas/dia representa **$100/dia ou $36.500/ano**.

---

### 3.3 Camada 2: Processamento Multi-Agent

**Problema resolvido:** Gargalo #1 (agente monolítico), #5 (sem separação de responsabilidades)

Esta é a camada central da arquitetura. Quatro agentes especializados trabalham em pipeline:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     PROCESSING PIPELINE                                  │
│                                                                          │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐         │
│  │ PLANNER  │───▶│DISCOVERY │───▶│GENERATOR │───▶│EVALUATOR │         │
│  │          │    │          │    │          │    │          │         │
│  │ O QUE    │    │ O QUE    │    │ COMO     │    │ ESTÁ     │         │
│  │ FAZER?   │    │ USAR?    │    │ FAZER?   │    │ CORRETO? │         │
│  └────┬─────┘    └────┬─────┘    └────┬─────┘    └────┬─────┘         │
│       │               │               │               │                │
│       ▼               ▼               ▼               ▼                │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐         │
│  │Planner   │    │Discovery │    │Generator │    │Evaluator │         │
│  │Contract  │    │Context   │    │Draft     │    │Verdict   │         │
│  │(JSON)    │    │(JSON)    │    │(JSON)    │    │(JSON)    │         │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘         │
│                                                                          │
│  Comunicação: State Files versionados + Lock Manager                     │
│  Cada agente lê o output do anterior e produz seu próprio output         │
└─────────────────────────────────────────────────────────────────────────┘
```

#### Agente 1: Planner Agent

**Responsabilidade:** Decidir O QUE fazer, não COMO fazer.

```
┌─────────────────────────────────────────────────────────────┐
│                    PLANNER AGENT                              │
│                                                               │
│  Input:                                                       │
│  - Mensagem do cliente                                        │
│  - Intenção classificada                                      │
│  - Estado atual da conversa (via state file)                  │
│  - Histórico compactado (últimas N interações relevantes)     │
│                                                               │
│  Processamento:                                               │
│  1. Analisa intenção + contexto atual                         │
│  2. Determina quais etapas são necessárias                    │
│  3. Gera um "Planner Contract" com:                           │
│     - Objetivo da interação                                   │
│     - Etapas necessárias (ordenadas)                          │
│     - Critérios de sucesso                                    │
│     - Restrições identificadas                                │
│                                                               │
│  Output: planner_contract.json                                │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ {                                                        │ │
│  │   "interaction_id": "int_45678",                         │ │
│  │   "intent": "purchase",                                  │ │
│  │   "objective": "Recomendar e vender whey protein",       │ │
│  │   "steps": [                                             │ │
│  │     "discover_preferences",                              │ │
│  │     "search_catalog",                                    │ │
│  │     "generate_recommendation",                           │ │
│  │     "validate_against_constraints"                       │ │
│  │   ],                                                     │ │
│  │   "constraints": [                                       │ │
│  │     "allergy: lactose",                                  │ │
│  │     "budget: R$ 150",                                    │ │
│  │     "delivery: same_day_sp"                              │ │
│  │   ],                                                     │ │
│  │   "success_criteria": [                                  │ │
│  │     "product_matches_dietary_restrictions",              │ │
│  │     "price_within_budget",                               │ │
│  │     "same_day_delivery_available"                        │ │
│  │   ]                                                      │ │
│  │ }                                                        │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                               │
│  Modelo: Claude Sonnet (bom equilíbrio custo/capacidade)      │
│  Pool Size: 5 workers                                         │
│  Timeout: 5 segundos                                          │
└─────────────────────────────────────────────────────────────┘
```

**Por que separar Planner?**

O Planner não gera a resposta final. Ele apenas decide **o que precisa ser feito**. Essa separação é crítica porque:

1. **Reuso:** O mesmo plano pode ser reutilizado se o cliente fizer uma pergunta similar
2. **Auditabilidade:** Se algo der errado, o primeiro lugar a olhar é o plano — ele diz o que DEVERIA ter sido feito
3. **Escalabilidade:** O Planner processa apenas a intenção, não toda a conversa. Prompt menor = mais rápido e mais barato.

#### Agente 2: Discovery Agent

**Responsabilidade:** Descobrir e organizar as informações necessárias.

```
┌─────────────────────────────────────────────────────────────┐
│                   DISCOVERY AGENT                             │
│                                                               │
│  Input:                                                       │
│  - Planner Contract                                           │
│  - Estado do cliente (state file)                             │
│  - Catálogo de produtos (query via MongoDB)                   │
│                                                               │
│  Processamento:                                               │
│  1. Lê o planner_contract.json                                │
│  2. Para cada constraint, busca informações relevantes:       │
│     - "allergy: lactose" → filtra produtos sem lactose        │
│     - "budget: R$ 150" → filtra por faixa de preço           │
│     - "delivery: same_day_sp" → verifica disponibilidade     │
│  3. Consulta catálogo (MongoDB) com filtros compostos         │
│  4. Enriquece com metadados (reviews, popularidade)           │
│  5. Organiza resultados em discovery_context.json             │
│                                                               │
│  Output: discovery_context.json                               │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ {                                                        │ │
│  │   "interaction_id": "int_45678",                         │ │
│  │   "candidate_products": [                                │ │
│  │     {                                                    │ │
│  │       "sku": "WHEY-ISO-001",                             │ │
│  │       "name": "Whey Isolado Premium",                    │ │
│  │       "price": 129.90,                                   │ │
│  │       "lactose_free": true,                              │ │
│  │       "rating": 4.8,                                     │ │
│  │       "stock_sp": 45,                                    │ │
│  │       "same_day_eligible": true                          │ │
│  │     },                                                   │ │
│  │     { ... },                                             │ │
│  │     { ... }                                              │ │
│  │   ],                                                     │ │
│  │   "applied_filters": [                                   │ │
│  │     "lactose_free",                                      │ │
│  │     "price_max_150",                                     │ │
│  │     "delivery_same_day_sp"                               │ │
│  │   ],                                                     │ │
│  │   "catalog_query_time_ms": 45                            │ │
│  │ }                                                        │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                               │
│  Modelo: N/A (usa MongoDB queries, não LLM para busca)        │
│  Pool Size: 8 workers                                         │
│  Timeout: 2 segundos                                          │
└─────────────────────────────────────────────────────────────┘
```

**Decisão de design importante:** O Discovery Agent **não usa LLM para buscar produtos**. Ele usa queries parametrizadas no MongoDB. O LLM seria desnecessariamente caro e lento para uma tarefa que é essencialmente uma busca em banco de dados. O agente apenas formata os resultados de forma estruturada.

#### Agente 3: Generator Agent

**Responsabilidade:** Gerar a recomendação final.

```
┌─────────────────────────────────────────────────────────────┐
│                    GENERATOR AGENT                            │
│                                                               │
│  Input:                                                       │
│  - Planner Contract (o que fazer)                             │
│  - Discovery Context (com quais produtos)                     │
│  - Histórico compactado da conversa                           │
│                                                               │
│  Processamento:                                               │
│  1. Analisa os produtos candidatos                            │
│  2. Aplica lógica de recomendação:                            │
│     - Melhor custo-benefício dentro do orçamento              │
│     - Compatibilidade com restrições                          │
│     - Preferências implícitas do cliente                      │
│  3. Gera explicação personalizada em português natural        │
│  4. Estrutura a resposta com:                                 │
│     - Produto recomendado (nome, preço, link)                 │
│     - Por que esse produto (justificativa)                    │
│     - Alternativas (opção B e C)                              │
│     - Call to action (comprar, tirar dúvida)                  │
│                                                               │
│  Output: generator_draft.json                                 │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ {                                                        │ │
│  │   "interaction_id": "int_45678",                         │ │
│  │   "primary_recommendation": {                            │ │
│  │     "sku": "WHEY-ISO-001",                               │ │
│  │     "reason": "Melhor custo-benefício sem lactose",      │ │
│  │     "price": 129.90,                                     │ │
│  │     "response_text": "Recomendo o Whey Isolado..."       │ │
│  │   },                                                     │ │
│  │   "alternatives": [                                      │ │
│  │     { "sku": "...", "reason": "..." },                   │ │
│  │     { "sku": "...", "reason": "..." }                    │ │
│  │   ],                                                     │ │
│  │   "generation_metadata": {                               │ │
│  │     "model": "claude-sonnet-4-20250514",                 │ │
│  │     "tokens_used": 1250,                                 │ │
│  │     "latency_ms": 1800                                   │ │
│  │   }                                                      │ │
│  │ }                                                        │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                               │
│  Modelo: Claude Sonnet (para qualidade)                       │
│  Pool Size: 10 workers (o mais demandado)                     │
│  Timeout: 8 segundos                                          │
└─────────────────────────────────────────────────────────────┘
```

#### Agente 4: Evaluator Agent

**Responsabilidade:** Validar se a recomendação atende aos critérios.

```
┌─────────────────────────────────────────────────────────────┐
│                    EVALUATOR AGENT                            │
│                                                               │
│  Input:                                                       │
│  - Planner Contract (critérios de sucesso)                    │
│  - Generator Draft (recomendação gerada)                      │
│  - Discovery Context (produtos disponíveis)                   │
│  - Constraints do cliente                                     │
│                                                               │
│  Processamento:                                               │
│  1. Verifica CADA critério de sucesso:                        │
│     ☐ product_matches_dietary_restrictions?                   │
│     ☐ price_within_budget?                                    │
│     ☐ same_day_delivery_available?                            │
│     ☐ response_is_polite_and_clear?                           │
│     ☐ no_hallucinated_products?                               │
│     ☐ price_matches_catalog?                                  │
│  2. Para cada critério: ✅ APROVADO ou ❌ REPROVADO           │
│  3. Se REPROVADO: gera feedback específico                    │
│  4. Decide: APPROVE (enviar ao cliente) ou REJECT (retornar)  │
│                                                               │
│  Output: evaluator_verdict.json                               │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ {                                                        │ │
│  │   "interaction_id": "int_45678",                         │ │
│  │   "verdict": "APPROVE",                                  │ │
│  │   "checks": [                                            │ │
│  │     {"criterion": "dietary", "result": "PASS",           │ │
│  │      "detail": "WHEY-ISO-001: lactose_free=true"},       │ │
│  │     {"criterion": "budget", "result": "PASS",            │ │
│  │      "detail": "R$129.90 ≤ R$150"},                      │ │
│  │     {"criterion": "delivery", "result": "PASS",          │ │
│  │      "detail": "Same-day disponível em SP"},             │ │
│  │     {"criterion": "no_hallucination", "result": "PASS",  │ │
│  │      "detail": "SKU existe no catálogo"},                │ │
│  │     {"criterion": "price_accuracy", "result": "PASS",    │ │
│  │      "detail": "R$129.90 confere com catálogo"},         │ │
│  │     {"criterion": "tone", "result": "PASS",              │ │
│  │      "detail": "Tom educado e claro"}                    │ │
│  │   ],                                                     │ │
│  │   "approval_confidence": 0.97                            │ │
│  │ }                                                        │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                               │
│  Modelo: Claude Haiku (barato, suficiente para verificação)   │
│  Pool Size: 5 workers                                         │
│  Timeout: 5 segundos                                          │
└─────────────────────────────────────────────────────────────┘
```

**Decisão de design importante:** O Evaluator usa **Haiku, não Sonnet ou Opus**. Verificação é uma tarefa mais simples que geração. Usar um modelo mais barato para avaliação reduz o custo total do pipeline sem sacrificar qualidade.

---

### 3.4 O Fluxo Completo com Métricas

```
TEMPO E CUSTO POR INTERAÇÃO (Pipeline Completo):

Etapa           Agente      Modelo    Tokens    Latência    Custo
─────────────────────────────────────────────────────────────────
1. Intent       Router      Haiku      150      200ms      $0.0002
2. Planning     Planner     Sonnet     800     1.200ms     $0.0032
3. Discovery    (MongoDB)   N/A         0       45ms       $0.0000
4. Generation   Generator   Sonnet    1.250    1.800ms     $0.0050
5. Evaluation   Evaluator   Haiku      400      600ms      $0.0006
6. Response     (template)  N/A         0       10ms       $0.0000
─────────────────────────────────────────────────────────────────
TOTAL:                               2.600    3.855ms     $0.0090

Comparação com v1.0 (agente único):
  v1.0: ~3.500 tokens, 4.500ms, $0.0525/interação
  v2.0: ~2.600 tokens, 3.855ms, $0.0090/interação
  
  Economia: -26% tokens, -14% latência, -83% custo
```

**Como isso escala para 10.000 conversas/dia:**

```
10.000 conversas/dia × ~30 interações/conversa (média de 60 min) = 300.000 interações/dia

Comparação de custo (sem considerar compaction adicional):
  v1.0: 300.000 × $0.0525 = $15.750/dia = $472.500/mês ❌
  v2.0: 300.000 × $0.0090 =  $2.700/dia =  $81.000/mês  ✅
  (Economia apenas da decomposição multi-agent + modelo certo: ~83%)

Comparação de custo (COM compaction, custo real observado):
  v1.0: 10.000 conversas × $0.629/conversa = $6.290/dia
  v2.0: 10.000 conversas × $0.096/conversa =   $960/dia
  (Economia combinada: multi-agent + compaction = ~85%)

---

### 3.5 Coordenação: File-Based com Lock Manager

**Problema resolvido:** Gargalo #3 (I/O de state files), race conditions

A coordenação entre agentes usa um sistema de **arquivos versionados com lock manager**. Esta foi uma das decisões mais controversas e, no fim, uma das mais acertadas.

#### Por que arquivos, não Redis?

| Critério | Redis | File-Based |
|---|---|---|
| Race conditions | Resolve com WATCH/MULTI | Resolve com lock files |
| Debugabilidade | Ruim (CLI + decode) | Excelente (`cat file.json \\| jq`) |
| Persistência | Frágil (em memória) | Natural (em disco) |
| Versionamento | Manual | Nativo (git ou timestamp) |
| Custo operacional | Alto (cluster gerenciado) | Baixo (disco local) |
| Auditoria | Complexa | Trivial (append-only logs) |
| Escala de leitura | Excelente | Boa com caching |
| Escala de escrita | Boa com sharding | Moderada (lock contention) |

**A decisão:** File-based com locks otimistas para leitura e locks exclusivos para escrita.

#### Estrutura de Diretórios Versionada

```
/var/koda/state/
├── conversations/
│   ├── cust_001/
│   │   ├── v0001_2026-05-20T08-00-00Z.json
│   │   ├── v0002_2026-05-20T08-05-00Z.json
│   │   ├── v0003_2026-05-20T08-12-00Z.json
│   │   ├── current -> v0003_2026-05-20T08-12-00Z.json  (symlink)
│   │   └── lock (arquivo de lock)
│   ├── cust_002/
│   └── ...
├── interactions/
│   ├── int_45678/
│   │   ├── planner_contract.json
│   │   ├── discovery_context.json
│   │   ├── generator_draft.json
│   │   ├── evaluator_verdict.json
│   │   └── final_response.json
│   └── ...
├── traces/
│   └── 2026-05-20.jsonl  (append-only log)
└── snapshots/
    └── daily_2026-05-20.tar.gz
```

#### Protocolo de Lock

```
OPERAÇÃO DE LEITURA (qualquer agente):

1. Verificar se lock existe
2. Se NÃO: ler current → symlink
3. Copiar versão para memória (snapshot local)
4. Processar com snapshot local (sem lock)
5. Se SIM (outro agente escrevendo): esperar 100ms, retentar (max 5x)

OPERAÇÃO DE ESCRITA (qualquer agente):

1. Criar arquivo .lock (operacão atômica: open O_CREAT|O_EXCL)
2. Se falhar: lock já existe → esperar 200ms, retentar (max 3x)
3. Se sucesso: ler current, modificar, escrever nova versão
4. Atualizar symlink current → nova versão
5. Remover arquivo .lock
6. Se crash: lock é removido por watchdog após 30s de timeout
```

**Por que locks no sistema de arquivos, não Redis?**
- Atomicidade nativa: `open()` com `O_CREAT|O_EXCL` é atômico no Linux
- Para coordenação entre múltiplos workers: os state files residem em um volume compartilhado (NFS ou EFS) — a mesma preocupação de I/O da tentativa inicial, mas mitigada pelo fato de que cada conversa tem seu próprio subdiretório, drasticamente reduzindo contenção comparado a um diretório único com milhares de arquivos
- Sem dependência externa adicional: não requer Redis ou PostgreSQL apenas para coordenação
- Simplicidade: `ls -la` mostra se há lock; `rm lock` resolve manualmente

---

## 🗜️ Seção 4: A Solução de Compaction

### 4.1 O Problema: Contexto Cresce, Custo Explode

Mesmo com a arquitetura multi-agent, havia um problema residual: **cada agente ainda precisava de contexto para funcionar**. O Generator Agent, por exemplo, precisava saber:
- O que o cliente disse nos últimos 15 minutos
- Quais preferências foram mencionadas
- Quais produtos já foram discutidos
- Qual é o tom da conversa

Sem compaction, o contexto enviado ao LLM crescia linearmente:

```
Tamanho do Contexto por Interação (sem compaction):

Interação #1:  1.500 tokens (system prompt + msg atual)
Interação #5:  4.200 tokens
Interação #10: 8.900 tokens
Interação #15: 14.500 tokens
Interação #20: 21.000 tokens
Interação #30: 35.000 tokens ← começa a degradar qualidade
Interação #50: 62.000 tokens ← custo proibitivo
```

### 4.2 A Solução: Compaction Inteligente em 3 Níveis

A equipe implementou um sistema de compaction que opera em 3 níveis:

```
┌──────────────────────────────────────────────────────────────┐
│                  COMPACTION ENGINE                             │
│                                                                │
│  NÍVEL 1: Compaction por Interação (online, síncrono)          │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │ Após cada resposta ao cliente:                            │ │
│  │ - Resume a interação em 1-2 frases                        │ │
│  │ - Extrai fatos importantes (preferências, decisões)       │ │
│  │ - Descarta o texto verbatim                                │ │
│  │                                                            │ │
│  │ Exemplo:                                                   │ │
│  │   Original (850 tokens):                                   │ │
│  │   "Cliente: Eu queria algo sem lactose... mas também      │ │
│  │    não muito caro... ah, e de preferência de chocolate... │ │
│  │    mas se tiver de baunilha também serve..."               │ │
│  │                                                            │ │
│  │   Compaction (45 tokens):                                  │ │
│  │   "Cliente busca proteína sem lactose, sabor chocolate    │ │
│  │    ou baunilha, orçamento até R$150, prefere entrega       │ │
│  │    same-day em SP."                                        │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                │
│  NÍVEL 2: Compaction por Conversa (background, a cada 10 min)  │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │ A cada 10 interações ou 10 minutos (o que vier primeiro): │ │
│  │ - Resume TODA a conversa até agora                        │ │
│  │ - Cria "conversation_summary.json"                        │ │
│  │ - Estrutura:                                               │ │
│  │   {                                                        │ │
│  │     "customer_profile": {...},                             │ │
│  │     "key_decisions": [...],                                │ │
│  │     "open_questions": [...],                               │ │
│  │     "timeline": [...]                                      │ │
│  │   }                                                        │ │
│  │ - Agentes leem o summary, não o histórico completo        │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                │
│  NÍVEL 3: Compaction Cross-Conversa (batch, diário)            │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │ Diariamente à 03:00 UTC:                                   │ │
│  │ - Consolida TODAS as conversas de um cliente               │ │
│  │ - Cria "customer_360_profile.json"                         │ │
│  │ - Inclui:                                                  │ │
│  │   - Histórico de compras                                   │ │
│  │   - Preferências recorrentes                               │ │
│  │   - Restrições permanentes (alergias)                      │ │
│  │   - Padrões de comportamento                               │ │
│  │ - Usado para personalização em conversas futuras           │ │
│  └──────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```

### 4.3 Algoritmo de Compaction: Sliding Window com Summarization

O algoritmo de compaction do KODA usa uma **janela deslizante com sumarização progressiva**:

```
┌─────────────────────────────────────────────────────────────┐
│           SLIDING WINDOW COMPACTION ALGORITHM                │
│                                                               │
│  Janela Completa (últimas 5 interações):                      │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ [Int N-4] [Int N-3] [Int N-2] [Int N-1] [Int N]        │ │
│  │  VERBATIM  VERBATIM  VERBATIM  VERBATIM  VERBATIM       │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                               │
│  Zona de Sumarização (interações 6-20):                       │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ "Cliente demonstrou interesse em whey e creatina.        │ │
│  │  Discutiu 5 produtos, eliminou 2 por preço.              │ │
│  │  Decidiu comprar whey isolado sabor chocolate.           │ │
│  │  Perguntou sobre frete e prazo de entrega."              │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                               │
│  Zona de Arquivo (interações 21+):                            │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ FATOS EXTRAÍDOS:                                          │ │
│  │ - Alergia: lactose, glúten                                │ │
│  │ - Orçamento: R$ 150-200                                   │ │
│  │ - Preferência: chocolate                                   │ │
│  │ - Objetivo: ganho de massa muscular                       │ │
│  │ - Já comprou: WHEY-ISO-001 (22/05/2026)                   │ │
│  │ - Próxima compra prevista: 30 dias                        │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### 4.4 Impacto do Compaction nas Métricas

```
ANTES DO COMPACTION (Conversa de 60 minutos, 30 interações):

Interação │ Contexto (tokens) │ Custo API │ Latência
──────────┼───────────────────┼───────────┼──────────
    #1    │      1.500        │  $0.006   │  1.2s
    #5    │      4.200        │  $0.017   │  1.8s
   #10    │     10.500        │  $0.042   │  2.5s
   #15    │     18.000        │  $0.072   │  3.2s
   #20    │     28.000        │  $0.112   │  4.1s
   #25    │     40.000        │  $0.160   │  5.5s
   #30    │     55.000        │  $0.220   │  7.2s
──────────┼───────────────────┼───────────┼──────────
TOTAL     │   157.200 tokens  │  $0.629   │  (média 3.6s)


DEPOIS DO COMPACTION (Mesma conversa, 30 interações):

Interação │ Contexto (tokens) │ Custo API │ Latência
──────────┼───────────────────┼───────────┼──────────
    #1    │      1.500        │  $0.006   │  1.2s
    #5    │      2.800        │  $0.011   │  1.5s
   #10    │      3.200        │  $0.013   │  1.6s
   #15    │      3.400        │  $0.014   │  1.7s
   #20    │      3.500        │  $0.014   │  1.7s
   #25    │      3.600        │  $0.014   │  1.7s
   #30    │      3.700        │  $0.015   │  1.8s
──────────┼───────────────────┼───────────┼──────────
TOTAL     │    21.700 tokens  │  $0.087   │  (média 1.6s)
          │    (86% REDUÇÃO)  │ (86% RED.)│ (56% RED.)
```

**O compaction sozinho gerou:**
- **86% de redução no consumo de tokens** em conversas longas
- **86% de redução no custo de API** (de $0.63 para $0.09 por conversa de 60 min)
- **56% de redução na latência média** (de 3.6s para 1.6s)

### 4.5 Compaction: Quando e Como Disparar

O compaction não é executado a cada interação — isso seria contraproducente (custo do compaction > economia). Em vez disso, usa gatilhos inteligentes:

```
┌─────────────────────────────────────────────────────────────┐
│                COMPACTION TRIGGERS                           │
│                                                               │
│  TRIGGER 1: Threshold de Tokens                              │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ Se contexto_atual > 8.000 tokens → DISPARA COMPACTION    │ │
│  │ (8.000 tokens = ponto onde custo começa a superar        │ │
│  │  o custo de rodar o próprio compaction)                  │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                               │
│  TRIGGER 2: Intervalo de Tempo                                │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ Se última_compaction > 10 minutos → DISPARA COMPACTION   │ │
│  │ (Garante que contexto não cresce descontroladamente      │ │
│  │  mesmo em conversas com mensagens curtas)                │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                               │
│  TRIGGER 3: Mudança de Intenção                               │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ Se intenção mudou (ex: "descoberta" → "compra")          │ │
│  │ → DISPARA COMPACTION                                     │ │
│  │ (Resume a fase anterior antes de iniciar a nova)         │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                               │
│  TRIGGER 4: Idle Time                                         │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ Se cliente inativo > 5 minutos → DISPARA COMPACTION      │ │
│  │ (Prepara o estado para quando o cliente voltar)          │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### 4.6 O Custo do Próprio Compaction

Uma preocupação legítima: **o compaction também custa dinheiro** (usa LLM para sumarizar). A equipe modelou o trade-off:

```
CUSTO DO COMPACTION vs. ECONOMIA GERADA:

Conversa de 60 minutos, 30 interações:

SEM compaction:
  Custo total: $0.629

COM compaction (Nível 1 + 2):
  Custo do compaction: 3 sumarizações × $0.003 = $0.009
  Custo das interações: $0.087
  Custo total: $0.096
  
  Economia: $0.629 - $0.096 = $0.533 por conversa (85%)
  
  Para 10.000 conversas/dia:
  Sem compaction: $6.290/dia
  Com compaction: $960/dia
  Economia: $5.330/dia = $159.900/mês
```

**O compaction se paga com folga.** Para cada $1 gasto em compaction, economiza-se ~$60 em custo de API.

---

## 📊 Seção 5: Diagrama ASCII da Arquitetura Escalada

### 5.1 Visão Macro: O Sistema Completo

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                              KODA SCALE-UP — ARQUITETURA COMPLETA                         │
│                              Suporta 10.000+ Conversas/Dia                               │
│                                                                                            │
│  ┌──────────────────────────────────────────────────────────────────────────────────────┐│
│  │                              ENTRADA (WHATSAPP)                                        ││
│  │                                                                                        ││
│  │  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐           ││
│  │  │Cliente 1 │   │Cliente 2 │   │Cliente 3 │   │Cliente N │   │ ...      │           ││
│  │  │(WhatsApp)│   │(WhatsApp)│   │(WhatsApp)│   │(WhatsApp)│   │          │           ││
│  │  └────┬─────┘   └────┬─────┘   └────┬─────┘   └────┬─────┘   └──────────┘           ││
│  │       │              │              │              │                                   ││
│  │       └──────────────┼──────────────┼──────────────┘                                   ││
│  │                      │              │                                                  ││
│  │              ┌───────▼──────────────▼───────┐                                         ││
│  │              │    WHATSAPP BUSINESS API     │                                         ││
│  │              │    (Webhook → Sistema)       │                                         ││
│  │              └───────────────┬──────────────┘                                         ││
│  └──────────────────────────────┼────────────────────────────────────────────────────────┘│
│                                 │                                                          │
│  ┌──────────────────────────────▼────────────────────────────────────────────────────────┐│
│  │                         CAMADA 1: INGESTÃO & ROTEAMENTO                                ││
│  │                                                                                        ││
│  │  ┌──────────────────────────────────────────────────────────────────────────────────┐ ││
│  │  │                         API GATEWAY (Nginx + Rate Limiting)                        │ ││
│  │  │                         - Valida assinatura WhatsApp                               │ ││
│  │  │                         - Rate limit: 100 req/s por tenant                         │ ││
│  │  │                         - Autentica e autoriza                                     │ ││
│  │  └───────────────────────────────┬──────────────────────────────────────────────────┘ ││
│  │                                  │                                                     ││
│  │  ┌───────────────────────────────▼──────────────────────────────────────────────────┐ ││
│  │  │                    MESSAGE QUEUE (Redis Streams)                                    │ ││
│  │  │                                                                                    │ ││
│  │  │  Stream: koda:incoming                                                             │ ││
│  │  │  ┌──────┬──────────┬─────────────┬──────────┬──────────┐                          │ ││
│  │  │  │  ID  │Customer  │ Message     │ Intent   │ Priority │                          │ ││
│  │  │  ├──────┼──────────┼─────────────┼──────────┼──────────┤                          │ ││
│  │  │  │ 001  │cust_123  │ "Quero..."  │purchase  │ HIGH     │                          │ ││
│  │  │  │ 002  │cust_456  │ "Dúvida..." │question  │ LOW      │                          │ ││
│  │  │  │ 003  │cust_789  │ "Atrasou!"  │complaint │ CRITICAL │                          │ ││
│  │  │  │ ...  │...       │ ...         │ ...      │ ...      │                          │ ││
│  │  │  └──────┴──────────┴─────────────┴──────────┴──────────┘                          │ ││
│  │  └───────────────────────────────┬──────────────────────────────────────────────────┘ ││
│  │                                  │                                                     ││
│  │  ┌───────────────────────────────▼──────────────────────────────────────────────────┐ ││
│  │  │                         INTENT ROUTER (Claude Haiku)                               │ ││
│  │  │                         - Classifica intenção (8 categorias)                       │ ││
│  │  │                         - Atribui prioridade                                        │ ││
│  │  │                         - Roteia para fila correta                                 │ ││
│  │  └───────────────────────────────┬──────────────────────────────────────────────────┘ ││
│  └──────────────────────────────────┼────────────────────────────────────────────────────┘│
│                                     │                                                      │
│  ┌──────────────────────────────────▼────────────────────────────────────────────────────┐│
│  │                          CAMADA 2: PROCESSAMENTO MULTI-AGENT                            ││
│  │                                                                                        ││
│  │  ┌─────────────────────────────────────────────────────────────────────────────────┐  ││
│  │  │                          ORCHESTRATOR (Coordenação Central)                       │  ││
│  │  │                          - Lê da fila de entrada                                  │  ││
│  │  │                          - Inicia pipeline de agentes                             │  ││
│  │  │                          - Gerencia timeouts e retries                            │  ││
│  │  └───────────────────────────────┬─────────────────────────────────────────────────┘  ││
│  │                                  │                                                    ││
│  │       ┌──────────────────────────┼──────────────────────────┐                        ││
│  │       │                          │                          │                        ││
│  │  ┌────▼─────┐              ┌─────▼──────┐            ┌──────▼─────┐                  ││
│  │  │ PLANNER  │──────────────▶ DISCOVERY  │────────────▶ GENERATOR  │                  ││
│  │  │  AGENT   │              │   AGENT    │            │   AGENT    │                  ││
│  │  │          │              │            │            │            │                  ││
│  │  │ Pool: 5  │              │ Pool: 8    │            │ Pool: 10   │                  ││
│  │  │ Model:   │              │ Model: N/A │            │ Model:     │                  ││
│  │  │ Sonnet   │              │ (MongoDB)  │            │ Sonnet     │                  ││
│  │  └────┬─────┘              └─────┬──────┘            └──────┬─────┘                  ││
│  │       │                          │                          │                        ││
│  │       │         ┌────────────────┘                          │                        ││
│  │       │         │                                           │                        ││
│  │       │    ┌────▼───────────────────────────────────────────▼──┐                     ││
│  │       │    │              COORDINATION LAYER                    │                     ││
│  │       │    │         (State Files + Lock Manager)              │                     ││
│  │       │    └────────────────────┬──────────────────────────────┘                     ││
│  │       │                         │                                                    ││
│  │       │                         ▼                                                    ││
│  │       │              ┌──────────────────┐                                            ││
│  │       └──────────────▶    EVALUATOR     │                                            ││
│  │                      │      AGENT       │                                            ││
│  │                      │                  │                                            ││
│  │                      │ Pool: 5          │                                            ││
│  │                      │ Model: Haiku     │                                            ││
│  │                      └────────┬─────────┘                                            ││
│  │                               │                                                      ││
│  │                          ┌────▼─────┐                                               ││
│  │                          │ APPROVE? │                                               ││
│  │                          └──┬───┬───┘                                               ││
│  │                     ┌───────┘   └───────┐                                           ││
│  │                YES  │                   │ NO (reject)                                ││
│  │                     ▼                   ▼                                            ││
│  │            ┌────────────┐      ┌───────────────┐                                    ││
│  │            │ RESPONSE   │      │ FEEDBACK LOOP │                                    ││
│  │            │ GENERATOR  │      │ → Back to     │                                    ││
│  │            │ (Template) │      │   Generator   │                                    ││
│  │            └─────┬──────┘      └───────────────┘                                    ││
│  │                  │                                                                    ││
│  └──────────────────┼────────────────────────────────────────────────────────────────────┘│
│                     │                                                                      │
│  ┌──────────────────▼────────────────────────────────────────────────────────────────────┐│
│  │                           CAMADA 3: PERSISTÊNCIA & ESTADO                              ││
│  │                                                                                        ││
│  │  ┌─────────────────┐  ┌──────────────────┐  ┌──────────────────┐                      ││
│  │  │  STATE STORE    │  │  TRACE STORE     │  │  METRIC STORE    │                      ││
│  │  │                 │  │                  │  │                  │                      ││
│  │  │ /var/koda/      │  │ /var/koda/       │  │ Prometheus +     │                      ││
│  │  │ state/          │  │ traces/          │  │ Grafana          │                      ││
│  │  │                 │  │                  │  │                  │                      ││
│  │  │ - Conversations │  │ - Append-only    │  │ - Latência       │                      ││
│  │  │ - Interactions  │  │   JSONL logs     │  │ - Throughput     │                      ││
│  │  │ - Snapshots     │  │ - Auditoria      │  │ - Erro rate      │                      ││
│  │  │ - Locks         │  │ - Debugging      │  │ - Custo          │                      ││
│  │  └────────┬────────┘  └────────┬─────────┘  └────────┬─────────┘                      ││
│  │           │                    │                      │                                 ││
│  │           └────────────────────┼──────────────────────┘                                 ││
│  │                                │                                                        ││
│  │  ┌─────────────────────────────▼──────────────────────────────────────────────────┐   ││
│  │  │                        COMPACTION ENGINE (Background)                           │   ││
│  │  │                                                                                 │   ││
│  │  │  ┌────────────────┐    ┌──────────────────┐    ┌──────────────────┐            │   ││
│  │  │  │Nível 1:        │    │Nível 2:          │    │Nível 3:          │            │   ││
│  │  │  │Interação       │───▶│Conversa          │───▶│Cross-Conversa    │            │   ││
│  │  │  │(online, sync)  │    │(bg, cada 10 min) │    │(batch, diário)   │            │   ││
│  │  │  └────────────────┘    └──────────────────┘    └──────────────────┘            │   ││
│  │  └─────────────────────────────────────────────────────────────────────────────────┘   ││
│  └───────────────────────────────────────────────────────────────────────────────────────┘│
│                                                                                            │
│  ┌───────────────────────────────────────────────────────────────────────────────────────┐│
│  │                       CAMADA 4: OBSERVABILIDADE & CONTROLE                              ││
│  │                                                                                        ││
│  │  ┌──────────────┐  ┌───────────────┐  ┌──────────────┐  ┌──────────────┐             ││
│  │  │  DASHBOARD   │  │   ALERTING    │  │  AUTO-SCALE  │  │  AUDIT LOG   │             ││
│  │  │  (Grafana)   │  │  (Prometheus  │  │  (K8s HPA)   │  │  (JSONL)     │             ││
│  │  │              │  │   AlertMgr)   │  │              │  │              │             ││
│  │  │ - Conversas  │  │              │  │ - Scale up   │  │ - Compliance │             ││
│  │  │   ativas     │  │ - Latência    │  │   ao atingir │  │ - Debugging  │             ││
│  │  │ - Throughput │  │   > 5s       │  │   70% capac. │  │ - Auditoria  │             ││
│  │  │ - Custo      │  │ - Erro rate  │  │ - Scale down │  │              │             ││
│  │  │ - Pipeline   │  │   > 5%       │  │   abaixo de  │  │              │             ││
│  │  │   status     │  │ - Fila       │  │   30% capac. │  │              │             ││
│  │  │              │  │   > 1000     │  │              │  │              │             ││
│  │  └──────────────┘  └───────────────┘  └──────────────┘  └──────────────┘             ││
│  └───────────────────────────────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 5.2 Visão de Fluxo de Dados: Uma Interação Completa

```
TIMELINE DE UMA INTERAÇÃO (Cliente → KODA → Cliente):

t=0ms    Cliente envia: "Quero whey sem lactose até R$150"
         │
t=50ms   API Gateway recebe, valida, autentica
         │
t=55ms   Enfileirado em Redis Stream (koda:incoming)
         │
t=60ms   Intent Router classifica: intent=purchase, priority=HIGH
         │
t=260ms  Intent Router responde com classificação
         │
t=270ms  Orchestrator lê da fila, inicia pipeline
         │
t=275ms  ┌─ PLANNER AGENT ─────────────────────────────┐
         │  Lê state file do cliente                    │
         │  Analisa intenção + constraints              │
         │  Gera planner_contract.json                  │
         │  Tempo: 1200ms | Custo: $0.0032              │
         └──────────────────────────────────────────────┘
         │
t=1475ms ┌─ DISCOVERY AGENT ───────────────────────────┐
         │  Lê planner_contract.json                    │
         │  Consulta MongoDB com filtros                │
         │  Retorna 3 produtos compatíveis              │
         │  Tempo: 45ms | Custo: $0 (MongoDB)           │
         └──────────────────────────────────────────────┘
         │
t=1520ms ┌─ GENERATOR AGENT ───────────────────────────┐
         │  Lê discovery_context.json                   │
         │  Gera recomendação personalizada             │
         │  Output: generator_draft.json                │
         │  Tempo: 1800ms | Custo: $0.0050              │
         └──────────────────────────────────────────────┘
         │
t=3320ms ┌─ EVALUATOR AGENT ───────────────────────────┐
         │  Lê planner_contract.json                    │
         │  Lê generator_draft.json                     │
         │  Valida 6 critérios                          │
         │  Veredito: APPROVE (6/6 PASS)                │
         │  Tempo: 600ms | Custo: $0.0006               │
         └──────────────────────────────────────────────┘
         │
t=3920ms ┌─ RESPONSE GENERATOR ────────────────────────┐
         │  Formata resposta (template)                 │
         │  Inclui links de compra                      │
         │  Tempo: 10ms | Custo: $0                     │
         └──────────────────────────────────────────────┘
         │
t=3930ms ┌─ COMPACTION (Nível 1) ──────────────────────┐
         │  Resume interação para histórico             │
         │  Atualiza state file                         │
         │  Tempo: 200ms | Custo: $0.0003               │
         └──────────────────────────────────────────────┘
         │
t=4130ms Envia resposta ao cliente via WhatsApp
         │
         TOTAL: 4.130ms | Custo: $0.0091
```

---

## 📋 Seção 6: Tabela Comparativa de Estratégias de Coordenação

### 6.1 Estratégias Avaliadas

Durante o desenvolvimento, a equipe avaliou 5 estratégias de coordenação diferentes antes de escolher a File-Based com Locks:

| Dimensão | Agente Único (v1.0) | Escala Horizontal Ingênua | Redis State Store | Message Queue + DB | File-Based + Locks (v2.0) |
|---|---|---|---|---|---|
| **Arquitetura** | 1 agente faz tudo | Múltiplos agentes idênticos | Agentes com Redis central | Agentes com fila + PostgreSQL | Agentes com arquivos versionados |
| **Coordenação** | Nenhuma (monolítico) | Nenhuma (race conditions) | WATCH/MULTI transactions | SELECT FOR UPDATE + queue ack | File locks (O_CREAT\|O_EXCL) |
| **Escala de Leitura** | ⭐ (linear) | ⭐⭐ (distribuída) | ⭐⭐⭐⭐⭐ (excelente) | ⭐⭐⭐⭐ (boa) | ⭐⭐⭐ (moderada) |
| **Escala de Escrita** | ⭐ (linear) | ⭐ (corrupção de dados) | ⭐⭐⭐⭐ (boa com sharding) | ⭐⭐⭐⭐ (boa) | ⭐⭐⭐ (moderada) |
| **Latência P95** | 4.5s | 12s (degradada) | 3.2s | 2.8s | 3.8s |
| **Custo Operacional** | $0/mês (sem infra) | $200/mês (NFS) | $300/mês (Redis gerenciado) | $450/mês (Redis + PG) | $50/mês (disco local) |
| **Debugabilidade** | ⭐⭐⭐ (logs soltos) | ⭐ (caos) | ⭐⭐ (redis-cli) | ⭐⭐⭐ (SQL queries) | ⭐⭐⭐⭐⭐ (cat + jq) |
| **Persistência** | Arquivos locais | Frágil (NFS) | Frágil (em memória) | Excelente (PG) | Excelente (disco + snapshots) |
| **Auditoria** | Manual | Impossível | Complexa | Boa (SQL) | Excelente (JSONL) |
| **Versionamento** | Não | Não | Não | Parcial (triggers) | Nativo (symlinks) |
| **Resiliência a Falhas** | Baixa (crash = perda) | Muito baixa | Média (AOF) | Alta (WAL) | Alta (locks + snapshots) |
| **Curva de Aprendizado** | Baixa | Baixa | Média | Alta | Média |
| **Manutenção** | Simples | Pesadelo | Média | Média-Alta | Baixa-Média |
| **Adequação para Escala** | Até 100/dia | Não funciona | Até 5.000/dia | Até 50.000/dia | Até 20.000/dia |

### 6.2 Análise Detalhada de Cada Estratégia

#### Estratégia A: Agente Único (v1.0)

```
PRÓS:
✅ Simplicidade máxima
✅ Custo operacional zero
✅ Debug simples (um agente = um log)

CONTRAS:
❌ Não escala horizontalmente
❌ Gargalo único (CPU, I/O, API)
❌ Sem isolamento de falhas
❌ Custo de API cresce linearmente

QUANDO USAR:
- MVP / protótipo
- Até 100 conversas/dia
- Equipe de 1-2 pessoas
```

#### Estratégia B: Escala Horizontal Ingênua

```
PRÓS:
✅ Teoricamente escala horizontalmente
✅ Reuso de código existente

CONTRAS:
❌ Race conditions inevitáveis em state files
❌ NFS é gargalo de I/O
❌ Sem coordenação entre instâncias
❌ Debugging quase impossível

QUANDO USAR:
- NUNCA em produção
- Apenas para aprendizado do que NÃO fazer
```

#### Estratégia C: Redis State Store

```
PRÓS:
✅ Resolve race conditions (transações atômicas)
✅ Baixíssima latência de leitura (<1ms)
✅ Fácil de implementar (bibliotecas maduras)

CONTRAS:
❌ Custo operacional alto (cluster gerenciado)
❌ Persistência frágil (em memória)
❌ Debug difícil (estado é opaco)
❌ Sem versionamento nativo
❌ Perda de dados em crash sem AOF configurado

QUANDO USAR:
- Sistemas com alta exigência de latência
- Quando custo operacional não é preocupação
- Como cache, não como source of truth
```

#### Estratégia D: Message Queue + Banco de Dados

```
PRÓS:
✅ Coordenação robusta (filas + transações)
✅ Persistência excelente (PostgreSQL)
✅ Escala bem (particionamento)
✅ Auditoria nativa (SQL queries)

CONTRAS:
❌ Maior complexidade operacional
❌ Duas dependências externas (Redis + PostgreSQL)
❌ Maior latência (2 sistemas)
❌ Maior custo operacional
❌ Overhead para sistemas menores

QUANDO USAR:
- Sistemas com >50.000 conversas/dia
- Exigências de compliance rigorosas
- Equipes com experiência em sistemas distribuídos
```

#### Estratégia E: File-Based + Lock Manager (v2.0 — ESCOLHIDA)

```
PRÓS:
✅ Debugabilidade excepcional (arquivos são autodescritivos)
✅ Versionamento natural (symlinks + timestamps)
✅ Baixo custo operacional
✅ Sem dependências externas adicionais
✅ Auditoria trivial (append-only JSONL)
✅ Resiliência (snapshots + locks com timeout)

CONTRAS:
❌ Escala de escrita moderada (lock contention)
❌ Latência de I/O pode variar com carga de disco
❌ Não é ideal para >20.000 conversas/dia (nesse ponto, migrar para PostgreSQL)
❌ Requer disciplina na organização de diretórios

QUANDO USAR:
- 100 a 20.000 conversas/dia
- Quando debugabilidade é prioritária
- Equipes que valorizam simplicidade operacional
- Sistemas onde estado é principalmente texto (JSON)
```

### 6.3 Por Que File-Based Foi a Escolha Certa para KODA

A decisão final foi motivada por três fatores:

1. **Debugabilidade é rei:** A equipe KODA tinha 5 engenheiros. Quando algo dava errado a 2 da manhã, a última coisa que queriam era decodificar `redis-cli` outputs. Poder fazer `cat state/cust_123/current | jq .preferences` era um superpoder operacional.

2. **Custo importa:** Com o orçamento apertado da campanha, gastar $300-450/mês em infraestrutura de coordenação era difícil de justificar. File-based custava praticamente zero além do disco que já existia.

3. **"Você não vai precisar" (YAGNI):** A projeção mais agressiva era 15.000 conversas/dia. File-based escala confortavelmente até 20.000. Se um dia o KODA precisasse de 50.000, a migração para PostgreSQL seria justificada e teria ROI claro.

---

## 📊 Seção 7: Métricas Comparativas

### 7.1 Antes vs. Depois: KODA v1.0 vs. v2.0

| Métrica | v1.0 (Março 2026) | v2.0 (Maio 2026) | Melhoria |
|---|---|---|---|
| **Capacidade Máxima** | 100 conversas/dia | 15.000 conversas/dia | **150x** |
| **Conversas Simultâneas** | 5-10 | 500+ | **50-100x** |
| **Latência Média (p50)** | 2.5 segundos | 1.6 segundos | **36% mais rápido** |
| **Latência P95** | 4.5 segundos | 3.8 segundos | **16% mais rápido** |
| **Latência P99** | 8.2 segundos | 5.1 segundos | **38% mais rápido** |
| **Taxa de Erro** | ~5% | ~1.2% | **76% redução** |
| **Custo por Interação** | $0.0525 | $0.0091 | **83% redução** |
| **Custo por Conversa (média)** | $0.63 (60min) | $0.096 (60min) | **85% redução** |
| **Custo Diário (10.000 conv.)** | $6.290/dia | $960/dia | **85% redução** |
| **Custo Mensal (300K conv.)** | $188.700/mês | $28.800/mês | **85% redução** |
| **Tempo de Debug (por incidente)** | 2-4 horas | 15-30 minutos | **8x mais rápido** |
| **Cobertura de Métricas** | 3 métricas | 47 métricas | **15x mais visibilidade** |
| **Tempo de Onboarding (novo dev)** | 2 semanas | 3 dias | **5x mais rápido** |
| **Satisfação do Cliente (NPS)** | 62 | 78 | **+16 pontos** |
| **Taxa de Abandono de Carrinho** | 34% | 18% | **47% redução** |
| **Tempo Médio de Conversa** | 38 min | 42 min | **+11% (clientes engajam mais)** |

### 7.2 Métricas de Escala: O Que Acontece Quando o Volume Sobe

```
TESTE DE CARGA: Comportamento do Sistema em Diferentes Volumes

Volume (conv/dia) │ v1.0 Latência │ v1.0 Erro% │ v2.0 Latência │ v2.0 Erro% │ Custo/dia (v2.0)
──────────────────┼───────────────┼─────────────┼────────────────┼─────────────┼────────────────
       100        │    2.5s ✅    │   5.0% ⚠️   │    1.6s ✅     │   1.2% ✅   │    $9.60
       500        │    4.8s ⚠️    │  12.0% 🔴   │    1.7s ✅     │   1.3% ✅   │   $48.00
     1.000        │    8.2s 🔴   │  23.0% 🔴   │    1.8s ✅     │   1.4% ✅   │   $96.00
     2.500        │   15.0s 🔴   │  41.0% 🔴   │    2.1s ✅     │   1.6% ✅   │  $240.00
     5.000        │  CRASH 🔴    │   N/A       │    2.5s ✅     │   1.9% ✅   │  $480.00
     7.500        │  CRASH 🔴    │   N/A       │    2.9s ✅     │   2.3% ⚠️   │  $720.00
    10.000        │  CRASH 🔴    │   N/A       │    3.4s ⚠️     │   2.8% ⚠️   │  $960.00
    12.500        │  CRASH 🔴    │   N/A       │    4.1s ⚠️     │   3.5% 🔴   │$1.200.00
    15.000        │  CRASH 🔴    │   N/A       │    5.2s 🔴     │   4.8% 🔴   │$1.440.00
```

**Interpretação:**
- **v1.0:** Começa a degradar aos 500 conv/dia. Crash total aos 5.000. Nunca chegaria perto dos 10.000.
- **v2.0:** Mantém-se estável até 7.500 conv/dia. Degradação gradual começa aos 10.000 (conforme esperado). Aos 15.000, precisa de otimização adicional (próxima fase: migração para PostgreSQL + sharding).

### 7.3 Métricas de Custo por Componente (10.000 conversas/dia)

```
DISTRIBUIÇÃO DE CUSTO DIÁRIO (v2.0, 10.000 conv/dia, ~200K interações):

Componente                    Custo/Dia    % do Total
─────────────────────────────────────────────────────
API LLM (Claude):
  - Intent Router (Haiku)      $40.00       4.2%
  - Planner Agent (Sonnet)    $192.00      20.0%
  - Generator Agent (Sonnet)  $380.00      39.6%
  - Evaluator Agent (Haiku)    $48.00       5.0%
  - Compaction (Haiku)         $60.00       6.2%
  Subtotal LLM:               $720.00      75.0%
─────────────────────────────────────────────────────
Infraestrutura:
  - Servidores (compute)      $120.00      12.5%
  - Redis (cache + streams)    $50.00       5.2%
  - MongoDB (catálogo)         $30.00       3.1%
  - Storage (state files)      $10.00       1.0%
  - Monitoring (Prom/Grafana)  $20.00       2.1%
  - WhatsApp Business API      $10.00       1.0%
  Subtotal Infra:             $240.00      25.0%
─────────────────────────────────────────────────────
TOTAL DIÁRIO:                 $960.00     100.0%
TOTAL MENSAL (30 dias):     $28.800.00
```

**Insight crítico:** 75% do custo está nas chamadas de API LLM. Qualquer otimização de custo deve focar primariamente em reduzir o uso de LLM, não em infraestrutura. Isso explica por que compaction e escolha de modelos (Haiku vs. Sonnet) são tão importantes.

### 7.4 Métricas de Confiabilidade

```
DISPONIBILIDADE DO SISTEMA (Maio 2026, pós-migração):

Métrica                        │ Alvo     │ Real    │ Status
───────────────────────────────┼──────────┼─────────┼────────
Uptime (24/7)                  │ 99.5%    │ 99.87%  │ ✅
Tempo de Resposta P95          │ <5s      │ 3.8s    │ ✅
Taxa de Erro                   │ <2%      │ 1.2%    │ ✅
Tempo de Recuperação (MTTR)    │ <15 min  │ 8 min   │ ✅
Perda de Dados                 │ 0        │ 0       │ ✅
Incidentes Críticos/mês        │ <3       │ 1       │ ✅
```

---

## 🔧 Seção 8: KODA Application — Aplicação Prática

### 8.1 Como Usar Este Case Study no Seu Dia a Dia

Este case study não é apenas uma história — é um **manual de engenharia**. Aqui está como aplicar cada lição ao seu contexto:

#### Para Desenvolvedores Implementando Features

**Cenário: Você vai implementar uma nova feature no KODA (ex: "Recomendação de Combos")**

```
CHECKLIST PRÉ-IMPLEMENTAÇÃO:

☐ 1. A feature escala? Quantas conversas simultâneas ela vai gerar?
     → Se >10% de aumento de carga, revisar capacity planning

☐ 2. Onde o estado da feature vive?
     → State file versionado? Redis cache? MongoDB?
     → Quem lê? Quem escreve? Concorrência?

☐ 3. Qual modelo usar para cada etapa?
     → Intenção simples → Haiku ($)
     → Geração complexa → Sonnet ($$)
     → Validação → Haiku ($)
     → Busca de dados → MongoDB (sem LLM)

☐ 4. Onde colocar checkpoints de qualidade?
     → Antes de enviar resposta ao cliente: SEMPRE
     → Após busca de produtos: se resultado >50 itens
     → Após cálculo de preço: se envolve desconto

☐ 5. Como debugar se algo der errado?
     → Trace file (JSONL) registra cada etapa?
     → State file tem versão anterior para comparação?
     → Métricas mostram onde o erro ocorreu?
```

#### Para Arquitetos Desenhando Novos Sistemas

**Cenário: Você vai desenhar um novo agente do zero**

```
PRINCÍPIOS DE ARQUITETURA (derivados deste case study):

1. Comece com 1 agente, mas PROJETE para N agentes
   - Separe responsabilidades desde o dia 1
   - Mesmo que hoje seja um monolito, as interfaces devem
     permitir decomposição futura

2. State files são seus amigos
   - JSON é debugável, versionável, diffable
   - Só migre para Redis/PostgreSQL quando as métricas
     PROVAREM que você precisa

3. Compaction é um multiplicador de economia
   - Implemente Nível 1 (por interação) desde o início
   - Adicione Nível 2 e 3 conforme escala crescer
   - O compaction se paga: cada $1 gasto = $60 economizado

4. Use o modelo certo para cada tarefa
   - Nem tudo precisa de Opus/Sonnet
   - Classificação, validação, sumarização = Haiku
   - Geração complexa = Sonnet
   - Busca de dados = sem LLM

5. Observabilidade não é opcional
   - 47 métricas podem parecer exagero para 100 conv/dia
   - Mas quando você escala para 10.000, cada métrica
     vai te salvar horas de debugging
```

#### Para Líderes Técnicos Gerenciando Equipes

**Cenário: Você precisa decidir se investe em re-arquitetura agora ou depois**

```
FRAMEWORK DE DECISÃO: Quando Re-Arquitetar?

Sinais de que você PRECISA re-arquitetar AGORA:
☐ Latência P95 > 3x a latência baseline
☐ Taxa de erro > 5%
☐ Custo crescendo mais rápido que receita
☐ Debug de incidentes > 2 horas
☐ Equipe com medo de deployar (fragilidade)

Sinais de que você PODE esperar:
☐ Latência estável abaixo do threshold
☐ Taxa de erro < 2%
☐ Custo previsível e proporcional ao volume
☐ Incidentes resolvidos em <30 min
☐ Equipe confiante em deployar

Regra de bolso:
Se você está a MENOS de 3 meses de precisar de 10x a
capacidade atual, comece a re-arquitetar AGORA.
Re-arquitetura apressada = arquitetura ruim.
```

### 8.2 Exemplo Prático: Implementando uma Nova Feature com a Arquitetura v2.0

Vamos simular a implementação de uma feature real usando a arquitetura escalada:

**Feature: "Alerta de Reposição" — KODA avisa cliente quando produto favorito volta ao estoque**

```
PASSO 1: Modelagem no Pipeline Multi-Agent

┌─────────────────────────────────────────────────────────────┐
│ PLANNER: O que precisa acontecer?                            │
│                                                               │
│ {                                                             │
│   "feature": "stock_alert",                                   │
│   "trigger": "product_out_of_stock",                         │
│   "steps": [                                                  │
│     "register_alert",                                         │
│     "monitor_stock",                                          │
│     "notify_customer_on_restock",                             │
│     "offer_alternative_until_then"                            │
│   ]                                                           │
│ }                                                             │
└─────────────────────────────────────────────────────────────┘

PASSO 2: State File para a Feature

/var/koda/state/cust_123/alerts/stock_alert_001.json:
┌─────────────────────────────────────────────────────────────┐
│ {                                                             │
│   "alert_id": "sa_001",                                       │
│   "customer_id": "cust_123",                                  │
│   "product_sku": "WHEY-ISO-001",                              │
│   "product_name": "Whey Isolado Premium",                     │
│   "registered_at": "2026-05-23T14:30:00Z",                   │
│   "status": "active",                                         │
│   "notify_channel": "whatsapp",                               │
│   "alternative_offered": "WHEY-VEG-003",                      │
│   "check_interval_minutes": 30                               │
│ }                                                             │
└─────────────────────────────────────────────────────────────┘

PASSO 3: Integração com Pipeline Existente

Quando um cliente pergunta sobre produto fora de estoque:

1. Intent Router: detecta intenção "product_inquiry"
2. Planner Agent: adiciona step "check_stock_and_offer_alert"
3. Discovery Agent: verifica estoque → "OUT_OF_STOCK"
4. Generator Agent: gera resposta:
   "Infelizmente o Whey Isolado Premium está em falta.
    Quer que eu te avise quando voltar? Enquanto isso,
    posso sugerir o Whey Vegano Premium que é similar."
5. Evaluator Agent: verifica se resposta é útil e empática
6. Se cliente aceitar: cria state file do alerta

PASSO 4: Background Worker para Monitoramento

A cada 30 minutos, um worker consulta MongoDB:
  - Encontra todos os alertas ativos
  - Verifica estoque atual dos SKUs
  - Se voltou ao estoque → dispara notificação
  - Atualiza state file: status = "notified"
```

**Resultado dessa abordagem:**
- A feature foi implementada em 3 dias (vs. estimativa de 2 semanas sem a arquitetura)
- Reusou 80% do pipeline existente (Intent Router, Discovery, Generator, Evaluator)
- Adicionou apenas 1 novo state file type e 1 background worker
- Custo marginal: ~$0.002 por alerta (apenas o compaction adicional)

### 8.3 Um Dia na Vida do KODA Scale-Up: Simulação Real

Para cristalizar como a arquitetura v2.0 funciona na prática, vamos acompanhar **um dia real** de operação — 24 horas na vida do KODA pós-campanha, processando 10.000 conversas.

```
═══════════════════════════════════════════════════════════════════
        24 HORAS NA VIDA DO KODA SCALE-UP (v2.0)
        Data: 27 de Maio de 2026 — 10.247 conversas processadas
═══════════════════════════════════════════════════════════════════

06:00 — INÍCIO DO DIA
─────────────────────
O sistema acorda antes dos clientes:

- Compaction Engine (Nível 3) termina batch noturno:
  → 2.847 perfis de cliente consolidados
  → 156 alertas de reposição verificados
  → 3 produtos detectados como "em falta" → alertas disparados

- Auto-scale reduz pools para mínimo:
  → Planner: 2 workers
  → Discovery: 3 workers
  → Generator: 4 workers
  → Evaluator: 2 workers

- Dashboard mostra:
  Conversas ativas: 0
  Custo acumulado (dia): $0.00
  Latência P95: N/A


07:00 — PRIMEIROS CLIENTES
──────────────────────────
As primeiras mensagens começam a chegar. Clientes matinais:

07:03 — Cliente #001: "Bom dia! Quero comprar creatina"
  → Intent Router: intent=purchase, priority=HIGH
  → Pipeline: Planner (1.2s) → Discovery (0.04s) →
    Generator (1.8s) → Evaluator (0.6s)
  → Resposta em 3.9s. Custo: $0.009
  ✅ Cliente compra. Receita: R$ 79,90

07:15 — 12 conversas ativas simultâneas
  → Todos os pools operando com folga
  → Latência média: 1.8s

07:30 — Auto-scale detecta aumento:
  → Planner: 2 → 3 workers
  → Generator: 4 → 5 workers


08:00 — HORA DO RUSH MATINAL
────────────────────────────
O volume começa a subir rapidamente:

08:00 — 85 conversas ativas
08:15 — 142 conversas ativas
08:30 — 210 conversas ativas ← Dispara alerta de escala

Auto-scale responde automaticamente:
  → Planner: 3 → 5 workers
  → Discovery: 3 → 6 workers
  → Generator: 5 → 8 workers
  → Evaluator: 2 → 4 workers

08:45 — Pico de 247 conversas simultâneas
  → Latência P95: 2.8s (dentro do threshold de 5s)
  → Custo/minuto: $0.42
  → 3 alertas de "alta demanda" registrados
  → NENHUM erro. NENHUMA conversa travada.

08:52 — Incidente menor detectado:
  → Discovery Agent #3 timeout ao consultar MongoDB
  → Lock file de um state file não foi liberado (bug conhecido)
  → Watchdog detecta lock com >30s → remove automaticamente
  → Retry do Discovery Agent: sucesso
  → Tempo total de recuperação: 42 segundos
  → Cliente não percebeu (resposta atrasou apenas 3 segundos)


10:00 — ESTABILIDADE DA MANHÃ
─────────────────────────────
O sistema se estabiliza em ~180 conversas ativas:

10:00 — Compaction Nível 2 começa a rodar (gatilho: 10 minutos):
  → 47 sumarizações de conversa executadas
  → Economia estimada: 320.000 tokens evitados
  → Custo do compaction: $0.14
  → Economia gerada: $4.80 (34x ROI)

10:15 — Cliente VIP detectado (histórico de 5 compras):
  → Intent Router classifica como "returning_vip"
  → Planner carrega customer_360_profile.json
  → Generator personaliza resposta com histórico
  → Cliente compra R$ 347 em suplementos em 4 minutos
  → Receita do cliente VIP: 7x maior que média

10:45 — Primeiro pico de reclamações (3 clientes simultâneos):
  → Intent Router: intent=complaint, priority=CRITICAL
  → Mensagens vão para o topo da fila
  → Tempo de resposta para complaints: 1.2s (vs 3.8s média)
  → 2 resolvidas em <2 minutos, 1 escalada para humano


12:00 — HORA DO ALMOÇO
──────────────────────
Volume cai. Sistema respira:

12:00 — 95 conversas ativas
  → Auto-scale reduz pools:
  → Planner: 5 → 3 workers
  → Generator: 8 → 5 workers

12:30 — Manutenção programada:
  → Snapshot diário dos state files (todas as conversas)
  → Tamanho total: 2.3GB (10.247 state files)
  → Tempo de snapshot: 4 minutos
  → Zero impacto em conversas ativas (snapshot é read-only)

12:45 — Rotação de trace files:
  → trace_2026-05-27.jsonl fechado (847MB)
  → Novo arquivo: trace_2026-05-27_pm.jsonl iniciado


14:00 — TARDE MODERADA
──────────────────────
Volume se mantém estável, com picos pontuais:

14:00 — 150 conversas ativas
14:30 — Promoção relâmpago ativada: "20% OFF próximos 30 min"
  → Volume sobe para 310 conversas em 8 minutos
  → Auto-scale: Generator pool vai para 10 workers
  → Latência P95 sobe para 3.4s (aceitável)
  → 487 recomendações geradas durante a promoção
  → Receita: R$ 12.450 em 30 minutos

15:00 — Incidente #2: API da Anthropic com latência elevada
  → Latência das chamadas Sonnet sobe de 1.8s para 4.5s
  → Dashboard detecta e alerta automaticamente
  → Orchestrator ativa fallback: muda Generator para Haiku
  → Qualidade reduz marginalmente (avaliação ainda passa)
  → Latência volta a 2.1s
  → 18 minutos depois: Anthropic normaliza
  → Orchestrator reverte para Sonnet

16:00 — Equipe de operações analisa os alertas do dia:
  → 2 incidentes (lock file + API latency)
  → Ambos resolvidos automaticamente em <60 segundos
  → Zero intervenção manual necessária
  → Tempo da equipe gasto em operação: 15 minutos (análise)


18:00 — RUSH DO FIM DO DIA
──────────────────────────
Segundo pico do dia. Clientes saindo do trabalho:

18:00 — 340 conversas ativas ← MAIOR PICO DO DIA
  → Todos os pools no máximo:
  → Planner: 5, Discovery: 8, Generator: 10, Evaluator: 5
  → Latência P95: 4.1s (ainda abaixo do threshold de 5s)
  → Custo/minuto: $0.68
  → 100% de aprovação do Evaluator (sem falsos positivos)

18:30 — Conversa mais longa do dia atinge 2h15min:
  → 47 interações processadas
  → Compaction Nível 2 executado 4 vezes
  → Contexto mantido em ~3.500 tokens (vs 62.000 sem compaction)
  → Custo total da conversa: $0.38 (vs $2.40 sem compaction)
  → Cliente comprou R$ 523 em produtos

19:00 — Volume começa a cair:
  → 210 conversas ativas
  → Auto-scale reduz gradualmente


21:00 — NOITE CALMA
────────────────────
Volume baixo. Sistema opera com folga:

21:00 — 45 conversas ativas
  → Pools no mínimo

21:30 — Compaction Nível 3 (cross-conversa) inicia:
  → Processa 847 conversas concluídas hoje
  → Atualiza 523 customer_360_profiles
  → Detecta 12 clientes com múltiplas conversas no dia
  → Consolida preferências para conversas futuras

22:00 — Relatório diário parcial:
  → Conversas processadas: 9.847
  → Receita gerada: R$ 42.150
  → Custo API: $782.40
  → Custo infra: $218.00
  → Margem operacional: 98.8%


00:00 — MADRUGADA
──────────────────
Sistema em modo de manutenção:

00:00 — 8 conversas ativas (clientes noturnos)
  → Pools mínimos

01:00 — Backup completo:
  → State files: 2.3GB → S3 (versionado)
  → Trace files: 1.7GB → S3
  → Snapshots: 450MB → S3

02:00 — Otimização de índices MongoDB

03:00 — Compaction Nível 3 (batch final):
  → Consolida TODAS as conversas do dia
  → Atualiza todos os customer_360_profiles
  → Prepara dados para analytics


06:00 — FIM DO CICLO DE 24 HORAS
─────────────────────────────────
Relatório final do dia:

┌─────────────────────────────────────────────────────────────┐
│         KODA SCALE-UP — RELATÓRIO DIÁRIO                     │
│         Data: 27 de Maio de 2026                             │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Conversas processadas:          10.247                       │
│  Interações processadas:        208.431                       │
│  Pico de conversas simultâneas:    347 (18:23)               │
│                                                               │
│  Latência média (p50):             1.9s                       │
│  Latência P95:                     4.1s                       │
│  Latência P99:                     5.0s                       │
│                                                               │
│  Taxa de erro:                     1.1%                       │
│  Avaliações aprovadas:          98.9%                         │
│  Rejeições com retry:            1.1%                         │
│  Rejeições definitivas:          0.0%                         │
│                                                               │
│  Custo API LLM:                 $812.40                       │
│  Custo Infraestrutura:          $227.00                       │
│  Custo Total:                 $1.039,40                       │
│  Custo por conversa:             $0.10                        │
│                                                               │
│  Compaction:                                               │
│    Nível 1 (interação):        208.431 execuções              │
│    Nível 2 (conversa):          12.847 execuções              │
│    Nível 3 (cross):              1 execução (batch)           │
│    Tokens evitados:          ~4.2 milhões                     │
│    Economia gerada:            ~$63.00                        │
│                                                               │
│  Receita gerada:            R$ 46.570,00                      │
│  Ticket médio:              R$ 24,70                          │
│  Conversão (consulta→compra): 18.4%                           │
│                                                               │
│  Incidentes:                       2                          │
│    - Lock file timeout          (resolvido em 42s)            │
│    - API Anthropic latência     (resolvido em 18min)          │
│  Intervenção manual:               0                          │
│                                                               │
│  Uptime:                       99.97%                         │
│                                                               │
└─────────────────────────────────────────────────────────────┘

STATUS: ✅ DIA NORMAL DE OPERAÇÃO
        Nenhum cliente impactado significativamente.
        Nenhuma escalação para on-call.
        Sistema operou dentro de todos os thresholds.
```

**O que este dia demonstra:**

1. **Resiliência automática:** Dois incidentes ocorreram e foram resolvidos sem intervenção humana. O sistema se curou sozinho.

2. **Escala elástica:** Os pools de agentes escalaram de 11 workers (mínimo) para 28 workers (pico) e voltaram para 11, tudo automaticamente. O custo de infraestrutura acompanhou a demanda real, não a capacidade máxima ociosa.

3. **Compaction como multiplicador:** O compaction evitou 4.2 milhões de tokens desnecessários, gerando economia de $63 em um único dia. Projetado para o mês: ~$1.890 de economia só com compaction.

4. **Priorização efetiva:** Reclamações (CRITICAL) foram respondidas em 1.2s vs 3.8s da média. Clientes insatisfeitos receberam atenção prioritária automaticamente.

5. **Custo previsível e baixo:** $0.10 por conversa, incluindo todas as camadas. Com margem operacional de 98.8%, o modelo de negócio é sustentável mesmo em escala.

### 8.4 Lições Operacionais do Dia Real

Algumas observações que só aparecem quando você opera o sistema por 24 horas:

**Padrão #1: A curva de carga não é uniforme**
```
Volume de Conversas por Hora (27/05/2026):

06h: ▏   8
07h: ▎  47
08h: ██ 210  ← Rush matinal
09h: █▌ 165
10h: █▌ 172
11h: █▌ 158
12h: █  105  ← Almoço (vale)
13h: █▏ 138
14h: █▌ 150
15h: █▌ 168
16h: █▌ 155
17h: █▌ 180
18h: ██▎ 347 ← Rush pós-trabalho (MAIOR PICO)
19h: ██ 210
20h: █▌ 145
21h: █   85
22h: ▎   32
23h: ▏   12
00h: ▏    6
01h: ▏    4
02h: ▏    3
03h: ▏    2
04h: ▏    1
05h: ▏    2
```

**Implicação:** Auto-scale precisa reagir rápido (subir em <2 minutos, descer em <10 minutos). Pools estáticos desperdiçariam dinheiro 80% do tempo ou falhariam nos picos.

**Padrão #2: 80% do custo ocorre em 20% do tempo**
```
Distribuição de custo API por hora:

00h-06h:   3% do custo diário  (madrugada)
06h-12h:  38% do custo diário  (manhã)
12h-18h:  32% do custo diário  (tarde)
18h-00h:  27% do custo diário  (noite)
```

**Implicação:** Se você precisa cortar custo, corte nos horários de pico (otimização de prompt, cache mais agressivo), não na madrugada.

**Padrão #3: Conversas longas são minoria mas consomem a maioria dos tokens**
```
Distribuição de duração de conversa:

 0-10 min:  62% das conversas → 18% dos tokens
10-30 min:  24% das conversas → 31% dos tokens
30-60 min:  10% das conversas → 28% dos tokens
  60+ min:   4% das conversas → 23% dos tokens
```

**Implicação:** O compaction é mais valioso exatamente onde o custo é maior — nas conversas longas. Focar compaction nas conversas de 30+ minutos traria 80% do benefício com 20% do esforço.

---

## 📈 Seção 8.5: Roadmap Futuro — Para Onde o KODA Vai (Planejamento Especulativo)

> **Nota:** Esta seção descreve direções futuras planejadas, não funcionalidades já implementadas. As arquiteturas descritas abaixo são projeções baseadas em tendências de crescimento, não representam o estado atual do sistema em produção.

A arquitetura v2.0 foi projetada para suportar até 20.000 conversas/dia. Mas a equipe já está planejando a v3.0 para quando (não "se") o volume ultrapassar esse limite:

### Fase 3.1: Migração para PostgreSQL (>20.000 conv/dia)

```
Quando atingir consistentemente >15.000 conversas/dia por 2 semanas:

Estado atual (v2.0):
  State files: /var/koda/state/cust_NNN/current.json
  Lock manager: file-based (O_CREAT|O_EXCL)
  Limite prático: ~20.000 conversas/dia

Estado futuro (v3.0):
  State: PostgreSQL com row-level locking (SELECT FOR UPDATE)
  Lock manager: PostgreSQL advisory locks
  Limite projetado: ~100.000 conversas/dia

Migração:
  1. Adicionar PostgreSQL como write-through cache
     (escreve no PG + mantém state file por 30 dias)
  2. Validar com shadow traffic por 2 semanas
  3. Migrar leituras para PG
  4. Descontinuar state files (manter apenas snapshots)
```

### Fase 3.2: Coordenação com Kafka (>50.000 conv/dia)

```
Quando Redis Streams começar a mostrar latência de enfileiramento:

Redis Streams (atual):
  Latência: <1ms até ~50.000 msg/min
  Limite: ~100.000 msg/min (single-threaded Redis)

Kafka (futuro):
  Latência: <5ms até ~1.000.000 msg/min
  Benefício adicional: replay de eventos, multi-tenant nativo
  Custo adicional: ~$200/mês (cluster gerenciado)
```

### Fase 3.3: Model Fine-Tuning para KODA

```
Reduzir dependência de modelos genéricos (Sonnet/Haiku):

Fine-tune um modelo específico para KODA:
  - Treinado com 100.000+ interações reais do KODA
  - Otimizado para tarefas específicas:
    * Recomendação de suplementos
    * Linguagem de e-commerce brasileiro
    * Tratamento de objeções comuns
  - Custo estimado: 80% menor que modelo genérico
  - Latência: 40% menor (modelo menor, mais rápido)
  - Qualidade: igual ou superior para o domínio KODA
```

### Fase 3.4: Multi-Region (Expansão Nacional)

```
Quando KODA expandir para outras regiões do Brasil:

Desafios:
  - Latência para Norte/Nordeste pode ser 50-100ms maior
  - Legislação local (ICMS, frete regional)
  - Catálogos diferentes por região

Solução planejada:
  - Deploy multi-region (SP, BH, Recife)
  - State files replicados async (eventual consistency)
  - Catálogo regionalizado (MongoDB sharding por região)
  - Latência alvo: <5s em qualquer região do Brasil
```

---

## 💡 Seção 9: Lições Aprendidas

### 9.1 As 10 Lições Fundamentais

#### Lição #1: Escala Não É Sobre Servidores — É Sobre Fluxo

> *"Adicionar mais máquinas resolve o sintoma. Redesenhar o fluxo resolve o problema."*

O maior erro da equipe foi achar que escalar era sinônimo de "mais instâncias". A verdadeira escala veio quando redesenharam **como o trabalho flui** através do sistema — do modelo mental de "funil" para "rede".

**Ação prática:** Antes de escalar horizontalmente, desenhe o fluxo de dados. Onde estão os gargalos? Onde o trabalho espera? Onde ele duplica?

---

#### Lição #2: Separação de Responsabilidades é um Multiplicador de Escala

> *"Um agente fazendo 8 coisas não escala. Oito agentes fazendo 1 coisa cada, sim."*

A decomposição do agente monolítico em Planner → Discovery → Generator → Evaluator não foi apenas uma melhoria de qualidade — foi um **multiplicador de escala**. Cada agente pôde ser otimizado independentemente: pool size, modelo, timeout, caching.

**Ação prática:** Para cada responsabilidade no seu sistema, pergunte: "Isso pode ser feito por um componente separado?" Se sim, separe. Mas não exagere — 4 agentes funcionaram para KODA. 20 agentes seriam um pesadelo de coordenação.

---

#### Lição #3: Compaction É o Melhor Investimento em Custo

> *"Cada $1 gasto em compaction economiza $60 em API calls."*

O compaction não é um "nice to have" — é um **imperativo financeiro** para qualquer sistema que processa conversas longas. A redução de 86% no consumo de tokens transformou a economia da KODA.

**Ação prática:** Implemente compaction Nível 1 (por interação) desde o primeiro dia. É barato, é simples, e o ROI é imediato.

---

#### Lição #4: Use o Modelo Certo Para Cada Tarefa

> *"Nem toda mensagem merece um Opus."*

A decisão de usar Haiku para Intent Router e Evaluator (e Sonnet apenas para Planner e Generator) foi responsável por ~40% da economia de custo. Tratar todas as tarefas como igualmente complexas é um desperdício.

**Ação prática:** Classifique cada etapa do seu pipeline por complexidade. Tarefas de classificação e verificação → modelo leve. Tarefas de geração criativa → modelo pesado.

---

#### Lição #5: Debugabilidade Não É Opcional — É Infraestrutura

> *"Se você não consegue debugar em produção, você não tem produção."*

A escolha de file-based coordination foi motivada primariamente por debugabilidade. Quando um incidente acontece às 3 da manhã, a capacidade de fazer `cat state/customer_123/current | jq` e entender o problema em 30 segundos é a diferença entre um incidente de 5 minutos e um de 5 horas.

**Ação prática:** Para cada componente do sistema, pergunte: "Se isso falhar às 3 da manhã, quanto tempo levo para diagnosticar?" Se a resposta for >15 minutos, você tem um problema de debugabilidade.

---

#### Lição #6: State Files Versionados São um Superpoder

> *"Poder voltar no tempo e ver exatamente o que o sistema 'pensava' em qualquer momento é priceless."*

O versionamento de state files (via symlinks + timestamps) permitiu:
- Debug de race conditions (comparar v0003 com v0004)
- Rollback de estado corrompido
- Auditoria de decisões do agente
- Treinamento de novos modelos (dados de qualidade)

**Ação prática:** Todo estado mutável deve ser versionado. O custo de armazenar versões antigas é irrisório comparado ao valor de poder voltar no tempo.

---

#### Lição #7: Métricas Preveem Problemas; Logs Explicam Problemas

> *"Quando a latência P95 começou a subir, sabíamos que algo estava errado. Os trace files nos disseram exatamente o quê."*

As 47 métricas do dashboard não eram vaidade — cada uma foi escolhida porque já havia salvado a equipe de um incidente. Métricas são seu sistema de alerta precoce; trace files são seu sistema de diagnóstico.

**Ação prática:** Para cada métrica no dashboard, pergunte: "O que eu faria se essa métrica dobrasse?" Se não souber responder, a métrica não é acionável.

---

#### Lição #8: A Migração Deve Ser Incremental

> *"Não reescrevemos o KODA. Evoluímos ele."*

A equipe não jogou fora o v1.0 e construiu o v2.0 do zero. Eles:
1. Identificaram os 7 gargalos
2. Priorizaram por impacto (não por facilidade)
3. Resolveram um gargalo por vez
4. Testaram cada mudança em produção com feature flags
5. Só passaram para o próximo gargalo quando o anterior estava validado

**Ação prática:** Nunca faça "big bang rewrites". Evolua incrementalmente. Cada passo deve ser reversível e testável isoladamente.

---

#### Lição #9: Simplicidade Operacional > Pureza Teórica

> *"Poderíamos ter usado Kafka + PostgreSQL + Kubernetes operators. Mas aí precisaríamos de uma equipe de SRE."*

A escolha de Redis Streams (em vez de Kafka) e file-based state (em vez de PostgreSQL) foi deliberada. A equipe tinha 5 engenheiros. Adicionar complexidade operacional que a equipe não conseguia sustentar seria pior do que uma arquitetura tecnicamente "inferior" mas operacionalmente viável.

**Ação prática:** Antes de adotar uma tecnologia, pergunte: "Nossa equipe consegue operar isso às 3 da manhã?" Se a resposta for não, procure alternativa mais simples.

---

#### Lição #10: Escala se Projeta, Não se Improvisa

> *"Se tivéssemos esperado a campanha começar para pensar em escala, teríamos falhado."*

O fato de Fernando ter começado a planejar a escala ANTES da campanha — mesmo que as primeiras tentativas tenham falhado — foi o que salvou o projeto. Escala não é algo que se adiciona depois; é algo que se projeta desde o início.

**Ação prática:** Mesmo que você tenha 100 conversas/dia hoje, projete para 1.000. Mesmo que você tenha 1.000, projete para 10.000. As decisões arquiteturais que você toma hoje determinam o quão dolorosa será a escala amanhã.

---

### 9.2 O Que Faríamos Diferente (Retrospectiva Honesta)

Nem tudo foram acertos. A equipe documentou o que faria diferente se pudesse voltar no tempo:

1. **Compaction desde o dia 1:** O compaction só foi implementado na v2.0. Se tivesse sido implementado na v1.0, teria economizado ~$5.000 em custos de API nos primeiros 2 meses.

2. **Métricas desde o dia 1:** O dashboard com 47 métricas foi construído durante a crise de escala. Se existisse antes, a equipe teria detectado os gargalos semanas antes.

3. **Testes de carga semanais:** A equipe só fez teste de carga quando a campanha estava a 5 dias de distância. Testes de carga semanais teriam revelado os problemas de escala muito antes.

4. **Não subestimar NFS:** A primeira tentativa (escala horizontal com NFS) foi um desastre que custou 2 dias de trabalho. A equipe deveria ter pesquisado mais antes de implementar.

5. **Documentar decisões arquiteturais:** As razões por trás de cada decisão (ex: "por que file-based, não Redis?") foram documentadas apenas neste case study. Deveriam ter sido documentadas como ADRs (Architecture Decision Records) no momento da decisão.

---

## 📝 Seção 10: O Que Você Aprendeu

### Resumo dos Conceitos-Chave

Este case study cobriu a jornada completa de escalar o KODA de 100 para 10.000 conversas por dia. Aqui está o que você deve levar consigo:

#### 🏗️ Arquitetura
- ✅ Agentes monolíticos não escalam. A separação em Planner → Discovery → Generator → Evaluator permite escalar cada componente independentemente.
- ✅ A Camada 1 (Ingestão) protege o sistema. Rate limiting, filas e classificação de intenção evitam que picos derrubem o pipeline.
- ✅ File-based coordination com locks é uma alternativa viável (e muitas vezes superior) a Redis/PostgreSQL para sistemas de médio porte.

#### 🗜️ Compaction
- ✅ Compaction não é opcional para agentes long-running. Sem ele, o custo de API cresce exponencialmente com o tempo de conversa.
- ✅ Compaction em 3 níveis (interação, conversa, cross-conversa) reduz o consumo de tokens em 86%.
- ✅ O compaction se paga: cada $1 investido economiza ~$60 em API calls.

#### 📊 Métricas & Observabilidade
- ✅ 47 métricas não é exagero quando você opera 10.000 conversas/dia. Cada métrica deve ser acionável.
- ✅ Trace files (JSONL append-only) são a melhor ferramenta de debugging para sistemas multi-agent.
- ✅ Dashboards em tempo real permitem detectar degradação antes que os clientes sintam.

#### 💰 Economia
- ✅ A arquitetura multi-agent + compaction reduziu o custo por conversa em 85%.
- ✅ Usar o modelo certo para cada tarefa (Haiku para tarefas simples, Sonnet para complexas) é responsável por ~40% da economia.
- ✅ O custo operacional da arquitetura v2.0 é 83% menor que a v1.0 para o mesmo volume.

#### 🔧 Operação
- ✅ Debugabilidade é um requisito de arquitetura, não um afterthought.
- ✅ State files versionados permitem auditoria, debug e rollback.
- ✅ Simplicidade operacional é mais importante que pureza teórica.

### Checklist de Auto-Avaliação

Você realmente entendeu este case study? Verifique:

- [ ] Consigo explicar por que escala horizontal ingênua falhou
- [ ] Consigo desenhar o pipeline de 4 agentes (Planner → Discovery → Generator → Evaluator)
- [ ] Consigo explicar os 3 níveis de compaction e quando cada um dispara
- [ ] Consigo comparar file-based coordination com Redis-based e justificar a escolha
- [ ] Consigo listar as 10 lições aprendidas sem consultar o texto
- [ ] Consigo aplicar o framework de decisão de "quando re-arquitetar" a um sistema real
- [ ] Consigo calcular o ROI do compaction para um dado volume de conversas
- [ ] Entendo por que 75% do custo está em API LLM e como otimizar isso

### Para Onde Ir Agora

**Se você quer aprofundar em arquitetura:**
→ `01-koda-architecture.md` — A arquitetura completa do KODA em detalhes
→ `03-nivel-3-advanced-architecture/01-multi-agent-systems.md` — Teoria de sistemas multi-agente

**Se você quer implementar compaction:**
→ `03-nivel-3-advanced-architecture/04-server-side-compaction.md` — Guia prático de compaction

**Se você quer melhorar o harness:**
→ `05-harness-improvements.md` — Propostas de melhoria para o harness KODA

**Se você quer ver outros cases:**
→ `../../09-case-studies/` — Cases genéricos (não-KODA) como Order Processing e Fulfillment Workflow

---

## 📚 Referências & Leitura Adicional

### Dentro deste Programa
- `01-koda-architecture.md` — Arquitetura completa do KODA
- `02-customer-journey-flows.md` — Fluxos de jornada do cliente
- `03-feature-design-patterns.md` — Padrões de design de features
- `04-evaluation-rubrics-koda.md` — Rubricas de avaliação
- `05-harness-improvements.md` — Melhorias de harness
- `03-nivel-3-advanced-architecture/01-multi-agent-systems.md` — Multi-Agent Systems
- `03-nivel-3-advanced-architecture/04-server-side-compaction.md` — Compaction
- `03-nivel-3-advanced-architecture/05-harness-evolution.md` — Harness Evolution

### Conceitos Relacionados
- Generator/Evaluator Pattern (`02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md`)
- Sprint Contracts (`02-nivel-2-practical-patterns/02-sprint-contracts.md`)
- State Persistence (`03-nivel-3-advanced-architecture/02-state-persistence.md`)
- File-Based Coordination (`03-nivel-3-advanced-architecture/03-file-based-coordination.md`)

### Externo
- Redis Streams documentation
- Linux file locking (fcntl, O_CREAT|O_EXCL)
- Anthropic model pricing & capability comparison
- "Building Reliable Multi-Agent Systems" — Anthropic Engineering Blog

---

## 💭 Reflexão Final

> *"Escalar não é sobre fazer a mesma coisa mais rápido. É sobre fazer a coisa certa, do jeito certo, na hora certa — repetidamente, confiavelmente, sem perder a essência."*

A jornada do KODA de 100 para 10.000 conversas por dia não foi uma história sobre tecnologia. Foi uma história sobre **pensar diferente**.

O time não resolveu o problema adicionando mais servidores. Resolveu repensando fundamentalmente como o trabalho flui através do sistema. Separou responsabilidades. Criou checkpoints. Investiu em observabilidade. E, mais importante, **projetou para escala antes que a escala chegasse**.

Você pode estar em uma posição similar agora. Talvez seu sistema esteja funcionando bem com 100 conversas/dia. Talvez você esteja confortável. Mas a pergunta que Fernando se fez naquela segunda-feira é a mesma que você deve se fazer:

> **"Se o volume aumentar 100x amanhã, seu sistema aguenta?"**

Se a resposta for não — ou se você não souber a resposta — comece a projetar hoje.

Porque a escala não espera.

Ela simplesmente chega.

---

## 🎬 Próxima Cena

Feche este arquivo.

Pense no sistema que você está construindo ou mantendo agora.

Quantas "conversas por dia" ele processa? 10? 100? 1.000?

Agora imagine 100x esse volume.

O que quebraria primeiro? Onde estão seus gargalos? Quais das 10 lições deste case study se aplicam ao seu contexto?

Essa intuição — de olhar para um sistema e ver onde ele vai quebrar — é o que separa engenheiros que reagem a incidentes de engenheiros que previnem incidentes.

**Você agora está no segundo grupo.**

---

**Pronto para `03-feature-design-patterns.md`? Continue. O KODA te espera.**

---

*Escrito com base na experiência real de escala da equipe KODA.*
*Este case study é um documento vivo. Se você encontrar algo que não se aplica mais ou tem uma experiência de escala diferente para compartilhar, contribua.*

---

## 📋 Metadata

| Campo | Valor |
|---|---|
| **Arquivo** | case-study-02.md |
| **Nível** | 4 — KODA-Específico |
| **Tipo** | Case Study |
| **Tempo Estimado** | 120 minutos |
| **Status** | ✅ Completo |
| **Dependências** | Nível 4 Módulos 01-05 |
| **Pré-requisitos** | Nível 1, 2, 3 completos |
| **Data de Criação** | Maio 2026 |
| **Última Atualização** | Maio 2026 |
| **Issue** | [#23](https://github.com/pavani06/long-running-agents/issues/23) |
