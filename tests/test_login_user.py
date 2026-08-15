import allure
import pytest
import requests

from data import Urls, Messages
from helpers import generate_user_data


class TestLoginUser:

    @allure.title('Вход под существующим пользователем')
    @allure.description('Проверяем, что зарегистрированный пользователь может войти в систему')
    def test_login_existing_user_returns_success(self, created_user):
        user, access_token = created_user
        payload = {'email': user['email'], 'password': user['password']}

        response = requests.post(Urls.BASE_URL + Urls.LOGIN, json=payload)

        assert response.status_code == 200
        assert response.json()['success'] is True
        assert response.json()['accessToken'] is not None

    @allure.title('Вход с неверным логином или паролем')
    @allure.description('Проверяем, что при неверных данных вход не выполняется')
    @pytest.mark.parametrize('wrong_field', ['email', 'password'])
    def test_login_with_wrong_credentials_returns_error(self, created_user, wrong_field):
        user, access_token = created_user
        payload = {'email': user['email'], 'password': user['password']}
        payload[wrong_field] = generate_user_data()[wrong_field]

        response = requests.post(Urls.BASE_URL + Urls.LOGIN, json=payload)

        assert response.status_code == 401
        assert response.json()['message'] == Messages.INCORRECT_CREDENTIALS