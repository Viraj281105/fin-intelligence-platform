"""Unit tests for SQL AST validator and security sanitizer."""

import pytest
from src.sql.validator import SQLSecurityValidator


def test_valid_select_query():
    validator = SQLSecurityValidator(default_limit=50)
    query = "SELECT ticker, market_value FROM portfolio_positions WHERE asset_class = 'Equities'"
    res = validator.validate_and_sanitize(query)

    assert res.is_valid is True
    assert res.is_read_only is True
    assert "portfolio_positions" in res.ast_tables
    assert "LIMIT 50" in res.sanitized_sql.upper()


def test_disallowed_drop_statement():
    validator = SQLSecurityValidator()
    query = "DROP TABLE portfolio_positions;"
    res = validator.validate_and_sanitize(query)

    assert res.is_valid is False
    assert "Security Violation" in res.error_message


def test_disallowed_delete_statement():
    validator = SQLSecurityValidator()
    query = "DELETE FROM transactions WHERE transaction_id = 5;"
    res = validator.validate_and_sanitize(query)

    assert res.is_valid is False
    assert "Security Violation" in res.error_message


def test_limit_capping():
    validator = SQLSecurityValidator(default_limit=100)
    query = "SELECT * FROM transactions LIMIT 5000;"
    res = validator.validate_and_sanitize(query)

    assert res.is_valid is True
    assert "LIMIT 100" in res.sanitized_sql.upper()
