from src.main.api.foundation.endpoint import Endpoint
from typing import Dict, Callable

"""Это базовый класс (родитель) для всех реквестеров. 
Его задача — хранить в себе общие данные, которые нужны любому запросу: 
заголовки, эндпоинт и правило проверки ответа."""

class HttpRequester:
    def __init__(self, request_spec: Dict, endpoint: Endpoint, response_spec: Callable):
        self.request_spec = request_spec
        self.endpoint = endpoint
        self.response_spec = response_spec