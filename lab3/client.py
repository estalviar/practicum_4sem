import socket

def send_receive_data(server_host, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((server_host, server_port))
    except ConnectionRefusedError:
        print("Ошибка: Невозможно подключиться к серверу.")
        return

    print(f"Соединение с сервером {server_host}:{server_port} установлено.")

    while True:
        try:
            message = input("Введите строку (для выхода введите 'exit'): ")
        except KeyboardInterrupt:
            print("\nЗавершение работы.")
            break

        if not message:
            continue

        if message == 'exit':
            break

        client_socket.sendall(message.encode())
        data = client_socket.recv(1024)
        print(f"Прием данных от сервера: {data.decode()}")

    client_socket.close()
    print(f"Разрыв соединения с сервером {server_host}:{server_port}")


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


server_host, server_port = get_host_port()
send_receive_data(server_host, server_port)
