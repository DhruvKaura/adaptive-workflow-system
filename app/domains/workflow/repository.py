from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.workflow.models import (
    WorkflowEvent
)


class WorkflowRepository:

    @staticmethod
    async def create_event(
        db: AsyncSession,
        event: WorkflowEvent
    ):

        db.add(event)

        await db.commit()

        await db.refresh(event)

        return event