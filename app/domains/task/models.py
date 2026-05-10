import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database.base import Base


class Task(Base):

    __tablename__ = "tasks"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    title: Mapped[str] = mapped_column(String, nullable=False)

    description: Mapped[str] = mapped_column(Text, nullable=True)

    status: Mapped[str] = mapped_column(String, default="todo", index=True)

    priority: Mapped[str] = mapped_column(String, default="medium")

    due_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"), index=True)

    assignee_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"), nullable=True, index=True
    )

    created_by: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), index=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # -----------------------------------
    # Relationships
    # -----------------------------------

    project = relationship("Project", back_populates="tasks")

    assignee = relationship(
        "User", foreign_keys=[assignee_id], back_populates="assigned_tasks"
    )

    creator = relationship(
        "User", foreign_keys=[created_by], back_populates="created_tasks"
    )

    workflow_events = relationship(
        "WorkflowEvent", back_populates="task", cascade="all, delete-orphan"
    )
