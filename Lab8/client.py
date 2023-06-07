import requests
import json

def register_user(login, password):
    url = 'http://127.0.0.1:5000/user/'

    data = {
        'login': login,
        'password': password
    }

    headers = {'Content-Type': 'application/json'}

    response = requests.post(url, data=json.dumps(data), headers=headers)

    if response.status_code == 201:
        print('User registered successfully')
    else:
        print('Registration failed:', response.text)

# Пример использования
login = input('Enter login: ')
password = input('Enter password: ')

register_user(login, password)
