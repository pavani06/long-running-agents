---
title: "Solucao do Exercicio 2: State Persistence com SQLite e Recovery"
type: curriculum-solution
nivel: 3
aliases: ["solução persistence", "SQLite recovery", "checkpoint manager", "state persistence"]
tags: [curriculo-conteudo, nivel-3, solucao, checkpointing, crash-recovery, state-persistence, snapshot, rollback, atomic-writing, audit-trail, session-state, journey-phase, sqlite, wal-mode, python, implementacao-referencia]
relates-to: ["[[curriculum/03-nivel-3-advanced-architecture/exercises/exercise-02|Exercise 02]]"]
last_updated: 2026-06-10
---
# ✅ Solucao do Exercicio 2: State Persistence com SQLite e Recovery
## Implementando Checkpointing, Atomic Writes e Recuperacao de Falhas para o KODA

**Nivel:** 3 - Arquitetura Avancada
**Tempo Estimado de Leitura:** 45-60 minutos
**Dificuldade:** ⭐⭐⭐⭐ (Avancada)
**Pre-requisito:** Ter completado `exercise-02.md` e lido `02-state-persistence.md`
**Status:** Solucao Completa com Codigo Funcional

---

## 📖 Prologo: A Conversa Que Nao Pode Ser Perdida

Voce recebeu a seguinte tarefa do seu tech lead:

> "O KODA esta perdendo conversas quando o servidor reinicia. Precisamos de state persistence com SQLite. O Fernando quer checkpointing automatico e recovery transparente — o cliente nao pode perceber que houve uma falha. Voce tem 2 dias."

Voce ja leu `02-state-persistence.md` e entendeu a teoria: SQLite para durabilidade, checkpoints em transicoes de fase, atomic writes para evitar corrupcao, estrategias de recovery por cenario de falha.

Agora voce precisa **implementar**.

Este documento e a solucao completa — o codigo que voce entregaria ao final desses 2 dias. Cada funcao, cada decisao de design, cada trade-off esta explicado. Voce nao vai apenas copiar codigo; vai entender **por que** cada linha foi escrita daquela forma.

Ao final, voce tera nao apenas uma implementacao funcional, mas um modelo mental de como state persistence transforma um agente fragil em um agente que sobrevive a qualquer falha.

---

## 🎯 Visao Geral da Solucao

### O Que Vamos Construir

```
┌─────────────────────────────────────────────────────────────────────┐
│                     STATE PERSISTENCE PARA KODA                       │
│                                                                     │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐                       │
│  │ Planner  │───►│ Generator│───►│ Evaluator│                       │
│  └────┬─────┘    └────┬─────┘    └────┬─────┘                       │
│       │               │               │                             │
│       │      ┌────────┴────────┐      │                             │
│       └──────┤  PERSISTENCE    ├──────┘                             │
│              │     LAYER       │                                    │
│              └────────┬────────┘                                    │
│                       │                                             │
│              ┌────────┴────────┐                                    │
│              │    SQLite DB    │                                    │
│              │  (koda_state)   │                                    │
│              └────────┬────────┘                                    │
│                       │                                             │
│         ┌─────────────┼─────────────┐                              │
│         ▼             ▼             ▼                              │
│   ┌──────────┐ ┌──────────┐ ┌──────────┐                           │
│   │Sessions  │ │Checkpoints│ │Cart State│  ... e mais tabelas       │
│   └──────────┘ └──────────┘ └──────────┘                           │
│                                                                     │
│  Toda operacao de estado passa pela persistence layer.               │
│  Nada fica apenas em memoria.                                        │
│  Se o processo morrer, o estado sobrevive no SQLite.                  │
└─────────────────────────────────────────────────────────────────────┘
```

### Arquivos Que Voce Vai Criar

```
state_persistence/
├── db.py                 # Gerenciamento do SQLite (schema, conexao, migrations)
├── session_store.py      # CRUD de sessoes e estado da jornada
├── checkpoint.py         # Logica de checkpointing (full + delta + hibrido)
├── atomic_write.py       # Helper para escrita atomica em disco
├── recovery.py           # Estrategias de recuperacao (rollback, replay, compensacao)
├── saga.py               # Implementation do Saga Pattern para checkout
├── koda_state_machine.py # State machine da jornada KODA com persistencia
└── test_recovery.py      # Testes de recuperacao apos falha simulada
```

### Tecnologias

- **Python 3.10+** com type hints completos
- **SQLite3** (built-in, sem dependencias externas) com WAL mode
- **json** (built-in) para serializacao de estado complexo
- **pathlib** para paths cross-platform
- **unittest** para testes de recovery

### Por Que SQLite e Nao Outro Backend?

| Criterio | Decisao | Justificativa |
| --- | --- | --- |
| **Schema enforcement** | SQLite com constraints CHECK e foreign keys | Evita corrupcao silenciosa de estado — o banco rejeita tipos errados |
| **Queries complexas** | SQL com JOIN e aggregations | Permite perguntar "quantos carrinhos estao abertos ha mais de 30 min?" sem carregar todos os arquivos |
| **Transactional safety** | ACID com WAL mode | Rollback automatico em caso de crash no meio de uma transacao |
| **Single-file portability** | Um arquivo `.db` | Backup e restauracao triviais. Nada de servidor separado |
| **Concorrencia** | WAL mode: readers + 1 writer | Perfeito para Planner (write), Generator (read), Evaluator (read) em sequencia |
| **Zero operacao** | Sem servidor, sem config, sem dependencia de rede | Nao adiciona complexidade operacional ao KODA |

---

## 🗄️ Parte 1: O Banco de Dados (db.py)

### Schema Completo

O schema do SQLite e o contrato fundamental do sistema de persistencia. Cada tabela, constraint e indice tem um proposito especifico na jornada de compra do KODA.

```python
# db.py
import sqlite3
import os
from pathlib import Path
from typing import Optional

DB_PATH = Path("state/koda_state.db")

SCHEMA_SQL = """
-- Sessoes de conversa: a unidade fundamental de jornada
CREATE TABLE IF NOT EXISTS sessions (
    session_id      TEXT PRIMARY KEY,
    customer_id     TEXT,
    channel         TEXT NOT NULL DEFAULT 'whatsapp',
    current_phase   TEXT NOT NULL DEFAULT 'welcome',
    status          TEXT NOT NULL DEFAULT 'active'
        CHECK (status IN ('active', 'paused', 'closed', 'expired')),
    created_at      TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Perfil do cliente: informacoes coletadas na fase DISCOVERY
CREATE TABLE IF NOT EXISTS customer_profile (
    customer_id         TEXT PRIMARY KEY,
    name                TEXT,
    dietary_restrictions TEXT,          -- JSON array: ["gluten", "lactose"]
    training_goal       TEXT,
    budget_min_brl      REAL,
    budget_max_brl      REAL,
    preferences_json    TEXT,           -- JSON object com preferencias
    created_at          TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at          TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Historico de mensagens da conversa
CREATE TABLE IF NOT EXISTS conversation_turns (
    turn_id         INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id      TEXT NOT NULL REFERENCES sessions(session_id),
    turn_number     INTEGER NOT NULL,
    role            TEXT NOT NULL CHECK (role IN ('customer', 'koda', 'system')),
    content         TEXT NOT NULL,
    agent_phase     TEXT,
    token_count     INTEGER,
    created_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Carrinho de compras
CREATE TABLE IF NOT EXISTS cart_state (
    cart_id         TEXT PRIMARY KEY,
    session_id      TEXT NOT NULL REFERENCES sessions(session_id),
    customer_id     TEXT NOT NULL,
    items_json      TEXT NOT NULL,       -- JSON array com itens
    total_brl       REAL NOT NULL CHECK (total_brl >= 0),
    shipping_city   TEXT,
    shipping_zone   TEXT,
    status          TEXT NOT NULL DEFAULT 'draft'
        CHECK (status IN ('draft', 'confirmed', 'paid', 'expired')),
    payment_link    TEXT,
    created_at      TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Checkpoints: snapshots de estado em pontos seguros da jornada
CREATE TABLE IF NOT EXISTS checkpoints (
    checkpoint_id   TEXT PRIMARY KEY,
    session_id      TEXT NOT NULL REFERENCES sessions(session_id),
    phase           TEXT NOT NULL,
    turn_number     INTEGER NOT NULL,
    state_snapshot  TEXT NOT NULL,       -- JSON completo do estado no momento
    checkpoint_type TEXT NOT NULL DEFAULT 'full'
        CHECK (checkpoint_type IN ('full', 'delta')),
    base_checkpoint_id TEXT,             -- FK para checkpoint base (se delta)
    created_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Eventos de sistema: auditoria de transicoes e falhas
CREATE TABLE IF NOT EXISTS system_events (
    event_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id      TEXT NOT NULL,
    event_type      TEXT NOT NULL
        CHECK (event_type IN (
            'session_started', 'phase_transition', 'checkpoint_created',
            'crash_detected', 'recovery_started', 'recovery_completed',
            'compensation_executed', 'error_logged'
        )),
    event_data_json TEXT,
    created_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Indices para queries frequentes
CREATE INDEX IF NOT EXISTS idx_turns_session
    ON conversation_turns(session_id, turn_number);
CREATE INDEX IF NOT EXISTS idx_cart_session
    ON cart_state(session_id);
CREATE INDEX IF NOT EXISTS idx_checkpoints_session
    ON checkpoints(session_id, created_at);
CREATE INDEX IF NOT EXISTS idx_events_session
    ON system_events(session_id, created_at);
"""

def get_connection(db_path: Optional[Path] = None) -> sqlite3.Connection:
    """
    Retorna uma conexao SQLite configurada com WAL mode e foreign keys.

    WAL mode permite que readers e um writer coexistam sem bloqueio mutuo.
    Foreign keys garantem integridade referencial entre tabelas.
    """
    path = db_path or DB_PATH
    path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(str(path))
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.row_factory = sqlite3.Row  # Permite acesso por nome de coluna

    return conn

def init_db(db_path: Optional[Path] = None) -> sqlite3.Connection:
    """
    Inicializa o banco de dados: cria schema se nao existir.
    Idempotente — seguro chamar multiplas vezes.
    """
    conn = get_connection(db_path)
    conn.executescript(SCHEMA_SQL)
    conn.commit()

    # Loga inicializacao
    conn.execute(
        "INSERT INTO system_events (session_id, event_type, event_data_json) VALUES (?, ?, ?)",
        ("system", "session_started", '{"component": "db_init"}')
    )
    conn.commit()

    return conn

def close_db(conn: sqlite3.Connection) -> None:
    """Fecha conexao com checkpoint WAL para garantir durabilidade."""
    conn.execute("PRAGMA wal_checkpoint(TRUNCATE)")
    conn.close()
```

### Por Que Este Schema?

Cada decisao de schema foi intencional:

1. **`TEXT PRIMARY KEY` em vez de `INTEGER`**: Sessoes do KODA sao identificadas por strings como `wa_2026_05_26_pedro`. Usar TEXT evita uma camada de traducao desnecessaria.

2. **`CHECK` constraints em colunas de status**: Previne que codigo com bug insira `"actve"` em vez de `"active"`. O banco rejeita na hora, em vez de propagar estado invalido.

3. **`items_json` como TEXT com JSON**: Carrinhos podem ter estruturas variaveis (diferentes tipos de produto, promocoes, combos). JSON da flexibilidade sem sacrificar a capacidade de query — podemos usar `json_extract()` do SQLite quando necessario.

