from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.project.models import Project


class ProjectRepository:

    @staticmethod
    async def create_project(db: AsyncSession, project: Project):

        db.add(project)

        await db.commit()

        await db.refresh(project)

        return project

    @staticmethod
    async def get_project_by_id(db: AsyncSession, project_id):

        result = await db.execute(select(Project).where(Project.id == project_id))

        return result.scalar_one_or_none()
