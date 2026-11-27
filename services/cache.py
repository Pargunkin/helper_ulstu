"""Кэш file_id отправленных медиа для повторного использования.

Хранит соответствие: путь_к_файлу -> file_id (из Telegram).
При первом запуске читается из SQLite, при записи — синхронизируется туда же,
чтобы кэш переживал перезапуск бота.
"""

import json
import logging
import sqlite3
import threading
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "bot_state.db"

_local = threading.local()


def _get_conn() -> sqlite3.Connection:
    conn = getattr(_local, "conn", None)
    if conn is None:
        conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA synchronous=NORMAL;")
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS media_cache (
                filepath TEXT PRIMARY KEY,
                file_id  TEXT NOT NULL
            );
            """
        )
        conn.commit()
        _local.conn = conn
    return conn


def _load_all() -> dict[str, str]:
    """Загружает весь кэш из SQLite в память."""
    cache: dict[str, str] = {}
    try:
        rows = _get_conn().execute("SELECT filepath, file_id FROM media_cache").fetchall()
        for filepath, file_id in rows:
            cache[filepath] = file_id
    except Exception:
        logging.exception("Ошибка при загрузке media_cache из SQLite")
    return cache


def _save_one(filepath: str, file_id: str) -> None:
    """Сохраняет одну запись в SQLite."""
    try:
        _get_conn().execute(
            "INSERT INTO media_cache (filepath, file_id) VALUES (?, ?) "
            "ON CONFLICT(filepath) DO UPDATE SET file_id = excluded.file_id",
            (filepath, file_id),
        )
        _get_conn().commit()
    except Exception:
        logging.exception("Ошибка при сохранении media_cache")


def _remove_one(filepath: str) -> None:
    """Удаляет запись из SQLite."""
    try:
        _get_conn().execute(
            "DELETE FROM media_cache WHERE filepath = ?", (filepath,)
        )
        _get_conn().commit()
    except Exception:
        pass


# ── Синглтон-словарь, инициализируется при первом импорте ──


class _MediaCache(dict[str, str]):
    """dict[str, str] с автоматической синхронизацией в SQLite."""

    def __init__(self) -> None:
        super().__init__()
        self._loaded = False

    def _ensure_loaded(self) -> None:
        if not self._loaded:
            self.update(_load_all())
            self._loaded = True
            logging.info(
                "[MEDIA CACHE] Загружено %d записей из SQLite", len(self)
            )

    def __getitem__(self, key: str) -> str:
        self._ensure_loaded()
        return super().__getitem__(key)

    def __contains__(self, key: object) -> bool:
        self._ensure_loaded()
        return super().__contains__(key)

    def __setitem__(self, key: str, value: str) -> None:
        self._ensure_loaded()
        super().__setitem__(key, value)
        _save_one(key, value)

    def __delitem__(self, key: str) -> None:
        self._ensure_loaded()
        super().__delitem__(key)
        _remove_one(key)

    def pop(self, key: str, default=None) -> str | None:
        self._ensure_loaded()
        val = super().pop(key, default)
        if val is not None:
            _remove_one(key)
        return val

    def get(self, key: str, default=None) -> str | None:
        self._ensure_loaded()
        return super().get(key, default)


MEDIA_CACHE = _MediaCache()