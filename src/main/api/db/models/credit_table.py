from sqlalchemy import Column, Integer, Float, ForeignKey
from src.main.api.db.base import Base

class Credit(Base):
    __tablename__ = "credit"
    id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey("account.id"), nullable=False)
    amount = Column(Float, nullable=False)
    term_months = Column(Integer, nullable=False)
    balance = Column(Float, nullable=False)