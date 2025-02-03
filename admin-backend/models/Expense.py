from sqlalchemy import Column, Integer, String, Float, DateTime, Date
from db.db import Base


class Expense(Base):
    __tablename__ = 'expenses'

    _id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(String, nullable=False)
    updated_at = Column(String, nullable=False)