from bs4 import BeautifulSoup
import requests
import telebot
from telebot import types
import csv
from random import choice
import pandas as pd
import json

from bot_token import token, api_key_for_random_quote
from urllib.parse import urlencode


bot = telebot.TeleBot(token)

keyboard = types.ReplyKeyboardMarkup(row_width=1)  # наша клавиатура
itembtn1 = types.KeyboardButton('Цитата дня')  # создадим кнопку
itembtn2 = types.KeyboardButton('Цитата из книг')
itembtn3 = types.KeyboardButton('Случайная цитата')
keyboard.add(itembtn1, itembtn2, itembtn3)  # добавим кнопки 1  2  3 на первый ряд

ci = []

# Создаем список из цитат из книг (их берем из файла с цитатами)
def get_ci():
    global ci
    ci = []
    url = 'https://storage.yandexcloud.net/citatnik-bot/quotes_book.csv'
    df = pd.read_csv(url,encoding='utf-8')
    print(df)
    # Считывание данных из CSV файла
    for i in range(len(df)):
        ci.append(f' {df["Цитата"][i]}\nАвтор: {df["Автор"][i]}\nИз книги: {df["Книга"][i]}')


get_ci()
print(ci)


# Возвращает случайную цитату из книги
def get_book_quote():
    return choice(ci)


# Возвращает цитату дня с сайта citatko.com
def get_daily_quote():
    try:
        request = requests.get('https://citatko.com/tsitata-dnya')
        b = BeautifulSoup(request.text, "html.parser")
        p3 = b.find("div", {"id": "quote-content"}).get_text()
        return p3
    except:
        return 'Что-то пошло не так'


# возвращает случайную цитату
def get_random_quote():
    try:
        request = requests.get('https://citbase.ru/random')
        b = BeautifulSoup(request.text, "html.parser")
        p3 = b.find("pre", {"class": "mb-4"}).get_text()
        author = b.find("span", {'class': 'mr-2 last:mr-0'}).get_text().strip()
        return p3 + '\n' + author
    except:
        return 'Что-то пошло не так'


# привязываем функции к кнопкам на клавиатуре
def callback_worker(call):
    msg = None
    if call.text == "Цитата дня":
        msg = bot.send_message(call.chat.id, get_daily_quote(), reply_markup=keyboard)

    elif call.text == "Цитата из книг":
        msg = bot.send_message(call.chat.id, get_book_quote(), reply_markup=keyboard)

    elif call.text == "Случайная цитата":
        msg = bot.send_message(call.chat.id, get_random_quote(), reply_markup=keyboard)
    if msg:
        bot.register_next_step_handler(msg, callback_worker)


# напишем, что делать нашему боту при команде старт
@bot.message_handler(commands=['start'])  # декоратор
def send_keyboard(message, text="Привет, чем я могу тебе помочь?"):
    msg = None
    # пришлем это все сообщением и запишем выбранный вариант
    msg = bot.send_message(message.from_user.id,
                           text=text, reply_markup=keyboard)  # бот возращает юзеру клавиатуру с кнопками

    # отправим этот вариант в функцию, которая его обработает
    if msg:
        bot.register_next_step_handler(msg, callback_worker)


@bot.message_handler(content_types=['text'])
def handle_docs_audio(message):
    send_keyboard(message, text="Я не понимаю :-( Выберите один из пунктов меню:")


bot.polling(none_stop=True)




