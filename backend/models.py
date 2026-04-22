from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime

class ClassifyRequestModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    description: str
    hs_code: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class CustomsValueRequestModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    price: float
    currency: str
    freight: float
    insurance: float
    price_eur: float
    customs_value: float
    created_at: datetime = Field(default_factory=datetime.utcnow)

class NewsItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    url: str
    source: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    sender: str
    text: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
