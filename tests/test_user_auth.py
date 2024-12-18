from lib.my_requests import MyRequests
import pytest
import allure


from lib.base_case import BaseCase
from lib.assertions import Assertions

@allure.epic("User Authentication Tests")
class TestUserAuth(BaseCase):
    exclude_params = [
        "no_cookie",
        "no_token"
    ]

    @allure.step("Setting up user authentication and necessary tokens and cookies")
    def setup_method(self):
        data = {
            'email': 'vinkotov@example.com',
            'password':'1234'
        }
        response1 = MyRequests.post("/user/login", data = data)

        self.auth_sid = self.get_cookie(response1, "auth_sid")
        self.token = self.get_header(response1, "x-csrf-token")
        self.user_id_from_auth_method = self.get_json_value(response1, "user_id")

    @allure.description("This test successfully authorize user by email and password")
    @allure.severity("High")
    def test_authUser(self):

        response2 = MyRequests.get(
            "/user/auth",
            headers={"x-csrf-token" : self.token},
            cookies={"auth_sid" : self.auth_sid}
        )

        Assertions.assert_json_value_by_name(
            response2,
            "user_id",
            self.user_id_from_auth_method,
            "User ids are not equal"
        )

    @allure.description("This test check authorization status w/o sending auth cookie or token")
    @pytest.mark.parametrize('condition', exclude_params)
    def test_negativeAuthUser(self, condition):

        if condition == "no_cookie":
            response2 = MyRequests.get(
                "/user/auth",
                headers={"x-csrf-token": self.token}
            )
        else:
            response2 = MyRequests.get(
                "/user/auth",
                cookies={"auth_sid": self.auth_sid}
            )

        Assertions.assert_json_value_by_name(
            response2,
            "user_id",
            0,
            f"User is authorized with condition {condition}"
        )
