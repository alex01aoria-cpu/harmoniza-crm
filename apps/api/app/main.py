from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.routers.auth import router as auth_router
from app.routers.lead_capture import router as lead_capture_router
from app.routers.leads import router as leads_router
from app.routers.tasks import router as tasks_router
from app.routers.outcomes import router as outcomes_router
from app.routers.dashboard import router as dashboard_router
from app.routers.ops import router as ops_router

settings = get_settings()
app = FastAPI(title=settings.app_name)

if settings.cors_origins_list:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(auth_router)
app.include_router(lead_capture_router)
app.include_router(leads_router)
app.include_router(tasks_router)
app.include_router(outcomes_router)
app.include_router(dashboard_router)
app.include_router(ops_router)


@app.get("/health")
def healthcheck() -> dict[str, str]:
    return {
        "status": "ok",
        "app": settings.app_name,
        "environment": settings.environment,
    }
