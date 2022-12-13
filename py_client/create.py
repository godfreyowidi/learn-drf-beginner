import requests

headers = { "Authorization": 'Bearer deaf927ed0fba21b668c3f40a601b8010a6320c4'}
endpoint = "http://localhost:8000/api/products/"

data = {
  "title": "this is a test field",
  "price": 11.05
}
get_response = requests.post(endpoint, json=data, headers=headers)

print(get_response.json())


