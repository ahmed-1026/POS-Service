from sqlalchemy import Column, Integer, String
from db.db import Base, engine

class Branch(Base):
    __tablename__ = 'branches'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    secret_key = Column(String, nullable=False)

Base.metadata.create_all(engine)