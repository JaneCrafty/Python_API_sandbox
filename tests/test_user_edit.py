import pytest
import requests

from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import allure

@allure.epic("User Edition Tests")
class TestUserEdit(BaseCase):

    @allure.story("Ability to edit a user after registration")
    def test_edit_just_created_user(self):
        register_data = self.user_data_provider()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        login_data = {
            'email': email,
            'password': password
        }

        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        new_name = "Changed Name"

        response3 = MyRequests.put(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid},
                                   data={"firstName": new_name}
                                   )
        Assertions.assert_code_status(response3, 200)

        response4 = MyRequests.get(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid}
                                   )
        Assertions.assert_json_value_by_name(response4,
                                             "firstName",
                                             new_name,
                                             "Wrong name of the user after edit"
                                             )
    @allure.story("Inability to edit user's data when unauthorized")
    def test_edit_user_unauthorized(self):

        register_data = self.user_data_provider()
        response1 = MyRequests.post("/user/", data=register_data)
        user_id = self.get_json_value(response1, "id")
        new_name = "Changed Name Unauth"

        response2 = MyRequests.put(f"/user/{user_id}", data={"firstName": new_name})
        Assertions.assert_code_status(response2, 400)
        response_json = response2.json()
        assert response_json.get("error") == "Auth token not supplied", \
            f"Unexpected response content {response2.content.decode('utf-8')}"

    @allure.story("Inability to edit a user when authorized as another user")
    @pytest.mark.xfail(reason="Unauthorized edit had been allowed by API")
    def test_edit_user_authorized_as_another_user(self):
        first_user_data = self.user_data_provider()
        response1 = MyRequests.post("/user/", data=first_user_data)
        first_user_id = self.get_json_value(response1, "id")

        second_user_data = self.user_data_provider()
        MyRequests.post("/user/", data=second_user_data)
        login_data = {
            'email': second_user_data['email'],
            'password': second_user_data['password']
        }
        response3 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response3, "auth_sid")
        token = self.get_header(response3, "x-csrf-token")

        new_name = "Changed Name By Another User"
        response4 = MyRequests.put(f"/user/{first_user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid},
                                   data={"firstName": new_name}
                                   )

        Assertions.assert_code_status(response4, 400)

        response5 = MyRequests.get(f"/user/{first_user_id}")
        Assertions.assert_json_value_by_name(response5, "firstName", first_user_data['firstName'],
                                             "Name of the first user was changed.")

    @allure.story("Inability to change user email to an invalid one")
    def test_edit_user_invalid_email(self):
        user_data = self.user_data_provider()
        response1 = MyRequests.post("/user/", data=user_data)
        user_id = self.get_json_value(response1, "id")
        login_data = {
            'email': user_data['email'],
            'password': user_data['password']
        }
        response2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        invalid_email = "invalidemail.com"
        response3 = MyRequests.put(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid},
                                   data={"email": invalid_email}
                                   )
        Assertions.assert_code_status(response3, 400)

    @allure.story("Inability to change user first name to a very short value")
    def test_edit_user_short_first_name(self):
        user_data = self.user_data_provider()
        response1 = MyRequests.post("/user/", data=user_data)
        user_id = self.get_json_value(response1, "id")
        login_data = {
            'email': user_data['email'],
            'password': user_data['password']
        }
        response2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        short_name = "A"
        response3 = MyRequests.put(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid},
                                   data={"firstName": short_name}
                                   )
        Assertions.assert_code_status(response3, 400)