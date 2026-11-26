import httpx

from main.api.models.login_user_request import LoginUserRequest
from main.api.models.login_user_response import LoginUserResponse
from main.api.requests.requests import Requester


class LoginUserRequester(Requester):
    def post(self, login_user_request: LoginUserRequest) -> LoginUserResponse | httpx.Response:
        
        url =f'{self.base_url}/auth/token/login'
        response = httpx.post(
            url=url,
            json=login_user_request.model_dump(),
            headers=self.headers
        )
        self.response_spec(response)
        return LoginUserResponse(**response.json())