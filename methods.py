import requests

url = "https://playground.learnqa.ru/ajax/api/compare_query_type"

# 1. HTTP-запрос без параметра method
response = requests.get(url)
print(f"1. GET-запрос без параметра method: {response.text}")

# 2. HTTP-запрос с методом не из списка (HEAD)
response = requests.head(url)
print(f"2. HEAD-запрос: Status Code {response.status_code}, Content: {response.text}")

# 3. HTTP-запрос с правильным значением method
methods = ["GET", "POST", "PUT", "DELETE"]
for method in methods:
    if method == "GET":
        response = requests.get(url, params={"method": method})
    else:
        response = requests.request(method, url, data={"method": method})
    print(f"3. {method}-запрос с параметром method={method}: {response.text}")

# 4. Проверка всех сочетаний реальных запросов и значений параметра method
for actual_method in methods:
    for param_method in methods:
        if actual_method == "GET":
            response = requests.get(url, params={"method": param_method})
        else:
            response = requests.request(actual_method, url, data={"method": param_method})
        print(
            f"4. {actual_method}-запрос с параметром method={param_method}: "
            f"Status Code {response.status_code}, Response: {response.text}"
        )
