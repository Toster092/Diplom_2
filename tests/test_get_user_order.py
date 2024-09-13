import allure
import requests
from data import Constants
from faker import Faker

faker = Faker()


class TestGetUserOrder():
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

    @allure.title('Проверка успешного получения заказов авторизованным пользователем')
    def test_get_user_order_with_auth_success(self):
        headers = {
            'Authorization': f"Bearer {self.token}"
        }
        response = requests.get(Constants.URL_ORDER, headers=headers)

        assert response.status_code == 200 and response.json()['success'] == True

    @allure.title('Проверка появления ошибки при получении заказов  неавторизованным пользователем')
    def test_get_user_order_without_auth_show_error(self):
        response = requests.get(Constants.URL_ORDER)

        assert response.status_code == 401 and response.json() == Constants.BODY_NOT_AUTH