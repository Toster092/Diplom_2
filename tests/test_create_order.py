import allure
import requests
from data import Constants
from faker import Faker

faker = Faker()


class TestCreateOrder():
    @classmethod
    def setup_class(cls):
        cls.user_data = {
            'email': faker.email(),
            'password': faker.password(),
            'name': faker.name()
        }
        response = requests.post(Constants.URL_CREATE_USER, json=cls.user_data)
        cls.token = response.json()['accessToken'].replace('Bearer ', '')

    @classmethod
    def teardown_class(cls):
        headers = {
            'Authorization': cls.token
        }
        requests.delete(Constants.URL_CHANGE_USER, headers=headers)

    @allure.title('Проверка успешного создания заказа авторизованным пользователем')
    def test_create_order_with_auth_success(self):
        payload = {
            "ingredients": ["61c0c5a71d1f82001bdaaa6d"]
        }
        headers = {
            'Authorization': f"Bearer {self.token}"
        }
        response = requests.post(Constants.URL_ORDER, json=payload, headers=headers)

        assert response.status_code == 200 and response.json()['success'] == True

    @allure.title('Проверка появления ошибки при создании заказа без ингридиентов авторизованным пользователем')
    def test_create_order_with_auth_without_ing_shows_error(self):
        payload = {
            "ingredients": []
        }
        headers = {
            'Authorization': f"Bearer {self.token}"
        }
        response = requests.post(Constants.URL_ORDER, json=payload, headers=headers)

        assert response.status_code == 400 and response.json() == Constants.BODY_NO_INGRIDIENT

    @allure.title('Проверка появления ошибки при создании заказа с неправильным хэшем авторизованным пользователем')
    def test_create_order_with_auth_wrong_hash_shows_error(self):
        payload = {
            "ingredients": ["88"]
        }
        headers = {
            'Authorization': f"Bearer {self.token}"
        }
        response = requests.post(Constants.URL_ORDER, json=payload, headers=headers)

        assert response.status_code == 500

    @allure.title('Проверка успешного создания заказа без авторизации')
    def test_create_order_without_auth_success(self):
        payload = {
            "ingredients": ["61c0c5a71d1f82001bdaaa6d"]
        }
        response = requests.post(Constants.URL_ORDER, json=payload)

        assert response.status_code == 200 and response.json()['success'] == True

    @allure.title('Проверка появления ошибки при создании заказа без ингридиентов без авторизации')
    def test_create_order_without_auth_without_ing_shows_error(self):
        payload = {
            "ingredients": []
        }
        response = requests.post(Constants.URL_ORDER, json=payload)

        assert response.status_code == 400 and response.json() == Constants.BODY_NO_INGRIDIENT

    @allure.title('Проверка появления ошибки при создании заказа с неправильным хэшем без авторизации')
    def test_create_order_without_auth_wrong_hash_shows_error(self):
        payload = {
            "ingredients": ["88"]
        }
        response = requests.post(Constants.URL_ORDER, json=payload)

        assert response.status_code == 500