4. **`system_events` como audit trail**: Cada transicao de fase, checkpoint e recovery e registrado. Isso permite responder perguntas como "quantas sessoes sofreram crash esta semana?" com um `SELECT COUNT(*)`.

5. **`WAL mode`**: Write-Ahead Logging permite que readers leiam enquanto um writer escreve. Critico para o padrao Planner (write) → Generator (read) → Evaluator (read).

6. **`row_factory = sqlite3.Row`**: Permite acessar colunas por nome (`row["session_id"]`) em vez de indice (`row[0]`), tornando o codigo mais legivel e resistente a mudancas de schema.

---

## 💾 Parte 2: Session Store (session_store.py)

O session store e a camada de acesso a dados que isola o resto do codigo dos detalhes do SQLite. Toda operacao de leitura e escrita de estado passa por aqui.

```python
# session_store.py
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Dict, Any, List

from db import get_connection, DB_PATH

# ============================================================================
# FUNCOES DE SESSAO
# ============================================================================

def create_session(
    session_id: str,
    customer_id: Optional[str] = None,
    channel: str = "whatsapp",
    conn: Optional[sqlite3.Connection] = None
) -> Dict[str, Any]:
    """
    Cria uma nova sessao no estado inicial (fase: welcome).

    Retorna o dict da sessao criada.
    """
    should_close = conn is None
    conn = conn or get_connection()

    try:
        now = datetime.now(timezone.utc).isoformat()
        conn.execute(
            """INSERT INTO sessions (session_id, customer_id, channel, current_phase, status, created_at, updated_at)
               VALUES (?, ?, ?, 'welcome', 'active', ?, ?)""",
            (session_id, customer_id, channel, now, now)
        )

        # Evento de auditoria
        conn.execute(
            "INSERT INTO system_events (session_id, event_type, event_data_json) VALUES (?, ?, ?)",
            (session_id, "session_started", json.dumps({"channel": channel}))
        )
        conn.commit()

        return {
            "session_id": session_id,
            "customer_id": customer_id,
            "channel": channel,
            "current_phase": "welcome",
            "status": "active",
            "created_at": now,
            "updated_at": now
        }
    finally:
        if should_close:
            conn.close()

def get_session(session_id: str, conn: Optional[sqlite3.Connection] = None) -> Optional[Dict[str, Any]]:
    """Recupera uma sessao pelo ID. Retorna None se nao existir."""
    should_close = conn is None
    conn = conn or get_connection()

    try:
        row = conn.execute(
            "SELECT * FROM sessions WHERE session_id = ?", (session_id,)
        ).fetchone()

        return dict(row) if row else None
    finally:
        if should_close:
            conn.close()

def update_session_phase(
    session_id: str,
    new_phase: str,
    conn: Optional[sqlite3.Connection] = None
) -> None:
    """
    Atualiza a fase atual da sessao.

    Registra a transicao no audit trail para rastreabilidade.
    """
    should_close = conn is None
    conn = conn or get_connection()

    try:
        old_phase_row = conn.execute(
            "SELECT current_phase FROM sessions WHERE session_id = ?", (session_id,)
        ).fetchone()

        if old_phase_row is None:
            raise ValueError(f"Session {session_id} not found")

        old_phase = old_phase_row["current_phase"]
        now = datetime.now(timezone.utc).isoformat()

        conn.execute(
            "UPDATE sessions SET current_phase = ?, updated_at = ? WHERE session_id = ?",
            (new_phase, now, session_id)
        )

        # Audit trail da transicao
        conn.execute(
            "INSERT INTO system_events (session_id, event_type, event_data_json) VALUES (?, ?, ?)",
            (
                session_id,
                "phase_transition",
                json.dumps({"from": old_phase, "to": new_phase})
            )
        )
        conn.commit()
    finally:
        if should_close:
            conn.close()

# ============================================================================
# FUNCOES DE PERFIL DO CLIENTE
# ============================================================================

def upsert_customer_profile(
    customer_id: str,
    name: Optional[str] = None,
    dietary_restrictions: Optional[List[str]] = None,
    training_goal: Optional[str] = None,
    budget_min_brl: Optional[float] = None,
    budget_max_brl: Optional[float] = None,
    preferences: Optional[Dict[str, Any]] = None,
    conn: Optional[sqlite3.Connection] = None
) -> Dict[str, Any]:
    """
    Cria ou atualiza o perfil do cliente.

    Usa upsert (INSERT OR REPLACE) para ser idempotente.
    """
    should_close = conn is None
    conn = conn or get_connection()

    try:
        now = datetime.now(timezone.utc).isoformat()
        restrictions_json = json.dumps(dietary_restrictions) if dietary_restrictions else None
        preferences_json = json.dumps(preferences) if preferences else None

        conn.execute(
            """INSERT INTO customer_profile
               (customer_id, name, dietary_restrictions, training_goal,
                budget_min_brl, budget_max_brl, preferences_json, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
               ON CONFLICT(customer_id) DO UPDATE SET
                   name = COALESCE(excluded.name, customer_profile.name),
                   dietary_restrictions = COALESCE(excluded.dietary_restrictions, customer_profile.dietary_restrictions),
                   training_goal = COALESCE(excluded.training_goal, customer_profile.training_goal),
                   budget_min_brl = COALESCE(excluded.budget_min_brl, customer_profile.budget_min_brl),
                   budget_max_brl = COALESCE(excluded.budget_max_brl, customer_profile.budget_max_brl),
                   preferences_json = COALESCE(excluded.preferences_json, customer_profile.preferences_json),
                   updated_at = excluded.updated_at""",
            (customer_id, name, restrictions_json, training_goal,
             budget_min_brl, budget_max_brl, preferences_json, now, now)
        )
        conn.commit()

        return get_customer_profile(customer_id, conn=conn) or {}
    finally:
        if should_close:
            conn.close()

def get_customer_profile(
    customer_id: str,
    conn: Optional[sqlite3.Connection] = None
) -> Optional[Dict[str, Any]]:
    """Recupera perfil do cliente com deserializacao de campos JSON."""
    should_close = conn is None
    conn = conn or get_connection()

    try:
        row = conn.execute(
            "SELECT * FROM customer_profile WHERE customer_id = ?", (customer_id,)
        ).fetchone()

        if row is None:
            return None

        profile = dict(row)
        # Deserializa campos JSON
        if profile.get("dietary_restrictions"):
            profile["dietary_restrictions"] = json.loads(profile["dietary_restrictions"])
        if profile.get("preferences_json"):
            profile["preferences"] = json.loads(profile["preferences_json"])
            del profile["preferences_json"]

        return profile
    finally:
        if should_close:
            conn.close()

# ============================================================================
# FUNCOES DE CARRINHO
# ============================================================================

def save_cart(
    session_id: str,
    customer_id: str,
    items: List[Dict[str, Any]],
    total_brl: float,
    shipping_city: Optional[str] = None,
    shipping_zone: Optional[str] = None,
    status: str = "draft",
    payment_link: Optional[str] = None,
    conn: Optional[sqlite3.Connection] = None
) -> Dict[str, Any]:
    """
    Salva ou atualiza o estado do carrinho.

    O campo items_json armazena a lista de itens como JSON.
    Cada item tem: sku, name, qty, unit_price_brl.
    """
    should_close = conn is None
    conn = conn or get_connection()

    try:
        now = datetime.now(timezone.utc).isoformat()
        cart_id = f"cart_{session_id}"

        conn.execute(
            """INSERT INTO cart_state
               (cart_id, session_id, customer_id, items_json, total_brl,
                shipping_city, shipping_zone, status, payment_link, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
               ON CONFLICT(cart_id) DO UPDATE SET
                   items_json = excluded.items_json,
                   total_brl = excluded.total_brl,
                   shipping_city = COALESCE(excluded.shipping_city, cart_state.shipping_city),
                   shipping_zone = COALESCE(excluded.shipping_zone, cart_state.shipping_zone),
                   status = excluded.status,
                   payment_link = COALESCE(excluded.payment_link, cart_state.payment_link),
                   updated_at = excluded.updated_at""",
            (cart_id, session_id, customer_id, json.dumps(items), total_brl,
             shipping_city, shipping_zone, status, payment_link, now, now)
        )
        conn.commit()

        return get_cart(session_id, conn=conn) or {}
    finally:
        if should_close:
            conn.close()

def get_cart(session_id: str, conn: Optional[sqlite3.Connection] = None) -> Optional[Dict[str, Any]]:
    """Recupera o carrinho da sessao com deserializacao dos itens."""
    should_close = conn is None
    conn = conn or get_connection()

    try:
        row = conn.execute(
            "SELECT * FROM cart_state WHERE session_id = ?", (session_id,)
        ).fetchone()

        if row is None:
            return None

        cart = dict(row)
        cart["items"] = json.loads(cart["items_json"])
        del cart["items_json"]
        return cart
    finally:
        if should_close:
            conn.close()

# ============================================================================
# FUNCOES DE TURNS (HISTORICO DE CONVERSACAO)
# ============================================================================

def save_turn(
    session_id: str,
    turn_number: int,
    role: str,
    content: str,
    agent_phase: Optional[str] = None,
    token_count: Optional[int] = None,
    conn: Optional[sqlite3.Connection] = None
) -> int:
    """
    Salva uma mensagem (turn) da conversa.

    Retorna o turn_id gerado.
    """
    should_close = conn is None
    conn = conn or get_connection()

    try:
        cursor = conn.execute(
            """INSERT INTO conversation_turns
               (session_id, turn_number, role, content, agent_phase, token_count, created_at)
               VALUES (?, ?, ?, ?, ?, ?, datetime('now'))""",
            (session_id, turn_number, role, content, agent_phase, token_count)
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        if should_close:
            conn.close()

def get_recent_turns(
    session_id: str,
    limit: int = 20,
    conn: Optional[sqlite3.Connection] = None
) -> List[Dict[str, Any]]:
    """Recupera os N turns mais recentes da sessao."""
    should_close = conn is None
    conn = conn or get_connection()

    try:
        rows = conn.execute(
            """SELECT * FROM conversation_turns
               WHERE session_id = ?
               ORDER BY turn_number DESC
               LIMIT ?""",
            (session_id, limit)
        ).fetchall()

        return [dict(row) for row in reversed(rows)]
    finally:
        if should_close:
            conn.close()
```

### Decisoes de Design no Session Store

1. **`conn` como parametro opcional**: Permite que operacoes compostas compartilhem a mesma conexao. Se `conn=None`, a funcao cria e fecha sua propria conexao. Isso evita o anti-pattern de abrir/fechar conexao para cada operacao atomica.

2. **`UPSERT` com `ON CONFLICT DO UPDATE`**: Operacoes idempotentes. Se o perfil ja existe, atualiza; se nao, cria. Sem race condition.

3. **`COALESCE` no UPDATE**: Preserva valores existentes quando o novo valor e NULL. Se voce passa `name=None` no upsert, o nome anterior nao e sobrescrito.

4. **Campos JSON como TEXT**: Itens do carrinho e preferencias sao armazenados como JSON string em colunas TEXT. Isso da flexibilidade para estruturas variaveis enquanto mantem a capacidade de query via `json_extract()` do SQLite.

5. **Audit trail automatico**: `create_session` e `update_session_phase` registram eventos em `system_events` automaticamente. Nao depende do desenvolvedor lembrar de logar.

---

## 🔄 Parte 3: Checkpointing (checkpoint.py)

O sistema de checkpointing e o coracao da state persistence. Ele salva snapshots do estado em pontos seguros da jornada, permitindo recuperacao apos qualquer falha.

