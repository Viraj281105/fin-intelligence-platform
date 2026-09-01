"""SQL validation scaffold using sqlglot for security analysis."""

import sqlglot
from sqlglot import exp
from src.core.schemas import SQLValidationResult


class SQLValidator:
    """Validates that generated SQL statements are read-only and safe to execute."""

    def validate(self, sql_query: str) -> SQLValidationResult:
        """Parse SQL and ensure it is a safe SELECT statement."""
        if not sql_query or not sql_query.strip():
            return SQLValidationResult(is_valid=False, error_message="Empty query")

        try:
            parsed = sqlglot.parse_one(sql_query)
            if not isinstance(parsed, exp.Select):
                return SQLValidationResult(
                    is_valid=False,
                    error_message="Only SELECT queries are allowed",
                    is_read_only=False,
                )
            
            tables = [t.name for t in parsed.find_all(exp.Table) if t.name]
            return SQLValidationResult(
                is_valid=True,
                sanitized_sql=parsed.sql(),
                ast_tables=tables,
                is_read_only=True,
            )
        except Exception as e:
            return SQLValidationResult(is_valid=False, error_message=str(e))
