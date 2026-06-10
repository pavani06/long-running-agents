---
title: "Persistência de Estado para Agentes Long-Running"
type: curriculum-lesson
nivel: 3
aliases: []
tags: [curriculo-conteudo, nivel-3, arquitetura-avancada]
relates-to: ["[[docs/canonical/serializable-pause-resume-state|Serializable Pause/Resume State]]"]
last_updated: 2026-06-10
---
# 💾 Persistência de Estado para Agentes Long-Running
## Como SQLite, JSON Files e Checkpointing Mantêm Agentes Vivos Através de Falhas

**Tempo Estimado:** 90 minutos
**Nível:** 3 - Arquitetura Avançada
**Pré-requisito:** Ter completado `02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md` e `03-nivel-3-advanced-architecture/01-multi-agent-systems.md`
**Status:** 🟢 CRITICO - Base para agentes que sobrevivem a reinicios, crashes e janelas de contexto longas
**Data de Criação:** Maio 2026

---

## 📖 Prólogo: A Conversa que o Crash Apagou

**Cenário Real: quarta-feira, 21h15.**

Pedro estava decidido.

Ele tinha passado 47 minutos conversando com o KODA no WhatsApp.

Era uma compra grande: whey protein, creatina, um pré-treino sem cafeína e um multivitamínico.

Tudo alinhado com o orçamento de R$ 380, a restrição de glúten e a preferência por produtos com boa avaliação.

```
21:02 KODA: Pedro, seu carrinho esta pronto. Resumo:
- Whey Isolado Baunilha 900g .......... R$ 189,90
- Creatina Monohidratada 300g ......... R$  59,90
- Pre-treino Sem Cafeina 150g ......... R$  79,90
- Multivitaminico 60 caps ............. R$  49,90
- Frete para Vila Mariana, SP ......... R$   0,00 (gratis acima de R$ 300)
Total: R$ 379,60

Posso gerar o link de pagamento?
21:03 Pedro: Pode. Finaliza ai.
```

O KODA gerou o link.

Pedro clicou.

A tela de pagamento abriu.

Ele digitou os dados do cartão.

E então o servidor do KODA reiniciou.

Foi uma reinicialização de rotina, agendada, silenciosa.

Só que o KODA estava rodando sem state persistence.

Tudo o que existia estava na memória do processo:

- O perfil do Pedro.
- As restrições alimentares.
- Os produtos comparados.
- O carrinho montado.
- O link de pagamento gerado.
- O fato de que Pedro estava a um clique de confirmar.

Quando o processo voltou, a memória estava vazia.

```
21:04 Pedro: Deu erro no pagamento. Tenta de novo?
21:04 KODA: Oi! Como posso te ajudar?
21:04 Pedro: Ue, eu tava finalizando a compra.
21:05 KODA: Claro! Me conta qual produto voce procura.
21:05 Pedro: Nao, eu ja escolhi. So quero pagar.
21:06 KODA: Entendi. Qual o seu objetivo de treino?
```

Pedro ficou irritado.

Depois, desconfiado.

Depois, foi embora.

Não porque o produto era ruim.

Não porque o preço era alto.

Não porque o atendimento foi frio.

Foi embora porque o KODA esqueceu tudo.

E esquecer, para um cliente que passou 47 minutos construindo uma decisão, dói mais do que um erro.

Dói porque parece descaso.

Este módulo ensina como evitar exatamente isso.

Ao final, você vai entender que persistência de estado não é uma feature de infraestrutura.

É uma promessa de respeito ao tempo do cliente.

---

## 🔗 Conexão com Nível 2 e Módulo Anterior

No Nível 2, você aprendeu o padrão Generator/Evaluator em `02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md`.

A ideia central era separar quem cria de quem avalia.

No módulo anterior, `01-multi-agent-systems.md`, você aprendeu a decompor uma conversa em Planner, Generator e Evaluator.

Cada agente recebia um contrato e escrevia artefatos em disco: `plan.json`, `generation.json`, `evaluation.json`.

Aqueles arquivos eram pontes entre agentes.

Mas havia uma pergunta que ficou no ar: o que acontece quando o processo morre?

Se o Planner escreveu `plan.json`, mas o servidor caiu antes do Generator ler, o que acontece quando o sistema volta?

Se o Generator produziu `generation.json`, mas o Evaluator nunca rodou, como o sistema sabe que precisa retomar?

Essas perguntas não são sobre agentes.

São sobre estado.

E estado que sobrevive ao processo é o assunto deste módulo.

| Módulo | Pergunta Principal | Resposta |
| --- | --- | --- |
| Nível 2 — Generator/Evaluator | A resposta gerada está correta? | Qualidade por verificação independente |
| Nível 3 — Multi-Agent | Qual agente faz o quê? | Qualidade por decomposição de responsabilidades |
| Nível 3 — State Persistence | O estado sobrevive a falhas? | Qualidade por durabilidade e recuperação |

State persistence é a camada que transforma agentes bem desenhados em agentes que sobrevivem à realidade.

A realidade inclui:

1. Reinicializações de servidor.
2. Timeouts de API.
3. Picos de latência.
4. Conversas que duram horas.
5. Clientes que voltam dias depois.
6. Deploys que acontecem no meio de uma jornada.

Sem state persistence, cada um desses eventos apaga o progresso do cliente.

Com state persistence, cada um desses eventos vira apenas uma pausa.

---

## 🧠 Por Que Agentes Precisam de Persistência de Estado

### O Problema da Memória Volátil

Agentes de IA têm dois tipos de memória:

1. **Memória de contexto (context window):** o que o modelo "vê" na chamada atual. Limitada, cara e volátil. Quando a chamada termina, desaparece.

2. **Memória externa (state persistence):** o que está salvo em disco, banco ou cache. Barata, durável e recuperável. Sobrevive a qualquer evento.

A maioria dos protótipos de agente usa apenas a memória de contexto.

Isso funciona em demos de 5 minutos.

Falha em produção.

```
┌─────────────────────────────────────────────────────────────────────┐
│                     Jornada Sem Persistência                         │
│                                                                     │
│  Minuto  0: ████████░░░░░░░░░░░░░░░░  (contexto fresco)              │
│  Minuto 15: ████████████████░░░░░░░░  (coletando preferências)       │
│  Minuto 30: ████████████████████████  (comparando produtos)          │
│  Minuto 45: ████████████████████████  (montando carrinho)            │
│  Minuto 46: ════════════════════════  (SERVIDOR REINICIA)            │
│  Minuto 47: ░░░░░░░░░░░░░░░░░░░░░░░░  (memória zerada)               │
│                                                                     │
│  Resultado: 47 minutos de conversa perdidos.                         │
│             Cliente precisa recomeçar do zero.                       │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                     Jornada Com Persistência                         │
│                                                                     │
│  Minuto  0: ████████░░░░░░░░░░░░░░░░  ──► save: session_start.json   │
│  Minuto 15: ████████████████░░░░░░░░  ──► save: preferences.json     │
│  Minuto 30: ████████████████████████  ──► save: comparison.json      │
│  Minuto 45: ████████████████████████  ──► save: cart.json            │
│  Minuto 46: ════════════════════════  (SERVIDOR REINICIA)            │
│  Minuto 47: ████████████████████████  ◄── load: cart.json            │
│                                                                     │
│  Resultado: Conversa retoma exatamente de onde parou.                │
│             Cliente não percebe a reinicialização.                   │
└─────────────────────────────────────────────────────────────────────┘
```

### As Quatro Falhas que State Persistence Previne

