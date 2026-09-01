"""FastAPI application entrypoint for Financial Intelligence Platform."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import router
from src.config.settings import get_settings

settings = get_settings()

app = FastAPI(
    title="🏦 Financial Intelligence SLM Platform",
    description="Enterprise-grade SLM platform for Financial Text-to-SQL, SEC Filings Analysis, Quantitative Math, and Compliance Auditing.",
    version="0.2.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Enable CORS for frontend clients / dashboards
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
def root():
    return {
        "name": settings.APP_NAME,
        "version": "0.2.0",
        "docs": "/docs",
        "environment": settings.ENV,
    }
