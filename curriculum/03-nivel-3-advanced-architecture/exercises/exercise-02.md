---
title: "Exercício 2: Implementar Checkpointing e Recovery com SQLite"
type: curriculum-exercise
nivel: 3
aliases: []
tags: [curriculo-conteudo, nivel-3, exercicio, checkpointing, crash-recovery, state-persistence, snapshot, rollback, atomic-writing, audit-trail, session-state, journey-phase, sqlite, wal-mode, python]
last_updated: 2026-06-10
---
# 🛡️ Exercício 2: Implementar Checkpointing e Recovery com SQLite

## State Persistence para KODA sobreviver a crashes sem esquecer Pedro

**Nível:** 3 - Advanced Architecture  
**Tempo Estimado:** 60-90 minutos  
**Dificuldade:** ⭐⭐⭐⭐ (Avançada)  
**Pré-requisito:** Ter lido `02-state-persistence.md` e completado o módulo de state machine do KODA  
**Status:** Hands-On Prático com Recovery Real

---

## 📖 O Problema Real

Quarta-feira, 21h15.

Pedro passou 47 minutos conversando com o KODA no WhatsApp. Ele explicou que quer ganhar massa, evita glúten, prefere produtos bem avaliados e tem orçamento de R$ 380.

O KODA montou uma compra grande:

```text
21:02 KODA: Pedro, seu carrinho está pronto:
- Whey Isolado Baunilha 900g: R$ 189,90
- Creatina Monohidratada 300g: R$ 59,90
- Pré-treino Sem Cafeína 150g: R$ 79,90
- Multivitamínico 60 caps: R$ 49,90
Total: R$ 379,60

Posso gerar o link de pagamento?
21:03 Pedro: Pode. Finaliza aí.
```

O link foi gerado. Pedro abriu o pagamento. Antes de concluir, o servidor reiniciou.

Quando Pedro voltou:

```text
21:04 Pedro: Deu erro no pagamento. Tenta de novo?
21:04 KODA: Oi! Como posso te ajudar?
21:05 Pedro: Eu estava finalizando a compra.
21:05 KODA: Claro! Qual seu objetivo de treino?
```

Pedro não abandonou porque o produto era ruim. Ele abandonou porque o KODA esqueceu tudo.

Neste exercício, você vai implementar a camada que evita esse tipo de perda: **checkpointing com SQLite, WAL mode, snapshot completo, recovery e rollback**.

O módulo pai `02-state-persistence.md` explica por que isso importa: state persistence transforma falhas reais de produção em pausas recuperáveis. Aqui você vai codificar essa promessa.

---

## 🎯 Objetivo

Você vai implementar um **CheckpointManager para KODA** que:

1. Persiste sessões e checkpoints em SQLite com `journal_mode=WAL`.
2. Salva snapshots completos do estado de uma conversa em pontos seguros.
3. Recupera a sessão mais recente após um crash de processo.
4. Permite rollback para checkpoint específico quando uma tentativa falha.
5. Garante escrita atômica usando transações SQLite.
6. Mantém audit trail mínimo para explicar por que cada checkpoint existe.

**Resultado Final:** você entenderá como KODA preserva perfil, carrinho, fase da jornada e link de pagamento mesmo quando o processo morre no pior momento.

---

## 📋 Requisitos

### Funcional

- [ ] Classe `CheckpointManager` usando SQLite.
- [ ] SQLite configurado com `PRAGMA journal_mode = WAL`.
- [ ] Schema para `sessions`, `checkpoints` e `audit_events`.
- [ ] Estado de sessão com perfil do cliente, carrinho, fase, turno e próxima ação esperada.
- [ ] Criação de checkpoint com snapshot completo.
- [ ] Recovery pelo checkpoint mais recente após simular crash.
- [ ] Rollback para checkpoint específico ou último checkpoint seguro.
- [ ] Audit trail de criação de checkpoint e rollback.
- [ ] Testes que simulam a jornada de Pedro.

### Técnico

- [ ] Python 3.8+ sem dependências externas.
- [ ] `sqlite3`, `dataclasses`, `enum`, `json`, `tempfile` e `pathlib`.
- [ ] Type hints nos métodos públicos.
- [ ] Tratamento de erro em transações com `commit` e `rollback` explícitos.
- [ ] Serialização JSON determinística com `sort_keys=True`.
- [ ] Nenhuma escrita parcial deve substituir o último checkpoint válido.