Toda arquitetura de agentes enfrenta quatro categorias de falha.

Cada uma delas é resolvida por uma dimensão diferente de state persistence.

| Categoria de Falha | Exemplo Real | Sem Persistência | Com Persistência |
| --- | --- | --- | --- |
| **Crash de processo** | Servidor reinicia durante conversa | Conversa inteira perdida. Cliente vê KODA "esquecer" tudo. | Estado recarregado do disco. KODA retoma com "Voce estava finalizando a compra, certo?" |
| **Timeout de LLM** | API do Claude retorna erro 529 após 60s | Turno atual perdido. Nenhum rastro do que estava sendo gerado. | Última geração salva como `generation_partial.json`. Sistema tenta novamente ou usa fallback. |
| **Janela de contexto esgotada** | Conversa de 3h excede 200K tokens do Sonnet | Informações antigas somem. KODA esquece alergias do início. | Dados críticos externalizados em `customer_profile.json`. Context window recebe apenas resumo + estado relevante. |
| **Retomada entre sessões** | Cliente volta 3 dias depois para continuar compra | KODA não tem ideia de quem é o cliente nem do que foi discutido. | `session_state.json` recarrega perfil, carrinho abandonado e última etapa da jornada. |

### O Custo de Não Persistir

Cada falha sem persistência tem um custo mensurável para o KODA.

```
Cenário: 1000 conversas por dia, 5% de taxa de crash/evento por conversa.

Sem state persistence:
  50 conversas perdidas por dia
  ~30 clientes frustrados que abandonam
  ~15 vendas perdidas por dia
  ~R$ 2.850/dia em receita perdida (ticket médio R$ 190)
  ~R$ 85.500/mês

Com state persistence:
  50 conversas pausadas e retomadas
  ~3 clientes percebem lentidão (não perda)
  ~1 venda perdida por dia (clientes que desistem por outros motivos)
  ~R$ 190/dia em receita perdida
  ~R$ 5.700/mês

Economia mensal: ~R$ 79.800
```

Persistência de estado não é um luxo arquitetural.

É uma decisão de negócio com ROI direto.

---

## 🗄️ Backends de Persistência: SQLite vs JSON vs Redis

A primeira decisão de arquitetura ao implementar state persistence é: onde guardar o estado?

Não existe resposta universal.

Cada backend resolve um conjunto diferente de trade-offs.

### Visão Geral dos Três Backends

| Dimensão | SQLite | JSON Files | Redis |
| --- | --- | --- | --- |
| **Modelo de dados** | Relacional, schemas, queries SQL | Documentos, schemaless, hierarchical | Key-value, estruturas de dados (hash, list, set, stream) |
| **Persistência** | Durável por padrão via journaling; WAL mode é opcional e melhora concorrência | Durável se escrita atômica (write-then-rename) | Configurável (RDB snapshots + AOF log) |
| **Latência de leitura** | < 1ms para lookup por índice | < 1ms para arquivo em cache do SO | < 1ms (sub-millisecond) |
| **Latência de escrita** | ~1-5ms (com fsync) | ~1-5ms (depende do disco) | < 1ms |
| **Concorrência** | Single-writer (readers ok com WAL) | Single-writer (file lock necessário) | Multi-writer nativo |
| **Complexidade operacional** | Baixa (arquivo único, sem servidor) | Mínima (apenas filesystem) | Média (servidor separado, config de persistência) |
| **Query power** | SQL completo, joins, aggregations | Nenhum (precisa ler e parse completo) | Comandos por estrutura de dados |
| **Schema enforcement** | Forte (DDL, constraints, foreign keys) | Nenhum (confia no writer) | Nenhum (confia no writer) |
| **Portabilidade** | Arquivo binário portável | Arquivo texto portável | Dependente de servidor Redis |
| **Tamanho máximo prático** | ~10 GB por arquivo | ~100 MB por arquivo (carga completa em RAM) | Limitado pela RAM disponível |
| **Backup** | `.backup` command ou API; cópia direta requer DB quiescente ou incluir `-wal` e `-shm` | Copia o diretório | RDB snapshot ou AOF replay |
| **Audit trail** | Possível com triggers e tabela de log | Natural (arquivos são o log) | Possível com Redis Streams |
| **Melhor para** | Estado estruturado, queries complexas, relações entre entidades, dados que crescem | Prototipagem, traces, estado simples, pipelines de arquivo entre agentes, auditoria humana | Cache, sessões de curta duração, filas, estado quente que precisa de latência mínima |

### SQLite: O Banco que Mora no Arquivo

SQLite é um banco de dados relacional completo que vive em um único arquivo.

Sem servidor.

Sem configuração.

Sem dependência de rede.

```sql
-- Esquema de estado para uma sessão KODA
CREATE TABLE sessions (
    session_id      TEXT PRIMARY KEY,
    customer_id     TEXT NOT NULL,
    channel         TEXT NOT NULL DEFAULT 'whatsapp',
    status          TEXT NOT NULL DEFAULT 'active',
    created_at      TEXT NOT NULL,
    updated_at      TEXT NOT NULL,
    metadata_json   TEXT
);

CREATE TABLE conversation_turns (
    turn_id         INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id      TEXT NOT NULL REFERENCES sessions(session_id),
    turn_number     INTEGER NOT NULL,
    role            TEXT NOT NULL CHECK (role IN ('customer', 'koda', 'system')),
    content         TEXT NOT NULL,
    agent_phase     TEXT,
    created_at      TEXT NOT NULL,
    token_count     INTEGER
);

CREATE TABLE customer_profile (
    customer_id     TEXT PRIMARY KEY,
    name            TEXT,
    dietary_restrictions TEXT,
    preferences_json    TEXT,
    budget_range_json   TEXT,
    created_at      TEXT NOT NULL,
    updated_at      TEXT NOT NULL
);

CREATE TABLE cart_state (
    cart_id         TEXT PRIMARY KEY,
    session_id      TEXT NOT NULL REFERENCES sessions(session_id),
    customer_id     TEXT NOT NULL,
    items_json      TEXT NOT NULL,
    total_brl       REAL NOT NULL,
    status          TEXT NOT NULL DEFAULT 'draft',
    payment_link    TEXT,
    created_at      TEXT NOT NULL,
    updated_at      TEXT NOT NULL
);

CREATE TABLE checkpoints (
    checkpoint_id   TEXT PRIMARY KEY,
    session_id      TEXT NOT NULL REFERENCES sessions(session_id),
    phase           TEXT NOT NULL,
    state_snapshot  TEXT NOT NULL,
    created_at      TEXT NOT NULL
);

CREATE INDEX idx_turns_session ON conversation_turns(session_id, turn_number);
CREATE INDEX idx_cart_session ON cart_state(session_id);
CREATE INDEX idx_checkpoints_session ON checkpoints(session_id, created_at);
```

Vantagens do SQLite para KODA:

1. Schema forte previne corrupção silenciosa de estado. Com tabelas `STRICT` ou constraints `CHECK(typeof(total_brl) = 'real')`, o SQLite rejeita valores de tipo incorreto.

2. Queries SQL permitem perguntas como "quantas sessões estão com carrinho em draft há mais de 30 minutos?" sem carregar todos os arquivos em memória.

3. Transações ACID garantem que um checkpoint nunca fique pela metade. Se o servidor cair no meio de um `BEGIN TRANSACTION`, o SQLite faz rollback automático.

4. WAL mode permite que múltiplos readers leiam enquanto um writer escreve — ideal para o padrão Planner (write), Generator (read), Evaluator (read) em paralelo.

