import io
import os
import zipfile
import requests
import pathlib
from pathlib import Path
from zipfile import ZipFile
from urllib import request
import wget


def download_prices():
    # Создаем директорию 'Prices', если она не существует
    if not os.path.exists('Prices'):
        os.makedirs('Prices')

    # Список ссылок поставщиков
    links = {
        'Attrade': 'https://attrade.ru/pr30fe16ff-24c4-4bd1-be40-69cbd4593924/TempFolder/Price_Stock.zip',
        'Invask': 'https://invask.ru/downloads/Ostatki_tovara.xls?v=1',
        'Slami': 'http://www.slami.ru/info/dilprice_slami.zip',
        'United': 'https://united-music.by/dealers/UM_PRICE_RUR.xls'
    }

    def Attrade():
        # Удаляем старый файл, если он есть
        if os.path.exists('Prices/Attrade.xls'):
            os.remove(Path(pathlib.Path.cwd(), 'Prices/Attrade.xls'))
        # Скачиваем прайс лист и разархивируем его
        r = requests.get(links['Attrade'])
        with r, zipfile.ZipFile(io.BytesIO(r.content)) as archive:
            archive.extractall('Prices')
            os.rename('Prices/Price_Stock.XLS', 'Prices/Attrade.xls')

    def Invask():
        if os.path.exists('Prices/Invask.xls'):
            os.remove(Path(pathlib.Path.cwd(), 'Prices/Invask.xls'))
        wget.download(links['Invask'], 'Prices/Invask.xls')

    def Slami():
        # Удаляем старый файл, если он есть
        if os.path.exists('Prices/Slami.xls'):
            os.remove(Path(pathlib.Path.cwd(), 'Prices/Slami.xls'))
        # Загружаем архив и ищем название файла внутри
        filename = wget.download(links['Slami'], 'Prices')
        with ZipFile(filename, 'r') as myzip:
            name1 = myzip.namelist()[0]
            myzip.extract(name1, 'Prices')
            os.rename(f'Prices/{name1}', 'Prices/Slami.xls')

        os.remove(filename)  # удаляем архив

    def United():
        # Удаляем старый файл, если он есть
        if os.path.exists('Prices/United.xls'):
            os.remove(Path(pathlib.Path.cwd(), 'Prices/United.xls'))
        # Скачиваем файл и переименовываем
        wget.download(links['United'], 'Prices/United.xls')

    # Проверяем каждую ссылку поставщика и вызываем функцию соответствующего поставщика, если ссылка работает
    for supplier, link in links.items():
        try:
            response = requests.get(link)
            response.raise_for_status()

            # Вызываем функцию соответствующего поставщика
            if supplier == 'Attrade':
                Attrade()
            elif supplier == 'Invask':
                Invask()
            elif supplier == 'Slami':
                Slami()
            elif supplier == 'United':
                United()

        except (requests.exceptions.RequestException, FileNotFoundError) as e:
            if isinstance(e, FileNotFoundError):
                print()
                print(f'Файл ссылки поставщика {supplier} не найден')
            else:
                print()
                print(f'Ссылка поставщика {supplier} не работает', end='\n')