### Validação

- [ ] WAL mode confirmado via `PRAGMA journal_mode`.
- [ ] Recovery carrega `phase=payment` após crash no pagamento.
- [ ] Perfil de Pedro preserva restrição a glúten e orçamento de R$ 380.
- [ ] Carrinho recuperado contém 4 itens e total de R$ 379,60.
- [ ] Rollback para checkpoint inicial remove carrinho adicionado depois.
- [ ] Falha ao criar checkpoint inválido não corrompe o checkpoint anterior.

---

## 🚀 Starter Code

Copie o código abaixo para um arquivo local, por exemplo `exercise_02_checkpointing.py`. Ele já contém a simulação do KODA e os testes. Sua tarefa é preencher os pontos marcados como `PONTO DE IMPLEMENTAÇÃO`.

```python
import json
import sqlite3
import tempfile
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


def utc_now() -> str:
    """Retorna timestamp UTC em ISO-8601."""
    return datetime.now(timezone.utc).isoformat()


class JourneyPhase(Enum):
    """Fases principais da jornada KODA."""
    WELCOME = "welcome"
    DISCOVERY = "discovery"
    RECOMMENDATION = "recommendation"
    CART = "cart"
    PAYMENT = "payment"
    FULFILLMENT = "fulfillment"
    FOLLOW_UP = "follow_up"
    CLOSED = "closed"


@dataclass
class CartItem:
    sku: str
    name: str
    qty: int
    unit_price_brl: float

    def subtotal_brl(self) -> float:
        return round(self.qty * self.unit_price_brl, 2)


@dataclass
class SessionState:
    session_id: str
    customer_id: str
    customer_profile: Dict[str, Any] = field(default_factory=dict)
    cart_items: List[CartItem] = field(default_factory=list)
    phase: JourneyPhase = JourneyPhase.WELCOME
    turn_number: int = 0
    last_customer_message: Optional[str] = None
    last_koda_response: Optional[str] = None
    payment_link: Optional[str] = None
    next_expected_action: str = "collect_customer_goal"
    updated_at: str = field(default_factory=utc_now)

    def cart_total_brl(self) -> float:
        return round(sum(item.subtotal_brl() for item in self.cart_items), 2)

    def to_snapshot(self) -> Dict[str, Any]:
        """Converte estado em dict serializável para o checkpoint."""
        return {
            "session_id": self.session_id,
            "customer_id": self.customer_id,
            "customer_profile": self.customer_profile,
            "cart_items": [asdict(item) for item in self.cart_items],
            "cart_total_brl": self.cart_total_brl(),
            "phase": self.phase.value,
            "turn_number": self.turn_number,
            "last_customer_message": self.last_customer_message,
            "last_koda_response": self.last_koda_response,
            "payment_link": self.payment_link,
            "next_expected_action": self.next_expected_action,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_snapshot(cls, snapshot: Dict[str, Any]) -> "SessionState":
        """Reconstrói estado a partir de snapshot salvo no SQLite."""
        items = [CartItem(**item) for item in snapshot.get("cart_items", [])]
        return cls(
            session_id=snapshot["session_id"],
            customer_id=snapshot["customer_id"],
            customer_profile=snapshot.get("customer_profile", {}),
            cart_items=items,
            phase=JourneyPhase(snapshot.get("phase", JourneyPhase.WELCOME.value)),
            turn_number=int(snapshot.get("turn_number", 0)),
            last_customer_message=snapshot.get("last_customer_message"),
            last_koda_response=snapshot.get("last_koda_response"),
            payment_link=snapshot.get("payment_link"),
            next_expected_action=snapshot.get("next_expected_action", "continue"),
            updated_at=snapshot.get("updated_at", utc_now()),
        )


class CheckpointManager:
    """
    Gerencia checkpoints de sessões KODA em SQLite.

    Sua implementação deve seguir o módulo `02-state-persistence.md`:
    - SQLite em WAL mode para concorrência de leitura.
    - Schema explícito para sessões, checkpoints e audit events.
    - Snapshot completo em pontos seguros da jornada.
    - Recovery pelo checkpoint mais recente.
    - Rollback para checkpoint específico ou último checkpoint seguro.
    - Escritas atômicas usando transações.
    """

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.initialize_schema()

    def _connect(self) -> sqlite3.Connection:
        """
        Abre conexão SQLite configurada para durabilidade.

        PONTO DE IMPLEMENTAÇÃO:
        - Use sqlite3.connect(self.db_path)
        - Ative row_factory para sqlite3.Row
        - Execute PRAGMA foreign_keys = ON
        - Execute PRAGMA journal_mode = WAL
        - Execute PRAGMA busy_timeout = 5000
        - Retorne a conexão
        """
        raise NotImplementedError("configure a conexão SQLite com WAL e foreign keys")

    def initialize_schema(self) -> None:
        """
        Cria as tabelas necessárias.

        PONTO DE IMPLEMENTAÇÃO:
        Crie pelo menos estas tabelas:
        - sessions: session_id, customer_id, status, current_phase, created_at, updated_at
        - checkpoints: checkpoint_id, session_id, checkpoint_number, phase, turn_number,
          snapshot_json, created_at
        - audit_events: event_id, session_id, event_type, details_json, created_at

        Requisitos importantes:
        - checkpoints.session_id referencia sessions.session_id
        - checkpoint_number deve permitir ordenar o histórico
        - use índices para latest checkpoint por sessão
        """
        raise NotImplementedError("crie schema SQLite para sessões, checkpoints e auditoria")

    def create_initial_state(self, session_id: str, customer_id: str) -> SessionState:
        """Cria estado inicial da sessão antes da primeira mensagem."""
        return SessionState(session_id=session_id, customer_id=customer_id)

    def create_session(self, state: SessionState) -> None:
        """
        Registra ou atualiza a linha da sessão.

        PONTO DE IMPLEMENTAÇÃO:
        - Use INSERT com ON CONFLICT(session_id) DO UPDATE
        - Atualize current_phase e updated_at
        - Não apague checkpoints existentes
        """
        raise NotImplementedError("grave a sessão sem apagar histórico")

    def create_full_checkpoint(
        self,
        state: SessionState,
        reason: str,
        safe_to_resume: bool = True,
    ) -> str:
        """
        Salva snapshot completo do estado atual.

        PONTO DE IMPLEMENTAÇÃO:
        - Gere snapshot com state.to_snapshot()
        - Serialize com json.dumps(sort_keys=True)
        - Abra transação com BEGIN IMMEDIATE
        - Faça upsert em sessions
        - Calcule checkpoint_number = último número + 1
        - Insira checkpoint
        - Insira audit_event com reason e safe_to_resume
        - Commit no final
        - Rollback se qualquer operação falhar
        - Retorne checkpoint_id
        """
        raise NotImplementedError("implemente checkpoint completo com transação atômica")

    def load_latest_checkpoint(self, session_id: str) -> Optional[Tuple[str, SessionState]]:
        """
        Carrega o checkpoint mais recente de uma sessão.

        PONTO DE IMPLEMENTAÇÃO:
        - Busque checkpoints da sessão ordenando por checkpoint_number desc
        - Se não existir checkpoint, retorne None
        - Faça json.loads(snapshot_json)
        - Reconstrua SessionState.from_snapshot(snapshot)
        - Retorne (checkpoint_id, state)
        """
        raise NotImplementedError("carregue o checkpoint mais recente")

    def rollback_to_checkpoint(
        self,
        session_id: str,
        checkpoint_id: Optional[str] = None,
    ) -> Tuple[str, SessionState]:
        """
        Recupera estado a partir de checkpoint específico ou do último seguro.

        PONTO DE IMPLEMENTAÇÃO:
        - Se checkpoint_id for None, use load_latest_checkpoint
        - Se checkpoint_id for informado, busque exatamente esse checkpoint
        - Registre audit_event com event_type='rollback'
        - Retorne (checkpoint_id, state)
        - Levante ValueError se checkpoint não existir
        """
        raise NotImplementedError("implemente rollback auditável")

    def list_checkpoints(self, session_id: str) -> List[Dict[str, Any]]:
        """
        Lista checkpoints para debug e auditoria.

        PONTO DE IMPLEMENTAÇÃO:
        - Retorne lista ordenada por checkpoint_number
        - Inclua checkpoint_id, phase, turn_number, created_at
        """
        raise NotImplementedError("liste checkpoints da sessão")


class KodaSession:
    """Simula uma sessão KODA usando checkpoints duráveis."""

    def __init__(self, manager: CheckpointManager, session_id: str, customer_id: str):
        self.manager = manager
        recovered = self.manager.load_latest_checkpoint(session_id)
        if recovered:
            self.last_checkpoint_id, self.state = recovered
        else:
            self.state = self.manager.create_initial_state(session_id, customer_id)
            self.last_checkpoint_id = self.manager.create_full_checkpoint(
                self.state,
                reason="session_started",
            )

    def process_customer_message(self, message: str) -> str:
        """Processa uma mensagem e salva checkpoint ao final do turno."""
        self.state.turn_number += 1
        self.state.last_customer_message = message

        if self.state.phase == JourneyPhase.WELCOME:
            response = self._handle_welcome(message)
        elif self.state.phase == JourneyPhase.DISCOVERY:
            response = self._handle_discovery(message)
        elif self.state.phase == JourneyPhase.RECOMMENDATION:
            response = self._handle_recommendation(message)
        elif self.state.phase == JourneyPhase.CART:
            response = self._handle_cart(message)
        elif self.state.phase == JourneyPhase.PAYMENT:
            response = self._handle_payment(message)
        else:
            response = "Pedro, sua sessão está encerrada com segurança."

        self.state.last_koda_response = response
        self.state.updated_at = utc_now()
        self.last_checkpoint_id = self.manager.create_full_checkpoint(
            self.state,
            reason=f"turn_{self.state.turn_number}_completed",
        )
        return response

    def _handle_welcome(self, message: str) -> str:
        self.state.phase = JourneyPhase.DISCOVERY
        self.state.next_expected_action = "collect_profile_and_budget"
        return "Pedro, me conta seu objetivo de treino, restrições e orçamento."

    def _handle_discovery(self, message: str) -> str:
        text = message.lower()
        profile = self.state.customer_profile
        profile["name"] = "Pedro"
        profile["goal"] = "ganho de massa"
        if "glúten" in text or "gluten" in text:
            profile["dietary_restrictions"] = ["gluten"]
        if "380" in text:
            profile["budget_brl"] = 380.0
        profile["preferences"] = ["boa avaliação", "sem cafeína no pré-treino"]
        self.state.phase = JourneyPhase.RECOMMENDATION
        self.state.next_expected_action = "confirm_recommendation"
        return "Entendi: ganho de massa, sem glúten e orçamento de R$ 380. Vou montar uma recomendação."

    def _handle_recommendation(self, message: str) -> str:
        self.state.cart_items = [
            CartItem("WHEY-ISO-BAUN-900", "Whey Isolado Baunilha 900g", 1, 189.90),
            CartItem("CREA-MONO-300", "Creatina Monohidratada 300g", 1, 59.90),
            CartItem("PRE-NOCAF-150", "Pré-treino Sem Cafeína 150g", 1, 79.90),
            CartItem("MULTI-VIT-60", "Multivitamínico 60 caps", 1, 49.90),
        ]
        self.state.phase = JourneyPhase.CART
        self.state.next_expected_action = "confirm_payment_link"
        total = self.state.cart_total_brl()
        return f"Pedro, seu carrinho está pronto por R$ {total:.2f}. Posso gerar o link de pagamento?"

    def _handle_cart(self, message: str) -> str:
        self.state.payment_link = f"https://pay.koda.app/{self.state.session_id}"
        self.state.phase = JourneyPhase.PAYMENT
        self.state.next_expected_action = "payment_confirmation"
        return f"Link gerado: {self.state.payment_link}. Se der erro, eu consigo recuperar seu carrinho."

    def _handle_payment(self, message: str) -> str:
        total = self.state.cart_total_brl()
        if self.state.payment_link:
            return f"Pedro, seu carrinho de R$ {total:.2f} está seguro. Posso reenviar {self.state.payment_link}."
        return "Pedro, seu carrinho está seguro. Vou gerar um novo link."


def create_test_manager() -> Tuple[tempfile.TemporaryDirectory, CheckpointManager]:
    temp_dir = tempfile.TemporaryDirectory()
    db_path = str(Path(temp_dir.name) / "koda_state.db")
    return temp_dir, CheckpointManager(db_path)


def test_wal_mode_enabled() -> None:
    temp_dir, manager = create_test_manager()
    try:
        with manager._connect() as conn:
            mode = conn.execute("PRAGMA journal_mode").fetchone()[0]
        assert mode == "wal", "SQLite deve operar em WAL mode"
    finally:
        temp_dir.cleanup()


def test_recovery_after_crash() -> None:
    temp_dir, manager = create_test_manager()
    try:
        session = KodaSession(manager, "wa_pedro_001", "cust_pedro")
        session.process_customer_message("Oi")
        session.process_customer_message("Quero ganhar massa, sem glúten, orçamento 380")
        session.process_customer_message("Pode montar o carrinho")
        session.process_customer_message("Pode gerar o link")

        recovered_session = KodaSession(manager, "wa_pedro_001", "cust_pedro")
        assert recovered_session.state.phase == JourneyPhase.PAYMENT
        assert recovered_session.state.customer_profile["name"] == "Pedro"
        assert recovered_session.state.cart_total_brl() == 379.60
        assert recovered_session.state.payment_link is not None
    finally:
        temp_dir.cleanup()


def test_rollback_to_specific_checkpoint() -> None:
    temp_dir, manager = create_test_manager()
    try:
        state = manager.create_initial_state("wa_pedro_rollback", "cust_pedro")
        first_checkpoint = manager.create_full_checkpoint(state, reason="clean_start")
        state.phase = JourneyPhase.CART
        state.cart_items.append(CartItem("WHEY-ISO-BAUN-900", "Whey Isolado Baunilha 900g", 1, 189.90))
        manager.create_full_checkpoint(state, reason="cart_added")

        rolled_checkpoint, rolled_state = manager.rollback_to_checkpoint(
            "wa_pedro_rollback",
            checkpoint_id=first_checkpoint,
        )
        assert rolled_checkpoint == first_checkpoint
        assert rolled_state.phase == JourneyPhase.WELCOME
        assert rolled_state.cart_items == []
    finally:
        temp_dir.cleanup()


def test_failed_checkpoint_does_not_replace_latest() -> None:
    temp_dir, manager = create_test_manager()
    try:
        state = manager.create_initial_state("wa_pedro_atomic", "cust_pedro")
        checkpoint_id = manager.create_full_checkpoint(state, reason="valid_checkpoint")
        state.customer_profile["invalid_value"] = {"nao_serializa_em_json"}
        try:
            manager.create_full_checkpoint(state, reason="invalid_checkpoint")
        except TypeError:
            pass
        latest_id, latest_state = manager.load_latest_checkpoint("wa_pedro_atomic")
        assert latest_id == checkpoint_id
        assert "invalid_value" not in latest_state.customer_profile
    finally:
        temp_dir.cleanup()


def run_all_tests() -> None:
    print("=" * 70)
    print("EXERCÍCIO 2: CHECKPOINTING E RECOVERY COM SQLITE")
    print("=" * 70)
    test_wal_mode_enabled()
    print("Teste 1 passou: WAL mode ativo")
    test_recovery_after_crash()
    print("Teste 2 passou: recovery após crash recupera Pedro")
    test_rollback_to_specific_checkpoint()
    print("Teste 3 passou: rollback específico recupera estado anterior")
    test_failed_checkpoint_does_not_replace_latest()
    print("Teste 4 passou: falha de escrita não substitui checkpoint válido")
    print("Todos os testes passaram")


if __name__ == "__main__":
    print("Starter code carregado com sucesso.")
    print("Implemente os pontos marcados como PONTO DE IMPLEMENTAÇÃO e execute run_all_tests().")

```