5. Um arquivo único simplifica backup, restauração e migração entre ambientes.

Cuidados:

1. Um único writer por vez. Se dois agentes tentarem escrever ao mesmo tempo, um recebe `SQLITE_BUSY`. Resolve-se com fila ou retry com backoff.

2. O arquivo cresce. Precisa de `VACUUM` periódico para recuperar espaço após deleções.

3. Concorrência de escrita em alto volume (>100 writes/segundo) pode saturar. Para KODA, isso raramente é problema porque o throughput de conversas é baixo comparado a sistemas web.

### JSON Files: Simplicidade que Audita

JSON files são a escolha natural quando você está aprendendo ou prototipando.

Eles são a base do file-based coordination que vimos no módulo anterior.

```
state/
└── sessions/
    └── wa_2026_05_26_pedro/
        ├── session_start.json
        ├── customer_profile.json
        ├── plan.json
        ├── generation.json
        ├── evaluation.json
        ├── cart.json
        ├── payment_link.json
        ├── checkpoint_turn_008.json
        ├── checkpoint_turn_015.json
        └── checkpoint_turn_022.json
```

Vantagens do JSON para KODA:

1. Legibilidade humana. Qualquer pessoa da equipe pode abrir `cart.json` e entender exatamente o que está acontecendo. Isso reduz drasticamente o tempo de debug.

2. Audit trail natural. Cada arquivo é um ponto no tempo. Você pode reconstruir toda a jornada do cliente lendo os arquivos em ordem.

3. Versionamento amigável. `git diff` entre versões de um arquivo JSON mostra exatamente o que mudou.

4. Zero dependências. Não precisa instalar banco, não precisa de servidor, não precisa de driver. Só `fs.writeFileSync` e `fs.readFileSync`.

5. Schema version pode ser embedado no próprio JSON com `"schema_version": "1.0"`, permitindo migração explícita quando a estrutura muda.

Cuidados:

1. Escrita atômica é essencial. Se você escrever direto no arquivo e o processo cair no meio, o arquivo fica corrompido. Use write-temp-then-rename:

```python
import json, os, tempfile

def atomic_write_json(path, data):
    tmp = tempfile.NamedTemporaryFile(
        mode='w',
        dir=os.path.dirname(path),
        delete=False,
        suffix='.tmp',
        encoding='utf-8'
    )
    try:
        json.dump(data, tmp, ensure_ascii=False, indent=2)
        tmp.flush()
        os.fsync(tmp.fileno())
    finally:
        tmp.close()
    os.rename(tmp.name, path)
```

2. Leitura requer parse completo do arquivo. Para arquivos acima de 10 MB, isso fica lento. Mantenha arquivos pequenos (<1 MB) e particione estado por domínio.

3. Sem queries. Para saber "quantos carrinhos estão abertos", você precisa ler todos os diretórios de sessão e parse cada `cart.json`. SQLite resolve isso com um `SELECT COUNT(*)`.

4. Sem schema enforcement. Se o Generator escrever `"total_brl": "cento e noventa"` em vez de `189.90`, nada impede. Validação precisa ser explícita no código.

### Redis: Velocidade para Estado Quente

Redis é um data structure server em memória.

Ele é a escolha certa quando latência importa mais que durabilidade — ou quando você configura persistência adequadamente.

```
┌───────────────────────────────────────────────────────────┐
│                     Redis no KODA                          │
│                                                           │
│  sessao:wa_pedro:profile      → hash com perfil            │
│  sessao:wa_pedro:cart         → hash com itens e total     │
│  sessao:wa_pedro:turns        → list com últimos N turns   │
│  sessao:wa_pedro:checkpoint   → string com JSON snapshot   │
│  cache:catalog:2026-05-26     → hash com catálogo do dia   │
│  queue:generator:tasks        → list com tarefas pendentes  │
│  events:payment:approved      → stream de eventos           │
└───────────────────────────────────────────────────────────┘
```

Vantagens do Redis para KODA:

1. Latência sub-millisecond. Ideal para estado que é lido e escrito em todo turno de conversa, como o perfil do cliente e o resumo da sessão.

2. Estruturas de dados nativas. Hash para perfil, list para histórico de turns, sorted set para ordenar checkpoints por timestamp. Isso reduz código de serialização.

3. TTL (time-to-live) nativo. Sessões podem expirar automaticamente: `EXPIRE sessao:wa_pedro:cart 3600` remove o carrinho após 1 hora sem atividade.

4. Pub/sub para eventos. Quando o pagamento é aprovado, um evento é publicado e o Fulfillment Agent reage imediatamente.

5. Atomicidade em operações simples. `HINCRBY sessao:wa_pedro:cart item_count 1` é atômico, sem preocupação com race condition.

Cuidados:

1. Persistência não é o default. Redis em modo puro é volátil — reiniciou, perdeu. É preciso configurar RDB snapshots (a cada N writes) e AOF (append-only file) para durabilidade.

2. RAM é cara e limitada. Estado de milhares de sessões simultâneas pode consumir gigabytes rapidamente. Estratégia de TTL e eviction é mandatória.

3. Servidor separado. Adiciona complexidade operacional: precisa monitorar, fazer backup, configurar replica para HA.

4. Sem schema. Assim como JSON files, Redis não valida estrutura. Dados malformados entram silenciosamente.

### Como Escolher o Backend

A escolha não é binária.

Sistemas maduros usam camadas:

```
┌────────────────────────────────────────────────────────────┐
│                 Arquitetura de Persistência do KODA         │
│                                                            │
│  CAMADA 1: Redis (estado quente)                            │
│  ├─ Perfil do cliente em hash                               │
│  ├─ Carrinho atual                                          │
│  ├─ Últimos N turns da conversa                             │
│  └─ TTL: 2 horas de inatividade                             │
│                                                            │
│  CAMADA 2: SQLite (estado durável)                          │
│  ├─ Histórico completo de conversas                         │
│  ├─ Checkpoints de jornada                                  │
│  ├─ Perfis permanentes de cliente                           │
│  └─ Catálogo snapshotado do dia                             │
│                                                            │
│  CAMADA 3: JSON files (audit trail)                         │
│  ├─ Traces de cada turno para debug                         │
│  ├─ Artefatos de Planner/Generator/Evaluator                │
│  └─ Log de decisões para revisão humana                     │
└────────────────────────────────────────────────────────────┘
```

Regra prática:

1. **Comece com JSON files.** Você vai errar o schema várias vezes. JSON perdoa. Quando o schema estabilizar, migre as partes quentes.

2. **Adicione Redis para estado quente.** Perfil do cliente, carrinho, últimos turns. Tudo que é lido em todo ciclo de conversa.

3. **Migre para SQLite quando precisar de queries.** "Quantos clientes com restrição de lactose têm carrinho acima de R$ 200?" é trivial no SQLite e impossível (eficientemente) em JSON files.

4. **Mantenha JSON files para audit trail.** Mesmo quando o estado operacional está no SQLite, ter arquivos JSON legíveis salva horas de debug.

---

## 🔄 Padrões de Checkpointing

Estado não basta ser persistido.

Ele precisa ser persistido no momento certo, com a granularidade certa, de forma que permita recuperação sem corromper a jornada.

Isso é o que padrões de checkpointing resolvem.

### O Que é um Checkpoint

Um checkpoint é uma fotografia do estado do agente em um ponto seguro da jornada.

Não é o estado completo de toda a conversa.

É o subconjunto de estado necessário para retomar dali em diante.

