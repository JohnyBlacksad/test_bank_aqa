import pytest

from main.api.models.create_user_request import CreateUserRequest
from main.api.models.login_user_request import LoginUserRequest
from main.api.requests.create_user_requester import CreateUserRequester
from main.api.requests.login_user_requester import LoginUserRequester
from main.api.specs.request_specs import RequestSpecs
from main.api.specs.response_specs import ResponseSpecs


@pytest.mark.api
class TestUserLogin:
    def test_login_admin(self):
        login_request = LoginUserRequest(username='admin', password='123456')

        response = LoginUserRequester(
            request_spec=RequestSpecs.unauth_headers(),
            response_spec=ResponseSpecs.request_ok()
        ).post(login_request)


        assert response.user.usernmae == login_request.username
        assert response.user.role == 'ROLE_ADMIN'


    def test_login_user(self):
        create_user_request = CreateUserRequest(username='Maxx12564', password='Pas!sw0rd', role='ROLE_USER')
        
        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username='admin', password='123456'),
            response_spec=ResponseSpecs.request_bad()
        ).post(create_user_request)

        login_user_request = LoginUserRequest(username=create_user_request.username, password=create_user_request.password)

        response = LoginUserRequester(
                    request_spec=RequestSpecs.unauth_headers(),
                    response_spec=ResponseSpecs.request_ok()
                ).post(login_user_request)

        assert response.user.usernmae == create_user_request.username
        assert response.user.role == create_user_request.role
