import requests

url = "https://playground.learnqa.ru/api/long_redirect"
response = requests.get(url, allow_redirects=True)
redirects = response.history

redirect_count = len(redirects)
print(f"Количество редиректов: {redirect_count}")

for i, redirect in enumerate(redirects):
    print(f"Redirect {i + 1}: {redirect.url}")

final_url = response.url
print(f"Итоговый URL: {final_url}")
