from http.server import BaseHTTPRequestHandler, HTTPServer
import os

# Задаем рабочую директорию сервера
directory = "/Users/idenisoff/Desktop/test6"

# Класс, обрабатывающий HTTP-запросы
class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Получаем путь запрашиваемого ресурса
            path = self.path

            if path == "/":
                # Если не указан ресурс, отдаем содержимое index.html
                path = "/index.html"

            # Строим полный путь к файлу
            full_path = os.path.join(directory, path[1:])

            # Проверяем, существует ли файл
            if os.path.exists(full_path):
                # Определяем тип содержимого файла
                content_type = self.get_content_type(full_path)

                # Отправляем успешный ответ с содержимым файла
                self.send_response(200)
                self.send_header("Content-type", content_type)
                self.end_headers()

                with open(full_path, "rb") as file:
                    self.wfile.write(file.read())
            else:
                # Отправляем ошибку 404, если файл не найден
                self.send_error(404, "File Not Found: {}".format(self.path))

        except Exception as e:
            # Отправляем ошибку сервера, если возникла ошибка
            self.send_error(500, str(e))

    def get_content_type(self, file_path):
        # Определяем тип содержимого файла на основе его расширения
        extension = os.path.splitext(file_path)[1].lower()

        if extension == ".html":
            return "text/html"
        elif extension == ".css":
            return "text/css"
        elif extension == ".jpg" or extension == ".jpeg":
            return "image/jpeg"
        elif extension == ".png":
            return "image/png"

        else:
            return "application/octet-stream"

    # Переопределяем метод log_message для отключения вывода логов в консоль
    def log_message(self, format, *args):
        return

# Задаем настройки сервера
host = ""
port = 80

# Создаем объект HTTP-сервера с указанными настройками и обработчиком запросов
server = HTTPServer((host, port), RequestHandler)

print(f"Сервер запущен на порту {port}")
print(f"Рабочая директория: {directory}")

# Запускаем сервер
server.serve_forever()
