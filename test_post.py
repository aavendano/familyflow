import requests

url = "http://localhost:8000/api/families/1/groceries/"
data = {"name": "Bananas"}

print(f"Making POST to {url} with {data}")
response = requests.post(url, json=data)
print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")
