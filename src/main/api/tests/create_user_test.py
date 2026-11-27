import pytest

from main.api.generators.model_generator import RandomModelGenerator
from main.api.models.create_user_request import CreateUserRequest


@pytest.mark.api
class TestCreateUser:
    @pytest.mark.parametrize(
            "create_user_request",
            [RandomModelGenerator.generate(CreateUserRequest)]
        )
    def test_create_user(self, api_manager, create_user_request):

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
    def test_create_invalid_user(self, username, password, api_manager):
        
        create_user_request = CreateUserRequest(username=username, password=password, role='ROLE_USER')
        api_manager.admin_steps.create_invalid_user(create_user_request)