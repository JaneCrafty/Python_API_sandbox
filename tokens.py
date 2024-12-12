import requests
import time

url = "https://playground.learnqa.ru/ajax/api/longtime_job"

# Создание задачи, переменных и вывод необходимых данных
response_create = requests.get(url)
response_create_data = response_create.json()

if "token" not in response_create_data or "seconds" not in response_create_data:
    raise Exception("Некорректный ответ при создании задачи")

token = response_create_data["token"]
wait_time = response_create_data["seconds"]
print(f"Задача создана. Токен: {token}, ожидание: {wait_time} секунд")

# Запрос с token до завершения задачи
response_check_before = requests.get(url, params={"token": token})
response_check_before_data = response_check_before.json()

if response_check_before_data.get("status") != "Job is NOT ready":
    raise Exception("Некорректный статус до завершения задачи")

print("Статус до завершения задачи: Job is NOT ready")

# Ожидание отработки задачи в секундах
print(f"Ждем {wait_time} секунд...")
time.sleep(wait_time)

# Запрос с token после завершения задачи
response_check_after = requests.get(url, params={"token": token})
response_check_after_data = response_check_after.json()

if response_check_after_data.get("status") != "Job is ready":
    raise Exception("Некорректный статус после завершения задачи")

if "result" not in response_check_after_data:
    raise Exception("Результат отсутствует в ответе после завершения задачи")

# Вывод результатов
print("Статус после завершения задачи: Job is ready")
print(f"Результат: {response_check_after_data['result']}")
