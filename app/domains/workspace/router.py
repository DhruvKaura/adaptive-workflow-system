from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.session import get_db
from app.core.security.dependencies import get_current_user
from app.core.security.permissions import require_workspace_role
from app.domains.auth.models import User
from app.domains.workspace.models import WorkspaceMember
from app.domains.workspace.schemas import WorkspaceCreate
from app.domains.workspace.service import WorkspaceService

router = APIRouter(prefix="/workspaces", tags=["Workspaces"])


@router.post("/")
async def create_workspace(
    workspace_data: WorkspaceCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    workspace = await WorkspaceService.create_workspace(
        db, workspace_data, current_user
    )

    return {"workspace_id": str(workspace.id), "name": workspace.name}


@router.delete("/{workspace_id}")
async def delete_workspace(
    workspace_id: UUID,
    db: AsyncSession = Depends(get_db),
    membership: WorkspaceMember = Depends(require_workspace_role(["owner"])),
):

    await WorkspaceService.delete_workspace(db, workspace_id)

    return {"message": f"Workspace {workspace_id} deleted successfully"}