```
Checkpoint no KODA:

{
  "checkpoint_id": "ckpt_pedro_022",
  "session_id": "wa_2026_05_26_pedro",
  "turn_number": 22,
  "phase": "cart_ready_for_payment",
  "snapshot": {
    "customer": {
      "id": "cust_pedro_7391",
      "name": "Pedro",
      "dietary_restrictions": ["gluten"],
      "budget_brl": 380
    },
    "cart": {
      "items": [
        {"sku": "WHEY-ISO-BAUN-900", "qty": 1, "price": 189.90},
        {"sku": "CREA-MONO-300", "qty": 1, "price": 59.90},
        {"sku": "PRE-NOCAF-150", "qty": 1, "price": 79.90},
        {"sku": "MULTI-VIT-60", "qty": 1, "price": 49.90}
      ],
      "total_brl": 379.60,
      "shipping_city": "Sao Paulo",
      "shipping_neighborhood": "Vila Mariana"
    },
    "last_action": "payment_link_generated",
    "payment_link": "https://pay.koda.app/ord_99281",
    "next_expected_action": "payment_confirmation"
  },
  "created_at": "2026-05-26T21:03:12-03:00"
}
```

### Padrão 1: Snapshot Completo

O snapshot completo salva todo o estado relevante em um único ponto.

É o padrão mais simples de entender.

Também é o mais seguro para recuperação, porque o estado é autocontido.

```
Fluxo com Snapshot:

Turno N:
  ┌──────────┐
  │ Cliente  │ mensagem
  └────┬─────┘
       │
       ▼
  ┌──────────┐
  │ Planner  │
  └────┬─────┘
       │ plan.json
       ▼
  ┌──────────┐
  │ Generator│
  └────┬─────┘
       │ generation.json
       ▼
  ┌──────────┐
  │ Evaluator│ ──► Se approved: SNAPSHOT COMPLETO
  └──────────┘     ├─ customer_profile
                   ├─ cart_state
                   ├─ last_turn
                   └─ next_phase
```

**Quando usar:** jornadas críticas onde perder estado é inaceitável. Fechamento de pedido, pagamento, confirmação de entrega.

**Vantagens:**

1. Recuperação trivial: carrega o snapshot e continua.
2. Sem dependência de snapshots anteriores.
3. Ideal para retomada entre sessões (cliente volta dias depois).

**Desvantagens:**

1. Custo de escrita proporcional ao tamanho do estado.
2. Se o estado é grande, cada snapshot consome I/O significativo.
3. Snapshots frequentes com estado grande geram ruído no audit trail.

**Implementação:**

```python
import json
from datetime import datetime, timezone
from pathlib import Path

def create_full_snapshot(session_id, customer, cart, phase, last_action):
    checkpoint = {
        "checkpoint_id": f"ckpt_{session_id}_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
        "session_id": session_id,
        "phase": phase,
        "snapshot": {
            "customer": customer,
            "cart": cart,
            "last_action": last_action
        },
        "created_at": datetime.now(timezone.utc).isoformat()
    }

    path = Path(f"state/sessions/{session_id}/checkpoints/{checkpoint['checkpoint_id']}.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    atomic_write_json(path, checkpoint)

    return checkpoint["checkpoint_id"]

def restore_from_snapshot(session_id):
    checkpoint_dir = Path(f"state/sessions/{session_id}/checkpoints")
    if not checkpoint_dir.exists():
        return None

    # Encontra o checkpoint mais recente
    snapshots = sorted(checkpoint_dir.glob("ckpt_*.json"), reverse=True)
    if not snapshots:
        return None

    with open(snapshots[0]) as f:
        return json.load(f)
```

### Padrão 2: Incremental (Delta)

O checkpoint incremental salva apenas o que mudou desde o último checkpoint.

Ele reduz I/O e armazenamento quando o estado é grande mas muda pouco entre turnos.

```
Fluxo com Checkpoint Incremental:

Turno N:   checkpoint_base.json  (snapshot completo)
           ├─ customer: {name: "Pedro", restrictions: ["gluten"]}
           └─ cart: {items: [], total: 0}

Turno N+1: checkpoint_delta_01.json (apenas mudanças)
           └─ cart: {items: [{sku: "WHEY-ISO", qty: 1}], total: 189.90}

Turno N+2: checkpoint_delta_02.json (apenas mudanças)
           └─ cart: {items: [{sku: "WHEY-ISO", qty: 1}, {sku: "CREA", qty: 1}], total: 249.80}

Turno N+3: checkpoint_delta_03.json (apenas mudanças)
           └─ cart: {items: [...3 items], total: 329.70}
```

Para restaurar o estado no turno N+3, você aplica:

```
estado_atual = checkpoint_base + delta_01 + delta_02 + delta_03
```

**Quando usar:** jornadas com muitos turns onde o estado cresce progressivamente e escrever snapshots completos seria desperdício.

**Vantagens:**

1. Escrita mínima por turno: apenas o que mudou.
2. Audit trail mostra exatamente o que mudou em cada passo.
3. Ideal para debugging: "o que aconteceu entre o turno 15 e o 16?"

**Desvantagens:**

1. Recuperação mais lenta: precisa aplicar N deltas para chegar ao estado atual.
2. Se um delta corrompe, todos os deltas seguintes são afetados.
3. Snapshots base precisam existir periodicamente para limitar a cadeia de deltas.

**Implementação:**

```python
def create_delta_checkpoint(session_id, base_checkpoint_id, changes):
    checkpoint = {
        "checkpoint_id": f"delta_{session_id}_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
        "session_id": session_id,
        "type": "delta",
        "base_checkpoint_id": base_checkpoint_id,
        "changes": changes,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    path = Path(f"state/sessions/{session_id}/checkpoints/{checkpoint['checkpoint_id']}.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    atomic_write_json(path, checkpoint)
    return checkpoint["checkpoint_id"]

def compute_delta(previous_state, current_state):
    """Calcula apenas os campos que mudaram entre dois snapshots."""
    delta = {}
    all_keys = set(previous_state.keys()) | set(current_state.keys())

    for key in all_keys:
        prev_val = previous_state.get(key)
        curr_val = current_state.get(key)
        if prev_val != curr_val:
            delta[key] = curr_val

    return delta

def restore_from_deltas(session_id):
    checkpoint_dir = Path(f"state/sessions/{session_id}/checkpoints")
    all_checkpoints = sorted(checkpoint_dir.glob("*.json"))

    if not all_checkpoints:
        return None

    # Carrega o snapshot base (primeiro full)
    with open(all_checkpoints[0]) as f:
        state = json.load(f)["snapshot"]

    # Aplica deltas em ordem
    for cp_path in all_checkpoints[1:]:
        with open(cp_path) as f:
            cp = json.load(f)
        if cp.get("type") == "delta":
            for key, value in cp["changes"].items():
                state[key] = value

    return state
```

### Padrão 3: Híbrido (Full + Delta)

O padrão híbrido combina snapshots completos periódicos com deltas entre eles.

É o padrão mais usado em produção porque equilibra segurança de recuperação com eficiência de I/O.

```
Estratégia Híbrida:

Turno  1: ████████ FULL SNAPSHOT (base)
Turno  5: ░░░░ delta
Turno 10: ░░░░ delta
Turno 15: ████████ FULL SNAPSHOT (consolidado)
Turno 20: ░░░░ delta
Turno 25: ░░░░ delta
Turno 30: ████████ FULL SNAPSHOT (consolidado)
...

Regra: full snapshot a cada 10 turns ou em pontos críticos da jornada.
       delta nos turns intermediários.
```

**Regras para o híbrido:**

