import requests

url = "http://127.0.0.1:5000/items/1"
data = {"name": "Teloseen", "description": "Using to enhance Breathing"}

response = requests.post(url, json=data)

# response = requests.put(url, json=data)

# response = requests.delete(url)

print(response.json())