---

## 🏗️ Como Começar

### Passo 1: Entender o Estado que Precisa Sobreviver

Leia `SessionState.to_snapshot()`. Este snapshot representa o mínimo necessário para o KODA retomar sem constranger Pedro:

- `customer_profile`: nome, objetivo, restrições, orçamento e preferências.
- `cart_items`: SKUs, nomes, quantidades e preços.
- `phase`: onde a conversa parou na state machine.
- `turn_number`: último turno processado.
- `payment_link`: link já gerado, quando existir.
- `next_expected_action`: o que o KODA espera do cliente.

Esse design segue o módulo `02-state-persistence.md`: checkpoint não é todo o histórico, é o subconjunto necessário para retomar com segurança.

### Passo 2: Implementar `_connect`

Configure cada conexão SQLite para operar como store durável:

```python
conn = sqlite3.connect(self.db_path)
conn.row_factory = sqlite3.Row
conn.execute("PRAGMA foreign_keys = ON")
conn.execute("PRAGMA journal_mode = WAL")
conn.execute("PRAGMA busy_timeout = 5000")
return conn
```

`WAL` permite múltiplos readers enquanto um writer grava. Para KODA, isso ajuda quando Generator, Evaluator e ferramentas de observabilidade leem estado enquanto um turno salva checkpoint.