1. Snapshot completo no início de cada fase da jornada (descoberta → recomendação → carrinho → pagamento → fulfillment).
2. Snapshot completo a cada N turns (N=10 é um bom ponto de partida).
3. Delta em todos os outros turns.
4. Após restaurar, se a cadeia de deltas for maior que N, consolide em um novo snapshot completo.

**Quando usar:** produção. Sempre.

### Diagrama da State Machine de Checkpointing

```
                              ┌─────────────┐
                              │   INÍCIO    │
                              │  da sessão  │
                              └──────┬──────┘
                                     │
                                     ▼
                              ┌─────────────┐
                        ┌────►│ FULL        │
                        │     │ SNAPSHOT    │
                        │     └──────┬──────┘
                        │            │
                        │            ▼
                        │     ┌─────────────┐
                        │     │ TURNO       │◄──────────┐
                        │     │ (mensagem)  │           │
                        │     └──────┬──────┘           │
                        │            │                   │
                        │            ▼                   │
                        │     ┌─────────────┐           │
                        │     │ DELTA       │           │
                        │     │ CHECKPOINT  │           │
                        │     └──────┬──────┘           │
                        │            │                   │
                        │     ┌──────┴──────┐           │
                        │     │             │           │
                        │     ▼             ▼           │
                        │  ┌────────┐  ┌─────────┐     │
                        │  │turno < │  │turno >= │     │
                        │  │   N    │  │   N     │     │
                        │  └───┬────┘  └────┬────┘     │
                        │      │            │           │
                        │      │            ▼           │
                        │      │     ┌─────────────┐    │
                        │      │     │ CONSOLIDA   │    │
                        │      │     │ FULL SNAP   │────┘
                        │      │     └─────────────┘
                        │      │
                        │      ▼
                        │  ┌─────────────┐
                        │  │ FASE        │
                        │  │ CRÍTICA?    │
                        │  └──────┬──────┘
                        │         │
                        │    ┌────┴────┐
                        │    │ sim     │ não
                        │    ▼         │
                        │  ┌─────────┐ │
                        │  │ FORÇA   │ │
                        │  │ FULL    │ │
                        │  │ SNAP    │─┘
                        │  └─────────┘
                        │
                        │     ┌─────────────┐
                        └─────┤ RECUPERAÇÃO │
                              │ (se crash)  │
                              └──────┬──────┘
                                     │
                                     ▼
                              ┌─────────────┐
                              │ CARREGA     │
                              │ ÚLTIMO FULL │
                              │ + DELTAS    │
                              └──────┬──────┘
                                     │
                                     ▼
                              ┌─────────────┐
                              │ RETOMA      │
                              │ JORNADA     │
                              └─────────────┘
```

---

## 🔧 Estratégias de Recuperação

Checkpoints salvam estado.

Estratégias de recuperação definem o que fazer com esse estado quando algo dá errado.

### Estratégia 1: Rollback para Último Checkpoint Seguro

A estratégia mais simples: quando algo falha, volta para o último checkpoint confirmado e tenta de novo.

```
┌──────────────────────────────────────────────────────────────┐
│                   ROLLBACK                                   │
│                                                              │
│  Turno 20: Evaluator aprova ──► checkpoint_20 salvo           │
│  Turno 21: Generator produz ──► API do Claude timeout         │
│                                                              │
│  Ação: ROLLBACK para checkpoint_20                            │
│         KODA: "Tive uma pequena pausa. Voce estava            │
│                finalizando a compra, certo?"                   │
│         Re-executa turno 21 com estado restaurado             │
└──────────────────────────────────────────────────────────────┘
```

**Quando usar:** falhas transientes. Timeout de API, erro de rede, crash de processo.

**Implementação:**

```python
def rollback_to_checkpoint(session_id, checkpoint_id=None):
    if checkpoint_id:
        # Rollback para checkpoint específico
        cp_path = Path(f"state/sessions/{session_id}/checkpoints/{checkpoint_id}.json")
        with open(cp_path) as f:
            return json.load(f)["snapshot"]
    else:
        # Rollback para o último checkpoint seguro
        return restore_from_snapshot(session_id)

def handle_turn_with_rollback(session_id, message, max_retries=3):
    for attempt in range(max_retries):
        try:
            state = restore_from_snapshot(session_id)
            response = process_turn(state, message)
            return response
        except (TimeoutError, ConnectionError) as e:
            if attempt == max_retries - 1:
                # Último attempt: mensagem de fallback
                return "Tive uma instabilidade. Voce pode repetir a ultima mensagem?"
            # Rollback implícito: o loop recarrega estado do disco
            continue
```

### Estratégia 2: Replay Determinístico

Em vez de voltar atrás, o replay re-executa a sequência de ações desde o checkpoint, assumindo que as ações são determinísticas e o resultado será consistente.

```
┌──────────────────────────────────────────────────────────────┐
│                   REPLAY                                     │
│                                                              │
│  Checkpoint 15 salvo                                         │
│  Turnos 16-22 executados normalmente                          │
│  Servidor reinicia                                           │
│                                                              │
│  Ação: REPLAY dos turnos 16-22                                │
│         Cada turno re-executa:                                │
│         - Planner lê estado do turno N-1                      │
│         - Generator produz com mesmo input                    │
│         - Evaluator valida com mesmos critérios               │
│         Estado converge para o mesmo ponto                   │
│                                                              │
│  KODA no turno 23: "Voce estava finalizando a compra..."     │
└──────────────────────────────────────────────────────────────┘
```

**Quando usar:** sistemas onde as ações são determinísticas (mesmo input = mesmo output). Funciona bem com LLMs se o temperature for 0.

**Implementação:**

```python
def replay_turns(session_id, from_turn, to_turn):
    checkpoint = restore_from_snapshot(session_id)
    state = checkpoint["snapshot"]

    turns_dir = Path(f"state/sessions/{session_id}/turns")
    turn_files = sorted(turns_dir.glob("turn_*.json"))

    for turn_file in turn_files:
        with open(turn_file) as f:
            turn = json.load(f)

        turn_number = turn["turn_number"]
        if turn_number < from_turn or turn_number > to_turn:
            continue

        # Re-executa o turno com o estado acumulado
        result = process_turn(state, turn["customer_message"])
        state = result["new_state"]

        # Escreve o resultado do replay
        replay_path = Path(f"state/sessions/{session_id}/replay/turn_{turn_number}.json")
        replay_path.parent.mkdir(parents=True, exist_ok=True)
        atomic_write_json(replay_path, result)

    return state
```

### Estratégia 3: Compensação (Saga Pattern)

Quando uma operação que altera estado externo falha no meio, a compensação desfaz os passos já concluídos.

Este padrão é crítico para KODA porque envolve sistemas externos: estoque, pagamento, transportadora.

```
┌──────────────────────────────────────────────────────────────┐
│                   COMPENSAÇÃO (SAGA)                         │
│                                                              │
│  Passo 1: Reservar estoque .......... ✅ Sucesso              │
│  Passo 2: Gerar link de pagamento ... ✅ Sucesso              │
│  Passo 3: Aplicar cupom de desconto . ❌ Falha               │
│                                                              │
│  Compensação:                                                │
│    Desfaz Passo 2: Cancela link de pagamento                 │
│    Desfaz Passo 1: Libera estoque reservado                  │
│                                                              │
│  Estado volta ao ponto antes da tentativa de compra.          │
│  KODA: "Tive um problema com o cupom. Ainda posso            │
│         finalizar sem o desconto, ou prefere esperar?"        │
└──────────────────────────────────────────────────────────────┘
```

**Implementação:**

