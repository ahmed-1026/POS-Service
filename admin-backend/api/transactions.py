from fastapi import APIRouter, HTTPException, Depends
from models.Transaction import Transaction
from typing import List
from cruds.branches import get_branch_by_id
from db.db import get_db, dbs
from sqlalchemy.orm import Session

router = APIRouter()

# @router.post("/transactions/", response_model=Transaction)
# async def add_transaction(transaction: Transaction, db: Session = Depends(get_db, key="MainDbSession")):
#     db.add(transaction)
#     db.commit()
#     db.refresh(transaction)
#     return transaction

@router.get("/branches/{branch_id}/transactions/")
async def get_transactions(branch_id: int, db: Session = Depends(get_db)):
    branch = get_branch_by_id(db, branch_id)
    if not branch:
        print("Branch not found")
        raise HTTPException(status_code=400, detail="Invalid branch key")
    db = dbs[branch.name]()
    transactions = db.query(Transaction).all()
    return transactions