### Passo 3: Criar o Schema

Crie três tabelas:

```sql
CREATE TABLE IF NOT EXISTS sessions (
    session_id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'active',
    current_phase TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
```

```sql
CREATE TABLE IF NOT EXISTS checkpoints (
    checkpoint_id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL REFERENCES sessions(session_id),
    checkpoint_number INTEGER NOT NULL,
    phase TEXT NOT NULL,
    turn_number INTEGER NOT NULL,
    snapshot_json TEXT NOT NULL,
    safe_to_resume INTEGER NOT NULL CHECK (safe_to_resume IN (0, 1)),
    created_at TEXT NOT NULL,
    UNIQUE(session_id, checkpoint_number)
);
```

```sql
CREATE TABLE IF NOT EXISTS audit_events (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL REFERENCES sessions(session_id),
    event_type TEXT NOT NULL,
    details_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);
```

Adicione índice para recuperar o último checkpoint rapidamente:

```sql
CREATE INDEX IF NOT EXISTS idx_checkpoints_latest
ON checkpoints(session_id, checkpoint_number DESC);
```

### Passo 4: Implementar Checkpoint Atômico

Em `create_full_checkpoint`, a ordem importa:

1. Atualize `state.updated_at`.
2. Gere `snapshot = state.to_snapshot()`.
3. Serialize com `json.dumps(snapshot, ensure_ascii=False, sort_keys=True)`.
4. Abra conexão.
5. Execute `BEGIN IMMEDIATE`.
6. Faça upsert na sessão.
7. Calcule o próximo `checkpoint_number`.
8. Insira checkpoint.
9. Insira audit event.
10. Execute `commit`.
11. Em exceção, execute `rollback` e relance o erro.

