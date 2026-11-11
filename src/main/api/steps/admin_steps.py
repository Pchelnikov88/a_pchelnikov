from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.steps.base_steps import BaseSteps
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.models.login_user_request import LoginUserRequest

"""Степа — это прослойка между
тестом и реквестером, по сути отдельная бизнес-операция: «создать
пользователя», «авторизоваться», «получить заказ». Именно в степах
формируются все данные запроса: headers, body, query- и path-
параметры и прочее. Степа может связать несколько вызовов в один
сценарий и возвращает тесту уже готовый результат — например,
созданную сущность 

Что лежит в вашей папке steps:
base_steps.py - Базовый класс, от которого наследуются остальные. 
admin_steps.py - Действия, доступные только администратору:
user_steps.py - Действия обычного пользователя:"""

class AdminSteps(BaseSteps):
    def create_user(self, create_user_request: CreateUserRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username="admin", password="123456"),
            Endpoint.ADMIN_CREATE_USER,
            ResponseSpecs.request_ok()
        ).post(create_user_request)

        self.created_obj.append(response)
        return response

    def delete_user(self, user_id: int):
        CrudRequester(
            RequestSpecs.auth_headers(username="admin", password="123456"),
            Endpoint.ADMIN_DELETE_USER,
            ResponseSpecs.request_ok()
        ).delete(user_id)

    def create_invalid_user(self, create_user_request: CreateUserRequest):
        CrudRequester(
            RequestSpecs.auth_headers(username="admin", password="123456"),
            Endpoint.ADMIN_CREATE_USER,
            ResponseSpecs.request_bad()
        ).post(create_user_request)

    def login_user(self, login_user_request: LoginUserRequest):
        response = ValidateCrudRequester(
            RequestSpecs.unauth_headers(),
            Endpoint.LOGIN_USER,
            ResponseSpecs.request_ok()
        ).post(login_user_request)
        return response