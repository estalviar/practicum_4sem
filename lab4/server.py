import socket
import threading
import sys

class ChatServer:
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 8000
        self.server_socket = None
        self.clients = {}  # Словарь для хранения подключенных клиентов и их адресов
        self.messages = []  # Список для хранения истории сообщений
        self.running = True
        self.paused = False

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print('Сервер запущен на {}:{}'.format(self.host, self.port))

        control_thread = threading.Thread(target=self.handle_control_commands)
        control_thread.start()

        while self.running:
            if not self.paused:
                client_socket, client_address = self.server_socket.accept()
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
                client_thread.start()

        self.server_socket.close()

    def handle_control_commands(self):
        while True:
            command = input('Введите команду (stop, pause, logs, clear_logs, clear_auth): ')
            if command == 'stop':
                self.stop_server()
                break
            elif command == 'pause':
                self.pause_server()
            elif command == 'logs':
                self.show_logs()
            elif command == 'clear_logs':
                self.clear_logs()
            elif command == 'clear_auth':
                self.clear_auth_file()
            else:
                print('Неверная команда.')

    def stop_server(self):
        self.running = False

    def pause_server(self):
        self.paused = not self.paused
        if self.paused:
            print('Сервер приостановлен.')
        else:
            print('Сервер возобновил работу.')

    def show_logs(self):
        print('История сообщений:')
        for message in self.messages:
            print('{}: {}'.format(message[0], message[1]))

    def clear_logs(self):
        self.messages = []
        print('История сообщений очищена.')

    def clear_auth_file(self):
        with open('auth.txt', 'w') as f:
            f.write('')
        print('Файл идентификации очищен.')

    def handle_client(self, client_socket, client_address):
        username = self.authenticate(client_socket)
        if username is None:
            return

        self.clients[client_socket] = username
        print('Новое подключение от {}: {}'.format(client_address, username))

        self.send_history(client_socket)
        self.broadcast_message('{} присоединился к чату.'.format(username))

        while True:
            message = client_socket.recv(1024).decode().strip()
            if message == '/quit':
                break
            self.messages.append((username, message))
            self.broadcast_message('{}: {}'.format(username, message))

        self.remove_client(client_socket)
        client_socket.close()

    def authenticate(self, client_socket):
        client_socket.send('Введите ваше имя: '.encode())
        username = client_socket.recv(1024).decode().strip()
        if not self.is_valid_username(username):
            client_socket.send('Неверное имя пользователя. Пожалуйста, выберите другое имя.'.encode())
            client_socket.close()
            return None
        return username

    def is_valid_username(self, username):
        if not username:
            return False
        for client_username in self.clients.values():
            if client_username == username:
                return False
        return True

    def send_history(self, client_socket):
        if self.messages:
            history = 'Последние сообщения:\n'
            for message in self.messages:
                history += '{}: {}\n'.format(message[0], message[1])
            client_socket.send(history.encode())

    def broadcast_message(self, message):
        for client_socket in self.clients:
            client_socket.send(message.encode())

    def remove_client(self, client_socket):
        if client_socket in self.clients:
            username = self.clients[client_socket]
            del self.clients[client_socket]
            self.broadcast_message('{} покинул чат.'.format(username))

chat_server = ChatServer()
chat_server.start()
