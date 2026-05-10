from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.auth.models import User
from app.domains.project.models import Project
from app.domains.project.schemas import ProjectCreate
from app.domains.project.repository import (
    ProjectRepository
)


class ProjectService:

    @staticmethod
    async def create_project(
        db: AsyncSession,
        project_data: ProjectCreate,
        workspace_id,
        current_user: User
    ):

        project = Project(
            name=project_data.name,
            description=project_data.description,
            workspace_id=workspace_id,
            created_by=current_user.id
        )

        return await ProjectRepository.create_project(
            db,
            project
        )