from fastapi import FastAPI
from pydantic import BaseModel
from utils import classify_hs_code, calculate_customs_value
from crawler import crawl_description

app = FastAPI(title="LUDARA AI Backend")

# -----------------------------
# Request Models
# -----------------------------

class ClassifyRequest(BaseModel):
    description: str

class CustomsValueRequest(BaseModel):
    price: float
    currency: str
    freight: float
    insurance: float

# -----------------------------
# Routes
# -----------------------------

@app.get("/")
def root():
    return {"status": "LUDARA backend running"}

@app.post("/classify")
def classify(req: ClassifyRequest):
    hs = classify_hs_code(req.description)
    return {"hs_code": hs}

@app.post("/customs-value")
def customs_value(req: CustomsValueRequest):
    result = calculate_customs_value(
        req.price,
        req.currency,
        req.freight,
        req.insurance
    )
    return result

@app.get("/crawl")
def crawl(q: str):
    text = crawl_description(q)
    hs = classify_hs_code(text)
    return {
        "found_text": text,
        "hs_code": hs
    }
