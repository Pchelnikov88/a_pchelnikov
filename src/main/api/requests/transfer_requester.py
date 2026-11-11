from http import HTTPStatus
import requests
from src.main.api.models.transfer_request import TransferRequest
from src.main.api.models.transfer_response import TransferResponse
from src.main.api.requests.requester import Requester


class TransferRequester(Requester):
    def post(self, transfer_request: TransferRequest) -> TransferResponse | requests.Response:
        url = f"{self.base_url}/account/transfer"
        response = requests.post(
            url=url,
            json=transfer_request.model_dump(),
            headers=self.headers
        )

        self.response_spec(response)

        # Если ответ успешный (200), парсим в модель
        if response.status_code == HTTPStatus.OK:
            return TransferResponse(**response.json())

        # Если ответ с ошибкой, возвращаем сырой Response
        return response




"""from http import HTTPStatus
import requests
from src.main.api.configs.config import Config
from src.main.api.models.repay_request import RepayRequest
from src.main.api.models.repay_response import RepayResponse
from src.main.api.requests.requester import Requester


class RepayCreditRequester(Requester):
    def post(self, repay_request: RepayRequest) -> RepayResponse | requests.Response:
        url = f"{Config.fetch('backendUrl')}/credit/repay"
        response = requests.post(
            url=url,
            json=repay_request.model_dump(),
            headers=self.headers
        )
        self.response_spec(response)

        if response.status_code == HTTPStatus.OK:
            return RepayResponse(**response.json())
        return response """