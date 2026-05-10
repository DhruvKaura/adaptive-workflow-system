import uuid

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database.base import Base


class User(Base):

    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    email: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)

    username: Mapped[str] = mapped_column(
        String, unique=True, nullable=False, index=True
    )

    hashed_password: Mapped[str] = mapped_column(String, nullable=False)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # -----------------------------------
    # Relationships
    # -----------------------------------

    workspaces = relationship("Workspace", back_populates="owner")

    projects = relationship("Project", back_populates="owner")

    assigned_tasks = relationship("Task", foreign_keys="Task.assignee_id")

    created_tasks = relationship("Task", foreign_keys="Task.created_by")
