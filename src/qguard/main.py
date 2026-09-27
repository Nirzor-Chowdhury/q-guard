from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from qguard.api.routes.health import router as health_router
from qguard.api.routes.qkd import router as qkd_router
from qguard.core.config import get_settings
from qguard.core.logging import configure_logging

settings = get_settings()
configure_logging(settings.log_level)


def create_app() -> FastAPI:
    """Create and configure the Q-Guard FastAPI application."""
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description=(
            "Adaptive quantum-safe MITM defense gateway control plane. "
            "Phase 0 foundation."
        ),
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=False,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
        allow_headers=["*"],
    )

    app.include_router(health_router)
    app.include_router(qkd_router)

    @app.get("/", include_in_schema=False)
    def root() -> dict[str, str]:
        return {
            "service": settings.app_name,
            "status": "running",
            "api": "/api/v1/health",
            "documentation": "/docs",
        }

    return app


app = create_app()
