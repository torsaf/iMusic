from ftplib import FTP


def files_to_ftp():
    # Настройки FTP сервера
    ftp_server_address = 'ftp.7215.ru'
    ftp_directory = '/domains/a0771402.xsph.ru/Bot/'
    ftp_username = 'a0771402'
    ftp_password = 'diahcukeuh'

    # Список файлов, которые нужно отправить
    file_names = ['!BD.csv', '!Forclients.csv', '!Name.csv']

    # Создаем соединение с FTP сервером
    ftp = FTP(ftp_server_address)
    ftp.login(user=ftp_username, passwd=ftp_password)

    # Переходим в нужную директорию на сервере
    ftp.cwd(ftp_directory)

    # Отправляем каждый файл в список
    for file_name in file_names:
        file_path = 'CSV/' + file_name  # путь к файлу
        with open(file_path, 'rb') as file:
            ftp.storbinary(f'STOR {file_name}', file)  # отправляем файл на сервер

    # Закрываем соединение
    ftp.quit()
