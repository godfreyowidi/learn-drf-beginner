import requests

# endpoint = "http://httpbin.org/anything"
endpoint = "http://localhost:8000/api/"

get_response = requests.post(endpoint, json={"title": "ABC123", "content": "Hello world again"})
# print(get_response.json())
# print(get_response.headers)
# print(get_response.text)
# print(get_response.status_code)

print(get_response.json())


