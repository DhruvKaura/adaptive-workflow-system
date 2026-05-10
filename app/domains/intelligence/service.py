from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.task.models import Task
from app.domains.workflow.models import WorkflowEvent
from app.integrations.ollama.client import OllamaClient
from app.integrations.ollama.prompts import build_workflow_summary_prompt


class IntelligenceService:

    @staticmethod
    async def predict_deadline_risk(db: AsyncSession, task_id):

        result = await db.execute(select(Task).where(Task.id == task_id))

        task = result.scalar_one_or_none()

        if not task:
            return {"error": "Task not found"}

        risk_score = 0

        reasons = []

        if task.due_date:

            remaining_hours = (task.due_date - datetime.utcnow()).total_seconds() / 3600

            if remaining_hours < 24:

                risk_score += 40

                reasons.append("Deadline approaching")

        events_result = await db.execute(
            select(WorkflowEvent).where(WorkflowEvent.task_id == task_id)
        )

        events = events_result.scalars().all()

        blocked_count = 0

        for event in events:

            if (
                event.event_type == "STATUS_CHANGED"
                and event.new_value.get("status") == "blocked"
            ):

                blocked_count += 1

        if blocked_count >= 2:

            risk_score += 30

            reasons.append("Task repeatedly blocked")

        transition_count = len(events)

        if transition_count > 10:

            risk_score += 20

            reasons.append("High workflow churn")

        risk_level = "low"

        if risk_score >= 70:
            risk_level = "high"

        elif risk_score >= 40:
            risk_level = "medium"

        return {
            "task_id": str(task.id),
            "risk_score": risk_score,
            "risk_level": risk_level,
            "reasons": reasons,
        }

    @staticmethod
    async def generate_productivity_insights(db: AsyncSession, task_id):

        events_result = await db.execute(
            select(WorkflowEvent).where(WorkflowEvent.task_id == task_id)
        )

        events = events_result.scalars().all()

        blocked_count = 0

        review_count = 0

        for event in events:

            if event.new_value and event.new_value.get("status") == "blocked":

                blocked_count += 1

            if event.new_value and event.new_value.get("status") == "review":

                review_count += 1

        insights = []

        if blocked_count >= 2:

            insights.append("Task experiences frequent blockers")

        if review_count >= 3:

            insights.append("Task repeatedly returns to review")

        if not insights:

            insights.append("Workflow appears healthy")

        return {"task_id": str(task_id), "insights": insights}
