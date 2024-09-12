import allure
import requests
from data import Constants
from faker import Faker

faker = Faker()


class TestChangeUserData():
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

    @allure.title('Проверка успешного изменения имени пользователя')
    def test_change_user_name_success(self):
        payload = {
            'email': self.user_data['email'],
            'password': self.user_data['password'],
            'name': faker.name()
        }
        headers = {
            'Authorization': f"Bearer {self.token}"
        }
        response = requests.patch(Constants.URL_CHANGE_USER, json=payload, headers=headers)

        assert response.status_code == 200 and response.json()['success'] == True

    @allure.title('Проверка успешного изменения пароля пользователя')
    def test_change_user_password_success(self):
        payload = {
            'email': self.user_data['email'],
            'password': faker.password(),
            'name': self.user_data['name']
        }
        headers = {
            'Authorization': f"Bearer {self.token}"
        }
        response = requests.patch(Constants.URL_CHANGE_USER, json=payload, headers=headers)

        assert response.status_code == 200 and response.json()['success'] == True

    @allure.title('Проверка успешного изменения почты пользователя')
    def test_change_user_email_success(self):
        payload = {
            'email': faker.email(),
            'password': self.user_data['password'],
            'name': self.user_data['name']
        }
        headers = {
            'Authorization': f"Bearer {self.token}"
        }
        response = requests.patch(Constants.URL_CHANGE_USER, json=payload, headers=headers)

        assert response.status_code == 200 and response.json()['success'] == True

    @allure.title('Проверка появления ошибки при смене имени пользователя без авторизации')
    def test_change_user_name_without_auth_shows_error(self):
        payload = {
            'email': self.user_data['email'],
            'password': self.user_data['password'],
            'name': faker.name()
        }
        response = requests.patch(Constants.URL_CHANGE_USER, json=payload)

        assert response.status_code == 401 and response.json() == Constants.BODY_NOT_AUTH

    @allure.title('Проверка появления ошибки при смене пароля пользователя без авторизации')
    def test_change_user_password_without_auth_shows_error(self):
        payload = {
            'email': self.user_data['email'],
            'password': faker.password(),
            'name': self.user_data['name']
        }
        response = requests.patch(Constants.URL_CHANGE_USER, json=payload)

        assert response.status_code == 401 and response.json() == Constants.BODY_NOT_AUTH

    @allure.title('Проверка появления ошибки при смене почты пользователя без авторизации')
    def test_change_user_email_without_auth_shows_error(self):
        payload = {
            'email': faker.email(),
            'password': self.user_data['password'],
            'name': self.user_data['name']
        }
        response = requests.patch(Constants.URL_CHANGE_USER, json=payload)

        assert response.status_code == 401 and response.json() == Constants.BODY_NOT_AUTH
