import telebot
from telebot import types
import json

bot = telebot.TeleBot("881872217:AAHjDOnnKDXr5D5LnyphqkO7Roe4QboXhTA")

chat = []

bookslist = [{"text": "Kaplan Prep Book 4/5", "id": "BQACAgIAAxkBAAMhXklypBJyY-RvQGXBWa8SARLgIycAAnMFAAL9rFBKk7m2Y4uCJmsYBA"},
             {"text": "Cracking the SAT 5/5", "id": "BQACAgIAAxkBAAM0Xkl2loQAAdwDhMAIDdyN5oE9ywehAALZBAACgTRISgnQSBWIN8vDGAQ"}]


@bot.message_handler(commands=['start'])
def send_welcome(message):
    id = message.json["chat"]["id"]
    chat.append(id)
    bot.send_message(id, "Привет! Это бот помогающий в подготовке к SAT")
    markup = types.InlineKeyboardMarkup()
    btn_books = types.InlineKeyboardButton(text='Книги', callback_data="books")
    btn_tests = types.InlineKeyboardButton(text="Тесты для подготоки", callback_data="tests")
    btn_about = types.InlineKeyboardButton(text="О боте", callback_data="about")
    markup.add(btn_books)
    markup.add(btn_tests)
    markup.add(btn_about)
    bot.send_message(id, "Меню", reply_markup=markup)


@bot.message_handler(func=lambda message: message.data == "books")
def books(message):
    for book in bookslist:
        bot.send_document(message.from_user.id, book["id"])


@bot.message_handler(content_types=['document'])
def add_book(message):
    file_id = message.document.file_id
    title = message.document.file_name
    bookslist.append({"text": title, "id": file_id})


bot.polling()
