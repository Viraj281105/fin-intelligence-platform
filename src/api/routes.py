"""REST API endpoints for financial SLM queries, SQL execution, and analysis."""

import uuid
from fastapi import APIRouter, HTTPException, status
from src.core.schemas import (
    FinancialTaskType,
    QueryRequest,
    QueryResponse,
    AuditLogRecord,
)
from src.training.inference_engine import inference_engine
from src.security.guardrails import FinancialGuardrails
from src.security.pii_masker import FinancialPIIMasker
from src.sql.executor import SafeSQLExecutor
from src.analysis.financial_math import FinancialCalculator
from src.analysis.compliance import ComplianceRuleEngine
from src.core.audit import audit_logger

router = APIRouter(prefix="/v1", tags=["Financial Intelligence API"])
sql_executor = SafeSQLExecutor()


@router.post("/query", response_model=QueryResponse)
async def execute_financial_query(request: QueryRequest) -> QueryResponse:
    """End-to-end unified financial query inference with safety guardrails and audit logging."""
    req_id = str(uuid.uuid4())

    # 1. Guardrail input validation
    guard_check = FinancialGuardrails.check_input_prompt(request.query)
    if not guard_check.is_safe:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Guardrail Alert: {guard_check.reason}",
        )

    # 2. Financial PII Redaction
    masked_query, pii_count = FinancialPIIMasker.mask_text(request.query)

    # 3. Model Inference
    response = inference_engine.generate(
        query=masked_query,
        task_type=request.task_type,
        context=request.context,
    )
    response.pii_redacted = (pii_count > 0)

    # 4. If Text-to-SQL task and SQL was generated, optionally execute on the safe warehouse
    if request.task_type == FinancialTaskType.TEXT_TO_SQL and response.sql_query:
        exec_res = sql_executor.execute_query(response.sql_query)
        response.sql_results = exec_res

    # 5. Redact response before logging
    masked_resp, _ = FinancialPIIMasker.mask_text(response.answer)

    # 6. Compliance Audit Record
    audit_record = AuditLogRecord(
        request_id=req_id,
        task_type=request.task_type.value,
        user_query_redacted=masked_query,
        model_response_redacted=masked_resp,
        generated_sql=response.sql_query,
        sql_execution_success=(response.sql_results.success if response.sql_results else None),
        latency_ms=response.latency_ms,
        prompt_tokens=len(masked_query.split()),
        completion_tokens=response.tokens_generated,
        pii_detected_count=pii_count,
        guardrail_flagged=False,
    )
    audit_logger.log(audit_record)

    return response


@router.get("/schema", response_model=dict)
async def get_database_schema():
    """Retrieve the financial warehouse DDL schema definition."""
    return {"schema": sql_executor.get_schema_summary()}


@router.get("/health", response_model=dict)
async def health_check():
    """System health check and status."""
    return {
        "status": "healthy",
        "model_loaded": inference_engine._is_loaded,
        "service": "fin-intelligence-slm-platform",
    }
