import pytest


@pytest.mark.api
class TestCreateAccount:
    def test_create_account(self, api_manager, create_user_request):
        
        response = api_manager.user_steps.create_account(create_user_request)

        assert response.id > 0
        assert response.number.isdigit()
        assert response.balance == 0