# pytest src/main/api/tests/test_account_deposit.py
# allure serve allure-results
# python -m pytest -v src/main/api/tests --alluredir=allure-results --clean-alluredir

import pytest
import random
from typing import Tuple
from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.db.crud.account_crud import AccountCrudDb as Account

@pytest.mark.api
class TestAccountDeposit:
    def test_deposit_valid(
        self,
        api_manager: ApiManager,
        user_with_account: Tuple[CreateUserRequest, CreateAccountResponse],
        db_session: Session
    ) -> None:

        # 1. Распаковываем кортеж из фикстуры
        user, account = user_with_account

        # 2. ЦЕЛЕВАЯ СТЕПА: Пополняем счет на случайную сумму
        response, deposit_amount = api_manager.user_steps.deposit_random_amount(
            user, account.id
        )

        # 3. Проверки (ответ API)
        assert response["id"] == account.id, "ID счета в ответе не совпадает"
        assert response["balance"] == deposit_amount, f"Баланс в ответе не равен {deposit_amount}"

        # 4. Проверки (БД)
        db_account = Account.get_account_by_id(db_session, account.id)
        assert db_account.balance == deposit_amount, f"Баланс в БД не совпадает. В БД: {db_account.balance}"

    def test_deposit_invalid_account(
            self,
            api_manager: ApiManager,
            user_with_account: Tuple[CreateUserRequest, CreateAccountResponse],
            db_session: Session
    ) -> None:

        # 1. Распаковываем кортеж
        user, _ = user_with_account

        # 2. Генерируем несуществующий ID счета и валидную сумму
        invalid_account_id = random.randint(100_000, 999_999)
        valid_amount = round(random.uniform(1000.0, 9000.0), 2)

        # 3. Формируем запрос
        deposit_request = DepositRequest(accountId=invalid_account_id, amount=valid_amount)

        # 4. ЦЕЛЕВАЯ СТЕПА: пополняем несуществующий счет (ожидает 404)
        api_manager.user_steps.deposit_invalid_account(user, deposit_request)

        # 5. Проверка целостности данных в БД:
        db_account = Account.get_account_by_id(db_session, invalid_account_id)

        assert db_account is None, f"Счет с ID {invalid_account_id} не должен существовать в БД, но он был найден"




    """def test_deposit_valid(self, api_manager: ApiManager, db_session: Session) -> None:
        # 1. Генерируем уникального пользователя
        create_user_request = RandomModelGenerator.generate(CreateUserRequest)
        api_manager.admin_steps.create_user(create_user_request)

        # 2. Создаем счет
        account = api_manager.user_steps.create_account(create_user_request)

        # 3. Пополняем счет на случайную сумму
        response, deposit_amount = api_manager.user_steps.deposit_random_amount(
            create_user_request, account.id
        )

        # 4. Проверяем ответ API
        assert response["id"] == account.id, "ID счета в ответе не совпадает"
        assert response["balance"] == deposit_amount, f"Баланс в ответе не равен {deposit_amount}"

        # 5. Проверяем БД
        db_account = Account.get_account_by_id(db_session, account.id)
        assert db_account.balance == deposit_amount, f"Баланс в БД не совпадает. В БД: {db_account.balance}"

    def test_deposit_invalid_account(self, api_manager: ApiManager) -> None:
        # 1. Генерируем уникального пользователя
        create_user_request = RandomModelGenerator.generate(CreateUserRequest)

        # 2. Создаем пользователя через админа
        api_manager.admin_steps.create_user(create_user_request)

        # 3. Генерируем несуществующий ID счета и валидную сумму
        invalid_account_id = random.randint(100_000, 999_999)

        # Сумму генерируем в рамках требований (1000-9000),
        valid_amount = round(random.uniform(1000.0, 9000.0), 2)

        # 4. Пытаемся пополнить несуществующий счет
        deposit_request = DepositRequest(accountId=invalid_account_id, amount=valid_amount)

        # 5. Ожидаем ошибку 404 Not Found
        with pytest.raises(AssertionError):
            api_manager.user_steps.deposit(create_user_request, deposit_request) """





"""import requests
import pytest

@pytest.mark.api
class TestCreateAccount:
    def test_create_account(self):
        login_admin_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json={
                "username": "admin",
                "password": "123456"
            },
            headers={
                "accept": "application/json",
                "Content-Type": "application/json"
            }
        )

        assert login_admin_response.status_code == 200, "Не удалось авторизоваться под администратором"
        token = login_admin_response.json().get("token")

        create_user_response = requests.post(
            url="http://localhost:4111/api/admin/create",
            json={
                "username": "Maga051",
                "password": "Pas!sw0rd",
                "role": "ROLE_USER"
            },
            headers={
                "accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        assert create_user_response.status_code == 200, "Не удалось создать пользователя через администратора"

        login_user_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json={
                "username": "Maga050",
                "password": "Pas!sw0rd"
            },
            headers={
                "accept": "application/json",
                "Content-Type": "application/json"
            }
        )

        assert login_user_response.status_code == 200, "Не удалось авторизоваться под новым пользователем"
        token_user = login_user_response.json().get("token")

        create_account_response = requests.post(
            url="http://localhost:4111/api/account/create",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token_user}"
            }
        )

        assert create_account_response.status_code == 201, "Не удалось создать банковский счет"
        assert create_account_response.json().get("balance") == 0, "Начальный баланс созданного счета не равен 0"
        accountId = create_account_response.json().get("id")

        account_deposit_response = requests.post(
            url="http://localhost:4111/api/account/deposit",
            json={
                "accountId": accountId,
                "amount": 1000
            },
            headers={
                "accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token_user}"
            }
        )

        assert account_deposit_response.status_code == 200, "Не удалось пополнить счет"
        assert account_deposit_response.json().get("id") == accountId, "ID счета в ответе на пополнение не совпадает с ожидаемым"
        assert account_deposit_response.json().get("balance") == 1000, "Баланс после пополнения не равен 1000"


    def test_create_account_invalid(self):
        login_admin_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json={
                "username": "admin",
                "password": "123456"
            },
            headers={
                "accept": "application/json",
                "Content-Type": "application/json"
            }
        )

        assert login_admin_response.status_code == 200, "Не удалось авторизоваться под администратором"
        token = login_admin_response.json().get("token")

        create_user_response = requests.post(
            url="http://localhost:4111/api/admin/create",
            json={
                "username": "Maga070",
                "password": "Pas!sw0rd",
                "role": "ROLE_USER"
            },
            headers={
                "accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        assert create_user_response.status_code == 200, "Не удалось создать пользователя через администратора"

        login_user_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json={
                "username": "Maga07",
                "password": "Pas!sw0rd"
            },
            headers={
                "accept": "application/json",
                "Content-Type": "application/json"
            }
        )

        assert login_user_response.status_code == 200, "Не удалось авторизоваться под новым пользователем"
        token_user = login_user_response.json().get("token")

        create_account_response = requests.post(
            url="http://localhost:4111/api/account/create",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token_user}"
            }
        )

        assert create_account_response.status_code == 201, "Не удалось создать банковский счет"
        assert create_account_response.json().get("balance") == 0, "Начальный баланс созданного счета не равен 0"
        accountId = create_account_response.json().get("id")

        account_deposit_response = requests.post( # Пополнение не существующего счета
            url="http://localhost:4111/api/account/deposit",
            json={
                "accountId": 5555,
                "amount": 1000
            },
            headers={
                "accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token_user}"
            }
        )

        assert account_deposit_response.status_code == 404, "Сервер не вернул 404 при пополнении несуществующего счета"

"""