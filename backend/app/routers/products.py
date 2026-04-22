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

@router.post("/")
def create_product(
    description: str,
    sku: str | None = None,
    origin_country: str | None = None,
    db: Session = Depends(get_db)
):
    product = models.Product(
        description=description,
        sku=sku,
        origin_country=origin_country
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

@router.get("/")
def list_products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()
