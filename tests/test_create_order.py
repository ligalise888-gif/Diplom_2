import allure
import requests

from data import Urls, Messages, TestData


class TestCreateOrder:

    @allure.title('Создание заказа с авторизацией и ингредиентами')
    @allure.description('Проверяем, что авторизованный пользователь может оформить заказ')
    def test_create_order_with_auth_and_ingredients_returns_success(self, created_user, ingredient_ids):
        user, access_token = created_user
        payload = {'ingredients': ingredient_ids}

        response = requests.post(
            Urls.BASE_URL + Urls.ORDERS,
            json=payload,
            headers={'Authorization': access_token}
        )

        assert response.status_code == 200
        assert response.json()['success'] is True
        assert response.json()['order']['number'] is not None

    @allure.title('Создание заказа без авторизации')
    @allure.description('Проверяем поведение системы при оформлении заказа без токена')
    def test_create_order_without_auth_returns_success(self, ingredient_ids):
        payload = {'ingredients': ingredient_ids}

        response = requests.post(Urls.BASE_URL + Urls.ORDERS, json=payload)

        assert response.status_code == 200
        assert response.json()['success'] is True
        assert response.json()['order']['number'] is not None

    @allure.title('Создание заказа без ингредиентов')
    @allure.description('Проверяем, что пустой список ингредиентов не принимается')
    def test_create_order_without_ingredients_returns_error(self, created_user):
        user, access_token = created_user
        payload = {'ingredients': TestData.EMPTY_INGREDIENTS}

        response = requests.post(
            Urls.BASE_URL + Urls.ORDERS,
            json=payload,
            headers={'Authorization': access_token}
        )

        assert response.status_code == 400
        assert response.json()['success'] is False
        assert response.json()['message'] == Messages.INGREDIENTS_REQUIRED

    @allure.title('Создание заказа с неверным хешем ингредиента')
    @allure.description('Проверяем, что при несуществующем хеше сервер возвращает ошибку')
    def test_create_order_with_invalid_ingredient_hash_returns_error(self, created_user):
        user, access_token = created_user
        payload = {'ingredients': TestData.INVALID_INGREDIENT_HASH}

        response = requests.post(
            Urls.BASE_URL + Urls.ORDERS,
            json=payload,
            headers={'Authorization': access_token}
        )

        assert response.status_code == 500
        assert 'Internal Server Error' in response.text