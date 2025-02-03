from sqlalchemy import Column, Integer, Float, Text
from db.db import Base


class Transaction(Base):
    __tablename__ = 'transactions'

    _id = Column(Integer, primary_key=True, autoincrement=True)
    ref_number = Column(Text)
    customer = Column(Integer, default=0)
    customer_name = Column(Text, default="")
    order_number = Column(Integer, nullable=False)
    discount = Column(Float, default=0)
    status = Column(Integer, default=1)
    subtotal = Column(Float, nullable=False)
    tax = Column(Float, default=0)
    order_type = Column(Integer, default=1)
    items = Column(Text, nullable=False)
    date = Column(Text, nullable=False)
    payment_type = Column(Text, nullable=False)
    payment_info = Column(Text)
    total = Column(Float, nullable=False)
    paid = Column(Float, nullable=False)
    change = Column(Float, nullable=False)
    till = Column(Integer, nullable=False)
    user = Column(Text, nullable=False)
    user_id = Column(Integer, nullable=False)