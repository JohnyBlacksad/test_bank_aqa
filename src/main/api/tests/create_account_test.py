import httpx
import pytest


@pytest.mark.api
class TestCreateAccount:
    def test_create_account(self):
        login_admin = httpx.post(
            url="http://localhost:4111/api/auth/token/login",
            headers={
                "Content-Type": "application/json",
                "accept": "application/json"
            },
            json={
                'username': 'admin',
                'password': '123456',
            }
        )
        
        assert login_admin.status_code == 200
        
        token = login_admin.json().get('token')
        
        create_user = httpx.post(
            url='http://localhost:4111/api/admin/create',
            json={
                "username": "Maxx13",
                "password": "Pas!sw0rd",
                "role": "ROLE_USER"
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )
        
        assert create_user.status_code == 200
        
        login_user_response = httpx.post(
            url="http://localhost:4111/api/auth/token/login",
            json={
                "username": "Maxx13",
                "password": "Pas!sw0rd"
            }
        )
        
        assert login_user_response.status_code == 200

        user_token = login_user_response.json().get('token')

        create_account_response = httpx.post(
            url="http://localhost:4111/api/account/create",
            headers={
                'accept': "application/json",
                "Authorization": f"Bearer {user_token}"
            }
        )

        assert create_account_response.status_code == 201
        assert create_account_response.json().get("id") is not None
        assert create_account_response.json().get("number") is not None
        assert isinstance(create_account_response.json().get('balance'), int)
        assert create_account_response.json().get('balance') == 0