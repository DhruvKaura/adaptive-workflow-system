from uuid import UUID

from celery.result import AsyncResult
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.session import get_db
from app.domains.intelligence.schemas import GeminiResponse
from app.domains.intelligence.service import IntelligenceService
from app.integrations.ollama.client import OllamaClient
from app.workers.ai_tasks import generate_ai_summary

router = APIRouter(prefix="/intelligence", tags=["Workflow Intelligence"])


@router.get("/tasks/{task_id}/risk")
async def predict_task_risk(task_id: UUID, db: AsyncSession = Depends(get_db)):

    return await IntelligenceService.predict_deadline_risk(db, task_id)


@router.get("/tasks/{task_id}/insights")
async def get_task_insights(task_id: UUID, db: AsyncSession = Depends(get_db)):

    return await IntelligenceService.generate_productivity_insights(db, task_id)


@router.get("/test-ollama")
async def test_ollama(
    prompt: str = ("Explain workflow bottlenecks " "in one sentence."),
):

    response = await OllamaClient.generate_response(prompt)

    return {"response": response}


@router.post("/generate-summary")
async def generate_summary():

    task = generate_ai_summary.delay("Adaptive Workflow System")

    return {"task_id": task.id, "status": "processing"}


@router.get("/task-status/{task_id}")
async def get_task_status(task_id: str):

    task_result = AsyncResult(task_id)

    response = {
        "task_id": task_id,
        "status": task_result.status,
        "result": task_result.result if task_result.ready() else None,
    }

    return response
