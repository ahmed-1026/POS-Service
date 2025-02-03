from sqlalchemy.orm import Session
from models.Branch import Branch


def get_branch_by_key(db: Session, branch_key: str) -> Branch:
    return db.query(Branch).filter(Branch.secret_key == branch_key).first()

def get_branch_by_id(db: Session, branch_id: int) -> Branch:
    return db.query(Branch).filter(Branch.id == branch_id).first()