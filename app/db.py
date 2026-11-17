"""Persistência SQLite; sessão transacional por requisição."""
from contextlib import contextmanager
from pathlib import Path
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()


def db_path() -> str:
    return os.getenv("STOCKGUARD_DB", "stockguard.sqlite3")


@contextmanager
def db_session():
    path = db_path()
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path, timeout=8, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def initialize():
    with db_session() as db:
        db.executescript("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sku TEXT NOT NULL COLLATE NOCASE UNIQUE,
            name TEXT NOT NULL,
            stock INTEGER NOT NULL DEFAULT 0 CHECK(stock >= 0),
            min_stock INTEGER NOT NULL DEFAULT 0 CHECK(min_stock >= 0),
            unit TEXT NOT NULL DEFAULT 'UN',
            location TEXT NOT NULL DEFAULT 'PRATELEIRA'
        );
        CREATE TABLE IF NOT EXISTS movements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id INTEGER NOT NULL REFERENCES items(id),
            type TEXT NOT NULL CHECK(type IN ('IN','OUT','ADJUST')),
            quantity INTEGER NOT NULL CHECK(quantity >= 0),
            stock_before INTEGER NOT NULL,
            stock_after INTEGER NOT NULL CHECK(stock_after >= 0),
            reason TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id INTEGER NOT NULL REFERENCES items(id),
            status TEXT NOT NULL CHECK(status IN ('OPEN','RESOLVED')),
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            resolved_at TEXT
        );
        CREATE UNIQUE INDEX IF NOT EXISTS one_open_alert_per_item
        ON alerts(item_id) WHERE status='OPEN';
        """)
