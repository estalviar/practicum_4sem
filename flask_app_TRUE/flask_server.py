import binascii
import hashlib
import json
import os
from datetime import datetime
from hashlib import sha256
from flask import Flask, request, abort, jsonify


app = Flask(__name__)


def load():
    with open('auth.json', 'r', encoding='utf-8') as file:
        return list(json.load(file))


def dump(auth):
    with open('auth.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(auth))


def checkLogin(login):
    global users
    return login in [user['login'] for user in users]


def makeResponse(result=True, description=''):
    return {'result': result,
            'description': description}


def hashPassword(password, salt: str = None):
    if salt:
        salt = salt.encode('ascii')
        newPassword = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 80000)
        newPassword = binascii.hexlify(newPassword)
        return (salt + newPassword).decode('ascii')
    else:
        salt = sha256(os.urandom(70)).hexdigest().encode('ascii')
        newPassword = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 80000)
        newPassword = binascii.hexlify(newPassword)
        return (salt + newPassword).decode('ascii'), salt.decode('ascii')


def regUser(user):
    global users
    password, salt = hashPassword(user['password'])
    newUser = {'login': user['login'],
               'password': password,
               'salt': salt,
               'date': datetime.now().isoformat()}
    users.append(newUser)
    dump(users)
    return makeResponse(True, 'пользователь был зарегистрирован в системе'), 201


def checkPassword(user):
    global users
    login = user['login']
    password = user['password']
    try:
        checkedUser = list(filter(lambda x: x['login'] == login, users))[0]
        checkedPassword = checkedUser['password']
        checkedSalt = checkedUser['salt']
        newPassword = hashPassword(password, checkedSalt)
        return checkedPassword == newPassword
    except IndexError:
        return False


@app.route('/user/reg', methods=['POST'])
def regUsers():
    user = json.loads(request.get_data())
    if checkLogin(user['login']):
        return makeResponse(False, 'этот логин уже был зарегистрирован')
    else:
        return regUser(user)


@app.route('/user/<string:username>', methods=['GET'])
def getUser(username):
    try:
        global users
        user = list(filter(lambda x: x['login'] == username, users))[0]
        print('print1 ', user)
        return jsonify({'users': user})
    except IndexError:
        abort(404)


@app.route('/users', methods=['GET', 'POST'])
def authUser():
    global users
    match request.method:
        case 'GET':
            return jsonify({'users': users})
        case 'POST':
            match checkLogin(json.loads(request.get_data())['login']), checkPassword(json.loads(request.get_data())):
                case True, True:
                    return makeResponse(True, 'авторизация прошла успешно')
                case True, False:
                    return makeResponse(False, 'некорректный пароль')
                case False, _:
                    return makeResponse(True, 'некорректное имя пользователя')


@app.route('/')
def user_data():
    return 'система регистрации пользователей'


users = load()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
