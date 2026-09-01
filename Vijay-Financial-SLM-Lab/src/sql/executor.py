"""Safe SQLite executor scaffold."""

import sqlite3
from pathlib import Path
from src.config.settings import get_settings


class SQLExecutor:
    """Executes validated SQL statements against SQLite warehouse."""

    def __init__(self, db_path: Path | None = None):
        settings = get_settings()
        self.db_path = db_path or (settings.DATA_DIR / "financial_warehouse.db")

    def execute(self, query: str) -> list[dict]:
        """Execute query and return list of row dictionaries."""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        try:
            cursor.execute(query)
            rows = [dict(r) for r in cursor.fetchall()]
            return rows
        finally:
            conn.close()