### Estrategia Hibrida Implementada

```
Regra de Checkpointing:

1. FULL SNAPSHOT na criacao da sessao (turno 0)
2. FULL SNAPSHOT em toda transicao de fase (welcome → discovery → cart → payment)
3. DELTA CHECKPOINT nos turns intermediarios (a cada turn que nao e transicao de fase)
4. FULL SNAPSHOT forcado a cada 10 turns (consolidacao periodica)
5. FULL SNAPSHOT forcado apos recovery (reconstroi base limpa)
```

```python
# checkpoint.py
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Dict, Any, List

from db import get_connection
from session_store import (
    get_session, get_customer_profile, get_cart, get_recent_turns
)

# Constantes de configuracao
FULL_SNAPSHOT_INTERVAL = 10  # Full snapshot a cada N turns
CRITICAL_PHASES = {"payment", "fulfillment"}  # Fases que sempre forcam full snapshot

def create_full_snapshot(
    session_id: str,
    turn_number: int,
    phase: str,
    conn: Optional[sqlite3.Connection] = None
) -> str:
    """
    Cria um snapshot completo do estado da sessao.

    Coleta todos os dados relevantes: sessao, perfil, carrinho, ultimos turns.
    Retorna o checkpoint_id.
    """
    should_close = conn is None
    conn = conn or get_connection()

    try:
        session = get_session(session_id, conn=conn)
        if session is None:
            raise ValueError(f"Session {session_id} not found")

        # Coleta estado completo
        customer_id = session.get("customer_id")
        profile = get_customer_profile(customer_id, conn=conn) if customer_id else None
        cart = get_cart(session_id, conn=conn)
        recent_turns = get_recent_turns(session_id, limit=20, conn=conn)

        snapshot = {
            "session": session,
            "customer_profile": profile,
            "cart": cart,
            "recent_turns": recent_turns,
            "turn_number": turn_number,
            "phase": phase
        }

        checkpoint_id = f"ckpt_{session_id}_{turn_number:04d}_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"

        conn.execute(
            """INSERT INTO checkpoints
               (checkpoint_id, session_id, phase, turn_number, state_snapshot, checkpoint_type, created_at)
               VALUES (?, ?, ?, ?, ?, 'full', ?)""",
            (checkpoint_id, session_id, phase, turn_number, json.dumps(snapshot),
             datetime.now(timezone.utc).isoformat())
        )

        # Evento de auditoria
        conn.execute(
            "INSERT INTO system_events (session_id, event_type, event_data_json) VALUES (?, ?, ?)",
            (session_id, "checkpoint_created",
             json.dumps({"checkpoint_id": checkpoint_id, "type": "full", "turn": turn_number, "phase": phase}))
        )

        conn.commit()
        return checkpoint_id
    finally:
        if should_close:
            conn.close()

def create_delta_checkpoint(
    session_id: str,
    turn_number: int,
    phase: str,
    base_checkpoint_id: str,
    changes: Dict[str, Any],
    conn: Optional[sqlite3.Connection] = None
) -> str:
    """
    Cria um checkpoint delta: apenas as mudancas desde o ultimo checkpoint.

    changes deve ser um dict contendo apenas os campos que mudaram.
    Exemplo: {"cart": {"items": [...], "total_brl": 189.90}}
    """
    should_close = conn is None
    conn = conn or get_connection()

    try:
        checkpoint_id = f"delta_{session_id}_{turn_number:04d}_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"

        delta_snapshot = {
            "base_checkpoint_id": base_checkpoint_id,
            "changes": changes,
            "turn_number": turn_number,
            "phase": phase
        }

        conn.execute(
            """INSERT INTO checkpoints
               (checkpoint_id, session_id, phase, turn_number, state_snapshot,
                checkpoint_type, base_checkpoint_id, created_at)
               VALUES (?, ?, ?, ?, ?, 'delta', ?, ?)""",
            (checkpoint_id, session_id, phase, turn_number, json.dumps(delta_snapshot),
             base_checkpoint_id, datetime.now(timezone.utc).isoformat())
        )

        conn.commit()
        return checkpoint_id
    finally:
        if should_close:
            conn.close()

def should_full_snapshot(
    turn_number: int,
    phase: str,
    last_full_snapshot_turn: int
) -> bool:
    """
    Decide se deve criar um full snapshot neste turno.

    Regras:
    1. Turno 0 ou 1 (inicio da sessao)
    2. Fase critica (payment, fulfillment)
    3. A cada FULL_SNAPSHOT_INTERVAL turns desde o ultimo full
    """
    if turn_number <= 1:
        return True
    if phase in CRITICAL_PHASES:
        return True
    if (turn_number - last_full_snapshot_turn) >= FULL_SNAPSHOT_INTERVAL:
        return True
    return False

def compute_delta(
    previous_state: Dict[str, Any],
    current_state: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Calcula a diferenca entre dois estados.

    Apenas campos que mudaram sao incluidos no delta.
    Campos identicos sao omitidos para economizar espaco.
    """
    delta = {}
    all_keys = set(previous_state.keys()) | set(current_state.keys())

    for key in all_keys:
        prev_val = previous_state.get(key)
        curr_val = current_state.get(key)
        if prev_val != curr_val:
            delta[key] = curr_val

    return delta

def get_last_full_snapshot(
    session_id: str,
    conn: Optional[sqlite3.Connection] = None
) -> Optional[Dict[str, Any]]:
    """Recupera o ultimo checkpoint do tipo 'full' para a sessao."""
    should_close = conn is None
    conn = conn or get_connection()

    try:
        row = conn.execute(
            """SELECT * FROM checkpoints
               WHERE session_id = ? AND checkpoint_type = 'full'
               ORDER BY created_at DESC LIMIT 1""",
            (session_id,)
        ).fetchone()

        if row is None:
            return None

        result = dict(row)
        result["state_snapshot"] = json.loads(result["state_snapshot"])
        return result
    finally:
        if should_close:
            conn.close()

def get_checkpoints_since(
    session_id: str,
    since_checkpoint_id: str,
    conn: Optional[sqlite3.Connection] = None
) -> List[Dict[str, Any]]:
    """
    Recupera todos os checkpoints (full e delta) criados apos um determinado checkpoint.

    Usado durante recovery para reconstruir estado a partir do ultimo full + deltas.
    """
    should_close = conn is None
    conn = conn or get_connection()

    try:
        # Primeiro, obtem o timestamp do checkpoint base
        base = conn.execute(
            "SELECT created_at FROM checkpoints WHERE checkpoint_id = ?",
            (since_checkpoint_id,)
        ).fetchone()

        if base is None:
            return []

        rows = conn.execute(
            """SELECT * FROM checkpoints
               WHERE session_id = ? AND created_at > ?
               ORDER BY created_at ASC""",
            (session_id, base["created_at"])
        ).fetchall()

        results = []
        for row in rows:
            cp = dict(row)
            cp["state_snapshot"] = json.loads(cp["state_snapshot"])
            results.append(cp)

        return results
    finally:
        if should_close:
            conn.close()
```

### Por Que Checkpointing Hibrido?

O hibrido (full periodico + delta incremental) oferece o melhor equilibrio:

| Metrica | So Full | So Delta | Hibrido |
| --- | --- | --- | --- |
| **Tamanho por checkpoint** | Grande (estado completo) | Pequeno (apenas mudancas) | Grande a cada 10 turns, pequeno nos demais |
| **Tempo de escrita** | Alto (serializa tudo) | Baixo (serializa so diff) | Medio |
| **Tempo de recovery** | Baixo (carrega 1 arquivo) | Alto (aplica N deltas) | Medio (carrega ultimo full + ~10 deltas) |
| **Resiliencia a corrupcao** | Alta (arquivo autocontido) | Baixa (depende de toda a cadeia) | Media (perde no maximo 10 turns) |
| **Audit trail granularidade** | Baixa (pontos esparsos) | Alta (cada turn visivel) | Alta (todos os turns, full nos marcos) |
| **Recomendado para** | Jornadas curtas | Debug detalhado | **Producao** |

---

## 📝 Parte 4: Atomic Write Helper (atomic_write.py)

Escrita atomica e essencial para evitar corrupcao de arquivos. Escrever diretamente no destino pode truncar o arquivo se o processo cair no meio da operacao.

```python
# atomic_write.py
import json
import os
import tempfile
from pathlib import Path
from typing import Any

def atomic_write_json(path: Path, data: Any, indent: int = 2) -> None:
    """
    Escreve dados JSON atomicamente usando write-temp-then-rename.

    Garantias:
    1. O arquivo destino nunca fica truncado/corrompido.
    2. Se o processo cair durante a escrita, o arquivo original permanece intacto.
    3. A operacao e atomica no filesystem: rename e instantaneo no mesmo dispositivo.

    Funcionamento:
    1. Cria arquivo temporario no mesmo diretorio (mesmo filesystem = rename atomico).
    2. Escreve JSON completo no temporario.
    3. Forca flush + fsync para garantir que dados chegaram ao disco.
    4. Renomeia temporario para o destino (operacao atomica no kernel).

    Args:
        path: Caminho do arquivo destino.
        data: Dados a serem serializados como JSON.
        indent: Indentacao do JSON (default 2 espacos).
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    # Cria arquivo temporario no mesmo diretorio para garantir
    # que rename seja atomico (mesmo filesystem)
    tmp = tempfile.NamedTemporaryFile(
        mode='w',
        dir=str(path.parent),
        prefix=f".{path.name}.",
        suffix='.tmp',
        delete=False,
        encoding='utf-8'
    )

    try:
        # Escreve o JSON completo
        json.dump(data, tmp, ensure_ascii=False, indent=indent)
        tmp.write('\n')  # Newline final por convencao

        # Forca flush para o kernel
        tmp.flush()

        # Forca fsync para garantir que dados chegaram ao disco
        # (essencial para durabilidade em caso de power loss)
        os.fsync(tmp.fileno())

    except Exception:
        # Em caso de erro, remove o temporario e nao toca no destino
        tmp.close()
        os.unlink(tmp.name)
        raise

    finally:
        tmp.close()

    # Renomeio atomico: o kernel garante que o destino
    # sera o arquivo completo ou o anterior — nunca algo pela metade
    os.rename(tmp.name, str(path))

def atomic_read_json(path: Path, default: Any = None) -> Any:
    """
    Le um arquivo JSON com tratamento de erros.

    Se o arquivo nao existe ou esta corrompido, retorna o valor default.
    NUNCA retorna estado vazio silenciosamente — loga o incidente.
    """
    path = Path(path)

    if not path.exists():
        return default

    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        # Loga o incidente — corrupcao de estado e grave
        print(f"[WARN] Failed to read {path}: {e}")
        return default
```

### Por Que `atomic_write_json` e Mandatoria?

O cenario abaixo acontece com mais frequencia do que gostariamos:

```
# CODIGO PERIGOSO (NAO USE)
with open("cart.json", "w") as f:
    json.dump(cart, f)   # Se crashar aqui...
    json.dump(more, f)   # ...ou aqui...

# Resultado: cart.json truncado ou com JSON invalido.
#            Na proxima leitura: json.JSONDecodeError.
#            Estado do cliente: perdido.
```

Com `atomic_write_json`:

```
atomic_write_json(Path("cart.json"), cart)

# Se crashar durante a escrita do temporario:
#   - temporario e removido
#   - cart.json original permanece intacto
#   - na proxima leitura: estado completo do checkpoint anterior

# Se crashar apos o rename:
#   - cart.json contem o JSON completo (rename e atomico)
#   - na proxima leitura: estado mais recente disponivel
```

