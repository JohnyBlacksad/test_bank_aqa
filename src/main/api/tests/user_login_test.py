import httpx
import pytest


@pytest.mark.api
class TestUserLogin:
    def test_login_admin(self):
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
        assert login_admin.json()['user']['username'] == 'admin'
        assert login_admin.json()['user']['role'] == 'ROLE_ADMIN'

    def test_login_user(self):
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
                "username": "Maxx12",
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
                "username": "Maxx12",
                "password": "Pas!sw0rd"
            }
        )

        assert login_user_response.status_code == 200
        assert login_user_response.json().get('user').get('username') == "Maxx12"
        assert login_user_response.json().get('user').get('role') == "ROLE_USER"
