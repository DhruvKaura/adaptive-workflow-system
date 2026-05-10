import uuid
from datetime import datetime

from sqlalchemy import (
    String,
    ForeignKey,
    DateTime,
    JSON
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from app.core.database.base import Base


class WorkflowEvent(Base):
    __tablename__ = "workflow_events"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )

    task_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("tasks.id")
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id")
    )

    event_type: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    old_value: Mapped[dict] = mapped_column(
        JSON,
        nullable=True
    )

    new_value: Mapped[dict] = mapped_column(
        JSON,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    task = relationship("Task")

    user = relationship("User")