# pytest src/main/api/tests/test_account_transfer.py
# allure serve allure-results
# python -m pytest -v src/main/api/tests --alluredir=allure-results --clean-alluredir

import pytest
import random
from typing import Tuple
from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.models.transfer_request import TransferRequest

@pytest.mark.api
class TestAccountTransfer:
    def test_transfer_between_own_accounts(
        self,
        api_manager: ApiManager,
        user_with_two_accounts: Tuple[CreateUserRequest, CreateAccountResponse, CreateAccountResponse, float, float],
        db_session: Session
    ) -> None:

        # 1. Распаковываем данные из фикстуры
        user, first_account, second_account, deposit_amount_1, deposit_amount_2 = user_with_two_accounts

        # 2. ЦЕЛЕВАЯ СТЕПА: Переводим на второй счет ровно ту сумму, которой пополнили первый
        response = api_manager.user_steps.transfer_amount(
            user,
            from_account_id=first_account.id,
            to_account_id=second_account.id,
            amount=deposit_amount_1
        )

        # 3. Проверки ответа API
        assert response.fromAccountId == first_account.id, "ID счета списания не совпадает"
        assert response.toAccountId == second_account.id, "ID счета зачисления не совпадает"
        assert response.fromAccountIdBalance == 0.0, f"Ожидался остаток 0.0, получено {response.fromAccountIdBalance}"

        # 4. Проверки в БД
        db_first = Account.get_account_by_id(db_session, first_account.id)
        db_second = Account.get_account_by_id(db_session, second_account.id)

        assert db_first.balance == 0.0, f"Остаток на первом счете должен быть 0.0, в БД: {db_first.balance}"

        expected_second_balance = round(deposit_amount_2 + deposit_amount_1, 2)
        assert db_second.balance == expected_second_balance, f"Сумма на втором счете должна быть {expected_second_balance}, в БД: {db_second.balance}"

    def test_transfer_negative_amount(
        self,
        api_manager: ApiManager,
        user_with_two_accounts: Tuple[CreateUserRequest, CreateAccountResponse, CreateAccountResponse, float, float],
        db_session: Session
    ) -> None:

        # 1. Распаковываем данные из фикстуры
        user, first_account, second_account, deposit_amount_1, deposit_amount_2 = user_with_two_accounts

        # 2. Фиксируем балансы ДО попытки перевода
        db_first_before = Account.get_account_by_id(db_session, first_account.id)
        db_second_before = Account.get_account_by_id(db_session, second_account.id)

        # 3. Генерируем случайную отрицательную сумму
        negative_amount = -round(random.uniform(500.0, 5000.0), 2)

        # 4. Формируем запрос (обходим Pydantic-валидацию)
        transfer_request = TransferRequest.model_construct(
            fromAccountId=first_account.id,
            toAccountId=second_account.id,
            amount=negative_amount
        )

        # 5. ЦЕЛЕВАЯ СТЕПА: перевод невалидной суммы со счета на счет пользователя (ожидаем 400)
        api_manager.user_steps.transfer_invalid_amount(user, transfer_request)

        # 6. ПРОВЕРКА ЦЕЛОСТНОСТИ В БД:
        db_session.expire_all() # # Обновляем сессию, чтобы получить актуальные данные

        db_first_after = Account.get_account_by_id(db_session, first_account.id)
        db_second_after = Account.get_account_by_id(db_session, second_account.id)

        assert db_first_after.balance == db_first_before.balance, \
            f"Баланс первого счета изменился после неудачного перевода! Было {db_first_before.balance}, стало {db_first_after.balance}"

        assert db_second_after.balance == db_second_before.balance, \
            f"Баланс второго счета изменился после неудачного перевода! Было {db_second_before.balance}, стало {db_second_after.balance}"




""" 
@pytest.mark.api
class TestAccountTransfer:
    def test_transfer_between_own_accounts(self, api_manager: ApiManager, db_session: Session) -> None:
        # 1. Создаем пользователя
        create_user_request = RandomModelGenerator.generate(CreateUserRequest)
        api_manager.admin_steps.create_user(create_user_request)

        # 2. Создаем первый счет и пополняем его случайной суммой
        first_account = api_manager.user_steps.create_account(create_user_request)
        _, deposit_amount_1 = api_manager.user_steps.deposit_random_amount(create_user_request, first_account.id)

        # 3. Создаем второй счет и ТОЖЕ пополняем его случайной суммой
        second_account = api_manager.user_steps.create_account(create_user_request)
        _, deposit_amount_2 = api_manager.user_steps.deposit_random_amount(create_user_request, second_account.id)

        # 4. Переводим на второй счет ровно ту сумму, которой пополнили первый
        response = api_manager.user_steps.transfer_amount(
            create_user_request,
            from_account_id=first_account.id,
            to_account_id=second_account.id,
            amount=deposit_amount_1
        )

        # 5. Проверяем ответ API
        assert response.fromAccountId == first_account.id, "ID счета списания не совпадает"
        assert response.toAccountId == second_account.id, "ID счета зачисления не совпадает"
        # На первом счете должно остаться 0
        assert response.fromAccountIdBalance == 0.0, f"Ожидался остаток 0.0, получено {response.fromAccountIdBalance}"

        # 6. Проверяем БД
        db_first = Account.get_account_by_id(db_session, first_account.id)
        db_second = Account.get_account_by_id(db_session, second_account.id)

        # На первом счете 0
        assert db_first.balance == 0.0, f"Остаток на первом счете должен быть 0.0, в БД: {db_first.balance}"

        # На втором счете: изначальный баланс (deposit_amount_2) + перевод (deposit_amount_1)
        expected_second_balance = round(deposit_amount_2 + deposit_amount_1, 2)
        assert db_second.balance == expected_second_balance, f"Сумма на втором счете должна быть {expected_second_balance}, в БД: {db_second.balance}"

    def test_transfer_negative_amount(self, api_manager: ApiManager) -> None:
        # 1. Создаем пользователя
        create_user_request = RandomModelGenerator.generate(CreateUserRequest)
        api_manager.admin_steps.create_user(create_user_request)

        # 2. Создаем первый счет и пополняем его случайной суммой
        first_account = api_manager.user_steps.create_account(create_user_request)
        _, _ = api_manager.user_steps.deposit_random_amount(create_user_request, first_account.id)

        # 3. Создаем второй счет и пополняем его случайной суммой
        second_account = api_manager.user_steps.create_account(create_user_request)
        _, _ = api_manager.user_steps.deposit_random_amount(create_user_request, second_account.id)

        # 4. Генерируем случайную отрицательную сумму
        negative_amount = -round(random.uniform(500.0, 5000.0), 2)

        # 5. Формируем запрос (обходим Pydantic-валидацию)
        transfer_request = TransferRequest.model_construct(
            fromAccountId=first_account.id,
            toAccountId=second_account.id,
            amount=negative_amount
        )

        # 6. Отправляем запрос и ожидаем 400 Bad Request
        TransferRequester(
            request_spec=RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password
            ),
            response_spec=ResponseSpecs.request_bad()
        ).post(transfer_request)
 """










"""
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
        ).post(transfer_request) """