Nao existe cenario onde `cart.json` fica corrompido.

---

## 🔧 Parte 5: Recovery Strategies (recovery.py)

Checkpoints salvam estado. Recovery strategies definem o que fazer quando algo da errado.

```python
# recovery.py
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Dict, Any, Tuple, Callable

from db import get_connection
from checkpoint import (
    get_last_full_snapshot, get_checkpoints_since, create_full_snapshot
)
from session_store import get_session, update_session_phase

# ============================================================================
# ESTRATEGIA 1: ROLLBACK PARA ULTIMO CHECKPOINT SEGURO
# ============================================================================

def rollback_to_last_checkpoint(
    session_id: str,
    conn: Optional[sqlite3.Connection] = None
) -> Optional[Dict[str, Any]]:
    """
    Recupera o estado da sessao a partir do ultimo checkpoint seguro.

    Fluxo:
    1. Localiza o ultimo full snapshot
    2. Carrega o estado base
    3. Aplica deltas em ordem (se houver)
    4. Cria um novo full snapshot consolidado (pos-recovery)
    5. Registra o evento de recovery

    Returns:
        Estado reconstruido ou None se nao houver checkpoint
    """
    should_close = conn is None
    conn = conn or get_connection()

    try:
        # Registra inicio do recovery
        conn.execute(
            "INSERT INTO system_events (session_id, event_type, event_data_json) VALUES (?, ?, ?)",
            (session_id, "recovery_started",
             json.dumps({"strategy": "rollback", "timestamp": datetime.now(timezone.utc).isoformat()}))
        )
        conn.commit()

        # Passo 1: Carrega ultimo full snapshot
        last_full = get_last_full_snapshot(session_id, conn=conn)
        if last_full is None:
            conn.execute(
                "INSERT INTO system_events (session_id, event_type, event_data_json) VALUES (?, ?, ?)",
                (session_id, "error_logged",
                 json.dumps({"error": "no_checkpoint_found", "strategy": "rollback"}))
            )
            conn.commit()
            return None

        state = last_full["state_snapshot"]
        phase = last_full["phase"]

        # Passo 2: Aplica deltas desde o ultimo full
        deltas = get_checkpoints_since(session_id, last_full["checkpoint_id"], conn=conn)
        for delta_cp in deltas:
            if delta_cp.get("checkpoint_type") == "delta":
                changes = delta_cp["state_snapshot"].get("changes", {})
                for key, value in changes.items():
                    state[key] = value
                phase = delta_cp["phase"]  # Atualiza para a fase mais recente

        # Passo 3: Atualiza a sessao com a fase recuperada
        update_session_phase(session_id, phase, conn=conn)

        # Passo 4: Cria full snapshot consolidado pos-recovery
        create_full_snapshot(session_id, state.get("turn_number", 0), phase, conn=conn)

        # Passo 5: Registra sucesso do recovery
        conn.execute(
            "INSERT INTO system_events (session_id, event_type, event_data_json) VALUES (?, ?, ?)",
            (session_id, "recovery_completed",
             json.dumps({"strategy": "rollback", "phase_recovered": phase}))
        )
        conn.commit()

        return state
    finally:
        if should_close:
            conn.close()

# ============================================================================
# ESTRATEGIA 2: REPLAY DETERMINISTICO
# ============================================================================

def replay_turns_from_checkpoint(
    session_id: str,
    process_turn_fn: Callable[[Dict[str, Any], str], Tuple[str, Dict[str, Any]]],
    conn: Optional[sqlite3.Connection] = None
) -> Optional[Dict[str, Any]]:
    """
    Re-executa os turns da conversa a partir do ultimo checkpoint.

    Util quando as operacoes sao deterministicas e o estado pode ser
    reconstruido re-executando a sequencia de mensagens.

    Args:
        session_id: ID da sessao a recuperar
        process_turn_fn: Funcao que processa um turno.
            Recebe (state, customer_message) e retorna (response, new_state).

    Returns:
        Estado final apos replay de todos os turns
    """
    should_close = conn is None
    conn = conn or get_connection()

    try:
        conn.execute(
            "INSERT INTO system_events (session_id, event_type, event_data_json) VALUES (?, ?, ?)",
            (session_id, "recovery_started",
             json.dumps({"strategy": "replay", "timestamp": datetime.now(timezone.utc).isoformat()}))
        )
        conn.commit()

        # Carrega estado base do ultimo checkpoint
        checkpoint_state = rollback_to_last_checkpoint(session_id, conn=conn)
        if checkpoint_state is None:
            return None

        current_state = checkpoint_state
        turn_number = checkpoint_state.get("turn_number", 0)

        # Busca todos os turns apos o checkpoint
        rows = conn.execute(
            """SELECT * FROM conversation_turns
               WHERE session_id = ? AND turn_number > ? AND role = 'customer'
               ORDER BY turn_number ASC""",
            (session_id, turn_number)
        ).fetchall()

        # Re-executa cada turno
        for row in rows:
            customer_message = row["content"]
            response, current_state = process_turn_fn(current_state, customer_message)
            # O novo estado ja e salvo pelo process_turn_fn

        conn.execute(
            "INSERT INTO system_events (session_id, event_type, event_data_json) VALUES (?, ?, ?)",
            (session_id, "recovery_completed",
             json.dumps({"strategy": "replay", "turns_replayed": len(rows)}))
        )
        conn.commit()

        return current_state
    finally:
        if should_close:
            conn.close()

# ============================================================================
# ESTRATEGIA 3: COMPENSACAO (SAGA PATTERN)
# ============================================================================

class SagaCompensation:
    """
    Implementa o padrao Saga para operacoes que envolvem sistemas externos.

    Cada passo da saga tem:
    - Uma funcao de execucao (do_step)
    - Uma funcao de compensacao (undo_step) para desfazer se algo falhar

    Se qualquer passo falhar, todos os passos anteriores sao compensados
    na ordem inversa (LIFO).
    """

    def __init__(self, session_id: str, conn: Optional[sqlite3.Connection] = None):
        self.session_id = session_id
        self.conn = conn or get_connection()
        self.own_connection = conn is None
        self.steps_executed: list = []
        self.compensation_stack: list = []

    def add_step(self, step_name: str, do_fn: Callable, undo_fn: Callable) -> None:
        """
        Adiciona um passo a saga.

        Args:
            step_name: Nome descritivo do passo (ex: "reserve_inventory")
            do_fn: Funcao que executa o passo. Recebe o resultado acumulado.
            undo_fn: Funcao que desfaz o passo. Recebe o resultado do do_fn.
        """
        self.compensation_stack.append((step_name, do_fn, undo_fn))

    def execute(self, initial_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Executa todos os passos da saga em ordem.

        Se um passo falhar, desfaz todos os passos concluidos em ordem inversa.

        Returns:
            Dict com status ('success' ou 'rolled_back') e resultados.
        """
        context = initial_context or {}

        try:
            for step_name, do_fn, undo_fn in self.compensation_stack:
                # Executa o passo
                result = do_fn(context)
                context[step_name] = result
                self.steps_executed.append(step_name)

                # Loga sucesso do passo
                self.conn.execute(
                    "INSERT INTO system_events (session_id, event_type, event_data_json) VALUES (?, ?, ?)",
                    (self.session_id, "checkpoint_created",
                     json.dumps({"saga_step": step_name, "status": "completed"}))
                )
                self.conn.commit()

            return {"status": "success", "context": context, "steps": self.steps_executed}

        except Exception as e:
            # Compensacao: desfaz na ordem inversa
            compensation_errors = []
            for step_name in reversed(self.steps_executed):
                try:
                    # Encontra a funcao undo do passo
                    for name, do_fn, undo_fn in self.compensation_stack:
                        if name == step_name:
                            undo_fn(context.get(step_name))
                            break

                    self.conn.execute(
                        "INSERT INTO system_events (session_id, event_type, event_data_json) VALUES (?, ?, ?)",
                        (self.session_id, "compensation_executed",
                         json.dumps({"saga_step": step_name, "status": "compensated"}))
                    )
                except Exception as comp_error:
                    compensation_errors.append({"step": step_name, "error": str(comp_error)})

            self.conn.commit()

            return {
                "status": "rolled_back",
                "error": str(e),
                "steps_completed": self.steps_executed,
                "compensation_errors": compensation_errors
            }

    def close(self) -> None:
        """Fecha a conexao se ela foi criada por esta instancia."""
        if self.own_connection:
            self.conn.close()

# ============================================================================
# DETECCAO DE CRASH E RECOVERY AUTOMATICO
# ============================================================================

def detect_and_recover(
    session_id: str,
    process_turn_fn: Optional[Callable] = None,
    db_path: Optional[Path] = None
) -> Optional[Dict[str, Any]]:
    """
    Detecta se uma sessao precisa de recovery e aplica a estrategia adequada.

    Logica de deteccao:
    1. Sessao existe no banco?
    2. Status e 'active' mas nao ha atividade recente?
    3. Ultimo turno foi registrado mas nao ha checkpoint correspondente?

    Se houver evidencia de crash, aplica rollback + replay.
    """
    conn = get_connection(db_path)

    try:
        session = get_session(session_id, conn=conn)
        if session is None:
            return None

        if session["status"] != "active":
            # Sessao ja foi fechada ou expirada — nao precisa de recovery
            return None

        # Verifica se ha gap entre o ultimo turno e o ultimo checkpoint
        last_checkpoint = get_last_full_snapshot(session_id, conn=conn)
        if last_checkpoint is None:
            # Sessao sem checkpoint — estado inicial
            return None

        # Registra a deteccao de possivel crash
        conn.execute(
            "INSERT INTO system_events (session_id, event_type, event_data_json) VALUES (?, ?, ?)",
            (session_id, "crash_detected",
             json.dumps({"detected_at": datetime.now(timezone.utc).isoformat()}))
        )
        conn.commit()

        # Aplica recovery
        state = rollback_to_last_checkpoint(session_id, conn=conn)

        if state and process_turn_fn:
            state = replay_turns_from_checkpoint(session_id, process_turn_fn, conn=conn)

        return state
    finally:
        conn.close()
```

### Tabela de Decisao: Qual Estrategia Usar?

| Cenario de Falha | Estrategia | Justificativa |
| --- | --- | --- |
| **Timeout de API do Claude** | Rollback | Estado interno nao foi alterado. So a chamada falhou. Recarrega estado e tenta de novo. |
| **Crash de processo entre turns** | Rollback + Replay | Estado interno perdido. Rollback recupera checkpoint. Replay re-executa turns perdidos deterministicamente. |
| **Falha em sistema externo (pagamento)** | Compensacao (Saga) | Mundo real foi alterado (pagamento pode ter sido processado parcialmente). Rollback de codigo nao desfaz transacao financeira. |
| **Corrupcao de estado detectada** | Rollback para checkpoint especifico | Isola o dano. Volta ao ultimo ponto confirmadamente consistente. |
| **Cliente volta apos 3 dias** | Rollback + Replay | Estado entre sessoes precisa ser reconstruido. Full snapshot base + replay dos turns finais da ultima sessao. |
| **Deploy no meio da jornada** | Rollback + Full snapshot consolidado | Estado pode divergir entre versoes de codigo. Rollback garante base consistente. Full snapshot consolida no novo formato. |

---

## 🏗️ Parte 6: KODA State Machine com Persistencia (koda_state_machine.py)

