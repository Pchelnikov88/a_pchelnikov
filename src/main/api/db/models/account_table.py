from sqlalchemy import Column, Integer, String, Float, ForeignKey
from src.main.api.db.base import Base

class Account(Base):
    __tablename__ = "account"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    number = Column(String, unique=True, nullable=False)
    balance = Column(Float, nullable=False)

    def __repr__(self): #  это магический метод в Python, который определяет, как объект будет выглядеть в виде строки для разработчика.
        return f"<Account(id={self.id}, user_id={self.user_id}, number={self.number}, balance={self.balance})>"