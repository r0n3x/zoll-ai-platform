from fastapi import APIRouter, Depends
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

@router.get("/")
def list_news(db: Session = Depends(get_db)):
    return db.query(models.NewsItem).order_by(
        models.NewsItem.published_at.desc()
    ).limit(50).all()