```python
class SagaCheckout:
    def __init__(self, session_id):
        self.session_id = session_id
        self.completed_steps = []
        self.compensations = []

    def execute(self, cart, coupon_code=None):
        try:
            # Passo 1: Reservar estoque
            inventory_result = self._reserve_inventory(cart["items"])
            self.completed_steps.append("inventory_reserved")
            self.compensations.append(lambda: self._release_inventory(cart["items"]))

            # Passo 2: Gerar link de pagamento
            payment_link = self._generate_payment_link(cart["total_brl"])
            self.completed_steps.append("payment_link_generated")
            self.compensations.append(lambda: self._cancel_payment_link(payment_link))

            # Passo 3: Aplicar cupom (pode falhar)
            if coupon_code:
                final_total = self._apply_coupon(coupon_code, cart["total_brl"])
                self.completed_steps.append("coupon_applied")

            return {"status": "success", "payment_link": payment_link}

        except Exception as e:
            # Compensação: desfaz na ordem inversa
            for compensate in reversed(self.compensations):
                try:
                    compensate()
                except Exception as comp_error:
                    # Loga mas não interrompe a compensação
                    print(f"Compensation warning: {comp_error}")

            return {"status": "rolled_back", "error": str(e), "completed_steps": self.completed_steps}
```

### Como Escolher a Estratégia de Recuperação

| Situação | Estratégia | Por quê |
| --- | --- | --- |
| Timeout de API LLM | Rollback | Simples, imediato. Estado não foi alterado, só a tentativa falhou. |
| Crash de processo entre turns | Rollback | Último checkpoint tem o estado consistente. Re-executa o turno. |
| Crash durante deploy | Replay | Estado pode divergir. Replay garante convergência determinística. |
| Falha em sistema externo (pagamento) | Compensação | Mundo real foi alterado. Rollback de código não desfaz pagamento. |
| Corrupção de estado detectada | Rollback para checkpoint específico | Isola o dano. Volta ao último ponto confirmadamente bom. |
| Cliente volta após 3 dias | Replay + Snapshot | Estado entre sessões precisa ser reconstruído. Snapshot base + replay dos turns finais. |

---

## 🎓 Aplicação KODA: Customer State Machine

Agora vamos aplicar state persistence a uma jornada completa do KODA.

O que era uma conversa linear vira uma state machine com fases, transições e checkpoints.

### A State Machine da Jornada de Compra

```
                        ┌──────────────┐
                        │   WELCOME    │
                        │ (saudação)   │
                        └──────┬───────┘
                               │ cliente responde
                               ▼
                        ┌──────────────┐
                        │  DISCOVERY   │
                        │ (coleta de   │
                        │  perfil)     │
                        └──────┬───────┘
                               │ perfil completo
                               ▼
                        ┌──────────────┐
              ┌────────►│RECOMMENDATION│◄─────────┐
              │         │ (comparação  │          │
              │         │  de opções)  │          │
              │         └──────┬───────┘          │
              │                │                   │
              │         ┌──────┴──────┐           │
              │         │             │           │
              │         ▼             ▼           │
              │   ┌──────────┐  ┌──────────┐     │
              │   │ cliente  │  │ cliente  │     │
              │   │ escolhe  │  │ quer ver │     │
              │   │ produto  │  │ mais     │     │
              │   └────┬─────┘  └────┬─────┘     │
              │        │             │           │
              │        │             └───────────┘
              │        │
              │        ▼
              │   ┌──────────────┐
              │   │    CART      │
              │   │ (montagem do │
              │   │  carrinho)   │
              │   └──────┬───────┘
              │          │ carrinho pronto
              │          ▼
              │   ┌──────────────┐
              │   │   PAYMENT    │
              │   │ (pagamento)  │
              │   └──────┬───────┘
              │          │
              │    ┌─────┴─────┐
              │    │           │
              │    ▼           ▼
              │ ┌──────┐  ┌──────────┐
              │ │ pago │  │ timeout  │──► EXPIRA sessão
              │ └──┬───┘  │ 2 horas  │    (TTL Redis + checkpoint SQLite)
              │    │      └──────────┘
              │    ▼
              │ ┌──────────────┐
              │ │  FULFILLMENT │
              │ │ (pós-venda)  │
              │ └──────┬───────┘
              │        │ entregue
              │        ▼
              │ ┌──────────────┐
              │ │  FOLLOW-UP   │
              │ │ (14 dias)    │
              │ └──────────────┘
              │
              └───── (cliente insatisfeito: volta para RECOMMENDATION)
```

### Persistindo Cada Fase

Cada fase da state machine tem um contrato de persistência específico.

| Fase | O que Persistir | Backend | Checkpoint Strategy | TTL |
| --- | --- | --- | --- | --- |
| **WELCOME** | `session_id`, `customer_id`, `channel`, `started_at` | Redis + SQLite | Snapshot ao criar sessão | 24h |
| **DISCOVERY** | `customer_profile.json`: restrições, objetivos, orçamento, preferências | Redis (hash) + JSON file | Delta a cada nova informação | Até fim da sessão |
| **RECOMMENDATION** | `comparison.json`: produtos considerados, scores, justificativas | JSON file | Full snapshot ao aprovar recomendação | Até fim da sessão |
| **CART** | `cart.json`: itens, quantidades, preços, frete, total | Redis (hash) + SQLite | Full snapshot ao confirmar carrinho | 2h após último update |
| **PAYMENT** | `payment.json`: link, status, transaction_id | SQLite (transação) | Full snapshot ao gerar link + ao confirmar pagamento | 1h após pagamento |
| **FULFILLMENT** | `fulfillment.json`: tracking, status, eventos de entrega | SQLite | Delta a cada evento de status | 30 dias após entrega |
| **FOLLOW-UP** | `follow_up.json`: data agendada, template de mensagem | SQLite | Snapshot ao agendar | Até follow-up concluído |

### Exemplo de Código: State Machine com Persistência

