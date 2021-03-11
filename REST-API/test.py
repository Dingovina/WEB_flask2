import requests

response = requests.get('http://127.0.0.1:5000/api/jobs/')
print(response.json())
response = requests.get('http://127.0.0.1:5000/api/jobs/1')
print(response.json())
response = requests.get('http://127.0.0.1:5000/api/jobs/-1')
print(response.json())
response = requests.get('http://127.0.0.1:5000/api/jobs/abc')
print(response.json())