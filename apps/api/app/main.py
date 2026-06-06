from fastapi import FastAPI

from app.core.config import get_settings
from app.routers.auth import router as auth_router

settings = get_settings()
app = FastAPI(title=settings.app_name)
app.include_router(auth_router)


@app.get("/health")
def healthcheck() -> dict[str, str]:
    return {
        "status": "ok",
        "app": settings.app_name,
        "environment": settings.environment,
    }
