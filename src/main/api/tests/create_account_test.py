import pytest

from main.api.models.create_user_request import CreateUserRequest
from main.api.requests.create_account_requester import CreateAccountRequester
from main.api.requests.create_user_requester import CreateUserRequester
from main.api.specs.request_specs import RequestSpecs
from main.api.specs.response_specs import ResponseSpecs


@pytest.mark.api
class TestCreateAccount:
    def test_create_account(self):

        create_user_request = CreateUserRequest(username="Maxx1356ss", password="Pas!sw0rd", role="ROLE_USER")
        
        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username='admin', password='123456'),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)
        

        response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            response_spec=ResponseSpecs.request_created()
        ).post()

        assert response.id > 0
        assert response.number.isdigit()
        assert response.balance == 0