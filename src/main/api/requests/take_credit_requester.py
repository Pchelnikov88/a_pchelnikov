from http import HTTPStatus
import requests
from src.main.api.configs.config import Config
from src.main.api.models.credit_request import CreditRequest
from src.main.api.models.credit_response import CreditResponse
from src.main.api.requests.requester import Requester


class TakeCreditRequester(Requester):
    def post(self, credit_request: CreditRequest) -> CreditResponse | requests.Response:
        # Берем base_url из Config, так как self.base_url может не быть
        url = f"{self.base_url}/credit/request"
        response = requests.post(
            url=url,
            json=credit_request.model_dump(),
            headers=self.headers
        )
        self.response_spec(response)

        if response.status_code == HTTPStatus.CREATED:
            return CreditResponse(**response.json())
        return response