"""Core data models and schemas for the Financial SLM Platform.

💡 Learning Concepts & References:
- What is Pydantic? It provides data parsing and strict type-safety in Python.
  If a user sends invalid data, Pydantic automatically catches the error and gives a clear message.
- 📖 Reference: https://docs.pydantic.dev/latest/
- 📖 GFG Guide: https://www.geeksforgeeks.org/pydantic-python/
- What is an Enum? A set of named symbolic constants (e.g. TEXT_TO_SQL, FINANCIAL_MATH).
- 📖 GFG Guide: https://www.geeksforgeeks.org/enum-in-python/
"""

from enum import Enum
from typing import Any
from pydantic import BaseModel, Field
from datetime import datetime, timezone


class FinancialTaskType(str, Enum):
    """Supported financial domain task categories.
    
    Why use Task Types?
    - By categorizing tasks, we can route the user query to the best specialized
      system prompt or tool (e.g., math solver vs. SQL generator).
    """
    TEXT_TO_SQL = "text_to_sql"
    SEC_FILING_QA = "sec_filing_qa"
    FINANCIAL_MATH = "financial_math"
    SENTIMENT_ANALYSIS = "sentiment_analysis"
    COMPLIANCE_AUDIT = "compliance_audit"
    GENERAL_FINANCE = "general_finance"


class QueryRequest(BaseModel):
    """Inbound request model for the financial query API.
    
    Represents what a user or frontend client sends to the AI server.
    """
    query: str = Field(..., description="User query in plain English (e.g., 'What is Apple's gross margin?')")
    task_type: FinancialTaskType = Field(
        default=FinancialTaskType.GENERAL_FINANCE,
        description="Target specialized domain capability"
    )
    context: str | None = Field(
        default=None, 
        description="Optional background context (e.g. a database schema or SEC 10-K excerpt)"
    )


class SQLValidationResult(BaseModel):
    """Result of SQL security and syntax analysis.
    
    Why is this important?
    - We must check if the AI-generated SQL is read-only before running it against a real database.
    """
    is_valid: bool = Field(..., description="True if SQL is syntactically correct and safe to run")
    sanitized_sql: str | None = Field(default=None, description="Cleaned, formatted SQL string")
    ast_tables: list[str] = Field(default_factory=list, description="List of tables referenced by the query")
    error_message: str | None = Field(default=None, description="Detailed explanation if validation failed")
    is_read_only: bool = Field(default=True, description="Enforces that no DROP, DELETE, or UPDATE is allowed")


class QueryResponse(BaseModel):
    """Outbound response model with reasoning trace and results.
    
    Why include reasoning_trace?
    - Chain-of-Thought (CoT) reasoning allows financial analysts to audit HOW the AI reached its conclusion.
    """
    task_type: FinancialTaskType
    reasoning_trace: str | None = Field(default=None, description="Step-by-step thinking inside <thought> tags")
    answer: str = Field(..., description="Final user-facing financial explanation or answer")
    sql_query: str | None = Field(default=None, description="Generated SQL statement if Text-to-SQL task")
    latency_ms: float = Field(default=0.0, description="Inference execution time in milliseconds")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