A transação é o padrão de escrita atômica aqui. Se o processo falhar no meio, SQLite descarta a transação incompleta.

### Passo 5: Implementar Recovery

`load_latest_checkpoint(session_id)` deve buscar o último checkpoint seguro:

```sql
SELECT checkpoint_id, snapshot_json
FROM checkpoints
WHERE session_id = ? AND safe_to_resume = 1
ORDER BY checkpoint_number DESC
LIMIT 1;
```

Depois:

```python
snapshot = json.loads(row["snapshot_json"])
state = SessionState.from_snapshot(snapshot)
return row["checkpoint_id"], state
```

Não use silent fail. Se JSON estiver corrompido, deixe o erro aparecer ou implemente fallback explícito para checkpoint anterior como desafio extra.

### Passo 6: Implementar Rollback

Rollback é recovery intencional:

- Sem `checkpoint_id`, volte ao último checkpoint seguro.
- Com `checkpoint_id`, carregue aquele ponto específico.
- Registre `audit_events.event_type = 'rollback'`.
- Retorne `(checkpoint_id, state)`.

Esse padrão cobre timeouts de LLM, falhas de pagamento e bugs detectados por evaluator.

### Passo 7: Rodar os Testes

Depois de implementar, execute:

```bash
python exercise_02_checkpointing.py
```

