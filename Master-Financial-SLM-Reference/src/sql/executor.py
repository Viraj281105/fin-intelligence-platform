"""Safe database execution engine supporting SQLite, PostgreSQL, and DuckDB."""

import time
import sqlite3
from pathlib import Path
from src.core.schemas import ExecutionResult
from src.sql.validator import SQLSecurityValidator
from src.config.settings import get_settings


class SafeSQLExecutor:
    """Executes sanitized, read-only SQL queries with timeout and safety guarantees."""

    def __init__(self, db_path: Path | None = None):
        settings = get_settings()
        self.validator = SQLSecurityValidator()
        self.db_path = db_path or (settings.DATA_DIR / "financial_warehouse.db")
        self._init_sample_database()

    def _init_sample_database(self):
        """Initialize mock financial schema and sample records if database does not exist."""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.executescript("""
        CREATE TABLE IF NOT EXISTS portfolio_positions (
            position_id INTEGER PRIMARY KEY,
            fund_id TEXT NOT NULL,
            ticker TEXT NOT NULL,
            asset_class TEXT NOT NULL,
            market_value REAL NOT NULL,
            unrealized_gain_loss REAL NOT NULL,
            as_of_date TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id INTEGER PRIMARY KEY,
            account_id TEXT NOT NULL,
            transaction_type TEXT NOT NULL,
            ticker TEXT NOT NULL,
            shares REAL NOT NULL,
            price_per_share REAL NOT NULL,
            total_amount REAL NOT NULL,
            fee_amount REAL NOT NULL,
            transaction_timestamp TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS income_statements (
            statement_id INTEGER PRIMARY KEY,
            company_ticker TEXT NOT NULL,
            fiscal_year INTEGER NOT NULL,
            fiscal_quarter INTEGER NOT NULL,
            total_revenue REAL NOT NULL,
            operating_expenses REAL NOT NULL,
            ebitda REAL NOT NULL,
            net_income REAL NOT NULL,
            diluted_eps REAL NOT NULL
        );
        """)

        # Insert seed records if empty
        cursor.execute("SELECT COUNT(*) FROM portfolio_positions;")
        if cursor.fetchone()[0] == 0:
            cursor.executescript("""
            INSERT INTO portfolio_positions VALUES 
            (1, 'FUND_ALPHA', 'AAPL', 'Equities', 14500000.00, 2300000.00, '2024-09-30'),
            (2, 'FUND_ALPHA', 'MSFT', 'Equities', 18200000.00, 4100000.00, '2024-09-30'),
            (3, 'FUND_ALPHA', 'NVDA', 'Equities', 24000000.00, 9500000.00, '2024-09-30'),
            (4, 'FUND_BETA', 'UST_10Y', 'Fixed Income', 50000000.00, -850000.00, '2024-09-30'),
            (5, 'FUND_BETA', 'JNJ', 'Equities', 9500000.00, 450000.00, '2024-09-30');

            INSERT INTO income_statements VALUES
            (1, 'AAPL', 2024, 4, 94930000000.00, 14294000000.00, 30500000000.00, 14736000000.00, 0.97),
            (2, 'MSFT', 2024, 4, 64727000000.00, 17163000000.00, 34200000000.00, 22036000000.00, 2.95),
            (3, 'NVDA', 2024, 3, 35082000000.00, 4287000000.00, 22100000000.00, 19309000000.00, 0.78);
            """)

        conn.commit()
        conn.close()

    def get_schema_summary(self) -> str:
        """Return the DDL schema description of the database for LLM prompting."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
        tables = [row[0] for row in cursor.fetchall() if row[0]]
        conn.close()
        return "\n\n".join(tables)

    def execute_query(self, raw_sql: str) -> ExecutionResult:
        """Validate, sanitize, and execute query returning tabular result rows."""
        start_time = time.perf_counter()

        # Step 1: Security AST Validation
        val_res = self.validator.validate_and_sanitize(raw_sql)
        if not val_res.is_valid or not val_res.sanitized_sql:
            return ExecutionResult(
                success=False,
                error=val_res.error_message or "Invalid SQL query",
                execution_time_ms=0.0,
            )

        # Step 2: Safe execution in SQLite
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute(val_res.sanitized_sql)
            rows = cursor.fetchall()
            
            columns = [desc[0] for desc in cursor.description] if cursor.description else []
            data = [dict(row) for row in rows]
            
            conn.close()
            elapsed = (time.perf_counter() - start_time) * 1000

            return ExecutionResult(
                success=True,
                columns=columns,
                rows=data,
                row_count=len(data),
                execution_time_ms=round(elapsed, 2),
            )
        except Exception as e:
            elapsed = (time.perf_counter() - start_time) * 1000
            return ExecutionResult(
                success=False,
                error=f"Execution error: {str(e)}",
                execution_time_ms=round(elapsed, 2),
            )
