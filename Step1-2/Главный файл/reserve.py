import ftplib
from datetime import datetime
import shutil
import os


def reserve_file():
    # получение текущей даты и времени
    now = datetime.now()
    date_time = now.strftime("%d-%m-%y - %H-%M")

    # задание деталей FTP-сервера
    server = 'ftp.7215.ru'
    user = 'a0771402'
    password = 'diahcukeuh'
    destination_folder = '/domains/7215.ru/Reserve/'

    # создание копии файла
    original_file = '!Товары.xlsm'
    copy_file = 'copy_' + original_file
    shutil.copy(original_file, copy_file)

    # переименование файла с текущей датой и временем
    new_file = original_file.split('.')[0] + '-' + date_time + '.' + original_file.split('.')[1]
    os.rename(copy_file, new_file)

    # подключение и передача файла на FTP-сервер
    ftp = ftplib.FTP(server)
    ftp.login(user, password)
    with open(new_file, 'rb') as file:
        ftp.cwd(destination_folder)
        ftp.storbinary('STOR ' + new_file, file)

    # удаление переименованного файла
    os.remove(new_file)

    # отключение от FTP-сервера
    ftp.quit()