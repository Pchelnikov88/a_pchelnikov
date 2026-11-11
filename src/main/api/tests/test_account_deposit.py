# pytest src/main/api/tests/test_account_deposit.py
# allure serve allure-results
# python -m pytest -v src/main/api/tests --alluredir=allure-results --clean-alluredir

import requests
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
