from pydantic import BaseModel


class GeminiResponse(BaseModel):
    gemini_response: str
