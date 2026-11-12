# pytest src/main/api/tests/test_credit_repay.py
# allure serve allure-results
# python -m pytest -v src/main/api/tests/test_credit_repay.py --alluredir=allure-results --clean-alluredir (удаляется старые записи)
# allure serve allure-results

import pytest
from sqlalchemy.orm import Session
from src.main.api.models.repay_request import RepayRequest
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit
from src.main.api.classes.api_manager import ApiManager
from src.main.api.fixtures.user_fixtures import UserWithCredit

@pytest.mark.api
class TestCreditRepay:
    def test_repay_credit_valid(
            self,
            api_manager: ApiManager,
            user_with_credit: UserWithCredit,
            db_session: Session
    ) -> None:

        # 1. Распаковываем данные
        user = user_with_credit.user
        account = user_with_credit.account
        credit = user_with_credit.credit
        credit_amount = user_with_credit.credit_amount

        # 2. ЦЕЛЕВАЯ СТЕПА: Погашаем кредит на полную сумму
        repay_request = RepayRequest(
            creditId=credit.creditId,
            accountId=account.id,
            amount=credit_amount
        )
        response = api_manager.user_steps.repay_credit(user, repay_request)

        # 3. Проверки ответа API
        assert response.creditId == credit.creditId, "ID кредита в ответе на погашение не совпадает с ожидаемым"
        assert response.amountDeposited == credit_amount, f"Сумма погашения в ответе не равна {credit_amount}"

        # 4. Проверка целостности данных в БД
        db_account = Account.get_account_by_id(db_session, account.id)
        db_credit = Credit.get_credit_by_id(db_session, credit.creditId)

        assert db_account is not None, "Счет не найден в БД"
        assert db_credit is not None, "Кредит не найден в БД"

        # После полного погашения баланс кредита и счета должен быть 0
        assert db_credit.balance == 0.0, f"Баланс кредита в БД не равен 0 после погашения. Текущий: {db_credit.balance}"
        assert db_account.balance == 0.0, f"Баланс счета в БД не равен 0 после погашения кредита. Текущий: {db_account.balance}"

    def test_repay_credit_invalid(
            self,
            api_manager: ApiManager,
            user_with_credit: UserWithCredit,
            db_session: Session
    ) -> None:

        # 1. Распаковываем данные
        user = user_with_credit.user
        account = user_with_credit.account
        credit = user_with_credit.credit
        credit_amount = user_with_credit.credit_amount

        # 2. Фиксируем состояние до попытки погашения
        db_account_before = Account.get_account_by_id(db_session, account.id)
        db_credit_before = Credit.get_credit_by_id(db_session, credit.creditId)
        account_balance_before = db_account_before.balance
        credit_balance_before = db_credit_before.balance

        # 3. Формируем запрос с суммой, превышающей долг (например, на 5000 больше)
        repay_request = RepayRequest(
            creditId=credit.creditId,
            accountId=account.id,
            amount=credit_amount + 5000.0
        )

        # 4. ЦЕЛЕВАЯ СТЕПА (ожидает 422, внутри степы сработает AssertionError)
        with pytest.raises(AssertionError):
            api_manager.user_steps.repay_credit(user, repay_request)

        # 5. Проверка целостности в БД (данные не должны измениться)
        db_session.expire_all()

        db_account_after = Account.get_account_by_id(db_session, account.id)
        db_credit_after = Credit.get_credit_by_id(db_session, credit.creditId)

        assert db_account_after.balance == account_balance_before, \
            f"Баланс счета изменился после неудачного погашения! Было {account_balance_before}, стало {db_account_after.balance}"

        assert db_credit_after.balance == credit_balance_before, \
            f"Баланс кредита изменился после неудачного погашения! Было {credit_balance_before}, стало {db_credit_after.balance}"



















