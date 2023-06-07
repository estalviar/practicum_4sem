import socket
import threading

class ChatClient:
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 8000
        self.client_socket = None

    def start(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))
        print('Подключено к серверу {}:{}'.format(self.host, self.port))

        username = input('Введите ваше имя: ')
        self.client_socket.send(username.encode())

        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()

        self.send_messages()

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode()
                print(message)
            except Exception as e:
                print('Ошибка приема сообщений:', str(e))
                break

    def send_messages(self):
        while True:
            try:
                message = input()
                self.client_socket.send(message.encode())
                if message == '/quit':
                    break
            except Exception as e:
                print('Ошибка отправки сообщения:', str(e))
                break

        self.client_socket.close()

chat_client = ChatClient()
chat_client.start()
