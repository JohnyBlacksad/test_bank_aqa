import pytest

from main.api.models.login_user_request import LoginUserRequest
from main.api.models.create_user_request import CreateUserRequest
from main.api.models.create_user_response import CreateUserResponse
from main.api.models.login_user_response import LoginUserResponse
from main.api.requests.create_user_requester import CreateUserRequester
from main.api.specs.request_specs import RequestSpecs
from main.api.specs.response_specs import ResponseSpecs

@pytest.mark.api
class TestCreateUser:
    def test_create_user(self, api_manager):

        create_user_request = CreateUserRequest(
            username="Max22055",
            password='Pas!sw0rd',
            role='ROLE_USER'
        )

        response = api_manager.admin_steps.create_user(create_user_request)
        
        
        assert create_user_request.username == response.username
        assert create_user_request.role == response.role

    @pytest.mark.parametrize(
            'username, password',
            [
                ("МАК", "Pas!sw0rd"),
                ("ab", "Pas!sw0rd"),
                ("abv!", "Pas!sw0rd"),
                ("Maxx1", "Pas!sw0rд"),
                ("Maxx2", "Pas!sw0"),
                ("Maxx3", "pas!sw0rd"),
                ("Maxx4", "PASSW0RD"),
                ("Maxx5", "PAS!SWORD")
            ]
                             )
    def test_create_invalid_user(self, username, password):
        
        create_user_request = CreateUserRequest(username=username, password=password, role='ROLE_USER')
        
        response = CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username='admin', password='123456'),
            response_spec=ResponseSpecs.request_bad()
        ).post(create_user_request)