import requests

def test_cookie():
    url = "https://playground.learnqa.ru/api/homework_cookie"
    response = requests.get(url)
    cookies = response.cookies

    # Проверяем, что хотя бы одна cookie пришла в ответе
    assert len(cookies) > 0, "Ответ не содержит cookies"

    # Печатаем все cookies
    for cookie_name, cookie_value in cookies.items():
        print(f"Cookie: {cookie_name} = {cookie_value}")

    # Проверяем найденную cookie
    expected_cookie_name = "HomeWork"
    expected_cookie_value = "hw_value"

    assert expected_cookie_name in cookies, f"Cookie {expected_cookie_name} отсутствует в ответе"
    assert cookies[expected_cookie_name] == expected_cookie_value, (
        f"Значение cookie {expected_cookie_name} отличается от ожидаемого: {cookies[expected_cookie_name]}"
    )
