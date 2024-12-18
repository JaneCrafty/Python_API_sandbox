from datetime import datetime

import requests
import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import allure

@allure.epic("User Registration Tests")
class TestUserRegister(BaseCase):

    def setup_method(self):
        base_part = "learnqa"
        domain = "example.com"
        random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        self.email = f"{base_part}{random_part}@{domain}"

    @allure.story("Successful user creation")
    def test_create_user_successfully(self):
        data = self.user_data_provider()
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    @allure.story("User registration with an already existing email")
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'

        data = {
            'password': '1234',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }

        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.text == f"Users with email '{email}' already exists", \
            f"Unexpected response content {response.content}"

    @allure.story("User registration with an incorrect email w/o '@'")
    def test_create_user_with_invalid_email(self):
        data = self.user_data_provider(email="testemail.com")
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)

    @allure.story("User registration without one of the fields")
    @pytest.mark.parametrize('field', ['username', 'password', 'email', 'firstName', 'lastName'])
    def test_create_user_without_field(self, field):
        data = self.user_data_provider()
        data.pop(field)
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)

    @allure.story("User registration with a very short name")
    def test_create_user_with_short_name(self):
        data = self.user_data_provider(firstName="A")
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)

    @allure.story("User registration with a very long name")
    def test_create_user_with_long_name(self):
        name = "A" * 251
        data = self.user_data_provider(firstName=name)
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)