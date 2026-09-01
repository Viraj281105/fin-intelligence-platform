"""Safe SQLite executor scaffold.

💡 Learning Concepts & References:
- What is SQLite? A lightweight, serverless database engine built directly into Python.
  It stores tables in a single file on disk (financial_warehouse.db) without needing separate servers.
- 📖 Python sqlite3 Module Documentation: https://docs.python.org/3/library/sqlite3.html
- 📖 GFG: Python SQLite Tutorial: https://www.geeksforgeeks.org/python-sqlite/
"""

import sqlite3
from pathlib import Path
from src.config.settings import get_settings


class SQLExecutor:
    """Executes validated SQL statements against the local SQLite financial warehouse."""

    def __init__(self, db_path: Path | None = None):
        settings = get_settings()
        self.db_path = db_path or (settings.DATA_DIR / "financial_warehouse.db")

    def execute(self, query: str) -> list[dict]:
        """Execute query and return list of row dictionaries."""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Returns rows as dictionary-like objects
        cursor = conn.cursor()
        try:
            cursor.execute(query)
            rows = [dict(r) for r in cursor.fetchall()]
            return rows
        finally:
            conn.close()
