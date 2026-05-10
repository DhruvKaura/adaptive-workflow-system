from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.session import get_db
from app.domains.intelligence.schemas import GeminiResponse
from app.domains.intelligence.service import IntelligenceService
from app.integrations.ollama.client import OllamaClient

router = APIRouter(prefix="/intelligence", tags=["Workflow Intelligence"])


@router.get("/tasks/{task_id}/risk")
async def predict_task_risk(task_id: UUID, db: AsyncSession = Depends(get_db)):

    return await IntelligenceService.predict_deadline_risk(db, task_id)


@router.get("/tasks/{task_id}/insights")
async def get_task_insights(task_id: UUID, db: AsyncSession = Depends(get_db)):

    return await IntelligenceService.generate_productivity_insights(db, task_id)


@router.get("/test-ollama")
async def test_ollama(prompt: str = "Explain workflow bottlenecks in one sentence."):

    response = await OllamaClient.generate_response(prompt)

    return {"response": response}