Durante desenvolvimento, você pode chamar `run_all_tests()` no final do arquivo. Todos os testes devem passar sem depender de rede, Redis ou APIs externas.

---

## 🎯 Desafios Extra

### Desafio 1: Delta Checkpoints

Implemente `create_delta_checkpoint(previous_state, current_state)` para salvar apenas campos alterados desde o último checkpoint. Depois implemente `restore_from_full_plus_deltas(session_id)`.

Critério de sucesso: recovery precisa produzir o mesmo `SessionState` do snapshot completo, mas com menos bytes gravados por turno.

### Desafio 2: Integração com Redis

Use Redis como camada de estado quente para `customer_profile` e `cart_items`, mantendo SQLite como fonte durável.

Critério de sucesso: se Redis for limpo, KODA consegue reconstruir o estado a partir do último checkpoint SQLite.

### Desafio 3: Multi-Agent Coordination com Persistência

Adicione estados parciais para Planner, Generator e Evaluator:

- `planner_state_json`
- `generation_state_json`
- `evaluation_state_json`

Critério de sucesso: se o crash acontecer após Planner mas antes de Evaluator, o sistema reexecuta apenas as etapas faltantes.

### Desafio 4: Checksum de Snapshot

Adicione coluna `snapshot_sha256` em `checkpoints` e valide o hash antes de carregar recovery.

