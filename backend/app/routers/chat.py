from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import models

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/conversations")
def create_conversation(type: str = "bot", db: Session = Depends(get_db)):
    conv = models.Conversation(type=type, created_by=None)
    db.add(conv)
    db.commit()
    db.refresh(conv)
    return conv

@router.get("/conversations")
def list_conversations(db: Session = Depends(get_db)):
    return db.query(models.Conversation).all()

@router.get("/conversations/{conversation_id}/messages")
def get_messages(conversation_id: int, db: Session = Depends(get_db)):
    return db.query(models.Message).filter(
        models.Message.conversation_id == conversation_id
    ).all()

@router.post("/conversations/{conversation_id}/messages")
def send_message(conversation_id: int, content: str, db: Session = Depends(get_db)):
    conv = db.query(models.Conversation).filter(
        models.Conversation.id == conversation_id
    ).first()

    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")

    msg = models.Message(
        conversation_id=conversation_id,
        sender_user_id=None,
        content=content,
        is_bot=False
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)

    if conv.type == "bot":
        bot_msg = models.Message(
            conversation_id=conversation_id,
            sender_user_id=None,
            content=f"Bot-Antwort zu: {content}",
            is_bot=True
        )
        db.add(bot_msg)
        db.commit()
        db.refresh(bot_msg)
        return {"user": msg.content, "bot": bot_msg.content}

    return {"message": msg.content}
