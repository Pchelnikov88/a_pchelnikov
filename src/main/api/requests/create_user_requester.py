from http import HTTPStatus

from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_user_response import CreateUserResponse
from src.main.api.requests.requester import Requester
import requests

class CreateUserRequester(Requester):
    """Создание пользователя"""
    def post(self, create_user_request: CreateUserRequest):
        url = f"{self.base_url}/admin/create"
        response = requests.post(
            url=url,
            json=create_user_request.model_dump(),
            headers=self.headers
        )

        self.response_spec(response)
        if response.status_code in [HTTPStatus.OK, HTTPStatus.CREATED]:
            return CreateUserResponse(**response.json())
        return response

"""Берет модель CreateUserRequest, превращает её в JSON (model_dump()), 
формирует URL {base_url}/admin/create, подставляет заголовки и отправляет POST. 
Если ответ 200 OK — возвращает модель CreateUserResponse, иначе — сырой Response.

Зачем нужен: Инкапсулирует логику отправки запроса именно на этот эндпоинт. 
Если завтра изменится URL или формат ответа, вы поменяете это только в одном месте."""