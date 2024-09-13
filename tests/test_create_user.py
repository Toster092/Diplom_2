import allure
import requests
from data import Constants
from faker import Faker

faker = Faker()
class TestCreateUser():
    @classmethod
    def setup_class(cls):
        cls.user_data = {
            'email': faker.email(),
            'password': faker.password(),
            'name': faker.name()
        }

    def teardown_class(cls):
        login_payload = {
            'email': cls.user_data['email'],
            'password': cls.user_data['password']
        }
        login_response = requests.post(Constants.URL_LOGIN_USER, json=login_payload)
        token = login_response.json().get('accessToken')
        headers = {
            'Authorization': token
        }
        requests.delete(Constants.URL_CHANGE_USER, headers=headers)

    @allure.title('Проверка успешного создания пользователя')
    def test_create_user_success(self):
        payload = self.user_data
        response = requests.post(Constants.URL_CREATE_USER, json=payload)
        assert response.status_code == 200 and response.json()['user'] is not None

    @allure.title('Проверка появления ошибки при создании уже зарегистрированного пользователя')
    def test_create_same_user_shows_error(self):
        payload = self.user_data
        response = requests.post(Constants.URL_CREATE_USER, json=payload)
        assert response.status_code == 403 and response.json() == Constants.SAME_USER

    @allure.title('Проверка появления ошибки при незаполненном поле Пароль')
    def test_create_user_without_password_shows_error(self):
        payload = {
            'email': faker.email(),
            'name': faker.name()
        }
        response = requests.post(Constants.URL_CREATE_USER, json=payload)
        assert response.status_code == 403 and response.json() == Constants.BODY_NO_FIELD