from sqlalchemy import (
    Column, Integer, String, DateTime, Boolean, ForeignKey,
    Text, Float, JSON
)
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="user")
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    owner_user_id = Column(Integer, ForeignKey("users.id"))
    sku = Column(String, index=True)
    description = Column(Text, nullable=False)
    technical_data = Column(JSON, nullable=True)
    origin_country = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User")

class Classification(Base):
    __tablename__ = "classifications"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    proposed_code = Column(String, index=True)
    final_code = Column(String, index=True)
    confidence = Column(Float)
    ai_explanation = Column(Text)
    status = Column(String, default="proposed")
    reviewed_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    reviewed_at = Column(DateTime, nullable=True)

    product = relationship("Product")
    reviewer = relationship("User", foreign_keys=[reviewed_by])

class TariffNode(Base):
    __tablename__ = "tariff_nodes"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, index=True)
    level = Column(String)
    description = Column(Text)
    region = Column(String)
    notes = Column(Text)
    valid_from = Column(DateTime, nullable=True)
    valid_to = Column(DateTime, nullable=True)
    source = Column(String)

class TariffUpdate(Base):
    __tablename__ = "tariff_updates"
    id = Column(Integer, primary_key=True, index=True)
    source = Column(String)
    imported_at = Column(DateTime, default=datetime.utcnow)
    records_added = Column(Integer)
    records_updated = Column(Integer)
    status = Column(String)
    log = Column(Text)

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

class ConversationParticipant(Base):
    __tablename__ = "conversation_participants"
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    sender_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    content = Column(Text, nullable=False)
    is_bot = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class NewsItem(Base):
    __tablename__ = "news_items"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    source_url = Column(String, nullable=True)
    published_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)

class FxRate(Base):
    __tablename__ = "fx_rates"
    id = Column(Integer, primary_key=True, index=True)
    base_currency = Column(String)
    target_currency = Column(String)
    rate = Column(Float)
    date = Column(DateTime)
