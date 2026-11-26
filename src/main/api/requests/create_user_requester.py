import httpx
import http

from main.api.models.create_user_request import CreateUserRequest
from main.api.models.create_user_response import CreateUserResponse
from main.api.requests.requests import Requester


class CreateUserRequester(Requester):
    def post(self, create_user_request: CreateUserRequest) -> CreateUserResponse:
        url = f'{self.base_url}/admin/create'
        response = httpx.post(
            url=url,
            json=create_user_request.model_dump(),
            headers=self.headers
        )

        self.response_spec(response)
        
        if response.status_code in (http.HTTPStatus.OK, http.HTTPStatus.CREATED):
            return CreateUserResponse(**response.json())

        return response