Critério de sucesso: corrupção manual de `snapshot_json` deve ser detectada antes de reconstruir estado.

---

## 📊 Checklist de Implementação

- [ ] `_connect` ativa `foreign_keys`, `journal_mode=WAL` e `busy_timeout`.
- [ ] `initialize_schema` cria `sessions`.
- [ ] `initialize_schema` cria `checkpoints` com FK para `sessions`.
- [ ] `initialize_schema` cria `audit_events`.
- [ ] Índice `idx_checkpoints_latest` criado.
- [ ] `create_session` faz upsert sem apagar checkpoints.
- [ ] `create_full_checkpoint` usa snapshot completo.
- [ ] `create_full_checkpoint` usa `BEGIN IMMEDIATE`.
- [ ] `create_full_checkpoint` faz `commit` apenas após checkpoint e audit event.
- [ ] `create_full_checkpoint` faz `rollback` em erro.
- [ ] `load_latest_checkpoint` recupera o checkpoint mais recente.
- [ ] `load_latest_checkpoint` reconstrói `SessionState` corretamente.
- [ ] `rollback_to_checkpoint` funciona sem `checkpoint_id`.
- [ ] `rollback_to_checkpoint` funciona com `checkpoint_id` específico.
- [ ] `rollback_to_checkpoint` registra audit event.
- [ ] `list_checkpoints` retorna checkpoints ordenados.
- [ ] Teste de WAL passa.
- [ ] Teste de recovery após crash passa.
- [ ] Teste de rollback específico passa.
- [ ] Teste de atomicidade passa.

---

## 💡 Dicas de Implementação

**Dica 1:** Serialize antes de iniciar a transação quando quiser validar que o snapshot é JSON válido. Se preferir incluir a serialização dentro da transação, garanta `rollback` no `except`.

**Dica 2:** Use `checkpoint_number` como relógio lógico por sessão. Timestamps podem empatar em testes rápidos.

**Dica 3:** Não salve apenas o carrinho. O módulo pai chama isso de anti-padrão: checkpoint sem fase não diz se Pedro está montando carrinho, pagando ou aguardando confirmação.

**Dica 4:** Recovery deve ser explícito. Retornar estado vazio quando a leitura falha recria exatamente o bug que fez Pedro ir embora.

**Dica 5:** SQLite já fornece atomicidade. Use transações em vez de tentar simular atomic write manualmente.

**Dica 6:** Mantenha os testes em `tempfile.TemporaryDirectory()` para evitar sujeira local e garantir que cada execução começa com banco limpo.

---

## ✅ Validação Final

Sua implementação está correta se:

1. ✅ `test_wal_mode_enabled()` confirma `journal_mode = wal`.
2. ✅ `test_recovery_after_crash()` cria nova instância de `KodaSession` e recupera Pedro em `phase=payment`.
3. ✅ O carrinho recuperado tem total de R$ 379,60.
4. ✅ A restrição a glúten e o orçamento de R$ 380 continuam no perfil.
5. ✅ `test_rollback_to_specific_checkpoint()` volta para o estado inicial e remove itens adicionados depois.
6. ✅ `test_failed_checkpoint_does_not_replace_latest()` prova que uma escrita inválida não substitui o último checkpoint válido.
7. ✅ O código não depende de serviços externos.
8. ✅ O arquivo roda com Python 3.8+.

Para comparar com uma implementação completa, veja `solutions/exercise-02-solution.py` depois de concluir sua versão.

---

## 🎓 O Que Você Aprendeu

Após completar este exercício, você entende:

- ✅ Como desenhar schema SQLite para session state do KODA.
- ✅ Por que `WAL mode` melhora a convivência entre readers e writer.
- ✅ Como criar checkpoints com snapshot completo.
- ✅ Como recuperar estado depois de crash sem pedir que o cliente recomece.
- ✅ Como implementar rollback auditável.
- ✅ Como usar transações para evitar checkpoint parcial.
- ✅ Como testar state persistence simulando falhas reais.

**Próximo:** Exercício 3 - Persistência aplicada à coordenação entre agentes.

---

*Exercício 2 de Nível 3 | Curso Long-Running Agents | FutanBear Technical Program*
