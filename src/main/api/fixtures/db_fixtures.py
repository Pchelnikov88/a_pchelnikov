import pytest
from src.main.api.db.engine import SessionLocal, engine

@pytest.fixture(scope='function')
def db_session():
    """Эта фикстура используется для изоляции тестов при работе с базой данных.
    Она открывает соединение, начинает транзакцию и привязывает к ней ORM-сессию SQLAlchemy.
    В блоке finally она делает rollback (откат) транзакции. Это гарантирует, что все изменения,
    сделанные в рамках теста (создание пользователей, изменение баланса), будут автоматически
    отменены после завершения теста."""
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionLocal(bind=connection)

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()

