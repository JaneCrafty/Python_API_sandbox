import pytest
import requests
from lib.base_case import BaseCase


class TestUserDelete(BaseCase):

    def test_delete_user_2(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response1 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        response2 = requests.delete("https://playground.learnqa.ru/api/user/2", headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid})
        assert response2.status_code == 400, f"Unexpected status code {response2.status_code}"

    def test_positive_delete_created_user(self):
        registration_data = self.user_data_provider()
        response1 = requests.post("https://playground.learnqa.ru/api/user/", data=registration_data)
        user_id = self.get_json_value(response1, "id")

        response2 = requests.post("https://playground.learnqa.ru/api/user/login", data={'email': registration_data['email'],
                                                         'password': registration_data['password']})
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        response3 = requests.delete(f"https://playground.learnqa.ru/api/user/{user_id}", headers={"x-csrf-token": token},
                                      cookies={"auth_sid": auth_sid})
        assert response3.status_code == 200, f"Unexpected status code {response3.status_code}"

        response4 = requests.get(f"https://playground.learnqa.ru/api/user/{user_id}")
        assert response4.status_code == 404, f"Unexpected status code {response4.status_code}"

    def test_delete_user_authorized_as_another_user(self):
        first_user_data = self.user_data_provider()
        response_first_user = requests.post("https://playground.learnqa.ru/api/user/", data=first_user_data)
        first_user_id = self.get_json_value(response_first_user, "id")

        second_user_data = self.user_data_provider()
        requests.post("https://playground.learnqa.ru/api/user/", data=second_user_data)

        response1 = requests.post("https://playground.learnqa.ru/api/user/login",
                                    data={'email': second_user_data['email'], 'password': second_user_data['password']})
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        response2 = requests.delete(f"https://playground.learnqa.ru/api/user/{first_user_id}",
                                      headers={"x-csrf-token": token},
                                      cookies={"auth_sid": auth_sid})

        assert response2.status_code == 400, f"Unexpected status code {response2.status_code}"
        response_check = requests.get(f"https://playground.learnqa.ru/api/user/{first_user_id}")
        assert response_check.status_code == 200, f"User was actually deleted! Status code: {response_check.status_code}"