Esta e a integracao final: a state machine da jornada KODA com persistencia completa em SQLite.

```python
# koda_state_machine.py
import json
import sqlite3
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Optional, Dict, Any, Tuple

from db import init_db, get_connection
from session_store import (
    create_session, get_session, update_session_phase,
    upsert_customer_profile, get_customer_profile, save_cart, get_cart,
    save_turn, get_recent_turns
)
from checkpoint import (
    create_full_snapshot, create_delta_checkpoint,
    should_full_snapshot, compute_delta, get_last_full_snapshot
)

class JourneyPhase(Enum):
    """Fases da jornada de compra do KODA."""
    WELCOME = "welcome"
    DISCOVERY = "discovery"
    RECOMMENDATION = "recommendation"
    CART = "cart"
    PAYMENT = "payment"
    FULFILLMENT = "fulfillment"
    FOLLOW_UP = "follow_up"
    CLOSED = "closed"

class KodaStateMachine:
    """
    State machine da jornada KODA com persistencia completa em SQLite.

    Caracteristicas:
    - Estado sobrevive a reinicializacoes de processo
    - Checkpoints automaticos em transicoes de fase
    - Isolamento: cada fase tem seu proprio handler
    - Audit trail completo de cada transicao

    Uso:
        koda = KodaStateMachine("wa_2026_05_26_pedro")
        response, phase = koda.process_message("Quero whey protein")
        print(response)  # "Oi! Qual seu objetivo de treino?"
    """

    def __init__(self, session_id: str, db_path: Optional[Path] = None):
        self.session_id = session_id
        self.db_path = db_path
        self.conn = init_db(db_path)
        self.last_full_snapshot_turn = 0

        # Garante que a sessao existe (ou carrega existente)
        session = get_session(session_id, conn=self.conn)
        if session is None:
            create_session(session_id, conn=self.conn)
            create_full_snapshot(session_id, 0, "welcome", conn=self.conn)
            self.turn_number = 0
            self.current_phase = JourneyPhase.WELCOME
        else:
            self.current_phase = JourneyPhase(session["current_phase"])
            # Determina turn_number a partir do banco
            last_turn = self.conn.execute(
                "SELECT MAX(turn_number) as max_turn FROM conversation_turns WHERE session_id = ?",
                (session_id,)
            ).fetchone()
            self.turn_number = last_turn["max_turn"] or 0

            # Recupera o turno do ultimo full snapshot
            last_full = get_last_full_snapshot(session_id, conn=self.conn)
            if last_full:
                self.last_full_snapshot_turn = last_full.get("turn_number", 0)

    def process_message(self, customer_message: str) -> Tuple[str, JourneyPhase]:
        """
        Processa uma mensagem do cliente na fase atual.

        Fluxo para cada mensagem:
        1. Incrementa turn_number
        2. Salva a mensagem do cliente como turn
        3. Roteia para o handler da fase atual
        4. Handler retorna (resposta, proxima_fase)
        5. Se houve transicao de fase, cria full snapshot
        6. Senao, cria delta checkpoint
        7. Salva a resposta como turn

        Returns:
            Tuple com (mensagem_de_resposta, fase_atualizada)
        """
        self.turn_number += 1

        # Salva mensagem do cliente
        save_turn(self.session_id, self.turn_number, "customer",
                  customer_message, self.current_phase.value, conn=self.conn)

        # Captura estado antes do processamento (para delta)
        previous_state = self._capture_current_state()

        # Roteia para o handler
        handlers = {
            JourneyPhase.WELCOME: self._handle_welcome,
            JourneyPhase.DISCOVERY: self._handle_discovery,
            JourneyPhase.RECOMMENDATION: self._handle_recommendation,
            JourneyPhase.CART: self._handle_cart,
            JourneyPhase.PAYMENT: self._handle_payment,
            JourneyPhase.FULFILLMENT: self._handle_fulfillment,
            JourneyPhase.FOLLOW_UP: self._handle_follow_up,
        }

        handler = handlers.get(self.current_phase)
        if handler is None:
            response = "Sessao em estado desconhecido. Reiniciando atendimento."
            self.current_phase = JourneyPhase.WELCOME
            update_session_phase(self.session_id, "welcome", conn=self.conn)
        else:
            response, next_phase = handler(customer_message)
            old_phase = self.current_phase

            if next_phase != self.current_phase:
                # Transicao de fase → FULL SNAPSHOT
                self.current_phase = next_phase
                update_session_phase(self.session_id, next_phase.value, conn=self.conn)
                create_full_snapshot(
                    self.session_id, self.turn_number, next_phase.value, conn=self.conn
                )
                self.last_full_snapshot_turn = self.turn_number
            else:
                # Mesmo fase → verifica se precisa de delta ou full
                current_state = self._capture_current_state()
                delta = compute_delta(previous_state, current_state)

                if should_full_snapshot(self.turn_number, self.current_phase.value,
                                        self.last_full_snapshot_turn):
                    create_full_snapshot(
                        self.session_id, self.turn_number, self.current_phase.value, conn=self.conn
                    )
                    self.last_full_snapshot_turn = self.turn_number
                elif delta:
                    last_full = get_last_full_snapshot(self.session_id, conn=self.conn)
                    if last_full:
                        create_delta_checkpoint(
                            self.session_id, self.turn_number,
                            self.current_phase.value, last_full["checkpoint_id"],
                            delta, conn=self.conn
                        )

        # Salva resposta do KODA
        save_turn(self.session_id, self.turn_number + 0.5, "koda",
                  response, self.current_phase.value, conn=self.conn)

        return response, self.current_phase

    def _capture_current_state(self) -> Dict[str, Any]:
        """Captura o estado atual para computacao de delta."""
        session = get_session(self.session_id, conn=self.conn)
        customer_id = session.get("customer_id") if session else None
        profile = get_customer_profile(customer_id, conn=self.conn) if customer_id else None
        cart = get_cart(self.session_id, conn=self.conn)

        return {
            "phase": self.current_phase.value,
            "turn_number": self.turn_number,
            "customer_profile": profile,
            "cart": cart
        }

    # ========================================================================
    # HANDLERS DE FASE
    # ========================================================================

    def _handle_welcome(self, message: str) -> Tuple[str, JourneyPhase]:
        """Fase WELCOME: saudacao inicial e encaminhamento para discovery."""
        customer_id = f"cust_{self.session_id}"

        # Atualiza sessao com customer_id
        self.conn.execute(
            "UPDATE sessions SET customer_id = ? WHERE session_id = ?",
            (customer_id, self.session_id)
        )
        self.conn.commit()

        response = (
            "Oi! Eu sou o KODA, seu assistente de suplementos. "
            "Pra te ajudar melhor, me conta: qual o seu objetivo de treino "
            "e voce tem alguma restricao alimentar?"
        )
        return response, JourneyPhase.DISCOVERY

    def _handle_discovery(self, message: str) -> Tuple[str, JourneyPhase]:
        """Fase DISCOVERY: coleta de perfil e preferencias do cliente."""
        session = get_session(self.session_id, conn=self.conn)
        customer_id = session["customer_id"]

        # Extrai informacoes da mensagem (simplificado; em producao usaria LLM)
        restrictions = []
        if any(term in message.lower() for term in ["lactose", "leite", "queijo"]):
            restrictions.append("lactose")
        if any(term in message.lower() for term in ["gluten", "trigo", "farinha"]):
            restrictions.append("gluten")
        if any(term in message.lower() for term in ["amendoim", "castanha", "nozes"]):
            restrictions.append("amendoim")

        training_goal = None
        if any(term in message.lower() for term in ["massa", "ganhar", "hipertrofia", "crescer"]):
            training_goal = "hypertrophy"
        elif any(term in message.lower() for term in ["emagrecer", "secar", "definir", "peso"]):
            training_goal = "weight_loss"
        elif any(term in message.lower() for term in ["resistencia", "cardio", "corrida"]):
            training_goal = "endurance"

        # Salva perfil
        upsert_customer_profile(
            customer_id=customer_id,
            dietary_restrictions=restrictions if restrictions else None,
            training_goal=training_goal,
            conn=self.conn
        )

        # Verifica se ja temos informacao suficiente para avancar
        profile = get_customer_profile(customer_id, conn=self.conn)
        if profile and profile.get("training_goal") and profile.get("budget_max_brl"):
            # Perfil completo — avanca para recomendacao
            response = (
                f"Perfil completo! Seu objetivo: {training_goal or 'nao definido'}. "
                f"Restricoes: {', '.join(restrictions) if restrictions else 'nenhuma'}. "
                "Vou buscar as melhores opcoes pra voce."
            )
            return response, JourneyPhase.RECOMMENDATION

        # Ainda precisa de mais informacao
        if not training_goal:
            response = "Entendi! E qual o seu objetivo principal? Ganhar massa, emagrecer ou resistencia?"
        elif not profile or not profile.get("budget_max_brl"):
            response = "Otimo! E qual o orcamento maximo que voce tem em mente por mes?"
        else:
            response = "Perfeito! Mais alguma preferencia? Sabor, marca, tipo de embalagem?"
        return response, JourneyPhase.DISCOVERY

    def _handle_recommendation(self, message: str) -> Tuple[str, JourneyPhase]:
        """Fase RECOMMENDATION: comparacao e sugestao de produtos."""
        # Em producao, isso consultaria o catalogo e usaria LLM para gerar recomendacao
        response = (
            "Com base no seu perfil, separei 3 opcoes que se encaixam bem. "
            "Quer que eu monte o carrinho com a melhor opcao?"
        )
        return response, JourneyPhase.CART

    def _handle_cart(self, message: str) -> Tuple[str, JourneyPhase]:
        """Fase CART: montagem e confirmacao do carrinho."""
        session = get_session(self.session_id, conn=self.conn)
        customer_id = session["customer_id"]

        if "sim" in message.lower() or "monta" in message.lower() or "ok" in message.lower():
            # Monta carrinho com produto exemplo
            items = [
                {"sku": "WHEY-ISO-BAUN-900", "name": "Whey Protein Isolado Baunilha 900g",
                 "qty": 1, "unit_price_brl": 189.90},
                {"sku": "CREA-MONO-300", "name": "Creatina Monohidratada 300g",
                 "qty": 1, "unit_price_brl": 59.90},
            ]
            total = sum(item["unit_price_brl"] * item["qty"] for item in items)

            save_cart(
                session_id=self.session_id,
                customer_id=customer_id,
                items=items,
                total_brl=total,
                shipping_city="Sao Paulo",
                shipping_zone="Vila Mariana",
                status="draft",
                conn=self.conn
            )

            response = (
                f"Carrinho montado com {len(items)} itens. Total: R$ {total:.2f}. "
                "Posso gerar o link de pagamento?"
            )
        else:
            response = "Sem problemas! Me diga quais produtos voce prefere e eu monto o carrinho."

        return response, JourneyPhase.CART

    def _handle_payment(self, message: str) -> Tuple[str, JourneyPhase]:
        """Fase PAYMENT: geracao de link de pagamento e confirmacao."""
        cart = get_cart(self.session_id, conn=self.conn)

        if not cart:
            return "Nao encontrei seu carrinho. Vamos montar de novo?", JourneyPhase.CART

        if "sim" in message.lower() or "pode" in message.lower() or "gerar" in message.lower():
            payment_link = f"https://pay.koda.app/order/{self.session_id}"

            # Atualiza carrinho com link de pagamento
            save_cart(
                session_id=self.session_id,
                customer_id=cart["customer_id"],
                items=cart["items"],
                total_brl=cart["total_brl"],
                shipping_city=cart.get("shipping_city"),
                shipping_zone=cart.get("shipping_zone"),
                status="confirmed",
                payment_link=payment_link,
                conn=self.conn
            )

            response = f"Link de pagamento gerado: {payment_link}"
            return response, JourneyPhase.FULFILLMENT
        else:
            response = "Tudo bem. Me avise quando quiser prosseguir com o pagamento."
            return response, JourneyPhase.PAYMENT

    def _handle_fulfillment(self, message: str) -> Tuple[str, JourneyPhase]:
        """Fase FULFILLMENT: pos-venda e acompanhamento de entrega."""
        response = (
            "Seu pedido foi confirmado! Em ate 3 dias uteis voce recebe "
            "a confirmacao de envio. Vou te avisar quando sair para entrega."
        )
        return response, JourneyPhase.FOLLOW_UP

    def _handle_follow_up(self, message: str) -> Tuple[str, JourneyPhase]:
        """Fase FOLLOW_UP: acompanhamento pos-entrega."""
        response = (
            "Que bom falar com voce de novo! Como foi sua experiencia "
            "com os produtos? Esta satisfeito com os resultados?"
        )
        return response, JourneyPhase.CLOSED

    def close(self) -> None:
        """Encerra a state machine e fecha a conexao com o banco."""
        self.conn.close()
```

