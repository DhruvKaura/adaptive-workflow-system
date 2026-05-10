from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class TaskCreate(BaseModel):
    title: str
    description: str | None = None

    priority: str = "medium"

    due_date: datetime | None = None

    assignee_id: UUID | None = None


class TaskStatusUpdate(BaseModel):
    status: str
