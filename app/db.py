
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

DB_PATH = Path(__file__).resolve().parents[1] / "app.db"

def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def query(sql: str, params: Sequence[Any] | None = None) -> List[Dict[str, Any]]:
    """
    S06: используем параметризованные запросы вместо конкатенации строк,
    чтобы исключить SQL-инъекции (placeholders + параметры).
    """
    with get_conn() as conn:
        rows = conn.execute(sql, params or []).fetchall()
        return [dict(r) for r in rows]

def query_one(sql: str, params: Sequence[Any] | None = None) -> Optional[Dict[str, Any]]:
    """
    S06: безопасный вариант одиночного запроса с параметрами.
    """
    with get_conn() as conn:
        row = conn.execute(sql, params or []).fetchone()
        return dict(row) if row else None