---

## 🧪 Parte 7: Testes de Recovery (test_recovery.py)

Testes que **simulam falhas reais** e verificam se o estado e recuperado corretamente.

```python
# test_recovery.py
import json
import os
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

from db import init_db, get_connection, SCHEMA_SQL
from session_store import (
    create_session, get_session, update_session_phase,
    upsert_customer_profile, save_cart, get_cart
)
from checkpoint import (
    create_full_snapshot, create_delta_checkpoint,
    get_last_full_snapshot, get_checkpoints_since
)
from recovery import (
    rollback_to_last_checkpoint, SagaCompensation, detect_and_recover
)
from koda_state_machine import KodaStateMachine, JourneyPhase


class TestStatePersistence(unittest.TestCase):
    """Testes de persistencia de estado com SQLite."""

    def setUp(self):
        """Cria banco temporario para cada teste."""
        self.tmp_dir = tempfile.mkdtemp()
        self.db_path = Path(self.tmp_dir) / "test_koda.db"
        self.conn = init_db(self.db_path)

    def tearDown(self):
        """Limpa o banco temporario."""
        self.conn.close()
        import shutil
        shutil.rmtree(self.tmp_dir, ignore_errors=True)

    # ========================================================================
    # TESTES DE SESSAO E PERFIL
    # ========================================================================

    def test_create_and_get_session(self):
        """Sessao criada deve ser recuperavel com todos os campos."""
        session = create_session("wa_test_001", conn=self.conn)
        self.assertEqual(session["session_id"], "wa_test_001")
        self.assertEqual(session["current_phase"], "welcome")
        self.assertEqual(session["status"], "active")

        recovered = get_session("wa_test_001", conn=self.conn)
        self.assertEqual(recovered["session_id"], "wa_test_001")

    def test_session_not_found_returns_none(self):
        """Sessao inexistente deve retornar None."""
        result = get_session("wa_nonexistent", conn=self.conn)
        self.assertIsNone(result)

    def test_update_session_phase(self):
        """Transicao de fase deve ser persistida e auditada."""
        create_session("wa_test_002", conn=self.conn)
        update_session_phase("wa_test_002", "discovery", conn=self.conn)

        session = get_session("wa_test_002", conn=self.conn)
        self.assertEqual(session["current_phase"], "discovery")

        # Verifica audit trail
        events = self.conn.execute(
            "SELECT * FROM system_events WHERE session_id = ? AND event_type = 'phase_transition'",
            ("wa_test_002",)
        ).fetchall()
        self.assertEqual(len(events), 1)
        event_data = json.loads(events[0]["event_data_json"])
        self.assertEqual(event_data["from"], "welcome")
        self.assertEqual(event_data["to"], "discovery")

    def test_upsert_customer_profile(self):
        """Perfil deve ser criado e atualizado corretamente."""
        profile = upsert_customer_profile(
            "cust_001",
            name="Pedro",
            dietary_restrictions=["gluten", "lactose"],
            training_goal="hypertrophy",
            budget_max_brl=380.0,
            conn=self.conn
        )
        self.assertEqual(profile["name"], "Pedro")
        self.assertEqual(profile["dietary_restrictions"], ["gluten", "lactose"])
        self.assertEqual(profile["budget_max_brl"], 380.0)

        # Atualiza parcial (so muda budget)
        updated = upsert_customer_profile(
            "cust_001",
            budget_max_brl=500.0,
            conn=self.conn
        )
        self.assertEqual(updated["name"], "Pedro")  # Nao foi sobrescrito
        self.assertEqual(updated["budget_max_brl"], 500.0)  # Foi atualizado

    def test_save_and_get_cart(self):
        """Carrinho deve ser salvo e recuperado com itens corretos."""
        create_session("wa_test_cart", conn=self.conn)

        items = [
            {"sku": "WHEY-001", "name": "Whey Protein", "qty": 2, "unit_price_brl": 89.90},
            {"sku": "CREA-001", "name": "Creatina", "qty": 1, "unit_price_brl": 59.90},
        ]
        total = sum(i["unit_price_brl"] * i["qty"] for i in items)

        cart = save_cart(
            "wa_test_cart", "cust_cart", items, total,
            shipping_city="Sao Paulo", conn=self.conn
        )
        self.assertEqual(cart["total_brl"], total)
        self.assertEqual(len(cart["items"]), 2)
        self.assertEqual(cart["items"][0]["sku"], "WHEY-001")

        recovered = get_cart("wa_test_cart", conn=self.conn)
        self.assertEqual(recovered["total_brl"], total)

    # ========================================================================
    # TESTES DE CHECKPOINT
    # ========================================================================

    def test_create_full_snapshot(self):
        """Full snapshot deve conter estado completo da sessao."""
        create_session("wa_ckpt_test", conn=self.conn)
        upsert_customer_profile("cust_ckpt", name="Test User", conn=self.conn)

        self.conn.execute(
            "UPDATE sessions SET customer_id = ? WHERE session_id = ?",
            ("cust_ckpt", "wa_ckpt_test")
        )
        self.conn.commit()

        ckpt_id = create_full_snapshot("wa_ckpt_test", 5, "discovery", conn=self.conn)
        self.assertIsNotNone(ckpt_id)

        # Verifica que o checkpoint foi salvo
        last = get_last_full_snapshot("wa_ckpt_test", conn=self.conn)
        self.assertIsNotNone(last)
        self.assertEqual(last["phase"], "discovery")
        self.assertIn("customer_profile", last["state_snapshot"])

    def test_delta_checkpoint_captures_changes(self):
        """Delta deve conter apenas os campos que mudaram."""
        create_session("wa_delta_test", conn=self.conn)
        full_id = create_full_snapshot("wa_delta_test", 1, "welcome", conn=self.conn)

        changes = {"cart": {"items": [{"sku": "A", "qty": 1}], "total_brl": 99.90}}
        delta_id = create_delta_checkpoint(
            "wa_delta_test", 2, "welcome", full_id, changes, conn=self.conn
        )

        deltas = get_checkpoints_since("wa_delta_test", full_id, conn=self.conn)
        self.assertEqual(len(deltas), 1)
        self.assertEqual(deltas[0]["checkpoint_type"], "delta")
        self.assertIn("changes", deltas[0]["state_snapshot"])

    # ========================================================================
    # TESTES DE RECOVERY
    # ========================================================================

    def test_rollback_recovers_state_after_simulated_crash(self):
        """
        Simula um crash e verifica se rollback recupera o estado.

        Cenario:
        1. KODA processa 5 mensagens, criando checkpoints
        2. Servidor "crasha" (simulado fechando conexao)
        3. Nova conexao abre e executa rollback
        4. Estado deve ser recuperado do ultimo checkpoint
        """
        # Fase 1: Operacao normal
        create_session("wa_crash_test", conn=self.conn)
        upsert_customer_profile("cust_crash", name="Cliente Crash",
                                dietary_restrictions=["gluten"], conn=self.conn)

        self.conn.execute(
            "UPDATE sessions SET customer_id = ? WHERE session_id = ?",
            ("cust_crash", "wa_crash_test")
        )
        self.conn.commit()

        # Cria checkpoints em varias fases
        create_full_snapshot("wa_crash_test", 1, "welcome", conn=self.conn)
        update_session_phase("wa_crash_test", "discovery", conn=self.conn)
        create_full_snapshot("wa_crash_test", 3, "discovery", conn=self.conn)
        update_session_phase("wa_crash_test", "cart", conn=self.conn)

        save_cart("wa_crash_test", "cust_crash",
                  [{"sku": "WHEY", "qty": 1, "name": "Whey", "unit_price_brl": 99.90}],
                  99.90, conn=self.conn)
        create_full_snapshot("wa_crash_test", 5, "cart", conn=self.conn)

        # Fase 2: Simula crash fechando a conexao
        self.conn.close()

        # Fase 3: Recovery — nova conexao
        recovery_conn = init_db(self.db_path)  # Nova conexao, como apos reboot

        state = rollback_to_last_checkpoint("wa_crash_test", conn=recovery_conn)

        self.assertIsNotNone(state, "Estado nao foi recuperado apos crash simulado")
        self.assertIn("customer_profile", state)
        self.assertIn("cart", state)
        self.assertEqual(state["cart"]["total_brl"], 99.90)

        # Verifica que a sessao foi restaurada para a fase correta
        session = get_session("wa_crash_test", conn=recovery_conn)
        self.assertEqual(session["current_phase"], "cart")

        # Verifica audit trail de recovery
        events = recovery_conn.execute(
            "SELECT * FROM system_events WHERE session_id = ? AND event_type = 'recovery_completed'",
            ("wa_crash_test",)
        ).fetchall()
        self.assertGreater(len(events), 0, "Evento de recovery nao foi registrado")

        recovery_conn.close()

    def test_recovery_from_empty_state(self):
        """Sessao sem checkpoints deve retornar None no rollback."""
        create_session("wa_empty_recovery", conn=self.conn)
        state = rollback_to_last_checkpoint("wa_empty_recovery", conn=self.conn)
        self.assertIsNone(state, "Sessao sem checkpoints nao deveria retornar estado")

    # ========================================================================
    # TESTES DE SAGA (COMPENSACAO)
    # ========================================================================

    def test_saga_successful_execution(self):
        """Saga deve executar todos os passos em ordem quando nao ha falhas."""
        create_session("wa_saga_test", conn=self.conn)

        executed_steps = []
        compensated_steps = []

        def reserve_inventory(ctx):
            executed_steps.append("reserve_inventory")
            return {"reserved": True, "items": ["WHEY", "CREA"]}

        def undo_reserve(result):
            compensated_steps.append("undo_reserve")

        def generate_payment(ctx):
            executed_steps.append("generate_payment")
            return {"link": "https://pay.koda.app/test"}

        def undo_payment(result):
            compensated_steps.append("undo_payment")

        saga = SagaCompensation("wa_saga_test", conn=self.conn)
        saga.add_step("reserve_inventory", reserve_inventory, undo_reserve)
        saga.add_step("generate_payment", generate_payment, undo_payment)

        result = saga.execute()
        saga.close()

        self.assertEqual(result["status"], "success")
        self.assertEqual(executed_steps, ["reserve_inventory", "generate_payment"])
        self.assertEqual(compensated_steps, [], "Nada deveria ter sido compensado")
        self.assertEqual(result["steps"], ["reserve_inventory", "generate_payment"])

    def test_saga_rollback_on_failure(self):
        """Se um passo falha, todos os anteriores devem ser compensados."""
        create_session("wa_saga_fail", conn=self.conn)

        compensated_steps = []

        def step_one(ctx):
            return {"step": 1}

        def undo_one(result):
            compensated_steps.append("undo_one")

        def step_two_fails(ctx):
            raise ValueError("Falha simulada no passo 2")

        def undo_two(result):
            compensated_steps.append("undo_two")

        saga = SagaCompensation("wa_saga_fail", conn=self.conn)
        saga.add_step("step_one", step_one, undo_one)
        saga.add_step("step_two", step_two_fails, undo_two)

        result = saga.execute()
        saga.close()

        self.assertEqual(result["status"], "rolled_back")
        self.assertIn("Falha simulada", result["error"])
        self.assertEqual(compensated_steps, ["undo_one"],
                         "Apenas step_one deveria ser compensado")
        self.assertEqual(result["steps_completed"], ["step_one"])

    # ========================================================================
    # TESTES DA STATE MACHINE KODA
    # ========================================================================

    def test_state_machine_full_journey(self):
        """Jornada completa deve transitar por todas as fases."""
        koda = KodaStateMachine("wa_jornada_teste", db_path=self.db_path)

        # Welcome → Discovery
        response, phase = koda.process_message("Oi")
        self.assertEqual(phase, JourneyPhase.DISCOVERY)
        self.assertIn("objetivo", response.lower())

        # Discovery → Discovery (coleta mais info)
        response, phase = koda.process_message(
            "Quero ganhar massa e tenho intolerancia a lactose"
        )
        self.assertEqual(phase, JourneyPhase.DISCOVERY)
        self.assertIn("orcamento", response.lower())

        # Discovery → Recommendation (info completa)
        response, phase = koda.process_message("Meu orcamento e 400 reais")
        self.assertEqual(phase, JourneyPhase.RECOMMENDATION)

        # Recommendation → CART
        response, phase = koda.process_message("Sim, monta o carrinho")
        self.assertEqual(phase, JourneyPhase.CART)

        # CART → PAYMENT
        response, phase = koda.process_message("Sim, gera o pagamento")
        self.assertEqual(phase, JourneyPhase.FULFILLMENT)

        # FULFILLMENT → FOLLOW_UP
        response, phase = koda.process_message("Ok, obrigado")
        self.assertEqual(phase, JourneyPhase.FOLLOW_UP)

        # FOLLOW_UP → CLOSED
        response, phase = koda.process_message("Foi otimo, gostei muito")
        self.assertEqual(phase, JourneyPhase.CLOSED)

        koda.close()

    def test_state_machine_survives_crash(self):
        """
        Teste critico: state machine deve sobreviver a um crash simulado.

        Cenario:
        1. KODA processa mensagens ate chegar na fase CART
        2. Simula crash (fecha state machine)
        3. Cria nova state machine com mesmo session_id
        4. Deve retomar da fase CART
        """
        # Fase 1: Processa ate CART
        koda1 = KodaStateMachine("wa_survive_test", db_path=self.db_path)
        koda1.process_message("Oi")  # → DISCOVERY
        koda1.process_message("Quero ganhar massa, intolerante a lactose")  # → DISCOVERY
        koda1.process_message("Orcamento 500 reais")  # → RECOMMENDATION
        koda1.process_message("Sim, monta o carrinho")  # → CART
        koda1.close()

        # Fase 2: Simula crash (fim do processo)
        del koda1

        # Fase 3: Nova state machine — deve retomar da fase CART
        koda2 = KodaStateMachine("wa_survive_test", db_path=self.db_path)

        # Verifica que retomou na fase correta
        self.assertEqual(koda2.current_phase, JourneyPhase.CART,
                         "State machine nao retomou da fase CART apos crash")

        # Continua a jornada
        response, phase = koda2.process_message("Sim, gera o pagamento")
        self.assertEqual(phase, JourneyPhase.FULFILLMENT)

        # Verifica que o carrinho foi preservado
        cart = get_cart("wa_survive_test", conn=koda2.conn)
        self.assertIsNotNone(cart, "Carrinho nao foi preservado apos crash")
        self.assertEqual(cart["total_brl"], 249.80)  # 189.90 + 59.90

        koda2.close()

    # ========================================================================
    # TESTES DE ATOMIC WRITE
    # ========================================================================

    def test_atomic_write_no_corruption(self):
        """Atomic write nao deve corromper arquivo em caso de falha simulada."""
        from atomic_write import atomic_write_json, atomic_read_json

        test_path = Path(self.tmp_dir) / "test_atomic.json"
        data = {"key": "value", "nested": {"a": 1, "b": [2, 3, 4]}}

        # Escreve normalmente
        atomic_write_json(test_path, data)
        recovered = atomic_read_json(test_path)
        self.assertEqual(recovered, data)

        # Simula falha de disco mockando fsync para lancar excecao
        original_data = {"original": "data"}
        atomic_write_json(test_path, original_data)

        with patch('os.fsync', side_effect=OSError("Simulated disk error")):
            try:
                atomic_write_json(test_path, {"should": "fail"})
            except OSError:
                pass  # Esperado

        # Arquivo original deve estar intacto
        recovered = atomic_read_json(test_path)
        self.assertEqual(recovered, original_data,
                         "Arquivo foi corrompido por atomic write com falha")


if __name__ == "__main__":
    unittest.main(verbosity=2)
```

