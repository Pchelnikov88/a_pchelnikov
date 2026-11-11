from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.requests.requester import Requester
import requests

"""В конечной архитектуре эта папка не нужна!!!!"""

class CreateAccountRequester(Requester):
    def post(self, model=None) -> CreateAccountResponse:
        url = f"{self.base_url}/account/create"
        response = requests.post(
            url=url,
            headers=self.headers,
        )

        self.response_spec(response)
        return CreateAccountResponse(**response.json())

"""Папка requests (в вашей структуре src/main/api/requests/) содержит классы, которые называются Requester'ы. 
Они нужны для того, чтобы отправлять HTTP-запросы к конкретным эндпоинтам API.

Если steps — это «сценарии» (что сделать: создать юзера, перевести деньги), 
то requests — это «исполнители» (как именно отправить запрос на сервер).

requester.py (Базовый класс)
Это абстрактный класс (наследник ABC), от которого наследуются все остальные реквестеры.

Зачем нужен: Он задает общий контракт. В его конструкторе сохраняются headers (заголовки), 
base_url (базовый URL) и response_spec (правила проверки ответа). 
Все остальные реквестеры используют эти поля, чтобы не дублировать код инициализации.

"""

