from fastapi import FastAPI, Depends
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import select

from .utils import classify_hs_code, calculate_customs_value
from .database import init_db, get_session
from .models import (
    ClassifyRequestModel,
    CustomsValueRequestModel,
)
from sqlmodel import Session

app = FastAPI(title="LUDARA AI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # für Produktion einschränken
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ClassifyRequest(BaseModel):
    description: str

class CustomsValueRequest(BaseModel):
    price: float
    currency: str
    freight: float
    insurance: float

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/")
def root():
    return {"status": "LUDARA backend running"}

@app.post("/classify")
def classify(req: ClassifyRequest, session: Session = Depends(get_session)):
    hs = classify_hs_code(req.description)
    entry = ClassifyRequestModel(description=req.description, hs_code=hs)
    session.add(entry)
    session.commit()
    session.refresh(entry)
    return {"hs_code": hs, "id": entry.id}

@app.post("/customs-value")
def customs_value(req: CustomsValueRequest, session: Session = Depends(get_session)):
    result = calculate_customs_value(
        req.price,
        req.currency,
        req.freight,
        req.insurance,
    )
    entry = CustomsValueRequestModel(
        price=req.price,
        currency=req.currency.upper(),
        freight=req.freight,
        insurance=req.insurance,
        price_eur=result["price_eur"],
        customs_value=result["customs_value"],
    )
    session.add(entry)
    session.commit()
    session.refresh(entry)
    return {**result, "id": entry.id}

@app.get("/events")
def list_events(limit: int = 50, session: Session = Depends(get_session)):
    events = []

    stmt1 = select(ClassifyRequestModel).order_by(ClassifyRequestModel.created_at.desc()).limit(limit)
    for row in session.exec(stmt1):
        events.append({
            "type": "HS",
            "time": row.created_at,
            "description": row.description,
            "hs_code": row.hs_code,
        })

    stmt2 = select(CustomsValueRequestModel).order_by(CustomsValueRequestModel.created_at.desc()).limit(limit)
    for row in session.exec(stmt2):
        events.append({
            "type": "Zollwert",
            "time": row.created_at,
            "price": row.price,
            "currency": row.currency,
            "customs_value": row.customs_value,
        })

    events.sort(key=lambda e: e["time"], reverse=True)
    return events[:limit]
