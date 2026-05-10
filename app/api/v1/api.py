from fastapi import APIRouter

from app.domains.auth.router import (
    router as auth_router
)

from app.domains.project.router import (
    router as project_router
)

from app.domains.task.router import (
    router as task_router
)

from app.core.health.router import (
    router as health_router
)


api_router = APIRouter(
    prefix="/api/v1"
)

api_router.include_router(
    auth_router
)

api_router.include_router(
    project_router
)

api_router.include_router(
    task_router
)

api_router.include_router(
    health_router
)