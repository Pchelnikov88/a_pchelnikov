from src.main.api.configs.config import Config
from src.main.api.foundation.http_requester import HttpRequester
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.models.base_model import BaseModel
from typing import Optional
import allure


"""Поверх него — validated CRUD-реквестер: он знает ожидаемый статус и
модель ответа, сам проверяет статус-код и десериализует тело в Pydantic-
объект — возвращает уже типизированный Python-объект, а не сырой
JSON. Это сильно упрощает позитивные сценарии: не нужно вручную
доставать поля из .json() и повторять одни и те же проверки
структуры, тесты становятся типобезопасными, а дублирование уходит.
Что за модель и по какому URL дёргать — описано в реестре эндпоинтов,
поэтому сам реквестер остаётся универсальным. На этом же уровне
удобно логировать запрос и ответ в отчёт (Allure) — вся наблюдаемость в
одном месте."""

class ValidateCrudRequester(HttpRequester):
    def __init__(self, request_spec, endpoint, response_spec):
        super().__init__(request_spec, endpoint, response_spec)
        self.crud_requester = CrudRequester(
            request_spec=request_spec,
            endpoint=endpoint,
            response_spec=response_spec
        )

    def post(self, model: Optional[BaseModel] = None) -> Optional[BaseModel]:
        response = self.crud_requester.post(model)
        with allure.step(f"POST {Config.fetch('backendUrl')}{self.endpoint.value.url} and Validated Model"):
            allure.attach(f"Validated Model response: {self.endpoint.value.response_model.__name__}")

        self.response_spec(response)
        return self.endpoint.value.response_model.model_validate(response.json())

    def delete(self, user_id: int):
        response = self.crud_requester.delete(user_id)
        self.response_spec(response)
        return self.endpoint.value.response_model.model_validate(response.json())