```python
from enum import Enum
from datetime import datetime, timezone
from pathlib import Path
import json

class JourneyPhase(Enum):
    WELCOME = "welcome"
    DISCOVERY = "discovery"
    RECOMMENDATION = "recommendation"
    CART = "cart"
    PAYMENT = "payment"
    FULFILLMENT = "fulfillment"
    FOLLOW_UP = "follow_up"
    CLOSED = "closed"

class KodaSessionStateMachine:
    def __init__(self, session_id):
        self.session_id = session_id
        self.state_dir = Path(f"state/sessions/{session_id}")
        self.state_dir.mkdir(parents=True, exist_ok=True)

    def load_state(self):
        state_path = self.state_dir / "session_state.json"
        if state_path.exists():
            with open(state_path) as f:
                return json.load(f)
        return self._initialize_state()

    def _initialize_state(self):
        return {
            "session_id": self.session_id,
            "phase": JourneyPhase.WELCOME.value,
            "customer_id": None,
            "customer_profile": {},
            "cart": {"items": [], "total_brl": 0.0},
            "last_turn": 0,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat()
        }

    def save_state(self, state):
        state["updated_at"] = datetime.now(timezone.utc).isoformat()
        state_path = self.state_dir / "session_state.json"
        atomic_write_json(state_path, state)

    def transition_to(self, state, new_phase):
        old_phase = state["phase"]
        state["phase"] = new_phase.value if isinstance(new_phase, JourneyPhase) else new_phase
        self.save_state(state)
        self._create_phase_checkpoint(state, old_phase, state["phase"])

    def _create_phase_checkpoint(self, state, from_phase, to_phase):
        checkpoint = {
            "checkpoint_id": f"phase_{from_phase}_to_{to_phase}",
            "session_id": self.session_id,
            "from_phase": from_phase,
            "to_phase": to_phase,
            "snapshot": {
                "customer_profile": state.get("customer_profile", {}),
                "cart": state.get("cart", {}),
                "last_turn": state.get("last_turn", 0)
            },
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        cp_dir = self.state_dir / "checkpoints"
        cp_dir.mkdir(exist_ok=True)
        atomic_write_json(cp_dir / f"{checkpoint['checkpoint_id']}.json", checkpoint)

    def process_turn(self, customer_message):
        state = self.load_state()
        phase = state["phase"]
        state["last_turn"] += 1

        # Roteia para o handler da fase atual
        handlers = {
            "welcome": self._handle_welcome,
            "discovery": self._handle_discovery,
            "recommendation": self._handle_recommendation,
            "cart": self._handle_cart,
            "payment": self._handle_payment,
            "fulfillment": self._handle_fulfillment,
        }

        handler = handlers.get(phase)
        if not handler:
            return "Sessao em estado desconhecido. Vou reiniciar o atendimento."

        response, next_phase = handler(state, customer_message)

        if next_phase and next_phase != phase:
            self.transition_to(state, next_phase)

        return response

    def _handle_welcome(self, state, message):
        state["customer_id"] = f"cust_{self.session_id}"
        response = "Oi! Sou o KODA. Qual o seu objetivo de treino e tem alguma restricao alimentar?"
        return response, JourneyPhase.DISCOVERY

    def _handle_discovery(self, state, message):
        # Extrai restrições e objetivos da mensagem
        state["customer_profile"]["raw_input"] = message
        state["customer_profile"]["collected_at"] = datetime.now(timezone.utc).isoformat()

        if "lactose" in message.lower():
            state["customer_profile"]["restrictions"] = ["lactose"]
        if "gluten" in message.lower():
            state["customer_profile"]["restrictions"] = state["customer_profile"].get("restrictions", []) + ["gluten"]

        self.save_state(state)

        response = "Entendi. Qual o seu orcamento para este mes?"
        return response, JourneyPhase.DISCOVERY  # Continua em discovery até coletar tudo

    def _handle_recommendation(self, state, message):
        cart_items = state["cart"].get("items", [])
        response = f"Com base no seu perfil, recomendo 2 opcoes. Quer que eu monte o carrinho?"
        return response, JourneyPhase.CART

    def _handle_cart(self, state, message):
        state["cart"] = {
            "items": [{"sku": "WHEY-ISO-BAUN-900", "qty": 1, "price": 189.90}],
            "total_brl": 189.90,
            "shipping": "gratis"
        }
        self.save_state(state)
        response = f"Carrinho pronto: R$ {state['cart']['total_brl']}. Posso gerar o pagamento?"
        return response, JourneyPhase.PAYMENT

    def _handle_payment(self, state, message):
        payment_link = f"https://pay.koda.app/{self.session_id}"
        state["payment_link"] = payment_link
        self.save_state(state)
        return f"Link de pagamento: {payment_link}", JourneyPhase.FULFILLMENT

    def _handle_fulfillment(self, state, message):
        state["fulfillment_status"] = "delivered"
        self.save_state(state)
        return "Seu pedido foi entregue! Daqui 14 dias pergunto como foi.", JourneyPhase.FOLLOW_UP
```

### O Que Esta State Machine Garante

1. Em qualquer ponto da jornada, o estado está salvo em disco.
2. Se o servidor reiniciar, `load_state()` recupera exatamente a fase e os dados.
3. Transições de fase criam checkpoints automáticos para auditoria.
4. O cliente nunca percebe a reinicialização — o KODA retoma com o contexto completo.
5. O código de cada fase é isolado: mudar `_handle_discovery` não afeta `_handle_payment`.

### Conversa Real com Persistência

```
21:02 KODA: Pedro, seu carrinho esta pronto. Total: R$ 379,60. Posso gerar o link?
       └─ state salvo: phase=CART, cart={4 items, total=379.60}

21:03 Pedro: Pode. Finaliza ai.
       └─ state carregado do disco
       └─ transição: CART → PAYMENT
       └─ checkpoint criado: phase_cart_to_payment.json
       └─ payment_link gerado e salvo

[SERVIDOR REINICIA]

21:04 Pedro: Deu erro no pagamento. Tenta de novo?
       └─ state carregado do disco: phase=PAYMENT, cart pronto, link gerado
       └─ KODA: "Pedro, seu carrinho com 4 itens por R$ 379,60 esta seguro.
                O link de pagamento e: https://pay.koda.app/ord_99281.
                Quer que eu gere um novo?"
```

A diferença entre "Oi! Como posso te ajudar?" e "Seu carrinho está seguro" é state persistence.

---

## 📊 Comparativo: Estratégias de Coordenação com Persistência

State persistence não vive sozinha.

Ela se combina com as estratégias de coordenação que vimos no módulo multi-agent.

| Estratégia | Sem Persistência | Com Persistência | Melhora |
| --- | --- | --- | --- |
| **Sequencial** (Planner → Generator → Evaluator) | Se o Evaluator falha, perde-se plan.json e generation.json. Recomeça tudo. | Arquivos em disco. Evaluator reexecuta lendo os mesmos arquivos. Planner e Generator não precisam refazer trabalho. | Retrabalho cai de 100% para ~10% |
| **Paralelo** (múltiplos Generators) | Se um Generator falha, não há como saber quais terminaram. Ou refaz tudo ou assume inconsistência. | Cada Generator escreve seu output em disco. Sistema verifica quais arquivos existem e reexecuta apenas os ausentes. | Retrabalho cai de 100% para ~1/N |
| **Event-driven** (agentes reagem a eventos) | Se um agente perde um evento, ele nunca reage. Estado fica inconsistente sem detecção. | Eventos são persistidos (Redis Streams, SQLite queue). Agente processa do último evento confirmado. | Eventos perdidos caem de ~5% para <0.1% |

### Diagrama: Coordenação Sequencial com Persistência

```
┌──────────────────────────────────────────────────────────────────────────┐
│                    SEQUENCIAL COM PERSISTÊNCIA                             │
│                                                                          │
│  ┌──────────┐    plan.json     ┌────────────┐   generation.json           │
│  │ Planner  │ ───────────────► │ Generator  │ ───────────────►            │
│  └──────────┘                  └────────────┘                  │          │
│       │                              │                         │          │
│       │ escreve                      │ escreve                  │          │
│       ▼                              ▼                         ▼          │
│  ┌──────────────────────────────────────────────────────────────────┐    │
│  │                     STATE DIRECTORY                               │    │
│  │  sessions/wa_pedro/                                               │    │
│  │  ├── plan.json             ← Planner escreve                      │    │
│  │  ├── generation.json       ← Generator escreve                    │    │
│  │  ├── evaluation.json       ← Evaluator escreve                    │    │
│  │  └── checkpoints/          ← snapshots de fase                    │    │
│  └──────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│  Se crash após plan.json mas antes de generation.json:                    │
│    Sistema detecta: plan.json existe, generation.json não.                │
│    Ação: reexecuta Generator (Planner não precisa refazer).               │
│                                                                          │
│  Se crash após generation.json mas antes de evaluation.json:              │
│    Sistema detecta: generation.json existe, evaluation.json não.          │
│    Ação: reexecuta Evaluator (Generator não precisa refazer).             │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## ⚠️ Anti-Padrões de Persistência

### Anti-Padrão 1: "Vou Salvar no Final"

Salvar estado apenas no final da jornada é o erro mais comum.

```
Jornada de 45 minutos:
  Minuto  0-44: tudo em memória
  Minuto 45:     salva estado
                 └─ mas o crash aconteceu no minuto 30
