import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from bs4 import BeautifulSoup
import requests
from telebot import types
from random import choice
import pandas as pd
from config_reader import config
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import F

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Для записей с типом Secret* необходимо
# вызывать метод get_secret_value(),
# чтобы получить настоящее содержимое вместо '*******'
bot = Bot(token=config.bot_token.get_secret_value())
# Диспетчер
dp = Dispatcher()

# keyboards
day = InlineKeyboardButton(
    text="Цитата дня", callback_data='day')
book = InlineKeyboardButton(
    text="Цитата из книг", callback_data='book')
rand = InlineKeyboardButton(
    text="Случайная цитата", callback_data='rand')
inline_main_kb = InlineKeyboardMarkup(inline_keyboard=[[day], [book], [rand]])

new_book = InlineKeyboardButton(
    text="Другая цитата из книги", callback_data='another_book_quote')

ret_book = InlineKeyboardButton(
    text="Назад", callback_data='back')
inline_book_kb = InlineKeyboardMarkup(inline_keyboard=[[new_book], [ret_book]])

new_rand = InlineKeyboardButton(
    text="Другая цитата", callback_data='another_rand_quote')

ret_rand = InlineKeyboardButton(
    text="Назад", callback_data='back_rand')
inline_rand_kb = InlineKeyboardMarkup(inline_keyboard=[[new_rand], [ret_rand]])

ci = []
# Создаем список из цитат из книг (их берем из файла с цитатами)
def get_ci():
    global ci
    ci = []
    url = 'https://storage.yandexcloud.net/citatnik-bot/quotes_book.csv'
    df = pd.read_csv(url, encoding='utf-8')
    print(df)
    # Считывание данных из CSV файла
    for i in range(len(df)):
        ci.append(f' {df["Цитата"][i]}\nАвтор: {df["Автор"][i]}\nИз книги: {df["Книга"][i]}')


get_ci()


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

print(get_random_quote())
# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет, чем я могу тебе помочь?", reply_markup=inline_main_kb)

@dp.message(Command("clear"))
async def cmd_start(message: types.Message):
    await message.answer("Привет, чем я могу тебе помочь?", reply_markup=inline_main_kb)



@dp.callback_query(F.data == "day")
async def send_daily_quote(callback: types.CallbackQuery):
    await callback.message.answer(get_daily_quote(), reply_markup=inline_main_kb)


@dp.callback_query(F.data == "book")
async def send_daily_quote(callback: types.CallbackQuery):
    await callback.message.answer(get_book_quote(), reply_markup=inline_book_kb)

@dp.callback_query(F.data == "another_book_quote")
async def send_daily_quote(callback: types.CallbackQuery):
    await callback.message.answer(get_book_quote(), reply_markup=inline_book_kb)

@dp.callback_query(F.data == "back")
async def send_daily_quote(callback: types.CallbackQuery):
    await callback.message.answer("Привет, чем я могу тебе помочь?", reply_markup=inline_main_kb)


@dp.callback_query(F.data == "rand")
async def send_daily_quote(callback: types.CallbackQuery):
    await callback.message.answer(get_random_quote(), reply_markup=inline_rand_kb)
@dp.callback_query(F.data == "another_rand_quote")
async def send_daily_quote(callback: types.CallbackQuery):
    await callback.message.answer(get_random_quote(), reply_markup=inline_rand_kb)
@dp.callback_query(F.data == "back_rand")
async def send_daily_quote(callback: types.CallbackQuery):
    await callback.message.answer("Привет, чем я могу тебе помочь?", reply_markup=inline_main_kb)


@dp.message()
async def handle_docs_audio(message: types.Message):
    await message.answer( text="Некорректный ввод")


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
