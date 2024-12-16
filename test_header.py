import requests

def test_header():
    url = "https://playground.learnqa.ru/api/homework_header"
    response = requests.get(url)
    headers = response.headers

    # Проверяем, что headers не пусты
    assert len(headers) > 0, "Ответ не содержит headers"

    # Печатаем все headers
    for header_name, header_value in headers.items():
        print(f"Header: {header_name} = {header_value}")

    # Проверяем полученный header
    expected_header_name = "x-secret-homework-header"
    expected_header_value = "Some secret value"

    assert expected_header_name in headers, f"Header {expected_header_name} отсутствует в ответе"
    assert headers[expected_header_name] == expected_header_value, (
        f"Значение header {expected_header_name} отличается от ожидаемого: {headers[expected_header_name]}"
    )
