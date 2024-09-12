import allure
import requests
from data import Constants
from faker import Faker

faker = Faker()

class TestLoginUser:
    token = None

    @classmethod
    def setup_class(cls):
        cls.user_data = {
            'email': faker.email(),
            'password': faker.password(),
            'name': faker.name()
        }
        requests.post(Constants.URL_CREATE_USER, json=cls.user_data)

    @classmethod
    def teardown_class(cls):
        if cls.token:
            headers = {
                'Authorization': cls.token
            }
            requests.delete(Constants.URL_CHANGE_USER, headers=headers)

    @allure.title('Проверка успешной авторизации пользователя')
    def test_login_user_success(self):
        payload = {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }
        response = requests.post(Constants.URL_LOGIN_USER, json=payload)
        assert response.status_code == 200 and response.json().get('accessToken') is not None

    @allure.title('Проверка появления ошибки при авторизации под несуществующим пользователем')
    def test_login_wrong_data_shows_error(self):
        payload = {
            'email': 'wrong_email',
            'password': 'wrong_password'
        }
        response = requests.post(Constants.URL_LOGIN_USER, json=payload)
        assert response.status_code == 401 and response.json() == Constants.BODY_WRONG_DATA
