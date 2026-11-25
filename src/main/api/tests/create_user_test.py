import httpx
import pytest


@pytest.mark.api
class TestCreateUser:
    def test_create_user(self):

        login_admin_response = httpx.post(
            url="http://localhost:4111/api/auth/token/login",
            json={
                "username": "admin",
                "password": "123456",
            },
            headers={
                "Content-Type": "application/json",
                "accept": "application/json"
            }
        )

        assert login_admin_response.status_code == 200
        token = login_admin_response.json().get('token')

        create_user_response = httpx.post(
            url='http://localhost:4111/api/admin/create',
            json={
                "username": "Max220",
                "password": "Pas!sw0rd",
                "role": "ROLE_USER"
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        assert create_user_response.status_code == 200
        assert create_user_response.json().get('username') == 'Max220'
        assert create_user_response.json().get('role') == 'ROLE_USER'

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
        token = login_admin.json().get('token')

        create_user_response = httpx.post(
            url='http://localhost:4111/api/admin/create',
            json={
                "username": username,
                "password": password,
                "role": "ROLE_USER"
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        assert create_user_response.status_code == 400
        assert create_user_response.json().get('error') != None