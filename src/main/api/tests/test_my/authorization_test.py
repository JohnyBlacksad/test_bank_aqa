import httpx
import pytest

@pytest.mark.api
@pytest.mark.AUTH
class TestAuthorization:
    def test_admin_auth_successful(self):
        auth_admin_response = httpx.post(
            url="http://localhost:4111/api/auth/token/login",
            json={
                "username": "admin",
                "password": "123456"
            }
        )
        
        status_code = auth_admin_response.status_code
        assert status_code == 200

        user = auth_admin_response.json().get('user')
        username = user.get('username')
        role = user.get('role')

        assert isinstance(user, dict)
        assert username == "admin"
        assert role == "ROLE_ADMIN"

    def test_auth_created_user_successful(self, create_user):

        created_user = create_user()

        auth_user_response = httpx.post(
            url="http://localhost:4111/api/auth/token/login",
            json={
                "username": created_user.get('username'),
                "password": created_user.get('password')
            }
        )

        status_code = auth_user_response.status_code
        assert status_code == 200

        user_data = auth_user_response.json().get('user')
        assert isinstance(user_data, dict)
        
        username = user_data.get('username')
        role = user_data.get('role')
        token = auth_user_response.json().get('token')

        assert username == created_user.get('username')
        assert role == "ROLE_USER"
        assert token is not None

    def test_auth_user_with_credit_role(self, create_user):
        credit_created_user = create_user("ROLE_CREDIT_SECRET")

        auth_user_response = httpx.post(
            url="http://localhost:4111/api/auth/token/login",
            json={
                "username": credit_created_user.get('username'),
                "password": credit_created_user.get('password')
            }
        )
        assert auth_user_response.status_code == 200

        userdata = auth_user_response.json().get('user')
        assert isinstance(userdata, dict)

        username = userdata.get('username')
        role = userdata.get('role')
        token = auth_user_response.json().get('token')

        assert username == credit_created_user.get('username')
        assert role == credit_created_user.get('role')
        assert token is not None

    def test_auth_invalid_username(self, create_user):
        created_user = create_user()

        auth_user_response = httpx.post(
            url="http://localhost:4111/api/auth/token/login",
            json={
                'username': created_user.get('username')+"1",
                'password': created_user.get('password')
            }
        )

        assert auth_user_response.status_code == 401

    def test_auth_invalid_password(self, create_user):
        created_user = create_user()

        auth_user_response = httpx.post(
            url="http://localhost:4111/api/auth/token/login",
            json={
                'username': created_user.get('username'),
                'password': created_user.get('password') + ' '
            }
        )

        assert auth_user_response.status_code == 401

    def test_create_user_with_invalid_token(self, admin_login_token, get_user_data):
        token = admin_login_token + '1'
        user_data = get_user_data
        create_user_response = httpx.post(
            url = "http://localhost:4111/api/admin/create",
            json={
                'username': user_data.get('username'),
                'password': user_data.get('password')
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        assert create_user_response.status_code == 401