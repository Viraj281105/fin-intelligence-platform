"""FastAPI routes scaffold for the Financial SLM Platform.

💡 Learning Concepts & References:
- What is FastAPI? A modern, fast (high-performance) web framework for building APIs with Python.
- Why is it popular for AI?
  1. Built-in OpenAPI (Swagger) documentation generated automatically at `/docs`.
  2. Automatic request validation using Pydantic models.
  3. High performance async/await support for streaming AI tokens.
- 📖 FastAPI Official Tutorial: https://fastapi.tiangolo.com/tutorial/
- 📖 GFG: FastAPI Tutorial: https://www.geeksforgeeks.org/fastapi-tutorial/
"""

from fastapi import APIRouter, HTTPException, status
from src.core.schemas import QueryRequest, QueryResponse
from src.training.inference_engine import inference_engine
from src.security.guardrails import Guardrails
from src.security.pii_masker import PIIMasker

router = APIRouter(prefix="/v1", tags=["FinSLM Platform"])


@router.post("/query", response_model=QueryResponse)
async def query_model(req: QueryRequest) -> QueryResponse:
    """Submit a financial query to the FinSLM engine."""
    # 1. Guardrail input validation
    if not Guardrails.is_safe(req.query):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Guardrail Alert: Prompt injection attempt detected.",
        )

    # 2. PII Redaction
    masked_query = PIIMasker.mask(req.query)

    # 3. Model Inference
    return inference_engine.generate(
        query=masked_query,
        task_type=req.task_type,
        context=req.context,
    )


@router.get("/health")
async def health():
    """Health check status endpoint."""
    return {"status": "healthy", "service": "fin-slm-platform"}
