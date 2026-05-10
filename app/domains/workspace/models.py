import uuid

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database.base import Base


class Workspace(Base):
    __tablename__ = "workspaces"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    name: Mapped[str] = mapped_column(String, nullable=False)

    owner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))

    owner = relationship("User")


class WorkspaceMember(Base):
    __tablename__ = "workspace_members"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    workspace_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("workspaces.id"))

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))

    role: Mapped[str] = mapped_column(String, default="member")

    workspace = relationship("Workspace")

    user = relationship("User")
