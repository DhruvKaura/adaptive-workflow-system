from uuid import UUID

from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.session import get_db

from app.domains.analytics.service import (
    AnalyticsService
)


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)

@router.get("/tasks/{task_id}/cycle-time")
async def get_task_cycle_time(
    task_id: UUID,
    db: AsyncSession = Depends(get_db)
):

    return await (
        AnalyticsService.calculate_task_cycle_time(
            db,
            task_id
        )
    )


@router.get("/blocked-tasks")
async def get_blocked_tasks(
    db: AsyncSession = Depends(get_db)
):

    return await (
        AnalyticsService.detect_blocked_tasks(
            db
        )
    )