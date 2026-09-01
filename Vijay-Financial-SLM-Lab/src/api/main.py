"""FastAPI Application entrypoint.

💡 Learning Concepts & References:
- What is an Application Entrypoint? The root file that creates the server app object,
  attaches middleware (like CORS for browser dashboards), and includes route modules.
- 📖 GFG: Building REST APIs with Python: https://www.geeksforgeeks.org/rest-api-introduction/
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import router
from src.config.settings import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    description="Financial Intelligence SLM Learning & Serving Platform",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Enable CORS so browser apps / dashboards can talk to the API
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
        "docs": "/docs",
        "health": "/v1/health",
    }
