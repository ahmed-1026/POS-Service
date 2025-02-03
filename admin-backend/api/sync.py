from fastapi import APIRouter, HTTPException, Depends, Request
from models.Branch import Branch
from typing import List
from db.db import dbs
from db.actions import create_database
from cruds.transactions import add_transaction
from cruds.expenses import add_expense
from cruds.branches import get_branch_by_key
from sqlalchemy.orm import Session
from pydantic import BaseModel

router = APIRouter()

def get_db_session(request: Request):
    print(f"Request URL: {request.url}")
    db = dbs["MainDbSession"]()
    try:
        yield db
    finally:
        db.close()

@router.post("/sync/{branch_key}")
async def list_branches(branch_key: str, data: dict, db: Session = Depends(get_db_session)):
    branch = get_branch_by_key(db, branch_key)
    if not branch:
        print("Branch not found")
        raise HTTPException(status_code=400, detail="Invalid branch key")
    print(branch.name)
    db = dbs[branch.name]()
    transactions = data.get("transactions", [])
    if transactions:
        [add_transaction(db, transaction) for transaction in transactions]
    expenses = data.get("expenses", [])
    if expenses:
        print("Adding expenses", expenses)
        [add_expense(db, expense) for expense in expenses]

@router.post("/branches")
async def create_branch(branch_data: dict, db: Session = Depends(get_db_session)):
    print(branch_data)
    check_branch = db.query(Branch).filter(Branch.name == branch_data["name"]).first()
    if check_branch:
        raise HTTPException(status_code=400, detail="Branch already exists")

    create_database(branch_data["name"])
    new_branch = Branch(**branch_data)
    db.add(new_branch)
    db.commit()
    db.refresh(new_branch)
    return new_branch
