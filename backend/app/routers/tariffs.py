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

@router.get("/search")
def search_tariffs(query: str, db: Session = Depends(get_db)):
    return db.query(models.TariffNode).filter(
        models.TariffNode.description.ilike(f"%{query}%")
    ).limit(50).all()

@router.get("/{code}")
def get_tariff(code: str, db: Session = Depends(get_db)):
    return db.query(models.TariffNode).filter(models.TariffNode.code == code).first()
