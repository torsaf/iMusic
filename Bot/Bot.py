import telebot
import openpyxl
from telebot import types
import csv
from tabulate import tabulate
import pandas as pd

bot = telebot.TeleBot("6065379061:AAE1oFujbxtkeeVmP-OyGNo-1aAJMZ8_onA")


@bot.message_handler(commands=['start'])
def process_start_command(message: types.Message):
    bot.send_message(message.chat.id, "Привет!\nПоработаем?🤓")


@bot.message_handler(commands=['help'])
def start(message):
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    url_button1 = types.InlineKeyboardButton(text="Ждите", callback_data='Ждите')
    url_button2 = types.InlineKeyboardButton(text="Гарантия", callback_data='Гарантия')
    url_button3 = types.InlineKeyboardButton(text="Наличие", callback_data='Наличие')
    url_button4 = types.InlineKeyboardButton(text="Не в наличии", callback_data='Не в наличии')
    url_button5 = types.InlineKeyboardButton(text="Продан", callback_data='Продан')
    url_button6 = types.InlineKeyboardButton(text="Торг", callback_data='Торг')
    url_button7 = types.InlineKeyboardButton(text="Оплата", callback_data='Оплата')
    url_button8 = types.InlineKeyboardButton(text="Доставка", callback_data='Доставка')
    url_button9 = types.InlineKeyboardButton(text="Авито-доставка", callback_data='Авито-доставка')
    url_button10 = types.InlineKeyboardButton(text="Транспортные", callback_data='Транспортные')
    url_button11 = types.InlineKeyboardButton(text="СДЭК", callback_data='СДЭК')
    url_button12 = types.InlineKeyboardButton(text="Заказ Иж", callback_data='Заказ Иж')
    url_button13 = types.InlineKeyboardButton(text="Заказ", callback_data='Заказ')
    url_button14 = types.InlineKeyboardButton(text="Кредит", callback_data='Кредит')
    url_button15 = types.InlineKeyboardButton(text="Дима", callback_data='Дима')
    url_button16 = types.InlineKeyboardButton(text="Зала нет", callback_data='Зала нет')
    url_button17 = types.InlineKeyboardButton(text="Оригинал", callback_data='Оригинал')
    url_button18 = types.InlineKeyboardButton(text="Отзыв", callback_data='Отзыв')
    url_button19 = types.InlineKeyboardButton(text="Выкуп", callback_data='Выкуп')
    url_button20 = types.InlineKeyboardButton(text="Состояние товара", callback_data='Состояние товара')
    keyboard.add(url_button1, url_button2, url_button3, url_button4, url_button5, url_button6, url_button7, url_button8,
                 url_button9, url_button10, url_button11, url_button12, url_button13, url_button14, url_button15,
                 url_button16, url_button17, url_button18, url_button19, url_button20)
    bot.send_message(message.chat.id, 'Быстрые ответы:', reply_markup=keyboard, parse_mode='html')


@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    book = openpyxl.open('Answer.xlsx', read_only=True)
    sheet = book.active
    cells = sheet['A1':'B24']
    if call.data == 'Ждите':
        bot.send_message(call.message.chat.id, cells[0][1].value)
    if call.data == 'Гарантия':
        bot.send_message(call.message.chat.id, cells[1][1].value)
    if call.data == 'Наличие':
        bot.send_message(call.message.chat.id, cells[2][1].value)
    if call.data == 'Не в наличии':
        bot.send_message(call.message.chat.id, cells[3][1].value)
    if call.data == 'Продан':
        bot.send_message(call.message.chat.id, cells[4][1].value)
    if call.data == 'Торг':
        bot.send_message(call.message.chat.id, cells[5][1].value)
    if call.data == 'Оплата':
        bot.send_message(call.message.chat.id, cells[6][1].value)
    if call.data == 'Доставка':
        bot.send_message(call.message.chat.id, cells[7][1].value)
    if call.data == 'Авито-доставка':
        bot.send_message(call.message.chat.id, cells[8][1].value)
    if call.data == 'Транспортные':
        bot.send_message(call.message.chat.id, cells[9][1].value)
    if call.data == 'СДЭК':
        bot.send_message(call.message.chat.id, cells[10][1].value)
    if call.data == 'Заказ Иж':
        bot.send_message(call.message.chat.id, cells[11][1].value)
    if call.data == 'Заказ':
        bot.send_message(call.message.chat.id, cells[12][1].value)
    if call.data == 'Кредит':
        bot.send_message(call.message.chat.id, cells[13][1].value)
    if call.data == 'Дима':
        bot.send_message(call.message.chat.id, cells[14][1].value)
    if call.data == 'Зала нет':
        bot.send_message(call.message.chat.id, cells[15][1].value)
    if call.data == 'Оригинал':
        bot.send_message(call.message.chat.id, cells[16][1].value)
    if call.data == 'Отзыв':
        bot.send_message(call.message.chat.id, cells[17][1].value)
    if call.data == 'Выкуп':
        bot.send_message(call.message.chat.id, cells[18][1].value)
    if call.data == 'Состояние товара':
        bot.send_message(call.message.chat.id, cells[19][1].value)


