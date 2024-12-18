import pytest
import requests

from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserEdit(BaseCase):

    def test_edit_just_created_user(self):
        register_data = self.user_data_provider()
        response1 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        login_data = {
            'email': email,
            'password': password
        }

        response2 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        new_name = "Changed Name"

        response3 = requests.put(f"https://playground.learnqa.ru/api/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid},
                                   data={"firstName": new_name}
                                   )
        Assertions.assert_code_status(response3, 200)

        response4 = requests.get(f"https://playground.learnqa.ru/api/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid}
                                   )
        Assertions.assert_json_value_by_name(response4,
                                             "firstName",
                                             new_name,
                                             "Wrong name of the user after edit"
                                             )

    def test_edit_user_unauthorized(self):

        register_data = self.user_data_provider()
        response1 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)
        user_id = self.get_json_value(response1, "id")
        new_name = "Changed Name Unauth"

        response2 = requests.put(f"https://playground.learnqa.ru/api/user/{user_id}", data={"firstName": new_name})
        Assertions.assert_code_status(response2, 400)
        response_json = response2.json()
        assert response_json.get("error") == "Auth token not supplied", \
            f"Unexpected response content {response2.content.decode('utf-8')}"

    @pytest.mark.xfail(reason="Unauthorized edit had been allowed by API")
    def test_edit_user_authorized_as_another_user(self):
        first_user_data = self.user_data_provider()
        response1 = requests.post("https://playground.learnqa.ru/api/user/", data=first_user_data)
        first_user_id = self.get_json_value(response1, "id")

        second_user_data = self.user_data_provider()
        requests.post("https://playground.learnqa.ru/api/user/", data=second_user_data)
        login_data = {
            'email': second_user_data['email'],
            'password': second_user_data['password']
        }
        response3 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)
        auth_sid = self.get_cookie(response3, "auth_sid")
        token = self.get_header(response3, "x-csrf-token")

        new_name = "Changed Name By Another User"
        response4 = requests.put(f"https://playground.learnqa.ru/api/user/{first_user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid},
                                   data={"firstName": new_name}
                                   )

        Assertions.assert_code_status(response4, 400)

        response5 = requests.get(f"https://playground.learnqa.ru/api/user/{first_user_id}")
        Assertions.assert_json_value_by_name(response5, "firstName", first_user_data['firstName'],
                                             "Name of the first user was changed.")

    def test_edit_user_invalid_email(self):
        user_data = self.user_data_provider()
        response1 = requests.post("https://playground.learnqa.ru/api/user/", data=user_data)
        user_id = self.get_json_value(response1, "id")
        login_data = {
            'email': user_data['email'],
            'password': user_data['password']
        }
        response2 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        invalid_email = "invalidemail.com"
        response3 = requests.put(f"https://playground.learnqa.ru/api/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid},
                                   data={"email": invalid_email}
                                   )
        Assertions.assert_code_status(response3, 400)

    def test_edit_user_short_first_name(self):
        user_data = self.user_data_provider()
        response1 = requests.post("https://playground.learnqa.ru/api/user/", data=user_data)
        user_id = self.get_json_value(response1, "id")
        login_data = {
            'email': user_data['email'],
            'password': user_data['password']
        }
        response2 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        short_name = "A"
        response3 = requests.put(f"https://playground.learnqa.ru/api/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid},
                                   data={"firstName": short_name}
                                   )
        Assertions.assert_code_status(response3, 400)