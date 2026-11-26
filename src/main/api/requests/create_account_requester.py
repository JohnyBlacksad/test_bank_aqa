import httpx

from main.api.models.create_account_response import CreateAccountResponse
from main.api.requests.requests import Requester


class CreateAccountRequester(Requester):
    def post(self, model=None) -> CreateAccountResponse | httpx.Response:
        url = f'{self.base_url}/account/create'
        response = httpx.post(
            url=url,
            headers=self.headers
        )
        self.response_spec(response)
        return CreateAccountResponse(**response.json())