import requests

response = requests.get('http://localhost:8000/api/currentTime')
print(response.json())