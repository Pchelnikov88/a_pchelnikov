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


