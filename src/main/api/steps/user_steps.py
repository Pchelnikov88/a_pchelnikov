import random
from requests import Response
from typing import Tuple, Any, Dict
from src.main.api.models.transfer_request import TransferRequest
from src.main.api.requests.transfer_requester import TransferRequester
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.requests.deposit_requester import DepositRequester
from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_request import CreditRequest
from src.main.api.models.credit_response import CreditResponse
from src.main.api.models.repay_request import RepayRequest
from src.main.api.models.repay_response import RepayResponse
from src.main.api.requests.take_credit_requester import TakeCreditRequester
from src.main.api.requests.repay_credit_requester import RepayCreditRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps


class UserSteps(BaseSteps):
    def create_account(self, create_user_request: CreateUserRequest) -> CreateAccountResponse:
        response = CrudRequester(
            RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password
            ),
            Endpoint.CREATE_ACCOUNT,
            ResponseSpecs.request_created()
        ).post(model=None)
        return CreateAccountResponse(**response.json())

    def take_credit(self, create_user_request: CreateUserRequest, credit_request: CreditRequest) -> CreditResponse:
        return TakeCreditRequester(
            request_spec=RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password
            ),
            response_spec=ResponseSpecs.request_created()
        ).post(credit_request)

    def repay_credit(self, create_user_request: CreateUserRequest, repay_request: RepayRequest) -> RepayResponse:
        return RepayCreditRequester(
            request_spec=RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password
            ),
            response_spec=ResponseSpecs.request_ok()
        ).post(repay_request)

    def deposit_random_amount(self, create_user_request: CreateUserRequest, account_id: int) -> Tuple[Dict[str, Any], float]:
        """Генерирует случайную сумму от 1000 до 9000, пополняет счет и возвращает ответ и сумму"""
        amount = round(random.uniform(1000.0, 9000.0), 2)

        deposit_request = DepositRequest(accountId=account_id, amount=amount)

        response = DepositRequester(
            request_spec=RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password
            ),
            response_spec=ResponseSpecs.request_ok()
        ).post(deposit_request)

        return response, amount

    def deposit(self, create_user_request: CreateUserRequest, deposit_request: DepositRequest) -> Dict[str, Any]:
        """Сценарий пополнения счета. Ожидает успешный ответ 200 OK."""
        return DepositRequester(
            request_spec=RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password
            ),
            response_spec=ResponseSpecs.request_ok()
        ).post(deposit_request)

    def transfer(self, create_user_request: CreateUserRequest, transfer_request: TransferRequest) -> Any:
        """Сценарий перевода денег между счетами. Ожидает 200 OK"""
        return TransferRequester(
            request_spec=RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password
            ),
            response_spec=ResponseSpecs.request_ok()
        ).post(transfer_request)

    def transfer_random_amount(self, create_user_request: CreateUserRequest, from_account_id: int, to_account_id: int) -> Tuple[Any, float]:
        """Генерирует случайную сумму перевода (от 500 до 10000) и выполняет перевод.
        Возвращает ответ API и сгенерированную сумму"""
        amount = round(random.uniform(500.0, 10000.0), 2)

        transfer_request = TransferRequest(
            fromAccountId=from_account_id,
            toAccountId=to_account_id,
            amount=amount
        )

        response = self.transfer(create_user_request, transfer_request)
        return response, amount

    def transfer_amount(self, create_user_request: CreateUserRequest, from_account_id: int, to_account_id: int, amount: float) -> Any:
        """Переводит указанную сумму между счетами"""
        transfer_request = TransferRequest(
            fromAccountId=from_account_id,
            toAccountId=to_account_id,
            amount=amount
        )
        return TransferRequester(
            request_spec=RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password
            ),
            response_spec=ResponseSpecs.request_ok()
        ).post(transfer_request)

    def deposit_invalid_account(self, create_user_request: CreateUserRequest, deposit_request: DepositRequest) -> Response:
        """Сценарий пополнения несуществующего счета. Ожидает 404 Not Found."""
        return DepositRequester(
            request_spec=RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password
            ),
            response_spec=ResponseSpecs.request_not_found()
        ).post(deposit_request)

    def transfer_invalid_amount(self, create_user_request: CreateUserRequest, transfer_request: TransferRequest) -> Any:
        """Сценарий перевода с невалидной суммой. Ожидает 400 Bad Request"""
        return TransferRequester(
            request_spec=RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password
            ),
            response_spec=ResponseSpecs.request_bad()
        ).post(transfer_request)