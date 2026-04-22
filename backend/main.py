from fastapi import FastAPI, Depends
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from datetime import datetime

from .utils import classify_hs_code, calculate_customs_value, fetch_customs_news
from .database import init_db, get_session
from .models import (
    ClassifyRequestModel,
    CustomsValueRequestModel,
    NewsItem,
    Message,
)

app = FastAPI(title="LUDARA AI Backend")

# CORS – HIER KANNST DU SPÄTER allow_origins einschränken
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # z.B. ["https://ludara-ai.onrender.com"]
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
    return {"status": "LUDARA backend running", "time": datetime.utcnow()}

# -----------------------------
# HS-Code
# -----------------------------

@app.post("/classify")
def classify(req: ClassifyRequest, session: Session = Depends(get_session)):
    hs = classify_hs_code(req.description)
    entry = ClassifyRequestModel(description=req.description, hs_code=hs)
    session.add(entry)
    session.commit()
    session.refresh(entry)
    return {"hs_code": hs, "id": entry.id}

# -----------------------------
# Zollwert
# -----------------------------

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

# -----------------------------
# Events (Verlauf)
# -----------------------------

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

# -----------------------------
# News
# -----------------------------

@app.get("/news")
def get_news(session: Session = Depends(get_session)):
    stmt = select(NewsItem).order_by(NewsItem.created_at.desc()).limit(20)
    return session.exec(stmt).all()

@app.post("/news/update")
def update_news(session: Session = Depends(get_session)):
    items = fetch_customs_news()
    for item in items:
        news = NewsItem(title=item["title"], url=item["url"], source=item["source"])
        session.add(news)
    session.commit()
    return {"status": "updated", "count": len(items)}

# -----------------------------
# Messenger
# -----------------------------

@app.post("/messages/send")
def send_message(sender: str, text: str, session: Session = Depends(get_session)):
    msg = Message(sender=sender, text=text)
    session.add(msg)
    session.commit()
    session.refresh(msg)
    return {"status": "sent", "id": msg.id}

@app.get("/messages")
def get_messages(limit: int = 50, session: Session = Depends(get_session)):
    stmt = select(Message).order_by(Message.created_at.desc()).limit(limit)
    return session.exec(stmt).all()
