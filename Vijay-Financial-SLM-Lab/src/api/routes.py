"""FastAPI routes scaffold for the Financial SLM Platform."""

from fastapi import APIRouter
from src.core.schemas import QueryRequest, QueryResponse
from src.training.inference_engine import inference_engine

router = APIRouter(prefix="/v1", tags=["FinSLM"])


@router.post("/query", response_model=QueryResponse)
async def query_model(req: QueryRequest) -> QueryResponse:
    """Submit a query to the FinSLM engine."""
    return inference_engine.generate(query=req.query, task_type=req.task_type, context=req.context)


@router.get("/health")
async def health():
    """Health check status endpoint."""
    return {"status": "ok", "service": "fin-slm-platform"}
