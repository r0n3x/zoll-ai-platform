from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# utils.py liegt im selben Ordner wie main.py → also backend.utils
from backend.utils import classify_hs_code, calculate_customs_value

app = FastAPI(title="LUDARA AI Backend")

# ---------------------------------------------------------
# CORS – erlaubt deinem Frontend, das Backend aufzurufen
# ---------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # oder spezifisch: ["https://ludara-ai.onrender.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------
# Request Models
# ---------------------------------------------------------
class ClassifyRequest(BaseModel):
    description: str

class CustomsValueRequest(BaseModel):
    price: float
    currency: str
    freight: float
    insurance: float

# ---------------------------------------------------------
# Routes
# ---------------------------------------------------------
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
