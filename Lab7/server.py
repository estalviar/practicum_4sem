import os
import shutil
import socket
import logging


PORT = 12345

WORKING_DIRECTORY = "/path/to/working/directory"

# Создаем логгер и настраиваем его
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("file_manager_server")
logger.addHandler(logging.FileHandler("server.log"))

# Создаем сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("0.0.0.0", PORT))
server_socket.listen(1)

logger.info(f"Сервер запущен и прослушивает порт {PORT}...")

while True:
    # Принимаем подключение от клиента
    client_socket, client_address = server_socket.accept()
    logger.info(f"Установлено соединение с клиентом {client_address}")

    while True:
        # Получаем команду от клиента
        command = client_socket.recv(1024).decode()

        # Обработка команды
        if command == "LIST":
            # Получение списка файлов и папок в рабочей директории
            file_list = os.listdir(WORKING_DIRECTORY)
            file_list_str = "\n".join(file_list)
            client_socket.send(file_list_str.encode())
            logger.info(f"Отправлен список файлов и папок клиенту {client_address}")
        elif command == "CREATE_DIR":
            # Создание новой папки
            dir_name = client_socket.recv(1024).decode()
            dir_path = os.path.join(WORKING_DIRECTORY, dir_name)
            os.mkdir(dir_path)
            client_socket.send("OK".encode())
            logger.info(f"Создана новая папка {dir_name} для клиента {client_address}")
        elif command == "DELETE_DIR":
            # Удаление папки
            dir_name = client_socket.recv(1024).decode()
            dir_path = os.path.join(WORKING_DIRECTORY, dir_name)
            shutil.rmtree(dir_path)
            client_socket.send("OK".encode())
            logger.info(f"Удалена папка {dir_name} для клиента {client_address}")
        elif command == "CREATE_FILE":
            # Создание нового файла
            file_name = client_socket.recv(1024).decode()
            file_path = os.path.join(WORKING_DIRECTORY, file_name)
            file_content = client_socket.recv(1024).decode()
            with open(file_path, "w") as file:
                file.write(file_content)
            client_socket.send("OK".encode())
            logger.info(f"Создан новый файл {file_name} для клиента {client_address}")
        elif command == "COPY_FILE":
            # Копирование файла
            src_file_name = client_socket.recv(1024).decode()
            dst_file_name = client_socket.recv(1024).decode()
            src_file_path = os.path.join(WORKING_DIRECTORY, src_file_name)
            dst_file_path = os.path.join(WORKING_DIRECTORY, dst_file_name)
            shutil.copy2(src_file_path, dst_file_path)
            client_socket.send("OK".encode())
            logger.info(f"Скопирован файл {src_file_name} в {dst_file_name} для клиента {client_address}")
        elif command == "RENAME_FILE":
            # Переименование файла
            old_file_name = client_socket.recv(1024).decode()
            new_file_name = client_socket.recv(1024).decode()
            old_file_path = os.path.join(WORKING_DIRECTORY, old_file_name)
            new_file_path = os.path.join(WORKING_DIRECTORY, new_file_name)
            os.rename(old_file_path, new_file_path)
            client_socket.send("OK".encode())
            logger.info(f"Переименован файл {old_file_name} в {new_file_name} для клиента {client_address}")
        elif command == "GET_FILE_CONTENT":
            # Получение содержимого файла
            file_name = client_socket.recv(1024).decode()
            file_path = os.path.join(WORKING_DIRECTORY, file_name)
            with open(file_path, "r") as file:
                file_content = file.read()
            client_socket.send(file_content.encode())
            logger.info(f"Отправлено содержимое файла {file_name} клиенту {client_address}")
        elif command == "EXIT":
            # Закрытие соединения с клиентом
            client_socket.close()
            logger.info(f"Соединение с клиентом {client_address} закрыто")
            break

# Закрываем серверный сокет
server_socket.close()
