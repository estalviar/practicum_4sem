import socket

# Определите IP-адрес и порт сервера
SERVER_IP = "127.0.0.1"
SERVER_PORT = 12345

# Создаем сокет
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))

while True:
    # Выводим доступные команды
    print("Доступные команды:")
    print("LIST - Получить список файлов и папок в рабочей директории сервера")
    print("CREATE_DIR - Создать новую папку")
    print("DELETE_DIR - Удалить папку")
    print("CREATE_FILE - Создать новый файл")
    print("COPY_FILE - Скопировать файл")
    print("RENAME_FILE - Переименовать файл")
    print("GET_FILE_CONTENT - Получить содержимое файла")
    print("EXIT - Выйти из программы")

    # Запрос команды от пользователя
    command = input("Введите команду: ").upper()

    # Отправляем команду на сервер
    client_socket.send(command.encode())

    # Обработка команды
    if command == "LIST":
        # Получаем список файлов и папок
        file_list = client_socket.recv(1024).decode()
        print("Список файлов и папок:")
        print(file_list)
    elif command == "CREATE_DIR":
        # Запрашиваем имя новой папки
        dir_name = input("Введите имя новой папки: ")
        client_socket.send(dir_name.encode())
        response = client_socket.recv(1024).decode()
        print(response)
    elif command == "DELETE_DIR":
        # Запрашиваем имя папки для удаления
        dir_name = input("Введите имя папки для удаления: ")
        client_socket.send(dir_name.encode())
        response = client_socket.recv(1024).decode()
        print(response)
    elif command == "CREATE_FILE":
        # Запрашиваем имя и содержимое нового файла
        file_name = input("Введите имя нового файла: ")
        file_content = input("Введите содержимое нового файла: ")
        client_socket.send(file_name.encode())
        client_socket.send(file_content.encode())
        response = client_socket.recv(1024).decode()
        print(response)
    elif command == "COPY_FILE":
        # Запрашиваем имя существующего файла и имя нового файла
        src_file_name = input("Введите имя существующего файла: ")
        dst_file_name = input("Введите имя нового файла: ")
        client_socket.send(src_file_name.encode())
        client_socket.send(dst_file_name.encode())
        response = client_socket.recv(1024).decode()
        print(response)
    elif command == "RENAME_FILE":
        # Запрашиваем имя существующего файла и новое имя файла
        old_file_name = input("Введите имя существующего файла: ")
        new_file_name = input("Введите новое имя файла: ")
        client_socket.send(old_file_name.encode())
        client_socket.send(new_file_name.encode())
        response = client_socket.recv(1024).decode()
        print(response)
    elif command == "GET_FILE_CONTENT":
        # Запрашиваем имя файла для получения содержимого
        file_name = input("Введите имя файла: ")
        client_socket.send(file_name.encode())
        file_content = client_socket.recv(1024).decode()
        print(f"Содержимое файла {file_name}:")
        print(file_content)
    elif command == "EXIT":
        # Закрываем соединение с сервером и выходим из программы
        client_socket.close()
        print("Соединение с сервером закрыто")
        break
    else:
        print("Неверная команда. Попробуйте снова.")
