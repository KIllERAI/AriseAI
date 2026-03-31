from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
from app.services.llm_service import generate_response
from app.core.database import get_db
from app.models.models import User, Conversation, Message, Memory

router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    personality: str = "calm"
    user_id: int = 1  # Default user, can be changed later
    conversation_id: Optional[int] = None


@router.post("/chat")
async def chat(payload: ChatRequest, db: Session = Depends(get_db)):
    # Get or create conversation
    if payload.conversation_id:
        conversation = db.query(Conversation).filter(Conversation.id == payload.conversation_id).first()
    else:
        # Create new conversation for this user
        user = db.query(User).filter(User.id == payload.user_id).first()
        if not user:
            user = User(name=f"User {payload.user_id}", personality_type=payload.personality)
            db.add(user)
            db.commit()
            db.refresh(user)
        
        conversation = Conversation(user_id=user.id, title="New Chat")
        db.add(conversation)
        db.commit()
        db.refresh(conversation)

    # Fetch user's memory context
    user_memories = db.query(Memory).filter(Memory.user_id == payload.user_id).all()
    memory_context = "\n".join([f"{m.key}: {m.value}" for m in user_memories]) if user_memories else ""

    # Get LLM response
    reply = generate_response(
        payload.message,
        payload.personality,
        memory=memory_context
    )

    # Save user message
    user_message = Message(
        conversation_id=conversation.id,
        role="user",
        content=payload.message
    )
    db.add(user_message)

    # Save assistant message
    assistant_message = Message(
        conversation_id=conversation.id,
        role="assistant",
        content=reply
    )
    db.add(assistant_message)
    db.commit()

    return {
        "reply": reply,
        "conversation_id": conversation.id,
        "message_id": assistant_message.id
    }