"""import pytest
from sqlalchemy.orm import Session
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user_secret_request import CreateUserSecretRequest
from src.main.api.models.credit_request import CreditRequest
from src.main.api.models.repay_request import RepayRequest
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit
from src.main.api.classes.api_manager import ApiManager

@pytest.mark.api
class TestCreditRepay:
    def test_repay_credit_valid(self, api_manager: ApiManager, db_session: Session) -> None:
        # 1. Генерируем пользователя и даем ему роль CREDIT_SECRET
        create_user_request = RandomModelGenerator.generate(CreateUserSecretRequest)

        # 2. Создаем пользователя через админа
        response_user = api_manager.admin_steps.create_user(create_user_request)
        assert create_user_request.username == response_user.username, "Имя пользователя в ответе не совпадает с отправленным"

        # 3. Создаем счет для пользователя
        account = api_manager.user_steps.create_account(create_user_request)

        # 4. Берем кредит (5000 на 12 месяцев)
        credit_request = CreditRequest(accountId=account.id, amount=5000.0, termMonths=12)
        credit_response = api_manager.user_steps.take_credit(create_user_request, credit_request)

        # 5. Погашаем кредит на полную сумму
        repay_request = RepayRequest(
            creditId=credit_response.creditId,
            accountId=account.id,
            amount=5000.0
        )
        response = api_manager.user_steps.repay_credit(create_user_request, repay_request)

        # 6. Проверки ответа API
        assert response.creditId == credit_response.creditId, "ID кредита в ответе на погашение не совпадает с ожидаемым"
        assert response.amountDeposited == 5000.0, "Сумма погашения в ответе не равна 5000.0"

        # 7. Проверка целостности данных в БД

        # Получаем счет и кредит из БД
        db_account = Account.get_account_by_id(db_session, account.id)
        db_credit = Credit.get_credit_by_id(db_session, credit_response.creditId)

        # Проверяем, что записи существуют
        assert db_account is not None, "Счет не найден в БД"
        assert db_credit is not None, "Кредит не найден в БД"

        # Проверяем баланс кредита в БД. После полного погашения он должен стать 0.
        assert db_credit.balance == 0.0, f"Баланс кредита в БД не равен 0 после погашения. Текущий: {db_credit.balance}"

        # Проверяем баланс счета.
        assert db_account.balance == 0.0, f"Баланс счета в БД не равен 0 после погашения кредита. Текущий: {db_account.balance}"

    def test_repay_credit_invalid(self, api_manager: ApiManager, db_session: Session) -> None:
        # 1. Подготовка: пользователь со счетом и кредитом
        create_user_request = RandomModelGenerator.generate(CreateUserSecretRequest)

        api_manager.admin_steps.create_user(create_user_request)
        account = api_manager.user_steps.create_account(create_user_request)

        credit_request = CreditRequest(accountId=account.id, amount=5000.0, termMonths=12)
        credit_response = api_manager.user_steps.take_credit(create_user_request, credit_request)

        # 2. Фиксируем состояние до попытки погашения
        db_account_before = Account.get_account_by_id(db_session, account.id)
        db_credit_before = Credit.get_credit_by_id(db_session, credit_response.creditId)

        assert db_account_before is not None and db_credit_before is not None, "Подготовка не удалась: счета или кредита нет в БД"

        account_balance_before = db_account_before.balance
        credit_balance_before = db_credit_before.balance

        # 3. Пытаемся погасить сумму, превышающую долг (10000 вместо 5000)
        repay_request = RepayRequest(
            creditId=credit_response.creditId,
            accountId=account.id,
            amount=10000.0
        )

        # 4. Ожидаем ошибку (сервер вернет 422, что вызовет AssertionError в ResponseSpecs)
        with pytest.raises(AssertionError):
            api_manager.user_steps.repay_credit(create_user_request, repay_request)

        # 5. Проверка целостности в БД (данные не должны измениться)

        # Обновляем сессию, чтобы получить актуальные данные из БД (если они вдруг изменились)
        db_session.expire_all()

        db_account_after = Account.get_account_by_id(db_session, account.id)
        db_credit_after = Credit.get_credit_by_id(db_session, credit_response.creditId)

        # Проверяем, что балансы остались прежними
        assert db_account_after.balance == account_balance_before, \
            f"Баланс счета изменился после неудачного погашения! Было {account_balance_before}, стало {db_account_after.balance}"

        assert db_credit_after.balance == credit_balance_before, \
            f"Баланс кредита изменился после неудачного погашения! Было {credit_balance_before}, стало {db_credit_after.balance}"""


