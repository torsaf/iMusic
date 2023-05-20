import pandas as pd
import pathlib
from pathlib import Path
import os
import xlrd


def go_step1():
    class Vendor:
        def __init__(self, name, shortname, start, art, model, nal, opt, rrc, ext='xls', sheet_name=0):
            self.name = name
            self.shortname = shortname
            self.start = start
            self.art = art
            self.model = model
            self.nal = nal
            self.opt = opt
            self.rrc = rrc
            self.ext = ext
            self.sheet_name = sheet_name

        def delit_CSV():
            """Удаляем старые файлы, что бы заполнить их заново"""
            if os.path.exists(Path(pathlib.Path.cwd(), "CSV", "!BD.csv")):
                os.remove(Path(pathlib.Path.cwd(), "CSV", "!BD.csv"))
            if os.path.exists(Path(pathlib.Path.cwd(), "CSV", "!Name.csv")):
                os.remove(Path(pathlib.Path.cwd(), "CSV", "!Name.csv"))

        def open_xls_file(self):
            """открывает XLS-файл"""
            if self.name == 'Invask':
                file_path = f"./Prices/{self.name}.{self.ext}"
                # откройте файл с помощью xlrd и прочитайте файл с помощью Pandas
                df = pd.read_excel(xlrd.open_workbook(file_path, encoding_override="windows-1251"), header=None).fillna(0).loc[self.start:, :]
            else:
                df = pd.read_excel(Path(pathlib.Path.cwd(), "Prices", f"{self.name}.{self.ext}"), sheet_name=self.sheet_name, header=None).loc[self.start:, :]
                df = df.fillna(0)
            self.re_name(df)

        def re_name(self, df):
            """Переименовывает столбцы в нужный вид"""
            df.rename(columns={self.art: 'Артикул', self.model: 'Модель', self.nal: 'Наличие', self.opt: 'ОПТ', self.rrc: 'РРЦ'}, inplace=True)
            df['Поставщик'] = self.name
            df = df[['Поставщик', 'Артикул', 'Модель', 'Наличие', 'ОПТ', 'РРЦ']]
            self.change_words(df)

        def change_words(self, df):
            # Определяем списки значений, которые требуется исключить
            exclude_values = ['Уточняйте ', 'Уточняйте', 'не для продажи в РФ', 'Çâîíèòå', '0', 'Звоните', 'витрина']
            # Фильтруем DataFrame, используя значение включающего оператора "и" (&)
            df = df.loc[~df['РРЦ'].isin(exclude_values) & ~df['ОПТ'].isin(exclude_values) & (df['РРЦ'] != 0) & (df['ОПТ'] != 0)]
            df = df.loc[(df['Наличие'] != 'витрина') & (df['ОПТ'] != 'витрина')]
            # Удаляем дубликаты
            df = df.drop_duplicates('Артикул')
            self.change_type(df)

        def change_type(self, df):
            """Убираем строки в ячейках которых, всякий мусор"""
            df = df.fillna(0)
            df[['ОПТ', 'РРЦ']] = df[['ОПТ', 'РРЦ']].astype(float).astype(int)
            df['Артикул'] = df['Артикул'].apply(lambda x: str(x).strip())
            df['Модель'] = df['Модель'].apply(lambda x: str(x).strip())
            self.tocsv(df)
            self.create_BD_file(df)

        def tocsv(self, df):
            """Сохраняет в CSV Файл всех поставщиков после того, как мы прибрались в столбцах"""
            df.to_csv(Path(pathlib.Path.cwd(), "CSV", f"{self.name}.csv"), sep=';', mode='w', index=False)

        def create_BD_file(self, df):
            """Создаёт файл !BD"""
            df['Поставщик'] = self.shortname
            df.to_csv(Path(pathlib.Path.cwd(), "CSV", "!BD.csv"), sep=';', mode='a', index=False)

        def create_Name_file():
            """Берёт из главного файла название и все артикулы и сохраняет в файл !Name"""
            df1 = pd.read_excel(Path(pathlib.Path.cwd(), "!Товары.xlsm"), sheet_name='General', header=None).iloc[2:, 10:31]
            df1 = df1[[10, 14, 15, 16, 17, 18, 19]]
            df1 = df1.applymap(lambda x: x.strip() if isinstance(x, str) else x)
            df1.to_csv(Path(pathlib.Path.cwd(), "CSV", "!Name.csv"), index=False)

        def create_general_file():
            """Из главного файла берет большинство столбцов и сохраняет в файл General, для второй части кода"""
            df = pd.read_excel(Path(pathlib.Path.cwd(), "!Товары.xlsm"), header=None).loc[1:, :]
            df = df[[0, 10, 14, 15, 16, 17, 18, 19]]
            df[[0, 10, 14, 15, 16, 17, 18, 19]] = df[[0, 10, 14, 15, 16, 17, 18, 19]].astype(str)
            df[[16, 17, 18, 19]] = df[[16, 17, 18, 19]].apply(lambda x: x.str.strip())
            df.rename(columns={0: 'Номер в Avito - Id', 10: 'Название объявления - Title', 14: 'Склад', 15: 'Цена склада', 16: 'Attrade', 17: 'Slami', 18: 'Invask', 19: 'United'}, inplace=True)
            df['Итоговая цена'] = 0
            df.to_csv(Path(pathlib.Path.cwd(), "CSV", "General.csv"), sep=';', mode='w', index=False)


    Attrade = Vendor('Attrade', 'ATT', 21, 1, 4, 7, 18, 11)
    Invask = Vendor('Invask', 'INV', 14, 0, 2, 8, 7, 6)
    Slami = Vendor('Slami', 'SLM', 5, 2, 4, 8, 7, 5)
    United = Vendor('United', 'UNT', 9, 1, 2, 5, 11, 9)

    Vendor.delit_CSV()
    Attrade.open_xls_file()
    Invask.open_xls_file()
    Slami.open_xls_file()
    United.open_xls_file()

    Vendor.create_Name_file()
    Vendor.create_general_file()