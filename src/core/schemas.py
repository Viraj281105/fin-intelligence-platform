"""Core data models and schemas for the Financial SLM Platform."""

from enum import Enum
from typing import Any
from pydantic import BaseModel, Field
from datetime import datetime, timezone


class FinancialTaskType(str, Enum):
    """Supported financial domain task categories."""
    TEXT_TO_SQL = "text_to_sql"
    SEC_FILING_QA = "sec_filing_qa"
    FINANCIAL_MATH = "financial_math"
    SENTIMENT_ANALYSIS = "sentiment_analysis"
    COMPLIANCE_AUDIT = "compliance_audit"
    GENERAL_FINANCE = "general_finance"


class QueryRequest(BaseModel):
    """Inbound request model for the financial query API."""
    query: str = Field(..., description="User query in plain English")
    task_type: FinancialTaskType = Field(
        default=FinancialTaskType.GENERAL_FINANCE,
        description="Target specialized domain capability"
    )
    context: str | None = Field(default=None, description="Optional background context or database schema")


class SQLValidationResult(BaseModel):
    """Result of SQL security and syntax analysis."""
    is_valid: bool
    sanitized_sql: str | None = None
    ast_tables: list[str] = Field(default_factory=list)
    error_message: str | None = None
    is_read_only: bool = True


class QueryResponse(BaseModel):
    """Outbound response model with reasoning trace and results."""
    task_type: FinancialTaskType
    reasoning_trace: str | None = None
    answer: str
    sql_query: str | None = None
    latency_ms: float = 0.0
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