@bot.message_handler(content_types=["text"])
def price_list(message):
    if message.text.startswith('.') or message.text.startswith('. '):
        productname = []
        with open("!Forclients.csv", encoding='utf-8') as my_file:
            file_reader = csv.reader(my_file, delimiter=';')
            for row in file_reader:
                if message.text.lower()[1:].strip() in row[0].lower().rstrip():
                    productname.append(row)
        productname.sort(key=lambda t: int(t[1]))
        for i in productname:
            bot.send_message(message.chat.id, f'<b>{i[0]}</b>: {i[1]} р.', parse_mode='html')
        if len(productname) == 0:
            bot.send_message(message.chat.id,
                             'Такого товара нет в базе 🤔 или Вы не верно ввели название. Попробуйте указать только бренд искомого товара или 1-2 ключевых слов (как на авито!)',
                             parse_mode='html')
        bot.send_message(message.chat.id, f'✅Найдено результатов: {len(productname)}', parse_mode='html')
    else:
        productname = []
        article = []
        count = 0
        with open("!Name.csv", encoding='utf-8') as r_file:  # Открываем файл name
            file_reader = csv.reader(r_file)  # Присваиваем этому файлу переменную
            for row in file_reader:
                if message.text.lower().rstrip() in row[0].lower().rstrip():
                    result = [i for i in row if i != ''][1:]
                    article.append(result)
                    productname.append(row[0])
                    count += 1
                    if len(productname) >= 20:
                        bot.send_message(message.chat.id, 'Товаров слишком много. Вывожу несколько ...', parse_mode='html')
                        break
            if productname == []:
                bot.send_message(message.chat.id, 'Хм.. Какая то ошибка 🤔', parse_mode='html')
        for num in range(len(productname)):
            with open("!BD.csv", encoding='utf-8') as t_file:
                file_reader = csv.reader(t_file)
                lst = [['----', '-----', '---', '-----', '-----']]
                for row in file_reader:
                    for i in article[num]:
                        if i == row[1]:
                            lst.append([row[0] + ':', row[1], row[3], row[4], row[5]])

            df = pd.DataFrame(lst, columns=['', 'арт', 'нал', 'опт', 'ррц'])
            df = df.to_string(index=False)

            if len(df) > 53:  # это условие не выводит пустые поисковые значения, если товары не были найдены в прайсе поставщика
                bot.send_message(message.chat.id, f'<b>{productname[num]}</b>' + '\n\n' + f'<pre>{df}</pre>',
                                 parse_mode='html')  # Выводим наименование позиции с двумя пропусками и дата фрейм
            else:
                count -= 1
        keyboard = types.InlineKeyboardMarkup(row_width=5)
        url_button1 = types.InlineKeyboardButton(text="Trade", url="https://attrade.ru/catalog/")
        url_button2 = types.InlineKeyboardButton(text="Invask", url="https://invask.ru/partner/catalog/")
        url_button3 = types.InlineKeyboardButton(text="Slami", url="https://dealer.slami.ru/")
        url_button4 = types.InlineKeyboardButton(text="United", url="https://united-music.ru/ru/")
        keyboard.add(url_button1, url_button2, url_button3, url_button4)
        bot.send_message(message.chat.id, '✅ Найдено результатов: ' + f'<b>{count}</b>', reply_markup=keyboard,
                         parse_mode='html')


while True:
    try:
        bot.polling(none_stop=True)
    except:
        continue