### Como Executar os Testes

```bash
# Executa todos os testes
python -m pytest test_recovery.py -v

# Executa apenas testes de recovery
python -m pytest test_recovery.py -v -k "recovery"

# Executa apenas testes da state machine
python -m pytest test_recovery.py -v -k "state_machine"
```

### O Que Estes Testes Cobrem

| Teste | O Que Verifica | Por Que e Importante |
| --- | --- | --- |
| `test_create_and_get_session` | CRUD basico de sessao | Fundacao: sem isso, nada funciona |
| `test_update_session_phase` | Transicao de fase + audit trail | Garante rastreabilidade de cada mudanca |
| `test_upsert_customer_profile` | Criacao e atualizacao parcial de perfil | COALESCE no SQL garante que updates parciais nao sobrescrevam dados |
| `test_rollback_recovers_state_after_simulated_crash` | **Recovery apos crash** | Teste mais critico: simula crash real e verifica recuperacao |
| `test_saga_successful_execution` | Saga executa todos os passos | Fluxo feliz do padrao de compensacao |
| `test_saga_rollback_on_failure` | **Compensacao reverte passos anteriores** | Garante que falhas parciais nao deixam estado inconsistente |
| `test_state_machine_survives_crash` | **State machine sobrevive a reinicializacao** | Teste end-to-end: fecha processo e retoma do estado correto |
| `test_atomic_write_no_corruption` | Arquivo permanece intacto apos falha de escrita | Garante que atomic_write_json funciona como prometido |

---

