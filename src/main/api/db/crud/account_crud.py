from src.main.api.db.models.account_table import Account
from sqlalchemy.orm import Session


class AccountCrudDb:
    @staticmethod
    def get_account_by_id(db: Session, account_id: int) -> Account | None:
        """Метод для получения банковского счета из базы данных по его ID"""
        return db.query(Account).filter_by(id=account_id).first()

    @staticmethod
    def delete_account(db: Session, account_id: int) -> None:
        """Метод нужен для удаления банковского счета из базы данных по его ID"""
        account = db.query(Account).filter_by(id=account_id).first()
        if account:
            db.delete(account)
            db.commit()