"""FastAPI Application entrypoint."""

from fastapi import FastAPI
from src.api.routes import router
from src.config.settings import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    description="Financial Intelligence SLM Learning & Serving Platform",
    version="0.1.0",
)

app.include_router(router)
