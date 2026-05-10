from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.session import get_db
from app.core.security.dependencies import get_current_user
from app.domains.auth.models import User
from app.domains.task.schemas import TaskCreate, TaskStatusUpdate
from app.domains.task.service import TaskService

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/project/{project_id}")
async def create_task(
    project_id: UUID,
    task_data: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    task = await TaskService.create_task(db, project_id, task_data, current_user)

    return {"task_id": str(task.id), "title": task.title, "status": task.status}


@router.patch("/{task_id}/status")
async def update_task_status(
    task_id: UUID,
    payload: TaskStatusUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    task = await TaskService.update_task_status(
        db, task_id, payload.status, current_user
    )

    return {"task_id": str(task.id), "new_status": task.status}
