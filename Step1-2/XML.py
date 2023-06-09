import pandas as pd
from pathlib import Path
import pathlib
import sys

def from_file_to_xml():
    # Получаем текущую директорию
    dir_path = pathlib.Path.cwd()

    # Составляем путь до файла
    file_path = dir_path / "!Товары.xlsm"

    # Проверяем наличие файла и выводим сообщение
    if file_path.is_file() == False:
        print("Файл '!Товары.xlsm' не найден")
        input()
        sys.exit([0])

    # Указываем пути к файлам
    path = Path.cwd() / "!Товары.xlsm"
    path_xml = Path.cwd() / "XML.xml"

    # Читаем XLSX-файл и выбираем нужные столбцы
    df = pd.read_excel(path, header=None, sheet_name='General', usecols=[0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 20], skiprows=1).rename(
        columns={0: 'Id', 2: 'Category', 3: 'GoodsType', 4: 'AdType', 5: 'Address', 6: 'AllowEmail', 7: 'ContactPhone', 8: 'Condition', 9: 'ManagerName', 10: 'Title', 11: 'Description', 12: 'Images',
                 13: 'VideoURL', 20: 'Price'})
    # Удаляем строки, где цена равна 0 и конвертируем столбец 'Price' в тип float
    df = df[df['Price'] != 0].astype({'Price': float})
    # Заменяем цены, равные 1, на пропущенные значения
    df.loc[df['Price'] == 1, 'Price'] = pd.NA
    # Заполняем пустые значения в столбцах 'Price' и 'VideoURL'
    df[['Price', 'VideoURL']] = df[['Price', 'VideoURL']].fillna('')
    # Заменяем символ '&' на строку '&amp;' в нужных столбцах
    df[['Title', 'Description', 'Images', 'VideoURL']] = df[['Title', 'Description', 'Images', 'VideoURL']].replace('&', '&amp;', regex=True)

    # Функция, которая преобразует строки DataFrame в XML-строки
    def to_xml(df, filename=None, mode='w'):
        # Вложенная функция, которая преобразует одну строку DataFrame в одну XML-строку
        def row_to_xml(row):
            xml = ['<Ad>']
            for i, col_name in enumerate(row.index):
                xml.append(f'  <{col_name}>{row.iloc[i]}</{col_name}>')
            xml.append('</Ad>')
            return '\n'.join(xml)

        # Преобразуем все строки DataFrame в XML-строки
        res = '\n'.join(df.apply(row_to_xml, axis=1))

        # Если не указано имя файла, то возвращаем XML-строки
        if filename is None:
            return res
        # Иначе записываем полученные данные в указанный файл
        with open(filename, mode, encoding="utf-8") as f:
            f.write(res)

    # Добавляем метод to_xml в модуль DataFrame
    pd.DataFrame.to_xml = to_xml

    # Строки, которые будут записаны в начале и конце XML-файла
    a = '<?xml version="1.0" encoding="UTF-8"?>\n<Ads formatVersion="3" target="Avito.ru">\n'
    b = '\n</Ads>'

    # Записываем данные в XML-файл
    with open(path_xml, "w", encoding="utf-8") as h:
        h.write(a + df.to_xml() + b)
