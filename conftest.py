import pytest
import requests

from data import Urls
from helpers import generate_user_data


@pytest.fixture
def created_user():
    user = generate_user_data()
    response = requests.post(Urls.BASE_URL + Urls.REGISTER, json=user)
    access_token = response.json().get('accessToken')

    yield user, access_token

    if access_token:
        requests.delete(Urls.BASE_URL + Urls.USER, headers={'Authorization': access_token})


@pytest.fixture
def ingredient_ids():
    response = requests.get(Urls.BASE_URL + Urls.INGREDIENTS)
    data = response.json()['data']
    return [data[0]['_id'], data[1]['_id']]