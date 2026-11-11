from src.main.api.configs.config import Config
from src.main.api.foundation.http_requester import HttpRequester
from src.main.api.models.base_model import BaseModel
from typing import Optional
from requests import Response
import requests
import allure

"""это «ядро» (движок) вашего фреймворка. Файлы нужны для того, 
чтобы тесты и шаги (steps) не писали код HTTP-запросов вручную (requests.post(...)), 
а использовали готовые универсальные классы."""

"""Реквестеры разделены на два уровня. Низкоуровневый отвечает
исключительно за отправку HTTP-запроса: берёт базовый URL, заголовки
и авторизацию из конфига, выполняет вызов через сессию requests и
возвращает сырой response . Его удобно использовать в негативных
сценариях, когда важен именно код ответа и тело ошибки."""

class CrudRequester(HttpRequester):
    def post(self, model: Optional[BaseModel] = None) -> Response:
        body = model.model_dump() if model is not None else ""

        with allure.step(f"POST {Config.fetch('backendUrl')}{self.endpoint.value.url}"):
            allure.attach(str(body), "Request body", allure.attachment_type.JSON)

            response = requests.post(
                url=f"{Config.fetch('backendUrl')}{self.endpoint.value.url}",
                headers=self.request_spec["headers"],
                json=body
            )

            allure.attach(
                response.text,
                "Response body",
                allure.attachment_type.JSON
            )

        self.response_spec(response)
        return response

    def delete(self, user_id: int) -> Response:
        response = requests.delete(
            url=f"{Config.fetch('backendUrl')}{self.endpoint.value.url}/{user_id}",
            headers=self.request_spec["headers"]
        )
        self.response_spec(response)
        return response


