from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from sqlalchemy import delete

from app.domains.workspace.models import (
    Workspace,
    WorkspaceMember
)

from sqlalchemy import select

class WorkspaceRepository:

    @staticmethod
    async def create_workspace(
        db: AsyncSession,
        workspace: Workspace
    ):

        db.add(workspace)

        await db.commit()

        await db.refresh(workspace)

        return workspace

    @staticmethod
    async def add_member(
        db: AsyncSession,
        member: WorkspaceMember
    ):

        db.add(member)

        await db.commit()

        await db.refresh(member)

        return member
    
    @staticmethod
    async def get_workspace_by_id(
        db: AsyncSession,
        workspace_id: UUID
    ):

        result = await db.execute(
            select(Workspace).where(
                Workspace.id == workspace_id
            )
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def delete_workspace(
        db: AsyncSession,
        workspace_id: UUID
    ):

        # First delete all members
        await db.execute(
            delete(WorkspaceMember).where(
                WorkspaceMember.workspace_id == workspace_id
            )
        )

        # Then delete the workspace
        workspace = await WorkspaceRepository.get_workspace_by_id(
            db,
            workspace_id
        )

        if workspace:
            await db.delete(workspace)
            await db.commit()