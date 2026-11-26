import httpx
import pytest
import string
import secrets
import uuid

@pytest.fixture
def admin_login_token():
    '''Авторизация администратора'''
    admin_auth_response = httpx.post(
        url="http://localhost:4111/api/auth/token/login",
        json={
            "username": "admin",
            "password": "123456"
        }
    )

    token = admin_auth_response.json().get('token') 

    assert admin_auth_response.status_code == 200, f'Ошибка авторизации администратора, статус код {admin_auth_response.status_code}'
    assert token is not None, f'Ошибка при получении токена авторизации, токен: {token}'
    
    return token

def generaet_user_data():
    '''Генерация пользовательских данных'''
    username = f'User{uuid.uuid4().hex[:8]}'
    alpha = string.ascii_uppercase+string.digits+"!@#$%&"
    password = (
        secrets.choice(string.ascii_uppercase)
        + secrets.choice(string.ascii_lowercase)
        + secrets.choice(string.digits)
        + secrets.choice("!@#$%")
        + "".join(secrets.choice(alpha) for _ in range(8))
        )

    return {"username": username, "password": password}


@pytest.fixture
def get_user_data():
    user_data = generaet_user_data()
    return user_data


@pytest.fixture
def create_user(admin_login_token):
    '''Создание пользователя'''

    def _create_user(role="ROLE_USER"):
        user_data = generaet_user_data()
        create_user_response = httpx.post(
            url="http://localhost:4111/api/admin/create",
            json={**user_data, "role": role},
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {admin_login_token}"
            }
        )
        assert create_user_response.status_code == 200, f'Ошибка создания пользователя. Статус код: {create_user_response.status_code}\n{create_user_response.text}'

        return {**user_data, "role": role}
    return _create_user



@pytest.fixture
def user_login_token(create_user):
    '''Авторизация пользователя'''

    auth_user_response = httpx.post(
        url="http://localhost:4111/api/auth/token/login",
        json={
            'username': create_user.get('username'),
            'password': create_user.get('password')
        }
    )

    assert auth_user_response.status_code == 200, f'Ошибка авторизации пользователя. Статус код: {auth_user_response.status_code}'

    token = auth_user_response.json().get('token')

    return token