# pytest src/main/api/tests/test_account_transfer.py
# allure serve allure-results
# python -m pytest -v src/main/api/tests --alluredir=allure-results --clean-alluredir

import pytest
from sqlalchemy.orm import Session
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.transfer_request import TransferRequest
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.requests.create_account_requester import CreateAccountRequester
from src.main.api.requests.transfer_requester import TransferRequester
from src.main.api.requests.deposit_requester import DepositRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.db.crud.account_crud import AccountCrudDb as Account


@pytest.mark.api
class TestAccountTransfer:
    def test_transfer_between_own_accounts(self, db_session: Session):
        username = "Alex15"

        # Создаем пользователя через админа
        user_creds = CreateUserRequest(username=username, password="Pas!sw0rd", role="ROLE_USER")
        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(user_creds)

        # Получаем заголовки для нового пользователя
        user_auth_spec = RequestSpecs.auth_headers(username=username, password="Pas!sw0rd")

        # 1. Создаем первый счет и пополняем его
        first_account = CreateAccountRequester(
            request_spec=user_auth_spec,
            response_spec=ResponseSpecs.request_created()
        ).post()

        DepositRequester(
            request_spec=user_auth_spec,
            response_spec=ResponseSpecs.request_ok()
        ).post(DepositRequest(accountId=first_account.id, amount=1000.0))

        # 2. Создаем второй счет
        second_account = CreateAccountRequester(
            request_spec=user_auth_spec,
            response_spec=ResponseSpecs.request_created()
        ).post()

        # 3. Выполняем перевод средств
        transfer_amount = 600.0
        transfer_request = TransferRequest(
            fromAccountId=first_account.id,
            toAccountId=second_account.id,
            amount=transfer_amount
        )

        response = TransferRequester(
            request_spec=user_auth_spec,
            response_spec=ResponseSpecs.request_ok()
        ).post(transfer_request)

        # 4. Проверки ответа API
        assert response.fromAccountId == first_account.id, "ID счета списания в ответе не совпадает с отправленным"
        assert response.toAccountId == second_account.id, "ID счета зачисления в ответе не совпадает с отправленным"
        # Баланс первого счета: 1000.0 - 600.0 = 400.0
        assert response.fromAccountIdBalance == 400.0, "Баланс счета списания в ответе API неверен после перевода"

        # 5. Проверки в БД

        # Получаем оба счета из БД по их ID
        db_first_account = Account.get_account_by_id(db_session, first_account.id)
        db_second_account = Account.get_account_by_id(db_session, second_account.id)

        # Проверяем, что счета существуют в БД
        assert db_first_account is not None, "Первый счет не найден в БД"
        assert db_second_account is not None, "Второй счет не найден в БД"

        # Проверяем балансы в БД
        # Первый счет (списание): должен быть 400.0
        assert db_first_account.balance == 400.0, f"Баланс первого счета в БД не совпадает. Ожидалось 400.0, получено {db_first_account.balance}"

        # Второй счет (зачисление): должен быть 600.0
        assert db_second_account.balance == 600.0, f"Баланс второго счета в БД не совпадает. Ожидалось 600.0, получено {db_second_account.balance}"

    def test_transfer_to_non_existent_account(self):
        username = "Alex105"

        user_creds = CreateUserRequest(username=username, password="Pas!sw0rd", role="ROLE_USER")
        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(user_creds)

        user_auth_spec = RequestSpecs.auth_headers(username=username, password="Pas!sw0rd")

        # Создаем счет для отправки
        first_account = CreateAccountRequester(
            request_spec=user_auth_spec,
            response_spec=ResponseSpecs.request_created()
        ).post()

        # Пытаемся перевести на несуществующий ID
        transfer_request = TransferRequest(
            fromAccountId=first_account.id,
            toAccountId=999999,
            amount=600.0
        )

        # Ожидаем 404
        TransferRequester(
            request_spec=user_auth_spec,
            response_spec=ResponseSpecs.request_not_found()
        ).post(transfer_request)