from datetime import timezone
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.auth.models import User

from app.domains.task.models import Task

from app.domains.task.schemas import TaskCreate

from app.domains.task.repository import (
    TaskRepository
)

from app.domains.project.repository import (
    ProjectRepository
)

from app.domains.workflow.models import (
    WorkflowEvent
)

from app.domains.workflow.repository import (
    WorkflowRepository
)

from app.domains.workflow.service import (
    WorkflowService
)

from app.core.celery.tasks import (
    process_workflow_event
)

from app.core.websocket.manager import (
    manager
)

from app.core.logging.logger import (
    get_logger
)

logger = get_logger(__name__)

class TaskService:

    @staticmethod
    async def create_task(
        db: AsyncSession,
        project_id,
        task_data: TaskCreate,
        current_user: User
    ):

        project = await ProjectRepository.get_project_by_id(
            db,
            project_id
        )

        if not project:
            raise Exception("Project not found")

        due_date = task_data.due_date

        if due_date is not None and due_date.tzinfo is not None:
            due_date = due_date.astimezone(timezone.utc).replace(tzinfo=None)

        task = Task(
            title=task_data.title,
            description=task_data.description,
            priority=task_data.priority,
            due_date=due_date,
            assignee_id=task_data.assignee_id,
            project_id=project_id,
            created_by=current_user.id
        )

        task = await TaskRepository.create_task(
            db,
            task
        )

        event = WorkflowEvent(
            task_id=task.id,
            user_id=current_user.id,
            event_type="TASK_CREATED",
            old_value=None,
            new_value={
                "status": task.status
            }
        )

        await WorkflowRepository.create_event(
            db,
            event
        )

        process_workflow_event.delay(
            "TASK_CREATED",
            str(task.id)
        )

        return task

    @staticmethod
    async def update_task_status(
        db: AsyncSession,
        task_id,
        new_status: str,
        current_user: User
    ):

        task = await TaskRepository.get_task_by_id(
            db,
            task_id
        )

        if not task:
            raise Exception("Task not found")

        valid = WorkflowService.validate_transition(
            task.status,
            new_status
        )

        if not valid:
            raise Exception(
                "Invalid workflow transition"
            )

        old_status = task.status

        task.status = new_status

        task = await TaskRepository.save(
            db,
            task
        )

        event = WorkflowEvent(
            task_id=task.id,
            user_id=current_user.id,
            event_type="STATUS_CHANGED",
            old_value={
                "status": old_status
            },
            new_value={
                "status": new_status
            }
        )

        await WorkflowRepository.create_event(
            db,
            event
        )

        process_workflow_event.delay(
            "STATUS_CHANGED",
            str(task.id)
        )

        await manager.broadcast({
            "event": "TASK_STATUS_CHANGED",
            "task_id": str(task.id),
            "new_status": task.status
        })

        return task