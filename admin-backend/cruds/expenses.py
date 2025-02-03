from sqlalchemy.orm import Session
from sqlalchemy import DateTime, Date
from models.Expense import Expense


def add_expense(session: Session, expense_data: dict):
    # print(f"Adding expense: {expense_data}")
    date: DateTime = expense_data["updated_at"]
    expense = Expense(**expense_data)
    session.add(expense)
    session.commit()
    session.refresh(expense)
    return expense

def view_expense(session: Session, expense_id: int):
    return session.query(Expense).filter(Expense._id == expense_id).first()