from fastapi import APIRouter, HTTPException, Depends, Request
from models.Branch import Branch
from typing import List
from db.db import dbs
from db.actions import create_database
from sqlalchemy.orm import Session

router = APIRouter()

def get_db_session(request: Request):
    print(f"Request URL: {request.url}")
    db = dbs["MainDbSession"]()
    try:
        yield db
    finally:
        db.close()

@router.get("/branches")
async def list_branches(db: Session = Depends(get_db_session)):
    return db.query(Branch).all()

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

# @router.put("/branches/{branch_id}", response_model=Branch)
# async def update_branch(branch_id: int, branch: BranchCreate):
#     for b in branches_db:
#         if b["id"] == branch_id:
#             b["name"] = branch.name
#             b["location"] = branch.location
#             return b
#     raise HTTPException(status_code=404, detail="Branch not found")

# @router.delete("/branches/{branch_id}")
# async def delete_branch(branch_id: int):
#     global branches_db
#     branches_db = [b for b in branches_db if b["id"] != branch_id]
#     return {"message": "Branch deleted successfully"}

@router.get("/branches/{branch_id}")
async def get_branch(branch_id: int, db: Session = Depends(get_db_session)):
    branch = db.query(Branch).filter(Branch.id == branch_id).first()
    if branch:
        return branch