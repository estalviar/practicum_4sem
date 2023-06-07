import hashlib
import json
from datetime import datetime
from flask import Flask, request

app = Flask(__name__)

users = []

def save_users():
    with open('users_passwords.json', 'w') as file:
        json.dump(users, file)

def load_users():
    try:
        with open('users_passwords.json', 'r') as file:
            users.extend(json.load(file))
    except FileNotFoundError:
        pass

@app.route('/user/', methods=['POST'])
def register_user():
    data = request.get_json()
    if 'login' not in data or 'password' not in data:
        return 'Missing login or password', 400

    login = data['login']
    password = data['password']

    # Проверка, что пользователь с таким логином уже не зарегистрирован
    if any(user['login'] == login for user in users):
        return 'User already exists', 400

    # Хеширование пароля с солью
    salt = 'random_salt'  # Можно использовать случайную соль для каждого пользователя
    hashed_password = hashlib.sha256((password + salt).encode()).hexdigest()

    # Создание объекта пользователя
    user = {
        'login': login,
        'password': hashed_password,
        'registration_date': str(datetime.now())
    }

    users.append(user)
    save_users()
    return 'User registered successfully', 201

if __name__ == '__main__':
    load_users()
    app.run(debug=True)
