"""SQL validation scaffold using sqlglot for security analysis.

💡 Learning Concepts & References:
- What is an Abstract Syntax Tree (AST)? A tree representation of code syntax.
  Instead of fragile string checks (like checking if 'DROP' is in the text),
  an AST parses the true grammatical structure of the SQL query.
- Why is it critical for Text-to-SQL?
  1. An attacker might hide `DROP TABLE` inside a comment or nested subquery.
  2. AST parsing detects malicious commands regardless of formatting.
- 📖 sqlglot Parser Documentation: https://sqlglot.com/sqlglot.html
- 📖 GFG: SQL Injection and Prevention: https://www.geeksforgeeks.org/sql-injection/
"""

import sqlglot
from sqlglot import exp
from src.core.schemas import SQLValidationResult

DISALLOWED_EXPRESSIONS = (
    exp.Drop,
    exp.Delete,
    exp.Insert,
    exp.Update,
    exp.Alter,
    exp.Create,
)


class SQLValidator:
    """Validates that generated SQL statements are read-only and safe to execute."""

    def validate(self, sql_query: str) -> SQLValidationResult:
        """Parse SQL and ensure it is a safe SELECT statement."""
        if not sql_query or not sql_query.strip():
            return SQLValidationResult(is_valid=False, error_message="Empty query provided")

        try:
            parsed = sqlglot.parse_one(sql_query)
            
            # Check for write/destructive statements
            for disallowed in DISALLOWED_EXPRESSIONS:
                if parsed.find(disallowed):
                    return SQLValidationResult(
                        is_valid=False,
                        error_message=f"Security Alert: Query contains disallowed expression '{disallowed.__name__}'",
                        is_read_only=False,
                    )

            if not isinstance(parsed, exp.Select):
                return SQLValidationResult(
                    is_valid=False,
                    error_message="Only read-only SELECT queries are permitted",
                    is_read_only=False,
                )
            
            tables = [t.name for t in parsed.find_all(exp.Table) if t.name]
            return SQLValidationResult(
                is_valid=True,
                sanitized_sql=parsed.sql(pretty=True),
                ast_tables=tables,
                is_read_only=True,
            )
        except Exception as e:
            return SQLValidationResult(is_valid=False, error_message=f"SQL Syntax Error: {e}")