```

**Correção:** salve estado a cada transição de fase e a cada N turns.

### Anti-Padrão 2: "Um Arquivo Gigante com Tudo"

Um único `state.json` de 5 MB com todo o histórico, perfil, carrinho e catálogo.

```
Problemas:
  1. Parse leva 200ms a cada turno.
  2. Escrita atômica de 5 MB é frágil.
  3. Corrupção em um campo corrompe tudo.
  4. Impossível debugar: onde está o campo que mudou?
```

**Correção:** particione estado por domínio. `customer_profile.json`, `cart.json`, `session_meta.json`, `turns/turn_*.json`.

### Anti-Padrão 3: "Redis sem Persistência Configurada"

Usar Redis como único store sem RDB ou AOF.

```
Redis padrão: tudo em RAM.
  Reiniciou o Redis? Estado perdido.
  Migrou de instância? Estado perdido.
  Escalou horizontalmente? Sem replica, estado perdido.
```

**Correção:** configure `save 60 1000` (RDB a cada 60s se 1000 writes) e `appendonly yes` (AOF).

### Anti-Padrão 4: "Checkpoint só de Dados, sem Metadados de Fase"

Salvar `cart.json` sem registrar em qual fase da jornada o carrinho foi criado.

```
Problema:
  Sistema carrega cart.json após crash.
  Mas não sabe se o cliente já pagou, se o carrinho é um draft,
  ou se é um carrinho abandonado de 3 dias atrás.
```

**Correção:** todo checkpoint inclui `phase`, `turn_number` e `next_expected_action`.

### Anti-Padrão 5: "Sobrescrever Arquivo sem Write-Temp-Rename"

```python
# ERRADO
with open("cart.json", "w") as f:
    json.dump(cart, f)
# Se o processo cair no meio do write, cart.json fica truncado.
```

**Correção:** sempre use write-temp-then-rename (atomic write).

### Anti-Padrão 6: "Silent Fail on Load"

```python
# ERRADO
try:
    state = json.loads(path.read_text())
except:
    state = {}  # Estado vazio! Cliente perdeu tudo silenciosamente.
```

**Correção:**

```python
# CORRETO
try:
    state = json.loads(path.read_text())
except (FileNotFoundError, json.JSONDecodeError) as e:
    # Tenta checkpoint anterior
    state = restore_from_snapshot(session_id)
    if state is None:
        # Só aqui assume estado inicial
        state = initialize_state()
    # Loga o incidente
    print(f"State recovery: loaded from checkpoint after error: {e}")
```

---

## 🎯 Key Takeaways

1. State persistence é a diferença entre um agente que funciona em demo e um agente que sobrevive em produção.

2. A memória de contexto do LLM é volátil e limitada. Estado crítico deve viver fora dela.

3. SQLite, JSON files e Redis não são concorrentes — são camadas complementares. JSON para prototipagem e audit trail, Redis para estado quente, SQLite para queries e durabilidade.

4. Checkpoints devem ser criados em pontos seguros da jornada: transições de fase e a cada N turns.

5. O padrão híbrido (full snapshot periódico + deltas incrementais) oferece o melhor equilíbrio entre segurança de recuperação e eficiência de I/O.

6. Estratégias de recuperação devem ser escolhidas por cenário: rollback para falhas transientes, replay para determinismo, compensação para efeitos colaterais externos.

7. State persistence combinada com coordenação de agentes reduz retrabalho em 90%+ quando ocorrem falhas.

8. A state machine da jornada do cliente é o mapa que diz o que persistir, quando persistir e como recuperar.

9. Anti-padrões de persistência são silenciosos: você só descobre quando o cliente já perdeu a conversa.

10. Persistir estado não é uma feature técnica. É uma promessa ao cliente de que o tempo dele importa.

---

## 🚀 Checkpoint: O Que Você Aprendeu

- [ ] Consigo explicar a diferença entre memória de contexto e memória externa (state persistence).

- [ ] Consigo enumerar as quatro categorias de falha que state persistence previne.

- [ ] Consigo comparar SQLite, JSON files e Redis em dimensões como latência, durabilidade, concorrência e complexidade operacional.

- [ ] Consigo decidir qual backend usar para cada tipo de estado no KODA (perfil, carrinho, histórico, audit trail).

- [ ] Consigo implementar checkpointing com snapshot completo, delta incremental e estratégia híbrida.

- [ ] Consigo escrever uma função `atomic_write_json` que evita corrupção de arquivo.

- [ ] Consigo escolher entre rollback, replay e compensação para cada cenário de falha.

- [ ] Consigo desenhar uma state machine para a jornada de compra do KODA com fases, transições e checkpoints.

- [ ] Consigo implementar um `KodaSessionStateMachine` que sobrevive a reinicializações de processo.

- [ ] Consigo identificar anti-padrões de persistência em código existente (save tardio, arquivo único gigante, Redis sem AOF, sobrescrita não-atômica, silent fail).

- [ ] Consigo explicar por que state persistence combinada com multi-agent coordination reduz retrabalho em 90%+.

- [ ] Consigo justificar o ROI de state persistence para um stakeholder de negócio.

---

## 📚 Referências & Próximas Leituras

- `curriculum/03-nivel-3-advanced-architecture/01-multi-agent-systems.md` para revisar como agentes usam arquivos de estado como contrato.

- `curriculum/03-nivel-3-advanced-architecture/03-file-based-coordination.md` para aprofundar coordenação por arquivos JSON.

- `curriculum/03-nivel-3-advanced-architecture/04-server-side-compaction.md` para entender compactação de histórico em conversas longas.

- `curriculum/03-nivel-3-advanced-architecture/05-harness-evolution.md` para ver como o harness de persistência evolui com o tempo.

- `curriculum/02-nivel-2-practical-patterns/04-trace-reading.md` para aprender a ler traces de estado e diagnosticar falhas.

- Documentação oficial do SQLite: WAL mode, atomic commit, locking.

- Documentação oficial do Redis: RDB persistence, AOF persistence, eviction policies.

- PostgreSQL documentation para quando o volume de dados justificar um banco mais robusto.

- Papers sobre saga pattern e distributed transactions para cenários com múltiplos sistemas externos.

- `curriculum/04-nivel-4-koda-specific/02-customer-journey-flows.md` para aplicar state persistence em jornadas completas do KODA.

---

## 💭 Reflexão Final

Quando Pedro perdeu 47 minutos de conversa porque o servidor reiniciou, o problema não era o servidor.

Servidores reiniciam.

É o que servidores fazem.

O problema era que o KODA tratava a memória do processo como se fosse permanente.

State persistence é sobre aceitar a realidade: processos morrem, redes falham, discos corrompem, clientes voltam depois de dias.

E, apesar de tudo isso, o agente precisa estar pronto.

Não é sobre evitar falhas.

É sobre sobreviver a elas com dignidade.

Cada checkpoint que você salva é uma mensagem silenciosa para o cliente:

"Seu tempo importa. Eu lembro de você. Pode continuar de onde parou."

Essa é a diferença entre um chatbot e um agente confiável.

E confiança, no final, é o único produto que realmente importa.

---

*Escrito com foco em clareza prática, relevância arquitetural e respeito ao tempo do leitor.*
*Memória: State persistence é a camada que transforma agentes bem desenhados em agentes que sobrevivem.*
