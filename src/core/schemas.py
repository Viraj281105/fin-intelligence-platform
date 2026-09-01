"""Core domain schemas and Pydantic models."""

from enum import Enum
from typing import Any
from pydantic import BaseModel, Field
from datetime import datetime, timezone


class FinancialTaskType(str, Enum):
    TEXT_TO_SQL = "text_to_sql"
    SEC_FILING_QA = "sec_filing_qa"
    FINANCIAL_MATH = "financial_math"
    SENTIMENT_ANALYSIS = "sentiment_analysis"
    COMPLIANCE_AUDIT = "compliance_audit"
    GENERAL_FINANCE = "general_finance"


class QueryRequest(BaseModel):
    query: str = Field(..., description="User's natural language financial query")
    task_type: FinancialTaskType = Field(
        default=FinancialTaskType.GENERAL_FINANCE,
        description="Target specialized domain task"
    )
    context: str | None = Field(
        default=None,
        description="Optional additional context (e.g. SEC excerpt, schema info)"
    )
    stream: bool = Field(
        default=False,
        description="Whether to stream token responses via SSE"
    )
    session_id: str | None = Field(
        default=None,
        description="Optional session or conversation ID"
    )


class SQLValidationResult(BaseModel):
    is_valid: bool
    sanitized_sql: str | None = None
    ast_tables: list[str] = Field(default_factory=list)
    ast_columns: list[str] = Field(default_factory=list)
    error_message: str | None = None
    is_read_only: bool = True


class ExecutionResult(BaseModel):
    success: bool
    columns: list[str] = Field(default_factory=list)
    rows: list[dict[str, Any]] = Field(default_factory=list)
    row_count: int = 0
    execution_time_ms: float = 0.0
    error: str | None = None


class MathComputationResult(BaseModel):
    metric_name: str
    formula: str
    steps: list[str]
    inputs: dict[str, float]
    result: float
    interpretation: str | None = None


class QueryResponse(BaseModel):
    task_type: FinancialTaskType
    reasoning_trace: str | None = None
    answer: str
    sql_query: str | None = None
    sql_results: ExecutionResult | None = None
    math_results: MathComputationResult | None = None
    latency_ms: float = 0.0
    tokens_generated: int = 0
    pii_redacted: bool = False
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class AuditLogRecord(BaseModel):
    request_id: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    task_type: str
    user_query_redacted: str
    model_response_redacted: str
    generated_sql: str | None = None
    sql_execution_success: bool | None = None
    latency_ms: float
    prompt_tokens: int
    completion_tokens: int
    pii_detected_count: int = 0
    guardrail_flagged: bool = False
    client_ip: str | None = None
