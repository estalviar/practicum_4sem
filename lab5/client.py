import socket
import random

def power(base, exponent, mod):
    result = 1
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exponent //= 2
    return result

def save_keys(public_key, private_key):
    with open("client_keys.txt", "w") as file:
        file.write(f"Public Key: {public_key}\nPrivate Key: {private_key}")

def load_keys():
    with open("client_keys.txt", "r") as file:
        lines = file.readlines()
        public_key = int(lines[0].split(":")[1].strip())
        private_key = int(lines[1].split(":")[1].strip())
        return public_key, private_key

def encrypt_message(message, key):
    encrypted_message = ""
    for char in message:
        encrypted_char = chr(ord(char) ^ key)
        encrypted_message += encrypted_char
    return encrypted_message

def decrypt_message(encrypted_message, key):
    decrypted_message = ""
    for char in encrypted_message:
        decrypted_char = chr(ord(char) ^ key)
        decrypted_message += decrypted_char
    return decrypted_message

def generate_keys():
    private_key = random.randint(1, 100)
    public_key = power(5, private_key, 97)
    save_keys(public_key, private_key)
    return public_key, private_key

def diffie_hellman_client():
    # Создание сокета
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_host = 'localhost'
    server_port = 12345

    # Подключение к серверу
    client_socket.connect((server_host, server_port))
    print("Подключение установлено!")

    # Загрузка ключей из файла (если существуют) или их генерация
    try:
        public_key, private_key = load_keys()
        print("Загружены существующие ключи.")
    except FileNotFoundError:
        public_key, private_key = generate_keys()
        print("Сгенерированы и сохранены новые ключи.")

    # Отправка серверу публичного ключа
    client_socket.send(str(public_key).encode())

    # Получение от сервера его публичного ключа
    server_public_key = int(client_socket.recv(1024).decode())

    # Вычисление общего секретного ключа
    shared_secret = power(server_public_key, private_key, 97)

    print("Серверный публичный ключ:", server_public_key)
    print("Общий секретный ключ:", shared_secret)

    return client_socket, shared_secret

def run_client():
    client_socket, shared_secret = diffie_hellman_client()

    while True:
        # Чтение сообщения от пользователя
        message = input("Введите сообщение (или 'q' для выхода): ")
        if message == 'q':
            break

        # Шифрование сообщения
        encrypted_message = encrypt_message(message, shared_secret)

        # Отправка зашифрованного сообщения серверу
        client_socket.send(encrypted_message.encode())

        # Получение и расшифровка ответа от сервера
        response = client_socket.recv(1024).decode()
        decrypted_response = decrypt_message(response, shared_secret)
        print("Получено ответное сообщение от сервера:", decrypted_response)

    # Закрытие соединения
    client_socket.close()

run_client()
