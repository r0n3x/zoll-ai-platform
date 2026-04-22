from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import models
from ..ai_client import classify_product_llm

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/products/{product_id}/classify")
async def classify_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    candidates = [
        {"code": t.code, "description": t.description}
        for t in db.query(models.TariffNode).limit(20).all()
    ]

    result = await classify_product_llm(
        description=product.description,
        technical_data=product.technical_data,
        candidates=candidates
    )

    classification = models.Classification(
        product_id=product.id,
        proposed_code=result.get("code"),
        confidence=result.get("confidence", 0.0),
        ai_explanation=result.get("reasoning", "")
    )
    db.add(classification)
    db.commit()
    db.refresh(classification)
    return classification
