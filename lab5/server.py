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
    with open("server_keys.txt", "w") as file:
        file.write(f"Public Key: {public_key}\nPrivate Key: {private_key}")

def load_keys():
    with open("server_keys.txt", "r") as file:
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

def diffie_hellman_server():
    # Создание сокета
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_host = 'localhost'
    server_port = 12345

    # Привязка сокета к адресу и порту
    server_socket.bind((server_host, server_port))

    # Ожидание подключения клиента
    server_socket.listen(1)
    print("Ожидание подключения клиента...")

    # Принятие подключения
    client_socket, address = server_socket.accept()
    print("Подключение установлено!")

    # Загрузка ключей из файла (если существуют) или их генерация
    try:
        public_key, private_key = load_keys()
        print("Загружены существующие ключи.")
    except FileNotFoundError:
        public_key, private_key = generate_keys()
        print("Сгенерированы и сохранены новые ключи.")

    # Получение от клиента его публичного ключа
    client_public_key = int(client_socket.recv(1024).decode())

    # Вычисление общего секретного ключа
    shared_secret = power(client_public_key, private_key, 97)

    # Отправка серверу публичного ключа
    client_socket.send(str(public_key).encode())

    print("Серверный публичный ключ:", public_key)
    print("Общий секретный ключ:", shared_secret)

    return client_socket, shared_secret

def run_server():
    client_socket, shared_secret = diffie_hellman_server()

    while True:
        # Получение зашифрованного сообщения от клиента
        encrypted_message = client_socket.recv(1024).decode()
        if not encrypted_message:
            break

        # Расшифровка сообщения
        decrypted_message = decrypt_message(encrypted_message, shared_secret)
        print("Получено сообщение от клиента:", decrypted_message)

        # Шифрование и отправка ответа клиенту
        response = encrypt_message(decrypted_message, shared_secret)
        client_socket.send(response.encode())

    # Закрытие соединения
    client_socket.close()
    server_socket.close()

run_server()
