"""SQLite-хранилище для персистентных данных бота.

Заменяет глобальные dict-ы: last_messages, anon_threads, anon_replies,
saved_first_messages — на таблицы в SQLite.

Интерфейс полностью совместим со старым dict API:
    d[key] = value
    d[key]
    d.get(key, default)
    d.pop(key, default)
    key in d

FSM-хранилище остаётся MemoryStorage (через aiogram),
так как aiogram 3.x не имеет встроенного SQLiteStorage.
"""

import json
import sqlite3
import threading
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "bot_state.db"

_local = threading.local()


def _get_connection() -> sqlite3.Connection:
    conn = getattr(_local, "conn", None)
    if conn is None:
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA synchronous=NORMAL;")
        _init_tables(conn)
        _local.conn = conn
    return conn


def _init_tables(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS bot_kv (
            namespace TEXT NOT NULL,
            key INTEGER NOT NULL,
            value TEXT NOT NULL DEFAULT '',
            PRIMARY KEY (namespace, key)
        );
        """
    )
    conn.commit()


def close_db() -> None:
    conn = getattr(_local, "conn", None)
    if conn is not None:
        conn.close()
        _local.conn = None


# ──────────────────────────────────────────────────────────────────────
# Dict-совместимый класс
# ──────────────────────────────────────────────────────────────────────


class SQLiteDict:
    """Обёртка над таблицей bot_kv, имитирующая dict[int, int | list[int]].

    namespace — имя таблицы (last_messages, anon_threads, …).
    key и value — значение, сериализованное в JSON (для списков)
    или plain int (для одиночных чисел).
    """

    def __init__(self, namespace: str) -> None:
        self.namespace = namespace

    def _fetchone(self, key: int) -> sqlite3.Row | None:
        return _get_connection().execute(
            "SELECT value FROM bot_kv WHERE namespace = ? AND key = ?",
            (self.namespace, key),
        ).fetchone()

    # ── чтение ──

    def get(self, key: int, default=None) -> int | list[int] | None:
        row = self._fetchone(key)
        if row is None:
            return default
        raw = row["value"]
        if raw.startswith("["):
            return json.loads(raw)
        try:
            return int(raw)
        except ValueError:
            return raw  # для bool-совместимых значений (True/False)

    def __getitem__(self, key: int) -> int | list[int]:
        val = self.get(key)
        if val is None:
            raise KeyError(key)
        return val

    def __contains__(self, key: int) -> bool:
        return self._fetchone(key) is not None

    # ── запись ──

    def __setitem__(self, key: int, value: int | list[int] | bool) -> None:
        serialized = json.dumps(value) if isinstance(value, list) else str(int(value) if isinstance(value, bool) else value)
        _get_connection().execute(
            """INSERT INTO bot_kv (namespace, key, value)
               VALUES (?, ?, ?)
               ON CONFLICT(namespace, key) DO UPDATE SET value = excluded.value""",
            (self.namespace, key, serialized),
        )
        _get_connection().commit()

    # ── удаление ──

    def pop(self, key: int, default=None) -> int | list[int] | None:
        val = self.get(key)
        if val is None:
            return default
        _get_connection().execute(
            "DELETE FROM bot_kv WHERE namespace = ? AND key = ?",
            (self.namespace, key),
        )
        _get_connection().commit()
        return val


# ──────────────────────────────────────────────────────────────────────
# Экземпляры — полная замена старым глобальным dict-ам
# ──────────────────────────────────────────────────────────────────────

last_messages = SQLiteDict("last_messages")
anon_threads = SQLiteDict("anon_threads")
anon_replies = SQLiteDict("anon_replies")
saved_first_messages = SQLiteDict("saved_first_messages")