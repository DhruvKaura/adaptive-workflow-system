from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.auth.models import User
from app.domains.workspace.models import Workspace, WorkspaceMember
from app.domains.workspace.repository import WorkspaceRepository
from app.domains.workspace.schemas import WorkspaceCreate


class WorkspaceService:

    @staticmethod
    async def create_workspace(
        db: AsyncSession, workspace_data: WorkspaceCreate, current_user: User
    ):

        workspace = Workspace(name=workspace_data.name, owner_id=current_user.id)

        workspace = await WorkspaceRepository.create_workspace(db, workspace)

        member = WorkspaceMember(
            workspace_id=workspace.id, user_id=current_user.id, role="owner"
        )

        await WorkspaceRepository.add_member(db, member)

        return workspace

    @staticmethod
    async def delete_workspace(db: AsyncSession, workspace_id: UUID):

        await WorkspaceRepository.delete_workspace(db, workspace_id)
