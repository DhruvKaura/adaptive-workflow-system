from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.task.models import Task


class TaskRepository:

    @staticmethod
    async def create_task(db: AsyncSession, task: Task):

        db.add(task)

        await db.commit()

        await db.refresh(task)

        return task

    @staticmethod
    async def get_task_by_id(db: AsyncSession, task_id):

        result = await db.execute(select(Task).where(Task.id == task_id))

        return result.scalar_one_or_none()

    @staticmethod
    async def save(db: AsyncSession, task: Task):

        await db.commit()

        await db.refresh(task)

        return task
