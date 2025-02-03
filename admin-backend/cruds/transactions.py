from sqlalchemy.orm import Session
from models.Transaction import Transaction


def add_transaction(session: Session, transaction_data: dict):
    # print(f"Adding transaction: {transaction_data}")
    try:
        transaction_data["discount"] = float(transaction_data.get("discount", 0))
    except ValueError:
        transaction_data["discount"] = 0.0
    check_transaction = session.query(Transaction).filter(Transaction.order_number == transaction_data["order_number"]).first()
    if check_transaction:
        # print("Transaction already exists")
        return check_transaction
    transaction = Transaction(**transaction_data)
    session.add(transaction)
    session.commit()
    session.refresh(transaction)
    return transaction

def view_transaction(session: Session, transaction_id: int) -> Transaction:
    return session.query(Transaction).filter(Transaction._id == transaction_id).first()