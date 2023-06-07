import os
import shutil
from settings import WORKING_DIRECTORY

def print_menu():
    print("Примитивный файловый менеджер")
    print("1. Просмотреть содержимое текущей папки")
    print("2. Создать новую папку")
    print("3. Создать новый файл")
    print("4. Записать текст в файл")
    print("5. Просмотреть содержимое текстового файла")
    print("6. Удалить файл по имени")
    print("7. Удалить папку")
    print("8. Копировать файлы из одной папки в другую")
    print("9. Переместить файл")
    print("10. Переименовать файл")
    print("11. Перейти в папку")
    print("12. Выйти из программы")

def list_files():
    files = os.listdir(WORKING_DIRECTORY)
    for file in files:
        print(file)

def create_folder():
    folder_name = input("Введите название новой папки: ")
    folder_path = os.path.join(WORKING_DIRECTORY, folder_name)
    try:
        os.mkdir(folder_path)
        print(f"Папка '{folder_name}' успешно создана.")
    except FileExistsError:
        print(f"Папка '{folder_name}' уже существует.")

def create_file():
    file_name = input("Введите название нового файла: ")
    file_path = os.path.join(WORKING_DIRECTORY, file_name)
    try:
        with open(file_path, 'w') as file:
            print(f"Файл '{file_name}' успешно создан.")
    except FileExistsError:
        print(f"Файл '{file_name}' уже существует.")

def write_to_file():
    file_name = input("Введите название файла для записи текста: ")
    file_path = os.path.join(WORKING_DIRECTORY, file_name)
    if os.path.isfile(file_path):
        text = input("Введите текст для записи в файл: ")
        with open(file_path, 'w') as file:
            file.write(text)
        print(f"Текст успешно записан в файл '{file_name}'.")
    else:
        print(f"Файл '{file_name}' не найден.")

def view_file_content():
    file_name = input("Введите название текстового файла для просмотра содержимого: ")
    file_path = os.path.join(WORKING_DIRECTORY, file_name)
    if os.path.isfile(file_path):
        with open(file_path, 'r') as file:
            content = file.read()
            print(f"Содержимое файла '{file_name}':")
            print(content)
    else:
        print(f"Файл '{file_name}' не найден.")

def delete_file():
    file_name = input("Введите название файла для удаления: ")
    file_path = os.path.join(WORKING_DIRECTORY, file_name)
    if os.path.isfile(file_path):
        os.remove(file_path)
        print(f"Файл '{file_name}' успешно удален.")
    else:
        print(f"Файл '{file_name}' не найден.")

def delete_folder():
    folder_name = input("Введите название папки для удаления: ")
    folder_path = os.path.join(WORKING_DIRECTORY, folder_name)
    try:
        shutil.rmtree(folder_path)
        print(f"Папка '{folder_name}' успешно удалена.")
    except FileNotFoundError:
        print(f"Папка '{folder_name}' не найдена.")
    except OSError:
        print(f"Невозможно удалить папку '{folder_name}'. Папка не пуста или доступ к ней запрещен.")

def copy_file():
    source_file = input("Введите название файла для копирования: ")
    source_path = os.path.join(WORKING_DIRECTORY, source_file)
    if os.path.isfile(source_path):
        destination_folder = input("Введите название целевой папки для копирования: ")
        destination_path = os.path.join(WORKING_DIRECTORY, destination_folder)
        if os.path.isdir(destination_path):
            shutil.copy2(source_path, destination_path)
            print(f"Файл '{source_file}' успешно скопирован в папку '{destination_folder}'.")
        else:
            print(f"Целевая папка '{destination_folder}' не существует.")
    else:
        print(f"Файл '{source_file}' не найден.")

def move_file():
    source_file = input("Введите название файла для перемещения: ")
    source_path = os.path.join(WORKING_DIRECTORY, source_file)
    if os.path.isfile(source_path):
        destination_folder = input("Введите название целевой папки для перемещения: ")
        destination_path = os.path.join(WORKING_DIRECTORY, destination_folder)
        if os.path.isdir(destination_path):
            shutil.move(source_path, destination_path)
            print(f"Файл '{source_file}' успешно перемещен в папку '{destination_folder}'.")
        else:
            print(f"Целевая папка '{destination_folder}' не существует.")
    else:
        print(f"Файл '{source_file}' не найден.")

def rename_file():
    file_name = input("Введите название файла для переименования: ")
    file_path = os.path.join(WORKING_DIRECTORY, file_name)
    if os.path.isfile(file_path):
        new_name = input("Введите новое название файла: ")
        new_path = os.path.join(WORKING_DIRECTORY, new_name)
        try:
            os.rename(file_path, new_path)
            print(f"Файл успешно переименован в '{new_name}'.")
        except FileExistsError:
            print(f"Файл '{new_name}' уже существует.")
    else:
        print(f"Файл '{file_name}' не найден.")

def change_directory():
    global WORKING_DIRECTORY
    new_directory = input("Введите название целевой папки для перехода: ")
    new_path = os.path.join(WORKING_DIRECTORY, new_directory)
    if os.path.isdir(new_path):
        WORKING_DIRECTORY = new_path
        print(f"Вы перешли в папку '{new_directory}'.")
    else:
        print(f"Папка '{new_directory}' не найдена.")

def main():
    while True:
        print_menu()
        choice = input("Выберите действие (1-12): ")

        if choice == '1':
            list_files()
        elif choice == '2':
            create_folder()
        elif choice == '3':
            create_file()
        elif choice == '4':
            write_to_file()
        elif choice == '5':
            view_file_content()
        elif choice == '6':
            delete_file()
        elif choice == '7':
            delete_folder()
        elif choice == '8':
            copy_file()
        elif choice == '9':
            move_file()
        elif choice == '10':
            rename_file()
        elif choice == '11':
            change_directory()
        elif choice == '12':
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == '__main__':
    main()
