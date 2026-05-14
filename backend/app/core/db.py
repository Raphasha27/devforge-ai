import os
from sqlalchemy import create_engine, Column, Integer, String, JSON, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://devforge:devforge@db:5432/devforge")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class DBRepo(Base):
    __tablename__ = "repositories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    metadata_json = Column(JSON)
    health_score = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

class DBMessage(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    actor = Column(String)
    emoji = Column(String)
    text = Column(String)
    channel = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

class DBSuggestion(Base):
    __tablename__ = "suggestions"
    id = Column(Integer, primary_key=True, index=True)
    repo = Column(String)
    suggestion = Column(String)
    risk = Column(String)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
