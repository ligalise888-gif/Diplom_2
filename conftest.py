import pytest
import requests

from data import Urls
from helpers import generate_user_data


@pytest.fixture
def user_data():
    return generate_user_data()


@pytest.fixture
def created_user(user_data):
    response = requests.post(Urls.BASE_URL + Urls.REGISTER, json=user_data)
    assert response.status_code == 200, f'Не удалось создать пользователя: {response.text}'
    access_token = response.json().get('accessToken')

    yield user_data, access_token

    if access_token:
        requests.delete(Urls.BASE_URL + Urls.USER, headers={'Authorization': access_token})


@pytest.fixture
def ingredient_ids():
    response = requests.get(Urls.BASE_URL + Urls.INGREDIENTS)
    assert response.status_code == 200, f'Не удалось получить список ингредиентов: {response.text}'
    data = response.json().get('data', [])
    assert len(data) >= 2, 'В ответе меньше двух ингредиентов'
    return [data[0]['_id'], data[1]['_id']]