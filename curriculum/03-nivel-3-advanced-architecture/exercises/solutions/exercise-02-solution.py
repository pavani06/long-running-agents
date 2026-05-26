import hashlib
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
    """Gerencia checkpoints de sessões KODA em SQLite."""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.initialize_schema()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("PRAGMA journal_mode = WAL")
        conn.execute("PRAGMA busy_timeout = 5000")
        return conn

    def initialize_schema(self) -> None:
        with self._connect() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS sessions (
                    session_id TEXT PRIMARY KEY,
                    customer_id TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'active',
                    current_phase TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS checkpoints (
                    checkpoint_id TEXT PRIMARY KEY,
                    session_id TEXT NOT NULL REFERENCES sessions(session_id),
                    checkpoint_number INTEGER NOT NULL,
                    phase TEXT NOT NULL,
                    turn_number INTEGER NOT NULL,
                    snapshot_json TEXT NOT NULL,
                    snapshot_sha256 TEXT NOT NULL,
                    safe_to_resume INTEGER NOT NULL CHECK (safe_to_resume IN (0, 1)),
                    created_at TEXT NOT NULL,
                    UNIQUE(session_id, checkpoint_number)
                );

                CREATE TABLE IF NOT EXISTS audit_events (
                    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL REFERENCES sessions(session_id),
                    event_type TEXT NOT NULL,
                    details_json TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );

                CREATE INDEX IF NOT EXISTS idx_checkpoints_latest
                ON checkpoints(session_id, checkpoint_number DESC);

                CREATE INDEX IF NOT EXISTS idx_audit_session
                ON audit_events(session_id, created_at);
                """
            )

    def create_initial_state(self, session_id: str, customer_id: str) -> SessionState:
        return SessionState(session_id=session_id, customer_id=customer_id)

    def create_session(self, state: SessionState) -> None:
        now = utc_now()
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO sessions (session_id, customer_id, status, current_phase, created_at, updated_at)
                VALUES (?, ?, 'active', ?, ?, ?)
                ON CONFLICT(session_id) DO UPDATE SET
                    customer_id = excluded.customer_id,
                    current_phase = excluded.current_phase,
                    updated_at = excluded.updated_at
                """,
                (state.session_id, state.customer_id, state.phase.value, now, now),
            )

    def create_full_checkpoint(
        self,
        state: SessionState,
        reason: str,
        safe_to_resume: bool = True,
    ) -> str:
        state.updated_at = utc_now()
        snapshot = state.to_snapshot()
        snapshot_json = json.dumps(snapshot, ensure_ascii=False, sort_keys=True)
        snapshot_hash = hashlib.sha256(snapshot_json.encode("utf-8")).hexdigest()
        created_at = utc_now()

        with self._connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            try:
                conn.execute(
                    """
                    INSERT INTO sessions (session_id, customer_id, status, current_phase, created_at, updated_at)
                    VALUES (?, ?, 'active', ?, ?, ?)
                    ON CONFLICT(session_id) DO UPDATE SET
                        customer_id = excluded.customer_id,
                        current_phase = excluded.current_phase,
                        updated_at = excluded.updated_at
                    """,
                    (state.session_id, state.customer_id, state.phase.value, created_at, created_at),
                )
                row = conn.execute(
                    "SELECT COALESCE(MAX(checkpoint_number), 0) + 1 AS next_number FROM checkpoints WHERE session_id = ?",
                    (state.session_id,),
                ).fetchone()
                checkpoint_number = int(row["next_number"])
                checkpoint_id = f"ckpt_{state.session_id}_{checkpoint_number:04d}"
                conn.execute(
                    """
                    INSERT INTO checkpoints (
                        checkpoint_id, session_id, checkpoint_number, phase, turn_number,
                        snapshot_json, snapshot_sha256, safe_to_resume, created_at
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        checkpoint_id,
                        state.session_id,
                        checkpoint_number,
                        state.phase.value,
                        state.turn_number,
                        snapshot_json,
                        snapshot_hash,
                        1 if safe_to_resume else 0,
                        created_at,
                    ),
                )
                audit_details = {
                    "checkpoint_id": checkpoint_id,
                    "checkpoint_number": checkpoint_number,
                    "reason": reason,
                    "phase": state.phase.value,
                    "turn_number": state.turn_number,
                    "safe_to_resume": safe_to_resume,
                }
                conn.execute(
                    """
                    INSERT INTO audit_events (session_id, event_type, details_json, created_at)
                    VALUES (?, 'checkpoint_created', ?, ?)
                    """,
                    (state.session_id, json.dumps(audit_details, ensure_ascii=False, sort_keys=True), created_at),
                )
                conn.commit()
                return checkpoint_id
            except Exception:
                conn.rollback()
                raise

    def load_latest_checkpoint(self, session_id: str) -> Optional[Tuple[str, SessionState]]:
        with self._connect() as conn:
            row = conn.execute(
                """
                SELECT checkpoint_id, snapshot_json, snapshot_sha256
                FROM checkpoints
                WHERE session_id = ? AND safe_to_resume = 1
                ORDER BY checkpoint_number DESC
                LIMIT 1
                """,
                (session_id,),
            ).fetchone()
        if row is None:
            return None
        return row["checkpoint_id"], self._state_from_row(row)

    def rollback_to_checkpoint(
        self,
        session_id: str,
        checkpoint_id: Optional[str] = None,
    ) -> Tuple[str, SessionState]:
        if checkpoint_id is None:
            latest = self.load_latest_checkpoint(session_id)
            if latest is None:
                raise ValueError(f"Nenhum checkpoint encontrado para {session_id}")
            selected_checkpoint_id, state = latest
        else:
            with self._connect() as conn:
                row = conn.execute(
                    """
                    SELECT checkpoint_id, snapshot_json, snapshot_sha256
                    FROM checkpoints
                    WHERE session_id = ? AND checkpoint_id = ?
                    """,
                    (session_id, checkpoint_id),
                ).fetchone()
            if row is None:
                raise ValueError(f"Checkpoint {checkpoint_id} não encontrado para {session_id}")
            selected_checkpoint_id = row["checkpoint_id"]
            state = self._state_from_row(row)

        created_at = utc_now()
        details = {"checkpoint_id": selected_checkpoint_id, "phase": state.phase.value, "turn_number": state.turn_number}
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO audit_events (session_id, event_type, details_json, created_at)
                VALUES (?, 'rollback', ?, ?)
                """,
                (session_id, json.dumps(details, ensure_ascii=False, sort_keys=True), created_at),
            )
        return selected_checkpoint_id, state

    def list_checkpoints(self, session_id: str) -> List[Dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT checkpoint_id, checkpoint_number, phase, turn_number, safe_to_resume, created_at
                FROM checkpoints
                WHERE session_id = ?
                ORDER BY checkpoint_number ASC
                """,
                (session_id,),
            ).fetchall()
        return [dict(row) for row in rows]

    def _state_from_row(self, row: sqlite3.Row) -> SessionState:
        snapshot_json = row["snapshot_json"]
        expected_hash = row["snapshot_sha256"]
        actual_hash = hashlib.sha256(snapshot_json.encode("utf-8")).hexdigest()
        if actual_hash != expected_hash:
            raise ValueError("Checksum do checkpoint não confere")
        snapshot = json.loads(snapshot_json)
        return SessionState.from_snapshot(snapshot)


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


def test_checkpoint_audit_trail() -> None:
    temp_dir, manager = create_test_manager()
    try:
        session = KodaSession(manager, "wa_pedro_audit", "cust_pedro")
        session.process_customer_message("Oi")
        session.process_customer_message("Quero ganhar massa, sem gluten, orçamento 380")
        checkpoints = manager.list_checkpoints("wa_pedro_audit")
        assert len(checkpoints) == 3
        assert checkpoints[0]["checkpoint_number"] == 1
        assert checkpoints[-1]["phase"] == JourneyPhase.RECOMMENDATION.value
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
    test_checkpoint_audit_trail()
    print("Teste 5 passou: audit trail lista checkpoints em ordem")
    print("Todos os testes passaram")


if __name__ == "__main__":
    run_all_tests()
