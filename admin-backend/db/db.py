from fastapi import HTTPException
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
import re


Base = declarative_base()

# Database Setup
DATABASE_URL = "sqlite:///pharmacy.db"

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)

MainDbSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

dbs = {
    "MainDbSession": MainDbSession,
}

def add_session_to_dbs(name: str):
    db_url = f"sqlite:///{name}.db"
    db_engine = create_engine(db_url)
    db_session = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
    Base.metadata.create_all(db_engine)
    dbs[name] = db_session

def get_db():
    db = MainDbSession()
    try:
        yield db
    finally:
        db.close()

# Dependency for FastAPI routes

