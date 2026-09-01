"""SQL AST validation and security sanitization engine using sqlglot."""

import sqlglot
from sqlglot import exp
from src.core.schemas import SQLValidationResult
from src.config.settings import get_settings

DISALLOWED_EXPRESSIONS = (
    exp.Drop,
    exp.Delete,
    exp.Insert,
    exp.Update,
    exp.Alter,
    exp.Create,
    exp.Command,
    exp.Pragma,
)


class SQLSecurityValidator:
    """Enterprise SQL safety validator enforcing read-only constraints and AST parsing."""

    def __init__(self, default_limit: int = 100):
        settings = get_settings()
        self.default_limit = min(default_limit, settings.MAX_QUERY_LIMIT)

    def validate_and_sanitize(self, sql_query: str) -> SQLValidationResult:
        """Parse AST, verify read-only safety, enforce LIMIT clause, and return sanitized query."""
        if not sql_query or not sql_query.strip():
            return SQLValidationResult(
                is_valid=False,
                error_message="Empty SQL query provided",
                is_read_only=False,
            )

        try:
            # Parse query AST
            parsed = sqlglot.parse_one(sql_query, read="postgres")
        except Exception as e:
            try:
                # Fallback to generic dialect
                parsed = sqlglot.parse_one(sql_query)
            except Exception as e2:
                return SQLValidationResult(
                    is_valid=False,
                    error_message=f"SQL Syntax Error: {e2}",
                    is_read_only=False,
                )

        # 1. Check for disallowed DDL/DML statements
        for disallowed in DISALLOWED_EXPRESSIONS:
            if parsed.find(disallowed):
                return SQLValidationResult(
                    is_valid=False,
                    error_message=f"Security Violation: Query contains prohibited write/DDL expression '{disallowed.__name__}'",
                    is_read_only=False,
                )

        # 2. Verify root is SELECT or Union of Selects
        if not isinstance(parsed, (exp.Select, exp.Union)):
            return SQLValidationResult(
                is_valid=False,
                error_message="Security Violation: Root query must be a SELECT expression",
                is_read_only=False,
            )

        # 3. Extract Table and Column names for audit trail
        tables = [t.name for t in parsed.find_all(exp.Table) if t.name]
        columns = [c.name for c in parsed.find_all(exp.Column) if c.name]

        # 4. Enforce mandatory LIMIT clause
        limit_node = parsed.find(exp.Limit)
        if not limit_node:
            parsed = parsed.limit(self.default_limit)
        else:
            try:
                # If existing limit exceeds default limit, cap it
                current_limit_text = str(limit_node.expression)
                if current_limit_text.isdigit() and int(current_limit_text) > self.default_limit:
                    limit_node.set("expression", exp.Literal.number(self.default_limit))
            except Exception:
                pass

        sanitized_sql = parsed.sql(dialect="postgres", pretty=True)

        return SQLValidationResult(
            is_valid=True,
            sanitized_sql=sanitized_sql,
            ast_tables=list(set(tables)),
            ast_columns=list(set(columns)),
            is_read_only=True,
        )
