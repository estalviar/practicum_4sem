import os
import shutil


def info():
    print('Доступны следующие команды в формате:\n[команда] [название файла/папки]:')
    c = ['выход', 'создать', 'переименовать', 'удалить', 'назад', 'вперед',
         'настройки', 'справка', 'где', 'показать', 'редактировать', 'читать', 'копировать', 'переместить']
    print(c)


def dontunderstand():
    print('Я не понял. Хотите вызвать справку? [да/нет]')
    yn = input()
    if yn == 'да':
        info()
    else:
        print('Ладно.')


def creating(name, a):
    try:
        if a:
            print('Создаю файл...')
            open(name, 'a').close()
        elif not a:
            print('Создаю папку...')
            os.mkdir(os.path.normpath(os.getcwd() + '/' + name), mode=0o777)
        else:
            dontunderstand()
    except FileExistsError:
        print('Файл/папка уже существует. Попробуйте изменить название.')


def deleting(name, a):
    if a:
        shutil.rmtree(os.path.normpath(os.getcwd() + '/' + name), ignore_errors=False, onerror=None)
        print(f'Папка {name} удалена')
    elif not a:
        os.remove(name)
        print(f'Файл {name} удален')
    else:
        print('Кажется такого файла/папки не существует.')


def renaming(oldname):
    print('Введите новое имя:')
    newname = str(input())
    os.rename(oldname, newname)
    print('Переименовано.')


def read(name, a):
    if a:
        file = open(name, 'r')
        print('Вывожу содержимое файла {}'.format(name))
        print(file.readlines())
        file.close()
    else:
        print('Кажется это папка, а не файл.')


def change(name, a):
    if a:
        file = open(name, 'w+')
        print('Введите желамое:')
        i = str(input())
        file.write(i)
        file.close()
    else:
        print('Кажется это папка, а не файл.')


def up(name, a):
    if a:
        print('Кажется это файл, а не папка.')
    elif not a:
        print('Перехожу в папку {}...'.format(name))
        os.chdir(os.getcwd() + '/' + name)
        print(f'Текущая папка {os.getcwd()}')


def copying(name, drr):
    print(drr)
    print('Укажите абсолютный путь до папки, куда создать копию:')
    i = str(input())
    try:
        fp = os.path.normpath(os.getcwd() + '/' + name)
        ds = os.path.normpath(i)
        shutil.copy(fp, ds)
    except FileNotFoundError and PermissionError:
        print('Для создания копии необходимо находится в папке оригинала.\nИ копировать можно только файлы.')


def moving(name):
    print('Укажите абсолютный путь до папки, куда переместить:')
    i = str(input())
    try:
        fp = os.path.normpath(os.getcwd() + '/' + name)
        ds = os.path.normpath(i)
        shutil.move(fp, ds)
        print(fp)
        print(ds)
    except (FileNotFoundError):
        print('Для перемещения необходимо находится в папке оригинала.')


def down(drr):
    a = os.getcwd()
    if a == drr:
        print('Вы находитесь в корневой папке.')
    else:
        print('Перехожу назад...')
        os.chdir('..')
        print(f'Текущая папка {os.getcwd()}')


def main():
    with open('settings.txt', 'r') as settings:
        drr = os.path.normpath(settings.readline())
        print('Корневая директория', drr)
        settings.close()
    os.chdir(drr)

    while True:
        print('Введите команду:')
        act = input().split(' ')
        if len(act) > 1:
            if '.' in act[1]:
                a = True
            else:
                a = False

        if act[0] == 'выход':
            print('До свидания!')
            break

        elif act[0] == 'справка':
            info()

        elif act[0] == 'создать':
            creating(str(act[1]), a)

        elif act[0] == 'удалить':
            deleting(str(act[1]), a)

        elif act[0] == 'переименовать':
            renaming(str(act[1]))

        elif act[0] == 'где':
            print(os.getcwd())

        elif act[0] == 'показать':
            print(os.listdir())

        elif act[0] == 'вперед':
            try:
                up(act[1], a)
            except IndexError:
                print('Название папки отсутствует')
            except FileNotFoundError:
                print('Папка не существует')

        elif act[0] == 'назад':
            down(drr)

        elif act[0] == 'редактировать':
            change(str(act[1]), a)

        elif act[0] == 'читать':
            read(str(act[1]), a)

        elif act[0] == 'копировать':
            copying(str(act[1]), drr)

        elif act[0] == 'переместить':
            moving(str(act[1]))

        else:
            dontunderstand()


main()
