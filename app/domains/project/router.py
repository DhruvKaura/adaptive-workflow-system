from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.session import get_db
from app.core.security.dependencies import get_current_user
from app.core.security.permissions import require_workspace_role
from app.domains.auth.models import User
from app.domains.project.schemas import ProjectCreate, ProjectResponse
from app.domains.project.service import ProjectService

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("/workspace/{workspace_id}", response_model=ProjectResponse)
async def create_project(
    workspace_id: UUID,
    project_data: ProjectCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    membership=Depends(require_workspace_role(["owner", "admin"])),
):

    return await ProjectService.create_project(
        db, project_data, workspace_id, current_user
    )
