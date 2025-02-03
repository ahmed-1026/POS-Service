from .db import dbs, add_session_to_dbs, Base
from sqlalchemy.orm import Session
from fastapi import HTTPException
import re
from sqlalchemy import create_engine


from models.Branch import Branch

db: Session = dbs["MainDbSession"]()
branches = db.query(Branch).all()
for branch in branches:
    add_session_to_dbs(branch.name)


def create_database(db_name: str):
    # Preprocess the database name
    db_name = re.sub(r'\W+', '_', db_name)
    if db_name in dbs:
        raise HTTPException(status_code=400, detail="Database already exists")

    # Create SQLite database file
    add_session_to_dbs(db_name)