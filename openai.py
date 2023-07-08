import requests

headers = {
    'Content-Type': 'application/json',
}

json_data = {
    'model': 'gpt-4',
    'messages': [
        {
            'role': 'user',
            'content': 'Hello, how are you?',
        },
    ],
}

response = requests.post('http://127.0.0.1:8080/v1/', headers=headers, json=json_data)

print(response.json())