from fastapi import APIRouter
from pydantic import BaseModel
from app.services.llm_service import generate_response

router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    personality: str = "calm"


@router.post("/chat")
async def chat(payload: ChatRequest):
    reply = generate_response(
        payload.message,
        payload.personality,
        memory="User is building Arise"
    )

    return {"reply": reply}
