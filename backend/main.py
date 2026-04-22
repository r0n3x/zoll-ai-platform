from fastapi import FastAPI
from pydantic import BaseModel

# utils.py liegt im selben Ordner wie main.py → also backend.utils
from backend.utils import classify_hs_code, calculate_customs_value

app = FastAPI(title="LUDARA AI Backend")

class ClassifyRequest(BaseModel):
    description: str

class CustomsValueRequest(BaseModel):
    price: float
    currency: str
    freight: float
    insurance: float

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
