import socket
import logging

def start_server(host, port):
    logging.basicConfig(filename='server.log', level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    logging.info("Запуск сервера")
    logging.info(f"Начало прослушивания порта {port}")

    running = True

    while running:
        client_socket, client_address = server_socket.accept()
        logging.info(f"Подключение клиента {client_address[0]}:{client_address[1]}")

        while True:
            data = client_socket.recv(1024)
            if not data:
                break

            logging.info(f"Прием данных от клиента {client_address[0]}:{client_address[1]}: {data.decode()}")

            client_socket.sendall(data)
            logging.info(f"Отправка данных клиенту {client_address[0]}:{client_address[1]}: {data.decode()}")

        logging.info(f"Отключение клиента {client_address[0]}:{client_address[1]}")
        client_socket.close()

    server_socket.close()
    logging.info("Остановка сервера")


def get_host_port():
    default_host = '127.0.0.1'
    default_port = 8000

    host = input(f"Введите имя хоста [{default_host}]: ") or default_host

    while True:
        try:
            port = int(input(f"Введите номер порта [{default_port}]: ") or default_port)
            break
        except ValueError:
            print("Ошибка: Некорректный номер порта.")

    return host, port


host, port = get_host_port()
start_server(host, port)
