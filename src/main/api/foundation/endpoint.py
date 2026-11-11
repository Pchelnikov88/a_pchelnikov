from enum import Enum
from typing import Optional, Type
from dataclasses import dataclass
from src.main.api.models.base_model import BaseModel
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_user_response import CreateUserResponse
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.credit_request import CreditRequest
from src.main.api.models.credit_response import CreditResponse
from src.main.api.models.repay_request import RepayRequest
from src.main.api.models.repay_response import RepayResponse
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.login_user_response import LoginUserResponse

"""«реестр всех эндпоинтов» (URL-адресов) вашего API.
 Он нужен для того, чтобы в тестах и шагах (steps) не хардкодить 
 строки вроде "/admin/create" или "/credit/repay", а брать их из одного места."""

@dataclass
class EndpointConfiguration:
    url: str
    request_model: Optional[Type[BaseModel]]
    response_model: Optional[Type[BaseModel]]

class Endpoint(Enum):
    ADMIN_CREATE_USER = EndpointConfiguration(
        request_model=CreateUserRequest,
        url="/admin/create",
        response_model=CreateUserResponse
    )
    ADMIN_DELETE_USER = EndpointConfiguration(
        request_model=None,
        url="/admin/users",
        response_model=None
    )
    CREATE_ACCOUNT = EndpointConfiguration(
        request_model=None,
        url="/account/create",
        response_model=CreateAccountResponse
    )

    TAKE_CREDIT = EndpointConfiguration(
        request_model=CreditRequest,
        url="/credit/request",
        response_model=CreditResponse
    )
    REPAY_CREDIT = EndpointConfiguration(
        request_model=RepayRequest,
        url="/credit/repay",
        response_model=RepayResponse
    )

    LOGIN_USER = EndpointConfiguration(
        request_model=LoginUserRequest,
        url="/auth/token/login",
        response_model=LoginUserResponse
    )