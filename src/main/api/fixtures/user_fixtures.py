import pytest
import random
from typing import Tuple
from src.main.api.models.create_user_request import CreateUserRequest
from dataclasses import dataclass
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_secret_request import CreateUserSecretRequest
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.credit_response import CreditResponse
from src.main.api.models.credit_request import CreditRequest
from src.main.api.generators.model_generator import RandomModelGenerator

@pytest.fixture
def create_user_request(api_manager: ApiManager)-> CreateUserRequest:
    """Фикстура для генерации пользователя(ROLE_USER)"""
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(user_request)
    return user_request

@pytest.fixture
def user_with_account(api_manager: ApiManager, create_user_request: CreateUserRequest) -> Tuple[CreateUserRequest, CreateAccountResponse]:
    """Создает пользователя и банковский счет для него.
    Возвращает кортеж: (объект пользователя, объект счета)"""
    account = api_manager.user_steps.create_account(create_user_request)
    return create_user_request, account

@pytest.fixture
def user_with_two_accounts(
    api_manager: ApiManager,
    create_user_request: CreateUserRequest
) -> Tuple[CreateUserRequest, CreateAccountResponse, CreateAccountResponse, float, float]:
    """Создает пользователя, два счета и пополняет их случайными суммами.
    Возвращает кортеж: (пользователь, первый_счет, второй_счет, сумма_1, сумма_2)"""
    # 1. Создаем первый счет и пополняем
    first_account = api_manager.user_steps.create_account(create_user_request)
    _, deposit_amount_1 = api_manager.user_steps.deposit_random_amount(create_user_request, first_account.id)

    # 2. Создаем второй счет и пополняем
    second_account = api_manager.user_steps.create_account(create_user_request)
    _, deposit_amount_2 = api_manager.user_steps.deposit_random_amount(create_user_request, second_account.id)

    return create_user_request, first_account, second_account, deposit_amount_1, deposit_amount_2

@dataclass
class UserWithCredit:
    user: CreateUserSecretRequest
    account: CreateAccountResponse
    credit: CreditResponse
    credit_amount: float

@pytest.fixture
def create_credit_user_request(api_manager: ApiManager) -> CreateUserSecretRequest:
    """Генерирует и создает пользователя с ролью ROLE_CREDIT_SECRET"""
    user_request = RandomModelGenerator.generate(CreateUserSecretRequest)
    api_manager.admin_steps.create_user(user_request)
    return user_request

@pytest.fixture
def user_with_credit(api_manager: ApiManager, create_credit_user_request: CreateUserSecretRequest) -> UserWithCredit:
    """Создает счет и берет кредит на случайную сумму (от 5000 до 15000).
    Возвращает dataclass с пользователем, счетом, кредитом и суммой кредита"""
    account = api_manager.user_steps.create_account(create_credit_user_request)

    # Генерируем случайную сумму кредита в рамках бизнес-требований
    credit_amount = round(random.uniform(5000.0, 15000.0), 2)

    credit_request = CreditRequest(accountId=account.id, amount=credit_amount, termMonths=12)
    credit_response = api_manager.user_steps.take_credit(create_credit_user_request, credit_request)

    return UserWithCredit(
        user=create_credit_user_request,
        account=account,
        credit=credit_response,
        credit_amount=credit_amount
    )