## 📊 Parte 8: Diagrama da Arquitetura Completa

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                    ARQUITETURA DE STATE PERSISTENCE DO KODA                    │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                         CAMADA DE AGENTES                             │    │
│  │                                                                      │    │
│  │   ┌──────────┐      ┌──────────┐      ┌──────────┐                  │    │
│  │   │ Planner  │─────►│ Generator│─────►│ Evaluator│                  │    │
│  │   │ (decide  │      │ (cria    │      │ (valida  │                  │    │
│  │   │  o que   │      │  resposta│      │  resposta│                  │    │
│  │   │  fazer)  │      │          │      │          │                  │    │
│  │   └────┬─────┘      └────┬─────┘      └────┬─────┘                  │    │
│  │        │                 │                 │                         │    │
│  │        └────────┬────────┴────────┬────────┘                         │    │
│  │                 │                 │                                  │    │
│  └─────────────────┼─────────────────┼──────────────────────────────────┘    │
│                    │                 │                                       │
│                    ▼                 ▼                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                    PERSISTENCE LAYER                                  │    │
│  │                                                                      │    │
│  │  ┌────────────────┐  ┌────────────────┐  ┌────────────────────┐     │    │
│  │  │ Session Store  │  │   Checkpoint   │  │    Recovery        │     │    │
│  │  │                │  │   Manager      │  │    Engine          │     │    │
│  │  │ • create       │  │                │  │                    │     │    │
│  │  │ • get/update   │  │ • full snap    │  │ • rollback         │     │    │
│  │  │ • profile CRUD │  │ • delta        │  │ • replay           │     │    │
│  │  │ • cart CRUD    │  │ • hybrid       │  │ • compensation     │     │    │
│  │  │ • turns CRUD   │  │ • consolidate  │  │ • detect & recover │     │    │
│  │  └───────┬────────┘  └───────┬────────┘  └─────────┬──────────┘     │    │
│  │          │                   │                      │                │    │
│  │          └───────────────────┼──────────────────────┘                │    │
│  │                              │                                       │    │
│  └──────────────────────────────┼───────────────────────────────────────┘    │
│                                 │                                            │
│                                 ▼                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                        SQLite DATABASE                                │    │
│  │                      (koda_state.db, WAL mode)                       │    │
│  │                                                                      │    │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │    │
│  │  │ sessions │ │customer  │ │conver-   │ │cart_state│ │checkpoints│  │    │
│  │  │          │ │_profile  │ │sation_   │ │          │ │          │  │    │
│  │  │• id (PK) │ │          │ │turns     │ │• id (PK) │ │• id (PK) │  │    │
│  │  │• phase   │ │• id (PK) │ │          │ │• items   │ │• session │  │    │
│  │  │• status  │ │• restrict│ │• turn #  │ │• total   │ │• phase   │  │    │
│  │  │• timestamps│ │• budget │ │• role    │ │• status  │ │• snapshot│  │    │
│  │  │          │ │• prefs   │ │• content │ │• link    │ │• type    │  │    │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘  │    │
│  │                                                                      │    │
│  │  ┌──────────────┐                                                    │    │
│  │  │system_events │  ← Audit trail de TODAS as operacoes               │    │
│  │  │• session_id  │                                                    │    │
│  │  │• event_type  │  (started, transition, checkpoint, crash,          │    │
│  │  │• data (JSON) │   recovery, compensation, error)                   │    │
│  │  │• timestamp   │                                                    │    │
│  │  └──────────────┘                                                    │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                     KODA STATE MACHINE                                │    │
│  │                                                                      │    │
│  │  WELCOME ──► DISCOVERY ──► RECOMMENDATION ──► CART ──► PAYMENT       │    │
│  │                                                     │                │    │
│  │                                                     ▼                │    │
│  │                                          FULFILLMENT ──► FOLLOW_UP   │    │
│  │                                                              │       │    │
│  │                                                              ▼       │    │
│  │                                                            CLOSED    │    │
│  │                                                                      │    │
│  │  Cada transicao de fase dispara:                                     │    │
│  │   1. update_session_phase() no SQLite                                 │    │
│  │   2. create_full_snapshot() com estado completo                       │    │
│  │   3. system_events INSERT para audit trail                            │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                         RECOVERY FLOW                                 │    │
│  │                                                                      │    │
│  │  Processo inicia                                                     │    │
│  │       │                                                              │    │
│  │       ▼                                                              │    │
│  │  detect_and_recover(session_id)                                       │    │
│  │       │                                                              │    │
│  │       ▼                                                              │    │
│  │  Ha checkpoints? ──nao──► Estado inicial (nova sessao)               │    │
│  │       │                                                              │    │
│  │       sim                                                            │    │
│  │       ▼                                                              │    │
│  │  Carrega ultimo FULL SNAPSHOT                                        │    │
│  │       │                                                              │    │
│  │       ▼                                                              │    │
│  │  Aplica DELTAS em ordem                                              │    │
│  │       │                                                              │    │
│  │       ▼                                                              │    │
│  │  Estado reconstruido ──► KODA retoma do ponto exato                  │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 📊 Parte 9: Tabela Comparativa — Estrategias de Coordenacao com Persistencia

State persistence transforma cada estrategia de coordenacao de agentes. Sem persistencia, qualquer falha de um agente significa retrabalho total. Com persistencia, apenas o agente que falhou precisa reexecutar.

| Estrategia | Sem Persistencia | Com Persistencia (SQLite) | Reducao de Retrabalho |
| --- | --- | --- | --- |
| **Sequencial** (Planner → Generator → Evaluator) | Se o Evaluator falha, perde-se `plan.json` e `generation.json`. Recomeca tudo do Planner. Tempo: 3x o normal. | Arquivos salvos como checkpoints no SQLite. Evaluator reexecuta lendo estado do banco. Planner e Generator nao precisam refazer. Tempo: 1.1x o normal. | ~90% |
| **Paralelo** (multiplos Generators concorrentes) | Se um Generator falha, nao ha como saber quais terminaram. Ou refaz todos ou assume inconsistencia. | Cada Generator salva seu output no banco com `checkpoint_type='generator_output'`. Sistema verifica `SELECT COUNT(*)` e reexecuta apenas os `NULL`. | ~95% (1/N dos generators) |
| **Event-driven** (agentes reagem a eventos) | Se um agente perde um evento, ele nunca reage. Estado fica inconsistente sem deteccao. | Eventos persistidos em `system_events`. Agente processa do ultimo evento confirmado (`SELECT * WHERE event_id > last_processed`). | Eventos perdidos: <0.1% |
| **Round-robin** (agentes se alternam) | Perda de turno = estado inconsistente sem deteccao. | Turnos salvos em `conversation_turns`. Estado reconstruido de `checkpoints`. Sistema sabe exatamente qual turno foi o ultimo processado. | Recuperacao total |
| **Priority-based** (agentes com prioridade) | Se agente de alta prioridade falha, o de baixa pode processar antes, causando out-of-order. | Fila de prioridade no banco: `SELECT ... ORDER BY priority DESC, created_at ASC`. Mesmo apos crash, ordem e preservada. | Garantia de ordenacao |

### Exemplo Concreto: Sequencial com Persistencia

```
Cenario: Planner → Generator → Evaluator, 3 checkpoints.

SEM PERSISTENCIA:
  1. Planner roda (2s)        → plan em memoria
  2. Generator roda (3s)      → generation em memoria
  3. Evaluator CRASHA (0.5s)   → estado perdido
  4. Reinicia: Planner (2s) + Generator (3s) + Evaluator (1s) = 6s
  Total: 2 + 3 + 0.5 + 6 = 11.5 segundos, 2x retrabalho

COM PERSISTENCIA (SQLite):
  1. Planner roda (2s)        → INSERT INTO checkpoints (plan)
  2. Generator roda (3s)      → INSERT INTO checkpoints (generation)
  3. Evaluator CRASHA (0.5s)   → ultimo checkpoint: generator
  4. Recovery: SELECT do checkpoint do generator (0.1s)
  5. Evaluator reexecuta (1s)
  Total: 2 + 3 + 0.5 + 0.1 + 1 = 6.6 segundos, 0x retrabalho
```

---

## 🎓 Parte 10: Aplicacao KODA — Cenarios Reais

### Cenario 1: Crash Durante Pagamento

```
21:02  KODA: "Pedro, seu carrinho esta pronto. Total: R$ 379,60."
       └─ SQLite: checkpoint criado, phase=CART, cart salvo

21:03  Pedro: "Pode finalizar."
       └─ SQLite: phase→PAYMENT, payment_link gerado
       └─ SQLite: checkpoint criado, phase=PAYMENT

[SERVIDOR REINICIA — 21:03:45]

21:04  Pedro: "Deu erro no pagamento."

       └─ detect_and_recover("wa_pedro"):
           1. Encontra session status='active'
           2. Ultimo checkpoint: phase=PAYMENT, payment_link=...
           3. rollback_to_last_checkpoint() → estado com payment_link
           4. replay_turns_from_checkpoint() → reexecuta turno 21

21:04  KODA: "Pedro, seu carrinho com 4 itens esta seguro.
             O link de pagamento: https://pay.koda.app/ord_99281
             Quer que eu gere um novo?"

       └─ Cliente nao percebeu a reinicializacao.
```

### Cenario 2: Retomada Apos 3 Dias

```
Sexta 18:00  Pedro monta carrinho mas nao finaliza.
             └─ SQLite: phase=CART, cart_status='draft'

[3 dias depois]

Segunda 14:00  Pedro: "Oi KODA, quero finalizar aquela compra"

               └─ detect_and_recover("wa_pedro"):
                   1. Session existe, status='active'
                   2. Ultimo checkpoint: phase=CART, cart com 4 itens
                   3. Estado recuperado com carrinho intacto

               KODA: "Bem-vindo de volta, Pedro! Seu carrinho ainda
                      esta aqui: Whey Isolado, Creatina, Pre-treino
                      e Multivitaminico. Total: R$ 379,60.
                      Quer finalizar a compra?"
```

### Cenario 3: Timeout de API com Retry

```
Turno 15:  Generator tenta chamar Claude API.
           └─ Erro 529 (Overloaded) apos 60s

           └─ Codigo:
              try:
                  response = call_claude_api(prompt)
              except TimeoutError:
                  # Rollback para checkpoint do turno 14
                  state = rollback_to_last_checkpoint(session_id)
                  # Retry com backoff
                  time.sleep(2 ** attempt)
                  response = call_claude_api(prompt)

           └─ Cliente recebe resposta no turno 15 com 2s de atraso.
              Nao percebeu que houve 3 tentativas internas.
```

---

## ⚠️ Parte 11: Anti-Padroes e Como Evita-los

| Anti-Padrao | Como Este Codigo Evita |
| --- | --- |
| **"Salvar no final"** (estado so em memoria, salva no fim da jornada) | `process_message()` salva estado a cada turno. Transicoes de fase forcam full snapshot. |
| **"Arquivo gigante unico"** (um `state.json` de 5 MB) | Estado particionado em 5 tabelas SQLite (sessions, customer_profile, cart_state, conversation_turns, checkpoints). Cada tabela tem responsabilidade unica. |
| **"Redis sem persistencia"** | Usamos SQLite com WAL mode e `PRAGMA wal_checkpoint(TRUNCATE)`. Dados estao em disco, nao em RAM. |
| **"Checkpoint sem metadados de fase"** | Todo checkpoint inclui `phase`, `turn_number` e `checkpoint_type`. O campo `state_snapshot` contem o JSON completo. |
| **"Sobrescrever arquivo sem atomic write"** | `atomic_write_json()` usa write-temp-then-rename com `os.fsync()`. Nao existe cenario de corrupcao. |
| **"Silent fail on load"** (captura `Exception` e retorna `{}`) | `rollback_to_last_checkpoint()` tenta checkpoint anterior antes de inicializar estado vazio. `detect_and_recover()` registra evento `error_logged`. |

---

## 🧠 O Que Voce Aprendeu

- [x] **Implementar SQLite schema para sessoes, perfil, carrinho, turns e checkpoints** com constraints CHECK, foreign keys e indices otimizados.

- [x] **Construir uma persistence layer (session_store.py)** que isola o resto do codigo dos detalhes do SQLite, com suporte a conexoes compartilhadas e upserts idempotentes.

- [x] **Implementar checkpointing hibrido** (full snapshot + delta incremental) com regras claras: full em transicoes de fase, delta em turns intermediarios, consolidacao a cada 10 turns.

- [x] **Escrever `atomic_write_json()`** usando write-temp-then-rename com `os.fsync()`, garantindo que nenhum arquivo de estado fique corrompido.

- [x] **Implementar 3 estrategias de recovery**: rollback (para falhas transientes), replay (para reconstrucao deterministica), e compensacao/Saga (para sistemas externos).

- [x] **Construir `detect_and_recover()`** que identifica automaticamente se uma sessao precisa de recovery e aplica a estrategia correta.

- [x] **Integrar tudo na `KodaStateMachine`**: state machine da jornada KODA com persistencia completa, checkpoints automaticos, e transicoes auditaveis.

- [x] **Testar recovery com falhas simuladas**: testes que fecham a conexao com o banco, recriam uma nova (simulando reboot), e verificam que o estado foi recuperado.

- [x] **Testar o padrao Saga**: verificando que passos sao executados em ordem e compensados na ordem inversa em caso de falha.

- [x] **Testar que a state machine sobrevive a um crash**: fecha a state machine no meio da jornada, cria uma nova com o mesmo session_id, e verifica que retoma da fase correta com os dados intactos.

- [x] **Compreender o impacto de state persistence no retrabalho**: com persistencia, falhas de agentes em pipeline sequencial causam ~10% de retrabalho (vs 100% sem persistencia).

- [x] **Saber escolher entre SQLite, JSON files e Redis** baseado em criterios como schema enforcement, query power, complexidade operacional e durabilidade.

- [x] **Identificar anti-padroes de persistencia** e saber como corrigi-los: save tardio, arquivo unico gigante, Redis sem AOF, sobrescrita nao-atomica, silent fail.

---

## 📚 Referencias

- `curriculum/03-nivel-3-advanced-architecture/02-state-persistence.md` — modulo teorico que fundamenta esta solucao
- `curriculum/03-nivel-3-advanced-architecture/01-multi-agent-systems.md` — coordenacao entre agentes que consomem estado persistido
- `curriculum/03-nivel-3-advanced-architecture/03-file-based-coordination.md` — coordenacao por arquivos JSON como complemento ao SQLite
- `curriculum/02-nivel-2-practical-patterns/04-trace-reading.md` — como usar os dados do `system_events` para debugar falhas
- Documentacao oficial do SQLite: https://sqlite.org/wal.html — WAL mode, atomic commit, locking
- Documentacao do Python sqlite3: https://docs.python.org/3/library/sqlite3.html

---

## 💭 Reflexao Final

State persistence nao e sobre evitar que servidores reiniciem.

Servidores sempre vao reiniciar. APIs sempre vao dar timeout. Deploys sempre vao acontecer no meio de uma jornada.

State persistence e sobre o que acontece **depois**.

Quando Pedro perdeu 47 minutos de conversa e o KODA respondeu "Oi! Como posso te ajudar?", o problema nao era o servidor — era a arquitetura que tratava memoria de processo como se fosse permanente.

Cada checkpoint que voce salva e uma mensagem para o cliente: "Seu tempo importa. Eu lembro de voce."

Cada recovery bem-sucedido e uma falha que o cliente nunca soube que aconteceu.

Isso e o que separa um chatbot de um agente confiavel.

E confianca, no final, e o unico produto que importa.

---

*Solucao completa do Exercicio 2 — State Persistence com SQLite e Recovery*
*Nivel 3 — Arquitetura Avancada | Maio 2026*
*Escrito com foco em codigo funcional, clareza arquitetural e respeito ao tempo do leitor.*
