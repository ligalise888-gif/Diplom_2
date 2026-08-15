import allure
import pytest
import requests

from data import Urls, Messages
from helpers import generate_user_data


class TestCreateUser:

    @allure.title('Создание уникального пользователя')
    @allure.description('Проверяем, что пользователь с новыми данными успешно регистрируется')
    def test_create_unique_user_returns_success(self):
        user = generate_user_data()
        response = requests.post(Urls.BASE_URL + Urls.REGISTER, json=user)

        assert response.status_code == 200
        assert response.json()['success'] is True

        access_token = response.json().get('accessToken')
        if access_token:
            requests.delete(Urls.BASE_URL + Urls.USER, headers={'Authorization': access_token})

    @allure.title('Создание пользователя, который уже зарегистрирован')
    @allure.description('Проверяем, что повторная регистрация с теми же данными возвращает ошибку')
    def test_create_existing_user_returns_error(self, created_user):
        user, access_token = created_user
        response = requests.post(Urls.BASE_URL + Urls.REGISTER, json=user)

        assert response.status_code == 403
        assert response.json()['message'] == Messages.USER_ALREADY_EXISTS

    @allure.title('Создание пользователя без одного из обязательных полей')
    @allure.description('Проверяем, что без email, password или name регистрация не проходит')
    @pytest.mark.parametrize('missing_field', ['email', 'password', 'name'])
    def test_create_user_without_required_field_returns_error(self, missing_field):
        user = generate_user_data()
        del user[missing_field]

        response = requests.post(Urls.BASE_URL + Urls.REGISTER, json=user)

        assert response.status_code == 403
        assert response.json()['message'] == Messages.REQUIRED_FIELDS