from fastapi import FastAPI
from .database import Base, engine
from . import models
from .routers import (
    auth, products, classifications, tariffs,
    news, chat, customs_value
)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Zoll AI Platform")

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(products.router, prefix="/products", tags=["products"])
app.include_router(classifications.router, prefix="/classifications", tags=["classifications"])
app.include_router(tariffs.router, prefix="/tariffs", tags=["tariffs"])
app.include_router(news.router, prefix="/news", tags=["news"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])
app.include_router(customs_value.router, prefix="/customs-value", tags=["customs-value"])
