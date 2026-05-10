from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.workflow.models import (
    WorkflowEvent
)


class AnalyticsService:

    @staticmethod
    async def get_task_event_history(
        db: AsyncSession,
        task_id
    ):

        result = await db.execute(
            select(WorkflowEvent)
            .where(
                WorkflowEvent.task_id == task_id
            )
            .order_by(
                WorkflowEvent.created_at
            )
        )

        return result.scalars().all()
    
    from datetime import datetime


    @staticmethod
    async def calculate_task_cycle_time(
        db: AsyncSession,
        task_id
    ):

        events = await (
            AnalyticsService.get_task_event_history(
                db,
                task_id
            )
        )

        if not events:
            return None

        start_time = events[0].created_at

        completed_event = None

        for event in events:

            if (
                event.event_type == "STATUS_CHANGED"
                and
                event.new_value.get("status")
                == "completed"
            ):

                completed_event = event

        if not completed_event:
            return {
                "completed": False
            }

        cycle_time = (
            completed_event.created_at
            - start_time
        )

        return {
            "completed": True,
            "cycle_time_seconds":
                cycle_time.total_seconds()
        }
    
    @staticmethod
    async def detect_blocked_tasks(
        db: AsyncSession,
        threshold_hours: int = 24
    ):

        result = await db.execute(
            select(WorkflowEvent)
            .where(
                WorkflowEvent.event_type
                == "STATUS_CHANGED"
            )
        )

        events = result.scalars().all()

        blocked_tasks = []

        now = datetime.utcnow()

        for event in events:

            if (
                event.new_value.get("status")
                == "blocked"
            ):

                duration = (
                    now - event.created_at
                ).total_seconds() / 3600

                if duration >= threshold_hours:

                    blocked_tasks.append({
                        "task_id":
                            str(event.task_id),

                        "blocked_hours":
                            round(duration, 2)
                    })

        return blocked_tasks